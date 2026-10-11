"""產生 CFG 習題的 Colab notebook（學生版＋答案版）。

格式照老師 10-11 寄的 Colab（nltk.CFG.fromstring + ChartParser + svgling），沒有 T 節點：S -> NP VP。
學生版 cfg_exercise.ipynb 推上 GitHub，學生用 Open in Colab 連結開；
答案版寫到 _output/answer_keys/（gitignore，不推上 public repo）。答案是 AI 寫的，要老師核。

學生看得到的文字（markdown、程式註解、提示訊息）一律英文。

用法：python ch02-2_cfg/make_notebooks.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_STUDENT = ROOT / "ch02-2_cfg" / "cfg_exercise.ipynb"
OUT_KEY = ROOT / "_output" / "answer_keys" / "cfg_exercise_KEY.ipynb"

# 共用的檢查程式。學生在 Colab 看到的是表單收合的 Setup 格。
HELPER = r'''# @title Setup: run this cell first (click ▶)
!pip install -q nltk svgling

import itertools
import nltk
import svgling
from nltk.grammar import Nonterminal
from IPython.display import display

MAX_TREES = 6


def _read_grammar(text):
    try:
        return nltk.CFG.fromstring(text)
    except ValueError as e:
        print("❌ Your grammar could not be read. Python says:")
        print("   ", e)
        print("Check: one rule per line, an arrow ->, alternatives separated by |, "
              "and every word in quotes, e.g.  N -> 'dog' | 'cat'")
        return None


def _words(sentence):
    return sentence.strip().rstrip(".!?").split()


def _warnings(g):
    if str(g.start()) != "S":
        print(f"⚠️  Your first rule starts with {g.start()}, so NLTK treats {g.start()} as the "
              "top of the tree. Put the S rule first.")
    lhs = {p.lhs() for p in g.productions()}
    undefined = sorted({str(s) for p in g.productions() for s in p.rhs()
                        if isinstance(s, Nonterminal) and s not in lhs})
    if undefined:
        print("⚠️  These symbols appear on the right of an arrow but never on the left: "
              + ", ".join(undefined))
        print("   If they are words, put them in quotes ('book'). "
              "If they are categories, add a rule for them.")
    loops = sorted({str(p.lhs()) for p in g.productions() if p.rhs() == (p.lhs(),)})
    if loops:
        print("⚠️  A rule like " + ", ".join(f"{x} -> {x}" for x in loops)
              + " lets the computer stack the same node forever. Remove it.")


def _phrases_built(g, words):
    """Phrases (2+ words) the grammar can build, to help find where a parse breaks."""
    chart = nltk.ChartParser(g).chart_parse(words)
    found = set()
    for e in chart.edges():
        if e.is_complete() and isinstance(e.lhs(), Nonterminal) and e.length() >= 2:
            found.add((e.start(), e.end(), str(e.lhs())))
    return sorted(found, key=lambda x: (x[0], -x[1]))


def show(grammar, sentence, max_trees=MAX_TREES):
    """Parse `sentence` with your grammar and draw every tree it gives."""
    g = _read_grammar(grammar)
    if g is None:
        return
    words = _words(sentence)
    print("Sentence:", " ".join(words))
    _warnings(g)
    lexicon = {s for p in g.productions() for s in p.rhs() if isinstance(s, str)}
    missing = [w for w in words if w not in lexicon]
    if missing:
        print("❌ These words are not in your lexicon:", ", ".join(missing))
        print("   Capital letters count: 'John' and 'john' are different words.")
        return
    trees = list(itertools.islice(nltk.ChartParser(g).parse(words), max_trees + 1))
    if not trees:
        print("❌ Your grammar does not generate this sentence.")
        built = _phrases_built(g, words)
        if built:
            print("   Phrases your grammar can build:")
            for i, j, cat in built:
                print(f"     {cat}: {' '.join(words[i:j])}")
            print("   Look for the part of the sentence that no rule puts together.")
        return
    if len(trees) > max_trees:
        print(f"Your grammar gives more than {max_trees} trees. Showing the first {max_trees}.")
        trees = trees[:max_trees]
    elif len(trees) == 1:
        print("✅ Your grammar gives 1 tree.")
    else:
        print(f"Your grammar gives {len(trees)} trees, so it is ambiguous for this sentence.")
        print("Use constituency tests to decide which tree matches the meaning.")
    for n, t in enumerate(trees, 1):
        print(f"\nTree {n}:  {t._pformat_flat('', '()', False)}")
        display(svgling.draw_tree(t))


def check(grammar, good, bad=()):
    """Count the trees for each sentence. Good sentences need 1+, starred ones need 0."""
    g = _read_grammar(grammar)
    if g is None:
        return
    _warnings(g)
    lexicon = {s for p in g.productions() for s in p.rhs() if isinstance(s, str)}
    parser = nltk.ChartParser(g)
    for sentence, should_parse in [(s, True) for s in good] + [(s, False) for s in bad]:
        words = _words(sentence)
        missing = [w for w in words if w not in lexicon]
        n = 0 if missing else len(list(itertools.islice(parser.parse(words), MAX_TREES + 1)))
        # 星號句缺詞時不算過關，不然空白文法也會全拿 ✅
        ok = not missing and (n > 0) == should_parse
        label = ("" if should_parse else "*") + " ".join(words)
        note = f"missing words: {', '.join(missing)}" if missing else f"{n} tree(s)"
        print(("✅ " if ok else "❌ ") + f"{label:<45} {note}")


print("Ready. Run the cells below in order.")
'''

INTRO = """# Syntax: write a phrase structure grammar

In this notebook you write **phrase structure rules** and a **lexicon** in NLTK's format.
The computer then draws every tree your grammar gives for a sentence.

The program only shows you the tree(s). Deciding whether a tree is *right* is your job:
for each sentence, use **constituency tests** to argue for your structure.

**Before you start:** click **File → Save a copy in Drive**, and work in your copy.
Then run the **Setup** cell below (click ▶ on its left)."""

FORMAT = """## How the grammar format works

Here is a grammar that generates *Mary saw Bob*. Run the cell to see its tree.

* One rule per line: `S -> NP VP` means "an S is an NP followed by a VP".
* `|` separates alternatives: `NP -> Det N | Det N PP`.
* Words go in quotes and must match the sentence exactly (`'John'` is not `'john'`).
* The **first** rule must be the `S` rule: it is the top of the tree.
* Lines that start with `#` are comments; the computer ignores them.
* Leave out the final period when you type the sentence."""

EXAMPLE = '''grammar0 = """
# Phrase structure rules
S -> NP VP
VP -> V NP | V NP PP
PP -> P NP
NP -> 'John' | 'Mary' | 'Bob' | Det N | Det N PP

# Lexicon
V -> 'saw' | 'ate' | 'walked'
Det -> 'a' | 'an' | 'the' | 'my'
N -> 'man' | 'dog' | 'cat' | 'telescope' | 'park'
P -> 'in' | 'on' | 'by' | 'with'
"""

show(grammar0, "Mary saw Bob")'''

TESTS = """## Constituency tests you can use

| Test | What you do | Example |
|---|---|---|
| Substitution (pro-form) | Replace the string with *it, she, they, there, then, do so* | *the girl with the hat* → *she* |
| Movement | Move the string to the front of the sentence | *On the desk, John put the book.* |
| Question / fragment answer | Ask a question; the string can be the short answer | *Where did John put the book?* — *On the desk.* |
| Coordination | Join the string with another of the same kind using *and* | *on the desk and under the chair* |

A string that passes these tests is a constituent, so it should be **one node** in your tree.
A string that fails them should *not* be one node."""

# (標題, 任務說明, 句子, 學生起始文法, 答案文法, 論證提示, 答案論證)
TASKS = [
    (
        "Task 1. *John put the book on the desk.*",
        "Write the rules and the lexicon so that your grammar generates this sentence. "
        "*put* needs both an object and a location: *\\*John put the book* is not a sentence.",
        "John put the book on the desk",
        '''# Phrase structure rules
S -> NP VP

# Lexicon
''',
        '''S -> NP VP
VP -> V NP PP
PP -> P NP
NP -> 'John' | Det N
V -> 'put'
Det -> 'the'
N -> 'book' | 'desk'
P -> 'on'
''',
        "Is *the book* one constituent, or is *the book on the desk* one constituent? "
        "Give at least two tests. If your grammar gives two trees, say which one is right.",
        "VP -> V NP PP 是對的：the book 和 on the desk 是 V 的兩個姊妹節點。\n"
        "代換：John put it on the desk（it = the book）可以；*John put it（it = the book on the desk）不行，"
        "所以 the book on the desk 不是一個 NP。\n"
        "問句：Where did John put the book? — On the desk. PP 可以單獨回答。\n"
        "移位：On the desk, John put the book.\n"
        "如果學生也寫了 NP -> Det N PP，會得到兩棵樹；NP 內含 PP 那棵缺了 put 必要的處所補語，要排除。",
    ),
    (
        "Task 2. *The girl with the hat smiled.*",
        "Write a grammar for this sentence. *smiled* has no object.",
        "The girl with the hat smiled",
        '''# Phrase structure rules
S -> NP VP

# Lexicon
''',
        '''S -> NP VP
NP -> Det N | Det N PP
PP -> P NP
VP -> V
Det -> 'The' | 'the'
N -> 'girl' | 'hat'
P -> 'with'
V -> 'smiled'
''',
        "Show with a test that *the girl with the hat* is one NP.",
        "代換：She smiled（she = the girl with the hat）。\n"
        "問句：Who smiled? — The girl with the hat.\n"
        "並列：The girl with the hat and the boy smiled.\n"
        "注意大寫：句首是 'The'，詞庫要有 'The'（或把 'The' 和 'the' 都列）。",
    ),
    (
        "Task 3. *Bob ate the cake with a fork.*",
        "Write a grammar for this sentence. Think about what *with a fork* goes with: the cake, or the eating?",
        "Bob ate the cake with a fork",
        '''# Phrase structure rules
S -> NP VP

# Lexicon
''',
        '''S -> NP VP
VP -> V NP | VP PP
PP -> P NP
NP -> 'Bob' | Det N
V -> 'ate'
Det -> 'the' | 'a'
N -> 'cake' | 'fork'
P -> 'with'
''',
        "Use a test to show whether *the cake with a fork* is one constituent or not.",
        "with a fork 修飾吃的動作，PP 掛在 VP 上（VP -> VP PP，或寫成 VP -> V NP PP 也接受，看老師的 X-bar 立場）。\n"
        "代換：Bob ate it with a fork（it = the cake）可以；*Bob ate it 不能表示「吃了附叉子的蛋糕」。\n"
        "do so：Bob ate the cake with a fork, and Mary did so with a spoon. did so 取代 ate the cake，"
        "所以 ate the cake 是一個 VP，with a fork 在它外面。\n"
        "問句：What did Bob eat? — The cake.（不是 The cake with a fork）",
    ),
    (
        "Task 4. *Mary saw the man with the telescope.*",
        "This sentence has two meanings. Write **one** grammar that gives **two** trees, one for each meaning.",
        "Mary saw the man with the telescope",
        '''# Phrase structure rules
S -> NP VP

# Lexicon
''',
        '''S -> NP VP
VP -> V NP | VP PP
NP -> 'Mary' | Det N | NP PP
PP -> P NP
V -> 'saw'
Det -> 'the'
N -> 'man' | 'telescope'
P -> 'with'
''',
        "For each tree, write the meaning it gives, and one test that brings out that meaning.",
        "樹 A（PP 在 VP）：Mary 用望遠鏡看。Mary saw him with the telescope（him = the man）。\n"
        "樹 B（PP 在 NP）：看到拿著望遠鏡的那個人。Mary saw him（him = the man with the telescope）；"
        "Who did Mary see? — The man with the telescope.",
    ),
]

FINAL_TITLE = "Task 5. One grammar for everything"
FINAL_TEXT = """Combine your grammars into **one** grammar that generates all four sentences
and does **not** generate the starred ones. `check` prints ✅ when a good sentence gets
at least one tree and a starred sentence gets none.

Hint: *put*, *ate*, *saw* and *smiled* do not take the same things after them.
You may need more than one verb category (for example `Vt`, `Vi`, `Vput`)."""
FINAL_GOOD = ["John put the book on the desk", "The girl with the hat smiled",
              "Bob ate the cake with a fork", "Mary saw the man with the telescope"]
FINAL_BAD = ["John put the book", "The girl smiled the cake", "Mary saw"]
FINAL_KEY = '''S -> NP VP
VP -> Vput NP PP | Vt NP | Vi | VP PP
NP -> 'John' | 'Bob' | 'Mary' | Det N | NP PP
PP -> P NP
Vput -> 'put'
Vt -> 'ate' | 'saw'
Vi -> 'smiled'
Det -> 'The' | 'the' | 'a'
N -> 'book' | 'desk' | 'girl' | 'hat' | 'cake' | 'fork' | 'man' | 'telescope'
P -> 'on' | 'with'
'''

ARGUE_TEMPLATE = """**Your argument** (double-click to edit)

My tree: *(which tree number, or describe it)*

Test 1:

Test 2:
"""


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text, form=False):
    meta = {"cellView": "form"} if form else {}
    return {"cell_type": "code", "execution_count": None, "metadata": meta,
            "outputs": [], "source": text.splitlines(keepends=True)}


def grammar_cell(var, body, call):
    return code(f'{var} = """\n{body}"""\n\n{call}')


def build(key: bool):
    cells = [md(INTRO), code(HELPER, form=True), md(FORMAT), code(EXAMPLE), md(TESTS)]
    for n, (title, text, sent, start, ans, prompt, ans_arg) in enumerate(TASKS, 1):
        cells.append(md(f"## {title}\n\n{text}"))
        cells.append(grammar_cell(f"grammar{n}", ans if key else start, f'show(grammar{n}, "{sent}")'))
        cells.append(md(f"**Argue for your tree.** {prompt}"))
        cells.append(md(f"**參考答案（AI 寫的，請老師核）**\n\n{ans_arg}" if key else ARGUE_TEMPLATE))
    cells.append(md(f"## {FINAL_TITLE}\n\n{FINAL_TEXT}"))
    call = f"check(grammar5,\n      good={FINAL_GOOD!r},\n      bad={FINAL_BAD!r})"
    body = FINAL_KEY if key else "# Phrase structure rules\nS -> NP VP\n\n# Lexicon\n"
    cells.append(grammar_cell("grammar5", body, call))
    return {
        "nbformat": 4, "nbformat_minor": 0,
        "metadata": {"colab": {"provenance": [], "toc_visible": True},
                     "kernelspec": {"name": "python3", "display_name": "Python 3"},
                     "language_info": {"name": "python"}},
        "cells": cells,
    }


if __name__ == "__main__":
    OUT_KEY.parent.mkdir(parents=True, exist_ok=True)
    for path, key in [(OUT_STUDENT, False), (OUT_KEY, True)]:
        path.write_text(json.dumps(build(key), ensure_ascii=False, indent=1), encoding="utf-8")
        print("寫入", path.relative_to(ROOT))
