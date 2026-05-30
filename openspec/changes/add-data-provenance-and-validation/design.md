## Context

`get_stock_data()` 回傳的 dict 已有 `_data_quality: 'full'|'limited'`，但這個資訊沒有被傳遞到前端。`build_annual_data_template()` 在 `fin` 為空時靜默使用硬編碼範例數字（2020–2024 固定值），前端毫無提示。`analyze()` route 將 Claude 回傳的 JSON 直接 forward，沒有任何欄位層級的來源標記。

## Goals / Non-Goals

**Goals:**
- API 回傳新增 `data_sources: dict` 與 `data_warnings: list`，前端無需猜測
- 五個關鍵欄位加來源標示：`current_price`、`annual_data`（財務表）、`target_price_12m`、`overall_rating`、`moat_score`
- 驗證：股價 <= 0、財務數據全為 0、`_data_quality == 'limited'` 三種異常轉為 warning
- 底部資料品質摘要卡片：一眼看出「真實數據 vs AI 估算」比例

**Non-Goals:**
- 對每個 JSON 欄位（數十個）都加來源標示（過度工程）
- 後端重新抓取或修正 AI 估算值
- 歷史記錄頁面的來源顯示（僅限即時報告）

## Decisions

**`data_sources` 結構**
```json
{
  "current_price": "yahoo_finance",
  "annual_data":   "yahoo_finance",   // 或 "example_fallback"
  "cashflows":     "yahoo_finance",
  "target_price_12m": "claude_ai",
  "overall_rating":   "claude_ai",
  "moat_score":       "claude_ai"
}
```
- `yahoo_finance`：來自 yfinance 真實抓取
- `claude_ai`：Claude 生成或估算
- `example_fallback`：yfinance 失敗，後端使用硬編碼範例

**`data_warnings` 結構**
```json
[
  {"field": "current_price", "message": "股價為 0 或無效，請確認股票代碼"},
  {"field": "annual_data",   "message": "財務數據使用範例預設值，非真實市場數據"}
]
```

**前端徽章策略**
- `yahoo_finance` → 綠色小字 `YF`（可信，低調顯示）
- `claude_ai` → 藍色小字 `AI`（AI 估算，中立）
- `example_fallback` → 橘色 `⚠ 範例數據`（需引起注意）
- 警告欄位旁加 `⚠` icon，hover 顯示警告訊息

**資料品質摘要卡位置**
置於報告 `#section7`（投資策略）之後、`#sandbox` 之前，用淺色邊框卡片呈現。

## Risks / Trade-offs

- [Claude AI 也可能抓到錯誤的股價] Claude 有時在 JSON 中填錯 `current_price` → 已有警告機制捕捉 ≤ 0 的情況，且我們優先用 yfinance `currentPrice` 覆蓋
- [example_fallback 警告讓使用者困惑] 說明文字要清楚：「財務歷史數據為估算範例，僅供參考，非真實財報數字」
