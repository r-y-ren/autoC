import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

adaptive_receipt = pd.DataFrame([
    {"opponent": "combined", "valid": 24, "wins": 21, "ties": 2, "losses": 1, "mean_margin": 126.250},
    {"opponent": "hybrid", "valid": 24, "wins": 3, "ties": 20, "losses": 1, "mean_margin": -3.833},
    {"opponent": "guard31_v56", "valid": 24, "wins": 24, "ties": 0, "losses": 0, "mean_margin": 184.500},
    {"opponent": "v56", "valid": 24, "wins": 24, "ties": 0, "losses": 0, "mean_margin": 207.333},
    {"opponent": "yummers", "valid": 24, "wins": 24, "ties": 0, "losses": 0, "mean_margin": 209.500},
])
display(adaptive_receipt.style.format({"mean_margin": "{:+,.3f}"}))
assert int(adaptive_receipt["valid"].sum()) == 120
assert int(adaptive_receipt[["wins", "ties", "losses"]].sum().sum()) == 120
fig, ax = plt.subplots(figsize=(9.2, 3.8))
colors = ["#38bdf8" if x >= 0 else "#f97316" for x in adaptive_receipt["mean_margin"]]
ax.bar(adaptive_receipt["opponent"], adaptive_receipt["mean_margin"], color=colors)
ax.axhline(0, color="#334155", linewidth=.8)
ax.set_ylabel("Mean money margin · local exact audit")
ax.set_title("Visible-state adaptive router · fresh 12-seed paired holdout")
ax.grid(axis="y", alpha=.22)
fig.tight_layout(); display(fig); plt.close(fig)
print("120/120 valid; 96 wins, 22 ties, 2 losses; official score pending server row.")
