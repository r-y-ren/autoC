# Reported audited historical summary from the completed matched panels.
# This fixed table is historical evidence; fresh rows are recomputed later below.
display(pd.DataFrame([
    {"arm":"original source", "games":120, "wins":94, "mean_margin":406.3833333333},
    {"arm":"lookahead 4", "games":120, "wins":100, "mean_margin":595.2666666667},
    {"arm":"seed hedge 0", "games":120, "wins":94, "mean_margin":418.05},
]).style.format({"mean_margin":"{:+,.3f}"}))
