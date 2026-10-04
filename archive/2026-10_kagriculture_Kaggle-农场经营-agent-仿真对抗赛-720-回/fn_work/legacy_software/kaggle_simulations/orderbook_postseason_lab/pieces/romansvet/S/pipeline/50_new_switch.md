# 50 — how to add a new knob and judge it

A new idea enters the ledger as a **free module float** (or a free switch), never
as a code change to the shipped path. At its default the traced program must be
**byte-identical** to what ships; the knob is flown by a module override only.
Two shipped examples to copy: `brain.HERD_TILT` and `plan.MELON_PLATE_TILES` /
`MELON_PLATE_DAY`.

## 1. Declare it — default OFF, guarded by a trace-time `if`

`src/kagg3/core/brain.py:835`:

```python
# Guarded by a trace-time Python `if`, so at the default 0.0 the two lines
# below are the shipped graph character for character [LAW, as HERD_RAMP].
HERD_TILT = 0.0
```

`src/kagg3/core/plan.py:1423`:

```python
# `MELON_PLATE_TILES = 0` is OFF and is read at TRACE time, so the guard is a
# Python `if` and the expression the planner builds is character for character
# the one it builds today (`tests/test_melon_plate.py`).
MELON_PLATE_TILES = 0.0

#: First (and only) day the plate plants on. Read only when TILES > 0.
MELON_PLATE_DAY = 0.0
```

and the read site is an `if` that is **false at trace time** when the float is 0:

```python
if melon_plate_on():            # `float(MELON_PLATE_TILES) > 0.0`
    macro = _melon_plate(xp, view, macro)
```

```python
if HERD_TILT:                   # falsy at 0.0 -> the else branch is the ship
    animal_share = sig(head[6] + HERD_TILT * xp.maximum(obs.day - 12.0, 0.0) / 10.0)
else:
    animal_share = sig(head[6])
```

**Why a float and not a gene switch.** `plan.SWITCH_GENES` is 18 names wide and
the shipped layout is 7,692 floats. A 19th column is a **layout move**
(7,692 → 7,725: 32 hidden + bias) which un-pairs every banked CRN row in the
ledger. A free float has no column, no `N_SWITCH_GENES` bump, no layout move,
and every banked pairing stays CRN.

## 2. Pin the byte-identity — `tests/test_melon_plate.py` is the template

Three assertions, all cheap:

```python
def test_zero_is_the_shipped_default():
    assert float(P.MELON_PLATE_TILES) == 0.0
    assert not P.melon_plate_on()

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS[:2])
    assert got == PIN            # digests taken off the PRE-SWITCH master tree

def test_off_never_calls_the_rewrite(monkeypatch):
    ...                          # monkeypatch the rewrite, assert it is never entered
```

plus an **opt-in** whole-game coin pin, off by default because two engine games
are minutes, not milliseconds:

```python
@pytest.mark.skipif(os.environ.get("KAGG3_MELONPLATE_COINS") != "1", reason="opt-in")
def test_off_two_boards_are_coin_exact(): ...
```

Run **that one file** — never the suite, `pytest -q tests` OOMs this box:

```
cd /mnt/e/_work/kaggriculture3 && JAX_PLATFORMS=cpu .venv/bin/python -m pytest tests/test_melon_plate.py -q
```

The test file must start with `import _pin; _pin.bootstrap()` **before** numpy
and pytest, so `kagg3` is imported out of the tree the test is measuring.

## 3. Fly it — `SW_EXTRA` appends to the ESR string

`judge.sh` builds `SW=${SW:-$SW_BASE}${SW_EXTRA}`, a raw string append, so
`SW_EXTRA` **must start with a comma**. Names are `plan` constants unless
prefixed `brain.`:

```
SW_EXTRA=,brain.HERD_TILT=-1.0
SW_EXTRA=,MELON_PLATE_TILES=6,MELON_PLATE_DAY=20
SW_EXTRA=,brain.HERD_TILT=-1.0,MELON_VETO_FLOOD_ON=True
```

## 4. `plan._sw` precedence — the LAW you must not fight

```python
cur = bool(globals()[name])
if cur != SWITCH_GENE_DEFAULTS[name]:
    return cur                  # a constant moved off its SHIPPED value is a
                                # MANUAL OVERRIDE and wins outright
...                             # only otherwise does the theta's gene column rule
```

Consequences, and they are the whole reason the judge's switch string looks
redundant:

* Naming a gene-switch at its **shipped default** in the switch string is **not**
  an override, so **the candidate theta's GENE BLOCK rules** — which is how an ES
  checkpoint is meant to be flown. That is the *gene-block rule*.
* Naming it at anything else pins it against any theta, which is how a paired
  A/B runner isolates one switch.
* A **zero gene column is the shipped default**, which is what makes a padded
  older theta the shipped package exactly (`pad_theta.py`).
* "The gene block carries EVERY shipped switch": `N_SWITCH_GENES` is **18** today
  (`SWITCH_GENES[17] = WIDE_PICK_FREE_ON`, added with WIDEPICK2, layout
  7,659 → 7,692). When a free float finally SHIPS as a switch it becomes column
  18, `N_SWITCH_GENES` goes to 19 and the layout moves — an ES restart, not a
  free change. Free floats exist precisely to postpone that.

## 5. Judge it

```
# the tape legs + the bar
WORKERS=4 bash S/pipeline/20_judge.sh myknob_v1 S/winjudge/ship7692/theta7659.npy
# ...but 20_judge.sh judges a THETA.  To judge a SWITCH on the shipped theta,
# call judge.sh directly with SW_EXTRA, the way every knob in the ledger was:
LEGS=hiband WORKERS=4 SW_EXTRA=,MYKNOB=0.5 bash S/winjudge/judge.sh myknob_v1 S/winjudge/ship7692/theta7659.npy
LEGS=band2  WORKERS=4 SW_EXTRA=,MYKNOB=0.5 bash S/winjudge/judge.sh myknob_v1_b2 S/winjudge/ship7692/theta7659.npy
.venv/bin/python S/winjudge/report_pool511.py myknob_v1 ship7692 myknob_v1_b2 ship7692 \
  | tee /tmp/r.txt && .venv/bin/python S/pipeline/verdict.py /tmp/r.txt --bar ship
```

And if the knob touches the **opening or the order book**, it is not believed
until it clears the live clone, because a tape cannot re-plan:

```
WORKERS=4 bash S/pipeline/25_clone_leg.sh myknob_v1 S/winjudge/ship7692/theta7659.npy
```

## 6. Bar

`Δtheirs ≤ 0` **and** pooled `t ≥ 3` **and** net board flips `> 0`.
Margin without flips buys no rating — the ladder is Bradley-Terry over board
WINS. Write the result to `docs/strategy/<date>-<name>.md` and append one line
to `docs/strategy/BUILD-STORY.md` **whether it ships or is rejected**.
