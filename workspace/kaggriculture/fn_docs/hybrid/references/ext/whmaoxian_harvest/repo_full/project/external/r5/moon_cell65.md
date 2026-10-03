## 25. Corrected comparison: match the seed, opponent and seat

**Correction, 22 September:** the earlier four-opponent baseline included `guard31`,
while the variant sweep included `public2965`. Their aggregate means were not
comparable. The earlier claim that these tests established baseline superiority
was incorrect. The combined 192-game baseline margin is **+1,097.802**, correcting
the earlier arithmetic value of +1,037.802.

We completed the missing baseline arm on seeds 7452001–7452012, the same five
opponents, and both seats. All 120 new games finished with both agents DONE and
exactly 720 states. The existing variant receipts record DONE/DONE but lack an
explicit state-count field, a limitation retained in this historical comparison.

| Arm | Games | Wins | Ties | Losses | Mean money margin | Paired margin gain |
|---|---:|---:|---:|---:|---:|---:|
| Original public source | 120 | 94 | 0 | 26 | +406.383 | — |
| Sale lookahead 4 | 120 | 100 | 0 | 20 | +595.267 | +188.883 |
| Seed hedge 0 | 120 | 94 | 0 | 26 | +418.050 | +11.667 |

This is motivation for fresh experiments. Seeds are the independent blocks;
mirrored seats are paired checks, not independent samples. Money margins and
these local wins cannot be converted into a Kaggle rating.
