# MELONVETO_POST — re-apply the flooded-melon veto after ACTIONRL

2026-09-21. `MELONVETO_POST_ON` defaults OFF. When ON, `_melon_veto` runs a
second time immediately after `_residual_override`, reusing
`MELON_VETO_FLOOD_K = 60`; the existing pre-head veto is unchanged. The action
RL gate forwards the environment switch into the engine switch string. A
zero switch gene selects that same OFF arm, and a focused pin proves the OFF
plan is byte-identical to `_pin.SHIPPED`.

Diff summary:

- `src/kagg3/core/plan.py`: declare the default-OFF switch and apply the
  existing veto immediately after the residual merge; append its gene without
  renumbering the preceding switch catalogue.
- `src/kagg3/core/policy.py`: widen the switch-gene block from 18 to 19.
- `S/actionrl/gate.sh`: forward `MELONVETO_POST_ON` when present.
- `tests/test_melonveto_post.py`: pin OFF identity and the post-head ordering
  and effect.
- `tests/test_geneswitch.py`, `tests/test_widepick.py`: update catalogue and
  layout assertions for the appended gene.

Proof:

    proof board day=10 melon_book=I0+60 ripe=0 money=200000 base_melon=1
    proof melon target pre_veto=0 after_head940=4 post_switch=0 K=60

Gates (CRN-paired, two purses, board = seats averaged):

| leg | dmargin | se | t | dours | dtheirs | bett/wors | win% base->cand | flips |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| BAND3 | +145 | 71 | +2.02 | +1 | -144 | 56/36 | 54.2->54.2 (65->65) | +0/-0 |
| BAND2 | +5 | 88 | +0.06 | -103 | -108 | 118/109 | 75.1->76.4 (175->178) | +9/-6 |

Validation: `JAX_PLATFORMS=cpu .venv/bin/python -m pytest -q tests/_pin.py
tests/test_melonveto_post.py` — 2 passed.

## Verdict

**NO SHIP** under the bar: BAND3 +145, t 2.02, Δtheirs −144, t −2.80, wins 65→65, flips 0; BAND2 +5, t 0.06, Δtheirs −108, t −2.24, wins 175→178, flips +9/−6. The switch stays **OFF**. A ~100–150 coin denial against ~10k loss margins is not a rating lever. This axis is **CLOSED** unless a larger-K variant shows OOS flips.
