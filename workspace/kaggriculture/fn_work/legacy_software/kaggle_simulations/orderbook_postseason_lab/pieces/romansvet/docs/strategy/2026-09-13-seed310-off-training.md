# Seed310 OFF training completion

The second separate trajectory completed its prescribed ten generations on
2026-09-13. This establishes a valid final checkpoint, not improvement over B.
No checkpoint selection, trajectory pooling or submission promotion occurred.

Execution ran07:51:44.058052–09:48:40.030181Z,7015.972 seconds, within the
existing10800-second child/10860-second outer limits. Wrapper exit0 and helper
PID1130257 absent. The old SSH observation session59892 can linger after remote
completion; it is not evidence that training remains active.

All206 local manifest inputs and121 externally bound inputs passed the frozen
saved auditor. Peak GPU allocation was9702MiB across140276 samples, with maximum
sampling gap0.107017 seconds. Generation10 took1082.89 seconds, including the
scheduled absolute evaluation; no resume or retry was performed.

Root and Sol independently ran `audit_train_seed310.py` on the downloaded saved
evidence. Their outputs are byte-identical and PASS. Collection and extraction
verified the70-member archive, source immutability, wrapper completion and
member hashes; the expected remote source symlink remains preserved.

| Evidence | SHA-256 |
| --- | --- |
| Training manifest | b3fc988a126ce9b063dcc0c6fb4cfd198d5cb3b018afad1914feded69d125395 |
| Download archive | 9c403ce99b0afc5cec4a4bf6cec7574a954f5da881fac718ae3027aa831b0fdf |
| Execution | 2febccacac129f9d9fcde3e28a54f461784b3abda3e2087fc4317098459c6bfb |
| Training receipt | 14fb51dd6066fef04e76742ff9a5efdf8fc3355419180e5a7fcb4d95c7e77ffe |
| Root/Sol saved audit | 33efb07e601d381b4c3d1e7b3641d6402d1c33960df9cc9fbcf15a1e869cdf1b |
| Final theta file | 5fd10008a525fe5c56f514985b77d7b7e72300e02611ab6bc723ee776d0f9a9b |
| Final float32[6789] array | 92092f93139f9777c369c621aca95acb90e06e89630c9aef1c35f728dec9c582 |
| Final state | 8a87223259cfe494296072cd1aaae18dbe21b886fd46ae86ab47ce1dd6cbfab1 |

Evidence root: `S/unitorder/off_train_seed310_20260913`.
Candidate: `unitorder_off_seed310_g10`.
Its fixed final centre proceeds to the separate seven-family real-engine judge,
using the same424 keys/212 boards as seed309 and reporting each family separately.
No claim about beating B follows from training fitness or this audit.
