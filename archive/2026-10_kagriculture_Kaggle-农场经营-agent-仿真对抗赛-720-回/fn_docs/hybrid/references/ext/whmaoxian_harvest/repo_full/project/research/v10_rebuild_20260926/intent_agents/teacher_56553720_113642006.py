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
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlK+m0m3apk}Cb3gdqJ@nQZw!{I4>cLENiCv;05YU5w1#}m%3qk+Bt=%OjD>KaO9J7e5tm=9aMYJ)aGCkbQ?cDzGAMgJDkN@y@|N8DP+WU9^_Q!wypI`seAO7$k@BY{S{`!C0`}XDiyMO$rumADgkKcdyo8SHT?)|&(KK=gP`~3C4|NDRZ_kVf!7y13WfByGB{@uU)@gM%}>;Lng?{`Z7@^|0=@T<T5@x#xbfA`bJcYm%dcIA&heE9C;?Ppe?@=uTZ`(J<j@cG^Q`sd<i7ys4AkH7lmIs1M=6$|EmK@kf!yWqPImtS2@`xW`=clS46|L}Le{rJPDzqu$acIodweE#^;MTzizr=3sxe_!`6zj3lluRg6@t*9^W|Fj(Y-tYVKuRnhL@p5rI`TNSn?^~?}*`<|HZx-aurw+UJ=}$QMHJq&l)93|r`Fu~;q_j@z`(iG!ZkJv!u_3(z#ad!{*`?Q?CcbdhT+rDry<X5oTF~u%XBTwc-5rDlJ?wo&T+mb6CaU@KC%g3e2gy>2z1XT<di`ll+LW@n*rr{2{b@@oDgNEFcy`Zj9_CM$TD#aKinY|1w7(SVFc<f-Z2t7wF1`LS#9ht)v}TuHe_EGbK=(o`{6Z`5lXszAmck3I@yGOjS0ya9W><>48qmu<JvfK7yV$>AwM)T`Dciqb9(L*Vr-^%+{b`$Bdc9t*me`js|5f$>?;cgZdwlolhaWzE_xW%C>f=wJzyIO;|8e=ho9tHTS3iCF@tu8PsnF+D_VYU5=oO}|eA>1F`|wqtCw_s+yCXJb&519d{b|!KHFm_yJxc1!tNjH&E$BdjvYrNh3%)4l?gH}q%89)VONXv}9lqWO_fLwaUut3Z>Be56f!<jA*=F=-L%w<W0x0z{@{B=#^D2MD*L!_SoBhz_c9HB->5i9(JKp8#HXh-0Bi}S^`*^m|m@+?-UX9C=Uw`=NzkU4q^D!f?%#XN~i9q2tIP{q5v98DYBA3W1<=iW;=hMKz=5{%ByGXd5$djyU-GuXGyS<yH`nitQM`>`3AODx{M{W#|E8;U8dCGuM+Pt(0sAEJs?FYMBX^C&Y3q8{5^jL-;t!(^NKJ$aZDlb;?inI7@f1>a1@{yW6M{4pPsfj;Q6=18=gX&2Sn>Tudd$SI{jb5^{H_;YrX-2fAS@abwLv5e(%q@Dj(0h31??N)XLc@P9SS2fa()N7)652rY(|+T^?(df+@cv$8NSVGaN<XqTv`A3PcjgbU0u5`je+lX0(IE(Z_u>Jd?^oNxJg~JB5A{K#Qkz|IyO0x(oBjOxrw_mX%a1?(^xxkBH_XJpa5OfgO!gN$%FY{o0aZqXiEg6ko;9n#YsS&E-QTtF&*{MYx?OVnrw#sI+km70%xip3{<c<T^Ck9lE-X;c*fy^}{=5W(0F`sO@D!iH^K=O2%-#zuUn7fWG8<_S&+O?3yUlMrZ6@>Fm&zY;0A0r13N?<+?k;~E(dKf?zB(q4TUO7vUtgRtg(I~V@Orz#&x}FM$|L0HBNUbh92{eubzMYmE5Lg|URJJnRm^4OvQ)pUXnfDzEn=gm6WZwec}G2g-&L6s6@I3?JTv7DpDFKl1pMq<zTxnLWd#zR{LBm>2g7%wBHtq0VPt+qY_PGH+nb-|!G`2$_gAB@d5>tJ276VQ>~(9SuNH|OD^`9)J^0sc9eN1R5K4X4%LLlN<#7Kbk2aK{Z)2}OGsdQgH>x=>BL=uiQrop4n$vFE1u(Ht_+M@$M(olvAL)0weBBexUPv^1A<^uG#Otv#whdIeM{oQ!JbcBKujS=l!<!j_%s2L~ne$OH&;~b*zkI1m`#T(*O`1z8w-$~3z7$}r(G7NIr%A}w$-2c{w#(aIyR5Mz*&Z2aa)U3KUvhJ`i3<y{+h^<A*PVC!Xx)HH2rs^@wTY_5E|q$LDrxL9%O2Dw$d0i~MHCA+3%alitg+0f<5%RcSER762GHy!yHwjLf2ml2BSo`IRixmTl5OYH?4kdDy?Xz<EUAvs(|*0WX&1{0<K}jsrMFZ%AS-)WKT1w3U+y=06q#aIhy!l0!nZQ*S3z1N6SYezmb=8Q0&w45f?gzY+cns(YsLWd`(Dm(ztBSW*p2SvJKdE}nhdn0R;WN1{>!B}LBxJY%fCRk;mflF`@qdESI6#`CE39$+OJok^vkaW{K#(Ct9R?m1_1oXW!J0i-epO0us!zcRklYF?*BLKB5eUMV$;SgyrGql`VN>kq8HRgG7nu;o#)41>a$A4<XeR;{14pzI?GYsFNI+L%h#K92-`1(HzV62tk|XMwY5CKm}_8UcJ8Lqq!ol65k;IoWd3{F!1G?b#9{ia%ZltEhws;`<nYT9khk3IdhkBI(2tyUJ$Rp<E-J@<J$zMCs2q)^t<D&BvIP;?!t*s+R0?-vv~xLLUZ=7#j7=(XlPl~vq_N|W&fcXbdzW6ZyYz#$o<nXu2R*r*(neA_+r0f!*G%u~2?>1Q<|{0A#|6_%byNco!(k6!ZDgcE65IU>jk>u11!?1&0t`l^<5eMyXBI$z-0P6S+gZU`Z8}QM?4R!b@;wjF_w0G4dSpKscCm8gV4qg37udr$5P#B2&q6yr3muT$Rr%3Nbln{VIab=LqTP@C*Fw!gXXjLiJN?xz3z^fy0u#^MUuf)o(!%SFx7u`wpexTy>%7ju;n=+$XuBO#2{^`w3hjA2#hBfpfmUCT&NBh0{8rXyJ(Cy64v<kL^AaL6FDgG_0!>|@$(eK&+fZdCG`cE@9zDsh&wUeQ9JlsLQyUA}Xerdj8k|fy4D_coV<tVs%5JH(E=-c70umCVtKWYA!*AZbACaL|WdtO=jn)S;CdVaAE`CdMP~Tocw@P9hTIqLd1>dbLDoF<>3>E5q+0hkzYw{e+6&MGdIsKY`YOin<)(ch_#O$rRr4Y7zSvt7{iv3b`d%rAM4q^6wz1l8ZmTVlbyI-mTmX+=_-Vg|c0Ez_^@alDV3|YemhImDv4(?Oktyi0!Y6V5zPFwb)q6W4!5n!grkc*8cePo)sAyf0{YtiJdMH9ak?Hf>>NNu~5TXw)}Q5<r)57+{fHoH_ho4ZsxxHPf-QgzK;mP`&7-7i(=XVrnKgj>ZH!8y9rtlf*Ueprr=k|A2?83S*Zja+2ZWsvEivV5<3hS_bmUM`{Ky{uFj>z5_=zESK_^+dcZv2PIFE>#cHdhv5ljupCJsxHpUlEsaq_DkUoZGv<)NJ}?pDcs_x$BCaF7hamtcxlBrjJW8SQ7e;hc}A@Oxcq>1&_LhfGyl?IF|8f-N5&K<gI0`O|M-wQ4IeYHct;}<%3j{VO_H}Jsh>>t6eVwVDLAvq{+UfCW;T~7z<+(s&+e5VU&>nqIp}N)IoJ-8&bQ(XP7ZSqQ^rL>CvC*2U#)jI)^7C4fQ3Ka#Y*ANOZKlnefs$$B)}S1_wesNU4G`0re)*ix^?rBn^e0T^3VNxu%m7}+n+7}+^+}Q>f+zuOKg89rk4S01epa1j2Dy~VIKKvClOKx%kv!AU>}>7CcDJ2EX4-7)h@aHoF>h1XirFaB2p5I3>PIdD&X&MIptLR9rg<p18boG#aQ<TqRK+uFHjch<@VBe+M79_k#_5>3}~8EGQ7QeRt7YaZ@^txQMIt5^L=H4p`COrvEn3`Xc2v-Mf5E;l$4$5o?%?e>s;>S*?{z=;zg&ceW}=6cDpZ?ro6kS#BH^BOz53-Zg!pg$epHd$f(rvqf!e+rI4X*J*hFR$Z?Gb-r7l&sKV-p3fET#aeqY)lxaB-pHeJKTN3MUTlr9hOVaC~zq4bxvUJi)SP@lE3Qj3!G8f7hSE#+QVbj$`(p6V|yC0A(im=^JdO}~)fu2r5edYwMSoSM)_hMajP8gX?Q2etm6WQ4s4pf)CA$N3u0iQ(9tG^OTh;xP5BMQCF>i~HZd^!5LfP)H=x%D`?j&YLEy-yslTJ!-a`gye=(=g$@+GuX4)JRRj)9MM_m~Y`mWo#uXFO`ciZLYo|0Ob~&)5zTJM#FoJhWDaVl*Z9CGc>6bsREO~qUI2X;bv(KI!o&m<J}=+zd$>SnFS3L`vo>64KdiS&=3QmLc5q1kL`GQ@z~nHhz<xehG1zZ9T;)}m-XX~7lAik1YUU&csWw-P){;J@5qwfFHn}OP{8+|D8@GIDXpTp-7ioyw?YA|x!o5i?A=ZauWP8bIAQOTI<09yxXF8;bPg{W9Bn7xXgh!cc1)R$jJA7hv^`j}s>RaNw%Ev0zQC10d>3!0WpF1PlKXBC)XAQ?@%inp1I9zgR=&y3_RL$TW#;LU0QvEDd32g%84QBVlh!J2G&3i~c$_8EJkFv-OlI=xc3E-2)h&gr+cM3L7&JR#2H6qI)@*^qM(5?6cbrx>nnnM@z;*^ntuRk&fUyiotuV54L99(cr)UHe?<^=jVxah>z4kX663$}Y7;OPqJ!nBDcXowil+Ix_CEv~-quW1qnW_<?NjcmCt+9;0ps_$@8GV&z^i>oY-JhaD+E~oHaqud##XDan`|yFpSrFe)3;5(kj+qV@R*pwe9gmG@WEEalrv)3W(3ZUx8sz*^Z1s$CkKZp)?(sqaKkZV?aF%UdwfEg8-tj8a9#S$pd}ArzmnFBCwB=S=%JZj<Z;f#lx`mV~J8`l1?)y@RZ%)|f(@M5*QfeW=*ha^x#|KNvdueGn$K=j-r5F2nqK5(LnQ`3A*|EKvX;JbtJFi>hcn=^J+C?EoKngMff@r<0b<Awq+dv6-7_rF_&{j@|aj#xV7WX{|#ywx_r~#tMmJkxqYv!R>4cY8=$!#YaFol}@BQAc(oA^tcOM+Q!31;UmZL$owf1?xy?Y38Vfm^dxYI|?vpv7(SQeU2dL*_k~lgIl^84Uw^sRQObA%h+nM5$h&yB<5vt1%?xO}}`Oeo+Hnid}MhND5zk;Z+xzzY!-ir8fwkpwm~tv|(p2?6lRxpxrx{U2*f<0v@5#CX;x3QISdZ_|68&zwJ6ulwcT#1~}G}LMeIC;{sg`_bc?J%;jPwUb&cg<znTPi=EHKntY`D#^+*XPcBwtz-Z;{M?m2g1BE*a3QrakUNL>sM$4NrEpIA8c~hk+gMi=RZF@3<CW(tD*QMjUXi`YHdmdS9qCh^R)bPnJUIUW6Alek>wFp4Md-w2q7?NCgBS;0NMGSs#c}&S|C@d=(jzf~4-Qu@C0`ux@8APE|!FAU8!#MjY`!sOk-@Yux#TCqcu3(AGyeivuJ&5~Xe)50@`zOb2CF>VDO}X$4*@9vw6phc5^0FLqa=AaNUP`#~#rr7X?G-o-zZtn{#E(u#yN+}0-ZSIrhWZBA7muaOh~{7s%^5>97Yp{wB53IerMm-6IxeS}6%&a3@FVhcbloLHd3(BKJlknEg0mdz6&es!pC7?FJeF4o`)aZ5t1U>rN~|4=gtZM&Q0*XiJxj2WBVrWcgel&5&lM_ib6@GP0qLTpteJ+xN)QgKc32e5a#HqGc@%WJr+)tQ+Yg^VaikG?BD9Xp6L}4^hfJb%?Fonp--<Om241f#--@&6iks>DQV9`2pkMXPbnqn<L;L|*Q|!}3b!!SLet6KNRKDrsb#O9qLF;6TKTNgqkJt`NL`^DVcKSnGdHO4JES$NuD}umAb3KP$p_32yYhVv(=pi>AGb(n8F?ruFQWMJ>|D2u2wx(SIt0W8hr#*8#TG*Yx^1~Tkwl^FeRMYkt+38m{-kBuX?TV?F*k>o>??lKdqv(@EkGb~ZQ`gg>9vPi=X?a0(gO^~_I3s?GhM(Miktg!f;nrCAJF!Cwk#(|%D+<2Tmavm{gxz>U*vuQkR-Q1~dBWu610^<^{8@O4sp=5F?U7Xw9!X+R`NE>|HHOMJmJ2ypD&#z6(5J9i5=}_SK|)HgS&*jLEtW7n?Bm>2lVM#zvPUH57K%+)>bFS&c+=mTnZ$+0jT(&`^&oCEJR!(@MpxeWjIMl=!@JIT+vgZOMUD!QqIq+sR+a+MSdvALaV7@KnOH1mVvBJmWRdlN09nVCrrP!J{Y1WaAw~w2+IsR=jCHKJK(>eoFM!8C=;5rw{g)$nw<8?_`e9Q4qJp<X)Gjyaq;JP1I_U&^G=xrHSUP=W>GYkY(+}2%ZLvJbE$G7L0ELUgwOsaQuww)o|A?K(ttYJv=0#~as3k6M4iFFT0AT_Qm~lk49lMF~fFsMgs1_9)4MfPVOTzUu2zqf3#|dqoyI-MOH}2O68{(v&Z}|+2Uz+2@eQ?^aZ^QYpfRP-%@%9UeHldI<z3IuCE_~K>X8E+slQr!yOjJ~8fR_qt0h?k9yF{!Y%y}iz0?ZMz^P0Bl`&B=eS&he|ayhF0;|<!aY|>PW%@MFA(>H9PW9G>s#p8X^Ual%F>2w>93-Yy)%@*q`8(H#;pmRjF|5Cki<T1r$#}q5J4Mk@V*;XkNcb$xO3n)4LB;xp)lZE}sfR4fJgOpESxxoOUAR2?fuZ@LYdklUZ?4)F|lah^{Tp(`b+STevd0PY+HN+p-MPbo5m?PLd$Lq8oKDzoLb=nH#m}vAb2SLi>i^p!f8@z)#IS&l1p1eoYo~`?hnlSS?>N$?<Z|dv=)Y%#}C-V%JMhlq_od^*OIhT)TkX}<lkyz4gDl~U-SfMBSPF?9cbqn690oo;Dl$m*3_>B5vU`$N~NvxpSpSv#vk-=cd?xHo;(hlb^d)L4>hjeH>uLj70)}?1a>r%++9i<!rzU_;CK0q(McN%40!(4cQaHCbe9;4FbFe*jdO?gX;&E3GJD7dJf>D>0)X)topU}R3TNJ-i<HI-81RZ4?bDJ>rHO9%FLs(otE3l+$#-q~L!?bEmp0|^s;t>6+Q3jc_eHWBJH!y$<2A_x%d;mP1X7hPltZDUGWFE(o~3`I<vAr*)`*c>_L2uV>|x8pE=qfA9DiRGed#+Csju3~c;MEKZa!pFf19~Ucp+=3Ah4(H=ym%w!1{InHe=)Bq^iYJ!d5ij1Ka$}uAOQBgKRc4L6?q~*&q=PrinUOdL*iv=lXYLN~nhe}O<ca-urkaD{ddQ187<6CQL#?rAT0hAyN1ZG$TJf;)yzlJDo0qj8$zG?Ge@5Zw>gae3O<bIIk@#mVeo(mC0gt!+`8OIlFLN#i%egp3@*YIVFp|eaFQohQ36njAu`Y%U#+hvxhT+BCTOLS-US5F;eIRcLD$#xzlE!_syo$UV@!K>LB*Hez0Z03XPpL1gfkI&o6bkQSTRc9tdv3mZkA*#Bvn5-w{tul{%EQJ6sWXr%Dwf3suK0WE&r5U~RoQ7&APvqpjjH@Ks<4*?JyfgXp;|XD+2Eg%R+l5J@vHTImcVxJ0OBqq7mLHbk-PwX<)-J)Z9EPNB)pnQqZk$nXe{?WY4Fm_$;(VPM-F*Oco4ac-D5=ZB4f6P>C1P1fljNw2R;5?jsU66pC6U@`MiVVQaxD$4bKv|IUYLyjDsiQEKiughKC8@6q$+L$uVj-7rX@=EbY!GL&Yr>g08$77Z@Do%xjvGV}`zQ3I2XQl>;kKn8|>=T90DcuR)?%BC_lb#&ANavlnfr*`Vec5p<Nql2+tC!EBK`<JjbAkx|w(kW6I}#UgoDgUPeP<RsZPL?znnfg)G?WI&?Lo-uQDO1$D4u?M%{;_|B~<i@C4J8VIPNaDpFB`7R!wC+P@7A9Vj0`mevQyE`~$hS(2xsTT=&5Y4fod!>)Sv<Es1&AuoY)Vq7Su%R?-`Cl+hH{|d+Q33<18Z>SZys&n@WnqICn<zYN0Tc)LPlSdYdA2{)x{7<V?JXvl@*&>%T9XDo-7r5<Sn(X+7K2{%fLg}4F?}Ek&Vlfqr56lj#rserZYw|4{O)wox;*i>S|m!Lii8|w}pR3aSFS%t+=yW@n#no>>=b+a*pVSWb@`4bWsw+s0K|NoI#@E^4NK7>}arLb~IQ@Y&57H7l$#-gK4Yi2w7o&Pgm~g#*4@jZ&y%!NvDl>Iq0;@fh?3v9_|zDrm(-CYUsm0;;!GY_W1z%;A<a}f~|ZuTr>vl+<*vOiX$&Hq$h6{Rih9C0x<p3g3ykqU2yXui>E4Qo9x&_j9Z1SAZx8U%Hz^)^mQH=_Kef#q`%Q7AU9*Ii!CFAzxh5G0C!XqR|4&``VCsezUTn<hg6_9fLUhfYa}lQS1c+I7iSvu&Dy6dyGD9RHlD(ncvFSqFf5Sa50`Cl;%$SI$2K^jvKP>vxMZ4*s<AgSeZ3o6&9sqIv?0+=WDDI}1TDof;NT07$+~Ca)p=A5NdW9DDmG%M*mR&`i<XPabEnCoVuiQID!e^b=F{ypR4nr%@#@L%`_|n&c$<9L3<PoWFyqEBhm9BPYQ!9LPq5&`nHE$F6t1i?sItnS>XB0Km!qAi{5DK>IRmc`&dR9}#SsxX$rCDYcv{c*mIdcl_sZ<6XztawV^biLO$W<0J;kO#IanNc!8tYsARpbOIm$<qArr40`bP64)FEYOGbkpjD_^WIJSSEep0llFB0?ZC9|EDl+LMR1Hy$$1r(`m`O7dpNPD9(t9dwNBp<|T8Tn4ne^x(rw7JZkNt<W4+8V_zP@D^<UT7&Hyk8wNv$rPT3*xC$_Gz6kHHd<vrY4PR8>+3VGyR5u`veN=esWqN_j~i#-pmfF(L!sMIn)wvUR!24S2?4Fo31#;TI5a@7dyL$N-^hLPkLb`fB}YED2DTZBcAz_+4$BAyB^k8ZXz^mB#EXpp|2E=&<+6R-_@;B?Ilzv{kP_1bWzZD?bOs-|G5Gb?Ht7dkhmjL99~7>5H#OF~N#-tQhXfuY8!Vf~NX3LFJ|-fl8*VXTPSxe8hxsum`nJukFz8zQMba^uc?DkKS;8+j4MX=z%Y2Ml5Dh7;Cvsywk^AYnd|*&EGzW0dbP^x^R}RZ59lTNb<ZW{l#l_M3iBnzwgHAprhK?(J#$eeIizP<{{ZwVnW#_~H2G7tQ{1A7bcKn>D+>x0t!vl7JKbQ@mS{FJ9b{!7F^>PSL9ICt#)YYv6ts7rE06P$F0s^AV7>KqUAlk-)Xy>`b56D6SMbR41NF6+iws?Fi@hDn31^pdSPEKVxIn_aBuL$vgC)v>Q+MI(vdc{M$ue9A?qscaM8tZddQkd3N9&5B58*$VaTIz|n=jntwyUfPru)#xf)h7?FZZx!7d=7+~2qe?qII8+)I>dn6ix%G)VQiW$-2_u^_pt|kc#g<|b9PYf<o>2R94#E$;NehA%Xh-gUhFjc>EgDZrocK4XxWF|ETh$<z&g`t6~p)(QJa-V-uhwboC@-G02vbTN*C2u3gA#32Gz}NP~B-jWUyX*r<t%8K0jWA1gl4{e4Ow&qY)aQ3SCC%hC>iM9fIHmcbcB|0%K@qd%#>{!otD|3p0;nXUAO+l$y)SK6{pZ$fcOj+tdBK+oyPgnGvAR&T{zqI7YFP_sYpMU-M8b>E(+t3nmytgq1vTCJHxYo^Dqk$*seTsXffE14}VfQr+J4l&?ci345qbwW#vS%jS!1=K10>B=;txJk|mjLh)ot<ctk~o>5Wx4E}Q(hhp#?ip7rx(xaq3zX0AD58$CQ=Z&Sh$&Gk{Ry~}!BpYiw2y5AsPc%@fC4^)0^0VYXF0nWx5VO9ojI$l(M|e&?bVkz*L&LVpB-UbFXHRa_^(BDFd21&}A)`!#VE*2;Ic9iB@<hX6@aW>g+lW+O9CP<YbxvL~y5zlULTJH0UWD3nTtYv1WYtFFQjU--5i0e#ljI)pP|iSOZp<-VbX0&A7RcFcR+qSRd%E!gQ`oC#gV}gDq>Xn&3dZc360dTc)UbHYBOV2uu4t|8fiRfFyB=Q_{p$O_=3)^@VO20u!I+{R1lBd|uF6yGj`K>%v@B5XBQmdpD;^`kZWldWg2OH#h5dyOEUlh=4lGsdTS^{{nOEH_8BF2omjg`!7RxizT%9-GM<DY)0xnnQ%;X_~)>6f9E#)}<H5zZ?9g@lmPXq@YpVZutn?5lD=$AJ@{{%ok^R7UaXJzFDmW?;^J2HxK@W4v<04s+nKQ(qRM781hJeyqs6ODj$E(z#Ro>0DJH+IY2JmI(HWr&mB@^YUkFV~Sgvhb-A)~8m!Pwjl43beK+zsePr%SPXPOP<26S-Hb-ZQ~t&H(t)X;dluq``E&XIgcXgtb|2GOr%kHGSG374S0xp7AGB=U?sqvYMx@vW^@$$MNj^wlI;R0Top5c^JUJxI0Y*T+2^1;K-intBlg$2$yX(Xg=vPJcfz0a#4<QoEuO(@$#$b_YGdl_)y8yaT8g~onnC~}pUZD@^}Wd@)}9p7PPT?}?a{1Tz(;c9;j`rM&5$uSsrjgO0U0q+_=o{ny@=4}u6DHL@I5Vl-_yeTp31tLdr4xIJ*ft*(|XW-V|vhn8fBHVm}rf+h~GRW_Q`KzpC2bU8={aTz;Sr+`n}1zZ6dz>S7&DSIQffPf@-HY9CnJ!p^`tYw^5iWH{U@dQPsr!WDZX`$u3K3vKk9}4;J>Gb^+S!G`?eT*dccw>mEL=dw5c9LRhz<c7GG$K86U_;rp$Kc(X^uTMmphCG_c-ZQ}Okcl(fjw~BY|9r7GeKHNZM=ok#zc{~#UdiG{e=R}dp`s>E(ulp&WwXDBhto(Wljztqc7A>}hg@|}6{6fseC(Xm+NL^a*acmrEetsP*%D3yWxQ9m}(}84-?C}gok`el0;SGt~e?#eJ;r!6*7}l|I3W{6F;>D+lr=S&HLE2nK*D^njzM?5Cypn0Ip9W|w5MKuMtsd5nL$6vqcxDahRmE?k@u{6%En4)fYO`;grp1HDr4ARy)-Mke*SWz;$HO8!DGK9*x&S-WIfM)F>$dbg+f<~u20xf7N#RXN8XXEc=uprZq{b~*+(Jow%whIriPqDCK}$@^%Q6z0gOSkOjD*HVY*b&wM&%<m3e!Mhg5DXUm==#KxU{5;H!R{U@bh^CKNY{RU`Xb15l92|#17hVHY#i83B+3-O4jM|AZeUX867i?2T3nC`|!gO4$ih~t~@`!;y!HzF{dQ@5#>aMpiZ=V7!LcEkSJ57OT@%!|9jyZU9@54W|I(1OO$eywErnP3LrZ`GueB`MlVqrlI#MAX^D|5iqECWrEJaLy0W!IJ)VarDoO+XvW<8Vz@KKl+-*3H0RCKF1R*OIgOT_x#+5k+l|&w1XiN#4NxBrWF0FO(xDUZ$d3z-W4g649ZHchR4L4!lOnACH+|JRU!1GRUu-JSFD}z_U&I3c8g5p_HTawU@C!d3MTL4o8@173s`jpfKfDyFRJ|~`hnQc5?5nt^WK;kP5`|mdP|Mc;uT_8Q);&}#ur|#36L^)P4JRMHe62QKB@bwhJ*E1hV()mylv0rUa-~yzdNii*!oP*W8)AeY-JN1v|O}KcU>t(Zx%sUrEO3K-$<UqUN2B_K`CS2X&sD;>YJ^h<Dy8s#pLVPPNZKTGq&g5uZ6$o+KP@ry~fx(A~#{pet#ntaU-1tZAhdE|vPuMA9>b>#sesTq#c896MbeKA94uNIP-=-0Sy1|4!A%qu3^^}<o#k}13OM88`3#9j@@W5;J$aeu*nBqybUjTVhVOp}~F|5pX5qMwdo+Zd*`9QuIdf^??54YL>p1kmCyn*a+(2`R|6Tg5b77MUnKri5gBETUWOy>ZVnCI$Sn!ugX1hB|aP19Iy^%(&J(015bG(fUTVAHRxNhoe6`mf9q;{0F(bvIdOq{qOlQHPHe;It*vO*2n7%`CG>cjuaZv#rHH;`WyA{tAsH;OnO1MiC{YHiy5b%tvwsSXy>3n=28;LoxbBUGQT@7^tQi={VN|WkVHSlwCZc?4lw`yuqypuqw&Xt3NKS=m0nT<x68oyn9J@*dCu`yl=8GFgDV0#{2p;B-!*OC$Z=O<J_NBU|=rwd#Ac*k8|ZqP+cl4CmBu8yg&_zB#`a<GjHD?rYwoex6uIlaHLpGcZk(GE@i9od?lADT}9t5h#e+h7euMuqNQ>GJ&d{}6#kN+=Czj?O~1xy`rT#};Z$sehqQcQfr<AV$~>>X+9hz)o?@Yd#yknj7)&;Si!djS`<57)4}+eYPkI8*v(sg=-Q?SEE8DE`ej?rW6QRT?>qs$5@`zECz^uDRN}zt+RE)r+pAQJfdJ2gGRt2Pcd_ir)5HlBf3NOwvMOk%+dIZF+5(&t;y1Nw?9gOQ%$|<SCMjYIr4Sr_Keg|;xAu<za|DA-7x1TS^pyE^U<EYh1Zwck~-J$Wxw`p90z6gl#iJae%SfW{1X)sMneMl^l+SJdPJSli{c?!vD0?vNwEx+EMU;nTMypHrgO<d!Uoe$6T)FC?G9M@C1)1O|8^^m;@KMtG@3cAOyx6%ak%{b^YFN`U+{*IR6w1^lHW(gObmkDSX3-6Vz330v^-;gJF&SC$1<UYJ#iH#ATC0D=^Z;^R(5#7#x`0d;$|A>pF9B7w<K$6BAlli%r%)>MKoE{p1HkqBC$?S4y!V6F7#?mzI?@yxeeTT!7cDg-j591>%DB*#Injl-Uvn<j)X-22hj#H6D)d=$5by8=iE&2v6PFlSEUE=NU3e6Xloja08z?Zn`BKC-rmL-<tkXjbMa<cHsNsXw>`-NQAJZX8G{qGUO{76QF$^zW%8U;4mFMwbpjM!Lscd_OW7Rjx};=NBo!4Brw<XDF63gmt87JBIFGg9~DJJZIm3WtlH5lSVmj4cA38^a9Hfl$6@y}qQ73{TQ9FX+ssh0E5~4eBm=NG^AqDtvYEPL4Ea%^j)4OrsOo^Qi#Tr17WC13x(oW-9OA(mn1i!|&cQ`A1y7B#TUIG_^dJ8Z+&$F^YVpDe@)a!EZ>B9HjE<3fPfZ3yEhfWFKpxcox~IO!OKPfOd!ebI{!C#amk@oAPXiLtrkImA8)pEZqoY=@v7pq0yuSqe-W72x8_32!{aOs2l5+Fj%*Q>9V`a>9EKwy}Kxf1!h%zs1%ILau~`LzoA^g4doEeWLL0Od+|;QGJ$Te1iDk45+Dj2JcchG(}K#IVs(ejR~~-fuE{^*VzpHzv8V|~g}D79Xc(C{O)d-@0>qFziy`-;Fl2>Tih$fv0Qop$tLoE~S6)+Id_%T{LuvI;jg%3LGic(<bnsS|t*fF!dkz*?Rl7(@*4i)l(~kS~jrr-*XM~UAa9ML`s}`@VT0D^<c^7=+?WOMNiBQ>;Mwu)<Vr1!Qm!pBdaDsKFWm$!mWmR92<lyIJ(=#tywA=<UQGjz;g4BxPxkZDcr0&r6PrK&H#=Go)k0e%OCIZQqdQf;Tg?eBTLFF$BNLa$;A901V2=?Y&Wa8rBUl)*WSskuW!>*BoO!xo2)MqT(fNFC<@;Tc@Pg|#A7l^G><#YGiDP~e|<DaGP0kOfAz6aS2cjF`RHm~^7xR_-7Vse<12zEnJC0C1ATqU~%eqXFm(aNj4nn&H$d3D$Hn2)Rjd>r<Q6x068)mvg&?U{&Vf^>y|g&N9~RxstwL43)4#CR^A6!hv&L6=!Dm1Rf3#F<GGXUb_Dm<*Ya92d2Yh_0aLTfXRYha5e7<miPbfj3X4Mfb<F5B?D+&r{!MR9#D&2$_<gVwLU+(>=vUhX8{Mnh%P3xYr=Jr`z=~g{=B$Iu$pkJdAI1ufW9_bbsVM9AW!+7ssaX)*eV$ZRa0x@EoPZy0DbY`l#G&if^_ak8bPH_{KPUZ*s5^f$k4=Gc4detYq?I^@iYvyf>6huiNGk);SMZPOL*W*NV)>_6xAt7&dlpJX>;l0t6j{;N%F}m8Zw$Eq~*M<!>|}GobOzfa+le7{;@?@x+$yNo?c&YGo74&0|;K(vBTr{HuBfHroHC$Cymh;cKxD3+^a}HE%sk7OMtbAkM)KnhK1yqyTi1c<3Z~p_8CrhhePRXgy@deTT2V&cg;KTEJfNWB_J71MsGmD*Q86emc`VA%Fu90lfLMCjX4<_3%(osyAR?K@6oQAAmf0Th-~YRYlT_JO7A)W60k3w|JwGEiQ_>00adSIv@r^`0{}8HLM9K4%4s88ks@0|L>&@WaB;V95EZ^(98_sTaa57`)fdKQxCz&0ozoFQj!2xvfLLr49VhFBSuWjcoa$qaWzf6M{x3a1cTjWJJ2{jv&Pv8-K6(Rh?JS;=~Q@bbazGC&EtFlc=HmcF+f3vm-_|S@DgKh1BrW2pAQJ!V_WBpx6Y{bd!lVLO6Fy*_b_C^sU-;@zwZBgi2MpsL^j*|1%5}G^cUq~7qIV0<AvSLxXTRMNmJ%Sf%@9*I6l>VQkhDK6M}Bh1=&20Ba_Hqx4b4AVofg2i3WtOLpexdJ9;1M{s}IK{R-5&e*%Pw#IqkVotJr_6K;hfav_<&C}(fNhP>GYq$kUeS6czR9yFixYsyI4ql{EgACJ8Cm4E4r?Zna$xqAk{)X9RWi$z0oV)0B_fb4MScQ}<FY$xh~OCa3Cvo^oJh~Ituy3&68{SUu+_kX`mSlcTri7TrlrVWNBYcM4A4>A=^W<(dBoucG`xlB;*V1RDm;?PE$WHWPg)$V@|v}%P?Y}F#BL5(#H>M_%x!I}mw)--6N+ld^*qH>|zk?PA|I!<eAXqDwve|Mi9M-(~AN$L)9@1XfbfZmoOGSMs$O$A$d`<rg_ga|k5!n;{#J_b5R<%4i96Q?juA|Ds>E0{i)&BW8|0iLBvL&8$q8V&Kvn`hz~sta`r1d})l5BbXsRn_SwnCV=PBN5dveBgQg;tf2n^iZxsO*Ld)lY{m;#iP${c98;oV`^C*_d`r?jMoGAY8KH9b&gk$5*sY-Q-)o`>1h`&QqYn#lU)Me9Fefk!arhV?{azBQ{AV;i7fB2B4}T1jxlN(Q{7~u7^4}Qrd5`@k8-9ro+F=mx_dp4$gB~j2hZkSjsPavXXe=qCVPy_*&STY9^-Nv0dpH|WFXrMXOC6bK#9itivPV&>bz0F;2Eu(C&w+(e!^8|aUN#tg0;69KKl1PMr3N{{=Y}e?e;4{QoY7fD;}0wbrA0|VELqQd-e<HxZ=(aEEY;ot4BIw92Sh=NU&+3yUTv6fEhlI<rfs20A-5wumpq7ha62$4%2d(pq5P2)NbxhHo%On))ZTA)#cyPX*rV5t%Mgb@lh1Ws)k*(?xjO=5h62hd{DHe@iZTTp}PuHnh?^Cv&>zf?HdLsWskdTIdHyPc)zR;as~G*j8!CIWAG~47XabfWnMOvT-pXlo@M3Jh!RiiPWYOL@kbkeBQCZg>deRmg;TWI6^5e??oC>FJybnZ<TX9fAJ1WFs`3F*7u0erzbcbg-UhozLLBww$T-_Pd1XB1dB!j_+0w3hns|51^PEEM38pabvy`pQ8{#%^hvD10!(FkVT|)Qlu;Uzf1oP8wW<o*U`y?1W$h(HJ;}@-ZRwytobNl45y~%}TN9AQ#z(9aP!b)<M`-qrHsV+C&;kq;(R!AEU*<??^S3T})FEBdIdmy&s=G7V8TTx+Y@>%8<UgZ=F?dC5PvW%^Gq{}bF89X@-Y+i{uczf^Rv-i%ty>~uzT#+0|sqDB-Bz2U1g!dVUwknpAi!GQTT=_EZ%BRN(4*HC^zSCV!;kVl%yfSER4zsKto7Dq)72_1(k^M|d>8@Yi!~EFxBuc>Rm9ajr#klXo@k&m*fmLYIp@Dn%eYNE%ZpwW$y$g*}L4AkAjJd;R-3mXgI{0&*3&=Rd*;AtjxF`=TdTZQ|KhVDPeTYi`(m?^<h)t8GW5Tfob%yD<14Y4`o5O*k(>I^#aG+T9Wk;DgCi>#R`^HTA3ZdI1@(W-hZi3jhR~*}(0vL@Wodg#@Ayc-kA#GdtA>MBx`uuA+(iM?Rb%=OcY{)VWq%Jm(o!PmE@|XYo@_zswd$U^')))
