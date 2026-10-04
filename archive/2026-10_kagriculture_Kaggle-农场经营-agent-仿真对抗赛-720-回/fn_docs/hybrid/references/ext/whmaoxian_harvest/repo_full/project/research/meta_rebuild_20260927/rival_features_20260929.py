"""Public-only rival-sale features. No private inventory, identity, rating or seed inputs."""
import math as _k29f_math
_K29F_PRODUCTS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')
_K29F_TARGETS=('STRAWBERRY','MELON','MILK','WOOL')
_K29F_SOURCES=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','GOOSE','COW','SHEEP')
_K29F_ANIMAL_PRODUCT={'GOOSE':'EGG','COW':'MILK','SHEEP':'WOOL'}
_K29F_SHOPS=('BAKERY','PIZZA_SHOP','BRUNCH_SPOT','YARN_STORE','ICE_CREAM_SHOP','PET_CAFE','SMOOTHIE_SHOP','FARMERS_MARKET')
_K29F_HOME=((4,4),(5,4),(4,5),(5,5))

def _k29f_snapshot(obs):
    step=int(obs['step']);day=step//24;farms=[]
    for farm in obs['farms']:
        counts={i:0 for i in _K29F_SOURCES};yields={i:0 for i in _K29F_PRODUCTS};ages={i:0 for i in _K29F_SOURCES}
        by_position={};unserved=0
        for y,row in enumerate(farm['tiles']):
            for x,t in enumerate(row):
                if not isinstance(t,dict):continue
                source=t.get('animal') or t.get('crop')
                if source not in counts:continue
                counts[source]+=1;age=max(0,day-int(t.get('placed_day',t.get('planted_day',day))));ages[source]+=age
                product=_K29F_ANIMAL_PRODUCT.get(source,source);q=max(0,int(t.get('yield_units',0)));yields[product]+=q
                by_position[(x,y)]=(product,q)
                unserved+=int(not t.get('fed_today',t.get('watered_today',True)))
        positions=[farm['farmer']]+list(farm['hands']);on={i:0 for i in _K29F_PRODUCTS};ready={i:0 for i in _K29F_PRODUCTS}
        for p in positions:
            value=by_position.get(tuple(p))
            if value:on[value[0]]+=1;ready[value[0]]+=value[1]
        distances=[min(abs(p[0]-x)+abs(p[1]-y) for x,y in _K29F_HOME) for p in positions]
        farms.append(dict(money=float(farm['money']),hands=len(farm['hands']),land=len(farm['unlocked_quadrants']),home=sum(d==0 for d in distances),near=sum(d<=2 for d in distances),distance=sum(distances)/len(distances),farmer=list(farm['farmer']),counts=counts,yields=yields,ages=ages,on=on,ready=ready,unserved=unserved))
    return dict(step=step,farms=farms,inventory=dict(obs['market']['inventory']),prices=dict(obs['market']['prices']),shops=list(obs['town']['unlocked_shops']))

def _k29f_vector(now,target,item,history):
    step=now['step'];hour=step%24;day=step//24
    vector=[step/720,hour/24,(hour%4)/4,(day%3)/3,len(now['shops'])/8]
    vector.extend(float(item==p) for p in _K29F_TARGETS)
    vector.extend(float(now['shops'].count(s)) for s in _K29F_SHOPS)
    for p in _K29F_PRODUCTS:
        vector.extend((_k29f_math.log1p(max(0,now['prices'][p])),(now['inventory'][p]-10000)/200))
    for seat in (target,1-target):
        f=now['farms'][seat]
        vector.extend((_k29f_math.log1p(max(0,f['money'])),f['hands']/16,f['land']/4,f['home']/16,f['near']/16,f['distance']/10,f['farmer'][0]/10,f['farmer'][1]/10,f['unserved']/100))
        for source in _K29F_SOURCES:
            count=f['counts'][source];product=_K29F_ANIMAL_PRODUCT.get(source,source)
            vector.extend((count/25,f['yields'][product]/100,f['ages'][source]/max(1,count)/30))
        vector.extend((f['yields'][item]/100,f['on'][item]/16,f['ready'][item]/25))
    for lag in (1,2,4,8):
        old=history[-lag] if len(history)>=lag else now
        for p in (item,'FERTILIZER','WHEAT'):
            vector.append((now['inventory'][p]-old['inventory'][p])/100)
        f=now['farms'][target];before=old['farms'][target]
        vector.extend(((f['money']-before['money'])/1000,(f['yields'][item]-before['yields'][item])/25,(f['home']-before['home'])/16,(f['near']-before['near'])/16))
    assert all(_k29f_math.isfinite(x) for x in vector)
    return vector
