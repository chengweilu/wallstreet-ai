## MODIFIED Requirements

### Requirement: 報告可匯出為 PNG 圖片
系統 SHALL 在報告頁面提供「下載圖片」按鈕，點擊後將整份報告渲染為 PNG 並觸發瀏覽器下載，檔名包含正確的股票代碼。

#### Scenario: 檔名含正確 ticker
- **WHEN** 使用者完成分析（例如 QCOM）後點擊「下載圖片」
- **THEN** 下載的 PNG 檔名格式為 `QCOM_YYYYMMDD.png`，ticker 取自 `currentData.ticker`（而非未定義的 `currentAnalysis`）

#### Scenario: 成功匯出含圖表的完整報告
- **WHEN** html2canvas 捕捉 `#report` 節點完成
- **THEN** 生成的 PNG 包含報告所有區塊，Chart.js 圖表以圖像形式完整呈現（不是空白）

#### Scenario: 匯出期間按鈕禁用
- **WHEN** html2canvas 正在渲染
- **THEN** 按鈕顯示「⏳ 生成中...」且為 disabled 狀態

#### Scenario: 匯出完成後按鈕恢復
- **WHEN** PNG 下載觸發完成（成功或失敗）
- **THEN** 按鈕文字與可用狀態均恢復為初始值
