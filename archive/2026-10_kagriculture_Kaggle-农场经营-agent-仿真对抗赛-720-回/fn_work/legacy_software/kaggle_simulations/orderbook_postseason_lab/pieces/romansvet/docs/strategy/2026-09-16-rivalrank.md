# RIVALRANK — the rival's real sales rank our row, in both directions, for nothing

2026-09-16 13:39–14:25Z, worktree `/mnt/e/_work/kaggriculture3-rivalrank`, branch `rivalrank`
off master `b86b4c4`. `2026-09-16-slotmirror.md` §6 item 1 — the one live direction that doc left
open — and `2026-09-16-rivaltell-arm.md` §5 item 3's own instruction: read a **burst**, not a
rate, and feed the **ranking**, not the batch. Built, instrumented, **REJECTED at the ENG22 kill
gate in both signs**. No POOLED180, no upload. Numbers: `S/rivalrank/results.md`.

## 1. VERDICT

Bar: ≥ +100 and t ≥ 2 on the increment over the shipped pair, on ENG22 *and* V45LEG.

| arm | ENG22 (44 games) | V45LEG (60 clone games) | §115b |
|---|---:|---:|---|
| `SIGN=-1, W=1` (yield) | **−19** (t −1.57) | **+35** (t +2.33) | REJECT |
| `SIGN=+1, W=1` (front-run) | **+2** (t +1.01) | **−32** (t −3.00) | REJECT |
| `SIGN=-1, W=4` / `SIGN=+1, W=4` | **−51** (t −2.82) / **+4** (t +1.04) | **+0** (t +0.01) / **−40** (t −3.63) | REJECT |

Nothing reaches a fifth of the kill bar or a twentieth of §115b's +450, so POOLED180 (169
boards) was never cut. **The two legs disagree on the sign**: the clone tapes
want the dumped item demoted (+35, t 2.33) and the fertilizer-engine class wants it promoted
(+2, +4, t ≈ 1). A lever whose sign is a property of the opponent population, at a size of 40
coins, is noise wearing a mechanism's coat — and at `W=4`, where the measured term dominates
the proxy outright and **0 of 60** V45LEG games stay coin-identical, it pays **+0.5**.

## 2. WHAT WAS BUILT

`SELL_SLOT_RIVALRANK_ON`, default OFF (`plan.py:4362`, doc block `:4306-4361`). The batch term
is untouched; the switch adds **one term to the key `sell_slot_perm` sorts**:

    rank[p]  = sum_{j < q[p]} price(p, inv[p] + j) - price(p, inv[p] + burst[p] + j)
    score[p] = sell_slot_scores[p] + SIGN * W * rank[p]

`burst[p]` is `agent/tell.py::RivalTell.burst()` — the rival's **largest single-turn net sale**
of the last `RIVAL_TELL_WINDOW = 6` turns, gated at one turn with a credited sale (a maximum
needs no second sample; the rate arm needed two), WHEAT and FERTILIZER never gated
(`RIVAL_TELL_SKIP`: the net is signed there). The burst and not the mean because our slot index
only decides who reaches the shared inventory first **inside one turn's slot round**, and a
rival puts at most one turn's orders into that round.

`+1` FRONT-RUNS the item the rival is dumping, `-1` YIELDS it. The row is then shifted by a
uniform per-row constant, invisible to the sort, so every live slot keeps a non-negative key and
stays ahead of `sell_slot_perm`'s empty slots.

Plumbing, inert by default: `DayView.opp_burst` (`plan.py:5422`, all-zero `_NO_BURST`),
`parse_view(..., opp_burst=None)`, `agent/runtime.py` building the one `RivalTell` per seat when
either tell switch is armed. Branch `rivaltell` (`9bb5173`) is merged whole, `RIVAL_TELL_ON` OFF.

**14 tests** (`tests/test_rivalrank.py`) plus `test_slotprio` / `test_slotmirror` /
`test_rivaltell`'s 36, all green. The pin that matters —
`test_off_plan_is_byte_identical_to_master`: ten whole-plan sha256 digests (five boards × two
reservations) against a pristine `git archive b86b4c4 src` tree in a subprocess, `kagg3`
imported before the helpers so it cannot compare the tree with itself. **Equal**, as is
`test_an_armed_seat_with_no_measurement_is_the_slotprio_plan`. (Master has since advanced to
`4c6565b` with `fertreserve`'s own OFF switch; the pin is this branch's branch point.)

**The simulator is blind to this switch** (`rivaltell-arm.md` §2): `sim/rollout` has no per-turn
pot history, so a sim burst is all-zero and an ON sim run *is* the SLOTPRIO run — hence an
**engine** kill gate and not `S/simscreen`.

## 3. THE INSTRUMENT — the sign, measured (`S/rivalrank/instrument.py`)

Five real ENG22 boards, 10 seat-games, `sell_slot_scores` and `sell_slot_rivalrank` wrapped in
Five real ENG22 boards, `sell_slot_scores` and `sell_slot_rivalrank` wrapped in the parent
before the eval pool forks so every worker records: 300 dawns, 528 SELL rows, 1,401 live slots.

* **The tell fires four times as often as the rate arm did.** 0.83 items a dawn against 0.212
  (`rivaltell-arm.md` §1), 44 % of dawns firing at all against 18.6 %, and the burst clears the
  proxy's floor of 8 on **23.2 %** of fires (mean 5.04, max 24) where the *rate* cleared it on
  0.0 % — the burst is a live quantity in a way the mean never was.
* **And the proxy already over-pays the item the rival is dumping.** On the 236 fired slots the
  proxy scores **162.7** coins of contention and the measurement says **63.1** — delta **−99.6**,
  positive on only **4.7 %** of them. Against unfired slots (proxy 77.2, measured 0.0) the
  instrument's rule gives **SIGN = −1, YIELD**: the dumped item belongs later.
* **The row barely moves at W=1**: 3.2 % of rows re-order under `+1`, 8.1 % under `-1`, because
  with 2.65 live products a row a 63-coin correction rarely overturns a pair. `W=4` is the same
  arm with that objection removed.

The instrument's sign is the one V45LEG likes (+35) and the one ENG22 dislikes (−19); `W=4` then
removed the "too small to move" defence and the answer stayed zero. Both readings of the shelf
were arguable in advance — measured contention is real, or a dumped item's shelf is already deep
and its curve flat — and the engine says neither is worth 100 coins anywhere.
## 4. WHAT THIS CLOSES

1. **`slotmirror` §6 item 1 is answered and negative.** All three rival models a slot rank can
   stand on are now measured: the proxy board read (`opp_ripe`, +459, shipped), the exact
   self-mirror (−23 / −60), and the exact measured row here (±40, opponent-dependent sign).
   **The sell-slot rival-model family is closed.**
2. `agent/tell.py` is still exact and free, but **neither of its two readings pays inside
   `SELL_SLOT_PRIORITY`**: the mean dies under the batch clamp, the burst dies in the rank. Its
   next user should feed something that is not a nine-slot permutation of a three-row day.
3. `2026-09-16-slotprio.md` §6 item 2 (the other 21 turns) is the sell-row family's only live
   hole left, and `spread6` already closed "just add rows" once.
