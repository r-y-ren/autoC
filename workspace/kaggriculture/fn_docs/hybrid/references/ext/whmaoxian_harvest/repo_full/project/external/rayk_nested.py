"""Lev Neganov episode 91587143 player 1: distilled trajectory with the tested c17/c27 controller."""
import base64
import copy
import json
import zlib

_TRACE = json.loads(zlib.decompress(base64.b85decode(
    'c-rk<%Whm*a{L#rYav#VY{@&eR5MKsTNFsjg>i#uG%#ZrFvg3vcZUDn6d(1t85tRwc`hYtdRL;V?mh3585tS*%l{tz`)|Mh<L|#8{mU;$pU!V?j_wvm|MA;@{q4W+|8W2DAHV(npMU?K`_I1|{d94?zW-nP;m6N^{q_9g#n0!LM~kEPSDT~7vHA1OPwVxkqs7Vdf84CsAMXFW`DuNAd$c&6{Q2kg<<-Z%KYzNu`tbSv?fwt${%>*6i;MSv`TS|`{oDTha<p0B+&(mP`{Ak2dq3N@Z@>HAJDwVG_?C}X*S9}CJaqTTzUS$u^gU0_RG<Ch=Znh^zuy1z_VbqsArGE>Q*Zs{`TO;DkmwLSee=sK96bO2KR(`WXV!VopY|68d(Gh&59a#(c75$V|NVI|K#yO*<MP~t=a=q1_vuS)Tqc_gJ#N?Z!qnOq>>dY}y*{D#x!b4t10qkPef-VU=cfS&;}K4vKhC>_XNRLQe|xR-$3dSzyXSYOmK_Iu{?_Ny=PCmt&mU;EGA`jff@VMe77WK@D^kte{&u(Crhlq6&kpa9-ORe*+0EOBJauWzCRRqHvX|K)JbXwz4%s>3br7z!_g9yf>-V?6{%L)EdvSU3Zx7A1_epB47OpMS4Dx{ITQ1d5@Yb-Q!RREL{k(TaPEfr0-8-wWmjC$4A3ynqesXvw-mEXbxNdtp<<TR<9-#5j&hAqF)7A=!Pafa=w|>^5c9a=^=x}IYhmY@)XU(J^o!en|DOMT^&VSf;rG@@og4-DX+zeA}?>*TEgNF$WJ|3k?1E=<WY7y*tO@&w60WLIQH^8O^^7w*ja|SqUAoDB>N2wX2!ZWrbWPhuU5O^papz>|;&+^;qRd;ab9io`WlRw|wUY~D%Twh=R^=PpwUWSto!!N~A*W=f@D7#nYvwONXQ{A3OuGj(qmE|i{zc*~-?6HPNr0rHsuiw@^0sKCC5s&DAfjzS$1SSz-ov|;eSV+6&QF`94VJ`kX$jtOi56uX%_QC`cY+belHJk!a#YRp*x6ak~$3w<Eq-PhjJYI4pPQ#^t-2J26<zC~H9$~S~#(yrlXpSTOW%Zt4|7+m_1A|Gfi8APrFmb>`K_IQ-Bu`yzsW~=KM3(c{m;~MB-nLHa`0m@-1GmxdsON%Dp4lD5J>TBS%7o}1xebTPvm}MWDt-R`ukPoQ`-cZ(xaQ_N<R;zwKk3nx>Ymc{`d?;@g9hY)Y=qbai`~=MQtBHVU)w@J4(1D(3xpiz+YRxl?GeJpj<UZJ)zOX*VUG<EjkDSZYb)&T%k7o)_@TFnrjH!~>o};$3n1MISDeKJI<B~iqIIrC*3J5uDsagQKcp3=F~p-6nt|B*9f~V_xW4*yRKXISjiRfoOGcu8T0kpmEv&vZYhm9*c?m;-`5$>k;`S&Vf~w>%#6&!TVL}Y(7&Y*~6&;R<bXX`T*ip9&^pMgE4E?4u?#!}D7$f#Ecp-!jvd5=c2gKllr}ygF`@6q)J{-lSodp}vi-;Gx%zL3rm#Veo{^>GzfGA^Eb6B@e-Y!G>E^WyZ#|I`OV9O#w?j|`h5C8FaJ0G7Oa@@)Cp4{ulnfQQ#T{^A?0CD69dp9n#3V@tiCfl-zs6705g_o)plaZrAE3)N}-?)4JWONWo{WJ;z+I^C~G~=b{n{Er4Y?5l>vW_x={J8L|8QV~?@*^(A?wj_&uPmbJ36J|maFQ{0T(F7`?*(*lL`!J^V62$P(N&mOPo;p~b{OCUnNb@tDmF@nK-TRmZJ=v9Q!TFrtmo%Gez^EEUd-+Y<??IHA`KUVF?6{lQ=SlM`v$SON!we#32*|zk_3BV0MW`GffK7v>9ZvVXe2`|!D@lG5V^{205zNy2Kds9cYk+hlaCK}i|q`=C-?U8^eXJ((x_X;R2Rm+7FRbU#|4XH4~uAnm(3Ni4kq;_=xO_L?wyM=(ji)4CuC&gnY&5`oFJw%*BL3IBfgC*c_KUW*N#yq@z#0W{_(vX*oLoBN#ZR#Zp}n9?1@?XX%?hC1ed8ng3PSiq9BeOnghssnt5?ptKBrqI6oD23Tm~xrs|-O!tNq+Mj?~Mrx05~blY`>bMFdf(a9e;Skel)4w(7Cjo7`-jJ+F~j~5RMT7-7ob~0GnY2t-w3y0@yxQKv%=br}9e{ofeYA2P?k#v!c?QkgTsd_qr(MQaY5q!?+4ZR3xvmFzeY4tGJr(rAOh}~d&+!r1i`=Yo5!%Y02FE0P`MN$EiSRY~jNocJd5NTQTOUK~h7CmzZBICY-Wk&XLEsP;B10-uWXC4pd6VPZzi>|WDnvLMr4==(2M3(|#B=Y&<1G~a2nJim!c-Jx4JP$=M=GnN6@;Ru<xLeSL<<dxe1xq9J4_y2>XF?NxxMO!DKv1R#XhCScX!C1B2^4@Rjj~WB{)K!Kp{0mU+0ap}ZyR9!bN4t{l!nul)W5L-DiDhhW3mPC_8D;}-sJvjt!utPD{=qP%pDq+SOr)63>16v{)r&YOc`WQ+;XND#j%D_Z<>(B&eV5KxngH`rL4NWw}N29jtDu}1xbxi#wUYr)w@BIvO`t#cO(e$!vLoXoSM4RWs?sX8HXCb0ekIfG&*>C1P*aSoOIBqvv+e8Tpb+A{{vGix*bJ6UJWk;&9r`_pHJ_Yqs_ip8!Vzi>>8hPFhf!s3&@GX(ezoV@yUZ|Kt5cXH5Pg-c)->mjJFR;lCpNLlSTwsJQb)rwPxh#Lb&D_lO5G$m<eE~YrBf$pyiDEODA(O7!}oNuK`Z30(L0qQd<-gaHca&H90)?3hJBv^=>geW!b>daWc5papK66*>Hw!E5?O?r&HmPW*0g4oRQO`kuE!wLRX}c17j}AgP<Ted%M>QdBT;iIP?*wASW~Vt3P6*N8m?j0I~ahyFq*i#q0QVGt9DnNr=-MCTfFbyIBI!Fd$Bp7NbB1Tk4N9n3|f-QJk@Lz+l5}2B6*!t10RXk6DT`*OK4+MVzLAsG@2$Bx=0-zwO~L3~lNxP0-Ty&21HU8HSiKZOt|-mwyQ7Cu6<nk}zz^G<)<y9EK5jnlFhGMl(B{D<P7fA!<j_5;dK4D8aRgN;Tm%bnBG>f?g`=D1Iz+)q&y7;EPH?TgW#Z$k5P?$PSUhpLlA?^5IOVzc31<O+m`=f({&OWz6O#b~7G+tXx_hV75Lj?vPua5_VA}R)bgspHVL<Zc$a2r+g9eS`NK2&P9b8jofNKhcK4MSMyWDhN1Ot6AS=(jzR_%)=dz+=)<nPp#y4)9Ev9}Dkm=uk_D`;_~A{eEqOXvErLgQivuu$K!m9Nbb~qJ4?iS`z=Z6X7#w+;$_un%9!~o=>ysX^=$C*+|K^o>sg8hHO4vHDE4>o@TM%<Yijv&xJ(w@daoPXMGN%M`=n22QQ$+2HzC?~_Ggyrf`wOAkcD|9bYaCL}E=NN$9x;;E((}c8*$n{~n8xg_tu$21+_y3g_^eUGxBqdtd&9uDv5B$;DF9r=R4^nW4d*d;vOjbl1Y{F$h|^l7d-#&*cIC-zV;UNcJmA^LDJC8Wj}qaWskw2OI}yg8(Rs~NJ<1|k{>lXd>lJ`mC}mv=10AMlkfqFn$J>Pw#hbxFJrkuWa|$!SjeAA%zN3jIXrvV970iz7%_YfP>VZlbtmIAu?JQ*KgGj8IN@vcK_n3WCX<Vt)lZ6JDwlfYOE4zuci#X)+=GnXL;`#S7*4q(p5?tqz3l|R<<?Ac7hFaprQ%cJ6?rT92<4RUN^yCEO)|@)||L^wx-ixx&F?bOqF-Iw@zWjhEB$}2X7#~0XHiG5fMr2$IFp?PV=<xT*@Zyl_D&)4$X%@6~$dHv3tumM_(;x%4)$2$!&$pK=EtR64p=Llt@JuW*+aR=Rq{N3_^$^a;@N0|YvXEGC7Z{|S5L_+xZ9lLqyL_dLWlF{Zw5G_J&tXug;;#nF*<s5F@DW2CnB8bmsuA{@?QI!F6zd;s`BS>M_I}&$!8PxSA4aIW)jkaN#b)tnzA3J;tCzMP>D>?N06~M3SL8{(q;F-<Q{A`nW3~Bk?x<QM!1sdmqc{}WD{xa11}HPC#}`dD<0SEuWf))6lPlE2DQ5fgF6hOyh)YQ$H&PT;GMGyni6;e11qhT%D#Nyvjpv23V~b{?=Vf^>0oJUyICs7AL+LC@eW+8ADF7tXRHaWzKVj{&lC>0GU!iQIBp=a%ky8>X<Aa=f5cpKCFz>^R)tF)c4)BDK=Qu)!kTCtJ%3XqmEuH`IJw%oHg3u^|CVXOi%DG?y0%V&2KYUXFSy_8hcMJ%}Nz<nTpMoPyA(3FqFyin$rRp_`c7!_=V~d3`oipe3Ye64#j2Us?-#PC4+wX&uJs;INj(e_3xx@|)I|_-OG>O!WY~t{W5qQ&FK?8yWqYKc=^yn<bJ3u{VESk$ArV6E7(^hXNbh}w?Ia0R9R#w}o?Hr_8qc?Pa0R)R7znO>>6pnmTrYJU<Mkw;->I`x1s(#T-|7i2biO?*!e=KGvOF4*n(i|mcWSE;QTu)~f9D}9xPFdn|-2_%~O5nSb6kB?ZVy-y>9U3c}4ipXL`_cHKh!}eB{s3&bi@YWlW1m0TwFlv+i76$s(yaiK^)jh(NS*l{FM?EbijG(Ep;N1k$Wze(PDSOF6>hVyClotNZcZd-=UNdE+6!S>yHxkz!Kwg6e2{s0wg)2i2MK;l!>WBJ@NbKW!vj6he3ZDVXg{X-@6wg)YmjxJtGaUkCltSjzdEhd9`0mP={|Wz6^PtrP5t;xY%am16I}jIFXju1Ya&QmuXrrAQH-q+JP!p$buUXx24-1xF_PZZWJ-iu1len9?$?5O2{yQtfX6~BzJH#r3{XosW@0jIm(@ZquJh}sdksramTl?kCR|GzK>@wCljTg~uK{^P*#3d=zRu%9QBo~kIP$2I#~(}IjUSboq)201xVGuC;yJ-Zg#s{9ta<@Job4r!amv1k#hBXUBP(lAtcCHUT1$`hPGjm2kU0XpwJ>&bK7!*1U&-!>vSo~v?3{pdkjAJ$QS>;#Y+B_mAxBP-WL=clW9O@yQ_t`V;&DmPk2GPdgG}x%tjZWp){ry;iAj;Cdt|MH7fXpK3hK+X?gy-&`MNQ5?J(s1ZID&J4*;Hg)9jL=q>`5d=m`I_?!$7_Z>ekWb+YI|Bul9vT;jxzPiqFql)~$6<>rx`heWL!l6q1vcAr>$oSl?_&I+2zfm%+otuL?MKvI}-kA~p3EEPbf&M1i^HAG9pe<^Uh8MrCcbo;@H-P!u|3Ja=}sR#X+MDIa!TBj$Zg3%glenO$$heG02u;uYxM>9#Nb3U5ZCnc;UAd+ZB!TG|2q-1d=MKuNx?^*3?DuJ);cKcpIybyY9QiOwGZIW{&nJy^}IN$;m*i2FJVqJ#5n!qNqJ_@gu{Jeb!Zuz#u;CS7M|2@I?<<}N`2bY%5+n{BlO2@L8T@cx*T3xmduUd++h^HfMBuRp3s(~p=?g4R?5_uak0<&n+C4}u`sPg4(e_hy)M~zYu-t4|r=tX3`xsZ$yi)i3kOd$_Tx#vg>gb~$|F~}z+rM2K0HGzMck=8}A0_MtaV!N+6Fki-b#25+i$|PB#P>1le#EoRpYE53Am98h*22&gI^sZ9&49YwDC@0+;FH!qZJ|hz%AIfo7sXIr=N18Xu6bR%CZ>01rjiqa1^<3zK)vdGX-it5;9A$2;eOY&<45#^dWTTJJD9Dz3_isN?^NvNStc#t>z?U@S@yQRaH~v$pik|F*rd;XE^Y`n0U3f7#O%kl)u|B9EH&l>*Q_rONigPf(?7xL|)Rwn%f{Y}^t5x7n<4AeHXm*AHgon;@LKZa7$4w_m%U@I~0)+WTDq0ixgL<;R#Khl7bikx^VJ5@pB})<b(wAwNPU_-Z<cowTCeujyaPj9*4vs4l^w}EHIJyCT!Ml|Tu-h@I5d);cO_JzlWEBg_1Fad$r_Kcx*GLsCJM~H2qLvk(aCTLOiPUb<)7!{GAZcYtMp5Cl-Kh}Ah=Kq~LVbeNQOpQ=J`iHQ1>-WnJW3C^NUkDEy0N>hJw=2Q7NsEJ=(mu?k_&d{vR2j2O~$ku9Lj7Pri?-@14Vi`o4paB{Ob-ufurzx41+%ro^!Q%NOOcD<`vaRYFRziIgyf(#kC_J0`96FFgp~uC&NgcoQgcUxE1o}mxXj_Dv-j3GQ-C*IRxe!q$0UIEB+Vu`&1ZM0d(x^m82{&U+4i9Jpi>%?m{Zn@yT76jkP+#7}*4^UcSbxn^8(SC#Nrjuoa575U{8KnhC#ZR(1)5Ssf3U{6Z=LGo)ZeraHQoXUl0*9AvALiFGfZ*p<7ZPf;47I=0a_XI0DDUYPy7{1l?Wj0{O~72m?^%d3xH0QL%nEHKeT0vU`Kkj@U3%^`SGyhWjsB-1e{F(gv+M$mjHVd~3c6eURlZI%kN>tx2_ueqHol@!`p)QXJ5<G0xyA7{uTqS6?lzERv!@>?rNq;MC90(cr^XMP3_^uoqteFAGEBh8i8)&*k-cUz-N0k4E1#?+ZlYAH3MgG~F0z@e=|;M?iXEmaQUR;D(}me8b|Nzja6^k5u<h;PuJX-hc#>0!-U_M0Q|v(A9Yf`Fl2o;<Lum0Txtm&W3->qV^aAQ{ib-q;O_8TI5+pmbtpda`oT#g5VIR@RkgHh1JUC2C}o+U0mUEMF|0OOg`=MDr36%M>1{wGn{!5}1zofC*rW312XE7P5XQSShhz85@=pd8wNIb4MVSRwDrJY-fi72uegR-+cG%KQz3flSg+ssfwocm|W7}oy($35Hyoui#bydUP2ypd#n-1M#~0AiLorHj@d&k24X}ck(gA};Sdr`r?>lJZUQ1`9LcFI%FsFn!Ympc__hmkX+;)G5-iM}g2&CGcM;S?Gjp>k>dmxOW*`T~{=@KHTz>fV{;s<HOsc$961wY!^a7`iXg}>i0S}SZFE`9S(F^cn*K@HbsiJHmvp5V-(Q<9`lucHkWLeH<%}S|7tl36UUSM(q*0eqN7$M8LbcYMAHzodYV7IX>Oix9!z#;|?Mu~@LkAvy1Wx4*5P===G6pOm&rJ93dL6oKB)Ul9Du4oO!u~e$Q9#&@yt04L?B>@G_6580L$_}Jx5NI?8(*R7+DK}vQfE*g6`RC7vkOdGP{wKwl3QeNjKmf!T^0p3OD1Qz-;boFch*AS}H=of@{Ic@&;&;o;)mUq+g{-0-2mYko&prGH>No41*v0ZlCORSfDXF?4L+-54v3uj>r=FU`<hKafT)?q?wN>oqtFRtxo1F-F6qP$3p_Hvjk%c#=Qg(e*B3oLvjJ9$}(d|y1Hy?kA0xiAD;Y$H#$z-Snkc&#S7*t$7lkh1--~$7P)+4Gce|jtPWgL`{1OGk8idQN!7MZG>ls<mKfuO6Js4HppduFAM>VjPfuy7sf80EydH8%jo*Jb>2Ks|QW5FXPI>P8n;-j(dl5XTJ@BIkn{ecBk+K%jvZ<1RK%Gm%CS(z5x@&ETmq^N>|D->CB0d^j@a0?q7=Y9F$*!K{bCl1NYz@#RV`G9)NNNY9B=0yL9vXKG<?om$4Kq;=sC0pd-<v-15v>m=uHG^v=>6!RG)h~F*QWj^p`2J9o!zOod1wu!ZojM0phtlxgTa^Q^bQGsh#d}Adh^htQfiYs#|;J8tHkMk1-XZX-0Iwl1|{^A>$O*Qp-1-DeTlI|3Z;=Z7k<>a?yUMUNF4OZfUy(&m?iGuzI@w7HOL4hTc3o)<Mm7iZFxGYn?I!LHg$1Mm@E5x-ZDWr{tLRJNAE+aosm>^+e%cx5#r*?pZmn0<@@T%G=2MV&vCWqo}N#zle@GTv^{mlr*y&?`45PDIflPn7+Z%2uQQc?}WZZpdoWm;E-`tV^O1D-$#>#zq<QqQfTNe}R;bv#h|@*@X}t_?YvyYy~js_)XsdV#^3lw(NwpdtzRdT}IalxCGF6>ZG*$xoTd8m|>g;A&!EkD)A#Oe&#rc7!{vxCm(^I&VEh;;S5vrDYyV%MP3^MsCV3ALfULprz{|ri;>Vh{9Jy_x0FZc^c>QpipYGgPf(i3>Zm(-KGh&3B@r3)>c!bZ98&AU`_cDh`o7=ZbR!$E`!`alUnvlbj~`>uVIwOL&VHh84ecwaUu7QB`rjjax7*m(a=+^OQm<DOGzqK(yK;QDmAH2$>M-UDNRwX0a+*;8CQYv=686a0fh`wTr5sxOrTeG{p0Yj?9<|_(f?x3Iu$l2XB%kh9yx$9PKt~>mdiM^iBGI5IdSYpxUHe%4Kxg+pQOs2jl-j1PAYRuGlkeCB!X!#7b~#`GJ{eUI?(pwzRLl(o-5rRno+44VdIAu6P^wz9N-fkheAD^pBwcdICYh*Cpf@7&Zp@&TJQxPwUW4Iux2#96ALSX^$j%Ga9*14D#sOK0v#8l@=-py+|4Q+U0fs9h23hnF2%)Y2tKRTn;bX#DRxN+TxmBA<vA%v1S#6c*c;C~mB%8BI5(Dlu?=NQl_)8BbT~g$M$%a)3h#^7j@$^n21#`crb5V-atpia^2;_S4eCF=b%yQ-R1Wm}6NbveJ10d7+HoH4S?L9v3SiH0KAD&hRA_37Jr?Dci`hz>e6H8<YK%m+rOXTSSt;rJf|2?+l2WdOk-#f1BYeNC(7Q6(6?!tFpqZiT*^eQLScw(JxGPh&M({wG4;kr3X=x7Y8^yQ(c=aG)UL<Gbg62#wN0c<_rJYFyu2`A|^7A<+<ZNy@>?tY~I*dX{jP;1ED!O-ZU(}6|IGjME%VoxL0I*(<jwQ|tN_Pwp6Gq+N12SV#B0GroQ#TV+tsxNENp#@50zIN2zC<ym$ZT9_rF69WOcGW;Pg}VemJE~u)0s(*w7721sOrceV<B2FF%OQ^xgk^&@F!0LT39I7w<YEHB)SW0==58n7&ry-Ydrv&j7s&wDH|xI;smHfQo{-yosmqNGY_k>O5CRauQ~f(GXpcK!((-j3Izoz@=bKCH%T&X$#W&I4ato(ajrtz$)ycR=eluN`;DGYPKnqux$1zCoF@-`GH`qz0Vdtm67|c?wA&cvH>Jm<dIyZa>;9iGyCo?n8wpM@qiON9lvSJ6aH1uC!jgtheV!yPEkd0QnpdLC3DJB4-hfh8G-j!Up?|S6%K?&5VT3z_top%H=E)ibS8e7PPXwRT%s;2*gy!BV+zi^Ilx1O8O-x1P0SaG7yNHMMs+>-a1ZHY54e7=u+>o-`tZQe7mTY0hM7@#{Wp@}6y{#z6(IGd@&N||cW0~J-RB4Ky3Z#S;Gbn6o=$1zUhA1cU6u^xnvH@TKn9^hGcWEqe=?1o0W^iLOy9nm-(7FI(ZQwY8%*^MuEyT+@R4)%wjaY6{ez+BMiPelCkc1=7ZoiVZY}mkqVGTV4jV=`Sb;R&XAX+i4&F|evJZ-f!xY=1kY3p@YyPG3JZKaibSjCBF{I`i{(k4-SN>0L|JfKd&xrEFUO>yBmRYCFK!Bv=Gro5;d6JZHLHeGBnTEa5r6rmJ3CEsq4ZWgekq)?|4r31#loUWEL{p6y(brC4$P-WO?*1{2zm2@IhMa_T=icsk~S{>GkP0p>|7F4GW4@{^^lp8Xg;*!WI4ZoTZ5hj9oGXF+nd@1vaP%2iOOiGIuiaQskmSf~pA&{4=FG<BPCbMvGNSRpO9lD8YW5#xob+LpzWTMPMb+Bz>BJh&wZmY5yvRS-4!yM%sQf?rvcv2_LQAjE{V^BsY8C$>hSD8b?DpL871?b<pErn9{Ygx(qPAke%F`B%1*Vlep_@~Ft?7ze1xn7ApOxw4PJSd#79CJ^WrGy|orKTd+ujp44#jU%UG8%Ivr!U+!^ZL<EDX({A939(sTAGe)wvG_A1;$P-C8}7SCn<uMn{X~jm;t2#Q5og?vsxO|_SFoCq`AOiFp}a0>jWnWCBlw+)X<kS4x*;9br^YJ3160%%Mp%1J8SeT(0%tp(ejettDr3Fl!|q+>KM&UO_1iaRP$yzG|DrL1f?p&6iLD;GHqeO$^w$YHg~xDnCq62!~@q7DPz9lQj&}VhJcde{?s|{PZBX;Aw|G*hD!c74eTn_lu;$=Qt`2rkCV%MXeC(;YX!?y2|_u{Ej>FH^egu4k%4Zhl>N@)j=bQ3*b1oGqUkR%;#$qAWI?#d1jl^3u(WEsH31k;=~(*6z-dzSkP><hnUjyzmDJ<49%4XM!n30kOIyZUE6jnZLhtKba=t=bZhN8ixss#uDdj(|-=P-v%?Z~MX+>sstCP1L5?pGROwP??F=7Z0>Cl@aGfCog4J?c8eH~O{ZepcGLn7CqI@xXnxiOfi*_G-+@_MO2uDp@@cnfv4NxPn0sTjg^{=9X?><7jT2nrS+)-rgj#BQGA4w;N_>qauq$o_09<;g7l<%!JmYy>Km9)YeQ6@kO-ekvGw>gpGc4TXV~m8zn!Ywt`Ux^Vb=%{tu1cmEG_*RJ*'
)).decode("utf-8"))

_SELLABLE = ("STRAWBERRY", "MELON", "MILK", "WOOL", "EGG", "TOMATO", "CARROT", "WHEAT", "FERTILIZER")

_FRONT_RUN_HORIZON = 1
_FRONT_RUN_ITEMS = ("MELON", "STRAWBERRY", "MILK", "WOOL")
_BASE_PRICE = {"MELON": 250, "STRAWBERRY": 120, "MILK": 160, "WOOL": 200}
_GLUT_WEIGHT = {"MELON": 3.5, "STRAWBERRY": 2.0, "MILK": 2.0, "WOOL": 3.2}
_LAST_STEP = -1
_CLONE_CONFIDENCE = 0


def _public_signature(farm):
    """Compact public fingerprint for detecting a mirrored build."""
    counts = {item: 0 for item in (
        "COW", "SHEEP", "GOOSE", "WHEAT", "CARROT", "TOMATO",
        "STRAWBERRY", "MELON", "PASTURE", "COOP", "WEED",
    )}
    for row in farm.get("tiles", []) or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            for key in ("animal", "crop", "kind"):
                value = tile.get(key)
                if value in counts:
                    counts[value] += 1
                    break
    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands", []) or [])]
    return (
        len(farm.get("hands", []) or []),
        tuple(sorted(farm.get("unlocked_quadrants", []) or [])),
        tuple(sorted(tuple(position) for position in positions)),
        tuple(counts[item] for item in sorted(counts)),
    )


def _signature_distance(left, right):
    distance = abs(left[0] - right[0])
    distance += 3 * abs(len(left[1]) - len(right[1]))
    distance += sum(abs(a - b) for a, b in zip(left[3], right[3]))
    if left[2] != right[2]:
        distance += 2
    return distance


def _update_clone_profile(obs, step):
    global _CLONE_CONFIDENCE
    if step not in (4, 24) and not (step >= 48 and step % 24 == 0):
        return
    farms = obs.get("farms", []) or []
    if len(farms) < 2:
        return
    player = int(obs.get("player", 0) or 0)
    distance = _signature_distance(
        _public_signature(farms[player]),
        _public_signature(farms[1 - player]),
    )
    if distance <= 1:
        _CLONE_CONFIDENCE = min(8, _CLONE_CONFIDENCE + 1)
    elif distance <= 4:
        _CLONE_CONFIDENCE = max(0, _CLONE_CONFIDENCE - 1)
    else:
        _CLONE_CONFIDENCE = max(0, _CLONE_CONFIDENCE - 3)


def _front_run(action, obs, step):
    """Sell one premium line immediately before a clone's expected glut."""
    if _CLONE_CONFIDENCE < 2 or _FRONT_RUN_HORIZON <= 0:
        return
    orders = list(action.get("market", []) or [])
    if len(orders) >= 10:
        return
    already = {}
    for order in orders:
        if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(0, int(order[2] or 0))
    planned = {}
    end = min(len(_TRACE), step + _FRONT_RUN_HORIZON + 1)
    for future_step in range(step + 1, end):
        distance = future_step - step
        for order in _TRACE[future_step].get("market", []) or []:
            if not (
                isinstance(order, list) and len(order) >= 3
                and order[0] == "SELL" and order[1] in _FRONT_RUN_ITEMS
            ):
                continue
            item = order[1]
            quantity = max(0, int(order[2] or 0))
            if item not in planned:
                planned[item] = [distance, quantity]
            else:
                planned[item][1] += quantity
    shed = (obs.get("private") or {}).get("shed") or {}
    prices = ((obs.get("market") or {}).get("prices") or {})
    choices = []
    for item, (distance, quantity) in planned.items():
        available = max(0, int(shed.get(item, 0) or 0) - already.get(item, 0))
        quantity = min(available, quantity)
        if quantity <= 0:
            continue
        price = float(prices.get(item, _BASE_PRICE[item]) or 0)
        priority = (
            price * quantity * _GLUT_WEIGHT[item]
            + (_FRONT_RUN_HORIZON + 1 - distance) * _BASE_PRICE[item]
        )
        choices.append((priority, item, quantity))
    if choices:
        _, item, quantity = max(choices)
        orders.append(["SELL", item, quantity])
        action["market"] = orders[:10]


def _terminal_liquidation(action, obs, step):
    """Replay-derived safety net: leave no sellable shed inventory at season end."""
    if step < 680:
        return
    shed = (obs.get("private") or {}).get("shed") or {}
    market = action.setdefault("market", [])
    already = {
        order[1]
        for order in market
        if isinstance(order, list) and len(order) >= 2 and order[0] == "SELL"
    }
    for item in _SELLABLE:
        qty = int(shed.get(item, 0) or 0)
        if qty > 0 and item not in already and len(market) < 10:
            market.append(["SELL", item, qty])


def _shed_access(size):
    half = size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _move_toward(pos, target, tiles):
    x, y = pos
    tx, ty = target
    choices = []
    if tx < x:
        choices.append(("WEST", (x - 1, y)))
    if tx > x:
        choices.append(("EAST", (x + 1, y)))
    if ty < y:
        choices.append(("NORTH", (x, y - 1)))
    if ty > y:
        choices.append(("SOUTH", (x, y + 1)))
    size = len(tiles)
    for op, (nx, ny) in choices:
        if 0 <= nx < size and 0 <= ny < size and tiles[ny][nx] != "LOCKED":
            return [op]
    return ["PASS"]


def _terminal_action(obs):
    """Observation-driven final-eight-turn harvest/drop/sell controller."""
    player = int(obs.get("player", 0) or 0)
    farm = (obs.get("farms") or [])[player]
    private = obs.get("private") or {}
    tiles = farm.get("tiles") or []
    size = len(tiles)
    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands") or [])]
    inventories = list(private.get("inventories") or [])
    inventories.extend({} for _ in range(len(positions) - len(inventories)))
    sheds = set(_shed_access(size))

    available = {
        (x, y)
        for y, row in enumerate(tiles)
        for x, tile in enumerate(row)
        if isinstance(tile, dict) and int(tile.get("yield_units", 0) or 0) > 0
    }
    actions = []
    pending = {}
    for pos_raw, inventory in zip(positions, inventories):
        pos = tuple(pos_raw)
        inventory = inventory or {}
        load = sum(max(0, int(v or 0)) for v in inventory.values())
        x, y = pos
        tile = tiles[y][x] if 0 <= y < size and 0 <= x < size else None
        if load > 0 and pos in sheds:
            action = ["DROP"]
            for item, count in inventory.items():
                if item in _SELLABLE:
                    pending[item] = pending.get(item, 0) + max(0, int(count or 0))
        elif isinstance(tile, dict) and int(tile.get("yield_units", 0) or 0) > 0:
            action = ["HARVEST"]
            available.discard(pos)
        elif load > 0:
            target = min(sheds, key=lambda q: abs(q[0] - x) + abs(q[1] - y))
            action = _move_toward(pos, target, tiles)
        elif available:
            target = min(available, key=lambda q: (abs(q[0] - x) + abs(q[1] - y), q[1], q[0]))
            available.discard(target)
            action = _move_toward(pos, target, tiles)
        elif isinstance(tile, dict) and tile.get("fertilizer_available", False):
            action = ["COLLECT_FERTILIZER"]
        else:
            action = ["PASS"]
        actions.append(action)

    shed = dict(private.get("shed") or {})
    for item, count in pending.items():
        shed[item] = int(shed.get(item, 0) or 0) + count
    prices = ((obs.get("market") or {}).get("prices") or {})
    sells = [
        (int(shed.get(item, 0) or 0) * int(prices.get(item, 1) or 1), item, int(shed.get(item, 0) or 0))
        for item in _SELLABLE
    ]
    sells = [row for row in sells if row[2] > 0]
    sells.sort(reverse=True)
    market = [["SELL", item, qty] for _, item, qty in sells[:10]]
    if int(obs.get("hour", 0) or 0) <= 1:
        already = int(farm.get("hires_today", 0) or 0)
        for _ in range(min(10 - len(market), max(0, 8 - already))):
            market.append(["HIRE"])
    return {"farmer": actions[0], "hands": actions[1:], "market": market[:10]}


def _base_agent(obs, config=None):
    global _LAST_STEP, _CLONE_CONFIDENCE
    step = min(int(obs.get("step", 0) or 0), len(_TRACE) - 1)
    if step == 0 or step <= _LAST_STEP:
        _CLONE_CONFIDENCE = 0
    _LAST_STEP = step
    _update_clone_profile(obs, step)
    if step >= 717:
        return _terminal_action(obs)
    action = copy.deepcopy(_TRACE[step])
    _front_run(action, obs, step)
    _terminal_liquidation(action, obs, step)
    return action


# ===========================================================================
# Market-controller overlay
# ===========================================================================
import math as _math

# Per-step remaining sell volume of this field plan, measured over c27 self-play.
_SUPPLY = json.loads(zlib.decompress(base64.b85decode(
    'c%1Fr%Wm5+5Cza*39{~j!?(Ii3pWj#)PQRsXp4SH(SNTlZOK$D%hrRG91k$}ECK|GWl5pP5&z!5eqB9m??2xC_S${8>%g|40o8~KRn)i|T_c-Ng)B~CGN496wl}hgs1QXm@KJ@zO8JSLEoMTcp!~L+F{jWC^e|LF)=(2sf$PIb3(SlNzsDBEF#JfoWe(t$Yj9w9c;Cbw<7UNFSXW_+8eK!jXnZ0v6}ZhU25LvUVmLTB{V)npQt&Tu2T?{8u6>1DeP;Bfh-txjrG(rgadmg#C&QQ5mb7*zObT%PjIEHq#)0xwmcrH0IS6;r%ds_7fjeO<R-XVDHtFe5b{U9c@TIh4Qa~f2^712`IfKEUA#@B*lD={N5Gf8RziqLrKOgSyKR;|X>+lpP>YsCQadB~Rad9Oo3_rH(mxt||haX&ATwGjSTv-akk00C3!|SKjX7dw65Q*tshG7_nVVGkyprl}RZvx~bgg>YpF-fdKOSG4qgU%8bqxwVs6t+gzh!`qtez1P$MN(W?6824OUyMG5Y$A?9(^>?+g>mRks6oAK>ZeGxbZYtsodn6F-$d?$<E};~EL)F^?O7_S=&9^w^}PO$2eRE-I>Ru`&4T`{s6B{cFwQ{YZl6U*zQ14uWyS3#%h2Z*@^*MPQP3v8n8;y4cWAPRbdmZHJgFv)oG)UwHJsJsBlnMRadB~RadBm-FjM*T{4I2j>|PvW80OtT4e<Ic^F9%mLxt<aObni{eUSnSOm>`25B5IDhw)1T#~HJ2gbkb)it^`?XCZfm;OhyiIuT((rx*gdOtM5Af}2MpCW=~4u!#b8dq^Fe(W!z<VQjEXR6G?ub;2p#H~XpMB5DU|K3=`9*UzC3<m5IO40GEoV6^e>(Kih?vsxDB>cI}F?O-s7>4zgO*m=mOMPEO7fFHFt)1`zxoKzFEYZV<Sf2W`*g3~vl6)Si2btbe1*(mA?61N3mCrB|}<jgtQPJ>6GFRRV=>G|o`Y7^F*FlVr6C;{`%5t~lbSY!)lcb=RE!hfF_mzI-r-D(o354i67ZQuEZwrOsCA(S1oU{8hVL>-fNRvtUO?m%zt9OxwICh{0%a-kZ?nHV;0J{oL}oHQfG!C2wLe($Yu`<RKME{uGWj?HT?+Td1C5YbH5F*r?^*4GKtKIO3v+vWF6XxHyrn;6*2-<p>3c(Rs!pD~m+;RUgj8S*-S*aeT2QB@B!|NaA0p<>w'
)).decode("utf-8"))

_I0 = 10000
_PRICE_FLOOR = 1
_MP = {
    "WHEAT": (25, 400, "sqrt", 0.80, "log", 0.20),
    "CARROT": (35, 450, "log", 0.20, "sqrt", 0.70),
    "TOMATO": (60, 200, "linear", 0.40, "sqrt", 0.60),
    "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON": (250, 300, "log", 0.20, "sq", 3.60),
    "EGG": (50, 332, "linear", 0.40, "log", 0.20),
    "MILK": (160, 122, "sqrt", 0.60, "linear", 1.60),
    "WOOL": (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}
_SHOP_DEMAND = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_CENTER_ITEMS = tuple(k for k in _MP if k != "FERTILIZER")

# Products the controller owns, mapped to a reservation price expressed as a
# fraction of base price. Everything else keeps the tape's schedule untouched.
_RESERVE = {}
# Sort SELL orders by gross value so the most valuable sale takes the earliest
# slot; market slots resolve index by index across both players.
_SORT_SELLS = True
# Ranking key for slot placement: "gross", "unit" or "impact".
_SORT_KEY = 'impact'
# True places promoted sells ahead of buys/hires; False keeps the tape's layout.
_SELLS_FIRST = True
# Only these products may be promoted into early slots. Empty means all.
_PROMOTE = ('MELON', 'STRAWBERRY', 'MILK', 'WOOL')
# Extra slot priority for a product whose remaining supply outruns the town's
# remaining appetite. Such a product is a race, not a hold: its price will only
# fall, so the units sold before the opponent's are the only ones worth much.
# Ranking purely by current price gets this backwards — a already-crashed product
# looks unimportant precisely when beating the opponent to the floor matters most.
_RACE_WEIGHT = 0.0
# Products that may be promoted only from this step onward. Selling wheat early
# lowers the price an opponent pays for feed, which can rescue a cash-starved
# rival; deferring wheat promotion keeps that pressure on during the early game
# when starvation actually bites.
_PROMOTE_AFTER = {}
# Products promoted only while the opponent's public money is at least this much.
# A rival near insolvency is the one most helped by our extra supply, so we hold
# that pressure on until they are clearly solvent.
_PROMOTE_IF_OPP_MONEY = {}
# Products whose SELL orders jump ahead of every other order in the turn, rather
# than merely being reordered among the slots the tape already used for sells.
# Slot 0 is priced against an inventory neither player has touched yet, so this
# is what beats an opponent that front-loads its own contested sells. Never list
# WHEAT or FERTILIZER here: those are the only products an opponent can
# BUY_PRODUCT, and their buys lift the price a later slot would sell into.
_LIFT = ()
# Step at which to pre-empt the base's own end-of-game liquidation. 0 disables.
_EARLY_TERMINAL = 0
# Force selling once the shed reaches this load, protecting end-of-day drops.
_SHED_PRESSURE = 80
# Reservation decays linearly to zero across this window, spreading liquidation.
_RAMP_START = 576
_RAMP_END = 716

_SUPPLY_DRIVER = {
    "MILK": ("animal", "COW"),
    "WOOL": ("animal", "SHEEP"),
    "EGG": ("animal", "GOOSE"),
    "FERTILIZER": ("animal", None),
    "STRAWBERRY": ("crop", "STRAWBERRY"),
    "MELON": ("crop", "MELON"),
    "WHEAT": ("crop", "WHEAT"),
    "CARROT": ("crop", "CARROT"),
    "TOMATO": ("crop", "TOMATO"),
}


def _mshape(func, x):
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return _math.sqrt(x)
    if func == "log10":
        return _math.log10(1.0 + x)
    return _math.log(1.0 + x)


def _mprice(item, inventory):
    """Exact port of the engine's market_price."""
    base, throughput, below_f, below_t, above_f, above_t = _MP[item]
    if inventory < _I0:
        amp = below_t * base / _mshape(below_f, throughput)
        value = base + amp * _mshape(below_f, _I0 - inventory)
    else:
        amp = above_t * base / _mshape(above_f, throughput)
        value = base - amp * _mshape(above_f, inventory - _I0)
    return max(_PRICE_FLOOR, int(round(value)))


def _remaining_drain(item, step, shops):
    """Units of `item` the town consumes between `step` and the season end.

    Shops fire on steps divisible by 4, the town center on steps divisible by 12
    with multipliers that step up on days 10 and 20. Still-locked shops are
    credited from the day they are expected to unlock (one new shop every three
    days), so late-game demand is not understated.
    """
    if item == "FERTILIZER":
        return 0.0  # neither the shops nor the town center consume fertilizer
    unlocked = set(shops or ())
    live = 0
    pending = []
    for name, products in _SHOP_DEMAND.items():
        if item not in products:
            continue
        weight = 2 if len(products) == 1 else 1
        if name in unlocked:
            live += weight
        else:
            pending.append(weight)
    n_locked = len(_SHOP_DEMAND) - len(unlocked)
    pending_total = sum(pending)
    is_center = item in _CENTER_ITEMS
    total = 0.0
    for s in range(step, 720):
        day = s // 24
        if s % 4 == 0:
            total += live
            if pending_total and n_locked > 0:
                expected = min(n_locked, max(0, day // 3 + 1 - len(unlocked)))
                total += pending_total * (expected / n_locked)
        if is_center and s % 12 == 0:
            total += 4 if day >= 20 else (2 if day >= 10 else 1)
    return total


def _count_driver(farm, kind, name):
    total = 0
    for row in farm.get("tiles") or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            if kind == "animal":
                animal = tile.get("animal")
                if animal and (name is None or animal == name):
                    total += 1
            elif tile.get("kind") == "PLANT" and tile.get("crop") == name:
                total += 1
    return total


def _opponent_scale(obs, item):
    """Opponent's expected remaining supply of `item`, relative to ours."""
    driver = _SUPPLY_DRIVER.get(item)
    if driver is None:
        return 1.0
    farms = obs.get("farms") or []
    if len(farms) < 2:
        return 1.0
    me = int(obs.get("player", 0) or 0)
    kind, name = driver
    mine = _count_driver(farms[me], kind, name)
    theirs = _count_driver(farms[1 - me], kind, name)
    if mine <= 0:
        return 1.0 if theirs > 0 else 0.0
    return max(0.0, min(2.0, theirs / float(mine)))


def _reserve_price(item, step, obs, shops):
    """Reservation price for one unit of `item`.

    A fixed fraction of base price, decayed linearly to zero over the
    liquidation ramp, and scaled down when the town's remaining appetite cannot
    absorb the supply still to come: a structurally oversupplied product is a
    race to sell, not something to hold.
    """
    base = _MP[item][0]
    frac = _RESERVE[item]
    if step >= _RAMP_START:
        span = float(max(1, _RAMP_END - _RAMP_START))
        frac *= max(0.0, (_RAMP_END - step) / span)
    drain = _remaining_drain(item, step, shops)
    supply = float(_SUPPLY.get(item, [0] * 721)[min(step, 720)])
    ahead = supply * (1.0 + _opponent_scale(obs, item))
    if ahead > 0.0:
        frac *= min(1.0, drain / ahead)
    return base * frac


def _plan_sells(obs, step, slots, short_of_cash):
    """Choose SELL orders for the controlled products."""
    if slots <= 0:
        return []
    shed = (obs.get("private") or {}).get("shed") or {}
    inventory = ((obs.get("market") or {}).get("inventory") or {})
    shops = (obs.get("town") or {}).get("unlocked_shops") or []
    load = sum(max(0, int(v or 0)) for v in shed.values())
    forced = load >= _SHED_PRESSURE or short_of_cash > 0

    candidates = []
    for item in _RESERVE:
        held = int(shed.get(item, 0) or 0)
        if held <= 0:
            continue
        inv = int(inventory.get(item, _I0) or _I0)
        if forced:
            units = held
        else:
            reserve = _reserve_price(item, step, obs, shops)
            units = 0
            while units < held and _mprice(item, inv + units) >= reserve:
                units += 1
        if units > 0:
            candidates.append((_mprice(item, inv) * units, item, units))
    candidates.sort(reverse=True)
    return [["SELL", item, units] for _, item, units in candidates[:slots]]


def _cash_needed(orders, obs):
    """Coins this turn's buy orders require."""
    seeds = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
    animals = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
    prices = ((obs.get("market") or {}).get("prices") or {})
    total = 0
    for order in orders:
        if not isinstance(order, list) or not order:
            continue
        op = order[0]
        if op == "BUY_SEED" and len(order) >= 3:
            total += seeds.get(order[1], 0) * int(order[2] or 0)
        elif op == "BUY_ANIMAL" and len(order) >= 3:
            total += animals.get(order[1], 0) * int(order[2] or 0)
        elif op == "BUY_PRODUCT" and len(order) >= 3:
            total += int(prices.get(order[1], 50) or 50) * int(order[2] or 0)
        elif op == "BUY_LAND":
            total += 4000
    return total


def _race_factor(item, step, obs):
    """1.0 when the town can absorb everything still coming, higher when not."""
    if _RACE_WEIGHT <= 0.0:
        return 1.0
    shops = (obs.get("town") or {}).get("unlocked_shops") or []
    drain = _remaining_drain(item, step, shops)
    supply = float(_SUPPLY.get(item, [0] * 721)[min(step, 720)])
    ahead = supply * (1.0 + _opponent_scale(obs, item))
    if ahead <= 0.0:
        return 1.0
    glut = max(0.0, 1.0 - drain / ahead)
    return 1.0 + _RACE_WEIGHT * glut


def _sell_priority(order, obs, step=0):
    """Rank a SELL order for slot placement; higher goes into an earlier slot.

    Market slots resolve index by index across both players, so an order in an
    earlier slot is priced before the opponent's matching order in a later slot.
    ``gross`` ranks by revenue at stake. ``impact`` ranks by how much revenue is
    actually lost by going second, which is the quantity times this order's own
    price impact — that promotes steep premium curves (wool, melon, milk) over
    large but nearly flat staple sales (wheat, egg).
    """
    if not (isinstance(order, list) and len(order) >= 3 and order[0] == "SELL"):
        return -1.0
    item = order[1]
    try:
        qty = int(order[2] or 0)
    except (TypeError, ValueError):
        return -1.0
    if qty <= 0 or item not in _MP:
        return -1.0
    inventory = ((obs.get("market") or {}).get("inventory") or {})
    inv = int(inventory.get(item, _I0) or _I0)
    unit = _mprice(item, inv)
    held = int(((obs.get("private") or {}).get("shed") or {}).get(item, 0) or 0)
    qty = min(qty, held) if held > 0 else qty
    race = _race_factor(item, step, obs)
    if _SORT_KEY == "unit":
        return float(unit) * race
    if _SORT_KEY == "impact":
        return float(qty) * float(unit - _mprice(item, inv + qty)) * race
    return float(unit) * float(qty) * race


def _bank_inner_agent(obs, config=None):
    """c27 with its SELL layer partially replaced by the market controller."""
    action = _base_agent(obs, config)
    try:
        step = int(obs.get("step", 0) or 0)
        # Liquidate one step before the base's own terminal dump. Both dumps hit
        # a market that only falls, so whoever sells first takes the un-crashed
        # price; an opponent sharing this route dumps at its tape's step and gets
        # what is left. Nothing downstream needs the goods or the shed space.
        if _EARLY_TERMINAL and step == _EARLY_TERMINAL:
            shed = (obs.get("private") or {}).get("shed") or {}
            rows = []
            for item in _MP:
                held = int(shed.get(item, 0) or 0)
                if held > 0:
                    rows.append((_sell_priority(["SELL", item, held], obs, step), item, held))
            if rows:
                rows.sort(reverse=True)
                action["market"] = [["SELL", i, q] for _p, i, q in rows[:10]]
                return action
        if step >= 717:
            return action  # proven terminal controller; leave untouched
        orders = list(action.get("market") or [])
        keep = [
            order for order in orders
            if not (
                isinstance(order, list) and len(order) >= 2
                and order[0] == "SELL" and order[1] in _RESERVE
            )
        ]
        player = int(obs.get("player", 0) or 0)
        money = float(((obs.get("farms") or [{}])[player]).get("money", 0) or 0)
        short = max(0.0, _cash_needed(keep, obs) - money)
        sells = _plan_sells(obs, step, 10 - len(keep), short)
        if not _SORT_SELLS:
            action["market"] = (sells + keep)[:10]
            return action

        def is_sell(o):
            return isinstance(o, list) and o and o[0] == "SELL"

        opp_money = None
        if _PROMOTE_IF_OPP_MONEY:
            farms = obs.get("farms") or []
            if len(farms) > 1:
                opp_money = float(farms[1 - player].get("money", 0) or 0)

        def promotable(o):
            if not is_sell(o):
                return False
            item = o[1]
            if item in _PROMOTE_IF_OPP_MONEY:
                if opp_money is None:
                    return False
                return opp_money >= _PROMOTE_IF_OPP_MONEY[item]
            if item in _PROMOTE_AFTER:
                return step >= _PROMOTE_AFTER[item]
            return not _PROMOTE or item in _PROMOTE

        # Only promotable sells compete for the earliest slots. WHEAT and
        # FERTILIZER are the only products an opponent can BUY_PRODUCT, so
        # promoting those ahead of their buys would lower the price they pay for
        # feed; those sells are deliberately left in their tape position, where
        # the opponent's buys have already drained inventory and lifted the price.
        # A lifted sell jumps ahead of *every* other order, so it is priced
        # before the opponent's matching sell in any later slot. Only worth it
        # for products the opponent dumps: for WHEAT and FERTILIZER — the only
        # two an opponent can BUY_PRODUCT — a later slot is strictly better,
        # because their buys drain inventory and lift the price we sell into.
        if _LIFT:
            lifted = [o for o in keep if is_sell(o) and o[1] in _LIFT]
            if lifted:
                lifted.sort(key=lambda o: -_sell_priority(o, obs, step))
                held = [o for o in keep if not (is_sell(o) and o[1] in _LIFT)]
                keep = lifted + held

        merged = [o for o in sells if promotable(o)] + [o for o in keep if promotable(o)]
        merged.sort(key=lambda o: -_sell_priority(o, obs, step))
        rest = [o for o in sells if not promotable(o)] + [o for o in keep if not promotable(o)]
        if _SELLS_FIRST:
            action["market"] = (merged + rest)[:10]
        else:
            # Keep the tape's slot layout: sorted sells refill the slots that
            # already held promotable sells; every other order stays put.
            out = []
            queue = list(merged)
            for order in keep:
                out.append(queue.pop(0) if (promotable(order) and queue) else order)
            out.extend(queue)
            action["market"] = out[:10]
        return action
    except Exception:
        return action


# Intraday banking experiment. Productive operations and resource pickups are
# hard constraints: only PASS or movement may be replaced by a short shed trip.
_BANK_VALUE = 1500.0
_BANK_MAX_DISTANCE = 1
_BANK_MIN_PRICE_RATIO = 0.25
_BANK_START = 120
_BANK_STOP = 680
_BANK_ITEMS = ("MELON", "STRAWBERRY", "MILK", "WOOL")
_BANK_BASE = {"MELON": 250, "STRAWBERRY": 120, "MILK": 160, "WOOL": 200}
_BANK_SAFE = {"PASS", "NORTH", "SOUTH", "EAST", "WEST"}


def _bank_access(size):
    half = size // 2
    return {(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)}


def _bank_move(position, target, tiles):
    x, y = position
    tx, ty = target
    choices = []
    if tx < x:
        choices.append(("WEST", (x - 1, y)))
    if tx > x:
        choices.append(("EAST", (x + 1, y)))
    if ty < y:
        choices.append(("NORTH", (x, y - 1)))
    if ty > y:
        choices.append(("SOUTH", (x, y + 1)))
    size = len(tiles)
    for op, (nx, ny) in choices:
        if 0 <= nx < size and 0 <= ny < size and tiles[ny][nx] != "LOCKED":
            return [op]
    return ["PASS"]


def _bank_value(inventory, prices):
    return sum(
        max(0, int(inventory.get(item, 0) or 0)) * float(prices.get(item, _BANK_BASE[item]) or 0)
        for item in _BANK_ITEMS
    )


def _bank_add_sales(action, pending, obs, step):
    if not pending:
        return action
    market = [list(order) for order in (action.get("market") or [])]
    prices = ((obs.get("market") or {}).get("prices") or {})
    locations = {}
    for index, order in enumerate(market):
        if len(order) >= 3 and order[0] == "SELL":
            locations[order[1]] = index
    for item in _BANK_ITEMS:
        quantity = max(0, int(pending.get(item, 0) or 0))
        ratio = float(prices.get(item, 0) or 0) / _BANK_BASE[item]
        if quantity <= 0 or ratio < _BANK_MIN_PRICE_RATIO:
            continue
        if item in locations:
            market[locations[item]][2] = max(0, int(market[locations[item]][2] or 0)) + quantity
        elif len(market) < 10:
            locations[item] = len(market)
            market.append(["SELL", item, quantity])

    def promoted(order):
        return len(order) >= 3 and order[0] == "SELL" and order[1] in _BANK_ITEMS

    premium = [order for order in market if promoted(order)]
    premium.sort(key=lambda order: -_sell_priority(order, obs, step))
    rest = [order for order in market if not promoted(order)]
    action["market"] = (premium + rest)[:10]
    return action


def agent(obs, config=None):
    action = _bank_inner_agent(obs, config)
    try:
        step = int(obs.get("step", 0) or 0)
        if not (_BANK_START <= step < _BANK_STOP):
            return action
        player = int(obs.get("player", 0) or 0)
        farm = (obs.get("farms") or [])[player]
        tiles = farm.get("tiles") or []
        positions = [farm.get("farmer", [0, 0]), *(farm.get("hands") or [])]
        inventories = list((obs.get("private") or {}).get("inventories") or [])
        inventories.extend({} for _ in range(len(positions) - len(inventories)))
        unit_actions = [list(action.get("farmer") or ["PASS"])]
        unit_actions.extend(list(order or ["PASS"]) for order in (action.get("hands") or []))
        unit_actions.extend(["PASS"] for _ in range(len(positions) - len(unit_actions)))
        access = _bank_access(len(tiles))
        prices = ((obs.get("market") or {}).get("prices") or {})
        pending = {}

        for index, (raw_position, inventory) in enumerate(zip(positions, inventories)):
            position = tuple(raw_position)
            inventory = inventory or {}
            op = unit_actions[index][0] if unit_actions[index] else "PASS"
            value = _bank_value(inventory, prices)
            # Credit ordinary tape DROP operations too: selling the newly
            # deposited premium batch immediately is part of the experiment.
            if op == "DROP" and position in access:
                for item in _BANK_ITEMS:
                    pending[item] = pending.get(item, 0) + max(0, int(inventory.get(item, 0) or 0))
                continue
            if value < _BANK_VALUE or op not in _BANK_SAFE:
                continue
            distance, target = min(
                ((abs(position[0] - q[0]) + abs(position[1] - q[1]), q) for q in access),
                key=lambda row: (row[0], row[1][1], row[1][0]),
            )
            if distance == 0:
                unit_actions[index] = ["DROP"]
                for item in _BANK_ITEMS:
                    pending[item] = pending.get(item, 0) + max(0, int(inventory.get(item, 0) or 0))
            elif distance <= _BANK_MAX_DISTANCE:
                unit_actions[index] = _bank_move(position, target, tiles)

        action["farmer"] = unit_actions[0]
        action["hands"] = unit_actions[1:len(positions)]
        return _bank_add_sales(action, pending, obs, step)
    except Exception:
        return action
