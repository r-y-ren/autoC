## 8. Why the supply predictors were rejected

Correctly reconstructing past market flow does not mean predicting the next sale. We tried using positive rival supply from 24 callbacks earlier. Across 45,277 scored predictions, precision was 28.06% and recall 13.99%. Accuracy looked high at 96.38%, but predicting no supply event every time scored 97.03%. Another 3,023 ambiguous predictions were left unscored.

We also tracked publicly visible harvests and the worker's later return to the shed. On 21 already observed histories, this potential-delivery observer reached 42.90% precision and 23.82% recall. Its 96.44% accuracy again fell below the always-no-event baseline of 96.70%. It cannot observe private cargo directly.

A candidate that used this observer to gate the timing rule gained two wins and lost two in 42 discovery games. Both agents won 31 games, but the candidate's mean margin fell from 5,240.98 to 3,885.83 and its worst margin fell from −2,890 to −3,495. We rejected it as a replacement. These results do not show that every possible delivery predictor will fail; they show that these particular signals did not support this particular change.

One further trap is duplicate opponents. Dynamic Route Agent contained exactly the same agent and plans as Aurax v2. Most Powerfull Route duplicated the SevenTurnWide runtime and settings; only JSON whitespace differed. The additional Evgen chassis has different reactive code but all 13 plans match Shop0909. Different notebook titles should not inflate the apparent diversity of a benchmark.

For your next experiment, record actual purchases, pickups, production, sales and both final rewards. Separate an avoided loss of goods from a newly won game, keep the regressions, and identify which opponent implementations share their production plans.
