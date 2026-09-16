# Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assisted Disaster Relief Networks

Jinsong Gui , Member, IEEE, and Fujian Cai

AbstractâIn the disaster-hit areas where ground network infrastructure has been severely damaged, one challenging problem for multi-UAV-assisted disaster relief networks is how to improve the coverage probability of each UAV. On the basis of solving this problem, the second challenging problem is how to design a channel and power-beam allocation scheme to optimize system throughput while meeting spectrum-energy efficiency constraint. In this article, we first propose a new method for measuring single UAV coverage quality, which considers both the ratio of effective coverage time to single loop flight time and that of the ground terminals with effective coverage time to the total ground terminals. Then, we develop a set of new algorithms to take advantage of the uneven distribution of ground terminals, which can achieve the total coverage probability improvement and the reduction of deployment costs of UAVs. Finally, we formulate the second problem as Markov decision process (MDP) and develop a solution based on deep deterministic policy gradient (DDPG). Simulation results demonstrate the validity and superiority of our proposed solutions compared with other benchmark strategies in different perspectives.

Index TermsâDisaster relief network, coverage probability, throughput optimization, spectrum-energy efficiency.

## I. INTRODUCTION

V ARIOUS natural disasters have occurred in many coun-tries for a long time, causing enormous economic losses tries for a long time,causing enormous economic losses and even threatening peopleâs lives. The extent of such losses is exacerbated by the disruption to the spread of emergency information [1], [2]. In post-disaster areas, it is essential to establish communications between disaster management centers and victims/rescue-teams on the ground to facilitate the search and rescue operation [3]. Some traditional popular network architectures [4] can provide communication services in post-disaster areas, but they have the common or respective insuperable defects [5], [6], [7]. Specifically, terrestrial networks could be affected by disasters and extreme weather conditions, air-ground networks hardly connect affected and unaffected areas, and space-ground networks strictly require that all ground terminals have the ability to connect directly to satellites. By connecting the UAVs over the affected areas, the victims and rescuersâ wireless terminals, the land-based infrastructures in the unaffected areas, and the global low orbit satellites, the spaceair-ground integrated network (SAGIN) [8], [9] can overcome the deficiencies of the aforementioned networks.

<!-- image-->  
Fig. 1. Information delivering process in space-air-ground integrated disaster relief network.

As shown in Fig. 1, the satellite system collects and sends low-resolution photography and location information of disaster spots to the disaster management center. Then, the center makes the deployment decision of UAVs according to the information from the satellite system. With the help of UAVs, the center can obtain high-resolution photography of disaster spots. So the rescue scheme can be made and then transmitted to the UAVs from the disaster management center. Next, the UAV system continually scans disaster areas and collects more detailed information. Meanwhile, ground users will also actively request for medical supplies and report local disasters. Based on the collected information, the UAV system could precisely guide ground users for evacuation in one-to-one or one-to-many manner.

To sum up, two ways can be identified for UAVs to serve as many victims and rescue teams as possible in post-disaster areas. One is to deploy a large number of UAVs, and the other is to improve the ability of each UAV to cover ground terminals. Of course, the second way is more practical because resources are limited in post-disaster areas. The work in [10] is a typical example for coverage probability optimization in UAV-assisted disaster relief networks, which is concerned about the two UAV deployment scenarios. For a single static UAV scenario, there is a big gap in quality of experience between coverage-edge and coverage-center ground terminals. However, in a single mobile UAV scenario, the optimization of UAV flight path planning is extremely challenging. The authors in [11] are the first researchers to conduct the network coverage probability analysis in the dual-UAV-assisted emergency network (i.e., one is static and the other is moving). However, in order to better adapt to the stochastic movement of ground users in post-disaster areas, especially when secondary disasters occur, a single mobile UAV should have a high frequency of flight trajectory adjustment. This may result in extremely irregular trajectories, which makes it more challenging to properly plan the flight path of a single mobile UAV.

To cope with the above challenges, we consider deploying three or more UAVs (i.e., one hovering UAV and two or more cyclically flying UAVs) to both suppress the irregular tendency of flight path and adapt to the random mobility of ground users. However, in the case of uneven distribution of ground users, how to improve the coverage probability of each mobile UAV to its service area is an urgent problem to be solved. Furthermore, with the increasing number of UAVs in the air, the probability of multiple UAVs gathering in a small space also increases. In this case, co-channel interference may occur when different ground terminals attempt to simultaneously send data to different UAVs in channel multiplexing mode. If co-channel interference cannot be effectively reduced by adjusting transmission powers, channel resource allocation should be further considered for interference control [12], [13].

In addition, the authors of [11] introduced the concept of average channel access delay, where a transmission connection between an UAV and a ground terminal will be established only if this ground terminalâs associating time with this UAV exceeds the specified average channel access delay. That is, if this channel access delay increases and the duration of this ground terminal covered by this UAV is fixed, the data transmission time will decrease. In this case, the higher data transfer rate can compensate for the loss of data transmission time, and thus the desired amount of data that can be successfully transferred between them can be maintained. Towards this end, we will exploit the characteristics of millimeter wave (mmWave) communication technology to achieve a high-rate transmission. However, the alignment time overhead of mmWave beams needs to be strictly controlled below the threshold that the system can tolerate. Our main contributions are listed as follows.

1) We propose a new method to measure single UAV coverage quality. Since the distribution of ground terminals in post-disaster areas is very uneven, we consider the ratio of effective coverage time (detailed in Section III-C) of the UAV (making one horizontal circular flight) to its entire single circular flight time in the design of new measurement method. Also, the ratio of ground terminals with effective coverage time to the total ground terminals is considered in the design. Thus, its coverage probability definition is obviously different from that based on the ratio of areas.

2) We expand the number of UAVs from two to three or even more to better adapt to the stochastic movement of ground terminals, which aims to get the local optimal combination of different UAVsâ flight trajectory parameters. These parameters can be obtained by Algorithms 1â¼4 proposed in this paper, which can realize coverage probability optimization (CPO) under a cost-effective UAV deployment. Further, to utilize the ultra-high-rate transmission of mmWave technology and reduce its beam alignment overhead, we predict each UAVâs location information based on the CPO parameters and apply it in Algorithm 5.

3) We extend the application scenario from a single downlink mode to more communication modes to adapt to the characteristics of space-air-ground disaster relief networks, which may lead to co-channel interference in uplink unicast scenario. We aim to make the UAVs reuse the same set of radio channels as much as possible while meeting the spectrum-energy efficiency constraint to improve throughput. Because this goal cannot be achieved by only adjusting the transmission powers of ground terminals, we propose Algorithm 5 to obtain the minimum increment of the required channel resources and sub-optimal power-beam control results.

4) Simulation results show that our CPO scheme can improve multi-UAV-assisted network coverage quality under a cost-effective UAV deployment in the case of very uneven distribution of ground terminals, and our throughput optimization scheme meeting the spectrum-energy efficiency constraint can control the co-channel interference within a system tolerance limit by using the minimum number of the added channels.

The rest of this paper are organized as follows. In Section II, we review the relevant works on network coverage and throughput optimization. The system model and problem statement are described in Section III. The algorithms for solving the CPO problem and throughput optimization problem under spectrum-energy efficiency constraint are given in Section IV, where Algorithms 1â¼4 for solving the CPO problem are described in Sections IV-A, IV-B, IV-C, and IV-D and Algorithm 5 for solving the throughput optimization problem under spectrum-energy efficiency constraint is described in Section IV-E. Finally, we evaluate the simulation results in Section V and conclude this paper in Section VI.

## II. RELATED WORK

There are many existing works on overcoming various challenges in UAV-assisted wireless networks, where network coverage and throughput optimization are relevant to the topic of this paper. The authors in [10] explored them by using a single static UAV and a single mobile UAV, respectively. They derived an analytical framework for the coverage and data rate analysis. In [14], the authors conducted the three-dimensional (3D) space coverage analysis for a single UAV, and adopted a generalized Poisson multinomial distribution to model the discrete interference states in 3D space. The authors in [15] focused on joint optimization of a single UAV height and path-loss compensation factor to improve the user coverage in 3D space. The authors in [16] addressed the coverage optimization problem of one mobile UAV to improve the quality of service of cell-edge users instead of all users.

As mentioned before, the network with only one UAV could not perform well in disaster-relief scenarios. Therefore, some typical works considered the coverage problem of multi-UAVassisted networks [11], [17], [18], [19], [20], [21], [22], [23], [24]. The authors in [17] analyzed the coverage probability of a specific ground terminal to be served in a multi-UAV-assisted network. They adopted the random waypoint mobility and uniform mobility to characterize the movement process of each UAV in vertical and spatial directions, respectively. The authors in [18] focused on improving the coverage quality of mobile cellular terminals by deploying multiple UAVs, where the UAVs are not intended to cover all terminals. Through homogeneous Poisson point process analysis, the authors in [19] derived the UAV coverage probability in Terahertz networks. The authors in [20], [21] explored the network coverage quality improvement problem by deploying UAVs to act as base stations (BSs). They aim to minimize the average UAV-terminal distance while keeping the UAV-BSs connected to some nearby stationary BSs. The authors in [22], [23] analyzed the coverage performance of UAVs and provided the coverage probability expressions. The authors in [24] analyzed the coverage probability and data rate of an aerial user associated with an aerial-BS or terrestrial-BS according to average received signal strength.

Besides the above works, there are also more flexible solutions to the coverage optimization problem of multi-UAV-assisted networks [25], [26], [27], [28]. The authors in [25] aimed to minimize the number of required UAVs and improve the coverage rate by optimizing 3D positions of UAVs, user clustering, and frequency band allocation, while the authors in [26] aimed to achieve considerable coverage and throughput by leveraging a fractional frequency reuse scheme and optimizing the cell partitions. However, they do not use multiple mobile UAVs and flight path planning. In [27], all the deployed UAVs were just fixed at their locations to cover all the ground devices. As the number of devices increases, so should the number of deployed UAVs to achieve full coverage. The authors in [28] addressed the UAV deployment and association problem based on statistical user position instead of instantaneous user position.

Even though some existing works [29], [30], [31] concerned about multi-mobile-UAV deployment, these works are not suitable for disaster relief networks. The authors in [29] addressed the improving problem of the capacity and coverage of cellular networks by deploying multiple tethered UAVs. The tethered UAVs rely on ground charging stations, so they are likely to be damaged in the worst-hit post-disaster areas. In [30], the authors investigated the optimal 3D placement for a UAV swarm with an attempt to solve 3D irregular terrain surface coverage problem. However, the goal is not to achieve the cost-efficient coverage (e.g., the smallest number of UAVs). The authors in [31] aimed to achieve 3D communication coverage in a UAV-assisted network by only deploying multiple UAVs over the coverage holes of ground BSs.

Based on the above, although the multi-mobile-UAV assisted coverage optimization problem has made a certain breakthrough, it is still being ignored how to improve the coverage probability of a single mobile UAV. How to deploy UAVs at low cost while improving network coverage quality remains a challenge. Multi-static-UAV deployment either hardly achieves seamless coverage or creates too much overlapping coverage. Due to the complex collaborative path planning challenge, Multi-mobile-UAV deployment makes seamless coverage achievement more difficult. Therefore, the existing UAV path planning methods are difficult to adapt to the stochastic movement of ground users in disaster areas.

In fact, it is scalable to design UAV-assisted network coverage schemes for disaster relief networks by combining a static UAV with multiple mobile UAVs. It neatly sidesteps the challenge of designing complex UAV flight paths to accommodate the stochastic movement of ground users. This is because, the static UAV deployed in the area with the densest ground users forms an approximate circular coverage area, and each mobile UAV is suitable for forming a ring coverage area to make a seamless splice with the circular coverage area. In addition, the users outside the circular coverage area can be logically merged if they are relatively scattered, which is convenient for each mobile UAV to improve coverage probability by only focusing on a small number of target areas.

To our best knowledge, the authors in [11] made the first exploration in this regard. However, they did not take advantage of the highly uneven distribution of ground users in disaster areas to improve single UAV coverage quality. Moreover, their coverage probability definition based on the ratio of areas fundamentally hinders the realization of this goal. In addition, when expanding the one-static-one-mobile-UAV networking model in [11] to one-static-multi-mobile-UAV networking model, we will face the problem of how to effectively divide the appropriate coverage task area of each mobile UAV. Meanwhile, the throughput optimization problem with the spectrum-energy efficiency constraint is rarely involved in the existing works that are relevant to this paper. Therefore, it is also a challenge for ground terminals to utilize valuable UAV coverage time and other available resources to achieve this goal. The above challenges inspired the exploration of this paper.

## III. SYSTEM MODEL AND PROBLEM STATEMENT

## A. Network Architecture

To facilitate the analysis of CPO problem and throughput optimization problem, we simplify the SAGIN in this paper. As shown in Fig. 2, it mainly includes one hovering master UAV (MUAV), a certain number (denoted by $\mathcal { N } _ { \mathrm { s } } =$ $\{ 1 , \ldots , n , \ldots , | \mathcal { N } _ { s } | \} )$ of mobile slave UAVs (SUAVs), and a large number (denoted by $\mathcal { N } _ { u } = \{ 1 , . . . , k , . . . , | \mathcal { N } _ { u } | \} )$ of ground user stations (GSTAs). Specifically, the MUAV denoted by m, with a fixed circular coverage range on the ground, is deployed over the center of affected area, while anyone of the ${ \mathrm { S U A V s } } ,$ with a mobile oval-like coverage range (see Fig. 2) on the ground, is flying around the MUAV in a horizontal circular flight path. We assume that the MUAVâs position is indicated as $( x _ { m } , y _ { m } , z _ { m } )$ . Due to the mobility of SUAVs, we denote the position of any SUAV n as $( x _ { n } ( t ) , y _ { n } ( t ) , z _ { n } ( t ) ) ^ { 1 }$ , where $t \in \Lambda = \{ 1 , . . . , T \}$ , t is the index variable of time slices with equal length $L _ { z }$ , and T is the total number of time slices.

<!-- image-->  
Fig. 2. Network architecture and coverage areas for UAVs.

The time slice length $L _ { z }$ is determined according to the node movement frequency, which is inversely correlated with the movement frequency of nodes in order to ensure that the position of the most frequently moved node is basically unchanged during a time slice. Also, due to the possible mobility of GSTAs, we denote the position during time slice t of any GSTA k as $( x _ { k } ( t )$ ï¼ $y _ { k } ( t ) , z _ { k } ( t ) )$ . Taking one MUAV and two SUAVs for an example, we use $R _ { m } ^ { c } , R _ { n } ^ { c }$ and $R _ { n } ^ { c }$ to denote the real-time coverage radius of MUAV $m ,$ SUAV n and SUAV n\`respectively, and adopt $R _ { n } ^ { f }$ and $R _ { n } ^ { f }$ to denote the flight trajectory radius of SUAV n and SUAV n\`respectively. In addition, $R ^ { G }$ refers to the radius of the whole disaster area.

With the continuous progress of wireless communication chip technology and the continuous reduction of manufacturing cost, it will be common for all radio advices to equipped with multiple cellular interfaces. Therefore, it is reasonable to assume that all the UAVs and GSTAs have both mmWave and sub-6 GHz cellular interfaces. In the deploying scenario shown in Fig. 2, these UAVs and GSTAs can always communicate with each other in sub-6 GHz frequency band while they can communicate with each other in mmWave frequency band only when their communication distances are within a limited range. All the GSTAs can periodically send their location coordinates (e.g., send once per the interval $L _ { z } )$ to the MUAV via their cellular interfaces in sub-6 GHz frequency band. In this paper, we assume that sub-6 GHz frequency band is only used in the transmission of control information, while mmWave frequency band is used to transmit user data.

## B. Air-to-Ground Mmwave Channel Model

For a mmWave frequency band in air-to-ground (A2G) communications, we adopt the widely used switch-based analog beam pattern described in [32], [33] to evaluate the normalized beamforming gain as follows.

$$
g \left( \varphi , \vartheta \right) = \left\{ \begin{array} { l l } { \frac { 2 \pi - ( 2 \pi - \varphi ) \epsilon } { \varphi } , } & { i f \ \left| \vartheta \right| \leq \frac { \varphi } { 2 } } \\ { \epsilon , } & { o t h e r w i s e } \end{array} \right.\tag{1}
$$

where $\varphi$ and $\vartheta$ are the main lobe beam width in radian and the beam offset angle to the main lobe in radian respectively, and  is a small positive number representing the side lobe gain. Due to the high line-of-sight (LoS) probability of A2G links, the directional transmitting gain $g _ { i , j } ^ { t }$ and the directional receiving gain $g _ { i , j } ^ { r }$ between node i and node j in the case of beam alignment can be estimated by

$$
\left\{ \begin{array} { l l } { g _ { i , j } ^ { t } = \frac { 2 \pi - \left( 2 \pi - \varphi _ { i , j } ^ { t } \right) \epsilon } { \varphi _ { i , j } ^ { t } } } & { ( 2 a ) } \\ { g _ { i , j } ^ { r } = \frac { 2 \pi - \left( 2 \pi - \varphi _ { i , j } ^ { r } \right) \epsilon } { \varphi _ { i , j } ^ { r } } } & { ( 2 b ) } \end{array} \right.\tag{2}
$$

where $\varphi _ { i , j } ^ { t }$ and $\varphi _ { i , j } ^ { r }$ are the beam width of the transmitter and the beam width of the receiver, respectively. Also, the mmWave channel gain model [34] in the case of LoS condition is considered in this paper, which is given by

$$
g _ { i , j } ^ { c } = \left| \chi _ { i , j } ^ { c } \delta \left( \tau - \tau _ { i , j } \right) \right| ^ { 2 }\tag{3}
$$

where $\chi _ { i , j } ^ { c }$ is the amplitude of LoS path between node i and node $j , \delta ( \cdot )$ is the Dirac delta function, and $\tau _ { i , j }$ is the propagation delay of LoS path between node i and node j. The parameters $\chi _ { i , j } ^ { c }$ and $\tau _ { i , j }$ are evaluated as follows [35].

$$
\left\{ \begin{array} { l l } { \chi _ { i , j } ^ { c } = \frac { c } { 4 \pi f _ { c } d _ { i , j } } } \\ { \tau _ { i , j } = \frac { d _ { i , j } } { c } } \end{array} \right.\tag{4a}
$$

(4b)

(4)

where $d _ { i , j }$ is the distance of LoS path between node i and node $j ,$ c is the speed of light, and $f _ { c }$ is the carrier frequency. Let $p _ { i , j } ^ { t }$ be the directional beamâs transmission power from node $j$ to node $i ,$ the received power $p _ { i , j } ^ { r }$ from node j to node i can be evaluated by

$$
p _ { i , j } ^ { r } = p _ { i , j } ^ { t } g _ { i , j } ^ { t } g _ { i , j } ^ { r } g _ { i , j } ^ { c }\tag{5}
$$

According to the Formulas (2)â¼(5) and the fact that the parameter  is a small positive number, we can get the estimation formula of mmWave A2G link signal propagation as follows.

$$
p _ { i , j } ^ { r } = \frac { p _ { i , j } ^ { t } } { 4 \varphi _ { i , j } ^ { t } \varphi _ { i , j } ^ { r } } \bigg ( \frac { c } { f _ { c } d _ { i , j } } \bigg ) ^ { 2 } , \ i \in \mathcal { N } _ { u } , \ j = m o r \ j \in \mathcal { N } _ { s }\tag{6}
$$

## C. UAV Association and Link Establishment

Based on the above network architecture, we assume that all the GSTAs aspire to communicate with any other network through the satellite Internet. Meanwhile, each UAV only connects to the GSTAs in a given finite area, and it sends a pilot signal to them to test the quality of A2G links. A GSTA can perceive the availability of downward communication if the signal strength from the UAV is more than a threshold Î².

For simplicity without loss of generality, we only consider the vertical ground-facing beam direction of each UAV for communication with the GSTAs in mmWave frequency band, and assume that each GSTA can be beamaligned with its associated UAV. At this time, if the signal strength received by a GSTA is greater than a signal strength threshold Î², there is downward communication from this UAV to this GSTA. Therefore, we can find each UAVâs maximum LoS mmWave communication range according to the Formula (6). For any UAV j, where $j \in \mathcal { N } _ { \mathrm { s } } \cup \{ m \}$ , if GSTA k is covered by it, we have

$$
\frac { p _ { j } ^ { t , m a x } } { 4 \varphi _ { k , j } ^ { t } \varphi _ { k , j } ^ { r } } \bigg ( \frac { c } { f _ { c } d _ { k , j } \left( t \right) } \bigg ) ^ { 2 } \geq \beta\tag{7}
$$

where $p _ { j } ^ { t , m a x }$ is the maximum transmission power of UAV j to all the GSTAs covered by it and $d _ { k , j } ( t ) =$ $\sqrt { \left( R _ { k , j } ( t ) \right) ^ { 2 } + \left( H _ { k , j } ( t ) \right) ^ { 2 } }$ in the distance between GSTA k and UAV j during time slice t. $R _ { k , j } ( t )$ is the length of the horizontal projection of $d _ { k , j } ( t )$ while $H _ { k , j } ( t )$ is the hovering/flight height of UAV j relative to GSTA k at time slice t. They are expressed by (8a) and (8b), respectively.

$$
\left\{ { R } _ { k , j } \left( t \right) = \sqrt { \left( x _ { j } \left( t \right) - x _ { k } \left( t \right) \right) ^ { 2 } + } \right.\tag{8a}
$$

(8)

(8b)

In fact, $d _ { k , j } ( t )$ is not more than UAV jâ maximum LoS mmWave communication range $d _ { k , j } ^ { m a x }$ . Here, $d _ { k , j } ^ { m a x }$ is expressed by

$$
d _ { k , j } ^ { m a x } = \frac { c } { f _ { c } } \sqrt { \frac { p _ { j } ^ { t , m a x } } { 4 \varphi _ { k , j } ^ { t } \varphi _ { k , j } ^ { r } \beta } }\tag{9}
$$

Since the vertical ground-facing beam direction of each UAV is used for communication, the maximum hovering/flight height of UAV j and the maximum ground distance of UAV j to GSTA k are expressed by

$$
\left\{ \begin{array} { l l } { H _ { k , j } ^ { m a x } = d _ { k , j } ^ { m a x } \cos \frac { \varphi _ { k , j } ^ { t } } { 2 } } \\ { R _ { k , j } ^ { m a x } = d _ { k , j } ^ { m a x } \sin \frac { \varphi _ { k , j } ^ { t } } { 2 } } \end{array} \right.\tag{10a}
$$

(10b)

(10)

In fact, the ground in the disaster area is likely to have very serious height differences. When the vertical ground-facing beam width of each UAV is fixed, the impact on the ground coverage is negligible. However, it still has an impact on the throughput under the fixed communication resources. In order to simplify the formula expression of UAV coverage radius, we assume that all the GSTAs are distributed on the same ground plane. Meanwhile, we also assume that the MUAV hovers horizontally and all the SUAVs fly horizontally all the time. Therefore, if $H _ { k , j } ( t )$ is regarded as the constant $H _ { j } \leq H _ { k , j } ^ { m a x } , R _ { k , j } ( t )$ must satisfy the following relation to ensure that UAV j can cover GSTA k.

$$
R _ { k , j } \left( t \right) \leq H _ { j } \tan \frac { \varphi _ { k , j } ^ { t } } { 2 }\tag{11}
$$

The coverage radius of UAV j during time slice t can be estimated by

$$
R _ { j } \left( t \right) = \operatorname* { m a x } _ { k \in \mathcal { N } _ { u } } \{ R _ { k , j } \left( t \right) \vert r e l a t i o n \ \left( 1 1 \right) \ i s \ m e t \}\tag{12}
$$

where $R _ { j } ( t ) = R _ { n } ^ { c } ( t )$ and $H _ { j } = H _ { n }$ if $j = n \in \mathcal { N } _ { \mathrm { s } }$ , and $R _ { j } ( t ) = R _ { m } ^ { c } ( t )$ and $H _ { j } = H _ { m } { \mathrm { i f } } j = m$ . Moreover, during time slice t, if the coverage radius is fixed as $R _ { j } ( t )$ , flight altitude is fixed as $H _ { j }$ , and transmission beam width of UAV j are fixed as $\varphi _ { j } ^ { t } ,$ , and reception beam width of each GSTA in its coverage area is also fixed as $\varphi _ { j } ^ { r }$ , we get the following relation according to (7).

$$
p _ { j } ^ { t , m i n } \left( t \right) = \frac { 4 \beta \varphi _ { j } ^ { t } \varphi _ { j } ^ { r } \left( f _ { c } \right) ^ { 2 } } { c ^ { 2 } } \left( \left( R _ { j } \left( t \right) \right) ^ { 2 } + \left( H _ { j } \right) ^ { 2 } \right)\tag{13}
$$

where $p _ { j } ^ { t , m i n } ( t )$ is the minimum transmission power of UAV j to all the GSTAs in its coverage area during time slice t, and the actual used transmission power ptj(t) is not less than $p _ { j } ^ { t , m i n } ( t )$ . In addition, $p _ { j } ^ { t , m i n } ( t ) = p _ { n } ^ { t , m i n } ( t ) \mathrm { i f } j = n \in \mathcal { N } _ { \mathrm { s } }$ , and $p _ { j } ^ { t , m i n } ( t ) =$ $p _ { m } ^ { t , m i n } ( t ) \bar { \mathrm { i f } } j = m$

We assume that an UAV can independently dispatch certain frequency resources, where the total available frequency resources can be evenly divided into C orthogonal channels so that the UAV can concurrently serve C GSTAs of its coverage range in its vertical ground-facing beam direction. We use ${ \mathbb C } = \{ c \} _ { c = 1 } ^ { C }$ to denote such available channel set and employ B to denote the bandwidth of each channel in the set C. All the other UAVs can reuse the set C as long as they are far enough apart to mitigate co-channel interference effects. Otherwise, an additional set of channels is required, which is denoted by the set CË . Specifically, each UAV first uses the channels in the set C to communicate with the GSTAs covered by it. If the co-channel interference value exceeds the threshold, the corresponding channel is replaced with one in the set CË . The specific replacement strategy is outside the scope of this paper due to the limited paper length.

We also assume that the maximum transmission power of each GSTA (e.g., k) in the coverage range of any UAV satisfies the following relation so that two-way communication can be achieved between this UAV and its associating GSTAs during time slice t.

$$
p _ { k } ^ { t , m a x } \left( t \right) \geq \operatorname* { m a x } _ { j \in \mathcal { N } _ { \mathrm { s } } \cup \left\{ m \right\} } \left\{ p _ { j } ^ { t , m i n } \left( t \right) \right\}\tag{14}
$$

While the MUAVâs coverage on the ground can be regarded as a static area, each SUAVâs coverage is a dynamically changing area. As described in [11], given a fixed circular trajectory with radius R and a constant speed V , each SUAVâs position repeats per the following interval.

$$
L _ { c } = { \frac { 2 \pi R } { V } }\tag{15}
$$

During $L _ { c }$ , the channel access delay $\tau _ { 0 }$ for each GSTA to build an effective connection with its corresponding SUAV cannot be ignored. However, according to the definition in [11], $\tau _ { 0 }$ is only the interval between the time when a GSTA enters into the corresponding SUAVâs coverage range and the time when the GSTA starts to send/receive the data packets to/from the SUAV. Therefore, to ensure the transmission time of a specified length of data, the interval $\tau _ { 0 }$ needs to be increased to $\tau _ { 1 }$ . As shown in Fig. 2, only the GSTAs located in the shadowing area keep connecting to the corresponding SUAV and successfully transmit a specified length of data all through the interval $\tau _ { 1 }$

During the interval $\tau _ { 1 }$ , each SUAV flies for a certain distance $( \tau _ { 1 } V )$ along its trajectory. Under this circumstance, we can find the coverage area of each SUAV during the interval $\tau _ { 1 }$ . From Fig. 2, we see that only the GSTAs located inside the shadowing area can establish full transmissions to the corresponding SUAV and successfully transmit a specified length of data. Obviously, the distances from each SUAV to the corresponding GSTAs on the ground are different and change with time. However, the GSTAs covered by each SUAV have the same data transmission time during the interval $\tau _ { 1 }$ if the channel access delay $\tau _ { 0 }$ for each GSTA is same. It is noted that the size of each SUAVâs coverage area on the ground depends on its flying speed $V ,$ , where the higher speed will lead to the smaller SUAVâs coverage area. As shown in Fig. 2, we can derive the central angle $\theta _ { n }$ (radian) for SUAV n flying along its circular trajectory radius $R _ { n } ^ { f }$ with a constant speed V during the interval $\tau _ { 1 }$ as

$$
\theta _ { n } = \frac { \tau _ { 1 } V } { R _ { n } ^ { f } }\tag{16}
$$

Obviously, we have the upper bound of the flight speed V for each SUAV as

$$
V < \operatorname* { m i n } _ { n \in \mathcal { N } _ { s } } \left\{ \frac { 2 R _ { n } ^ { f } } { \tau _ { 1 } } \arcsin \left( \frac { R _ { n } ^ { c } } { R _ { n } ^ { f } } \right) \right\}\tag{17}
$$

The position relation of UAV n in the starting point and ending point during the interval $\tau _ { 1 }$ (see the bottom of Fig. 2) briefly shows how to obtain the inequation (17). Here, UAV n just does not form a light-shadow area in the flight during the interval $\tau _ { 1 }$ . Meanwhile, the speed of UAV n at this time is at a critical value, which can be easily calculated by Right Angle relationship. When the speed of UAV $n$ is less than this critical value, it will form a light-shadow area during the interval $\tau _ { 1 }$ Moreover, if the inequation (17) is met, each UAV in $\mathcal { N } _ { s }$ forms a light-shadow area during the interval $\tau _ { 1 }$

The GSTAs located outside the light-shadowing area during the interval $\tau _ { 1 }$ do not have enough time to connect to their associated SUAVs. Therefore, the communication probability between them and each SUAV is zero. However, when each SUAV flies at a constant speed and meets the inequation (17), the probability that the GSTAs located in the light-shadowing area in Fig. 2 will get data transfer time with the time length no more than $( \tau _ { 1 } - \tau _ { 0 } )$ is estimated by

$$
P r _ { n } = \frac { V \left( \tau _ { 1 } - \tau _ { 0 } \right) } { 2 \pi R _ { n } ^ { f } } , \forall n \in \mathcal { N } _ { s }\tag{18}
$$

where $P r _ { n }$ denotes the probability that there is an opportunity to transmit data between SUAV n and its associating GSTAs. The intuitive meaning of the (18) is the ratio of the effective data transmission time $( \mathrm { i } . \mathrm { e } . , \tau _ { 1 } - \tau _ { 0 } )$ of the GSTAs in the lightshadow area to single circle flight time $( \mathrm { i . e . , } \frac { 2 \pi R _ { n } ^ { f } } { V } )$ of the UAV covering them. Since any GSTA in the light-shadow area has the same effective data transmission time, single circle flight time will directly affect the probability $P r _ { n }$

The SUAVs are usually deployed on the periphery of the MUAVâs coverage area to compensate for their inability to cover the area. Once the flight radius is determined, it is usually not changed unless the coverage area needs to be adjusted. Therefore, under such a case and the constraint of the relationships (17) and (18), the higher the flight speed V is, the greater the probability $P r _ { n }$ is. However, the light-shadowing area becomes smaller or even zero as the flight speed gets higher. Based on the above analysis, we can find that, under the assumption of uniform distribution of GSTAs, there is always a conflict between the improvement of the probability that any GSTA has an opportunity to transmit data and the increase of the number of the GSTAs that get the chance to transmit data. Fortunately, there is always an uneven distribution of GSTAs in disaster areas, which opens up the possibility of exploring a solution to the conflict.

## D. Single SUAV Coverage Quality Metric and Corresponding CPO Problem Statement

Take SUAV n for an example, we define the ratio of the number of the GSTAs covered by SUAV n in its single flight circle to the total number of GSTAs as $\mathcal { P } _ { n }$ . Therefore, we consider the improvement of $P r _ { n }$ and the increase of $\mathcal { P } _ { n }$ to define a new metric index, which is given as follows.

$$
S C Q _ { n } = \xi P r _ { n } + ( 1 - \xi ) \mathcal P _ { n }\tag{19}
$$

where $S C Q _ { n }$ means the coverage quality of SUAV n and $0 <$ $\xi < 1$ . As the foregoing, the MUAV can receive all the GSTAsâ location coordinates per the time length $L _ { z } ,$ , where $L _ { z }$ may be set based on the empirical value of GSTAsâ moving probability and it should be set to a smaller value if GSTAsâ moving probability is higher. Therefore, based on the recently collected GSTAsâ coordinates, the MUAV can use some kind of clustering algorithm to obtain the clusters of GSTAs that are usually discrete each other. These clusters are reasonably divided into the two groups, where the MUAV performs coverage task for a group while the SUAVs perform coverage task for another group. Each SUAV is responsible for coverage of partial clusters in the latter group. Take SUAV n for an example, the partial clusters it is responsible for is denoted by $\mathbb { Z } _ { n } = \left\{ \mathbb { Z } _ { n , 1 } , \ . . . , \mathbb { Z } _ { n , k } , . . . , \mathbb { Z } _ { n , K } \right\}$ , where K is the number of the clusters that are assigned to SUAV n for management.

Based on the obtained clusters of GSTAs, the MUAV adjusts its static coverage area and plans the circular flight trajectory for each SUAV. Take SUAV n for an example, according to the circular flight trajectory determined by the MUAV, it can adjust $R _ { n } ^ { c }$ and its flight speed $V$ for each cluster in its circular flight trajectory. SUAV n aims to make its light-shadowing area adapt to the size of each cluster in its ring-shaped service area. This ensures that the GSTAs in each cluster are covered in the light-shadowing area as much as possible. Also, SUAV n should speed up to enhance its average flight speed in the areas without any cluster. It aims to improve $P r _ { n }$ as much as possible by shortening flight time per single circular flight trajectory. Based on the new metric for single SUAV coverage quality, the CPO problem for all the SUAVs is described below.

$$
\left\{ \begin{array} { l l } { \mathbb { P } 1 : \displaystyle \operatorname* { m a x } _ { \cup _ { n \in \mathcal { N } _ { s } } \mathbb { Z } _ { n } } \sum _ { n \mathcal { N } _ { \mathrm { s } } } \frac { S C Q _ { n } } { | \mathcal { N } _ { s } | } } \\ { s . t . C 1 : \ 0 < P r _ { n } \leq 1 , \forall n \mathcal { N } _ { \mathrm { s } } } \\ { C 2 : \ 0 < \xi < 1 } \\ { C 3 : \ 0 < \mathcal { P } _ { n } \leq 1 , \forall n \mathcal { N } _ { \mathrm { s } } } \\ { C 4 : \displaystyle 0 < V \leq V ^ { m a x } } \\ { C 5 : \ { p } _ { n } ^ { t , m i n } \left( t \right) \leq p _ { n } ^ { t } \left( t \right) \leq p _ { n } ^ { t , m a x } , \forall \in \mathcal { N } _ { \mathrm { s } } } \end{array} \right.\tag{20}
$$

where $p _ { n } ^ { t } ( t )$ is the transmission power of SUAV n to all the GSTAs covered by it during time slice t. The constraint C1 aims to keep the probability within a reasonable range. The constraint C2 specifies the range of weight coefficient to accommodate both $P r _ { n }$ and $\mathcal { P } _ { n }$ . The constraint C3 will ensure that there must exist some GSTAs located in the light-shadowing area in Fig. 2. The constraint C4 will ensure that each SUAV meets the speed limit while the constraint C5 will ensure that it meets the power limit.

## E. Estimation Formulas for Interference, Throughput, and Spectrum-Energy Efficiency

When the width of the ring-shaped service area determined by the MUAV exceeds the width of single SUAVâs oval-like light-shadowing area, it will be subdivided by the MUAV into multiple ring-shaped sub-areas, and then assigned to multiple SUAVs to independently optimize the coverage probability of each sub-area. When the clustering area with large size is subdivided into different ring-shaped sub-areas, the SUAVs that are responsible for the covering tasks of these sub-areas may converge over this large clustering area at the same time. In the case, these SUAVs cannot reuse the same set of channel resources because co-channel interference exceeds the tolerable threshold of system performance. The above co-channel interference usually occurs in the uplink unicast scenario from GSTAs to SUAVs.

Taking the two concurrent mmWave links (e.g., k â n from GSTA k to SUAV n and k\`â n\`from GSTA k\`to SUAV n\`) for an example, the interference power received at SUAV n is estimated by

$$
p _ { \boldsymbol { k } , n } ^ { r } = p _ { \boldsymbol { k } , n } ^ { t } g _ { \boldsymbol { k } , n } ^ { t } g _ { \boldsymbol { k } , n } ^ { r } g _ { \boldsymbol { k } , n } ^ { c } g _ { \boldsymbol { k } , n } ^ { c }\tag{21}
$$

where $g _ { \boldsymbol { k } , n } ^ { t }$ and $g _ { \boldsymbol { k } , n } ^ { r }$ represent the directional transmission gain and directional reception gain of the link from GSTA k\` and SUAV n, respectively. In addition, let $\vartheta _ { \boldsymbol { k } , n } ^ { t }$ be the offset angle between GSTA k\`âs transmitting beam direction and the link from GSTA k\`to SUAV n, and also let $\vartheta _ { \boldsymbol { k } , n } ^ { r }$ be the offset angle between SUAV nâs receiving beam direction and the link to SUAV n from GSTA k\`. When $\begin{array} { r } { | \vartheta _ { \boldsymbol { k } , n } ^ { t } | \leq \frac { \varphi _ { \boldsymbol { k } , n } ^ { t } } { 2 } } \end{array}$ and $\begin{array} { r } { | \vartheta _ { \boldsymbol { k } , n } ^ { r } | \leq \frac { \varphi _ { k , n } ^ { r } } { 2 } } \end{array}$ , the beam of the interfering node (i.e., GSTA k\`) is aligned with the beam of the interfered node (i.e., SUAV n). According to the Formula (1), the directional transmission-reception gain of interference path in the case of beam alignment can be estimated by

$$
g _ { \boldsymbol { k } , n } ^ { t } g _ { \boldsymbol { k } , n } ^ { r } = \frac { 2 \pi - \left( 2 \pi - \varphi _ { \boldsymbol { k } , n } ^ { t } \right) \epsilon } { \varphi _ { \boldsymbol { k } , n } ^ { t } } \cdot \frac { 2 \pi - \left( 2 \pi - \varphi _ { \boldsymbol { k } , n } ^ { r } \right) \epsilon } { \varphi _ { \boldsymbol { k } , n } ^ { r } }\tag{22}
$$

We assume that any GSTA $( \mathrm { e . g . } , k \in \mathcal { N } _ { u } )$ can only connect to one SUAV $( \mathrm { e } . \mathrm { g } . , n \in \mathcal { N } _ { \mathrm { s } } )$ via only a channel $( \boldsymbol { \mathrm { e } } . \boldsymbol { \mathrm { g } } . , c \in \mathbb { C } )$ at a time in a UAV-assisted disaster relief network. Then, we set $x _ { k , n }$ as an integer variable to record the channel number of the mmWave link $k  n$ . Furthermore, we define a binary function $\varnothing ( \cdot )$ with single integer variable to indicate whether $x _ { k , n }$ holds a channel number, which is given by

$$
\begin{array} { r } { \varnothing \left( x _ { k , n } \right) = \left\{ \begin{array} { l l } { 1 , } & { x _ { k , n } \in C \cup \hat { \mathbb { C } } } \\ { 0 , } & { o t h e r w i s e } \end{array} \right. } \end{array}\tag{23}
$$

Also, we define a binary function $\varpi ( \cdot , \cdot )$ with double integer variables to indicate whether two links (e.g., k â n and $k  n )$ share the same channel, which is given by

$$
\begin{array} { r } { \varpi \left( x _ { k , n } , x _ { k , n } \right) = \left\{ \begin{array} { l l } { 1 , } & { x _ { k , n } = x _ { k , n } \in C \cup \hat { \mathbb { C } } } \\ { 0 , } & { o t h e r w i s e } \end{array} \right. } \end{array}\tag{24}
$$

For a mmWave link $( \mathrm { e . g . , } k \to n )$ , its signal-to-interference plus noise ratio (SINR) is denoted by $\gamma _ { k , n }$ , which can be estimated by

$$
\begin{array} { r } { \gamma _ { k , n } = \frac { \displaystyle \emptyset \left( x _ { k , n } \right) p _ { k , n } ^ { r } } { \sum _ { k \in \mathcal { N } _ { u } \backslash k } \sum _ { n \in \mathcal { N } _ { \mathrm { s } } \backslash n } \varpi \left( x _ { k , n } , x _ { k , n } \right) p _ { k , n } ^ { r } + B \cdot N _ { 0 } } } \end{array}\tag{25}
$$

where $N _ { 0 }$ is the power spectral density of background noise while $p _ { k , n } ^ { r }$ is the receiving power of SUAV n and estimated by the Formula (6). The throughput of mmWave link k â n is given by

$$
\mathcal { T } _ { k , n } = B \log _ { 2 } { ( 1 + \gamma _ { k , n } ) }\tag{26}
$$

The sum throughput of all the mmWave links from the nodes in $\mathcal { N } _ { u }$ to the nodes in $\mathcal { N } _ { \mathrm { s } }$ is estimated by

$$
\mathcal { T } _ { s u m } = \sum _ { k \in \mathcal { N } _ { u } } \sum _ { n \in \mathcal { N } _ { \mathrm { s } } } \mathcal { T } _ { k , n }\tag{27}
$$

The sum power consumption of all the mmWave links from the nodes in $\mathcal { N } _ { u }$ to the nodes in $\mathcal { N } _ { \mathrm { s } }$ is estimated by

$$
P _ { s u m } = \sum _ { k \in \mathcal { N } _ { u } } \sum _ { n \in \mathcal { N } _ { \mathrm { s } } } \emptyset \left( x _ { k , n } \right) \left( p _ { k , n } ^ { t } + P _ { R F } \right)\tag{28}
$$

where $P _ { R F }$ is the power consumption of an RF chain. The average system spectral-energy efficiency is estimated by

$$
S E E = \frac { \left| \mathbb { C } \right| } { \left| \mathbb { C } \right| + \Delta _ { c } } \frac { \mathcal { T } _ { s u m } } { P _ { s u m } \left| \mathbb { C } \right| B }\tag{29}
$$

where $\Delta _ { c }$ is the number of the channels taken from the set $\hat { \mathbb { C } }$ and $\Delta _ { c } \leq | \hat { \mathbb { C } } |$

## F. Throughput Optimization Problem Statement Under Spectrum-Energy Efficiency Constraint

The uplink co-channel interference can be reduced or even eliminated by adjusting the transmission powers of ground terminals and increasing the number of channels. We formulate the optimization problem aiming to maximize the system throughput under the spectrum-energy efficiency constraint, and then obtain a set of values of reasonable transmission power-beams for GSTAs and the necessary number of the new added channels by finding its approximate optimal solution. For this purpose, we described the throughput optimization problem under the spectrum-energy efficiency constraint as follows.

$$
\left\{ \begin{array} { l l } { \mathbb { P } ^ { 2 } : \displaystyle { \operatorname* { m a x } _ { N _ { u } , N _ { v } , \Omega , \hat { C } } } ^ { 2 } \mathbb { P } _ { s u m } } \\ { s . t . C 6 : 0 \in \mathcal { P } _ { k , n } ^ { \varepsilon } \leq p _ { k } ^ { t , m a x } , \forall k \mathcal { N } _ { u } , \forall n \mathcal { N } _ { s } } \\ { C ^ { 1 } : x _ { k , n } \in C \cup \{ \mathbb { C } , \forall k \mathcal { N } _ { u } , \forall n \mathcal { N } _ { s } } \\ { C \& \colon \Delta _ { c } \leq \left| \hat { C } \right| } \\ { C \mathbb { S } : 0 < \varphi _ { k , n } ^ { \varepsilon } \leq \varphi _ { n } ^ { m a x } , \forall k \mathcal { N } _ { u } , \forall n \mathcal { N } _ { s } } \\ { C \mathbb { 1 } 0 : \varphi _ { k , n } ^ { \varepsilon } = \varphi _ { n } ^ { m a x } , \forall k \mathcal { N } _ { u } , \forall n \mathcal { N } _ { s } } \\ { C \mathbb { 1 } : \displaystyle { \operatorname* { m a x } _ { s } \hat { \theta } \left( x _ { k , n } \right) } \leq 1 , \forall k \mathcal { N } _ { u } } \\ { C \mathbb { 1 } : \displaystyle { \operatorname* { m a x } _ { s \in \mathcal { N } _ { s } } \left( \langle x _ { k , n } \rangle \leq | \mathbb { C } | , \forall n \mathcal { N } _ { s } \right) } } \\ { C \mathbb { 1 } : \displaystyle { \operatorname* { m a x } _ { s \in E \in \mathcal { K } } S E } > S E E _ { h } } \end{array} \right.\tag{30}
$$

where $S E E _ { t h }$ is the low bound of the desired spectral-energy efficiency; the constraint C6 will ensure that each GSTA meets the power limit; the constraint C7 specifies the scope of reusable channel resources; the constraint C8 means that additional set of channels are only taken from the set $\hat { \mathbb { C } } ;$ the constraint C9 will ensure that the transmission beam width of a mmWave uplink $( \mathrm { e . g . } , k \to n )$ is more than 0 and no more than the maximum beam width $\varphi _ { n } ^ { m a x }$ of SUAV n, where $\varphi _ { n } ^ { m a x }$ vertically faces the ground and covers just the light-shaded area; the constraint C10 specifies that the receiving beam width of the uplink $k  n$ is equal to $\varphi _ { n } ^ { m a x }$ ; the constraint C11 will ensure that no GSTA can connect to more than one SUAV; the constraint C12 will ensure that each SUAV serves at most |C| GSTAs simultaneously; the constraint C13 means that the average system spectral-energy efficiency must be more than $S E E _ { t h }$ . Because each SUAV acting as a receiver in an uplink scenario is moving and needs to perform the coverage task, we specify that the receiving beam width and azimuth of each SUAV are constant to reduce the beam-alignment overhead.

## IV. THE PROPOSED ALGORITHMS FOR SOLVING OPTIMIZATION PROBLEMS

The solution to the problem P1 lays a foundation for solving the problem P2. However, as mentioned earlier, it may lead to the co-channel interference problem, which will be addressed in the problem P2. These two optimization problems are challenging because the problem P1 is non-convex and the problem P2 is both non-convex and combinatorial. For the problem P1, the optimization of $P r _ { n }$ and $\mathcal { P } _ { n }$ is usually in conflict with each other. However, there is the collaborative optimization chance in the case of uneven distribution of GSTAs, where the critical parameter is each SUAVâs flight speed. Unfortunately, even the approximate optimal solution to the problem P1 cannot be characterized by a single speed for each SUAV but by a set of speeds per SUAV, where the appropriate number of speeds per SUAV may depend on the heterogeneity of the distribution of GSTAs. Based on the above, the classical nonconvex optimization methods will be difficult to apply to the problem P1. We believe that it is feasible to cluster the GSTAs and describe each cluster, and then execute covering-task-area division and optimization based on distribution of clusters, which lays a foundation for designing a method to solve the problem P1. In addition, for the problem P2, Even if the classical nonconvex or combinatorial optimization methods can apply to it, they are difficult to meet the delay requirements of the application scenarios concerned in this paper. However, the trained deep reinforcement learning (DRL) model has almost negligible time costs in the decision-making phase, which can adapt to dynamic network environments. Therefore, we will propose DRL-based solution to the problem P2. In this section, we detail the corresponding algorithms for the formulated optimization problems.

<!-- image-->  
Fig. 3. Example of describing a cluster.

## A. Clustering GSTAs and Obtaining Description Parameters of Clusters

By the max-min-distance clustering algorithm, which has been widely used, we can get the cluster set Z for all the GSTAs when the position dataset $\mathbf { \hat { \mathbb { D } } } = \{ ( x _ { u } , y _ { u } ) \} _ { u = 1 } ^ { | \mathcal { N } _ { u } | }$ is available. For each cluster $( \mathrm { e . g . , ~ } \mathbb { Z } _ { z } \in \mathbb { Z } )$ , we define a quad of parameters $( \rho _ { z } ^ { l w } , \rho _ { z } ^ { u p } , \mathcal { R } _ { z } ^ { n a r } , \mathcal { R } _ { z } ^ { f a r } )$ to describe its shape. As shown in Fig. 3, they are based on a standard plane coordinate system with the MUAVâs coordinates $( x _ { m } , y _ { m } )$ as the origin.

The parameter $\mathcal { R } _ { z } ^ { n a r }$ represents the near boundary (unit in meter) of the cluster $\mathbb { Z } _ { z }$ while the parameter $\mathcal { R } _ { z } ^ { f a r }$ represents its far boundary. Also, the parameter $\rho _ { z } ^ { l w }$ represents the low edge of the cluster zz while the parameter $\rho _ { z } ^ { u p }$ represents its upper edge (unit in radian). For any pair of coordinates $( x _ { k } , y _ { k } )$ from $\mathbb { Z } _ { z } .$ , the angle $\rho _ { z }$ between the line from it to the origin of the coordinate system and the positive direction of X-axis can be computed by

$$
\begin{array} { r } { \left\{ a r c t a n \frac { \left| y _ { m } - y _ { k } \right| } { \left| x _ { m } - x _ { k } \right| } , x _ { k } > x _ { m } , y _ { k } > y _ { m } \right. } \end{array}\tag{31a}
$$

$$
\int \pi - a r c t a n { \frac { | y _ { m } - y _ { k } | } { | x _ { m } - x _ { k } | } } , \ x _ { k } \left. x _ { m } , \ y _ { k } \right. y _ { m }\tag{31b}
$$

$$
\begin{array} { r } { \rho _ { z } = \Big \{ \pi + a r c t a n { \frac { | { \bf x } _ { m } - { \bf x } _ { k } | } { | { \bf x } _ { m } - { \bf x } _ { k } | } } , ~ x _ { k } < x _ { m } , ~ y _ { k } < y _ { m } } \end{array}\tag{31c}
$$

$$
\begin{array} { r } { \Big \lfloor 2 \pi - a r c t a n { \frac { | y _ { m } - y _ { k } | } { | x _ { m } - x _ { k } | } } , \ x _ { k } > x _ { m } , y _ { k } < y _ { m } } \end{array}\tag{31d}
$$

(31)

The shape description parameters of each cluster can be obtained by Algorithm 1. Here, the lines 2â¼16 are responsible for picking out each cluster that spans both the first-quadrant and the fourth-quadrant from the set $\mathbb { Z } ,$ splitting it into the two clusters that belong to the first-quadrant and the fourthquadrant respectively, and keeping them in the set ZË . This is because the clusters that span both the first-quadrant and the fourth-quadrant cannot be described by a quad of parameters $( \rho _ { z } ^ { l w } , \rho _ { z } ^ { \bar { u p } } , \mathcal { R } _ { z } ^ { n a r } , \mathcal { R } _ { z } ^ { f a r } )$ , where $\rho _ { z } ^ { l w }$ and $\rho _ { z } ^ { u p }$ are computed according to the Formula (31). After updating the set $\mathbb { Z }$ with the set ${ \hat { \mathbb { Z } } } ,$ all the clusters the set $\mathbb { Z }$ can be described by a quad of parameters $( \rho _ { z } ^ { l w } , \rho _ { z } ^ { u p } , \mathcal { R } _ { z } ^ { n a r } , \mathcal { R } _ { z } ^ { f a r } )$ . Therefore, the lines 20â¼30 are responsible for iterating through each pair of coordinates in $\mathbb { Z } _ { z }$ to find $( \rho _ { z } ^ { l w } , \rho _ { z } ^ { u p } , \mathcal { R } _ { z } ^ { n a r } , \mathcal { R } _ { z } ^ { f a r } )$ .

## B. Covering-Task-Area Division Based on Distribution of Clusters

When the transmission beam width of the MUAV is fixed to $\varphi _ { m }$ , and the MUAV hovers at a fixed effective height $H _ { m }$ and adopts the maximum transmission power $p _ { m } ^ { t , m a x }$ , according to the relation (11), the MUAVâs maximum coverage radius $R _ { m } ^ { m a x }$ is estimated by

$$
R _ { m } ^ { m a x } = H _ { m } \tan \frac { \varphi _ { m } } { 2 }\tag{32}
$$

Also, for any SUAV (e.g., n) with the fixed transmission beam width $\varphi _ { n } .$ , when it flies at a fixed effective height $H _ { n }$ and adopts the maximum transmission power $p _ { n } ^ { t , m a x }$ , according to the relation (11), the SUAV nâs maximum coverage radius $R _ { n } ^ { m a x }$ is estimated by

$$
R _ { n } ^ { m a x } = H _ { n } \tan \frac { \varphi _ { n } } { 2 } \forall n \in \mathcal { N } _ { \mathrm { s } }\tag{33}
$$

In fact, $R _ { n } ^ { m a x }$ is the radius of the SUAV nâs static circular coverage area. Due to the movement characteristics of the each SUAV, the real coverage area will decrease as its speed increases. So we use the following formula to estimate the real coverage of each SUAV, which is used as a benchmark for dividing the covering-task-area for each SUAV.

$$
R _ { b h } = \operatorname* { m i n } \{ 2 \kappa R _ { n } ^ { m a x } | \forall n \in \mathcal { N } _ { \mathrm { s } } \}\tag{34}
$$

where $0 < \kappa < 1$ . Here the smaller coefficient Îº leads to the smaller area divided for each SUAV. In this case, the GSTAs are covered more fully, but more SUAVs are needed. The reasonable value for the coefficient Îº will be determined by the simulation experiments in Section V.

The covering-task-area division process is described in Algorithm 2. Here, the lines from 2 to 14 are responsible for dividing the covering-task-area for the MUAV, while the lines from 23 to 39 are responsible for dividing the covering-task-area cluster is divided into two different covering-task-areas (see the lines 9â¼11 and the lines 32â¼34). After determining the coverage area of the MUAV, the coverage area of the SUAVs can be estimated (see the lines 15â¼19) and the number of the necessary SUAVs can be further estimated (see the line 20). Also, after knowing the number of the necessary SUAVs, we can divide the covering-task-areas for them.

Algorithm 1: Obtaining Description Parameters of Clusters.   
Run at the MUAV   
Input: Cluster set Z and the MUAVâs coordinates $( x _ { m } , y _ { m } )$   
Output: $\cup _ { \mathbb { Z } _ { z } \in \mathbb { Z } } \{ ( \rho _ { z } ^ { l w } , \rho _ { z } ^ { u p } , \mathcal { R } _ { z } ^ { n a r } , \mathcal { R } _ { z } ^ { f a r } ) \}$   
$1 \colon { \hat { \mathbb { Z } } } = \varnothing$   
2: For $\mathbb { Z } _ { z } \in \mathbb { Z }$ do   
3: $x _ { m i n } = y _ { m i n } { = } \operatorname { I n f n i t y } ; x _ { m a x } = y _ { m a x } { = }$ Infinitesimal   
Number   
4: $\mathbb { z } _ { + + } = \varnothing ; \mathbb { z } _ { + - } = \varnothing$   
5: For $\forall ( x _ { k } , y _ { k } ) \in \mathbb { Z } _ { z }$ do   
6: $\textbf { I f } x _ { k } > ~ x _ { m a x }$ then $x _ { m a x } = x _ { k }$ End if   
7: $\mathbf { I f } \ y _ { k } > \ y _ { m a x }$ then $y _ { m a x } = y _ { k }$ End if   
8: $\mathbf { I f } \left( x _ { k } > x _ { m } \right) \land \left( y _ { k } > y _ { m } \right)$ then Add $( x _ { k } , y _ { k } )$ to   
$\mathbb { Z } _ { + + }$ End if   
9: ${ \bf { I f } } x _ { k } < x _ { m i n }$ then $x _ { m i n } = x _ { k }$ End if   
10: ${ \bf { I f } } y _ { k } < y _ { m i n }$ then $y _ { m i n } = y _ { k }$ End if   
11: $\mathbf { I f } \left( x _ { k } > x _ { m } \right) \land \left( y _ { k } < y _ { m } \right)$ then Add $( x _ { k } , y _ { k } )$ to   
$\mathbb { Z } _ { + - }$ End if   
12: End for   
13: ${ \bf I f } \left( x _ { m a x } > x _ { m } \right) \wedge \left( y _ { m a x } > y _ { m } \right) \wedge \left( x _ { m i n } > \right.$   
$x _ { m } ) \wedge ( y _ { m i n } < y _ { m } )$ then   
14: Remove $\mathbb { Z } _ { z }$ from $\mathbb { Z } ;$ Add $\mathbb { Z } _ { + + }$ and $\mathbb { Z } _ { + - }$ to $\hat { \mathbb { Z } }$   
15: End if   
16: End for   
17: $\mathbb { Z } = \mathbb { Z } \cup \hat { \mathbb { Z } }$   
18: For $\mathbb { Z } _ { z } \in \mathbb { Z }$ do   
19: $\rho _ { z } ^ { l w } = \mathcal { R } _ { z } ^ { n a r } =$ Infinity, $\rho _ { z } ^ { u p } = \mathcal { R } _ { z } ^ { f a r } =$ Infinitesimal   
Number   
20: For $\forall ( x _ { k } , y _ { k } ) \in \mathbb { Z } _ { z }$ do   
21: $\mathbf { I f } \ x _ { k } > x _ { m }$ and $y _ { k } > y _ { m }$ then Compute $\rho _ { z }$   
according to the Formula (31a) End if   
22: $\mathbf { I f } \ x _ { k } < x _ { m }$ m and y $y _ { k } > y _ { m }$ then Compute $\rho _ { z }$   
according to the Formula (31b) End if   
23: $\mathbf { I f } \ x _ { k } < x _ { m }$ and $y _ { k } < y _ { m }$ then Compute $\rho _ { z }$   
according to the Formula (31c) End if   
24: $\mathbf { I f } \ x _ { k } > x _ { m }$ and $y _ { k } < y _ { m }$ then Compute $\rho _ { z }$   
according to the Formula (31d) End if   
25: $\mathcal { R } _ { z } = \| ( x _ { m } , y _ { m } ) - ( x _ { k } , y _ { k } ) \|$   
26: If $\mathcal { R } _ { z } < \mathcal { R } _ { z } ^ { n a r }$ then $\mathcal { R } _ { z } ^ { n a r } = \mathcal { R } _ { z }$ End if   
27: If $\mathcal { R } _ { z } > \mathcal { R } _ { z } ^ { f a r }$ then $\mathcal { R } _ { z } ^ { f a r } = \mathcal { R } _ { z }$ End if   
28: If $\rho _ { z } < \rho _ { z } ^ { l w }$ then $\rho _ { z } ^ { l w } = \rho _ { z }$ End if   
29: If $\rho _ { z } > \rho _ { z } ^ { u p }$ then $\rho _ { z } ^ { u p } = \rho _ { z }$ End if   
30: End for   
31: Return $( \rho _ { z } ^ { l w } , \rho _ { z } ^ { u p } , \mathcal { R } _ { z } ^ { n a r } , \mathcal { R } _ { z } ^ { f a r } )$   
32: End for   
for each SUAV. The coefficient Î¶ in the line 6 and the lines   
29â¼31 represents the threshold of the proportion of a cluster   
area distributed in neighboring covering-task-areas, which aims   
to avoid producing very small clusters. If a small part of a cluster   
is distributed in the neighborhood, this part will not be divided   
into another separate covering-task-area. However, the GSTAs   
in this small part are allowed to logically merge in the same   
clusterâs covering-task-area in device-to-device (D2D) mode   
(see the lines $6 { \sim } 7$ and the lines 29â¼30). Otherwise, a large

<!-- image-->  
Fig. 4. Estimation of effective coverage area for a SUAV.

## C. Optimization for Covering-Task-Area

For a covering-task-area $( \boldsymbol { \mathrm { e . g . } } , \mathbb { Z } _ { \mathbb { k } } ^ { s } \in \mathbb { Z } ^ { t } ) .$ , when SUAV n is in charge of covering it, $\mathbb { Z } _ { \mathbb { k } } ^ { s }$ is rewritten as $\mathbb { Z } _ { n }$ for convenience. For a cluster $( \mathbf { e . g . , } \mathbb { Z } _ { n , k } \in \mathbb { Z } _ { n } )$ , we need to know how to build an effective SUAV coverage area that just matches this cluster area. That is, to form the shaded area with the shape parameters $( R _ { b h } , \boldsymbol { B _ { b h } } )$ in Fig. 4, how do we determine the flight speed $V _ { n , k }$ of SUAV n over cluster $\mathbb { Z } _ { n , k }$ when $R _ { n } ^ { c }$ and $R _ { n } ^ { f }$ are fixed?

Since $R _ { b h }$ can be determined based on the Formula (34) and it must be met, the angle $\theta _ { n , k }$ of SUAV n flying over cluster $\mathbb { Z } _ { n , k }$ along the path of radius $R _ { n } ^ { f }$ during the interval $\tau _ { 1 }$ is calculated by

$$
\theta _ { n , k } = 2 \arcsin \frac { \sqrt { \left( R _ { n } ^ { c } \right) ^ { 2 } - \left( \frac { R _ { b h } } { 2 } \right) ^ { 2 } } } { R _ { n } ^ { f } }\tag{35}
$$

Therefore, the corresponding flight speed $V _ { n , k }$ of SUAV n is calculated by

$$
V _ { n , k } = \frac { \theta _ { n , k } R _ { n } ^ { f } } { \tau _ { 1 } }\tag{36}
$$

In addition, we also need to know where SUAV n starts at flight speed $V _ { n , k } .$ . That is, how to determine the coordinates of $P O S _ { 1 }$ in Fig. 4. Since the trajectory radius $R _ { n } ^ { f }$ of SUAV n and the shape parameter $\rho _ { n , k } ^ { u p }$ of cluster $\mathbb { Z } _ { n , k }$ jointly determine the point a in Fig. 4, we take it as the reference point to get the coordinates $( \rho _ { n , k } ^ { s } , \mathcal { R } _ { n , k } ^ { s } )$ of POS1. Since $\mathcal { R } _ { n , k } ^ { s }$ is exactly $R _ { n } ^ { f } .$ , we just have to figure out $\rho _ { n , k } ^ { s }$ . Therefore, the following corollary exists.

Algorithm 2: Covering-Task-Area Division.   
Run at the MUAV   
Input: $\cup _ { \mathbb { Z } _ { z } \in \mathbb { Z } } \{ ( \rho _ { z } ^ { l w } , \rho _ { z } ^ { u p } , \mathcal { R } _ { z } ^ { n a r } , \mathcal { R } _ { z } ^ { f a r } ) \}$   
Output: $\mathbb { Z } ^ { m }$ and $\mathbb { Z } ^ { t }$   
1 $: \mathbb { Z } ^ { m } = \varnothing ; \mathbb { Z } ^ { s } = \varnothing$   
2: For $\forall \mathbb { Z } _ { z } \in \mathbb { Z } { \bf d o }$   
3: $\mathbf { I f } \ \mathcal { R } _ { z } ^ { f a r } < { R _ { m } ^ { m a x } }$ then $\mathbb { Z } ^ { m } = \mathbb { Z } ^ { m } \cup \{ \mathbb { Z } _ { z } \}$ End if   
4: If $\mathcal { R } _ { z } ^ { n a r } \geq R _ { m } ^ { m a x }$ then $\mathbb { Z } ^ { s } = \mathbb { Z } ^ { s } \cup \{ \mathbb { Z } _ { z } \}$ End if   
5: $\mathbf { I f } \ \mathcal { R } _ { z } ^ { \mathit { \tilde { n } a r } } < { R } _ { m } ^ { \mathit { \tilde { m a x } } } \leq \mathcal { R } _ { z } ^ { f a r }$ then   
6: If $\frac { \mathcal { R } _ { z } ^ { f a r } - R _ { m } ^ { m a x } } { \mathcal { R } _ { \sim } ^ { f a r } - \mathcal { R } _ { \sim } ^ { n a r } } < \zeta$ then   
7: $\mathbb { Z } ^ { \acute { m } } = \mathbb { Z } ^ { \acute { m } } \cup \{ \mathbb { z } _ { z } \}$   
8: Else   
9: Get $\mathbb { Z } _ { z , 1 }$ with $( \rho _ { z } ^ { l w } , \rho _ { z } ^ { u p } , \mathcal { R } _ { z } ^ { n a r } , R _ { m } ^ { m a x } )$ from $\mathbb { Z } _ { z }$   
10: Get $\mathbb { Z } _ { z , 2 }$ with $( \rho _ { z } ^ { l w } , \rho _ { z } ^ { u p } , R _ { m } ^ { m a x } , \mathcal { R } _ { z } ^ { f a r } )$ from $\mathbb { Z } _ { z }$   
11: $\mathbb { Z } ^ { m } = \mathbb { Z } ^ { m } \cup \lbrace \mathbb { Z } _ { z , 1 } \rbrace ; \mathbb { Z } ^ { s } = \mathbb { Z } ^ { s } \cup \lbrace \mathbb { Z } _ { z , 2 } \rbrace$   
12: End if   
13: End if   
14: End for   
15: Rmax = Infinitesimal Number; Rmin = Infinity   
16: For $\forall \mathbb { Z } _ { k } ^ { s } \in \mathbb { Z } ^ { s }$ do   
17: If $\mathcal { R } _ { k } ^ { f a r } > { \mathbb { R } ^ { m a x } }$ then $\mathbb { R } ^ { m a x } = \mathcal { R } _ { k } ^ { f a r }$ End if   
18: If $\mathcal { R } _ { k } ^ { n a r } < { \mathbb { R } ^ { m i n } }$ then $\mathbb { R } ^ { m i n } = \mathcal { R } _ { k } ^ { n a r }$ End if   
19: End for   
$\begin{array} { r } { 2 0 : \mathbb { K } = \lceil \frac { \mathbb { R } ^ { m a x } - \mathbb { R } ^ { m i n } } { R _ { b h } ^ { s } } \rceil } \end{array}$   
21: For k = 1; k < K; k + + do $\mathbb { Z } _ { \mathbb { k } } ^ { s } = \emptyset$ End for   
22: âbk = Rmin   
23: For k = 1; k < K; k + + do   
24: $\mathbb { Z } ^ { r } = \emptyset ; \mathcal { R } _ { \Bbbk } ^ { b } = \mathcal { R } _ { \Bbbk } ^ { b } + R _ { b h } ; R _ { n } ^ { f , s } = \mathcal { R } _ { \Bbbk } ^ { b } - 0 . 5 R _ { b h }$   
25: For $\forall \mathbb { Z } _ { k } ^ { s } \in \mathbb { Z } ^ { s }$ do   
26: If $\mathcal { R } _ { k } ^ { f a r } < \mathcal { R } _ { \Bbbk } ^ { b }$ then $\mathbb { Z } _ { \mathbb { k } } ^ { s } = \mathbb { Z } _ { \mathbb { k } } ^ { s } \cup \{ \mathbb { Z } _ { k } ^ { s } \}$ End if   
27: If $\mathcal { R } _ { k } ^ { \mathit { \tilde { n } a r } } \geq \mathcal { R } _ { \mathbb { k } } ^ { b }$ then $\mathbb { Z } ^ { r } = \mathbb { Z } ^ { r } \cup \{ \mathbb { Z } _ { k } ^ { s } \}$ End if   
28: If $\mathcal { R } _ { k } ^ { n a r } < \mathcal { R } _ { \mathbb { k } } ^ { \bar { b } } \leq \mathcal { R } _ { k } ^ { f a r }$ then   
29: If $\frac { \mathcal { R } _ { k } ^ { f a r } - \mathcal { R } _ { \Bbbk } ^ { b } } { \mathcal { R } _ { k } ^ { f a r } - \mathcal { R } _ { k } ^ { n a r } } < \zeta$ then $\mathbb { Z } _ { \mathbb { k } } ^ { s } = \mathbb { Z } _ { \mathbb { k } } ^ { s } \cup \{ \mathbb { Z } _ { k } ^ { s } \}$ End if   
30: If $\frac { \mathcal { R } _ { \Bbbk } ^ { b } - \mathcal { R } _ { k } ^ { n a r } } { \mathcal { R } _ { k } ^ { f a r } - \mathcal { R } _ { k } ^ { n a r } } < \zeta$ then $\mathbb { Z } ^ { r } = \mathbb { Z } ^ { r } \cup \{ \mathbb { z } _ { k } ^ { s } \}$ End if   
31: If $\frac { \mathcal { R } _ { k } ^ { f a r } - \mathcal { R } _ { \Bbbk } ^ { b } } { \mathcal { R } _ { k } ^ { f a r } - \mathcal { R } _ { k } ^ { n a r } } \ge \zeta$ and $\frac { \mathcal { R } _ { \Bbbk } ^ { b } - \mathcal { R } _ { k } ^ { n a r } } { \mathcal { R } _ { k } ^ { f a r } - \mathcal { R } _ { k } ^ { n a r } } \ge \zeta$ then   
32: Get $\mathbb { Z } _ { k , 1 }$ with $( \rho _ { k } ^ { l w } , \rho _ { k } ^ { u \ddot { p } } , \mathcal { R } _ { k } ^ { n a r } , \mathcal { R } _ { \Bbbk } ^ { b } )$ from $\mathbb { Z } _ { k } ^ { s }$   
33: Get zk,2 with $( \rho _ { k } ^ { l w } , \rho _ { k } ^ { u p } , \mathcal { R } _ { \Bbbk } ^ { b } , \mathcal { R } _ { k } ^ { f a r } )$ from $\mathbb { Z } _ { k } ^ { s }$   
34: $\mathbb { Z } _ { \mathbb { k } } ^ { s } = \mathbb { Z } _ { \mathbb { k } } ^ { s } \cup \{ \mathbb { z } _ { k , 1 } \} ; \mathbb { Z } ^ { r } = \mathbb { Z } ^ { r } \cup \{ \mathbb { z } _ { k , 2 } \}$   
35: End if   
36: End if   
37: End for   
38: $\mathbb { Z } ^ { s } = \mathbb { Z } ^ { r }$   
39: End for   
40: $\begin{array} { r } { \mathbb { Z } ^ { t } = \bigcup _ { \mathbb { k } = 1 } ^ { \mathbb { K } } \mathbb { Z } _ { \mathbb { k } } ^ { s } } \end{array}$   
41: Return $\bar { \mathbb { Z } } ^ { m ^ { - } }$ and $\mathbb { Z } ^ { t }$

Corollary 1. If the parameter $R _ { b h }$ is fixed and the parameter $\rho _ { n , k } ^ { a }$ of the reference point a is exactly $\rho _ { n , k } ^ { u p } ,$ , the parameter $\rho _ { n , k } ^ { p o s 1 }$

of $P O S _ { 1 }$ can be estimated by

$$
\rho _ { n , k } ^ { p o s 1 } = \rho _ { n , k } ^ { u p } + 2 \mathrm { a r c s i n } \frac { \sqrt { ( R _ { n } ^ { c } ) ^ { 2 } - \left( \frac { R _ { b h } } { 2 } \right) ^ { 2 } } } { R _ { n } ^ { f } } - \mathrm { a r c s i n } \frac { R _ { n } ^ { c } } { R _ { n } ^ { f } }\tag{37}
$$

Proof: From Fig. 4, we can know that the following relation exists.

$$
\omega _ { n , k } = \arcsin \frac { R _ { n } ^ { c } } { R _ { n } ^ { f } }\tag{38}
$$

Therefore, we have $\rho _ { n , k } ^ { p o s 1 } = \rho _ { n , k } ^ { u p } + \theta _ { n , k } - \omega _ { n , k }$ , where the parameters $\theta _ { n , k }$ and $\omega _ { n , k }$ can be substituted based on the Formulas (35) and (38) to derive the Formula (37). So the proof is completed. Similarly, the following corollary also exists.

Corollary 2. If the parameter $R _ { b h }$ is fixed and the parameter $\rho _ { n , k } ^ { b }$ of the reference point b is exactly $\rho _ { n , k } ^ { l w }$ , the parameter $\rho _ { n , k } ^ { p o s 2 }$ of $P O S _ { 2 }$ can be estimated by

$$
\rho _ { n , k } ^ { p o s 2 } = \rho _ { n , k } ^ { l w } - 2 \mathrm { a r c s i n } { \frac { \sqrt { ( R _ { n } ^ { c } ) ^ { 2 } - \left( { \frac { R _ { b h } } { 2 } } \right) ^ { 2 } } } { R _ { n } ^ { f } } } + \mathrm { a r c s i n } { \frac { R _ { n } ^ { c } } { R _ { n } ^ { f } } }\tag{39}
$$

The proof of Corollary 2 is similar to that of Corollary 1, so it is not repeated. In addition, from Fig. 4, we can know that $\psi _ { n , k } = 2 \omega _ { n , k } - \theta _ { n , k }$ . According to the Formulas (35) and (38), Ïn,k is formulated in detail as follows.

$$
\psi _ { n , k } = 2 \mathrm { a r c s i n } { \frac { R _ { n } ^ { c } } { R _ { n } ^ { f } } } - 2 \mathrm { a r c s i n } { \frac { \sqrt { \left( R _ { n } ^ { c } \right) ^ { 2 } - \left( { \frac { R _ { b h } } { 2 } } \right) ^ { 2 } } } { R _ { n } ^ { f } } }\tag{40}
$$

According to the shape parameters $\rho _ { n , k } ^ { l w }$ and $\rho _ { n , k } ^ { u p }$ of cluster $\mathbb { Z } _ { n , k }$ and the SUAV flight radius $( \boldsymbol { \mathrm { e } } . \boldsymbol { \mathrm { g } } . , \ R _ { n } ^ { f } )$ , if $\rho _ { n , k } ^ { u p } - \rho _ { n , k } ^ { l w } \leq$ $\psi _ { n , k }$ , the interval $\tau _ { 1 }$ is enough time for SUAV n to cover this cluster (see Fig. 4). Otherwise, the following corollary gives an estimating method of the time to cover this cluster.

Corollary 3. If the size of any cluster $( \mathrm { e } . \mathrm { g } . , \mathbb { Z } _ { n , k } )$ with the shape parameters $\rho _ { n , k } ^ { l w }$ and $\rho _ { n , k } ^ { u p }$ is more than the effective coverage size of a SUAV (e.g., n) flying along the path of radius $R _ { n } ^ { f }$ at the speed $V _ { n , k } ~ ( \mathrm { i . e . , ~ } \rho _ { n , k } ^ { u p } - \rho _ { n , k } ^ { l w } > \psi _ { n , k } )$ , the time required for this SUAV to achieve the effective coverage of this cluster can be estimated by

$$
\tau _ { n , k } = \frac { \tau _ { 1 } \left( \left( \rho _ { n , k } ^ { u p } - \rho _ { n , k } ^ { l w } \right) + 2 \left( \theta _ { n , k } - \omega _ { n , k } \right) \right) } { \theta _ { n , k } }\tag{41}
$$

Proof: As shown Fig. 3, we can know that SUAV n can reach the target of covering the z-th cluster only by flying from $o _ { \gamma } ^ { s }$ to $o _ { z } ^ { d }$ in the arc trajectory with the radius $R _ { n } ^ { f }$ at the speed $V _ { z }$ Therefore, the arc length from osz to $o _ { z } ^ { d }$ can be estimated by $\mathcal { L } _ { z } =$ $R _ { n } ^ { f } ( ( \rho _ { z } ^ { u p } - \rho _ { z } ^ { l w } ) + 2 \bar { ( \theta _ { z } - \omega _ { z } ) ) }$ . Since the speed of the SUAV n is known, it is easy to get its flight time $\begin{array} { r } { ( \mathrm { e } . \mathrm { g } . , \tau _ { z } = \frac { \mathcal { L } _ { z } } { V _ { z } } ) } \end{array}$ in the corresponding arc trajectory. When the z-th cluster is regarded as $\mathbb { Z } _ { n , k } .$ , the Formula (41) can be derived based on the Formula (36). Therefore, the proof is completed.

The covering-task-area optimization process is described in Algorithm 3. The clusters in the service area of SUAV n are arranged in descending order of cluster location coordinate values (see line 1), and then the flight speed, starting point, ending point and flight time of SUAV n are calculated for each cluster in turn (see lines 2â¼8). Next, the clusters that overlap or are very close to each other are merged (see lines 11â¼14). Finally, the size of the clusters is updated (see line 17) and the members of the correspond set are sorted for later usage (see lines 18â¼19).

Algorithm 3: Optimizing covering-task-area.   
Run at the MUAV   
Input: $\mathbb { Z } _ { n }$ // The covering-task-area for SUAV n   
Output: $\vec { \mathbb { Z } } _ { n } ^ { o }$ and $\bigcup _ { k = 1 } ^ { K } \left\{ < V _ { n , k } , \rho _ { n , k } ^ { p o s 1 } , \rho _ { n , k } ^ { p o s 2 } , \tau _ { n , k } > \right\}$   
$/ / \stackrel {  o } { \mathbb { Z } } _ { n } ^ { o }$ is the optimized covering-task-area for SUAV n   
1: Sort clusters of $\mathbb { Z } _ { n }$ in descending order of $\textstyle \bigcup _ { k = 1 } ^ { K } \rho _ { n , k } ^ { u p }$   
and get $\widehat { \mathbb { Z } } _ { n } ^ { s } = \langle \mathbb { z } _ { n , 1 } , \ . . . , \mathbb { z } _ { n , k } , . . . , \mathbb { z } _ { n , K } \rangle$   
2: For $k = 1 ; k \le K ; k + + \mathbf { d o }$   
3: Get $\rho _ { n , k } ^ { l w }$ and $\rho _ { n , k } ^ { u p }$ of cluster $\mathbb { Z } _ { n , k }$   
4: Compute $V _ { n , k }$ according to Formulas (35) and (36)   
5: Compute $\rho _ { n , k } ^ { p o s 1 }$ according to Formula (37)   
6: Compute $\rho _ { n , k } ^ { p o s 2 }$ according to formula (39)   
7: Compute $\tau _ { n , k }$ according to Formula (41)   
8: End for   
9: $: \mathbb { Z } _ { n } ^ { o } = \{ \mathbb { Z } _ { n , 1 } \} ; \Delta K = 0$   
10: For $k = 2 ; k \leq K ; k + +$ do   
11: If $R _ { n } ^ { f } ( \rho _ { n , k - 1 } ^ { p o s 2 } - \rho _ { n , k } ^ { p o s 1 } ) < \mathcal { L } _ { t h }$ then   
12: $\rho _ { n , k } ^ { u p } = \rho _ { n , k - 1 } ^ { u p } ; \mathbb { Z } _ { n } ^ { o } = \mathbb { Z } _ { n } ^ { o } - \{ \mathbb { Z } _ { n , k - 1 } \}$   
13: $\mathbb { Z } _ { n } ^ { o } = \mathbb { Z } _ { n } ^ { o } \cup \{ \mathbb { Z } _ { n , k } \} ; \Delta K + +$   
14: Update $\rho _ { n , k } ^ { p o s 1 } , \rho _ { n , k } ^ { p o s 2 }$ and $\tau _ { n , k }$   
15: Else $\mathbb { Z } _ { n } ^ { o } = \mathbb { Z } _ { n } ^ { o } \cup \{ \mathbb { Z } _ { n , k } \}$ End if   
16: End for   
17: $K = K - \Delta K$   
18: Sort clusters of $\mathbb { Z } _ { n } ^ { o }$ in descending order of $\textstyle \bigcup _ { k = 1 } ^ { K } \rho _ { n , k } ^ { u p }$   
and get $\vec { \mathbb { Z } } _ { n } ^ { o } = \langle \mathbb { z } _ { n , 1 } , \ldots , \mathbb { z } _ { n , k } , \ldots , \mathbb { z } _ { n , K } \rangle$   
19: Return $\mathbb { Z } _ { n }$ and $\bigcup _ { k = 1 } ^ { K } \left\{ < V _ { n , k } , \rho _ { n , k } ^ { p o s 1 } , \rho _ { n , k } ^ { p o s 2 } , \tau _ { n , k } > \right\}$

## D. Solution for Problem P1

When determining how much time SUAV n would spend on each cluster it serves, it only ensures improvement on $\mathcal { P } _ { n }$ of the coverage quality metric $S C Q _ { n }$ . In order to improve $P r _ { n }$ , the flight time between clusters must be minimized. The following corollary gives an estimating method of the minimum flight time between clusters.

Corollary 4. When a SUAV (e.g., n) flies along the circular trajectory of radius $R _ { n } ^ { f } .$ , the minimum required time between any two adjacent clusters $( \mathrm { e } . \mathrm { g } . , \mathbb { Z } _ { n , k }$ and $\mathbb { Z } _ { n , k + 1 } )$ can be estimated by

$$
\tau _ { n , k } ^ { b c }
$$

$$
= \sqrt { 2 \sqrt { \frac { \mathscr { L } _ { n , k } ^ { b c } } { a } + \frac { { V _ { n , k } } ^ { 2 } + V _ { n , k + 1 } } { 2 a ^ { 2 } } } } - \frac { V _ { n , k } + V _ { n , k + 1 } } { a }\tag{42a}
$$

$$
\begin{array} { r } { \left[ \begin{array} { l } { \frac { { { \mathcal L } _ { n , k } ^ { b c } } } { V ^ { m a x } } + \frac { { { V } ^ { m a x } } } { a } + \frac { { { { V } _ { n , k } } } ^ { 2 } + { { V } _ { n , k + 1 } } ^ { 2 } } { 2 a V ^ { m a x } } - \frac { { { V } _ { n , k } } + { { V } _ { n , k + 1 } } } { a } } \end{array} \right. } \end{array}\tag{42b}
$$

(42)

where $\mathcal { L } _ { n , k } ^ { b c }$ is the arc length from the cluster $\mathbb { Z } _ { n , k } \mathrm { ~ } ^ { \mathrm { ~ \sum ~ S ~ } } { \cal P } { \cal O } S _ { 2 }$ to the cluster $\mathbb { Z } _ { n , k + 1 } \mathrm { ~ \ ' s ~ } P O S _ { 1 }$ , while $V ^ { m a x }$ and a are the theoretical maximum speed and acceleration of the $\mathrm { { S U A V } } n .$

Proof. Take Fig. 4 as an example for convenience, in order to shorten the flight time on $\mathcal { L } _ { n , k } ^ { b c } .$ , we obviously need to increase the flight speed from $V _ { n , k }$ to a certain value $V _ { u p } ^ { s }$ and then decrease it from $V _ { u p } ^ { s } \mathrm { t o } V _ { n , k + 1 }$ by using the same acceleration a. When $\mathcal { L } _ { n , k } ^ { b c }$ is long enough and a is large enough, $V _ { u p } ^ { s }$ can reach $V ^ { m a x }$ Otherwise, $V _ { u p } ^ { s }$ may be less than $V ^ { m a x }$ . Therefore, we derive the expression of the minimum flight time $\tau _ { n , k } ^ { b c }$ from the cluster $\mathbb { Z } _ { n , k } \mathrm { ~ \mathrm { ~ s ~ } ~ } P O S _ { 2 }$ to the cluster $\mathbb { Z } _ { n , k + 1 } \mathrm { ~ \bar { ~ s ~ } ~ } P O S _ { 1 }$ by distinguishing between the two cases.

For the case where $V _ { u p } ^ { s } < V ^ { m a x } , \tau _ { n , k } ^ { b c }$ consists of the time of accelerating phase $\tau _ { u p }$ and the time of decelerating phase $\tau _ { d w } .$ From the velocity formula of physics theory, we have

$$
\left\{ \begin{array} { l l } { \tau _ { u p } = \frac { V _ { u p } ^ { s } - V _ { n , k } } { a } } & { ( 4 3 a ) } \\ { \tau _ { d w } = \frac { V _ { u p } ^ { s } - V _ { n , k + 1 } } { a } } & { ( 4 3 b ) } \end{array} \right.\tag{43}
$$

From the displacement formula of physics theory, we have

$$
\mathcal { L } _ { n , k } ^ { b c } = \frac { V _ { u p } ^ { s } + V _ { n , k } } { 2 } \tau _ { u p } + \frac { V _ { u p } ^ { s } + V _ { n , k + 1 } } { 2 } \tau _ { d w }\tag{44}
$$

Based on (43) and (44), we have

$$
\left\{ \begin{array} { l l } { \tau _ { u p } = \sqrt { \frac { \mathcal { L } _ { n , k } ^ { b c } } { a } + \frac { { V _ { n , k } } ^ { 2 } + { V _ { n , k + 1 } } ^ { 2 } } { 2 a ^ { 2 } } } - \frac { V _ { n , k } } { a } } & { \left( 4 5 a \right) } \\ { \tau _ { d w } = \sqrt { \frac { \mathcal { L } _ { n , k } ^ { b c } } { a } + \frac { { V _ { n , k } } ^ { 2 } + V _ { n , k + 1 } { } ^ { 2 } } { 2 a ^ { 2 } } } - \frac { V _ { n , k + 1 } } { a } } & { \left( 4 5 b \right) } \end{array} \right.\tag{45}
$$

Therefore, based on (45) and $\tau _ { n , k } ^ { b c } = \tau _ { u p } + \tau _ { d w } .$ , the Formula (42a) is derived. Also, we can derive the following formula for calculating the value of $V _ { u p } ^ { s }$ according to $V _ { u p } ^ { s } = V _ { n , k } + a \tau _ { u p } .$

$$
{ \cal V } _ { u p } ^ { s } = \sqrt { a { \mathcal { L } _ { n , k } ^ { b c } } + \frac { { V _ { n , k } } ^ { 2 } + V _ { n , k + 1 } { } ^ { 2 } } { 2 } }\tag{46}
$$

For the case where $V _ { u p } ^ { s }$ can reach $V ^ { m a x } , \tau _ { n , k } ^ { b c }$ includes the time $( \mathrm { e . g . , \tau _ { \mathit { c s t } } } )$ of constant flight at $V ^ { m a x }$ besides $\tau _ { u p }$ and $\tau _ { d w }$ From the velocity formula of physics theory, we have

$$
\left\{ \begin{array} { l l } { \tau _ { u p } = \frac { V ^ { m a x } - V _ { n , k } } { a } } \\ { \tau _ { d w } = \frac { V ^ { m a x } - V _ { n , k + 1 } } { a } } \end{array} \right.\tag{47}
$$

From the displacement formula of physics theory, we have

$$
\mathcal { L } _ { n , k } ^ { b c } = \frac { ( V ^ { m a x } ) ^ { 2 } - ( V _ { n , k } ) ^ { 2 } } { 2 a } + \frac { ( V ^ { m a x } ) ^ { 2 } - \left( V _ { n , k + 1 } \right) ^ { 2 } } { 2 a } + \tau _ { c s t } V _ { \phantom { m a x } , a } ^ { m a x }\tag{48}
$$

Therefore, based on (47) and (48) as well as $\tau _ { n , k } ^ { b c } = \tau _ { u p } +$ $\tau _ { c s t } + \tau _ { d w } .$ , the Formula (42b) is derived. Based on the above complete derivation results, the proof is completed.

The optimization process of SUAV flight time per lap is described in Algorithm 4. First, we need to count the number of members in each cluster (see lines 2â¼4). Then each cluster whose number of members is smaller than the threshold and close to the neighboring cluster is merged into the neighboring cluster after all the clusters are arranged in ascending order (see lines 5â¼10). Next, the size of the clusters set is updated (see line 11) and then the merging operation of the adjacent clusters that meet the conditions is repeated (see line 13) after all the clusters are sorted in descending order (see line 12). It is worth noting that $R _ { n } ^ { f } | \rho _ { n , k } ^ { p o s 1 } - \rho _ { n , k + 1 } ^ { p o s 2 } |$ should be updated to $R _ { n } ^ { f } | \rho _ { n , k } ^ { p o s 2 } - \rho _ { n , k + 1 } ^ { p o s 1 } |$ during repeating the steps 6â¼11. Finally, after updating the parameters of each cluster processed above (see line 14), the flight time for a lap of a SUAV is accumulated and returned (see line 15â¼23).

Algorithm 4: Optimizing SUAV flight time per lap.   
Run at the MUAV   
Input: $\overline { { \mathbb { Z } } } _ { n } ^ { \cup }$ and $\bigcup _ { k = 1 } ^ { K } \left\{ < V _ { n , k } , \rho _ { n , k } ^ { p o s 1 } , \rho _ { n , k } ^ { p o s 2 } , \tau _ { n , k } > \right\}$   
Output: $\tau _ { n } / /$ The flight time per lap for SUAV n   
$1 \colon \tau _ { n } = 0 ; \Delta K = 0$   
0   
2: For $\forall \mathbb { Z } _ { n , k } \in \mathbb { Z } _ { n } ^ { \mathsf { ^ { \circ } } }$ do   
3: Count the number of GSTAs in $\mathbb { Z } _ { n , k }$ and save it in $\mathbb { N } _ { n , k } ^ { s }$   
4: End for   
5: Update the clusters of $\vec { \mathbb { Z } } _ { n } ^ { o }$ in ascending order of   
$\textstyle \bigcup _ { k = 1 } ^ { K } \rho _ { n , k } ^ { u p }$   
6: For $\bar { k } = 1 ; k < K ; k + + { \bf d o }$   
7: $\mathbf { I f } \mathbb { N } _ { n , k } ^ { s } < \mathbb { N } _ { t h } ^ { s }$ and $R _ { n } ^ { f } | \rho _ { n , k } ^ { p o s 1 } - \rho _ { n , k + 1 } ^ { p o s 2 } | < D _ { r }$ then   
8: $\begin{array} { r } { \vec { \mathbb { Z } } _ { n } ^ { o } = \vec { \mathbb { Z } } _ { n } ^ { o } - \{ \mathbb { Z } _ { n , k } \} ; \mathbb { N } _ { n , k + 1 } ^ { s } = \mathbb { N } _ { n , k + 1 } ^ { s } + \mathbb { N } _ { n , k } ^ { s } ; } \end{array}$   
$\Delta K + +$   
9: End if   
10: End for   
11: $K = K - \Delta K$   
12: Update the clusters of $\vec { \mathbb { Z } } _ { n } ^ { o }$ in descending order of   
$\textstyle \bigcup _ { k = 1 } ^ { K } \rho _ { n , k } ^ { u p }$   
13: Repeat the steps $6 \sim 1 1$ and go to the step 14   
14: Update $\bigcup _ { k = 1 } ^ { K } \mathbf { \bar { \left\{ \right.} } <  V _ { n , k } , \rho _ { n , k } ^ { p o s  } , \rho _ { n , k } ^ { p o s 2 } , \tau _ { n , k } > \}$   
15: For $k = 1 ; k < K ; k + + \mathbf { d o }$   
16: Calculate $V _ { u p } ^ { s }$ according to Formula (46)   
17: $\mathbf { I f } ~ V _ { u p } ^ { s } < V ^ { r _ { n } ^ { s } a x }$ then   
18: Calculate $\tau _ { n , k } ^ { b c }$ according to Formula (42a)   
19: Else Calculate $\tau _ { n , k } ^ { b c }$ according to Formula (42b) End if   
20: $\tau _ { n } = \tau _ { n } + ( \tau _ { n , k } + \tau _ { n , k } ^ { b c } )$   
21: End for   
22: $\tau _ { n } = \tau _ { n } + \tau _ { n , K }$   
23: Return $\tau _ { n }$

## E. DRL-Based Model for Problem P2

As mentioned above, we propose a DRL-based solution to the problem P2. In this solution, an artificial intelligence (AI) agent interacts with the UAV-assisted dynamic network environment in a sequence of actions, observations and rewards. We divide the time interval between each two continuous updates for network coverage parameters into a series of equal time slots, which is denoted by $\{ 1 , \ldots , N \}$ . When the length of such a time slot is sufficiently short, the position of any SUAV can be considered to be approximately unchanged during a time slot. At each time slot $t \in \{ 1 , \ldots , N \}$ , the AI agent decides an action for each SUAV. The each SUAV will connect the GSTAs it covers and the perform channel allocation according to the action, while the corresponding GSTAs will select the appropriate transmission powers and beams to achieve sub-optimal power-beam control.

It is worth noting that the speed and trajectory of SUAVs are not be affected by the decided action, since they are determined by the network coverage scheme described earlier and thus must obey their coverage mission arrangement. Based on the above, the system throughput optimization problem with the spectrumenergy efficiency constraint is described as a discrete-time Markov decision process (MDP) denoted by a tuple $( \mathcal { S } , \mathcal { A } , \mathcal { R } )$ ï¼ where ?? is the set of states, ?? is the set of actions, and â is the set of reward functions. $\mathcal { S } ^ { t }$ refers specifically to the state space of the network environment during time slot $\scriptstyle { \mathrm { \# , } }$ which is defined by

$$
\mathcal { S } ^ { \epsilon } = [ \mathbb { A } ^ { \epsilon } , \mathbb { B } ^ { \epsilon } , \mathbb { D } ^ { t } \mid t \in \{ 1 , \dots , N \} ]\tag{49}
$$

where $\mathbb { A } ^ { t }$ is used to record whether each SUAV covers any ground cluster during time slot $\scriptstyle t ; \mathbb { B } ^ { t }$ is used to record whether each SUAV is requested by any GSTA to provide communication services until the beginning of time slot $\smash { t : \mathbb { D } ^ { t } }$ is used to record whether each SUAV receives data from any ground cluster until the beginning of time slot ??.

In the state space $\mathcal { S } ^ { t } , \mathbb { A } ^ { t }$ records the all the SUAVsâ coverage information on the ground clusters during time slot $\scriptstyle { \mathrm { \# , } }$ which is detailed as $\mathbb { A } ^ { t } { = } [ \bar { \mathfrak { a } } _ { 1 } ^ { t } , . . . , \mathfrak { a } _ { n } ^ { t } , . . . , \mathfrak { a } _ { | \mathcal { N } _ { \mathrm { s } } | } ^ { t } \ | \ n \in \mathcal { N } _ { \mathrm { s } } , t \in$ $\{ 1 , \ldots , N \} ]$ . Take $\mathfrak { a } _ { n } ^ { t }$ for an example, it records SUAV nâs coverage information on the ground clusters it is responsible for providing communication services during time slot ??, which is detailed as $\mathfrak { a } _ { n } ^ { \mathcal { t } } = [ \mathfrak { a } _ { n , 1 } ^ { t } , \ \dots , \mathfrak { a } _ { n , k } ^ { \mathcal { t } } , \ \cdot \cdot \cdot , \mathfrak { a } _ { n , K _ { n } } ^ { t } | k \in \{ 1 , \dots , K _ { n } \} ]$ Likewise, take $\mathfrak { a } _ { n , k } ^ { t }$ for an example, it records SUAV nâs coverage information on the k-th ground cluster it is responsible for providing communication services during time slot ??. Here, at least one GSTA in the k-th ground cluster can communicate with SUAV n if $\mathfrak { a } _ { n , k } ^ { t } = 1$ . Otherwise $\mathfrak { a } _ { n , k } ^ { t } = 0$

B?? records the all the SUAVsâ receiving request information from the ground clusters until the begin of time slot ??, which is detailed as $\begin{array} { r } { \mathbb { B } ^ { t } = [ \mathbb { b } _ { 1 } ^ { t } , \ . . . , \mathbb { b } _ { n } ^ { t } , \ . . . , \mathbb { b } _ { | \mathcal { N } _ { \mathrm { s } } | } ^ { t } \ | \ n \in \mathcal { N } _ { \mathrm { s } } } \end{array}$ ï¼ $t \in \{ 1 , \ldots , N \} ]$ . Take $\mathbb { b } _ { n } ^ { t }$ for an example, it records SUAV nâs receiving request information from the ground clusters it is responsible for providing communication services until the beginning of time slot ??, which is detailed as $\mathbb { b } _ { n } ^ { t } = [ b _ { n , 1 } ^ { t } ,$ â¦, $\mathbb { b } _ { n , k } ^ { t } , ~ . . . , \ \mathbb { b } _ { n , K _ { n } } ^ { t } \ \vert \ k \in \left\{ 1 , . . . , K _ { n } \right\} \rbrack$ . Likewise, take $\mathbb { b } _ { n , k } ^ { t }$ for an example, it records SUAV nâs receiving request information from the k-th ground cluster it is responsible for providing communication services until the beginning of time slot ??. The request information should include the location coordinates of GSTAs and the number of GSTAs, but the scheme in this paper only focuses on whether the number of requests exceeds the number of concurrent services the SUAV can provide. If the number of requests (e.g., it is denoted by N) is less than |C| (i.e., the number of concurrent services), $\begin{array} { r } { \bar { \mathbb { b } } _ { n , k } ^ { t } = \frac { \mathbb { N } } { | \mathbb { C } | } } \end{array}$ . Otherwise $\mathbb { b } _ { n , k } ^ { t } = 1$

$\mathbb { D } ^ { t }$ records the information of all the SUAVsâ receiving data from the ground clusters until the begin of time slot $\scriptstyle { \mathrm { \# , } }$ which is detailed as $\mathbb { D } ^ { t } \mathbf { = } [ \mathbb { d } _ { 1 } ^ { t } , ~ . . . , \mathbb { d } _ { n } ^ { t } , ~ . . . , ~ \mathbb { d } _ { | \mathcal { N } _ { \mathrm { s } } | } ^ { t } ~ | ~ n \in \mathcal { N } _ { \mathrm { s } }$ ï¼ $t \in \{ 1 , \ldots , N \} ]$ . Take $\mathbb { d } _ { n } ^ { t }$ for an example, it records SUAV nâs receiving data information from the ground clusters it is responsible for providing communication services until the beginning of time slot ??, which is detailed as $\mathbb { d } _ { n } ^ { t } = [ \mathbb { d } _ { n , 1 } ^ { t }$ , â¦, $\mathbb { d } _ { n , k } ^ { \ell } , ~ . . . , \mathbb { d } _ { n , K _ { n } } ^ { \ell } \mid k \in \left\{ 1 , \ldots , K _ { n } \right\} ]$ . Likewise, take $\mathbb { d } _ { n , k } ^ { t }$ for an example, it records the amount of data received by SUAV n from the k-th ground cluster it is responsible for providing communication services until the beginning of time slot ??. According to the above state information, the AI agent can select an action for the UAV-assisted dynamic network. Similarly, $\mathcal { A } ^ { t }$ refers specifically to the action space of the AI agent during time slot ??, which is defined by

$$
\mathcal { A } ^ { t } = [ \mathbb { F } ^ { t } , \mathbb { G } ^ { t } , \mathbb { H } ^ { t } \mid t \in \{ 1 , \dots , N \} ]\tag{50}
$$

where $\mathbb { F } ^ { t }$ is used to record whether each SUAV adopts additional channel resources or changes the amount of additional channel resources used by it during time slot $\mathit { t } ; \mathbb { G } ^ { t }$ and $\mathbb { H } ^ { t }$ are used to record whether each SUAV helps its serving GSTAs to adjust their transmission powers and transmission beam widths during time slot ??.

In the action space $\mathcal { A } ^ { t }$ , the action vector $\mathbb { F } ^ { t }$ is decided by the AI agent for each SUAV, which is detailed as $\mathbb { F } ^ { t } = [ \mathbb { f } _ { 1 } ^ { t } , . . . , \mathbb { f } _ { n } ^ { t } .$ $\dots , \mathbb { f } _ { | \mathcal { N } _ { \mathrm { s } } | } ^ { t } \mid n \in \mathcal { N } _ { \mathrm { s } } , t \in \{ 1 , \dots , N \} ]$ . Take $\mathbb { f } _ { n } ^ { t }$ for an example, it records the amount of additional channel resources selected by SUAV n for the ground clusters during time slot $\scriptstyle { \mathrm { \# , } }$ which is detailed as $\mathbb { f } _ { n } ^ { t } = [ \mathbb { f } _ { n , 1 } ^ { \bar { t } } , . . . , \mathbb { f } _ { n , k } ^ { \bar { t } } , . . . , \mathbb { f } _ { n , K _ { n } } ^ { \bar { t } } \mid k \in \{ 1 , . . . , K _ { n } \} ]$ Likewise, take $\mathbb { f } _ { n , k } ^ { t }$ for an example, it means SUAV nâs selecting amount of additional channel resources for the k-th ground cluster it is responsible for providing communication services during time slot ??.

In addition, the action vectors $\mathbb { G } ^ { t }$ and $\mathbb { H } ^ { t }$ are decided by the AI agent for the GSTAs served by each SUAV. $\mathbb { G } ^ { t }$ and $\mathbb { H } ^ { \star }$ are detailed as [g??1, â¦, $\begin{array} { r } { \underline { { \mathrm { g } } } _ { n } ^ { t } , \ . . . , \ \underline { { \mathrm { g } } } _ { | \mathcal { N } _ { \mathrm { s } } | } ^ { t } \ | \ n \in \mathcal { N } _ { \mathrm { s } } , t \in \{ 1 , . . . , N \} ] } \end{array}$ and $[ \mathbb { h } _ { 1 } ^ { t } , . . . , \mathbb { h } _ { n } ^ { t } , . . . , \mathbb { h } _ { | \mathcal { N } _ { \mathrm { s } } | } ^ { t } \mid n \in \mathcal { N } _ { \mathrm { s } } , t \in \{ 1 , . . . , N \} ]$ , respectively. Take $\boldsymbol { \underline { { \mathrm { g } } } } _ { n } ^ { t }$ and ${ \mathbb { h } } _ { n } ^ { t }$ for an example respectively, $\boldsymbol { \underline { { \mathrm { g } } } } _ { n } ^ { t }$ records the sets of transmission powers selected by SUAV n for the ground clusters during time slot ??, while $\ln _ { n } ^ { \dot { t } }$ records transmission beam widths corresponding to the sets of transmission powers. $\boldsymbol { \underline { { \mathrm { g } } } } _ { n } ^ { t }$ and $\mathbb { h } _ { n } ^ { t }$ are further described as $[ \underline { { \mathfrak { g } } } _ { n , 1 } ^ { t } , . . . , \underline { { \mathfrak { g } } } _ { n , k } ^ { t } ,$ $\dots , \underset { 0 , n , K _ { n } } { \mathbb { g } } \mid k \in \{ 1 , \dots , K _ { n } \} ]$ and $[ \mathbb { h } _ { n , 1 } ^ { t } , . . . , \mathbb { h } _ { n , k } ^ { t } , . . . , \mathbb { h } _ { n , K _ { n } } ^ { t } \ |$ $k \in \{ 1 , \ldots , K _ { n } \} ]$ , respectively.

Likewise, take $\boldsymbol { \mathrm { g } } _ { n , k } ^ { t }$ and $\ln _ { n , k } ^ { t }$ for an example respectively, $\boldsymbol { \mathrm { g } } _ { n , k } ^ { t }$ means SUAV nâs selecting set of transmission powers for the k-th ground cluster it is responsible for providing communication services during time slot ??, while $\mathbb { h } _ { n , k } ^ { t }$ means SUAV nâs selecting the set of transmission beam widths corresponding to the sets of transmission powers. $\boldsymbol { \mathrm { g } } _ { n , k } ^ { t }$ and $\mathbb { h } _ { n , k } ^ { t }$ are further described as $\{ \mathbf { g } _ { n , k , 1 } ^ { t } , \ . . . , \mathbf { g } _ { n , k , c } ^ { t } , \ . . . , \mathbf { g } _ { n , k , | \mathbb { C } \cup \hat { \mathbb { C } } | } ^ { t } \mid c \in \{ 1 , . . . , | \mathbb { C } \cup \hat { \mathbb { C } } | \} \}$ and $\{ \mathfrak { h } _ { n , k , 1 } ^ { t } , \mathbf { \Omega } \cdot \cdot . . , \mathfrak { h } _ { n , k , c } ^ { t } , \mathbf { \Omega } \cdot . . . , \mathfrak { h } _ { n , k , | \mathbb { C } \cup \hat { \mathbb { C } } | } ^ { t } \mid c \in \{ 1 , \dots , | \mathbb { C } \cup \hat { \mathbb { C } } | \} \}$ respectively, where the value range of each power is not less than 0 and not more than the maximum transmission power of GSTAs, while the value range of each beam width is more than 0 and less than $\varphi _ { n } ^ { m a x }$ . Therefore, the above action space determines the immediate reward for the UAV-assisted dynamic network. $\mathcal { R } ^ { t }$ refers specifically to a function of state and action during time slot ??, which measures the effect of the action taken by an agent at a given state and is defined by

$$
\mathcal { R } ^ { t } = \left[ \begin{array} { c } { \left( 1 - \partial \right) \left( S E E \left( t \right) - S E E _ { t h } \right) + } \\ { \partial \varphi \mathcal { T } _ { s u m } \left( t \right) \vert t \in \left\{ 1 , \ldots , N \right\} } \end{array} \right]\tag{51}
$$

where $S E E ( t )$ is the system spectral-energy efficiency during time slot ??, while $\mathcal { T } _ { s u m } ( t )$ is the system throughput during time slot ??. In addition, $\partial$ is a weight coefficient and $0 < \partial <$ 1, while $\varphi$ is an adjustment coefficient aiming to balance the order of magnitude gap between throughput and spectral-energy efficiency.

Our goal is to maximize the system throughput under the system spectral-energy efficiency constraint, so we take $\mathcal { R } ^ { t }$ during time slot ?? as the instant reward in the tuple. After the AI agent executes an action, it will get immediate feedback as a standard for the following decision making. To get the maximum cumulative discounted reward in the long term, the state-action value function $Q ( \cdot )$ in Q-learning can be used, which is defined by

$$
\begin{array} { r l } & { Q \left( \mathcal { S } ^ { t } , \mathcal { A } ^ { t } \right) \gets Q \left( \mathcal { S } ^ { t } , \mathcal { A } ^ { t } \right) + \varrho \{ \mathcal { R } ^ { t } + } \\ & { \quad \quad \quad \sigma \operatorname* { m a x } _ { \mathcal { A } ^ { t + 1 } } Q \left( \mathcal { S } ^ { t + 1 } , \mathcal { A } ^ { t + 1 } \right) - Q \left( \mathcal { S } ^ { t } , \mathcal { A } ^ { t } \right) \} } \end{array}\tag{52}
$$

where $\varrho$ is the learning rate and Ï is the discount factor.

## F. Solution for Problem P2

In the problem P2, the state-action value function $Q ( \cdot )$ cannot be expressed mathematically, so deep neural networks (DNNs) can be used to approximate the optimal value of $Q ( \cdot )$ , which is expressed by

$$
Q \left( \mathcal S ^ { t } , \mathcal A ^ { t } | \Theta ^ { Q } \right) \approx Q ^ { * } \left( \mathcal S ^ { t } , \mathcal A ^ { t } \right)\tag{53}
$$

where $\Theta ^ { Q }$ is the parameters of a certain DNN. Based on the Formula (53), our proposed DRL-based channel allocation and power-beam control strategies can be evaluated and improved over time through ongoing network training. In fact, although the allocation of additional channel resources can be approximated as discrete action selection process, the power control and beam width adjustment are exactly regarded as the two continuous tasks. The framework of DRL based on the actor-critic deep deterministic policy gradient (DDPG) [36] is very appropriate to cope with continuous action space. Therefore, we design a DDPG-based throughput optimization algorithm under spectralenergy efficiency constraint to solve problem P2, which is described in Algorithm 5.

In Algorithm 5, a certain DNN (that is composed of an online network $\Theta ^ { \mu }$ and a target network $\Theta ^ { \dot { \mu } } )$ serves as an actor to choose an action, while a certain deep Q-network (that is composed of an online network $\Theta ^ { Q }$ and a target network $\Theta ^ { Q } )$ acts as a critic network to interact with the actor, which judges whether the action is proper. By repeating the above process, the actor gradually figures out how to select appropriate action for each state, while the critic constantly iterates to enhance the stateaction values. The actor will output a specific action value at each iteration according to $\mathcal { A } ^ { t } = \mu ( \mathcal { S } ^ { t } | \Theta ^ { \mu } )$ , while the critic will output a specific Q value of the current state-action based on the Formula (53). Based on a stochastic gradient descent (SGD) method, the actor updates the weights of online network $\Theta ^ { \mu }$

Algorithm 5: DDPG-based throughput optimization under   
spectral-energy efficiency constraint.   
Run at the disaster management center and the MUAV   
Input: $\mathbb { X } , \varsigma , \sigma , \varrho$ // DDPG network parameters   
Output: $\Theta ^ { \mu } , \Theta ^ { Q } , \mathcal { A } ^ { t * }$ // Online policy and Q network   
parameters, and optimal action   
at each time slot ??   
The train stage is performed in the disaster management   
center   
1: Initialize replay memory pool $\mathbb { X }$ with its size $| \mathbb { X } |$   
2: Initialize $\Theta ^ { \mu }$ and $\Theta ^ { Q }$ with random weights   
3: Initialize target policy network $\Theta ^ { \dot { \mu } }$ with $\Theta ^ { \mu }$   
4: Initialize target Q network $\Theta ^ { Q }$ with $\Theta ^ { Q }$   
5: For episode $\in \{ 1 , 2 , \ldots , E \}$ do   
6: Initialize the scenario and observe system state $\mathcal { S } ^ { 1 }$   
7: For $t \in \{ 1 , \ldots , N \}$ do   
8: Get the action $\mathcal { A } ^ { \hat { t } } = \mu ( \mathcal { S } ^ { t } | \Theta ^ { \mu } )$   
9: Get the reward $\mathcal { R } ^ { t }$ and observe next state $\mathcal { S } ^ { t + 1 }$   
10: Save the data $( \mathcal { S } ^ { t } , \mathcal { A } ^ { t } , \mathcal { R } ^ { t } , \mathcal { S } ^ { t + 1 } )$ i n X   
11: If X is full then   
12: Select the sets of samples $( \boldsymbol { \mathrm { e } } . \boldsymbol { \mathrm { g } } . , \boldsymbol { b s } )$ from X   
randomly   
13: Update the online policy (actor) network   
parameters $( \Theta ^ { \mu } )$ by maximizing $J ( \Theta ^ { \mu } ) =$   
$\operatorname { \mathbb { E } } _ { \Theta ^ { \mu } } [ Q ( \mathcal { S } ^ { t } , \mu ( \mathcal { S } ^ { t } | \hat { \Theta } ^ { \mu } ) | \Theta ^ { Q } ) ]$   
14: Update the online $Q$ (critic) network parameters   
$( \bar { \Theta } ^ { Q } )$ by minimizing $L o s s ( \Theta ^ { Q } ) = ( \bar { \mathcal { R } } ^ { t } +$   
$\sigma Q ( \mathcal { S } ^ { t + 1 } , \mathcal { A } ^ { t + 1 } | \Theta ^ { \breve { Q } } ) - Q ( \mathcal { S } ^ { t } , \mathcal { A } ^ { t } | \dot { \Theta } ^ { Q } ) ) ^ { 2 }$   
15: $\Theta ^ { \bar { Q } }  \varsigma \Theta ^ { Q } + ( \bar { 1 } - \varsigma ) \Theta ^ { \bar { Q } } ; \Theta ^ { \bar { \mu } } $   
$\varsigma \Theta ^ { \mu } + ( 1 - \varsigma ) \Theta ^ { \mu }$   
16: End if   
17: End for   
18: End for   
19: Return $\Theta ^ { \mu } , \Theta ^ { Q }$ The decision stage is performed in the   
MUAV   
20: Observe the system state $\mathcal { S } ^ { t }$ of the current time slot ??   
21: Select optimal action $\mathcal { A } ^ { t * } = \mu ( \mathcal { S } ^ { t } | \Theta ^ { \mu } )$   
22: Return $\mathcal { A } ^ { t * }$   
by maximizing $J ( \Theta ^ { \mu } ) = \mathbb { E } _ { \Theta ^ { \mu } } [ Q ( \mathcal { S } ^ { t } , \mu ( \mathcal { S } ^ { t } | \Theta ^ { \mu } ) | \Theta ^ { Q } ) ]$ , while the   
critic updates the weights of online network $\Theta ^ { Q }$ by minimizing   
$L o s s ( \dot { \Theta } ^ { Q } ) = ( \mathcal { R } ^ { t } + \overset { \smile } { \sigma } Q ( \mathcal { S } ^ { t + 1 } , \mathcal { A } ^ { t + 1 } | \Theta ^ { Q } ) - Q ( \mathcal { S } ^ { \dot { t } } , \mathcal { A } ^ { t } | \Theta ^ { Q } ) ) ^ { \overset { \sim } { 2 } } .$

In a training process, the experience replay memory pool X is initialized and set to the size $| \mathbb { X } |$ . Then, E episodes are adopted in the training process. Next, the actor decides an action $\mathcal { A } ^ { t }$ based on the current online network $\mu ( \mathcal { S } ^ { t } | \Theta ^ { \mu } )$ and the critic evaluates the appropriateness of this action by determining whether the Q value of the current state-action is optimized. After executing $\mathcal { A } ^ { t }$ , it will move on to the next state $\mathcal { S } ^ { t + 1 }$ and get an instant reward $\mathcal { R } ^ { t }$ . The tuples $( \mathcal { S } ^ { t } , \mathcal { A } ^ { t } , \mathcal { R } ^ { t } , \mathcal { S } ^ { t + 1 } )$ generated by state transitions are kept in $ \mathbb { X } ,$ which will be used to train the online network. When X is full, a mini-batch will be randomly selected from X to update both the actor online network $\Theta ^ { \mu }$ and the critic online network $\Theta ^ { Q }$ . Finally, the actor target network $\Theta ^ { \dot { \mu } }$ and the critic target network $\Theta ^ { \dot { Q } }$ can be updated by $\Theta ^ { \mu }  \varsigma \Theta ^ { \mu } +$ $( 1 - \varsigma ) \Theta ^ { \dot { \mu } } \mathrm { a n d } \Theta ^ { Q }  \varsigma \Theta ^ { Q } + ( 1 - \varsigma ) \Theta ^ { Q }$ respectively, where Ï is the rate at which the target networks are updated and $0 < \varsigma <$ 1.

## G. Performance Analysis of Algorithms

For Algorithm 1, there are two nested loops, where the size of the outer loop is |Z| while that of the inner loop is $\left| \mathbb { Z } _ { z } \right|$ Therefore, the computational complexity of Algorithm 1 is $O ( | \mathbb { Z } | | \mathbb { z } _ { z } | )$ . For Algorithm 2, there are one nested loop, where the size of the outer loop is K while that of the inner loop is $| \mathbb { Z } ^ { s } |$ . Therefore, the computational complexity of Algorithm 2 is $O ( \mathbb { K } | \mathbb { Z } ^ { s } | )$ . Since Algorithm 3 has only two single-loop structures with the size K and includes two sorting procedures, its complexity depends on the complexity of the sorting algorithm used in this paper. Algorithm 4 has three single loops with the size K since $K = | \vec { \mathbb { Z } } _ { n } ^ { \sigma } |$ , its computational complexity is also $O ( K )$ . The results of problem P1 are obtained by sequential execution of Algorithms 1â¼4, so the computational complexity of problem P1 depends on the most computationally complex one of the above four algorithms. Since there is no iterative process, the optimization scheme of problem P1 is definitely convergent. However, as mentioned earlier about the complexity of problem P1, Algorithms 1â¼4 can only give an approximate solution for local optimization. Since Algorithm 5 is based on the classical DDPG architecture, its computational complexity and convergence performance should be at least as good as the classical DDPG algorithm, which will be further elaborated in the simulation section. Based on the previous description of the complexity of problem P2, Algorithm 5 can only give an approximate solution for local optimization.

## V. PERFORMANCE EVALUATION

## A. Experimental Parameter Settings

We have carried out a series of simulation experiments for the two solutions proposed in the previous sections. As shown in Fig. 2, we simulate the post-disaster area as a circle with the radius $R ^ { G }$ , make the MUAV hover above the circle center, and randomly deploy a certain number of GSTAs in the circular area. In addition, one or more SUAVs are deployed in the area that is not covered by the MUAV, forming one or more ring areas. The stochastic movement of GSTAs is simulated by randomly updating the positions of some GSTAs.

For the problem P2, besides the solution of this paper, the block coordinate descent (BCD) based method [37] can also be tried to solve it. In addition, the heuristic algorithm such as genetic algorithm (GA) are also suitable for solving it, since it is very efficient to solve any problem where the solution space is too large to be searched exhaustively [38]. To facilitate the description of simulation results below, we refer to our solution and the two comparison solutions as DDPG-based, BCD-based, and GA-based schemes, respectively.

In the simulation experiments, the hardware and software configurations contain Apple M2, Hynix LPDDR5 16GB, Pycharm 2022.3.2, Python 3.9.6, and PyTorch 1.13.1. Unless otherwise stated, the main simulation parameters are shown in Tables I, II,

TABLE I  
SIMULATION PARAMETERS FOR CPO
<table><tr><td>Symbol</td><td>Description</td><td>Value</td></tr><tr><td>a</td><td>Acceleration of each SUAV</td><td> $\overline { { { 3 \mathrm { ~ m } } / { \mathrm { s } ^ { 2 } } } }$ </td></tr><tr><td> $R ^ { G }$ </td><td>Radius of disaster area</td><td>500 m</td></tr><tr><td> $R _ { m } ^ { c }$ </td><td>Radius of MUVA&#x27;s coverage area</td><td>100 m</td></tr><tr><td> $\mathcal { N } _ { u }$ </td><td>NumberofGSTAs</td><td>1000</td></tr><tr><td> $V ^ { m a x }$ </td><td>Maximum speed of each SUAV</td><td>140 km/h</td></tr><tr><td> $\zeta$ </td><td>Proportion threshold in Algorithm 2</td><td>0.1</td></tr><tr><td> $\kappa$ </td><td>Benchmark coefficient for dividing the covering-task-area in Algorithm 2</td><td>0.75</td></tr><tr><td> $\mathcal { L } _ { t h } ^ { s }$ </td><td>Distance threshold between two clusters in Algorithm 3</td><td>50m</td></tr><tr><td> $\mathbb { N } _ { t h } ^ { s }$ </td><td>Threshold number of GSTAs in one cluster in Algorithm 4</td><td>5</td></tr><tr><td> $D _ { r }$ </td><td>D2D distance threshold in Algorithm 4</td><td>50m</td></tr><tr><td> $\tau _ { 0 }$ </td><td>Channel access delay</td><td>1 s</td></tr><tr><td> $\tau _ { 1 } { - } \tau _ { 0 }$ </td><td>Data transmission time interval</td><td>9s</td></tr><tr><td> $\beta$ </td><td>Signal strength threshold</td><td>-90 dBm</td></tr><tr><td> $\underline { { H _ { m } } } , \underline { { H _ { n } } }$ </td><td>FlightaltitudeforMUAV,SUAVn</td><td>100m</td></tr></table>

SIMULATION PARAMETERS FOR MMWAVE COMMUNICATION

TABLE II
<table><tr><td>Symbol</td><td>Description</td><td>Value</td></tr><tr><td>E</td><td>Side lobe gain</td><td>0.001</td></tr><tr><td> $B$ </td><td>Band width</td><td>1GHz</td></tr><tr><td> $N _ { 0 }$ </td><td>Power spectral density of background noise</td><td>-174dBm/Hz</td></tr><tr><td> $f _ { c }$ </td><td>Carrier frequency</td><td>28GHz</td></tr><tr><td> $P _ { R F }$ </td><td>Power consumption of an RF chain</td><td>0.0344W</td></tr><tr><td> $N _ { R F }$ </td><td>Number ofRF chains on each UAV</td><td>8</td></tr><tr><td> $| \mathbb { C } \cup \hat { \mathbb { C } } |$ </td><td>Numberof available channels</td><td>8+4</td></tr><tr><td> $\varphi _ { m } ^ { m a x }$ </td><td>Maximumbeamwidth ofMUAV</td><td>120Â°</td></tr><tr><td> $\varphi _ { n } ^ { m a x }$ </td><td>Maximumbeamwidthof SUAVn</td><td>120Â°</td></tr><tr><td> $\smash { p _ { w a } ^ { t , m a x } }$  Pm</td><td>Maximum transmission power of MUAV</td><td>5.5W</td></tr><tr><td> $y _ { n } ^ { t , m a x }$ </td><td>Maximum transmission power of SUAV n</td><td>5.5W</td></tr></table>

TABLE III

SIMULATION PARAMETERS FOR DRL
<table><tr><td>Symbol</td><td>Description</td><td>Value</td></tr><tr><td>ã®</td><td>Discount factor</td><td>0.9</td></tr><tr><td>0</td><td>Learning rate</td><td>0.1</td></tr><tr><td>m</td><td>Parameter for epsilon-greedy policy</td><td>0.1</td></tr><tr><td>[X</td><td>Experience replay pool size</td><td>2000</td></tr><tr><td> $\varsigma$ </td><td>Updated ratio for each target network</td><td>0.01</td></tr><tr><td>bs</td><td>Mini-batch experience replay size</td><td>32</td></tr><tr><td>E</td><td>Number of episodes</td><td>3000</td></tr></table>

TABLE IV

SIMULATION PARAMETERS FOR BCD AND GA
<table><tr><td>Symbol</td><td>Description</td><td>Value</td></tr><tr><td> $\varrho _ { b 1 }$ </td><td>Learning rate of transmission power for BCD</td><td>0.05</td></tr><tr><td> $\varrho _ { b 2 }$ </td><td>Learning rate of beam width for BCD</td><td>0.01</td></tr><tr><td> $I _ { b c d }$ </td><td>Maximum iterations for BCD</td><td>100</td></tr><tr><td> $\varepsilon _ { b c d }$ </td><td>Convergence tolerance in BCD</td><td>1e-6</td></tr><tr><td> $P _ { g a }$ </td><td>Population size for GA</td><td>10</td></tr><tr><td> $G _ { g a }$ </td><td>Generations for GA</td><td>500</td></tr><tr><td> $M _ { g a }$ </td><td>Mutation probability for GA</td><td>0.1</td></tr><tr><td> $\underline { { C _ { g a } } }$ </td><td>Cross probability for GA</td><td>0.5</td></tr></table>

III, and IV. Here, the simulation parameters for CPO are adopted with reference to [11], those for mmWave communication are selected with reference to [32], [33], [34], [35], those for DRL are adopted with reference to [36], and those for BCD and GA are selected with reference to [37], [38].

<!-- image-->  
UAV hovering/flight altitude (Meters)

Fig. 5. Impact of hovering/flight altitude on maximum coverage radius in omnidirectional transmission mode.  
<!-- image-->  
Fig. 6. Impact of UAV hovering/flight altitude on minimum transmission power in directional transmission mode.

## B. Experimental Results and Analysis

1) Performance Comparison of Solution to CPO Problem: The simulation results for the solution to the CPO problem are shown in Figs. 5, 6, 7, 8, 9, and 10. Specifically, Figs. 5, 6, and 7 show the relationships between communication parameters and coverage area of a single UAV, Figs. 8 and 9 reveal the relationships between SCQ and the degree of GSTAsâ uneven distribution, and Fig. 10 shows the impact of GSTAsâ movement on SCQ.

As shown in Fig. 5, when the hovering/flight altitude is fixed, the UAVâs maximum coverage radius in omnidirectional transmission mode increases with its maximum transmission power. This is mainly because a larger maximum transmission power allows the transmitted message to travel farther before its signal strength decays below the sensitivity threshold of the received signal.

<!-- image-->  
Fig. 7. Impact of UAV flight speed on $R _ { b h }$ in directional transmission mode.

<!-- image-->  
Fig. 8. Impact of degree of GSTAsâ uneven distribution on SCQ under different values of the coefficient Î¾.

<!-- image-->  
Fig. 9. Impact of degree of GSTAsâ uneven distribution on SCQ under the two strategies.

<!-- image-->  
Fig. 10. Impact of GSTAsâ movement on SCQ.

Fig. 5 also shows that the UAVâs maximum coverage radius decreases with the hovering/flight altitude when its maximum transmission power is fixed. The main reason has been described above. Based on the results of Fig. 5, we explore the minimum transmission powers required for the four effective coverage radii of a single UAV at the different effective hovering/flight altitudes. The results are shown in Fig. 6. Here, at the same hovering/flight altitude, the smaller the area to be covered, the lower the minimum transmission power to be required. The reason behind this phenomenon is explained as above.

Meanwhile, we can also see from Fig. 6 that, under the same coverage radius, the higher the hovering/flight altitude, the lower the minimum transmission power required to ensure the coverage radius. This is because, as the hovering/flight altitude increases, the UAV uses a smaller transmission beam width to ensure coverage, where the smaller transmission beam width can increase directional gain and save transmission power consumption. Although the longer propagation path will consume more energy, in this simulation environment, the benefits brought by the increased directional gain outweigh the losses caused by the increased propagation distance.

Fig. 7 shows the impact of flight speed on the coverage area of a single UAV, where the flight altitude is 100 m and the flight trajectory radius is 400 m. The $R _ { b h }$ shown in Fig. 4 is used to approximate the coverage area size of a moving UAV. We can see from Fig. 7 that the UAV flight speed is inversely proportional to $R _ { b h }$ . This is consistent with the inference from the Formulas (35) and (36).

According to the above simulation results, we set both the MUAVâs hovering altitude and the two SUAVsâ flight altitude to 100m, the coverage radius of the MUAV to 100 m, and the coverage radius of each SUAV to 120 m. In addition, the two SUAVsâ flight trajectory radii are set to 200 m and 400 m, respectively. Based on such simulation parameter Settings, the relationships between SCQ and the degree of GSTAsâ uneven distribution are shown in Figs. 8 and 9. Here, in order to reflect a real post-disaster area and also not to make the simulation environment construction too complicated, we assume that 10 safety locations are evenly distributed in the post-disaster area and each victim can freely choose anyone. We adopt the number of safety locations unselected by any victim to approximate the heterogeneity of distribution of GSTAs. Obviously, the greater the number of safety locations that have been unselected by anyone, the greater the uneven distribution of GSTAs.

As shown in Fig. 8, when the coefficient Î¾ is fixed, the higher the degree of GSTAsâ uneven distribution, the greater the value of SCQ. This is because the greater unbalanced distribution means that the areas with coverage demand are more concentrated. In the areas where there is no demand for coverage, the speed of the moving UAV is not limited by the coverage tasks, which helps to improve the value of $P r _ { n }$ of SCQ while ensuring the basic stability of the value of $\mathcal { P } _ { n }$ of SCQ. In addition, we can also see from Fig. 8 that, under the same degree of GSTAsâ uneven distribution, the larger the coefficient $\xi ,$ the smaller the value of SCQ. This is because the value of $P r _ { n }$ of SCQ is always less than the value of $\mathcal { P } _ { n }$ of SCQ, which is not conducive to improving SCQ value when the coefficient Î¾ gets larger according to the Formula (19).

It is worth noting that, under the four typical values of the coefficient Î¾, there is no significant difference in the sensitivity of SCQ values to reflect the degree of GSTAsâ uneven distribution when the heterogeneity of distribution of GSTAs is relatively larger. For example, when the number of unselected safety locations are 7 and 9, it is hard to see the difference of SCQ from Fig. 8. This is because, under our simulation environment, no more than 3 safety locations need to be covered at this time, so each moving UAV may be responsible for covering less than 3 safety locations. Therefore, there is little space to improve the coverage probability by using the heterogeneity degree of user distribution at this time.

Fig. 9 shows the benefits of taking advantage of the uneven distribution of GSTAs. Here, we set the coefficient Î¾ to 0.9 to mainly focus on the value of $P r _ { n }$ of SCQ, since the uneven distribution of GSTAs mainly affects $P r _ { n } .$ For convenience, CPO-GD is used to refer to the strategy taking advantage of the uneven distribution of GSTAs, and CPO-NGD denotes the corresponding comparison strategy that does not consider the uneven distribution of GSTAs. As can be seen from Fig. 9, when the degree of GSTAsâ uneven distribution gradually increases, the value of SCQ under the strategy CPO-GD is gradually improved. The reason behind this phenomenon is similar to the explanation given for the results in Fig. 8. In addition, we also see that the value of SCQ in the strategy CPO-NGD is hardly improved when the heterogeneity of distribution of GSTAs is relatively larger. This is because the strategy CPO-NGD does not speed up any SUAVâs flight in the areas without GSTAs. In this case, $P r _ { n }$ does not increase, and thus SCQ is not improved accordingly.

Based on simulation parameter Settings in Figs. 8 and 9, we fixed the number of unselected safety locations at 9 and the coefficient Î¾ at 0.1 to explore the impact of GSTAsâ movement on SCQ under another two different coverage probability optimization strategies. As shown in Fig. 10, CPO-GM represents the strategy considering GSTAsâ movement, while CPO-NGM represents the strategy without considering GSTAsâ movement.

<!-- image-->  
(a) Throughput

<!-- image-->  
(b) Spectrum-energy efficiency

Fig. 11. Impact of the coefficient â on convergence performance of DDPGbased throughput optimization algorithm.  
<!-- image-->  
(a) Throughput

<!-- image-->  
(b)Spectrum-energy efficiency  
Fig. 12. Impact of background noise on convergence performance of DDPGbased throughput optimization algorithm.

We simulate GSTAsâ movement by referring to the idea of random waypoint model. For each movement, we randomly select a certain number of GSTAs (i.e., 20%) to move in a random direction and a random distance, where the maximum moving distance is set to 100m.

In Fig. 10, with the increase of GSTAsâ movement count, SCQ fluctuates around 0.9 under the CPO-GM strategy, while SCQ continues to decline under the CPO-NGM strategy. This is because the SUAVs do not focus on GSTAsâ movement under the CPO-NGM strategy. Therefore, even if there are some GSTAs that have moved, it will not update the clustering results for GSTAs, which makes the current network coverage parameters cannot reflect the actual distribution of GSTAs. In this case, the value of $\mathcal { P } _ { n }$ will get worse with the increase of GSTAsâ movement count, while $P r _ { n }$ keeps unchanged because the results of Algorithms 1â¼4 are not updated. So SCQ will get worse and worse. However, under the CPO-GM strategy, Algorithm 1â4 will be re-executed when the GSTAsâ movement count reaches a preset threshold, so that the updated network coverage parameters can reflect the actual distribution of GSTAs. Therefore, the CPO-GM strategy outperforms the CPO-NGM strategy in terms of SCQ.

2) Performance Comparison of DDPG-Based Throughput Optimization Scheme Under Different Parameters: In Figs. 11 and 12, we mainly focus on the impact of several significant parameters on the convergence performance of DDPG-based throughput optimization algorithm. Here, besides the common topology parameters described for Figs. 8, 9, and 10, the networking parameters determined by the proposed solution to

<!-- image-->

<!-- image-->  
(b)Spectrum-energy eficiency  
Fig. 13. Performance comparison of three schemes for solving problem P2.

CPO problem also include the number of unselected safety locations (e.g., 9) and the coefficient Î¾ (e.g., 0.1). First, based on a large number of simulation experiments, we set the adjustment coefficient Ï to 0.025 and $S E E _ { t h }$ to 30Gbps/Hz/W. Then, we perform the simulation to explore the impact of different values of the weight coefficient â on convergence performance.

From Fig. 11, we observe that the variation trends of throughput and SEE are completely opposite during the whole training process. The convergence value of throughput and SEE depends on the value of -. That is because the smaller value of - (e.g., 0.1) means the greater proportion of SEE in the reward value according to the Formula (51). Therefore, in the training process, SEE shows a gradual upward trend with the increasing number of episodes and converges to 40Gbps/Hz/W approximately. However, on the contrary, throughput shows a gradual decline with the increasing number of episodes and converges to 400Gbps approximately. This is because throughput only accounts for a relatively small portion of the reward value. With the increase of - (e.g., 0.5), throughput shows a gradual upward trend and converges at about 420Gbps. However, due to the limited concurrency capacity of the network, when throughput reaches the upper limit, even if the value of - increases further (e.g., 0.9), it will not significantly help to improve throughput. In this case, SEE also converges to a lower value (i.e., about 30Gbps/Hz/W).

Based on the results of Fig. 11, we fix the coefficient - at 0.9 to explore the impact of background noise $( \mathrm { i } . \mathrm { e } . , N _ { 0 } )$ on training performance of DDPG-based throughput optimization algorithm. As shown in Fig. 12, as the background noise decreases from -165dBm/Hz to -185dBm/Hz, the convergence value of throughput increases from about 450Gbps to 500Gbps. However, the convergence value of SEE does not change significantly (around 30Gbps/Hz/W). This is because a given transmission power produces a higher signal-to-noise ratio under less background noise and thus obtains a higher throughput according to Shannonâs theorem. However, the variation trend of SEE depends on the relationship between the gained benefits (i.e., throughput) and the paid costs (i.e., power consumption and frequency band resources). In this simulation environment, the benefits and costs are basically balanced, so there is no significant change in the convergence of SEE.

3) Performance Comparison of Different Solutions to Throughput Optimization Problem P2: The simulation results of our DDPG-based scheme and the two comparison schemes for solving the problem P2 are shown in Fig. 13. From Fig. 13(a), we see that the BCD-based scheme has the lowest throughput among the three schemes. As a whole, the GA-based scheme exhibits the highest performance, whereas the DDPG-based scheme performs slightly worse than the GA-based scheme. This is mainly because the uplink mmWave communication scenario in this paper exhibits a non-smooth characteristic. Although SUAVsâ receiving beam direction and width are fixed, those of GSTAs are dynamic due to beam alignment requirements. Therefore, any pair of transmitter and receiver may shift from a non-beam-aligned state to a beam-aligned state, or vice versa, thereby causing a sudden change in throughput. Consequently, there is a high probability that the BCD-based scheme will fall into a local optimum due to its low exploration capability. Conversely, both the GA-based and DDPG-based schemes have a greater likelihood of finding a global optimum when dealing with non-smooth problems due to their high exploration capabilities.

Based on the aforementioned reasons, the simulation results of Fig. 13(b) can be well explained. For the BCD-based scheme, due to its tendency to a local optimum, it fails to fully exploit channel resources to maximize throughput under the predefined SEE constraint, resulting in the lowest obtained SEE. Because of the fuller exploration of the unknown space and no interactive learning ability with the environment, the GA-based scheme is more greedy, especially when the channel resources are more abundant. While this helps improve throughput, it tends to come at the expense of more channel resources. It is noteworthy that the GA-based scheme has to re-execute the entire search process whenever the network environment parameters (e.g., the positions of SUAVs, channel quality) are changed, incurring non-negligible time costs. Despite the longer convergence time during the training phase, the trained DDPG-based model has almost negligible time costs in the subsequent decision-making process. This advantage is particularly pronounced in postdisaster relief networks.

## VI. CONCLUSION

In this article, we proposed a new method for measuring single UAV coverage quality and developed a set of novel algorithms for solving the CPO problem. The proposed solution can take advantage of the uneven distribution of ground terminals to improve the coverage quality of multi-UAV-assisted disaster relief networks. Then, in order to cope with the throughput optimization problem under the spectrum-energy efficiency constraint, we proposed a DDPG-based scheme to determine the appropriate number of channels and the sub-optimal values of power-beam pairs to achieve the above goal. After the comparison with the benchmark strategies or schemes, we find that our scheme performs better in different perspectives.

## REFERENCES

[1] J. S. Kumar and M. A. Zaveri, âGraph-based resource allocation for disaster management in IoT environment,â in Proc. 2nd Int. Conf. Adv. Wireless Inf., Data Commun. Technol., Paris, France, 2017, pp. 1â6.

[2] Y. Duan, Y. P. Zhao, Y. Q. Xu, Y. Peng, and D. T. Liu, âUnmanned aerial vehicle sensor data anomaly detection using kernel principle component analysis,â in Proc. IEEE 13th Int. Conf. Electron. Meas. Instruments, 2017, pp. 241â246.

[3] M. Erdelj and E. Natalizio, âUAV-assisted disaster management: Applications and open issues,â in Proc. Int. Conf. Comput. Netw. Commun., 2016, pp. 1â5.

[4] S. J. H. Pirzada, M. Haris, M. N. Hasan, T. Xu, and L. Jianwei, âDetection and communication of disasters with space-air-ground integrated network,â in Proc. IEEE 23rd Int. Multi-Topic Conf., 2020, pp. 1â6.

[5] M. Erdelj, E. Natalizio, K. R. Chowdhury, and I. F. Akyildiz, âHelp from the sky: Leveraging UAVs for disaster management,â IEEE Pervasive Comput., vol. 16, no. 1, pp. 24â32, First Quarter 2017.

[6] F. Ono, H. Ochiai, and R. Miura, âA wireless relay network based on unmanned aircraft system with rate optimization,â IEEE Trans. Wireless Commun., vol. 15, no. 11, pp. 7699â7708, Nov. 2016.

[7] J. Li, D. Lu, G. Zhang, J. Tian, and Y. Pang, âPost-disaster unmanned aerial vehicle base station deployment method based on artificial bee colony algorithm,â IEEE Access, vol. 7, pp. 168327â168336, 2019.

[8] J. Liu, Y. Shi, Z. M. Fadlullah, and N. Kato, âSpace-air-ground integrated network: A survey,â IEEE Commun. Surv. Tut., vol. 20, no. 4, pp. 2714â2741, Fourth Quarter 2018.

[9] Z. Y. Jia, M. Sheng, J. D. Li, and Z. Han, âTowards data collection and transmission in 6G space-air-ground integrated networks: Cooperative HAP and LEO satellite schemes,â IEEE Internet Things J., vol. 9, no. 13, pp. 10516â10528, Jul. 2022.

[10] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âUnmanned aerial vehicle with underlaid device-to-device communications: Performance and tradeoffs,â IEEE Trans. Wireless Commun., vol. 15, no. 6, pp. 3949â3963, Jun. 2016.

[11] S. Zhang and J. Liu, âAnalysis and optimization of multiple unmanned aerial vehicle-assisted communications in post-disaster areas,â IEEE Trans. Veh. Technol., vol. 67, no. 12, pp. 12049â12060, Dec. 2018.

[12] B. Wang, Y. Sun, N. Zhao, and G. Gui, âLearn to coloring: Fast response to perturbation in UAV-assisted disaster relief networks,â IEEE Trans. Veh. Technol., vol. 69, no. 3, pp. 3505â3509, Mar. 2020.

[13] J. S. Gui and F. J. Cai, âEfficient radio channel allocation in integrated mmWave/sub-6 GHz UAV-assisted disaster relief networks,â Mobile Inf. Syst., vol. 2021, 2021, Art. no. 6707804.

[14] J. Lyu and R. Zhang, âNetwork-connected UAV: 3-D system modeling and coverage performance analysis,â IEEE Internet Things J., vol. 6, no. 4, pp. 7048â7060, Aug. 2019.

[15] S. Shakoor, Z. Kaleem, D.-T. Do, O. A. Dobre, and A. Jamalipour, âJoint optimization of UAV 3-D placement and path-loss factor for energyefficient maximal coverage,â IEEE Internet Things J., vol. 8, no. 12, pp. 9776â9786, Jun. 2021.

[16] Y. Ji, Z. Yang, H. Shen, W. Xu, K. Wang, and X. Dong, âMulticell edge coverage enhancement using mobile UAV-relay,â IEEE Internet Things J., vol. 7, no. 8, pp. 7482â7494, Aug. 2020.

[17] P. K. Sharma and D. I. Kim, âRandom 3D mobile UAV networks: Mobility modeling and coverage probability,â IEEE Trans. Wireless Commun., vol. 18, no. 5, pp. 2527â2538, May 2019.

[18] H. Huang and A. V. Savkin, âA method for optimized deployment of unmanned aerial vehicles for maximum coverage and minimum interference in cellular networks,â IEEE Trans. Ind. Inform., vol. 15, no. 5, pp. 2638â2647, May 2019.

[19] X. F. Wang et al., âPerformance analysis of terahertz unmanned aerial vehicular networks,â IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 16330â16335, Dec. 2020.

[20] A. V. Savkin and H. Huang, âDeployment of unmanned aerial vehicle base stations for optimal quality of coverage,â IEEE Wireless Commun. Lett., vol. 8, no. 1, pp. 321â324, Feb. 2019.

[21] H. L. Huang and A. V. Savkin, âDeployment of heterogeneous UAV base stations for optimal quality of coverage,â IEEE Internet Things J., vol. 9, no. 17, pp. 16429â16437, Sep. 2022.

[22] B. Galkin, J. KibiÅda, and L. A. DaSilva, âA stochastic model for UAV networks positioned above demand hotspots in urban environments,â IEEE Trans. Veh. Technol., vol. 68, no. 7, pp. 6985â6996, Jul. 2019.

[23] X. W. Li, H. P. Yao, J. J. Wang, X. B. Xu, C. X. Jiang, and L. Hanzo, âA near-optimal UAV-aided radio coverage strategy for dense urban areas,â IEEE Trans. Veh. Technol., vol. 68, no. 9, pp. 9098â9109, Sep. 2019.

[24] N. Cherif, M. Alzenad, H. Yanikomeroglu, and A. Yongacoglu, âDownlink coverage and rate analysis of an aerial user in vertical heterogeneous networks (VHetNets),â IEEE Trans. Wireless Commun., vol. 20, no. 3, pp. 1501â1516, Mar. 2021.

[25] C. Zhang, L. Y. Zhang, L. P. Zhu, T. Zhang, Z. Y. Xiao, and X.-G. Xia, â3D Deployment of multiple UAV-mounted base stations for UAV communications,â IEEE Trans. Commun., vol. 69, no. 4, pp. 2473â2488, Apr. 2021.

[26] M. Nafees, J. Thompson, and M. Safari, âMulti-tier variable height UAV networks: User coverage and throughput optimization,â IEEE Access, vol. 9, pp. 119684â119699, 2021.

[27] R. R. Chen, Y. J. Sun, L. P. Liang, and W. C. Cheng, âJoint power allocation and placement scheme for UAV-assisted IoT with QoS guarantee,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 1066â1071, Jan. 2022.

[28] L. Y. Wang, H. X. Zhang, S. S. Guo, and D. F. Yuan, âDeployment and association of multiple UAVs in UAV-assisted cellular networks with the knowledge of statistical user position,â IEEE Trans. Wireless Commun., vol. 21, no. 8, pp. 6553â6567, Aug. 2022.

[29] O. M. Bushnaq, M. A. Kishk, A. Celik, M.-S. Alouini, and T. Y. Al-Naffouri, âOptimal deployment of tethered drones for maximum cellular coverage in user clusters,â IEEE Trans. Wireless Commun., vol. 20, no. 3, pp. 2092â2108, Mar. 2021.

[30] Z. Mou, Y. Zhang, F. Gao, H. Wang, T. Zhang, and Z. Han, âDeep reinforcement learning based three-dimensional area coverage with UAV swarm,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3160â3176, Oct. 2021.

[31] X. P. Guo, C. Zhang, F. Z. Yu, and H. Chen, âCoverage analysis for UAVassisted mmWave cellular networks using Poisson hole process,â IEEE Trans. Veh. Technol., vol. 71, no. 3, pp. 3171â3186, Mar. 2022.

[32] Q. Xue, X. Fang, and C. X. Wang, âBeamspace SU-MIMO for future millimeter wave wireless communications,â IEEE J. Sel. Areas Commun., vol. 35, no. 7, pp. 1564â1575, Jul. 2017.

[33] T. Bai and R. W. Heath, âCoverage and rate analysis for millimeterwave cellular networks,â IEEE Trans. Wireless Commun., vol. 14, no. 2, pp. 1100â1114, Feb. 2015.

[34] Y. Cui, X. Fang, Y. Fang, and M. Xiao, âOptimal nonuniform steady mmWave beamforming for high-speed railway,â IEEE Trans. Veh. Technol., vol. 67, no. 5, pp. 4350â4358, May 2018.

[35] P. Liu, J. Blumenstein, N. S. PeroviÂ´c, M. Di Renzo, and A. Springer, âPerformance of generalized spatial modulation MIMO over measured 60 GHz indoor channels,â IEEE Trans. Commun., vol. 66, no. 1, pp. 133â148, Jan. 2018.

[36] Y. T. Liu, J. J. Yan, and X. H. Zhao, âDeep reinforcement learning based optimal transmission polices for opportunistic UAVs-aided wireless sensor network,â IEEE Internet Things J., vol. 9, no. 15, pp. 13823â13836, Aug. 2022.

[37] Y. Zeng, R. Zhang, and T. J. Lim, âThroughput maximization for UAVenabled mobile relaying systems,â IEEE Trans. Commun., vol. 64, no. 12, pp. 4983â4996, Dec. 2016.

[38] B. Lorenzo and S. Glisic, âOptimal routing and traffic scheduling for multihop cellular networks using genetic algorithm,â IEEE Trans. Mobile Comput., vol. 12, no. 11, pp. 2274â2288, Nov. 2013.

<!-- image-->

Jinsong Gui (Member, IEEE) received the BE degree from the University of Shanghai for Science and Technology, China, in 1992, and the MS and PhD degrees from Central South University, China, in 2004 and 2008, respectively. He is currently a professor with the School of Electronic Information, Central South University. He is the member of China Computer Federation (CCF). He published more than 60 international journal papers and more than 10 international conference papers. His research interests cover the general area of distributed systems, as well as related fields such as wireless network topology control, cloud and green computing, network trust and security.

<!-- image-->

Fujian Cai is currently working toward the masterâs degree with the School of Computer Science and Engineering, Central South University, China. Her research interests include edge computing, Internet of Things, wireless sensor networks, network simulation and performance evaluation.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist/page_10_img_1.png|page_10_img_1]]
3. [[../extracted_images/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist/page_20_img_1.jpeg|page_20_img_1]]
4. [[../extracted_images/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist/page_20_img_2.jpeg|page_20_img_2]]

---

