# ROTBAND local cache audit and exclusion fix — 2026-09-12

The offline audit found 100 unique raw replay IDs outside the existing exclusion manifest and ROTBAND's 48 owned episodes: 48 root-level `S/ep_<id>.json` games involving our own submission, 47 TOP50 evaluation replays, and five SpaTaro/top-tier provenance replays. None was imported: own games are not independent support, and TOP50/SpaTaro data would pool evaluation provenance into training.

The gap was in manifest construction. `build_exclusions.py` previously covered tape artifacts, ID lists, town registries, and structured candidate metadata, but not raw-only replay caches. It now scans only explicit repository pipeline locations: root `S/ep_*.json`, TOP50 and SpaTaro episode caches, and BAND40/NEXT30/NEXTHIGH replay directories. It deliberately does not traverse arbitrary user replay directories and excludes `S/rotband/` itself.

Each exclusion is bound to the replay's embedded `info.EpisodeId`; embedded team names are also added to provenance exclusions. `test_exclusions.py` requires every raw pipeline replay to be excluded and every ROTBAND-owned episode to remain eligible. This changes selection eligibility only by enforcing the pre-existing policy that locally held/evaluation episodes and teams are unavailable to ROTBAND.

After regeneration the manifest contains 956 episode IDs and 449 team names, including 444 IDs bound from raw pipeline caches. All 48 ROTBAND-owned episode IDs have zero episode overlap. The stronger team-name provenance check flags 16 existing ROTBAND tapes whose selected team identity in `episodes.json` occurs in older raw caches: episodes 108094356, 108099298, 108099911, 108099726, 108100361, 108101761, 108094711, 108104856, 108104897, 108091965, 108103728, 108106163, 108106166, 108102339, 108105792, and 108096036. These are exact selected team names, not generic replay labels.

The coordinator chose strict enforcement. `verify_and_window.py` now separates fidelity from eligibility: `checksums.json` retains all 48 verified archived cuts so resumptions do not recut them, while `private_registry.json` contains only the 32 eligible schedules. `rejections.json` records the 16 rejected episodes, selected team name/ID, and reason. The partial audit reports `fidelity_verified=48 eligible_pool=32 rejected=16`; no source replay or tape artifact was removed.

Raw provenance parsing now decodes the top-level `info` object and requires valid `info.EpisodeId` and `info.TeamNames`. An expected pipeline replay with malformed provenance aborts exclusion generation. The regression test includes a malformed file whose unrelated outer `EpisodeId` must not be accepted.

Verification now requires both drawn and town success lines bound to the exact
selected episode and seat. An audit refuses to replace an archived replay or
tape hash if the underlying file changed, and retains old evidence even for
temporarily missing cuts. Tests reject wrong-seat logs, duplicate-mode logs,
and changes to each of the three hashes. Rechecking the actual corpus preserves
48 verified cuts, 32 eligible schedules and zero windows.

The picker supports `--max-requests 1` for a bounded retry after cooldown.
Accepted episode metadata remains append-only even when later team exclusions
invalidate a row. Mocked requests verify the one-request budget, immediate
429 stop, and retention of earlier accepted and rejected provenance.
