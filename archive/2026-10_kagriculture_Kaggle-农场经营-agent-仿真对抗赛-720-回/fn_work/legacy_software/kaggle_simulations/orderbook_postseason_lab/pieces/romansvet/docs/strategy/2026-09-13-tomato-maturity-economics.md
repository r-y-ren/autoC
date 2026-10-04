# Episode 108450468 maturity-economics stop test

The predeclared no-game test rejects the proposed maturity-value input as the
explanation for B's day-10--14 tomato omission in this episode. No public-B
corpus expansion, new feature, training, or engine branch follows from this
case.

## Exact result

At each recorded seat-1 dawn on days 10--16, the diagnostic reconstructs the
shipped B macro and complete NumPy plan. It then calls the existing planner's
own arithmetic: projected inventory at each product's first yield is
`PJ.inv_at_day(...) + _pipeline_units(...)`; `_stream_rev` prices the first
new seed's full remaining unit stream; and the actual `grow_mult`, seed cost,
and `budget.RATIO_SHIFT` produce the purchase rank key. This is exactly the
seed-list value used by `_candidates`, inspected before `plant_target == 0`
removes tomato from the day's wants.

| day | B target T/S/M | tomato quote now -> projected | units | raw stream T / S / M | budget key T / S / M |
|---:|---:|---:|---:|---:|---:|
| 10 | 0 / 3 / 1 | 66 -> 73 | 4 | 292 / 766 / 1,596 | 3,932 / 12,124 / 21,222 |
| 11 | 0 / 2 / 3 | 67 -> 74 | 4 | 295 / 768 / 1,288 | 3,112 / 8,970 / 21,824 |
| 12 | 0 / 2 / 2 | 68 -> 80 | 4 | 320 / 875 / 1,030 | 4,976 / 12,912 / 19,609 |
| 13 | 0 / 2 / 1 | 69 -> 82 | 4 | 328 / 895 / 906 | 6,840 / 16,322 / 20,236 |
| 14 | 0 / 2 / 3 | 71 -> 84 | 4 | 333 / 680 / 846 | 7,925 / 10,547 / 18,355 |
| 15 | 1 / 3 / 1 | 73 -> 85 | 4 | 340 / 750 / 614 | 12,144 / 16,496 / 14,848 |
| 16 | 1 / 0 / 0 | 74 -> 88 | 4 | 349 / 496 / 540 | 14,991 / 9,820 / 12,928 |

On every zero-tomato day, tomato ranks below both requested strawberry and
melon in raw stream return. It also ranks below them after B's network
multiplier and seed cost form the budget key. The frozen stop days were 12--14;
there tomato trails strawberry by 347--567 raw coins and melon by 513--710.
The stop condition therefore fires without needing a judgment about route or
terminal value.

The projection does see the rising market: tomato's modeled first-unit quote
is already 80 on day 12 and 84 on day 14, versus dawn quotes 68 and 71. The
issue is that four tomato units at those quotes remain less valuable under the
planner's own model than the competing strawberry and six-unit melon streams.
Adding that same maturity signal to the network would duplicate a signal whose
direction does not support the proposed allocation in this case. Day 16 is a
useful internal check: B requests tomato when its network-weighted budget key
finally exceeds both strawberry and melon, although the raw stream is still
smaller.

## Boundary and provenance

This is candidate-ranking evidence, not a hypothetical grant or counterfactual
outcome. It does not model the route, labor, future opponent actions, shared
market response, or terminal purse. It does establish that the specific
representation premise from the preceding research note is false here. The
episode may still contain another crop-allocation defect, but it is not shown
by feeding the existing first-yield value back to the product head.

The helper verifies replay SHA-256
`5f8cfbd958edc029b614f6d089e6ad499dd2c16a50da0550d41b64077b4c1449`,
the case receipt and macro snapshot, every source hash recorded by that
receipt, shipped B MD5 `7fcf39485bae65ee84171957c5843814`, all seven exact
macro rows, imported module origins, and complete plan BUY/PLANT counts. It ran
under `JAX_PLATFORMS=cpu` and exited 0 in 3.2 seconds.

- helper: `S/unitorder/tomato_maturity_economics.py`, SHA-256
  `185f1b0142fa530980c070fea7ad9530bb632bf340f03feadedc146ae2dc668f`
- JSON receipt/table: `S/unitorder/episode_108450468/tomato_maturity_economics.json`,
  SHA-256 `50c05f74f1f0b202d7204776aa6ff1a2666cd0089dfdf208077bad37dca95fea`
- CSV table: `S/unitorder/episode_108450468/tomato_maturity_economics.csv`,
  SHA-256 `f029be3472a3fd7353a167f8283d56acf6708578b163190f4ec4f38bae415d5b`

The ignored JSON and CSV remain preserved beside the replay. No evaluation
family was read or pooled.
