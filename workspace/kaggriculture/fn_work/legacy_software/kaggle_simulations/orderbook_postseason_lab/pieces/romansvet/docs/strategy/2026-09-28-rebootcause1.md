# REBOOTCAUSE1: why the remote 2x RTX 3090 host hard-rebooted twice on 2026-09-28

Host: user@remote-host (`remote-host`). ASRock Z490 Phantom Gaming 4 (BIOS P1.50, 2020), Intel i3-10300 (4C/8T, 65 W TDP),
125 GB RAM + 31 GB swap, 2x RTX 3090 (factory-OC boards: default/current power limit 390 W, max 480 W), driver 580.126.20,
kernel 6.8.0-1008-nvidia. Clock is UTC. No passwordless sudo (`sudo -n true` fails), so no dmidecode, pstore, BIOS event log or
power-limit changes. `user` is in group `adm`, so the full journal, `/var/log/syslog*` and `/var/log/kern.log*` were readable.
Raw command output: `S/rebootcause1/p1.log` through `p11.log`, plus the power traces `p9_power.csv` and `p10_power.csv`.

## Verdict

**The host lost power at the hardware level, most likely because the PSU tripped or sagged on a load transient when a second
heavy GPU job ramped up. Confidence is about 75 %.** The only competing explanation that fits the evidence equally well is a
mains dip or a failing PSU or board VRM. A physical check can tell these apart (see "What the user must do").

The decisive evidence has three parts.
1. **The log just stops.** The journal and rsyslog end in the middle of routine sshd lines (14:02:46 and 14:05:22 for boot -2,
   14:45:19 for boot -1). There is no shutdown sequence, no `Power key pressed`, no oops, panic, lockup, MCE, EDAC, AER,
   NVRM Xid or OOM line in either boot. `last -x` has no shutdown record for either boot.
2. **The box rebooted itself, which software cannot cause on this host.** `kernel.panic = 0`, `panic_on_oops = 0`,
   `hardlockup_panic = 0` and `softlockup_panic = 0`. No hardware watchdog is loaded (no iTCO_wdt, and systemd
   `RuntimeWatchdogUSec = 0`). A kernel panic or hang on this box would freeze it until someone pressed a button. Instead, a new
   kernel started 30-45 s after the last log line both times: 14:05:58 and 14:46:06, derived from the kern.log `[ 9.9 s]` offsets.
   That timing means a hardware reset (PWR_OK drop or power loss, with the board powering back on) rather than a software fault.
3. **Both crashes happened while a second heavy GPU job was starting.** Both GPUs were already busy, and the CPU was
   saturated (see the timeline below). The host ran single-GPU or steady dual-GPU work for hours before each crash without
   trouble. Each crash came within seconds to a few minutes of a new training job reaching the GPU. RTX 3090s are known for
   millisecond power spikes of about 1.5-2x board power, that is 550-750 W per card at a 390 W limit. `nvidia-smi -pl` does
   not catch these spikes.

## Timeline (UTC, 2026-09-28)

| time | event | source |
|---|---|---|
| 09-27 onwards | rlfast1 PPO `run2s` learner on **GPU0**; rlfast1 `run3g1` learner on **GPU1**; esband1 run3 ES with CPU workers | trainfix4 doc, S/esband1 |
| 11:05-13:58 | BCBODY4 train3.py rungs r4a/r4b/r4c run one at a time on **GPU1**, alongside the trainers above. No crash. | S/bcbody1/checkpoint.txt |
| 12:03:36 | kernel: `nvidia 0000:02:00.0` (GPU1) device open | journal boot -2 |
| ~13:58 | r5a0 (train3 from scratch, 100k steps, 47 ms/step) starts on **GPU1** | bcbody1 checkpoint |
| 14:02:46 | r5a1 (train3, warm start) launched for **GPU0**. It first spends about 153 s loading data into RAM on the CPU. | bcbody1 checkpoint, out5a1_dead.log |
| 14:05:22.41 | kernel: `nvidia 0000:01:00.0` (GPU0) device open. **This is the last kernel line of boot -2.** | journal boot -2 |
| 14:05:22.8 | r5a0 writes its step-12000 checkpoint on GPU1 | out5a0/*.npz mtimes |
| 14:05:24.54 | r5a1 log: `warm start out4c/params_best.npz`. JIT compilation and the first GPU0 training steps follow. | out5a1_dead.log mtime |
| **~14:05:25-14:05:45** | **CRASH 1.** State at the time: GPU0 = rf2s PPO + r5a1 ramping; GPU1 = rf3g1 PPO + r5a0 BC at full load; CPU = ES workers. | new kernel at 14:05:58 |
| 14:06:05 / 14:08:24 | boot -1 starts; r5a1 is relaunched on GPU0 alone | journal |
| 14:08-14:21 | r5a1 runs **alone on GPU0** for 787 s. Survives. | out5a1.log |
| ~14:35-14:37 | r5a2 is launched on GPU0 (102 s data load), then trains at about 19 ms/step (GPU0 at 100 %) | out5a2.log |
| 14:37:50 / ~14:40 | BCSIM1 PPO is launched and relaunched on **GPU1**: 6 rollout workers (CPU + batched GPU), then the learner | bcsim1 checkpoint |
| 14:45:05.96 | r5a2 writes its step-18000 log line and checkpoint (**last file write**). The next line was due at about 14:45:44 and never arrived. | out5a2.log |
| 14:45:19.09 | last journal line (routine sshd) | journal boot -1 |
| **~14:45:20-14:45:50** | **CRASH 2.** State at the time: GPU0 = r5a2 at 100 %; GPU1 = BCSIM1 PPO learner starting; CPU = PPO rollout workers. | new kernel at 14:46:06 |
| 14:46:13 | boot 0 starts; up ever since (checked at 17:08) | `uptime` |
| 17:05:03-17:06:40 | passive 100-250 ms sampling while r5a3 ramped on GPU0 with the GPU1 grid eval running: GPU0 peaked at 330 W, GPU1 at 217 W (about 550 W of GPU in 100 ms averages). Survived. The 14:05 state was heavier than this: two trainers plus a BC job per GPU. | p9/p10_power.csv |

## Evidence per hypothesis

| hypothesis | status | evidence |
|---|---|---|
| **PSU / power transient (OCP/OPP trip or 12 V sag -> PWR_OK drop)** | **LIKELY (~75 %)** | The log stops dead. The machine restarts itself 30-45 s later, which software cannot do here (panic=0, no watchdog). Both events happened with both GPUs loaded and a new heavy job ramping. Worst-case sustained budget: 2 x 390 W (GPUs) + ~90 W (CPU PL2) + ~60 W (board, 4 DIMMs, NVMe, fans) ≈ 930 W. Millisecond transients can exceed 1.2 kW. The PSU model and wattage cannot be read without physical access. |
| Mains dip / house wiring | possible (residual) | Same signature as a PSU trip. It would not correlate with GPU ramps, yet both events did. |
| Kernel panic / hard lockup | **refuted** | No oops, panic, soft/hard lockup or hung-task lines. With `kernel.panic=0` and no watchdog, a panic would have frozen the box instead of rebooting it. |
| OOM | **refuted** | No `oom-kill`, `Out of memory` or `Killed process` lines in boots -2, -1 or 0. OOM kills processes, not hosts. 117 GB is available now; each train3 job holds about 3.7 GB RSS. |
| GPU fault (NVRM Xid, fallen off the bus) | **refuted** | There are zero NVRM Xid lines in any boot. A GPU fault kills the CUDA process and logs an Xid; it does not reboot the host. HW Power Braking and HW Thermal Slowdown counters are 0 on both GPUs in the current boot. |
| GPU thermal | **refuted** | The GPUs run at 31-63 °C under load now (slowdown 95 °C, shutdown 98 °C). Thermal slowdown counters are 0. A GPU thermal shutdown would drop the GPU, not the host. |
| CPU thermal (THERMTRIP) | unlikely, unverifiable | `coretemp` is not loaded (thermald: "No coretemp sysfs"), so CPU temperatures are unreadable without root. The CPU is a 65 W part. THERMTRIP powers the board off and it normally stays off; it does not come back in 30 s. |
| Disk | **refuted as the reboot cause, but a live risk** | `/` is at 97 % (865 G used, 32 G free), with no I/O or ext4 errors. A full disk crashes jobs, not the host. |

Other observations:
- Four earlier boots also ended without a shutdown record: 08-08 13:57, 08-29 13:43, 08-31 01:23 and 09-01 23:20. Those gaps
  were 10-30 min, so they were probably manual power cycles or outages. That is a different signature from today's automatic
  restarts within 45 s, but it shows this box has lost power before.
- The host had run steady dual-GPU loads for weeks (for example DUAL234 on 09-18, and rf2s on GPU0 with rf3g1 on GPU1 since
  09-27). The trigger therefore looks like the start of a job on top of existing load, not steady dual-GPU load as such.
  That is what you would expect from a transient trip rather than an average-power limit.

## Recommendations

Without sudo, starting now (coordinator rules):
1. **One ramp at a time.** Never start a GPU job while the other GPU is at full load unless the host has run that exact pair
   before. Keep the heaviest pairing (BC train3 on one card plus a PPO learner on the other) off until the power limits below
   are set.
2. **Prefer one heavy trainer per host.** Put BC training (train3) on one remote GPU and run only light batched rollouts or
   evals on the other. The 17:05 pairing (train3 on GPU0 plus grid eval on GPU1, about 550 W of GPU) survived; the
   14:05 pairing (two trainers plus BC per GPU) did not.
3. **CPU thread cap.** Keep total rollout and ES worker processes at 8 or fewer (the CPU has 4C/8T; load average reached 26).
   This helps throughput more than power, because the CPU is only about 90 W.
4. **Disk.** Free space on `/` (97 % full) before the next large data rsync.

What the user must do (needs sudo or physical access):
1. **Cap the GPUs and their transients.** Clock locking is what actually suppresses the millisecond spikes; the power
   limit only acts on about 100 ms averages. Suggested settings:
   `sudo nvidia-smi -i 0,1 -pl 300` and `sudo nvidia-smi -i 0,1 -lgc 210,1700`
   (a 3090 loses roughly 5-10 % of ML throughput at 300 W). These settings reset on reboot, so persist them with a root
   `@reboot` cron entry or a systemd oneshot. Persistence mode is already on.
2. **Read the PSU label** (model, wattage, age). If it is under 1000 W, or it is an older unit with sensitive OCP (for
   example a Seasonic Focus/Prime-era design), replace it with an ATX 3.0 unit of 1200 W or more. Until then, keep the caps
   from step 1 in place.
3. **Check the cabling.** Each GPU 8-pin connector should have its own PCIe cable from the PSU, with no daisy-chained
   pigtails. The factory-OC 3090s probably take 2-3 connectors each.
4. **Optional:** put the host on a UPS with event logging. A mains dip will show up in the UPS log, while a PSU trip will not,
   so this settles the residual hypothesis. Also check the BIOS "Restore on AC power loss" setting for context.
