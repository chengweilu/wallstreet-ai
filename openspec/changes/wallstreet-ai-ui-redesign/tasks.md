## 1. Landing Hero 改善

- [x] 1.1 更新 `.landing-title` CSS：font-size 改為 `clamp(36px, 5.5vw, 58px)`，line-height 改為 `1.08`，letter-spacing 改為 `-0.025em`
- [x] 1.2 更新 `.input-card` CSS：移除 padding-bottom，box-shadow 改為琥珀色微光，padding 改為 `24px 24px 0`
- [x] 1.3 新增 `.input-divider` CSS class：`border-top: 1px solid var(--stone-6); margin: 0;`
- [x] 1.4 更新 `.input-row` CSS：`margin-bottom: 0; padding-bottom: 20px`
- [x] 1.5 更新 `.btn-history-landing` CSS：移除獨立外框 border，圓角改為 `0 0 20px 20px`，融入卡片底部
- [x] 1.6 HTML 中在 `.input-row` 與 `.btn-history-landing` 之間插入 `<div class="input-divider"></div>`
- [x] 1.7 更新 `.features` CSS：從 `grid` 改為 `flex wrap`，justify-content 置中
- [x] 1.8 更新 `.feature` CSS：改為 inline-flex chip 樣式，加入 hover 邊框效果
- [x] 1.9 更新 `.feature-desc` CSS：加入 `display: none`
- [x] 1.10 更新 `.btn-analyze` CSS：靜態加入 `box-shadow: 0 4px 16px rgba(180,83,9,0.28)`，hover 陰影加強

## 2. Report Header 改善

- [x] 2.1 更新 `.report-header` CSS：背景改為 `linear-gradient(160deg, #1c1917 0%, #2c2420 60%, #3b1f0a 100%)`
- [x] 2.2 更新 `.rating-stamp` CSS：`border-radius` 改為 `20px`，邊框改為 `1.5px`，新增 `position: relative`
- [x] 2.3 新增 `.rating-stamp::after` CSS：內層光影 `box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06)`
- [x] 2.4 更新 `.final-rating-stamp` CSS：`border-radius` 改為 `24px`，邊框改為 `1.5px`
- [x] 2.5 更新 `.metric-item` CSS：hover 改為 `background: rgba(217,119,6,0.08)`（琥珀色微光）
- [x] 2.6 更新 `.sec-num` CSS：`border-radius` 改為 `8px`，改用 `inline-flex`，font-family 加入 `'Inter'`

## 3. Cards 與 Chart Cards 升級

- [x] 3.1 更新 `.card` CSS：`border-radius` 改為 `18px`，陰影改為 `0 1px 12px rgba(28,25,23,0.05)`，加入 hover `translateY(-1px)` 與陰影加深
- [x] 3.2 更新 `.chart-card` CSS：`border-radius` 改為 `18px`，陰影與 `.card` 一致，加入 hover 陰影效果
- [x] 3.3 更新 `.card-title` CSS：`font-size` 改為 `11px`，`letter-spacing` 改為 `0.09em`，左側線條改為 `2.5px` 寬、`13px` 高

## 4. Data Table 升級

- [x] 4.1 更新 `.data-table th` CSS：`font-size` 改為 `10px`，`letter-spacing` 改為 `0.08em`，`border-bottom` 改為 `1px`（移除 2px）
- [x] 4.2 新增 `.data-table tbody tr:nth-child(even) td` CSS：`background: #fafaf9`（zebra stripe）
- [x] 4.3 更新 `.data-table tr:hover td` CSS：改為 `background: rgba(217,119,6,0.04)`

## 5. Scenario Cards 與 History 升級

- [x] 5.1 更新 `.sc-target` CSS：`font-size` 改為 `36px`，加入 `font-family: 'Inter'`，`line-height: 1`，`letter-spacing: -0.02em`
- [x] 5.2 更新 `.hc-stamp` CSS：`border-radius` 改為 `10px`，邊框改為 `1.5px`
- [x] 5.3 更新 `.history-card` CSS：`border-radius` 改為 `18px`，陰影改為 `0 1px 12px rgba(28,25,23,0.05)`，hover 陰影加深

## 6. 視覺驗證

- [ ] 6.1 在瀏覽器開啟 index.html，確認 Landing Hero 標題、chip 列、Input Card 分隔線正確顯示
- [ ] 6.2 輸入股票代碼執行分析，確認 Report Header 漸層、評分章圓角方形正確顯示
- [ ] 6.3 確認 Metrics 指標列 hover 為琥珀色微光
- [ ] 6.4 確認競爭對手表格顯示 zebra stripe 與 hover 效果
- [ ] 6.5 確認情境卡目標價以大字體 Inter 顯示
- [ ] 6.6 確認歷史記錄頁面的 stamp 和 card 圓角一致
