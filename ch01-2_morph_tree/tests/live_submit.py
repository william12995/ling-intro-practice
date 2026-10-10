"""用 docs/ 裡建好的正式頁（不 mock 後端）以測試學號送一題 S1-11，看頁面是否顯示 Answers recorded。送完要到 Sheet 刪掉測試列。"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
page = pathlib.Path(__file__).resolve().parents[2] / "docs" / "ch01-2_morph_tree" / "index.html"
SEED = "localStorage.setItem('ling_student', JSON.stringify({sid:'Z00000000',name:'TEST-delete-me'})); localStorage.setItem('ling_morph_tree_tutorial_seen','true');"
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge"); c = b.new_context(); c.add_init_script(SEED)
    pg = c.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(page.as_uri()); pg.wait_for_timeout(800)
    pg.evaluate("cur=11; render()")
    tree = pg.evaluate("ITEMS[11].tree")
    nodes, par, n = {}, {}, [0]
    def go(x):
        if "w" in x: return "w%d" % x["i"]
        n[0] += 1; nid = "n%d" % n[0]; nodes[nid] = {"l": x["l"], "x": 0, "h": 1}
        for k in x["k"]: par[go(k)] = nid
        return nid
    go(tree)
    pg.evaluate(f"S[11].nodes={json.dumps(nodes)}; S[11].par={json.dumps(par)}; S[11].nid=99; refresh()")
    pg.fill("#why", "live test: un- attaches to the verb lock first, then -able.")
    pg.click("#submit")
    for _ in range(40):
        pg.wait_for_timeout(500)
        t = pg.locator("#sync").inner_text()
        if "recorded" in t: break
    print("verdict:", pg.locator("#result .verdict").inner_text(), "| sync:", t, "| errors:", errs)
    b.close()
