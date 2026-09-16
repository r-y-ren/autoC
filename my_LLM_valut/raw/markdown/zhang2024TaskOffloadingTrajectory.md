# Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC Systems

Yuhao Zhang , Zhufang Kuang , Member, IEEE, Yanyan Feng, and Fen Hou , Member, IEEE

AbstractâWith the advantages of high mobility and flexible deployment, Unmanned Aerial Vehicle (UAV) combines with Mobile Edge Computing (MEC) is a promising technology. When dynamic Terminal Users (TUs) offload tasks to UAVs, eavesdroppers may eavesdrop on the channel information. The offloading decisions, trajectory plannings of UAVs and resource allocation with the objective of high-capacity secure communication is a challenging problem. In this paper, we design a multi-UAVs MEC system, where the original region is divided into several sub-regions and TUs offload tasks to UAVs which provide computing services for these TUs. Meanwhile, A joint optimization problem of offloading decision, resource allocation and trajectory planning is formulated, where TUs move with the Gauss-Markov random model. In addition, the Base Station (BS) emits jamming signals to evade the eavesdropping of offloading information from eavesdroppers. The goal of the optimization problem is to maximize the TUsâ minimum secure calculation capacity, and a Joint Dynamic Programming and Bidding (JDPB) algorithm is proposed to solve it. The Successive Convex Approximation (SCA) and Block Coordinate Descent (BCD) algorithms are used to handle the resource allocation and trajectory planning problems, and the bidding method is used to address the task offloading decision problem. Simulation results show that JDPB has better performance and better robustness under different parameter settings than other schemes.

Index TermsâDynamic user, multi -UAVs, secure communication, task offloading, trajectory planning, MEC.

Digital Object Identifier 10.1109/TMC.2024.3442909

## I. INTRODUCTION

M OBILE Edge Computing (MEC) is a promising tech-nology for enhancing the edge computing power of nology forenhancing theedge computing power of mobile networks [1]. For example, a new fully-decentralized on-demand MEC-small cells peer-offloading network is proposed to enhance latency and service providersâ privacy protection [2]. In [3], combining MEC servers and cloud servers, the energy consumption of the entire MEC system is minimized by splitting computational tasks. Afterwards, a noval simultaneously transmitting and reflecting reconfigurable intelligent surface assisted MEC system is present to optimize the energy consumption [4]. In Vehicle Edge Computing (VEC), Gao et al. ensure service quality by incorporating a fast switching channel between vehicles and edge servers [5]. At the same time, because of the special advantages of Unmanned Aerial Vehicles (UAVs) involving flexible deployment, strong mobility and line-of-sight connection, the UAVs have been widely used in wireless networks [6]. In [7], the hovering and maneuvering capabilities of the UAVs are used to provide task offloading services for devices in wireless networks. Especially when communication Base Station (BS) is not available, the UAVs can provide additional computation power and global coverage of terminal devices [8]. Although the integration of the UAV into the MEC can bring benefits to wireless communication, the combination still faces many challenges, such as task offloading, trajectory planning and resource allocation [9].

The existing related work does not consider trajectories of multi-UAVs, dynamic TUs and secure communication simultaneously, then we propose a secure communication scheme for a multi-UAV-assisted MEC system for dynamic users, while considering task offloading, trajectory planning and resource allocation. Table I reveals a comparison of existing works. In this scheme, the UAV dynamically adjusts its position to provide services to the moving ground users. And a BS is set to send jamming signals to reduce the interception of offloading data from ground eavesdroppers. Meanwhile, we maximize the minimum secure calculation capacity for the user by optimizing the UAVsâ trajectory and other wireless resources, including transmission power, time and computation frequency. The main contributions of this paper are summarized as follows:

- A secure communication scenario with a multi-UAVsassisted MEC system is researched, where the original region is divided into some sub-regions and TUs offload tasks to UAVs which provide computing services for TUs.

TABLE I  
COMPARISON OF THE EXISTING WORKS
<table><tr><td rowspan=1 colspan=1>Reference</td><td rowspan=1 colspan=1>Optimizationobjectives</td><td rowspan=1 colspan=1>Dynamicuser</td><td rowspan=1 colspan=1>Multi-UAVs</td><td rowspan=1 colspan=1>Trajectoryplanning</td><td rowspan=1 colspan=1>Securecommunication</td><td rowspan=1 colspan=1>offloadingdecision</td><td rowspan=1 colspan=1>resourceallocation</td></tr><tr><td rowspan=1 colspan=1>[9]</td><td rowspan=1 colspan=1>energy</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>[14]</td><td rowspan=1 colspan=1>energy</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>utility</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[28]</td><td rowspan=1 colspan=1>reward</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[32]</td><td rowspan=1 colspan=1>offloadingcapacity</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[42]</td><td rowspan=1 colspan=1>offloadingcapacity</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>our paper</td><td rowspan=1 colspan=1>ofloadingcapacity</td><td rowspan=1 colspan=1>J</td><td rowspan=1 colspan=1>J</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>1</td></tr></table>

Meanwhile, the BS can send signals to interfere with the ground eavesdroppersâ eavesdropping. In response, a joint optimization problem of offloading decision, resource allocation and trajectory planning of multi-UAVs is formulated, where the TUs move with a Gauss-Markov random model. The goal is to maximize the minimum secure calculation capacity of all TUs while considering the energy consumption requirements of each UAV.

The optimization problem is decomposed into two subproblems and a optimization method framework based on convex optimization and bidding method is proposed to solve it more easily. For the first subproblem, the resource allocation and trajectory planning problems of UAVs are solved by Successive Convex Approximation (SCA) and Block Coordinate Descent (BCD) algorithms. And for the second subproblem, dynamic programming and bidding algorithms are combined to solve the offloading decision problem from TUs to UAVs.

- A Joint Dynamic Programming and Bidding (JDPB) method is proposed to solve the formulated problem. Simulation results show that JDPB effectively improves the security performance compared with the Random Strategy (RS), Greedy Strategy (GS) and other three benchmark schemes. And for the UAVs at different starting points, JDPB exhibites better generalization ability.

## II. RELATED WORK

There is a lot of literature that studies random movement of TUs, the research object of secure communication capacity, and trajectories of multiple UAVs separately, but there is little literature that considers them as a whole. At the same time, many scholars devote themselves to the such problem by optimizing different research objects.

To alleviate the burden on the MEC system and achieve better quality of service, reducing the energy consumption of the UAV-supported MEC system has been widely studied. For instance, an optimal digital propositioning scheme is assigned to the terminal device by minimizing the energy consumption of the terminal device [10]. In [11], an Intelligent Reflective Surface (IRS) system is deployed to improve the environment of wireless communication by minimizing the energy consumption. In [12], a two-level alternation algorithm is proposed to solve the problem that offloading usersâ latency-sensitive tasks to collaborative devices or MEC servers, which can obtain less energy consumption. To improve the security and reliability, the communication and computation resource allocations are optimized by minimizing the energy consumption of the UAV [13]. In [14], a platform of flying MEC is considered to provide computing resources to user equipment by minimizing energy consumption. In [15], the average weighted energy consumption is minimized by jointly optimizing task offloading, communication and computation resource allocation and trajectory planning.

In addition, reducing the latency of the MEC system can also provide better services to terminal devices. In [16], a UAV-assisted task offloading paradigm is raised to minimize the average task response latency. In [17], a millimeter-wave backhaul UAV-assisted network for multi-access edge computing is proposed, which solves the UAV trajectory planning and resource allocation problems by minimizing the network delay. In [18], a stochastic computation offloading problem is formulated to maintain low latency. In [19], collaborations among multiple UAVs are considered to optimize task offloading and resource allocation by minimizing the total latency of users. In [20], a two-layer UAV maritime communication network is established to solve the latency minimization problem. In [21], the authors jointly optimize service caching, task offloading, resource allocation and UAV deployment issues by minimizing the maximum task completion delay.

Recently, some scholars have also paid much attention to network utility and network overhead. For example, a multileader multi-follower Stackelberg game is designed to optimize task offloading and resource allocation by maximizing network energy efficiency [22]. In [23], a joint cache decision, computation offloading, CPU frequency allocation and transmission power allocation problem is proposed to reduce the cost of task transmission by adding computational resources and caches. In [24], a multi-leader multi-follower Stackelberg game is devised to jointly optimize the task offloading, UAV location deployment problem by minimizing the network overhead. In [25], a novel UAV-supported MEC architecture is presented to jointly optimize the task offloading, spectrum and computation resource allocation and UAV location deployment problems by minimizing the overhead of Internet of Things (IoT) users. In [26], a two-level alternation framework is proposed to solve the power allocation and partial offloading scheduling problem by minimizing the weighted sum of the energy consumption and execution delay. In [27], a innovative data offloading decision framework is proposed to improve user service by maximizing utility.

In practice, the usersâ location may change dynamically with time, which increases the difficulty of UAV trajectory planning. In [28], to ensure the qualities of services for the users, the UAV with limited energy dynamically performs computational tasks obtained from the mobile users and plans the trajectory based on the locations of the mobile users. In [29], a UAV-assisted MEC platform is built to provide flexible and resilient computing services for mobile users, which can jointly optimize the resource allocation and UAV trajectory. In [30], the deterministic policy gradient algorithm is proposed, which enables the UAV can intelligently track mobile users to maximize the expected uplink and rate by the learned trajectories.

Notably, the above work basically only considers how to improve the performance and efficiency of the MEC system, without considering the secure communication issues. Actually, there exists a problem that eavesdroppers may eavesdrop the offloading data, which poses a great risk to the communication security [31], so it is necessary to ensure the physical layer security. For example, in order to reduce the eavesdropping of data offloading by UAV eavesdroppers, a jammer is set up to emit jamming signals on the ground to optimize the resource allocation and trajectory planning [32]. Furthermore, Non-Orthogonal Multiple-Access (NOMA) technique is used to improve the spectrum efficiency and maximize the average secure calculation capacity of the system [33]. And the secure transmission assisted by UAV is also considered in [34].

The rest of the paper is organized as follows: Section III presents the system model and the original optimization problem. Section IV proposes the dynamic programming based value competing optimization algorithm and solves the problem by a convex optimization approach. In Section V, we perform simulations to demonstrate the effectiveness of our proposed scheme. Section VI concludes the full paper.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, first we propose a MEC model based on multi-UAV multi-dynamic users and analyze the capacity of the task unloading and the energy of calculation. Then the optimization problem is formulated with the goal of maximizing the systemâs secure calculation capacity.

## A. Network Model

Since TUs have limited computing capabilities and energy, the flying fixed-wing UAVs serve as edge servers to provide services to the TUs. Fig. 1 shows the system model. The model contains K TUs, M UAVs, E eavesdroppers and a BS, and the BS is used to disturb eavesdroppers. The sets of TUs and UAVs are denoted by $\mathcal { K } = \{ 1 , 2 , . . . , K \}$ and $\mathcal { M } = \{ 1 , 2 , . . . , M \}$ , respec-= 1 2 = 1tively. The set of eavesdroppers is denoted by $\mathcal { E } = \{ 1 , 2 , . . . , E \}$ . The locations of BS and eavesdroppers $e \in { \mathcal { E } }$ 1 2are fixed as $q _ { s } = ( x _ { s } , y _ { s } )$ and $q _ { e } = ( x _ { e } , y _ { e } )$ , respectively. The TUs move s = ( s s) e = ( e e)randomly and offload the tasks to the UAV. As shown in Fig. 1,

<!-- image-->  
Fig. 1. System model.

TUs 1,3,4 are eavesdropped by eavesdropper 2, TU 2 is eavesdropped by eavesdropper 1, and the BS jams eavesdroppers 1,2. The position of each TU is dynamically updated according to the Gauss-Markov Random Model (GMRM). The TUs offload data to the UAV, and eavesdroppers eavesdrop on the data link at the same time. The BS interferes with the eavesdroppers to ensure secure communication by broadcasting the interference signal. Since the UAVs have already known the BS interference signal in advance, the UAVs can separate the interference signal from the received signal, so the jamming doesnât impact the ongoing authentic communications. However, eavesdroppers do not know the BS signal in advance, so eavesdroppers treat all reveived signals as effective signals and are interfered by the BS signal. We assume that UAVs receive the position information and channel state information of the TUs and eavesdroppers according to the on-board optical camera or the synthetic aperture radar in each time slot [32], thus the optimization is real-time and we can acquire the limit of secure calculation capacity performance.

Interestingly, different from the search and rescue in the event of disasters [35], the model can be applied in the battlefield. Concretely, the UAVs collect intelligence from the TUâs exploration, in which the link needs to be secure, so a BS is set up to jam devices that are not in the system. In addition, the model can also be used in the trading, in which the eavesdroppers may be placed in advance. In order to prevent information leakage, a BS is set to interfere with the eavesdroppers.

The task offloadings of TUs are based on Time Division Multiple Access (TDMA) scheme. The maximal latency is denoted as $T ,$ , which is divided into N time slots and each time slot length is $\Delta$ with $\Delta = T / N$ . We assume that TU j has a task $U _ { j }$ to execute Î Î =in the total time T and $U _ { j }$ can be defined as $U _ { j } \stackrel { \cdot } { = } ( C _ { j } , Q _ { j } )$ where $C _ { j }$ j j = ( j j)describes the number of CPU cycles of TU j required jto compute per input bit of data and $Q _ { j }$ defines the minimum secure computing requirement of TU j in each time slot t. It indicates that the number of secure computing bits for each TU in each time slot must exceed a threshold, so that the basic secure computational requirement for each TU can be guaranteed.

The time slot segmentation protocol of TUs in TDMA scheme is shown in Fig. 2. We define $K _ { \mathrm { m a x } }$ as the maximum number of TUs that can be served by each UAV. In every time slot, the number of TUs for each UAV service is different. K represents the number of the TUs served by the ith UAV and $\begin{array} { r } { \sum _ { i } ^ { M } K _ { i } = K } \end{array}$ $\tau _ { j , i } [ t ]$ i i =represents the time allocation factor for each TU j to offload the task to UAV i in time slot $t ,$ and $\begin{array} { r } { \sum _ { j } ^ { K _ { i } } \tau _ { j , i } [ t ] \leq 1 } \end{array}$ $0 \leq \tau _ { j , i } [ t ] \leq 1 , i \in \mathcal { M }$

<!-- image-->  
Fig. 2. The time slot segmentation protocol of TUs in TDMA scheme.

## B. TUs Movement Model

The locations of TUs are random in time slot t 0 and we =assume that the TUsâ position does not change during a time slot . According to the GMRM [36], the velocity $v _ { j } [ t ]$ and Îdirection $\theta _ { j } [ t ]$ j [ ]of the jth TU in the tth time slot are updated as

$$
v _ { j } [ t ] = \alpha _ { 1 } v _ { j } [ t - 1 ] + ( 1 - \alpha _ { 1 } ) \bar { v } + \sqrt { 1 - \alpha _ { 1 } ^ { 2 } } \Phi _ { j } , \forall j , t ,\tag{1a}
$$

$$
\theta _ { j } [ t ] = \alpha _ { 2 } \theta _ { j } [ t - 1 ] + ( 1 - \alpha _ { 2 } ) \bar { \theta } _ { j } + \sqrt { 1 - \alpha _ { 2 } ^ { 2 } } \Psi _ { j } , \forall j , t ,\tag{1b}
$$

where v is the average velocity of all TUs in the last time slot, $\bar { \theta _ { j } }$ Â¯is the average direction of the jth TU, and $0 \leq \alpha _ { 1 } , \alpha _ { 2 } \leq 1$ j 0 1indicate the weight of velocity and direction to adjust the previous state, respectively. To balance the current state and the previous state, we set the $\alpha _ { 1 }$ and $\alpha _ { 2 }$ to 0.5 [36]. We assume that the average rate of all TUs is same and the average direction of different TUs is different. For the jth TU, $\Phi _ { j }$ and $\Psi _ { j }$ follow Î¦j Î¨jtwo indenpendent Gaussian distributions with different meanvariance pairs $( \bar { \xi } _ { v _ { j } } , \zeta _ { v _ { j } } ^ { 2 } )$ and $( \bar { \xi } _ { \theta _ { j } } , \zeta _ { \theta _ { i } } ^ { 2 } )$ , both of which reflect v v Î¸ Î¸ the movement randomness of the TUs and follow the standard normal distribution by setting (0,1) [36].

The location of the jth TU in the tth time slot is denoted by $q _ { j } [ t ] = ( x _ { j } [ t ] , y _ { j } [ t ] , 0 )$ . According to the boundary-free simuj[ ] = ( j[ ] j[ ] 0)lation movement model and (1a) and (1b), the TU location is updated as [36]

$$
x _ { j } [ t ] = x _ { j } [ t - 1 ] + v _ { j } [ t - 1 ] \cos \theta _ { j } [ t - 1 ] \times \Delta , \forall j , t ,\tag{2a}
$$

$$
y _ { j } [ t ] = y _ { j } [ t - 1 ] + v _ { j } [ t - 1 ] \sin \theta _ { j } [ t - 1 ] \times \Delta , \forall j , t .\tag{2b}
$$

In addition, the location of the ith UAV in the tth time slot is denoted by $q _ { i } [ t ] = ( x _ { i } [ t ] , y _ { i } [ t ] , H )$ , where H is the fixed altitude i[ ] = ( i[ ] i[ ] )for the UAV to fly. If the altitudes of the UAVs are not fixed, UAVs that are too high can cover more TUs, but require more transmission delay and energy consumption. UAVs that are too low can reduce transmission delay and energy consumption, but only cover fewer TUs. This 3-dimensional trajectory planning problem needs to find an optimal height that balances the number of the TUs and the transmission delay and energy consumption, which is a difficult question. Thus we only consider fixed heights in this paper.

## C. TUs Offloading Model

Since most UAV communications use Line Of Sight (LOS) links, the channels between the UAVs and TUs are assumed to be the LOS links, which follow free-space path loss [37], [38], [39], [40]. So the channel gain between UAV i and TU j in the time slot t is expressed as

$$
g _ { j , i } [ t ] = \frac { \beta _ { 0 } } { ( x _ { j } [ t ] - x _ { i } [ t ] ) ^ { 2 } + ( y _ { j } [ t ] - y _ { i } [ t ] ) ^ { 2 } + H ^ { 2 } } , \forall j , i , t ,\tag{3}
$$

where $\beta _ { 0 }$ is the unit distance channel gain. The channel gain between the BS and the eavesdropper e is expressed as

$$
g _ { s , e } = \frac { \beta _ { 0 } } { ( x _ { s } - x _ { e } ) ^ { 2 } + ( y _ { s } - y _ { e } ) ^ { 2 } } , \forall e .\tag{4}
$$

The channel between TU j and eavesdropper e is modeled as an independent Rayleign fading, so the channel gain from TU j to the eavesdropper e in the time slot t is expressed as

$$
g _ { j , e } [ t ] = \frac { \beta _ { 0 } \rho _ { e } } { d _ { j , e } [ t ] ^ { \varphi } } , \forall j , e , t ,\tag{5}
$$

where $\rho _ { e }$ is Rayleigh fading coefficient following exponential edistribution with unit mean, $d _ { j , e } [ t ]$ is the distance between TU j,e[ ]j and eavesdropper e in the tth time slot, which is defined as $d _ { j , e } [ t ] = \| q _ { j } [ t ] - q _ { e } \|$ , and $\varphi$ is the path loss coefficient. j,e[ ] = j[ ] eAccording to Shannon formula, the offloading transmission rate from TU j to UAV i in the time slot t is expressed as

$$
r _ { j , i } [ t ] = B \log _ { 2 } \bigg ( 1 + \frac { p _ { j } [ t ] g _ { j , i } [ t ] } { N _ { 0 } B } \bigg ) , \forall j , i , t ,\tag{6}
$$

where $p _ { j } [ t ]$ is the transmission power of TU j in the time slot $t , \ N _ { 0 }$ ]is the noise power spectral density and B is the channel bandwidth. The BS broadcasts signal and eavesdroppers regard it as valid signals, so the leakage rate from TU j to the eavesdropper e in the time slot t is expressed as [41]

$$
r _ { j , e } [ t ] = B \log _ { 2 } \bigg ( 1 + \frac { p _ { j } [ t ] g _ { j , e } [ t ] } { p _ { s } g _ { s , e } + N _ { 0 } B } \bigg ) , \forall j , e , t ,\tag{7}
$$

where $p _ { s }$ is the interference signal power transmitted by BS. The ssecure offloading rate from TU j to UAV i in the time slot t is expressed as

$$
\bar { r } _ { j , i } [ t ] = ( r _ { j , i } [ t ] - \operatorname* { m a x } _ { e \in \mathcal { E } } r _ { j , e } [ t ] ) ^ { + } , \forall j , i , e , t ,\tag{8}
$$

where the $( . ) ^ { + }$ means that it is meaningful when it takes a ( )positive number [42]. The amount of data that TU j securely offloads to UAV i in the time slot t is expressed as

$$
D _ { j , i } [ t ] = \tau _ { j , i } [ t ] \times \Delta \times \bar { r } _ { j , i } [ t ] , \forall j , i , t .\tag{9}
$$

## D. UAV Energy Consumption Model

1) Computing Energy: The CPU of UAV i operates at a frequency $f _ { i } [ t ]$ cycle/s. The amount of data to be computed i[ ]in time slot t for TU j is $D _ { j , i } [ t ]$ and the computing energy consumption is expressed as

$$
E _ { i , j } ^ { c } [ t ] = \eta C _ { j } D _ { j , i } [ t ] f _ { i } [ t ] ^ { 2 } , \forall j , i , t ,\tag{10}
$$

where $\eta$ is the effective switching capacitance of the UAV and $C _ { j }$ is the number of CPU cycles required to compute 1 b of data.

In order to process all the data in $\Delta ,$ , the frequency $f _ { i } [ t ]$ of UAV Îi should satisfy the following constraint

$$
f _ { i } [ t ] \geq \frac { 1 } { \Delta } \sum _ { j = 1 } ^ { K _ { i } } C _ { j } D _ { j , i } [ t ] , \forall j , i , t .\tag{11}
$$

Combining (9) and (10), the computing energy consumption required by UAV i for the offloaded data of TU j at time slot t is expressed as

$$
E _ { i , j } ^ { c } [ t ] = \eta C _ { j } \tau _ { j , i } [ t ] \times \Delta \times \bar { r } _ { j , i } [ t ] f _ { i } [ t ] ^ { 2 } , \forall j , i , t .\tag{12}
$$

2) Flying Energy: The flying energy consumption within each time slot t is related to the velocity $v _ { i } [ t ]$ of the UAV. Since $\Delta$ i[ ] Îis small enough, we assume that the position of UAV is constant within each time slot. Then the velocity of the UAV in the tth time slot can be calculated by dividing the distance by the time and the velocity is expressed as

$$
v _ { i } [ t ] = \frac { \| q _ { i } [ t + 1 ] - q _ { i } [ t ] \| } { \Delta } , \forall i , t .\tag{13}
$$

In particular, when $t { = } 1$ Î, the velocity is calculated using the initial UAV position $q _ { i } ^ { I } ( q _ { i } ^ { I } = q _ { i } [ 1 ] )$

$$
v _ { i } [ 1 ] = \frac { \| q _ { i } [ 2 ] - q _ { i } ^ { I } \| } { \Delta } , \forall i .\tag{14}
$$

when $t = N$ Î, the velocity is calculated using the UAV final position $q _ { i } ^ { F } ( q _ { i } ^ { F } = q _ { i } [ N + 1 ] )$

$$
v _ { i } [ N ] = \frac { \| q _ { i } ^ { F } - q _ { i } [ N ] \| } { \Delta } , \forall i ,\tag{15}
$$

where the initial position $q _ { i } ^ { I }$ is fixed. We can set a final location ias the landing point and they can reserve energy to fly to the landing point when the UAVs finish the flying during the total time $T ,$ . The flying energy consumption of UAV i is expressed as

$$
\begin{array} { r } { E _ { i } ^ { f } [ t ] = 0 . 5 \mathrm { { m } } \times \Delta \times \lVert \boldsymbol { v } _ { i } [ t ] \rVert ^ { 2 } , \forall i , t , } \end{array}\tag{16}
$$

where m is the mass of the UAV and each UAV has the same mass.

## E. Problem Formulation

During the entire UAV flying time T , the secure calculation capacity of TU j to UAV i is defined as the average number of secure calculation bits that can be achieved as

$$
\bar { R } _ { j , i } [ t ] = \frac { 1 } { T } \left( \Delta \times \sum _ { t = 1 } ^ { N } \tau _ { j , i } [ t ] \bar { r } _ { j , i } [ t ] \right) , \forall j , i , t .\tag{17}
$$

The objective of the optimization problem is to maximize the minimum secure calculation capacity by jointly optimizing the offloading decision $a _ { i j } [ t ] , \bar { j } \in \mathcal { K }$ from TU j to UAV i; the transmission power $p _ { j } [ t ]$ [ ]of TU $j ;$ the time allocation factor $\tau _ { j , i } [ t ]$ j[ ]; the CPU processing frequency $f _ { i } [ t ]$ of UAV j,i[ ]i; and the trajectory $q _ { i } [ t ] , i \in \mathcal { M } , t \in N$ i[ ]of UAV. Let $\Theta =$ $\{ a _ { i j } [ t ] , p _ { j } [ t ] , \tau _ { j , i } [ t ] , f _ { i } [ t ] , q _ { i } [ t ] \}$ Î =, then we can formulate the opij [ ] j [ ] j,i[ ] itimization problem as

$$
( P 1 ) : \operatorname* { m a x } _ { \Theta } \ \operatorname* { m i n } _ { j \in \mathcal { K } } \ a _ { i j } [ t ] { \bar { R } } _ { j , i } [ t ]\tag{18a}
$$

$$
\mathrm { s . t . } \sum _ { t = 1 } ^ { N - 1 } \sum _ { j = 1 } ^ { K _ { i } } a _ { i j } [ t + 1 ] E _ { i , j } ^ { c } [ t + 1 ] + \sum _ { t = 1 } ^ { N } E _ { i } ^ { f } [ t ] < \epsilon , \forall j , i , t ,\tag{18b}
$$

$$
v _ { \operatorname* { m i n } } \leq v _ { i } [ t ] \leq v _ { \operatorname* { m a x } } , \forall i , t ,\tag{18c}
$$

$$
\| q _ { i } [ t ] - q _ { i ^ { \prime } } [ t ] \| \geq d , i \neq i ^ { \prime } , i , i ^ { \prime } \in \mathcal { M } , \forall t ,\tag{18d}
$$

$$
0 \leq p _ { j } [ t ] \leq p _ { \operatorname* { m a x } } , \forall j , t ,\tag{18e}
$$

$$
\frac { 1 } { T } \sum _ { t = 1 } ^ { N } \tau _ { j , i } [ t ] \times \Delta \times p _ { j } [ t ] \leq p _ { j } ^ { a v e } , \forall j , i , t ,\tag{18f}
$$

$$
\sum _ { j = 1 } ^ { K } \tau _ { j , i } [ t ] \leq 1 , \forall j , i , t ,\tag{18g}
$$

$$
0 \leq \tau _ { j , i } [ t ] \leq 1 , \forall j , i , t ;
$$

$$
D _ { j , i } [ t ] \geq Q _ { j } , \forall j , i , t ,\tag{18h}
$$

(18i)

$$
f _ { i } [ t ] \geq \frac { 1 } { \Delta } \sum _ { j = 1 } ^ { K _ { i } } C _ { j } D _ { j , i } [ t ] , \forall j , i , t ,\tag{18j}
$$

$$
0 \leq f _ { i } [ t ] \leq f _ { \operatorname* { m a x } } , \forall i , t ,\tag{18k}
$$

$$
a _ { i j } [ t ] \in \{ 0 , 1 \} , \forall j , i , t ,\tag{18l}
$$

$$
\sum _ { j = 1 } ^ { K } a _ { i j } [ t ] \leq K _ { \operatorname* { m a x } } , \forall j , i , t ,\tag{18m}
$$

$$
\sum _ { i = 1 } ^ { M } a _ { i j } [ t ] = 1 , \forall j , i , t ,\tag{18n}
$$

where  in (18b) is the UAV initial total energy. Equations (18c) is the minimum and maximum speed constraints for the UAV to maintain high altitude flying. Equation (18d) indicates that the two UAVs need to maintain at least a secure distance. Equation (18e) is the transmission power constraint of the TU. Equation (18f) is the offloading energy consumption constraint of TU j over the whole period $T ,$ where $p _ { j } ^ { a v e }$ is the average transmitted power of $\mathrm { T U } j$ j. Equations (18g) and (18h) are the constraints that need to be satisfied by the time allocation factor of TU j in each time slot. Equation (18i) denotes that the number of secure computation bits of TU j in time slot t must exceed a threshold value to guarantee the minimum secure computation requirement for each TU, and $Q _ { j }$ denotes the minimum secure computation jrequirement for each TU j in each time slot. Equation (18j) denotes the constraint that the CPU processing frequency of UAV i in each time slot to process all TUsâ secure data. Equation (18k) denotes the constraint that the CPU processing frequency of UAV i needs to satisfy, where $f _ { \mathrm { m a x } }$ is the maximum CPU processing frequency that the UAV can achieve. Equation (18m) denotes the constraint on the number of TUs that can be served by each UAV. Equation (18n) indicates that each TU can be served by only one UAV.

## IV. PROBLEM SOLUTION

Since the locations of the TUs in each time slot are constantly changing, area division is required within each time slot and one match is required between UAV and TU for each time slot.

In order to solve problem (P1), it is divided into two subproblems. In the first subproblem we solve the continuous variables the transmission power $p _ { j } [ t ]$ of TU $j ,$ the time allocation factor $\tau _ { j , i } [ t ]$ , the CPU processing frequency $f _ { i } [ t ]$ of UAV, and the j,i[ ] i[ ]trajectory q t of UAV. And in the second subproblem we solve i[ ]the integer variables offloading dicisions $a _ { i j } [ t ]$ between the ij[ ]UAVs and the TUs. Once the first subproblem is solved to obtain the optimal policies, we can easily optimize $a _ { i j } [ t ]$ by bidding.

The optimization of offloading decision $a _ { i j } [ t ]$ ] is a 0-1 proij[ ]gramming problem from (18l), which can be solved by dynamic programming, so a Joint Dynamic Programming and Bidding (JDPB) optimization method is proposed in Algorithm 1.

The main idea of JDPB method is to bid for the TUs one by one, and the bidding evaluation index is the number of TUsâ secure calculation capacities. We stipulate the UAV that obtains the most secure calculation capacities wins the bit, and if the number of TUs served by the UAV exceeds the maximum serving number $K _ { \mathrm { m a x } }$ of TUs, the UAV will be removed from the bidding.

The problem solved by the JDPB algorithm is the offloading decision $a _ { i j } [ t ]$ and the search space within each time slot is $K \times M$ ij [ ]. Therefore, its computational complexity is related to the number of TUs K and the number of UAVs M. To simplify the optimization, the original region is divided into several regions using Algorithm 2 such that each region contains at most $K _ { \mathrm { m a x } }$ TUs. The original region refers to the entire area before the division of the area. In addition, we bid for all regions instead of individual TU, next the UAV serves all TUs in the region and the evaluation metric is the number of secure calculation capacities for TUs in the region. The number of bids is reduced from K to $K _ { a } ,$ where $K _ { a }$ is the number of regions and the a acomputational complexity will be greatly reduced. In JDPB, step 1 is to divide the region into $K _ { a }$ sub-regions by Algorithm a2 and the regions are ranked according to the number of TUs. Step 2 is to initialize the variables. Steps 4â10 are to prepare for bidding, it is checked whether the number of the TUs assigned to each UAV is larger than the maximum number of TUs $K _ { \mathrm { m a x } } ,$ where $G _ { k }$ in step 4 is the number of the TUs in region k. kEligible UAVs participate in the bidding and non-eligible UAVs withdraw from the bidding. The bidding evaluation metric is the number of secure calculation capacities of the TUs, so each UAVâs policy will be optimized in the bid region by Algorithm 3. Steps 11â15 are the bidding process. We denote $\bar { R } _ { k , i } ^ { u }$ as the number of secure calculation capacities of all TUs k,iserved by UAV i in round k. Unlike the GS, the JDPB is a Markov process where the number of secure calculation capacities in round k is relative to round $k - 1$ . So the UAV with the largest difference $\Delta \bar { R } _ { k , i } ^ { u }$ 1in step 11 between the number of TUsâ secure Î k,icalculation capacities in round k and round k â  will win 1the bidding. The winning UAV updates the state each round, including the number of the TUsâ secure calculation capacities $\bar { R } _ { k , i } ^ { u }$ , the location of the TUs and the number of the TUs. When k,iUAV i wins the bidding in round k, the offloading decision $a _ { i j }$ should be set to 1.

## A. Optimizing Resource Allocation and Trajectory Planning

The resource allocation includes the transmission power $p _ { j } [ t ]$ of TU j, the time allocation factor $\tau _ { j , i } [ t ]$ j[ ]and the CPU processing frequency $f _ { i } [ t ]$ j,i[ ]of UAV i. We decouple the subproblem into M i[ ]independent optimization problems, which reduces the number of coupled optimization variables and computational complexity. However, there is still a minimum distance constraint between UAVs. The optimization problem for UAV i is denoted as (P2):

Algorithm 1: JDPB Algorithm for the Optimization Prob  
lem.   
1: divide into $K _ { a }$ regions by Algorthm 2;   
2: a Initialize bidding count $k = 0 ;$ number of TUs served   
by UAV $i , K _ { i } = 0 ; \mathrm { T U } j$ = 0of region k task offloading   
decision $a _ { i j } = 0 ;$   
3: for all $k = \mathrm { 1 } : K _ { a }$ do   
4: =for all $i = 1 : M$ do   
5: if $K _ { i } + G _ { k } \le K _ { \operatorname* { m a x } }$ then   
6: i + k Optimize the transmission power $p _ { j } [ t ] .$ , the   
time allocation factor $\tau _ { j , i } [ t ]$ j [ ], the CPU   
processing frequency ${ \dot { f } } _ { i } [ t ]$ ]and the trajectory   
$q _ { i } [ t ]$ i[ ]by maximizing the number of TUs secure   
i[ ]calculation capacities when UAV i serves   
region k by Algorthm 3;   
7: else   
8: UAV i withdraws from the bidding;   
9: end if   
10: end for   
11: Calculate the number of all TUs secure calculation   
capacities $\bar { R } _ { k , i } ^ { u }$ for region k served by UAV i;   
12: k,i Calculate the secure calculation capacities   
difference relative to the previous bidding:   
$\Delta \bar { R } _ { k , i } ^ { u } = \bar { R } _ { k , i } ^ { u } - \bar { R } _ { k - 1 , i } ^ { u } ,$ where $\bar { R } _ { 0 , i } ^ { u } = 0 ;$   
13: Î k,i = k,i k ,i ,i = 0 Find the UAV with the maximum difference   
$\Delta \bar { R } _ { k , i } ^ { u } \colon i _ { r } = \arg$ max $\Delta \bar { R } _ { k , i } ^ { u } ;$   
14: Î k,i r = arg max Î k,i UAV i serves TU j of region k and sets $a _ { i _ { r } j } = 1 ;$   
15: Update the state of the UAV.   
16: end for

Algorithm 2: TUs Area Division Algorithm.   
1: Initialize division dimension ${ \overline { { A = 1 } } } ;$   
2: Divide the original region into $A \times A$ sub-regions   
averagely;   
3: Calculate the number of TUs in each sub-region and   
get the maximum number of TUs $K ^ { \prime } ;$   
4: if $K ^ { \prime } \le K _ { \operatorname* { m a x } }$ then   
5: Calculate the number of TUs $G _ { k }$ in region $k ,$   
$k \in \{ 1 , 2 , . . . , K _ { a } \}$ k, and determine the TUs locations;   
6: else   
7: $A = A + 1 ;$   
8: = + 1 Back to Step 2;   
9: end if   
10: Sort and number regions by decreasing number of   
TUs.

$$
\begin{array} { r } { ( P 2 ) : \underset { \Theta \backslash \{ a _ { i j } [ t ] \} } { \operatorname* { m a x } } \ \underset { j \in \mathcal { K } } { \operatorname* { m i n } } \ \bar { R } _ { j , i } [ t ] } \\ { \mathrm { s . t . } ( 1 8 \mathrm { c } ) - ( 1 8 \mathrm { k } ) } \end{array}\tag{19a}
$$

$$
\mathrm { s . t . } \sum _ { t = 1 } ^ { N - 1 } \sum _ { j = 1 } ^ { K } E _ { i , j } ^ { c } [ t + 1 ] + \sum _ { t = 1 } ^ { N } E _ { i } ^ { f } [ t ] < \epsilon , \forall j , i , t ,\tag{19b}
$$

Since it is not possible to solve the problem (P2) directly, we introduce the auxiliary variables $s , s _ { j } ^ { 1 } [ t ]$ and $s _ { j } ^ { 2 } [ t ]$ , where j [ ] j [ ]s represents the lower bound of the objective, which aims to maximize the minimum secure calculation capacity, $s _ { j } ^ { 1 } [ t ]$ is the jlower bound of the offloading rate from TU j to UAV i and $s _ { j } ^ { 2 } [ t ]$ j [ ]is the leakage rate from TU j to the eavesdropper. The secure transmission rate $\bar { r } _ { j , i }$ can be expressed as $s _ { j } ^ { 1 } [ t ] - s _ { j } ^ { 2 } [ t ]$ . Thus Â¯j,i j [ ] j [ ]equations (19b), (18i) and (18j) can be replaced by equations (20e), (20f) and (20g), respectively. Then, the optimization variables $Z = \{ p _ { j } [ t ] , \bar { \tau _ { j , i } } [ t ] , \bar { f _ { i } } [ t ] , q _ { i } [ t ] , s , s _ { j } ^ { 1 } [ t ] , s _ { j } ^ { 2 } [ t ] \}$ are equiv-= j[ ] j,alently transformed as

$$
( P 3 ) : \operatorname* { m a x } _ { Z } s\tag{20a}
$$

$$
\mathrm { s . t . } ( 1 8 \mathrm { c } ) - ( 1 8 \mathrm { h } ) , ( 1 8 \mathrm { k } )
$$

$$
s \leq \frac { 1 } { T } \left( \Delta \sum _ { t = 1 } ^ { N } \tau _ { j , i } [ t ] ( s _ { j } ^ { 1 } [ t ] - s _ { j } ^ { 2 } [ t ] ) \right) , \forall j , i , t ,\tag{20b}
$$

$$
s _ { j } ^ { 1 } [ t ] \leq B \log _ { 2 } \left( 1 + \frac { p _ { j } [ t ] g _ { j , i } [ t ] } { N _ { 0 } B } \right) , \forall j , i , t ,\tag{20c}
$$

$$
s _ { j } ^ { 2 } [ t ] \geq B \log _ { 2 } \left( 1 + \frac { p _ { j } [ t ] g _ { j , e } [ t ] } { p _ { s } g _ { s , e } + N _ { 0 } B } \right) , \forall j , e , t ,\tag{20d}
$$

$$
\sum _ { t = 1 } ^ { N - 1 } \sum _ { j = 1 } ^ { K _ { i } } \eta C _ { j } \times \Delta \times \tau _ { j , i } [ t ] ( s _ { j } ^ { 1 } [ t ] - s _ { j } ^ { 2 } [ t ] ) f _ { i } [ t ] ^ { 2 } + \sum _ { t = 1 } ^ { N } E _ { i } ^ { f } [ t ]
$$

$$
< \epsilon , \forall j , i , t ,\tag{20e}
$$

$$
\tau _ { j , i } [ t ] \times \Delta \times ( s _ { j } ^ { 1 } [ t ] - s _ { j } ^ { 2 } [ t ] ) \geq Q _ { j } , \forall j , i , t ,\tag{20f}
$$

$$
f _ { i } [ t ] \geq \sum _ { j = 1 } ^ { K _ { i } } C _ { j } \tau _ { j , i } [ t ] ( s _ { j } ^ { 1 } [ t ] - s _ { j } ^ { 2 } [ t ] ) , \forall j , i , t .\tag{20g}
$$

We decompose into two steps to solve the problem (P3). In step 1, we optimize the variable $\boldsymbol { Z } \backslash q _ { i } [ t ]$ with the given trajectory $\{ q _ { i } [ t ] \}$ i[ ]. And in step 2, we optimize the trajectory $\{ q _ { i } [ t ] \}$ with i[ ]the given $\boldsymbol { Z } \backslash q _ { i } [ t ]$

i[ ]1) Optimizing $Z \backslash q _ { i } [ t ]$ With Given $\{ q _ { i } [ t ] \}$ : For the given trajectory $\{ q _ { i } [ t ] \}$ , the problem (P3) is re-expressed as

$$
\begin{array} { c } { { ( P 4 ) : \displaystyle \operatorname* { m a x } _ { Z \backslash \{ q _ { i } [ t ] \} } s } } \\ { { \mathrm { s . t . } ( 1 8 \mathrm { e } ) - ( 1 8 \mathrm { h } ) , ( 1 9 \mathrm { k } ) , ( 2 0 \mathrm { b } ) - ( 2 0 \mathrm { g } ) } } \end{array}\tag{21}
$$

Problem (P4) is non-convex because of the non-convexity of (19b), (20c), (20d), (20e) and $( 2 0 \mathrm { g } )$ . Then we can solve it using the SCA technique, which approximates the non-convex optimal problems.

For the given transmittion power $p _ { j } [ t ]$ of TU j and computational frequency $f _ { i } [ t ]$ of $\mathrm { U A V } i$ j [ ], the time allocation optimization i[ ]problem is expressed as

$$
\begin{array} { r l r } & { } & { ( P 4 . 1 ) : \qquad \mathrm { m a x } } \\ & { } & { \{ \tau _ { j , i } [ t ] \} , \{ s _ { j } ^ { 1 } [ t ] , s _ { j } ^ { 2 } [ t ] \} } \\ & { } & { \mathrm { s . t . } ( 1 8 \mathrm { f } ) - ( 1 8 \mathrm { h } ) , ( 2 0 \mathrm { b } ) - ( 2 0 \mathrm { g } ) } \end{array}\tag{22}
$$

The constraints are linear for $\tau _ { j , i } [ t ]$ , so (P4.1) is a convex probj,i[ ]lem, which can be solved by standard optimization techniques, such as CVX.

For the given time allocation factor $\tau _ { j , i } [ t ]$ of TU j and the computational frequency $f _ { i } [ t ]$ of $\mathrm { U A V } i ,$ j,i[ ], the transmission power i[ ]optimization problem is expressed as

$$
\begin{array} { r l } & { ( P 4 . 2 ) : \underset { \{ p _ { j } [ t ] \} , \{ s _ { j } ^ { 1 } [ t ] , s _ { j } ^ { 2 } [ t ] \} } { \operatorname* { m a x } } s } \\ & { \mathrm { s . t . } ( 1 8 \mathrm { e } ) , ( 1 8 \mathrm { f } ) , ( 2 0 \mathrm { b } ) - ( 2 0 \mathrm { g } ) } \end{array}\tag{23}
$$

The constraints are linear except for (20c) and (20d). But (20c) and (20d) are non-convex, thus the problem (P4.2) is non-convex and cannot be solved directly. We use the SCA technique to solve it by approximating (P4.2) as a convex problem at each iteration and then obtain the transmission power $p _ { j } [ t ]$ of TU j by iterative updates.

We assume that $\{ p _ { j } ^ { l } [ t ] \}$ is the transmission power after the j [ ]lth iteration of TU j. Using the first-order Taylor expansion to approximate (20c) as a convex function denoted as

$$
s _ { j } ^ { 1 } [ t ] \leq B \log _ { 2 } \left( 1 + \frac { p _ { j } ^ { l } [ t ] g _ { j , i } [ t ] } { N _ { 0 } B } \right)
$$

$$
+ \frac { 1 } { \ln 2 } \frac { g _ { j , i } [ t ] } { N _ { 0 } } \frac { ( p _ { j } [ t ] - p _ { j } ^ { l } [ t ] ) } { ( 1 + \frac { p _ { j } ^ { l } [ t ] g _ { j , i } [ t ] } { N _ { 0 } B } ) } , \forall j , i , t .\tag{24}
$$

Similarly (20d) approximates the convex function denoted as

$$
s _ { j } ^ { 2 } [ t ] \geq B \log _ { 2 } \left( 1 + \frac { p _ { j } ^ { l } [ t ] g _ { j , e } [ t ] } { p _ { s } g _ { s , e } + N _ { 0 } B } \right)
$$

$$
+ \frac { 1 } { \ln 2 } \frac { B g _ { j , e } [ t ] } { p _ { s } g _ { s , e } + N _ { 0 } B } \frac { ( p _ { j } [ t ] - p _ { j } ^ { l } [ t ] ) } { ( 1 + \frac { p _ { j } ^ { l } [ t ] g _ { j , e } [ t ] } { p _ { s } g _ { s , e } + N _ { 0 } B } ) } , \forall j , e , t .\tag{25}
$$

Thus, the problem (P4.2) is reformulated as

$$
( P 4 . 2 . 1 ) : \operatorname* { m a x } _ { \{ p _ { j } [ t ] \} , \{ s _ { j } ^ { 1 } [ t ] , s _ { j } ^ { 2 } [ t ] \} } \ : s\tag{26}
$$

$$
\mathrm { s . t . } ( 1 8 \mathrm { e } ) , ( 1 8 \mathrm { f } ) , ( 2 0 \mathrm { b } ) , ( 2 0 \mathrm { e } ) , ( 2 0 \mathrm { f } ) , ( 2 0 \mathrm { g } ) , ( 2 4 ) , ( 2 5 )
$$

(P4.2.1) is a convex problem that can be solved by standard convex optimization techniques.

For the given time allocation factor $\tau _ { j , i } [ t ]$ and transmission power $p _ { j } [ t ]$ jof TU j, the offloading rate $s _ { j } ^ { 1 } [ t ]$ and the leakage rate $s _ { j } ^ { 2 } [ t ]$ jcan be obtained to find the constraint related to the j [ ]computation frequency $f _ { i } [ t ]$ . The objective is to optimize the i[ ]computation energy consumption of the UAV, independent of the transmission part. Thus the optimization problem is formulated as

$$
( P 4 . 3 ) : \operatorname* { m i n } _ { \{ f _ { i } [ t ] \} } \sum _ { t = 1 } ^ { N - 1 } \sum _ { j = 1 } ^ { K _ { i } } E _ { i , j } ^ { c } [ t + 1 ]\tag{27}
$$

The (20e) is a second-order polynomial for $f _ { i } [ t ]$ , so it is a i[ ]convex function. All other constraints are linear, so (P4.3) is a convex problem. Then we can solve it by the existing convex optimization methods.

2) Optimizing $\{ q _ { i } [ t ] \}$ With Given $Z \backslash q _ { i } [ t ] .$ : For the given time allocation factor $\tau _ { j , i } [ t ]$ i[ ]of TU j, the transmission power $p _ { j } [ t ]$ j,i[ ]and the computation frequency $f _ { i } [ t ]$ j [ ]of UAV i, the optimization problem is formulated as

$$
\begin{array} { c } { { ( P 5 ) : \qquad \mathrm { m a x } } } _ { { \{ q _ { i } [ t ] \} , \{ s _ { j } ^ { 1 } [ t ] , s _ { j } ^ { 2 } [ t ] \} } } ^ { { s } }   \\ { { \mathrm { s . t . } ( 1 8 \mathrm { c } ) , ( 1 8 \mathrm { d } ) , ( 2 0 \mathrm { b } ) - ( 2 0 \mathrm { g } ) } } \end{array}\tag{28}
$$

The nonconvexity of (20c) makes the problem (P5) nonconvex and difficult to solve. It can be solved by the SCA technique, which approximates as a convex problem in each iteration.

We assume that $\{ q _ { i } ^ { l } [ t ] \}$ is the trajectory of UAV i after the lth i[ ]iteration. For (20c), it can be translated as

$$
\begin{array} { r l } & { s _ { j } ^ { 1 } [ t ] \leq B \log _ { 2 } ( ( H ^ { 2 } + \| q _ { i } [ t ] - q _ { j } [ t ] \| ^ { 2 } ) N _ { 0 } B + p _ { j } [ t ] \beta _ { 0 } ) } \\ & { ~ - B \log _ { 2 } ( ( H ^ { 2 } + \| q _ { i } [ t ] - q _ { j } [ t ] \| ^ { 2 } ) N _ { 0 } B ) , \forall j , i , t . } \end{array}\tag{29}
$$

Using the SCA technique, the right-hand side of (29) can be approximated by $B _ { j } ^ { 1 } [ t ] - B _ { j } ^ { 2 } [ t ]$ , where $B _ { j } ^ { 1 } [ t ]$ and $B _ { j } ^ { 2 } [ t ]$ are denoted as

$$
\begin{array} { l } { { B _ { j } ^ { 1 } [ l ] = B \log _ { 2 } ( ( H ^ { 2 } + \| q _ { 1 } ^ { l } [ l ] - q _ { j } [ l ] \| ^ { 2 } ) N _ { 0 } B + p _ { j } [ l ] \beta _ { 0 } ) } } \\ { { \ \ } } \\ { { \ \ } } \\ { { \ \ } + \displaystyle \frac { B } { \ln 2 } \frac { 2 \| q _ { l } ^ { l } [ l ] - q _ { j } [ l ] \| N _ { 0 } B } { ( H ^ { 2 } + \| q _ { l } ^ { l } [ l ] - q _ { j } [ l ] \| ^ { 2 } ) N _ { 0 } B + p _ { j } [ l ] \beta _ { 0 } } }  \\ { { \ } } \\ { { \ \ } } \\ { { \ \ } , { \forall j , i , t , \ } } \\ { { B _ { j } ^ { 2 } [ l ] = B \log _ { 2 } ( ( H ^ { 2 } + \| q _ { 1 } ^ { l } [ l ] - q _ { j } [ l ] \| ^ { 2 } ) N _ { 0 } B ) \ } } \\ { { \ \ } } \\ { { \ \ } } \\ { { \ } + \displaystyle \frac { B } { \ln 2 } \frac { 2 \| q _ { 1 } ^ { l } [ l ] - q _ { j } [ l ] \| N _ { 0 } B ( q _ { k } [ l ] - q _ { l } ^ { l } [ l ] ) } { ( H ^ { 2 } + \| q _ { l } ^ { l } [ l ] - q _ { j } [ l ] \| ^ { 2 } ) N _ { 0 } B } }  \\ { { \ } } \\ { { \ } } \end{array}\tag{30}
$$

31)

Equation (29) is converted as

$$
s _ { j } ^ { 1 } [ t ] \leq B _ { j } ^ { 1 } [ t ] - B _ { j } ^ { 2 } [ t ] , \forall j , t .\tag{32}
$$

For (18c), it can be translated as

$$
\begin{array} { r l } & { \| q _ { i } ^ { l } [ t + 1 ] - q _ { i } [ t ] \| ^ { 2 } + 2 \| q _ { i } ^ { l } [ t + 1 ] - q _ { i } [ t ] \| \| q _ { i } [ t + 1 ] - q _ { i } ^ { l } [ t + 1 ] \| } \\ & { \qquad \quad \geq \Delta ^ { 2 } \times v _ { \operatorname* { m i n } } ^ { 2 } , \forall i , t . \qquad ( 3 } \end{array}\tag{33}
$$

For (18d), it can be translated as

$$
\begin{array} { r l } & { \| q _ { i } ^ { l } [ t ] - q _ { i ^ { \prime } } [ t ] \| ^ { 2 } + 2 \| q _ { i } ^ { l } [ t ] - q _ { i ^ { \prime } } [ t ] \| \| q _ { i } [ t ] - q _ { i } ^ { l } [ t ] \| } \\ & { ~ \geq d ^ { 2 } , \forall i , t . } \end{array}\tag{34}
$$

Thus, problem (P5) can be transformed as

$$
\begin{array} { c } { { ( P 5 . 1 ) : \displaystyle \operatorname* { m a x } _ { \{ q _ { i } [ t ] \} , \{ s _ { j } ^ { 1 } [ t ] , s _ { j } ^ { 2 } [ t ] \} } s } } \\ { { \mathrm { s . t . } ( 1 8 \mathrm { c } ) , ( 2 0 \mathrm { b } ) , ( 2 0 \mathrm { d } ) - ( 2 0 \mathrm { g } ) , ( 3 2 ) - ( 3 4 ) } } \end{array}\tag{35}
$$

(P5.1) is a convex problem, and it can be solved by standard optimization techniques.

To sum up, problem (P2) is solved by the BCD optimization algorithm, as shown in Algorithm 3.

3) Feasibility of the Algorithm 3: In the case of the initialization of the conditions, it is necessary to make sure that the required $Q _ { j }$ is attainable to ensure the feasibility of jAlgorithm 3, so we formulate the problem (P6) as

$$
( P 6 ) : \operatorname* { m a x } _ { \{ Z , Q _ { j } ^ { u } \} } Q _ { j } ^ { u }\tag{36a}
$$

Algorithm 3: BCD-Based Optimization Algorithm.   
1: Initialize Give $\tau _ { j , i } ^ { l } [ t ] , p _ { j } ^ { l } [ t ] , f _ { i } ^ { l } [ t ] , q _ { i } ^ { l } [ t ] .$ , set $l = 0$ and   
j,solution accuracy $\mu , \mu > 0 .$   
2: Repeat   
3: Solve problem (22) by given ${ q } _ { i } ^ { l } [ t ] , { p } _ { j } ^ { l } [ t ] , { f } _ { i } ^ { l } [ t ]$ , and   
obtain time allocation factor $\tau _ { j , i } [ t ]$ [ ] j [ ]solution.   
4: j,i Solve problem (26) by given ${ \bf \dot { \boldsymbol { q } } } _ { i } ^ { l } [ t ] , \boldsymbol { \tau } _ { j , i } ^ { l } [ t ] , f _ { i } ^ { l } [ t ]$ , and   
obtain transmission power $p _ { j } [ t ]$ i[ ] j,solution.   
5: Update $\tau _ { j , i } ^ { l } [ t ] = \dot { \tau } _ { j , i } [ t ] , \dot { p _ { j } ^ { l } } [ t ] = p _ { j } [ t ]$   
6: j,i j Solve problem (27) by given ${ q } _ { i } ^ { l } [ t ] , { \tau } _ { j , i } ^ { l } [ t ] , { p } _ { j } ^ { l } [ t ]$ , and   
obtain computation frequency $f _ { i } [ t ]$ [ ] j,i[ ]solution.   
7: Update ${ \bf \dot { \omega } } _ { f _ { i } ^ { l } [ t ] } = f _ { i } [ t ]$   
8: i [ ] = i[ ] Solve problem (35) by given $\tau _ { j , i } ^ { l } [ t ] , p _ { j } ^ { l } [ t ] , f _ { i } ^ { l } [ t ]$ , and   
obtain UAV trajectory $q _ { i } [ t ]$ j,i[solution.   
9: Update $q _ { i } ^ { l } [ t ] = q _ { i } [ t ] .$   
10: Update $l  l + 1 .$   
11: + 1 Until The target increase is less than Î¼ or l to reach   
maximum number of iterations.   
12: Output $s , s _ { j } ^ { 1 } [ t ] , s _ { j } ^ { 2 } [ t ] , \tau _ { j , i } [ t ] , p _ { j } [ t ] , f _ { i } [ t ] , q _ { i } [ t ] .$

$$
\begin{array} { r l } & { \mathrm { s . t . } ( 1 8 \mathrm { c } ) - ( 1 8 \mathrm { h } ) , ( 1 8 \mathrm { j } ) , ( 1 8 \mathrm { k } ) , ( 1 9 \mathrm { b } ) } \\ & { \quad \tau _ { j , i } [ t ] \times \Delta \times \bar { r } _ { j , i } [ t ] \geq Q _ { j } ^ { u } , \forall j , t , } \end{array}\tag{36b}
$$

where $Q _ { j } ^ { u }$ can be obtained by solving problem (P6). Then the jfeasibility of Algorithm 3 can be easily checked and a more reasonable parameter initialization can be set [43].

## B. Optimizing Offloading Decision $a _ { i j } [ t ]$

The second subproblem is to maximize the minimum secure calculation capacity for all TUs by optimizing the UAV offloading decision $a _ { i j } [ t ]$ . We extract the constraints with $a _ { i j } [ t ]$ ij [ ] ij [ ]in problem (P1) and represent the optimization problem as (P7)

$$
\begin{array} { l } { { ( P 7 ) : \operatorname* { m a x } _ { a _ { i j } [ t ] } \ \operatorname* { m i n } _ { j \in { \mathscr K } } \ a _ { i j } [ t ] { \bar { R } } _ { j , i } [ t ] \ } } \\ { { \mathrm { s . t . } \ \mathrm { ~ } ( 1 8 1 ) , ( 1 8 \mathrm { m } ) , ( 1 8 \mathrm { n } ) } } \end{array}\tag{37a}
$$

In the first subproblem we have obtained the secure calculation capacities of areas served by all UAVs, then we solve the problem (P7) with the bidding algorithm in Algorithm 1.

## C. Complexity of the Algorithm 1

Furthermore, we analyze the complexity of the JDPB. For the first subproblem, the problem is decoupled into M small problems and the time complexity of each small problem is $O ( R )$ , where R is the number of iterations to solve the small ( )problem with Algorithm 3. For the second subproblem, the time complexity is O KM , where K and M are the number of the ( )TUs and the UAVs, respectively. However, because Algorithm 2 zones all TUs, the final time complexity of the first subproblem is $O ( K _ { a } M )$ , where $K _ { a }$ is the number of areas. There are N time ( a ) aslots in the whole problem, so the total time complexity of the problem is $O ( K _ { a } \bar { M } R N )$

TABLE II SIMULATIONS PARAMETERS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>Bandwidth</td><td rowspan=1 colspan=1>1MHz [43]</td></tr><tr><td rowspan=1 colspan=1>n</td><td rowspan=1 colspan=1>Effective switching capacitanceof UAV</td><td rowspan=1 colspan=1> $1 0 ^ { - 2 8 }$ [44]</td></tr><tr><td rowspan=1 colspan=1> $C _ { j }$ </td><td rowspan=1 colspan=1>Number of CPU cycles per bitof data</td><td rowspan=1 colspan=1>1550.7 [44]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N _ { 0 } B } }$ </td><td rowspan=1 colspan=1>Noise power</td><td rowspan=1 colspan=1>-110 dBm [43]</td></tr><tr><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>UAV altitude</td><td rowspan=1 colspan=1>5m [44]</td></tr><tr><td rowspan=1 colspan=1>m</td><td rowspan=1 colspan=1>UAV mass</td><td rowspan=1 colspan=1>9.65kg [44]</td></tr><tr><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>Time slot size</td><td rowspan=1 colspan=1>0.5s [43]</td></tr><tr><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=1>Number of time slots</td><td rowspan=1 colspan=1>20 [43]</td></tr><tr><td rowspan=1 colspan=1>Umax</td><td rowspan=1 colspan=1>Maximum speed</td><td rowspan=1 colspan=1>50m/s [44]</td></tr><tr><td rowspan=1 colspan=1> $v _ { m i n }$ </td><td rowspan=1 colspan=1>Minimum speed</td><td rowspan=1 colspan=1>4m/s[45]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { K } }$ </td><td rowspan=1 colspan=1>Numberof TUs</td><td rowspan=1 colspan=1>45[44]</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>NumberofUAVs</td><td rowspan=1 colspan=1>10 [44]</td></tr><tr><td rowspan=1 colspan=1> $K _ { m a x }$ </td><td rowspan=1 colspan=1>Maximal number of TUper UAV</td><td rowspan=1 colspan=1>5[44]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { d } }$ </td><td rowspan=1 colspan=1>SafedistanceofUAV</td><td rowspan=1 colspan=1>1m</td></tr><tr><td rowspan=1 colspan=1> $p _ { s }$ </td><td rowspan=1 colspan=1>Transmit power of BS</td><td rowspan=1 colspan=1>20dBm[43]</td></tr><tr><td rowspan=1 colspan=1> ${ \underline { { p _ { m a x } } } }$ </td><td rowspan=1 colspan=1>Peak power of TUs</td><td rowspan=1 colspan=1>20dBm[43]</td></tr><tr><td rowspan=1 colspan=1> $Q _ { j }$ </td><td rowspan=1 colspan=1>Required secure computing bitsof TU</td><td rowspan=1 colspan=1>0.5Mbits [43]</td></tr><tr><td rowspan=1 colspan=1>E</td><td rowspan=1 colspan=1>Each UAV energy budget</td><td rowspan=1 colspan=1>30kJ [44]</td></tr></table>

## V. SIMULATION RESULTS

In this section, we evaluate the effectiveness of the proposed scheme by simulation results. Table II shows the parameters of the system. In order to validate the effectiveness of the JDPB, the performance is compared with five other schemes.

Scheme 1: the UAVs fly in a straight line from their respective starting points to the final position reached in scenario 1, and the offloading decision, the transmission power and computation frequency are optimized using JDPB, each TUâs time allocation factor $\tau _ { j , i } [ t ]$ is divided equally.

j,i[ ]Scheme 2: the UAVs fly in a straight line from their respective starting points to the final location reached in scenario 1, and the offloading decision, the time allocation and computation frequency are optimized using JDPB with a fixed power, where the power is fixed as the ratio of $P _ { \mathrm { m a x } }$ to the number of the TUs.

Scheme 3: the UAVs fly in a straight line from their respective starting points to the final location reached in scenario 1, and the offloading decision, the time allocation, power and computation frequency are optimized by using JDPB.

GS: each TU is assigned to the nearest UAV, the offloading decision is obtained based on the communication distance. The time allocation, power allocation, computation frequency and the trajectory are optimized by using Algorithm 3 (BCD-based optimization algorithm).

- RS: each TU is randomly assigned to a UAV. The time allocation, power, computation frequency and the trajectory are optimized by using Algorithm 3 (BCD-based optimization algorithm).

In the simulation scenario, 45 TUs are randomly distributed in original region, where is an area of size $1 0 0 \times 1 0 0 \mathrm { { m ^ { 2 } } }$ . The 100 100coordinates of the region boundaries are [0,0], [0,100], [100,0] and [100,100]. The position of the BS is fixed at [50,50] and the positions of the three eavesdroppers are fixed at [33,33], [66,33] and [50,66], respectively. For the UAVs, we choose two starting point scenario pairs to compare the performance of the proposed algorithm. In the first scenario, the UAVs are initially distributed around the area with each UAV starting at [0,0], [0,33], [0,66], [0,100], [33,100], [66,100], [100,100], [100,66], [100,33] and [100,0]. In the second scenario, the UAVs are initially deployed centrally at the second starting point [0,0]. The initial scenario is displayed in Fig. 3.

<!-- image-->  
Fig. 3. Distribution of TUs, UAVs, eavesdroppers and BS.

In the simulation, because the TUsâ positions change in each time slot, we set the UAVs not to fly towards the landing point, but to optimize the trajectory individually at each time slot. At the end of the flying time T , one or more landing points can be set and the UAVs reserve energy to fly to the landing point for recharging and replenishment.

Applying Algorithm 1, since each UAV can only serve 5 TUs at the same time, we divide 25 sub-regions at the first time slot and 23 of these sub-regions have the TUs. So each UAV will compete for 23 rounds to obtain the optimal offloading decisions. The 23 sub-regions are numbered in order according to the number of the TUs from largest to smallest, as shown in Table III.

Fig. 4 displays the convergence performance of the BCD algorithm for 10 UAVs in the first time slot. The result displays that most of the optimization problems solved by the BCD algorithm can converge. Meanwhile, the sub-regions served by 10 UAVs and the maximized minimum secure calculation capacity and the total TUsâ secure calculation capacity per UAV service are revealed in Table IV. For instance, areas 6, 14, 18 and 19 are allocated to the first UAV. The minimum secure calculation capacity and the sum secure calculation capacity of all TUs in the areas is 2.03 Mbps and 10.1 Mbps, respectively.

Fig. 5 shows the trajectories of UAVs in different scenario. Fig. 5(a) exhibits the trajectories of the UAVs in the first scenario, where the UAVs take off around the region. The flying time, minimum flying speed and UAV energy budget are set to $T = 1 0$ $\mathrm { s } , v _ { \mathrm { m i n } } = 4 \mathrm { m } / \mathrm { s }$ = 10 and E   kJ, respectively. Fig. 5(b) displays = 4 = 30the trajectories of the UAVs in the second scenario, where all the UAVs take off from the same starting point. Due to the high coupling of the UAVs at the distance, the flying time, minimum flying speed and UAV energy budget are set to $T = 1 0 \mathrm { s } , v _ { \mathrm { m i n } } =$ = 10 =m/s and E kJ, respectively. The result shows that the 6 = 50trajectories of the UAVs are close to the TUs served. Because of the different starting points of the UAVs in the two scenarios, when they all take off from the same starting point, the UAVs are easily in collision and therefore need to maintain a safe distances. However, the UAVs that take off from different starting points are not easily in collision, so the trajectories of the UAVs in the two scenarios are different.

<!-- image-->

Fig. 4. Convergence performance of the BCD algorithm for 10 UAVs in the first time slot.  
<!-- image-->  
(a) UAVsâtrajectories in scenario 1.

<!-- image-->  
(b) UAVsâ trajectories in scenario 2.  
Fig. 5. UAVsâ trajectories in different scenario.

TABLE III  
NUMBER OF TUS AND RANGE OF EACH AREA IN THE FIRST TIME SLOT
<table><tr><td rowspan=1 colspan=1>Area no.</td><td rowspan=1 colspan=1>Number of TUs</td><td rowspan=1 colspan=1>Range of area (m)</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>x â[0,20],y â[20,40]</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>x â[60,80],y â[0,20]</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>x â[60,80], y â[80,100]</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>x â[80,100], y â[40,60]</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>x â[20,40],y â[80,100]</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>x â[40,60],y â[0,20]</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>x â[40,60], y â[20,40]</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>x â[40,60],y â[40,60]</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>x â[0,20], y â[60,80]</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>x â[20,40], y â[60,80]</td></tr><tr><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>x â[40,60], y â[60,80]</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>x â[60,80], y â[60,80]</td></tr><tr><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>x â[80,100],y â[80,100]</td></tr><tr><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[20,40], y â[0,20]</td></tr><tr><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[20,40], y â[20,40]</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[60,80],y â[20,40]</td></tr><tr><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[80,100],y â[20,40]</td></tr><tr><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[0,20],y â[40,60]</td></tr><tr><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[20,40],y â[40,60]</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[60,80],y â[40,60]</td></tr><tr><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[80,100], y â[60,80]</td></tr><tr><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[0,20],y â[80,100]</td></tr><tr><td rowspan=1 colspan=1>23</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>x â[40,60],y â[80,100]</td></tr></table>

SUB-AREA OFFLOADING DECISIONS AND MAX-MIN SECURE CALCULATION CAPACITY AND TOTAL TUSâ SECURE CALCULATION CAPACITY PER UAV SERVICE IN THE FIRST TIME SLOT

TABLE IV
<table><tr><td rowspan=1 colspan=1>UAVno.</td><td rowspan=1 colspan=1>Allocatedarea no.</td><td rowspan=1 colspan=1>Max-min securecalculation capacity(Mbps)</td><td rowspan=1 colspan=1>Sum securecalculationcapacity (Mbps)</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>6,14,18,19</td><td rowspan=1 colspan=1>2.03</td><td rowspan=1 colspan=1>10.1</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2.85</td><td rowspan=1 colspan=1>14.2</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>8,13,15</td><td rowspan=1 colspan=1>1.81</td><td rowspan=1 colspan=1>9.03</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>9,22</td><td rowspan=1 colspan=1>4.15</td><td rowspan=1 colspan=1>12.5</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>5,23</td><td rowspan=1 colspan=1>3.53</td><td rowspan=1 colspan=1>14.1</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3.64</td><td rowspan=1 colspan=1>14.6</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>10,11,17</td><td rowspan=1 colspan=1>1.87</td><td rowspan=1 colspan=1>9.37</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>4,21</td><td rowspan=1 colspan=1>3.58</td><td rowspan=1 colspan=1>14.3</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>7,12,16</td><td rowspan=1 colspan=1>1.97</td><td rowspan=1 colspan=1>9.83</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>2,20</td><td rowspan=1 colspan=1>2.18</td><td rowspan=1 colspan=1>10.9</td></tr></table>

Fig. 6 displays the locations of the UAVs and the TUs in some time slots and the divisions of the TUsâ regions in scenario 1, where 6(a) is the 2nd time slot, 6(b) is the 12th time slot and 6(c) is the 19th time slot. The results reveal that each UAV selects a trajectory close to the assigned TUs, although the TUsâ locations change within each time slot resulting in the divisions into different regions.

<!-- image-->  
(a) 2nd time slot

<!-- image-->  
(b) 12th time slot

<!-- image-->  
(c) 19th time slot  
Fig. 6. UAVs and TUsâ locations in partial time slots in scenario 1.

In this experiment, the sum of the average secure calculation capacity of all TUs is expressed as the secure communication capacity of the whole system, and the sum of the average secure calculation capacity of all TUs is the total average secure calculation capacity. Fig. 7 exhibits the variation of the secure communication capacity of the system with the maximum transmission power $P _ { \mathrm { m a x } } .$ It can be seen that the total average secure calculation capacity enhances with the increase of $P _ { \mathrm { m a x } }$ . This is because when $P _ { \mathrm { m a x } }$ grows, the TUs can hold more energy to send more offloading messages. It can be also revealed that the sum average secure calculation capacity decreases as the number of TUs increases. The reason is when the number of the TUs grows, the time allocated to the TUs reduces and the total channel utilization increases, which makes it easy to cause network load and congestion problems, resulting in a decrease of the total throughput.

<!-- image-->  
Fig. 7. Variation of sum average secure calculation capacity with $P _ { \mathrm { m a x } }$

<!-- image-->  
Fig. 8. Variation of sum average secure calculation capacity with $v _ { \mathrm { m i n } }$

Fig. 8 shows the variation of the sum average secure calculation capacity with $v _ { \mathrm { m i n } }$ for different maximum transmission power $P _ { \mathrm { m a x } }$ and different number of TUs. It can be seen that when $v _ { \mathrm { m i n } }$ raises, the sum average secure calculation capacity also increases. This is because when $v _ { \mathrm { m i n } }$ raises, the UAV can reach the TU density area faster, and the TU closer to the UAV can send more offloading information. However, it does not mean that the larger $v _ { \mathrm { m i n } }$ is better. Fig. 9 displays that the sum average flying energy consumption of the UAVs increases as $v _ { \mathrm { m i n } }$ raises, where the sum average flying energy consumption refers to the sum of the average flying energy consumption of all UAVs. When $v _ { \mathrm { m i n } }$ raises, the sum average consumption increases exponentially, which requires more energy budget. In Fig. 9, since the changes on the number of TUs and the maximum transmission power have little effect on the flying rate of the UAV, it can be seen that the energy consumption has minor difference in each case.

<!-- image-->  
Fig. 9. Variation of sum average flying energy consumption with $v _ { \mathrm { m i n } } .$

<!-- image-->  
Fig. 10. Variation of sum average secure throughput with different time slot sizes.

<!-- image-->

Fig. 11. Sum average secure throughput with different time slot sizes in scenario 1.  
<!-- image-->  
Fig. 12. Sum average secure calculation capacity with different $P _ { \mathrm { m a x } }$ in scenario 1.

Fig. 10 exhibits the variation of the sum average secure throughput with  for different maximum transmission power $P _ { \mathrm { m a x } }$ Îand the number of the TUs. Meanwhile, Fig. 10 also shows that the sum average secure throughput of the system increases as the time slot size raises. The reason is when the time slot increases, the TUs can send more offloading messages within a time slot.

Fig. 11 displays the variation of the sum average secure throughput with the time slot size . It can be seen that JDPB Îis better than the other five schemes because JDPB optimizes both resources and trajectories. Furthermore, we use TDMA in JDBP, which reduces the signal interference from other TUs and greatly improves the system secure calculation capacity. Since the RS may assign the UAV to a remote TU, the optimization result of the RS is much smaller than other schemes. In this case, the UAV does not have enough time to approach to the TUs and the TUs cannot offload a large amount of information.

In Fig. 12, we can find that JDPB has the best performance compared with the other five schemes in the case of $P _ { \mathrm { m a x } }$ variation. Since the power in scheme 2 is fixed as the ratio of $P _ { \mathrm { m a x } }$ to the number of the $\mathrm { T U s , }$ the power is also lower when $P _ { \mathrm { m a x } }$ is smaller. So the optimization result of scheme 1 is better than scheme 2 when $P _ { \mathrm { m a x } }$ is lower. But the result of scheme 2 is much superior to scheme 1 when $P _ { \mathrm { m a x } }$ is larger.

<!-- image-->  
Fig. 13. Sum average secure calculation capacity with different $P _ { \mathrm { m a x } }$ in two scenarios.

Fig. 13 exhibits the sum average secure calculation capacity of JDBP and GS scheme, RS scheme under different $P _ { \mathrm { m a x } }$ in scenario 1 and scenario 2. The result shows that JDBP is better than GS scheme and RS scheme at different $P _ { \mathrm { m a x } } .$ . Furthermore, we can see the different performances for two scenarios. In scenario 1, JDPB is slightly superior to GS scheme and far better than RS scheme. In scenario 2, JDBP is much superior to GS scheme and RS scheme, while the optimization results of GS scheme and RS scheme have slight difference. And in scenario 2, the disadvantage of GS scheme that assigning TUs to the nearest UAV is revealed. Compared with scenario 1 where the UAVs are distributed around the region with a wider distribution, in scenario 2 for the TUs, the UAVs are deployed at the same starting point [0,0] with a smaller initial distribution and the distance from a TU to all UAVs is the same. Consequently, the GS scheme can randomly assign the TUs to one UAV instead of assigning them based on the distance between the TU and the UAV. So the performance of the GS scheme is the same as the RS scheme. The results prove that the JDPB algorithm is more robust than the GS.

## VI. CONCLUSION

In this paper, a joint optimization algorithm JDPB is proposed to solve the task offloading, resource allocation and trajectory planning problems, where the TUs move with a Gauss-Markov random model. The objective is to maximize the minimum secure calculation capacity of the TUs and we decompose the original optimization problem into two subproblems. Due to the non-convexity of the resource allocation and the flying trajectory of the UAV problem, we use the SCA and BCD algorithms to optimize the first subproblem. Then we utilize bidding method to optimize task offloading in the second subproblem. Comparing with other schemes, JDPB has better performance in sum average secure calculation capacity and sum average secure throughput.

In future work, we will expand this work. First, if a more realistic scenario is to be considered, it is necessary to include weather factors or air resistance in the communication model. Second, in order to make the range of the UAVs more extensive, it is an interesting problem how to solve the 3-dimensional trajectory of the UAVs. Third, introducing blockchain technology between UAVs can further guarantee data privacy and security.

## REFERENCES

[1] M. Liu, G. Feng, Y. Sun, N. Chen, and W. Tan, âA network function parallelism-enabled MEC framework for supporting low-latency services,â IEEE Trans. Services Comput., vol. 16, no. 1, pp. 40â52, Jan./Feb. 2023.

[2] J. Shi, Y. Zhou, Z. Li, Z. Zhao, Z. Chu, and P. Xiao, âDelay minimization for NOMA-mmW scheme-based MEC offloading,â IEEE Internet Things J., vol. 10, no. 3, pp. 2285â2296, Feb. 2023.

[3] L. Tan, Z. Kuang, J. Gao, and L. Zhao, âEnergy-efficient collaborative multi-access edge computing via deep reinforcement learning,â IEEE Trans. Ind. Informat., vol. 19, no. 6, pp. 7689â7699, Jun. 2023.

[4] Q. Zhang, Y. Wang, H. Li, S. Hou, and Z. Song, âResource allocation for energy efficient STAR-RIS aided MEC systems,â IEEE Wireless Commun. Lett., vol. 12, no. 4, pp. 610â614, Apr. 2023.

[5] J. Gao, Z. Kuang, J. Gao, and L. Zhao, âJoint offloading scheduling and resource allocation in vehicular edge computing: A two layer solution,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 3999â4009, Mar. 2023.

[6] B. Liu, Y. Wan, F. Zhou, Q. Wu, and R. Q. Hu, âResource allocation and trajectory design for MISO UAV-Assisted MEC networks,â IEEE Trans. Veh. Technol., vol. 71, no. 5, pp. 4933â4948, May 2022.

[7] N. Nouri, F. Fazel, J. Abouei, and K. N. Plataniotis, âMulti-UAV placement and user association in uplink MIMO ultra-dense wireless networks,â IEEE Trans. Mobile Comput., vol. 22, no. 3, pp. 1615â1632, Mar. 2023.

[8] K. Zhang, X. Gui, D. Ren, and D. Li, âEnergyâlatency tradeoff for computation offloading in UAV-Assisted multiaccess edge computing system,â IEEE Internet Things J., vol. 8, no. 8, pp. 6709â6719, Apr. 2021.

[9] B. Xu, Z. Kuang, J. Gao, L. Zhao, and C. Wu, âJoint offloading decision and trajectory design for UAV-enabled edge computing with task dependency,â IEEE Trans. Wireless Commun., vol. 22, no. 8, pp. 5043â5055, Aug. 2022.

[10] M. A. Hossain, A. R. Hossain, and N. Ansari, âNumerology-capable UAV-MEC for future generation massive IoT networks,â IEEE Internet Things J., vol. 9, no. 23, pp. 23860â23868, Dec. 2022.

[11] H. Mei, K. Yang, J. Shen, and Q. Liu, âJoint trajectory-task-cache optimization with phase-shift design of RIS-Assisted UAV for MEC,â IEEE Wireless Commun. Lett., vol. 10, no. 7, pp. 1586â1590, Jul. 2021.

[12] L. Tan, Z. Kuang, L. Zhao, and A. Liu, âEnergy-efficient joint task offloading and resource allocation in OFDMA-Based collaborative edge computing,â IEEE Trans. Wireless Commun., vol. 21, no. 3, pp. 1960â1972, Mar. 2022.

[13] X. Gu, G. Zhang, M. Wang, W. Duan, M. Wen, and P.-H. Ho, âUAV-Aided energy-efficient edge computing networks: Security offloading optimization,â IEEE Internet Things J., vol. 9, no. 6, pp. 4245â4258, Mar. 2022.

[14] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for uav-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[15] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âCellular-connected Multi-UAV MEC networks: An online stochastic optimization approach,â IEEE Trans. Commun., vol. 70, no. 10, pp. 6630â6647, Oct. 2022.

[16] S. Zhu, L. Gui, D. Zhao, N. Cheng, Q. Zhang, and X. Lang, âLearningbased computation offloading approaches in UAVs-Assisted edge computing,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 928â944, Jan. 2021.

[17] Y. Yu, X. Bu, K. Yang, H. Yang, X. Gao, and Z. Han, âUAV-Aided low latency multi-access edge computing,â IEEE Trans. Veh. Technol., vol. 70, no. 5, pp. 4955â4967, May 2021.

[18] H. Wu, J. Chen, T. N. Nguyen, and H. Tang, âLyapunov-guided delayaware energy efficient offloading in IIoT-MEC systems,â IEEE Trans. Ind. Informat., vol. 19, no. 2, pp. 2117â2128, Feb. 2023.

[19] Y. K. Tun, T. N. Dang, K. Kim, M. Alsenwi, W. Saad, and C. S. Hong, âCollaboration in the sky: A distributed framework for task offloading and resource allocation in multi-access edge computing,â IEEE Internet Things J., vol. 9, no. 23, pp. 24221â24235, Dec. 2022.

[20] Y. Liu, J. Yan, and X. Zhao, âDeep reinforcement learning based latency minimization for mobile edge computing with virtualization in maritime UAV communication network,â IEEE Trans. Veh. Technol., vol. 71, no. 4, pp. 4225â4236, Apr. 2022.

[21] G. Zheng, C. Xu, M. Wen, and X. Zhao, âService caching based aerial cooperative computing and resource allocation in multi-UAV enabled MEC systems,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 10934â10947, Oct. 2022.

[22] J. Chen et al., âA multi-leader multi-follower stackelberg game for coalition-based UAV MEC networks,â IEEE Wireless Commun. Lett., vol. 10, no. 11, pp. 2350â2354, Nov. 2021.

[23] Q. Chen, Z. Kuang, and L. Zhao, âMultiuser computation offloading and resource allocation for cloudâedge heterogeneous network,â IEEE Internet Things J., vol. 9, no. 5, pp. 3799â3811, Mar. 2022.

[24] Q. Wu et al., âJoint computation offloading, role, and location selection in hierarchical multicoalition UAV MEC networks: A stackelberg game learning approach,â IEEE Internet Things J., vol. 9, no. 19, pp. 18293â 18304, Oct. 2022.

[25] L. Zhang and N. Ansari, âOptimizing the operation cost for UAV-aided mobile edge computing,â IEEE Trans. Veh. Technol., vol. 70, no. 6, pp. 6085â6093, Jun. 2021.

[26] Z. Kuang, L. Li, J. Gao, L. Zhao, and A. Liu, âPartial offloading scheduling and power allocation for mobile edge computing systems,â IEEE Internet Things J., vol. 6, no. 4, pp. 6774â6785, Aug. 2019.

[27] P. A. Apostolopoulos, G. Fragkos, E. E. Tsiropoulou, and S. Papavassiliou, âData offloading in UAV-Assisted multi-access edge computing systems under resource uncertainty,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 175â190, Jan. 2023.

[28] Q. Liu, L. Shi, L. Sun, J. Li, M. Ding, and F. Shu, âPath Planning for UAV-Mounted mobile edge computing with deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 69, no. 5, pp. 5723â5728, May 2020.

[29] Z. Yang, S. Bi, and Y.-J. A. Zhang, âOnline trajectory and resource optimization for stochastic UAV-Enabled MEC systems,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5629â5643, Jul. 2022.

[30] S. Yin, S. Zhao, Y. Zhao, and F. R. Yu, âIntelligent trajectory design in UAV-Aided communications with reinforcement learning,â IEEE Trans. Veh. Technol., vol. 68, no. 8, pp. 8227â8231, Aug. 2019.

[31] R. Khan, P. Kumar, D. N. K. Jayakody, and M. Liyanage, âA survey on security and privacy of 5G technologies: Potential solutions, recent advancements, and future directions,â IEEE Commun. Surveys Tuts., vol. 22, no. 1, pp. 196â248, First Quarter 2020.

[32] W. Lu et al., âResource and trajectory optimization for secure communications in dual unmanned aerial vehicle mobile edge computing systems,â IEEE Trans. Ind. Informat., vol. 18, no. 4, pp. 2704â2713, Apr. 2022.

[33] W. Lu et al., âSecure NOMA-Based UAV-MEC network towards a flying eavesdropper,â IEEE Trans. Commun., vol. 70, no. 5, pp. 3364â3376, May 2022.

[34] M. Hua, Y. Wang, Q. Wu, H. Dai, Y. Huang, and L. Yang, âEnergyefficient cooperative secure transmission in Multi-UAV-Enabled wireless networks,â IEEE Trans. Veh. Technol., vol. 68, no. 8, pp. 7761â7775, Aug. 2019.

[35] N. Zhao et al., âUAV-Assisted emergency networks in disasters,â IEEE Wireless Commun., vol. 26, no. 1, pp. 45â51, Feb. 2019.

[36] S. Batabyal and P. Bhaumik, âMobility models, traces and impact of mobility on opportunistic routing algorithms: A survey,â IEEE Commun. Surveys Tuts., vol. 17, no. 3, pp. 1679â1707, Third Quarter 2015.

[37] M. M. Azari et al., âEvolution of non-terrestrial networks from 5G to 6G: A survey,â IEEE Commun. Surveys Tuts., vol. 24, no. 4, pp. 2633â2672, Fourth Quarter 2022.

[38] F. Zhou, Y. Wu, R. Q. Hu, and Y. Qian, âComputation rate maximization in UAV-enabled wireless-powered mobile-edge computing systems,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1927â1941, Sep. 2018.

[39] Q. Hu, Y. Cai, G. Yu, Z. Qin, M. Zhao, and G. Y. Li, âJoint offloading and trajectory design for UAV-enabled mobile edge computing systems,â IEEE Internet Things J., vol. 6, no. 2, pp. 1879â1892, Apr. 2019.

[40] T. Zhang, Y. Xu, J. Loo, D. Yang, and L. Xiao, âJoint computation and communication design for UAV-assisted mobile edge computing in IoT,â IEEE Trans. Ind. Informat., vol. 16, no. 8, pp. 5505â5516, Aug. 2020.

[41] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and L. Hanzo, âMulti-agent deep reinforcement learning-based trajectory planning for multi-UAV assisted mobile edge computing,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 1, pp. 73â84, Mar. 2021.

[42] Y. Zhou et al., âSecure communications for UAV-enabled mobile edge computing systems,â IEEE Trans. Commun., vol. 68, no. 1, pp. 376â388, Jan. 2020.

[43] Y. Xu, T. Zhang, D. Yang, Y. Liu, and M. Tao, âJoint resource and trajectory optimization for security in UAV-Assisted MEC systems,â IEEE Trans. Commun., vol. 69, no. 1, pp. 573â588, Jan. 2021.

[44] Y. Luo, W. Ding, and B. Zhang, âOptimization of task scheduling and dynamic service strategy for multi-UAV-enabled mobile-edge computing system,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 3, pp. 970â984, Sep. 2021.

[45] C. Zhan, H. Hu, X. Sui, Z. Liu, and D. Niyato, âCompletion time and energy optimization in the UAV-enabled mobile-edge computing system,â IEEE Internet Things J., vol. 7, no. 8, pp. 7808â7822, Aug. 2020.

<!-- image-->

Yuhao Zhang received the BEng degree in computer science and technology from the Central South University of Forestry and Technology. He is currently working toward the MEng degree in software engineering with the Central South University of Forestry and Techology. His current research interests include mobile edge computing, optimization algorithm and its application.

<!-- image-->

Zhufang Kuang (Member, IEEE) received the MSc and PhD degrees in computer science from the National University of Defense Technology and Central South University, Changsha, China, 2006 and 2012, respectively. He was a post-doctoral researcher with the School of Software, Central South University, Changsha, China. From 2015 to 2016. He was a visiting scholar/professor with the University of Victoria, Victoria, BC, Canada. He is currently a full professor with the Department of Computer Science and Technology, Central South University of Forestry

and Technology. His current research interests include wireless communications and networking, Internet of Things (IoTs), mobile edge computing, artificial intelligence. He is a distinguished member of CCF, a member of the CCF Internet of Things Council and a member of the CCF Network and Data Communications Council, and ACM. He is a chair of CCF YOCSEF CHANGSHA from 2022 to 2023.

<!-- image-->

Yanyan Feng received the BS degree from Henan University, in 2014, and the MS and PhD degrees from Central South University, in 2017 and 2021, respectively. Currently, she is an associate professor with the College of Electronic Information and Physics, Central South University of Forestry and Technology, Changsha, China. Her research interests mainly include quantum communication, quantum cryptography and quantum machine learning, Internet of Things.

<!-- image-->

Fen Hou (Member, IEEE) received the PhD degree in electrical and computer engineering from the University of Waterloo, Waterloo, Canada, in 2008. She is currently an associate professor with the State Key Laboratory of IoT for Smart City, the Department of Electrical and Computer Engineering, and the GuangdongâHong KongâMacau Joint Laboratory for Smart Cities, University of Macau. Her research interests include resource allocation intelligent computing networks, mechanism design, and optimal user behavior in crowd sensing networks. She was a corecipient of the IEEE Globecom Best Paper Award, in 2010, the Distinguished Service Award in the IEEE MMTC, in 2011, and the IEEE VTC-Fall Best Student Paper Award, in 2021. She served as the TPC chair and the co-chair for several IEEE conferences, such as ICCS 2014, INFOCOM 2014, ICCC 2015, ICC 2016, and ICCC 2021. She currently serves as an associate editor of IET Communications and IEEE Communications Surveys and Tutorials.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC/page_14_img_1.jpeg|page_14_img_1]]
3. [[../extracted_images/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC/page_14_img_2.jpeg|page_14_img_2]]
4. [[../extracted_images/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC/page_14_img_3.jpeg|page_14_img_3]]
5. [[../extracted_images/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC/page_14_img_4.jpeg|page_14_img_4]]

---

