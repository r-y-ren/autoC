# Campaign resumption: top five

The active user goal is continuous improvement to a verified top-five Kaggle rank,
using time-boxed Sol subagents. The user additionally requires each completed code
change to be committed with an explanatory message. The coordinator owns commits
and integration; subagents own separate experiment directories.

## Current evidence

The previous handoff-reading turn produced useful evidence, but launched no work.
On resumption, master was at ec9416c with only the user's untracked `replays/`.
An actual SSH inspection found both remote RTX 3090s idle at 1 MiB. The local
RTX 3070 was at 749 MiB. Sandbox-local `ps` cannot establish host process state.

Fresh public API pulls into `S/ladder2/` on 2026-09-12 around 07:45Z found:

| Submission | Completed games | Wins | Latest rating |
| --- | ---: | ---: | ---: |
| B, 56161192 | 172 | 128 | 2598.06 |
| hr, 56143250 | 288 | 188 | 2626.90 |

The fifth-place submission was 56114097 at 3015.0. These are observations,
not fitted equilibrium predictions. No current evidence establishes top five.

## Rules checked

The official [competition rules](https://www.kaggle.com/competitions/kaggriculture/rules)
were retrieved through the public `competitions.PageService/ListPages` endpoint
with competitionId 147734 (rules page 742993). The page's HTML shell alone does
not expose the rules. Sections 2.6 and 2.11 permit publicly accessible external
data/tools and downloadable episode action replays. Section 2.12 forbids runtime
ingress and egress. Sections 3.5 and 3.6 restrict private sharing across teams.
Use public replays for offline training, preserve provenance, and keep the deployed
agent self-contained. No publication or submission was made during this check.

The CompetitionService response allows five submissions/day and two scored
submissions. It reports the final deadline as September 30, 2026 at 23:59 UTC;
the handoff's September 23 target is not that final deadline.

## Decision and experiments

Interpret the user's "No pooling" literally for evaluation: report each held-out
family separately and do not use the old pooled 90-board promotion statistic.
Also preserve the operational instruction against repeated monitoring loops:
use bounded jobs and completion notifications. B stays live; a validated new
candidate is intended to replace hr, with the physical upload left to the user.

1. **flow215 rotation safety:** direct resume restores the saved ladder before
   appending new tapes. A replacement list therefore grows support and memory
   instead of rotating. Stage checkpoint conversion and validate the actual
   trainer load path before any rotating launch.
2. **ROTBAND data:** select 180 distinct eligible teams and construct 120-tape
   windows replacing 30 tapes per window. Exclude all judge episodes, including
   all NEXT30 and NEXT14 boards. NEXT30 is not a training anchor. Selection is
   not tape verification; acquisition, action fidelity, and leakage checks must
   finish before launch.
3. **Smoothie recovery:** establish identity against the correct baseline, then
   read each engine leg separately. Correlated shop observations are not causal
   improvement evidence.
4. **flow213 fixed-support trial:** cap the default run at ten generations,
   keep all 1,191 selected genes including press, recheck allocation and remote
   files, and use NEXT14 because NEXT30 is in this arm's training set. This is
   an additional-support experiment, not a matched rotating-vs-fixed A/B: the
   forthcoming rotating arm uses different tapes.

No sim score, persistent parameter direction, or passing staging test promotes
a candidate. Promotion requires paired real-engine evidence with separate
held-out family results, followed by package fidelity and runtime checks.

The repository has no Git remote. Local commits preserve history but are not
a backup against disk loss.

## Historical checkpoint at 08:44Z (superseded below)

- flow213 is live on remote GPU0: group 1027375, trainer 1027398, root SSH
  session 20345. Two generations completed (1,161.5s and 837.3s), 236/240 rungs,
  approximately 9,158 MiB GPU memory. Ten-generation cap remains in force.
  Do not duplicate a launch after a tool timeout. After completion, archive
  `state.npz`, extract its centre, and run the paired engine legs as
  `flow213_g10s_hr` with NEXT14 routing. The watcher is stopped.
- ROTBAND has 48 verified replay/drawn/town triples and zero judge overlap.
  Source, selection and checksum provenance are committed. HTTP 429 stopped
  acquisition; there are no data jobs running. The runtime `http_stop.json`
  records that stop with unknown exact request time and requires a deliberate
  cooldown before any new request. Do not weaken the 120-tape window threshold
  or bypass the rate limit. flow215 remains unlaunched; GPU1 is available.
- flow211 g20 objective-family read completed and is committed: NEXT30 +391,
  W2 -489, LIVEC42 -40 coins, with separate-family statistics. Its held-out
  g20 screens remain missing. flow212's corresponding read is running in root
  tool session 39767, bounded to 1,800 seconds, with log
  `S/snr/flow212/recover_g20.log`. The earlier failed child jobs are terminal;
  they must not be mistaken for these corrected root-owned invocations.
- The post-sale reinvestment idea has a test specification. A preliminary
  heterogeneous-opponent replay census does not establish feasibility for B;
  the B-specific correction is still being finalized.
- User-requested Codex auto review is enabled in `/root/.codex/config.toml`,
  backed up to `config.toml.bak.20260912T080152Z`, and validated by TOML parsing
  and the installed Codex configuration loader. Existing session overrides
  may still govern the running session.

## Checkpoint at 09:08Z

- This continuation made progress: both g20 objective reads and the combined
  held-out screen completed, two centres were refused, training-data exclusion
  gaps were repaired, and the post-sale route hypothesis gained a reproducible
  B-specific necessary-condition census. The top-five goal remains active.
- flow213 is confirmed live on remote GPU0, trainer PID 1027398. Last direct
  inspection at about 09:06Z showed four completed generations; the last took
  835.3 seconds. The ten-generation cap remains. Archive and judge its g10
  centre with NEXT14 after completion; do not relaunch or duplicate it.
- flow211 and flow212 g20 are REFUSED by H30 screen losses at t=-4.00 and
  t=-2.81 respectively. H30B is also negative for each. All 120 B reference
  games match the prior screen exactly. Both objective-read sessions and the
  held-out screen are terminal with exit 0; child handle 84676 and wrapper
  91192 describe the completed screen, not live work. No further g20 TOPB2 or
  engine promotion checks are owed for these refused centres.
- ROTBAND retains 48 fidelity-verified archived cuts, but only 32 are eligible
  after the raw-cache/team exclusion audit. Sixteen are explicitly rejected;
  no artifacts were deleted. There are zero 120-tape windows. Current team
  exclusions also remove 41 of the original 180 acquisition targets before
  any HTTP request. The ListEpisodes 429 stop remains in force; no network
  acquisition ran in this continuation. Use a deliberate backoff from the
  recorded 08:45:20Z stop before a future normal-endpoint retry, and preserve
  immediate stopping on any renewed 403/429. Do not bypass the stop state.
- The post-sale census and route collector both completed; root reproduced
  46/60 positive-net-cash sale-days and 19/60 with seed-only geometric route
  capacity. The exact twelve episodes and tests are documented. These are
  upper bounds, not productive purchases. Next build a default-off seed-only
  runtime prototype with current-cash, target-conflict and crop-value checks;
  evaluate it directly in the unchanged engine. The runtime already supports
  an intraday patch to its cached plan. No policy code has been changed.
- All Sol tasks in this continuation are finalized. The only known remaining
  live experiment is flow213. The watcher and flow215 remain unlaunched.

## Checkpoint at 11:50Z

- Campaign work made concrete progress: flow213 finished training and its
  seven-family engine judge; the post-sale hook was implemented, its immediate
  crop-death bug was identified and fixed, and a watered crop was harvested in
  a fresh real-engine smoke. Top five remains unachieved and unverified; no
  production or upload change has been made.
- flow213 trainer PID 1027398 is absent, the remote log ends `done`/`EXIT=0`,
  and both remote GPUs report 1 MiB. Root judge handle 39524 is terminal exit 0.
  Its g10 centre has no demonstrated improvement over B; see consensus §129
  and `2026-09-12-flow213-g10-judge.md`. Do not restart this judge or extend
  training merely because hardware is free.
- The corrected post-sale hook is committed at 22d2c16. `water_smoke` completed
  exit 0 with one purchased/planted/watered/surviving MELON and a later six-unit
  harvest. Full H30 `h30_water` is running on smoothie-owned handle 75668,
  original process group 3486, runner 3488, worker 3503. Last child observation
  confirmed 13/60 replays. Root cannot poll a child-owned handle: ask the owner
  or inspect actual host processes. Preserve the 1,800-second cap and all
  partial artifacts; no result exists until the complete CSV and verifier pass.
- ROTBAND's first normal-endpoint retry after the deliberate 30-minute backoff
  succeeded: episode 108106946 seat 1 passed both 719-step fidelity checks,
  increasing archived cuts to 49 and eligible tapes to 33, with 16 rejected
  and zero windows. A further bounded 12-request acquisition is live on
  fresh_support-owned handle 19949; do not duplicate it. It stops on the first
  403/429. flow215 still requires the full 120 verified eligible tapes.
- Code changes are committed by logical change with explanatory messages.
  The current Sol owners are smoothie (watered pilot), rotation (strict judge
  coverage audit), and fresh_support (bounded acquisition and provenance).

## Stopped for terminal restart at 12:09Z

The user requested all work saved and agents stopped. All campaign processes
and Sol agents are stopped; remote training remains finished and both GPUs are
idle. Read `2026-09-12-HANDOFF-RESTART.md` before continuing. The preceding live
handles and counts are historical, not current state.

H30 watered evaluation is complete and adverse (-256.83 margin, t=-1.32).
The full-game artifacts are valid; its hour-23 verifier error was corrected.
ROTBAND has 119 saved selections, 61 verified archives and 45 eligible tapes;
58 selected episodes await download/cutting. No 120-tape window exists. A
four-board Flow213 seed-room ON/OFF comparison also completed and was identical
on all eight games. Code fixes, selected metadata and small result CSVs have
been committed; larger replays and the remote-source archive remain preserved
inside the workspace. Do not resume jobs until the user returns.
