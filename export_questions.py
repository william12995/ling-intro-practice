"""把四份練習的題目匯出成 Markdown，附每題有幾位學生寫過。

2026-10-27 老師要出期中考，要知道學生練過哪些題目。
題目直接從 *.src.html 的 ITEMS / SECTIONS 陣列抽（用 node 執行那段 JS），作答人數從
_output/private/ 底下最新的 Sheet 匯出檔算，排除助教自己和測試學號。

用法：python export_questions.py
輸出：_output/題目匯出/（已列入 .gitignore，期中考相關不推上 public repo）
"""
import collections
import datetime
import glob
import html
import json
import os
import re
import subprocess

import openpyxl

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_output", "題目匯出")
EXCLUDE = {"R13142001", "Z00000000", "B20260101"}   # 使用者自己、測試學號

# (頁面原始檔, 陣列名稱, Sheet 匯出檔前綴, 輸出檔名, 標題, 網址)
PAGES = [
    ("ch01_morphology/morphology_lab.src.html", "SECTIONS", "ch01_morphology", "1_構詞.md",
     "構詞 Morphology", "https://william12995.github.io/ling-intro-practice/ch01_morphology/"),
    ("ch01-2_morph_tree/morph_tree.src.html", "ITEMS", "ch01-2_morph_tree", "2_構詞樹選樹.md",
     "構詞樹選樹 Morphological trees", "https://william12995.github.io/ling-intro-practice/ch01-2_morph_tree/"),
    ("ch02_syntax/tree_lab.src.html", "ITEMS", "ch02_syntax", "3_句法選樹.md",
     "句法選樹 Syntax trees", "https://william12995.github.io/ling-intro-practice/ch02_syntax/"),
    ("ch02-2_cfg/cfg_lab.src.html", "ITEMS", "ch02-2_cfg", "4_詞組結構律.md",
     "詞組結構律 Phrase structure rules", "https://william12995.github.io/ling-intro-practice/ch02-2_cfg/"),
]


def load_array(src, name):
    text = open(os.path.join(ROOT, src), encoding="utf-8").read()
    start = text.index(f"const {name} = [")
    end = text.index("\n];", start) + 3
    consts = {}
    for k in ("TR", "KR"):   # 構詞頁的資料表用 "__TR__" 佔位
        m = re.search(rf'^const {k} = (".*?");$', text, re.M)
        if m:
            consts[k] = json.loads(m.group(1))
    js = text[start + len(f"const {name} = "):end - 1]
    out = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify({js}))"],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    return json.loads(out), consts


def plain(s):
    s = (s or "").replace("*", r"\*")   # 星號句的 * 要跳脫，不然會跟斜體混在一起
    s = re.sub(r"</?(em|i)>", "*", s)
    s = re.sub(r"</?b>", "**", s)
    s = re.sub(r"</?code>", "`", s)
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def stats(prefix):
    """每個 qid：作答學生數、第一次就對的人數（只算有判分的）。"""
    files = sorted(glob.glob(os.path.join(ROOT, "_output", "private", f"{prefix}_2026-*.xlsx")))
    if not files:
        return {}, None
    f = files[-1]
    ws = openpyxl.load_workbook(f, read_only=True)["answers"]
    rows = ws.iter_rows(values_only=True)
    head = list(next(rows))
    ix = {k: head.index(k) for k in ("student_id", "qid", "correct", "attempt")}
    who = collections.defaultdict(set)
    first_ok = collections.defaultdict(set)
    graded = collections.defaultdict(set)
    for r in rows:
        sid = str(r[ix["student_id"]] or "").strip().upper()
        qid = r[ix["qid"]]
        if not sid or sid in EXCLUDE or not qid:
            continue
        who[qid].add(sid)
        c = r[ix["correct"]]
        # Sheet 匯出的 correct、attempt 是浮點數（1.0）；不計分的題目 correct 是空白
        if float(r[ix["attempt"]] or 0) == 1 and c not in (None, ""):
            graded[qid].add(sid)
            if str(c).upper() in ("TRUE", "1", "1.0"):
                first_ok[qid].add(sid)
    res = {q: (len(who[q]), len(first_ok[q]), len(graded[q])) for q in who}
    date = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(f)).group(1)
    return res, date


def stat_line(st, qid, graded=True):
    n, ok, g = st.get(qid, (0, 0, 0))
    g = g if graded else 0
    if not n:
        return "作答人數：0"
    s = f"作答人數：{n}"
    if g:
        s += f"，第一次就答對 {ok}/{g}（{ok / g:.0%}）"
    return s


def letters(i):
    return "ABCDEFG"[i]


def morphology(data, consts, st):
    out = []
    for si, sec in enumerate(data, 1):
        out.append(f"## {sec['name']}（開源課本 {sec['ex']}）\n")
        out.append(f"> {plain(sec.get('note'))}\n")
        shown = set()
        for ii, it in enumerate(sec["items"], 1):
            qid = f"S{si}-{ii:02d}"
            d = it.get("d", "")
            for k, v in consts.items():
                d = d.replace(f"__{k}__", v)
            if d and d not in shown:   # 同一節共用的資料表只印一次
                out.append("```\n" + d + "\n```\n")
                shown.add(d)
            t = it["type"]
            if t == "cut":
                q = f"Split *{it['w']}* into its smallest morphemes."
            else:
                q = plain(it["q"])
            tag = "（不計分）" if it.get("grade") is False else ""
            out.append(f"**{qid}**{tag}　{q}\n")
            if it.get("note"):
                out.append(f"提示：{plain(it['note'])}\n")
            if t == "mc":
                for k, o in enumerate(it["o"]):
                    mark = " ✓" if it.get("a") == k and it.get("grade") is not False else ""
                    out.append(f"- {letters(k)}. {plain(o)}{mark}")
                out.append("")
            elif t == "multi":
                for o in it["o"]:
                    mark = {"y": " ✓", "n": "", "e": " （選不選都算對）"}[o["s"]]
                    out.append(f"- {plain(o['t'])}{mark}")
                out.append("")
            elif t == "cut":
                alts = [it["m"]] + it.get("alt", [])
                out.append("答案：" + "；".join(" + ".join(m) for m in alts) + "\n")
            elif t == "fill":
                out.append("答案：eldʒıklerimizde\n")
            out.append(f"解說：{plain(it.get('e'))}\n")
            out.append(f"*{stat_line(st, qid)}*\n")
    return out


def tree_page(data, st):
    out = []
    for i, it in enumerate(data):
        qid = "練習（不計分）" if it.get("tut") else f"S1-{i:02d}"
        say = it["say"] + (f"（意思：{it['mean']}）" if it.get("mean") else "")
        out.append(f"**{qid}**　*{say}*　〔{it['ex']}〕\n")
        ok = it["ans"] if isinstance(it["ans"], list) else [it["ans"]]
        for k, t in enumerate(it["opts"]):
            out.append(f"- 樹 {letters(k)}{' ✓' if k in ok else ''}：`{t}`")
        out.append("")
        out.append(f"解說：{plain(it.get('e'))}\n")
        if not it.get("tut"):
            out.append(f"*{stat_line(st, qid)}*\n")
    return out


def cfg_page(data, st):
    out = []
    for i, it in enumerate(data):
        if it.get("tut"):
            qid = "練習（不計分）"
        elif it.get("final"):   # 合併文法那題只交文法，不寫論證
            qid = f"S2-{i:02d}（文法）"
        else:
            qid = f"S2-{i:02d}（文法）／S1-{i:02d}（論證）"
        out.append(f"### {it['ex']}：{it['say']}\n")
        out.append(f"**{qid}**\n")
        out.append(f"題目：{plain(it.get('task'))}\n")
        if it.get("good"):
            out.append("要產生：" + "；".join(f"*{s}*" for s in it["good"]))
            out.append("不能產生：" + "；".join(f"\\**{s}*" for s in it["bad"]) + "\n")
        g = it.get("sample") or it.get("start")
        if g:
            out.append(("給學生的起始文法" if it.get("tut") else "參考文法（AI 寫的）") + "：\n")
            out.append("```\n" + g.strip() + "\n```\n")
        if it.get("e"):
            out.append(f"解說：{plain(it['e'])}\n")
        if not it.get("tut"):
            n2 = st.get(f"S2-{i:02d}", (0,))[0]
            n1 = st.get(f"S1-{i:02d}", (0,))[0]
            out.append(f"*交了文法 {n2} 人*\n" if it.get("final") else f"*交了文法 {n2} 人，交了論證 {n1} 人*\n")
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    index = []
    for src, name, prefix, fn, title, url in PAGES:
        data, consts = load_array(src, name)
        st, date = stats(prefix)
        if name == "SECTIONS":
            body = morphology(data, consts, st)
            nq = sum(len(s["items"]) for s in data)
        elif "cfg" in src:
            body = cfg_page(data, st)
            nq = len(data) - 1
        else:
            body = tree_page(data, st)
            nq = len(data) - 1
        head = [f"# {title}\n",
                f"線上練習頁：{url}　原始檔：`{src}`\n",
                f"共 {nq} 題（不含練習題）。作答人數取自 {date} 匯出的成績 Sheet，排除助教和測試學號。"
                + ("這一頁整頁不計分，參考文法和解說是 AI 寫的，老師還沒核過。\n" if "cfg" in src else
                   "✓ 是頁面上的標準答案；標準答案、誘答選項和解說是 AI 寫的，老師還沒全部核過。\n")]
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write("\n".join(head + body))
        n = [v[0] for k, v in st.items() if k != "practice"]
        index.append(f"| [{title}]({fn}) | {nq} | {min(n)}–{max(n)} 人 |")
    open(os.path.join(OUT, "0_總覽.md"), "w", encoding="utf-8").write("\n".join([
        "# 四份線上練習的題目（期中考出題參考）\n",
        f"{datetime.date.today()} 從頁面原始檔匯出。四份的每一題都已經上線，學生都看得到；"
        f"作答人數取自 {date} 匯出的成績 Sheet（全班約 42 人，排除助教和測試學號）。\n",
        "| 練習 | 題數 | 每題作答人數 |", "|---|---|---|", *index, "",
        "構詞那份幾乎全班都寫完了，其他三份只有一半左右的學生寫過。"
        "題目出處（開源課本或老師簡報）見 `../練習來源與建議題目_2026-10-16.md`。\n",
        "重新產生：`python export_questions.py`。\n"]))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
