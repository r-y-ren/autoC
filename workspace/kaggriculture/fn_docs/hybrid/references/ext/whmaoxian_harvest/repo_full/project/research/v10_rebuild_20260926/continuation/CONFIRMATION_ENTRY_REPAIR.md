# Evaluation entrypoint repair — candidate remains frozen

The public MarketShock notebook builds a module with a callable `module.agent`.
Its last defined helper is `install_water_repair_local_patch(parent)`. Kaggle's
`get_last_callable` chooses that helper, so the first callback returns another
function rather than a JSON action. The unadapted file is therefore not a valid
file-path submission as written. Its original source and builder receipt are kept.

The evaluation-only `marketshock_adapter.py` loads the byte-identical public
source, binds its declared `agent`, and exposes the inherited diagnostic reports.
No production, market, routing, thresholds or opponent behavior is modified.
The candidate hash remains e03333c6bef0c83764d56f1cc958782f032c5bbdc0684bae1cc2ccd6b61f3e7c.

All 288 affected cases (candidate, V9 and V10; the same 48 worlds and both seats)
are scheduled anew. Initial failed attempts must not be counted as wins or full
matches. Unaffected valid cases may be reused with exact source/seed/seat identity.
The full original manifest, ledger and logs must remain under an initial-attempt
archive, and the replacement mapping must be recorded before final assessment.
No thresholds or source-selection decisions depend on the held-out scores.

This is a test of the public author's intended callable with an explicit entry
adapter, not evidence that the unadapted notebook package works on Kaggle or has
any asserted rating. Six implementations are not six independent code lineages.
