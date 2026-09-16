# Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling

Huansheng Xue , Honglong Chen , Senior Member, IEEE, Zhichen Ni , Xiaolong Liu and Feng Xia , Senior Member, IEEE

AbstractâIn recent years, wireless rechargeable sensor networks (WRSNs) have gained significant attention in the research community due to the current advancements in wireless power transfer technology. In mobile charger scheduling, previous works primarily emphasized the survival rate of sensor nodes. However, the primary task of a WRSN is to monitor targets in a given area. Therefore, the coverage of targets (CoT) maximization should be the primary objective of mobile charger scheduling. In this paper, we shift the focus to the CoT maximization on-demand charging scheduling problem, and formulate it as a multi-objective optimization problem, aiming to simultaneously enhance the average coverage and energy efficiency. We prove that the problem is NP-hard by reformulating it as a Multiple Travelling Salesman Problem with Deadline. We first propose the multiple chargers scheduling scheme for maximizing coverage of targets called Max-Cov, which is designed to optimize the charging scheduling process and improve network performance in terms of coverage. Then, we further propose the multiple chargers scheduling scheme based on requests grouping called MaxCov-RG, which can well balance the trade-off between the performance and computational complexity. Finally, we validate the effectiveness of the proposed schemes via extensive simulations.

Index TermsâCoverage of targets, multiple chargers scheduling, requests grouping, wireless rechargeable sensor networks.

## I. INTRODUCTION

E NERGY consumption is a critical concern for wirelesssensor networks (WSNs) due to their heavy dependence on sensor networks (WSNs) due to their heavy dependence on compact batteries for powering the sensor nodes [1]. In recent years, research on extending network lifetime has primarily focused on two categories: energy conservation and energy provisioning [2], [3], [4]. The emergence of wireless rechargeable sensor networks (WRSNs) has facilitated energy provisioning through wireless power transfer (WPT) [5], [6], [7]. A typical WRSN comprises static rechargeable sensor nodes, one or more mobile chargers (MCs), and one or more static base stations (BSs) that also serve as depots for the MCs. The MCs depart from the depot, traverse the network to recharge the sensor nodes, and return to the depot for recharging or maintenance tasks. This charging system enables continuous operation of WRSNs, which can be widely applied in sensor-based Internet of Things (IoT) for smart cities, smart agriculture, healthcare, military surveillance, and other various real-world scenarios. However, scheduling the MCs for energy replenishment of the sensor nodes is essential in WRSNs, which significantly impacts the network lifetime [8].

The mobile chargers scheduling in WRSNs is becoming more and more significant. Recent studies on scheduling techniques primarily focus on improving the survival rates of sensor nodes. The primary objective of these scheduling schemes is to ensure the successful completion of tasks by enhancing the coverage of targets (CoT) within the designated area. However, it is crucial to note that the primary task of WRSNs is to monitor specific events in the target area. Although increasing the survival rate of sensor nodes may contribute to improving the CoT of the WRSN to a certain extent, it may not be the optimal approach. Some works also concentrate on enhancing the CoT of WRSNs, but most of them overlook a critical factor: the impact of the dynamic network topology due to the frequent joining and leaving of sensor nodes [9], [10].

The applications of WRSNs span across various domains, which require a high CoT in an on-demand charging architecture, particularly with the recent advancement of the IoT [11], [12], [13]. In this paper, we address the problem of maximizing CoT through on-demand charging scheduling in WRSNs. We first analyze the limitations of traditional on-demand charging architectures and present a model for WRSNs that incorporates multiple mobile chargers and base stations. Then we formulate the problem as a multiple-objective optimization problem. After that, we propose two scheduling schemes: the multiple chargers scheduling scheme for maximizing coverage of targets (MaxCov) and the multiple chargers scheduling scheme based on requests grouping (MaxCov-RG).

The contributions of this paper are summarized as follows:

- We formulate the CoT maximization on-demand charging scheduling problem in WRSNs, which is proved to be NP-hard.

- We propose the multiple chargers scheduling scheme for maximizing coverage of targets called MaxCov, which assigns requests to each charger using the Requests Matching Algorithm.

- We further propose the multiple chargers scheduling scheme based on requests grouping called MaxCov-RG to well-balance the trade-off between the performance and computational complexity.

We conduct extensive simulations to validate the effectiveness of the proposed schemes, the results of which illustrate that the proposed MaxCov and MaxCov-RG schemes outperform the state of the art.

The remainder of the paper is organized as follows. Section II reviews related work. In Section III, we present the CoT maximization on-demand charging scheduling problem in WRSNs. In Section IV, we describe the MaxCov scheme in detail. In Section V, we propose the MaxCov-RG scheme. Then, we show the analyses of proposed schemes and the mathematical tools used in this paper in Section VI. Performance evaluations are given in Section VII. Section VIII concludes this paper.

## II. RELATED WORK

In this section, we mainly review related works on mobile chargers scheduling in WRSNs, including periodical charging schemes, on-demand charging schemes, coverage of targets maximization and multiple chargers scheduling.

## A. Periodical Charging

In the realm of wireless charging architecture, Xie et al. [8] proposed a novel approach that tackles the charging problem by leveraging energy distribution and consumption models, effectively transforming it into a variant of the renowned Traveling Salesman Problem (TSP). Within this framework, the MC traverses a predetermined path, strategically charging sensor nodes embedded in WRSN. Building upon these advancements, Liu et al. [14] introduced a partial charging mechanism tailored specifically for multi-node charging scenarios. However, due to the dynamic nature of network topology, discrepancies between the information held by MCs or the BS and the actual state of the network can arise. As a result, completing the charging process becomes challenging. Consequently, the periodical charging architecture fails to adapt to real-time changes and is impractical for many applications.

## B. On-Demand Charging

The on-demand charging architecture of WRSNs is constructed in [15]. To complete the charging, the charging action is usually performed by the sensor nodes in concert with MCs through messaging. In [16], the introduced charging scheduling algorithm, namely TSCA, is specifically designed for single MC charging scheduling. However, it is important to note that these algorithms were not developed for multiple MCs scheduling scenarios. Then, in [17], [18], Lin et al. researched multiple MCs charging scheduling in on-demand architecture. Kaswan et al. [19] proposed an on-demand scheme, called distributed mobile charging protocol (DMCP) that utilizes the benefits of partial charging. Liu et al. [20] proposed a charging algorithm based on reinforcement learning for mobile devices. However, the aforementioned works primarily focus on maximizing the node survival rate rather than the coverage of targets.

TABLE I  
SUMMARY OF MOBILE CHARGERS SCHEDULING SCHEMES
<table><tr><td rowspan=1 colspan=2>Paper</td><td rowspan=1 colspan=1>On-demand</td><td rowspan=1 colspan=1>Multiplechargers</td><td rowspan=1 colspan=1>Coverage oftargets</td><td rowspan=1 colspan=1>Multipleobjectives</td></tr><tr><td rowspan=1 colspan=2>[8]</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=2>[9]</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=2>[14]</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2>[15]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=2>[16]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2>[17]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2>[18]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=2>[19]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2>[25]</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2>Our</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr></table>

## C. Coverage of Targets

Sensor network performance evaluation often relies on the coverage of targets as a critical metric. In [9], [21], Zhou et al. proposed a charging algorithm named Î»-GTSP charging algorithm to determine the optimal number of sensors to be charged in each cluster to maintain k-coverage for targets in the network. However, Î»-GTSP is not to address charging scheduling in on-demand architecture. Xue et al. [22] proposed n-CSCT-R scheme to maximize the coverage of targets in ondemand charging architecture. However, it is worth mentioning that the n-CSCT-R scheme is not developed for multiple MCs scheduling scenarios.

## D. Multiple Chargers Scheduling

In [23], Lin et al. proposed cooperative scheduling based on game theory, in which mobile chargers engage in repeated games and find the next sensor to charge based on a Nash equilibrium. And, the proposed algorithm handles such charging conflicts between mobile chargers through an intelligent pre-charging mechanism. Chen et al. [24] proposed a multi-intelligence reinforcement learning framework to schedule multiple mobile chargers to maximize network lifetime and energy usage efficiency. In [17], Lin et al. first utilized the k-means algorithm to cluster the sensors and assigned a mobile charger to each cluster for energy replenishment. Tomar et al. [25] proposed an on-demand charging scheme that utilizes fuzzy logic for determining the charging schedule of the nodes by contemplating various network attributes. However, the above works neglected the CoT in WRSNS.

The comprehensive comparisons between the proposed schemes and the prevailing ones are delineated in Table I. In this paper, we propose MaxCov and MaxCov-RG schemes to maximize the CoT in the on-demand charging architecture of WRSNs.

<!-- image-->  
Fig. 1. CoT on-demand charging architecture in WRSNs.

## III. PROBLEM STATEMENT

In this section, we provide a comprehensive overview of the model for WRSNs with multiple chargers, in terms of sensor nodes, targets and mobile chargers. And, we formalize the CoT maximization on-demand charging scheduling problem in detail.

## A. Symbols and Definitions

We summarize the notations used in this paper in Table II.

## B. Network Model

We presume that a WRSN is set up to monitor a number of targets in a two-dimensional area. In this network, there are a lot of sensor nodes , several mobile chargers  and several base stations . Sensor nodes are placed throughout the twodimensional area to cover a specific number of targets T. Their tasks include monitoring the states of targets, gathering data, and sending data to base stations. MCs can travel around the area and provide energy for sensor nodes via wireless power transfer technology. Through MCs, base stations, which act as link nodes, supply power to the entire network.

First, we detail the on-demand charging architecture in WRSNs. As shown in Fig. 1, the batteries that power sensor nodes have a finite amount of capacity. One sensor node is classified as a weak node if its residual energy falls below the predetermined threshold. A node sends a charging request to the mobile chargers when it becomes weak. MCs will acknowledge receipt of the request and add it to a pool of requests. And, the request will be responded to by one of MCs, if it is eligible.

The typical on-demand charging architecture in WRSNs is as described above. Most of the current research on the on-demand charging scheduling issue aims to increase sensor node survival rates. Instead of concentrating on targets, they focus on maintaining sensor nodes. However, it is widely acknowledged that the primary duty is to monitor targets in the region. The ultimate objective should not be to maximize sensor node survival rates. We must put more effort into maximizing the CoT.

TABLE II SYMBOLS AND DEFINITIONS
<table><tr><td>Symbol</td><td>Definition</td></tr><tr><td>B</td><td>The set of base stations.</td></tr><tr><td> $\mathcal { M }$ </td><td>The set of mobile chargers.</td></tr><tr><td> $N$ </td><td>The set of sensor nodes.</td></tr><tr><td> $\mathcal { T }$ </td><td>The set of targets.</td></tr><tr><td> $S _ { N } ( i , t )$ </td><td>The state of sensor node i at time t.</td></tr><tr><td>0</td><td>The energy threshold for sensor nodes.</td></tr><tr><td> $E _ { N } ( i , t )$ </td><td>The residual energy of node  $N ( i )$  at time t.</td></tr><tr><td> $E _ { \mathcal { M } } ( \boldsymbol { u } , t )$ </td><td>The residual energy of mobile charger M(uï¼ at</td></tr><tr><td></td><td>time t.</td></tr><tr><td> $E _ { N } ^ { m i n }$ </td><td>The minimum residual energy of sensor nodes.</td></tr><tr><td> $r _ { N } ( i , t )$ </td><td>The energy consumption rate of sensor node N(i)</td></tr><tr><td></td><td>at time t.</td></tr><tr><td> $r _ { M } ^ { w p t }$ </td><td>The charging rate by mobile chargers.</td></tr><tr><td> $\dot { \xi } _ { N } ( i , \tau )$ </td><td>The charging status of sensor node  $N ( i )$  at time T.</td></tr><tr><td> $S _ { \mathcal { T } } ( j )$ </td><td>The state of target  $\mathcal { T } ( j )$ </td></tr><tr><td></td><td>The number of alive nodes covering target</td></tr><tr><td> $n _ { N } ( j , t )$ </td><td> $\mathcal { T } ( j )$  The set of sensor nodes that cover the target</td></tr><tr><td> $\varPhi _ { j }$ </td><td> $\mathcal { T } ( j )$ </td></tr><tr><td> $r _ { \mathcal { M } } ( u , t )$  wpt</td><td>The energy consumption rate of M(uï¼ at time t.</td></tr><tr><td> $r _ { \mathcal { B } S } ^ { \because \prime }$ </td><td>the rate that mobile chargers replenish energy by base stations.</td></tr><tr><td> $\xi _ { M } ( u , \tau )$ </td><td>The charging status of the M(u) at time T.</td></tr><tr><td> $\sigma$ </td><td>The average coverage.</td></tr><tr><td> $\eta$ </td><td>The energy efficiency.</td></tr><tr><td> $\varrho ( t )$ </td><td>The coverage rate at time t.</td></tr><tr><td> $\mathbb { E } _ { N } ^ { t o t a l }$ </td><td></td></tr><tr><td> $\mathbb { E } ^ { t o t a l }$ </td><td>The total energy consumed by sensor nodes.</td></tr><tr><td>M</td><td>The total energy consumed by mobile chargers.</td></tr><tr><td> $t _ { 0 }$ </td><td>The initial time.</td></tr><tr><td> $t _ { e }$ </td><td>The end time.</td></tr><tr><td> $t$ </td><td>The current time.</td></tr><tr><td> $R _ { r }$ </td><td>The set of real requests.</td></tr><tr><td> $R _ { p }$ </td><td>The set of predictive requests.</td></tr><tr><td> $R _ { d }$ </td><td>The set of dead node requests.</td></tr><tr><td> $R _ { s }$ </td><td>The set of supply requests.</td></tr><tr><td> $P _ { R }$ </td><td>The pool of requests.</td></tr><tr><td> $W \left( i , t \right)$ </td><td>The reward function that MC can receive after</td></tr><tr><td></td><td>completing a serving action.</td></tr><tr><td> $E _ { N } ^ { * } ( i , t )$ </td><td>The forecast residual energy. The travel cost that the</td></tr><tr><td> $T ( i , u , t )$ </td><td> $M ( u )$  move to sensor node N(i) at time t.</td></tr><tr><td> $d _ { N M } ( i , u , t )$ </td><td>The distance from sensor node N(i) to the mobile charger  $M ( u )$ </td></tr><tr><td> $d _ { m a x }$ </td><td>The maximum distance in this area.</td></tr><tr><td> $t _ { D } ( i )$ </td><td>The request deadline of sensor node  $N ( i ) .$ </td></tr><tr><td> $D ( i , t )$ </td><td>The time discount.</td></tr><tr><td> $t _ { n } ^ { m a x }$ </td><td>The latest deadline of requests in  $P _ { R } .$ </td></tr><tr><td></td><td>The risk-reward ratio.</td></tr><tr><td> $\overleftrightarrow { R } ( i , u , t )$   $\mathcal { A }$ </td><td>The action vector.</td></tr><tr><td> $\mathbb { A }$ </td><td>The set of all possible action vectors.</td></tr><tr><td> $\mathcal { \widetilde { A } }$ </td><td>The optimal action vector.</td></tr><tr><td> $C \left( u \right)$ </td><td></td></tr><tr><td></td><td>The charging cost of mobile charger  $M ( u )$ </td></tr><tr><td> $\widetilde { C } ( i - 1 , i )$ </td><td>The time cost.</td></tr><tr><td> $\Delta C ( u )$ </td><td>The variation of charging cost.</td></tr></table>

1) Sensor Nodes: We define $E _ { N } ( i , t )$ as the residual energy of node $N ( i )$ at time t, which can be expressed as

$$
E _ { N } ( i , t ) = E _ { N } ( i , t ^ { \prime } ) - \int _ { t ^ { \prime } } ^ { t } r _ { N } ( i , \tau ) d \tau + \int _ { t ^ { \prime } } ^ { t } \xi _ { N } ( i , \tau ) \cdot r _ { \mathcal { M } } ^ { w p t } d \tau ,\tag{1}
$$

where $t ^ { \prime }$ is the previous time, $r _ { N } ( i , \tau )$ refers to the energy consumption rate of sensor node $N ( i )$ at time $\tau , r _ { M } ^ { w p t }$ is the charging rate that mobile chargers transmit energy to sensor nodes by wireless power transfer technology and $\xi _ { N } ( i , \tau )$ refers to the charging status of sensor node $N ( i )$ at time Ï . If sensor node $N ( i )$ is being charged by a mobile charger at time t, $\xi _ { N } ( i , \tau ) = 1$ , otherwise, $\xi _ { N } ( i , \tau ) = 0$

We denote the state of node $N ( i )$ at time t by $S _ { N } ( i , t )$ , which is expressed as

$$
S _ { N } ( i , t ) = \left\{ \begin{array} { l l } { 1 , } & { E _ { N } ( i , t ) \geq { { E } _ { N } ^ { \mathrm { m i n } } } , } \\ { 0 , } & { { E _ { N } ( i , t ) } < { { E } _ { N } ^ { \mathrm { m i n } } } , } \end{array} \right.\tag{2}
$$

where $E _ { N } ^ { \mathrm { m i n } }$ denotes the minimum residual energy that makes sure sensor nodes work.

Sensor nodes have two states: alive and dead. When node $N ( i )$ runs normally, the state of $N ( i )$ is alive $( S _ { N } ( i , t ) = 1 )$ . If node $N ( i )$ becomes dead $( S _ { N } ( i , t ) = 0 )$ , it means that the residual energy of node $N ( i )$ can not make itself work normally. When the residual energy of node $N ( i )$ falls below the threshold Î¸, the node will be classified as a weak node and deliver a charging request to the MC. Note that a weak node is still an alive node.

2) Targets: In the initial state, every target is covered by h nodes. When the number of alive nodes covering the same target $\mathcal { T } ( j )$ is less than k $( k \le h )$ , this target is defined as a lost target. We define $S _ { \mathcal { T } } ( j )$ as the state of target $\mathcal { T } ( j )$ . One target has two states: active $( S _ { \mathcal { T } } ( j ) = 1 )$ and lost $( S _ { \mathcal { T } } ( j ) = 0 )$ , which is expressed as

$$
S _ { \mathcal { T } } ( j , t ) = \left\{ \begin{array} { l l } { 1 , } & { n _ { N } ( j , t ) \geq k , } \\ { 0 , } & { n _ { N } ( j , t ) < k , } \end{array} \right.\tag{3}
$$

where $n _ { N } ( j , t )$ is the number of alive nodes covering target $\mathcal { T } ( j )$ which can be calculated as follows:

$$
n _ { N } ( j , t ) = \sum _ { i \in \varPhi _ { j } } S _ { N } ( i , t ) .\tag{4}
$$

Here, $\varPhi _ { j }$ denotes the set of sensor nodes that cover the target $\mathcal { T } ( j )$

We try to maintain more targets in the CoT on-demand charging architecture, so the MC will first recharge the sensor node that is a part of the target covered by fewer live nodes. For example, the MC will recharge sensor nodes following the new path rather than the original path in Fig. 1.

3) Mobile Chargers: We define $E _ { M } ( u , t )$ as the residual energy of mobile charger $M ( u )$ at time t, which can be expressed as

$$
\begin{array} { r l r } {  { E _ { \mathcal { M } } ( u , t ) = E _ { \mathcal { M } } ( u , t ^ { \prime } ) - \int _ { t ^ { \prime } } ^ { t } \boldsymbol { r } _ { \mathcal { M } } ( u , \tau ) d \tau } } \\ & { } & { + \int _ { t ^ { \prime } } ^ { t } \xi _ { \mathcal { M } } ( u , \tau ) \cdot \boldsymbol { r } _ { \mathcal { B } S } ^ { w p t } d \tau , ~ } \end{array}\tag{5}
$$

where $r _ { M } ( u , \tau )$ refers to the energy consumption rate of $M ( u )$ at time $\tau , r _ { \mathcal { B } S } ^ { w p t }$ is the rate that mobile chargers replenish energy by base stations and $\xi _ { M } ( u , \tau )$ refers to the charging status of the $M ( u )$ at time Ï .

Mobile chargers have three states: sleeping $( s _ { s } )$ , moving $( s _ { m } )$ and charging $( s _ { c } )$ . When a mobile charger is in different states, its energy consumption rate $r _ { M } ( \boldsymbol { u } , t )$ is different. $r _ { M } ( \boldsymbol { u } , t )$ is defined as the energy consumption rate of $M ( u )$ at time t, which

can be expressed as

$$
\begin{array} { r } { r _ { \mathcal { M } } ( u , t ) = \left\{ \begin{array} { l l } { r _ { \mathcal { M } } ^ { s l p } ( u ) , } & { s ( u ) = s _ { s } , } \\ { r _ { \mathcal { M } } ^ { s l p } ( u ) + r _ { \mathcal { M } } ^ { m o v e } ( u ) , } & { s ( u ) = s _ { m } , } \\ { r _ { \mathcal { M } } ^ { s l p } ( u ) + r _ { \mathcal { M } } ^ { w p t } ( u ) , } & { s ( u ) = s _ { c } , } \end{array} \right. } \end{array}\tag{6}
$$

where $r _ { \mathcal { M } } ^ { s l p } ( u ) , r _ { \mathcal { M } } ^ { m o v e } ( u )$ and $r _ { \mathcal { M } } ^ { w p t } ( u )$ refer to the energy consumption rate that mobile chargers spend energy on on-board computer, movement and wireless power transfer respectively. And, s(u) represents the state of $M ( u )$

## C. Problem Formulation

In the CoT on-demand charging architecture, we define Ï as the average coverage, which is calculated using (7). It is evident that Ï serves as a crucial indicator that represents the CoT. One of the primary objectives of the problem is to maximize the average coverage Ï. Additionally, energy efficiency Î· is another important indicator in this problem. We consider that only the energy consumed by the sensor nodes is directly beneficial since they are responsible for completing monitoring missions. The energy consumed by the MC during its movement is not directly helpful in accomplishing monitoring missions. Therefore, our goal is to increase the proportion of energy consumed by the sensor nodes in the total energy consumption, ultimately maximizing the energy efficiency Î·.

In summary, the objectives of the problem are to simultaneously maximize the average coverage Ï and the energy efficiency $\eta .$ Therefore, the problem can be formalized as P1 as presented below:

$$
\mathbf { P 1 } : \quad \left\{ \begin{array} { l l } { \operatorname* { m a x } } & { \sigma = \frac { \int _ { t _ { 0 } } ^ { t _ { e } } \varrho ( \tau ) d \tau } { t _ { e } - t _ { 0 } } , } \\ { \operatorname* { m a x } } & { \eta = \frac { \mathbb { E } _ { N } ^ { t _ { o } } t a l } { \mathbb { E } _ { N } ^ { t _ { o } } t a l } , } \end{array} \right.\tag{7}
$$

$$
\begin{array} { r } { \int \varrho ( t ) = \frac { n _ { T } ( t ) } { | T | } , } \end{array}\tag{8}
$$

$$
\begin{array} { r } { \mid n _ { \mathcal { T } } ( t ) = \dot { \sum } _ { j = 1 } ^ { | \mathcal { T } | } S _ { \mathcal { T } } ( j , t ) , } \end{array}\tag{9}
$$

(10)

(11)

$$
\begin{array} { r } { \left\lfloor \mathbb { E } _ { M } ^ { t o t a l } = \sum _ { u = 1 } ^ { | M | } \int _ { t _ { 0 } } ^ { \bar { t } _ { e } } r _ { { M } } ( u , \tau ) d \tau , \right. } \end{array}\tag{12}
$$

where $\varrho ( t )$ is defined as the coverage rate at time $t , n _ { \mathcal { T } } ( t )$ refers to the number of active targets at time $t . \mathbb { E } _ { N } ^ { t o t a l }$ and $\mathbb { E } _ { M } ^ { t o t a l }$ denote the total energy consumed by sensor nodes and mobile chargers. $t _ { 0 }$ and $t _ { e }$ refer to the initial time and end time. The constraint (9) represents the coverage rate as the ratio of the number of active targets to the total number of targets. And, the number of active targets can be calculated by summing the states of each target according to (10). In addition, (9) and (9) depict the total energy consumed by all sensor nodes and all mobile chargers from the initial time to end time respectively.

## IV. THE PROPOSED MAXCOV SCHEME

In this section, the multiple chargers scheduling scheme for maximizing coverage of targets called MaxCov is proposed in detail. First, we present the overview of MaxCov scheme. Then, we explain pool of requests constructing algorithm and requests matching algorithm in detail.

<!-- image-->  
Fig. 2. Process schematic for MaxCov scheme.

<!-- image-->  
Fig. 3. Example of MaxCov scheme.

## A. Overview of MaxCov

In this paper, we take multiple mobile chargers to collaborate for charging the entire network rather than divide the network into multiple subdomains. We proved the superiority of this way in Section VI. Just as Theorem 2, we use an $M / M / n$ queueing model to design our schemes in this paper. In addition, we prove that the problem P1 is NP-hard. So finding a global optimal solution is difficult. A greedy solution is obtained in this scheme. The process of MaxCov scheme details as follows:

- Pool of Requests Constructing: The pool of requests will be constructed according to Algorithm 1, which deals with heterogeneous requests in WRSNs.

Requests Matching: Every mobile charger selects one request from the pool of requests according to Algorithm 2.

- Nodes Recharging: Each mobile charger fulfills its own requests and then repeats the requests matching.

Fig. 2 shows the process of MaxCov scheme. An example of MaxCov scheme is shown in Fig. 3. There are requests (a to e) in the pool of requests. These requests are waiting for a response from mobile chargers. Then, every mobile charger selects one request from the pool of requests using the Requests Matching Algorithm.

## B. Pool of Requests

According to the on-demand charging architecture, sensor node $N ( i )$ sends a charging request to MCs for energy replenishment when the residual energy $E _ { N } ( i , t )$ of node $N ( i )$ falls below the threshold. The charge request is stored in the pool of requests and awaits further processing after being received by MC. Therefore, we define $P _ { R }$ as the pool of requests to store charging requests which include the above real requests sent by sensor nodes.

Since sensor nodes in WRSNs are not fixed, they must include their own information in the charging requests that they send. The format of the request message is $\{ I D , x , y , t _ { s } , r _ { N } , I D _ { \mathcal { T } } , C _ { R } \}$ . Here, $I D$ represents the unique identification number of the node. x and y denote its location coordinates. $t _ { s }$ refers to the time when the request is sent. $r _ { N }$ is the rate of energy consumption of the node. $I D _ { \mathcal { T } }$ represents the identification number of the target that is covered by this node. And $C _ { R }$ is used to indicate the type of this request.

In the pool of requests $P _ { R }$ , there are three other types of requests except real requests mentioned above. These different types of requests are described in detail as follows.

1) Real Requests $R _ { r } .$ : When the residual energy $E _ { N } ( i , t )$ of node $N ( i )$ falls below the threshold, sensor node $N ( i )$ will deliver a charging request, which is called the real request. The majority of requests in the system are real requests, and they typically have higher priorities. The ideal situation is for MCs to fulfill all real requests, which guarantees that no target will be lost. However, sometimes MCs are too busy to fulfill every real request. They must choose requests which are more important and serve as many requests as possible. The set of real requests is denoted by $R _ { r }$

2) Predictive Requests $R _ { p } \mathrm { : }$ The pool can be empty if there are not any charging requests for a while because charging requests are distributed at random. The energy forecast model is made to address this issue. When node $N ( i )$ sends a charging request, the $r _ { N } ( i , t ^ { * } )$ in the request will be recorded in order to forecast the residual energy of $N ( i )$ . The energy forecast model will estimate the forecast residual energy $E _ { N } ^ { * } ( i , t )$ of each node by the $r _ { N } ( i , t ^ { * } )$ in their last request

$$
E _ { N } ^ { * } ( i , t ) = E _ { N } ( i , t ^ { * } ) - \int _ { t ^ { * } } ^ { t } r _ { N } ( i , t ^ { * } ) d \tau + \int _ { t ^ { * } } ^ { t } \xi _ { N } ( i , \tau ) \cdot r _ { \cal M } ^ { w p t } d \tau ,\tag{13}
$$

where $t ^ { * }$ refers to the moment at which the sensor node sent the last charging request. When $E _ { N } ^ { * } ( i , t )$ falls below the forecast threshold $\theta ^ { * }$ , node $N ( i )$ will be assumed that it sent a predictive request with a lower priority in accordance with the energy forecast model. Predictive requests would be also recorded in the pool of requests $P _ { R }$ and the set of predictive requests is denoted by $R _ { p }$

3) Dead Node Requests $R _ { d } .$ : The charging requests are stochastic, so an MC experiences busy and unoccupied periods. During busy periods, MCs can be too busy to fulfill every charging request, which results in some dead nodes. The free strategy is suggested in the CSCT scheme to make better use of unoccupied periods [22]. Similarly, during unoccupied times, the MC can revive dead nodes. Therefore, we assume that dead nodes also have charging requests with the lowest priority, which are called dead node requests. $R _ { d }$ d refers to the set of dead node requests.

4) Supply Requests $R _ { s } \mathrm { : }$ After a series of movements and charging nodes, the MC inevitably needs to return to the BS and refuel to maintain its serviceability due to the energy limitation. In [17], Lin et al. proposed a temporal- and spatial-collaborative charging scheme with multiple vehicles, called mTS. In mTS, MC will check its residual energy before it goes to complete the action in the current loop. If the residual energy of MC is enough to recharge the sensor node and return to BS, the MC moves to the node selected above; otherwise, it directly returns to BS for supply. However, the action for supply can also be regarded as a charging request. Treating the supply as a request has two advantages: one is that MCs can return to the BS in unoccupied periods for supply; the other is that MCs will always be powered. We define $R _ { s }$ as the set of supply requests.

## C. Priorities of Requests

In this scheme, MCs respond to the pool of requests $P _ { R }$ . When there are still requests in $P _ { R } ,$ , the MCs fulfill each one at a time. In a perfect world, the MC would fulfill every request, guaranteeing that no target would be missed. If the MC is unable to fulfill all requests, it should prioritize the most important ones and fulfill as many as it can. We define $W ( i , t )$ as the reward function that MC can receive after completing a serving action in order to differentiate the importance of each request

$$
W ( i , t ) = \left\{ \begin{array} { l l } { a ^ { - ( h ^ { * } - n _ { N } ( j , t ) ) } , } & { i \in R _ { r } , } \\ { a ^ { - 1 } \cdot b , } & { i \in R _ { p } , } \\ { a ^ { - ( h ^ { * } - n _ { N } ( j , t ) ) } \cdot c ^ { S _ { N } ( i ) } , } & { i \in R _ { d } , } \\ { W _ { s } ( i , t ) , } & { i \in R _ { s } , } \end{array} \right.\tag{14}
$$

where a, b and c are adjustable parameters, $a , b , c \in ( 0 , 1 ]$ Suppose node $N ( i )$ , which sends the request i, covers the target $\mathcal { T } ( j )$ , the smaller $n _ { N } ( j , t )$ is, the larger the value of $W ( i , t )$ is. It means that the request i has a higher priority to be served if the target $\mathcal { T } ( j )$ covered by node $N ( i )$ has fewer alive nodes. The differentiation among different priorities is controlled by a. If parameter a is set to 1, all requests will have the same priority, and it means that the CoT will not be focused on. Therefore, conventional architecture is a special case of the architecture proposed in this paper. In addition, $W _ { s } ( i , t )$ refers to the reward function of supply requests, which can be calculated as

$$
W _ { s } ( i , t ) = \left\{ { a } ^ { - 1 } \cdot \boldsymbol { b } \cdot \boldsymbol { c } , \quad E _ { M } ( u , t ) \geq E _ { M } ^ { l } , \right.\tag{15}
$$

where $E _ { \mathcal { M } } ^ { l }$ is defined as the minimum amount of energy required to accomplish the task and successfully return to base stations [22].

We think that a request should be assigned to the MC that is closer to the node that sent the request in order to decrease the distance MCs have to travel and increase their efficiency. Therefore, $T ( i , u , t )$ is defined as the travel cost that the $M ( u )$ move to sensor node $N ( i )$ at time t, which is expressed as

$$
T ( i , u , t ) = \frac { d _ { N M } ( i , u , t ) } { d _ { \operatorname* { m a x } } } ,\tag{16}
$$

where $d _ { N M } ( i , u , t )$ refers to the distance from sensor node $N ( i )$ to the mobile charger $\mathcal { M } ( u ) , d _ { \mathrm { m a x } }$ is the maximum distance in this area.

Each request has a deadline $t _ { D } ( i )$ . Mobile chargers need to fulfill the request before its deadline or the request will expire. $D ( i , t )$ is defined as the time discount to determine how urgent

```perl
Algorithm 1: Pool of Requests Constructing Algorithm.
Input: Real requests $\overline { { R _ { r } } }$
Output: Pool of requests $P _ { R }$
1: for $i \gets 1$ to | | do
2: if $S _ { N } ( i , t ) = 0$ then
3: Record this dead node request in $R _ { d } ;$
4: $t _ { d } ( i ) \gets + \infty ;$
5: for $i \gets 1$ to | | do
6: Calculate $E _ { N } ^ { * } ( i , t )$ by (13);
7: if $E _ { N } ^ { * } ( i , t ) < \theta ^ { * }$ and the request of N(i) â/ $R _ { r } \cup R _ { d }$
then
8: Record this predictive request in $R _ { p } ;$
9: Generate supply requests $R _ { s }$
10: $P _ { R } \gets R _ { r } \cup R _ { p } \cup R _ { d } \cup R _ { s } ;$
```

Algorithm 2: Requests Matching Algorithm.   
Input: Pool of requests $P _ { R } .$   
Output: Optimal action vector ${ \mathcal { \widetilde { A } } } .$   
1: for i â 1 to $| P _ { R } |$ do   
2: Calculate the reward function $W ( i , t )$ by (14) and   
the time discount $D ( i , t )$ by (17);   
3: for u â 1 to | | do   
4: Calculate the travel cost $T ( i , u , t )$ by (16);   
5: Calculate the risk-reward ratio $R ( i , u , t )$ by (18);   
6: Find the optimal action vector $\mathcal { \widetilde { A } }$ from all possible   
action vectors A by (20);

the request is, which can be calculated as

$$
D ( i , t ) = \frac { t _ { D } ( i ) - t } { t _ { D } ^ { \operatorname* { m a x } } - t } ,\tag{17}
$$

where $t _ { D } ^ { \mathrm { m a x } }$ is the latest deadline of requests in $P _ { R }$

## D. Requests Matching Algorithm

In this subsection, the requests matching algorithm is proposed to assign a charging request to each MC. First, we define $R ( i , u , t )$ as the risk-reward ratio that the $M ( u )$ fulfills the request i, which can be expressed as

$$
R ( i , u , t ) = \frac { W ( i , t ) } { T ( i , u , t ) \cdot D ( i , t ) } .\tag{18}
$$

Therefore, for each request in $P _ { R } .$ every MC has a risk-reward ratio $R ( i , u , t )$

To represent the matching relationship between the charging requests and the MCs,  is defined as the action vector that stores one combination of requests and MCs. The representation of is as follows:

$$
\begin{array} { r } { \mathcal { \mathcal { A } } = \left( \begin{array} { l l } { i _ { 1 } } & { u _ { 1 } } \\ { i _ { 2 } } & { u _ { 2 } } \\ { \vdots } & { \vdots } \\ { i _ { x } } & { u _ { x } } \end{array} \right) , } \end{array}\tag{19}
$$

where $i _ { x }$ refers to the request matched with the MC $u _ { x }$ , and $x \leq | M |$

<!-- image-->  
Fig. 4. Process schematic for MaxCov-RG scheme.

In the process of requests matching, all possible action vectors will be searched, until the optimal action vector  is found. A is defined as the set of all possible action vectors. The optimal action vector $\widetilde { \mathcal { A } }$ refers to the action vector that makes the maximum sum of $R ( i , u , t )$

$$
\operatorname* { m a x } \sum _ { \mathcal { A } \in \mathbb { A } } R ( i , u , t ) .\tag{20}
$$

Algorithm 2 provides a detailed description for the process of requests matching. Initially, it computes the reward and time discount associated with each request. Subsequently, it determines the risk-reward ratio of each request for various mobile chargers by considering the cost of movement as a factor. Lastly, it derives the optimal action vector by utilizing (20).

## V. THE PROPOSED MAXCOV-RG SCHEME

In this section, we propose the multiple chargers scheduling scheme based on requests grouping called MaxCov-RG to wellbalance the trade-off between the performance and computational complexity. To avoid the high computational complexity, we propose the n-path algorithm to find the solution and the requests grouping algorithm to divide charging requests into groups.

## A. Overview of MaxCov-RG

In this scheme, all requests from the pool of requests will be divided into | | groups for mobile chargers. And, the requests in each group will be arranged in a specific order. Then, every mobile charger fulfills the requests in its own group in order. The Process of MaxCov-RG scheme is shown in Fig. 4. The following is a description of how the scheme works in detail:

- Pool of Requests Constructing: The pool of requests will be constructed according to Algorithm 1.

Requests Grouping: All requests from the pool of requests will be divided into | | groups according to Algorithm 3, if there is any new request in the pool of requests.

- Nodes Recharging: Each mobile charger fulfills requests in its own group in order.

In addition, the requests grouping is dynamic, it will be repeated when there is a new request in the pool. An example of the MaxCov-RG scheme is shown in Fig. 5. Suppose that there have been requests (a to g) in the pool of requests at time t. In the MaxCov-RG scheme, every request in the pool of requests should be allocated into a group. So, requests (a to g) have been divided into their groups (A, B and C), but they are still waiting to be served. Now, there is a new request h in the pool. The new request h will be allocated into a proper group by the Requests Grouping Algorithm.

<!-- image-->  
Fig. 5. Example of MaxCov-RG scheme.

## B. Requests Grouping Based on Cooperative Game

Cooperative game theory is an applied mathematics theory that models and analyzes systems. In order to succeed, each player must determine the best course of action based on the decisions of the other players. Pareto optimality is frequently used in game theory to optimize resource allocation and constrain player behavior. When a system reaches the Pareto state, its overall profit is maximized.

In our scheme, each mobile charger is regarded as a player involved in the game. Their common objective is to minimize the total charging cost. Every mobile charger has a charging cost, C(u), which can be calculated by

$$
C ( u ) = \sum _ { i \in H ( j ) } \widetilde { C } ( i - 1 , i ) ,\tag{21}
$$

where $H ( j )$ denotes a possible path j for the MC to recharge sensor nodes, $\widetilde { C } ( i - 1 , i )$ refers to the time cost.

Algorithm 3 shows the requests grouping algorithm. When there is any new request in the pool of requests, the requests grouping algorithm will begin to work.

In this algorithm, for each new request, every mobile charger will give a variation of charging cost $\Delta C ( u )$ according to (22), and the one which gives the minimum charging cost will obtain the request.

$$
\Delta C ( u ) = C ^ { + } ( u ) - C ^ { - } ( u ) .\tag{22}
$$

Finally, all requests from the pool of requests will be divided into | | groups according to Algorithm 3.

## C. n-Path Algorithm

The process of serving a request by the MC can be divided into two distinct steps: moving to the sensor node and charging it. As long as the MC reaches the node before the deadline, the node will not run out of energy. Consequently, the MC can obtain the reward when it reaches the node on time. However, it is important to note that the MC incurs a time cost in order to obtain this reward. We define $\widetilde { C } ( i - 1 , i )$ as the time cost from location S(i â 1) to S(i). Here, S(i â 1) and S(i) can represent the locations of various devices such as nodes, the MC, and the base station (BS). The time cost from $S ( i - 1 )$ to $S ( i )$ encompasses both the time spent at $S ( i - 1 )$ and the time required to move from $S ( i - 1 )$ to S(i). In other words, this period begins upon arrival at $S ( i - 1 )$ and concludes upon arrival at $S ( i ) . \widetilde { C } ( i - 1 , i )$ can be calculated as

Algorithm 3: Requests Grouping Algorithm. Algorithm 4: n-Path Algorithm.   
Input: Pool of requests $P _ { R } ,$ previous grouping vector ${ \mathcal { G } } ^ { - } .$ Input: $\mathcal { G } ^ { - } ( u )$ , the new request.   
Output: New grouping vector $g ^ { + }$ Output: The best n-path, charging cost $C ( u )$   
1: $\mathcal { G } ^ { + }  \mathcal { G } ^ { - } ;$ 1: Construct P by $\mathcal { G } ^ { - } ( u )$ and the new request;   
2: $C _ { f } \gets + \infty ;$ 2: for $i \gets 1$ to $| { \mathcal P } |$ do   
3: for $i \gets 1$ to $| P _ { R } |$ do 3: $\widetilde { C } ( i - 1 , i ) \gets t _ { s t a y } ( i - 1 ) + t _ { m o v e } ( i - 1 , i ) ;$   
4: for u â 1 to |M| do 4: for all possible n-paths do   
5: Call Algorithm 4 for the best n-path and charging 5: for $i \gets 1$ to n do   
cost $C ( u ) ;$ 6: i $\begin{array} { r } { : \sum _ { l = 1 } ^ { i } \widetilde { C } ( l - 1 , l ) < t _ { d } ( i ) - t } \end{array}$ then   
6: if $\Delta C ( u ) < C _ { f }$ then 7: $\begin{array} { r } { \mathbf { i f } \mathcal { W } < \sum _ { l = 1 } ^ { i } W ( l ) } \end{array}$ then   
7: $\begin{array} { r } { \mathcal { G } ^ { + } ( u , : )  \bar { \mathcal { G } } ^ { - } ( u , : ) \cup P _ { R } ( i ) ; } \end{array}$ 8: $\textstyle { \mathcal { W } } \gets \sum _ { l = 1 } ^ { i } W ( l ) ;$   
8: $C _ { f } \gets \Delta C ( u ) ;$ 9: Record this path as the best n-path and record   
this charging cost $C ( u ) ;$ ;

$$
\widetilde { C } ( i - 1 , i ) = t _ { s t a y } ( i - 1 ) + t _ { m o v e } ( i - 1 , i ) ,\tag{23}
$$

where $t _ { s t a y } ( i - 1 )$ and $t _ { m o v e } ( i - 1 , i )$ denote the time length of staying at $S ( i - 1 )$ and the time length of moving from $S ( i - 1 )$ to S(i).

In order to obtain rewards, it is necessary for the MC to reach location $S ( i )$ before the respective deadline. This timing constraint can be described by (24). Specifically, the MC will receive the reward $W ( i , t )$ if the sum of the time costs from request 1 to request i is smaller than the deadline for request i.

$$
\sum _ { l = 1 } ^ { i } \widetilde { C } ( i - 1 , i ) < t _ { d } ( i ) - t .\tag{24}
$$

Algorithm 4 shows the n-path algorithm, it searches all possible paths to find the best path, which maximizes rewards got by the MC and minimizes the time cost,

$$
\left\{ \begin{array} { l l } { \operatorname* { m a x } } & { \sum _ { i \in H ( j ) } W ( i , t ) , } \\ { \operatorname* { m i n } } & { \sum _ { i \in H ( j ) } \widetilde { C } ( i - 1 , i ) , } \end{array} \right.\tag{25}
$$

(26)

where $H ( j )$ denotes a possible path j for the MC to recharge sensor nodes.

## VI. THEORETICAL ANALYSIS

In this section, we present the analysis of the proposed schemes and demonstrate the mathematical tools employed in this paper. These include problem analysis utilizing graph theory and scheme analysis using queueing theory.

Theorem 1: The problem P1 is NP-hard.

Proof: Let $G = ( V , E )$ represent a weighted graph, where V denotes the set of sensor nodes that send charging requests and E represents the set of edges connecting these sensor nodes. The graph has a designated start node r, a reward function $\mathcal { W } : V $ $\mathbb { Z } ^ { + }$ , a deadline function $\mathcal { D } : V \to \mathbb { Z } ^ { + }$ , a release date function $\mathcal { R } : V \to \mathbb { Z } ^ { + }$ , and a length function $\mathcal { L } : E \to \mathbb { Z } ^ { + }$ . The reward function assigns priorities to the requests, while the deadline function  and the release date function  specify the deadlines and start times of the requests in $P _ { R }$ . The length function represents the distances between sensor nodes. In this context, it can be observed that the Multiple Travelling Salesman Problem with Deadline (Deadline-MTSP) is a reduction of problem P1.

As it is widely recognized, the Deadline-TSP problem has been proven to be NP-hard [26]. Similarly, the Deadline-MTSP problem is also NP-hard, as it encompasses the Deadline-TSP problem as a special case when $| \mathcal { M } | = 1$ . Finally, we established the NP-hardness of problem P1. -

In this subsection, we adopt the queueing theory to further analyze Problem P1. As the sensor nodes are deployed throughout the network, we assume that charging request arrivals follow the Poisson process with the arrival rate Î» [16]. Each MC can be considered as a service window in the queueing model, the service time of which follows an exponential distribution with service rate $\mu .$ Therefore, the WRSN with one MC can be regarded as an M/M/1 queueing model.

1) $M / M / 1$ Queueing Model: In terms of charging requests sent by sensor nodes, the arrival rate of charging requests can be calculated as

$$
\lambda = \frac { r _ { N } } { ( 1 - \theta ) C _ { N } } \cdot | N | .\tag{27}
$$

And, we define b as the state of the queueing system. The value of b is equal to the number of charging requests in the system. Then, we calculate the steady-state probability of the system in each state, which is denoted by $P _ { b }$ . State 0 can only be converted to state 1, because state b does not allow for any negative values. According to the principle of rate equality, (28) can be obtained. We can also describe other states except state 0 by (29).

$$
\lambda \cdot P _ { 0 } = \mu \cdot P _ { 1 } .\tag{28}
$$

$$
( \lambda + \mu ) \cdot P _ { 0 } = \lambda \cdot P _ { b - 1 } + \mu \cdot P _ { b + 1 } .\tag{29}
$$

Then, $P _ { b }$ can be calculated according to (28) and (29), which is expressed as follows:

$$
P _ { b } = \left( { \frac { \lambda } { \mu } } \right) ^ { b } \cdot P _ { 0 } .\tag{30}
$$

Since the sum of $P _ { b }$ is equal to 1, (31) is obtained,

$$
\sum _ { b = 0 } ^ { \infty } P _ { b } = \sum _ { b = 0 } ^ { \infty } \left( { \frac { \lambda } { \mu } } \right) ^ { b } \cdot P _ { 0 } = { \frac { P _ { 0 } } { 1 - { \frac { \lambda } { \mu } } } } = 1 .\tag{31}
$$

Then, we get the value of $P _ { 0 } ,$ , which is expressed as follows:

$$
P _ { 0 } = 1 - \frac { \lambda } { \mu } .\tag{32}
$$

Finally, we get the average number of requests in the system, which is denoted by L

$$
L = \sum _ { b = 0 } ^ { \infty } b \cdot P _ { b } = { \frac { \lambda } { \mu - \lambda } } = { \frac { \rho } { 1 - \rho } } ,\tag{33}
$$

where $\begin{array} { r } { \rho = \frac { \lambda } { \mu } } \end{array}$

Therefore, a WRSN with multiple MCs can be simply regarded as a system with n $M / M / 1$ queueing models. However, it can also be regarded as an $M / M /  \eta$ n queueing model.

2) $M / M / n$ Queueing Model: Similar to the $M / M / 1$ queueing model, we can get the average number of requests in the $M / M / n$ queueing model

$$
\widetilde L = \frac { n \cdot \rho - n \cdot \rho ^ { 2 } + \rho \cdot C ( n , \rho ) } { 1 - \rho } ,\tag{34}
$$

where $C ( n , \rho )$ is Erlang-C formula.

Comparing the average number of requests in an $M / M / n$ queueing model and a system with $c M / M / 1$ queueing models, we can conclude as follows.

Theorem 2: In WRSNs, the performance of an $M / M / n$ queueing model is superior to that of a system consisting of n $M / M / 1$ queueing models.

Proof: We define $\widehat { L }$ as the average number of requests in a system with n $M / M / 1$ queueing models, which is calculated by

$$
{ \widehat { L } } = n \cdot L = { \frac { n \cdot \rho } { 1 - \rho } } .\tag{35}
$$

Then, we compare $\widehat { L }$ and $\widetilde { L }$ . When $n = 1 , C ( n , \rho ) = \rho ,$ these two systems are equal. When $n > 1$ , according to the Erlang-C formula, we can get $\widehat { L } > \widetilde { L }$ . Therefore, the average number of requests in the system with n $M / M / 1$ queueing models is larger than the $M / M / n$ queueing model. It indicates that the performance of an $M / M / n$ queueing model is superior to that of a system with n $M / M / 1$ queueing models for WRSNs. -

## VII. PERFORMANCE EVALUATION

In this section, we present simulation results that illustrate the performance of MaxCov scheme and MaxCov-RG scheme. First, we introduce the simulation configuration and baseline schemes. Afterward, performance comparison between Max-Cov, MaxCov-RG and baseline schemes is explained in detail. In addition, we compare the performance of the above schemes with different network scales and the varying number of base stations.

TABLE III  
PARAMETERS OF SIMULATION
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Network size  $( m ^ { 2 } )$ </td><td>1000 Ã1000</td></tr><tr><td>Number of nodes</td><td>80</td></tr><tr><td>Number of targets</td><td>20</td></tr><tr><td>Energy consumption rate of node (mW)</td><td>[10,20]</td></tr><tr><td>Energy capacity of each node (J)</td><td>100</td></tr><tr><td>Energy threshold for node</td><td>20%</td></tr><tr><td>Velocity of MC (m/s)</td><td>2</td></tr><tr><td>Moving consumption rate of MC (mW)</td><td>2500</td></tr><tr><td>Charging consumption rate of MC (mW)</td><td>15000</td></tr></table>

## A. Simulation Configuration

We conducted simulations using the parameter settings outlined in Table III. In our simulations, we considered a twodimensional area measuring 1000 m Ã 1000 m, with 80 sensor nodes and 20 targets randomly dispersed throughout the area. Each target was ensured to be covered by at least 4 sensor nodes. The energy consumption rate of each sensor node was randomly selected from the range of [10 mW, 20 mW]. Additionally, each sensor node had an energy capacity of 100J. To determine when a sensor node should send a charging request to the MC, we set a threshold of 20 percent residual energy. Once the energy level of a sensor node dropped below this threshold, it would send a charging request to the MC. The MC had a velocity of 2 m/s.

## B. Baseline Setup

In the on-demand charging architecture of WRSNs, there is currently no existing scheme specifically designed to maximize CoT. Therefore, for comparison purposes, we select n-CSCT-R [22] and mTS [17] as baseline schemes. The mTS algorithm is a temporal-spatial charging scheduling algorithm developed for the on-demand charging architecture in WRSNs. Its objective is to minimize the number of dead nodes while maximizing energy efficiency to prolong the network lifetime.

## C. Performance Comparison

In this subsection, we compare the performance of two proposed schemes and two baseline schemes. There are statistical results of extensive simulation experiments shown in Fig. 6.

1) Average Coverage: As shown in Fig. 6(a), the average coverage of MaxCov-RG, MaxCov, n-CSCT-R and mTS are 96.7%, 93.3%, 89.3% and 81.4%. This is attributed that MaxCov-RG, MaxCov and n-CSCT-R consider maximizing the CoT. The mTS has the lowest average coverage because it does not pay attention to CoT and the resurrection of sensor nodes. Since n-CSCT-R is not a scheme for multiple charger collaboration, the average coverage of n-CSCT-R is also lower than the schemes proposed in this paper. This is in line with what we would have expected.

2) Coverage Rate: In Fig. 6(b), we observe the variation curves of the coverage rate of all schemes with time. The coverage rate of MaxCov-RG, MaxCov, n-CSCT-R and mTS at $t _ { e }$ are 95.8%, 89.1%, 80.5% and 64.1% respectively. It shows that the MaxCov scheme has a high coverage rate, which is 8.6% and 25% higher than n-CSCT-R and mTS. It is in line with what we would have expected given that the design objective of mTS scheme is to keep as many sensor nodes active as possible rather than maximizing the CoT, which is what this paper values. And, the MaxCov-RG scheme has the best coverage rate at $t _ { e } ,$ which is 6.7% higher than the MaxCov scheme. It shows that the MaxCov-RG scheme gets a better solution.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼

<!-- image-->  
(d)  
Fig. 6. Performance comparison for four schemes. (a) Average coverage. (b) Coverage Rate. (c) Energy efficiency. (d) Node survival rate.

3) Energy Efficiency: In Fig. 6(c), the energy efficiency Î· of MaxCov-RG, MaxCov, n-CSCT-R and mTS are 44.3%, 42.1%, 39.9% and 40.3% respectively. The two schemes proposed in this paper, MaxCov-RG and MaxCov, have better energy efficiency, which shows that more energy is transmitted to sensor nodes by the MC.

4) Node Survival Rate: Fig. 6(d) shows the node survival rate of the four schemes. All curves of node survival rate decrease as time grows in the initial phase, but in the late, they fluctuate and then stabilize, except n-CSCT-R scheme. Compared with mTS, the node survival rate of MaxCov-RG and MaxCov improved by 29.2% and 23.8% respectively. When compared to n-CSCT-R, MaxCov-RG and MaxCov still have higher node survival rates. The comparison mentioned above demonstrates the excellent performance of the two schemes suggested in this paper. Although our schemes prioritize maximum coverage of targets, the node survival rate in comparison to mTS improves with the implementation of the energy forecast model and the resurrection of sensor nodes. It shows that the performance of the schemes suggested in this paper is substantially better than the baseline. These outcomes demonstrate the viability of the proposed schemes.

## D. Performance Comparison With Different Network Scales

We compare the performance of the n-CSCT scheme with different network scales in this subsection. The simulation conditions are configured as follows: (i) 2 MCs and 80 nodes; (ii) 3 MCs and 120 nodes; (iii) 4 MCs and 160 nodes.

1) Average Coverage With Different Network Scales: As shown in Fig. 7(a), the average coverage of MaxCov-RG decreases slowly with increasing network size, the average coverage of MaxCov decreases faster than MaxCov-RG, and the average coverage of n-CSCT-R decreases fastest. It indicates that the proposed schemes are effective for collaborative charging in WRSNs. The average coverage of mTS is almost unchanged as the network size increases, because the network is divided into several subregions in the mTS scheme.

<!-- image-->  
(a)

<!-- image-->

<!-- image-->  
(cï¼

(b)  
<!-- image-->  
(d)  
Fig. 7. Performance comparison with different network scales. (a) Average coverage. (b) Energy efficiency. (c) Coverage Rate. (d) Node survival rate.

2) Energy Efficiency With Different Network Scales: In Fig. 7(b), the energy efficiency of the MaxCov-RG, MaxCov, n-CSCT-R, and mTS schemes under different network scales is presented. As the network scales increase, it can be observed that the energy efficiency of the MaxCov-RG scheme experiences a gradual decrease. However, despite this decrease, the MaxCov-RG scheme still outperforms the baseline approaches in terms of energy efficiency.

3) Coverage Rate With Different Network Scales: Fig. 7(c) shows the coverage rate at $t _ { e }$ of the MaxCov-RG, MaxCov, n-CSCT-R, and mTS schemes with different network scales. The coverage rate of the MaxCov-RG scheme decreases slowly with increasing network size, while the coverage rate of the MaxCov scheme decreases faster than MaxCov-RG. These observations suggest that the proposed schemes, including MaxCov-RG and MaxCov, are effective for collaborative charging in WRSNs.

4) Node Survival Rate With Different Network Scales: As shown in Fig. 7(d), the comparison further illustrates the exceptional performance of the two proposed schemes in this paper. Despite the primary focus of our schemes being the maximization of target coverage, the inclusion of an energy forecast model and the resurrection of sensor nodes contribute to a higher node survival rate compared to the mTS scheme.

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 8. Performance comparison with varying number of base stations. (a) Average coverage. (b) Energy efficiency.  
<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 9. Impact of n on performance for MaxCov-RG and n-CSCT-R. (a) Average coverage. (b) Energy efficiency.

## E. Performance Comparison With Varying Number of Base Stations

In this subsection, we assess the average coverage and energy efficiency of the MaxCov-RG, MaxCov, n-CSCT-R, and mTS schemes by varying the number of base stations, as depicted in Fig. 8. The simulation conditions are configured as follows: (i) 1 BS, 2 MCs and 80 nodes; (ii) 2 BSs, 4 MCs and 160 nodes; (iii) 3 BSs, 6 MCs and 240 nodes.

1) Average Coverage: The results presented in Fig. 8(a) reveal significant findings regarding the performance of the proposed schemes in WRSNs. First, these schemes exhibit varying decreases in average coverage as the network size expands. Second, the MaxCov-RG scheme showcases the least susceptibility to changes in network size, with the exception of the mTS scheme.

2) Energy Efficiency: Fig. 8(b) illustrates the energy efficiency of the MaxCov-RG, MaxCov, n-CSCT-R, and mTS schemes as the number of BSs varies. As the network scales increase, it can be observed that the energy efficiency of the MaxCov-RG scheme gradually decreases. Nevertheless, even with this decrease, the MaxCov-RG scheme still outperforms the baseline approaches in terms of energy efficiency.

## F. Impact of n on Performance

In this subsection, we compare the performance of MaxCov-RG and n-CSCT-R by varying the parameter n. Fig. 9 illustrates the evaluation of average coverage and energy efficiency for both MaxCov-RG and n-CSCT-R with different values of n.

1) Impact of n on Average Coverage: As depicted in Fig. 9(a), the average coverage initially experiences a rapid increase with the increment of the parameter n, but later exhibits a slower growth. This suggests that a larger value of the parameter n leads to improved target coverage. However, if the parameter n becomes excessively large, the computational complexity will also increase to a point where the MC cannot calculate it in real time.

2) Impact of n on Energy Efficiency: The energy efficiency of MaxCov-RG and n-CSCT-R with varying values of n is illustrated in Fig. 9(b). As the value of n increases, the energy efficiency exhibits a gradual decrease. This indicates that longer n-paths result in higher energy consumption during the movement of the MC.

## VIII. CONCLUSION

In this paper, we have addressed the problem of CoT maximization in on-demand charging scheduling for WRSNs by treating different charging requests differently. We proposed the MaxCov scheme, which involves constructing a pool of requests to handle heterogeneous requests effectively. Furthermore, we introduced the MaxCov-RG scheme, which well-balanced the trade-off between the performance and computational complexity. We also proved that the problem we addressed is NP-hard and demonstrated that the M/M/n queueing model outperforms a system with n M/M/1 queueing models in WRSNs with multiple mobile chargers. Performance evaluations have demonstrated that the MaxCov-RG scheme achieves a high coverage of targets.

## REFERENCES

[1] E. Sisinni, A. Saifullah, S. Han, U. Jennehag, and M. Gidlund, âIndustrial Internet of Things: Challenges, opportunities, and directions,â IEEE Trans. Ind. Inform., vol. 14, no. 11, pp. 4724â4734, Nov. 2018.

[2] T. Liu et al., âUtilizing the neglected back lobe for directional charging scheduling,â IEEE Trans. Mobile Comput., early access, Nov. 28, 2023, doi: 10.1109/TMC.2023.3334518.

[3] A. Kaswan, P. K. Jana, and S. K. Das, âA survey on mobile charging techniques in wireless rechargeable sensor networks,â IEEE Commun. Surveys Tut., vol. 24, no. 3, pp. 1750â1779, Third Quarter, 2022.

[4] W. You et al., âPractical charger placement scheme for wireless rechargeable sensor networks with obstacles,â ACM Trans. Sensor Netw., vol. 20, no. 1, pp. 1â23, 2024.

[5] Y. Yang and C. Wang, Wireless Rechargeable Sensor Networks, Berlin, Germany: Springer, 2015.

[6] R.-S. Liu, P. Sinha, and C. E. Koksal, âJoint energy management and resource allocation in rechargeable sensor networks,â in Proc. IEEE Conf. Comput. Commun., 2010, pp. 1â9.

[7] S. He, J. Chen, F. Jiang, D. K. Yau, G. Xing, and Y. Sun, âEnergy provisioning in wireless rechargeable sensor networks,â IEEE Trans. Mobile Comput., vol. 12, no. 10, pp. 1931â1942, Oct. 2013.

[8] L. Xie, Y. Shi, Y. T. Hou, and H. D. Sherali, âMaking sensor networks immortal: An energy-renewal approach with wireless power transfer,â IEEE/ACM Trans. Netw., vol. 20, no. 6, pp. 1748â1761, Dec. 2012.

[9] P. Zhou, C. Wang, and Y. Yang, âStatic and mobile target k-coverage in wireless rechargeable sensor networks,â IEEE Trans. Mobile Comput., vol. 18, no. 10, pp. 2430â2445, Oct. 2019.

[10] T. Wu et al., âJoint sensor selection and energy allocation for tasks-driven mobile charging in wireless rechargeable sensor networks,â IEEE Internet Things J., vol. 7, no. 12, pp. 11505â11523, Dec. 2020.

[11] V.-T. Pham, T. N. Nguyen, B.-H. Liu, M. T. Thai, B. Dumba, and T. Lin, âMinimizing latency for data aggregation in wireless sensor networks: An algorithm approach,â ACM Trans. Sensor Netw., vol. 18, no. 3, pp. 1â21, 2022.

[12] P. Yang et al., âMORE: Multi-node mobile charging scheduling for deadline constraints,â ACM Trans. Sensor Netw., vol. 17, no. 1, pp. 1â21, 2020.

[13] W. Ouyang, M. S. Obaidat, X. Liu, X. Long, W. Xu, and T. Liu, âImportance-different charging scheduling based on matroid theory for wireless rechargeable sensor networks,â IEEE Trans. Wireless Commun., vol. 20, no. 5, pp. 3284â3294, May 2021.

[14] T. Liu, B. Wu, S. Zhang, J. Peng, and W. Xu, âAn effective multi-node charging scheme for wireless rechargeable sensor networks,â in Proc. IEEE Conf. Comput. Commun., 2020, pp. 2026â2035.

[15] L. He, L. Kong, Y. Gu, J. Pan, and T. Zhu, âEvaluating the on-demand mobile charging in wireless sensor networks,â IEEE Trans. Mobile Comput., vol. 14, no. 9, pp. 1861â1875, Sep. 2015.

[16] C. Lin, J. Zhou, C. Guo, H. Song, G. Wu, and M. S. Obaidat, âTSCA: A temporal-spatial real-time charging scheduling algorithm for on-demand architecture in wireless rechargeable sensor networks,â IEEE Trans. Mobile Comput., vol. 17, no. 1, pp. 211â224, Jan. 2018.

[17] C. Lin, Z. Wang, J. Deng, L. Wang, J. Ren, and G. Wu, âmTS: Temporaland spatial-collaborative charging for wireless rechargeable sensor networks with multiple vehicles,â in Proc. IEEE Conf. Comput. Commun., 2018, pp. 99â107.

[18] C. Lin, Z. Yang, Y. Sun, J. Deng, L. Wang, and G. Wu, âCooperative game for multiple chargers with dynamic network topology,â in Proc. 49th Int. Conf. Parallel Process., 2020, pp. 1â10.

[19] A. Kaswan, P. K. Jana, M. Dash, A. Kumar, and B. P. Sinha, âDMCP: A distributed mobile charging protocol in wireless rechargeable sensor networks,â ACM Trans. Sensor Netw., vol. 19, no. 1, pp. 1â29, 2022.

[20] T. Liu, B. Wu, W. Xu, X. Cao, J. Peng, and H. Wu, âRLC: A reinforcement learning-based charging algorithm for mobile devices,â ACM Trans. Sensor Netw., vol. 17, no. 4, pp. 1â23, 2021.

[21] P. Zhou, C. Wang, and Y. Yang, âLeveraging target k-coverage in wireless rechargeable sensor networks,â in Proc. IEEE 37th Int. Conf. Distrib. Comput. Syst., 2017, pp. 1291â1300.

[22] H. Xue, H. Chen, Q. Dai, K. Lin, J. Li, and Z. Li, âCSCT: Charging scheduling for maximizing coverage of targets in WRSNs,â IEEE Trans. Computat. Social Syst., early access, May 06, 2022, doi: 10.1109/TCSS.2022.3169780.

[23] C. Lin et al., âGTCCS: A game theoretical collaborative charging scheduling for on-demand charging architecture,â IEEE Trans. Veh. Technol., vol. 67, no. 12, pp. 12124â12136, Dec. 2018.

[24] Y. Chen, H. Wu, Y. Liang, and G. Lai, âVarLenMARL: A framework of variable-length time-step multi-agent reinforcement learning for cooperative charging in sensor networks,â in Proc. IEEE 18th Annu. Int. Conf. Sens. Commun. Netw., 2021, pp. 1â9.

[25] A. Tomar, L. Muduli, and P. K. Jana, âA fuzzy logic-based on-demand charging algorithm for wireless rechargeable sensor networks with multiple chargers,â IEEE Trans. Mobile Comput., vol. 20, no. 9, pp. 2715â2727, Sep. 2021.

[26] N. Bansal, A. Blum, S. Chawla, and A. Meyerson, âApproximation algorithms for deadline-TSP and vehicle routing with time-windows,â in Proc. 36th Annu. ACM Symp. Theory Comput., 2004, pp. 166â174.

<!-- image-->  
Huansheng Xue received the BE and ME degrees in control science and engineering from the China University of Petroleum, Qingdao, China, in 2020 and 2023, respectively. He is currently working toward the PhD degree with the College of Control Science and Engineering, China University of Petroleum. His research interests include wireless sensor networks and Internet of Things.

<!-- image-->

Honglong Chen (Senior Member, IEEE) received the ME degree in control science and engineering from Zhejiang University, China, in 2008, and the PhD degree in computer science from The Hong Kong Polytechnic University, Hong Kong, in 2012. He was a postdoctoral researcher with the School of CIDSE, Arizona State University from 2015 to 2016. He is currently a professor and PhD supervisor with the College of Control Science and Engineering, China University of Petroleum, China. His current research interests are in the areas of Internet of Things, edge

computing and crowdsensing. He has published more than 100 research papers in prestigious journals and conferences including IEEE Transactions on Information Forensics and Security, IEEE Transactions on Mobile Computing, IEEE Transactions on Wireless Communications, IEEE Transactions on Industrial Informatics, IEEE Transactions on Vehicular Technology, IEEE Internet of Things Journal, IEEE INFOCOM, IEEE ICPP, IEEE ICDCS, etc. He is a senior member of CCF (China Computer Federation), and a member of ACM.

<!-- image-->

<!-- image-->

Zhichen Ni received the BE degree in measurement and control technology and instrumentation and the ME degree in control science and engineering from the China University of Petroleum, China, in 2019 and 2022, respectively. He is currently working toward the PhD degree with the College of Control Science and Engineering, China University of Petroleum. His current research interests include edge computing and edge intelligence.

Xiaolong Liu received the BE degree in automation from the China University of Petroleum, Qingdao, China, in 2022. He is currently working toward the ME degree with the College of Control Science and Engineering, China University of Petroleum. His research interest is in the field of mobile crowdsensing.

<!-- image-->

Feng Xia (Senior Member, IEEE) received the BSc and PhD degrees from Zhejiang University, Hangzhou, China. He is a professor with the School of Computing Technologies, RMIT University, Australia. He has published more than 300 scientific papers in international journals and conferences (such as IEEE Transactions on Artificial Intelligence, IEEE Transactions on Knowledge and Data Engineering, IEEE Transactions on Neural Networks and Learning Systems, IEEE Transactions on Computers, IEEE Transactions on Mobile Computing, IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Big Data, IEEE Transactions on Computational Social Systems, IEEE Transactions on Network Science and Engineering, IEEE Transactions on Emerging Topics in Computational Intelligence, IEEE Transactions on Emerging Topics in Computing, IEEE Transactions on Human-Machine Systems, IEEE Transactions on Vehicular Technology, IEEE Transactions on Intelligent Transportation Systems, IEEE Transactions on Automation Science and Engineering, ACM Transactions on Knowledge Discovery from Data, ACM Transactions on Intelligent Systems and Technology, ACM Transactions on the Web, ACM Transactions on Multimedia Computing, Communications, and Applications, WWW, AAAI, SIGIR, WSDM, CIKM, JCDL, EMNLP, and INFOCOM). His research interests include data science, artificial intelligence, graph learning, digital health, and systems engineering. He is a senior member of ACM, and an ACM distinguished speaker.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_3_img_1.png|page_3_img_1]]
2. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_5_img_1.png|page_5_img_1]]
3. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_5_img_2.png|page_5_img_2]]
4. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_7_img_1.png|page_7_img_1]]
5. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_7_img_2.png|page_7_img_2]]
6. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_12_img_1.jpeg|page_12_img_1]]
7. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_12_img_2.jpeg|page_12_img_2]]
8. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_12_img_3.jpeg|page_12_img_3]]
9. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_12_img_4.jpeg|page_12_img_4]]
10. [[../extracted_images/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling/page_12_img_5.jpeg|page_12_img_5]]

---

