# tests/stale — dev-feature tests parked by SRCSYNC1 (2026-09-27)

src/kagg3 is byte-equal to the uploaded vrp10_esw tarball (MASTER RULE). These tests exercise
switches/modules that exist only on dev branches (CARE_RIDE, SLIVER, NONV_THETA, RL_ACT, Q4 relay,
book_*, endgame, resale, ...). They are NOT collected (no conftest here, `tests/stale` is not on the
named-test list). When a feature is ported to master src for a ship, `git mv` its test back to tests/.
