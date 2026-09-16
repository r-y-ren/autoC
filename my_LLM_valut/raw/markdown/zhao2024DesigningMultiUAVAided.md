# On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcement Learning

Ze Yu Zhao , Yue Ling Che , Member, IEEE, Sheng Luo , Member, IEEE, Gege Luo, Kaishun Wu , Fellow, IEEE, and Victor C. M. Leung , Life Fellow, IEEE

AbstractâThis paper proposes a novel design on the wireless powered communication network (WPCN) in dynamic environments under the assistance of multiple unmanned aerial vehicles (UAVs). Unlike the existing studies, where the low-power wireless nodes (WNs) often conform to the coherent harvest-then-transmit protocol, under our newly proposed double-threshold based WN type updating rule, each WN can dynamically and repeatedly update its WN type as an E-node for non-linear energy harvesting over time slots or an I-node for transmitting data over sub-slots. To maximize the total transmission data size of all the WNs over T slots, each of the UAVs individually determines its trajectory and binary wireless energy transmission (WET) decisions over times slots and its binary wireless data collection (WDC) decisions over sub-slots, under the constraints of each UAVâs limited on-board energy and each WNâs node type updating rule. However, due to the UAVsâ tightly-coupled trajectories with their WET and WDC decisions, as well as each WNâs time-varying battery energy, this problem is difficult to solve optimally. We then propose a new multiagent based hierarchical deep reinforcement learning (MAHDRL) framework with two tiers to solve the problem efficiently, where the soft actor critic (SAC) policy is designed in tier-1 to determine each UAVâs continuous trajectory and binary WET decision over time slots, and the deep-Q learning (DQN) policy is designed in tier-2 to determine each UAVâs binary WDC decisions over sub-slots under the given UAV trajectory from tier-1. Both of the SAC policy and the DQN policy are executed distributively at each UAV. Finally, extensive simulation results are provided to validate the outweighed

Manuscript received 1 December 2023; revised 6 June 2024; accepted 30 July 2024. Date of publication 6 August 2024; date of current version 5 November 2024. This work was supported in part by the National Natural Science Foundation of China under Grant 62072314 and Grant U2001207, in part by the Guangdong Natural Science Foundation under Grant 2023A1515011327, in part by the Guangdong Provincial Key Lab of Integrated Communication, Sensing and Computation for Ubiquitous Internet of Things under Grant 2023B1212010007, in part by the Project of DEGP under Grant 2023KCXTD042 and Grant 2021ZDZX1068, in part by the Guangdong âPearl River Talent Recruitment Programâ under Grant 2019ZT08X603, and in part by the Guangdong âPearl River Talent Planâ under Grant 2019JC01X235. Recommended for acceptance by Y. Zhu. (Corresponding author: Yue Ling Che.)

performance of the proposed MAHDRL approach over various state-of-the-art benchmarks.

Index TermsâMulti-agent hierarchical deep reinforcement learning (MAHDRL), multiple unmanned aerial vehicles (UAVs) aided network, trajectory and scheduling optimization, wireless powered communication network (WPCN).

## I. INTRODUCTION

T HE unmanned aerial vehicle (UAV) aided wireless pow-ered communication network (WPCN) has emerged as one ered communication network (WPCN) has emerged as one promising technology to realize the energy-sustainable wireless communications. As compared to the traditional WPCNs with fixed deployment on ground [1] and [2], the UAVs with high mobility are able to provide more efficient radio frequency (RF) wireless energy transmissions (WET) to the low-power wireless nodes (WNs) over the largely shortened energy transmission distances [3]. This not only evokes an increased number of sufficiently-charged WNs and thus higher communication throughput in UAV-aided WPCNs in general [4], but also enables adaptive and on-demand wireless services in different network scenarios [5]. Due to the WNsâ dynamically changing demands for energy harvesting and/or information transmissions over time, the design of the UAV-aided WPCN is generally challenging. In the literature, for the ease of the WPCN design, either the WNs conform to the coherent harvest-then-transmit protocol [6], or the UAVs are pre-assigned to transmit energy or collect wireless data as separate groups [7]. The dynamics of the UAV-aided WPCN have not been fully explored yet. This motivates us to investigate both of the WNsâ time-varying service demands and the UAVsâ individually-adaptive trajectory and transmission designs, for enabling the UAV-aided WPCN in dynamic environments.

## A. Related Work

UAV-aided wireless communications: Benefiting from the air-to-ground (A2G) wireless channels with high quality, the UAVs have been utilized as the aerial base stations (ABS) to provide ubiquitous wireless connections [8]. The line-of-sight (LoS) probability based A2G channel model has been investigated in [9], which shows that the LoS probability between the UAV and the WN on ground generally increases with their in-between elevation angle. The joint design of the UAVsâ trajectories and communication resource allocations is essential for the UAV-aided wireless communications. For the single-UAV scenario, the UAVâs trajectory and time resource allocation are usually alternatively optimized via the successive convex approximation (SCA) technique to, e.g., maximize the WNsâ minimum achievable data transmission rate [10] or minimize the age of information (AoI) of the WNsâ transmission data [11] and [12]. The SCA technique has also been employed in the multi-UAV communication scenario [13], but the resultant system performance may be comprised for the high complexity caused by the coupling between the multiple UAVsâ trajectories and transmissions [14]. To achieve higher downlink capacity, the deep reinforcement learning (DRL) is leveraged in [15] and [16] to determine the wireless data collection (WDC) schemes and the movements of multiple UAVs.

UAV-aided WET: The feasibility of the UAV-aided WET has been validated by the field tests in [17]. The joint design of the UAV trajectory and WET has been widely studied in [18], [19], [20] for the single-UAV scenario or in [21] and [22] for the multi-UAV scenario, respectively, to maximize the total harvested energy at the WNs. However, all the above studies ideally assumed that all the WNs not only have the same energy demands, but also utilize linear energy harvesters, where each WN harvests non-zero direct current (DC) energy regardless of the UAVsâ transmission distances. It is noted that for multi-UAV aided WET, [23] proposed a new metric called the hungry-level of energy (HoE) to measure the WNsâ different and time-varying energy demands, and exploited the DRL algorithm to design on-demand WET based on non-linear energy harvesting at the WNs.

UAV-aided WPCN: Despite of the extensive studies on the UAV-aided communications and the UAV-aided WET, the design of the UAV-aided WPCN is not a simple combination of them. Since the WNs use their harvested energy from the UAVsâ WET in the downlink to support their data transmissions in the uplink to the UAVs, the UAVsâ WET performance may bottleneck the WNsâ data transmissions in the UAV-aided WPCN. In the literature, the UAVsâ task period is usually divided into a WET phase and a follow-up WDC phase [24], [25], [26], where each phase has the same time length for all the UAVs. While such a two-phase protocol simplifies the UAV-aided WPCN design, due to the WNsâ generally different energy demands, not all the WNs can harvest sufficient energy in the UAVsâ WET phase, and thus not all the WNsâ data transmission requirements can be satisfied in the UAVsâ WDC phase. Moreover, in [7], instead of evoking adaptive WET and WDC at each of the UAVs, multiple UAVs were divided into two groups to separately transmit energy to or collect data from the WNs, where the deep deterministic policy gradient (DDPG) algorithm is applied to jointly design the multi-UAVâs trajectory and resource allocations.

## B. Our Contributions

In this paper, we propose a novel design of the wireless powered dynamic communication network under the assistance of multiple UAVs, where each of the WNs with different energy demands can dynamically harvest energy whenever in short energy supply and transmit data whenever sufficiently charged. To adapt to the WNsâ different service demands, each of the UAVs individually determines its trajectory and binary WET decisions over time slots and its binary WDC decisions over sub-slots. However, due to the UAVsâ tightly-coupled trajectories with their WET and WDC decisions, as well as each WNâs time-varying battery energy, the optimal network design is very challenging to realize using the traditional optimization techniques. By taking each UAV as an individual agent, we then propose a novel multi-agent based hierarchical DRL (MAH-DRL) framework with two tiers, to address the UAVsâ action decisions distributively over the two different time scales of time slots and sub-slots.

Our main contributions are summarized as follows:

1) Practical System Model with Repeatedly Updating WN Types: Section II models the multi-UAV aided WPCN by exploiting the LoS-probability based A2G channel model. Under the newly proposed double-threshold based WN type updating rule, each WN repeatedly updates its node type as an E-node for harvesting energy or an I-node for transmitting data over time slots. In each time slot, if a WN is an E-node, a practical non-linear energy harvesting model is applied for its energy harvesting; and if a WN is an I-node, the sub-slot based data transmission scheduling is used to alleviate the UAVsâ received co-channel interference. The battery energy management at each WN and each UAV are all addressed.

2) Novel Problem Formulaion Solved by MAHDRL Framwork: Section III formulates the problem to maximize the total transmission data size of all the WNs over T slots, by jointly optimizing the trajectory, the WET decisions, and the WDC decisions of each UAV, under the constraints of each UAVâs limited on-board energy and each WNâs node type updating rule. Due to the high complexity to solve this problem optimally, we propose the novel MAHDRL framework with two tiers to solve the problem efficiently, where the soft actor critic (SAC) policy is executed in tier-1 to determine each UAVâs continuous trajectory and binary WET decision over time slots, and the deep-Q learning (DQN) policy is executed in tier-2 to determine each UAVâs binary WDC decisions over sub-slots under the given UAV trajectory from tier-1.

3) Hierarchical Training of the Central SAC and the Local DQN: Sections IV designs the central training of the SAC policy for tier-1, due to its relatively higher complexity caused by the entropy-based action space exploration, and Section V designs the local training of the DQN policy with lower complexity in tier-2, respectively. For both policies, due to each E-nodeâs low battery energy and thus weak transmit power to report its status, only UAVs nearby (if any) can observe with its actual status, which generally leads to the partially observable Markov decision process (POMDP) based modeling at both the central trainer and the individual UAV. Due to the mutually affected policy decisions among the two tiers, the reward functions for both the SAC and the DQN are designed to achieve the proper trade-off between satisfying the E-nodesâ and the

<!-- image-->  
Fig. 1. Multi-UAV aided WPCN with repeatedly changing WN types.

I-nodesâ different service demands under the WN type updating rule. Once well trained, both of the SAC policy and the DQN policy are executed distributively at each UAV.

4) Extensive simulation results for Performance Evaluation: Section VI validates the outweighed performance of the proposed MAHDRL approach over various state-of-theart benchmarks in both of the training stage and the test stage. A network example is also illustrated to elaborate the dynamics of the WNsâ node type variations and the UAVsâ adaptive trajectories. Moreover, the scalability of the proposed MAHDRL approach in different network scales is also validated.

## II. SYSTEM MODEL

As shown in Fig. 1, we consider a multi-UAV aided WPCN, where each of the $U \geq 2 \ \mathrm { U A V s }$ transmits wireless energy to and/or collects wireless data from in total of W WNs for a task period of T slots with $\mathcal { T } = \{ 1 , . . . , T \} , \mathcal { U } = \{ 1 , . . . , U \}$ and $\mathcal { W } = \{ 1 , . . . , W \}$ . Each UAV flies at a fixed altitude of h meters (m). To prevent the UAVsâ WET in the downlinks from causing co-channel interference to their WDC in the uplinks, each UAV is equipped with two antennas to enable separate WET and WDC over different and non-overlapped frequency bands at the same time.

Each WN is installed with a single antenna and a rechargeable battery, and either harvests energy from or transmits data to the UAVs in each slot. The WNs that harvest energy in slot t are referred to as the E-nodes. Each of the E-nodes stores the harvested energy in its rechargeable battery. The WNs that transmit data in slot t are referred to as the I-nodes. All the I-nodes in slot t have sufficient battery energy to support their data transmissions. We use $F _ { w } [ t ] = \{ 0 , 1 \}$ to label the type of WN-w in slot $t \in \tau$ , where WN-w is an I-node if $F _ { w } [ t ] = 1$ , or an E-node, otherwise. Correspondingly, the WN set W is divided into the I-node subset $\mathcal { T } [ t ] \triangleq \{ w | F _ { w } [ t ] = 1 , w \in \mathcal { W } \}$ and the Enode subset $\mathcal { E } [ t ] \triangleq \{ w | \bar { F } _ { w } [ t ] = 0 , w \in \mathcal { W } \}$ in slot t with $\mathcal { W } =$ $\mathcal { E } [ t ] + \mathcal { T } [ t ]$ ]. Due to the time-varying WN battery energy, each WNâs type and thus the elements in $\mathcal { E } [ t ]$ and $\mathcal { T } [ t ]$ may all change over different time slots. Table I gives the notations of the key parameters in this paper.

TABLE I  
NOTATIONS OF KEY PARAMETERS
<table><tr><td>Notations</td><td>Description</td></tr><tr><td> $F _ { w } [ t ]$ </td><td>The type of WN-w in slot t</td></tr><tr><td> $q _ { u } [ t ] , q _ { w }$ </td><td>Location ofUAV-u or WN-w in slot t</td></tr><tr><td> $d _ { w } ^ { u } [ t ]$ </td><td>Distance between UAV-u and WN-w in slot t</td></tr><tr><td> $\vartheta , \varrho$ </td><td>Time length of a slot or a sub-slot</td></tr><tr><td> $P _ { W } , P _ { U }$ </td><td>Each WN&#x27;s or UAV&#x27;s transmit power</td></tr><tr><td> $G _ { w } ^ { u } [ t ]$ </td><td>Channel gain between WN-w and UAV-u in slot t</td></tr><tr><td> $Z _ { u } [ t ]$ </td><td>UAV-u&#x27;sWET decision in slot t</td></tr><tr><td> $E _ { w } ^ { h a r } [ t ]$ </td><td>Harvested energy at WN-w in slot t</td></tr><tr><td> $D _ { u , w } ^ { t } [ k ]$ </td><td>UAV-u&#x27;sWDCdecison forWN-w at sub-slot k in slot t</td></tr><tr><td> $M _ { u , w } ^ { t } [ k ]$ </td><td>WN-w&#x27;s transmission data size to UAV-u at sub-slot k in slot t</td></tr><tr><td> $C _ { w } \left[ t \right]$ </td><td>Aggregated transmission data size of WN-w in slot t</td></tr><tr><td> $B _ { w } [ t ] , B _ { u } [ t ]$ </td><td>Battery level of WN-w or UAV-u in slot t</td></tr></table>

## A. LoS-Probability Based Channel Model

Denote the coordinate of WN-w as $q _ { w } = ( x _ { w } , y _ { w } , 0 )$ and that of UAV-u in slot t as $q _ { u } [ t ] = ( x _ { u } [ t ] , y _ { u } [ t ] , h )$ , respectively, âw â W and $\forall u \in \mathcal { U } .$ . Since the time length Ï of each slot is generally very short, each $\mathrm { U A V } _ { \mathrm { \Delta } }$ location is assumed to be unchanged within each slot. The distance between $\mathrm { U A V } â u$ and WN-w in slot t is obtained as $d _ { w } ^ { u } [ t ] = \lVert q _ { w } - q _ { u } [ t ] \rVert$ , where $\| \cdot \|$ is the euclidean norm.

Let $P _ { L o S , w } ^ { u } [ t ] = ( 1 + a \exp ( - b ( \beta _ { w } ^ { u } [ t ] - a ) ) ) ^ { - 1 }$ denote the LoS probability between UAV-u and WN-w in slot $t \left[ 9 \right]$ , where $\beta _ { w } ^ { u } [ t ] = \sin ^ { - 1 } ( h / d _ { w } ^ { u } [ t ] )$ is their in-between elevation angle in slot t, and a and b are two constant parameters measured from the environment. The non-line-of-sight (NLoS) probability is thus $P _ { N L o S , w } ^ { u } [ t ] = 1 - P _ { L o S , w } ^ { u } [ t ]$ . The average channel gain between UAV-u and WN-w in slot t is obtained as

$$
G _ { w } ^ { u } [ t ] = P _ { L o S , w } ^ { u } [ t ] G _ { 0 } d _ { w } ^ { u } [ t ] ^ { - \alpha _ { L } } + P _ { N L o S , w } ^ { u } [ t ] G _ { 0 } d _ { w } ^ { u } [ t ] ^ { - \alpha _ { N } } ,\tag{1}
$$

where $G _ { 0 }$ is the average channel gain at a reference distance of 1 m, and $\alpha _ { L }$ and $\alpha _ { N }$ with $0 < \alpha _ { L } < \alpha _ { N }$ are the LoS link and NLoS linksâ path-loss exponents, respectively.

## B. UAVsâ Energy Transmissions to E-Nodes

Denote $Z _ { u } [ t ] \in \{ 0 , 1 \}$ as UAV-uâs WET decision in slot t, where UAV-u transmits energy with a fixed transmit power $P _ { U } >$ 0 in slot t if $Z _ { u } [ t ] = 1$ , or keeps silent on the frequency band for WET, otherwise, to save its limited on-board energy. We consider a non-linear energy harvester at each E-node, which transforms its received RF power p at the antenna into the DC power $\bar { P } ( p )$ stored in the battery nonlinearly as follows [27]:

$$
\begin{array} { r } { \bar { P } ( p ) = \left\{ \begin{array} { l l } { 0 , } & { p \in [ 0 , P _ { s e n } ) , } \\ { f ( p ) , } & { p \in [ P _ { s e n } , P _ { s a t } ) , } \\ { f ( P _ { s a t } ) , } & { p \in [ P _ { s a t } , + \infty ] , } \end{array} \right. } \end{array}\tag{2}
$$

where $P _ { s e n }$ and $P _ { s a t }$ with $0 < P _ { s e n } < P _ { s a t }$ are the sensitivity power and the saturation power of the energy harvester, respectively, and $f ( \cdot )$ is a non-linear power transform function that can be obtained through the curve fitting technique [27]. From (2), no DC power is harvested if $p < P _ { s e n }$ and the harvested DC power keeps unchanged if $p \geq P _ { s a t }$ . Since the received RF power at E-node-w from all the UAVs is $\begin{array} { r } { \sum _ { u = 1 } ^ { U } P _ { U } Z _ { u } [ t ] G _ { w } ^ { u } [ t ] } \end{array}$ its harvested energy in slot t is

$$
E _ { w } ^ { h a r } [ t ] = \bar { P } \left( \sum _ { u = 1 } ^ { U } P _ { U } Z _ { u } [ t ] G _ { w } ^ { u } [ t ] \right) \vartheta , \forall w \in \mathscr { W } .\tag{3}
$$

Due to the practically high value of $P _ { s e n }$ (with, e.g., -10 dBm [28]), the UAVs with $Z _ { u } [ t ] = 1$ need to locate close to E-node-w to assure its non-zero energy harvesting.

Denote $B _ { w } [ t ]$ as the battery energy level of ${ \mathbf { W } } { \mathbf { N } } { \mathbf { - } } w \in \mathcal { W }$ at the begining of slot $t \in \mathcal T$ and $B _ { W } ^ { \mathrm { m a x } }$ as the WN battery capacity, respectively. If WN-w is an E-node in slot t, i.e., $F _ { w } [ t ] = 0$ based on $( 3 ) , B _ { w } [ t + 1 ]$ is updated as

$$
B _ { w } [ t + 1 ] = \operatorname* { m i n } \left( B _ { W } ^ { \operatorname* { m a x } } , B _ { w } [ t ] + E _ { w } ^ { h a r } [ t ] \right) , \forall w \in \mathcal { E } [ t ] .\tag{4}
$$

## C. UAVsâ Data Collections From I-Nodes

For the I-nodes, to alleviate the UAVsâ received co-channel interference in each time slot, we increase the selections of time resources by dividing each time slot into $K \geq 2$ sub-slots, as shown in Fig. 1. Each sub-slot is of time length  with $\vartheta = K \varrho .$ Denote $D _ { u , w } ^ { t } [ k ] \in \{ 0 , 1 \}$ as UAV-uâs sub-slot based WDC decision, where $D _ { u , w } ^ { t } [ k ] = 1$ represents that UAV-u collects data from I-node-w at the k-th sub-slot in slot t, or $D _ { u , w } ^ { t } [ k ] = 0$ ï¼ otherwise. It is considered at any sub-slot k, each UAV collects data from at most one I-node, and each I-node transmits data to at most one UAV, which is expressed as

$$
\sum _ { w = 1 } ^ { W } D _ { u , w } ^ { t } [ k ] \leq 1 \mathrm { a n d } \sum _ { u = 1 } ^ { U } D _ { u , w } ^ { t } [ k ] \leq 1 , \forall u \in \mathcal { U } , \forall w \in \mathbb { Z } [ t ] .\tag{5}
$$

Denote $\Gamma _ { u , w } ^ { t } [ k ]$ as the signal-to-interference-plus-noise-ratio (SINR) received at $\mathrm { U A V } â u$ from I-node-w at the k-th sub-slot in slot t. Denote $P _ { W } > 0$ as each I-nodeâs fixed transmit power. Due to the sufficiently-short time slot length, $G _ { w } ^ { u } [ t ]$ in (1) is assumed to remain unchanged over all sub-slots in slot t. As a result, $\Gamma _ { u , w } ^ { t } [ k ]$ is obtained as

$$
\Gamma _ { u , w } ^ { t } [ k ] = \frac { D _ { u , w } ^ { t } [ k ] P _ { W } G _ { w } ^ { u } [ t ] } { \sum _ { i \in \mathcal { U } } \sum _ { j \in \mathcal { I } [ t ] , j \neq w } D _ { i , j } ^ { t } [ k ] P _ { W } G _ { j } ^ { u } [ t ] + \sigma ^ { 2 } } ,\tag{6}
$$

where $\sigma ^ { 2 }$ is the received noise power at each UAV. Denote $M _ { u . w } ^ { t } [ k ]$ as I-node-wâs transmission data size (bits/Hz) to UAV-u at the k-th sub-slot in slot $t \in \mathcal T$ . We have $M _ { u , w } ^ { t } [ k ] = \log _ { 2 } ( 1 +$ $\Gamma _ { u , w } ^ { t } [ k ] ) \varrho$ . Hence, the aggregated transmission data size of I-node-w over all the K sub-slots in slot t, denoted by $C _ { w } [ t ]$ , is obtained as

$$
C _ { w } [ t ] = \sum _ { u = 1 } ^ { U } \sum _ { k = 1 } ^ { K } M _ { u , w } ^ { t } [ k ] .\tag{7}
$$

Denote $C _ { t o t a l }$ as the total transmission data size of all the I-nodes over all the T slots with $\begin{array} { r } { C _ { t o t a l } = \sum _ { t = 1 } ^ { T } \sum _ { w = 1 } ^ { W } C _ { w } [ t ] } \end{array}$

To support the data transmissions, each I-node-w consumes an energy amount of $\begin{array} { r } { \sum _ { u = 1 } ^ { U } \sum _ { k = 1 } ^ { K } D _ { u , w } ^ { t } [ k ] P _ { W } \vartheta } \end{array}$ in slot t from its battery. Thus, if WN-w is an I-node with $F _ { w } [ t ] = 1$ , for a

given $B _ { w } [ t ] , B _ { w } [ t + 1 ]$ is updated as

$$
B _ { w } [ t + 1 ] = \operatorname* { m a x } \left( B _ { w } [ t ] - \sum _ { u = 1 } ^ { U } \sum _ { k = 1 } ^ { K } D _ { u , w } ^ { t } [ k ] P _ { W } \vartheta , 0 \right) , \forall w \in \mathbb { Z } [ t ] .\tag{8}
$$

## D. Double-Threshold Based WN Type Updating

At the beginning of each slot, based on each WN is an E-node or I-node in the previous slot, each WN updates its battery energy level according to (4) or (8), respectively. Based on the $B _ { w } [ t ]$ WN-w updates its WN type at the beginning of slot t according to a double-threshold based WN type updating rule given as follows:

$$
F _ { w } [ t ] = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f } \ B _ { w } [ t ] \geq B _ { I } o r \ B _ { E } < B _ { w } [ t ] < B _ { I } , \ F _ { w } [ t - 1 ] = 1 , } \\ { 0 , } & { \mathrm { i f } \ B _ { w } [ t ] \leq B _ { E } o r \ B _ { E } < B _ { w } [ t ] < B _ { I } , F _ { w } [ t - 1 ] = 0 , } \end{array} \right.\tag{9}
$$

where $B _ { E }$ and $B _ { I }$ are the given E-node threshold and the Inode threshold, respectively, with $P _ { W } \vartheta < B _ { E } < B _ { I }$ . From (9), $\mathrm { W N } { - } w$ becomes an E-node in slot t when $B _ { w } [ t ] \leq B _ { E }$ , and an I-node in slot t when $B _ { w } [ t ] \geq B _ { I }$ . When $B _ { E } < B _ { w } [ t ] < B _ { I }$ ï¼ there are two cases: 1) if WN-w is an I-node in the previous slot t â 1 with $F _ { w } [ t - 1 ] = 1$ , since $B _ { w } [ t ]$ is still higher than the E-node threshold $B _ { E }$ , it keeps transmitting data as an I-node in slot t; and 2) if WN-w is an E-node in the previous slot tâ1 with $F _ { w } [ t - 1 ] = 0$ , since $B _ { w } [ t ]$ does not exceed the I-node threshold $B _ { I }$ , WN-w continues harvesting energy as an E-node in slot t.

It is noted that unlike the widely-used single threshold to determine each WNâs type in, e.g., [1], where each WNâs data transmission is often suspended due to the frequently-changed node type, by consuming the battery energy from higher than $B _ { I }$ to lower than $B _ { E }$ with a sufficiently large $B _ { I } - B _ { E }$ under (9), each I-nodeâs data transmission becomes more reliable.

## E. UAVsâ Energy Consumption Model

The energy consumption of each UAV is mainly caused by the UAVâs movement, WET and WDC. Denote $P _ { I }$ as the fixed WDC power consumption at each UAV. The total WDC energy consumption of UAV-u in slot t is $\begin{array} { r } { \sum _ { w = 1 } ^ { W } \sum _ { k = 1 } ^ { K } D _ { u , w } ^ { t } [ k ] P _ { I \varrho . } } \end{array}$ From [29], UAV-uâs propulsion power consumption in slot t is determined by its velocity $\begin{array} { r } { V _ { u } [ t ] \triangleq \frac { 1 } { \vartheta } \Vert q _ { u } [ t + \overline { { 1 } } ] - q _ { u } [ t ] \Vert } \end{array}$ as follows:

$$
\begin{array} { l } { { \displaystyle P _ { p r o } ( V _ { u } [ t ] ) = P _ { a } \left( 1 + \frac { 3 V _ { u } [ t ] ^ { 2 } } { V _ { t i p } ^ { 2 } } \right) + \frac { 1 } { 2 } f _ { 0 } \varpi e _ { 1 } A V _ { u } [ t ] ^ { 3 } } } \\ { { \displaystyle ~ + P _ { b } \left( \sqrt { 1 + \frac { V _ { u } [ t ] ^ { 4 } } { 4 e _ { 0 } ^ { 4 } } } - \frac { V _ { u } [ t ] ^ { 2 } } { 2 e _ { 0 } ^ { 2 } } \right) ^ { \frac { 1 } { 2 } } , } } \end{array}\tag{10}
$$

where the details of the constant parameters $P _ { a } , P _ { b } , V _ { t i p } , e _ { 0 }$ $f _ { 0 } , \ \varpi , \ e _ { 1 }$ and A are given in [29]. The propulsion energy consumption of UAV-u in slot t is obtained as $P _ { p r o } ( V _ { u } [ t ] ) \vartheta$ The WET energy consumption of UAV-u in slot t is obtained as $Z _ { u } [ t ] P _ { U } \vartheta$ . Hence, UAV-uâs total energy consumption in slot t is $\begin{array} { r } { E _ { u } [ t ] = \sum _ { w = 1 } ^ { W } \sum _ { k = 1 } ^ { K } D _ { u , w } ^ { t } [ k ] P _ { I } \varrho + P _ { p r o } ( V _ { u } [ t ] ) \vartheta + } \end{array}$ $Z _ { u } [ t ] P _ { U } \vartheta$ . Denote $B _ { u } [ t ]$ as the battery energy level of UAV-u at the beginning of slot $t \in \mathcal T$ . We obtain that

$$
B _ { u } [ t ] = \operatorname* { m a x } \left( B _ { u } [ t - 1 ] - E _ { u } [ t - 1 ] , 0 \right) .\tag{11}
$$

Assume that each UAV is fully charged at the initial with $B _ { u } [ 0 ] = B _ { U } ^ { \mathrm { m a x } }$ , where $B _ { U } ^ { \mathrm { m a x } }$ is the UAV battery capacity. At the end of the last slot $t = T$ , UAV-uâs remained battery energy, denoted by $B _ { u } ^ { e n d }$ , is obtained by substituting $t = T + 1$ into (11).

## III. PROBLEM FORMULATION AND MAHDRL FRAMEWORK

## A. Problem Formulation

We jointly optimize the trajectories $Q = \{ q _ { u } [ t ] \}$ , the WET decisions $Z = \{ Z _ { u } [ t ] \}$ , and the WDC decisions $\pmb { D } =$ $\{ D _ { u , w } ^ { t } [ k ] \}$ of all the UAVs, to maximize the WNsâ total transmission data size $C _ { t o t a l }$ , subject to the constraints on each WNâs minimum required transmission data size, and each WNâs battery energy and WN type variations over time, as well as each UAVâs trajectory and battery energy constraints. The problem is formulated as (P1).

In problem (P1), the constraint in (12) guarantees that the overall transmission data size of each WN in T slots is no smaller than the minimum required data size $C _ { \mathrm { m i n } } > 0 ;$ the constraint in (13) ensures that each UAVâs velocity does not exceed the maximum allowable velocity $V _ { U } ^ { \mathrm { m a x } }$ ; the constraint in (14) guarantees that UAV-uâs remained battery energy at the end is not lower than a required level $B _ { U } ^ { \mathrm { m i n } }$ for, $\mathrm { e . g . }$ , its safe return; the constraints in (15) and (16) represent the binary WDC and WET decisions of each UAV, respectively; the constraint in (17) assures a safe distance of $d _ { \mathrm { m i n } }$ between any two UAVs.

$$
\begin{array} { r l } & { ( \mathrm { P 1 } ) : \displaystyle \operatorname* { m a x } _ { Q , Z , D } \ \sum _ { t = 1 } ^ { T } \sum _ { w = 1 } ^ { W } C _ { w } [ t ] } \\ & { \qquad \mathrm { s . t . ~ } ( 4 ) , ( 5 ) , ( 8 ) , ( 9 ) , ( 1 1 ) , } \end{array}
$$

$$
\sum _ { t = 1 } ^ { T } C _ { w } [ t ] \geq C _ { \operatorname* { m i n } } , \forall w \in \mathcal { W } ,\tag{12}
$$

$$
V _ { u } [ t ] \leq V _ { U } ^ { \operatorname* { m a x } } , \forall u \in \mathcal { U } , \forall t \in \mathcal { T } ,\tag{13}
$$

$$
B _ { u } ^ { e n d } \geq B _ { U } ^ { \operatorname* { m i n } } , \forall u \in \mathcal { U } ,\tag{14}
$$

$$
D _ { u , w } ^ { t } [ k ] \in \{ 0 , 1 \} , \forall u \in \mathcal { U } , \forall w \in \mathcal { T } [ t ] , \forall t \in \mathcal { T } ,\tag{15}
$$

$$
Z _ { u } [ t ] \in \{ 0 , 1 \} , \forall u \in \mathcal { U } , \forall t \in \mathcal { T } ,\tag{16}
$$

$$
d _ { u } ^ { u ^ { \prime } } [ t ] \geq d _ { \operatorname* { m i n } } , \forall u , u ^ { \prime } \in \mathcal { U } , u \neq u ^ { \prime } , \forall t \in \mathcal { T } ,\tag{17}
$$

Problem (P1) is a very complicated mixed-integer programming problem, which is difficult to solve optimally. In particular, to maximize $C _ { t o t a l } .$ , the WNs are expected to become the I-nodes to transmit data in most of the T slots based on (9), which in turn requires each E-node to harvest sufficient energy rapidly. However, due to the E-nodesâ different battery energy levels and thus different amounts of energy required to harvest to reach the threshold $B _ { E }$ in (9), it is difficult to ensure that most of the E-nodes along each UAVâs trajectory can become the I-nodes in each slot. Moreover, while the multiple UAVs with binary WET decisions are encouraged to stay close to enhance an E-nodeâs harvested energy, due to the additive property of the harvested energy in (3), they may also be required to stay far away from each other to alleviate their received co-channel interference for WDC. As a result, the multi-UAVsâ decisions on their trajectories and the binary WET and WDC selections are all tightly coupled over time under the time-varying WN types. In addition, all the UAVs must use their limited on-board energy carefully to meet (13) and (17). Therefore, problem (P1) is very challenging to solve.

## B. Proposed MAHDRL Framework

Given the high complexity to solve problem (P1), the DRL approach is leveraged. Since there lacks a central controller to determine all the UAVsâ Q, Z and D, we consider a multi-agent based DRL approach with each UAV as an agent [30], [31], [32]. However, it is noted that the existing multi-agent based DRL approach using a single DRL algorithm (e.g., DQN [33]) may not be able to solve the proposed problem (P1) properly, mainly due to the following three reasons: 1) Problem (P1) involves UAV-uâs policy decisions over two different time scales, where one is over the time slots for determining $\{ Z _ { u } [ t ] \}$ and $\{ q _ { u } [ t ] \}$ and the other is over the sub-slots for determining $\{ D _ { u , w } ^ { t } [ k ] \}$ ï¼ and thus requires at least two DRL algorithms, each for one time scale; 2) Since a more rapid decision is required for $\{ D _ { u , w } ^ { t } [ k ] \}$ over the sub-slots than $\{ Z _ { u } [ t ] \}$ and $\{ q _ { u } [ t ] \}$ over the time slots, a lower DRL algorithm complexity is required for the time scale of sub-slots than that over the time slots; 3) Although $Z _ { u } [ t ]$ and $\{ D _ { u , w } ^ { t } [ k ] \}$ are binary, the trajectory $q _ { u } [ t ]$ is continuous. This requires the DRL algorithm working over the time slots to have continuous action outputs.

To meet the above requirements, a multi-agent based two-tier hierarchical DRL design is proposed to solve problem (P1). As shown in Fig. 1, in the two-tier model at each UAV-u, the SAC algorithm [34] with continuous action outputs is employed in tier-1 to determine UAV-uâs trajectories and WET decisions over slots; and in tier-2, based on the determined trajectory in tier-1, the DQN with discrete action outputs is applied to determine UAV-uâs WDC decisions over sub-slots. Moreover, although the off-line trained SAC policy is distributively executed at each UAV at tier-1 in the implementation stage, due to the higher complexity of the SAC algorithm than the DQN, as well as the UAVsâ mutually coupled decisions on Q, Z and D in problem (P1), the SAC is trained centrally (at, e.g., the central trainer) by using the observations gathered from all the UAVs in the training stage. The DQN in tier-2 is both trained and executed at each UAV distributively. As will be specified in the following two sections, since the UAVs may not be able to obtain all the WNsâ status, both the SAC and the DQN adopt the POMDP-based modeling.

## IV. SAC IN TIER-1

## A. Observation and POMDP State

As shown in Fig. 1, the central trainer gathers the local observations of all the UAVs for the SACâs training. Each UAV observes the $\mathrm { W N s } ^ { \prime }$ status from their periodic status reporting at the beginning of each slot t via a common ground-to-air channel. For each E-node-w, it reports its current battery energy level $B _ { w } [ t ]$ and the accumulated transmission data size $\sum { _ { t ^ { \prime } = 1 } ^ { t - 1 } C _ { w } [ t ^ { \prime } ] }$ from the first slot to the previous slot $t - 1$ to all the UAVs. However, due to its very limited battery energy and thus weak transmit power for status reporting, only (if any) UAVs that locate within a given horizontal distance of $d _ { \mathrm { c o v } } > 0$ to E-node-w can receive its reporting. Hence, depending on their horizontal distance $d _ { r e p , w } ^ { u } [ t ] = \sqrt { ( x _ { u } [ t ] - x _ { w } ) ^ { 2 } + ( y _ { u } [ t ] - y _ { w } ) ^ { 2 } }$ in slot t, the observation of E-node-wâs battery level at UAV-u, denoted by $B _ { w } ^ { u } [ t ]$ , is given as

$$
B _ { w } ^ { u } [ t ] = \left\{ \begin{array} { l l } { B _ { w } [ t ] , } & { \mathrm { i f ~ } d _ { r e p , w } ^ { u } [ t ] \leq d _ { \mathrm { c o v } } , } \\ { B _ { w } ^ { u } [ t - 1 ] , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. , \forall w \in { \mathcal E } [ t ] ,\tag{18}
$$

where i $\mathsf { f } d _ { r e p , w } ^ { u } [ t ] \leq d _ { \mathrm { c o v } } , B _ { w } ^ { u } [ t ]$ is updated as E-node-wâs actual battery energy $B _ { w } [ t ]$ or keeps unchanged as $B _ { w } ^ { u } [ t - 1 ]$ . Due to the generally high power sensitivity $P _ { s e n } \mathrm { i n } ( 2 ) , \mathrm { i f } d _ { r e p , w } ^ { u } [ t ] > d _ { \mathrm { c o v } } ,$ it is assumed that E-node-w harvests zero energy from UAV-u in slot t, i.e., $\bar { P } ( P _ { U } Z _ { u } [ t ] G _ { w } ^ { u } [ t ] ) \vartheta = 0 $ . Similarly, denote UAV-uâs observation of E-node-wâs accumulated transmission data size by $C _ { w } ^ { u } [ t ]$ , which is obtained as

$$
C _ { w } ^ { u } [ t ] = \left\{ \begin{array} { l l } { \sum _ { t ^ { \prime } = 1 } ^ { t - 1 } C _ { w } [ t ^ { \prime } ] , } & { \mathrm { i f ~ } d _ { r e p , w } ^ { u } [ t ] \leq d _ { \mathrm { c o v } } , } \\ { C _ { w } ^ { u } [ t - 1 ] , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. , \forall w \in \mathcal { E } [ t ] .\tag{19}
$$

For each I-node-w, besides $B _ { w } [ t ]$ and $\textstyle \sum _ { t ^ { \prime } = 1 } ^ { t - 1 } C _ { w } [ t ^ { \prime } ]$ , it also reports its current WN type $F _ { w } [ t ] = 1$ to all the UAVs. Due, to their sufficient battery energy to support the status reporting, it is assumed that each I-nodeâs reported information can be well received at all the UAVs. Hence, for any $\mathrm { U A V } â u$ , we have $B _ { w } ^ { u } [ t ] = B _ { w } [ t ]$ and $\begin{array} { r } { C _ { w } ^ { u } [ t ] = \sum _ { t ^ { \prime } = 1 } ^ { t - 1 } C _ { w } [ t ^ { \prime } ] , \bar { \forall } w \in \mathcal { T } [ t ] } \end{array}$ . Considering the very short reporting time period, we assume that only trivial amount of energy is consumed at each E-node and I-node for status reporting, and thus is ignored in (4) and (8), respectively, for their battery energy updating.1

At each UAV agent, based on its received reporting from the WNs at the beginning of each slot t, the observation of UAV-u in slot t is given as $\begin{array} { r } { o _ { u } ^ { S } [ t ] = \{ F _ { 1 } [ t ] , . . . , F _ { W } [ t ] , B _ { 1 } ^ { u } [ t ] , . . . , B _ { W } ^ { u } [ t ] } \end{array}$ $C _ { 1 } ^ { u } [ t ] , . . . , C _ { W } ^ { u } [ t ] , \bar { x _ { u } } [ t ] , y _ { u } [ t ] , \bar { B _ { u } } [ t ] \}$ , which consists of all the WNsâ actual node types in slot t, all the WNsâ battery energy levels observed at UAV-u, all the WNsâ accumulated transmission data size observed at UAV-u, and UAV-uâs own horizontal location and battery energy in slot t. Denote $\mathcal { O } ^ { S }$ as the observation space with $\bar { o } _ { u } ^ { S } [ t ] \in \bar { \mathcal { O } } ^ { S }$ . Specifically, for the observation of $\{ F _ { w } [ t ] \}$ , UAV-u can easily identify the I-node set $\mathcal { T } [ t ]$ as the set of WNs who report $F _ { w } [ t ] = 1$ in slot t and thus obtains the E-node set as $\mathscr { E } [ t ] = \mathscr { W } - \mathscr { T } [ t ]$ . By labeling $F _ { w } [ t ] = 0$ for any $w \in \mathcal { E } [ t ]$ , UAV-u observes all the WNsâ actual node types. For the observation of $\{ B _ { 1 } ^ { u } [ t ] , . . . , B _ { W } ^ { u } [ t ] \}$ and $\{ C _ { 1 } ^ { u } [ t ] , . . . , C _ { W } ^ { u } [ t ] \}$ while the I-nodesâ actual battery energy levels and accumulated data size are obtained based on their reporting, the E-nodesâ battery energy levels and accumulated data size are generally partially observable at UAV-u as given in (18) and (19), respectively.

<!-- image-->  
Fig. 2. Central training of the SAC policy.

As a result, since $U < W$ generally holds in practice, the gathered observations from all the U UAVs at the central trainer only provides partial information about all the W WNsâ status in slot t in general. This leads to a POMDP modeling at the central trainer. Denote the POMDP state [35] in slot t as $s [ t ] =$ $\{ o _ { 1 } ^ { S } [ t ] , . . . , o _ { U } ^ { S } [ t ] \}$ , which is stored in the replay buffer at the central trainer, as shown in Fig. 2. The POMDP state space is denoted as S with $s [ t ] \in S$

## B. Action and Reward Function

For each UAV-u, the output of the SAC policy in each slot t contains UAV-uâs horizontal moving angle $\varphi _ { u } [ t ]$ , velocity $V _ { u } [ t ]$ and WET decision $Z _ { u } [ t ]$ , where $q _ { u } [ t ]$ is easily obtained from $( \varphi _ { u } [ t ] , V _ { u } [ t ] )$ . We thus denote the action of UAV-u in the POMDP model as $a _ { u } ^ { S } [ t ] = \{ \varphi _ { u } [ t ] , V _ { u } [ t ] , Z _ { u } [ t ] \}$ , where $( \varphi _ { u } [ t ] , V _ { u } [ t ] )$ is assured to satisfy the constraint in (13) by using the range mapping function in [7]. Since the SAC has continuous action output [34], to satisfy the binary WET decision constraint in (16), we let $Z _ { u } [ t ] = 1$ when the SAC policy networkâs WET decision output is positive, or $Z _ { u } [ t ] = 0$ , otherwise. The action space is denoted as $\mathcal { A } ^ { S }$ with $a _ { u } ^ { S } [ t ] \in \mathcal { A } ^ { S }$

In each slot t, based on UAV-uâs observation $o _ { u } ^ { S } [ t ]$ , it implements an action $a _ { u } ^ { S } [ t ] \in \mathcal { A } ^ { S }$ , and obtains a reward at the end of slot t. As will be specified in the next subsection, the trajectory determined by the SAC policy is used as a known state for the POMDP modeling of the DQN for WDC decisions. Hence, to find a proper trajectory for each UAVâs WET in tier-1 and WDC in tier-2, the SAC reward function $r _ { u } ^ { S } [ t ]$ is designed to achieve a proper trade-off between maximizing the E-nodesâ harvested energy and the I-nodesâ transmission data size under the constraints given in (12), (14) and (17) for problem (P1). To be specific, the reward function includes the following four parts:

1) Reward on WET to E-nodes: Due to the generally different battery energy of the E-nodes, their energy demands are different in general. To provide on-demand WET to the E-nodes, we adopt the metric of HoE to measure each WNâs time-varying energy demands as in [23]. Denote $H _ { w } [ t ]$ as the HoE of WN-w in slot t. If w â I[t], WN-w is an I-node with $H _ { w } [ t ] = 0 ;$ and If $w \in \mathcal { E } [ t ]$ ï¼ WN-w is an E-node with its $H _ { w } [ t ]$ given as:

$$
\begin{array} { r } { H _ { w } [ t ] = \left\{ \begin{array} { l l } { H _ { w } [ t - 1 ] + 1 , } & { \mathrm { i f ~ } E _ { w } ^ { h a r } [ t - 1 ] < E ^ { e x p } , } \\ { \operatorname* { m a x } ( H _ { w } [ t - 1 ] - 1 , 1 ) , } & { \mathrm { i f ~ } E _ { w } ^ { h a r } [ t - 1 ] \geq E ^ { e x p } , } \end{array} \right. } \end{array}\tag{20}
$$

where $\begin{array} { r } { E ^ { e x p } = \frac { B _ { I } - B _ { E } } { T } } \end{array}$ represents the average energy amount that is expected to harvest at each E-node in each slot, such that it can transform to an I-node based on (9) for at least one time on average during the T slots. From (20), the HoE of E-node-w is increased by 1 if $E _ { w } ^ { h a r } [ t { - } 1 ] < E ^ { e x p }$ , or reduced by 1, otherwise. In each slot t, the minimum HoE is set to 1 for all the E-nodes. Denote UAV-uâs reward on WET to all the E-nodes in slot t by $b _ { u } ^ { W E T } [ t ]$ and is given as

$$
b _ { u } ^ { W E T } [ t ] = N _ { u } [ t ] \cdot \sum _ { w \in \mathcal { E } [ t ] } H _ { w } [ t ] ( B _ { w } ^ { u } [ t + 1 ] - B _ { w } ^ { u } [ t ] ) ,\tag{21}
$$

where $\begin{array} { r } { N _ { u } [ t ] = \sum _ { w \in \mathcal { E } [ t ] } \frac { \bar { P } ( P _ { U } Z _ { u } [ t ] G _ { w } ^ { u } [ t ] ) \vartheta } { B _ { w } ^ { u } [ t + 1 ] - B _ { w } ^ { u } [ t ] } } \end{array}$ is UAV-uâs WET weight by charging all the E-nodes, with $\frac { \bar { P } ( P _ { U } Z _ { u } [ t ] G _ { w } ^ { u } [ t ] ) \vartheta } { B _ { w } ^ { u } [ t + 1 ] - B _ { w } ^ { u } [ t ] }$ representing the ratio of E-node-wâs harvested DC energy from $\mathrm { U A V } â u$ to that from all the UAVs, and $\begin{array} { r } { \sum _ { w \in { \mathcal E } [ t ] } H _ { w } [ t ] ( B _ { w } ^ { u } [ t + } \end{array}$ $1 ] - B _ { w } ^ { u } [ t ] )$ is the sum of each E-nodeâs increased battery energy in slot t biased by its HoE. If $B _ { w } ^ { u } [ t + 1 ] - B _ { w } ^ { u } [ t ]$ is zero for a particular E-node-w, since $\bar { P } ( P _ { U } Z _ { u } [ t ] G _ { w } ^ { u } [ t ] ) \vartheta = 0 $ is also obtained, as detailed in Section IV-A, we set $\begin{array} { r } { \frac { \bar { P } ( \bar { P } _ { U } Z _ { u } [ t ] G _ { w } ^ { u } [ t ] ) \vartheta } { B _ { w } ^ { u } [ t + 1 ] - B _ { w } ^ { u } [ t ] } = 0 } \end{array}$ It is easy to find from (21) that UAV-u generally gets more reward by transmitting energy to the E-nodes with higher HoE and/or higher $G _ { w } ^ { u } [ t ]$ . Hence, $b _ { u } ^ { W E T } [ t ]$ reflects the effects of UAV-uâs WET on increasing all the E-nodesâ battery energy according to their demands in slot t.

2) Reward on WDC from I-nodes: Let $b _ { u } ^ { W D C } [ t ]$ represent UAV-uâs reward on collecting data from the I-nodes in slot t, which is expressed as

$$
b _ { u } ^ { W D C } [ t ] = \sum _ { w \in \mathbb { Z } [ t ] } \left( \sum _ { t ^ { \prime } = 1 } ^ { t } C _ { w } [ t ^ { \prime } ] - \frac { t } { T } C _ { \operatorname* { m i n } } \right) .\tag{22}
$$

In (22), $\begin{array} { r l } { ~ } & { { } \sum _ { t ^ { \prime } = 1 } ^ { t } C _ { w } [ t ^ { \prime } ] \ \mathrm { o r } \ \frac { t } { T } C _ { \mathrm { m i n } } } \end{array}$ gives I-node-wâs accumulated data size that is already transmitted or expected to transmit on average from the first slot to the current slot t, respectively. The larger value $b _ { u } ^ { W D C } [ t ]$ achieves, the larger reward UAV-u obtains to meet the constraint in (12). It is noted that under the UAVâs trajectory from the SAC policy, $\textstyle \sum _ { t ^ { \prime } = 1 } ^ { t } C _ { w } [ t ^ { \prime } ]$ is determined by the UAVâs WDC decisions from the DQN policy in tier-2. Hence, the SAC policy and the DQN policy in the two tiers are mutually affected in general.

3) Reward on Energy Saving: Denote $b _ { u } ^ { E S } [ t ]$ as UAV-uâs reward on saving its own battery energy in slot t to meet the constraint in (14). We have $b _ { u } ^ { E S } [ \dot { t } ] = \dot { B _ { u } } [ t + 1 ] - B _ { U } ^ { \mathrm { m i n } }$ , which requires to be positive for maximizing UAV-uâs reward.

4) Reward on Safe Distance: Denote $b _ { u } ^ { S D } [ t ]$ as UAV-uâs reward on keeping the safe distance of $d _ { \mathrm { m i n } }$ to any other UAV to meet the constraint in (17), where we set $b _ { u } ^ { S D } [ t ] = - 1$ if the constraint in (17) is not satisfied, or $b _ { u } ^ { S D } [ t ] = 0$ , otherwise.

TABLE II SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>h</td><td rowspan=1 colspan=1>5m</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>-90 dBm</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \ { P } } } _ { U } , \underline { { \ { P } } } _ { W } , \underline { { \ P } } _ { I }$ </td><td rowspan=1 colspan=1> $\overline { { 1 \mathrm { ~ W } , 0 . 1 \mathrm { ~ m W } , 1 0 \mathrm { ~ m W } } }$ </td><td rowspan=1 colspan=1> $\overline { { P _ { s e n } , P _ { s a t } } }$ </td><td rowspan=1 colspan=1>-10,7 dBm</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \alpha _ { L } , \alpha _ { N } } }$ </td><td rowspan=1 colspan=1>3,5</td><td rowspan=1 colspan=1> $\overline { { B _ { E } , B _ { I } } }$ </td><td rowspan=1 colspan=1>2,4 mWÂ·s</td></tr><tr><td rowspan=1 colspan=1> $\overline { { B _ { u } ^ { m i n } , B _ { u } ^ { m a x } } }$ </td><td rowspan=1 colspan=1>3e4,4e5WÂ·s</td><td rowspan=1 colspan=1> $\underbrace { d _ { m i n } , C _ { m i n } } _ { }$ </td><td rowspan=1 colspan=1>2 m,100 bits/Hz</td></tr><tr><td rowspan=1 colspan=1>E-greedy strategy</td><td rowspan=1 colspan=1> $\overline { { 0 . 0 1 \to 1 e - 6 } }$ </td><td rowspan=1 colspan=1> $\xi _ { 1 } , \xi _ { 2 } , \xi _ { 3 } , \xi _ { 4 }$ </td><td rowspan=1 colspan=1>20,0.01,1e-6,1</td></tr><tr><td rowspan=1 colspan=1>Î³ï¼T</td><td rowspan=1 colspan=1>0.99,0.999</td><td rowspan=1 colspan=1>a,b forPLoS</td><td rowspan=1 colspan=1>12.08,0.11</td></tr><tr><td rowspan=1 colspan=1>replaybuffer&#x27;ssize</td><td rowspan=1 colspan=1>131072</td><td rowspan=1 colspan=1>mini-batch&#x27;s size</td><td rowspan=1 colspan=1>128</td></tr></table>

Since all the four rewards have different units and magnitudes, they cannot be directly summed up. We multiply the non-negative coefficients $\xi _ { 1 } , \ \xi _ { 2 } , \ \xi _ { 3 }$ and $\xi _ { 4 }$ to $b _ { u } ^ { W E T } [ t ]$ $b _ { u } ^ { W D C } [ t ] , b _ { u } ^ { \check { E } S } [ t ]$ and $b _ { u } ^ { S D } [ t ]$ , respectively, to assure the different rewards have the same or similar magnitudes, and obtain the overall reward function as $r _ { u } ^ { S } [ t ] = \xi _ { 1 } \bar { b _ { u } ^ { W E T } } [ t ] + \xi _ { 2 } b _ { u } ^ { W D C } [ t ] +$ $\xi _ { 3 } b _ { u } ^ { E S } [ t ] + \xi _ { 4 } b _ { u } ^ { S D } [ t ]$ . The values of the 4 coefficients for simulations are given in Table II. We denote the reward space as $\mathcal { R } ^ { S }$ with $r _ { u } ^ { S } [ t ] \in \mathcal { R } ^ { S }$

## C. SAC Training at the Central Trainer

Given the limited computational resources available to each UAV and the restricted range for the E-nodesâ status reporting, the SAC policy is centrally trained at the central trainer, to enhance the POMDP state observation completeness and alleviate the computational burden on the UAVs. As shown in Fig. 2, there are a total of U parallelly-trained SAC models at the central trainer, each for one UAV. Each SAC model consists of five neural networks, which are the policy network Actor-u with parameter $\theta _ { u } .$ , the two state networks $V _ { u , 1 }$ Net and $V _ { u , 2 }$ Net with parameters $\phi _ { u , 1 }$ and $\phi _ { u , 2 }$ , respectively, for V critic, and the two state-action networks $Q _ { u , 1 }$ Net and $Q _ { u , 2 }$ Net with parameters $\eta _ { u , 1 }$ and $\eta _ { u , 2 }$ , respectively, for Q critic. After the central training, the well-trained parameters of the Actor-u network at the central trainer is then copied to UAV-u.

From Fig. 2, the two V critic networks and the two Q critic networks, are used to assist the training of Actor-u, and the entropy $\mathcal { H } ( \cdot )$ that is used to design the loss function can enhance the agent UAV-uâs exploration of the environment [34]. To be specific, the policy network Actor-u trains the policy function $\pi _ { u } ^ { S } ( \cdot )$ that maps the observation $o _ { u } ^ { S } [ t ]$ of UAV-u to its action $a _ { u } ^ { S } [ t ] , V _ { u , 1 }$ Net and $V _ { u , 2 }$ Net train the state-action functions $V _ { u , 1 } ( \cdot )$ and $V _ { u , 2 } ( \cdot )$ , respectively, and $Q _ { u , 1 }$ Net and $Q _ { u , 2 }$ Net train the state functions $Q _ { u , 1 } ( \cdot )$ and $Q _ { u , 2 } ( \cdot )$ , respectively. The state functions $V _ { u , 1 } ( \cdot )$ and $V _ { u , 2 } ( \cdot )$ estimate the value of the cumulative discount reward received by UAV-u in state s[t]. We have $V _ { u , 1 } ( s [ t ] ) = \mathbb { E } _ { a _ { u } ^ { \prime } \sim \pi _ { u } ^ { S } } [ Q _ { \mathrm { m i n } } ( s [ t ] , a _ { u } ^ { S } [ t ] ) -$ $\alpha _ { u } \mathcal { H } ( \pi _ { u } ^ { S } ) ]$ , where $\mathcal { H } ( \pi _ { u } ^ { S } ) { = } \log ( \pi _ { u } ^ { S } ( a _ { u } ^ { \prime } | o _ { u } ^ { \bar { S } } [ t ] ) )$ is the entropy of the output action $a _ { u } ^ { \prime }$ based on policy $\pi _ { u } ^ { S }$ in observation $o _ { u } ^ { S } [ t ] , \ a _ { u } ^ { \prime } \sim \pi _ { u } ^ { S }$ denotes the action $a _ { u } ^ { \prime }$ taken from the policy $\pi _ { u } ^ { S } , Q _ { \mathrm { m i n } } ( \cdot ) = \mathrm { m i n } ( Q _ { u , 1 } ( \cdot ) , Q _ { u , 2 } ( \cdot ) )$ ), and $\alpha _ { u }$ is the temperature coefficient (i.e., the entropy weight). Generally, $\alpha _ { u }$ should be reduced with the number of trainings in order to ensure the convergence of Actor-u. Moreover, the state-action functions $Q _ { u , 1 } ( \cdot )$ and $Q _ { u , 2 } ( \cdot )$ estimate the cumulative discount reward value when UAV-u executes the action $a _ { u } ^ { S } [ t ]$ in state s[t]. We have $Q _ { u , m } ( s [ t ] , a _ { u } ^ { S } [ t ] ) = r _ { u } ^ { S } [ t ] + \gamma \mathbb { E } [ V _ { u , 2 } ( s [ t + 1 ] ) ]$ ], where Î³ is the discount factor and $\mathbb { E } [ \cdot ]$ is the operation of expectation. The goal is to find the optimal policy $\begin{array} { r } { \pi _ { u } ^ { \bar { S } * } = \arg \operatorname* { m a x } _ { \pi _ { u } ^ { S } } \sum _ { t \in \mathcal { T } } \mathbb { E } [ r _ { u } ^ { S } [ \bar { t } ] + } \end{array}$ $\alpha _ { u } \mathcal { H } ( \pi _ { u } ^ { S } ) \dag$ ] that maximizes the reward and the entropy gained at $\mathrm { U A V } â u$

The parameter $\theta _ { u }$ of the Actor-u network is sent from the central trainer to each UAV-u at regular intervals, and each UAV-u copies the received parameter $\theta _ { u }$ to its local Actor-u network, which outputs UAV-uâs action $a _ { u } ^ { S } [ t ] \in \mathcal { A } ^ { S }$ based on its local observation $o _ { u } ^ { \dot { S } } [ t ] \in \mathcal { O } ^ { S }$ in each slot t. After implementing the action $a _ { u } ^ { S } [ t ]$ , UAV-u obtains the reward $r _ { u } ^ { S } [ t ] \stackrel { } { \in } \mathcal { R } ^ { S }$ and the new observation $o _ { u } ^ { S } [ t + 1 ]$ at the beginning of slot $t + 1$ As shown in Fig. 1, the central trainer receives the combined information $( s [ \bar { t } ] , a _ { u } ^ { S } [ t ] , r _ { u } ^ { S } [ t ] , s [ t + 1 ] )$ from each UAV with $s [ t ] = \{ o _ { 1 } ^ { S } [ t ] , . . . , o _ { U } ^ { \bar { S } } [ \bar { t } ] \}$ as detailed in Section IV-A, and stores it in the replay buffer.

The parameters of the five neural networks in the SAC model u are updated to minimize the corresponding loss functions shown in Fig. 2. Specifically, the j-th training of the SAC model u is based on the experience of taking mini-batch $( s _ { j } , a _ { u , j } ^ { S } , r _ { u , j } ^ { S } , s _ { j } ^ { \prime } )$ from the replay buffer. Denote $\phi _ { u , 1 }$ as the parameter for the $V _ { u , 1 }$ Net. UAV-u uses the loss function

$$
\begin{array} { r l } & { L _ { V _ { u , 1 } } ( \phi _ { u , 1 } ) } \\ & { \ = \mathbb { E } \left[ \frac { 1 } { 2 } \left( V _ { u , 1 } ( s _ { j } ) - \mathbb { E } _ { a _ { u } ^ { \prime } \sim \pi _ { u } ^ { S } } \left[ Q _ { \operatorname* { m i n } } ( s _ { j } , a _ { u } ^ { \prime } ) - \alpha _ { u } \mathcal { H } _ { j } \right] \right) ^ { 2 } \right] , } \end{array}\tag{23}
$$

where the entropy $\mathcal { H } _ { j } = \log ( \pi _ { u } ^ { S } ( a _ { u } ^ { \prime } | o _ { u , j } ^ { S } ) )$ . For the parameter $\phi _ { u , 2 }$ of the $V _ { u , 2 }$ Net, we apply a soft update with $\phi _ { u , 2 }  \tau \phi _ { u , 2 } +$ $( 1 - \tau ) \phi _ { u , 1 } , \tau \in [ 0 , 1 )$ . Moreover, denote $\eta _ { u , m }$ as the parameter for the $Q _ { u , m }$ Net, $\forall m \in \{ 1 , 2 \}$ . The loss function for the $Q _ { u , m }$ Net is

$$
\begin{array} { r l } & { L _ { Q _ { u , m } } ( \eta _ { u , m } ) } \\ & { \ =  { \mathbb { E } \left[ \frac { 1 } { 2 } \left( Q _ { u , m } ( s _ { j } , a _ { u , j } ^ { S } ) - \left( r _ { u , j } ^ { S } + \gamma  { \mathbb { E } \left[ V _ { u , 2 } ( s _ { j } ^ { \prime } ) \right]   ^ { 2 }  } } . } \\right]end{ar\right)ray}\right) \end{array}\tag{24}
$$

For the SAC policy network Actor-u, we apply the following loss function:

$$
L _ { \pi _ { u } ^ { S } } ( \theta _ { u } ) = \mathbb { E } _ { \varepsilon \sim \chi } \left[ \alpha _ { u } \mathcal { H } _ { j } ^ { \prime } - Q _ { \operatorname* { m i n } } ( s _ { j } , a _ { \theta _ { u } } ( o _ { u , j } ^ { S } ; \varepsilon ) ) \right] ,\tag{25}
$$

where unlike the entropy $\mathcal { H } _ { j }$ in (23), the entropy $\mathcal { H } _ { j } ^ { \prime } =$ $\log ( \pi _ { u } ^ { S } ( a _ { \theta _ { u } } ( o _ { u , j } ^ { S } ; \varepsilon ) | o _ { u , j } ^ { S } ) )$ is calculated from the noise-action $a _ { \theta _ { u } } ( o _ { u , j } ^ { S } ; \varepsilon )$ , where $\varepsilon \sim \chi$ is the noise sample taken from a fixed distribution $\chi .$ According to [34], adding noise to the actions during the training can avoid network overfitting, and at the same time, increase UAV-uâs exploration of the environment. At last, for the update of the temperature coefficient $\alpha _ { u }$ , we use the loss function

$$
L _ { \alpha _ { u } } ( \alpha _ { u } ) = \mathbb { E } _ { a _ { u } ^ { \prime } \sim \pi _ { u } ^ { S } } \left[ - \alpha _ { u } \log \left( \pi _ { u } ^ { S } ( a _ { u } ^ { \prime } | o _ { u , j } ^ { S } ) \right) - \alpha _ { u } \tilde { H } \right]\tag{26}
$$

where $\tilde { H }$ is a constant that is generally equal to the dimension of the observation $\ o _ { u } ^ { S } \ ( \mathrm { i . e . , ~ } \tilde { H } { = } | o _ { u } ^ { S } | )$ . All the parameters $\phi _ { u , 1 } .$ $\eta _ { u , m } , \theta _ { u } , \alpha _ { u }$ are updated as the optimal values that minimize the corresponding loss functions given in (23)â(26), respectively, by using the Adaptive moment estimation (Adam) optimization algorithm [36].

## V. DQN IN TIER-2

## A. POMDP Modeling for WDC Decisions

Based on the determined trajectory from the SAC in tier-1, DQN in tier-2 is used to determine each UAVâs binary WDC decisions over the K sub-slots. As compared to the SAC training, since the DQN model is simpler, to avoid large transmission overhead of neural network parameters with the central trainer, the training of the DQN in tier-2 is performed at each of the UAVs locally.

1) Observation: Similar to the case for observing the WNsâ status in Section IV-A, each UAV obtains its observation via the WNsâ periodic status reporting. Here, considering the triviallychanged environment over the sub-slots in the same slot, instead of impelling each WN to additionally report its status over sub-slots, we only use the WNsâ reported status at the beginning of each slot t. Denote, the observation of UAV-u at sub-slot k in slot t is $o _ { u } ^ { D , t } [ k ] = \{ x _ { u } [ t ] , y _ { u } [ t ] , C _ { 1 } ^ { u } [ t ] , . . . , C _ { W } ^ { u } [ t ] , k \}$ , which consists of UAV-uâs own horizontal location in slot t, all the WNsâ accumulated transmission data size from $t ^ { \prime } { = } 1$ to the previous slot tâ1, and the sub-slot index k. In $o _ { u } ^ { D , t } [ k ] , ( x _ { u } [ t ] , y _ { u } \bar { [ t ] } )$ is determined by the SAC policy in tier-1, $\{ C _ { w } ^ { u } [ t ] \}$ only provide partial information on all the WNsâ accumulated transmission data as specified in Section IV-A, and k is used to distinguish different sub-slots. By using $o _ { u } ^ { D , t } [ k ]$ as the observation for the DQN, we also obtain a POMDP for the UAV-uâs WDC decisions. Denote $\mathcal { O } ^ { D }$ as the observation space with $o _ { u } ^ { D , t } [ k ] \in \mathcal { O } ^ { D }$

2) Action and Reward: Denote $a _ { u } ^ { D , t } [ k ] = w \in \mathcal { W }$ as the POMDP action of UAV-u at sub-slot k in slot t. Given an observation $o _ { u } ^ { D , t } [ k ] \in \mathcal { O } ^ { D }$ , the DQNâs output is a Q-vector $Q ( o _ { u } ^ { D , t } [ k ] )$ of length W , where the w-th element gives the probability of scheduling ${ \sf W N - w } \in \mathcal { W }$ . To satisfy the one-to-one user association constraint in (5), we consider the following steps to determine each $D _ { u , w } ^ { t } [ k ] \colon \mathrm { a } )$ UAV-u initializes a WN candidate set $\mathcal { W } _ { c a } = \mathcal { W } ;$ b) UAV-u sets $D _ { u , w } ^ { t } [ k ] = 1$ for w = $\arg \operatorname* { m a x } _ { w \in \mathcal { W } _ { c a } } Q ( o _ { u } ^ { D , t } [ k ] )$ , and sets $D _ { u , i } ^ { t } [ k ] = 0 , \forall i \in \mathcal { W } , i \neq$ w; c) if the selected WN-w is an I-node, UAV-u sends an association request to WN-w; if WN-w is an E-node or WN-w feeds back UAV-u that UAV-u	 with u	 < u also selects it, UAV-u sets $D _ { u , w } [ k ] = 0$ , updates $\mathcal { W } _ { c a } = \mathcal { W } _ { c a } - \{ \boldsymbol { w } \}$ , and goes to step b). The above steps repeat until the selected I-node WN-w feeds back an association confirmation to UAV-u, or $\mathcal { W } _ { c a } = \emptyset$ is obtained. For the former case, UAV-u finds a proper I-node-w as its POMDP action that meets the constraint in (5), and for the latter case, UAV-u remains silent. Since $U < W$ and the required one-to-one association in (5), the above procedure is rapid to find $a _ { u } ^ { D , t } [ k ]$ . Denote the DQN action space as $\mathcal { A } ^ { D }$ with $a _ { u } ^ { \hat { D } , t } [ k ] \in \mathcal { A } ^ { D }$ . For $\mathrm { U A V }  â u \in \mathcal { U }$ , the reward function is expressed as

$$
r _ { u } ^ { D , t } [ k ] = \sum _ { w \in \mathbb { Z } [ t ] } M _ { u , w } ^ { t } [ k ] + \sum _ { w \in \mathbb { Z } [ t ] } \left( C _ { w } ^ { u } [ t ] - \frac { t - 1 } { T } C _ { \operatorname* { m i n } } \right) .\tag{27}
$$

In (27), the first item $\textstyle \sum _ { w \in { \mathcal { T } } [ t ] } M _ { u , w } ^ { t } [ k ]$ is UAV-uâs received data size at sub-slot k in slot t under the constraint in (5), and the second item $\begin{array} { r } { \sum _ { w \in \mathbb { Z } [ t ] } ( C _ { w } ^ { u } [ t ] - \frac { t - 1 } { T } C _ { \operatorname* { m i n } } ) } \end{array}$ is the sum of all I-nodesâ gap between their accumulated data size and the expected transmission data size $\textstyle { \frac { t - 1 } { T } } C _ { \operatorname* { m i n } }$ over the past tâ1 slots. With proper

<!-- image-->  
Fig. 3. Local training of the DQN at UAV-u.

WDC decisions, the UAV obtains large $\textstyle \sum _ { w \in { \mathcal { T } } [ t ] } M _ { u , w } ^ { t } [ k ]$ to assure the constraint in (12).

## B. DQN Training at Each Local UAV

As shown in Fig. 3, the DQN model at each local UAV contains two neural networks, which are the Evaluate-Q-u network and the Target-Q-u network with parameter $\lambda _ { u , 1 } , \lambda _ { u , 2 }$ , respectively. The Evaluate-Q-u network is trained as the state-action function $Q _ { u , 1 } ^ { D } ( \cdot )$ , which gives the UAV-uâs Q-value (i.e., the cumulative discount reward) distribution for different actions under the observation $o _ { u } ^ { D , t } [ k ]$ . The Target-Q-u network is trained as a stateaction function $\dot { Q } _ { u , 2 } ^ { D } ( \cdot )$ to guide the training of the Evaluate-Q-u network. The goal is to enable UAV-u to maximize its own cumulative discount reward $Q _ { u , 1 } ^ { D * } ( o , a )$ . According to [33], we have $\begin{array} { r } { Q _ { u , 1 } ^ { D * } ( o , a ) = r + \gamma \sum _ { o ^ { \prime } \in \mathcal { O } _ { D } } \mathcal { P } _ { o , o ^ { \prime } } ^ { a } } \end{array}$ maxa $Q _ { u , 1 } ^ { D * } ( o ^ { \prime } , a ^ { \prime } )$ ï¼ where $o = o _ { u } ^ { D , t } [ k ] , a = a _ { u } ^ { D , t } [ k ] , r = r _ { u } ^ { D , t } [ k ] , o ^ { \prime } = o _ { u } ^ { D , t + 1 } [ k ]$ a	 is the action with maximum Q-value at $\boldsymbol { o } ^ { \prime } ,$ and $\mathcal { P } _ { o , o ^ { \prime } } ^ { a }$ is the probability that UAV-u executes action a to get the next observation $o ^ { \prime }$ at the current observation o.

The parameter $\lambda _ { u , 1 }$ of the Evaluate-Q-u network is updated according to the following loss function

$$
L _ { Q _ { u , 1 } ^ { D } } ( \lambda _ { u , 1 } ) = \mathbb { E } \left[ \frac { 1 } { 2 } \left( Q _ { u , 1 } ^ { D } ( o _ { u , j } ^ { D } , a _ { u , j } ^ { D } ) - Q _ { t a r g e t } \right) ^ { 2 } \right] ,\tag{28}
$$

where $Q _ { t a r g e t } = ( r _ { u , j } ^ { D } + \gamma \operatorname* { m a x } _ { a ^ { \prime } } Q _ { u , 2 } ^ { D } ( o _ { u , j } ^ { D , ' } , a ^ { \prime } ) )$ , and the j-th training is performed based on the experience of taking a minibatch $( o _ { u , j } ^ { D } , a _ { u , j } ^ { D } , r _ { u , j } ^ { D } , o _ { u , j } ^ { D , ^ { \prime } } )$ from the local replay buffer. For the Target-Q-u network with parameter $\lambda _ { u , 2 }$ , we perform the asynchronous update based on the parameter $\lambda _ { u , 1 }$ , similar to the process in [33].

## C. MAHDRL Algorithm

Based on the SAC model in Section IV and the DQN model in Section V, the MAHDRL algorithm to solve the problem (P1) is given in Algorithm 1. In summary, for the SAC training in tier-1, the maximization of the WET reward in (21) guides the UAV to learn along the direction of increasing each E-nodeâs battery energy so as to transform more E-nodes into the I-nodes and, at the same time, the maximization of the WDC reward in (22) leads each UAV to increase $C _ { t o t a l }$ from the transformed I-nodes when determining its trajectory, while the reward maximizations of $b _ { u } ^ { E S } [ t ]$ and $b _ { u } ^ { S \breve { D } } [ t ]$ guide the UAVs to meet the constraints in (14) and (17), respectively. In tier-2, the maximization of the DQN reward in (27) further leads each UAV to maximize $C _ { t o t a l }$ under the constraint in (12). The constraints in (5), (13) and (16) are properly satisfied by the action output of the SAC and the DQN policies. Therefore, the proposed MAHDRL approach can properly solve problem (P1).

```latex
Algorithm 1: MAHDRL Algorithm.
1: Initialize replay buffer, learning rate, discount factor Î³,
soft update weight Ï and temperature factor $\alpha _ { u } , u \in \mathcal { U } .$
Initialize the parameters of SACâs all five networks and
DQNâs two networks;
2: for Episode $ 1 , . . . , E P S$ do
3: Initialize the locations and battery levels of all UAVs
and WNs;
4: Initialize the observation $o _ { u } ^ { S } [ 0 ] , o _ { u } ^ { D , 0 } [ 1 ] , . . . , o _ { u } ^ { D , 0 } [ K ]$
and SAC state $s [ 0 ] , \forall u \in \mathcal { U } ;$
5: for $t \gets 1 , . . . , T$ do
6: get action $a _ { u } ^ { S } [ t ]$ and $a _ { u } ^ { D , t } [ k ]$ based on Sections IV-B
and V-A2, respectively;
7: execute action $a _ { u } ^ { S } [ t ]$ , and $a _ { u } ^ { D , t } [ k ]$ , based on Sections
IV-B and V-A2, respectively;
8: store the experience $( s [ t ] , \dot { a } _ { u } ^ { S } [ t ] , r _ { u } ^ { S } [ t ] , s [ t + 1 ] )$ and
$( o _ { u } ^ { D , t } [ k ] , a _ { u } ^ { \hat { D , t } } [ k ] , r _ { u } ^ { D , t } [ k ] , o _ { u } ^ { D , t + 1 } [ k ] )$ into the replay
buffer;
9: using the loss functions in (23), (24), (25), (26) and
(28) to update the $\mathbf { S A C } \mathbf { \ ' } _ { \mathbf { S } }$ parameters based on
Section IV-C and update the DQNâs parameters
based on Section V-B, respectively;
10: $o _ { u } ^ { S } [ t ]  o _ { u } ^ { S } [ t + 1 ] , o _ { u } ^ { D , t } [ k ]  o _ { u } ^ { D , \bar { t } + 1 } [ k ]$ and
$s [ t ] \gets s [ t + 1 ] ;$
11: end for
12: end for
```

We now analyze the time complexity of implementing Algorithm 1. Let $L _ { A } = 5$ and $N _ { A , j } , L _ { V } = 5$ and $N _ { V , j }$ , and $L _ { Q } = 5$ and $N _ { Q , j }$ represent the number of fully connected layers and the number of neurons in the j-th layer of Actor-u network, $V _ { u , m } ~ ( m \in \{ 1 , 2 \} )$ Net, and $Q _ { u , m } \ \mathrm { N e t }$ , respectively. The time complexity of training the SAC at one step according to [34] is $\begin{array} { r } { \mathcal { O } ( \dot { \sum } _ { j = 2 } ^ { L _ { A } } N _ { A , j - 1 } \cdot N _ { A , j } + \sum _ { j = 2 } ^ { L _ { V } } N _ { V , j - 1 } \cdot \bar { N } _ { V , j } + } \end{array}$ $\textstyle \sum _ { j = 2 } ^ { L _ { Q } } N _ { Q , j - 1 } { \cdot } N _ { Q , j } )$ . Denote $L _ { E } = 5$ and $N _ { E , j }$ as the number of fully connected layers and the number of neurons in the j-th layer of the Evaluate-Q-u network, $u \in \mathcal { U }$ , respectively. The time complexity of training the DQN at one step according to [33] is $\mathcal { O } ( \overset { \cdot } { \sum } _ { j = 2 } ^ { L _ { E } } N _ { E , j - 1 } \cdot \overset { \cdot } { N _ { E , j } } )$ . Therefore, the time complexity of the proposed MAHDRL algorithm is $\mathcal { O } ( U \times E P S \times$ $\begin{array} { r } { T \times ( \sum _ { j = 2 } ^ { L _ { E } } N _ { E , j - 1 } \cdot N _ { E , j } + \sum _ { j = 2 } ^ { L _ { A } } N _ { A , j - 1 } \cdot N _ { A , j } + \sum _ { j = 2 } ^ { L _ { V } } N _ { V , j - 1 } \cdot 1 ) ^ { 2 } = 0 . 1 1 \cdot 1 0 ^ { - 3 } } \end{array}$ $\begin{array} { r } { N _ { V , j } + \sum _ { j = 2 } ^ { L _ { Q } } N _ { Q , j - 1 } { \cdot } N _ { Q , j } ) \big ) } \end{array}$ , which increases linearly over the number of the UAVs.

## VI. SIMULATION RESULTS

Simulation results are provided in this section to validate the performance of the proposed MAHDRL approach in Algorithm 1. As specified in Sections IV-C and V-B, in the training stage, the SAC policy is first trained centrally at the central trainer, where the well-trained parameters are then copied to tier-1 in each of the UAV agentâs DRL model. The DQN policy in tier-2 is trained locally at each of the UAV agent. In the test stage, all the UAVs distributively make their WET, WDC and trajectory decisions based on their own policy networks.

<!-- image-->  
Fig. 4. Comparison of MAHDRL with DDPG+DQN.

We perform simulations based on python-3.9.12 and pytorch-1.12.1. Unless otherwise stated, in all the simulations, we consider an area of $4 0 0 \mathrm { ~ m ~ } \times 4 0 0$ m and set $U = 4 ~ \mathrm { U A V s }$ with random start locations, W = 10 WNs with random initial battery energy in the range of [2, 4] mWÂ· s, the mission period $T = 3 0 0$ $s , K = 4$ sub-slots, and E-nodesâ reporting range $d _ { \mathrm { c o v } } = 2 0$ m. The UAVsâ propulsion power model parameters follow that in [29]. For the neural networks of the SAC and the DQN, we set the input layers with $N _ { A , 1 } = 3 W + 3 , N _ { V , 1 } = ( 3 W + 3 ) \times U$ $N _ { Q , 1 } = ( 3 W + 3 ) \times U + 3$ and $N _ { E , 1 } = W + 2$ , respectively, and set the output layers with $N _ { A , 5 } = 3 , N _ { V , 5 } = 1 , N _ { Q , 5 } = 1$ and $N _ { E , 5 } { = } W$ , respectively. According to [16], [31] and [37], for all the neural networks, 256 neurons are set in the hidden layers. For the SAC in tier-1, we set the learning rates for all the Actor, the Q Critic, and the V Critic networks to 0.0003, and set the temperature coefficient $\alpha _ { u } \mathrm { { ^ { s } } }$ learning rate to 0.0002. For the DQN at tier-2, its learning rate is set to decay from 0.01 to 0.000001, and its exploration rate of the environment is set to decay from 0.9 to 0.02. Other simulation parameters are given in Table II.

## A. Comparison With Benchmarks

1) Training Stage: In the training stage, we compare the proposed MAHDRL with a benchmark, where the widely-used DDPG model in [7] is adopted to replace the SAC in tier-1 in our proposed MAHDRL. For both approaches, the same DQN model as specified in Section V is used in tier-2 for each UAVâs WDC decisions. The SAC in the proposed MAHDRL and the DDPG in the benchmark have the same number of neural network layers and the same learning rate. Fig. 4 shows the WNsâ total transmission data size $C _ { t o t a l }$ over 2000 trainings under both approaches. It is observed that our proposed MAHDRL with the SAC outperforms the benchmark with DDPG, due to the entropy-based loss function in the SAC that encourages the

<!-- image-->  
Fig. 5. Comparison of MAHDRL with benchmarks.

UAVs to explore the environment more. Although $C _ { t o t a l }$ under the proposed MAHDRL approach fluctuates relatively wider than the benchmark, its fluctuation is still within an acceptable interval to achieve convergence.

2) Test Stage: In the test stage, where the UAVs apply the well-trained policies to determine their actions, we compare our proposed MAHDRL solution with the following four different benchmark schemes:

(a) MAHDRL w./o. HoE: Each E-nodeâs HoE is not considered in this scheme, and the reward in (21) is reduced to $\begin{array} { r } { b _ { u } ^ { W E T } [ t ] = N _ { u } [ t ] \cdot \sum _ { w \in \mathcal { E } [ t ] } ( B _ { w } ^ { u } [ t + 1 ] - B _ { w } ^ { u } [ t ] ) } \end{array}$ . All the other parts are the same as that in the proposed MAHDRL solution. (b) Phase Division: This benchmark scheme applies the classic time phase division for UAVsâ WET and WDC as in [6]. All the UAVs only transmit energy in the WET phase from slot t = 1 to slot $t = \bar { T } - 1$ , and only collect data from the I-nodes from slot $t = \bar { T }$ to slot $t = T$ . We find use the optimal TÂ¯ that maximizes $C _ { t o t a l }$ via one-dimensional exhaustive search. (c) TEAM: The TEAM scheme in [7] is applied, where the UAVs are divided into two groups, one group is only responsible for WET and the other is only for WDC. We equally divide the UAVs into two groups. (d) Random WDC: The DQN in tier-2 is replaced by the random scheduling of the I-nodes over the sub-slots. For all the benchmark schemes, each UAV still applies the SAC algorithm to find its own trajectory, and for the former three benchmark schemes, each UAV applies the DQN algorithm to schedule the I-nodes for WDC.

First, Fig. 5 shows the variations of $C _ { t o t a l }$ over T under the proposed and the above four benchmark schemes, respectively. It is observed that our proposed MAHDRL significantly outperforms all the benchmarks. This validates that by catering to the dynamic WN type updating over time, the performance of the multi-UAV aided WPCN can be largely improved.

Next, we compare the running time of the proposed MAHDRL approach with that of the benchmarks. It is easy to find from Section V-C that the MAHDRL w./o. HoE, the Phase Division and the TEAM have the same time complexity as our proposed MAHDRL approach, and the time complexity of the Random WDC approach is $\begin{array} { r } { \mathcal { O } ( U \times E P S \times T \times ( \sum _ { j = 2 } ^ { L _ { A } } N _ { A , j - 1 } . } \end{array}$

<!-- image-->  
Fig. 6. Running time comparison.

$$
\begin{array} { r } { N _ { A , j } + \sum _ { j = 2 } ^ { L _ { V } } N _ { V , j - 1 } \cdot N _ { V , j } + \sum _ { j = 2 } ^ { L _ { Q } } N _ { Q , j - 1 } \cdot N _ { Q , j } ) ) } \end{array}
$$

applying the DQN algorithm, which is less than our proposed MAHDRL approach and the other three benchmark approaches. In Fig. 6, since the MAHDRL w./o. HoE approach consumes almost the same running time as the proposed MAHDRL approach, we show the running time of the proposed MAHDRL, the Phase Division, the TEAM, and the Random WDC approaches under different UAV numbers. The running time of each approach is obtained as the average of 10 simulations, where each simulation result is trained with 100 episodes. It is observed from Fig. 6 that the running time of each approach almost doubles as the number of UAVs is doubled. Moreover, under each UAV number, the running time of the proposed MAHDRL is very close to that of the Phase Division and TEAM approaches, and the running time of the Random WDC approach is always the lowest. This is in accordance with our time complexity analysis, and further verifies the good performance of our proposed MAHDRL approach shown in Fig. 5, as compared to the benchmarks.

## B. Network Example

To further illustrate the performance of the proposed MAH-DRL scheme, we consider a network of a smaller scale, with 2 UAVs and 4 WNs randomly locating within a horizontal area of 300 mÃ300 m. Fig. 7 shows the UAVsâ trajectories and WET decisions over time. The shortest distance between the two UAVs in Fig. 7 is 2.74 m, which is larger than the required safe distance $d _ { \mathrm { m i n } }$ . It is also observed that each UAV does not always select $Z _ { u } [ t ] = 1$ to save its energy.

Fig. 8(a) and (b) show each WNâs type and battery energy variations over time, respectively, where each WNâs battery energy increases when it is an E-nodes, or decreases when it is an I-node. The WN type updating under the two thresholds $B _ { I }$ and $B _ { E }$ follows (9). It is also observed from Fig. 7 that since only UAV-1 comes to WN-1 and WN-2 for WET, they have fewer chances to become I-nodes than WN-3 and WN-4, where both UAVs fly to them and transmit energy. However, once WN-1 and WN-2 become I-nodes, they have higher chances to be scheduled to transmit data. The total transmission data size (bits/Hz) of the 4 WNs in the T slots is 263.42, 487.01, 638.49 and 733.88, respectively, satisfying the constraint in (12). It is also interesting to observe similar battery charging rates at WN-3 and WN-4 from time slot 176 to slot 268 in Fig. 8(b). This is mainly because that, as observed from Fig. 7, UAV-1 or UAV-2 flies in the neighborhood of WN-3 and WN-4 from slot 176 to slot 268 or slot 17 to slot 268, respectively. During the corresponding time slots, each UAV transmits energy to WN-3 and WN-4 from sufficiently short distances, such that (close to) saturated power is harvested at WN-3 and WN-4, which leads to their similar battery energy charging rates. Also, since the closely located UAV-2 can efficiently collect data from both WN-3 and WN-4, the battery energy decreasing rates are also similar.

<!-- image-->  
Fig. 7. UAVsâ trajectories and WET decisions.

We also show each WNâs battery energy under the MAHDRL w./o. HoE benchmark in Fig. 8(c). It is observed that unlike Fig. 8(b), where each WN can become an I-node with its battery energy exceeding $B _ { I }$ , WN-1 and WN-2 in Fig. 8(c) cannot harvest sufficient energy over all T slots and thus cannot meet the constraint in (12). This matches with Fig. 5, where our proposed MAHDRL outperforms the MAHDRL w./o. HoE benchmark. In addition, at the end of T = 300 slots, the remaining battery energy of the two UAVs are 72399.97 W Â· s and 30115.61 W Â· s, respectively, satisfying the constraint in (14).

Next, in Fig. 9, to show the scalability of our proposed MAHDRL approach, we gradually increase the network scale and show the achieved $C _ { t o t a l }$ under different $C _ { \mathrm { m i n } }$ , where we consider that the number of WNs always equals the twice of the number of UAVs, i.e. $W = 2 U$ . When the number of the UAVs increases from U = 1 to U = 30 in Fig. 9, the number of WNs increases from W = 2 to W = 60 accordingly. It is observed from Fig. 9 that when U = 1, the same $C _ { t o t a l }$ is achieved under different $C _ { \mathrm { m i n } } .$ , and when $1 < U < 1 2 .$ , a larger $C _ { t o t a l }$ is always achieved under a larger $C _ { \mathrm { m i n } }$ under each value of $U ,$ since most of the E-nodes can be properly transformed into I-nodes to meet $C _ { \mathrm { m i n } }$ ; however, when $U \geq 1 2$ , due to the increased information transmission interference under the large UAV number to meet a large $C _ { \mathrm { m i n } } .$ , it is found that a larger $C _ { t o t a l }$ is achieved under a smaller $C _ { \mathrm { m i n } }$ over each value of U . It is also observed that under each $C _ { \mathrm { m i n } }$ , the value of $C _ { t o t a l }$ always increases over the UAV number and thus the network scale. This verifies the scalability of our proposed MAHDRL approach.

<!-- image-->

<!-- image-->

<!-- image-->  
ï¼cï¼

Fig. 8. Network example: (a) WNsâ type variations. (b) WNsâ battery levels under MAHDRL. (c) WNsâ battery levels under MAHDRL w./o. HoE benchmark.  
<!-- image-->  
Fig. 9. Impact of UAV number on $C _ { t o t a l }$

<!-- image-->  
Fig. 10. Impact of $d _ { \mathrm { c o v } }$ on $C _ { t o t a l }$

At last, Fig. 10 shows the impact of the status reporting distance $d _ { \mathrm { c o v } }$ in (18) on $C _ { t o t a l } .$ . It is observed from Fig. 10 that as $d _ { c o v }$ increases, more information of the E-nodes can be obtained at the central trainer, and thus $C _ { t o t a l }$ increases; and when $d _ { c o v }$ is sufficiently large, such that almost each E-nodeâs complete status can be all obtained by the central trainer, the POMDP modeled in Sections IV-A and V-A approaches an MDP, respectively, where $C _ { t o t a l }$ is almost unchanged.

## VII. CONCLUSION

This paper proposed a novel design of the multi-UAV aided WPCN with repeatedly-changing WN types over time. By applying the LoS-probability based A2G channels, we utilized the practical non-linear energy harvesting model at each E-node, and further developed all the UAVsâ and the WNsâ battery energy management models. To effectively solve the complicated total transmission data size maximization problem, the new MAH-DRL framework with two tiers was proposed. We designed the central training of the SAC policy and the local training of the DQN policy by exploiting the interactions between the UAVs and the WNs. Once well trained, both the SAC policy and the DQN policy are executed distributivity at each UAV. Extensive simulations validated that our proposed MAHDRL approach that adapts to the network dynamics outperforms benchmarks. In practice, the deployment of the central trainer and its available computation resources may largely affect the performance of the multi-UAV aided WPCN. In the future work, it is interesting to study the UAV-enabled mobile central trainer and investigate the joint transmission and computation design of the multi-UAV aided WPCN.

## REFERENCES

[1] Y. Che, L. Duan, and R. Zhang, âSpatial throughput maximization of wireless powered communication networks,â IEEE J. Sel. Areas Commun., vol. 33, no. 8, pp. 1534â1548, Aug. 2015.

[2] Z. Wang, L. Duan, and R. Zhang, âAdaptively directional wireless power transfer for large-scale sensor networks,â IEEE J. Sel. Areas Commun., vol. 34, no. 5, pp. 1785â1800, May 2016.

[3] Y. Che, Z. Zhao, S. Luo, K. Wu, L. Duan, and V. Leung, âUAV-aided wireless energy transfer for sustaining Internet of Everything in 6G,â Drones, vol. 7, no. 10, pp. 628â639, 2023.

[4] J. Xu, Y. Zeng, and R. Zhang, âUAV-enabled wireless power transfer: Trajectory design and energy optimization,â IEEE Trans. Wirel. Commun., vol. 17, no. 8, pp. 5092â5106, Aug. 2018.

[5] Z. Wang and L. Duan, âChase or wait: Dynamic UAV deployment to learn and catch time-varying user activities,â IEEE Trans. Mobile Comput., vol. 22, no. 3, pp. 1369â1383, Mar. 2023.

[6] L. Xie, J. Xu, and R. Zhang, âThroughput maximization for UAV-enabled wireless powered communication networks,â IEEE Internet Things J., vol. 6, no. 2, pp. 1690â1703, Apr. 2019.

[7] O. S. Oubbati, M. Atiquzzaman, H. Lim, A. Rachedi, and A. Lakas, âSynchronizing UAV teams for timely data collection and energy transfer by deep reinforcement learning,â IEEE Trans. Veh. Technol, vol. 71, no. 6, pp. 6682â6697, Jun. 2022.

[8] L. Wang, Y. L. Che, J. Long, L. Duan, and K. Wu, âMultiple access mmWave design for UAV-aided 5G communications,â IEEE Wirel. Commun., vol. 26, no. 1, pp. 64â71, Feb. 2019.

[9] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[10] C. Zhan, Y. Zeng, and R. Zhang, âEnergy-efficient data collection in UAV enabled wireless sensor network,â IEEE Wireless Commun. Lett., vol. 7, no. 3, pp. 328â331, Jun. 2018.

[11] J. Liu, P. Tong, X. Wang, B. Bai, and H. Dai, âUAV-aided data collection for information freshness in wireless sensor networks,â IEEE Trans. Wireless Commun., vol. 20, no. 4, pp. 2368â2382, Apr. 2021.

[12] P. Tong, J. Liu, X. Wang, B. Bai, and H. Dai, âUAV-enabled age-optimal data collection in wireless sensor networks,â in Proc. IEEE Int. Conf. Commun. Workshops, 2019, pp. 1â6.

[13] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for multi-UAV enabled wireless networks,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2109â2121, Mar. 2018.

[14] S. S. Hassan, Y. M. Park, Y. K. Tun, W. Saad, Z. Han, and C. S. Hong, â3TO: THz-enabled throughput and trajectory optimization of UAVs in 6G networks by proximal policy optimization deep reinforcement learning,â in Proc. IEEE Int. Conf. Commun., 2022, pp. 5712â5718.

[15] G. Chen, X. B. Zhai, and C. Li, âJoint optimization of trajectory and user association via reinforcement learning for UAV-aided data collection in wireless networks,â IEEE Trans. Wireless Commun., vol. 22, no. 5, pp. 3128â3143, May 2023.

[16] Q. Wang, W. Zhang, Y. Liu, and Y. Liu, âMulti-UAV dynamic wireless networking with deep reinforcement learning,â IEEE Commun. Lett., vol. 23, no. 12, pp. 2243â2246, Dec. 2019.

[17] B. Clerckx, R. Zhang, R. Schober, D. W. K. Ng, D. I. Kim, and H. V. Poor, âFundamentals of wireless information and power transfer: From RF energy harvester models to signal and system designs,â IEEE J. Sel. Areas Commun., vol. 37, no. 1, pp. 4â33, Jan. 2019.

[18] J. Shi, P. Cong, L. Zhao, X. Wang, S. Wan, and M. Guizani, âA two-stage strategy for UAV-enabled wireless power transfer in unknown environments,â IEEE Trans. Mobile Comput., vol. 23, no. 2, pp. 1785â1802, Feb. 2024.

[19] H. Ren, Z. Zhang, Z. Peng, L. Li, and C. Pan, âEnergy minimization in RISassisted UAV-enabled wireless power transfer systems,â IEEE Internet Things J., vol. 10, no. 7, pp. 5794â5809, Apr. 2023.

[20] J. Baek, S. I. Han, and Y. Han, âOptimal UAV route in wireless charging sensor networks,â IEEE Internet Things J., vol. 7, no. 2, pp. 1327â1335, Feb. 2020.

[21] J. Mu and Z. Sun, âTrajectory design for multi-UAV-aided wireless power transfer toward future wireless systems,â Sensors, vol. 22, no. 18, 2022, Art. no. 6859.

[22] L. Xie, X. Cao, J. Xu, and R. Zhang, âUAV-enabled wireless power transfer: A tutorial overview,â IEEE Trans. Green Commun. Netw., vol. 5, no. 4, pp. 2042â2064, Dec. 2021.

[23] Z. Zhao, Y. Che, S. Luo, K. Wu, and V. Leung, âMulti-agent graph reinforcement learning based on-demand wireless energy transfer in multi-UAV-aided IoT network,â in Proc. 21st Int. Symp. Model. Optim. Mobile Ad Hoc Wirel. Netw., Singapore, 2023, pp. 1â8.

[24] L. Liu, K. Xiong, J. Cao, Y. Lu, P. Fan, and K. B. Letaief, âAverage AoI minimization in UAV-assisted data collection with RF wireless power transfer: A deep reinforcement learning scheme,â IEEE Internet Things J., vol. 9, no. 7, pp. 5216â5228, Apr. 2022.

[25] W. Luo, Y. Shen, B. Yang, S. Wang, and X. Guan, âJoint 3-D trajectory and resource optimization in multi-UAV-enabled IoT networks with wireless power transfer,â IEEE Internet Things J., vol. 8, no. 10, pp. 7833â7848, May 2021.

[26] Y. Che, Y. Lai, S. Luo, K. Wu, and L. Duan, âUAV-aided information and energy transmissions for cognitive and sustainable 5G networks,â IEEE Trans. Wireless Commun., vol. 20, no. 3, pp. 1668â1683, Mar. 2021.

[27] P. N. Alevizos and A. Bletsas, âSensitive and nonlinear far-field RF energy harvesting in wireless communications,â IEEE Trans. Wireless Commun., vol. 17, no. 6, pp. 3670â3685, Jun. 2018.

[28] PowerCast Module. Accessed. Jul., 2020. [Online]. Available: http://www. mouser.com/ds/2/329/P2110B-DatasheetRev-3-1091766.pdf

[29] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[30] Z. Dai et al., âAoI-minimal UAV crowdsensing by model-based graph convolutional reinforcement learning,â in Proc. IEEE Conf. Comput. Commun., 2022, pp. 1029â1038.

[31] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[32] H. Peng and X. Shen, âMulti-agent reinforcement learning based resource management in MEC and UAV-assisted vehicular networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 1, pp. 131â141, Jan. 2021.

[33] V. Mnih et al., âHuman-level control through deep reinforcement learning,â Nature, vol. 518, no. 7540, pp. 529â533, 2015.

[34] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, âSoft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,â in Proc. Int. Conf. Mach. Learn., PMLR, 2018, pp. 1861â1870.

[35] M. L. Puterman, Markov Decision Processes: Discrete Stochastic Dynamic Programming. Hoboken, NJ, USA: John Wiley & Sons, 2014.

[36] D. P. Kingma and J. Ba, âAdam: A method for stochastic optimization,â 2014, arXiv:1412.6980.

[37] A. Barto, âReinforcement learning: An introduction by Richardsâ Sutton,â SIAM Rev., vol. 63, no. 2, pp. 419â431, 2021.

<!-- image-->

Ze Yu Zhao received the BEng degree in computer science and technology from Jishou University, Hunan, China, in 2021, and the MEng degree in computer science and technology from Shenzhen University, Shenzhen, China, in 2024. He is currently working toward the PhD degree with the College of Computer Science and Software Engineering, Shenzhen University, China. His research interests include deep reinforcement learning, UAV-enabled mobile communications and wireless information and power transfer.

<!-- image-->

Yue Ling Che (Member, IEEE) received the BEng and MEng degrees in electrical engineering from the University of Electronic Science and Technology of China in 2006 and 2009, respectively, and the PhD degree in electrical engineering from the Nanyang Technological University, Singapore, in 2014. From 2014 to 2016, she was a postdoc research fellow in Engineering Systems and Design Pillar, Singapore University of Technology and Design. She is now an associate professor with the College of Computer Science and Software Engineering with the Shenzhen

University. Her research interests include energy-efficient wireless communication systems, AI-enabled wireless communications, UAV-enabled mobile communications, wireless information and power transfer, and stochastic modeling and optimization methods.

<!-- image-->

Sheng Luo (Member, IEEE) received the BEng and MEng degrees in communication engineering from the University of Electronic Science and Technology of China in 2009 and 2012, respectively, and the PhD degree in communication engineering from Nanyang Technological University, Singapore, in 2017. Since 2017, he has been with Shenzhen University, where he is currently an associate professor with the College of Computer Science and Software Engineering. He has published more than 40 papers in top international journals and international conferences, such as IEEE

Transactions on Wireless Communications, IEEE Transactions on Communication, etc. His current research interests are in the areas of wireless sensing, wireless information and power transfer, mmWave communication, and spatial modulation.

<!-- image-->

Gege Luo received the BEng degree in software engineering from Wuhan Textile University, Wuhan, China, in 2021, and the MEng degree in computer technology from Shenzhen University, Shenzhen, China, in 2024. She is currently working as a development engineer in Lenovo Shenzhen, China. Her research interests are in UAV-assisted communicationsensing integration.

<!-- image-->

Kaishun Wu (Fellow, IEEE) received the PhD degree from the Hong Kong University of Science and Technology, Hong Kong, in 2011. He is currently a professor in information hub of the Hong Kong University of Science and Technology (Guangzhou). His research interests include wireless communications and mobile computing. He won several best paper awards of international conferences, such as IEEE Globecom 2012 and IEEE MASS 2014.

<!-- image-->

Victor C. M. Leung (Life Fellow, IEEE) is the dean of the Artificial Intelligence Research Institute and a professor of Engineering with Shenzhen MSU-BIT University, China, a distinguished professor of computer science and software engineering with Shenzhen University, China, and an emeritus professor of electrical and computer engineering and director with the Laboratory for Wireless Networks and Mobile Systems, the University of British Columbia (UBC), Canada. His research is in the broad areas of wireless networks and mobile systems, and he has published

widely in these areas. His published works have together attracted more than 60,000 citations. He is named in the current Clarivate Analytics list of âHighly Cited Researchersâ. He is serving on the editorial boards of IEEE Transactions on Green Communications and Networking, IEEE Transactions on Computational Social Systems, and several other journals. He received the 1977 APEBC Gold Medal, 1977-1981 NSERC Postgraduate Scholarships, IEEE Vancouver Section Centennial Award, 2011 UBC Killam Research Prize, 2017 Canadian Award for Telecommunications Research, 2018 IEEE TCGCC Distinguished Technical Achievement Recognition Award, and 2018 ACM MSWiM Reginald Fessenden Award. He coauthored papers that were selected for the 2017 IEEE ComSoc Fred W. Ellersick Prize, 2017 IEEE Systems Journal Best Paper Award, 2018 IEEE CSIM Best Journal Paper Award, and 2019 IEEE TCGCC Best Journal Paper Award. He is a fellow of the Royal Society of Canada (Academy of Science), Canadian Academy of Engineering, and Engineering Institute of Canada.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_3_img_1.png|page_3_img_1]]
2. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_6_img_1.png|page_6_img_1]]
3. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_9_img_1.png|page_9_img_1]]
4. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_10_img_1.jpeg|page_10_img_1]]
5. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_10_img_2.jpeg|page_10_img_2]]
6. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_11_img_1.jpeg|page_11_img_1]]
7. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_11_img_2.jpeg|page_11_img_2]]
8. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_12_img_1.jpeg|page_12_img_1]]
9. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_12_img_2.jpeg|page_12_img_2]]
10. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_12_img_3.jpeg|page_12_img_3]]
11. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_13_img_1.jpeg|page_13_img_1]]
12. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_13_img_2.jpeg|page_13_img_2]]
13. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_13_img_3.jpeg|page_13_img_3]]
14. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_13_img_4.jpeg|page_13_img_4]]
15. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_14_img_1.jpeg|page_14_img_1]]
16. [[../extracted_images/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem/page_14_img_2.jpeg|page_14_img_2]]

---

