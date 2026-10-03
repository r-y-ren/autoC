import pandas as pd
import matplotlib.pyplot as plt

composition_receipt = pd.DataFrame([
    {"control":"demand-preserving", "valid":24, "wins":24, "ties":0, "losses":0, "mean_margin":27.833},
    {"control":"more-wheat", "valid":24, "wins":24, "ties":0, "losses":0, "mean_margin":56.500},
    {"control":"visible-price31", "valid":24, "wins":14, "ties":10, "losses":0, "mean_margin":28.667},
    {"control":"guard31", "valid":24, "wins":0, "ties":24, "losses":0, "mean_margin":0.000},
])
display(composition_receipt.style.format({"mean_margin":"{:+,.3f}"}))
assert int(composition_receipt["valid"].sum()) == 96
assert int(composition_receipt[["wins","ties","losses"]].sum().sum()) == 96
fig, ax = plt.subplots(figsize=(8.4, 3.5))
ax.bar(composition_receipt["control"], composition_receipt["mean_margin"], color=["#16a34a","#38bdf8","#a78bfa","#f59e0b"])
ax.axhline(0, color="#334155", linewidth=0.8)
ax.set_ylabel("Mean money margin · local exact audit")
ax.set_title("Guard31 + V56 composition")
ax.grid(axis="y", alpha=.22)
fig.tight_layout(); display(fig); plt.close(fig)
print("96/96 valid; 62 wins, 34 ties, 0 losses; official score pending server row.")
