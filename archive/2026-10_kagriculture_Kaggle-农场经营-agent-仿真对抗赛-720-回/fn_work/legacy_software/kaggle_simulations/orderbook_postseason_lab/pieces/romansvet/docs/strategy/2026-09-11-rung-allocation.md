# Rung allocation audit — what flow209 / flow210 actually optimise (2026-09-12)

**Question.** `docs/strategy/2026-09-11-g10-decode-diff.md` §3 and `S/shopcrn/census.md`
report 178 episodes/generation = 166 pinned-town action tapes × 1 episode + 6 `_pool`
+ 6 `_theta`, with the four archetypes drawing **zero** episodes despite
`arch_frac 0.9` in `~/stage_hr/artifacts/flow209/config.json`. Defect or design?

**VERDICT: (c) — a config override in `S/flow209/launch_flow209.sh`, and the intended
one.** Line 186 of the launcher passes
`--rung-weight expander=0 --rung-weight rusher=0 --rung-weight rancher=0
--rung-weight patient_grower=0`; the four archetypes are the *only* unpinned rungs on
the ladder, so after `--pinned-once` drops the 166 pinned rungs from the residual
allocation the residual weight vector is all-zero and the trainer takes its documented
"every rung is pinned → the residual is self-play" branch. `arch_frac 0.9` is *inert*
under this configuration: it is never read. This is not a rounding or ordering defect,
and it is not the 2026-09-05 `--arch-frac 0.0` incident (§5). No fix is required.

All line numbers are the training tree
`/mnt/e/_work/kaggriculture3/.claude/worktrees/arms-next` (read-only for this audit).

---

## 1. The allocation order, rule by rule

| # | rule | file:line | what it does for flow209 |
|---|---|---|---|
| 1 | tape rungs are appended to the **archetype ladder** | `scripts/train.py:2370-2394`, `src/kagg3/es/train.py:3756-3762` | ladder = 4 archetypes + 166 `tape_act_*` = **170 rungs** (`train.log`: `rungs=170`) |
| 2 | a tape with a recorded town becomes a **pinned** rung | `src/kagg3/es/train.py:3764-3766` | all 166 `artifacts/tape_actions_town/*.npz` carry a town → `pinned_slots` = 166 (`train.log`: `pinned-fixed-seed: 166 pinned rung(s)`) |
| 3 | `--rung-weight` → `rung_weights`, default 1.0; refuses only if **every** rung is 0 | `src/kagg3/es/train.py:3767-3779` | 4 archetypes @0, 85 tapes @2, 61 tapes @4, 20 tapes @10.2 |
| 4 | **pinned block first**, one episode per pinned rung, never truncated | `src/kagg3/es/train.py:4413-4429` (`pinned_block`), `:4924-4941` | 166 slots lead the layout |
| 5 | **residual pairs = `max((episodes − n_pinned) // 2, 1)`** | `src/kagg3/es/train.py:4926` | `(179 − 166) // 2 = 6` pairs |
| 6 | episodes actually played = `n_pinned + 2 × residual_pairs` | `src/kagg3/es/train.py:4432-4443` (`pinned_keep`) | 166 + 12 = **178** of the 179 budgeted (§4) |
| 7 | the residual is allocated with the pinned rungs at **weight 0** (`drop`) | `src/kagg3/es/train.py:4522-4546` | `wv` = weights with the 166 zeroed; the 4 archetypes are already 0 → `wv.sum() == 0` |
| 8 | **all-zero residual weights → `arch_frac` is replaced by 0.0** | `src/kagg3/es/train.py:4547-4551` | `arch_frac 0.9` never reaches `arch_pairs`; this is the branch that fires |
| 9 | `k = arch_pairs(n_pairs, n_arch, arch_frac)` = archetype pairs | `src/kagg3/es/train.py:703-711`, `:829` | `round(0.0 × 6) = 0` → **zero archetype episodes** |
| 10 | everything not archetype rotates over `pool + [theta]` | `src/kagg3/es/train.py:853-858` | `j = arange(6) % (n_pool+1)`; at `pool 1` → 3 pairs vs `pool[0]`, 3 pairs vs `theta` = 6 + 6 episodes |
| 11 | per-episode fitness weight = `2 × rung weight` on the pinned block, 1.0 elsewhere | `src/kagg3/es/train.py:4478-4491` (`pinned_weights`), `EPISODES_PER_PAIR = 2` at `:555` | see the table in §2 |
| 12 | seat of each pinned board alternates per generation, staggered by position | `src/kagg3/es/train.py:4445-4476` (`pinned_seats`) | every pinned board is seen from both seats on consecutive generations |
| 13 | slot rotation (`--slot-rotation carry`) | `src/kagg3/es/train.py:714-781`, `:4555-4562` | **not reached**: it only allocates the archetype block, which is empty here |

Summary of the order: **pinned tapes first at a fixed 1 episode each (weight-independent),
then the leftover budget is halved into pairs, then the archetype/drawn-tape block takes
`round(arch_frac × pairs)` of those pairs weighted by `--rung-weight`, then self-play
absorbs the rest.** With 166 of 170 rungs pinned and the remaining 4 at weight 0, steps
8-10 collapse the whole residual onto self-play.

Cross-check, remote `~/stage_hr/artifacts/flow209/train.log`:

```
pinned-once: 166 pinned rungs x 1 episode + 13 episodes carried
WARNING: --pinned-once leaves 13 episodes for 4 unpinned rung(s) and self-play, ...
fitness-manifest: ... rungs=170  tape_score=margin
gen 1 ... pool 1  rungs 166/170 ...
```

`rungs 166/170` (`scripts/train.py:3123-3127` counts rungs with a non-zero episode
count) — **the 4 missing of 170 are exactly `expander`, `rusher`, `rancher`,
`patient_grower`**, the four archetypes, confirmed by the warning line ("4 unpinned
rung(s)") and by the weight override in the launcher/config.

## 2. The objective, in one table

Per generation, per candidate (`--pop 4096` candidates all play the same row — CRN).

| rung family | rungs | episodes/gen | per-episode weight | weight total | share of objective | opponent rating band | shop |
|---|---:|---:|---:|---:|---:|---|---|
| pinned tapes `--rung-weight 2` (old loss-tape band + 09-05 top-tier cut) | 85 | 85 | 4.0 | 340.0 | **27.24 %** | ~1900-2100 (rated w2 median 1998, p10 1704 / p90 2186; the <1900 tail was dropped at flow187) | PINNED town |
| pinned tapes `w4` — LIVE-C band boards (`S/livec/ids.txt` 1-42) | 42 | 42 | 8.0 | 336.0 | **26.92 %** | 2300-2615, mean opponent 2457 | PINNED town |
| pinned tapes `w4` — LOSS10 (`S/bloss/loss_ids.txt`) | 10 | 10 | 8.0 | 80.0 | **6.41 %** | 2175-2381 | PINNED town |
| pinned tapes `w4` — top-50 new-template (`S/top50/train_ids_patterns.txt`) | 9 | 9 | 8.0 | 72.0 | **5.77 %** | top-50 tier (~2700+) | PINNED town |
| pinned tapes `--rung-weight 10.2` — top-ten | 20 | 20 | 20.4 | 408.0 | **32.69 %** | 2821-2954 (the 09-09 top-ten cut) | PINNED town |
| self-play `_pool` (the frozen `--init-theta` anchor) | 1 | 6 | 1.0 | 6.0 | **0.48 %** | our own seed theta | DRAWN |
| self-play `_theta` (the current, un-perturbed centre) | 1 | 6 | 1.0 | 6.0 | **0.48 %** | our own centre | DRAWN |
| archetypes (`expander`, `rusher`, `rancher`, `patient_grower`) | 4 | **0** | — | 0.0 | **0 %** | hand-written, no rating | — |
| **total** | **170** | **178** | | **1248.0** | **100 %** | | |

`340 + 336 + 80 + 72 + 408 + 12 = 1248`; pinned share `1236/1248 = 99.04 %`, drawn
`12/1248 = 0.96 %` — reproduces `S/shopcrn/census.md` exactly.

Family composition verified by set intersection against `S/livec/ids.txt` (first 42),
`S/bloss/loss_ids.txt` and `S/top50/train_ids_patterns.txt`: the 61 `w4` rungs are
42 + 10 + 9 with **no overlap and no remainder**. Rating bands are quoted from
`docs/strategy/2026-09-10-rung-strength-A.md` §1 (Kaggle `initialScore` at the taped
game), `S/livec/provenance.txt`, `S/express/census_band.md` and the LOSS10 anatomy
(memory `LOSS10: no counter class`).

**The six self-play episodes are against neither the champion nor the population.**
`candidates() = pool + archetypes + [theta]` (`src/kagg3/es/train.py:4409-4411`): the
`_theta` opponent is the **current un-perturbed centre** θ_t, and at `pool 1` the
`_pool` opponent is `pool[0]` = the theta loaded by `--init-theta`
(`artifacts/kagg2_games/thetas/flow193_g100_hr.npy` = candidate B for flow209; the hr
seed for flow210), frozen at construction (`:3605`) and protected from eviction
(`_snapshot`, `:5838-5844`). `champion.npy` / `best_abs.npy` are selection records and
are never opponents. The split moves once snapshots start landing
(`pool_every 100`): at pool 12, `j = arange(6) % 13` puts all six pairs on pool members
and `_theta` reads 0 — the family total stays 12 episodes / 0.96 % either way.

**So the objective is:** a per-episode-weighted margin score
(`fitness-manifest: abs_weight=0, margin_scale=3000, tape_score=margin`) over 166 fixed,
deterministic pinned-town boards played once each per generation with alternating seats,
plus a 1 %-weight self-play tail against our own seed and centre. It is, to 99 %, a
**fixed 166-board supervised objective**, not a self-play objective.

## 3. Why zero archetype episodes is (c) and not (a) or (b)

* **(c) config override — YES.** `S/flow209/launch_flow209.sh:186` zeroes all four
  archetypes; `config.json` `rung_weight[0:4] = ["expander=0","rusher=0","rancher=0",
  "patient_grower=0"]`. This alone produces the zero, through step 8's all-zero branch.
* **(a) "the consequence of `--pinned-once` with 166 tapes at weights past the budget" —
  NO.** `--pinned-once` gives every pinned rung exactly one episode *regardless of
  weight* (`pinned_block` docstring, `:4419-4429`); weights enter only the fitness mean.
  The pinned block cannot crowd the archetypes out by weight. It crowds them out by
  *count* only in the sense that 166 of 179 episodes are spoken for — and the remaining
  6 pairs would still have gone 5-to-the-archetypes (`round(0.9 × 6) = 5`, i.e. **10 of
  the 12 residual episodes**) had the four not been weighted 0.
* **(b) rounding/ordering defect — NO** for the archetypes. The one genuine rounding
  artefact is separate and immaterial (§4).

## 4. The one real (cosmetic) rounding artefact

`src/kagg3/es/train.py:4926` floors: `(179 − 166) // 2 = 6` pairs = 12 episodes, so
**178 of the configured 179 episodes are played**, while the startup banner
(`scripts/train.py:186-188`) announces "13 episodes carried". One-line fix if ever
wanted: `n_pairs = max(-(-(cfg.episodes - len(pin)) // 2), 1)` (ceil).
**Material? NO.** It moves the residual from 12 to 14 episodes: drawn weight share
`12/1248 = 0.96 %` → `14/1250 = 1.12 %`, pinned `99.04 % → 98.88 %`. A 0.16-point shift
in a family that carries under 1 % of the objective; the gradient is unchanged for
practical purposes. Not worth restarting an arm for; it belongs in the next recipe if
anything.

## 5. History check — the 2026-09-05 `--arch-frac 0.0` incident is a different failure

`docs/strategy/2026-09-05-build-story.md:453-461` and
`docs/strategy/2026-09-08-how-we-built-the-agent.md:190-194`: flow123-flow127 ran with
`--arch-frac 0.0`, which zeroes the **entire archetype block — and the tape rungs live
inside that block** — so those five runs were 100 % self-play and their tape verdicts
were void. The remedy adopted at flow128/flow129 was precisely *"`--arch-frac 0.9`, the
four archetypes weighted 0"* (`how-we-built-the-agent.md:213` and its knob table at
`:329`). flow209/flow210 inherit that line unchanged.

Two things have changed since, and both keep the histories consistent:

1. Under `--pinned-once` (in every arm since flow16x) the tape rungs no longer depend on
   `arch_frac` at all — they have their own block ahead of the pair layout. `arch_frac`
   now governs only the 6 residual pairs, and with the archetypes at 0 it governs
   nothing. The flow123-127 failure mode (**tapes** starved) cannot recur here: the log
   line `rungs 166/170` shows all 166 tapes played every generation.
2. The guard written after that incident, `Trainer.tape_slot_complaint`
   (`src/kagg3/es/train.py:4597-4633`, surfaced by `scripts/train.py` and enforceable
   with `--require-tape-slots`), fires only when `arch_frac ≤ 0` **or** every *tape* rung
   is weight 0. flow209 trips neither, correctly: it is silent because no tape is
   starved. `require_tape_slots: false` in the config is therefore not masking anything.

The memory line *"--arch-frac 0.0 gave tape rungs ZERO slots (flow123-127 = self-play)"*
stands, and does **not** apply to flow209/flow210.

## 6. Verdict

**Intended (c).** The four archetypes are deliberately weighted 0 in the launcher and
have been since flow128; `arch_frac 0.9` is dead configuration under `--pinned-once` with
an all-pinned ladder and should be read as inherited boilerplate, not as a broken
promise. The objective the two live arms optimise is 99.04 % 166 fixed pinned boards
(27.2 % ~1900-2100 / 26.9 % 2300-2615 LIVE-C / 6.4 % LOSS10 2175-2381 / 5.8 % top-50 /
32.7 % top-ten 2821-2954) and 0.96 % self-play against our own seed and centre.
No fix required.
