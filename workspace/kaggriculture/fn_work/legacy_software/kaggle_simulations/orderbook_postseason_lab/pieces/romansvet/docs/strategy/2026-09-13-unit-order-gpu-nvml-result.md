# GPU qualification passed; loop selected

The new four-arm qualification completed2026-09-12T22:48:41.807289Z after
2194.066737seconds, within the3660+kill10 cap. Remote wrapper exit0 and all four
known helper processes absent; both GPUs independently observed idle1MiB.
The original SSH tool handle92254 has not returned despite authoritative remote
completion. Do not interpret that transport handle as a live GPU job or rerun it.

Root61187 saved-only auditPASS and independent Sol saved-only auditPASS. Both
audit files are byte-identical SHA94fd559b. All155bound files, source/config/
runtime identities, full cold/steady state, key/RNG/slot carry, zero updates,
36raw arrays, exact repeats and992-to8192 indexed equality pass. Every arm's
outputs.npz has the same SHAa1379161. No old refused arm contributes evidence.

| Arm | Peak process MiB | Maximum monitor gap, seconds | Warm8192 median, seconds |
| --- | ---: | ---: | ---: |
| loop-1 | 4962 | 0.057651391 | 10.891107951 |
| unrolled-1 | 5030 | 0.060531989 | 11.139542925 |
| unrolled-2 | 5030 | 0.057495876 | 11.132814874 |
| loop-2 | 4962 | 0.068778615 | 10.903537507 |

The frozen comparison selects **loop**. Unrolled geometric advantage is
-0.021918913424396447, so it does not satisfy the>=5% improvement rule.
Within-variant repeatability passes. The selected pair's conservative
evaluator-only ten-generation projection is7171.7684029724915seconds<=9000.
The reviewed loop overlay remainsb5aeeb2c unchanged.

This qualifies the ON repeated-row evaluator only. It does not measure a real
perturbed population or full generation throughput, establish an OFF result,
perform training, or demonstrate policy improvement. Next is exactly one selected
shipped/OFF confirmation, then guarded fresh training and separate-family judging.

Evidence directory: S/unitorder/gpu_qualification_nvml_20260913.

| Artifact | SHA256 |
| --- | --- |
| execution.json | b16a4285d9fa92c9c030bf04176caed0e2b37094fc44a6c505dcc82e6e914b3e |
| root_saved_audit.json / sol_saved_audit.json | 94fd559bfd8e087be6cb8be872831ffbdb87c7c8adfc40f84fdd647283fadc2d |
| loop-1/receipt.json | 161e5caf11de14a572169b9cffce179633b0be27bdb6180157d6e78ec63da4ec |
| unrolled-1/receipt.json | 8d26aa165911b92e9f3b827b2f273fb876cf10dacbc3d116fcf1ef68fd1737e6 |
| unrolled-2/receipt.json | 0e1202aa98a544c84cc0d6157a00401220e6269f4673832730f892106bacb372 |
| loop-2/receipt.json | d20dfba998146d309a9e771ef70849a38074151a358b015843c4f04bcab80bea |
| each outputs.npz | a1379161d4586a342f3d88460a6201ade6a590b8598802c362eaef58392ef956 |

Original execution manifest888b4e2f remains immutable. Post-execution auditor
3060e608 was independently reviewed and committed34b198b before auditing, with
separate audit-planb3985f74. This distinguishes audit provenance from the original
execution; it does not rewrite the execution manifest. All raw files, arm logs,
monitorJSONLs and wrapper sidecars are downloaded unchanged. The original v2
cadence refusal is preserved separately. No pooling, promotion, production edit
or upload. Topfive remains unachieved.
