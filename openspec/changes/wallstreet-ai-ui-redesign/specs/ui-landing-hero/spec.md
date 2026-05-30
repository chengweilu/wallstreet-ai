## ADDED Requirements

### Requirement: Landing 標題視覺衝擊力
標題字體 SHALL 使用 `clamp(36px, 5.5vw, 58px)`，行高 SHALL 為 `1.08`，letter-spacing SHALL 為 `-0.025em`，以增強首屏視覺吸引力。

#### Scenario: 大螢幕標題尺寸
- **WHEN** 使用者在 1280px 以上螢幕載入首頁
- **THEN** 標題字體應達到 58px，行高緊湊，文字不換行過多

#### Scenario: 小螢幕標題自適應
- **WHEN** 使用者在 375px 手機螢幕載入首頁
- **THEN** 標題字體自動縮小至 36px，版面不溢出

### Requirement: Input Card 內部分隔線
Input Card SHALL 在主要操作區（股票代碼輸入 + 分析按鈕）與次要操作區（查看歷史）之間加入 `1px solid var(--stone-6)` 分隔線。

#### Scenario: 分隔線可見
- **WHEN** 使用者看到 Landing 頁面的 Input Card
- **THEN** 輸入欄位與歷史按鈕之間應有一條細分隔線，清楚區分主次操作

### Requirement: History 按鈕融入卡片底部
History 按鈕 SHALL 移除獨立外框 border，改為無邊框樣式，底部圓角與 Input Card 一致（`border-radius: 0 0 20px 20px`）。

#### Scenario: 按鈕外觀一致性
- **WHEN** 使用者看到 Input Card
- **THEN** 歷史按鈕應視覺上融入卡片底部，不出現雙重邊框

### Requirement: Feature 區塊 chip 化
Feature 區塊 SHALL 從 3 欄卡片格改為水平 flex wrap chip 列，每個 chip 僅顯示 icon 和標題，描述文字隱藏。

#### Scenario: Chip 列排列
- **WHEN** 使用者看到 Landing 頁面下方的功能介紹
- **THEN** 應看到水平排列的功能 chips，而非 3 欄卡片

#### Scenario: Chip hover 效果
- **WHEN** 使用者 hover 到任一 chip
- **THEN** chip 邊框應顯示琥珀色微光（`rgba(217,119,6,0.3)`）

### Requirement: 分析按鈕立體陰影
分析按鈕 SHALL 在靜態狀態具備 `box-shadow: 0 4px 16px rgba(180,83,9,0.28)`，hover 時陰影加強並上浮 2px。

#### Scenario: 按鈕靜態陰影
- **WHEN** 使用者看到分析按鈕
- **THEN** 按鈕應有明顯的立體感陰影

#### Scenario: 按鈕 hover 狀態
- **WHEN** 使用者 hover 到分析按鈕
- **THEN** 按鈕上移 2px，陰影加深至 `0 10px 28px rgba(180,83,9,0.38)`
