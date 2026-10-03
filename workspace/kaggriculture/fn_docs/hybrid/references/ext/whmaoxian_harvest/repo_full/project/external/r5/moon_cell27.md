### Use the same auditor on a downloaded public episode

Attach a public episode JSON as notebook input and set `PUBLIC_REPLAY_PATH` below. The exported `public_cash_audit.py` calls the official worker and market code separately for each recorded starting observation. It checks **both cash transitions for all 719 turns** and both private states outside dawn, and records successful sales, purchases, hiring, and land acquisition.

It deliberately does not roll the entire game forward or reconstruct random dawn events. Its role is to explain executed public cash flows quickly. Both players' recorded private inventories are used for offline accounting only; they are not inputs to the submitted agent. Agent decision rules must use only the information available in their own observation.
