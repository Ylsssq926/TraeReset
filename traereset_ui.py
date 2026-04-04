#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TraeReset UI layer."""

from __future__ import annotations

import sys
from datetime import datetime

import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox

from traereset_core import (
    ANTI_RESALE_NOTICE,
    APP_TITLE,
    BRAND_NAME,
    DATA_DIR_DEFAULT,
    DIR_HINT,
    DISCLAIMER_TEXT,
    discover_logo_path,
    FONT_MONO,
    FONT_UI,
    GUIDE_TIPS,
    IS_WIN,
    PERSISTENT_NOTICE_TEXT,
    PROJECT_GITHUB_URL,
    REFUND_NOTICE,
    SOURCE_NOTICE,
    clear_accounts,
    deep_clean_local_state,
    get_status,
    has_accepted_disclaimer,
    is_admin,
    is_trae_running,
    is_valid_trae_dir,
    reset_device_id,
    restart_as_admin,
    restore_backup,
    save_disclaimer_accepted,
    verify_write,
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG_APP = "#eef8f6"
BG_SURFACE = "#ffffff"
BG_SOFT = "#f4fcfa"
BG_TINT = "#e4f3f3"
BG_HERO = "#dff4f4"
BG_LOG = "#f7fbfb"
FG_PRIMARY = "#12313b"
FG_SECONDARY = "#4a6b73"
FG_MUTED = "#7e9ba3"
FG_LIGHT = "#ffffff"
ACCENT = "#2f7de1"
ACCENT_HOVER = "#2368bf"
ACCENT_ALT = "#53b59f"
ACCENT_ALT_HOVER = "#429d89"
SUCCESS = "#2f9b72"
WARN = "#d29a36"
WARN_HOVER = "#ba8626"
DANGER = "#d96363"
DANGER_HOVER = "#c24c4c"
BORDER = "#cfe8e4"
GHOST = "#edf6f7"
GHOST_HOVER = "#dceff1"
INFO = "#5aa9e6"
LOG_OK = "#2f9b72"
LOG_WARN = "#cf8a22"
LOG_ERR = "#d45a5a"
LOG_DIM = "#78949b"

WINDOW_WIDTH = 1260
WINDOW_HEIGHT = 900
MIN_WIDTH = 1080
MIN_HEIGHT = 780


def ui_font(size, weight="normal"):
    return ctk.CTkFont(family=FONT_UI, size=size, weight=weight)


def mono_font(size, weight="normal"):
    return ctk.CTkFont(family=FONT_MONO, size=size, weight=weight)


def load_logo_image(logo_path, size):
    if not logo_path or not logo_path.exists():
        return None
    try:
        return ctk.CTkImage(light_image=Image.open(logo_path), size=size)
    except Exception:
        return None


class DisclaimerDialog(ctk.CTkToplevel):
    def __init__(self, master, logo_image=None):
        super().__init__(master, fg_color=BG_APP)
        self.logo_image = logo_image
        self.title("免责声明")
        self.resizable(False, False)
        self.geometry("760x620")
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self._build()
        self.update_idletasks()
        x = master.winfo_rootx() + max(0, (master.winfo_width() - 760) // 2)
        y = master.winfo_rooty() + max(0, (master.winfo_height() - 620) // 2)
        self.geometry(f"760x620+{x}+{y}")

    def _build(self):
        shell = ctk.CTkFrame(self, fg_color=BG_APP)
        shell.pack(fill="both", expand=True, padx=18, pady=18)

        card = ctk.CTkFrame(shell, fg_color=BG_SURFACE, corner_radius=26, border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True)

        hero = ctk.CTkFrame(card, fg_color=BG_HERO, corner_radius=24)
        hero.pack(fill="x", padx=20, pady=20)
        icon = ctk.CTkFrame(hero, fg_color=ACCENT, corner_radius=18, width=74, height=74)
        icon.pack(pady=(24, 12))
        icon.pack_propagate(False)
        if self.logo_image:
            ctk.CTkLabel(icon, text="", image=self.logo_image).place(relx=0.5, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(icon, text="T", text_color=FG_LIGHT, font=ui_font(34, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(hero, text="TraeReset", text_color=FG_PRIMARY, font=ui_font(28, "bold")).pack()
        ctk.CTkLabel(
            hero,
            text="清理账号状态、缓存目录与设备标识之前，请确认你理解本工具边界。",
            text_color=FG_SECONDARY,
            font=ui_font(13),
        ).pack(pady=(6, 24))

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=26, pady=(0, 24))
        ctk.CTkLabel(body, text="免责声明", text_color=FG_PRIMARY, font=ui_font(18, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            body,
            text="程序本体不会被修改，所有操作仅限本地用户数据目录。",
            text_color=FG_SECONDARY,
            font=ui_font(13),
            wraplength=660,
            justify="left",
        ).pack(anchor="w", pady=(6, 12))

        text = ctk.CTkTextbox(
            body,
            height=220,
            fg_color=BG_SOFT,
            text_color=FG_SECONDARY,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            font=ui_font(13),
            wrap="word",
        )
        text.insert("1.0", DISCLAIMER_TEXT)
        text.configure(state="disabled")
        text.pack(fill="both", expand=True)

        source_card = ctk.CTkFrame(body, fg_color=BG_HERO, corner_radius=18, border_width=1, border_color=BORDER)
        source_card.pack(fill="x", pady=(14, 0))
        ctk.CTkLabel(
            source_card,
            text="开源来源与反转售提示",
            text_color=FG_PRIMARY,
            font=ui_font(14, "bold"),
        ).pack(anchor="w", padx=14, pady=(12, 4))
        ctk.CTkLabel(
            source_card,
            text=PERSISTENT_NOTICE_TEXT,
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=640,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 12))

        ctk.CTkButton(
            body,
            text="关闭",
            width=140,
            height=44,
            fg_color=GHOST,
            hover_color=GHOST_HOVER,
            text_color=FG_PRIMARY,
            corner_radius=16,
            font=ui_font(14),
            command=self.destroy,
        ).pack(anchor="e", pady=(18, 0))


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_APP)
        self.withdraw()
        self.title(APP_TITLE)
        self.current_dir = None
        self.summary_var = ctk.StringVar(value="尚未执行操作")
        self.status_badge_var = ctk.StringVar(value="等待检测")
        self.health_var = ctk.StringVar(value="请选择目录并刷新状态")
        self.runtime_var = ctk.StringVar(value="正在检测 Trae 运行状态")
        self.action_btns = []
        self.hero_stats = {}
        self.info_values = {}
        self._startup_locked = False
        self.logo_path = discover_logo_path()
        self.logo_image_small = load_logo_image(self.logo_path, (40, 40))
        self.logo_image_large = load_logo_image(self.logo_path, (48, 48))

        self.geometry(self._center_geometry(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.minsize(MIN_WIDTH, MIN_HEIGHT)

        self._build_main()
        self.after(10, self._finish_startup)

    def _center_geometry(self, width, height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = max(0, (screen_w - width) // 2)
        pos_y = max(0, (screen_h - height) // 2)
        return f"{width}x{height}+{pos_x}+{pos_y}"

    def _finish_startup(self):
        self._log("=" * 60, "dim")
        self._log(f"{SOURCE_NOTICE} | {PROJECT_GITHUB_URL}", "info")
        self._log(ANTI_RESALE_NOTICE, "warn")
        self._log(REFUND_NOTICE, "warn")
        self._log("=" * 60, "dim")

        if DATA_DIR_DEFAULT.is_dir():
            self.current_dir = DATA_DIR_DEFAULT
            self._set_textbox_value(self.dir_text, str(DATA_DIR_DEFAULT))
            self._log(f"检测到默认目录: {DATA_DIR_DEFAULT}", "ok")
            self._set_summary("已加载默认目录")
        else:
            self._set_status_badge("未找到默认目录", DANGER)
            self.runtime_var.set("未检测到默认 Trae 目录，请手动选择。")
            self._set_summary("未检测到默认目录，请手动选择")
            self._log(f"未检测到默认 Trae 数据目录，通常位于 {DIR_HINT}", "warn")

        self.deiconify()
        self.lift()
        self.focus_force()

        self.after(30, self._refresh_runtime_state)
        if self.current_dir:
            self.after(80, lambda: self._do_refresh(silent=True))

        if not has_accepted_disclaimer():
            self.after(120, self._show_startup_gate)

    def _build_main(self):
        self.root_frame = ctk.CTkFrame(self, fg_color=BG_APP)
        self.root_frame.pack(fill="both", expand=True, padx=18, pady=18)

        self._build_topbar(self.root_frame)
        content = ctk.CTkFrame(self.root_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, pady=(14, 0))
        content.grid_columnconfigure(0, weight=5)
        content.grid_columnconfigure(1, weight=4)
        content.grid_rowconfigure(1, weight=1)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self._build_hero(left)
        self._build_environment_card(left)
        self._build_status_card(left)
        self._build_log_card(left)
        self._build_action_card(right)
        self._build_health_card(right)
        self._build_startup_gate()

    def _build_topbar(self, parent):
        bar = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        bar.pack(fill="x")
        inner = ctk.CTkFrame(bar, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        title_row = ctk.CTkFrame(left, fg_color="transparent")
        title_row.pack(anchor="w")
        if self.logo_image_small:
            ctk.CTkLabel(title_row, text="", image=self.logo_image_small).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(title_row, text="TraeReset", text_color=FG_PRIMARY, font=ui_font(26, "bold")).pack(side="left")
        ctk.CTkLabel(left, textvariable=self.runtime_var, text_color=FG_SECONDARY, font=ui_font(12)).pack(anchor="w", pady=(4, 0))

        right = ctk.CTkFrame(inner, fg_color="transparent")
        right.pack(side="right")
        self.status_badge = ctk.CTkLabel(
            right,
            textvariable=self.status_badge_var,
            text_color=FG_LIGHT,
            fg_color=ACCENT_ALT,
            corner_radius=999,
            width=164,
            height=36,
            font=ui_font(12, "bold"),
        )
        self.status_badge.pack(anchor="e")

        buttons = ctk.CTkFrame(right, fg_color="transparent")
        buttons.pack(anchor="e", pady=(10, 0))
        ctk.CTkButton(
            buttons,
            text="免责声明",
            width=100,
            height=36,
            fg_color=GHOST,
            hover_color=GHOST_HOVER,
            text_color=FG_PRIMARY,
            corner_radius=14,
            font=ui_font(12),
            command=self._show_disclaimer,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            buttons,
            text="关于",
            width=78,
            height=36,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=FG_LIGHT,
            corner_radius=14,
            font=ui_font(12, "bold"),
            command=self._on_about,
        ).pack(side="left")

    def _build_hero(self, parent):
        hero = ctk.CTkFrame(parent, fg_color=BG_HERO, corner_radius=28, border_width=1, border_color=BORDER)
        hero.pack(fill="x")
        inner = ctk.CTkFrame(hero, fg_color="transparent")
        inner.pack(fill="x", padx=22, pady=22)

        hero_title = ctk.CTkFrame(inner, fg_color="transparent")
        hero_title.pack(anchor="w")
        if self.logo_image_large:
            ctk.CTkLabel(hero_title, text="", image=self.logo_image_large).pack(side="left", padx=(0, 12))
        ctk.CTkLabel(hero_title, text="更干净、更稳定的本地状态重置", text_color=FG_PRIMARY, font=ui_font(28, "bold")).pack(side="left")
        ctk.CTkLabel(
            inner,
            text="用于清理 Trae 本地账号状态、缓存目录与设备标识，并保持更清晰的操作流程。",
            text_color=FG_SECONDARY,
            font=ui_font(13),
            wraplength=700,
            justify="left",
        ).pack(anchor="w", pady=(8, 14))

        source_card = ctk.CTkFrame(inner, fg_color=BG_SURFACE, corner_radius=18, border_width=1, border_color=BORDER)
        source_card.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(
            source_card,
            text="开源来源与反转售提示",
            text_color=ACCENT,
            font=ui_font(13, "bold"),
        ).pack(anchor="w", padx=16, pady=(12, 4))
        ctk.CTkLabel(
            source_card,
            text=PERSISTENT_NOTICE_TEXT,
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=680,
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 12))

        stats = ctk.CTkFrame(inner, fg_color="transparent")
        stats.pack(fill="x")
        stats.grid_columnconfigure((0, 1, 2), weight=1)

        cards = [
            ("accounts", "账号条目"),
            ("session", "缓存目标"),
            ("storage", "存储键"),
        ]
        for index, (key, title) in enumerate(cards):
            card = ctk.CTkFrame(stats, fg_color=BG_SURFACE, corner_radius=20, border_width=1, border_color=BORDER)
            card.grid(row=0, column=index, sticky="ew", padx=(0, 10) if index < 2 else (0, 0))
            ctk.CTkLabel(card, text=title, text_color=FG_MUTED, font=ui_font(11, "bold")).pack(anchor="w", padx=16, pady=(12, 4))
            value = ctk.CTkLabel(card, text="-", text_color=FG_PRIMARY, font=ui_font(26, "bold"))
            value.pack(anchor="w", padx=16, pady=(0, 12))
            self.hero_stats[key] = value

    def _build_environment_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        card.pack(fill="x", pady=(14, 12))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)

        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="环境与目录", text_color=FG_PRIMARY, font=ui_font(18, "bold")).pack(side="left")
        ctk.CTkButton(
            header,
            text="刷新状态",
            width=92,
            height=34,
            fg_color=GHOST,
            hover_color=GHOST_HOVER,
            text_color=FG_PRIMARY,
            corner_radius=14,
            font=ui_font(12),
            command=self._on_refresh,
        ).pack(side="right")

        ctk.CTkLabel(
            inner,
            text="路径、备份和恢复都会基于当前目录执行。目录内容会显示在下方只读文本区域。",
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=720,
            justify="left",
        ).pack(anchor="w", pady=(8, 12))

        self.dir_text = ctk.CTkTextbox(
            inner,
            height=64,
            fg_color=BG_SOFT,
            text_color=FG_PRIMARY,
            corner_radius=16,
            border_width=1,
            border_color=BORDER,
            font=mono_font(12),
            wrap="word",
        )
        self.dir_text.insert("1.0", "未选择目录")
        self.dir_text.configure(state="disabled")
        self.dir_text.pack(fill="x")

        controls = ctk.CTkFrame(inner, fg_color="transparent")
        controls.pack(fill="x", pady=(14, 0))
        ctk.CTkButton(
            controls,
            text="选择目录",
            width=120,
            height=40,
            fg_color=ACCENT_ALT,
            hover_color=ACCENT_ALT_HOVER,
            text_color=FG_LIGHT,
            corner_radius=16,
            font=ui_font(13, "bold"),
            command=self._on_browse,
        ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            controls,
            text="恢复备份",
            width=120,
            height=40,
            fg_color=GHOST,
            hover_color=GHOST_HOVER,
            text_color=FG_PRIMARY,
            corner_radius=16,
            font=ui_font(13),
            command=self._on_restore,
        ).pack(side="left")

    def _build_status_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        card.pack(fill="x", pady=(0, 12))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)

        ctk.CTkLabel(inner, text="当前状态", text_color=FG_PRIMARY, font=ui_font(18, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            inner,
            text="这里展示当前账号残留、设备 ID 和缓存覆盖范围。",
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=720,
            justify="left",
        ).pack(anchor="w", pady=(6, 12))

        fields = [
            ("accounts", "检测到账号"),
            ("detail", "账号详情"),
            ("mid", "Machine ID"),
            ("tmid", "Telemetry Machine ID"),
            ("did", "Dev Device ID"),
            ("sqm", "SQM ID"),
            ("cache", "缓存目标"),
            ("risk", "风险摘要"),
        ]
        for key, label in fields:
            row = ctk.CTkFrame(inner, fg_color=BG_SOFT, corner_radius=16, border_width=1, border_color=BORDER)
            row.pack(fill="x", pady=5)
            row.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(row, text=label, width=150, anchor="w", text_color=FG_MUTED, font=ui_font(12, "bold")).grid(row=0, column=0, sticky="nw", padx=14, pady=12)
            if key in {"mid", "tmid", "did", "sqm", "detail", "risk"}:
                widget = ctk.CTkTextbox(
                    row,
                    height=54 if key in {"mid", "tmid", "did", "sqm"} else 64,
                    fg_color=BG_SURFACE,
                    text_color=FG_PRIMARY,
                    corner_radius=12,
                    border_width=0,
                    font=mono_font(12) if key in {"mid", "tmid", "did", "sqm"} else ui_font(12),
                    wrap="word",
                )
                widget.insert("1.0", "-")
                widget.configure(state="disabled")
                widget.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=8)
            else:
                widget = ctk.CTkLabel(
                    row,
                    text="-",
                    anchor="w",
                    justify="left",
                    wraplength=520,
                    text_color=FG_PRIMARY,
                    font=ui_font(12),
                )
                widget.grid(row=0, column=1, sticky="ew", padx=(0, 14), pady=12)
            self.info_values[key] = widget

    def _build_log_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(inner, text="执行日志", text_color=FG_PRIMARY, font=ui_font(18, "bold")).pack(anchor="w")
        ctk.CTkLabel(inner, textvariable=self.summary_var, text_color=FG_SECONDARY, font=ui_font(12)).pack(anchor="w", pady=(6, 10))

        self.log_box = ctk.CTkTextbox(
            inner,
            fg_color=BG_LOG,
            text_color=FG_PRIMARY,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            wrap="word",
            state="disabled",
            font=mono_font(12),
        )
        self.log_box.pack(fill="both", expand=True)
        self.log_box.tag_config("ok", foreground=LOG_OK)
        self.log_box.tag_config("warn", foreground=LOG_WARN)
        self.log_box.tag_config("err", foreground=LOG_ERR)
        self.log_box.tag_config("dim", foreground=LOG_DIM)
        self.log_box.tag_config("info", foreground=ACCENT)

    def _build_action_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        card.pack(fill="x")
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)

        ctk.CTkLabel(inner, text="操作面板", text_color=FG_PRIMARY, font=ui_font(18, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            inner,
            text="推荐优先使用一键深度重置。单项按钮适合单独执行局部步骤。",
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=420,
            justify="left",
        ).pack(anchor="w", pady=(6, 14))

        self.primary_button = ctk.CTkButton(
            inner,
            text="一键深度重置",
            height=56,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=FG_LIGHT,
            corner_radius=18,
            font=ui_font(16, "bold"),
            command=self._on_oneclick,
        )
        self.primary_button.pack(fill="x")
        self.action_btns.append(self.primary_button)

        ctk.CTkLabel(
            inner,
            text="执行顺序: 清账号键与 Cookie -> 清缓存目录 -> 重置设备标识 -> 验证结果。",
            text_color=FG_MUTED,
            font=ui_font(11),
            wraplength=420,
            justify="left",
        ).pack(anchor="w", pady=(10, 14))

        grid = ctk.CTkFrame(inner, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1), weight=1)

        buttons = [
            ("清理账号状态", DANGER, DANGER_HOVER, self._on_clear),
            ("清缓存目录", WARN, WARN_HOVER, self._on_clean_cache),
            ("重置设备标识", ACCENT_ALT, ACCENT_ALT_HOVER, self._on_reset),
            ("刷新检测", GHOST, GHOST_HOVER, self._on_refresh),
        ]
        for index, (text, color, hover, command) in enumerate(buttons):
            button = ctk.CTkButton(
                grid,
                text=text,
                height=44,
                fg_color=color,
                hover_color=hover,
                text_color=FG_LIGHT if color != GHOST else FG_PRIMARY,
                corner_radius=16,
                font=ui_font(13, "bold" if color != GHOST else "normal"),
                command=command,
            )
            button.grid(row=index // 2, column=index % 2, sticky="ew", padx=(0, 10) if index % 2 == 0 else (0, 0), pady=(0, 10))
            self.action_btns.append(button)

        if IS_WIN and not is_admin():
            admin = ctk.CTkFrame(inner, fg_color=BG_SOFT, corner_radius=18, border_width=1, border_color=BORDER)
            admin.pack(fill="x", pady=(8, 0))
            row = ctk.CTkFrame(admin, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=12)
            ctk.CTkLabel(
                row,
                text="当前不是管理员权限。若目录中文件仍被占用，可提升权限后再次执行。",
                text_color=FG_SECONDARY,
                font=ui_font(11),
                wraplength=250,
                justify="left",
            ).pack(side="left", fill="x", expand=True)
            ctk.CTkButton(
                row,
                text="管理员重启",
                width=108,
                height=36,
                fg_color=GHOST,
                hover_color=GHOST_HOVER,
                text_color=FG_PRIMARY,
                corner_radius=14,
                font=ui_font(12),
                command=self._restart_admin,
            ).pack(side="right", padx=(12, 0))

    def _build_health_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True, pady=(12, 0))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(inner, text="覆盖面与提示", text_color=FG_PRIMARY, font=ui_font(18, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            inner,
            textvariable=self.health_var,
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=420,
            justify="left",
        ).pack(anchor="w", pady=(6, 14))

        tips = ctk.CTkFrame(inner, fg_color=BG_SOFT, corner_radius=18, border_width=1, border_color=BORDER)
        tips.pack(fill="both", expand=True)
        for text in GUIDE_TIPS:
            row = ctk.CTkFrame(tips, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=8)
            ctk.CTkLabel(row, text="•", text_color=ACCENT_ALT, font=ui_font(18, "bold"), width=18).pack(side="left")
            ctk.CTkLabel(row, text=text, text_color=FG_SECONDARY, font=ui_font(12), wraplength=340, justify="left").pack(side="left", fill="x", expand=True)

        source_box = ctk.CTkFrame(inner, fg_color=BG_HERO, corner_radius=18, border_width=1, border_color=BORDER)
        source_box.pack(fill="x", pady=(12, 0))
        ctk.CTkLabel(source_box, text="项目来源", text_color=ACCENT, font=ui_font(13, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
        ctk.CTkLabel(
            source_box,
            text=PERSISTENT_NOTICE_TEXT,
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=340,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 12))

    def _build_startup_gate(self):
        self.startup_gate = ctk.CTkFrame(self.root_frame, fg_color=BG_APP, corner_radius=28, border_width=0)

        shell = ctk.CTkFrame(self.startup_gate, fg_color="transparent")
        shell.place(relx=0.5, rely=0.5, anchor="center")

        card = ctk.CTkFrame(shell, fg_color=BG_SURFACE, corner_radius=28, border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True)

        hero = ctk.CTkFrame(card, fg_color=BG_HERO, corner_radius=24)
        hero.pack(fill="x", padx=20, pady=20)
        icon = ctk.CTkFrame(hero, fg_color=ACCENT, corner_radius=18, width=78, height=78)
        icon.pack(pady=(24, 12))
        icon.pack_propagate(False)
        if self.logo_image_large:
            ctk.CTkLabel(icon, text="", image=self.logo_image_large).place(relx=0.5, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(icon, text="T", text_color=FG_LIGHT, font=ui_font(34, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(hero, text="TraeReset", text_color=FG_PRIMARY, font=ui_font(28, "bold")).pack()
        ctk.CTkLabel(
            hero,
            text="首次启动前请先确认免责声明。确认后即可进入主界面继续操作。",
            text_color=FG_SECONDARY,
            font=ui_font(13),
        ).pack(pady=(6, 24))

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=28, pady=(0, 24))
        ctk.CTkLabel(body, text="免责声明", text_color=FG_PRIMARY, font=ui_font(18, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            body,
            text="本工具只修改本地用户数据，不改动 Trae 程序本体。",
            text_color=FG_SECONDARY,
            font=ui_font(13),
            wraplength=700,
            justify="left",
        ).pack(anchor="w", pady=(6, 12))

        textbox = ctk.CTkTextbox(
            body,
            width=720,
            height=220,
            fg_color=BG_SOFT,
            text_color=FG_SECONDARY,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            font=ui_font(13),
            wrap="word",
        )
        textbox.insert("1.0", DISCLAIMER_TEXT)
        textbox.configure(state="disabled")
        textbox.pack(fill="x")

        source_card = ctk.CTkFrame(body, fg_color=BG_HERO, corner_radius=18, border_width=1, border_color=BORDER)
        source_card.pack(fill="x", pady=(14, 0))
        ctk.CTkLabel(source_card, text="开源来源与反转售提示", text_color=FG_PRIMARY, font=ui_font(14, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
        ctk.CTkLabel(
            source_card,
            text=PERSISTENT_NOTICE_TEXT,
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=680,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 12))

        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.pack(fill="x", pady=(20, 0))
        ctk.CTkButton(
            actions,
            text="同意并继续",
            width=220,
            height=48,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=FG_LIGHT,
            corner_radius=16,
            font=ui_font(15, "bold"),
            command=self._accept_startup_gate,
        ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(
            actions,
            text="退出程序",
            width=160,
            height=48,
            fg_color=GHOST,
            hover_color=GHOST_HOVER,
            text_color=FG_PRIMARY,
            corner_radius=16,
            font=ui_font(15),
            command=self._exit_from_startup_gate,
        ).pack(side="left")

    def _refresh_runtime_state(self):
        self.runtime_var.set("Trae 正在运行" if is_trae_running() else "Trae 当前未运行，可安全执行本地重置")

    def _show_startup_gate(self):
        if self._startup_locked:
            return
        self._startup_locked = True
        self._set_btns(False)
        self.startup_gate.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.startup_gate.lift()

    def _accept_startup_gate(self):
        save_disclaimer_accepted()
        self._startup_locked = False
        self.startup_gate.place_forget()
        self._set_btns(True)
        self._set_summary("免责声明已确认")
        self._log("用户已确认免责声明", "info")
        self._log(f"来源提示: {PROJECT_GITHUB_URL}", "dim")
        self._log(REFUND_NOTICE, "warn")

    def _exit_from_startup_gate(self):
        self.destroy()
        sys.exit(0)

    def _show_disclaimer(self):
        DisclaimerDialog(self, logo_image=self.logo_image_large)

    def _set_summary(self, text):
        self.summary_var.set(text)

    def _set_status_badge(self, text, color):
        self.status_badge_var.set(text)
        self.status_badge.configure(fg_color=color)

    def _set_textbox_value(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def _update_status_panel(self, status):
        account_count = len(status["accounts"])
        self.hero_stats["accounts"].configure(text=str(account_count))
        self.hero_stats["session"].configure(text=str(status["session_path_count"]))
        self.hero_stats["storage"].configure(text=str(status["storage_key_count"]))

        self.info_values["accounts"].configure(text=f"{account_count} 个")
        self._set_textbox_value(self.info_values["detail"], ", ".join(status["accounts"]) if status["accounts"] else "无登录账号")
        self._set_textbox_value(self.info_values["mid"], status["machine_id"])
        self._set_textbox_value(self.info_values["tmid"], status["telemetry_machine_id"])
        self._set_textbox_value(self.info_values["did"], status["dev_device_id"])
        self._set_textbox_value(self.info_values["sqm"], status["sqm_id"])
        cache_text = f"{status['session_path_count']} 个目标" if status["session_path_count"] else "未发现缓存目标"
        self.info_values["cache"].configure(text=cache_text)
        self._set_textbox_value(self.info_values["risk"], status["risk_summary"])
        self.health_var.set(
            f"当前目录检测到 {account_count} 个账号条目、{status['storage_key_count']} 个存储键、{status['session_path_count']} 个缓存目标。"
        )

        if account_count or status["storage_key_count"] or status["session_path_count"]:
            self._set_status_badge("存在残留状态", WARN)
        else:
            self._set_status_badge("状态较干净", SUCCESS)

    def _log(self, message, tag=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        self.log_box.configure(state="normal")
        self.log_box.insert("end", line, tag if tag else ())
        line_count = int(self.log_box.index("end-1c").split(".")[0])
        if line_count > 700:
            self.log_box.delete("1.0", f"{line_count - 500}.0")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_btns(self, enabled):
        state = "normal" if enabled else "disabled"
        for button in self.action_btns:
            button.configure(state=state)

    def _check(self):
        if self._startup_locked:
            return False
        if not self.current_dir:
            messagebox.showwarning("提示", "请先选择 Trae 数据目录")
            return False
        if is_trae_running():
            hint = "右键任务栏 Trae 图标退出，或在任务管理器结束 Trae 进程。" if IS_WIN else "请先从菜单或命令行完全退出 Trae。"
            messagebox.showwarning("Trae 正在运行", f"请先关闭 Trae 再操作。\n\n{hint}")
            return False
        return True

    def _do_refresh(self, silent=False):
        if not self.current_dir:
            if not silent:
                self._log("请先选择数据目录", "warn")
            return
        status = get_status(self.current_dir)
        self._update_status_panel(status)
        self.after(10, self._refresh_runtime_state)
        if not silent:
            self._set_summary("状态已刷新")
            self._log("已刷新目录状态", "info")

    def _on_browse(self):
        selected = filedialog.askdirectory(title="选择 Trae 数据目录")
        if not selected:
            return
        if not is_valid_trae_dir(selected):
            messagebox.showwarning("目录无效", f"未在该目录下找到 Trae 常见数据文件。\n\n通常位于:\n{DIR_HINT}")
            return
        self.current_dir = selected
        self._set_textbox_value(self.dir_text, selected)
        self._log(f"已切换目录: {selected}", "info")
        self._set_summary("目录已切换")
        self._do_refresh(silent=True)

    def _on_refresh(self):
        self._do_refresh()

    def _run_action(self, action_name, func, success_text, confirm_title, confirm_message):
        if not self._check():
            return
        if not messagebox.askyesno(confirm_title, confirm_message):
            return
        self._set_btns(False)
        self._set_summary(f"正在执行: {action_name}")
        self._log(f"开始执行: {action_name}", "info")
        try:
            func()
            self._set_summary(success_text)
        except PermissionError:
            self._log("权限不足，部分文件可能被占用或需要更高权限", "err")
            self._set_summary(f"{action_name}失败: 权限不足")
        except Exception as exc:
            self._log(f"错误: {exc}", "err")
            self._set_summary(f"{action_name}失败")
        finally:
            self._set_btns(True)
            self._do_refresh(silent=True)

    def _on_clear(self):
        def action():
            logs, removed = clear_accounts(self.current_dir)
            for line in logs:
                self._log(line)
            self._log("账号状态清理完成" if removed else "未发现可清理的账号状态", "ok" if removed else "warn")

        self._run_action(
            "清理账号状态",
            action,
            "账号状态清理完成",
            "确认清理账号状态",
            "将删除 storage.json 中的账号/权益键，并清理 Cookie 文件。\n\n确定继续吗？",
        )

    def _on_clean_cache(self):
        def action():
            logs, removed = deep_clean_local_state(self.current_dir)
            for line in logs:
                self._log(line)
            self._log("缓存目录清理完成" if removed else "未发现需要清理的缓存目录", "ok" if removed else "warn")

        self._run_action(
            "清缓存目录",
            action,
            "缓存目录清理完成",
            "确认清理缓存目录",
            "将删除或重建本地数据库、缓存和会话目录。\n\n确定继续吗？",
        )

    def _on_reset(self):
        def action():
            logs, ids = reset_device_id(self.current_dir)
            for line in logs:
                self._log(line)
            verification = verify_write(self.current_dir, ids)
            for detail in verification["details"]:
                self._log(f"  验证: {detail}", "ok" if verification["ok"] else "warn")
            self._log(verification["summary"], "ok" if verification["ok"] else "warn")

        self._run_action(
            "重置设备标识",
            action,
            "设备标识重置完成",
            "确认重置设备标识",
            "将重写 machineid 和 telemetry 设备字段。\n\n确定继续吗？",
        )

    def _on_oneclick(self):
        def action():
            self._log("步骤 1/4: 清理账号状态", "info")
            clear_logs, _ = clear_accounts(self.current_dir)
            for line in clear_logs:
                self._log(line)

            self._log("步骤 2/4: 清理缓存目录", "info")
            cache_logs, _ = deep_clean_local_state(self.current_dir)
            for line in cache_logs:
                self._log(line)

            self._log("步骤 3/4: 重置设备标识", "info")
            reset_logs, ids = reset_device_id(self.current_dir)
            for line in reset_logs:
                self._log(line)

            self._log("步骤 4/4: 验证结果", "info")
            verification = verify_write(self.current_dir, ids)
            for detail in verification["details"]:
                self._log(f"  {detail}", "ok" if verification["ok"] else "warn")
            self._log(verification["summary"], "ok" if verification["ok"] else "warn")

        self._run_action(
            "一键深度重置",
            action,
            "一键深度重置已完成",
            "确认一键深度重置",
            "将连续执行以下操作:\n\n1. 清理账号状态\n2. 清理缓存目录\n3. 重置设备标识\n4. 验证结果\n\n确定继续吗？",
        )

    def _on_restore(self):
        if not self.current_dir:
            messagebox.showwarning("提示", "请先选择数据目录")
            return
        if is_trae_running():
            messagebox.showwarning("Trae 正在运行", "请先关闭 Trae 再恢复备份。")
            return
        if not messagebox.askyesno("确认恢复备份", "将恢复最近一次自动备份覆盖到当前目录。\n\n确定继续吗？"):
            return

        self._set_btns(False)
        self._set_summary("正在恢复备份")
        self._log("开始恢复最近一次备份", "info")
        try:
            logs, count = restore_backup(self.current_dir)
            for line in logs:
                self._log(line)
            if count:
                self._log("备份恢复完成", "ok")
                self._set_summary("备份恢复完成")
            else:
                self._log("未找到可恢复的备份", "warn")
                self._set_summary("未找到可恢复的备份")
        except Exception as exc:
            self._log(f"恢复失败: {exc}", "err")
            self._set_summary("恢复备份失败")
        finally:
            self._set_btns(True)
            self._do_refresh(silent=True)

    def _restart_admin(self):
        if restart_as_admin():
            self.destroy()
            sys.exit(0)
        messagebox.showerror("失败", "无法以管理员身份重启")

    def _on_about(self):
        messagebox.showinfo(
            "关于",
            f"{APP_TITLE}\n\n"
            f"开源作者：{BRAND_NAME}\n"
            f"项目地址：{PROJECT_GITHUB_URL}\n\n"
            "Trae 本地状态深度重置工具\n\n"
            "功能范围:\n"
            "- 清理账号与权益残留键\n"
            "- 清理常见 Cookie / 缓存 / 本地数据库\n"
            "- 重置设备标识并验证写入\n\n"
            f"{ANTI_RESALE_NOTICE}\n"
            f"{REFUND_NOTICE}",
        )
