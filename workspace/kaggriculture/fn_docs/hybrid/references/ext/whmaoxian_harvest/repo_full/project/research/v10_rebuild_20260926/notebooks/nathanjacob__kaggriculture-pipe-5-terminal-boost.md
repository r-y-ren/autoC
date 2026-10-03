# Farm Smarter, Not Harder: A 1,400-Game Tested Agent

**TL;DR**: Fork this, submit, get a top agent. But if you want to learn *how* 
1,400 games of statistical testing shaped every decision, read on.

**What this notebook does:**
1. Embeds the complete agent (no external datasets needed)
2. Writes `main.py` and packages `submission.tar.gz`
3. Fork → Submit → Done

**Results (200 games per matchup, LB-identical rules):**

| Opponent | W-L-T | Elo Rate | Significant? |
|----------|-------|----------|--------------|
| Ahmed v40 (Elo 1747) | 165-34-1 | 82.8% | p<0.001 *** |
| Ahmed v41 (Elo 1668) | 192-8-0 | 96.0% | p<0.001 *** |
| degnonguidi (Elo 1660) | 192-8-0 | 96.0% | p<0.001 *** |
| renjistarfall (Elo 1655) | 195-5-0 | 97.5% | p<0.001 *** |
| reyhanks (Elo 1649) | 197-3-0 | 98.5% | p<0.001 *** |
| more-yield (Elo 1645) | 197-3-0 | 98.5% | p<0.001 *** |
| **Overall** | **1248-144-8** | **89.3%** | |


---

## The Journey: 5 Generations

Each generation was tested against the full gauntlet (top 7 agents, 200 games each) before promotion.
No vibes. No "it looks better". Pure W/L/T at p < 0.05.

| Generation | Key Change | Elo Rate vs Top 7 |
|-----------|------------|-------------------|
| Pipe-1 | Base agent | 81.8% |
| Pipe-2 | +sell timing | 83.0% |
| Pipe-3 | +opening optimization | 84.5% |
| Pipe-4 | +reactive layers | 85.0% |
| **Pipe-5** | **+terminal optimization** | **89.0%** |

The biggest single jump was Pipe-4 → Pipe-5. Analysis of 33 losses against the hardest opponent
showed **85% of close losses happen in the final 7 game steps**. Optimizing those last steps
flipped the hardest matchup from 66% to 83%.


---

## What I Learned From 2,800+ Games

| # | Lesson | The Hard Way |
|---|--------|-------------|
| 1 | **Verify your tar.gz** | One missing file = score 876 |
| 2 | **200 games minimum** | 20 games can't detect a 5% edge (p > 0.05) |
| 3 | **Win rate, not margin** | Elo only sees W/L/T. A $1 win = a $50K win |
| 4 | **Iterate, don't rebuild** | Each generation improves the last, never starts over |
| 5 | **Most games are ties** | Against similar agents, 80%+ games tie. Converting ties to wins is everything |
| 6 | **The last day matters most** | 85% of close losses happen in the final 7 steps |


---

## Build the Agent

No datasets, no internet, no GPU. The complete agent is embedded below.


## Build the Submission Archive


---

# Attribution and License

This agent is a derivative work. Credit where credit is due:

### Base agent: Ahmed Berat Ozer
- V43: Recovering Lost Harvests
- V40-V42 progression: Plans That Fit the Shops → Production That Fits the Market
- Apache-2.0

### Key contributions incorporated:
- **thomastschinkel**: Public State Router chassis
- **yhay81**: Shop router action tapes (shop-router-0908, 0909, 0911, 0913)
- **prvsiyan**: V221B/V224C production/timing lineage
- **aurax7**: Reactive V4/V5 reservation activation, day-end storage guard
- **Dmitrii Gluzdov**: Physical terminal rescue, Two Coins simulation planner
- **tetsutani**: Weed repair, room guard, clamp sells, dead stock layers
- **destbreso, lucifer19**: Additional capabilities
- **Rayk Kretzschmar**: Opening assignment from Rank Your Agent

All upstream Apache-2.0 notices are retained in the agent source.

---
*5 generations, 2,800+ games, 0 vibes-based decisions. If you found this useful, an upvote helps!*
