#!/bin/bash
# TraeReset macOS 启动脚本
# 双击即可运行，自动安装依赖

cd "$(dirname "$0")"

echo "================================"
echo "  TraeReset - Trae 设备限制重置工具"
echo "  制作人: 掠蓝 | 交流群: 676475076"
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

# 检查并安装 customtkinter
if ! python3 -c "import customtkinter" 2>/dev/null; then
    echo "[信息] 正在安装 customtkinter..."
    python3 -m pip install customtkinter --quiet
    if [ $? -ne 0 ]; then
        echo "[错误] 安装 customtkinter 失败，请手动执行："
        echo "  pip3 install customtkinter"
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
