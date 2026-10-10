import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from build_site import wrap
from playwright.sync_api import sync_playwright
src = (pathlib.Path(__file__).resolve().parents[1] / "morph_tree.src.html").read_text(encoding="utf-8")
out = pathlib.Path("page.html"); out.write_text(wrap(src), encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    for vw in [(1100,900),(390,844)]:
        c = b.new_context(viewport={"width":vw[0],"height":vw[1]}, has_touch=vw[0]<500, is_mobile=vw[0]<500, device_scale_factor=2 if vw[0]<500 else 1)
        pg = c.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(out.resolve().as_uri()); pg.wait_for_timeout(500)
        pg.screenshot(path=f"s_login_{vw[0]}.png")
        pg.fill("#sid","b13012345"); pg.fill("#sname","Test"); pg.click("button[type=submit]"); pg.wait_for_timeout(300)
        print(vw, "tutorial open:", pg.locator(".tut").count())
        for k in range(4):
            pg.wait_for_timeout(1500 + 300*k); pg.screenshot(path=f"s_tut{k}_{vw[0]}.png")
            pg.click("#tut-next")
        pg.wait_for_timeout(300); print("tutorial closed:", pg.locator(".tut").count()==0, "seen:", pg.evaluate("localStorage.getItem('ling_morph_tree_tutorial_seen')"))
        pg.screenshot(path=f"s_main_{vw[0]}.png", full_page=True)
        print("coach:", pg.locator("#coach").inner_text()[:120].replace("\n"," | "))
        print("errors:", errs); c.close()
    b.close()
