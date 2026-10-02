#!/usr/bin/env python3
"""Read a `report_pool511.py` / `report.py` table off stdin (or a file) and
print the SHIP / PROMOTE verdict clause by clause.

    python S/pipeline/verdict.py <report.txt> [--bar ship|promote]

The table's rows look like

    POOLED511   511    -     +200   78 +2.55   +153 +1.88     -46  -0.67  257/232  76.9->77.1 (393->394) +15/-14 1.000

so the leading fields are fixed (leg, boards, rows, dmargin, se, t, dours, t,
dtheirs, t) and the last two are always `flips` (+a/-b) and `signp`.

SHIP bar [JOINTFREE / REALESJUDGE]:  dtheirs <= 0  AND  t >= 3  AND  net flips > 0.
PROMOTE bar (the loop's softer internal bar, a centre is not an upload):
                                     dtheirs <= 0  AND  t >= 2  AND  net flips >= 0.

Exit 0 when the bar passes, 1 when it does not, 2 when the table is unreadable
(an unreadable table is NEVER a pass).
"""
from __future__ import annotations

import re
import sys

BARS = {"ship": (0.0, 3.0, 1), "promote": (0.0, 2.0, 0)}


def rows(text):
    out = {}
    for ln in text.splitlines():
        f = ln.split()
        if len(f) < 12 or not re.match(r"^[A-Z][A-Z0-9]+$", f[0]):
            continue
        try:
            out[f[0]] = dict(
                boards=int(f[1]), dmargin=float(f[3]), se=float(f[4]), t=float(f[5]),
                dours=float(f[6]), dtheirs=float(f[8]),
                flips=f[-2], signp=float(f[-1]))
        except (ValueError, IndexError):
            continue
    return out


def main(path, bar="ship"):
    text = open(path).read() if path != "-" else sys.stdin.read()
    tab = rows(text)
    if not tab:
        print("VERDICT: UNREADABLE -- no leg rows found; treat as REJECT")
        return 2
    key = next((k for k in ("POOLED511", "POOLED567", "POOLED278") if k in tab), None)
    if key is None:
        key = max(tab, key=lambda k: tab[k]["boards"])
    r = tab[key]
    m = re.match(r"\+(\d+)/-(\d+)", r["flips"])
    net = int(m.group(1)) - int(m.group(2)) if m else 0
    gift_max, t_min, flip_min = BARS[bar]

    print(f"\n--- {bar.upper()} BAR on {key} ({r['boards']} boards) ---")
    for name, got, ok, want in (
            ("gift-free  dtheirs", f"{r['dtheirs']:+.0f}", r["dtheirs"] <= gift_max, f"<= {gift_max:+.0f}"),
            ("pooled t          ", f"{r['t']:+.2f}", r["t"] >= t_min, f">= {t_min:.1f}"),
            ("net board flips   ", f"{net:+d} ({r['flips']}, signp {r['signp']:.3f})",
             net >= flip_min, f">= {flip_min:+d}" if flip_min else ">= 0"),
    ):
        print(f"  {'PASS' if ok else 'FAIL'}  {name}  {got:<34s} want {want}")
    ok = (r["dtheirs"] <= gift_max) and (r["t"] >= t_min) and (net >= flip_min)
    print(f"  dmargin {r['dmargin']:+.0f} se {r['se']:.0f}   dours {r['dours']:+.0f}")
    print(f"VERDICT: {'PASS -- ' + ('SHIP-READY' if bar == 'ship' else 'PROMOTE') if ok else 'REJECT'}")
    if r["t"] >= t_min and net < flip_min:
        print("  NOTE: margin without flips buys no rating -- the ladder is "
              "Bradley-Terry over board WINS [jointfree2].")
    return 0 if ok else 1


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    b = "ship"
    if "--bar" in sys.argv:
        b = sys.argv[sys.argv.index("--bar") + 1]
    raise SystemExit(main(a[0] if a else "-", b))
