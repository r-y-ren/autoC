# A Two-Stage Strategy for UAV-Enabled Wireless Power Transfer in Unknown Environments

Junling Shi , Peiyu Cong, Liang Zhao , Member, IEEE, Xingwei Wang , Shaohua Wan , Senior Member, IEEE, and Mohsen Guizani , Fellow, IEEE

AbstractâDue to the outstanding merits such as mobility, high maneuverability, and flexibility, Unmanned Aerial Vehicles (UAVs) are viable mobile power transmitters that can be rapidly deployed in geographically constrained regions. They are good candidates for supplying power to energy-limited Sensor Nodes (SNs) with Wireless Power Transfer (WPT) technology. In this paper, we investigate a UAV-enabled WPT system that transmits power to a set of SNs at unknown positions. A key challenge is how to efficiently gather the locations of SNs and design a power transfer scheme. We formulate a multi-objective optimization problem to jointly optimize these objectives: maximization of UAVâs search efficiency, maximization of total harvested energy, minimization of UAVâs flight energy consumption and maximization of UAVâs energy utilization efficiency. To tackle these issues, we present a two-stage strategy that includes a UAV Motion Control (UMC) algorithm for obtaining the coordinates of SNs and a Dynamic Genetic Clustering (DGC) algorithm for power transfer via grouping SNs into clusters. First, the UMC algorithm enables the UAV to autonomously control its own motion and conduct target search missions. The objective is to make the energy-restricted UAV find as many SNs as feasible without any priori known location information. Second, the DGC algorithm is used to optimize the energy consumption of the UAV by combining a genetic clustering algorithm with a dynamic clustering strategy to maximize the amount of energy harvested by SNs and the energy utilization efficiency of the UAV. Finally, experimental results show that our proposed algorithms outperform their counterparts.

Index TermsâEnergy consumption optimization, sensor node (SN), target search, two-stage strategy, unmanned aerial vehicle (UAV), wireless power transfer (WPT).

Digital Object Identifier 10.1109/TMC.2023.3240763

## I INTRODUCTION

W IRELESS Sensor Networks (WSNs) have received sub-stantial attention for realizing smart cities, agriculture, stantial attention for realizing smart cities,agriculture, transportation and so forth [1], [2], [3]. In WSNs, Sensor Nodes (SNs) are sometimes energy-constrained and deployed to collect and report information about the surrounding environments. Since SNs are usually powered by batteries with limited power, it is almost impossible to provide long-term and high Quality of Service (QoS). Hence, it is critical to develop a technique that is capable of offering a reliable energy supply for WSNs [4]. Although wire-line charging is available as an option, wires are susceptible to breakage and cost, leading to energy limitations in WSNs. The alternate technology to extend the lifetime of WSNs is Wireless Power Transfer (WPT) which can be flexibly and quickly deployed in various scenarios. Typical WPT technologies include far-field directional Radio Frequency (RF) signals [5] and magnetic resonance coupling [6], where the RF-WPT can provide long-distance power transfer. According to [7], the WPT market was estimated to be worth US\$4.5 billion in 2021 and is expected to reach US\$13.4 billion by 2026.

Existing studies utilized ground chargers to transmit power to SNs [8], [9]. However, the efficiency of WPT that decreases rapidly with distance and the poor Line-of-Sight (LoS) transmission channel caused by obstacles limit the power transfer range. Although this issue can be solved with intense deployment, the economic cost will be tremendously high. Besides, it is difficult for ground chargers to enter some regions with complex terrains. Nowadays, Unmanned Aerial Vehicles (UAVs) are attracting increasing interest due to their distinct advantages such as low cost, high flexibility, and controllable maneuverability [10], which can make UAVs become new forms of wireless power transmitters. Compared with ground chargers, UAVs can not only benefit from higher-quality LoS communication channels but also can set up wireless links to SNs without facilities[11], [12]. Moreover, UAVs can fly near SNs to provide them with closer-range power transfer, further improving the transfer efficiency [13]. Therefore, UAV-enabled WPT is very promising for supplying power to SNs.

To better support the UAV-enabled WPT, clustering is a splendid option that can allow UAVs to transmit power to SNs in units of groups, thereby reducing the flying distance of UAVs [14]. For example, the authors in [15] first divide SNs into clusters, each of which contains a Center Node (CN) and a set of End Nodes (ENs) via genetic weighted clustering. CN is responsible for receiving power from the UAV and then distributing it to ENs in its cluster. The Traveling Salesman Problem (TSP) solution is utilized to generate an optimal path to transmit power to CNs. Compared with direct charging, this strategy enables more SNs to receive energy, which can better cope with emergencies where numerous SNs lack energy.

Nevertheless, most existing investigations on WPT rely on the premise that the coordinates of SNs are already known. Unfortunately, sometimes the destruction of infrastructure and facilities would cause the loss of location data for SNs. As a result, target search is required to collect the location information of these SNs. Currently, many technologies such as the Global Positioning System (GPS), RF and cameras are capable of assisting UAVs to search for static or mobile targets[16], [17]. There are already some studies investigating the UAV-enabled target search based on a apriori known target location probability map[18], [19], [20], [21], [22]. However, their strategies cannot successfully execute target search tasks without the acquisition of target location probability information in advance. Some literature also conducts target search with deep learning and reinforcement learning algorithms[23], [24], [25]. Although some machine learning algorithms have little dependence on apriori information, they necessitate plentiful training data before being put into practical application and the trained results may fail to be applicable to new environments.

Motivations: Before transferring power to SNs, they should be located because the lack of SNs location information will result in the chargers failing to generate appropriate flight trajectories, thereby wasting plenty of energy. However, due to environmental degradation or time constraints, gaining the location information of SNs in advance is not always possible. In consequence, a strategy should be developed for scenarios in the absence of apriori known position information about SNs. Furthermore, since the energy capacity of the UAV is restricted, its energy consumption should be optimized to maximize the power harvested by SNs.

To tackle the above problems, we put forward a two-stage strategy to assist the UAV to search and charge massive lowpower SNs with unknown positions across a vast region. We take advantage of $U A V _ { t s }$ and $U A V _ { w p t }$ to distinguish UAVs for different tasks. During the target search stage, a UAV Motion Control (UMC) algorithm based on the Artificial Potential Field (APF) is applied to assist the $U A V _ { t s }$ to search and store the locations and energy levels of SNs. APF is appropriate for scenarios in which there is no apriori information about SNsâ positions and can be put into the application without the prior training process. After target search, SNs should be charged by the $U A V _ { w p t }$ to resume their working status. For this purpose, we present a Dynamic Genetic Clustering (DGC) algorithm which encompasses a new fitness function for the genetic algorithm and a dynamic clustering strategy based on [15]. This work adopts a two-stage strategy instead of the simultaneous search and power transfer strategy so that after obtaining coordinate information about the majority of SNs in the given region by target search, a superior clustering scheme and UAV flight trajectory can be designed for the power transfer stage. Therefore, the UAV can fly along the optimized trajectory to reduce flight energy consumption.

Contributions: The main contributions of this paper are summarized as follows.

1) We consider a novel UAV-enabled WPT system that transmits power to a set of SNs at unknown positions. To deal with this situation, we propose a two-stage strategy that includes a UMC algorithm for target search and a DGC algorithm for power transfer.

2) The UMC algorithm is proposed to collect the coordinates and energy levels of SNs before transferring power to them, which requires no apriori target probabilities distribution in the given region. To the best of our knowledge, this is the first work that employs APF to search massive SNs without a apriori location information.

3) We present the DGC algorithm to transfer power to SNs. The energy utilization efficiency of the UAV is maximized via the dynamic clustering strategy, which allows the UAV to transfer more power to SNs instead of carrying its redundant remaining energy back to the starting point. Besides, we also design a new fitness function to enhance the DGC algorithmâs metric for selecting candidate populations, thus increasing the amount of energy harvested by SNs and reducing the UAVâs flight energy consumption.

The remainder of this paper is organized as follows. Related work is reviewed in Section II. The system model divided into three parts is described in Section III. The formulated problem is discussed in Section IV. Section V then provides the UMC algorithm and DGC algorithm in detail. Experimental simulations and results are shown in Section VI. Finally, the conclusion is drawn in Section VII.

## II RELATED WORK

The target search and power transfer problems have recently attracted widespread interest and various literature has been conducted to deal with multifarious demands and objectives. The literature is shown as follows.

## A Target Search

Given an unknown region, how to gather the location information of targets is an interesting issue. Yao et al. [18] developed a UAV offline path planning for river coverage search tasks based on the apriori likelihood probability of given area importance. Kashino et al. [19] presented a moving target search planning method for multi-UAV formation according to the target probability curve. A hybrid evolutionary algorithm was proposed in [20] to utilize UAVs to find missing tourists with location probabilities. Yao et al. [22] proposed a state predictor information fusion consensus algorithm based on UAVsâ predicted target probability maps. These studies rely heavily on the apriori information to design target search algorithms. There is also some literature utilizing machine learning algorithms with little reliance on apriori information to carry out target search. For example, Cao et al. [23] mastered the control strategy of the snake game through deep reinforcement learning, and then applied it to the UAV-enabled target search. Wu et al. [24] combined hierarchical reinforcement learning with the potential field method to search for static and dynamic targets in a threedimensional (3D) environment. Cao et al. [25] leveraged frontier detection and deep reinforcement learning to autonomously explore unknown underwater environments based on the grid map of the region. Unfortunately, the well-trained results required extensive training, which will cost a lot of time and resources [25], and thus may not be applicable in the real-world scenario in time.

The field of designing a target search strategy that dispenses with pre-training and apriori known target location information has drawn little attention. Brown et al. [26] presented a dynamic progressively spiral-out formation for a group of UAVs to perform an exhaustive search for a few moving ground targets and no apriori information about target locations was known. Yet, due to the requirements of Internet of Things (IoT), multiple SNs are normally deployed to enable connectivity and monitoring in large-scale areas. The problem of UAV-enabled searching a crowd of static on-ground SNs whose locations are unknown is more worthy of investigation.

## B Wireless Power Transfer

To restore the energy-deficient SNs to the working state, the UAV should transmit power to them. To this end, recent research efforts have investigated UAV-enabled power transfer. For instance, Hu et al. [27] were the first to propose that the optimal solution to the min-energy maximization issue in UAVenabled WPT systems must follow the successive-hover-and-fly trajectory design structure. Xu et al. [28] presented the Lagrange dual method to maximize the harvested energy and tackle the fairness issue among all SNs by optimizing the trajectory of the UAV under its maximum velocity constraint. Yang et al. [29] and Beak et al. [30] optimized the trajectory of the UAV as well as its hovering locations and duration to maximize the minimum harvested energy of SNs. Yuan et al. [31] investigated the trajectory design which took the nonlinear energy harvesting model into account to balance harvested energy among SNs. In addition to the research on fairness among SNs, there are some studies aiming at maximizing the received energy of SNs or the throughput of WSNs. Yan et al. [13] investigated the optimal hovering strategies for both 1D and 2D typologies to maximize the power received by SNs under UAVâs energy capacity constraint. Feng et al. [32] investigated an energy harvesting maximization by optimizing the UAV flight altitude and the wireless coverage while taking the UAVâs 3D positioning, charging time, and beam pattern into consideration. Mo et al. [33] investigated how to maximize the minimal power harvested by all SNs based on a radio-map-based placement optimization method in the case where the UAV only knew the SNsâ locations partially. Ye et al. [34] maximized the WSNs throughput while minimizing UAVâs energy consumption through convex optimization.

The above-mentioned studies mainly focused on the issues of transmitting power to small WSNs (WSN with an area less than 100 $m ^ { 2 }$ or the number of nodes less than 100 is defined as small WSN in this work, or large WSN otherwise). [15], [35], [36] studied the power transfer problem of large WSNs which is more suitable for the demand of intelligent life. Wu et al. [35] presented a heuristic algorithm to maximize the energy efficiency of UAVs while minimizing the communication delay in the multi-UAV enabled WSN. Sun et al. [36] aimed to optimize the power resource allocation strategy with the constraint of the apriority among different modes in wireless nodes. Pandiyan et al. [15] combined a genetic weighted clustering algorithm with a TSP solution to minimize the UAV flight distance and energy losses by distributing the power packets from the UAV to SNs in the form of clusters. This strategy can be used as an emergency measure to bring more SNs back to work in a short period of time and gather their stored information. However, if a considerable number of SNs receive too little power to support the transmission of information, this strategy will become meaningless. Besides, the issue of UAV energy utilization is also worth discussing.

## III SYSTEM MODEL

In this section, we introduce three parts of the system model, namely artificial potential field model, power transfer model and UAV energy consumption model. N SNs with unknown locations are considered in a given region. SNs are indexed by the set $\mathcal { N } = \{ 1 , \ldots , N \}$ , each of which is assumed to be unable to communicate with the other. Any location information about SNs in the given region cannot be obtained in advance and the UAV cannot get any assistance from the base station. We suppose that the UAV flies at a stable height above the ground when it is in flight. Note that $U A V _ { t s }$ and $U A V _ { w p t } \mathrm { { f l y } }$ at different altitudes to accomplish various tasks. At any time instant $t \in \tau$ / $q _ { u } ( t ) = ( x ( t ) , y ( t ) )$ represents the position of the UAV on the horizontal plane. After taking off from the starting point (0,0), the UAV performs tasks in the target region and finally returns to (0,0). In other words, the UAV has the identical take-off and landing position, i.e., $q _ { u } ( 0 ) = q _ { u } ( T ) = ( 0 , 0 )$ , where T is the end moment of the total duration of the entire task, ${ \mathcal { T } } \triangleq ( 0 , T ]$

In the first stage, the $U A V _ { t s }$ needs to take off from the starting point and cruise within the target zone to find the locations of ground SNs. The set of Searched SNs (SSNs) is $\mathcal { N } ^ { \prime } = \{ 1 , \ldots , N _ { s } \}$ and the coordinate of ith SSN $q _ { s } ( i )$ can be denoted as $( x _ { i } , y _ { i } )$ . The $U A V _ { t s }$ is assumed to be equipped with target recognition sensors that can sense the existence of SNs and achieve their energy levels $E _ { S N }$ [37]. The sensing radius of the $U A V _ { t s }$ is denoted as $R _ { s } .$ . SSNs provide repulsive forces for the $U A V _ { t s } .$ , enabling it to fly towards the unsearched area and continue hunting for the locations of undetected SNs. If the $U A V _ { t s }$ is in a dilemma of force balance, the position of the attractive force will be generated to release the $U A V _ { t s }$ from the dilemma.

After target search, the $U A V _ { t s }$ should return to the starting point and transmit the coordinate and energy level information of SSNs to the $U A V _ { w p t }$ after the target search mission. We assume that SSNs requiring energy are in a standby state. Then, the $U A V _ { w p t }$ equipped with power transfer components starts from the starting point to charge SSNs. Before the UAV begins a mission cycle, it is assumed to be fully charged. Each SSN is equipped with wireless power receiving units to obtain energy.

TABLE I MAIN PARAMETERS USED IN SYSTEM MODEL
<table><tr><td>Variable</td><td>Definition</td></tr><tr><td> $N$ </td><td>Number of sensor nodes</td></tr><tr><td> $N _ { s }$ </td><td>Number of searched sensor nodes</td></tr><tr><td> $K$ </td><td>Number of clusters</td></tr><tr><td> $q _ { u } ( t )$ </td><td>Location of the UAV at time instant t</td></tr><tr><td> $q _ { s } ( i )$ </td><td>Location of i-th SSN</td></tr><tr><td> $q _ { a }$ </td><td>Location of the attractive force</td></tr><tr><td> $E _ { U A V }$ </td><td>Energy level of the UAV</td></tr><tr><td> $E _ { S N }$ </td><td>Energy level of sensor node</td></tr><tr><td> $\overrightarrow { F _ { r } }$ </td><td>The repulsive force</td></tr><tr><td> $\overrightarrow { F _ { a } }$ </td><td>The attractive force</td></tr><tr><td> $\overrightarrow { F }$ </td><td>The resultant force</td></tr><tr><td> $d _ { 0 }$ </td><td>Influence radius of each SSN</td></tr><tr><td> $d _ { U N _ { n } }$ </td><td>Euclidean distance between the  $U A V _ { t , s }$  and n-th SN  $U A V _ { t , s }$ </td></tr><tr><td> $d _ { U S _ { i } }$ </td><td>Euclidean distance between the and i-th SSN</td></tr><tr><td> $\delta$ </td><td>Repulsion scale factor</td></tr><tr><td> $\xi$ </td><td>Attractiveness scale factor</td></tr><tr><td> $R _ { s }$ </td><td>The detection radius of the  $U A V _ { t s }$ </td></tr><tr><td> $R _ { c }$ </td><td>The radius of the cluster</td></tr><tr><td> $\gamma$ </td><td>Power transfer efficiency of  $U A V _ { w p t }$  to CN</td></tr><tr><td> $\gamma _ { p i }$ </td><td>Piezoelectric driver efficiency</td></tr><tr><td> $\gamma _ { a c }$ </td><td>Acoustic to direct-current efficiency</td></tr><tr><td> $t _ { w p t } ^ { \kappa }$ </td><td>Time for  $C N _ { k }$  to be fully charged</td></tr><tr><td> $P _ { w p t }$ </td><td>UAV power consumption for WPT</td></tr><tr><td> $P _ { p r o }$ </td><td>UAV power consumption for propulsion</td></tr><tr><td> $P _ { h o v }$ </td><td>UAV power consumption for hovering</td></tr><tr><td> $P _ { d r a g }$ </td><td>UAV power consumption for climbing</td></tr><tr><td> $H _ { w p t }$ </td><td>Hovering height for UAV power transfer</td></tr><tr><td> $E _ { r e c }$ </td><td>Sum of energy received by all SSNs</td></tr><tr><td> $E _ { f l y }$ </td><td>Flight energy consumption</td></tr><tr><td> $E _ { h o v }$ </td><td>Hovering energy consumption</td></tr><tr><td> $E _ { w p t }$ </td><td> WPT energy consumption</td></tr><tr><td> $v ( t )$ </td><td>The horizontal speed of the UAV at time t</td></tr><tr><td> $v _ { z }$ </td><td>Vertical speed of the UAV</td></tr><tr><td> $\eta _ { s }$ </td><td>Search efficiency</td></tr><tr><td> $\eta _ { c }$ </td><td>Energy conversion efficiency</td></tr><tr><td> $\eta _ { u }$ </td><td>Energy utilization efficiency</td></tr></table>

During the charging period, SSNs will be divided into a set of clusters $K = \{ 1 , \ldots , K \}$ and each cluster $k \in \mathcal { K }$ is composed of a CN and several ENs. The CN continues receiving power transmitted from the $U A V _ { w p t }$ until it gets fully charged and then drives the piezoelectric transducer to transfer acoustic power to ENs in its cluster[15]. The list of main modeling parameters is shown in Table I.

## A Artificial Potential Field Model

The APF model utilized by the UMC algorithm is based on [37], which is made up of two types of forces including the repulsive force $\overrightarrow { F _ { r } }$ and the attractive force $\overrightarrow { F _ { a } } \mathrm { : }$ (i) the repulsive force $\overrightarrow { F _ { r } }$ from the SSN pushes away the UAV to the unsearched area, (ii) the attractive force $\overrightarrow { F _ { a } }$ drags the UAV from force balance. We only study the effect of SSNs on the UAV motion on the two-dimensional plane. In other words, the repulsive force and the attractive force do not affect the height of the UAV. The details are shown as follows.

<!-- image-->  
Fig. 1. Repulsive forces generated by SSNs.

1) The Repulsive Force for Pushing the UAV: To enable the UAV to move away from the SSNs, we denote that $\Vec { F } _ { r } ^ { i }$ is the repulsive force generated by the $S S N _ { i }$ which can propel the UAV. The value of $\vec { F } _ { r } ^ { i }$ decreases with distance. We model the repulsive forces as follows,

$$
\begin{array} { r } { \overrightarrow { F _ { r } ^ { i } } = \left\{ \begin{array} { l l } { \overline { { \delta ( \frac { 1 } { d _ { U S _ { i } } } - \frac { 1 } { d _ { 0 } } ) ^ { 2 } } } , } & { R _ { s } \leq d _ { U S _ { i } } < d _ { 0 } } \\ { 0 , } & { d _ { U S _ { i } } \geq d _ { 0 } , } \end{array} \right. } \end{array}\tag{1}
$$

where $d _ { 0 }$ represents the influence radius of each SSN; dUS is the euclidean distance between the UAV and ith SSN; Î´ is the repulsion scale factor; UAVâs detection range is approximated as a circle with the radius of $R _ { s }$ . The repulsive force adopts the universal gravitation model whose direction is always towards the UAV. As illustrated in Fig. 1, repulsive forces take effect only when the distance between the UAV and SSNs is shorter than $d _ { 0 }$ $( \mathrm { i . e . , } S S N _ { 1 }$ and $S S N _ { 2 } )$ . Note that $d _ { U S _ { i } }$ should be larger than $R _ { s } ,$ , which prevents newly discovered SSNs within the detection range from obstructing the UAVâs forward movement. If the distance from the UAV to the SSN $d _ { U S _ { i } }$ exceeds the threshold $d _ { 0 } \ ( { \mathrm { i . e . , ~ } } S S N _ { 3 } )$ , this SSN will have no repulsive effect on the UAV. In other words, if $d _ { U S _ { i } }$ is larger than $d _ { 0 }$ , the value of $\Vec { F } _ { r } ^ { i }$ will become zero.

This model is appropriate because it directs the UAV away from SSNs and toward the unsearched area. Hence, the UAV will fly to the region without SSNs under the effect of repulsive forces and continue its search mission. The overall repulsive force that affects the UAVâs motion can be calculated as

$$
\overrightarrow { F _ { r } } = \overrightarrow { F _ { r } ^ { 1 } } + \overrightarrow { F _ { r } ^ { 2 } } + \cdot \cdot \cdot + \overrightarrow { F _ { r } ^ { i } } ,\tag{2}
$$

where i is the number of SSNs; $\vec { F } _ { r } ^ { i }$ is the repulsive force generated by the ith SSNs. The UAV will be affected by this resultant repulsive force if it is within the influence range of multiple SSNs. The resultant repulsive force is the vector sum of the repulsive force generated by each SSN.

2) The Attractive Force for Breaking Force Balance: As shown in Fig. 2, considering the case where the repulsive forces from SSNs make the UAV fall into force balance. In the ideal condition, UAVâs motion would stop if the resultant repulsive force on it is zero, which is too harsh and difficult to achieve. When the resultant force is minimal, the UAV will move slowly. In this work, the UAV is assumed to stop moving if the value of the resultant force is less than a threshold $F _ { t h }$ . We further introduce an attractive force to drag the UAV out of the dilemma of force balance. Specifically, we divide the target area into grids. The distance from each unsearched grid to each SSN is calculated and the shortest one will be chosen as the representative, and we call this distance S-distance for short. The grid with the longest S-distance will be selected as the location where the attractive force is generated, which can drag the UAV out of the force balance.

<!-- image-->  
Fig. 2. The attractive force for breaking force balance.

The attractive force is also based on the universal gravitation model, which is given by

$$
\overrightarrow { F _ { a } } = \overrightarrow { \xi \times d ( q _ { a } - q _ { u } ) } ,\tag{3}
$$

where Î¾ is the attractiveness scale factor; $q _ { a }$ is the position of the attractive force; $d ( q _ { a } - q _ { u } )$ is the euclidean distance between the UAV and the position of the attractive force. Since the attractive force should have more impact on the UAV than SSNs to generate enough force to drag the UAV from force balance, the value of $\overrightarrow { F _ { a } }$ should be larger than $\overrightarrow { F _ { r } ^ { i } }$

3) The Resultant Force Driving UAVâs Motion: The resultant force that drives the UAV to move can be obtained by the vector addition as follows,

$$
\vec { F } = \overrightarrow { F _ { r } } + \overrightarrow { F _ { a } } .\tag{4}
$$

According to Newtonâs second law of motion, the variation in speed is determined by the resultant force exerted on the UAV, which is

$$
\Delta \overrightarrow { v } = \overrightarrow { F } \cdot \Delta t / m = \overrightarrow { F } \cdot \Delta t ,\tag{5}
$$

where $\Delta t$ is the time the UAV moves; m is the UAVâs virtual quality which is set to 1 in this study for the convenience of calculation [37]. Note that if the UAV is at maximum speed, the forces applied to it will not have the effect of accelerating.

To evaluate different search schemes, we define a variable $\eta _ { s }$ to represent their search efficiency

$$
\eta _ { s } = \frac { n _ { s } } { T _ { t s } } ,\tag{6}
$$

where $n _ { s }$ is the number of SSNs; $T _ { t s }$ is the execution time of the target search task. It can be seen that the more SSNs found in a certain period, the higher the search efficiency.

## B Power Transfer Model

After collecting the location information of SNs via target search, the power transfer model is utilized. SNs equipped with rechargeable batteries can store the harvested energy through the power management unit when receiving power. The DGC algorithm can assign some nodes as CNs and the remaining nodes as ENs. CNs receiving power from the UAV will be fully charged before distributing power to the ENs in the clusters. If SNs are located within the power transfer range of one CN, they can operate in the power transfer mode and receive energy from the CN through the power management unit. This strategy has been demonstrated to lead a larger number of SNs to receive energy than the strategy of allowing the UAV to directly charge SNs. Note that CNs only distribute part of their energy to ENs because they also need energy to deliver their stored data. After charging the CN in one cluster, the UAV will continue transferring power to the CN in the next cluster, and the trajectory is designed by the TSP solution. The above-mentioned power transmission strategy is depicted in Fig. 3.

<!-- image-->  
Fig. 3. Illustration of wireless power transfer strategy.

It can be seen that two SSNs are not involved in any cluster, named $S S N _ { 1 }$ and SSN2, this is because their energy levels are above the threshold value (60% of SSNâs energy capacity EmaxSSN ). If these two SSNs make a charge request during the power transfer mission, they can wait for the next power transfer cycle. If a SN cannot be involved by any cluster due to being far away from other SNs, it is allowed to receive power from the UAV as a cluster with one SN.

The UAV to CN channel adopts LoS link and the free-space path loss model which are widely used in the existing work (e.g., [35], [38], [39]). The channel power gain between the UAV and $C N _ { k }$ at time $t \in T$ is expressed as

$$
h _ { u , k } ( t ) = \frac { \beta _ { 0 } } { \left\| q _ { C N _ { k } } - q _ { u } ( t ) \right\| ^ { 2 } + H _ { w p t } ^ { 2 } } ,\tag{7}
$$

where $\beta _ { 0 }$ is the channel power gain at the distance of 1 m; $H _ { w p t }$ is UAVâs hovering altitude for power transfer;  Â·  represents the euclidean norm. Since the hovering height of the UAV is fixed, the value of $h _ { u , k } ( t )$ can be approximated as stable. Furthermore, the noise power is substantially lower than the UAVâs energy transmit power, so the energy received from the noise can be negligible [35].

Since $h _ { u , k } ( t )$ and the RF energy harvesting efficiency $\gamma ^ { \prime }$ are both assumed to be stable in this work, for ease of exposition, we utilize Î³ to represent the relationship between the transmitted power of the UAV $P _ { w p t }$ and the received power of SNs $P _ { r e c } ,$ which is shown as

$$
P _ { r e c } = P _ { w p t } \cdot \gamma = P _ { w p t } h _ { u , k } ( t ) \gamma ^ { \prime } ,\tag{8}
$$

In the practical situation, the conversion of RF signal to DC power is a nonlinear process in energy harvesting [40]. For a CN, when considering this sophisticated model, the relationship between the harvested DC power $P _ { d c }$ and the received RF power $P _ { r e c }$ can be devised as follows

$$
P _ { d c } = \frac { \psi _ { d c } - P _ { M } \Omega } { 1 - \Omega } , \Omega = \frac { 1 } { 1 + e x p ( a b ) } ,\tag{9}
$$

where

$$
\psi _ { d c } = \frac { P _ { M } } { 1 + e x p ( - a ( P _ { r e c } - b ) ) } ,\tag{10}
$$

is a function of the received power. a reflects the nonlinear charging rate with respect to the input power; b determines the minimum turn-on voltage of the power harvesting circuit; $P _ { M }$ is the SNâs maximum harvested power.

The total time of CNs in all the clusters to be fully charged is represented as $T _ { w p t }$ , and it is given by

$$
T _ { w p t } = \sum _ { k = 1 } ^ { K } t _ { w p t } ^ { k } = \sum _ { k = 1 } ^ { K } \frac { E _ { C N _ { k } } ^ { m a x } - E _ { C N _ { k } } - E _ { s } } { P _ { d c } } ,\tag{11}
$$

where $E _ { C N _ { k } } ^ { m a x }$ is the energy capacity of the $C N _ { k } ; E _ { C N _ { k } }$ is the energy level of $C N _ { k }$ before receiving power from the UAV; $P _ { r e c }$ is the harvested power of CN; the UAV has static power of emitting energy $P _ { w p t }$ to charge CNs; Î³ is designed to represent the efficiency of UAV to CN power transfer. The energy consumption of SSNs in the standby state has been assumed to be $E _ { s }$ based on [15]. It is observed that $T _ { w p t }$ is the sum of the time to charge the CN of each cluster that the UAV arrives at. After the energy of the CN reaches saturation, it will actuate the piezoelectric driver with the efficiency of $\gamma _ { p i }$ and convert acoustic power to direct-current with the efficiency $\gamma _ { a c }$ for the acoustic power transfer which has been studied experimentally before for WPT[41]. The CN distributes part of its energy to ENs in the cluster and they can continuously receive power from the CN until its energy level drops to a preset threshold. The channel model between CN and ENs in a cluster and the calculation of the energy levels of ENs can be found in [15], which has taken into account the distance, channel loss, transmission efficiency and other factors.

## C UAV Energy Consumption Model

We consider three energy-consuming actions of UAVs during the mission period including flight, hovering and power transfer. Wherein, the overall energy consumption $E _ { w p t }$ of the UAV for WPT can be figured out by substituting the result o $: T _ { w p t }$ in (11) into (12). The UAV is assumed to have stable transmit power $P _ { w p t }$ when delivering energy to CNs. Therefore, the energy consumption of power transfer $E _ { w p t }$ can be expressed as

$$
E _ { w p t } = P _ { w p t } \cdot T _ { w p t } ,\tag{12}
$$

In addition to transferring energy to SNs, the UAV also requires to consume maneuvering energy which needs to be

considered in both mission phases. The propulsion power consumption is given by

1\2

$$
\begin{array} { l } { { \displaystyle P _ { p r o } ( V ) = P _ { 0 } \left( 1 + \frac { 3 V ^ { 2 } } { U _ { t i p } ^ { 2 } } \right) + P _ { j } \left( \sqrt { 1 + \frac { V ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { V ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) } } \\ { { \displaystyle ~ + \frac { 1 } { 2 } d _ { 0 } \rho s A V ^ { 3 } } , } \end{array}\tag{13}
$$

where $P _ { 0 }$ and $P _ { j }$ are two constants relevant to the physical parameters of the UAV and the environments, respectively; $U _ { t i p }$ is the tip velocity of the rotor; $v _ { 0 }$ is the mean rotor induced speed in hover; $d _ { 0 }$ and s denote the fuselage drag ratio and rotor solidity respectively; $\rho$ is the air density and A is rotor disc area. More details about this model can be found in [42]. The maneuvering energy includes hovering and flying, denoted as $E _ { h o v }$ and $E _ { f l y } .$

By substituting $V = 0$ in (13), the power of hovering $P _ { h o v }$ is expressed as

$$
P _ { h o v } = P _ { p r o } ( V = 0 ) = P _ { 0 } + P _ { j } .\tag{14}
$$

When the UAV reaches above the CN of each cluster, energy is transmitted to the CN in preparation for the power transmission to ENs in the cluster. The hovering energy consumption for charging CN can be derived as

$$
E _ { h o v } = P _ { h o v } \cdot T _ { h o v } ,\tag{15}
$$

$$
T _ { h o v } = T _ { w p t } ,\tag{16}
$$

where $T _ { h o v }$ is the hovering time required for the UAV to charge CNs in all clusters. Since the hovering of the UAV aims to transmit power to CNs, $T _ { h o v }$ and $T _ { w p t }$ are equal. As a result, we can calculate the value of $E _ { h o v }$ by taking $T _ { w p t }$ in (11) into (15).

To simplify the calculation, the UAV is assumed to move at a constant velocity $v _ { m a x }$ between clusters when charging SNs in the power transfer phase, and the energy consumption of the UAV during acceleration and deceleration is neglected [35], [43]. However, the influence of acceleration and deceleration on the speed of the UAV is not ignored. Therefore, the velocity of the UAV v(t) at different times is not always the same. The energy required for the flight can be calculated as follows

$$
E _ { f l y } = \int _ { 0 } ^ { T _ { f l y } } P _ { p r o } ( V = v ( t ) ) d t ,\tag{17}
$$

where $T _ { f l y }$ indicates the flight time required by the UAV, including taking off from the starting point, flying between SNs (target search phase) or between clusters (power transfer phase), and returning to the starting point. Moreover, if the UAV moves between clusters, it can fly at a higher altitude to avoid obstacles on the ground. However, when the UAV hovers over the CN for power transfer, it can approach the CN in the cluster as close as possible to obtain higher power transfer efficiency. Hence, suppose that there is no obstacle between the two, and the altitude can be shortened to 1 m. After the UAV completes the task of charging the CN, it can continue to climb to the flight altitude and proceed to the next cluster. Therefore, the additional power consumption of the vertical flight $E _ { d r a g }$ is given by

$$
P _ { d r a g } = \frac { 1 } { 8 } C \rho A v _ { z } ^ { 3 } ,\tag{18}
$$

where $C$ is the profile drag coefficient depending on the rotor blades; A is the total area of rotor disks and $v _ { z }$ is the vertical speed of the UAV.

The sum of energy required by the UAV to climb after transmitting power to CNs is shown as follows

$$
E _ { d r a g } = \sum _ { k = 1 } ^ { K } P _ { d r a g } \cdot \frac { H _ { f } - H _ { w p t } } { v _ { z } } ,\tag{19}
$$

where $H _ { f }$ is denoted as the altitude of UAV flight and $\frac { H _ { f } - H _ { w p t } } { v _ { z } }$ is the time of the vertical flight.

In addition, We consider the communication energy consumption of the UAV based on [30]

$$
E _ { c o m } = k _ { n } \Big ( \epsilon _ { e l } + \epsilon _ { a m p } \Big ( \| q _ { C N } - q ( t ) \| ^ { 2 } \Big ) + H ^ { 2 } \Big ) ,\tag{20}
$$

where $k _ { n }$ represents the size of the information that needs to be collected or sent; $\epsilon _ { e l }$ and $\epsilon _ { a m p }$ are two constants related to the energy consumption of collecting information. This model is utilized for energy consumption for recognizing SNs and communicating with them to collect information about their energy levels and positions during the target search mission.

The UAVâs overall energy consumption comprises flying, hovering, power transmission, and taking off and landing at the starting point during power transfer. In order to explore how the UAV accomplishes the power transfer task efficiently, we define a new variable named UAV energy conversion efficiency which is given by

$$
\eta _ { c } = \frac { E _ { S S N } ^ { r e c } - E _ { s } } { E _ { U A V } ^ { m a x } - E _ { U A V } ^ { r e } } ,\tag{21}
$$

$$
E _ { S S N } ^ { r e c } = \sum _ { i = 1 } ^ { n _ { s } } ( E _ { S S N _ { i } } ( T _ { w p t } ) - E _ { S S N _ { i } } ( 0 ) ) ,\tag{22}
$$

where $E _ { S S N } ^ { r e c }$ is the sum of energy harvested by all SSNs; $T _ { w p t }$ is the total time of the $U A V _ { w p t }$ transferring power to CNs; $E _ { S S N _ { i } } ( 0 )$ and $E _ { S S N _ { i } } ( T _ { w p t } )$ are the energy levels of the SSNi before and after receiving energy, respectively. $E _ { U A V } ^ { r e }$ is the remaining energy of the UAV after returning to the starting point and $E _ { U A V } ^ { m a x }$ is the energy capacity of the UAV. Hence, the value of $\eta _ { c }$ can be calculated. Observe that the lower UAVâs flight energy consumption and the higher energy used for WPT, the higher the energy conversion efficiency.

To explore the influencing factors of energy utilization efficiency of the UAV, another variable $\eta _ { u }$ is created which can be computed as follows

$$
\eta _ { u } = \frac { E _ { U A V } ^ { m a x } - E _ { U A V } ^ { r e } } { E _ { U A V } ^ { m a x } } ,\tag{23}
$$

it can be seen that the higher the energy consumption of the UAV to perform the task of power transfer, the higher its energy utilization efficiency will be.

## IV PROBLEM FORMULATION

The issue of target search and energy consumption optimization in the UAV-enabled WPT system is formulated into three sub-problems. First, the search efficiency of the UAV in the target search phase should be maximized to find as many SNs as possible. Hence, the value of $\eta _ { s }$ which is defined as the UAVâs search efficiency requires to be maximized. Second, the amount of energy harvested by SNs during the power transfer phase should be increased while the flight energy consumption of the UAV should be minimized. To achieve this purpose, we should maximize the value of $\eta _ { c }$ which is defined as the energy conversion efficiency in (16). Third, the residual energy of the UAV after completing the WPT mission should be as small as possible, implying that we need to enhance the energy utilization efficiency of the UAV, which can be accomplished by the maximization of $\eta _ { u } .$ . In summary, the values of variables Î·s, $\eta _ { c }$ and $\eta _ { u }$ should be jointly optimized. Accordingly, this multi-objective optimization problem can be formulated as

$$
( P 1 ) : \operatorname* { m a x } _ { q , V , E } \qquad ( \eta _ { s } , \eta _ { c } , \eta _ { u } )\tag{24}
$$

$$
\mathrm { s . t . } \quad 0 \leq x ( t ) \leq a , a > 0 ,
$$

$$
0 \leq y ( t ) \leq b , \ b > 0 ,\tag{24a}
$$

(24b)

$$
E _ { \Theta } \leq E _ { U A V } \leq E _ { U A V } ^ { m a x } , ~ E _ { \Theta } > 0 ,\tag{24c}
$$

$$
0 \leq v ( t ) \leq v _ { m a x } ,\tag{24d}
$$

$$
q ( 0 ) = q ( T ) ,\tag{24e}
$$

$$
0 \leq E _ { C N _ { k } } \leq E _ { C N _ { k } } ^ { m a x } ,\tag{24f}
$$

$$
E _ { C N _ { k } } ^ { m a x } - E _ { C N _ { k } } \leq P _ { d c } \cdot t _ { w p t } ^ { k } .\tag{24g}
$$

Here, the limitations involve coordinate and speed limits for the UAV as well as energy limits for the UAV and SSNs. Constraints (24a) and (24b) represent the area restrictions when the UAV is in flight. Constraint (24c) is the energy limitation of the UAV, where $E _ { \Theta }$ is the energy threshold to ensure that the UAV can be back to the take-off point. The UAVâs velocity is restricted by constraint (24d). Constraint (24e) indicates that the UAVâs starting point is the same as the ending point. (24f) is the constraint for the energy level of each CN, and (24g) is the constraint on the amount of energy that each CN can receive from the UAV. As a result, the first sub-problem in Problem (P1) can be addressed by the UMC algorithm, while the remaining sub-problems can be solved by the DGC algorithm.

## V UAV MOTION CONTROL AND DYNAMIC GENETIC CLUSTERING ALGORITHM

In this section, we aim to devise algorithms for the two-stage strategy to facilitate searching and charging SNs with unknown locations. This problem is formulated as Problem (P1), which is divided into two parts, i.e., maximizing the search efficiency of the $U A V _ { t s }$ in the target search phase and optimizing the energy consumption of the $U A V _ { w p t }$ in the power transmission phase. The first part in P1 can be tackled by the UMC algorithm. During the target search phase, the $U A V _ { t s }$ should follow the constraints (24a)â(24e) in P1. The second subproblem is to jointly optimize the UAVâs energy conversion efficiency and energy utilization efficiency. To deal with this problem, we present a DGC algorithm that combines genetic clustering with the TSP solution. The $U A V _ { w p t }$ for power transfer should follow the constraints (24a)â(24g). The overall work carried out in this paper is depicted in Fig. 4.

<!-- image-->  
Fig. 4. Workflow of the solution to P1.

The UMC algorithm is based on the APF method to generate virtual forces. The basic idea of the conventional APF is to treat the motion of the robot in the environment as the movement in a virtual artificial force field. The attractive force generated by the goal point drags the robot, while the repulsive force of the obstacle repels it. Finally, the motion of the robot is controlled by the calculated resultant force. Here, the UMC algorithm based on the APF method is utilized to control the UAVâs motion to search for the positions of SNs. After the target search stage, the $U A V _ { w p t }$ receives SSNsâ information which refers to the location and energy level information of SSNs. We adopt the DGC algorithm to first divide SSNs into clusters, each of which consists of a CN and some ENs. Then a trajectory can be designed by the TSP solution for the UAV power transmission task. This strategy can be used as a contingency measure for SNs to gain some energy to resume their working state. Note that both the UMC algorithm and the DGC algorithm can work solely. In other words, after the $U A V _ { t s }$ completes a round of target search task and transmits the location and energy level information about SNs to the $U A V _ { w p t }$ , it can start the next task at any time if conditions permit, i.e., the UAVâs energy is sufficient and some SNs have not been found. In the same way, if some SNs have not received energy after the $U A V _ { w p t }$ completes one round of missions, they can also wait for the next round of charging mission.

## A UAV Motion Control Algorithm

Each SN $n \in N$ is randomly distributed in the given region. The locations of SNs are supposed to be unknown. Hence, the $U A V _ { t s }$ needs to collect the coordinates and energy levels information of SNs through the UMC algorithm in the first stage of the two-stage strategy in preparation for the following WPT mission. Furthermore, this approach does not require each SNâs position information in advance. The $U A V _ { t s }$ can discover the SNs by using target recognition sensors and autonomously controlling its motion towards the unsearched region. The core principle of UAV-enabled target search is to model this demand as a virtual force field and the UAV will move towards its proper position by following the force field. The pseudo-code of UMC is described in Algorithm 1.

Algorithm 1: UAV Motion Control Algorithm.   
Input:   
UAVâs initial energy EmaxUAV , UAVâs initial velocity $\overrightarrow { v _ { m a x } } .$   
UAVâs sensing radius $R _ { s } ;$   
Output:   
The coordinates $\left\{ \left( x _ { 1 } , y _ { 1 } \right) , \ldots , \left( x _ { i } , y _ { i } \right) \right\}$ and energy levels   
$\{ E _ { S S N _ { 1 } } , \ldots , E _ { S S N _ { i } } \}$ of SSNs.   
1: The UAV takes off from the origin point (0,0);   
2: i â 1;   
3: while $( E _ { U A V } < E _ { \Theta } \mathrm { A N D } i < N )$ do   
4: if $\left( d _ { U N _ { i } } < R _ { s } \right)$ then   
5: The UAV senses and stores the location and   
energy level of $S N _ { n } ;$   
6: $S S N _ { i }  S N _ { n } ;$   
7: $i + + ;$   
8: end if   
9: if $( d _ { U S _ { i } } < d _ { 0 } \mathrm { A N D } d _ { U S _ { i } } \geq R _ { s } )$ then   
10: $S S N _ { i }$ exerts the repulsive force $\vec { F } _ { r } ^ { i }$ to the UAV   
according to (1);   
11: else   
12: $\overrightarrow { F _ { r } ^ { i } }  0$ ;   
13: end if   
14: The resultant repulsive force $\overrightarrow { F _ { r } }$ is determined by   
$( 2 ) ;$   
15: if $( | \overrightarrow { F _ { r } } | < F _ { t h } )$ then   
16: Create a position to generate an attractive force   
$\overrightarrow { F _ { a } }$ according to (3);   
17: Calculate the resultant force $\vec { F }$ according to   
(4);   
18: end if   
19: Change the velocity $\overrightarrow { v ( t ) }$ according to (5);   
20: Calculate $E _ { f l y }$ according to (17);   
21: $E _ { U A V }  E _ { U A V } - E _ { f l y } ;$   
22: end while   
23: return $\{ q _ { s _ { 1 } } , \ldots , q _ { s _ { i } } \}$ and $\{ E _ { S S N _ { 1 } } , \ldots , E _ { S S N _ { i } } \} .$

1) Initialization (Step 1-Step 3): set both take-off and landing positions of the UAV as (0,0). The energy level of the UAV is $E _ { U A V } ^ { m a x }$ when it takes off from the starting point. The storage space of the UAV is assumed to be sufficient to store the locations and energy levels information of SSNs. If the UAVâs energy level falls below the amount of energy required to return to the starting point or all unknown SNs have been located, the search mission ends.

2) Detection of SNs (Step 4-Step 8): the distance between the UAV and $S N _ { n }$ is represented by $d _ { U N _ { n } }$ . Once an unsearched SN enters the detection range of the UAV (i.e., $d _ { U N _ { i } } < R _ { s } )$ its energy level and location information will be detected and stored by the UAV, and this SN will become a SSN. Next, this

SSN will exert a repulsive force on the UAV to propel it towards the unsearched area.

3) Calculation of Repulsive Forces (Step 9-Step 14): if the euclidean distance between the UAV and ith SSN $d _ { U S _ { i } }$ is less than the influence radius $d _ { 0 }$ and greater than $R _ { s } , S S N _ { i }$ will generate a repulsive force to propel the UAV towards the unsearched area. Otherwise, $S S N _ { i }$ cannot affect the movement of the UAV. The reason for making the effective range of the repulsion force larger than $R _ { s }$ is to prevent the new SSNs within the UAVâs detection range from affecting the UAV moving forward. The resultant repulsive force acting on the UAV can be calculated by (2).

4) Generation of the Attractive Force (Step 15-Step 18): if only repulsive forces from SSNs act, the UAV will fall into force balance when acting with equal repulsive forces from opposite directions. In other words, if the resultant repulsive force is smaller than $F _ { t h }$ , the movement of the UAV will stop and the target search mission cannot continue. To deal with such an issue, an attractive force is created to make the UAV out of force balance (as shown in Fig. 2). Furthermore, the generating position of the attractive force should be considered because inappropriate attractive force positions may frequently lead the UAV into the searched area, resulting in the waste of the UAVâs energy. Hence, we divide the region into grids and then find a grid far away from SSNs as the position of the attractive force. Specifically, we first calculate the distance between each unsearched grid and SSNs and take the S-distance as the representative. Then, we select the grid with the longest S-distance to generate the attractive force. After determining the attractive forceâs position, the resulting force will be recalculated according to (4). Based on this method, we present the following two strategies to generate the position of the attractive force:

Reach Grid Strategy (RGS): create an attractive force at the grid with the longest S-distance and the attractive force disappears when the UAV reaches this grid.

Maximum Speed Strategy (MSS): create an attractive force at the grid with the longest S-distance and the attractive force disappears when the UAV reaches its maximum speed.

If the resultant force acting on the UAV makes its velocity less than $V _ { t h }$ while the attractive force is in effect, we set the value of repulsive forces to 0 so that the UAV can reach its maximum velocity quickly.

5) Calculation of UAVâs Velocity (Step 19-Step 22): based on the obtained location information, the UAV can calculate the resultant force which includes the attractive force from the calculated position and repulsive forces from SSNs. The real-time velocity of the UAV can be determined by (5). Note that if the UAV is at its maximum speed, the UAV will maintain its velocity even if the force acting on the UAV has an acceleration effect. (15) can be used to calculate the flight energy consumption of the UAV.

## B Dynamic Genetic Clustering Algorithm

After receiving the information about SSNs gathered in the target search stage, the $U A V _ { w p t }$ should start the power transfer task. Assume that the $U A V _ { w p t }$ is fully charged (i.e., $E _ { U A V } =$ $E _ { U A V } ^ { m a x } )$ when it takes off from the origin point (0,0). Before the WPT mission, the $U A V _ { w p t }$ should take advantage of the DGC algorithm to form the SSNs into clusters and then provide an optimized path via the TSP solution. In brief, after the locations of CNs are determined, the nearest CN to the UAV is selected as the next target point. We adopt the strategy that each cluster consists of a CN and some ENs. CN harvests power from the UAV and then distributes it to ENs. The specific definitions of crossover, mutation and penalty function in the genetic algorithm can be found in [15]. The pseudo-code of DGC is shown in Algorithm 2.

Algorithm 2: Dynamic Genetic Clustering Algorithm.   
Input:   
The coordinates $\left\{ \left( x _ { 1 } , y _ { 1 } \right) , \ldots , \left( x _ { i } , y _ { i } \right) \right\}$ and energy levels   
$\{ E _ { S S N _ { 1 } } , \ldots , E _ { S S N _ { i } } \}$ of SSNs, UAVâs initial velocity   
$\overrightarrow { v _ { m a x } } , \mathrm { U A V ^ { \circ } s }$ initial energy $E _ { U A V } ^ { m a x } ;$   
Output:   
Optimized clusters of SSNs and UAV flight path.   
1: The UAV takes off from the origin point $( 0 { , } 0 ) ;$   
2: Set the clustering constants $( k _ { m a x } , R _ { c } , C R , I , p , E _ { \Theta } ) ;$   
3: $E _ { w p t }  0 ;$   
4: $l \gets 1 ;$   
5: while $( l < 2 )$ do   
6: Initialize p parental populations;   
7: $I  0 ;$   
8: Evaluate each parental population through the   
fitness function $f ;$   
9: while $( I \leq I _ { m a x } )$ do   
10: Perform the crossover and mutation operation   
to generate offsprings;   
11: Evaluate the fitness function for the new   
populations;   
12: Select the new populations which have greater   
values of $f ;$   
13: $I + + ;$   
14: end while   
15: Store the coordinates of CNs in $U A V _ { p a t h } ;$   
16: Utilize TSP solution to generate $U A \dot { V } _ { p a t h } ^ { o p t } ;$   
17: Record $E _ { U A V } ^ { r e }$ and calculate $E _ { w p t } ^ { \prime }$ according to   
(11) and (12);   
18: if $( E _ { S S N } ^ { r e c } < E _ { S S N , } ^ { r e c ^ { \prime } } \mathrm { A N D } \ E _ { U A V } ^ { r e } \geq E _ { \Theta } )$ then   
19: $E _ { S S N } ^ { r e c }  E _ { S S N } ^ { r e c ^ { \prime } } ;$   
20: $l \gets 1 ;$   
21: Revise the value of $k _ { m a x }$ and $\mathit { R _ { c } } \mathrm { ; }$   
22: else   
23: $l + + ;$   
24: end if   
25: end while   
26: return $U A V _ { p a t h } ^ { o p t } .$

1) Initialization (Step 1-Step 7): the genetic algorithm begins by estimating the maximum number of clusters $k _ { m a x }$ that can be formed. The value of $k _ { m a x }$ is determined by the approximate energy consumption of the UAV for traversing all clusters and its energy level. Specifically, the value of $k _ { m a x }$ is set as the number of CNs that the UAV can charge with a portion of its energy capacity. The maximum cluster radius $R _ { c }$ is also set. The number of iterations I is initialized as 0 and its maximum value is $I _ { m a x }$ . The value of l, which determines whether the loop statement can continue, is set to 1. If l equals 2, the loop is ended, otherwise, it continues.

Assume that i SSNs have requests for charging and randomly select k SSNs as CNs. The rest SSNs are assigned to one of these clusters if they are within the energy transmission range of one CN. This process is repeated until p parental populations are formed. Furthermore, in some dense areas, a CN may be overloaded by allocating too many ENs. Hence, a penalty function is utilized to isolate the dense clusters and divide a large cluster into several smaller clusters.

2) Fitness Function (Step 8 and Step 11-Step 14): when utilizing the genetic algorithm, a fitness function is necessitated as a criterion for evaluating each candidate population, and the most promising population is ultimately selected. Each population represents a clustering policy that includes the number and radius of clusters, as well as CNâs location and ENsâ distribution for each cluster. A good fitness function can enhance the metric of candidate populations for a better selection of them. One of our objectives is to improve the value of $\eta _ { c } ,$ , which is achieved by increasing the amount of energy harvested by SSNs and decreasing the flight energy consumption of the UAV. In consequence, both aspects should be considered when designing the fitness function, which can be expressed as

$$
f = \left\{ \begin{array} { l l } { \frac { \alpha { \cdot } E _ { S S N } ^ { r e c } } { E _ { U A V } ^ { m a x } { - } E _ { U A V } ^ { r e } } , } & { E _ { U A V } ^ { r e } \geq E _ { \theta } } \\ { - 1 , } & { E _ { U A V } ^ { r e } < E _ { \theta } , } \end{array} \right.\tag{25}
$$

where $E _ { U A V } ^ { r e }$ is the remaining energy when the UAV decides to return to the starting point; the amount of energy received by SSNs $E _ { S S N } ^ { r e c }$ can be obtained by (22) while the UAVâs maneuvering energy consumption including hovering and flight can be calculated by (13) and (17). Since the energy harvested by SSNs is fairly minor compared to the UAV maneuvering energy, we introduce a variable Î± to narrow the numerical gap between the numerator and the denominator of the fitness function. In this work, the value of Î± is set as 100. The more energy SSNs harvested and the less maneuvering energy consumption of the UAV, the better fitness of this population. The value of the fitness function is set as -1 if the UAV runs out of power during the charging cycle.

3) Crossover (Step 10): crossover is the probability process of producing offspring who will inherit the genes of the parent population. The role of crossover is to ensure the stability of the population and make it evolve towards the optimal solution. The Cross-Ratio (CR) parameter, which determines the percentage of genes permitted to crossover between two different parental populations, is used to govern the 2-point crossover method in this study. SSNs in clusters belonging to different candidate populations are selected for exchange. Specifically, suppose that there are two candidate populations, then cluster 1 and cluster 2 are respectively selected from these two populations based on the set CR. Next, SSNs are chosen from the two selected clusters for exchange. Note that all clusters in the candidate populations need to follow this operation. Moreover, there may be duplicates in some clusters after the crossover process. Hence, the final step of the crossover is to eliminate duplicates in all clusters.

4) Mutation (Step 10): different from crossover operation, the mutation is caused by duplication errors of a single parental population during the replication operation, resulting in a new candidate being generated. The purpose of mutation is to maintain population variety and prevent local convergence induced by crossover. Due to the random nature of the crossover procedure, certain nodes in the populationâs cluster may be outside the energy transmission range of the CN. As a result, the mutation step is supplied to modify the candidate population. We adopt swap mutation to investigate this step, in which two SSNs are randomly chosen from two separate clusters in one population and then switched. After mutation, a scan for each population is conducted to prevent the situation of nodes overlapping.

5) Dynamic Clustering Strategy (Step 15-Step 24): once the iteration of the genetic algorithm is completed, the UAV stores the coordinates of CNs and generates an optimal path for charging SSNs. The number of formed clusters $k _ { m a x }$ is fixed in the original work [15]. However, $k _ { m a x }$ may be insufficient when dealing with large WSNs, which results in some SSNs not being allocated to any clusters and being unable to receive power. In addition, as a result of the workload limitation, the UAV would carry much energy back to the starting point. Since plenty of SNs lack energy and the UAVâs energy capacity is limited, its carried energy should be utilized to perform the WPT task as much as possible rather than being brought back to the starting point redundantly. In other words, when the UAV returns, its residual energy should be as low as possible.

Hence, a dynamic clustering strategy is presented to improve the energy utilization efficiency of the UAV defined in (23) and the amount of energy received by SSNs. Specifically, $k _ { m a x }$ should be adjusted to aggregate more SNs into more clusters, which allows the UAV to devote more energy to the power transfer task. Moreover, the dynamic clustering strategy can also improve the power transfer efficiency between CN and ENs in the cluster. This is because the number of clusters rising will lead to competition among some clusters for ENs and these ENs will choose the CN that is close to them, which can reduce the power transfer distance. The shortening of the distance between the CN and ENs can reduce the power transmission path loss, allowing ENs to receive more power. Besides, SNs receiving power as CNs that are not included by any clusters may increase, which can also make the total energy received by SNs increase. Despite this, the value of $k _ { m a x }$ cannot increase indefinitely because the UAVâs energy may be insufficient to support traversing all clusters and an overabundance of power-distribution CNs would reduce the total energy harvested by SSNs. To address this issue, we first introduce a variable named $E _ { U A V } ^ { r e }$ to restrict the growth of $k _ { m a x } ,$ i.e., the growth of $k _ { m a x }$ must be based on the premise of $E _ { U A V } ^ { r e } > E _ { \Theta }$ . The value of $E _ { \Theta }$ is defined as the sum of the UAV flight energy consumption from the CN of the current cluster to the CN of the next cluster, the CN of the next cluster to the starting point and landing. Second, we define $E _ { S S N } ^ { r e c ^ { \prime } }$ as the sum of energy harvested by SSNs after modifying the number of clusters and compare it with $E _ { S S N } ^ { r e c }$ before the change to identify the number of clusters. The DGC algorithm will come to a halt if the number of clusters grows to a point where the total energy harvested by SSNs decreases. Although the UAV spends most of its energy flying instead of charging CNs, the energy that the UAV spends on the flight is to move between clusters, which is part of the power transfer mission. Hence, the higher flight energy consumption indicates a higher number of UAV movements between clusters, which reflects more CNs obtaining power.

## C Complexity Analysis and Signal Overhead

This section presents the time complexity analysis and signal overhead for the two proposed algorithms. The details are shown below.

1) UMC Algorithm: the main time of this algorithm is spent on calculating the generation of the attractive force. $N _ { s }$ is the number of SSNs and $g$ is the number of grids divided. All the SSNs and grids should be traversed before determining the position of the attractive force. Suppose that all SNs have been found or the UAV energy is exhausted, a total of $N _ { a }$ times to find the position of the attractive force is required. Therefore, the time complexity of the UMC algorithm is $O ( N _ { a } \cdot N _ { s } \cdot g )$ For the signal overhead, it is assumed that the signal overhead of collecting the location and energy level information of a SN is B Bytes, so the signal overhead of executing the UMC algorithm once is $N _ { s } \cdot B$ Bytes.

2) DGC Algorithm: according to [15], the time complexity of finding CNs is $O ( I \cdot p ^ { 2 } )$ , where p is the number of the parental populations and I is the number of iterations. Running the TSP algorithm has a complexity of $O ( k ^ { 2 } )$ , where k is the number of CNs. Since k is limited and its value is far less than $I \cdot p ^ { 2 }$ , the time complexity of the genetic algorithm is $O ( I \cdot p ^ { 2 } )$ Besides, we proposed a dynamic clustering strategy to improve the energy utilization efficiency of the UAV. Assume that it takes $N _ { t }$ iterations for the algorithm to end. Hence, the total time complexity of the DGC algorithm is $O ( N _ { t } \cdot I \cdot p ^ { 2 } )$ . In addition, the main action of $U A V _ { w p t }$ that incurs communication overhead is the transmission of information about locations and energy levels of SNs with $U A V _ { t s }$ . Hence, the communication overhead of the power transfer phase is the same as that of the target search phase, i.e., $N _ { s } \cdot B$ Bytes.

## D Practical Implementation

For the practical implementation of our proposed solution, we have summarized three factors that need to be considered. First, the UAV should move at an altitude $H _ { t s }$ to avoid obstacles on the ground when performing the target search task or moving between clusters when performing power transfer. Second, the $U A V _ { t s }$ should be equipped with components such as GPS to get the location of SNs. Third, when the $U A V _ { w p t }$ is hovering to transmit power to SNs on the ground, its altitude should be as low as possible to reduce the power transmission path loss. Fourth, due to the limited energy capacity of the UAV, on one hand, the energy level of the UAV during the mission needs constant attention to prevent its remaining energy could not make it return to the starting point. On the other hand, the UAV energy utilization efficiency should be maximized so that the UAV can transfer more power to SNs instead of carrying its redundant remaining energy back to the starting point. Moreover, we deem that there exist some techniques to improve the performance of the $U A V _ { t s }$

- By equipping SNs with antennas capable of receiving signals and increasing the height of the antennas, the communication distance between UAVs and SNs can be extended.

- The high-gain antenna can increase the energy density in the communication direction and improve the signal-tonoise ratio, thus extending the communication range.

Locations of SNs can be as far away from interference sources as possible, and SNs can be equipped with wireless communication products with strong anti-interference capability.

## VI NUMERICAL RESULTS

In this section, we provide numerical results to evaluate the performance of UMC-enabled target search and DGC-enabled power transfer algorithms. The simulation experiments were carried out with these two algorithms uploaded to [44], which were coded in C++ 17, on a 64-bit Intel Core i5 CPU running at 2.30 GHz with 8 GB RAM.

## A Experiment Setup

Unless otherwise specified, the simulation parameters are set as follows. We consider a square region of $1 0 0 0 \times 1 0 0 0 ~ m ^ { 2 }$ with multiple rechargeable SNs distributed randomly, whose number is set from 500 to 1,500. The number of the $U A V _ { t s }$ and $U A V _ { w p t }$ is assumed to be one, respectively. The UAV is assumed to take off and return to the starting point (0,0). After the UAV departs from the starting point, it flies at a velocity of 10 m/s. The flight and hovering power of the UAV are set as 363 W and 280.5 W [45], respectively. In this work, we only investigate the trajectory design and optimization in the horizontal plane. For ease of illustration, the energy consumption of the UAV during deceleration and acceleration is neglected.

To evaluate the performance of different methods on target search and power transfer, we employ the following metrics.

- Number of SSNs is the number of SNs that the UAV can search within a certain period of time.

Standard deviation indicates the stability of different strategies. The smaller the difference in the number of SNs that the UAV can locate with different starting points, the better the stability of the algorithm is.

- The amount of energy harvested by SNs represents the amount of total energy received by SNs after the UAV performs power transfer.

The residual energy of the UAVis the remaining energy of the UAV returning to the starting point after completing the power transfer task.

- The conversion efficiency is the ratio of the amount of total energy harvested by SNs to the energy consumed by the

UAV to perform the power transfer task. More details can be seen in (21).

Energy utilization efficiency of the UAV is the ratio of the energy consumed by the UAV to perform power transfer to the UAVâs energy capacity. Further details on this metric are described in (23).

In addition, we also introduce several parameter constraints into our simulation experiments.

Task duration: This constraint is the duration for which the UAV performs the target search task.

- Number of SNs: To test the impact of each strategy on different indicators comprehensively, we set up different numbers of SNs to conduct various experiments.

Maximum cluster radius: To evaluate the energy harvested by SNs with different areas and numbers of SNs, we set various values of maximum cluster radius limitation.

Take-off position: To assess the stability performance of different strategies, we set different locations within a given area as the takeoff points of the UAV.

## B Approaches for Comparison

For the phase of target search, we compare the proposed RGS and MSS with the following strategy.

- BSS: the Blanket Search Strategy (BSS) divides the region into rows and conducts a traversal on these rows in turn. When the UAV performs BSS, we assume it moves at maximum speed all the time so that the BSS can be an upper bound to measure the performance of other strategies.

For the power transfer stage, we compare the fitness function in our proposed DGC algorithm with the following algorithms.

- GWC: the fitness function in Genetic Weighted Clustering (GWC) [35] is given by

$$
f = \alpha \cdot E _ { r e c } + \frac { \beta } { d _ { U A V } } ,\tag{26}
$$

where Î± and $\beta$ are two fixed values, which are set as 100 and 10, respectively; $d _ { U A V }$ is the flight distance of the UAV.

- MAVNS: the fitness function in Memetic Algorithm and Variable Neighborhood Search (MAVNS) [15] is

$$
f = \left[ 1 - \frac { L ( p ) - L ( p _ { m i n } ) } { L ( p _ { m a x } ) - L ( p _ { m i n } ) } \right] ^ { 2 } ,\tag{27}
$$

where $L ( p )$ is the trajectory length of pth population; $L ( p _ { m a x } )$ is the longest trajectory in all populations and $L ( p _ { m i n } )$ is the shortest one.

- MGA: the fitness function in Modified Genetic Algorithm (MGA) [46] is expressed as

$$
f = \alpha \cdot t a n h ( E _ { r e c } ) + \beta \cdot ( 1 - t a n h ( \eta _ { u } ) ) ,\tag{28}
$$

where Î± and $\beta$ are both set as 50; since the units are different between variables, the tanh function is used to remove their dimensions.

Furthermore, we contrast the proposed clustering strategy with the following two strategies, respectively.

TABLE II  
SIMULATION PARAMETERS FOR TARGET SEARCH
<table><tr><td>Definition</td><td>Variable</td><td>Value</td></tr><tr><td>Influence radius of each SSN</td><td> $d _ { 0 }$ </td><td>200 m</td></tr><tr><td>The height of the UAVts</td><td> $H _ { t s }$ </td><td>100 m</td></tr><tr><td>Repulsion scale factor</td><td> $\delta$ </td><td>10000</td></tr><tr><td>Attractiveness scale factor</td><td> $\xi$ </td><td>100</td></tr><tr><td>The detection radius of the UAV</td><td> $R _ { s }$ </td><td>30m</td></tr><tr><td>Velocity threshold when the att-</td><td> $V _ { t h }$ </td><td>5m/s</td></tr><tr><td>ractive force is in effect Force threshold for force balance</td><td> $F _ { t h }$ </td><td>1N</td></tr></table>

<!-- image-->  
Fig. 5. Performance of the number of SSNs with or without the attractive force when N=1000.

Static clustering strategy: the number of clusters is estimated based on the UAVâs energy capacity and approximate energy consumption for power transfer.

Simultaneous strategy: the target search task is performed concurrently with power transfer.

## C Comparisons of UAV-Enabled Target Search Algorithm

In this subsection, we consider a scenario where SNs are distributed in a region and no apriori information can be obtained in advance. The UAV is assumed to be equipped with components that can sense the presence of SNs and its twodimensional sensing range can be approximated as a circle. We create the UMC algorithm to search for these SNs. $\epsilon _ { a m p }$ and $\epsilon _ { e l }$ are set as 0.1 [nJ/bit/m2] and 50 [J/bits]. The performance of this algorithm is evaluated by varying the number of SNs and duration of the search task. Some parameters such as Repulsion and Attractiveness scale factor are set based on [37] and we have numerically adjusted them to fit our simulation experiments. The main simulation parameters are given in Table II.

First, SNs are uniformly distributed in the given region and we evaluate the effect of the attractive force on the number of SSNs. Fig. 5 demonstrates that without the aid of the attractive force, the number of SSNs stops rising after 8 minutes. This is because the UAV is stuck in a force balance and can no longer move when it is only subjected to repulsive forces. On the contrary, the attractive force can drag the UAV out of the force balance and enable it to continue the target search mission.

Second, the performance of various approaches for the target search is investigated. We adopt two strategies to find the optimal position to generate the attractive force, i.e., RGS and MSS (see

<!-- image-->  
Fig. 6. Performance of the number of SSNs over time under different strategies when N=1000.

<!-- image-->  
Fig. 7. Performance of the number of SSNs under different starting points with non-uniformly distributed SNs.

Section V for details). BSS is also adopted in the comparison experiment. We mainly study the influence of different strategies on search efficiency defined in (6). The number of SNs is set as 1,000 and they are distributed uniformly within the region. In the case of uniform distribution of SNs, the trajectory of the UAV hardly affects the search efficiency. Therefore, even if the UAV trajectories under various strategies are different, it does not affect the comparison of search efficiency.

As shown in Fig. 6, the search efficiency of MSS is close to that of other strategies before 16 minutes but decreases with time. Besides, the search efficiency of RGS is close to the BSS strategy before 26 minutes. As time goes on, the search efficiency of our proposed strategy starts to decrease and is even lower than BSS. This is because in our proposed strategy, after searching for a certain number of SNs, the UAV will fly over repeatedly to the already searched areas due to the influence of the attractive force.

However, when the distribution of SNs is not uniform, the BSS strategy cannot always maintain good performance. We design an experiment in the case of uneven distribution of SNs. The region is divided into 4 blocks of the same area, and 10%, 20%, 30%, 40% of the total SNs are allocated to them, respectively. The duration of the mission is set as 30 minutes. Fig. 7 shows that RGS and MSS both perform better than BSS. This is because the UAV take-off point is set in the area with sparse SNs and the UAV under BSS spends most of its time searching this area. On the contrary, RGS and MSS have much higher search efficiency because their searched areas are more evenly dispersed.

<!-- image-->  
Fig. 8. Performance of the number of SSNs under different take-off points with non-uniformly distributed SNs.

<!-- image-->  
Fig. 9. Performance of standard deviation under different experiment index with non-uniformly distributed SNs.

We then conduct a further experiment, in which 20 points are selected to set as the take-off positions of the UAV and each index on the X-axis represents a position. The number of SNs is set as 1,000. RGS in the UMC algorithm is selected as the representative to compare with the BSS because RGS is more suitable for this scenario. As depicted in Fig. 8, the performance of RGS is more stable than BSS. This is because the introduction of the attractive force and the S-distance in the UMC algorithm results in the attractive force always appearing in the largest unsearched area to drag the UAV. As a result, our proposed strategy can select a more reasonable target search route and the search efficiency is less affected by SNs distribution.

We further conduct another simulation experiment to measure the stability of different strategies. The number of SNs is set from 500 to 1,500. Standard deviation is supplied to represent the stability of different strategies, which is a quantity calculated to indicate the extent of deviation for a group. From Fig. 9, the search efficiency of our proposed RGS is more stable than BSS. The reasons for this phenomenon are explained in the interpretation of the experimental results in Fig. 8.

In conclusion, BSS is a good choice if the UAV conducts target search in the region where SNs are evenly distributed with unlimited time and UAVâs energy. However, in scenarios of uneven distribution of SNs and limited UAV energy, RGS is a more suitable choice due to its higher stability. Therefore, there will not be a situation where the search efficiency is greatly reduced due to the bad selection of the take-off point. In other words, RGS can reduce the impact of SNs distribution. Moreover, RGS facilitates the collection of rough information for the entire given area because the areas searched are dispersed in the given region rather than concentrated in a part of the region.

<!-- image-->  
Fig. 10. Trajectories of the UAV performing RGS with uniformly and nonuniformly distributed SNs.

In addition, the trajectories of the $U A V _ { t s }$ performing RGS with uniform and non-uniform distribution of SNs are shown in Fig. 10. It can be seen that the searched areas of $U A V _ { t s }$ is relatively evenly distributed both in the case of uniform and uneven distribution of SNs.

## D Comparisons of UAV-Enable WPT Algorithm

In this section, according to numerical results of the target search task, the fully charged UAV can search about 60% of SNs in 32 minutes, i.e., the positions and energy levels of 60% SNs in the given region can be known before conducting the power transfer mission. The starting and ending points of the UAV are both (0,0). For a comprehensive comparison of the discrepancies among different strategies, it is assumed that these SNs have not been supplied with energy for a long time due to disasters, resulting in over 90% of them having requests for power. The parameters are shown in Table III.

1) Convergence Analysis: We conduct an experiment to demonstrate the convergence of the DGC algorithm. As shown in Fig. 11, the curve has a tendency to converge after 1,000 episodes, and the convergence becomes increasing obvious in the subsequent iterations. After about 4,500 episodes, the convergence of the curve reaches the best.

2) Fitness Function Comparison: This subsection compares the proposed fitness function in the DGC algorithm to the existing ones in GWC, MAVNS and MGA. The evaluation of different strategies focuses on the total energy harvested by SNs, energy conversion efficiency, and the energy consumption of the UAV.

TABLE III  
SIMULATION PARAMETERS FOR POWER TRANSFER
<table><tr><td>Definition</td><td>Variable</td><td>Value</td></tr><tr><td>Energy capacity of each SN</td><td> $E _ { S N } ^ { m a x }$ </td><td>18.7J</td></tr><tr><td>The radius of the cluster</td><td> $R _ { c } ^ { - }$ </td><td>80 cm</td></tr><tr><td>The flying height of the  $U A V _ { w p t }$ </td><td> $H _ { f }$ </td><td>10 m</td></tr><tr><td>The hovering height of the  $U A V _ { w p t }$ </td><td> $H _ { w p t }$ </td><td>1m</td></tr><tr><td>Power transfer efficiency of  $\mathrm { U A V _ { - } }$ </td><td> $\gamma$ </td><td>0.5</td></tr><tr><td>to-CN UAV power consumption for WPT</td><td> $P _ { w p t }$ </td><td>6W</td></tr><tr><td>Piezoelectric driver efficiency</td><td> $\gamma _ { p i }$ </td><td>0.9</td></tr><tr><td>Acoustic to direct-current efficiency</td><td> $\gamma _ { d c }$ </td><td>0.98</td></tr><tr><td>Constant related to the circuit</td><td> $a$ </td><td>6400</td></tr><tr><td>Constant related to the circuit</td><td> $b$ </td><td>0.003</td></tr><tr><td>SN&#x27;s maximum harvested power</td><td> $P _ { M }$ </td><td>6W</td></tr><tr><td>Vertical speed of the UAV</td><td> $v _ { z }$ </td><td> $2 \mathrm { m } / \mathrm { s }$ </td></tr><tr><td>The size of the population</td><td> $p$ </td><td>50</td></tr><tr><td>The number of generations</td><td>I</td><td>50</td></tr></table>

<!-- image-->  
Fig. 11. Performance of convergence of the DGC algorithm.

First, Fig. 12(a) demonstrates that the increasing number of SNs leads to the improvement of the overall harvested energy across all strategies. Among four fitness functions, it can be seen that our proposed fitness function in the DGC algorithm enables SNs to harvest the largest amount of energy. Second, in Fig. 12(b), we compare the UAV energy conversion efficiency $\eta _ { c }$ defined by (21) with different fitness functions. It can be observed that $\eta _ { c }$ increases when more SNs are involved in the WPT task. The best performance is the fitness function in our proposed DGC algorithm and followed by the GWC. The performance of MGA is erratic but generally not as good as GWC. Moreover, when the number of SNs is less than 1,000, the UAV that performs K-means receives less energy than all others. However, MAVNS has the lowest performance when the number of SNs is more than 1,000. This is because in the work of proposing MAVNS, the goal is to minimize flight energy consumption, which is reflected in Fig. 12(c). It can be observed that the UAV under MAVNS has the most residual energy when returning to the starting point. However, in terms of energy conversion efficiency, K-means is always inferior to other strategies. The fitness function is well known as a metric for evaluating candidate populations and a good fitness function can effectively select eminent candidate populations.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(c)

Fig. 12. Optimized objectives with the different number of SNs in DGC, GWC, MAVNS, MGA and K-means: (a) the amount of energy harvested by SNs; (b) the UAV energy conversion efficiency; (c) the residual energy of the UAV.  
<!-- image-->

<!-- image-->

<!-- image-->

()äºº  
<!-- image-->

<!-- image-->  
Fig. 13. UAV trajectories with different fitness fuctions: (a) GWC; (b) MAVNS; (c) MGA (d) DGC; (e) K-means.

As shown in the two experiments, our proposed fitness function can maintain good performances because it can screen out more populations in line to maximize $\eta _ { c }$ . In general, experiments in this subsection prove that the fitness function in our proposed DGC algorithm has the benefit of attaining multi-objective optimization. Besides, the trajectories of the UAV corresponding to each fitness function are given in Fig. 13(a)â(e), with 1,200 SNs. Each dot in these figures represents the hover point of the UAV. In order to obtain higher energy efficiency, the UAV needs to descend to a certain height $H _ { w p t }$ at the hover point and then climb to a higher altitude $H _ { f }$ to avoid obstacles.

3) Clustering Strategy Comparison: This subsection studies the impact of the dynamic clustering strategy on the amount of energy harvested by SNs and the UAVâs energy utilization efficiency. It can be observed from Fig. 12(c) that the UAV has much residual energy after returning to the starting point. In particular, although the MAVNS strategy makes the UAV have the most remaining energy, the power harvested by SNs also lags far behind other strategies correspondingly, which leads to the low value of $\eta _ { c }$ shown in Fig. 12(b).

However, since the UAVâs energy capacity is limited, its energy should be utilized as much as possible to perform the power transfer mission rather than being brought back to the starting point. Therefore, we design a novel clustering strategy to improve UAV energy utilization and choose our proposed fitness functions to enforce this strategy for convenience. Fig. 14(a) depicts the comparison of the amount of energy harvested by SNs with and without implementing the dynamic clustering strategy. It illustrates that the dynamic clustering strategy can enable SNs to receive more power than the static strategy. This is because our strategy can gather more clusters with shorter radii, thus leading to the reduction of the transmission loss between CN and ENs. Besides, the increase of clusters can enable more CNs to harvest energy from the UAV. When the number of SNs becomes larger, the gap between the two strategies tends to be obvious, which can demonstrate that the dynamic clustering strategy is suitable for WSNs with many SNs.

To measure the UAV energy utilization efficiency in the power transfer phase, we define a variable $\eta _ { u }$ calculated by (23). From Fig. 14(b), it can be observed that under the static clustering strategy, the energy consumed by the UAV to charge SNs with different densities has little difference because the number of clusters assigned by the static strategy is fixed. In contrast, as the number of SNs increases, $\eta _ { u }$ also grows when conducting our proposed dynamic clustering strategy because the UAV can take advantage of more energy to perform the WPT task, thus leading to an increase in $\eta _ { u }$ and the total harvested energy of SNs. It can be concluded that with the same amount of UAVâs energy and the same number of SNs in the given region, our proposed strategy increases the amount of energy harvested by SNs as well as the energy utilization of the UAV compared with [15]. Specifically, numerical results show that after utilizing our proposed fitness function and dynamic clustering strategy, the amount of energy harvested by SNs is about 12% to 32% higher than [15] and the UAV energy utilization is improved by about 11% to 36%. This is because the UAV can transfer power to more CNs and the power transfer efficiency between CN and EN is higher when executing our proposed strategy, thus increasing the amount of energy received by SNs, which can demonstrate its superiority. However, our proposed DGC algorithm is $N _ { t }$ times the time complexity of the algorithm of [15], where $N _ { t }$ is the number of iterations needed. The trajectories of the static and dynamic clustering strategies are given in Fig. 15.

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 14. Performance of the dynamic and static clustering strategy under different number of SNs: (a) the amount of harvested energy by SNs; (b) energy utilization efficiency of the UAV.  
<!-- image-->  
Fig. 15. UAV trajectories of the static and dynamic clustering strategy.

## E Comparison of Two-Stage and Simultaneous Strategy

We adopt the two-stage strategy of target search followed by power transfer rather than the simultaneous strategy in which both tasks are conducted at the same time because efficient trajectory planning before charging SNs can allow the UAV to save energy and SNs to receive more power. Since the sensing range $R _ { s }$ of the $U A V _ { t s }$ during target search is larger than the radius of clusters $R _ { c }$ during power transmission, the $U A V _ { w p t }$ can perform the DGC algorithm on the local area detected by $U A V _ { t s }$ in a little period. The time for $U A V _ { w p t }$ to execute the DGC algorithm is ignored. We assume that $U A V _ { w p t }$ is always within the communication range of $U A V _ { t s }$ when executing the simultaneous policy so that both of them can transmit the information of SNs at any time. Besides, the $U A V _ { t s }$ is assumed to perform the BSS to avoid its repeated overflights of already searched areas. The area of the region is set to $1 \bar { 0 } 0 0 \times 1 0 0 0 \ : m ^ { 2 }$ As shown in Fig. 16(a) and (b), the amount of energy harvested by SNs and energy conversion efficiency under the two-stage strategy are both higher than those under the simultaneous strategy. When the number of SNs becomes larger, the gap between the two increases.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 16. Performance of the two-stage and simultaneous strategy under different number of SNs: (a) the amount of harvested energy by SNs; (b) energy conversion efficiency.

## VII CONCLUSION

In this paper, we considered a new scenario for the UAVenable wireless power transfer system, in which the UAV searches for SNs at unknown locations and then delivers power to them. We formulated a novel problem that simultaneously optimizes the search efficiency, energy conversion efficiency, and energy utilization efficiency of the UAV. To tackle this issue, we proposed a two-stage strategy that combines a UMC algorithm to collect the positions and energy levels of SNs with a DGC algorithm to transmit power to SNs. Specifically, we adopted the UMC algorithm to obtain the information of SNs without any apriori known target location information. After the target search task was accomplished, the DGC algorithm was utilized to dynamically form SNs into clusters and provide an optimized path for power transmission. Numerical results showed that the UMC algorithm could find more SNs than the blanket search strategy, and its performance was more stable when the nodes were not evenly distributed. In the WPT phase, simulation results also demonstrated that the UAV energy conversion efficiency could be enhanced by the new fitness function, while the dynamic clustering strategy could enable SNs to harvest more power and improve the energy utilization efficiency of the UAV.

There are some unaddressed problems in this paper deserving further investigation. For instance, this paper only focused on the case of a single UAV. However, due to the limited energy capacity of the UAV, there is a restriction on what a UAV can complete. Therefore, multi-UAV-enabled target search and power transfer in an unknown environment is a more interesting research problem. Moreover, this work only focused on horizontal trajectory design, whereas multi-UAV cooperative three-dimensional trajectories design for power transfer is a promising issue.

## REFERENCES

[1] S. Feng, P. Setoodeh, and S. Haykin, âSmart home: Cognitive interactive people-centric Internet of Things,â IEEE Commun. Mag., vol. 55, no. 2, pp. 34â39, Feb. 2017.

[2] Y. Mehmood, F. Ahmad, I. Yaqoob, A. Adnane, M. Imran, and S. Guizani, âInternet-of-Things-based smart cities: Recent advances and challenges,â IEEE Commun. Mag., vol. 55, no. 9, pp. 16â24, Sep. 2017.

[3] W. Xu, W. Liang, X. Jia, H. Kan, Y. Xu, and X. Zhang, âMinimizing the maximum charging delay of multiple mobile chargers under the multi-node energy charging scheme,â IEEE Trans. Mobile Comput., vol. 20, no. 5, pp. 1846â1861, May 2021.

[4] W. Liang, W. Xu, X. Ren, X. Jia, and X. Lin, âMaintaining large-scale rechargeable sensor networks perpetually via multiple mobile charging vehicles,â ACM Trans. Sensor Netw., vol. 12, no. 14, pp. 1â26, May 2016.

[5] S. Bi and R. Zhang, âPlacement optimization of energy and information access points in wireless powered communication networks,â IEEE Trans. Wireless Commun., vol. 15, no. 3, pp. 2351â2364, Mar. 2016.

[6] Z. Dang, Y. Cao, and J. A. A. Qahouq, âReconfigurable magnetic resonance-coupled wireless power transfer system,â IEEE Trans. Power Electron., vol. 30, no. 11, pp. 6057â6069, Nov. 2015.

[7] 2022. [Online]. Available: https://www.Marketsandmarkets.com/Market-Reports/wireless-charging-market-640.html

[8] Z. Wang, L. Duan, and R. Zhang, âAdaptively directional wireless power transfer for large-scale sensor networks,â IEEE J. Sel. Areas Commun., vol. 34, no. 5, pp. 1785â1800, May 2016.

[9] C. Sha, Y. Sun, and R. Malekian, âResearch on cost-balanced mobile energy replenishment strategy for wireless rechargeable sensor networks,â IEEE Trans. Veh. Technol., vol. 69, no. 3, pp. 3135â3150, Mar. 2020.

[10] L. Zhao, K. Yang, Z. Tan, X. Li, S. Sharma, and Z. Liu, âA novel cost optimization strategy for SDN-enabled UAV-assisted vehicular computation offloading,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 6, pp. 3664â3674, Jun. 2021.

[11] J. Shi, L. Zhao, X. Wang, W. Zhao, A. Hawbani, and M. Huang, âA novel deep Q-Learning-based air-assisted vehicular caching scheme for safe autonomous driving,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 7, pp. 4348â4358, Jul. 2021.

[12] J. Shi, L. Zhao, X. Wang, M. Guizani, H. Gaanin, and N. Lin, âFlying social networks: Architecture, challenges and open issues,â IEEE Netw., vol. 35, no. 5, pp. 242â248, Sep./Oct. 2021.

[13] H. Yan, Y. Chen, and S.-H. Yang, âUAV-enabled wireless power transfer with base station charging and UAV power consumption,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 12883â12896, Nov. 2020.

[14] L. Xie, X. Cao, J. Xu, and R. Zhang, âUAV-enabled wireless power transfer: A tutorial overview,â IEEE Trans. Green Commun. Netw., vol. 5, no. 4, pp. 2042â2064, Dec. 2021.

[15] A. Y. Pandiyan, D. E. Boyle, M. E. Kiziroglou, S. W. Wright, and E. M. Yeatman, âOptimal dynamic recharge scheduling for two-stage wireless power transfer,â IEEE Trans. Ind. Informat., vol. 17, no. 8, pp. 5719â5729, Aug. 2021.

[16] A. Symington, S. Waharte, S. Julier, and N. Trigoni, âProbabilistic target detection by camera-equipped UAVs,â in Proc. IEEE Int. Conf. Robot. Autom., 2010, pp. 4076â4081.

[17] S. Xu, K. Do ËganÃ§ay, and H. Hmam, âDistributed pseudolinear estimation and UAV path optimization for 3D AOA target tracking,â Signal Process., vol. 133, pp. 64â78, Apr. 2017.

[18] P. Yao, Z. Xie, and P. Ren, âOptimal UAV route planning for coverage search of stationary target in river,â IEEE Trans. Control Syst. Technol., vol. 27, no. 2, pp. 822â829, Mar. 2019.

[19] Z. Kashino, G. Nejat, and B. Benhabib, âMulti-UAV based autonomous wilderness search and rescue using target iso-probability curves,â in Proc. IEEE Int. Conf. Unmanned Aircr. Syst., 2019, pp. 636â643.

[20] Y.-C. Du, M.-X. Zhang, H.-F. Ling, and Y.-J. Zheng, âEvolutionary planning of multi-UAV search for missing tourists,â IEEE Access, vol. 7, pp. 73480â73492, Jun. 2019.

[21] D. Luo, J. Shao, Y. Xu, Y. You, and H. Duan, âCoevolution pigeon-inspired optimization with cooperation-competition mechanism for multi-UAV cooperative region search,â Appl. Sci., vol. 9, no. 5, Dec. 2019, Art. no. 827.

[22] P. Yao and X. Wei, âMulti-UAV information fusion and cooperative trajectory optimization in target search,â IEEE Syst. J., vol. 16, no. 3, pp. 4325â4333, Sep. 2022.

[23] C. Wu et al., âUAV autonomous target search based on deep reinforcement learning in complex disaster scene,â IEEE Access, vol. 7, pp. 117227â117245, Aug. 2019.

[24] X. Cao, H. Sun, and L. Guo, âPotential field hierarchical reinforcement learning approach for target search by multi-AUV in 3-D underwater environments,â Int. J. Control, vol. 93, no. 7, pp. 1677â1683, Aug. 2019.

[25] X. Cao, C. Sun, and M. Yan, âTarget search control of AUV in underwater environment with deep reinforcement learning,â IEEE Access, vol. 7, pp. 96549â96559, Jul. 2019.

[26] D. Brown and L. Sun, âDynamic exhaustive mobile target search using unmanned aerial vehicles,â IEEE Trans. Aerosp. Electron. Syst., vol. 55, no. 6, pp. 3413â3423, Dec. 2019.

[27] Y. Hu, X. Yuan, J. Xu, and A. Schmeink, âOptimal 1D trajectory design for UAV-enabled multiuser wireless power transfer,â IEEE Trans. Commun., vol. 67, no. 8, pp. 5674â5688, Aug. 2019.

[28] J. Xu, Y. Zeng, and R. Zhang, âUAV-enabled wireless power transfer: Trajectory design and energy optimization,â IEEE Trans. Wireless Commun., vol. 17, no. 8, pp. 5092â5106, Aug. 2018.

[29] T. Yang, Y. Hu, X. Yuan, and R. Mathar, âGenetic algorithm based UAV trajectory design in wireless power transfer systems,â in Proc. IEEE Wireless Commun. Netw. Conf., 2019, pp. 1â6.

[30] J. Baek, S. I. Han, and Y. Han, âOptimal UAV route in wireless charging sensor networks,â IEEE Internet Things J., vol. 7, no. 2, pp. 1327â1335, Feb. 2020.

[31] X. Yuan, T. Yang, Y. Hu, J. Xu, and A. Schmeink, âTrajectory design for UAV-enabled multiuser wireless power transfer with nonlinear energy harvesting,â IEEE Trans. Wireless Commun., vol. 20, no. 2, pp. 1105â1121, Feb. 2021.

[32] W. Feng et al., âJoint 3D trajectory design and time allocation for UAVenabled wireless power transfer networks,â IEEE Trans. Veh. Technol., vol. 69, no. 9, pp. 9265â9278, Sep. 2020.

[33] X. Mo, Y. Huang, and J. Xu, âRadio-map-based robust positioning optimization for UAV-enabled wireless power transfer,â IEEE Wireless Commun. Lett., vol. 9, no. 2, pp. 179â183, Feb. 2020.

[34] H.-T. Ye, X. Kang, J. Joung, and Y.-C. Liang, âOptimization for full-duplex rotary-wing UAV-enabled wireless-powered IoT networks,â IEEE Trans. Wireless Commun., vol. 19, no. 7, pp. 5057â5072, Jul. 2020.

[35] P. Wu, F. Xiao, H. Huang, and R. Wang, âLoad balance and trajectory design in multi-UAV aided large-scale wireless rechargeable networks,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13756â13767, Nov. 2020.

[36] L. Sun, L. Wan, K. Liu, and X. Wang, âCooperative-evolution-based WPT resource allocation for large-scale cognitive industrial IoT,â IEEE Trans. Ind. Informat., vol. 16, no. 8, pp. 5401â5411, Aug. 2020.

[37] H. Zhao, H. Wang, W. Wu, and J. Wei, âDeployment algorithms for UAV airborne networks toward on-demand coverage,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 2015â2031, Sep. 2018.

[38] M. Jiang, Y. Li, Q. Zhang, and J. Qin, âJoint position and time allocation optimization of UAV-enabled time allocation optimization networks,â IEEE Trans. Commun., vol. 67, no. 5, pp. 3806â3816, May 2019.

[39] L. Xie, J. Xu, and R. Zhang, âThroughput maximization for UAV-enabled wireless powered communication networks,â IEEE Internet Things J., vol. 6, no. 2, pp. 1690â1703, Apr. 2019.

[40] E. Boshkovska, D. W. K. Ng, N. Zlatanov, and R. Schober, âPractical nonlinear energy harvesting model and resource allocation for swipt systems,â IEEE Commun. Lett., vol. 19, no. 12, pp. 2082â2085, Dec. 2015.

[41] M. Kiziroglou, D. Boyle, S. Wright, and E. Yeatman, âAcoustic power delivery to pipeline monitoring wireless sensors,â Ultrasonics, vol. 77, pp. 54â60, May 2017.

[42] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[43] Y. Yu, J. Tang, J. Huang, X. Zhang, D. K. C. So, and K.-K. Wong, âMultiobjective optimization for UAV-assisted wireless powered IoT networks based on extended DDPG algorithm,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6361â6374, Sep. 2021.

[44] 2022. [Online]. Available: https://github.com/NetworkCommunication/ UMC-DGC---CPY

[45] 2015. [Online]. Available: https://www.dji.com/uk/matrice100/info

[46] Q. Qian, A. Y. Pandiyan, and D. E. Boyle, âOptimal recharge scheduler for Drone-to-Sensor wireless power transfer,â IEEE Access, vol. 9, pp. 59301â 59312, Apr. 2021.

<!-- image-->

<!-- image-->  
Junling Shi received the PhD degree in computer application technologies from Northeastern University, Shenyang, China, in 2019. She is currently working with the School of Computer Science, Shenyang Aerospace University. Her research interests include UAV networks, UAV path planning, and vehicle ad hoc networks, etc. She is the local president of SmartCNS-2019, the publication chair of Trustcom-2021, and the special issue editor of Wileyâs Internet Technology Letters.

<!-- image-->

Peiyu Cong received the BS degree from Liaoning University, Shenyang, China, in 2020. He is currently working toward the MS degree with Shenyang Aerospace University, Shenyang. His research interests include wireless power transfer, UAV trajectory planning, and wireless rechargeable sensor networks.

<!-- image-->

Xingwei Wang received the BSc, MSc, and PhD degrees in computer science from Northeastern University, Shenyang, China, in 1989, 1992, and 1998, respectively. He is currently a professor of Northeastern University. His current research interests include cloud computing and future Internet. He has published more than 100 journal articles, books, and refereed conference papers.

Liang Zhao (Member, IEEE) received the PhD degree from the School of Computing, Edinburgh Napier University, in 2011. He is a professor with Shenyang Aerospace University, China. Before joining Shenyang Aerospace University, he worked as associate senior researcher in Hitachi (China) Research and Development Corporation from 2012 to 2014. He is also a JSPS invitational fellow (2023). He was listed as Top 2% of scientists in the world by Standford University (2022). His research interests include ITS, VANET, WMN, and SDN. He has published more

than 150 articles. He served as the chair of several international conferences and workshops, including 2022 IEEE BigDataSE (Steering co-chair), 2021 IEEE TrustCom (Program co-chair), 2019 IEEE IUCC (Program co-chair), and 2018â2022 NGDN workshop (founder). He is associate editor of Frontiers in Communications and Networking and Journal of Circuits Systems and Computers. He is/has been a guest editor of IEEE Transactions on Network Science and Engineering, Springer Journal of Computing, etc. He was the recipient of the Best/Outstanding Paper Awards with 2015 IEEE IUCC, 2020 IEEE ISPA, 2022 IEEE EUC and 2013 ACM MoMM.

<!-- image-->

Shaohua Wan (Senior Member, IEEE) received the PhD degree from the School of Computer, Wuhan University, in 2010. He is currently a professor with the Shenzhen Institute for Advanced Study, University of Electronic Science and Technology of China. From 2016 to 2017, he was a visiting professor with the Department of Electrical and Computer Engineering, Technical University of Munich, Germany. His main research interests include deep learning for Internet of Things. He is an author of more than 150 peer-reviewed research papers and books, including more than 40 IEEE/ACM Transactions papers such as IEEE Transactions on Industrial Informatics, IEEE Transactions on Intelligent Transportation Systems, ACM Transactions on Internet Technology, IEEE Transactions on Network Science and Engineering, IEEE Transactions on Multimedia, IEEE Transactions on Computational Social Systems, ACM Transactions on Multimedia Computing, Communications, and Applications, IEEE Transactions on Emerging Topics in Computational Intelligence, Pattern Recognition, etc., and many top conference papers in the fields of edge intelligence.

<!-- image-->

Mohsen Guizani (Fellow, IEEE) received the BS (with distinction), MS and PhD degrees in electrical and computer engineering from Syracuse University, Syracuse, New York, in 1985, 1987 and 1990, respectively. He is currently a professor of machine learning and the associate provost with the Mohamed Bin Zayed University of Artificial Intelligence (MBZUAI), Abu Dhabi, UAE. Previously, he worked in different institutions in the USA. His research interests include applied machine learning and artificial intelligence, Internet of Things (IoT), intelligent autonomous systems, smart city, and cybersecurity. He was listed as a Clarivate Analytics Highly Cited researcher in computer science, in 2019, 2020 and 2021. He has won several research awards including the â2015 IEEE Communications Society Best Survey Paper Awardâ, the Best ComSoc Journal Paper Award, in 2021 as well five Best Paper Awards from ICC and Globecom Conferences. He is the author of ten books and more than 800 publications. He is also the recipient of the 2017 IEEE Communications Society Wireless Technical Committee (WTC) Recognition Award, the 2018 AdHoc Technical Committee Recognition Award, and the 2019 IEEE Communications and Information Security Technical Recognition (CISTC) Award. He served as the editor-in-chief of IEEE Network and is currently serving on the editorial boards of many IEEE Transactions and Magazines. He was the chair of the IEEE Communications Society Wireless Technical Committee and the chair of the TAOS Technical Committee. He served as the IEEE Computer Society Distinguished speaker and is currently the IEEE ComSoc Distinguished lecturer.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_13_img_1.jpeg|page_13_img_1]]
2. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_13_img_2.jpeg|page_13_img_2]]
3. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_13_img_3.jpeg|page_13_img_3]]
4. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_14_img_1.png|page_14_img_1]]
5. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_15_img_1.jpeg|page_15_img_1]]
6. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_15_img_2.jpeg|page_15_img_2]]
7. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_16_img_1.jpeg|page_16_img_1]]
8. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_16_img_2.jpeg|page_16_img_2]]
9. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_16_img_3.png|page_16_img_3]]
10. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_18_img_1.jpeg|page_18_img_1]]
11. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_18_img_2.jpeg|page_18_img_2]]
12. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_18_img_3.jpeg|page_18_img_3]]
13. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_18_img_4.jpeg|page_18_img_4]]
14. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_18_img_5.jpeg|page_18_img_5]]
15. [[../extracted_images/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe/page_18_img_6.jpeg|page_18_img_6]]

---

