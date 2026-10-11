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

## 發現的重要資訊

- 老師的 Colab 沒有 T 節點（`S -> NP VP`），跟句法拖拉頁照簡報用的 T ±pst 不一樣。網頁照老師 Colab 的格式。
- `RecursiveDescentParser` 遇到左遞迴（`VP -> VP PP`）會無限遞迴，網頁的剖析器自己處理左遞迴和一元迴圈。
- clasp 在 repo 子資料夾建新專案會被根目錄的 .clasp.json 擋（Project file already exists），要加 `-P .`。

## 下次從這裡開始

1. 擁有者（rino881209@gmail.com）開一次 https://script.google.com/macros/s/AKfycby9PDgxL0Ry8eabFqauesQ1ZUg1jO9v5pFX63ygP_2LXuXsQwIOSuRu8d4Nj6pDLVML6g/exec 按授權，看到 `callback({"ok":true,"ping":true})`。之後用 Z00000000 做一題，確認 answers 有 S1 和 S2 兩列，再刪掉測試列、時區改 GMT+08:00。
2. 請老師核：四題的標準答案和解說（AI 寫的）、記法不放 T 可不可以、現有拖拉畫樹頁要不要改成不計分。
3. 10-10 的待辦還在：ch01 判太嚴的兩處、構詞樹標籤、老師核新題答案、刪測試列、Sheet 時區。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 詞組結構律頁 | 改 `ch02-2_cfg/cfg_lab.src.html` 的 `ITEMS`，跑 `python build_site.py` |
| 本機測試 | `cd ch02-2_cfg/tests && python test_page.py`，看 `t_1100.log`、`t_390.log` |
| 後端 | `python clasp_deploy/deploy_clasp.py ch02_cfg` |
