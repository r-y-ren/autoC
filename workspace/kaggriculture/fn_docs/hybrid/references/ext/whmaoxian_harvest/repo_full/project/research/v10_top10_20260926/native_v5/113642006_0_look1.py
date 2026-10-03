# Locally implemented, observation-reactive executor of public production intents.
# Historical episodes supply task targets, not hidden live opponent observations.
import copy
_ITEMS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')
_SEEDS={'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}
_ANIMALS={'COW':400,'SHEEP':500,'GOOSE':300}
_HOME=((4,4),(5,4),(4,5),(5,5))
_STATE={}
_REPORT={'errors':0,'seed_waits':0,'supply_waits':0,'weed_repairs':0}
def _walk(position,target):
    x,y=position;u,v=target
    if x!=u:return ['EAST' if u>x else 'WEST']
    if y!=v:return ['SOUTH' if v>y else 'NORTH']
    return None
def _fib(n):
    a=b=1
    for _ in range(n):a,b=b,a+b
    return a
def _tile(tiles,p):return tiles[p[1]][p[0]]
def _home(p):return min(_HOME,key=lambda h:(abs(p[0]-h[0])+abs(p[1]-h[1]),h))
def _command(obs,actor,tasks,state,needs,seeds,stock,claimed):
    seat=int(obs['player']);day=int(obs['step'])//24;hour=int(obs['step'])%24
    farm=obs['farms'][seat];tiles=farm['tiles'];positions=[farm['farmer']]+farm['hands']
    pos=positions[actor];inv=obs['private']['inventories'][actor]
    pointer=state['pointers'][actor]
    if day==29 and sum(inv.values()) and hour>=21-abs(pos[0]-_home(pos)[0])-abs(pos[1]-_home(pos)[1]):
        return _walk(pos,_home(pos)) or ['DROP']
    while pointer<len(tasks):
        task=tasks[pointer];target=tuple(task['xy']);cmd=list(task['op']);op=cmd[0]
        tile=_tile(tiles,target);distance=abs(pos[0]-target[0])+abs(pos[1]-target[1])
        skip=False;replacement=None
        if hour<task['hour']:
            return _walk(pos,target) or ['PASS']
        if op=='PICKUP':
            item=cmd[1];quantity=int(cmd[2]) if len(cmd)>2 else 1
            # A historical pickup is additive, not a target carried-inventory level.
            key=(actor,pointer)
            outstanding=state.setdefault('pickup_remaining',{}).get(key,quantity)
            skip=outstanding<=0
            if outstanding:needs[item]=max(needs.get(item,0),outstanding-stock.get(item,0))
            if not skip and not distance:
                take=min(outstanding,stock.get(item,0))
                if take<=0:
                    _REPORT['supply_waits']+=1
                    return ['PASS']
                stock[item]-=take
                if take==outstanding:
                    state['pickup_remaining'].pop(key,None)
                    state['pointers'][actor]=pointer+1
                else:
                    state['pickup_remaining'][key]=outstanding-take
                return ['PICKUP',item,take]
        elif op=='PLANT':
            crop=cmd[1]
            if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])
            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']
            elif tile is not None:skip=True
            elif seeds.get(crop,0)<=0:
                needs['seed:'+crop]=needs.get('seed:'+crop,0)+1
                if not distance:_REPORT['seed_waits']+=1;return ['PASS']
        elif op in ('BUILD_PASTURE','BUILD_COOP'):
            if isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']
            elif tile is not None:skip=tile!='LOCKED'
            if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])
        elif op=='DIG':skip=tile is None or isinstance(tile,dict) and 'animal' in tile
        elif op=='WATER':skip=not isinstance(tile,dict) or tile.get('kind')!='PLANT' or bool(tile.get('watered_today'))
        elif op=='CARE':skip=not isinstance(tile,dict) or 'animal' not in tile or bool(tile.get('cared_today'))
        elif op=='FEED':
            skip=not isinstance(tile,dict) or 'animal' not in tile or bool(tile.get('fed_today'))
            if not skip and not inv.get('WHEAT',0):needs['WHEAT']=max(1,needs.get('WHEAT',0));return _walk(pos,_home(pos)) or (['PICKUP','WHEAT',1] if stock.get('WHEAT',0) else ['PASS'])
        elif op=='COLLECT_FERTILIZER':skip=not isinstance(tile,dict) or not tile.get('fertilizer_available')
        elif op=='FERTILIZE':
            skip=not isinstance(tile,dict) or tile.get('kind')!='PLANT' or tile.get('fertilized_until_day',-1)>=day+2
            if not skip and not inv.get('FERTILIZER',0):needs['FERTILIZER']=max(1,needs.get('FERTILIZER',0));return _walk(pos,_home(pos)) or (['PICKUP','FERTILIZER',1] if stock.get('FERTILIZER',0) else ['PASS'])
        elif op=='HARVEST':
            skip=not isinstance(tile,dict) or int(tile.get('yield_units',0))<=0
            if skip and isinstance(tile,dict) and tile.get('crop') in ('WHEAT','CARROT','MELON') and not tile.get('watered_today'):
                crop=tile['crop'];age=day-int(tile['planted_day']);low,high={'WHEAT':(2,4),'CARROT':(2,3),'MELON':(10,12)}[crop]
                if low<=age<=high:skip=False;replacement=['WATER']
        elif op=='PLACE' and cmd[1] in _ANIMALS:
            if isinstance(tile,dict) and 'animal' in tile:skip=True
            elif not inv.get(cmd[1],0):
                item=cmd[1];needs[item]=max(1,needs.get(item,0));return _walk(pos,_home(pos)) or (['PICKUP',item,1] if stock.get(item,0) else ['PASS'])
            elif tile is None:replacement=['BUILD_COOP' if cmd[1]=='GOOSE' else 'BUILD_PASTURE']
            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']
        elif op in ('DROP','PLACE'):skip=not sum(inv.values())
        else:skip=True
        if skip:
            pointer+=1;state['pointers'][actor]=pointer;continue
        if tile=='LOCKED' and op not in ('DROP','PICKUP','PLACE'):
            return _walk(pos,target) or ['PASS']
        if distance:return _walk(pos,target)
        if replacement:
            if replacement[0]=='DIG':_REPORT['weed_repairs']+=1
            return replacement
        if op=='PLANT':seeds[cmd[1]]=max(0,seeds.get(cmd[1],0)-1)
        state['pointers'][actor]=pointer+1
        claimed.add((target,op))
        return cmd
    if sum(inv.values()):return _walk(pos,_home(pos)) or ['DROP']
    return ['PASS']
def _project_stock(obs,commands):
    stock=dict(obs['private']['shed']);seat=int(obs['player'])
    farm=obs['farms'][seat];positions=[farm['farmer']]+farm['hands']
    for i,c in enumerate(commands):
        pos=tuple(positions[i]);inv=obs['private']['inventories'][i]
        if pos not in _HOME or not c:continue
        if c[0]=='PICKUP':
            q=int(c[2]) if len(c)>2 else 1
            stock[c[1]]=max(0,int(stock.get(c[1],0))-q)
        elif c[0]=='DROP':
            for item,q in inv.items():
                take=min(q,max(0,100-sum(stock.values())))
                stock[item]=stock.get(item,0)+take
        elif c[0]=='PLACE' and c[1] not in _ANIMALS:
            q=min(int(c[2]) if len(c)>2 else 1,inv.get(c[1],0),max(0,100-sum(stock.values())))
            stock[c[1]]=stock.get(c[1],0)+q
    return stock

def _market(obs,commands,needs,target_hands):
    seat=int(obs['player']);step=int(obs['step']);day=step//24
    farm=obs['farms'][seat];prices=obs['market']['prices'];stock=_project_stock(obs,commands)
    animals=sum(isinstance(t,dict) and 'animal' in t for row in farm['tiles'] for t in row)
    reserve={'WHEAT':max(3,animals,needs.get('keep:WHEAT',0)),'FERTILIZER':max(3,needs.get('FERTILIZER',0),needs.get('keep:FERTILIZER',0))}
    if day==29:reserve={'WHEAT':0,'FERTILIZER':0}
    orders=[];cash=float(farm['money'])
    for item in sorted(_ITEMS,key=lambda p:-int(prices.get(p,0))*stock.get(p,0)):
        q=max(0,int(stock.get(item,0))-reserve.get(item,0))
        if q:orders.append(['SELL',item,q]);cash+=q*max(1,int(prices.get(item,1))*.55)
    count=len(farm['hands']);hired=int(farm['hires_today'])
    while count<target_hands and len(orders)<10:
        cost=_fib(hired)
        if cash<cost:break
        orders.append(['HIRE']);cash-=cost;count+=1;hired+=1
    owned=len(farm['unlocked_quadrants']);wanted=int(needs.get('land',owned))
    if wanted>owned and owned<4 and len(orders)<10:
        cost=(1000,2000,4000)[owned-1]
        if cash>=cost+20:orders.append(['BUY_LAND']);cash-=cost
    for item in ('WHEAT','COW','SHEEP','GOOSE','FERTILIZER'):
        q=max(0,int(needs.get(item,0)))
        if not q or len(orders)>=10:continue
        cost=_ANIMALS[item] if item in _ANIMALS else int(prices[item])+12
        q=min(q,max(0,int(cash//cost)))
        if q:orders.append(['BUY_ANIMAL' if item in _ANIMALS else 'BUY_PRODUCT',item,q]);cash-=q*cost
    for crop in ('WHEAT','MELON','STRAWBERRY','CARROT','TOMATO'):
        q=max(0,int(needs.get('seed:'+crop,0)))
        if not q or len(orders)>=10:continue
        q=min(q,max(0,int(cash//_SEEDS[crop])))
        if q:orders.append(['BUY_SEED',crop,q]);cash-=q*_SEEDS[crop]
    return orders[:10]

def intent_agent(observation,configuration=None):
    step=int(observation['step']);day=step//24;seat=int(observation['player'])
    farm=observation['farms'][seat];count=len(farm['hands'])+1
    state=_STATE.get(seat)
    if state is None or step==0 or state['day']!=day:
        state=_STATE[seat]={'day':day,'pointers':[0]*30}
    if step==0:
        for key in _REPORT:_REPORT[key]=0
    daily=_PLAN[day];needs={};claimed=set()
    seeds=dict(observation['private']['seeds']);stock=dict(observation['private']['shed'])
    tasks=daily['tasks'];commands=[]
    for actor in range(count):
        commands.append(_command(observation,actor,tasks[actor] if actor<len(tasks) else [],
                                 state,needs,seeds,stock,claimed))
    # Prefund imminent seed tasks rather than waiting at an empty field.
    seed_need={}
    for queue in tasks:
        for task in queue:
            c=task['op']
            if c[0]=='PLANT' and step%24<=task['hour']<=step%24+3:
                seed_need[c[1]]=seed_need.get(c[1],0)+1
    for crop,q in seed_need.items():
        needs['seed:'+crop]=max(needs.get('seed:'+crop,0),q-seeds.get(crop,0))
    # Buy upcoming task inputs before the unit reaches the pickup deadline.
    # Only our own demonstrated task plan is used; no opponent private information.
    next_inputs={}
    hour=step%24
    for actor,queue in enumerate(tasks):
        pointer=state['pointers'][actor]
        for task in queue[pointer:]:
            if task['hour']>hour+_INPUT_LOOK:break
            command=task['op']
            if command[0]=='PICKUP':
                item=command[1]
                quantity=int(command[2]) if len(command)>2 else 1
                next_inputs[item]=next_inputs.get(item,0)+quantity
            if command[0] in ('PLANT','BUILD_PASTURE','BUILD_COOP'):
                tile=_tile(farm['tiles'],task['xy'])
                if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])
    upcoming_stock=_project_stock(observation,commands)
    for item,quantity in next_inputs.items():
        needs[item]=max(needs.get(item,0),quantity-upcoming_stock.get(item,0))
        needs['keep:'+item]=quantity
    orders=_market(observation,commands,needs,sum(h <= step%24+0 for h in daily['hire_hours']))
    return {'farmer':commands[0],'hands':commands[1:],'market':orders}
intent_agent.telemetry=_REPORT
agent=intent_agent

import base64,json,zlib
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlKThAQVaqWNMGavT-k~djqY#~f&Q1lUU48bsv00{ylId%e^Ajp3YWy{uFx~kTy-90nk$AKSgL)_}-^zPkNwQj%p?>GPSyMO(MKfL*?`u5F#{O%9`^7()L<~RTS=KufK=l?Em%lB{J{M)~O{-1At_089R^Xp%|dHd$uU%q?y`M=}mfAUZN_Mg9h^H=fhoB#Kpzx#*Z|L$M^<MaRdpSN3!-+%S>yREfJTANPS{@tg~YybA$`wxHj<}WL&z4E)SKE3<+(~2goh}N}+z4GE(Q(6(MYsF|Uy|`Eue#H!2t=LO1uO|HRY2#|&{qo&cpH7x`d+FuXgx@~eS4+WOdU3UM@#BC0mU|V%?VSIz_-DWV=Karq`>U_M{q*aP?|!;+u~&*OQI(!ya&GJ_zeH175xpBb%Wsjiu@i8$VlM?ZcHFocxUr*hwLxvQuRnYTY_xo`l-p=|<FvlGX0^}xufICIR0lo`fByUZ=?DGezBA6;pBDf1yLUeaj@&HVUIgCO^Gn1m{dn2jA=O@bxkH+?h3%^id+FuXrnDdH+iLE|vmd6M?0<7VPU+1t_hS^!_i(;+^Y=;i(#zi`OH16(KJd>z`k#IDJo{olz(~C1+O9d>rRGJOy;9gUVhNJWA2!%aFMrr5J&VNev&4S5g7Wq0(vq;YNiGlcY(4DL#XtY};aBFDDgsX`*}tK*wAjC;w6xj3DfrHQ|HD7|=imS1Z-4m5fB4hC<4^zj{)d0<j~!dmJGQSsynp}h>rcP^>vtbNee?dC|9ko{1KzWpEPp$v{n}^f1~U7#F6{PceD%?o(&fA~7;JGQpC*N@KBBy$+Qr_*iow=IiD>_S{FzU7QOeSxlEIyvmv?fNZXt;euh`E{yXR^@NNsrsmY?snxc<5WTj}DWj`BZ>UmJ2;CHp)*JxS}KC+YdQbkxBqU5{@(_^E(&m^pg;=xNY@`oRA3tB?QZ-M3I{ZV$%>JwS?+F8HqY>JdjEv?Y}8aPC(6Y6F<e|K5$RV=u>o!g;U!-gGI#oP@vl@ZsBcrzauM%3p8#WH0(tXZ7`mv$H8fBZohpx>q+E3q4Qi^vs4H3#GtTX7Ugi{XjSRn-ErZh}>l^%@>HH)Yw%68fFN)YTApjCmzLJrH%c?1Fq7bP^Xcd$)huohgh<`<a#d@90j`ktXBROfl(;736f(IC{w|~Pxb;o-%0#@r||O~;8O}82?5v!6PkJa@Yd>;I$9>JH$j>0fhy1^B9KY+j2IntR^(s!NPpcU{dHGf+CU!+akcydY9vSVPi#XT>54q~l-+ak#Lvkw++F)s(@`(?D?0oUAbaqqiGmB<cBFwoPR)MG*GFHp7fIk)f-uTWcoW!=7q5A-S6~BTWu(jxABQ~OV7Xe#5i;x*R}Xg5BltuQ)C&y^w57Qzja)cJ{$aI225O1L{@NO6FQC@)CeV6kU<@mrAq`@kY@Q+AUW%1qSuXRY2fJ*$*YSD3uZ^*J8vCQpLzr)H%jaMLXpO+Y5%O<8ef;XXpS}C|@$c;sxpJS0FPr44`s0-O=S9t2IFW)~iIRs)@E<N)EQ_s;aFe3{{5RgOftOzO!2>0M@A;Fx<odnMY^#iXc(7VRuBcLEM<nu_EjPe<4RhU#dy@Gvj*IrC?Se*+aV9-Z2acnQU6AY*7uU$okv)f$R(>MfAHUAOz|rCg<vb?3cgl2k$AhE|=RqQ$*(FLsSfeNfnqd&srYg|mi%gF%3f=Pe_4ag){S?uT?DN5QGZxgH_@rJMpgmRZJ91(Y&*g|~N+zN*0Q<T<HBgIGoOIX+CM<Mm0Hh*yX#+xIHoG){x}}$Irvux3e}dGH=UwqruP6PP5A;Vn(Sx@_H(QneuxCo-_2W-Hwh!r_WM10hvfZs0p!sg>m$$Rs=VY5tq~gF-hJ1~p06&!mej3}N#lf~{4(3)|rNXA2L`G<x3skM@C_B<0pe0eQ{K1W@(uKUz7bt(<#Q%LWz*6HUSS#DyV46XQ$<(X!t9oufVZv>PvDinyu-|Z6z24Y<fW}cLT_Z%gMo2*QryWq0tsWx)-DCZ7@^DUeY#grMsJ7N@^h2jvAV^&SNa*aDr_H5Ov(dJfwhc-C=Bz5&>(!Dr?b)py)I$#cQ=QU7wTVbkdZ;!LDcMUe&VUSDOxn0b+5+~*?e<dX?>MAgg!ML&?QLjfZev@Ou~RdoG%9hgW(X~}WsU<_Z#N!g8>?LmP!K|p=GFITuVyFHtU8Uk5_kYC@c>x4g;Wrsy1-Nw9?9(BS5r7`yZq5C(uxdSu-VHs9QCIa1H9n0m#f?GbP0x<Ngus|I=7rI0SD;SUa#)y(<K4B<gnMPrT6K>w+;ECy;Maa(=h{!tAn+#4LJr~=;x)OPNjz&b5&>a({mW$Ati3^0&&29S~0;34tu!<L7%R`4k@X`p2{heq$S`fRqXXDHh8+k1M_XKS3jetOR!Ta1$(_JC`!jnk_|vvC{a3~!V$mEk$tS)HUX8MXh)0Ugt4y*&Aw_h`)WuHGWb0VQsWA;w@#bRu=ENyl**Mfeh0?9Uu1dQ{guMLla-y%_T47HH2Jsi(tyHuOPTMMs!SWm@(9Ht?9fM4!v09a-05nD0}QRs_eWvpV!&Wkp%`s1P;BTDL_AJ>i|_DOZp-8#gx(NX>>(}UBbtBRqfDQTcV?^rtUFR^$^z(h6qQCnefxgMGEc<PhSKdhls;f6O$)6(sOqkKok<TO!`g6NJ_~o0++EFT>fsDfi?|#f1J_NQ)Guu=g`|F`O^Vse%8+j4A>HO-gA0WgIx}<?qMa{9vsJ`3`CX6p3hm5$&Q&+(s^#`lIaI3g!=ZCv7k?Pkh`Dd?$JHwS)}Bun(Z2X$FVCjJM+Yd>t47ni`XZrhtorf+7GG(tCeT>&yG=6AUl+&VqCLXk0tv-x?B{IKU$Y>sNSr~__EIr;OG12`{K6G`g~sjQuG%y{WdcTb5<pY^<z4lZcbS%MXIi?QY3X+2rQ4C0ZU>Kan|5|dICBM?Hst$H8}gbaIi3FPkmR4dxm4X5r%Rf7wQMg{C$gtYItD^Dd%e2D^2yWa4jZ8D_392iT{0Z(;_db7S(SyE##OmYsFDBnoA-Z%xJzl3^YAO+kQf?|f+_7Oh%59+uioCQ_H;@iv(<sp1_cWs;$5SebAu<o1)jK;c!opaX$p-doW)7Q@iNzBah9@dwn0wega1ny_%C7be+dKsB@7#%B{jcodnx!43>#mh%d1U$Dfs;hZzor#Z!d*EeLS&vjpc_OP?IMEPZSo%Xl{k3sUiGbn0ghpiliK=Qo2SS!(L9rfkt2#CG1+QGkF`zC^uD^Crt^>JYO*=gf?M%z+0Ya9421(UYB&>v}J3YEQcV4HD6kJ>KGlO)I~vl+$aSuX`{l|DDtI1+$aSuua@nlU?~v&r9k9Mf#@#<B3}wbe<=`&Qotmfo}*P?qIChCUMrtol|{G25kdvh#DvXQPF}RlkgsU3lS96ey;w8J*<PWMcJk)0qM>71{~fR4<8H6kCJK2ee3zG+J~T^rJQhn=0h1A0@7NFE^7srvlo9|J!<E`AKvx6N>ouS&L6nYjr3=l$%m6Av+l^MXwC!wVJJ#UzNN04#cu?l4W>W#NAL=0t3+=~qB*Lw?sryksmzc_FEpIig7zIKT(@5hgd`LSwL_W@2<F>YgSRM^de7>=n#%>HZxk3lZ`>hIn0M)EipiiO_zOL>?+*ZHgnCx|OOOfrx8qB!8LVE%7O|pq0qHRiRQz7|0_h6fmoc%Y=rkY@)6RrTtO->%EjP??vd`XmCJnsmmh7~Z?$Oop}LZn*#R^V*`i7etEqC+4V#C+lDIpSd-*|M>qKi>JLcJQtsr?)xCpQ3CGKF#-kd%5=hpFXYWa0S_3uVRm<kJ~*;PW&i2`A5mggDNk&2rTMt`7Ba}dOCQyec-vLiRYf~nF{X^Zbx3Y9r=u!`y#7_-bm#z`BPYuKgE?EMYa_%V1y<emk5l|?Zp};V0(oI3}@1O<%b`2_lzBJ!)1HLI#HzC7lFuRn8YdCTmz^|#%Kz~KKda98MD<`_rcy;a@`yPhb`pbw|q`Nj+p8t;!7y_Gmk)<FafecOqSg;GwX4tQIj3sW|PICQe?5Nw1}?B5~?$F8GWg?2YSj&g<;{t?vX2kf+6UBV+jOwsW9nEApk32&=%7HIapHF=2-vb?hxj4!}@}JBaq4TXqWjPzyuj)^&<o5#?GHRElZobarVO5U*mdzWL_vBQulc{snDe1vLs&*^u#|bP5gcDiBjqU=A5YY&Zf%kk8I9U63|?cx$Wm7rZ|<QMau_1>6eZm<->MTp#2vPb5l@sB$?KcR9Z*UX&uSrWh9Z8kz`&*Qh6Ck=QVqCPu+f^Dec&~BIi#e&UP7^4MX`@4th@lDQq`GkWW7%jrZV!#MYgr!N)*z*(0xnlM9o9jm<GF;h;4KvI?LpPd2(`5wdikd+?sPVD_=|p%ItVZh$ABHg<-Xt8)#l(A=5DgJaD_FVoI2jTWm7TdYP8pJ}(3%)7m0l{5j^bxVJ%x|`E?;&YJ{=uvKi0zWxco)HikfZ7s*M@L$TF_rhnnv*PwhR03|BL{7+JZS^BNN27=-m@s!mDYS4R42v0U=1^GfdDt)yelN5KGWVVi5~hSdg!BYv1!}s1n|9$QjDj3U+sE8mq{rz9dL94mF3V^WAc2J$n#Y)pG{DCRYvEdC+Fjg4);_CietURVy~ISUJEPLYil*|UI8A>rM0?^cl3*u2Eudxy&5#_lK~MMFxdC}z5wVICCMQ;aprO2m>Ap_!pvl#xU(?sTtsmL%}E1rUjlJU9<!{*J6<)Vp&fn;uu0$I<y34ZG2$9dEHi+3V7altGJq3rY^cebo;uv&0G!wukYvihuJX6oXk2>Gxb$4Zr4f`FGf59Spv(}2%i^(#g?uxMrq+X^xX66L%!UwTkjb~b;`;51i!-J5oX6M}rX+}!D}i_MipLI`l0%v{UeYF4^fcyN`M}w#iX6M!XddyXhXHF8!%Qzp+jpw*+Nuu&Ee(_X+6MnUA3OtbC_Ab7omV@5i-U%9WwTZXHXHodZ17;SivF_F0?JMcASW#=ly~anxw4b5JR_<G9sGSx-nus;uJw*2zQ~3-#5D((piR$j5(ic&7kaD>IMN<sdtxg$yGaTR-VFhRlDhJKRy}jS2!tECO|9`slOxr3CEd%BYD;)3?<=Q#TxZe6aOk8}dX1J<cANce4Tvy7W!Q~DllZ)(q>^p`8VpoWE;48y7^o`@P^Zjd5FD(o;b5KCBTin97<oBjw&jRhty|qK`lQjE#70A252a#cyl64FsxVlWq7}XuymgSQQNx*%z2y2p&i(|o!rx-$m6IZ0y&R}#%nVMY9Kr~0R9RrFtpQsAP9;3?{je%c3YqK&4wHHL@G@-pJ(q{?auDRIf##nt{N0BS@6RrIw3jAmk6$>)WEn}CwDd2~tlC6_L3zIhGV_IWq$$OG(0WieXr$?Mhhd~o>Enx*J_5MirNzf?;8Ui(5fy|7fRe7>qlvo{ZjQkB!=VyC-A|tBenO}FmA}s>>*E?fBih#FZM2lU*pLq?Lf}JVu&U=MZ9ap{-)G?^q1|3W(BQ!B<v@bM<J)cG6U<CcFtcldnfVE3LbGl$qt0qCAqp?|1T*pz%&?{bB&xQ+LE_jgW)GZ}?Wt<^4@O<_jtS{~cwT&GY4L-W^h$N(sf5#{KVy1c;c)8up%HmU_)Dt)_A!jc$mf-qxpR2S5jGzwDWkY}&`QDZIEd>~+7FGmdJL%|(+QvQLn_H^OBzvItcQ7lES=4RQeAfA3t;oPyiShYjff)i(GwluEPtnOrDgr$x$N$(oY!FfMEk8Jhu@m%Y;*`CfKP$GE?I-$&N=ezgS1<Tp!!M31N`8%jV|aoYnxMHRxuD2Lk0$3Ea`xDW`;?Oh>~`&VqMyrIMUX{k&khb1-)>X&^Gjc{boJBm^IsAKPd~O!G4)eFzf~BxK|+vM0*81_RDkvG%U<5Hkyl}PLVF7j-?13Yk5pl1azym1)pP-Rxo@H#%V_}YvHQ}*pm1V6J)f3INtVHi>-BOP}^f^P@y#Ef*F*63eU09z($&PP-t#Lr3nGFE2?~$XFfXRKDnApBVv@K*=XwN;L|9BConVm12cKyuFTw}sR<niak#)tUR-?1`F-UISq0sW9xL7Gx6+Ngm9AV}bY5E9J<?h%5LL#;JFl-*EpKFvZR4epU$W-a<zzijoxiTmW@NJ3ea_btEShL^1aP+>^!+*55z*n?Ei+l&nSPni^ox8jUtn-z$cj?#npC<Bmazwp2@v1K#LBr2;VH;70-o3axQm#c8ki}G@M9<5ZFDtcA{wf*Nt>KPUH|T;QpG;PNy3E8LZ~b{-Ph3R!J^Z1k@FB~mPMjv1=-%u1gPc~w%GKTE20DdN<TIvooRb!HL75^lM3b`8R_O67gJ~F-58s}xVg?dTo1dffCpDWd*!gQLI>#tkXM>60<$ii7C~Nb@PKr-&{!A@4~t&UnMQ*vjRrT`qd46{)QwdD*^hWFMbkc@MX^R<J0_a;Sc~FlT&W!+=Y9Zm*A#$f)_&mDM#YBj@OY3^+ox0Uy_|~8O5`?uWqaXf#gOVfV^I_c&`ak$A<gDPJFmS29Y9)yvmr%%yn`ZMF>|W4nNz2|oF?zd1duTe8=U>pR^$pk4wh(pn9=erwC)caFWXk|((9cx-6<Tq0<BLciw6zyE=%S<=Z8pH%e8E4SnSwMq@7gcGTV#DtnuUtor|6kqXu~L#>I*aG3ptGe4EP3ysjRU<(80o7y&(HI59cKG8i10Juwc&ALCH@TjXP*krD=tR`UeN%I9KVu^`_~Gp!`JMmk+J(*oMX*xgtiS*x+%9Q=!qtViAWQWRPxT3x=;ytZ`ks>rY#>X$rO?a80jp7^ZxxR%v!v<j4!j672aSgY`ey3*rQXF>K;=GadtlsM_s*g&Vo#>F{CwreAUG(uv-ND*OKHB7c<OlhqI#5}d{Ago<-(WVht$d*`!Y`a4zJN7ct)^)Ox#(L9kpsViJUHyLDjladtYPplR$F;e~@gCjBXURfz1XZ!y_kv_qw;<UWv~q4Bm;rdA_1~4Y@@{Jk0Ys?_7jFTc-rUm}c?posEWRqY&c&gtZ7hhpB*YCY#w=UruuNUm2wqlL?3r!zm%VXXdNr#fXf(>$&UT32GoPY>1@<@HUWEq7W*VQ&9!0}2mL)zuC)<!Kk%cq(ESzBs&c|*(;R9`c?<&D9G}@{tAP230lt2HI|Asrz*1?-ScRsZ95NaTB2A0hv0sL$l4h*)y-pdfyE1gZ#cQ#G_Y?{8aY4T^&^qozUKbxkmP)LzRvSkYR({y}S)A8s5rvr~LD;7Ks0n6*N0Y5!{3*`llMlf%qo))$OVWq=1?<4BO#v6M#kLybG<t5S}b2om5!F#R%H6m~h?<9>)YeCP64SG&|&~si;x+()#lx`ds$-~Jbb}fr+;7UukWtvd-;Do3z+-Yr4`E!w%E>+rosMGdC(-p~sxCz1ik3&#ZeS)gW3#u|GsB(CK$EOGQ(*u0b1AJ@y7oLGqeZJhC7se0AcMU6XJ>u>Q*zIupK^=+RUW1qtV49A=mzv4rc9{KchlRhz%9pj><90awZikLY#$Z?8hV<|e_3Ti{^MhxS!{nsh)a{UExucE>K4E&`sSfL5xA)biJ3=jwr$I!T(qP$$JCx>W4Lp#Fl|b_pc;R@YNe1^2o9?FizPMplCZ1VMc4IZ!k1<v8IgX_T|FBg(_r>3_I@HzjXgsY=R0yM{28;T(SqQq|Wt&x?(_%nVCtAQ09USmv*5uV?5#aE0YP2)cpxvLQ&1W#$#MdwF4!n7?HlOPrSMlL@6`%Ai$_dd!I|l%V1)W6-z0+ywoz5)zJ~mph*^i>@ugbAS-XI{pLtUq3?HrVmDL=WmC=e_jf#5-0U0h(u8VJgp$0xduq%A|$<|f_7hxMp2=zyq82SmdKK0hu#wW^G(ESJ2-a;f|ARg%NuHMt#L6U%eS{5(H<s4>~^+mJo>-7epT<ne8AIL=2;zcIBFw%I&9v=5kS4;5^Ruwg5<mrs&%_*@#Xyo$WzKxSPO_!C0K=<<4ThaGiv_+`iBHq4d}Ejqo}a?EbLFumKVZz^J7i9M+DQD3mW910CY<l>Fhdk<FbJs0O8f!4ctBq(J!ElI<NddRFM1$G{k7WMU*a2(8#L2$<-kWGDD$?Mwd0m5-b0eH_uW=u4$Yts)(WKKRv)uA3w218HG7+Z>C&aBgcs?|Qmvs(sIyUXNz@_Oy?rCN3y6JkeX^n9Vf=qt=k*2(955OSx3kjFv9Z;uQ79?=OR$zd-^c&80)*Tj>kfo<juY!k15jJ(~_<aIaGLmQm9>gGX`jx8DDia<d@SSO9J$_6XD<`uUu%L>~Rb0^zL=pi-xr+d$oWMfkQ%1iw_PYal|JAnLj@2hrBw4J8vbv^x7*MSEz;z5FEQ!I+<q?;?IS1#KVwjW=bms9n?2|S6SxUzd24TJOA>UmF*^x&(mfm>=H5X}o3a1|~Q2_=nmR^fa|G%skzouRp%gN&Px5gzMm=jO|&9=ynTvJQS%*wNDj++hO#V7@6&6Y!U10=`s5G*20Qh)~tax`YI$)8~j1ca*6TN@+|wS{=H~*gb=z>6mIs$f}z+|6<@&heGeRCfsla)LwqvT7IPi@J#ls55}jGx~TaqNd_-@ctDI)fr<_ZHO9tjsu%Y3TVV$tT8%t{o;?=v#cvT``CFvZkmcD)p=T%MzCPF)d0P<0X=Pi`&UU$Dt!16Gd^FPX&$QSTXODdJ80^=TA)LuDa9yqXSP9@yiL7q;!}H?v5-(o(`I3haa}VuRu`oTL$nWrk1_Gk1?e}e2i9#;n!$urUD^UojlnZbDN|^^Z3y)Mb9;qC(8u|XZT~$u=Fj78N4X@^jr9kI-#ajr3U$2*TTmy+s?g6NHlPz@u4-yBDXNWyX9{ep%heL^`ril<03QQTU?vUX_pk4HcQx(oo3gUT*U1*<=%0tLqI%OVO(5cGY5q0;vpfds=6pX5Y=(c1tLKNi&oDqKh%`eP@Jf2gYw_d_-uf%9c(UTb${h4vmlNsljdPV=#EAmq>PcULdzXH%@E{gA`x$~o&JL4F9;W2p2aG95wdj!&Taj-WXbe9y^`D3Cj@-WFWh{7Nd*N22?dpLi21+A~xR2%tJk9$UHd!i|BU5utBV?520dpJD9<8+&br$FDL7UohB`O*P4(ohcZi(&_$5#8l5BkJf;Q72w$Q@<={!u^;8YZlZruR!mhaZhQ76gqlz#(7a^Tv#oFJTzlL&#(x3DxwUT-I#a_n%xxF3LOlQXlGVHU0I3tj*9Dy`OYBx2FR&W6m@3_MRb%JN`^|3jUJzg*i^pt<b8#niP#4uVk^Ys1W2GLzO7QxWE<l~4OUL!Y8^t|2A*-7A6ld>59N?)p#f51tw=PB$aO@tI++*c<Q|NFL)`wr!r|JT_J<g*aBVp%yYMCv8Rt}Bb`-^zuHASSi|$L;p0tle3a>II8*}kg4TQVfKzPvi=a7g+kAHCT`v+(K7K_h6xbd?4?vdS3T0gI8y$X5&Gc3dHk3exHY)@JRj$~yM6=XvpkR|bzp4->_xqY3##o<fL4z$QUMf()rx>A0j+V~8!JIKbE*2Y7T4<ISOEK1!onF6KA@teo=tuJc$$7(1y5X}~Mh^g8y&n>em$K|we630;7yN2E7!K@d}z$@`)NQE{-k~LR-#lXuv-F-e>uY!RR7knA;Ge0`%UWIm{Drg}ErU=L(;dZTZ3<-rWp~^hJ*fRGYyy3)rBsYh|AKcK`aX3=Br$3b2ksI#uA=uf+(_zRk7(<2wY!Vcn(qj-Ij!)NCY^WTj1-qqdTfXj@mwW?MTf#v;dP2Dy?=9I-vLNSF8u<z-9ZtD`!snNAz8B3KESDb0QDO4ba*>UmAu^sr?!9NI@#&&70RiID262Wko<-O-KKTWaGmf{zR}z61m>Dn4{ZON~LS7PWk#g=y6_<@ogtzu(CW==uj~0z>D!h=6mmbQhv-RMn8#~)Ss2RDY)laro-!!?yB>t5T9PckXnj3CLmCKYRSAa^p0t`AcoX>WnHNcO`6nO0x^WbbR;IowNMdt-`vll?vDrRL5xCWThcPxcd83_jZG;5CR@mpIKEz8qo-tl1Nb_nVC;?M~+O*yV<`s7OH87uw8xe(x{G7;p6^ZFH$+2oMfR9^9gBo1a?2~=z)5Gu+k3!)rXrkw8A`PwW6j<n~`OIhf~;m8G>M;`l3JcwC5#{SiB?Eef=|1v|=QGmO%1_6`y2MCM)0Ff6<WnT5<kS}#t*aD*Q2WkBcbl!lv`}_*b0KVwt^|B*$eybdI1xj>q0;(@heehNX(~*9V0J`MXkR#D7%PW(s2LRA-lo0O;Kxq6ZzoAS&E?yw*mVls<MyfA`qx1G2gXZC;Kof-J-M*M!K*qvn7++k_N<g}Y?(jG`#DM^YlgDb)4TuE}<NZIw-ftH64p!|GZEvyA(McN)Xx3V<*9ZXq7G_={qPPb*i~y4PjgmP>DY2v@?dVuF3&{FcyE(GG`Vs0O!ayqd@)HuDpAfYTFRO^Ar=8F!7OyAo{Z@|rH%n=Cg}p}+RxkDfGNU!FCB&1gSBD|leKOy%!ZW)<+bd14YqVT{@Ur{BYub}XcAx#S`~6~BRUf7})^uA)!iquQJ_wM;tWcuXigve|{-Ez~+L$dYm4y8slkMPdiXSnxMDrN&55E!rq=!AoJjL{q$SWduWg=G{k)+KXN!q2A#X$xv5ZbloIg$CoLs2D^Ba9|+)9meu5^PJ4XXrWT7wMVk@Jw`|#q<^DY;0G23gLEp0cmDbc{3xG(3$`TsdN2Kv=>OSQQme+vt(RU`{$K3hz`CiU`D`jM+ET11H>PI@C@rHs~y$tH+#|fO9l*op<uhExv^?sfS7+NBDq7%3l!Zb;&$+5ninW#p@Z5G9fSjU>e=~@rt?m`NFc-DZ*kh7@>WL^c`W)1^&yB$jsg!Fj%S5g6rRFfX$pI%DePl$79tK{nul|wnRXn*!g$&jJdS-qA}v4`4GSEjg=kQ32W{oCE(h6<XL38!10jaB+JBzQLgs@tcyk4f*`H0mimoJ2E9%Ki%fcHi3-5GN-lU1+VG(PIE*d??S7$gCJd--xmK7Fy2pL^8n-+xoMJe_e)20$_ovM*`)sPA0F2jq=8(t)p`O$e}4S>Qy6<Q9u>#h7aR8t&49|Y&o-`bHw0T~q2=VwaBGbMv@!*fZFwQue=aRzkK+L0-P5tA$I{JgyeL3g418@#Vpu$P!0NYpa7*o)3*+tpqGsf4jaweE5B1rm+Oc;o5eVEc?bgr*2!(<5i*UOfEsJprU?L0Tk?^Pg?bKeS~hz)w6ThU@(HrmYD+KV|bl46x)0l!r5#CU096Y>Ow8xs5qP71|>}X1xa9Q8uv1Aa;xEUiMo{2v6DRsQXo4qUo_EiU(U(ef#O-SKs~Y-N%oAPa9X^Q+1Ci6-H9JpecoC?8h_q;~D#LeeV7F7yR5Lef;o=J2QO-Gl<IbewH!{NQ`*UG}hu}9AP2@J6LQFrp_z5WG{e*0GRzuk;Y4zgn4DCQF<*r@$I`ByyS;7c=>ZN@a`ACII99)l(~yy&Jt-d(qVQk+B;i(@hgqD#OS;w#$1nagUCUdAqSm5HGmwX&=){cmbOMH>aJjuNef3};MqFa<B3`Po|u)t#by(V3^~!B457?L`)n^Y%B!s<CfNIevQd_@aFwbI5f%-a`4c=!q)1beZjg`SNgQ%Sk|$h*$~npNBe?|V*G&K#Qk8>7IJ^gElSb^>{`0~QS!e?uz)t7v-iH0>IXQ-6+#`E`lYP(d_dSE}dxn3U@37xgm`c$RzmpatKyMO^gSJJg?F%0o-D!89dEc1nq+TcUK9H3)E4tKU3thNpI}G~Ksvc3p;SqIE_7PE+PrkTz5W#}Fk0x(n80{s-$&?=`kB4U%6)+S9bX$y-zDz&DPw@Jg<%1HbQ5sKixT$nn%{d(@)`->=k_lmYQ^5JgWS}k?*h~Pxh=cbx1UNRPJPzVhfNTeOh$Z-GpnlwNVoRrOYsO-xZQyk#$rFQ{{i(Kvzr|`>f|<U-kdv4^(~7+LSo8#vM$VrAyT!~Kl{`~oo+&XeDkbK&iG7QaFL{OejDppbcHJ0!jS)RQehK&SyDCgFe~-mB&@cf&%y*;PbY>!$WuRZ3?Xi_PbcLo}q}=V1Ts|6yPs(t5V}b5*gs+DqSw#b@lP6*#;}H{AZ*Jl5vD$z-6&TU@zzEvlFlaxZYzAWgfV+Al?8X&%NFxzGjK%Wk47?wRI9e-S{g=`>%5?PtiMr!XE+U?=4b9p)+Di!X`O^{Pa7U2aXT22lidCX3CWsOVnH@}zY4dWl-gZC27!PdwVOS0IN;u5auXBhnjSxm^8na~2DT%r5M8{odI(PFc+B$!WgBL{xhi+3I4o9z#=S1gZ2O;K~tL}byxhxdj{_}`X6hh{Y3hPnWCEE+g#BePbsCY2_=J8Dg0wEQl==K6g*9?&kWU#n<%-MEh9iXN)lTHzud_d#mgYKixd?xbdGb*f)a1I=nnBXP~YJzEch7R34bO_Y=Mcho{Ua><7EZq?Y!4%d=z!-^jvx<*<aWSeZd}ueLlWGj!1Meyy`Ou=wyRcN2_z6)(;fV?8)1HFcs2#DyQ-u{fxag_;s%+CZ@DK`M<}iS@;`9_yO1d1$G~3kOydVqYxq5(g!u354R(LGWRx&tSv8Bfv3F+nJ4rzza<cHAFkqQ<QYji7D2BPw(E%K^5tu>mg2r79*P${lSnmp8?XNJ);!)VtGBe2Y>o<x@Wr5J(p&*sTwX^02OYYH-o4%C3Bi4W8Q6tz-JxHBS3bQ-8-8OB&@p7bLk%m^ixFQyq84vZ)lJ->oPqZ>PwK!HXw7waIW5-p1Y@-}%Sr;@m4IkFT4d-eYAnFQN>Nw80!6NZKqJjqGXpPZEVTg<-Xq*r8g0#nbQ3?{7|9`?jdvjjO{c&23`Bcm+2uMwvs-4lc`>4{mOCuR}hFD=@4Y@8FBw&EzX^IoStD<;oC0!T}63o`vi9COWx!_Z9d41wdbbo80f_L?)EMzjAsH^WsJMZ;#Rn4=xc>mt*30|+mH@ZwWB19GL>ce2(47?x$xCSy>Hu440_4#{SM>&MeY5TomK0m<mnQlN^*Vx-xWAJcglb0(R#V+a-LG<kZ~GhOJJE@abqwlMS`n~{?`IR(}fMU&n>Q-g2=6(lzZ%57=Dwn{vqCetaAJO!sMQgFIM+~LS+P)xFEH+RGaw6Hdym9+uwfaQv;n%&Dc6iX#mr~`SCI^YUstG<}w&U>p2I%YUXXLEOS)O>K{Ekl2YLwHp9{=Inm_u}v03*WyN9(vz$BE{jr!oq<S%+P$KbS&%>G+g0Y^5GbH{#JNNF<JU1Tgu4_jF}l`&Xhb1tj9NKx>rEc<->m!2~Af!`Weym7-@F*=0#;#ezXE(ba31O3KSwCP`KLpyh0%+y2~tdmsuCP%w~6)x3DQt_i)&+@OpYjy(sS}3NUIcV5D14l?BVG%HLyikb2^z-Pogp$d?j*85f5tJr;**(f`RJ3`4F_lcyRbPwZ31W1moeHSHd&O^4FRC6H;<{n=AmvXsu6$1e9U8BrN=WkbxM8fymC+0pIvBtGpn?u8Sd5-Sgng_fY##Z;-b<IoqzG<47JtG9~xB~NkJlmmtBm27^Pu0z&?p)P-m-IAf2BT2nElGJzOLK?N5e#P%Te0YC;#U)K~_o$ec)7RO&cdUWBJvr{w0LmIXtOPnG{W_D+O$szAOeVB<zL1L>j6bxHi+miE;=?1m{W!vE2R7XXbBxHYg`(kQooUDiiviwI=M0NrFTjRhm{C>o7*#nOr<x~Ct9xv!fL&-pGuy8Sr9!%Q))k9isF9%)PYk`<lzZZgI-;3*N2o#raxy#_J@8~)fF~mlPXe`g<XxDPD}ZOg>Z(}Pd8dhT9p3+X1em`6u?(>2%K+Oi`=aB4E@VDO<L|Na`tD#aA<Sg`W(w0|rf?63tMk6(2wN+ZOC$UJ6x;<9vm>gsvk)D|7*`Y9fbk{~AC?b4kAZY%+@gcm$7xEkXfGiwI?{qgM`F)o%SF8L7TulpzrLJrILx5JGb!%Sq`0&e_XY<!67;<tW6_YWPhvIKc`bykvcl-TM)esqX-6(VGw(C0oX8P4`duU5i$LV*A&ulOfi$AJ;`AeUBj>eF@R;JnMS4o&O>wHn6sOtqP(t468lyJU)c2X>^$1B`Foglg=7J?aPR%<!q2GzUkg@MEq9dy;w}3Wl9cwHBz(by3e<SE+^CV#nT7?^S=ojxCI5lX^ml09r(0v78MpfeNSMt5Xrs7IslnJ;$qBqROldH663lEqNM{d;QqmQB|&dFgV<BC|SJpA8xOl8`Qc6)koX2wSbr(P)jF5R|I!KoKzEiwsq7@GXH2p%L_@lKH||ACkBOA%Vn?4uW&eRNy+fnaiGhY$!&DoE~PGTW2Gv?8N3a*rBq)zV$LN0Yaq4}9!V;{CTP??m1YQrs(OUvp%SbjdGNd_(gwI=^NxUk2~3GwFQc$f_Q%OlttZ=;gpgXm&^>ccc-r!OPF5M|~dnT#n?)<;V_OEja-s@u>tAoNuH(k*vI8Qr6a>DMboBc)&W?hd(jA7`z$Sz-z4S&l!QI51yr@CuIzqHnc_52s<WTz`h33eC7IY1q4c9_$>m@0g)GQA%TE(jm6Q%8o)JqjWUqKOyvl79!cvSB(3wkv`g%@o4A>V#89W`o1<cC#NgZw64O&960cA$i_lwh&?)1jkrE(3f!Mz)K@@R%L~9P@?^aj1qRkP3Iu>+&(<AGP2k0I%J>)^hadE6BOYS*(xn1@G*7$EDe+(nF(2Uf=TODa|Ve;5SI<gw7Cr+a6HC2$EjWp3~<C}X3fGc~3Kn$9srQ=+I#h)%Ku%qxN48>G1AwWDyP<S*MWc0`&vj<6Pv`ALYV{;)%lnj!e%;q(+%%a;xcX^>sUZNNrDoVu3AGT$5AWI6kCR2tEVE?2W0ybDN&>X({0Y8H<=p{N5fMfDW1q(03s~)Lf<He6d`n<<AJLL$@Jt4`f^!^7AsW13+&0$T~Oi)U}sVC~yJa`W+hYRv4k~FV@r0kjD^X*uskK*b`u;HWRha>8qo_j<Q)Zek1K;^EBZtR|5N#&OjwpGJpA9z3ru|&efsQM)2^m{L6{dhc*b~9IAE;16GP0`>Ks%^LqXN7bgvg`P#Yx_e^SrSCvlE8%s^V`aUZK3n}?0^W0EB$!Tv-IgPB;{uhRo0U<(Dr~QY8RJ>ai^iT;czgf&4J@0<QWS9(CWvy_7r_1<88)_#hzc|*+iQ8)zFCm8o(B5`K#C--NwR_m)NKwPHjiViR1GH^YY4m&q<kgR!5d<qlcZtk#0KoJLmJ-nXRgct0xFJIEea@_gWVfx^ZnZs&cuTD=2Qz6O`$345o8Gue>G9F~Il#^Zow<w+ocJ')))

_INPUT_LOOK=1
