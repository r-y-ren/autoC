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
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqORr?dajpMLk9&~shi4Sowg|P<1lcrU3xpuR0|N&9HsA~6{`X5+S7bdhBG!uBb*fHxjYJU&)jn0Z_s)!1>s!D7pEv*b$AA8Z|9JCP<?WmQ{NsQ8(@+2O```c1oB#elKmBKUTYh}|=3oBxr+<9&&DUT4=KF8nynXZKhacX&jX(YSfBcvK`u8_~72m%3xBvR%Km7Y2|M@?E`Y-?Y?V|Ko-+%r7t3Q16#djaS|MuORpDUAH`OW(;zI^xpKlA6h4AlMQVt@GcyDvVzd7FPOE_U%>zkB!9FP~P|1z9ZU>w+W}OuOLAFHXO>7}gc>{G0pTPk;EE-@beQ;ddvc$u9lji;wTVJt+~s@38o^KY!i7{KCO5z4)|rv7UZ>`<KO7SHJIfzkc`bo73fZ_V=Ze-#1&!u}Ui=UoFQ!f9lVb&8|HE0Xx5fqqSTLy<ASO?|el{t0cco<^rpB>E!}z(hZQT1r~>0diiNnT43dEWfxdp-mSs{YxaFEEU+%!wAuVQf?ay~1x2aE{_(S2diiNZdPGF?$M1IO<);m)B>A6Z$@46$=8N@gp_P-nHdza8NcVfvU##MjC7M5cv`a643h^0Ze_F9iFF&nHH=lc%C4QNux52y2PD|lsR`^%udWRz{v|?8ZPc&dxb^a1-(v!vh{jyyOK9r*U`^9FLUVfVR9J4=d+NGDP<zj*T_~W0durt7yAKt%z_vObw{PnwUKYsoG>%Tw!{|)xG<g0H#oGgI|?3$F%%k1Y>e$$nhE#CPS3U~%z?774*FnC|PMOky=t!sZ;vrCN?e)@!x_Q=`(0?!L7P@t@*hMz`H%DH{Hys3|oJ(pg-Ki5zF^RFnePu&6>P4DoXW?<tx>{9qWDj&tgZAJFpMoHP3i@VosZY!c)diiyT3oL^_f8G80`_3bKu#KA-*v`$>J$U*qZIAFSC7%S?!z#1iEVA3X<zr;*tfNVHPa?gJs{AZZ+@l$N-POI_SNHuS$!>c7a{0gh;@iJ{_nor07M@6t{07^2rzlO+VOLyznG^5oe)sX)FMjydyKle!JA08USE=n-GW(no&u*3O4e;mt$)6~rU2?tNGk)k@{ziqr&MMzxiTuiyCTyph9C9NwupOq;65=}#*mqv}>l7br%2cM(ecev?W+&b8l%EQbA1?*AnHSU_w&7it<qzBW>m2sCadn+)f2M&m+N-f=U{8LD9ZD8<({t2dRoRFI`V1&HdowyvLWZ3Au(P}T>MS?vhhQ7TvAaRM{PFnXXW8AmwVh)_XB#?v$1vh^)729#CHlQBFWmG}J%It;I?5Hq-783JXR`4Fq+pj^zu_W2<65qVNMC1Cw)Em_k?$Xm!?ue_-6BMMY`5GZB>p<Z8!FH{xzmcPzl~@euKu)1w+|yfFPFZ*pf&|EKGJ6nN!oQ*T(iJDc$Ho9)r0qRS6I1SVS0tT!p(k7X5YH#9%F8Ab2z=*_29_XyM5BzLSRr958P}=`lS}hmzt}I6mEFBhT0L0Zbv-qK2B+LwcQp9c6TTH?xu&}nLSjaI)%@zKXLEbH$Qh$e#?BL<tcrqnQdZhj;U@nImCy^{BtesUUNR^e5$p{+M_jRkhglg(a7|G*2RM!mTC2F;+5XXv&;g$6$$WG1UUf)e$J72sir0`8LL;V(g298rsNhjEBU$E*bTt_Y*y$FAa3tarCX-Tdw{WiC0Fqcdp^E6t&m<9>EgA&ZUSE|Kw7ZNwBN5p?OpojOi{b|eVC&5^93W6idP(?{nH7Te7=ucmrB=M)}@^_U#&~kS=lco107jJyIy^WrsEnci90vY+b?um(zl;7;nvD!(L0=^yVUeJoo@}+kFBN2>3qWbOJNhAsVPV+Xz3W#S5V$LB^9=(_d+wd=3fHB>TULOT6$hK%Re3y@tD3`u|;|S+1ESl()INU56ub4zLQ<5P8yP=(tEJEd-SVBCfk#so|o6J`6R9Q?0x1n;583C^)CL(A*}<YLCPC58{KIi(mTU;0*d=Hu;qUGy^+4db*XwpKHX7)g3o5xtAeM~rxN&))2>$?h^G&w=zpF?{&|)UJ*`yxzyUtA5?MTUP90NPG4}f`*`?CcDBGnM=h|XdTs*(3RFOHy_qtS-dY;|}=2KnXUOuM$_u&SVNb{}pEk0iIlH!3%&_`A|`W$+fTj^jwF*Up0`bl^35D?$N_5riorR(kbkP5?AkE5ZD;&k39o;UR&8m)zce2I^IGZg0NasJoNqZIARh?iEYN>Ah}e@10n$nr@hk&W#pf5t=_f69bV=$@lY3cYo_UVargrJ?F7;XBd>7QuJ@N!+HrLWd@TE^_cT#N&a-eUz5<#+LM#-=cwE?X8xxylEfO@y=sPUDvB)+0&Bb@cXUn)v5MrN!U7aPZav&Y3gmOQpziwawPL)qij}znH>5W&ERWPc*UV2O3y8xfLA{{dhmSy;5#STYJN0OOT4bQ_=(a{t&SmAG`r&Bs`~5dIV9e4ocQ;5;@{tS59<au5F+0|7@p~$=N6pAEhs#jw;w~)Oz(O^o7tH#GKxWOxhJ?<lK>`OoLUY;5NDk6`OELwJtvm~Z@iA~Bb!|hPm4%Y<+{|`wGwTutAP&D%lhrt?|<{=ZKIqf;(eRg9#44`jePPO)xkEGr!C<!jb++2R%pt4-4o%&?M8;Q;Xs?Gac(=RATuM_a-(mq1f0s~Ls{MH2(}xYZ#sQM>03t>b=_p(_@UKTTBH<*U2?5}-_TJ7UPl%8_Irulz7<wMU)lX$XZL$!ueH1VJc?;csU^HMIxsw(kg9s6jgXdF7vIMz+7%a5HboOnD_YCC3xZDRJP*aTqj+(MJEC23{j^DT5h>^IJ92)u>)7G0Bcd{!^ie~5ex^IQOt$0?R|`>iIu8G@Jm_C}(7*EJ-5tvK1#@TIr-MzSkdc;s-Rqar<^^e{t2C<O-Vj=P@HLb=x-Kz*j+`{N^OrbyRZgI1w({-3_vIDUS*N9KuMGv7(05Thn~QG^tvblNU03MDF39R8-RlE&B}0O0>E$!ko3*+%-|~xy7PTuAa!-3Q-qRt$695WN0C41YRet4E&&omk9+UQa$U+Ha;85wQMyE%qlTX%*ynZ|L`t8ckQajHb)u2OvTD(W25dN}d{Nclg_oouiydxqh>?q*4V9`xFTiVd0YP(CvFd%IY1L~IDxv}b4c^k+B7F5epVvoMBz&7m9&HbAXAHI7Bg}~H{e$1C2K8R3<ysZ1npZVv{6xO;>Dqe3)QgzcWxY%{l1y`wbU=!tG*Q@)k(~{|MORVeFLsqtk5L({(VeNv&o9D7t*gWN{^{eN>=4GXw2YXuA%$--XOV$14X-PLft=OgNw&k>BIP}=-dbNXaS^}>0VArcBlnjz9vPG_V&Y%vSLFrUR?lmVX7rOr15TD)Md~HlA6TNeW?sciEc+BANsxZSVWl<xV-^w;=X*k2!Ytc^HeHCf<Roe6-Wp)f2D?0|22U*}X_U)b#;@!x1#jT<0q4A;yjqAsrC<8aP_f>iT+1vZJE{*4<Hacxx3T~96y&IGE$Wh*n$$R7{l;Cwk3HBJO=E@cpc90kLlq%e(jKH5Vg8!5e_)|t$oHEoA<+>C+V1&g1L)EvfOX0J{);6qTeg;I>*!E<NowZ?2+JzN1g_Dt%fn-_+0!U3f;!Z`7)M-J|04iYN^CnePnG=<x0w?%Xk?fiM(aEX>o&8~hdOnLW1%9-YWI4cnZSq(KLt`cIorUNC7F)+*vpNq3kdr#mPU^g;^Or~4$>IKRp*QAEV_LOZ{priOt=B43#Gt!`XXKZeiS?ZU^EeJ=db^MrU`D*jiiiM$8_tI=C<t@#@5D)KCz30%r!dp2i|IA{wm3==`|#b;4&Ecs4mNG>U|(^!6eoCX?aQ@^SF%~{6}dmw1<L)g9>yx?-gSX;?iC8qbMLw#3g0cK<?eP);@de9Xy;VBRHX!*mJENxckm70>2LVDL=p6;_$8-mojvH#^s&Bo&>6H<chFYdv3X1xz{sMnf8n8wEQVClxQ67qRBcEWY-CaBkp+-+dbPLg>@1Elu3q1Zhv5z?&Eu@}+q}WX)`OyZ<i5dX6JWCk(Do+g!}c`&T!#3=B5#KUh2@wt1#pb4{+`aeMaF?V#i;c~D*GImTaST2hnFT+za>3tVCD!N%PXDJ69~I=<oFF+TA)e3g*~()`Oaq|5B^n@He4jvjS;4s_wN0N-<_e8w(Ql?FW2qu%K3h_EKAkiO4;;trI&pSY(x~nTAFx;F1XOr0DB`zO9LoDAeR?(8>B!hFXS=NOAq{XqbSyR4D^On+#tFS4wXMR)WyNUmP)Vd;nPC}t(lO)n|G1Nz*G7XtxJ>-hJm+cj!gjJ@Bj!iNym{T587<sd>U1HV&CbB{p1Js(SAl;|Gcz>^ztdr(>&7dus8#4CEnUUJR(?(KM#<_R>vGZ*ikxzX+Rh83|6_fa#@zDZ{^dH=H2a0<$*8m_6pePPPj1;SgUKJ9=ujPpWg|4qMkapzIe?mEd05OSD3xPm~BIgcC=hqXh%z-0zO*iljmLE+~{<8qjRS8h`Q249-IYMdO&k=H<cNM)h#quw$S%f3*(;X`)G94DlfZlw(NfONrPAGPkINHl3jA`uYbMTi!CnWQ;G4JC^57Y-6MT#g@=qH%8JBlH!|=E=<UMmEShbRUpyZNZLFWRIezsVj=ZNn@t*i1HOdEv1zVS@%>&46jJWO&QBnZ@WbxpXS?xt-wHIygRNYzW#-thMVUuAVY4Jv;#T(@|ob*9kX$Ebj8Jkub0+bH)CA3WU4BaK`AepNzUtv37eP`S?c7`_7Hp?t$HrcL|W;Vqx)wVk83T>-{#s3Vu1q<ospzf_a7s3)OZlY0<^Hq6K3jizz{Y8oO7o|@fX7OnvkqNveL;y|EO#n@azeEMMQF%Y$n(eUIa95fL(P*pv;QjK!F1cQY(QoNb{3Yg_`0~NCgW`~n(=NGQ>;X6NfBf*<FFt;-W#7Rg`)+{7Mml$xKXb7wHMYp9oX7mEZdYoz$!UdcDhPI|+QdCoI@_O??Nar?eOf{uxYwoXO>_En4DbA~%b%9SFMs;gV$(A}3?w0^Xl>_4PvPU1=I$oEI?Uji?If<)?XOUsm?c^~A@}`1`y{V;uFJ3=iR)6B*p$g77(uRyP~q?xD<meF_Y`@dqB=yA7J2Y2^6bH2@G9%WAo@vb=!{!9aqy$xI-P|WgDT7}nGIIavsGqDUn$Y&4;kHwxpNb%IVr5<r0z*_8Y?*&tm0&D3Qht~=uR|YTN>+B5OpkVHLLQGqRJQqI#0VE+;28}cbk%3YV9{|-OgSF#`$yb7Qq+t4yds^pnGQ57qk=N*ku%Zm$7<#v;#LM1x?h2-cm{24!YhNg=IP*2b#p5XELj0tE^hC?TO#|VHS~$YWp(}qANBIhgj^61fr<A9VV?zL$>d(d6ND-H-aVpH`1u><X>h+aRy-@DvNzUHEoU6v`soM6G+%JUJOTuY$nL!4^6%5=F|&d+MRDQr16jno0IRDt&odXr884@PY5xn?<v`a?RLhj0J1+?W&>5n{jz2Yt==t#M-o+9F(%EHqDPlDP+&6x1%jeBE-#JtUW)oP%mmTwa;<X&!DZwrO+zE#DgKQ-+G+e~r_l1SLd(O-raY{9T=_2?h9?hADr+tothr=vA~Aypi5Y4Cx-2J)zCC>8_wdoPhlgA6r_aC)u0L)=UUqQMmDQ7VR!=te^kkFOlf_7rrqU*iIn%y=S$P#$`Bdi<<%cIxeiMk<*v)Q3^oa+$U^}wlk(T?|Yq?L}NC9{+jLim@pP2beEOr>-S6}}P5|}uD+=&*=y#6X}MvEqooT}6I4F#-NX>Wa(Dhgy9!T<x&E-{wvx(Hgf*d-R)LeXdoMc=eg44!%%XuO{GUf4qIXOG#GmkTt&Nw8<OHercd9_`5Qp@VU8m5&o^wjzZRCq!PH5KwUfZ@5mjYwcD^pIgmo*%vohUmRehGk|}`dFeVGOV#OEs=ggdmFQTiM8{I4t!7EbZQ7@IOou3Sr~NZ*n>6flZEJD5;Q_aT$*xx)si*rN@FS~TuRdE(ONL{^yRKIsvZp1TbH1%h)g8npNTygInaob>Gdrz6aN`1rSrRX1$*h<q(_)tFc*MUhg>E#qQG6z?ydO%a(FbFYMqAc%5Va<M0@NDlenfV8{UJ02o-J21#+#M)VZ~-E7gwJ&dBJ0#Hx^f~q}P)Evnd5An#8-Z@`29E2gaU!VA4n%xk1`I4btXskT#xd)7W?+4No)d5@QIqE+TWH6UrNeI6X(o4wSxYu`BeOsW3qLMqgiN6SALpv>W5m=mxA4k4EpyJ~dVI<I5%j+r8C<&y{Ch4qjOtY@IZ5dT4t@@4mOY?|e)gj@5%80rN1Ye>b+ynRdd*LfhFr?*2*R2jrB61K}##uykFad+ygY2yFtozQOB7gIxkcS)w1x5_u>~<e@B)hq9cOTz?V6pW^9I-3D8AYdW|$#kvYQG99Ho81U^>nAAx=baK!t*g&gb<E9EW(JF*Os}Sm@3ZdDI;4^`b#?9IS2t?f}UunEVqfLv$cGf$%S)k84@G7jJ9{;OdBoU@!<FB#vtgUI6xWHMkT5D4SvzbYdb$2h1#O$_?d+|AwSAPeZpD9O9I+BS1#HWlNitO<$sh8M!Mf=zmr>_J_hfjnOD={yu#JuiF%o{5)r?ZUbrocSV?#)EIH}j@@v-t9a8_yB#Hl))WDQ)6MZ>FDry~vsd=9wd!`<qc~I)C6*(wq_x$0<A<r`d2EI1iJao@Qd~awh0Wx}fLk>t|AfzkdH4vb9aq_T;`eO)o5aM6k-X)jQi(AA7sf$#&&s;3VeI!hj^g*Y0?+G&D<UU9xJ|03oermnR9`^&M~FpKq-#Z(+VUii1=;H&*S8jw%op4!SMN^tLQ-Zp#wsU{SV?eRJ#RaIi$)!Q#r7%CBDR^Qm(`V42&x9@hORu#tQi^&_bxnPwM37-Z}c0s8;y9TgA6e0s1U6?_pECX_zYne>H@<!XoNcRuyhD<WCGY)&r<YsWW&xKp@q;FSvS$b0ISLN|b$U7<G<)-}RSJm~A2_srN$yaFim48y_)<!bFO(NNam+_bd<PahJmH=R1p8zIcav;$W`e2S=RFw?HVy#&6YnnWTykxq%7NNdlq#!uV8R%LdjpEeqZ;Xt?ryM$2jbiazH^C}*?yBW36BU#5|haSmto~>XeL&g5f;+<QV4pb^L-BOuJOJydiJX@C-Yj#}(ty%06Gwo!R-Mw_O(L`4rWLr-0z*wRKWjI)>QPg($%^fJy>FXP`SvAmR)m_kg;)(6$CcF<=XdXRWc!KtEkF1+b0R%K+LM*X`l~^=ZV$t^`7K5hv1)Aa)H$@hF_NPo0p=V5;pD_*m81@4GqPwM*<y`_);mkt`8z({e){zD=q)iY*=4l1ZE`jB2(eBd7vbMxFDk2^eye=Z%9}%5AoxeX4-4v-<n0!J=+S2}9q5s50<FjRZQD^N%nu%%9jwDI+GCX+chu3%Q08aU--c}@;!5Dk#9J0*!FA}QGT07j$$pL1J7r6&Vin{I`8<uUMRpv-b1=|H9Qm08Pox-LAIZCppmk4@!8F;n+es=9+%l&=w@=m$3JLR^wQ+~zac-qolR~WNosF~9?n>pRV>5_XU#QYg*9LbHAZPUnpE?N2Uv(6=xJ3NE!@Z2$IVHk+LM(YD*CQIg-ERI1afFn<dzeGsFsNYm;UExKpnq2_iN{CLfusX@Qr;}`~PI9n1$+@SKL}ZVeu6R$gSRK0JHMqjOl_B1RJnU__-3x+H$d=&#5)g%^-NV_g5uP)=5K*K&7A_M=7T%9N;r(Pe=rXvh(BQJN2`<xiKZVv;Hd<fVH>HxISij=?PKeBrctqa=g}*s0UFgJp*g%Ta12NJZ3wg?1c(c7mzo@om99F{z`;jO!ChCqF9)6uPbVIo=f;N=cB`V7MBg5(n<?Y|I>bu6!V6OSP1Ws$N3*LmCSb$xp@V?2uAjQlFDJGA?LkCYpS2(2Hdbo>lw81nY2o%gqO@|{LZsOr^%LN<`3$aVQ+*Fx}$iA!L@m&qS?`p7b8V58kEH3a;4=cYlhUd`3hc-8G0=}*hzIPr}-)N#IzyQ_nt96aEk^+5!GC;JmYS^w0XMy>?^jFoxqyYoPp07)cSJt`+!k)WGr(05lx@y#Y`QeAt2x`C!dB*Dl9FV{I{_FQ&{o$K0zWeySC{7ezm;bw4{L?jB_pkynnNr1MZ;{4lLus(wYL^&qopq6Da_IauI^;9aF1g;+DVZC2M{ut2?5bUX3eL0L*zff94O%z|<T1hX(|f259Wm_z@Ag7S^c3t8m*^Z;|22mt66Jo>JtRk`sch4(fRiH|z-5d)H!j&~?bXt9h`e8QTBK;<q|-mrX8MN@+42-y-bifO_ymEbo~x@}B;Edv&IgnCM08?7$HBtuA~ID|xkNox^9kX5LilbD;WMz%k;j6_1Z7tgXX2wcx1A&EZOTWJzur{M%xVTQs~O09ngKrSEYY##iH;=)H*wWg#u?tMHBX4(C%a<KvJZ3lB=x;!QlDbiT@&fdbSn&GSM13WAyrF!c17kz0@))H$bOMP_K5`O+i~6hRc^<1fpR;R7mai-JGz5G3)TiLSR1%j#~}tQHaCwDbZfXh@ugKgInoN{CIy-yqxH039Ji-1u^Wwm8$4$Yh>cwRP>F}&Wk*1zbQ;n4d=8Dw@TAmCcS=p-gLEzrF?%d=mAbdti*9!RRiCp%c<2Zar43dvgyxVRnZftS4E!V0?ygU}6t-(RD5aa}o+{tD&<=#=NCfS)`(S!PIs+ckc{L-Bd`c&P1T;H9uO!@a@?tATaGauL&yKkH;*OiIwAP-+RS(vKF*hw3;Zf4+m7vZ_2X(g1pw4dlHx9t0B)i1$3`_0}N4{e6G%?{s(MAIX`<`EXdR*<i?^||%xcdEp@An5|GT&c0o)8`qVCagwA=nb;3`EEfH<3blfGN6^D$!D^Ov5V<<WT50?2*8=fGYnmjn*@I^g*LXRdSsy&SFPrjUJs<;~YKcNKYi=4F*GWAA$239r{4gq1YfxL(^p*O;>p|U8m`95;P%s&bAe7;)vs(MrJE1)XGLfD+iB-Pj-nhfms(p(d18ZJ)?Y+H_?IJL??C=o%iT$h24WUb`Rd!J^0+*g5TH8u*Z+X<vB-f;T;k-0t6TFkr8xw_HE%m1?Ag=iw_!jq=r&z<7P_jZsWDkM4(0!f%;}UTI_$jz&YKB;Y<jp`iY8rP*j|vw2QRTF4^--Xp4#A+5nc1*~@*kNFJQ7uqn4wpENe{ZSf0aniE&<2U!@%fSVs%A<<)Sepus)2}s0Q<u9?(BDg3Xe+%k-f@FPiUMOZ9x*M%qcK%e>`O{eI&S0H8bCW3_q#RfpM^#mAUgdkU&F;+-UEs!dfwO0N@ls*9eb4UQX}fn<e_x;{Zc0P3$gIrk@~SPcBdj!Z5`t!<5g(EnPP-Sj=4WQk#u!u_+vaqf`ve7+CG=gt2^@pzNb4f#U5{O2bA`(wnKa<6AR^GQ$TQBwIm4iLs6$&x)vghKu0|tnyHo)sZ9uk=u<7uKj(BiH2j^+$yo`=6?L4}PO>xGSdU|H^V$5UEh!Q**GXY=jhlTMPL@-QQ*L@+mffuhuM7-t@Z=wW*Vq>>(@umXn>NL(^+7+-~GXnvdkq0g$2cB29QaQj5k<SuMyv#G=>lbp9J@sjis!vm-W{H-X<vjzNoUj)?maoRAOAp?+HJKP(%pvyFx4n$MjYv=BMQz<N(8U1Y4wqP`1AC-XYv5B<1FB6jkqIZ?p!9Np__vMb-wqys8*K8L*~G(uZP})wtv;#poVR9EsLiGc2Ctrnk)bD=N>x6M5MR=h^0MO-c>iAMeMzPFC5b-|%6fxD>kZ^iU4f%NIrd=MS#X&hA(o?#jCU1OYVUhU8<{t?k@wE#bqFdG?-7iP^ZHdcJkZyOAP8SaCNJE^#3FsuBj_@>h=h#}+--E=E_`y$4%`cJ+y%$@D&ytQO!?qB?2g-+xt<Ke8!-%xK&}{QK3<Hr&x)X;<h}GN@Q9o|R1_reYSNdO!hyqJ4M`a9k0h*~yK612Tr8<h3o-{EDi!!cZ}NmnWq+tt;V-fBp;Dc<-%Z+ncX|5XOSH{<^W(HfOIIhaz<~EGk80ZgdrTON4U>Vnut}>uY%&Z23SAtOfJzzGMQ6Ve!a#vIwVOdZzA)RocScD&IX%@O_EcoD9)f{<+6ZjIPC;dtNOv&>`{6_!eYa7A4U*KXEA*dsU4uw!pz9kv|1a<(8UPt+y!+Qh;=}z&*x=;7M-$i8V56jXXg;e9d7}Y<g?5#6yF%X=tZRfjf=55gj-f(wYZO6d@o>89ZJ>Wj`o*Nfz5<(<A;*JB{Vc7ka!-+2@t}+$WH$hkHoF)Yvf3B6E<?B@yTeVW%?IR-AtJD|?J7bw<9qmFkHGENdv?z;jhBXZ+U+-KDYUc+oj9FuT_m**GJlDMHuT6a@5pP<9nEfdM)Wy}v^r<$N0m^MmR<#$CuRz44#SX{0vn88)_8i^;8A3O>I$QQ=#PjY(_~Y@6U7<rA|c)#QFbl!-4T74BS;-=(+-|rHgSI07K|)CVPqUZ7@Y#bNbeYEgOaSEsh&JDjj&R9R7$f;4By4NNZLjX{t`uDZs9l3Pqf$*Ek>ZlH0mFe8&Nm$Wq=ozNaP%RBBvS{nxe<|3LPY#0I~-KkfACYB=}R)IrDUg=m~w2Aq*9|r`KN${K}M<@8xUn)r4zqDp@)`CFm>^q0>-=z70iq**SqP8k*qnK@f{L4)e4OZ7QfCEuXBg8=GA;^LX@_$Fs)?4%o-fJNnHokd81%y3U2mlLa-Ak5LKYr$D+Gcxc9JTtw447E}u<$cJ5lhJ-d?aRgrC9&L%c*&l$=Z1S7KWj7xlyE%=~o1QQgr`fzYm}zZCB$R29km8f>t~C3}lf(jVuFf>=R>lQSzEd<&?II?lNyo`(ns#ac$h*RGsL;&bN=w86Q8_BwX|{}Q($^OQuVGJi2_Z;tenEQU1?i0!q&I%jQP2$thWX7h!7@VuxND!S&Q4v|AOX0LtGBVP-r<NjnY5GlMtO*vPGIG1dt9!HPHF3Q(fQ$F*aeUa3ex?{XMyB73nca|@W}}17Mq_z%kJi3`nil!ib3R<d<G8e894aQz~M;pTJSLnk9CO90lP1YYfDJLE&>f1wCg<3uJgF*I!~;UI2Kk(ERXEc*2qo=pwGh`>kW;OMkRdt5hQ#aS>?P2Z#bA~H_`1GQq?Wh-Z_9v&bnGFw6v@%p#sjjDoby>v6+Dk@f)1A#0dWuub)E81*<I=#68`WmJC*2GN^##WYyoq`jVL5uiGVt?tfhb?c1SCOrmFKa30rn=`BM~^HXPdYn@>Nl~6m3uH;fet><*-CkFuV3?)}!Y-oUPP9L`uf9S}}q2nnzyahE2l6N$)1@_vQ&}q*GsyN!#1=7nY*ri5J5u!)TduNp=ChJC+EJeQ;HuZal1(+t@(r?8ebsn&_?^9ZptlmA*#uTi|^5@CQQWR?dQ@}KZU_gN*^F(QQ)l?Z9?J#(C<Ar``BjM`2^Lem@9klC=w9XKT;b0|((n+R(4Pun2op@zp;m0`5E`djj8Bmf9{t_oW&XPb})gz#4FnEqP6y-g$PqoYO=+wMpf$H#3-!XfL4ik?|Hb}VH`{n5dk)Nha`>sPmZ@|ON^f7=NKWqmRWe(IJ@}RQp29;$RRF-@sUq>WtM7L|3xG|dI8~0R_w?vI82A^zOf^=cmx&{$;K?bD88juESK$@HWBf!4|^Bf--ZdSHN@ze154_d|;0f3QtaNmr8RS*Qlk>Oh18Lo{+By?6;I6V;|fmS2NO*LZTBSwnt6p{`M%`SyQV55Js5_jZW>T3TaRf#C?y6B=e`K%pSVPZ8tDbtkUSnLw`>94biyIn*)@*D40>L}N5Gc5$mx_Rcv-YQ2{1#!!sK1V!`o^{h4EI(<v4;=EoKIZ}vIj@Ktct6o0MB>n-fRQKh0n9&`o{>GoKYEg;cp;@pS|zeEJ<+V$7Uk(3leH|*vMxYkzG-XuR<Fi*m;_LR@l_ti*J&8v0WmA967#8dYdK!=*!7VKPGJW)^(OmedN=SAriFo?;xNa2a|O^LZ*qsx9&T|*Twow=Ue(RlUOP<OP<g_#x+5&B?}TN+ELJ4>D)E<i9EEl8LT=@ej8It3W*Y`?Rlq`bM%AS!s_y2fI-TeSggY8N4LlLjv1jh~&fFwNLK}KSw01~JV|w+<GsOec?24<^#5;hdeQ1E+I+|?=Ab)E<O~{E>H=Sqza^2i;K~lFkU74M-Lauq<R}T%sORP#wMPm%sKr=V}Gl3>!BzhK=H)m0W51efLye4?kBOfpf@*dE;#CF&Ncnj<#K^8m-5*s=tn}%U#Vq*{ufQMl!{a+ew5m85slvIhTzS5peC4wTEb%nl@S=R_pfI(m1q<t+1`cfL3-Jn@nnq2~es1wjb82lwVLf<1F`YvkC1|3p4v}IcD8blKVSy4KhI5}xeR@jtRMO!CDsErGsqXx#BVD_3}ml#T82*!uywmZ7`S=X8s8e>;!TSd1k(9L?b&D{<lb)XFro*2vKAy{`mkb3Z!IBBhzyi1S#j%8E5l{`6?5lIdb$$r(NC=aLs5F_Gdo4ZS-@&$fpp@MX!cYXBe%BLs7deccHy(i0_^{DOf004fuxgxhX<PGH%qO7xO7ZDV4MQ<0o2Py7w0HtR%>PttX8uD(4%N9LcHkVAQN@}Eu?g%j9&9K>9t4?#EkzFa$5+6-pMO&y508PEQe-lg_%5>V$&2X5R#$gsdW}<mg;R0<Z^|)s)6)Dd&)@K^4xm7Rx2D;lNhAMmQvNWIGm^m|gf-)3b%#(2T@PxCx)zj-B<R5zNmCaC80Cr{$b|7w<tgdvt$%csD2Lz_j{PTujwe$q5-5RW>xET<w8Q3gJsCsi<V)&2NMNo*q7E{g9V~Xm#F1;X8?e**0ntK4&=mD4_f10%FEYYg7ys0_^P}gSjYm<;o2tcueeW1NNGT<8CfIeehUo_@bC$I(Ew_{-2P|$7Jr0W89W!Nrzda$?<^ar~F4zpA~CLt&`hn8*IV1t51c-29t^#hY`6Gfo21h3}_q=IGs63cz@YjiHn@a59nHIjAleylX4tkGI90BeS((j*{*@;DrtqM_TAA<FW&3i$&tWZR&TZBp|s8rpuv0E4c0&|O|^zXI+^mkexjP7HMHi7Z!5o*|23w?@xOCOa!hoAaC$S#R<)KK0Y_dl;kUM~P2`5n>5HW^M+vL|+=@%j?!&H+2jYQ&!acfg-(%U38vp0)WFHh90JY>bx##dhko}NdkLR5?JIHd}I%HE(+Lb(fK{n?E*+{j448<15zfB#e~1<Ng8_z(wK>e!T@DSQp625C9<Ndu>xVxh7CY4M!py|A==agN`he^%A$3MJe|ax-Bti#d$A@O4cG2`hz^ju1LF*)J;Rd5McO51*2X1+pbC`9i?X%HcC-1JF#2-ZIS=E2j}?Ut-bxl}+B{olHjA|Svq&4CMGDxoh~uv6uGdHf^t|&axO-iKyXF}+br%c-%qBu)ci`FBGtqn!*FFp4T4PTP$>)A_a1|noB;3?sci#J0;hRI4&75T(Hb!3t-X@5et*~mgx~FDq$0^JjDvntfNgEU%0p>ujRayksHbroq_M6EJHTYPLY1sgD^;4MkNWwG?_YnCAO$Y9w9+tZk(U}28Is=Fe#G&K9k}?%418Bm|&Wu377s4FD=rzINhLi<i;4%cw?sDsBEB6NO<##VYTt)LHTPvgs9C&?FwJ~HCX&i!=4IVTCut{LJabTOI*d=D3h2l_mbyl<{lZ~Yf>E)*WnR>aCdZ{$YBi$rVo3Jx6^0MN`PYC=L8_g7pgN`ha_r?u<jIWCzry_QV;<h?@P(P48oF_(gS~4~53fN&00C9QbMO}#&xD{HfRyVb3jStrxHxZqEewme492G>?oA%-Ce9!}&=Ab<ZMh^yn!$yl7V+RAcVPkl^E+TVV6VEC(5=nQ*S5Lv(tpsaII##07vGS%NukZ@FW|t7bux`Oy;{|Ujvpprd=v?rYpWL}8cW$uUqKsxLu2pG7YEa@+gCd?9gpnNllDTY;!5U0lhC+a<?eD_#>XaBDM}`fMSGQUica5FvIJgAMsvC9*j0ksSj^c1dMx1wb&B2~8NfTpWmIc0$kU>~x2VsRBQ+0MsHTF(lN8%T<;lWD$MC~{ldPH64>k{KWTNg>asc;w#-Id?6nTCp<SMuIzqT22k>*WM_W`O7-$jJ_+9wE@{)vc3xpIEU2mcZVC-h-H~fTa}Z7D<YHD?xEqKH+nBgwLf-;hr+GjENuB6&l2Vi1y4l$1Sbjt7g!}Pl`c@`;nR>fQj}a4UZpb`29$O_akW*rYe<W9vdVfQ1?R@RwYI^;Jjm&Uqkp3YNI(YHdUF9#blSjSc?D{b_#!q)gItMd{SukCr=n%n=gmBFM2j#O~umL9uBD)P=HeLMO0aLP-opi11La`>bF5{`xGh3lcO_G)7#pK4~-kwr4E3c$$3Gc8u>xVbK2WrU7<s~)-}S9*6Hg5h;>A4+RKyY6p9k4AB~l@pj{q4UIzoN(^G}6eaf_Jpk@y?T8OkarqJG)y6KG(*?Yt}wm>|MX_vs3n&$Jzytt4rYCD}~*C0<!==z2S2*-2hA}z~Ho3gx2g9$3l7-;s`N8>TCC3Qvv=0G9eCV3+3Ggm%dV%q5v1obEL)Sv88KDd%Bj!kUxL@y<~gb*=ox~fq1dvg$G__&>ER~XO4brB?t#()Nib}AIwsUUI|nr8=~*#@Q^c`l7iBOS1wl3il<v&)m}b`z=_c+4t>4h#rK1xG#Gd8%L>iXOo_?wxFcu{|@ZL~g7Sx!VPLKN(UV2U>j`H`T|k3=$wjl}No#j&mVK-5j=47n;I!TY4cId;>ec>5Q%58R5Exq4P|T3MYIEMucmm9e487$r0h&@LoA)Oa{&o=eDM47eKl-3?UQ`J$`)JAi9dFLXr39D}EPtk-S*!0_o@lybVFukLv{p>qsdww*3ACb)@V07zM_7V)8x%OrAC%%Y5q#=#~+=ul+}N?rYykW+I}|BmaU_1c5Jw<;zbjpYmHz9+ekpB!#TFYb>^YsLa61PAcWW+<;g${G{@-)A6L<-6@XM6IE5v%n~p@C}tbZVB&EwLSN%q4&yN9K}7o*=l-7Tkk>tmsRteGH2tTZyoo;WCL344RQBgZ75)+{kK6-NSV1|pyOB5fM&2YFd56LM90r{T;?LF<`Yp1q5x)OHU*ELtH89`Lh%NP4d9owSRz8t5F4F-!GIjb`EMoo?KM9b#bM-}JyGHmP3hj5PM<w>iV8BVIwuU{JEW!!Y<f72Lep6c^gIo2+IUj^Bzeg&5iiSKxDbmg)c?SB7vVCn)wi+VJAt@|2z|b7tY=zlI-BKYR77}mYd3C9@3NE7C6{rg>+d~BhAU@auPy{$59ShE=c8SrJT^Esdx8wnJ=sW*t+uaUI!!q-4Wjk46?PPV&PS)70s=;Pe?HbmCZCE=W5CSn((qhbZDG1n@#%rS6We$5YIU=0ss{%6YJ;8uaFrZ67nGJns=ZS)zJY5e@(3Pi~+;G6ezyU9=wa~!6W*hh{CkTZ315%a<%Ac0!l<8<DnesPz%HQOprlu!qYO1=b#G?W4%lXSYoWJ}CoWIPeCFRjyXGedN9sS8zKRUiDt7nGd2df`9zl$hM85_m{cnreuSJfzO9FXzDhY#-|#`%`&zp#Mx!UEFEZ2;+$l~u~bzqHjKuIMech76jMZj4RXXidG0+i-+)4RO4f_Kp`%ir<4${L*eF*lOVyJ`b!OD7$Z{y$c#=%8EibHVICL^O5}0CqVLhaKaNj*-N&;*t}yfUvfPV>XgtsW)tURH_OtYov#GW*?E;+aVX}RD^zFLRaneYQ58|a10HsSEM*qtA=8Zu`uv4>A<D1;T}GgrwC=ff8ZE0Ej`W=A56=m_?l012sZ5)tiaiT4nn}orMot|PhvmaQb7^9v2V&SQ9$%Fv%Qc#21MqM3^^NhSlU)M$>LZV`iFmdNhRhju3DKt?SI>o?mif0IJ|f||<Jca5zBgu1VX!p^g00)O4HUDd0std$ez<r!SKfp3nI+feJ*iIGg9SugQrKvUU8l|a)2?uZ-@=T5>>*QUKbbo7Wa@;^U@->v;6rS~f%!J~)u$<{tYKH^kJ5Dwv=zo=W6{BJcOV!GjbPm5)5|(Fk>fjAj<3AK5FLhzg`PN>>e-gHqX)%)LxdlF7KvK}tq6QA7mK3Nj)G1*0w(JSkVRhEha!J+?vCQzDT(6i0_pe?6A#tPHnq;wv6mNz-KqK-+2}F(&GCLBYu6_#yv3>6J{DYfH9!*|7RwXu5~D}EE`k)f*d-Pk5-O*%I*yPX7okJ^_$%VUnfNLmjGo&}B$9<lg%u*zz3GUs)vFjJ0g-{sO%+IRxZtI&jy_nau5d;q2=aE!gJiI%673tgSrlsX92M8@0;@j)c@nyfIm1y29W^pxaI{2^a^=Bv<iV%Y!#j9+lf;vu_Q^8TszbzqXB!osLr^^=ht7|#0OF{*VZvym=}AU=VKN$O=xAuW9rBIH4v@!BR%)nu2~0ae{3Gy@_`y+X8E#k}1wTO5dT6ga(4Fr{6BDv0>#5L~g}RAZX#8Ml+Jhy^{~dX_TK7bV@mkJG(^ddJ3)*m3n$v;C)i_dbvL~3QIA$EN)9R;S^YcLSf(JX6L6;|(*;(<-&dY{$qc5-@CzSGdnne|f@Wm<UDyiSSnMOq9v?wj)Y&V@zB~iEAv^QySV?m#4%>DGI+y_48K6;qDnGY0gj>uDaI3sot(yPwT40H;nss@^T`Ul`#GWxp^i4h47*5=nxI57_^4ECUxAS2v6`!YKeY#Hp(uAxy@hjt4!6?tY<R2@2nw^ujXUX6gCjDzudBmsLj5`eNz{0QW;g-nr_>_%I%+omPE86&deNX(igyW1tOX|4i%=}BKA65{s6MZF$eRMNZhp1hZ0+b9V5Q`&<+fd=c0tB^7$%y<zhPTtw37Z=X<WvHBbyn};a6Ft_`Z6E1zs264U%M(=c-rK(JsU*6?BRP0(BY>4O%t@F=!WG+EXbJRu!cm@Z6r@{_9l;W@(CyUWIsON_%aA;<lK2V0N;>#31g)C#^nLQW-ho3vLC~Spy&ODHad-@r#Ul`eIzh#eB~TqB=e{?lojw?TJkUZ}@PjxO=v+Of&_+W&;wJ?4uv`ZaX=Cy|ljsT9O7tdb>`m)6LS5hCTNK#;zqSNfJ!{BF)ICV$;9w`n+Q-2*7o5Bb8pM`7AU1hGLo(RbW~FFnF)h|brW2fs?a;x^N|QD#>C;t!qF}yFu#DDf$5N>~hv9I_B9t?@>$*ABP1=Q)J&j#+1*Qzz_&!}hJhC<~vAZ07$d-Aj96)<GVvlpEA6<Sy*FDG8unkvcI}xMxM&1}x>=M}J()n3Z_so(eio#x(81sL#iv=Vj@Kc*&>(dsCq#p$g(<UgutcGY2xrkxi<37<`A(ggw$k5%+LwAFxAEgk1<%~|11X|c9Zof@HcS0XfXfRmibs^m@F@9b=5-i*a@qacc4A+yw;MhzBIuJ6ve8WhYjTOnT9q<kCVI8~G*!A>v6B#2sJS>A|mBSIXF=<UwOb*!;KM}pW1J^r8Sn-z-oo;goiThE<RUMQeijKj>Oz)^Kw}a~)7kmS)$7cG*A94*;hpnMGoCcn;mBVZR3`36?!fgtec-8Nv$@d|ww{SCKC$L-%RByCBVmRy@lW$r@2h=nsn$X&0CqW{u04gQ1Il3w?O>sO@`4hpd9yDBO4$gYtn;Xqrr6FNkMNC3F<+f+t8O<cvPz9d72S5CX9*B0@m2~jat>Tz&)uZNAYMkki%zwkNg!dka69mVu0X1lb!a(V-Xhh5Qu=Vtg+|xcdCJ7N17eWvFe0ALa@&5s#&AG_')))
