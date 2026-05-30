## 1. 後端數據擴充（app.py）

- [x] 1.1 在 `get_stock_data()` 的 info 欄位抓取清單中加入 `enterpriseValue`、`ebitda`、`forwardEps`
- [x] 1.2 新增 `calc_data_completeness(d)` 函式：對 8 個關鍵欄位（currentPrice、trailingPE、grossMargins、operatingMargins、profitMargins、returnOnEquity、freeCashflow、financials）加權計分，返回 0–100 整數
- [x] 1.3 在 `build_prompt()` 函式開頭呼叫 `calc_data_completeness(d)`，將結果存入 `completeness` 變數

## 2. Prompt 框架強化（app.py）

- [x] 2.1 在 `build_prompt()` 的 prompt 開頭（`name_lock` 之前）加入三階段分析框架段落：「研究框架：① 區分已驗證數據 vs AI 估算 ② 對每個多頭論點進行魔鬼代言人反駁 ③ 給出數據加權後的最終判斷」
- [x] 2.2 在 prompt 的即時市場數據區段，對每個有值的欄位加上「✅」標記，對 None/0 欄位加上「⚠️ 需估算」標記
- [x] 2.3 在 prompt 中加入 `data_completeness_score: {completeness}` 告知 Claude 數據完整度，要求 Claude 在 `confidence_score` 欄位中給出不超過此分數的自評

## 3. JSON Schema 擴充（app.py prompt）

- [x] 3.1 在 prompt 的 JSON 模板頂層加入 `"confidence_score": 85` 佔位欄位（要求 Claude 替換為 0–100 整數）
- [x] 3.2 在 prompt 的 `section4` JSON 模板加入 `"ev_ebitda_analysis": "EV/EBITDA三法加權估值分析..."` 欄位
- [x] 3.3 在 prompt 的 `section4` JSON 模板加入 `"weighted_target": 185.50` 欄位（三法加權目標價）
- [x] 3.4 在 prompt 中加入 EV/EBITDA 數據輸入：`EV: {fmt_num(d.get('enterpriseValue'))} | EBITDA: {fmt_num(d.get('ebitda'))}`

## 4. 前端顯示信心分數（index.html）

- [x] 4.1 在 `renderReport()` 函式中找到 metrics bar 渲染區，新增「分析信心」指標欄位，讀取 `d.confidence_score`
- [x] 4.2 信心分數顏色邏輯：`>= 80` 用 `.up`（綠），`50–79` 用 `.amber`（琥珀），`< 50` 用 `.down`（紅）
- [x] 4.3 在 Section 4 HTML 模板（估值分析卡片區）加入 EV/EBITDA 分析文字區塊與加權目標價顯示

## 5. 驗證

- [x] 5.1 啟動伺服器，分析 AAPL，確認 prompt 包含框架指示與 ✅/⚠️ 標記（看 Flask log 或加臨時 print）
- [x] 5.2 確認 Claude 回傳 JSON 含 `confidence_score` 欄位
- [x] 5.3 確認 report metrics bar 顯示「分析信心」欄位並正確著色
- [x] 5.4 確認 Section 4 顯示 EV/EBITDA 分析與加權目標價
