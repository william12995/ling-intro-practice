"""用 clasp 把 apps_script/Code.gs 推到某一章的 Sheet，並更新到同一個部署（網址不變）。

每章一個資料夾 clasp_deploy/<quiz id>/：
  .clasp.json      clasp 的專案設定（scriptId、綁定的 Sheet）
  deployment.txt   網頁應用程式的部署 id，endpoints.json 裡的網址就是它
  src/             推送前由這支腳本重新產生（Code.gs、appsscript.json、config.gs），不進 git

    python clasp_deploy/deploy_clasp.py ch02_syntax

ch01_morphology 不走這裡：它的 clasp 設定是 repo 根目錄的 .clasp.json（rootDir=apps_script），
那份 Sheet 沒有 config.gs，靠 Code.gs 的預設值收 ch01。不要把別章的檔案放進 apps_script/，會被一起推到 ch01。
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "apps_script"


def main():
    if len(sys.argv) != 2:
        sys.exit("用法：python clasp_deploy/deploy_clasp.py <quiz id>")
    quiz = sys.argv[1]
    d = HERE / quiz
    if not (d / ".clasp.json").exists():
        sys.exit(f"{d} 沒有 .clasp.json，這章還沒用 clasp 建過")
    src = d / "src"
    if src.exists():
        shutil.rmtree(src)
    src.mkdir()
    for f in ("Code.gs", "appsscript.json"):
        shutil.copy(SRC / f, src / f)
    (src / "config.gs").write_text(
        "// 這份專案收哪一章（deploy_clasp.py 產生，不要手改）\n"
        f"var DEFAULT_QUIZZES = '{quiz}';\n", encoding="utf-8")
    clasp = shutil.which("clasp") or "clasp"
    run = lambda *a: subprocess.run([clasp, "-P", str(d), *a], check=True)
    run("push", "-f")
    dep = (d / "deployment.txt").read_text(encoding="utf-8").strip()
    run("update-deployment", dep, "-d", f"{quiz} update")
    print(f"已更新部署 {dep}，網址不變")


if __name__ == "__main__":
    main()
