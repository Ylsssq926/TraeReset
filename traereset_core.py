#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TraeReset core logic."""

from __future__ import annotations

import ctypes
import json
import os
import platform
import secrets
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

APP_NAME = "TraeReset"
VERSION = "1.1.1"
APP_TITLE = f"{APP_NAME} v{VERSION}"
DISCLAIMER_VERSION = "1.1.1-full-upgrade"
BRAND_NAME = "掠蓝"
PROJECT_GITHUB_URL = "https://github.com/Ylsssq926/TraeReset"
ANTI_RESALE_NOTICE = "本项目为掠蓝开源作品，请勿二次售卖。"
REFUND_NOTICE = "如果你是付费购买获得本工具，请立即退款。"
SOURCE_NOTICE = f"开源作者：{BRAND_NAME}"
PERSISTENT_NOTICE_TEXT = (
    f"{SOURCE_NOTICE}\n"
    f"项目地址：{PROJECT_GITHUB_URL}\n"
    f"{ANTI_RESALE_NOTICE} {REFUND_NOTICE}"
)

IS_WIN = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"

if IS_WIN:
    DATA_DIR_DEFAULT = Path(os.environ.get("APPDATA", "")) / "Trae"
    DIR_HINT = "%APPDATA%\\Trae"
    FONT_UI = "Microsoft YaHei UI"
    FONT_MONO = "Consolas"
elif IS_MAC:
    DATA_DIR_DEFAULT = Path.home() / "Library" / "Application Support" / "Trae"
    DIR_HINT = "~/Library/Application Support/Trae"
    FONT_UI = "PingFang SC"
    FONT_MONO = "Menlo"
else:
    DATA_DIR_DEFAULT = Path.home() / ".config" / "Trae"
    DIR_HINT = "~/.config/Trae"
    FONT_UI = "Noto Sans CJK SC"
    FONT_MONO = "Noto Sans Mono"

STORAGE_REL = Path("User") / "globalStorage" / "storage.json"
STATE_DB_REL = Path("User") / "globalStorage" / "state.vscdb"
STATE_DB_BACKUP_REL = Path("User") / "globalStorage" / "state.vscdb.backup"
LOCAL_STATE_REL = Path("Local State")
MACHINE_ID_REL = Path("machineid")

AUTH_KEY_PATTERNS = [
    "iCubeAuthInfo://",
    "iCubeServerData://",
    "iCubeEntitlementInfo://",
    "-entitlement-notified",
    "icube.cloudide",
]

COOKIE_PATHS = [
    Path("Network") / "Cookies",
    Path("Network") / "Cookies-journal",
    Path("Partitions") / "icube-web-crawler-shared-session-v1.0" / "Network" / "Cookies",
    Path("Partitions") / "icube-web-crawler-shared-session-v1.0" / "Network" / "Cookies-journal",
    Path("Partitions") / "trae-webview" / "Network" / "Cookies",
    Path("Partitions") / "trae-webview" / "Network" / "Cookies-journal",
]

RESET_PATHS = [
    STATE_DB_REL,
    STATE_DB_BACKUP_REL,
    LOCAL_STATE_REL,
    Path("IndexedDB"),
    Path("Local Storage"),
    Path("Session Storage"),
    Path("Code Cache"),
    Path("GPUCache"),
    Path("DawnCache"),
    Path("Network") / "TransportSecurity",
]

GUIDE_TIPS = [
    "操作前先完全退出 Trae，包括托盘或后台残留进程。",
    "一键深度重置会同时清理账号状态、缓存目录和设备标识。",
    "所有修改前都会自动生成 .bak 备份，便于恢复最近一次状态。",
    "如果默认目录未检测到，可使用“选择目录”手动定位 Trae 数据目录。",
    "本项目为掠蓝开源作品，如系购买获得请立即退款。",
]

DISCLAIMER_TEXT = (
    "1. 本工具仅用于个人学习与技术研究。\n\n"
    "2. 所有操作会优先备份现有文件或目录，恢复功能仅覆盖最近一次备份。\n\n"
    "3. 一键深度重置会清理本地账号状态、缓存目录和设备标识，适合旧版方案失效时使用。\n\n"
    "4. 本工具不修改 Trae 程序本体，仅处理本地用户数据。\n\n"
    f"5. 开源作者：{BRAND_NAME}\n项目地址：{PROJECT_GITHUB_URL}\n\n"
    f"6. {ANTI_RESALE_NOTICE}\n{REFUND_NOTICE}"
)


def configure_platform():
    if IS_WIN:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass


def get_runtime_base_dir():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def discover_logo_path(base_dir=None):
    root = Path(base_dir) if base_dir else get_runtime_base_dir()
    image_patterns = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.ico")

    def collect_files(folder):
        items = []
        if not folder.exists() or not folder.is_dir():
            return items
        for pattern in image_patterns:
            items.extend(sorted(folder.glob(pattern)))
        return items

    candidate_groups = [
        collect_files(root / "logo"),
        collect_files(root),
    ]

    for files in candidate_groups:
        if not files:
            continue
        preferred = [
            path for path in files
            if any(keyword in path.name.lower() for keyword in ("logo", "icon", "brand"))
        ]
        if preferred:
            return preferred[0]
        return files[0]
    return None


def as_path(value):
    return Path(value).expanduser()


def _get_config_path():
    if IS_WIN:
        base = Path(os.environ.get("APPDATA", os.path.expanduser("~"))) / "TraeUnlock"
    elif IS_MAC:
        base = Path.home() / "Library" / "Application Support" / "TraeUnlock"
    else:
        base = Path.home() / ".config" / "TraeUnlock"
    base.mkdir(parents=True, exist_ok=True)
    return base / "config.json"


def load_config():
    try:
        with _get_config_path().open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def save_config(config):
    try:
        with _get_config_path().open("w", encoding="utf-8") as file:
            json.dump(config, file, ensure_ascii=False, indent=2)
    except Exception:
        pass


def has_accepted_disclaimer():
    config = load_config()
    return bool(config.get("disclaimer_accepted", False)) and config.get("disclaimer_version") == DISCLAIMER_VERSION


def save_disclaimer_accepted():
    config = load_config()
    config["disclaimer_accepted"] = True
    config["disclaimer_version"] = DISCLAIMER_VERSION
    save_config(config)


def is_admin():
    if IS_WIN:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    return os.geteuid() == 0 if hasattr(os, "geteuid") else True


def restart_as_admin():
    if not IS_WIN:
        return False
    try:
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        return True
    except Exception:
        return False


def data_path(data_dir, relative):
    return as_path(data_dir) / relative


def ensure_parent(path):
    path.parent.mkdir(parents=True, exist_ok=True)


def backup_target(path):
    return Path(f"{path}.bak")


def backup_item(path):
    if not path.exists():
        return None
    backup = backup_target(path)
    if backup.exists():
        if backup.is_dir() and not backup.is_symlink():
            shutil.rmtree(backup)
        else:
            backup.unlink()
    if path.is_dir() and not path.is_symlink():
        shutil.copytree(path, backup)
    else:
        ensure_parent(backup)
        shutil.copy2(path, backup)
    return backup


def remove_path(path):
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def read_json_file(path):
    if not path.is_file():
        return None
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return None


def write_json_file(path, data):
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def read_machineid(data_dir):
    path = data_path(data_dir, MACHINE_ID_REL)
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return None


def write_machineid(data_dir, value):
    path = data_path(data_dir, MACHINE_ID_REL)
    ensure_parent(path)
    backup_item(path)
    path.write_text(value, encoding="utf-8")


def read_storage(data_dir):
    return read_json_file(data_path(data_dir, STORAGE_REL))


def write_storage(data_dir, data):
    path = data_path(data_dir, STORAGE_REL)
    backup_item(path)
    write_json_file(path, data)


def read_local_state(data_dir):
    return read_json_file(data_path(data_dir, LOCAL_STATE_REL))


def write_local_state(data_dir, data):
    path = data_path(data_dir, LOCAL_STATE_REL)
    backup_item(path)
    write_json_file(path, data)


def is_valid_trae_dir(path):
    base = as_path(path)
    return any(
        candidate.exists()
        for candidate in [
            base / MACHINE_ID_REL,
            base / STORAGE_REL,
            base / STATE_DB_REL,
            base / LOCAL_STATE_REL,
        ]
    )


def is_trae_running():
    try:
        if IS_WIN:
            output = subprocess.check_output(
                ["tasklist"],
                creationflags=0x08000000,
                text=True,
                timeout=10,
            )
            return "trae.exe" in output.lower()
        output = subprocess.check_output(["ps", "aux"], text=True, timeout=10)
        lowered = output.lower()
        return "/trae" in lowered or " trae" in lowered
    except Exception:
        return False


def generate_device_ids():
    return {
        "machineid": str(uuid.uuid4()),
        "telemetry.machineId": secrets.token_hex(32),
        "telemetry.devDeviceId": str(uuid.uuid4()),
        "telemetry.sqmId": "{" + str(uuid.uuid4()).upper() + "}",
    }


def collect_storage_keys(storage):
    if not storage:
        return []
    return [key for key in storage.keys() if any(pattern in key for pattern in AUTH_KEY_PATTERNS)]


def extract_accounts(storage):
    accounts = []
    if not storage:
        return accounts
    for key, value in storage.items():
        if not key.startswith("iCubeAuthInfo://icube.cloudide"):
            continue
        try:
            auth = json.loads(value) if isinstance(value, str) else value
            account = auth.get("account", {})
            name = account.get("username", "未知")
            contact = account.get("email", "") or account.get("nonPlainTextMobile", "")
            accounts.append(f"{name} ({contact})" if contact else name)
        except Exception:
            accounts.append("(解析失败)")
    return accounts


def get_status(data_dir):
    base = as_path(data_dir)
    storage = read_storage(base)
    local_state = read_local_state(base)
    accounts = extract_accounts(storage)
    storage_keys = collect_storage_keys(storage)
    session_targets = COOKIE_PATHS + RESET_PATHS
    existing_session_paths = [str(rel) for rel in session_targets if (base / rel).exists()]
    telemetry = storage or {}

    return {
        "machine_id": read_machineid(base) or "未找到",
        "telemetry_machine_id": telemetry.get("telemetry.machineId", "未找到"),
        "dev_device_id": telemetry.get("telemetry.devDeviceId", "未找到"),
        "sqm_id": telemetry.get("telemetry.sqmId", "未找到"),
        "accounts": accounts,
        "storage_key_count": len(storage_keys),
        "session_path_count": len(existing_session_paths),
        "session_paths": existing_session_paths,
        "has_state_db": (base / STATE_DB_REL).exists(),
        "has_local_state": isinstance(local_state, dict),
        "risk_summary": "检测到多处本地账号与会话状态" if storage_keys or existing_session_paths else "未发现明显账号缓存",
    }


def clear_accounts(data_dir):
    base = as_path(data_dir)
    logs = []
    removed = 0
    storage = read_storage(base)

    if storage is None:
        logs.append("  未找到 storage.json")
    else:
        keys = collect_storage_keys(storage)
        if keys:
            backup_item(base / STORAGE_REL)
            for key in keys:
                storage.pop(key, None)
                logs.append(f"  删除存储键: {key}")
                removed += 1
            write_json_file(base / STORAGE_REL, storage)
        else:
            logs.append("  storage.json 中未发现账号或权益键")

    for relative in COOKIE_PATHS:
        target = base / relative
        if not target.exists():
            continue
        backup_item(target)
        remove_path(target)
        logs.append(f"  清除会话文件: {relative}")
        removed += 1

    if removed == 0:
        logs.append("  没有需要清除的账号内容")
    return logs, removed


def deep_clean_local_state(data_dir):
    base = as_path(data_dir)
    logs = []
    removed = 0

    for relative in RESET_PATHS:
        target = base / relative
        if not target.exists():
            continue
        backup_item(target)
        remove_path(target)
        kind = "目录" if target.is_dir() else "文件"
        logs.append(f"  清理{kind}: {relative}")
        removed += 1

    return logs, removed


def patch_local_state_ids(local_state, ids):
    if not isinstance(local_state, dict):
        return local_state, False

    changed = False
    for key in [
        "telemetry.machineId",
        "telemetry.devDeviceId",
        "telemetry.sqmId",
        "machineId",
        "devDeviceId",
        "sqmId",
    ]:
        if key in local_state:
            if key.endswith("machineId") and key != "telemetry.devDeviceId":
                local_state[key] = ids["telemetry.machineId"]
            elif key.endswith("devDeviceId"):
                local_state[key] = ids["telemetry.devDeviceId"]
            elif key.endswith("sqmId"):
                local_state[key] = ids["telemetry.sqmId"]
            changed = True

    storage = local_state.get("storage")
    if isinstance(storage, dict):
        mapping = {
            "telemetry.machineId": ids["telemetry.machineId"],
            "telemetry.devDeviceId": ids["telemetry.devDeviceId"],
            "telemetry.sqmId": ids["telemetry.sqmId"],
            "machineid": ids["machineid"],
        }
        for key, value in mapping.items():
            if key in storage:
                storage[key] = value
                changed = True

    return local_state, changed


def reset_device_id(data_dir):
    base = as_path(data_dir)
    logs = []
    ids = generate_device_ids()

    write_machineid(base, ids["machineid"])
    logs.append(f"  Machine ID: {ids['machineid']}")

    storage = read_storage(base)
    if storage is None:
        storage = {}
    storage["telemetry.machineId"] = ids["telemetry.machineId"]
    storage["telemetry.devDeviceId"] = ids["telemetry.devDeviceId"]
    storage["telemetry.sqmId"] = ids["telemetry.sqmId"]
    storage["has_device_id_updated_to_aha"] = "false"
    write_storage(base, storage)
    logs.append(f"  telemetry.machineId: {ids['telemetry.machineId'][:24]}...")
    logs.append(f"  telemetry.devDeviceId: {ids['telemetry.devDeviceId']}")

    local_state = read_local_state(base)
    local_state, changed = patch_local_state_ids(local_state, ids)
    if changed:
        write_local_state(base, local_state)
        logs.append("  Local State 中的设备相关字段已同步更新")
    elif local_state is not None:
        logs.append("  Local State 已存在，但未找到可替换的设备字段")
    else:
        logs.append("  未找到 Local State")

    return logs, ids


def verify_write(data_dir, expected_ids):
    base = as_path(data_dir)
    details = []
    ok = True

    actual_machineid = read_machineid(base)
    if actual_machineid != expected_ids["machineid"]:
        ok = False
        details.append("machineid 与本次生成值不一致")
    else:
        details.append("machineid 已更新")

    storage = read_storage(base)
    if not storage:
        ok = False
        details.append("storage.json 缺失或无法读取")
    else:
        checks = {
            "telemetry.machineId": expected_ids["telemetry.machineId"],
            "telemetry.devDeviceId": expected_ids["telemetry.devDeviceId"],
            "telemetry.sqmId": expected_ids["telemetry.sqmId"],
        }
        for key, expected in checks.items():
            if storage.get(key) != expected:
                ok = False
                details.append(f"{key} 未写入预期值")
            else:
                details.append(f"{key} 已更新")

        residual = collect_storage_keys(storage)
        if residual:
            ok = False
            details.append(f"storage.json 仍残留 {len(residual)} 个账号或权益键")

    uncleared = []
    for relative in COOKIE_PATHS + RESET_PATHS:
        if (base / relative).exists():
            uncleared.append(str(relative))
    if uncleared:
        ok = False
        details.append(f"仍存在 {len(uncleared)} 个本地缓存目标")
    else:
        details.append("会话缓存目标已清理")

    return {
        "ok": ok,
        "summary": "验证通过" if ok else "验证发现未完成项",
        "details": details,
    }


def restore_backup(data_dir):
    base = as_path(data_dir)
    logs = []
    restored = 0

    targets = [MACHINE_ID_REL, STORAGE_REL, LOCAL_STATE_REL, STATE_DB_REL, STATE_DB_BACKUP_REL]
    targets.extend(COOKIE_PATHS)
    targets.extend(RESET_PATHS)

    seen = set()
    for relative in targets:
        key = str(relative)
        if key in seen:
            continue
        seen.add(key)
        dst = base / relative
        bak = backup_target(dst)
        if not bak.exists():
            continue
        if dst.exists():
            remove_path(dst)
        if bak.is_dir() and not bak.is_symlink():
            shutil.copytree(bak, dst)
        else:
            ensure_parent(dst)
            shutil.copy2(bak, dst)
        logs.append(f"  已恢复: {relative}")
        restored += 1

    if restored == 0:
        logs.append("  没有找到任何可恢复的备份")
    return logs, restored
