"""接真的後端測四頁的「回報題目」和「My answers」，再本機測 ch01 的「只重做答錯的」。
用 docs/ 裡已經 build 好、帶後端網址的頁面，學號 Z00000000（分析時要排除）。結果寫 report_history.log（UTF-8）。"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
PAGES = {"ch01": "docs/ch01_morphology/index.html", "morph": "docs/ch01-2_morph_tree/index.html",
         "syntax": "docs/ch02_syntax/index.html", "cfg": "docs/ch02-2_cfg/index.html"}
log = []


def answer_one(name, pg):
    """每頁答一題，讓 My answers 有東西可列。"""
    if name == "ch01":
        pg.locator(".opt").first.click()
        pg.fill("#why", "Test reasoning: comparing the forms of the word.")
        pg.click("#submit")
    elif name in ("morph", "syntax"):
        pg.click('[data-go="1"]'); pg.wait_for_timeout(100)
        pg.locator('input[name="pick"]').first.check()
        pg.fill("#why", "Test argument: replace the phrase with it.")
        pg.click("#submit")
    else:
        pg.click('[data-go="1"]'); pg.wait_for_timeout(100)
        pg.evaluate("document.querySelector('#gram').value = ITEMS[1].sample; document.querySelector('#gram').dispatchEvent(new Event('input'))")
        pg.click("#run")
        pg.fill("#why", "Test argument: the book can be replaced by it.")
        pg.click("#submit")
    pg.wait_for_timeout(300)


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    for name, rel in PAGES.items():
        for vw in [(1100, 900), (390, 844)]:
            c = b.new_context(viewport={"width": vw[0], "height": vw[1]}, has_touch=vw[0] < 500)
            pg = c.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto((ROOT / rel).as_uri()); pg.wait_for_timeout(500)
            pg.fill("#sid", "Z00000000"); pg.fill("#sname", "Test"); pg.click("button[type=submit]"); pg.wait_for_timeout(400)
            tag = f"{name} {vw[0]}"
            if vw[0] == 1100:   # 只在桌機送真的資料，避免 Sheet 多太多測試列
                answer_one(name, pg)
                pg.locator("[data-report] [data-open]").click()
                pg.fill("#rnote", f"Test report from automated check ({name}).")
                pg.locator("[data-report] [data-send]").click()
                pg.wait_for_selector("[data-report] .hint", timeout=30000)
                log.append(f"{tag} report: {pg.locator('[data-report]').inner_text()!r}")
                pg.wait_for_function("JSON.parse(localStorage.getItem(QKEY) || '[]').length === 0", timeout=60000)
            else:
                log.append(f"{tag} report link: {pg.locator('[data-report] [data-open]').count()}")
            pg.click("#hist")
            pg.wait_for_function("document.getElementById('hstat') && !/Loading/.test(document.getElementById('hstat').textContent)", timeout=60000)
            log.append(f"{tag} history: {pg.locator('#hstat').inner_text()!r}, items {pg.locator('.hitem').count()}, attempts {pg.locator('.hatt').count()}")
            if pg.locator(".hitem").count():
                log.append(f"{tag} first item: {pg.locator('.hitem').first.inner_text()[:300]!r}")
                pg.locator(".hitem summary").first.click()
            pg.screenshot(path=str(HERE / f"rh_{name}_{vw[0]}.png"), full_page=True)
            log.append(f"{tag} scrollWidth {pg.evaluate('document.documentElement.scrollWidth')} vs {vw[0]}")
            pg.click("#hback"); pg.wait_for_timeout(300)
            log.append(f"{tag} back to practice: {pg.locator('#hist').count() == 1 and pg.locator('.hitem').count() == 0}")
            log.append(f"{tag} errors: {errs}")
            c.close()

    # ch01 只重做答錯的（本機，不送資料）：把第 1 部分做成兩題錯，按按鈕後只清那兩題，重新載入後也還是未作答
    c = b.new_context(); pg = c.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((ROOT / PAGES["ch01"]).as_uri()); pg.wait_for_timeout(400)
    pg.fill("#sid", "Z00000000"); pg.fill("#sname", "Test"); pg.click("button[type=submit]"); pg.wait_for_timeout(300)
    pg.evaluate("""() => { const S = state.bySec[0], n = SECTIONS[0].items.length;
      S.res = SECTIONS[0].items.map((_, k) => k === 1 || k === 3 ? false : true);
      SECTIONS[0].items.forEach((_, k) => { S.ans[k] = 0; S.why[k] = 'x'.repeat(30); });
      S.i = n; state.lv = 0; saveProg(); renderSec(); }""")
    log.append(f"redo button: {pg.locator('#redo-wrong').inner_text()!r}")
    pg.click("#redo-wrong"); pg.wait_for_timeout(200)
    log.append(f"after redo: i={pg.evaluate('state.bySec[0].i')} res={pg.evaluate('JSON.stringify(state.bySec[0].res)')} attempt={pg.evaluate('state.bySec[0].attempt')}")
    pg.reload(); pg.wait_for_timeout(400)
    log.append(f"after reload: res1={pg.evaluate('String(state.bySec[0].res[1])')} res3={pg.evaluate('String(state.bySec[0].res[3])')} submit enabled-able: {pg.locator('#submit').count()}")
    log.append(f"redo errors: {errs}")
    pg.evaluate("localStorage.removeItem(progKey())")
    c.close()
    b.close()

(HERE / "report_history.log").write_text("\n".join(log), encoding="utf-8")
