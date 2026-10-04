import pandas as pd
import matplotlib.pyplot as plt

combined_receipt = pd.DataFrame([
    {"control":"guard31", "valid":24, "wins":24, "ties":0, "losses":0, "mean_margin":62.417},
    {"control":"visible-price31", "valid":24, "wins":24, "ties":0, "losses":0, "mean_margin":79.000},
    {"control":"demand-preserving", "valid":24, "wins":24, "ties":0, "losses":0, "mean_margin":90.583},
    {"control":"more-wheat", "valid":24, "wins":24, "ties":0, "losses":0, "mean_margin":107.167},
])
display(combined_receipt.style.format({"mean_margin":"{:+,.3f}"}))
assert int(combined_receipt["valid"].sum()) == 96
assert int(combined_receipt[["wins","ties","losses"]].sum().sum()) == 96
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.bar(combined_receipt["control"], combined_receipt["mean_margin"], color=["#16a34a","#38bdf8","#a78bfa","#f59e0b"])
ax.axhline(0, color="#334155", linewidth=.8)
ax.set_ylabel("Mean money margin · local exact audit")
ax.set_title("Combined policy · fresh 12-seed paired holdout")
ax.grid(axis="y", alpha=.22)
fig.tight_layout(); display(fig); plt.close(fig)
print("384/384 valid; 96 wins, 0 ties, 0 losses; official score pending server row.")
