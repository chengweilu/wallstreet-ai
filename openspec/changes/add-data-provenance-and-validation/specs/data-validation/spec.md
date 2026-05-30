## ADDED Requirements

### Requirement: 後端驗證關鍵數據合理性
後端 `analyze()` route SHALL 在回傳前驗證關鍵欄位，並將異常情況記錄至 `data_warnings` 列表。

#### Scenario: 股價無效警告
- **WHEN** `current_price <= 0` 或 `current_price` 為 null
- **THEN** `data_warnings` 包含 `{"field": "current_price", "message": "股價資料異常，請確認股票代碼是否正確"}`

#### Scenario: 財務數據使用範例警告
- **WHEN** `data_sources.annual_data == "example_fallback"`
- **THEN** `data_warnings` 包含 `{"field": "annual_data", "message": "財務歷史數據為範例預設值，非真實財報，僅供參考"}`

#### Scenario: yfinance 抓取失敗警告
- **WHEN** `_data_quality == 'limited'`（yfinance 部分或全部失敗）
- **THEN** `data_warnings` 包含 `{"field": "market_data", "message": "即時市場數據抓取受限，部分數值由 AI 依訓練資料填補，可能非最新"}`

#### Scenario: 無異常時回傳空列表
- **WHEN** 所有驗證通過
- **THEN** `data_warnings == []`

### Requirement: 前端在報告中顯示資料警告
前端 SHALL 對有警告的欄位顯示 `⚠` 圖示，hover 時顯示警告訊息。

#### Scenario: 股價旁顯示警告
- **WHEN** `data_warnings` 包含 `field == "current_price"` 的項目
- **THEN** 報告 header 的股價旁顯示 `⚠` 圖示，hover 顯示警告文字

#### Scenario: 無警告時不顯示警告圖示
- **WHEN** `data_warnings == []`
- **THEN** 報告頁不顯示任何 `⚠` 警告圖示
