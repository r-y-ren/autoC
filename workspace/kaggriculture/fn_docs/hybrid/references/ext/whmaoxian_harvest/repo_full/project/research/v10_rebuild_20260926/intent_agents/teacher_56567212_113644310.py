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
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqTdyU@ai#xDKlel4FMgw_wneDrCP>P{j6eti{9wR<?ePVefieGms1YRYOGd<6k+t_Zr@Nj+2@LHzduLT;My&O%-~ac!fBNIU{NsPT`<wFq-GBb^KmPfrfBOCJ|NGtl{y#tcXL(<KeE;rW|Lv!LeE01)U;p~I-@beQ?(0v#d-p#6^uPbpzy8<1zx$i`{@wrjuRs3dzyI-H{`05*@_*kiN`LX&Z$AF=58r<E{SUwW?!&vkRwldh+mBy;{o(#IGf?@L%l+N2K794VyZ8C8#l<fE+YcXp`SW$wbwL&j`nn*A1=BA0`m4*YE{1hQy#DU~{-;0u-ETg8{Pg!1rO7V+-B&++`0k=a_`bv9)BgN*|NI*VyY%MM(#?wc@%>+xV_p5e-~Z~vhi@+z$JO7LE`Hx^EyyaZjC{8s?>@EJwbwsk=htww7EGZR%;oi6uSsd0<oC&3V%09aU1CkT1(LPI;;>6^KW$1&th}%663ff`Raj!pzSG4e)}<Ran?FdfOK-oTD3#bhf3{0+KdnfQiD>@(-7dZTv>}xw|MM()o@dp3y<RP~a&g}#YpD(Cj!)L>ReZWc^QVt?>FtjpK4<JtD|YGar&Z|&bT72TFSPVNco*7bDZJ1M|KeQlbA+W<>`L*e2JEh`Uu8{ty4b&9woAbWQ?!4<*zD5VPZOVI_NPs|^me`6EU_Pd{8JTn8u<Ft$B!Sr{^1XQ`{BDEzWMmg|GfPF4ff{bm*0K*_MLr%$k69y_VX&g^-9b}?|LHzJcn;~Ug8%RyidfUtU2)pv_GxerN$HS@);%Vl(YQ>UKdoLKv_=>KbKyVbGvhSeZ|0@Po<Zxd_a{Rgc;aMcDodQ3+BC7+4ZlU*cV9wPTj9;nM8BjBsUpuZ}gwPQ@PK8yquM<s6Xf{O29f5k9c8G48KgX>t)(r!^@PsZ?LD;i}l8o29k7ZT$cRmtMC5d!}mY<dR*WC@ZDFx`^AUvzWX1@3AUhb-phwv;+|RPtF7+sw4C>II_Q!2kRBHNqr90H$(w$#(=DRQlKZ>5^4rZsHx>BCz~m32%8p1Zs&o%w@@Lj)m)!p@i9W5$57>bJ{@Q_h`BZQGbprj!yX#C5?|-hYGbOqSnzFQ@lu1yf`^cT{1y8!eD!;qwK48>-rP%S-({eQp{<fd~ZKXT{4eU`Vu>;D&Zu5@XNGh9w@RXBlIPByqzoN>68XVXzaO~~^V}SNp$|aQD{YTq5^mMjE!?yq<J`QEx2g?3RejlLw*t+|p4CvNTt|0DSL1J5tjh_hxyX5}O6Y;Utay>-)I&YWI<*y-bej42n9`qJ90+TV~3j{ZUiNDT_kB*ifS^2$qLz-UL4(+ny?&}<OjrOPU?X}3y-Q_bz^0a}{W*aE6TTx9SmHm^u+t*rogS*1b&Prxq)abTkZtsjDJ^V@ZKDbc&y8AYqq_2DSI8NFfkG<{f1AjzuyVnjpG(`I49Lbk6(WXL<;+gNUR7dY(@EW+l3)znBIKR}k_e*OsyrzjS+OsJ1$ivaHsF-5G7F_e~3*?lAzCk+sJl=eRAQBGa6~e#O>thrXk38>px#O^_40-0$^7S8#Y4NRN4i`P5FXfEW=riKrk6xN+W2|0$%9%K_N{zhJgDmWep|P*ymvb?p?_;^CliAItHUxllQ+LaOR;4m6Y1A81ZSD44zr8D>-M;<-g<|oVqp)#kwo~i+A+#=)uez>_JL@%Cm#P!IpGyYX%8z!v+PY1TIN?M4>gR9h&{sILLz4`zQM%XM%eF3-?d_*l`&PSox_08`yk7&uuD;oUPU)T$_n*K6;HDx=D|>0&(^qx|4q%y8Qv#F8hwiDHe_;df5NUCSt)-T>-Xd9gB%80k>$cmvRDO$eyZGh?8Ft0ZEiAq}Y~yvbOX1fBdhmUTv3#U-3F0ymHm?m>Mah2d$*U;a#ajE`xLa=T(<arLZqhjIQsL>4f?cY=7%l}O;;x4`gEqQ_KBPxv<Sf`}S*rHZFV_a?bX=FJ=laX1Q*=lr*Y&DY^70u4e&n?4)n4b%CDZ;+Q?g6dIc*YzPWwm4DlJRfHX5a68L*zw<qz%AHLUAZUBl%M9UQ{Tbv<}&n}BsY*`@G8d7Wb1S2qE4n5*B0>M$}x2~0#N4`yQ8^5>MD4Vd(cHhXU(J=EJ`Z*osPh<5Sy_nMMjVH{g8`^@u!dYzjKXIsGe5d+q*NFL4$HG-tyQhHcbS=~|D{ja>2lJ0fs7U*&-B_d72o9nXMS1_nSZ#A!ft!n>~T$g(QM&f9ff;*%Md|I(f)mPzVN#c+;>r!==hwXv`zaLUs5f7SXzr@SEJit<rX{tyfr6dj1u_159+ZFip58c4u?Qsv4!n<KSpD!Q5_S&EMm>wq9k(@wBGTEi@vFPO;Aurt#mEP-n7W;-s!Qe04b2}tpvxE*%JfA=KQATEl>Dp6yy`|Eg%EBg0*|Dz2Y}k%f9?ac7`F9!^iYTblq9BKxIP$9B%*&`MFV^b3B+NmD6Xk7f?-pzx$OwK1r>$vZ0=n*nzFP`?zC&k+&z*?yGR4Bn6djDv#!?v5vJ@Um1oVh=`SWD*@rR0F#&+)`ZoAuoo^#U71xD}dZZbj$tAF#&$6vpD->99S_)wtb*oED;ZIYSVVG{Sm?km%?H1YW%Hie3{OA*CY-fNFlcAM7OUE0`tGf$w$2+MUj-DT!=mxZ54)9nkniMsV%kz4qMZQ)n8h2Pm0{@82b&pp9hOh-Rg5EXepFmj+O%EfGP;2SoIK{llgDA?S#W9qB5Sk18NuZu_>?tmm))h@=`qJ!4%c3OQaxANqX5%z;?&%X4^eGvnthpy*6zx?L!-T~_&dj+Utr+GW%Ce5ISgpiZqW%_|gKQr$&6B|3Y?X<{m^7<=4vSk1l6D1ML{3RA%;?<uj(TWF-BtIL8R^(wu4vALaJDdUES0SkGxDVVpswt`*V7gtQbD1EonA9vCXg3a$0LZe2h{9Vbt*-Q9oxB)%?md9+QLn+#$vq6+l0ALd!1iSeAE?v#U#6*xXZXeQlNQe-3PfE*h;<I);VG7dmFA&(ngg8H2&K>wlchDJ|8x@^?fU=A{`PmDK7G8@{5-<{FL$Jm3#i<r#HI~_(#?4$ZuX@2dq={GooKu%><LNivH2|-Q6EUyEeFVC4DP{Yb>-ZGd07g&1=q!zTX0=*b5m6*+_Z5o&ULB!{Jt#doStl5s&3=6HA2#ot`p;rPJYX#aQM#lN)vvJyjW<eo%^!XUINK3RgadJCFT;4)@qiQ!1c-CvSe`Zk9DbfLbxoMT#I5|s_twuNJmH(9pRit{XSmbG|bAsECpA71n#qHmx3!l0{7XlOTm>N?fXnx`BA>l<du(2*CIPzE9`Ww?oHPks|^^eHel{)10sC_j<k(V7P5l-{lcpV8sAYHw5djR$Yj19{Ur+m6VAp5gn%j1V+`4`pu*w`d%Ei{0xFLbs9ZTeiKp3So}a38plQJQsY%7dd$uXcODRYt(|fil%H~fz+dM~sZ*Gu;FEA+kqac;s?~i`?^qa4K_+)R#0)G$*{)0&14<cc)7VrMJVb_BDvEV<61kXuC+m97%Kh{~bQ)ksqeNXKq8?+}Yy@=s4YRe(Jeljg6DL{pGjl7hq(^9GdRA|>YJuuDu02Q&r$9$k4wqj&q#E>@jbkdWy%mDy0)MUq=P3q>^gs?sJ<2)$IAyCP*K*eFfi#ussus~%i+!Yq6BwnDBU5QYC`feU;v&pB;=6N=o`x$iDoP$RD04{Dt^I;N@!XMr<9y)+10|NaFk=?S`?%)MYNn6{AH)TrFuxQX$JZ)~p9qy&-Q2)uc;$+{)oxes=PF}hGMp>4sZ@6;Qa7!MYCw6iU4CmoHZ9T75_TB3OMbRS^po*T$dHdib<m*!PC2?6Y?X}$OT6JT0IdcL&ZrZhAYfx$6XxasO{lB3R*CvN)(C8JVl@K>u2|NKw7EV`A16`J->RnJS{=mxh$JeFmO>kM#yzh^pD2>GThteM}^kKKz6?gCL&Q5<eIjxzFAuO!CF4j$3Z==Jc=AQCHRuU)P6|%Yc&qx{x(rGIXAri=av(C272CW(hv}z!3ss_?SSo*NgAU+Vqxqb-VJ)kQ4fZBu5g{|4L*v#nu*>c~REq7>^v98c&8TsP=vemM}%eE?N*(j9^&mnCmhU0)&X53nmX=_P}$mq&B#LKc2bcnBuHO$!hCkMA=dxE6&LJuQY>K_4jKj8iaA19Z^g;Q&;OTi&U1o7d%83mH}+m7=?yE^FN^F$$~ZjwqP=?GSg_>+g<MY{y13p6yJrSR8TUkhS@@OS0ogqhv0(B0wCBF~S=1IY)T0kzlHWku!oM|oMQ{?feNBH2ntr6ad4P&#r#0osv6{2(!~h7f66mXVP~wQJ!yVkAX(&`m1$BqE=0k5LXY3yx~6a<0?5vPkR7(x$E~^Q!&IM_~Zz88DXsN$Z#|Vl22)k|ZvyDA|&d%*A;WtT}cdsXwuX`otRQw|Kvq$8%(LFPH5id@qMxCm_W7>o>9oH{VxytV$La=j#oZ&p;SLzGxczqG@{r!A8qOmDGc{X_`y)yR_2p(zf|7?fkoR(pnPPY85@<Fk4yhZ%7d0+PydJxix72{<J;#tA}^wt@}LiK~|A;lsiT-DP-kI=anZ8Z*@nxW0d_{He~lF8?q~QbFK@NoAXi+W3~#aU8yxO5jztN^NpJ@Uqlp%xrI9I7V4XBp$6zhg7lj;bovGL@c`!8!@R$nDZ-25zx(v*`wt?fd+iqa^DN}+Pe>avEe0WXpBVuSj)vPth8YnswWup|*nXAO8G*OCJWOx?#Y;}mvCX6vE0I>Lq)o+2<`pZ|!`N&%V-wYzH(u{jd4fap5F8YePocf-jkc!`-eMl?lKUSu;x2gHbl-W?{lL~L<VTk_*_S0ot5&znqnhx*Yr><)X0J$!n=L}t<u+96>!2milNNGETF9L?h1{7I>&cz?_@g5PJJ6wWO3SysJ~5Sc)`0ZK#omcSq39U6*x@x4`@^q1IVyYX9LVr~u!`?Z!M8N54p&!r-?+*&Ge=sC0i7+bjpo!y#6i%GhYGm>(!c=^rm$%{5F;_wrm5WaYkb?U@om56Y5O&Q+pj%}K>AiCF|x>euo~|P6u?ilHK%N~f)kB5lVQ|T{iI5x&17cp#NNmdt2YI^<o@=GZk%vR{3SvjP}Sum^+C-cK(i|~iQ;9&fP@6oE?3XHmn9REE+o5Ny$LSo4wKZct!vdg;c}8Nye;sqEVtVh_>L5)SW=*jNgI%@Yqkr}HhkX8OLzv^I+JS51nL=t3P+%Z(yK3YufA^f>YKe82X@x$#=9O5vliK0?_eEqhlP>!Kpy|fdi?92$G@@|>&jxR>n6tfEui9*5d<A<Ew|^BV<NV$zrR@~eYZSb10-9+l4Qno$a~f@f~%a_W{<G1{{3P9`$%#~k>>1zZw;8VYwg>0h1R~k+{)Ow3B@i|#|@VyoogkoOVxu5woMavcGJ&cn!LsLl`DHHbW;O&rEu4DNKmxCYldB`2!z%Jnn0)^lA^pRDJq*omPU(X2Q7}Bd*av>XmKnS{J4`dc#GsrJ4nv_QaO{wL*jmJ&Y)&A%e+|(NWWYiOgi1am&a9!H%=t(9RpdowYX(8Bat@@0M9!eMu6;C2Y<dxj4Tv8oD2~41P#+gOG0BeIYXOd$b>Ps{BwBZpXjK7Pr@s9g}wl(sJ=#DU#BJefH%NkF>rZ+$C(Ob?4}$#SRo4z@8pnXh3V=Vjg}Q=X%BpYr#SLcV6K^l1y&kn*zF3PkWd)f;^bkAK`P1Et^zYDS6X)@`<kQ2*Bt%6W`~+8p!@Ds$^DK3it~au6%dOD$YersSc)cP*!Z5+BPGz(pBQ=ZOSV-khHDFpW@xs7*jVUTYQ*GS$MH#uviMnrFKh<V-~HH=4>yRm0F%#B2&}ZMqFD-S8U6jL2iQ{>I0e$}%aee}OZ^=V;;m?>XCSp-dHO=rRDDRY8Fq|SyoPzxYj|8#Z0DEx;2kaFXrp{#eD88UJ+m(R!n*A1p3A<mlEcAD4krzUjWifGZK?*d?OVSZE+R&E35(ewd%ZAT9Cq=|mpSc<8}d-F(<)YO&P0b?keLqp1p0E)WsZ1@T`B$sl_m*y8YC<nr!_fhv=yudxRMJ5&b(r_9437&s&TF3!NX{@tago)mgh>c*+k?UKTV7Xami%$V%`%L7FJkDCno?(L=+`@iV=?yBSxMn8MWpJV)D5!N(VZFPU_h%^^8oGZgjGA+f0^zHY>(x0XhzSjn*Fq&(Z1(rF(cNox*B}(Jp~EiV;Z0%KRl3+j&RW5TnP2*gc~~jR+<h5y$$7`DPJf2MU0ddkYc$0g^=c-h!mOftK<j;$L`^x3;CN)^DNRY_alwv~Fv8&6{ge0^ISI1*A{b5`Jg^6{06hte!BlbF9kFv6@|g2Noq{TL-BWACv-K`J6My^r@jq-WVJ9$SygmA543C>0*;|7PoMx`8tC}!pFeNPLhX>pZ#q7^0La9;1{_BR^&2pk;|oC1ruYfWn#KpHZwshl@_J(aE)PC=%fC1jr7y<qPZC9F-B&`7zq0q$E{+a-Q6yMF>6S!_~b_};W)WshwqSe4aXPm2l9mn%NKsrP`0-K(^r+evVOh(NQQSRf>e2H|8%jVnnvqSM(p(U4IcI-N+c_*K@Vz2D%(ZSW(mTT%FNBiGdF3leLxu{7-%!gkSfPc|FEc`tZQ!@jV0`~ZEYTwF_cs_VX+0V25lHp(aID(TB{rI$hMWj*-)0pqqK(=Q|lrmjk-tDXe>x$upEuKiO~o&MkCP}jl7A`C_E+mI2mI1xtLGT-%Eo2ve8`5G<7Z(9=`_=`(W8p-jFS2Ubf`oZC4041L*aXRlhD!R=rSwuKKmK&&rH~1c8$l1jcBW7*kt4&R#cTVAog<1Nt=-ZHX~k!Uo9i?pqCh6vY-dJnexZUd3F<L9);&6M?5p@S?6*Y+Qt?Mt~?2at=>ma&#^q%bCVS$ZDTQ(DLLhQrlCi^)FQx=7|tfdW1mSHEf1{9*79rkLOc}_GlrRGSNx&L?>@fbP69e*&I=mh^UO+$h+b&8{ai-2YGc)Ioc^lTjM1OIhun?IgC&0Gzlq+P!u<JY2w_at+^E{eaa3rK%vn9jdu3~u|j6FGQ^IEiSMl!4?Lss4f*bYf$ZntTt45GWw6O|E;Q$W*U#}Lb9od`O92OOnAbF0e4Lyl1yu9ywD$I4^tZ*WTWBU*rHN;qZU9e5FbdM1R<k%F-=|J5>Bx12(WEDZK@KpubS*5=k%Q|RE<<L}5VxV-yu4N^&|0OqsZ~le$+OUr@O6{lOuOOaIih3l_MDV;AP=(Ax{Jn|qX+Aao}1R_KwF~|ZH>;G*63nmgNd$l^mLsaJIv_YVHTFdgP5Z;YgVqTS-I^Imyh#0zy9#`&N~r0??h-QI3S&gv#%&|HuI<K>_K6^%;e1hT~{1ro!2+<v{>1S6!CCN%v02OKi1qE_Pn6@sw3P&L_Ib3)KgQ+ZtA=MrF#S@ox=t|s+w3>eNk+zz$o@Tg;5-|^EyS^d3|@RIFl<sx8%zEdo9w0skC{F%Jea+(#NQ_d5r4(c?dY#0DA%CM3l}@&4-0*HrD;uSofcNPLq#anLc)9-Z0)aDZfgqaL}#72ZdVdcg0#@qudn+*Y|D@`Bu5UvS4Vif}y#Y>JsQ-j~rG*&~C6;oJz}?IxS}!n{uY<<Mc+}H15*<*Himr4stp@l<D+P=JOYzYWJ1Hq(1HGzX_AtCexoVsn-aT$|&*&GY?mfdARfPrs41#%aNCGYR{X?t?YY84s`qtsCXdO4kQ4Ik#Dd9AS$Z+>(D?&UIPV>E2(%kIcqKQnycV>6*TbHK@L5I#!q#c?!@cSWhQO&FliemvC8~)9_Jv?Fd&1+fCL@`B5vwYL3*-5O_s(F!aG%39p3E<H2boHt7-BQ_CV7|Wqmzu%I&IpvD!uIt=0JJ?6j>{2E|TvTeB{b-UN|%9;a8slnMk$b1y;@)h43j{K(4&k^@O2YYh^+fe)y1#l_@#Ex;z!Ueai*$ly`DffocNTXtl26EU??wKW^2SqYPR4BPBr0`^=%d?&!^O9eO?4^oGOu<{bZZrg86)I8+c*^N9o$xn|WKNW-g<gmwNNhUQ|U#iBy={y5x@{*t^?L;fTZr>2QsbN8;h&y_2nxg|Bx&g#{7^;AEk$QMLE*wO&RZqJFKD-UUiyi4pygR(@sOa+RQqjHA$i>VJa1x%gy%)LI@V++&z;7N>{B)DzJ$_0B_(2aR-%ys}=J}vuE;mFIHaFE>uOw$4J|FCg2zY0viZ<9~yq-*{hcTtp0fU@JvXzN=o&TQwd5DG2L##Hi{`&H|AC5nGIR3P0QiKpKpgS^2h^9+J*Xl4u8oDl!@B7TE-3qIAt9xp<#;V;0t9F}vq^k(zeVA-#h_4`>brjr^G~1f$3hZ_fbVFj7IBo8fc|&5js^p17jJAR;b7}IjzO3wxKI-1+qdUl2gNNEi8)|FbFPkjf$op}1z(D7t;Ro&YkwtFW#xUAN65lZ;{u-62j0k~k)?h7E6jyDHRHHFoo%TIXJ~%Vl^E22})A1D!nOvfM`ZPjQ9)#u67Sg&xUr6g3WFbM<*J*FZv?~almu+N@y!#~4?vp~hPwJ-or19~H!;U}~pPN8@x&gU8qYihX4!aBT0eK1&?J3Ng__0E}P#Wz*>6<PTKBqYGImOA7Q!KxRlBWI2d-Rw>3*nk0T(P^u6$gENleW)CyTXu3za+XW=mCE+95?e~IzsjVDg9D#s2$~<`=)Tuh)R42vJY<5Vo@i-E+G&XG^SZ2J2wy6c|0U)5k7l{UCIQg{6P2$h2<;MJp)){b#RlG!G%plTilfT2^*fmbHg*gAhZ57O^NnOY7fR&E~48Yc<G(KSE8JAK&9bq=7QwT75*A4PqFTY<t1i5oH?Q7uKdNw^qv*5=rUJ1#C9EM3>E$oE1dyDs~qE|%uzO2Jx6GlPN5ygs^j<d0d<>4WT-Da@q=pqt-P(a+qPQsu(;{Q9q7&;v+%kkdiBjq^cr@9AV-hm5Zq_3B$emTX}pnWZEN`H1k-&hfm)~V??r`w%{y&NJXP*F9Ej+dmrdNviD|v#8SeO~aL0zcNT7{**z_Mo-q(|9pBaLV01a@%K10cdpw1iNPUsruZAJiUljo;J&qN>}s7Fg^O2L*I&DE)Io_P^Jya#x|ci-kF3$5Egv&B1Z@))$hW6+Xa0_(@7owOzG!nI2TkZaPX^#kK4Bd<vaye1)dGznRg?j+hO0sz!dJzOFa1D}g)OKSTiyxq8W8IE_`>NyOFHfXq+nn2my36!0_zF{X&J}ynt@tjpOT!q$f)lCgo<3oXmT>{fB2al*6s`wzu57{%V@=U8_!ETQcd=Y8r4!Kukq!6DWsm&VBLVUMrTbx#tn8-V$l83Ne9k^_S>qkiu!?8K4CwcAjBd>Wh?v0OP>^zLSqstd#4JNyUGE1GHwl^j>%P8RZ@|ZX|I6_(wfbZ04!>)yOW0Td56`vHK0!Hl5K{tk-Ts3%K;Ng9VhxZj5BW>CvFhI6=+&5X*GM;T>5BAFv8&8$&(*20j3=%@tGn(sGQML=@S4&|BJdGXj^e-%OG%?8}m_eoS6RcsEz=zZ3bKq^wFlA+AW|fhzFq9VsZ6wSZ%d08nMoz)OwUD#$3rprT>~I=D<Aq~(^Jf*atHfUOuCD2b^^&!cg+?A08hN;DJ}<QSywK+JvS~gq{Ghjb<e3WH3X^BPNIq~n^MRk54@_X*wOHXyg9v3WK|?*lYtI6q=M1RE4f8B)8qeOU1XS*DG`7Rh_c|QB$4%~6bo3p$E|Qu8iNC~r7)-wL3ew6brJ;ULigdq6eqUuc6%}bol%rynilzaWhtUbMs?kh`u?cm|ARz2iy2tARtb2^9NFN1>xcZ|o;VBy2Td^gIosbGciBNh1FXrun4=J!AEYXIrLL0*BrXj4+>a0Plv*w;UOCCfLP<SLU>Sd#SBdG1eP~YNSwD8aJ%OZuYzAk_?)R<+tK17BDhd5Sv6(H#H!Wx&_9;>^%LVza?K8!q8AoA8vX*M@-FFKV<6dQkuou+gnJa9N`Y5KF4wn5@=P&pT94P4+IQo)D$-lC=v1i#2*s&v>IAey`0-v+xtB+o`(p{Eenu+^CN1Zn`u+lqjODBgpnc*{HHz~}S^K4VCgjLExJaQ&{$N|3|?vqlBpfR*f$gS2z`)XqIzJD2rdvE2RcZ1-ESaslXY<KBY&Uwza6HEjAC(QZ#3&f9!4=dC$7<uU{TppEGO<!8pQ%10tuqt_gCn>DCybuSK{?>1?8g0$D}L__+_HGRdorXEGnlT>?(t1cE7OIB9hMP79m`4fcd3rc{Q==#`^Jx-l+^4UHIKAU0&%Cs4%Y?^_pZ3bH1jh*)p0frzmdTxF4GL?O2MC%tA(Q0LLXPyUFcphBid2oXdGzz?`CwWMu`Ak`T!zrs)N-EDNkwiQbjVwk}Qky>|wey!acy?Sm*>SIe9S0w3G`mjn0OyKbbUn)ktVhsr5OXbc4-aqJMbJ1U*-4=((z>p<K*e(yCloC`puX32dFvW!nFSuE7ikYeracUYh4f7$cZ^TklSennbIKtC`p(GLLnB`Yd)&|hVlvHLmd_0nCC#jZ0;n8=$sag6KiAkq=yedu2xhiccV=s&udlP2t&{eo1zWCZ$nxG+u)y<kSBLRv54<ik^3*;kc@-9xKwjeNNKtL>6xB{&-=M9|fwnq7EO*s`I?$1NfR^?8cmgo^pd&Y?n;i~(pDf-Ij$E>0D{&wa3>BC^d*<KcY(vEm6h>NBDcyF}_@u&1*{UsNqlPNsby3z1%85O>g4<ldiUKazB``a=+Wi~(K8fso(v9Kc;Aw>7#u<83tP7ww#k!O*0)4)zw~p!ImZ}nF)w@z}C;k$_f@p=Wyz*4Hsx}P<?^_PGvW(=pb&pH>^A5g!yf6}$IR@T$pLxb&<uQiSE`jY!!$1Ngo_m<j^xC(YUQ3)gGzY18YOH+dZS{oSR&JJvd3{}sn`sv*v&3})G)siIJ-2$8FGZ1AF|;Uh2<xoCa&GD?1Kp-hbelSFwy6uvoojTDzi)Eq#Pd}3Fmkp5ZJ<i#RAnBg%G6w7(JnDs-0PyhJiCAT`@Z}1gFP+PuCdTgwO4661E;K-dn}!Ky<cozZ%0Xn1<goD02ZopVU2hoJaG<q1tHU1l^CjLN!#fm$N%&Q{QARBx8ZNT`S|O1|Njq##hoB87?F||R!Uk~DQRb=q=S``N~2p@OX|^uW{>`~@HFdg(=s60WwcoXDbi$)eTYTcn}+Zcxo%hJ5cu^p&gdv(BfRK=SY&$c_nNpDrU>mY<^?&UnLdS0g(5D&OyJ_q1g^AqsvSj!i`ri_?HWjd3|$~%2ZN6fgKdE&%|3-30mM_$nLzAGAcmjNia<Tm0`;^B+0UNX<9d`T{`nG0B{?I%`e5NkBM=?}gHTSG4tzwUwUe3FPL@p>WaXL3gD1AdGq`snxL1|_$%i&t#8>d$@|vhfWP@oS#^%c}9z5J+I^ZUVJ&!o-ZDa~JHod5^=|ycfy(n|qzXtXuAgV{)q<SPC&jF+Y!+Vad7WKozga^LZ*F_X?B>i|s3coolV%3>`9-UIL)lfuAt0TOm@ro!%aLJh|tj5_`yCx_EXYv_1k!J^HyToW)uZzT9Mdh!t(R@Rh(lL-OITu45`55AK#t_pn#PWb=((|3*8P+7b2nwXg0K}v41E}gD8g{$r`fmbGBUqafI?1G9AG2WMqH;FF?0BHU@0o}mS=d`yVQ<?L_I6g-J6T~b(zwzzeJJTP(;c<4*-@*$eDcndeujO>H|2a-Zy?egxL2IGTt0)u<xFFM8t8_HfT>?_epxr}<3XDO<7696DYA{Gl<W#;v*V0eK4X?QW0p6$s^)Eo;aDe+V~xDjH=nv)R7)UheLJi59eWXXla&g`NNa_YBWgp=R&Ea03Y4VLX`ygRjzql|j!aJ4hdjoV7!6Zmpt(pMA0v>v2`gWbu+GX~VxuJsla(x_uqRoN`9qmMFg+!Jd2@=|wQC%Ewzat_vWlBprc86)WQkT})wG%b*P*11c8M8y{N(iF4DTEu4d}EhV17sf;$0mo)#M3RE04%<yV;_&O=n!EPlk%i?Fo^|JkfLV@x>FR3SeB~Vwb@3jtL+D8-IzN7O+lMz?x|FZ%VBCS8I=aCW=A*Rlcsd8ZiNCL2<$qXl)__3nb!^3m=cH%M*po?sK?*9Z!foxqq*b`)BsxFcx1v40Bl-N7<>Ado4;i2lXzaD!DZ#-&DzAbp7r?<;!rP$tPyb-NdZVTPcURwlu|M@Nf;2T|@~&Co2doe7r;P#5)k@q!U2*ygXmHcZF(Jc!7p2bBUfHt4Jz8v1@F0cCK{D9Cj&an~6*c={6<djQBkxeqTJ|x1#_O&;uiPV>FXaJP^ciM*Dst(Z136q|8$z3Qs|8G-OngpIpXffecjJg&{*w`yM^+Dfzx|R1vS*sC(jwPJ4DH@BE6k^NTpVH2(0?d0SdHv{#dM1<9a!SXFWc@g5Y!%b#X=Z;sYk&z{bDIn2RdefX-%H{=^LbO&Yy@_y;1acvR8Qi0Jm9Z#;geNztl0;k6;AMK)R9~R)^mrlm{FaUt=<!^S;_1^@T|Dn_VX6#Skk0dH6Pdk*HX}luGdGREjJpDP)8ka<CT=J&IrSQUYK;jPfh@$}~aEROkFLF-~Xr4AfX*=LMWkgZz3N$yk0w*<ohSKR7%Cswtj`M+Y7sW!oE)e_8g`d_`cBCdVH5w!{f=<M=A468cpNYROocN1-9MQz!OuM2hZE$X^M<NBg!q{CQSoCC?{^i>E>ce>R)lYc$Vm=TqnXvuSy2Lomtc%2_cH*xw^Az>@M$@62=lRY1C+ePmLL3oQcy|v$ej^YwWJ=&LC3fZ`D5_mz9GcffP_jC9iNm(pNvk^WroQM&csi48zr-Y4UF_r#0uH+bjwMVeFwfNVT`US)*w<+qdv`dfyPL+|X&SqdbQkEPyGX;^GYxMqZ<nLqwL?Ur;}Yc%^i1+ZP`b)p8}$?{o{714LJZ=yr0F**uitP5-wr&-)=K?Af^5T~vX4`$c$8Gp;bm83gf!|YrcD`PX3bKvKPW*xsC5O*6R%+7iiaI&&i7M+c*fWs9b=mrvN-0>>c=HfZ3Njyd{%e{*&Y>S`-}q_96i39lqF&fKu*xQ1b)X%0A)1zOPn@5fk>`Um<!sQ>{Lr`s3ql&-nsyGduep=#HR=qK0~Y1Rw%@D1!on#WTq{S*~&W;98_3Yk4v?!QnWCjYsE+%7*ZhG@>Wy#j>Ya4TN-#RQ)zYqG_}FfdWS7SRGcE~0_b*u7-RB#L&b6>+5uD?0lL*4pxfx{>$LPR(9*-WDLqU!YK-WpC3G5!aeVuMK;Dk?9?tmOw-}$BQL6_uwyE^krqQ%{KJYfZ`oP;tYmyo(UmL7?ZEmJ>1X?+mXystuR1Owf0%dlGFy&O|F}1-ifwh3aUW2mWD(~h0oJqdZW3&SZdy2PdU4V5~x43*6N0s5R!JRi90w5DAvL~>SJ!v<xhfV-~JOxnZgmjh@GB!hF0*~NGc8Q@AUl&1Xbl4?UI<99^_i}s4J>h|`5gtf{!f5)$>`@H@QbVPyvn~+dL!FmG4qDZif<x6PC(s<6>6_j>sZb7U8EjU|+)P~wd>U}#lXi<I4Y+Qk0XO~{I}arRAS=dg0=gpajCY?yuy0|fX&VWn&{1EOTDsVYX|q3&ed(Q*H##|v>%%TFbnlpBDL&}T4JxI0S#91Ey;fHu(-&o1O<*)9<Up-1i)8GMtS-d6defMFJ;}9>k#gH3;;YHBeNR|A9TB7v2s0q&#GS|D43Tit>;iI5tmQ)uo}U@)5*McvYSkWy_<TyjEPSu=BG&54SM4;1XYhmE;7P-Z{xqz_Ut;#8Vb#r1db0=I6kVtBidhw&BoTI$aXNYKzjQO2YTK@xcFJ)cNc@(8D3X9@+9cdUerXBxInkAmdd`dAb6)vNY_|FS`lUJS0_pN5ZS<FY?Ul!hJ|%ZnQGE`(;_kAhT_b(l4q0mCWvSUNAz+{W+=9&K7Rb8cNOMx9Q;O`lN{RJcy#+j|1;&Axo!v%aTEG$vr0L<hMxN^`A7<#pE-g*A+tIMllNk%54KJE0i%k(LYu{_EeXq0ryUF_RV&D<^097B(pN+taz4DjXco+DvOJHb7u>UIAo?TJi2;idEnpIB-$R$n=n?t>RDAsZayHj9Hgt5-BxU=j_E~`8XQ`n~`{gY($>txq((scv!;q<f7>|xt^HGP*z(*?KljxgQKtM3wz;ZH_`ckuaR)3(4-iC~fUn7wi0-xlLSO9YRe(DLLDEzgJLs`DB+-b4Va52r2dBkaVAB5)Usaq9D4QMhkW_fXkpPQdMV4OG!QOuu38Pl#=eMyWWWdCv3ct1T46+u)6k>TQPDGdv{k3fv_(b!7l)SEj@O)1!^U(yp3%WaHInCo%7>Mf|=9Ts|1Gn@X#}q)mM=RCI%us>z#rTHO{O=ZrbId7nwduZNqbO%SRlUaaA1VY-t6yGA~ZD+Ncwn0yLx3y=DlE&S%leo+-SB%V8wJ>go_E`r=e5wT4;$QXl1zXG&a*j=PiX*b<PC(chkzBz8J$C#7gEHKT{lzrjCl{XnR`%q`J7M|}+YA7-DOg?@wmY)YSQW(J57V@B?Ll;bhGH4M>;?3~#wyb%^fc)g7*yTEg?67Ie)Xhhehm8goY!n%@fP$qd1#(H}pb6*{n_UVjorZXM(=LEiAnQ`KKXE1uzlMb2yf;+=@!!QWQz@R5V0n%e=|NVUv>PX#Nxyi~?_>k>^wi$C5yG4JYZP|*g^@U6#0_A8s8|u!1uPohf%nj~RLL$OVzke=U?QC;*d;I=EdcQN#9tzx72Ij3_MqL<$&(fQ1~Pk5(q$rXd&vWbhr)Lw&!kAas;<~2#$IM!gi&U&YwWx%5g^%9VnG*>zOYiNXHxg-9%-Orts2DHH1~W-GQK{t(7vj!`fL}8tG@8pSnZCD>0w@5hX@g&i!EO)O;ut@^NXvkH2=Nr8Or%6CCOzU4FyxCwQaI>$8j7DqPL>k1>))-b}a~x57Kc!o^{#B0coQi4x{kB&1~U8Ump+~Z^n;eY4gd3;%l5Eh;LtMRDGvW^<y((czP0s<7WDAI@5m-(=wu?1w;xdx@sy<kf|PmO!X6FDo>DUo*q;}aTu6BWw_u#Dcb5AqBT@`NZ%=AbOg!{d%SqPX##>8r5goEYy?j=dQeQ+Om?iE5SUGinoLv6J2bUZWcXG@hQxLf0}>?L?SH1(yVC4k?1NpP+2tVe>WQ3fm%jzEf!F|Dnwt&B#9Nz12hS`z^5Z!d<-g$2eh@0+m>?<>IyoYH;t_SL;UR(i%bq5~sTBN@Q-3qhW6%SXfB_4{j>4ji!kPLD%(=mwU?TTdWr`dY`wP!anwU9O>;mYufhl9#LqdPy<43?>8W@@_KTLm!`P|nPdRuy3g9u2V>l^m;M>)5z3!roRx)eNoB!1?TJTsq!jBpx%jh!E5O~)wfH6WNb!-*BbF+ftr!-;n|%KDpUT?4&&4&yJI<5Y}^Txd?Qj8QK9D@5Fz2X=lX&-A6;x%}=pLygZ+V?Mj6`I3<PVbMxjN>Z>(h$Q6nqdN&X{dguJKRO8+gd-N5{j6sptHio3UtmHR(CZSTQ4FUi%bCUz2Zf#?#SYNPq)CR6CK;wpl3_kDq&V>`6(mQw^Orbm!pyZME!YLp+XA537<$ZAiFrr9DHdc$?nuM~H}+tT!m0Jlg9Y=24$XO~PVq6sZs<14&>HJu(8S<@CW`4!l7%kY1yBtAx>S9_V@Qtf%6Gb399R0pcvSLl-rItwy)Aeo&$}v_yyIl@+sDLV+x6^WnMZ!Ro&nr?e#op2J|Jh~fIR8xV+yX!)|BXWi!Vy}RSc~Q-LNXxLcXs*{PY+7=9`bd7Gr3hIl-1KS~0R7t+*K;g_x&I5ijPOYTL*T079aralQVO;R$-J*A?gtdIBofz;kfKAFKK%0hQfxD;|?hdrZcepi2;A6!HG_04bv{C-yNMOHe7Q`}zQz9+7;jIP_%2Ck@01J|ISg?+_yKDlw26%bE(2V|a1taD-{ijcBaEM`J|?OVO7UP(8fM;R<Gu36XSGK&P?-wnA+49yca=LW@9-{wBJA*n|u-_5uTIL>^j^U2#>h(sX-y${N^lX;crZ08<0P=wXu2XwR~!`BH;#9o`p~_dHaMb~8;+;8ySlZbcp<nKmt6d|+3j$6TF0j>ThhZ`;o9TlIJ}yXLAF-0goK>HtEn6=An&1!o?|uWNkPX7gkS4SrwXfK7K)vRDMkA{sE;JjcZyu!S-K>UPE5pEc|n;R!f-LWQ_%mL4v0vkP)}H&z-E2dj;UqT8TCIrj+PUtY1BqNk`6nH!BI>@@Rl@=;9DE`cW>fsNM0F0s(^#YW2)`=)$xIOL1+t~DVHqIChO4vZdk;HJR|6(RvjDScbA4lu%L>00a&kYPm7(mQ(4!~8=4+KtdU1;5tm85XCZ{Z;blC7}HgRI(K9?RZCAtB9be?FovyjWIVH8yNjOdg5VuC$sEV+Ol)Q?QaGBaMxe9#Ue^0A+U4ee3Z^4)06s2s|dPXq3^k|Zd>r6c8_b(>FnEbV1q95o@^t76LB?wownf7c%Xyn_z-LM_Ra-c`Opqzda@ydZC@sKEt=~&`{=UOrYISWV>r1c@yRvV#sFTI{GdC(EY4PW%>gJSeP)Q!jiOyb>?bO8fJ8u4a*~Rqn2>W(l81y}Jqr+OofQWY7H}2g!SsF0R}8kzG{<hTOW<MiMA2RA664smZh&bs22TSlK1gyL;Kczs+=d-|XP$Dluq6pSqN7&2=9q!YMmo`@9a)2NN_&HLtks0`cM>SHJrKGR$(@}V1u)pTp)8-R=urcCbU4ygkwFv@VEP6U?$Va(P+tp}7BKKyz~qU+&NhmM0w;I2S5v^3+_kE&L!=2X1g_AMt@g4>ZqI`-x`GGAA5?5Umd#g8I!?ca+B%e>Uvp%o0fRzo=&_l4M(dJwwrt_^JOEv?$*|?)gtHCNw$9@adb{oU<%c80VcPz6lZ}ko-W@ZsVwV_7UWm|*xhH%PMCh!hy0UE#W7z4Fnj<Gd^lK@5UQ5ZCadn<UHx7jSs(?K$7#EpKX4Y>sSi8~Og#Cw2QD?Hfc_wBZvh>NZ1P+|YG%j!O8RpY2G1la5>`u6!RH_3eUN!C!jZYrsl{}=e%m$s_s@V_hvfYn*f%vbziEXBTXSF9a_S!|$7Hh%t+vs|<YzfzNZC#}!b)&S>lno`YaYb8aeJ|)!*%=N8vT4$z*9f4HjG5Bf(Q(Z}sdP`T@6E7fF)i;t$gr6E**s@-8$Dh+`U2~zLVM`j&EtVnz(&vX2H5TdslVeeA^gB2<~+Uc%NKft+R7j+r_zJ2?to2>mxbgM@UgcRf&JpQ-+cV#AHMzS`yYP$9T2abMM1Ta`w*aq7nq{ZXaUV|Bq2;*h8sOf;Y7d6ru1S_G$`4T99bNYhE69-$)<_&$UEV(J;_fbIz5q4$$#D9FPlfr8&^~TH8=)>3P_{M%NM@%<PkeF!((p;vlZLR(sweC(8-5BRmR>dU*7H}@LpLDFVQEA#<xfg1V_yD{nhQk;-6Ri*PpHq3iklSAO9a=>+iD')))
