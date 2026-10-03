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
            missing=max(0,quantity-int(inv.get(item,0)))
            skip=missing==0
            if missing:needs[item]=max(needs.get(item,0),missing-stock.get(item,0))
            if not skip and not distance:
                take=min(missing,stock.get(item,0))
                if take<=0:_REPORT['supply_waits']+=1;return ['PASS']
                stock[item]-=take;return ['PICKUP',item,take]
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
    reserve={'WHEAT':max(3,animals),'FERTILIZER':max(3,needs.get('FERTILIZER',0))}
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
    orders=_market(observation,commands,needs,daily['hands'])
    return {'farmer':commands[0],'hands':commands[1:],'market':orders}
intent_agent.telemetry=_REPORT
agent=intent_agent

import base64,json,zlib
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqUyo$Rapk|uJkLXB<bS`7$gxC-GKnFzgjXO80e&#BfW7NKz%C4b_odfMv8wAv#5s|-s=J5%BuZeaZdcu#H!|X!-}%$Ozx#(j|Ks2P%e%j7@8A9Fpa125{Pa(M`qRI^```cPr~j<)>yPi>{nP*a=^x*H`_&h}|Kqps-oN|en;+i2&p-X||L{-$_RsJBD!+gCzy9sdfB(;a{>Oj)>A(EP`-7#w`Quk#fBARce)#VDKYsf7?k_9FU-|9VAHMi_`<Vq;`Sa!e@Vk#6zJK?={AF?V7k}~L@;ck`f^xCouRnhL@|Oie`-Gw_$mw{6s2`E5zvB9@$WQ)^AK(A{E4QPs?YrN7{P^wVcYgJ2$>ATR{Lan)I)470Z$7pAYp?&zq5W7_ANDst-4XBp@bT+!{^sHf%Kp+HK79Z2)5Q|emWcal)nEGb)08hVAAH(>-SxjLo&M6NpSHC7rM_?M{ZbB}8ueEPp1A8@y=zZ{`>QX1<<l=leOUdULHwmpKdorLTy{UL`%9mG+R&CH_tTcY^vS15(zm4MzId*_%X+ajh_@lB`?Gj2o~hlK{*RIUrQq%&z^7GzDY&~N;M1nRl-OP9x6$zqq5Sy3i<7%;1liHl{kOU=isUbS`sHTr_wYZh_)DLDTGf{L`{D4HKK-<*-#FR(>(mEdy-%mM!ru>*zZCr43h-&gUkd(i0(@Hcmx6DW<bRqZf9caV%ad>N#~=T5)&D=}RQsUw#W!Dn{qc+M|L(6pe)|5aufO{5m;b-XKRbN+>6>rg`KO}-eO|$jNEgffO3FGZZ4}>=J@}|KgI}#Tf9ca(uxndK0e}9w`*U>u=MevBqgBO=J-8z0&?l!#p--;r8>XOp$8oW6ePPwF@vL8Z&<}d@|19lRR_{vz@5|0!?b^8ybD}y4H|wj`NziVY?*Eq9eSG!nU*E^p3!~ljg<<a)8F=XTULe<ZMx(3E#aE1(FZ(Kg#OVH#-+lP>-#&f^RiwAY<#*qI`tZYVK7RW2w|6@V$yu+Z>mPZrEzn8q7f+7N%Rl$t{tDG!q#V+6gO2D&hx^>w@<nf8$axh7^wR~3fWkhWR!^*iTNRS&R)vWE#1yt3P(NkR4V%R`U4TFS_URD1O6zo$Ht5=MK|hM|EC~B7@GbPo_g@p=ITya~TInM$a-hDwb!Pk&p7~R_@tmrQI^D>ad@~}^y=whOwZ86xx6==+iOOGRd$vLr>U=!9a79X#?sw|6Y9mAa!NY1p@Ma%#ZxsCA*l62HWS0^2Ph0eL3jah)d9`)7UhU~STjAe5g+E%sefy&&w>Q#yDfM+|LK~Rm2PU(be-JZznqBmD>PMo>!uj0Ro4lOLlP)=mxsd`xW30P+_2pmh7?rN{CwrO@y03gQz}YArtMwI+$M+WfIZ7_Hf(+Q`o~-Cbq1fL#o*RXu_!1QT;4jg_G4tKiY`%OOd)w-J|7TcH1!RH37h$6ADth_)=-OygiQ<$~#{v(uX@Hd+lP)>R)&Pxv<?;=@NjC{!bptQ+x8SMWxE|@o4W!69b?}>W{B4IEbhOvqf~3nwuR8%6uxRaQoZ^62IbJ&^?V%KZ1zHITxm6hTDeqTUY_(|$vie(F^4O}<+4saeZ8~`W1E%P=@L-D}q|xC>1cCR$Lpp}`;b@#bh!04@?dfFq7in*a0Zow)4@L7KEn|5=&3)bt;3~I(F2OVQF02Oh!ZqhdjZNVdNcwO8u*N3&V*?N3lb1ALI6)7gk3KWd_D$?dq|aT8K6U~1E%v<V6|wH^`DMkIU;Q?w)<1l{PLS-su*1;p^Cfg?-ssZ2(?^WO9x)`*!wl;^C_BGZ2A5BM%E_M;EG5M{I<gd_Dq=sq>={SeBkPRce)G+D9|5;pyYY&D@s0jG%Hg`7ulnXQvtm&1fB?VxOU=^wmnGxi(+(%A!(VSs&_%JY+}wHhc)@B%jHdnWoVQXAS0a|&%ioT4Rvs@kn~9e{8|kb(UTXFse_1jQKJD-(>;8IEX7J0Bg?{An*PG`s(cC?IHKe`Sl|8f2UF|ow8(q?#GO>5psy$-@?5<5)oVWJ7W^^B>wj`mq5>WgIMY*`?&}E-;ab2HPwnNwU8kY0{hMpTCCm!Ph1BKb0hHsfHsr8npu6N1web~X4M$=wq*vR8@1@=f!f4Sw4xO@YGdr0=zo0Is<H((BkY>(H2mElCiuftyt?vx{RT0dTIp4LU_gx(aR^!TLjj86vJ?VN0HY0<q-zMsms87kdoPz(38RrPiB2F(6?vjriTOr!z5kw-LeCwfYp+Fk&5#;+gDLVho@XO<VRFTVD~JGw}gmTVip<k$ge<jJ=2^v3!C>w&KA=>i!ZFK;&N1DC(t?8#jo7O_v%-tG(i<u8|jPh|7go6?}mC3*8mo!N8HLic0w*PFBP%YDa?2Uc1gxY;+3h&k)-UUAhp9-o!gB?KRO5KDqKt0&&DlX%09B_a$U6f?qNc~b59y;iu}X18jAZkzIdz`|piTGKawreM%}j~5t{^5edmHS!gtKo`Eoshee0r-fdF?Rw<3S2;d}zj3-Ar!ePDNL^5Ab%Ak0mGcxo>>#|M+B>=0=nDT+AMYGS?*ZGVioc6szA`~Z{gqY|H{Q26cH5;VYJ#56L_|NsJY>(XAmy_ldxi|D@{)>io>K>H!92vNlhtp<!4%)z9E~=DEm|y{X|c5IwR;dB2)5s6TKEJX^ak&+UwSDWm;*;D<F!*6YcG%zaUEvbR)$mFFOS3jdC}H+_-2A|9)b6{wFUZbTA5dwaoRx&#7;Lvc*}^;CkcLs8T1Y_H+PstzcAkp>)zSBvuAI*%wA_5)(sho)?`MD99<_&cbg35OXg+2B_fuQH?hp?70b{TS6#@`_<N)R{R)~=(f5?qG%#k-)A+P^{>`-5+&bpSBh(y?6_sD^9?h0LCV!nSdsMfq!A0;KFEytOmrEv>q;kB}R1IA&SzIE=@lvz)DOUnFT^da5@+&Q?=jY^;m!a_jE8WhJSh;vd8R?K}P}iggFBUUKfsGyosspzM9c9YJijIvN%SF}Sxrm<QrRFbsxnyt=J;zJU8uD_<<ig*Mmzr&Xa#0GopC;ljHA~kL7#|ei;D8#kkm<wpQ!;pufOs#<s(rJK^$1+v1TFgd%KEdby}pdWzh&VTQlo;7QTyJ6b8fb36Hg+e4P&}Vb#hSga=6s|5zCb_PJJ~L+6dKXAJd?fVT+fqWm*fSE8fzMgdOyaO|;(*iCcBiZ}Rt;>A&ouD8I|4{%ctLrREQIxx{}BH-D*F0bVX~PXYQ4ys+Q=a-Uz(ts)y|j;CA2%W!aSHU0~mkwpe&qiqmcx`MQ>P;Rc>ycS^cz~-tKI9HwRIqH+n%F}NuKYDn$dHk-}g1+Od9e#W2sAyhV4TIFo30SO``D*zzLS=rvexY$?ez|y&TIR-b*4#_qJ%tsC7Isk8*g;j-hV#M`<L^Icg+-#gfS}VN(M@~NiD<YI%R1VcjWy(!JziiWpdBCWjgsPcfl*Q@3(%6{cq_E{P0r?dYuy)rwWX>%USX-~E?0Eu`8Zx-Js-!LxuwuNUSS#93pmwNHslHnRtGy+oqK~-UUnz6?5=F~aw;u~>9i<jY>HwgBFKNNEgUWLF6$ScPIX-OfOM+My|G6JiDJwRnzm#_JF#LkEGAUmS+~uuN=bIA#lmWcI;$ZXzTfA?Y6kA_K4^Sfv7;us5X=JTcj|VO0#-YMpBj(v`MPs*Y<`t-v<D7<nYsn4<=u)lQLE8tEZR1<qLWiGK5g*5$rn42%;bQh(t*gZ4l?hKqAnlH0u6_t8Cj#Hzk_xuFW#gaNIEIJNxAWvv?rJ`u1o{@ws&v*zT!*Vp9NG@&+5hV6rx0XJTvX_EOZT1H)|L`HVsw1nBtmex}>u-+UN$VH>G$eN45@d?Vbe8o5$tM7=uci<Qmzz(feikS!<#)N}xEgDh=q{W}E52VeI;QD0?0kz-1D0?G-Tj2@<9*p7)%2_*dZ>OpVsR>W4C64`m(A=fRk8MQ6foz+Cl)u(17Lq=Agy=}K=Hz0;MpZ=^pzu@M%gN*7vMuB&9}1KXu^<u6}>-#9lEFT0&{#Sf#;g(^E2YQO^irYh=$W3uDp1uTFykeCrec=2@Og<gYKYXLgzgZoz3P6cF^MonD(D*A4vqXbI1y2U#{=bDHv8g3}{$o^zl4D|hp_vH-mPyq>WJ1xMSJeo1_3S8k8xRqDn_S59FgD<g0q{QN(jmbJup2pfG05&HD&)qX<a#R0QkfH&RGc|T*HrScj+-q+GKL1;ZFTmxyT?C-{pvf*q^=rOh%gvbvlw^}ul5J9)Pfj5#WQiiyY5%MeB_D+7m?l9?4Gd6pp-~scTjgDrnYUT$ZsB^WT>0K`o`BZ5u$rjCYNE=nCaTgXvJ$=TB?7M!T6-$A_Ea{tr<oiQ7|}6#6QUY%MK=G<b@O!c`J8D7%&6xAl=zFe@MBRSV}*2eo}@i>o_42Xq7wDsZJB=c=2Kt2k$XnmdnN<-Oux(d12Wu0M;9HIT=_W=GISGm=2rGzsFi)8cJ_rj_Fky-&CqdALr1#0MyCmiox^4C9R6BIr!OCPCbaHEXx)iy>P}t*t&-?lVbj$5Sxr+RLzHgKp`AIjF$bBj9t{c#KbWnwSVdRFOte`=ae*`-f$R;`KnYHY(T6_gA+Ro%nygl8?Rg8e=OkZU;q7xG{OC@_ci5lQ{ADn@BhWHUAR+JgsByyh=1!r$9qMo+GK8mF#c9Q0iJQ`QWpSU$OeeD%x&XX606$v1OKI`bT4Pvk3F7*mOKI$sSmmk!y4edmE!Y7}iwB>xc&lULg+YLp=(Y$daqwe(UhR_gSIsy_Ytfe|i61)|qNfS9!Xb0ope2rrx1{m7Ed8ci#&24~L@!+zwRUJ_FelRbt5%qbrr&leGVM$c=#9flO2CPJRN8jlz&?0ZE}(t89T=xD&Q~(8wG(8j4a#~DpI2pVUTx2a)>)I-WIbYQ(;}8=n|q;c?se1k+Gt*p-W^P4M?7uk&2Enn^9#s-`n;dG5XI4)r07pkX1&R;;lV5RQ>3fw=;u{p&#Oe9SEH~X<)`2M?&HUAuV6QH5M2vcw1MQZ|3X-N`{BFq{|Jq7%MHci=5L$+S_tJ*bgOmZRiP45h3*DKH+ode2Sm@!QStI$SH!3|M@Gem(=z*+ff~(#tHge0j@Ka1jLP;0o*Aw84vfLF?xaq9_gwrXa9;+%k86h~>k=EEPcr-^L|>-I`!bym{^%#o&+Lb*A`L~L1!>Pbj@Kv;*Mw50jvuatv{-fc$MFga{(&`03q4oW6Kev~;-k!(pZ=&%-vGCL=EucpZ(Mv^ff=0wd0uKwVP<@%666=n@JO3zcJW2&?kE@2viJMw%wc74^0jfqG2vHi9i3>h4o2swybrYV@pO~-fhL~Lp@z4}xvqh{r6f>~QVj~XN5nR{@2PF{u*b$1dAdYGPkHQ+6@^DNU_k+o;Qm(xqR#7Wo7Nd2^|ob4Z;P6?9?et8SJw!?RxN8J;BP$oq{-VN*B&E6KjBm!u#SjrX_S546WcacY&%%7?c9SSEt;aAX|e96nnuqbSdsZ_<@rd3kM=6ooE-@g{`vU!-S?k9{P3HPpFaI9^1@mC5Eknth!#*jNx4V04uAk_OX(#nf2G<>(9?(}{SZv@AqYs%i`f|<!nAKX1D(Id!Gjr-zvT9b$vD{h>7S+N<_6%A*(%y!i2T>W3np3_s;eoVk;)Pwe4|4(L^M2D(ePqL!#PDzE_qLCtjDj@XZ4P@eK0EMq<Ni^_JzZq?HiL*B-WuT?D41Ub^HJeF)G7*Y_`$ORV}^;nP0Ef5}pSGBzi{-ntz=DWhBfnf=o65@`(n>=S_7Wfbu#zU)=}eg=r@Wt(_>F+6j~9sT1p62EPccD$^$r)og{bL4(5Q3|6Mo0+}}}Yu>DT=FQ3yd@D=veROXHmU9@x^F|NP0VzSG*$>3Qi@Z6NKO3jAm^)f#C04pXgUvF{+Zg1I%WE+!$mGpp+1D{02?a~U(a~Q5Qwd78MilIQPr(jkAKBeeM1-p=LD;~f0{&S#j`-!KwH_hMDBDQkSu&51iVTo#0QGDpZx26@|Gjt-$BHzD3NPZQrq6C~Hdpp!1&tP*4u1tYvH=o)7w?ZuydqQlC2)Z(aUZ(yKJ;wc`1J~5>{JNu&WCw>jS6AxVXEfd>25(g-0=##-Droq9?fy}!6R*OH)fTEo>c<OE8>Q<I8@X3!c)O6D`G<C&E~~g1K52W27e^;l^h)omK+3$+^%JD;;(Sjwc61FX1DM%EnaRlXxY>XB!lFH^X?D#n#`-a#7AHejp4*&q!Sv)hsFLbI`&tu;7=QVZ;mL8W9(TlE7Z+^jJ3~$SyevY`Aimpqcp~_0*S<o?=k{@mO%aCtFM2rMnK+y7GP*9&uY%_v;e(tGTFAt+U%N~=Y57p%CDGsol$)gYW#<I*Y-T^c>HY4(~cMDwzK;TyV0Vm(;SOTb1Y<Y(=I%aBEXy(ehoo14-?O@2%6L0=+!TtUTvJ=g+9ZVH*U2<nR`W}U6g2nj)Mm~4qogy7@6mqyZI{~?Rw1X!6Px$#%+CY?oGi=g@|ai?uk}kga9=ZBp1-47CwpdvGH>q4UdHiWp&*4X0iWFEcSPm?Vrc{?jUvKwCSv&@0mOnDe;7Bi4d+!oN!(FOKkk$bFhj>p>aX_fMje^0G@YbYPkO<Z<kFx(pz|5c8wstTO8@#`AZ!BO#P^KT>L0L`EuB!j>VZO+6=ygkLPXZR2B%D?q^N+4As}#l&58XJzNB)n1>_r9*(pZ_z90w9-R`3j_PD@kX8e3&*poJ0uoeX=&%Cu$H;6$`yKP9m8YD@hc!+sDPoW=_ccgk5l0bAGz7KZ7zJBi<E$;oY_3s9rvg}d(l`wzHVKs2)wozrwkOxf#)nLE%W3ms;S!E@3+14FiHY_l?rvs6tN$CV{_mS}>=BU52{0+#Wwn2n=49iZ-$GcR4ix02fKV)~=LF?mh+hi9Z+g>%qdg+cL8~WP_w+RQ?ghDg%iX8B4N(Fi<7Qw`1{og<YkV{^IB6wqmc3qME&(NOuA2_t9!e+Fr^170u%W#=Y$#m3p|Gw(sH_U11$^DKa$&N{h4ltXI~kN_DHl?J46j=wW*C%~BQ3wJDf9iE!1^4!v2*Os4x%SJh*mp_jnoSnT8Of#g{UV6c{g5fghY`{{t^Q@A35f+D-;9z;wSJ=HOA1q&_na)n~e|tyg^%(r#}UEGup7>dG?3rN1s&gGIMu9w%DkC@OJI>GDEW;ZuktO3!CWDEI7LK(709j>#TfU@QCCEPdqR9riQxDBy$gY3~a0QP$%TYxkKur;j4?hICn^slmP(3(LN-+mZ|t+9+!C!X@E{eN5D<{Uv8(e=T0?In<W6kY<u>g-2lQA@j&N@>#l?{fb~>`#HT8x$P_!r>>`=Bi^yqhbgJq^2j^vPaNhhWB3_RgvqwP5NYtZ)A94<-N-VrOv-(p@q8=Umd~`9cspC!El`hG741pTCCn2Qg*z>+EZ75;?keMHJi$6|xbw*oL`0hLggO><Qnuev%W>5!C*|Wz0Y$tEmgNRF$rw}H82?28K*cnOq>nyyA7!V#i1H<D*>KW-g#FL?PR%aoyhmSWTl7OfZr61-4J>bzTvgnJ<iDnrJ%`z;TV$n*|>pM-aAN~rs@YOAbdQ6Mfv%cw>-c=9v;^P|hfkS5p4m{FG#}m;zaEeT&k<jiyu6XC&DU)wfrAStC#sS&rpf9BD=Ph|1ZgwDM!L}!~>i#t<_tT`OEz6&_KvHOEP?N<!dOB0_;}e&Y6mopJbM9YxBUPM8s+f=(4^m^~y{U|@=2(1{y&}4y%x5=B%o!zT=L?iqpD$oCEM5kL0zQkv<O-q56_r+Nv`w{!s?7@_&;>`JBh>VA7jnfT3<+hYJ*X@B2P@>CdpiCV3xvw2QS4w-MD+~^ZU-Afg$;i=<@$9Y!k8qM%qPN<`SeH3XnGdEO?tDLR<@cSJR?thdqSb@31!2cU~!2c3q;*Bc0w(lKm;1vl+yS7Ai3`05eukhsqIPR2Q779ku-x8Pcz7;1uhujVwDaTYqaNL(4LD)4@>l9>mEtAb{ksyL8S8skzqAu&fCTV1xO&q7(hl7Gz5z@-8P}6Kr*X)1ijX6WEvRI;538d$*moWf!r>+?Y#DLB$!p3`szqq{S7r}f%Sy7TgQq%^k-VuSFn7oG@LL#%tdrlH*eK}Pk-CX@;1}RgKjlUC;gYn)?cQ4lduzz7d^j*L=I2u0Fi!XEbSumJRISvJ2e1<Mih(Y^a|ytC!W(T`d*spU2X(kM$?pSX5VrF?{YITa4~Q**`k2tx2gBpQ*Qt(w&=|!ATBAixTJ21OIkoue5YI<7aQ_xA%JwBe>Toa_Z&Q>cA(8(4ER)eHRqX>+8UJ^za~HjNGfP7so=E9;r#&}5fZ)8Y>EWmA&d?TU%w0JF#2vIz)6-w-|+Go&^e3=9zxof&!_FMC>DWKkrqi6>G4#N^HNA7n&}sgz1YiGL$DX<5PYyh@I}+?(k9I=^XUjB65vqd0S=A7#Lo9CR)F8DTNvHHO8Axv7U2fIGLXq}VF$;Rof~&{Y&`s_G4w>~m`pvTcn@t2PfKcmFR4$%?;GZcO}zz~dOrtsV}SDsUK2WKQpe(@oh6b0Q1JwS8>?31ud&A>045LjSOK^Pf**rN1<z}X%zLqDPM+7|u~LCtmJ-QjsqtKv#$RGT&8_G#BCV*DOa@I<cwm0Kh6|eDE#NwXdeI2#w5hht5uU#As?Zl=YK&wPql6TR5K=5$$7@TeXyB6oVF?zG7sx!sqWF_U0%kN()C@!>(j^ZsXG)Knz-zz+-pIC?;jPH0u>^E0i{9XBWbf7Xvdn-l=gfxf3(Zno{FG{$L(js~$J&WhM`5!!C&4!HUG)W=b{#h^ukWSeFVNdKo5q~ZHcbcHG@Y9bl;k&1Fx9|S%LP&mz)hNV7jq5RlgyE*k;_G2e)U_dJwvw@Ur~s1*=^##{0Om!d(w3OmVSE4^ywvUon9=(UfMJTNg&qH@~H`JS1`#3J)moTA>!W#MnFOSwvd*7)9#@OaP(oIWOf>8ZRKygi9Oy#=b5sIXhN4X3>sH4HgOeWD+R$YzcpHf1ITvZ*aV|DD=8LaAavvS*Gk6_R^ukD#tmjxq!3Rs^9Dq{Rq}|ucbn8WH%N_(AC~1vypJJ`dyMh#@x=|+^oNY~W7AhUBiV#%u*M8nZf7X7SN+NIo<=<bgf|KYT-kP+1wb2tPM#&|p5U*=OClPr#2kUhvl&l3Tf9^>@#HVLOVSBT*R_Nc0Nl~#CSklqRbgt{fP26O%%5WG)<)m7!(NT(u>z97VtpHhZCH1{VJ%(*O*gga$r_amp59G%GiGj$p1E~@MJNgm7D5H)VaYCz^@C84Kvr|0b(J6R(ANN>Ap<5FNvt16@}AL0BDS5E>W)tVpS#3-?!x=rGp~lfTy!;~(Os&pNK4nkXLeMTVjQ@H>xnNngY;&RXDsqZE8NN-_?SXZ$~T<&`cPT+rrxwwsQN=}$cbMuD+8j1grtp7Sp<*yB;rK?3=GibcDaDu+&1U%PJiQg(e+S0`3qEXedc+Z_p%1Pa8N*th+dGP;$UZrbF=G~=+0oKJA>k@REb7b<8@!plWTQ!ZpncO@Xf36jfHR?3qc>@PIiR5=oxILXRtyW(QAmqf1=Y{_|Rdak9jA4!7HHscb3`FS!M@&pBDN)g=hWeO)@1CASW9Ea>84(bn=Ad#(L2(1YL&NSQ%z#`?!;B<E}smbmsFKve4eEN_($1!>J*?WJvwE%QqKVe72vn+-dl156qo`Jgi1vUk_zBFCHV7V&TogGtNpZyt(nvvK|X>p1kjE>9zgC$^2+DztPI15rDVPFuQ&6%BjTr(uDS<HQJY^7J~(v>_FPxyk}Few%-=oek(#%Y`&x%kES0qy>U9=;zV1+^q#*&qUk3Oew@xe+D|mqCDv4D*mJd}iXD+Cddm1iW{WjM-tK2PffI8BV<f8_A=;Jz*e7>?(RHUENP<w0dAyzHY1jVDiqz2LRX+~FyQ7X*VF-a`f6k&U$-2R~L@LXLqUDa&j6`K=IiNdlW}YX+#$MKy0~BbT2)vqmE!qXWo$)wRIgxoaH}F-H$5+iA`J{83kU`h`!b_0KbvGRlY7GZaMR-bvfhn4s?r`O$-JD~q&`g+Id?*aDVRjzZQkk*&F)Iz-{Y(l-+cO9CJ*e9BC6}6lA@KswOp7jcvRaRj)p~fZwXU)AG`7jgc12j(?#-sR6Gc+qqDbEPy6~5ojSXwb)n_fo)RTFK#tH=MAz*~^h8`Y)<g`Vnl)Uonxyld!AITZe<pqtE7u-W1VBbGbUPii45Qx=)uV*=7%%U(aT1N%kX0G`d_?VEhUw$1)9wTsXkF7h^Qbtw2-!LMK?YY6&<~iU9#G3GKh1l0ysIZEa0f<dt6OPx|z>dL=`KHh6BE|p~;%is?UueWvqY+=bB9~pj@$%Qhp&w%RT+U2Zj^vn+u()N=;+6^HZNcPcT^_%awvFqrK<k&K5P#mJi@B$HHD4r?<|Zuu)tw^=TY@KS-Mohj9ZuG1P57WQxe}`YmK;kTFy8cS=T0trq_^#U?!aHO7=<anyqF8T89R1zTkaXag0M}HDHiNnK;<HZ7Jjq<0=|b+noo>`r*oY{aqxu~r2z42y2HL;#s$p$KUh@1Wt(|z=@#hJmY=__K#Yx!4bM@4vT=o3Xh?abA?0mz46W=UlpgPBky|gE7|l`kPVPeJP$BOK&uGd3RQg&a2T-K7JGuBv!62dxIMwz256o~0K|+p}xETD$LnM2EMq(n65Rl=MLvRRmJp-sE8xulK$%Vp%?8%L2>W9%<=LJojZtKlJw!n%<3*4vgh{bmpT$8%l+ia1LH|59b=zt!wJn4G)7f<qlQn!&=erIR-lbz+S2;(;S3b@^1U)S#Oyoehu%R2GEn#^Ypmq@rlc?&n7=DLvL$^c`ez$94b8qlL$lMS334hJ?tQ`jYr^CIT9lmu@X0ViYx1O$U#ut4GMv2|13(*qi$z<rz|!kc{F<FctnxHppn?KSs3sPPIVed_~_##*o)crc<b2jMcdj=keL_NUwa;4g8q!a#({>uAz1u&IRxWt0FYql7^jWdoFfdBVpYBm?fd4Bp5%(eVQqhM}tzgtalwSiZ+I;4x4!MB5V>@>r>L+Vt4Y@DV)2$LtSdmss!2^8&Zr5YFo)%`OGYc(}{9I4;{jNJ-{HN=nQE9Ps3hK&F%~$(?t}y-KkR72&PC>YZHn(AWYpUyfIxiU#p3iPL6u2Hq{vc(=T%Je5u5Yvt3Vdti))F#RF$b=m-5rx^J9dG!>TtaA;Q_vGE$i6@|m&j=#u&=y*#MWPr2)FS}c;RacqDrMMm-lj-=cv3|M03}GP(1aIC6+VQdMS@j&JSS!Fmw0Bvc*eC13^wU*X5YY`>Le!efr*V~Ce6FhkHD>T@hrF%35{7i32qT+%r^kSX8=H;d72>yaN%WO1%Ed~vR+*XW^61H@cK7@&D9$i=yxI~qO&@su-;){CB^XqsH8ZJLJaSiLnRghxr3NG5(6I3fG$u|8FlTClI$<gq#i;?v|zC*pPz0+AG>#U>^|6$(u?6n6thcQHW2_XAX8;TGLan{+MRSDk046)z1H_&Gk``s11O>cL3{gpKG2Fx#EqGN-ay|n>baR&n|8Yw&Wq5251j=*j6Gk=^q1p$?|fQs8jVNEbUaGl@;2pIL~Z8XCx)d)Z=lQoxZ!fmRT&3#Ka?u&F05(P<Fd5BNAI*$&cTQEbpSlI<H9~(WMrEjFHp}9o$ox2NE>PSi;Nl1@d9kd1NFwNh=4|mPf)FD*;A6XJ&5G+m!m-~mT(V%&%$z71a>R@B^FlOfv7=@+Ii8@aCg*_47+1~8nDNtOHO~y)%LLbe;=}&VM@Ckk<9_}yz6be`U|wbsqs?49!MI{H)XO5WZT1yW=?qo0=|Y2@SQgJk3H}G;!RsQlC>`J==8#0Vx^%6orWF^jh(NFcZ3eYwmg=ZuFsqHfHnW$=j!tY-mai;efevk`n&-*Tjrw;Bw(x0)n5eF=N+LRbY7P;d|eJ)pASrfb-aMB&j+f(lJoQesD!HqC<kp%_BA3RdLUWO0D&AYfOhxO;^;!MEF%K!cmWmxhH1c7Kx_8&88}S=h8n+GD3k6k=r1ahuJW05gSUFo%J39XhNlf>c*2$8_XVZAscB+KiG?q@5hz{ZFA)%f63~bM%T8C#3$2>BpiD0uZc@*xM8Fi1!ljVt$D_rbj<hnrFafw2DyW`_;ejVd(_atUAYO-T*Yw@<wtK$4S{SJfC{1XrG@<Pwup1leLLw@3F^{gTQPn&W;XG`n(dSBc>c_L>z`V(6&XUty3bhO==<xz_MpSs9w(zG5;ZGM5IbF!c=|Xtl>2pQF*l(L-go^RDIbHz1Z4kmsWeG2hRVWQsp)^^AlFn=_q?xsxXhwB)n3#uko~YkRk<u+~lx_jEUBshM!DQXzHOjVpnmKFGBBK#VlL69h7JYqz6q>RXvsks0SSF9;I!aYPlE=s{1Dv0ohI2tBxg(Tqvv}-Z0JkALZX*z7*CSDOV<XCL-bI=m$g+1+9*-qukC%s;oWV|e`KG@Djb#)7mKHD@W|jz<3+;hC?ObY5lJs);Em+3D7aID4W6>j|FF0O$614DHgYE5zs1=Wh(t$+--FQz!uXNi3Txqf(z#D;#tP>Er2#-T4z77x6lqU{jjM@K(uPekl7!aU9c-+F>vS(^Uf5KaQdMLVP(papuiLA=L5r&uxg(7KkWaybu9L6#9g|HDN9{dtyTfK#Sy@;?cp~Jp}4*L>*7OJ;X^YXVkxEp44ZJ#!@7?q24d)+?}C?q~lJI_Y5+oX$^&L&@&dbFzvuV*d3TGTC~F+5$5C}&4p2&>0nC0=Zp@#zaBYt%~~INzGCqHBO3-opIwPG8^fy+ioZHPAdiMC6kTtMbW}mHFgO>wE^=&9=yhZzPvJl1t-h0FZVh(b|z5(T)h;CvTAipN=Q^*f=Ka8YgWAO|MpKGLVTiA{Lpv8Y4#-^Acyw2LvOPC+GJF+<)M3e|+FF*nx|s{Kx_Rx;1clh^3<XxxI{~qR^HK;Z^7oQK3s*g)Y1bJ@d5jjNbe<zSq9_v1<h2<}L^+)XKpkj0>ffzXS`2SLe?VSYXm%fn|RVkK<iD6NM*^=q-7Puwi^Eir&%}_COqp{wZiX{#YIY@7uiUqwc9bP77HPhujuOOc7tWfZZ>UPC}nT+OWjQ+wfKh%P7LjU5)UQzK7}Q@U{gZk{3TU&XK4)iAUWP{t_#X^HJ}@%4$A|?(<ohIEI(01#;PYIG25#mm8l0KukQmT6oAvp&=uUhKvAM61X@u?!#9QPUFFHcIYGB{+valq;)=2W-%f*CcNO(@2A^n<u9@E@N*skuSYm$de_L-uD1L&kbn@A3S>4zA$M9pcv=85st&c(gr9RNTjUL7P-%sx(v}yK$|jLlk<fEZ>>5`Hwu|_mkCyFd2i^!7k-QnyUvr*l41S^tujy(5uRfw3!v;&(HO`QhPEv>lV%4FjS5xsWef{B!k3W4SfB5R_-@p5R2SuE_fgZnh%x2yGVkTWh1!~qDh;+#kPH4%6zr@OOwMGOMHaFN`ix<fxUVSWx!r_gf@j@9IM%AC`s$YCJ6A|HInV=f)4_N_!2;%X;u#lKP<h7>Q=xUn5ifQH^QU$<n5VHu2puzXvk>qw(ij#RMPTC7$ceKtN4)E0Y_RWMG@>EmVQ;klzXe{BPvxJMu0xs5`K_{op=6L|M-6Aybj?=)=Lrmde9FM^h>}w#LIO5{-As!XUfTnpC8utCzPzFOHU1^DQ3s9eRm2`#DL}-G?qKTD>MOI3tb=-o8I&kJk-ytS!<39#XOhCmW(<gaQ<rgglDJGhu_;?N1C5cfvMuZ$PH^?E2zDB*+TM^NT1sqXJHeMcQ=E03{zT2ebdyCIc%e)e=+$nO6m(>+sR##YAoiV?aOpEv4l6SU}cN&_!v*ml-4kuyn<jy-LCliqg5iImZYl`?D7YfRg7o@0>K-37I=96g<9*{P)=<CxhkOIx(A$ww>OZC20st+H0U<FShCVzbp_iG6jDR||K<s$&b3M{_~@^R>+-YxNj)2b)=qnYQAiY}Pl!r_@D@46?F>H&lv5UYwqAoE_Zsw<a$W%;O@e^i7uklviI9;N`=+<GCHw6HK~baQ`Zj#TD@b~0+gg5-Xkmivu+MTw+{ipNmkA$vL^rMm|v<i3bLwh2B1P4F3Sg3m}YG3`5?5#Qn5@Ey*G?=Zl{flDA8!ia`g&Pa&m8{1@;ZPJlwDu_*zB5abpnQJ4wqNmaZLERYFWA@C>BOgXABP0Mtehc2&3*JG8X8Hp&_*vA9=-vVZpwBdeM`F*HM4qo2Deq1j2{=iCoi?um(Uez&WPo%_TF_*V-xA=dP^q3<fLrH*Au%jxqH)VxV2&l4nXG1J(QW%ox9!ExtTA^aS`C;ND+iRcrw7y<|JpTLM1r=1QIWms-)LcWx)nM76=>Q>0wNz0-z&{Ne1agDTg-~;FS*@z8x0r$TAB`uEqhh@rKGa>rTJ-C9vr)3z<id!!eNVJD4%j7jwg`Dls3|s5}(HO*fhyaaZ4us@+Nn_hq3cK7k|<mltgn-@}Aa4o4#6No9g4tot^P`5jN$;`00a2e+xh+AtW#(hW>s|35;Qy?fwc>{Mh{?+-auXfu8w}m%ygp!7@9sORThh#vsIe&LL!Q1@PD)GQ-STX)|lPhf3g#Y<88GZ8&BsEmj`>3RF<H!pX9WPnHcaN@>v4!pRt9{@38Iaq^;2Kz{1@JnaxQ+vgb*t}>FAn~P6CDEbwd12Bwkff3P$aU|rZ-$f7ZfeSNlhZG*HR3q@G#%mBq2y~6`u>&z@aK2O`K~c6h)E?PG-aOWtSN1SCm2C)jwjn%dq0S1V0O@&Dg{!BaE7Zzt-4l<*sA0;n3i?Pv<fwj!zll;_l_&*Aq;ZMc<uqxEB^Vh#`^9~GV91yhVw9iC-FTCxJg+px%HSz{zD<i{@buI0G>#ct5^r?QF{AUnv?66UBpGWPf=KldMygNx`WA~n(GL|Fnx>ygp2?`77>c_cblfcu^^cQa+>)Q~H4W={4lrQ2)XPD4ww!#QMFRpdkjw7Q&M^l*kfY;@qp%j*h{XKxnMIa$Kf+rXw5QI{dv<>XYNIQD^4_GcZ}Ga)97&cGx<ft!;sO$i2=J^bJ-}<BRER;l#AhfKLT?u29e@L|H+6n`{ixvT0PWT!^6Fji!2J1nlN?hZld;e#7KycrVJ`N7gt$afBP;L2>>-H14mhXN7zMw9c?;(qBYFz0DsJ!?1dca95#Bd=fVds9(`YsFV%5k9P0z{>lV2SQLFf!SG0k_0E~{!pc);r$I!)=52&M1W73K2?{CefzZ>Am^nf}<boa<qJvWNNBbDZ|3>m@{JYqT<Tb0R<a(Rzx|kn;=bor%-D7`*L_&%4%BsPk?Lb%-Gm!7ukftFDmEGZUmdX|!>UfQlthBIZh0R6Ltb=cFZ&`h7gbhVLL{>dRMTXm!;>(5OKRL1&B^b*2xh^A4Ae-j9&7bp|TgyjT^1@PR$|nip%ASp4y?5xa1_0Oey_BUoT+3lliZPPTpy7|>?+f<?~n5sjzFePXZeX2fZ8-E8+I2F(zg{tC2-SIswXp^pP?PgAQEe}hT&!?4qacW8HpI%#A3BB-O#oNe;6#uOovXP*T|j2k9D3Z1c0=;TMC0qXPImEDJ?rvdLgs#L19?RW$lMay>`6JZm=hfT<C*aR%STD<hiaw*S<lX_|O94gyv0TfyHv0w~-wzE}Qj&RZ})m!zKz`feUW1rG4_6gM1nRqFEq@QVRTMlU3jFH-kBq1l>ULpa+HD7003b2>reD-ixkRN%_3WycS7*4$WK_ami#W&y|z1bS?+o#jLknAkyf!`Y{Zi*fpaDS)m(t}3btO)5wl}HTUw=nQm&DEf0-Og!@FQx>1?hy!3e@=Bv#*aPF!MF$Po=;^Um*xJ}7|c*|w}8^T(-WKNuRwn&;k879j~gPt?c)i2EK9t@({t!0Jp)jaMI$-NCQWZ4qnAjY{U)o<*36%#fZ?Ytd6QNLk6PM2waCY+CHvXp=W2D&_}Bv{=;u`}+2`jIe>FpVQ3KerreV4slR&2KZnEc(4<Jww!LwWNLy(#hFb-9^wSHo*=-NsLg^!n$&j+26e9#Ez>Y3w@(U&6Hxb6Xi%8E3Hg{RC%Y)87|ra|ZX5@;EffOw~#C+|jEQ-kNjr3k|AnKNw~h{C;os1yBWM5T<K=3mYL{&MXmVgC5zfBg7=0m~4xg#')))
