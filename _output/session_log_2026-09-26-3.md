# 工作紀錄 — 2026-09-26（第三次）

## 本次完成事項

**頁面全英文。** 老師要求（外文系）。`ch01_morphology/morphology_lab.src.html` 裡學生看得到的文字全部換成英文：39 題的題目、選項、解說，還有按鈕、登入畫面、頁尾出處。`build_site.py` 的 `lang` 改成 `en`，首頁也改成英文。題號、順序和判分邏輯都沒動，39 題的標準答案丟進判分函式仍然全部判對。推理欄長度從 5–300 字改成 20–600 字元，因為原本的長度是照中文訂的。Code.gs 和 Sheet 欄名維持中文。commit `737da98`。

**AI 回饋上線，`FEEDBACK_ON` 目前是開著的。**
- 流程：學生送出一題，頁面先照常呼叫 `record()`，另外再發 `action=feedback`。Apps Script 把題目、標準答案、解說、學生的答案和推理送給 Gemini，把回饋寫進新的 `feedback` 分頁，再傳回頁面。回饋失敗或變慢都不影響 `answers`。
- 送給 Gemini 的資料不含學號和姓名。送出前，推理欄下面會告知推理會送到 Google Gemini。每則回饋固定附一句英文：回饋是 AI 寫的、僅供參考，頁面上的標準答案也是 AI 協助起草的。這句寫死在頁面上，不靠模型產生。
- 學生可以按「I disagree with this feedback」並寫理由，會記在 `feedback` 分頁的 `disagree` 和 `disagree_note` 欄。另外留了 `ta_check`、`ta_note` 兩欄給助教抽查時填。
- 模型：先用 `gemini-3.8-flash`，失敗就改用 `gemini-3.5-flash-lite`。遇到 503 先等 1.5 秒重試一次，429 就直接換下一個模型。模型回的 markdown 星號會先去掉。每個學號每分鐘最多 8 次。
- 設定放在 Script Properties：`GEMINI_FREE_KEY`（使用者用 rino881209 建的免費金鑰，已設好）、`FEEDBACK_ON`（已設 true）、`FEEDBACK_MODELS`（沒設，用預設）、`GEMINI_PAID_KEY`（沒設）。
- `action=config` 會回報 `missing`，列出哪一項沒設好，不會回傳金鑰本身。
- Apps Script 部署更新到 @7，網址沒變。
- 相關 commit：`0c47cc6`、`bf634c0`、`227abaf`、`8b6832f`、`c53cb81`。

**說明書。** `_output/使用說明_老師.md`（中文，給高老師，含給分建議和三件待老師決定的事）、`_output/User_Guide_Students.md`（英文，給學生）。學生版之後使用者自己潤過稿，還加了 marp 開頭。commit `aa49915`。

## 驗證過的

- 用免費金鑰在本機直接呼叫 API，四種案例都測了：答案對推理也對、答案對推理錯、答案錯、申論。`gemini-3.8-flash` 的回饋最好，「答案對、推理錯」那題明確指出「英文後綴不一定是衍生」。`3.5-flash-lite` 很快，但土耳其文那題把 -imiz 講錯了。`3.1-flash-lite` 要 6–16 秒。`gemma-4-31b-it` 預設會思考，32 秒後把 token 用光還沒產出文字，所以不用。
- 使用者在編輯器跑了 `testFeedback`，兩個模型各跑四個案例，八則都 OK。
- 用無頭 Edge 跑正式網址，假學號 `Z00000000`，寬度 390px：送出前看得到告知 → 作答有記錄 → 6.9 秒後出現回饋 → 按不同意，後端回報成功。後端要先找到那筆回饋才會回成功，所以這也證明 `feedback` 分頁確實有寫進去。
- 模擬後端回應測過：回饋關閉，或 config 請求失敗時，不會出現 AI 框，也不會送出回饋請求。回饋文字用 textContent 放進頁面，模型回傳的 HTML 不會被執行。
- Google 收得下 9,000 字元的 GET 網址，12,000 會回 400。最長的回饋請求約 8,100 字元，頁面超過 8,500 會先截短解說，再截推理。

## 發現的重要資訊

- NVIDIA build.nvidia.com 的免費版條款只准內部測試和評估，服務真實使用者不行，所以沒用。
- ENG_Pragmatic 的 `.env` 裡有 `GEMINI_API_KEY`，但那個專案的帳單是另一位老師綁的，用了會花那個帳戶的錢。所以沒拿來測試，也沒設成付費備援。
- appsscript.json 沒有明列 `oauthScopes` 時，編輯器不會跳出 `script.external_request` 的授權，UrlFetchApp 直接報沒有權限。現在已經明列三個 scope。改了 manifest 之後，`clasp push` 會回「Skipping push」，要加 `--force` 才推得上去。
- `clasp logs` 要另外綁 GCP 專案，目前讀不到執行紀錄，只能請使用者從編輯器複製。
- Gemini 免費版的每分鐘和每日上限還不知道。使用者要到 https://aistudio.google.com/rate-limit 看。粗估全班 50 人做完一輪約 1,950 次呼叫，課堂上同時作答時尖峰每分鐘 50–100 次。
- 免費金鑰出現在這次的對話紀錄裡，要不要作廢重建由使用者決定。

## 下次從這裡開始

1. 使用者自己在線上網站把 39 題做一遍，藉此核對標準答案和解說，不用整份重寫，也不用匯出表格。發現有問題的題目，直接改 src 的 `SECTIONS` 陣列再重建。學生還沒開始作答，所以題目可以自由改，題號順序也能動。測試用 `Z` 開頭的學號，之後才好找出來刪。
2. 把 rate-limit 頁面的 RPM 和 RPD 數字拿到手。如果不夠，從這三條路選一條：改成學生按了才產生回饋、只對答錯的題和申論題自動回饋、接付費備援。
3. 請老師決定三件事（說明書最後一節）：同不同意推理送到 Google 免費版、成績算法和比例、要不要明講 AI 回饋不算分。老師不同意的話，把 `FEEDBACK_ON` 改成 `false` 就能關掉。
4. 刪掉 Sheet 裡的測試資料：`answers` 所有 `Z00000000` 的列（之前三筆、「redeploy test」、「AI feedback test」），`feedback` 所有 `Z00000000` 的列。
5. 待使用者決定的功能：失敗的回饋呼叫也寫進 `feedback` 分頁，用來看實際用量；`summary` 加推理平均長度和短推理題數兩欄，讓助教快速找出敷衍的人。
6. claude.ai 上有一份只有大綱的 Claude Docs 空文件（https://claude.ai/code/artifact/a36a9cb1-677f-407f-b242-b2151f01bf66），使用者說要的話就刪。
7. 把網址發給學生（NTU COOL）之前，1–4 都要先處理完。

## 環境備忘

| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 學生網址 | https://william12995.github.io/ling-intro-practice/ch01_morphology/ |
| Apps Script 編輯器 | https://script.google.com/d/1gN8mqyFxAeyF8Xsa1yZLOa1MRELmghHQFK9QMXoQJw711C5VhtsI_3kE/edit |
| 部署 | `AKfycbzlAf829w4jB1icEHwgIWH65hKQA3NKtYW0TiS40NTBqcW3eZnuFW1kSfHOk5czmtuzsw`，目前 @7 |
| Playwright | 已裝，`chromium.launch(channel="msedge")` 可用 |
| 回饋設定說明 | `DEPLOY.md` 第 5 節 |

改題目後重建並上線：

```
C:\Python313\python.exe build_site.py --endpoint "https://script.google.com/macros/s/AKfycbzlAf829w4jB1icEHwgIWH65hKQA3NKtYW0TiS40NTBqcW3eZnuFW1kSfHOk5czmtuzsw/exec"
git add -A && git commit -m "..." && git push
```

改 Code.gs 或 appsscript.json 後：

```
clasp push --force
clasp create-deployment --deploymentId AKfycbzlAf829w4jB1icEHwgIWH65hKQA3NKtYW0TiS40NTBqcW3eZnuFW1kSfHOk5czmtuzsw --description "..."
```

查後端設定狀態：用 GET 呼叫 `<部署網址>?callback=cb&data={"action":"config"}`（data 要 URL encode），回傳 `feedback` 是否開啟，以及 `missing` 列出哪些設定還沒設。
