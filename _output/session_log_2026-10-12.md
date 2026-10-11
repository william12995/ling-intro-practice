# 工作紀錄 — 2026-10-12

## 本次完成事項

- 老師來信兩則（使用者轉述）：
  1. 把 NLTK context-free grammar 做成習題：給幾個英文句子，學生照老師 Colab 的格式寫詞組結構律和 lexicon。老師的 Colab：https://colab.research.google.com/drive/1OkKRtSI8HS6Mr5XGYtXHcJqZNmqa_GeE （內容是 groucho grammar 的 *I shot an elephant in my pajamas*、NLTK book 的 grammar1 *Mary saw Bob*，用 ChartParser／RecursiveDescentParser 加 svgling 畫樹）。
  2. 拖拉畫樹的介面老師試了覺得不好用，不適合拿來評分。評分改成讓學生選哪個結構對，再論證為什麼。程式只要畫出學生的文法產生的樹，對不對由學生用詞組測試法論證。例句是 *John put the book on the desk*。
- 做了 CFG 習題 notebook：
  - 產生器 `ch02-2_cfg/make_notebooks.py` 同時產生學生版 `ch02-2_cfg/cfg_exercise.ipynb`（推上 GitHub）和答案版 `_output/answer_keys/cfg_exercise_KEY.ipynb`（gitignore）。
  - 內容：一格收合的 Setup，裡面有 `show(grammar, sentence)` 和 `check(grammar, good, bad)`。範例沿用老師的 grammar1 和 *Mary saw Bob*，接著是詞組測試法表格。Task 1–4 的句子依序是 *John put the book on the desk*、*The girl with the hat smiled*、*Bob ate the cake with a fork*、*Mary saw the man with the telescope*（要寫出兩棵樹）。Task 5 要學生把前面的文法合成一份，產生四個好句，同時排除 *\*John put the book*、*\*The girl smiled the cake*、*\*Mary saw*，藉此帶出次類畫分。
  - 每題的程式格後面有一格論證，學生自己填。答案版的論證是 AI 寫的，標了「請老師核」。
  - `show` 會擋掉這幾種錯：文法格式錯（例如 `=>`）、詞沒加引號、詞不在詞庫（含大小寫不同）、第一條規則不是 S、`NP -> NP` 這種會無限迴圈的規則。句子分析不出來時，會列出文法能組成的片語。分析出兩棵以上的樹時，會提示這個文法有歧義，要學生用測試法決定哪棵對。
  - 本機用 `ch02-2_cfg/tests/run_notebook.py` 跑過：答案版四句的樹都對，Task 5 七句全 ✅。故意寫錯的六種情況訊息都正確。過程中修了一個問題：空白文法跑 `check` 時，星號句原本會因為缺詞而顯示 ✅。
- CLAUDE.md 表格加了一列。`.gitignore` 加了 `_output/answer_keys/`。

## 發現的重要資訊

- 老師的 Colab 沒有 T 節點（`S -> NP VP`），跟句法拖拉頁照簡報用的 T ±pst 不一樣。notebook 照老師 Colab 的格式。
- `RecursiveDescentParser` 遇到左遞迴（`VP -> VP PP`）會無限遞迴，所以 notebook 一律用 ChartParser，並用 islice 限制最多畫 6 棵。
- Colab 不會把成績記到 Sheet。學生怎麼繳（下載 .ipynb 上傳 NTU COOL，或分享 Colab 連結）還沒定。
- Colab 實機還沒開過。本機只驗了解析邏輯和 svgling 能產生 SVG，`!pip` 那行和 svgling 在 Colab 裡實際的顯示要開連結確認。

## 下次從這裡開始

1. 在 Colab 開學生版連結跑一遍，確認 Setup 格會收合、樹畫得出來。
2. 等老師回覆後再做評分用的選擇題頁（選哪棵樹對＋論證，網站上記 Sheet）。要問老師的事：
   - 選擇題的樹用哪種記法：照 Colab 不放 T，還是照簡報放 T。
   - 現有的拖拉畫樹頁（ch02_syntax、構詞樹）改成不計分的練習，還是照舊。
   - notebook 怎麼繳。
3. 新頁要開新的 quiz id 和新的 Sheet（clasp），ch02_syntax 的題目不動。
4. 10-10 的待辦還在：ch01 判太嚴的兩處、構詞樹標籤、老師核答案、刪測試列、Sheet 時區。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe`（已裝 svgling 0.5.0、nltk 3.9.4；沒有 IPython，測試腳本自己 stub） |
| 改題目 | 改 `ch02-2_cfg/make_notebooks.py` 的 `TASKS`，再跑 `python ch02-2_cfg/make_notebooks.py` |
| 本機測試 | `python ch02-2_cfg/tests/run_notebook.py <nb.ipynb> <out.txt> [額外.py ...]`，輸出寫 UTF-8 檔再讀 |
| 學生連結 | https://colab.research.google.com/github/william12995/ling-intro-practice/blob/main/ch02-2_cfg/cfg_exercise.ipynb |
