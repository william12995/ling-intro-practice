# 工作紀錄 — 2026-10-10

## 本次完成事項

- 給使用者三個作業頁和成績 Sheet 的連結（Sheet ID 來自各 `.clasp.json` 的 parentId）：
  - 構詞切詞：`1doD3tRlHDfJ8zRIMcppIHKwF6rXbx9swWlcf79sYnGw`
  - 句法：`1DM6D84b5SGCnGUVc3rF1KCN2opY3SY_fo23nGISZRJY`
  - 構詞樹：`1ntELF7RcI20udt-wriuT8waeEiCiUn9P8UA7L3aG7GE`
- 構詞樹改名（commit `878572c`）。原因是第三單元是別的內容。
  - 頁面資料夾從 `ch03_morph_tree/` 改成 `ch01-2_morph_tree/`，新網址 https://william12995.github.io/ling-intro-practice/ch01-2_morph_tree/ 。
  - quiz id、`clasp_deploy/ch03_morph_tree/`、endpoints.json 的 key 都沒改：Sheet 紀錄、學生瀏覽器的進度、`deploy_clasp.py` 用資料夾名當 quiz id，全部綁著這個 id。
  - `build_site.py` 加了 `MOVED`，會在舊網址產生轉址頁；首頁順序改成 Morphology、word trees、Syntax。
  - 測試 record、build-all mouse、tap 都是 0 失敗（touch 沒跑）。線上新網址回 200，舊網址會轉到新網址。CLAUDE.md、DEPLOY.md 已更新。
- 回答使用者：構詞樹的標準答案全寫 Affix，學生標 Affix 或對的種類（Prefix／Suffix／Circumfix）都算對。使用者還沒決定要不要拿掉這三個標籤。
- 檢查第一周（ch01_morphology）Sheet 作答：
  - 用 Drive 匯出 xlsx，以 event_id 去重，排除 R13142001、Z00000000、B20260101。
  - 27 位學生，18 位寫完 39 題。沒寫完的 9 位：4 位只寫 1～2 題，5 位寫到一半。
  - 錯最多的題：S2-12 misclassified（第一次答對 6/22）、S3-02、S4-02、S5-06、S5-07、S2-01。
  - 明細：`_output/private/ch01_check_2026-10-10.md`
- 可能判太嚴的兩處，另寫成 `_output/private/ch01_太嚴格的判分_2026-10-10.md`，給使用者自己檢查後跟老師討論。內容有列號、學生、推理：
  - S2-12 寫 mis + class + if + ied 的 6 人。
  - S5-07 寫 ɯ／ɪ 代替 ı 的 2 人。

## 發現的重要資訊

- `deploy_clasp.py` 用 `clasp_deploy/<資料夾名>` 當 quiz id，改頁面名稱時這個資料夾不能跟著改。
- 名單人數不知道，無法判斷有沒有人完全沒作答。
- `_output/private/` 有學生姓名學號，已 gitignore。

## 下次從這裡開始

1. 等使用者跟老師討論 `ch01_太嚴格的判分_2026-10-10.md` 的結果。如果算對：
   - S2-12 的 `alt` 加 `["mis","class","if","ied"]`。
   - `normFill` 把 ɯ、ɪ 換成 i。
   - 重建、push。Sheet 已記錯的列由使用者手動改 correct=1。
2. 構詞樹要不要拿掉 Prefix／Suffix／Circumfix 標籤（等使用者或老師決定）。
3. 沿用 10-08 的待辦：
   - 老師核新題答案。
   - 刪 Z00000000 測試列，兩份新 Sheet 時區改 GMT+08:00。
   - 分析構詞樹 Sheet。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 構詞樹頁 | `ch01-2_morph_tree/morph_tree.src.html`，測試 `ch01-2_morph_tree/tests/`（`test_build_all.py` 結果寫在 `t3_<mode>.log`，不印在 console） |
| 第一周作答匯出 | `_output/private/ch01_2026-10-10.xlsx` |
| 讀 Sheet | Drive 工具 `download_file_content`（exportMimeType 用 xlsx MIME）→ base64 解碼 → openpyxl |

改完 src 跑 `python build_site.py`，再 commit、push。
