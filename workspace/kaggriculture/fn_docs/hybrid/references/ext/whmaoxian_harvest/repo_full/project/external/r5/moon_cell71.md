## 28. Final market ordering · 22 September 2026

### Why ordering the final action matters

The engine processes market lists slot by slot, then unit by unit in lockstep. Sales of the same products can therefore earn different amounts when their slots differ. Earlier layers advance available sales and compact empty sale slots. Those later edits can make a previously optimized order stale.

Starting at step 216, the new wrapper reapplies the inherited ordering routine to the final market list. It permutes only contiguous SELL blocks of length 2–6. Product quantities, worker commands, non-SELL slots and the order of fixed purchases stay unchanged. It retains the existing final-action bookkeeping convention; it does not install the rejected own-sale history repairs below.

The search model compares against a clone of our own stock and orders and assumes unlimited money. It does not observe the rival’s private inventory, know the rival’s next action, or prove a funding guarantee. Reordering sales can still change cash at intervening purchases and change a responding opponent’s later behavior. The real-game holdout, rather than the model gain, is the relevant local evidence.

### Frozen holdout and reproducible comparisons

The completed panel has 3 arms × 7 intact opponent policies × 24 previously unused seeds × both seats = **1,008 games**. Its exact Cartesian coverage, source and engine hashes, actual callable names, 720 states, 719 calls per player and zero final-ordering errors passed the terminal audit. The candidate also passed every prospectively declared holdout selection gate. Every graph below is recomputed from embedded terminal rows. A win is one point, a tie half a point, and a loss zero.

We compare separately with the previous `bc80` controller and the original public `baseline`. The graphs include opponent groups, every seed block and the full distribution of paired changes. Seed-block bootstrap intervals reflect this panel’s finite sample; they do not account for all possible opponent populations. Shared upstream ancestry further limits generalization. No official rating is inferred.

**Uncertainty matters:** the 95% seed-block interval for mean winpoint change versus `bc80` touches zero. The panel does not exclude no average winpoint improvement, despite the positive observed gain and passed local gates. The code uses exactly the frozen analyzer’s `random.Random(7493999)` sequence: 20,000 resamples of the 24 sorted seed blocks, with the same draw indices for both control comparisons. It verifies every reported interval against the accepted analysis.

Terminal result SHA256: `b7abe9a9e42dcb7f79122b9a047a3e0819ff7a5a6626fe7500c09fdebf022adc`  
Protocol SHA256: `9c0e7b3fbdb0c432de04d129e375199cf326b52c9a734fa195c776b8074df63b`  
Independent analysis SHA256: `10f43203400ceffc6d9a5387bce9eab87f438cbb4ccf58633a12926841b6157a`
