# Pipe-16: Idle Workers on The Metav4 Farm

**TL;DR**: One layer on top of Tschinkel's v13 champion. 50-0 head-to-head, +$118/game margin.
Fork this, submit, and read on to learn how wasted PASS actions became free wheat.

---

**What this notebook does:**
1. Embeds the complete agent (no external datasets, no GPU, no internet)
2. Writes `main.py` and packages `submission.tar.gz`
3. Fork -> Submit -> Done

**Gauntlet Results (7 opponents, 50 games each):**

| Opponent | W-L | Elo Rate |
|----------|-----|----------|
| **Tschinkel v13 (Metav4 Farm)** | **50-0** | **100%** |
| **ahmed v48** | **50-0** | **100%** |
| **ahmed v49** | **47-3** | **94%** |
| **pipe-15 (prev. best)** | **47-3** | **94%** |
| **lynnsakurai v2** | **45-5** | **90%** |
| **tetsutani** | **40-10** | **80%** |
| **dmitriigluzdov** | **39-11** | **78%** |
| **Overall** | **318-32** | **90.9%** |

---

## How We Found It

Tschinkel's v13 (The Metav4 Farm) is already dominant: 40-0 vs his own 2945 champion, rebuilt PREDICT library from 1,200 fresh replays, V219 tomato crew skip, loosened CARROT2, earlier fertilization.

But the tape still has **idle workers doing nothing on days 0-2**. Three hands sit on `PASS` while the farm bootstraps. That's 15+ wasted actions.

### The money ledger told us:

We ran per-day money attribution on 50 games. Days 0-2 showed consistent $50-100 gaps against agents that utilized their workers differently. The idle hands are dead weight.

### The fix: HybridOpening (from dmitriigluzdov's insight)

Dmitrii Gluzdov's "A Smaller Market Shock" discovered that idle day-0 workers can be redirected to plant and harvest a temporary wheat crop:

1. **Step 0**: Add `BUY_SEED WHEAT 1` ($10) to the existing market orders
2. **Steps 2-6**: Idle hand 1 walks west to tile (2,4), plants wheat, waters it
3. **Step 29**: Water instead of building the not-yet-needed pasture
4. **Steps 49-57**: Idle hand 0 waters, harvests, restores pasture, delivers wheat
5. **Step 57**: Sell the harvested wheat as bonus income

**Key insight**: We keep Tschinkel's profitable `BUY 20 / SELL 15` opening round trip (it wins money against most opponents). We only ADD the seed purchase and worker redirection. Best of both worlds.

---

## Why This Stacks Cleanly on v13

v13 already has sophisticated sell reordering (ORDERPRI2 + v44y lockstep), rebuilt PREDICT tables, and the tomato crew skip. Our HybridOpening operates in a completely different domain:

| Component | Game Phase | What It Touches |
|-----------|-----------|-----------------|
| v13's ORDERPRI2 + v44y | Every step (216+) | Market order slots |
| v13's PREDICT/PREDICT2 | Every step | Sale timing |
| v13's V219 Crew Skip | Days 19, 21, 23 | Tomato labour |
| **HybridOpening** | **Steps 0-57 only** | **Idle worker actions + 1 seed** |

No overlap. The worker redirection finishes before any of v13's reflex layers activate. The pasture is restored by step 55, so the tape resumes its normal schedule from day 3 onward.

---

## Validation: 350 Games Don't Lie

| Opponent | This Agent | v13 Alone | Delta |
|----------|-----------|-----------|-------|
| v13 (Metav4 Farm) | **100%** | — | — |
| ahmed v48 | **100%** | 94% | **+6** |
| ahmed v49 | **94%** | 84% | **+10** |
| lynnsakurai v2 | **90%** | 92% | -2 |
| tetsutani | **80%** | 76% | **+4** |
| dmitriigluzdov | **78%** | 90% | -12 |
| pipe-15 | **94%** | 96% | -2 |

Net: **90.9%** overall (was 88.3%). The v49 improvement (+10) and tetsutani fix (+4) are the big wins. The dmitriigluzdov dip (-12) is expected — they use the same worker trick, so our edge there comes only from v13's other improvements.

---

## Build the Agent

No datasets, no internet, no GPU. The complete agent is embedded below.

## Build the Submission Archive

---

# Attribution and License

This agent is a derivative work. Full credit to the original authors:

### Base agent: Thomas Tschinkel
- **The Metav4 Farm (Submission v13)**: Route replayer chassis with RACEPX/RACE reservation, PREDICT/PREDICT2 rebuilt from 1,200 Metav4 replays, V219 Tomato Crew Skip, CARROT2 feed guard, ORDERPRI2 + v44y lockstep reorder, SHEDROOM, FERT day 14, and the full v9-v13 layer stack
- Apache-2.0

### Worker utilization layer: Dmitrii Gluzdov
- **A Smaller Market Shock**: Bounded alternative productive openings
- Redirects idle workers on days 0-2 to plant/harvest a temporary wheat crop
- Adapted here as "HybridOpening" — keeps the original profitable wheat round trip while adding worker utilization
- Apache-2.0

### Upstream lineage (preserved in agent source):
- **Ahmed Berat Ozer**: V25-V49 progression, the public V39 tape foundation
- **yhay81**: Shop router action tapes
- **prvsiyan**: V221B/V224C production/timing lineage
- **aurax7**: Reactive reservation activation
- **tetsutani**: Demand-preserving turn sale timing, weed repair
- **Rayk Kretzschmar, degnonguidi, leoprovorov, destbreso, lucifer19, salemali7**: Additional layers and tooling

All upstream Apache-2.0 notices are retained in the agent source.

---
*16 generations. 5 failed parameter tweaks. 1 idle-worker insight that stacked. If you found this useful, an upvote helps!*