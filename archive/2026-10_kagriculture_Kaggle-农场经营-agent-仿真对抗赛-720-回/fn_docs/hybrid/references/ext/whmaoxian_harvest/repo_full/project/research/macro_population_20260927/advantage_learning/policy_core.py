"""Kaggriculture game research: legal SELL actions for virtual crops.
This module has no network, filesystem, account, or real financial operations.
It supports local comparisons of simulated final-game scores.
"""
AL_ITEMS=('CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL')
AL_FEATURES=55

def al_options(obs,action,projected):
    step=int(obs['step']);seat=int(obs['player'])
    if not 72<=step<648 or obs['farms'][seat]['money']<500:return []
    orders=action.get('market',[])
    commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
    blocked={c[1] for c in commands if len(c)>1 and c[0]=='PICKUP'}
    blocked.update(o[1] for o in orders if len(o)>1 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    out=[]
    for item in AL_ITEMS:
        if item in blocked or obs['market']['prices'].get(item,0)<=1:continue
        indices=[i for i,o in enumerate(orders) if len(o)>=3 and o[:2]==['SELL',item]]
        if len(indices)>1 or not indices and len(orders)>=10:continue
        original=sum(max(0,int(orders[i][2])) for i in indices)
        spare=max(0,int(projected.get(item,0))-original)
        if spare:out.append((item,sorted({1,min(4,spare),min(8,spare)})))
    return out
