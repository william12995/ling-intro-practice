# 上線步驟：GitHub Pages ＋ Google Sheet 記成績

整套分兩個部分。網頁放在 GitHub Pages 上，學生從那裡作答。成績寫進你自己的 Google Sheet，Sheet 前面接一支 Apps Script 負責收資料。

```
學生瀏覽器（docs/ch01_morphology/index.html）
   │  每答一題送一筆（JSONP GET；斷網時先存在瀏覽器，連上後自動補送）
   ▼
Apps Script 網頁應用程式（apps_script/Code.gs）
   ▼
Google Sheet：answers 分頁（每次作答一列）→ 選單「成績 → 重算總表」產生 summary 分頁
```

## 1. 建 Sheet 和後端（約 5 分鐘）

1. 用你的帳號新建一份空白 Google Sheet，取名例如「語言學概論練習成績」。這份 Sheet 會存學生的學號和姓名，**不要開放公開連結**。
2. 在 Sheet 裡按 **擴充功能 → Apps Script**，把 `apps_script/Code.gs` 全文貼上，存檔。
3. 按 **部署 → 新增部署**，類型選 **網頁應用程式**：
   - 執行身分：**我**
   - 具存取權者：**任何人**。選「同網域」的話，學生必須在同一個瀏覽器登入 NTU Google 帳號才送得出去，沒登入的人會一直顯示「上傳中」。NTU 的 Workspace 帳號有可能根本不給「任何人」這個選項，遇到的話改用個人 Gmail 帳號建這份 Sheet 和 Apps Script。
4. 第一次會要求授權存取試算表，同意即可。
5. 複製「網頁應用程式」網址，長得像 `https://script.google.com/macros/s/AKfy…/exec`。
6. 先測後端有沒有活著：把網址直接貼進瀏覽器，應該看到 `callback({"ok":true,"ping":true})`。

2026-09-26 起 `answers` 多了 `reasoning`、`truncated` 兩欄。如果你在這之前已經用舊版測試過、Sheet 裡已經有 `answers` 分頁，先把那個分頁整個刪掉，讓新版重建表頭。

之後如果改了 Code.gs，要用 **部署 → 管理部署 → 編輯 → 版本選「新版本」**，網址才會維持不變。用「新增部署」會產生一個新網址，網頁就得重建。

## 2. 把網址烤進網頁

```
C:\Python313\python.exe build_site.py --endpoint "https://script.google.com/macros/s/AKfy…/exec"
```

會重新產生 `docs/`。頁面右上角應該顯示「成績已記錄」，而不是「成績只存在這台電腦」。

## 3. 放上 GitHub Pages

1. GitHub 開一個 **public** repo（免費帳號的 private repo 不能開 Pages）。例如 `ling-intro-practice`。
2. 把這個資料夾推上去。`.gitignore` 已經排除 `textbook/`，課本 PDF 不會被推上去。
3. repo 的 **Settings → Pages**：Source 選 **Deploy from a branch**，branch 選 `main`、資料夾選 `/docs`。
4. 一兩分鐘後網址會是 `https://<帳號>.github.io/ling-intro-practice/`，第 1 章在 `…/ch01_morphology/`。
5. `docs/.nojekyll` 不要刪。之前台語標註頁遇過，沒有它 GitHub 會用 Jekyll 處理，頁面可能壞掉。

## 4. 上線前自己跑一次

1. 開線上網址，用假學號 `Z00000000`、姓名「測試」登入，答兩三題。其中一題的推理欄貼滿 600 個字元再送出。
2. 回 Sheet 看 `answers` 分頁多出對應的列，`reasoning` 欄有那些字（`truncated` 欄空白代表沒被截短）。推理是用網址送的，中文一個字編碼後佔 9 個字元，這一步就是確認 Google 收得下最長的情況。如果頁面一直顯示「上傳中」，就是網址太長，要把頁面裡的 `WHY_MAX` 調小。
3. 按 Sheet 上方選單 **成績 → 重算總表**，看 `summary` 分頁有這個假學號。第一次用選單會再要求一次授權。
4. 測完把 `answers` 裡的測試列刪掉。

## 5. AI 回饋（預設關閉）

學生送出一題後，頁面另外呼叫後端的 `action=feedback`，後端把題目、標準答案、解說和學生的答案與推理送給 Gemini，回饋顯示在解說下面，同時寫進 Sheet 的 `feedback` 分頁。回饋失敗或變慢都不影響 `answers` 的作答紀錄。送給 Gemini 的內容不含學號和姓名。

開啟前要先做到：

1. 老師同意。免費版 Gemini 的條款寫明輸入內容會被 Google 拿去改進產品，頁面上已經告訴學生推理會送到 Google Gemini。
2. 39 題的標準答案核過。回饋是照標準答案寫的，答案錯了回饋也會跟著錯。

設定步驟：

1. 用 rino881209@gmail.com 到 https://aistudio.google.com/apikey 建一把金鑰。所屬的 Google Cloud 專案不要綁帳單，綁了就不是免費版，會被收費。
2. 到 https://aistudio.google.com/rate-limit 看這把金鑰每個模型的每分鐘和每日上限，挑全班同時作答撐得住的。
3. 打開 Apps Script 編輯器 → 專案設定 → 指令碼屬性，加：
   - `GEMINI_FREE_KEY`：上面那把金鑰
   - `FEEDBACK_MODELS`（選填）：依序嘗試的模型，逗號分隔，預設 `gemini-3.8-flash,gemini-3.5-flash-lite`。遇到 503（免費版常見的「需求過高」）先重試一次，還不行或 429（額度用完）就換下一個。只支援 Gemini 系列，Gemma 試過不能用。
   - `GEMINI_PAID_KEY`（選填）：免費的全部失敗才用，會收費。
4. 在編輯器裡選 `testFeedback` 執行一次（appsscript.json 要明列 `oauthScopes`，否則編輯器不會跳授權，UrlFetchApp 會直接報沒權限；2026-09-26 踩過）。它會把 `FEEDBACK_MODELS` 裡每個模型各跑四個案例，每行開頭標模型名稱和 OK/FAIL；FAIL 後面是 Google 回的錯誤訊息。第一次會要求「連線到外部服務」的授權，這是新加的權限，要按同意，不然網頁版也呼叫不了 Gemini。執行紀錄會印出四個測試案例的回饋，重點看第 2 個：答案對但推理錯，模型要能指出推理的問題，不能只附和標準答案。
5. 都沒問題再加 `FEEDBACK_ON` = `true`。改屬性不用重新部署，頁面重新整理就會生效。要關掉就把它改成別的值。

`feedback` 分頁的欄位：`disagree` 是學生按了「I disagree with this feedback」（`disagree_note` 是學生寫的理由），`ta_check`、`ta_note` 留給助教抽查時填。建議優先看三種：學生不同意的、答案對但回饋說推理有問題的、申論題。每個學號每分鐘最多 8 次回饋，擋住有人拿後端網址當免費聊天機器人。

## 成績怎麼算

- `answers` 每次作答都留一列，不覆蓋。學生按「重新作答」會開新的 attempt，舊的紀錄還在。
- `summary` 的「首次答對」看的是每題最早那一次作答，「最佳答對」看的是每題有沒有任何一次答對。要拿哪一個當成績由老師決定。
- 學號格式限定一個英文字母加 8 位數字，前後端都會擋。
- 每題學生要先作答、再寫推理過程（至少 20 個字元，最多 600 個字元；頁面改成英文後放寬），按「送出」後才判分和顯示解說，送出後兩欄都鎖住。系統只判答案，推理存在 `reasoning` 欄給老師抽查。
- 第 7 部分（習題 5 申論）不計分，`correct` 欄留白，只算進「已作答題數」。
- 題號（`S1-01`、`S5-07`）是照題目順序編的。學生開始作答之後，不要調換或替換既有題目，新題目只加在最後，不然 Sheet 裡同一個題號會對到不同的題目。
- 網路重送偶爾會讓 `answers` 出現重複的列（同一個 event_id），重算總表時只算一次，不用手動刪。

## 限制

- 答案寫在網頁原始碼裡，懂得看原始碼的學生查得到。後端網址也在原始碼裡，理論上有人可以偽造紀錄。這套適合練習和參與分數，不適合當正式考試。
- 學生換電腦或清掉瀏覽器資料，頁面上的進度會從頭開始，但 Sheet 裡的紀錄不受影響，首次作答仍以最早那筆為準。
- 姓名是學生自己填的，對照點名單時以學號為準。
