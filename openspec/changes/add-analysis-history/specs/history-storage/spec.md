## ADDED Requirements

### Requirement: Auto-initialize SQLite on startup
Flask 應用程式啟動時必須自動建立 `history.db` 與 `analyses` 資料表（若不存在）。

#### Scenario: 首次啟動（history.db 不存在）
- **WHEN** 執行 `python3 app.py`，`history.db` 不存在
- **THEN** 自動在 `stock_analyzer/` 根目錄建立 `history.db`，並建立 `analyses` 表與兩個 index

#### Scenario: 重複啟動（history.db 已存在）
- **WHEN** `history.db` 已存在且有資料
- **THEN** 使用 `CREATE TABLE IF NOT EXISTS`，不覆蓋現有資料

### Requirement: Auto-save on successful analysis
每次 `/api/analyze` 成功時必須自動儲存報告。

#### Scenario: 分析成功
- **WHEN** Claude 回傳 JSON 解析成功，`analysis` dict 完整
- **THEN** 呼叫 `save_to_history(analysis)` 將以下欄位存入 DB：
  - `ticker`（從 analysis.ticker）
  - `company_name`（從 analysis.company_name）
  - `rating`（從 analysis.overall_rating）
  - `target_price`（從 analysis.target_price_12m，可為 null）
  - `current_price`（從 analysis.current_price）
  - `market`（從 analysis.market）
  - `currency`（從 analysis.currency）
  - `created_at`（當下 ISO 8601 時間）
  - `full_json`（`json.dumps(analysis)`，不含 `price_history` key）

#### Scenario: 儲存失敗（DB 錯誤）
- **WHEN** `save_to_history()` 內發生任何 exception
- **THEN** 不影響 API 正常回傳，只在 server console 印出 `[history] save failed: <error>`

### Requirement: price_history 不儲存
`full_json` 中不包含 `price_history` 欄位（從 analysis dict 移除後再序列化）。

#### Scenario: 儲存時
- **WHEN** `save_to_history()` 被呼叫，analysis 含 `price_history`
- **THEN** 先執行 `data = {k:v for k,v in analysis.items() if k != 'price_history'}` 後再序列化
