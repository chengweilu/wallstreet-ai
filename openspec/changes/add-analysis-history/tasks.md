## 1. SQLite 初始化與儲存邏輯（`app.py`）

- [x] 1.1 在 `app.py` 頂部 import `sqlite3`，定義 `DB_PATH`
- [x] 1.2 實作 `init_db()` 函數，建立 `analyses` 表與兩個 index
- [x] 1.3 模組載入時呼叫 `init_db()`（啟動時自動建表）
- [x] 1.4 實作 `save_to_history(analysis: dict)` 函數，排除 `price_history`，try/except 包裹
- [x] 1.5 在 `analyze()` route 的 `return` 前呼叫 `save_to_history(analysis)`

## 2. 歷史 API 路由（`app.py`）

- [x] 2.1 實作 `GET /api/history`，支援 `?ticker=` 篩選，依 `created_at DESC` 排序
- [x] 2.2 實作 `GET /api/history/<int:record_id>`，回傳 full_json；找不到時 HTTP 404
- [x] 2.3 實作 `DELETE /api/history/<int:record_id>`；找不到時 HTTP 404

## 3. 前端歷史頁面結構（`templates/index.html`）

- [x] 3.1 在 `#report` 之後新增 `<section id="history">` HTML 結構
- [x] 3.2 新增歷史卡片 CSS 樣式（`history-card`、評等印章、按鈕、空狀態）
- [x] 3.3 在 Navbar 加入「📋 歷史」連結 + 歷史報告 badge
- [x] 3.4 在 Landing 頁的 `input-card` 底部加入「📋 查看歷史記錄」按鈕

## 4. 前端歷史功能 JavaScript（`templates/index.html`）

- [x] 4.1 實作 `showHistory()` 函數
- [x] 4.2 實作 `loadHistory()` 函數
- [x] 4.3 實作 `renderHistoryCards(items)` 函數
- [x] 4.4 實作 `reloadFromHistory(id)` 函數，含「🕐 歷史報告」badge
- [x] 4.5 實作 `deleteHistory(id, cardElement)` 函數，含淡出動畫
- [x] 4.6 實作 `filterHistory()` client-side 搜尋篩選
- [x] 4.7 `DOMContentLoaded` 時呼叫 `fetchHistoryCount()` 更新 Landing 頁數量徽章
- [x] 4.8 price_history 為空時顯示「歷史報告 · 即時走勢不可用」提示

## 5. 收尾

- [x] 5.1 確認 `history.db` 加入 `.gitignore`
- [ ] 5.2 重啟 Flask，手動分析一支股票，確認 `history.db` 有新記錄
- [ ] 5.3 在瀏覽器點擊「歷史記錄」，確認卡片正常顯示，點「重新載入報告」可完整還原報告頁面
