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
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rk<ThAQFas4lR=0o2vd6Ol^7Q%!EMMrQ9!7z}A00DBffdqm7dt_Ud_A*s<PW8<0ejoSAHq7D-cY1oN>)d|xe{cTfcmMX!|NZ7~>f1NJ|J{H8>-YcdH^2G6H~;g$-~VTMTfTey=HLJ0`~UjpmtTMRcfb1Oo40Si`Ng|;-~VU){{Q)xfB(aOz4@E?_RW9(;dlT1U%&ge-+%u<{`hvQ`281OzT2uzQf)e|{fAHA*Z%#x_aFY@&5xDUuKf0kPwzhdRMDi0XkBaAl^55VQbn+?6{B5xaj_`;iW#_Cu}d$nCj9bg<7(gj;@uaYPD;C7dU-YBw~zMKQm{)eu9hx-{O{g!uY$Oo^N+<p`_<R)zxwSjzxd|UuRgx}>B_~f6knn$J;UT&*javwrc@EV3p>kik+iTAaJ6EWf(tutTn${<QMuZnmfDvez6BOqJ}KoETHe^LFRoebeg4ZYPA}Dg55r&oeSi5u|Ge&uJ@=>LzkT=aD`3mb!tF)iZ9Tt4%+imS%@tDZ(#sXnq$O-$ZP=xkSDVs$tZysZ1(YAJxLJI$u<~|kv={S~UORI!N8#fT&Pz9c++>$t{<v8xaW9;}FP!LKIMK6kiv0j1u|;58AX1v8x5K>OW>*RePHcUW`AmXcdihME^cWMrL=*eL49ZupOC@1#eK~qE`730ul+)s`K7RNm@Okz2Vhal-0;S1*>QZU3pT1Pu>{S46P~Uy`r|KV$ut`6{e)-}3`*&Y{`t9Go`}pbW_h0|h=_(8OA@-#F?VR>jmZ2NSZ2MB!rP=rwp)tMOd9O6sZc*Om3fYcDxuV+L??uI6o5V!SLw@*~PgYUN(r%Z*m7JGXa+Pi&i4U*X&rZANYClM=yaVOuYb~z7?!Z#IxM*Mb62-Z+tdg>A)<d_=^G)ceT~fLpf9&FCBGS&~m~2GPc;csz<}beZ_>b?tfd&)yXmHTuvpDIt^J-xpvEM;ULOC1H-5PLh{FM3MyFJE|P`dZaA*}E*QJyc|=P=vs&p&+l=H2Nw3k*)Kf6-(Y{pCFQ<%hGqFhc{LKX2(*HyR5)z3TLYj2^<Jz_xwz$Q}LqH~JeCR#u37wq6>@5bvq6ss=Ru5mwc-i?Jsj#Z{$&EaHY*X$Y><INIc~u*d^i*)F+W3kApAF8A!p-y$%0#uh<xECOYWI`~m&;HO%NpK29;ss)Td;4L8l%V2T`0JQsBKS*Wv994m{CW1pn&-~QUzD54Mj`T-7(jRf<-3;{mA6L6PpcQfq5Qt^S!-tVa^s;-#n|KfaBQt2fYC7uWenopc!VVbxZlZu5x1E$Acv`cc^7Ymi?IH;@Ob~Xv3Ht&I^5Qiwb_F(MR>so&0CUJ=6P5s{Y#{(9b@gB;J;qP;P`=RMLR;aYL>m2Yzy@LU91Qdli^phdB))*=%ZoreA_LQ1X%A@-m1lDg>2@jBf@QhQ)7tg6d%K?Z`=}Ueq_Mx<JcKm}AK)BJ2Cd&8IA;FMr;lHJ`?Gf+KmOVtuq*eO`0hxa$v;jvf8M*yg^efJ4JWyW1pgkg#k<&A2si2N&wu0n&gs&tK6scV@JIV(mt4QMnLQCB-xsW9kQ=8I*-41}X3OW?yoT8BMN@HnA?Wdri|eK>n?{d!COu6D_OFX&lkAF%Yvkv|o&#npKM?LmwFawSl*c)LT)=p7=}edCGhL=nojgX{a4IMA6qgtnVU2zjXhKC$4|{<gt7LktQs_}cUq3dlF}vd3m|b@w#Cmy*_DH|)$n!}&UnH(+(}?y1{G{xuYFniHq{F@<Vd3lu;5pLS5u^KWo*e-?n%*OxPK)#XNmxH@YT3^npY*pp&|l_6PyGsg1g!kmJ5#c~Yg#cO+q)74r0rsPB+%H;YiG~IlRXk6Z3U(q<r@(Nb*eP#)Yx-i9PByJ!48Y7^xm|S0t;<sf!0(Vut)j>v?dD}tH-vwc5LhPzc=mw!3BS-LQnB%?u=uAqc!kTZ{V+5zWwwVx1Azu53n#@$occ5EejfZWT0{0Nw*P^ZX*)VAZmM9WgE;0Pz$hgbMkOvc05~Ly-{uLJkk%HYJnhn1+c8MXP!1orSnMJE^QlD3Y#;lWY?=*Z`$)fbI>t!_@C;O9;!{0iqb>1iBicfz1RaXa4~7&7HJ9C3%A>)(!X&?t4KTk6zl9nBck&0r?ID*vD0};Im^Vo&P!-VE|W9Bmb~$3-&j590DT{X#a?}n(gBVXr~)?f3fRE2bOKMoU6NUV&)&tc;Stpiel>;Nw#y&QB2{GQg3T`1@Z6s&26(|~m#fS0v;;%Xq>tV}ZF5dbz!`hB>(w=VS`x5J4!d4$y-y#$?ZO!CQWcR*$ILXYHrBp22N`supBEbavNQ*&^c-aFr6KZci38jc#aF37jQF1_CV0VNmutZHX$7_=N)7!~_QWKWfO}%G>s7Gww8VouZr7_H?b8x$PfWqCSLIddn9;U@a0}Z&2Q*1yHxSv!+HG$$>4|o<1y2~~tk9gZMsv=FbQ}l2zCk)BgPgU~BW_rFg&Rs>OQ!x{kyUc{HwOD~R(9CicN-_u6zIYWBnp4@%KXu*$~1*6&tn|&7Jc3&tdB$tv95Rvzy$1keH3=c225!cO4D|M;@g)XHg)3X1rB%awoFDs=oEnkGSVX0q8a`@$|&1-XT}QGXGiKzSwPT^qV6b2ao-P(=80e0gu6Z`+y_j!X;rxgqTQ7rH0dLJSew+#d*P14!>hqhJ)CiB5v9XpfW(OtJf_W3Nbq=i1~HGSGCmx6e7Jeo=R%`}4j^5PXy+TzXf<(7e%GU2q3wCkAuU5VJ5v95c2fV-&T`;U{V;G6ql4|o?kfKCJ0C)$eb&QXE>wk2dQiw(jV6TkMGD$jH53F)%hKA1U!&gdHm*2-T^!Si@(9xjB&VaX->gZ0vVv5RILoQ+QZb)R!ibyv!WFwh6AWy(W*P%C0rNQtWU2lhu6la7OpDGlEjrJ%=sfYF^T><NgGY2uo7g0r>#~#J==hOBUQ;ut(|;Y3!;?2l)s=Bt(#)%6yHp*!o|beBNNRSyy2A3w)94OcgY9~Cg`SoS2OoL6Ufrv*Fu1sCmkEjU-+%r7?+_y`Z0JhM>X2|Ak1Q(fsj@5d+^#;P{jR8)(-`qUGlXIY5V^0>?7YE~>jF=XOFXZk@Z^L>liK2>L3o*AvN&Q{HufNg^TGe^4E(n<_`jWj|8|Cr51ATww_OT;Hp9j@?DA^UE(O1s;qBxa`|VQrW66`3*SLMy1~qxY@kG&bjNDdeavH)Bh6z_u>tV`~N~mksrm&YAbD)9QMJ2t~9ZlY&Gs?%X%yX%P<3HaqC^R-<-oV?tY1AfOeqWa+{IpwPoGi5<g*DS&c}^J}!q-J#fVj~LT#`kFuTkV%fw<8MTwX2PrC=)%{jEUcTY>0r1tQ-HM1Ly~iB{lq_dcK_e&sWMWx+0SqELZUG-0KclecIytSs7fa#&fii!~#j?Fx;klQ(}A4J^z0?|A(|>2|d?V8}}e#k^Map_#e$v6#6Ewv14D$9{O1$IA$!kpM6mF7;l)y&4E+ui;(^qH&yyS7>K}41grGZ)s)w*3P!AV+~!8bO>3D2W7WvJ{J%fq8>uH(0)8e<lXuibU(W1lK)0p%Z*JdW`xi<G}15&pJb0th>tVpxUIDz2D;#6=Nr3mVAHR<l3NV4_gfwM0J>SJL7zk?eBIrPFs^>XG1+zUks{m08tS-Rp}he4CK<~Rxi+P>k&nEedw|PG4)&X7g-x)}38BAolaq%bqg`UOFNsos=N*yKu!58tImeXUh}5g!3Yje+uSFb0bO-^1h%h``N8Icq+cp;T$2<Sj4&LbF^fm|iQ<ROVruqJFmuv6;>C>7HqmS)+6<9od-0nGX;^)N4KPOHe$av8?U{Pbshpj41)WJ*a15ZUwJQa1%bbE(bJMv=f$cNqB7d9>QLMn$zp289!8duIJvXy`VBQ$BdL|}w&7i)O`c7=xeUI1Nx`ptHa=@Hjcwky_29^JkOL<GYGP0{8FKus`4F(~%V4xzu8Q^vYa_EyRD*$>!DA&0-^ZTKmjT7i#HY-b(;CSjUlg;XrNX=c`yOrsS$+{h*iGo{EvS!oeGlLb>};4%7AZO`kJmkNWrlYIoP2*`zi_l@NT(4D}f8-V~+z?dwi`f)Ivs?Cr7@$L}Ta>LsG{3sZbOz!{&#4sZtnJ+hXyxeIK+T4wA7ta0}*XtwmB!7{1&!a_!Cj6Eqv3j5f`eA9H?|V;_Ru{0-MBQ{YHEn-pVxDq*<_h6$KVvY(d@L;*Jn)IYbc!h-#*+fAQ9H~#LD7I@S_4vP4M?XoAd{DXL|y`tc?n46B_N&G+s!>y`iZ8aWBZDnPmwsIWN7pY<!3qAI|*c{y+DAtfbDOlrP-aPz{f!I*dwoklN+0XP1P|S;h^;fvI3whD<irk5wdKcd*GnBU=6bKrW2P2>3~h2HkF2mt#b{`&<vZ!jc3hRFVj9UjTWj6Tc}14uW4_X%zMLRl~VyYcuW7Px|{iT;&Yc2WKupx1%C3ZJR=|^0Cg$^w~n-Q5Xx%~II*sQ<+0PE$U*xpPulJ+(wT0M9W4r$r8Un6)pxNk7|G0A0K^&C?+Qt{&$JUvqK8I_9vUfBZQ6-C0d#Pq72_G<SF4`TWIB-Q1PaEX55nY`Dv@WZWIl<Y@_LNUr&i9#nJVt73lvp-iG^h|3(FQ(q}SHk+r8pCnoDJM8>i?OD++`mfW6LM+SdT$JYb0M`F#PXEJ}|<AmqFPAr}_lZ7hV`S%7yg;=6$+qXCF8fyE_{1y<vIteSFE9e!i4N#Ek-yz3zlWSJYpL(YwboB;%RV?j;c{M6z31|Z1B=p$3Mbd|rwMkCgPMy%%=VvXR>m|1$*Ve}6j8(E|_v0!j!an^cJ?iLv)nAtFb408OoE3V(JxHv6Z4|R-fVg7+wx|&GXiqx@#=H!r=jn}ft4LyxUS3W$ps_Mq>Hk?Pi>R~7wMJLls67`*mySDnnKx@Ke7q-EF&j-&<9Lh>+em~XD-{PQwTG@itfw~4i>KZ(#t0KItv~sf3%Ew9T3FVbKc^2*DJI{#9KnH)HlQ-mzh<m*wb}zD_4sp%8C1`W;n`D0_%8ed71{~=Nag%{<u{xl<A2bF9e&zive&&8j3O918S|h3^M*{9jNSGr5moQqUWSEa@IJ%e<owPo%(Q?dgv&OCQ5hlb8yD?`HpQ@BpvJF6gf!fVQ=F9`5c!@#rlt~Q&lGQbktkXKi$;%icFJsKMjB)E=S9gm$X*3tH(RkQHsUI1OS`5p|3=pPhjPC`09VCa;P^e^=TyMzPpR-o@Tdcg|Qsk+Z19gy*L9vug7(taP3wyOS*b6|hgeSfqlBG!~ll{P95-%TdhK<JO@@QU;i(K{9{Og6k{qW)a*(DtooAm(K{K6S2%Q(}dC4+%x(<T}!%KM!UGv7$_d3${3dQcZ=q`7v7A*fHu<cpR}0;t}lHOOwzRHiKx75oPPny%iXiJKN~4#@XIsS-c?PoCL-LTCS#zt1M?;u=3A+ScN294UE`As<YHfQ!c5RL@S@d<L1n&%#SVyIn$%<iO?Sz=^`+yKv$Y%uG)(vulEx`3Yu1^KCKz&T5wsjhB0Z8TkojSkwLyU0dJ)bL<wOxhi-jN5lttO?*&TM*1RYzO$V9K}&h1zVTGLX_BKc9j~xCb$!!_yixq64q$s5M#JXwO8VS6ywz6p?tKMpAGAU+JPx3`6aqv8svaY&$ee^v*&~(Yy(NvtE%w8_FqV$&L5VQC(E+geTwbTn?nYCQ+3JZ7ZI-{&J7`${^po#yx184y{6t%@C5Hu@X?Ao7*w2SLUw5Oy@9-RXVnN#N>#tfw$g}z2b&@XVq-vWkVKyib%R-*{zgRv2ZPpC47ZC;RU`4vLTXCe_iX$J~Bnx@r_@Hf6|N6~(d=YE5aePt_NaOf2Q()Ky=p<Lc{-a$1PxLaK`3x&^iw)FbfKsG8q+`+lV>PTa`mejMEm$9;jDg`ZHBLLKSPS1Rz%Ipy_#&fcgX5i$wV+y;__REh_!P=-E|@V1DD508XVXYi3JOhIs5I738>PyddFInp?vtdsH2p>SmyKqX4nBV}cp@^RKO&P??8>BEnsv}|e1?n2<W<F&blz7kja7i_=yAu5es|o+yW`5;MdvlO-J_|+B2Z=6yYs?Y)$2wU*EU`g`8kVSUFOsS75MA2Y(^ie-RFEgQKE?kJ^;h}LEoQ)_z)dt+%iek9rKs@n7_zp^#uk3hAb%MQ<KVs!D9D76CT8GF|kUmLnsLHjDY7X0Jb8gnFi)YBK+8icNtyHors2@Y|`eY(5e4GH>tD}7eXc&R2F#dYrykhf#<nMXNWX`BGHP0Y_DemRC8-qZ05@q2ja2u=1hAotI-0(oh&d9i99!lw3w<o@5ZzY#?5u!wtCn-13Z-q+WUm{3_1cQAh^=#5Ex|XoCorHgGZaA1+~IRcUUxV&NS3pX{fi+#>43rVr=a5p8asvQWWh28V_sKvty!Yk2M~S#+BMJGVBL{Zj%MwX4W>~*7n1OoA7v$6x*l&@V)$p;q<{{4~_MOTM$EP^^E09ASf=K%Y>XHAKDP@CGhvtB32D4+2b9Q?1~9frA?SR?ZGs8FC~C!Y1r577oj3|@Nuv#+QaOVZ=q3t;5gW}0)}3%r0LGq*cC;6I#4`lXm?pM<vHI(%32O(TLW6hZsO{s!jjo8BD2MlCrK`PMvNMo$=eafqZ;%IdqpANwz4wss|N+VC8VE55K$RxOpdV*hE--yxI^)WJ5>G_`50)V1w!-IJb|(DzWNwiX(h2W(rK!h7S1ll?8fTIR*ijMWH3Im5_RJ<QfPf>b(ul)s?x#hA;WHvVDbd7Cx7sI;)B=YTJXAYj-dQu<bgxL&Jj0Kl;+3EnFV=Ind3d7IOC*qVgsEM8yANh*=~Fcx(EpzBOQX}zcAT`Fr~Hr4l~NWgQQk&S&o2bA+KQ>&+QI{?AXg4TUW?N8VF9iA+ov&clDcaH~tnotKv@L8rOy*4=BB*@mq+iplWsdUU;o)0VLafR?Y_mbM;QN^1IUh+-;3MfM|5#<}Iv^c5Y;M4CZgKht|xVi;F{1+gOBmNrD?#09rQ7VL7_0ySuEd*fX%^$F*_VdNu1r&}ay<ovjf4%zO$F7TC0Oy9&*U%`|wKJz9oglqEhBC);=|5pXm3fSX}V)yHn;-vd4T-c@{CXed_EJ`P&@D1ZJZ{|$FQv4eMT?tD(?A-q9g4=kJU0QlZC8~|;B4V57vSlXMWZ*Q9X-ZXuC)8zN2>D!wozc)=?zK|jfbIbhjr<3@uPU6vnTn8S0R?K%C>Xz5%?R~oaR?6TTO<mrGG%aie0z!vv+eh??jd$yA9>1073qhn2<Zk>7gLhj2dPHC!-boaj*20++8_t~gaOS+Aaa9JcC>J>{GK-T(=2{l1!j%?n%N(NY!3lXsxYfoORje!;MpoLmsME$p)0NYM_z=P8Cx=?A`qWyLS8HWZt@VQF7*AvH7hw#(wXzFOPN_b#?#>J9hvSonb-x}__yr<&xF?|w(r(uvW(JrRB=B8m@>n2dzXf99Z?W<nZ}(Ur4!;GWBZ4v5O}Qaid_)~Q6zcro8RRf;X*X3o<YVq=k%CXq9(WeSdbsWGn)b|S+8rU5$1@}%&33T7#T^Ruw1z84%}Sst47}i+mzLZ^q`I4D_{9yg^771Txf`qHevE;O&xR~5n2N3Hz%Txd)uGCkr{-yG*g_aQHCPO|O;FH<F583yoiPKNLD9mU7*`}=F|Ez<<y@TXNOpi6od)e1HEpVcaZG&ulJLMgDr=*+?y(vleyj0G-=drdJ+yrQaAwd6rqDZ`mfq>i^73P&m74u1CjY98Tci{MqC3=zTGq@#nV9mEi;Kd*;t>WOMB~MUg{<+Qym)+K>qy!;RBdk3ZRl9fAA>fCy0k$wT>JAw@u|gST(gbDUVRwk;t4c$KPpUeILjutvut81G?~W(vWIn({eBVI;|cEai%1^72#1Y*^qg0wwnI0Y;)k9irg{boHv8DHGuz9bN!h&S&fCwU=PL&?Tcf~VCn~m=SE)N3vZKSoJ0`b>x4fUxX~~v}cjM*o-PW2@kp@egMU@46BUO7jK-CU~6e1$^#;VK*D>9#pqn1FcY&^o3vYUdX;qyXd43q*pYD$Z$eoU?oVo3<3c?4*xPeOS$eLX;~uILW$nE;JR)pbSuK?%^wht@hY>&f8tiJ4{^-Wn;q74cV472?O(h|3slclnM_UL_trR~K<(`0R+No@=pAcf(v?VNSD7dFO+dI~}|{4x*cTjOq7Ca}fCxdkN7y?Wwya*+e~cGw-RJc->{>O`ayN_L&|=;>5K+50b2Gi62*F4GMTWY4BFIb=fr^xqV*l+@^#)+Wtik=@f9f_Dmr-W-w5BgMrR74kqnMAV1yvYOE7&;;GtiPrv(i;4zMPkj&bYsAB5u=86TD+xCR5$Cu_HRXuP5&(A2Xtl&l??7X6T-cy=A_^xZ<F5L%20fV+*g$rpy`6!*$RUZ-s4ElR#Xm01=`Q~Hf&br3B`SP#_FRh-eZ=g(XcOF!qzT}4Z^WIi2Phawv<x9TQVl+>WeTYET%I1WGuG44I5_gox5(;fhvRWN_(AYgwrRf-XNwBM%um57OR);e1w!YwSX4PI6;ac9N0}V~~AP@$xl3LV!E+>PRTDSnzbSQwT;7EsrFk>?})t-C$-MIsgyG9;f&mPzM;&-jD{4LVy&GKNS(1Vq7Pid^ILoKY*wX)~a&K`ls+Ie=;veih-PSfI%IeTQQ#{k2w%;QXkm+LCo$4V@JN^^CiA)Zg4m-zI;&zC%GnR{ryiUs%;yUFkHga$&Xt8GDUxtl`9<->*}O?OiW#grRw{YsffKMN0IHXg<tv<mwEdSO+D^Dq)ZR)w!doTWfVjKy0BlV7jBcU(h|O=1G5l#{J|0*@dEk5`F3Ngn(yPKPs!CbfwWPYO&muI^CdLvUYoi&K@=P%z_pi(P1ck;>!CUD{<HS_rDj>k(D?ZG@m0j{^~P$tH*>1P(YdeD(Fu&5b;s^P#t1!fsb$oTccAv5Wo~yXc9rb4<OWf9e(ash20Kv7%oA=rR}0_tP)>j(*WNyk2;C-STkerR5%BbX}a;O$W^-1$MNUXxBYV>I{yIkwEQ3BD+0Yzq|s(S8QO7e1*q71H3&!7`N^-(~{So=JGupHso=-eaKUwZ&8bmsfcXp0B33__4q{r|7ak1In3KSdeqa2SJ>3g%j|GJlE9j)HBA}N568GowL=0OJ^JFjs4p(820@;Ov3O=!#4{B!hD=;cy!Fg(N^6Dbg-EkAE1a&ZG<!#-b;kT=5b6SCekqE%vjh-2S`8(ZCCT2A&-`sFO?&cwLeKo|1M;^OPH_UHPZX6_>1eVIU!%q<r%1Gpj&5VhxV;Z8&X(tG$RN<bpRl7yG@HnEuyb8SZT<~)`vVI{d3V|uVz{Eb<zVi@n?q!rE`ixl6knEi<J~K|FUxz<{uL>_%2001y;JoR?ru-vLEoQ4{S`fy!pUzbocUWUK1<=o%k8^IZa-<=ye8u+t}WcaVYmN=wEQ<@=igB5Id*V#v5Ep6Ne3so*oML|OWH0yj<EUT2s?j^!<P{rXn}o-_LpSqO4*~!FZb8wXP7)f9?of9K9pnua{kMr%s!LhR*Drs^BB(cMgM@YR}8t5I2U(F-`X#xF0&%a<$QAzOHrJ|hJDn8Ni~{zSmKSC3T?zBOS<}sd6>Do`#iuNo!}A|93AlOJUWSDg*LY;XpaPj6UedVb{ldG$A$2=$~-gK$_yC1RmFTHABe>7$<S1DIC8|NKStb<bnbC5*x4S`VdXFwD~AIN78DxPWAH4F&jVN7tsHg-yXApfcJY}PivuKG!k9jKV#FJ7S=mr7B4>aa`Q|4b?whZiQFlrvU$lL&{CyxVhRKuCMIL*GxPA_y_?|J$r$uMd1H}9dq9kE7j<9Rsvo@KjkH!5s-eq428d@NJyfjlqjXevwP_#uxd*A(i(uIQ2E;@VRUuJxI1;cmIAgRKu_jtXdEOlFtlDe_i{)5`1YX$+yHV81C^)O$7%BQRM-P*>N7GVw_ftAY?UP77x4+QZmGU#k|KB$h?EI%s!;kEnagA>JoPjI%2&fD~67eHVw=F1Pb9GK&LEK*b%L<V{{YmSWeTU#tG%jsn@^<XuGP^|L#rW0uH^<l~J&-m=m&NTry!HFR8ofqYZr!<FlsPZy4Bt9|o@}^?Tn^2`uSx_3e0`f3_QEtZcj2AHQ&FM*P5B}8l$Rn_chf<3tn4tQD37!e@pJzfm3bS|C1!2-A2w~9#A@Yi_%uBl*8m;aMi$IJFK<z>U?M0x|etrdx2cLDUeAyAezg5V*0%$sz3Dp-CKX^Zf=}2!#03UN}=#gj|=aos<1HkyGO7ji@4vj|z8p=21;t|qr2@V={rTS7tI`3gJXrgZlGy_>)?FF0Hv%-q(&`Ini#(;zs-C^W#h|K~FYL6oh;b=hMdV1<J$^J%3_F&gO(c>+as5)s^1<gO~^|~Fv-@?pGP!x-VL);Ez=2J>6^-0@0d@&PcQ#52vufc4xeuO-UaLG!({D;KnKSXW8%QB_uIZkM7jrB15r9SEN2qCyxFm1#I8QVqY$b7L2$XMElve35aehc(Mcmm9Jabbrp4(nC3E5yFi<i18*2n^l|An-c-<go(Cek*|el4w<bsyNmJXGo}wfeIdkX=4^KQ9HeMcYeU2?{C_$FRbx|eK3<9T41U+F_}m6WDg8~_Q0g)L&ylm^tZ?>!h2<iR~;#=&7H#9rOM*q6BY;{Tl2xleB+_WDasM%7r2@D_7DoT>&IgQ&&e3+8DjAav7iP16=!g4H**Rdce{Y}PO7|jl1g_?fMM0SFeusuk|u$7xzb!H7aa)lN&rR&UluSHVYpKfcp3uYSwL8nb(HgtdI>bU==>!EM!`@_-_jIWHB~^o#uWA4A%+TymKAYe_&g02l#b6qbchc6fjk54{9&c@=EFz^#o%vo+7R>BVI}g&bUHlk;vu~e;*!h3gGT*X`5lEPxL2Cs-f4pSSR8YRvz6vyAZbP-E>1>!S}MF8ONB(*k}R4iIHm^CAmR?%UgQ|Dh!3y0otuIXDqHP8&m}waSt7h^11RB+9-Vnw(N<<!G~Q^@c&EbwCru*{i!e%bk?Jw_x{(+W*Lc<0_QJ4$LC8U)*(4#{!%Fepm^QI!Ygdi5U589BcR6Wf-bo{=Jdn;ib^wG9s?l<gI&S6Gp}Oq=Y9Ry6JIb#kn!{NIKTtfTpTQu{U=YTk&m~CKzPa0+7|^0?M-mK1Q?9TZ^>z&c+(P#^c*Cw>mzW<&)W)~iMd!2aY8OD7VJt+hdt8Qr5GOLxd3qSxKAR8WPy}%6kv(%SR{r^#00P7yWfG<U$hHCiTCx+M9v+iCc7A*NFV`V@DCUEBVJH!!xe~1=?}rs^?<kW3j#*9>+H64P!Uo<TH?W{0c8lxQ{97f2MecMQ8C1ig>G3;?2YX?C^XcOk-~Q~~$B)0J9kK9%yvOb8oVpaA@g&c9l4m^0^@jG>U-0{b)5i~=xXsXKL4)W(?`Jxr0LO?+O=C@9#t}9%u*b#ru<E?KOLhS?7{Cl_iZpV{B=jr8kJ4-5NwI(B7BGMP%D?;h&(A*ZFUtN!v2TeqLFq8V7ww%bzL=QCn`U(0G-IwO$?fmLa{kl+!jM8~0Bu{^8p)`;0$3)k6N!Om@MMpRX7RgdR{j>7O)@gnLwmA@GUp|~U23#fTO}p{9O-o3yAh6-;&_#=4ABt{nhg{@!lOvjlx~pY;z>qwB(o=6bIN(o^Ru=D$kk0y8WNF%Ryn*&XOqV6+5Ypw4_Ro79>8$t?B0g`=Q)XnV(lZlg_Gx=;Xn5b{@gSCBYuZLr@~%}j;x=w7*%?c6dv?gq#DEUxz(Na|C#qqx=!kKGVc^wSv#Xk`L%Eg_bi7&KU&pAYB*e^4hmW#`tr#)*A8-6P}kAq&3gd9A7f|A50v1;vyKWFqXPOd#!6qNAK^H7{mk+~$=N8ir#Q@0I<4@Wj<jt=e+o&5FbyhTbYrqom;7ob0AR$yJ0Jo?22(NzaV$U@gFM6%>@!fuZaCwm(=Ih*F?%=g+LPpo>&^bO(8AwhwH?4rXJN=VOrB{)-fJv+(oZAjS%BSQeul(6Lt<WXNX%^m{1y{m@(R@%MWQQhvoZJvB6>Xe67I=&)pcb49*gamVWNAO(MGrV%S0~AKtCzlGbwYT3XQTzecL11dNdAvl(F*0qS)gIBM(QgiiSidPr^jT6DF?S+``{uwb61aFQV~z5wuxh(0)MK{loqNcQr$J-OeF=7K`P#8F&K_ac)+;f-mJ%D3i<!q~eY{*@k$sHZ+^&XqOO_aSf5LPYaMeEI@7_^-|O;R*8$4Aig8yZZJIt%*)Ao+vgD`%VFC9!#Yr}WW!ATI)^CH2qmN@Dogedk{HTPbe4sNbvM6+t@F1ycok%D2sP!&Z}b{>PIL%%5FD=A=<WxG%gWI0KaVIwA=v$>tR96rvRyz1h-<k(#RJ$kk5M9!2dOASw+kR;D8wj`k>KueW7~~VfV$L7Iz(vl`HYj#y^lV(naI1%sF*!MC~$aSf{Q4q0jB90AawHpAyB{<arcOOMF=IZbw?}%Q&?m8Vhq*IE<U<ceW!mz-ixYHT~S24d81TgbRT#l`p8EZW!|`@vb<1;Nea(gKx_9D+}`epi=L{x*ui*DrC(*6<$>o`08@(r)Qa<0KuGB_G1Ht@ce9TykWK3WmI>GQI9Oe>Je|qlbjDUDYaFGQlR~6zK9e6~M@L4O%uiaFv}e*XSSDl2Ccz+MtJ5l`$;zveM_!fUnpjFF9X-R4o?%F9VMt)}RXx!z_lrXU=c>&U?$QwBlGl`o6dh;;&n+LQmniDVm~e|llt49512c>X)jTmuL@E->Mqi9YGOQd?0(*W1(MUJ8H-VCoWRBNC_9j}W1!RcwNcJXi&8K83EcWXC-7_t=`O;#a<|qukDR?57qCbKu@wb?L5lpYh9R;SeKbcY5Nq5+DIL$}ofRUP(my8U!<a3QU_~@QQg-OrR0zF5I2rp{U^J8P5$h3b)q3!xQZFDhtW)nb$f{!56@7^)j+&c^{2G2Y=K9onF32oP$@jsgV=efzQ!c-bI3&tGnU<MhP_9#I34upZ9%0-Yn)xMJ--zj2ia`AoM8iQhr6`NOeNXQf1Kb{srOtI4fk}0OeNfnPTNwcX$rd=^+XEJS@5h@#M^0cpKOwlu@$fgHvA?rUJMo#+V6j&z}P15^}AHrQ%kN_em0Hy)UD)BU%Ovg>~#GJNB%;^r%h$FQ@an`0S;1Tc8!g_~R);qKVJ}t5ucQ3P1EZ$gQ1>{9mfGgpx`tpi9Z^$y}yy773&E0XL<`XDynI1eGf~LZs-;3w`Ui|0x!k^y@54~^Mm*Q|>Vd20EhH*YpRu=XN8m_1<d2@_Bt1G;u&@6qCEv04!#sLj;bV@JG(dk}sO_xvgRpd2YE!AgW(_@6z-J9@~VZG7{KGDHB2B=4fgdX8)<@17snCRnUp^uMs@%Y&6<Kr!S4b(Lp_UovgW>YW9Y>GmH8jA$!9#v(*qpI@v*c@z~IB9S8=wRrjL|^83!>HrQQHzFA784k<nVLL@D0xDlG9Chj8nS8kSZ$t@#u|ZKrtVLR(sHJBIy`o{{3tA}jM%s#?oo|(kLv79c6#!kcAMkE`A><}lgC19*6U)%RNHZy3xgH91NhZj#k-WJxNGKtLgPv{@k^H->oHN6zr}7jQOyyU-W-AHyOA7?-cG;bw;w*dKfmIVgt&V|%gZ6_Y^*zWfVw^F?bI>K8a%ATJ0<-(lTT3!G}}vNs&~GTiyKrvw2_N^IFw@CBijQxqH6~>wgyv;$WzO<BZ_!*8L*`ZWG4ogO`TIGf?a?Ozc6R3<Z-rgSX4DnwpRD}S^=xj#9X#t5lUWk@8l~Mzfc22C!QaAwJ7%l5Ot_B^A=KtM%rZDF?w*vxPUuG9(M$K@yOdYCs!QLUA?iQ)!%oTL)YOqNRJfL-ykegEc!CV_KVx-c!mra3DWp`?7Z|l*d>I2t>0&1dVCh{VTpBqvT^ueMf+=0mZmaBHk(YbD{Kx~1Z8y)b8s~Q4j7OUab)|9NRRp&B<I&4S(BTg-~8B1xTi_nqFq9GholAXki>osEZg+Pdy;qB@cVK;bIy?p&(ym^Q}5DRbRC>HNl*rNjCe!r9TThb&TD~kl@(+6H5SsK`9yMOn|a4eWwVXIuI`#XUnDorC!eJ`oOt>Xl$P@*DtL@|;v#b<@kTt=W5m<!Q7s`Ubxn91YA<|<1J5&+j7%ki*%d&}7%V$->g-|g03%jpi&&Ad?=hlXt1Rt-_I@2}1O~tlpCG0qz-sfPdJS6n8{CJ<{3zjBgVvcDaa#_pS@7j;CEoHS-#a)fuB2a?T!2UPquF?JmG+6@vHao4z?yuFQ}jerIqYj(aZ#0LCiEQ>rgmclyS;00R*2#$({0NZoE1{m;-6qwqscFe-~q`MzZSXkA9x$T6bJUqaeARSPPfH12$E@bXq3?4gXC@|lRY_1D+)g&fvM5<Fx{2FG<oa$zy~lT-t)Wi?&p2iZg0^VK*1iHBRZu^#-`$HosZEiHiOACcoU#W2P{Wc#d+nf^Kt+rG{Gd2%gu=T;I;D8Bb5()I!N-QgJg%fmz+bA_-up<PCU|{*j8S#N^5Iim7?1oJUSih&jB&c7`!Ffz`L&P4;%rW51tUE=XDI5p|r*82s`F(z$OgR#O3;51;kp26Xe7Kc0lk3+$A9JU1O28u?BffUQi9BOj9YzoyXR?2V3j>>Dr}CyB|n~`c>Z?CsX4O=WZaGo^6qMIdxeC<C=rH87GaM04WZ{`c=88h~FgIb0Gh=x)RUY9PzAUL4-Ix8pL>jNHf!8A9O$$$7*!tp2L{iB|u=O`fV(bp`R9-ep+~6CJjJL9<xeEVnp?XTC}}J2C@y4rqFHt;U0qI%AQdagQjii$X8$ysVL$?Ww&<94P#+or~)kk@=$^aqzOHvN9dV7fK;Ppz;cwF3y`9Op8TvfuW@b`{XDwM#&z-{%;3<8A|V8@@uUNwQZPE1d2|4Y=$5z-)<HB!BtXFTAPm8Yj_~4`d{V~3%LJ=O%Gh{u=8$@VxaI^M!C@&R>XqLA;Nb=apK?2_DYpq`DmW@dZKenB5|%tNy{x!C&ucs?d!PXRRF~<^xjN!_8jX4ly8?ASkiQyHWDD%rU!VfrMQeFaN~ZG52+OMB85TUQgxEmg@>zYLa@qli!9^ZlsND>um)nj+2W>PsQfnLa!|5iSNB%ngG28yMQzi<LH&Ji_%lxwPKxF9HKRb|y;)-$}^hkbsOj!95MwNvs4K!-t8Q{g`+uUgcZ#Z0=X+z|=h@8d(;Jo@au02JcUClP}#-in~(RCut4r}O)08NvNw61pS`whRf?I*AOQ4_7&j>H$o=MU!omB)F`$^^DLf@vE)ejSde*ty?#Ca--nRGD=3q$&r80wMDL_M-GSt_^Edl6rHc?hSgTGd(WNbcpJeX~uVd{O<n&9+@6Y')))
