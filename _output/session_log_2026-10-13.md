# 工作紀錄 — 2026-10-13

## 本次完成事項

- 使用者貼了老師 10-12 那封信的原文：「讓學生寫詞組結構律和 LEXICON，以便產生某些句子（例如 John put the book on the desk）。你的程式只要顯示他們寫的詞組結構律和 LEXICON 所產生的句法結構樹長什麼樣子，以及他們的句法結構樹如果使用詞組測試法論證是否正確即可。」對照之後發現，詞組結構律頁的「兩棵樹選一棵（計分）」不是這封信要求的，是從拖拉頁那則「選哪個結構對＋論證」搬過來的。
- 使用者說盡量簡化，照原信改 `ch02-2_cfg/cfg_lab.src.html`（commit `b5500d1`，已 push）：
  - 拿掉 opts/ans 和選樹 UI。每句現在是 Step 1 寫文法畫樹，Step 2 用詞組測試法論證自己的樹（挑至少一個詞組；文法給多棵樹時要說是哪一棵）。文法要畫得出樹、論證至少 20 字元才能送出。
  - 整頁不計分。每句送兩筆：S1-xx 是論證（response 是剖析摘要），S2-xx 是文法全文，correct 都空白。
  - 四句的解說改寫，不再提 Tree A／B。telescope 那句的題目改成「在論證裡說明哪棵樹是 the man was holding the telescope」。
  - 進度 key 改 `ling_prog_v2_`。
  - `apps_script/Code.gs` 的 FIXED 拿掉 ch02_cfg（總表不再列「S1 首次答對」），已用 `deploy_clasp.py ch02_cfg` 重新部署（@2）。
  - `test_page.py` 改成寫論證送出；桌機、手機都跑完五題，沒有橫向捲動，沒有 JS 錯誤。
  - CLAUDE.md 表格、DEPLOY.md 第 8 節已更新。
- 幫使用者寫了給老師的信，附三個連結（詞組結構律、句法選樹、構詞樹選樹）讓老師自己選，並請老師核答案，也確認詞組結構律頁沒有 T 而句法選樹頁有 T 是否可以。信是使用者自己寄。

## 發現的重要資訊

- 「詞組結構律」是老師信裡的用詞（phrase structure rules），不是我取的。
- 句法選樹、構詞樹兩頁還是「兩棵選一棵＋論證，計分」，這次沒動，等老師選。

## 下次從這裡開始

1. 看老師回信選哪一種，依回覆調整或下架其他頁。
2. 三份 Sheet（句法、構詞樹、詞組結構律）刪掉 Z00000000 的測試列，時區改 GMT+08:00。老師如果照信裡說的進去試做，她的測試列也要記得排除。
3. 老師核過的答案、解說回來後再修。
4. 10-10 的待辦還在：ch01 判太嚴的兩處（S2-12、S5-07）。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 詞組結構律頁 | 改 `ch02-2_cfg/cfg_lab.src.html` 的 `ITEMS`，跑 `python build_site.py` |
| 本機測試 | `cd ch02-2_cfg/tests && python test_page.py`（詞組結構律頁）、`python test_mc_pages.py`（句法、構詞樹），看 `*.log` |
| 後端 | `python clasp_deploy/deploy_clasp.py ch02_cfg` |
| 三個連結 | https://william12995.github.io/ling-intro-practice/ch02-2_cfg/ 、/ch02_syntax/ 、/ch01-2_morph_tree/ |

重新執行主腳本：
`C:\Python313\python.exe build_site.py`
