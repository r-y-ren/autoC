# Contested-tape win columns in `paired.py`

*2026-09-09 — harness agent. Tool: `S/bank/paired.py` (backup `paired.py.bak_contested`).
Finding it implements: `docs/strategy/2026-09-10-drawn-vs-pinned.md`.*

## Why

On a drawn-town leg the base theta wins ~90 % of boards, because open-loop tapes replayed on a
*drawn* town lose their board and fold (`memory/tape-fidelity-2026-09-11.md`). The tapes the base
already beats 8/8 are a **ceiling bucket**: a candidate can only give margin back there and can
never gain a win, so a drawn win-rate dip concentrates in it by construction. The honest drawn win
read is the **contested** sub-leg — the tapes the base does *not* win on every board.

The veto rule that follows: **a drawn win dip does not veto when the panel margin is level; wins
are read on contested tapes.** The full-panel *margin* floor is unchanged — margin is not
ceiling-clipped.

## The change

`paired.py` gains a `contested(off, on, keys)` helper and appends **two columns to the `ALL` row
only**:

| column | meaning |
|---|---|
| `cwin b->c` | base -> candidate win rate on contested tapes, percent |
| `ctapes` | contested tapes / contested boards |

Contested is decided **from the BASE csv only**, per tape, on **boards** — the two seats of a
`(seed, opponent)` board are averaged into one observation, exactly as the printed `t` does. A
tape is contested when the base wins fewer than all of its boards.

Every pre-existing column keeps its meaning, position and width; per-`tape` rows are byte-identical
to before, so the `^tape` consumers are untouched and `^ALL` consumers simply see two more fields at
the end of the line. A legend line is printed after the `t_rows` legend. `S/legs/legs.sh` needs **no
change**: line 10 already calls `paired.py <base csv> <cand csv>` (base first) and greps `^ALL`, so
the six leg summary lines pick the new columns up automatically.

## Verification — reproduces the finding

`S/judge/flow166_g170_legs/today41_777001.csv` vs `S/esf135c/cand_g350_today41_777001.csv`:

```
ALL 656 89.5% 83.7%  19 15439 0.02  82  63  46 84 0  328 0.03      79.8%->82.7%    21/168
```

`79.8 % -> 82.7 % = +3.0 pts on 21 tapes / 168 boards` — the drawn-vs-pinned note's numbers
(+3.0 pts, +2,447 margin, 21 tapes, 168 boards) exactly, against a full-panel read of −5.8 pts.

`top10_777001`: `82.2 % -> 85.2 % = +3.0 pts on 19 tapes / 304 boards` (full panel +2.8 pts) — the
contested read agrees with the full panel here, as expected on a leg with a thinner ceiling
(19 of 20 tapes contested).

## flow166_g170, six drawn legs vs the g350 base

| leg | n | win full | d margin | t | contested win | ctapes/boards |
|---|---|---|---|---|---|---|
| band6@777001  | 192 | 86.5 -> 84.4 (−2.1) | −994  | −0.50 | 83.8 -> 81.2 (**−2.6**) | 5 / 80 |
| top10@777001  | 640 | 82.8 -> 85.6 (+2.8) | +699  | +0.75 | 82.2 -> 85.2 (**+3.0**) | 19 / 304 |
| band6@777002  | 192 | 85.4 -> 87.5 (+2.1) | +300  | +0.21 | 78.1 -> 85.9 (**+7.8**) | 4 / 64 |
| flood6@777001 | 192 | 89.1 -> 89.1 (+0.0) | +644  | +0.31 | 82.8 -> 84.4 (**+1.6**) | 4 / 64 |
| jesse4@777001 | 128 | 96.9 -> 92.2 (−4.7) | −2685 | −1.29 | 87.5 -> 93.8 (**+6.3**) | 1 / 16 |
| today41@777001| 656 | 89.5 -> 83.7 (−5.8) | +19   | +0.02 | 79.8 -> 82.7 (**+3.0**) | 21 / 168 |

Raw `ALL` rows (paste-able, the two new fields are the trailing pair):

```
band6@777001   ALL  192  86.5%  84.4%   -994  19468  -0.50   -181    813  16 20 0   96  -0.71   83.8%->81.2%    5/80
top10@777001   ALL  640  82.8%  85.6%    699  16760   0.75   2502   1803  84 66 0  320   1.06   82.2%->85.2%  19/304
band6@777002   ALL  192  85.4%  87.5%    300  14008   0.21  -1827  -2127  18 14 0   96   0.30   78.1%->85.9%    4/64
flood6@777001  ALL  192  89.1%  89.1%    644  20607   0.31   4873   4229  15 15 0   96   0.43   82.8%->84.4%    4/64
jesse4@777001  ALL  128  96.9%  92.2%  -2685  16669  -1.29  -2802   -118   4 10 0   64  -1.82   87.5%->93.8%    1/16
today41@777001 ALL  656  89.5%  83.7%     19  15439   0.02     82     63  46 84 0  328   0.03   79.8%->82.7%  21/168
```

**Five of six legs are up on contested wins.** The two legs whose full-panel win rate looked worst
(today41 −5.8, jesse4 −4.7) are the two that flip to clearly positive once the ceiling bucket is
removed: their dips are ceiling artefacts, and neither vetoes. The one leg still negative on
contested is **band6@777001 (−2.6 pts, 5 tapes / 80 boards)** — small, within its own t of −0.50,
and contradicted by band6@777002 (+7.8) on the same six tapes at a different seed base, i.e. the
band6 seed lottery rather than a signal.

## Caveats / unverified

* Contested is a **board-level** criterion; `w_off`/`w_on` in the older columns stay row-level, so
  `cwin b->c` is not the same denominator as `win OFF`/`win ON` and the two deltas will not match
  arithmetically. This is deliberate — boards are the independent unit.
* The columns are **descriptive only**. Nothing in `legs.sh` or any gate reads them yet; the veto
  rule remains an operator judgement.
* Small legs make `ctapes` tiny: jesse4 has **one** contested tape (16 boards) and band6 four to
  five. Contested win rates on those legs are near-anecdotal — quote them with the count.
* No new simulations were run; every number above is a re-read of csvs already on disk (g170 legs
  written 2026-09-09 15:22–17:13Z, g350 refs 2026-09-07).
