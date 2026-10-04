# [Kaggriculture (team InSociEUP)](https://www.kaggle.com/competitions/kaggriculture)

A two-player farming game played by code. Each side gets a farm, 720 turns (a 30-day season) and
a shared market in town; whoever holds more coins at the end wins. An agent is a single Python
file, and Kaggle plays the agents against each other on a ladder.

**Standing on 2026-10-02 (provisional): rank 1,704 of 10,246 teams (top 16.6%), rating 1,620.9.**
Submissions closed on 2026-09-30. Games continue until about 2026-10-15, and a final Bradley-Terry
tournament over those games sets the leaderboard, so this number will still move. For scale: the
leader is at 3,076, rank 30 at 2,695, and the top 10% starts at 1,825.

This repository is the complete working record: the market economics we measured, our own agent
and the local toolkit built around it, the public agents we adopted in the last week, and a
decision log written as it happened. It was built by Santanu Banerjee working with an AI coding
agent (Claude, in Claude Code), which also ran a scheduled daily upgrade-and-submit cycle.
[CONVERSATION_TRAIL.md](CONVERSATION_TRAIL.md) summarizes that collaboration and defends, or
concedes, each decision.

## What was submitted

| | Date | Agent | Rating | |
|---|---|---|---|---|
| v1 | 09-11 | our own adaptive agent | 683.7 | frozen 09-21 |
| v2 | 09-13 | own agent, 10-melon opening | 693.2 | frozen 09-23 |
| v3 | 09-21 | own agent, 11-melon opening | 733.1 | frozen 09-23; about rank 5,123 of 9,894 |
| v4 | 09-23 | *herd-safe* ensemble (Dmitrii Gluzdov) | 2,264.8 | frozen 09-24 |
| v5 | 09-23 | *the-2965 Master Hybrid Engine* (haideptry) | 2,303.5 | frozen 09-24; team rank about 925 |
| v6 | 09-24 | *cha22* route-replay agent (Abhinav0370) | 1,634.2 | frozen 09-30 |
| v7 | 09-24 | *Herd Safe v3* (Arsgorynich) | 1,555.2 | frozen 09-30 |
| **v8** | 09-30 | *Step1009* (tetsutani) | **1,620.9** | **final slot 1**, live on 10-02 |
| **v9** | 09-30 | *cha22* again, unchanged | **1,483.0** | **final slot 2**, live on 10-02 |

v1 to v3 are ours. v4 to v9 are other authors' public agents, submitted unchanged; the credit is
theirs (see [Credits](#credits)). Every file is in [`submission/history/`](submission/history),
byte-exact to the author's published file and matching its SHA-256. The submission pipeline
converts CRLF line endings to LF, which is the only difference from what Kaggle received.

**Do not read this table top to bottom as a ranking.** Only a team's two most recent submissions
play; a displaced one stops and its rating freezes. v4 and v5 look strongest only because they
froze on 09-24, before most of the field adopted the same public agents and the 2,000–2,400 band
deflated. Measured against the same opponents in the same window, the order was the opposite:
cha22 2,099, Herd Safe v3 1,920, herd-safe 1,899, the-2965 1,751
([`work/ladder/`](work/ladder), [how](#reproducing)).

## The short version

1. **Sept 4–11: our own agent.** We read the engine source, built an exact local simulator about
   10× faster than the official one, and instrumented the market. That produced real findings
   ([the economics](#the-economics-measured-not-assumed)) and a rule-based agent. Against a panel of
   four strong public agents it went from 0–24 (51,007 coins to their 125,580) to 3–61 (77,598 to
   101,810): better, and still losing 95% of games.
2. **Sept 12–23: a daily improvement loop on that agent.** Nine scheduled runs tested ideas against
   the live agent on paired seeds and shipped only what won both on the panel and head-to-head.
   Two shipped (v2, v3). The ladder rating went from 683.7 to 733.1.
3. **Sept 23: the pivot.** With a week left we compared our agent with the public notebooks. The
   best one beat ours 8–0 locally (117,158 coins to 69,259). The host allows building on public
   work, so we adopted it. Within a day the team was near rank 925.
4. **Sept 24–30: riding the public frontier.** Each run re-pulled the newest public agents, played
   them against our live pair in the real engine, and took a slot only for an agent that won.
   That replaced the pair twice more (v6/v7, then v8/v9).
5. **What that bought.** Everyone else could do the same, and did. Exact ties, which only happen
   when an agent meets a copy of itself, were 2% of v4's games (09-23), 15% of v6's (09-24 to
   09-30) and **31% of v8's since the deadline**. The rank drifted from about 925 back to about
   1,700.

## What mattered, in rough order of value

1. **Forking the public frontier, and doing it late.** One afternoon of adoption moved the team
   about 4,000 places; three weeks on our own agent had moved the rating 50 points. The agents
   that beat ours 61–3 on September 4 were public and could have been submitted that day.
2. **A public agent is everyone's agent.** Adoption buys the crowd's median, not an edge. The
   notebook titles said "LB 2700" and "2965"; on 09-30 their own authors' teams sat at 2,242 and
   1,376. Those titles were peak readings on a ladder where two identical submissions have been
   seen 1,400 points apart.
3. **Local head-to-head predicted the ladder**, even between near-clones separated by tens of
   coins. The local order (Step1009 > cha22 > Herd Safe v3 > herd-safe > the-2965) is the order
   the ladder produced whenever two of them played in the same window. After the deadline:
   Step1009 1,649, cha22 1,545.
4. **Rating hygiene.** A frozen rating cannot be compared with a live one, and an early rating is
   mostly luck. Compare agents by performance against the same opponents in the same window.
5. **Two measurement facts about the game.** It is seat-symmetric per seed (swapping seats gives
   the mirror result to the coin, so playing both seats doubles the cost and adds nothing). And
   the town's shops are not fixed by the seed once two runs diverge, which moves results by about
   10k coins: short sweeps are noise.
6. **The economics below.** They shaped our own agent and remain true, but the public agents
   encode most of them already.
7. **An unattended daily loop needs to be unattended.** Ours ran on a desktop scheduler that only
   fires while the app is open: 12 of 19 scheduled days ran, and one upload failed without anyone
   noticing for three days.

## The economics (measured, not assumed)

These came from instrumenting the engine's own `_commit_unit` to record every trade
(`work/revenue.py`), on kaggle-environments 1.32.7.

**The market is a shared, finite pool.** Total extractable value is roughly $180–210k per game,
set by town demand. Both players draw from the same pool, which is why real games end at 100–140k
rather than the 180k a top agent makes against a do-nothing opponent.

**Price lives or dies at inventory 10,000 (`I0`).** Premium goods pay about 2× base while market
inventory is below `I0` and collapse toward the $1 floor above it:

| product | base | glut curve | units above `I0` to reach $1 |
|---|---|---|---|
| Strawberry | 120 | linear ×1.6 | 62 |
| Milk | 160 | linear ×1.6 | 76 |
| Wool | 200 | sq ×3.2 | 59 |
| Melon | 250 | sq ×3.6 | 158 |
| Carrot | 35 | sqrt ×0.7 | 842 |
| Tomato | 60 | sqrt ×0.6 | 529 |
| **Wheat** | 25 | **log ×0.2** | never (still ~$19 at +1000) |
| **Egg** | 50 | **log ×0.2** | never (still ~$41 at +500) |

So *not gluting* is worth more than producing more. A reference agent that made 164k averaged
$240 per strawberry and $240 per milk, double base, purely by keeping inventory under `I0`.

**Two products have no shop demand.** Fertilizer and melon are bought only by the town centre
(fertilizer not even that). Their prices never recover, so holding them is a pure loss.

**Hinge-curve products spike when scarce.** Carrot, tomato and egg use a `hinge` scarcity curve
that is calm up to a threshold and then runs away. We logged tomato at $636 and carrot at $160 in
games where neither player grew them. The host's August balance change (kaggle-environments
1.32.7) made this deliberate: tomato spikes in about half of all games if nobody grows it.

**Expected season-long town demand** (8 shop instances, drawn with replacement): wheat 495,
strawberry 396, carrot 297, milk 297, tomato 198, egg 198, wool 198, melon 30, fertilizer 30.
Wool depends entirely on the yarn store, which is absent in about a third of seasons.

**Crops are not perpetual.** A strawberry tile produces exactly four times and then dies; so does
tomato. A fertilised and watered production day gives two units instead of one.

**Strawberry gluts in some seasons only.** In one game both farms sold 489 units into about 396
of demand and the price ended at $1; in another, with two ice-cream shops, it held $210–239 all
season. A fixed cap is the wrong tool either way.

## Our own agent

Two layers ([`submission/history/main_2026-09-23_v3_prev.py`](submission/history/main_2026-09-23_v3_prev.py)
is the last version; `work/agent_v*.py` is how it got there).

**Market layer.** It sells against a reserve price computed from the live price curve rather than
emptying the shed. The reserve falls when the projected price (from both farms' visible production
and the remaining town demand) is below spot, when the shed nears its 100-item cap, and as the
season ends.

**Production layer.** It sizes the herd and the fields from the room the market leaves, reading
the opponent's farm (it is public) to subtract their expected output.

**Why it lost.** First throughput: strong agents did about 149 useful actions a day against 117
moves, ours about 100 against 190. A graded routing cost fixed that (about 150 against 115). What
remained was structural. Opponents sold far more from a similar number of tiles, and nearly every
change that raised our bank raised the opponent's by more, because both draw on the same pool.
[`STRATEGY_LOG.md`](STRATEGY_LOG.md) has every idea, with numbers, including the ones that failed:
selling policy (under 1% effect), geese (the feed costs more than the eggs earn), fighting for a
product the opponent floods (46k against 68k for standing aside), fertilising melons (+6,345 for
us, +9,138 for them), a strawberry cap (won the panel, lost head-to-head 4–12), and replaying a
recorded action tape (57k: it desyncs on a new seed).

## How the public agents were chosen

Public notebooks pack the real agent as a compressed blob. We extracted each one, checked it
against the author's pinned SHA-256, confirmed it imports only the standard library, and played it
in the real engine **by file path**, so Kaggle's own loader picks the entry point (it takes the
last callable in the file, which for these wrapper chains is not the function named `agent`).
An agent took a slot only if it beat the current holder across seeds. The results behind each
adoption are in `work/h2h*/`, and the day-by-day reasoning is in `STRATEGY_LOG.md`.

Submissions went through a private Kaggle notebook built by
[`kaggle_notebook/build.py`](kaggle_notebook/build.py): it embeds the agent (gzip + base64, since a
1 MB agent inline exceeds Kaggle's notebook size limit), plays self-play and a game against
`starter` inside Kaggle, checks the file hash, and only then is `main.py` submitted from the
notebook's output.

## What is here

```
README.md                  this file
CONVERSATION_TRAIL.md      the human–AI working conversation, summarized; each decision defended
STRATEGY_LOG.md            day-by-day log from the daily runs: every idea, the numbers, what shipped
FEEDBACK.md                the channel for feedback to the daily run
LICENSE, LICENSES/         MIT for our own work; Apache-2.0 for the adopted agents
submission/
  CURRENT.json             the final pair, with provenance and evidence
  UPSTREAM_NOTICE.txt      credits for every adopted agent
  history/                 every submitted agent, v1–v9, byte-exact
  main.py                  the agent the notebook pipeline builds from (= v8)
kaggle_notebook/           build.py, submit_to_competition.sh, and the notebook run logs
work/
  fastenv.py               the official engine on plain dicts, ~10x faster, identical banks
  eval.py, sweep.py, tourney.py, pool.py     panel evaluation and parameter sweeps for our own agent
  revenue.py, diag2.py, *dump.py             per-product revenue, per-day actions, and other probes
  agent_v*.py, agent_*_<date>.py             our agent's history and the rejected candidates
  extract_all*.py          pull the inner agent out of a public notebook
  matches2.py, summarize.py   head-to-head in the real engine, one subprocess per game
  h2h*/                    the results behind every adoption decision
  ladder/                  ladder games of our submissions + leaderboard snapshots (ids and scores only)
  replays_index.csv        the 41 replays studied: ids, sizes, hashes
  screened_public_agents.csv   every public kernel screened: ref, author, SHA-256
docs/
  daily-routine-prompt.md  the prompt the scheduled daily run executed
  claude-memory/           the AI agent's persistent notes for this project
```

## What is not in this repo, and where to get it

All of it is public on Kaggle already; none of it is ours to re-host.

| Kept local | Where it comes from |
|---|---|
| 41 episode replays, 1.23 GB (`work/replays/`) | `kaggle competitions replay <episode_id>` for each id in [`work/replays_index.csv`](work/replays_index.csv). Kaggle also publishes the top games daily as `kaggle/kaggriculture-episodes-<date>` (index: `kaggle/kaggriculture-episodes-index`). |
| `datasets/gm-episodes` (a 159 MB replay shard and episode tables) | `kaggle datasets download georgymamarin/kaggriculture-episodes` |
| `datasets/reference-agents` (ten reference agents, price curves) | `kaggle datasets download raykkretzschmar/kaggriculture-reference-agents` |
| The public agents screened but not submitted (`work/pub*/`) | `kaggle kernels pull <kernel_ref>` for each row of [`work/screened_public_agents.csv`](work/screened_public_agents.csv), then `work/extract_all30.py`. Authors re-run their notebooks, so today's version can differ from the SHA-256 on record. |
| The sparring panel and other notebooks read for ideas (`notebooks/`) | Public notebooks by boatlee, kaitofukami, indarkarhana, pilkwang, tetsutani, yhay81, raykkretzschmar, georgymamarin and bovard. `work/pool.py` lists the files it expects under `notebooks/extracted/`. |
| Saved Kaggle pages and forum threads | Not redistributable: they are logged-in page snapshots and other people's posts. What we took from them is summarized in `CONVERSATION_TRAIL.md` and `STRATEGY_LOG.md`. |
| The raw leaderboard download | It carries team names. The committed snapshots keep rank, team id and score. |

## Reproducing

```bash
pip install "kaggle-environments>=1.32.7"
```

Ladder performance of our submissions, from the committed data:

```bash
python work/ladder/ladder_perf.py work/ladder/games_2026-10-02.json work/ladder/leaderboard_2026-10-02.csv
```

A head-to-head between the three finalists in the real engine (12 games, about a minute each):

```bash
python work/matches2.py out.json work/h2h_example.json
```

```bash
python work/summarize.py out.json
```

Rebuild the submission notebook for whatever is in `submission/main.py`:

```bash
python kaggle_notebook/build.py
```

The panel tools for our own agent (`eval.py`, `sweep.py`, `tourney.py`) need the sparring agents
from the table above. On Windows, set `PYTHONUTF8=1` before using the `kaggle` CLI.

## Credits

The agents that carried this team's rating were written by other people and published openly:

- **Step1009** (v8): tetsutani, [demand-preserving-turn-sale-timing](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing)
- **cha22** (v6, v9): Abhinav0370, `abhinav0370/kaggriculture-cha22-agent`
- **Herd Safe v3** (v7): Arsgorynich, [herd-safe-v3-experimental-risk-aware-feed](https://www.kaggle.com/code/arsgorynich/herd-safe-v3-experimental-risk-aware-feed)
- **herd-safe** (v4): Dmitrii Gluzdov, `dmitriigluzdov/kaggriculture-herd-safe-sale-window-lb-2700`
- **the-2965 Master Hybrid Engine** (v5): haideptry, `haideptry/the-2965-master-hybrid-engine`

They build in turn on Ahmed Berat Özer's V39–V57 series, Thomas Tschinkel's state router and
Metav4, Yusuke Hayashi's Shop Router, shiiin9's order-book evaluator, and work by aurax7,
destbreso and prvsiyan. The full notices are in
[`submission/UPSTREAM_NOTICE.txt`](submission/UPSTREAM_NOTICE.txt) and inside each file. The
engine is [kaggle-environments](https://github.com/Kaggle/kaggle-environments) (Apache-2.0). The
sparring panel used Rayk Kretzschmar's reference agents and public agents by boatlee, kaitofukami
and indarkarhana.

Our own code and notes are MIT-licensed; the adopted agents stay under Apache-2.0
([`LICENSE`](LICENSE)).
