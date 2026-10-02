# 針對 code review 修正的回歸測試
import sys, pathlib, json
from playwright.sync_api import sync_playwright
SEED = "localStorage.setItem('ling_student', JSON.stringify({sid:'Z00000000',name:'Test'})); localStorage.setItem('ling_syntax_tutorial_seen','true');"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from build_site import wrap
src = (pathlib.Path(__file__).resolve().parents[1] / "tree_lab.src.html").read_text(encoding="utf-8")
out = pathlib.Path("page.html"); out.write_text(wrap(src), encoding="utf-8")
fails = []
def check(c, w): print(("PASS " if c else "FAIL ") + w); (None if c else fails.append(w))
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    c = b.new_context(viewport={"width":1100,"height":900}); c.add_init_script(SEED)
    pg = c.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(out.resolve().as_uri()); pg.wait_for_timeout(500)
    st = lambda: json.loads(pg.evaluate("JSON.stringify({nodes:S[cur].nodes, par:S[cur].par, sel:S[cur].sel})"))
    setstate = lambda nodes, par: pg.evaluate(f"S[cur].nodes={json.dumps(nodes)}; S[cur].par={json.dumps(par)}; S[cur].nid=50; refresh()")
    coach = lambda: pg.locator("#coach").inner_text()

    # 1. coach：NP 多接了 T，應該叫學生剪 T，不是剪 a
    setstate({"n1":{"l":"Det","x":0,"h":1},"n2":{"l":"N","x":0,"h":1},"n3":{"l":"N'","x":0,"h":2},"n4":{"l":"NP","x":0,"h":3},"n5":{"l":"T","x":0,"h":1}},
             {"w0":"n1","w1":"n2","n2":"n3","n1":"n4","n3":"n4","n5":"n4","w2":"n5"})
    t = coach(); check("T" in t and "belong" in t and "a is" not in t, "coach: cut the extra child first -> " + t.split("\n")[0])
    # 1b. 少接一個又多接一個：NP 底下 Det、T
    setstate({"n1":{"l":"Det","x":0,"h":1},"n2":{"l":"N","x":0,"h":1},"n3":{"l":"N'","x":0,"h":2},"n4":{"l":"NP","x":0,"h":3},"n5":{"l":"T","x":0,"h":1}},
             {"w0":"n1","w1":"n2","n2":"n3","n1":"n4","n5":"n4","w2":"n5"})
    t = coach(); check("belong" in t and "T" in t, "coach: wrong extra + missing -> " + t.split("\n")[0])

    # 2. 重複的層級：N' over N' 要報多出來的那個
    pg.evaluate("cur=0; render()")
    setstate({"n1":{"l":"Det","x":0,"h":1},"n2":{"l":"N","x":0,"h":1},"n3":{"l":"N'","x":0,"h":2},"n9":{"l":"N'","x":0,"h":3},"n4":{"l":"NP","x":0,"h":4},
              "n5":{"l":"T","x":0,"h":1},"n6":{"l":"V","x":0,"h":1},"n7":{"l":"V'","x":0,"h":2},"n8":{"l":"VP","x":0,"h":3},"n10":{"l":"T'","x":0,"h":4},"n11":{"l":"TP","x":0,"h":5}},
             {"w0":"n1","w1":"n2","n2":"n3","n3":"n9","n1":"n4","n9":"n4","w2":"n5","w3":"n6","n6":"n7","n7":"n8","n5":"n10","n8":"n10","n4":"n11","n10":"n11"})
    pg.locator("#submit").click(); pg.wait_for_timeout(50)
    r = pg.locator("#result .expl").inner_text()
    check("second" in r and "N'" in r and pg.locator("#cv .node.bad").count() == 1, "duplicate level reported and marked red -> " + r.split("\n")[1][:80])
    pg.locator("#again").click()

    # 3. 多指：拖曳中第二根手指按下，不能留下殘影
    cdp = c.new_cdp_session(pg)
    pg.evaluate("S[0]=fresh(); render()")
    tc = b.new_context(viewport={"width":390,"height":844}, has_touch=True, is_mobile=True); tc.add_init_script(SEED)
    tp = tc.new_page(); tp.goto(out.resolve().as_uri()); tp.wait_for_timeout(400); tcdp = tc.new_cdp_session(tp)
    T = lambda t, pts: tcdp.send("Input.dispatchTouchEvent", {"type":t, "touchPoints":pts})
    bb = tp.locator('.chip[data-l="N"]').bounding_box(); x, y = bb["x"]+10, bb["y"]+10
    bb2 = tp.locator('.chip[data-l="V"]').bounding_box(); x2, y2 = bb2["x"]+10, bb2["y"]+10
    T("touchStart", [{"x":x,"y":y,"id":0}])
    for k in range(1,5): T("touchMove", [{"x":x+5*k,"y":y-20*k,"id":0}]); tp.wait_for_timeout(15)
    T("touchStart", [{"x":x+20,"y":y-80,"id":0},{"x":x2,"y":y2,"id":1}])
    T("touchMove", [{"x":x+20,"y":y-90,"id":0},{"x":x2+30,"y":y2-30,"id":1}])
    T("touchEnd", [{"x":x+20,"y":y-90,"id":0}]); T("touchEnd", []); tp.wait_for_timeout(80)
    check(tp.locator(".ghost").count() == 0, f"no stuck ghost after two-finger touch (ghosts={tp.locator('.ghost').count()})")
    tp.evaluate("cur=1; render()"); check(tp.locator(".ghost").count() == 0, "render clears ghosts")
    tc.close()

    # 4. 滑鼠在空白處拖、到畫布外放開，之後滑過畫布不該捲動
    pg.evaluate("document.querySelector('#cvwrap').scrollIntoView({block:'center'})"); pg.wait_for_timeout(50)
    r = pg.locator("#cv").bounding_box()
    pg.mouse.move(r["x"]+50, r["y"]+40); pg.mouse.down(); pg.mouse.move(r["x"]+60, r["y"]+60, steps=4)
    pg.mouse.move(r["x"]+60, r["y"]-200, steps=4); pg.mouse.up()
    y0 = pg.evaluate("scrollY"); pg.mouse.move(r["x"]+200, r["y"]+100, steps=5); pg.mouse.move(r["x"]+220, r["y"]+180, steps=5)
    check(pg.evaluate("scrollY") == y0 and pg.evaluate("drag") is None, "pan ends when mouse released outside")

    # 5. 縮放視窗：沒接東西的節點跟著詞走（也包括 undo 回來的）
    pg.evaluate("S[0]=fresh(); cur=0; render()")
    pg.evaluate("addFree('NP', G.wx[1], 60)")
    dx0 = pg.evaluate("L.pos.n1.x - G.wx[1]")
    pg.set_viewport_size({"width":700,"height":900}); pg.wait_for_timeout(400)
    dx1 = pg.evaluate("L.pos.n1.x - G.wx[1]")
    check(abs(dx0 - dx1) < 0.5, f"free node keeps position relative to words on resize ({dx0:.1f} vs {dx1:.1f})")
    pg.set_viewport_size({"width":1100,"height":900}); pg.wait_for_timeout(400)

    # 6. 點選模式：點已經接著的父節點要有回饋
    pg.evaluate("S[0]=fresh(); render()")
    setstate({"n1":{"l":"N","x":0,"h":1}}, {"w1":"n1"})
    pg.evaluate("document.querySelector('#cvwrap').scrollIntoView({block:'center'})")
    pg.locator('[data-w="w1"]').click(); pg.locator('[data-n="n1"]').click()
    check("already" in pg.locator("#msg").inner_text() and st()["sel"] is None, "feedback when tapping current parent")

    # 7. 鍵盤：Tab 到標籤按 Enter、Tab 到 + 按 Enter；選標籤後在畫布按 Enter 放空白處；選詞再選節點
    pg.evaluate("S[0]=fresh(); render()")
    pg.locator('.chip[data-l="Det"]').focus(); pg.keyboard.press("Enter")
    check(pg.evaluate("armed") == "Det", "keyboard Enter on chip arms it")
    pg.locator('[data-plus="w0"]').focus(); pg.keyboard.press("Enter")
    s1 = st(); check(any(v["l"]=="Det" for v in s1["nodes"].values()) and "w0" in s1["par"], "keyboard Enter on + places label")
    pg.locator('.chip[data-l="Det"]').focus(); pg.keyboard.press("Enter")   # 取消
    pg.locator('.chip[data-l="NP"]').focus(); pg.keyboard.press(" ")
    pg.locator("#cv").focus(); pg.keyboard.press("Enter")
    s2 = st(); np_ = [k for k,v in s2["nodes"].items() if v["l"]=="NP"]; check(len(np_) == 1, "keyboard Enter on canvas places free node")
    pg.locator('.chip[data-l="NP"]').focus(); pg.keyboard.press("Enter")   # 取消
    det = [k for k,v in s2["nodes"].items() if v["l"]=="Det"][0]
    pg.locator(f'[data-n="{det}"]').focus(); pg.keyboard.press("Enter")
    check(pg.evaluate("document.activeElement.dataset.n") == det, "focus stays on node after redraw")
    pg.locator(f'[data-n="{np_[0]}"]').focus(); pg.keyboard.press("Enter")
    check(st()["par"].get(det) == np_[0], "keyboard select piece then parent attaches")
    pg.locator(f'[data-n="{np_[0]}"]').focus(); pg.keyboard.press("Enter")
    pg.locator(f'[data-del="{np_[0]}"]').focus(); pg.keyboard.press("Enter")
    check(np_[0] not in st()["nodes"], "keyboard delete via x button")

    # 8. 題目文字：14e 的提示、名字和代名詞以 NP 直接掛為主
    pg.evaluate("cur=4; render()"); q = pg.locator(".q").inner_text()
    check("attaches to is written in its base form" in q, "14e prompt wording")
    check(pg.evaluate("ITEMS[3].key").startswith("[TP [NP Emily]") and pg.evaluate("ITEMS[4].key").startswith("[TP [NP I]"), "bare NP is primary key for names/pronouns")
    check("prototype" not in pg.title().lower() and "prototype" not in pg.locator(".eyebrow").inner_text().lower(), "no 'prototype' in student-visible header")
    check(not errs, f"no JS errors {errs}")
    print("FAILS", len(fails)); b.close()
