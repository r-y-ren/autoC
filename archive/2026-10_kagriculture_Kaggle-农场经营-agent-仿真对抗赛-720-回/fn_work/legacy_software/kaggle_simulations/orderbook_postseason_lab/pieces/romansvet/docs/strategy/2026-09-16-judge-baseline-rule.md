# Judge rule: "B" is no longer the six-switch string (2026-09-16)

**Standing rule.** Since master d3716e6 (upload 56277270) the plan ships `LOT4_ON = True`,
`LOT4_TURN = 17` and `SELL_SLOT_PRIORITY_ON = True` as module defaults. The six-switch
`BASE` string in `S/combo2/run_all.sh`

    OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True,brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True

therefore no longer produces B. It produces the shipped PAIR (B + LOT4@17 + SLOT-PRIO).
Any leg that wants the pre-09-16 baseline must append

    ,LOT4_ON=False,SELL_SLOT_PRIORITY_ON=False

or it silently measures the pair against itself (V45LEG2: `l2_B` and `l2_ctl` were
coin-identical on 88/88 rows before the fix; `docs/strategy/2026-09-16-v45leg2.md` §Gotcha).

Consequences:

* **Increments over the pair** (the §115b object since COMBO2) need no change: CTL = BASE, ARM = BASE + the new switch.
* **"vs B" reads** (pop-shift tracking, retention history, any table with a B column) must use
  `BASE,LOT4_ON=False,SELL_SLOT_PRIORITY_ON=False`. Label it `Bold` / "pre-pair B" in csv names and tables.
* **Banked control rows**: `S/lossflip/*c2_combo*` are the PAIR; the older `*_B*` / `brv45_ident`
  rows are pre-pair B. Do not mix them in one paired difference.
* The same applies to every switch that ships in future: the moment a switch's default flips to
  True, the baseline string must gain its `=False` override. Add the override to this file when it happens.

Baseline history this affects (band-rated opponents): B +2,045 (09-11 NEXTHIGH) → +1,103 (09-15
V45LEG) → −514 (09-16 V45LEG2 BAND). Those three numbers are all true pre-pair B and comparable.
