"""Observable step-144 features; no identities, seeds, future or rival-private data."""
PRODUCTS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')
TYPES=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','COW','SHEEP','GOOSE')
SHOPS=('BAKERY','PIZZA_SHOP','BRUNCH_SPOT','YARN_STORE','ICE_CREAM_SHOP','PET_CAFE','SMOOTHIE_SHOP','FARMERS_MARKET')
def route_features(obs):
    seat=int(obs['player']);day=int(obs['step'])//24;features={}
    shops=obs['town']['unlocked_shops']
    for shop in SHOPS:
        features['shops:'+shop]=shops.count(shop)
        for index in (0,1):features[f'shop{index}:'+shop]=int(len(shops)>index and shops[index]==shop)
    for item in PRODUCTS:
        features['market_inventory:'+item]=float(obs['market']['inventory'].get(item,10000))-10000
        features['market_price:'+item]=float(obs['market']['prices'].get(item,0))
    for prefix,index in [('own',seat),('rival',1-seat)]:
        farm=obs['farms'][index];tiles=[t for row in farm['tiles'] for t in row if isinstance(t,dict)]
        features[prefix+':cash']=float(farm['money']);features[prefix+':land']=len(farm['unlocked_quadrants'])
        features[prefix+':weeds']=sum(t.get('kind')=='WEED' for t in tiles)
        for item in TYPES:
            selected=[t for t in tiles if t.get('animal')==item or t.get('crop')==item]
            features[prefix+':count:'+item]=len(selected)
            features[prefix+':age_sum:'+item]=sum(day-int(t.get('placed_day',t.get('planted_day',day))) for t in selected)
            features[prefix+':ready:'+item]=sum(int(t.get('yield_units',0)) for t in selected)
            features[prefix+':care:'+item]=sum(int(t.get('pending_care_bonus',0)) for t in selected)
    private=obs['private']
    for item in PRODUCTS:
        features['own_stock:'+item]=int(private['shed'].get(item,0))+sum(int(inv.get(item,0)) for inv in private['inventories'])
    for item in TYPES[:5]:features['own_seeds:'+item]=int(private['seeds'].get(item,0))
    return features
