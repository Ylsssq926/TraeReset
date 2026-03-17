#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TraeReset - Trae IDE 设备限制重置工具
制作人: 掠蓝 | 交流群: 676475076
"""

import json, os, platform, shutil, subprocess, uuid, secrets
import traceback, sys, ctypes
from datetime import datetime

if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

import customtkinter as ctk
from tkinter import messagebox, filedialog

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ─── 色彩系统 (蓝白) ─────────────────────────────────────────

BG       = "#f0f4f8"
BG_CARD  = "#ffffff"
BG_HEAD  = "#1a56db"
BG_HEAD2 = "#1e40af"
BG_LOG   = "#f8fafc"
BG_INPUT = "#f1f5f9"

FG       = "#1e293b"
FG_DIM   = "#94a3b8"
FG_BODY  = "#475569"
FG_LINK  = "#1a56db"
FG_WHITE = "#ffffff"
FG_SUB   = "#bfdbfe"

BLUE     = "#1a56db"
BLUE_H   = "#1e40af"
RED      = "#dc2626"
RED_H    = "#b91c1c"
AMBER    = "#d97706"
AMBER_H  = "#b45309"
GHOST    = "#e2e8f0"
GHOST_H  = "#cbd5e1"
BORDER   = "#e2e8f0"
GREEN    = "#16a34a"

VERSION = "1.0.0"
APP_NAME = "TraeReset"
APP_TITLE = f"TraeReset v{VERSION}"

# ─── 平台 & 常量 ─────────────────────────────────────────────

IS_WIN = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"

if IS_WIN:
    DATA_DIR_DEFAULT = os.path.join(os.environ.get("APPDATA", ""), "Trae")
    DIR_HINT = "%APPDATA%\\Trae"
    FONT_UI = "Microsoft YaHei UI"
    FONT_MONO = "Consolas"
elif IS_MAC:
    DATA_DIR_DEFAULT = os.path.join(
        os.path.expanduser("~"), "Library", "Application Support", "Trae")
    DIR_HINT = "~/Library/Application Support/Trae"
    FONT_UI = "PingFang SC"
    FONT_MONO = "Menlo"
else:
    DATA_DIR_DEFAULT = os.path.join(os.path.expanduser("~"), ".config", "Trae")
    DIR_HINT = "~/.config/Trae"
    FONT_UI = "Noto Sans CJK SC"
    FONT_MONO = "Noto Sans Mono"

STORAGE_REL = os.path.join("User", "globalStorage", "storage.json")
AUTH_KEY_PATTERNS = [
    "iCubeAuthInfo://", "iCubeServerData://", "-entitlement-notified"]
COOKIE_PATHS = [
    os.path.join("Network", "Cookies"),
    os.path.join("Network", "Cookies-journal"),
    os.path.join("Partitions", "icube-web-crawler-shared-session-v1.0",
                 "Network", "Cookies"),
    os.path.join("Partitions", "icube-web-crawler-shared-session-v1.0",
                 "Network", "Cookies-journal"),
    os.path.join("Partitions", "trae-webview", "Network", "Cookies"),
    os.path.join("Partitions", "trae-webview", "Network", "Cookies-journal"),
]
GUIDE_TIPS = [
    "使用前请先关闭 Trae，否则修改不生效或文件被锁定",
    "提示「设备数量已达上限」? 点「一键重置」就行",
    "重置后重新打开 Trae，用新账号登录即可",
    "所有操作会自动备份原文件（.bak），可手动恢复",
    "如果工具检测不到目录，点「自定义目录」手动选择",
]

# ─── 免责声明记忆 ────────────────────────────────────────────

def _get_config_path():
    """配置文件路径，存到用户目录下，确保打包后也能持久化"""
    if IS_WIN:
        base = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")),
                            "TraeUnlock")
    elif IS_MAC:
        base = os.path.join(os.path.expanduser("~"),
                            "Library", "Application Support", "TraeUnlock")
    else:
        base = os.path.join(os.path.expanduser("~"), ".config", "TraeUnlock")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "config.json")

def has_accepted_disclaimer():
    try:
        with open(_get_config_path(), "r", encoding="utf-8") as f:
            return json.load(f).get("disclaimer_accepted", False)
    except Exception:
        return False

def save_disclaimer_accepted():
    try:
        with open(_get_config_path(), "w", encoding="utf-8") as f:
            json.dump({"disclaimer_accepted": True}, f)
    except Exception:
        pass

# ─── 管理员权限 ──────────────────────────────────────────────

def is_admin():
    if IS_WIN:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    return os.geteuid() == 0 if hasattr(os, "geteuid") else True

def restart_as_admin():
    if IS_WIN:
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable,
                " ".join([f'"{a}"' for a in sys.argv]), None, 1)
            return True
        except Exception:
            return False
    return False

# ─── 核心逻辑 ────────────────────────────────────────────────

def is_valid_trae_dir(path):
    return (os.path.isfile(os.path.join(path, "machineid"))
            or os.path.isfile(os.path.join(path, STORAGE_REL)))

def is_trae_running():
    try:
        if IS_WIN:
            out = subprocess.check_output(
                ["tasklist"], creationflags=0x08000000, text=True, timeout=10)
            return "trae.exe" in out.lower()
        else:
            out = subprocess.check_output(["ps", "aux"], text=True, timeout=10)
            return "/trae" in out.lower()
    except Exception:
        return False

def read_storage(data_dir):
    path = os.path.join(data_dir, STORAGE_REL)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

def write_storage(data_dir, data):
    path = os.path.join(data_dir, STORAGE_REL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        shutil.copy2(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_machineid(data_dir):
    path = os.path.join(data_dir, "machineid")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_status(data_dir):
    info = {"machine_id": read_machineid(data_dir) or "未找到",
            "dev_device_id": "未找到", "accounts": []}
    storage = read_storage(data_dir)
    if not storage:
        return info
    info["dev_device_id"] = storage.get("telemetry.devDeviceId", "未找到")
    for key, val in storage.items():
        if not key.startswith("iCubeAuthInfo://icube.cloudide"):
            continue
        try:
            auth = json.loads(val) if isinstance(val, str) else val
            acct = auth.get("account", {})
            name = acct.get("username", "未知")
            ct = acct.get("email", "") or acct.get("nonPlainTextMobile", "")
            info["accounts"].append(f"{name} ({ct})" if ct else name)
        except Exception:
            info["accounts"].append("(解析失败)")
    return info

def clear_accounts(data_dir):
    logs, removed = [], 0
    storage = read_storage(data_dir)
    if storage:
        keys = [k for k in list(storage.keys())
                if any(p in k for p in AUTH_KEY_PATTERNS)]
        for k in keys:
            del storage[k]
            logs.append(f"  删除: {k}")
            removed += 1
        if keys:
            write_storage(data_dir, storage)
    else:
        logs.append("  未找到 storage.json")
    for rel in COOKIE_PATHS:
        full = os.path.join(data_dir, rel)
        if os.path.isfile(full):
            try:
                os.remove(full)
                logs.append(f"  删除: {rel}")
                removed += 1
            except OSError as e:
                logs.append(f"  失败 {rel}: {e}")
    if removed == 0:
        logs.append("  没有需要清除的内容")
    return logs, removed

def reset_device_id(data_dir):
    logs = []
    mid_path = os.path.join(data_dir, "machineid")
    os.makedirs(os.path.dirname(mid_path) or ".", exist_ok=True)
    new_mid = str(uuid.uuid4())
    if os.path.isfile(mid_path):
        shutil.copy2(mid_path, mid_path + ".bak")
    with open(mid_path, "w", encoding="utf-8") as f:
        f.write(new_mid)
    logs.append(f"  Machine ID: {new_mid}")
    storage = read_storage(data_dir)
    if storage:
        nt = secrets.token_hex(32)
        ns = "{" + str(uuid.uuid4()).upper() + "}"
        nd = str(uuid.uuid4())
        storage["telemetry.machineId"] = nt
        storage["telemetry.sqmId"] = ns
        storage["telemetry.devDeviceId"] = nd
        storage["has_device_id_updated_to_aha"] = "false"
        write_storage(data_dir, storage)
        logs.append(f"  telemetry.machineId: {nt[:20]}...")
        logs.append(f"  telemetry.devDeviceId: {nd}")
    else:
        logs.append("  未找到 storage.json，仅更新了 machineid")
    return logs

def verify_write(data_dir, expected_mid):
    """写入后验证文件是否真的改了"""
    actual = read_machineid(data_dir)
    if actual != expected_mid:
        return False, f"machineid 验证失败: 期望 {expected_mid[:12]}... 实际 {(actual or '空')[:12]}..."
    st = read_storage(data_dir)
    if st and st.get("telemetry.devDeviceId", "") == "":
        return False, "storage.json 中 devDeviceId 为空"
    return True, "文件验证通过"

def restore_backup(data_dir):
    logs, restored = [], 0
    targets = [
        ("machineid",    os.path.join(data_dir, "machineid")),
        ("storage.json", os.path.join(data_dir, STORAGE_REL)),
    ]
    for name, dst in targets:
        bak = dst + ".bak"
        if os.path.isfile(bak):
            shutil.copy2(bak, dst)
            logs.append(f"  已恢复: {name}")
            restored += 1
        else:
            logs.append(f"  未找到 {name}.bak")
    if restored == 0:
        logs.append("  没有找到任何备份文件")
    return logs, restored

# ─── 主应用 ──────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG)
        self.title(APP_TITLE)
        self.current_dir = None

        # 窗口尺寸 & 居中
        W, H = 780, 760
        self.update_idletasks()
        sx = self.winfo_screenwidth()
        sy = self.winfo_screenheight()
        x = max(0, (sx - W) // 2)
        y = max(0, (sy - H) // 2)
        self.geometry(f"{W}x{H}+{x}+{y}")
        self.minsize(720, 680)

        self.main_frame = ctk.CTkFrame(self, fg_color=BG)
        self.disclaimer_frame = ctk.CTkFrame(self, fg_color=BG)
        self._build_disclaimer()
        self._build_main()

        # 已同意过免责声明则直接进主界面
        if has_accepted_disclaimer():
            self.main_frame.pack(fill="both", expand=True)
            self.after(100, self._on_startup)
        else:
            self.disclaimer_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # ─── 免责声明页 ──────────────────────────────────────────

    def _build_disclaimer(self):
        f = self.disclaimer_frame
        wrap = ctk.CTkFrame(f, fg_color="transparent")
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        logo = ctk.CTkFrame(wrap, fg_color=BLUE, corner_radius=16,
                            width=64, height=64)
        logo.pack(pady=(0, 14))
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="T",
                     font=ctk.CTkFont(family=FONT_UI, size=30, weight="bold"),
                     text_color=FG_WHITE).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(wrap, text="TraeReset",
                     font=ctk.CTkFont(family=FONT_UI, size=24, weight="bold"),
                     text_color=FG).pack(pady=(0, 4))
        ctk.CTkLabel(wrap, text="Trae 设备限制重置工具  ·  by 掠蓝  ·  交流群 676475076",
                     font=ctk.CTkFont(family=FONT_UI, size=12),
                     text_color=FG_DIM).pack(pady=(0, 24))

        # 声明卡片
        card = ctk.CTkFrame(wrap, fg_color=BG_CARD, corner_radius=12,
                            border_width=1, border_color=BORDER)
        card.pack(fill="x")

        # 橙色顶部条
        bar = ctk.CTkFrame(card, fg_color=AMBER, height=3, corner_radius=0)
        bar.pack(fill="x")

        ctk.CTkLabel(card, text="  免责声明",
                     font=ctk.CTkFont(family=FONT_UI, size=15, weight="bold"),
                     text_color=AMBER).pack(anchor="w", padx=20, pady=(14, 8))

        tb = ctk.CTkTextbox(card, width=480, height=180,
                            font=ctk.CTkFont(family=FONT_UI, size=13),
                            fg_color=BG_INPUT, corner_radius=8,
                            text_color=FG_BODY, wrap="word",
                            activate_scrollbars=False)
        tb.insert("1.0",
            "1. 本工具仅供个人学习与技术研究使用，请勿用于商业或非法用途。\n\n"
            "2. 使用本工具产生的一切后果由使用者自行承担，与作者无关。\n\n"
            "3. 本工具不修改 Trae 软件本体，仅操作本地用户数据文件。\n\n"
            "4. 如侵犯相关权利，请联系作者删除。")
        tb.configure(state="disabled")
        tb.pack(padx=20, pady=(0, 20), fill="both")

        # 按钮
        brow = ctk.CTkFrame(wrap, fg_color="transparent")
        brow.pack(pady=(20, 0))
        ctk.CTkButton(brow, text="同意并继续", width=180, height=46,
                      font=ctk.CTkFont(family=FONT_UI, size=15, weight="bold"),
                      fg_color=BLUE, hover_color=BLUE_H,
                      text_color=FG_WHITE, corner_radius=10,
                      command=self._accept).pack(side="left", padx=(0, 12))
        ctk.CTkButton(brow, text="不同意，退出", width=160, height=46,
                      font=ctk.CTkFont(family=FONT_UI, size=15),
                      fg_color=GHOST, hover_color=GHOST_H,
                      text_color=FG_BODY, corner_radius=10,
                      command=self._reject).pack(side="left")

    def _accept(self):
        save_disclaimer_accepted()
        self.disclaimer_frame.place_forget()
        self.main_frame.pack(fill="both", expand=True)
        self._on_startup()

    def _reject(self):
        self.destroy()
        sys.exit(0)

    # ─── 主界面 ──────────────────────────────────────────────

    def _build_main(self):
        m = self.main_frame

        # ── 顶部蓝色标题栏 ──
        hdr = ctk.CTkFrame(m, fg_color=BG_HEAD, corner_radius=0, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        ctk.CTkLabel(hdr, text="  T",
                     font=ctk.CTkFont(family=FONT_UI, size=20, weight="bold"),
                     text_color=FG_WHITE, fg_color=BG_HEAD2,
                     corner_radius=6, width=36, height=36).pack(
            side="left", padx=(16, 10), pady=10)
        ctk.CTkLabel(hdr, text="TraeReset",
                     font=ctk.CTkFont(family=FONT_UI, size=17, weight="bold"),
                     text_color=FG_WHITE).pack(side="left")
        ctk.CTkLabel(hdr, text=f"v{VERSION}  ·  by 掠蓝",
                     font=ctk.CTkFont(family=FONT_UI, size=12),
                     text_color=FG_SUB).pack(side="left", padx=(8, 0))

        ctk.CTkButton(hdr, text="关于", width=52, height=30,
                      font=ctk.CTkFont(family=FONT_UI, size=12),
                      fg_color=BLUE_H, hover_color=BLUE,
                      text_color=FG_SUB, corner_radius=6,
                      command=self._on_about).pack(side="right", padx=(0, 16), pady=13)

        # ── 可滚动内容区 ──
        content = ctk.CTkScrollableFrame(m, fg_color="transparent",
                                         scrollbar_button_color=GHOST,
                                         scrollbar_button_hover_color=GHOST_H)
        content.pack(fill="both", expand=True, padx=20, pady=(14, 10))

        # ── 目录卡片 ──
        self._card_dir = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=10,
                                      border_width=1, border_color=BORDER)
        self._card_dir.pack(fill="x", pady=(0, 10))
        di = ctk.CTkFrame(self._card_dir, fg_color="transparent")
        di.pack(fill="x", padx=20, pady=16)

        dl = ctk.CTkFrame(di, fg_color="transparent")
        dl.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(dl, text="数据目录",
                     font=ctk.CTkFont(family=FONT_UI, size=15, weight="bold"),
                     text_color=FG).pack(anchor="w")
        self.dir_label = ctk.CTkLabel(
            dl, text="未选择 — 请点击右侧按钮选择",
            font=ctk.CTkFont(family=FONT_MONO, size=12), text_color=FG_DIM)
        self.dir_label.pack(anchor="w", pady=(4, 0))

        dr = ctk.CTkFrame(di, fg_color="transparent")
        dr.pack(side="right")
        ctk.CTkButton(dr, text="选择目录", width=90, height=34,
                      font=ctk.CTkFont(family=FONT_UI, size=12),
                      fg_color=BLUE, hover_color=BLUE_H,
                      text_color=FG_WHITE, corner_radius=8,
                      command=self._on_browse).pack(side="left", padx=(0, 8))
        ctk.CTkButton(dr, text="恢复备份", width=90, height=34,
                      font=ctk.CTkFont(family=FONT_UI, size=12),
                      fg_color=GHOST, hover_color=GHOST_H,
                      text_color=FG_BODY, corner_radius=6,
                      command=self._on_restore).pack(side="left")

        # ── 状态卡片 ──
        sc = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=10,
                          border_width=1, border_color=BORDER)
        sc.pack(fill="x", pady=(0, 10))
        si = ctk.CTkFrame(sc, fg_color="transparent")
        si.pack(fill="x", padx=20, pady=16)

        st_top = ctk.CTkFrame(si, fg_color="transparent")
        st_top.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(st_top, text="当前状态",
                     font=ctk.CTkFont(family=FONT_UI, size=15, weight="bold"),
                     text_color=FG).pack(side="left")
        ctk.CTkButton(st_top, text="刷新", width=56, height=28,
                      font=ctk.CTkFont(family=FONT_UI, size=12),
                      fg_color=GHOST, hover_color=GHOST_H,
                      text_color=FG_BODY, corner_radius=5,
                      command=self._on_refresh).pack(side="right")

        self.info_labels = {}
        for key, txt in [("accounts", "检测到的账号"), ("detail", "账号信息"),
                         ("mid", "Machine ID"), ("did", "Dev Device ID")]:
            row = ctk.CTkFrame(si, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=f"{txt}:", width=130, anchor="w",
                         font=ctk.CTkFont(family=FONT_UI, size=13),
                         text_color=FG_DIM).pack(side="left")
            v = ctk.CTkLabel(row, text="-", anchor="w",
                             font=ctk.CTkFont(family=FONT_MONO, size=13),
                             text_color=FG_LINK)
            v.pack(side="left", fill="x", expand=True)
            self.info_labels[key] = v

        # ── 操作卡片 ──
        ac = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=10,
                          border_width=1, border_color=BORDER)
        ac.pack(fill="x", pady=(0, 10))
        ai = ctk.CTkFrame(ac, fg_color="transparent")
        ai.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(ai, text="操作",
                     font=ctk.CTkFont(family=FONT_UI, size=15, weight="bold"),
                     text_color=FG).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(ai, text="遇到「设备数量已达上限」无法登录？点击下方一键重置即可解决",
                     font=ctk.CTkFont(family=FONT_UI, size=12),
                     text_color=FG_DIM).pack(anchor="w", pady=(0, 10))

        # 主操作: 一键重置 (大按钮)
        self._btn_oneclick = ctk.CTkButton(
            ai, text="一键重置  —  清除账号 + 重置设备 ID",
            height=50,
            font=ctk.CTkFont(family=FONT_UI, size=16, weight="bold"),
            fg_color=BLUE, hover_color=BLUE_H,
            text_color=FG_WHITE, corner_radius=10,
            command=self._on_oneclick)
        self._btn_oneclick.pack(fill="x", pady=(0, 10))

        # 次要操作行
        sub_row = ctk.CTkFrame(ai, fg_color="transparent")
        sub_row.pack(fill="x")

        self.action_btns = [self._btn_oneclick]
        for txt, c, h, cmd in [
            ("清除所有账号", RED,   RED_H,   self._on_clear),
            ("重置设备 ID",  AMBER, AMBER_H, self._on_reset),
        ]:
            b = ctk.CTkButton(sub_row, text=txt, height=36,
                              font=ctk.CTkFont(family=FONT_UI, size=13),
                              fg_color=c, hover_color=h,
                              text_color=FG_WHITE, corner_radius=8,
                              command=cmd)
            b.pack(side="left", padx=(0, 10), expand=True, fill="x")
            self.action_btns.append(b)

        ctk.CTkLabel(ai, text="大多数情况下直接点「一键重置」即可，无需分步操作",
                     font=ctk.CTkFont(family=FONT_UI, size=12),
                     text_color=FG_DIM).pack(anchor="w", pady=(10, 0))

        # 管理员提示（仅 Windows 非管理员时显示）
        if IS_WIN and not is_admin():
            admin_row = ctk.CTkFrame(ai, fg_color=BG_INPUT, corner_radius=8)
            admin_row.pack(fill="x", pady=(10, 0))
            admin_inner = ctk.CTkFrame(admin_row, fg_color="transparent")
            admin_inner.pack(fill="x", padx=12, pady=8)
            ctk.CTkLabel(admin_inner,
                         text="如果操作时提示权限不足，可尝试以管理员身份重新启动本工具",
                         font=ctk.CTkFont(family=FONT_UI, size=11),
                         text_color=FG_DIM).pack(side="left")
            ctk.CTkButton(admin_inner, text="以管理员身份重启", width=130, height=28,
                          font=ctk.CTkFont(family=FONT_UI, size=11),
                          fg_color=GHOST, hover_color=GHOST_H,
                          text_color=FG_BODY, corner_radius=6,
                          command=self._restart_admin).pack(side="right")

        # ── 日志卡片 ──
        lc = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=10,
                          border_width=1, border_color=BORDER)
        lc.pack(fill="both", expand=True, pady=(0, 6))
        li = ctk.CTkFrame(lc, fg_color="transparent")
        li.pack(fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(li, text="操作日志",
                     font=ctk.CTkFont(family=FONT_UI, size=15, weight="bold"),
                     text_color=FG).pack(anchor="w", pady=(0, 8))

        self.log_box = ctk.CTkTextbox(
            li, font=ctk.CTkFont(family=FONT_MONO, size=12),
            fg_color=BG_INPUT, text_color=FG_BODY,
            corner_radius=8, wrap="word", state="disabled",
            border_width=1, border_color=BORDER, height=160)
        self.log_box.pack(fill="both", expand=True)
        self.log_box.tag_config("ok",   foreground=GREEN)
        self.log_box.tag_config("warn", foreground=AMBER)
        self.log_box.tag_config("err",  foreground=RED)
        self.log_box.tag_config("dim",  foreground=FG_DIM)

    # ─── 启动 ────────────────────────────────────────────────

    def _on_startup(self):
        self._log("=" * 44)
        self._log(f"  {APP_TITLE}  |  制作人: 掠蓝")
        self._log("  交流群: 676475076")
        self._log("=" * 44)
        self._log("")

        if os.path.isdir(DATA_DIR_DEFAULT):
            self.current_dir = DATA_DIR_DEFAULT
            self.dir_label.configure(text=DATA_DIR_DEFAULT, text_color=FG)
            self._log(f"  已检测到 Trae: {DATA_DIR_DEFAULT}", "ok")
            self._do_refresh()
        else:
            self._log("  未检测到 Trae 数据目录", "warn")
            self._log(f"  请点击「选择目录」手动选择 (通常位于 {DIR_HINT})", "warn")

        self._log("")
        for i, t in enumerate(GUIDE_TIPS, 1):
            self._log(f"  {i}. {t}", "dim")
        self._log("")

    # ─── 工具方法 ─────────────────────────────────────────────

    def _log(self, msg, tag=None):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        line = f"[{ts}] {msg}\n"
        self.log_box.insert("end", line, tag if tag else ())
        lc = int(self.log_box.index("end-1c").split(".")[0])
        if lc > 500:
            self.log_box.delete("1.0", f"{lc - 400}.0")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_btns(self, on):
        st = "normal" if on else "disabled"
        for b in self.action_btns:
            try:
                b.configure(state=st)
            except Exception:
                pass

    def _do_refresh(self, silent=False):
        if not self.current_dir:
            if not silent:
                self._log("请先选择数据目录", "warn")
            return
        s = get_status(self.current_dir)
        n = len(s["accounts"])
        self.info_labels["accounts"].configure(text=f"{n} 个")
        self.info_labels["detail"].configure(
            text=", ".join(s["accounts"]) if s["accounts"] else "无登录账号")
        self.info_labels["mid"].configure(text=s["machine_id"])
        self.info_labels["did"].configure(text=s["dev_device_id"])
        if not silent:
            self._log("状态已刷新", "dim")

    def _check(self):
        if not self.current_dir:
            messagebox.showwarning("提示", "请先选择数据目录")
            return False
        if is_trae_running():
            h = ("右键任务栏 Trae 图标 → 退出\n或在任务管理器中结束进程"
                 if IS_WIN else "菜单栏 Trae → Quit\n或终端 killall Trae")
            messagebox.showwarning("Trae 正在运行", f"请先关闭 Trae 再操作。\n\n{h}")
            return False
        return True

    # ─── 按钮回调 ─────────────────────────────────────────────

    def _on_browse(self):
        p = filedialog.askdirectory(title="选择 Trae 数据目录")
        if not p:
            return
        if not is_valid_trae_dir(p):
            messagebox.showwarning("目录无效",
                f"未找到 machineid 或 storage.json\n\n通常位于:\n{DIR_HINT}")
            return
        self.current_dir = p
        self.dir_label.configure(text=p, text_color=FG)
        self._log(f"手动选择: {p}")
        self._do_refresh()

    def _on_refresh(self):
        self._do_refresh()

    def _on_clear(self):
        if not self._check():
            return
        if not messagebox.askyesno("确认清除",
                "确定清除所有已登录账号？\n\n将删除 Token、Cookies 等登录信息。"):
            return
        self._set_btns(False)
        self._log("清除账号...")
        try:
            logs, cnt = clear_accounts(self.current_dir)
            for l in logs:
                self._log(l)
            self._log("清除完成" if cnt > 0 else "没有需要清除的内容",
                       "ok" if cnt > 0 else "warn")
            self._do_refresh(silent=True)
        except PermissionError:
            self._log("权限不足", "err")
        except Exception as e:
            self._log(f"错误: {e}", "err")
        finally:
            self._set_btns(True)

    def _on_reset(self):
        if not self._check():
            return
        if not messagebox.askyesno("确认重置",
                "确定重置设备 ID？\n\n将生成全新的设备标识。"):
            return
        self._set_btns(False)
        self._log("重置设备 ID...")
        try:
            logs = reset_device_id(self.current_dir)
            for l in logs:
                self._log(l)
            # 验证写入
            mid = read_machineid(self.current_dir)
            ok, msg = verify_write(self.current_dir, mid)
            if ok:
                self._log(f"写入验证通过", "ok")
            else:
                self._log(f"写入验证失败: {msg}", "err")
            self._do_refresh(silent=True)
        except PermissionError:
            self._log("权限不足", "err")
        except Exception as e:
            self._log(f"错误: {e}", "err")
        finally:
            self._set_btns(True)

    def _on_oneclick(self):
        if not self._check():
            return
        if not messagebox.askyesno("确认一键重置",
                "将执行:\n  1. 清除所有已登录账号\n  2. 重置设备 ID\n\n"
                "适用于「设备数量已达上限」，确定继续？"):
            return
        self._set_btns(False)
        self._log("━" * 36)
        self._log("  一键重置开始")
        self._log("━" * 36)
        try:
            self._log("[1/2] 清除账号...")
            logs, _ = clear_accounts(self.current_dir)
            for l in logs:
                self._log(l)
            self._log("[2/2] 重置设备 ID...")
            logs = reset_device_id(self.current_dir)
            for l in logs:
                self._log(l)
            # 验证
            mid = read_machineid(self.current_dir)
            ok, msg = verify_write(self.current_dir, mid)
            self._log("━" * 36)
            if ok:
                self._log("  一键重置完成，文件验证通过", "ok")
                self._log("  现在可以打开 Trae 登录新账号了", "ok")
            else:
                self._log(f"  重置完成但验证异常: {msg}", "warn")
            self._log("━" * 36)
            self._do_refresh(silent=True)
        except PermissionError:
            self._log("权限不足，请以管理员身份运行", "err")
        except Exception as e:
            self._log(f"错误: {e}", "err")
        finally:
            self._set_btns(True)

    def _on_restore(self):
        if not self.current_dir:
            messagebox.showwarning("提示", "请先选择数据目录")
            return
        if is_trae_running():
            messagebox.showwarning("Trae 正在运行", "请先关闭 Trae。")
            return
        if not messagebox.askyesno("确认恢复",
                "从 .bak 备份恢复到操作前的状态？\n仅能恢复最近一次。"):
            return
        self._set_btns(False)
        self._log("恢复备份...")
        try:
            logs, cnt = restore_backup(self.current_dir)
            for l in logs:
                self._log(l)
            self._log("恢复完成" if cnt > 0 else "没有可恢复的备份",
                       "ok" if cnt > 0 else "warn")
            self._do_refresh(silent=True)
        except Exception as e:
            self._log(f"恢复失败: {e}", "err")
        finally:
            self._set_btns(True)

    def _restart_admin(self):
        if restart_as_admin():
            self.destroy()
            sys.exit(0)
        else:
            messagebox.showerror("失败", "无法以管理员身份重启")

    def _on_about(self):
        messagebox.showinfo("关于",
            f"TraeReset v{VERSION}\n"
            "Trae IDE 设备限制重置工具\n\n"
            "制作人: 掠蓝\n"
            "交流群: 676475076\n\n"
            "仅供个人学习与技术研究使用。\n"
            "https://github.com/Ylsssq926/TraeReset")


if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception:
        err = traceback.format_exc()
        try:
            messagebox.showerror("启动失败", f"程序异常:\n{err}")
        except Exception:
            pass
        sys.exit(1)
