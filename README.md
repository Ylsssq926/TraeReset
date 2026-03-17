<div align="center">

# TraeReset

**Trae IDE 设备限制重置工具**

解决 Trae IDE 提示「设备数量已达上限」无法登录的问题

[![Release](https://img.shields.io/github/v/release/Ylsssq926/TraeReset?style=flat-square)](https://github.com/Ylsssq926/TraeReset/releases)
[![License](https://img.shields.io/github/license/Ylsssq926/TraeReset?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue?style=flat-square)]()

[下载 Windows 版](https://github.com/Ylsssq926/TraeReset/releases/latest) · [交流群 676475076]()

</div>

---

## 这是什么

Trae IDE 会通过设备 ID 限制同一台机器上可登录的账号数量。当你切换账号过多时，会遇到「设备数量已达上限」的提示，导致无法登录新账号。

TraeReset 通过重置本地设备标识文件来解除这个限制，让 Trae 服务端将你的电脑识别为一台新设备。

**本工具不修改 Trae 软件本体，仅操作本地用户数据文件。**

## 原理

Trae 在本地存储了以下设备标识：

| 文件 | 内容 | 作用 |
|------|------|------|
| `machineid` | UUID | 机器唯一标识 |
| `storage.json` → `telemetry.machineId` | 64位十六进制 | 遥测机器 ID |
| `storage.json` → `telemetry.devDeviceId` | UUID | 开发设备 ID |
| `storage.json` → `telemetry.sqmId` | GUID | SQM 标识 |

TraeReset 的工作流程：
1. 清除登录凭证（Token、Cookies）
2. 生成全新的设备 ID 写入上述文件
3. 验证文件是否写入成功

## 快速开始

### Windows

直接下载运行，无需安装任何环境：

1. 前往 [Releases](https://github.com/Ylsssq926/TraeReset/releases/latest) 下载 `TraeReset.exe`
2. 关闭 Trae
3. 双击运行 `TraeReset.exe`
4. 点击「一键重置」
5. 重新打开 Trae，登录新账号

### macOS

```bash
# 安装依赖
pip3 install customtkinter

# 运行
python3 trae_unlock.py
```

### 从源码运行（所有平台）

```bash
git clone https://github.com/Ylsssq926/TraeReset.git
cd TraeReset
pip install -r requirements.txt
python trae_unlock.py
```

## 功能

- **一键重置** — 清除账号 + 重置设备 ID，一步到位
- **清除账号** — 删除 Token、Cookies 等登录信息
- **重置设备 ID** — 生成全新的 Machine ID / Device ID
- **写入验证** — 操作后自动读回文件验证是否真的改了
- **自动备份** — 修改前自动备份原文件（.bak），支持一键恢复
- **免责声明记忆** — 同意一次后不再重复弹出

## 数据目录

| 平台 | 路径 |
|------|------|
| Windows | `%APPDATA%\Trae` |
| macOS | `~/Library/Application Support/Trae` |
| Linux | `~/.config/Trae` |

## 自行打包

```bash
pip install pyinstaller customtkinter
pyinstaller --onefile --windowed --name TraeReset --hidden-import customtkinter trae_unlock.py
```

打包产物在 `dist/TraeReset.exe`。

## 常见问题

**Q: 提示权限不足怎么办？**
A: 操作卡片底部有「以管理员身份重启」按钮，点击即可。通常不需要管理员权限。

**Q: 工具检测不到 Trae 目录？**
A: 点击「选择目录」手动选择 Trae 的数据目录，路径见上方表格。

**Q: 重置后还是提示设备上限？**
A: 确保操作前已完全关闭 Trae（包括托盘图标），然后重新执行一键重置。

**Q: 能恢复到重置前的状态吗？**
A: 可以，点击「恢复备份」即可从 .bak 文件恢复。仅保留最近一次备份。

## 免责声明

1. 本工具仅供个人学习与技术研究使用，请勿用于商业或非法用途
2. 使用本工具产生的一切后果由使用者自行承担，与作者无关
3. 本工具不修改 Trae 软件本体，仅操作本地用户数据文件
4. 如侵犯相关权利，请联系作者删除

## 关于

制作人：掠蓝
交流群：676475076
协议：[MIT](LICENSE)
