# 工作紀錄 — 2026-10-04

## 本次完成事項

10-04 會議記錄四點：句法樹的畫法也用到構詞、句法題少放 X-bar 多放基礎題、練習歧義（I saw the man with the telescope、unlockable）、台語標註資料檢查完寄給老師。台語那點不屬於這個資料夾，使用者說不用管。老師來信指定構詞樹照 Lecture4Morphology 投影片的畫法，使用者下載到 `_output/Lecture4Morphology.ppt`（已被 `_output/*.ppt` 擋在 git 外）。

- 先回答使用者的問題：句法頁沒有接 Gemini 回饋。前端沒有 `action=feedback`，後端 Code.gs 雖然有那段，句法那份 Sheet 也沒開 `FEEDBACK_ON`。
- 用 PowerPoint COM 把 .ppt 轉成 PDF 看。樹在第 26–29 張：`[Adj [V [Affix re] [V use]] [Affix able]]`，第 29 張的練習是 unhappiness、deactivation。
- 新頁 `ch03_morph_tree/morph_tree.src.html`：整份照抄句法頁的引擎，換掉題目、標籤（Category：N V Adj Adv；Morpheme：Affix）、GLOSS、學生看得到的文字（sentence → word/morpheme），教學動畫四段改用 re + use 示範。quiz id `ch03_morph_tree`，教學看過的 key 改成 `ling_morph_tree_tutorial_seen`，佇列和進度 key 本來就帶 quiz id。
- 題目（S1-01～S1-14，練習題 reusable 不計分）：reader、unkind、kindness、unkindness、foolishness、unhappiness、governmental、encouragement、mailbox、deactivation、unlockable（able to be unlocked）、unlockable（not able to be locked）、river boat race（a race between river boats）、river boat race（a boat race held on a river）。來源：老師投影片（reusable、unhappiness、deactivation、encouragement、reader、mailbox）、開源課本 5.6（unkindness、foolishness）、5.9（untieable 的歧義寫法、river boat race）、5.10（governmental），unlockable 是會議指定。歧義詞拆兩題、各附一個意思，每題只有一棵標準樹。送到 Sheet 的 prompt 有帶意思，例如 `unlockable (able to be unlocked)`。
- 屈折詞尾（-s、-est、-er 比較級）先沒出，投影片沒示範怎麼畫。
- `build_site.py` 的 PAGES 加了 ch03，`apps_script/Code.gs` 的 summary 固定欄位加 `'ch03_morph_tree': ['S1']`（構詞、句法兩份 Sheet 沒重新部署，不受影響）。
- 測試（`ch03_morph_tree/tests/`）：`test_build_all.py` 滑鼠 40、觸控 40 全過（15 題照標準答案拖完都判 Correct、錯誤順序的 unkindness 判 Not quite、編輯工具、線交叉提示）；`test_tap_mode.py`、`test_record_and_ux.py` 都 0 失敗（record 測的是 S1-11、prompt 帶意思）。句法頁專屬的 `test_review_fixes.py` 沒搬，那些是引擎回歸測試，句法頁那邊有在跑。`smoke.py` 截圖看過教學動畫和完成畫面。
- 用 clasp 建了 Sheet「語言學概論 構詞樹練習成績」（https://drive.google.com/open?id=1ntELF7RcI20udt-wriuT8waeEiCiUn9P8UA7L3aG7GE ），推上 Code.gs＋config.gs（`DEFAULT_QUIZZES = 'ch03_morph_tree'`），部署 id `AKfycbwoxhgQffIOeRvwBNInh7s1igaXq9UiBObKFopK_rSCvOCrgd4mtmb4DY7kzScY7M34`（存在 `clasp_deploy/ch03_morph_tree/deployment.txt`）。
- Commit `868f01b`，已 push。docs/ 還沒有 ch03，因為 endpoints.json 還沒填網址。

## 發現的重要資訊

- clasp `create-script` 在新資料夾裡建完，`.clasp.json` 的 rootDir 是空字串，要改成 `src`，並刪掉它拉下來的 appsscript.json。
- 引擎的判分和教學提示完全不看標籤名稱，換標籤表就能畫構詞樹，不用改邏輯。

## 下次從這裡開始

1. 等使用者用 rino881209@gmail.com 開 /exec 網址按授權。之後：`python build_site.py --endpoint ch03_morph_tree=https://script.google.com/macros/s/AKfycbwoxhgQffIOeRvwBNInh7s1igaXq9UiBObKFopK_rSCvOCrgd4mtmb4DY7kzScY7M34/exec`，commit、push，用 Z00000000 做一題看 Sheet，請使用者刪測試列。Sheet 時區改台北。
2. 標準答案是 AI 擬的，請老師核，特別是 deactivation（act + ive + ate 的切法）、encouragement 的 en- 先接、mailbox 的頂層 N。
3. 會議的句法部分還沒做：少放 X-bar、多放基礎練習、"I saw the man with the telescope" 兩棵樹。ch02 已上線、有學生作答，既有題目不能換或調順序。要另開一份基礎句法頁，還是在 ch02 最後加題，等使用者決定。
4. 構詞樹這頁沒接 AI 回饋（後端預設關）。
5. 之前的待辦：ch01 切詞題 prompt 錯誤（`buildPrompt_` 的 note）、句法 Sheet 測試列和時區。

## 環境備忘
| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 構詞樹頁 | `ch03_morph_tree/morph_tree.src.html` |
| 構詞樹後端 | `clasp_deploy/ch03_morph_tree/`（改後端：`python clasp_deploy/deploy_clasp.py ch03_morph_tree`） |
| 老師投影片 | `_output/Lecture4Morphology.ppt`（PowerPoint COM 轉 PDF 才讀得到） |

跑構詞樹測試（在 `ch03_morph_tree/tests/`）：
```
set PYTHONIOENCODING=utf-8
python test_build_all.py mouse
python test_build_all.py touch
python test_tap_mode.py
python test_record_and_ux.py
```
