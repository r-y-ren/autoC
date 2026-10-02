# astra BRAINSTORM9 round 1 (gpt-6-astra, 2026-09-30 16:54Z)

Prompt: scratchpad astra_bs19/prompt.md (the 800-point gap: what it means mechanically, boldest untested ideas with 2-hour tests and qualifying numbers, the one last-slot prospect, the round-2 question).

**758 points currently; “800” means a major change in who we beat.** It is not an 800-coin deficit: only wins, losses and ties enter the ladder; coin margins do not directly count. [Official evaluation](https://www.kaggle.com/competitions/kaggriculture/overview/citation)

**100× win odds would correspond to +800 on a conventional 400-point Elo scale—but that scale is not verified here.** Under that illustrative model, 3,000 versus 2,281 would mean:
- Against 2,400 opposition: **97% versus 34%** wins.
- Against 2,900 opposition: **64% versus 3%** wins.
These are scale illustrations, **not measured class win rates**. Bradley–Terry compresses matchups into one strength; our programme/V asymmetry makes literal class predictions unreliable.

**15 losses per 20 comparable P48 games** is the concrete deficit. Moving 25%→60–75% requires recovering **7–10 of those 15 losses**, while retaining our V advantage. That is an operational target, not a demonstrated requirement for 3,000. We lack matched MMPQ exposure to calculate the exact fraction it wins that we lose.
**+5/156 reacting flips** establishes a useful improvement; it does not establish anything approaching that transformation.

**3 experiments remain defensible, ranked by plausible programme-win upside.** “Untested” below means absent from the supplied log; check implementation history before spending the two hours.

**1. OPENING: replace wheat inventory with productive capital, retaining the PFS crop engine.**
Mechanism: replace `BUY WHEAT 53` with a rolling feed reserve; spend released cash on an early cow/sheep tranche and its required housing. Preserve NORTH and PFS’s strawberry scheduling. Test financing the herd earlier, not importing MMPQ’s entire opening.
The danger is measurable: changing our wheat purchases also changes the rival’s purchasing costs and subsequent production. **Both purses**, feed shortages and delayed crop work decide whether this works.
**2-hour test:** a small 2×2 screen—bulk/rolling wheat × normal/early herd—against reacting programmes and V56; freeze one candidate before confirmation. No d0 programme latch: that opponent information is unavailable then.
**Third-slot number:** ≥**+8 net programme wins/80 held-out seats**, plus the common gate below.
Closed adjacent axis: programme bodies **−27k versus reacting V, −17k on faithful P48**; class-latched bodies **−15…−29k**. Those reject copying the programme, not necessarily this isolated capital reallocation.

**2. HERD + LABOUR: buy additional saleable output and the capacity to deliver it together.**
Mechanism: test **+2/+4 animals**, allocating cows/geese by observed milk/egg demand, jointly with enough hands to service them. Protect strawberry deadlines first; count housing, feed, wages and displaced crop work. Extra wool in a saturated market is worthless.
**269 versus 314 late animal units on P48** is a more useful target than matching a headcount. The supplied **17 versus 13** and rulebook **≈22 at d13** need matching dates before becoming herd caps; **207 versus 71 eggs** identifies a hypothesis, not guaranteed revenue.
**2-hour test:** 2×2 incremental herd × incremental service capacity; reacting programme seats plus full V56. Require actual collected/sold output, and examine whether our extra supply simply restores rival revenue elsewhere.
**Third-slot number:** ≥**+8/80 programme flips**; seek recovery of roughly **30–45 late animal units** as mechanism evidence, with strawberry production preserved.
Closed adjacent axes: generic hiring/reserve stacks, gene descent and clone retrains failed. The remaining hypothesis is the **financed herd–labour interaction**; merely forcing 12 hands repeats a failed axis.

**3. LABOUR ALLOCATION: reserve crews for competing production deadlines.**
Mechanism: a short-horizon allocator explicitly books travel and service time for strawberry harvests and animal production eves, then assigns remaining labour. More hands cannot help if the controller spends them on lower-value work.
**2-hour test:** first audit missed valuable deadlines on programme losses. If substantial, compare normal allocation with deadline reservations at identical staffing; add staffing only as a separate interaction cell. Judge against reacting programmes and V56.
**Third-slot number:** again ≥**+8/80 programme flips**; fewer missed deadlines without additional wins does not qualify.
Closed adjacent axes: unit fixes, greedy/sampled PPO and executor rules. **CARE_HOLD/CREW_PUSH_COST are already in SWITCH2**, so they are not new ideas. Run this only if the audit exposes scheduling behaviour those mechanisms do not implement.

**0 distinct endgame candidates currently justify a dispatch.** Sale timing **24/24**, death rules, crop mix, seed/acreage and bundle execution have been tested. “Stop feeding earlier” or “liquidate sooner” would reopen those axes without new evidence. Q4 is likewise closed by financing/profitability reads.

**1 common replacement gate:** freeze before confirmation; compare against retiring **vrp25**, and report vrp26 beside it. Require board-clustered paired win-score **95% lower bound >0**, margin **t≥2**, nonnegative own-coin change per set, no V56 paired-win regression, and preserved strawberry/late-animal output. The **+8/80** threshold alone is insufficient; verify package identity and errors too.
**1 harness limitation matters especially for these ideas:** market reactions are modelled, but rival unit actions remain tape-anchored. Large opening/herd changes need renewed reaction-faithfulness checks; identical baseline replay cannot validate those counterfactuals.

**7h14m permits a focused attempt, not four serial research programmes.** Prioritize opening finance, then its herd–labour interaction; reserve at least two hours for frozen confirmation and packaging.
**0 current candidates merit an upload, and none has evidence supporting closure of the whole gap tonight.** A qualifying incremental winner remains plausible.
**ONE last-slot prospect: the opening-finance candidate.** If it fails the gate, **none**—retain 56706557 rather than retire it for an unqualified experiment.

**Round 2 opening question:** “When we release the cash locked in d0 wheat and invest it in an early serviced herd, do we recover programme losses while preserving the strawberry wall—and how much of the gain survives the rival’s changed purse?”