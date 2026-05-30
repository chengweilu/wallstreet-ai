## ADDED Requirements

### Requirement: GET /api/history — 列出所有歷史記錄
回傳摘要列表，不含 full_json（避免傳輸量過大）。

#### Scenario: 有歷史記錄
- **WHEN** `GET /api/history`
- **THEN** 回傳 `{"success": true, "data": [...]}`，每筆包含：
  - `id`, `ticker`, `company_name`, `rating`, `target_price`, `current_price`, `market`, `currency`, `created_at`
  - 依 `created_at` **降序**排列（最新在前）

#### Scenario: 有 ticker 篩選
- **WHEN** `GET /api/history?ticker=QCOM`
- **THEN** 只回傳 `ticker = 'QCOM'` 的記錄（大小寫不敏感，`UPPER(ticker) = UPPER(?)`）

#### Scenario: 無歷史記錄
- **WHEN** `GET /api/history`，DB 為空
- **THEN** 回傳 `{"success": true, "data": []}`（HTTP 200，不是 404）

### Requirement: GET /api/history/<id> — 讀取單筆完整報告
回傳 full_json（前端用來重載完整報告頁面）。

#### Scenario: 記錄存在
- **WHEN** `GET /api/history/3`，id=3 存在
- **THEN** 回傳 `{"success": true, "data": <full_json dict>}`（解析 JSON 字串後回傳）

#### Scenario: 記錄不存在
- **WHEN** `GET /api/history/999`，id=999 不存在
- **THEN** 回傳 `{"error": "找不到此分析記錄"}` HTTP 404

### Requirement: DELETE /api/history/<id> — 刪除單筆記錄

#### Scenario: 刪除成功
- **WHEN** `DELETE /api/history/3`
- **THEN** 從 DB 刪除 id=3，回傳 `{"success": true, "message": "已刪除"}`

#### Scenario: 記錄不存在時刪除
- **WHEN** `DELETE /api/history/999`，id 不存在
- **THEN** 回傳 HTTP 404 `{"error": "找不到此分析記錄"}`
