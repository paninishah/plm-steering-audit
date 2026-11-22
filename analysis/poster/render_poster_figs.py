"""
Export the paper's figures at poster scale -- WITHOUT touching their layout.

First attempt inflated type relative to the figure. That broke the dense
two-panel figures (titles collided, annotations landed on the data) and it also
missed tick labels, which take matplotlib's default size rather than an explicit
fontsize= the rewriter could see.

A figure's layout is a solved problem already: the paper's version is known
good. The only thing wrong for a poster is PHYSICAL size. So scale everything
uniformly -- which is exactly what rendering the unmodified figure at a higher
DPI does. Type keeps its proportions and grows with the figure.

    type on the board = original pt x (print width / figsize width)

so the print width is the only dial. Nothing in the repo's scripts is modified.

Usage:  python render_poster_figs.py <analysis_dir> <out_dir>
"""
import os
import re
import sys
import runpy

ANALYSIS = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])

# A1 portrait, 2 cm margins, 1.5 cm gutter
FULL_W = 21.8          # inches, full content width
COL_W = 10.6           # inches, one of two columns
WIDE_IF_OVER = 5.0     # a figure authored wider than this is a full-width one
PRINT_DPI = 300

SCRIPTS = [
    ("fig3_gate.py",      "paper Figure 2  (headline)"),
    ("fig2_steering.py",  "paper Figure A1"),
    ("fig4_predictor.py", "paper Figure A4"),
    ("fig_appendix.py",   "paper Figures A2, A3, A6, A7"),
]

SRC_DIR = os.path.join(ANALYSIS, "figure render scripts")
os.makedirs(OUT, exist_ok=True)

PRELUDE = '''
import matplotlib
matplotlib.use("Agg")
import os as _os
from matplotlib.figure import Figure as _Fig
_OUT, _FULL, _COL, _WIDE, _DPI = %r, %r, %r, %r, %r
_orig = getattr(_Fig, "_poster_orig_savefig", _Fig.savefig)
_Fig._poster_orig_savefig = _orig
_REPORT = []
def _savefig(self, fname, *a, **k):
    stem = _os.path.splitext(_os.path.basename(str(fname)))[0]
    w_in = self.get_size_inches()[0]
    target = _FULL if w_in >= _WIDE else _COL
    scale = target / w_in
    k.pop("dpi", None)
    # vector: scales losslessly, place it at the target width
    _orig(self, _os.path.join(_OUT, stem + ".pdf"), *a, **k)
    # raster: dpi chosen so the file is PRINT_DPI once placed at target width
    _orig(self, _os.path.join(_OUT, stem + ".png"), *a, dpi=_DPI * scale, **k)
    _REPORT.append((stem, w_in, target, scale))
_Fig.savefig = _savefig
'''


def min_font(src):
    vals = [float(v) for v in re.findall(r"fontsize=\s*([0-9.]+)", src)]
    return min(vals) if vals else None


os.chdir(ANALYSIS)          # the scripts read their CSVs from here
rows = []

for name, what in SCRIPTS:
    path = os.path.join(SRC_DIR, name)
    src = open(path, encoding="utf-8").read()
    mf = min_font(src)
    body = (PRELUDE % (OUT, FULL_W, COL_W, WIDE_IF_OVER, PRINT_DPI)) + "\n" + src
    tmp = os.path.join(OUT, "_" + name)
    open(tmp, "w", encoding="utf-8").write(body)
    print("%-20s %s" % (name, what))
    try:
        ns = runpy.run_path(tmp, run_name="__main__")
        for stem, w_in, target, scale in ns.get("_REPORT", []):
            rows.append((stem, w_in, target, scale, mf, mf * scale if mf else None))
    except Exception as exc:
        print("  FAILED: %s: %s" % (type(exc).__name__, exc))
    finally:
        os.remove(tmp)

print("\n%-24s %8s %9s %7s %9s %10s" %
      ("figure", "authored", "print in", "scale", "min pt", "-> on board"))
print("-" * 72)
for stem, w_in, target, scale, mf, got in rows:
    print("%-24s %7.1f\" %8.1f\" %6.2fx %8.1f %9.1f pt"
          % (stem, w_in, target, scale, mf, got))
