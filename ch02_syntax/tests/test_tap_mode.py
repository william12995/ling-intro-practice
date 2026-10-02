import sys, pathlib, json
from playwright.sync_api import sync_playwright
SEED = "localStorage.setItem('ling_student', JSON.stringify({sid:'Z00000000',name:'Test'})); localStorage.setItem('ling_syntax_tutorial_seen','true');"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from build_site import wrap
src = (pathlib.Path(__file__).resolve().parents[1] / "tree_lab.src.html").read_text(encoding="utf-8")
out = pathlib.Path("page.html"); out.write_text(wrap(src), encoding="utf-8"); fails=[]
def check(c, w): print(("PASS " if c else "FAIL ")+w); (None if c else fails.append(w))
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    c = b.new_context(viewport={"width":390,"height":844}, has_touch=True, is_mobile=True, device_scale_factor=2); c.add_init_script(SEED)
    pg = c.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(out.resolve().as_uri()); pg.wait_for_timeout(500)
    st = lambda: json.loads(pg.evaluate("JSON.stringify({nodes:S[cur].nodes, par:S[cur].par, sel:S[cur].sel})"))
    pg.evaluate("document.querySelector('#cvwrap').scrollIntoView({block:'start'})")
    # 點選模式：點 Det → 點 a 上的 +
    pg.locator('.chip[data-l="Det"]').tap(); pg.locator('[data-plus="w0"]').tap()
    s = st(); check(any(v["l"]=="Det" for v in s["nodes"].values()) and "w0" in s["par"], "tap label then tap +")
    # 點 NP → 點空白處
    pg.locator('.chip[data-l="NP"]').tap()
    r = pg.locator("#cv").bounding_box(); pg.touchscreen.tap(r["x"]+120, r["y"]+60)
    pg.locator('.chip[data-l="NP"]').tap()   # 取消
    s = st(); np_ = [k for k,v in s["nodes"].items() if v["l"]=="NP"]; check(len(np_)==1, "tap label then tap empty spot")
    det = [k for k,v in s["nodes"].items() if v["l"]=="Det"][0]
    # 點 Det 選起來 → 點 NP：Det 接到 NP 底下
    pg.locator(f'[data-n="{det}"]').tap(); check(st()["sel"]==det, "tap node selects it")
    check("goes under" in pg.locator("#msg").inner_text(), "select hint shown")
    pg.locator(f'[data-n="{np_[0]}"]').tap(); s = st(); check(s["par"].get(det)==np_[0] and not s["sel"], "tap piece then tap parent attaches")
    # 選了詞 → 點節點
    pg.locator('[data-w="w1"]').tap(); pg.locator(f'[data-n="{np_[0]}"]').tap(); check(st()["par"].get("w1")==np_[0], "tap word then tap node attaches")
    # ✕ 刪除
    pg.locator(f'[data-n="{np_[0]}"]').tap(); pg.locator(f'[data-del="{np_[0]}"]').tap(); check(np_[0] not in st()["nodes"], "tap x deletes")
    # 橫向自動捲：14a 拖 Det 到右邊緣
    pg.evaluate("cur=1; render()"); pg.evaluate("document.querySelector('#cvwrap').scrollIntoView({block:'start'})"); pg.wait_for_timeout(50)
    cdp = c.new_cdp_session(pg)
    T = lambda t,x,y: cdp.send("Input.dispatchTouchEvent", {"type":t, "touchPoints":([] if t=="touchEnd" else [{"x":x,"y":y}])})
    cb = pg.locator('.chip[data-l="Det"]').bounding_box(); x,y = cb["x"]+10, cb["y"]+10
    w = pg.locator("#cvwrap").bounding_box()
    T("touchStart",x,y)
    for k in range(1,6): T("touchMove", x+(w["x"]+w["width"]-12-x)*k/5, w["y"]+w["height"]-90); pg.wait_for_timeout(20)
    for k in range(25): T("touchMove", w["x"]+w["width"]-12, w["y"]+w["height"]-90+(k%2)); pg.wait_for_timeout(15)
    T("touchEnd",0,0); pg.wait_for_timeout(50)
    check(pg.evaluate("document.querySelector('#cvwrap').scrollLeft") > 0, "horizontal autoscroll at canvas edge")
    # 空白處滑動可以捲頁面
    y0 = pg.evaluate("scrollY"); r = pg.locator("#cv").bounding_box()
    T("touchStart", r["x"]+150, r["y"]+200)
    for k in range(1,8): T("touchMove", r["x"]+150, r["y"]+200-15*k); pg.wait_for_timeout(15)
    T("touchEnd",0,0); pg.wait_for_timeout(50)
    check(pg.evaluate("scrollY") > y0, f"swipe on empty canvas scrolls page ({y0} -> {pg.evaluate('scrollY')})")
    check(not errs, f"no JS errors {errs}")
    print("FAILS", len(fails)); b.close()
