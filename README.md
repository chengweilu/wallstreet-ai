# WallStreet AI — 股票深度研究系統

<div align="center">

![WallStreet AI Banner](https://img.shields.io/badge/WallStreet%20AI-股票深度研究系統-d97706?style=for-the-badge&labelColor=1c1917)
&nbsp;
![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-5046e5?style=for-the-badge&logo=anthropic&logoColor=white)
&nbsp;
![Yahoo Finance](https://img.shields.io/badge/Data-Yahoo%20Finance-6001d2?style=for-the-badge)

**輸入任一美股或台股代碼，60 秒內生成機構級投資研究報告**

[快速開始](#快速開始) · [功能介紹](#功能介紹) · [技術架構](#技術架構) · [本地部署](#本地部署)

</div>

---

## ✨ 功能介紹

### 🏛️ 機構級報告 · 8 大分析維度

| 維度 | 內容 |
|------|------|
| 📊 **商業模式** | 核心營收結構、TAM 市場規模、5 年 CAGR 預測 |
| 🏰 **競爭護城河** | 雷達圖評分、品牌/轉換成本/專利壁壘分析 |
| 💰 **財務分析** | 近 5 年三率走勢、自由現金流、ROE 深度解析 |
| 📐 **估值分析** | DCF + P/E + EV/EBITDA 三法加權目標價 |
| ⚔️ **多空辯論** | 多頭催化劑 vs 空頭風險數據對決 |
| 🔭 **情境展望** | 牛市 / 基本 / 熊市 三情境機率與目標價 |
| 🎯 **投資策略** | 短期操作區間、長期展望、核心決策金句 |
| 📈 **技術面分析** | MA20/50/200、RSI、MACD 信號評分（0–100） |

### 🤖 AI 智慧沙盒
三大敏感度情境動態模擬，量化衝擊對財務與估值的影響

### 📋 歷史記錄
所有分析報告自動儲存，隨時回顧、重新載入

---

## 🚀 快速開始

### 1. 取得 Anthropic API Key

前往 [console.anthropic.com](https://console.anthropic.com) 建立帳號並取得 API Key

### 2. 安裝依賴

```bash
git clone https://github.com/chengweilu/wallstreet-ai.git
cd wallstreet-ai
pip3 install -r requirements.txt
```

### 3. 設定環境變數

```bash
cp .env.example .env
```

編輯 `.env`：

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxx   # 你的 Claude API Key
FLASK_PORT=5001                    # 可選，預設 5000
```

### 4. 啟動伺服器

```bash
python3 app.py
```

或使用啟動腳本：

```bash
./start.sh
```

### 5. 開啟網頁

```
http://localhost:5001
```

---

## 🖥️ 使用方式

### 分析股票

1. 在首頁輸入股票代碼（支援美股與台股）：

```
美股：AAPL  NVDA  TSLA  MSFT  GOOGL
台股：2330  2317  2454  0050
```

2. 點擊「開始深度分析」，等待約 30–60 秒

3. 完整的 8 維度機構級報告自動生成 ✅

### 技術面分析

報告生成後，系統自動抓取技術指標：

- **均線狀態**：MA20 / MA50 / MA200 多空排列
- **RSI 動能**：14 日相對強弱（超買 > 70 / 超賣 < 30）
- **MACD 趨勢**：黃金交叉 / 死亡交叉信號
- **信號總分**：0–100 分，對應強多 / 偏多 / 中性 / 偏空 / 強空

### 輸入格式說明

| 市場 | 格式 | 範例 |
|------|------|------|
| 美股 | 英文代碼 | `AAPL`、`NVDA`、`META` |
| 台股上市 | 4 位數字 | `2330`、`2317` |
| 台股 OTC | 數字 | `6505`、`3443` |

---

## 🏗️ 技術架構

```
wallstreet-ai/
├── app.py              # Flask 後端 + Yahoo Finance + Claude API
├── templates/
│   └── index.html      # 單頁前端（HTML + CSS + Chart.js）
├── history.db          # SQLite 分析歷史（自動建立，不進版控）
├── requirements.txt    # Python 依賴
└── .env                # 環境變數（不進版控）
```

### 技術棧

| 層級 | 技術 |
|------|------|
| **後端** | Python · Flask · yfinance |
| **AI 引擎** | Anthropic Claude (claude-opus-4-5) |
| **即時數據** | Yahoo Finance API |
| **前端** | 原生 HTML/CSS/JS · Chart.js |
| **資料庫** | SQLite（本地儲存） |
| **字型** | Noto Sans TC · Inter |

### 分析流程

```
用戶輸入代碼
    ↓
Yahoo Finance 取得即時數據
（股價、財報、毛利率、ROE、自由現金流…）
    ↓
計算數據完整度分數（0–100）
    ↓
三階段 Prompt 框架送入 Claude API
（數據驗證 → 魔鬼代言人 → 加權判斷）
    ↓
JSON 解析 + 數據驗證
    ↓
渲染完整報告 + 非同步載入技術面
    ↓
儲存至 SQLite 歷史記錄
```

---

## ⚙️ 環境變數

| 變數 | 必填 | 說明 |
|------|------|------|
| `ANTHROPIC_API_KEY` | ✅ | Claude API 金鑰 |
| `FLASK_PORT` | ❌ | 伺服器埠號（預設 5000） |

> **注意**：macOS 的 AirPlay Receiver 預設佔用 5000 埠，建議改用 `FLASK_PORT=5001`

---

## 📊 Report 欄位說明

| JSON 欄位 | 說明 |
|-----------|------|
| `confidence_score` | 分析信心（0–100），依 Yahoo Finance 數據完整度計算 |
| `overall_rating` | 整體評級：BUY / HOLD / AVOID |
| `target_price_12m` | 12 個月目標價 |
| `section4.weighted_target` | DCF + P/E + EV/EBITDA 三法加權目標價 |
| `section4.ev_ebitda_analysis` | EV/EBITDA 估值法分析 |

---

## 🗂️ 歷史記錄

所有分析報告自動儲存到本地 `history.db`（SQLite），可在首頁查看歷史記錄、點擊重新載入任一份報告。

---

## ⚠️ 免責聲明

本系統由 AI 生成分析報告，**僅供參考，不構成投資建議**。  
投資涉及風險，過往表現不代表未來結果。  
請在做出投資決策前諮詢專業財務顧問。

---

<div align="center">

Powered by **Claude AI** × **Yahoo Finance Real-Time Data**

Made with ❤️ by [Chengwei Lu](https://github.com/chengweilu)

</div>
