"""本機跑整頁：登入、每題用標準文法畫樹、寫論證送出；另外直接測剖析器的邊界情況。結果寫 t_<w>.log（UTF-8）。"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from build_site import wrap
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
src = (HERE.parent / "cfg_lab.src.html").read_text(encoding="utf-8")
out = HERE / "page.html"; out.write_text(wrap(src), encoding="utf-8")
CASES = {  # 文法, 句子 → 期望的 summary 開頭
 "ok": ("S -> NP VP\nVP -> V NP PP\nNP -> 'John' | Det N\nPP -> P NP\nV -> 'put'\nDet -> 'the'\nN -> 'book' | 'desk'\nP -> 'on'", "1 tree"),
 "ambig": ("S -> NP VP\nVP -> V NP PP | V NP\nNP -> 'John' | Det N | NP PP\nPP -> P NP\nV -> 'put'\nDet -> 'the'\nN -> 'book' | 'desk'\nP -> 'on'", "2 tree"),
 "unquoted": ("S -> NP VP\nNP -> John", "missing"),
 "arrow": ("S -> NP VP\nNP => 'John'", "grammar error"),
 "noparse": ("S -> NP VP\nVP -> V NP\nPP -> P NP\nNP -> 'John' | Det N\nV -> 'put'\nDet -> 'the'\nN -> 'book' | 'desk'\nP -> 'on'", "no tree"),
 "loop": ("S -> NP VP\nVP -> V NP PP\nNP -> NP | 'John' | Det N\nPP -> P NP\nV -> 'put'\nDet -> 'the'\nN -> 'book' | 'desk'\nP -> 'on'", "1 tree"),
 "leftrec": ("S -> NP VP\nVP -> VP PP | V NP | VP PP PP\nNP -> 'John' | Det N | NP PP\nPP -> P NP\nV -> 'put'\nDet -> 'the'\nN -> 'book' | 'desk'\nP -> 'on'", "2 tree"),
 "smartquote": ("S → NP VP\nVP -> V NP PP\nNP -> ‘John’ | Det N\nPP -> P NP\nV -> 'put'\nDet -> 'the'\nN -> 'book' | \"desk\"\nP -> 'on'  # comment", "1 tree"),
 "contline": ("S -> NP VP\nVP -> V NP PP\nNP -> 'John'\n   | Det N\nPP -> P NP\nV -> 'put'\nDet -> 'the'\nN -> 'book' | 'desk'\nP -> 'on'", "1 tree"),
 "unclosed": ("S -> NP VP\nNP -> 'John", "grammar error"),
}
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    for vw in [(1100, 900), (390, 844)]:
        log = []
        c = b.new_context(viewport={"width": vw[0], "height": vw[1]}, has_touch=vw[0] < 500)
        pg = c.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(out.as_uri()); pg.wait_for_timeout(400)
        pg.fill("#sid", "Z00000000"); pg.fill("#sname", "Test"); pg.click("button[type=submit]"); pg.wait_for_timeout(300)
        it1 = {"say": "John put the book on the desk"}
        for k, (g, want) in CASES.items():
            s = pg.evaluate("([g, it]) => runGrammar(g, it).summary", [g, it1])
            log.append(f"{'PASS' if s.startswith(want) else 'FAIL'} {k}: {s[:110]}")
        # 練習題
        pg.click("#run"); pg.wait_for_timeout(200)
        log.append("practice trees: " + str(pg.locator("#out svg.tree").count()))
        pg.screenshot(path=str(HERE / f"p0_{vw[0]}.png"), full_page=True)
        n = pg.evaluate("ITEMS.length")
        for k in range(1, n):
            pg.click(f'[data-go="{k}"]'); pg.wait_for_timeout(150)
            sample = pg.evaluate(f"ITEMS[{k}].sample")
            pg.fill("#gram", sample); pg.click("#run"); pg.wait_for_timeout(150)
            log.append(f"item {k} out: " + pg.locator("#out").inner_text()[:120].replace("\n", " | "))
            if not pg.evaluate(f"!!ITEMS[{k}].final"):
                log.append(f"item {k} before: " + pg.locator("#need").inner_text())
                pg.fill("#why", "Substitution test: I can replace the phrase with it.")
                log.append(f"item {k} ready: " + pg.locator("#need").inner_text())
                pg.click("#submit"); pg.wait_for_timeout(150)
            else:
                pg.click("#gsub"); pg.wait_for_timeout(150)
            log.append(f"item {k} verdict: " + pg.locator(".verdict").inner_text())
            pg.screenshot(path=str(HERE / f"p{k}_{vw[0]}.png"), full_page=True)
        prog = pg.evaluate("JSON.stringify(S.map(s=>[s.done,s.gdone,s.attempt]))")
        log.append("state: " + prog)
        # 重新整理後進度還在
        pg.reload(); pg.wait_for_timeout(400)
        log.append("after reload dots done: " + str(pg.locator(".dot.done").count()))
        sw = pg.evaluate("document.documentElement.scrollWidth"); log.append(f"scrollWidth {sw} vs {vw[0]}")
        log.append("errors: " + json.dumps(errs))
        (HERE / f"t_{vw[0]}.log").write_text("\n".join(log), encoding="utf-8")
        c.close()
    b.close()
