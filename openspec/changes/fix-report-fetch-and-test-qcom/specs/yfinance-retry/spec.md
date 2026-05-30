## ADDED Requirements

### Requirement: Exponential backoff on rate limit
`get_stock_data()` 在遭遇 Yahoo Finance 限速時必須自動重試，不立即放棄。

#### Scenario: yfinance 第一次回傳 YFRateLimitError
- **WHEN** `stock.info` 拋出 `YFRateLimitError`
- **THEN** 等待 2 秒後重試，最多重試 3 次（總等待上限 14 秒）

#### Scenario: 三次重試後仍失敗
- **WHEN** 三次 yfinance 呼叫均回傳 `YFRateLimitError`
- **THEN** 降級模式：`_data_quality` 標記為 `'limited'`，繼續呼叫 Claude（依訓練知識分析），不回傳 404

#### Scenario: 非限速錯誤（如 ticker 不存在）
- **WHEN** yfinance 拋出非 `YFRateLimitError` 的 Exception
- **THEN** 不重試，直接降級，避免無意義等待

### Requirement: Custom session header
每次 yfinance 請求使用包含真實瀏覽器 User-Agent 的 requests.Session，降低被限速機率。

#### Scenario: 正常請求
- **WHEN** 使用者輸入有效股票代碼（如 QCOM）
- **THEN** yfinance 透過帶有 User-Agent header 的 session 發出請求，回傳完整 info dict
