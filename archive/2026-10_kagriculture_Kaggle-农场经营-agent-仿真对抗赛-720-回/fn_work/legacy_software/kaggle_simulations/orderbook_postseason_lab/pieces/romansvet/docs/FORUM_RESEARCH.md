# Kaggriculture forum research — 2026-08-24

Source: all 108 topics in the competition discussion forum, harvested via
`discussions.DiscussionsService/GetTopicListByForumId` + `GetForumTopicById`
in a live browser session. ~45 read in full including comment trees.
Topic ids below link as `kaggle.com/competitions/kaggriculture/discussion/<id>`.

**Coverage:** 108 topics exist in the forum; **85 were read in full**, including all
comment trees. The 23 not read are greetings, under-18 / eligibility / account-admin
requests, and downvoted self-promotion — all at 0 or negative votes with no technical
content. Every topic with >=3 votes was read, as was every topic an organizer replied to.

Claims are tagged:
- **[OFFICIAL]** — organizer (bovard / Domino Weir / Addison Howard / María Cruz).
- **[MEASURED]** — a competitor published numbers with a reproducible method.
- **[CLAIM]** — asserted without published method.
- **[OURS]** — cross-checked against this repo during the research pass.

---

## 1. Engine facts the docs get wrong or omit

`#732450` (SIDHAARTH SHREE) forced an organizer audit; `#731953` (Triston Morgan)
and `#732820` did the same. **[OFFICIAL]** answers, all now folded into the docs:

| Thing | Truth |
|---|---|
| Animal CARE bonus | **+1/day**, not +2 as the rulebook said |
| SELL FERTILIZER | **Valid.** Docs saying otherwise were wrong |
| CARE required for fertilizer? | **No.** Every surviving animal yields 1/day regardless |
| Fertilizer accumulation | **None.** Boolean, not a counter — uncollected is gone |
| DIG | Only on **unoccupied** structures |
| Planting-day watering | Unwatered seed **weeds that same night** (EOD increment runs before the weed check) |
| Strawberry | Not indefinite: exactly 4 yields (ages 10,12,14,16), then dies |
| Melon max yield | Reached at age 10; the documented 6–12 window has **2 dead days** |
| Shed | **Not a tile object.** Access is exactly (4,4),(5,4),(4,5),(5,5) |
| Market orders | **Do not** require standing on an access tile (unlike PICKUP/DROP) |
| `T` = 24-day capacity | Deliberate: the market is calibrated on the *late* game, not all 30 days |
| actTimeout | **1 s/turn**, but `core` deducts only the *excess* over 1 s from a 60 s bank (`#733041`, `#733431`) |
| Random seed | **Not** exposed to agents; is in the replay (`#734743`) **[OFFICIAL]** |
| Locked tiles | **Passable.** A unit may move onto and across unbought quadrants; tile actions no-op there and consume nothing (`#733902`). The *browser demo* wrongly blocks the move — do not build intuition from it |

Unanswered by organizers: whether the last turn counts (a logging agent saw only
719 observations, ending day 29 turn 22 — Akul Sareen in `#732450`), and terminal
settlement of unsold shed inventory (`#733155`).

## 2. Balance patches — know which engine a number came from

- **1.32.6** (`#733431`, PR #1394): Town Center buys **1×/day** and no longer
  escalates to 2×/4× late. Shops are now sampled **with replacement**, so a season
  can roll 4 bakeries and zero yarn stores.
- **1.32.7** (`#735311`, PR #1399): hinge added to carrot/tomato/egg so price spikes
  under high shop demand + no production. `HINGE_GAIN = 8.0`; knees at
  carrot T=450, tomato T=200, egg T=332; carrot `below_target` also moved 0.20 → 1.00.
  Bovard: *"This should be the last change, excepting game breaking bugs."*

**[OFFICIAL]** Bovard, `#734562`: *"The servers always use the latest published
version, no overrides."* There is no evaluator-specific config layer — the source on
GitHub is the contract. Two traps in the same thread: the **competition-attached
Kaggle notebook/kernel was observed running `kaggle-environments == 1.29.3`**, far
behind the evaluator, and a kernel-observed config (`maxTurns 2000`,
`townCenterSellInterval 6`) that does not match the shipped game. **Pin the package
yourself; never read constants out of the attached kernel.**

> **[OURS]** Directly relevant to `kagg3-sim-equivalence-scope`: our gate is only as
> good as the version it was transcribed from, and "latest published" is a moving
> target we do not control. Re-run the equivalence gate after any upstream release.

**[MEASURED]** destbreso replayed 120 recorded episodes: firing rates land at
tomato 55.0% / carrot 28.3% / egg 25.8% against the stated 50/26/22. But median
scarcity sits *below* each knee (219 vs 200 tomato, 316 vs 450 carrot, 228 vs 332 egg),
so **the median game is the old game to the dollar**; only p90+ pays. Egg never
reaches the money short of the deepest game. Luka Duvanov re-derived from
`MARKET_PARAMS` and agreed: carrot +18% season value, tomato +0.2%, egg 0%.

> **[OURS]** `pyproject.toml` pins `kaggle-environments==1.32.7`. Any forum table
> dated before Aug 15 is a 1.32.6 table.

## 3. The market is the whole game — and it is a cliff

`#732655` (nishchal jain, engine teardown) **[MEASURED]**, everything starts at
market inventory 10,000:

| inventory | STRAW | MILK | WOOL | MELON | EGG |
|---:|---:|---:|---:|---:|---:|
| 9,800 | 239 | 283 | 245 | 296 | 62 |
| **10,000** | **120** | **160** | **200** | **250** | **50** |
| 10,050 | 24 | 55 | 55 | 225 | 43 |
| **10,100** | **1** | **1** | **1** | 150 | 42 |

Strawberry, milk and wool go **full price → $1 floor in ~100 units**. Overproducing
a premium good is not diminishing returns, it is a step function to zero.

Two more from the same teardown:
- **The $1 floor is sticky.** `_commit_unit` only increments inventory `if price > 1`.
  Past the floor you destroy goods for nothing and do not even move the price.
- **Market fills run before town consumption** in the step loop, so selling one step
  *after* a consumption tick prices better. Worth +0.2–1.4%/unit. **[OURS]** our
  `rollout.py` already has this ordering (`process_market` then `town_consume`).

### 3.1 The single most valuable insight in the forum

`#734412` (Luka Duvanov), independently confirmed by destbreso and Georgy Mamarin
by two different derivations **[MEASURED]**: *the base-price table ranks the crops
almost exactly backwards.* Price is `base ± amp·f(|inv − I0|)` with **separate
curves either side of I0**. You sell into the glut side. The town — Town Center
1×/day plus shops every 4 turns — digs the scarcity side for free, all season.

Season output of each product, sold **into the hole the town dug** vs **dumped flat**:

| product | base | town eats | into the hole | dumped flat |
|---|---|---|---|---|
| STRAWBERRY | 120 | 426 | **$100,445** | $4,173 |
| MILK | 160 | 327 | **$86,662** | $6,432 |
| WOOL | 200 | 228 | $54,340 | $8,097 |
| WHEAT | 25 | 525 | $21,152 | $10,813 |
| TOMATO | 60 | 228 | $16,812 | $7,861 |
| CARROT | 35 | 327 | $13,246 | $6,904 |
| EGG | 50 | 228 | $12,972 | $9,658 |
| MELON | 250 | 30 | $8,184 | $7,416 |

Mechanism (destbreso's independent route): shops unlock at end of day `d` when
`(d+1) % 3 == 0`, capped at 8 → **132 shop-instance-days** per season. Same nine
numbers from two derivations.

**Melon is the trap.** It is the most expensive item and the *smallest market*:
**no shop menu contains melon** (check `SHOPS`: bakery, pizza, brunch, yarn, ice
cream, pet cafe, smoothie, farmers market). Its only sink is the Town Center's
1/day — **30 units for the whole season**. Its glut curve is squared with target
3.6, putting it on the $1 floor after 158 units. Melon holds price *shallowly*
(still $150 at inv 10,100) but has **no scarcity upside at all**.

**Shop-count is the real demand signal** (Harshini Reddy, `#734637`): milk sits on
3 menus and sells above its 160 base most of the season; wool on 1; melon on 0.

**Variance matters as much as the mean** (Georgy Mamarin, `#734412`): 8 shops drawn
uniformly *with replacement* → median season opens only **5 distinct types of 8**.
Median season demand: wheat 504, strawberry 396, milk 288, carrot 270, and 180 each
for tomato/wool/egg. **34% of seasons have no wool buyer at all**; carrot is zero in
10% of seasons and ~684 at p95. A fixed herd size is only safe because those
constants were fixed — with replacement, they are not.

**Closed-form ceiling** (destbreso): total money available in an episode is about
**$703k at median demand for both players combined**. Across 32,570 public episodes
none exceeds it, and the best game on record collects **48%** of it. The market's
willingness to pay is *not* what limits agents here.

## 4. Action economy vs market depth — the two rankings disagree

`#734033` (maximo lorenzo y losada) **[MEASURED]**, profit per *farmer action* at
base prices — the binding constraint is 720 turns, not land or money (the market
accepts 10 orders/turn, so trading is effectively free):

melon 142 $/action · sheep+CARE 100 · cow+CARE 79 · cow feed-only 35 ·
sheep feed-only 32 · goose+CARE 28 · strawberry 27 · goose feed-only 18 ·
tomato 17 · carrot 17 · wheat 15

Reconcile with §3: **melon wins per action for the first ~30–150 units and is
worthless past that.** The action ranking is a priority order, not a revenue forecast
(the author says so explicitly). Wheat ranks last as a cash crop but every animal
eats it daily — its real value is feedstock.

**CARE is a 2–4× multiplier and is table stakes, not an edge.** Daily CARE multiplies
lifetime output ~**4.25× sheep, 3.27× cow, 2.08× goose** (`#732655`); the banked bonus
pays out in full on the next production day, so on wool's 3-day interval you bank 3
and collect 4 instead of 1. nishchal counted **321 CARE actions** in one strong public
agent's 720 turns. **[OURS]** `care_on` is already a per-day gene (`core/plan.py:149`).

**Fertilizer ceiling is `animals × days`** — one boolean per animal per day,
use-it-or-lose-it. The only question is what fraction your units physically reach.

## 5. Negative results others already paid for

`#732655` **[MEASURED]**, all in a local re-implementation of the step loop:

| Idea | Measured |
|---|---|
| **Geese** (egg is near-uncrashable, nobody sells it) | **−$42,512/game** |
| Hold through the glut crash, sell the recovery | −$1,408 (twice, independently) |
| More cows | −$3,895 → −$22,408 |
| **More hired hands** (fib cost outruns output) | **−$21,399** |
| Committing units to multi-turn routes | −$6,788 |
| Tomato / carrot | ≈ −$1,400 each |

*Why crash-holding fails:* **shed caps at 100 and end-of-day overflow is silently
destroyed.** Holding bins more produce than the recovery pays. Bank is permanent,
shed is not. *Why geese fail despite every premise being true:* a high price on a
low-throughput product is not an opportunity — they displace tiles from lines
earning several times more per tile-day.

**The one thing that worked:** herd composition, swept properly. `n_sheep` 6 → 9 was
**+$7,347/game (z=+8.8)**. The optimum is *sharp* — 9 great, 10 negative. And it is
not "more animals": 7 cows + 7 sheep = −$10,238; 0 cows + 14 sheep = −$41,987.
**The mix matters, not the headcount.** (The top public notebook is titled
"V16-RC5 | High-Score **8C/4S** Premium Market Lead", 243 votes.)

Endgame, `#735119` (Yogesh Jadhav) **[MEASURED]**, 16 paired episodes, 8 seeds × both seats:
- **Day-26 seed cutoff: +781.88 paired mean, 95% CI [+587, +977], positive 16/16.**
- Static calendar-based late-hiring cap: −233.00, CI [−510, +44], positive in 7 of 16.
  A calendar date is too blunt to value a late worker; his adaptive replacement also
  failed on normal supply (2–6, −276 mean) and is not submission-ready.

## 6. Land: the field independently reached our conclusion

`#734308` "Why aren't top solutions using 4th quadrant?" — nobody at any level of
the leaderboard buys it. Answers converge on: quadrant cost + Fibonacci hire cost
for the extra labour + late start on production ⇒ ROI is not there. Steve421471 has
seen a top agent buy land and *leave the outer perimeter empty to cut walking*.
Victor Mercklé: his max-money strategy used all 4 quadrants, but "almost everyone
will dump the market before you if you do that."

`#736567` (dzjiann) **[MEASURED]**, RL, arrives from the other direction: his policy
managed plot 1 well but only hit a 20–40% successful-harvest rate on plots 2 and 3,
so *"buying additional land appeared to have negative expected value"* and the policy
**stopped purchasing land altogether during training**.

> **[OURS]** This corroborates `kagg3-land-toxicity` from three independent
> directions. Our blind-verified −77.5k for a *free* quadrant is not a sim bug and
> ES is not failing to find a gradient — the gradient genuinely points down.
> The open question our data and theirs share: land pays only if the extra tiles are
> stocked with something the town still wants, and §3 says by the time quadrant 3–4
> comes online there is nothing left with a hole to sell into.

## 7. Walking is where the turns go

Luka Duvanov `#734412` **[MEASURED]**: his first agent spent **83% of all unit-turns
moving**, because it recomputed each hand's target every turn and they thrashed.
Making a unit **finish the tile it stands on before moving** — FEED, CARE, HARVEST and
COLLECT_FERTILIZER are all done from the same square — took that to 55% and
**roughly tripled the final bank**. Zone-based worker assignment (one hand per
column band, BFS within the zone) is the other commonly-cited fix (`#732623`).

Also: `HIRE` costs `fib(n)` and **the counter resets every morning**, so ten hands
cost $143 for 230 extra actions — labour is cheap; the constraint is that hands walk.
(Set against nishchal's −$21,399 for more hands: cheap to hire, expensive to *route*.)

## 8. Determinism, seeds and the RNG coupling

`#732613` (Yusuke Hayashi) **[MEASURED]**, the mechanism, on stock 1.32.5:
`_end_of_day` builds `random.Random((seed * 1_000_003) ^ day)`, calls `_spawn_weeds`
for player 0 then player 1, **and only afterwards draws the shop**. `_spawn_weeds`
consumes one `rng.random()` **per empty tile**. Consequences:

1. The shop draw is **not exogenous** — it moves with how many empty tiles each farm
   has, on *either* board.
2. **A fixed seed only fixes the town when your change leaves the RNG-consumption
   path alone.** This is a measurement trap, not a fairness problem: any A/B where
   the variant plants a different number of tiles is comparing different towns.

> **[OURS]** `sim/eod.py:53` already keys `random.Random((seed * 1_000_003) ^ day)`
> and threads the raw word stream through `spawn_weeds` → `unlock_shop` with the
> used-word offset. We model this correctly. The measurement trap still applies to
> our own sweeps.

`#731152` (Georgy Mamarin) **[MEASURED]**, seat symmetry: the per-unit market loop
quotes **both players against the same pre-commit inventory** before either commits,
so **going first buys no priority** — six seeds, both seats, identical banks. What
*is* seat-dependent is the **weeds**, since both farms draw from one stream in seat
order. A bot that reads the board can still diverge by seat. Seeds replay bit-for-bit
across processes. (Countered in `#736219`: Syed Asad Ali says destbreso measured a
seat-0 win-rate edge — treat seat symmetry as true for the market, open for the board.)

## 9. Opponent inference is tractable

`#737027` (dzjiann) **[MEASURED]**: opponent inventory is recoverable from public
state because the player-specific trades cancel:

```
ΔS_i = H_i − C_i − (ΔM_i + D_i) − F_i − L_i        opponent_total_i = S_i − own_total_i
```

MAE: **carrot 0.008, tomato 0.000, egg 0.000**. Milk/wool are much noisier because
concentrated selling hits the $1 floor, after which stock leaves private inventory
without appearing in `market.inventory` — a genuine identifiability problem, not
estimator error. His proposed feature set is the estimate *plus* `lower_bound`,
`upper_bound`, `uncertainty_width`, `floor_risk`, `private_loss_risk` per commodity.

This is the concrete lever behind Russell Kirk's framing in `#732613`: *"If you both
try to sell the same thing, both your profits suffer — and the first to sell gets the
better price."*

## 10. The ladder: how ratings actually move

`#736219` (Ryo Hasegawa, #1 at time of writing, 55 votes) **[MEASURED]** from fits to
his own submissions + an Elo simulator:

- New submission starts at **600**; **~90% converged after ~60 games**, usually within
  ~5 h. Burst of ~15 games/h for the first 4–5 h, then **1–2/h**.
- `K ≈ 200·e^(−n/26)` plus a small floor. (Syed Asad Ali measured a **plateau-then-cliff**
  instead: flat ~220 for 10 games, cliff to ~45–55 by game 20, floor ~8.5 by game 80.
  Either way, **the first few dozen games set the level**.)
- Afterwards growth is **logarithmic**: ~+50–70 per 100 games, residual noise ±25–50.

| games | share of 400-game rating | ±1 SD | wall clock |
|---:|---:|---:|---|
| 20 | ~60% | ±160 | ~1.5 h |
| 60 | ~87% | ±105 | ~4–5 h |
| 96 | ~92% | ±80 | ~1 day |
| 200 | ~97% | ±50 | ~4 days |
| 300 | ~99% | ±35 | ~1 week |

Rules that follow:
- **Do not judge a submission before ~60 games.** Compare two submissions **at the
  same game count** — an older one carries a 100–150 pt age advantage.
- **Treat <50 pt differences as noise**, even at 200 games.
- **Optimize win probability against the bots near your rating, not mean coin totals.**
  A bot winning 70% by small margins outrates one winning 60% by huge margins. Most
  changes that raise mean coins while raising variance are rating-negative.
- **Judge a change by win rate against *each* strong opponent, not the pooled mean.**
- Re-rolling an unchanged bot is worth ~+40 live points at 96 games, ~+10–15 once
  converged, **and none of it survives the final Bradley-Terry pass.**

Path dependence is real and disputed in size: `#734000` reports **byte-identical
copies ending 300–1400 apart**; Jacob Davis (`#736127`) ran the same experiment and
saw 2200 vs 1700 early **converge to within a few points** over several hours. Tien N.
(`#736219`): resubmit an unchanged bot only if it *started* badly.

### Final evaluation — the rule that changes submission planning
**[OFFICIAL]** Addison Howard + Bovard, `#732931`:

> The final B-T tournament uses **all episodes between *active* agents across the
> whole competition**. Episodes against now-deactivated agents do not count.
> **BOTH agents must still be active** for an episode to count.

Only your **latest 2 submissions** are active (5/day allowed). So every resubmission
retires a slot *and* destroys the episode history that slot had accumulated against
opponents who are still live. `#736187` **[OFFICIAL]**: no midterm eval will be run,
but "the scores your submissions converge towards are a useful signal" and BT scores
historically land close to final ratings.

Timeline: entry/merger **2026-09-23**, final submission **2026-09-30**, games run
**Oct 1 – ~Oct 15**, then the BT fit. **What you need on deadline day is your two
strongest error-free agents in the two slots** — an erroring agent plays nothing.

Match frequency has dropped ladder-wide since ~Aug 20 (`#736314`); plausibly compute
shifted to the Pokémon TCG final evaluation, which resolved similarly after Orbit Wars.

## 11. The meta: a monoculture, and it is beatable but not by strength alone

Consensus across `#732902`, `#733002`, `#733055`, `#734529`, `#735683`, `#736369`:

- Top-150–200 is **byte-identical to one of two variants** of a public notebook
  lineage (Kaito Fukami's, `#734212`). onlysmrtsumx: turns 1–51 identical across
  13 player-instances and 8 seeds, same actions and quantities **despite different
  prices, cash and opponents**; crop mix does not change whether the wool shop
  unlocks day 9 or day 24. **They are not price-responsive at all.**
- The static plan reportedly achieves an **81%+ win rate** (`#733055`, **[CLAIM]**).
- **[MEASURED]** `#733924`: three of the top-5 share an identical opening down to seed
  counts and hire numbers, which pins that ELO band at 3,117–3,131. **Two private bots
  sit above it** and match no public notebook.
- Michael Timbs (`#735683`) confirms as an insider: he extracted the play directly
  from the episode corpus, and *"a lot of teams are sitting on much better solutions
  but still iterating before submission so as not to reveal too much."* Because all
  traces are public, the game theory rewards **hoarding until the deadline** — expect
  the visible leaderboard to misrepresent the field until late September.

**Non-transitivity is the load-bearing finding.** `#736439` (dzjiann) **[MEASURED]**,
960 games, 6 public strategies, 16 seeds × both seats × both directed matchups:

```
Public B85 beats Andrews 2883      30–2
Andrews 2883 beats Kaito v35       21–11
Kaito v35 beats Public B85         24–8
```

Adaptive Farming was strongest overall (121/160) yet **lost to Kaito v35 17–15**. His
held-out diagnostic: opponent identity alone predicts outcome at 56.5%, opening branch
alone 56.5%, **opponent × opening 67.5%**. Conclusion: the pairwise payoff matrix is
more informative than average win rate, and a policy that must commit to an opening
before it can identify the opponent gets **cancelling gradients** — his PPO plateau
may be a correct mixed strategy, not an optimization failure.

> **[OURS]** This is the sharpest risk to `no-third-party-agents`. A self-play +
> built-ins pool optimizes absolute strength; the ladder pays on a payoff matrix
> against a specific, largely-cloned population. Being 4th-best absolutely while
> losing the three matchups that matter is a live failure mode here.

## 12. RL: the field's verdict, and where we actually stand

`#734952`, `#733383`, `#736567`, `#736917`, `#736369`, `#734384`:

- **No high-ranking entry uses RL.** Multiple top-20 competitors confirm pure heuristics.
  Rustam Bazarbayev: "Without RL you can reach 2400+."
- Reported PPO/self-play ceilings: **Shubham Phapale 20–22k** (JAX port, Kaggle TPUs,
  full self-play, reward = own gold − opponent gold at turn 720); **Mahog ~20k**;
  **LuvGoel <5k while rule-based earns 150k+**; **Zacchaeus "far less than rule-based"**.
  Phương Doan reports **100k** but only with a rule-based + PPO hybrid.
- BC fails on distribution: the replay corpus is huge but **behaviourally near-identical**,
  so cloned policies are fine in-distribution and collapse out of it (`#736567`, fishcat,
  那个男人). Atomic-action BC suffers compounding error; high-level BC works "moderately".
- Failure modes named repeatedly: 720-turn horizon, delayed harvest reward, zero-tolerance
  mechanics (one missed watering cascades), and — Michael Timbs — *"swapping one crop to
  another completely tanks the rest of the play and destroys any gradient."*
- Recommended shape where anyone got traction: **rigid rule-based logistics + a learned
  layer for the ambiguous parts** (market timing, opponent response). hengck23: copy a
  high-reward replay agent, then train a model to estimate opponent capacity/cash/sell
  date and feed "deviation from forecast" features to a market policy net.

> **[OURS]** Our ~102.7k absolute (`kagg3-genome-unblock-shipped`) is **4–5× the best
> pure-RL number anyone has published** and in the same band as strong rule-based
> agents. Our ES-over-a-structured-planner is exactly the hybrid shape the field
> converged on. The gap to the top is not our learning method.

## 13. Infrastructure others have built

- **Daily Top Episodes dataset** `kaggle/kaggriculture-episodes-index` (`#731215`)
  **[OFFICIAL]** — up to 20 GB/day of replays ordered by average agent rating.
- **Episode API quota** **[OFFICIAL]**: **3,600 episode views / 24 h** on
  `competitions.EpisodeService/ListEpisodes` (`#732114`); over-eager crawling gets
  an IP block that needs a manual reset.
- **[MEASURED]** `#736625` (Georgy Mamarin): the daily dumps and API-crawled corpora
  **stopped overlapping entirely on Aug 9** — 12 straight days with zero shared ids
  against an expected ~147. Both are slivers of a ladder playing ~**140,000 public
  episodes/day** (dumps ~0.5%, his crawl 0.5–3%). Practical: the two sources are
  *complementary*, need dedup only for Jul 30 – Aug 8, and neither is the meta.
- **Engine ports** (`#733392`): Baran Kucuk — CUDA, 1024 envs batched, **50,000 steps/s
  on an RTX 5090**. Michael Timbs — Rust, with a harness proving identical environment,
  submission ships as a single binary called from the Python entry point.
  Nikita Lugovoy — public **"4000× environment speedup"** notebook.
- Reference-agent tiers: raykkretzschmar's reference-agents dataset (tiers 0–9) is the
  common offline yardstick (`#735466`).
- Notebooks worth reading: destbreso's *Dissecting the Top Two* / *A DNA Test for Agents*
  / *Mutants at the Top* / *The Leaderboard Is a Habitat Gradient*; Yusuke Hayashi's
  *Your Seed Does Not Fix the Town*; nishchal jain's engine teardown; Luka Duvanov's
  *Strawberry Pays 24× What the Price Table Says*.

## 14. Submission and runtime envelope

**[OFFICIAL]** Bovard, `#731810` — the full answer to the five questions everyone asks:

| Limit | Value |
|---|---|
| Submission size | **100 MiB for EVERYTHING**, model weights included |
| Internet | **None** |
| Accelerators | **CPU only** — no GPU, no TPU |
| vCPUs / RAM / HDD | 1.6 / 6.5 GiB / 8 GiB |
| Config at eval | **Default configs**, not your local ones |
| Time | **1 s per turn with a 60 s time bank** |
| Daily submissions / active | 5 per day, latest **2** active |
| File location | `/kaggle_simulations/agent/` — set imports accordingly |

Consequences drawn on the forum: an in-the-loop LLM is out (no GPU, ~1.6 CPU-seconds
per move); `#733431` (robga) recommends baking any match-long precomputed table into
`submission.zip`, then spending the leftover per-turn budget plus the bank on search.

**Entry-point resolution** (`#733535`, Panagiotis Anagnostou): the harness does **not**
look for a function named `agent`. It executes your file as a module and picks up the
**last callable defined in the namespace**, then inspects `co_argcount` to decide
between `f(obs)` and `f(obs, config)`. `agent` is a convention, not a requirement — but
a stray helper defined after your entry point will silently become the agent.

**Environment dependency trap** (`#735332`): the Kaggle image shipped `numba` against
`NumPy 2.4`, which older numba rejects (`ImportError: Numba needs NumPy 2.0 or less`).
Unresolved by the hosts at time of writing. Verify third-party deps against the real
image, not a local venv.

**Packaging pitfall** (`#732450`): submitting from a Kaggle Notebook that only does
`%%writefile main.py` produces **no submission artifact** and fails at scoring.

> **[OURS]** These reinforce `kagg3-submission-packaging` — a broken archive scores
> ~3,000 coins silently. CPU-only + no internet + 100 MiB total is the envelope our
> shipped `theta.npy` and its runtime must fit; the "last callable wins" rule is a
> live hazard for any module that defines helpers below the entry point.

**Miscellany worth knowing:** the browser demo also omits `DROP` from its action
drop-down (`#733902`), so it is not a faithful reference. Rule 6.b's open-source
deeming clause names "discussion forum or notebooks" and it is **unclarified whether
public Datasets are covered** (`#733868`) — CC BY-SA agent code shared via a Dataset
may collide with rule 6.c's OSI-only requirement. No host answer yet. A 4-player /
8-player variant was floated and Bovard replied it "might just [be] a follow up
playground competition" (`#735209`) — not this one.


## 15. What this changes for us

Ordered by expected value, cross-referenced to memory.

1. **Stop selling melon at scale.** `kagg3-vs-kagg2-autopsy` records that we "sell
   melons into kagg2's crater." §3.1 says melon has **no shop sink at all** and floors
   after 158 units, while strawberry/milk are worth 10–24× *if timed into the town's
   hole*. Our `sell_min[9]` and `sell_lots` genes already express the timing; the
   product mix (`plant_target[5]`, `animal_kind`) may not be reaching the right corner.
   **Test:** a forced strawberry/milk-weighted route vs the current champion, paired
   seeds and both seats.
2. **Herd mix is a sharp, high-value optimum we may be leaving on the table.**
   +$7,347 for 6→9 sheep, negative at 10; the top public notebook runs 8C/4S. Our
   `animal_kind` handles **one animal type per day** — the mix is only expressible
   across days, which may be why ES cannot resolve it. Worth an explicit sweep
   (cf. `kagg3-es-converged`: small single-gene gains exist that ES cannot resolve).
3. **Day-26 seed cutoff** — +782/game, positive 16/16, cheap to implement as a
   terminal-phase rule.
4. **Land stays closed.** Three independent confirmations (§6). Stop spending
   research budget re-litigating it; the residual question is narrower — whether
   land pays *given* a product mix with unsaturated demand.
5. **The pool is our biggest structural risk** (§11). The ladder pays on a payoff
   matrix over a cloned population, and non-transitivity is measured, not theoretical.
   `no-third-party-agents` keeps the pool clean but blind. A middle path that does not
   violate it: reconstruct opponent *archetypes* from the public replay corpus
   (behavioural clusters, not code) and add them to the eval set — measuring win rate
   per archetype, not pooled mean.
6. **Change our offline metric.** §10: the ladder pays win *rate* vs near-rated
   opponents; the final BT fit is wins/losses only. `kagg3-selfplay-blind-spot` says
   our 1-bit fitness is fine — the forum agrees the 1-bit target is the *right* one.
   What needs to change is reporting per-opponent win rate rather than pooled margin.
7. **Submission discipline for Sep 30.** Only 2 slots are active; BT counts only
   episodes where **both** agents are still active. Freeze early, do not re-roll,
   leave a day to confirm both run clean. Judge nothing before 60 games / ~5 h.
8. **Re-verify the packaging envelope before Sep 30** (§14): CPU-only, no internet,
   100 MiB total including `theta.npy`, and the harness takes the *last callable in the
   module* as the agent. Cheap to check, silently catastrophic to get wrong.
9. **Watch the measurement trap** (§8): any A/B that changes how many tiles are empty
   changes the shop draw. Our sim models the stream correctly, but paired-seed
   comparisons across structurally different plans are not comparing the same town.
