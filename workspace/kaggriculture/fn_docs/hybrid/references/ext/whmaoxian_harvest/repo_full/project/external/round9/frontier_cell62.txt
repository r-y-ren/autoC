import pandas as pd
import matplotlib.pyplot as plt

hybrid_receipt = pd.DataFrame([
    {"window": "12 seeds x 3 controls", "valid": 72, "wins": 42, "ties": 18, "losses": 12, "mean_margin": 139.083},
    {"window": "12 seeds x 5 controls", "valid": 120, "wins": 95, "ties": 20, "losses": 5, "mean_margin": 230.367},
    {"window": "combined", "valid": 192, "wins": 137, "ties": 38, "losses": 17, "mean_margin": 196.148},
])
display(hybrid_receipt.style.format({"mean_margin": "{:+,.3f}"}))
assert int(hybrid_receipt["valid"].sum()) == 384
assert int(hybrid_receipt[["wins", "ties", "losses"]].sum().sum()) == 384
fig, ax = plt.subplots(figsize=(9.4, 3.8))
bars = ax.bar(hybrid_receipt["window"], hybrid_receipt["mean_margin"], color=["#38bdf8", "#16a34a", "#f59e0b"])
ax.axhline(0, color="#334155", linewidth=.8)
ax.bar_label(bars, fmt="%+.1f", padding=4)
ax.set_ylabel("Mean money margin - local exact audit")
ax.set_title("Hybrid source: two-window current-engine receipt")
ax.grid(axis="y", alpha=.22)
fig.tight_layout(); display(fig); plt.close(fig)
print("192 valid games across two windows; official score pending server row.")
