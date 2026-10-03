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
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqORpr!ai#xDt!v@$hjy)IiEOaQYIGOXm>~)R0WAa!AkF9j%s|k8pB4zRGxNHcons!6_ffeLMU*k)W_m=po1OEWKmO;tfBMru|Kq>C`<wFq-M|0o-~QLn|LKo^{Lgp)_y7I;f6M#w<^8*V`QJbP$9La<_w8^0@cp~@@4o%?)4TWa=l}kn{^dXZ_1)jZ_wWACfBfkm|MgG*{O>>iKmYZ9QTn%k`0nGc{^9#?e*FB0A3nVMYh|)4zyJ8nw;!H<W(F$%a=AbK=EFCi-@VU&EiQKP-+lP-t6#3Ot_!kQ(ANb?ESPq|x8GcTbup|f;`Mj;`=9^tcfb4a@zd`wN|Rms(>I?#{BThseBWX5X@CB@fBB7rU3&9r>1IWJdH<K?SXaOAkH7iw;rq+QarO75i{Cd}3$jWpBR^S?Pd>HTwbwsk=htww7EGZR%;oi6uSsd0<oC&3V%09aU1CkT1(LPI;;>6^KW$1&th}%663ff`Raj!pzSG4e)}<Ran?FdfOK-oTD3#bhf3{0+KdnfQiD>@(-7dZTv>}xw|MM()o@dp3y<RP~a&g}#YpD(Cj!)L>ReZWc^QVt?>FtjpK4<JtD|YGar&Z|&bT72TFSPVNco*7bDZJ1M|KeQlbA+W<>`L*e2JEh`Uu8{ty4b&9woAbWQ?!4<*zD5VPZOVI_NPs|^me`6EU_<N{<{i04Sf6Q<Hrx*e*TBQ`|!i(?>>I_KQI4xgS|QV)eoP(f5#jlu9raK_fCm9JY4UDiv1vk_Wzd!*MAT2sMfyli65jc$}i7wX=gKfdyiZ`cQW(`<lR4@?p%Lk&v)X_70fplP-^T|f4MyK(^9lcZ=VSXd51uEqx=Lfz;RbuEp2zT%$>)_aVIIcA0VHGvUi0gWvef)u*`2Y<emlcqE~+Pe$ua=f$y|I4>;te*j(dbak215AiFjK?agiko~^H^G{2;0#bwEFzWL$rKm7RF*Pr|G^AF$r^tT^=_~Cybr|*KEqb_fW#69-WT@KKlJK_0}cHSEC<o+A+qrBCZ_bYz$B)%VZS@QHTP!D@e(KoTua^c%1lRu^_tq-xN(jAt`pXj4q^7MyH^jThhga>@VXzhmOd!zB!33O|pT&Hx7S#^h3*O?OCB2HOaP|BRF(p~mWcgiQ-f0lO#beA-0zf$aYV{W;c27lYn16C8W+m)xvfqjoAcII2y-RDvJTV;<D=#!)4eEQ^g;@{TD@3p$OIX!P%v$u6qF1hSpa@#q4b+!vT*e-0udK8`$2l@>S=totqAnsm4Vr2<s@07Lum38?m6E_u&ZgUQL>lcA}+|yTL#OHs@S7PF?GvfoR<wsV2kK6dc=(J0ozPJNEyIpPrBYmB6J3P>vy32|uf7`(OeXBo>@A*Yu$RHm}lBYM7HhWWe8{{k7;BB^I9CI&t&KTIYe&ob}Pp37K81UZvz|4+*^O>XH1SodIO@F3$Vn_BR6S)iE&(aBfG#x2CM0f3n--FM;Dcxz-@qI_Fo#2p39@r;R#w`wwW8`~t`SIR-Df$Dn&r-;TwAPtv^y4g@^>)r1BSb_jh`!D{`>NZ2JoE44vim?!yBD3GWi$&k&+@%)>A~-C;;ZX)&>C*7X;6<mS@T=G%+5X-$I|7CbF5yRN+%$)qM0+yaPo_#v9I&zGsB_pbGb{G*)Ch=*Hx1r>~sBkZ1OZeTvx1H-cOcXW|th(`A2O`)wUT3-$zAk1~CA|;x)%;{}jSSU%#H$rSetRb#Z5HaqCj`boxul0DMu=E>(N03EVtJrnLiY`|rPbJhELT+Onf`o4HqPU98yKPp$S{cJuJ=((NHuh>t~kl_tAX6@nzoDypy244m~ctAPdPxTj9+ntzer<yCOIL{E7UfRC)S_1Rf^qMKjW_1S)1D!+ufU3{~18FmGBQx9A4F5T2aQIse*b$)r`33LmENs-6SCr@b;YcIiMKj`HpnC)V%D?;C>&91)rye=&%Wn{sNX&ddY9?~yn+hxUHEMn)P%NyVRv}%{C9m~r*KYDk^1Jx}2QZnsNlXk}wRURavr?r2StI{hNl#7V(!+<r5E`Ml`LS<bKFO=Yz^sVdR)e;<Hm32M5WL~CbIeMm7k(W6KUgk{e*As8x)nrGJAI0R|9(Z|q2Z86?&?w`U$Vxnpb=Ol(0P*Q=(qp1{!ZPtODcGeqeaoAN-Bkm9a+Bx6OrEcQTG|Vj&zL-aL-L}YsRhOQ7ArWwT=$!9?x>2i4wZ46@F6IoLT@+#hzjJUkQx;YfWcI|)UibZw>TX|6s5OnbI2#y95PMzOXM9YH^Qa8RRtw~mp^m^f48%4xb6|!c|M<N6~Y~l0d!irT`G54hFz?;?p~<N<ry9k6PVH!>6iz~+b>Hphp=0hs(wB3Rg3<*o*O9vZ%%Z;;raZ*cM`KTsA!<#9U6!wx<6m&{(Q9`3%YvY-pbf~po2Q{K-0`ii7PKd>DvnQt!_l%yAch1Cb!+YcJg;^qTb!wrs}A-y&?{3tT^a-CltIyvG5W_2WEES=bOtfER#<#R5Nm-ewbf}+aO4yjq_xZ5%6!~ci(;d?YsAl+E0qNeqtLQg*~xtf~?wMnsn*7H}}?X4BMu(jQ9$`{to@4Bai#M*G<~qlk$>`KyUft-T^u$`XpI^3hficlTq=Xj0$=(Vk9e(m#ie@lr5h_659+fY%{#F&G61P!^d7T{JxlE_}$uoVa$Lek3vTW&`aLTL4sXj3~=;}gD0yqu2T*gwmOkRas>*`JdTW`9=`+h{6S9@`B<+xR75dhruBgN1U=xf57+d<eG?rJbSL}kr=@p@1)=g5gvP7DhF$V>4NtdFEd}}#Q{*RQ`Q`Rqk+WcCXS#K-%iHM&N}wAkfC<R6A#N%^r|=@oW|tWB#zg5v2Y-q4xE;ou5w}I2>g5o(X%af#U+baGN8Vtow38F`<3lf>Zdd5wF39&LJ$Q!t7>I6bo_r2Ztc-i0$k=rWyptSk8W(nngI8e(yTky@azgRMUt)H&^&8#RA9Pz^ZUY9kNniMYu8L}SFSi<z3)fhe8cPUk+{DA<Y746|Jj{x8>bzs_sl#IAjr{pArUcP?n#yS9zwfl8854iGoS!~@`gkd-JtulObF>LZs&3v}j)^2QDO$R?IbBJ18&TKd*_&<o1OZ-Sr}d}usX82NkxFdW<~13tpS(Vf6QCA$TDZ8pUw``a;|EM%UT?Zu-+sDEib|5NzCQU@pMGdw7w7k#+jg!?)otfxT6E`HP3uzibd@ct#;sw*ZL4RRMK`6{{h`JGq1FAN&HtgoV=+Hj>`z;`QCfG^1Rf-*v~lXxb*Z}5xhxqDtL3_0?Ll0YOm0@NE>+(;83ckP3kdQU#Qt1f%>@~y2V%v}l=-6FRJr-Zx>W7GUY0bjjk+!cSAGCqEzvH8SN_``^2#%W!Hy8-<^&<olh;H~UNcakU1K@LD-TZ8j&78_dHrkRQ@|2$kFOp}pvo*P>?yAAHHzk4g}G0UEaIuP>F1;>os$}HPHIvyxR;xDz1jx2ESX&Id|j$O67t=LiuMjf_&TDp1Bp_Jy#vX1soH+OEU}N$%`R0RFP9~I3o_yh65I47Ytz%Q_B|pLYkM-?&dSUtE$a=NvfjwM7K>eC#G!J=%En(}=bfL^E-_NGP|RvRK^hMMEQNwIwe*dZDvdqy|Fp|7sZs?k{t#^<@9D1~-kxsy=v&0TahzEz(XaC4&<8o}rt!;0>L08R+6r%m^+Ac(2W40vbTu7~XFJdG!+CZ;=h@TOcGw)KM*A=gZJ4+8DuvJ2)U-Fl?pr`JC#dD&3D(S><e<z9suZ>tvMb4ZyOP585<A;V9DBXQNw*Rs-AYWGtwg|j@YlLiYzM>mB!~JFFt#i{>0ndK#-Qr5Sh>a41<EZZ6ri`*y0xXKiPi;*nn)->)kK%WDzICT?Ru~slNRl><wrKV9`4D^&7RC;n}osNBn+M=;oBa2bxb0Jw5aB$lRVH?NZxy%H=9(2H;{`>qsq;S%d%8`@sx`{uyV8Fb*cLDDOhK{(4F;WS3Ef{baryI$?wf{+Gnw|kD+w|#U{tO9sBv5`~AED=)k&=n?#Sq?f2yl-C%9}k+$*64#%|Va15+(=&}U%4IyY;UYaZ$jA=FV*roSB`6?>=G@CmuDn}484b_&j6+LfaME@2W9XZ)IBPWOS;ws+$OeFG2k-&8zY36`eYutLZifgMvR*1EXR<l9~6|fcJ@<i4A>hH#@zdahKbl=Ag%C&~{GSS`{F7-0Nj#Adkbl%w<_+dwq?&jp!DDTXz;8uJDcCHS_Dv?|MyAK~f{r-v(IOGlKCRaF;{&IzrFnJnE<bBbZ)>6t+35VNz`rY2s<MvKo!plUDMBw<D7ngRsLMIeJFXg;vc#GRSbvd_YIKs2avfgS~Fe7An!yMQVEj<LzC$aAnYspQlC3lO6n|X>rR*#g~E>hdrg}=_@^wp7%AG_3fm;)zB9wKi{DwNmsnCU)dx?GDWfnlsb=WA?sz9zl5lc8`93(IC0c}3nv$PD<LkuG}JZnj-@@u(ZL$#vQ$@ReF1^4{@88^94oK4@B0Wbv|D@#zlj^QYf^^Z64pz8z>^<1w~<jBQUH+jd|E+a+s9#qOHR60#Y%E>&-uf}KgT%|klPi-#Sl#!g>w+KTUGTM%GA$!$Sku8j>OA{g!>R5%6_NxVj>bD89$?UAX*V2;mYY&`aS9X#;P6A3ST?Zp)dza^@6<*O_BiA)<fdFVu^!4cE0Fq-=u+9L93i$wD&q@C|&iDCNF5gNA}SsC`>aIiL3?HIKmEBRf(l0;IwL~*aJ$lsbRn9~Q$RKUxi<$060bn+r?B(ni#f&<|QNZ^A*8xKe0Bp%5>`~#bT4{U%rnbv&?bRL}2i*7GNMp3||5onq(VtU=@tjeFWs{fo-J?E?~-{1K}u<YqHAcCsF>Z#_YoGRGDi&aA|(|QeQ9czeuz%{$NxJjFB<s+Fxmz%b1(+51$!sZkjAUi|YLktRCZO`^<$`)v=_o3ozY;2HNqg7#zR&~#4)o9Mpv{^w!2VX%9$@I<1o?|Xc;B!pgbbe*t`Q<=$CcgEbh}OTY<=BIzUq89>PIt4gn}Nn|1~x%xgH~4uT3sE1)*?J(UJEN$cX#LY7=zYh$cj&gutMcn&<i*1EZocrmntibYI{nj&MKWIjrKo{M4=s<kIPJn#{B^(iHt_ndK>$+2x|N53tmSM{W;d6?PT3$MpgukiYq%Ru4jR50Zy&aAAZh2Jw@+SXuVV2)H^xIZ~*3wKtyP&<?|5{FH%qR;t>%VU_TtDBFgGugb2y71+mz5ipN0kBfDJ>>X;f!P%q0;*cJcKB<*RE6ird2HAQJtQzXuGDvm9JC=1swmo)~$#1?JQBPP&Mk9H}1pLh;DY8n)s;a&IIl8py6@IW>M_P$yd<uFEk#IuGmz~!Lrfhjl~j48Suj4AP#sN~wB31-|mXH%}!Xf+U^AA(O3tANhsJ|Oa<rNn1g7f;M~#bdVZHZ69Y4&udhKsi#tp&Yhp4+{-Ur}!Z<dmNGR0h@+~YR4Tdp5vVkNg6b1Ao9_4h?xOCh5+e#G7OJCfw(dWw7+WLu?bI9XOq50SwiNpPjonzg|`gw<j&#9Y@c?G`V0=dg^l-m$ws-zE5kbada3+%Hkytk%fo1(k}L0NGx#90UER!fbvHL-i92jp49D%r1PHWoGttJ)ylLDlJTGI|C4{;WyEA2pBW*Bs-ZRyVH%+!s?^oabTG&mk|Gf~0TI@<84Yf*@Sc`Gk<=O!VLQzDKUNIfq;B~!vmMM_1rP*2-<K(Z$dok&-+I7wY_dcFTy0n)Qu5jHpJzvvCPnjAhh*%}Hqk=(KcW5oEt>`p1<CqLo{O&5NV^W+z4jmK1*`OJYG{SL{;79`;X?|m8-HwwrJI1i7VT!bAG}EThvS}Kv_M-r9{%X&UVLu3rc9bi5=xYJk$VVDF8m;dgX$Bp17U-a}xOu2a^r5EEhnl*1sA;qXSB?q1Y^CZWx3xY)(HO1^K#d_HA1SOrrS9oXHes=Y?MF`<XB&9UcA?ev9x?gk(|d)*SJ9n4D!_=A0Hb1=IO_uC2`?0&Px!TaZL!mCwCAl$N|a{yucuwA&Ke;0NlZMPrAQZMTNImJs*VjH4TeWZkv-N#D$fu)Dirppa1Yt|JyQ!k?#03jJT%~i15nv)Lj=6<R$LUa=puMD;=?hZ8hZn(sT)l@4Idc1YB+czucJTmI`Nm7`N-?)h`g3H*U1l>PCRHj?o6``X%dCcPU*l&01vxK+6kiAHNsz2X_-T#TX4g!(8tT`8fo<f`T}F5X)Q7HxW`5#8)ZV|R<0jRx><z*J|R&anFgrnbc?O*)e|<TxVA>?h`Ur#IDgOp(>yTlOyapS#lxMcICqAT<P8)Fks$b3<TVq@BOKf9WP2pF*zNFxtVR!D20ed~@nsd=AFYd^{Sm}*lOD_(CaoTbAnW`L^&kWp`e1f3$WUp1IweUV>*Lf$qeeRIAefGTC)su2j`GQTluz<ah!Z~{P9DQT@)#B(PX>r*MJ^=U?)89NyEJZ!2RYFm<h<!Yrh_YDqrKdH)5|?*QSCDXD7;=0QUjryd-(?rd~61`19Eag<IM&Qf1_Ydh)Oe!;^3J^4hetK<U@&*59Nn^2#^nLB9t<XP|9Z^lz<JH;Xc^fjzweR*ZH)_aT=kIaFIH8avhFdSPO!#^%sK&-9+0DK+j>dX>Xyq3ex<w117Oymx5mSzR11-z3`m~COn?eqCBn<&CL0kPY|O;7QOUSR5{v~AlfAc$csvfmQ9k4kBMqW#zZ;9_b(>usbUx-UZj&*j7wur-F@%WJ=jyXd<rh43==+gCmIA(=%EDw%QrVC*sNpl0Q*4C-?h{49!K)8G27pL{4IbsFFaNc5g!#+d{kNSQD?<RgC|Kla4*>r3mt*<X(&VjyTrz;j|MB;N{Ll&X`sn`2!Q3!cSK`0?D8FP4hC{loZrA>>w^es8Rlt;k?c80f%P273HEC9Fzxj#Gu_y$G*+<N7?8zVeDd&+zz<fBOu1^jdZ+PL-GKCK2Y-!XB$)=nO0;l5e&Tmf*9K{|0WhE5hhNtq;a1S~i8#N)B23i0E?Fd6xHByznvI*{URlXwpTMUip#pQ=)^h$;Loyxc0#GzL#a8j?nzeNeqFFo2{0>=oBhIvjJhgGtQ=52utivbY98`AMhI@99(P8MG!p6Q9f9&g7PTIt2GAkHY;BdkMPFnblP<hZ|MV%|_5~6ccP*h@kF|sq%eAH;~(XcCYN&LD7C$3=*DLy7k9$(T9smQlAg1$68u`$t;*O6o-Z35r?ykVWEnhqXn8hB7$vP;ZdK}f4Dx0>UTB60^sFTGmD6x$HE3&gA0L*kh2(lck~jURkB)DOBYqNn9JIo{ShJ#+M1v~^3Fjakj~oA~}9BTW>PJsR!mW8OD@pWwjPJI+9nf8l3jFA7RUp3Cj;K;+32q0SD3#@=pvdIH=4r^RaFCf;R{?}Gq{!<WA}d2&GD^B2>7vgHaz`9en|?8LCJosi0QLK@o%8EhwH(onESw?dBVN;Dpo-FQ@X;g5Y~Hz4`}|JwFmD0c#K)R}y~Sv-vQr5$!UPaK~1AqSX#U{b&I>H%JDSEG?=jYgt18fjCbLHqh0u>=mTyG~^Zekw~mup6T&%CfCNLs{0@<^ok(@zze5<Y8yncp!`y4rY$%ItL@m5DSec)M)%Qc2{^bvQsC*qaA19=9$Ov!sN224r{b_c-R$a0?q)iUk;E902w2?=o6iU!^z1AFAQwHYtWa;Y7-Of6xS5qcNg&~fY?UEUI$N<4YbKtw%`ojNAp5qT8v@%;@K%vNomk(u`5s-R(I2|x`T$rs_9-sD6t|NlM%HI?fp?f!AQn1tfA{16LDSYqUk!c9tS$x9a@i|<Gd!HjuLD-m)X(YBxYq44~hrhyw2c?yw_w-J6K#rp*46h20*|&NQ_ZzWd*g347`RTvfD_iOL35jBeT8N%=TXMUhmZi${jR8b{+_5t-Kc;VaR6w5|8wPcOH5}=hmu;!6~{EgHz%!QSqKP(oa&gjTMmWAa!{v9q-WSn8U#fkb+%e06Eu1VzVpp*C<M{CfQqC*Md9lj(ps-Yr);~SbQ9~dmcpg%GZsf$_^uqjIin~!fMd*a*^)3r_HW=<~Q8cmo(XV2hDIeXgq|^xMziVWYT@bnRL1nC)?i(3`>`RV{)gwqAr97^y)=Iugq{@3`E7Fz7Ms)cfRL7b^<Kmp8H|!s&fP_%1A(L*1vpcbK$d+I+(}{u|+ng$8ua!=2b7+Yhb!_qdeTI=;CnQ3wM<txGO?FkCAN)xK~0o_K7!;7CvI{ILH;{(cF^7RPB?h-KBq0Gwgo5;elAU&I!0kU=!#Z&dknt^&4s<#}b<(ty%w?Lfz=rNAiF`65TIJbiX8R_DhmSJ(w8D6z1x4FuUh-!?$_iOVjR)?2Z^NHZ#^`urDBw%Aq(3c0CbDT6|i;!Vh^XzVIQ|R^$am9-P#X>Cl@2aS2Y~g+t{I14OAnxpTBGF!ZmY-8wFbuJF2=N?W^vU15%D-v~TMvEU9z6x;MCu?5~E9BsC*`2fa{z=e0-H=fWlc!zL!{xjJI<?J5eZBWA?9p_#nt-%f7%0nKxM0@1&rbn*u9yv!0?Vx=Ra`!HIlFQQ<cXD}pWV}63#@nG@<IEc_DsQ;xv=t&wKA|nr78NYG1m6EZ(yl@WG6A3{OIr!Cn<k&c#K$Rl;9AxG6a$}4g+$4bRD(Y+x+AFu5lMBW<cge<t2}}Q0T~x*h2HLE-X~2kg0T#!<GOAN&KfOoJF=&_i7b+Dtk<dmJ3kOhmLyC%&??Y@R3};b6cb_L&D+NvD+UVu#?qf%+x&+_>~x7(G#coU_oo~u5sN4g6+2iAyTk<DL8qR?pRIhUi1F2<k}3%Pg)qL82U|tn_Ho>qq^W0;=4TRj{t|ghkjx71o=B9wYvl%Im(PVtRmhEqSgWyOt-)%w=H7TkKB(Lu9Snp2^)bmf3?1wOC%Fz8uNs`BAmXME?jH|}5!ke#gFE%fEXn&>(4P;KR~;av$_0CZ^KW{}-e>^mac%sB+GIhWb}Vk6cC7p*Hr|;sJSpxIPjUbGW%<LW&xqZ<@#liZp9}Z|#6b!=A@LKhuo{lE#pzC4jDeScMLusad-4{GKX0+}61v7Sr6x~ZiYKYm6zy1bgda9{_+h87Zycyob0ADL2X=NKj}Y6oBf*f^fCo=@N8nA{&#P<8x?!r(=-$q&zJe#KKKirj6Mu=0n2hR)$>@iv*{tw57epZ0^PtQr&18>$-Sg--)}udIi~ihn=!bKl>CNNt*CHyaFF14X5uKAZNof)F4`mk&-;IH$@5aRAcMFf-ZM;tFI52KN1uyFo(}0}!bTWz2$+#G#nT!HY7@`GKrF2%5!V`>MOqjQ>V#z){Y329o?J(?7L?y$p;RjR4tKa@9{phjhxO;&7A0U5vw(-!qyil!6HiRCDmy}dK9H855BSM7|cpj^ws`2rS-hv8+)zd2q{Nv!NnwTC?Q5c(*b&*IcEgQ9Uqqgzi4WQ;XZ!t*8FEd$jIsSulv@EzsBx&C22I=U<NP{Rd4WcX_kYtrIN)zAwl(W@S*a=scQ&F)jrRxJogpSJVKA1i@f_i7&fn}2S`wqlX=annNqg;VQrZI)g<b~<!IAT%+iHTrFKyya~bo%-RPmmD1Y{fHgym%;l_iLnAQpoKGSz9-18$Y}iStgC&s<)RK|FvU4)!T{d8tDf*%(<%2dSbLojN4;fB(A#5Ut^((LNXnx@m5(RGHmddxUWE2l@JK)ZMahAGnqgdT&D%s!<J634n~1jTt^2BE@r#v`h`;L0`{c<)iz!j-W>@9vY18qLXgM;>5r1*dx6^YG9@$zqM<Bk0>o>YwuXejH6?Uk59dD13p?-&J9rj$U>A1SSlD4>VK>ivfrl(r2Q#VdsaM81;+ev0xC*b~%KS<-A_*UaBA<@M+(=;ZmuJQl-9yWg2<FgE3|IQf;VsJN9hb;OYr3N`_;YyU0qB--uG=!yyE0b>pAi{+L63!<!9O4@!p`Griw4jgNpVZ##Vwb69HsZTE`W%<>rzmd+t33d6c8YF$O|4&2kf-u$%^Whj5L!NaC3_HYi2bwh1JZ|J<UvGH8X?N%*;K_jI=jX9k{alwBiR^C^teDC^z0j>PS7-rNdzx5rZjh(yLe6G<Zlx1uk?t_H5WrSCc1zr2{11fLa_DSxIDrcw~=^Nhmy3K&GzAVPev@MV<jaSTU!wVpKA|><dh$*<LmVCf*nrd1Ih7farFC_$Lj1sxt8wy^7|>!i@9FWXx=8`i*d!K^yBQFPM*>6vyOFaXd-W4-11}Wf?`AcL4Db7LMu2-9*|b_?K+AM^P$G)@nL?HbX*iV4ZtKWnx@z&ZI9<ZboTJf&9F>8x&Bqt`WYxMqgiNQ-cpf^mdn>Z(R?Yush%D>3pwecqm@ML)FUABWUe6MKi*({bH)LyS1_IR!@H9q><}k6S*E~du*odv1QX9TRlvgZWmqesE1tuy#XLktt=}@p71E4_pEhLzpCIgE2h*z5RD#!X!h`50BFqhN(SQ3Ab#&*$!SJEW?gi>k^xdFDy2avr};s`d6^`f%BOa>yQFpx-cT|b9MePp^BNP%3NQU>hLmaWi1kUc=93tiHIc1GvBpXl%Rw@XLa6>~qxu)$ArJT;Jm6n&=-wZnWXf$Z>JpHSN8kgZhrBdlPtp!TDL<md&W#%L!Td8n;8D)aY4c2aZ1C8?_W_VVPQz)?v&dJZLaP{S4B24!y$$xDUHE}^;m6G_cJjFRvyc49yVqlP1uw`MVK6Xqb#ORLpPwJNrSox1&0_}0s1J8-lcprpjh9eYerG0v#%RQ$Y-P%x9ttYoT&usNYz;tZCZCowt7|K)uC4Cr+5jHZVhK)~A|*4S8mlzBk850$z)icvXiico7KvBsJ+Mp|mPuBrbylS|Se04~tV}INy8`B#Bu^+p5)BE>E)b<-yz~D+6l}1iImn2Ncu!?818NW9qym|yhsPB89(D4-l^pS7mCq6DjvO&0uM8UJVxp_?tjMUOz0QhVgNP&`vjm@><q6N)$j*v<cGgP_I(zbG9hY<#d6P<1|12QI*ibrPz81xJ*+_X@g>{e6@SxEXo8gG<op@@mepg^KrO3l(GY?d)G#M3Puo`cRb&>exJqx{cRbog+ADL)JXQDOs1rT`eys8P79^!$SA!GFL>G97WFv)uxlC`3@k|&R$2{wktM9pLL8o<s(1dZgqv}{N0HRwc79y!=1j0rU))jdN}Kh9cIcyut5DjNAz(PRgcn9CB&GiiMG$Jk8rh^J(SDB$XcyzJnZG)*i9=zNH2k|qzTw$29z@+6)~6}8Wi*~1ft7d)s`XX|_lKZ#wJqh^<g5)D8AddzMDx;($F{5D?4J9OUXICwZ!<hfb->r@imgJ-4O8^Z=unaYMOo>d18V8~8G8WVI}EQf8>x+5Ad4u3Y@q%Tn(6eN$K`+>oF^BAm%YADtv#(kBS-7M+_)plM`1k*}4$45_lDtk~^`PHMay1p0bv?qVCo_yJ2Ur4d5OmLFkQ!>FRZgOAb*>?7%qHB<pNfSt9lnCrNelV@>%Cssjt0ab~N*;_>-oR)T{u%+$y0M$X`rE#21Wy||y-coE*G?jJuantrtcf)b!C)xChM}1A5R9RcdCzdQ^;qVf3zKp2ad#f=QkDTP6_m`ab@!-xNzv+8+V9&PB&%unVqs`)<}INLF-zEWYbuy{fOj|A-rdC#FK0M@F=ABJyY2H7$1jootr>+g-=S}(1Wg<=@;~<MR>0U*Xe8b23N#%p18B}cU*J3}Ax$UOqz&F^=C84^w&U1o3-DmkSI60=qDPMYyaJf4A7UE~RO@?2@#*o2hfUXa^0>aUZJi_ZGXWJUtWmorq5&iH5~*mgL*qeXdWAG5*XgSAr>n}Jt{U$xZ_J$nrK_YsXSiSkpNBB#mT7El;@4H6oJU0=%UgIF7?pWoR6@n@Xdu_*c_V=~lceM@leiejg|<KgR%=g^_-S$A6IG(4QQO5IwOtQP0|&J)Ximv==afi>4doK$H1Gnq)xK_ZTZY@xh$8N&phX80HX8KVOdk@F{Bc-ZPorG}AM<wj?!G)&RRF6haZG%LH6>;%i_C;XGZXUW9JF|t3&Mk>8TahqqZxt2gQ07|P8_b|LwaDT&c;$%*@S`5CUjWSi^GmB<3hJi9<aqwou8z{PaGiO*FKsmQ_3&YK30}9y~Q_E?JEA@gF4ll!>QicgHQLk%?Il?Z@k;Q;s@+?(KTE-*agz`B}IB*`YMoA>FYpJZ4E<;XBeWHj*DFa@31o3p2cD)rXyM-1$R=$q4F;uXexoK8NS_L?Y6z%{{nef)2_KjmjR&=q{F!KNUY{TVr_;{!10A${O*QbK>A#|M^qMYwehM*2_3jT>NHx1hK?`tagwwKGEsI=S`kHkq6U&^H|~k(^~j%9bl#MUqtfjn<!)LRV89^ExEYSiepG|dvpWdA&_U?pZX0UhBF@WU>z!Y>FQu|GmCnypx@V@+{WF!$&s3Bln~cDEWKlk{C=bh`)D>WjmvRl8V{3XRG5l>jNpF}uY@;>8%`z$89sEWUDuRbl5&VRT;2~5rK2p1RBDKe!kN5frkmQ}w8$om7{-}wrWz1xn>=HO1W&${c!e3&wO|4MWDP*BVn9@Wd%|yrOAdUMK1HJl|@DDo&7wHj#NdCmLT;!F1fZqp(Ll>U?mHCW69Tzt3B4wJfF2JT4kn>5)Ld$!IAZ&xau0R{8&3<qW`uZjf{fRX6C+!)BWt(l{p+TB)xY<gMS1tf~K=NKRBrh7ekjO*m((}iaH4nAg!4hixn<*e;^K=p_Pam7F)rEf<oB#Cb(?>DzOen>YoDkh)VRe&rPdC|EGT&hP!;|h0N4h_p_@kP5s38!Nn=<;wM;A1Yoa6zpd-DK0D~&VpX`I<HPnGG(w1zR`Q6lT2>*MFN3&gh+51*D#P-9OnDK{2gD<{v0*6c4uENP7BF@<H~wU5P-QiNzM#b!%8OrP0N88R3kBo8x(H#4;F3N#;BzLT(gG+HI2es>IxQfXTj;^Z=pPwOIRw!h^ZiztTd<?!^z-T}u*Fc~y-dh+=t(JnDu@DNB&R<=YB8C-`qG(LHBc#=n_J9+fbNs%rTIF#U*K=VDASX$kQrH#J6PRlH(Be4{T9c4#M3C&~A2tKQMa7u?Uw_u6Tv^OF*O##JSj7o$d>r_6DWY|GfFhnH;IEKb@Ezq<vd4QNeqS5tP8JKBer-!Y1sFqN)A9;vz7R58UB7rK7Y|iS==4`Y?tFr>Y=~3g+6hB0m=)uNm`oChAz)q{M7$NI-2X>8}78}Y(ip0CLf-UlqaTE!4X`#x?7m97%%q`9OUp;85`#g-QlJK+0x`^kMI(RIJ=dmPy#}$06`rtDwKA4No$y{t`ti!qlR%|vvLs|GsthAmbcAg?RC0tGP+$TnQv-a$N02^W5=A^;>GEl$su*U53FD5?HJ$WMC6XGoF{51{_h7rI$UQ0d!&nUzT#?X@D*+_BBHA&Y{Y3Adw8&$)uL}`(%R%Osym7&U)GOZ<Tw3f7QYDotz3r&FzhI!~N-+nl8Km+L`ocw!^gX?|~j&K9a72nu5l$!mym73-2R%%wvkBl7l=H6jX2FGCdN(hmeeVNUT&usQ2O3Utpj-PD`c(y4In&jCu$;e|Nqbj#ec9GNu$owUWRs%NRCvFWJv4EdM2mB;&xA<59Wnv_ipg0;4a28g;S@#5-&4$ld-D?P0GkK~?q_dGT?J@A=ddAIQPvlHyh@+vS-*ngjQ*@<{ro<l;GZK*e%&5%#b)Yg61a*Q)<Z+Wko;)P-Z0k+ok#FIH016)jpmRSb&HYT#E-~-huLi6c*S*$Z|9fE{H~BdW0OX`{!2+8L*7kD2jP^U0?mRsF&gsT+%B{)3szkdd<N2A{ny6g#vgYarY4*PtzWGjD)yAQKP2mqh?B4Xzt?@^<gJZ~C@x#$p?3w4We0P;-gV*=EMqc0Re~+y19Y<S7nX?$mKY2WGh4;XD6uEK&fap^Wv{YE5SSC8{I?-y+49KP$tp)2xrCqCW+%e#J+$uC2^K+#G!>%10e<+Z<@z?m35&0ik+ixmsJEDR#REOyZ)0?~oGrID;_id5qATg)DswYo>3_QXy@m|PcmnbHcb%FH4Y5e7NkA-s5R!t<)0g`a7ONrCxn`T+ct(^70M_M_D1z&@nugWtcs)rd-H<%IClj$|TI5NE;3g)_i&-9u+GGhCwjuE%l6=)>TwC!f{+o13^_j`ml6bEr0^83rL1jlG@0O00HU!vT@6le1fb>(Xa$1Xbu3WNDC`!F4%%z}$DG5KfZ!vgxDP|L>QmV@07lx3OCLt94f$Jd(X-7vK?LZ$3S;hY<OKBsuoG4hf{;Agt-lEzBU2vcxm5T@wP6ioaW6Fb*DSeS2?h1q$iW#5BZnwsM+7G~n}ypw)$ay)<|H%1O2a4{{@t7lqvT@u-8f#aa{ji+Snxq@iGD1eDWkhs8`!C&H}Tb?P>Jw;5__?7Y{(FhMjnmB1?V&K^n*~8B$I6vcdRagEJT`Y{j&w3^exsgYNubeUIQO0}h$qhfzLo|6w3^Gy0(z*n0I!{1U)%Z(v!273N0&|Kdkk=aNOH9cwp*&~zf>Sn#5&!`f1|NGJJZiaQ7hO*&vt1w#RU8t)O6RG_?J<{XaByvGEb;}Q{ef|n%VWpI6J6R~t!0OcyDHOS#bQ^WV#TVvOgpWJ8@#$N97xjd3@io{IToH&@8IDN53_&b%ziNByP*LU(8Tr;^8E<;eyJhfk;xIn2$jJ;#ZWG(S52r?oNmKT6fn(6P!NH%M1v>9A@ID_z@L(XJ>Kvr7K5#e1ePWsr_>zu4?g8f;ZqXczlL_OFlJ<RWUb05mWXqeFl*x6ri-mg-cls^Gmt6Ajy4ju@j<cTiND5tSVFj-L=Ir|&3z6=-=92vKiMS&O22`vqcuAOH}Y}0CJ?ElKi^ocgIjqB|4}w6C5}Mwewa3X8b*!8$Nl7o3i35ECIc!yUYEdJ`@o~Nf+{$wb`doF$a_M_?oo<p<i}|Dcu9XaJrI9Isz&)Z)Y#)t-#ZQs8sHdcfMc||8U(<xqbK>bA!_wWllM`DL&YDoGU`EmJdXHi1!)I9NE;xH5XfQ;8d7;gWaq)}!2`2@A#D0%$&Y!5{21Q=`LV%XV+eF2V@qhIN>^nkj>%!QON?VYIt>M;u1dE3x`3V>c64(1fH8h8Fh=;C<fJ-CPXBHfK-%9;^<v@)5*h7>y>gtQB{qRDhr=^W2>j3@9yl6-#l2kOSLH9UvDUBKL(4A<P|@;bTFX}*LCy`&amLtziDm~TUOAX>iIW~Ub-Nl8e~H=Q?vaDEBynT23-}PN!G~yVq6$InU<YrDwV_9UDz9r0l@nwiYV4e1uw#nJ8g}K!@J?{n&1Y1aBhh#c#Bd<m9b|^cPIcs2Hr5Q3TU3wm>(>%~E$bL%?@{*f5HoZ`Ih2guK91e&YvLm#dLtt`8#0_{hIJA{0*s&84`U1}(!~_*lBe&8^fC#9s41@7q$mbZSdIh~X1fGF&`tk=Zt@2@MYbS2ogI+EX@h$aK?Z1(o=lR{Lt%$<4z2rZi&>a?nOs)Sp8#e<JWf{r8k+|NGVCIyH@_|r0fao?<o37=BK85-+SOkLc-FYHYX!}qATEB;PPfSeEO|VnG<MSDnSc<~pk=I!#5?IY32CAso9kK&es-nKiz{^=c-C-n!ZYnTEA(EyIYI`yKV;yP!vrYI(^CeLKV=~Emst3NOY@`*bUbAM9B^ruIB9Z-e0)i~b13hf!qc9XHPEdgRVgY8QVAdjmJ!b9Z_AR@?vbQ!<qnxTI|y$eE05Z%3L$r#*^Q9Z!>kL6IA?l<Ht{e)&*0HB!-JmDG(dx<2c%$^7(=V_lK7SR!LPgnzmk3pWL)h=W%0>p^2Yn!8WcK?bX($}mwNa*Nt7@5y`iS@$rzc&ag#CGsrX}MXvreZj5zkJ8FA7AA7H{xd6^Txfq@7T)y_S>>OOV*-wSJF(4ovgyz+Iw4+vL=bUsj&vrL@~U+5&REhL7y!QUcV1k|y=E+NF1o4m=U_lgRQbgz3F4j`ihpTP}2By8-3gu%RFB=xKCmsn|&GGaOdF%<)kaO8r*B5!a@(p%wPtVq=Gzpg>#L(uh!s>Mty@pYL^q-8c~Q)ZKCU|6L!PHj`;)DMJsCG_;YE`qFT*d>auqCs;phJ%YS++2)79};Ax=A?z1VKeY6@;a03NLrIcBgHQoDZFT;vOTS-x3FczaoaPF$qlE(I=M1yn`*3UN_Zkw3`Gyw<-;aFEYd!lnC-xw)pnnc5|UA1fz>!QoEswuLa(*cfC<oZ2HsQyvHa^|j9?sTq>%?;WhuaPvS!<gGqW%a$M6KD0-)a26EpIV-t9QiVk<!PjRFL78Z>85=3oW(yx3JRXSR#T^I}JPD-f$|(yop`$JyvOtEl6wo_wXjZ{&`9c&h9O=`5}c%uf4C##uHI7v(wO*mTSkU3gk=b4cEiP9uE83-}RltqOp(Vo)cqxInIrb^>?%@r~v|tJG83z!&-FaZ?}Sj-6$9gjC8S8gaw|>C)kK1QB}x#t&+!j<hX0YD2qeb9x9dl$PC+_+*sgiF>KMNxAc8?fC*>MeutV8XDK<jY-tnAJLKT^xWxKgO9k<rBK6O5ZZ&UI82uD6nSTI_>7H|a-KOlJ;>2uBS%fnJB9(xy!f<wBGenr;)s)$^(gYrS4YvoHgZ+lU(q|5m^Ni8#XgP_kWK9r%iBEVv88IPOM70vOn2|9U4d@tl-AvF;PvSn5&`7Ht~#PM21RViZ>`sq3x_U>HO&vtA#Jo<uAdR|mUx+V_9)dWuT*dJwkg;@suG}n|I9U2ra)(>^*xcou#HRRkONCfj-D{*#F9#6wn^mG2?dwPy%CVafQ?z361L1Y!Cpf;hq5W06mH@2JsBBuiS9$k3@Pyq5XU<^ZOz79H}f=v!rQ(ZZQYK;E-~h<SYohvEJVHF*=9hY@6he&Mc(9{&@t+|#Aw^YiGv=kd9zF4v5}QQIa$%89HA(VYj5R!SF_jfboQ#w$2?z-1A!bpSm)%KfEIesG<WH41c)4XvGKQgr9CKsYXyxQ*1RNubLEIl?{E+z<sB^Ar%K1oYcnmK;it7KS$gnBhUoEHBzoUCP8x@1$EGpUOzP}lQfFF|r}CvHKRt{d8g=4(^Th%3j+O2oPDe~+a>PVtdbn5}kmu&;L=8`KjnDCj$&*cz*_M|ykW?)_GR90{5ETa`snSrO?!Xo~AU(mu5sDtKQF-P!xT2@*4#nr-{dd9Pzl-s>rb?j2KEWaO34HQ$@FXuso=6luL?UG<3_%dFcZdg@s16s;0flD%$IYG}H}f)oom5zk19^<SZuA7nV4(49&;#xWD7)e3(7oWtIDTS1Y=zHkkngZLe32f()I1C^(mXMB%5JMkkEF_v--%uNm;d_m{{gf{f3N')))
