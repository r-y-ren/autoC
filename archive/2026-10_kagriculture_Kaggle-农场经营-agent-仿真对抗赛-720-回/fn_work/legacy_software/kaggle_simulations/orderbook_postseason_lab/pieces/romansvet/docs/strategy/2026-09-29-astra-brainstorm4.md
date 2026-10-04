# ASTRA BRAINSTORM 4 — third participant: BRAINSTORM3 round-1 review (KEEP cell, tile-use lever, the determinant, slot)
Date: 2026-09-29 14:13-14:15Z | Model: gpt-6-astra (reasoning high, read-only, ephemeral) | Prompt: S/astra_bs4/prompt.md

**1. Run KEEP as a repair experiment; do not assume it preserves G2’s herd gain.** Restoring seed priority addresses the measured failure, but purchase priority alone does not guarantee timely planting, watering, harvesting and sale.

PFS spends **976+554+196+185+214 = 2,125 coins on seeds during d5–9**. Strawberry seeds cost **100**: restoring ten purchases consumes **1,000**, equivalent to **2.5 cows or 3.33 geese before feed**. This is total seed spending, not a measured strawberry-only reinvestment purse; the docs do not establish how much KEEP leaves available. [Funding ledger](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-portgap1.md), [seed costs](/mnt/e/_work/kaggriculture3/src/kagg3/spec.py:40).

The earlier evidence constrains expectations: reinvestment displaced seeds and lost **1.5–2.8k own revenue during d10–17**; additive reinvestment lost **2.0–2.6k margin** because apparent leftovers funded subsequent commitments. The previous aggregate calculation—**5,759−2,214−1,932=1,613** before feed—did not establish an available purse at purchase time. Round 1’s **0/12** audit supersedes that interpretation.

Nevertheless, sacrificing some animal gain could improve margin:

| V21, change versus PFS | Own coins | Rival coins | Margin |
|---|---:|---:|---:|
| G2 | +932 | +3,999 | −3,067 |
| CLS | +1,837 | +7,639 | −5,802 |

G2’s strawberry revenue changes are **+1,209 own / +4,288 rival**. Restoring the timing could recover more denial than the remaining herd earns. That is a hypothesis, not an additive forecast. [VCHECK1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-vcheck1.md).

I would run **PFS, G2+KEEP, CLS+KEEP**, reusing existing G2/CLS rows. Define KEEP precisely: on **every active reinvestment day d4–9**, compute the unmodified PFS grant on the current observation; reserve its granted strawberry quantity and cost before allocating reinvestment animals, while retaining feed and land reserves. Do not inflate strawberry demand or merely assign an equal priority that cheaper animals can win. Log seed purchases, planting dates, care, sales and remaining animal expenditure.

Use **v21 then m40**. Screening bar: **W≥12/21 and ≥37/40**, margin **≥−1k on each**, d15–17 strawberries **≥PFS−5**, no first-melon delay, no additional escapes. Then run **80 games each against p48c and g0capsfix**, requiring own **≥+1.5k, board-clustered t≥2**, margin **≥0**, W≥control. These are screening gates; slot promotion still needs faithful-programme confirmation.

**2. The tile choice is a lever only where the displaced crop’s sale schedule can survive.** Keeping d0 unchanged allows d3–5 changes; preserving late volume also requires preserving the earlier strawberry supply that sets late prices.

My additional cell is proposed **`EARLY_COW_TILE=1`** on pure PFS:

- During d3–4, advance at most **one** purchase toward PFS’s existing cow target, using a harvested NW tile otherwise scheduled for wheat/carrot replanting.
- Never remove a standing crop or displace strawberry/melon planting; reserve the replacement crop’s seed and a feasible Q2 planting slot.
- Require **400 plus feed** without delaying Q2 or committed seeds. Count the cow toward subsequent targets; do not add another animal later to compensate.
- OFF preserves PFS exactly. No blanket FEED_ALL or reinvestment.

For **one cow advanced approximately two days**, these are planning ranges, **not measured counterfactuals**:

| Book, coins/game | Own | Rival |
|---|---:|---:|
| Fertilizer | +120…+180 | −100…0 |
| Milk | 0…+800 | −300…0 |
| Wool / eggs | 0 intended | 0 intended |
| Displaced wheat/carrot | −200…0 | 0…+100 |
| Strawberry / melon | 0 required | 0 intended |
| Extra feed spending | −60…−80 | — |

Fertilizer uses roughly **two animal-days ×0.85 units ×90**; milk’s upper case allows one additional six-unit collection around **133/unit**, rather than assuming every advanced cow earns it. The **400 is advanced capital**, not additional lifetime cost, only if later purchases actually deduplicate. Gross production gains must also absorb lower prices on existing output.

The cheapest read is a **ledger over the existing 12 prefixes**, tracing each eligible tile and replacement crop through d29. Require **10/12** feasible placements, no protected-sale delay, and nonnegative cash after commitments; first test affordability without hypothetical extra receipts. If admitted, run **10 boards × two rivals (V56, p48c) × two bodies =40 games**, one seat each. Require nonnegative margin in both families and preserved strawberry/melon timing; this admits further testing, not upload.

**3. The strongest measured determinant is strawberry supply sold before the rival’s late wave.** Across this mix, its effect on the rival’s price exceeds the measured benefit of extra animals.

On V21, reducing our d15–17 strawberries **51→21** raises V56’s late price **89→135**: **208×46≈9,568 coins**, consistent with its **+9,879 full strawberry-book gain**. G2’s intermediate timing gives **208×20≈4,160**, consistent with **+4,288**.

Exposure is **57% V, 25.92% P48-shaped, 10.08% remaining MELON, 7% other**. Corrected late strawberry volumes are **208 /155 /168** for V56/P48/PQ4; a hypothetical ten-coin price increase across those three exposures costs approximately **1,756 weighted rival coins**. This is sensitivity arithmetic, not a prediction that all three prices move equally.

Majkel’s **189** late strawberries make it another exposed rival: applying V56’s **20–46** price change gives **3,780–8,694 gross rival coins**. Its Q4 and third melon batch do not establish that response; the documented **−5…−7k CLS analogy remains unmeasured**. [TOPAUDIT2](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-topaudit2.md).

**PFS has not been shown to maximise this property.** It is the measured baseline to preserve. P48’s first melon sale at **246** remains another unresolved disadvantage: the port reaches **256**, with **45.1 versus 69 productive tiles**, while p48c supplies only **72 versus155 late strawberries and 84 versus180 eggs**. Clone gains cannot establish that either denial or herd investment is optimal. [REFRESH3](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-refresh3.md).

**4. I confirm two PFS-copy uploads:** CLS loses **9/21 V wins**, and even granting its **+2,815 clone margin** across all non-V exposure gives **0.57×−5,802+0.43×2,815≈−2,097 weighted coins**. G2’s **−3,067 V margin** and unconfirmed programme transfer do not justify replacing the anchor; two uploads are needed to leave **PFS+PFS**. The max-of-two rule selects whole-submission ratings, so the documented **+10–14 expected points** from duplicate PFS noise is conditional, not additional strength, and the user retains the upload decision.

## Prompt

## ASTRA BRAINSTORM 4 (2026-09-29 14:13Z) — third participant: BRAINSTORM3 round 1 review

You are the standing third participant of BRAINSTORM3 (fresh Opus agent + orchestrator + you). Repo /mnt/e/_work/kaggriculture3 (read-only). Read first: docs/strategy/2026-09-29-astra-brainstorm3.md (your session-2 verdict, incl. the prompt with the full context and your HERD_RECEIPTS_18 / TRANSFER3 seeds), S/astra_bs4/round1_excerpt.md (BRAINSTORM3 round 1), docs/strategy/2026-09-29-vcheck1.md (both reinvest bodies vs the faithful V56 rival: vrp21_clsearch W 13->4 on the live V boards, margin -5.8k; bs2lp W 13->12, margin -3.1k; mechanism = PFS's ~50 d15-17 strawberries cap V56's 208-unit wave at @89, the reinvest bodies sell 21 / 30 and V56 sells @135 / @109), docs/strategy/2026-09-29-refresh3.md (family-pure clone rivals p48c / pq4c registered: closer on strawberry/egg/milk/wool, still no melon wave), docs/strategy/2026-09-29-topaudit2.md (Majkel1337's own body: 189-unit late strawberry wave, third melon batch, Q4 that pays), and the tail of S/p48graph2/checkpoint.txt (the morning-route port: herd 15.9 vs 18.4, Q3 d8 1/16, first melon 256; variants running).

### Round-1 result
HERD_RECEIPTS_18 funding audit 0/12: the d2 h1 cow fails everywhere - cash ~630 vs 400 is there, but the NW quadrant has no free tile from d2 h2; P48 puts animals on HARVESTED crop tiles on d3-5 (plants 20 -> 16.3, animals 5 -> 8.3) and buys Q2 only on d6, PFS replants those tiles so its herd stays 6 until Q2 d5: the herd gap is a d3-5 TILE-USE choice. TRANSFER3 is ready (116 fresh boards, three package trees identity 6/6, V56 + p48c + tree-rival arms, dry runs OK). Agent's hypothesis: what transfers is timing denial (the d15-17 strawberries ahead of V56's wave, the first melon sale), not the herd gain; identity boards d15-17 strawberries pfs 40.7 / g2 29.3 / cls 22.0. Agent's round-2 cell: REINVEST_SEED_KEEP="STRAWBERRY" on G2 (strawberry seed buys keep priority over animals on d5-9): {G2, G2+KEEP, CLS+KEEP} vs V56 v21 + m40 first (bar W >= 12, margin >= -1k vs PFS, strawberries >= PFS-5), then p48c / g0capsfix 80 g (own >= +1.5k t >= 2, margin >= 0). Slot state: live pair vrp20 (PFS) + vrp21_clsearch (V-LOSS); the orchestrator recommended two PFS-copy uploads; the user has not decided; 4 uploads left today, 5 tomorrow, deadline 09-30 21:00Z.

### Deliver (markdown, ≤ 1,200 words, numbers not adjectives)
1. Critique of the round-2 cell: will keeping strawberry seeds restore the V wall while keeping any herd gain, or does the reinvest purse then vanish (the d5-9 seed coins WERE the purse)? Give the coin arithmetic from the docs. Which cell would you run instead or in addition (exact switch semantics, grid, bar)?
2. The tile-use finding: P48 grazes animals on harvested crop tiles d3-5 instead of replanting. Is that a lever for PFS within the invariants (d0 unchanged, late volume kept)? What is the expected own/rival effect in coins per book, and the cheapest read (ledger over existing replays or ≤ 40 games)?
3. Given VCHECK1, TOPAUDIT2 (Majkel's 189-unit strawberry wave) and the corrected targets: which SINGLE property of a body most determines its margin against the current rival mix (57 % V, 36 % MELON of which 72 % P48-code), with the coins; and does PFS already have it maximised?
4. Slot: confirm or amend the two-PFS-copies recommendation in 3 sentences.
