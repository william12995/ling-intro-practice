# 語言學概論助教課

使用者 2026-09 起擔任老師的語言學概論助教。這個資料夾放課程教材與互動網頁，跟碩論研究無關，研究的東西不要寫進來。

## 課本

`textbook/An_Introduction_to_Language.pdf`：Fromkin, Rodman & Hyams, *An Introduction to Language*, 9th ed., 2011。

- PDF 頁碼 = 印刷頁碼 + 20。頁面上引用一律用印刷頁碼。
- 章節（PDF 頁）：Intro Brain and Language 23；1 Morphology 56–96；2 Syntax 97；3 Meaning 159；4 Phonetics 209；5 Phonology 246；6 What Is Language 304；7 Acquisition 344；8 Processing 395；9 Language in Society 450；10 Language Change 508。
- console 是 cp950，抽 PDF 文字要寫成 UTF-8 檔再讀。

## 已做的教材

| 章 | 原始檔 | 上線版 |
|---|---|---|
| Ch.1 Morphology | `ch01_morphology/morphology_lab.src.html` | `docs/ch01_morphology/index.html`（GitHub Pages，尚未推上去） |

只改 `*.src.html`，改完跑 `python build_site.py --endpoint "<Apps Script 網址>"` 重建 `docs/`，`docs/` 不要手改。src 沒有 doctype/head，是因為它同時可以直接發布成 claude.ai artifact 當預覽（https://claude.ai/artifact/NxGDg4swf7XuwU4kNLLs93 ，私人；更新時帶這個 URL 當 `url`）。artifact 裡連不到 Google，成績只會存在瀏覽器。

成績記錄：學生先填學號姓名，每答一題送一筆到 Google Sheet（`apps_script/Code.gs`）。部署步驟和成績算法在 `DEPLOY.md`。新增章節時要做三件事：`build_site.py` 的 `PAGES` 加一列、Code.gs 的 `QUIZZES` 加 quiz id、新頁面的 `QUIZ_ID` 要跟它一致。

題號是照陣列位置編的（`A01`、`B2-05`），學生開始作答後不能調換或替換既有題目，只能在最後加。

`.gitignore` 排除 `textbook/`，課本有版權，不能推上 public repo。

## 慣例

- 老師的要求：先用課本章節內文範例做互動答題，再由簡入深出題。
- 章末習題不放進互動頁，留給作業用。
- 答案有爭議的題目（例如 receive 要不要切出 -ceive）兩種都算對，在解說裡講清楚，不要硬判。
- 同一份頁面裡的判準要一致：前面教過的概念（例如黏著詞根），後面的題目不能反過來扣分。
- 頁面上不放給老師或助教看的說明（出處註記、出題設計理由、「本頁包含什麼」這類導言）。學生只需要題目、操作提示和解說。使用者 2026-09-26 明確要求拿掉。
