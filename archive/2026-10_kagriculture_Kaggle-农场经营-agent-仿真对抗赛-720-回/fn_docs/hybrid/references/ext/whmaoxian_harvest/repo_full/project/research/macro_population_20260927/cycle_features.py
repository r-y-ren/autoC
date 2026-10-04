"""Public-state features for forecasting commodity orders in a toy game."""
import math
_CY_ITEMS=('WHEAT','FERTILIZER')
_CY_CROPS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON')
_CY_ANIMALS=('COW','SHEEP','GOOSE')
def cycle_features(obs,item,history):
    step=int(obs['step']);seat=int(obs['player']);day=step//24
    mine=obs['farms'][seat];other=obs['farms'][1-seat];market=obs['market']
    counts={};yields={};unfed=0;fertilizer=0;needs_fertilizer=0
    for row in other['tiles']:
        for tile in row:
            if not isinstance(tile,dict):continue
            kind=tile.get('crop') or tile.get('animal')
            if kind:
                counts[kind]=counts.get(kind,0)+1
                yields[kind]=yields.get(kind,0)+max(0,int(tile.get('yield_units',0)))
            if tile.get('animal'):
                unfed+=not tile.get('fed_today',False)
                fertilizer+=bool(tile.get('fertilizer_available',False))
            if tile.get('crop') and int(tile.get('fertilized_until_day',-1))<day:
                needs_fertilizer+=1
    positions=[other['farmer']]+list(other['hands'])
    near=sum(p[0] in (4,5) and p[1] in (4,5) for p in positions)
    consecutive=history.get('step')==step-1
    prices=market['prices'];inventory=market['inventory']
    pp=history.get('prices',prices) if consecutive else prices
    pi=history.get('inventory',inventory) if consecutive else inventory
    f=[float(item==x) for x in _CY_ITEMS]
    f+=[step/24,step%24,step%4,step%72,719-step]
    f+=[inventory[x] for x in _CY_ITEMS]+[prices[x] for x in _CY_ITEMS]
    f+=[inventory[x]-pi[x] for x in _CY_ITEMS]+[prices[x]-pp[x] for x in _CY_ITEMS]
    f+=[counts.get(x,0) for x in _CY_CROPS+_CY_ANIMALS]
    f+=[yields.get(x,0) for x in _CY_CROPS]
    f+=[unfed,fertilizer,needs_fertilizer,len(other['hands']),near,len(other['unlocked_quadrants'])]
    f+=[math.log1p(max(0,other['money'])),math.log1p(max(0,mine['money']))]
    f+=[len(mine['hands']),sum(isinstance(t,dict) and bool(t.get('animal')) for row in mine['tiles'] for t in row),sum(isinstance(t,dict) and t.get('crop')=='WHEAT' for row in mine['tiles'] for t in row)]
    shops=obs['town']['unlocked_shops']
    grain=sum(s in ('BAKERY','PIZZA_SHOP','BRUNCH_SPOT','ICE_CREAM_SHOP','FARMERS_MARKET') for s in shops)
    f+=[len(shops),grain,0]
    f+=[other['money']-history.get('other_money',other['money']) if consecutive else 0]
    if len(f)!=43:raise ValueError('Commodity feature dimension mismatch')
    return [float(x) for x in f]

def cycle_commit(obs,history):
    history.update(step=int(obs['step']),prices=dict(obs['market']['prices']),inventory=dict(obs['market']['inventory']),other_money=obs['farms'][1-int(obs['player'])]['money'])

CYCLE_FEATURE_COUNT=43
CYCLE_INPUT_SCOPE='Public farms, public market, public town and their causal history; no private opponent inventory, identity or seed.'
