<div align="center">

# TraeReset

**Trae IDE 本地状态深度重置工具**

解决 Trae IDE 提示「设备数量已达上限」或旧版本地重置方案失效的问题

[![Release](https://img.shields.io/github/v/release/Ylsssq926/TraeReset?style=flat-square)](https://github.com/Ylsssq926/TraeReset/releases)
[![License](https://img.shields.io/github/license/Ylsssq926/TraeReset?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue?style=flat-square)]()

[下载 Windows 版](https://github.com/Ylsssq926/TraeReset/releases/latest)

> **开源作者：掠蓝**  
> GitHub：<https://github.com/Ylsssq926/TraeReset>  
> **如果你是通过付费购买获得本工具，请立即退款。请勿二次倒卖。**

</div>

---

## 这是什么

Trae IDE 会在本地保存设备标识、账号状态、 Cookie 和缓存目录。当你频繁切换账号，或者客户端开始依赖更多本地状态时，单纯修改 `machineid` 的旧方案通常已经不够用。

TraeReset 当前版本会执行一套更完整的本地状态重置流程：

1. 清理账号与权益残留键
2. 清理 Cookie、缓存目录和本地数据库
3. 生成全新的设备 ID 并写回
4. 对关键写入结果做验证

**本工具不修改 Trae 软件本体，仅操作本地用户数据文件。**

## 全新升级

当前版本属于一次完整升级，重点修了这些问题：

- 修复首次打开窗口时的布局抖动
- 修复长路径、长设备 ID 和中文说明容易被截断的问题
- 将 UI 重新调整为蓝、淡绿、白主色调，整体更干净轻盈
- 恢复并强化免责声明流程，首次启动必须确认，主界面也可随时再次查看
- 将代码拆成入口、核心逻辑、UI 三层，便于后续维护和继续扩展

## 原理

当前版本主要覆盖以下本地状态：

| 类别 | 目标 |
|------|------|
| 设备标识 | `machineid` |
| 遥测标识 | `storage.json` 中的 `telemetry.machineId` / `telemetry.devDeviceId` / `telemetry.sqmId` |
| 账号状态 | `storage.json` 中的 `iCubeAuthInfo://` / `iCubeServerData://` / `iCubeEntitlementInfo://` 等键 |
| 本地数据库 | `User/globalStorage/state.vscdb` / `state.vscdb.backup` |
| 浏览器状态 | `Local State` / `Local Storage` / `Session Storage` / `IndexedDB` |
| Cookie | `Network/Cookies` 及常见分区 Cookie 文件 |
| 缓存目录 | `Code Cache` / `GPUCache` / `DawnCache` 等 |

## 项目结构

- `trae_unlock.py`：最薄启动入口
- `traereset_core.py`：扫描、清理、备份、恢复、验证逻辑
- `traereset_ui.py`：窗口、布局、事件和界面状态管理

## 快速开始

### Windows

1. 前往 [Releases](https://github.com/Ylsssq926/TraeReset/releases/latest) 下载 `TraeReset.exe`
2. 完全关闭 Trae
3. 双击运行 `TraeReset.exe`
4. 首次启动先确认免责声明
5. 点击「一键深度重置」
6. 重启 Trae 后重新登录

### macOS

当前提供两种分发方式：

1. `TraeReset_macOS.tar.gz`
   解压后双击 `TraeReset_macOS.command`，脚本会自动安装依赖并启动
2. `.app` 打包方案
   仓库中已提供 `TraeReset_macOS.spec`，可在 macOS 环境下用 `PyInstaller` 生成原生 `.app`

手动运行方式：

```bash
pip3 install -r requirements.txt
python3 trae_unlock.py
```

### 从源码运行

```bash
git clone https://github.com/Ylsssq926/TraeReset.git
cd TraeReset
pip install -r requirements.txt
python trae_unlock.py
```

## 功能

- **一键深度重置**：清理账号状态、缓存目录并重置设备标识
- **清理账号状态**：删除 `storage.json` 中的账号/权益残留键并清理 Cookie
- **清缓存目录**：清理本地数据库、浏览器状态和常见缓存目录
- **重置设备标识**：生成新的 Machine ID / Device ID / SQM ID
- **增强验证**：验证关键字段是否写入完成，并检查残留缓存目标
- **自动备份**：修改前自动生成 `.bak` 备份，可恢复最近一次状态
- **免责声明入口**：首次启动强制确认，主界面顶部可再次查看
- **现代化 UI**：蓝、淡绿、白配色，路径和长文本统一改为更稳定的展示组件

## 数据目录

| 平台 | 路径 |
|------|------|
| Windows | `%APPDATA%\Trae` |
| macOS | `~/Library/Application Support/Trae` |
| Linux | `~/.config/Trae` |

## 打包

### Windows EXE

```bash
pyinstaller TraeReset.spec
```

### macOS `.app`

```bash
pyinstaller TraeReset_macOS.spec
```

### 通用依赖

```bash
pip install -r requirements.txt
```

## 常见问题

**Q: 为什么旧版只改 `machineid` 的方案最近不稳定？**  
A: 新版客户端往往会同时使用 `storage.json`、本地数据库、Cookie、缓存目录等状态进行关联识别。TraeReset 现在会把这些本地状态一起清理和重置。

**Q: 为什么之前界面有时文字显示不完整？**  
A: 中文字体在不同平台的实际宽度会比估算更大，普通单行标签很容易截断。当前版本已把长路径、长 ID 和长说明改成可换行或只读文本框展示。

**Q: 为什么窗口刚打开时会跳动？**  
A: 旧版在窗口显示后才继续切换页面和刷新内容。现在会先构建界面、完成首轮装载，再显示窗口，避免明显抖动。

**Q: 工具检测不到 Trae 目录？**  
A: 点击「选择目录」手动定位 Trae 数据目录，常见路径见上表。

**Q: 能恢复到重置前的状态吗？**  
A: 可以。点击「恢复备份」后会从最近一次生成的 `.bak` 备份恢复对应文件或目录。

## 免责声明

1. 本工具仅供个人学习与技术研究使用，请勿用于商业或非法用途
2. 使用本工具产生的一切后果由使用者自行承担，与作者无关
3. 本工具不修改 Trae 软件本体，仅操作本地用户数据文件
4. 开源作者：掠蓝
5. GitHub：<https://github.com/Ylsssq926/TraeReset>
6. 如果你是通过付费购买获得本工具，请立即退款
7. 请勿将本项目二次倒卖或去除来源后重新分发
8. 如侵犯相关权利，请联系作者删除

## 关于

协议：[MIT](LICENSE)
