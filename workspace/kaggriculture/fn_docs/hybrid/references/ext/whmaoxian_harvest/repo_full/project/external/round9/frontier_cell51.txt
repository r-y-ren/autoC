import pandas as pd
from IPython.display import display

promotion_receipt = pd.DataFrame([
    {"candidate": "guard31", "engine": "1.32.7", "scheduled": 360, "valid": 360, "wins": 344, "ties": 6, "losses": 10, "mean_margin": 28560.236, "source_sha256": '725729aca693fa8bad40cc6fbfbcd56cf37a08a9490dedef49c4f9f16844655e'},
])
display(promotion_receipt)
assert promotion_receipt.loc[0, "scheduled"] == promotion_receipt.loc[0, "valid"] == 360
assert promotion_receipt.loc[0, "source_sha256"] == '725729aca693fa8bad40cc6fbfbcd56cf37a08a9490dedef49c4f9f16844655e'
print("Complete local receipt; official score pending the next completed Kaggle row.")
