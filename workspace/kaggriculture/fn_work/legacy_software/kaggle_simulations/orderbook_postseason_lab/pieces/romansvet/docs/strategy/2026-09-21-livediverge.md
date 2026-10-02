# LIVE-DIVERGE — VPOST32 replay mismatch is seed/weed noise, not live fallback

## Conclusion

The premise that a different final margin proves that the live agent emitted a
different action under the same state is false for this replay.  VPOST32 pinned
the opponent actions and town, but it deliberately drew a **new engine seed for
each opponent**.  Weed spawning remained stochastic under that new seed.  On
all 18 margin-divergent boards, the first live/replay observation difference is
a `WEED`; the policy action differs only later, after it has been given a
different board.

This is conclusive rather than correlational:

1. The exact uploaded archive (`dist/submission_res940_vpost.tar.gz`, md5
   `47e2088d644ef695a51a86671923787c`) was run sequentially over the recorded
   live observations.  It reproduced **every one of our 719 recorded actions on
   all 32 episodes**.
2. The 18 divergent candidate-seat replays were regenerated at the VPOST32
   seeds and reproduced the saved VPOST32 margins exactly.  Every trace's first
   state difference was a weed.
3. Those same 18 tapes were then regenerated with each episode JSON's
   `info.seed`.  All **18/18 final margins became exactly equal to live**,
   including `111547423` (`+60,397`, not `+66,957`).

Therefore the top cause is the replay harness's fresh seed ladder, not Kaggle
CPU speed, an exception, an action timeout, cumulative runtime, seat, or a
fallback in the agent.

## First action divergences

`turn` is the hour within the day whose observation produced the recorded
action (the action is stored in the following replay step).  To keep the table
readable, `F`, `Hn`, and `M` mean farmer, hand index `n`, and market.  Only the
components that differ are printed; all omitted components are byte-identical,
so each pair still specifies the complete difference between the two actions.
“Local” is the candidate-seat VPOST32-ON replay used by the prior report.

| episode | seat | first day/turn | live action (differing components) | local action (differing components) | timeout/error marker | live margin | replay margin |
|---:|---:|---:|---|---|---|---:|---:|
| 111539738 | 1 | 4/1 | `M=[SELL CARROT 24, SELL FERTILIZER 6, BUY_PRODUCT WHEAT 6, BUY_SEED WHEAT 4, BUY_SEED CARROT 1, BUY_SEED STRAWBERRY 4]` | `M=[SELL CARROT 24, SELL FERTILIZER 6, BUY_PRODUCT WHEAT 6, BUY_SEED WHEAT 4, BUY_SEED CARROT 1, BUY_SEED STRAWBERRY 3, BUY_SEED MELON 1]` | none; `DONE`; overage 60→60 | +69,507 | +72,536 |
| 111540836 | 0 | 15/1 | `M=[SELL STRAWBERRY 8, SELL WOOL 5, SELL FERTILIZER 14, SELL EGG 5, BUY_SEED WHEAT 2, BUY_SEED TOMATO 1]` | `M=[SELL STRAWBERRY 8, SELL FERTILIZER 14, SELL WOOL 2, SELL EGG 5, BUY_SEED WHEAT 2, BUY_SEED TOMATO 1]` | none; `DONE`; overage 60→60 | +31,583 | +31,799 |
| 111543025 | 0 | 4/1 | `H0=PASS; M=[SELL CARROT 24, SELL FERTILIZER 6, BUY_PRODUCT WHEAT 5, BUY_SEED WHEAT 5, BUY_SEED STRAWBERRY 4]` | `H0=WEST; M=[SELL CARROT 24, SELL FERTILIZER 6, BUY_PRODUCT WHEAT 5, BUY_SEED WHEAT 6, BUY_SEED STRAWBERRY 4]` | none; `DONE`; overage 60→60 | +39,132 | +38,085 |
| 111544111 | 1 | 15/2 | `M=[HIRE,HIRE]` | `M=[HIRE]` | none; `DONE`; overage 60→60 | +53,844 | +55,143 |
| 111546316 | 1 | 4/0 | `M=[HIRE×4]` | `M=[HIRE×5]` | none; `DONE`; overage 60→60 | +5,760 | +5,018 |
| 111547423 | 0 | 4/21 | `H3=NORTH` | `H3=WATER` | none; `DONE`; overage 60→60 | +60,397 | +66,957 |
| 111551827 | 0 | 4/0 | `M=[HIRE×4]` | `M=[HIRE×5]` | none; `DONE`; overage 60→60 | +5,696 | +6,727 |
| 111552949 | 1 | 4/1 | `M=[SELL FERTILIZER 6, SELL CARROT 6, BUY_PRODUCT WHEAT 5, BUY_SEED WHEAT 8, BUY_SEED STRAWBERRY 4]` | `M=[SELL FERTILIZER 6, SELL CARROT 6, BUY_PRODUCT WHEAT 6, BUY_SEED WHEAT 8, BUY_SEED CARROT 1, BUY_SEED STRAWBERRY 3]` | none; `DONE`; overage 60→60 | +18,647 | +16,767 |
| 111554047 | 0 | 27/2 | `M=[]` | `M=[HIRE]` | none; `DONE`; overage 60→60 | +3,984 | +3,895 |
| 111555213 | 0 | 24/2 | `M=[HIRE]` | `M=[HIRE,HIRE]` | none; `DONE`; overage 60→60 | +3,616 | +3,354 |
| 111556360 | 1 | 6/0 | `M=[HIRE×5]` | `M=[HIRE×4]` | none; `DONE`; overage 60→60 | +1,183 | +1,214 |
| 111557456 | 1 | 7/9 | `H0=DIG` | `H0=PLANT STRAWBERRY` | none; `DONE`; overage 60→60 | +9,382 | +9,053 |
| 111558619 | 1 | 27/0 | `M=[HIRE×10]` | `M=[HIRE×9]` | none; `DONE`; overage 60→60 | +7,973 | +8,028 |
| 111559749 | 1 | 6/20 | `H3=PLANT STRAWBERRY` | `H3=DIG` | none; `DONE`; overage 60→60 | +3,919 | +5,453 |
| 111564245 | 0 | 11/0 | `M=[HIRE×10]` | `M=[HIRE×9]` | none; `DONE`; overage 60→60 | +11,653 | +11,774 |
| 111566501 | 1 | 10/0 | `M=[HIRE×10]` | `M=[HIRE×9]` | none; `DONE`; overage 60→60 | +5,291 | +4,189 |
| 111567205 | 0 | 27/2 | `M=[HIRE]` | `M=[]` | none; `DONE`; overage 60→60 | +811 | +900 |
| 111567625 | 1 | 27/13 | `H9=NORTH` | `H9=WEST` | none; `DONE`; overage 60→60 | −2,169 | −2,203 |

## Episode status and timing evidence

The episode schema has root `statuses`/`rewards` and, per step and seat,
`action`, `reward`, `status`, `info`, and `observation`.  These files contain no
per-step `duration` or `time` field.  For our seat on every one of the 32 games:

- status is `ACTIVE` until terminal `DONE`; root status is `DONE`;
- every post-initial action is a dict (no `None` action that would mark an
  `INVALID`, `ERROR`, or `TIMEOUT` turn);
- every per-step `info` is empty and there is no error text;
- `remainingOverageTime` is exactly `60` at the start, minimum, and end.

The configuration embedded in every episode is `actTimeout: 1` and
`runTimeout: 1200`.  Nothing consumed even a fraction represented by the
overage field.  As a secondary local check, direct calls to the exact archive
over all live observations had a worst measured call of about 0.15 s on this
CPU.  Local speed does not prove Kaggle speed, but the live status and untouched
overage budget do: there is no timeout signature.

The package also contains no clock, deadline, timeout budget, or fallback
logic.  Its entrypoint creates a `Runtime` and directly returns `rt.act`
(`main.py:92-100` in the archive).  `Runtime.act` rebuilds a plan at hour zero
and otherwise renders the cached plan, with no `try/except` around either path
(`src/kagg3/agent/runtime.py:40-99`).  An exception would reach the engine and
produce an error status; it would not silently select another policy.

## Correlations

- **Seat:** 8/15 seat-0 boards and 10/17 seat-1 boards diverged (53% versus
  59%).  This is not a meaningful seat concentration.
- **Day:** first action divergence ranged from day 4 through day 27 (median
  8.5); 9/18 were by day 7 and 5/18 were on/after day 24.  This is not a
  cumulative-time pattern.  More directly, overage remained 60 through the
  terminal step on every board.
- **Heavy planning:** 6/18 first differing actions were at hour zero and 14/18
  were by hour two.  That superficially resembles a dawn-planning effect, but
  it is explained by state sensitivity: plans are rebuilt from the dawn board.
  The first *observation* difference always appears at a day boundary and is a
  weed; action differences can appear immediately in hire/seed counts or later
  when a cached route reaches the changed tile.

## Root cause in the replay code

The VPOST32 command uses `--seed-base 3700788101 --seed-per-opponent` via the
BAND3 leg (`S/winjudge/judge.sh:81-84,104`).  The runner explicitly derives a
new RNG seed from that base and opponent index (`scripts/eval_vs_baselines.py:53-75`).
Those are not the live episode seeds stored in `episode["info"]["seed"]`.

Town pinning does not make the rest of the board deterministic.  Its own
contract says the original end-of-day function runs first, including weeds,
and only then overwrites `unlocked_shops`; the RNG/weed outcomes are left
untouched (`scripts/town_inject.py:20-31,134-149`).  Consequently “recorded
town + recorded opponent tape” is not a byte-identical board unless the live
engine seed is also restored.

## Concrete fix

There is no agent fix to make: the live package behaved exactly as coded.  The
fix is in the replay harness:

1. Add an explicit per-opponent seed map to
   `scripts/eval_vs_baselines.py:53-75,345-348` (or an equivalent `--seed-map`
   option), sourced from each downloaded episode's `info.seed`.
2. In `S/winjudge/judge.sh:81-84`, use that map for live-fidelity replays
   instead of `--seed-base ... --seed-per-opponent`.
3. Keep town pinning: the live seed reproduces weed draws, while the pin is
   still required because a taped opponent can alter the RNG-to-town coupling.

This exact remedy was exercised, not merely proposed: rerunning all 18
divergent tapes with their live `info.seed` reproduced all 18 live margins
exactly.  VPOST32 remains a valid common-random-number counterfactual for ON
versus OFF, but its 14/32 live-margin fidelity must not be interpreted as live
agent nondeterminism or timeout behavior.
