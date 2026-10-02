# 工作紀錄 — 2026-10-03

## 本次完成事項

使用者看過 10-02 的拖拉版，喜歡練習句的逐步解說，要求：讓學生一下就看懂互動規則（像遊戲那樣有教學動畫），再接上成績紀錄，而且句法要記在另一份 Sheet。這次都做完了，只差使用者建第二份 Sheet。

頁面 `ch02_syntax/tree_lab.src.html`：

- 「How to play」教學動畫：四段會自己播的示範，分別是往上疊、合併、修正（剪線、拖到 Delete）、送出。每段有一隻手在做動作，無限循環。第一次登入自動打開；右上角按鈕可以重看；可以略過；方向鍵、Esc、Tab 都能用；減少動態的設定下停在固定畫面。
- 練習句的提示會發亮：提示框有「Step 3 of 11」和進度條，要拖的標籤、要放的 +、建議放的空白處（虛線圈）、要往上拖的那塊（會動的虛線箭頭）、要剪的線、要刪的節點都會發亮，最後 Submit 也會發亮。測試只照著發亮的東西做，16 步做完並判成 Correct。
- 標籤盤底下固定一行規則：+ stack up · empty spot new group · drag up connect · tap a line cut。
- 登入（學號一個字母加 8 位數字，跟 ch01 共用登入資料）、計分題要先寫至少 20 字元的推理才能送出，送出後鎖住；練習句不計分、不送。
- 每題送出時送一筆：題號 `S1-01`～`S1-04`、level 1、response 是帶標籤的括號、correct、attempt、reasoning。Try again 是第 2 次作答，推理清空。
- 每個學號的進度存在瀏覽器（`ling_prog_v1_ch02_syntax_<學號>`），重新整理後樹和作答狀態都在。
- 換題時題目先捲進畫面，再讓詞那一排露在標籤盤上面。

另一份 Sheet 的做法：

- `build_site.py` 改成每章各有自己的網址，存在新的 `endpoints.json`（ch01 的網址已經存進去）。沒有網址的章節不輸出，所以 ch02 在使用者給網址之前不會上線。重建後 ch01 的輸出完全沒變（`git diff docs/` 是空的）。
- 給網址時（`--endpoint ch02_syntax=網址`）會先問後端 `action=config`，那份 Sheet 的 `QUIZZES` 沒設成 ch02_syntax 就擋下來。
- `apps_script/Code.gs`：每份 Sheet 只收指令碼屬性 `QUIZZES` 列的章節，沒設就是 `ch01_morphology`，現有的構詞 Sheet 行為不變。summary 欄位改成每章固定（ch01 S1–S6、ch02 S1）。
- ch02 的上傳佇列用自己的 key（`ling_queue_ch02_syntax`），不會碰到 ch01 還沒送出的紀錄（兩頁同網域，localStorage 共用，這是 advisor 抓到的風險）。後端回 `unknown quiz` 時留在佇列、提醒學生，設好後自動補送。
- `DEPLOY.md` 第 2 節改成每章網址的寫法，新增第 6 節：句法 Sheet 的建立步驟。CLAUDE.md 的表格和「新增章節」說明也更新了。

兩輪 code review（另開的 agent）：第一輪是 10-02 的；這次第二輪沒有高嚴重度問題，修了它找到的：換題後題目被捲出畫面、後端沒設 QUIZZES 時答案會被丟進退件區、教學動畫焦點跑掉時 Esc 失效、Esc 會順便清掉頁面上選好的標籤、選著標籤時點線沒反應、換學生沒清掉選好的標籤、存壞的進度會讓頁面出錯、教學第 4 步沒提到要寫推理、summary 欄位會跳動、build_site 略過的章節留著舊檔沒提醒。

最後一輪測試全過：`test_build_all.py` 桌機 24、手機觸控 24，`test_tap_mode.py` 10，`test_review_fixes.py` 18，`test_record_and_ux.py` 44，共 120 項 0 失敗。另外用假的回應測了 build_site 的後端檢查三種情況。

Commit：`6dfb1f2`（教學動畫、提示、成績紀錄）、`9c3631c`、之後一筆是第二輪 review 修正＋這份紀錄。

## 發現的重要資訊

- 兩頁在同一個 github.io 網域，localStorage 共用。新章節的佇列、進度 key 一定要帶 quiz id；只有 `ling_student`（學號姓名）刻意共用。
- 現在還沒有 ch02 的 Sheet。頁面送出的紀錄在沒有網址時只存在學生瀏覽器（顯示 Saved on this device only），所以一定要先建 Sheet 再上線。
- 學生第一次送出後就看得到標準樹，Try again 的結果很可能是照抄；評分看 summary 的「首次答對」。
- 標準答案仍是 AI 依老師簡報推的，還沒有人核過（特別是動詞寫原形、時態獨立一格、14e 的 have + VP）。

## 下次從這裡開始

1. 使用者照 `DEPLOY.md` 第 6 節建第二份 Sheet：新 Sheet → 貼 `apps_script/Code.gs` → 指令碼屬性 `QUIZZES` = `ch02_syntax` → 部署成網頁應用程式 → 把 `/exec` 網址給我。
2. 拿到網址後：`python build_site.py --endpoint ch02_syntax=<網址>`（會自動檢查後端設定），commit、push，頁面就在 `https://william12995.github.io/ling-intro-practice/ch02_syntax/`。用 `Z00000000` 做一題，看 Sheet 有那一列，重算總表，刪測試列。
3. 請老師核答案和記法（同 10-02 的待辦）。
4. 之後可以加的題目：Every girl read some poetry、A hyena laughed at me、帶 PP/AdvP 附加語的句子、歧義句兩棵樹。加題只能加在 ITEMS 最後。
5. AI 回饋這頁還沒接（沒被要求，後端預設也關）。
6. ch01 的舊待辦還在（`session_log_2026-09-26-3.md`）。

## 環境備忘

| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 頁面原始檔 | `ch02_syntax/tree_lab.src.html` |
| 每章後端網址 | `endpoints.json`（ch01 已填，ch02 待填） |
| 後端 | `apps_script/Code.gs`（每份 Sheet 用指令碼屬性 `QUIZZES` 指定收哪一章） |
| 測試 | `ch02_syntax/tests/`：`test_build_all.py mouse|touch`、`test_tap_mode.py`、`test_review_fixes.py`、`test_record_and_ux.py`、`smoke.py`（截圖看外觀） |

重新跑全部測試（在 `ch02_syntax/tests/` 底下）：
```
set PYTHONIOENCODING=utf-8
python test_build_all.py mouse
python test_build_all.py touch
python test_tap_mode.py
python test_review_fixes.py
python test_record_and_ux.py
```
每支最後一行是 `FAILS 0` 或 `TOTAL FAILS: 0`（`test_build_all.py` 的結果寫在 `t3_mouse.log`／`t3_touch.log`）。
