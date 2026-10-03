## 16. Demand-preserving route and visible-price guard (2026-09-21)

The selected controller combines the public demand-preserving route with a small visible-state repair. At step 91 it sells the temporary Wheat immediately only when the observed Wheat price is at least **31**. At lower prices it leaves the stock for the inherited queue. The rule uses only the legal current observation and never reads opponent identity, hidden state, or replay IDs.

Fresh engine 1.32.7 evidence: **360/360 valid games**, both seats, 12 fresh seeds, 15 opponents; **344 wins, 6 ties, 10 losses**, 97.18% decisive win rate, and mean margin **+28,560.236**. Against the price31 control on the same engine family it records **17 wins, 6 ties, 1 loss** over 24 fresh paired games, mean margin **+30.92**. These are local engineering receipts, not an official Kaggle score.
