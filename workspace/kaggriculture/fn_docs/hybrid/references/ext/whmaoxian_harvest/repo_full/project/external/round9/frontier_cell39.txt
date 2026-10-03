import pandas as pd
import matplotlib.pyplot as plt

ab = pd.DataFrame([
    {"panel": "Fixed frontier · 4 seeds × 12 opponents × 2 seats", "control": 33474.8646, "latched": 33490.9063, "games": 96, "valid": 96},
    {"panel": "Holdout frontier · 8 fresh seeds × 12 opponents × 2 seats", "control": 30660.0573, "latched": 31165.8021, "games": 192, "valid": 192},
])
ab["gain"] = ab["latched"] - ab["control"]
ab["validity"] = ab["valid"].astype(str) + "/" + ab["games"].astype(str)
display(ab[["panel", "control", "latched", "gain", "validity"]].style.format({"control": "{:,.1f}", "latched": "{:,.1f}", "gain": "+{:,.1f}"}))

fig, ax = plt.subplots(figsize=(9.4, 4.2))
x = list(range(len(ab)))
width = 0.34
ax.bar([i - width/2 for i in x], ab["control"], width, label="Pipe16 control", color="#64748b")
ax.bar([i + width/2 for i in x], ab["latched"], width, label="Latched opening router", color="#16a34a")
for i, gain in enumerate(ab["gain"]):
    ax.text(i, max(ab.loc[i, "control"], ab.loc[i, "latched"]) + 500, f"Δ {gain:+,.0f}", ha="center", fontsize=9)
ax.set_xticks(x, ["Fixed panel", "Fresh holdout"])
ax.set_ylabel("Mean candidate margin")
ax.set_title("Local exact-engine A/B: a latched visible-opening route")
ax.grid(axis="y", alpha=.25)
ax.legend(frameon=False)
plt.tight_layout()
display(fig)
plt.close(fig)
assert (ab["valid"] == ab["games"]).all()
assert (ab["latched"] > ab["control"]).all()
print("A/B panels valid:", ", ".join(ab["validity"]))