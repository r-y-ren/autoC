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
    orders=_market(observation,commands,needs,sum(h <= step%24+1 for h in daily['hire_hours']))
    return {'farmer':commands[0],'hands':commands[1:],'market':orders}
intent_agent.telemetry=_REPORT
agent=intent_agent

import base64,json,zlib
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlK+pb*6apk}8nGbot=&jwNt%h1=gH4SvBM^cB58%N7_Kai$Gcf$`!ya4eI#oL&){4wsrw)1054tf_n^n0pBV*lu|8H;p@sI!X4}X61i}Lo(zx?sf|MT;|`~C0#?alxBzn}lLye*&JzWL|>_4(hv`Qf{7fBoAZ-n@PD?fc)oc^g0f_y73M|N5slzld+&{O^DL<3IfAkN@;9pZ~+Zzdb1Zo8Nx-{V)IU!#6*E{OyN#Z~j`D?8+a$|K{6wx1X7T%D+7B?|${}n~!ha=D!vfyZCS4z5C_Q&smQPvRKfM3zAqc?SgN=x%}#4IIf6Kzq`Nx{1<=on|I&8|ND#5WS9Q#n~(24T$BjkcR2X8|M<Fp{*8lOdi81PYDIl|`<LZdkAB}DfA#L&50{JM$=@$s{Jz;*kX2e4`DQ`hd}_06pZ<iMU&GN_Foj+)m(TZfO-kz|zfI;6t9I%25^K^ckgO#Zhh2L8Y2pi)%>^Cp((47Cqy=5xR(3(>!`(qx(9Pag#0A}@Z6cdLf3Qohe~>7Z*o!UOrPrTUq)jQBi>=$G*Pk||lH}h#lV|s==3)M1sg;XeB3VmqNc&5&4s&rYi{?)s?b7QXL)_KuPb+rm^`}+o1#~a8#4oh;Hh34>WhuPS3V%!=cU8htD|V&0s{y^-(}S}~yNmq`X1f&Jn4<j)#%7mZf10?L*`GG;((CndwZuOC^uPR%KmGSV{PaKn`9HpwpZ@vu)Bo9jUP-ckCHeOK_us$!_TwM^_T7h%-+lkxf4ls+V0TEr{P6yVH}*XyL!Xz~&#Qd@mzZwzX*UOK&sXiA_yq><Mp=}lD885Wr**s3*eEZzE~#D5_80iHpaKQTdTRLP_@bP<BFO722KJIHoyGDk`FejmK0uy+sfpdb3wyH$T4wEM>#IK-^3BWlLaDuxM-TFwm-&-F-|JhN_Cu4~MX*byt6w0le%FWI=L7TeYj<(vwMRJe$kz|sQ=V;%rp%h8_vNzWSKoa2FYkW*xMv&|`Ei&sJxJWHhn_uktrc><-N|)yT~DKd@yzWHTJ0j?E+WsZvUTr`oo(W7TIl1Amp%aR*oOT4$np`4+|i!la8V|F(vF~wARRN(Za>)7ejWHmH_<bdO3y|3*~aAW(vhFkWqGlRmx;mOy90fBmd~l+Ij4gEoC^For65a{o)mX_+B@kP>diVh>e~MEpRc2L%j|WqthEqrwS^e;Jt#tLmh#MH_1vMi_sCyJWaxv2=3J0RRJN<Rt-C>6g?idgme`&AvIO4AlZ@Wdw=L;6(*^+nYVOYb0mi~rA=tl!)b&>gtv>Af0igTpE$<tfIPv&yGypX1ira-8aER*1j~~AI-QT?X@ZrC{0j_s}f8l5tMwylmc03#>efv|!Zh>x>=<YPCziY&StHa+l@z3di*Q#A|`&VoH4YmL$`I(pQ7*1(mWlmjS=kkf2%NMqxtB*DK01%WwAK8f~+BBXmL-1FQ-fj6VnLIPk6=>+p?!B=mz~sp*k!PS}{`3P#E9Ne#F<lN1fPHkA%ia9y1Woc*{#-lr#Umt+DVo50=~#Yd45(EeA+A0`V%fEe^M|u8hRD4HSk~mV<ch4sTuUxX^=pYnqC9-#Cp}is#@P=$qe=X*cX)=q6Cd^-p3?kKTE39*6JG@Y?fk?Fpv}Tpm?U5N$~Kz2Lc^czUG(N>c{$T-v{}omuW?-w5H+^5@9gbp(l>!X4+t|qJ8t}&IJR!`G`5kSwf9Fmw7A?K$wLZdd|TKXOJAdvtT&=@VcH9jcBHmyKzyIWwhEvmp^&}YW3;t#Q{Vl&T)wh_W(@?IH4tdlK;VT)5qp(0-A5Px=DU0i)o#M&SvzSAkDly(FveZ_#{&0*KYyu8ciS8UM4A{Ww+Ds%z7&|M(EW2|2RO*h$hxF}-S9l>hBXc$+X4eU?Be_9*PC3OV!|4&_R%?xwb<1@IVVsF0lSyAHk~usrP5KKCEa;s34Pi;*D*E82(RL1K__;B6_$~-e?>NXMGEVx0li$XOSMh(=ZXQiG!(m3o!kFhG7mn@9>E{itJk~BlI$2d9oMV-d9vIgZZ7XpdP}9VGqZQ`T@q9I?mp=uWLUc)Y`CBb-%7V%1!<9V)Iua#jtjRkD%)}4=`YgQ{;IE`)Azkf-@ZhN?xqXfu~)kP?lcK!NS#fBuIHC4tAlWOlU8$r?!A{s0rr8@E?4L0mnG4`<~gocaq7#j1^mcr*Q>Ya%kv!k$YIy3-P>hJa8N0Z>s2a65^nl8-5)JyZ)>x`xxAq*@!OH<AbJ%oB;(J;gL!_WBtNSdYlYxjS%PmmEQOHt%XgG?vN|q>cNE*nD%qv#RWdz6eDlJD>)f58NXr1*=aV=Si2V07!9!cTSYa}!%Zlh=Rv*`^%<9V$kn~&Zdhm`r(2wkPJ$T3ME@H)TJ$!vph!uq<cJ?)>V=jW8iDyrgRaw}L^NTVKzMTn=QyCJ*F1FI%BzA^T*cnD;A&Ji3n8(_U`9T}ZCO4Rk9yfMrr^%fE+i|ID5O?*2c2@<nGIcZoP>UI$!p+cQ+R%U|DLt;x$b!dTkTzFIzyw1&LKWI{WHIf>y|*ZIn6Wq`4ZGyK{;BHE-*fYP&z@JR@~>31W?>aOH8#D#9twc?lV*BoS?Qr=gY=-vkDgZ7-7csv)2<EWew4bhblz8XpoBQ3U+uDxQ97*4@Vxzr#=JYNOrE^IqeCT}d8%0Dnf(s;=(*7XdX1OwnDZ%Y;(3ZmxI-kYz95w+=XLq5%+Goz5BnY<GZr#G1p-Y-py`%$8=9y-5E?I~K#zxHeC57rBns0%(8Rn%lmGJKFv#Jp-lefF>28${ORb+-9~>o<N~mCO#H{Ey-+lk<H*ed@l&CN&3f|=D8!}+UrM^vm*K1IdotEx^#DFr>uijXE_2#OK8kh%Us8hveMTNiPcn;AF3~$byRdqiBRyg?b1@{T!zvjbIi2r(7+PUn4<5G3^zbqLJ_3?4N+8kV#Ob%*2E>$7KO!pP9BY%V@iFw%b>TY;wn3oR>@j~4ll%jlCul7ROiWs_`jU0yzHEd}jNJw47875D|h%}c%X1vjtpw3@{I(`W{c3C))F?J`L=LPFPac8j)*dkGj?E|(-rHu=dIxbZg&SgpGz{KNHb!3$tK*n;vS9oY4SsPBi8=ZSwUW*bTndmtJZ`O?5M$}~x={c@^IeCV0X|-N1p>MscRN35@CHB6N>{9huyDYJ<0o5*5PsDujb9atxd0eV4&dZX)jhv24;Wn#-EHFqm)@aq&;0L~eANVF-worK4LEFX$bc~gi;k7(gRxne3h}vjuZSdJ{VOvUPMLl~lHAbV=6xTmK<g>zu91Px@M?{Z@clr|Ktx4)9gFOm~(=G)EFVR1EiNxT=qKH08to-SBcy`|ac`8)dHnFi?A{}bPTX}5rx>Dvkiw@3+LA+Y;utS~n?vDle-NhN;uS@pt-oO9x9V9?%S9k4i-(P;_kj7f==1O(*kyEN24*BD8J=isugDuXMKOWbEt#k74;c0CTC&r8mN`IML2#gSvOjsVGDkt$g8cUyS*aRLMYX-Z-@ZQ8GuGucR{hT7rX=n#SdFqh@3*l-}>hwVU7_?J7EshHmJ7u8&1w)UAp2|W!E>ITg<@Qo|Hkmntk#_5-3}K2?(!Bk7RE98}Z?avWPPRau^KDWVV<G7@S;aFg&?53oi^$8`;8FHmdxnuLFCV#+X93ceiWi-#_N8KPS?#`5n&cjy61UajF`;+TvDkI;BUhSdAtO)2k30<&c|r!W`J~1)BgZwOBP%Cyml7+>NnBsK2+%7kn@Fo{_#9kWF%noO*UYB_T#{G+`kn3NywbTJ%R-}kQjACXbeAA=hz}}n*h$h1XMMwNkSB<+VRw3tp29{~qDA3i2YpD6D|Dw_T~STAcyv$|bF9BOc)2&qHeT^H+AyC_tL9}<0p*^#g3b}?TIB_DykWbX0i3{5L$R$JpF8$%oywz}8KTcb($9<mxmF2h#-yo?QajQKQza9ayMpH8Ei|XhheYL|as#DJxyK5aH`fLtGTXV(I9j1`wAFD%;W&>G8VQQHd*|<hafuLcv$Pr=v2=>VYm-4%pzFl^Y8nc%0(+J=nm?}4M)N|2b^}VM*i}C~h}AGg0fIpxpcTrkh1{cM``f~cpbIa8&b$aZ?d1Pwk9l^s(5NDUJ;^RmmaI^~w}>d1)$DPoqC!0`P*kWw0jxqjX8RvqA`>qX$Trje=#wff5I~5&N1t>K$rqd<2j2|20$ObWZmXD98<`>3wHb0_&6Wns1Dk8JLHVAQ780R&J1B#s;1Ho#dvZ<o%mq*3ULz_iUrS{h;JMWQ@+3omGI;x2SDKl)81@%Ct>T$9pCzoZA5)~+k4ecWkK{e9XhHY<JuED(!$@-q8qF!_i=2XCtC<Ws;N`WM_bXO*jY0ohz}^HYiZDlGfV2xKiZH%!LTordPXPoMt}HIx)^OoYJGD<56^&wo6m2e-J>&LBZqo|QCY(d;3BGN5jdA|e5h<_8CDL|tuELVq7De!xCADRm)Rs|b@p!%oNkB1Iz{ZQE2JfjD?867rAVHKnEwYi<@<lpHRyiJ%ZGE8j3eDCpAKl|8Eku?r1+XzzvIQi{4g0u2xnT<h{2WR#ZW*@C($RMxcz32q`yI&y>B+L3FH3H3T*ECUlqW;9?1dp>12CrzbSm3*vN!nqQf+Tu#plx$mgRuVL}ICh4%l9w3kC1Zrr=DDJKJ+!Z1#b^{)cCVVH4*s_QlMHf~O;@khke8j`|A#ZC7?t2+$9Ufc_%bE^7iK8z|OLS{p`Pa%6y|(^1%~my(5T&p~0&*92;KX0WAp1acaA<WvJDt6g&2?k*T4b^Z|t?ckIGf3rJFs#v+3oh+BFUn#>tyAmc|2v%%0*U{V9Xc3sa)Q4v(5qT5g;PC-d=Es1pXu~jQX}BsQE!m4xXME<jt$}<M?X8LSG^i!nCATM@@Wm%ys1W(<Z9r397vU0g-U>Js9Bgcr_BUv>E#<H)Zhl+9{8HL60`HqCvbr8$&L8}Hr~@}yjEc}8#(Yx1A+Hl0pk3c_g}#)zjHbYg{UR^+%e>gH@)=E?j{u*1MpN`;G!+JZR?dC|1}<wbaAjfO&ceWBO=~o1sZpe*Mrl!MlxfBvVDfj{p7cd$z`=9l!af6*u%vZ8kDk?0=pIr{tV$qWE_OU1q7-H@2!Oyxm+HI?J5Id&p#sbz&b7D9rQmkTl~o0I#*QDzzxEjkS!e4O5*<UWGs_>w^H$l+fwtiGjY=*GVf0f7)5?m?Y-{!)zIgG;0~(~DxMsMRKhg2Mi6_n`6eXe9eV&Yy;n07}O<eXe#g#AK#}qGLfcNgJ#hFI+sB}7MJI4q;GHz$_t3l6Y470HqW?#cF2Mh1Zs%7a3r3(hkMNX&K_!1a=^JDOIaN8v)d3(A<JlW_lMKW!5(Of|B&rgwT9xEw?Z#7uH)m)@o1=c@B0^}N~fOb&2o+Z}Dk&=n9z!cB9=Zf1v6JpX@l3}0+y@4L|hQ&c|;4O)Rwx`PTqTwI?jJ;_YUjn}&lCWHPf>y#eTg?N3m*UDd+vvHbMmm908vP>}ulja5h!Kk2dxI<_j>(<6g#;C#+h{5&-?;G-H<_WJb)(522b%duEZZ_YgUWO5{@78Tw0ga@UtTXexndR0WV0)D65nwR>{tvv<mBO+WS1E8?BgOeA*=AuS$SBg+a<6hF`<98XO81qc7xCS$b*-^HHQ^bw+%fGI*7^JfCRgNFm(sVEMNScSn{Pv`aI5K1wHsA@37U7;!8&QUxHg<U$GrDY}Jm7JQ0fy)565xG#!$HsPimb@#2+sM(wmQ>g0V<Bkzlvd9GsRxr&{SKbSP{GV$zAkC*yWqR2eri6Dc9zyjil1;q0jAYNFmVq>X_{gfG-LLdn=7bGrnL6Xf<G>u`g*yCoO`KELWYZZb$*)aE6Y#`ziyVqB-`<Eeh&*<<5f@}&6+0;eIrg@Ti`PivA`Piv=k{h~CH#>&+pMo}th<4OTW(fPBu>6L)MptMoU16|vg}FvokQL1h!a^PQo^02{ml*kWhPVb$(&o<JL&jbuzv+Vh0(ka~p5Q9nd^s0(?v&%#ZMyoT;-*CYD>n|Muh40A918Ym2$MarO!mw&*(=LrZ>;IrU@3}o(eliJ<tB$IxNL-ATkaSB5i1WjcUrm2i^k%j);GO6G(5aRgNZ_5#tzx`&?d$Mj)3K)T1ZS9t&m@rfJ<2rh~plP5Zci9xI*_yJgyNo#7;lo@L3AKG)IX0fVs=Q3g=@7Mi}zs?GXZP5+QAR-4maj`1s_=Qdx&5KH1?;s0hFSuM^a7HLQu-0<nTHXOuu|AKQ|5R<~`~ull*j$}1j~@R9W&uhG_Eo#tyyM}C#e@vt?9k!O@7k2ghmxq`5ub8<YE!`B)z6C<^S^vX^b`~qc%#q`TJw~^-<ot<NhwS8)JND*xXF>x7+Xgh(D&QBtQpE-Is9v$c)%`uAk^p$H2VhX}F2tHd_e73IPvyC0440e<<+0h2#4X)k2c1q7ykW)j{f!!nqeZ|?q5rU|Z<%`OJen<_qf=LD%9*m19X7XiC7v7uQ!N2Sq)1NzU@^oaf{_*{9zWMkbQC{~u`=7rmr#C34HSSL2DK3Q;8E+jK5fnO?5$7WRCM^Y2Nw=vpqN*}KI!bhORHCD!(qeQ}QZEjjCvy&)m1%faU{p>8YRsS#pSv$CLWhgFxP#VCOFNvytzARs90H{Fyh<VmoEM$}&I?Oc?I<S+FkT<@^8q^Oqthtz+T_Fwe+zBQ;Bguq4yRGXo|J7u!zzNPpUd19T4}^_(1>FUv|LHr_B6dx;q^+5*DDPk)(cXzrFxAn8ixXz&j&Ajr%esVHdrs<eLk1TkoZT;wBt^tISGp>EP~m<hL;RtbJ5nNr9DXrvt@_Bon?VZds0U4jbIiyLMxQkZQI63l*ywhu<TLI1#$rz%h;d<kt)_TsbXWLii4FZ&c#p#hfQ#@OJD+SeA-tq1YGSA#S=?!Q3r44I9VIblxUtumU$jucG!VOgu(mZ^p$`F*nf2LLvV*BO$06z@(6vNslTw;83BtrK#uUmu=vEDe1$#u>Pc2P>O6SRLWarHxuYYqU6ynNdogGJ8HJy#qC+h-=&;*G;$Lg<<GpF;D&98n`D^u&&zzE7W=fo*WM9O#Flt6eZ>`6q2b1%JaV44!p_#oJhP<six4eqWw~EUf@`j+w>xZFM+()9TsJ0PfV>6Rs+0^(;PI^zQFG6B{5fbkzn>?<vN8Y-6kA*#Bv6Wb`tPdSy$`i=~i7t>)E0%5rHca=Fm8aE_Rc1$43;AlkkyYkLR*AhN=rL6lkEyzO$r}HRv}hdRdS9*gvvjjZ2M~7|xmX<bjpPN$Ca0e0HhJU|2v#)%J~8wYkWL<bQsWhuomY=eNBnmRc>cGJ)?@VVBm=wKWa9_FK&8dpjh>MYM<mnqCo%<oi0`1LWRJ6d!JYkYj)%%WW8>*F!(;6~aclpZS0&KT=pkftQC61+i+NX>ItxPHgB@<U5vS~LbIdi(!ZD-Wb=CWE8k1v=uW)?<MYA4Sa$JLimaHhDD;PQn>9}6BgJpplUqm920?Rs)&+zs373Cr4H6AjM;bbwrR+66@ll+7UG@|W6O0>WYMU{@F6GRK#*G$U+ImkA<2qSHy(cTE%VT~{s1r&kTLZn6Ab)jVuGS4sYiVc{h2b!{ctw|k^>=jD$RJ7=%##37cPg@UX(?(vBu?KwA-`74gFC{Xq>+2G&ugi<aL-FYAnlEEvpDYh{_6)9!1{n)c#-+f3Ro5>dt$1G}jf}M!vTRpZ>^V=O2hdWps*OYewF*2Eoj4SLiCkWNExydeFrB{<d5}3j?@W}oD_7&F5&DHVMos)PiZjunZN-({il<#*aCwkViE%~pBReGLMJFOL@u|@yzP?Bs93D%I$qoZkWQTz%tqlXU<6;}%dolME9U3cK?Cwe+oxJWV@RI-J%N#AdQ$VGi0%UDt@Gy~JM}p)1RKpvN@o)Wxb&SsI)3IX^3bw<UxXugOxd9QlfS*V^hw_EXn?=?Ly?|y*zqBAE;BFV(e8}L5!^x%|)+PR{LLQLiQ59uX>0b3Zs|tI@?z5|(w2{Wmtm|USh~RI2JpP9}s*dY&jyd)Q$>CT60DCMdU>m^mGSn`TeS#}{ln00-4f96rQ-)n5y(E(-R0iG$Avrt-WQ@dRy&HJz-Qcm_4X6kOwD?Vt=7wrq%1B@DnpV?otQ2iXbR*V8_ZEw`ToG`=g~w#oGx4fCbcV$2RTesHYtUJDKxczic*}FA&O&F2x0p)2#Z=^T<~8Un^1ANq3Ca7~4LEqKdD*`MG2k#Wy)aXZ7idJp$KL<+eQq@kc=+7=43BG(_21bA47@NnStmm@Mnq&J&!oU{X+GbP6`WMvD+({8aZ+E8O~7m5{kly6$T@duew_Z-kxg3Dlshi8I=^_dS{+MPHo2j*y6(XWvtwYD*)iHmA|g5=^3e$zkllG8d-5Q0JVoFCMRGcq>@2jM+(E#I9s)+%rt;Tr&yA1#81(H~_A7H(Sv<I~|1~fEOU;WfJgV*R2UD0CVr$bpiV=v+SZI}drv;Xi*SAMrTbX&0WTi!tQfu7#9(SE@gAy3i8tz<nY1YG1WI3u?4+u<sPS&|+z@b5S)#J9_{BG-=e?*7eDL7)UHF#}RQGSVV;Fb*vF4AZb(%>~nf!81b{%OSh%4NGY`KEL7tY1e+M_N+>MbNJXwC`@Xd-wI$*69Zv+vo_9&)-(OlM3sdB(oKxL*|ar3x-Wxq|&zopXKnHKL29V=fBLz3f-$L^5J7HG$h;LMrPxsGaE0xEzJ&$mxks54q{H=1M||hbkD{cg?HW>N6}bZ8;t-c`KiYGi-tUD4FFeKiN;bM2FrL@v@Dg0l$B4#Ydr0`@pIaSI^J`(Z9B79ng`DSe=r*(weD;Xvf3Oh>fun6IHY!MQ7kt$x+8w+7;EE_?q!^;ui<3Ffs;)ZCp*uOy+OVZC{R{-nrY*KvcW@Gfd|UYkE(akZZb=|$qs&cMz{q$kA~LF#<*yQmpp9xOuP1#ZOQe|<1=BJR(VX(;@T7=uK}W-+;^Ta7^BP2TMqr(8aUp0^mNkbY4RBfYRZmC8{Vjrn(k2e%@?hxG4jqdL%I&8%^t%G`g|PG`o`#B)ye%$b=Xum1i#H8gO=}vmA%+$4$tX4hi3&@t2VM``K9i{<4nI)490UrUS=L#tJ_jC6>x0>-x0AR7bR2*rjQ*z)5YyGU1`jtu?Bmm*{>!($6Z7HvPXoxPfZ-rlnPK<E`xB*q4MnxmG6K%O;3A)kubA8V9sl5!NjTsBM((a$6XK9kITzGdY1i?KQSSqr~7xeL-B;k51@I@aG3NsMzNhYz=<>^^X3lo{7KFaFUm}qa10Sx@&uYyOe*rUyZlH#9cEnYHm43OO;AZ!TVxWv>M9>ZR|&hPb+st-3e4h*Pv&{!GH&-Or`&7)3qgIdG_tQviJnne`3%l;8quQhM2o@C55l9QF24Z&8ISUzgXzgq-sEmQL8~54SCTC?9mKWh$s%ef<q`rrc^O)8z?;|i9CniMjB?Jh%Zc!uoaTro7cNcYGLsyOah^S~QrDM&2Z|&{=?IHid)+3Y;bFxcje)@<gcENkl6|qr)fdazdFkko_pS~>3df)lYSVFv58;VclLoIG8CW8o>TxNFb;Uh70*$#b>~wKf0q)pB-fgkE#GxD0wHKI%o;@4P<Xw>_?~1e-scTBT(mu&y@|;IJRM=giTJwQ`n!x)VUl#rHyT9WC5lDg6VwQq2Mcstx73{9c^YQk1rbJpEsP_?(*TW@`p<uO(o-V;=7mxz~#OIl2Pcp}AFzH?st9xaFDTMyC(Hvl~WF*bcdGdY&k@pjD`8j7M2??~AN`8we$LX(eeFN{5lwNrHH|YGNCWhSfiM$mviTbBk)c*w3Kk^nrmceD_rJ99z{o9$;*m(4%deE0`8d8mC43TztX3(@NV9F8@-X)<S$`i_0@xt!Q)02&xUWUwR3!<K0<8<jbT}Lp<z(-G5Gn@Hlw(`v^(EpkwELV~)26d;e(ty}CP<ObqP2LW8^1|qegDRMSWG)BlJc>9p6J`@@a*xb2hW3d+;7RLQ>~?6(6#y%%eu|Hq(NP>1J^4GOXcs`)tC(Y)FOu%XX<<=ZKQ8(VEF1ZHYy-4z@{1DH!d%44+vazAthqRSO`hp%igu%Gs%-L?tFo!kEDL$dH5mcIP?z82?0b{bT6>a6@7cT*dyhup0;ZFb$Jm0yfkOu7q~;^r1!NvU;`0b(9VEi7yV}u)!z4BNO;QtYk}8XH?j^2O_N2UM!d4f3Jh}%`$g9+ovZid~{p6>|@jmz+@8jd-YC}Ae0N4{ZUgXzV-%iBD|LV+)9@~F$OHhp&o5PrKIP~`WdK-nla`PSVa^T$=tuh-Zo#f6Xbz+4D&>IV&ce?;>hzj4<I1H96kD50hYTi6KIZLRyA+CRw^FD^0*Wo0t$bq9r4xBayr4mYa%%yR@+Uq`~y{=-FdxwNblv&qMK|6+(Rvz>O(4eD1)j8p&vXZ;7O740JvMnpQ2P@>Bi?h?f&rXxAh9N?u62B0m@kxDKz^O|$-u4EZK7b+?CFRw%bcsh{+<}aa=&>kAf*9(ytcbwvze{;(%Za4fG0|hw8x-G@!OK_!&r?gh7PYv1wPg|=eMM8KdMVO`Kn?X6AP5aAWj)j$hw?RfK+n9Sd=<Zq!smciwP?@-t!dvlO|uA(Dc*|=0G+UAa$5)}#dCa6(_x3shcF%fvK@rawkJuh!4GC{l6ZTQLdT3YI%c#l^5=#t-5~`&I5GOtN%Lt@qiIbP%+eN$gSJrIw1vVadSqXsN9Gef64O9p(%`<vLroqNa%o8?Z#Knigy{1|h$_xyX)&g0TjEkfEw~qrJqs0W!={j?hmwbS3{MKDibf|<?Li{b%~pL|=EB+D(3$7iXWSHyAo!#}KcbxRu&6h!9umZ{|0K$IsS?4l+kam8MhESVIc=VT>A#Y8`3O8^Spj?qXl#4$tm+{uOoCkiF*Y&&Me<o<y((l^aYUD)bn}E)Y1m-2K`{aw)O?<+jo1;`pv%)>$v4JeHhzr(YK~bZk<hm^$%LINT}oS*W;=PTj^OydqY{HozEz%^R@mr<busT;++Buo=V)2rktjHOEWS9G#w%+3#+a!^5iY4w324U?&jG|O3~B`u?+y-pmsARX>$KE92cDl9ZOC2`aUB;xA})*`P;Gj^)5q&}f%JHTry>9bzE5uwX|M3OJ8ZEf41Rhb_^<@QM?L|i@(CznzgnPl2S|q#)-+vm=vMI#;8*+Iu75Od=Ea+851W8w-nk&&Qj9ih2igTEppJ8xc~yrq7h>o2^zSt70%#xzQL?mXle`9p21nznpp4x{3w0X~3}FmBROoU>&VHlg!ari&X3rfx@vDe~_~aP?!4<(;9p(_-VGc1JLd_VzPD2TGgApgHs<}*eNay9wUD~XpT_7#^#DlBZqvHjnUy3=^aRFpbh3UnH$GI}vMPS2UJ@XkJuLsi5&>L%$ez<A>dGf}paRZ{mN=wcp4g3P`Sct%J0lk0&3gN=yO6?MgT-#ow1nv|ifaQ&9GQ?~P#)z>zZF8;V0tCARHuH*_>fvU>4p}{{nLVV(GkZ8c{6O7w#u*7SFdx)mV+9y($wbn~6G<aW2-3~Dy5DPS@Q*lO6X3r<%Lw?EsQ65*(oKuQ-czO#xk4^2BbVt)P4O^;zEX<Mn#BdGmPQ)W@j&@eiI-a^kK8(`01)qQ>%o~)aJ2M~%LdwDhCh5^41xD0i4ND}lYIA05(P#g+UL8k-&TUnI&$)X9?;<8S#<&CQoncdd-NDrz63p`LQaxF@W@NgfJ6e>y+88q{mV=varqV+_im05tM1OQ8v8=FGEXyd+0AA2-GWG6@^wKJ(G6Mz2e7)ROG4r=32LT$T4UGeHFkZqi9k4mTA>dOUshn?-Gm}f$Io^N+_Z<aOhRLxghdPnn|DQc6R-E|M&v`I$LpOQl=Gx=nIqTv_S=d!E4))kwVgsJ4awN4AqgH0iISIf_e2TQj+;sm==Ade*;r43P{4$MG>=cHAsAxQB2VGPIi{$Fu27GF_)sGGI9GSK#Da+Ha+7pQ=&+Fn*J$gWzGkcg`0@~u3AD3Lz{lIq7h{m|srWudbkJKud3|HNw6D{W1bq<@M-w@|A+Yqas*+!d6#5WYB(<oY(|IoMbh!n|A^^@<inTC#O}M8L?jP2D*O3pX$z~ja^5(h0I^^Wjaf6jF1KsPdzGPg&PYk<*T<$UJ%`~-q8ofZ|B`?WV*3kl+vLZ8t>BEU9Yy#@U#2Y1R5}U8Z5#-6WwAp_ixiTMDVw1*a2^DZ;TSVSAME7!UelPdVKjL6n3EI7ZepkvXC;Hhr(akd*?H;CqHoWbg;q7p!y%SFk$D%au?>wSVf}6vTwz~~!w^5cAAaSFcCP=8PEYUP}n)K=P;#9O!c?F!WI`6a6=6j7+Ee+n-F7U>7iKdjwo*coW><iog5_`l>>lIUQXfTssQki&3rN-suoj@*Yp0vEh{_}`i{z^cDN)()Sje;y47eL4o#(hk@Z&-0il;qZ8@UA9HsSf7YWG{(!EQEdV=6LApGa~ooJJaM>g~K1uNTiZi#$3VHjbR4pEhyi!zPy-_2v5>5m*>dliOZ(d1?nz&)Gk(=O?-9n4vr{j&G#s+*+B=g=TkANPD51FgHSoFV>0i{Qa!#b&F{<7`9~bS7>h{DIJGdByk^Ir*I4wKX3?h=cYQ;x<lvoWSGtZ&YzREDA^M07$+O5#C9CH(jc9d9L>o=N9=vH~uvyV&>;vXMnR#Csz^siBpUyQ08yZatFq#C}D4a?(STj*Thz96xURc+K#=0(am)l(o+d{SU79?$p)XMneX)#dC;U|~;esT%-lS3?%^VjLPAQSN#OT;_HaRH*j!L$10F+a$>rB-#AgvI7}{p$Q94pyU;0t>BRe2LpHg2tLxJd-m^$|x);qpp!M8tdUOSR{NEW!~qbm3`Xu%xlw=ZxT0fylwAj*T}_bG`poc$SuRxXHl6wn?+jLE>eQEjtl;><9>c)KD_^kkairVZVrvs;5Ax<XFCM%f`4#th0KOD%8cr^#;ERgIT{HJXIw{G-j!&1SM~)-Hh!qqJwvrY%XSbm1~`Ugk$=%Vw`g$QR2?1x-L84E@ecdXBbnBi8A0%c9wgqAA#V&K$oxeC$x7(_BaY=Lf}>#=8MxT^*9GKcW{0~}vuorW)8juc^%;XUvYHOuK1RFfY3r2i0<m?<eC%F1#gqze{G;?eAg;U8_aK|^PCgNDdPSVZ#U$AmlWmS9*bPP1Wer}I73>oDeX%k{GcN%v9tl|GC1BlSVlp=PK^zq+mj9QlH?2jrM<S645+4FqY$%;t0iLIW9TWM4@t8az=-C~DE>mSPOQC?-HJxVHq|=Bp5i&E`m$Z&3v!Lf2zT|X=tUY>U?TKfK7f&Ka^{2Eq{t-J*W}h_lt_52xnVX=Bmg>sVJ;jfQ0D}`64~lug=S2cgwd-M?S@v;xGH!CYjg)h*yv4rgBFTF}!Zz|QB2MBhLXfQ5%0FV`iA;lab4ii)W4YNBpP#q$Y7nx)Af)i!bM#*KU`qqtjOu2hz#C@CG|KD^%3X5tP<F;@+fZ1|0AyY<w(h_g8K4~(U;{L4HeGn$W%pzhI;O?J5ymTznA2<6#|sPlC_ef?;pqd}Lmx0)Ze!uuFV&MG$D8BIj+xVAeBe@{?Qj`Z4GIhGBvaSuPTk><F}9_IB*O<dZxh(6sTzn)v4hJ312SO&UkN<E61@1zqVtF0;#z2BWyMX7ufNW1Qxz@EFL(k6BOW+-(@G`&88bh^sh-5ah9?f*{Ixp&jN{88tDt;vzzBnwTz5WWx$_>b-Q(ek1SVJh5drU!qwjC<mL+ptUUh*Q3U+ot=7#X)0ZDII6OtVEVV5;B&Fc8iOB=}K-SQln9%*Yphwv@Pt&06MAO@^kfONos72=%)fVwRAMGkATbpnZzNz)#MH$q%Z1MfB*d~U;FcUd;N)JN8(JD{8NaS0J=Q#_ptPoS=@{Jg%;VSu+maas%{WO#X8fDJD(iZ>AN_w@OIbU(Irj(F>g`pgH~kRwH23wsZ17o2|*0EX=GpNAN-5RYWqE;8^tQl!68Om+eLjuc+~U5vX-qdhrg(iAAdo%={v_lbZ?OT-a$i%!VqxsP!of8Fw$Kp<*4-lIVfJQTVlwxjn60qEd@IIciL06M^`2s}k1(&3yNJ#{mb#|wD@h?@5zY{=6tAl+S>yxJ0A2%$NqyLctxh*y$9r9HAW<dvPFu;NY8`%Xe!JBzpu7BZE=NY+u^6$s!kM&ImS>cCVWaKy7VKfkTtzWcn=e)HY;zkc)ozfM>sENhZ8t4XG<iaKjmBs3W^sZHiqC!WHhB$K)9RPNxnZh+^|ZX9Iqbad4oe-5;2g;H$QBKAXtwI8Z$_Ct-e9~!Lv(4>2gxCU6oME5M&7x%PJwQH!J<yC)o#~w#GI!aus4w-PHNl1Wlmts57R1r;2n|ULhYLkfw^X$Z%XGcDmI{JdC*GWsAh~I^547$&uGw`f?fLUo0kFdnILW8>UP8fJj>Oc(y!4!|ggZwflRW*QFjEv6vXhZoEpQoNbdGpjWJ%-CrhYUH|#6{Pg<dN+byGQ}MF%d0~^dVk2#_NImJd5~+I=Rcc<OM_flxEj(GTTAR60{V~V3)wxKqM$M@sF6<i&-4@9QP?zBFcNL2-7E<Rg5~xWH)_ijl&F$#xhIRM_JO7XT?XJ;GQ>9mo<uX<N4de5#A)*&z$8u8LdXPuCX_(gS}bT*qcT;-K6~uWY^*7aS&@LwfNWw;OLVo?;p^34(s$}zy;c7ILo}vZEi1EdmG`S|JZs&CSxA|dBpSXxDuq%YrM4N;iY8<)h+@~PzsypxPXp2uKe_2pp>+{(<ozGUV<b2rhuj|$6*6za6J}lkZj76Da*rx4Jsdy)IAwa!{v>dB27%YxjO-nvJEI>3p%W=$n0`{skBDP=X1g<oA?k5WZ}d9TlW$txmc2scSA^8UwN82LDQ`UGR+bx`^<I+Xc&jVN73U;n>LPs6YsQDK?31%g|UhxEDT;n$EqM)(9COzf=lq=h|A1;j#1#*-T_||YoyYGqd&=(Nu3$ipm2z$U18YV;I5{L7fI!<%CGJT4S5bTRFx!%`lqJ7e5y#^iVN&J2@%(aBOPselFoP@bYFwnWHY?X^!bk>#O`2T^DztAYN8?T^4x}I>o#}E2672qv%{0K;bF~B8<P%2ejoE!^vLhLlrlePRkOlgaXH)vhpkOaEU_sLy8<5jEBvV-r@prpvnbWYraD}ey2I*d@&HZrq<rOlUweYFXx`(n?3+$UaBoG0qrvB!n|Kw|V!SthKagc=$s<jEA@<<GabWXG%f@?rH=oCM<UPLQ*2zO~;G&xC_T3q-D((@JtyCdA^CIt=rzZk7dWXNhT#*y=c{?yyhQh_+c2(Er>VTHS*yeelKGIsa>$h{8q1usr=$H?YZ1EZ1Ft<;el3wxdS?o|1tH!0_c=dg?X&2SxKBC-#2Bx6K!OH}=ZF6abZk8Q%IL{5Eonp<Yq5UofLs`8R9)}!gU-~heq<`t4IIgXYi@IZkF&8y}Vc&tGV8g{>AyMh8O?OyG4Ei>sK%#-ZS@6a$oxUUJK8O4Q=!hL4w(TXywx@tQZKoCB;74G}w$-F<>pndCxx|J?cOB1Bt7uWOLn~9(rW<V|L$G)t6!_dTuT!7?{nP&gKj&Ah')))
