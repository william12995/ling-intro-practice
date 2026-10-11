"""在本機依序執行 notebook 的程式格（略過 !pip），輸出寫到 UTF-8 檔。用法：python run_notebook.py nb.ipynb out.txt"""
import io, json, sys, contextlib, types
drawn = []
d = types.ModuleType("IPython.display")
d.display = lambda x: drawn.append(x) or print(f"[drawn tree #{len(drawn)}]")
sys.modules["IPython"] = types.ModuleType("IPython")
sys.modules["IPython.display"] = d
nb = json.load(open(sys.argv[1], encoding="utf-8"))
buf = io.StringIO()
ns = {}
with contextlib.redirect_stdout(buf):
    for c in nb["cells"]:
        if c["cell_type"] != "code": continue
        src = "".join(l for l in c["source"] if not l.lstrip().startswith("!"))
        print("=" * 20); exec(src, ns)
    for extra in sys.argv[3:]:
        print("=" * 20, "EXTRA"); exec(open(extra, encoding="utf-8").read(), ns)
open(sys.argv[2], "w", encoding="utf-8").write(buf.getvalue())
