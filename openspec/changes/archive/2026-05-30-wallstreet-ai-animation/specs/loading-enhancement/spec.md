## ADDED Requirements

### Requirement: Shimmer 骨架動畫
Loading 畫面中的文字占位符 SHALL 使用 shimmer 動畫效果，而非靜態顯示。

#### Scenario: 分析進行中
- **WHEN** 使用者點擊分析按鈕，loading section 顯示
- **THEN** 骨架占位元素顯示由左至右掃過的 shimmer 光澤動畫（無限循環，duration: 1.5s）

### Requirement: 進度條平滑過渡
`.loader-bar` 的寬度變化 SHALL 使用 `transition: width 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)`，避免跳動。

#### Scenario: 進度更新
- **WHEN** JS 更新 loader-bar 寬度
- **THEN** 進度條平滑滑動至新寬度，不閃動

### Requirement: Loading Ring 升級動畫
`.loader-ring` SHALL 使用雙色圓弧旋轉，並加入輕微脈衝（scale）效果。

#### Scenario: Loading 進行中
- **WHEN** loading section 可見
- **THEN** 旋轉圓圈同時有 1.02 倍的緩慢脈衝呼吸效果（duration: 2s, alternate）
