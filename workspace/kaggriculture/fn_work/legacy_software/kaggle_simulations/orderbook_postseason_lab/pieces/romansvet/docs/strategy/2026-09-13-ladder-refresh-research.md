# Public ladder refresh attempt and bounded top-five research

## Fresh authoritative observation at 14:33 UTC

The existing credential-free capture helper completed three paced public
requests at14:33:20/25/30 UTC, all HTTP200. Raw responses, metadata and summary
are preserved in `S/ladder2/snapshot_20260913T1433/`; root rehashed each response
and reproduced the summary from raw bytes.

| Field | Observed value |
| --- | ---: |
| Existing B submission | 56161192 |
| Team leaderboard rank / displayed score | **192 / 2725.0** |
| Fifth-place displayed score | **3028.9** |
| Displayed gap to fifth | **303.9** |
| B completed games / wins / ties | 317 / 216 / 0 |
| Latest completed episode rating | 2725.0654624711315 |
| Latest completed episode end | 14:28:45.865361800 UTC |

This is the existing B entry after further public matches. Both newly trained
momentum candidates failed to demonstrate an offline improvement and were not
submitted; the change from rank249 at08:07 is not credited to those changes.
The top-five goal remains unmet. The earlier snapshot below is historical.

## Fresh authoritative observation at 08:07Z

The established snapshot schema is `S/ladder2/capture_snapshot.py`: paced,
credential-free `ListEpisodes` reads for submissions 56161192 and 56143250,
followed by `GetLeaderboard` for competition 147734. Raw responses, request
metadata and hashes are written before `summarize_snapshot.py` separately
derives episode and leaderboard fields.

An initial sandboxed attempt began at 2026-09-13 08:02:41Z. DNS resolution
failed on the first `ListEpisodes` request, before an HTTP response. No raw
response was received and no second endpoint was contacted. That failed
attempt remains preserved at
`S/ladder2/snapshot_20260913T0802_failed/failure.json` (SHA-256
`669d61770f27f3215174b4795f20e92a81d0c7e3d530c20bf773fa32284a4a61`).
It contains no credential or authentication material.

Root then ran the same helper once with network access in a fresh output
directory. Its three paced requests completed at 08:06:57Z, 08:07:02Z and
08:07:07Z, all HTTP 200. Independent verification recomputed every response
SHA-256 from raw bytes, reproduced `summary.json` exactly, and found one
leaderboard row for team TEAM_ID whose public submission is 56161192. The
fresh observation is:

| field | observed value | source meaning |
|---|---:|---|
| B completed games / wins | 286 / 195 | file-specific `ListEpisodes` history |
| B latest completed episode rating | 2684.1926 | `updatedScore` from episode 108469556, ended 08:03:08Z |
| team leaderboard rank / displayed score | **249 / 2684.1** | team row from the separate 08:07:07Z leaderboard response; its public entry is submission 56161192 |
| fifth-place displayed score | **3030.1** | leaderboard row at rank five, submission 56180166 |
| displayed gap to fifth | **346.0** | 3030.1 minus 2684.1 |

The team row is a leaderboard observation; the episode rating is the last
file-specific update present in this response. Their near equality does not
make them the same field, and later games can make either observation stale.
The raw response hashes are
`821198552db0a6bfe3a370748bac81923264af35753630202827fe8dd252a4c2`
(B episodes),
`e583bbc2116a09ce707e0d3369f1288e23b621130c6d0a632283f0f9ba5674df`
(hr episodes), and
`a94779302225e1ce3087b20e31dc8a9b2122d42677db69ed9e79d761fdaebd0e`
(leaderboard). The saved summary SHA-256 is
`0884746d027c428d9b4ed024c072d0efea94f876dc4d0332dbeba059dbe68daf`;
the independent audit is preserved beside it with SHA-256
`a6d0c807edb435d612e65bcf956edee50c4f772701ad80a17223c1d94a27ed93`.

## Largest useful strategic difference: productive-input efficiency after the opening

The existing top-50 catalogue already shows that the top five were not one
policy template. Their two saved wins each span adaptive Majkel1337 and
SpaTaro, a clone-derived `feel the agi`, an open-loop geese/tomato build, and
an open-loop heavy-wheat build. All deploy workers, animals and melon much
earlier than B, but the joint wall-opening intervention already reproduced
that broad opening and lost decisively. Those observations do not reopen the
forced-melon, labour-ramp or sell-timing families.

The strongest remaining difference worth studying is how efficiently an
already productive herd/crop program consumes bought inputs. In six preserved
peer games, Majkel1337 beat SpaTaro 6-0 while earning lower gross revenue in
four. Median total spending was 8.8k lower, explained almost entirely by
bought wheat: 117-190 units costing 4.1-7.2k versus 375-535 units costing
14.0-21.7k. Majkel was behind at day 10 in all six and ahead during both days
11-20 and days 21-29 in all six. Its revenue mix also held 39-66 strawberry
units to days 27-29, but the consistent, largest measured term was input cost,
not extra gross sales or a market attack.

This is evidence for an accounting question, not evidence that B overbuys
wheat or that a feed scalar would improve it. The cheapest discriminating next
measurement needs no new download or game: on the already-fixed two public
wins for each of the snapshot's ranks 1-5, trace every executed wheat purchase
to later FEED, resale, or remaining inventory and report spend and physical
animal-product output per episode and template. Add a separately selected B
case only if its provenance is fixed before reading this metric; do not use the
loss-selected public-B12 as representative support.

Stop the general input-efficiency hypothesis if Majkel's low purchased-wheat
burden is not shared by at least two other saved top-five templates, or if the
accounting cannot distinguish feed consumption from resale without inferred
counterfactuals. A positive descriptive pattern would justify inspecting the
existing feed reservation and purchase projection for one concrete mismatch;
it would not authorize a policy pilot.

Sources are already local: `S/top50/features.json` SHA-256
`0f6d779c60b6c09567404995d16bc28db7ef1d1ea4d603fe7a0bb2e39a068a6a`,
`2026-09-11-top50-patterns.md` SHA-256
`04015bdbd0e778aec66aaa6fc8a0da38249b412ba7807034045c89d7b27141c4`,
and `2026-09-11-majkel-vs-spataro.md` SHA-256
`22f7999075368369fa3a39d25c8aca5e6e08f090a0ba21a67a92debbe65c72`.
No replay was downloaded or executed for this review.

Follow-up: [the saved wheat-accounting diagnostic](2026-09-13-top5-wheat-accounting.md)
found zero other templates at or below Majkel on the declared purchase/output
ratio. The generalization stops for that metric and these selected wins;
heterogeneous product units and unexplained residuals prevent an economic
efficiency conclusion. No B case or policy pilot followed.
