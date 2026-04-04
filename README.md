# TraeReset

中文 | [English](#english)

## 中文

**Trae IDE 本地状态深度重置工具**

TraeReset 用于清理 Trae 在本地保存的账号状态、缓存目录和设备标识，适合在旧版只改 `machineid` 的方案不再稳定时使用。

### 主要特点

- 一键深度重置，覆盖账号残留、缓存目录和设备标识
- 检测并展示当前识别到的账号，减少误清理风险
- 所有修改前自动生成 `.bak` 备份，并支持恢复最近一次自动备份
- 提供高级选项，用于分步执行局部操作
- 支持中英双语界面
- 支持检查更新

### 功能范围

当前版本主要覆盖以下本地状态：

- `machineid`
- `storage.json` 中的 `telemetry.machineId` / `telemetry.devDeviceId` / `telemetry.sqmId`
- `storage.json` 中的 `iCubeAuthInfo://` / `iCubeServerData://` / `iCubeEntitlementInfo://` 等键
- `User/globalStorage/state.vscdb` / `state.vscdb.backup`
- `Local State` / `Local Storage` / `Session Storage` / `IndexedDB`
- `Network/Cookies` 及常见分区 Cookie 文件
- `Code Cache` / `GPUCache` / `DawnCache` 等缓存目录

### 推荐使用流程

1. 先确认当前操作目录是否正确
2. 查看当前检测到的账号列表，避免误清理
3. 执行一键深度重置
4. 仅在需要时再使用高级选项

### 快速开始

#### Windows

1. 从 Releases 下载 `TraeReset.exe`
2. 完全关闭 Trae
3. 运行 `TraeReset.exe`
4. 首次启动先确认免责声明
5. 确认当前检测到的账号后，再执行一键深度重置

#### macOS

当前提供两种方式：

1. `TraeReset_macOS.tar.gz`
   解压后双击 `TraeReset_macOS.command`
2. `.app` 打包方案
   仓库中提供 `TraeReset_macOS.spec`，可在 macOS 环境下用 `PyInstaller` 生成原生 `.app`

### 从源码运行

```bash
pip install -r requirements.txt
python trae_unlock.py
```

### 项目结构

- `trae_unlock.py`：最薄启动入口
- `traereset_core.py`：扫描、清理、备份、恢复、验证、更新检查逻辑
- `traereset_ui.py`：窗口、双语文案、布局、事件和界面状态管理

### 免责声明

1. 本工具仅供个人学习与技术研究使用。
2. 本工具不修改 Trae 程序本体，仅处理本地用户数据。
3. 使用本工具产生的一切后果由使用者自行承担。
4. 开源作者：掠蓝
5. GitHub：<https://github.com/Ylsssq926/TraeReset>
6. 如果你是通过付费购买获得本工具，请立即退款，请勿二次倒卖。

---

## English

**Local deep reset tool for Trae IDE state**

TraeReset clears local Trae account traces, cache targets, and device identifiers when older reset methods based only on `machineid` are no longer reliable.

### Key features

- Deep reset as the primary one-click flow
- Detected account list to reduce accidental cleanup
- Automatic `.bak` backups before changes, plus restore for the latest auto backup
- Advanced options for step-by-step operations
- Built-in Chinese and English UI support
- Manual update checking

### Coverage

The current version targets these local artifacts:

- `machineid`
- `telemetry.machineId` / `telemetry.devDeviceId` / `telemetry.sqmId` inside `storage.json`
- `iCubeAuthInfo://` / `iCubeServerData://` / `iCubeEntitlementInfo://` keys inside `storage.json`
- `User/globalStorage/state.vscdb` / `state.vscdb.backup`
- `Local State` / `Local Storage` / `Session Storage` / `IndexedDB`
- `Network/Cookies` and common partition cookie files
- Cache folders such as `Code Cache`, `GPUCache`, and `DawnCache`

### Recommended flow

1. Confirm the working folder first
2. Review the detected account list to avoid clearing the wrong state
3. Run Deep Reset knowing a `.bak` backup is created before changes
4. Use Advanced Options or Restore Latest Auto Backup only when needed

### Quick start

#### Windows

1. Download `TraeReset.exe` from Releases
2. Fully quit Trae
3. Run `TraeReset.exe`
4. Accept the disclaimer on first launch
5. Review detected accounts, then run Deep Reset

#### macOS

Two distribution modes are available:

1. `TraeReset_macOS.tar.gz`
   Extract it and run `TraeReset_macOS.command`
2. Native `.app` build path
   `TraeReset_macOS.spec` is included for building a native `.app` on macOS with `PyInstaller`

### Run from source

```bash
pip install -r requirements.txt
python trae_unlock.py
```

### Project structure

- `trae_unlock.py`: thin launcher entry
- `traereset_core.py`: scan, cleanup, backup, restore, verification, and update-check logic
- `traereset_ui.py`: window layout, bilingual strings, events, and UI state management

### Disclaimer

1. This tool is for personal study and technical research only.
2. It does not modify the Trae application itself, only local user data.
3. You are responsible for any consequences of using it.
4. Open-source author: 掠蓝
5. GitHub: <https://github.com/Ylsssq926/TraeReset>
6. If you paid for this tool, request a refund immediately. Do not resell it.
nd immediately. Do not resell it.
