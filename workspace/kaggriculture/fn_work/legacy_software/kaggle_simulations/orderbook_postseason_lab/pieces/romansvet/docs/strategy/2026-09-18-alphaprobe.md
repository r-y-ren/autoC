# ALPHAPROBE — the ALPHAFARM first falsifier: dawn-by-dawn Macro search PASSES the bar

2026-09-18, branch `alphafarm`, tasks 1-2 of [[alphafarm]] §6. Read with [[mpcfeas]], [[planselect]], [[esjudge9]],
[[goalaudit]]. Tool `S/alphafarm/search_probe.py`, rows `S/alphafarm/run12_*.tsv`.

## 1. Method
Board = `(pinned-town action tape, engine seed rung, seat)` — `S/simscreen/screen.py`'s board, the tape seat being
the engine it was cut from. Per board: S=4 **selection** shop/weed streams plus one **held-out** stream never used
in a selection (episodes start byte-identical, [[mpcfeas]], so the stream is the whole board randomness). Dawns run
sequentially d = 0..29 — sample K=8 candidate Macros as integer jitter around the one the policy emits (candidate 0
= its own macro, zero jitter), roll each to game end on every selection stream with the same theta continuing and
the same tape, score two-purse `ours − theirs` averaged over the 4, commit the argmax, advance every stream one day
with the committed macro injected on day d. **Chain A (search)** selects on the 4 streams and is evaluated on the
held-out one; **chain B (oracle)** selects on the held-out stream itself (the hindsight bound); **baseline** = the
pure policy on that stream and tape.

Mechanics, all inside the shipped sim. Resume-from-dawn is `rollout.run_day` in a `lax.scan` whose body is
`lax.cond(d >= d_start, run, identity)` with `d_start` **unbatched** — the predicate is then unbatched, the cond
stays a real branch under `vmap`, skipped days cost nothing and the 30-day program compiles ONCE (~350 s on CPU, the
whole fixed cost). The candidate reaches `brain.decide` through a **tail appended to our seat's theta row**
(`PO.unpack` slices fixed offsets, so the tail is invisible to the policy) plus a `decide` wrapper applying the
jitter when `obs.day == d_inject` on our seat only — the design's fallback channel, per seat and correctly batched.
Jitter (script docstring for the units): one component of `plant_target`/`animal_want`/`grow_mult`, or
`crew_target`/`hire_bias`/`land_bias`, `fert_defer` skipped as a DEAD gene [[planner4]]; centre theta = the shipped
`theta.npy` (6,789) zero-padded to `N_PARAMS` 7,659, judgekit switch string. **CORRECTNESS TEST, run first:** K=1,
zero jitter, 2 boards — the committed trajectory must reproduce the pure-policy one. **PASS, to the coin**;
injection, resume and advance add nothing of their own.

## 2. Boards, cost, result — held-out stream, paired against the pure policy
12 boards, **6 + 6**, not the designed 24: the run is 32.5 min of local CPU (5.4 eps/s measured, 7,600 eq-episodes)
and a second batch would have paid the compile again outside the time box. Engine six = the six most negative
`cesr_topleg2/3` boards (the gated engine-class loss tail, the [[goalaudit]] target); band six = the first six
BAND250 tapes of `S/lossflip/cf3_esr_band250.csv`.

| set | n | Δmargin | se | t | Δours | Δtheirs | oracle Δ | up |
|---|---|---|---|---|---|---|---|---|
| engine loss tail | 6 | **+3,997** | 629 | 6.35 | +3,213 | −784 | +3,907 | 6/6 |
| BAND250 | 6 | **+1,827** | 380 | 4.81 | +2,122 | +294 | +1,624 | 6/6 |
| **POOLED** | 12 | **+2,912** | 479 | **6.07** | +2,667 | **−245** | **+2,766** | **12/12** |

Candidate 0 is committed **72.5 %** of dawns. In-sample dawn gain 95 coins → 2,849/board, within noise of the
realised +2,912: dawn gains are **additive and do not shrink out of sample**. Candidate spread at a dawn (sd over
the 8 candidates of the 4-stream mean) 264 coins → per-candidate se ≈ 132, meeting the design's §4 rule (se < 300);
CRN earns its price.

## 3. Verdict — **PASS, and the lottery signature is absent**
Bar (pre-registered, [[alphafarm]] §5): pooled Δmargin ≥ +1,000/board, Δtheirs ≤ 0, t ≥ 3. Read: **+2,912, Δtheirs
−245, t 6.07**, 12/12 boards positive — every term clears. The decisive line is the oracle. MPCFEAS and PLANSELECT
died of a large oracle with a zero held-out read (argmax agreement 0.20 vs chance 0.25); here the **oracle is +2,766
against the held-out +2,912** — hindsight buys *nothing*, and the two chains correlate 0.988 across boards. The gain
is a property of the board, not of the shop draw: exactly the test those families failed. The searched object is
still the `Macro` [[esjudge9]] closed — what is new is not the action space but that improvement is **measured per
dawn against a CRN-paired continuation**, not as one scalar per theta.

Caveats: (a) the tape opponent cannot react, so part of the engine tail's −784 Δtheirs is denial a live seat might
answer; (b) **BAND250 Δtheirs is +294** — the clone class gifts under search, so distillation must keep the design's
"drop any label with `d_theirs > 0`" rule, not the pooled sign; (c) 12 boards, one theta, no distillation: this
prices the *search*, not a theta. Pricing — haircut 30-60 % and "a gain under +2,000 cannot fund a +1,000 ship", so
+2,912 gives **+870…+1,750**, above the §115b +450 bar with room. **GO on tasks 3-4** (`soft_decide.py`,
`ei_train.py`); cheap next reads are the other 12 boards and K=16.
