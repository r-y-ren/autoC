"""Observable day-six macro context; no identity, seed or future information."""
import math
ITEMS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')
SHOPS=('BAKERY','PIZZA_SHOP','BRUNCH_SPOT','YARN_STORE','ICE_CREAM_SHOP','PET_CAFE','SMOOTHIE_SHOP','FARMERS_MARKET')
ANIMALS={'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}

def farm_features(farm):
    count={};stock={};age={};active={}
    for row in farm['tiles']:
        for tile in row:
            if not isinstance(tile,dict):continue
            item=tile.get('crop') or ANIMALS.get(tile.get('animal'))
            if not item:continue
            count[item]=count.get(item,0)+1
            stock[item]=stock.get(item,0)+max(0,int(tile.get('yield_units',0)))
            age[item]=age.get(item,0)+int(tile.get('planted_day',tile.get('placed_day',0)))
            active[item]=active.get(item,0)+int(bool(tile.get('watered_today') or tile.get('fed_today')))
    vec=[count.get(i,0) for i in ITEMS]+[stock.get(i,0) for i in ITEMS]
    vec += [age.get(i,0)/max(1,count.get(i,0)) for i in ITEMS]
    vec += [active.get(i,0) for i in ITEMS]
    vec += [math.log1p(max(0,float(farm['money']))),len(farm['hands']),len(farm['unlocked_quadrants'])]
    return vec

def features(observation):
    seat=int(observation['player']);a,b=observation['farms'][seat],observation['farms'][1-seat]
    shops=observation['town']['unlocked_shops'][:2];market=observation['market']
    own,other=farm_features(a),farm_features(b)
    vec=[shops.count(s) for s in SHOPS]+own+other+[x-y for x,y in zip(own,other)]
    vec += [float(market['prices'][i]) for i in ITEMS]
    vec += [float(market['inventory'][i]) for i in ITEMS]
    vec += [float(observation['private']['shed'].get(i,0)) for i in ITEMS]
    vec += [float(observation['private']['seeds'].get(i,0)) for i in ITEMS[:5]]
    return [float(v) for v in vec]

FEATURE_COUNT=157
