# Wide-crew season integration result

The isolated repaired loop passes the unchanged full-season test
`test_sim_matches_engine_with_a_wide_crew[1164543749]`. Root session45712
completed normally from20:05:40.404217Z to20:08:27.059219Z, 166.655seconds,
within its fixed1200second cap. The JUnit case took140.836seconds and records
one test, zero failures, errors or skips. Both frozen source and reference
engine binding markers are present.

Root37824 audited the saved artifacts without executing another game. All185
bound paths match, including all36 staged source modules and140 staged tests.
An independent Sol review reproduced the artifact and source hashes with no
mismatch. The audit is in `S/unitorder/wide_season_20260912.root_audit.json`.

- Execution SHA256: `49679a194c3ca5413e69981f7c3d078c36969758a7979da669b4fc8d81b1f40c`.
- JUnit SHA256: `01e163ed8eb1d5f4ce77f3810b57ccd395d0652d4ad359611c3fde33de8e8f12`.
- Log SHA256: `70a773696351a18c77e46afd2a22b9335dcba05de4ee6f2243d39d839cb86523`.

The fixed synthetic policy reaches at least12 hands. Both seats match the
engine at29 end-of-day boundaries and the final partial-day boundary for
money, market stock, land and shop counts, shed, seeds and all tile metadata.
Archived planner switches, including seed-room ON, were preserved.

This is a season integration result for the loop default. The test omits
hourly transitions, shop identities, worker positions/counts, hires today,
private inventories and insertion order. It does not establish full State,
action-tape parity, submitted B behavior, unrolled season behavior, GPU
performance or competitive gain. The next reviewed implementation will add
hourly State evidence before the separate tape and GPU gates. Production
source and submission payloads remain unchanged; top five remains unachieved.
