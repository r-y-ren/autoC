# Structural continuation — development only, no new release

Preserve root V9 and releases V9 / V10 / V10-R2. R2 source SHA256:
b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4
The acceptance target remains credible 2800 strength; no rating is inferred from local proxy wins.

Completed in this continuation:
- plan_screen: 1,464 valid full games, 60 raw-public-plan variants plus R2 controls.
- plan_extended: 576 valid full games on 12 further development worlds.
  plan02's initial 6/6 direct wins over R2 fell to 4/24 on expanded worlds; not promoted.
- livestock: 342 valid games, 16 causal post-opening allocation variants plus controls.
  Synthetic prefix/reset checks: 32 passed. No external win-count improvement.
- counter_pilot: 4 valid games; repeated again inside the subsequent screen.
- counter_screen: 144 valid full games. Market mechanics matched 180 randomized
  official one-turn cases, but the scenario policy did not improve match wins.
- ranch_screen: 104 attempts. Only 8 R2 controls completed normally;
  96 ranch candidates raised an empty-pasture None-counting error, not full valid games.

Partial / blocked branches:
- fix_ranches.py contains the correction and synthetic-check prefix, but the append
  creating a new job manifest was denied. Do not claim a corrected full match run.
- build_procurement.py is incomplete after its final write was denied; not executed.
- dispatch_helpers.txt is a standalone-controller draft; dispatch_projects.txt write
  was denied. There is no complete observation-driven takeover agent yet.

Additional exact public sources were downloaded, syntax-reviewed and extracted:
public_programs/farm2945.py and yield_v37.py. Their source hashes match the authors'
notebook assertions. Embedded literal model sources have no external I/O calls;
the optional V92_SELL_LIB setting is absent. No notebook setup cells were executed.
