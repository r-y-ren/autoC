import pandas as pd
import matplotlib.pyplot as plt

frontier_v2 = pd.DataFrame([
    {"controller": "guard31 · 4-seed public screen", "valid": 88, "wins": 88, "ties": 0, "losses": 0, "mean_margin": 42190.330},
    {"controller": "one-turn race · 4-seed public screen", "valid": 96, "wins": 88, "ties": 4, "losses": 4, "mean_margin": 38687.885},
    {"controller": "Master V3 · 4-seed public screen", "valid": 96, "wins": 80, "ties": 8, "losses": 8, "mean_margin": 38650.302},
    {"controller": "Fieldcraft · companion restored", "valid": 96, "wins": 72, "ties": 0, "losses": 24, "mean_margin": 21518.844},
])
display(frontier_v2.style.format({"mean_margin": "{:+,.3f}"}))
fig, ax = plt.subplots(figsize=(9.2, 4.0))
ax.barh(frontier_v2["controller"], frontier_v2["mean_margin"], color=["#16a34a", "#38bdf8", "#a78bfa", "#f59e0b"])
ax.set_xlabel("Mean candidate margin · local exact audit")
ax.set_title("Fresh public frontier v2")
ax.grid(axis="x", alpha=.22)
fig.tight_layout(); display(fig); plt.close(fig)
assert (frontier_v2["valid"] > 0).all()
assert (frontier_v2["wins"] + frontier_v2["ties"] + frontier_v2["losses"] == frontier_v2["valid"]).all()
print("Fresh frontier v2 receipt: all listed rows valid; official score pending server submission.")
