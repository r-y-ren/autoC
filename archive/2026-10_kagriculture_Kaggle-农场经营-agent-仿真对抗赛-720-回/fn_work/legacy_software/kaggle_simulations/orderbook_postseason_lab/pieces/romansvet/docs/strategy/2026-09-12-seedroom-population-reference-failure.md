# Population audit refused by original ON reproduction check

The pair finished at 16:05:31Z: ON exit 1, OFF exit 0. Root SSH session 18616
is terminal, both timeout/probe pairs are absent, and both GPUs are idle.
No optimizer ran. All results, logs and exit files are preserved locally at
`S/seedrank/seedrank_pair_20260912/`; large NPZ files remain ignored by Git.
Remote staging resolves through symlinks to `/home/user/kagg3/artifacts/`.

ON's mean win score is 0.6280547380447388; the original first-generation
reference is 0.6280192732810974. Best win score matches 0.7016128897666931.
Raw integer outcomes yield 637,983 half points over 507,904 episodes, versus
the original mean's implied 637,947: +36 half points, equivalent to 18 wins.
This is an outcome difference, not merely mean-reduction rounding.

Root verified every saved array hash and all remote/local NPZ/receipt/log
SHA-256 values. The current pair has identical source/helper/config, B, window,
tapes, mask, eps, candidate and complete episode/fitness-weight fingerprints,
and identical recorded runtime/backend/device kind. Nevertheless the required
original-ON reference failed. `compare.py` correctly writes `valid:false` and
refuses before reporting rank/gradient comparisons. No decision under dfeae9e
is valid yet; the original strict check remains intact.

Independent review identified evidence upstream of the arm toggle. The original
training versus current ON initialization differs in 20 of 124 rounded liveness
rows (sum absolute logged difference 623 coins, maximum 116). Current ON versus
current OFF initialization differs in 19 rows (sum 855, maximum 76), although
both initializations run the archived ON setting before selecting a mode or
clearing caches. Root independently reproduced these counts. Thus capture
placement, the later toggle and later cache clearing do not explain this prior
variation. Numerical/process/device reproducibility needs investigation; the
precise cause is not established by rounded logs alone.

The next bounded diagnostic is ON-only on one GPU: capture exact raw inputs
and money during actual initialization, repeat that same 992-row liveness
probe with its cached executable, then repeat after clearing caches. Verify
raw-input identity and unchanged theta/optimizer counters throughout. Cached
versus retraced differences can distinguish execution from compilation effects
without another 4096×124 population. Staging/review is in progress; no new GPU
run is authorized merely by this report and no expected score is being changed.

Evidence: `reference_failure_audit.json`, `comparison.json`, both receipts,
logs and raw NPZ arrays in the local pair directory. Production B and submitted
payloads remain unchanged. This is not a training or promotion result.
