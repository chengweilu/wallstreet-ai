## ADDED Requirements

### Requirement: 報告可匯出為 PNG 圖片
系統 SHALL 在報告頁面提供「下載圖片」按鈕，點擊後將整份報告渲染為 PNG 並觸發瀏覽器下載。

#### Scenario: 成功匯出
- **WHEN** 使用者在報告頁面點擊「下載圖片」按鈕
- **THEN** 系統使用 html2canvas 捕捉 `#report` 節點，生成 PNG 並觸發下載，檔名格式為 `TICKER_YYYYMMDD.png`

#### Scenario: 匯出期間顯示進度
- **WHEN** html2canvas 正在渲染（捕捉過程）
- **THEN** 按鈕顯示「生成中...」並暫時禁用，防止重複點擊

#### Scenario: 匯出完成後恢復按鈕
- **WHEN** PNG 下載觸發完成後
- **THEN** 按鈕文字恢復為「下載圖片」且重新啟用

### Requirement: html2canvas 函式庫從 CDN 載入
系統 SHALL 透過 `<script>` 標籤從 CDN 載入 html2canvas，不需後端安裝任何套件。

#### Scenario: CDN 載入
- **WHEN** 瀏覽器載入頁面
- **THEN** html2canvas 腳本從 CDN URL 載入，可在 `exportReportAsImage()` 函數中使用
