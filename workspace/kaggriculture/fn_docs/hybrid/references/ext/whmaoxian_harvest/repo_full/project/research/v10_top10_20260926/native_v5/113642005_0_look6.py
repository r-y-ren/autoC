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
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqUym%uapk|ueZCKwk^lWhQP&b7$|NqS6}$o=2=D@4EMV_SHn0oB-+jr|QtY0th&U&*x@YEczz0i~QeD$sl@%Fr&hPx;Ki>WGpZ?{a{_^hc+WU9^_NTx6kMIB0AO7$k@Ba7y`Tqab_w~E?@Ba0Fe*Z7uef`DfzxmzQ@7}-r{Hx!;d!N7m|Nry9{`;Tb{at?l?tlIJpZ@93fBKhy`~Khj=lg@Dzxdr3U;grsUw`(^x4--N;oaX>iof#fFF*VI!|i7lVC9dO`}<#i`0U$v@5|p7SAX&6pIu&OJ6=#O7X1B(55N3r!O%XTC<}5rULop7<m#`u{wwm6KjXXiKmN+?=xh7t*B?H7efgbV{aSMPM=8H^^S_QCf9IP|?f%;9KXYh5*42mo!}oW@yWf8J@~eNi_=2*(^!J~A`{Coo64923`)So*`t;M3FESr|+F$SbpO#L4>C;bJ+Wk`BH}-xhhfj_As{>Em^{?Kwr@{Tzm%sAq7o$F`{?8!((x;zRv|lc}pVs}QPd{yFOOpF(%U}BB(<JFzQgdHCSKnp5*c!y!kktKIycf^ZZcP8j$o^7rcM;&zs=pN6T@vtV(_c#LF7(^zc!yAaeBi~&-8O>kXzKo3-4{jjmp=V+v-W%VpH}>(Pd}|{OZ@$C_)DLD+SG5H?EQ7>gRkDFQ(NKhhsj?G{%!^MwBj!Xe>VX>t@}&CH%szAO_IO#>6_)rH~HNU|H*&<^MCu}5C8FB{`wC5>p$Q9@IUwePe9c^0e$|}mtTJP{M$eN{fCd=e(~iO|Ml_%lYglA<;SnSe&-*X3iNpeKRaD4_e(762(?j_PxeHl788CM-~6Rd@6E35DFyub>+a9d`JY4lGmlm-FZM)>98jMeH-$dZs;{1cZYsxB#Px+$zxcC$=|Ml}$^WyoTUos?1-vgid$nulKFo<~G2E=LT8lxuWxD@cV)yaYuYY|XdvB8O&u%~bbNL==cYTl88%YNCg1z_3^$pYL>U8lHX6DPp${$I(zvS1Sef%#UzJV&(+hX*aZ$Eza`(J$c`0*d_c65@n-d5K?@?cx0lh{U{9I=;wPQLvWs=r7%)a3>p>5rNLxwBP`-tds~3JvI|3)BXMeLSrmS_!u{B-5=85&elNY?+{b%AgxOi*M2ZfBfy!A$0N9>EdnBCFO#C6ysSC_F3Rt?vwA=Cce`ye4n<`M`GjvetYZ8_^Cbfr*`8xRTp)-@iF=4MWTD#`j2XT-34#IA665Uzs}~=x8MI>fBoli6)w~%d2~gK)Gpm``DtZHh8m5BWr*NiL*}L__)W9X|C7k}Bj}&D=<5{zQJ3;+3v#^-)VI9Czmy7p=7I+RM@w#Rr1eq?@6f0>APESJcr*VXX7rf5=<C$aN|zP&xve^RIVCAwixhJs1*XqfH}>kwzuqw_eFT{7F+=D+^vxt_qo%CZS3Dlyi}dF%xzJKHV557oqDLyo{?;Sis3^r3x#+C|iB^=E@3&_2t=!oAS$`>ff~8hKcqn{zChB&h*R_u>nl`mAPMviuAwk;=SS>Q?TBK}E;`nzl-}0MuTk%!5{4#$Fp4z|bk^bF4s-IIQ$T`Q~cE|}xd)+Na9DVe<6QE^_7L~^F4tSO0MP<?+O7T~qC8Cg9g;BWjj)=vUp|0fXZ)NBs3(?op%DnN(boLc8Pa8Gf|4=IW-96Yk32BZv`b6NB@sKW~eQp}3PxS+ObbHj<{YBafWI!Y7!}HR7NSj$6P>!E>1GwriptJCd{SK>Xy>P+%Q8QF{Ig|d|Kdc!_{@B2S_~iW!xLwfm>7$Pmw09Ky66qt^qEBQ%>5Dxtda<k<i+)=1%P)QvvkDwOUnlqlUf4P5_W2UJYHxJa-s#iFVox8E=mCiJ9+aKmDuc@>KN;mu3N3b;Sx2XtViZj5g_S+uN_%7p@~f}D`sM@R!fQ7k_Rqi4A5}SA_v2OHd}daR^BvItSAVHlHUG3^9DLg0pmzA{&4Iiq?wOlA?;h`7?ex*K-<|V(%Hc}HDt!6dk&e&frDhBA@@FF*pT|qh?&VKQ=E0{O-elchZ>ko4TC&iOT>g6Vh$fo3Xs^7qH@mXuRl2MD=XRq@+EXU>?pn2HOn}|BX^ZpLe%Fk~#MG7~^i~4uBBAITH_f~3(>Jb5x5_r}+Fmb{KHJdKCgd<=TwtJPyVJ-nlhwA~4b|l{nZ6G@*zIWA%M2ToT&}<#>FF=Gd>EH+KyVMq{(5tMfB6Q?0nP65dayE_sFrs4>%pCJgbwn@>&=6_C{5CvVw9e&^qtAdU>l*6Z96Tx4a&D#`3^*-I}mE&p0=vKj^2RTUvG9N1QVAupl$Mq-tI(CiBsDPz^3{2gIUP$MfSY<0=CT8p5#Z@+|mkg<Ch#e9FIKN4xiq0A7DMuwLM)RW98+|hJE1jmz(Xn%flk}iQ3zJp}+j)67Y#^{(4hTbh#vN9;q{X4qE7bEdF|PY<{`#7^1>TYYI18$`J`@-Q6p!p7L#Hd3;hjnGhW5K~M|YHJ^BcP~r_jmNqfKe#{6f=1Do|H)G*;oZZU>+HuPN01LNiYSG{Pp@V@PK3-rb)sGu**0@-Z3SRgksBYF>ofe4=wk?v^UTOId5Xk9Tp28eRA!S0Pl?lcXR?brku|xER>h|PnqbvMReY|rR%?WIuD*i5l`Pc-J2~=97+<2el*zKpDs3&?pZxa0s^AJG8*_6+M02&ge%F8jvc?KY~NAnN^P*%Schp&8db2QptwrHVsriIqB*AGJMCD?wSY0(sX5*)mvf9a)kU{D;XjMq+Oti3==#LSp!w;GP8*Url~0LUNyBI~exGk-V_AN<_P1pNoE%zMr_3L({Fr`svK7e(k}2EY9bdi$B1+s~rkrf(;C?_l29gE?J;ud`0_hKNOLQKJ=*E<mPRQHE|N^LpYEk=n?c)aLa{ZD?DqE`w?OJyL;Y22IB3d%A3zUbE;~e%d=6XIiRmoq^;LT9C#{(l2+9W{W11zfKoTs$16Jf`yKknj?tIC6mjCIbLdNjxLuhE@$L;sagA!D|wtQET&ccl@{gmQ})S=*m!xCZiYy#*u0}8cSv)nD_Vq?ni+G#M$ZY=X<UPjGUZ}L$7Ye`qU!Hl@X+y6^B28bGPvNO<E3T|dAY>jewM$~>=~4cQpo)@5r3&!x|YCfp#TR5)Xs&BCZ-?p!8;7Zds$ZPn{BMa;PNJD(brejpIz<sWvBuyZ@7>O7j(wj_r{-dvyYp2`WbCE)7`I=L!Xz!rRI-Vu5@+ktD(>~sz$q@2CXYwy!b8CN-|w9mv#j3pzCa+&3H%}t4oHHzsF4fWe)`uUM}@t!{RSBf3V9X{%g4TOU(-Ka*2Bi(0Aa4{pOeZ{EBWB**J4N-6~ue-*w92^I62VW&?%I03#E^(M}01eL=cgDCgJiZwoM-U<2g~94ODWCG|;Z<;gphpH4j7oqks?Lf^6O4!?tSR97#p%t6ZP1T5B10&0adLMMTG{m$b~0_EaeYq=-OS)(z1_Y_uSTG&}uV`o`i8}18FxWE4_78aTE0)$SBOgH^YCt~SJEVOBBeAbX#_IQC2<#v4fH%f}*1x87sEI><&<E_wQM>(74EgL}m)s`ync!j0PyIj$s=i_*V^?V#}=9a?qc!lMdFW}%$*^nzRdmZfTb?(hxdD))Ovc0m|?y0nHrqjBav8kJxh@k(mzH_w9yR2V){MB*Y1LChP_r@NbHHtA>XxfqyZPtp>)0j|sXWcftLMGX%77Hsg>a5IY_<o@mD=WCad!g~2$BvrtLbME^C92z53Rvw3eri0v=j+bNvH4ZT(H=PbW$G5FmUk=KXRSsrvS{1biVj!B__V>dFJJ7;GLtiqN+&zRQpvnKt-5?H3p781#%PUJ2M^liym*syAb_RtCg;Y7>z-idpiKHdd=pQb`^F6*zD)jEP)YTyW<AeAO0<bI(<ahF7ddsa$N{9+P+5$rwt1>dI!ot`?y!2-ipPRv>x9?t$>6+sT+Yl`sI&{Ok*yuQp{5_kCMv}Qsu!yifxd0F+YX%8uD^$}=aT`PDj{270TZhraqHrV)0xMQ6`lgsXbr7?Y7_R<*3s}Fj7nE@D%}Q7R__=K+b~8t%;=r2G>_3cUFi!)8u$~Nabe1Kq2=ki(w08aUCLkn_7(V@bwf3?+gevVHTvMFvV)@rEZ}ddqK-f&J6~SF0$4|hnK^_PU^iYYHh9Gspw&LOZ*~1uK&olf#MQ5&?^ZfWpp>gyKm~O0iD;|gj#H29PlioF-=BDI&j1e<kchX_BHqcvArr6S6<)<#c@=LzO_DqK5^F?CEFK$~tP|yFv|oadb5bhaJyS3@1yThm8W6oxV~1*k9jeW}{x`r1xYYmy;J@2N0Q(Ob{bJa_<}13~d~85!HfgEZCP(_@h_phMC}N%V&ni*!L5z=SG{oe>0LK@ag<(Kf-l>^+tETQauBYmm?+y3~h@lHBnkuYls_crUD$P18(feK^bS$C8sX~iWWmBA*$svIeUXwQ|tr2Hs^WR)IPbVK9ns&&KdNM(YznBX@Hx)A2NSE(P+LP~TcS<HIQNV_EZNxgF#AW*ZoKJl}M{X=}Z>$X5Sp6=C6v){Roo{qxbLEFc$Yf5~!CcvU>sI!y+u677*n8{FH(SU(Z6WFE8l6rlc379a!}@ETufBY;n$Y4Dp~We(DNcC}SWKe1g^gV6CpB_~Y*o6!hxYf-_8w#mdo)cb{PecciWXfqGtrI~1t8MM2eLPH19dtnhB^9_C&jv=YO;c=wdYXOo|Alag}2X%@bf*D6Jmc-^OwPlkU(EGfhfM?qs9p{o;zg^cc=}HXceAr6{i)0C2nos)y{n)gP+U_?E;kO0A*?MUZ=&6bd8C&rJCz|UZ=5BVwI}`=w>hMw5kWNJ|29|;ti9DR}TS#quU~=#0iu2c?C|^Up3>vu0>y>Bz`t!D5ECSFNZ8{gVsSV-q^--x%8WE8NX=_qr-IZ)Y`$K!9YsuuUcXJntt1@$VfCjpf?W7Edf9KQEA(G8~os*ynsONcB-7h++fMPAWx9dH>mwV%wU!Eg0(%jT4$YPlQoj9O&?jJ&GLmd%hyfsY@?}1dUr6H9r3iCdV8liqh|?ycox;C{ZNK*k>;>Pf6y{(f_@FpX0abMU8P4q(h_^5CGtocwFfC<{pQynK74&e)u9vfTEOZJq^SLsmGSjw-+cQ!XwqA5a2Yp$+w|8$%$TBEwiB-|m591@H_5uu(_}u$dTvgWm;Xj1rpY-nO+Fl`+0P8riw4{&_A_(526<-GoB`mO(c1ICq%7->?8G<N#a{xqZU7XzcD}MMvGG|c!(T$QZhE|R)A<mRe$t4|ez+>qa|F7S_E_Y2jq-3!DDmp};aW%+R)>fjudpB@STD8EqgOpWCooVx%Fp@!kNWr(aNB2oqMY_7%C{Am(M*u%rQZ~040tN4e$gzDw8?-MU)=6adofLXzmHxWRv0H=K1UoAe#REmiKhHul#j~$Njo2vH+es4;wc|$kc^z`KFC{Q1NA7S@`D<y$H{$9kfR4rHonNyRTO&SWQQy*Jn{icBzQ!?Kt*Wnyd<}2oe@%!TXrP5sQK&BT!wsgjqq#LvRDE>$)iu2yuEVmu_p8rPUT7Nh#r?_=GQ$vZe#VhgVp2CJ;>6cas8Rr^KJ@m^q_+k8PQgrvsCz)v0{zlkx=6wk8j_6`|-2i|Kh{PkN=3ga27wO#d-;%g{4nY5mK!KAi(TWdI`&4srC}|*rQ251e1IS0_yZ)b_R%G@0-p*=dW?_fXC!7xqV_XPSAe(XXzQf0SINbiuM<x5VkOdi58FQg3D*5yF^gp=ui#O6%STdyjWdvP7x$b-cuv%QSkIxy`ya(j4nE9?x&=EZLu!v$Upt#*~c->MPi-4!k&@JURw~bBBOG?$0jY^T-D+mmHG8rHsPT$z{Ph&rTOPcYeu3KBYb9qR-b5Eecn_V0^G2pL)d+oVVJ<8&;pCHDX=inp*kMl1^$cB(ldQbQO$lS8+#~x>S1NtF^~zgvL?{FX9BG(F1WI|;72!LV9kdyVQ=(=9nc#@CIUcyy~vy6`IB)xi@Bp^R)?jlIM`&>yv<zhxCR%qluX`qmVL3)k(#hXoFV-su$iEoZA9kY_hjxs(30IkMU=X_T!c+mD&U``vyWeHcI*-QjIy5;o=NivJ;?wW2~cBa@;3AHVB?EddaOwIsPIaUYWnr|26$ypd(dcA>hM>fa~&XWc=0~V#LG6tUji4%68EzU?`O|84nVIE#!iLc?tGX>*r*W39`0)Ho$eO2!yT`%+l_YA?9s4SpH9+7d1Ihi=z%7{&LVC|i)S@`Pd$|)vm$0@-n3q<HGn6`0sco4Xvz8FU<pK!67E_%C;kdYf~y@ZU<M4Y<>ED2gVt89KnzJvI9&g5ugSawOnj6U(HKrVvpS*Ke^?0dqC<%F3jVYS`R0hiIL4j@#X>C)$n5((C|2durq5&=IC5kRPmoB~06CJ5um*mVQvLReFMp#(Qr>|&U}!VX>fi9x0ll>{+0M$^Y^<E;p@yf<uNbbKQJoYD5P;Cy_Q>scLT!xPju+_mwfoG&(YmYCJd8~9Fl2LIFFe>HfVUZbnL+dy6VJj3n%v$%*)JZHZ5;E3KIWG<M79I8dqvY<l#GE+j0Zb0UhKpe8Tp#K`756OdU)-@qczmtZhdgXPQlEHh_1En=~`ceMl}>{7m%wKJ{k0}ad;gKvxN#}bt3m>)&E4S`gfK8pNAIjAid<Y0j?ndnmk@9@i1+Pz_d#ord|0<Z2W9=u%bwzu|xU{Wo*&}o_DHhxCke2yG=YjTzE8hjnKneoF3l!OC0{#{it?a{Iov#irJ%%#hF6e48DYqM{?-k76`uXXAJ-iVc6PKuw{QeTm+_=%_H$PkF=L93Qt@f9Y~5!^JH(<Rs*il=G%_~Dph0XumW++$ZSLV9rLE!r<}-{HBKujVze&zHCkh7N)c-{#LwTD7F(X>tS!lGgi=SR0$5PfI1NcQ2_zXyua}ce&NZ?(A_L!Y+DKWryk*^pIcRrdqTP+V`<>7pf<}7?`sS#61VncN3=?;;@Smi`*|_JoXc?%F1$l2Ezzpj-K@l6`S4(g)U^;oUN2ECv_e86wp2qOKAg^$_`@pv$Vj*NA4b0LY`($D5lSU#at;fx>*N)63py$nX(+Au`S&91Kc<{J4w4H~|jf*!o)`bd{6)LoVJDe6bOjg{m-k5ABGubS0Lkd9Xb%VtWGud*aE4Vd?zQ3PXA9Xi&)ZN)x^<-z&YSXcik|IMcQ8wig^~6~5#!Hfr)RW0yVjxl^$DDeF!cAZN1pcYUn5!3huHJmh^1+`sXruG=2jy-Y95!Fi{(SxDlgeGj@-8zMo8}MR^u1nYg!jX3qk*hrlaiVRr=%X*zY2eyl}|4ok@Vt;rx)MUQ1=;j?h%%OZM7asiM()mNPska0g@Lk56PA?fKfQwhlH0q6<_b;;`Je!(5V0lxUc`y?Ns(Wt|qXv1aO*d&q1`Cb(kVf>KyUzl~5wF9^jDp0EZMAbmy3(B=e3EIjxOORh{T;z3k1_n?Gp8>rrDo35XqudUWt}(BV{xg%@yEf3Qi^qk|uzF2-1Oys5kDCOMBpP$Tyw1O^>@_PC`DCF~zE^RsaAC+@BkX=_m5oyTDCDuPKfwe;BxYSJlt4jO<E<?VV9w`uY$!{jd^aF884BME<<g%=tF+GJ;7c)UnGBb^6|GQ`m8EJXGo^oEKO&|RVo#e5(cJi0{|eUUlQL`0#9h-FhxT4@G;ry2OeUjY}sx(iWHgwcA|H$788GIayuke^#Ngg%$(>|BE9C+RFCdZSK};WZK?9!NUxyw7Fwy{r^TZ_YT48=VJ+TmrngufshN#CF*B^jO`$M&*8*^iXE`Lm5a^4b5}1_$O3ncz%2^b7D!34}s48D{st;6PXti674~vjl4I!(M2DNFUD6yUX=MXNr`!^<m@nm^6JA3Od7_^z*)dYR+xbyGy|j3qK>vH>QE(oA>O*+ymbW8Uhcxcc!Y1E>~s-z!T(_O{&P?6zhdcA`7|CL?478-FTrheW6-hT&#+wQFT^U7#4`RwSjM0Jh#9@n;&)STHq**h^Mj}DiSJ@4w2Pr^xEL(L5#*Gpdlpfs6BNi>Lwi^Ho*!i3Jv`3=l{U3KCH<fk@hcLYkmAt^`LuKgBgw4NNoI|<W(?YzG3l9#p0(X0S=(+yOFxKo{va}}rp$TUc%T3Y1S<o4YJ#g^VXfOH{uGFTb&sIe@{UZS2O1oma6I6(GdPgjCAXc|evYKTYQte2j;p_+2Cc)Mu*B<F_=o;X%lZnIFR6wz&xg5)ZtCW(I`HXlds*IQ8lKRthUujLGTHjely4F?4D#CO*AV~VNg^O-(2PZEWS*=eJin&~u+oUI(VSkPB=*D;-$ma`Grh}=z{_Zw>dx#tGvHlrMg}ehxF+*Fk(=RoejARTJsbx(W{cjF0#cPiOI7NoRHX$3%6G~Nav>x?7oJG>fotQe#L>ZHaR=HH#t2iD*M^>n#jR1%@@v9<fZT(|at}@$Fy0^c5kcP@J*h|-A42@Vc=@}y52HOd0$^rI^bIec0PDjT^da1i`Fs)(i-{44F=>$)lOB&TIWHMCqQHLP5RJW1Hw2=A&dLWnD_=AlFKx2%G9SlKB8d?-o*2>iOYD4GV+DZ0x*^j2tAy{oV3~2?D+3uY7k0i}+3|8`r^~}1E<;b04&Bs~llNHK@KB`&XqEcV{JsIB*l=8s;rMefJO((%;H9I3=6)<*0a_xF0~L=PxG{b;{u+BMb71nQkQG3MATTp{qVT*X%e<Gv<^+f>9#Rzuf+>+8m>Lg)Y5XPj)4Y!kanj0W$z-xch3D$WYq(?!-cYU+trrcnPMf0490B+XFCKj%7Rg8$GRj+#2yexLf4sI>j0Qdl5aeL-u!77ZF^WHMB+y6`1=m2FBV8Hsa)$Y+rMw0#<&A8M85WFu8ks<Myyy+CM)qE9%gYSdcg}3szR>W-#ZRf0IrJ<%%dDNqh!i&La}uN!NQU4$^b0r=JML~?-*ClWp!a$<O+KCNtPZxbIybv4$?vjY(t@kL3?wapJ2~wxMjfzmnIq{Ymy3S+#jmg)4&8fvMbXY>x6}XfgUuf9Z_~YC`VlA7N1VKM#Ie+WY13dNfv`o(^Cq<Q!K5hkfJXX-2#Fh*It6*<Lc07->xib((I<wI*^!~OmA|no_ShAj$Jipu3SIXwX!OO{L|=@p;041-*Jz~<pzVQ^8jJ?6q*!)>(B0*qD``VmA)K&6IGBHtLI}&un;G?f$|F+fZ8+rIfI}{RqLw3xLWX|sF($&t7dO~s05a*1O^@n~#38C#9y4IyouMRQ^(V`FLiP;M;wS=fWqWECOl<_(eU|cjg1;88n`pFLa|BY>W;|qV@p{t4Q^e#h;VLZ9*HT*mph%a&gs~e{8LDY1?g2|Ne~PVJ8-3Fbdo?233g`xl^=%ZkVcq$LwRjCQ-T9`6c~mm%dN)kY7|b<#FxUMRq4YUeEfpA=CA&D*4?;ZxY|VkzRer!jUjw*@3^;8hv8EZxdu||!cza%|(>?_}^AhvS3-6iFyk!1z(bbGbx3aoQE?qF6*-=%BG3632I=<Wt(wp6$vD+W5a4Ub{W6BAx{<D$y`s`WuhU2vDsQR;R$kkslTLhx3gk+LX^#o4?CE{xU%n;BXc)5Vw12@O@P8;NS(e>;-`3qE7e&!LL_p%wiaOgmbXk(Ds<6uXRbF(>@=muh@8;Ig7UWtBJ<27W@lel$syvcz<@y#3ajjM1TS3#fjPIl6}=uvH^N3}wm+G_~?f1+z#_&8*v-FYV#!Yc?E=q&%Ev-}VCJ}vZp3QGdc8+b}2+D<m2?S!{?=@bjg+4Z8q3c6aev1-lEwtFYr?OlO*>dZ$(WTAarmG*IM#%4pZ%8*EM7pX3^Mr}U<y3@Sd9vDvp5nPSFz8*@IUObX4#bTv}=cScctaRf6XgwAyJ$Vn^(rf#NhXJ5H|3(X#Mt~PT!?^gx3#=0FaTD6()@YBLS_~Fw00c>V^PZc*+J0MT`>hC}vH8k#kChB@9jC7-I@$>mZ8OtH1NJ^zcn@6lhY)U-(568zu?9WE>Z>(X>{Le4^UohLf~+CfcR$NjoR}LJqhjR<9k&D^LAm>jt~>oe_=I}Q<6S>byY^>Rq=s~_`Uwo)9d*14!x1d|a~5rH*3HT#Qduq(Q+F(SBq~eGP2G88^gJP{_Oh-VppNTAc-Gu&(Jtuij3=ndiTtd&fx?<R3Ty7DES=kg%+}u5XM%*UyUB%62RVQ}!h<;s<k8$Tkt;9l<{Vpv=F8;b17?T~v-9Ye%8bpAxoha|XA(u)o`<OK0otao%+wSNiPwQ<TAQg;+Ioc2*28<Pb&Z`TyG>TzE5fRKZ#F$&CzW>7Ps&^R$va<V{xVa$VP(4dNamOpGw%Rkfyh4uvryh>$0LyGw&-A#SDuPjd5yp$sRg<Up|L82d&mgv`v;2XNcYJevHJA&EMJXTJLW~pt$^FiwK4-A6XFEO&m%l!1n%vzb*EYas>-(|Mg;3UH?ZD3dK}?q6Hc%YZhH$nR<SYwaT9E!_8OZJGT3S0^vPeuw7>#}?OFs14Ge2EFl<)~v&&Ro{(3lPMC{hgnVHX#g!K{DzzkXgGhw1Gm`Sax=y!6!ahVoqB(sF%&l|2W_oT7ri)7LihQ+_Sb0pMD@KCRt_i&-}&^j$0A9M^@VuiwzV}S?8o4)Pb$z_ilx83#~_-htpI^~y_tbzAz$4*qtJu_brQVKHcg3S%6s-)2RkQSiM_i!-uiDC70lyoSlzVO-=Akj_t>le)5fT08in+{;PYhGKR20Gm3$FwVuoTEd?a}>vHTwxX(d0uJcdE1;;E4v6K+dEq1)(a=5ft0<IyAX0!$YR11pE7``z82E~Ols{;F8)$5`zQm3c76W?V`D<dk)tIpRR8fv${t{wm_Q{2i}>Ua9KvSL0Jtdz9oZSB3xyonlP=K&5u^Xki=#T-`<sC{gB4FRxKDEuOAIj>DRr{}+9Kg|%8%92DL!PM(zW$3o(ck`fg=O|&JO%1JMdo-tZwqvbi0AWu65*jaXDJXcH-eTna@NnkvxU+mZv}se<4|x0oh1_ak0)wpy$0NjyN}*M{Gi?uuB~0Mc-}74c=l2PKYH4s0zI-gTh;F>!t*#2ZTz2`#43^Ir+TDWmB?nZ@vfGknVdN<rPXG*QXwhwR1bXVnnMBf@*9{e8)BMPq+QSU*crdg9rxL(YIfaS_=)`C;{k32}3u^26O}SmybQ*2Hcz(yeV>`GYT+&LzglLYl)n(NRekiZJ>&Ywx>em5moE75wjf|BzSC)*+j-JvEG>t25z|_G}uYPUJAVNaK~<O9J_&Bl+5R%l$f13;O`xQ7%N@3JMR*;m140i!rOw?JGty(wgu$J9IrrS58_u6rw#H9R9vD_ad}goDx31y$_H5Yz^o045r81tX#=92Vi4`;6<uVq&NUq4lXre6o~9-~Z-^jGTbQC2Nq-0slmPgLo1Jy4-eJq0n<9zjNmU{M#38Lh6JAYK_}r5g$#UuOXqLfW;+di585cY-2&TI^f&+W16Vk|MG&Y*QH19%E0=Lq|bLCbfr)Kd~xkX?$@2>xNLn*uvlmZR#40(wQFDNVc3mg&%>yk2K_mKcKp!sXAUeiER6gf7X)lP*)5d*6`ju$|6$7$GOcv~GRA`!?##B`PzVR;4=hME+qYk!nve}Se45jqnF%W3)a#2xx<zO%FW!Oopt41uDUt>m%^6L<k3E+dlF>=@eaBo=uDo1*Xa#|IlaG~%H{5wQq50MG-8R%C2$3=Z@z`<CU;4e8o6?!9pGgpQ8rEIMNBIb^2492bS>(;C=l9!sY4Sn`%jD#xO8Gw)+D%sG0OWd;xsmus%dIG{zMRB?BKTcd87rTsm6JEn48K&<%#@UR^}_wgblO!atydVc79dul{_P0L?o41$gqV1pp2fo5eAG+Lp83R=sa+_dfCD2KlsO@^`5eE{ti*2E%oUEwdWumTW7GGf%ui_W6Equ^xNZS~X8KPIPg`fIMXhvonGAx|16$IB6I9iZX6-o~rHK>M2-uNUlrXajvyCc8kk(cEa}lt(b<Ylu1DX;i@2bMY_U*_9*V?h?;xFZ?A|8lTW<e8SLR{hGo@=;Uq7h?(j7ylD?u^Z)x?ecr&^6?DKae+^WhH{fQ=e3pU)4EnkHi=g_vBOHa!i+6@E-hu1$feE#a7qIpDK!sXzo~QuTdDQ?fq3vnIMnq{3MA;cgk>dr>?tWVST}ZoSWR4v#z%s`$q1Xxt(w;s8r^&=ncUTLB;N1lxMup&2J_K*@elS`-o+9$`v>_i)xP1HtAXnZbH?jQ2!q?>p1F!Ix2*^qa{6qkqr|a*9*56wUs27e&sb`fdVCYHVLQnKF)MAfN+F775vAh^`sGbP)fyYbJUk@89UWWkKbnx>Ae!d4=7(EWCUudj;q3sd38=E3S!Y*{hk1oJbB|j1&MwCsRP^H`X<5^;7-ZVF7X>KmnT!voscmX*`Dm=ei_#=q$M-Yh|L1g0yBD{n3xsqq>x6Lt(#dzBsF96>*2rH(tteD2im<B6jnyidTr#}|b7F$lVwYp+W%ndtF6#1k`>6SK1w*VwBVq~ab-tX}mWm`VY<~3*~(g=jt0O2}|zP>={P1#CytlCK|lSgtL%Bmm9V~m&q4%tov!=Sp|5sK1TJU}o2?hqc_5lGJKk>tFwk(@X0qF**mU}(yT==_c6)R39P!cH6hroRGBffN9{7H}kHmMxhJZInFiTx#%^^m6zu$Ho958X|;aWh5j*I9_@Z{;=_E!Oo{W%}65EiYHR(=%aydyr)52x@{D$G@}q8mq2dU38-O&2dflctOp9u69+`bKmx-TA7UL02z4MlxZ!S5H#H(s;e9|ol$0}Rz}DJ?UuEAdL(GLj2{<`2^voz&;}{=9c#RT|kO@+<-m=ABM7EgF*<wOxiwQpq)!V6g`CA>_4Kup7Pa9gNOJS^g@c#KjAsKtxd4QVTOI^GOH~A9RqpeSPWo+?vr*5T<(eQdigFE7qT0NR8@v_B?k7yu)q+S=nncH-!T?4rC7RHr#`uc|NLc*V}fo2RMN}ya=DNwGg7ASXG3^dr5w*_K+W5Vn)VH(dBfCMIq7MSFSz(n|FdW!@Gbv!W020LNbIB8pHdbNU-fsC~gMakqP8##ismpIZspem_6sJ}<D1O}cZfKO!xJC(8IAvu71x27@=F=tdiOPDcd6xy62yi{ExQgw+-)rFU;XC7{z(VO3<1=}}2c8vf_-9;*e`aM{za-k&kmxu!K>iii(6igaXu<Xy_>A#DotMKd+y>BlO%8buf(fj_w9*9FpLj~>GA8Sb9eVdnt)IDj)X_+qKFyI0KE#j*iu=@oPQ|O~g8@o7pL*EJk9z}RftdX_S_kceg-nJmv^5RF!Ig+d=@npTiUt;CKK<ZssSz##AqCP8v$1ps#Kn#2j$H0&CV(N1Mt%+x43y&))G_Iu4xDo(x0vD&oefSEpa6IhJ4#%Y1pR;HvwN9GKERe(oju)IC{&X9y{3SLXqt3(R^~A_b?;6?K)t0{oQW;`;g3P8d<W8#$Ps>|IC8U<*@KX+fi@bphzOB%F+wx*U;3V=Y5_+zQUE>O2dl8fL(XzV>4Bl89k$4-_sdJwE41VkiuMTSg*FT~{!=_KzHO`PKPg000Vil{X>r-(-efinvAHM%ee*49jzj^onPLnvn13jbd*w(uJ#Z0=?3KX_EkRX#K90-#Oe~FdHc#Q~~Y;K^&7O$j9ypCBA8N?fn<Au^VjH5xOj|SrVqKL#0%TCpJr^yO9O%S&TMxn%<Ca*O#N0;0TR&g`;;4A>ZgBVy?EDpXwkEF@7dY#Pcb<$oiyrY`t=!2(5%5Mhpkf)l;o@#VfMq^nSon>WA7L~E~tUftycGv@C?-qfNcN{*B9%2fQ^>_^EU|%TVL?joVH1Vhe2sAvj&}{L?W<VG^>PqXVTL3bxOQ|aqUP7}#7R|m)Ec{Y3E%p{f`GM0z`VM<x8zeGl_5!LfnLZPQD!*vGNHHNF#Rqk`eoKt+F(M3-xxpY=^fl_m-ijzwEOd!lvhf-^Gk$J_<K!l-@mqXcTju3@<xUB2y!Ni}+PlJP?~Ea@WLn|(7WA_f^wZFwpDlCbb`}bICwJafIhjOGh=rjyT2sUvxlrVuydc?)1d>ho@Ssd1^?-1rMPHxplN4xR4|y01U8?u3QhoRc1uN$Y!3F4pxSvaoNx>^;ENKC7Utn=jkl8~Y^=>IFoK`(aGR-{6RCHDC7Ff?@g4aDIRS&@UfD~68Cz<zhTwP7=D~n^*Or|2N%k<`i^|E9_oBK1wt`?SEjlKb%8C#Y4T%U}Zxgg<Sr-g&#UdbgXBK0w}e8|R+i1O|M9JwzMknNPuK&O1hJLNNymP|VsXT-rcHyn&J;$RFAcHlb6W<H|9nllot`9?|ErKEHu2@9f}qzL6CZ^q~dFZ-#q)lj$C^_bDK^YDlfizEp!nBQ`K_HusE$(sJa41QoWBjUIKOXw4g{E^u6C6VW=M#{U><_1nMVW(}dKoaH^kQo5$l4ds9Bf$j7EL4c-7EjlCU`U|LnIzuwmd|4;YbGnKS#)nd)4hH1BXZ0giIxoJ#cBp6?TH5U>40{P7Tcih09j<O`ZxNVo$gmoe+3$Dl7NJX#5Yv4kFg+t=@$K>`b%!N-A1DdfR?5Mb<18=eyO`GerbLh;0Fh|7+9d?uW(T27!;_S2=)ntKc$WEr^JUpJvO{@Qvs7n=e>!!?_tV4kKvy*Q6<qtmAog&(MGhEBB%ObbZ2KgUWAQ;F%tWrA>slsP6(aMh(W}kQzv6MYrDS!RY-RK2zQ$Ecc5p!<0Y{3cd+zN>=G+2vN2dQpK|6ITmd{b_snp-R@(8}?ja>OBMM$6ZyUCnN-LU&zXDa=t#FX-;)85Mv{M>cwQzg}88<fgYn;4t6ws(TW>7n`%{GI^)UBuMUT*%v1O&BTF+Kq6=@y3(?J7rtm-=0l<sK(7^TtZyIZidgnrgh7afG<q2#z}ty#{AqC6Y^JyG-r5KIHOaO@3t$s8iXlac8^6gI4pbK<JPje^t1m3%WwB7T4YNNVFR!FRP#<6(pSMcleuf<y9$HaM&7`0$xtjuUM**;ZtPXw+9BFNg*WqsRWNV{mS#|SFFgN!pG^fNaRmH4Rqt!x+U?J=^V36-%C(Zc7vO--XchFA7O&~q_1zWAQk;kk)e_MnGBnZs*a%u-a$w3@)-hgri@$i^9`wC9nS%p3>UIF==PTrC$wnPKnAkn-2pr1<p*MWTm==@XB&}JAwD9>f&fIwErWLF8KThcuRslX#Si+M^z|)Xe3~OcmO{7DM?ir<;uQfhR;8zWEfhjAXutUkg;40tg1m!*AoixtkGLO|lO5pZnrvUaRUQ~pKW}hk3PeB_Iy57(elpAtAJ7?>NJwSn&6+)w8K9%m>F`IvZ(!c%dB;ScLQ9VuJO+W&)KA0!4jx5rXZkc+vb<QyGQ#DvqRQlF2UQR{GEYp0UZTsY8c`?kB8X1&{v^Wt`*|e?Jp$xj`S+VCnntES_ADnb@lW=|-+I{7-Uz;gfN+i0xNeT^CqI8r5%_X`K@B!>Ivj&Hu<;q(dNOw2O~ww<C?d4y9_Z&4vcqO_n<q_D&JixM1nS6K>9UJQ;ptem1VYA-N8Rupq>P67vJEZ4T8L3KXi4deA*#-FRCV4f)6x48(#Xz0xtkX&H4r`@=w3r*?GlSWBQ{bVju)UfZfi~pjCNs`huQAd4+{g@%wDiu`aL296}e9ox81QgZTOq*=Eb0CWYb@PcKWLM<}LJ@q3sE8wc>9uA%Ym?+HfK54q7K|kzWMl6dJ}&eju450QBrr#fX{2<maU`HZPt0yfgrrp1T76(1<nQ!bjyyl{PSsKsRam{$(QDLilV8+0C|q^;wJ8XIXyd8S!K<t)4@*oh<-0>pozNq1|@2O3M-Ank9{^{t~#Mn|Od!+672~0z4B`rO*8{Er81b0h}>+Tan=9#CuRAK-A{zEK4T#QasciI16$%4_YR%B9X?4*GNbtWuy33{-ZZr;|TzCm>3e(<vj3vlgCYEgp(7{Y2)>vp*btU%u#g|gEuz}{8fWYb1r8&>voi5e0L>as*ezd`g5veGJZ0G&dxnx8+|G#xjYeUP09>Kcnc`jJ3Z8y{tEPm5?+%e_(US|+ddxm$AZf{JcWne<1;`|Sv3EnY@+)XGM%}-9roOT66o`{yC`Y+flS^+<H6IIc27<7vHHn=w)oLo-7`@3z#;p2)lc>j`@~<(&}Y;DBduvnu*YPgsk@u(`RoI{6+}4go(Ui#P6-&0D&2iQG3j(|<(0xG(8(v3&PZZu1giDSfz0Sj5$$dFfYD_|`p3c}?IZRj-MQ1C7C;Gfl}bS0Q_qu$qur~)!{}0km-oy8It}FRUO&`{elwzK$4<jGXMnZ2cC$JC*2s7N`Q85oT(rE#')))

_INPUT_LOOK=6
