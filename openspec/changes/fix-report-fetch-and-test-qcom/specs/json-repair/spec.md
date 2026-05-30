## ADDED Requirements

### Requirement: Multi-layer JSON parsing
Claude API 回傳的文字必須透過最多 4 層 fallback 才宣告失敗，不能在第一層 `json.loads` 失敗時立即回傳 500。

#### Scenario: Claude 回傳帶 trailing comma 的 JSON
- **WHEN** Claude 回傳的字串包含 `,}` 或 `,]` 等 trailing comma
- **THEN** Layer 2 正則清理移除 trailing comma 後，`json.loads` 解析成功

#### Scenario: Claude 回傳中文佔位符文字
- **WHEN** JSON 中數字欄位值為中文說明（如 `目標價數字`、`護城河分數1到10`）
- **THEN** Layer 2 將未引號數字佔位符替換為 `0`，字串佔位符替換為空字串，解析成功

#### Scenario: JSON 因 max_tokens 截斷不完整
- **WHEN** Claude 回傳的 JSON 在中途被截斷，末尾缺少閉合括號
- **THEN** Layer 3 從第一個 `{` 到最後一個完整的 `}` 提取，補上缺少的閉合符後解析

#### Scenario: 所有修復嘗試均失敗
- **WHEN** 四層 fallback 都無法解析 JSON
- **THEN** 回傳 HTTP 500，錯誤訊息包含 raw 輸出前 300 字，方便使用者回報問題

### Requirement: Markdown code block stripping
Claude 有時在 JSON 外包裹 markdown code fence（\`\`\`json ... \`\`\`）。

#### Scenario: 回傳包含 code fence
- **WHEN** raw 文字以 \`\`\` 開頭
- **THEN** 在嘗試任何解析前先移除 code fence 包裝
