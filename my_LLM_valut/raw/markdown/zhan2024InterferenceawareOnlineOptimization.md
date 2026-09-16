# Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Constraints

Cheng Zhan , Member, IEEE, Han Hu , Member, IEEE, Zhi Liu , Senior Member, IEEE, Jing Wang , Member, IEEE, and Rongfei Fan , Member, IEEE

AbstractâThe incorporation of Unmanned Aerial Vehicles (UAVs) into cellular networks opens up new possibilities to enhance their ubiquitous operations and establish superior performance owing to the high probability of line-of-sight (LoS) for air-toground channels. However, this also results in the UAV inducing more significant uplink interference to non-associated Base Stations (BSs). This paper explores the online design policy in cellular-connected multiple UAV communications in the absence of channel conditions, focusing on wireless resource allocation and dynamic three-dimensional (3-D) path planning. Our objective is to maximize the minimum uplink throughput for all UAVs while considering the energy constraints of the UAVs. First, we implement an online design utilizing the achievable rate based on the estimated instantaneous channel state information (CSI) for the current time slot, and the expected data rate for future time slots based on channel distribution information (CDI). Our solution employs the exact penalty method along with alternating optimization and successive convex optimization methods. Second, we formulate an online design by merely using the achievable rate based on the estimated instantaneous CSI for the current time slot. We introduce an energy-triggered penalty term to regulate the energy consumption of the UAVs, resulting in a low-complexity solution even if the CDI is unavailable before the flight. Lastly, we conduct extensive simulations to corroborate our findings and provide comprehensive comparisons with other baseline schemes to underline the effectiveness of the proposed designs.

Index TermsâEnergy budget, multiple cellular-connected UAVs, online design, unknown channel conditions, uplink throughput maximization.

## I. INTRODUCTION

U NMANNED Aerial Vehicles (UAVs) have increasinglybecome vital tools in diverse fields such as disaster relief, surveillance and monitoring, precision agriculture, and remote sensing. These innovative applications unlock their potential, extending their utility into military, public security, and civilian domains [1], [2], [3]. Traditional UAVs usually communicate with ground-based pilots through basic point-to-point (P2P) links using unlicensed spectrum, such as ISM 2.4 GHz. However, this approach has led to subpar air-to-ground (A2G) transmission performance, characterized by low data throughput, constrained communication range, and susceptibility to interference [4]. The restricted coverage and insufficient bandwidth of these P2P links present significant challenges when operating UAVs over large airspace. In pursuit of large-scale UAV deployment and enhanced A2G communication, an effective strategy is to incorporate UAVs into globally established cellular networks. In this framework, UAVs act as aerial users, harnessing the power of robust terrestrial base stations (BSs). This increasingly recognized approach is often referred to as the cellular-connected UAV solution [5], [6], [7], [8].

Various strategies have been explored to enhance the functionality of cellular-connected UAVs. The work in [9] leveraged a cellular-connected UAV to create a mobile bistatic synthetic aperture radar in tandem with its BS, offering comprehensive sensing capabilities across vast areas. The work in [10] proposed an integrated scheduling method for sensing, communication, and control to facilitate backhaul transmission from the UAV to the BS, which is enabled by mmWave/THz communication in cellular-connected UAV networks. The works in [11] and [12] explored a case where an aerial user equipment transmits in uplink to a BS using aerial-terrestrial non-orthogonal multiple access (NOMA). The work in [13] addressed the challenge of ubiquitous communication coverage by introducing a coverageaware navigation approach to navigate around coverage gaps in cellular BSs while still accomplishing their missions. In [14], the focus was on reducing the energy consumption of cellularconnected UAVs by jointly designing the mission completion time, UAV trajectory, and communication BS associations, ensuring a consistent communication connectivity during the UAV flight. Nevertheless, these works primarily focus on optimization strategies involving single cellular-connected UAV, and a

Digital Object Identifier 10.1109/TMC.2024.3438759 consideration for multiple UAVs is yet to be thoroughly addressed.

The Federal Aviation Administration (FAA) has projected that the number of commercial UAV fleets may reach a staggering 1.6 million by 2024 [15]. Furthermore, it is projected that numerous UAVs may be operational within each square mile near warehouses or operational centers, suggesting that each cell in hotspot areas could accommodate multiple active cellularconnected UAVs [16]. The work in [17] proposed a unified framework for beamforming, user association, and UAV-height control in multi-UAV communications connected through cellular networks, aiming to maximize the minimum achievable rate for UAVs. In [18], multiple cellular-connected UAVs employed machine learning algorithms to facilitate advanced applications like object detection and video tracking. A two-phase transmission protocol exploiting cellular and device-to-device (D2D) communication for UAV swarms was proposed in [19]. The work in [20] delved into multi-UAV mobile edge computing (MEC) networks connected through cellular networks, with an objective to minimize the average weighted sum energy consumption. The performance of downlink NOMA for cellular-connected UAVs was analyzed using stochastic geometry in [21]. However, these studies did not consider co-channel interference for UAVs. It is essential to acknowledge that while nearly line-of-sight (LoS) A2G channels for cellular-connected UAVs can receive high power, they can simultaneously induce significant interference. This issue becomes increasingly critical with the escalating number of UAVs connected to cellular networks, which could substantially impact the system performance. Therefore, developing efficient interference mitigation techniques for multiple cellular-connected UAV scenarios remains a key challenge [22], [23], [24], [25].

UAVs are intrinsically mobile, resulting in trajectories that are ripe for optimization. The ability for 3D movement gives UAVs an additional level of flexibility for enhancing communication performance through communication-aware trajectory design [26]. For example, UAV trajectories can be strategically planned according to the known locations of BSs along the flight path, which ensures consistent communication coverage with associated BSs, while minimizing interference with nonassociated BSs. Although numerous studies have tackled the issue of UAV trajectory optimization (e.g., [27], [28], [29], [30], [31]), they often fall short in several respects. First, they adopt deterministic LoS dominant or probabilistic LoS channel models suitable for rural areas, devoid of high and dense obstacles. Such assumptions fail to address unique conditions related to cellular-connected UAVs in urban landscapes, especially the issue of co-channel interference. In reality, BSs usually orient their antennas downwards to better serve terrestrial users. This strategy substantially decreases antenna gain for aerial users [32], [33]. Particularly, UAVs that typically operate at higher altitudes than BSs are mostly served by the side-lobes of the BS antennas, which have weak antenna gains closely tied to the downtilt angle and UAV locations. Moreover, these studies often limit themselves to two-dimensional (2D) UAV trajectory designs with a fixed flight altitude, obtained in an offline manner in advance of the flight based on the missionâs requirements. However, these offline designs, grounded in statistical channel analysis, can only provide an average assurance of UAV communication performance. They fail to guarantee reliable performance at each location along the flight, as the offline policy cannot accommodate the real-time changes in UAV-ground channel states. This oversight is significant, given the stark differences between the strengths of LoS and non-line of sight (NLoS) states. The work in [34] introduced a hybrid offline-online method to jointly optimize 3D UAV trajectory and communication scheduling for data harvesting. Another work [35] employed a Deep Reinforcement Learning (DRL) strategy to study online altitude control and scheduling policy for minimizing the Age of Information (AoI) in UAV-assisted Internet of Things (IoT) networks. However, the above studies overlooked the co-channel interference and energy budget considerations for cellular-connected UAVs. The work in [36] explored the joint optimization of resource block allocation and beamforming design for cellular-connected UAVs, but neglected trajectory planning. The online design for resource allocation and 3D UAV trajectory for cellular-connected multiple UAV communication with co-channel interference and energy budget is challenging, which, to our best knowledge, has not been studied in prior work.

Inspired by the limitations in existing designs, this paper mainly investigate the interference-aware online optimization techniques in a scenario in which multiple cellular-connected UAVs travel from starting to final locations, uploading data to ground BSs within a specified time. These UAVs are assumed to share the same frequency band, and therefore the issue of co-channel interference should be addressed. Prior to flight, the UAVs only possess knowledge of the BS locations but they can measure real-time A2G channel state information (CSI) throughout their flight. To ensure fairness across the network, the main aim of this paper is to maximize the minimum uplink transmission throughput of these UAVs. This goal is accomplished by a joint design of 3D UAV trajectories, transmission scheduling, and power allocation, all while adhering to energy budget constraints. The main contributions of this paper are summarized as follows:

First, we develop an online design framework aimed at uplink throughput maximization in multiple cellularconnected UAV communications. This framework intelligently adapts to real-time A2G CSI to optimize the uplink throughput, considering the critical issue of co-channel interference and UAV energy constraints. The A2G channel model used is more practical than its statistical counterpart, which only reflects the ergodic pathloss gain across multiple building distribution realizations.

Second, we propose an online design scheme employing statistical channel distribution information (CDI). This scheme uses the achievable rate based on instantaneous CSI for the current time slot, and the expected data rate for future time slots, based on CDI. An efficient algorithm is developed for this scheme, leveraging the exact penalty method for simplification, alternating optimization for systematic problem decomposition, and successive convex optimization for iterative refinement towards the local optimum.

Third, we propose an online design scheme which operates without the CDI. Such design focuses on maximizing the immediate uplink throughput while incorporating an energy-triggered penalty term for sustainable energy management across the mission. This ensures UAVs efficiently navigate dynamic environments, maintaining energy adequacy for their destinations through a streamlined, lowcomplexity solution that optimizes trajectory and resource allocation adaptively, despite lacking advance CDI knowledge.

The structure of this paper is as follows: Section II introduces the system model, while Section III outlines the problem statement and the methodology of the proposed online designs. Section IV discusses the online design scheme that includes CDI, and Section V describes the online design scheme without CDI. Our simulations and the ensuing result analysis are detailed in Section VI, while conclusions are presented in Section VII.

Notations: we use lower-case letters to represent scalars, while bold-face lower-case and upper-case letters represent vectors and matrices, respectively. The term $\mathbb { R } ^ { M \times 1 }$ refers to the space of an M-dimensional real-valued vector. The notations $\lVert \mathbf a \rVert$ and T stand for the euclidean norm and transpose of a vector , respectively. |K| represents the cardinality of set K, while aP Â· denotes probability. The expectation operation is denoted ( )by E Â· .

## II. SYSTEM MODEL

## A. Network Model

In this paper, we focus on an urban multi-cell cellular network with K base stations (BSs), represented as $\kappa =$ $\{ s _ { 1 } , s _ { 2 } , \ldots , s _ { K } \}$ , and M rotary-wing UAVs, denoted by $\mathcal { M } =$ $\left\{ u _ { 1 } , u _ { 2 } , \dotsc , u _ { M } \right\}$ =. The distribution of buildings, encompassing 1 2the 2D locations of high-rise structures on the ground and their respective heights, is constructed based on one realization of the statistical model recommended by the ITU [13], [37]. Similar to [6], we operate under the assumption of a densely populated BS environment, which guarantees seamless communication between the UAVs and at least one BS during their flight. These UAVs, equipped with either sensors or cameras, capture mission-centric data, which is then uploaded to the cellular infrastructure for subsequent processing. For any given $\mathrm { U A V } , u _ { m }$ its starting and ending geographical coordinates are denoted by $\mathbf { u } _ { m , I } \in \mathbb { R } ^ { 3 \times 1 }$ and $\mathbf { u } _ { m , F } \in \mathbb { R } ^ { 3 \times 1 }$ , respectively. In practice, $\mathbf { u } _ { m , I }$ u u uoften signifies a site targeted for inspection or data accumulation, while $\mathbf { u } _ { m , F }$ pertains to a UAVâs charging hub. Powered by their ufinite on-board battery capacities, UAVs traverse their specified routes, uploading data to the BSs within the time horizon T . To simplify our model, we segment the time duration T into N equal slots, with each slot spanning $\begin{array} { r } { \delta = \frac { T } { N } } \end{array}$ . We highlight that Î´ =is designed to be minimal, enabling the assumption that UAVs remain stationary in each time slot, independent of their actual motion. The main notations used in this paper are summarized in Table I.

TABLE I  
SUMMARY OF MAIN NOTATIONS AND DEFINITIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>K</td><td rowspan=1 colspan=1>ThenumberofBSs</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>The number of UAVs</td></tr><tr><td rowspan=1 colspan=1> $s _ { k }$ </td><td rowspan=1 colspan=1>The k-th BS</td></tr><tr><td rowspan=1 colspan=1> $u _ { m }$ </td><td rowspan=1 colspan=1>The m-th UAV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { T } }$ </td><td rowspan=1 colspan=1>The total time horizon (s)</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N } }$ </td><td rowspan=1 colspan=1>The total number of time slots</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { g } _ { k }$ </td><td rowspan=1 colspan=1>The 3D location of BS $s _ { k }$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathbf { u } _ { m } [ n ] } }$ </td><td rowspan=1 colspan=1>The 3D location of the UAV $\overline { { u _ { m } } }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { v } _ { m } ^ { x y } [ n ]$ </td><td rowspan=1 colspan=1>The horizontal velocity of the $\operatorname { U A V } u _ { m }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $v _ { m } ^ { z } [ n ]$ </td><td rowspan=1 colspan=1>Thevertical velocity of the $\overline { { \mathrm { U A V } ~ u _ { m } } }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $V _ { \mathrm { m a x } } ^ { x y }$ </td><td rowspan=1 colspan=1>The maximum UAV speed inhorizontal direction (m/s)</td></tr><tr><td rowspan=1 colspan=1> $V _ { \mathrm { m a x } } ^ { z }$ </td><td rowspan=1 colspan=1>The maximum UAV speed invertical direction (m/s)</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { u } _ { m , I } , \mathbf { u } _ { m , F }$ </td><td rowspan=1 colspan=1>The initial and final three-dimensional positionsof the UAV $u _ { m }$ </td></tr><tr><td rowspan=1 colspan=1> $H _ { \operatorname* { m i n } } , H _ { \operatorname* { m a x } }$ </td><td rowspan=1 colspan=1>Theminimumandmaximumallowablealtitudeforall the UAVs</td></tr><tr><td rowspan=1 colspan=1> $x _ { m , k } [ n ]$ </td><td rowspan=1 colspan=1>Transmission schedulingandassociation indicator for BSï¼204å· $s _ { m }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $R _ { m , k } [ n ]$ </td><td rowspan=1 colspan=1>Theachievable rate from theUAVum toBS sk at time slot n</td></tr><tr><td rowspan=1 colspan=1> $p _ { m } [ n ]$ </td><td rowspan=1 colspan=1>The transmission power of the $\overline { { \mathrm { U A V } \ u _ { m } } }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $h _ { m , k } [ n ]$ </td><td rowspan=1 colspan=1>Thebaseband equivalentchannel coefficientbetween UAV $u _ { m }$ and BS $s _ { k }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\beta _ { m , k } [ n ]$ </td><td rowspan=1 colspan=1>The large-scale channel power gain betweenUAV $u _ { m }$ and ${ \tt B S } _ { { s } _ { k } }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $G _ { m , k } [ n ]$ </td><td rowspan=1 colspan=1>The antenna gain between the UAVand BS $s _ { m }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $P _ { m } ^ { h } [ n ]$ </td><td rowspan=1 colspan=1>The horizontal propulsion power for theUAV $u _ { m }$ at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\operatorname { T } _ { m } ^ { \operatorname { m a x } }$ </td><td rowspan=1 colspan=1>Themaximum transmission power of the UAV $\overline { { u _ { m } } }$ </td></tr><tr><td rowspan=1 colspan=1> $\frac { \pi \mathrm { a x } } { E _ { m } ^ { \mathrm { m a x } } }$ </td><td rowspan=1 colspan=1>The energybudget for theUAV $\overline { { u _ { m } } }$ </td></tr><tr><td rowspan=1 colspan=1> $\mathbb { P } _ { m , k } ^ { L } [ n ]$ </td><td rowspan=1 colspan=1>Theprobability of thechannelbetweenUAV $u _ { m }$ and ${ \tt B S } _ { { s _ { k } } }$ being ina LoS state at time slot n</td></tr></table>

We denote the 3D location of BS $s _ { k }$ as $\mathbf { g } _ { k } = [ \widetilde { x } _ { k } , \widetilde { y } _ { k } , \widetilde { z } _ { k } ] ^ { \mathrm { T } } \in$ $\mathbb { R } ^ { 3 \times 1 } , \forall k$ . For UAV $u _ { m } ,$ g = [Ë Ë Ë ]its 3D location at time slot n is denoted as $\mathbf { u } _ { m } [ n ] = [ x _ { m } [ n ] , y _ { m } [ n ] , z _ { m } [ n ] ] ^ { \mathrm { T } } \in \mathbb { R } ^ { 3 \times 1 }$ . Here, $[ x _ { m } [ n ] , y _ { m } [ n ] ] ^ { \mathrm { T } } \in \mathbb { R } ^ { 2 \times 1 }$ [ ] [ ]represents the $\mathrm { U A V } _ { \mathrm { \Delta } }$ position on [ [ ] [ ]]the horizontal plane, while $z _ { m } [ n ]$ indicates its altitude. To [ ]make our exposition clearer, we introduce a reference time slot, denoted as slot , such that $\mathbf { u } _ { m } [ 0 ] = \mathbf { u } _ { m , I } .$ . To nav-0 u [0] = uigate safely and adhere to aerial regulations, the UAVâs altitude must be within a defined range, influenced by factors like surrounding structures [38]. This leads to the constraint: $H _ { \mathrm { m i n } } \leq z _ { m } [ n ] \leq H _ { \mathrm { m a x } } , \forall m , n$ , with $H _ { \mathrm { m i n } }$ and $H _ { \mathrm { m a x } }$ representing the allowable altitude bounds. Based on the assumption that the UAV manages its velocity in both horizontal and vertical directions independently [34], we define $\mathbf { v } _ { m } ^ { x y }$ and $v _ { m } ^ { z }$ as its horizontal and vertical velocities, respectively. Specifically, $\begin{array} { r } { { \bf v } _ { m } ^ { x y } [ n ] = [ \frac { x _ { m } [ n ] - x _ { m } [ n - 1 ] } { \delta } , \frac { y _ { m } [ n ] - y _ { m } [ n - 1 ] } { \delta } ] ^ { \mathrm { T } } } \end{array}$ and $\begin{array} { r } { v _ { m } ^ { z } [ n ] = \frac { z _ { m } [ n ] - z _ { m } [ n - 1 ] } { \delta } } \end{array}$ . Both velocities are constrained by [ ] =their maximums, $\underline { { V _ { \mathrm { m a x } } ^ { x y } } }$ and $V _ { \mathrm { m a x } } ^ { z }$ (in m/s), leading to the conditions: $\sqrt { ( x _ { m } [ n ] - x _ { m } [ n - 1 ] ) ^ { 2 } + ( y _ { m } [ n ] - y _ { m } [ n - 1 ] ) ^ { 2 } } \leq$ $V _ { \operatorname* { m a x } } ^ { x y } \delta$ and $| z _ { m } [ n ] - z _ { m } [ n - 1 ] ) | \leq V _ { \operatorname* { m a x } } ^ { z } \delta , \forall n$ [ 1]). The distance max [ ]between any UAV $u _ { m }$ [and BS $s _ { k }$ maxat time slot n is denoted by $d _ { m , k } [ n ] = \| \mathbf { u } _ { m } [ n ] - \mathbf { g } _ { k } \|$

## B. Communication Model

The influence of ground reflections and building scatterings results in A2G channels manifesting either LoS or NLoS properties. Let $c _ { m , k } [ n ]$ represent the channel state between $\mathrm { U A V } ~ u _ { m }$ and BS $s _ { k }$ [ ]at time slot n. Specifically, $c _ { m , k } [ n ] = 1$ indicates a LoS state, while $c _ { m , k } [ n ] = 0$ signifies a NLoS [ ] = 0state. Additionally, we utilize the widely-accepted power-law path-loss model [30] to define the path-loss function for A2G channel:

$$
l _ { m , k } [ n ] = \left\{ \begin{array} { l l } { { d _ { m , k } ^ { - \alpha } [ n ] , } } & { { c _ { m , k } [ n ] = 1 , } } \\ { { \kappa d _ { m , k } ^ { - \alpha } [ n ] , } } & { { c _ { m , k } [ n ] = 0 . } } \end{array} \right.\tag{1}
$$

Here, $\alpha \geq 2$ signifies the path-loss exponent. The factor $\kappa <$ 2 accounts for the additional path loss introduced by the 1NLoS link. In line with 3GPP standards [40], each BS is equipped with directional antennas. These antennas, set at a downtilt angle of $\theta _ { D } \in [ 0 ^ { \circ } , 9 0 ^ { \circ } ]$ , are realized through a [0 90 ]vertical uniform linear array (ULA) composed of $N _ { 0 }$ el-0ements. As derived in [41], the directional antenna gain from UAV $u _ { m }$ towards BS $s _ { k }$ at time slot n is given by $\begin{array} { r } { G _ { m , k } [ n ] = \frac { ( 1 0 ^ { \frac { \mathrm { t } _ { e } } { 1 0 } } ) \sin ^ { 2 } ( \frac { N _ { 0 } \pi } { 2 } ( \sin \theta _ { m , k } [ n ] - \sin \theta _ { D } ) ) } { N _ { 0 } \sin ^ { 2 } ( \frac { \pi } { 2 } ( \sin \theta _ { m , k } [ n ] - \sin \theta _ { D } ) ) } } \end{array}$ , where $G _ { e } \triangleq$ $\begin{array} { r } { - \operatorname* { m i n } ( 1 2 ( \frac { \theta _ { m , k } [ n ] } { H P B W _ { v } } ) ^ { 2 } , G _ { 0 } ) } \end{array}$ is defined as the minimal element power gain in dB. Here, $\theta _ { m , k } [ n ] \triangleq$ arcsin $\Big ( \frac { \tilde { z } _ { k } - z _ { m } [ n ] } { d _ { m , k } [ n ] } \Big )$ [ ] arcsinrepresents the elevation angle at time slot n, $G _ { 0 }$ [ ] )is the threshold for antenna nulls, and $H P B W _ { v }$ 0stands for the half-power beamwidth. Let $h _ { m , k } [ n ]$ signify the baseband [ ]equivalent channel coefficient for the A2G channel between UAV $u _ { m }$ and $\mathrm { ~ B S ~ } \ s _ { k }$ at time slot n, which can be split into $h _ { m , k } [ n ] = \sqrt { G _ { m , k } [ n ] \beta _ { m , k } [ n ] } \tilde { h } _ { m , k } [ n ]$ . In this expression, $\tilde { h } _ { m , k } [ n ]$ is a complex random variable normalized such that $\mathbb { E } [ | \tilde { h } _ { m , k } [ n ] | ^ { 2 } ] = 1$ , illustrating small-scale fading. $\beta _ { m , k } [ n ] =$ $\beta _ { 0 } l _ { m , k } [ n ] = ( c _ { m , k } [ n ] + ( 1 - c _ { m , k } [ n ] ) \kappa ) \beta _ { 0 } d _ { m , k } ^ { - \alpha } [ n ]$ represents 0 [ ] = ( [ ] + (1 [ ]) )the large-scale channel coefficient with $\beta _ { 0 }$ [ ]being the channel gain at a reference distance of $d _ { 0 } = 1$ 0m. Given the realization 0 = 1of the urban environment, UAVs are assumed to have real-time access to instantaneous CSI during their flight [34], [39], where the UAVsâ on-board sensors allow them to actively measure the CSI in real-time. This capability enables them to dynamically identify channel state $\{ c _ { m , k } [ n ] \}$ by examining whether the [ ]A2G channelâs line is obstructed by any building structures. Consequently, with each A2G channel refresh, the UAV can precisely ascertain the type of large-scale pathloss. To further enhance the accuracy and timeliness of CSI, real-time feedback mechanisms is incorporated from the BSs as well. For practical implementations, the BSs can also deduce and update the CSI by continuously monitoring the uplink signals received from the UAVs [34]. As such, both UAVs and BSs contribute to the CSI acquisition and have access to real-time CSI, making the communication system more robust and responsive to the dynamic aerial environment.

To ensure UAVs do not degrade the performance of terrestrial users, we allocate an exclusive frequency band with bandwidth B for A2G communications. This band is shared by all UAVs for communication with BSs, effectively removing the potential for inter-cell interference from terrestrial networks as in [16], [42]. We assume that terrestrial BSs adopt time division multiple access to cater to the M aerial users due to its simplicity and computational efficiency [43], [44], which can also facilitate coordinated and synchronized data transmission. Furthermore, we restrict each UAV to connect with at most one BS during any given time slot. Let $x _ { m , k } [ n ] \in \{ 0 , 1 \}$ be a binary variable: $x _ { m , k } [ n ] = 1$ [indicates that UAV $u _ { m }$ 0 1schedules a transmission to [ ] = 1the associated BS $s _ { k }$ during time slot $n ,$ and  otherwise. Thus, $\begin{array} { r } { \sum _ { m = 1 } ^ { M } x _ { m , k } [ n ] \le 1 , \forall k } \end{array}$ , n and $\begin{array} { r } { \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] \le 1 , \forall m , n } \end{array}$ . The =1 [ ] 1transmission power of UAV $u _ { m }$ =1 [ ] 1at time slot n is represented as $p _ { m } [ n ]$ , such that $0 \leq p _ { m } [ n ] \leq P _ { m } ^ { \mathrm { m a x } }$ , where $P _ { m } ^ { \mathrm { m a x } }$ is the [ ] 0 [ ]maximum transmission power of $u _ { m } .$ . The achievable rate from $u _ { m }$ to $s _ { k }$ at time slot n is

$$
R _ { m , k } [ n ] = { \cal B } \log _ { 2 } \bigg ( 1 + \frac { p _ { m } [ n ] | h _ { m , k } [ n ] | ^ { 2 } } { \sum _ { j = 1 , j \neq m } ^ { M } p _ { j } [ n ] | h _ { j , k } [ n ] | ^ { 2 } + \sigma ^ { 2 } } \bigg ) ,\tag{2}
$$

with $\sigma ^ { 2 }$ as the receiverâs noise power. The term $\textstyle \sum _ { j = 1 , j \neq m } ^ { M }$ $p _ { j } [ n ] | h _ { j , k } [ n ] | ^ { 2 }$ signifies the interference from other $\mathrm { U A V s } ^ { \prime }$ [ ] [ ]transmissions at time slot n. Hence, the data upload rate from $u _ { m }$ to the cellular network is $\begin{array} { r } { \sum _ { k = 1 } ^ { K } x _ { m , k } [ \bar { n } ] R _ { m , k } [ n ] . } \end{array}$ , =1 [ ]and the aggregate uplink throughput for UAV $u _ { m }$ ]is $\begin{array} { r } { \delta \sum _ { n = 1 } ^ { N } \sum _ { k = 1 } ^ { \tilde { K } ^ { - } } \dot { x _ { m , k } } [ n ] \dot { R } _ { m , k } [ n ] } \end{array}$

## C. Energy Consumption Model

The energy consumption for a UAV encompasses two main components: communication energy and propulsion energy. For a given UAV $u _ { m }$ at time slot $n ,$ the communication-related energy is denoted by ${ \cal E } _ { m } ^ { C } [ n ] = p _ { m } [ n ] \delta$ . Diving deeper into propul-[ ] = [ ]sion energy, this consumption can be further categorized into horizontal (level flight) and vertical energy consumption within a 3D space. For any time slot n, the horizontal propulsion power for $\begin{array} { r } { u _ { m } \mathrm { i s } P _ { m } ^ { h } [ n ] = ( P _ { 0 } + \frac { 3 P _ { 0 } \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 2 } } { U _ { t r _ { 1 } n } ^ { 2 } } + \frac { 1 } { 2 } d _ { 0 } \tilde { \rho } s \boldsymbol { A } \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 3 } ) + } \end{array}$ $\begin{array} { r } { P _ { i } ( \sqrt { 1 + \frac { \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } ) ^ { 1 / 2 } } \end{array}$ , where $v _ { 0 }$ and $U _ { t i p }$ repre-4 2sent the average rotor induced velocity and the tip speed of the rotor blade, respectively [30], [46]. The terms $P _ { i }$ and $P _ { 0 }$ are 0the induced and blade profile power during hovering. Furthermore, $d _ { 0 } , s , A .$ , and $\tilde { \rho }$ are the fuselage drag ratio, rotor solid-0 Ëity, rotor disc area, and air density, respectively. Considering vertical propulsion, the power consumption is modeled as a linear function based on [26], expressed as $P _ { m } ^ { v } [ n ] = G v _ { m } ^ { z } [ n ]$ for all positive $v _ { m } ^ { z } [ n ]$ , where G is the UAVâs weight. Notably, [ ]the UAVâs weight can be depicted as $G = \tilde { m } g$ , with g and m representing gravitational acceleration and the UAVâs mass, respectively. We assume that $P _ { m } ^ { v } [ n ] = 0$ for $v _ { m } ^ { z } [ n ] \leq 0$ as autorotation can be employed during UAV vertical descents, where the propulsion power can be negated [45]. The total propulsion energy consumption for UAV $u _ { m }$ at time slot n is thus given by $\bar { E _ { m } ^ { P } } [ n ] = \delta ( \mathsf { \bar { P } } _ { m } ^ { h } [ n ] + \operatorname* { m a x } \{ G v _ { m } ^ { z } [ n ] , 0 \} )$ . Consequently, the [ ] = ( [ ] + max [ ] 0 )cumulative energy consumption of the UAV over the entire time horizon $T$ can be expressed as $\begin{array} { r } { E _ { m } = \sum _ { n = 1 } ^ { N } ( E _ { m } ^ { P } [ n ] + E _ { m } ^ { C } [ n ] ) } \end{array}$ .

## III. PROBLEM STATEMENT AND PROPOSED ONLINE DESIGN

In an urban context with numerous buildings, multiple cellular-connected UAVs uploads data to cellular networks with co-channel interference. During their flights, the UAVs are equipped to accurately estimate the instantaneous CSI in real-time with individual BSs. To ensure fairness across the network, our aim is to enhance the lowest uplink throughput for every UAV. Elevating the lowest throughput ensures that all UAVs achieve a baseline performance level, which is crucial for applications requiring coordinated multi-UAV operations while ensuring more stable and reliable network operations. This is accomplished by optimizing the three key factors: the 3D trajectory of the UAV, denoted as $\{ \mathbf { u } _ { m } [ n ] \}$ }, the communication scheduling, $\{ x _ { m , k } [ n ] \}$ u [ ], and the transmission power, $\{ p _ { m } [ n ] \}$ [ ]The optimization problem can be formulated as follow:

$$
( \mathrm { P 1 } ) : \operatorname* { m a x } _ { \substack { \eta , \{ \mathbf { u } _ { m } [ n ] \} , \{ x _ { m } [ n ] \} , \{ p _ { m } [ n ] \} } } \eta
$$

$$
\mathrm { s . t . } \sum _ { n = 1 } ^ { N } \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] R _ { m , k } [ n ] \geq \eta , \forall m ,\tag{3}
$$

$$
x _ { m , k } [ n ] \in \{ 0 , 1 \} , \forall m , k , n ,\tag{4}
$$

$$
\sum _ { m = 1 } ^ { M } x _ { m , k } [ n ] \leq 1 , \forall k , n ,\tag{5}
$$

$$
\sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] \leq 1 , \forall m , n ,\tag{6}
$$

$$
0 \leq p _ { m } [ n ] \leq P _ { m } ^ { \mathrm { m a x } } , \forall m , n ,\tag{7}
$$

$$
\delta \sum _ { n = 1 } ^ { N } ( ( P _ { m } ^ { h } [ n ] + \operatorname* { m a x } \{ G v _ { m } ^ { z } [ n ] , 0 \} ) + p _ { m } [ n ] ) \leq E _ { m } ^ { \operatorname* { m a x } } , \forall m ,\tag{8}
$$

$$
\lVert \mathbf { v } _ { m } ^ { x y } [ n ] \rVert \leq V _ { \operatorname* { m a x } } ^ { x y } , \forall m , n ,
$$

$$
| v _ { m } ^ { z } [ n ] | \leq V _ { \mathrm { m a x } } ^ { z } , \forall m , n ,\tag{9}
$$

(10)

$$
{ \bf u } _ { m } [ 0 ] = { \bf u } _ { m , I } , { \bf u } _ { m } [ N ] = { \bf u } _ { m , F } , \forall m ,\tag{11}
$$

$$
\| \mathbf { u } _ { m } [ n ] - \mathbf { u } _ { j } [ n ] \| \geq D _ { \operatorname* { m i n } } , \forall m \neq j , \forall n ,\tag{12}
$$

where $D _ { \mathrm { m i n } }$ denotes the minimum safe separation distance. The minabove optimization is conducted while respecting the energy constraints for each UAV, with $E _ { m } ^ { \mathrm { m a x } }$ representing the energy budget for a specific UAV $u _ { m }$ . The UAVâs starting and destination points are given by $\mathbf { u } _ { m , I }$ and $\mathbf { u } _ { m , F }$ respectively. It is worthwhile to note that $P _ { m } ^ { h } [ n ]$ uis a function of velocity $\mathbf { v } _ { m } ^ { x y } [ n ]$ due to its definition, and $R _ { m , k } [ n ]$ is determined by $p _ { m } [ n ]$ [ ]and ${ \bf u } _ { m } [ n ]$ [ ]due to its definition in (2) since $h _ { m , k } [ n ]$ [depends on ${ \bf u } _ { m } [ n ]$ [ ]. As a [ ] u [ ]result, the above design variables are closely coupled in (P1) and the joint optimization of these variables is crucial. Furthermore, itâs essential to note the inherent unpredictability due to the unavailability of instantaneous CSI between the UAV and the BSs for each time slot. This means $\{ h _ { m , k } [ n ] \}$ is, in essence, a random variable. Even if $\{ h _ { m , k } [ n ] \}$ is given in advance, (P1) is a [ ]mixed-integer non-convex optimization problem. Consequently, itâs difficult to identify the optimal solution to problem (P1) directly.

Given the UAVâs ability to precisely estimate the instantaneous CSI in real-time with each BS during its flight, it can dynamically adjust its trajectory and communication scheduling as well as power allocation based on the measured CSI. Thus, at the start of every time slot, both trajectory design and resource allocation are carried out online, updating the real-time policies accordingly. Note that the pre-flight knowledge of the CDI can further aid in optimizing the design. As such, we propose two online design schemes in this paper: the Online Design with CDI and the Online Design without CDI. Both aim to provide suboptimal solutions to problem (P1). For the Online Design with CDI scheme, we leverage both the achievable rate, derived from the estimated instantaneous CSI of the current time slot, and the anticipated data rate for upcoming slots based on the CDI. We develop an efficient strategy to obtain suboptimal solution by combining the exact penalty method with alternating optimization and successive convex optimization techniques. Conversely, the proposed Online Design without CDI scheme exclusively relies on the achievable rate from the estimated instantaneous CSI of the present time slot. We have developed an energy-triggered penalty term to oversee UAV energy consumption, offering a suboptimal solution even in the absence of pre-flight CDI knowledge.

## IV. ONLINE DESIGN WITH CDI

In this section, we examine the online trajectory and resource allocation design, taking into account both the instantaneous CSI during the flight and the CDI. We propose an online design approach that optimizes resource allocation and UAV movements for each time slot, incorporating varying design variables. The optimization problem for each slot is formulated as a mixed-integer non-convex optimization problem. To address this, we present an efficient algorithm that yields a suboptimal solution.

## A. Online Design Strategy

We employ the probabilistic model presented in [47], [48] to compute the likelihood of the channel between UAV $u _ { m }$ and BS $s _ { k }$ being in a LoS state at time slot n, which is represented as $\begin{array} { r } { \mathbb { P } _ { m , k } ^ { L } [ n ] = \frac { 1 } { 1 + C \exp ( - D [ \theta _ { m , k } [ n ] - C ] ) } } \end{array}$ . In this formula, C 1+ exp( [ [ ] ])and D are constants that depend on the specific environment, and $\begin{array} { r } { \theta _ { m , k } [ n ] = \arcsin ( \frac { \tilde { z } _ { k } - z _ { m } [ n ] } { d _ { m , k } [ n ] } ) } \end{array}$ represents the elevation angle at time slot $n ,$ with $z _ { m } [ n ]$ [ ]denoting the height of the UAV $u _ { m }$ [ ]at time slot n. As such, the probability that an A2G channel experiences NLoS conditions is $\begin{array} { r } { \mathbb { P } _ { m , k } ^ { \boldsymbol { N } ^ { \star } } ( n ) = 1 - \mathbb { P } _ { m , k } ^ { L } ( n ) } \end{array}$ ( ) = 1 ( )Furthermore, the small-scale fading of the A2G channel follows Rician fading under LoS conditions, and Rayleigh fading under NLoS conditions [30]. Thus, we have $\mathbb { E } [ | h _ { m , k } [ n ] | ^ { 2 } ] =$ $G _ { m , k } [ n ] \hat { \mathbb { P } } _ { m , k } ^ { L } [ n ] \beta _ { 0 } d _ { m , k } [ n ] ^ { - \alpha }$ , where $\hat { \mathbb { P } } _ { m , k } ^ { L } [ n ]$ is a modified LoS probability $\hat { \mathbb { P } } _ { m , k } ^ { L } [ n ] = \mathbb { P } _ { m , k } ^ { L } [ n ] + ( 1 - \mathbb { P } _ { m , k } ^ { L } [ n ] ) \kappa$ . This intro-[ ] = [ ] + (1 [ ])duces an additional factor Îº for the likelihood of NLoS occurrence. In this section, we operate under the assumption that statistical CDI (e.g., the LoS probabilistic model and fading model) is accessible before the UAVâs flight. In this case, probabilistic modeling provides a means to estimate future channel states, enhancing the robustness and efficacy of our online design process for forthcoming time slots.

<!-- image-->  
Fig. 1. An illustration of the online design with CDI at time slot $n ^ { \prime } .$

We focus on an online design for trajectory and resource allocation, which is determined at each discrete time slot. We label the current time slot as $n ^ { \prime } ,$ , where $1 \leq n ^ { \prime } \leq N$ . Within this time slot $n ^ { \prime } { . }$ 1, the UAV has the capability to obtain instantaneous CSI such as $G _ { m , k } [ n ^ { \prime } ] , c _ { m , k } [ n ^ { \prime } ] .$ , and $\lceil \tilde { h } _ { m , k } [ n ^ { \prime } ]$ by initiating a [ ] [ ] [ ]handshake process with the BSs at the slotâs onset. In practice, when the $\mathrm { U A V } ~ u _ { m }$ is at location $\mathbf { u } _ { m } [ n ^ { \prime } - 1 ]$ at the beginning of the time slot n	 , it can measure $G _ { m , k } [ n ^ { \prime } ]$ 1]and $c _ { m , k } [ n ^ { \prime } ]$ based on [ ] [ ]the current elevation angle and an inspection of any obstructions, such as buildings, in the UAV-to-BS path, which remain constant throughout the n	 th slot. It is crucial to note that the small-scale fading coefficient is subject to frequent shifts, where a single n	 th slot might encompass L fading blocks, $L \geq 1$ . Addressing this challenge, we gather the CSI of the latest $L$ fading blocks up to the point $\mathbf { u } _ { m } [ n ^ { \prime } - 1 ]$ and use their average as the estimated $\tilde { h } _ { m , k } [ n ^ { \prime } ]$ u [ 1]for the n	 th slot. Despite a potential performance [ ]discrepancy due to this estimation, a reduction in slot duration diminishes the gap. When Î´ is sufficiently small, L nears 1, making the performance variance negligible [13]. Consequently, the data rate achievable from $\mathrm { U A V } ~ u _ { m }$ to BS $s _ { k }$ during the n	 th slot is:

$$
\begin{array} { l } { { R _ { m , k } [ n ^ { \prime } ] = B \log _ { 2 } } } \\ { { \left( 1 + \frac { p _ { m } [ n ^ { \prime } ] G _ { m , k } [ n ^ { \prime } ] \beta _ { m , k } [ n ^ { \prime } ] | \tilde { h } _ { m , k } [ n ^ { \prime } ] | ^ { 2 } } { \sum _ { j = 1 , j \ne m } ^ { M } p _ { j } [ n ^ { \prime } ] G _ { j , k } [ n ] \beta _ { j , k } [ n ^ { \prime } ] | \tilde { h } _ { j , k } [ n ^ { \prime } ] | ^ { 2 } + \sigma ^ { 2 } } \right) } } \end{array}\tag{13}
$$

For forthcoming slots, n where $n ^ { \prime } < n \leq N$ , instantaneous CSI is not accessible by the UAV. Note the UAV is aware of the statistical CDI before flight. Therefore, we resort to the expected data rate for these subsequent slots in our online optimization. The expected data rate from $\mathrm { U A V } u _ { m }$ to ${ \mathrm { B S } } \ s _ { k }$ during the slot n is $\mathbb { E } [ R _ { m , k } [ n ] ]$ for $n ^ { \prime } < n \leq N$ . This can be approximated using [ [ ]]the result from [49] as:

Proposition 1: ([49, Theorem 1]). For independent random variables X (with $X \geq 0 )$ and Y (with $Y > 0 )$ , the approximation E $\begin{array} { r } { [ \log _ { 2 } ( 1 + \frac { X } { Y } ) ] \approx \log _ { 2 } ( 1 + \frac { \mathbb { E } [ X ] } { \mathbb { E } [ Y ] } ) } \end{array}$ 0holds.

Let $X = p _ { m } [ n ] | h _ { m , k } [ n ] | ^ { 2 }$ and $\begin{array} { r } { Y = \sum _ { j = 1 , j \neq M } ^ { M } p _ { j } [ n ] | h _ { j , k } [ n ] | ^ { 2 } } \end{array}$ $+ \sigma ^ { 2 }$ . Utilizing Proposition 1 to evaluate $\mathbb { E } [ R _ { m , k } [ n ] ]$ , we obtain

E Rm,k n â B [ ] [ [ ] ]-j=1,j=m pj n E |hj,k n | 2 Ï2 ) M pm n E |hm,k n | 2 Blog2(1+ -j=1,j=m pj n Gj,k n PËLj,k n Î²0dj,k n âÎ± Ï2 ) M pm n Gm,k n PLm,k n Î²0dm,k n âÎ± Itâs noteworthy that both $\hat { \mathbb { P } } _ { m , k } ^ { L } [ n ]$ and $G _ { m , k } [ n ]$ are intricate [ ] [ ]functions with respect to the UAV trajectory ${ \bf u } _ { m } [ n ]$ , u [ ]rendering them challenging to address directly. By adopting the homogeneous approximation method from [30], [50], we simplify as $\hat { \mathbb { P } } _ { m , k } ^ { L } [ n ] \approx \bar { \mathbb { P } } _ { m , k } ^ { L }$ and $G _ { m , k } [ n ] \approx \bar { G } _ { m , k } ,$ ân, where $\bar { \mathbb { P } } _ { m , k } ^ { L }$ and $\bar { G } _ { m , k }$ are average values derived from the straight-line path between $\mathbf { u } _ { m , I }$ and $\begin{array} { r } { \mathbf { u } _ { m , F } . } \end{array}$ . Such u uapproximation retains high accuracy as discussed in [30]. Thus, our estimated data rate becomes $\mathbb { E } [ R _ { m , k } [ n ] ] \approx B \log _ { 2 } ( 1 +$ $\begin{array} { r } { \frac { p _ { m } [ n ] \bar { G } _ { m , k } \bar { \mathbb { P } } _ { m , k } ^ { L } \beta _ { 0 } d _ { m , k } [ n ] ^ { - \alpha } } { \sum _ { j = 1 , j \neq m } ^ { M } p _ { j } [ n ] \bar { G } _ { j , k } \bar { \mathbb { P } } _ { j , k } ^ { L } \beta _ { 0 } d _ { j , k } [ n ] ^ { - \alpha } + \sigma ^ { 2 } } \Big ) \stackrel { \Delta } { = } \bar { R } _ { m , k } [ n ] } \end{array}$ For the [ ] [ ] +present time slot n	 , the data rate $R _ { m , k } [ n ^ { \prime } ]$ can be precisely [ ]determined using (13). Thus, to streamline the development of an efficient joint design approach, we use $\bar { R } _ { m , k } [ n ]$ as our [ ]anticipated data rate for upcoming time slots. It is worthwhile to note that such approximation allows for a tractable analysis of expected data rates, acknowledging that while not exact, it provides an estimation for the purposes of optimizing UAV flight paths and resource allocation. The use of expected data rates over future time slots serves as an auxiliary tool to inform the decision-making process for current slot optimization. Given that these future estimations do not directly influence the immediate operational decisions but rather guide the overall strategic approach, the impact of variance on the approximationâs accuracy is neglected.

At the beginning of each time slot $n ^ { \prime } ,$ , an online design is executed, updating the real-time resource allocation and trajectory optimization. Specifically, when optimizing the design variables at time slot $n ^ { \prime }$ , the entire N time slots are partitioned into three parts, $\mathrm { i . e . , 1 ) }$ Historical Phase (Before n	 ): Weâve already determined $\{ x _ { m , k } [ n ] , \mathbf { u } _ { m } [ n ] , p _ { m } [ n ] \} _ { 1 \leq n < n ^ { \prime } }$ [ ] u [ ]from previous time slots; 2) Current Phase $( n ^ { \prime } ) \colon$ The design variables $\{ x _ { m , k } [ n ^ { \prime } ] , \mathbf { u } _ { m } [ n ^ { \prime } ] , p _ { m } [ n ^ { \prime } ] \}$ are opti-[ ] u [ ] [ ]mized in the current slot using the instantaneous CSI represented by $( G _ { m , k } [ n ^ { \prime } ] , \beta _ { m , k } [ \bar { n ^ { \prime } } ] , \tilde { h } _ { m , k } [ n ^ { \prime } ] ) ; 3 )$ Future ( [ ] [ ] [ ])Phase (After n	 ): The design variables for future slots, $\{ x _ { m , k } [ n ] , { \mathbf { u } } _ { m } [ n ] , p _ { m } [ n ] \} _ { n ^ { \prime } < n \leq N }$ , are optimized in the current slot using CDI values $( \bar { G } _ { m , k } , \bar { \mathbb { P } } _ { m , k } ^ { L } )$ . It is worthwhile to ( )note that the UAV re-evaluates its strategy at each time slot $n ^ { \prime } .$ . This involves adjusting both its trajectory and resource allocation with BSs across all future slots $n ^ { \prime } \leq n \leq N$ due to the energy constraints. Based on such framework, the online design for each time slot $n ^ { \prime } , 1 \leq n ^ { \prime } \leq N$ primarily concerns the design variables $\{ x _ { m , k } [ n ] , { \mathbf { u } } _ { m } [ n ] , p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N }$ , and the [ ] u [ ] [ ]optimization problem can thus be expressed as:

$$
\begin{array} { l } { { \displaystyle ( { \mathrm { P 2 } } ) : \operatorname* { m a x } _ { \eta , \{ x _ { m , k } [ n ] , { \mathbf { u } } _ { m } [ n ] , p _ { m } [ n ] \} _ { n ^ { \prime } \le n \le N } } \eta } } \\ { { \displaystyle \mathrm { s . t . ~ } \sum _ { n = 1 } ^ { n ^ { \prime } - 1 } \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] R _ { m , k } [ n ] + \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ^ { \prime } ] R _ { m , k } [ n ^ { \prime } ] } } \end{array}
$$

$$
+ \sum _ { n = n ^ { \prime } + 1 } ^ { N } \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] \bar { R } _ { m , k } [ n ] \geq \eta , \forall m ,\tag{14}
$$

$$
x _ { m , k } [ n ] \in \{ 0 , 1 \} , \forall m , k , n \geq n ^ { \prime } ,\tag{15}
$$

$$
\sum _ { m = 1 } ^ { M } x _ { m , k } [ n ] \leq 1 , \forall k , n \geq n ^ { \prime } ,\tag{16}
$$

$$
\sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] \leq 1 , \forall m , n \geq n ^ { \prime } ,\tag{17}
$$

$$
0 \leq p _ { m } [ n ] \leq P _ { m } ^ { \operatorname* { m a x } } , \forall m , n \geq n ^ { \prime } ,\tag{18}
$$

$$
\delta \sum _ { n = 1 } ^ { N } ( ( P _ { m } ^ { h } [ n ] + \operatorname* { m a x } \{ G v _ { m } ^ { z } [ n ] , 0 \} ) + p _ { m } [ n ] ) \leq E _ { m } ^ { \operatorname* { m a x } } , \forall m ,\tag{19}
$$

$$
\| \mathbf { v } _ { m } ^ { x y } [ n ] \| \leq V _ { \operatorname* { m a x } } ^ { x y } , \forall m , n \geq n ^ { \prime } ,\tag{20}
$$

$$
| v _ { m } ^ { z } [ n ] | \leq V _ { \mathrm { m a x } } ^ { z } , \forall m , n \geq n ^ { \prime } ,\tag{21}
$$

$$
\mathbf { u } _ { m } [ N ] = \mathbf { u } _ { m , F } , \forall m ,\tag{22}
$$

$$
\| \mathbf { u } _ { m } [ n ] - \mathbf { u } _ { j } [ n ] \| ^ { 2 } \geq D _ { \operatorname* { m i n } } ^ { 2 } , \forall m \neq j , n \geq n ^ { \prime } ,\tag{23}
$$

In (P2), Î· represents the minimum uploading throughput for all UAVs, as delineated by constraint (14). Specifically, for forthcoming time slots where the CSI information remains unavailable, we focus on the predicted data rate of the UAVs for any future time slot $n ,$ where $n ^ { \prime } < n \leq N$ . The set $\{ x _ { m , k } [ n ] , \mathbf { u } _ { m } [ n ] , p _ { m } [ n ] \} _ { 1 \leq n < n ^ { \prime } }$ was previously established [ ] u [ ] [ ] 1through online optimization for the time slot n, with $n <$ $n ^ { \prime }$ . Hence, terms like $\begin{array} { r } { \sum _ { n = 1 } ^ { n ^ { \prime } - 1 } \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] R _ { m , k } [ n ] \stackrel { \Delta } { = } \Gamma _ { m , n ^ { \prime } - 1 } } \end{array}$ and $\delta \Sigma _ { n = 1 } ^ { n ^ { \prime } - 1 } ( ( P _ { m } ^ { h } [ n ] +$ max $\{ G v _ { m } ^ { z } [ n ] , 0 \} ) + p _ { m } [ n ] ) \triangleq \Omega _ { n ^ { \prime } - 1 }$ =1 (( [ ] + max [ ] 0 ) + [ ]) Î© 1are known in advance. However, during the current time slot $n ^ { \prime } { . }$ , the achievable rate $R _ { m , k } [ n ^ { \prime } ]$ depends on the design variable $\mathbf { u } _ { m } [ n ^ { \prime } ]$ [ ]with given the measured CSI. Our online control apu [ ]proach is detailed in Algorithm 1. In Algorithm 1, we determine the online resource allocation and trajectory by addressing problem (P2) iteratively. Note that (P2) is a mixed-integer non-convex optimization problem, which has an intrinsic complexity when trying to solve it. Despite this, the following subsections will outline a more tractable suboptimal solution to (P2).

## B. Proposed Solution to Problem (P2)

In this subsection, we develop an efficient strategy to obtain suboptimal solution to (P2) by integrating exact penalty method (EPM) [51], alternating optimization, and successive convex approximation (SCA) to address the inherent complexity of (P2). EPM is utilized to transform the mixed-integer non-convex problem into a equivalent continuous optimization problem. This step is crucial for breaking down the complexity of the original problem and making it more tractable. Alternating optimization is utilized by decomposing the complex problem into simpler sub-problems, each focusing on a different set of variables (trajectory, power, scheduling) while fixing the others, which ensures that each aspect of the problem can be addressed systematically. SCA is employed to approximate non-convex

1: Initialize solution set $\Lambda _ { m } = \varnothing , \forall m ;$

2: Obtain $( \bar { G } _ { m , k } , \bar { \mathbb { P } } _ { m , k } ^ { L } )$ Î =using CDI;

3: for $n ^ { \prime } = 1 \mathrm { t o } \ N \ \mathbf { d o }$

= 14: Compute $\Gamma _ { m , n ^ { \prime } - 1 }$ and $\Omega _ { n ^ { \prime } - 1 }$ based on $\Lambda _ { m }$

Î 1 Î© 15: Carry out CSI measurement to fetch

$$
( G _ { m , k } [ n ^ { \prime } ] , c _ { m , k } [ n ^ { \prime } ] , \tilde { h } _ { m , k } [ n ^ { \prime } ] ) ;
$$

6: $\mathrm { D e t e r m i n e ~ } \{ x _ { m , k } [ n ] , { \mathbf { u } } _ { m } [ n ] , p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N }$ and

$\{ R _ { m , k } [ n ^ { \prime } ] \}$ [ ] u [ ] [ ]by solving problem (P2);

7: $\mathbf { f o r } \operatorname { e a c h } \mathrm { U A V } \ u _ { m }$ do

8: The $\mathrm { U A V } ~ u _ { m }$ connects to BS $s _ { k }$ when $x _ { m , k } [ n ^ { \prime } ] = 1$ configuring its transmit power to $p _ { m } [ n ^ { \prime } ]$ [and progressing towards location $\mathbf { u } _ { m } [ n ^ { \prime } ] ;$

9: end for

10: Update $\Lambda _ { m }$ as

$$
\bar { \Lambda _ { m } } = \Lambda _ { m } \bigcup \{ x _ { m , k } [ n ^ { \prime } ] , \mathbf { u } _ { m } [ n ^ { \prime } ] , p _ { m } [ n ^ { \prime } ] , R _ { m , k } [ n ^ { \prime } ] \} ;
$$

Î =11: end for

constraints with convex ones iteratively, leading to a sequence of convex optimization problems that can be efficiently solved.

1) Problem Reformulation: First, we convert the binary variable constraint in (15) into equivalent ones. Considering two matrices Ï,  â RmÃkÃn, let us define the Frobenius norm of as $\begin{array} { r } { \| \mathbf { b } \| _ { F } \triangleq ( \sum _ { i = 1 } ^ { m } \sum _ { j = 1 } ^ { k } \sum _ { l = 1 } ^ { n } | b _ { i j l } | ^ { 2 } ) ^ { 1 / 2 } } \end{array}$ . The notation $\langle \pi , \mathbf { b } \rangle$ b ( =1 =1 =1 ) brepresents the sum of all elements in their Hadamard product Ï â¦ , and $\pi \preceq 0$ indicates that each element of $\pi$ does not b 0exceed 0. With these definitions, we introduce an extension to the theorem initially proposed in [51].

Theorem 1: Let $\Theta \triangleq \{ ( \pi , \mathbf { b } ) | 0 \preceq \pi \preceq 1 , \| 2 \mathbf { b } - 1 \| _ { F } ^ { 2 } \leq$ mkn, $\langle 2 \pi - 1 , 2 \mathbf { b } - 1 \rangle = m k n \}$ b) 0}. If $( \pmb { \pi } , \mathbf { b } ) \in \Theta$ 2b 1, then $\pi \in$ $\{ 0 , 1 \} ^ { \dot { m } \times k \times n }$ 1 2and $\mathbf { b } \in \{ 0 , 1 \} ^ { m \times k \times n }$ (n, and $\pi = \mathbf { b }$

1 b 0 1 = bProof: In the proof, we establish the relationships between the binary nature of the matrices $\pi$ and  by employing bthe Cauchy-Schwarz Inequality and the Squeeze Theorem [51]. First, we aim to establish that $\pi \in \{ 0 , 1 \} ^ { m \times k \times n }$ 0 1Given the provided definition and invoking the Cauchy-Schwarz Inequality, we have $m k n = \left. 2 \pi - 1 , 2 \mathbf { b } - 1 \right. \leq$ $\| 2 \pi - 1 \| _ { F } \| 2 \mathbf { b } - 1 \| _ { F } \leq \sqrt { m k n } \| 2 \pi - 1 \| _ { F }$ 1 2b 1 This implies $\Vert 2 \pi - 1 \Vert _ { F } \geq { \sqrt { m k n } }$ 2 1. Furthermore, considering the constraint $0 \preceq \pi \preceq 1$ , it follows that $\| 2 \pi - 1 \| _ { F } ^ { 2 } \leq$ mkn. Coupling 0 1these insights yields $\Vert 2 \pi - 1 \Vert _ { F } ^ { 2 } = \bar { m } k n$ Consequently, given that $\pi \in \mathbb { R } ^ { m \times k \times n }$ 2 1 =and the aforementioned constraints, we deduce that $\pi \in \{ 0 , 1 \} ^ { m \times k \times n }$ Second, to demonstrate ${ \bf b } \in \{ 0 , 1 \} ^ { m \times k \times n } ,$ 0 1 we start by noting mkn  Ï $\begin{array} { r } { - 1 , 2 \mathbf { b } - 1 \rangle = \sum _ { i = 1 } ^ { m } \sum _ { j = 1 } ^ { k } \sum _ { l = 1 } ^ { n } ( 2 \pi _ { i j l } - 1 ) ( 2 b _ { i j l } - 1 ) \le \sum _ { i = 1 } ^ { m } \sum _ { l = 1 } ^ { n } ( 2 b _ { i j l } - 1 ) ( 2 b _ { i j l } - 1 ) ( 2 b _ { i j l } - 1 ) , } \end{array}$ $\begin{array} { r } { \sum _ { j = 1 } ^ { k } \sum _ { l = 1 } ^ { n } | 2 \pi _ { i j l } - 1 | | 2 b _ { i j l } - 1 | \leq \sum _ { i = 1 } ^ { m } \sum _ { j = 1 } ^ { k } \sum _ { l = 1 } ^ { n } | 2 b _ { i j l } } \end{array}$ $- 1 | \leq \sqrt { m k n } \| 2 \mathbf { b } - 1 \| _ { F } .$ As such, itâs evident that $\| 2 \mathbf { b } - 1 \| _ { F } ^ { 2 } \geq m k n$ 1. Given that $\| 2 \mathbf { b } - 1 \| _ { F } ^ { 2 } \leq m k n$ and by 2b 1 2b 1employing the Squeeze Theorem, all equalities are automatically satisfied. Using the equality condition of the Cauchy-Schwarz Inequality, we conclude that $\mathbf { \Psi } \in \{ 0 , 1 \} ^ { m \times k \times n }$ . Lastly, given that both Ï and  reside in $\{ 0 , 1 \} ^ { m \times k \times n }$ , and considering the relation $m k n = \left. 2 \pi - 1 , 2 \mathbf { b } - 1 \right.$ , we deduce $\pi = \mathbf b$ = 2 1 2b 1 = bIncorporating the above discussions, the proof is thus concluded. 

From Theorem 1, we establish a variable matrix $\mathbf { x \in }$ $\{ 0 , 1 \} ^ { M \times K \times ( N - n ^ { \prime } + 1 ) }$ corresponding to $\{ x _ { m , k } [ n ] \} _ { n ^ { \prime } \leq n \leq N \cdot } \mathrm { \bf ~ B y }$ introducing an auxiliary variable matrix, $\begin{array} { r } { \dot { \mathbf { b } } \in \mathbb { R } ^ { \bar { M } \times \bar { K } \times \bar { ( } N ^ { - } n ^ { \prime } + 1 \bar { ) } } } \end{array}$ bwe can state that constraint (14) yields three distinct constraints: $0 \preceq \mathbf { x } \preceq 1 , \| 2 \mathbf { b } - 1 \| _ { F } ^ { 2 } \leq M K ( N - n ^ { \prime } + 1 )$ , and $\langle 2 { \bf x } - 1 , 2 { \bf b } - 1 \rangle = M K ( N - n ^ { \prime } + 1 )$ ( + 1). Consequently, we can 2x 1 2b 1 =recast problem (P2) into:

$$
( \mathrm { P 3 } ) : \operatorname* { m a x } _ { \substack { \mathbf { x } , \mathbf { b } , \eta , \{ \mathbf { u } _ { m } [ n ] , p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N } } } \eta
$$

$$
{ \mathrm { s . t . ~ } } ( 1 4 ) , ( 1 6 ) { - } ( 2 3 ) .
$$

$$
0 \preceq \mathbf { x } \preceq 1 ,\tag{24}
$$

$$
\left\| 2 \mathbf { b } - 1 \right\| _ { F } ^ { 2 } \leq M K ( N - n ^ { \prime } + 1 ) ,\tag{25}
$$

$$
\langle 2 { \bf x } - 1 , 2 { \bf b } - 1 \rangle = M K ( N - n ^ { \prime } + 1 ) ,\tag{26}
$$

where $\mathbf { b } , \mathbf { x } \in \mathbb { R } ^ { M \times K \times ( N - n ^ { \prime } + 1 ) }$ . This implies that the initial b xdiscrete integer optimization problem (P2) is now recast into its continuous counterpart (P3). Let us define $\Upsilon _ { m , k } [ n ^ { \prime } ] \stackrel { \triangle } { = }$ $G _ { m , k } [ n ^ { \prime } ] ( c _ { m , k } [ n ^ { \prime } ] \ + \ ( 1 - c _ { m , k } [ n ^ { \prime } ] ) \kappa ) \beta _ { 0 } | \tilde { h } _ { m , k } [ n ^ { \prime } ] | ^ { 2 }$ and $\bar { \Upsilon } _ { m , k } \triangleq \bar { G } _ { m , k } \bar { \mathbb { P } } _ { m , k } ^ { L } \beta _ { 0 }$ . To solve (P3), we introduce a penalty Î¥ 0method using EPM, leading us to a new optimization problem (P4):

$$
\begin{array} { r l } & { \left( \mathrm { P 4 } \right) : \underset { \mathbf { x } , \mathbf { b } , \eta , \left\{ \mathbf { u } _ { m } \left[ n \right] , p _ { m } \left[ n \right] \right\} _ { n ^ { \prime } \le n \le N } } { \operatorname* { m a x } } \ \eta - \rho ( M K ( N - n ^ { \prime } + 1 ) } \\ & { } \\ & { \qquad - \left. 2 \mathbf { x } - 1 , 2 \mathbf { b } - 1 \right. ) } \\ & { \qquad \mathrm { s . t . ~ } \left( 1 6 \right) - ( 1 8 ) , ( 2 0 ) - ( 2 5 ) , } \end{array}
$$

$$
\begin{array} { l } { \displaystyle \Gamma _ { m , n ^ { \prime } - 1 } + \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ^ { \prime } ] B \log _ { 2 } } \\ { \displaystyle \left( 1 + \frac { p _ { m } [ n ^ { \prime } ] \Gamma _ { m , k } [ n ^ { \prime } ] \left\| { \bf u } _ { m } [ n ^ { \prime } ] - { \bf g } _ { k } \right\| ^ { - \alpha } } { \sum _ { j = 1 , j \ne j } ^ { M } p _ { j } [ n ^ { \prime } ] \Gamma _ { j , k } [ n ^ { \prime } ] \left\| { \bf u } _ { j } [ n ^ { \prime } ] - { \bf g } _ { k } \right\| ] ^ { - \alpha } + \sigma ^ { 2 } } \right) } \\ { + \displaystyle \sum _ { n = n ^ { \prime } + 1 } ^ { N } \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] B \log _ { 2 } } \\ { \displaystyle \left( 1 + \frac { p _ { m } [ n ] \bar { \Gamma } _ { m , k } \| { \bf u } _ { m } [ n ] - { \bf g } _ { k } \| ^ { - \alpha } } { \sum _ { j = 1 , j \ne k } ^ { M } p _ { j } \left\| { \bf D } _ { j , k } \right\| \left\| { \bf u } _ { j } [ n ] - { \bf g } _ { k } \right\| ^ { - \alpha } + \sigma ^ { 2 } } \right) \ge \eta , \forall m , } \end{array}\tag{27}
$$

$$
\begin{array} { r l } & { \Omega _ { n ^ { \prime } - 1 } + \delta \displaystyle \sum _ { n = n ^ { \prime } } ^ { N } ( ( P _ { m } ^ { h } [ n ] + \operatorname* { m a x } \{ G v _ { m } ^ { z } [ n ] , 0 \} ) + p _ { m } [ n ] ) } \\ & { \quad \le E _ { m } ^ { \operatorname* { m a x } } , \forall m , } \end{array}\tag{28}
$$

In (P4), $\rho > 0$ is a penalty parameter progressively increased to 0satisfy the equality constraint in (26). Itâs worth noting that both $\Gamma _ { m , n ^ { \prime } - 1 }$ and $\Omega _ { n ^ { \prime } - 1 }$ are predetermined in preceding time slots. Î 1Additionally, $\Upsilon _ { m , k } [ n ^ { \prime } ]$ is determined due to instantaneous CSI at the time slot $n ^ { \prime } { . }$ [ ], whereas $\bar { \Upsilon } _ { m , k }$ is determined via a homogenous Î¥approximation strategy based on CDI. In the following, we will focus on solving (P4) with fixed $\rho .$

Problem (P4) is a non-convex optimization problem due to non-convex constraints (27) and (28) with coupled design variables: , , $\{ \mathbf { u } _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N }$ , and $\{ p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N }$ , which x b u [ ] [ ]is challenging to tackle directly. To provide a more tractable approach, we partition (P4) into three distinct subproblems: transmit power and auxiliary variable optimization, 3D trajectory optimization, and transmission scheduling optimization. Both the transmit power and auxiliary variable optimization, as well as the 3D trajectory optimization, are non-convex. However, they can be rendered convex using the first order Taylor approximation. On the other hand, transmission scheduling optimization is a linear programming problem and can be directly tackled. Consequently, we develop an efficient algorithm that iteratively addresses these three subproblems to yield a suboptimal solution.

2) Power Optimization Subproblem: For a given UAV 3D trajectory $\{ \mathbf { u } _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N }$ and transmission scheduling , the u [ ]first subproblem is expressed as

$$
\begin{array} { r l r } {  { ( { \mathrm { P 5 } } ) : \operatorname* { m a x } _ { { \bf b } , \eta , \{ p _ { m } [ n ] \} _ { n ^ { \prime } \le n \le N } } \eta - \rho ( M K ( N - n ^ { \prime } + 1 ) } } \\ & { } & \\ & { } & { \quad -  2 { \bf x } - 1 , 2 { \bf b } - 1  ) } \\ & { } & \\ & { } & { \mathrm { s . t . } ( 1 8 ) , ( 2 5 ) , ( 2 7 ) , ( 2 8 ) . } \end{array}
$$

However, solving (P5) is challenging due to the non-convex constraint (27). By adopting the successive convex approximation (SCA) method, we can approximate the non-convexity. Specifically, given $R _ { m , k } [ n ^ { \prime } ]$ is expressed as $R _ { m , k } [ n ^ { \prime } ] =$ $\begin{array} { r } { B \log _ { 2 } ( \sum _ { j = 1 } ^ { M } p _ { j } [ n ^ { \prime } ] \Upsilon _ { j , k } [ n ^ { \prime } ] \| { \bf u } _ { j } [ n ^ { \prime } ] - { \bf g } _ { k } \| ^ { - \alpha } + \sigma ^ { 2 } ) - B \log _ { 2 } } \end{array}$ $\begin{array} { r } { ( \sum _ { j = 1 , j \neq m } ^ { M } p _ { j } [ n ^ { \prime } ] \Upsilon _ { j , k } [ n ^ { \prime } ] \| \mathbf { u } _ { j } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { - \alpha } + \sigma ^ { 2 } ) \triangleq \hat { R } _ { k } [ n ^ { \prime } ] - } \end{array}$ $\check { R } _ { m , k } [ n ^ { \prime } ]$ =, we define the transmission power in the r-th iteration as $p _ { m } ^ { r } [ n ^ { \prime } ]$ . As $\check { R } _ { m , k } [ n ^ { \prime } ]$ is concave, its first-order Taylor expansion at $p _ { m } ^ { r } [ n ^ { \prime } ]$ ] is given by $\check { R } _ { m , k } [ n ^ { \prime } ] = B \log _ { 2 }$ $\begin{array} { r } { ( \sum _ { j = 1 , j \neq m } ^ { M } p _ { j } [ n ^ { \prime } ] \Upsilon _ { j , k } [ n ^ { \prime } ] \| \mathbf { u } _ { j } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { - \alpha } + \sigma ^ { 2 } ) \leq B \log _ { 2 } } \end{array}$ $\begin{array} { r } { \big ( \sum _ { j = 1 , j \neq m } ^ { M } p _ { j } ^ { r } [ n ^ { \prime } ] \Upsilon _ { j , k } [ n ^ { \prime } ] \| { \bf u } _ { j } [ n ^ { \prime } ] - { \bf g } _ { k } \| ^ { - \alpha } + \sigma ^ { 2 } \big ) + B } \end{array}$ $\begin{array} { r } { \sum _ { j = 1 , j \neq m } ^ { M } \frac { \Upsilon _ { j , k } \left[ n ^ { \prime } \right] \| \mathbf { u } _ { j } \left[ n ^ { \prime } \right] - \mathbf { g } _ { k } \| ^ { - \alpha } \log _ { 2 } ( e ) } { \sum _ { l = 1 , l \neq m } ^ { M } \Upsilon _ { l , k } \left[ n ^ { \prime } \right] \| \mathbf { u } _ { l } \left[ n ^ { \prime } \right] - \mathbf { g } _ { k } \| ^ { - \alpha } + \sigma ^ { 2 } } \big ( p _ { j } \big [ n ^ { \prime } \big ] - p _ { j } ^ { r } \big [ n ^ { \prime } \big ] \big ) \triangleq } \end{array}$ $\check { R } _ { m , k } ^ { [ e ] } [ n ^ { \prime } ]$ where $\check { R } _ { m , k } ^ { [ e ] } [ n ^ { \prime } ]$ is a linear function. Thus, $R _ { m , k } [ n ^ { \prime } ] \geq \hat { R } _ { k } [ n ^ { \prime } ] - \check { R } _ { m , k } ^ { [ e ] } [ n ^ { \prime } ]$ . Following the same logic for $\bar { R } _ { m , k } [ n ]$ , we obtain $\bar { R } _ { m , k } [ n ] \geq \hat { \bar { R } } _ { k } [ n ] - \check { \bar { R } } _ { m , k } ^ { [ e ] } [ n ]$ , where $\hat { \bar { \cal R } } _ { k } [ n ]$ and $\check { R } _ { m , k } ^ { [ e ] } [ n ]$ are similar to $\hat { R } _ { k } [ n ^ { \prime } ]$ and $\check { R } _ { m , k } ^ { [ e ] } [ n ^ { \prime } ]$ achieved by substituting $\Upsilon _ { j , k } [ n ^ { \prime } ]$ with $\bar { \Upsilon } _ { j , k }$ . This leads to the approximation of (P5) as

$$
\begin{array} { r l r } {  { ( { \mathrm { P 6 } } ) : \operatorname* { m a x } _ { { \mathbf { b } } , \eta , \{ p _ { m } [ n ] \} _ { n ^ { \prime } \le n \le N } } \eta - \rho ( M K ( N - n ^ { \prime } + 1 ) } } \\ & { } & \\ & { } & { -  2 \mathbf { x } - 1 , 2 \mathbf { b } - 1  ) } \end{array}
$$

s.t. (18), (25), (28),

$$
\begin{array} { r l } {  { \Gamma _ { m , n ^ { \prime } - 1 } + \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ^ { \prime } ] ( \hat { R } _ { k } [ n ^ { \prime } ] - \check { R } _ { m , k } ^ { [ e ] } [ n ^ { \prime } ] ) } \quad } & { } \\ & { + \sum _ { n = n ^ { \prime } + 1 } ^ { N } \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] ( \hat { \bar { R } } _ { k } [ n ] - \check { R } _ { m , k } ^ { [ e ] } [ n ] ) \geq \eta , \forall m , } \end{array}\tag{29}
$$

which is convex and can be effectively solved using CVX [52].

3) Trajectory Optimization Subproblem: Given the fixed transmission scheduling  and transmit power $\{ p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N }$ , and x [ ]the auxiliary variable , we aim to optimize the UAV 3D trajectory. The second subproblem can be formulated as:

$$
\begin{array} { r l } & { ( \mathrm { P 7 } ) : \underset { \eta , \{ \mathbf { u } _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N } } { \operatorname* { m a x } } \eta - \rho ( M K ( N - n ^ { \prime } + 1 ) } \\ & { - \left. 2 \mathbf { x } - 1 , 2 \mathbf { b } - 1 \right. ) } \\ & { \mathrm { s . t . } \ ( 2 0 ) { - } ( 2 3 ) , ( 2 7 ) , ( 2 8 ) . } \end{array}
$$

Note that constraints (23), (27) and (28) are non-convex concerning $\{ \mathbf { u } _ { m } [ n ] \}$ . To approximate (23), we have $\Vert \mathbf { u } _ { m } [ n ] -$ $\mathbf { u } _ { j } [ n ] \| ^ { 2 } \geq - \| \mathbf { u } _ { m } ^ { r } [ n ] - \mathbf { u } _ { j } ^ { r } [ n ] \| ^ { 2 } + 2 ( \mathbf { u } _ { m } ^ { r } [ n ] - \mathbf { u } _ { j } ^ { r } [ n ] ) ^ { \mathrm { { T } } } ( \mathbf { u } _ { m } [ n ]$ $- \mathbf { u } _ { j } [ n ] )$ u [ ] u [ ] + 2(u [ ]by applying linearization over term $\Vert \mathbf { u } _ { m } [ n ] - \mathbf { u } _ { j } [ n ] \Vert ^ { 2 }$ u [ ])around the point $( \mathbf { u } _ { m } ^ { r } [ n ] , \mathbf { u } _ { j } ^ { r } [ n ] )$ u [ ] u [ ]. To approximate (27), we represent $R _ { m , k } [ n ^ { \prime } ]$ as $R _ { m , k } [ n ^ { \prime } ] = \hat { R } _ { k } [ n ^ { \prime } ] - \check { R } _ { m , k } [ n ^ { \prime } ]$ . By viewing $\| { \bf u } _ { j } [ n ^ { \prime } ] - { \bf g } _ { k } \| ^ { \alpha }$ [ ] = [ ] [ ]as a variable, we establish that both $\hat { R } _ { k } [ n ^ { \prime } ]$ and $\check { R } _ { m , k } [ n ^ { \prime } ]$ are convex. This necessitates the transformation of $\hat { R } _ { k } [ n ^ { \prime } ]$ into a concave function. Defining $\mathbf { u } _ { m } ^ { r } [ n ^ { \prime } ]$ [ ]as the 3D location in the r-th iteration, we derive the u [ ]first-order expansion of $\hat { R } _ { k } [ n ^ { \prime } ] \mathrm { a t } \| \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { \alpha } , \mathrm { i . e . , } \hat { R } _ { k } [ n ^ { \prime } ] \geq$ $\begin{array} { r } { B \log _ { 2 } ( \sum _ { j = 1 } ^ { M } p _ { j } [ n ^ { \prime } ] \Upsilon _ { j , k } [ n ^ { \prime } ] \| \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { - \alpha } + \sigma ^ { 2 } ) - B \sum _ { j = 1 } ^ { M } } \end{array}$ $\Psi _ { j , k } [ n ^ { \prime } ] ( \| \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { \alpha } - \| \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { \alpha } ) \triangleq \dot { R } _ { k } [ n ^ { \prime } ]$ =1, where $\begin{array} { r } { \Psi _ { j , k } [ n ^ { \prime } ] = \frac { \log _ { 2 } ( e ) \Upsilon _ { j , k } [ n ^ { \prime } ] \| \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { - \alpha - 1 } p _ { j } [ n ^ { \prime } ] } { \sum _ { i = 1 } ^ { M } p _ { j } [ n ^ { \prime } ] \Upsilon _ { j , k } [ n ^ { \prime } ] \| \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { - \alpha } + \sigma ^ { 2 } } } \end{array}$ . Accordingly, we have $R _ { m , k } [ n ^ { \prime } ] \geq \dot { R } _ { k } [ n ^ { \prime } ] - \check { R } _ { m , k } [ n ^ { \prime } ]$ , which is still non-concave [ ]with respect to $\mathbf { u } _ { j } [ n ^ { \prime } ]$ ]due to $\check { R } _ { m , k } [ n ^ { \prime } ]$ . To address this, we u [ ]introduce the slack variable $s _ { j , k } [ n ^ { \prime } ]$ [ ], constraining it such that $\| \mathbf { u } _ { j } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { \alpha } \geq s _ { j , k } [ n ^ { \prime } ]$ [ ]. Recognizing the non-convex nature u [ ] g [ ]of this constraint due to $\| \mathbf { u } _ { j } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { \alpha }$ , we approximate it u [ ]with the first-order expansion at $\mathbf { u } _ { i } ^ { r } [ n ^ { \prime } ]$ as $\| \mathbf { u } _ { j } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { \alpha } \geq$ $\| \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { \alpha } + \alpha \| \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } \| ^ { \tilde { \alpha } - 2 } ( \mathbf { u } _ { j } ^ { r } [ n ^ { \prime } ] - \mathbf { g } _ { k } ) ^ { \mathrm { T } } ( \mathbf { u } _ { j }$ $[ n ^ { \prime } ] - \mathbf { g } _ { k } )$ g + u [ ] g (u [ ]. On the other hand, by substituting $\| \mathbf { u } _ { j } [ n ^ { \prime } ] - \bar { \mathbf { g } _ { k } } \| ^ { \alpha }$ [ ]with $s _ { j , k } [ n ^ { \prime } ]$ in $\check { R } _ { m , k } [ n ^ { \prime } ]$ , we upper bound $\mathbb { \breve { R } } _ { m , k } [ n ^ { \prime } ]$ by $\begin{array} { r } { \check { R } _ { m , k } [ n ^ { \prime } ] \leq B \log _ { 2 } ( { \sum _ { j = 1 , j \neq m } ^ { M } \frac { p _ { j } [ n ^ { \prime } ] \Upsilon _ { j , k } [ n ^ { \prime } ] } { s _ { i , k } [ n ^ { \prime } ] } + \sigma ^ { 2 } } ) \triangleq \ddot { R } _ { m , k } [ n ^ { \prime } ] } \end{array}$ , =1 =rendering it convex. Finally, $R _ { m , k } [ n ^ { \prime } ]$ is approximated as a concave function $\dot { R } _ { k } [ n ^ { \prime } ] - \ddot { R } _ { m , k } [ n ^ { \prime } ]$ . Using a parallel approach for $\bar { R } _ { m , k } [ n ]$ [ ] [ ], we similarly deduce that $\bar { R } _ { m , k } [ n ]$ can be approximated to a concave function $\dot { \bar { R } } _ { k } [ n ] - \ddot { \bar { R } } _ { m , k } [ n ]$ , where $\dot { \bar { R } } _ { k } [ n ]$ and $\ddot { \bar { R } } _ { m , k } [ n ]$ are similar to $\dot { R } _ { k } [ n ^ { \prime } ]$ and $\ddot { R } _ { m , k } [ n ^ { \prime } ]$ , achieved [ ]by substituting $\Upsilon _ { j , k } [ n ^ { \prime } ]$ with $\bar { \Upsilon } _ { j , k }$

To approximate constraint (28), we introduce auxiliary variables, denoted as $\{ \xi _ { m } [ n ] \}$ . These variables are defined such that $\begin{array} { r } { \xi _ { m } [ n ] \geq ( \sqrt { 1 + \frac { \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } ) ^ { 1 / 2 } } \end{array}$ . This can be reformulated as $\begin{array} { r } { \frac { 1 } { \xi _ { m } ^ { 2 } [ n ] } \leq \xi _ { m } ^ { 2 } [ n ] + \frac { \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 2 } } { v _ { 0 } ^ { 2 } } } \end{array}$ . It is worth noting that the expression $\begin{array} { r } { \xi _ { m } ^ { 2 } [ n ] + \frac { \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 2 } } { v _ { 0 } ^ { 2 } } } \end{array}$ is jointly convex with respect to $\xi _ { m } [ n ]$ and ${ \bf v } _ { m } ^ { x y } [ n ]$ . This observation leads [ ] v [ ]us to employ the SCA technique to address the complexity. As a result, we derive the following constraint $\frac { 1 } { \xi _ { m } ^ { 2 } [ n ] } \leq$ $\zeta _ { m } [ n ]$ , where $\zeta _ { m } [ n ] \triangleq ( \xi _ { m } ^ { r } [ n ] ) ^ { 2 } + 2 \xi _ { m } ^ { r } [ n ] ( \xi _ { m } [ n ] - \xi _ { m } ^ { r } [ n ] ) +$ $\frac { | | ( \mathbf { v } _ { m } ^ { \bar { x } y } [ n ] ) ^ { r } | | ^ { 2 } + 2 ( ( \bar { \mathbf { v } } _ { m } ^ { x y } [ n ] ) ^ { r } ) ^ { \mathrm { T } } ( \mathbf { v } _ { m } ^ { \bar { x } y } [ n ] - ( \mathbf { v } _ { m } ^ { x y } [ n ] ) ^ { \bar { r } } ) } { v _ { 0 } ^ { 2 } }$ . The expression for $\zeta _ { m } [ n ]$ serves as a lower-bound approximation of $\xi _ { m } ^ { 2 } [ n ] +$ $\frac { \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 2 } } { v _ { 0 } ^ { 2 } }$ , derived using the first-order Taylor expansion around the reference points $\xi _ { m } ^ { r } [ n ]$ and $( \mathbf { v } _ { m } ^ { x y } [ n ] ) ^ { r }$ during the r-th it-[ ] (v [ ])eration. As such, the propulsion power for $\mathrm { U A V } ~ u _ { m }$ at time slot $n ,$ , represented as $P _ { m } ^ { h } [ n ]$ , can be reformulated into a convex form $\begin{array} { r } { \hat { P } _ { m } ^ { h } [ n ] = P _ { 0 } + \frac { 3 P _ { 0 } \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 2 } } { U _ { \mathit { t } + { n } } ^ { 2 } } + \frac { 1 } { 2 } d _ { 0 } \tilde { \rho } s A \| \mathbf { v } _ { m } ^ { x y } [ n ] \| ^ { 3 } + } \end{array}$ $P _ { i } \xi _ { m } [ n ]$ . Based on the above discussions, we can approximate [ ]problem (P7) as:

$$
\begin{array} { r l } {  { ( { \bf P } 8 ) : \operatorname* { m a x } _ { \substack { \eta , \{ \xi _ { m } [ n ] , s _ { j , k } [ n ] , { \bf u } _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N } } } \eta - \rho ( M K ( N - n ^ { \prime } + 1 ) } } \\ & { -  2 { \bf x } - 1 , 2 { \bf b } - 1  ) } \end{array}
$$

$$
- \mathbf { u } _ { j } [ n ] ) \geq D _ { \operatorname* { m i n } } ^ { 2 } , \forall m \neq j , n ^ { \prime } \leq n \leq N ,\tag{30}
$$

$$
\left\| \mathbf { u } _ { j } ^ { r } [ n ] - \mathbf { g } _ { k } \right\| ^ { \alpha } + \alpha \left\| \mathbf { u } _ { j } ^ { r } [ n ] - \mathbf { g } _ { k } \right\| ^ { \alpha - 2 } ( \mathbf { u } _ { j } ^ { r } [ n ] - \mathbf { g } _ { k } ) ^ { \mathrm { T } }
$$

$$
\mathbf { \nabla } \times ( \mathbf { u } _ { j } [ n ] - \mathbf { g } _ { k } ) \geq s _ { j , k } [ n ] , n ^ { \prime } \leq n \leq N ,\tag{31}
$$

$$
{ \frac { 1 } { \xi _ { m } ^ { 2 } [ n ] } } \leq \zeta _ { m } [ n ] , n ^ { \prime } \leq n \leq N ,\tag{32}
$$

$$
\begin{array} { l } { { \displaystyle \Gamma _ { m , n ^ { \prime } - 1 } + \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ^ { \prime } ] ( \dot { R } _ { k } [ n ^ { \prime } ] - \ddot { R } _ { m , k } [ n ^ { \prime } ] ) } } \\ { { \displaystyle + \sum _ { n = n ^ { \prime } + 1 } ^ { N } \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ] ( \dot { \bar { R } } _ { k } [ n ] - \ddot { \bar { R } } _ { m , k } [ n ] ) } , } \end{array}\tag{33}
$$

$$
\begin{array} { r l r } {  { \Omega _ { n ^ { \prime } - 1 } + \delta \sum _ { n = n ^ { \prime } } ^ { N } ( ( \hat { P } _ { m } ^ { h } [ n ] + \operatorname* { m a x } \{ G v _ { m } ^ { z } [ n ] , 0 \} ) + p _ { m } [ n ] ) } } \\ & { } & { \leq E _ { m } ^ { \operatorname* { m a x } } , \forall m . \qquad ( 3 4 ) } \end{array}
$$

The problem (P8) is convex and can be effectively solved using CVX. By replacing the non-concave terms in (P7) with its lowerbound approximations in (P8), it can be shown that any feasible solution to (P8) inherently satisfies (P7), and thus the objective value of (P8) provides a lower bound to that of (P7).

4) Scheduling Optimization Subproblem: For optimizing transmission scheduling, is adjusted using and $\{ p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N }$ obtained from $( \mathrm { P } 6 ) .$ , and $\{ \mathbf { u } _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N }$ from [ ](P8). Thus, the third subproblem is

$$
( \mathrm { P 9 } ) : \operatorname* { m a x } _ { \mathbf { x } , \eta } \eta - \rho \left( M K ( N - n ^ { \prime } + 1 ) - \langle 2 \mathbf { x } - 1 , 2 \mathbf { b } - 1 \rangle \right)
$$

s.t. (16), (17), (24), (27).

Problem (P9) is a conventional linear programming which is directly solvable using CVX.

5) Overall Algorithm and Convergence Analysis: Taking into account the previous discussions, to tackle the original problem (P3), we iteratively solve (P4) with a fixed $\rho ,$ maximizing $\eta - \rho M K ( N - n ^ { \prime } + 1 )$ over $\{ \mathbf { x } , \mathbf { b } , \{ \mathbf { u } _ { m } [ n ] , p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N } \}$ ( + 1) x b u [ ] [ ]Detailed iteration steps for the EPM method in addressing (P3) are outlined in Algorithm 2. Initially, a small value is chosen for $\rho$ to provide greater adaptability in optimizing the uplink throughput. Over iterations, $\rho$ is gradually increased until it meets its peak at $\rho _ { \mathrm { m a x } }$ . It can be shown that with sufficiently large $\rho _ { \mathrm { m a x } } ,$ condition (26) is satisfied, and  will converge max xto either 0 or 1 [51]. In addition, convergence with fixed $\rho$ is guaranteed when $\rho _ { \mathrm { m a x } }$ is achieved. Specifically, considering the maxr-th iterationâs objective as $O b j ( \bar { \mathbf { x } ^ { r } } , \mathbf { b } ^ { r } , \{ \bar { \mathbf { u } _ { m } ^ { r } } [ n ] \} , \{ p _ { m } ^ { r } \bar { [ n ] } \} )$ ï¼ (x b u [ ] [ ] )improvements in power allocation lead to a better objective value, i.e., $O b j ( \mathbf { x } ^ { r } , \mathbf { b } ^ { r } , \{ \mathbf { u } _ { m } ^ { r } [ n ] \} , \{ p _ { m } ^ { r } [ n ] \} ) \leq$ $O b j ( \mathbf { x } ^ { r } , \mathbf { b } ^ { r + 1 } , \{ \mathbf { u } _ { m } ^ { r } [ n ] \} , \{ p _ { m } ^ { r + 1 } [ n ] \} )$ u [ ] [ ] ) The 3D trajectory (x b u [ ] [ ] )gets updated in the next step with an even higher objective value. Transmission scheduling then undergoes reallocation, ensuring the objective value does not diminish. Thus, we have $\bar { O b } j ( \mathbf { x } ^ { r + 1 } , \mathbf { b } ^ { r + 1 } , \{ \mathbf { u } _ { m } ^ { r + 1 } [ n ] \} , \{ p _ { m } ^ { r + 1 } [ n ] \} ) \ge$ $O b j ( \mathbf { x } ^ { r } , \mathbf { b } ^ { r } , \{ \mathbf { u } _ { m } ^ { r } [ n ] \} , \{ p _ { m } ^ { r } [ n ] \} )$ u [ ] [ ] ). Due to the limitations in (x b u [ ] [ ] )communication resources, the uplink throughput is bound to a maximum value. This guarantees the convergence of Algorithm 2. It provides a suboptimal solution to problem (P2), satisfying all constraints, including the safe distance constraint. The computational complexity of solving (P6), (P8), and (P9) via CVX depend on the number design variables, resulting in a complexity of $O ( ( K M ( N - \bar { n ^ { \prime } } + 1 ) ^ { 3 . 5 } ) )$ (( ( + 1) ))Therefore, the overall computational complexity of Algorithm 2 is $O ( I ( K M ( N - n ^ { \prime } + \bar { 1 } ) ) ^ { 3 . 5 } )$ , with I denoting iteration ( (number.

Algorithm 2: EPM for Solving the Problem (P2).   
1: Initialize $\mathbf { x } ^ { 0 } , \mathbf { b } ^ { 0 } , \{ \mathbf { u } _ { m } ^ { 0 } [ n ] , p _ { m } ^ { 0 } [ n ] \} _ { n ^ { \prime } \leq n \leq N } .$ ; Set iteration   
index as $r = 0 ;$ u [ ] [ ] Initialize penalty parameters $\rho ^ { 0 } > 0$   
$\rho _ { \mathrm { m a x } } > 0 ,$ = 0 and $c > 1$   
max2: repeat   
3: Solve the convex problem (P6) with given and $\mathbf { x } ^ { r }$   
$\{ \mathbf { u } _ { m } ^ { r } [ n ] , p _ { m } ^ { r } [ n ] \} _ { n ^ { \prime } \leq n \leq N } ;$ x denote the optimal auxiliary   
u [ ] [ ]variable and transmit power as $\mathbf { b } ^ { r + 1 }$ and   
$\{ p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N } ^ { r + 1 } .$ , respectively;   
4: Solve the convex problem (P8) with given $\mathbf { x } ^ { r } , \mathbf { b } ^ { r + 1 }$   
$\{ p _ { m } [ n ] \} _ { n ^ { \prime } \leq n \leq N } ^ { r + 1 } ,$ and $\{ \mathbf { u } _ { m } ^ { r } [ n ] \} _ { n ^ { \prime } \leq n \leq N } ;$ x b denote the   
optimal 3D trajectory as $\{ \mathbf { u } _ { m } ^ { r + 1 } [ n ] \} _ { n ^ { \prime } \leq n \leq N } ;$   
u [ ]5: Solve the linear problem (P9) with given $\mathbf { b } ^ { r + 1 }$ and   
$\{ \mathbf { u } _ { m } ^ { r + 1 } [ n ] , p _ { m } ^ { r + 1 } [ \bar { n } ] \} _ { n ^ { \prime } \leq n \leq N } ;$ b denote the optimal   
u [ ] [ ]transmission scheduling as $\mathbf { x } ^ { r + 1 }$ ;   
6: Update $\boldsymbol { \rho } ^ { r + 1 } =$ min $\{ c \rho ^ { r } , \rho _ { \mathrm { m a x } } \}$ ;   
7: Update $r = r + 1 ;$   
= + 18: until Convergence is achieved with desired accuracy.

## V. ONLINE DESIGN WITHOUT CDI

In this section, we propose an online scheme without CDI for UAV trajectory design and resource allocation, with the assumption that the UAV can only access instantaneous CSI in realtime throughout its flight. In other words, real-time CSI acquisition through direct measurement forms the foundation of our optimization strategy. We introduce an energy-triggered penalty term in our optimization problem to oversee UAV energy consumption. This term adjusts the optimization objectives based on real-time energy usage estimates, encouraging energy-efficient trajectory adjustments that prevent energy budget overruns. This adaptive mechanism allows UAVs to dynamically adjust their flight paths, communication scheduling, and power allocation in response to the instantaneous channel conditions they encounter, which not only maximizes immediate network performance but also ensures long-term mission feasibility through efficient energy management, even in the absence of pre-flight CDI knowledge.

As outlined in Section IV, the online design process for both trajectory and resource allocation takes place at each individual time slot. At a specific time slot, denoted as $n ^ { \prime } ,$ the UAV has access to the current CSI, represented as $( G _ { m , k } [ n ^ { \prime } ] , c _ { m , k } [ n ^ { \prime } ] , \tilde { h } _ { m , k } [ n ^ { \prime } ] )$ . For upcoming time slots, given [ ] [ ]by the range n where $n ^ { \prime } < n \leq N$ , neither the instantaneous CSI nor the CDI is accessible to the UAV. As a consequence, the online optimization focuses primarily on maximizing the uplink throughput exclusively for the time slot $n ^ { \prime }$ . However, a notable challenge arises as UAVs cannot forecast their trajectories for future time slots. This unpredictability implies that, to reach their final destinations on time, the UAVs might incur substantial flight-related energy consumption in the last few time periods, potentially surpassing the energy budget. Specifically, at the beginning of time slot $n ^ { \prime } ,$ given that UAV $u _ { m }$ is positioned at $\mathbf { u } _ { m } [ n ^ { \prime } - 1 ]$ , the UAVâs cumulative energy consumption for u [ 1]the total time horizon T , denoted $E _ { m } ^ { t } ,$ can be approximated as $E _ { m } ^ { t } = \Omega _ { n ^ { \prime } - 1 } + E _ { m } ^ { c } [ n ^ { \prime } ] + E _ { m } ^ { f } [ N - \ddot { n ^ { \prime } } + 1 ]$ . Here, $E _ { m } ^ { c } [ n ^ { \prime } ]$ de-= Î© 1 + [ ] + [ + 1] [ ]notes the communication energy consumed in the n	 time slot, while $E _ { m } ^ { f } [ N - n ^ { \prime } + 1 ]$ indicates the energy associated with fly-[ + 1]ing over the remaining duration of $N - n ^ { \prime } + 1$ time slots. While $\Omega _ { n ^ { \prime } - 1 }$ is derivable from the prior $n ^ { \prime } - 1$ + 1time slots and $E _ { m } ^ { c } [ n ^ { \prime } ]$ is optimizable in the $n ^ { \prime }$ time slot, $E _ { m } ^ { f } [ N - n ^ { \prime } + 1 ]$ remains [ + 1]uncertain. This uncertainty can result in situations where $E _ { m } ^ { t }$ surpasses the energy threshold $E _ { m } ^ { \mathrm { m a x } }$

To address the above challenge, we first explore the energy minimization problem concerning straight-line flights of the UAV $u _ { m }$ . This involves the UAV $u _ { m }$ flying directly from any starting point $\mathbf { u } _ { m , 0 }$ to its final destination $\mathbf { u } _ { m , F }$ , maintaining constant horizontal $\bar { \mathbf { v } } _ { m } ^ { x y }$ and vertical $\hat { v } _ { m } ^ { z }$ uvelocities within a time duration of $\tilde { T } _ { m }$ vÂ¯ Â¯. This problem can be formulated as:

$$
\begin{array} { l } { ( { \bf P } 1 0 ) : \underset { \bar { T } } { \mathrm { m i n } } \bar { T } \left( P _ { 0 } + \frac { 3 P _ { 0 } \mathrm { \nabla } \| \bar { \bf { v } } _ { m } ^ { x y } \| ^ { 2 } } { U _ { t i p } ^ { 2 } } + \frac { 1 } { 2 } d _ { 0 } \tilde { \rho } s A \| \bar { \bf { v } } _ { m } ^ { x y } \| ^ { 3 } \right. } \\ { \left. + \ P _ { i } \left( \sqrt { 1 + \frac { \| \bar { \bf { v } } _ { m } ^ { x y } \| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \| \bar { \bf { v } } _ { m } ^ { x y } \| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } + \mathrm { m a x } \{ G \bar { v } _ { m } ^ { z } , 0 \} \right) } \end{array}
$$

$$
\mathrm { s . t . } \ \bar { \mathbf { v } } _ { m } ^ { x y } \bar { T } = \tilde { \mathbf { u } } _ { m , F } - \tilde { \mathbf { u } } _ { m , 0 } ,
$$

$$
\bar { v } _ { m } ^ { z } \bar { T } = H _ { m , F } - H _ { m , 0 } ,\tag{35}
$$

(36)

$$
\hat { T } \leq \tilde { T } _ { m } ,\tag{37}
$$

where $\tilde {  { \mathbf { u } } } _ { m , F }$ and $\tilde {  { \mathbf { u } } } _ { m , 0 }$ signify the horizontal coordinates of $\mathbf { u } _ { m , F }$ and $\mathbf { u } _ { m , 0 }$ , respectively. $H _ { m , F }$ and $H _ { m , 0 }$ usignify the altitudes of $\mathbf { u } _ { m , F }$ and $\mathbf { u } _ { m , 0 } ,$ 0 respectively. Note that (P10) is a nonlinear opu u 0timization problem with a single design variable T . We employ the golden section search method [53] to solve (P10), illustrated in Algorithm 3. Here, $\bar { E } _ { m } ( \bar { T } )$ represents the objective function ( )of (P10) considering flight time $\bar { T }$

To address the $\mathrm { U A V } _ { \mathrm { \Delta } }$ energy constraints for online design at time slot $n ^ { \prime }$ , we set ${ \bf u } _ { m , 0 } = { \bf u } _ { m } [ n ^ { \prime } - 1 ]$ and $\tilde { T } _ { m } = ( N -$ $n ^ { \prime } + 1 ) \delta .$ By applying Algorithm 3, we can compute the min-+ 1)imal energy consumption for the UAVâs flight, represented as $\hat { E } _ { m } ^ { f } [ N - \hat { n ^ { \prime } } + 1 ]$ . Therefore, it it necessary that the following energy constraint is met, i.e., $\Omega _ { n ^ { \prime } - 1 } + E _ { m } ^ { c } \dot { [ n ^ { \prime } ] } + \hat { E } _ { m } ^ { f } [ N - n ^ { \prime } ] \stackrel {  } { + }$ $1 ] \leq E _ { m } ^ { \mathrm { m a x } }$ Î© 1 + [ ] + [ +. To facilitate the online optimization on a per-slot basis, we introduce an energy-triggered penalty term $E _ { m } ^ { p } [ n ^ { \prime } ]$ into our objective function, which can be expressed as:

Algorithm 3: Golden Section Search Algorithm for Solving   
Problem (P10).   
1: Input: $\mathbf { u } _ { m , F } , \mathbf { u } _ { m , 0 } , \tilde { T } _ { m } ;$   
u2: Initialize $\bar { T } _ { 1 } ^ { L } = 0 , \bar { T } _ { 1 } ^ { R } = \tilde { T } _ { m } ;$ ; initialize the tolerance $\epsilon ,$   
and set $l = 1 ;$   
3: Compute $g _ { 1 } ^ { L } = \bar { T } _ { 1 } ^ { L } + 0 . 3 8 2 ( \bar { T } _ { 1 } ^ { R } - \bar { T } _ { 1 } ^ { L } ) , g _ { 1 } ^ { R } = \bar { T } _ { 1 } ^ { L } +$   
$0 . 6 1 8 ( \bar { T } _ { 1 } ^ { R } - \bar { T } _ { 1 } ^ { L } )$   
0 618(4: repeat   
5: if $\bar { E } _ { m } ( \bar { T } _ { 1 } ^ { L } ) \geq \bar { E } _ { m } ( \bar { T } _ { 1 } ^ { R } )$ then   
6: $\bar { T } _ { l + 1 } ^ { L } = g _ { l } ^ { L } , g _ { l + \bot } ^ { L } = g _ { l } ^ { R } , \bar { T } _ { l + 1 } ^ { R } = \bar { T } _ { l } ^ { R } , g _ { l + 1 } ^ { R } = \bar { T } _ { l + 1 } ^ { L } +$   
$0 . \dot { 6 } 1 8 ( \bar { T } _ { l + 1 } ^ { R } - \bar { T } _ { l + 1 } ^ { L } ) ;$   
0 617: else $\bar { T } _ { l + 1 } ^ { L } \stackrel { . . . } { = } \bar { T } _ { l } ^ { L } , g _ { l + 1 } ^ { R } = g _ { l } ^ { L } , \bar { T } _ { l + 1 } ^ { R } = g _ { l } ^ { R } , g _ { l + 1 } ^ { L } =$   
$\bar { T } _ { l + 1 } ^ { L } + 0 . 3 8 2 ( \bar { T } _ { l + 1 } ^ { R } - \bar { T } _ { l + 1 } ^ { L } ) ;$   
8: +1 +end if   
9: $n = n + 1 ;$   
10: until $\bar { T } _ { l } ^ { R } - \bar { T } _ { l } ^ { L } < \epsilon ;$   
11: Output: $\begin{array} { r } { \bar { T } ^ { * } = \frac { \bar { T } _ { l } ^ { L } + \bar { T } _ { l } ^ { R } } { 2 } } \end{array}$ and $\bar { E } _ { m } ( \bar { T } ^ { * } )$

$$
E _ { m } ^ { p } [ n ^ { \prime } ] = \Omega _ { n ^ { \prime } - 1 } + E _ { m } ^ { c } [ n ^ { \prime } ] + \varphi \hat { E } _ { m } ^ { f } [ N - n ^ { \prime } + 1 ] - E _ { m } ^ { \operatorname* { m a x } } ,\tag{38}
$$

Here, $\varphi \geq 0$ serves as the weight factor for the estimated flight 0energy. The online optimization for the given time slot $n ^ { \prime }$ can be formulated as:

$$
( \mathrm { P 1 1 } ) : \operatorname* { m a x } _ { \substack { \eta , \{ x _ { m , k } [ n ^ { \prime } ] , \mathbf { u } _ { m } [ n ^ { \prime } ] , p _ { m } [ n ^ { \prime } ] \} } } \eta - ( \lambda E _ { m } ^ { p } [ n ^ { \prime } ] ) ^ { + }
$$

$$
\mathrm { s . t . } \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ^ { \prime } ] R _ { m , k } [ n ^ { \prime } ] \geq \eta , \forall m ,\tag{39}
$$

$$
x _ { m , k } [ n ^ { \prime } ] \in \{ 0 , 1 \} , \forall m , k ,\tag{40}
$$

$$
\sum _ { m = 1 } ^ { M } x _ { m , k } [ n ^ { \prime } ] \leq 1 , \forall k , \sum _ { k = 1 } ^ { K } x _ { m , k } [ n ^ { \prime } ] \leq 1 , \forall m ,\tag{41}
$$

$$
0 \leq p _ { m } [ n ^ { \prime } ] \leq P _ { m } ^ { \operatorname* { m a x } } , \forall m ,\tag{42}
$$

$$
\Omega _ { n ^ { \prime } - 1 } + E _ { m } ^ { c } [ n ^ { \prime } ] + \hat { E } _ { m } ^ { f } [ N - n ^ { \prime } + 1 ] \leq E _ { m } ^ { \operatorname* { m a x } } , \forall m ,\tag{43}
$$

$$
\| \mathbf { v } _ { m } ^ { x y } [ n ^ { \prime } ] \| \leq V _ { \operatorname* { m a x } } ^ { x y } , | v _ { m } ^ { z } [ n ^ { \prime } ] | \leq V _ { \operatorname* { m a x } } ^ { z } , \forall m ,\tag{44}
$$

$$
\| \mathbf { u } _ { m } [ n ^ { \prime } ] - \mathbf { u } _ { j } [ n ^ { \prime } ] \| \geq D _ { \operatorname* { m i n } } , \forall m \neq j ,\tag{45}
$$

where $\lambda > 0$ is the weight factor for the penalty term and $( x ) ^ { + } = \operatorname* { m a x } \{ 0 , x \}$ . Based on the definition of $E _ { m } ^ { p } [ n ^ { \prime } ]$ in (35), $\hat { E } _ { m } ^ { f } [ N - n ^ { \prime } + 1 ]$ [ ]represents the feasible energy consumption for [the UAV $u _ { m }$ + 1]to reach its final destination within the remaining time. When there is an energy deficit, the penalty term $E _ { m } ^ { p } [ n ^ { \prime } ]$ imposes an adverse effect on the objective function, which is in contradiction with the aim of problem (P11). Consequently, the UAV will modify its trajectory to manage its energy consumption. Essentially, this means that the UAVs can estimate their energy usage for the forthcoming time slots, which is facilitated by the proposed penalty term, ultimately aiding in lowering the overall flight-associated energy consumption in the mission. The proposed online control approach is summarized in Algorithm 4. In Algorithm 4, we determine the online resource allocation and trajectory optimization by solving problem (P11) for each time slot. It is worth noting that even though problem (P11) remains a mixed-integer non-convex optimization problem, its structure is similar to (P2). Hence, a similar algorithm to Algorithm 2 can be leveraged to efficiently solve (P11). The complexity of the algorithm solving (P11) can be given by ${ \cal O } ( I ( K \bar { M } ) ^ { 3 . 5 } )$ since it only focuses on a single time slot optimization with fewer design variables in comparison to Algorithm 2.

```latex
Algorithm 4: Online Control Algorithm Without CDI.
1: Initialize solution set $\Lambda _ { m } = \varnothing , \forall m ;$
2: for $n ^ { \prime } = 1$ to $N$ do
=3: Obtain $\Omega _ { n ^ { \prime } - 1 }$ based on $\Lambda _ { m } ;$
4: Obtain $\hat { E } _ { m } ^ { f } [ N - n ^ { \prime } + 1 ]$ Îwith Algorithm 3 by letting
${ \bf u } _ { m , 0 } = { \bf u } _ { m } [ n ^ { \prime } - 1 ]$ + 1]and $\tilde { T } _ { m } = \bar { ( N - n ^ { \prime } + 1 ) } \delta .$
u 0 = u [ 1] = (5: Perform CSI measurement to obtain
$( G _ { m , k } [ n ^ { \prime } ] , c _ { m , k } [ n ^ { \prime } ] , \tilde { h } _ { m , k } [ n ^ { \prime } ] ) ;$
( [6: Obtain $\{ x _ { m , k } [ n ^ { \prime } ] , \mathbf { u } _ { m } [ n ^ { \prime } ] , p _ { m } [ n ^ { \prime } ] \}$ and $\{ R _ { m , k } [ n ^ { \prime } ] \}$ by
[ ] u [ ] [ ] [solving problem (P11) with similar algorithm as
Algorithm $2 ;$
7: for each $\mathrm { U A V } ~ u _ { m }$ do
8: The UAV $u _ { m }$ transmits to ${ \mathrm { B S ~ } } s _ { k }$ with $x _ { m , k } [ n ^ { \prime } ] = 1$
by setting transmit power as $p _ { m } [ n ^ { \prime } ]$ [ ] = 1and flies towards
location $\mathbf { u } _ { m } [ n ^ { \prime } ] ;$
9: end for
10: Update $\begin{array} { r } { \Lambda _ { m } = \Lambda _ { m } \bigcup \{ x _ { m , k } [ n ^ { \prime } ] , \mathbf { u } _ { m } [ n ^ { \prime } ] , p _ { m } [ n ^ { \prime } ] , } \end{array}$
$R _ { m , k } [ n ^ { \prime } ] \} ;$
[11: end for
```

It is worthwhile to note that the optimization process is conducted at the BSs, where both UAVs and BSs play pivotal roles in acquiring and updating the real time CSI. The processed CSI information is then used by the BSs to run the optimization algorithms, which involve calculating the optimal transmit power and issuing necessary control commands to the UAVs. In practice, the BSs can be equipped with powerful computational resources, enabling them to perform these complex calculations swiftly, ensuring that the solutions are implemented aligning with the dynamic nature of aerial communication environments.

## VI. SIMULATION RESULTS

In this section, we present a thorough simulation study to evaluate the uplink throughput performance of our proposed online optimization techniques. We emphasize the joint design of resource allocation and 3D path planning both with and without CDI. The simulations focus on an urban subregion defined by $[ 0 , 2 ] \times [ 0 , 2 ] \times [ 0 , 0 . 2 ]$ (in km). Local building dis-[0 2] [0 2] [0 0 2]tribution for this subregion is derived from one realization of the ITU statistical model [13], [37]. The parameters for this model align with those detailed in Section II-A. It is worth noting that the building distribution remains constant throughout the simulation, reflecting practical conditions. In our setup, we continuously monitor UAV locations at each time slot to categorize the $\mathrm { L o S / N L o S }$ links. This categorization is based on potential blockages between UAVs and BSs. Our scenario includes $M = 2$ cellular-connected UAVs and $K = 7$ BSs uniformly = 2 = 7spread within the considered region, as depicted in Fig. 2. Both the initial and final UAV locations follow the configurations in Fig. 2. Each BS has a fixed altitude of $H _ { G } = 2 5$ m, and all UAVs = 25share the same energy budget and maximum transmit power, i.e., $E _ { m } ^ { \mathrm { m a x } } = \bar { E } ^ { \mathrm { m a x } } , P _ { m } ^ { \mathrm { m a x } } = \bar { P } ^ { \mathrm { m a x } }$ , âm. The energy consumption = =parameters for rotary-wing UAVs are set as follows: $G = 2 0$ $d _ { 0 } = 0 . 6 , U _ { t i p } = 1 2 0 , A = 0 . 5 0 3 , \tilde { \rho } = 1 . 2 2 5 , s = 0 . 0 5 , v _ { 0 } =$ $\mathrm { 1 . 0 3 , ~ } P _ { 0 } = 7 9 . 8 5 6 3 , ~ P _ { i } = 8 8 . 5 2 7 9 ~ [ 3 0 $ 1 225 = 0 05 0 =]. For the probabilistic

<!-- image-->  
(a) 2D trajectory.

<!-- image-->  
(b) 3D trajectory.  
Fig. 2. Optimized 2D and 3D trajectories.

<!-- image-->  
Fig. 3. Convergence behavior of Algorithm 2.

LoS model: $C = 1 0 , D = 0 . 6 , \kappa = 0 . 2$ . The antenna param-= 10 = 0 6 = 0 2eters are taken from [40], [41] and are set as $H P B W _ { v } = 6 5 ^ { \circ }$ $\theta _ { D } = 1 0 ^ { \circ } , G _ { m } = 3 0 { \mathrm { d B } } , N _ { 0 } = 8 .$ . The Rician factor, $K _ { c } ,$ = 65 is con-= 10figured at $K _ { c } = 1 0$ 0 0 = 8dB. For the EPM method, we set $\rho ^ { 0 } = 0 . 1$ ï¼ $c = \sqrt { 1 0 } , \rho _ { \mathrm { m a x } } = 5$ = 0 1as in [51]. Unless otherwise stated, other important parameters are set as: $H _ { \mathrm { m i n } } = 1 0 0 \mathrm { m } , H _ { \mathrm { m a x } } = 2 0 0 \mathrm { m }$ $D _ { \operatorname* { m i n } } = 1 0 \mathrm { m } , \sigma ^ { 2 } = - 1 1 0 \mathrm { d B } \mathrm { m } , \beta _ { 0 } = - 6 0 \mathrm { d } \mathrm { B } , \alpha = 2 . 2 , B = 1$ minMHz, $\delta _ { t } = 1 \mathrm { s } , V _ { \mathrm { m a x } } ^ { x y } = 5 0 \mathrm { m } / \mathrm { s } , V _ { \mathrm { m a x } } ^ { z } = 2 0 \mathrm { m } / \mathrm { s } , \lambda = 1 , \varphi = 4$ $\bar { P } ^ { \operatorname* { m a x } } = 1 \mathrm { W } , \bar { E } ^ { \operatorname* { m a x } } = 2 0 0$ mKJoule, $T = 6 0 ~ \mathrm { s }$

## A. Optimized Solution With Offline and Online Designs

Without loss of generality, we give the convergence behavior for Algorithm 2 with $n ^ { \prime } = 1$ in Fig. 3. It is observed that the curve converges within just over ten iterations, which confirms the analysis in Section IV-B. Fig. 2 illustrates the optimized trajectories using our proposed online schemes in comparison with the offline design scheme, which only employs the statistical CDI for optimization as in [30]. For the offline design scheme, it becomes evident that each UAV navigates towards its destination while also trying to get closer to the BSs. The reason is that, in the offline design, optimization exclusively relies on statistical channel information. Consequently, aspects like building blockage and antenna patterns are averaged with a consistent value throughout the UAVsâ flight. As such, the distance from the UAV to the BS emerges as the principal determinant in the A2G channel. As a result, UAVs tend to move close to BSs to attain optimal channel quality for data uploading, which is also verified in Fig. 4(a). Fig. 4 shows the optimized transmission scheduling and power control across different schemes. From Fig. 2(a), the binary solutions for transmission scheduling are obtained through the iterative Algorithm 2 using the EPM approach. Specifically, the penalty term is designed to heavily penalize any deviation from binary values, effectively pushing the solution towards the binary domain as the penalty parameter is progressively increased. Fig. 4(b) further highlights how the two UAVs can mitigate interference by adjusting their transmit power, especially while move close to each other for sending data to BSs. In particular, one UAV might diminish its transmit power to circumvent intense interference. By employing such strategy, we maintain strong direct links and decrease co-channel interference to increase the overall throughput.

<!-- image-->  
(a) Transmission scheduling.

<!-- image-->

<!-- image-->

<!-- image-->  
(b) Power control  
Fig. 4. Optimized transmission scheduling and power control.

For the depicted online design schemes in Fig. 2, their trajectories differ from the offline design. Such difference arises because the online designs can swiftly adjust based on the location-dependent A2G CSI in real-time. This adaptability is crucial in ensuring optimal performance at each point during their flight paths. Notably, in the online design with CDI, UAV $u _ { 1 }$ avoids approaching BS $s _ { 4 }$ too closely, unlike the offline 1 4scheme. The reason is that the performance can be degraded near BS $s _ { 4 }$ due to the obstructions from buildings and antenna 4pattern. In this case, the two UAVs mostly transmit at their peak power to enhance spectral efficiency. Given that they largely remain at a considerable distance from each other, the trajectory design efficiently mitigates both direct channel and co-channel interference.

<!-- image-->  
Fig. 5. The tradeoff between flight energy consumption and flight time.

For the online design without CDI, the initial segment of the optimized trajectory mirrors that of the online design with CDI. However, differences emerge towards the latter segment. Such difference can be attributed to the designâs reliance only on the CSI information of the current time slot. Consequently, it first seeks to maximize throughput by ignoring the energy constraints and later becomes energy-conscious, particularly while navigating to the endpoint. As the two UAVs approach each other, the power control strategy takes effect. It is observed from Fig. 4(a) that UAVs may bypass the closest BS since the actual A2G quality is influenced not only by distance but also by factors like building obstructions and antenna patterns. The binary decision for transmission scheduling is obtained effectively from the proposed EPM method. Furthermore, Fig. 2(b) reveals that UAVs sometimes ascend, even when it requires more energy. Such actions arise from the benefits of achieving robust direct links and mitigating co-channel interference, enhanced by factors like building obstructions, antenna configurations, and small scale fading. Thus, a integrated strategy involving power control and 3D trajectory planning offers more flexibility in reducing interference and improving throughput. It is worthwhile to note that the online design without CDI introduces an energy-triggered penalty term, which ensures UAVs possess adequate energy reserves to reach their destination. In particular, the estimated flight energy for this purpose is derived by solving (P10) from any selected starting point. The energy consumption for UAV u with design variable T , is depicted in Fig. 5 by letting ${ \bf u } _ { 1 } ^ { 0 } = { \bf u } _ { 1 } ^ { I }$ . A noticeable trend is emerging that energy u1 = u1consumption initially reduces but increases as flight time $\tilde { T }$ increases. Such trend illustrates the balance between reduced flight time and increased proportional power with given specific start and end points, where such balance point can be efficient determined by the proposed Algorithm 3.

<!-- image-->  
Fig. 6. The proportion of time saved by our online designs relative to offline design.

To validate the computational overhead associated with our proposed online designs, we assess the running time of the schemes in a computational environment powered by an Intel Core i5-6700, 3.40 GHz processor with 16 GB of RAM, employing Matlab R2022a with CVX. The relative computational efficiency of our online designs, as depicted in Fig. 6, is further highlighted when compared to traditional offline design scheme. Specifically, the figure shows the proportion of time saved by our online designs relative to offline design, demonstrating substantial improvements in time efficiency. The average running time for the online design without CDI was only a few hundred milliseconds (462 ms), which is less than the slot duration $\delta _ { t } .$ . This aligns well within practical time constraints and demonstrates a significant reduction compared to offline methods. Additionally, as UAVs near their destinations, the computation time for CDIassisted design decreases, due to the reduction in optimization parameters, which verifies the detailed analysis discussed in Sections IV and V. To further enhance computational efficiency, we note the potential of employing advanced optimization tools such as CVXGEN [55], capable of reducing computation times by up to 1000 times compared to standard CVX-based implementations, and thus the running time can be reduced to the order of a millisecond for the online schemes, which is practically affordable. Coupled with the high computational capabilities typically available at BSs, these enhancements make our online designs a viable and effective solution for practical UAV network operations.

## B. Performance Comparisons

To the best of our knowledge, no current methods specifically address the same problem in cellular-connected networks. For comparative purposes, we introduce three baseline schemes with the state-of-the-art approaches: 1)Offline design benchmark: This scheme employs an offline optimization for resource allocation and 3D UAV trajectory, which relies on a homogeneous approximation approach as in [20], [30]; 2) Online straight-line flight benchmark: In this strategy, UAVs directly traverse to their destinations in a straight line. At every time slot, an online design for transmission scheduling and power allocation is executed as in [34]; 3) Online interference ignorance benchmark: This approach involves each UAV executing an online joint design of 3D trajectory and resource allocation to maximize its throughput without considering the co-channel interference from other UAVs as in [54]; 4) Online design with only CDI benchmark: In this strategy, only CDI information is available and the UAVs perform online joint design to maximize its throughput at each time slot with only CDI information.

<!-- image-->  
(a) Minimum throughput for UAVs versus the UAVs' energy budget.

<!-- image-->  
(b) Minimum throughput for UAVs versus the time horizon.  
Fig. 7. Performance comparisons of proposed designs.

Fig. 7(a) illustrates the minimum throughput of all UAVs across different schemes versus the energy budget $\bar { E } _ { \mathrm { m a x } }$ when $T = 6 0 \ { \mathrm { s } } .$ max. It is observed that the throughput increases as $\bar { E } _ { \mathrm { m a x } }$ increases, and our proposed online algorithms consistently outperforms the baseline schemes. The superior performance can be attributed to the enhanced flexibility that a larger UAV energy budget offers, permitting the UAVs to selectively fly or even hover over locations with superior A2G communication quality. The performance gap between online and offline design schemes shows the advantages of real-time adjustments based on current UAV locations during flights. Moreover, the distinction between our proposed Algorithms 1 and 3 suggests that incorporating CDI information into online optimization can further optimize performance. Even though CDI does not offer explicit location-aware channel information, it delivers valuable heuristic insights from a statistical view, especially beneficial when optimizing with UAV energy constraints. By comparing the performance of the online straight-line flight benchmark with our proposed algorithms, the benefits of UAVsâ 3D mobility are identified. Similarly, when comparing our approaches with the online interference ignorance benchmark, the advantage of an interference-aware power control and trajectory design is illustrated. Fig. 7(b) displays the minimum throughput of all UAVs across the different schemes as the time horizon $T$ varies when $\bar { E } _ { \operatorname* { m a x } } = 1 0 0$ KJoule. It is observed that as T max = 100increases, all schemes experience an increase in throughput, and the performance gap becomes more noticeable. This trend signifies the growing importance of joint optimization for both enhancing direct links and minimizing co-channel interference as $T$ increases. Conversely, constraining UAVs to a straightline trajectory limits their potential. Embracing UAV mobility alongside power control provides more design freedom for UAV trajectories, leading to more throughput enhancement. By comparing the proposed online design with Algorithm 4 with the benchmark of online design with only CDI, the importance of CSI measurement at each time slot is evaluated. In addition, the performance gain between the online design with Algorithm 1 and online design with Algorithm 4 is brought by the strategic incorporation of prior CDI knowledge for supplementary guidance.

## VII. CONCLUSION

In this paper, we developed an online optimization framework for cellular-connected multi-UAV communications. The objective was to maximize the minimum uplink throughput for the UAVs, taking into consideration their energy budget constraints and the co-channel interference between them. Utilizing the instantaneous CSI obtained during the UAVsâ flights, we propose two online design schemes, one with CDI information and another without. For these schemes, we adopted the exact penalty method for sequential convex optimization and the energy-triggered penalty for online control, respectively. Simulation results validate the effectiveness of our proposed algorithms, showing a significant throughput improvement compared with baseline schemes. Our results also reveal the key factors impacting the system, particularly the relevance of interference-aware power control and 3D path planning for UAVs.

## REFERENCES

[1] A. A. Khuwaja, Y. Chen, N. Zhao, M.-S. Alouini, and P. Dobbins, âA survey of channel modeling for UAV communications,â IEEE Commun. Surv. Tut., vol. 20, no. 4, pp. 2804â2821, Fourth Quarter 2018.

[2] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[3] S. Hu, W. Ni, X. Wang, A. Jamalipour, and D. Ta, âJoint optimization of trajectory propulsion and thrust powers for covert UAV-on-UAV video tracking and surveillance,â IEEE Trans. Inf. Forensics Secur., vol. 16, pp. 1959â1972, 2021.

[4] Y. Zeng, J. Lyu, and R. Zhang, âCellular-connected UAV: Potential, challenges, and promising technologies,â IEEE Wireless Commun., vol. 26, no. 1, pp. 120â127, Feb. 2019.

[5] W. Mei, Q. Wu, and R. Zhang, âCellular-connected UAV: Uplink association, power control and interference coordination,â IEEE Trans. Wireless Commun., vol. 18, no. 11, pp. 5380â5393, Nov. 2019.

[6] S. Zhang, Y. Zeng, and R. Zhang, âCellular-enabled UAV communication: A connectivity-constrained trajectory optimization perspective,â IEEE Trans. Commun., vol. 67, no. 3, pp. 2580â2604, Mar. 2019.

[7] K. Gao, H. Wang, H. Lv, and P. Gao, âA DL-based high-precision positioning method in challenging urban scenarios for B5G CCUAVs,â IEEE J. Select. Areas Commun., vol. 41, no. 6, pp. 1670â1687, Jun. 2023.

[8] M. Chen, W. Saad, and C. Yin, âEcho-liquid state deep learning for 360â¦ content transmission and caching in wireless VR networks with cellularconnected UAVs,â IEEE Trans. Commun., vol. 67, no. 9, pp. 6386â6400, Sep. 2019.

[9] S. Hu, X. Yuan, W. Ni, and X. Wang, âTrajectory planning of cellularconnected UAV for communication-assisted radar sensing,â IEEE Trans. Commun., vol. 70, no. 9, pp. 6385â6396, Sep. 2022.

[10] B. Chang, W. Tang, X. Yan, X. Tong, and Z. Chen, âIntegrated scheduling of sensing, communication, and control for mmWave/THz communications in cellular connected UAV networks,â IEEE J. Select. Areas Commun., vol. 40, no. 7, pp. 2103â2113, Jul. 2022.

[11] N. Senadhira, S. Durrani, X. Zhou, N. Yang, and M. Ding, âUplink NOMA for cellular-connected UAV: Impact of UAV trajectories and altitude,â IEEE Trans. Commun., vol. 68, no. 8, pp. 5242â5258, Aug. 2020.

[12] X. Pang et al., âUplink precoding optimization for NOMA cellularconnected UAV networks,â IEEE Trans. Commun., vol. 68, no. 2, pp. 1271â1283, Feb. 2020.

[13] Y. Zeng, X. Xu, S. Jin, and R. Zhang, âSimultaneous navigation and radio mapping for cellular-connected UAV with deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 20, no. 7, pp. 4205â4220, Jul. 2021.

[14] C. Zhan and Y. Zeng, âEnergy minimization for cellular-connected UAV: From optimization to deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5541â5555, Jul. 2022.

[15] M. Mozaffari, X. Lin, and S. Hayes, âTowards 6G with connected sky: UAVs and beyond,â IEEE Commun. Mag., vol. 59, no. 12, pp. 74â80, Dec. 2021.

[16] X. Cai, I. Z. KovÃ¡cs, J. Wigard, R. Amorim, F. Tufvesson, and P. E. Mogensen, âPower allocation for uplink communications of massive cellular-connected UAVs,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 8797â8811, Jul. 2023.

[17] J. Hou, Y. Deng, and M. Shikh-Bahaei, âJoint beamforming, user association, and height control for cellular-enabled UAV communications,â IEEE Trans. Commun., vol. 69, no. 6, pp. 3598â3613, Jun. 2021.

[18] X. Liu, Y. Deng, and T. Mahmoodi, âWireless distributed learning: A new hybrid split and federated learning approach,â IEEE Trans. Wireless Commun., vol. 22, no. 4, pp. 2650â2665, Apr. 2023.

[19] Y. Han, L. Liu, L. Duan, and R. Zhang, âTowards reliable UAV swarm communication in D2D-enhanced cellular networks,â IEEE Trans. Wireless Commun., vol. 20, no. 3, pp. 1567â1581, Mar. 2021.

[20] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âCellular-connected Multi-UAV MEC networks: An online stochastic optimization approach,â IEEE Trans. Wireless Commun., vol. 70, no. 10, pp. 6630â6647, Oct. 2022.

[21] W. K. New, C. Y. Leow, K. Navaie, Y. Sun, and Z. Ding, âInterferenceaware NOMA for cellular-connected UAVs: Stochastic geometry analysis,â IEEE J. Select. Areas Commun., vol. 39, no. 10, pp. 3067â3080, Oct. 2021.

[22] W. Mei and R. Zhang, âCooperative downlink interference transmission and cancellation for cellular-connected UAV: A divide-and-conquer approach,â IEEE Trans. Commun., vol. 68, no. 2, pp. 1297â1311, Feb. 2020.

[23] U. Challita, W. Saad, and C. Bettstetter, âInterference management for cellular-connected UAVs: A deep reinforcement learning approach,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2125â2140, Apr. 2019.

[24] M. Z. Hassan, G. Kaddoum, and O. Akhrif, âResource allocation for joint interference management and security enhancement in cellular-connected internet-of-drones networks,â IEEE Trans. Veh. Technol., vol. 71, no. 12, pp. 12869â12884, Dec. 2022.

[25] W. Mei and R. Zhang, âAerial-ground interference mitigation for cellularconnected UAV,â IEEE Wireless Commun., vol. 28, no. 1, pp. 167â173, Feb. 2021.

[26] Y. Sun, D. Xu, D. W. K. Ng, L. Dai, and R. Schober, âOptimal 3Dtrajectory design and resource allocation for solar-powered UAV communication systems,â IEEE Trans. Commun., vol. 67, no. 6, pp. 4281â4298, Jun. 2019.

[27] M. Hua, L. Yang, C. Li, Q. Wu, and A. L. Swindlehurst, âThroughput maximization for UAV-aided backscatter communication networks,â IEEE Trans. Commun., vol. 68, no. 2, pp. 1254â1270, Feb. 2020.

[28] S. Hu, Q. Wu, and X. Wang, âEnergy management and trajectory optimization for UAV-enabled legitimate monitoring systems,â IEEE Trans. Wireless Commun., vol. 20, no. 1, pp. 142â155, Jan. 2021.

[29] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for multi-UAV enabled wireless networks,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2109â2121, Mar. 2018.

[30] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[31] M. Hua, L. Yang, Q. Wu, C. Pan, C. Li, and A. L. Swindlehurst, âUAVassisted intelligent reflecting surface symbiotic radio system,â IEEE Trans. Wireless Commun., vol. 20, no. 9, pp. 5769â5785, Sep. 2021.

[32] R. Amer, W. Saad, and N. Marchetti, âMobility in the sky: Performance and mobility analysis for cellular-connected UAVs,â IEEE Trans. Commun., vol. 68, no. 5, pp. 3229â3246, May 2020.

[33] M. M. Azari, F. Rosas, and S. Pollin, âCellular connectivity for UAVs: Network modeling, performance analysis, and design guidelines,â IEEE Trans. Wireless Commun., vol. 18, no. 7, pp. 3366â3381, Jul. 2019.

[34] C. You and R. Zhang, âHybrid offline-online design for UAV-enabled data harvesting in probabilistic LoS channel,â IEEE Trans. Wireless Commun., vol. 19, no. 6, pp. 3753â3768, Jun. 2020.

[35] M. Samir, C. Assi, S. Sharafeddine, and A. Ghrayeb, âOnline altitude control and scheduling policy for minimizing AoI in UAV-assisted IoT wireless networks,â IEEE Trans. Mobile Comput., vol. 21, no. 7, pp. 2493â2505, Jul. 2022.

[36] Y. Li and A. H. Aghvami, âRadio resource management for cellularconnected UAV: A learning approach,â IEEE Trans. Commun., vol. 71, no. 5, pp. 2784â2800, May 2023.

[37] âPropagation data and prediction methods required for the design of terrestrial broadband radio access systems operating in a frequency range from 3 to 60 GHz,â document recommendation ITU-R P.1410. Accessed: Feb. 18, 2019. [Online]. Available: https://www.itu.int/rec/R-REC-P.1410/en

[38] R. Karmakar, G. Kaddoum, and O. Akhrif, âA novel federated learningbased smart power and 3D trajectory control for fairness optimization in secure UAV-assisted MEC services,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 4832â4848, May 2024.

[39] X. Dai, B. Duo, X. Yuan, and M. Di Renzo, âEnergy-efficient UAV communications in the presence of wind: 3D modeling and trajectory design,â IEEE Trans. Wireless Commun., vol. 23, no. 3, pp. 1840â1854, Mar. 2024.

[40] G. T. 36.777, âTechnical specification group radio access network; study on enhanced LTE support for aerial vehicles,â 5G Americas, Tech. Rep. TR 36.777, Dec. 2017.

[41] X. Xu and Y. Zeng, âCellular-connected UAV: Performance analysis with 3D antenna modelling,â in Proc. IEEE Int. Conf. Commun. Workshops, 2019, pp. 1â6.

[42] M. M. Azari, G. Geraci, A. Garcia-Rodriguez, and S. Pollin, âUAV-to-UAV communications in cellular networks,â IEEE Trans. Wireless Commun., vol. 19, no. 9, pp. 6130â6144, Sep. 2020.

[43] A. Fotouhi et al., âSurvey on UAV cellular communications: Practical aspects, standardization advancements, regulation, and security challenges,â IEEE Commun. Surv. Tut., vol. 21, no. 4, pp. 3417â3442, Fourth Quarter 2019.

[44] K. Li, W. Ni, X. Wang, R. P. Liu, S. S. Kanhere, and S. Jha, âEnergyefficient cooperative relaying for unmanned aerial vehicles,â IEEE Trans. Mobile Comput., vol. 15, no. 6, pp. 1377â1386, Jun. 2016.

[45] A. Filippone, Flight Performance of Fixed and Rotary Wing Aircraft. Amsterdam, The Netherlands: Elsevier, 2006.

[46] C. Zhan and Y. Zeng, âAerialâground cost tradeoff for multi-UAV-enabled data collection in wireless sensor networks,â IEEE Trans. Commun., vol. 68, no. 3, pp. 1937â1950, Mar. 2020.

[47] H. Pan, Y. Liu, G. Sun, J. Fan, S. Liang, and C. Yuen, âJoint power and 3D trajectory optimization for UAV-enabled wireless powered communication networks with obstacles,â IEEE Trans. Commun., vol. 71, no. 4, pp. 2364â2380, Apr. 2023.

[48] C. Sun, X. Xiong, Z. Zhai, W. Ni, T. Ohtsuki, and X. Wang, âMax-min fair 3D trajectory design and transmission scheduling for solar-powered fixed-wing UAV-assisted data collection,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8650â8665, Dec. 2023.

[49] M. Hua, L. Yang, Q. Wu, and A. L. Swindlehurst, â3D UAV trajectory and communication design for simultaneous uplink and downlink transmission,â IEEE Trans. Commun., vol. 68, no. 9, pp. 5908â5923, Sep. 2020.

[50] J. -H. Lee, K. -H. Park, Y. -C. Ko, and M. -S. Alouini, âThroughput maximization of mixed FSO/RF UAV-aided mobile relaying with a buffer,â IEEE Trans. Wireless Commun., vol. 20, no. 1, pp. 683â694, Jan. 2021.

[51] G. Yuan and B. Ghanem, âAn exact penalty method for binary optimization based on MPEC formulation,â in Proc. 31st AAAI Conf. Artif. Intell., 2017, pp. 2867â2875.

[52] M. Grant and S. Boyd, âCVX: MATLAB software for disciplined convex programming,â 2016. [Online] Available: http://cvxr.com/cvx

[53] Y. Liu, K. Xiong, Y. Lu, Q. Ni, P. Fan, and K. B. Letaief, âUAV-aided wireless power transfer and data collection in Rician fading,â IEEE J. Select. Areas Commun., vol. 39, no. 10, pp. 3097â3113, Oct. 2021.

[54] C. Zhan and Y. Zeng, âEnergy-efficient data uploading for cellularconnected UAV systems,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7279â7292, Nov. 2020.

[55] J. Mattingley and S. Boyd, âCVXGEN: A code generator for embedded convex optimization,â Optim. Eng., vol. 13, no. 1, pp. 1â27, Mar. 2012.

<!-- image-->

Cheng Zhan (Member, IEEE) received the BEng and PhD degrees in computer science from the School of Computer Science, University of Science and Technology of China, Anhui, China, in 2006 and 2011, respectively. From 2009 to 2010, he was a research assistant with the Department of Computer Science, City University of Hong Kong. From 2016 to 2017, he was a visiting scholar with the Department of Electrical and Computer Engineering, National University of Singapore. He is currently a professor with the School of Computer and Information Science, South-

west University, China. His research interests include unmanned aerial vehicle communications, multimedia communications, wireless sensor networks, and network coding. He served as a TPC member for the IEEE ICC, GLOBECOM, WCNC, and UIC.

<!-- image-->

Han Hu (Member, IEEE) received the BE and PhD degrees from the University of Science and Technology of China, China, in 2007 and 2012, respectively. He is currently a professor with the School of Information and Electronics, Beijing Institute of Technology, China. His research interests include multimedia networking, edge intelligence and space-air-ground integrated network. He received several academic awards, including Best Paper Award of IEEE TCSVT 2019, Best Paper Award of IEEE Multimedia Magazine 2015, Best Paper Award of IEEE Globecom

2013, etc. He served as an associate editor of IEEE Transactions on Multimedia and Ad Hoc Networks, and a TPC member of Infocom, ACM MM, AAAI, IJCAI, etc.

<!-- image-->

Zhi Liu (Senior Member, IEEE) received the BE degree from the University of Science and Technology of China, China, and the PhD degree in informatics from the National Institute of Informatics. He is currently an associate professor with The University of Electro-Communications, Japan. His research interest includes video network transmission, vehicular networks and mobile edge computing. He was a recipient of the IEEE StreamComm 2011 Best Student Paper Award, the 2015 IEICE Young Researcher Award, and the ICOIN 2018 Best Paper Award. He is now an editorial board member of Wireless Networks (Springer) and IEEE Open Journal of the Computer Society.

<!-- image-->

Jing Wang (Member, IEEE) received the PhD degree from Peking University, in 2011. She is currently an associate professor with the School of Information, Renmin University of China. Her research interests include edge intelligence and data analytics, computer system for artificial intelligence, and energy-efficient computing. She received Beijing Nova Award, she has published papers on top computer conferences, such as MICRO, ISCA, HPCA, and IEEE/ACM Transactions journals. She received the Best Paper Award of ICCD, Featured paper of

IEEE Transactions on Computer, etc. She served as a TPC member of ISCA, NAS, and ASDB.

<!-- image-->  
and statistical signal process.

Rongfei Fan (Member, IEEE) received the BE degree in communication engineering from the Harbin Institute of Technology, Harbin, China, in 2007, and the PhD degree in electrical engineering from the University of Alberta, Edmonton, AB, Canada, in 2012. Since 2013, he has been a faculty member with the Beijing Institute of Technology, Beijing, China, where he is currently an associate professor with the School of Cyberspace Science and Technology. His research interests include edge computing, federated learning, resource allocation in wireless networks,

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons/page_16_img_1.jpeg|page_16_img_1]]
2. [[../extracted_images/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons/page_16_img_2.jpeg|page_16_img_2]]
3. [[../extracted_images/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons/page_16_img_3.jpeg|page_16_img_3]]
4. [[../extracted_images/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons/page_17_img_1.jpeg|page_17_img_1]]
5. [[../extracted_images/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons/page_17_img_2.jpeg|page_17_img_2]]

---

