## ADDED Requirements

### Requirement: History section as fourth SPA view
在現有 `#landing` / `#loading` / `#report` 三個 section 之外，新增 `#history` section，使用相同的 show/hide 切換模式。

#### Scenario: 進入歷史頁面
- **WHEN** 使用者在 Landing 頁點擊「📋 歷史記錄」按鈕，或點擊 Navbar 的「歷史」連結
- **THEN** 隱藏其他 section，顯示 `#history`，呼叫 `loadHistory()`，自動顯示歷史卡片列表

#### Scenario: 從報告頁返回歷史
- **WHEN** 在 `#report` 視圖點擊 Navbar「📋 歷史」
- **THEN** 切換到 `#history` view（報告不需要重新生成）

### Requirement: History card list
`#history` section 顯示卡片網格，每張卡片包含關鍵資訊。

#### Scenario: 顯示歷史卡片
- **WHEN** `loadHistory()` 從 `/api/history` 取得資料
- **THEN** 每張卡片顯示：
  - ticker badge + market badge（US/TW）
  - 公司名稱（粗體）
  - 評等印章（BUY=綠 / HOLD=橘 / AVOID=紅）
  - 現價與目標價（含幣別符號）
  - 分析日期（格式：YYYY-MM-DD HH:mm）
  - 「重新載入報告」按鈕（主要 CTA）
  - 「刪除」按鈕（次要，點擊需確認）

#### Scenario: 歷史為空
- **WHEN** 無任何歷史記錄
- **THEN** 顯示空狀態插圖文字「尚無分析記錄，從首頁開始分析第一支股票吧！」並提供「開始分析」按鈕返回 Landing

#### Scenario: 搜尋篩選
- **WHEN** 使用者在搜尋框輸入 ticker（如「QCOM」）
- **THEN** 即時篩選卡片，只顯示符合的記錄（client-side 篩選，不重新呼叫 API）

### Requirement: Reload report from history
點擊「重新載入報告」直接還原報告頁面。

#### Scenario: 重新載入成功
- **WHEN** 點擊歷史卡片的「重新載入報告」
- **THEN** 呼叫 `GET /api/history/<id>`，取得 full_json，呼叫 `renderReport(data)` 顯示完整報告
  - 報告頁面 Navbar 顯示「🕐 歷史報告」badge
  - price_history 為空時，走勢圖區域顯示「歷史報告 · 即時走勢不可用」提示

#### Scenario: 刪除記錄
- **WHEN** 點擊刪除按鈕
- **THEN** 彈出 `confirm('確定要刪除此分析記錄？')` 確認對話框；確認後呼叫 `DELETE /api/history/<id>`，成功後從卡片列表移除該卡片（不需重新整理頁面）

### Requirement: Landing page history entry
Landing 頁面加入歷史入口。

#### Scenario: Landing 頁顯示歷史按鈕
- **WHEN** 載入 Landing 頁面
- **THEN** 輸入框下方顯示「📋 查看歷史記錄」次要連結按鈕；若 `/api/history` 回傳至少一筆記錄，按鈕旁顯示數量徽章（如 `5 筆記錄`）
