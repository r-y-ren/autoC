# 2026-09-14 — mid-game herd growth (d3-d11): screen, ledger, reachability

**Sim, descriptive, paired, CRN. No engine game, no training arm, no `src/` edit.**
68 pinned-town boards (40 TOPB2 `S/simscreen/boards_topb2.json` + 28 LIVE-C
`S/simscreen/boards.json`, frozen in `S/melon_decomp/boards.json`), theta B =
`artifacts/kagg2_games/thetas/flow193_g100_hr.npy`, shipped `hr` switches, action-replay
opponent seat. Tools `S/herd/{mk_off,ledger,report,validate,reach}.py`; raw
`S/herd/raw_<arm>.npz`; full tables `S/herd/report_all.md`.

**Question.** `2026-09-11-integer-search.md` §2 moved `animal_want` only on
**d0-d2** and found B a local optimum there; the mid-game window d3-d12, funded by
the d5-d10 wheat cash, was never screened, and the `LOSS10` memory left
"fertilizer −7.3k/game with more cows" open. `2026-09-14-melon-decomposition.md`
made B's animal line a price-denial asset worth +21,156 to the opponent when melon
shrinks it; the top-five residual is FERT −11,322 / MILK −7,326
(`2026-09-14-episode-108806196-close-loss.md` §5).

## 0. Tool and identity gate

The arm is an additive per-day offset on B's **own decoded** `animal_want`, not a
plate: `KAGG3_OFF_INTS` (`/root/wt_isearch/src/kagg3/core/brain.py:968-1020`, the
`S/isearch` §0 extension; that worktree = `arms-next` 45f8217 + that extension only,
`plan.py` byte-identical to the repo's), each arm's edit at **variant 0** so the
shipped theta reads it with no variant tail. The two-seat ledger is
`S/melon_decomp/ledger.py` re-pointed there (`S/herd/ledger.py`, two changed lines).

**Identity: `base` (all-zero table, wt_isearch) reproduces melon-decomposition arm B
(arms-next, no offset machinery) with max |Δ| = 0 on all 14 recorded arrays and 0
coins of margin on all 68 boards** (`S/herd/validate.py`); base win 42.6 %, margin
+101 = the `2026-09-14-melon-decomposition.md` §2 row. Resolution ±400 coins/board.

## 1. Arm table (paired vs base; ALL = 68 boards, TOPB2 40, LIVE-C 28)

| arm | edit | req. | Δ ALL | sd | t | win % | Δours | Δtheirs | Δ TOPB2 (t) | Δ LIVE-C (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| `cow35p1` | COW +1 d3-5 | +3 | −350 | 1,787 | −1.62 | 39.7 | −445 | −95 | −226 (−1.11) | −528 (−1.19) |
| `cow68p1` | COW +1 d6-8 | +3 | **−1,009** | 2,586 | **−3.22** | 35.3 | −846 | +164 | −605 (−1.80) | −1,587 (−2.73) |
| `cow68p2` | COW +2 d6-8 | +6 | **−1,187** | 2,988 | **−3.28** | 42.6 | −1,217 | −30 | −689 (−1.79) | −1,898 (−2.81) |
| `cow911p1` | COW +1 d9-11 | +3 | −579 | 3,556 | −1.34 | 48.5 | −2,111 | −1,532 | −793 (−1.35) | −272 (−0.43) |
| `shp35p1` | SHEEP +1 d3-5 | +3 | −392 | 1,714 | −1.89 | 42.6 | −44 | +349 | −254 (−1.03) | −590 (−1.62) |
| `shp68p2` | SHEEP +2 d6-8 | +6 | **−24** | 1,249 | −0.16 | 48.5 | −91 | −66 | **+53** (+0.28) | −135 (−0.54) |
| `cs68p1` | COW+SHEEP +1 d6-8 | +6 | −910 | 2,632 | −2.85 | 41.2 | −975 | −64 | −532 (−1.47) | −1,451 (−2.55) |
| `cs610p2` | COW+SHEEP +2 d6-10 | +20 | **−2,697** | 3,494 | **−6.37** | 29.4 | −3,043 | −346 | −2,284 (−3.98) | −3,287 (−5.34) |

**Eight of eight arms are ≤ 0 pooled and on LIVE-C**; the one not negative on TOPB2
(`shp68p2`, +53) is the arm that barely executes (§2). Every arm refuses under the
`S/isearch` §3 rule (Δ ≤ 0 on a family, or `Δours < Δtheirs`). Dose is monotone:
COW d6-8 +1 → −1,009, +2 → −1,187; COW+SHEEP +6 → −910, +20 → −2,697.

## 2. Execution check: the requests are mostly refused, and refusal is not free

Δ vs base, mean per board (`S/herd/report_all.md`):
| arm | req. | COW bought | SHEEP bought | all bought | alive d10 | alive d20 | animal spend | tiles d10 | idle d10 |
|---|---|---|---|---|---|---|---|---|---|
| `cow35p1` | +3 | +0.24 | −0.13 | **+0.07** | +0.18 | +0.00 | +19 | −0.24 | +0.06 |
| `cow68p1` | +3 | +0.74 | −0.56 | **+0.26** | +0.21 | +0.19 | +41 | −0.38 | −0.56 |
| `cow68p2` | +6 | +1.09 | −0.63 | **+0.37** | +0.35 | +0.29 | +93 | −0.97 | −0.85 |
| `cow911p1` | +3 | +1.88 | −0.29 | **+1.21** | +0.47 | +0.96 | +491 | +0.00 | −0.47 |
| `shp35p1` | +3 | +0.00 | +0.13 | **+0.16** | +0.15 | +0.16 | +75 | −0.26 | +0.12 |
| `shp68p2` | +6 | +0.06 | +0.09 | **+0.18** | +0.21 | +0.18 | +76 | −0.74 | −0.94 |
| `cs68p1` | +6 | +0.76 | −0.44 | **+0.29** | +0.29 | +0.22 | +76 | −0.97 | −0.79 |
| `cs610p2` | +20 | +1.99 | +0.34 | **+1.69** | **−0.37** | +1.56 | +774 | **−3.54** | **+17.88** |

1. **Delivery is 2-40 %.** d3-d8 wants convert at 2-9 %: B's dawn cash on d3-d8 is
   617/668/1,417/866/768/1,886 coins against ~400/animal (`raw_B.npz`), so the
   mid-game herd is **budget-bound, not want-bound** — the mid-game reading of
   `S/isearch` §5 ("the want is slack where it is not executed"). Only **d9-11**
   executes (40 %, +1.88 cows; dawn cash 1,664/5,803/3,548).
2. **The marginal cow displaces a sheep** (−0.13 … −0.63 on every COW arm): net
   animals alive at d10 rise only +0.18…+0.47 on a +3…+6 request — the mid-game form
   of `S/isearch` §5's "only the total binds" (`cow02p1 ≡ shp02p1`).
3. **An unexecuted want still costs tiles**: `plant_total = n_dev − sum(animal_want)`
   (`src/kagg3/core/brain.py:992`) subtracts it from the crop budget whether or not
   the animal is bought. `cs610p2` asks 20, buys 2, and at d10 holds −3.54 tiles
   (STRAWBERRY −2.04, MELON −0.85, WHEAT −0.53) and **+17.88 idle tiles** against a
   base of ~2.7 — the whole −2,697. The engine-like 14-animal herd is **not reachable
   through `animal_want`**: asking for it strips the crop plan and idles the land.

## 3. Ledger: where the coins go (Δ coins/board, both seats)

| arm | our MILK | our EGG | our WOOL | our FERT | our crops | their MILK | their WOOL | their STRAW | their ALL |
|---|---|---|---|---|---|---|---|---|---|
| `cow68p1` | −527 | +124 | −224 | **+156** | −285 | −1,345 | +1,218 | +350 | **+135** |
| `cow68p2` | −756 | −115 | −378 | **+253** | −175 | −1,903 | +1,246 | +724 | −80 |
| `cow911p1` | −33 | −643 | −277 | **+482** | −1,104 | −1,915 | +593 | +31 | **−1,625** |
| `cs68p1` | −503 | −108 | −184 | **+230** | −273 | −1,464 | +803 | +673 | −103 |
| `cs610p2` | −829 | −875 | −161 | **+766** | −738 | −2,383 | +367 | +1,964 | −487 |

Almost all of it lands in **d15-29** (the d0-9 and d10-14 columns of
`S/herd/report_all.md` are inside ±300 on every arm and both seats).
* **Fertilizer — sign confirmed, size refuted.** Every arm is fertilizer-positive,
  **+33 … +766** coins/board, rising with cows bought; +766 at +2.0 cows is this
  channel's ceiling against the **−11,322 fertilizer / −7,326 milk** gap of episode
  108806196. `LOSS10`'s "fertilizer −7.3k with more cows" closes as *right sign, two
  orders of magnitude too small, overpaid for elsewhere*.
* **d6-8 is our own glut, not denial.** `cow68p1` holds +0.91 cows at d10 and sells
  **less** milk (−527): the extra d15-29 supply pushes the milk quote down for both
  seats (theirs −1,345) and the opponent re-books the value as wool (+1,218) and
  strawberry (+350), net **+135**. `Δours −846 < Δtheirs +164` — we pay alone, the
  two-purse displacement signature of `counterfactuals-overstate`.
* **d9-11 is real denial we cannot afford.** `cow911p1` takes 1,915 of milk and 525
  of fertilizer off the opponent (their ALL SALES −1,625, the only arm that hurts
  them) but costs us EGG −643, WHEAT −378, TOMATO −348, WOOL −277, MELON −202 and
  +539 of spend: −2,111 ours, −579 net. Genuine denial, still the wrong trade.

## 4. Reachability: can the ES move the mid-game herd?

Decode-only, `S/herd/reach.py`; method copied from
`2026-09-14-melon-reachability.md` §2-3 (bisect an exact additive coordinate,
`jax.grad` for the norm; an isotropic sigma draw projects on any fixed unit
direction as N(0, sigma), so sd = boundary / (sigma·‖g‖)). The chain is

    animal_count = _qfloor(sig(head[6]) * n_dev)   src/kagg3/core/brain.py:968-969
    wa = softmax(grow[EGG,MILK,WOOL]*(1+sig(head[2])*4) + a_mix)        :988-990
    animal_want = _largest_remainder(wa, animal_count, 3);  plant_total = n_dev - sum(animal_want)   :991-992

with `head = gh @ g2 + gb2` (`src/kagg3/core/policy.py:684`, shapes `:327`) and `a_mix`
from `crew = gh @ g8 + gb8` (`:683`, `:369`). So `gb2[6]` (theta slot 3,880) is an
**exact additive bias** on `head[6]` — the animal analogue of the melon doc's `cb[I_MELON]`.

**B asks for no animal at all across d3-d9.** On the 720 real observations of
`tests/data/trajectory_obs.npz` at days 3-9, `animal_share` is 0.043-0.073 (day means
0.050-0.057) and `animal_count >= 1` on **0 of 80** boards on each of those days; the
first non-zero want is d10 (22/80), d11 (66/80).

| pinned dawn | head[6] | animal_share | B want G/C/S | Δ`gb2[6]` for +1 COW | want after |
|---|---|---|---|---|---|
| d6 (fixture row 12) | −2.8654 | 0.05389 | 0/0/0 | **+0.7858** | 0/1/0 |
| d7 (row 14) | −2.7974 | 0.05746 | 0/0/0 | **+1.0055** | 0/1/0 |
| d8 (row 16) | −2.8298 | 0.05574 | 0/0/0 | **+1.2202** | 0/1/0 |

‖∇θ head[6]‖ at B (mean over the three dawns); the boundary clearing all three
(+1.2202) in units of one draw's aligned component:

| block | n | ‖g‖ | sd@0.01 | sd@0.02 | sd@0.05 |
|---|---:|---:|---:|---:|---:|
| FULL theta | 6,789 | 8.704 | **14.0** | **7.0** | 2.8 |
| `gp` | 864 | 3.924 | 31.1 | 15.5 | 6.2 |
| `dh` | 128 | 4.060 | 30.1 | 15.0 | 6.0 |
| `g2,gb2` | 594 | 3.283 | 37.2 | 18.6 | 7.4 |
| `gb2` alone | 18 | 1.000 | 122.0 | 61.0 | 24.4 |
| **`g8,gb8` (animal mix)** | 132 | **0.000** | **inf** | inf | inf |

The easiest single dawn (d6) is 9.0 sd at sigma 0.01 and 4.5 at 0.02; all three
take 14.0 / 7.0. Recent arms train at sigma 0.01 and 0.02 (`S/flow21*/launch_*.sh`).
**The ES cannot move the mid-game herd at training sigma** — one member would have
to be a 7-14 sd aligned excursion — and `g8`/`gb8`, the block whose stated job is
the herd mix, has **exactly zero** gradient on `head[6]`: it can only split an
`animal_count` of 0, so it cannot produce a mid-game animal at any sigma. Same
shape as the melon verdict (§3 there: no block within 5 sigma at 0.01-0.02).

## 5. Conclusion

1. **Not a lever; the sign is negative in every window tested**: d3-5 −350/−392,
   d6-8 −909 … −1,187 (t −2.85 … −3.28), d9-11 −579, d6-10 at dose 2 −2,697
   (t −6.37); both families, monotone in dose. The arm nearest level (`shp68p2`,
   −24) is level because it is inert (+0.09 sheep).
2. **The want is the wrong channel**, not "cows are bad": d3-d8 is budget-bound (2-9 %
   delivery), the marginal cow displaces a sheep, and every unexecuted unit of want is
   still taken off `plant_total` (`brain.py:992`) — the whole of the −2,697 and the
   +17.88 idle tiles. The top-five herd cannot be copied by asking for it.
3. **Neither learnable nor worth a hand rule.** Not learnable: 7-14 sd of one draw at
   the training sigma, and the herd-mix block is exactly inert. Not worth a hand rule:
   the rule it would encode is what §1 measures, and that is negative everywhere.
   `2026-09-11-integer-search.md` §7's "B is a strict local optimum in its own integer
   lattice at radius 1-2" now extends from d0-d2 to **d3-d11 on `animal_want`**.
4. UNVERIFIED / not done: no engine leg was run. These are sim rows on a board set
   whose B row matches simscreen to the coin, and whose simscreen rows matched the
   engine at sign 6/6, max Δ 45 coins (`2026-09-11-simscreen-topb2.md`). Nothing
   survived, so no hold-out was spent and there is no finalist.
