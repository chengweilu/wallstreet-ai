## 1. 後端：`get_stock_data()` 追蹤數據來源（`app.py`）

- [x] 1.1 在 `get_stock_data()` 初始化 `result['_sources'] = {}`，並在每個 yfinance 抓取區塊成功後設定：`_sources['current_price'] = 'yahoo_finance'`、`_sources['financials'] = 'yahoo_finance'`、`_sources['cashflows'] = 'yahoo_finance'`、`_sources['price_history'] = 'yahoo_finance'`
- [x] 1.2 在 `build_annual_data_template()` 結尾回傳一個 tuple `(annual_data_str, source)`，其中 source 為 `'yahoo_finance'`（fin 非空）或 `'example_fallback'`（fin 為空）

## 2. 後端：`analyze()` route 建立 `data_sources` 與 `data_warnings`（`app.py`）

- [x] 2.1 在 `analyze()` route 取得 `stock_data` 後，從 `stock_data.get('_sources', {})` 讀取 yfinance 來源，並加上 AI 固定來源，組成 `data_sources` dict：`{ "current_price": ..., "annual_data": ..., "cashflows": ..., "target_price_12m": "claude_ai", "overall_rating": "claude_ai", "moat_score": "claude_ai" }`
- [x] 2.2 實作 `validate_analysis(analysis, stock_data, data_sources)` 函數，回傳 `data_warnings` 列表，檢查三條規則：股價 <= 0、`annual_data == 'example_fallback'`、`_data_quality == 'limited'`
- [x] 2.3 在 `analyze()` 呼叫 Claude 並解析 JSON 後，呼叫 `validate_analysis()`，並將 `data_sources` 與 `data_warnings` 注入 `analysis` dict，再回傳

## 3. 前端：來源徽章 CSS 與 JS（`templates/index.html`）

- [x] 3.1 新增來源徽章 CSS：`.src-badge`（基底）、`.src-yf`（綠色，`YF`）、`.src-ai`（藍色，`AI`）、`.src-fallback`（橘色，`⚠ 範例數據`）、`.src-warn`（⚠ tooltip 容器）
- [x] 3.2 實作 `applyDataBadges(data)` JS 函數，根據 `data.data_sources` 在以下位置插入徽章：報告 header 股價旁、報告 header 目標價旁、section2 護城河評分旁、section3 財務表格標題旁

## 4. 前端：資料警告 tooltip（`templates/index.html`）

- [x] 4.1 在 `applyDataBadges()` 中，遍歷 `data.data_warnings`，對對應欄位附近的 `⚠` 圖示加入 `title` 屬性顯示警告文字
- [x] 4.2 在 `renderReport(data)` 函數中（報告渲染完成後）呼叫 `applyDataBadges(data)`

## 5. 前端：資料品質摘要卡片（`templates/index.html`）

- [x] 5.1 在 HTML 的 `#sandbox-sec` 之前新增 `<div id="data-quality-sec">` 卡片結構（含「真實市場數據」與「AI 估算」兩欄 + 警告區）
- [x] 5.2 新增卡片 CSS 樣式（cream 背景、stone 邊框、橘色警告區塊）
- [x] 5.3 實作 `renderDataQualityCard(data)` JS 函數，填充兩欄內容與警告訊息
- [x] 5.4 在 `renderReport(data)` 末尾呼叫 `renderDataQualityCard(data)`

## 6. 收尾

- [ ] 6.1 重啟 Flask，分析 QCOM，確認：報告 header 股價旁出現綠色 `YF` 徽章、目標價旁出現藍色 `AI` 徽章、底部出現資料品質摘要卡片
- [ ] 6.2 確認當 yfinance 失敗（模擬方式：輸入無效 ticker 後觀察）時，警告訊息正確顯示

