order_example_28={'schema': 'clone-model-ordering-example-v1', 'evidence_boundary': 'Historical visible-state input and deterministic clone model only. Model assumes equal stock and original order list for rival, with unlimited funding. No counterfactual full-game result.', 'trace_sha256': '55a20ca7376d0bde1a24eb2739db8856a60bbcfac6c11fcc757db4f716676555', 'source_sha256': '178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a', 'step': 447, 'original_orders': [['SELL', 'MILK', 2], ['SELL', 'WOOL', 2], ['SELL', 'EGG', 2], ['BUY_SEED', 'WHEAT', 2]], 'reordered_orders': [['SELL', 'WOOL', 2], ['SELL', 'EGG', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 2]], 'projected_stock': {'WHEAT': 6, 'CARROT': 0, 'TOMATO': 0, 'STRAWBERRY': 0, 'MELON': 0, 'EGG': 2, 'MILK': 2, 'WOOL': 4, 'FERTILIZER': 6, 'GOOSE': 0, 'COW': 0, 'SHEEP': 0}, 'initial_inventory': {'WHEAT': 9730, 'CARROT': 9857, 'TOMATO': 9865, 'STRAWBERRY': 9923, 'MELON': 10125, 'EGG': 9923, 'MILK': 10075, 'WOOL': 10037, 'FERTILIZER': 10330}, 'market_parameters': {'WHEAT': {'base': 25, 'I0': 10000, 'T': 400, 'below_func': 'sqrt', 'below_target': 0.8, 'above_func': 'log', 'above_target': 0.2}, 'CARROT': {'base': 35, 'I0': 10000, 'T': 450, 'below_func': 'hinge', 'below_target': 1.0, 'above_func': 'sqrt', 'above_target': 0.7}, 'TOMATO': {'base': 60, 'I0': 10000, 'T': 200, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'sqrt', 'above_target': 0.6}, 'STRAWBERRY': {'base': 120, 'I0': 10000, 'T': 100, 'below_func': 'sqrt', 'below_target': 0.7, 'above_func': 'linear', 'above_target': 1.6}, 'MELON': {'base': 250, 'I0': 10000, 'T': 300, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.6}, 'EGG': {'base': 50, 'I0': 10000, 'T': 332, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'log', 'above_target': 0.2}, 'MILK': {'base': 160, 'I0': 10000, 'T': 122, 'below_func': 'sqrt', 'below_target': 0.6, 'above_func': 'linear', 'above_target': 1.6}, 'WOOL': {'base': 200, 'I0': 10000, 'T': 105, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.2}, 'FERTILIZER': {'base': 100, 'I0': 10000, 'T': 200, 'below_func': 'linear', 'below_target': 0.4, 'above_func': 'linear', 'above_target': 0.4}}, 'original_clone_revenues': [347.0, 347.0], 'reordered_clone_revenues': [349.0, 332.0], 'model_margin_change': 17.0}
# Edit this copy's stock, order lists or market inventory to explore the model.
from collections import Counter
example_policy_28=get_last_callable(AGENT_SOURCE.decode('utf-8'),path='main.py')
assert example_policy_28.__name__ == EXPECTED_LOADER_NAME
lockstep_model_28=example_policy_28.__globals__['_v44y_lockstep']
def evaluate_order_example_28(case):
    original=case['original_orders'];reordered=case['reordered_orders']
    assert Counter(map(tuple,original)) == Counter(map(tuple,reordered))
    for index,order in enumerate(original):
        if order[0]!='SELL':assert reordered[index] == order
    common=(case['initial_inventory'],case['projected_stock'],case['projected_stock'],case['market_parameters'])
    before=lockstep_model_28(original,original,*common)
    after=lockstep_model_28(reordered,original,*common)
    return before,after
example_before_28,example_after_28=evaluate_order_example_28(order_example_28)
assert list(example_before_28)==order_example_28['original_clone_revenues']
assert list(example_after_28)==order_example_28['reordered_clone_revenues']
assert (example_after_28[0]-example_after_28[1])-(example_before_28[0]-example_before_28[1])==order_example_28['model_margin_change']
display(pd.DataFrame({'slot':range(len(order_example_28['original_orders'])),
    'before':order_example_28['original_orders'],'after':order_example_28['reordered_orders']}))
display(pd.DataFrame([{'ordering':'original','our modeled trade receipts':example_before_28[0],'clone modeled trade receipts':example_before_28[1]},
    {'ordering':'final reorder','our modeled trade receipts':example_after_28[0],'clone modeled trade receipts':example_after_28[1]}]))
print('Model relative change:',order_example_28['model_margin_change'])
print('These are modeled trade receipts. The unchanged seed purchase is excluded from these totals; its cost and affordability must be checked separately. No counterfactual game or official rating is claimed.')
