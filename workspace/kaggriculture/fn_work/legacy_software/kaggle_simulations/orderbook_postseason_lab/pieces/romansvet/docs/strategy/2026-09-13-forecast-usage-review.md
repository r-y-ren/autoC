# Forecasting in the submitted agent and current training

The user asked whether the agent uses forecasting and whether it could help
training. The submitted B uses analytical forecasts in both its policy inputs
and planner; it is not restricted to today's price alone.

- `core/brain.py:344-440` forecasts both farms' harvestable supply now and
  additional production over1,3 and7 days using public crop/animal state.
- `brain.py:192-275` estimates remaining town demand and subtracts market
  inventory, our stored products and both farms' committed production.
- `brain.py:444-489` values near-term production using today's quotes. This
  particular feature is not a forecast of the future price curve.
- `core/plan.py:4802-4814` separately projects inventory to a product's first
  yield using town draw and our committed pipeline, then prices its unit stream
  on the market curve. Opponent supply is not explicitly added in this planner
  calculation; learned `grow_mult` and `press` are meant to account for it.

These references are to the captured source under
`S/unitorder/off_train_20260913/loop-train/private_stage/src/kagg3`.
The production forecast assumes watering/feeding and sufficiently frequent
harvests. It does not know future opponent decisions, hidden storage or future
random shop draws. Forecasted production is not necessarily realized sales.

Root inspected the actual B checkpoint through a byte-identical /tmp source
copy, with project Python and bytecode disabled. Evidence is preserved in
`S/unitorder/forecast_usage_20260913.json`, SHA-256
`d46694beaf6861a3efcc87ffc7129f5880d2aa3dbf2ea0c0ddb03934f85fa4e0`.
All512 `fh`,16 `fs` and384 `fv` forecast-path weights are nonzero. The paths
are connected by `brain.decide` and `policy.forward`; this establishes that
forecast inputs are wired into B, not their per-state benefit or causal size.

Current seed309/310 training names `gp,dh,ds,g5,gb5,w3,b3,b1` in its mask.
It can adjust decisions and the residual-demand input path, while holding
`fh/fs/fv` fixed. The underlying forecast formulas are analytical and are not
being fitted to future observations by this ES run. Each candidate is judged
by simulated game performance, not forecast prediction error.

Better forecasts could help decisions if they add usable information at the
relevant horizon. They do not guarantee better outcomes: predictions can be
redundant, wrong under changed actions, or translated into unhelpful choices.
The proposed momentum test should compare against the existing current-state
and production-timing features on training-side data, with separate validation.
Prediction improvement and policy improvement are separate claims. No forecast
or momentum code was changed during this review; the current run continues.
