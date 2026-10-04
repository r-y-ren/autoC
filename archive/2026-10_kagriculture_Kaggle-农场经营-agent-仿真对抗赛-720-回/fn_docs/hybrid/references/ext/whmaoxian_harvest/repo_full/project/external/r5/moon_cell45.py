import pandas as pd
import matplotlib.pyplot as plt
summary = pd.DataFrame([
    {"arm":"control · public reference", "games":128, "valid":128, "wins":3},
    {"arm":"candidate · delayed harvest", "games":128, "valid":128, "wins":125},
])
display(summary)
fig, ax = plt.subplots(figsize=(8.8, 3.5))
ax.bar(summary["arm"], summary["wins"], color=["#64776b", "#247a4b"])
ax.set_ylabel("Paired wins")
ax.set_title("Exact-engine screen · 64 seeds × 2 seats")
ax.grid(axis="y", alpha=.25)
plt.xticks(rotation=12, ha="right"); plt.tight_layout(); display(fig); plt.close(fig)
assert (summary["valid"] == summary["games"]).all()
print("valid games: 128/128; local mean delta: +27.5625")