import pandas as pd
import matplotlib.pyplot as plt

frontier_audit = pd.DataFrame([
    {"controller": "guard31 · fresh 12-seed holdout", "valid_games": 360, "wins": 344, "ties": 6, "losses": 10, "mean_margin": 28560.236},
    {"controller": "guard28 · same broad holdout", "valid_games": 360, "wins": 342, "ties": 4, "losses": 14, "mean_margin": 30127.114},
    {"controller": "price31 · earlier 1.32.7 frontier", "valid_games": 112, "wins": 104, "ties": 0, "losses": 8, "mean_margin": 31279.446},
    {"controller": "tetsutani latest · public pull", "valid_games": 128, "wins": 118, "ties": 0, "losses": 10, "mean_margin": 31267.531},
])
display(frontier_audit)
fig, ax = plt.subplots(figsize=(9.2, 4.0))
ax.barh(frontier_audit["controller"], frontier_audit["mean_margin"], color=["#16a34a", "#f59e0b", "#38bdf8", "#a78bfa"])
ax.set_xlabel("Mean candidate margin · local exact audit")
ax.set_title("Stable candidate selection from fresh public screens")
ax.grid(axis="x", alpha=.22); fig.tight_layout(); display(fig); plt.close(fig)
assert (frontier_audit["valid_games"] > 0).all()
