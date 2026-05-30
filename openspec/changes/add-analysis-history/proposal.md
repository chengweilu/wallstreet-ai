## Why

每次分析完成後結果就消失，使用者無法回顧過去的報告、比較同一股票不同時間的評等變化，也無法快速重新載入已分析的報告（需要重花 API 費用再分析一次）。現在需要一個持久化的歷史紀錄系統，讓每次分析自動存檔，並提供瀏覽頁面讓使用者隨時回看。

## What Changes

- **自動儲存分析結果**：每次 `/api/analyze` 成功後，將完整報告 JSON 連同元資料（ticker、公司名、評等、目標價、分析日期）自動寫入本機 SQLite 資料庫（`history.db`）
- **歷史列表 API**：新增 `GET /api/history` 端點，回傳所有歷史分析的摘要列表（依日期降序），支援按 ticker 篩選
- **報告讀取 API**：新增 `GET /api/history/<id>` 端點，回傳單筆完整報告 JSON，讓前端可以完整還原報告頁面
- **歷史瀏覽頁面**：在現有 SPA 中新增「歷史記錄」視圖，顯示卡片式列表，每張卡片含公司名稱、評等徽章、目標價、分析日期，點擊即可重新載入完整報告（不需重新呼叫 AI）
- **刪除功能**：每筆歷史紀錄可個別刪除（`DELETE /api/history/<id>`）
- **Navbar 新增入口**：Landing 頁面加入「歷史記錄」按鈕，報告頁面 Navbar 加入「📋 歷史」連結

## Capabilities

### New Capabilities
- `history-storage`: SQLite 持久化儲存分析結果，自動去除 price_history 等大型資料節省空間
- `history-api`: REST API 端點（list / get / delete）供前端讀取歷史
- `history-ui`: 歷史瀏覽頁面，卡片列表 + 點擊重載完整報告

### Modified Capabilities
<!-- 無需修改既有 spec -->

## Impact

- **`app.py`**：新增 SQLite 初始化邏輯、`save_to_history()` 函數、3 個新 API 路由
- **`templates/index.html`**：新增 `#history` section、歷史卡片 HTML 模板、載入歷史的 JS 函數、Navbar 入口
- **依賴**：使用 Python stdlib `sqlite3`，zero new dependencies
- **資料存放**：`history.db` 建立於 `stock_analyzer/` 根目錄，gitignore 排除
