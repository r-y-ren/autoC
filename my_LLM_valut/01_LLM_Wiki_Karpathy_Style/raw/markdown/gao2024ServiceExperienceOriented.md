# Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks

Xingxia Gao , Graduate Student Member, IEEE, and Linbo Zhai , Member, IEEE

AbstractâThe unmanned aerial vehicle (UAV)-enabled multiaccess edge computing (MEC) technology is opening up new opportunities in the integrated space-air-ground in the 5G era and beyond. However, providing low-latency services solely from an overall perspective cannot ensure a high quality of experience (QoE) for user equipments (UEs). Therefore, we propose a service experience-oriented cooperative caching framework, where the UAVs can effectively serve each UE by providing communication and computing resources. A novel metric called service experience ratio is defined to reflect the experience at the UEs. Under the constraints of UAVâs energy budget and delay requirements, we consider jointly optimizing task offloading, resource allocation, trajectory planning, and service caching placement to maximize the service experience ratio. Since the original problem is a mixedinteger non-convex programming problem with a fractional structure, it is challenging to be solved in polynomial time. Based on Dinkelbachâs method and convex optimization theory, we simplify the problem model and propose a four-stage alternating iterative service ratio maximization algorithm to solve this problem. Besides, we also analyze the convergence and complexity of our proposed algorithm. Numerical results demonstrate that the service experience ratio achieved by the proposed algorithm is 19â34% higher than the comparative works.

Index TermsâCaching placement, edge computing, resource allocation, task offloading, UAV trajectory.

## I. INTRODUCTION

I N RECENT years, with the development and popularizationof mobile communication technology, many new applica- of mobile communication technology, many new applications such as online video, map navigation, mobile payment, and face recognition have emerged [1]. Subsequently, the proliferation of intelligent devices connected to the network has led to an explosive growth of data. At the same time, in emergencies such as the COVID-19, face-to-face communication between people has become difficult, and dependence on online medicine, online learning and remote work has increased significantly. The above applications are usually delay-sensitive and require enormous communication and computation resources. To support a large number of intelligent devices and process a large amount of data in a timely manner, multiple access edge computing (MEC), formerly known as mobile edge computing, has become a key technology in the next-generation wireless network [2].

Nevertheless, the current edge computing system also has many problems. Terrestrial MEC servers with fixed locations cannot be adjusted according to the requirements of user equipments (UEs). They may have poor channel quality due to the non-Line-of-Sight (NLoS) links, which leads to limited communication rate [3]. Worse still, due to severe obstruction or damage caused by natural disasters, some UEs can be abstained from MEC services [4]. Recently, the unmanned aerial vehicle (UAV) has emerged as a promising technology to improve wireless connectivity and provide extensive coverage in MEC networks thanks to the advantages of flexible deployment and low-cost [5]. Typically, there are two technologies for UAV-enabled MEC networks, where the UAV acts as the aerial relay [6], [7] and the aerial MEC [8]. Besides, with the rapid increase of UEs, single or even multiple UAVs [9] may not be able to meet the demands of massive computation-intensive and delay-sensitive applications, such as virtual reality and intelligent transportation. Therefore, in UAV-assisted MEC networks, terrestrial MEC base stations (BSs) still exist. Given the potential of utilizing the communication and computation resources in both UAVs and ground BSs, the air-ground cooperation model provides new opportunities for the development of real-time applications in future wireless networks.

Although many scholars have studied cooperative MEC networks including multiple UAVs and ground BSs, there are still some unprecedented challenges in improving UEâs service experience: (i) compared to networks that only include ground MEC servers, there are limited computing, bandwidth and energy resources in UAV-assisted MEC networks. Hence, it is necessary to design a collaborative task offloading strategy to efficiently utilize resources; (ii) although the flexibility of UAVs brings more possibilities to MEC networks, the coupling of variables such as task offloading and resource allocation also makes UAV trajectory planning more complex [10], and there is still a paucity of research on joint optimization of task offloading, trajectory planning, caching placement, and resource allocation for cacheenabling UAV networks; (iii) many emerging applications are data-driven, and frequent downloading service contents from cloud servers will bring huge time and cost expenses [11]. The UAVs which cache the related databases and corresponding programs in advance can efficiently execute the computation tasks generated by UEs [12]. Most of the existing works focus on computation content caching in UAV-assisted MEC systems, and some works have studied computation service caching in multi-UAV deployment scenarios, where the location of each UAV is fixed. However, so far only a few works consider computation service caching in the dynamic UAV networks; (iv) a lot of existing optimization goals that only ensure overall service quality may leads to unfair treatment of some UEs, which will result in poor service experience of these UEs.

<!-- image-->  
Fig. 1. Illustration of UAV-assisted wireless network.

The aforementioned research works have laid solid foundations on UAV-enabled MEC networks. Motivated by the issues discussed above, we study a multi-UAV-enabled MEC networks where cellular-connected UAVs are considered to provide MEC services or used as relays to fully exploit the system resources. To reduce the service delay while guaranteeing the fairness among UEs, we study the service experience ratio of UEs via supporting both horizontal collaboration among UAVs and vertical collaboration between UAVs and the BS. To maximize the service experience ratio, we jointly optimize the service caching placement, task offloading, computation and communication resources allocation, and UAV trajectory under the constraints of UAVâs energy and multi-dimensional (storage, computation, and communication) resources. The main contributions are summarized as follows.

1) Considering the strict requirements for service delay and the fairness among all UEs, the service experience ratio is designed as the ratio of the fairness index to total service delay. We propose a service experience ratio maximization problem in multi-UAV assisted MEC networks, which is proven to be NP-hard.

2) We reformulate the service experience ratio maximization problem to a parametric programming form using the Dinkelbachâs method. Then, we decompose the problem into four sub-optimization problems. A joint alternating iterative optimization algorithm is designed to obtain the optimal solution. To be specific, we first propose a satisfaction-based optimization algorithm to solve the task offloading subproblem. Next, a priority-aware optimization algorithm is developed to solve the service caching subproblem. Then, the successive convex approximation (SCA) technique is employed to optimize the UAVâs trajectory. Besides, the computation and communication resources allocation are optimized by employing the standard convex tools.

3) Numerical results show that an appropriate trade-off between service delay and fairness among all UEs can be made, which verifies the effectiveness of our proposed algorithm. Moreover, the proposed algorithm outperforms the other three state-of-art baselines in maximizing the service experience ratio.

We organize the rest of this paper as follows. Section II describes the related work. Section III introduces the system model. In Section IV, we formulate the service experience ratio maximization problem. In Section V, the joint alternating optimization algorithm is proposed to solve the formulated problem. Simulation results and analysis are presented in Section VI. Finally, Section VII concludes this paper.

## II. RELATED WORK

Plenty of research works have been recently devoted to the field of MEC. According to the status of MEC servers, we can categorize them into two types. In particular, one mainly studies the static MEC servers connected with BSs [13], [14], while the other focuses on the mobile MEC servers mounted on dynamic wireless communication platforms, such as UAVs [15]. Recently, UAV-assisted MEC networks have attracted widespread attention due to the advantages of flexibility and operability [16]. The UAV can be integrated with MEC servers [8] and serve as mobile relay [17] for computation offloading, and it can be used as data collector [18].

However, due to the size constraints and limited resources of UAVs, only depending on UAVs to provide MEC services for UEs poses risks. Accordingly, many scholars have studied the networks that simultaneously include ground BSs and multiple UAVs integrating with MEC servers. Zhang et al. [19] proposed a new framework of UAV-assisted MEC system in IoT where the tasks generated by UEs were computed locally or offloaded to the UAV. Deng et al. [20] studied MEC for artificial intelligence (AI) applications in air-ground-integrated wireless networks. The above works either considered a single UAV or only enabled multiple UAVs to work independently in the MEC networks. Instead, excellent collaboration between the UAVs can effectively utilize resources to perform offloading and balance the load among UAVs.

The works of UAV-assisted MEC network mainly focus on task offloading, resource allocation, trajectory planning, and service caching placement. In terms of task offloading, He et al. [21] proposed a multi-hop task offloading with on-the-fly computation scheme, which allowed multiple UAVs to form an aerial computing network. In terms of resource allocation, Liu et al. [22] formulated a fair energy-efficient resource optimization problem. In terms of trajectory planning, Miao et al. [23] raised a multi-UAV-assisted MEC offloading algorithm based on global and local path planning controlled by ground station and onboard computer. Moreover, Li et al. [24] studied an energy efficient scheduling system that allowed UAVs to determine their trajectories. In terms of service caching placement, Zhang et al. [25] studied the joint optimization of UAV deployment, caching placement and user association for maximum quality of experience (QoE) of UEs, and Zhou et al. [26] made caching placement decision every T time slots based on the interior point method to reduce the caching overhead. However, few works considered the joint optimization of task offloading, resource allocation, trajectory planning, and service caching.

Most research works are dedicated to optimizing energy consumption, system throughput, task processing latency, and weighted sum of energy consumption and latency in UAV-aided MEC networks. Mao et al. [27] and Qian et al. [28] proposed energy consumption minimization problem by jointly optimizing the trajectory of UAV and the transmit power of each UE. Ning et al. [29] designed a 5G-enabled UAV-to-community offloading system, with the goal of maximizing the system throughout. Nguyen et al. [30] aimed to minimize the average latency of UEs by jointly controlling the offloading decision for dependent tasks and allocating the communication resources of UAVs. In order to minimize the weighted sum cost of latency and energy consumption, Liu et al. [31] jointly optimized the caching and offloading decisions, the edge UAVs deployment, and the radio and computation resource allocation. Based on the broad overview of existing researches, few works have been dedicated to tackling the service experience ratio. In other words, the research of reducing service latency while ensuring fairness among UEs has rarely been studied.

Different from the existing works, we study a collaborative task offloading framework in which the UAV executes the tasks generated by associated UEs, or further relays them to other collaborative UAVs and the macro base station (MBS). Besides, we develop a service experience ratio maximization problem by jointly optimizing task offloading, resource allocation, trajectory planning, and service caching placement. Then, we decompose the problem into four subproblems and tackle it by a four-stage alternating iterative algorithm.

## III. SYSTEM MODEL

We consider a cellular wireless network as shown in Fig. 1, which consists of one MBS, U rotary-wing UAVs and M UEs, denoted by $b , \ u \in \mathcal { U } = \{ 1 , 2 , . . . , U \}$ and $m \in \mathcal { M } =$ $\{ 1 , 2 , . . . , M \}$ = 1 2 =, respectively. The rotary-wing UAVs are adopted 1 2since they can move flexibly and hover over fixed locations. The UAVs, integrating with MEC servers, have certain communication, computing, and storage (CCS) resources but subject to the size, weight, and power (SWAP) limitations. Unlike UAVs, the MBS, which has more CCS resources, is composed of ground MEC servers. The UEs are unable to establish wireless communication with the MBS due to signal congestion and shadowing, or the low communication quality [32]. Hence, UEs can only establish communication connection with MBS through UAVs. The UAV connects with the MBS through a wireless backhaul link. Each UE transmits offloading data to the UAV via wireless uplink. In Fig. 1, considering the service caching, the task can be offloaded to the UAV only when two conditions are satisfied: i) the corresponding service is cached in the UAV; ii) the UAV can provide sufficient computing and communication resources.

Due to limited computation capacities, UEs do not execute local computing. Thus, the MBS and all UAVs cooperatively provide MEC services for UEs. Let $\mathcal { S } = \{ 1 , 2 , . . . , S \}$ denote = 1 2the all services provided by the MBS. Each UAV can only storage partial services in set S because of limited storage space. The connection between UEs and UAVs can remain stable in a sufficiently short period of time. For simplicity, we divide the task period N into T time slots with equal duration $\Delta _ { t }$ , i.e., $N = \Delta _ { t } T$ and $t \in \mathcal { T } = \{ 1 , 2 , . . . , T \}$ Î. Each UE can generate = Î = 1 2only one task within one time slot, and each task is atomic and unsplit [29]. Let $V _ { m , s } ^ { t }$ denote the task generated from UE m requiring service s at time slot t, which can be modeled as a triplet $< { \cal I } _ { m , s } ^ { t } , W _ { m , s } ^ { t } , D _ { m , s } ^ { t } >$ , where $I _ { m , s } ^ { t }$ denotes the input data size of the task, $W _ { m , s } ^ { t }$ represents the total required computing resources to accomplish the task, and $D _ { m , s } ^ { t }$ denotes the maximum tolerable delay, beyond which the results are invalid for UE m. Let $V ^ { t }$ denote the set of all UEsâ tasks at time slot t.

In the scheduling process of UAVs, software-defined network (SDN) acts as a control center for UAVs [33]. The global information of the system, including each UAVâs location, speed, and the channel state information between the UAVs, can be obtained through the SDN controller. If some UAVs lose their connection, we can deploy new UAVs to provide support.

## A. UAV Mobility Model

Since the length of each time slot is small enough, each UAV can be considered static within each time slot. Hence, the trajectory of each UAV during the entire task execution cycle can be regarded as a sequence of discrete points. All UAVs fly at a fixed altitude of $h ,$ which allows them to avoid frequent ascent and descent to evade obstacles. Considering a three-dimensional (3D) Cartesian coordinate system, the horizontal coordinate of UAV u at time slot t is denoted by $\boldsymbol { Q } _ { u } ^ { t } = ( x _ { u } ^ { t } , y _ { u } ^ { t } )$ . The trajectory of UAV u can be described as $Q _ { u } = \{ Q _ { u } ^ { 1 } , . . . , Q _ { u } ^ { T } \}$ Then, let $Q = \{ Q _ { 1 } , . . . , Q _ { U } \}$ =denote the trajectories of all UAVs. =Similarly, the horizontal coordinates of the active MBS b and UE m can be denoted as $Q _ { b } = ( x _ { b } , y _ { b } )$ and $Q _ { m } = ( x _ { m } , y _ { m } )$ respectively.

To enhance coverage, the flight trajectory of each UAV should be within the target area [34], which is defined as $[ 0 , x _ { \mathrm { m a x } } ] \times$ $[ 0 , y _ { \mathrm { m a x } } ] . \operatorname { L e t } v _ { \mathrm { m a x } }$ represent the UAVâs maximum speed. In time [0 ]slot t, in order to avoid signal interference and ensure collision avoidance among UAVs, any two UAVs should keep a minimal safe distance denoted by $d _ { \mathrm { m i n } }$ . For instance, the distance between UAV u and UAV i is not less than $d _ { \mathrm { m i n } }$ . At the end of a cycle, the UAV returns to its original location. Accordingly, we obtain the following trajectory constraints:

$$
\left\{ \begin{array} { l l } { 0 \leq x _ { u } ^ { t } \leq x _ { \operatorname* { m a x } } , \quad \forall u \in \mathcal { U } , \forall t \in \mathcal { T } , } \\ { 0 \leq y _ { u } ^ { t } \leq y _ { \operatorname* { m a x } } , \quad \forall u \in \mathcal { U } , \forall t \in \mathcal { T } , } \\ { | | Q _ { u } ^ { t + 1 } - Q _ { u } ^ { t } | | \leq v _ { \operatorname* { m a x } } \Delta _ { t } , \quad \forall t \in \mathcal { T } , } \\ { | | Q _ { u } ^ { t } - Q _ { i } ^ { t } | | \geq d _ { \operatorname* { m i n } } , \quad \forall u \in \mathcal { U } , \forall i \in \mathcal { U } \setminus \{ u \} , \forall t \in \mathcal { T } , } \\ { Q _ { u } ^ { 1 } = Q _ { u } ^ { T } , \quad \forall u \in \mathcal { U } . } \end{array} \right.\tag{1}
$$

## B. Communication Model

Based on the Orthogonal Frequency Division Multiple Access (OFDMA) technique [35], the interference among UEs in wireless uplink can be ignored. Due to the distance limitation of signal transmission, UAV u can only provide MEC services to UEs within the coverage range denoted by $R _ { u } .$ . In time slot t, the horizontal distance between UE m and UAV u is $d _ { m , u } ^ { t } = \sqrt { ( x _ { m } ^ { t } - x _ { u } ^ { t } ) ^ { 2 } + ( y _ { m } ^ { t } - y _ { u } ^ { t } ) ^ { 2 } }$ . Similarly, $d _ { u , b } ^ { t } =$ $\sqrt { ( x _ { u } ^ { t } - x _ { b } ^ { t } ) ^ { 2 } + ( y _ { u } ^ { t } - y _ { b } ^ { t } ) ^ { 2 } }$ is the horizontal distance between ( ) + ( )UAV u and MBS b at time slot t.

Let $b _ { m , u } ^ { t } \in [ 0 , 1 ]$ denote the bandwidth resource allocated [0 1]by UAV u to UE m at time slot t. Then, we use the variable $B = \{ b _ { m , u } ^ { t } | m \in \mathcal { M } , u \in \mathcal { U } , t \in \mathcal { T } \}$ to indicate the bandwidth =resource allocation decisions. Due to the obstacles in the environment, the Ground-to-Air (G2A) and Air-to-Ground (A2G) channels may be either Line-of-Sight (LoS) or NLoS. According to [36], the LoS probability between UE m and UAV u is expressed as

$$
\begin{array} { l } { \displaystyle P _ { L o S } ( { d } _ { m , u } ^ { t } ) } \\ { = \frac 1 { 1 + \beta _ { 0 } \exp \left( - \beta _ { 1 } \left( \frac { 1 8 0 } { \pi } \arcsin \left( \frac { h } { { d } _ { m , u } ^ { t } } \right) - \beta _ { 0 } \right) \right) } , } \end{array}\tag{2}
$$

where $\beta _ { 0 }$ and $\beta _ { 1 }$ are constants determined by the environment. Accordingly, the NLoS probability is $P _ { N L o S } ( d _ { m , u } ^ { t } ) =$ $1 - P _ { L o S } ( d _ { m , u } ^ { t } )$ ( ) =. Then, the path loss between UE m and UAV 1 ( )u at time slot t is calculated by

$$
\begin{array} { r } { P L ( d _ { m , u } ^ { t } ) = \left\{ \begin{array} { l l } { \left( \displaystyle \frac { 4 \pi f _ { c } d _ { m , u } ^ { t } } { c } \right) ^ { 2 } \eta _ { L o S } , } & { \mathrm { w i t h } ~ P _ { L o S } ( d _ { m , u } ^ { t } ) , } \\ { \left( \displaystyle \frac { 4 \pi f _ { c } d _ { m , u } ^ { t } } { c } \right) ^ { 2 } \eta _ { N L o S } , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. } \end{array}\tag{3}
$$

where $f _ { c }$ denotes the carrier frequency, c is the speed of light, and $\eta _ { L o S }$ and $\eta _ { N L o S }$ are the excessive path losses of the LoS and NLoS links $( \eta _ { N L o S } > \eta _ { L o S } > 1 )$ , respectively. Let $p _ { m }$ be the (transmit power of UE m and $\sigma ^ { 2 }$ 1)denote the noise power. Then, the achievable uplink data rate from UE m to UAV u at time slot t can be calculated as

$$
R _ { m , u } ^ { t } = b _ { m , u } ^ { t } W _ { 0 } \log _ { 2 } \left( 1 + \frac { \alpha \cdot p _ { m } } { P L ( d _ { m , u } ^ { t } ) \cdot \sigma ^ { 2 } } \right) ,\tag{4}
$$

where Î± denotes the channel power gain at the reference distance of 1 m, and $W _ { 0 }$ is the total bandwidth resource.

Similarly, the achievable wireless link data rate from UAV u to MBS b can be given by

$$
R _ { u , b } ^ { t } = b _ { u , b } ^ { t } W _ { 1 } \log _ { 2 } \left( 1 + \frac { \alpha \cdot p _ { u } } { P L ( d _ { u , b } ^ { t } ) \cdot \sigma ^ { 2 } } \right) ,\tag{5}
$$

where $W _ { 1 }$ is the available wireless backhaul link bandwidth, and $p _ { u }$ indicates the transmit power of UAV u.

Let $R _ { u a v }$ denote the communication range of the UAV. Then, if the euclidean distance between two UAVs is not greater than $R _ { u a v }$ , they can communicate with each other. The horizontal distance between UAV u and UAV i at time slot t is $d _ { u , i } ^ { t } = \sqrt { ( x _ { u } ^ { t } - x _ { i } ^ { t } ) ^ { 2 } + ( y _ { u } ^ { t } - y _ { i } ^ { t } ) ^ { 2 } }$ . Consequently, considering = ( ) + ( )the free-space path loss [37], the available data rate between UAV u and UAV i can be given by

$$
R _ { u , i } ^ { t } = W _ { 2 } \log _ { 2 } \left( 1 + \frac { \alpha \cdot p _ { u } } { ( d _ { u , i } ^ { t } ) ^ { 2 } } \right) ,\tag{6}
$$

where $W _ { 2 }$ is the available wireless link bandwidth between UAV u and UAV i.

## C. Service Caching Placement Model

The UAV which executes tasks generated by UEs requiring corresponding services needs to cache the associated data, such as libraries and databases. Different from the MBS with huge and diverse resources, each UAV only stores a subset of services due to its limited cache capacity [34]. To ensure that all tasks can be executed, we assume that the MBS has S types of services. Let $c _ { s }$ denote the storage space required by service s. When the UE is located in the coverage range of multiple UAVs, caching services can reduce delay in a collaborative manner. Let $K _ { u }$ denote the total storage space of UAV u. $a _ { u , s } ^ { t } \in \{ 0 , 1 \}$ is a binary 0 1decision variable indicating whether service s is cached or not on UAV u at time slot t. If service s is cached on UAV u at time slot $t , a _ { u , s } ^ { t } = 1$ . Otherwise, $a _ { u , s } ^ { t } = 0$ . Let $A = \{ a _ { u , s } ^ { t } | u \in \mathcal { U } , s \in$ $s , t \in { \mathcal { T } } \}$ = 1 = 0 =denote the service caching placement decisions.

## D. Collaborative Computation Offloading Model

Each UAV can be employed as a mobile computing server, or act as a relay to further offload tasks to the MBS or other UAVs. To improve the performance of task execution, UAVs can provide parallel MEC services for UEs [29]. We use $X =$ $\{ { x } _ { m , s , u , i } ^ { t } | m \in \mathcal { M } , s \in \mathcal { S } , u \in \mathcal { U } , i \in \mathcal { U } \cup \{ b \} , t \in \mathcal { T } \}$ to represent the task offloading decisions. $x _ { m , s , u , i } ^ { t } \in \{ 0 , 1 \}$ is a binary offloading decision variable for task ${ \dot { V } } _ { m , s } ^ { t } .$ 0 1If task $V _ { m , s } ^ { t }$ is executed by UAV $i , x _ { m , s , u , i } ^ { t } = 1$ . Otherwise, $x _ { m , s , u , i } ^ { t } = 0$ . In addition, when $i = u , x _ { m , s , u , i } ^ { t } = 1$ means task $V _ { m , s } ^ { t }$ = 0is executed by = =the associated UAV u. When $i \in \mathcal { U } \setminus \{ u \} , x _ { m , s , u , i } ^ { t } = 1$ means task $V _ { m , s } ^ { t }$ = 1is executed by the non-associated collaborative UAV i. When $i = b , x _ { m , s , u , i } ^ { t } = 1$ means task $V _ { m , s } ^ { t }$ is executed by MBS = = 1b. Each task can only be offloaded to one UAV or the MBS. The task offloading decision should satisfy

$$
\sum _ { i \in \mathcal { U } \cup \{ b \} } x _ { m , s , u , i } ^ { t } = 1 , ~ \forall m \in \mathcal { M } , s \in \mathcal { S } , u \in \mathcal { U } .\tag{7}
$$

1) Associated UAV Computing: In many computationintensive applications, the delay and energy consumption for sending the results is small enough and can be neglected [19]. The task generated by the UE is first transmitted to one UAV, which serves as the associated UAV for the task. The communication delay from the UE to the associated UAV u can be given by

$$
D _ { m , s , u } ^ { t } = \frac { I _ { m , s } ^ { t } } { R _ { m , u } ^ { t } } .\tag{8}
$$

Let $f _ { m , s , u } ^ { t }$ denote the percentage of the computing resource allocated to task $V _ { m , s } ^ { t } .$ . Then, we use $F = \{ f _ { m , s , u } ^ { t } | m \in \mathcal { M } , s \in$ $\mathcal { S } , u \in \mathcal { U } , t \in \mathcal { T } \}$ =to denote the computing resource allocation decisions. The computation delay for UAV u can be calculated by

$$
C _ { m , s , u } ^ { t } = \frac { W _ { m , s } ^ { t } } { f _ { m , s , u } ^ { t } \mathcal { F } _ { u } } ,\tag{9}
$$

where $\mathcal { F } _ { u }$ denotes the computing capacity of UAV u. Therefore, the service delay of task $V _ { m , s } ^ { t }$ for the associated UAV u is calculated as

$$
F _ { m , s , u , u } ^ { t } = D _ { m , s , u } ^ { t } + C _ { m , s , u } ^ { t } .\tag{10}
$$

2) Non-Associated Collaborative UAV Computing: The service delay of task $V _ { m , s } ^ { t }$ for the non-associated collaborative UAV i includes three parts, the communication delay from the UE to the associated UAV u, the communication delay from the associated UAV u to non-associated collaborative UAV i, and the computation delay for UAV i. The communication delay from the associated UAV u to non-associated collaborative UAV i can be calculated by

$$
D _ { m , s , u , i } ^ { t } = \frac { I _ { m , s } ^ { t } } { R _ { u , i } ^ { t } } .\tag{11}
$$

Then, the computation delay for UAV i can be given by

$$
C _ { m , s , i } ^ { t } = \frac { W _ { m , s } ^ { t } } { f _ { m , s , i } ^ { t } \mathcal { F } _ { i } } .\tag{12}
$$

Consequently, the service delay of task $V _ { m , s } ^ { t }$ for the nonassociated collaborative UAV i can be expressed as

$$
\begin{array} { r } { F _ { m , s , u , i } ^ { t } = D _ { m , s , u } ^ { t } + D _ { m , s , u , i } ^ { t } + C _ { m , s , i } ^ { t } i \in \mathcal { U } \setminus \{ u \} . } \end{array}\tag{13}
$$

3) MBS Computing: If task $V _ { m , s } ^ { t }$ is offloaded at MBS b, the communication delay from the associated UAV u to MBS b can be given by

$$
D _ { m , s , u , b } ^ { t } = \frac { I _ { m , s } ^ { t } } { R _ { u , b } ^ { t } } .\tag{14}
$$

The computation delay for MBS b can be calculated as

$$
C _ { m , s , b } ^ { t } = \frac { W _ { m , s } ^ { t } } { f _ { b } } ,\tag{15}
$$

where $f _ { b }$ denotes the computing capacity of MBS b. Hence, the service delay of task $V _ { m , s } ^ { t }$ for MBS b can be given by

$$
F _ { m , s , u , b } ^ { t } = D _ { m , s , u } ^ { t } + D _ { m , s , u , b } ^ { t } + C _ { m , s , b } ^ { t } .\tag{16}
$$

Based on the above analysis, the service delay of task $V _ { m , s } ^ { t }$ can be obtained as

$$
\begin{array} { r l } & { F _ { m , s } ^ { t } = a _ { u , s } ^ { t } x _ { m , s , u , u } ^ { t } F _ { m , s , u , u } ^ { t } + a _ { i , s } ^ { t } x _ { m , s , u , i } ^ { t } F _ { m , s , u , i } ^ { t } } \\ & { \phantom { F _ { m , s } ^ { t } = a _ { u , s } ^ { t } } + x _ { m , s , u , b } ^ { t } F _ { m , s , u , b } ^ { t } . } \end{array}\tag{17}
$$

## E. Energy Consumption Model

The energy consumption of the UAV mainly consists of three parts, namely computing, relaying and flying. Based on [37], the energy consumption of UAV u for computing is calculated as

$$
E _ { u , e } = \kappa \sum _ { t \in \mathcal { T } } \sum _ { m \in \mathcal { M } } \sum _ { s \in \mathcal { S } } \sum _ { i \in \mathcal { U } } x _ { m , s , i , u } ^ { t } ( f _ { m , s , u } ^ { t } \mathcal { F } _ { u } ) ^ { 3 } C _ { m , s , u } ^ { t } ,\tag{18}
$$

where Îº is the capacitance coefficient of the CPU in the UAV. The energy consumption of UAV u for relaying to UAV i and

MBS b can be expressed as

$$
\begin{array} { r l } & { E _ { u , r c } } \\ & { = \displaystyle \sum _ { t \in { \mathcal T } } \displaystyle \sum _ { m \in { \mathcal M } } \sum _ { s \in { \mathcal S } } p _ { u } } \\ & { \qquad \quad \times \left( \displaystyle \sum _ { i \in { \mathcal U } \backslash \{ u \} } x _ { m , s , u , i } ^ { t } D _ { m , s , u , i } ^ { t } + x _ { m , s , u , b } ^ { t } D _ { m , s , u , b } ^ { t } \right) . } \end{array}\tag{19}
$$

As derived in [16], for rotary-wing UAV u flying with speed $v _ { u } ^ { t }$ , the propulsion power consumption can be modeled as

$$
\begin{array} { r l r } {  { p ( v _ { u } ^ { t } ) = P _ { 0 } ( 1 + \frac { 3 ( v _ { u } ^ { t } ) ^ { 2 } } { U _ { t i p } ^ { 2 } } ) + P _ { i } ( \sqrt { 1 + \frac { ( v _ { u } ^ { t } ) ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { ( v _ { u } ^ { t } ) ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } ) ^ { \frac { 1 } { 2 } } } } \\ & { } & { + \frac { 1 } { 2 } d _ { 0 } \rho s A _ { r } ( v _ { u } ^ { t } ) ^ { 3 } , } \end{array}\tag{20}
$$

where $P _ { 0 } , U _ { t i p } , P _ { i } , v _ { 0 } , d _ { 0 } , \rho ,$ s and $A _ { r }$ are constants based on the UAV and environment. We assume that UAV u follows a uniform rectilinear motion. Then, we have

$$
v _ { u } ^ { t } = \frac { \lvert | Q _ { u } ^ { t + 1 } - Q _ { u } ^ { t } \rvert | } { \Delta _ { t } } \forall t \in \mathcal { T } , \forall u \in \mathcal { U } .\tag{21}
$$

Thus, the flight energy consumption of UAV u at entire task cycle is given by

$$
E _ { u , f } = \sum _ { t \in \mathcal { T } } \Delta _ { t } P ( v _ { u } ^ { t } ) .\tag{22}
$$

Hence, the total energy consumption of UAV u is obtained as

$$
E _ { u } = E _ { u , e } + E _ { u , r c } + E _ { u , f } .\tag{23}
$$

## IV. PROBLEM FORMULATION

## A. Problem Formulation

We jointly optimize the UAV trajectory Q, bandwidth resource allocation B, service caching A, task offloading X, and computing resource allocation F . If we only minimize the total service delay, some UEs may suffer unfair treatment, thereby leading to high service delay of these UEs. To address this issue, we introduce Jainâs fairness index as a quantitative measure of service fairness [38]. Let $\begin{array} { r } { \bar { F } _ { m , s } = \frac { 1 } { T } \sum _ { t = 1 } ^ { \bar { T } } F _ { m , s } ^ { t } } \end{array}$ denote the average service delay of task $V _ { m , s } ^ { t }$ in the task period. The set of the average service delay for task $V _ { m , s } ^ { t }$ is expressed as $\bar { \mathbf { F } } = \{ \bar { F } _ { m , s } | m \in \mathcal { M } , s \in \mathcal { S } \}$ . The fairness of the average service =delay among UEs is characterized by Jainâs fairness equation, which can be defined as

$$
J ( \bar { \mathbf { F } } ) = \frac { \left( \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } \right) ^ { 2 } } { M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } } ,\tag{24}
$$

where $J ( { \bar { \mathbf { F } } } )$ is continuous and lies in $[ \textstyle { \frac { 1 } { M } } , 1 ]$ . The value of $J ( { \bar { \mathbf { F } } } )$ measures the fairness among all UEs, and a higher value ( )means all UEs have similar service delays and better fairness is achieved. In extreme cases, $\begin{array} { r } { J ( \bar { \mathbf F } ) = \frac { 1 } { M } } \end{array}$ corresponds to the ( ) =most unfair experience in which all UEs have significantly different service delays, and $J ( { \bar { \mathbf { F } } } ) = 1$ corresponds to the fairest ( ) = 1experience in which all UEs have the same service delay.

Lemma 1: The value of $J ( { \bar { \mathbf { F } } } )$ lies within $[ \textstyle { \frac { 1 } { M } } , 1 ]$

( ) [ 1]Proof: Let C be a constant. Then, according to Cauchyâs inequality, we can obtain

$$
\sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \left( \bar { F } _ { m , s } \right) ^ { 2 } \cdot \sum _ { m = 1 } ^ { M } C ^ { 2 } \geq \left( \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } \cdot C \right) ^ { 2 } .\tag{25}
$$

Consequently, we have $\begin{array} { r } { M \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } \geq ( \sum _ { m = 1 } ^ { M } } \end{array}$ $\textstyle \sum _ { s = 1 } ^ { S } { \bar { F } } _ { m , s } ) ^ { 2 }$ , and thus $J ( \bar { \mathbf { F } } ) \leq 1$ . In addition, the condition ) ( ) 1for the equation to hold is that the service delay of each UE is equal. Based on the extension of the complete square formula, we obtain $\begin{array} { r } { ( \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } ) ^ { 2 } \geq \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } } \end{array}$ , and thus $\begin{array} { r } { J ( \mathbf { \bar { F } } ) \geq \frac { \mathrm { ~ j ~ } } { M } } \end{array}$ -

( )Ulteriorly, considering the limited onboard energy and CCS resources of the UAV, we attempt to reduce the average service delay while guaranteeing the fairness among UEs. If we only maximize the fairness index, the total service delay may be high, resulting in poor overall experience. Thus, we define the objective function as the ratio of the fairness to the average service delay. Consequently, the optimization problem of maximizing the service experience ratio can be formulated as

$$
\mathcal { P } _ { 1 } : \operatorname* { m a x } _ { Q , B , A , X , F } \frac { J ( \bar { \mathbf { F } } ) } { \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } F _ { m , s } ^ { t } }\tag{26}
$$

$$
\begin{array} { r } { s . t . C _ { 1 } : x _ { m , s , u , i } ^ { t } \leq a _ { u , s } ^ { t } , \forall m \in \mathcal { M } , \forall s \in \mathcal { S } , \forall u \in \mathcal { U } , } \end{array}
$$

$$
C _ { 2 } : \sum _ { m \in \mathcal { M } } \sum _ { i \in \mathcal { U } \cup \{ b \} } x _ { m , s , u , i } ^ { t } b _ { m , u } ^ { t } \leq 1 , \forall s \in \mathcal { S } , \forall u \in \mathcal { U } ,
$$

$$
C _ { 3 } : \sum _ { m \in \mathcal { M } } \sum _ { s \in \mathcal { S } } x _ { m , s , u , i } ^ { t } f _ { m , s , u } ^ { t } \le 1 , \forall u \in \mathcal { U } , \forall i \in \mathcal { U } \setminus \{ u \} ,
$$

$$
C _ { 4 } : \sum _ { s \in \mathcal { S } } a _ { u , s } ^ { t } c _ { s } \leq K _ { u } , \forall u \in \mathcal { U } ,
$$

$$
C _ { 5 } : { x _ { m , s , u , u } ^ { t } } d _ { m , u } ^ { t } \le R _ { u } , \forall m \in \mathcal { M } , \forall s \in \mathcal { S } , \forall u \in \mathcal { U } ,
$$

$$
C _ { 6 } : | | Q _ { u } ^ { t + 1 } - Q _ { u } ^ { t } | | \leq v _ { \operatorname* { m a x } } \Delta _ { t } , Q _ { u } ^ { 1 } = Q _ { u } ^ { T } , \forall u \in \mathcal { U } ,
$$

$$
C _ { 7 } : 0 \le x _ { u } ^ { t } \le x _ { \operatorname* { m a x } } , 0 \le y _ { u } ^ { t } \le y _ { \operatorname* { m a x } } , \forall u \in \mathcal { U } ,
$$

$$
C _ { 8 } : | | Q _ { u } ^ { t } - Q _ { i } ^ { t } | | \geq d _ { \operatorname* { m i n } } , \forall u \in \mathcal { U } , \forall i \in \mathcal { U } \setminus \{ u \} ,
$$

$$
C _ { 9 } : x _ { m , s , u , i } ^ { t } d _ { u , i } ^ { t } \leq R _ { u a v } , \forall u \in \mathcal { U } , \forall m \in \mathcal { M } , \forall s \in \mathcal { S } ,
$$

$$
\forall i \in \mathcal { U } \setminus \{ u \} ,
$$

$$
C _ { 1 0 } : E _ { u } \le E _ { t h } , \forall u \in \mathcal { U } ,
$$

$$
C _ { 1 1 } : F _ { m , s } ^ { t } \leq D _ { m , s } ^ { t } , \forall m \in \mathcal { M } , \forall s \in \mathcal { S } ,
$$

$$
C _ { 1 2 } : \sum _ { i \in \mathcal { U } \cup \{ b \} } x _ { m , s , u , i } ^ { t } = 1 , \forall m \in \mathcal { M } , s \in \mathcal { S } , u \in \mathcal { U } ,
$$

$$
C _ { 1 3 } : a _ { u , s } ^ { t } \in \{ 0 , 1 \} , \forall u \in \mathcal { U } , \forall s \in \mathcal { S } ,
$$

$$
C _ { 1 4 } : x _ { m , s , u , i } ^ { t } \in \{ 0 , 1 \} , \forall m \in \mathcal { M } , \forall s \in \mathcal { S } , \forall u \in \mathcal { U } ,
$$

$$
\begin{array} { r l } & { \quad \forall i \in \mathcal { U } \setminus \{ u \} , } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \end{array} \mathrm { ~ a n ~ ~ , ~ }
$$

where constraint $C _ { 1 }$ means that task $V _ { m , s } ^ { t }$ only can be offload to UAV u caching service s. Constraint $C _ { 2 }$ represents the bandwidth limitation. Constraint $C _ { 3 }$ denotes the computing resource capacity of each UAV. Constraint $C _ { 4 }$ implies each UAVâs storage space. Constraint $C _ { 5 }$ states that the UE should be within the coverage range of its associated UAVs. Constraint $C _ { 6 }$ and $C _ { 7 }$ capture the position variation constraint of the UAV between any two time slots. Constraint $C _ { 8 }$ ensures collision avoidance among UAVs in each time slot. Constraint $C _ { 9 }$ restricts the horizontal distance between UAV u and its collaborative UAV i to be less than $R _ { u a v }$ . Constraints $C _ { 1 0 }$ illustrates the energy upper bound $E _ { t h }$ of each UAV. Constraints $C _ { 1 1 }$ 1 indicates the maximum tolerable latency requirements. Constraint $C _ { 1 2 }$ denotes that each task can only be offloaded to one of UAVs or the MBS. Constraint $C _ { 1 3 }$ and $C _ { 1 4 }$ respectively indicate that the service caching placement and task offloading variables are binary, while constraint $C _ { 1 5 }$ denotes that the bandwidth and computing resources allocation variables are continuous. Due to the coupling of variables such as task offloading and trajectory planning, Lemma 2 shows the NP-hardness of the above optimization problem.

Lemma 2: The optimization problem (26) is NP-hard.

Proof: The optimization problem jointly optimizes the UAV trajectory, task offloading, and multidimensional resource allocation. Given the UAV trajectory and multidimensional resource allocation, the task offloading in (26) is equivalent to the traveling salesman problem, which is NP-hard. Thus, the optimization problem in (26) is NP-hard. -

Considering the NP-hardness, the original optimization is challenging to solve in general. Therefore, we adopt a transformation approach for solving it in the following section.

## B. Problem Transformation

To solve problem $\mathcal { P } _ { 1 }$ , we equivalently simplify the objective function into the following

$$
\begin{array} { r } { \frac { J ( \bar { \mathbf { F } } ) } { \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } F _ { m , s } ^ { t } } = \frac { \frac { ( \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } ) ^ { 2 } } { M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } } } { \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } } } \\ { = \frac { \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } } { M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) _ { \infty } ^ { 2 } } . } \end{array}\tag{)(27}
$$

Therefore, problem $\mathcal { P } _ { 1 }$ can be rewritten as

$$
\mathcal { P } _ { 2 } : \operatorname* { m a x } _ { Q , B , A , X , F } \frac { \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } } { M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } }\tag{28}
$$

$$
s . t . \quad \quad C _ { 1 } - C _ { 1 5 } .
$$

Problem $\mathcal { P } _ { 2 }$ is a fractional programming problem. We employ the Dinkelbachâs method [39]. The objective function of problem $\mathcal { P } _ { 2 }$ can be reformulated into the following parametric

programming form

$$
f ( \eta ) \triangleq \operatorname* { m a x } _ { Q , B , A , X , F } \left\{ \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } - \eta M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } \right\} .\tag{29}
$$

Lemma 3: Let Î·â denote the optimal service experience ratio. The optimal solution of problem $\mathcal { P } _ { 2 }$ can be obtained if and only if

$$
f ( \eta ^ { * } ) = 0 .\tag{30}
$$

Proof: Please refer to [40].

-

Therefore, problem $\mathcal { P } _ { 2 }$ can be transformed into an equivalent parametric problem as follows

$$
\mathcal { P } _ { 3 } : \operatorname* { m a x } _ { Q , B , A , X , F } \left\{ \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } - \eta M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } \right\}\tag{31}
$$

$$
s . t . \quad \quad C _ { 1 } - C _ { 1 5 } ,
$$

which is a mixed-integer non-convex programming problem. To solve this problem, we propose a four-stage alternating iteration algorithm, which is shown in the next part.

## V. ALGORITHM DESIGN

We decompose problem $\mathcal { P } _ { 3 }$ into four sub-problems, respectively optimizing the task offloading X, service caching placement A, UAV trajectory Q, as well as bandwidth and computing resources allocation $( B , F )$ . After each round of these four ( )sub-optimization stages, the value of Î· is updated according to $f ( \eta ) \triangleq 0$ defined in (29).

## A. Task Offloading Based on Satisfaction

We first consider to optimize the task offloading X by fixing the other variables $( Q , B , A , F )$ . Then, the task offloading sub-(problem can be formulated as

$$
\begin{array} { r l } & { \mathcal { P } _ { 3 - 1 } : \displaystyle \operatorname* { m a x } _ { X } \left\{ \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } - \eta M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } \right\} } \\ & { s . t . \quad C _ { 1 } , C _ { 3 } , C _ { 5 } , C _ { 9 } - C _ { 1 2 } , C _ { 1 4 } . } \end{array}\tag{32}
$$

In order to better describe the optimization process of task offloading, we define the set of UAVs that cache the services required by task $V _ { m , s } ^ { t }$ as $\mathcal { U } _ { m , s } ^ { c a n }$ . Each UE sends the task to its associated UAV, and the set of tasks received by the associated UAV is defined as $\mathcal { M } _ { u } ^ { r e q }$ , which includes the tasks offloaded by the associated UEs and the collaborative UAVs. If the associated UAV u belongs to $\mathcal { U } _ { m , s } ^ { c a n }$ , this means that UAV u hits the service required task $V _ { m , s } ^ { t } .$ Then, the hit task is added to the set $\mathcal { M } _ { u } ^ { e x e }$ , and the missed task is added to $\mathcal { M } _ { u } ^ { o f f }$ . In the initial task offloading decision, we assume that all tasks in set $\mathcal { M } _ { u } ^ { e x e }$ are computed by the associated UAV u. The tasks in set $\mathcal { M } _ { u } ^ { o f f }$ are further offloaded to the collaborative UAV i in set $\mathcal { U } _ { m , s } ^ { c a n }$ or MBS b with the highest value of problem $\mathcal { P } _ { 3 - 1 }$

We select the optimal offloading location for tasks based on UEâs satisfaction. First, we calculate the satisfaction of each

UE according to (32), and select the task in set $\mathcal { M } _ { u } ^ { e x e }$ with the smallest satisfaction in turn for further offloading. Then, we remove it from set $\mathcal { M } _ { u } ^ { e x e }$ to $\mathcal { M } _ { u } ^ { o f f }$ , until all the tasks in set $\mathcal { M } _ { u } ^ { e x e }$ meet the maximum tolerable delay as well as CSS resources and energy constraints. In set $\mathcal { M } _ { u } ^ { o f f }$ , each task has different satisfactions with different offloading locations. The larger the service experience ratio, the bigger the value of satisfaction. Then, the task $V _ { m , s } ^ { t } ,$ which is rejected by the associated UAV u and needs to be further offloaded, has a satisfactory value for the collaborative UAV i, which can be given by

$$
\varphi _ { m , s , u } ^ { t } ( i ) = \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } - \eta M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } ,\tag{33}
$$

$$
\bar { F } _ { m , s } = \frac { 1 } { T } \sum _ { t = 1 } ^ { T } { F _ { m , s , u , i } ^ { t } } .\tag{34}
$$

Similarly, the task $V _ { m , s } ^ { t }$ has a satisfactory value for MBS $b ,$ which can be expressed as

$$
\varphi _ { m , s , u } ^ { t } ( b ) = \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } - \eta M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } ,\tag{35}
$$

$$
\bar { F } _ { m , s } = \frac { 1 } { T } \sum _ { t = 1 } ^ { T } F _ { m , s , u , b } ^ { t } .\tag{36}
$$

The associated UAV sends the task $V _ { m , s } ^ { t }$ to the location with a high satisfaction value. If the offloading location is MBS b, the task will be offloaded directly, and $x _ { m , s , u , b } ^ { t } = 1$ . If the offloading = 1location is the collaborative UAV i, the permission of UAV i is required. If the offloading request is rejected, the task $V _ { m , s } ^ { t }$ will be sent to the next optimal offloading location in the next iteration until it is permitted. Then, $x _ { m , s , u , i } ^ { t } = 1$ . Repeat the above = 1optimization process until obtaining the offloading locations of all tasks. The task offloading based on satisfaction is shown in Algorithm 1. Each task has different value of satisfactions with different offloading locations. Then, we select the optimal offloading location for tasks based on the value of satisfactions.

## B. Service Caching Based on Priority

In this section, we tackle the service caching placement A optimization sub-problem with fixed the other variables $( Q , B , X , F )$ . Then, the sub-problem of service caching deci-( )sion is formulated as

$$
\begin{array} { r l } & { \mathcal { P } _ { 3 - 2 } : \displaystyle \operatorname* { m a x } _ { A } \left\{ \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } - \eta M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } \right\} } \\ & { s . t . \quad C _ { 1 } , C _ { 4 } , C _ { 1 0 } , C _ { 1 1 } , C _ { 1 3 } . } \end{array}\tag{37}
$$

Due to the limited storage space, the UAV cannot cache all services. We determine the service caching decisions to minimize the service delay while guaranteeing fairness. To improve the utilization of storage space, the service required by the task with a higher value of $\mathcal { P } _ { 3 - 2 }$ has a high priority to be cached at the UAV until the storage space is reached. Let $\mathcal { M } _ { i } = \{ m \in$ $\mathcal { M } | x _ { m , s , u , i } ^ { t } = 1 , \forall s \in \mathcal { S } , \forall u , i \in \mathcal { U } , t \in \mathcal { T } \}$ and $| \mathcal { M } _ { i } |$ denote = 1the set and number of the tasks offloaded to UAV i, respectively.

Algorithm 1: Satisfaction-Based Task Offloading Algo  
rithm.   
Input: UAV trajectory $Q ,$ service caching A, resource   
allocation B and F , the set of tasks $V ^ { t }$   
Output: task offloading decisions X.   
1: Initialize $\mathcal { U } _ { m , s } ^ { c a n } , \tilde { \mathcal { M } } _ { u } ^ { r e q } , \mathcal { M } _ { u } ^ { e x e } , \mathcal { M } _ { u } ^ { o f f }$ equal to â;   
2: Initial task offloading decisions:   
3: for $u \in \mathcal { U }$ do   
4: $\mathcal { M } _ { u } ^ { r e q } \gets$ received the tasks;   
5: $\mathcal { M } _ { u } ^ { e x e }  x _ { m , s , u , u } ^ { t } = 1 , \mathcal { M } _ { u } ^ { o f f }$ â according to the   
value of $\mathcal { P } _ { 3 - 1 } ;$   
6: end for   
7: for $V _ { m , s } ^ { t } \in V ^ { t }$ do   
8: $\mathcal { M } _ { u } ^ { e x e } \gets a _ { m , s } ^ { t } = 1 ;$   
9: if $\begin{array} { r } { \bar { F } _ { m , s } ^ { t } \le \bar { D } _ { m , s } ^ { \bar { t } } , \sum _ { m \in \mathcal { M } } \sum _ { s \in \mathcal { S } } x _ { m , s , u , i } ^ { t } f _ { s } \le f _ { u } , } \end{array}$   
and $\dot { E _ { u } } \le E _ { t h } ( \forall u \in \mathcal { U } )$   
10: $\mathcal { M } _ { u } ^ { e x e } = \mathcal { M } _ { u } ^ { e x e } ;$   
11: $x _ { m , s , u , u } ^ { t } = 1 ;$   
12: else   
13: Computing the value of $\mathcal { P } _ { 3 - 1 } ;$   
14: Sort $\mathcal { P } _ { 3 - 1 }$ in descending order, select a task $V _ { m , s } ^ { t }$   
with the smallest value in turn for further   
offloading, let $\mathcal { M } _ { u } ^ { e x e } = \mathcal { M } _ { u } ^ { e x e } \setminus \{ V _ { m , s } ^ { t } \}$ and   
$\mathcal { M } _ { u } ^ { o f f } = \mathcal { M } _ { u } ^ { o f f } \cup \{ V _ { m , s } ^ { t } \} ;$   
15: end if   
16: end for   
17: for $V _ { m , s } ^ { t } \in \mathcal { M } _ { u } ^ { o f f }$ do   
18: Sort $\varphi _ { m , s , u } ^ { t } ( i )$ and $\varphi _ { m , s , u } ^ { t } ( b )$ in descending order,   
( ) ( )select a collaborative UAV i or MBS b with the   
biggest value to send the task;   
19: if i  b do   
20: = Send the task to MBS $b ,$ let $\mathcal { M } _ { u } ^ { o f f } \setminus \{ V _ { m , s } ^ { t } \}$   
$x _ { m , s , u , b } ^ { t } = 1 ;$   
21: else   
22: Send the task to collaborative UAV i until it is   
allowed, let $\mathcal { M } _ { u } ^ { o f f } \setminus \{ V _ { m , s } ^ { t } \} , x _ { m , s , u , i } ^ { t } = 1$ ;   
23: end if   
24: end for

We denote $s _ { i }$ and $| S _ { i } |$ as the set and the number of the services required by the tasks. Since multiple tasks may require the same service, we have $\left| S _ { i } \right| < \left| \mathcal { M } _ { i } \right|$ . The service required by task $V _ { m , s } ^ { t }$ is cached at $\mathrm { U A V } \ i \ ( i \in \mathcal { U } )$ with a priority value, which can be expressed as

$$
\begin{array} { l } { { \displaystyle \operatorname { \overline { { E } } } _ { m , s , i } = \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } - \eta M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ) ^ { 2 } } , } \\ { { \displaystyle \bar { F } _ { m , s } = \frac { 1 } { T } \sum _ { t = 1 } ^ { T } F _ { m , s } ^ { t } } } \\ { { = \left\{ \begin{array} { l l } { { \displaystyle \frac { 1 } { T } \sum _ { t = 1 } ^ { T } F _ { m , s , u , w } ^ { t } , } } & { { \displaystyle x _ { m , s , u , u } ^ { t } = 1 , } } \\ { { \displaystyle \frac { 1 } { T } \sum _ { t = 1 } ^ { T } F _ { m , s , u , i } ^ { t } , } } & { { \displaystyle x _ { m , s , u , i } ^ { t } = 1 . } } \end{array} \right. } } \end{array}\tag{38}
$$

(39)

Algorithm 2: Priority-Based Service Caching Algorithm.   
Input: UAV trajectory ${ \overline { { Q } } } ,$ task offloading decisions X,   
resource allocation B and $F _ { ; }$ , the set of tasks $V ^ { t } .$   
Output: service caching decisions $A .$   
1: Initialize $\boldsymbol { S } _ { i } , \boldsymbol { S } _ { i } ^ { \prime }$ equal to $\mathcal { D } ;$   
2: for $i \in \mathcal { U }$ do   
3: for $V _ { m , s } ^ { t } \in V ^ { t }$ do   
4: if $V _ { m , s } ^ { i ^ { - } } \ne V _ { m , s ^ { \prime } } ^ { t } , s = s ^ { \prime }$ do   
5: Computing the value of $\varpi _ { m , s , i } ,$ , sort $\varpi _ { m , s , i }$ in   
descending order, select the task $V _ { m , s } ^ { t }$ with the   
biggest value to store, let $S _ { i } = S _ { i } \stackrel {  } { \cup } \{ V _ { m , s } ^ { t } \}$ ;   
6: else   
7: ${ \cal { S } } _ { i } = { \cal { S } } _ { i } ;$   
8: =end if   
9: Sort the element of $S _ { i }$ in descending order;   
10: repeat   
11: Select the service required by the task with the   
biggest value of $\mathcal { P } _ { 3 - 2 }$ to store in turn, let   
${ \tilde { S _ { i } ^ { \prime } } } { \bar { = } } { \tilde { S _ { i } ^ { \prime } } } \cup \{ s \}$ , and get the service caching   
=placement decision $a _ { i , s } ^ { t }$ by (40);   
12: until the maximum cache capacity of the UAV is   
reached   
13: end for   
14: end for

Next, we sort the tasks requiring the same service in descending order based on the value of $\varpi _ { m , s , i }$ , and then store the task with the highest value in set ${ \mathcal { S } } _ { i } , { \mathrm { i . e . , } } { \mathcal { S } } _ { i } = \{ m _ { 1 } , m _ { 2 } , . . . , m _ { | { \mathcal { S } } _ { i } | } \}$ where $m = \arg \operatorname* { m a x } _ { m \in \mathcal { M } _ { i } } \varpi _ { m , s , i } .$ = Then, we sort the elements in set $S _ { i }$ in descending order based on the value of $\varpi _ { m , s , i }$ , and cache the service with a higher value until reaching the upper limit of the storage space. Let $a _ { i , \mathscr { s } } ^ { t }$ indicate whether the service s is cached at UAV i. We further obtain $S _ { i } ^ { \prime } = \left\{ s _ { 1 } , s _ { 2 } , . . . , s _ { J - 1 } \right\}$ where $\begin{array} { r } { J = \operatorname* { m i n } _ { j } \sum _ { j = 1 } ^ { J } c _ { j } > K _ { i } } \end{array}$

$$
a _ { i , s } ^ { t } = \left\{ \begin{array} { l l } { 1 , \quad } & { \mathrm { i f } s \in  { S _ { i } ^ { \prime } } , } \\ { 0 , \quad } & { \mathrm { o t h e r w i s e } , } \end{array} \right. \forall i \in \mathcal { U } .\tag{40}
$$

The details are shown in Algorithm 2, and the main process is as follows: First, the service required by the task is cached at the UAV with a priority value based on formula (38). Next, we sort the tasks requiring the same service based on descending order based on the priority value, and store the task with the highest priority value in set S. Then, we sort the elements in set S based on descending order and cache the service with a higher value until reaching the upper limit of the UAVâs storage space.

## C. UAV Trajectory Optimization

In this part, we optimize the UAVâs trajectory with fixed the other variables $( A , B , X , F )$ , which is expressed as

$$
\begin{array} { l } { \mathcal { P } _ { 3 - 3 } : } \\ { \displaystyle \operatorname* { m a x } _ { Q } \left\{ \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } F _ { m , s } ^ { t } \right. } \end{array}
$$

$$
\begin{array} { r l } & { \displaystyle - \eta M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \left( \frac { 1 } { T } \sum _ { t = 1 } ^ { T } F _ { m , s } ^ { t } \right) ^ { 2 } \Bigg \} } \\ & { \displaystyle s . t . \quad C _ { 5 } , C _ { 7 } , C _ { 9 } - C _ { 1 1 } , } \\ & { \displaystyle C _ { 6 } : | | Q _ { u } ^ { t + 1 } - Q _ { u } ^ { t } | | ^ { 2 } \leq ( v _ { \operatorname* { m a x } } \Delta _ { t } ) ^ { 2 } , } \\ & { \displaystyle C _ { 8 } : | | Q _ { u } ^ { t } - Q _ { i } ^ { t } | | ^ { 2 } \geq d _ { \operatorname* { m i n } } ^ { 2 } . } \end{array}\tag{41}
$$

We remove the constants, $F _ { m , s } ^ { t }$ can be simplified as

$$
\begin{array} { r l } & { \overline { { \tilde { F } _ { n , n } ^ { * } } } , } \\ & { = u _ { n , c } ^ { * } , x _ { n + , n - s } ^ { * } \frac { \tilde { F } _ { n , n } ^ { * } } { \tilde { F } _ { n , n } ^ { * } \cup \mathcal { C } _ { n , n } ^ { * } } \frac { \tilde { F } _ { n , n } ^ { * } } { \left| \tilde { F } _ { n , n } ^ { * } - \tilde { G } _ { n , n } ^ { * } \right| \left| \tilde { F } _ { n , n } ^ { * } \right| } } \\ & { + u _ { n , c } ^ { * } \frac { \tilde { F } _ { n , n - s , n - s } ^ { * } } { \tilde { F } _ { n , n } ^ { * } \cup \mathcal { C } _ { n , n } ^ { * } } \left( \frac { F _ { n , n - s } ^ { * } } { \left| \tilde { F } _ { n , n } ^ { * } - \tilde { G } _ { n , n } ^ { * } \right| \left| \tilde { F } _ { n , n } ^ { * } \right| \mathrm { d } _ { \mathcal { C } _ { n , n } ^ { * } } } \right) } \\ & { + \frac { 1 } { W _ { 2 } ^ { * } \cup \mathcal { C } _ { n , n } ^ { * } } \frac { \tilde { F } _ { n , n - s } ^ { * } } { \left( 1 - \frac { \sigma _ { n } } { \left| \tilde { G } _ { n , n } ^ { * } - \tilde { G } _ { n , n } ^ { * } \right| \left| \tilde { F } _ { n , n } ^ { * } \right| } \right) } } \\ & { + \frac { \tilde { F } _ { n , n - s } ^ { * } } { W _ { 2 } ^ { * } \cup \mathcal { C } _ { n } ^ { * } \left( 1 - \frac { \sigma _ { n } } { \left| \tilde { G } _ { n , n } ^ { * } - \tilde { G } _ { n , n } ^ { * } \right| \left| \tilde { F } _ { n , n } ^ { * } \right| } \right) } } \\ &  + z _ { n , n , s } ^ { * } \frac  \tilde { F } _  n \end{array}\tag{42}
$$

It is noted that problem $\mathcal { P } _ { 3 - 3 }$ is non-convex with $\tilde { F } _ { m , s } ^ { t }$ . The left-hand-side of constraints $C _ { 1 0 }$ and $C _ { 1 1 }$ is non-convex w.r.t. the UAV trajectory Q. Since the domain of convex function is non-empty convex set, constraint $C _ { 8 }$ is non-convex. Then, to tackle this sub-problem, we adopt the SCA method to obtain the local optimal solution of problem $\mathcal { P } _ { 3 - 3 }$ . We define $e _ { m , u } ^ { t }$ as the available spectrum efficiency from UE m to UAV u, which can be written as

$$
e _ { m , u } ^ { t } = \log _ { 2 } \left( 1 + \frac { \alpha p _ { m } } { | | Q _ { u } ^ { t } - Q _ { m } | | ^ { 2 } + h ^ { 2 } } \right) .\tag{43}
$$

It is obvious that $e _ { m , u } ^ { t }$ is a convex function w.r.t. $| | Q _ { u } ^ { t } - Q _ { m } | | ^ { 2 }$ Therefore, it can be globally lower-bounded by its first-order Taylor expansion with $\left| \left| Q _ { u } ^ { t } - Q _ { m } \right| \right|$ at any point [41]. In the k-th iteration, for the given $Q _ { u } ^ { t } ( k )$ , the lower bound of the function $e _ { m , u } ^ { t }$ can be calculated as

$$
\begin{array} { r l } {  { \hat { e } _ { m , u } ^ { t } = e _ { m , u } ^ { t } ( k ) + \nabla e _ { m , u } ^ { t } ( k ) } } \\ & { \quad \times ( | | Q _ { u } ^ { t } - Q _ { m } | | - | | Q _ { u } ^ { t } ( k ) - Q _ { m } | | ) , } \end{array}\tag{44}
$$

where $e _ { m , u } ^ { t } ( k )$ and $\nabla e _ { m , u } ^ { t } ( k )$ are the available spectrum effi-( ) ( )ciency from UE m to UAV u in the k-th iteration, and the firstorder derivative of $e _ { m , u } ^ { t } ( k )$ w.r.t. $\vert \vert Q _ { u } ^ { t } ( k ) - Q _ { m } \vert \vert$ , respectively. ( )They are given as follows

$$
\begin{array} { l l } { \displaystyle e _ { m , u } ^ { t } ( k ) = \log _ { 2 } \left( 1 + \frac { \alpha p _ { m } } { \vert \vert Q _ { u } ^ { t } ( k ) - Q _ { m } \vert \vert ^ { 2 } + h ^ { 2 } } \right) , } \\ { \nabla e _ { m , u } ^ { t } ( k ) } \end{array}\tag{45}
$$

$$
= \frac { - \alpha p _ { m } \log _ { 2 } e } { ( | | Q _ { u } ^ { t } ( k ) - Q _ { m } | | ^ { 2 } + h ^ { 2 } ) \left( | | Q _ { u } ^ { t } ( k ) - Q _ { m } | | ^ { 2 } + h ^ { 2 } + \alpha p _ { m } \right) } .\tag{46}
$$

Similarly, we have the lower bounds of the available spectrum efficiency from UAV u to UAV i and the available spectrum efficiency from UAV u to MBS b, denoted by $\hat { e } _ { u , i } ^ { t }$ and $\hat { e } _ { u , b } ^ { t }$ respectively.

As a result, the lower bound of $F _ { m , s } ^ { t }$ can be given by

$$
\begin{array} { r l r } {  { \hat { F } _ { m , s } ^ { t } = a _ { u , s } ^ { t } x _ { m , s , u , u } ^ { t } ( \frac { I _ { m , s } ^ { t } } { b _ { m , u } ^ { t } W _ { 0 } \hat { e } _ { m , u } ^ { t } } + C _ { m , s , u } ^ { t } ) } } \\ & { } & { + a _ { i , s } ^ { t } x _ { m , s , u , i } ^ { t } ( \frac { I _ { m , s } ^ { t } } { b _ { m , u } ^ { t } W _ { 0 } \hat { e } _ { m , u } ^ { t } } + \frac { I _ { m , s } ^ { t } } { W _ { 2 } \hat { e } _ { u , i } ^ { t } } + C _ { m , s , i } ^ { t } ) } \\ & { } & { + x _ { m , s , u , b } ^ { t } ( \frac { I _ { m , s } ^ { t } } { b _ { m , u } ^ { t } W _ { 0 } \hat { e } _ { m , u } ^ { t } } + \frac { I _ { m , s } ^ { t } } { W _ { 1 } \hat { e } _ { u , b } ^ { t } } + C _ { m , s , b } ^ { t } ) . } \end{array}\tag{47}
$$

In constraint $C _ { 8 } ,$ since $| | Q _ { u } ^ { t } - Q _ { i } ^ { t } | | ^ { 2 }$ is convex w.r.t. the UAV trajectory $Q .$ , we invoke the SCA method to relax the constraint. By applying the first-order Taylor expansion at any given $Q _ { u } ^ { t } ( k )$ and $Q _ { i } ^ { t } ( k )$ , we have the following inequality

$$
\begin{array} { r l } & { \lvert | Q _ { u } ^ { t } - Q _ { i } ^ { t } \rvert | ^ { 2 } \geq - \lvert | Q _ { u } ^ { t } ( k ) - Q _ { i } ^ { t } ( k ) \rvert | ^ { 2 } + 2 ( Q _ { u } ^ { t } ( k ) } \\ & { - Q _ { i } ^ { t } ( k ) ) ^ { T } ( Q _ { u } ^ { t } - Q _ { i } ^ { t } ) . } \end{array}\tag{48}
$$

In constraint $C _ { 1 0 }$ , function $E _ { u }$ is composed of the flight power $p ( v _ { u } ^ { t } )$ . According to formula (20), the first and third terms of this power is convex function about speed $\ v { v } _ { u } ^ { t }$ . Thus, we introduce a slack variable $\vartheta = \{ \vartheta _ { u } ^ { t } \} _ { u \in \mathcal { U } , t \in \mathcal { T } }$ to deal with second term. It becomes to

$$
\vartheta _ { u } ^ { t } \geq \left( \sqrt { 1 + \frac { ( v _ { u } ^ { t } ) ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { ( v _ { u } ^ { t } ) ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { \frac { 1 } { 2 } } .\tag{49}
$$

Through simplification, we can obtain

$$
\frac { 1 } { ( \vartheta _ { u } ^ { t } ) ^ { 2 } } \leq ( \vartheta _ { u } ^ { t } ) ^ { 2 } + \frac { ( v _ { u } ^ { t } ) ^ { 2 } } { v _ { 0 } ^ { 2 } } .\tag{50}
$$

In the k-th iteration, for given speeds $v _ { u } ^ { t } ( k )$ and $\vartheta _ { u } ^ { t } ( k )$ , we ( ) ( )approximate the right-hand-side of the above inequality as

$$
\begin{array} { r l r } & { } & { \frac { 1 } { ( \vartheta _ { u } ^ { t } ) ^ { 2 } } \le ( \vartheta _ { u } ^ { t } ( k ) ) ^ { 2 } + 2 \vartheta _ { u } ^ { t } ( k ) [ \vartheta _ { u } ^ { t } - \vartheta _ { u } ^ { t } ( k ) ] \quad } \\ & { } & { \qquad + \frac { ( v _ { u } ^ { t } ( k ) ) ^ { 2 } + 2 v _ { u } ^ { t } ( k ) [ v _ { u } ^ { t } - v _ { u } ^ { t } ( k ) ] } { v _ { 0 } ^ { 2 } } . } \end{array}\tag{51}
$$

Then, we can approximate $P ( v _ { u } ^ { t } )$ by its upper bound as

$$
\begin{array} { r l r } {  { P ( v _ { u } ^ { t } ) \le \hat { P } ( v _ { u } ^ { t } ) = P _ { 0 } ( 1 + \frac { 3 ( v _ { u } ^ { t } ) ^ { 2 } } { U _ { t i p } ^ { 2 } } ) + P _ { 1 } \vartheta _ { u } ^ { t } } } \\ & { } & { + \displaystyle \frac { 1 } { 2 } d _ { 0 } \rho s A _ { r } ( v _ { u } ^ { t } ) ^ { 3 } . } \end{array}\tag{52}
$$

Based on the above discussion, all non-convexity in problem $\mathcal { P } _ { 3 - 3 }$ has been solved. The original problem in the k-th iteration

can be reformulated as the following approximate form

$$
\begin{array} { r l } & { \displaystyle | s . L . ~ C _ { 5 } - C \tau , C _ { 9 } , } \\ & { \displaystyle C _ { 8 } : d _ { \mathrm { m i n } } ^ { 2 } \leq - | | Q _ { u } ^ { l } ( k ) - Q _ { i } ^ { l } ( k ) | | ^ { 2 } } \\ & { \displaystyle + 2 ( Q _ { u } ^ { l } ( k ) - Q _ { i } ^ { l } ( k ) ) ^ { T } ( Q _ { u } ^ { l } - Q _ { i } ^ { l } ) , \forall u \in \mathcal { U } , \forall i \in \mathcal { U } \backslash \{ u \} , } \\ & { \displaystyle C _ { 1 0 } : \hat { E } _ { u } = E _ { u , e } + \sum _ { t \in T } \sum _ { m \in \mathcal { A } } \sum _ { s \in \mathcal { B } } p _ { u } \left( \sum _ { i \in \mathcal { A } \backslash \{ u \} } x _ { m , s , u , i } ^ { t } \frac { I _ { m , s } ^ { t } } { W _ { 2 } \hat { e } _ { u , s } ^ { t } } \right. } \\ & { \displaystyle \left. + x _ { m , s , u , b } ^ { t } \frac { I _ { m , s } ^ { t } } { W _ { i } \hat { e } _ { u , b } ^ { t } } \right) + \sum _ { t \in T } \Delta _ { t } P ( v _ { u } ^ { t } ) \leq E _ { t h , \forall u \in \mathcal { U } , } } \\ & { \displaystyle C _ { 1 1 } : \hat { F } _ { m , s } ^ { t } \leq D _ { m , s } ^ { t } , \forall m \in \mathcal { M } , \forall s \in \mathcal { S } . } \end{array}\tag{53}
$$

Lemma 4: The subproblem $\mathcal { P } _ { 3 - 3 } ^ { \prime }$ is convex.

Proof: For $\hat { F } _ { m , s } ^ { t } .$ , we can simplify it into $y = [ \kappa ( x ) ] ^ { 2 }$ where $x \geq 0$ = [ ( )]. Thus, we can get the second-order derivative of y w.r.t. x, as shown below.

$$
{ \frac { d ^ { 2 } y } { d x ^ { 2 } } } = 2 \left( \left( { \frac { d \kappa } { d x } } \right) ^ { 2 } + \kappa ( x ) { \frac { d ^ { 2 } \kappa } { d x ^ { 2 } } } \right) .\tag{54}
$$

It is obvious that $\kappa ( x ) > 0 , \forall x \geq 0$ . Since $\kappa ( x )$ is a convex function, we have $d ^ { 2 } \kappa / ( d x ^ { 2 } ) > 0$ 0 ( ). Consequently, we conclude that $d ^ { 2 } y / ( d x ^ { 2 } ) > 0$ , âx â¥ . Furthermore, we can find that $( \hat { F } _ { m , s } ^ { t } ) ^ { 2 }$ is a convex function, which leads to the convexity of ( )problem $\mathcal { P } _ { 3 - 3 } ^ { \prime } .$ -

After proving the convexity of this problem, the optimal solution for UAV trajectory can be obtained by CVX. It is noted that the optimal solution obtained from approximate problem $\mathcal { P } _ { 3 - 3 } ^ { \prime }$ is the lower bound of problem $\mathcal { P } _ { 3 - 3 }$

## D. Joint Computing and Bandwidth Resource Allocation

In this subsection, we study the joint computing and bandwidth resource allocation optimization with fixed the other variables Q, A, X , which is formulated as

$$
\begin{array} { r l r } & { \mathcal { P } _ { 3 + 4 } : \frac { 1 } { R _ { 1 } \epsilon } \frac { 1 } { T _ { \epsilon } } \frac { \lambda ^ { 2 } } { \epsilon } \frac { \lambda ^ { 3 } } { 2 } \epsilon \frac { \epsilon } { R _ { 1 } \epsilon } , } & { \langle \Xi ^ { \prime } \rangle } \\ & { } & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad } & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ &  \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \ \end{array}\tag{5}
$$

$$
\begin{array} { r l } & { \quad = \hat { a } _ { \mathrm { i } } ^ { \dagger } , \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad = \hat { a } _ { \mathrm { i } } ^ { \dagger } , \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ &  \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad  \end{array}
$$

Lemma 5: The subproblem $\mathcal { P } _ { 3 - 4 }$ is convex optimization problem w.r.t $b _ { m , s } ^ { t } > 0$ and $f _ { m , s , u } ^ { t } > 0$

0 0Proof: It is obvious that the constraints $C _ { 2 } , C _ { 3 } , C _ { 1 0 }$ and $C _ { 1 5 }$ are convex w.r.t resource allocation variables $( B , F )$ . Next, we prove that the objective function of constraint $C _ { 1 1 }$ )and subproblem $\mathcal { P } _ { 3 - 4 }$ is convex [42]. In constraint $C _ { 1 1 }$ and the objective function, the third term is clearly convex, for the first and second terms, we define $f ( x , y ) = \frac { a } { x } + \frac { b } { y } \left( \forall x , y > 0 \right)$ where $a > 0$ and $b > 0$ are constants. Then, we can obtain its Jacobian matrix as 0follows

$$
\nabla f ( x , y ) = \left[ { \frac { \partial f } { \partial x } } \quad { \frac { \partial f } { \partial y } } \right] = \left[ - { \frac { a } { x ^ { 2 } } } \quad - { \frac { b } { y ^ { 2 } } } \right] .\tag{56}
$$

Thus, we can derive the Hessian of $f ( x , y )$ as

$$
\nabla ^ { 2 } f ( x , y ) = \left[ { \begin{array} { c c } { { \frac { \partial ^ { 2 } f } { \partial x ^ { 2 } } } } & { { \frac { \partial ^ { 2 } f } { \partial x \partial y } } } \\ { { \frac { \partial ^ { 2 } f } { \partial y \partial x } } } & { { \frac { \partial ^ { 2 } f } { \partial y ^ { 2 } } } } \end{array} } \right] = \left[ { \begin{array} { c c } { { \frac { 2 a } { x ^ { 3 } } } } & { 0 } \\ { 0 } & { { \frac { 2 b } { y ^ { 3 } } } } \end{array} } \right] .\tag{57}
$$

Accordingly, the determinant of the Hessian of $f ( x , y )$ is

$$
| \nabla ^ { 2 } f ( x , y ) | = { \frac { 4 a b } { x ^ { 3 } y ^ { 3 } } } > 0 .\tag{58}
$$

Therefore, constraint $C _ { 1 1 }$ is convex because of the convexity of the sum of convex function. -

Since problem $\mathcal { P } _ { 3 - 4 }$ is convex, we adopt CVX to obtain the solution for bandwidth and computing resources allocation.

## E. Overall Alternating Algorithm, Convergence and Complexity

We propose an alternating optimization to solve the problem $P _ { 3 }$ , as shown in Algorithm 3. The key idea is to iteratively optimize task offloading, service caching, UAV trajectory as well as computing and bandwidth resources allocation until the objective function value converges. The theoretical analysis of convergence and complexity is as follows.

Algorithm 3: Joint Alternating Optimization of Task Of  
floading, Service Caching, UAV Trajectory and Resource   
Allocation.   
Input: Set the initial solution $( Q ^ { 0 } , A ^ { 0 } , X ^ { 0 } , B ^ { 0 } , F ^ { 0 } )$ , the   
tolerance 
.   
Output: The optimal solutions $\eta ^ { * } , \{ Q ^ { * } , A ^ { * } , X ^ { * } , B ^ { * } , F ^ { * } \}$   
to problem $\mathcal { P } _ { 3 }$   
1: Initialize $\eta _ { 0 } = 1 ,$ , and the outer loop index $i = 0 ;$   
2: repeat   
3: Initialize the inter loop index $j = 0 ;$   
4: repeat   
5: Solve problem $\mathcal { P } _ { 3 - 1 }$ for given $Q ^ { i } , A ^ { i } , B ^ { i } , F ^ { i }$ and   
$\eta ^ { i }$ , and obtain the optimal value $X ^ { i }$ based on   
Algorithm 1;   
6: Update $\{ X ^ { i } \}  \{ X ^ { j + 1 } \}$ ;   
7: Solve problem $\mathcal { P } _ { 3 - 2 }$ for given $Q ^ { i } , X ^ { i } , B ^ { i } , F ^ { i }$ and   
$\eta ^ { i } .$ , and obtain the optimal value $A ^ { i }$ based on   
Algorithm 2;   
8: Update $\{ A ^ { i } \}  \{ A ^ { j + 1 } \}$ ;   
9: Solve problem $\mathcal { P } _ { 3 - 3 }$ for given $A ^ { i } , X ^ { i } , B ^ { i } , F ^ { i }$ and   
$\eta ^ { i } .$ , and obtain the optimal value $Q ^ { i }$ based on SCA   
technique;   
10: Update $\{ Q ^ { i } \}  \{ Q ^ { j + 1 } \} ;$ ;   
11: Solve problem $\mathcal { P } _ { 3 - 4 }$ for given $Q ^ { i } , A ^ { i } , X ^ { i }$ and $\eta ^ { i }$ ,   
and obtain the optimal value $B ^ { i }$ and $F ^ { i }$ based on   
CVX method;   
12: Update $\{ B ^ { i } , F ^ { i } \}  \{ B ^ { j + 1 } , F ^ { j + 1 } \}$   
13: Update $j = j + 1 ;$   
14: until $\{ \bar { Q } ^ { j + 1 } , A ^ { j + 1 } , X ^ { j + 1 } , B ^ { j + 1 } , F ^ { j + 1 } \}$   
converge to the anticipant accuracy;   
15: Update $\{ Q ^ { i + 1 } , A ^ { i + 1 } , X ^ { i + 1 } , B ^ { i + 1 } , F ^ { i + 1 } \} $   
$\{ \hat { Q } ^ { j + 1 } , \tilde { A } ^ { j + 1 } , X ^ { j + 1 } , B ^ { j + 1 } , F ^ { j + 1 } \} ;$   
16: Update the Dinkelbach auxiliary variable   
$\mathrm { ~  ~ \mu ~ } _ { n ^ { i + 1 } } = \frac { \mathrm { ~  ~ \sum ~ } _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } ^ { i + 1 } } { \mathrm { ~  ~ \sum ~ } _ { m = 1 } ^ { \cal { N } } \sum _ { s = 1 } ^ { S } \bar { F } _ { m , s } ^ { i + 1 } }$   
$\begin{array} { r } { \overline { { M \cdot \sum _ { m = 1 } ^ { M } \sum _ { s = 1 } ^ { S } ( \bar { F } _ { m , s } ^ { i + 1 } ) ^ { 2 } } } , } \end{array}$   
17: Update $i = i { \overline { { + } } } 1 ;$   
18: until $| f ( \eta ^ { i + 1 } ) - f ( \eta ^ { i } ) | \leq \epsilon ;$   
19: Update $\eta ^ { * }  \eta ^ { i + 1 } , \{ Q ^ { * } , A ^ { * } , X ^ { * } , B ^ { * } , F ^ { * } \} $   
$\{ \stackrel { . } { Q } ^ { i + 1 } , \stackrel { . } { A } ^ { i + 1 } , \stackrel { . } { X } ^ { i + 1 } , \stackrel { . } { B } ^ { i + 1 } , \stackrel { . } { F } ^ { i + 1 } \}$

Lemma 6: The Algorithm 3 is convergent.

Proof: Algorithm 3 solves the fractional programming problem by adopting the Dinkelbachâs method in the outer loop. The convergence of the Dinkelbachâs method is proven in [40]. To verify the convergence performance of Algorithm 3, we need to prove that, when the sequence $( Q ^ { j } , A ^ { j } , \bar { X } ^ { j } )$ is updated, (the objective function value of problem $\mathcal { P } _ { 1 } ( Q ^ { j } , A ^ { j } , X ^ { j } )$ keeps non-decreasing. By Algorithm 3, we have

$$
\begin{array} { r l } & { \mathcal { P } _ { 1 } ^ { j - 1 } = \mathcal { P } _ { 1 } ( Q ^ { j - 1 } , A ^ { j - 1 } , X ^ { j - 1 } , B ^ { j - 1 } , F ^ { j - 1 } ) } \\ & { \qquad \leq \mathcal { P } _ { 1 } ( Q ^ { j - 1 } , A ^ { j - 1 } , X ^ { j } , B ^ { j - 1 } , F ^ { j - 1 } ) } \\ & { \qquad \leq \mathcal { P } _ { 1 } ( Q ^ { j - 1 } , A ^ { j } , X ^ { j } , B ^ { j - 1 } , F ^ { j - 1 } ) } \\ & { \qquad \leq \mathcal { P } _ { 1 } ( Q ^ { j } , A ^ { j } , X ^ { j } , B ^ { j - 1 } , F ^ { j - 1 } ) } \end{array}
$$

TABLE I SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Settings</td><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Settings</td></tr><tr><td rowspan=1 colspan=1> $\overline { { T } }$ </td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1> $\overline { { W _ { 0 } } }$ </td><td rowspan=1 colspan=1>20 MHz</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \Delta _ { t } } }$ </td><td rowspan=1 colspan=1>0.5 s</td><td rowspan=1 colspan=1> $\overline { { W _ { 1 } } }$ </td><td rowspan=1 colspan=1>10 MHz</td></tr><tr><td rowspan=1 colspan=1> $\underline { { v _ { m a x } } }$ </td><td rowspan=1 colspan=1> $\overline { { 3 0 ~ \mathrm { m / s } } }$ </td><td rowspan=1 colspan=1> $\overline { { B } }$ </td><td rowspan=1 colspan=1>20 MHz</td></tr><tr><td rowspan=1 colspan=1> $\underline { { d _ { m i n } } }$ </td><td rowspan=1 colspan=1>2 m</td><td rowspan=1 colspan=1> ${ \underline { { p _ { m } } } }$ </td><td rowspan=1 colspan=1>0.2W</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { u a v } } }$ </td><td rowspan=1 colspan=1>150m</td><td rowspan=1 colspan=1> $p _ { u }$ </td><td rowspan=1 colspan=1>0.5W</td></tr><tr><td rowspan=1 colspan=1> $\overline { { h } }$ </td><td rowspan=1 colspan=1>100 m</td><td rowspan=1 colspan=1> $\overline { { \mathcal { F } _ { u } } }$ </td><td rowspan=1 colspan=1>20 GHz</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { u } } }$ </td><td rowspan=1 colspan=1>100m</td><td rowspan=1 colspan=1>K</td><td rowspan=1 colspan=1>10-27</td></tr></table>

$$
\leq \mathcal { P } _ { 1 } ( Q ^ { j } , A ^ { j } , X ^ { j } , B ^ { j } , F ^ { j } ) = \mathcal { P } _ { 1 } ^ { j } ,\tag{59}
$$

where the first inequality holds because of the optimality of $X ^ { j }$ by Algorithm 1. The second inequality holds due to the optimality of $A ^ { j }$ by Algorithm 2. The third inequality holds because of the suboptimality of $Q ^ { j }$ by the SCA technique. The fourth inequality holds due to the optimality of $B ^ { j }$ and $F ^ { j }$ by CVX. Therefore, the objective function of original problem is always non-decreasing after each iteration, which is also finitely upper-bounded. -

We suppose that Algorithm 3 runs $I _ { \mathrm { m a x } } \times J _ { \mathrm { m a x } }$ iterations, where the loop for the Dinkelbachâs method repeats $I _ { \mathrm { m a x } }$ times, and $J _ { \mathrm { m a x } }$ is the inner iterations for solving four subproblems. The task offloading decisions can be resolved by Algorithm 1 within $O ( U \times M _ { 1 } )$ iterations. Let $M _ { 1 } = | \mathcal { M } _ { u } ^ { e x e } |$ denote the ( ) =number of UEs served by the UAV u. The service caching decisions can be tackled by Algorithm 2 within $O ( U \times S )$ iterations. The computational complexity of solving subproblems $\mathcal { P } _ { 3 - 3 }$ and $\mathcal { P } _ { 3 - 4 }$ is roughly $O ( \bar { U } ^ { 3 } M ^ { 3 } )$ . The overall complexity of Algorithm 3 is $O ( \bar { I _ { \mathrm { m a x } } } J _ { \mathrm { m a x } } ( U M _ { 1 } + U S + 2 U ^ { 3 } M ^ { 3 } ) )$ . It is ( ( + + 2obvious that the above complexity is polynomial.

## VI. SIMULATION RESULTS

In this section, we conduct extensive simulations to verify the effectiveness and performance of our proposed algorithm.

## A. Simulation Settings

The setting of simulation parameters follows the existing works [26], [34], [37]. We consider a UAV-assisted cellular network where 20 UEs $( M = 2 0 )$ are randomly distributed in ( = 20)a rectangle-shaped area with the side length of $x _ { \mathrm { m a x } } = 5 0 0$ m and $y _ { \mathrm { m a x } } = 5 0 0 \mathrm { m }$ . There are a static MBS and 5 $\mathrm { \Delta U A V s } \left( U = 5 \right)$ deployed within this area. The MBS can provide $S = 1 0$ types = 10of services for UEs. For different types of service caches, its required storage size $c _ { s } \in [ 0 . 5 , 1 ]$ , while the storage capacity of each UAV $K _ { u } = 3$ [0 5 1]. We assume that each UAV has the same = 3energy budget and computation capacity. Besides, in time slot t, UE m generates a task requiring service s with input data size $I _ { m , s } ^ { t } \in [ 1 0 , 1 0 0 ]$ KB, required CPU $W _ { m , s } ^ { t } \in [ 2 \times 1 0 ^ { 8 } , 2 \times 1 0 ^ { 9 } ]$ [10 100]cycles, tolerable delay $D _ { m , s } ^ { t } \in [ 4 0 , 5 0 ] \mathrm { ~ s ~ }$ [2 10 2 10 ]. Unless otherwise [40 50]stated, other system settings follow the 3GPP specification [34], shown in Table I.

Inspired by [29], to demonstrate the effectiveness and efficiency of our proposed algorithm, we use the following three performance metrics:

Service experience ratio: The ratio of the fairness among UEs to average service delay during task period.

- Average service delay: The average service delay of each UE and the sum of average service delay of all UEs.

- Fairness index: The fairness of service delay among UEs based on formula (24).

As mentioned earlier, our system setup involves the interactions among UEs, UAVs, and the MBS. To better evaluate the performance of our proposed algorithm, we provide simulation results and compare it with three baseline methods as follows.

1) Greedy with CVX-based resource optimization algorithm (GCR): Each task is offloaded or relayed to the nearest UAV until the UAV that caches the service required by the task is found. In addition, the computing and bandwidth resources allocation are optimized.

2) Fixed resource allocation (FRA) [26]: The service caching, task offloading and UAV trajectory are optimized while ignoring the computing and bandwidth optimization.

3) Non-cooperative offloading algorithm (NCOA) [32]: Without considering UAV collaboration, the UAV executes the tasks generated by associated UEs locally, or further relay them to the MBS. The UAV needs to cache the service required by the task to perform computation.

## B. Numerical Results

This section analyzes the comparison results from aspects such as trajectory planning, convergence performance, number of UEs, computing capacity, coverage range, storage capacity, and communication ability.

Fig. 2 depicts the optimized trajectories of four UAVs projected onto a two-dimensional (2D) plane during different task periods. In this figure, black dots denote the locations of UEs, while black triangle represents the location of MBS. During the task period N , to avoid collisions between UAVs, the trajectories of UAV 1, UAV 2, UAV 3 and UAV 4 do not intersect. When $N = 3 0 ~ \mathrm { s } ,$ the trajectory of each UAV is sampled every 2.5 s, = 30while when $N = 6 0 ~ \mathrm { s }$ and $N = 1 2 0 ~ \mathrm { s }$ , the trajectory of each = 60 = 120UAV is sampled every 5 s. As N increases, the flight trajectory of the UAV becomes closer to UEs. When N is large enough, such as $N = 1 2 0 ~ \mathrm { s }$ , the UAV can visit most UEs in sequence, = 120even keeps stationary above some UEs for several time slots. When N is large enough, the coverage range among UAVs may overlap. Thus, UAVs can adjust their trajectories cover all UEs in a collaborative manner to reduce the service delay and ensure the fairness among UEs.

As described in Fig. 3, we present the convergence performance of our proposed algorithm. We can obvious that our proposed algorithm converges to a stable value after four iterations under different U, which implies that the convergence speed of our proposed algorithm is fast. Specifically, the more UAVs there are, the higher the service experience ratio. This is because more UAVs fully leverage their collaborative effects to provide lower service delay for UEs. Besides, when the number of UAVs is 6, i.e., U  , we find that the service experience of UEs improved by 78.6% compared to $U = 4 ,$ , which confirms the effectiveness = 4of our proposed algorithm in multi-UAV scenario.

<!-- image-->  
Fig. 2. Optimized UAV trajectories under different task period N .

<!-- image-->  
Fig. 3. Convergence performance of our proposed algorithm.

We change the number of UEs that the UAVs need to serve. As illustrated in Fig. 4, we show the average fairness index of each UEâs service delay achieved by the GCV, FRA, NCOA and our proposed algorithm. We observe that as the number of UEs increases, the average fairness index decreases. It is evident the distribution of UEs may be more dispersed and less bandwidth and computing resources allocated to each UE. Besides, due to the optimization of resource allocation and UAV trajectory, our proposed algorithm can guarantee high fairness when there are a large number of UEs.

<!-- image-->  
Fig. 4. Average fairness index with different number of UEs.

<!-- image-->

From Fig. 5, we can see the performance comparison for different numbers of UAVs. As the number of UAV increases, the service experience ratio achieved by our proposed algorithm monotonically improves, since more UAVs can provide higher coverage. When the number of UAV is over 5, the UAVs cache most of the services required by tasks and have more computing and communication resources.

Fig. 5. Service experience ratio with different number of UAVs.

We study the value of service delay obtained by our proposed algorithm and the other three comparison algorithms. Fig. 6 shows the box plot of the average service delay. The average service delay achieved by our proposed algorithm falls in the interval [24.1, 40.4] s and has an average of 33.4 s. It can be concluded that our proposed algorithm can achieve lower average service delay and smaller fluctuation than the other three comparison algorithms, which further verifies that our proposed algorithm improves the service experience of all UEs. Due to the collaboration of UAVs, there are more reduction in average service delay.

In Fig. 7, we show how service experience ratio of all UEs changes as the UAVâs computation capacity $\mathcal { F } _ { u }$ increases from

Fig. 6. Comparison of average service delay under four approaches.  
<!-- image-->

<!-- image-->  
Fig. 7. Service experience ratio versus the computation capacity of each UAV.

10 to 24 GHz. We can find that the service experience ratio increases as the computing capacity increases. Specially, as the UAVâs computation capacity increases, the average service delay reduces, which results in the improvement on the service experience of all UEs. Moreover, the service experience ratio will not increase when the computation capacity exceeds a certain value due to the limitation of the UAVâs storage capacity and energy budget. On average, the service experience ratio achieved by our proposed algorithm is about 54%, 32% and 23% higher than those of the GCR, FRA and NCOA, respectively.

From Fig. 8, we can observe that the service experience ratio increases gradually with the coverage range of each UAV increases. The reason is that enlarging coverage range will lead to more covered UEs, resulting in higher service experience ratio. It can be seen from Fig. 8 that the performance improvement of GCR is slight compared with other algorithms. The reason is that UEs in GCR select the nearest UAV to access. Therefore, the coverage range has a limited influence on the service experience. Our proposed algorithm can greatly improve the service experience ratio by 62%, 36% and 17% compared with the GCR, FRA and NCOA, respectively.

<!-- image-->  
Fig. 8. Service experience ratio versus the coverage range of each UAV.

<!-- image-->  
Fig. 9. Service experience ratio versus the storage capacity of the UAV.

Fig. 9 displays the impact of the UAVâs storage capacity on the service experience ratio. With the increasing amount of the storage capacity, the service experience ratio of all UEs presents an upward trend. When the number of UEs remains unchanged, the probability of services requested by the UE being stored at the UAV cache increases as the UAVâs storage capacity increases. When the storage capacity is relatively small, the difference in service experience ratio achieved by four approaches is not significant, since most of tasks are offloaded to the MBS. When the storage capacity increases to a certain level so that all services can be stored in the cache, the increase of the storage capacity will not lead to higher service experience ratio. The average service experience ratio of our proposed algorithm is 31% and 16% higher than those of the FRA and NCOA.

Fig. 10 depicts the service experience ratio for different values of the bandwidth $W _ { 0 } .$ In the experiment, the bandwidth of each UAV ranges from [5, 30] MHz. As expected, an increase in the bandwidth leads to a higher service experience ratio. Comparing the results of our proposed algorithm with the other three algorithms, it can be seen that our proposed algorithm outperforms other algorithms. Specially, the GCR is always associated with the nearest UAV, which may cause uplink congestion. There is a big gap between the GCR with the other three algorithms. The average service experience ratio of our proposed algorithm is 55% and 15% higher than those of the GCR and NCOA.

<!-- image-->  
Fig. 10. Service experience ratio versus the bandwidth $W _ { 0 }$ of the UAV.

<!-- image-->  
Fig. 11. Service experience ratio versus different number of UEs.

In Fig. 11, we describe the service experience ratio for different number of UEs. We can find that the proposed algorithm outperforms the other two baseline algorithms, FRA and NCOA. The task offloading and service caching subproblems with binary variables are integer linear programming, and the optimal task offloading and service caching placement decisions can be found by the branch and bound (BnB) method. However, the BnB has a high computational complexity of $O ( 2 ^ { M U } + 2 ^ { U S } )$ . (2 + 2 )The computational complexity of the proposed Algorithms 1 and 2 is roughly $O ( M U + U S )$ , which is much lower than BnB. ( + )The performance gap between our proposed algorithm and the optimal algorithm BnB is very small, which can demonstrate the near-optimality of our algorithm.

<!-- image-->  
Fig. 12. Performance comparison between the proposed algorithm and other algorithms.

As shown in Fig. 12, we conduct the performance comparison between our proposed algorithm and other algorithms. We also compare our proposed algorithm with the other algorithm, i.e., the near optimal caching placement by greedy algorithm (CpG) [25]. It can be found that the proposed algorithm can reach a near-optimal performance to BnB, and outperform the other two baseline algorithms in improving the service experience ratio. The reason is that our task offloading algorithm and service caching placement algorithm play an important role in multi-UAV collaboration.

## VII. CONCLUSION

This article studies the service experience ratio maximization. We aim to reduce service delay while ensuring fairness between UEs. To maximize the service experience, we consider the joint optimization of task offloading, resource allocation, trajectory planning, and service cache placement under the constraints of UAVâs energy and delay requirements. The original problem is a mixed-integer non-convex programming problem with a fractional structure. We first transform the fractional problem into a parametric programming form based on Dinkelbachâs method. Next, we design a four-stage alternating iteration algorithm to maximize the service experience ratio. Numerical results demonstrate that an appropriate trade-off between service delay and fairness among all UEs.

## REFERENCES

[1] M. Asim, Y. Wang, K. Wang, and P.-Q. Huang, âA review on computational intelligence techniques in cloud and edge computing,â IEEE Trans. Emerg. Topics Comput. Intell., vol. 4, no. 6, pp. 742â763, Dec. 2020.

[2] P. A. Apostolopoulos, G. Fragkos, E. E. Tsiropoulou, and S. Papavassiliou, âData offloading in uav-assisted multi-access edge computing systems under resource uncertainty,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 175â190, Jan. 2023.

[3] J. Chen et al., âDeep reinforcement learning based resource allocation in multi-UAV-aided mec networks,â IEEE Trans. Commun., vol. 71, no. 1, pp. 296â309, Jan. 2023.

[4] Z. Yang, S. Bi, and Y.-J. A. Zhang, âOnline trajectory and resource optimization for stochastic UAV-enabled MEC systems,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5629â5643, Jul. 2022.

[5] W. Liu, B. Li, W. Xie, Y. Dai, and Z. Fei, âEnergy efficient computation offloading in aerial edge networks with multi-agent cooperation,â IEEE Trans. Wireless Commun., vol. 22, no. 9, pp. 5725â5739, Sep. 2023.

[6] X. Gao, X. Zhu, and L. Zhai, âMinimization of aerial cost and mission completion time in multi-UAV-enabled IoT networks,â IEEE Trans. Commun., vol. 71, no. 9, pp. 5335â5347, Sep. 2023.

[7] X. Zhu, L. Zhai, N. Li, Y. Li, and F. Yang, âMulti-objective deployment optimization of UAVs for energy-efficient wireless coverage,â IEEE Trans. Commun., early access, Jan. 22, 2024, doi: 10.1109/TCOMM.2024.3356795.

[8] Y. Liu, K. Xiong, Q. Ni, P. Fan, and K. B. Letaief, âUAV-assisted wireless powered cooperative mobile edge computing: Joint offloading, CPU control, and trajectory optimization,â IEEE Internet Things J., vol. 7, no. 4, pp. 2777â2790, Apr. 2020.

[9] L. Yang, H. Yao, J. Wang, C. Jiang, A. Benslimane, and Y. Liu, âMulti-UAV-enabled load-balance mobile-edge computing for IoT networks,â IEEE Internet Things J., vol. 7, no. 8, pp. 6898â6908, Aug. 2020.

[10] Z. Yang, C. Pan, K. Wang, and M. Shikh-Bahaei, âEnergy efficient resource allocation in UAV-enabled mobile edge computing networks,â IEEE Trans. Wireless Commun., vol. 18, no. 9, pp. 4576â4589, Sep. 2019.

[11] V. Farhadi et al., âService placement and request scheduling for dataintensive applications in edge clouds,â IEEE/ACM Trans. Netw., vol. 29, no. 2, pp. 779â792, Apr. 2021.

[12] T. Ouyang, Z. Zhou, and X. Chen, âFollow me at the edge: Mobility-aware dynamic service placement for mobile edge computing,â IEEE J. Sel. Areas Commun., vol. 36, no. 10, pp. 2333â2345, Oct. 2018.

[13] S. Song, S. Ma, X. Zhu, Y. Li, F. Yang, and L. Zhai, âJoint bandwidth allocation and task offloading in multi-access edge computing,â Expert Syst. Appl., vol. 217, 2023, Art. no. 119563. [Online]. Available: https: //www.sciencedirect.com/science/article/pii/S0957417423000647

[14] Y. Li et al., âCollaborative content caching and task offloading in multiaccess edge computing,â IEEE Trans. Veh. Technol, vol. 72, no. 4, pp. 5367â5372, Apr. 2023.

[15] Y. Liu, Y. Li, Y. Niu, and D. Jin, âJoint optimization of path planning and resource allocation in mobile edge computing,â IEEE Trans. Mobile Comput., vol. 19, no. 9, pp. 2129â2144, Sep. 2020.

[16] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[17] S. Tang, K. He, L. Chen, L. Fan, X. Lei, and R. Q. Hu, âCollaborative cache-aided relaying networks: Performance evaluation and system optimization,â IEEE J. Sel. Areas Commun., vol. 41, no. 3, pp. 706â719, Mar. 2023.

[18] X. Gao, X. Zhu, and L. Zhai, âAoI-sensitive data collection in multi-UAV-assisted wireless sensor networks,â IEEE Trans. Wireless Commun., vol. 22, no. 8, pp. 5185â5197, Aug. 2023.

[19] T. Zhang, Y. Xu, J. Loo, D. Yang, and L. Xiao, âJoint computation and communication design for UAV-assisted mobile edge computing in IoT,â IEEE Trans. Ind. Informat., vol. 16, no. 8, pp. 5505â5516, Aug. 2020.

[20] C. Deng, X. Fang, and X. Wang, âUAV-enabled mobile-edge computing for AI applications: Joint model decision, resource allocation, and trajectory optimization,â IEEE Internet Things J., vol. 10, no. 7, pp. 5662â5675, Apr. 2023.

[21] X. He, R. Jin, and H. Dai, âMulti-hop task offloading with on-the-fly computation for multi-UAV remote edge computing,â IEEE Trans. Commun., vol. 70, no. 2, pp. 1332â1344, Feb. 2022.

[22] X. Liu, Z. Liu, and M. Zhou, âFair energy-efficient resource optimization for green multi-NOMA-UAV assisted Internet of Things,â IEEE Trans. Green Commun. Netw., vol. 7, no. 2, pp. 904â915, Jun. 2023.

[23] Y. Miao, K. Hwang, D. Wu, Y. Hao, and M. Chen, âDrone swarm path planning for mobile edge computing in industrial Internet of Things,â IEEE Trans. Ind. Informat., vol. 19, no. 5, pp. 6836â6848, May 2023.

[24] J. Li, C. Yi, J. Chen, K. Zhu, and J. Cai, âJoint trajectory planning, application placement and energy renewal for UAV-assisted MEC: A triple-learner based approach,â IEEE Internet Things J., vol. 10, no. 15, pp. 13622â13636, Aug. 2023.

[25] T. Zhang, Y. Wang, Y. Liu, W. Xu, and A. Nallanathan, âCache-enabling UAV communications: Network deployment and resource allocation,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7470â7483, Nov. 2020.

[26] R. Zhou, X. Wu, H. Tan, and R. Zhang, âTwo time-scale joint service caching and task offloading for uav-assisted mobile edge computing,â in Proc. IEEE Conf. Comput. Commun., 2022, pp. 1189â1198.

[27] W. Mao, K. Xiong, Y. Lu, P. Fan, and Z. Ding, âEnergy consumption minimization in secure multi-antenna UAV-assisted MEC networks with channel uncertainty,â IEEE Trans. Wireless Commun., vol. 22, no. 11, pp. 7185â7200, Nov. 2023.

[28] L. P. Qian, H. Zhang, Q. Wang, Y. Wu, and B. Lin, âJoint multi-domain resource allocation and trajectory optimization in UAV-assisted maritime IoT networks,â IEEE Internet Things J., vol. 10, no. 1, pp. 539â552, Jan. 2023.

[29] Z. Ning et al., â5G-enabled UAV-to-community offloading: Joint trajectory design and task scheduling,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3306â3320, Nov. 2021.

[30] L. X. Nguyen, Y. K. Tun, T. N. Dang, Y. M. Park, Z. Han, and C. S. Hong, âDependency tasks offloading and communication resource allocation in collaborative UAV networks: A metaheuristic approach,â IEEE Internet Things J., vol. 10, no. 10, pp. 9062â9076, May 2023.

[31] B. Liu, C. Liu, and M. Peng, âComputation offloading and resource allocation in unmanned aerial vehicle networks,â IEEE Trans. Veh. Technol, vol. 72, no. 4, pp. 4981â4995, Apr. 2023.

[32] Z. Yu, Y. Gong, S. Gong, and Y. Guo, âJoint task offloading and resource allocation in UAV-enabled mobile edge computing,â IEEE Internet Things J., vol. 7, no. 4, pp. 3147â3159, Apr. 2020.

[33] L. Zhao et al., âVehicular computation offloading for industrial mobile edge computing,â IEEE Trans. Ind. Informat., vol. 17, no. 11, pp. 7871â 7881, Nov. 2021.

[34] J. Ji, K. Zhu, and L. Cai, âTrajectory and communication design for cache- enabled UAVs in cellular networks: A deep reinforcement learning approach,â IEEE Trans. Mobile Comput., vol. 22, no. 10, pp. 6190â6204, Oct. 2022.

[35] T. Ren et al., âEnabling efficient scheduling in large-scale UAV-assisted mobile-edge computing via hierarchical reinforcement learning,â IEEE Internet Things J., vol. 9, no. 10, pp. 7095â7109, May 2022.

[36] M. Yi, X. Wang, J. Liu, Y. Zhang, and R. Hou, âMultitask transfer deep reinforcement learning for timely data collection in rechargeable-UAVaided IoT networks,â IEEE Internet Things J., vol. 10, no. 23, pp. 20 545â20 559, Dec. 2023.

[37] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for uav-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[38] C. H. Liu, Z. Chen, and Y. Zhan, âEnergy-efficient distributed mobile crowd sensing: A deep learning approach,â IEEE J. Sel. Areas Commun., vol. 37, no. 6, pp. 1262â1276, Jun. 2019.

[39] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âUAV-assisted MEC networks with aerial and ground cooperation,â IEEE Trans. Wireless Commun., vol. 20, no. 12, pp. 7712â7727, Dec. 2021.

[40] W. Dinkelbach, âOn nonlinear fractional programming,â Manage. Sci., vol. 13, no. 7, pp. 492â498, 1967.

[41] J. Zhang et al., âComputation-efficient offloading and trajectory scheduling for multi-UAV assisted mobile edge computing,â IEEE Trans. Veh. Technol, vol. 69, no. 2, pp. 2114â2125, Feb. 2020.

[42] L. Wang, Q. Zhou, and Y. Shen, âComputation efficiency maximization for UAV-assisted relaying and MEC networks in urban environment,â IEEE Trans. Green Commun. Netw., vol. 7, no. 2, pp. 565â578, Jun. 2023.

<!-- image-->  
Xingxia Gao (Graduate Student Member, IEEE) is currently working toward the masterâs degree with the School of Information Science and Engineering, Shandong Normal University. Her current research interests include UAV, IoT, edge computing.

<!-- image-->

Linbo Zhai (Member, IEEE) received the BS and MS degrees from the School of Information Science and Engineering at Shandong University in 2004 and 2007, respectively, and the PhD degree from the School of Electronic Engineering at Beijing University of Posts and Telecommunications in 2010. From then on, he worked as a teacher in Shandong Normal University. His current research interests include cognitive radio, crowdsourcing and distributed network optimization.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_2_img_1.png|page_2_img_1]]
2. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_12_img_1.png|page_12_img_1]]
3. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_12_img_2.jpeg|page_12_img_2]]
4. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_13_img_1.png|page_13_img_1]]
5. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_13_img_2.png|page_13_img_2]]
6. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_13_img_3.png|page_13_img_3]]
7. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_13_img_4.png|page_13_img_4]]
8. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_14_img_1.png|page_14_img_1]]
9. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_14_img_2.png|page_14_img_2]]
10. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_14_img_3.png|page_14_img_3]]
11. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_14_img_4.png|page_14_img_4]]
12. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_15_img_1.png|page_15_img_1]]
13. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_16_img_1.jpeg|page_16_img_1]]
14. [[../extracted_images/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks/page_16_img_2.jpeg|page_16_img_2]]

---

