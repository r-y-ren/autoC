"""Observable-only market-flow features. No opponent private inventory or future state."""
import math
FLOW_ITEMS=('STRAWBERRY','MILK','WOOL','MELON','EGG','CARROT','TOMATO')
FLOW_BASE={'STRAWBERRY':120,'MILK':160,'WOOL':200,'MELON':250,'EGG':50,'CARROT':35,'TOMATO':60}
FLOW_SHOPS={'BAKERY':('EGG','WHEAT'),'PIZZA_SHOP':('MILK','TOMATO','WHEAT'),
 'BRUNCH_SPOT':('EGG','WHEAT','STRAWBERRY'),'YARN_STORE':('WOOL',),
 'ICE_CREAM_SHOP':('STRAWBERRY','MILK','WHEAT'),'PET_CAFE':('CARROT',),
 'SMOOTHIE_SHOP':('STRAWBERRY','MILK'),'FARMERS_MARKET':('WHEAT','CARROT','TOMATO','STRAWBERRY')}
FLOW_ANIMALS={'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}
FLOW_STATE={}
def flow_home(position):
    return min(abs(position[0]-x)+abs(position[1]-y) for x,y in ((4,4),(4,5),(5,4),(5,5)))

def flow_tiles(farm):
    tiles={};counts={item:0 for item in FLOW_ITEMS};held=dict(counts)
    for y,row in enumerate(farm['tiles']):
        for x,tile in enumerate(row):
            if not isinstance(tile,dict):continue
            item=FLOW_ANIMALS.get(tile.get('animal')) or tile.get('crop')
            if item not in counts:continue
            born=tile.get('placed_day',tile.get('planted_day',-1))
            quantity=int(tile.get('yield_units',0))
            tiles[(x,y)]=(item,born,quantity,int(tile.get('max_lifespan_step',-1)))
            counts[item]+=1;held[item]+=quantity
    return tiles,counts,held

def flow_demand(shops,item):
    return sum((2 if len(FLOW_SHOPS.get(shop,()))==1 else 1) for shop in shops if item in FLOW_SHOPS.get(shop,()))

def flow_project(obs,action):
    # Our own inventory projection; training labels use the target player's own view separately.
    stock=dict(obs['private']['shed']);farm=obs['farms'][int(obs['player'])]
    positions=[farm['farmer']]+farm['hands']
    commands=[action.get('farmer',['PASS'])]+list(action.get('hands',[]))
    for actor,(position,command) in enumerate(zip(positions,commands)):
        if not command or flow_home(position)!=0:continue
        bag=obs['private']['inventories'][actor];op=command[0]
        if op=='PICKUP' and len(command)>1:
            quantity=max(0,int(command[2])) if len(command)>2 else 1
            stock[command[1]]=max(0,stock.get(command[1],0)-quantity)
        elif op=='DROP':
            for item,quantity in bag.items():
                stock[item]=stock.get(item,0)+min(quantity,max(0,100-sum(stock.values())))
        elif op=='PLACE' and len(command)>1 and command[1] not in FLOW_ANIMALS:
            item=command[1];quantity=min(bag.get(item,0),max(0,int(command[2])) if len(command)>2 else 1)
            stock[item]=stock.get(item,0)+min(quantity,max(0,100-sum(stock.values())))
    return stock

def flow_sales(obs,action):
    stock=flow_project(obs,action);sold={item:0 for item in FLOW_ITEMS}
    for order in action.get('market',[])[:10]:
        if len(order)>=3 and order[0]=='SELL' and order[1] in sold:
            item=order[1];quantity=min(max(0,int(order[2])),stock.get(item,0))
            sold[item]+=quantity;stock[item]=stock.get(item,0)-quantity
    return sold

def flow_observe(obs):
    step=int(obs['step']);seat=int(obs['player']);rival=obs['farms'][1-seat]
    state=FLOW_STATE.get(seat)
    if state is None or step==0 or step<=state['step']:
        state=FLOW_STATE[seat]=dict(step=-1,prev=None,stock={i:0.0 for i in FLOW_ITEMS},
            smooth={i:0.0 for i in FLOW_ITEMS},age={i:100 for i in FLOW_ITEMS},
            hist={i:[0.0]*24 for i in FLOW_ITEMS})
    tiles,counts,held=flow_tiles(rival);_,owncounts,_=flow_tiles(obs['farms'][seat])
    positions=[tuple(rival['farmer'])]+[tuple(x) for x in rival['hands']]
    shops=list(obs.get('town',{}).get('unlocked_shops',[]))
    previous=state['prev'];external={i:0.0 for i in FLOW_ITEMS};harvest=dict(external);uncertain=dict(external)
    if previous is not None and previous['step']==step-1:
        if step%24:
            possible=set(previous['positions'])
            for position,old in previous['tiles'].items():
                item,born,quantity,expiry=old;new=tiles.get(position)
                if position not in possible:continue
                decrease=quantity if new is None or new[:2]!=old[:2] else max(0,quantity-new[2])
                if expiry>=0 and step-1>=expiry and (step-1-expiry)%2==0:
                    decrease=max(0,decrease-1)
                harvest[item]+=decrease
        for item in FLOW_ITEMS:
            draw=(flow_demand(previous['shops'],item) if (step-1)%4==0 else 0)+int((step-1)%24==0)
            change=float(obs['market']['inventory'][item]-previous['inventory'][item])+draw-previous['own'].get(item,0)
            external[item]=max(0,min(100,change));uncertain[item]=max(0,-change)
            state['stock'][item]=max(0,min(150,state['stock'][item]+harvest[item]-external[item]))
            state['smooth'][item]=.65*state['smooth'][item]+external[item]
            state['age'][item]=0 if external[item]>0 else min(100,state['age'][item]+1)
            h=(step-1)%24
            state['hist'][item][h]=.5*state['hist'][item][h]+.5*external[item]
    distances=[flow_home(p) for p in positions];count=max(1,len(positions));hour=step%24
    paused=sum(a==b for a,b in zip(positions,previous['positions']))/count if previous else 0.0
    cash=float(rival['money']);cash_change=cash-previous['cash'] if previous else 0.0
    features={}
    for index,item in enumerate(FLOW_ITEMS):
        price=float(obs['market']['prices'][item]);oldprice=previous['prices'][item] if previous else price
        hist=state['hist'][item]
        features[item]=[index,step/24.0,hour,len(rival['hands']),len(rival['unlocked_quadrants']),
            math.log1p(max(0,cash)),max(-10000,min(10000,cash_change))/1000.0,
            counts[item],held[item],owncounts[item],state['stock'][item],harvest[item],external[item],
            state['smooth'][item],state['age'][item],hist[hour],hist[(hour+1)%24],hist[(hour+2)%24],
            flow_demand(shops,item),price/FLOW_BASE[item],obs['market']['inventory'][item]-10000,
            (price-oldprice)/FLOW_BASE[item],sum(d==0 for d in distances)/count,
            sum(d<=2 for d in distances)/count,sum(distances)/count,min(distances),paused,
            sum(counts.values()),uncertain[item],hour%4,int(price<=1)]
    state['step']=step
    state['pending']=dict(step=step,tiles=tiles,positions=positions,shops=shops,cash=cash,
        inventory=dict(obs['market']['inventory']),prices=dict(obs['market']['prices']),own={})
    return features

def flow_commit(obs,action):
    state=FLOW_STATE[int(obs['player'])];pending=state['pending']
    sold=flow_sales(obs,action)
    pending['own']={item:(quantity if obs['market']['prices'][item]>1 else 0) for item,quantity in sold.items()}
    state['prev']=pending
