# 工作紀錄 — 2026-09-26

這個資料夾今天建立，從 `ENG_Pragmatic` 那邊開 session 做的。

## 本次完成事項

- 建了 `Ling-Intro-TA` 資料夾，並列入全域 CLAUDE.md 的資產地圖。課本 PDF 從 `ENG_Pragmatic/_output/` 搬到 `textbook/`。
- 做了 Ch.1 Morphology 互動練習頁 `ch01_morphology/morphology_lab.src.html`：第一部分 20 題課本範例；第二部分四關切詞，共 29 題（7+7+7+8）。
- 使用者要求拿掉給老師看的說明文字（footer 的出處註記、開頭導言），已經拿掉。規則寫進本資料夾的 CLAUDE.md。
- 加了成績記錄：學生填學號姓名後，每答一題送一筆 JSONP 到 Apps Script，寫進 Google Sheet。後端在 `apps_script/Code.gs`（append-only，不加鎖；重算總表時去重，首次作答依 server_time 判定）。`build_site.py` 產生 `docs/` 給 GitHub Pages 用。部署手冊在 `DEPLOY.md`。
- 本機 git repo 已 commit（`main`，作者 rino881209@gmail.com），還沒推上 GitHub。`.gitignore` 排除 `textbook/`。

## 下次從這裡開始（使用者說明天要用）

1. 使用者照 `DEPLOY.md` 第 1 步建 Sheet、貼 Code.gs、部署，把 `/exec` 網址給我。
2. 跑 `C:\Python313\python.exe build_site.py --endpoint "<網址>"`，commit。
3. 使用者跑 `! gh auth login`。確認 repo 名稱（建議 `ling-intro-practice`，必須 public）和要不要把 CLAUDE.md 加進 .gitignore，然後建 repo、push、Settings → Pages 選 main /docs。
4. 照 DEPLOY.md 第 4 步用假學號 `Z00000000` 測完整流程：頁面顯示「成績已記錄」，answers 有列，「成績 → 重算總表」產生 summary。測完刪掉測試列。
5. 老師要決定用「首次答對」還是「最佳答對」當成績。

## 還沒驗證

Apps Script 沒實際跑過，JSONP 寫進 Sheet 沒測過，登入畫面沒在瀏覽器看過。只跑過兩支程式的 `node --check`。

## 環境備忘

| 項目 | 值 |
|------|-----|
| Python | `C:\Python313\python.exe` |
| 課本 | `textbook/An_Introduction_to_Language.pdf`（9th ed.，PDF 頁 = 印刷頁 + 20） |
| 預覽 artifact | https://claude.ai/artifact/NxGDg4swf7XuwU4kNLLs93 （私人；連不到 Google，只能預覽，不要發給學生） |
| gh | 尚未登入 |

重建網頁：

```
C:\Python313\python.exe build_site.py --endpoint "https://script.google.com/macros/s/XXXX/exec"
```
