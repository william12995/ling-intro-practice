# 工作紀錄 — 2026-10-03（第二次）

## 本次完成事項

句法頁上線了：https://william12995.github.io/ling-intro-practice/ch02_syntax/ ，首頁也有連結。

- 用 clasp 建了句法的成績 Sheet「語言學概論 句法練習成績」（帳號 rino881209@gmail.com，https://docs.google.com/spreadsheets/d/1DM6D84b5SGCnGUVc3rF1KCN2opY3SY_fo23nGISZRJY/edit ），推上 Code.gs，部署成網頁應用程式。使用者只做了一次授權（開 /exec 網址按允許）。
- clasp 設定放在 `clasp_deploy/ch02_syntax/`（`.clasp.json`、`deployment.txt` 存部署 id）。以後改後端跑 `python clasp_deploy/deploy_clasp.py ch02_syntax`，會重新產生 `src/`、push、更新同一個部署，網址不變。
- 「這份 Sheet 只收 ch02」不用設指令碼屬性：`Code.gs` 的 `quizzes_()` 改成沒有 `QUIZZES` 時看 `DEFAULT_QUIZZES`（clasp 推送時帶的 `config.gs` 定義），都沒有才是 ch01。構詞那份沒重新部署。
- `build_site.py --endpoint ch02_syntax=…` 的後端檢查通過（回 `quizzes: ["ch02_syntax"]`），重建、push（`092d23b`）。
- 用建好的頁面（不 mock）以 `Z00000000` 實際送了 S1-01，頁面顯示 Answers recorded，用 Drive 工具讀 Sheet 確認 answers 第 2 列有這筆，括號、推理、題號都對。
- DEPLOY.md 第 6 節改成 clasp 的做法，手動步驟留作備案；CLAUDE.md 表格和「新增章節」說明更新。

- 看了構詞 Sheet 的作答（Drive 匯出 xlsx 分析）：17 位學生、442 筆、每筆一則 AI 回饋。逐人、逐題數字和錯誤答案＋AI 回饋全文在 `_output/private/`（有姓名學號，已 gitignore）。
- 老師要一份「學生答案＋AI 參考答案＋人工加註來提高 AI 批改正確率」的規劃，寫成 Claude Docs：https://claude.ai/code/artifact/42866cb1-4aa1-4b21-8021-099dc096e00d （私人，要分享給老師得從頁面的 Share 選單開）。

## 發現的重要資訊

- AI 回饋的程式錯誤：第 2 節的切詞題（S2-11～13）送給 Gemini 的說明是整節共用的「判斷詞類」，AI 至少 6 次責怪學生沒答詞類。`buildPrompt_` 的 `it.note` 來自 section note，要改成每題自己的說明。還沒修。
- 首次正確率最低：S2-12 misclassified 2/9（多數切成 mis + classifi + ed）、S3-02 2/5（漏 grammar teacher）、S4-02、S5-06、S5-07 都是 4/7。

- repo 根目錄本來就有 `.clasp.json`，是構詞那份 Sheet（rootDir=`apps_script`，會推整個資料夾含子資料夾）。別章的檔案放進 `apps_script/` 會被推到構詞專案，所以句法的放在 `clasp_deploy/`。
- clasp 3.4.1 的指令名稱：`create-script`、`create-deployment`、`update-deployment`。`create-script` 會從上層找 `.clasp.json`，要加 `-P .`；建完會把雲端預設的 appsscript.json 拉下來蓋掉本地，要再複製一次才 push。
- 部署完、擁有者授權前，/exec 回的是 Google 授權頁，不是 JSONP。
- 新 Sheet 的時區不是台北：測試列 server_time 顯示「上午 6:21」，實際是台北 21:21。client_time 是 UTC ISO，不受影響。

## 下次從這裡開始

0. 修上面那個切詞題的 prompt 錯誤（老師規劃第 1 步，不需要等決定）；等老師回覆規劃裡的四個待決定事項。
1. 測試列（answers 第 2 列，學號 Z00000000、姓名 TEST-delete-me）要刪掉，我沒有刪 Sheet 列的工具，已請使用者手動刪。下次先確認刪了沒。
2. Sheet 時區改成台北：檔案 → 設定 → 時區 GMT+08:00 台北（使用者自己改，或之後在 Code.gs 加一次性函式）。
3. 請老師核標準答案和記法（同 10-02 待辦）。
4. 加題（只能加在 ITEMS 最後）：Every girl read some poetry、A hyena laughed at me、PP/AdvP 附加語、歧義句。
5. ch01 的舊待辦還在（`session_log_2026-09-26-3.md`）。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| clasp | 3.4.1，登入 rino881209@gmail.com |
| 句法後端 | `clasp_deploy/ch02_syntax/`，部署 id 在 `deployment.txt` |
| 構詞後端 | 根目錄 `.clasp.json`（rootDir=apps_script） |
| 每章網址 | `endpoints.json` |
| 構詞成績 Sheet | `1doD3tRlHDfJ8zRIMcppIHKwF6rXbx9swWlcf79sYnGw`（answers、feedback 兩個分頁，沒有 summary 分頁） |
| 讀成績 | Drive 工具 `download_file_content` 匯出 xlsx（read_file_content 只給前十幾列），再用 openpyxl 讀；以 event_id 去重，排除 Z00000000、B20260101、R13142001（使用者自己）。分析腳本沒留，結果在 `_output/private/` |
| 改善規劃 | Claude Docs https://claude.ai/code/artifact/42866cb1-4aa1-4b21-8021-099dc096e00d |

改後端並更新部署：
```
python clasp_deploy/deploy_clasp.py ch02_syntax
```
重建網頁：
```
python build_site.py
```
