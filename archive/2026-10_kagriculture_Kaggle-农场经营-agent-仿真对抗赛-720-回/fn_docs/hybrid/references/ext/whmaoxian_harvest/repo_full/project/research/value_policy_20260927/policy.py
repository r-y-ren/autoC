"""Legal actions for the Kaggriculture simulation, using only the player's view."""
VP_ITEMS=('CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL')
VP_FEATURES=48

def vp_options(obs,action,projected):
    step=int(obs['step']);seat=int(obs['player'])
    if not 144<=step<672 or obs['farms'][seat]['money']<1500:return []
    commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
    blocked={c[1] for c in commands if len(c)>1 and c[0]=='PICKUP'}
    orders=action.get('market',[])[:10];out=[]
    for item in VP_ITEMS:
        if item in blocked or obs['market']['prices'].get(item,0)<=1:continue
        matches=[o for o in orders if len(o)>=3 and o[:2]==['SELL',item]]
        if len(matches)>1 or not matches and len(orders)>=10:continue
        original=sum(max(0,int(o[2])) for o in matches)
        spare=max(0,int(projected.get(item,0))-original)
        if spare:out.append((item,sorted({1,min(4,spare)}),original,spare))
    return out

def vp_action(action,item,quantity):
    orders=[list(o) for o in action.get('market',[])]
    for order in orders:
        if len(order)>=3 and order[:2]==['SELL',item]:order[2]=int(order[2])+quantity;break
    else:
        if len(orders)>=10:raise ValueError('No free order slot')
        orders.append(['SELL',item,quantity])
    return dict(action,market=orders)

def vp_sync(obs,action,ns):
    seat=int(obs['player']);step=int(obs['step'])
    projected=ns['projected_shed'](action,ns['FarmView'](obs))
    previous=ns.get('_OR2_STATE',{}).get(seat,{}).get('prev')
    if previous and previous.get('step')==step:
        for item in VP_ITEMS:
            quantity=sum(max(0,int(o[2])) for o in action.get('market',[])[:10] if len(o)>=3 and o[:2]==['SELL',item])
            previous.setdefault('own',{})[item]=min(max(0,int(projected.get(item,0))),quantity)
    race=ns.get('_RACE_STATE',{}).get(seat)
    if race and race.get('step')==step:race['prev_action']=action
    return projected
