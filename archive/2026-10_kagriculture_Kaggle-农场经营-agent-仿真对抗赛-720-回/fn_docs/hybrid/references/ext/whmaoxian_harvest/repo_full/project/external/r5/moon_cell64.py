import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

pipe19_receipt = pd.DataFrame([
    {"window": "current · 72 games", "valid": 72, "wins": 58, "ties": 0, "losses": 14, "mean_margin": 944.139, "min_margin": -478},
    {"window": "robust · 120 games", "valid": 120, "wins": 118, "ties": 0, "losses": 2, "mean_margin": 1190.000, "min_margin": -20},
    {"window": "combined · 192 games", "valid": 192, "wins": 176, "ties": 0, "losses": 16, "mean_margin": 1097.8020833333333, "min_margin": -478},
])
display(pipe19_receipt.style.format({"mean_margin": "{:+,.3f}", "min_margin": "{:+,.0f}"}))
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
axes[0].bar(pipe19_receipt["window"], pipe19_receipt["wins"], color=["#38bdf8", "#22c55e", "#a78bfa"])
axes[0].set_ylabel("Wins · exact local engine")
axes[0].set_title("Pipe-19 Ultra paired wins")
axes[0].tick_params(axis="x", rotation=18)
axes[1].bar(pipe19_receipt["window"], pipe19_receipt["mean_margin"], color=["#60a5fa", "#16a34a", "#8b5cf6"])
axes[1].axhline(0, color="#334155", linewidth=.8)
axes[1].set_ylabel("Mean money margin")
axes[1].set_title("Margin by validation window")
axes[1].tick_params(axis="x", rotation=18)
for ax in axes:
    ax.grid(axis="y", alpha=.22)
fig.tight_layout(); display(fig); plt.close(fig)
print("192/192 valid; 176 wins, 0 ties, 16 losses; official score pending server row.")
