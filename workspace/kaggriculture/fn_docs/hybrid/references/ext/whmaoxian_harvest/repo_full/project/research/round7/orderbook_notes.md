# Your Market List Is an Order Book

**Three measured changes on top of the strongest of the agents published on 20–21 September: an exact order book for
the market list, a priced gate on the late tomato investment, and four constants re-measured against today's field.
89 losses turned into wins, 0 wins lost, over 280 games.**

| | |
|:--|:--|
| **vs plain V55, 7 new public agents × 20 seeds × both seats** | **191-53 → 280-0**, mean margin **+758** |
| **vs plain V55, mirror** | 40-0 |
| **Recorded ladder games** | 108 real games of the current meta, including the unpublished agents: 74-34 → 78-30 |
| **Why V55** | the strongest of seven agents published on 20–21 September in a 840-game round robin |
| **Base** | V55 by Ahmed Berat Özer (Apache-2.0), byte-for-byte |
| **Runtime** | standard library only |

**To use it:** *Copy & Edit → Save & Run All → Submit* and pick `main.py`.

All the farming is the base's, which stands on a long public lineage (credits at the end).
What this notebook adds is layer D, and how it was measured.

## 1 · The agent

The next cell writes `main.py`, byte for byte the file I submitted: V55 as published, four of its constants set to
different values, then two appended blocks.
All upstream Apache-2.0 notices are kept at the top of the file.

## 2 · Layer D: your market list is an order book

Both players' market lists are settled together, slot by slot: order 1 of each list, one unit at a time at the same quote,
then order 2, and so on. A unit sold in an early slot gets a better price than the same unit later, because both players'
earlier sales have already pushed the price down. So the order of your own list decides who sells into whose glut.

Layer D replays that lockstep exactly for every way of placing the turn's sell orders into the slots the agent leaves
free, keeps purchases, round trips and deliberate empty slots where they are, and plays the ordering that does best
against the list a V48-family agent would submit in the same position. It scores at most 800 orderings a turn; the
original ordering is always among them and scores zero, so the layer can only move a sale when the replay says it pays.

V55 is still the V48 lineage and carries V48's own per-unit lockstep evaluator (`_v44y_factor_margin`), so the layer
appends to it with no port and no change to any V55 function. The first cell above prints which function it wraps.

## 3 · Why V55 is the base

Seven agents were published on 20 and 21 September. Each pair played 40 games (20 seeds × both seats), 840 in all:

Look at the margins as much as the win rates. The strongest of them is ahead by about fifty coins a game in a season worth
about a hundred thousand: these agents share most of their code, and the games between them are decided by a few
hundred coins at most. That is the regime where the order of a market list matters.

## 4 · Evidence

Plain V55 and V55 + D against the same seven agents, including V55 itself, on the same 20 seeds and both seats:

The gain is almost the same against every opponent (+124 to +133 per game), which is what an ordering layer should look
like: it does not depend on who the rival is, only on the fact that both lists settle together.

## 5 · The tomato gate

V55 carries prvsiyan's late tomato investment: on day 18 it can buy the south-east quadrant, hire for it and plant ten
tomatoes that produce on days 26 to 29. It fires only when three pizza shops or farmers markets are open, which is the
point where the town's demand for tomatoes (six a day each, plus one for the town centre) matches the twenty a day the
investment grows. That is the right quantity to care about, but a shop count is a coarse way to measure it: the price
comes from the market inventory, and TOMATO has the narrowest anchor in the game, `T=200`. Eighty units fetch 18,355
coins at an inventory of 9,600 and 1,653 at 10,200.

So the gate projects the inventory instead of counting shops -- the town's demand day by day, the rival's tomato tiles
(public, with the day each was planted), our own twenty a day -- and prices every unit with the engine's own curve. It
commits when the projection clears 9,000 coins. Forcing the investment on regardless costs 34 wins in 119 games; the
threshold was chosen on live games, not on replays, because on replays a lower one looked better and then lost six
games net in the mirror.

## 6 · Four constants, re-measured

Every published improvement in this competition is a module-level constant moved by hand, and V55 has 69 of them. I
swept 26, two values each, one candidate per value, 50 games apiece against the same opponents and seeds; seven
settings turned 8 to 10 losses into wins with none lost. The four below are the market side, and they all point the
same way -- work the market harder:

| constant | V55 | here | what it decides |
| --- | --- | --- | --- |
| `_V92_P_EVERY` | 3 | 2 | how often the rival's coming sales are re-predicted |
| `V9_RACE_DEFAULT` | 41 | 44 | how many turns ahead a planned sale is reserved against the rival's |
| `_OR2_SLOT_MARGIN` | 20 | 8 | the gain needed before a sale is moved into an earlier slot |
| `_CA_MARGIN` | -5 | -15 | how thin a wheat-to-carrot swap may be |

Each was worth 12 to 24 wins on its own over 280 games. Together they are worth more than the best of them alone, so
they are four effects and not one counted four times. The file is rebuilt from the published V55 by
`counter/knob_round2.py`: same base sha256, four numbers, two appended blocks.

## 7 · Credits and license

* **Ahmed Berat Özer**: V55 and the V25–V55 series — every farming and market decision in this agent, and the V48
  lockstep evaluator layer D reuses.
* **thomastschinkel**: the v9 layers V55 is built on (the file starts from his v9/3).
* Both credit a long chain of public work (yhay81, prvsiyan, Dmitrii Gluzdov, aurax7, tetsutani, Seyit Kaan Gunes and
  others); every upstream notice is kept verbatim at the top of `main.py`.
* Layer D and this notebook: mine, released under **Apache-2.0** like everything they build on.

If this was useful, an upvote helps others find it. Questions and corrections are welcome in the comments.