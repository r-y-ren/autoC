# User Preference Oriented Service Caching and Task Offloading for UAV-Assisted MEC Networks

Ruiting Zhou , Member, IEEE, Yifeng Huang , Yufeng Wang, Lei Jiao , Member, IEEE, Haisheng Tan , Senior Member, IEEE, Renli Zhang , and Libing Wu

AbstractâUnmanned aerial vehicles (UAVs) have emerged as a new and flexible paradigm to offer low-latency and diverse mobile edge computing (MEC) services for user equipment (UE). To minimize the service delay, caching is introduced in UAV-assisted MEC networks to bring service contents closer to UEs. However, UAVassisted MEC is challenged by the heavy communication overhead introduced by service caching and UAVâs limited energy capacity. In this article, we propose an online algorithm, OOA, that jointly optimizes caching and offloading decisions for UAV-assisted MEC networks, to minimize the overall service delay. Specifically, to improve the caching effectiveness and reduce the caching overhead, OOA employs a greedy algorithm to dynamically make caching decisions based on UEsâ preferences on services and UAVsâ historical trajectories, with the goal of maximizing the probability of successful offloading. To realize the rational utilization of energy from a long-term perspective, OOA decomposes the online problem into a series of single-slot problems by scaling the UAVâs energy constraint into the objective, and iteratively optimizes UAV trajectory and task offloading at each time slot. Theoretical analysis proves that OOA converges to a suboptimal solution with polynomial time complexity. Extensive simulations based on real world data further show that OOA can reduce the service delay by up to 33% while satisfying the UAVâs energy constraint, compared to three state-of-the-art algorithms.

Index TermsâUnmanned aerial vehicles, mobile edge computing, service caching, task offloading.

Received 21 April 2023; revised 23 December 2024; accepted 8 January 2025. Date of publication 13 February 2025; date of current version 10 April 2025. This work was supported in part by the National Key Research and Development Program of China under Grant 2024YFB2907100, in part by Shenzhen Science and Technology Program under Grant KJZD20240903100814018, in part by the National Natural Science Foundation of China under Grant 62232004, in part by the Central University Basic Research Fund of China under Grant 2242024K40021, in part by the Collaborative Innovation Center of Novel Software Technology and Industrialization, and in part by the Big Data Computing Center of Southeast University, as well as in part by the U.S. National Science Foundation under Grant CNS-2047719. (Corresponding author: Lei Jiao.)

Lei Jiao is with the Center for Cyber Security and Privacy, University of Oregon, Eugene, OR 97403 USA (e-mail: ljiao2@uoregon.edu).

## I. INTRODUCTION

T HE rapid development of 5G promotes the application ofcomputing-intensive and data-driven smart services, such computing-intensive and data-driven smart services, such as online games and automatic driving [1]. To meet the computing power and low-latency requirements of smart services, mobile edge computing (MEC) has been proposed to transfer the computing tasks of user equipment (UE) to the network edge for processing [2]. Unfortunately, MEC servers need to be deployed on fixed infrastructure, such as base stations (BSs), which incurs high deployment costs. MEC may not be able to work effectively in rural areas that lack sufficient infrastructures or urban areas during peak hours/natural disasters. In recent years, Unmanned Aerial Vehicles (UAVs) equipped with MEC servers have been widely discussed in industry and academia [3]. UAVs can provide low-latency and more flexible computing services due to their high mobility and flexible deployment. For example, on July 21, 2021, Mihe town in China was flooded due to heavy rainfall. In its communication interruption area, 255 UAVs form mobile base stations to provide communication signal that covers 50 square kilometers for five hours [4].

To fully realize UAV-assisted MEC, both service caching and task offloading are required. On the one hand, it has been shown that some popular content is repeatedly requested by UEs [5], [6]. By caching some popular content to UAVs nearby UEs and reusing the stored content, caching is considered to be an effective approach to reduce the service delay. In addition, many popular applications are data-driven and require caching some service content, such as libraries and machine learning models, on the UAVâs edge server [7], [8]. On the other hand, offloading computing-intensive and latency-sensitive tasks to UAVs can solve the shortcomings of UEs in terms of computation resources and battery capacities.

However, service caching and task offloading in UAV-assisted MEC face fundamental challenges. First, how to dynamically place and update cache contents in UAVs is challenging. Because one UAV has limited storage space, only some services can be cached. Furthermore, UEâs location and preference for services may change over time, but the frequent download of service contents from the remote cloud brings heavy communication overhead. Second, although the mobility of the UAV increases its flexibility, its flight trajectory significantly affects the number of UEs that the UAV can serve, and ultimately impacts the service delay. Therefore, UAV trajectory needs to be optimized to facilitate the deployment of UAV-assisted MEC. Third, due

Digital Object Identifier 10.1109/TSC.2025.3536319

Haisheng Tan is with the School of Computer Science and Technology, Key Laboratory of Wireless-Optical Communications, Chinese Academy of Sciences, University of Science and Technology of China, Langfang 101127, China (e-mail: hstan@ustc.edu.cn).

to the limited computation/communication resource and the battery capacity of a UAV, one UAV can only process a certain number of tasks for a period of time [9], [10]. Making offloading decisions for all tasks requires long-term and rational utilization of the resources and the energy.

Existing service caching or offloading in MEC studies the fixed edge or cellular networks [5], [6], [7], [11], [12], [13]. Their approaches cannot solve the service caching or offloading problem in UAV-assisted MEC, since they didnât consider UAV trajectory planing. In the related studies of UAV-assisted MEC, most studies only study service caching [14], [15], [16] or task offloading [17], [18], [19], [20], [21] alone, and do not consider both. A few papers consider both service caching and task offloading. Their solutions are either in offline scenarios [22], [23], or they only update the cache according to the task offloaded by UEs at the current time, ignoring the historical task information. Their caching decisions are not efficient since usersâ location and preferences may change over time. The caching decision need to be optimized dynamically from a long-term time scale. We will discuss it in detail in Section II.

In this paper, we model UAVâs important features (i.e., mobility and limited energy), and study the problem of dynamic service caching and task offloading in energy-constrained UAVassisted MEC networks, aiming to minimize the service delay. In order to realize the rational utilization of energy from a long-term perspective, we decouple the problem into a series of single-slot problems by splitting the energy constraint into the objective function. At the beginning of each time slot, we decide whether to update the cache according to the hit rate, i.e., the probability of successful offloading. If the gap between the average hit rate (calculated based on the offloading decision) and the expected hit rate (calculated by the caching decision) reaches the threshold, the cache is updated based on UEsâ preferences on services and UAVsâ historical trajectories to maximize the expected hit rate. In this way, we improve the caching efficiency by observing both offloading results and UEsâ preferences. Furthermore, the frequency of updating the cache can be dynamically adjusted by the threshold to reduce the communication overhead. We then propose an iterative algorithm based on first-order Taylor Expansion and dependent rounding technique to make UAV trajectories and task offloading decisions. Notice that in this paper, service caching and task offloading are jointly optimized within one time slot, not simultaneously. Some of the previous works [23], [24] make service caching and task offloading decisions at the same time. However, making caching decisions and offloading decisions simultaneously causes these papers to fail to consider the historical task information. In contrast, this paper dynamically updates service caching decisions based on historical task information, which improves the hit rate and also reduces the cache update frequency. We highlight our contributions as follows.

We formulate the user preference oriented service caching and task offloading problems in UAV-assisted MEC. The service caching, UAV trajectory and task offloading decisions need to be jointly optimized and made online under energy and resource capacity constraints. To minimize the service delay, the cache is dynamically updated based on the preferences of UEs for services. Both the service caching problem and the task offloading problem are NPhard.

We propose an online algorithm, OOA, that dynamically updates caching decisions and optimizes UAV trajectory and task offloading. For service caching, OOA reformulates the caching problem into a submodular maximization problem and employs a greedy caching algorithm that places services according to the service preferences of UEs. To achieve low latency in the long-term, we splits the energy consumption constraint into the optimization objective by using a weighing factor. The task offloading problem is then decomposed into a series of single-slot problems. OOA then develops an iterative algorithm to optimize UAV trajectory and task offloading.

We conduct rigorous theoretical analysis to prove that OOA converges to a suboptimal solution with polynomial time complexity. Moreover, we conduct extensive simulations based on real world data. Simulations results verify that OOA achieves near-optimal service delay under strict energy constraint. Particularly, OOA can reduce the service delay by up to 33% with 66% energy consumption less than three benchmark algorithms.

In the rest of the paper, we review related work in Section II. The system model of UAV-assisted MEC is introduced in Section III. Our online algorithm, OOA, is proposed in Section IV. The performance of OOA is evaluated in Sections V and VI concludes the paper.

## II. RELATED WORK

## A. Service Caching

Xu et al. [7] investigate service caching in MEC network and develop a game-theoretical mechanism for resource sharing among service providers. In [11] and [12], the authors focus on the cooperative caching in edge computing via distributed online learning. Caching contents considering usersâ content preferences is studied in [5], [6], [13]. However, these studies canât be applied to UAV-assisted MEC directly due to the mobility and energy limit of UAVs. Caching in UAVs has also been studied in recent years. Gu et al. [14] consider content caching, UAV deployments, and transmitting power allocation in Satellite-UAV-Vehicle-Integrated Networks. Zhang et al. [15] use a dynamic UAV trajectory scheduling algorithm to maximize the caching duration. Li et al. [16] minimize expected user delay by using mean field game theory to model caching and trajectory problems. Most of the above papers either consider caching a fixed number of services, assume the size of different services is the same, or fail to give rigorous proof for the theoretical performance of the caching algorithm. Besides, these papers only consider caching and canât make online offloading decisions. Different from these papers, we propose an online algorithm that jointly optimizes service caching, UAV trajectory, and task offloading.

## B. Task Offloading

Wang et al. [17] design an iterative cooperation algorithm to dynamically determine multiple UAVsâ trajectories, seeking the maximization of the number of served demands. Ning et al. [18] aim to maximize the throughput of UAVs by optimizing UAV trajectory and task scheduling. Zhu et al. [19] model the offloading of tasks from a cellular network to a UAV cloudlet as a Markov decision process to minimize the average response time. Both Sun et al. [20] and Tang et al. [21] jointly optimize the UAV trajectory, resource allocation, and task offloading to minimize the energy consumption of the UAV. However, the above papers ignore the problem of service caching. Itâs crucial to study the service caching on UAVs with restricted storage space, since different tasks may demand different services stored on UAVs.

## C. Joint Service Caching and Task Offloading

In [22] and [25], the authors estimate content popularity and deploy UAVs to minimize the request delay. Both Ji et al. [26] and Zhang et al. [27] consider jointly optimizing UAV trajectory, caching placement, and transmitting power to implement content delivery. Nevertheless, these papers canât satisfy the energy limit of UAVs. Wu et al. [28] presents a CNN-based model to make online caching and offloading decisions, yet fails to consider the communication and computation resource limits of UAVs. Qu et al. [23] optimizes service caching, UAV trajectory, computation resource allocation, and task scheduling simultaneously to minimize energy consumption. However, [23] is designed for offline. Zhou et al. [24] develop a two-timescale online service caching and task offloading algorithm for UAV-assisted networks. But [24] updates caching decisions periodically according to tasks received at one time slot, and canât strictly satisfy the energy budget of UAVs. In this paper, we make dynamic service caching, UAV trajectory, and task offloading decisions under strict energy budget constraints. Considering the time-varying services preferences and locations of UEs, we dynamically update caching decisions according to the preferences of UEs for services. Whatâs more, we consider using the energy of UAVs in a reasonable way to minimize the service delay in the long term.

## III. SYSTEM MODEL

## A. System Overview

UAV-assisted MEC Scenario: As shown in Fig. 1, we consider a UAV-assisted MEC system with U rotary-wing UAVs, a base station (BS) and a remote cloud. The system provides S types of services for I terrestrial UEs. Let X denote the integer set $\{ 1 , 2 , \ldots , X \}$ . For example, I denotes $\{ 1 , 2 , \ldots , I \}$ . The 1 2 1 2system time span is divided into T time slots. UEs may generate tasks requiring services at any time slot. Each task requires one specific type of service. To satisfy the delay requirement, all tasks must be processed at one time slot. However, the BS may be overloaded in some scenarios. Thus, some tasks need to be offloaded to the UAVs or the remote cloud. The remote cloud provides ample computing power for all kinds of services while resulting in high communication delay. In order to reduce the delay, services are cached in UAVs in advance. At the beginning of each time slot, BS decides whether to update the cached services in UAVs or not. If so, UEs first upload their personal preferences for services to the BS, and then the BS makes caching decisions according to UEsâ interests. Next, the BS collects tasks from UEs and decides whether to offload them to UAVs or to the remote cloud.

<!-- image-->  
Fig. 1. An illustration of UAV-assisted MEC.

Offloading Requirement: Tasks from UEs can be offload to UAVs only if following two conditions are satisfied: i) the UAV has enough communication and computation resources to process the task; ii) the service that the UEâs task requires is cached in the UAV. Otherwise tasks will be offloaded to the remote cloud.

## B. Service Caching

Caching Strategy: In order to reduce the computation delay, services are pre-cached on UAVs. Let $W _ { u }$ be the storage capacity of UAV u, and the storage space required by service s is denoted by $c _ { s }$ . Due to the preferences of UEs are time-varying, the cache decisions should be dynamic updated.

UE Preference: The intuition in designing efficient caching strategy is to cache services according to the preference of UEs. Let $P _ { i , s } \in [ 0 , 1 ]$ be the probability of UE i generating a task [0 1]requiring service s. Since one UE can generate multiple tasks at the same time, the expectation of the number of tasks generated by UE i is $\textstyle \sum _ { i } P _ { i , s }$ . At first, $P _ { i , s }$ is uploaded by UEs. As the BS processes more tasks from UEs, the BS will update $P _ { i , s }$ based on the historical information of tasks.

Decision Variables and Hit Ratio: The BS decides which services to cache. Let $x _ { u , s }$ denote whether service s is cached in UAV $u \ : ( \ : x _ { u , s } = 1 )$ or not $( \mathit { x } _ { u , s } = 0 )$ . Similar to [5], [29], = 1 = 0[30], the hit ratio is used to measure the performance of a caching strategy. The hit ratio of UE i is the probability that tasks generated by UE i can be offloaded to UAVs:

$$
H _ { i , a v g } = \frac { \sum _ { s } P _ { i , s } \bigg ( 1 - \prod _ { u = 1 } ^ { U } \left( 1 - \rho _ { i , u } x _ { u , s } \right) \bigg ) } { \sum _ { s } P _ { i , s } } ,
$$

where $\rho _ { i , u }$ is the probability that UE i is within the covering radius of UAV u. $\rho _ { i , u }$ is calculated according to the UAVsâ historical trajectories.

Caching Problem Formulation: We aim to maximize the sum of the hit ratio of UEs. The caching problem can be formulated as:

$$
( \mathbf { P 1 } ) \quad \operatorname* { m a x } \sum _ { i \in \mathcal { T } } H _ { i , a v g }
$$

$$
\sum _ { s \in \mathcal { S } } c _ { s } x _ { u , s } \leq W _ { u } , \forall u ,\tag{1a}
$$

$$
x _ { u , s } \in \{ 0 , 1 \} , \forall u , \forall s .\tag{1b}
$$

Constraint (1a) represents the storage constraint of UAV u.

Challenges: (P1) is a special case of multi-dimension knapsack problems, which is known to be NP-hard [31]. Moreover, according to [32], itâs hard to find an efficient polynomial time approximation scheme (EPTAS)1.

## C. Task Offloading

Task Information: Let $d _ { i , s } ^ { t }$ be the size of task requiring service s generated by UE i at slot t, and $\mu _ { s }$ be the workload (in terms of CPU cycles) of service s per unit data.

UAV Properties: We consider a 3-D Cartesian coordinate system, in which the horizontal coordinate of UAV u at time slot t is denoted as $G _ { u } ^ { t } = ( X _ { u } ^ { t } , Y _ { u } ^ { t } )$ (we assume that UAV u flies at a fixed altitude $Z _ { u } )$ ( ). The horizontal distance between UE i and UAV u at time slot t is calculated as: $D _ { i , u } ^ { t } =$ $\sqrt { ( X _ { i } ^ { t } - X _ { u } ^ { t } ) ^ { 2 } + ( Y _ { i } ^ { t } - Y _ { u } ^ { t } ) ^ { 2 } }$ , where $G _ { i } ^ { t } = ( X _ { i } ^ { t } , Y _ { i } ^ { t } )$ is the hor-( ) + ( ) = ( )izontal coordinate of UE i at time slot t. Following [33], the uplink data rate of UE i with UAV u at time slot t is calculated as:

$$
r _ { u , i } ^ { t } = B \log _ { 2 } \left( 1 + \frac { \delta p _ { u } } { \left( D _ { i , u } ^ { t } \right) ^ { 2 } + Z _ { u } ^ { 2 } } \right) ,
$$

where B is the bandwidth, Î´ is SNR, and $p _ { u }$ is the transmission power of UAV u. Tasks from UE i can be offloaded to UAV u only when UE i is within the UAVâs maximum horizontal covering radius $R _ { u } ^ { \mathrm { m a x } }$ . Meanwhile, suppose that the UAV flies at a constant speed, therefore the maximum flight distance of UAV u between two time slots is limited, denoted as $D _ { u } ^ { \mathrm { m a x } }$ Due to the communication and computation resource limits of UAVs, UAV u can only process at most $N _ { u } ^ { \mathrm { m a x } }$ tasks at one time slot.

Decision Variables: Suppose that each task can be offloaded to at most one UAV or the remote cloud. Following decisions need to be made jointly by the BS at each time slot: i) $a _ { t } \in \{ 0 , 1 \}$ , 0 1denotes whether the services cached in UAVs will be updated at time slot t; ii) $y _ { i , u , s } ^ { t } ( y _ { i , 0 , s } ^ { t } ) \in \{ 0 , 1 \}$ , represents whether the ( ) 0 1task from UE i requiring service s is offloaded to UAV u (the remote cloud) at time slot t; iii) $G _ { u } ^ { t } = ( X _ { u } ^ { t } , Y _ { u } ^ { t } )$ , the horizontal coordinate of UAV u at time slot t.

Service Delay: The delay experienced by UEs when offloading tasks consists of two parts: i) Communication Delay: The communication delay includes the delay to upload the task and the delay to return the computation result. Since the size of the computation result is generally much smaller than the taskâs input size, the delay to return the computation result is ignored here. Thus the communication delay can be calculated as: $\begin{array} { r } { L _ { i , c o m m } ^ { t } = \sum _ { s } ( \frac { d _ { i , s } ^ { t } y _ { i , 0 , s } ^ { t } } { r _ { 0 } } + \sum _ { u } \frac { d _ { i , s } ^ { t } y _ { i , u , s } ^ { t } } { r _ { u , i } ^ { t } } ) } \end{array}$ , where $r _ { 0 }$ is the u,iaverage uplink data rate of UE with the remote cloud. ii) Computation Delay: The remote cloud is assumed to have sufficient computing power, hence the computation delay of the remote cloud can be neglected. Let $f _ { u }$ denote the computing capacity (in terms of CPU cycles) of UAV u for each task. Therefore the computation delay of UE i at time slot t can be calculated as: $\begin{array} { r } { L _ { i , c o m p } ^ { t } = \sum _ { s } \sum _ { u } \frac { d _ { i , s } ^ { t } \mu _ { s } y _ { i , u , s } ^ { t } } { f _ { u } } } \end{array}$ . The overall delay of UE i at =time slot t is calculated as:

TABLE I NOTATIONS
<table><tr><td rowspan=1 colspan=1>Uu</td><td rowspan=1 colspan=1>number/setofUAVs</td></tr><tr><td rowspan=1 colspan=1>II</td><td rowspan=1 colspan=1>number/set of UEs</td></tr><tr><td rowspan=1 colspan=1> $\overrightharpoon { S / s }$ </td><td rowspan=1 colspan=1>number of types/set of services</td></tr><tr><td rowspan=1 colspan=1> $\overrightharpoon { T / \mathcal { T } }$ </td><td rowspan=1 colspan=1>number/set of time slots</td></tr><tr><td rowspan=1 colspan=1>xY</td><td rowspan=1 colspan=1>horizontal coordinate of UAV uat time slot t</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { u } ^ { m } } }$ ax</td><td rowspan=1 colspan=1>maximumcoverageradiusofUAVu</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D _ { i , u } ^ { t } } }$ </td><td rowspan=1 colspan=1>distance betweenUEiandUAVu</td></tr><tr><td rowspan=1 colspan=1> $r _ { u , i } ^ { t }$ </td><td rowspan=1 colspan=1>uplinkdate ratebetweenUEiandUAVuat time t</td></tr><tr><td rowspan=1 colspan=1> $\smash { \frac { \cdot u , \tau } { N _ { s } ^ { m a x } } }$ </td><td rowspan=1 colspan=1>number of tasksUAVu canprocessat one time slot</td></tr><tr><td rowspan=1 colspan=1> $\boldsymbol { W _ { u } }$ </td><td rowspan=1 colspan=1>storagecapacity ofUAVu</td></tr><tr><td rowspan=1 colspan=1> $\overline { { c _ { s } } }$ </td><td rowspan=1 colspan=1>storage space required byservice s</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \boldsymbol { P } _ { i , s } } }$ </td><td rowspan=1 colspan=1>probabilityofUEi generatinga task requiring service s</td></tr><tr><td rowspan=1 colspan=1> $\underline { d } _ { i , s } ^ { t }$ </td><td rowspan=1 colspan=1>size of task generated byUEiat time t for service s</td></tr><tr><td rowspan=1 colspan=1> $\overline { { x _ { u , s } } }$ </td><td rowspan=1 colspan=1>whether theservicesiscachedatUAVu</td></tr><tr><td rowspan=1 colspan=1> $y _ { i , u , s } ^ { t }$ </td><td rowspan=1 colspan=1>whether UE i&#x27;s task requiring service sis offloadedto UAVu at time slot t</td></tr></table>

$$
{ \cal L } _ { i } ^ { t } = { \cal L } _ { i , c o m m } ^ { t } + { \cal L } _ { i , c o m p } ^ { t } .
$$

Energy Consumption of UAVs: The battery capacity for UAV u is limited, denoted as $E _ { u } ^ { \mathrm { m a x } }$ . We consider four types of energy consumption for UAV u at time slot t. i) Communication Energy Consumption: The communication energy consumption is proportional to the communication delay, thus can be calculated as: $\begin{array} { r } { E _ { u , c o m m } ^ { t } = \sum _ { i } \sum _ { s } p _ { u } \frac { d _ { i , s } ^ { t } y _ { i , u , s } ^ { t } } { r _ { u , i } ^ { t } } } \end{array}$ . ii) Computation u,iEnergy Consumption: The unit energy consumption per time of UAV u when executing tasks is denoted as $\gamma _ { u }$ . Thus the computation energy consumption of UAV u at time slot t can be calculated as: $\begin{array} { r } { E _ { u , c o m p } ^ { t } = \gamma _ { u } \sum _ { i } \sum _ { s } \frac { d _ { i , s } ^ { t } \mu _ { s } y _ { i , u , s } ^ { t } } { f _ { u } } } \end{array}$ . iii) Flight Energy Consumption: Let $\omega _ { u }$ u denote the unit flying energy consumption of UAV u. The flight energy consumption can be calculated as: $E _ { u , f l y } ^ { t } = \omega _ { u } \big | \big | G _ { u } ^ { t } - G _ { u } ^ { t - 1 } \big | \big |$ . iv) Caching Energy =Consumption: The caching energy consumption is caused by storing services. Let Î· denote the unit energy consumption per data for storing. The caching services set of UAV u at time slot t is represented by $S _ { u } ^ { t }$ . The caching energy consumption can be calculated as $\begin{array} { r } { E _ { u , c a c h } ^ { t } = \sum _ { s \in S _ { u } ^ { t } / S _ { u } ^ { t - 1 } } \eta c _ { s } } \end{array}$ . The overall energy = u uconsumption of UAV u at time slot t is calculated as:

$$
E _ { u } ^ { t } = E _ { u , c o m m } ^ { t } + E _ { u , c o m p } ^ { t } + E _ { u , f l y } ^ { t } + a ^ { t } E _ { u , c a c h } ^ { t } .
$$

Important notations are listed in Table I for easy reference.

Offloading Problem Formulation: The task offloading problem is formulated as:

$$
( \mathbf { P 2 } ) \quad \operatorname* { m i n } \sum _ { t \in \mathcal { T } } \sum _ { i \in \mathcal { T } } L _ { i } ^ { t }
$$

$$
y _ { i , u , s } ^ { t } \left( D _ { i , u } ^ { t } \right) ^ { 2 } \leq \left( R _ { u } ^ { \operatorname* { m a x } } \right) ^ { 2 } , \forall i , \forall u , \forall s , \forall t\tag{2a}
$$

$$
y _ { i , u , s } ^ { t } \leq x _ { u , s } , \forall i , \forall u , \forall s , \forall t ,\tag{2b}
$$

$$
\sum _ { i \in \mathcal { T } } \sum _ { s \in \mathcal { S } } y _ { i , u , s } ^ { t } \le N _ { u } ^ { \mathrm { m a x } } , \forall u , \forall t ,\tag{2c}
$$

$$
\sum _ { u = 0 } ^ { U } y _ { i , u , s } ^ { t } = 1 , \forall i , \forall s , \forall t ,\tag{2d}
$$

$$
\sum _ { t \in \mathcal { T } } E _ { u } ^ { t } \leq E _ { u } ^ { \mathrm { m a x } } , \forall u ,\tag{2e}
$$

$$
\left\| \boldsymbol G _ { u } ^ { t + 1 } - \boldsymbol G _ { u } ^ { t } \right\| \le D _ { u } ^ { \operatorname* { m a x } } , \forall u , \forall t ,\tag{2f}
$$

$$
a _ { t } \in \{ 0 , 1 \} , y _ { i , 0 , s } ^ { t } \in \{ 0 , 1 \} , y _ { i , u , s } ^ { t } \in \{ 0 , 1 \} , \forall u , \forall s , \forall t .\tag{2g}
$$

Constraint (2a) and (2b) ensure that the task can be offload only if the UE is within the coverage radius of UAV and the UAV has cached the corresponding service. Constraint (2c) limits the maximum number of tasks offloading to UAV u at one time slot. Constraint (2d) ensures that tasks generated at time slot t must be offloaded at the current time slot. Constraint (2e) is UAV uâs energy constraint, where $E _ { u } ^ { \mathrm { m a x } }$ is the battery capacity of UAV u. Constraint (2f) captures the maximum fly distance of UAV between two time slots (  Â·  is the L2-norm).

Challenges: i) The offloading requests arrive online, and the BS has to make offloading decisions on the fly. ii) (P2) is a mixed-integer nonlinear programming (MINLP). Even in the offline setting, (P2) is NP-hard (With fixed UAV trajectories, the problem is a multi-dimension knapsack problem, which is NP-hard [31]). iii) Constraint (2e) in (P2) involves all time slots while other constraints refer to one time slot, which further poses challenges in the algorithm design. iv) The solution of (P1) will affect (P2). The coupling between (P1) and (P2) makes the difficulty of the problem further escalated.

## IV. ONLINE ALGORITHM DESIGN

## A. Algorithm Idea and Overall Algorithm

In this section, we design an online algorithm, OOA, that dynamically updates services caching and determines task offloading at each time slot to minimize the overall service delay. Fig. 2 shows the main idea.

1) At the beginning of each time slot, OOA decides whether to update services cached in UAVs based on the gap between the average hit ratio of previous offloaded tasks and the expected hit ratio calculated by the caching decision. If so, OOA solves P1 by a greedy algorithm GCA according to UEsâ preferences for services and UAVsâ historical trajectories. Then, by scaling the energy consumption into the objective function using an energy weighting factor, P2 is decomposed into one-slot problems $\mathbf { P _ { t } }$ . Next, OOA solves $\mathbf { P _ { t } }$ by an iterative algorithm IAU to obtain task offloading decisions for time slot t.

<!-- image-->  
Fig. 2. Main idea of OOA.

2) For caching problem P1, we first reformulate the origin problem by replacing the objective function with an equivalent submodular function H. Then, the algorithm GCA greedily makes caching decisions to maximize the sum of the hit ratio. The theoretical performance of the algorithm GCA is guaranteed, owning to the submodularity of H.

3) For one-slot task offloading problem $\mathbf { P _ { t } } .$ we propose an iterative algorithm IAU that alternately optimizes UAV trajectory and task offloading. First, IAU fixes task offloading decsions Y to obtain subproblem $\bf { P } _ { t _ { 1 } }$ , which is non-convex. To solve $\mathbf { P _ { t _ { 1 } } } , \mathbf { P _ { t _ { 1 } } }$ is converted to a simplified problem $\bf { P } _ { t _ { 1 } } ^ { \prime }$ by replacing the non-convex part in the objective function with an upper bound. $\mathbf { P _ { t _ { 1 } } ^ { \prime } }$ is a convex problem and can be solved by standard convex solver CVX [34]. Second, with the fixed UAV trajectory, IAU obtains subproblem $\mathbf { P _ { t _ { 2 } } } .$ , which is a 0-1 integer linear programming problem. We first relax the variables in $\bf { P _ { t _ { 2 } } }$ to fractional and get the fractional solution by interior point method. Then we use a dependent rounding algorithm DR to round the fractional solution into the integer solution.

Overall Algorithm Details: We summarize our algorithm OOA in Algorithm 1. Caching decisions and the expected hit ratio $\begin{array} { r } { H _ { e } = \overset { \sim } { \frac { } { } \sum _ { i } ^ { } } \frac { H _ { i , a v g } } { I } } \end{array}$ are initialized according to Algorithm 2 =before offloading tasks (line 2). At the beginning of each time slot $t > 1$ , if the average hit ratio $\hat { H } _ { a v g } ^ { t - 1 }$ is significantly smaller than $H _ { e } ,$ 1 the cached services in $\mathrm { U A V s } ,$ as well as the expected hit ratio, will be updated (lines $5 { - } 8 ) ^ { 2 }$ . Then UAV trajectory and task offloading decisions are made according to Algorithm 4 (line 12). At the end of the time slot, the energy weighting factor and the average hit ratio $\hat { H } ^ { t }$ are updated (lines 13â14).

Let $q _ { i , s , t }$ be the number of tasks requiring service s generated by UE i until slot t, and $P _ { i , s } ^ { * }$ be the task preference uploaded by UE i. Considering both the historical information of tasks and task preference uploaded by UEs, $P _ { i , s }$ after time slot t can be calculated as:

$$
P _ { i , s } = \frac { t } { T } \cdot \frac { q _ { i , s , t } } { T } + ( 1 - \frac { t } { T } ) P _ { i , s } ^ { * } .\tag{3}
$$

Let $\Upsilon ^ { t } = \{ ( i , s ) | d _ { i . s } ^ { t } > 0 , \forall i \in \mathcal { T } , \forall s \in \mathcal { S } \}$ be the task set at Î¥time slot $t , \Upsilon _ { 0 } ^ { t } = \{ ( i , s ) | d _ { i , s } ^ { t } > 0 \land y _ { i , 0 , s } ^ { t } = 1 , \forall i \in \mathbb { Z } , \forall s \in \mathcal { S } \}$

Algorithm 1: Overall Online Algorithm (OOA).   
Input: Hit ratio tolerance Îº, energy weighting factor Î±   
Output: Service caching $X ^ { t }$ , UAV trajectory $\mathbf { G } ^ { t }$ and task   
offloading $\mathbf { Y } ^ { t } , \forall t \in \mathcal { T }$   
1: Initialize ${ \lambda } _ { u } ^ { t } = 0 , { a } _ { t } = 0 , { t } _ { a } = 1 , \forall t , \forall u ;$   
= 0 = 02: Initialize caching decisions $X ^ { 0 }$ 1and the expected hit   
ratio $H _ { e }$ according to Algorithm 2;   
3: for $t = 1 : T$ do   
4: if $t \neq 1$ :and $H _ { e } - \hat { H } _ { a v g } ^ { t - 1 } > \kappa$ then   
5: = Set $a _ { t } = 1 , t _ { a } = t ;$   
6: Update $P _ { i , s }$ =according to (3)   
7: Update $X ^ { t }$ according to Algorithm 2;   
8: Update $H _ { e }$ based on $X ^ { t } ;$   
9: else   
10: Update $X ^ { t } = X ^ { t - 1 }$   
11: end if   
12: Obtain $\mathbf { G } ^ { t } , \mathbf { Y } ^ { t }$ according to Algorithm 4;   
13: Update $\lambda _ { u } ^ { t }$ according to (6);   
14: Update $\hat { H } _ { a v g } ^ { t }$ according to (4);   
15: end for

be the task set that is offloaded to the remote cloud at time slot t, and $t _ { a }$ be the time slot when the caching was last updated. Then, $\hat { H } _ { a v g } ^ { t }$ are calculated as:

$$
\hat { H } _ { a v g } ^ { t } = 1 - \frac { \sum _ { t ^ { \prime } = t _ { a } } ^ { t - 1 } | \Upsilon _ { 0 } ^ { t ^ { \prime } } | } { \sum _ { t ^ { \prime } = t _ { a } } ^ { t - 1 } | \Upsilon ^ { t ^ { \prime } } | } .\tag{4}
$$

## B. Caching Algorithm

Reformulation. Let $Q = U \times S$ denote the caching ground set, where $( u , s ) \in Q$ =indicates that UAV u caches service s. We ( )define a set function H on subsets  of Q:

$$
H ( \Psi ) = \sum _ { i \in \mathcal { T } } \sum _ { s \in \mathcal { S } } P _ { i , s } \left( 1 - \prod _ { u \in \Psi ( s ) } ( 1 - \rho _ { i , u } ) \right) / \left( \sum _ { i } P _ { i , s } \right)
$$

where $\Psi ( s ) = \{ u | ( u , s ) \in \Psi \}$ . Denote $\Psi [ u ] = \{ s | ( u , s ) \in \Psi \}$ Î¨( ) = ( ) Î¨ Î¨then problem P1 can be reformulated as:

$$
\begin{array} { r l } & { ( \mathbf { P 1 } ^ { \prime } ) \underset { \Psi \subseteq Q } { \operatorname* { m a x } } H ( \Psi ) } \\ & { ~ \displaystyle \sum _ { s \in \Psi [ u ] } c _ { s } \leq W _ { u } , \forall u \in \mathcal { U } . } \end{array}\tag{5a}
$$

Lemma 1: Function H is a monotone non-increasing submodular function.

Proof: We first proof that H is monotone nonincreasing. Define $H ( X | \Psi ) = H ( \Psi \cup X ) - H ( \Psi )$ For $\Psi \subseteq Q$ and $( u _ { 0 } , s _ { 0 } ) \in Q \backslash \Psi$ ) = (Î¨ we have $H ( ( u _ { 0 } , s _ { 0 } ) | \Psi ) =$ ( (( $\begin{array} { r } { \sum _ { i \in \mathcal { T } } P _ { i , s _ { 0 } } \Big ( \rho _ { i , u _ { 0 } } x _ { u _ { 0 } , s _ { 0 } } \prod _ { u \in \Psi ( s _ { 0 } ) } ( 1 - \rho _ { i , u } x _ { u , s } ) \Big ) \geq 0 } \end{array}$ Next we proof the submodularity of H. For $\Psi _ { 1 } \subseteq \Psi _ { 2 } , \Psi _ { 2 } \subseteq$ $Q ,$ , and $( u _ { 0 } , s _ { 0 } ) \in Q \backslash \Psi _ { 2 }$ we have $H ( ( u _ { 0 } , s _ { 0 } ) | \Psi _ { 1 } ) -$ $\begin{array} { r } { H ( ( u _ { 0 } , s _ { 0 } ) | \Psi _ { 2 } ) = \sum _ { i \in \mathcal { T } } P _ { i , s _ { 0 } } \bigg ( \rho _ { i , u _ { 0 } } x _ { u _ { 0 } , s _ { 0 } } ( 1 - } \end{array}$

```latex
Algorithm 2: Greedy Caching Algorithm Design (GCA).
Input: $c _ { s } , W _ { u } , \rho _ { i , u } , P _ { i , s } , \forall i \in \mathcal { T } , \forall u \in \mathcal { U } , \forall s \in \mathcal { S }$
Output: $x _ { u , s } , \forall u \in \mathcal { U } , \forall s \in \mathcal { S }$
1: Initialize $\Psi = \emptyset , V = \{ ( u , s ) | u \in \mathcal { U } , s \in \mathcal { S } \} , x _ { u , s } =$
$0 , W _ { u } ^ { \prime } = W _ { u } , \forall u \in \mathcal { U } , \forall s \in \mathcal { S } ;$
2: 0while $| V | > 0$ do
3: $\begin{array} { r } { \big ( \hat { u } , \dot { \hat { s } } \big ) \stackrel { \cdot } { = } \arg \operatorname* { m a x } _ { ( u , s ) \in V } \frac { H ( \Psi \cup ( u , s ) ) - H ( \Psi ) } { c _ { s } } } \end{array}$
4: $\Psi = \Psi \cup ( \hat { u } , \hat { s } ) ;$
5: $V = V \backslash ( \hat { u } , \hat { s } ) ;$
6: $x _ { \hat { u } , \hat { s } } = 1 , W _ { \hat { u } } ^ { \prime } = W _ { \hat { u } } ^ { \prime } - c _ { \hat { s } } ;$
7: for $( \hat { u } , s ) \in V$ =do
8: if $c _ { s } > W _ { \hat { u } } ^ { \prime }$ then
9: $V = V \bar { ( } \hat { u } , s ) ;$
10: =end if
11: end for
12: end while
```

$$
\prod _ { u \in \Psi _ { 2 } ( s _ { 0 } ) \setminus \Psi _ { 1 } ( s _ { 0 } ) } ( 1 - \rho _ { i , u } x _ { u , s } ) ) \times \prod _ { u \in \Psi _ { 1 } ( s _ { 0 } ) } ( 1 -
$$

$\rho _ { i , u } x _ { u , s } ) \Big ) \geq 0 .$ , which concludes the lemma.

Based on the submodularity of H, we present a greedy algorithm GCA to solve problem $\mathbf { P 1 } ^ { \prime }$ with theoretical performance guarantee. The key idea is to progressively select UAV-service pair that brings the highest marginal increase in the sum of the hit ratio while satisfying the storage constraints.

Caching Algorithm Details: The algorithm GCA is described in Algorithm 2. First, GCA initializes the greedy solution set , available UAV-service pair set V and remaining storage space $W _ { u } ^ { \prime }$ for each UAV (line 1). Then, in each loop, GCA successively selects u, s pair in V with the highest increment ( )for the objective function H per unit storage cost (line 3). The pair chosen in line 3 is added into  and removed from V (lines Î¨4â5). The remaining storage space of the UAV is updated in line 6. After adding a pair into , pairs that do not satisfy the storage Î¨constraint are removed from V (lines 7â11).

Now we analyze the theoretical performance of Algorithm 2. Previous works about service caching also apply greedy algorithm to solve submodular function maximization problems [5]. However, the proofs of their algorithms are valid only when the size of different services is the same. We consider different size of the cached services and give proof of the approximation ratio in this case. The approximation ratio of Algorithm 2 is given in Theorem 1.

Theorem 1: Let $\begin{array} { r } { k = \frac { \operatorname* { m i n } _ { u } W _ { u } } { \operatorname* { m a x } _ { s } c _ { s } } , \epsilon = \frac { k } { k - 1 } } \end{array}$ , Algorithm 2 is  â $e ^ { - \epsilon } )$ s s-approximate algorithm to problem P1.

)Proof: Let $X _ { i }$ denote the i-th element picked by Line 3in Algorithm 2. Let $\Psi _ { i } = ( X _ { 1 } , X _ { 2 } , . . . X _ { i } )$ denote the greedy so-Î¨ = ( )lution set after i-th picking. The greedy solution is defined as $\Psi _ { l } = ( X _ { 1 } , X _ { 2 } , . . . X _ { l } )$ (the greedy algorithm picked l elements Î¨ = ( )before it stops). c is the storage cost function. Let $O P T$ denote ()the optimal solution of problem P1. Let $\begin{array} { r } { B = \sum _ { u } W _ { u } . } \end{array}$ base on the definition of greedy rule and k, we have $\scriptstyle \sum _ { i = 1 } ^ { l } c ( X _ { i } ) > =$ $( 1 - \textstyle { \frac { 1 } { k } } ) B , L \leq B$ . Using Lemma 3 in [35], we have

$$
\begin{array} { r l } { H ( G _ { i } ) \geq \Bigg ( 1 - \displaystyle \prod _ { k = 1 } ^ { I } \left( 1 - \frac { c ( X _ { k } ) } { L } \right) \Bigg ) H ( O P T ) } \\ { \geq \Bigg ( 1 - \displaystyle \prod _ { k = 1 } ^ { I } \left( 1 - \frac { c ( X _ { k } ) } { B } \right) \Bigg ) H ( O P T ) } \\ { \geq \Bigg ( 1 - \displaystyle \prod _ { k = 1 } ^ { I } \left( 1 - \frac { \sum _ { i = 1 } ^ { I } c ( X _ { i } ) } { B } \right) \Bigg ) H ( O P T ) } \\ { \geq \Bigg ( 1 - \displaystyle \prod _ { k = 1 } ^ { I } \left( 1 - \frac { ( 1 - \frac { c } { k } ) B } { B I } \right) \Bigg ) H ( O P T ) } \\ { \geq \Bigg ( 1 - \displaystyle \prod _ { k = 1 } ^ { I } \left( 1 - \frac { ( 1 - \frac { c } { k } ) B } { B I } \right) \Bigg ) H ( O P T ) } \\ { = \Bigg ( 1 - \displaystyle \left( 1 - \frac { c } { k } \right) ^ { I } \Bigg ) H ( O P T ) \geq ( 1 - e ^ { - \ast } ) H ( O P T ) } \end{array}
$$

The first inequality is the Lemma 3 in [35]. The second inequality is trivial since $L \leq B$ . The third inequality holds because the inequality of arithmetic and geometric means. The fourth inequality is due to $\textstyle \sum _ { i = 1 } ^ { l } c ( X _ { i } ) { \overset { \vartriangle } { \geq } } ( 1 - { \frac { 1 } { k } } ) B$ . The last inequality is true since $\begin{array} { r } { g ( x ) = 1 - ( 1 - \frac { \epsilon } { r } ) ^ { x } , \epsilon > \overset { \sim } 0 } \end{array}$ )is monotone decreasing in $( 0 , + \infty )$ ( ) =and $1 _ { x  + \infty } g ( \bar { x } ) = 1 - e ^ { - \epsilon }$ -

## C. Offloading Algorithm

One-slot Offloading Problem: To eliminate the coupling of energy consumption in constraint (2e), for each UAV u, we design an energy weighting factor $\lambda _ { u } ^ { t }$ to decompose problem P2 into one-slot problems. How the energy budget of UAVs is spent will significantly affect the total service delay in the entire period. Running out of the energy budget of UAVs too soon will limit the future decision space for task offloading. The BS has to select UAVs with higher delay in the later stage, which further increases the service delay in the whole time span. Based on the analysis above, the energy weighting factor should increase as the remaining energy of the UAV decreases. Besides, the factor should have lower and upper bounds, which represent two extreme cases, i.e., no energy usage and energy exhaustion. According to these characteristics, we design $\lambda _ { u } ^ { t }$ which satisfies forementioned requirements as follows:

$$
\lambda _ { u } ^ { t } = \frac { \bar { L } ^ { t } \sum _ { t ^ { \prime } = 1 } ^ { t - 1 } E _ { u } ^ { t ^ { \prime } } } { ( E _ { u } ^ { \operatorname* { m a x } } ) ^ { 2 } } , \forall t \in \mathcal { T } ,\tag{6}
$$

where $\begin{array} { r } { \bar { L } ^ { t } = \frac { \sum _ { t ^ { \prime } = 1 } ^ { t - 1 } \sum _ { i \in \mathcal { T } } { L _ { i } ^ { t ^ { \prime } } } } { \sum _ { t ^ { \prime } = 1 } ^ { t - 1 } | \Upsilon ^ { t ^ { \prime } } | } } \end{array}$ is the average service delay of tasks tbefore time slot t. The initial value of $\lambda _ { u } ^ { t }$ is zero. $\lambda _ { u } ^ { t }$ increases when the remaining energy of the UAV goes down, and reaches the maximum value when the UAV has no energy. Then the one-slot task offloading problem is formulated as:

$$
( \mathbf { P _ { t } } ) \quad \operatorname* { m i n } \sum _ { i \in \mathcal { I } } L _ { i } ^ { t } + \sum _ { u \in \mathcal { U } } \lambda _ { u } ^ { t } E _ { u } ^ { t }
$$

$$
y _ { i , u , s } ^ { t } \left( D _ { i , u } ^ { t } \right) ^ { 2 } \leq ( R _ { u } ^ { m a x } ) ^ { 2 } , \forall i , \forall u , \forall s\tag{7a}
$$

$$
y _ { i , u , s } ^ { t } \leq x _ { u , s } , \forall i , \forall u , \forall s\tag{7b}
$$

$$
\sum _ { i \in \mathcal { T } } \sum _ { s \in \mathcal { S } } y _ { i , u , s } ^ { t } \le N _ { u } ^ { \operatorname* { m a x } } , \forall u ,\tag{7c}
$$

$$
\sum _ { u = 0 } ^ { U } y _ { i , u , s } ^ { t } = 1 , \forall i , \forall s ,\tag{7d}
$$

$$
E _ { u } ^ { t } \leq E _ { u , r } ^ { t } , \forall u ,\tag{7e}
$$

$$
\left\| \boldsymbol { G } _ { u } ^ { t + 1 } - \boldsymbol { G } _ { u } ^ { t } \right\| \leq D _ { u } ^ { \operatorname* { m a x } } , \forall u ,\tag{7f}
$$

$$
y _ { i , 0 , s } ^ { t } \in \{ 0 , 1 \} , y _ { i , u , s } ^ { t } \in \{ 0 , 1 \} , \forall u , \forall s .\tag{7g}
$$

where $\begin{array} { r } { E _ { u , r } ^ { t } = E _ { u } ^ { \operatorname* { m a x } } - \sum _ { t ^ { \prime } = 1 } ^ { t - 1 } E _ { u } ^ { t ^ { \prime } } } \end{array}$ is the remaining energy of =UAV u at the beginning of time slot t.

We further decompose problem $\mathbf { P _ { t } }$ into two subproblems, i.e., UAV trajectory and task offloading.

1) UAV Trajectory: With the fixed task offloading decisions, the UAV trajectory subproblem is formulated as:

$$
\begin{array} { r l } & { \displaystyle ( { \bf P } _ { { \bf t } _ { 1 } } ) \quad \operatorname* { m i n } \sum _ { i \in { \cal Z } } L _ { i , c o m m } ^ { t } + \sum _ { u \in { \cal U } } \lambda _ { u } ^ { t } ( E _ { u , c o m m } ^ { t } + E _ { u , f l y } ^ { t } ) } \\ & { \quad \mathrm { s . t . } \quad ( 7 a ) , ( 7 e ) , ( 7 f ) . } \end{array}
$$

Problem $\bf { P } _ { t _ { 1 } }$ is non-convex in $G _ { u } ^ { t }$ due to the logarithmic part. We try to find an approximation for the non-convex part in problem $\bf { P _ { t _ { 1 } } }$ so that the complexity is decreased. Itâs easy to verify that function $\begin{array} { r } { f ( x ) = \overline { { \frac { 1 } { \ln ( 1 + \frac { 1 } { x } ) } } } , \forall x > 0 } \end{array}$ is a concave function, thus we have:

$$
\frac { 1 } { r _ { u , i } ^ { t } } \leq \frac { \ln 2 } { B } \left( f ^ { \prime } ( \zeta ) \frac { \left\| G _ { u } ^ { t } - G _ { i } ^ { t } \right\| ^ { 2 } + Z _ { u } ^ { 2 } } { \delta p _ { u } } - \zeta ) + f ( \zeta ) \right) .
$$

where $\begin{array} { r } { \zeta = \frac { Z _ { u } ^ { 2 } } { \delta p _ { u } } } \end{array}$ . Then the simplified UAV trajectory subproblem =is given as:

$$
\begin{array} { r l } & { ( \mathbf { P _ { t 1 } ^ { \prime } } ) \underset { u = 1 } { \operatorname* { m i n } } \underset { \textbf { \^ { i } } \textbf { ^ { j } } \textbf { ^ { k } } \textbf { ^ { j } } \textbf { ^ { f } } } { \operatorname* { m i n } } } \\ & { \times \mathrm { l n } 2 \left( \frac { \left( 1 + \lambda _ { u } ^ { \varepsilon } p _ { u } \right) d _ { u , v } ^ { \varepsilon } g _ { u , u , v } ^ { \varepsilon } \left. G _ { u } ^ { \varepsilon } - G _ { v } ^ { \varepsilon } \right. ^ { 2 } } { B \delta p _ { u } } \right) } \\ & { + \sum _ { u } \lambda _ { u } ^ { \varepsilon } \omega _ { u } \left. G _ { u } ^ { \varepsilon } - G _ { u } ^ { \varepsilon - 1 } \right. } \\ & { \times . } \\ & { \sum _ { i } \sum _ { v } p _ { u } d _ { u , v } ^ { \varepsilon } g _ { u , v } ^ { \varepsilon } \frac { \mathrm { l n } 2 } { B } \left( f ^ { \prime } ( f ) , } \\ & { \times \int _ { i } ^ { 1 } \omega _ { u } \left( \varepsilon _ { u } ^ { \prime } , g _ { u , v } ^ { \varepsilon } \right) \frac { \mathrm { l n } 2 } { B } \left( f ^ { \prime } ( f ) \frac { \left. G _ { u } ^ { \varepsilon } - G _ { u } ^ { \varepsilon } \right. ^ { 2 } + Z _ { u } ^ { 2 } } { \delta p _ { u } } - f \right) + f ( \zeta ) \right) } \\ & { + \omega _ { u } \left. G _ { v } ^ { \varepsilon } - G _ { v } ^ { \varepsilon - 1 } \right. \leq E _ { u , v } ^ { \varepsilon } - { \left( E _ { u , v } ^ { \varepsilon } - { \left( E _ { u } ^ { \varepsilon } - g _ { v , v } ^ { \varepsilon } \right) } + a ^ { \varepsilon } E _ { v , v } ^ { \varepsilon } \right) } , \forall u . } \end{array}
$$

Problem $\mathbf { P _ { t 1 } ^ { \prime } }$ is convex on $G _ { u } ^ { t }$ and can be solved by CVX. In this way, the UAV trajectory subproblem is solved.

2) Suboptimal Task Offloading: With fixed UAV trajectory, we merge constraint (7a) and constraint (7b) into one constraint, then the task offloading problem is rewritten as:

$$
\left( \mathbf { P _ { t _ { 2 } } } \right) \operatorname* { m i n } \sum _ { i \in \mathcal { I } } \sum _ { s \in \mathcal { S } } \sum _ { u \in \mathcal { U } } \left( \frac { 1 + \lambda _ { u } ^ { t } p _ { u } } { r _ { u , i } ^ { t } } + \frac { \left( 1 + \lambda _ { u } ^ { t } \gamma _ { u } \right) \mu _ { s } } { f _ { u } } \right.
$$

$$
- \frac { 1 } { r _ { 0 } } \bigg ) d _ { i , s } ^ { t } y _ { i , u , s } ^ { t }
$$

```latex
Algorithm 3: Dependent Rounding Algorithm (DR), ât.
Input: Fractional solution $\overline { { \mathbf { Y } ^ { * } } }$
Output: Integer solution Y
1: Construct bipartite graph $( A , B , E )$ based on $\mathbf { Y } ^ { * }$
2: while $E \neq \emptyset$ do
3: = Remove edges in E such that $e _ { i s , u } \in \{ 0 , 1 \}$
4: 0 1while there exists a cycle or longest path  do
5: Divide into two matchings $M _ { 1 }$ and $M _ { 2 } ;$
6: $\eta _ { 1 } \overset { d e f } { = } \operatorname* { m i n } \{ \eta : ( \exists ( a _ { i s } , b _ { u } ) \in M _ { 1 } : e _ { i s , u } + \eta =$
$1 ) \bigvee ( \exists ( a _ { i s } , b _ { u } ) \in M _ { 2 } : e _ { i s , u } - \eta = 0 ) \big \} .$
7: $\eta _ { 2 } \overset { d e f } { = }$ min $\{ \eta : ( \exists ( a _ { i s } , b _ { u } ) \in M _ { 1 } : e _ { i s , u } - \eta =$
$0 ) \vee ( \exists ( a _ { i s } , b _ { u } ) \in M _ { 2 } : e _ { i s , u } + \eta = 1 ) \}$
8: 0) ( ( ) With the probability $\frac { \eta _ { 2 } } { \eta _ { 1 } + \eta _ { 2 } }$
Set $e _ { i s , u } = e _ { i s , u } + \eta _ { 1 } , \forall ( a _ { i s } , \hat { b _ { u } } ) \ \in M _ { 1 }$ and $e _ { i s , u } =$
$e _ { i s , u } - \eta _ { 1 } , \forall ( a _ { i s } , b _ { u } ) \in M _ { 2 } ;$
9: ( ) With the probability $\begin{array} { r } { \frac { \eta _ { 1 } } { \eta _ { 1 } + \eta _ { 2 } } , } \end{array}$
Set $e _ { i s , u } = e _ { i s , u } - \eta _ { 2 } , \forall ( a _ { i s } , \dot { b } _ { u } ) \in M _ { 1 }$ and $e _ { i s , u } =$
$e _ { i s , u } + \eta _ { 2 } , \forall ( a _ { i s } , b _ { u } ) \in M _ { 2 } ;$
10: + (end while
11: end while
12: Set $\bar { y } _ { i , u , s } ^ { t } = e _ { i s , u } , \forall i , \forall u , \forall s ;$
13: Set $\begin{array} { r } { \bar { y } _ { i , 0 , s } ^ { t ^ { \prime } } = 1 - \sum _ { u \in \mathcal { U } } \bar { y } _ { i , u , s } ^ { t } , \forall i , \forall s ; } \end{array}$
14: Return Y
```

$$
y _ { i , u , s } ^ { t } \leq \mathcal { k } _ { \geq 1 } \left( \operatorname* { m i n } ( \frac { ( R _ { u } ^ { \operatorname* { m a x } } ) ^ { 2 } } { ( D _ { i , u } ^ { t } ) ^ { 2 } } , x _ { u , s } ) \right) , \forall i , \forall u , \forall s\tag{11a}
$$

$$
\sum _ { i \in \mathcal { T } } \sum _ { s \in \mathcal { S } } y _ { i , u , s } ^ { t } \le N _ { u } ^ { \operatorname* { m a x } } , \forall u ,\tag{11b}
$$

$$
\sum _ { u \in \mathcal { U } } y _ { i , u , s } ^ { t } \le 1 , \forall i , \forall s ,\tag{11c}
$$

$$
\sum _ { i } \sum _ { s } ( \frac { p _ { u } } { r _ { u , i } ^ { t } } + \frac { \gamma _ { u } \mu _ { s } } { f _ { u } } ) d _ { i , s } ^ { t } y _ { i , u , s } ^ { t } \leq E _ { u , r } ^ { t } - E _ { u , f l y } ^ { t } - a _ { t } E _ { u , c a c h } ^ { t } , \forall u ,\tag{11d}
$$

$$
y _ { i , u , s } ^ { t } \in \{ 0 , 1 \} , \forall i , \forall u , \forall s ,\tag{11e}
$$

where $\forall ( x ) = 1 { \mathrm { i f } } x \geq 1$ , otherwise $\begin{array} { r } { \mathcal { H } ( x ) = 0 } \end{array}$ . By relaxing all ( ) = 1 1 ( ) = 0integral decision variables to fractional, problem $\bf { P _ { t _ { 2 } } }$ then becomes a continuous linear program $\mathbf { P _ { t _ { 2 } } ^ { \prime } }$

We first use interior point method [36] to obtain a fractional solution of problem $\mathbf { P _ { t 2 } ^ { \prime } } .$ Then we introduce a dependent rounding algorithm (DR) in Algorithm 3 that converts the fractional solution into the integer solution with theoretical performance guarantee. For preparation of the rounding procedure, DR first constructs a bipartite graph A, B, E based on fractional solution $Y ^ { * }$ ( ). The steps to construct bipartite graph are as follows: i) Let $A = \{ a _ { i s } | \forall i \in \mathcal { T } , \forall s \in \mathcal { S } \}$ . The node $a _ { i s }$ in A denotes the =task requiring service s from UE i. ii) Let $B = \{ b _ { u } | \forall u \in \mathcal { U } \}$ . The node $b _ { u }$ =in B denotes the UAV u. iii) For $a _ { i s } \in A$ and $b _ { u } \in B$ , put the edge $( a _ { i s } , b _ { u } )$ into E with weight $e _ { i s , u } = y _ { i , s , u } ^ { t * } .$ ( ) =Rounding Algorithm Details: In Algorithm 3, DR first eliminates edges with integral weights in line 3. Lines 4â10 provide the rounding process. In each iteration, DR finds a cycle or longest path and splits it into two matchings (line 5). Then, with carefully designed probability, weights of edges in one matching will increase while weights of edges in the other matching are decreased (lines 6â9). Finally, the integer solution is updated in lines 12â13.

Now we study the theoretical performance of Algorithm 3 and whether the integer solution returned by Algorithm 3 satisfies constraints of problem $\bf { P _ { t _ { 2 } } }$

Lemma 2: Let $P _ { t _ { 2 } }$ be the objective function of problem $\bf { P _ { t _ { 2 } } } .$ Given the fractional solution $Y ^ { * }$ of $\bf { P _ { t _ { 2 } } }$ and the corresponding integer solution Y returned by Algorithm 3, we have:

$$
\mathbb { E } ( P _ { t _ { 2 } } ( \bar { Y } ) ) = \mathbb { E } ( P _ { t _ { 2 } } ( Y ^ { * } ) ) .
$$

Proof: We first proof that $\mathbb { E } ( \bar { y } _ { i , u , s } ^ { t } ) = y _ { i , u , s } ^ { t * } .$ Suppose Algorithm 3 stops after J iterations. Let $e _ { i s , u } ^ { j }$ denote the weight of edge $( a _ { i s } , b _ { u } )$ after j iterations. As a result, we have $e _ { i s , u } ^ { 0 } =$ $y _ { i , u , s } ^ { t * }$ and $e _ { i s , u } ^ { J } = \bar { y } _ { i , u , s } ^ { t }$ . Now Consider iteration $j + 1$

= Â¯ + 1Case 1: The edge is not part of the cycle or the longest path, then its weight remains intact.

Case 2: The weight of the edge has been modified after iteration $j + 1$ , according to lines 8â9 in Algorithm 3 we have

$$
\mathbb { E } ( e _ { i s , u } ^ { j + 1 } ) = \frac { \eta _ { 2 } } { \eta _ { 1 } + \eta _ { 2 } } ( \mathbb { E } ( e _ { i s , u } ^ { j } ) + \eta _ { 1 } ) + \frac { \eta _ { 1 } } { \eta _ { 1 } + \eta _ { 2 } } ( \mathbb { E } ( e _ { i s , u } ^ { j } ) - \eta _ { 2 } )
$$

$$
= \frac { \eta _ { 1 } } { \eta _ { 1 } + \eta _ { 2 } } \mathbb { E } ( e _ { i s , u } ^ { j } ) + \frac { \eta _ { 2 } } { \eta _ { 1 } + \eta _ { 2 } } \mathbb { E } ( e _ { i s , u } ^ { j } ) = E ( e _ { i s , u } ^ { j } ) .
$$

In both cases $\mathbb { E } ( e _ { i s , u } ^ { j + 1 } ) = \mathbb { E } ( e _ { i s , u } ^ { j } )$ holds. Thus we have $\mathbb { E } ( \bar { y } _ { i , u , s } ^ { t } ) = \mathbb { E } ( e _ { i s , u } ^ { J } ) = \cdot \cdot \cdot = \mathbb { E } ( e _ { i s , u } ^ { 0 } ) = y _ { i , u , s } ^ { t * } .$ (Â¯ )Notice that problem $\bf { P _ { t _ { 2 } } }$ ) = = ( ) =can be reformulated as Y $\begin{array} { r } { \cdot \sum _ { i \in \mathcal { T } } \sum _ { s \in \mathcal { S } } \sum _ { u \in \mathcal { U } } m _ { i , u , s } ^ { t } y _ { i , u , s } ^ { t } , } \end{array}$ where $m _ { i , u , s } ^ { t } =$ $\begin{array} { r } { ( \frac { 1 + \lambda _ { u } ^ { t } p _ { u } } { r _ { u , i } ^ { t } } + \frac { ( 1 + \lambda _ { u } ^ { t } \gamma _ { u } ) \mu _ { s } } { f _ { u } } - \frac { 1 } { r _ { 0 } } ) d _ { i , s } ^ { t } , \forall i , u , s , t . } \end{array}$ . Using $\mathbb { E } ( \bar { y } _ { i , u , s } ^ { t } ) =$ $y _ { i , u , s } ^ { t * }$ , we obtain $\mathbb { E } ( P _ { t _ { 2 } } ( \hat { Y } ) ) = \mathbb { E } ( P _ { t _ { 2 } } ( Y ^ { * } ) )$

( ( )) = ( ( ))Lemma 3: Under the solution Y returned by Algorithm 3, constraint (11a), (11b) and (11c) must be satisfied, while constraint (11d) are in expectation satisfied.

Proof: Itâs easy to verify that constraint (11a) must be satisfied since $\vert \mathcal { k } ( x ) \in \{ 0 , 1 \}$ . As for the constraint (11b) and ( ) 0 1(11c). Consider a vertex v in the bipartite graph constructed in Algorithm 3. At any iteration, itâs trivial that (11b) and (11c) hold If v has at most one edge incident on it. Now consider v has at least two edges incident on it. For cycle or longest path  and two matchings $M _ { 1 } , M _ { 2 }$ Î, v must have exactly two edges in , and one of them is in $M _ { 1 }$ while the other is in $M _ { 2 }$ Î. Thus the modification of weights in Algorithm 3 wonât affect $\textstyle \sum _ { u } e _ { i s , u }$ and $\textstyle \sum _ { i , s } e _ { i s , u } ,$ $\mathrm { i . e . , } \sum _ { u } \bar { y } _ { i , u , s } ^ { t }$ and $\textstyle \sum _ { { i , s } } \bar { y } _ { i , u , s } ^ { t } ,$ hence (11b) and (11c) hold. Fi-Â¯ Â¯nally, we proof that constraint (11e) is satisfied. Constraint (11e) can be rewritten as $\begin{array} { r } { \sum _ { i \in \mathcal { T } } \sum _ { s \in \mathcal { S } } n _ { i , u , s } ^ { t } y _ { i , u , s } ^ { t } \le E _ { u , r } ^ { t } - E _ { u , f l y } ^ { t } - } \end{array}$ $a _ { t } E _ { u , c a c h } ^ { t } .$ , where $\begin{array} { r } { n _ { i , u , s } ^ { t } = \frac { p _ { u } d _ { i , s } ^ { t } } { r _ { u , i } ^ { t } } + \frac { \gamma _ { u } d _ { i , s } ^ { t } } { f _ { u } } } \end{array}$ . The following proof is similar to the proof of Theorem 2 since $\mathbb { E } ( \bar { y } _ { i , u , s } ^ { t } ) = y _ { i , u , s } ^ { t * } . \square$ (Â¯ ) =Lemma 4: Algorithm 3 converges in polynomial time.

Proof: Since at least one edge is removed from E per iteration, the while loop in lines 2â11 of Algorithm 3 terminates in $O ( | E | ) = O ( I U S )$ iterations. For each iteration, a cycle or ( ) = ( )longest path can be found in $O ( | A \cup B | ) = O ( I S + U )$ steps ( ) = ( + )via Depth First Search(DFS). Lines 8â9, 12-13 in Algorithm 3 also take O IUS steps. Therefore the running time of Algorithm 3 is $O ( ( I S + U ) I U S )$

Algorithm 4: Iterative Algorithm For UAV Trajectory and   
Task Offloading (IAU).   
Input: Tolerance $\phi ,$ maximum iterations $I ^ { \mathrm { m a x } } = 1 0 0 $   
Output: Solution {G, Y}   
1: Initialize a feasible solution $\{ \mathbf { G } ^ { 0 } , \mathbf { Y } ^ { 0 } \}$ , and iteration   
index i ;   
2: while $i \le I ^ { \mathrm { m a x } }$ do   
3: With fixed $\mathbf { Y } ^ { i - 1 }$ , obtain $\mathbf { G } ^ { i }$ by solving $\mathbf { P _ { t 1 } ^ { \prime } }$ ï¼   
4: Fix $\mathbf { G } ^ { i } ,$ , obtain fractional solution $\mathbf { Y } ^ { i * }$ by solving   
$\mathbf { P _ { t 2 } ^ { \prime } } ;$   
5: obtain integer solution $\mathbf { Y } ^ { i }$ according to Algorithm 3;   
6: if $| P _ { t } ( \mathbf { G } ^ { i } , \mathbf { Y } ^ { i } ) - P _ { t } ( \mathbf { G } ^ { i - 1 } , \mathbf { Y } ^ { i - 1 } ) | \leq \phi$ then   
7: (Break;   
8: else   
9: Set $i  i + 1 .$   
10: end if   
11: end while   
12: Return $\{ \mathbf { G } ^ { i } , \mathbf { Y } ^ { i } \}$

(( + ) )3) Iterative Algorithm Design: To obtain a suboptimal solution to problem $\mathbf { P _ { t } }$ , we develop an alternating optimizationbased algorithm (IAU) in Algorithm 4 that iteratively solves two subproblems. In Algorithm 4, IAU iteratively optimizes UAV trajectory (line 3) and task offloading (lines 4â5). The complexity and convergence analysis of Algorithm 4 is given as follows:

Lemma 5: Algorithm 4 converges with polynomial complexity.

Proof: For the convergence, we first prove that the objective function $\mathbf { P _ { t } } ( \mathbf { G } , \mathbf { Y } )$ keeps non-increasing when updating $\{ \mathbf G , \mathbf Y \}$ ( ). According to lines 3â5 in Algorithm 4, we have $\begin{array} { r } { \mathbf { \tilde { P } _ { t } } ( \mathbf { G } ^ { i - 1 } , \mathbf { Y } ^ { i - 1 } ) \ge \mathbf { \tilde { P } _ { t } } ( \mathbf { G } ^ { i } , \mathbf { Y } ^ { i - 1 } ) \ge \mathbf { P _ { t } } ( \mathbf { \bar { G } } ^ { i } , \mathbf { Y } ^ { i } ) } \end{array}$ , where the ( ) ( ) ( )first inequality is due to the sub-optimality of UAV trajectory $\mathbf { G } ^ { i }$ . The second inequality holds because of the suboptimality of $\mathbf { Y } ^ { i }$ by dependent rounding. In addition, the objective function $\mathbf { P _ { t } } ( \mathbf { G } , \mathbf { Y } )$ is always non-negative. Therefore, ( )the objective function keeps non-increasing after every iteration, which is also finitely lower-bounded by zero. For the complexity, in line 4 of Algorithm 4, problem $\bf { P _ { t _ { 2 } } ^ { \prime } }$ is solved by interior point method, whose computation complexity is $O ( ( I U S ) ^ { 3 } )$ . Following Lemma 4, the running time of Algo-(( ) )rithm 3 is $O ( ( I S + U ) I U S )$ . To summarize, the complex-(( +ity of Algorithm 4 is $O ( I ^ { \operatorname* { m a x } } ( ( I U S ) ^ { 3 } ) + ( I S + U ) I U S ) =$ $O ( I ^ { \operatorname* { m a x } } ( I U S ) ^ { 3 } ) )$ ( (( ) ) + ( + ) ) =where Imax is the maximum iteration times ( ( ) ))of Algorithm 4, which is polynomial, and this concludes the lemma. -

The overall performance of OOA is given by the following theorem.

Theorem 2: OOA converges in polynomial time.

Proof: First, itâs easy to verify that the complexity of Algorithm 2 is $O ( ( U S ) ^ { 2 } )$ , since the while loop in lines 2â12 of Algorithm 2 terminates in $O ( | V | ) = O ( U S )$ iterations. Therefore, the complexity of Algorithm 1 is $\dot { O } ( ( \dot { U } S ) ^ { 2 } + T * ( ( U S ) ^ { 2 } +$

$I ^ { \operatorname* { m a x } } ( I U S ) ^ { 3 } ) ) ) = O ( T I ^ { \operatorname* { m a x } } ( I U S ) ^ { 3 } )$ . Since the convergence ( ) ))) = ( ( ) )of Algorithm 4 is proofed in Lemma 5, we obtain that OOA converges in polynomial time. -

## V. PERFORMANCE EVALUATION

## A. Evaluation Setup

Parameter Settings: We simulate a UAV-assisted MEC network running for $T = 1 0 0$ time slots (a time slot is 20 seconds), with $U \in [ 2 , 1 0 ]$ 100UAVs and $I \in [ 1 2 , 4 8 ]$ UEs. UAVs are [2 10]randomly scattered in a square area of $\mathrm { 2 0 0 \times 2 0 0 ~ m ^ { 2 } }$ . For the coordinates of UEs, we use the EUA dataset [37], which contains locations of 125 base stations and 816 mobile users in Melbourne central business district area. We choose a base station whose coverage radius is 200 m, and then randomly choose I users in the coverage of the base station as the UEs in our simulation. The network provides $S = 2 0$ types of services for UEs. The storage = 2capacity of each UAV is $W _ { u } = 3$ , while the storage capacity required by service s $c _ { s }$ = 3is within . , . Following [15], [28], we [0 5 1]use Zipf distribution with exponent value 0.6 as the population of services, and the preferences of UEs $P _ { i , s }$ is derived from the population of services with a deviation range from $[ - 0 . 1 , 0 . 1 ]$ The size of each task is $d _ { i , s } ^ { t } \in [ 1 0 0 , 1 0 0 0 ]$ [ 0 1 0 1]KB. The workload of task requiring service s is $\mu _ { s } = [ 1 0 ^ { 6 } , 1 0 ^ { 7 } ]$ cycles (per bytes). = [10 10 ]Following the similar setting in [23], [24], [33], the parameters of UAVs are set as follows: the computation capacity of UAV for each task $f _ { u } = 1 \mathrm { G H z }$ , the maximum number of tasks UAV can process at one time slot $N _ { u } ^ { \mathrm { m a x } } \in [ 5 , 1 0 ]$ , the maximum flying distance at one slot $D _ { u } ^ { \mathrm { m a x } } = 5 0 \mathrm { m }$ [5 10], the maximum covering radius of UAV $R _ { u } ^ { \mathrm { { m a x } } } = 2 0 0$ m, the fixed altitude $Z _ { u } = 1 0 0$ m, the = 200 = 100spectrum bandwidth of each communication channel is $B = 1$ MHz. As for energy budget and consumption, according to the properties of DJI Mavic 2 Pro [38], the energy budget of UAV is $E _ { u } ^ { \mathrm { m a x } } = 4 ~ \mathrm { W h } . ^ { 3 }$ The transmission power of each UAV is set to $p _ { u } = 0 . 1 \mathrm { w } .$ . The unit flying energy consumption is $\omega _ { u } = 6 \mathrm { J } / \mathrm { m }$ = 0 1Baselines: We compare OOA with three algorithms.

RANDOM: Service caching and UAV trajectories are made randomly, and UEs will offload as many tasks as possible to UAVs as long as all the constrains are satisfied.

DELAY: DELAY makes all the decisions to minimize the delay just like OOA, without considering saving energy for the future $( \mathrm { i . e . , } \lambda _ { u } ^ { t } = 0 , \forall u , \forall t )$

= 0TJSO [24]: In TJSO, caching decisions, UAV trajectories and task offloading are jointly optimized periodically. TJSO does not consider strictly satisfying the energy constraint.

## B. Evaluation Results

Hit Ratio: Fig. 3 shows the expected hit ratio achieved by different caching algorithms under different numbers of types of services. The expected hit ratio decreases with the increase in the number of types of services because tasks generated by UEs are more diverse while the storage space of UAV remains the same.

<!-- image-->  
Fig. 3. Expected hit ratio under different numbers of types of services.

<!-- image-->  
Fig. 4. Average hit ratio of each time slot.

<!-- image-->  
Fig. 5. Expected hit ratio with different storage space $W _ { u }$

The RANDOM algorithm randomly caches services in UAVs and performs worst on the expected hit ratio. The OPTIMAL algorithm gives the optimal solution to the caching problem (P1), however, it runs for dozens of minutes. Compared with these two algorithms, GCA achieves a near-optimal expected hit ratio within one second. Fig. 4 shows the average hit ratio $\hat { H } _ { a v g } ^ { t }$ achieved by OOA and corresponding expected hit ratio $H _ { e } ,$ where the hit ratio tolerance Îº is set to 0.05. Itâs seen that the gap between $\hat { H } _ { a v g } ^ { t }$ and $H _ { e }$ is within the tolerance in most of the time slots. Once $H _ { e } - \hat { H } _ { a v g } ^ { t - 1 } > \kappa .$ , caching decisions is updated. Fig. 5 shows the expected hit ratio achieved by different caching algorithms under different storage space. The expected hit ratio increases with the increase in the storage space since larger storage space allows UAVs to cache more services. Similar to Fig. 3, among three algorithms, GCA can always achieve a near-optimal solution, and compared with the running time of the OPTIMAL algorithm, which takes several hours, GCA only takes less than 1 s.

Service Delay/Energy Consumption. Figs. 6 and 7 show the service delay of each time slot and UAVsâ cumulative energy consumption, respectively. Compared with other three algorithms, OOA achieves the lowest service delay under strict energy constraints. The service delay of TJSO is 8% higher than that of OOA in the first 80 time slots, and lower than that of OOA in the last 20 time slots. However, TJSO ignores the energy constraint and causes the highest energy consumption among four algorithms. DELAY algorithm achieves the lowest service delay at first. Nevertheless, due to the abuse of energy, most of the energy budget is used in the first 60 time slots, causing the service delay of DELAY significantly increases in the last 40 time slots. The RANDOM algorithm performs worst in service delay, which is 33% higher than that of OOA. In the last 10 time slots, because OOA strictly follows the energy budget constraint, and the remaining energy budgets of most UAVs currently are in short supply, OOA no longer changes the positions of UAVs. Since the flight energy consumption occupies much of the previous energy consumption, and many tasks are offloaded to the remote cloud, the energy consumption of OOA hardly increases at this time.

<!-- image-->  
Fig. 6. Service delay of each time slot.

<!-- image-->  
Fig. 7. Cumulative energy consumption.

<!-- image-->  
Fig. 8. Service delay with different numbers of types of services S.

Effect of Service Types: Fig. 8 shows the total service delay under different numbers of types of services after 100 time slots. We can see that OOA always achieves the lowest service delay with different numbers of service types. The service delay increases as the number of service types increases, since a larger number of types of service makes it difficult for UAVs to cache the services corresponding to user tasks. In addition, when the number of service types is small, the service delay achieved by TJSO is close to that of OOA. As the number of service types increases, the gap between OOA and TJSO gradually widens, which shows that it is for TJSOâs caching strategy to adapt to the diverse service types.

<!-- image-->  
Fig. 9. Service delay with different coverage radius $R _ { u } .$

<!-- image-->  
Fig. 10. Energy consumption with different $R _ { u } .$

<!-- image-->  
Fig. 11. Service delay with different storage space $W _ { u }$

Effect of UAVâs Coverage Radius: Figs. 9 and 10 show the total service delay and energy consumption under different coverage radius of UAV after 100 time slots. It can be observed that the service delay decreases as the coverage radius of UAV increases, since a larger coverage radius of UAVs means UAVs are more likely to receive offloaded tasks from UEs. The service delay of OOA hardly decreases when the coverage radius is larger than 250 m because a coverage radius of 250 m is enough for UAVs to cover most of the UEs in our simulation.

Effect of UAVâs Storage Space: Figs. 11 and 12 show the total service delay and energy consumption under different storage space of UAV after 100 time slots. It can be observed that the service delay decreases as the storage space of UAV increases because a larger storage space of UAV means UAVs are more likely to have the services that UEs require. As the storage space increases, the gap between the delay of OOA and TJSO becomes larger. Thatâs because a larger storage space will amplify the benefit of OOAâs dynamic caching algorithm.

<!-- image-->  
Fig. 12. Energy consumption with different storage space $W _ { u } .$

<!-- image-->  
Fig. 13. Service delay with different numbers of UAVs and UEs.

<!-- image-->  
Fig. 14. Service delay with different energy budgets $E _ { u } ^ { \mathrm { m a x } }$ and maximum served tasks $N _ { u } ^ { \mathrm { m a x } }$

Effect of the Number of UAVs and UEs. Fig. 13 show the total service delay under different numbers of UAV and UEs after 100 time slots. With a fixed number of UEs, the increase in the number of UAVs leads to the decrease in the service delay because more tasks can be offloaded to the UAVs. Notice that when the number of UEs is small, the increase in the number of UAVs can only slightly reduce the service delay, indicating that two UAVs have processed most of the tasks from UEs on this occasion.

Effect of UAVâs Energy Budget and computing capacity: Fig. 14 show the total service delay under different energy budgets $E _ { u } ^ { \mathrm { m a x } }$ and maximum served tasks $N _ { u } ^ { \mathrm { m a x } }$ of UAVs after 100 time slots. As shown in the figure, the service delay decreases with the increase of UAVâs energy budget and maximum served tasks, since more tasks can be processed by UAVs. The service delay of different energy budgets is similar when $N _ { u } ^ { \mathrm { m a x } }$ is small. This is because in this case, the bottleneck of the delay is the computing capacity of the UAV.

## VI. CONCLUSION

In this paper, we study the joint service caching and task offloading problem for UAV-assisted MEC Networks. Different from existing work, we consider a practical scenario where the caching decision is updated dynamically according to UEâs preference on services. We further consider the limited energy capacity of UAVs, and jointly optimize UAV trajectory and task offloading based on the caching decision. We propose an online algorithm, OOA, that dynamically updates services caching and determines task offloading at each time slot to minimize the overall service delay. OOA employs a greedy algorithm to greedily make caching decisions to maximize the sum of the hit ratio, and an iterative algorithm to alternately determine UAV trajectory and task offloading. Both the theoretical analysis and large-scale simulations verify the performance of OOA. Simulation results show that OOA can reduce the service delay by up to 33%, compared with three benchmarks.

## REFERENCES

[1] J. Cao, X. Liu, X. Su, S. Tarkoma, and P. Hui, âContext-Aware Augmented Reality With 5G Edge,â in Proc. IEEE Glob. Commun. Conf., 2021, pp. 1â 6.

[2] Y. C. Hu, M. Patel, D. Sabella, N. Sprecher, and V. Young, âMobile edge computingâA key technology towards 5G,â ETSI White Paper, vol. 11, no. 11, pp. 1â16, 2015.

[3] B. Li, Z. Fei, and Y. Zhang, âUAV communications for 5G and beyond: Recent advances and future trends,â IEEE Internet Things J., vol. 6, no. 2, pp. 2241â2263, Apr. 2019.

[4] Xinhua, âChina deploys UAV for telecom restoration in rain-hit henan,â 2021. [Online]. Available: http://en.people.cn/n3/2021/0723/c90000- 9875913.html

[5] A. Malik, J. Kim, K. S. Kim, and W.-Y. Shin, âA personalized preference learning framework for caching in mobile networks,â IEEE Trans. Mobile Comput., vol. 20, no. 6, pp. 2124â2139, Jun. 2021.

[6] X. Zhang et al., âData-driven caching with usersâ content preference privacy in information-centric networks,â IEEE Trans. Wireless Commun., vol. 20, no. 9, pp. 5744â5753, Sep. 2021.

[7] Z. Xu et al., âCollaborate or separate? Distributed service caching in mobile edge clouds,â in Proc. IEEE Conf. Comput. Commun., 2020, pp. 2066â 2075.

[8] V. Farhadi et al., âService placement and request scheduling for dataintensive applications in edge clouds,â IEEE/ACM Trans. Netw., vol. 29, no. 2, pp. 779â792, Apr. 2021.

[9] D.-T. Do, A.-T. Le, Y. Liu, and A. Jamalipour, âUser grouping and energy harvesting in UAV-NOMA system with AF/DF relaying,â IEEE Trans. Veh. Technol., vol. 70, no. 11, pp. 11855â11868, Nov. 2021.

[10] D.-H. Tran, V.-D. Nguyen, S. Chatzinotas, T. X. Vu, and B. Ottersten, âUAV relay-assisted emergency communications in IoT networks: Resource allocation and trajectory optimization,â IEEE Trans. Wireless Commun., vol. 21, no. 3, pp. 1621â1637, Mar. 2022.

[11] X. Lyu, C. Ren, W. Ni, H. Tian, R. P. Liu, and X. Tao, âDistributed online learning of cooperative caching in edge cloud,â IEEE Trans. Mobile Comput., vol. 20, no. 8, pp. 2550â2562, Aug. 2021.

[12] X. Xia, F. Chen, Q. He, J. Grundy, M. Abdelrazek, and H. Jin, âOnline collaborative data caching in edge computing,â IEEE Trans. Parallel Distrib. Syst., vol. 32, no. 2, pp. 281â294, Feb. 2021.

[13] Y. Han, L. Ai, R. Wang, J. Wu, D. Liu, and H. Ren, âCache placement optimization in mobile edge computing networks with unaware environmentâAn extended multi-armed bandit approach,â IEEE Trans. Wireless Commun., vol. 20, no. 12, pp. 8119â8133, Dec. 2021.

[14] S. Gu, X. Sun, Z. Yang, T. Huang, W. Xiang, and K. Yu, âEnergy-aware coded caching strategy design with resource optimization for satelliteuav-vehicle-integrated networks,â IEEE Internet Things J., vol. 9, no. 8, pp. 5799â5811, Apr. 2022.

[15] R. Zhang, R. Lu, X. Cheng, N. Wang, and L. Yang, âA UAV-enabled data dissemination protocol with proactive caching and file sharing in V2X networks,â IEEE Trans. Commun., vol. 69, no. 6, pp. 3930â3942, Jun. 2021.

[16] L. Li et al., âDelay optimization in multi-UAV edge caching networks: A robust mean field game,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 808â819, Jan. 2021.

[17] K. Wang, X. Zhang, L. Duan, and J. Tie, âMulti-UAV cooperative trajectory for servicing dynamic demands and charging battery,â IEEE Trans. Mobile Comput., vol. 22, no. 3, pp. 1599â1614, Mar. 2023.

[18] Z. Ning et al., â5G-enabled UAV-to-community offloading: Joint trajectory design and task scheduling,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3306â3320, Nov. 2021.

[19] S. Zhu, L. Gui, D. Zhao, N. Cheng, Q. Zhang, and X. Lang, âLearningbased computation offloading approaches in UAVs-assisted edge computing,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 928â944, Jan. 2021.

[20] C. Sun, W. Ni, and X. Wang, âJoint computation offloading and trajectory planning for UAV-assisted edge computing,â IEEE Trans. Wireless Commun., vol. 20, no. 8, pp. 5343â5358, Aug. 2021.

[21] Q. Tang, L. Liu, C. Jin, J. Wang, Z. Liao, and Y. Luo, âAn UAV-assisted mobile edge computing offloading strategy for minimizing energy consumption,â Comput. Netw., vol. 207, 2022, Art. no. 108857.

[22] M. Zhang, E.-H. Mohammed, and S. X. Ng, âIntelligent caching in UAVaided networks,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 739â752, Jan. 2022.

[23] Y. Qu et al., âService provisioning for UAV-enabled mobile edge computing,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3287â3305, Nov. 2021.

[24] R. Zhou, X. Wu, H. Tan, and R. Zhang, âTwo time-scale joint service caching and task offloading for UAV-assisted mobile edge computing,â in Proc. IEEE Conf. Comput. Commun., 2022, pp. 1189â1198.

[25] J. Luo, J. Song, F.-C. Zheng, L. Gao, and T. Wang, âUser-centric UAV deployment and content placement in cache-enabled multi-UAV networks,â IEEE Trans. Veh. Technol., vol. 71, no. 5, pp. 5656â5660, May 2022.

[26] J. Ji, K. Zhu, D. Niyato, and R. Wang, âJoint cache placement, flight trajectory, and transmission power optimization for multi-UAV assisted wireless networks,â IEEE Trans. Wireless Commun., vol. 19, no. 8, pp. 5389â5403, Aug. 2020.

[27] T. Zhang, Z. Wang, Y. Liu, W. Xu, and A. Nallanathan, âJoint resource, deployment, and caching optimization for ar applications in dynamic UAV NOMA networks,â IEEE Trans. Wireless Commun., vol. 21, no. 5, pp. 3409â3422, May 2022.

[28] H. Wu, F. Lyu, C. Zhou, J. Chen, L. Wang, and X. Shen, âOptimal UAV caching and trajectory in aerial-assisted vehicular networks: A learningbased approach,â IEEE J. Sel. Areas Commun., vol. 38, no. 12, pp. 2783â 2797, Dec. 2020.

[29] Y. Wu, S. Yao, Y. Yang, Z. Hu, and C.-X. Wang, âSemigradient-based cooperative caching algorithm for mobile social networks,â in Proc. IEEE Glob. Commun. Conf., 2016, pp. 1â6.

[30] B. Chen and C. Yang, âCaching policy for cache-enabled d2d communications by learning user preference,â IEEE Trans. Commun., vol. 66, no. 12, pp. 6586â6601, Dec. 2018.

[31] M. J. Magazine and M.-S. Chern, âA note on approximation schemes for multidimensional knapsack problems,â Math. Oper. Res., vol. 9, no. 2, pp. 244â247, 1984.

[32] A. Kulik and H. Shachnai, âThere is no EPTAS for two-dimensional knapsack,â Inf. Process. Lett., vol. 110, no. 16, pp. 707â710, 2010.

[33] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[34] M. Grant and S. Boyd, âCVX: Matlab software for disciplined convex programming, version 2.1,â 2014. [Online]. Available: http://cvxr.com/cvx

[35] A. Krause and C. Guestrin, âA note on the budgeted maximization of submodular functions,â Carnegie Mellon University, Center for Automated Learning and Discovery, 2005.

[36] S. Boyd, S. P. Boyd, and L. Vandenberghe, Convex Optimization. Cambridge, U.K.: Cambridge Univ. Press, 2004.

[37] P. Lai et al., âOptimal edge user allocation in edge computing with variable sized vector bin packing,â in Proc. Int. Conf. Service-Oriented Comput., Springer, 2018, pp. 230â245.

[38] DJI, DJI Mavic 2 Pro, 2022. [Online]. Available: https://www.dji.com/cn/ mavic-2-enterprise-advanced/specs

<!-- image-->

Ruiting Zhou (Member, IEEE) received the PhD degree from the Department of Computer Science, University of Calgary, Canada, in 2018. She is a professor with the School of Computer Science Engineering, Southeast University. Her research interests include cloud computing, machine learning and mobile network optimization. She has published research papers in top-tier computer science conferences and journals, including IEEE INFOCOM, ACM MOBI-HOC, IEEE/ACM Transactions on Networking, IEEE Journal on Selected Areas in Communications, IEEE

Transactions on Mobile Computing. She serves as the TPC chair for INFOCOM workshop-ICCN 2019â2023. She also serves as a reviewer for international conferences and journals such us IEEE ICDCS, IEEE/ACM IWQoS, IEEE SECON, IEEE Journal on Selected Areas in Communications, IEEE/ACM Transactions on Networking, IEEE Transactions on Mobile Computing, IEEE Transactions on Cloud Computing.

<!-- image-->

Yifeng Huang received the BE degree from the School of Computer Science, Wuhan University, China, in 2021. He is currently working toward the MS degree with the School of Cyber Science and Engineering, Wuhan University. His research interests include edge computing, UAV-enabled wireless networks, and online scheduling.

<!-- image-->

Yufeng Wang received the BE degree in information security from Wuhan University, China, in 2023. Now he is working toward the masterâs degree with Institute for Network Science and Cyberspace, Tsinghua University. His research interests include UAV-enabled wireless networks, network optimization and satellite networking.

<!-- image-->

Lei Jiao (Member, IEEE) received the PhD degree in computer science from the University of GÃ¶ttingen, Germany. He is currently a faculty member with the University of Oregon. Previously he worked as a member of technical staff with Nokia Bell Labs in Dublin, Ireland and as a researcher with IBM Research in Beijing, China. He is interested in the mathematics of optimization, control, learning, and economics applied to computer and telecommunication systems, networks, and services. He publishes papers in journals such as IEEE Journal on Selected

Areas in Communications, IEEE/ACM Transactions on Networking, IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Mobile Computing, and IEEE Transactions on Dependable and Secure Computing, and in conferences such as INFOCOM, MOBIHOC, ICNP, ICDCS, SECON, and IPDPS. He is an NSF CAREER awardee. He also received Best Paper Awards of IEEE LANMAN 2013 and IEEE CNS 2019. He was on the program committees of many conferences, including INFOCOM, MOBIHOC, ICDCS, IWQoS, and WWW, and was also the program chair of multiple workshops with INFOCOM and ICDCS.

<!-- image-->

Haisheng Tan (Senior Member, IEEE) received the BE degree in software engineering and BS degree in management both from the University of Science and Technology of China (USTC) with the highest honor, and the PhD degree in computer science from the University of Hong Kong (HKU). He is currently a professor with USTC. His research interests lie primarily in networking algorithm design and system implementation, where he has published more than 90 papers in prestigious journals and conferences. He recently received the awards of ACM China Rising

Star (Hefei Chapter), the Distinguished TPC Member of INFOCOM 2019, the Best Paper Award in WASAâ19, CWSNâ20, PDCATâ20 and ICPADSâ21.

<!-- image-->

Renli Zhang received the BE degree in information security from Wuhan University, China, in 2020. He is currently working toward the MS degree with the School of Cyber Science and Engineering, Wuhan University. His research interests include UAV-enabled wireless networks, network optimization, and online scheduling.

<!-- image-->

Libing Wu received the PhD degree from Wuhan University, China, in 2006. He is currently a professor with the School of Cyber Science and Engineering, Wuhan University. He was a visiting scholar with the Advanced Networking Lab, University of Kentucky, in 2011. He was a senior visiting fellow with the State University of New York, Buffalo, in 2017. His research interests include network security, Internet of Things, machine learning and data security.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_5_img_1.png|page_5_img_1]]
2. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_11_img_1.jpeg|page_11_img_1]]
3. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_13_img_1.jpeg|page_13_img_1]]
4. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_13_img_2.jpeg|page_13_img_2]]
5. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_13_img_3.jpeg|page_13_img_3]]
6. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_13_img_4.jpeg|page_13_img_4]]
7. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_13_img_5.jpeg|page_13_img_5]]
8. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_13_img_6.jpeg|page_13_img_6]]
9. [[../extracted_images/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks/page_13_img_7.jpeg|page_13_img_7]]

---

