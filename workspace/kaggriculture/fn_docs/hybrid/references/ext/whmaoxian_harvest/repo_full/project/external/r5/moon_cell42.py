import pandas as pd
import matplotlib.pyplot as plt

ab = pd.DataFrame([
    {"panel": "Fixed frontier · 4 seeds × 12 opponents × 2 seats", "pipe16": 33474.8646, "original": 34054.8958, "mixed": 34318.8229, "selected_earlycycle": 34571.1979, "games": 96, "valid": 96},
    {"panel": "Fresh holdout · 8 seeds × 12 opponents × 2 seats", "pipe16": 30660.0573, "original": None, "mixed": None, "selected_earlycycle": 36391.4688, "games": 192, "valid": 192},
])
display(ab.style.format({"pipe16": "{:,.1f}", "original": "{:,.1f}", "mixed": "{:,.1f}", "selected_earlycycle": "{:,.1f}"}))

fixed = ab.iloc[0]
fig, ax = plt.subplots(figsize=(9.8, 4.3))
labels = ["Pipe16 control", "Original opening", "Mixed opening", "EarlyCycle selected"]
values = [fixed.pipe16, fixed.original, fixed.mixed, fixed.selected_earlycycle]
ax.bar(labels, values, color=["#64748b", "#94a3b8", "#38bdf8", "#16a34a"])
ax.set_ylabel("Mean candidate margin")
ax.set_title("Pinned-engine opening A/B on the fixed frontier")
ax.grid(axis="y", alpha=.25)
plt.xticks(rotation=12, ha="right")
plt.tight_layout()
display(fig)
plt.close(fig)

assert (ab["valid"] == ab["games"]).all()
assert fixed.selected_earlycycle > fixed.pipe16
assert fixed.selected_earlycycle > fixed.original
assert fixed.selected_earlycycle > fixed.mixed
print("A/B panels valid:", ", ".join(f"{int(v)}/{int(g)}" for v, g in zip(ab["valid"], ab["games"])))