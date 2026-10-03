## 7. Four grain, 27 milk, still a loss

One guarded route drawn from a current rank-five public episode exposed a physical failure. At callbacks 171 and 195, our workers requested two wheat units from an empty shed and received none. Four subsequent feed commands had no wheat available; a cow eventually escaped after two unfed days. Eight cows were purchased, but only 218 milk were produced, harvested and sold.

The **V226A feed repair**, now included in the default agent, forecasts the next wheat pickup using our own existing worker positions, pending commands and current plan. It buys only the full shortage, bounded to four units per turn and eight per day, with cash and shed-room checks. It skips dawn, route boundaries, conflicting purchases and the final day. Worker commands and routes stay unchanged. It uses no rival identity, hidden seed, rival private stock or future observations.

In both diagnosed seats, buying four grain across two turns removed the missing pickups and failed feeds. The cow survived; **245 milk were produced, harvested and sold**, with no milk discarded. The margin improved from **−11,816 to −2,566**, so both games remained losses. The improvement was not solely milk revenue: our reward rose 6,735, the rival's fell 2,515, and our milk revenue rose 5,137. Every changed cashflow is shown below.

The eight discovery games had **two wins and six losses both before and after**. Six zero-purchase controls reproduced both rewards and terminal states exactly. This is a verified repair of one failure mechanism, not a demonstrated public-score improvement. An independent editable copy remains in `feed_experiment.py`. The dated 474-cell transfer comparison below is retained for reproducibility. Section 9 adds the completed fresh comparison and later public histories.

### A win caused by a larger rival decline

Public-history control 107191256 changed from −1,158 to +3,018 in both seats. It also bought four extra grain and sold 27 more milk. Yet **our milk revenue fell 1,231 and our final reward fell 912**. The rival sold exactly the same quantities as before, but its final reward fell 5,088. Shared-market repricing explains the improved relative outcome; describing it as a higher-income farming strategy would be wrong. The complete executed-unit and cash deltas are in the downloadable report. This case has sales accounting, not the full animal-production trace used for the rank-five diagnosis.

The optional twelve-game rerun below compares `timing_baseline.py` and the editable feed experiment on the rank-five case, timing regression 107191723, and newly gained win 107191256, both seats. These are explanatory fixtures. After editing, use new cases and seeds to assess generalization.

A separate current-population refresh tested the earlier timing agent against newly collected guarded routes: 34 wins and six losses in the top-ten panel versus the parent's 30 and ten; 28 wins and four losses at lower ranks versus 26 and six. Those routes can reproduce observed plans and guarded continuations, but are not the private reacting code of the current top ten. The complete dated report is included in `feed_research.json`.
