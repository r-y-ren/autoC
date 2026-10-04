# Seat-swap objective field at flow172_g1000 — the other seat of the pinned block (2026-09-11)

Agent measurement, 60-min box. Rig + results in `S/popcurve/B/seatswap.{py,json,log}` (remote `~/popcurve/B/`:
margins `seatswap*_margins.npz`, `grads/g_seat_t{0,1}_p512_s{9001,9002}.npy`, rollouts `p512_s*_t1.npz`).
GPU0 next to flow190, chunk 4096, 1,868 s.

## 1. What "the other seat" is in this trainer (read before the numbers)

`Trainer.pinned_seats(n)` (`~/stage_hr/src/kagg3/es/train.py:4653`) is `(t + i) % 2`: under `--pinned-once` the
seat of pinned rung *i* **already alternates every generation**, staggered by rung (74/73 split inside each
generation, swapped the next). The arm does not train from one seat; every pinned board is seen from both seats
on consecutive steps. There is **no CLI flag** for it (`--real-gate-pinned-seats` is the engine gate only); the
rotation is hard-wired off `self.t`. B / msab / lostw / recentre measured the `t=0` phase. This rig builds the
`t=1` phase (same 147 pinned words, every rung on its other seat; 12 carried episodes re-drawn as the arm would)
as the "seat-1 batch"; §2 also re-sorts the outcomes by *actual* seat.
## 2. F(centre) by seat — g1000 is as strong on the other seat

| field | pinned win | lost / 147 | obj_w | mean margin |
|---|---|---|---|---|
| phase t=0 (B's batch) | 72.1 % | 41 | 0.5951 | +4,110 |
| phase t=1 (every rung swapped) | 71.4 % | 42 | 0.5932 | +4,081 |
| actual seat 0 (74 rungs from t=0 + 73 from t=1) | 72.1 % | 41 | 0.5938 | +4,058 |
| actual seat 1 | 71.4 % | 42 | 0.5966 | +4,134 |

Per rung: won from both seats 104, lost from both 40, seat-0-only 2, seat-1-only 1; **per-rung margin correlation
across seats 0.994**. A `--with-town` board is one deterministic game whichever seat we hold (the `--pinned-once`
help text says so: "both seats return the same coins"); the town schedule fixes shops and the opponent's orders,
so the seat changes row order only. The other seat is **not a new field**.

## 3. Gradients

Same eps (seeds 9001, 9002), P 512, sigma 0.02, ms 3000, ||d|| 0.2323; g_t0 from B's saved rollouts (cos vs B's
stored gradient ≥ 0.9999), g_t1 from a fresh rollout on the t=1 batch, g_pool = (g_t0 + g_t1)/2 (the same-eps
estimator of the mean objective over both phases, up to per-field rank normalisation), all stepped at ||d||.
**cos(g_t0, g_t1) = +0.982 (9001), +0.977 (9002)**; ||g_pool||/||g_t0|| 0.98 — the seat swap moves the direction
far less than the seed lottery (cos across seeds ≈ 0); the three steps per seed are near-copies.

## 4. One-step comparison (+d gain = F(+d) − F(c); `beats` = of B's 16 random ±d controls)

**IN-SAMPLE phase t=0** (F(c) obj 0.5951 / win_w 0.6102 / margin +2,646; random step −0.0110 obj, 15/16 lose)

| step | obj +d | obj −d | antisym | z | κ | beats | win_w +d | margin +d | margin antisym (z) | beats (margin) |
|---|---|---|---|---|---|---|---|---|---|---|
| es9001_t0 (= B) | −0.0216 | −0.0292 | +0.0076 | +0.56 | +0.007 | 2/16 | −3.9 pt | −473 | +128 (+0.31) | 2/16 |
| es9001_t1 | −0.0143 | −0.0219 | +0.0076 | +0.56 | +0.007 | 6/16 | −2.1 pt | −215 | +346 (+0.83) | 8/16 |
| es9001_pool | −0.0174 | −0.0175 | +0.0001 | +0.01 | +0.000 | 4/16 | −3.2 pt | −354 | +60 (+0.14) | 5/16 |
| es9002_t0 (= B) | −0.0160 | −0.0153 | −0.0007 | −0.05 | −0.001 | 6/16 | −4.2 pt | −162 | +41 (+0.10) | 8/16 |
| es9002_t1 | −0.0085 | −0.0132 | +0.0047 | +0.34 | +0.005 | 9/16 | −2.8 pt | **+20** | +365 (+0.87) | 12/16 |
| es9002_pool | −0.0121 | −0.0164 | +0.0043 | +0.32 | +0.004 | 6/16 | −3.5 pt | −51 | +355 (+0.85) | 11/16 |

**IN-SAMPLE phase t=1** (F(c) obj 0.5932 / win_w 0.6066 / margin +2,680; random step −0.0065 obj, 13/16 lose)

| step | obj +d | obj −d | antisym | z | κ | beats | win_w +d | margin +d | margin antisym (z) | beats (margin) |
|---|---|---|---|---|---|---|---|---|---|---|
| es9001_t0 | −0.0144 | −0.0295 | +0.0151 | +1.63 | +0.021 | 3/16 | −2.3 pt | −359 | +145 (+0.42) | 1/16 |
| es9001_t1 | −0.0091 | −0.0154 | +0.0063 | +0.68 | +0.009 | 5/16 | −1.0 pt | −237 | +333 (+0.97) | 5/16 |
| es9001_pool | −0.0108 | −0.0120 | +0.0012 | +0.13 | +0.002 | 5/16 | −0.6 pt | −323 | +1 (0.00) | 2/16 |
| es9002_t0 | −0.0086 | −0.0154 | +0.0068 | +0.74 | +0.010 | 5/16 | −2.5 pt | −5 | +460 (+1.34) | 9/16 |
| es9002_t1 | −0.0028 | −0.0135 | +0.0108 | +1.16 | +0.015 | 11/16 | −0.9 pt | **+86** | +553 (+1.62) | 12/16 |
| es9002_pool | −0.0032 | −0.0149 | +0.0117 | +1.26 | +0.016 | 11/16 | −1.3 pt | **+113** | +560 (+1.64) | 13/16 |

**IN-SAMPLE pooled pinned block (294 = 147 × 2 seats, ep_cur)** — F(c) obj 0.5952 / win_w 0.6096 / margin +2,692;
random −0.0086 obj (14/16 lose). All six steps lose obj (−0.005 … −0.017) and win_w (−1.3 … −3.1 pt); margin +d
es9002_t1 +67, es9002_pool +42 (10/16), the rest −62 … −397; obj antisym z 0.17 … 1.08, κ ≤ 0.014.

**Displacement (in-sample; a random step flips 7.1 / 7.7 won rungs down, 2.6 / 3.8 lost up on t=0 / t=1):** the
t1 and pool steps flip 8-11 won rungs down and 2-5 lost up on *both* phases (es9001_t1+ 9/3 on t=0, 9/5 on t=1;
es9002_pool+ 11/3, 9/4) — the cost of B's own step (10-11 / 2-4) and of a random one. The seat-1 step does not
lose seat-0 rungs more than any direction; it buys back ≤ 5 of the 40 rungs lost from both seats.

**HELD-OUT (LIVE-C 43-72, 30 boards × 2 seats, uniform)** — F(c) obj 0.6161 / win 0.6667 / margin +3,179
(lostw: 0.6158 / 0.6667 / +3,177); random step −0.0171 obj / −6.9 pt / −481 coins (13/16, 15/16, 14/16 lose)
| step | obj +d | obj −d | antisym | z | κ | beats | win +d | margin +d | margin antisym (z) | beats (margin) | flips −/+ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| es9001_t0 (= B) | −0.0057 | −0.0430 | +0.0373 | +1.23 | +0.016 | 11/16 | −3.3 pt | −213 | +832 (+1.20) | 12/16 | −2/+0 |
| es9001_t1 | −0.0019 | −0.0205 | +0.0186 | +0.61 | +0.008 | 13/16 | −3.3 pt | −301 | +22 (+0.03) | 11/16 | −2/+0 |
| es9001_pool | −0.0099 | −0.0325 | +0.0226 | +0.75 | +0.010 | 10/16 | −3.3 pt | −247 | +215 (+0.31) | 11/16 | −2/+0 |
| es9002_t0 (= B) | −0.0118 | −0.0164 | +0.0045 | +0.15 | +0.002 | 10/16 | −6.7 pt | −440 | +257 (+0.37) | 10/16 | −4/+0 |
| es9002_t1 | −0.0201 | −0.0419 | +0.0218 | +0.72 | +0.009 | 8/16 | −6.7 pt | −444 | +571 (+0.82) | 10/16 | −4/+0 |
| es9002_pool | −0.0153 | −0.0318 | +0.0165 | +0.54 | +0.007 | 9/16 | −10.0 pt | −409 | +527 (+0.76) | 10/16 | −6/+0 |

## 5. Reading

1. **The other seat is the same field.** Per-rung margin correlation 0.994 across seats, 144/147 rungs with the
   same outcome, cos(g_t0, g_t1) 0.98 on both seeds. A pinned-town rung fixes the shops and the opponent's
   orders; the seat only decides who resolves a row first. g1000 is exactly as strong from seat 1 (71.4 %,
   42 lost) as from seat 0 (72.1 %, 41 lost), and the 40 rungs lost from one seat are lost from the other.
2. **Consequently the seat-1 / pooled gradients are B's gradient with slightly less noise**, and their steps
   behave like B's: in-sample every step loses obj and win_w on both phases (−0.003 … −0.022 obj); the only
   positive cells are three margin +d gains of +20 … +113 coins (es9002_t1 / es9002_pool, z 0.9-1.6, 12-13/16),
   inside the seed lottery the recentre doc measured (their 9001/9002 disagreement was the same size) and
   not reproduced by seed 9001 (−215 … −354).
3. **Held-out is a loss on every step and both seeds**: obj −0.002 … −0.020, win −3.3 … −10.0 pt, margin
   −247 … −444; antisym z ≤ 0.75, κ ≤ 0.010; no held-out loss flips up on any step, 2-6 wins flip down. The
   staging rule (held-out net gain > 0 on obj AND margin, ≥ 12/16 randoms on both seeds) fails its first clause
   for all four candidates; the best cell (es9001_t1 obj −0.0019, 13/16) is "loses less than random", as B does.
4. The arm already rotates seats per generation (§1), so g1000 was *trained* on both phases; a peak on both
   is what that rotation should produce.

## 6. Verdict

**Negative. flow192 is NOT staged** (no `~/launch_flow192.sh`, no `S/flow192/`). Two independent reasons:
(i) the measurement fails the held-out rule on every step and seed; (ii) there is no trainer flag to
change the pinned seat — the alternation is hard-wired in `pinned_seats` and already plays both seats —
so there was nothing an arm could be told to do differently even on a positive read (the task said: no
flag → stage nothing). Playing both seats *within* one generation would need a code change to
`pinned_keep`/`pinned_seats` (out of scope, src is frozen) and would buy a ×2 episode cost for a field with
correlation 0.994 to the one already played, i.e. nothing.

**A genuinely changed field** must change the *opponent or the board*, not our seat: fresh top-tier pinned tapes
inside the fitness (flow190's widened rungs are the closest live thing) or another opponent family. Re-weighting
(lostw) and re-seating (this doc) are both closed.

## 7. Dead ends / caveats

* Held-out win quantised at 1/60 (obj/margin carry it). One rollout per phase per seed; g_pool is the mean of two
  same-eps gradients (rank-normalised per field), not a 1,024-member draw. The t=1 batch re-draws the 12 carried
  episodes; the pooled block and §2 by-seat rows use pinned rungs only. Setup 576 s with three jobs on the card,
  total 1,868 s; `centre_reproduced` not re-asserted (lostw: 4/159 episodes differ, no class flips).
* Not tried: both seats of one rung inside one generation at P 256 (pointless at correlation 0.994); seed 9003.
