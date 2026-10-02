# Hourly wide-crew parity passes after a preserved audit import failure

The repaired loop matches the locked reference engine throughout the fixed
wide-crew seed1164543749 season. Both players' actions and720 canonical state
frames match, covering719 turns,29 EOD transitions and the last partial day.
The engine reaches16 hired workers. Both terminal balances are exact:
[66477,61281]. Direct and instrumented simulator states agree across all27
fields at all31 saved boundaries.

The single game diagnostic, committed inff3393e, ran20:28:42.961054Z to
20:33:08.063731Z in265.103seconds against a fixed1200second cap. Root82935's
child exited0 and the helper wrote PASS. Its original launcher then exited1:
the pure evidence validator loaded `core/ops.py` outside a package, while that
file's import-time schedule check uses `from .. import spec`. This was a
validator import failure after the raw evidence had been saved.

All original outputs and that failed execution remain unchanged. A new
package-context adapter was independently reviewed and committed inac4a283.
Its regression reproduces the original import failure and checks the exact
frozen module's schedule validation in the repaired import context. Root82857
then ran only the unchanged saved-evidence validator under a60second cap,
exit0/PASS. An independent Sol audit using normal staged package imports
also returned PASS. Neither audit reran an engine or simulator.

The audits verify all188 original bound files,168 raw arrays with exact shapes,
dtypes and hashes,720 canonical engine states,719 pairs of received/rendered
actions, raw hour23 inventory transitions before EOD, EOD resets, private
inventory order, worker positions/counts/hires, shop identities, and direct versus
instrumented boundary equality. The game helper additionally preserves the
existing raw tile/public-field checks at every hour.

| Artifact | SHA256 |
|---|---|
| Original failed execution | a2e7e718bef1b8d71ab7c66be0cd8cf25135d45ce8927b707bd41e6bb5a9304f |
| Game helper receipt | 91416bc1cc93abee8fec47862096dd09878fc1fd7e91b2f70eff8ef743f57082 |
| Raw simulator NPZ | db6020898bb2be5a31704c452cafadd579ec35b0d170f373cb802fff3ebab1fd |
| Canonical engine snapshots | acede79c9de75964003c5da4c1496f9894df716d0344f487439c16cd9b61d428 |
| Engine received actions | ec87557c3939756282467aa786d0b84de602f8bd6fe0b1accfb5bbd9e71331c4 |

The durable audit is the sibling
`S/unitorder/enhanced_season_20260912.root_saved_audit.json`. Raw files are in
`S/unitorder/enhanced_season_20260912/`; preserve them even where Git ignores
compressed artifacts. This result covers one synthetic policy/seed on CPU,
using archived switches including seed-room ON. It does not prove tape-seat
override fidelity, GPU performance, training repeatability or competitive gain.

The user's target remains top five. The remaining validation must serve a
bounded path back to candidate improvement: one exact captured tape case,
GPU performance/repeatability, then fresh bounded training and separate-family
evaluation against B. Production source and both B payloads remain unchanged,
MD5 7fcf39485bae65ee84171957c5843814. No promotion or upload occurred.
