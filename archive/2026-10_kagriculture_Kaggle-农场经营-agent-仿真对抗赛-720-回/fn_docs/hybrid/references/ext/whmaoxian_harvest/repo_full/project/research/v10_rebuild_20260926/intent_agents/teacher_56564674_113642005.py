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
        if cash<cost+50:break
        orders.append(['HIRE']);cash-=cost;count+=1;hired+=1
    owned=len(farm['unlocked_quadrants']);wanted=int(needs.get('land',owned))
    if wanted>owned and owned<4 and len(orders)<10:
        cost=(1000,2000,4000)[owned-1]
        if cash>=cost+100:orders.append(['BUY_LAND']);cash-=cost
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
    orders=_market(observation,commands,needs,daily['hands'])
    return {'farmer':commands[0],'hands':commands[1:],'market':orders}
intent_agent.telemetry=_REPORT
agent=intent_agent

import base64,json,zlib
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqUyo$Rapk|uJkLXB<bS`7$gxC-GKnFzgjXO80e&#BfW7NKz%C4b_odfMv8wAv#5s|-s=J5%BuZeaZdcu#H!|X!-}%$Ozx#(j|Ks2P%e%j7@8A9Fpa125{Pa(M`qRI^```cPr~j<)>yPi>{nP*a=^x*H`_&h}|Kqps-oN|en;+i2&p-X||L{-$_RsJBD!+gCzy9sdfB(;a{>Oj)>A(EP`-7#w`Quk#fBARce)#VDKYsf7?k_9FU-|9VAHMi_`<Vq;`Sa!e@Vk#6zJK?={AF?V7k}~L@;ck`f^xCouRnhL@|Oie`-Gw_$mw{6s2`E5zvB9@$WQ)^AK(A{E4QPs?YrN7{P^wVcYgJ2$>ATR{Lan)I)470Z$7pAYp?&zq5W7_ANDst-4XBp@bT+!{^sHf%Kp+HK79Z2)5Q|emWcal)nEGb)08hVAAH(>-SxjLo&M6NpSHC7rM_?M{ZbB}8ueEPp1A8@y=zZ{`>QX1<<l=leOUdULHwmpKdorLTy{UL`%9mG+R&CH_tTcY^vS15(zm4MzId*_%X+ajh_@lB`?Gj2o~hlK{*RIUrQq%&z^7GzDY&~N;M1nRl-OPLw~=_YL-DJQ>aS$?CGkIX_$$><Rrl`dzGRZW^yv?iwcpbJwBj#)`e{{L;_s!yU;6aZCRGAi`^{wml)W!T-EY*#V`?k>Z8-T$!JoVUpH}>(;7=~Vr*(fR_(Dtmr%CdcK7FA*`6hq-@jqAn|MOL~&sSf3^Yzyszxe*|{`%vm@4x!`tN(ua|C{_H%a@<N`SzWEC@awC75rp&vE1J%tpnOd%|F@mmRhR#hlJ)YeR>OaZPzK_&tG?cj?Vua;-9FrVtldZW#st#<S;ArfmwYy6?E@7u2HTptoo&;^-B->K~MglrQOQveJS95+1aaIJKI8_Nm8iy{mq?UwKu-@f#>a9LOv>2H`w)~V!e~vUEfLerj&twW$ztzee*TC7G8WkoB5)&@`tDHFZtbvPyg-XcTl~2Tfcty{ihE<{O04QPk(#2L!O-V=DYrp2ix48#Fq5rK(PE1{q3(%{YA<VGB>FCaMZTQovo1c){LB2v_L;ypw1}l<7svKO1KFlnQp>}=ub>xOAhr@2HlEUd^-vF<8Pl1p$oxI7X^bZPZ#u~7|(*R&jLRjn0#kB@iPJ8JIa+lMI&eS+goSG5Bixu=o`<ex~S8=lF9cw65WN@e^l%1F8H9}u$rj+b+%_KWTEEDqYGE0MCpDrP^&gF)Pg*$HU#e{GWSNo?~RSlphR{VLI1QxU#IX-w3Js{ck9)jzOxnn-Bb9Z6+BfqT5@|Mt(Q_?(?3yYSRD{G1cua^e{wT={9W{Q>Sw6SO8eY)puC(?m99~Wx$^?^bFAZg_2pl0F_k_VO!oL8bg%nnsI*aQR_iMsk8ei$9nxHAF&(foK3UO?%Cf(;NH;1?@zpqbr$C~WX6D<i*?e0!_O{jc{?D)k3n(Ooui8Z2RrGrI(Z$rJu*NB;E^netcNwsfW6~u@*%>YeUb%e7Z_-`GSKaZ;{4IED`>sdYcLOPMP8~+)9Dmy(2OaHow;&bw(d$ltjxAa{8mBnmRgTw=NqZ>8Ux8MFLT(jCeac%m7F%taBC-C~$2@lJboM<lPa7xR|9~m_Ej-v_2x)XUvPIy%@Q@axeK;DYPwoTiczc}L{YBbaVnAc(!$Z-0NRL?_P;)=}1^{c;L^l|ovF%|syBDs$KkA7JuXfUJn}_v8N!20n3_p3l1GXLX{QBtQ25o}Ho*4Sbw&)WZP#R;;i(X9Y4yj*OeEHRHW9Eay=j#Lq!V5b`-EO8rSM`mq>N|ZpS?uXV5<Lg8UZJw{TV-(h<R_~9A)}qS`(B-u*3nt1808py?PbqJ(;ivi{Pvq~zWWHc2HTBa|BG+*r&$iy{e0CopP3bpTnF3;)n97X<i9K#2cLF0(jESKbJj14m*?iryT|KUD{Y(hyK^2@Ib4a@qA!0t(xH01)a+tj{%oW}^?0e-0R3gjJovQ3o2>imO?|^JOBVW(%U^FE07bJp?Ny-mW>@x{Q+M?u-EMSAd&<P#U90wt39!31ZE@b(@0!u}nA(zr-bz5}Bot}nwuJOaBiGekWm|)7uTx4Nf9Qb~a$YhnFi_T&t+KAtz1GF{T6LjKrtiZJHbk2CGQ(yqmn*PGdiu*PC&%R*5ZptuzuuGpT)qKwKn{Go9;^%}D$^bQdT^&4p|k$+dh@I=N(=U;7^UYneP?bn*k0*mJ5!79l=9tJzDZH(CWTtKr>&~5qc>po*P9It!SpE&=&U@V{X5Z9;?(v6u&;joU>5Rwkv(#NfL-;qryA1LxwKZ?_$9|y%`w>~px%}rU_H>aJzXGc=H<<Xec<w!n;pH&!y@*H+S`4hzx?GA@QG~xdQ+2hxg>8MsWW>HTIhZ({(5sLf4T1%y2MJ$5;wcf5fy3O-7Bsd$K$gS*@Q?;529Ysw)(_7g%a-+veb(KjAceJGf%2Lzt;+P+w4{?&}~!x4_GcvQ)~L>&lC)T^6>&g%YNKfvj)b36zIa&ICZnE>a@aauw9S5_A1ARkV4LzlieIpCwo9$>;YBpt`%AwTh0^5s^`tj*B9ISR^jiI<Bi8?U0~Z>@i!sN4=0GupwcSn#``VDZnyPBLDKV?pY-?HJPTN8Sf}z?z(PX<Re3$fIL~2(c5vqN&Kexj^v(LZb7wW${kCX@c%~KNve#-t%rDrxCexBF_>ehxtiaOC_`nQ0Qk5_Mb(P(>Pl;G9Gwr3rDgT#8@&CMN>nwgVy*Lkr{M@>Rld@`zlNM5(cDfnE`(%VZ#qc}Kpm&(Lxx*~_ZTr?J@Xr06J@?Z!`Z}voU`SxJ1~*zE>6%%((`Be`GA~#zZ$h14nNWxJ_39#;#@{0q=#|iDj=rbrrYSj#Rsy8G!*iyE?zx_MlN@_N@2Ep*tQ`Jw?`gJRGx_Uu!KS+54KBdxc&Rxbxm+^2ES=+}rrzmt$>M@lj+dI1Q@N7n>7r)ZQBY|^06*cMynv3EhUrF(#0uRz%Atq!j=Gvgc$u3q#BB5sQympH=pa-sR&;DoS}x8Eol9CeUTXfLmrDkhv~;}GtUxc9_}kC&mzqt5a#2XRpC;ljH4EQzRn!C$m6T%#Y9&JkAJdO6;oS}5y)3Kt%{JEEaCsB7=<6%%&#w0RG9(L@bzMkx4LShsd$ZZO+2~C?yp6WH>E_(Yf!oXBQu9YFSDHTc)lg^)SEC(RgVwYyUU-*j6`QWrOFQCw(D63WZapN+)#b{`-(#l#vWF5GFPHkSVeyxmKiK6G|25qFrDg?qxx_sM=sWPje)G$Henq#6Y@9isZWS-Xd%iU`C}#zijlCucExJJ(UnpwWZhZ?dx2U9?!_Wn6b}aQdY2~Rul^<L@-1dG~;6mT=1P{MGbyPGjt%gBr<^(L(%Y3zb8lf`3Ucb<|GQV8BNG)4tIcsY6boZ>x%<THHFYK7Bv16{TjrN6y?B9P(3(H%1`9Y`Ut((TE6KQ%SmM66}S!>8Gd%VC%nL9q(8zsf@0;8l*7N8}?@m6SYtDMdAro_@p^QwL!T4i3<Z$#f{JM?@Uudtqv<IUU>haRu6toQ|-31)95*q|Ruju-1Q-NDXu=iW@0SNsXB_$!-@pi1j;I<3bUn|hpy_z)iJhDU3}%i_m}avc{<Ae8HJW9`u?q!>eorY#xKHm(@mjtSL<)@`#ZkdhsXL1E=fos};Q-{$mU<qG$AO*FnI*-`Ich~WV=OLZ4c0ZS#pkDSN%eBC*AHortU+5?BbOx*(2+HgfXu+`{N7Hu0_(Xp!-pEmf$=8K(XW^y`G>BMSSf|+;cSeK7wfhJ4PfUVK0<3XFV7w^puB+C@uo89=(;1hfxSAK<j+xRzrU-8xTFO|<!b`CFwwKdV!)=XPl3thw1%^C(!Y(rHqCido0Ht8&RIJ$xA9W9<klC1+=yC?YbuGtTj_UARS?V~r_^t0APHJCtgVpSTIZTujec;GO0{XLXDdrjT*vjcV)J8272wJsiWoq6V2;n7o#7SHO3GGPy89nC|+P<Ta0;n6Klq?;^kGa2bVqj$Q}SVr%3rDq&z?oVv~g-P0l)}`wbTl&CuseAd$SKxQu4Y`c2kqvFw8}1!_4prGXR09_9_hC^dDw7>oFJJ+zxx|bg!i%*VFDx6pIt<WtAKdD?Rx2RuG|K4e7v6WPHYHH~)h#*$I!8rx*l-W3N47M>(x6Wgc^}XK&moZDx6^{($wMp?ulN;S@mqPtZ$C}GJNT+>M5;0#Z<(w^=xJ19g4J_Uz~4QyK(Qg1u=1(O%BLDTW*h97ZSHl%0V=_*q!=I=-Yx<lhR`q=;~zF(Am&Da1Io2YE7vx8*C(gF6|zJTt3hy9iINZEhD=i;ralIE!_agLBh&J(&dl37b$4<-RURGi1k^igs|zcmDy)pE?8>Mr4Nfc3`(7fbEupopLTg=RQ|p?^xq=b0lQ(g*5f^6j-&{9OC!d3wwjdhW9~IIs=E6@>g$!WQ1$~nC1by0_l8H*xL(OIS)tgU!_1@>6$-q6+?{fZt4F1s3MaN2Gue;37>4Y8AmAw~gWnZYBeW8xM7wUX7klfQilCG}NX@X+saEYA5>#Lu(zI;5J&{7qlr7E&1Re23;O`>mw4PeV>HGqW-Sh^L6b^_5xAY>?eG$<(iEVt777F|R$(PkCJA<_T{vNuozRXZt0JNlf5z`DL_vhu36=VjEMlYDiBx6g_2qdOHBVt-Qem%*rzK+80NM84yr#tGw_JH;P&sKbrO5T0%oSTQJmF<9az_+2I4XEM{ttn4m;nhwC07H@1?{Iu2>R$CgnzGrM2J0(`RDu8bG!cGfz0H5Q*=PceGnRsCkpe4F3f=V1TS)W(CWc^h$&h1+CB}(GQPKM}dLalJf&o*dP<l<dyJf2Ix>6Y=E)-XX#*F~)zIvUKSwEn6Urm*R^-FnE0;?hoXzjit-z6AX4N7ZoWZSsT1`2upe+Zl5T6Ne@9@;pHX;h+)-ag$ZnOxE`7Zk@HFP1cFFHjQYBHq#f{OkX#>wT(t9=?%qXHqp~|nD6$~F~5L-EB%=FIXrP8(4;wh(VwEsI-p;}gIDaQNEhVM&#T0qSBX5YMqxoJR=@k*$B*9vzQjV?_Dv%=5Y6^qpp0)neE0nyp~-K#VP)L>ZPQ;10b`18=uW(lR3bvs-Sq87PnY@h?YTK!UjFNfm@enYbop?=W<N7fZyGS7*w4)I8swQ#;|G9eMr+ptle4V*wG-cP7k>%d$^i)J+TqE%#KuRc41WpH%IWb|PUn4>{iKnb{cu&J2MKg7?J>#m8s*`dP!QJf!?lpEtd1BtUST0du-<B+N3nXSPGG=%6sz;oANA=Q;I_~FggNa^m~SgEqf;Qy%f`vfSnyQH{h~=BX_Fo=zK-3U{$ld?ejjN%EGACAoQ^mq{EFSC6Ak~t7$B9mj&?plZ}QgB#4|wDd>J{{Xt34s(T`FpU8u48oZR;WI(i;u<BL39RiOt_cF4WL(;cuZgMd|*jwYxG=be}6Hmx&4N_5MPL>KjWJsQD~udWe(ty*qMz!G`%Nt1U{u05=TH3FnD?ub5@rtQ}~eQsm*xr5c`&OHRvqCx+e*7t4-aP)|T6`8+Qp2Af4^s!=%=8>%9pO0_fegEmh55M{N>C@jLFPy~>VX<C<XbJ3-RESjT00<DhlwQK}SE{`PJuqp~55XiKf`D4Rn4JM4@B5}R(D`c|JWUJ$klj8p8OLWo{j>CF-vIF}TSfZ|Q4CuU!$gZobpdAMhskGwTp}ECbf|{tj0dYTUaZbIrwIKe@2QjZgn0U_-qE%X#vYwC6;#r`*4T53V*;kcntFvj{*=9rAK*GhWq6NGP`bIQ#rGid>vd<s^I(8?@90N)fY)b%X-4uEBVc9&Q=e!|ecn_D0`#w=^VNOGUzm2H(AtTzshuzZpgI@dCH;%gsxo~7QO#B;n}sNR6k=sMEs)={vVPCH=l85E^tZCm-$(aWU^#~|Ja6>y9FP)3n*Bgxy~u;i&E?J9e0OuRm^)f#C04pXgN<9w+vMbq%WE+!$mIQH+1D{02?a~U(eWZMOi=hXqG0cP3U(l2$?lFKB3xYw!p15U@Xyi-#xFM$_K0#u*+vSFpLv8-WPmsXsAn^INBMck@WqQbR-`dhco9c6eRg}Zxw0oKXtdyT_$$zn4Ui+ecz<N#6`A5MfeU1bTi1oRu4mi%uU80Tr$TUdKFkhmR0v~_Y&G{zcMIC#j#t?2Mms|GXpXB79%)a!F{>=}tP;Rv5jUiTuA07mp2~t*5fd_RHZRs1!0zK<`y<J+<mhm)upvm~b}fq&e}$v2)s7Z0?uD0W@p7v{%cfQ!Oe7~9k$<??WM17RJ~fMI3@4sEozT!fEL?ce;lg?af7<YSb3|brW6$DWp>76btbHE;s`4q)XR-(!r7?yTNF<qjml5!@1nLi8ef@j2f60bL3)?!W_h`=Wv;e(tGTFAt+U%N~=Y57p%C8ubol$)gYW#-~+4el`c>HY4(~cMD72AD=-DpwOX^usvITo_HX%`+y5n#>?zlI>1hlyuc1kGvK)b<T{{fxkC;|wqK8NR%suALaJS2Ws1i5BQMc(CK(#g2oKd9Jyezv9uZhshp15<_j=)^nqB#5)oc%v6YoR_mT<^+gC!L)miyEo$MzJ0F`^*U`LLs8CkNZEqI)&%|PXSK0n~i0}?lM^2m08v35eW04XM#g+&ZyTqZ`mA}Ns4?YL0coZ5Jqz_2OCI#SmN2Z4RZ}N88#8be9M{L&!1-!*6;GMt3;m_2MYRAQo;*&3jJ?dDTsiMu`OZa%+hE8RHZ0dg2bk9(Itxb7a_SeHjV2XJ-67S(idl{kdIOQ?HqMOY&biOBh)3+M1h&JDl6ws|2lZq9HSw;pT+K-<%{XgYIsH}0sNiWb<jYTO%eAEyLe`9`Z8I-fOB(wQR9UUcLDNW-v{@5h=V^=d~;XKXNA2ydAkxs>e#I}aa!X+u|zRN+I853=0+}+HCwhT1dGSD}N-y@*06JWf!3wZx59nHo)zs0>kZ7ax20YP6_&j||45Wf_H-}I(&M|(t?!(&ghSn6rO-V3q@m%ERE8zLV<X4JrR4RT8s)-7pdebVyVEPD;gTmtglTsLjMJ(Pl|kCF!uZbKV<Cry%d=|W|t3oT#<r{xZll{>6Ay4uNfHB0W00yufyPcg%EwHyond(rk`efZtj;df`J*OQ%It8K_eii`{aMcEWk)Dr{48!u8q@=GRviGgsC95dz>3LJg$6KGG<Wv@eRi5Gg(-h7Ah!Jjv1U-R@w=WehYHgV7X#Qo@#%3TKaF8vmp?+@PNy<TQG_rqPHffQqtcbWy~ogTWq3V)rI&m|s_T;hr665rHN_Zffgv66vpwH}I#yx4e1k~Dltk{25f37IlLO*q<zgcm>+UjgKT@*&~Ssk{leY5&XZRQ4>bCZDqe=$UQLQ?#2}m?FmM9I@(^P;jsw#gO<Yh7=in=a|PN^Bxm9t&M)UJ$ApBUU)PLKR9px6cMjSjoBk0e<bSB!4ElyQzaH&(pmkfB~gzKem=SwtJU$Q?&_W7Jn%q`+>;OobnF@CmNt~If5^-ay2T%-yW*s+DSUSxgTYG#CXLY2XEUg6r|fxZ03ejN>p_^N$)gLCzl5MacI=EK{B;&ydJL$Qoq^%;BK3@P9v8}xN2{|C*<;Qdx=KKai6Rs8fr#+v7FqN~=0pP!g$5v&O@(Qtk@uZO-Vc8TT=?p~L_OO@>sjCQOn3B9^6E1l^npWX2M#<3NoN|-J8+6jrIDoXKp1)FEiIF8Ql&`1a>l9J=%6oT2;hBu9d33Y4#T!5wCesfD)-Z*r!C8$wm?#7Xi$^IKYBV-@#7Ph6EAXnx^wPdq4Of&@D@lcpQXlw)EIehDx<487GGtrh;AtJfsYciQ^{K>0R_Hz8RQE1EDGZ;gvMP|TCLGG)f%ccFT_n3oSTlI)=LC;0TA%+Z%8OR?Ll41KUg9E+|%)|Sc+6W4SffjBC2mVa68x-Uu^ipDc9r+VaX)1I6n~<=chknM$@zSZPJ^~w6fLw;K6$0+Y<_HPbeGq1Pf*aSs?13u@h?X1ai~Rrj)+t2XS`~&t*V0OKndgKWM4@ibNo!cmzT|Ev3OoB&&2HS))A{gZ5lZdRU^zVfRQJw%gFs4<emEhzzSKbKW){C_n<)#{g%VKqy#v>b6Nb1>#)YBk1-H+pJ}P8ybyD?baF^EtcC3gf~YbV6{=P4$sxU^g*k#CoK3nmI0za)3UyT<qNFgEc0P5qC3HPY~2u3C)H(|lhCa$>!km(E#9>DO~Up;UMc+=vOhe51jH1Yv0RPJlXryY`_upl2a!3NBQKQHo_Hesxo^E;Edzia_|};Ct#O*a5#T+6M>_`CCR@Cb%+1%!+kBncXON^lXom{OSPCs;shcvE77#DrDK^Ljlwhop{OVaF-N&<yv%*IQ578ZHTNy)3RbDrGCPcSJ1<kJs1p+b=8p}jDZAN*26i5V=Z?v@{xqJu>1f%QkqCkue-w0rwCDAv$MCS7KWpO}^Ss}von9rvov3MDQ(32JkJ?Zh#lk-ASBkJtUVfeiP8+#FO2w(#pw-0vQzG!Y<+T`YCKD?ns@+E3KU!w7s*!d>M3gCrxv!wf13Ezjo66ONrK}el~jHoL+q3-N}die8c=!w#SoO+1z9(fy{%hUkLQlGouH)|B@g9$QUe-6IK0EZg9`gG7tkj0BgOC+G6;sFIWrm)6eV~-^iOdcb$0vHhlbOz5Cp4Whx_fp%OxUt0ptOBtyB@!D`<FPS~zr=o;FVdk=T1hUM%)zMel>K-OmxIBZ&2`%KqG8u*Q`eaz<bL7xr!T}l8Hr9tSu7G^v3yQ>7!7<9AOOPRK?a$}WfXssNMMsD3blb4NV-nq<&5@GyLk=R%^TSkGh7_`G-`ovn$a6vjqJVJu9+Ed0G-*eeW6j0i=R?0bLd%k&RIK=A1Q1!=p-mAzJI@f)2`#j<@LQ(`~|wzVABHB*{11Wo2GNKfs*_N3Z@#kYPmqF0k}!i?qcHsdy+X4YI3>g%ddWmwP!x(jOVi3#DDo=We<11=}s~I^pfe*OWr!YSTet~X+M%c>Z0X{6WSPIG8TG34E+$rumIX?ENlvL(uD;0o5m7NfTIrsC9~5&Yb&Qk1#e`FfU9q^q6uBnFlaEw*aTyYt-J-pX4hyD4j|is0~(CptfW|Eg3yiQ7>7e%J%>YBjhnC<H<*r*LgdQKTOIXQ$s^+EZ6@U0U_vf_Se7F}LWVT%F>b*}+o2lR^oK0`W7EMpBPob#gvSh+duJ#eSpCWJo<=<bEIA51T-kP+g<2bdPM#&|p5U*=OClPr#2kTewHeP=Tf9^>@r*IKOQs6T@wJ2$07lX!G+|^%Rbgs+hkL*~%%5WG)<)m7!(NT(u>z97VtpHhZCLl6hV@`gZF+`BB_pnPGvth!Tcc-g-Cq$3or8r?fq7W6i(~yD)FU|89B5tT2R!sOz;(!giAECZhmpKz^pS{d=cQWeQ@|WAF>}1|=J?F3;V&0m&1iI&sw>jcweXo8RizklF5!CO%grFYS>zdu{Lu=x@&`Vq(3A2FC%!&Zmc6MrZ568i5F2vhSIo+QXdxkKBUBc_V?K#^5dZ@Nw7Fd_AUC(oIlR-~I9_x;R8Rf_m64x$a_7CQK`$H>&?2H2WT-gUnd02+x+S_ZnCZ@-_$pPRk=1zJ*YhN39i3ZpU;=#eDtu!hoX0}YN4S$6;Vyaxo9P*>&_?tcBL1J~^cFte*yv;4iC^#vas@ie?C31BgS}4+eV@X!{_`f85{aslji@@|Em=Bw!g6C(_I7_H3_+J+Hdcn&**@-M+qf$bH=X%ph%B`Cs?y%8%@}M*FBwul?vm7n7N5C^&ec1JbedS(19N8}d8^Ua*F!1Mi^qtiSWL9=jI$DpiEcc!tjA)aC+~Y(dTsyk3;?v5-)Lph2w>u8m=eEu<y7K*X+rzb8tqF{i@^d-b|CF;-m@uK+iwePzZIb>HeXWi(T*V&<MgFMM>|2Htzml4-`+<H?^~<>bis`f+BDTA)>LQMbG4?59mXhnp7}#&i#3Gn?q@lH6LSM&B&!@D+Li#=CwG6*b*CT5oKTN>yq)K1*Z$0k)X?NrKSRO0qmEZ$2!UmP&Y~^Jy1}?aD$9kU<&M>iL}h6?pgV77o_7kU^}NX!rRV@PT_-ZK=3ZBKK`(SXYgJCfWX%oY)#Qm+b4PLM+*xD__r6vW1bN*}I)u8(0lE>M#$k|+=BA-sdCxcJq$@N=CKsP0L+r7gC%jZ<(teCrLw7$D9MbmuM17CLHhq<*CVEJ`CN$GJO&!M8BQUle-fOLE>^#72vPxeOR_S}Q>Aj_w+&8`Cr3QDy@^kfB%Q3-a-T}A<Q~%&B?Z#t8J}+9a$#qzCu*oaWxWjZU&xR(@6$y=1B-}$%VBbGb#74SLc8JxpuV<NO%%U(aT6zWCX0Bfu_?Y{^06vfKj}f@H$JU){iK!~zZx|6Q_uRm8^XPDddrjEALb&YB6p_Nw#VS??@Xmt9W_%2GGB|y_7cn`os9?KxfkIQk8chY;)y3>Gk(a+7&Iu8_=W=F(b0lPag!M3k*27Gghzll6>x%lFRBv3e1-iv7QTg+RW6V97tob6DG-_e-ukIWP<q|xU>*hUN=sdGd%g6^E<CR#^u;f@^f$^qqJ9l!~gTrn2a|iyK#lTJZ<t1a_&DgOM^>WY576gZaOtE021FA47v{s}AsPR1<?0jPMJRJocik&aKjs-|$(@psW^EzO>fWgxJEvL<E3&cRDw*35c1(I)c(s+(CmyIjTLUYY4%{6bEV`ya;p(K1qi`;tQ#59kxcXAg(x(eA%c&t+fIMmm|IsiPa-O0sY3T78&z}&9ye_-rOh%0im#3koHo;%qC027m%gs=~v9D+k^>=~dl*<=xNN-h*xWKV8HgF=kfIxlGIbX#u*;s{nejo?0gM=bHfK%vyl-e!yB!YMyiM+fwfOG=l}zj*iu6x5B(@;f`rpX@AuMX<QZSHSIN0lN;7=cVFk@z;rG++;qkxJ2?0%3B@+HP?j{R|ZQX1t!5d3V|NwnmFOyaGtQqrot|9oR>=X7Ax@Fu>t|XpqE8Zct>sBRQL3N1}ShKr-<+-pZB<IWu4t0<AL^?`yK~*g~Gx0fktCp+YWCS(U*ff8e7NSaUJ{9ZGZ5WI9XvJg7I}U=@+EcLbEkWfUQx&Y>l$P*1&A!V~?u=_gx0>eVpj{0nE?PRSLp7A14zDvUQMs1_%eLpJ;oUL>^wXP8&GeNkM`q1(_{n>=NspsbSzQ9fF3PB=f!WpBG>2`(R^kag4cvD3r`cp_G_wIAG%)f#fP(#XIkku9ad*EyBBh)jPTD0k{Pu%N(yjMG)c_AE%A=42WE!A#!<BtSXyg*~({D_rT;0Ne+PU+Gzu?onm<H=apb&vNSe~;gdIbC!Vt=K8c86P+I__772U^u$2HTh#Qx6s`_EeteYYs<w?~g04yS{LK9wFRrsir7Kv}^@idmfU*efL<{6hiFmR^3`GW&{s*}se$1*mW%rx)9SOT}w#S`aNB${UNytzdHINz8Fp8+$0rgnx*!-ZFl75v={DS>tEn6a@)01wdoHCJz7phb$Dh|X%R!V-yrl@!MdppxP=)-k+e4wZ`tq#I&_N(`$!15!dwnAEjDO0vH|Q-=s01cQaMe11|7eNx}qN&R4_P%j2GQOquJ*`x-%faI1DNnUoGYj={4JOV<|_gdeBO&S{Uq@jp(1nuqXDMTwWL^oyvdINpS+vg^8Z94Q`IATI)M0A!BG4`x5(_fBD#PeyrX*7f-(;+N*%MO)eLAaSWtQamFy@4_VtcS}rS7jW~{ZOj7yAZ8WTg=k_9=+32Iny83*8w2dj&b{Vk&&Q!yg)rabiVU6B5kDQFEVC4#|y9-57Zm8f(RNdK0)QJWlwzC_PCS7UyjDXSXw`TR|_j-5k9W)msnVB2ciZsXo!mrpo?osvRASXyJLPD<HrP2PJhkS_OSeaA9AQ+;=CMD+5w8b>utRH3$(wf@#?`I$TQG4WwHxoJIak_PI&}1zJ{pron``zJ-hzmeO@_|=q~Yq_QGFcr8x<m<|GUax37tJgpS*`Y?+y^&ztsuHUHn|>hlKPuAtR@`D>v1ya6{`=F<=);Ka|>Uj)_X9RVhEUY9d`T@InwPF#IHXbl#m9Ku}AAq`g9(_obV8zO+gL3Q^)ex1P%IbHzm?x%&`g=ASq(Ae<;ENBeVfUSVm?DWd$A#r&v6qk1w#26KqSNXWS!CT5`IeCi6$<v0MJmGTkHwn(2B{-oF$HLd?2>h<_mk20G2{=W7nWszbg_hb|@TV6JQK@H@FJRh9;nGg@Gu2{`RNC2~Fxk8qlBk}D`+>(z(_asJCtiov*Yx-E_I|!6TNr%~sAp)bo}ulbwi_ECL!vNr1&}VtQ6)eU;YpND-B6|5`{P;iX5KV7XK8RQ)m?^u^mqX|SSmcYTlmw3@TUujoGxVJbRoQ1^|>Nv?6=J^s>OKQ94`RhHV8?kvLu<t%9;i%YnrUANoPYA(g9mebg;VOP0aW@PZa&6Na>a~O1A()FJf${V1n=Q8f9BP&CxYzWzq<w)&QwGi@v@<+D+MtbFA7)ER#oa9oecM$zwQ}0S?_xW5A#~-Vw^sSv+1az~~U3(GiHu>ygO3u@RX!@1kcmO<`!fiRh?}=hT#$Ji|^K0H?nKjeisX$`)`aW|lme3vHY{?ObZ0mGpA>Ex^XWBpRZGW2Gb{N;qD65*)Gd<iXCzJk3ZH)rv<^>6D|vZoHwVWE1hyZLe{qp@#t11TxG{Ku{w*cBS}JZBV<OIKnc985q8P5o>xtAOzvD4tJaI*ND!Aw-WVGs?MbGTWb@Im3_kvF-i)h<>bhmG^5y!W4H`qS4uo!Cdklw%OQIaIb=fTkO`ebCj9tR@4)8eZ*_13&1m#K?SV1E80+@Be^yaQ<eqk(jb?XN7cbFGz5w=UR})@0TYOcjTX$m^ydF{Lj=11fPv}a#s4?RM8%RE>mppLvHeE&60NT8T(dM1LzTtb6@TY5_QG<vsC>K^3lq;(Y%AJ-54YmPp5g7H^dwnCu0FCR$QwJcqNuuQ@IU+X^zO~*W;X)k`7qYQW*fmbtbedkRJY^t5ZbV-)c>za`u<RwyvJYrXDo^O|kr07_hX~*^n!(O!EU`!qaNeyM%|l!m)sGZrTo{FRVF)i=mxyp(;=*;|h3lE8nrHOpw=u!?&5vCp08w{=OQBW{mabeVf&C@GK)gDCh5!bW1{f^+b9n6U;@K-a*+g&2ON2q=(^vGCzOV=4P%2Sj+wn8TmF)ah&udHSp0?z){1<Vca)B@x@#PWNEe5GE^jW9Pah$x_Z-t1FBD|>fj#L;_T;F_>v$t15{O83_w{s-=PvX&kg}=ngvx?OFxU$+*qUC*7;E&<CYJr^k9?q#B^!3e6DRPR1c?(ZaDKtT)(F7HMxdK<j#(nq-l6O23&<<Lq+n=*&PPPue$}A(rW}p`wY5sH@t^6f6p6t%^?U9KHTt03e^@SF<2@P}2zyX{mm+G-*4Vni)(#q2!s8QXlrL+8;L+&E)JOlD8G~~Cun2<Y(y!?b7-(uIeLhNG18Gf{EM<SsQ5Z>4!`ZJ3<kIvJ^!B14-rE4ufF+e18*!&E;#u<_fN(ymOtjZU4u_~^vuRnb8@u#ok4_|%#`*;8EXo?d_&;#F&4X@i@%%tnKK$V;W2{~E9fj7DEmsojB*@&>$<_1bFP%tN6WG#r0<BcxzLg^w#)t~9AUwoezk%(g1!y50LSpnw^;(oy>o0xOvwT1%eqM^ZRhUOk@1^|)}^An3L!p{rz9G|%2DD#S=w3lh`NV+*tq6mMDB@#GP8PW)Js;TU$MrVICmi^IL_Qzz=A8XHtl+$LrK0q#S5x9EC;p*rirtp}O$ABC5r5;YYbMeU;k4m^e!%+*(PJe91g`otmv=Y1pAlkYZyh7nDG}~m+EYHNkJSEd|bwPwEI1Q!muq3v@D1&B6pn{j_Gft@Ti<Ykx6IxPy@Q7;$#dswn!c>_XOqE4nqh9Q-h)~8tvD{H8!|MpmfW8q9+?%w{aq)q6nU^e<J7wVU`oqHO4-2b5G-l3{X_ez!6w+1{QbVJVwhW@%X))}b+<9y1WHL)3)Q8@xO%a3WLLr3mf>b~f$bRADl`;((1md3-eSNxDRG?`-<l`)KvER3f{oxZLtRygmhM<q~el4Lb1+Tra><Peuf(2?ph8KNUyd}SIn*Ai(HS=s&(M7&ns6msGUiV~HJ%A?!a&B?JX5LG>btS&9EU;EH+KRAF+nY1m!!$&jTQ3Ca78cZvZtl+v+{%22QAWLLkYKRWg28dGn3fdL0T~)TWKT!Lc=zC`+?Qp@w$W#xjXvXT^cjhYrVW}iV$hr$2F)2UXa)d6a0z77D$!KY8A%nzWIb;X7(`!T#C|~#mlT1x<ju?=;Wa^(HZ|&Iz8*8BcAkwfV)-lMq+a`5s1YocL&t9V12gz(){H3U0;r_VG~Y;K&zD4=uNo=uP8$h0DU6*q+yb$mS14%!2~3*UWDj%`0MAf~saqsq=Yb)4HD@w}%Uc+cCA*od>Sobx`%Jg(#m@sWcO+U*m=`N3l(eTP)EocWHChyfwgZomz3Sg+VRpI|IsFxAl1l>OG!ow{%|0-LK)qX>jp{GC-F6!dMF3iw4zn&Z3K*a?KMh8Nqhbt%(ehU~5Oxe;R8E8t1(L4PM$%Q{ldc|{)VV2c$)w}n1oZbXpPvs9m^8a3(d?GIr?t_hua?-R`rLPCXFOhnO?ffU{Gb`>0?<?l3CxHw(w|cTW7uxHzXBCMcK-->nk{&sXTIYluq}A7a8v9OE3Kbd+MV@z2fV=*z+*$+3_EP4?Xc}0DuFX{?^Uq4;kl`_Sb6v>P(j@ar}i#BwKoKFrQui$XKRo_X@kGU$%{e(`KjX+wbSNor)W&L%1BynE<OQ)^H*$-;&*(vV2)_RIFbg{@1h6yV2hbIR0@w~su6rt<28sQL<C1b;(<IkIEX8es43fBYLDz8cOPr+D|;ZF$~J^M+YlbKP-g|=lJwxN!qrpI6>4R+?y5)f<}l@01)ZoMCRM+~-$W^|N|b^_*0?nDa+);75{wL=9^<|}Fz8GQk=aircf3hco>!V;g%uS(2&hHEiu!4Q8^_KqiMLAUm{s~-T9LAwCXKZXK@9u|W8f!!eTxOC=!c37P1Db0*JM;s4CMk3Iv1D^B8anO+>)Q~H4W={4p3ycc+f$2wwxfOMFRpd5Mb}l&M^l*5IE$Dqp%j*h~y#h;Z9g|5Ke3vw5QI{dv<>XYNIQDMB${bZ}Ga)9Eso*x<ft!;sO$@2<&2&9^kc5lEt81;xm+Fp*IWi4#0ufn>s(eepJGDfR}4Bef2JQVE+8Pk(VhDURmfIjKo^SFc*73LR=#8ntX-`f>w8ZDHv6K`EE?Ob&Og#?-(moXjSp{298cq;28N6>4AeMnA^ERjTSR6R?Ljx{H(Y%`PGpWgpTbK)4P}Gs;owI3%op{)0jYsU;=+#SwfHCzgPbCXv(RP;n6)tL01BTWD5wahd=F2^h<~e*Jw5DrV3#4<NOq1IOiACuM?+XGI*;SA4aZ6gy-Fe@DR5m0*&s0_Fy3!b|(IL(m>`M!7EFkuFRD#!+0K^&Spy>tNeI!4&On_q?s?{(2}f$KvjblpUxPk>P+ud=Up`&y&oYp?F^K^d9lg`;bVqEGwR~csI^Nh{>a$~i#T3@QoXIQFEA;FsUK$dTt7SvXfu1k!s_>ku2kec@!)m?<g{6GwwoD)=9W!=1=={Q=9{<BXNb0^<JF44!DJC)sB6Qov^%$*w3&Vpq*G|NH~INyicrwA&mSX39Frfv&e-^M^5fS4X?pHT{X-MmfL|X~M^)PDJObUN<vX2;hz#K)GGsR*1D1O&UhZW%qi4juz3vx1fr?FA0HD@=m>C1j?QETwBXl=Qt5^LcaEmzcu&T5Rs{$2)CKO8-B4k>TmjjACV-UC^3DAi*#Yh0m%~xucZtbP`wLM4|<f0z5ZevBVl@l-8kVsfZ@v#9%@5aW{2Iy2XBs0u;;P+;kn^FxYZlKd9??D54R)o)^3Ofexwix`Y=I*b6%aPK$ohTVUKnYL)B8a5^oZ6p^AJCv9d=HpmpNeEI4<=g!J45H*0y_Lo&z7dY0{x+cS6T@^7>WG0kLMGzr1cJq1E6AH29Pg{29}gf*5E>hM7OuYp65{l<A!z@fe$|y%9|`dcqr8Fsnk9eW!cXbKLM<Jw$L6psXwnM%RZ-{_^TN*ks5%yH4S3+n0z*McauGOKmZVf$idx%1%&V^0b5n2hX5z0uCA@@RQMP>`SjEoNl%SXz@9l?8ht6EE%qL;@2p50TX+V4#FVA`ks8!TD1p{g3CN7<dFpkv1vYqkUWx$zo;mTSfuP{)hdR-3MpSg!X*%c(z(Ln;PUw$6{>P917b!}cjQ')))
