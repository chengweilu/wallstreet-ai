#!/bin/bash
echo "🚀 啟動 WallStreet AI 股票分析系統..."
echo ""

cd "$(dirname "$0")"

# 安裝依賴（若尚未安裝）
pip3 install -r requirements.txt -q 2>/dev/null

# 啟動伺服器
echo "✅ 伺服器啟動中，請開啟瀏覽器訪問：http://localhost:5000"
echo "   按 Ctrl+C 停止"
echo ""
python3 app.py
