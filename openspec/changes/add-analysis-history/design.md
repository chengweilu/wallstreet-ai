## Context

WallStreet AI 是一個 Flask SPA。目前每次 `POST /api/analyze` 成功後，分析結果只存在 HTTP response 中，前端拿到就顯示，關頁後消失。`app.py` 沒有任何持久化邏輯。前端是單一 `index.html` 的純 JavaScript SPA，透過 show/hide section 切換視圖。現有視圖：`#landing`、`#loading`、`#report`。

## Goals / Non-Goals

**Goals:**
- 每次成功分析後自動儲存到本機 SQLite
- 新增歷史列表視圖（卡片式），可按 ticker 篩選
- 點擊歷史卡片直接重載完整報告（不呼叫 AI，免費）
- 報告視圖顯示「來自歷史紀錄」標示
- 可刪除個別歷史記錄

**Non-Goals:**
- 不做使用者帳號 / 多人共享（純本機單人使用）
- 不做報告比較 / diff 功能
- 不做雲端同步
- 不壓縮或加密 JSON 儲存

## Decisions

**D1 — 儲存引擎選 SQLite**
Python stdlib `sqlite3` 無需安裝，`history.db` 單檔便於備份。不用 JSON files（不好查詢）。不用 Redis（需要啟動服務）。

Schema:
```sql
CREATE TABLE analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    company_name TEXT,
    rating TEXT,
    target_price REAL,
    current_price REAL,
    market TEXT,
    currency TEXT,
    created_at TEXT NOT NULL,   -- ISO 8601
    full_json TEXT NOT NULL      -- 完整報告 JSON（不含 price_history，節省空間）
);
CREATE INDEX idx_ticker ON analyses(ticker);
CREATE INDEX idx_created_at ON analyses(created_at DESC);
```

**D2 — 儲存時機與內容**
在 `analyze()` route 成功解析 `analysis` dict 後、回傳 response 前呼叫 `save_to_history(analysis)`。
`full_json` 不存 `price_history`（每次都可重新從 yfinance 取得，且可能有幾百筆佔空間大），其他欄位全存。

**D3 — 前端新增第四個視圖 `#history`**
現有視圖切換模式（show/hide）直接擴展，新增 `#history` section。
Navbar 加入「📋 歷史」入口，Landing 頁面加入「查看歷史記錄」次要按鈕。

**D4 — 歷史卡片設計**
每張卡片顯示：
- 公司名稱 + ticker badge
- 評等印章（BUY/HOLD/AVOID 彩色）
- 現價 + 目標價 + 上漲空間
- 分析日期
- [重新載入報告] 按鈕 + [刪除] 按鈕

重新載入時呼叫 `GET /api/history/<id>`，取回 full_json 直接呼叫 `renderReport(data)` — 完全複用現有渲染邏輯。

**D5 — price_history 在歷史重載時的處理**
重載歷史報告時，`price_history` 為空陣列（因為未儲存），價格走勢圖不顯示或顯示「歷史報告無法顯示即時走勢圖」提示。其他 7 個 Chart.js 圖表正常顯示（因為數據都存在）。

**D6 — 同一 ticker 重複分析**
不去重，每次都存一筆新記錄。這讓使用者可以比較不同時間點的評等變化。最新在最上面。

## Risks / Trade-offs

| 風險 | 緩解措施 |
|------|---------|
| `full_json` 每筆 ~50-100KB，100 筆就約 10MB | SQLite 輕鬆支援，且歷史不會太多 |
| 儲存失敗不應阻斷 API 回傳 | `save_to_history()` 包裝在 try/except 中，失敗只 log 不拋出 |
| price_history 空陣列導致走勢圖空白 | 歷史視圖加「🕐 歷史報告 · 走勢圖不可用」badge |
| 前端 JS 複雜度增加 | 歷史功能全部封裝在 `HistoryManager` 物件中，不污染現有程式碼 |
