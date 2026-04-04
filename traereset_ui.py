#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TraeReset UI layer."""

from __future__ import annotations

import sys
import threading
import webbrowser
from datetime import datetime
import tkinter as tk

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
    DISCLAIMER_TEXT_EN,
    FONT_MONO,
    FONT_UI,
    GUIDE_TIPS,
    IS_WIN,
    PERSISTENT_NOTICE_TEXT,
    PROJECT_GITHUB_URL,
    REFUND_NOTICE,
    SOURCE_NOTICE,
    VERSION,
    check_for_updates,
    clear_accounts,
    deep_clean_local_state,
    discover_logo_path,
    get_language,
    get_status,
    has_accepted_disclaimer,
    is_admin,
    is_trae_running,
    is_valid_trae_dir,
    reset_device_id,
    restart_as_admin,
    restore_backup,
    save_disclaimer_accepted,
    save_language,
    verify_write,
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG_APP = "#eef8f6"
BG_SURFACE = "#ffffff"
BG_SOFT = "#f4fcfa"
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
LOG_OK = "#2f9b72"
LOG_WARN = "#cf8a22"
LOG_ERR = "#d45a5a"
LOG_DIM = "#78949b"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 920
MIN_WIDTH = 1120
MIN_HEIGHT = 800


def ui_font(size, weight="normal"):
    return ctk.CTkFont(family=FONT_UI, size=size, weight=weight)


def mono_font(size, weight="normal"):
    return ctk.CTkFont(family=FONT_MONO, size=size, weight=weight)


STRINGS = {
    "zh-CN": {
        "language_name": "中文",
        "language_toggle": "EN",
        "app_subtitle": "更清晰地识别账号状态，并以一键重置为主流程。",
        "running": "Trae 正在运行",
        "safe": "Trae 当前未运行，可安全执行本地重置",
        "missing_default_dir": "未检测到默认 Trae 目录，请手动选择。",
        "status_waiting": "等待检测",
        "status_dirty": "存在残留状态",
        "status_clean": "状态较干净",
        "status_missing": "未找到默认目录",
        "summary_idle": "尚未执行操作",
        "summary_loading": "正在加载本地状态",
        "summary_loaded": "已加载默认目录",
        "summary_missing": "未检测到默认目录，请手动选择",
        "summary_switched": "目录已切换",
        "summary_refreshed": "状态已刷新",
        "summary_disclaimer": "免责声明已确认",
        "summary_update_latest": "当前已经是最新版本",
        "summary_update_available": "检测到新版本可用",
        "summary_update_failed": "检查更新失败",
        "summary_update_idle": "尚未检查更新",
        "top_disclaimer": "免责声明",
        "top_about": "关于",
        "top_check_update": "检查更新",
        "hero_title": "一键重置前先确认账号与本地状态",
        "hero_detail_loading": "正在读取目录、账号和缓存状态。",
        "hero_detail_blocked": "Trae 正在运行，请先关闭后再执行重置。",
        "hero_detail_attention": "当前目录检测到 {account_count} 个账号、{storage_count} 个存储键、{cache_count} 个缓存目标，建议确认后再重置。",
        "hero_detail_ready": "未发现明显账号缓存，可直接查看明细或继续执行。",
        "hero_detail_missing": "未检测到默认 Trae 目录，请先手动选择。",
        "hero_notice_title": "开源来源与反转售提示",
        "accounts_title": "当前账号",
        "accounts_subtitle": "重置前先确认当前目录里识别到的账号，避免误清理。",
        "accounts_empty": "未检测到账号",
        "accounts_detected": "检测到 {count} 个账号",
        "accounts_unknown": "未知账号",
        "contact_none": "未发现邮箱或手机号",
        "status_title": "本地状态摘要",
        "status_subtitle": "这里展示设备标识、缓存覆盖和风险摘要。",
        "field_machine": "Machine ID",
        "field_telemetry": "Telemetry ID",
        "field_device": "Device ID",
        "field_sqm": "SQM ID",
        "field_storage": "存储键",
        "field_cache": "缓存目标",
        "field_risk": "风险摘要",
        "field_folder": "当前目录",
        "folder_title": "目录与恢复",
        "folder_subtitle": "所有修改前会自动生成 .bak 备份；“恢复最近一次自动备份”会基于当前目录执行。",
        "advanced_expand": "展开高级选项",
        "advanced_collapse": "收起高级选项",
        "summary_oneclick_running": "正在执行一键深度重置",
        "summary_oneclick_done": "一键深度重置已完成",
        "summary_restore_running": "正在恢复最近一次自动备份",
        "summary_restore_done": "最近一次自动备份已恢复",
        "summary_restore_missing": "未找到最近一次自动备份",
        "summary_checking_update": "正在检查更新",
        "update_checking": "检查中...",
        "folder_current": "当前操作目录",
        "folder_missing": "未选择目录",
        "btn_choose": "选择目录",
        "btn_restore": "恢复最近一次自动备份",
        "action_title": "主操作",
        "action_subtitle": "先确认目录和账号，再执行一键深度重置。细粒度能力放进高级选项。",
        "btn_oneclick": "一键深度重置",
        "btn_refresh": "刷新状态",
        "btn_update": "检查更新",
        "advanced_title": "高级选项",
        "btn_clear_accounts": "清理账号状态",
        "btn_clean_cache": "清缓存目录",
        "btn_reset_device": "重置设备标识",
        "log_title": "执行日志",
        "health_title": "覆盖面与提示",
        "health_summary": "当前目录检测到 {account_count} 个账号、{storage_count} 个存储键、{cache_count} 个缓存目标。",
        "health_accounts": "账号",
        "health_storage": "存储键",
        "health_cache": "缓存目标",
        "health_runtime": "运行状态",
        "version_status": "版本状态",
        "version_label": "当前版本 {version}",
        "update_status_idle": "尚未检查更新",
        "update_status_checking": "正在检查 GitHub Releases",
        "update_status_latest": "已是最新版本",
        "update_status_available": "发现新版本 {latest}",
        "update_status_failed": "检查失败：{error}",
        "startup_title": "首次启动前请先确认免责声明",
        "startup_subtitle": "确认后即可进入主界面继续操作。",
        "startup_body": "本工具只修改本地用户数据，不改动 Trae 程序本体。",
        "btn_accept": "同意并继续",
        "btn_exit": "退出程序",
        "btn_close": "关闭",
        "dir_invalid": "目录无效",
        "dir_invalid_msg": "未在该目录下找到 Trae 常见数据文件。\n\n通常位于:\n{hint}",
        "select_dir_first": "请先选择 Trae 数据目录",
        "close_trae_title": "Trae 正在运行",
        "close_trae_msg": "请先关闭 Trae 再操作。\n\n{hint}",
        "close_trae_restore": "请先关闭 Trae 再恢复备份。",
        "confirm_clear_title": "确认清理账号状态",
        "confirm_clear_msg": "将删除 storage.json 中的账号/权益键，并清理 Cookie 文件。\n\n确定继续吗？",
        "confirm_cache_title": "确认清理缓存目录",
        "confirm_cache_msg": "将删除或重建本地数据库、缓存和会话目录。\n\n确定继续吗？",
        "confirm_reset_title": "确认重置设备标识",
        "confirm_reset_msg": "将重写 machineid 和 telemetry 设备字段。\n\n确定继续吗？",
        "confirm_oneclick_title": "确认一键深度重置",
        "confirm_oneclick_msg": "将连续执行以下操作:\n\n1. 清理账号状态\n2. 清理缓存目录\n3. 重置设备标识\n4. 验证结果\n\n确定继续吗？",
        "confirm_restore_title": "确认恢复最近一次自动备份",
        "confirm_restore_msg": "将恢复最近一次自动备份覆盖到当前目录。\n\n确定继续吗？",
        "about_title": "关于",
        "about_body": "{app_title}\n\n开源作者：{brand}\n项目地址：{url}\n\nTrae 本地状态深度重置工具\n\n功能范围:\n- 清理账号与权益残留键\n- 清理常见 Cookie / 缓存 / 本地数据库\n- 重置设备标识并验证写入\n\n{anti_resale}\n{refund}",
        "backup_auto_log": "本次操作会在修改前自动生成 .bak 备份。",
        "update_latest_title": "已是最新版本",
        "update_latest_msg": "当前版本 {current} 已是最新版本。",
        "update_available_title": "发现新版本",
        "update_available_msg": "当前版本: {current}\n最新版本: {latest}\n\n是否打开发布页？",
        "update_failed_title": "检查更新失败",
        "update_failed_msg": "无法获取最新版本信息。\n\n{error}",
        "admin_hint": "当前不是管理员权限。若目录中文件仍被占用，可提升权限后再次执行。",
        "admin_restart": "管理员重启",
    },
    "en-US": {
        "language_name": "English",
        "language_toggle": "中文",
        "app_subtitle": "Review detected accounts first, then use deep reset as the main flow.",
        "running": "Trae is running",
        "safe": "Trae is not running. Local reset is safe to perform.",
        "missing_default_dir": "Default Trae directory was not detected. Please choose it manually.",
        "status_waiting": "Waiting",
        "status_dirty": "State detected",
        "status_clean": "State looks clean",
        "status_missing": "Default folder missing",
        "summary_idle": "No action has been run yet",
        "summary_loading": "Loading local state",
        "summary_loaded": "Default directory loaded",
        "summary_missing": "Default Trae directory was not detected",
        "summary_switched": "Directory switched",
        "summary_refreshed": "Status refreshed",
        "summary_disclaimer": "Disclaimer accepted",
        "summary_update_latest": "Already on the latest version",
        "summary_update_available": "A newer version is available",
        "summary_update_failed": "Update check failed",
        "top_disclaimer": "Disclaimer",
        "top_about": "About",
        "top_check_update": "Check Update",
        "hero_title": "Review account traces before deep reset",
        "hero_detail_loading": "Reading folder, account, and cache state.",
        "hero_detail_blocked": "Trae is still running. Close it before resetting.",
        "hero_detail_attention": "Detected {account_count} account(s), {storage_count} storage key(s), and {cache_count} cache target(s). Review them before resetting.",
        "hero_detail_ready": "No obvious account residue was found. You can review details or continue.",
        "hero_detail_missing": "Default Trae directory was not detected. Please choose it manually.",
        "hero_notice_title": "Open-source origin and anti-resale notice",
        "accounts_title": "Current Accounts",
        "accounts_subtitle": "Review the detected accounts in this directory before clearing anything.",
        "accounts_empty": "No accounts detected",
        "accounts_detected": "{count} account(s) detected",
        "accounts_unknown": "Unknown account",
        "contact_none": "No email or phone found",
        "status_title": "Local State Summary",
        "status_subtitle": "Device identifiers, cache targets, and risk summary are shown here.",
        "field_machine": "Machine ID",
        "field_telemetry": "Telemetry ID",
        "field_device": "Device ID",
        "field_sqm": "SQM ID",
        "field_storage": "Storage Keys",
        "field_cache": "Cache Targets",
        "field_risk": "Risk Summary",
        "field_folder": "Current Folder",
        "folder_title": "Directory and Restore",
        "folder_subtitle": "Path selection, backups, and restore all work on the current folder.",
        "advanced_expand": "Show Advanced Options",
        "advanced_collapse": "Hide Advanced Options",
        "summary_oneclick_running": "Running deep reset",
        "summary_oneclick_done": "Deep reset completed",
        "summary_restore_running": "Restoring backup",
        "summary_restore_done": "Backup restored",
        "summary_restore_missing": "No backup was found",
        "summary_checking_update": "Checking for updates",
        "update_checking": "Checking...",
        "folder_current": "Current Working Folder",
        "folder_missing": "No folder selected",
        "btn_choose": "Select Folder",
        "btn_restore": "Restore Latest Auto Backup",
        "action_title": "Primary Actions",
        "action_subtitle": "Confirm the folder and detected accounts first, then run Deep Reset. Advanced steps stay secondary.",
        "btn_oneclick": "Deep Reset",
        "btn_refresh": "Refresh Status",
        "btn_update": "Check Update",
        "advanced_title": "Advanced Options",
        "btn_clear_accounts": "Clear Account State",
        "btn_clean_cache": "Clean Cache Targets",
        "btn_reset_device": "Reset Device IDs",
        "log_title": "Execution Log",
        "health_title": "Coverage and Notes",
        "health_summary": "Detected {account_count} account(s), {storage_count} storage key(s), and {cache_count} cache target(s) in the current directory.",
        "health_accounts": "Accounts",
        "health_storage": "Storage Keys",
        "health_cache": "Cache Targets",
        "health_runtime": "Runtime",
        "version_status": "Version Status",
        "version_label": "Current version {version}",
        "update_status_idle": "Update has not been checked yet",
        "update_status_checking": "Checking GitHub Releases",
        "update_status_latest": "Already on the latest release",
        "update_status_available": "Update available: {latest}",
        "update_status_failed": "Check failed: {error}",
        "startup_title": "Please confirm the disclaimer before first use",
        "startup_subtitle": "Accept it to continue into the main interface.",
        "startup_body": "This tool only changes local user data. It does not modify the Trae application itself.",
        "btn_accept": "Accept and Continue",
        "btn_exit": "Exit",
        "btn_close": "Close",
        "dir_invalid": "Invalid folder",
        "dir_invalid_msg": "Common Trae data files were not found in this folder.\n\nTypical path:\n{hint}",
        "select_dir_first": "Please choose a Trae data directory first",
        "close_trae_title": "Trae is running",
        "close_trae_msg": "Please close Trae before continuing.\n\n{hint}",
        "close_trae_restore": "Please close Trae before restoring the latest auto backup.",
        "confirm_clear_title": "Clear account state",
        "confirm_clear_msg": "This removes account and entitlement keys from storage.json and clears cookie files.\n\nContinue?",
        "confirm_cache_title": "Clean cache targets",
        "confirm_cache_msg": "This removes or rebuilds local databases, caches, and session folders.\n\nContinue?",
        "confirm_reset_title": "Reset device identifiers",
        "confirm_reset_msg": "This rewrites machineid and telemetry device fields.\n\nContinue?",
        "confirm_oneclick_title": "Run deep reset",
        "confirm_oneclick_msg": "The following steps will be executed:\n\n1. Clear account state\n2. Clean cache targets\n3. Reset device identifiers\n4. Verify results\n\nContinue?",
        "confirm_restore_title": "Restore backup",
        "confirm_restore_msg": "This restores the latest backup over the current directory.\n\nContinue?",
        "about_title": "About",
        "about_body": "{app_title}\n\nOpen-source author: {brand}\nProject URL: {url}\n\nTrae local state deep reset tool\n\nScope:\n- Clear account and entitlement traces\n- Clear common cookies, caches, and local databases\n- Reset device identifiers and verify writes\n\n{anti_resale}\n{refund}",
        "backup_auto_log": "A .bak backup will be created automatically before changes.",
        "update_latest_title": "Already up to date",
        "update_latest_msg": "Current version {current} is already the latest release.",
        "update_available_title": "Update available",
        "update_available_msg": "Current version: {current}\nLatest version: {latest}\n\nOpen the release page now?",
        "update_failed_title": "Update check failed",
        "update_failed_msg": "Unable to fetch the latest release information.\n\n{error}",
        "admin_hint": "This app is not running as administrator. Elevate only if files remain locked.",
        "admin_restart": "Restart as Admin",
    },
}

class DisclaimerDialog(ctk.CTkToplevel):
    def __init__(self, master, strings, language):
        super().__init__(master, fg_color=BG_APP)
        self.strings = strings
        self.language = language
        self.title(self.t("top_disclaimer"))
        self.resizable(True, True)
        self.geometry("820x700")
        self.minsize(760, 640)
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self._build()
        self.update_idletasks()
        x = master.winfo_rootx() + max(0, (master.winfo_width() - 820) // 2)
        y = master.winfo_rooty() + max(0, (master.winfo_height() - 700) // 2)
        self.geometry(f"820x700+{x}+{y}")

    def t(self, key, **kwargs):
        text = self.strings[self.language][key]
        return text.format(**kwargs) if kwargs else text

    def disclaimer_text(self):
        return DISCLAIMER_TEXT if self.language == "zh-CN" else DISCLAIMER_TEXT_EN

    def _build(self):
        shell = ctk.CTkFrame(self, fg_color=BG_APP)
        shell.pack(fill="both", expand=True, padx=16, pady=16)

        card = ctk.CTkFrame(shell, fg_color=BG_SURFACE, corner_radius=26, border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True)

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=22)

        header = ctk.CTkFrame(body, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=self.t("top_disclaimer"), text_color=FG_PRIMARY, font=ui_font(22, "bold")).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text=self.t("startup_body"),
            text_color=FG_SECONDARY,
            font=ui_font(12),
            wraplength=720,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

        self.disclaimer_notice_label = ctk.CTkLabel(
            body,
            text=PERSISTENT_NOTICE_TEXT,
            text_color=FG_SECONDARY,
            font=ui_font(11),
            wraplength=720,
            justify="left",
        )
        self.disclaimer_notice_label.pack(anchor="w", pady=(12, 12))

        self.disclaimer_textbox = ctk.CTkTextbox(
            body,
            fg_color=BG_SOFT,
            text_color=FG_SECONDARY,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            font=ui_font(13),
            wrap="word",
        )
        self.disclaimer_textbox.insert("1.0", self.disclaimer_text())
        self.disclaimer_textbox.configure(state="disabled")
        self.disclaimer_textbox.pack(fill="both", expand=True)

        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.pack(fill="x", pady=(14, 0))
        ctk.CTkButton(
            actions,
            text=self.t("btn_close"),
            width=140,
            height=42,
            fg_color=GHOST,
            hover_color=GHOST_HOVER,
            text_color=FG_PRIMARY,
            corner_radius=16,
            font=ui_font(13),
            command=self.destroy,
        ).pack(anchor="e")


def load_logo_image(logo_path, size):
    if not logo_path or not logo_path.exists():
        return None
    try:
        return ctk.CTkImage(light_image=Image.open(logo_path), size=size)
    except Exception:
        return None


def make_account_subtitle(item, language):
    if language == "zh-CN":
        if item.get("email"):
            return item["email"]
        if item.get("phone"):
            return item["phone"]
        return STRINGS[language]["contact_none"]
    if item.get("email"):
        return item["email"]
    if item.get("phone"):
        return item["phone"]
    return STRINGS[language]["contact_none"]


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_APP)
        self.withdraw()
        self.language = get_language()
        self.current_dir = None
        self.logo_path = None
        self.logo_image_small = None
        self._startup_locked = False
        self._advanced_visible = False
        self._initial_loading = True
        self.last_status = None
        self.action_btns = []
        self.account_rows = []
        self.info_values = {}
        self.summary_var = ctk.StringVar(value=self.t("summary_idle"))
        self.status_badge_var = ctk.StringVar(value=self.t("status_waiting"))
        self.runtime_var = ctk.StringVar(value=self.t("status_waiting"))
        self.update_status_var = ctk.StringVar(value=self.t("update_status_idle"))
        self.update_status_key = "update_status_idle"
        self.update_status_kwargs = {}
        self.title(APP_TITLE)
        self.geometry(self._center_geometry(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self._build_main()
        self.after(10, self._finish_startup)

    def t(self, key, **kwargs):
        text = STRINGS[self.language][key]
        return text.format(**kwargs) if kwargs else text

    def disclaimer_text(self):
        return DISCLAIMER_TEXT if self.language == "zh-CN" else DISCLAIMER_TEXT_EN

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
        self._set_summary(self.t("summary_loading"))
        self.runtime_var.set(self.t("status_waiting"))
        self.hero_summary.configure(text=self.t("status_waiting"))
        self.hero_detail.configure(text=self.t("hero_detail_loading"))
        self._set_textbox_value(self.dir_text, self.t("folder_missing"))

        self.deiconify()
        self.lift()
        self.focus_force()
        self.after(30, self._start_initial_load)
        self.after(200, self._load_logo_later)
        if not has_accepted_disclaimer():
            self.after(120, self._show_startup_gate)

    def _build_main(self):
        self.root_frame = ctk.CTkFrame(self, fg_color=BG_APP)
        self.root_frame.pack(fill="both", expand=True, padx=18, pady=18)
        self._build_topbar(self.root_frame)

        content_host = ctk.CTkFrame(self.root_frame, fg_color="transparent")
        content_host.pack(fill="both", expand=True, pady=(14, 0))
        self.content_canvas = tk.Canvas(content_host, bg=BG_APP, highlightthickness=0, bd=0)
        self.content_scrollbar = ctk.CTkScrollbar(content_host, orientation="vertical", command=self.content_canvas.yview)
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)
        self.content_scrollbar.pack(side="right", fill="y")
        self.content_canvas.pack(side="left", fill="both", expand=True)
        content = ctk.CTkFrame(self.content_canvas, fg_color="transparent")
        self.content_window = self.content_canvas.create_window((0, 0), window=content, anchor="nw")
        content.bind("<Configure>", self._on_content_configure)
        self.content_canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)
        content.grid_columnconfigure(0, weight=5)
        content.grid_columnconfigure(1, weight=4)
        content.grid_rowconfigure(2, weight=1)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=(0, 10))
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.grid(row=0, column=1, rowspan=3, sticky="nsew")

        self._build_hero(left)
        self._build_accounts_card(left)
        self._build_log_card(left)
        self._build_status_card(left)
        self._build_folder_card(right)
        self._build_action_card(right)
        self._build_health_card(right)
        self._build_startup_gate()
        self._set_btns(False)

    def _build_topbar(self, parent):
        self.topbar = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        self.topbar.pack(fill="x")
        inner = ctk.CTkFrame(self.topbar, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=10)

        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        title_row = ctk.CTkFrame(left, fg_color="transparent")
        title_row.pack(anchor="w")
        self.topbar_logo_label = ctk.CTkLabel(title_row, text="")
        self.title_label = ctk.CTkLabel(title_row, text=APP_TITLE, text_color=FG_PRIMARY, font=ui_font(24, "bold"))
        self.title_label.pack(side="left")
        self.subtitle_label = ctk.CTkLabel(left, text=self.t("app_subtitle"), text_color=FG_SECONDARY, font=ui_font(11))
        self.subtitle_label.pack(anchor="w", pady=(2, 0))
        status_row = ctk.CTkFrame(left, fg_color="transparent")
        status_row.pack(anchor="w", pady=(6, 0), fill="x")
        self.version_title_label = ctk.CTkLabel(status_row, text=self.t("version_status"), text_color=FG_MUTED, font=ui_font(10, "bold"))
        self.version_title_label.pack(side="left")
        self.version_label = ctk.CTkLabel(status_row, text=self.t("version_label", version=VERSION), text_color=FG_PRIMARY, font=ui_font(11, "bold"))
        self.version_label.pack(side="left", padx=(8, 0))
        self.update_status_label = ctk.CTkLabel(status_row, textvariable=self.update_status_var, text_color=FG_SECONDARY, font=ui_font(11), wraplength=300, justify="left")
        self.update_status_label.pack(side="left", padx=(12, 0))

        right = ctk.CTkFrame(inner, fg_color="transparent")
        right.pack(side="right")
        self.status_badge = ctk.CTkLabel(right, textvariable=self.status_badge_var, text_color=FG_LIGHT, fg_color=ACCENT_ALT, corner_radius=999, width=168, height=34, font=ui_font(11, "bold"))
        self.status_badge.pack(anchor="e")
        buttons = ctk.CTkFrame(right, fg_color="transparent")
        buttons.pack(anchor="e", pady=(8, 0))
        self.lang_button = ctk.CTkButton(buttons, text=self.t("language_toggle"), width=68, height=34, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=14, font=ui_font(11), command=self._toggle_language)
        self.lang_button.pack(side="left", padx=(0, 8))
        self.update_button = ctk.CTkButton(buttons, text=self.t("top_check_update"), width=104, height=34, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=14, font=ui_font(11), command=self._check_updates)
        self.update_button.pack(side="left", padx=(0, 8))
        self.disclaimer_button = ctk.CTkButton(buttons, text=self.t("top_disclaimer"), width=96, height=34, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=14, font=ui_font(11), command=self._show_disclaimer)
        self.disclaimer_button.pack(side="left", padx=(0, 8))
        self.about_button = ctk.CTkButton(buttons, text=self.t("top_about"), width=74, height=34, fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=FG_LIGHT, corner_radius=14, font=ui_font(11, "bold"), command=self._on_about)
        self.about_button.pack(side="left")

    def _build_hero(self, parent):
        self.hero_card = ctk.CTkFrame(parent, fg_color=BG_HERO, corner_radius=28, border_width=1, border_color=BORDER)
        self.hero_card.pack(fill="x")
        inner = ctk.CTkFrame(self.hero_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        self.hero_title = ctk.CTkLabel(inner, text=self.t("hero_title"), text_color=FG_PRIMARY, font=ui_font(24, "bold"), justify="left")
        self.hero_title.pack(anchor="w")
        self.hero_summary = ctk.CTkLabel(inner, text=self.t("status_waiting"), text_color=FG_PRIMARY, font=ui_font(17, "bold"), wraplength=700, justify="left")
        self.hero_summary.pack(anchor="w", pady=(10, 0))
        self.hero_detail = ctk.CTkLabel(inner, text=self.t("summary_idle"), text_color=FG_SECONDARY, font=ui_font(12), wraplength=700, justify="left")
        self.hero_detail.pack(anchor="w", pady=(6, 0))

    def _build_accounts_card(self, parent):
        self.accounts_card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        self.accounts_card.pack(fill="x", pady=(14, 12))
        inner = ctk.CTkFrame(self.accounts_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        self.accounts_title_label = ctk.CTkLabel(inner, text=self.t("accounts_title"), text_color=FG_PRIMARY, font=ui_font(18, "bold"))
        self.accounts_title_label.pack(anchor="w")
        self.accounts_subtitle_label = ctk.CTkLabel(inner, text=self.t("accounts_subtitle"), text_color=FG_SECONDARY, font=ui_font(12), wraplength=720, justify="left")
        self.accounts_subtitle_label.pack(anchor="w", pady=(6, 10))
        self.accounts_list = ctk.CTkFrame(inner, fg_color="transparent")
        self.accounts_list.pack(fill="x")

    def _build_status_card(self, parent):
        self.status_card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        self.status_card.pack(fill="x")
        inner = ctk.CTkFrame(self.status_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)
        self.status_title_label = ctk.CTkLabel(inner, text=self.t("status_title"), text_color=FG_PRIMARY, font=ui_font(18, "bold"))
        self.status_title_label.pack(anchor="w")
        self.status_subtitle_label = ctk.CTkLabel(inner, text=self.t("status_subtitle"), text_color=FG_SECONDARY, font=ui_font(12), wraplength=720, justify="left")
        self.status_subtitle_label.pack(anchor="w", pady=(6, 12))
        fields = [
            ("mid", self.t("field_machine")),
            ("tmid", self.t("field_telemetry")),
            ("did", self.t("field_device")),
            ("sqm", self.t("field_sqm")),
            ("storage", self.t("field_storage")),
            ("cache", self.t("field_cache")),
            ("risk", self.t("field_risk")),
        ]
        self.status_field_labels = {}
        for key, label in fields:
            row = ctk.CTkFrame(inner, fg_color=BG_SOFT, corner_radius=16, border_width=1, border_color=BORDER)
            row.pack(fill="x", pady=5)
            row.grid_columnconfigure(1, weight=1)
            field_label = ctk.CTkLabel(row, text=label, width=150, anchor="w", text_color=FG_MUTED, font=ui_font(12, "bold"))
            field_label.grid(row=0, column=0, sticky="nw", padx=14, pady=12)
            self.status_field_labels[key] = field_label
            if key in {"mid", "tmid", "did", "sqm", "risk"}:
                widget = ctk.CTkTextbox(row, height=48 if key != "risk" else 56, fg_color=BG_SURFACE, text_color=FG_PRIMARY, corner_radius=12, border_width=0, font=mono_font(12) if key != "risk" else ui_font(12), wrap="word")
                widget.insert("1.0", "-")
                widget.configure(state="disabled")
                widget.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=8)
            else:
                widget = ctk.CTkLabel(row, text="-", anchor="w", justify="left", wraplength=520, text_color=FG_PRIMARY, font=ui_font(12))
                widget.grid(row=0, column=1, sticky="ew", padx=(0, 14), pady=12)
            self.info_values[key] = widget

    def _build_log_card(self, parent):
        self.log_card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        self.log_card.pack(fill="both", expand=True, pady=(0, 12))
        inner = ctk.CTkFrame(self.log_card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=16)
        self.log_title_label = ctk.CTkLabel(inner, text=self.t("log_title"), text_color=FG_PRIMARY, font=ui_font(18, "bold"))
        self.log_title_label.pack(anchor="w")
        self.log_summary_label = ctk.CTkLabel(inner, textvariable=self.summary_var, text_color=FG_SECONDARY, font=ui_font(12))
        self.log_summary_label.pack(anchor="w", pady=(6, 10))
        self.log_box = ctk.CTkTextbox(inner, height=240, fg_color=BG_LOG, text_color=FG_PRIMARY, corner_radius=18, border_width=1, border_color=BORDER, wrap="word", state="disabled", font=mono_font(12))
        self.log_box.pack(fill="both", expand=True)
        self.log_box.tag_config("ok", foreground=LOG_OK)
        self.log_box.tag_config("warn", foreground=LOG_WARN)
        self.log_box.tag_config("err", foreground=LOG_ERR)
        self.log_box.tag_config("dim", foreground=LOG_DIM)
        self.log_box.tag_config("info", foreground=ACCENT)

    def _build_folder_card(self, parent):
        self.folder_card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        self.folder_card.pack(fill="x", pady=(0, 12))
        inner = ctk.CTkFrame(self.folder_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)
        self.folder_title_label = ctk.CTkLabel(inner, text=self.t("folder_title"), text_color=FG_PRIMARY, font=ui_font(18, "bold"))
        self.folder_title_label.pack(anchor="w")
        self.folder_subtitle_label = ctk.CTkLabel(inner, text=self.t("folder_subtitle"), text_color=FG_SECONDARY, font=ui_font(12), wraplength=420, justify="left")
        self.folder_subtitle_label.pack(anchor="w", pady=(6, 12))
        self.folder_current_label = ctk.CTkLabel(inner, text=self.t("folder_current"), text_color=FG_MUTED, font=ui_font(12, "bold"))
        self.folder_current_label.pack(anchor="w", pady=(0, 6))
        self.dir_text = ctk.CTkTextbox(inner, height=72, fg_color=BG_SOFT, text_color=FG_PRIMARY, corner_radius=16, border_width=1, border_color=BORDER, font=mono_font(12), wrap="word")
        self.dir_text.insert("1.0", self.t("folder_missing"))
        self.dir_text.configure(state="disabled")
        self.dir_text.pack(fill="x")
        controls = ctk.CTkFrame(inner, fg_color="transparent")
        controls.pack(fill="x", pady=(12, 0))
        self.choose_button = ctk.CTkButton(controls, text=self.t("btn_choose"), width=124, height=40, fg_color=ACCENT_ALT, hover_color=ACCENT_ALT_HOVER, text_color=FG_LIGHT, corner_radius=16, font=ui_font(13, "bold"), command=self._on_browse)
        self.choose_button.pack(side="left", padx=(0, 10))
        self.restore_button_small = ctk.CTkButton(controls, text=self.t("btn_restore"), width=238, height=40, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=16, font=ui_font(12), command=self._on_restore)
        self.restore_button_small.pack(side="left")

    def _build_action_card(self, parent):
        self.action_card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        self.action_card.pack(fill="x")
        inner = ctk.CTkFrame(self.action_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)
        self.action_title_label = ctk.CTkLabel(inner, text=self.t("action_title"), text_color=FG_PRIMARY, font=ui_font(18, "bold"))
        self.action_title_label.pack(anchor="w")
        self.action_subtitle_label = ctk.CTkLabel(inner, text=self.t("action_subtitle"), text_color=FG_SECONDARY, font=ui_font(12), wraplength=420, justify="left")
        self.action_subtitle_label.pack(anchor="w", pady=(6, 14))
        self.primary_button = ctk.CTkButton(inner, text=self.t("btn_oneclick"), height=56, fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=FG_LIGHT, corner_radius=18, font=ui_font(16, "bold"), command=self._on_oneclick)
        self.primary_button.pack(fill="x")
        self.action_btns.append(self.primary_button)
        secondary = ctk.CTkFrame(inner, fg_color="transparent")
        secondary.pack(fill="x", pady=(12, 0))
        secondary.grid_columnconfigure((0, 1), weight=1)
        self.refresh_button = ctk.CTkButton(secondary, text=self.t("btn_refresh"), height=44, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=16, font=ui_font(13), command=self._on_refresh)
        self.refresh_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.action_btns.append(self.refresh_button)
        self.restore_button = ctk.CTkButton(secondary, text=self.t("btn_restore"), height=44, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=16, font=ui_font(13), command=self._on_restore)
        self.restore_button.grid(row=0, column=1, sticky="ew")
        self.action_btns.append(self.restore_button)
        quick_note = ctk.CTkFrame(inner, fg_color=BG_SOFT, corner_radius=16, border_width=1, border_color=BORDER)
        quick_note.pack(fill="x", pady=(12, 0))
        self.quick_note_label = ctk.CTkLabel(quick_note, textvariable=self.summary_var, text_color=FG_SECONDARY, font=ui_font(12), wraplength=420, justify="left")
        self.quick_note_label.pack(anchor="w", padx=14, pady=10)
        self.advanced_toggle = ctk.CTkButton(inner, text=self.t("advanced_title"), height=40, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=16, font=ui_font(13), command=self._toggle_advanced)
        self.advanced_toggle.pack(fill="x", pady=(12, 0))
        self.advanced_panel = ctk.CTkFrame(inner, fg_color=BG_SOFT, corner_radius=18, border_width=1, border_color=BORDER)
        self.advanced_grid = ctk.CTkFrame(self.advanced_panel, fg_color="transparent")
        self.advanced_grid.pack(fill="x", padx=14, pady=14)
        self.advanced_grid.grid_columnconfigure((0, 1), weight=1)
        self.advanced_clear_button = ctk.CTkButton(self.advanced_grid, text=self.t("btn_clear_accounts"), height=42, fg_color=DANGER, hover_color=DANGER_HOVER, text_color=FG_LIGHT, corner_radius=14, font=ui_font(13, "bold"), command=self._on_clear)
        self.advanced_clear_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.advanced_cache_button = ctk.CTkButton(self.advanced_grid, text=self.t("btn_clean_cache"), height=42, fg_color=WARN, hover_color=WARN_HOVER, text_color=FG_LIGHT, corner_radius=14, font=ui_font(13, "bold"), command=self._on_clean_cache)
        self.advanced_cache_button.grid(row=0, column=1, sticky="ew")
        self.advanced_reset_button = ctk.CTkButton(self.advanced_grid, text=self.t("btn_reset_device"), height=42, fg_color=ACCENT_ALT, hover_color=ACCENT_ALT_HOVER, text_color=FG_LIGHT, corner_radius=14, font=ui_font(13, "bold"), command=self._on_reset)
        self.advanced_reset_button.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(10, 0))
        self.action_btns.extend([self.advanced_clear_button, self.advanced_cache_button, self.advanced_reset_button])
        if IS_WIN and not is_admin():
            admin = ctk.CTkFrame(inner, fg_color=BG_SOFT, corner_radius=18, border_width=1, border_color=BORDER)
            admin.pack(fill="x", pady=(12, 0))
            row = ctk.CTkFrame(admin, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=12)
            self.admin_hint_label = ctk.CTkLabel(row, text=self.t("admin_hint"), text_color=FG_SECONDARY, font=ui_font(11), wraplength=250, justify="left")
            self.admin_hint_label.pack(side="left", fill="x", expand=True)
            self.admin_restart_button = ctk.CTkButton(row, text=self.t("admin_restart"), width=130, height=36, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=14, font=ui_font(12), command=self._restart_admin)
            self.admin_restart_button.pack(side="right", padx=(12, 0))

    def _build_health_card(self, parent):
        self.health_card = ctk.CTkFrame(parent, fg_color=BG_SURFACE, corner_radius=24, border_width=1, border_color=BORDER)
        self.health_card.pack(fill="x", pady=(12, 0))
        inner = ctk.CTkFrame(self.health_card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=14)
        self.health_title_label = ctk.CTkLabel(inner, text=self.t("health_title"), text_color=FG_PRIMARY, font=ui_font(18, "bold"))
        self.health_title_label.pack(anchor="w")
        self.health_summary_label = ctk.CTkLabel(inner, text=PERSISTENT_NOTICE_TEXT, text_color=FG_SECONDARY, font=ui_font(11), wraplength=420, justify="left")
        self.health_summary_label.pack(anchor="w", pady=(6, 10))
        tips = ctk.CTkFrame(inner, fg_color=BG_SOFT, corner_radius=18, border_width=1, border_color=BORDER)
        tips.pack(fill="both", expand=True)
        self.tip_labels = []
        for item in GUIDE_TIPS[:2]:
            row = ctk.CTkFrame(tips, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=6)
            ctk.CTkLabel(row, text="•", text_color=ACCENT_ALT, font=ui_font(18, "bold"), width=18).pack(side="left")
            label = ctk.CTkLabel(row, text=item[self.language], text_color=FG_SECONDARY, font=ui_font(12), wraplength=340, justify="left")
            label.pack(side="left", fill="x", expand=True)
            self.tip_labels.append((label, item))

    def _build_startup_gate(self):
        self.startup_gate = ctk.CTkFrame(self.root_frame, fg_color=BG_APP, corner_radius=28, border_width=0)
        shell = ctk.CTkFrame(self.startup_gate, fg_color="transparent")
        shell.place(relx=0.5, rely=0.5, anchor="center")
        card = ctk.CTkFrame(shell, fg_color=BG_SURFACE, corner_radius=28, border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True)
        hero = ctk.CTkFrame(card, fg_color=BG_HERO, corner_radius=24)
        hero.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(hero, text="TraeReset", text_color=FG_PRIMARY, font=ui_font(28, "bold")).pack(pady=(24, 0))
        self.startup_subtitle_label = ctk.CTkLabel(hero, text=self.t("startup_subtitle"), text_color=FG_SECONDARY, font=ui_font(13))
        self.startup_subtitle_label.pack(pady=(6, 24))
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=28, pady=(0, 24))
        self.startup_title_label = ctk.CTkLabel(body, text=self.t("startup_title"), text_color=FG_PRIMARY, font=ui_font(18, "bold"))
        self.startup_title_label.pack(anchor="w")
        self.startup_body_label = ctk.CTkLabel(body, text=self.t("startup_body"), text_color=FG_SECONDARY, font=ui_font(13), wraplength=700, justify="left")
        self.startup_body_label.pack(anchor="w", pady=(6, 12))
        self.startup_textbox = ctk.CTkTextbox(body, width=720, height=220, fg_color=BG_SOFT, text_color=FG_SECONDARY, corner_radius=18, border_width=1, border_color=BORDER, font=ui_font(13), wrap="word")
        self.startup_textbox.insert("1.0", self.disclaimer_text())
        self.startup_textbox.configure(state="disabled")
        self.startup_textbox.pack(fill="x")
        source_card = ctk.CTkFrame(body, fg_color=BG_HERO, corner_radius=18, border_width=1, border_color=BORDER)
        source_card.pack(fill="x", pady=(14, 0))
        self.startup_notice_title = ctk.CTkLabel(source_card, text=self.t("hero_notice_title"), text_color=FG_PRIMARY, font=ui_font(14, "bold"))
        self.startup_notice_title.pack(anchor="w", padx=14, pady=(12, 4))
        self.startup_notice_label = ctk.CTkLabel(source_card, text=PERSISTENT_NOTICE_TEXT, text_color=FG_SECONDARY, font=ui_font(12), wraplength=680, justify="left")
        self.startup_notice_label.pack(anchor="w", padx=14, pady=(0, 12))
        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.pack(fill="x", pady=(20, 0))
        self.startup_accept_button = ctk.CTkButton(actions, text=self.t("btn_accept"), width=220, height=48, fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=FG_LIGHT, corner_radius=16, font=ui_font(15, "bold"), command=self._accept_startup_gate)
        self.startup_accept_button.pack(side="left", padx=(0, 12))
        self.startup_exit_button = ctk.CTkButton(actions, text=self.t("btn_exit"), width=160, height=48, fg_color=GHOST, hover_color=GHOST_HOVER, text_color=FG_PRIMARY, corner_radius=16, font=ui_font(15), command=self._exit_from_startup_gate)
        self.startup_exit_button.pack(side="left")

    def _render_accounts(self, account_items):
        for widget in self.account_rows:
            widget.destroy()
        self.account_rows.clear()
        if not account_items:
            empty = ctk.CTkFrame(self.accounts_list, fg_color=BG_SOFT, corner_radius=16, border_width=1, border_color=BORDER)
            empty.pack(fill="x")
            label = ctk.CTkLabel(empty, text=self.t("accounts_empty"), text_color=FG_SECONDARY, font=ui_font(13), justify="left")
            label.pack(anchor="w", padx=16, pady=16)
            self.account_rows.append(empty)
            self.accounts_title_label.configure(text=self.t("accounts_title"))
            return
        self.accounts_title_label.configure(text=f"{self.t('accounts_title')} ({len(account_items)})")
        for item in account_items:
            row = ctk.CTkFrame(self.accounts_list, fg_color=BG_SOFT, corner_radius=16, border_width=1, border_color=BORDER)
            row.pack(fill="x", pady=(0, 8))
            title = item.get("display_name") or self.t("accounts_unknown")
            subtitle = make_account_subtitle(item, self.language)
            ctk.CTkLabel(row, text=title, text_color=FG_PRIMARY, font=ui_font(14, "bold"), anchor="w").pack(anchor="w", padx=16, pady=(12, 2))
            ctk.CTkLabel(row, text=subtitle, text_color=FG_SECONDARY, font=ui_font(12), anchor="w", justify="left").pack(anchor="w", padx=16, pady=(0, 12))
            self.account_rows.append(row)

    def _refresh_runtime_state(self):
        self.runtime_var.set(self.t("running") if is_trae_running() else self.t("safe"))

    def _load_logo_later(self):
        if self.logo_image_small:
            return
        self.logo_path = discover_logo_path()
        image = load_logo_image(self.logo_path, (24, 24))
        if image:
            self.logo_image_small = image
            self.topbar_logo_label.configure(image=self.logo_image_small)
            self.topbar_logo_label.pack(side="left", padx=(0, 10), before=self.title_label)

    def _build_hero_detail(self, status):
        level = status.get("summary_level", "missing")
        if level == "blocked":
            return self.t("hero_detail_blocked")
        if level == "attention":
            return self.t(
                "hero_detail_attention",
                account_count=status["account_count"],
                storage_count=status["storage_key_count"],
                cache_count=status["session_path_count"],
            )
        if level == "ready":
            return self.t("hero_detail_ready")
        return self.t("hero_detail_missing")

    def _start_initial_load(self):
        def worker():
            runtime_running = is_trae_running()
            payload = {
                "runtime_running": runtime_running,
                "default_exists": DATA_DIR_DEFAULT.is_dir(),
                "default_dir": str(DATA_DIR_DEFAULT),
            }
            if payload["default_exists"]:
                payload["status"] = get_status(DATA_DIR_DEFAULT, runtime_running=runtime_running)
            self.after(0, lambda: self._finish_initial_load(payload))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_initial_load(self, payload):
        self._initial_loading = False
        if payload["default_exists"]:
            self.current_dir = DATA_DIR_DEFAULT
            self._set_textbox_value(self.dir_text, payload["default_dir"])
            self._set_summary(self.t("summary_loaded"))
            self._log(f"Detected default directory: {payload['default_dir']}" if self.language == "en-US" else f"检测到默认目录: {payload['default_dir']}", "ok")
            self._update_status_panel(payload["status"])
        else:
            self._set_status_badge(self.t("status_missing"), DANGER)
            self.runtime_var.set(self.t("missing_default_dir"))
            self.hero_summary.configure(text=self.t("status_missing"))
            self.hero_detail.configure(text=self.t("hero_detail_missing"))
            self._set_summary(self.t("summary_missing"))
            self._log(self.t("missing_default_dir"), "warn")
        self._set_btns(not self._startup_locked)

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
        self._set_btns(not self._initial_loading)
        self._set_summary(self.t("summary_disclaimer"))
        self._log(self.t("summary_disclaimer"), "info")

    def _exit_from_startup_gate(self):
        self.destroy()
        sys.exit(0)

    def _show_disclaimer(self):
        DisclaimerDialog(self, STRINGS, self.language)

    def _toggle_language(self):
        self.language = "en-US" if self.language == "zh-CN" else "zh-CN"
        save_language(self.language)
        self._apply_language()
        if self.last_status:
            self._update_status_panel(self.last_status)

    def _apply_language(self):
        self.subtitle_label.configure(text=self.t("app_subtitle"))
        self.version_title_label.configure(text=self.t("version_status"))
        self.version_label.configure(text=self.t("version_label", version=VERSION))
        self.lang_button.configure(text=self.t("language_toggle"))
        self.disclaimer_button.configure(text=self.t("top_disclaimer"))
        self.about_button.configure(text=self.t("top_about"))
        self.hero_title.configure(text=self.t("hero_title"))
        self.accounts_title_label.configure(text=self.t("accounts_title"))
        self.accounts_subtitle_label.configure(text=self.t("accounts_subtitle"))
        self.status_title_label.configure(text=self.t("status_title"))
        self.status_subtitle_label.configure(text=self.t("status_subtitle"))
        self.folder_title_label.configure(text=self.t("folder_title"))
        self.folder_subtitle_label.configure(text=self.t("folder_subtitle"))
        self.folder_current_label.configure(text=self.t("folder_current"))
        self.choose_button.configure(text=self.t("btn_choose"))
        self.restore_button_small.configure(text=self.t("btn_restore"))
        self.action_title_label.configure(text=self.t("action_title"))
        self.action_subtitle_label.configure(text=self.t("action_subtitle"))
        self.primary_button.configure(text=self.t("btn_oneclick"))
        self.refresh_button.configure(text=self.t("btn_refresh"))
        self.restore_button.configure(text=self.t("btn_restore"))
        self.advanced_clear_button.configure(text=self.t("btn_clear_accounts"))
        self.advanced_cache_button.configure(text=self.t("btn_clean_cache"))
        self.advanced_reset_button.configure(text=self.t("btn_reset_device"))
        self.health_title_label.configure(text=self.t("health_title"))
        self.quick_note_label.configure(wraplength=420)
        self.health_summary_label.configure(text=PERSISTENT_NOTICE_TEXT)
        self.log_title_label.configure(text=self.t("log_title"))
        self.startup_title_label.configure(text=self.t("startup_title"))
        self.startup_subtitle_label.configure(text=self.t("startup_subtitle"))
        self.startup_body_label.configure(text=self.t("startup_body"))
        self.startup_accept_button.configure(text=self.t("btn_accept"))
        self.startup_exit_button.configure(text=self.t("btn_exit"))
        self.startup_notice_title.configure(text=self.t("hero_notice_title"))
        self.startup_textbox.configure(state="normal")
        self.startup_textbox.delete("1.0", "end")
        self.startup_textbox.insert("1.0", self.disclaimer_text())
        self.startup_textbox.configure(state="disabled")
        self._set_update_buttons(self.update_button.cget("state") == "normal")
        self._refresh_update_status_text()
        self._sync_advanced_toggle_text()
        field_map = {
            "mid": self.t("field_machine"),
            "tmid": self.t("field_telemetry"),
            "did": self.t("field_device"),
            "sqm": self.t("field_sqm"),
            "storage": self.t("field_storage"),
            "cache": self.t("field_cache"),
            "risk": self.t("field_risk"),
        }
        for key, label in field_map.items():
            self.status_field_labels[key].configure(text=label)
        if hasattr(self, "admin_hint_label"):
            self.admin_hint_label.configure(text=self.t("admin_hint"))
            self.admin_restart_button.configure(text=self.t("admin_restart"))
        for label, item in self.tip_labels:
            label.configure(text=item[self.language])
        if not self.current_dir:
            self._set_textbox_value(self.dir_text, self.t("folder_missing"))

    def _sync_advanced_toggle_text(self):
        self.advanced_toggle.configure(text=self.t("advanced_collapse") if self._advanced_visible else self.t("advanced_expand"))

    def _toggle_advanced(self):
        self._advanced_visible = not self._advanced_visible
        self._sync_advanced_toggle_text()
        if self._advanced_visible:
            self.advanced_panel.pack(fill="x", pady=(10, 0))
        else:
            self.advanced_panel.pack_forget()

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
        self.last_status = dict(status)
        account_count = status["account_count"]
        detail_text = self._build_hero_detail(status)
        self._render_accounts(status["account_items"])
        self._set_textbox_value(self.info_values["mid"], status["machine_id"])
        self._set_textbox_value(self.info_values["tmid"], status["telemetry_machine_id"])
        self._set_textbox_value(self.info_values["did"], status["dev_device_id"])
        self._set_textbox_value(self.info_values["sqm"], status["sqm_id"])
        self.info_values["storage"].configure(text=str(status["storage_key_count"]))
        self.info_values["cache"].configure(text=str(status["session_path_count"]))
        self._set_textbox_value(self.info_values["risk"], detail_text)
        self.runtime_var.set(self.t("running") if status.get("runtime_running") else self.t("safe"))
        if status["summary_level"] == "blocked":
            self.hero_summary.configure(text=self.t("running"))
            self.hero_detail.configure(text=detail_text)
            self._set_status_badge(self.t("running"), DANGER)
        elif status["summary_level"] == "attention":
            self.hero_summary.configure(text=self.t("status_dirty"))
            self.hero_detail.configure(text=detail_text)
            self._set_status_badge(self.t("status_dirty"), WARN)
        elif status["summary_level"] == "ready":
            self.hero_summary.configure(text=self.t("status_clean"))
            self.hero_detail.configure(text=detail_text)
            self._set_status_badge(self.t("status_clean"), SUCCESS)
        else:
            self.hero_summary.configure(text=self.t("status_missing"))
            self.hero_detail.configure(text=detail_text)
            self._set_status_badge(self.t("status_missing"), DANGER)

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
            messagebox.showwarning(self.t("dir_invalid"), self.t("select_dir_first"))
            return False
        if is_trae_running():
            hint = "Right-click the Trae taskbar icon or end the Trae process in Task Manager." if self.language == "en-US" else "右键任务栏 Trae 图标退出，或在任务管理器结束 Trae 进程。"
            messagebox.showwarning(self.t("close_trae_title"), self.t("close_trae_msg", hint=hint))
            return False
        return True

    def _do_refresh(self, silent=False):
        if not self.current_dir:
            if not silent:
                self._log(self.t("select_dir_first"), "warn")
            return
        status = get_status(self.current_dir)
        self._update_status_panel(status)
        if not silent:
            self._set_summary(self.t("summary_refreshed"))
            self._log(self.t("summary_refreshed"), "info")

    def _on_browse(self):
        title = "Select Trae data directory" if self.language == "en-US" else "选择 Trae 数据目录"
        selected = filedialog.askdirectory(title=title)
        if not selected:
            return
        if not is_valid_trae_dir(selected):
            messagebox.showwarning(self.t("dir_invalid"), self.t("dir_invalid_msg", hint=DIR_HINT))
            return
        self.current_dir = selected
        self._set_textbox_value(self.dir_text, selected)
        self._set_summary(self.t("summary_switched"))
        self._log(f"Directory switched: {selected}" if self.language == "en-US" else f"已切换目录: {selected}", "info")
        self._do_refresh(silent=True)

    def _on_refresh(self):
        self._do_refresh()

    def _set_update_buttons(self, enabled, checking=False):
        state = "normal" if enabled else "disabled"
        top_text = self.t("top_check_update") if enabled or not checking else self.t("update_checking")
        self.update_button.configure(state=state, text=top_text)

    def _set_update_status(self, key, **kwargs):
        self.update_status_key = key
        self.update_status_kwargs = kwargs
        self.update_status_var.set(self.t(key, **kwargs))

    def _refresh_update_status_text(self):
        self.update_status_var.set(self.t(self.update_status_key, **self.update_status_kwargs))

    def _check_updates(self):
        self._set_summary(self.t("summary_checking_update"))
        self._set_update_status("update_status_checking")
        self._log(self.t("summary_checking_update"), "info")
        self._set_update_buttons(False, checking=True)

        def worker():
            result = check_for_updates()
            self.after(0, lambda: self._handle_update_result(result))

        threading.Thread(target=worker, daemon=True).start()

    def _handle_update_result(self, result):
        self._set_update_buttons(True)
        if not result["ok"]:
            self._set_summary(self.t("summary_update_failed"))
            self._set_update_status("update_status_failed", error=result["error"])
            self._log(self.t("update_failed_msg", error=result["error"]), "err")
            messagebox.showwarning(self.t("update_failed_title"), self.t("update_failed_msg", error=result["error"]))
            return
        if not result["has_update"]:
            self._set_summary(self.t("summary_update_latest"))
            self._set_update_status("update_status_latest")
            self._log(self.t("update_latest_msg", current=result["current_version"]), "info")
            messagebox.showinfo(self.t("update_latest_title"), self.t("update_latest_msg", current=result["current_version"]))
            return
        self._set_summary(self.t("summary_update_available"))
        self._set_update_status("update_status_available", latest=result["latest_version"])
        self._log(self.t("update_available_msg", current=result["current_version"], latest=result["latest_version"]), "ok")
        if messagebox.askyesno(self.t("update_available_title"), self.t("update_available_msg", current=result["current_version"], latest=result["latest_version"])):
            webbrowser.open(result["release_url"])

    def _on_content_configure(self, event):
        self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.content_canvas.itemconfigure(self.content_window, width=event.width)

    def _on_mousewheel(self, event):
        if not hasattr(self, "content_canvas"):
            return
        if getattr(event, "num", None) == 4:
            delta = -1
        elif getattr(event, "num", None) == 5:
            delta = 1
        else:
            delta = int(-event.delta / 120) if getattr(event, "delta", 0) else 0
        if delta:
            self.content_canvas.yview_scroll(delta, "units")

    def _run_action(self, action_name, func, running_text, done_text, confirm_title, confirm_message):
        if not self._check():
            return
        if not messagebox.askyesno(confirm_title, confirm_message):
            return
        self._set_btns(False)
        self._set_summary(running_text)
        self._log(action_name, "info")
        self._log(self.t("backup_auto_log"), "dim")
        try:
            func()
            self._set_summary(done_text)
        except PermissionError:
            self._log("Permission denied" if self.language == "en-US" else "权限不足，部分文件可能被占用或需要更高权限", "err")
        except Exception as exc:
            self._log(f"Error: {exc}", "err")
        finally:
            self._set_btns(True)
            self._do_refresh(silent=True)

    def _on_clear(self):
        def action():
            logs, removed = clear_accounts(self.current_dir)
            for line in logs:
                self._log(line)
            self._log("Account state cleared" if self.language == "en-US" else ("账号状态清理完成" if removed else "未发现可清理的账号状态"), "ok" if removed else "warn")
        self._run_action(self.t("btn_clear_accounts"), action, self.t("btn_clear_accounts"), self.t("btn_clear_accounts"), self.t("confirm_clear_title"), self.t("confirm_clear_msg"))

    def _on_clean_cache(self):
        def action():
            logs, removed = deep_clean_local_state(self.current_dir)
            for line in logs:
                self._log(line)
            self._log("Cache targets cleaned" if self.language == "en-US" else ("缓存目录清理完成" if removed else "未发现需要清理的缓存目录"), "ok" if removed else "warn")
        self._run_action(self.t("btn_clean_cache"), action, self.t("btn_clean_cache"), self.t("btn_clean_cache"), self.t("confirm_cache_title"), self.t("confirm_cache_msg"))

    def _on_reset(self):
        def action():
            logs, ids = reset_device_id(self.current_dir)
            for line in logs:
                self._log(line)
            verification = verify_write(self.current_dir, ids)
            for detail in verification["details"]:
                self._log(detail, "ok" if verification["ok"] else "warn")
            self._log(verification["summary"], "ok" if verification["ok"] else "warn")
        self._run_action(self.t("btn_reset_device"), action, self.t("btn_reset_device"), self.t("btn_reset_device"), self.t("confirm_reset_title"), self.t("confirm_reset_msg"))

    def _on_oneclick(self):
        def action():
            clear_logs, _ = clear_accounts(self.current_dir)
            for line in clear_logs:
                self._log(line)
            cache_logs, _ = deep_clean_local_state(self.current_dir)
            for line in cache_logs:
                self._log(line)
            reset_logs, ids = reset_device_id(self.current_dir)
            for line in reset_logs:
                self._log(line)
            verification = verify_write(self.current_dir, ids)
            for detail in verification["details"]:
                self._log(detail, "ok" if verification["ok"] else "warn")
            self._log(verification["summary"], "ok" if verification["ok"] else "warn")
        self._run_action(self.t("btn_oneclick"), action, self.t("summary_oneclick_running"), self.t("summary_oneclick_done"), self.t("confirm_oneclick_title"), self.t("confirm_oneclick_msg"))

    def _on_restore(self):
        if not self.current_dir:
            messagebox.showwarning(self.t("dir_invalid"), self.t("select_dir_first"))
            return
        if is_trae_running():
            messagebox.showwarning(self.t("close_trae_title"), self.t("close_trae_restore"))
            return
        if not messagebox.askyesno(self.t("confirm_restore_title"), self.t("confirm_restore_msg")):
            return
        self._set_btns(False)
        self._set_summary(self.t("summary_restore_running"))
        try:
            logs, count = restore_backup(self.current_dir)
            for line in logs:
                self._log(line)
            self._set_summary(self.t("summary_restore_done") if count else self.t("summary_restore_missing"))
            self._log("Backup restored" if self.language == "en-US" else ("备份恢复完成" if count else "未找到可恢复的备份"), "ok" if count else "warn")
        except Exception as exc:
            self._log(f"Restore failed: {exc}", "err")
        finally:
            self._set_btns(True)
            self._do_refresh(silent=True)

    def _restart_admin(self):
        if restart_as_admin():
            self.destroy()
            sys.exit(0)
        messagebox.showerror("Error" if self.language == "en-US" else "失败", "Unable to restart as administrator" if self.language == "en-US" else "无法以管理员身份重启")

    def _on_about(self):
        messagebox.showinfo(self.t("about_title"), self.t("about_body", app_title=APP_TITLE, brand=BRAND_NAME, url=PROJECT_GITHUB_URL, anti_resale=ANTI_RESALE_NOTICE, refund=REFUND_NOTICE))
