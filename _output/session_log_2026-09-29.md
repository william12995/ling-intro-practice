# 工作紀錄 — 2026-09-29

## 本次完成事項

開始做 syntax 章的畫樹練習，目前只有原型 `ch02_syntax/tree_lab.src.html`，沒有加進 `build_site.py` 的 `PAGES`，所以沒上線，也沒接後端（沒有登入、推理欄、成績紀錄、AI 回饋）。

題目來源是開源課本 Ch.6 章末習題 6.22（PDF 401–406，共 20 題）。要畫樹的是 Ex 14–20：14 是 Ex 2 a–e 的 TP 樹、15 日語、16 修飾語、17 elephant in my pyjamas 歧義、18 嵌入子句、19–20 移位（疑問句、被動）。原型放了 Ex 14 的 a、c、d、e 四句，加一句不計分的教學句 a dog barked。14b（雙賓語）課本沒給畫法，跳過。

原型改了三版，使用者都看過：
1. 點選兩塊合併成父節點（`53b83ea`）。使用者說畫法很怪。
2. 打沒有標籤的括號＋拖標籤（`f320b2f`）。每個詞都要自己的括號，N' 上的 N 要寫 `[[children]]`，太彆扭。
3. 現行版（`baa3ffe`、`3f68df7`）：
   - 括號只用來分組，例如 `[[the children] [–PAST [read [the book]]]]`，每個詞自動有詞類格子。括號裡打標籤會被擋下並說明。
   - 標籤從固定在畫面頂端的標籤框拖到 `?` 上；手機可以先點標籤再點節點。拖或點的時候，每個節點上方的枝幹出現「+」，放上去就往上疊一層（N → N' → NP）。
   - 「✕ Remove」拖或點到標籤上可以移除；拖到已有標籤的節點會取代。
   - 改括號時，沒動到的成分會保留標籤（用涵蓋的詞範圍當 key）。
   - 樹下方即時顯示帶標籤的括號寫法。
   - 判分比對展開後的整棵樹；回饋列出缺的和多的節點（多的在樹上標紅），可以展開標準樹。
   - 教學句有藍色提示框，一步一步說下一步要放什麼、那個標籤是什麼意思；每題有可展開的標籤說明。
   - S 等同 TP，兩個都算對。

## 發現的重要資訊

- 使用者回報拖曳放不上去，原因是拖到視窗上緣會自動往上捲，而標籤框固定在頂端，所以每次一拖頁面就捲走。已拿掉往上捲，只留往下捲。
- Playwright 測試要注意：src 檔沒有 viewport meta，手機模擬要先用 `build_site.wrap()` 包過再測，不然會用 980px 排版；`mouse.move` 不會自動捲動，要先把元素捲進畫面。
- 標準答案是照課本 Figure 6.13/6.14 推的，只有 The robot repaired a spaceship 那張圖有直接依據。單獨的名字或代名詞畫成 NP → N' → N、14c 的 is 當 T 直接接 AP，這兩處沒有課本圖可對，要人核。
- 記法還沒定：老師上課用 Fromkin（S、Aux 那套），出題的開源課本用 X-bar/TP。現在只把 S 當 TP 的別名，Fromkin 真正的 S → NP VP（沒有 T'）結構仍會判錯。標籤表集中在 `GROUPS`/`GLOSS`，要換記法改那裡就好。

## 下次從這裡開始

1. 使用者自己再試一次現行原型，決定要不要正式做進題庫。還沒回答的問題：計分題要不要也有提示按鈕（會等於給答案）。
2. 問老師：畫樹照開源課本的 X-bar/TP，還是照 Fromkin 的 S/Aux。這會決定所有標準答案。
3. 決定要做之後：
   - 接上 ch01 的登入、推理欄、`record()`、AI 回饋（`keyText` 要加 tree 題型）。
   - 照 CLAUDE.md 做三件事：`PAGES` 加一列、Code.gs 的 `QUIZZES` 加 quiz id、頁面 `QUIZ_ID` 對上。
   - 前面先放 Ex 3、5、7 這類詞類和成分測試題（可以直接用 ch01 的選擇題元件）。
4. 之後再加：Ex 17 歧義（要兩棵樹都畫）、Ex 18 嵌入子句、Ex 19–20 移位（需要另做箭頭和刪除線）。
5. ch01 上次留下的待辦都還沒做：自己把 39 題做一遍核答案、拿 Gemini rate limit、請老師決定三件事、刪掉 `Z00000000` 測試列（見 `session_log_2026-09-26-3.md`）。

## 環境備忘

| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 原型 | `ch02_syntax/tree_lab.src.html`，直接用瀏覽器開 |
| 開源課本 Ch.6 | PDF 277–406；畫樹的說明在 6.13–6.21（PDF 340–400），習題 6.22 在 PDF 401–406 |
| Playwright | `chromium.launch(channel="msedge")`；手機測試用 `has_touch=True, is_mobile=True`，真的觸控拖曳用 CDP `Input.dispatchTouchEvent` |
| 學生網址（ch01） | https://william12995.github.io/ling-intro-practice/ch01_morphology/ |

原型的組裝和測試腳本放在 session 的暫存資料夾，沒進 repo；之後直接改 `ch02_syntax/tree_lab.src.html` 就好。
