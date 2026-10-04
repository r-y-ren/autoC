"""Causal own-player features for public-replay market imitation (stdlib only)."""
import math
_MBC_ITEMS=('CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL')
_MBC_ANIMALS={'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}
_MBC_SHOPS={'BAKERY':('EGG','WHEAT'),'PIZZA_SHOP':('MILK','TOMATO','WHEAT'),
 'BRUNCH_SPOT':('EGG','WHEAT','STRAWBERRY'),'YARN_STORE':('WOOL',),
 'ICE_CREAM_SHOP':('STRAWBERRY','MILK','WHEAT'),'PET_CAFE':('CARROT',),
 'SMOOTHIE_SHOP':('STRAWBERRY','MILK'),'FARMERS_MARKET':('WHEAT','CARROT','TOMATO','STRAWBERRY')}
def _mbc_farm(farm):
    counts={}; yields={}
    for row in farm['tiles']:
        for tile in row:
            if not isinstance(tile,dict):continue
            item=tile.get('crop') or _MBC_ANIMALS.get(tile.get('animal'))
            if item:
                counts[item]=counts.get(item,0)+1
                yields[item]=yields.get(item,0)+max(0,int(tile.get('yield_units',0)))
    positions=[farm['farmer']]+list(farm.get('hands',[]))
    near=sum(p[0] in (4,5) and p[1] in (4,5) for p in positions)
    return counts,yields,near

def _mbc_context(obs,action,projected,history):
    seat=int(obs['player']); own=obs['farms'][seat];other=obs['farms'][1-seat]
    ac,ay,an=_mbc_farm(own);bc,by,bn=_mbc_farm(other)
    private=obs['private']; bags={}
    for bag in private.get('inventories',[]):
        for item,quantity in bag.items():bags[item]=bags.get(item,0)+max(0,int(quantity))
    non_sells=[o for o in action.get('market',[])[:10] if o and o[0]!='SELL']
    return dict(obs=obs,own=own,other=other,projected=projected,history=history,
                counts=ac,yields=ay,other_counts=bc,other_yields=by,near=an,other_near=bn,
                bags=bags,non_sells=non_sells,total=sum(projected.values()),
                total_bags=sum(bags.values()),premium=sum(projected.get(i,0) for i in _MBC_ITEMS))

def _mbc_features(context,item):
    c=context;obs=c['obs'];step=int(obs['step']);private=obs['private']
    market=obs['market'];shops=obs['town']['unlocked_shops'];h=c['history']
    consecutive=h.get('last_step')==step-1
    price=float(market['prices'][item]);inventory=float(market['inventory'][item])
    shed=float(private['shed'].get(item,0));yield_other=c['other_yields'].get(item,0)
    prior_price=h.get('prices',{}).get(item,price) if consecutive else price
    prior_inventory=h.get('market_inventory',{}).get(item,inventory) if consecutive else inventory
    prior_shed=h.get('shed',{}).get(item,shed) if consecutive else shed
    prior_yield=h.get('other_yields',{}).get(item,yield_other) if consecutive else yield_other
    demand=sum((2 if len(_MBC_SHOPS.get(s,()))==1 else 1) for s in shops if item in _MBC_SHOPS.get(s,()))
    ns=c['non_sells']
    features=[float(item==i) for i in _MBC_ITEMS]
    features += [step/24,step%24,step%4,step%72,719-step]
    features += [c['projected'].get(item,0),shed,c['bags'].get(item,0),c['total'],c['premium'],c['total_bags'],c['projected'].get(item,0)-shed]
    features += [inventory,price,price-prior_price,inventory-prior_inventory,shed-prior_shed]
    features += [c['counts'].get(item,0),c['yields'].get(item,0),c['other_counts'].get(item,0),yield_other,prior_yield-yield_other]
    features += [math.log1p(max(0,c['own']['money'])),math.log1p(max(0,c['other']['money'])),len(c['own']['hands']),len(c['other']['hands']),len(c['own']['unlocked_quadrants']),len(c['other']['unlocked_quadrants']),c['near'],c['other_near']]
    features += [demand,len(shops),max(0,8-len(shops)),len(ns),sum(o[0]=='HIRE' for o in ns),sum(o[0]=='BUY_LAND' for o in ns)]
    features += [min(120,step-h.get('last_sale',{}).get(item,-120)),h.get('previous_sale',{}).get(item,0)]
    return [float(v) for v in features]

def _mbc_commit(context,sold):
    obs=context['obs'];history=context['history'];step=int(obs['step'])
    history['last_step']=step
    history['prices']=dict(obs['market']['prices'])
    history['market_inventory']=dict(obs['market']['inventory'])
    history['shed']=dict(obs['private']['shed'])
    history['other_yields']=dict(context['other_yields'])
    history['previous_sale']=dict(sold)
    for item,quantity in sold.items():
        if quantity>0:history.setdefault('last_sale',{})[item]=step

MBC_FEATURE_COUNT=45
MBC_INPUT_SCOPE='Own observation and proposed physical/non-SELL actions only; previous own sales are causal history. No opponent private state, identities, episode IDs, or random seeds.'
