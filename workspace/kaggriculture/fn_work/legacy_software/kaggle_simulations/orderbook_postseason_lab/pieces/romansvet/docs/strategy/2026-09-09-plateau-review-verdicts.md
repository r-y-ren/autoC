# 2026-09-09 — reviews of the plateau-diagnosis claims, and the held-out anatomy

Durable record of the subagent reports produced on 2026-09-09 (UTC). Each
section is the agent's own verdict, lightly trimmed. Raw summaries are in
`docs/strategy/2026-09-09-reviews/`; the dated one-line log is
`docs/strategy/2026-09-09-verdicts.txt`. Context: live sub 56098262 =
flow135_g350 (rating ≈2000); judge = 42 pinned held-out live boards (live
theta 9/42); campaign target = top 10 (≈2850) by 2026-09-23.

**Index of sections.** Sections 9-40 were appended after "What we use" and out of
order; nothing is moved, so use this list. §0 ES step dynamics per block (the centre is
an Adam-floor random walk; forward gene re-centred). §1 transfer / sampling / gate
statistics — not binding. §2 intraday market re-planning — closed. §3 forecast features
in the global head — already implemented, inert. §4 production timing and product
composition in the strategic heads — architecturally closed. §5 labour, purchases and
routing as one allocation — not binding. §6 held-out anatomy on 42 pinned live boards.
§7 why the late tomato/carrot/egg leg is missing (shop sinks; group selection). §8
reactive opponent diversity — not binding, the field is open-loop. §9 block ablation —
neither trunk nor new blocks own the held-out edge. §10 sell cadence — more sell rows
change nothing. §11 judge calibration — the 42-board flip count is a lottery (LEG20 rule
adopted, later superseded by §34/§36). §12 feed supply — FEED_RESERVE not binding. §13
plant-mix drain tilt — dose-responsive loss. §14 care-with-feed ride-along — flat, OFF.
§15 care-fill / care-hold — inert, then margin down. §16 today's six Kaggle losses — one
clone signature, no new loss class. §17 plant-fill-late — the idle-land family closed.
§18 pasture cadence — the grant ranks seeds above animals. §19 herd composition —
revenue per animal-day tracks the season sink; our one-day shop lag. §20 fertilizer
over-spend — an income-line artifact, not a lever. §21 animal restock — inert. §22 why
in-sim records lose the leg family — the training population, not the sim (the flow166
fix). §23 herd-mix residual-drain tilt — first knob past the LEG20 rule, legs pending.
§24 top ten vs the clone — the wall is adaptive late mix. §25 animal-first grant order —
grant-order family closed. §26 ROUTE_EARLY_ON — broken switch. §27 tomato sink gate at
one shop — the hand tomato family stays closed. §28 flow166 gen 50, the first leg-family
record — judged, not promoted. §29 shipped-off switch sweep in the sim — TAIL_FILL+BANK
flagged. §30 sim fidelity on fresh tapes — the LOSS12 sim column withdrawn. §31 sim
shed-ordering bug — PICKUP before DROP strands animals. §32 tail-fill + bank-before-lot
pair — engine-confirmed, legs pending. §33 flow166 gen 150 anatomy — growth, not denial.
§34 the family gate was a coin flip — SE ≈17.7k; the gate moved to fresh losses. §35
fresh-loss leg noise — LOSS12 SE, leg extended to LOSS20. §36 what has ever predicted
Kaggle — nothing local; the drawn legs become a veto. §37 first candidate to pass the
fresh-loss read: flow166 gen 170. §38 sim shed fix shipped — arms restarted as
flow172/173. §39 today's Kaggle slide is noise on an honest 43 % baseline. §40 flow166
gen 170 on the 55-board held-out live set — rule pass, veto pending. §41 (appended
after this index was written) two candidates pass the live read.

## Reviewed claims — do not re-review without new evidence

| # | claim (2026-09-08 plateau diagnosis) | verdict | date |
|---|---|---|---|
| 1 | transfer to real opponents; fix sampling + gate statistics; held-out families | fixed in code; not binding; residual → top-ten tapes into training (flow158) | 2026-09-09 |
| 2 | revise market decisions during the day | closed: goods reach the shed at end of day; every excursion lost/level; refusals 0.07 % | 2026-09-09 |
| 3 | forecast features into the global head, retrain jointly | already implemented (fh/fs/gp/fv/g11), inert; not binding | 2026-09-09 |
| 4 | give strategic heads production timing + product composition | architecturally closed on 6789 layout; zero on live champion; labor demand absent; not binding while selection is at the noise floor | 2026-09-09 |
| 5 | make labor, purchases, routing one coordinated allocation | not binding: route completes 99.8 % of queued value; HIRE_ROW_ON (the proposed reconciliation) exists, engine −378/game t −0.75; gap = planting date + crop choice | 2026-09-09 |
| 6 | repair training coverage (restated #1) + reactive opponent diversity | #1 parts reused; reactive diversity not binding: no trainer seat is opponent-reactive, synthetic seats always inflated in-sim and lost the gate, the field is open-loop | 2026-09-09 |

## 0. ES step dynamics per block (stepdyn)

rms per parameter of |θ − flow135_g350_gpfwdfv| at gen 90, sigma 0.02:
every block 0.028–0.034 (w1 0.0294, g1 0.0280, fh 0.0302, gp 0.0292,
fv 0.0292, g11 0.0345). Adam grad rms 0.42 in every block, snr
|m̂|/√v̂ 0.17–0.19 everywhere (pure-noise expectation 0.23), |step| 0.22·lr,
drift/√gen flat at 0.0033 across flow150–155 → the centre is an
Adam-floor random walk, no directed block. Forward gene: flow155 centre
z = −0.196 ± 0.106 (max −0.018) → 0 days on 2400/2400 boards, 3.2 sd below
the 0.031 decode threshold; selected one-sided into its clip. Fix adopted:
re-centre gb11 to +0.028 (centre still decodes 0 days = live; ≈44 % of
sigma-0.02 members decode ≥1 day). flow156 (sigma 0.02) and flow152
(sigma 0.03) restarted on that init.

## 1. "Make training transfer; fix sampling and gate statistics" — NOT binding

- Sampling allocation: FIXED. `SlotCarry` (train.py:714) token bucket,
  default on; `--pinned-once` gives every pinned rung one episode per
  member per generation.
- Gate statistics: FIXED twice. `paired_stats(group_seats=True)`
  (train.py:1625); pinned boards are identical in both seats and
  `--real-gate-pinned-seats 1` counts each board once; the gate decides on
  net flips (min-flips 3), no t-stat.
- Held-out families: 1 of 35 held-out players also appears among the 117
  training tapes; training tapes median rating 2019, 40/69 ≥2000.
  RESIDUAL: only 1 training tape ≥2200 and all 20 top-ten tapes are
  gate-only → the ES never sees the 2850 band. → `launch_flow158.sh`
  (top-ten tapes into training at weight 3, gate = 42 held-out) queued.
- "More compute moves us backward": the 2026-09-08 instance was a
  drawn-town artefact (drawn towns cripple open-loop tapes: g350 81 %
  drawn vs 2/10 pinned on the same fresh top-ten tapes). Real backward
  case was rung memorisation (flow148: +30 own tapes, 56.7→51.5 %
  held-out). Under the pinned gate records are flat, not backward.
- Held-out by opponent rating: <1900 (n 17) g350 8, flow155_g50 10,
  oracle-of-14-thetas 10; ≥1900 (n 18) g350 0, flow150_g40 2,
  flow155_g50 1, oracle 5. Every flip bought is on a sub-1900 opponent =
  behaviour ceiling of the policy family, not transfer.

## 2. "Let it revise market decisions during the day" — NOT binding (CLOSED)

- Premise true: runtime.py:30–46 builds the plan at hour 0 and replays;
  no re-plan on refused orders or price moves.
- Mechanics bound: collected goods sit in the unit until the end-of-day
  drop (sim/units.py:171, eod.py:210); OP_DROP only on the terminal day
  (plan.py:5933). Mid-day information cannot become a same-day sale
  without a purpose-built excursion.
- Every excursion measured paired lost or was level: OPP_SUPPLY −2,972 /
  −3,616 (t −3.8/−4.8); MIDDAY_PLACE_V2 −101; COLLECT_DAY_SELL +100 no
  flip; LATE_LOT inert; COLLECT_DROP pinned +16/−5 but drawn −1,441;
  EARLY_MILK −1,592; wool/tomato/carrot/herd all dose-responsively
  negative. Only won market lever EARLY_SELL A (+2,184 t 5.1) is a dawn
  schedule, shipped.
- Refusal count (24/42 held-out boards, engine-instrumented): our orders
  refused 3.96×/game = 0.07 % of 5,666 acting turns; 0 of 1,971 BUY rows and 0 HIRE/LAND/
  PLACE/DROP/PICKUP/MOVE refusals. Only signature:
  d21–29 SELL rows short ≈19 units/game (liquidation sizing). A
  re-plan-on-refusal hook has nothing to react to.

## 3. "Add forecast features into the global head, retrain jointly" — ALREADY DONE, not binding

Present in the 6789 layout, all zero-init prefix extensions of the 4,980
champion, jointly retrained in flow146–157: fh/fs 528p (own + opponent
production forecast, horizons 1/3/7 d, brain.py:283/492), gp 864p (product
summary into the head, policy.py:416), fv 384p (forward value,
brain.py:444), g11/gb11 33p (forward-admit horizon gene). Missing:
recent-sales history (PolicyObs is single-frame) and ready-to-harvest as a
head input (fv slices b[:,1:]). Every candidate from those arms is +3
held-out boards, margin down, 6/6 drawn legs down. Block ablation
(θ_old = candidate with new blocks reset; θ_new = g350 + new-block delta)
launched to attribute the +3 boards.

## 4. "Give the strategic heads production timing and product composition" — architecturally closed

Probes re-run on the 6789 layout (headinfo_review/probe.py, day-12 board):
with flow155_g50 (new blocks non-zero) strawberry-maturity change moves
47/47 global-head outputs (max .056) and ten-strawberry→ten-melon moves
47/47 (max .101) → the statement's exact claim is false now. On the live
champion the new blocks are exactly 0.0, so both probes reproduce the old
finding (0/47). Genuinely missing: expected labor demand (no block
anywhere); ready-to-harvest into the head (a 4-unit standing harvest moves
0/12 fv columns, reaches the head as a .0035 tremor via gp). With every
block at the same noise-floor snr, added inputs cannot be selected on →
deferred.

## 5. "Make labor, purchases, routing one coordinated allocation" — NOT binding

Sequence accurate (`_plan_and_stats` plan.py:5876: pass A derive with
hire_bill 0 at :5990, hire argmax :6046–6112, pass B :6117, admit/route
:6467–6495; `budget.grant` budget.py:146 = cash + shed only). Pass B differs
from pass A on 11.1 % of day-rows, all land days. Instrumented 180 day-rows
on 3 held-out boards: routed 99.8 % of 577,875 queued value/game;
admitted-not-routed 0.13 %; never-admitted 0.09 %; seeds idle 0.08
tiles/day; all-PASS hand-days (15.2/game) are hands with no ranks left.
Forced-crew history is the opposite of under-hiring (ramp11 PASS 15→37 %,
revenue 112.8k→67.3k; crew-12-by-d9 ours −887 / theirs +7,992;
CREW_FROM_TASKS per-hand 5 −4,580 t −28; FORWARD_ADMIT_ON 94→65 %). The
proposed bounded reconciliation pass already exists: `HIRE_ROW_ON`
(plan.py:3497, shipped OFF) removes all idle hand-days and +889 bill, and
reads −378/game t −0.75 on 768 paired engine games. Execution waste caps at
≈2k nominal against a −10.3k margin and does not convert. Gap = planting
date (they seed melon d0, we buy d3–5, first sale d15.8–18.5) and crop
choice, i.e. the mix genes. Unclosed planner item: cadence pair (hourly
PLACE+SELL vs our three fixed SELL_TURNS) — next measurement: the clone
seat's PASS share on the same boards.

## 6. Held-out anatomy (42 pinned live boards, live theta, both seats)

Day 10, ours / theirs: cash 3.1k / 15.9k; hands 9.8 / 10.7; planted
44.5 / 34.1; occupied 59.8 / 51.1; animals level; quads 2.9 / 2.1. We lead
every physical asset; the opponent's edge is cash from liquidating 68–90
melon units on d10–11 in 24-unit orders (≈215/u); we sell 0 melon d10–11
on all 42 boards. Day-10 state does NOT separate hard-loss / close-loss /
win groups.

Post-d10 ledger: d0–9 ≈13.8k both; d10–11 ours 4.7k vs theirs 20–22k (all
melon); d12–19 level; d20–29 ours 59–69k vs theirs 37–55k. The melon
d10–11 deficit (−14.9k hard / −17.2k win), fertilizer d12–19 (−3.2k) and
wool d0–9 (−2.6k) are the same in wins and losses → constant deficit, not
the separator. SEPARATOR: hard-loss opponents earn +25.4k more from
milk/strawberry/wool (board richness, which we track unit-for-unit) and on
those boards WE MISS THE LATE DIVERSIFICATION LEG: tomato d20–29 613 vs
7,622 on win boards (−7.9k), carrot d20–29 1,544 vs 6,486 (−5.4k), egg
d12–29 1.4k vs 5.4k (−4.2k); the opponent takes 913 tomato / 3,168 carrot
from those same markets. Prices per unit d12–29 level. Our melon tonnage
matches theirs (≈90 units) but lands after d12 at 147/u into our own flood
instead of 215/u on d10–11, and cannot compound.

## 7. Why the late tomato/carrot/egg leg is missing on hard boards (latediv)

Correction to §6: there is no seed offer draw (seeds/animals always buyable,
spec.py:41–49); the end-of-day draw picks SHOPS = demand sinks
(spec.py:174–199), pinned per board on the judge. The gap is (a) sink
availability: our late carrot coins r +0.66 with carrot sinks (+0.77 with
sink×days-remaining), tomato +0.48/+0.64, egg +0.48; all 14 boards with ≤1
carrot sink earn exactly 0 late carrot (5 HARD, 0 WIN); sink-matched the
group gap mostly vanishes (carrot at 2–3 sinks HARD 215 vs WIN 333). HARD
towns are wool/milk/strawberry towns (2.3/3.5 sinks vs 1.3/2.8) where the
open-loop tape gets rich → the 613-vs-7,622 gap was GROUP SELECTION. Not
(c) capital: d10 cash/tiles equal, same late seed volume, we earn more by
d19 on HARD. Not (b) a planner rule: ENDGAME_TOMATO_ON, OPP_MIX_ON,
PLANT_MIX_DRAIN_ON all inert; the shop→mix response is learned inside
theta via residual_drain (brain.py:227–275). Residual: at ≥4 carrot sinks
HARD 4,803 vs WIN 9,562 and at 2–3 tomato sinks 1,261 vs 7,936 — the tape
takes more of the pot, our few units sell higher (61/u vs 47/u) =
supply-short, we enter the race late. Paired probe queued
(S/drainpin/run.sh): PLANT_MIX_DRAIN_ON with gain 0.5/1.0/2.0 on the pinned
judge, d-ours/d-theirs read separately, split by sink count.
## 8. "Expand reactive opponent diversity" (restated coverage claim, new sub-point) — NOT binding

No trainer opponent is opponent-reactive: archetypes (archetypes.py:458)
are zero-weight presets of our own planner with every opponent feature
multiplied by 0; the self-play pool (train.py:2813) is our own lineage;
kagg2_flow / kaggle_flow replay market tables; tapes are byte-exact
open-loop. Archetypes sit at weight 0 because every arm that weighted
synthetic or self-play seats up climbed in-sim and fell in the engine
(flow87, flow120, flow123–127), and every promoted record came from tape
rungs (flow128/129). The graded field is an open-loop clone family: pinned
tapes reproduce live games coin-for-coin and the opponent's committed and
refused order streams are byte-identical under our flips. Under
--pinned-once any synthetic seat takes slots off the 86 live boards. The
real coverage residual is rating (one training tape ≥2200) → flow158.

## What we use

Rewritten at the end of the day from sections 0-40 and
`docs/strategy/2026-09-09-verdicts.txt`; it replaces the morning's version.

**1. The promotion read.** A candidate is promoted on the **LIVE55** set only: the 55
pinned boards cut from the live submission's own games that are not training rungs (62
tapes cut, 7 already rungs — §40, log 15:27Z), played in the engine paired against the
LIVE theta, 110 games. The rule is the fresh-loss rule of §36: win rate first, d-margin
> 0 excluding the two non-byte-exact tapes, grouped |t| ≥ 2, and at least 15 of 20
boards positive on the LOSS20 prefix. **Drawn legs (top10, band6, flood6, jesse4,
today41) are a non-regression veto only** — no leg pool significantly negative — and
band6 or jesse4 never veto alone. **Remote gates are screens, not authority.** Why, in
order: §11, the 42-board held-out flip count is a 15-coin lottery with zero true
positives over seven arms; §34, the remote family gate's 20-game sum has SE ≈17.7k, so
today's five accepts were 0.2-0.7 SE, four of five break under a single tape deletion,
and every family variant has Spearman ≤ 0 against the fresh-loss reads; §36, no local
read has ever predicted a Kaggle improvement — the drawn legs overstated the live theta
by 34 points (local 86.8 % vs a live ~52 %) and the "top10 pooled up, band level" rule
promoted flow102_g280, which settled −265; §39, the fresh-loss population is a
representative sample of the band (settled 42.9 % over 163 post-ramp games, today's
field 57 points weaker, p 0.77 for a change), so the target is +4 wins in 72. The live
pinned set keeps growing toward ~120 boards, wins cut as well as losses.

**2. The training recipe.** The first candidate to pass the promotion read came out of
the §22 population fix (recipe archived as `docs/strategy/2026-09-09-launch_flow166.sh`):
a **fixed population of pinned-town rungs** — 147 rungs, 20 at w3, 117 at w2, the 10
leg-family tapes at w0 so they are out of training and out of the rung-weighted abs
nomination; every open-loop rung repointed to `artifacts/tape_actions_town/`; the
byte-identical duplicate 106581754 dropped, gate 49 → 48 opponents / 96 games. Fitness
is margin only: `--abs-weight 0.0`, shaping off (d10-cash 0, tile-fill 0), margin-scale
3000, weight decay 0, init flow135_g350_gpfwdfv_gb028. Gate: `--real-gate-metric leg20`,
`--real-gate-recentre 3`, `--real-gate-every 100`, min-flips 3, pinned-seats 2. flow166
itself ran `--best-margin 0.005`; the lottery audit priced that at 0.14 SE (§11, log
09:21Z) and **0.04 (≈1 SE)** has been standard since flow167. That arm produced five
leg-family accepts and a monotone rise on never-trained fresh boards (g50 +722 → g130
+1,381 → g150 +1,879 → g170 +2,467 a game). The **gate then moved** from the leg family
to live boards: first the 12 fresh-loss tapes (60 gate opponents, §34), now the
**55-board live gate** (103 gate opponents, 206 games a read). The **shed-fixed sim**
(§31, §38) is mandatory under every arm — flow170/171 were killed and relaunched as
flow172/173 on it. Running: flow172 (GPU1, resumed from flow166_g170, fresh-loss gate)
and flow168 (GPU0, drain-mix gene, N_PARAMS 7053, from the padded g170 record, sigma
0.015, best-margin 0.04, 55-board gate, re-centre 3, every 100, seed 268). Queued:
launch_flow174 (=flow172 recipe with the 55-board gate), launch_flow175 (from
flow167_g150, 55-board gate), launch_flow169 (`--abs-weight 0.5`).

**3. Planner switches that survived.** One pair: **TAIL_FILL_ON + BANK_BEFORE_LOT_ON**
(§29, §32). Engine on the pinned judge: held-out +2/−0, H_dm +801, LEG20 +1,403 a game,
against a sim screen of +817 / +1,404 — agreement to 16 coins; tail-fill alone reads
+748 / +1,365 (sim +775 / +1,366). It is a planner switch, so it composes with any
promoted theta and ships with the next promoted package if its drawn legs hold; those
legs are pending. Everything else screened today lost or was inert. Families closed
today, with the number that closed each:

- Sell-hour cadence (§10): 6 rows −324, 4 rows −348 d-margin at +0/−0 → do not revisit sell-hour levers.
- Residual-drain plant-mix tilt (§13): gains 0.5 / 1.0 / 2.0 read H_dm −2,458 / −6,243 / −9,198, dose-responsive.
- Idle-land fill (§17): PLANT_FILL_LATE_ON 21.4 → 9.5 % (+0/−10), H_dm −6,275.
- Grant order (§25): ANIMAL_FIRST_ON 21.4 → 0.0 % (+0/−18), H_dm −52,957, LEG20 −56,864.
- Hand tomato gate (§27): ENDGAME_TOMATO_SHOPS=1 21.4 → 11.9 % (+0/−8), H_dm −8,840.
- Feed reserve (§12): FEED_RESERVE_ON DAYS=2 engine −2,666 ours / +812 theirs.
- Care knobs (§14, §15): CARE_WITH_FEED_ON H_dm −24 / LEG20 −258 (level); CARE_FILL+CARE_HOLD H_dm −332.
- Animal restock (§21): +0/−0, H_dm +54, LEG20 +0 — inert.
- Fertilizer (§20): all 179 applications pay (+16.8k a game); dropping the wheat ones costs −4.1k — not a lever.
- Turn-1 routing (§26): ROUTE_EARLY_ON ≈ −160k a game, 0/42 — a defect, not a measurement.
- Sweep failures (§29): FORWARD_ADMIT −6.4k, OPEN_DENY −30k, SAME_DAY_FERT −30.7k, MIDDAY_DROP −2.7k; FERT_FLOOR, ANIMAL_DEFER, LATE_STRAW_CAP lose; HARVEST_FIRST, OPP_MIX, SHED_OVERFLOW inert.
- 42-board block ablations (§9): each half alone reproduces the same +4 boards — do not re-run them at that n.

**4. Harness rules.**

- Every t we quote is **seat-grouped** (`S/bank/paired.py`); the row-wise t is inflated
  1.38-1.42× because the two seats of a pinned board are near-duplicates (§11, log
  09:31Z). judge.sh reads the LAST LEG20 line and exits 2 on a miss.
- **Fetch a fresh record from `real_gate_pending.npy`**, never `real_gate_cand.npy`
  (overwritten with the incumbent) and not `best_abs.npy` until the next checkpoint —
  the flow150_g40 and flow166_g80 fetches both pulled the wrong file (log 03:48Z,
  12:39Z).
- **Intersect any held-out set with the launch script's rungs before trusting it as a
  judge**: 7 of the 62 live boards were already training rungs, which is why the live
  set is 55; the flow150/151 rung list duplicated 30 drawn ids at launch.
- **Never train on open-loop tape files.** On pinned-town rungs the sim is engine-exact
  to ~85 coins; on open-loop rungs it over-reads the pinned engine by +12k a board and
  agrees on sign 47 % of the time (§22).
- **Never read a sim LOSS column on freshly cut tapes without the shed fix.** Same-turn
  animal hand-offs stranded an animal in the sim on 4 of 12 fresh tapes, 3-6k in the
  opponent's favour (§30, §31); after the fix those tapes sit −165…−682 from the engine
  (§38).
- **Kill chains by PID, never by matching the wait phrase.** An `until grep -q
  JUDGEDONE` process sweep killed four judge monitors sharing the command text (log
  13:43Z), a `pkill -f` killed my own ssh shell (01:58Z), and a process sweep killed the
  melon probe (06:33Z).

**5. Standing evidence — flow166 gen 170** (first candidate to pass the promotion
read; §37, §40 — flow167 gen 150 passed it too, §41).

| read | set | result |
|---|---|---|
| remote gate (leg20, screen) | 20 leg-family games vs g150 | +11,768/20 = +588/game; all-games +171/game; wins 42→40 (−2); margin −645 → −474 (fifth accept, log 14:00Z) |
| local pinned held-out | 42 pinned boards — **in-sample** for flow166 | 21.4 → 36.9 % (+13/−0), H_dm +3,310; LEG20 +1,481 (log 15:11Z) |
| LOSS20 | 20 never-trained live-loss boards vs the LIVE theta | +3,645/game (t 2.83), 16/20 boards positive, 10/40 games flipped from a 0/40 base; excluding the two non-exact tapes +4,855, SE 1,030, t 4.71 |
| LIVE55 | 55 held-out live boards / 110 games vs the LIVE theta | win 34.5 → 52.7 % (+22/−2), d-margin +2,767; excl-2 mean +3,145, SE 645, t 4.88, 42/53 positive → **RULE PASS**; the 7 in-sample boards read +1,496, below held-out, so no inflation |
| veto legs (drawn) | 1 of 6 done | band6@777001 86.5 → 84.4 %, −994, grouped t −0.5 = level (band6 never vetoes alone) |

**The drawn legs are pending** — five of six still running — so g170 is not promoted and
nothing has been handed over. The package is built and verified to the coin:
`dist/submission_flow166_g170_v2.tar.gz` md5 7f9e540bf3439348c638ac5b88f75353 (theta
flow166_g170 md5 05a59c1b, 6789 params), with v1 d39e5adc as the fallback.

## 9. Block ablation (closed 2026-09-09 07:41Z)

Question: do the appended network blocks (offset ≥4980: fh/fs/gp/g11/gb11/fv) carry the held-out gains of flow155_g50 (12/42) and flow150_g40 (11/42)?
Method: split each candidate at offset 4980 into "old" (new blocks reset to g350 values) and "new" (only the new-block delta applied to g350); pinned held-out 42 boards (84 games), base g350 9/42 = 21.4 %.

| arm | win | flips/drops | d-margin |
|---|---|---|---|
| flow155_g50_old | 26.2 % | +4/−0 | +434 |
| flow155_g50_new | 26.2 % | +4/−0 | −1,099 |
| flow150_g40_old | 23.8 % | +4/−2 | −154 |
| flow150_g40_new | 21.4 % | +2/−2 | −2,316 |

Verdict: each half alone reproduces the same +4 boards as the whole candidate; the boards are near-ties that flip under almost any perturbation. Neither the old trunk nor the new blocks own a held-out edge. NOT binding; do not re-run block ablations on 42-board reads (raw outputs: S/ablation/out.txt, csvs in S/lossflip/flow15*_old|new.csv).

## 10. Sell cadence (closed 2026-09-09 08:50Z)

Claim: the clones sell at 7-9 distinct hours a day vs our 3 fixed sell turns (SELL_TURNS 3/10/18); giving the planner 4 or 6 sell rows a day should recover part of the d15-29 price/unit gap.
Build: SELL_CADENCE_ON / N_SELL_ROWS in worktree sell-cadence (e07bb3b), OFF path byte-identical, 162 tests.
Read (pinned held-out 42, live theta): off = base exactly (+0/−0, d-margin 0); on6 +0/−0, d-margin −324; on4 +0/−0, d-margin −348.
Verdict: NOT binding. Selling more often changes nothing; the separator is which products the sinks want (§7), not the hour of sale. Do not revisit sell-hour levers.

## 11. Judge calibration (2026-09-09 09:00Z) — see docs/strategy/2026-09-09-judge-calibration.md

The 42-board held-out flip count is a 15-coin lottery with zero true positives over 7 arms; the gate is now LEG20 paired Δmargin > 0 (20 pinned games vs the 10 leg-family tapes), H_dm ≥ 0. Calibration to n≈20 arms running (S/judgecal/chain.sh).

## 12. Feed supply (closed 2026-09-09 09:35Z) — see docs/strategy/2026-09-09-feed-supply.md

Claim (from §care-coverage): the clone's +50 care-bonus animal units/game come from wheat supply; our units run out of wheat at the FEED site.
Measured: FEED emitted equals engine fed-days exactly (254.2/game) — no FEED fails for an empty unit inventory. The real cut is 13.3 animal-days/game rationed by `wheat_avail` inside `_derive` (a budget-grant refusal at d13-type days: 7.0 wanted, 3.2 granted).
Lever: FEED_RESERVE_ON (reserve shed wheat for the herd's next-N-day feeds before the wheat lot); DAYS=1 funds zero extra feeds, DAYS=2 funds +4.3 FEED at the cost of shed room → engine −2,666 us / +812 them on 3 boards × 2 seats. NOT binding; stays OFF. Remaining free target: ~40 fed-but-not-cared animal-days/game (CARE is free) → §13 when measured.

## 13. Plant-mix drain tilt (closed 2026-09-09 09:40Z)

PLANT_MIX_DRAIN_ON (brain.py:805; tilt the plant mix by the residual-drain estimate) at gain 0.5 / 1.0 / 2.0 on the pinned held-out 42: 14.3 % (+2/−8, −2,458) / 14.3 % (+2/−8, −6,243) / 6.0 % (+2/−15, −9,198). Dose-responsive loss; NOT binding; stays OFF. Do not revisit residual-drain mix tilts.

## 14. Care-with-feed ride-along (closed 2026-09-09 12:20Z: pinned +2/−0, H_dm −24, LEG20 −258 → level, OFF) — see docs/strategy/2026-09-09-care-with-feed.md

Fed-but-uncared animal-days = 25.7/game; 22.7 of them refused only by `care_pays`. CARE_WITH_FEED_ON (care-cov 78fc82c) drops that price test for a CARE riding the FEED's own tile chain: planner +22.6 care+feed pairs/game, no other op changes, PASS 1,123→1,169. Engine on 3 pinned boards: two games identical to the coin, one −147/+17 → FLAT; the free bonus units do not reach the purse. 42-board paired read chained (S/carefeed); stays OFF unless LEG20 moves.

## 15. Care-fill / care-hold knobs (closed 2026-09-09 10:45Z)

CARE_FILL_ON: pinned held-out +0/−0, H_dm +54, LEG20 +46 (inert, as the care census predicted: its hops start at the tail cursor). CARE_FILL_ON+CARE_HOLD_ON: +2/−0, H_dm −332 (0.6 sd of flips, margin down). NOT binding; both stay OFF.

## 16. Today's six Kaggle losses (measured 2026-09-09 11:00Z) — see docs/strategy/2026-09-09-loss6-anatomy.md

All six reproduce byte-exact on their pinned tapes. No new opponent family (148/168 pinned tapes are one clone signature) and no new loss class. Universal: d10 melon dump 17.4k (a tax, −3.2k net), d10 cash 2-4k vs 15-18k, 12-16 idle tiles, PASS 15-17 % vs 6-10 %, fertilizer −4.1k net. Sharpened item: the pasture loss is herd COMPOSITION — cows 3.35k vs sheep 2.87k each, corr(cow delta, milk delta) 0.91; the −22k saitamad game is 4 cows vs 8 after a day-3 YARN_STORE pulled the herd to sheep.

## 17. Plant-fill-late (closed 2026-09-09 11:20Z)

PLANT_FILL_LATE_ON (board-fill ee7328d; fill idle unlocked tiles from day 12): pinned held-out 21.4→9.5 % (+0/−10), H_dm −6,275, LEG20 d-margin -6551. Loses outright like the full fill (§board-fill dry run: −5.6…−6.9k own coins). NOT binding; the idle-land family is closed — at our tile count labour is slack, at theirs it binds and the herd bill pays for it.

## 18. Pasture cadence (measured 2026-09-09 11:30Z) — see docs/strategy/2026-09-09-pasture-cadence.md

Premise corrected: we lead the herd d1-4 and hold more cash to d10; the gap opens d6-10 and freezes at d12 (14-16 vs 17 animals). Cause on the trailing days: the budget grant ranks seeds above wanted, affordable animals (14 animals across 4 day-states; 12 strawberry bought instead). Ledger item re-priced at +6.4k/game net (was +12k), 72 % after d12. Levers under test: ANIMAL_RESTOCK_ON (refill built-but-empty coops/pastures from d12; planner +34 animals, PASS −52) and an animal-first grant order. Engine reads pending; nothing promoted.

## 19. Herd composition (measured 2026-09-09 12:00Z) — see docs/strategy/2026-09-09-herd-composition.md

Cow-vs-sheep value is board-specific (sign flips 2/6); the general fact is that revenue per animal-day tracks the season SINK (wool +0.98, milk +0.89). We buy the animal of the LAST shop unlocked (one-day lag, 6/6), the clone buys cows first open-loop. Matching their cow share is mostly denial (+2.2k margin, own purse negative on 2/6). Lever under test: ANIMAL_MIX_DRAIN_ON (residual-drain logit in the herd mix). The shop-lag reaction itself (YARN_STORE pull) is the exploitable error; a lever on it must be priced two-purse.

## 20. Fertilizer over-spend (closed 2026-09-09 12:55Z) — see docs/strategy/2026-09-09-fertilizer.md

The "−4.1k fertilizer" line in the loss ledger is an income-line artifact: the clone sells more fertilizer because it uses less. Every one of our 179 applications pays (net +16.8k/game vs their +12.4k); dropping the wheat ones would lose −4.1k/game through the wheat price curve. NOT a lever; do not revisit. Lesson for the ledger: an income-line delta on a purchasable input is not a loss.

## 21. Animal restock (closed 2026-09-09 13:35Z)

ANIMAL_RESTOCK_ON (refill built-but-empty coops/pastures from day 12): pinned held-out +0/−0, H_dm +54, LEG20 +0 — inert; the structure-refill fires on one board in three and moves ~2 animals. NOT binding; stays OFF.

## 22. Why in-sim records lose the leg family (measured 2026-09-09 14:05Z) — see docs/strategy/2026-09-09-sim-vs-leg20.md

Not a sim gap: on town-pinned tapes the sim matches the engine to ~80 coins with Spearman 1.00. It is the training population: 94 % of the weight sits on 99 pinned tapes the gate never plays; the only gate-visible weighted rungs are 15 open-loop tapes with a +12k sim bias and coin-flip signs; the 10 judged tapes carry zero weight. The in-sim gain (+2.6k weighted margin over 50 gens) lands almost entirely on gate-invisible boards and no gate set improves in the engine. Fix: flow166 (open-loop rungs → pinned-town files, all 42 non-family gate tapes at w2, family held out at w0, duplicate tape removed). Follow-up: in-sim leg20 each generation.

## 23. Herd-mix residual-drain tilt (pinned read 2026-09-09 15:20Z; legs pending)

ANIMAL_MIX_DRAIN_ON (care-cov 8ba5778): gain 0.5 → +2/−0, H_dm +13, LEG20 +228; gain 1.0 → +4/−0, H_dm +2, LEG20 +335. First knob to clear the LEG20 > 0 & H_dm ≥ 0 rule, but the margin is +17/game against an SE of ~1,340, so it is not evidence yet. Drawn legs top10 ×2 + today41 pooled at board level (S/amixlegs) decide; promotion needs the pooled paired margin positive at grouped |t| ≥ 2.

## 24. Top ten vs the clone (measured 2026-09-09 15:35Z) — see docs/strategy/2026-09-09-top10-vs-clone.md

Fourteen of twenty top-ten tapes open exactly like the 2000-band clone. After a control for opponent supply, the surviving divergences are late shop-adaptive product mix — tomato with a tomato sink (+3.8k), carrot volume (+3.7k), geese with egg sinks (+2.8k) — and a melon dump that varies with the board instead of a fixed 60 units. PASS share, hands, herd size, tiles and sell cadence are level, and top-ten d10 cash is lower. Implication: the wall is not opening or tempo; it is adaptive late mix, which every hand lever on drawn boards has lost. The route is the ES mix heads on the fixed population plus the residual-drain tilts (§23). Cheap probe: ENDGAME_TOMATO_SHOPS=1.

## 25. Animal-first grant order (closed 2026-09-09 16:20Z)

ANIMAL_FIRST_ON (fund wanted, affordable animals before seed on d3-9): pinned held-out 21.4→0.0 % (+0/−18), H_dm −52,957, LEG20 −56,864. The planner A/B's −153 tiles / +419 PASS compounds into a collapsed season. Grant-order family CLOSED; stays OFF.

## 26. ROUTE_EARLY_ON (sim screen 2026-09-09 17:20Z)

The turn-1 "route while the BUY row is pending" switch (6cbb3e1) collapses the season in the sim on every set (≈ −160k/game, 0/42). That is a defect, not a measurement; the switch stays OFF and is not a candidate until repaired.

## 27. Tomato sink gate at one shop (closed 2026-09-09 17:40Z)

ENDGAME_TOMATO_ON with ENDGAME_TOMATO_SHOPS=1: pinned held-out 21.4→11.9 % (+0/−8), H_dm −8,840, LEG20 −13,301. Loses outright; the hand tomato family stays closed. The top-ten's tomato income is shop-adaptive at a granularity this gate does not capture — it is a job for the mix heads on the fixed population.

## 28. First leg-family record, flow166 gen 50 (anatomy 2026-09-09 20:30Z; JUDGED NOT PROMOTED 2026-09-09 ~23:50Z: today41 −2,121 t −2.7, pooled negative) — see docs/strategy/2026-09-09-flow166-g50-anatomy.md

Remote gate +203/game on the family, local pinned +208, fresh losses +722 in the engine. The anatomy: a fixed day-0 swap (one wheat tile → carrot, one sheep → cow) and fewer sheep; wool −5.8k, milk +2.6k, carrot +1.4k. Two-purse: ours −1.9k, theirs −2.1k on the family — denial with our own purse down, concentrated on three of ten boards, t 0.25. Not a generalising gain on this evidence; the pooled drawn legs decide, prior unfavourable. The gen-80 record beat gen 50 on the family but reads −1.2k/game behind it on the fresh losses (fit to the trained set).

## 29. Shipped-off switch sweep in the sim (2026-09-09 21:00Z, continued 23:20Z: TAIL_FILL+BANK_BEFORE_LOT positive on all three sets → the pair is the candidate) — see docs/strategy/2026-09-09-switch-sweep.md

Nine never-pinned switches screened on the exact pinned boards. One flagged: TAIL_FILL_ON (+775 held-out t 3.3, +1,366 leg family t 2.6, fresh losses −354) → engine confirmation running. BANK_BEFORE_LOT_ON small positive everywhere. FERT_FLOOR, ANIMAL_DEFER, LATE_STRAW_CAP lose; OPP_MIX and SHED_OVERFLOW inert; ROUTE_EARLY broken (§26). Eight switches still unscreened (sweep continues).

## 30. Sim fidelity on fresh tapes (2026-09-09 21:30Z) — see docs/strategy/2026-09-09-loss12-sim-validation.md

The action-seat sim is coin-exact on the family tapes but under-plays the opponent seat by 3-6k on four of the twelve fresh loss tapes, theta-dependently. The sim's LOSS12 column is withdrawn from every screen; the engine leg is the judge for that set. Open bug: which recorded action or town feature the sim mishandles on those four tapes (stream running), because freshly cut tapes feed the training schedule.

## 31. Sim shed-ordering bug (found 2026-09-09 22:40Z) — see docs/strategy/2026-09-09-sim-tape-seat-bug.md

The action-seat sim resolves all PICKUPs before all DROPs in a turn; the engine walks units in index order. Tapes with same-turn animal hand-offs lose the animal in the sim (four of twelve fresh loss tapes; none of the family tapes). Fix: per-unit scan in the shed stage. Until it ships, sim reads on tapes with hand-offs are wrong in the opponent's favour for us, and such tapes in training bias the arms.

## 32. Tail-fill + bank-before-lot pair (engine pinned read 2026-09-09; LIVE55 pass 2026-09-10: 34.5→40.0 %, +6/−0, +875 t 3.7; drawn legs pending)

Engine: HELD-OUT +2/−0, H_dm +801, LEG20 +1,403/game (tail-fill alone +748 / +1,365). The sim predicted +817 / +1,404. First planner switch to pass the leg-family rule with a full standard error of margin. Drawn legs pooled at board level decide; if level or better, the pair ships with the next promoted theta.

## 33. flow166 gen 150 anatomy (2026-09-09) — see docs/strategy/2026-09-09-flow166-g150-anatomy.md

The later gains are growth, not denial: gen 150 − gen 50 is ours +1,659 / theirs +990 on the family, from earlier hiring (4/4 by day 1), fewer idle tiles on days 5-9, and sell rows moved to the evening. Carrot and board fill move in the top-ten census direction; tomato and the melon dump do not. Still concentrated (one board carries the step) and n=10 keeps every t at or below 1.1 — the drawn legs decide.

## 34. The family gate was a coin flip (2026-09-09) — see docs/strategy/2026-09-09-family-volatility.md

The remote gate's 20-game family sum has a standard error near 18k; today's accepts were 0.2-0.7 of it, and no family statistic orders candidates like the never-trained fresh-loss reads. Both arms were restarted from their best fresh-loss thetas (flow170 from flow166 g170, flow171 from flow167 g150) with the twelve fresh loss tapes as the held-out gate and the family moved into training. Promotion authority stays with the local judge: fresh-loss engine leg as the screen, pooled top10+today41 drawn legs as the verdict.

## 35. Fresh-loss leg noise (2026-09-09) — see docs/strategy/2026-09-09-loss12-se.md

At twelve boards the fresh-loss leg's SE is 1.2-2k a game; only flow167 gen 150 clears two SE and the top candidates cannot be ranked against each other. The leg is extended to the twenty loss tapes cut today (LOSS20). Promotion still needs the pooled drawn legs.

## 36. What has ever predicted Kaggle (2026-09-09) — see docs/strategy/2026-09-09-kaggle-calibration.md

Nothing local has. The drawn legs (open-loop tapes on drawn towns) overstated the live theta by 34 points; the "pooled top10 up, band level" rule produced the worst upload of the campaign. From now on the drawn legs are a non-regression veto only and promotion reads the fresh-loss leg (live population, pinned, never trained): LOSS20 margin > 0 without the two non-exact tapes, grouped |t| ≥ 2, at least 15 of 20 boards positive, paired against the live theta. The pinned live set is being grown with today's wins toward ~120 boards.

## 37. First candidate to pass the fresh-loss read: flow166 gen 170 (2026-09-09)

On twenty never-trained live-loss boards against the live theta: +4,855 a game excluding the two non-exact tapes, t 4.7, 16 of 20 boards positive, 10 of 40 games turned from a 0/40 base. flow167 gen 150 passes at the boundary (15/20, t 4.1); flow166 gen 150 fails the board count (14/20). The drawn legs (veto only) are running; the gen-170 package is built and verified to the coin, hand-over waits for the veto.

## 38. Sim shed fix shipped (2026-09-09) — see docs/strategy/2026-09-09-sim-shed-fix.md

The shed stage now walks units in index order. The four fresh tapes that diverged by 3-6k are within the shop-draw band, one family tape became coin-exact, hand-off-free boards are unchanged, and speed is flat. Deployed to both remote stages; the arms restarted on it as flow172 and flow173.

## 39. Today's Kaggle slide is noise on an honest 43 % baseline (2026-09-09) — see docs/strategy/2026-09-09-field-drift.md

The live submission never ran at 52 %: that figure was a 19-1 ramp against sub-1500 opponents. Against the ≥1800 field it has been 44 % on 09-08 and 42 % on 09-09 (p 0.77 for a change). Today's field is weaker, not stronger, and our coins are flat. The fresh-loss leg is therefore a representative sample of the band, and the target is +4 wins in 72, not +10 points.

## 40. flow166 gen 170 on the 55-board held-out live set (2026-09-10) — see docs/strategy/2026-09-09-judge-live55.md

Against the live theta on 55 pinned boards cut from the live submission's own games, none in training: win rate 34.5 → 52.7 % (+22/−2), margin +3,145 a game excluding the non-exact tapes, t 4.9, 42 of 53 boards positive. Passes the promotion read. Drawn legs run as the veto; hand-over follows a clean veto.

## 41. Two candidates pass the live read (2026-09-10)

flow166 gen 170: 34.5 → 52.7 % (+22/−2), +3,145 a game, t 4.9. flow167 gen 150: 34.5 → 50.9 % (+20/−2), +3,391 a game, t 6.2. Different arms and sigmas, the same gain on 55 never-trained live boards. Both packages built; the drawn legs (veto) decide the order of hand-over.

## 42. flow166 gen 170 on live boards: mostly growth (2026-09-10) — see docs/strategy/2026-09-10-flow166-g170-live-anatomy.md

The +2.8k a game on the 55 live boards is 62 % our purse rising and 38 % the opponent's price falling; on the boards the live theta already won it is pure growth. The gain is broad (84 of 110 board-seats up) and comes from earlier hiring on days 5-9 and a late-season price advantage after day 19, with the same carrot/cow/fewer-sheep structure seen on the family. Sim and engine agree to ~125 coins per tape on these boards after the shed fix.

## 43. Head-to-head on the live boards (2026-09-10) — see docs/strategy/2026-09-10-flow167-g150-live-anatomy.md

The two live-passing candidates tie on win rate within one board of 55. flow167 gen 150 wins margin (+3,232 vs +2,761, t 5.9 vs 4.0), is growth-only (opponent purse +395 vs −1,052 for gen 170), and carries half the downside (worst five boards −17.6k vs −37.7k). Its edge is late-season sell timing (rows moved to hour 18, +3 coins a unit). Provisional upload choice: flow167 gen 150, pending both veto legs. Note: pinned seats are identical, so every "110-game" live read is 55 boards.

## 44. Herd-mix residual-drain tilt, drawn legs (2026-09-10)

On 2,592 drawn boards the tilt gains +332 a game (grouped t 2.2) but loses 1.2 points of win rate (48 boards up, 80 down). Not shippable on that read; a live-board read is chained to settle it. §23 stays open pending that.

## 45. flow172 gen 60 leads (2026-09-10)

Sixty generations past gen 170 on the fixed population with the corrected sim, judged automatically: on the 55 held-out live boards 34.5 → 58.2 % (14 flips, 1 drop), +4,834 a game at t 8.4, 47 of 53 positive; on the twenty fresh losses +5,181 at t 4.6. It supersedes both earlier candidates on every read. Package and equivalence in progress; drawn legs as veto next.

## 46. Win-first gate calibrated (2026-09-10) — see docs/strategy/2026-09-10-winfirst-calibration.md

Six net boards is cleared by noise 11-45 % of the time because near-loss boards flip under symmetric noise; a negative slack is inert. The gene arm now runs as flow177 with nine net boards and no negative family margin allowed.

## 47. The gene learned nothing in the full-theta arm (2026-09-10) — see docs/strategy/2026-09-10-gene-decode-flow168.md

After 54 generations the drain-mix gene block is indistinguishable from a random block of the same size on every decoded statistic. The arm now trains the gene alone (flow178, 264 parameters, win-first gate) from the gen-170 record, which is the only run that can say whether the residual-drain tilt pays.

## 48. flow166 gen 170 clears the veto (2026-09-10)

Six drawn legs: no pool significantly negative (pooled top10+today41 by board: 86.4 → 84.9 % wins, +355 a game, t 0.57; today41 alone −19 boards of 328 with margin level). Under the rule the candidate is promotable: live set +18 points, fresh losses +4.9k a game, drawn veto clear. Handed to the operator with flow172 gen 60 (stronger on every live read, veto legs in progress) as the alternative worth a short wait.

## 49. Drawn win-rate dips are a ceiling artefact (2026-09-10) — see docs/strategy/2026-09-10-drawn-vs-pinned.md

gen 170's today41 dip sits entirely on the twenty tapes the live theta already beats 8 of 8 on drawn towns; every contested bucket is level or up, and on pinned boards the base won it drops one in 45. Veto rule: a drawn win-rate dip does not veto when margin is level; score wins on contested tapes only and keep the margin floor.

## §50 flow172_g60 live anatomy: the gain is evening-sell price, 91 % own purse (2026-09-10)

Source: docs/strategy/2026-09-10-flow172-g60-live-anatomy.md (S/g172live/). Sim = engine on the 55 live boards (mean |sim−eng| 154 coins, W/L agreement 100 %, g60−g170 delta corr 0.992).

| pair | ALL | ours | theirs | growth share |
|---|---:|---:|---:|---:|
| g60 − init (110 seats) | +4,592 | +3,372 | −1,220 | 74 % |
| g60 − g170 | +1,825 | +1,652 | −173 | 91 % |

g60's opening, pump, land, quad count and d0-4 hires are identical to g170's; the single moving lever is sell timing (h1 rows 105.8 → 99.4, h18 rows 32.2 → 38.0, realised price/unit 92.38 → 93.47), which lands as d15-19 +1,145/game and nothing before d9. Three extra flips over g170, all growth; the inherited drop board 107117102 is half-repaired (−7,328 → −3,640). Tail risk is half g170's (worst-5 sum −22.6k vs −43.1k). Reading: g60 = g170 + a later-day sell mix, no new denial channel, cleaner downside; it is the better upload if its drawn veto clears.

## §51 Residual LOSS20 under g60: one cluster, the d10-11 melon pot (2026-09-10)

Source: docs/strategy/2026-09-10-residual-loss20.md. The 15 fresh-loss boards g60 still loses and the 5 it flips are the same board: one clone opening (7 WHEAT + 12 MELON, 2 COW + 2 SHEEP, 5 hires d0, 22 by d4), gap at d14 between +15.0k and +22.8k on all 20, final margin set by how fast we repay after d14 (corr −0.86 with the recovery, +0.06 with the d14 gap). The d10-14 revenue band is −22.7k, of which the d10-11 melon pot is about −15k (theirs 233 units at 143.8, ours 92 at 117; we hold no melon before d10 and sell 84 units from d18 at 220 falling to 113). MILK+WOOL −4k, FERTILIZER −3k. g60 − live on the 30 seats: +4,369 (t 4.6), 69 % own purse. Conclusion: d0-9 is already ours and d15-29 already repays 14k; the next gain has to come from d10-14 income, i.e. melon in the ground on d0, which is blocked by hire enumeration pricing hands on today's tasks (FORWARD_ADMIT, see docs/strategy/2026-09-09 forced-opening-ramp). Sim numbers descriptive; four tapes drift by ≤0.5k, none near a verdict.

## §52 Sell-hour headroom: none (2026-09-10)

Source: docs/strategy/2026-09-10-sell-hour-headroom.md. Sim on the pinned boards with flow172_g60 as base (122 board-seats): a later evening row (3,10,21) −165 (t −0.9), a fourth row (3,10,18,21) −77 (t −0.5), the turn-1 sale off −77 (t −0.8), no morning lot −10.1k (confounded, turn 3 carries BUY_LAND). The turn-1 sale that shipped at +2.2k is worth zero under g60: ES re-allocated units between the existing lots through hold/press rather than changing the layout, and that lever is spent. No per-product hour map exists in the planner. Sell-hour family closed; no engine read.

## §53 flow172_g170c live anatomy: a denial-only step with a doubled tail (2026-09-10)

Source: docs/strategy/2026-09-10-flow172-g170c-live-anatomy.md. Sim = engine on the 55 live boards (mean |diff| 171, W/L 100 %, delta corr 0.994).

| pair | ALL | ours | theirs |
|---|---:|---:|---:|
| g170c − live | +5,534 | +3,333 | −2,201 |
| g170c − g60 | +942 (t 3.5) | −39 | −981 |

Nothing structural moved between g60 and g170c (basket, pump, hires, d10 tiles identical). The step prices our basket 0.7 coins/unit cheaper (93.47 → 92.80) and takes about 1k off the opponent's revenue on identical opponent units; it opens d20-29 and lands in their purse. d10-14 did not move (+226), so the melon-pot residual (§51) is untouched. The tail doubles: worst-5 −36.5k vs −22.6k, 43/110 board-seats regress against g60, 107088554 at −19.6k. LOSS20 35 % vs 25 %: the extra flips are the boards with the smallest base gap. Reading: ship g170c (or g200, same flip set) for win rate; g60 remains the low-tail fallback; the next growth has to come from d10-14, i.e. FORWARD_ADMIT.

## §54 FORWARD_ADMIT: already existed, already declined by the ES, rebuilt anyway and dead (2026-09-10)

Source: docs/strategy/2026-09-10-forward-admit.md (branch fwd-admit, commit ba21fd4, not merged). arms-next already carries FORWARD_ADMIT_ON/FORWARD_ADMIT_DAYS and a trained horizon gene g11; the switch sweep (2026-09-09) had it at HELD42 −8,676 (t −12), and g11 on the base theta decodes to forward_days = 0 every day: the ES, free to hire ahead of melon maturity, chose not to and instead raised the crew target to 11 by day 10. A narrower rebuild (quiet tiles only, value discounted 1/(1+k), hooked only into the hire argmax) reads HELD42 −2,628 (t −8.0), LEG20 −1,456 (t −2.8), LOSS12 −6,403 (t −5.5), flips +0/−8; 76/76 tests pass with the knob off. Conclusion: the day-10 melon pot (§51) is not a hiring problem. Process lesson: search docs/strategy for the knob name before building; the archive already had the answer.

## §55 LIVE-B: the candidates hold on eleven boards nothing has touched (2026-09-11)

Source: docs/strategy/2026-09-10-liveb-leg.md and S/liveb/chain_summary.txt. Eleven Kaggle boards cut after the LIVE62/LOSS20 freeze, absent from every training rung, remote gate and local judge (loss-weighted: the live theta wins 1/11).

| theta | win | d-margin | SE | t | positive |
|---|---:|---:|---:|---:|---:|
| flow172_g170c | 9.1 → 81.8 % | +6,885 | 987 | 6.97 | 11/11 |
| flow172_g200 | 9.1 → 72.7 % | +6,448 | 969 | 6.65 | 11/11 |
| flow172_g60 | 9.1 → 63.6 % | +5,464 | 823 | 6.64 | 11/11 |

The ranking and the size match LIVE55 (g170c 65.5 %/+5,930, g200 65.5 %/+5,850, g60 58.2 %/+4,834) on boards no selection step ever saw. n=11 keeps it directional, but every board is positive for every candidate. This is the first out-of-sample confirmation of the flow172 lineage; the leg grows by ~5 boards per day of Kaggle play (cut by hand each firing).

## §56 The day-10 melon pot is reachable by the route model, and still not a win (2026-09-11)

Source: docs/strategy/2026-09-10-melon-route-capacity.md (sim, descriptive, board 107056463, theta flow172_g170c). With the forced melon opening plus mid-day placement, 66 of 72 units sell on the day (72 units / 12,537 on d10-11 against the clone's 72 / 17,440 at an average 233): harvest cadence, shed capacity, sell rows and hands are not binding; the deposit turn is (12 units banked before t16, 54 cleared in one line at t18 at 171 behind the clone's ladder), costing about 4.2k of timing. Even so the pot does not pay: the second dumper takes ~174 not 233, and every forced melon build in the archive loses 15-20k over d12-29 because the 12 tiles displace the animal and wheat denial that wins the late game. Conclusion: the residual is a tile-budget question (melon additive to the day-0 board), not routing or hiring; melon-as-swap stays closed.

## §57 The simulator tile-collision gate over-counts; no fidelity hole (2026-09-11)

Source: docs/strategy/2026-09-11-sim-tile-collision-gate.md. The release gate tests/test_gates.py::test_no_tile_write_collisions fails in the shipped tree (7 hits over 60 trials; 8 with the bank switch). All hits come from TAIL_CARE_ON's care hop, which deliberately relaxes the tiles-no-block-holds rule, and every hit pairs two distinct animal operations on one animal tile. Those write disjoint arrays in the sim and the engine guards each with its own day flag, so order cannot change the outcome; the parallel and sequential applications agree on every field, and 400 trials show no same-op or non-animal collision. Verdict: gate definition problem, not a fidelity hole. Fix the gate to assert per written array; nothing blocks the packages.

## §58 Additive melon: no knob, and the purse arithmetic says no (2026-09-11)

Source: docs/strategy/2026-09-11-additive-melon.md. The planner cannot express "one extra quad on day 0, all melon, basket unchanged": the melon opening preserves the plant-target sum by construction (a swap), land purchase has no switch and its bias is a gene. Land cadence: the clone buys on d6 and d11 on all five inspected fresh-loss tapes, plants 19 tiles on d0 and ends the day with about 50 coins; we buy on d5 and d10, leave no empty tile on d0 and spend the purse down to 145. An additive quad plus 12 melon seeds costs about 1,960 out of a fully spent 3,000 against a pot worth about 12.5k at the second dumper's price, before the displacement of hands and water. Build spec recorded, not built. With §51, §54 and §56 this closes the melon family in all three forms; the day-10-14 gap is the price of the day-0 basket the ES chose.

*§55 addendum (13 boards, 2026-09-11 02:20Z):* g170c 76.9 % / +6,563 (13/13), g170c+pair 76.9 % / +6,486, g200 61.5 % / +5,876, g60 53.8 % / +4,854 (12/13), g60+pair 46.2 % / +5,070 (13/13). The aggressive file leads the safe one by four boards out of sample; the pair is neutral at this n.

## §59 Against the pinned top ten the candidates gain 5-6k and still lose two games in three (2026-09-11)

Source: S/top20 (the 20 pinned top-ten tapes of docs/strategy/2026-09-09-top10-vs-clone.md on their real towns, base flow135_g350 wins 20 %).

| candidate | win | d-margin | SE | t | positive |
|---|---:|---:|---:|---:|---:|
| g60 + pair | 20 → 35.0 % | +5,424 | 1,120 | 4.84 | 18/20 |
| g170c + pair | 20 → 30.0 % | +6,067 | 1,112 | 5.46 | 18/20 |
| g170c | 20 → 25.0 % | +5,537 | 1,135 | 4.88 | 17/20 |
| g60 | 20 → 27.5 % | +4,528 | 1,130 | 4.01 | 17/20 |

The margin gain against the top tier is the same size as against the 2000 band, the pair adds three to four top-ten boards on either theta, and the two lead files are level within noise. But every candidate still loses 65-70 % of top-ten games: the day-10 melon dump (§51, §56, §58) is the wall, and it is not reachable by any planner lever tried. The rating ceiling of these files is therefore below the top ten; the path to 2880 is the ES lineage continuing to move (flow172 records, flow179, the pair-on flow180).

*Caveat (02:55Z):* all 20 TOP20 tapes are flow172 training rungs (none in its gate), so this read is in-sample for g60/g170c; trained on them, the candidates still lose two in three.

*§55 addendum (17 boards, 03:55Z):* g170c 70.6 % / +7,482, g170c+pair 70.6 % / +7,417, g200 58.8 % / +6,816, g60 52.9 % / +5,591, g60+pair 47.1 % / +6,164; all 17/17 positive except g60 16/17. Ranking unchanged at every size.

## §60 TOPB, the held-out top-tier leg: half of the top-ten edge was training-set fit (2026-09-11)

Source: docs/strategy/2026-09-11-topb-leg.md. Twenty fresh pinned tapes (two per current top-ten team, 2921-3001, all cut byte-exact, in no training, gate or judge list; base flow135_g350 wins 25 %).

| candidate | win | d-margin | t | positive | TOP20 (in-sample) |
|---|---:|---:|---:|---:|---|
| g60 + pair | 25 → 35 % | +2,890 | 1.87 | 15/20 | +5,424, t 4.84 |
| g170c + pair | 25 → 30 % | +3,174 | 1.92 | 12/20 | +6,067, t 5.46 |

Direction agrees with the in-sample read, magnitude halves and neither candidate clears |t| ≥ 2. About half of the measured top-tier edge was fit to the training tapes. Both lose the same two boards (SpaTaro 107247899, binghua 107246553). TOP20 is a training diagnostic from here on; TOPB is the top-tier judge and grows with each fresh cut. The wall stands at 30-35 % against the top ten.

*§60 addendum (thetas alone):* g170c 35 % / +2,692 (t 1.8, 13/20), g200 20 % / +1,868 (t 1.2, +2/−4), g60 35 % / +2,628 (t 1.7, 16/20). g200 drops top-tier boards; it does not displace g170c.

## §61 g200's top-tier dip is noise, but the lineage's denial does not reach the top tier (2026-09-11)

Source: docs/strategy/2026-09-11-g200-top-tier-drift.md. On the twenty held-out top-tier boards g200 − g170c is −824 (SE 729, t −1.1), −185 without one board; the win-count collapse from 35 % to 20 % is three boards, two of them ties that flipped on margins under 1.1k, one real loss to SpaTaro (−13k in our purse from a mid-game mix shift out of melon and wool). Nothing moves before day 10. The lineage-wide finding: against the band the flow172 line takes about 2.2k off the opponent, against the top tier it hands them 0.8-1.1k, already at g60, so the held-out band margin overstates the top-tier margin roughly twofold. Rule: judge successors on the TOPB paired margin, never on its win count at n=20.

## §62 flow172_g300 anatomy: growth again, and the tail closes (2026-09-11)

Source: docs/strategy/2026-09-11-flow172-g300-live-anatomy.md. Sim = engine on the live boards (mean |diff| 200, W/L 100 %, delta corr 0.98). g300 − g170c on LIVE55 is +433 = +312 ours / −121 theirs, 72 % growth, concentrated on the loss boards (+876); on the held-out top tier +474 = +420/−53, though the lineage still hands the top tier about +0.9k (§61). Nothing structural moved: an egg and fertiliser tilt with three more late sell rows at price/unit 92.80 → 91.92; the step lands in d15-19 and d10-14 stays untouched. The tail that g170c had doubled closes: 107088554 −19.6k → −9.8k, worst-5 −21.6k against −36.5k. LOSS20 flips 8, the boards g170c left within |2.1k|. Verdict: ship g300 + pair, best or tied-best on all four judges (LIVE55 70.9 % / +6,753, LIVE-B 76.5 % / +8,119, TOPB +3,730 t 2.12, LOSS20 40 %) with half the tail; the step over g170c is itself below the live noise floor (t 0.56) but sign-consistent on every leg.

*§55 addendum (22 boards, 07:30Z):* g300+pair 72.7 % / +7,808 (22/22), g300 68.2 % / +7,718, g170c+pair 63.6 % / +7,202, g170c 63.6 % / +7,236, g200 54.5 % / +6,819, g60+pair 45.5 % / +5,842, g60 50.0 % / +5,404. Ranking unchanged; g300 on top.

## §63 The gate overlap does not inflate LIVE55 (2026-09-11)

Source: docs/strategy/2026-09-11-live55-overlap-bias.md. flow172's gate family contains 12 of the 55 held-out live boards. For all eight candidates those 12 boards score lower than the other 43 (pooled gate-minus-clean −562, SE 188, t −3.0), so the overlap deflates rather than inflates the read. Clean 43-board lines: g300 + pair 44.2 → 79.1 %, +6,630 (t 9.4, 38/43); g60 + pair 44.2 → 73.3 %, +5,227 (t 7.9, 38/43). The LIVE55 headline for the lineage stands.

## §64 How the lineage hands the top tier money: late wool and melon abstention (2026-09-11)

Source: docs/strategy/2026-09-11-top-tier-transfer.md (sim on the 20 held-out top-tier tapes, opponent purse reproduced to ~70 coins). The +848 the top-tier opponent gains under g300 versus the live theta is entirely price: their units, hands, quads and herd do not move, price per unit rises 0.53, and the whole gain opens in d20-29, where the top tier sells 43 % of its volume. Channels: wool abstention +1,454 (we sell 7.8 fewer units and their late wool quote rises 15; the top tier sells 41 % more wool than the band), melon abstention +551; our milk denial takes only −2,034 from them against −3,092 from the band, whose milk market is less flooded. Against the top tier the lineage's gift half doubles and its denial half shrinks. A top-tier-weighted fitness (flow181) can price the abstention but cannot separate gift from denial on a shared price curve; the opponent-supply switch that would target it is already dead on the band (§: opp-supply live read).
