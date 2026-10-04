| VERDICT | **KILL / OFF** — all three reacting-V56 dev cells lose 19–32 wins; held-out and tape gates unopened |
|---|---|

# SHEEPFIRST1 — opening wool stock (2026-09-22)

## Implementation and parity

`plan.SHEEP_FIRST_ON=False` adds a d0–2 sheep stock target after the residual rewrite.
`SHEEP_FIRST_N` is the target; `SHEEP_FIRST_MODE="swap"` removes the newly requested count from the
cow target, while `"add"` preserves the decoded cow target. The sheep lane reuses the existing herd
stock, pasture, acquisition-gate and budget-priority machinery; purse, shed and placement laws still
bind. Invalid modes and negative targets fail early.

OFF whole-plan output is byte-identical to pre-change master `ed3cd697` on three pinned boards (d0,
d2 and d10). `tests/test_sheep_first.py` pins defaults, both modes, the d0–2 window, validation, an
executed three-sheep buy row, and whole-plan parity.

## Reacting-V56 dev100

LIVE250 games 0–99 used original seats, seeds and pinned towns, reacting V56, residual head 940,
and eight CPU workers. The baseline is `S/gatefidelity/v56_live250_n250.csv`; `b/c/net` counts
loss→win / win→loss / net flips. Wool is exact committed sale units per board; purse and quadrants
are the dawn-d10 state. Seat fields are `b/c/net`.

| N, mode | b/c/net | Δours | Δtheirs | wool d0–9 | wool d10–19 | purse d10 | quads d10 | seat 0 | seat 1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3, swap | 2/23/**−21** | +809.10 | +4,015.16 | 10.00 | 68.26 | 3,213.46 | 2.30 | 1/10/−9 | 1/13/−12 |
| 3, add | 0/19/**−19** | −370.13 | +2,309.17 | 10.00 | 68.55 | 4,052.76 | 2.12 | 0/9/−9 | 0/10/−10 |
| 4, swap | 1/33/**−32** | +107.45 | +6,353.81 | 20.16 | 78.95 | 2,876.07 | 2.40 | 0/14/−14 | 1/19/−18 |

## Mechanism and decision

The lever worked on wool: N=3 doubled the motivating 5-unit d0–9 line to 10, and N=4 reached 20.16.
Downstream placement/funding clips remained real: mean dawn-d2/d3 herds were G/C/S 1/2/2 for
3-swap, 0/3/2 for 3-add, and 0/1/4 for 4-swap. Raising N bought the full four sheep only by removing
more of the incumbent animal mix. It increased later wool too, but did not reproduce ENGINE's cash
conversion: every cell gifted V56 2.3k–6.4k coins and lost heavily in both seats.

No cell met `net >= +3` and `Δtheirs <= 0`. Per protocol the held-out 100 and LIVE302 tape dev gate
were not run. Default remains OFF.
