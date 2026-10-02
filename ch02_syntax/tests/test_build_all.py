import sys, pathlib, json
from playwright.sync_api import sync_playwright
SEED = "localStorage.setItem('ling_student', JSON.stringify({sid:'Z00000000',name:'Test'})); localStorage.setItem('ling_syntax_tutorial_seen','true');"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from build_site import wrap
src = (pathlib.Path(__file__).resolve().parents[1] / "tree_lab.src.html").read_text(encoding="utf-8")
out = pathlib.Path("page.html"); out.write_text(wrap(src), encoding="utf-8")
MODE = sys.argv[1] if len(sys.argv) > 1 else "mouse"
QUICK = MODE == "quick"
if QUICK: MODE = "mouse"
log = open(f"t3_{MODE}.log","w",encoding="utf-8")
def P(*a): print(*a, file=log, flush=True)
fails = []
def check(cond, what):
    P(("PASS " if cond else "FAIL ") + what)
    if not cond: fails.append(what)

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    if MODE == "touch":
        c = b.new_context(viewport={"width":390,"height":844}, has_touch=True, is_mobile=True, device_scale_factor=2); c.add_init_script(SEED)
    else:
        c = b.new_context(viewport={"width":1100,"height":900}); c.add_init_script(SEED)
    pg = c.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(out.resolve().as_uri()); pg.wait_for_timeout(500)
    cdp = c.new_cdp_session(pg)
    def T(t, x, y): cdp.send("Input.dispatchTouchEvent", {"type":t, "touchPoints":([] if t=="touchEnd" else [{"x":x,"y":y}])})
    def down(x,y): T("touchStart",x,y) if MODE=="touch" else (pg.mouse.move(x,y), pg.mouse.down())
    def move(x,y): T("touchMove",x,y) if MODE=="touch" else pg.mouse.move(x,y)
    def up(): T("touchEnd",0,0) if MODE=="touch" else pg.mouse.up()
    def box(sel):
        r = pg.locator(sel).first.bounding_box(); return r["x"]+r["width"]/2, r["y"]+r["height"]/2
    def into_view(sel):   # 像使用者一樣先把畫布橫向捲到看得到目標
        import re
        m = re.search(r'data-(?:plus|n|w)="(\w+)"', sel)
        if not m: return
        i = m.group(1)
        pg.evaluate(f"""(()=>{{const e=document.querySelector('[data-n="{i}"],[data-w="{i}"]'); const w=document.querySelector('#cvwrap');
          if(!e) return; const r=e.getBoundingClientRect(), q=w.getBoundingClientRect();
          if(r.left < q.left+20 || r.right > q.right-20) w.scrollLeft += (r.left+r.right)/2 - (q.left+q.right)/2; }})()""")
    def drag(src_sel, tgt):
        into_view(src_sel)
        if not callable(tgt): into_view(tgt)
        x,y = box(src_sel); down(x,y); pg.wait_for_timeout(20)
        for k in range(1,4): move(x+2*k, y-3*k); pg.wait_for_timeout(15)
        tx,ty = tgt() if callable(tgt) else box(tgt)
        for k in range(1,9): move(x+(tx-x)*k/8, y+(ty-y)*k/8); pg.wait_for_timeout(15)
        up(); pg.wait_for_timeout(60)
    def state(): return pg.evaluate("JSON.stringify({nodes:S[cur].nodes, par:S[cur].par})")
    def show_canvas():
        pg.evaluate("document.querySelector('#cvwrap').scrollIntoView({block:'start'})"); pg.wait_for_timeout(40)
    def build(key_tree):
        """照標準答案由下往上做：單一子節點用 +，多個子節點先丟空白處再一個個拖上去"""
        def go(n):
            if "w" in n: return "w%d" % n["i"]
            kids = [go(k) for k in n["k"]]
            show_canvas()
            before = set(json.loads(state())["nodes"])
            if len(kids) == 1:
                drag(f'.chip[data-l="{n["l"]}"]', f'[data-plus="{kids[0]}"]')
            else:
                def spot():
                    xs = [box(f'[data-n="{k}"],[data-w="{k}"]') for k in kids]
                    return (xs[0][0]+xs[-1][0])/2, min(y for _,y in xs) - 55
                drag(f'.chip[data-l="{n["l"]}"]', spot)
            new = set(json.loads(state())["nodes"]) - before
            if len(new) != 1: pg.screenshot(path="fail2.png"); P("DBG", state(), pg.evaluate("[cur, scrollY, JSON.stringify(document.querySelector('#cv').getBoundingClientRect())]"))
            assert len(new) == 1, f"no node created for {n['l']}"
            nid = new.pop()
            if len(kids) > 1:
                for k in kids:
                    show_canvas(); a = box(f'[data-n="{k}"],[data-w="{k}"]'); bb_ = box(f'[data-n="{nid}"]')
                    drag(f'[data-n="{k}"],[data-w="{k}"]', f'[data-n="{nid}"]')
                    ok = json.loads(state())["par"].get(k) == nid
                    if not ok: P("connect fail", k, "->", nid, a, bb_, pg.evaluate("[scrollY, document.querySelector('#cvwrap').scrollLeft]")); pg.screenshot(path="fail.png")
            return nid
        go(key_tree)
    n_items = pg.evaluate("ITEMS.length")
    for i in range(99 if QUICK else 0, n_items):
        pg.evaluate(f"cur={i}; render()"); pg.wait_for_timeout(80)
        keys = pg.evaluate("ITEMS[cur].keys.map(k=>k.tree)")
        for ki, kt in enumerate(keys):
            if ki: pg.locator("#again").click(); pg.locator("#clear").click(); pg.wait_for_timeout(40)
            try: build(kt)
            except AssertionError as e: check(False, f"item {i} key {ki}: {e}"); continue
            if pg.locator("#why").count(): pg.fill("#why", "Because the verb takes the object NP as its complement inside V'.")
            sub = pg.locator("#submit"); check(sub.is_enabled(), f"item {i} key {ki}: submit enabled (status: {pg.locator('#need').inner_text()})")
            if sub.is_enabled():
                sub.click(); pg.wait_for_timeout(60)
                v = pg.locator("#result .verdict").inner_text(); check(v == "Correct", f"item {i} key {ki}: verdict={v}")
            if i == 0 and ki == 0: pg.screenshot(path=f"done_{MODE}.png", full_page=True)
    # 錯的樹：14a 少 N'
    pg.evaluate("cur=1; render()"); pg.locator("#again").click(); pg.locator("#clear").click()
    kt = pg.evaluate("ITEMS[1].tree")
    def strip(n):
        if "w" in n: return n
        if n["l"] == "N'" : return strip(n["k"][0])
        return {"l":n["l"], "k":[strip(k) for k in n["k"]]}
    build(strip(kt)) if not QUICK else None
    if not QUICK: pg.fill("#why", "Because the verb takes the object NP as its complement inside V'."); pg.locator("#submit").click(); pg.wait_for_timeout(60)
    r = pg.locator("#result .expl").inner_text()
    check(r.startswith("Not quite") and "Missing" in r and "N'" in r, "wrong tree feedback: " + r[:120].replace("\n"," | "))
    # 編輯工具：在練習句上
    pg.evaluate("cur=0; S[0]=({nodes:{}, par:{}, nid:1, hist:[], sel:null, link:null, done:false, ok:null}); render()")
    show_canvas()
    drag('.chip[data-l="N"]', '[data-plus="w1"]'); n1 = list(json.loads(state())["nodes"])[0]
    drag(".chip[data-l=\"N'\"]", f'[data-plus="{n1}"]')
    st = json.loads(state()); check(len(st["nodes"]) == 2 and st["par"].get(n1), "stack N' on N via +")
    n2 = [k for k in st["nodes"] if k != n1][0]
    # 換標籤：把 V' 丟到 N' 上
    show_canvas(); drag(".chip[data-l=\"V'\"]", f'[data-n="{n2}"]')
    check(json.loads(state())["nodes"][n2]["l"] == "V'", "relabel by dropping on node")
    pg.locator("#undo").click(); check(json.loads(state())["nodes"][n2]["l"] == "N'", "undo relabel")
    # 環：把 N' 拖到 N 底下 → 應拒絕
    show_canvas(); drag(f'[data-n="{n2}"]', f'[data-n="{n1}"]')
    check(json.loads(state())["par"].get(n2) != n1, "cycle refused")
    # 剪線：真的點在線的中間
    show_canvas()
    mid = pg.evaluate(f"""(()=>{{const l=document.querySelector('[data-e="{n1}"] .ln'), r=document.querySelector('#cv').getBoundingClientRect();
      return [r.left+(+l.getAttribute('x1')+ +l.getAttribute('x2'))/2, r.top+(+l.getAttribute('y1')+ +l.getAttribute('y2'))/2]}})()""")
    if MODE == "touch": pg.touchscreen.tap(*mid)
    else: pg.mouse.click(*mid)
    pg.wait_for_timeout(50)
    check(n1 not in json.loads(state())["par"], "tap line cuts it")
    # 拖到 Delete
    drag(f'[data-n="{n2}"]', "#trash"); check(n2 not in json.loads(state())["nodes"], "drag node to Delete")
    # 線交叉：TP → NP(a, +pst) VP(dog, bark)
    pg.locator("#clear").click(); show_canvas()
    def above(*ws, dy=150):
        def f():
            pts = [box(f'[data-w="{w}"]') for w in ws]; return (pts[0][0]+pts[-1][0])/2, pts[0][1]-dy
        return f
    def newest(l): return [k for k,v in json.loads(state())["nodes"].items() if v["l"]==l][-1]
    drag('.chip[data-l="NP"]', above("w0","w2", dy=90)); np_ = newest("NP")
    for w in ("w0","w2"): show_canvas(); drag(f'[data-w="{w}"]', f'[data-n="{np_}"]')
    show_canvas(); drag('.chip[data-l="VP"]', above("w1","w3", dy=150)); vp = newest("VP")
    for w in ("w1","w3"): show_canvas(); drag(f'[data-w="{w}"]', f'[data-n="{vp}"]')
    show_canvas(); drag('.chip[data-l="TP"]', above("w0","w3", dy=230)); tp = newest("TP")
    for n in (np_, vp): show_canvas(); drag(f'[data-n="{n}"]', f'[data-n="{tp}"]')
    P("cross state", state()); show_canvas(); pg.screenshot(path="cross.png")
    msg = pg.locator("#need").inner_text(); check("cross" in msg, "crossing lines message: " + msg)
    sw = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]"); check(sw[0] <= sw[1], f"no page horizontal scroll {sw}")
    check(not errs, f"no JS errors {errs}")
    P("TOTAL FAILS:", len(fails))
    b.close()
