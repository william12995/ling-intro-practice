# 工作紀錄 — 2026-10-08

## 本次完成事項

三件事都上線了（commit `5617483`、`718312d`、`08695ae`、之後一筆是構詞樹加題）。

句法頁 `ch02_syntax/tree_lab.src.html` 加 S1-05～S1-09（10-04 會議）：
- 三題課堂基礎句，只用 Appendix C rule 1–10：Every girl read some poetry（part 2 練習 1）、A hyena laughed at me（slide 6）、The girl may cry（slide 16）。
- I saw the man with the telescope 兩題，各附一個意思：the man has the telescope（N' → N' PP，rule 17）、I used the telescope to see the man（V' → V' PP，rule 16），照 part 2 slide 17。
- 從構詞樹頁搬了 `it.mean`：題目寫出要畫哪個意思，送 Sheet 的 prompt 帶括號意思。
- 頁尾改成 "Some sentences adapted from…"，因為有題目來自老師簡報。
- 「少放 X-bar」我解讀成只用基礎規則、仍畫完整 bar 層級（簡報說考試用 X-bar）。這是解讀，要跟老師確認。

ch01 切詞題 prompt bug（S2-11～13）：題目可以有自己的 `note`，蓋過整節的 note，畫面提示和送 Gemini 的說明都用它。修在前端，後端沒重新部署。用瀏覽器攔請求確認送出的 note 對了；沒有實際打 Gemini（避免在學生 Sheet 留測試列）。

構詞樹頁 `ch03_morph_tree/morph_tree.src.html` 加 S1-15～S1-24，全部出自開源課本：
- foolishly、librarianship、expectantly（後綴）、unluckiness（前後綴，解說對照 Tagalog 中綴 -um-）、nieces、newest（屈折）、Turkish evdʒıklerimizde（習題 1）、Japanese tabesaserareta（5.3）、Meskwaki neta·nesaki（前後綴，兩種順序都算對）、neta·nesena·naki（環綴 ne- … -ena·n，三個子節點同一層）。
- 外語題題目下多一行語素註解（`it.gl`）。
- 標籤盤加 Prefix、Suffix、Circumfix。標 Affix 一律照舊算對；標種類時要跟位置對（從標準答案推：兩個子節點左 Prefix 右 Suffix，三個子節點頭尾 Circumfix），標錯算錯。標準答案仍寫 Affix，S1-01～14 沒動。送 Sheet 的括號保留學生原本的標籤。
- 中綴、同時詞綴、內部變化、異幹不出題：樹的底部要能照順序讀出詞素，中綴會把詞根切開。

測試：句法 build-all 滑鼠 40、觸控 40，tap、review、record 都 0 失敗；構詞樹 build-all 滑鼠 62、觸控 62，tap、record 都 0 失敗。新增測試：舊進度（句法 5 題、構詞樹 15 題）讀得回來、歧義題 prompt 帶意思、詞綴種類四種情況（Prefix 對、Suffix 錯、Circumfix 錯、Affix 對）和環綴。兩頁線上版都確認已更新。

## 發現的重要資訊

- 測試腳本的坑：手機寬 390 時，8 個詞的句子拖曳兩端不在同一畫面，`into_view(target)` 會把來源捲出去。兩頁的 `test_build_all.py` 都加了 `both_in_view`（只在兩端都在畫布上時捲到中點）。選擇器裡有 `V'` 的單引號，要用 `json.dumps` 包。
- `python -I` 會讓使用者 site-packages 的 playwright 找不到，自己寫的測試腳本不要加 `-I`。
- 開源課本 5.2 Meskwaki 例子內文寫 ni-、例句寫 ne-，頁面一律用 ne-。
- 使用者學號 R13142001，分析學生作答時排除（已存記憶）。

## 下次從這裡開始

1. 請老師核：句法 S1-05～09、構詞樹 S1-15～24 的標準答案；「少放 X-bar」的解讀；構詞樹加 Prefix／Suffix／Circumfix 標籤可不可以（老師投影片只用 Affix）；telescope 的 N' → N PP 要不要也算對。
2. 三份 Sheet 的 Z00000000 測試列請使用者刪；句法、構詞樹兩份 Sheet 時區改 GMT+08:00。
3. 構詞樹作答資料還沒看（匯出 Sheet 看哪題錯最多，排除 R13142001、Z00000000、B20260101）。
4. 構詞樹、句法都沒接 AI 回饋（後端預設關）。
5. 舊待辦：rate-limit 數字、summary 加推理長度欄、空的 Claude Docs 要不要刪（`session_log_2026-09-26-3.md`）。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 句法頁 | `ch02_syntax/tree_lab.src.html`，測試 `ch02_syntax/tests/` |
| 構詞樹頁 | `ch03_morph_tree/morph_tree.src.html`，測試 `ch03_morph_tree/tests/` |
| 切詞頁 | `ch01_morphology/morphology_lab.src.html`（沒有自動測試） |
| 開源課本抽文字 | `pdftotext -enc UTF-8 -f 229 -l 276 textbook/Essentials-of-Linguistics-2nd-edition.pdf out.txt`（Ch.5） |
| 老師簡報文字 | 解壓 `_output/drive-download-…zip`，用 zipfile 讀 `ppt/slides/slide*.xml` 的 `<a:t>` |

重跑測試（在各頁的 `tests/` 底下）：
```
set PYTHONIOENCODING=utf-8
python test_build_all.py mouse
python test_build_all.py touch
python test_tap_mode.py
python test_record_and_ux.py
```
（句法頁另有 `test_review_fixes.py`）。改完 src 跑 `python build_site.py`，再 commit、push。
