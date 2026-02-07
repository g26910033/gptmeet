# gptmeet

## 非 Google Sheet / Google Doc 模式（已優化）

此版本將資料來源統一調整為 **不依賴 Google Sheet 與 Google Doc** 的模式，改用以下可組合來源：

- 直接手動輸入（`ManualInputSource`）
- 本機檔案（`LocalFileSource`）
- 通用 HTTP JSON API（`HttpJsonSource`）

核心管線位於 `src/data_pipeline.py`，可透過 `create_non_google_pipeline(...)` 快速建立純本地/通用 API 的資料整合流程。

## 設計重點

1. **移除供應商綁定**：避免 Google API 憑證與配額限制。
2. **降低維運成本**：統一來源介面 `DataSource`，後續替換來源不需改主流程。
3. **可測試性提升**：`tests/test_data_pipeline.py` 提供基礎單元測試。

## 執行測試

```bash
python -m unittest discover -s tests -p 'test_*.py'
```
