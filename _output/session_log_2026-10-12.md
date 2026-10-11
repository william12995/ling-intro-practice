# 工作紀錄 — 2026-10-12

## 本次完成事項

- 老師來信兩則（使用者轉述）：
  1. 把 NLTK context-free grammar 做成習題：給幾個英文句子，學生照老師 Colab 的格式寫詞組結構律和 lexicon。老師的 Colab：https://colab.research.google.com/drive/1OkKRtSI8HS6Mr5XGYtXHcJqZNmqa_GeE （內容是 groucho grammar 的 *I shot an elephant in my pajamas*、NLTK book 的 grammar1 *Mary saw Bob*，用 ChartParser／RecursiveDescentParser 加 svgling 畫樹）。
  2. 拖拉畫樹的介面老師試了覺得不好用，不適合拿來評分。評分改成讓學生選哪個結構對，再論證為什麼。程式只要畫出學生的文法產生的樹，對不對由學生用詞組測試法論證。例句是 *John put the book on the desk*。
- 先做了 Colab notebook 版，使用者問為何用 Colab：要統一放在 GitHub Pages 的網站，課程結束後當寫報告的統合資料夾。Colab 版已刪（在 git 紀錄裡）。
- 改做網站版 `ch02-2_cfg/cfg_lab.src.html` → https://william12995.github.io/ling-intro-practice/ch02-2_cfg/ ，quiz id `ch02_cfg`：
  - 頁面用 JS 讀 NLTK `CFG.fromstring` 格式（註解、`|`、續行、單雙引號；多收 → 和彎引號），自己剖析列出所有樹（上限 6，`NP -> NP` 這類一元迴圈擋掉），用 SVG 畫樹。錯誤訊息照 notebook 版：格式錯、沒加引號、詞不在詞庫、首條規則不是 S、自我迴圈；剖析不出來時列出組得起來的片語。
  - 每句兩步：Step 1 寫文法看樹（不計分，S2-xx，文法全文存在 reasoning）；Step 2 兩棵樹選一棵＋詞組測試法論證（計分，S1-xx）。送出後顯示解說和一份可行的文法。
  - 題目：練習 Mary saw Bob（老師的 grammar1）、John put the book on the desk、The girl with the hat smiled、Bob ate the cake with a fork、Mary saw the man with the telescope（選「那個人拿著望遠鏡」的樹）、合併文法要通過 4 好句、排除 3 星號句。
  - 測試 `ch02-2_cfg/tests/test_page.py`（Playwright＋Edge，結果寫 `t_<寬>.log`）：10 種文法邊界情況全過，桌機和手機都能走完五題、重新整理進度還在、沒有橫向捲動、沒有 JS 錯誤。
- 用 clasp 建了第四份 Sheet「語言學概論 詞組結構律練習成績」（https://drive.google.com/open?id=1KQJSK3pQcRVI7uZ1vEajzI1Ls13-2pv3BM8-1h6ERx8 ），部署 id 在 `clasp_deploy/ch02_cfg/deployment.txt`。`Code.gs` 的 FIXED 加 `ch02_cfg: ['S1']`，順手重推了 ch02_syntax、ch03_morph_tree 的後端（config 都正常回應）。
- build_site.py 的 PAGES 加一列，CLAUDE.md 表格、DEPLOY.md 第 8 節已更新。

- 使用者授權了 ch02_cfg 後端，線上用 Z00000000 送一題，頁面顯示 Answers recorded（Sheet 裡有一列 S1-01、一列 S2-01 測試資料，要刪）。
- 使用者要求句法拖拉頁和構詞樹拖拉頁也改成「選哪個結構對＋論證」，拖拉整個拿掉（兩頁都還沒開放給學生，題號直接從 S1-01 重用）：
  - `ch02_syntax/tree_lab.src.html`：練習句＋9 題，題目同拖拉版，每題兩棵樹。誘答樹：缺 T'、補語錯放成附加語（do so 測試）、have 後面不成 VP、some poetry 不成 NP、at me 不成 PP、may 當 V；telescope 兩題用同一對樹、問不同意思。
  - `ch01-2_morph_tree/morph_tree.src.html`：reusable＋24 題，題目同拖拉版。誘答樹：詞綴接錯順序（un 接名詞、en 後面接 *couragement）、節點詞類標錯、兩個後綴一次接（沒有中間的詞）、box 當詞綴、外語詞綴串攤平。Meskwaki neta·nesaki 兩種接法都算對（ans 陣列），第三個選項是當成環綴攤平。
  - 兩頁共用同一套選擇題引擎（跟詞組結構律頁的畫樹、登入、上傳同一套程式，複製在各頁裡），進度 key 改 v2。
  - 舊的拖拉測試（`ch02_syntax/tests/`、`ch01-2_morph_tree/tests/`）刪了，新測試 `ch02-2_cfg/tests/test_mc_pages.py`：候選樹葉子一致、答案位置合法、每題可送出、故意錯一題、重新整理後狀態還在、桌機手機都沒有橫向捲動、沒有 JS 錯誤，兩頁都過。
  - CLAUDE.md 兩列、DEPLOY.md 第 6、7 節的紀錄格式已改。

## 發現的重要資訊

- 老師的 Colab 沒有 T 節點（`S -> NP VP`），跟句法拖拉頁照簡報用的 T ±pst 不一樣。網頁照老師 Colab 的格式。
- `RecursiveDescentParser` 遇到左遞迴（`VP -> VP PP`）會無限遞迴，網頁的剖析器自己處理左遞迴和一元迴圈。
- clasp 在 repo 子資料夾建新專案會被根目錄的 .clasp.json 擋（Project file already exists），要加 `-P .`。

## 下次從這裡開始

1. 三份 Sheet（句法、構詞樹、詞組結構律）刪掉 Z00000000 的測試列，時區改 GMT+08:00。句法和構詞樹的 Sheet 裡如果有拖拉版時期的測試列，格式跟新版不同，一併刪。
2. 請老師核：三頁的標準答案、誘答樹和解說（AI 寫的）；詞組結構律頁不放 T 是否可以（句法選樹頁照簡報放 T）。
3. 開放給學生前，自己用手機走一遍三頁。
4. 10-10 的待辦還在：ch01 判太嚴的兩處（S2-12、S5-07）。構詞樹「Affix 或 Prefix／Suffix」那條已經不適用（選擇題全用 Affix）。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 詞組結構律頁 | 改 `ch02-2_cfg/cfg_lab.src.html` 的 `ITEMS`，跑 `python build_site.py` |
| 本機測試 | `cd ch02-2_cfg/tests && python test_page.py`（詞組結構律頁）、`python test_mc_pages.py`（句法、構詞樹），看 `*.log` |
| 後端 | `python clasp_deploy/deploy_clasp.py ch02_cfg` |
