# Forward vacancy on twelve public Candidate-B replays

## Result

The outcome-blind public replay census finds **6 deterministic seed-only route
opportunities among 46 positive-cash first-sale days** (13.0%).  All six
selected targets are reused by unchanged B
before the end of the injected melon's ten-day horizon.  The any-target upper
bound is also zero: none of the alternative route-feasible targets remains
vacant for the horizon.

This corpus is separate from H30 and is reported by itself.  It contains the
same first twelve metadata-selected Candidate-B public replays named in
`2026-09-12-postlot-feasibility.md`.  Selection is the first twelve eligible
`S/ep_*.json` files in sorted path order; the helper asserts the frozen episode
list so later cache additions cannot silently change it.  It never reads
`replays/` or user replays.

Cache-provenance limitation found in the subsequent fertilizer audit: ten of
these twelve files belong to the earlier LOSS10-selected cache. Selection in
this helper ignores outcomes, but that does not make the underlying cache an
unbiased ladder sample. Treat this as a fixed convenience corpus; see
`2026-09-12-fertilizer-premise-correction.md`.

The six chosen targets are first used after lags of two days (three), three
days (one), and five days (two).  Four become STRAWBERRY and two MELON.  Each
opportunity belongs to a different episode: six of twelve episodes contain a
route opportunity, and zero contain a forward-vacant target.  This is a fixed,
descriptive corpus rather than a random sample; no confidence interval is
claimed.  With only twelve episodes, one episode is 8.3 percentage points of
corpus incidence.  The result rejects no fixed prevalence threshold.  It does
show that the current deterministic target rule has found no additive land
capacity in either this public mechanism corpus or the separate H30 mechanism
audit.

## Scope and correction

The cash scope exactly matches the earlier census: days 1–6, the first daily
SELL after hour zero, and positive net cash from the observation before that
replay row to its resulting observation.  This reproduces 60 sale-days and 46
positive-cash rows.

The route calculation now matches `S/postlot/runtime_patch.py` where replay
state permits:

- movement distance is Manhattan distance and may cross LOCKED cells;
- a target must be exactly null or `kind: WEED` and cannot be reserved by another
  remaining non-move unit action;
- the start is the exact position before a trailing all-PASS suffix;
- capacity pays movement, optional DIG, PLANT, and immediate WATER;
- the chosen target is first by unit, then distance, x, and y.

The prior conservative route helper reported 19/60 because it used a different
geometry model, did not reserve all remaining work, and did not charge WATER.
The new 6/46 count is the relevant route count for the corrected hook, with the
positive-cash denominator shown explicitly.  It remains an upper bound:
replay row alignment may omit the runtime's current BUY-turn unit reservation.

Replay actions substitute for the cached current-day plan in this OFF-policy
diagnostic.  The result does not prove that the runtime would have enough
settled money, satisfy its exact seed-balance condition, settle the purchase,
or fire on any of these rows.  Future vacancy is retrospective mechanism
evidence; a submitted agent cannot read it.

## Decision consequence

Do not spend an engine evaluation on a forward-vacancy post-sale variant from
these data.  The measured route coverage is small, and observed forward-vacant
coverage is zero with substantial uncertainty.  A prospective proxy would
have to use only current and past permitted state.  Measure its precision and
coverage against this replay label, separately on each independent corpus,
before implementation.  Target reuse establishes displacement risk; it does
not isolate the seed cost, route perturbation, replanning, and shared-market
effects seen in H30.

## Reproduction and input identity

```bash
JAX_PLATFORMS=cpu .venv/bin/python -m pytest -q \
  S/postlot/test_forward_vacancy_public.py
JAX_PLATFORMS=cpu .venv/bin/python S/postlot/forward_vacancy_public.py
```

The helper prints row-level evidence, per-episode opportunity counts,
limitations, and these SHA-256 identities:

| input | SHA-256 |
|---|---|
| `S/ladder2/ep_56161192.json` | `5349ccf6cebc8ef8314209172bd91a9707ff58116c5eb18dd7a2576481066171` |
| `S/ep_107764944.json` | `c56dffd80b47a8d3ce37c69da4a1e03b37b6b5dbda58426be53a867dfc450ce0` |
| `S/ep_107766829.json` | `227d07d151006eead472e08129ddfb950daa06cf8ca0889bbcfb8bd712f4b1df` |
| `S/ep_107769126.json` | `a6ba557a33040f8e1bd8d10db3ff0a4b94b3c6cf2eca8495f66db81a8709b1e8` |
| `S/ep_107769991.json` | `00ba4223e7b76883cba2c1a15aadaf41875e33fddd7420c6a019234c9c47994a` |
| `S/ep_107771992.json` | `30a80115b8fa9756554eecb76436d647005f585bd21d2110893ab10369df63d7` |
| `S/ep_107777972.json` | `b512eca5c9aa2c851ee71dc40fb693c4b262173457e331c1840a30bf9cc8c052` |
| `S/ep_107779009.json` | `79a1743a13c1f7557525bca4b8c0227a522a1369d6c7828e81c7ed267e12fa02` |
| `S/ep_107779976.json` | `3f928259b73bbaf23ac93325ebc199879b96c18a4ef0f6dab04fe75157794201` |
| `S/ep_107780983.json` | `09bc7ca1a9cbd4c7f4f16276f2d49ce89abafef16ed1a31577d7a813d438c609` |
| `S/ep_107781955.json` | `2f44433be2702919387d0324ff53ca5ae27e9dac08c0caa10a11d51a4f1f0fe2` |
| `S/ep_107786955.json` | `a8a9d0088dd6a0da202360305a57aa8fae783cc9ca6a091d3322e3223fefa0d3` |
| `S/ep_107787963.json` | `6065741eeabe9425880e766bcb265cc6ee73fc13be2a1ac5f9152a49171089c2` |
