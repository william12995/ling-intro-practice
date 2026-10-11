"""本機跑句法、構詞樹兩頁選擇題：每題所有候選樹的葉子要一樣、標準答案要在範圍內；
登入後每題選對的送出，再挑一題選錯的。結果寫 mc_<頁>_<寬>.log（UTF-8）。"""
import sys, pathlib, json
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from build_site import wrap
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
PAGES = {"syntax": "ch02_syntax/tree_lab.src.html", "morph": "ch01-2_morph_tree/morph_tree.src.html"}
CHECK = """() => ITEMS.map((it, k) => {
  const leaves = b => { const o = []; (function w(n){ n.w !== undefined ? o.push(n.w) : n.k.forEach(w); })(fromBracket(b)); return o.join(" "); };
  const ls = it.opts.map(leaves), bad = [];
  if(new Set(ls).size !== 1) bad.push("leaves differ: " + ls.join(" / "));
  if(new Set(it.opts.map(b => bracket(fromBracket(b)))).size !== it.opts.length) bad.push("duplicate options");
  [].concat(it.ans).forEach(a => { if(!(a >= 0 && a < it.opts.length)) bad.push("ans out of range"); });
  return bad.length ? `item ${k} ${it.say}: ${bad.join("; ")}` : null;
}).filter(Boolean)"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    for name, src in PAGES.items():
        page = HERE / f"mc_{name}.html"; page.write_text(wrap((ROOT / src).read_text(encoding="utf-8")), encoding="utf-8")
        for vw in [(1100, 900), (390, 844)]:
            log = []; c = b.new_context(viewport={"width": vw[0], "height": vw[1]}, has_touch=vw[0] < 500)
            pg = c.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(page.as_uri()); pg.wait_for_timeout(400)
            pg.fill("#sid", "Z00000000"); pg.fill("#sname", "Test"); pg.click("button[type=submit]"); pg.wait_for_timeout(300)
            log.append("item problems: " + json.dumps(pg.evaluate(CHECK), ensure_ascii=False))
            n = pg.evaluate("ITEMS.length"); wide = 0
            for k in range(n):
                pg.click(f'[data-go="{k}"]'); pg.wait_for_timeout(80)
                ans = pg.evaluate(f"[].concat(ITEMS[{k}].ans)[0]")
                pick = ans if k != 2 else (ans + 1) % 2   # 第 2 題故意選錯
                pg.locator('input[name="pick"]').nth(pick).check()
                pg.fill("#why", "Test argument: replace the phrase with it.")
                pg.click("#submit"); pg.wait_for_timeout(80)
                wide = max(wide, pg.evaluate("document.documentElement.scrollWidth"))
                if k in (0, 2, n - 1): pg.screenshot(path=str(HERE / f"mc_{name}_{k}_{vw[0]}.png"), full_page=True)
            log.append("state: " + pg.evaluate("JSON.stringify(S.map(s => s.ok))"))
            pg.reload(); pg.wait_for_timeout(400)
            log.append(f"after reload ok dots: {pg.locator('.dot.ok').count()} no dots: {pg.locator('.dot.no').count()}")
            log.append(f"max scrollWidth {wide} vs {vw[0]}")
            log.append("errors: " + json.dumps(errs))
            (HERE / f"mc_{name}_{vw[0]}.log").write_text("\n".join(log), encoding="utf-8")
            c.close()
    b.close()
