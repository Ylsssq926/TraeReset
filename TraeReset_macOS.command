#!/bin/bash
# TraeReset macOS launcher
# Double-click to run and install dependencies if needed

cd "$(dirname "$0")"

echo "================================"
echo "  TraeReset - Trae local deep reset tool"
echo "  TraeReset - Trae 本地状态深度重置工具"
echo "  Open-source author / 开源作者: 掠蓝"
echo "  GitHub: https://github.com/Ylsssq926/TraeReset"
echo "  If you paid for this tool, request a refund immediately."
echo "  若你是付费购买获得，请立即退款，勿二次倒卖"
echo "================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[Error] Python3 was not found. Install it first:"
    echo "  brew install python3"
    echo "  or download it from https://www.python.org/downloads/"
    echo ""
    echo "[错误] 未找到 Python3，请先安装："
    echo "  brew install python3"
    echo "  或从 https://www.python.org/downloads/ 下载"
    echo ""
    echo "Press Enter to exit... / 按回车键退出..."
    read
    exit 1
fi

PY=$(command -v python3)
echo "[Info] Python: $PY ($(python3 --version 2>&1))"

if ! python3 -c "import customtkinter; import PIL; import certifi" 2>/dev/null; then
    echo "[Info] Installing runtime dependencies..."
    echo "[信息] 正在安装运行依赖..."
    python3 -m pip install customtkinter pillow certifi --quiet
    if [ $? -ne 0 ]; then
        echo "[Error] Failed to install runtime dependencies. Run manually:"
        echo "  pip3 install customtkinter pillow certifi"
        echo ""
        echo "[错误] 安装运行依赖失败，请手动执行："
        echo "  pip3 install customtkinter pillow certifi"
        echo ""
        echo "Press Enter to exit... / 按回车键退出..."
        read
        exit 1
    fi
    echo "[Info] Runtime dependencies installed"
    echo "[信息] 运行依赖安装完成"
fi

echo "[Info] Launching TraeReset..."
echo "[信息] 正在启动 TraeReset..."
echo ""
python3 trae_unlock.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[Error] Application exited unexpectedly"
    echo "[错误] 程序异常退出"
    echo "Press Enter to exit... / 按回车键退出..."
    read
fi
