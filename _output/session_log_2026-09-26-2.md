# 工作紀錄 — 2026-09-26（第二次）

這次是在 `ENG_Pragmatic` 的 session 裡代做的，因為使用者當時人在那邊。

## 本次完成事項

**老師來信改規則，題目整頁換掉。** 老師說 Fromkin 的習題太難，又有版權問題，改用開源課本 *Essentials of Linguistics* 2nd ed.（Anderson 等人，eCampusOntario，CC BY-NC-SA 4.0）出題。先放答案固定的觀念題，再加難到陌生語言解題。每題要有兩欄：固定答案（系統判）和推理過程（只存，給老師抽查「答案對、推理錯」）。推理最後怎麼處理，老師說之後再討論。

- 當時還沒有學生作答，`ch01_morphology/morphology_lab.src.html` 整頁換掉。舊的 Fromkin 版在 commit `be842ae`。
- 新版 39 題，分 7 部分，照課本 §5.12 的習題編號：習題 3 詞綴類型（8）、習題 4 詞類（10，加切詞 3）、習題 6 複合詞複選（4）、習題 7 希伯來文（2）、習題 1 土耳其文（6，加填空 1）、習題 2 海地克里奧爾語（4）、習題 5 申論（1，不計分）。
- 流程：先作答、寫推理（5–300 字），按送出才判分、顯示解說，送出後兩欄都鎖住。沒有這個順序，學生會照抄解說去補推理。
- 土耳其文填空接受 c、j、dj 代替 dʒ，i 代替 ı。有爭議的選項（習題 6 的 something、rubber end）選不選都算對。
- 頁尾一行開源課本的出處和授權，是 CC BY-NC-SA 的要求。
- `apps_script/Code.gs`：HEADER 最後加 `reasoning`、`truncated`，summary 分區改成 S1–S6，`correct` 空白的題目（申論）只算已作答。
- `DEPLOY.md`、`CLAUDE.md` 跟著改：新課本、頁碼對照、「章末習題不放」那條作廢、頁尾出處例外。

**後端部署（clasp）。**
- clasp 3.4.1 裝在全域，登入 rino881209@gmail.com（個人 Gmail，NTU 帳號可能不給「任何人」存取）。
- Sheet「語言學概論練習成績」：https://drive.google.com/open?id=1doD3tRlHDfJ8zRIMcppIHKwF6rXbx9swWlcf79sYnGw （沒開公開連結）
- 綁定的 script：https://script.google.com/d/1gN8mqyFxAeyF8Xsa1yZLOa1MRELmghHQFK9QMXoQJw711C5VhtsI_3kE/edit ，本機設定在 `.clasp.json`（rootDir = apps_script）。
- 部署 @1 網址：https://script.google.com/macros/s/AKfycbzlAf829w4jB1icEHwgIWH65hKQA3NKtYW0TiS40NTBqcW3eZnuFW1kSfHOk5czmtuzsw/exec ，使用者已授權，ping 回 ok。

**上線。**
- repo：https://github.com/william12995/ling-intro-practice （public，gh 帳號 william12995），Pages 從 main 的 /docs 發布。
- 學生網址：https://william12995.github.io/ling-intro-practice/ch01_morphology/
- commit：`b727940`（題目與後端）、`0325af0`（紀錄）。

## 驗證過的

- 39 題的標準答案丟進判分函式，全部判對；填空的各種打法判對，錯的順序判錯。
- curl 送兩筆測試資料，其中一筆推理 300 個中文字（網址 3380 字元），Google 照收。
- 無頭 Edge 從重建後的網頁送一筆，佇列清空，顯示「成績已記錄」。
- 線上版有後端網址和授權頁尾，600px 寬版面正常。更窄的手機寬度沒測到（無頭瀏覽器最窄約 500px）。

## 發現的重要資訊

- 課本 PDF 頁 = 印刷頁 + 20。Ch.5 在 PDF 229–276，習題 5.12 在 PDF 272–274。PDF 版拿掉了章內的 Check your understanding 互動題。
- 課本沒附解答，39 題的標準答案都是 AI 寫的。
- `clasp create` 會把 `appsscript.json` 蓋回預設（時區紐約、沒有 webapp 設定），重建專案時要改回來。
- 自動權限模式會擋「把外部網址換進網頁」和「建立 public repo」，這兩步要使用者明講才執行。

## 下次從這裡開始

1. 刪掉 Sheet `answers` 分頁裡 3 列 `Z00000000` 測試資料。
2. 請使用者或老師核對 39 題的標準答案。有錯就改 src，照下面的指令重建、push。題號照陣列位置編，學生開始作答後只能在最後加題。
3. 用手機開一次學生網址，確認窄螢幕版面。
4. 把網址給學生（NTU COOL 或課堂上）。
5. 之後的章節：`build_site.py` 的 `PAGES` 加一列、Code.gs 的 `QUIZZES` 加 quiz id、新頁面的 `QUIZ_ID` 要一致，Code.gs 的 `SECS` 也要對上新頁的分區。

## 環境備忘

| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 出題課本 | `textbook/Essentials-of-Linguistics-2nd-edition.pdf`（PDF 頁 = 印刷頁 + 20） |
| clasp | 全域 3.4.1，帳號 rino881209@gmail.com |
| gh | 已登入 william12995 |
| 預覽 artifact | https://claude.ai/artifact/NxGDg4swf7XuwU4kNLLs93 ，還是舊的 Fromkin 版，不要給學生 |

改題目後重建並上線：

```
C:\Python313\python.exe build_site.py --endpoint "https://script.google.com/macros/s/AKfycbzlAf829w4jB1icEHwgIWH65hKQA3NKtYW0TiS40NTBqcW3eZnuFW1kSfHOk5czmtuzsw/exec"
git add -A && git commit -m "..." && git push
```

改 Code.gs 後更新同一個部署（網址不變）：

```
clasp push
clasp create-deployment --deploymentId AKfycbzlAf829w4jB1icEHwgIWH65hKQA3NKtYW0TiS40NTBqcW3eZnuFW1kSfHOk5czmtuzsw --description "..."
```
