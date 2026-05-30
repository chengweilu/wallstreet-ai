## ADDED Requirements

### Requirement: 頂部核心數據看板
儀表板 SHALL 在頁面頂部以 Grid 卡片顯示 S&P 500 關鍵指標。

#### Scenario: 看板數據顯示
- **WHEN** 頁面載入完成
- **THEN** 顯示：當前市值門檻（億美元）、篩出邊緣股數量、候選調整日期、資料更新時間

### Requirement: 候選股動態矩陣表格
儀表板 SHALL 提供可排序、可搜尋的候選股表格。

#### Scenario: 欄位點擊排序
- **WHEN** 使用者點擊表頭（如「Days to Cover」、「市值」、「機構持股」）
- **THEN** 表格依該欄位升冪/降冪切換排序，箭頭圖示更新

#### Scenario: 關鍵字搜尋
- **WHEN** 使用者在搜尋框輸入文字（如 "TECH" 或 "Health"）
- **THEN** 表格即時過濾，只顯示 ticker 或板塊包含該字串的列

### Requirement: 板塊權重落差圖與 Days to Cover 圖
儀表板 SHALL 使用 Plotly.js 繪製互動式圖表。

#### Scenario: 板塊落差圖 hover
- **WHEN** 滑鼠懸停在板塊落差長條圖上
- **THEN** tooltip 顯示「S&P 500 權重 vs 全市場權重 差距：X.XX%」

#### Scenario: Days to Cover 圖排序
- **WHEN** Days to Cover 長條圖渲染完成
- **THEN** 依 days_to_cover 降冪排列，最高者顯示在最上方（橫向長條圖）

### Requirement: 互動式 K 線圖 + 技術指標
儀表板 SHALL 對前 3 名候選股提供可切換 Tab 的 K 線圖。

#### Scenario: Tab 切換股票
- **WHEN** 使用者點擊不同股票的 Tab
- **THEN** K 線圖、RSI、MACD 圖表全部更新至對應股票數據

#### Scenario: K 線圖縮放
- **WHEN** 使用者在 K 線圖上滾動滑鼠或拖拉選取範圍
- **THEN** Plotly 圖表縮放至選定時間區間，50/200 SMA 隨之更新

#### Scenario: 買點區間標注
- **WHEN** K 線圖渲染完成
- **THEN** 圖表顯示半透明綠色「策略買點區間」矩形與橘色「防守停損」水平線

### Requirement: 數據審計日誌 Modal
儀表板 SHALL 提供彈窗顯示 fetch_data.py 的驗證紀錄。

#### Scenario: 開啟 Modal
- **WHEN** 使用者點擊「查看驗證日誌」按鈕
- **THEN** Modal 彈出，顯示每支被驗證股票的來源、數值比對、是否校正

#### Scenario: 關閉 Modal
- **WHEN** 使用者點擊 Modal 外部或關閉按鈕
- **THEN** Modal 關閉，回到主儀表板
