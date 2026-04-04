#!/bin/bash
# TraeReset macOS 启动脚本
# 双击即可运行，自动安装依赖

cd "$(dirname "$0")"

echo "================================"
echo "  TraeReset - Trae 本地状态深度重置工具"
echo "  开源作者: 掠蓝"
echo "  GitHub: https://github.com/Ylsssq926/TraeReset"
echo "  若你是付费购买获得，请立即退款，勿二次倒卖"
echo "================================"
echo ""

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装："
    echo "  brew install python3"
    echo "  或从 https://www.python.org/downloads/ 下载"
    echo ""
    echo "按回车键退出..."
    read
    exit 1
fi

PY=$(command -v python3)
echo "[信息] Python: $PY ($(python3 --version 2>&1))"

# 检查并安装依赖
if ! python3 -c "import customtkinter" 2>/dev/null; then
    echo "[信息] 正在安装依赖..."
    python3 -m pip install -r requirements.txt --quiet
    if [ $? -ne 0 ]; then
        echo "[错误] 安装依赖失败，请手动执行："
        echo "  pip3 install -r requirements.txt"
        echo ""
        echo "按回车键退出..."
        read
        exit 1
    fi
    echo "[信息] customtkinter 安装完成"
fi

echo "[信息] 启动 TraeReset..."
echo ""
python3 trae_unlock.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 程序异常退出"
    echo "按回车键退出..."
    read
fi
