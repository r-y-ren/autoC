# An ES-trained planner, a residual RL head, and ~190 experiments that did not ship (rank ~330 write-up)

Thanks to Kaggle and to everyone who shared notebooks and discussion during Kaggriculture. We finished the submission period at **2,230 (rank 330 of 10,246, provisional until the final evaluation ends)**, after peaking at **2,858** on Sept 19 and rank 69 on Sept 26. This is not a winning solution. It is an honest account of what we built, what worked, and where we got stuck, because most of what we learned came from the dead ends.

## TL;DR

- We wrote a **bit-exact JAX copy of the environment** and trained a small policy with **OpenAI-ES**, which sets daily targets for a large hand-written **day planner**.
- On top of that we shipped a **PPO residual action head**, a **VRP crew router** (C kernel), and a set of default-off switches that each passed a paired, held-out judge.
- Our biggest single gain was **fertilizer timing** (+2,845 coins/board). Our biggest loss was a matchup we never solved: opponents who open with an early **melon plate**.
- Our biggest mistake was methodological: for most of the competition we judged candidates on **replayed opponent tapes**. Tapes do not react, and they overstated one candidate by 9x. We switched to closed-loop judging against reacting opponents only in the last three days.
- Our build log records roughly **16 uploads against ~190 rejected experiments**. The agent ended as a local optimum that incremental changes could not leave.

## 1. Agent architecture

The submission is pure numpy plus one small C kernel, deterministic, with a p99 act time of about 150-230 ms.

**Layer 1: policy (theta, ~7.7k floats).** One 64-unit encoder reads the board once per in-game day and outputs per-product grow/sell scores plus a "macro": crew size, planting target, animal wants, forward-buy days, fertilizer deferral. Trained by OpenAI-ES with common random numbers and antithetic sampling.

**Layer 2: day planner (~15.8k lines).** Turns the macro into the engine's action rows: one buy row, sell lots at fixed turns, per-unit routes, and an admission stage that decides which tiles each unit may reach. It is written once against an array module, so the JAX trainer and the numpy submission run the same code.

**Layer 3: residual action head.** A PPO head trained in self-play that nudges the planner's choices. It read +325 coins/board (t 8.2) on 233 held-out boards. It converted real losses and only gave back coin-flip wins.

**Layer 4: crew router.** At dawn a vehicle-routing search assigns tiles to workers, which saves hires. It was too slow in Python, so the kernel is compiled C.

**Around those:** a shed-overflow guard, terminal-day sell routes, a placement-night feed-and-care fix for new animals, and a rival detector that classifies the opponent's family from its first-hour cash and swaps in that family's supply curve for our price projection.

Every feature is a `NAME_ON` switch that defaults to off, with a test pinning the whole plan's hash to the shipped tree. A rejected switch merges without changing a byte of live behaviour. We had no agent errors or timeouts in any live game we audited.

## 2. How we judged changes (the most important part)

**The shop lottery.** The only randomness in the game is the end-of-day shop draw, which consumes one RNG draw per empty tile. Any change to our tile usage re-rolls every later shop. That is a zero-mean term of about ±25k coins a game, which wrecks on/off pairing and dominated our ES fitness noise for the first two weeks.

**Pinned tapes.** Replaying an opponent's recorded actions with the recorded town schedule removes the lottery and reproduces the live game to the coin. This became our judge: held-out boards, paired on/off.

**Two purses.** We report our coins and the rival's coins separately on every read. The market is shared, and its quote moves with cumulative inventory, so our production depresses their prices. Any lever that cuts our output hands them money. A day-0 melon plate cost us 676 coins and paid the rival 15,547, almost all of it through higher prices on the products we stopped supplying.

**Noise arithmetic.** One read of a 90-board judge has a standard error of about 175 coins. At a bar of "+450 at t ≥ 2", a batch of 30 true-zero candidates has an 18 % chance of producing a false promotion. We raised the bar to t ≥ 3 on 169 boards. An empirical-Bayes fit over 22 ES checkpoints said their true effect was −124 ± 47: the whole spread of "promising" results was judge noise.

**Where the judge failed.** A tape does not react. When our candidate deviated, the taped rival kept playing as if nothing had changed. One candidate read +25k on tapes and +2.7k against a rival that actually reacted, and an edge that passed on tapes did not transfer to the live ladder. In the last three days we replaced the tape judge with closed-loop play against reacting opponents: a pool of 36 public notebook agents and a behaviour clone of the top build. We should have done this from day one.

## 3. Timeline

| When | What |
|---|---|
| Aug 21 | Start. Exact JAX simulator, ES, goal of "strategy learned from outcomes only". |
| Early Sept | ES plateaus. We find the shop lottery and move to pinned tapes. |
| Sept 14-16 | ~2,750. Fertilizer timing lands: +2,845 coins/board, our largest gain. It came from comparing our play to a stronger class, not from our own ledgers. |
| Sept 19 | Peak 2,858. First RL head goes live. |
| Sept 20-23 | Nine PPO/ES follow-ups fail to ship. Ports of top-team play reach 86-91 % fidelity and lose. |
| Sept 24-27 | VRP router, ES-tuned work genes, feed fix. Rank 69 at 2,689. |
| Sept 28 | We learn the tapes were flattering us and build the closed-loop judge. A two-kernel hybrid (play a public agent's opening on some seats) fails live. |
| Sept 29-30 | Small significant gains ship (+1,577 and +262 margin a game). A from-scratch deterministic body loses to our own agent by 23k. |
| Deadline | 2,230, rank 330. |

## 4. Where we got stuck

**The melon seats.** Stronger opponents plant melons on day 0 and sell about 50 units near 249 on day 10. Melon price only ratchets down, so the first seller takes the pot, worth about 12.5k. We lost 22 of 22 audited games of this kind. Our own early plate lost 15-30k because we stopped supplying everything else. We tried selling earlier, racing, vetoing late melons, counter-crops and bigger herds. Every one lost or read zero.

**A local optimum.** Our body earns its margin from mid-game strawberries and late milk, wool and eggs. Every change that funded a different opening out of that budget lost. An ES over head offsets found 0 improvements in 112 tries. The top teams play a different build (bigger early crew, early melon, fourth quadrant), and no sequence of small steps leads there from ours.

**Imitation did not transfer.** We reconstructed the leader's decision logic as 18 rules, ported top-team openings, and trained a behaviour clone. The clone reached about 87 % of the real thing's strength. Every port lost to the class it imitated.

**RL beyond the first head.** After the one head that shipped, loss-weighted PPO, win-only PPO, paired-baseline PPO, from-scratch heads, distillation and ES on the head all failed our gates. Each learner nudged our existing trajectory. None found a different programme.

**The field moved faster than we did.** The opponents we met were mostly one public notebook lineage (the V-series by ahmedberatozer) that re-released almost daily, and later copies of top-team code. A frozen upload depreciates. The package that scored 2,858 on Sept 19 would not score that two weeks later, and our later, measurably better packages plateaued at 2,420-2,550.

**The ladder itself.** Rating steps shrink with games played, so a submission's landing point is mostly decided in its first 40 games. Re-uploading was about 30 times faster than climbing, which made the live rating a noisy instrument.

## 5. What we would do differently

1. **Judge against reacting opponents from the start.** Replays are exact and still wrong for any candidate that changes the game.
2. **Study the top of the board before optimising.** We spent weeks tuning against the band we met while the top ten played a different build.
3. **Budget for a rebuild.** About 190 rejected experiments around one body is a signal. We tried a second body only on the last day.
4. **Keep the two-purse ledger.** In a shared market, "we earned more" and "they earned less" are different facts, and margin alone hides which one happened.
5. **Do the noise arithmetic before believing a result.** Most of our early "gains" were the top order statistics of a noisy judge.
6. **Keep the exact simulator and the byte-identity pins.** Both were worth every hour.

## 6. How we worked

Most code and experiments were produced with AI coding agents (Claude Code), one time-boxed agent per mechanism, in parallel, each ending in a written result with numbers. A second model reviewed results. That left about 2,750 commits, 800 experiment directories and 1,150 result notes. The speed was real. So was the cost: it is easy to run 190 experiments around a local optimum very efficiently.

Happy to answer questions. Congratulations to the winners.
