## ADDED Requirements

### Requirement: 技術指標 API 路由
`app.py` SHALL 新增 `GET /api/technical/<ticker>` 路由，取 90 天日線數據，計算並回傳技術指標。

#### Scenario: 成功取得技術數據
- **WHEN** `GET /api/technical/AAPL` 被呼叫
- **THEN** 回傳 JSON `{"success": true, "data": {"ma20": float, "ma50": float, "ma200": float, "rsi": float, "macd": float, "macd_signal": float, "macd_hist": float, "price_with_ma": [...], "signal_score": int, "signal_label": str}}`

#### Scenario: 數據不足計算 MA200
- **WHEN** yfinance 日線數據少於 200 筆
- **THEN** `ma200` 欄位為 `null`，其他可計算指標正常回傳

#### Scenario: yfinance 失敗
- **WHEN** yfinance 拋出例外
- **THEN** 回傳 `{"success": false, "error": "..."}`，HTTP 200（前端 graceful fallback）

### Requirement: 指標計算正確性
RSI SHALL 使用 14 日 Wilder 平滑法（ewm with com=13）。MACD SHALL 使用 EMA12 - EMA26，Signal = 9 日 EMA of MACD。

#### Scenario: RSI 計算
- **WHEN** 收盤價序列長度 >= 14
- **THEN** `rsi` 為 0–100 之間的浮點數

#### Scenario: MACD 計算
- **WHEN** 收盤價序列長度 >= 26
- **THEN** `macd`、`macd_signal`、`macd_hist` 皆為浮點數
