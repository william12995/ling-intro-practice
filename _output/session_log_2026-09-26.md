# 工作紀錄 — 2026-09-26

這個資料夾今天建立，從 `ENG_Pragmatic` 那邊開 session 做的。

## 本次完成事項

- 建了 `Ling-Intro-TA` 資料夾，並列入全域 CLAUDE.md 的資產地圖。課本 PDF 從 `ENG_Pragmatic/_output/` 搬到 `textbook/`。
- 做了 Ch.1 Morphology 互動練習頁 `ch01_morphology/morphology_lab.src.html`：第一部分 20 題課本範例；第二部分四關切詞，共 29 題（7+7+7+8）。
- 使用者要求拿掉給老師看的說明文字（footer 的出處註記、開頭導言），已經拿掉。規則寫進本資料夾的 CLAUDE.md。
- 加了成績記錄：學生填學號姓名後，每答一題送一筆 JSONP 到 Apps Script，寫進 Google Sheet。後端在 `apps_script/Code.gs`（append-only，不加鎖；重算總表時去重，首次作答依 server_time 判定）。`build_site.py` 產生 `docs/` 給 GitHub Pages 用。部署手冊在 `DEPLOY.md`。
- 本機 git repo 已 commit（`main`，作者 rino881209@gmail.com），還沒推上 GitHub。`.gitignore` 排除 `textbook/`。

## 下次從這裡開始（使用者說明天要用）

1. 使用者照 `DEPLOY.md` 第 1 步建 Sheet、貼 Code.gs、部署，把 `/exec` 網址給我。
2. 跑 `C:\Python313\python.exe build_site.py --endpoint "<網址>"`，commit。
3. 使用者跑 `! gh auth login`。確認 repo 名稱（建議 `ling-intro-practice`，必須 public）和要不要把 CLAUDE.md 加進 .gitignore，然後建 repo、push、Settings → Pages 選 main /docs。
4. 照 DEPLOY.md 第 4 步用假學號 `Z00000000` 測完整流程：頁面顯示「成績已記錄」，answers 有列，「成績 → 重算總表」產生 summary。測完刪掉測試列。
5. 老師要決定用「首次答對」還是「最佳答對」當成績。

## 還沒驗證

Apps Script 沒實際跑過，JSONP 寫進 Sheet 沒測過，登入畫面沒在瀏覽器看過。只跑過兩支程式的 `node --check`。

## 環境備忘

| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 課本 | `textbook/An_Introduction_to_Language.pdf`（9th ed.，PDF 頁 = 印刷頁 + 20） |
| 預覽 artifact | https://claude.ai/artifact/NxGDg4swf7XuwU4kNLLs93 （私人；連不到 Google，只能預覽，不要發給學生） |
| gh | 尚未登入 |

重建網頁：

```
C:\Python313\python.exe build_site.py --endpoint "https://script.google.com/macros/s/XXXX/exec"
```

## 補記二（同日，在 ENG_Pragmatic 的 session 裡代做）

老師來信改規則：Fromkin 習題太難又有版權問題，題目改從開源課本 *Essentials of Linguistics* 2nd ed.（CC BY-NC-SA 4.0，`textbook/Essentials-of-Linguistics-2nd-edition.pdf`）的 Morphology 習題出，先放固定答案的觀念題，再加難到陌生語言解題。每題要兩欄：固定答案（系統判）和推理過程（只存，抽查用）。

- 當時還沒有學生作答，`ch01_morphology/morphology_lab.src.html` 整頁換掉。舊的 Fromkin 版在 commit `be842ae`。
- 新版 39 題，7 部分：習題 3 詞綴類型(8)、習題 4 詞類(10+切詞 3)、習題 6 複合詞複選(4)、習題 7 希伯來文(2)、習題 1 土耳其文(6+填空 1)、習題 2 海地克里奧爾語(4)、習題 5 申論(1，不計分)。
- 流程：先作答、寫推理（5–300 字），按送出才判分和顯示解說，送出後鎖住。推理存到 Sheet 的 `reasoning` 欄。
- `Code.gs` 的 HEADER 最後加了 `reasoning`、`truncated`，summary 的分區改成 S1–S6。`DEPLOY.md` 的上線測試多一步：貼 300 個中文字的推理，確認 Google 收得到。
- 自我測試：39 題的標準答案丟進判分函式全部判對；土耳其文填空接受 c/j/dj 代替 dʒ、i 代替 ı。無頭 Edge 截圖確認作答與送出後的畫面。
- 沒做：標準答案沒有人核過（課本沒附解答）；claude.ai artifact 預覽還是舊版；沒 commit；`docs/` 還沒推上 GitHub。

下次：請使用者或老師核對答案 → Apps Script 用「管理部署 → 新版本」更新（如果已有舊的 answers 分頁要先刪）→ 跑 DEPLOY.md 的上線測試 → commit、推 GitHub Pages。

## 補記三：Apps Script 首次部署（clasp）

- clasp 3.4.1 裝在全域，登入帳號 rino881209@gmail.com（個人 Gmail）。
- Sheet：https://drive.google.com/open?id=1doD3tRlHDfJ8zRIMcppIHKwF6rXbx9swWlcf79sYnGw （標題「語言學概論練習成績」，不要開公開連結）
- 綁定的 script：https://script.google.com/d/1gN8mqyFxAeyF8Xsa1yZLOa1MRELmghHQFK9QMXoQJw711C5VhtsI_3kE/edit ，本機設定在 `.clasp.json`（rootDir = apps_script）。
- `apps_script/appsscript.json`：時區 Asia/Taipei，webapp 執行身分 = 部署者、存取 = 任何人（匿名）。注意 `clasp create` 會把這檔蓋回預設值，重建專案時要再改回來。
- 部署 @1：AKfycbzlAf829w4jB1icEHwgIWH65hKQA3NKtYW0TiS40NTBqcW3eZnuFW1kSfHOk5czmtuzsw，網址 https://script.google.com/macros/s/AKfycbzlAf829w4jB1icEHwgIWH65hKQA3NKtYW0TiS40NTBqcW3eZnuFW1kSfHOk5czmtuzsw/exec
- 之後改 Code.gs：`clasp push` 後 `clasp create-deployment --deploymentId <上面那串> --description ...` 更新同一個部署，網址不變。
- 部署當下打網址回傳的是 Google 授權頁，還沒授權。docs/ 還沒用這個網址重建（自動權限擋下，交給使用者自己跑）。
- 更新：使用者已授權（ping 回 ok）。用 curl 送了兩筆 Z00000000 測試資料（S1-01 短推理、S1-02 推理 300 個中文字，網址 3380 字元），都回 ok。docs/ 已用 @1 網址重建，無頭 Edge 從網頁送一筆 S1-03，佇列清空、畫面顯示「成績已記錄」。Sheet 的 answers 分頁有三列 Z00000000 測試資料，上線前要刪。
- 還沒做：commit、推 GitHub Pages（gh 未登入）、標準答案人工核對。
- 已上線：repo https://github.com/william12995/ling-intro-practice （public，gh 帳號 william12995），Pages 從 main /docs 發布。學生網址 https://william12995.github.io/ling-intro-practice/ch01_morphology/ ，線上版確認有後端網址與授權頁尾。
- 上線前待辦：刪掉 Sheet answers 裡 3 列 Z00000000 測試資料；標準答案人工核對。改題目後要 build_site.py（帶網址）→ commit → push，Pages 會自動更新。
