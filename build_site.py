"""把各章的 *.src.html 包成可以放上 GitHub Pages 的完整網頁，輸出到 docs/（GitHub Pages 設定成從 main 分支的 /docs 發布）。

src 檔沒有 <!doctype>/<head>（它同時拿來發布成 claude.ai artifact，外殼由平台補），
這支腳本補上 doctype、charset、viewport，並把 __ENDPOINT__ 換成那一章的 Apps Script 網址。

每一章各記在自己的 Google Sheet，所以每章有自己的後端網址，存在 endpoints.json（網址本來就會出現在
docs/ 的公開網頁裡，放進 repo 沒有差別；存起來是為了重建時不會漏掉某一章的網址）。
還沒有網址的章節不會輸出，避免把只存本機的版本放上線。

用法：
    python build_site.py                                            # 用 endpoints.json 裡的網址重建
    python build_site.py --endpoint ch02_syntax=https://script.google.com/macros/s/XXXX/exec
                                                                    # 設定（或更新）某一章的網址，存進 endpoints.json 再重建
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "docs"
EP_FILE = ROOT / "endpoints.json"
PAGES = [  # (quiz id＝endpoints.json 的 key, src, 輸出路徑, 首頁上顯示的名稱)
    ("ch01_morphology", "ch01_morphology/morphology_lab.src.html", "ch01_morphology/index.html", "Morphology"),
    ("ch02_syntax", "ch02_syntax/tree_lab.src.html", "ch02_syntax/index.html", "Syntax: build the tree"),
]
URL_RE = r"^https://script\.google\.com/macros/s/[^/]+/exec$"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
"""


def wrap(src: str) -> str:
    # src 開頭是 <title>…<style>…</style>，其餘是 body 內容
    m = re.search(r"</style>\s*", src)
    head, body = src[: m.end()], src[m.end():]
    return HEAD + head + "</head>\n<body>\n" + body + "\n</body>\n</html>\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", action="append", default=[],
                    help="章節=Apps Script 網址，例如 ch02_syntax=https://script.google.com/macros/s/XXXX/exec；可以給好幾次")
    a = ap.parse_args()
    eps = json.loads(EP_FILE.read_text(encoding="utf-8")) if EP_FILE.exists() else {}
    keys = [p[0] for p in PAGES]
    for item in a.endpoint:
        if "=" not in item:
            raise SystemExit(f"請寫成 章節=網址，章節是 {', '.join(keys)} 其中之一：{item}")
        k, url = item.split("=", 1)
        k, url = k.strip(), url.strip()
        if k not in keys:
            raise SystemExit(f"沒有這個章節：{k}（可用的有 {', '.join(keys)}）")
        if not re.match(URL_RE, url):
            raise SystemExit(f"網址格式不對，應該長得像 https://script.google.com/macros/s/XXXX/exec ：{url}")
        eps[k] = url
    if a.endpoint:
        EP_FILE.write_text(json.dumps(eps, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"已更新 {EP_FILE.name}")

    SITE.mkdir(exist_ok=True)
    (SITE / ".nojekyll").write_text("", encoding="utf-8")   # 關掉 GitHub Pages 的 Jekyll
    links = []
    for key, src, out, label in PAGES:
        ep = eps.get(key, "")
        if not ep:
            print(f"略過 {key}：還沒有後端網址（建好 Sheet 後用 --endpoint {key}=網址）")
            continue
        html = (ROOT / src).read_text(encoding="utf-8")
        if "__ENDPOINT__" not in html:
            raise SystemExit(f"{src} 裡找不到 __ENDPOINT__")
        html = html.replace("__ENDPOINT__", ep)
        dst = SITE / out
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(wrap(html), encoding="utf-8")
        links.append(f'<li><a href="{out.rsplit("/", 1)[0]}/">{label}</a></li>')
        print(f"wrote {dst.relative_to(ROOT)}  →  {key} 的 Sheet")

    index = HEAD + """<title>Introduction to Linguistics: Practice</title>
<style>
body{margin:0;padding:0 16px;font-family:system-ui,sans-serif;background:#F2F4F7;color:#1B2230;line-height:1.7}
main{max-width:640px;margin:0 auto;padding-block:48px}
h1{font-size:28px;margin:0 0 16px}
a{color:#2F5BD3}
@media (prefers-color-scheme: dark){body{background:#12151C;color:#E6E9EF}a{color:#8FA8F7}}
</style>
</head>
<body><main><h1>Introduction to Linguistics: Practice</h1><ul>
""" + "\n".join(links) + "\n</ul></main></body></html>\n"
    (SITE / "index.html").write_text(index, encoding="utf-8")
    print("wrote docs/index.html")


if __name__ == "__main__":
    main()
