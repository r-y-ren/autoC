# Complete-plan branch fixture

`S/planselect/branch_fixture.py` provides the minimal offline plumbing needed to
compare complete feasible day plans from one fixed development dawn state. It is
a correctness fixture, not performance evidence.

## Frozen fixture

- State: the first row of `S/isearch/boards_dev.json`, tape `107463847`, seed
  `4674845`, controlled seat 1, dawn of day 5.
- Base: unchanged arms-next macro and `build_day` plan.
- Alternative: the predeclared ISEARCH `cmpp1` edit, `compact + 1` on day 5,
  clipped to planner `DIST_MAX`, with every other macro field unchanged.
- Branch control: both candidates use the same dawn state, opponent action tape,
  and end-of-day random word. A duplicate base branch is included.

The first predeclared alternative was ISEARCH `crw59p1` (`crew_target + 1`). Its
NumPy plan was byte-identical to the base plan, so it was discarded on the input
side. Its target was inspected and was also equal, but did not cause the switch.
The replacement `cmpp1` candidate was frozen before its target was generated.
The compact reconstruction of that first run is preserved at
`S/planselect/branch_fixture_crw59p1_identity.json`.

## Checks and result

The fixture independently decodes the base macro with NumPy and JAX and asserts
fieldwise equality. It builds frozen NumPy plans, asserts exact NumPy/JAX array
equality for both candidates, then injects each NumPy plan into the unchanged
one-day runner. The injected base result equals an unmodified `advance` call,
and the two duplicate base branches are exactly equal.

In the saved run, base and alternative plan SHA-256 values are respectively
`211a56031f1cab72cad80d7eab7bcd3b69960385ea334e1df2bf25a4c24b66df`
and `23863ccf197f3fabe7d7973e22fce8a8f38c39ea5d3caad79a5d917f5595e496`.
They differ in 14 array elements. Their resulting full-state hashes differ, but
both one-day summaries are own cash 870, opponent cash 786, cash margin 84,
eight own shed units, and own shed spot value 648.

`S/planselect/branch_fixture.json` records current-observation fields, macros,
and plans under `input_only`; full hidden-state, opponent-action, RNG, tape, and
seed identities under `audit_provenance_label_generation`; and resulting values
under `target_only`. It also records input-file hashes and the arms-next Python
source-tree hash `e2fe0a7dff6f29359e93bcd8d7ed71f1969287ce4351cb96dff60e811d29b158`.

The equality of the immediate cash and shed summaries is not evidence that the
plans have equal value. One-day targets exclude downstream crop returns. This
fixture only establishes that a future selector can construct distinct complete
plans from permitted current inputs and generate controlled, reproducible labels
without leaking label-generation provenance into gate features.
