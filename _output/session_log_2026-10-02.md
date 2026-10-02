# 工作紀錄 — 2026-10-02

## 本次完成事項

`ch02_syntax/tree_lab.src.html` 整個改成拖拉版，打括號那一步拿掉了。畫布最下面排詞，標籤盤黏在視窗底部：

- 標籤拖到詞或節點上方的「+」：往上疊一層並自動接好（N → N' → NP 這種一路往上的情況）。
- 標籤丟在空白處，再把各塊往上拖到它身上：把幾塊併在一起（NP、V'、T'、TP）。
- 標籤丟到節點上是換標籤；點線剪斷；任何東西拖到 Delete 刪除；空白處拖曳是捲動。
- 不用拖也行：點標籤再點位置；點一塊再點它要接的節點。鍵盤用 Tab／Enter 也是同一套，選了標籤後在畫布上按 Enter 會放在上方空白處。
- 位置全自動排：高度 = 底下最高的子節點 + 1，同一層疊在一起的節點自動往上推一層（例如線交叉的時候）。
- 判分、缺漏回饋、標準樹沿用上一版；送出前會擋下並說明：詞沒接、空節點、好幾塊沒合併、線交叉。

使用者把老師的 Drive 資料夾下載到 `_output/`（`drive-download-…zip`、`syntax_part1.pptx`），裡面有 `syntax_part1–3.pptx`。Drive 連接器看不到那個資料夾裡 week01 以外的檔案，所以只能請使用者下載。答案記法照簡報改了（細節見下）。簡報和 zip 已列入 .gitignore，沒推上去。

另外開了一個 agent 做 code review，修了它找到的問題：教學提示會先拆掉對的結構、多指觸控留下殘影、滑鼠在畫布外放開時捲動卡住、同一標籤疊兩層時回饋錯誤、縮放視窗後沒接的節點跑位、點已接的父節點沒有回饋、沒有鍵盤操作、+ 和 ✕ 太小、標題上的 prototype 字樣，以及幾處說明文字。

最後一輪全部測試都通過：桌機完整流程 24 項、手機觸控完整流程 24 項、點選模式 10 項、review 回歸 18 項。完整流程是用真的拖曳把每題（含替代答案）做完並判成 Correct，另外測錯誤回饋、Undo、環、剪線、刪除和交叉。

Commit：`ac560f6`（拖拉版＋記法），之後一筆是 review 修正＋測試＋這份紀錄。

## 發現的重要資訊

- 老師的記法（`syntax_part1–3.pptx`，Fromkin 10th ed. Ch.3, Appendix C）跟開源課本不一樣。現在答案照老師的：
  - 限定詞是 Det，跟 N' 一起在 NP 底下（rule 2），不是 DP。
  - T 放 ±pst 或情態動詞；沒有情態動詞時，畫布上給一個 `+pst`／`–pst` 方塊，動詞寫原形（簡報 slide 16 "The child ate" 就是 +pst + eat）。
  - is、have 是 V，不在 T：14c 是 V' → V AP（rule 7），14e 是 V' → V VP（rule 20）。這兩題的樹形跟 9/29 版不同。
  - 名字和代名詞：簡報 slide 6（me）、slide 21（John）直接掛 NP；slide 19 又說一個詞的片語也有三層。兩種都算對，主要答案用直接掛 NP。
  - 簡報說考試會用 X-bar。調色盤拿掉了 S（簡報的結論是句子是 TP），加了 Adv、AdvP。
- 手機上的兩個坑，下次做拖曳介面要記得：
  - Chrome 不吃 SVG 子元素的 `touch-action`，所以整張 SVG 要設 `none`，捲動自己做。
  - Chrome 的觸控校正會把手指吸到附近的小目標。原本節點下方有一個拉線用的點，按節點常被吸到那個點，變成反方向接線，所以拿掉了。
- 9/29 那種「拖曳中自動捲動讓目標跑掉」的 bug 又出現一次：標籤盤在底部，往上拖一定經過下緣。現在只保留往上捲和左右捲，開始拖時先把詞那一排捲到標籤盤上面。
- 答案還是 AI 依簡報推的，要人核。特別是 14e 的 have + VP、以及動詞寫原形這個做法，學生會不會覺得怪。

## 下次從這裡開始

1. 使用者自己在手機和電腦上各做一遍（直接用瀏覽器開 `ch02_syntax/tree_lab.src.html`，或照下面指令包成完整頁），確認操作順手。
2. 請老師看一下：記法照她的簡報可不可以；「動詞寫原形、時態放 T」這樣呈現 OK 嗎；名字、代名詞兩種畫法都算對可以嗎。
3. 要上線時，照 CLAUDE.md 做：接 ch01 的登入、推理欄、`record()`、AI 回饋；`PAGES` 加一列、Code.gs 的 `QUIZZES` 加 quiz id、`QUIZ_ID` 對上。review 提醒的兩件事那時一起處理：
   - 推理欄要在看到解說前寫完。
   - 「Try again」之後學生可以照標準樹重做拿到 Correct，紀錄要只算第一次，或在最後一次之前不顯示標準樹。
4. 題目可以照簡報再加：Every girl read some poetry（part 2 練習 1）、A hyena laughed at me（slide 6 範例）、帶 PP 和 AdvP 附加語的句子、歧義句兩棵樹（the boy saw the man with the telescope）。調色盤已經有 Adv、AdvP、PP，需要的話再加 Int、C、CP。
5. ch01 的舊待辦還在（見 `session_log_2026-09-26-3.md`）。

## 環境備忘

| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 頁面原始檔 | `ch02_syntax/tree_lab.src.html` |
| 測試 | `ch02_syntax/tests/test_build_all.py [mouse\|touch]`、`test_tap_mode.py`、`test_review_fixes.py`（Playwright + Edge） |
| 老師簡報 | `_output/drive-download-20261002T142655Z-1-001.zip`（含 syntax_part1–3、morphology），不進 git |
| 課本 | 出題：開源課本 Ch.6 習題 6.22（PDF 401–406）；記法：老師簡報 |

重新跑全部測試（在 `ch02_syntax/tests/` 底下，console 是 cp950，要設 UTF-8）：
```
set PYTHONIOENCODING=utf-8
python test_build_all.py mouse
python test_build_all.py touch
python test_tap_mode.py
python test_review_fixes.py
```
`test_build_all.py` 的結果寫在同資料夾的 `t3_mouse.log`／`t3_touch.log`，最後一行是 `TOTAL FAILS`。
