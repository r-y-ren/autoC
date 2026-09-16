# Balancing Total Energy Consumption and Mean Makespan in Data Offloading for Space-Air-Ground Integrated Networks

Lijun He , Member, IEEE, Jiandong Li , Fellow, IEEE, Yanting Wang , Member, IEEE, Jiangbin Zheng , and Liang He, Member, IEEE

AbstractâWe study the data offloading problem in space-air-ground integrated networks (SAGINs) by jointly optimizing task scheduling and power control to balance the total energy consumption and mean makespan. We consider a mixed integer nonlinear programming problem to minimize a normalized weighted combination of these two conflicting objectives. We first propose an approximation algorithm to find a high-quality solution, which is shown to be at most 1 from the optimum to this problem for given power allocation. We further show that optimal power allocation can be obtained in closed form under the assumption that satellite-ground links have low signal-to-noise ratio (SNR). Thus, the proposed approximation algorithm can be directly utilized to obtain a constantfactor solution to the studied problem in low-SNR scenarios. To extend our solution to more general scenarios, we further propose an efficient hybird algorithm based on a genetic framework. Our simulation results demonstrate the near-optimality and correctness of the proposed algorithms, and they unveil the interplay between total energy consumption and mean makespan in SAGINs as well.

Index TermsâSpace-air-ground integrated networks, data offloading, total energy consumption, mean makespan

## 1 INTRODUCTION

WITH the rapid development of communication technol- ogies, new commercial applications spring up in large numbers, such as earth monitoring, maritime applications, smart cities, Internet of things, etc [1], [2], [3]. These new applications pose great challenges in both network resources and network coverage. Solely relying on ground networks is difficult to support these applications due to scarce communications resources and limited communications coverage. To complement ground networks, thereâs a growing recognition in both academia and industry that a large number of satellites, unmanned aerial vehicles (UAVs), and balloons in space platforms and air platforms, not only improve network performance but also extend network coverage [4]. Thus, the integration of space networks, air networks, and ground networks to construct a space-air-ground integrated network (SAGIN) has become an important way forward [5].

As illustrated in Fig. 1, SAGIN is a hierarchical network where communication nodes at different altitudes complement each other [6]. This multi-layered architecture leads to significant advantages in large-scale coverage, invulnerability, and high throughput. In view of this, SAGINs are widely used in many practical applications, such as environmental monitoring, mapping, meteorology, and natural disaster surveillance [7], [8], [9]. Recently, SAGINs have received a large amount of capital investment. Some commercial companies, such as SpaceX, Oneweb, and O3B, plan to deploy a large number of satellites in space. Moreover, there are many industrial research programs devoted to developing high altitude pseudo-satellite (HAPS) systems, such as Stratobus Platform of Thales, Zephyr Platform of Airbus, etc[10].

However, the fast proliferation of satellites, UAVs, and balloons in SAGINs has brought an explosive grown in space data. Meanwhile, the high-velocity movement of satellites leads to intermittent and limited transmission links [11]. This results in an increasingly prominent conflict between data offloading and transmission resource limitation in SAGINs. Therefore, it is important to investigate how to allocate the limited transmission resources of SAG-INs across space, air, and ground segments to efficiently offload the collected data.

Furthermore, compared with stand-alone ground networks, the majority of network nodes in SAGINs are batterypowered and energy-constrained satellites and aircrafts [12].

<!-- image-->  
Fig. 1. Space-air-ground integrated networks.

For example, the available energy stored in HAPSs is generally insufficient to support overnight use during winter months [13]. Moreover, the energy consumption not only determines the size of but also the lifetime of these batterycarrying satellites and aircrafts [14]. This constitutes a major bottleneck for data offloading in SAGINs. Therefore, it is critical to minimize the energy consumption of each network node to improve the data offloading efficiency of SAGINs. However, focusing only on energy minimization would prolong the makespan of data offloading tasks, which represents the time required for any data offloading task to be completed. In general, the makespan indicates the timeliness of space data and further determines the use value of space data in SAGINs. This because the use value of space data would be reduced or eliminated if it is offloaded too late [15]. As such, it is also a key performance metric of SAGINs.

In brief, it is imperative to design a data offloading scheme to schedule space tasks in SAGINs, to reduce both energy consumption and mean makespan. This problem is challenging in the following three aspects: 1) Intermittent of communications links. The order of scheduling tasks determines the makespan of each task [16]. Since the satellites in SAGINs orbit the earth with high speed, data offloading can occur only in some short and intermittent time windows. Therefore, the makespan of each data offloading task is very sensitive to the scheduling strategy. This makes it difficult to allocate transmission resources within the intermittent time windows for data offloading tasks to minimize their makespan. 2) Heterogeneity of communications links. Different network nodes in SAGINs offload their collected data in different communications links. These communication links are mainly grouped into two types : satellite-ground links (SGLs) and intermittent inter-satellite links (ISLs). The capacity of different communications links follows different channel models. This further complicates the data offloading problem. 3) Multiple criteria for data offloading. Both task scheduling and power control not only determine total energy consumption but also the makespan. It is challenging to design joint task scheduling and power control to achieve a nontrivial tradeoff between total energy consumption and mean makespan in SAGINs.

In this work, we jointly optimize task scheduling and power control while considering intermittent time windows in SAGINs, aiming to balance the conflicting objectives of total energy consumption and mean makespan. The main contributions of this work are summarized in the following:

We put forward an optimization framework to design task scheduling and power control and explore the interplay between the total energy consumption and the mean makespan in SAGINs, under the constraints of data offloading and power. We adopt as the performance metric a normalized weighted sum of the total energy consumption and the mean makespan. This results in a mixed integer nonlinear programming (MINLP) problem that well characterizes the main features of data offloading in SAGINs.

Leveraging the special structure of SAGINs, we propose an approximation algorithm termed the balanced energy and makespan algorithm with fixed power alocation (BEM-FPA) to solve the aforementioned problem when power allocation is given. It is shown to have 1 performance bound for the studied problem for given power allocation. We further derive a closed-form optimal solution to power allocation, thereby enabling BEM-FPA to directly solve our problem. For the scenario of SGLs with general SNR, we propose a two-layer optimization solution termed balanced energy and makespan (BEM). Specifically, in the upper layer, we adopt a genetic framework by optimizing power to minimize the designed performance metric, and in the lower layer, we call the BEM-FPA algorithm given the resultant power allocation.

Extensive simulations are conducted on SAGINs to demonstrate the following results: 1) For the low-SNR scenarios, direct application of BEM-FPA results in a constant-factor approximation algorithm that is within 2% of optimality in the worst case. 2) For the scenarios with moderate to high-SNR SGLs, we observe how BEM effectively trades off the conflicting objectives of total energy consumption and mean makespan over a wide range of weights between them. 3) Our proposed algorithm outperforms state-of-the-art alternatives under various parameter settings.

The rest of this paper is organized as follows. Section 2 provides a review of the related work. In Section 3, we present the system model and the problem formulation. In Section 4, we present the efficient data offloading algorithms to solve the studied problem. Section 5 presents simulation results and discussions. Finally, we give concluding remarks in Section 6.

## 2 RELATED WORK

Many existing works on the data offloading issue for space networks aim to efficiently allocate transmission resources within intermittent time windows. Their data offloading designs are based on the mathematical tools including graph theory [17], [18], [19], metaheuristics [20], [21], [22], convex optimization [23], and game theory [24].

The high dynamics of satellite networks poses new challenges to the design of data offloading. The works of [17], on July 16,2024 at 03:06:40 UTC from IEEE Xplore. Restrictions apply.

[18], [19] used graph models to characterize the dynamics of satellite networks. Liu et al. [17] used a time-expanded graph model to study the impact of antenna slewing time on data offloading. Zhou et al. [18] exploited the timeexpanded graph to address data offloading with consideration for time-varying and differentiated communication links in data relay satellite networks (DRSNs). Jia et al. [19] used inter-satellite links to enable data offloading among satellites and then employed a space-time topology graph to depict the dynamic topologies of low earth orbit (LEO) satellite networks, aiming to simplify the complexity of the proposed data offloading scheme. However, the construction of graph models in [17], [18], [19] would result in a high computation cost, especially as the number of satellites increases.

To accommodate the large-scale networks of satellites, the works of [20], [21], [22] turned to metaheuristics. Deng et al. [20] proposed an improved genetic task scheduling method to deal with uncertain factors in DRSNs. To address the problem of data breakpoint transmission in DRSNs, Chen et al. [21] developed a task scheduling method based on the variable neighborhood descent method. Furthermore, Dai et al. [22] devised a dynamic task scheduling method based on an improved genetic algorithm, aiming to ensure the data offloading efficiency of emergency tasks in DRSNs.

In addition to metaheuristics, our prior work [23] utilized a stochastic optimization method to perform dynamic hybrid task scheduling for DRSNs, aiming to maximize the number of hybrid tasks. By using a three-sided matching mechanism, Jia et al. [24] cooperated the transmission resources across LEO satellites and HAPs to maximize the revenue of SAGINs.

The aforementioned studies have considered some practical influencing factors into their data offloading models, such as antenna slewing time [17], time-varying and differentiated communication links [18], inter-satellite links[19], randomness of task arrivals [20], [23], randomness of system environment [21], emergency tasks [22], and resources cooperation [24]. However, these works do not consider energy consumption, which could lead to shortening of the lifetime of satellites and aircrafts, thereby deteriorating the data offloading performance of SAGINs.

Recent works have addressed the energy consumption issues in SAGINs. Dong et al. [25] proposed an integrated HAP-Satellite architecture to support a novel energy-efficient transmission scheme for emergency scenarios. By optimizing the ratio of average rate over total power consumption, An et al. [26] proposed an energy-efficient power allocation mechanism for land mobile satellite systems. Ji et al. [27] jointly optimized power control and downlink resources to improve the energy efficiency of data offloading for multi-cell satellite-terrestrial networks. With the consideration of energy consumption, time-varying links, and the differentiation for tasks, Zhou et al. [28] proposed an efficient data offloading strategy for small satellite networks.

However, it is difficult to directly apply the above works to solve the data offloading problem for SAGINs due to the following reasons: First, the works [25], [26], [27] neglect the dynamics topologies in their schemes. Second, the energy consumption in [28] is characterized as resource constraints in their problem model of data offloading, which does not allow direct tuning of energy efficiency. Third, none of [25], [26], [27], [28] study the impact of heterogeneity of communications links on the data offloading efficiency of SAGINs. Finally, the works [26], [27], [28] address the data offloading problem only in terms of minimizing energy consumption, which could prolong the makespan of tasks and further decrease the quality of data offloading.

In contrast to the above, in this work we study joint task scheduling and power control to reduce the energy consumption and makespan at the same time, both of which are important to the data offloading efficiency of SAGINs. Interestingly, it is found that the joint task offloading and power control problems have been well investigated in the context of edge computing networks. Specifically, Guo et al. [29] devised online offloading strategies to minimize the average task execution delay with considering the constraint of average energy consumption. Vu et al. [30] proposed an improved brand-and-bound algorithm to minimize the total energy consumption under the constraints of service delay. However, these offloading strategies are very hard to solve our problem. This is because data offloading in edge computing networks can occur in the whole scheduling horizon, while data offloading in SAGINs can occur only in some short and intermittent time windows. Hence, to address the data offloading in SAGINs with high efficiency, it is necessary to consider the special property of the SAGINs as our work.

## 3 SYSTEM MODEL AND PROBLEM FORMULATION

We consider an SAGIN as shown in Fig. 1. Notations used in the following are listed in Table 1. We divide the scheduling horizon of the SAGIN into a set of fixed-size time slots, denoted by $\mathcal { T } = \{ 1 , \ldots , T \}$ . Let time slot $t \in \tau$ index the T Â¼time interval of $[ t , t + 1 ]$ T g t 2 T. In the SAGIN, the data collectors Â½t;are denoted by set $\mathcal { S } = \{ 1 , \ldots , S \}$ , which consists of spaceborne $( \mathrm { e . g . }$ S Â¼ f ; ; Sg, low-orbit earth observation satellites), airborne (e.g., UAVs, airships), and terrestrial $( \mathrm { e . g . }$ , ships) nodes. The data transmission tasks of the data collectors are denoted by set $\mathcal { T } = \{ 1 , \ldots , I \}$ , which can be offloaded through either I Â¼ f ; ; IgSGLs or ISLs. We let index the data collector collecting sÃ°iÃthe data of task . The data collectors transmit their collected idata to data sinks, which are a set of data relay satellites (DRSs). For ease of analysis processing, we do not consider ground stations in this scenario. We let $\mathcal { H } = \{ 1 , \ldots , H \}$ H Â¼ f ; ; Hgdenote the set of data receiver antennas on the DRSs. For clarify, we further divide set into $\mathcal { H } _ { 1 }$ and $\mathcal { H } _ { 2 } , \mathrm { i . e . , } \ \mathcal { H } _ { 1 } \cup$ $\mathcal { H } _ { 2 } = \mathcal { H } ,$ , such that $\mathcal { H } _ { 1 }$ and $\mathcal { H } _ { 2 }$ H H H H [respectively denote the set of H Â¼ H H Hdata receiver antennas of DRSs to access non-spacecrafts and spacecrafts $( \mathrm { i . e . , }$ low-orbit satellites). Let $h ( s )$ be the hÃ°sÃdata receiver antenna accessed by data collector . Finally, we define ${ \mathcal { T } } _ { 1 } = \{ i | h ( s ( i ) ) \in { \mathcal { H } } _ { 1 } \}$ and $T _ { 2 } = \{ i | h ( s ( i ) ) \in \dot { \mathcal { H } _ { 2 } } \}$ I Â¼ fijhÃ°sÃ°iÃÃ 2 H g I Â¼ fijhÃ°sÃ°iÃÃ 2 H gas the set of data transmission tasks from non-spacecraft and spacecraft, respectively, such that $\mathcal { T } _ { 1 } \cup \mathcal { T } _ { 2 } = \mathcal { T }$

I [ I Â¼ IAn ISL or SGL is generated only when data collector $s \in$ moves within the coverage of antenna $h \in \mathcal H$ s 2on a DRS. S h 2 HParticularly, the relative movement between data collectors and data sinks leads to intermittent ISLs and SGLs. We term the activation of each ISL or SGL as the transmission time onJuly16,2024at 03:06:40UTC from IEEE Xplore.Restrictionsapply.

TABLE 1 Notation List
<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $i , j$ </td><td>task index</td></tr><tr><td> $\overrightharpoon { T }$ </td><td>maximum time slot index</td></tr><tr><td> $\tau$ </td><td>set of fixed-size time slots  $( { \mathrm { i . e . , } } T = \{ 1 , . . . , T \} )$ </td></tr><tr><td>S</td><td>maximum data collector index</td></tr><tr><td>S</td><td>set of data collectors  $( { \mathrm { i . e . , } } S = \{ 1 , \dots , S \} )$ </td></tr><tr><td>H</td><td>maximumdatareceiverantennaindex</td></tr><tr><td> $\mathcal { H }$ </td><td>set of data receiver antennas  $( { \mathrm { i . e . , } \mathcal { H } } = \{ 1 , \dots , H \} )$ </td></tr><tr><td> $h ( s )$ </td><td>data receiver antenna accessed by data collector s</td></tr><tr><td> $\mathcal { K } _ { s , h }$ </td><td>set of TTWs between data collectors s and antenna</td></tr><tr><td> $\kappa _ { S , h }$ </td><td> $h$  set of TTWs betweenall data collectors and antenna</td></tr><tr><td> $G _ { s ( i ) } ^ { \mathrm { t r a n } }$ </td><td> $h$  transmit antenna gain of data collector s(i)</td></tr><tr><td> $G _ { h } ^ { \mathrm { r e c } }$ </td><td></td></tr><tr><td></td><td>gain of data receiver antenna h</td></tr><tr><td> $L _ { f }$ </td><td>free space loss</td></tr><tr><td> $L _ { l }$ </td><td>total line loss</td></tr><tr><td> $N$ </td><td>noise power</td></tr><tr><td> $B _ { c }$ </td><td>bandwidth</td></tr><tr><td> $R _ { i h } ^ { \mathrm { S G L } }$ </td><td>achievable data rate of SGLs</td></tr><tr><td>K</td><td>Boltzmann&#x27;s constant (in  $J K ^ { - 1 } )$ </td></tr><tr><td> $T _ { s }$ </td><td>total system noise temperature (in K)</td></tr><tr><td> $\left( E _ { b } / N _ { 0 } \right) _ { \mathrm { r e q } }$ </td><td>required ratio of received energy-per-bit</td></tr><tr><td></td><td>to noise-density</td></tr><tr><td> $M$ </td><td> link margin</td></tr><tr><td> $R _ { i h } ^ { \mathrm { I S L } }$ </td><td>achievable data rate of ISLs</td></tr><tr><td> $p _ { i h }$ </td><td>transmission time of task i on antenna h</td></tr><tr><td> $D _ { i }$ </td><td>data size of task i</td></tr><tr><td> $a _ { k }$   $b _ { k }$ </td><td>beginning time of TTW k end time of TTW k</td></tr><tr><td> $\mathcal { F } ( i , h )$ </td><td>set of feasibility time slots for task iwithin the</td></tr><tr><td></td><td>TTWs</td></tr><tr><td></td><td>on anyantenna h</td></tr><tr><td> $\mathcal { F } ( i )$ </td><td>set of all the feasibility time slots for task i</td></tr><tr><td> $\Phi ( i , h , t )$ </td><td>set of occupying time slots for task i to start offloading in time slot t on antenna h</td></tr><tr><td> $P _ { \operatorname* { m i n } } ^ { s ( i ) }$ </td><td>minimum transmit power of data collector</td></tr><tr><td> $P _ { \mathrm { m a x } } ^ { s ( i ) }$ </td><td>maximum transmit power of data collector</td></tr><tr><td> $E _ { i }$ </td><td>energy consumption to transmit the data of task i</td></tr><tr><td> $E _ { \mathrm { m a x } }$ </td><td>maximum total energy consumption</td></tr><tr><td></td><td>of all data collectors</td></tr><tr><td> $E _ { \mathrm { t o l } } ^ { * }$ </td><td>optimal total energy consumption of all data collectors</td></tr><tr><td> $C _ { i }$ </td><td>completion time to offload the data of task i</td></tr><tr><td> $C _ { \mathrm { m a x } }$ </td><td> maximum mean makespan</td></tr><tr><td> $C ^ { * }$ </td><td>optimal mean makespan</td></tr><tr><td> $\lambda$ </td><td>weighting factor</td></tr></table>

window (TTW). In general, the periodic motion of data collectors leads to multiple TTWs associated with antenna $h ,$ sdenoted by $\boldsymbol { \kappa } _ { s , h }$ . We further introduce a two-tuple $( a _ { k } , b _ { k } )$ to Ks;hdepict the TTW $k \in \mathcal { K } _ { s , h }$ with $a _ { k }$ and $b _ { k }$ Ã°ak; bkÃrespectively reprek 2 Ks;h ak bksenting its beginning and end times. Let $\begin{array} { r } { \mathcal { K } _ { S , h } = \bigcup _ { s \in \mathcal { S } } \mathcal { K } _ { s , h } . } \end{array}$

KS;h Â¼ s2SKs;hIn this work, we aim to study the data offloading problem that how to efficiently offload the space data from a set of DRSs to data collectors. As such, we only consider the data offloading occurring on the one-hop ILSs between DRSs and data collectors without consideration of the data offloading among LEO satellites. Moreover, the data offloading between data collectors and ground users is out of the scope of this work.

## 3.1 Channel Model

In this subsection, we present the channel models for SGLs and ISLs as follows.

## 3.1.1 SGLs

We denote by the transmit power (in ) allocated to task . Let $P = \{ \bar { P _ { i } } \}$ Pi W. The SNR of SGLs can be evaluated by

$$
\mathrm { S N R } = \frac { P _ { i } G _ { s ( i ) } ^ { \mathrm { t r a n } } G _ { h } ^ { \mathrm { r e c } } L _ { f } L _ { l } } { N } , \forall i \in \mathbb { T } , h \in \mathcal { H } _ { 1 } ,\tag{1}
$$

where $G _ { s ( i ) } ^ { \mathrm { t r a n } }$ is the transmit antenna gain of data collector $s ( i ) , G _ { h } ^ { \mathrm { r e c } }$ sÃ°iÃis the gain of data receiver antenna $h , L _ { f }$ is the free sÃ°iÃ Ghspace loss, $L _ { l }$ h Lfis the total line loss, and  is the noise power. Ll NWe use the Shannon formula to compute the achievable data rate of SGLs

$$
R _ { i h } ^ { \mathrm { S G L } } = B _ { c } { \log _ { 2 } } ( 1 + \mathrm { S N R } ) , \forall i \in \mathbb { Z } , h \in \mathcal { H } _ { 1 } ,\tag{2}
$$

with $B _ { c }$ being the bandwidth. Here, we assume that data Bcoffloading on SGLs is error-free transmission and some impact factors on SGLs (e.g., rain attenuation, cloud, fog) can be dealt with transmission schemes in physical layers.

## 3.1.2 ISLs

The achievable data rate on ISLs [31], [32], [33] is expressed as

$$
R _ { i h } ^ { \mathrm { I S L } } = \frac { P _ { i } G _ { s ( i ) } ^ { \mathrm { t r a n } } G _ { h } ^ { \mathrm { r e c } } L _ { f } L _ { l } } { \kappa T _ { s } ( E _ { b } / N _ { 0 } ) _ { \mathrm { r e q } } M } , \forall i \in \mathcal { T } , h \in \mathcal { H } _ { 2 } ,\tag{3}
$$

where k is the Boltzmannâs constant (in $J K ^ { - 1 } )$ $T _ { s }$ is the total system noise temperature (in ), $( E _ { b } / N _ { 0 } ) _ { \mathrm { r e q } }$ Tsis the required K Ã°Eb=N Ãratio of received energy-per-bit to noise-density, and  is the link margin.

## 3.2 Constraints

We first introduce binary variable $x _ { i h t } \in \{ 0 , 1 \}$ to represent the offloading strategy, such that $x _ { i h t } = 1$ f ; gindicates that the xiht Â¼data of task is started to be offloaded in time slot $t \in \tau$ on antenna $h ;$ iotherwise $x _ { i h t } = 0 .$ . Let $\pmb { x } = \{ x _ { i h t } \}$ t 2 T. We define a h xiht Â¼ x Â¼ fxihtgfeasible time slot within TTW for task as the time slot in k iwhich the data of task can be started to be offloaded. As ishown in Fig. 2, the feasible time slots for task within TTW are $t _ { 3 } , t _ { 4 } , t _ { 5 } ,$ , and $t _ { 6 } .$ iAs such, we can define the set of feasik t t t tbility time slots for task within the TTWs on any antenna as

$$
\mathcal { F } ( i , h ) = \bigcup _ { k \in \mathcal { K } _ { s ( i ) , h } } [ a _ { k } , b _ { k } - p _ { i h } ] .\tag{4}
$$

Wherein, represents the transmission time of task on antenna $h ,$ pih which is calculated by

$$
p _ { i h } = \frac { D _ { i } } { R _ { i h } ^ { \mathrm { S G L } } } , \forall h \in \mathcal { H } _ { 1 } ,\tag{5}
$$

and

$$
p _ { i h } = \frac { D _ { i } } { R _ { i h } ^ { \mathrm { I S L } } } , \forall h \in \mathcal { H } _ { 2 } ,\tag{6}
$$

<!-- image-->  
Fig. 2. Illustration for the sets of feasibility time slots and occupying time slots.

with $D _ { i }$ being the data size of task . As such, we can intro-Di iduce the following constraint to state that the data of each task is offloaded exactly once within the feasibility time slots on all the antennas

$$
\sum _ { \begin{array} { l } { h \in { \mathcal { H } } } \\ { t \in { \mathcal { F } } ( i , h ) } \end{array} } x _ { i h t } = 1 , \forall i \in { \mathcal { T } } .\tag{7}
$$

Next, we let $\begin{array} { r } { \mathcal { F } ( i ) = \bigcup _ { h \in \mathcal { H } } \mathcal { F } ( i , h ) } \end{array}$ denote the set of all the F Ã°iÃ Â¼ h2HF Ã°i; hÃfeasibility time slots for task . As such, we have the binary constraints as follows:

$$
\begin{array} { r l } & { x _ { i h t } \in \{ 0 , 1 \} , \forall i \in \mathcal { T } , t \in \mathcal { F } ( i ) , } \\ & { x _ { i h t } = 0 , \forall i \in \mathcal { T } , t \notin \mathcal { F } ( i ) . } \end{array}\tag{8}
$$

(9)

We further observe from Fig. 2 that the data offloading of task occupies the feasible time slots within $[ t , t + p _ { i h } - 1 ]$ i Â½t; t Ã¾ pih  with being the time slot to start offloading. We define the tset of occupying time slots for task to start offloading in time slot on antenna as

$$
\begin{array} { r } { \Phi ( i , h , t ) = [ t , t + p _ { i h } - 1 ] \cap \mathscr { F } ( i , h ) . } \end{array}\tag{10}
$$

Furthermore, we use binary variables $\rho _ { i h t }$ to represent time slot allocation, so that $\rho _ { i h t } = 1$ ihtindicates that time slot of iht Â¼antenna is occupied to offload the data of task $i ;$ totherwise $\rho _ { i h t } = 0$ h. Let $\pmb { \rho } = \left\{ \rho _ { i h t } \right\}$ i. As such, we introduce the following iht Â¼ Â¼ f ihtgthree constraints to implicitly represent the antenna capacity: each antenna can transmit the data of at most one task in any time slot

$$
\sum _ { i \in \mathcal { T } } \rho _ { i h t } \leq 1 , \forall h \in \mathcal { H } , t \in \mathcal { T } ,\tag{11}
$$

$$
\begin{array} { r } { \rho _ { i h n } \geq x _ { i h t } , \forall n \in \Phi ( i , h , t ) , i \in \mathcal { I } , h \in \mathcal { H } , t \in \mathcal { T } , } \end{array}
$$

$$
\rho _ { i h t } \in \{ 0 , 1 \} , \forall i \in \mathcal { T } , h \in \mathcal { H } , t \in \mathcal { T } .\tag{12}
$$

(13)

Finally, we introduce the power control constraint as follows:

$$
P _ { \operatorname* { m i n } } ^ { s ( i ) } \leq P _ { i } \leq P _ { \operatorname* { m a x } } ^ { s ( i ) } , \forall i \in \mathcal { I } ,\tag{14}
$$

where $P _ { \operatorname* { m i n } } ^ { s ( i ) }$ and $P _ { \mathrm { m a x } } ^ { s ( i ) }$ respectively denote the minimum P Ptransmit power and the maximum transmit power of data collector .

## 3.3 Problem Formulation

We denote by $E _ { i }$ the energy consumption to transmit the data of task $i ,$ Ei which is given by

$$
E _ { i } = \sum _ { \begin{array} { c } { h \in \mathscr { H } } \\ { t \in \mathscr { F } ( i , h ) } \end{array} } x _ { i h t } P _ { i } p _ { i h } .\tag{15}
$$

Then, the total energy consumption of the data collectors is

$$
\begin{array} { r } { E _ { \mathrm { t o l } } = \displaystyle \sum _ { i \in \mathcal { I } } E _ { i } = \displaystyle \sum _ { i \in \mathcal { I } } \sum _ { \begin{array} { c } { h \in \mathcal { H } } \\ { t \in \mathcal { F } ( i , h ) } \end{array} } x _ { i h t } P _ { i } p _ { i h } . } \end{array}\tag{16}
$$

Let $E _ { \mathrm { m a x } }$ and $E _ { \mathrm { t o l } } ^ { * }$ be the maximum total energy consump-E Etion and the optimal total energy consumption of all data collectors, respectively.

Let $C _ { i }$ be the completion time to offload the data of task . CiWe have

$$
C _ { i } = \sum _ { \begin{array} { c } { h \in \mathcal { H } } \\ { t \in \mathcal { F } ( i , h ) } \end{array} } x _ { i h t } ( t + p _ { i h } - 1 ) .\tag{17}
$$

We define the mean makespan as the mean sum of the completion time of tasks, which is expressed as $\begin{array} { r } { C = \frac { 1 } { | T | } \sum _ { i \in \mathcal { T } } C _ { i } } \end{array}$ Let $C _ { \mathrm { m a x } }$ and $C ^ { * }$ C Â¼ jIj i2I Cibe the maximum mean makespan and opti-C Cmal mean makespan, respectively.

We focus on a static data offloading problem to minimize the total energy consumption and the mean makespan of tasks. Here, we adopt the normalized weighted sum method [34] to balance the two conflicting objectives of minimizing both total energy consumption and mean makespan. This can provide a complete Pareto-optimal set [35] for our problems. In the normalized weighted sum method, each objective function should be first normalized in (0,1) aiming to give equal emphasis, and then multiplied by weights. Here, we introduce a weighting factor $\lambda \in [ 0 , 1 ]$ to - 2 Â½ ; balance two designed objectives. In practical applications, we tun the values of in [0,1] to obtain a set of mean make--span and total energy consumption for choice. Thus, we consider an MINLP problem given by

$$
\begin{array} { l } { { \displaystyle { \bf P 0 } \colon \operatorname* { m i n } _ { x , P } \left( \lambda \frac { C - C ^ { * } } { C _ { \mathrm { m a x } } - C ^ { * } } + ( 1 - \lambda ) \frac { E _ { \mathrm { t o l } } - E _ { \mathrm { t o l } } ^ { * } } { E _ { \mathrm { m a x } } - E _ { \mathrm { t o l } } ^ { * } } \right) } } \\ { { \mathrm { s . t . ~ } ( 7 ) - ( 9 ) , } } \\ { { \displaystyle \left( 1 1 \right) - ( 1 4 ) . } } \end{array}
$$

Note that compared with aerial networks or ground networks, one key characteristic of SAGINs is in the intermittent ISLs due to the high-speed motion of LEO satellites. In particular, the intermittent ISLs are depicted as the time window constraints of (7), (11), and (12) in P0 . As such, P0 is capable of capturing the key characteristic of SAGINs.

## 3.4 Problem Analysis

For analytical tractability, we rewrite P0 in the following form

$$
\begin{array} { r l } & { \mathbf { P 0 } \colon \underset { x , P } { \operatorname* { m i n } } \left( \lambda \frac { C } { C _ { \operatorname* { m a x } } - C ^ { * } } + ( 1 - \lambda ) \frac { E _ { \mathrm { t o l } } } { E _ { \operatorname* { m a x } } - E _ { \mathrm { t o l } } ^ { * } } \right) - \mathcal { U } } \\ & { \mathrm { s . t . } \ ( 7 ) - ( 9 ) , } \\ & { \quad \ ( 1 1 ) - ( 1 4 ) , } \end{array}
$$

where a constant is defined as

$$
\mathcal { U } = \lambda \frac { C ^ { * } } { C _ { \operatorname* { m a x } } - C ^ { * } } + ( 1 - \lambda ) \frac { E _ { \mathrm { t o l } } ^ { * } } { E _ { \operatorname* { m a x } } - E _ { \mathrm { t o l } } ^ { * } } .
$$

The following two preliminary observations reveal the different properties of the studied problem depending on whether $\bar { \lambda } > 0$ . It is obvious that when $\lambda = 0$ P0 degrades - > - Â¼into an energy minimization problem. In this case, since a smaller transmission power leads to a longer transmission duration, which can increase the energy consumption. In general, it is non-trivial to find the optimal power to minimize the energy consumption. However, as shown in the theorem below, in our problem, the minimum transmit power is optimal.

Theorem 1. When 0, we have $P _ { i } ^ { * } = P _ { \operatorname* { m i n } } ^ { s ( i ) } , \forall i .$

Proof. See Appendix A, (available online).

Theorem 2. P0 is NP-hard in general when  0 1 .

Proof. See Appendix B, available in the online supplemental material. â¡

## 4 PROPOSED SOLUTIONS

In this section, we first devise an approximation algorithm, termed BEM-FPA, with performance guarantee to solve P0 for given power allocation. Then, utilizing this algorithm as a building block, we solve P0 for the scenarios with both low-SNR SGLs and more general SGLs.

## 4.1 Approximation Algorithm With Performance Guarantee for Given Power Allocation

With given power allocation, P0 becomes the following problem

$$
\begin{array} { r l r } {  { \mathbf { P 0 } ^ { \mathrm { f i x e d \ p o w e r } } : \operatorname* { m i n } _ { \pmb { x } } \mathcal { G } \sum _ { i \in \mathcal { T } } \displaystyle \sum _ { h \in \mathcal { H } } x _ { i h t } ( t + p _ { i h } - 1 ) + \mathcal { V } } } \\ & { } & { ~ t \in \mathcal { F } ( i , h ) } \\ & { } & { \mathrm { s . t . ~ } ( 7 ) - ( 9 ) , } \\ & { } & { ( 1 1 ) - ( 1 3 ) , } \end{array}
$$

where constants and are respectively defined as

$$
\mathcal { G } = \frac { \lambda } { \vert \mathcal { T } \vert ( C _ { \mathrm { m a x } } - C ^ { * } ) }
$$

and

$$
\mathcal { V } = ( 1 - \lambda ) \frac { E _ { \mathrm { t o l } } - E _ { \mathrm { t o l } } ^ { * } } { E _ { \mathrm { m a x } } - E _ { \mathrm { t o l } } ^ { * } } - \mathcal { G } C ^ { * } .
$$

For the convenience of analysis, we remove the constant terms  and  from P0fixed power without changing its optimal G Vsolutions, to obtain the following task scheduling optimization problem

$$
\begin{array} { l } { { \displaystyle { \bf P 1 } \colon \operatorname* { m i n } _ { { \bf x } } \sum _ { i \in \mathcal { T } } \sum _ { h \in \mathcal { H } } x _ { i h t } ( t + p _ { i h } - 1 ) } \ ~ } \\ { { \displaystyle t \in \mathcal { F } ( i , h ) } } \\ { { \mathrm { s . t . ~ } ( 7 ) - ( 9 ) } , \ ~ } \\ { { \displaystyle \qquad ( 1 1 ) - ( 1 3 ) } . } \end{array}
$$

To solve P0fixed power efficiently, we first design a BEM-FPA algorithm with performance guarantee to solve P1 in Section 4.1.1, and then determine the values of parameters and  by evaluating the values of $E _ { \mathrm { t o l } } ^ { * } , E _ { \mathrm { m a x } } , C ^ { * }$ , and $C _ { \mathrm { m a x } }$ Gin VSection 4.1.2.

## 4.1.1 Task Scheduling Optimization

It would be easy to obtain heuristic solution to P1 through the Lagrangian Fix-and-Relax method developed in [36]. However, it is hard to quantify the performance gap between such a solution and the optimal solution. Therefore, we do not use this method to solve P1 but turn to leverage the convex quadratic and semidefinite relaxation (CQSR) method [37] to transform P1 into a convex quadratic program. Then, we use the rounding method PIPAGE [38] to convert the fractional solution to this convex quadratic program into an intergal solution. Finally, we prove that the obtained intergal solution has a constant-factor performance guarantee.

We observe that the difficulty to solve P1 is in the time window constraints of (7), (11), and (12). In what follows, we first exploit the special characteristics of space network to tackle the time window constraints aiming at simplifying P1, such that the CQSR method can be used to solve it. In particular, we observe that the considered network is consist of DRSs, which are in geosynchronous earth orbit (GEO). Also, three such DRSs are capable of providing 100 percent global coverage. As such, several DRSs are concentrated in three locations instead of uniformly distributed in GEO. This special structure of satellite constellation is used in the practical data relay satellite systems such as tracking and data relay satellite system (TDRSS) [39], Tianlian system [40], and European data relay satellite (EDRS) system [41]. Since the transmit antennas on DRSs in the same location are close to each other, they may be regarded as having the same TTWs.

Notice that the endpoints of TTWs $\kappa _ { S , h }$ partition the KS;hscheduling horizon of any antenna  into a set of time segments $( t _ { l } , t _ { l + 1 } ) , l = 1 , 2 , \ldots ,$ h as shown in Fig. 3a. For any Ã°antenna $h ,$ lÃ¾ Ã; l Â¼ ; ; we merge these time segments into time-slot hblocks by calculating the union set of $\bar { \kappa } _ { s , h } ,$ as shown Fig. 3b. KS;hFor example, the union set of time windows $( t _ { 1 } , t _ { 3 } )$ and $( t _ { 2 } , t _ { 4 } )$ in Fig. 3a is the time-slot block $( t _ { 1 } , t _ { 4 } )$ Ã°t ; t Ãin Fig. 3b. As Ã°t ; t Ãsuch, we merge time segments $( t _ { l } , t _ { l + 1 } ) , l = 1 , 2 , 3$ into timeslot block $( t _ { 1 } , t _ { 4 } )$ Ã°tl; tlÃ¾ Ã; l Â¼ ; ;. Then, we need to construct a compressed Ã°t ; t Ãspace by compressing the time axis to merge the produced time-slot blocks, as shown Fig. 3c. As such, the data offloading problem in the compressed space is without the time window constraints, thereby significantly simplifying P1.

<!-- image-->

(b)  
<!-- image-->  
Fig. 3. Time block construction.

We refer to each merged time-slot block as a machine and let $\mathcal { M } = \{ 1 , \dots , M \}$ denote the set of machines. Denote by $\Delta _ { i m }$ M Â¼ f ; ; Mgthe transmission time of task on machine . In what im i mfollows, our main idea is that each task is first assigned to ia machine, followed by which the tasks are sequenced in each machine. It is clear that the above two steps are without losing optimality of P1. We introduce new variables $y _ { i m } \in \{ 0 , 1 \}$ to present the scheduling strategy, where $y _ { i m } =$ yim 2 f ; g yim Â¼1 indicates that task is allocated to antenna to offload its data; otherwise $y _ { i m } = 0$ m. Furthermore, we denote by $\prec _ { m }$ an yim Â¼ morder for any machine on to sequence tasks. In particum Ilar, it is an optimal assignment of tasks to each machine according to the Smithâs rule [16]: $j \prec _ { m }$ if $\Delta _ { j m } \leq \Delta _ { i m }$ ,Amâ j m i jm  im; 8m 2. As such, we give a reformulation of P1 over a com-Mpressed time space as follows:

$$
\mathbf { P } 2 \colon \ \operatorname* { m i n } _ { \pmb { y } } \ \sum _ { i \in \mathcal { T } } \ C _ { i } ^ { \prime }
$$

$$
\mathrm { s . t . } \sum _ { m \in \mathcal { M } } y _ { i m } = 1 , \forall i \in \mathcal { T } ,\tag{18}
$$

$$
C _ { i } ^ { \prime } = \sum _ { m \in \mathcal { M } } y _ { i m } \big ( \Delta _ { i m } + \sum _ { j \prec _ { m } i } y _ { j m } \Delta _ { j m } \big ) , \forall i \in \mathcal { I } ,\tag{19}
$$

$$
y _ { i m } \in \{ 0 , 1 \} , \forall i \in \mathcal { I } , m \in \mathcal { M } .\tag{20}
$$

Constraints (18) reflect that each task is assigned to exactly one machine. Constraints (19) is the completion time. Notice that $C _ { i } ^ { \prime }$ in the objective function can be replaced by the term Cion the right-hand side of constraints (19), thus getting rid of constraints (19). Constraints (20) are binary constraints.

Then, we further remove constraints (19) from P2 to obtain the following form

$$
\begin{array} { r l } & { \mathbf { P 3 } \colon \displaystyle \operatorname* { m i n } _ { \pmb { y } } \displaystyle \sum _ { i \in \mathbb { Z } } \displaystyle \sum _ { m \in \mathcal { M } } y _ { i m } \big ( \Delta _ { i m } + \sum _ { j \prec _ { m } i } y _ { j m } \Delta _ { j m } \big ) } \\ & { \mathrm { s . t . } \quad \displaystyle \sum _ { m \in \mathcal { M } } y _ { i m } = 1 , \forall i \in \mathbb { Z } , } \\ & { \qquad y _ { i m } \in \{ 0 , 1 \} , \forall i \in \mathbb { Z } , m \in \mathcal { M } . } \end{array}
$$

In the following, we define as a vector of length given by $c _ { i m } = p _ { i m }$ . Let $W = \left( w _ { ( i m ) ( j m ^ { \prime } ) } \right)$ IMbe a symmetric $I M \times I M$ cim Â¼ pim-matrix with

$$
w _ { ( i m ) ( j m ^ { \prime } ) } = \left\{ \begin{array} { r l } { { 0 } } & { { m \neq m ^ { \prime } \mathrm { ~ o r ~ } i = j , } } \\ { { p _ { i m } } } & { { m = m ^ { \prime } \mathrm { ~ a n d ~ } i \prec _ { m } j , } } \\ { { p _ { j m } } } & { { m = m ^ { \prime } \mathrm { ~ a n d ~ } j \prec _ { m } i . } } \end{array} \right.\tag{21}
$$

It is observed from (21) that we can decompose $W$ into $| { \mathcal { M } } |$ W jMjdiagonal blocks, each corresponding to a time-slot block of a machine $m ,$ denoted by $W _ { m } .$ ,AmâM

$$
W _ { m } = \left( \begin{array} { c c c c c } { { 0 } } & { { \Delta _ { 1 m } } } & { { \Delta _ { 1 m } } } & { { \cdots } } & { { \Delta _ { 1 m } } } \\ { { \Delta _ { 1 m } } } & { { 0 } } & { { \Delta _ { 2 m } } } & { { \cdots } } & { { \Delta _ { 2 m } } } \\ { { \Delta _ { 1 m } } } & { { \Delta _ { 2 m } } } & { { 0 } } & { { } } & { { \Delta _ { 3 m } } } \\ { { \vdots } } & { { \vdots } } & { { } } & { { \ddots } } & { { \vdots } } \\ { { \Delta _ { 1 m } } } & { { \Delta _ { 2 m } } } & { { \Delta _ { 3 m } } } & { { \cdots } } & { { 0 } } \end{array} \right) .\tag{22}
$$

Then, P3 can be written in the following form

$$
\begin{array} { l } { \displaystyle \mathbf { P 4 } \colon \displaystyle \operatorname* { m i n } _ { \pmb { y } } F ( \pmb { y } ) = \pmb { c } ^ { T } \pmb { y } + \frac { 1 } { 2 } \pmb { y } ^ { T } W \pmb { y } } \\ { \mathrm { s . t . } \quad \displaystyle \sum _ { m \in \mathcal { M } } y _ { i m } = 1 , \forall i \in \mathcal { T } , } \\ \qquad \displaystyle y _ { i m } \in \{ 0 , 1 \} , \forall i \in \mathcal { T } , m \in \mathcal { M } .  \end{array}
$$

We relax $\pmb { y }$ to be continuous and obtain the following problem

$$
\begin{array} { l } { \displaystyle \mathbf { P 5 } \colon \mathrm { ~ \operatorname* { m i n } _ { \pmb { y } } ~ } F ( \pmb { y } ) = \pmb { c } ^ { T } \pmb { y } + \frac { 1 } { 2 } \pmb { y } ^ { T } W \pmb { y } } \\ { \mathrm { s . t . } \quad \displaystyle \sum _ { m \in \mathcal { M } } y _ { i m } = 1 , \forall i \in \mathcal { T } , } \\ { \quad \quad \quad 0 \leq y _ { i m } \leq 1 , \forall i \in \mathcal { I } , m \in \mathcal { M } . } \end{array}\tag{23}
$$

The optimal objective value to P5 is equal to that of $\mathbf { P 4 , }$ which can be easy proved according to the corollary 2.3 in [37]. Furthermore, one can observe that P5 is convex if and only if matrix $W$ is positive semidefinite. Unfortunately, Wmatrix is not always positive semidefinite. To this end, Wwe need to raise the diagonal entries of $W ,$ such that it is Wpositive semidefinite. This leads to the following new optimization problem, given by

$$
\begin{array} { r l } & { \displaystyle \mathbf { P 6 } \colon \displaystyle \operatorname* { m i n } _ { \pmb { y } } G _ { \xi } ( \pmb { y } ) = ( 1 - \xi ) \pmb { c } ^ { T } \pmb { y } + \frac { 1 } { 2 } \pmb { y } ^ { T } ( W + 2 \xi \mathrm { d i a g } ( \pmb { c } ) ) \pmb { y } } \\ & { \mathrm { s . t . } \quad \displaystyle \sum _ { m \in \mathcal { M } } y _ { i m } = 1 , \forall i \in \mathcal { T } , } \\ & { \displaystyle 0 \leq y _ { i m } \leq 1 , \forall i \in \mathcal { T } , m \in \mathcal { M } , } \end{array}
$$

where $\xi$ is a positive constant within (0,1).

To reveal the relationship between P5 and P6, we give the following theorem:

Theorem 3. P6 provides a lower bound of the optimal objective value to P5 for any $\xi > 0$

Proof. See Appendix C, available in the online supplemental material. â¡

Inspired by Theorem 3, we aim to find a tight lower bound of P5. Therefore, we consider the following optimization problem

$$
\begin{array} { r l } & { \mathbf { P } { \boldsymbol { \mathsf { 7 } } } { : \begin{array} { l } { \underset { \pmb { y } } { \operatorname* { m i n } } } \end{array} } \operatorname* { m a x } _ { \xi } G _ { \xi } ( \pmb { y } ) } \\ & { \mathrm { s . t . } \quad \displaystyle \sum _ { m \in \mathcal { M } } y _ { i m } = 1 , \forall i \in \mathbb { Z } , } \\ & { \qquad 0 \leq y _ { i m } \leq 1 , \forall i \in \mathbb { Z } , m \in \mathcal { M } . } \end{array}
$$

Obviously, P7 can be rewritten as the following form

```batch
P8: min
y,Z
s.t .
X 1
mEM
0â¤yimâ¤1,âiâI,mâM,
Zâ¥0.
```

We use the following lemma that specifies when P8 is a convex problem.

Lemma 1 (Lemma 2.4, [37]). P8 is convex if and only i $\begin{array} { r } { : \xi \ge \frac { 1 } { 2 } . } \end{array}$

Then, the following theorem reveals the relationship between the optimal objective values of P5 and P8.

Theorem 4. The optimal objective value to P8 is 2 times the optimal objective value to P5 $\begin{array} { r } { \dot { i } f \xi = \frac { 1 } { 2 } } \end{array}$

Proof. See Appendix D, available in the online supplemental material. â¡

Thus, we set $\xi = \textstyle { \frac { 1 } { 2 } }$ to rewrite P8 as the following problem

$$
\begin{array} { r l } & {  { \mathbf { P 9 } } \colon \displaystyle \operatorname* { m i n } _ { \pmb { y } , Z } Z } \\ & { \mathrm { s . t . } Z \geq G _ { \frac { 1 } { 2 } } ( \pmb { y } ) = \frac { 1 } { 2 } \pmb { c } ^ { T } \pmb { y } + \frac { 1 } { 2 } \pmb { y } ^ { T } ( W + \mathrm { d i a g } ( \pmb { c } ) ) \pmb { y } , } \\ & { \qquad \displaystyle \sum _ { m \in \cal M } y _ { i m } = 1 , \forall i \in \mathcal { I } , } \\ & { \qquad \displaystyle 0 \leq y _ { i m } \leq 1 , \forall i \in \mathcal { I } , m \in \mathcal { M } , } \\ & { \qquad \displaystyle Z > 0 . } \end{array}
$$

Furthermore, we substitute $\xi = \textstyle { \frac { 1 } { 2 } }$ to (34) to yield

$$
\begin{array} { r l } & { \displaystyle { F ( \pmb { y } ) = G _ { \frac { 1 } { 2 } } ( \pmb { y } ) + \frac { 1 } { 2 } \left( \pmb { c } ^ { T } \pmb { y } - \pmb { y } ^ { T } \mathrm { d i a g } ( \pmb { c } ) \pmb { y } \right) } } \\ & { \qquad \le { Z + \frac { 1 } { 2 } \left( \pmb { c } ^ { T } \pmb { y } - \pmb { y } ^ { T } \mathrm { d i a g } ( \pmb { c } ) \pmb { y } \right) } . } \end{array}\tag{24}
$$

It is observed from (24) that if $Z \geq \pmb { c } ^ { T } \pmb { y } ,$ then we obtain

$$
F ( { \pmb y } ) \le \frac { 3 } { 2 } Z - \frac { 1 } { 2 } { \pmb y } ^ { T } \mathrm { d i a g } ( { \pmb c } ) { \pmb y } \le \frac { 3 } { 2 } Z .\tag{25}
$$

This means that we can add a lower bound constraint on $Z ~ ( \mathrm { i . e . } , ~ Z \geq c ^ { T } y )$ to improve the approximation of P9, as Z Z  c yshown in Theorem 5 below. This leads to a relaxed problem as follows:

```perl
P10: min
y,Z
s.t. $Z \geq { \frac { 1 } { 2 } } { \pmb { c } } ^ { T } { \pmb { y } } + { \frac { 1 } { 2 } } { \pmb { y } } ^ { T } ( W + \mathrm { d i a g } ( { \pmb { c } } ) ) { \pmb { y } } ,$
Zâ¥Ty
X  1
mEM
0   1
 yim  0
```

We propose to solve P0fixed power by first solving P10 and then using the PIPAGE method [38] to recover an integer solution. This algorithm is termed BEM-FPA and is summarized in Algorithm 1.

Algorithm 1. Balanced Energy and Makespan Algorithm   
With Fixed Power Allocation (BEM-FPA)   
Input: Given $\xi = \textstyle { \frac { 1 } { 2 } }$ and $P _ { i } , \forall i .$   
 Â¼ 1: Formulate P10.   
2: Obtain an optimal solution  to P10.   
y3: Use the PIPAGE method to convert  into integer solution -.   
Output: -.

Furthermore, the following result reveals the approximation performance of BEM-FPA.

Theorem 5. BEM-FPA produces a 1 -approximate solution to fixed power

Proof. See Appendix E, available in the online supplemental material. â¡

Theorem 6. BEM-FPA has a time complexity of $\mathcal { O } ( ( I M ) ^ { 4 . 5 } \mathrm { l o g } \left( 1 / \epsilon \right) )$ , where $\epsilon \geq 0$ is the solution accuracy.

Proof. See Appendix F, available in the online supplemental material. â¡

## 4.1.2 Parameters Determination

To obtain the values of and , we need to determine the values of $E _ { \mathrm { t o l } } ^ { * } , \ E _ { \mathrm { m a x } } , \ C ^ { * } ,$ V, and $C _ { \mathrm { m a x } } .$ . We note that the E E C Ckey idea of the normalized weighted sum method [34] is to transform multiple objective functions with different range and units into their normalized weighted sum (i.e., the sum of non-dimensional objective functions), while guaranteeing that each normalized objective function is a function with a lower limit of zero and an upper limit of one. Theorem 2 indicates that computing the optimal values of $E _ { \mathrm { t o l } } ^ { * }$ and $C ^ { * }$ could result in a pro-E Chibitive cost. To reduce computational cost, the authors of [34] propose a suggestion that one can use their approximations for each optimal value of objective function to guarantee that each designed objective has a value between zero and one. Along this idea, we adopt the lower bounds of $E _ { \mathrm { t o l } } ^ { * }$ and $C ^ { * }$ as their approximations, denoted by $\hat { E } _ { \mathrm { t o l } } ^ { * }$ and ${ \hat { C } } ^ { * } .$ C, respectively.

E CThe following theorem indicates the values of $\hat { E } _ { \mathrm { t o l } } ^ { * }$ and $E _ { \mathrm { m a x } } .$

Theorem 7. The lower bound and upper bound of $E _ { \mathrm { t o l } } ^ { * }$ are respectively as follows:

$$
\begin{array} { r l } & { \hat { E } _ { \mathrm { t o l } } ^ { * } = \displaystyle \sum _ { i \in T _ { 1 } } \frac { P _ { \mathrm { m i n } } ^ { s ( i ) } D _ { i } } { B _ { c } \log \left( 1 + \frac { P _ { \mathrm { m i n } } ^ { s ( \mathrm { t r a n } } G _ { s ( i ) } ^ { \mathrm { r e c } } L _ { f } L _ { l } } { N } \right) } } \\ & { \qquad + \displaystyle \sum _ { i \in Z _ { 2 } } \frac { D _ { i } \kappa T _ { s } \left( E _ { b } / N _ { 0 } \right) _ { \mathrm { r e q } } M } { G _ { s ( i ) } ^ { \mathrm { t r a n } } G _ { h _ { c } ^ { * } } ^ { \mathrm { r e c } } L _ { f } L _ { l } } , } \\ & { \qquad h _ { i } ^ { * } = \mathrm { a r g m a x } \{ G _ { h } ^ { \mathrm { r e c } } , h \in \mathcal { H } _ { 1 } \} , } \\ & { \qquad h _ { 2 } ^ { * } = \mathrm { a r g m a x } \{ G _ { h } ^ { \mathrm { r e c } } , h \in \mathcal { H } _ { 2 } \} , } \end{array}
$$

and

$$
\begin{array} { r l } { E _ { \mathrm { m a x } } = } & { \displaystyle \sum _ { i \in \mathcal { I } _ { 1 } } \frac { P _ { \mathrm { m a x } } ^ { s ( i ) } D _ { i } } { B _ { \mathrm { c l o g } } \left( 1 + \frac { P _ { \mathrm { m a x } } ^ { s ( i ) } G _ { s ( i ) } ^ { \mathrm { r a n } } G _ { h _ { 3 } } ^ { \mathrm { r e c } } L _ { f } L _ { l } } { N _ { 3 } } \right) } } \\ & { + \displaystyle \sum _ { i \in \mathcal { I } _ { 2 } } \frac { D _ { i } \kappa T _ { s } \left( E _ { b } / N _ { 0 } \right) _ { \mathrm { r e q } } M } { G _ { s ( i ) } ^ { \mathrm { t r a n } } G _ { h _ { 4 } ^ { * } } ^ { \mathrm { r e c } } L _ { f } L _ { l } } , } \\ { h _ { 3 } ^ { * } = \displaystyle \mathrm { a r g m i n } \{ G _ { h } ^ { \mathrm { r e c } } , h \in \mathcal { H } _ { 1 } \} , } \\ { h _ { 4 } ^ { * } = \displaystyle \mathrm { a r g m i n } \{ G _ { h } ^ { \mathrm { r e c } } , h \in \mathcal { H } _ { 2 } \} . } \end{array}
$$

Proof. See Appendix $G ,$ available in the online supplemental material. â¡

Furthermore, we sequence tasks on antenna in order of descending processing time, denoted by $\prec _ { h }$ h. We give the following theorem:

Theorem 8. The lower bound of is $\hat { C } ^ { * } = Z ^ { * }$ , where $Z ^ { * }$ is an optimal solution to P10 with $P _ { i } = P _ { \operatorname* { m a x } } ^ { s ( i ) }$ Â¼ Z Z. The upper bound of $C ^ { * }$ is as follows

$$
C _ { \mathrm { m a x } } = \sum _ { i \in \mathcal { T } _ { 1 } } \left( p _ { i h _ { 3 } ^ { * } } + \sum _ { j \prec _ { h _ { 3 } ^ { * } } i } p _ { j h _ { 3 } ^ { * } } \right) + \sum _ { i \in \mathcal { T } _ { 2 } } \left( p _ { i h _ { 4 } ^ { * } } + \sum _ { j \prec _ { h _ { 4 } ^ { * } } i } p _ { j h _ { 4 } ^ { * } } \right) .
$$

Proof. See Appendix H, available in the online supplemental material. â¡

As such, we can determine the values of $\mathcal { G }$ and according to the values of $\hat { E } _ { \mathrm { t o l } } ^ { * } , E _ { \mathrm { m a x } } , \hat { C } ^ { * }$ , and $C _ { \mathrm { m a x } } .$

## 4.2 Joint Power and Task Scheduling Optimization 4.2.1 Approximation Algorithm with Performance Guarantee for Low-SNR SGLs

The SAGIN is a kind of digital communication systems, and thus may operate in the power-limited regime $( \mathrm { i . e . , S N R \ll 1 } )$ [42]. As such, in this subsection we aim to obtain an approximation solution to P0 with performance guarantee for the scenarios of low-SNR SGLs, i.e., SNR 1, where SNR is defined as (1). Specifically, we first explore the special structure of P0 to obtain an optimal solution to power allocation. Then, we further obtain our solution by utilizing BEM-FPA to directly solve P0 with the given optimal power allocation.

We start with the following theorem:

Theorem 9. For low-SNR SGLs, the global optimal power to P0 is the maximum transmit power, i.e., $P _ { i } ^ { * } = \dot { P } _ { \operatorname* { m a x } } ^ { s ( i ) } , \forall i .$

Lemma 2. For any task , the energy consumption $E _ { i }$ associated i Eiwith either a low-SNR SGL or any ISL is independent of the transmit power $P _ { i }$

Proof. See Appendix I, available in the online supplemental   
material. â¡

Proof of Theorem 9. See Appendix J, available in the online supplemental material. â¡

Algorithm 2. Balanced Energy and Makespan (BEM)   
Input: Set $\xi = \textstyle { \frac { 1 } { 2 } }$ , generation number $N ,$ population size .   
1:  Â¼ Produce an initial population $\mathcal { P } = \mathbf { \bar { \{ } }  \mathcal { P } _ { u } , 1 \leq u \leq U \}$ in a   
random manner.   
2: while $1 \leq n \leq N$ do   
3: for $u = 1 : U$ Ndo   
4: u Â¼ Map $\mathcal { P } _ { u }$ Uinto a candidate solution $P .$   
5: Pufor 1 : do   
6: if $h ( s ( i ) ) \in \mathcal { H } _ { 1 }$ then   
7: hÃ°sLet $P _ { i } = P _ { \operatorname* { m a x } } ^ { s ( i ) }$   
8: Pend if   
9: end for   
10: Call BEM-FPA $( \mathrm { i . e . , }$ Algorithm 1) to obtain the fitness   
value by using the new candidate solution .   
11: Update $\mathcal { P } _ { u } .$   
12: end for   
13: Execute the bio-inspired operations on [43].   
14: $n = n + 1$   
15: n Â¼ n Ã¾end while   
16: Map the best chromosome into ${ \mathbf { } } P .$   
Output: .

It follows from Theorem 9 that we can set $P ^ { * } = \{ P _ { \operatorname* { m a x } } ^ { s ( i ) } \}$ P Â¼ fand equivalently transform P0 into the following form

$$
\begin{array} { l } { { \displaystyle { \bf P 1 2 } \colon \operatorname* { m i n } _ { x , P ^ { * } } \mathcal { G } \sum _ { i \in \mathcal { I } } \sum _ { h \in \mathcal { H } } \quad x _ { i h t } ( t + p _ { i h } - 1 ) } } \\ { ~ } \\ { { \displaystyle t \in \mathcal { F } ( i , h ) } } \\ { { \quad + \quad \frac { 1 - \lambda } { E _ { \mathrm { m a x } } - E _ { \mathrm { t o n } } ^ { * } } E _ { \mathrm { c o n } } - \mathcal { U } } } \\ { { \mathrm { s . t . ~ } ( 7 ) - ( 9 ) , } } \\ { { \displaystyle \qquad ( 1 1 ) - ( 1 3 ) . } } \end{array}\tag{26}
$$

Here

$$
\begin{array} { r } { p _ { i h } = \left\{ \begin{array} { r l r } { \frac { D _ { i } N } { P _ { \mathrm { m a x } } ^ { s ( i ) } G _ { s ( i ) } ^ { \mathrm { t r a n } } G _ { h } ^ { \mathrm { r e c } } L _ { f } L _ { l } B _ { c } \mathrm { l o g } _ { 2 } e } , } & { } & { h \in \mathcal { H } _ { 1 } , } \\ { \frac { D _ { i } \kappa T _ { s } \left( E _ { b } / N _ { 0 } \right) _ { \mathrm { r e q } } M } { P _ { \mathrm { m a x } } ^ { s ( i ) } G _ { s ( i ) } ^ { \mathrm { t r a n } } G _ { h } ^ { \mathrm { r e c } } L _ { f } L _ { l } } , } & { } & { h \in \mathcal { H } _ { 2 } , } \end{array} \right. } \end{array}
$$

and

$$
\begin{array} { r } { E _ { \mathrm { c o n } } = \displaystyle \sum _ { i \in \mathcal { T } _ { 1 } } \frac { D _ { i } N } { G _ { s ( i ) } ^ { \mathrm { t r a n } } G _ { h } ^ { \mathrm { t r e c } } L _ { f } L _ { l } B _ { c } \log _ { 2 } e } } \\ { + \displaystyle \sum _ { i \in \mathcal { T } _ { 2 } } \frac { D _ { i } \kappa T _ { s } ( E _ { b } / N _ { 0 } ) _ { \mathrm { r e q } } M } { G _ { s ( i ) } ^ { \mathrm { t r a n } } G _ { h } ^ { \mathrm { r e c } } L _ { f } L _ { l } } . } \end{array}
$$

We can remove both the constant coefficient and the constant term $\begin{array} { r } { \frac { 1 - \lambda } { E _ { \mathrm { m a x } } - E _ { \mathrm { t } \mathrm { o l } } ^ { * } } E _ { \mathrm { c o n } } - \mathcal { U } } \end{array}$ Gfrom the objective function of P12 E E without losing optimality. We observe that this has the same form as P2. As such, we can directly call BEM-FPA to solve P12 to obtain a 1 -approximate solution with given $P _ { i } = P _ { \operatorname* { m a x } } ^ { s ( i ) } , \forall i$

## 4.2.2 Heuristic Algorithm for the Scenarios with Moderate to High-SNR SGLs

For the scenarios with moderate to high-SNR SGLs, solving the problem of balancing the minimum total energy consumption and mean makespan by joint task scheduling and power control is more difficult. The main challenge is in finding an optimal power allocation for the SGLs. It is however observed that if the transmit power allocation to P0 is fixed, it can be simplified to the scheduling problem of minimizing the mean makespan (i.e, P0fixed power), which can be solved efficiently by using Algorithm 1. Thus, in the proposed solution, we equivalently transform P0 into a nested problem with two levels of optimization. In the upper-level optimization, the master problem is to optimize transmit power by solving the following problem

$$
\begin{array} { r l r } & { \mathbf { P 1 3 : } \underset { P } { \mathrm { m i n } } g ( P ) } \\ & { \mathrm { s . t . } p _ { i h } = \frac { D _ { i } } { R _ { i h } ^ { \mathrm { S G L } } } , \forall i \in \mathcal { I } , h \in \mathcal { H } _ { 1 } , } & \\ & { } & { p _ { i h } = \frac { D _ { i } } { R _ { i h } ^ { \mathrm { I S L } } } , \forall i \in \mathcal { I } , h \in \mathcal { H } _ { 2 } , } & \\ & { } & { P _ { i } \in \mathcal { P } ^ { s ( i ) } , \forall i \in \mathcal { I } , } \end{array}
$$

where $\begin{array} { r } { \mathcal { P } ^ { s ( i ) } = \{ P _ { k } ^ { s ( i ) } | P _ { k } ^ { s ( i ) } = P _ { \operatorname* { m i n } } ^ { s ( i ) } + k \frac { P _ { \operatorname* { m a x } } ^ { s ( i ) } - P _ { \operatorname* { m i n } } ^ { s ( i ) } } { | \mathcal { P } ^ { s ( i ) } | } , k = } \end{array}$ $0 , 1 , \ldots , | \mathcal { P } ^ { s ( i ) } | - 1 \}$ Â¼and $g ( P )$ jPk Â¼ P Ã¾ k jPsÃ°iÃj ; k Â¼is the optimal objective value ;of $\mathbf { P 0 } ^ { \mathrm { f i x e d ~ p o w e r } }$ j  g gÃ°P Ãfor a given . In the lower-level optimization, Pwe optimize by solving P0fixed power.

xWe note that, by Lemma 2, the optimal power allocation for ISLs is still the maximum transmit power. As such, we rewrite P13 in the following form

$$
\begin{array} { r l } & { \mathrm { { \bf ~ P 1 4 } : ~ \displaystyle \operatorname* { m i n } _ { { \boldsymbol { P } } } ~ } g ( { \boldsymbol { P } } ) } \\ & { \mathrm { s . t . } p _ { i h } = \displaystyle \frac { D _ { i } } { R _ { i h } ^ { \mathrm { S G L } } } , \forall i \in { \cal T } , h \in \mathcal { H } _ { 1 } , } \\ & { p _ { i h } = \displaystyle \frac { D _ { i } } { R _ { i h } ^ { \mathrm { B G L } } } , \forall i \in { \cal T } , h \in \mathcal { H } _ { 2 } , } \\ & { P _ { i } = P _ { \mathrm { n a x } } ^ { \mathrm { s } ( i ) } , \forall i \in { \cal T } , h ( s ) \in \mathcal { H } _ { 1 } , } \\ & { P _ { i } \in \mathcal { P } ^ { s ( i ) } , \forall i \in { \cal T } , h ( s ) \in \mathcal { H } _ { 2 } . } \end{array}
$$

A genetic framework is adopted to solve P14. First, we represent a candidate solution to P14 $( \mathrm { i . e . , } P )$ as a chromosome. Then, we define $g ( P )$ Pas the fitness function to evaluate each gÃ°P Ãchromosome. Furthermore, we execute the bio-inspired operations involving mutation, crossover, and selection on these chromosomes. We omit these details here since they following a standard genetic framework [43]. In the following, we summarize the resultant BEM algorithm in Algorithm 2. The algorithm framework is illustrated in Fig. 4.

Next, we give Theorem 10 to state the complexity of the BEM algorithm.

<!-- image-->  
Fig. 4. Illustration for algorithm framework.

Theorem 10. The complexity of BEM is $\mathcal { O } ( U N ( I M ) ^ { 4 . 5 }$ log $( 1 / \epsilon ) )$

Proof. See Appendix $\mathrm { K } ,$ available in the online supplemental material. â¡

Finally, we analyse the convergence of two-layer algorithm BEM, which is composed of the outer-layer algorithm GA and the inner-layer algorithm BEM-FPA. In BEM-FPA, we utilize an interior-point method [44] to solve P10 . From [44], it is easy to obtain that BEM-FPA is linear convergence with ${ \mathcal { O } } ( \log \left( 1 / \epsilon \right) )$ . Furthermore, to analyse the convergence of $\mathrm { G A , }$ OÃ° Ã° =ÃÃwe utilize the result of [45], which is based on the minorization condition in the Markov chain theory. From [45], we obtain that $\| \mu _ { \alpha } - \pi \| \leq ( 1 - \delta ) ^ { \lfloor \alpha / \alpha _ { 0 } \rfloor }$ where $\mu _ { \alpha }$ represents the probabilk  k  Ã°  Ãity distribution of population at iteration a, p is the probability distribution, d denotes a positive constant with $0 < \delta < 1$ , a0 represents the first iteration, and $\lfloor \alpha / \alpha _ { 0 } \rfloor$ < <indicates the maximum integer less than or equal to a $/ \alpha _ { 0 }$ c. We let $\left( 1 - \delta \right) ^ { \lfloor \alpha / \alpha _ { 0 } \rfloor - 1 } \leq$ to yield that $\lfloor \alpha / \alpha _ { 0 } \rfloor \ge { \tilde { C } } { \bar { \log { ( 1 / \epsilon ) } } }$ =with $\begin{array} { r } { C = \frac { 1 } { \log \frac { 1 } { 1 \_ s } } > 0 } \end{array}$ . Using the fact that $\lfloor { \alpha } / { \alpha _ { 0 } } \rfloor \le { \alpha } / { \alpha _ { 0 } } ,$ we have $\alpha \geq \alpha _ { 0 } C \log ^ { \mathrm { ~ a ~ } / \epsilon } ( 1 / \epsilon )$ , which b = c  =  Cindicates GA is also linear convergence with ${ \mathcal { O } } ( \log \left( 1 / \epsilon \right) )$ . In OÃ° Ã° =ÃÃbrief, the convergence of BEM can be guaranteed, which is also verified in Fig. 7.

## 5 SIMULATION EVALUATION

In this section, we evaluate the performance of the proposed algorithms $( \mathrm { i . e . , }$ BEM-FPA and BEM) through extensive simulation. We aim to verify the performance of the proposed algorithms for low-SNR scenarios and high-SNR scenarios in term of feasibility, convergence, and effectiveness. We make comparison with a lower bound of the optimum in the low-SNR case, and with non-dominated sorting genetic algorithm-II (NSGA-II) [46], random power allocation, and random antenna allocation in the high-SNR case.

## 5.1 Parameters Setting

A co-simulation platform composed of the satellite tool kit and MATLAB is used to conduct our simulation. The related parameters are listed in Table 2. We consider the GEO backbone of SAGIN involving three DRSs. Each DRS is equipped with four receiver antennas. Half of the tasks are offloaded on ISLs and the other half are on SGLs. The data amount of each task is randomly generated from a uniform distribution in [5,15] Gbits. The scheduling horizon is from 1 September 2021

TABLE 2 Simulation Parameters
<table><tr><td>Data sinks</td><td>Latitude</td><td>Longitude</td></tr><tr><td>DRS 1</td><td> $0 ^ { \circ }$ </td><td> $4 1 ^ { \circ }$ </td></tr><tr><td>DRS 2</td><td> $0 ^ { \circ }$ </td><td> $1 7 4 ^ { \circ }$ </td></tr><tr><td>DRS 3</td><td> $0 ^ { \circ }$ </td><td> $2 7 5 ^ { \circ }$ </td></tr><tr><td> $L _ { f }$ </td><td> $1 0 ^ { - 2 3 }$ </td><td></td></tr><tr><td> $G _ { s ( i ) } ^ { \mathrm { t r a n } }$ </td><td> $3 6 \ : \mathrm { d B }$ </td><td></td></tr><tr><td> $G _ { h _ { 1 } } ^ { \mathrm { r e c } }$ </td><td>119.5894 dB</td><td></td></tr><tr><td> $G _ { h _ { 2 } } ^ { \mathrm { r e c } }$ </td><td>117.9284 dB</td><td></td></tr><tr><td> $G _ { h _ { - } } ^ { \mathrm { r e c } }$  h3</td><td>116.2675 dB</td><td></td></tr><tr><td> $G _ { h _ { 4 } } ^ { \mathrm { r e c } }$ </td><td>114.6065 dB</td><td></td></tr><tr><td>Line loss of ISLs</td><td>-200 dB</td><td></td></tr><tr><td>Line loss of SGLs</td><td>-210 dB</td><td></td></tr><tr><td> $P _ { \operatorname* { m i n } } ^ { s ( i ) }$ </td><td>100 watts</td><td></td></tr><tr><td> $P _ { \mathrm { m a x } } ^ { s ( i ) }$ </td><td>200 watts</td><td></td></tr><tr><td> $T _ { s }$ </td><td>316.2278K</td><td></td></tr><tr><td> $L _ { l }$ </td><td>1</td><td></td></tr><tr><td> $( E _ { b } / N _ { 0 } )$ </td><td>9.6 dB</td><td></td></tr><tr><td> $M$ </td><td> $1 . 4 1 2 5 ~ \mathrm { d B }$ </td><td></td></tr><tr><td>K</td><td> $1 . 3 8 0 5 4 * 1 0 ^ { - 2 3 } ~ \mathrm { J K ^ { - 1 } }$ </td><td></td></tr></table>

00:00:00.0 to 2 September 2021 00:00:00.0. We solve P10 optimally by using YALMIP [47] to call the SeDuMi solver [48].

The parameters of GA are listed as follows: The mutation probability is set to 0.8; the crossover probability is set to 0.5; the population size is set to 30; The number of genetic generations is set to 100.

The different settings for the low-SNR scenarios and high-SNR scenarios are listed as follows: In low-SNR scenarios, we set $L _ { f } = 1 0 ^ { - 2 3 }$ to satisfy SNR  1. In high-SNR scenarios, $L _ { f }$ Lf Â¼is set to $1 0 ^ { - 2 1 }$

## 5.2 Performance Evaluation

## 5.2.1 Low-SNR Scenarios

In Figs. 5 and 6, we adopt the lower bound as a baseline to verify the performance gap between the optimum of P0fixed power and the BEM-FPA algorithm. To find a lower bound of optimum, we use YALMIP to call the solver SeDuMi to solve the semidefinite programming problem P10 optimally. We label the normalized weighted sum of total energy consumption and mean makespan as network cost.

In Fig. 5a, we compare BEM-FPA with the lower bound for different task number (TN) and antenna number (AN) in terms of the network cost versus . Furthermore, we obtain the total -energy consumption and mean makespan from the network cost in Fig. 5a and further plot them versus  in Figs. 5b and 5c.

-From Fig. 5a, we observe that the network cost increases as -increases. Meanwhile, from Figs. 5b and 5c, we observe that both total energy consumption and mean makespan remain constant with increasing . From Fig. 5b, we observe that total -energy consumption remains constant with increasing . This -corresponds with Lemma 2, i.e., the energy consumption for each task is not a function of its allocated transmit power in low-SNR scenarios. This illustrates that total energy consumption is fixed in low-SNR scenarios when both the number of tasks and the number of antennas are given. Moreover, Fig. 5b shows that total energy consumption increases as the number of antennas increases. This is because the gain of receiver antenna in the simulation is set to a decreasing value with increasing antenna number. To minimize the mean makespan, more tasks are scheduled when there are more receiver antennas. Equation (29) indicates that energy consumption increases as the gain of receiver antenna deceases. Thus, the total energy consumption increases as the number of antennas increases.

Fig. 5c shows that mean makespan is unchange with increasing . This is because when total energy consumption is -a fixed value in low-SNR scenarios, the studied problem degrades into a mean makespan minimization problem $( \mathrm { i . e . , }$ P1). This means that there is no tradoff between mean makespan and total energy consumption in low-SNR scenarios. Furthermore, it is observed from Fig. 5 that the performance gap between BEM-FPA and the lower bound is very small. In particular, the maximum performance gap to optimality is less than 2%, which suggests that BEM-FPA performs even better than what is predicted by the bound in Theorem 5. Since the optimum of P12 lies between BEM-FPA and the lower bound, we see that BEM-FPA is nearly optimal.

Fig. 6a compares BEM-FPA with the lower bound for different and the number of antennas in terms of the network cost -versus the number of tasks. Figs. 6b and 6c respectively plot total energy consumption and the mean makespan versus the number of tasks. We again observe from Fig. 6a that the performance of BEM-FPA is very close to that of the lower bound with the number of tasks increases. This further verifies the efficiency of BEM-FPA. From Fig. 6b, we observe that the total energy consumption increases as the number of tasks increase, which is expected. From Fig. 6c, the two designs with a smaller number of tasks or a larger number of antennas achieve a smaller mean makespan. This is because: when giving the number of antennas, the more tasks the larger their makespan; when giving the number of tasks, the tasks can be scheduled in advance on more antennas, thereby reducing their makespan. This phenomenon indicates that we can reduce the mean makespan by reducing task number or increasing antenna number, which is also expected.

## 5.2.2 High-SNR Scenarios

In Fig. 7, we show the convergence evolution of BEM with different values of  in terms of network cost, total energy con--sumption, and mean makespan. It is observed from Fig. 7a that BEM typically converges in a small number of iterations. Fig. 7b shows that BEM obtains a larger total energy consumption with a larger value of as the number of iterations grows. -In Fig. 7c, we observe that BEM achieves a smaller mean makespan with a larger value of  as the number of iterations grows. -The above observations reflect the tradeoff between the two objectives of minimizing total energy consumption and the makespan.

Fig. 8 shows the performance between BEM and various baseline schemes in terms of network cost, total energy consumption, and mean makespan. The three baseline schemes are NSGA-II, random power+BEM-FPA, and random. Specifically, under random power+BEM-FPA, we first allocate power $P _ { i } \in \mathcal { P } ^ { s ( i ) }$ for any task in a random fashion and then Pi 2 P iwe run BEM-FPA given the random power allocation. Under random, both the power and transmit antenna are randomly allocated for each task.

Fig. 8a shows NSGA-II achieves a smaller network cost than that of random. This because NSGA-II using bio-inspired on July 16,2024 at 03:06:40 UTC from IEEE Xplore. Restrictions apply.

<!-- image-->  
(a) Network cost versus å¥.

<!-- image-->  
(b) Total energy consumption versus å¥.

<!-- image-->  
(c) Mean makespan versus å¥.

Fig. 5. Comparisons with lower bound of optimum versus .  
<!-- image-->  
(a) Network cost versus task number.

<!-- image-->

<!-- image-->  
(b) Total energy consumption versus task (c) Mean makespan versus task number number.

Fig. 6. Comparisons with lower bound of optimum versus task number.  
<!-- image-->  
(a) Network cost versus iterations.

<!-- image-->  
(b) Total energy consumption versus iterations.

<!-- image-->  
(c) Mean makespan versus iterations.  
Fig. 7. Verification of convergence.

operations to yield some better solutions over multiple generations. One observes from Fig. 8a that the network cost obtained by random power+BEM-FPA is far less than that of NSGA-II. This is because our proposed BEM-FPA can achieve a smaller mean makespan than that of NSGA-II, which is reflected by Fig. 8c. This exhibits the efficiency of BEM-FPA. Furthermore, it is observed from Fig. 8a that BEM achieves the smallest network cost among all schemes. In particular, BEM can further decrease the network cost over random power+BEM-FPA although the performance gap between them is small. This indicates that optimizing power allocation is necessary for reducing the network cost. In Fig. 8b, we observe that BEM yields the smallest total energy consumption among all schemes over all values. Furthermore, Fig. 8c shows that -BEM yields a smaller mean makespan than random power +BEM-FPA. These demonstrate that the joint power control and task scheduling can not only decrease the total energy consumption but also reduce the mean makespan for SAGINs. In brief, by jointly optimizing power control and task scheduling, BEM can boost the performance of SAGINs.

## 6 CONCLUSION

In this paper, we have investigated the data offloading problem for SAGINs aiming to balance the total energy consumption and the mean makespan. We formulate this problem as a normalized weighted sum minimization problem under the practical constraints of data offloading and power control. We develop a constant-factor approximate algorithm termed BEM-FPA for the studied problem with given onJuly16,2024at03:06:40UTCfrom IEEE Xplore.Restrictionsapply.

<!-- image-->  
(a) Network cost versus å¥.

<!-- image-->  
(b) Total energy consumption versus å¥.

Fig. 8. Comparisons with alternatives.  
<!-- image-->  
(c) Mean makespan versus å¥.

power allocation, which is shown to be nearly optimal in simulation. We show that under low-SNR SGLs, BEM-FPA is directly applicable to the joint optimization problem, by allocating the maximum transmitting power for each task. Furthermore, to solve the problem for moderate to high-SNR SGLs, we devise a fast yet efficient data offloading algorithm termed BEM through combining BEM-FPA and a GA approach. Our simulation results exhibit that BEM is highly effective and superior to state-of-the-art solutions.

## REFERENCES

[1] N. Cheng et al., âSpace/aerial-assisted computing offloading for IoT applications: A learning-based approach,â IEEE J. Sel. Areas Commun., vol. 37, no. 5, pp. 1117â1129, May 2019.

[2] C. Zhou et al., âDeep reinforcement learning for delay-oriented iot task scheduling in sagin,â IEEE Trans. Wireless Commun., vol. 20, no. 2, pp. 911â925, Feb. 2021.

[3] K.-Y. Lam, S. Mitra, F. Gondesen, and X. Yi, âAnt-centric IoT security reference architecture-security-by-design for satellite-enabled smart cities,â IEEE Internet Things J., vol. 9, no. 8, pp. 5895â5908, Apr. 2021.

[4] S. Zhou, G. Wang, S. Zhang, Z. Niu, and X. S. Shen, âBidirectional mission offloading for agile space-air-ground integrated networks,â IEEE Wireless Commun., vol. 26, no. 2, pp. 38â45, Apr. 2019.

[5] J. Liu, Y. Shi, Z. M. Fadlullah, and N. Kato, âSpace-air-ground integrated network: A survey,â IEEE Commun. Surveys Tuts., vol. 20, no. 4, pp. 2714â2741, Fourth Quarter 2018.

[6] W. Huang, T. Song, and J. An, âQA2: QoS-Guaranteed access assistance for space-air-ground internet of vehicle networks,â IEEE Internet Things J., vol. 9, no. 8, pp. 5684â5695, Apr. 2021.

[7] J. Du, C. Jiang, Q. Guo, M. Guizani, and Y. Ren, âThe federated satellite systems paradigm: Concept and business case evaluation,â IEEE Wireless Commun., vol. 23, no. 2, pp. 136â144, 2016.

[8] âKeynote 2: IoT via 5G satellite systems,â in Proc. 16th Int. Conf. Telecommun., 2021, pp. 2â2.

[9] J. S. Ojo, E. O. Olurotimi, and O. O. Obiyemi, âAssessment of total attenuation and adaptive scheme for quality of service enhancement in tropical weather for satellite networks and 5G applications in Nigeria,â J. Microw. Optoelectron. Electromagn. Appl., vol. 20, no. 2, pp. 228â247, 2021.

[10] E. Setiawan, âThe potential use of high altitude platform station in rural telecommunication infrastructure,â in Proc. Proc. Int. Conf. ICT Rural Develop., 2018, pp. 35â37.

[11] X. Shen et al., âAi-assisted network-slicing based next-generation wireless networks,â IEEE Open J. Veh. Technol., vol. 1, pp. 45â66, 2020.

[12] F. Dong, Q. Liu, W. Zhang, L. Guo, and X. Zhou, âEnergy-efficient transmissions in integrated HAP/satellite networks for emergency communications,â in Proc. Int. Conf. Wireless Commun. Signal Process., 2015, pp. 1â5.

[13] F. Dong, M. Li, X. Gong, H. Li, and G. F., âDiversity performance analysis on multiple HAP networks,â Sensors, vol. 15, no. 7, pp. 15398â15418, 2015.

[14] H. Tsuchida et al., âEfficient power control for satellite-borne batteries using Q-Learning in low-earth-orbit satellite constellations,â IEEE Wireless Commun. Lett., vol. 9, no. 6, pp. 809â812, Jun. 2020.

[15] C. D. Lippitt, D. A. Stow, and L. L. Coulter, Time-Sensitive Remote Sensing, Berlin, Germany: Springer, 2015.

[16] W. E. Smith, âVarious optimizers for single-stage production,â Nav. Res. Logistics Quart., vol. 3, no. 1/2, pp. 59â66, 1956.

[17] R. Liu, M. Sheng, C. Xu, J. Li, X. Wang, and D. Zhou, âAntenna slewing time aware mission scheduling in space networks,â IEEE Commun. Lett., vol. 21, pp. 516â519, Mar. 2017.

[18] D. Zhou, M. Sheng, R. Liu, Y. Wang, and J. Li, âChannel-aware mission scheduling in broadband data relay satellite networks,â IEEE J. Sel. Areas Commun., vol. 36, no. 5, pp. 1052â1064, May 2018.

[19] X. Jia, T. Lv, F. He, and H. Huang, âCollaborative data downloading by using inter-satellite links in LEO satellite networks,â IEEE Trans. Wireless Commun., vol. 16, no. 3, pp. 1523â1532, Mar. 2017.

[20] B. Deng, C. Jiang, L. Kuang, S. Guo, J. Lu, and S. Zhao, âTwophase task scheduling in data relay satellite systems,â IEEE Trans. Veh. Technol., vol. 67, no. 2, pp. 1782â1793, Feb. 2018.

[21] X. Chen, X. Li, X. Wang, Q. Luo, and G. Wu, âTask scheduling method for data relay satellite network considering breakpoint transmission,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 844â857, Jan. 2021.

[22] C.-Q. Dai, C. Li, S. Fu, J. Zhao, and Q. Chen, âDynamic scheduling for emergency tasks in space data relay network,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 795â807, Jan. 2021.

[23] L. He, J. Li, M. Sheng, R. Liu, K. Guo, and D. Zhou, âDynamic scheduling of hybrid tasks with time windows in data relay satellite networks,â IEEE Trans. Veh. Technol., vol. 68, no. 5, pp. 4989â5004, May 2019.

[24] Z. Jia, M. Sheng, J. Li, D. Zhou, and Z. Han, âJoint HAP access and LEO satellite backhaul in 6G: Matching game-based approaches,â IEEE J. Sel. Areas Commun., vol. 39, no. 4, pp. 1147â1159, Apr. 2021.

[25] F. Dong, H. Li, X. Gong, Q. Liu, and J. Wang, âEnergy-efficient transmissions for remote wireless sensor networks: An integrated HAP/satellite architecture for emergency scenarios,â Sensors, vol. 15, no. 9, pp. 22 266â22 290, Sep. 2015.

[26] K. An, T. Liang, X. Yan, Y. Li, and X. Qiao, âPower allocation in land mobile satellite systems: An energy-efficient perspective,â IEEE Commun. Lett., vol. 22, no. 7, pp. 1374â1377, Jul. 2018.

[27] Z. Ji, S. Wu, C. Jiang, D. Hu, and W. Wang, âEnergy-efficient data offloading for multi-cell satellite-terrestrial networks,â IEEE Commun. Lett., vol. 24, no. 10, pp. 2265â2269, Oct. 2020.

[28] D. Zhou, M. Sheng, X. Wang, C. Xu, R. Liu, and J. Li, âMission aware contact plan design in resource-limited small satellite networks,â IEEE Trans. Commun., vol. 65, no. 6, pp. 2451â2466, Mar. 2017.

[29] K. Guo, R. Gao, W. Xia, and T. Q. S. Quek, âOnline learning based computation offloading in MEC systems with communication and computation dynamics,â IEEE Trans. Commun., vol. 69, no. 2, pp. 1147â1162, Feb. 2021.

[30] T. T. Vu, D. N. Nguyen, D. T. Hoang, E. Dutkiewicz, and T. V. Nguyen, âOptimal energy efficiency with delay constraints for multi-layer cooperative fog computing networks,â IEEE Trans. Commun., vol. 69, no. 6, pp. 3911â3929, Jun. 2021.

[31] A. Golkar and I. Lluch i Cruz, âThe federated satellite systems paradigm: Concept and business case evaluation,â Acta Astron., vol. 111, pp. 230â248, 2015.

[32] D. Zhou, M. Sheng, Y. Wang, J. Li, and Z. Han, âMachine learning-based resource allocation in satellite networks supporting internet of remote things,â IEEE Trans. Wireless Commun., vol. 20, no. 10, pp. 6606â6621, 2021.

[33] L. Enrico, H. Samuel, A. Andoh, G. Alessandro, and S. Roberto, âAutonomous trajectory optimisation for intelligent satellite systems and space traffic management,â Acta Astron., vol. 194, pp. 185â201, 2022.

[34] R. Marler and J. Arora, âSurvey of multi-objective optimization methods for engineering,â Struct. Multidisciplinary Optim., vol. 26, no. 6, pp. 369â395, Apr. 2004.

[35] C. Lin and B.-S. Chen, âAchieving pareto optimal power tracking control for interference limited wireless systems via multi-objective $H _ { 2 } / H _ { \infty }$ optimization,â IEEE Trans. Wireless Commun., vol. 12, H =H1no. 12, pp. 6154â6165, Dec. 2013.

[36] F. Marinelli, S. Nocella, F. Rossi, and S. Smriglio, âA Lagrangian heuristic for satellite range scheduling with resource constraints,â Comput. Oper. Res., vol. 38, no. 11, pp. 1572â1583, 2011.

[37] M. Skutella, âConvex quadratic and semidefinite programming relaxations in scheduling,â J. ACM, vol. 48, pp. 206â242, 2001.

[38] A. A. Ageev and M. I. Sviridenko, âPipage rounding: A new method of construting algorithms with proven performane guarantee,â J. Combinatorial Optim., vol. 8, no. 3, pp. 307â328, 2004.

[39] Space Network Usersâ Guide (SNUG), Rev. 10, National Aeronautics and Space Administration, Goddard Space Flight Center, Greenbelt, MD, USA, Aug. 2012. Accessed: Nov. 2016. [Online]. Available: http://esc.gsfc.nasa.gov/assets/files/450-SNUG.pdf

[40] J. Wang, âChinaâs data relay satellite system and its application prospect,â Spacecraft Eng., vol. 22, no. 1, pp. 1â6, 2013.

[41] F. Heine, G. Muhlnikel, H. Zech, S. Philipp May, and R. Meyer, âThe European Data Relay System, high speed laser based data links,â in Prof. 7th Adv. Satell. Multimedia Syst. Conf. 13th Signal Process. Space Commun. Workshop, 2014, pp. 284â286.

[42] L. Li, L. Sboui, Z. Rezki, and M.-S. Alouini, âOn the capacity of fading channels with peak and average power constraints at low SNR,â IEEE Trans. Veh. Technol., vol. 68, no. 1, pp. 93â100, Jan. 2019.

[43] J. H. Holland, Adaptation in Nature and Artificial Systems, 2nd ed., Cambridge, U.K.: MIT Press, 1992.

[44] C. Helmberg, F. Rendl, R. Vanderbei, and H. Wolkowicz, âAn interior-point method for semidefinite programming,â SIAM J. Optim., vol. 6, no. 2, pp. 342â361, 1996.

[45] J. He and L. Kang, âOn the convergence rate of genetic algorithms,â Theor. Comput. Sci., vol. 229, no. 1/2, pp. 23â39, 1999.

[46] I. M. Ali, K. M. Sallam, N. Moustafa, R. Chakraborty, M. J. Ryan, and K.-K. R. Choo, âAn automated task scheduling model using non-dominated sorting genetic algorithm II for Fog-cloud systems,â IEEE Trans. Cloud Comput., early access, Oct. 20, 2020, doi: 10.1109/TCC.2020.3032386.

[47] J. Lofberg, âYALMIP: A toolbox for modeling and optimization in MATLAB,â in Proc. IEEE Int. Conf. Robot. Automat., 2004, pp. 284â289.

[48] Y. Labit, D. Peaucelle, and D. Henrion, âSeDuMi interface 1.02: A tool for solving LMI problems with SeDuMi,â in Proc. IEEE Int. Symp. Comput. Aided Control Syst. Des., 2002, pp. 272â277.

[49] L. Shi, âScheduling to minimize total weighted completion time via time-indexed linear programming relaxations,â SIAM J. Compt., vol. 49, no. 4, pp. 1â32, Apr. 2020.

[50] Z. Q. Luo, W. K. Ma, A. M. C. So, Y. Ye, and S. Zhang, âSemidefinite relaxation of quadratic optimization problems,â IEEE Signal Process. Mag., vol. 27, no. 3, pp. 20â34, May 2010.

<!-- image-->

Lijun He (Member, IEEE) received the BS degree in electronic information science and technology from Anqing Normal University, Anhui, China, in 2013, and the PhD degree in military communications from the State Key Laboratory of ISN, Xidian University, Xiâan, China, in 2020. From September 2018 to September 2019, he was with the University of Toronto, Toronto, ON, Canada, as a visiting scholar funded by the China Scholarship Council (CSC). From June 2020 to July 2022, he was a post-doctoral researcher with the

School of Software, Northwestern Polytechnical University (NPU). He is currently a associate professor with the School of Software, NPU. His current research interests include routing, scheduling, resource allocation, and satellite communications.

<!-- image-->

Jiandong Li (Fellow, IEEE) received the BE, MS and PhD degrees in communications engineering from Xidian University, Xiâan, China, in 1982, 1985 and 1991, respectively. He has been a faculty member of the school of Telecommunications Engineering, Xidian University since 1985, where he is currently a professor and vice director of the academic committee of State Key Laboratory of Integrated Service Networks. He was a visiting professor with the Department of Electrical and Computer Engineering, Cornell University from

2002-2003. He served as the general vice chair for ChinaCom 2009 and TPC chair of IEEE ICCC 2013. He was awarded as distinguished young researcher from NSFC and changjiang scholar from Ministry of Education, China, respectively. His major research interests include wireless communication theory, cognitive radio and signal processing.

<!-- image-->

Yanting Wang (Member, IEEE) received the BS and PhD degrees in communication and information systems from Xidian University, in 2012 and 2019, respectively. She is currently an assistant professor with the School of Software, Northwestern Polytechnical University. Her research interests include computation offloading, caching, applications of convex optimization theory, and heterogeneous networks. She served as the Technical Program Committee member for IEEE VTC-2020.

<!-- image-->

Jiangbin Zheng received the BS, MS, and PhD degrees in computer science from Northwestern Polytechnical University, Xiâan, China, in 1993, 1996, and 2002, respectively. From 2000 to 2001 and 2002, he was a research assistant with The Hong Kong Polytechnic University, Hong Kong. From 2004 to 2005, he was a research assistant with The University of Sydney, Sydney, Australia. Since 2009, he has been a professor and PhD supervisor with the School of Computer Science, Northwestern Polytechnical University. He has authored or co-authored more than 100 peer-reviewed journal/conference papers covering a wide range of topics in image/video analytics, pattern recognition, machine learning and Big Data analytics. His research interests focus on intelligent information processing, visual computing, multimedia signal processing, big data, and software engineering.

<!-- image-->

Liang He (Member, IEEE) received the BS degree in automatic control, the MS degree in navigation guidance and control, and the PhD degree in control theory and control science from Harbin Institute of Technology, harbin, China, in 2000, 2002, and 2006, respectively. From December 2014 to June 2015, he was a research assistant with the Polytechnic University of Milan, Milan, Italy. He has been a professor and PhD supervisor with the School of software, Northwestern Polytechnical University and a pluralistic professor with the East

China University of Science and Technology. His research interests focus on intelligent information processing, intelligent unmanned system and product technology, satellite communications, wireless communication resource management.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/csdl.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp/page_7_img_1.jpeg|page_7_img_1]]
3. [[../extracted_images/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp/page_14_img_1.jpeg|page_14_img_1]]
4. [[../extracted_images/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp/page_14_img_2.jpeg|page_14_img_2]]
5. [[../extracted_images/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp/page_14_img_3.jpeg|page_14_img_3]]
6. [[../extracted_images/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp/page_14_img_4.jpeg|page_14_img_4]]
7. [[../extracted_images/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp/page_14_img_5.jpeg|page_14_img_5]]

---

