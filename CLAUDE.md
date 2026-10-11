# 語言學概論助教課

使用者 2026-09 起擔任老師的語言學概論助教。這個資料夾放課程教材與互動網頁，跟碩論研究無關，研究的東西不要寫進來。

## 出題用的教材

2026-09-26 老師來信改規則：因為 Fromkin 的習題太難又有版權問題，互動頁的題目改從開源課本出。

`textbook/Essentials-of-Linguistics-2nd-edition.pdf`：Anderson, Bjorkman, Denis, Doner, Grant, Sanders & Taniguchi, *Essentials of Linguistics*, 2nd ed.（eCampusOntario Pressbooks），CC BY-NC-SA 4.0。

- PDF 頁碼 = 印刷頁碼 + 20（PDF 272 = p. 252）。
- Ch.5 Morphology 在 PDF 229–276，章末習題 5.12 在 PDF 272–274（Exercise 1–7）。PDF 版把章內的「Check your understanding」互動題拿掉了，只有線上版有。
- Ch.6 Syntax 在 PDF 277–406，畫樹的說明在 6.13–6.21（PDF 340–400），章末習題 6.22 在 PDF 401–406（Exercise 1–20，14–20 要畫樹）。
- 這本沒附解答，頁面上的標準答案是 AI 寫的，要人核過。
- 授權要求標出處，而且改寫版要用同一授權，所以頁尾一定要留一行出處和授權（見下面慣例的例外）。

### 講課用的課本（不再拿來出題）

`textbook/An_Introduction_to_Language.pdf`：Fromkin, Rodman & Hyams, *An Introduction to Language*, 9th ed., 2011。

- PDF 頁碼 = 印刷頁碼 + 20。頁面上引用一律用印刷頁碼。
- 章節（PDF 頁）：Intro Brain and Language 23；1 Morphology 56–96；2 Syntax 97；3 Meaning 159；4 Phonetics 209；5 Phonology 246；6 What Is Language 304；7 Acquisition 344；8 Processing 395；9 Language in Society 450；10 Language Change 508。
- console 是 cp950，抽 PDF 文字要寫成 UTF-8 檔再讀。

## 已做的教材

| 章 | 原始檔 | 上線版 |
|---|---|---|
| Morphology（開源課本 Ch.5 習題 1–7，39 題） | `ch01_morphology/morphology_lab.src.html` | `docs/ch01_morphology/index.html`（已上線：https://william12995.github.io/ling-intro-practice/ch01_morphology/ ） |
| Syntax 選樹（原本是拖拉畫樹，10-12 老師說拖拉不適合評分，整頁改成兩棵樹選一棵＋論證；拖拉版在 git `e14cfd1` 以前。練習句＋9 題：Ex 14 四句、三題課堂句、telescope 兩讀法。記法照老師簡報。學生還沒作答過，題號重新從 S1-01 用） | `ch02_syntax/tree_lab.src.html`，測試 `ch02-2_cfg/tests/test_mc_pages.py`（兩頁共用） | `docs/ch02_syntax/index.html`（https://william12995.github.io/ling-intro-practice/ch02_syntax/ ）。成績 Sheet 用 clasp 建在 rino881209@gmail.com，後端更新跑 `python clasp_deploy/deploy_clasp.py ch02_syntax`（DEPLOY.md 第 6 節） |
| 構詞樹 選樹（10-12 跟句法頁一起改成選樹＋論證，引擎相同。練習 reusable＋24 題，題目同拖拉版：基本、詞綴順序、複合詞、歧義兩讀法、後綴、屈折、Turkish／Japanese、Meskwaki（兩種接法都算對，ans 是陣列）、環綴。誘答樹是 AI 出的，要老師核） | `ch01-2_morph_tree/morph_tree.src.html` | `docs/ch01-2_morph_tree/index.html`（https://william12995.github.io/ling-intro-practice/ch01-2_morph_tree/ ）。10-10 從 ch03 改名 ch01-2，quiz id、`clasp_deploy/ch03_morph_tree/`、endpoints.json 的 key 都還是 `ch03_morph_tree`，舊網址由 build_site.py 的 `MOVED` 產生轉址頁。Sheet「語言學概論 構詞樹練習成績」，後端更新跑 `python clasp_deploy/deploy_clasp.py ch03_morph_tree` |
| 詞組結構律（10-12 老師要求：拖拉畫樹不適合評分。每句兩步：(1) 學生照老師 Colab 的 `nltk.CFG.fromstring` 格式寫規則和 lexicon，頁面在瀏覽器裡剖析、畫出所有樹，不計分，記成 S2-xx；(2) 兩棵樹選一棵再用詞組測試法論證，計分，記成 S1-xx。四句＋合併文法（要排除星號句）。記法照老師 Colab，沒有 T、沒有 bar 層。10-12 先試做 Colab 版，使用者要求統一放網站，Colab 版已刪） | `ch02-2_cfg/cfg_lab.src.html`，測試 `ch02-2_cfg/tests/test_page.py` | `docs/ch02-2_cfg/index.html`（https://william12995.github.io/ling-intro-practice/ch02-2_cfg/ ）。quiz id `ch02_cfg`，Sheet「語言學概論 詞組結構律練習成績」用 clasp 建在 rino881209@gmail.com，後端更新跑 `python clasp_deploy/deploy_clasp.py ch02_cfg` |

老師的句法簡報 `syntax_part1–3.pptx`（Fromkin 10th ed. Ch.3）在 `_output/`，已列入 .gitignore。構詞樹的記法照老師的 `_output/Lecture4Morphology.ppt` 第 28 張（reusable）：每個詞綴上面一個 Affix、每個詞根上面一個詞類（N、V、Adj、Adv），合起來的節點標新詞的詞類，詞素寫成不帶連字號（re、use、able）。句法的畫樹記法以簡報為準：Det（不是 DP）、T 放 ±pst 或情態動詞、have/be 是 V（Appendix C rule 7、20）、名字和代名詞可直接掛 NP。

2026-09-26 整頁換掉：原本的 Fromkin 內文範例版（20 題選擇＋四關切詞）在學生作答前就撤下了，舊版在 git 紀錄 `be842ae`。資料夾名稱和 quiz id 還是 `ch01_morphology`。

只改 `*.src.html`，改完跑 `python build_site.py` 重建 `docs/`，`docs/` 不要手改。每章記在自己的 Google Sheet，各自的網址存在 `endpoints.json`，換網址用 `--endpoint 章節=網址`；沒有網址的章節不會輸出。src 沒有 doctype/head，是因為它同時可以直接發布成 claude.ai artifact 當預覽（https://claude.ai/artifact/NxGDg4swf7XuwU4kNLLs93 ，私人；更新時帶這個 URL 當 `url`）。artifact 裡連不到 Google，成績只會存在瀏覽器。

2026-09-26 老師要求頁面全英文（外文系），學生看得到的文字都是英文，程式註解和 Sheet 欄名維持中文。AI 回饋（Gemini，後端 `action=feedback`）程式預設關閉，開啟條件和步驟在 `DEPLOY.md` 第 5 節；構詞那份 Sheet 已經開了（10-03 看到 442 則回饋，83% 是備援的 flash-lite 寫的），句法那份沒開；每則回饋都固定附一句「AI 寫的，僅供參考」。

成績記錄：學生先填學號姓名，每答一題送一筆到 Google Sheet（`apps_script/Code.gs`）。部署步驟和成績算法在 `DEPLOY.md`。新增章節時：照 `clasp_deploy/ch02_syntax/` 的做法用 clasp 建 Sheet 和部署（`config.gs` 寫 `DEFAULT_QUIZZES`，擁有者要開一次網址按授權），或手動貼 Code.gs、設指令碼屬性 `QUIZZES`；根目錄 `.clasp.json` 是構詞那份，會把整個 `apps_script/` 推上去，別章的檔案不要放那裡；`build_site.py` 的 `PAGES` 加一列；新頁面的 `QUIZ_ID` 要一致，上傳佇列的 localStorage key 要帶 quiz id（兩頁同網域，共用 localStorage）。

題號是照陣列位置編的（`S1-01`、`S5-07`），學生開始作答後不能調換或替換既有題目，只能在最後加。

`.gitignore` 排除 `textbook/`，課本有版權，不能推上 public repo。

## 慣例

- 老師的要求（2026-09-26 更新）：題目從開源課本的章末習題出。先放答案固定的觀念題，再逐步加難到陌生語言的解題。原本「章末習題不放、留給作業」那條作廢。
- 每題兩欄：固定答案（系統自動判）和推理過程（只存，給老師抽查答案對但推理錯的情況）。推理要在看到解說之前寫完，送出後才顯示解說，不然學生會照抄解說。推理最後怎麼處理，老師說之後再討論。
- 沒有固定答案的題目（例如習題 5 申論）設成不計分，`correct` 送空白。
- 答案有爭議的題目（例如 receive 要不要切出 -ceive）兩種都算對，在解說裡講清楚，不要硬判。
- 同一份頁面裡的判準要一致：前面教過的概念（例如黏著詞根），後面的題目不能反過來扣分。
- 頁面上不放給老師或助教看的說明（出處註記、出題設計理由、「本頁包含什麼」這類導言）。學生只需要題目、操作提示和解說。使用者 2026-09-26 明確要求拿掉。唯一例外是頁尾那一行開源課本的出處和授權，這是 CC BY-NC-SA 的要求，不能拿掉。
