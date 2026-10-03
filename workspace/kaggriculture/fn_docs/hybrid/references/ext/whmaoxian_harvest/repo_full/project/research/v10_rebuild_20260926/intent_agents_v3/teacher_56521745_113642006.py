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
_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rk<NzWunk^L`qu7mFjx27qeMM0tJVp<GpAtVk+Bf$)dG$X`+p9UH_moT&U%p)@MtI89MD4&Qg!^6YO-uA1%zWUv7e*fD)z4~5#{p!!Z`O|-W^WT2;tG~Yb-~apOKg;X#_3KxE`0sE2>#LuC@%c}F@$*-&Uw!%GH*dcA&-l&%^1DC$<&Uqv7hk{npTGR(w}1T2@BjSG|M9oiTZ`X*_W7HwwMkl=PS^hI!#8Vx`sVGspS}9`%4)Ct>a!1T-ha2ENh_jttzoacxYm?b1nXKc+Dk7k7KL9i16M2d(#xv}zkJ%b+E+h*^Vx@!rQKe7c{Sm;kM`A4u$Nw3EnWQhU%%#F1#vs)e=q+2FTQyDgJ1vrvoAmV;{BWNu3YSu;!9MeXPBHDJIgQ8lvYIV#?JCvByH>jT&>tk!Hpd^t_E)Gs9bGOTkZ3AUjZ8}pDg7zTHZLVFRoebbN=(sPA}Dg55vFyzJLCp|JZlNnfu-1AHI3>1K`Nb!tF)iZ9Tt4%+imS%^gzhrI$OTNn6;y+OU^iUTsSIvA(Y6emwhO%E|sW_v4h_9CJTL;d~G0OE-U?WG}t^eX_K~{p<t(?4$qLN6)h__5+N>TdwVz(_Ly_wAm|#T_ctt$^2o1z4Y>jjncD7{60(Uhbt&wpDry4Yn$ZqK+o30K3)8S_wRmgeyJkxq>}v`N=u9VTS`lt{hNaC?AKraef77ES<)M`&)>a$`{wfxzy9Hy_aDA^`^A5rKC^(gW+%&E&uPEi8M=YYev}KlOB!EfG^Rp1uK)&H1IdR*A&ZPCuc&rScd=ryrB5Qd{BM8elU<aubarHLC+FpzT%}t`;=?QUv(xUm+7D7&-ht)kdo8ZN?!Z>MxTvGbkK#v#+*V0BHtV6s=J_FX)F~-lk8dXUPG35?9Q}IqG~M5QG=Kcr`~P_JCDd-)1Fu03h2o@(xT}qM#CZp838mwkyOp!rP$l!fccW|5%Tb?jxGTRmU3W0Y-jCkB`|{1{u?Mv0*PA}si~iXyeg5w3Y|79W;U7or)s4nN&qz8whoMJ3DX?XjJlI9Q#*O|agq0m4caBRl1L7z(cGZ9e6vD2W_G0XbM{!qaqkQpzt2EHlX|!hYh)d*QlWZ@!-U|gsb}m1wmA^$`yoqgs<k$qtq;K%ky1>tD5<jyk{LBXUl)^_s0Jg#83Uag>T5oJJ+t*Z}_e0Q*=$Q^W%Bje|*OC5+NBSeKyqkf3|Kn<v2b4mNhMw4lJV+IJ+$g(8+=(A?W01M_tEQt~?vLn<M=<EYpC-yk|F)A01TAXzQ@%d>qP<AMwGsp`ZX%PwhP-&qi@gFH`YK~$exNwyF$PPsQjU;euef@!lOC%ldPrXAVSihih0<t*V~ihG`(U7!SZt%M5%mJ#EN=p>MFys=(izeq!pP<s((R>K36|wDPb=5k?&W&k@1tVuk;eXZ^AK(t+`u_-dad3cIEMY@hxea-_5C;R-~ZAccq{jr`07ZWkv~o~e_p%Hg@Y&91t)oi1pgVb#e>+|2sf$i&wu0n`gG}4A3W?4_|`tzORnGB%yz`c_XR5%<iaUMb`m1L*>azo*AUdbXd{`Q*0_jS+Ae7Hv}V%7ao{+**agX6adD0O9Kdt9XXWR+{qf8B3sfwwkiui4Tck`kaXjSNaHb;inO!0ngf(_ip!otp?VSQWrO5P@qR^dvU++TKh)eNq#HBm&J-swNdqUoKq_HHPei7FMMa1VHY~J>iA}z9K(qUhbu+WMD@QBok4G3A;Y{dY!m0qKr4qx;AIZfXlYQ;~Dp7ggo&|l_6577$UQC0ryohhx=w?FmRKBT`>TWO2Sc1vD>4!g0R*Uq+>lkG5(vH}zP@r8&2;#3;MX>1=B2iu1^$X0Qcy_$B?`k=)uP@1aq>PUZpmb9(%2RE)t3-U_wul&7<|9dk)EaS&iE8E;4hn*JTQ!m1=%C`L^1GgQlV&C?{eyVA$cw@_c8v2}cDG=#WAOS_5b`DjxNQ?m5j`hCDLlfDtKe&3M+FDQ151mYbxN-&HowH}2HkV30McZE5HU#jSbEjmlS1Z@FXH#-et2q2mbxIG_<_<;aq1xP`WG}rq12S+iY2y}Y3)maC+e@XtaY(xeYhfbW!q5WQ#&#rQr=CaYN8(;R4_Z~rd<C$qZaiW(R+|-|?t|dTtMAcXJx!*Ga2g9G@L*Qr!K`u%5g$TZfoUf^D%ruWrf}MJ`J-8+6&bo<vzKd_=yxjyc)@8eSGVEm5)1*8K6(T7NjY5t&dIC2Uft8DO9FPuVXs$9@6(5G+uucdsfsG5W9AZ92WwxOWemE|&r7qLO3yOpsx;=i=P<xSO5EH9qHTY-VuBYO_HqqQK3#zwQc{UMl~XE7OTbgA*y~jY@N|g>&D&nDenwB1V5d|H_IgzVl#Uq~8@RDhqI5twBYvMF`&heexhXx-juyoUV^S5GN!4g3)sPxw@Ov1f#ua2@oi?3e=@o7$Ei0KM`9-eA-QO7OGg#U2Yu|0aOY?LK&*Cq9GnDyesLJ4fmM0_*4Te5}681+T#!6Qs8ek@MzCQ{(_5$Xn3Q=f#fnxTSAdYb2J9vjtaa*SNAS8vrLJMgT{?J_F9%Z;}yfb43Cf$(`Qx-6-qX;nycH8&Ehj}`cHgj&znezcNXIlE~0Zn&h-AsDU7}jRz@>#f}I__!|QxE5HTJ+=a7_e>PRC#H0DWu9f?Lo{|RYq(hkJvU3r&}nr(2=045bb;+nyn(P$?tl!S7>M6b8NafHZ8YTwVie9e?M6cY}F5g3o#?>{rFbJ-@o&D9NK3+>}8cyc(Z+lKGkT7R$nBAjaAn>z*#G;efTv(`)=ck^Vh{OooJ6Roj_uw8vD(f^d~DwD-!36w7pb}s*+IKCckjSUZK(Ow@WjP6PbYdoCLB|e+^eXHC(2p)R~r2XIe^~cqw({rPRSArKX)$63#xsMhf}<BZa)C5l*Ln9g>xkH<zkA<8(<gua@nl>e%&kNymVsX0KOwSU!0g-C@hKy<Xj+r%Q%|A-ug_J*%=XxVS2p3E}Whzj*r-#O+C|oQGemh9tUp#71dP?OLJdcJ=liv8SU5nQ;!3HYg$hk>?uCej7Y_E%4;C#IqC%Pc>*XX)I0}QkVH6ivyEo^9yp+9{gXzz<&vY|4SJ7FJajDEUAfS+e^WZVA%K~U0!Y4OTq77cs;o?eS0bV>Ep@4YfL@tfSNp^ccR!gMpY{`)ePa_!t|-ARV3v|rO`FK81^y%4m8ZVs5aMXoyprmM!BiVJTppY=J|?2A*Bh^1Kxs6BP#I{^|~b4rY%(CWQhVPtog*sQ^)8KmM&`N<3=fPN&OVQMv*TC;zlWOd9`dW1xtbGF9jlB3PgV?5cyId`b&XGlmef+w*Z~;Dj!Xig|5W;Km~%hgq>DS-lENXtZ1*3^Rbe>STn2HUZK%$^5(CiL0?(_9j^i4Zm-tH1$il?me+zlG|zTC7SC2eiV<S&*blw(`29en5CHVTrPM1ZRs*5wH54mBq>OVZ3eBR-0OUb?dsen??QGdP*0AzO=U&BlP+X|yBLPtx>LK(A?Z<PZtgZK;`;j-7xW;KMsx++__Ce#&NP{MPm^nHjKF<8&w)THm#tTkezOmcIZuB*|LI=wGtqOer)vQ#YPofgOuI@!pR=?qx>~(TWk?qAAhPb^#djaxIVtpa1Y)We*ANf4@0GE**>^IFWn&6TXvVG+yCl5nLdx=rLBudYncSK6V3Q}rB>r!?eQmuX~WVV1T6>$*JAp{JfweZ{<@vx6<*;vpY@BC9cc-xNC+Z^OiQ8uQU=KH_BTzmgdpVoBPc5JU#fyL9u?Vb}SeombHbK>NIj2C?X78SF6zNf+~9lT&Z@Wj%@6HE6DRCh?PBQL#<d?3tyVbelyq;i;mDJ%(?;!2Mq8v__HLX(b51V-rgVh!)#UZJ7B7eLqFf3w}AY{dPP?G@`Jk8WQCB7$M^q-gU5pduKf7!><thtOZl_hQ|LdTYsb?+2Wvkb~axG5k0}sFw&Iq1etm0!+db!V0NacB{;+$CySdc6f_T7G_G3g|gBjcqYrA&cI{zrP`j?DK8ZUbq~7*t_aA5fcK5%2hf$kqzi!ntbj3DOvB?~I8~b;{qMU&Sj!D7`}2)3B-0~Zrgs1XVwjPS%$FNGUhcG{Z0^Rl3uk}E_5R2_$zP=1^Jr0_3BP4YdLHP3epnjl``#0!)CJ5jQE!}0h1x%un5P_{xgt^9&*n?95=)DA4SZ@Yo%G3v-K0Q!CmiO4plCoctpTaD2Bgy(kjYCxA};~Syac535|Ga8?dG1E`$W^xv2#Vve@L9|F*N#x@~Ir`odhz}ZUzvaenc8?k_8E+J56Daf##t{Ud1LCCIg#_V>-Y=>jh*6e^;JtbW0j!+JE=JIdQ?LW9LI7E-BRj(>!ge3=vc38W^G3CyNKin$2CNU0oV2G#j?ij2=GIPA!>tYRM`m0`Sw8{;Im06?fuui4<f}Zi50pIaZz#VA+rQ27*UNT8R;r_s5#mD++eUPKz1`?S4FI^R-B4o<ZiYDA<+OJQq|K#J*tbGH(I!HsHJ~Bw;?&zAT9z`XqYjqfo7BU+4tTxs6hcXLMifdO}m_K$;UM_=Y|RlV_Slo@tW#T!6~!DLS9(I3H&!xTmg9oY*B6R?RG|T3C@?TPtt(3eRXRmDFu~n_sM`4<6y~)q81Q1BkPLA-d=H1)!=Zy$ykYGY<jB#6Y?b942GHokeKpB0w8xHW>iv5@1^Lcvv;wh^i^Q>hL>rP5Kru2VOhL2-hHBncTx;#*M{{0SI_wLrva`)M45NK)}ZABU8R|mA}PCL(YSSoaY+ki~z`(cX`+WK!(s+7HUl_nwwdmv>p_LMP~bDHX9&=B)#nw*Kb!`92c!;EXKAl06`p92`G!#Dt6E-98#n4Vl=s;r{UzvXSr5Yp4i>~?}&9gj76jHWO_-eyi;}7R(%*~QI~9^Hu&%P;K_wU*-6cBh}!vE95hlZd#E~K*Wia;g9mn1l#`W~K6YBVIB7wkyi+GngPnZk8BrbQ;O}$tj=B*slXs-xMK)t0u6eHnZ7_b5D6T@8!((m0k;V?&6I;32O;T9zZr~Oapq2MC*_rz#6WqurYK<zI9Eq|kp<9kbS;Fd=5<)(%<>zAVa?%R9Mhhal&D*x-KbRCU?8bdbd`eML=`sL;1*#Vpxi1fl!xaXHQ${Ta%vIN5u1+fnCod$7ypS;4Lc*=itnL;#(r7keqY<r#(jPJ=u^1Xv7${3o`Q8h?I!KVH!AQwoa(y6Ye{NafZ?W>4N0Dh>4pbs$28L1&VFVVcEN<1-a4P_Y5}x>eP?RQOO!fnZX}El37&hCU%d>SkesR^=@?RJJ>fO7yXO}$M<P!9)FPxRJ3=~aTv=?YTY@)HAykCEq`9eC<WMDqSJg6Hq(rmfIAke31@kNUk0a)(RoMSg^DbuEf3V;J3MOW|9#BBpNC*1qNOo<=fC(rOcp~L&i-)EDRZH=E1ZL8@vT1s9f$VUSq=%6t-)zgbMpF!sDv+!chZZ9ENZs7KE06pRHeK7F}W~L{Y*)_q;`~)+h3A31kX0?|Pg_nDR8TkojSX1v2Ra@W?Z|oMc2QAC?R5kktqpncJg!Dc<?Y*<C_d$zsrMmG{d}*?qF(s~WICcHdh`d$%C6j;q7)Ha}^Gg2PIlSeFc#o6_QCvJ|jbC^iKy@jGhXzzVR#K7agiq-ol_ahujfXAP!@RVW4$VQCEW6PGu=!kG=f3X7Gm+`$iH=Q{ztcOYQ2+ju?{0XU*AV<fo1i6!37Tm)bO_kb$0}b}qrva79C>0v+U@JFnmov}`QY_(F6g9cn=WA%C=km+p83C6J^^i)4AT!04eVfLwzOYxr2T>;ADtviap3@;ZB+mI&3b$pYPNBFQqV`^_%c&q*bC4}u7dqXdj&kv%XI28EU7IvP>TUdk*<)AMgNcWA*RuP-9K%?d>Ca644<uV+EIpD_-X<62|mP`80`&?_afG!VqNOd_E_psC_%Yk)*_%bbFB2Hk){+Bnzm4Bte>_jl@IgG=b79m%W`S@i}EiU%_<#y0%Y)nR7QVDB`>*^Nx3xZpyT)q7gEW~f-mX3AGx+w0j{IR-!}UFZ6oh*D_0kt7sYmuC>9GLm0|DBD`Qo&8d)9Ncv0i0tX6f|OAl0`uj{HAfva|(^WzEgOf>KTSk4dn{v5=I=&;k4NviIkz03#gMLsPrFc2_gA}M!GDia0^z5~Yuh+|@6m0E{T5abyF&shL`K}<Ic%uYo3u@mnTx|;kD4MEwY?Mb1oe|I~mVjtlo7eXc&R2F#dYrykhf#<nMXNWX`BGHP0Z0~0RRC8-qZ05@q2ja2u=1jXLtKk5{oeeM#2^}|ww3w<o@5ZzY#?5u!czW1113Z-q+WUmn3_1cQAh^=#5Ex|XoCorHgGZaQ1+~IRcUZJw&NS3pX{fi+*1_o(Vr=a5p8asvQW)$5ItOdivtz<wk97`?#+BMJGVBL{ZcX8KW^Ds*?H_E|0gngCk$oBn-^)PQtVC|pG`1J+Aq=V2GnNp6pty9h64FUNv?1C{;P0nJtQu0X$2%z56%(dPn=p0SgK6?!N&wT+u&>!K1Vygk<6v2|hxs4hLZkk`fv#-@487h-(;benD~kGbpm@;O?6PFabAE`FwIs>52DFad#MMcKC9}PVO!rQnEV$?yF=}Wg?<cId1EXF~$hWDi%<Jkw5o-ylhY>_m#tM^TEQ4W<*^{nN{OJmnzePTX87X1V#4}H1t9&l@6=(3>w9ZOqYNYc_Gc9~w47!cgk!~9MzQ|sDWF_gwXQ0sf&gwFA=2fAC*E5FQAid;?K2QGW^TbD=$F=BlqYt3`UF3m5!1{nkRD>R%^a}EpGRIp&al%O_wFWw=H7*V*vR(KXbPp2vMJfc#KVh;3VM=TD9cFZW2TAObwKWZ|LSDf#9@`xX*RhwowXSfDG?1HiLsWGW?dmttZu~8FR)w9!J+2KkjyKLeKED;>8mL;^z8BuATKLFzot5+Pz+AZ#t=z7(zjj-L{}GKXT)YK%G;>e8;w7{-v*4-R7Z-;jwy_B9l7u#}0J3a$!*Xm@cXnADv1j1SzxT#z>D8=`pwSRwJKG_8&wL8;71(ridleeinrZMcd$b6{SeE!qn{4B$L_p2p18Rmb6(75qcMr7ry{mY(&`_$PT^zJ_QU3f-{u}OqQU~wA-1(r)LwJ9{8CW*${qeJDH~`iH8zMtMu5>m{-`O<zvuXOyrpcd8(|0ya{%o4M{2)adrk45LPbctQoxr09c@8{$teEFG)F~gIH}~oBTPTBWH1>EK(zLJ@2nZdv?H*AlHr{Q!dHhnMFT{{Wkh}3S4BjmTs1bp4cqdV7S_@ZBY`Ajb!<F-bMpYTOqFmy*$P7*%nQB?2`c_(WEpvdf2PZ@w-A-$R%Abq8E~(PSL7g@Zny#E2#0LoOe;jJ5>QhTqUM-bDwbTouQ#_5iUxYFD*3K?Gxup8cvO6zmAC6BJR=s*e*%ye~;humx$hy4-F%!VF7=f=MlgENE`z;6ye~Xo`Si8r9aQH0<9TAAZE~*X5;3MkLp-|-q&j5#cN4u%gAs=x^i4=T-^1!ng*287*t0{McNFL8{h%{Tl^7eKp#M2rsAQdZtrXcWw?@03p?jaK0O|5-#!>qhJvs&uLYN;P%VB)g@OADr6t2*q9zp*-0(el(gtqn^EgQW(G@wN#Dx=>}CFrYJDKr<#<coQA;?qt^F)g|qBcrZ2EQEAYwP1B|-7;WOmFUbzPqp>!6>mIA`;kWvp^exJX%tJc|0A~c9APT+HY3ZHLEU!K`T4~vjV&bpLs6|R3Aeuw1pk>V)lu0Q+xwt6oD;{CrK{Q-k7|0s`$(zR~mX4&ILe=Ib-G+Yk{4eN$s7nV#!?io#E<UxGjH?8eyhdQD`%zJn!<jX?ommr0VafbFKYLg&+3&ZIJ)YVwzlG%STX5LGM^C>owG+146g#vJm}(CdZ1%5V2ey~Lk#hK48mK&azHlJ3B?|m?pkixzmAAtoIyx+@V{&^~%jXfD7HpYVH(pNOZLKzC>A%GJQ(2@hSQQS1^dTbe#;UXjE7G2eqmDqUR6N3wvYP^=;qy9V43h#o>Pd^LcuejMX0{-Z;t`;wK8fVj==A`(x1!s-X96-N_0|>T2PGgUA6n|rd?$lfCuVvr#UE$ZpFmYuA7i5}W2D{XyFGc8b@)_Ww2k4fBcge}P|Wiq%qi9><9zUNr-O&bL3C}8G5a2A1|ol9FCllQJ!RJ<kEo|?<~?N-uUm|~Nz&xiGSkBdoVZrzL6U_n@!*QAKmkuD4W7!jD7)qZw@=HR+LT}?+yCbwmG-B5&lFN)0{zMh^gECEPg>J2Ki&IkloM@&soGCZzx#CHF^YJQOxcupV(RARip7=7_Jr-nm*&7!J#Yfgk0`FJ+(skZydrwuQ`$WEs%zjb*9S!5g0@+O3n@bRAf44E9}<NN`eSEkZs*|H=40f-x<<MA@}LJVO`fdp-W7KA^yN0hllQhVdHQm{EMM-W5}|o&<U<6eR<<N06rDbklDMP1lu$ThlF#bUQ^xL@3QfnzN`g(@eD@cFl{%DlxAnz_Gne+V$ky^A9cX5<2YE2~l+;Dd=Mpk_slo#Spb8FjNQf{tGgIxUr{A4A@VIH@;qmNoZ7+V;_R8NPojxoNMhZO`DfhLe&dA$>C`BvVUv{>I9c%sQq-CFxmTjiRmN$E3pT_{ZuFT#{hHvXC)5l8Oeo9+)qaL2mo|pLS!q1mHY?pgzriumF0Y!d?Co~YsTx|<(%iR+)?jAOrXu5ksD5P9?>sQJ=dRcfFvhgtFpjE{8*W0Qxn1_+zu`2e82h>9mTk#gc-jCPbI<6tWCb0lis>xP3fk%LY$LqtMBoF=;r^8u9lgdPh=LDwuR(GiHA-FAi#Hq?;D46iP#4fZyN9FP1E}b$DEyPsi>4++OU5FWh4+_S^Ktx%xi69DL1C9ni_~J+AK_1Wf%v&#Ew^w4Eqv(loi~bn5=!tQ2OueFi>J|B^mnW;RqF({%G8e`7({K5Xe#<z#UU+!j@<8UL;T~agU7XoX2TdgfcC?si*E&q93<4}jp!6Y;)gG>1UIF4OHn2v%!sDI+)}A1UTi2Os$*WFt$sP_H?>OB)-YL+xs70q#M0Rw5von<X`=Wq<G!VNS<_#S^>gU8OWa_777PuctV9gbprVQxKF>dqhkT6G&J~%JxgA1!6kmq46o*5SLOhrr~6BiS29kZKKT48!2((23#pDQb^-cc!?F~1mux&WC+iel_60fdfHLy0v>viIUMf0{~@p1dE>Gk^Mk{Aq<#oB-((MWt0Lnry?@s4>bZ60M`7+n6$L&qIr=<#`)22sH2~tQCo75xEX_Rwt>VoZN%){~>OFVBsk1PWw6xSCq9JOkH?$hm6xDFdK>D%d&2~`$YF;Sx?%3B887Klp1s2R6TvW+tYW@_vcW5MUSO#@>}|5{uYbR(zo$)`R<X+Pg?h`$+!x705b%_?T<il<ylW!y^SPO6BT4bA&@0ql^&(n{84(Hzs2Fprw+6@Jw^Kz-?~zMp_=v#6F11lnAWsIDGVUrzAQ@AGa1aJ$mpBLtgSC<@5gEcHjtJUcSw%fFJdjT0><TRZW6~(T(^eZ=D~y(&3G&ECPsxeF_Ps}eZ_doJl%c%S&vRGi3@HD_;DVcB&|XlLlv|}0*(FUNN&3fIfh?C_(El#6>RzK58ftXK9UDR;?HDgqBtBG*wY_@?MUhNxCiWPt?95)7>td=0p<n@1?e$34##I%E6z|3tAX9JtSzhc%nP*vf-GU`9z7A*jkkMjC=ZY`4~=~BlMZK7KvC~YsoIN{3zoMI<byDILb%8w&k)bfA=2J6Lilvi8SNi2PJ`$`7=<G28dm&*co)Yz)GHx93#5yeW=N<pS0M+8w#X*;WO&PVB*I(!GV{ADnEr|;DHUG+#tQ~zt=M{&(v8jLAJiXQQ`je4VQ*T~VZ!{%$9wme9fS=xqsnE<l9s>HTK+*Nbn|g*v~u@RNdO<a>pM8x3-~N$d(nBp-0TGqY>K(d16qG`u#N>|DkH%_pJvUG^nGiip=D9IOer3$k`Cb$UmQAtW+2Bkxt?6fJVTs6Iqv}63MPW|Z(f=rl9n6_n#zm0kPyJki+qYL@<H`BWkGM_ih0vrHlKd^7HBv<G2+1=BOZBJGx7Lj@i^^QztjFRvi#GGEJv~H&dT~Ht?Cbps{Y7JoHDOfa)^$)EBydb=7VJX2Kr?{jeGtGB>bOr&Ux7p6~9&Lxq=cp;Qs1MFCV-?!F0qCB!J|&HNQwSH}cAL>H)Cv8|ATk5(yeVrEe&SkMsLayG0Uce30sk#pt{#$DrA>DbTcDdABdd36LS|8HNrQ6b_JDp*x%j4)G0uk>au1PXiSH!`S-IX!V;#tAkbhMB7^|;&akA0h%G!$1C55zlE9CbtsyDhkQSo-zb?*loHD)(vFT*iGS9=+RYKR)sN8p5VlXr7if_9K!d1lcv<^1J?(_Xp7?mu)o*2yf3w(BSG0N*5%Xd%AVX8*S{^$|Xm!|#-6vrkD?GC+BE8bgxkiiZ2QQWnyb?Wm#PZoMmftTYRdr8_V@;BUM4lMj?1Qjo%)lgSt!Q_<+YkEwrVYo!DoEI+G1->-rmhhaLNt#v{_s2FPkPvc%u`GUh`b_AS0-}RkrCS58KGTTSsXmS0-;@NP7#?eJQTq}Il>+Sx4Pb*D8Xj(c&Obuvm!ks7M>9cv;@B5bd2p{PNB(eFCg88D(^0&(ohp%>2$8TiS`0X?8*B;X&#A-8vVQy&(Oh_1vKp+ZqI(6Q-G-Y2@|i5a?w$>eX|#xzhuB%7YdPE8VRem1Be@!B5gawazIggA|3^wrsaTA@i|xv(ZMB<2b!I4RyuEuizFlr{uZZ=7jHEyk%yT-QTKqj<OA@aL3CESMB$0&l_s8dns`1I#~k8prFrN?n$^ZJ1dFHXz~h(>B+|HJ(PqFgHHZeQcF+bK>mrW*C?vPDDi9)1tNrh}++jZHg11D_Nc-8OqUieXw4!;;w3xfmV(v~y*G-xe9u{Gg=wirYRCI<e!IPx3Z8Tv4gOEK%vl&0Q%adYiF>RL6)~On4FASM0?y{-KyiG+?NgbWH!vNSBRH5Zyvfj!?L$$I2q(5->`>lO66#PJOVSdI|JYy>u4?CAoSo`K~b7DaMs~t%&80Wace$Cr!5a1TNzrnj<1$&A4fkcgNi@oT4wq5N7kN_BqIO`rCULazK%p0B_dbQ7fLuiTsqC9eD?nSXb-xEN*6(lpl==|BH^Fv#90@TA}a<R^DZ`yL-^HVk-MD9wSgm*YJY4T=M!8T?xN!gg6Q=#SmGNCo_KCppB2C-XQcc9-|LO8)rN8PWw2~CfgP(0XZ>dO!BKl|$YZ{ENEC2co_Pt`qEQs?}m@J!)&rf@t{IIa)0fBk~rbU*Lkec%p5pD7HY%)FlsjDr3mzA=rpWf?~pzrd~&+Y_hr5-r&apza>Cj49IGD3kcDj3G*|g(oO|S5ub!aHcH(`pUog(T~nP?=Q-bMKM%~G|T8P3l{C2Ext6A#@kqQ-o|3C2c|)+pUkj+&Yv2<`cZfZppi;jV+wUw&d8+29x?DVob0ivEPjj1%HLwMnL>sHXiw@-=8|@{mm1~O))EuNeL+zrOR2L;RfdRx22JS+9`#V9xkfjLEAa#XIl{jaE*#~I-T7Ht0yO6)vJ5G~LGv2kH?v8z^KAcn;fE}=X%1k4b9QgT{`Z{DLNVKst+>g)XZZV`!S_AGKc{zCW-1h<=t#p!i;0{!$*DoxBGsyek7w?*BhS2VpmS2MlX>sP${Gw^YN&-S+_N19{b*HRr{VB*Iw*>WsLLl`Tss(ELET4_w;hc3660jb4-}8XQ-=zeQ35(7#!6qNAK?Lb{mk+~0nsQwr#Ku?IxW+jj!<btL<;GDFd-@6R%232mrQ3S0AR$ydlCZV8B_NL5hXwxgFM6%JTOoXZ8$)s(^fNMF=96G0+QrOrOp13*}~sqwQamiuV2XhOP*;(-Y_hB@<AhKJb>L|e#W*uV_RNwY|Cxa@fI^!@(N!WMWQS1l`;4NB6^JV5^k(_Rdr<k9*b>zVWNAOTSm7@$V5`gKtCzlGbwYT3XQTzk=i49b2JWol(F*0qS)gIHx5VCiH1ZcPv%3$Gas(r+``{uwb61a!J+X94z%N7(0)MK!o&UncXc$_jR^3N_8)vYie;J^coz?GZdSaiEu|}zN#+HTV#l4lKRoFdn%8o)mk^Zkr;o?sJ|4FZUn%MptHeb-K5t%kQC`lv+wMmgyMS#M3#*}CNo$$<bq<k}5pqUN8J6rJBr%ko=qw9O!ft*YTIX+Z@KVO$P+Q8A-{^JUoahkjAUIs}!rc!Hm*t(?{~nQdLa_T$={X8@WP1Ub&aEZ&6c1qEJZ^_TLZc$@++F~wks(Hbj0AU&rP^+k0@P||(y>01PfVPAsC@KU#zfvSM#bzALV?4`65K>VjTBAK6rh`@0D%I&h+9D1D+efnr90yLm%<vu7h|YyR`GE!qD6J30qtf_QjNiT;Jx4@pCXib@07~2Iw2k?JTU>?)l+cWt0P8ss%l~f?>m(|m2Hj&9vuP990ssfoSp(QNSBY8W_G%pgJXf5QV%dZxW321s*2^=N(N^uwys!X7`>bzAnov({17@iV!C2t?P=x8K$P{gMbcEKg+!B8I3<t5DaAFtlFs{ih6+7Hh1NoazzV8*B2w-bD+G=<n<pftA>JV$Q?gKW00KO{d!U}2sJCIltqM^N(?C7MFfvl}#1RqcLMS18F<!{9L_|5{`6GxJy0OCulrSXItPXM*(ZV4hPm)J+7>R3EAxojFSMTqhsjJPGy884dVHifi6J-?rQAUZs#q5hR`iKllU{?8)oTPQS!ycw-Rvrh;#kAaEWJ)FXHR9l-dy)wzJq!!<Ff1a}q($3}jdLQ?78-?i%<Ht*#N^3E03Qi%L8jk8W3Cx!7;*?6{69Y2MxP07uQ{V&H2dFk<5`6)G;AV@IoiQIDl%;ofKUzy4?UF*AXln=CrdnlJXsd)Ee1u_DmJz0kgz1Uemq?Sk+n`2kYp__mZ^BGL7L6xF&%?3N0DheeNY)olV@H%<9?oTKQ=>W3m*Tr89AwwQ((<ZG*#_0#s@b(L4tgsAe9DetHg6<G9BB<vuoNSyQVvI8;;-v#oU^9VMpvc3v1t5S^LfoSf$8<*uDHdv6x_m6_6KM0j{L9>dXD@yeG<_bAN+$Hg`uy%_lkDGKF_IG)0B)-;1YzFaG|$@cnz?q4zBZQ5+5|EF4(DP|HV(tHM4(!<BX=AC8fyW`&oOTcvNZrQoW-n2=$nO6i4}D%~qF>GG+56p=|+TlJZl^ccBu_a;1LSTeMNPjqmO0g4JDAu71q`MjziCc1qrbo*Er+s9_NkGHTEQ1@`yucCVTJ-sNuCkhE_EE1&KM3n`bsLJ1CbFg*dr0vn8gQ1raeHj-yDm@lCYSFXFVgf@>Pm|{mB~K1h#&eiZPc-cwtIc!LSR;_p)BR~tTGW$HhsQ4WFriHuaZ*DJoEmH3)Y+Nr^h7Z2Hphh{m=Y`Lj)j(u*TtBpw&OGx1}k(E?yI+oHwsU2*VqAt#+7X1m#!VwlbSAni`}A{nj^EkIWo(4BRLwioqoly-o1N!e#IpnaQ7&Wmvhe9WOb~8x;^Xd)U?SOJgg)vCH*>+4>Afg+e>DucfOE|8&p2Dkc)gilj5BtJM=ixV+S_227`sju7%>)Wt~FECw&2aPv_K$U@yRiUzoX6@|a6GT%wvM-l}`7rGQ;%VlLaS2qiDNclZ>GU#J<L6OZt`+LU_&h&oi6c^9WbBW*J77(KXST)-V8k2?ajc;uavlPeKt!JevE)p@5Ga2?+NdM1~?|FKZ6=nLiAFR!BGAuMF3M&s|X^TO?5FCh$I{Voa9<C1U>SE}>A<OnM&lq4g2^c38=60;Dhv>Oneju=-X)PV6Ok>`~UKaYX9WZZj$7rto{v1l(Lyf@N<_eNsRW6Sxw@wVEX_N=~~Z=7?C!ZWz-(BQVTmc9muCK8mp9aGAX4@+Wo(s?Ztt+Ha~zQ*DiG#^K<Ei-TXs3qD1r@Cu;dl5c7J$#V-Deys5C!2l*CFHz}2_7SxxX3(7ypc`y7}+#?)JaG(T@%uVdh9-fwH_f@3uY$(QCYBT$Ej0?hwnQP6EgNaMzmj*r47*Dsbh@*09d*c#BKzbY@T4MK`Up&4z1vw^PdK-(=rmH99pg5i;POVWlFwx_ETI5a5Ay<NAz>qcyg8YS>dtp;fQgXd=gRgq$@e>UtEbtl}Gmbjv-0AF=|f_&dhkf;H(P8lcn31CpfF3tR)!1u0WID7Qq8DD}E<(<v;K;eksxF8AbF$qlj*cED$8k?9lk2!2!u#OlEs>m{t^WMhsD-?Nz!fhG_EE@qtevO1x)w<=w;kK`MC#$ZL)$kS=+Aif?E>M#9$&Qp@1|a3&r18(Bf)mC?-0!Gh2*k4SDeBlUupjZcqiJn%so$rF^39X?lbBuC<70xCGXNPEImdBruXt>I3Jgn95lbFfc#Vlpv!cdmgKP}|=s0tX*FyGW0&7&hH!i(nCUjG%!12&Cc3^<M=fJYe7~g1rG56mXS*AaRWa$;KLbHF<3@ka<jH_I4g7>mHb_^Nq4gq_vwUnZ~<N>*kw7UTU1*+zs#2V;&N(EG~<<T654K<D_8_Akcu=zbdg4v0g-L4&-mED;&?}h#MUXdc5h8<HZB?ikY6^ptH6(R#P1JoU7a}3<2xvw_!boNm^(oY2hu3G%PTAd>b9%3DuMD(DoV`$c{vsShexZJ%p~6JyRJ5&A`$@tiXaxmlfDi;1UK=Du53ldL;NcntU;O<crw@6E#}gDhH&wU?NJs$d6s~8WU#GrJ}pcNhdEY3=Z`pVyzF`DLP;y1v!)XKnGBJ(hboVtQcqxqx*oLK^U$Q9g(~-`6PaYm(Nv?#INz9#UXv(<C?#51m~WRR8@NagNLyfe0t=trbj0DqTtjMHBTPA_myT#Jg-rr>>1GWy;i2r+3LuP;e*?UBUqjuYD5u^-?3CcHK>c;=bjix<(Cn*Rl`FTc(e!cDZ&+^`k3SNV=gA^c#Mm7b39(IAQGJf(csLdZ7dGwb95e$>-cvG4!W0p0wV7d;DUSkZRG*3&|!Rb%>RokYk1Iu^67C2<p&E@R)RFpi-4zC7niYcr*XC6uob2qd*dRW84G~E>c_bD6n*pHZ90s_dtW2bM4GeJ&~_h<JBze%RqTCk<15LFW7No`wj-Uy@%e%ob!ETjqzp5wBe}HElg#1B5}o^<^Lg#eR&~JD6T2H66#K{<po`ktxHk7xS=h}L%Qooo$n@Cw(kYu)t`J}U?d$&ssfdp$')))
