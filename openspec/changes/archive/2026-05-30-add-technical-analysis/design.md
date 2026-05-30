## Context

yfinance 已是現有依賴（`app.py` 第 2 行）。技術指標計算（RSI、MACD）使用 pandas rolling/ewm 即可實現，不需 ta-lib。前端已有 Chart.js（cdn 已載入），可直接繪製均線疊加圖。

## Goals / Non-Goals

**Goals:**
- `/api/technical/<ticker>` 回傳：`ma20/ma50/ma200`（最新值）、`rsi`（14日，最新值）、`macd`（MACD 線、Signal 線、Histogram 最新值）、`price_with_ma`（90天日線 + 三均線，供 Chart.js 用）、`signal_summary`（總分 0–100、建議文字）
- 技術面卡片在主報告渲染後非同步載入（不阻塞主分析）
- 手機板 responsive 顯示

**Non-Goals:**
- 不做 K 線圖（蠟燭圖），只做折線疊加圖
- 不做即時 tick 更新，只在報告生成後取一次
- 不做回測功能（algo-trading skill 的核心，但引入複雜度太高）

## Decisions

### D1: 技術指標純 Python 手算
RSI = 14 日相對強弱指數（用 pandas ewm 計算平均漲跌幅）  
MACD = EMA12 - EMA26，Signal = 9日 EMA of MACD  
MA = 簡單移動平均（rolling mean）  
**理由**：避免引入 ta-lib（需編譯）或 pandas-ta 新依賴。

### D2: 技術信號評分邏輯
| 條件 | 加分 |
|------|------|
| 價格 > MA200 | +25 |
| MA50 > MA200（黃金交叉）| +20 |
| 價格 > MA50 | +15 |
| RSI 40–70（健康區間）| +20 |
| MACD > Signal | +20 |

總分 0–100，對應建議：80+ 強多、60–79 偏多、40–59 中性、20–39 偏空、0–19 強空。

### D3: 前端非同步載入
`renderReport()` 完成後，JS 呼叫 `fetchTechnicalAnalysis(ticker)`，結果回傳後再渲染 Section 8，避免技術分析 API 失敗影響主報告。

## Risks / Trade-offs

- [風險] yfinance 日線數據可能需要額外請求（rate limit）→ 路由獨立，可接受延遲
- [取捨] 手算指標與專業工具可能有小數差異 → 對散戶參考足夠，不做專業交易用途
