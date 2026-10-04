Stream: PROGRAMME2R (remote-only)
Date: 2026-09-30 (committed by DOCSYNC1; verbatim S/programme2r/results.txt, patch S/programme2r/tree.diff)
Verdict: NONE - MMPQ rulebook executed by the planner (PROG_RULEBOOK_ON): fidelity ratio 0.804 (2/20 >= 90 %), V56 m40 W 0/40 dmargin -25,784 t -16.9, p48c -17,474 t -7.2

```
PROGRAMME2R results 2026-09-30 (remote only; /mnt/e down).  Tree: /home/user/stage_r/programme2r/tree (copy of S/pq4tail1/cand/t0) + tree.diff.
Policy: src/kagg3/prog/rulebook.py behind plan.PROG_RULEBOOK_ON (forces PROGRAM_ENGINE_ON; the MMPQ rulebook as the programme intent,
executed by the planner) + sub-switches plan.PROG_RB_* (melon-first route tier, no crew reserve, feed daily to d17 / production eves /
sheep stop d27 / none d29, d10+ sell-all cadence with fertilizer kept, d10 melon deposit by h18, mid-day wheat filler, strawberry/melon
before the mid-day herd buy, idle-unit harvest/water/collect/care).  prog/rb_tables.json = MMPQ per-day lookup tables (mktab.py), OFF by
default (PROG_RB_TABLES / _HERD: -3.0k / land 12/20 on fid20).  Rules (of the RULEBOOK table rows): implemented 22 (1.1 1.2 1.2b 1.3 1.4 2.1 2.2 2.4 2.6 2.7 2.14 2.15 3.1 3.3(d0-9) 4.1 4.2 4.4 4.6 4.7 4.8 5.2 5.3),
partial/hand-fit 14 (1.3b 2.3 2.5 2.8-2.13 3.3(d10+) 3.4 3.5 4.3 6.5 6.8), missing 10 (1.1b Q2 hour, 3.2 h0 10-order fill, 4.5 buy hour,
5.1 fixed d0-12 lots (planner releases stock instead), 6.1-6.4 literal d0-d2 order lists, 6.6 sell product order, 6.7 day shape).
OFF identity: tree with PROG_RULEBOOK_ON=False vs S/vband1/res/v56_ctl_m40 rows: 3/3 boards identical (ours, theirs, o240, t240).

FIDELITY (fid.py: our tree in MMPQ's seat of 20 real MMPQ replays, opponent = its tape, exact fast env; truth = both-tape replay, 6/6 exact)
  final config rb17 (tag fin):  land days exact 17/20 (bar 18) | d9 S/C/G within 1: 0/20 (bar 16) | d14 held >= 95: 11/20 (bar 95 all)
                                final >= 90% of MMPQ: 2/20 (bar 15) | final ratio mean 0.804 median 0.805 min 0.66 | apply p99 max 0.431 s
  means truth/ours: str15-17 50.0/30.6 | egg18-29 147/92.5 | wheat units 592/342 | tomato tiles d9-12 10.8/6.8 | PASS/day d10-28 0.9/15.2
                    WATER/day 56.6/49.9 | unfed animal-days 110/74 | terminal shed 0
  reference PFS (OFF) in the same 20 seats: ratio 0.934 (15/20 >= 90%), never buys Q4 (held 75), spend 25.7k vs ours 39.9k vs MMPQ 38.2k.
  iteration log (fid20 mean final): rb6 105.5k, rb10 105.4k, rb11 104.4k, rb13 105.4k, rb14 106.9k, rb15 108.1k, rb16 106.5k, rb17 106.5k
    (land 11->17/20 after the cow-schedule fix), rb18 tables 103.4k; P48 programme tables (PROGRAM_ENGINE_ON) 111.2k; PFS 122.8k; MMPQ 131.6k.

V56 reacting bank agent (S/pq4tail1/vr.py, seat 0, paired vs S/vband1/res/v56_ctl_*):
  m40 rb17: n 40 | W 0 (ctl 38) | own 91,633 rival 109,555 margin -17,922 (ctl +7,862) | dmargin -25,784 t -16.85 | down -14,838 t -12.58
            drival +10,946 t 9.15 | flips +0 -38 | str15-17 28.1 (ctl 48.5) milk18-29 106.0 (101.5) wool18-29 70.5 (101.5) egg18-29 135.2 (68.6)
  v21 rb17: n 21 | W 0 (ctl 13) | margin -23,379 (ctl +3,099) | dmargin -26,478 t -17.01 | down -15,386 | drival +11,092 | flips +0 -13
            str15-17 28.7 (50.9) milk 101.1 (97.7) wool 62.3 (77.4) egg 122.0 (84.3)
  (earlier rb9 m40: W 0/40, margin -20,476, str15-17 17.2)
p48c clone (rcr.py --rival p48c, boards_p48_16, both seats; PFS control run here as pfsp, same tree OFF):
  n 32 | W 25 (PFS 32) | own 98,995 rival 89,929 margin +9,066 (PFS +26,541) | dmargin -17,474 t -7.18 | down -13,982 t -9.52 | drival +3,492 t 2.46 | flips +0 -7
VERDICT: NONE.  Every bar fails except apply p99; the programme-engine execution of the rulebook converts MMPQ's spend (39.9k) into 143k
revenue vs MMPQ's 167k; gaps = wheat volume (-8k), strawberry d15-17 (-4k), eggs, idle crew (PASS 15/day vs 0.9).
```
