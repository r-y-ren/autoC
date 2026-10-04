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
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlKTaP5!ao&HK=Xp5y3*Sb|k+|Sev)CP)u!(^{Ko0^8NVYD34MG3iBirOwS7k(eU!0TG)jj<rikM(!S7n}zi0}5te}DH6fBMJ2|Ce{aD(~O@>!1GRzkmHtfBfUWzx!YR`|JNL@5`6>@BZn3eEpB_e*FHs-~Rr`ckkbQ_vsJs-p8;1{XhKEzy0&OU&Z(D{^!5_>F@vfPyhI@U;m%~cz;m(SHJ)MhhP8Qj~{;i{QI9izWYmMvMYc5;lp<yZ$C2wm4Ck6Km6w7htKcc=f4yeyZEm^e*E<>*IADXvRKfM3zAqc?Sk(<Tz+*i99P7r-`(GS{lnk=?&A-i{`R6Y*`<H@@cH9U7bU{?9S%P2|9#!R{Kmm9z529tbw_=9|L5DW9{s*Q|K{VzA1`l?Cx2hM_<gf=Lssd|$Tv6S&8IfI_UTX9`Fl88H%y^#n9J*XdQVFCNq(QqTddlp*SA=c9)V=tVsY4|*PkXnaM`?}qg{G^LnrBmF7GRQL+8WOLAarteXfW%beE2aZ2tVgF1`LiqEuqvY}qco{<I<;O3}R8x?OtxX+tVW{?jvgPS0w-%%9w9<>Hh`)~z<A^Cej?bMY*T=1(8(((4~XJk{(^D|YGir&Z|zbl+%+ztPhB;Jwi<OW_->@UQ9Pu1dJoid`w5YCtdd^u^hv)5ZP;vt0@vOws-YW3x-IKTSN#>`$9^>Gl0`b&GxZ@}E`zfA+}w?D5^FAAb1w-RHmi>yJNu{{DyW|J&vNZm?USU;p&!$9ML?lA+Jb?B`X!(MwEQ`Lt~V&f%**Py7Od_e3npJtsbZ_NR5b)Ho3@&nT%c&-NGiw4ee7%Kg;vDfptCn+4?iD+YENmR`E@IDCB&9=|D`eyNE)rwcnm1HG~Kv-Q=V4f*Ef0Z{5=<Q;?j<YoR9pYQc8P5YwB<09Cl(u@~~8SnD#)*j*QMm}lS@$qb{F=c-wJsOuKzxnXffBE?H=RGT~$gjARjX>fKIP^7B*Sa3(gPdG%sp}0huyVQmL91OP%op-5DqFK`>}<bw(-t3}vGlv{jvdD@mn^?+k-6&`-XqG^PC5~^wW4G1+3gFvI<EuY(<XXPQt4d>zpt45d>r}hTb6HDac&s=EFI{9Sbk3h&wDEP-&28qPbp|orMJJG-r!DpFM4wyd>ai~X2-j-)+e;pK4H*vO@w+W<(kXt%Y{C}BR^osm<5fgxv+|;oJn(A3xoCp^|YTXvB&jg34B~98Fr;dD(N@V2KxYYaA*DiV__Z$_Aeo|_7#Ge4_kWxp}u;``^HX9d`CALxtVsw?Ts98Z0YCEKYjSaUw!=Pr~mp6nBfBdz|r`Lvi%<Hx;IXG#8cL2f$oXu7Bs5AYs3+!!{0UW*Xh8;s$FvXr!{^|Ex?=n%*i?if0rsV-U7Q!PwX<iuw7eytQ7_Tdj$HuoOl{c<GCyZyX5ErmZ!qx*<P;TIcK)$jXmZkPc4Z&KP2<7IDk@O9)%hY<?xi>M@G3kvaeo~Nj|Ti>-fF6gv9YU6F7X1<!i>!Rpk=m>LnzW`?|PfIBWVth7aJjCTEW;DiJe#T$bvyhemNceBvj)JJ1%>54(s-{MvSS*0vL0+aA89`Sr3qb@01e1<LIFS_&Yw!gETJC%dwZgsza}Cp&Q7{45W)hekWHy!x!x6%9{g+xO0nK$C9w1HJ0Y{1&+JkK5RKlG7+fe%1ybZNuVn6C|%2ltpY|$CAFr0$J}i<HFt+;MhpL(}3tXhrJWPAVLv#xshmVi=)2#ce#9I0}b*A8srZ&$RBtuP{bbPOgGDgA8(guO>NvQ&)P0y$ns=|z8H5&5DVP&{qm(MEo^h}1!*3m+#VG2`%(a>LO02k-O?cAk2Q&0w!HJG<<)q7Y@Z7>s*4YqU+!`BsuFI*YQG=HvF5qjug3{gLOASYtxd5^cB%9}&yv17vLrigGwaxYWP}EBb3-Tg1}iLqX#XAA>^oApuNu&>1-n!`DSxRLfEz-wOVthhFD3Kf)9hvXalJajU6y3W`slb`J+zbM!f-R8N9ie*UXYm`xOYi8<pF)t>%_1&25gu@g>R+XkAifQbkwRNS<VKxDkj_6;OQ^Y*e0s4;mr4)mv0}UM7PX^Zp$m(WOte~Go;QYK{NQ}oz+2LyGeI*f`;46R{{2c(=Jyx;g==RLB2VzR}tsSuLb<bYS*iy^5y#+{K#R~tKHjWNpO%Nj_XxYL=wjNo9>TRlee`6;9Ne?mgwln3J{$)3rWy(F<PD<4$03dkXqs6R+f*O4oe|S{PGzk9ixs*;S<Gnj7oN?I!dM|*lk`|W1V|46zMj=&iN$n1S0=EP4J~H4px}-=&~X@h|tINDiQj!1mx%zyB?fz2l|oSt_Nq_?xIK>*TdtBLXjvmMYFHr8FLZYOgs;wtg5(fj8`sKzT;GugK<c$bT5frQ51GXQCV1_vjg#18;BpYe{6F9*ywFymkyH5*{B_ty7p{WS7<j)Fnv-73jpnwff?NFG^V}z*94x&6&kDW_zTk3CJ9(jNN-4m-yB(7`f<k+h0-z>SD;~+nAX2E{pEXZp6}W7NLBukiq@*DVsDL253mQu7k|=B?<6a|lWdSWQ~A-;>V3Bh$;-4+Lb)F;t}MOpE4wd349BldS;%i37EpMe{zOCCoz@9Y-aXNw+08uNtMU|lhY9oC=%l<xpm(hC6h`no#cSIk*;OBq$`kCm{8Z*=eJ2ll4v+~6nP2jNmLSmbN}7fyD&&K<M=8+T9~nNmZ>WdD)(<qfF3|+OytwOeSd@2ZYfBnRrNdI|XEv#T3U)>;gMRn@55Il)zOAf*3L|ykJ(WI?K_o66Z1S5%gX-wCG~^Kr#!Nq3WAWLVtAb`=;LlJiiY<c*Kg4+6k{Q^}oVkqZegdoTX3H1cC5XS84@)8b>Sbx?JpPYM)#LrLWH@xd$Mx#l|FUFqQ0Z~03IS%iad_M5BQ!_M0-o1d!&||;{K60?=I)>b<->Zl*~wNE&+YQ#IE<%Zw<ZF0)HNVs@-&J_b0K8L8a?H7e#+_ilymHNa3bUDPS(i_PJQCZV!vREL=CoIuvIE;T<Fqqse0pFmUIp+JT6stQrUr2Ecbhb#}1Np;N-i}vA4yYC{c@vUKH>K$jCIJ-Ug9g)XKxjGwegF^>7J&>t&_N#=b1E&y8f4s;{-n5_=4&cB%SC%ojg*=g5-BrRvRjSu(ht(s3!=W_6Io1<Ae|t=by=MmO*q-Nefd3NIUI+xUEry|J>LmiNXAD9Ue18x5WfJ{m1-OS7z~MJ}eMXtWyQ`p1XNQ25}0!5ip^@bK_%UxIuzN&RH7S0QoQrQqTv`WG*eSiD@W^8fQ|es)>Ey!5GT7ueV)kj??(?KHOeO(|=eML%T3Ze6W+_>NBcaK~cq?jqd(%PspipFaKk5z+^>t5N#9PnVxLq^(uEnV4=qa!R$sp-w!m2b<z@aDv(D#N&FfGfw^^I;|bi#1?Tuh%b`^fenF@n93ti<s_a)W9g3#Td-qW%V3unCYRVkHQOb(pHrkY4DBK)FEvtN5n3%#oZgooV{(e+#BqV*TPzfySm*IhQ@K%(3zQr6@^~pc8_Zm>NT+pFb}U6IY2NlbDm#|W_s}lPCR>=z`7S1lNs4p;tKwT0XpMKKHQr@yuPFPTJ;TP8mw(*JQUK{o#X+a4eW}=6R=Y2i7PW_OiQ8)NHKBLXvDkI;C0Ck8Ap=Xp4=fE7SVH!$`J~1)Bd=>j2Ubp^CM8x@leoTe5r0=yGLcrv@X@id;v=wbs+qUpza*dj<vZKUS)~IumW4w3q`Zvu<u2LZ5ZzNgu#=?u&H91eAj=Nn!0z;#JcW&>L5sq}4%&nqSLklHx+0n|+329E<yb#)@NjRGUA)0(v}rvb@XX7a0!l4&WrHKqv&swHc++$_Q8$6BhGIJ_K6k#}I#Wk^XNW!#Nq=Vy$W%&rXH1%@D77P<@H~2gyTx1FO<DekvOZ<Jqz$ph3Q{-MwjDB4xzHe4p+U0MT}0vdiV@oPiI{ok2feri=HJ{}jm|JS#a*?@2rAH0VrDW8MNokQN!z<0S7>{8p+XyP(kWKa506kaj4prxOb8-{@?s(9X4!hS@CxO^E0i;@P)<9!``Ke$oh_)Th)7Pd3zS<{DB$})6sc<Vu2WHv9v3JIQlS7=kRCJjk0!*#6a2Hy(m(p7N|XB$lJ3zbokP$C7sSE0Ag+MUTENmOrn5#C#C2^!+*l{1!IHe@+Tu?hqS8X-67SVyFc2I9@@lW8$)363S=MVLW94h9Yy&)(`d^+w2=D=Kf9p!q4j0q(Vy6{2lP0T#HELsuG_^4)N#Bv2!-^Ic&(C3D={}4!VW823fxbu>7`770;QC#T&AeBza%v3v=K{_qNDYL!2?LB=NDYLMc@tux0r~+Tpl@YC-?j$&cG@L<(vW8q)0=4Lx9r)aNAj3fI5goL)=uyp(`$6{r*1}hMGKL(J7*P^v9>5+&n#mt(~Px@;)cijO-R0pS@tzv=rnl4!(hLBApH=;r_<sRc^zJ)qgs{MW3p`v)Lx<4+T)`+e$pah*$x0(V<lT1qD<Jw1<Hgi6!3c}#dKxZ7D-3nec+vyBJEWqv!5qRVZJQ6ow$Zu2q<rcXiW>lvbHcx<s?q_*?nJ%?9Eg5d|JS=oI9CFn6%L0)axss;2l~D&cL{{E#}2J9_YzFJTt<YINPsRv-%01W~V}yqi+!DuK*xjIYl9?J}hGOi#WQh<%?`iS3~J&80E+jt(8s(Sg#&R7Lh#%U_D>Ur$Lp$mdFvHXyidr4Rfq^$!#aQ;9J!BOB}SZQVRUgc9z7jazmRebFJSfc|e=?5-;E?whHU$X>7E3OTN{IXW<ZeZ{Ogt=TcU~fF5YWo@Z%qDuXE53qfamowu!ld=uNPiS0BLCD|pnZ#?0PPrSe&^5bnl!%`QK5OkFaI1C&dY?byUXtZ18uq$qUTfmc2IxzxoXDJf49$$tZ{AZ{G5?M@e(9pwtQm`Pe?;D_t-f@L~D|6XMffwmTUZj_KkzVDqkvgBOJ^5^;=*dPZ46>}e`w@h<tRcLWMR+@l@QyVZ(WF&Gkya6<MHNw|$$Wr0-)(!+7ajcuPkRgdj8nprM)f@ARYy^IND#5AZg{z{@PIf_m@y!L?;Z`+c^fR8c-KM&b43hgZ%IkPZD1=42KK?i4`eC(j5MmV)dq=9cGmge4`V~CoYTM?|Mp=?F5+MG6aUi69h=#%>p`sQ;*$$Bs627a12KQ06LAwycTFe&LUHmusUpLn+LrsX?B#bWU%ZdsU0#75?wjkF#^R`S9%wtqn>;cGWbvB;#$|Z2vG8PHgC_@z+{;>H=?bOU0cH@VQ=D}Pc)j`Ibvi2T5^ubHyF@%o=rFf2Z8f%B0O-%pZEPNQCxl8hSSr<AWKspz^+dwj8mL=#u(h5gNXL;&i4eRL8@T66z(7M=(pq+4pm(@|-r<JD9d6)Vf`fLZ%B!H^-|CFL0T!=;x)4dktvmrD;mKBWF5m^U@?;x5V``)`FQu(M0^h1nmxJ@5IIuU!_~DqhsT)5~k+qFxiSmsbFHDok2U<6p`~jSqzr?aFMKh=r*6t7b<oT%ANBiY?*~vRrp+h#iLg(il*T5#i&_zxjiAi>evClp(QbVf>f1Q;_jJjO{3kehYr#*8**0Mo+=2srPvaLA`l)7!hanM0b-n=8&4TLEvI41Do&%~0OMAG+h9(U%!XJ?14HWIHH#D57MgMGy;&@e+gF7l)vI;;j0KWRGD0#T<>xB|T^?PuC)JJZR#nMU5tH1jmX%F_@#pGYuiN@e1So2tF}JfeUgJA}Yu-HFAz^BUG&ScYL^35NZY^_jvA2{g?kF48=b%`G&YTCtGfX1~r&!4=j81bb;=9--K-!zEF#ZxZ#_AyLohUIs#A3XR6pMKq>)a&Y;Or#ShLr+AV*xy~dzM(&^DF^LFL)cIowv7oTjg}TN>Xe<+9uuO!x#zc^H$PI!y9V1P)>*4uC9=s5(KP5=+{D?93>hDck@)y94Z}f6jVbsehtaGP`zHU>)ClwMU(pI@mCp{gf)lDbZqah^q#FErAOH!{aNxiXFWrJlO&PAg#2TYqBF5R+yf$f1`_)DxjlH6&%Eid(oiwfQJ=Bx1Vz6vJ5fY~u*+tiv^4>;nClWP1hX&^#=Tmr6ALC}kP_&8|$+~W$}-SD_ZI1oF1eZ%MR`_g<I?t{}VyCIwp3mDPElQ%U8w6%kD=ygw6apJ>@Bg;}9p0Hwvr=X(k0vt+Em(;MPTMNV;g!!2STGrT>9Iv|Vi+<J5MOHcSs9cV$|9Fiy^y)MfV>$w*Wcr3JAB;R%BzYVq%FESy1)Xl=F$%txhuIQ%<sb`wX|coi`Q<y#$ZLwut|`XaF|@jah_?2Zm~|rBEueJqlc?NhZWfL=13CtC3{pOQ<QfBrf@ll^zZMpLt!waWV>cy(-IPprbAcFkYopap(bx(wYRECLL1EAn%no)BL~1OrDtGxI)z1p#7-;k_E`pTFm+f45!*mC8vTsaV?!5ETk@NZIPrv){`4gg<?sqmNf73i~&^&9@oX9g+3M~)bx)CB6axQnwMS4wIN{y1HsWbAUGQSy0be>b9^PJLRo>Ni>ht6{~hfTUPTqiK5rh+79P(#nn3+0sbdK9-CwCY(p;T#s~8u;dr4z=gi06EaQ@C;~OSn^LtDMx@C`k=25P%t08jUulqPP}Bd(3T1w`_JL9|3o}P*(Nls0)+Z|nL9!&4JZy8P>g{V8cD~VrZg(N(x~xDqrszgL29;Cm(WGaPatFY;DPV79pTu9+6BDN=YkRve~Fp)%BeKvU=d_RAQ{-Ik^y8c+PbuKCMgNC?DDs>BroYq%IMq(W^W^`LFvA2+X#m;H#7y79IE*@E<j@$Ta+M5#JZ+LY^)M-uu8<am~`MU_)T^R%&(14`wE6%t6ie_#?o8V!P_uS)&Mgln#Pg8)nIy$#)5aSdF`q6*TcldSo*Xze*k$qFNU)x_N7+XcUnEkzeZj44qAdRc_ManWTeYtj9}lVnZL$jC(VO{n;tCK?IQ8d8vN#N+Bt@|{dxXY&D}GnL6=Dor)ba@VJnPv(b0kQn9pF+nJ^kev(YiL4Z}dSbvu<eS@>32ctf5LR5SfBtcm-GYZbjU;x=psB`iA)zvg81#5x)z*3lsGR<Frp^?GD@tM^#gH5OY#1q<@f4W+znERb9R*`i{RQ((h%PeFKE-9}}08?_L6=G#VPejAn8AwkcMs(5zP%|q7sYoz7g2#x#dem_g`dh`O~hLMY#!=6Z9fZ%cJF>8|tHGv>gGf)!)HUZJ&(I+)tE7^J7=XAtvr-0{e>p(ol>`pRfyG`(Y@C#I0hTZ7(_i*GSO@B;M;P>+m)=Bo*?HAl`|K{~j`D<)EGiG@F_9yPQfAgpW`Wii4Yc5~v^2K7#DpMyo$Y-#_!ZzY;{B1V2rh_-;e!H$$KaNOp?C}*EFQ7%%lSGbdkR*{64RZyPAR&p?i}s!@P~(fJA5vfmCGtCby?sR~#(9lm3<N7#B(9Y>rpClEVcLsmyN41ja6?h0V^svv0{1m1aX{&@&FI01z-Y9qL3fxM%tdWP;AIYJQBqxK#e+=Y3%nQuCg6c~D&J~+#v{9Y(i9Xe&#3XNmBBO8!vZ7ZCE0PnZ}Izjdgi4Bq;*wXqE&Hu@#HTaRb2B0AM6v;!FHR$6`UZ$9LgpX*q!RC1EkCDYkZKgwjP!}<cht*N%U@6>O-|{C!jHbx1AH;@?+AJH#dscnb4(EGa`>4=jUB_(jMY!{4>I=5I3ZWzeaK0Ikcm=vPbc>3k;eL@+mQ{2z6xJ;=Je|B*ri`nxEGf8G*xNWHH%2UyAIWFQv6TpZ2=gM&(}28AbQO3eCE^5<e%e)(X5(Klw5~3$O35w7y?fBnA)32=);;K2J3$;TYQ1C#+-OU0-}1<4drK&BWDN(8&!*w*_cKIysatTs|za#?=LsR{GF_@O!&maPuL9=L9F4Ralp(tqLzd7By9rFr^#F>x3!n8oSR!e$w_AH*2hmBO`*p`SE5S?x;F0xjClK8~lZ1c0cTlsNiS-h074KNTvs_Ku{k0jWmKAwNDv#jr5RAo+}x6_k!eb29V(omtk(;4ReFXFgKw364018MVj`h(Ig{1-ZibJ+b}5Fkm&ZQiS8{H&9oxmT??<ts%PU>c~lI^zN;)M*49w5?m)!`t;?48PMt-?5^oHZcw?x@=eldCSmf2%*^^xNt=nes2Jy1%24b6G25n(h7BA2~=qa!pHcR~<K4(6|n^@%5?(Dq@JPSC*CPU;yD3CraYJ>9m7OCJ8>R!=v8I5oHcEtT}0rTtPevm2dQtCJjsUw?grs-{5Ky-fbK(xAXtZbA*XVut)l~c#S>ZxP2^*=<GLFBUxG>p3Q81>}w-*}2D|5Y+EmrN+Mlib0rh#qc5+NRCd2IIzOa144dmJP%l1{4o2$A8Obf35lKg$Jx1u3if1LTqiCN9O_Y6br3Q@3bs(@~ZU6D<U&5ZLGAkQEH7l-{Y=RX;5xrT7#6!E~R-`iU>!Q<^e&V&&d||EI2fDu6pdxo8SJt^OxulDFsK&w1%9m>cB6-3*2Zyfjk;59U8oHDDcW5!1aunuUuwnlW#gFPv~`|W~4QNPXt|NKtJt<+i71PZJoZrv5jdE`Mhhz@u;wlM=}vHI>hN1b70t<L@Mn%@Zkz?Y40yK?frFTNazk@kxv72p&{7@H!_>|oY}nRZSito-ZQiZaByw{pJ11^#cej;-n;XLHi~@W+8*Roulq%hoV12+D}6#^sS1N-DlEE)$^^*DXV5jCF5UPgY(q`xIVZK9Nhi$%R)9a44S-q$83da)2m5(AR3HwCTw4^mjg5wduN^>bT&}zfg7q~JY&bx$NoUcY=8@hYKL->AD?B~4@hI5f@u|S0VCM(JyErwO<<w*cuRJ5f0iGm7Yh7bpbf`-n7JR0S^vbrJ_~-G5Fny#vK4o!jMUmIgPEX1@PX~<AWw9+s>}`$r?mRR)X=pV0y!|vqMx>2uR4Gh%DD&ovR>Bw&WSU1@2eVy|u>*bijc9aZbWrBx{-!$YB^*NC=8!MTGht;1JI!=CooBkNz-HBk%`6MkU0|DOVTxgNj)2L`BWHD6CZ&R$Z6Gru4&kEoNdXM9!}__nt)D9mXf)Os?=(l$#HXffkY4tPhxe&~BN`k5O2TD?tvS@W-J#AMaHr{MFEEB>winEKP34zZm0#p>=;)aBK;5@|+egoBzhoIqh~Me{-EA5?VP*qpdNUm6I*wIr=Z$M3&9}UnVeW<{J*1d2VS+D27|9b~R^g_|)8+CbS!bBxtlP{pu<Sl1%WRPW@TP}+5IrPpXx7!D%qu60FRYm7d&`jAn+$TVA1{RB$&$vtwg7rYMdUM>!D$?d#&akJzZwXSl5zY3cw;<(hwhvwOI4E_@kEB+8(BuO%cX;G7Cp&74W&v#I3_P23l8M+dW2z@1kWhLEW6AB&q+m&XinhLvMn<?tr%C?6XJ9|1UygxFv>JoOt$Mb#|)1K?r1U#9@v|B8<6Y^A+Ej<%+5<bhkSN*2rW3qi%@%wOXvsBkD4?t<w%?op;C{#NUSS{#t~@DjXkD|jtbDi7Sd&l)g=zyE3Uo3?D6b5U?%ToG<i3p#Q<AVqLubZ1(WA}#G`=Sm2)*82!jc{1@UFkufP8rE~9`HMlHr07+cg$U|qpxRi0|M&+8=8vOc|!h`f$1d5i$7UG(%8Y<2-D%ujrJX!e9<yv2a-HJ`dyOqasdPa8%3gXI}%7R!_O0f@X0fXiYzGvP#_HB|CjLpk358jUyb4oB&QXKjOyO=^h8O`o^|=%+V8{{%ok@~%FX=VayumW4Os+nI~lcwnV^fR$~^PmLW6QEhlW&$KIGq7e|4B>^4E70Od~VUOJDNuo_JL!7h)EKhIYwRCu`BL-yPTP3Vd&3vC)`92kBZB2faE4LOyvC}u{3GCXHI}Fn%@6bDWIrGHv5={0nm*Z<5MbeoGi-<LmM&`*t`y?Ci67?)jI<&zGfV)&b#ahkiD2|Js{7os^1yIr{X5!`xfO~NYRur<2i|zo+-nt&Kzt&B@Dk&^XGpxLmeWy2;i;LCdS*)gLH@c=aCcj>7Ooet?$Wx96)@M4fKKq{JwAP*^(hfE+h0LSDvw#oezHoZgH$%qUq~;^r1!P1(;v)iN^&&!>yE@T^!?!f~eM=MXTPo{r?j?y;&ZN9(omLm!H@XKc$g8Z9vL;&NE#9Zcgg*F9=;Pz0SVI(&05}FWUcc8_w@t)X|LUC?Jx=`Mk)YZsHiw<!aH!<>^)?DK<>os$H4#<j@T8OMvZN-fu&{SyVef7ipuJAvI~IqXapke@=EJ(1CzWOi>o(NxZz9~s5aBv}yA=^{^oV%V##mB9pN`ok&Nsi?hxEHuyld}}$B6Rb8Y)A_V9?6rnE=ppw1YY)N>tWg7gm2=PXVoE{q<nw*K=_#8u+znvNbG3L{s8##Atj{-xeq8(t5YOaiR~PV@3IPbuI4UQOI;4StEKp!;xf!x-GmRaOdw*I@xmmXLc;>*f<5ntz_`x)4)^E60aaFE~9IiA4iX93JWhqn(L<l8Uw_aL4B)-wd2sMCJ&yOm-MRQw^8`i&8ij+dRH~=iPN-r@VL~y$hgf3D;>8*Zc-G+2Xz5<sB;Jx;MZ;Gd$y@aaxH!^Q<B7+k`y}Bv(cfReUTbBTyYC2@G*tamj#+n3-(NFQeKvkP#lbe;$|ciK4K&LA~rG~v5}Yt5)<_HHHvBSxPnW!bn=EpyajeXZ(yh5H<lK2leR@5HPjP((T=lFSu;-{-t<tiPLBsk;e^WQnyEcV`ncJLZ%a5h+panD{P>Lfv=PLd6zEHo6BQP9qSeE2IJSgDnJQHxCU*PZ3*YFV4J)TjLNF~+(k^NLQ+5<Uc7S%W_l|uYqB11d1rXB`BUdD!OVyjQbrmFZc|12yRFnq%MH}%VfIrQ8x!Q0X0sOhV2$rl|3`XL&7+2<4R1$f3OKVElOwy&0b!n}W$9)J6%R4GDXy99AwP}S#Znz2aX2RX&;dYJ&1>Sdpi^bwgSZTZxwr>n|S`^Qc+LC~FJn<Z~+X9$Y@b2#5u6IdY02o0_?Q`JCm(j-K74g+^0VKY{u>Wdf|4%Qk+Xd3)4W4HJc<Mf#B+_2NaCbOWO91=y;Ok)tUypn!N##RH#D29vfeVm+Cah_(<Q%Nx-L9|pyIuci-h_+yxgIvV$eg(#Qc{dIB?meMC!lI`m~d5xqZVSr_4IF=b^){yg!ook+DKl*I)kHeRUpJ}LxH+|1_mDn9tU)p6=%QqaN#epZgb3zp0HEI)O+&qesBezR)?uWcbGa%hrlw%Z_@}uJz&I*s%i?;9g=ssbC(Y5XctH~eBzPQ?9tx>x-P|3>bL+hmBPee!{ay^?IN(@ub%x355@xlW$47(q#thD|DK#!HQ+xwEU@I5(7@lo9rN`+E}(DVfI_&ia#9;Yk+JQ~-TzMR{#XR4rZLR68jM)W)ArPwRe!KcU=yyWNg8f8>?;-x>G3QY&JP+;Pm^&*nhVV0bofdE&Q~)1GxGG$$TEF&x2*0rzZ(1{&bPGnS7`JAkAI3g#41U&IQ%wcevm6r(z0Kfu7nZ~<>wpa?yMP8pc-eS;~Wo^)s%RVbn=L#lZx!{hO-_3DFsKb{<t)s4es>AmyQs4H<9SDAwJ0n-(*K%?4W%{`1%+UY&wyX=<|TK6wgZdH*fWOr>sYhljKWKK`N{x8QqS&U<`-|knQv%Z>PUZArf!jLIc{(kt)^Qp;BXC>Q(0XLoSoJj6PcsTT31nMCse0rE36Piy9IVKP0I6>1mBNpVw&f)n@qM)M$klG<@NGf%gE4JkLJcC2-Ro)<Ob}eG-=W7i>ZmVHUjJvl|%<jozDgdIQe0#bxqa=i6^9Ypn489@X~upu{0#r#K{d#34$6)!ic=P=9R7*1yx&2ZU8UMK}TL0MgApp*CKKxr)4n7x$Q=%(+560^%Nt1lC;5Ziz()*L5W6loVhio~_Y_JAKU#2XNCNG7M-xoPe*lpD$M+<6H54ROg_#g!2835zf9%BN6mLKzvB#JcYpW#;VF{DN+hUV3E|Keop5}y3^(HBeVNCJE*rjd4Hb#!y4i`()cv7i$ez9JmaZD1U?<(sod#zujTn-EIqpp><&t}$3HjIgz#y+=p!#w0W#@nSxi|G2g0P^#M3MRO=04_i#1`)x8mdRWae!4zencb<4SCe_$)sEj<|`)n|<i^>dkMj-uX)$EagBO3g~C0yfK-doypuhtIzJC5onv)?%B)^hekW`lx{5D;{JXi3g5RmJYu`sBX%1fSwRUm8eD>G$;z@wW2YINPJ2v6;gna9_o|aRD{YzAXsyxU?dSq;N0(^6sO+Q>JbJvqZ5Odi?6k@-1&4An`Gt^)7eZ=8UEaUrvgS$4TkL<27}&35Ca5gHY1b&Q(QyF;8)3x8#JhbJhp<R)Ee7vJvJ|vnu1)qbWXD4O25)JH-hD<2o;)*6{;qJi+8H5H@|`hPfOBJ+0XhQ8bJpui?uhUv4fAG>Y<jnBHC>?Yl85ACwW-2agLiPGGiz=|Y0bnrkUgIYKy?~_njZMcVfd1HH<jvfQ)zxTmCj${@Fhz`TBE7utK>Bk{k%qz&oo6ot$5-aQX~hdJi7vKWY$99Sqss}T1cLo>{KRtUK4;;hyJtC-0HzwO$M9tY=$*pu92B{g8?ko2xaM9^PQp5qyVEyr*a6^%nuL_0eVmu)-9p2ZVBCGKNrKc2rIq2NZSIeGQLz=jIVMSyd}TETfz<A5D(-0Z8{~$1iHo&=uUA;fGBM68a{bU3o`F<RUNKfvH5MdI)90S)mEjzq9zy>;`WQ6VdNDP<IM6c3d^^sYkZ5wdM^wX<X#1k_ZeGdpQb$Xn)2jZvJD(c+q<<jf@&H~T<H$p%CL1+REW-IaaFd9l%%WUf<K?QU!RztK7B^`I1ZOJhqh|)+N!}58G`qQe{fHP%%&#FWa+j>mhN^r8o&!DN=I6jm1tR3_9Z(ueqYu-`?5jHZ4eU$I2UD+TG2dHG`LEt4sCz8Yn~ju!~XY3f;46#5PT^FiT6^-8<PPtKPVvK1)aadv78NXwC5rd5F7uvfOO03aD{4ijT|g`{O_ecW6%av(*eoHXcs+goswN3woaMP!7HbjNx_YOl)eYV23PtXWH;Q&N7PNP_|h0ml0BGga}vQO6jgFHc*Rw)OW^0l3i-^ux~q89U6ogNb&vVT*x=)ERHS(DU*5fGEjv9D5lN7)5U@}~nbHcTJRQWB$VYz1<VhvZ?o@J_1(R8J1WcUiG;t=K#({~D3CX_bb3}9nUElCUnLFg@(IZDsJPEvbA}XpsHofte*m<7%q)~M(X`-x!d?mhVfWvK1@zEi`;DqLNVjk{!k=s-4dYD3%eKehnn^SJ%+uSPvu`jwm@*a+`{kw}}lXz<nBs{kAm)LlY(qLU!Qe=HpZVtsaTaQP#^(cH}9KDkqY(${@L)|P3cn>R?{FuF=v`gL_%Ar?n^9bub4_Qu(t%qwyc4Nl{*lrA4I~SfU**$rHjzw^A1mDWr<Mful@xt;qijNskcxFKMFar$Z*;sgDOZ6nS@qV?kiRJXz6}YrxJB)u-&%i?aztlA*Q+N1UjBUXk$*|_l+hnn7&;{Zg?4YT@SW8%dP67{|1TS>5=+|Kws}@=hS#jUt>#uX$!bA($3!V(Xh-U!av{H$`#>{VLswV`n;UR!Ge^%$Oal9TL3QF|`>???+bm#MoJ8!GnJ+`VyIC14K5pWDS`u+xQG&0vkQ5S%qU_uAPU<h9x5Wa>rA<1F-by*`bsE+@=bbw6W<IWMYk+x=L2;YL-s@PuxVw<`JBL{3#AxcRASjlo<<S-;#=Y|+DG3`+(A;f4Jc#q)V^9TmJ%d*ipKC;Hy0X?LTONf-2;^|a)Zgh1;+Vy?D0K9pL(-<Hj%gf^eY<Y>Xw}HgHr`HDr?y;?N#9L?7`aRG#8Y%KJ*LxVU;M9@;kYA7gJw$$mC?eDLeu1BnBK<`%*#+z~Qg~r^F=m-YJ88;%C{SNJ_wlLjlggBqI3ef}osh$GADKk{y5)NUfvDxgjRv9XP!5vVj^4+*zk@f#aRqAK-vPoz;Mot6&dc2Bgqxv=TuA0G%Grx>AWyr1^kixB-If5a2hHdFnlciOC?grv$0JXDUU}#XE4dWS=p-<;vta6A(a;!JJX01RI~@8QPUV~JL>+JmgnM}I&94vQcOSprX}|mahu^;Yzh5V;?Uj|pnN<?g21A`S7!vvinTjSeq7%<fQF6dsCMb6>KsRu4=%5X<nK^pb9)AvW*9xWBU5l6o71lJUu9*fk)--6ara_Z#C*m3w6%*Z#WMBT$KCP{xRhIAiyZh`oqR3HBQgw)X8_h2Q^tKd{iDrRlD%i~1-&C6?M7UWe-pxAlG0@Q$1HH~i>O|NrWIoV+mYIR)$^)cHlT(C6uoW7wl~2OJ(@h6z`v=BqBp$z)>87e}%VI!t-p2^aU-<O${KcDIp6Lx+hB{=(hbAt1<s^^Tw%A1qj*UrQc@PhAurVGF+;~}pCe)=|-lZHE+NU(Th7-pQT5+JoVg|be9s`l&&ct70W(Tu4>=o@(7DSZKSP_9wHend`f5~oU&>B4%T8(9vhmR7VCr@~fJa;{BWF>3t=f+dBha*i%HjO#UEizh-Y+WN}RtGV&t`Rehw75yT63AY`(c}BoP}cCVeE;Z^DzEx)JUw-KLfHas4xD95<~ENOti6r!tN++AMCMr@|9ix#?zj?U$ZM3d<e{8pPnJF4-=q+Ajtl7Q;mU6x2Ff<eJMAsDr5rfoXbNc6avTw0Cdp%A1j%MInTk6sj-c|1McossG+d6RDbk#?o7u@mi?O>ktle(eWyVrzZIRD<gjXc-xe~}-4O?Q}OH|}yH%8vYAZbnGX{G{Aw+P5IyQA#$za5~58-@)<k5z2ixZh2@`Beppf5#QZT_gcr@LhDQ=D~%?yap(^gbI#u%FIU#1)ilH@Oxs73|eq#C)x6*GxHM^g3z=p40{^fXf*NSro2_L)jc^L&*4w1lKW6g)3lc?70Hpez*dkD;e0p(%cduMjOQ=+H4IJmr^`$e|0n|L4yGd?vxluF8sZ$!ZBVuDJeO>gme3<RY%&`jjr_DR=}^G-F*!vK*v?Ct?t@k%E7TO1>3ne5(Zs~Emg2B0;GMogjtX+ddRsAhQr%~&!wsoBEQ%(NzC=&(R^IouCm3kvy$Q>{)pG>TR#fmAd{(xJS062gY4h`eEH6tQN%0GD><*3>Hm{IuyzO@L*=|SPb~|p}JOl^msX1ZaoxZAq8Zp^26vFE+@?Lj(NMEB*`0L^7aveTzx8cghw>T`Q>e|vAP=Od{I1jN$TA+6Q=xuX3I}-jJGZ~UC8^gQd_GMGDD&884?Wf|OxU~7MzOOdzB8l8bDLc@B64cFinYy-Z>8udNvV+Lx86Vmyewi9h@8TYm)tT=&R6zUEkFg^CO9y3bZEY9S9s7y7sNM_vUMLFiTO7U)m7ZI=!`ETZql$ue26}AZ-B>z30O;m}{0-0%k3Q_!OO9htL2lYkf4;%*x0GY6NypZG81Qq6$Bv#lo>#4+BFPSwOIcf8w2j=p;=xDY_uiNP`0{@Mw4zW!')))
