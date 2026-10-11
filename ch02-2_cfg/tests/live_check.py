"""線上頁面送一題（Z00000000），看上傳狀態。"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge"); pg = b.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("https://william12995.github.io/ling-intro-practice/ch02-2_cfg/"); pg.wait_for_timeout(1500)
    pg.fill("#sid", "Z00000000"); pg.fill("#sname", "Test"); pg.click("button[type=submit]"); pg.wait_for_timeout(300)
    pg.click('[data-go="1"]'); pg.wait_for_timeout(200)
    pg.fill("#gram", pg.evaluate("ITEMS[1].sample")); pg.click("#run")
    pg.locator('input[name="pick"]').nth(0).check()
    pg.fill("#why", "TEST ROW - substitution: John put it on the desk.")
    pg.click("#submit")
    for _ in range(30):
        pg.wait_for_timeout(1000)
        s = pg.locator("#sync").inner_text()
        if "recorded" in s or "not accepted" in s: break
    print("sync:", s, "| queue:", pg.evaluate("localStorage.getItem('ling_queue_ch02_cfg')"), "| errors:", errs)
    b.close()
