> **Version update.** The submission is now **MarketShock-M1-WR1K**, with one audited day-21 local watering repair and exact parent pass-through everywhere else. The original experiment record below is unchanged.

## What was built

The base is a frozen Seven-Turn Rescue agent. The research layer reconstructs matches turn by turn and separates route selection from economic execution.

T4 adds one bounded mechanism. In likely mirror games it can sell selected parent-planned inventory one turn earlier. If a real probe shows that the opponent also preempts sales, the lead can become two turns. Every moved unit becomes a credit against the original sale, so the overlay cannot liquidate the same stock twice.

In three fixed worlds, lead-1 beat the untouched control in all six seat-swapped games. Adaptive lead-2 then beat lead-1 in all six. The crop-value guard added +196 in one world and exactly 0 in two, so I treat it as weak and world-specific rather than a general breakthrough.

```python
if mirror_gate_is_open and 336 <= step < 647:
    lead = 2 if counter_preemption_was_observed else 1
    for item, qty in parent_sales(step + lead):
        qty = min(qty, projected_shed[item])
        if 4 <= qty < 100 and market_order_slot_exists:
            sell_now(item, qty)
            credit_original_sale(item, qty)

parent_sale[item] -= credited_quantity[item]
```

The parent remains frozen. The intervention has a narrow gate, and every activation is logged.