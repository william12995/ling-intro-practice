# 工作紀錄 — 2026-10-09

接續 10-08 那次（同一個對話跨過午夜），大部分內容見 `session_log_2026-10-08.md`。

## 本次完成事項

- 使用者看了構詞樹新題 S1-15～S1-24 的截圖，覺得外語題偏難，但先維持題目不變，只加提示。
- `ch03_morph_tree/morph_tree.src.html` 四題外語題的語素註解後面各加一行 Hint（題號、順序、標準答案都沒動）：
  - S1-21 Turkish：ev 後面全是後綴，離詞根最近的先接。
  - S1-22 Japanese：tabe 是詞根，其他三個是後綴，從旁邊那個先接。
  - S1-23 Meskwaki my daughters：ne 在前、aki 在後，一個是前綴一個是後綴。
  - S1-24 Meskwaki our daughters：ne 和 ena·n 可能是同一個詞綴的兩半（環綴），同時接上，放在跟詞根同一個節點下。
- `test_record_and_ux.py` 0 失敗、`test_build_all.py mouse` 0 失敗。重建 docs、commit、push。

## 發現的重要資訊

- 使用者的回饋：外語題太難。之後要加外語題，要嘛降低難度（例如只有一兩個後綴），要嘛直接附提示。

## 下次從這裡開始

照 `session_log_2026-10-08.md` 的「下次從這裡開始」，優先順序不變：

1. 請老師核：句法 S1-05～09、構詞樹 S1-15～24 的標準答案；「少放 X-bar」的解讀；構詞樹的 Prefix／Suffix／Circumfix 標籤；telescope 的 N' → N PP 要不要也算對。
2. 三份 Sheet 的 Z00000000 測試列請使用者刪；句法、構詞樹 Sheet 時區改 GMT+08:00。
3. 匯出構詞樹 Sheet 看哪題錯最多（排除 R13142001、Z00000000、B20260101），特別看外語題 S1-21～24 加提示後的首次正確率。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 構詞樹頁 | `ch03_morph_tree/morph_tree.src.html`，測試 `ch03_morph_tree/tests/` |
| 線上版 | https://william12995.github.io/ling-intro-practice/ch03_morph_tree/ |

重跑構詞樹測試（在 `ch03_morph_tree/tests/`）：
```
set PYTHONIOENCODING=utf-8
python test_build_all.py mouse
python test_build_all.py touch
python test_tap_mode.py
python test_record_and_ux.py
```
改完 src 跑 `python build_site.py`，再 commit、push。
