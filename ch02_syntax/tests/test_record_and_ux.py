# 成績紀錄、教學動畫、照提示做完練習句、推理欄、進度保存
import sys, pathlib, json, urllib.parse
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from build_site import wrap
src = (pathlib.Path(__file__).resolve().parents[1] / "tree_lab.src.html").read_text(encoding="utf-8")
FAKE = "https://script.google.com/macros/s/TESTDEPLOY/exec"
out = pathlib.Path("page_online.html"); out.write_text(wrap(src.replace("__ENDPOINT__", FAKE)), encoding="utf-8")
URL = out.resolve().as_uri()
STUDENT = "localStorage.setItem('ling_student', JSON.stringify({sid:'Z00000000',name:'Test'}));"
TUTSEEN = "localStorage.setItem('ling_syntax_tutorial_seen','true');"
fails = []
def check(c, w): print(("PASS " if c else "FAIL ") + w); (None if c else fails.append(w))

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")

    def ctx(init="", mobile=False, reduce=False):
        c = b.new_context(viewport={"width":390,"height":844} if mobile else {"width":1100,"height":900},
                          has_touch=mobile, is_mobile=mobile, reduced_motion="reduce" if reduce else "no-preference")
        if init: c.add_init_script(init)
        return c

    sent, mode = [], {"fail": False}
    def handler(route):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(route.request.url).query)
        cb = q.get("callback", ["callback"])[0]; data = json.loads(q["data"][0]) if "data" in q else {}
        if mode["fail"]: route.abort(); return
        if mode.get("unknown") and data.get("qid"):
            route.fulfill(status=200, content_type="application/javascript", body=f'{cb}({json.dumps({"ok":False,"error":"unknown quiz"})})'); return
        sent.append(data)
        route.fulfill(status=200, content_type="application/javascript", body=f'{cb}({json.dumps({"ok":True,"id":data.get("event_id")})})')

    # ---------- 1. 登入：第一次來要填學號；格式錯會擋 ----------
    c = ctx(); pg = c.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    c.route("**/script.google.com/**", handler)
    pg.goto(URL); pg.wait_for_timeout(300)
    check(pg.locator("#login").count() == 1, "login form shown on first visit")
    pg.fill("#sid", "12345"); pg.fill("#sname", "X"); pg.click("button[type=submit]")
    check("8 digits" in pg.locator("#lerr").inner_text(), "bad student ID rejected")
    pg.fill("#sid", "b13012345"); pg.fill("#sname", "Tester"); pg.click("button[type=submit]"); pg.wait_for_timeout(300)

    # ---------- 2. 教學動畫：第一次自動打開；Esc 關掉後記住；How to play 可以再打開 ----------
    check(pg.locator(".tut").count() == 1, "tutorial opens on first visit")
    check(pg.evaluate("document.getAnimations().length") > 5, "tutorial scene is animating")
    pg.click("#tut-next"); check("2 of 4" in pg.locator("#tut-n").inner_text().lower(), "tutorial Next goes to step 2")
    pg.keyboard.press("ArrowLeft"); check("1 of 4" in pg.locator("#tut-n").inner_text().lower(), "arrow key goes back")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    check(pg.locator(".tut").count() == 0 and pg.evaluate("localStorage.getItem('ling_syntax_tutorial_seen')") == "true", "Esc closes tutorial and remembers it")
    check(pg.evaluate("document.getAnimations().filter(a => !(a instanceof CSSAnimation)).length") == 0 and pg.evaluate("tutAnims.length") == 0, "tutorial animations stopped after closing")
    pg.reload(); pg.wait_for_timeout(300); check(pg.locator(".tut").count() == 0, "tutorial not shown again after reload")
    pg.click("#howto"); check(pg.locator(".tut").count() == 1, "How to play reopens tutorial")
    pg.click("#tut-skip"); check(pg.locator(".tut").count() == 0, "Skip closes tutorial")

    # ---------- 3. 照教學提示把練習句做完（只看發亮的東西，不看標準答案） ----------
    def box(sel):
        r = pg.locator(sel).first.bounding_box(); return r["x"]+r["width"]/2, r["y"]+r["height"]/2
    def mdrag(a, bxy):
        pg.mouse.move(*a); pg.mouse.down(); pg.mouse.move(a[0]+8, a[1]-8, steps=3)
        t = bxy() if callable(bxy) else bxy
        pg.mouse.move(*t, steps=8); pg.mouse.up(); pg.wait_for_timeout(60)
    def show_canvas(): pg.evaluate("document.querySelector('#cvwrap').scrollIntoView({block:'start'})"); pg.wait_for_timeout(30)
    steps = 0
    while steps < 40:
        steps += 1
        h = pg.evaluate("C && C.hint")
        if not h or h.get("submit"): break
        show_canvas()
        if "plus" in h:
            mdrag(box(f'.chip[data-l="{h["chip"]}"]'), lambda: box(f'[data-plus="{h["plus"]}"] .pv'))
        elif "zone" in h:
            mdrag(box(f'.chip[data-l="{h["chip"]}"]'), lambda: box("#cv .hintzone circle"))
        elif "piece" in h:
            pc = h["piece"]; sel = f'[data-n="{pc}"]' if pc[0] == "n" else f'[data-w="{pc}"]'
            mdrag(box(sel), box(f'[data-n="{h["onto"]}"]'))
        else:
            print("unexpected hint", h); break
    check(pg.evaluate("C && C.hint && C.hint.submit") is True, f"practice finished by following hints only ({steps-1} actions)")
    check(pg.locator("#submit").is_enabled() and "pulse" in pg.get_attribute("#submit", "class"), "Submit enabled and glowing at the end")
    check(pg.locator("#why").count() == 0, "practice sentence has no reasoning box")
    pg.click("#submit"); pg.wait_for_timeout(100)
    check(pg.locator("#result .verdict").inner_text() == "Correct", "practice judged Correct")
    check(len(sent) == 0, f"practice sentence is not recorded (sent={len(sent)})")

    # ---------- 4. 計分題：推理欄要寫滿 20 字才能送；送出的內容 ----------
    pg.evaluate("cur=4; render()")
    tree = pg.evaluate("ITEMS[4].tree")
    def build_state(t):   # 直接放進狀態（拖曳流程其他測試已經測過）
        nodes, par, n = {}, {}, [0]
        def go(x):
            if "w" in x: return "w%d" % x["i"]
            n[0] += 1; nid = "n%d" % n[0]; nodes[nid] = {"l": x["l"], "x": 0, "h": 1}
            for k in x["k"]: par[go(k)] = nid
            return nid
        go(t); return nodes, par
    nodes, par = build_state(tree)
    pg.evaluate(f"S[4].nodes={json.dumps(nodes)}; S[4].par={json.dumps(par)}; S[4].nid=99; refresh()")
    check(not pg.locator("#submit").is_enabled() and "reasoning" in pg.locator("#need").inner_text(), "Submit blocked until reasoning is written")
    pg.fill("#why", "short"); check(not pg.locator("#submit").is_enabled(), "too-short reasoning still blocked")
    WHY = "have is a V here and takes the VP finished my homework as its complement."
    pg.fill("#why", WHY); check(pg.locator("#submit").is_enabled(), "Submit enabled with 20+ characters")
    pg.click("#submit"); pg.wait_for_timeout(300)
    check(pg.locator("#why").is_disabled(), "reasoning locked after submit")
    rec = [d for d in sent if d.get("qid")]
    check(len(rec) == 1, f"one record sent ({len(rec)})")
    if rec:
        d = rec[0]
        check(d["quiz"] == "ch02_syntax" and d["qid"] == "S1-04" and d["level"] == 1 and d["part"] == "S", f"quiz/qid/level: {d['quiz']} {d['qid']} {d['level']}")
        check(d["correct"] == 1 and d["attempt"] == 1 and d["reasoning"] == WHY, "correct/attempt/reasoning")
        check(d["response"].startswith("[TP [NP I]") and "[T –pst]" in d["response"], "response is the labeled bracketing: " + d["response"][:60])
        check(d["student_id"] == "B13012345" and d["name"] == "Tester" and d["prompt"] == "I have finished my homework", "student and prompt")
    check("Answers recorded" in pg.locator("#sync").inner_text(), "sync status says recorded")

    # Try again 是第 2 次作答，推理清空
    pg.click("#again"); check(pg.input_value("#why") == "" and pg.evaluate("S[4].attempt") == 2, "Try again clears reasoning and bumps attempt")

    # ---------- 5. 斷線時留在佇列，恢復後補送 ----------
    mode["fail"] = True
    pg.fill("#why", WHY); pg.click("#submit"); pg.wait_for_timeout(400)
    q = pg.evaluate("JSON.parse(localStorage.getItem('ling_queue_ch02_syntax')||'[]')")
    check(len(q) == 1 and "Uploading" in pg.locator("#sync").inner_text(), "failed upload stays queued")
    mode["fail"] = False
    pg.evaluate("flush()"); pg.wait_for_timeout(400)
    q = pg.evaluate("JSON.parse(localStorage.getItem('ling_queue_ch02_syntax')||'[]')")
    check(len(q) == 0 and any(d.get("attempt") == 2 for d in sent), "queued answer resent after reconnect")

    # ---------- 5b. 歧義句：題目和送出的 prompt 都帶意思 ----------
    pg.evaluate("cur=9; render()")
    check("I used the telescope to see the man" in pg.locator(".q").first.inner_text(), "ambiguous item shows its meaning")
    nodes, par = build_state(pg.evaluate("ITEMS[9].tree"))
    pg.evaluate(f"S[9].nodes={json.dumps(nodes)}; S[9].par={json.dumps(par)}; S[9].nid=99; refresh()")
    pg.fill("#why", WHY); pg.click("#submit"); pg.wait_for_timeout(300)
    d = [d for d in sent if d.get("qid") == "S1-09"]
    check(len(d) == 1 and d[0]["correct"] == 1 and d[0]["prompt"] == "I saw the man with the telescope (I used the telescope to see the man)", "S1-09 prompt carries the meaning: " + (d[0]["prompt"] if d else "none"))

    # ---------- 6. 進度保存：重新整理後樹和作答狀態還在 ----------
    pg.evaluate("cur=1; render()")
    pg.evaluate("S[1].nodes={n1:{l:'Det',x:0,h:1}}; S[1].par={w0:'n1'}; S[1].nid=2; refresh()")
    pg.reload(); pg.wait_for_timeout(400)
    check(pg.evaluate("cur") == 1 and pg.evaluate("S[1].par.w0") == "n1" and pg.evaluate("S[4].done") is True, "progress survives reload")
    check(not errs, f"no JS errors {errs}")
    c.close()

    # ---------- 7. 不碰 ch01 的佇列 ----------
    sent.clear()
    ch01 = {"event_id":"Z00000000|ch01_morphology|S1-01|1|1-0","quiz":"ch01_morphology","qid":"S1-01"}
    c = ctx(STUDENT + TUTSEEN + f"if(!localStorage.getItem('ling_queue')) localStorage.setItem('ling_queue', JSON.stringify([{json.dumps(ch01)}]));")
    c.route("**/script.google.com/**", handler)
    pg = c.new_page(); pg.goto(URL); pg.wait_for_timeout(500)
    pg.evaluate("flush()"); pg.wait_for_timeout(300)
    check(pg.evaluate("JSON.parse(localStorage.getItem('ling_queue')).length") == 1, "ch01 queue left untouched")
    check(not any(d.get("quiz") == "ch01_morphology" for d in sent), "no ch01 record sent by this page")
    c.close()

    # ---------- 8. 減少動態：教學動畫停在固定畫面；提示不閃 ----------
    c = ctx(STUDENT, reduce=True); pg = c.new_page(); pg.goto(URL); pg.wait_for_timeout(400)
    running = pg.evaluate("document.getAnimations().filter(a => a.playState === 'running').length")
    check(pg.locator(".tut").count() == 1 and running == 0, f"reduced motion: tutorial shown without running animations ({running})")
    c.close()

    # ---------- 9. 手機上一打開，練習句的 + 不會被標籤盤蓋住 ----------
    c = ctx(STUDENT + TUTSEEN, mobile=True); pg = c.new_page(); pg.goto(URL); pg.wait_for_timeout(600)
    pr = pg.locator('[data-plus="w0"] .pv').bounding_box(); pal = pg.locator("#pal").bounding_box()
    check(pr["y"] + pr["height"] < pal["y"], f"hinted + visible above the tray on load ({pr['y']:.0f} < {pal['y']:.0f})")
    c.close()

    # ---------- 10. 第二輪 review 的修正 ----------
    def mk_state(t):
        nodes, par, n = {}, {}, [0]
        def go(x):
            if "w" in x: return "w%d" % x["i"]
            n[0] += 1; nid = "n%d" % n[0]; nodes[nid] = {"l": x["l"], "x": 0, "h": 1}
            for k in x["k"]: par[go(k)] = nid
            return nid
        go(t); return nodes, par
    # 10a. 後端沒設 QUIZZES：留在佇列、不進退件區、提醒學生；設好之後補送
    sent.clear(); mode["unknown"] = True
    c = ctx(STUDENT + TUTSEEN); c.route("**/script.google.com/**", handler); pg = c.new_page(); pg.goto(URL); pg.wait_for_timeout(400)
    pg.evaluate("cur=1; render()"); nodes, par = mk_state(pg.evaluate("ITEMS[1].tree"))
    pg.evaluate(f"S[1].nodes={json.dumps(nodes)}; S[1].par={json.dumps(par)}; S[1].nid=99; refresh()")
    pg.fill("#why", "read takes the book as its complement inside V'."); pg.click("#submit"); pg.wait_for_timeout(400)
    q = pg.evaluate("JSON.parse(localStorage.getItem('ling_queue_ch02_syntax')||'[]').length"); dl = pg.evaluate("JSON.parse(localStorage.getItem('ling_deadletter_ch02_syntax')||'[]').length")
    check(q == 1 and dl == 0 and "not ready" in pg.locator("#sync").inner_text(), f"unknown quiz keeps answer queued (queue={q}, dead={dl})")
    mode["unknown"] = False; pg.evaluate("flush()"); pg.wait_for_timeout(400)
    check(pg.evaluate("JSON.parse(localStorage.getItem('ling_queue_ch02_syntax')||'[]').length") == 0 and "recorded" in pg.locator("#sync").inner_text(), "sent once the sheet is fixed")
    # 10b. 選著標籤時點線：照樣剪線
    pg.evaluate("cur=2; render()"); pg.evaluate("S[2].nodes={n1:{l:'Det',x:0,h:1}}; S[2].par={w0:'n1'}; S[2].nid=2; refresh()")
    pg.evaluate("document.querySelector('#cvwrap').scrollIntoView({block:'center'})")
    pg.click('.chip[data-l="NP"]')
    mid = pg.evaluate("""(()=>{const l=document.querySelector('[data-e="w0"] .ln'), r=document.querySelector('#cv').getBoundingClientRect();
      return [r.left+(+l.getAttribute('x1')+ +l.getAttribute('x2'))/2, r.top+(+l.getAttribute('y1')+ +l.getAttribute('y2'))/2]})()""")
    pg.mouse.click(*mid); pg.wait_for_timeout(50)
    check("w0" not in pg.evaluate("S[2].par"), "tap a line cuts it even with a label selected")
    # 10c. 換學生時不帶著選好的標籤
    pg.click('.chip[data-l="NP"]'); pg.click("#logout"); check(pg.evaluate("armed") is None, "Switch student clears selected label")
    c.close()
    # 10d. 手機：捲到底按 Next，新題目的題目文字要看得到
    c = ctx(STUDENT + TUTSEEN, mobile=True); pg = c.new_page(); pg.goto(URL); pg.wait_for_timeout(500)
    ok = True
    for k in range(4):
        pg.evaluate("scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(80)
        pg.locator("#next").tap(); pg.wait_for_timeout(250)
        top = pg.evaluate("document.querySelector('.q').getBoundingClientRect().top")
        if top < 0: ok = False; print("  q top", top, "after Next to item", k+1)
    check(ok, "question visible after Next on phone")
    q0 = pg.evaluate("cur=0; render(); 0"); pg.evaluate("scrollTo(0,0)"); pg.reload(); pg.wait_for_timeout(500)
    check(pg.evaluate("document.querySelector('.q').getBoundingClientRect().top") >= 0, "question visible on first load")
    c.close()
    # 10e. 教學：焦點在 body 時 Esc 照樣關、Tab 不會跑到後面；Esc 不會清掉頁面上選好的標籤
    c = ctx(STUDENT + TUTSEEN); pg = c.new_page(); pg.goto(URL); pg.wait_for_timeout(400)
    pg.click('.chip[data-l="NP"]'); pg.click("#howto"); pg.wait_for_timeout(100)
    pg.evaluate("document.activeElement.blur()"); pg.keyboard.press("Tab")
    check(bool(pg.evaluate("!!document.activeElement.closest('.tut')")), "Tab from body stays inside tutorial")
    pg.evaluate("document.activeElement.blur()"); pg.keyboard.press("Escape"); pg.wait_for_timeout(50)
    check(pg.locator(".tut").count() == 0 and pg.evaluate("armed") == "NP", "Esc closes tutorial without clearing the selected label")
    # 10f. 存壞的進度不會讓頁面掛掉
    pg.evaluate("localStorage.setItem('ling_prog_v1_ch02_syntax_Z00000000', JSON.stringify({v:1,cur:1,items:[null,{nodes:{},par:{},done:true,ok:true}]}))")
    perr = []; pg.on("pageerror", lambda e: perr.append(str(e)))
    pg.reload(); pg.wait_for_timeout(400)
    check(not perr and pg.evaluate("S[1].done") is False and pg.locator("#cv").count() == 1, f"corrupted progress handled ({perr})")
    c.close()
    print("FAILS", len(fails)); b.close()
