# Reliable and Energy-Efficient UAV Communications: A Cost-Aware Perspective

Farzad H. Panahi and Fereidoun H. Panahi

AbstractâUnmanned aerial vehicles (UAVs) are expected to play an important role in future wireless networks, serving as communication relays, computing servers, and flying infrastructure for ground users when ground-based infrastructure is congested or inaccessible. However, typical UAVs are powered by on-board batteries, which results in limited battery lifetime and poses a major restriction for UAV applications in communications. To overcome this, we propose a consistent and cost-aware energy procurement framework for a UAV powered concurrently by laser beams, emitted from locally deployed laser beam directors, and local renewable energy (RE) sources. The UAV intends to lower its overall energy cost for a certain operation cycle by optimizing the quantities of energy obtained from its battery as well as laser beams at each time period. Given the optimization results, we also propose a cost-aware UAV placement strategy with the ultimate goal of ensuring quality communication-energy links for the UAV, ground devices (GDs) and users. In addition, we assess the amount of additional procured RE that can be transferred via wireless power transfer to charge a set of distributed GDs. The simulations provide interesting insights into the efficiency of the proposed framework.

Index TermsâUnmanned aerial vehicle, renewable energy, green wireless communications, cellular network, low-power IoT devices.

## I. INTRODUCTION

R ECENTLY, owing to practical uses in communicationnetworks such as unmanned aerial vehicle (UAV)-assisted networks such as unmanned aerial vehicle (UAV)-assisted ubiquitous coverage, UAV-assisted information dissemination and data collecting [1], [2], [3], [4], [5], [6], research on UAV has received more and more interest. In particular, the use of UAV has been perceived in hotspot [7], [8], [9], [10], [11] as a viable strategy to solve the issue of traffic congestion. However, due to the restricted on-board energy resources, the practicality and dependability of UAV-enabled applications confront several critical hurdles, particularly for long-duration missions [12], [13], [14]. Unfortunately, most commercially available UAVs struggle to remain aloft for longer than 30 minutes. As a result, the UAV is always required to terminate its mission in order to recharge or replace its battery. To address this technological difficulty, numerous studies aimed at optimizing the use of the onboard energy by expanding the battery capacity [15], and optimizing the UAV trajectory [16] and placement [17]. These approaches can enhance the efficiency of the on-board energy consumption, but they cannot greatly extend the UAV flight duration, which is necessary for many UAV-enabled applications. Laser beaming is a new approach for extending mission time [12], [18], [19], [20]. This technology has demonstrated the possibility to provide significantly longer UAV flight durations, and is now being used by several companies [21]. More intriguingly, the laser beam might be utilized for both energy harvesting (EH) and information transmission. The use of renewable energy (RE) as a different alternative for powering UAVs has been researched in the literature [22], [23], [24].

This paper proposes a consistent and cost-aware energy procurement approach for a UAV powered concurrently by laser beams, emitted from locally deployed laser beam directors (LBDs), and local RE sources. Indeed, we are concerned with the energy procurement of a communication UAV that is fueled concurrently by power grid connected LBDs and RE sources, with the end goal of minimizing the energy procurement cost.

## A. Related Work

Most studies looking into UAV-related problems, such as 3D trajectory optimization and resource allocation, concentrated on the energy perspective of average or instantaneous power consumed/harvested when flying, hovering, processing data, or communicating, without taking into consideration the initial available energy and energy procurement costs. The energy efficiency (EE) of UAV-based wireless communications has been the subject of several works in the existing literature. Using tools from optimal transport theory, [25] addresses minimizing the transmit power of UAVs, serving ground users, while meeting the transmission rate requirements of these users. In [26], an energy-efficient UAV deployment strategy for collecting data from internet-of-things (IoT) devices in uplink is explored. In [27], an optimum deployment mechanism for UAV base stations (BSs) is suggested, with the goal of maximizing the network EE and coverage to a terrestrial BS. To achieve energy-efficient communication, the authors in [28] presented a coverage model based on a multi-UAV system. A generalized propulsion energy consumption model for rotary-wing UAVs is proposed by the authors in [29] while taking into account the practical thrust-to-weight ratio with regard to the UAVsâ velocities, accelerations, and changes in direction. Their aim is to maximize the EE of the UAV by jointly optimizing the user scheduling and UAV trajectory variables. Ref. [16] studies an energy-efficient UAV communication with a ground terminal via optimizing the UAVâs trajectory, a novel design paradigm that takes both the communication throughput and the UAVâs energy consumption into account. An overview of power control in ultra dense networks (UDNs) assisted by UAVs is given in [30]. Ref. [31] discusses a multi-UAV enabled IoT in which the UAVs function as BSs and provide data to terrestrial IoT nodes during flight. To ensure equitable energy consumption of the UAVs, a fair energy-efficient resource optimization approach for the IoT has been proposed, which seeks to maximize each UAVâs minimum EE by concurrently optimizing communication scheduling, power allocations, and UAVs trajectories. In [32], a multi-UAV enabled mobile Internet of Vehicles (IoVs) model is described, in which the UAVs track to serve the mobile vehicles and transmit downlink information to the vehicles during flight. Considering the constraints of anti-collision and communication interference between the UAVs, the system throughput is maximized by concurrently optimizing vehicle communication scheduling, UAV power allocation, and UAV trajectory.

UAVs will also play a crucial role in future wireless networks as computing servers. In [33], a UAV is employed to assist an access point in offering mobile edge computing (MEC) services to ground users in an energy-efficient way. Minimizing the energy consumption and time for UAV applications in a UAV-enabled MEC system is investigated in [34]. Ref. [35] studies the energy reduction problem in UAV-enhanced IoT networks through task offloading decisions and UAV trajectory design. In [36], the authors investigated the problem of minimizing the total required energy of a UAV by jointly optimizing the CPU frequencies, offloading amount, transmit power, and UAV trajectory in a UAV-enabled wireless powered cooperative MEC system. In [37], an innovative UAV-enabled MEC system was proposed, with the goal of minimizing the weighted sum of the service delay of all IoT devices and UAV energy consumption by concurrently optimizing UAV position, communication and computing resource allocation, and task splitting decisions. Ref. [38] studies the EE maximization problem of a UAV in a UAV-enabled MEC system while providing computation offloading services. A novel UAV-mounted reconfigurable intelligent surface (RIS) (U-RIS) assisted MEC system is considered in [39], in which a U-RIS is deployed to aid the communication between the ground users and an MEC server. To maximize the systemâs EE, the joint UAV trajectory, RIS passive beamforming, and MEC resource allocation design is developed. In [40], the problem of maximizing the residual energy of maritime search and rescue UAVs based on MEC is studied. The research objective is formalized as a residual energy maximization problem by optimizing communication and time resources concurrently. Although all of these papers and many more investigated methods to lower the energy consumption of UAV-enabled MEC systems, none of them considered the UAVâs energy procurement cost or service pricing.

Many other studies have looked at the advantages of EH for UAV-assisted wireless communications, e.g., [41], [42], [43]. These studies looked at EH through radio frequency sources rather than RE sources. The authors of [44] explored optimizing the total throughput for a solar-powered UAV system during a particular time period. Ref. [45] proposed an energy management system for cellular heterogeneous networks (HetNets) supported by dynamic solar-powered UAVs, which conserved energy and enhanced network capacity by optimizing the placement of BSs and the trajectory of solar-powered UAVs. In [46], the authors develop a framework for energy management in UAV-assisted HetNets, in which the UAVs can harvest solar energy as well as charge their batteries at fixed charging stations. Some statistical models for solar and wind EH are developed in [47], and they may be used to evaluate the performance of aerial wireless communication systems as well as integrated terrestrial-aerial communications systems employing EH. In order to accomplish the targeted mission with high performance and high efficiency, an energy management system is required to efficiently control the power splitting between the onboard power sources.

## B. Contributions

UAVs generally utilize a hybrid energy supply system architecture which may combine several energy sources to enhance longevity and achieve better performance. Therefore, it is essential to choose an appropriate energy source hybridization architecture with an optimal energy procurement system to ensure the efficient operation of modern UAVs. Although all the studies looking into UAV-related problems concentrated on the energy perspective of average or instantaneous power consumed/harvested when flying, hovering, processing data, or communicating, none of them considered the UAVâs energy procurement costs, nor did they consider determining the optimal amount of energies to be procured by the UAV from each energy source. Thus, the main contributions of the paper are summarized as follows:

We determine the optimal amount of energies to be procured by the UAV from each energy source, namely; laser beams emitted from the ground-based LBDs, and the UAVâs internal battery power procured from the RE sources. Furthermore, in the event that there is an excess of RE generation, we aim to quantify the extra RE that is used to wirelessly charge a number of distributed lowpower ground devices (GDs) (IoT nodes) using the wireless power transfer (WPT) technology in order to compensate for the cost of the energy procurement. In other words, the UAV can offset its energy expenses by selling energy to the GDs via WPT. The proposed energy procurement approach takes into account a time-varying scenario in that the procurement at a particular time period is dependent on the RE generation as well as the UAVâs battery power usage up to that time period. Toward this end, we formulate an optimization problem aiming to minimize the UAVâs energy procurement cost C. We particularly aim to minimize the cost of energy procurement at the UAV during an operation cycle divided into T time intervals of duration Ï . In fact, C represents the cost associated with the energy exchange with the LBDs and GDs, and it may be either positive or negative depending on the amount of energies to be received (from the LBDs) or provided (to the GDs).

<!-- image-->  
Fig. 1. System model: a cellular network consisting of a UAV, a ground base station (GBS), user equipments (UEs), low-power IoT ground devices (GDs), and locally deployed laser beam directors (LBDs).

- The efficient deployment of UAV is a key solution for seamless connectivity and reliable coverage, allowing for a trade-off between energy and wireless coverage. Given the optimization results of the UAVâs energy procurement cost, we propose a cost-aware UAV placement strategy by defining three different regions, namely the âsafe cellular regionâ, âsafe optical region,â and âsafe charging region,â with the ultimate goal of ensuring quality communicationenergy links between the ground BS (GBS)-UAV, LBDs-UAV, and GDs-UAV, respectively.

## II. SYSTEM MODEL

The wireless backhaul infrastructure for our system model can be a cellular network composed of several GBSs distributed spatially using a Poisson Point Process (PPP) $\Phi _ { G B S }$ with density of $\lambda _ { G B S }$ Î¦. However, in this paper, we focus on a single cell setting with a GBS, a UAV, randomly distributed user equipments (UEs), low-power IoT GDs, and LBDs as illustrated in Fig. 1. The UAV is intended to offer wireless coverage to the UEs. Note that, in this study, we concentrate on a downlink scenario. The UAV is therefore regarded as a transmitter while communicating to its serving UEs. The LBDs, which are placed on the ground and distributed spatially using a PPP $\Phi _ { L }$ with density $\lambda _ { L }$ Î¦, provide power to the UAV. Each LBD transmits energy with the same, constant level of power $p _ { \mathrm { L } }$ , and, at each time instant, the UAV is powered by its nearest LBD. As seen in Fig. 1, we assume that the UAV flies at a height $H _ { U }$ It is assuemed that if the UAV is placed above a predefined altitude, denoted as $H _ { U , \operatorname* { m i n } } ,$ the Line-of-sight (LoS) links can be established between the UAV and the LBDs/GDs/UEs, i.e., $H _ { U , \operatorname* { m i n } } \leq H _ { U } \leq H _ { U , \operatorname* { m a x } }$ , where $H _ { U , \operatorname* { m a x } }$ denotes the maximum altitude the UAV can fly. Without loss of generality, we will concentrate on a typical UAV that is placed at $( X _ { U } , Y _ { U } , H _ { U } )$ ï¼ while the serving LBD is located at $( X _ { L } , Y _ { L } , 0 )$ . As a result,

<!-- image-->  
Fig. 2. Illustration of the energy procurement framework for a UAV powered concurrently by its nearest LBD and wind energy as an RE source. The UAV has an internal battery to store the energy procured from the RE source.

$R _ { L } = \sqrt { d _ { L } ^ { 2 } + H _ { U } ^ { 2 } }$ represents the distance between the UAV and its serving LBD, where $d _ { L } = \sqrt { ( X _ { L } ^ { 2 } - X _ { U } ^ { 2 } ) + ( Y _ { L } ^ { 2 } - Y _ { U } ^ { 2 } ) }$ = ( ) + ( )indicates their horizontal distance. Given that a PPP is used to model the positions of the LBDs, the serving LBDâs location and, by extension, $d _ { L } ,$ , are random variables. In addition to harvesting energy from the LBDs and communicating with UEs, the UAV utilizes the WPT technology to wirelessly charge a number of GDs at predetermined places [48]. Note that a PPP $\Phi _ { G }$ with density $\lambda _ { G }$ Î¦is also used to model the positions of the GDs.

Apart from the nearest LBD, the UAV is also powered by a local RE source, in this paper wind energy, which can be a sustainable RE source. Note that a combination of different RE sources can be considered to balance out variability of production of one resource type [49], [50]. We aim to minimize the energy procurement cost at the UAV for an operation cycle divided into T time intervals of duration Ï . We denote the energy procured from a LBD to power the UAV during the time period $\kappa \in \{ 1 , \ldots , T \}$ by $e _ { \kappa } ^ { L }$ (see Figs. 1 and 2, and Table I). The corre-1sponding unit price at the Îº-th time period is represented by $\rho _ { \kappa } ^ { L }$ This pricing might change over the operation cycle depending on the strategy followed by the LBDs. We assume that the available energy from a LBD is not stored in the UAVâs battery but is used immediately upon the UAVâs energy request. This cost-aware strategy is implemented so that the energy gained from the RE source (which is free) is prioritized for storage (in the UAVâs battery) and utilization rather than the obtained energy from the LBD. Moreover, as stated earlier, the UAV has its own internal retailer, i.e., the RE generator, which generates an amount of energy at each time period Îº, denoted by $e _ { \kappa } ^ { R } .$ , which is supposed to be cost-free. The energy obtained from the RE source will be stored in the UAVâs internal battery (see Fig. 2). We assume that the UAVâs internal battery has a maximum storage capacity $B _ { U }$ As seen, the amount of energy procured by the UAV at the Îº-th time period from its own internal battery is represented by $e _ { \kappa } ^ { B }$ . To compensate for the cost of energy procurement at the UAV, we also consider that the UAV has the ability to wirelessly charge some GDs by the amount of energy $e _ { \kappa } ^ { W }$ at each time period Îº at a given price $\rho _ { \kappa } ^ { W }$ (where $\rho ^ { L } > \bar { \rho ^ { W } } )$ . In other words, the UAV can offset its energy expenses by selling energy to the GDs via WPT.

TABLE I MAJOR MATHEMATICAL NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>UAV&#x27;s energy procurement cost</td><td rowspan=1 colspan=1> $\overline { { B _ { U } } }$ </td><td rowspan=1 colspan=1>Maximum storage capacity of the UAV&#x27;sbattery</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>Number of time intervals in an operation cycle</td><td rowspan=1 colspan=1> $\overline { { B _ { L } } }$ </td><td rowspan=1 colspan=1>Minimum allowable stored energy in the UAV&#x27;s battery</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>Duration of each time interval</td><td rowspan=1 colspan=1> $\overline { { e _ { \kappa } ^ { W } } }$ </td><td rowspan=1 colspan=1>Amount of energy to charge the GDs at time period K</td></tr><tr><td rowspan=1 colspan=1> $\lambda _ { L }$ </td><td rowspan=1 colspan=1>Density of LBDs</td><td rowspan=1 colspan=1> $\smash { \overline { { \rho _ { \varepsilon } ^ { W } } } }$ </td><td rowspan=1 colspan=1>Unit price of charging the GDs at time period K</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \lambda _ { G } } }$ </td><td rowspan=1 colspan=1>Density of GDs</td><td rowspan=1 colspan=1> $\frac { \prime \prime } { e }$  $\underline { { e } } _ { \kappa } ^ { \cup }$ </td><td rowspan=1 colspan=1>UAV&#x27;s energy consumption at time period K</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \lambda _ { U E } } }$ </td><td rowspan=1 colspan=1>Density of UEs</td><td rowspan=1 colspan=1> $\overline { { F _ { U } } }$ </td><td rowspan=1 colspan=1>UAV&#x27;s directional antenna gain</td></tr><tr><td rowspan=1 colspan=1> $\lambda _ { G B S }$ </td><td rowspan=1 colspan=1>Density of GBSs</td><td rowspan=1 colspan=1> $\overline { { \beta _ { 0 } } }$ </td><td rowspan=1 colspan=1>Reference channel gainbetween theUAVandUEs</td></tr><tr><td rowspan=1 colspan=1> $e _ { \kappa } ^ { L }$ </td><td rowspan=1 colspan=1>Energy procured from a LBD during the time period K</td><td rowspan=1 colspan=1> $\underline { { p _ { L } } }$ </td><td rowspan=1 colspan=1>LBDs&#x27;transmit power</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \rho _ { \kappa } ^ { L } } }$ </td><td rowspan=1 colspan=1>Unit price of procuring energy from a LBD at time period K</td><td rowspan=1 colspan=1> $\underline { { \mu _ { L } } }$ </td><td rowspan=1 colspan=1>Efficiency of energy harvestingat the UAV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \delta _ { s } } }$ </td><td rowspan=1 colspan=1>Laser power ratio at the UAV</td><td rowspan=1 colspan=1> $\vartheta _ { L }$ </td><td rowspan=1 colspan=1>Medium&#x27;sattenuation coefficient</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D } }$ </td><td rowspan=1 colspan=1>Initial laser beam size</td><td rowspan=1 colspan=1> $A _ { L }$ </td><td rowspan=1 colspan=1>Receiver telescope&#x27;s or collection lens&#x27;sarea</td></tr><tr><td rowspan=1 colspan=1> $\varrho$ </td><td rowspan=1 colspan=1>Optical efficiency of the combined transmitter receiver</td><td rowspan=1 colspan=1> $\overline { { \Delta \theta } }$ </td><td rowspan=1 colspan=1>Angular spread of the laser beam</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { G } } }$ </td><td rowspan=1 colspan=1>Direct distance between the UAV and a typical GD</td><td rowspan=1 colspan=1> $\overline { { R _ { G } ^ { c } } }$ </td><td rowspan=1 colspan=1>Critical charging radius</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { L } } }$ </td><td rowspan=1 colspan=1>Direct distance betweenthe UAVand atypical LBD</td><td rowspan=1 colspan=1> $\overline { { R _ { L } ^ { c } } }$ </td><td rowspan=1 colspan=1>Critical optical radius</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { G B S } } }$ </td><td rowspan=1 colspan=1>Direct distance between the UAV and GBS</td><td rowspan=1 colspan=1> $\underline { { R _ { G B S } ^ { c } } }$ </td><td rowspan=1 colspan=1>Critical cellular radius</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \mathcal { P } _ { U , \operatorname* { m a x } } } }$ </td><td rowspan=1 colspan=1>Maximum UAV transmit power to serve the UEs inside its coverage</td><td rowspan=1 colspan=1> $\underline { { p _ { \mathrm { p r o p } } } }$ </td><td rowspan=1 colspan=1>Propulsion power consumption of the UAV</td></tr><tr><td rowspan=1 colspan=1> $\underline { { p _ { \mathrm { c o m m } } } }$ </td><td rowspan=1 colspan=1>UAV&#x27;s communication-related power consumption</td><td rowspan=1 colspan=1> $\overline { { e _ { \kappa } ^ { R } } }$  $\underline { { e } } _ { \kappa } ^ { \pi }$ </td><td rowspan=1 colspan=1>Generated REof theUAV&#x27;s internal retailerat time period Îº</td></tr><tr><td rowspan=1 colspan=1> $e ^ { t }$ </td><td rowspan=1 colspan=1>UAV&#x27;s propulsion-related energy consumption</td><td rowspan=1 colspan=1> $\overline { { e ^ { C } } }$ </td><td rowspan=1 colspan=1>UAV&#x27;scommunication-related energy consumption</td></tr><tr><td rowspan=1 colspan=1> $_ v$ </td><td rowspan=1 colspan=1>UAV&#x27;s flyingspeed</td><td rowspan=1 colspan=1> $\overline { { V _ { w } } }$ </td><td rowspan=1 colspan=1>Speed of wind</td></tr><tr><td rowspan=1 colspan=1> $\overline { { H _ { U } } }$ </td><td rowspan=1 colspan=1>UAV&#x27;s flying height</td><td rowspan=1 colspan=1> $\chi$ </td><td rowspan=1 colspan=1>Additional degradation parameter for the NLoS propagation</td></tr><tr><td rowspan=1 colspan=1> ${ \underline { { P _ { L } } } }$ </td><td rowspan=1 colspan=1>Total received power at the UAV from a LBD</td><td rowspan=1 colspan=1> $\overline { { e ^ { G } } }$ </td><td rowspan=1 colspan=1>Amount of energy harvested by a typical GD</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \eta _ { G } } }$ </td><td rowspan=1 colspan=1>Energy harvesting efficiencyata GD</td><td rowspan=1 colspan=1> $\overline { { h _ { t } } }$ </td><td rowspan=1 colspan=1>Optical turbulence effect variable</td></tr><tr><td rowspan=1 colspan=1> $\mu _ { R }$ </td><td rowspan=1 colspan=1>Averageamount of energyprocured from theRE source</td><td rowspan=1 colspan=1> $\overline { { L _ { U } } }$ </td><td rowspan=1 colspan=1>UAV&#x27;s locationvector</td></tr></table>

The energy consumption of the UAV at time period Îº is also denoted by $\mathbf { \bar { \rho } } _ { e _ { \kappa } } U$ (see Fig. 2), which comprises the propulsion, communication and on-board processing energies. In fact, the energies $e _ { \kappa } ^ { B }$ and $e _ { \kappa } ^ { L }$ are used together to fulfill the UAVâs energy consumption at each time period $( e _ { \kappa } ^ { U } ) , \mathrm { i } . e . , e _ { \kappa } ^ { B } + e _ { \kappa } ^ { L } = e _ { \kappa } ^ { U }$ , âÎº â $\{ 1 , \ldots , T \}$ + =(see Fig. 2). We will see later that in order to min-1imize the energy procurement costs while meeting the UAVâs energy consumption $e ^ { U }$ , the energies $e ^ { L }$ and $e ^ { W }$ cannot take values at the same time. In other words, the UAV cannot sell energy to the GDs while still harvesting energy from the nearest LBD. Finally, the energy procurement decisions are centrally managed using an energy control unit (ECU) by gathering all necessary data from the UAV and LBDs, as illustrated in Fig. 1. More specifically, the ECU determines the quantity of energy to be acquired by the UAV from each energy source throughout the course of the whole operation cycle after obtaining the necessary information from various actors, such as the LBD energy price plan, RE information, and the UAV energy consumption.

## A. Communication Model

In this work, the cellular cellâs whole available bandwidth is split into a set of orthogonal channels CH $\{ c h _ { 1 } , c h _ { 2 } , \ldots , c h _ { | \mathrm { C H } | } \}$ =, where |.| indicates the cardinality of set. We assume that any channel $c h _ { j } \in { \bf C H } \left( j \in \{ 1 , 2 , \dots , | { \bf C H } | \} \right)$ ( 1 2 )has a constant bandwidth w (effective bandwidth). Accordingly, $| \mathrm { C H } | . w = W$ , where W is the total available bandwidth in Hz. These orthogonal channels are randomly allocated to the GBS and UAV in such a way that $| \mathrm { C H } _ { G B S } | + | \mathrm { C H } _ { U } | = | \mathrm { C H } |$ , where $| \mathrm { C H } _ { G B S } |$ and $| \mathrm { C H } _ { U } |$ + =denote the number of allocated channels to the GBS and UAV, respectively. The total available bandwidth is divided into two portions, namely $W _ { G B S } = ( 1 - \rho ) W$ and $W _ { U } = \rho W$ = (1 ), which are used by the GBS and UAV, respectively. =The ground coverage region of the UAV can be approximated as a disk area of radius $r _ { C }$ centered at the UAVâs projection on the ground, as illustrated in Fig. 1. Furthermore, each UE i served either by the GBS or UAV is assigned an effective bandwidth w. If the UAV serves UE i, the instantaneous achievable rate for UE i is expressed as [11]

$$
R _ { U , i } = w \log _ { 2 } \left( 1 + \frac { F _ { U } \overline { { h \left( d _ { i } \right) } } P _ { U , i } } { w N _ { 0 } } \right)\tag{1}
$$

where $P _ { U , i }$ is the UAV transmit power allocated to UE i. We assume equal power allocation. The horizontal distance between the UAV and UE i is represented by $d _ { i }$ , and $N _ { 0 }$ is the noise power spectrum density. Furthermore, a directional antenna with gain $F _ { U }$ on the UAV is used to suppress the UAV interference in the GBS-user network, limiting the UAV communications to a circle area on the ground. Also, $\overline { { h ( d _ { i } ) } }$ is the average or expected ( )channel power gain between the UAV and i-th UE located at a horizontal distance $d _ { i } ,$ and is expressed as follows [51]

$$
\overline { { h \left( d _ { i } \right) } } \triangleq \mathbb { E } \left[ h \left( d _ { i } \right) \right] = \frac { \beta _ { 0 } P _ { \mathrm { L o S } } } { \left( H _ { U } ^ { 2 } + d _ { i } ^ { 2 } \right) ^ { \frac { \alpha _ { L } } { 2 } } } + \frac { \chi \beta _ { 0 } P _ { \mathrm { N L o S } } } { \left( H _ { U } ^ { 2 } + d _ { i } ^ { 2 } \right) ^ { \frac { \alpha _ { N } } { 2 } } } ,\tag{2}
$$

where $\beta _ { 0 }$ signifies the reference channel gain, $\alpha _ { L }$ and $\alpha _ { N }$ are respectively the LoS and NLoS path loss exponents, and $\chi < 1$ 1is the additional degradation parameter accounting for the NLoS propagation. The probability of establishing a LoS link between the UAV and i-th UE, indicated as $P _ { \mathrm { L o S } } ,$ is generally modeled as a logistic function of the elevation angle, which is computed statistically based on geometric parameters of the surroundings such as the number and height of buildings [8], [51]:

$$
P _ { \mathrm { L o S } } = ( 1 + b \exp ( - c ( \theta - b ) ) ) ^ { - 1 } ,\tag{3}
$$

where b as well as c are environment-related constants, and $\theta =$ $\textstyle { \frac { 1 8 0 } { \pi } } \tan ^ { - 1 } \left( { \frac { H _ { U } } { d _ { i } } } \right)$ =is the elevation angle as the UAV is seen from tan ( )the UE. On the other hand, the probability of NLoS links is consequently $P _ { \mathrm { N L o S } } = 1 - P _ { \mathrm { L o S } }$

If $R _ { U , i } \ge R _ { t h }$ holds for any i, from (1), and assuming that $\alpha _ { L } = \alpha _ { N } = \alpha$ , the maximum UAV transmit power to serve the = =UEs inside its coverage area of radius $r _ { C }$ can be derived as follows

$$
P _ { U , \mathrm { m a x } } \geq \frac { w N _ { 0 } \left( H _ { U , \mathrm { m a x } } ^ { 2 } + r _ { C } ^ { 2 } \right) ^ { \frac { \alpha } { 2 } } } { F _ { U } \beta _ { 0 } \left( \chi + ( 1 - \chi ) P _ { \mathrm { L o S } } \right) } \left( 2 ^ { \frac { R _ { t h } } { w } } - 1 \right) ,\tag{4}
$$

where $R _ { t h }$ is the minimum acceptable data rate of UEs.

## B. FSO Model

The widely used free-space optics (FSO) range equation can be utilized to determine the EH through the laser connection. Under the assumption of a linear EH model with an efficiency of $\mu _ { L }$ , the laser energy procured at the UAV over a time period of duration Ï when serving by a LBD at a horizontal distance of $d _ { L }$ is represented by [12], [18], [52]:

$$
e ^ { L } = ( 1 - \delta _ { s } ) \tau P _ { L } ,\tag{5}
$$

where $( 1 - \delta _ { s } )$ is the portion of the receiving power that is (1 )allocated to EH (Î´s is the power splitting factor), and $P _ { L }$ , i.e., the total received power at the UAV, is given as follows,

$$
P _ { L } = \frac { h _ { t } \mu _ { L } A _ { L } p _ { \mathrm { L } } \varrho \exp ( - \vartheta _ { L } R _ { L } ) } { \left( D + R _ { L } \Delta \theta \right) ^ { 2 } } ,\tag{6}
$$

where $R _ { L } = \sqrt { d _ { L } ^ { 2 } + H _ { U } ^ { 2 } }$ is the direct distance between the UAV and LBD, $h _ { t }$ +denotes a log-normal random variable accounting for the optical turbulence effect, the receiver telescopeâs or collection lensâs area is denoted by the symbol $A _ { L } , D$ is the initial laser beam size, and the mediumâs attenuation coefficient is represented by $\vartheta _ { L }$ . The optical efficiency of the combined transmitter receiver is $\varrho ,$ and the angular spread of the laser beam is denoted by $\Delta \theta$ . Note that (6) is derived from the Beer-Lambert equation. It accounts for the scattering effect and the divergence of the laser beam as it propagates through the atmosphere [12].

For the UAV-LBD communication link, we assume that information transfer is performed via On-Off keying modulation (OOK). As a result, the signal-to-noise ratio (SNR) level at the UAV is given by [12]:

$$
\gamma _ { L } = \frac { \delta _ { s } \eta _ { L } P _ { L } } { 2 h \nu \Delta f }\tag{7}
$$

where h is Planckâs constant, $\eta _ { L }$ is the photodiode responsivity, Î½ is the photonâs frequency, and $\Delta f$ is the modulation frequency bandwidth.

## C. WPT Model

As mentioned, at a given price, the UAV has the ability to wirelessly charge a random number of under coverage GDs by the amount of energy $e _ { \kappa } ^ { W }$ at each time period Îº (with a charging duration of Ï ) (see Fig. 2). Indeed, in this model, the same RF signals transmitted by the UAV can be harvested for energy by multiple GDs at the same time. Let $d _ { G } ( t )$ denotes the horizontal ( )distance of a typical GD form the UAV at time $t \in [ 0 , \tau ]$ . Since [0 ]the GDs are powered by the UAV, they operate as long as they intercept enough power. The received power at a typical GD, i.e., $P _ { G }$ , at a distance ${ \bf \bar { \cal R } } _ { G } = \sqrt { d _ { G } ^ { 2 } ( t ) + H _ { U } ^ { 2 } }$ when the UAV transmits with power $P _ { W } = e ^ { W } / \tau$ can be given by Friis Transmission Equation as [53]

<!-- image-->  
Fig. 3. Distance of the UAV-enabled WPT from the nearest GD, as well as the energy received through WPT at the nearest GD for charging it, as a function of the IoT GDsâ density.

$$
P _ { G } = P _ { W } \frac { G _ { T } G _ { R } \lambda ^ { 2 } } { ( 4 \pi ) ^ { 2 } R _ { G } ^ { \alpha _ { p } } } ,\tag{8}
$$

where $G _ { T }$ and $G _ { R }$ are respectively the antenna gain of the UAV and the GD, Î» is the RF signal wavelength, and $p \in \{ L :$ :, N  NLoS}. We can assume that the GDs are in LoS of LoS :the UAV, and there is no shadowing. By taking into account the sensitivity of rectenna, i.e., the minimum (threshold) power $P _ { t h }$ required for its activation, the most accurate EH model to describe the harvested power at a GD can be given by the following piecewise linear function [54]

$$
\begin{array} { r } { P _ { G } ^ { H } ( P _ { G } ) \triangleq \left\{ \begin{array} { l l } { 0 , } & { P _ { G } \in [ 0 , P _ { t h } ) , } \\ { \eta _ { G } \left( P _ { G } \right) \cdot P _ { G } , } & { P _ { G } \in [ P _ { t h } , P _ { s a t } ) , } \\ { P _ { G } ^ { H } \left( P _ { s a t } \right) , } & { P _ { G } \geq P _ { s a t } , } \end{array} \right. } \end{array}\tag{9}
$$

which is non-decreasing and continuous for all $P _ { G } \in \mathbb { R }$ . Indeed, $P _ { G } ^ { H }$ is the conversion of $P _ { G }$ into usable direct current (DC) power. By using curve-fitting tools for any empirical dataset, the function $\eta _ { G } ( \cdot )$ can be simply expressed as a polynomial, ( )yielding a mathematically tractable expression with adequate precision. In our paper, the rectennas are assumed to function in the ideal region (i.e., $P _ { G } \in [ P _ { t h } , P _ { s a t } ) )$ for all GDs with a con-[ )stant harvesting efficiency Î·G. Note that $P _ { s a t }$ is the harvesterâs saturation power threshold.

In Fig. 3, we can see that the distance between the UAVenabled WPT and the nearest GD decreases as the density of the GDs increases, hence the typical GD under consideration will generally receive more energy for charging through WPT as it is closer to the UAV.

## D. UAV Power Consumption Model

The propulsion power $p _ { \mathrm { p r o p } }$ communication-related power pcomm, and on-board processing power $p _ { \mathrm { c o n s t } }$ all contribute to the UAVâs power consumption. The instantaneous propulsion power consumed by a fixed-wing UAV is described by the following

equation [12], [16]:

$$
p _ { \mathrm { p r o p } } = \neq \left| c _ { 1 } \| \mathbf { v } \| ^ { 3 } + \frac { c _ { 2 } } { \| \mathbf { v } \| } \left( 1 + \frac { \| \mathbf { a } \| ^ { 2 } - \frac { \left( \mathbf { a } ^ { T } \mathbf { v } \right) ^ { 2 } } { \mathbf { v } ^ { 2 } } } { g ^ { 2 } } \right) + m \mathbf { a } ^ { T } \mathbf { v } \right| ,\tag{10}
$$

where v and a respectively are the UAV instantaneous velocity and acceleration vectors, m denotes the UAVâs mass, and two parameters, $c _ { 1 }$ and $c _ { 2 } .$ , are used to characterize the aircraftâs weight, wing area, and air density. Also, $g = 9 . 8 \mathrm { \tilde { ~ } m / s ^ { 2 } }$ is the gravitational acceleration of the earth. For a vector a, a denotes its euclidean norm, and $\mathbf { a } ^ { T }$ represents its transpose. For steady straight-and-level flight [16] with constant speed v, we have $\| \mathbf { v } ( t ) \| = v$ and $\left\| \mathbf { a } \right\| = \mathbf { 0 }$ . Thus, (10) reduces to

$$
p _ { \mathrm { p r o p } } = \left( c _ { 1 } v ^ { 3 } + { \frac { c _ { 2 } } { v } } \right) .\tag{11}
$$

## III. PROBLEM FORMULATIONS

Based on the above explanations, the UAVâs cumulative energy procurement cost at each time period Îº is formulated as follows:

$$
C _ { \kappa } = \sum _ { i = 1 } ^ { \kappa } \left( \rho _ { i } ^ { L } e _ { i } ^ { L } - \rho _ { i } ^ { W } e _ { i } ^ { W } \right) , ~ \kappa \in \{ 1 , \ldots , T \} .\tag{12}
$$

The goal is to minimize the cost of energy procurement at the UAV for an operation cycle divided into $T$ time intervals of duration Ï . Indeed, C, which reflects the cost of the UAVâs energy exchange with the LBDs and GDs, can be either positive or negative depending on the quantity of energy received (from the LBDs) or provided (to the GDs). The minimization of C should be conducted while keeping the following constraints in mind: (i) The ECU should comply with the UAVâs energy consumption constraint at each time period Îº (14). (ii) For the UAV and time period $\kappa ,$ the sum of the quantities of energy procured from the internal battery $( e ^ { B } )$ and transferred to the GDs $( e ^ { W } )$ up to the time period Îº cannot exceed the generated RE of the internal retailer up to the Îº-th time period (the left inequality of (15), with $B _ { L }$ denoting the minimum allowable stored energy in the UAVâs battery). (iii) Finally, for the internal battery, the quantity of stored energy should not be greater than the capacity $B _ { U }$ (the right inequality of (15)). In summary, the minimization problem can be represented as follows:

$$
( \mathrm { P } ) \operatorname* { m i n } _ { \{ e _ { \kappa } ^ { W } , e _ { \kappa } ^ { B } , e _ { \kappa } ^ { L } \} } C _ { \kappa }\tag{13}
$$

$$
\mathrm { s . t . } e _ { \kappa } ^ { B } + e _ { \kappa } ^ { L } = e _ { \kappa } ^ { U } , \forall \kappa\tag{14}
$$

$$
{ { B } _ { L } } \le \sum _ { i = 1 } ^ { \kappa } { { { e } _ { i } ^ { R } } } - \sum _ { i = 1 } ^ { \kappa } { \left( { { e } _ { i } ^ { B } } + { { e } _ { i } ^ { W } } \right) } \le { { B } _ { U } } , { \forall \kappa }\tag{15}
$$

$$
e _ { \kappa } ^ { B } , e _ { \kappa } ^ { W } , e _ { \kappa } ^ { L } \geq 0 , \forall \kappa\tag{16}
$$

where the UAVâs energy consumption at time period Îº of duration Ï is represented by $e _ { \kappa } ^ { U }$ , and is given as

$$
e _ { \kappa } ^ { U } = \left( p _ { \mathrm { c o m m } } + p _ { \mathrm { p r o p } } + p _ { \mathrm { c o n s t } } \right) \tau ,\tag{17}
$$

<!-- image-->  
Fig. 4. Safe cellular, optical, and charging regions with the critical radii $R _ { G B S } ^ { c } , R _ { L } ^ { c }$ , and $R _ { G } ^ { c }$ , respectively.

where $p _ { \mathrm { c o m m } } = \lambda _ { U E , \kappa } \mathcal { A } S _ { c } P _ { U , \mathrm { m a x } }$ is the UAVâs communication-=related power consumption. $\lambda _ { U E , \kappa }$ is the density of the UEs during the Îº-th time period, $S _ { c } = \pi r _ { C } ^ { 2 }$ denotes the UAVâs coverage area, $P _ { U , \mathrm { { m a x } } }$ =is given in (4), and the average association probability of a typical UE with the UAV is given by A. The above-mentioned minimization problem can be easily addressed using linear programming algorithms [55]. More specifically, we use YALMIP [56], a toolbox for modeling and optimization in MATLAB, to solve the above optimization. The authors in [56] illustrate how straightforward it is to model complex optimization problems using YALMIP. Nevertheless, (P) is a linear optimization problem over $e _ { \kappa } ^ { W }$ and $e _ { \kappa } ^ { L }$ , and can be solved optimally, as shown in the following proposition.

Proposition 1: The optimal cost $C _ { \kappa } ^ { * }$ to  is

$$
C _ { \kappa } ^ { * } = \rho ^ { \Omega } \left( B _ { L } - \Delta E _ { \kappa } \right) + C _ { \kappa - 1 } , \Omega \in \{ W , L \} ,\tag{18}
$$

where $C _ { 0 } = 0$ and $\begin{array} { r } { \Delta E _ { \kappa } = \sum _ { i = 1 } ^ { \kappa } e _ { i } ^ { R } - \sum _ { i = 1 } ^ { \kappa - 1 } ( e _ { i } ^ { B } + e _ { i } ^ { W } ) - } \end{array}$ $e _ { \kappa } ^ { U }$

Proof: With some mathematical simplifications on the constraints in (14) and (15), (P) can be solved only under the following constraint:

$$
B _ { L } - \Delta E _ { \kappa } \leq e _ { \kappa } ^ { L } - e _ { \kappa } ^ { W } \leq B _ { U } - \Delta E _ { \kappa } ,\tag{19}
$$

where $e _ { \kappa } ^ { B } , e _ { \kappa } ^ { W } , e _ { \kappa } ^ { L } \geq 0$ , âÎº and $B _ { U } \gg \Delta E _ { \kappa }$ . Thus, given the 0 Îlinearity of (P) and the sign of the above lower bound, the optimal variables can be simply obtained as $\{ e _ { \kappa } ^ { B ^ { * } } = e _ { \kappa } ^ { U } , e _ { \kappa } ^ { W ^ { * } } = \stackrel { . } { \Delta } E _ { \kappa } - \nonumber$ $B _ { L } , e _ { \kappa } ^ { L ^ { * } } = 0 \}$ for $B _ { L } \le \Delta E _ { \kappa }$ . Moreover, when $B _ { L } > \Delta E _ { \kappa } ,$ we have $\begin{array} { r } { \{ e _ { \kappa } ^ { B ^ { * } } = e _ { \kappa } ^ { U } - B _ { L } + \Delta E _ { \kappa } , e _ { \kappa } ^ { W ^ { * } } = 0 , e _ { \kappa } ^ { L ^ { * } } = B _ { L } - \Delta E _ { \kappa } \} } \end{array}$ = + Î = 0 =Hence, using the optimal energy values, we obtain $C _ { \kappa } ^ { * }$ given in (18).

## IV. UAV PLACEMENT STRATEGY

To guarantee robust backhaul connectivity between the UAV and its associated GBS, the UAV should fly within a ball of critical radius $R _ { G B S } ^ { c }$ centered around the serving GBS. This is known as the âsafe cellular regionâ (see Fig. 4). A typical LBD, on the other hand, guarantees energy-communication coverage for the UAV as long as the UAV flies within a ball centered around the LBD and of critical radius $R _ { L } ^ { c }$ . The âsafe optical regionâ is what we call this area. Furthermore, to provide an adequate EH level at a typical GD, the UAV should fly within a ball of radius $R _ { G } ^ { c }$ centered around the GD. This is referred to as the âsafe charging regionâ. Positioning the UAV above the cell area (inside the safe cellular region) can ensure an appropriate cellular backhaul link and thus good coverage for the UEs, but it cannot guarantee energy-communication coverage between the UAV and its nearest LBD or an adequate EH level at a typical GD, because the UAV is not guaranteed to be located within the safe optical or safe charging regions as well.

<!-- image-->  
Fig. 5. GBS-UAV coverage simulation. The blue and yellow points, respectively, represent the UEs connected to the GBS and UAV in an association time.

Lemma 1 (Distance to Nearest Nodes): An important quantity is the direct distance $R _ { i }$ separating the UAV from its nearest node in tier i (with density of $\lambda _ { i } )$ , where $i \in \{ G B S , L : L B D , G$ GD}. It can be shown that $R _ { i }$ : :has a cumulative distribution function (CDF) as

$$
F _ { R _ { i } } ( R ) = \mathbb { P } \left[ R _ { i } \le R \right] = 1 - e ^ { - \lambda _ { i } \pi \left( R ^ { 2 } - H _ { U } ^ { 2 } \right) } .\tag{20}
$$

Proof: See Appendix A, available online.

## A. Critical Cellular Radius

Obviously, the UAV is under cellular coverage when its SNR from its nearest GBS $( \gamma _ { G B S } )$ exceeds a predefined threshold $\gamma _ { G B S } ^ { t h }$ , and it is dropped from the network when SNR falls below this threshold. Thus, the cellular coverage probability is defined as the probability that the the received signal from the GBS at the UAV can achieve the target SNR threshold:

$$
P _ { \mathrm { c o v } } ^ { G B S } = \mathbb { P } \left( \gamma _ { G B S } > \gamma _ { G B S } ^ { t h } \right) .\tag{21}
$$

Since $\gamma _ { G B S }$ is a strictly decreasing function with respect to the direct distance between the GBS and UAV (i.e., $R _ { G B S } )$ , the cellular coverage probability, based on the Lemma 1, is

$$
P _ { \mathrm { c o v } } ^ { G B S } = \mathbb { P } \left( R _ { G B S } \leqslant R _ { G B S } ^ { c } \right) = 1 - e ^ { - \lambda _ { G B S } \pi \left( R _ { G B S } ^ { c } ^ { 2 } - H _ { U } ^ { 2 } \right) } ,\tag{22}
$$

where the critical radius $R _ { G B S } ^ { c }$ can be derived when $\gamma _ { G B S }$ is set equal to $\gamma _ { G B S } ^ { t h }$ . Nevertheless, without loss of generality, it can be assumed that $R _ { G B S } ^ { c }$ is a constant cellular coverage radius and that the UAV is always flying inside this radius.

Algorithm 1: UAV Relocation Function.   
1: $\mathbf { R E L O C A T E } ( \Phi _ { G B S } , \Phi _ { L } , \Phi _ { G } )$   
2: (Î¦ Î¦ Î¦Compute critical distances: $R _ { i } ^ { c }$   
$( i \in \{ G B S , L : L B D , G : G D \} )$   
3: : : ) Set the initial location of UAV to   
${ \vec { L } } _ { U } = [ X _ { U } , Y _ { U } , H _ { U } ] .$   
4: = [ ] Save the locations of the nearest nodes in   
$( \Phi _ { G B S } , \Phi _ { L } , \Phi _ { G } )$ as:   
5: $\vec { L } _ { i } = [ X _ { i } , Y _ { i } , H _ { i } ]$ (see Fig. 4).   
6: = [Repeat:   
7: Calculate distance vectors: $\vec { L } _ { U } ^ { i } = \vec { L } _ { U } - \vec { L } _ { i } .$   
8: $A = ( i =  { { } ^ { \circ } L ^ { \prime \prime } } )  { \operatorname { A N D } } ( v \in [  { { \mathrm { i } } ^ { \circ } } , 6 2 ] )$   
9: $B = ( i = ^ { \cdot \cdot } G ^ { \prime \prime } ) \mathrm { A N D } ( v \in ( 0 , 1 0 )$ )OR   
$v \in ( 6 2 , 1 0 0 ] ) .$   
10: $M \gets 1 .$   
11: if $\begin{array} { r } { \dot { \left( A \operatorname { O R } B \right) } : M \gets 0 . } \end{array}$   
12: $\vec { L } _ { U } \gets \vec { L } _ { U } + M * ( v \Delta t \cdot \mathrm { s i g n } ( R _ { i } ^ { c } - | \vec { L } _ { U } ^ { i } | )$   
$\cdot ( \vec { L } _ { U } ^ { i } / | \vec { L } _ { U } ^ { i } | ) ) .$   
13: Until $| \vec { L } _ { U } ^ { i } | < R _ { i } ^ { c } .$   
14: END

## B. Critical Optical Radius

As previously stated, a typical LBD can ensure energycommunication coverage for the UAV if the UAV flies inside a ball of radius $R _ { L } ^ { c }$ centered on the serving LBD (see Fig. 4). Indeed, $R _ { L } ^ { c }$ is computed in such a way that the UAVâs joint SNR and energy coverage probability (from the serving LBD) is greater than a specified threshold given by B (i.e., $\mathbb { P } ( ( 1 - \delta _ { s } ) P _ { L } \ge p _ { \mathrm { p r o p } } + p _ { \mathrm { c o m m } } + p _ { \mathrm { c o n s t } } , \gamma _ { L } \ge \gamma _ { L } ^ { t h } ) \ge$ $B ) )$ ((1 ) + + ). Nevertheless, it has been demonstrated in [12] and [57] )that the energy coverage probability dominates the joint energy and communication coverage probability, and hence the critical charging radius $R _ { L } ^ { c }$ is derived by lower bounding the energy coverage probability. Based on Lemma 1, a closed-form expression in the non-turbulent regime can be obtained as follows:

$$
R _ { L } ^ { c } = \frac { 2 } { \vartheta _ { L } } W _ { 0 } \left( \frac { \vartheta _ { L } } { 2 \Delta \theta } \sqrt { \frac { \left( 1 - \delta _ { s } \right) e ^ { \frac { \vartheta _ { L } D } { \Delta \theta } } \mu _ { L } A _ { L } \varrho p _ { L } } { p _ { \mathrm { p r o p } } + p _ { \mathrm { c o m m } } + p _ { \mathrm { c o n s t } } } } \right) - \frac { D } { \Delta \theta } ,\tag{23}
$$

where $W _ { 0 } ( . )$ represents the principal branch of the Lambert ( )W function [58]. It should be noted that optical turbulence typically has an effect on laser intensity, particularly for longrange applications. In the case of lognormal turbulence, where $h _ { t } \sim \mathrm { l o g n o r m a l } ( - 2 \sigma , 2 \sqrt { \sigma } )$ , the critical charging radius $R _ { L } ^ { c }$ lognormal( 2 2 )is calculated numerically by solving a nonlinear equation, as shown in [12].

## C. Critical Charging Radius

As mentioned, at a given price, the UAV has the ability to wirelessly charge a random number of under coverage GDs. Similar to the previous subsection, the energy coverage probability at a typical GD can be computed to derive the critical charging radius $R _ { G } ^ { c }$ . Thus, the energy coverage probability $P _ { \mathrm { c o v } } ^ { G }$ at the GD indicates the probability that the harvested power

<!-- image-->  
(a) energy consumption vs. speed

<!-- image-->  
(b) energy consumption vs. time

Fig. 6. UAVâs energy consumption as a function of the UAVâs flying speed and for an operation cycle of 1 hour.  
<!-- image-->  
(a) Optimal amount of energies for an operation cycle of 1 hour.

<!-- image-->

<!-- image-->  
(b) Optimal amount of energies vs. the UAV's flying speed.  
Fig. 7. Optimal amount of energies to be procured or transferred at each time period [Fig. 7(a)] and for each UAVâs flying speed [Fig. 7(b)] to minimize the energy procurment cost at the UAV.

where

<!-- image-->  
Fig. 8. Optimal energy transferred by the UAV to the GDs through WPT versus the UAV flying speed and average energy procured from the RE source.

$P _ { G } ^ { H }$ is larger than some threshold $\gamma _ { G } ^ { t h }$ . Since $P _ { G } ^ { H }$ is a strictly decreasing function with respect to the radius $R _ { G }$ , similarly, based on Lemma 1, we have:

$$
P _ { \mathrm { c o v } } ^ { G } = 1 - e ^ { - \lambda _ { G } \pi ( { R _ { G } ^ { c } } ^ { 2 } - H _ { U } ^ { 2 } ) } ,\tag{24}
$$

$$
R _ { G } ^ { c } = \left( P _ { W } \frac { G _ { T } G _ { R } \lambda ^ { 2 } } { ( 4 \pi ) ^ { 2 } \gamma _ { G } ^ { t h } } \right) ^ { ( 1 / \alpha _ { p } ) } ,\tag{25}
$$

in which, $p \in \{ L : \mathrm { L o S } , N : \mathrm { N L o S } \}$

: LoS :Depending on the optimization results of (13), and based on the critical radii $R _ { i } ^ { c } ~ ( i \in \{ G B S , L : L B D , G : G D \} )$ defined : :in the above subsections and shown in Fig. 4, we propose a cost-aware UAV placement algorithm (see Algorithm 1) for the independent PPP distributions $\Phi _ { i }$ with corresponding densities $\lambda _ { i } .$ Î¦ The goal is to place the UAV inside the critical radii $R _ { i } ^ { c }$ based on the optimization outcomes. As an example, as will be explained in Figs. 6(a) and 7(b), for the speeds $v \in ( 0 , 1 0 )$ or $v \in ( 6 2 , 1 0 0 ]$ , the UAVâs energy consumption $e ^ { U }$ (0 10)is higher (62 100]than the average amount of energy procured from the RE source $( \mu _ { R } )$ for the given time period, and hence the UAV needs to rely on both the internal battery and the LBDs to fulfill its energy requirements. In this situation, the UAV should travel toward the nearest LBD (using Algorithm 1) until it is within that LBDâs safe optical region of radius $R _ { L } ^ { c }$

TABLE II MAJOR SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1> $D$ </td><td rowspan=1 colspan=1>0.1m</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>9.26Ã104kg/m</td></tr><tr><td rowspan=1 colspan=1> $\Delta \theta$ </td><td rowspan=1 colspan=1> $\overline { { { 1 0 } ^ { - 4 } } }$ </td><td rowspan=1 colspan=1> $c _ { 2 }$ </td><td rowspan=1 colspan=1> $\underline { { 2 2 5 0 \mathrm { k g m } ^ { 3 } / \mathrm { s } ^ { 4 } } }$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { \vartheta _ { L } } }$ </td><td rowspan=1 colspan=1> $\overline { { { 1 0 ^ { - 2 } } { \ m } } }$ </td><td rowspan=1 colspan=1> $\underline { { \mu _ { L } A _ { L } \varrho } }$ </td><td rowspan=1 colspan=1> $\overline { { 0 . 0 0 4 \mathrm { ~ m } ^ { 2 } } }$ </td></tr><tr><td rowspan=1 colspan=1>PL</td><td rowspan=1 colspan=1> $\overline { { 1 0 \mathrm { W } } }$ </td><td rowspan=1 colspan=1> $\rho _ { \kappa } ^ { L } , \forall \kappa$ </td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \eta _ { G } } }$ </td><td rowspan=1 colspan=1>0.9</td><td rowspan=1 colspan=1> $\overline { { \rho _ { \kappa } ^ { W } , \forall \kappa } }$ </td><td rowspan=1 colspan=1>0.1</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \delta _ { s } } }$ </td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 5 } } }$ </td><td rowspan=1 colspan=1> $B _ { U }$ </td><td rowspan=1 colspan=1>100Wh</td></tr><tr><td rowspan=1 colspan=1> $p _ { \mathrm { p r o p } }$ </td><td rowspan=1 colspan=1>100W</td><td rowspan=1 colspan=1>U</td><td rowspan=1 colspan=1> $\overline { { { \mathrm { ~ 5 ~ m ~ } } / { \mathrm { ~ s ~ } } } }$ </td></tr></table>

<!-- image-->  
Fig. 9. Optimal energy procured from the UAVâs internal battery versus the UAV flying speed and average energy procured from the RE source.

## V. SIMULATION RESULTS

A service area of . km Ã . km including one GBS and a 0 5 0 5UAV serving the ground UEs is considered (see Fig. 5). Unless otherwise specified, we utilize a use and store approach, which means that the available energy from the internal retailer is used before storing it, i.e., $B _ { L } = 0$ . As mentioned, the MATLAB = 0toolbox YALMIP is used to solve the minimization problem in (13). Indeed, the energy procurement cost at the UAV is minimized for an operation cycle of 1 hour divided into $T = 6 0$ = 60time intervals of duration 1 min. Unless otherwise specified, Ëwe utilize the simulation settings as listed herein. We also focus on the wind energy for our RE generation scenario. The UAV altitude is set at $H _ { U } = 5 \mathrm { m }$ , and it flies at a constant velocity = 5mv  m/s . The UAV downlink transmit power is supposed to be $P _ { U } = 1 \mathrm { { ^ { \sim } W } }$ , and the UEsâ threshold rate requirement is set at $R _ { t h } = 5 0 0 ^ { \circ }$ W . At a particular time period, the wind speed $V _ { w }$ = 500Ëkbpsis chosen to be uniformly distributed in the range m/s, m/s . [0 20 ]We use the wind energy model explained in [59] to determine the average of $e _ { \kappa } ^ { R } .$ , and is formulated as ${ \textstyle \frac { 1 } { 2 } } \rho A V _ { w } ^ { 3 } C _ { p } \tau$ with air density Ï . $\mathrm { k g / m ^ { 3 } }$ , blade swept area $\overset {  } { A } = \overset { \cdot } { 0 } . 0 4 \pi \overset { \sim } { \mathrm { ~ m } } ^ { 2 }$ =wind speed $V _ { w } ^ { 3 }$ 225Ëkg m = 0 04 Ëmwhich varies at each time period, and conversion coefficient $C _ { p } = 0 . 9$ . Table II summarizes the other simulation settings.

In Fig. 6(a), at a given time period $\kappa ,$ we can observe the impact of varying the UAVâs flying speed (for a fixed-wing UAV) on the UAVâs energy consumption level. As seen, there exists an optimal flying speed at which the fixed-wing UAV consumes the least amount of energy $e ^ { U }$ . For speeds between $v \simeq 1 0 \mathrm { m / s }$ and $v \simeq 6 2 \mathrm { m / s } .$ , the UAVâs energy consumption $e ^ { U }$ 10m s 62m sis less than the average amount of energy procured from the RE source $( \mu _ { R } = 4 . 7 \mathrm { { W h } ) }$ for the given time period, hence the UAV will be in a position to sell the excess energy to the GDs by charging them through WPT. This will not apply if the UAVâs flying speed exceeds $v = 6 2 \mathrm { { m } / \mathrm { { s } } }$ or falls behind $v = 1 0 \mathrm { m / s }$ = 62mAs can be noticed from (17), $e ^ { U }$ = 10m sis a function of both the communication-related energy consumption (i. $\mathbf { e } . , e ^ { C } = p _ { \mathrm { c o m m } } \tau )$ and propulsion-related energy consumption $\mathrm { i . e . , } e ^ { P } = p _ { \mathrm { p r o p } } \tau )$ We can see from the closeness of the $e ^ { \dot { U } }$ and $e ^ { P }$ =curves that the communication-related energy consumption is much lower than the propulsion energy consumption and hence can be neglected. As seen in Fig. 6(b), for a fixed UAVâs flying speed, $\bar { e } ^ { U }$ and $e ^ { P }$ will remain constant for an operation cycle of 1 hour. In other words, if the UAV flies at a constant speed, its energy consumption level stays almost unchanged, assuming that the UE density remains constant throughout the operation cycle. We can see that $e ^ { R } { \mathrm { . } }$ , the energy obtained from the RE source (wind energy), fluctuates over an operation cycle as wind speed varies at each time period.

<!-- image-->  
Fig. 10. Optimal energy procured from the nearest LBD to power the UAV versus the UAV flying speed and average energy procured from the RE source.

As shown in Fig. 7(a), the optimal solution (i.e., $[ e ^ { W ^ { * } } , e ^ { B ^ { * } } , e ^ { L ^ { * } } ] )$ of the minimization of C in (13) has been obtained for each time period Îº in an operation cycle of 1 hour. For instance, at the 40th time period $( \mathrm { i } . \mathbf { e } . , \kappa = 4 0 )$ , the amount of = 40energy received (at the UAV) from its internal battery is near zero $( \mathrm { i } . \mathrm { e } . , e ^ { B ^ { * } } \simeq 0 )$ because the procured energy from the wind source has been very small (see Fig. 6(b)). In this condition, the UAV should rely on the nearest LBD to receive the required energy to continue its mission, hence $e ^ { L ^ { * } }$ will be high, and obviously the UAV cannot sell its energy to charge the GDs. When the amount of energy procured from the nearest LBD $( \mathrm { i } . \mathrm { e } . , e ^ { L ^ { * } } )$ is large, the energy procurement cost is high; however, when the amount of energy procured from the LBD is small, the energy procurement cost is near zero or even negative depending on the amount of energy the UAV transfers to the GDs $( \mathrm { i } . \mathrm { e } . , e ^ { W ^ { * } } )$ . Fig. 7(b) depicts the optimal solution $( \mathrm { i . e . , } [ e ^ { W ^ { * } } , e ^ { B ^ { * } } , e ^ { L ^ { * } } ] )$ to the minimization of C in (13) for various UAV flight speeds and for a specified time period Îº. For that time period, the average amount of energy procured from the RE source is considered, $\mathrm { i . e . , } \mu _ { R } = 4 . 7 \mathrm { W h }$ For speeds between $v \simeq 1 0 \mathrm { m / s }$ and $v \simeq 6 2 \mathrm { m / s } ,$ = 4 7 the UAV will 10m s 62m sbe in a position to sell its excess energy to the GDs (the red bars), while procuring the least amounts of energy from its internal battery (the black bars). This is because the UAVâs energy consumption $e ^ { U }$ is minimal for this range of flight speed (see Fig. 6(a)). For speeds outside of the specified range, the UAV needs to rely on both the internal battery and the LBDs to fulfill its energy requirements. Furthermore, the higher the UAV acquires energy from the LBDs, the greater the cost of energy procurement.

<!-- image-->  
(a) harvested energy from the nearest LBD in Wh.

<!-- image-->  
(b) laser EH: success map.  
Fig. 11. UAVâs harvested energy from the nearest LBD versus the LBDsâ density and for an operation cycle of 1 hour. In Fig. 11(b), the filed-in black and white rectangles represents the unsuccessful and successful UAV energy-receiving requests, respectively.

As previously stated in Fig. 7(b), the average amount of energy procured from the RE source was $\mu _ { R } = 4 . 7 \mathrm { W h }$ for the given = 4 7parameters of the wind energy model. However, if the UAV can acquire more average energy from the wind source (i.e., a higher $\mu _ { R } )$ , the UAV will be able to sell more energy (a higher $e ^ { \breve { W } ^ { \ast } } )$ to the GDs (see Fig. 8), as it can procure more energy from its internal battery (see Fig. 9). Moreover, when more energy is procured from the UAVâs internal battery to fulfill the UAVâs energy requirements, the energy obtained from the LBDs becomes smaller (see Fig. 10), and therefore the overall energy procurement cost decreases. As a result, the average amount of energy procured from the RE source has a significant influence on the optimal values of $e ^ { W ^ { \ast } } , e ^ { B ^ { \ast } }$ and $e ^ { L ^ { * } }$

In Fig. 11(a), the UAVâs harvested energy from the nearest LBD $( \mathrm { i } . \mathrm { e } . , \mathrm { } e ^ { L } )$ has been depicted as a function of the LBDsâ density $( \lambda _ { L } )$ and during an operation cycle of 1 hour. When the density of LBDs rises, the distance between the UAV and the nearest LBD reduces, increasing the amount of harvested energy at the UAV. For a small $\lambda _ { L }$ , the harvested energy level at the UAV from the nearest LBD is very low and below the UAVâs targeted levels of energy $( e ^ { L ^ { * } }$ in Fig. 7(a)), and hence most UAV requests for receiving energy from the nearest LBD will fail (see Fig. 11(b)). When $\lambda _ { L }$ is large, however, the number of successful energy-receiving requests rises due to the shorter distance between the UAV and its nearest LBD. The filled-in black and white rectangles in the figure indicate unsuccessful and successful energy-receiving requests, respectively.

<!-- image-->  
Fig. 12. UAVâs energy procurement cost $C$ versus the minimum allowable stored energy (in the UAVâs battery) and average energy procured from the RE source.

As noticed from the left inequality of (15), for the UAV and time period $\kappa ,$ the generated RE of the internal retailer up to the Îº-th time period minus the sum of the quantities of energy procured from the internal battery $( e ^ { B } )$ and transferred to the GDs $( e ^ { W } )$ up to the time period Îº should be equal or greater than the minimum allowable stored energy $( B _ { L } )$ at each time period Îº. For $B _ { L } > 0$ , the UAV is not allowed to deplete its 0whole battery at each time period. To fulfill $B _ { L }$ at each time period, the UAV should either lower the amount of energy it sells to the GDs (i.e., reduce $e ^ { W } )$ or procure less energy from its battery (i.e., procure less $e ^ { B } )$ and instead obtain more energy from the nearest LBD. Either way, the overall cost of energy procurement (i.e., C) will increase slightly depending on the values of $B _ { L }$ and $B _ { U }$ (the maximum storage capacity), as shown in Fig. 12. However, inserting a non-zero value of $B _ { L }$ will assure an initial available energy for the next time periods, which will be required when energy generation from the RE source is not significant. As seen in the figure, the greater the value of $B _ { L }$ , the higher the cost of energy procurement. Furthermore, as previously demonstrated, the smaller the value of $\mu _ { R } ,$ , the greater the cost of energy procurement.

## VI. CONCLUSIONS AND FUTURE DIRECTIONS

In this paper, we proposed a consistent and cost-aware energy procurement framework for a communication UAV powered concurrently by laser beams and local RE sources. The UAV intends to lower its overall energy cost for a given operation cycle by optimizing the quantities of energy obtained from its own internal battery and laser beams at each time period. Indeed, the goal is to make accurate procurement decisions to minimize the cost of total energy. In addition, we assess the amount of additional procured RE that can be transferred (at a given price) to charge a set of distributed low-power IoT GDs via the WPT technology. We formulated a cost optimization problem for the UAV based on the UAVâs energy exchange with the LBDs and GDs. We employed the YALMIP MATLAB toolbox to handle the proposed constrained optimization problem. Considering a deterministic setting for the RE generation (i.e., no uncertainty in the RE generation), the simulation results demonstrated the effectiveness of the proposed energy procurement procedure in providing a consistent while cost-effective energy procurement framework. However, from a practical point of view, RE generation from sources such as wind and solar power is not deterministic at each time period Îº due to its randomness and intermittent nature [59]. In the presence of uncertainty in $e _ { \kappa } ^ { R } ,$ both inequalities in the second constraint (15) of the specified minimization problem become random quantities, requiring the optimization problem to be adjusted, making it complicated and difficult to solve. Thus, the extension of the current work to describe the energy generated by the internal retailer using a stochastic process is intriguing and will be investigated in future work. Future extensions of this work will also include scenarios involving multiple UAVs.

Furthermore, ground users/IoT devices can offload their computation-intensive tasks to edge servers in mobile edge computing (MEC) systems to conserve energy and reduce latency. Moreover, UAVs have been envisioned as a promising technology for providing relaying and MEC services for ground users in high-demand communication locations, such as hotspot zones. However, the UAVâs limited endurance duration influences the execution of MEC services, resulting in partial MEC services within the time restriction. Similar to the current work, as a future work paper, we can consider the cost-effective and energyefficient scheme design of the UAV while delivering highquality computation offloading services for ground users/IoT devices, particularly in locations where ground communication infrastructures are overloaded or damaged as a consequence of natural catastrophes. The bits allocation of ground users/IoT devices, as well as the trajectory of the UAV can be concurrently optimized with the aim of minimizing energy procurement costs (or maximizing EE) of the UAV. Aside from the UAVâs energy capability constraints, the optimization problem can also take data causality, task delays, service pricing and velocity limitation into account.

## REFERENCES

[1] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âWireless communication using unmanned aerial vehicles (UAVs): Optimal transport theory for hover time optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 12, pp. 8052â8066, Dec. 2017.

[2] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for multi-UAV enabled wireless networks,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2109â2121, Mar. 2018.

[3] Q. Wu and R. Zhang, âCommon throughput maximization in UAV-enabled OFDMA systems with delay consideration,â IEEE Trans. Commun., vol. 66, no. 12, pp. 6614â6627, Dec. 2018.

[4] Y. Cai, Z. Wei, R. Li, D. W. K. Ng, and J. Yuan, âJoint trajectory and resource allocation design for energy-efficient secure UAV communication systems,â IEEE Trans. Commun., vol. 68, no. 7, pp. 4536â4553, Jul. 2020.

[5] C. Zhang and W. Zhang, âSpectrum sharing for drone networks,â IEEE J. Sel. Areas Commun., vol. 35, no. 1, pp. 136â144, Jan. 2017.

[6] I. Khoufi, A. Laouiti, C. Adjih, and M. Hadded, âUAVs trajectory optimization for data pick up and delivery with time window,â Drones, vol. 5, no. 2, 2021, Art. no. 27. [Online]. Available: https://www.mdpi.com/2504-- 446X/5/2/27

[7] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âEfficient deployment of multiple unmanned aerial vehicles for optimal wireless coverage,â IEEE Commun. Lett., vol. 20, no. 8, pp. 1647â1650, Aug. 2016.

[8] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âUnmanned aerial vehicle with underlaid device-to-device communications: Performance and tradeoffs,â IEEE Trans. Wireless Commun., vol. 15, no. 6, pp. 3949â3963, Jun. 2016.

[9] B. Galkin, J. KibiÅda, and L. A. DaSilva, âA stochastic model for UAV networks positioned above demand hotspots in urban environments,â IEEE Trans. Veh. Technol., vol. 68, no. 7, pp. 6985â6996, Jul. 2019.

[10] J. Lyu, Y. Zeng, R. Zhang, and T. J. Lim, âPlacement optimization of UAV-mounted mobile base stations,â IEEE Commun. Lett., vol. 21, no. 3, pp. 604â607, Mar. 2017.

[11] J. Lyu, Y. Zeng, and R. Zhang, âUAV-aided offloading for cellular hotspot,â IEEE Trans. Wireless Commun., vol. 17, no. 6, pp. 3988â4001, Jun. 2018.

[12] M. A. Lahmeri, M. Kishk, and M.-S. Alouini, âStochastic geometry-based analysis of airborne base stations with laser-powered UAVs,â IEEE Commun. Lett., vol. 24, no. 1, pp. 173â177, Jan. 2020.

[13] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surveys Tut., vol. 21, no. 3, pp. 2334â2360, Third Quarter 2019.

[14] Y. Zeng, R. Zhang, and T. J. Lim, âWireless communications with unmanned aerial vehicles: Opportunities and challenges,â IEEE Commun. Mag., vol. 54, no. 5, pp. 36â42, May 2016.

[15] B. Saha et al., âBattery health management system for electric UAVs,â in Proc. Aerosp. Conf., 2011, pp. 1â9.

[16] Y. Zeng and R. Zhang, âEnergy-efficient UAV communication with trajectory optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 6, pp. 3747â3760, Jun. 2017.

[17] M. Alzenad, A. El-Keyi, F. Lagum, and H. Yanikomeroglu, â3D placement of an unmanned aerial vehicle base station (UAV-BS) for energy-efficient maximal coverage,â 2017, arXiv:1705.03415.

[18] J. Ouyang, Y. Che, J. Xu, and K. Wu, âThroughput maximization for laser-powered UAV wireless communication systems,â 2018. [Online]. Available: https://arxiv.org/abs/1803.00690

[19] B. Galkin and L. A. DaSilva, âUAVs as mobile infrastructure: Addressing battery lifetime,â 2018. [Online]. Available: https://arxiv.org/abs/1807. 00996

[20] W. Jaafar and H. Yanikomeroglu, âDynamics of laser-charged UAVs: A battery perspective,â IEEE Internet Things J., vol. 8, no. 13, pp. 10573â10582, Jul. 2021.

[21] T. J. Nugent and J. T. Kare, âLaser power for UAVs,â 2010. [Online]. Available: https://docplayer.net/6901067-Lasermotive-white-paperpower-beaming-for-uavs-a-white-paper-by-t-j-nugent-and-j-t-karelasermotive-llc.html

[22] S. Sekander, H. Tabassum, and E. Hossain, âOn the performance of renewable energy-powered UAV-assisted wireless communications,â Jul. 2019, arXiv:1907.07158.

[23] Y. Chu, C. Ho, Y. Lee, and B. Li, âDevelopment of a solar-powered unmanned aerial vehicle for extended flight endurance,â Drones, vol. 5, no. 2, 2021, Art. no. 44. [Online]. Available: https://www.mdpi.com/2504-- 446X/5/2/44

[24] L. Amorosi, L. Chiaraviglio, and J. GalÃ¡n-JimÃ©nez, âOptimal energy management of UAV-based cellular networks powered by solar panels and batteries: Formulation and solutions,â IEEE Access, vol. 7, pp. 53698â53717, 2019.

[25] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âOptimal transport theory for power-efficient deployment of unmanned aerial vehicles,â in Proc. IEEE Int. Conf. Commun., 2016, pp. 1â6.

[26] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âMobile Internet of Things: Can UAVs provide an energy-efficient mobile architecture?,â in Proc. IEEE Glob. Commun. Conf., 2016, pp. 1â6.

[27] M. Alzenad, A. El-Keyi, and F. Lagum, â3-D placement of an unmanned aerial vehicle base station (UAV-BS) for energy-efficient maximal coverage,â IEEE Wireless Commun. Lett., vol. 6, no. 4, pp. 434â437, Aug. 2017.

[28] L. Ruan et al., âEnergy-efficient multi-UAV coverage deployment in UAV networks: A game-theoretic framework,â China Commun., vol. 15, no. 10, pp. 194â209, 2018.

[29] X. Dai, B. Duo, X. Yuan, and W. Tang, âEnergy-efficient UAV communications: A generalised propulsion energy consumption model,â IEEE Wireless Commun. Lett., vol. 11, no. 10, pp. 2150â2154, Oct. 2022.

[30] H. Wang, G. Ding, F. Gao, J. Chen, J. Wang, and L. Wang, âPower control in UAV-supported ultra dense networks: Communications, caching, and energy transfer,â IEEE Commun. Mag., vol. 56, no. 6, pp. 28â34, Jun. 2018.

[31] X. Liu, Z. Liu, B. Lai, B. Peng, and T. S. Durrani, âFair energy-efficient resource optimization for multi-UAV enabled Internet of Things,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 3962â3972, Mar. 2023.

[32] X. Liu, B. Lai, B. Lin, and V. C. M. Leung, âJoint communication and trajectory optimization for multi-UAV enabled mobile Internet of Vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 15354â15366, Sep. 2022.

[33] X. Hu, K.-K. Wong, K. Yang, and Z. Zheng, âUAV-assisted relaying and edge computing: Scheduling and trajectory optimization,â IEEE Trans. Wireless Commun., vol. 18, no. 10, pp. 4738â4752, Oct. 2019.

[34] C. Zhan, H. Hu, X. Sui, Z. Liu, and D. Niyato, âCompletion time and energy optimization in the UAV-enabled mobile-edge computing system,â IEEE Internet Things J., vol. 7, no. 8, pp. 7808â7822, Aug. 2020.

[35] H. Guo and J. Liu, âUAV-enhanced intelligent offloading for Internet of Things at the edge,â IEEE Trans. Ind. Inform., vol. 16, no. 4, pp. 2737â2746, Apr. 2020.

[36] Y. Liu, K. Xiong, Q. Ni, P. Fan, and K. B. Letaief, âUAV-assisted wireless powered cooperative mobile edge computing: Joint offloading, CPU control, and trajectory optimization,â IEEE Internet Things J., vol. 7, no. 4, pp. 2777â2790, Apr. 2020.

[37] Z. Yu, Y. Gong, S. Gong, and Y. Guo, âJoint task offloading and resource allocation in UAV-enabled mobile edge computing,â IEEE Internet Things J., vol. 7, no. 4, pp. 3147â3159, Apr. 2020.

[38] L. Li, X. Wen, Z. Lu, and W. Jing, âAn energy efficient design of computation offloading enabled by UAV,â Sensors, vol. 20, no. 12, 2020, Art. no. 3363. [Online]. Available: https://www.mdpi.com/1424--8220/ 20/12/3363

[39] Z. Zhai, X. Dai, B. Duo, X. Wang, and X. Yuan, âEnergy-efficient UAVmounted RIS assisted mobile edge computing,â IEEE Wireless Commun. Lett., vol. 11, no. 12, pp. 2507â2511, Dec. 2022.

[40] Z. Dai, G. Xu, Z. Liu, J. Ge, and W. Wang, âEnergy saving strategy of UAV in MEC based on deep reinforcement learning,â Future Internet, vol. 14, no. 8, 2022, Art. no. 226. [Online]. Available: https://www.mdpi. com/1999--5903/14/8/226

[41] T. Long, M. Ozger, O. Cetinkaya, and O. B. Akan, âEnergy neutral Internet of Drones,â IEEE Commun. Mag., vol. 56, no. 1, pp. 22â28, Jan. 2018.

[42] L. Yang, J. Chen, M. O. Hasna, and H.-C. Yang, âOutage performance of UAV-assisted relaying systems with RF energy harvesting,â IEEE Commun. Lett., vol. 22, no. 12, pp. 2471â2474, Dec. 2018.

[43] Z. Yang, W. Xu, and M. Shikh-Bahaei, âEnergy efficient UAV communication with energy harvesting,â IEEE Trans. Veh. Technol., vol. 69, no. 2, pp. 1913â1927, Feb. 2020.

[44] Y. Sun, D. Xu, D. W. K. Ng, L. Dai, and R. Schober, âOptimal 3D-trajectory design and resource allocation for solar-powered UAV communication systems,â IEEE Trans. Commun., vol. 67, no. 6, pp. 4281â4298, Jun. 2019.

[45] A. Alsharoa, H. Ghazzai, A. Kadri, and A. E. Kamal, âSpatial and temporal management of cellular HetNets with multiple solar powered drones,â IEEE Trans. Mobile Comput., vol. 19, no. 4, pp. 954â968, Apr. 2020.

[46] A. Alsharoa, H. Ghazzai, A. Kadri, and A. E. Kamal, âEnergy management in cellular HetNets assisted by solar powered drone small cells,â in Proc. IEEE Wireless Commun. Netw. Conf., 2017, pp. 1â6.

[47] S. Sekander, H. Tabassum, and E. Hossain, âStatistical performance modeling of solar and wind-powered UAV communications,â IEEE Trans. Mobile Comput., vol. 20, no. 8, pp. 2686â2700, Aug. 2021.

[48] L. Xie, X. Cao, J. Xu, and R. Zhang, âUAV-enabled wireless power transfer: A tutorial overview,â 2021. [Online]. Available: https://arxiv.org/ abs/2103.00207

[49] M. Boukoberine, Z. Zhou, and M. Benbouzid, âA critical review on unmanned aerial vehicles power supply and energy management: Solutions, strategies, and prospects,â Appl. Energy, vol. 255, pp. 1â22, Dec. 2019.

[50] F. H. Panahi and F. H. Panahi, âUnmanned aerial vehicles toward intelligent transportation systems,â to be published.

[51] M. A. Ali and A. Jamalipour, âUAV-aided cellular operation by user offloading,â IEEE Internet Things J., vol. 8, no. 12, pp. 9855â9864, Jun. 2021.

[52] D. Killinger, âFree space optics for laser communication through the air,â Opt. Photon. News, vol. 13, no. 10, pp. 36â42, Oct. 2002. [Online]. Available: http://www.optica-opn.org/abstract.cfm?URI=opn-13--10-36

[53] O. Cetinkaya and G. V. Merrett, âEfficient deployment of UAV-powered sensors for optimal coverage and connectivity,â in Proc. IEEE Wireless Commun. Netw. Conf., 2020, pp. 1â6.

[54] P. N. Alevizos and A. Bletsas, âSensitive and nonlinear far-field RF energy harvesting in wireless communications,â IEEE Trans. Wireless Commun., vol. 17, no. 6, pp. 3670â3685, Jun. 2018.

[55] S. Boyd and L. Vandenberghe, Convex Optimization. Cambridge, U.K.: Cambridge Univ. Press, 2004.

[56] J. Lofberg, âYALMIP : A toolbox for modeling and optimization in MATLAB,â in Proc. IEEE Int. Conf. Robot. Automat., 2004, pp. 284â289.

[57] M.-A. Lahmeri, M. A. Kishk, and M.-S. Alouini, âLaser-powered UAVs for wireless communication coverage: A large-scale deployment strategy,â IEEE Trans. Wireless Commun., vol. 22, no. 1, pp. 518â533, Jan. 2023.

[58] R. Corless, G. Gonnet, D. Hare, D. Jeffrey, and D. Knuth, âOn the Lambert W function,â Adv. Comput. Math., vol. 5, pp. 329â359, Jan. 1996.

[59] N. B. Rached, H. Ghazzai, A. Kadri, and M.-S. Alouini, âEnergy management optimization for cellular networks under renewable energy generation uncertainty,â IEEE Trans. Green Commun. Netw., vol. 1, no. 2, pp. 158â166, Jun. 2017.

<!-- image-->  
Farzad H. Panahi received the MSc and PhD degrees in electrical engineering from the Iran University of Science and Technology, in 2009 and 2015, respectively. Since 2012, he has been with the University of Kurdistan, Sanandaj (UOK) where he is currently an assistant professor with the Department of Electronics and Communication Engineering. His research interests include Internet of Things and intelligent sensor networks, robotics and autonomous systems, and intelligent communication systems.

<!-- image-->  
communications.

Fereidoun H. Panahi received the MS and PhD degrees in electrical engineering from Keio University, Yokohama, Japan, in 2013 and 2016, respectively. From 2016 to 2019, he was a visiting postdoctoral researcher with Keio University and the Department of Electrical Engineering, University of California, Los Angeles (UCLA). He is currently an Assistant Professor with the University of Kurdistan, Sanandaj (UOK), Iran. His research interests include green communications and networking, the Internet of Things, and intelligent wireless

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_3_img_2.png|page_3_img_2]]
3. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_6_img_1.jpeg|page_6_img_1]]
4. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_7_img_1.jpeg|page_7_img_1]]
5. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_8_img_1.jpeg|page_8_img_1]]
6. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_9_img_1.jpeg|page_9_img_1]]
7. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_9_img_2.jpeg|page_9_img_2]]
8. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_10_img_1.png|page_10_img_1]]
9. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_10_img_2.jpeg|page_10_img_2]]
10. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_10_img_3.jpeg|page_10_img_3]]
11. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_12_img_1.jpeg|page_12_img_1]]
12. [[../extracted_images/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications /page_12_img_2.jpeg|page_12_img_2]]

---

