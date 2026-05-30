## ADDED Requirements

### Requirement: 抓取 S&P 500 成分股清單
系統 SHALL 從 Wikipedia 或 fallback 清單取得 S&P 500 所有成分股 ticker。

#### Scenario: Wikipedia 抓取成功
- **WHEN** `pd.read_html` 成功解析 Wikipedia S&P 500 頁面
- **THEN** 回傳包含 ticker 與板塊的 DataFrame，至少 490 筆

#### Scenario: Wikipedia 抓取失敗使用 fallback
- **WHEN** `pd.read_html` 拋出例外
- **THEN** 改用預存的 ticker 清單，並在 audit_log 記錄 `"sp500_source": "fallback"`

### Requirement: 雙源交叉驗證市值與淨利
系統 SHALL 對 S&P 500 前 50 大市值股票進行 yfinance 與 SEC Edgar 雙源比對。

#### Scenario: 數據一致（誤差 ≤ 1%）
- **WHEN** yfinance 與 SEC Edgar 的市值誤差 ≤ 1%
- **THEN** 使用 yfinance 數據，audit_log 記錄 `"status": "verified"`

#### Scenario: 數據不一致（誤差 > 1%）
- **WHEN** 誤差 > 1%
- **THEN** 以 SEC Edgar 數據為主，audit_log 記錄 `"status": "corrected"`, `"yf_value"`, `"sec_value"`, `"diff_pct"`

### Requirement: 計算邊緣股與被動資金指標
系統 SHALL 計算以下量化指標並輸出至 `dashboard_data.json`。

#### Scenario: 邊緣股篩選
- **WHEN** fetch_data.py 執行完畢
- **THEN** `dashboard_data.json` 包含 `edge_stocks` 陣列，每筆含 ticker、market_cap、is_loss（虧損）、sector、板塊替換後權重變化

#### Scenario: Alpha 指標計算
- **WHEN** fetch_data.py 執行完畢
- **THEN** 每支候選股包含：`institutional_ownership`（%）、`estimated_passive_buy_m`（百萬美元）、`days_to_cover`（天數）

### Requirement: 輸出標準化 JSON
系統 SHALL 輸出 `data/dashboard_data.json` 與 `data/audit_log.json`，並將數據內嵌至 `index.html` 的 `<script>` 變數中。

#### Scenario: JSON 輸出完整
- **WHEN** fetch_data.py 成功執行
- **THEN** `dashboard_data.json` 包含 `meta`、`edge_stocks`、`candidates`、`sector_diff`、`top3_ohlcv` 五個頂層 key

#### Scenario: 內嵌 HTML 更新
- **WHEN** fetch_data.py 執行完畢
- **THEN** `index.html` 中的 `window.DASHBOARD_DATA = {...}` 變數被更新為最新數據
