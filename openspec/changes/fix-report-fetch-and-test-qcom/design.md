## Context

WallStreet AI 的核心流程：`POST /api/analyze` → yfinance 取數據 → build_prompt → Claude API → `json.loads` → 回傳前端。

目前失敗集中在第 4→5 步：Claude 回傳的文字包含佔位符文字（「目標價數字」）、trailing comma、或因 max_tokens 截斷導致 JSON 不完整，`json.loads` 直接拋出 `JSONDecodeError`，前端只顯示通用錯誤。yfinance 第 2 步若被 Yahoo 限速，拿到空數據仍繼續，Claude 會在回傳 JSON 中留下更多佔位符。

## Goals / Non-Goals

**Goals:**
- 修復 JSON 解析失敗，讓大多數 Claude 回傳都能被正確處理
- yfinance 加自動重試，讓 QCOM 能拿到真實財務數據
- 修正 prompt 中文佔位符，避免 Claude 誤解欄位
- 提供 `test_qcom.py` 可執行的端對端驗證腳本

**Non-Goals:**
- 不引入 `json-repair` 等第三方庫（保持 zero new deps）
- 不做完整的 unit test suite
- 不修改前端視覺設計

## Decisions

**D1 — JSON 修復策略（三層 fallback）**
```
Layer 1: json.loads(raw)                          → 最快路徑
Layer 2: json.loads(clean(raw))                    → 正則清理後再解析
  - 移除 trailing comma: ,\s*([}\]])  →  \1
  - 移除 JSON 內的中文「描述」佔位符（替換成 0 或 ""）
  - 修正未閉合的字串
Layer 3: json.loads(extract_first_object(raw))     → 截斷修復，抓 { 到最後一個完整 }
Layer 4: raise 帶具體 raw 前 200 字的錯誤          → 回傳給前端顯示
```
不使用外部庫，確保 zero new deps。

**D2 — yfinance 重試策略**
```python
for attempt in range(3):
    try:
        data = stock.info  # or financials
        break
    except YFRateLimitError:
        time.sleep(2 ** attempt)  # 2s, 4s, 8s
    except Exception:
        break  # 非限速錯誤不重試
```
重試最多 3 次，不阻塞超過 14 秒（2+4+8），失敗後降級到 Claude 訓練知識模式。

**D3 — Prompt 數字佔位符修正**
原本：`"target_price_12m": 目標價數字,`
改為：`"target_price_12m": 185.50,  // 範例：請填入實際估算的目標價數字`
用 C-style 行內注解（`//`），Claude 在 JSON 生成模式下能正確忽略它。

**D4 — test_qcom.py 設計**
獨立腳本，讀取 `ANTHROPIC_API_KEY` 環境變數，POST 到 `http://localhost:5000/api/analyze`，驗證回傳 JSON 必含欄位（`company_name`, `section1`~`section7`, `sandbox`），打印重點摘要（公司名、評等、目標價、護城河評分），全部通過才顯示 `✅ QCOM 分析成功`。

## Risks / Trade-offs

| 風險 | 緩解措施 |
|------|---------|
| Layer 3 截斷修復可能拿到不完整 JSON，部分欄位為 null | 前端已有 `id || '--'` fallback，不影響顯示 |
| yfinance 14 秒重試增加請求延遲 | loading 動畫夠長，使用者感受不明顯 |
| Prompt 行內注解 `//` 若 Claude 將其包入字串值 | 加入 Layer 2 清理移除 `//` 行 |
| QCOM 測試需要真實 API Key 才能執行 | 測試腳本說明文件加 `.env` 讀取支援 |
