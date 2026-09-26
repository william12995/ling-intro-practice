"""把各章的 *.src.html 包成可以放上 GitHub Pages 的完整網頁，輸出到 docs/（GitHub Pages 設定成從 main 分支的 /docs 發布）。

src 檔沒有 <!doctype>/<head>（它同時拿來發布成 claude.ai artifact，外殼由平台補），
這支腳本補上 doctype、charset、viewport，並把 __ENDPOINT__ 換成 Apps Script 網址。

用法：
    python build_site.py --endpoint "https://script.google.com/macros/s/XXXX/exec"
    python build_site.py            # 不給網址：成績只存在學生自己的瀏覽器
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "docs"
PAGES = [  # (src, 輸出路徑, 首頁上顯示的名稱)
    ("ch01_morphology/morphology_lab.src.html", "ch01_morphology/index.html", "Morphology"),
]

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
    ap.add_argument("--endpoint", default="", help="Apps Script 網頁應用程式網址（/exec 結尾）")
    a = ap.parse_args()
    ep = a.endpoint.strip()
    if ep and not re.match(r"^https://script\.google\.com/macros/s/[^/]+/exec$", ep):
        raise SystemExit(f"網址格式不對，應該長得像 https://script.google.com/macros/s/XXXX/exec ：{ep}")

    SITE.mkdir(exist_ok=True)
    (SITE / ".nojekyll").write_text("", encoding="utf-8")   # 關掉 GitHub Pages 的 Jekyll
    links = []
    for src, out, label in PAGES:
        html = (ROOT / src).read_text(encoding="utf-8")
        if "__ENDPOINT__" not in html:
            raise SystemExit(f"{src} 裡找不到 __ENDPOINT__")
        if ep:
            html = html.replace("__ENDPOINT__", ep)
        dst = SITE / out
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(wrap(html), encoding="utf-8")
        links.append(f'<li><a href="{out.rsplit("/", 1)[0]}/">{label}</a></li>')
        print(f"wrote {dst.relative_to(ROOT)}")

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
    print(f"wrote docs/index.html；後端：{ep or '未設定（只存本機）'}")


if __name__ == "__main__":
    main()
