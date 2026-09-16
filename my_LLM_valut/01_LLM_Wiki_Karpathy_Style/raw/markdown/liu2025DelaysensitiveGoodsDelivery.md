# Delay-Sensitive Goods Delivery and In-Situ Sensing Using a Multi-Task Drone

Bin Liu , Member, IEEE, Wei Ni , Fellow, IEEE, Ren Ping Liu , Senior Member, IEEE, Y. Jay Guo , Fellow, IEEE, and Hongbo Zhu , Member, IEEE

AbstractâDrones are evolving into highly capable and adaptable devices, prompting the development of advanced control frameworks. This paper introduces a novel online control framework tailored for a multi-task drone, explicitly addressing the simultaneous execution of in-situ sensing and goods delivery. To tackle this complex scenario, a finite-horizon Markov decision process (FH-MDP) is formulated to ensure not only the prompt delivery of goods but also the minimization of energy consumption and the maximization of the droneâs reward for in-situ sensing. A significant contribution lies in establishing the monotonicity and subadditivity of the FH-MDP. This mathematical foundation provides evidence for the existence of an optimal, monotone, deterministic Markovian policy. The crux of the optimal policy revolves around flight distance- and time-related thresholds, determining the precise points at which the drone should switch its optimal action. This unique feature empowers the multi-task drone to make real-time decisions, such as adjusting flight speed or engaging in in-situ sensing, by comparing its current state with these predefined thresholds. This process can be accomplished with a linear complexity, ensuring efficiency in decision-making. The optimality of our approach is rigorously demonstrated through numerical validation, where it is compared against a computationally expensive, dynamic programming-based alternative. Under the considered simulation settings, our approach reduces drone energy consumption by a substantial 19.8% compared to existing benchmarks. This not only highlights the practical effectiveness of the proposed framework but also underscores its potential for significant advancements in the field of drone operations and energy efficiency.

Index TermsâDrone, multitask, delivery, in situ sensing, finitehorizon Markov decision process.

Digital Object Identifier 10.1109/TMC.2025.3570437

## I. INTRODUCTION

D RONES, also known as autonomousaerial vehicles, enjoyexcellent flexibility and have been widely applied to provide environmental sensing [1], weather monitoring [2], goods delivery [3], and disaster rescue [4], [5]. Equipped with embedded sensors, such as cameras, microphones, and thermometers, a drone is often capable of conducting multiple different tasks [6], [7]. As depicted in Fig. 1, a multi-task drone equipped with sensors and dispatched to deliver goods, can carry out in-situ sensing along its delivery route.

To coordinate the different tasks of a multi-task drone (e.g., goods delivery and in-situ sensing) is challenging. One reason is that roadside tasks may require different levels of commitment and tolerate different latencies [8], [9]. As illustrated in Fig. 1, goods delivery is typically subject to strict deadlines, while in-situ sensing is a secondary task and only performed when possible. Another reason is that multitasking can give rise to difficulties in the energy management of a drone [10]. Since drones are primarily powered by batteries, it is important to utilize the battery energy efficiently while completing multiple tasks by their deadlines [11], [12].

The control of a multi-task delivery drone would involve joint optimization of speed and task schedule along the trajectory. The energy consumption of the drone is a nonlinear function of its speed, leading to non-convexity in both objectives and constraints [13]. The decisions consist of both continuous and binary variables, i.e., the droneâs speed and task selection [14]. Such a drone scheduling problem is typically a mixed integer non-linear program (MINLP) [15], [16], requires a sequential decision process, and incurs a prohibitive computational complexity, especially when there is a large state space [17].

On the other hand, the rise of the low-altitude economy has created new opportunities and challenges for drone deployment, particularly in multi-task operations [18]. Multi-task drones can enhance operational efficiency and resource utilization, making them a critical component of the low-altitude economy. Effective scheduling and control of these drones are essential to balance energy consumption, timely task execution, and mission rewards. Optimizing drone task coordination, this research contributes to the broader applications of drones in smart logistics, environmental monitoring, and other emerging low-altitude scenarios.

<!-- image-->  
Fig. 1. An illustration of a multi-task drone performing goods delivery and in-situ sensing at places of interest (POIs). The drone follows the proposed method by first gathering its preplanned flight route, required arrival time, and any in-situ sensing requests along the way. Based on this information, the drone adjusts its speed and decides whether to perform sensing tasks at the POIs using thresholds related to flight distance and time. By comparing the remaining distance m and elapsed time t with these thresholds, the drone optimizes its actions to ensure timely goods delivery, minimize energy consumption, and maximize its reward for in-situ sensing.

## A. Single-Task Drone

Existing studies have been predominantly focused on singletask drones, most of which aimed to optimize specific aspects of drone operations, such as navigation, task scheduling, or energy consumption. In [19], drone navigation was formulated as a generalized traveling salesman problem (TSP) for persistent monitoring missions. By determining the order of the targets to be visited and monitored, the longest interval between consecutive visits was minimized to optimize the route. However, the computational complexity is high and becomes prohibitive when the number of nodes is large. In [20], based on a vector field approach, a curved path-following method was proposed to control a drone conducting video tracking and surveillance. By exploiting the notion of input-to-state stability, the along-track error and the cross-track error were reduced for robust surveillance and tracking. This method is suited for shortdistance planning but is complex and less suitable for long-range planning. Bartolini et al. [21] investigated the multi-trip task assignment of squads of drones for early target inspection. An NP-hard integer linear programming (ILP) was formulated to schedule multiple drones. A greedy and prune (GaP) algorithm was designed to offer 1/2 of the optimality in polynomial time. In [22] and [23], scheduling a truck-drone delivery system was studied, where a truck carries parcels and acts as a moving dock for drones. The dronesâ flights was scheduled by solving an MINLP problem with a high complexity. In [24], a distributed scheduling framework was proposed for drone navigation and roadside charging. Multi-agent deep reinforcement learning integrated with convolutional neural networks (CNNs) was used to minimize the energy consumption of the drones. However, there is a risk of overfitting of the CNNs to the training data. Zhang et al. [25] considered a drone powered by solar energy and roadside charging stations. By optimizing its trajectory and schedule, sustainable communication services were maintained without energy outage.

The above existing studies [19], [20], [21], [22], [23], [24], [25] have primarily focused on single-task drones. While they offer solutions for specific scenarios such as navigation, task scheduling, or energy management, they lack the ability to simultaneously consider and optimize multiple objectives. Consequently, they cannot handle the complexities of multi-task drone operations, as the multiple tasks may need to be optimized concurrently.

## B. Multi-Task Drone

Recent studies have increasingly considered multiple tasks for drones, including goods delivery and sensing. In [26], multipurpose drone task assignment and trajectory planning was cast as an ILP under a simplified circular neighborhood area assumption. However, the assumption may not accurately reflect the complexities of real-world scenarios. In [27], a two-phase optimization approach was developed for drone-based package pickup and delivery, with a heuristic solution designed. However, the heuristic algorithm cannot handle dynamic requests, such as dynamically sensing task requests, and it is not adjustable in real-time. In [28], task assignment was based on a greedy allocation strategy, and ant colony optimization (ACO) was applied to plan the route of drones to minimize energy consumption while maximizing task coverage. However, the routes need to be replanned when the coverage task changes.

In [29], a joint routing and charging strategy was optimized using mixed-integer linear programming. A heuristic algorithm was developed to operate within limited computation time, but lacks real-time adjustability. In [30], a stochastic-geometry-based analysis of multi-purpose drones was conducted for package and data delivery, focusing on the impact of spatial randomness in delivery points and communication links. This was later extended in [31] to develop a stochastic geometry-based trajectory design for multi-purpose drones, which optimizes package and data delivery using probabilistic models but fails to guarantee timely delivery. In [32], a decentralized routing framework for cellular-connected drones was proposed, where a game-theoretic approach was employed to provide efficient goods delivery and sensing and ensure trajectory confidentiality. However, the framework did not optimize the droneâs speed for energy efficiency.

While these studies [26], [27], [28], [29], [30], [31], [32] have considered multiple objectives, they have not addressed the challenges of balancing strict delivery deadlines with secondary in-situ sensing tasks. Moreover, the studies generally lack the capability of updating the optimal policy online to adapt to in-situ sensing requests arising during the droneâs flight.

## C. Contribution

This paper presents a novel and optimal control policy for a multi-task drone that performs delay-bounded goods delivery, as well as in-situ sensing whenever possible. A new finite-horizon Markov decision process (FH-MDP) problem is formulated to ensure timely goods delivery, minimize the droneâs energy consumption, and maximize its reward for in-situ sensing. We prove the existence of a monotone deterministic Markovian policy for the optimal action selection of the drone; i.e., the optimal action (i.e., the speed and the decision of performing in-situ sensing) is monotone with respect to the remaining trip and elapsed time. We also reveal the optimal action only changes when either of two thresholds regarding the remaining distance or elapsed time is reached. By comparing its state with the thresholds, the drone can optimally decide its action online.

The key contributions of this paper are summarized as follows.

The contribution of this work lies in selecting and qualifying the use of FH-MDP and monotone deterministic Markovian policy to model and solve the new problem of multi-task drone control, as well as extending the model for online applications.

We establish the new multi-task drone control framework, where the drone can dynamically select its action at each slot, including full speed, cruise speed, or performing in-situ sensing. A new FH-MDP problem is formulated to maximize its sensing reward, minimize its energy consumption, and ensure timely goods delivery.

By proving the monotonicity and subadditivity of the new FH-MDP, we qualify the use of deterministic Markovian policy to solve the FH-MDP problem. Monotone deterministic Markovian policies are known to be the optimal policy for FH-MDP problems [33].

We unveil the new threshold-based structure of the optimal policy, and derive the thresholds at which the action of the drone optimally switches. The drone can select its optimal action instantly at each time slot by comparing its current state with the thresholds at a linear complexity.

Extensive simulations corroborate that the new approach is able to guarantee the droneâs timely delivery, minimize its energy consumption, and maximize its sensing reward through comparison with the computationally expensive, standard dynamic programming (DP)-based solution. The simulations also show that our algorithm can save 19.8% of the droneâs energy under our considered simulation setting, compared to its alternative methods.

FH-MDP problems were used to model a high-speed railway passengerâs selection of network interfaces [34], a droneâs decision to hitchhike on passing vehicles [35], or an electric vehicle (EV)âs charging strategy for long-range driving [36]. In [34], for a given train schedule, the network interface selection was optimized between mmWave and LTE interfaces to minimize operational cost while satisfying the service requests of passengers. In [35], a droneâs selection of actions, including flight speed, hitchhiking (on passing ground vehicles), or recharging at roadside charging stations, was optimized to minimize its energy consumption while ensuring its timely arrival at its destination. In [36], the charging stations and durations were optimized to minimize the travel time of an EV and prevent its battery depletion along the trip. However, these works [34], [35], [36] focused on scheduling tasks of a single type, and are inapplicable to the multi-task drone control problem studied in this paper. Moreover, the complete a-priori knowledge of the passengerâs itinerary and the passing ground vehicles was required to optimize offline network selection [34], hitch-hiking schedule [35], and EV charging strategy [36]. In contrast, the optimal policy developed in this paper can be updated online, adapting to sensing requests arising during the flight of the drone.

This paper is arranged as follows. Section II depicts the system configuration. Section III casts the multi-task drone control problem. In Section IV, we prove the threshold-based structure of the optimal policy, which can be obtained online with considerably low complexity. Numerical and simulation results are provided using practical flight parameters in Section V. Finally, Section VI concludes the paper.

## II. SYSTEM MODEL

Fig. 1 illustrates the proposed multi-task drone system, where a multi-task drone delivers the parcels to the destination and performs in-situ sensing along the delivery route. We consider a rotary-wing drone due to its excellent maneuverability and increasing applications in complex urban environments, especially in tasks involving vertical takeoff, landing, and hovering. As fixed-wing drones cannot hover or perform vertical takeoff/landing, they are less flexible and suited for complex urban environments or tasks. This paper assumes that the drone can either carry the sensing data back to its post or upload the data to a server if connected via cellular networks. Both approaches are feasible and straightforward, particularly with the growing adoption of cellular-connected drones [7].

The focus of our work is on drone multi-task scheduling for goods delivery (or more generally, high-priority and compulsory tasks) and in-situ sensing (or more generally, low-priority and optional tasks). Specifically, goods delivery is typically subject to strict deadlines. By contrast, in-situ sensing is a secondary task performed only when feasible. This consideration explicitly prioritizes goods delivery over in-situ sensing. Nevertheless, nothing stops us from prioritizing individual tasks by assigning specific time frames and locations. The priorities are configured prior to multi-task scheduling.

## A. Task Requirement of the Drone

The drone is expected to reach the destination by no later than a specified time T (min), and the preplanned route length is M (km). The drone can perform in-situ sensing at the places of interest (POIs) along the delivery route and report the sensing results to get rewards. The drone needs to slow down and hover over POIs to perform sensing. Hovering over the POI takes extra time and may prevent timely delivery. Since drones are typically powered by batteries, it is critical to meticulously control the speed of the drone and sensing activities for timely goods delivery and maximum sensing rewards.

We divide T evenly into time slots with the duration of each slot being Ï (in seconds) Let $t \in { \mathcal { T } } = \{ 1 , 2 , \dots , T / \tau \}$ be the = 1 2index to the time slots. The drone can choose A number of different speeds, or hover and sense over POI at a time slot. Let $v _ { a }$ denote the droneâs speed, $a \in \mathcal { A } = \{ 1 , \dots , A \} . \ v _ { 1 } = v _ { \operatorname* { m a x } }$ is the full speed. $v _ { A } = v _ { \mathrm { e c o } }$ = 1is the cruise speed. $a = A + 1$ = = + 1indicates the drone performs in-situ sensing. The total flight length M is discretized into segments with length Î» per segment. Let $m \in \mathcal { M } = \{ 0 , \lambda , 2 \lambda , . . . , M \}$ be the index to the segments. = 0 2We also divide the droneâs path in line with street blocks. The index to a street block is $l \in \mathcal { L } = \{ 1 , . . . , L \}$ , where L denotes the number of street blocks along the flight path from start to destination. Each street block has a length of $L _ { 0 }$ . The street blocks are categorized into two types:

1) $\mathcal { L } ^ { ( 0 ) }$ : The street blocks with no POI;

2) $\mathcal { L } ^ { ( 1 ) }$ : The street blocks with POIs, i.e., sensing needed.

We define $\pmb { s } = ( m , l )$ as the droneâs state. m is the distance = ( )ahead toward the final destination. l is the droneâs current street block. Since in-situ sensing is only performed in the POIs, the different actions that the drone can possibly take at different street blocks are expressed as

$$
\begin{array} { r } { A ^ { ( l ) } = \left\{ \begin{array} { l l } { \mathcal { A } , } & { \mathrm { i f ~ } l \in \mathcal { L } ^ { ( 0 ) } ; } \\ { \mathcal { A } \bigcup \{ A + 1 \} , } & { \mathrm { i f ~ } l \in \mathcal { L } ^ { ( 1 ) } . } \end{array} \right. } \end{array}\tag{1}
$$

In other words, selecting different speeds $a \in { \mathcal { A } }$ is always possible, while the action of in-situ sensing $( a = A + 1 )$ heavily depends on the current location of the drone.

## B. Reward for Sensing and Penalty for Late Arrival

Our mechanism dynamically determines task execution based on the rewards, remaining flight distance, and elapsed time $( \mathrm { i . e . }$ location-dependent factors) to maximize rewards from sensing

tasks while ensuring timely goods delivery. Task priority or data quality can be abstracted and reflected by adjusting the task rewards accordingly.

A reward can be provided to the drone for the in-situ sensing activities conducted at the POIs, as given by

$$
R _ { t } ( l , a ) = R ( l , a ) = \left\{ \begin{array} { l l } { \mu ( l ) \tau _ { s } ( l ) , } & { \mathrm { i f ~ } a = A + 1 , l \in \mathcal { L } ^ { ( 1 ) } ; } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{2}
$$

where $\mu ( l )$ is the unit sensing reward per second at POI location ( )l. The reward for performing a sensing task depends on the required sensing time, and is measured by the amount of electricity (in Wh) that can be purchased.

The drone is expected to reach the destination by time T . A penalty is issued if the drone fails to do so, i.e., the drone arrives at or after $T + 1$ . We define the penalty (in Wh) as

$$
E _ { T + 1 } ( s ) = E _ { T + 1 } ( m ) = \Phi ( m ) ,\tag{3}
$$

where $\Phi ( m )$ is non-decreasing and convex in m, and $\Phi ( m ) = 0$ $\forall m \leq 0$ ( ) Î¦( ) = 0. The cost function concerning the considered penalty is expressed as

$$
\begin{array} { r } { U _ { t } ( s , a ) = \left\{ \begin{array} { l l } { E _ { t } ( l , a ) - R _ { t } ( l , a ) , } & { \mathrm { i f ~ } t \in \mathcal { T } ; } \\ { E _ { T + 1 } ( m ) , } & { \mathrm { i f ~ } t = T + 1 . } \end{array} \right. } \end{array}\tag{4}
$$

## C. Mobility and Energy Models of the Drone

The traveled distance of the drone over a time slot when the drone takes action a is given by

$$
\begin{array} { r l } & { D _ { t } ( l , a ) = D ( l , a ) } \\ & { \quad = \{ { v _ { a } } \tau , \ \qquad \mathrm { i f } a \in \ r { A , l \in \mathcal { L } } = \mathcal { L } ^ { ( 0 ) } \bigcup \mathcal { L } ^ { ( 1 ) } ; } \\ & { \quad = \{ { v _ { A } } ( \tau - \tau _ { s } ( l ) ) + v _ { a } \tau _ { s } ( l ) , \mathrm { i f } a = A + 1 , l \in \mathcal { L } ^ { ( 1 ) } .  } \end{array}\tag{5}
$$

where $\tau _ { s } ( l )$ is the sensing duration at street block l. After ( )sensing, the drone proceeds at the cruise speed $v _ { A }$ for the rest of the slot.

The droneâs energy consumption is primarily dominated by its propulsion energy and the in-situ sensing-related energy [37], [38]. The propulsion power consumption of the drone (in Watts) depends on its flying speed and is usually a function of the flying speed, i.e., $p ( v _ { a } )$ [39]. Consider a rotary-wing drone. At the speed $v _ { a }$ ( ), its propulsion power is given by [40]

$$
\begin{array} { r } { p ( v _ { a } ) = \underbrace { P _ { 0 } \left( 1 + \frac { 3 v _ { a } ^ { 2 } } { Q _ { \mathrm { t i p } } ^ { 2 } } \right) } _ { \mathrm { b l a d e ~ p r o f l e } } + \underbrace { P _ { i } \kappa \left( \sqrt { \kappa ^ { 2 } + \frac { v _ { a } ^ { 4 } } { 4 V _ { 0 } ^ { 4 } } } - \frac { v _ { a } ^ { 2 } } { 2 V _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } } _ { \mathrm { i n d u c e d } } } \\ { + \underbrace { \frac { 1 } { 2 } \chi f _ { 0 } g W v _ { a } ^ { 3 } } _ { \mathrm { p a r a s i t e } } , \qquad ( 6 ) } \end{array}
$$

where $P _ { 0 }$ and $P _ { i }$ are the blade profile power and induced hovering power, respectively; $Q _ { \mathrm { t i p } }$ is the tip speed of the rotor blade; $\kappa = \Gamma / \omega$ is the thrust-to-weight ratio, with being the = Îthrust power and $\omega = \omega _ { \mathrm { s e l f } } + \omega _ { \mathrm { l o a d } }$ Îbeing the total weight, i.e., the total mass of the drone and its load; $\begin{array} { r } { V _ { 0 } = \sqrt { \frac { \omega } { 2 \chi W } } } \end{array}$ is the mean rotor-induced hovering speed; $f _ { 0 }$ and $g$ are the fuselage drag ratio and rotor solidity, respectively; Ï and $W$ are the air density and rotor disc area, respectively.

The energy consumption (in Joules) when action a is chosen at street block l can be written as

$$
\begin{array} { r l } & { E _ { t } ( l , a ) = } \\ & { \begin{array} { l } { \int p ( v _ { a } ) \tau , \ } & { \mathrm { i f } a \in A , l \in \mathcal { L } ; } \\ { p ( v _ { 1 } ) [ \tau - \tau _ { s } ( l ) ] + [ p ( v _ { a } ) + p _ { s } ] \tau _ { s } ( l ) , } & { \mathrm { i f } a = A + 1 , l \in \mathcal { L } ^ { ( 1 ) } , } \end{array} } \end{array}\tag{7}
$$

where $p _ { s }$ is the normalized power consumption for collecting and reporting information at block l. When the drone performs in-situ sensing, the drone also consumes power to hover over the POIs. The energy used for in-situ sensing is usually much lower than the droneâs propulsion [40].

We note that the energy and time consumptions introduced by acceleration and deceleration during the droneâs approach to a PoI are factored into the evaluation of the overall energy efficiency and time usage in the proposed control method. Specifically, the energy consumption due to acceleration and deceleration is accounted for in the overall power consumption for the sensing task $, \mathrm { i . e . , } p ( v _ { A + 1 } ) \mathrm { i n } ( 4 )$ . The time required for the sensing task at the PoI is incorporated into the sensing duration $\tau _ { s } ( l )$

## III. PROBLEM STATEMENT

In this section, we select the actions of the drone to minimize the energy usage of the drone, maximize the sensing reward, and complete the goods delivery in time. With the definition of state $s = ( m , l )$ , the state transition probability is the probability of = ( )state s transiting to state $s ^ { \prime }$ if action a is performed, as given by

$$
\begin{array} { r l } & { \mathrm { P r } ( s ^ { \prime } | s , a ) = \mathrm { P r } \left( ( m ^ { \prime } , l ^ { \prime } ) | ( m , l ) , a \right) } \\ & { \qquad = \mathrm { P r } \left( l ^ { \prime } | l \right) \mathrm { P r } \left( m ^ { \prime } | ( m , l ) , a \right) , } \end{array}\tag{8}
$$

where $\mathrm { P r } ( m ^ { \prime } | ( m , l ) , a )$ gives the distance transition probability, Pr( ( ) )i.e., the conditional probability of the remaining distance transiting from m to m if the drone takes action a at street block l, and can be written as

$$
\operatorname* { P r } { ( m ^ { \prime } | ( m , l ) , a ) } = \left\{ { 1 , } { \mathrm { ~ i f ~ } } m ^ { \prime } = [ m - D ( l , a ) ] ^ { + } ; \right.\tag{9}
$$

and $[ m ] ^ { + } = \operatorname* { m a x } \{ 0 , m \} . \operatorname* { P r } ( l ^ { \prime } | l )$ is the location transition prob-[ ] = max 0 Pr( )ability of the drone when the droneâs location changes from street block l to street block $l ^ { \prime } ,$ as given by

$$
\operatorname* { P r } { ( l ^ { \prime } | l ) } = { \left\{ \begin{array} { l l } { 1 , { \mathrm { ~ i f ~ } } D ( l , a ) \geq L _ { 0 } ; } \\ { 0 , { \mathrm { ~ o t h e r w i s e } } , } \end{array} \right. }\tag{10}
$$

where the drone flies from street block l to street block $l ^ { \prime }$ on the condition that the flight distance over the time slot outreaches a street block.

To minimize the energy consumption of the drone, maximize the sensing reward, and deliver the goods in time, the multi-task drone control problem is formulated as

$$
\underset { \pi \in \Pi } { \mathrm { m i n i m i z e } } \quad E _ { s } ^ { \pi } \left[ \sum _ { t = 1 } ^ { T } U _ { t } \left( \pmb { s } _ { t } ^ { \pi } , \pi _ { t } \left( \pmb { s } _ { t } ^ { \pi } \right) \right) + U _ { T + 1 } \left( \pmb { s } _ { T + 1 } ^ { \pi } \right) \right]
$$

$$
\begin{array} { r l } { \mathrm { s . t . } } & { { } \pi _ { t } \in \mathcal { A } \cup \{ A + 1 \} ; } \\ { \quad } & { { } s _ { 0 } = \left( M , l _ { 0 } \right) , } \end{array}\tag{11}
$$

where the control policy of the drone, denoted by $\pi ,$ is composed of sequential actions during the flight. $\pi = \{ \pi _ { t } ( m , l ) , \forall m \in$ $\mathcal { M } , l \in \mathcal { L } , t \in \mathcal { T } \}$ , where $\pi _ { t } ( m , l )$ = ( )denotes the action chosen at state $\pmb { s } = ( m , l )$ for $t \in { \mathcal { T } } , { \mathrm { i . e . , ~ } } \pi _ { t } ( m , l )$ provides the mapping: $\pi _ { t } ( m , l ) : \mathcal { M } \times \mathcal { L }  \mathcal { A } \cup \{ A + 1 \}$ ). All the possible ac-( ) : + 1tion policies of the drone constitute the feasible set, denoted by . $s ^ { \pi }$ represents the state after applying policy Ï under state $s . E _ { s } ^ { \pi } [ \cdot ]$ denotes the expectation with respect to the probability mobility distribution of the drone. $s _ { 0 } = ( M , l _ { 0 } )$ is the initial state of the drone. $l _ { 0 }$ = ( )is the starting street block of the drone.

Problem (11) is an FH-MDP problem. Conventionally, the optimal control policy can be obtained offline by using dynamic programming (DP) [41]. The minimum cost $V _ { t } ( s )$ is the optimal Bellman equation [42], as given by

$$
V _ { t } ( s ) = V _ { t } ( m , l ) = \operatorname* { m i n } _ { a \in \mathcal { A } ^ { ( l ) } } \{ K _ { t } ( m , l , a ) \} ,\tag{12}
$$

where $K _ { t } ( m , l , a )$ is the expected cost function and

$$
\begin{array} { l } { { \displaystyle K _ { t } ( m , l , a ) = E _ { t } ( l , a ) - R _ { t } ( l , a ) } } \\ { { \displaystyle \quad \quad + \sum _ { l ^ { \prime } \in { \mathcal { L } } } \sum _ { m ^ { \prime } \in M } \mathrm { P r } \left( ( m ^ { \prime } , l ^ { \prime } ) | ( m , l ) , a \right) V _ { t + 1 } ( m ^ { \prime } , l ^ { \prime } ) } } \\ { { \displaystyle \qquad \quad ( 1 3 a } } \\ { { \displaystyle \quad = \operatorname* { m i n } \left\{ m , D _ { t } ( l , a ) \right\} \cdot \zeta _ { t } ( l , a ) } } \\ { { \displaystyle \quad \quad + \sum _ { l ^ { \prime } \in { \mathcal { L } } } \mathrm { P r } \left( l ^ { \prime } | l \right) V _ { t + 1 } \left( | m - D _ { t } ( l , a ) | ^ { + } , l ^ { \prime } \right) . } } \end{array}\tag{13b}
$$

The expected cost function $K _ { t } ( m , l , a )$ is composed of the ( )immediate cost at slot t, and the estimated cost in the remaining slots. (13b) is achieved by substituting the energy consumption (7), the in-situ sensing reward (2), and the transition probability (8) into (13a). $\zeta ( l , a )$ is the normalized cost regarding the ( )traveled distance per time slot, i.e.,

$$
\begin{array} { r l } & { \zeta _ { t } ( l , a ) = \frac { U _ { t } ( l , a ) } { D _ { t } ( l , a ) } } \\ & { = \left\{ \begin{array} { l l } { \frac { p ( v _ { a } ) } { v _ { a } } , } & { \mathrm { i f ~ } a \in \mathcal { A } , l \in \mathcal { L } ; } \\ { \frac { p ( v _ { A } ) ( \tau - \tau _ { s } ( l ) ) + [ p ( v _ { a } ) + p _ { s } - \mu ( l ) ] \tau _ { s } ( l ) } { v _ { A } ( \tau - \tau _ { s } ( l ) ) + v _ { a } \tau _ { s } ( l ) } , \mathrm { i f ~ } a = A + 1 , l \in \mathcal { L } ^ { ( 1 ) } . } \end{array} \right. } \end{array}\tag{14}
$$

From the principle of optimality [41], $\pi ^ { * } = \{ \pi _ { t } ^ { * } ( m , l )$ , âm $\in$ $\mathcal { M } , l \in \mathcal { L } , t \in \mathcal { T } \}$ = ( )is the optimal policy, when the action selected at state s satisfies

$$
\pi _ { t } ^ { * } ( s ) = \pi _ { t } ^ { * } ( m , l ) = \operatorname * { a r g m i n } _ { a \in \mathcal { A } ^ { ( l ) } } K _ { t } ( m , l , a ) .\tag{15}
$$

The optimal action $\pi _ { t } ^ { * } ( m , l )$ can be achieved by using the ( )backward induction of DP. However, the computational complexity of DP is $\mathcal { O } ( A T M / \lambda )$ [43], [44]. As the growth of the ( )trip distance M, allowed time T , and speed mode number A, the state space of the multi-task drone control problem, i.e., problem (11), can be large, incurring an excessive complexity.

## IV. OPTIMAL MONOTONE POLICY AND THRESHOLD-BASED STRUCTURE

If the Bellman equation of an FH-MDP satisfies two conditions of monotonicity and subadditivity, a monotone deterministic Markovian policy can be built as the optimal policy for the FH-MDP [33]. The monotone deterministic Markovian policy can be obtained by comparing the state of the FH-MDP with thresholds pertinent to the monotonicity and subadditivity conditions, hence reducing the computational complexity significantly.

In this section, we develop the monotone deterministic Markovian policy for the action selection of the multi-task drone. Specifically, we first verify that the optimal Bellman equation of the FH-MDP, i.e., $V _ { t } ( m , l )$ , is non-decreasing in both the ( )remaining distance m and the elapsed time t. In other words, the Bellman equation is monotone. We also prove the subadditivity of the expected cost function of the FH-MDP, $K _ { t } ( m , l , a )$ . Then, ( )we establish the optimal monotone deterministic Markovian policy of problem (11), based on the subadditivity, i.e., the optimal action $\pi _ { t } ^ { * } ( m , l )$ in (15) is monotone in both m and t. The ( )optimal policy exhibits a threshold-based structure, where the switch of the optimal action is only triggered when either of two thresholds about m and t is met. By evaluating the droneâs state against the thresholds, the action of the drone can be optimally selected at each time slot.

## A. Monotonicity of Bellman Equation

We first reveal the monotonicity of the optimal Bellman equation $V _ { t } ( m , l ) \mathrel { ( 1 2 ) }$ ). Assume that the sensing time $\tau _ { s }$ is locationindependent, i.e., $\tau _ { s } : = \tau _ { s } ( l )$ $\forall l \in { \mathcal { L } }$ . The traveled distance of := ( )the drone over a slot in (5) can be updated as

$$
d _ { a } = { \left\{ \begin{array} { l l } { v _ { a } \tau , } & { { \mathrm { i f ~ } } a \in { \mathcal { A } } { \mathrm { ~ a n d ~ } } l \in { \mathcal { L } } ; } \\ { v _ { A } ( \tau - \tau _ { s } ) + v _ { A + 1 } \tau _ { s } , } & { { \mathrm { i f ~ } } a = A + 1 { \mathrm { ~ a n d ~ } } l \in { \mathcal { L } } ^ { ( 1 ) } . } \end{array} \right. }\tag{16}
$$

From $( 1 6 ) , d _ { 1 } > \cdot \cdot \cdot > d _ { A } > d _ { A + 1 }$ holds for $v _ { \mathrm { m a x } } > v _ { \mathrm { e c o } } >$ $v _ { \mathrm { h o v } }$ and non-zero sensing time, $\mathrm { i . e . , } \tau _ { s } > 0$ . We normalize the 0cost function of the drone, i.e., (14), with the unit traveled distance per time slot, as given by

$$
\begin{array} { r l } & { \zeta _ { a } = } \\ & { \left\{ p ( v _ { a } ) / v _ { a } , \right. \qquad \mathrm { i f } \ a \in \mathcal { A } ; } \\ & { \left\{ \frac { p ( v _ { A } ) ( \tau - \tau _ { s } ) + [ p ( v _ { A + 1 } ) + p _ { s } - \mu ( l ) ] \tau _ { s } } { v _ { A } ( \tau - \tau _ { s } ) + v _ { A + 1 } \tau _ { s } } , \mathrm { ~ i f } \ a = A + 1 , l \in \mathcal { L } ^ { ( 1 ) } . \right. } \end{array}\tag{17}
$$

Hence, the expected cost function (13) is reformed as

$$
\begin{array} { r l } {  { K _ { t } ( m , l , a ) = \operatorname* { m i n } \{ m , d _ { a } \} \cdot \zeta _ { a } } } \\ & { + \displaystyle \sum _ { l ^ { \prime } \in \mathcal { L } } \mathrm { P r } ( l ^ { \prime } | l ) V _ { t + 1 } ( [ m - d _ { a } ] ^ { + } , l ^ { \prime } ) . } \end{array}\tag{18}
$$

The following lemma shows that the overtime penalty function for not completing the delivery in time is much higher than the rewards for executing the in-situ sensing, or the energy saving of choosing a lower speed.

Lemma 1: The cost function $U _ { t } ( l , a )$ in (4) satisfies

$$
U _ { T + 1 } ( m ) - U _ { T + 1 } ( m - d _ { a } ) \geq U _ { t } ( l , a ) .\tag{19}
$$

Namely, the incurred overtime penalty is higher than the energy consumption for the same flying distance.

Proof: $U _ { t } ( l , a ) = \zeta _ { a } d _ { a }$ is a linearly increasing function of ( ) =the traveled distance $d _ { a }$ . With (3), for $t = T + 1$ , the cost function $U _ { T + 1 } ( m ) - U _ { T + 1 } ( m - d _ { a } ) = \Phi ( m ) - \Phi ( m - d _ { a } )$ . The penalty function $\Phi ( m )$ gives a non-decreasing convex function of $m ,$ and $\Phi ( m ) - \Phi ( m - d _ { a } )$ rises more than quadratically with $d _ { a }$ Î¦( ) Î¦( ). The penalty of not accomplishing a flight distance of $d _ { a }$ in time is larger than the cost of flying the distance. -

Based on Lemma 1, we establish the monotonicity of $V _ { t } ( m , l )$ in (12), as follows.

Theorem 1: (Monotonicity) $\forall l \in { \mathcal { L } }$ , the optimal Bellman equation $V _ { t } ( m , l )$ satisfies

i) $V _ { t } ( m , l )$ )does not decrease in $m , \forall t \in \mathcal { T }$

ii) $V _ { t } ( m , l )$ does not decrease in $t , \forall m \in { \mathcal { M } }$

( )Namely, the higher expected cost incurs when a longer flight distance or less flight time remains before the drone can reach the destination in time. The Bellman (12) exhibits monotonicity.

Proof: See Appendix A, available online.

## B. Subadditivity and Optimal Policy

As revealed in Theorem 1, we obtain the monotonicity of the minimum cost function, which is the prerequisite for the optimal monotone deterministic Markovian policy of problem (11). In this subsection, we reveal the optimal policy, and show its threshold-based structure. In what follows, we first derive the irreducible set of candidate actions at any street block l, denoted by $\widetilde { A } ^ { ( l ) }$ . Then, we prove the subadditivity of the expected cost function in (13), i.e., $K _ { t } ( m , l , a )$ , in the action set. Based on the subadditivity, we reveal the threshold-based structure of the optimal policy.

Lemma 2: Suppose that there are two candidate actions, i.e., $a ^ { + } , a ^ { - } \in \mathcal { A } ^ { ( l ) }$ . If

$$
d _ { a ^ { + } } \geq d _ { a ^ { - } } \mathrm { ~ a n d ~ } \zeta _ { a ^ { + } } \leq \zeta _ { a ^ { - } } ,\tag{20}
$$

then action aâ would never be selected in the optimal policy and the candidate action set can be reduced to $\mathcal { \tilde { A } } ^ { ( i ) } = \mathcal { A } ^ { ( l ) } \setminus \left\{ a ^ { - } \right\}$ =In other words, the actions satisfying (20) would consume more energy over the same flight distance and can be precluded for the selection of the optimal action.

Proof: See Appendix B, available online.

Based on Lemma 2, we can derive that the sensing action $( a = A + 1 )$ can only be selected in the optimal policy when = + 1the following condition specified in Lemma 3 is satisfied.

Lemma 3: If the distance traveled per time satisfies $d _ { A } >$ $d _ { A + 1 }$ , the sufficient condition of choosing the sensing action in the optimal policy is given by

$$
\zeta _ { A + 1 } \leq \zeta _ { A } .\tag{21}
$$

There is also a low bound of the sensing reward per POI, denoted by $\mu _ { \mathrm { L o w } }$ , which is achieved if $\tau _ { s } = 1$ and satisfies

$$
\mu _ { \mathrm { L o w } } \left( l \right) > p ( v _ { A + 1 } ) + p _ { s } - \frac { v _ { \mathrm { h o v } } } { v _ { \mathrm { e c o } } } p ( v _ { A } ) .\tag{22}
$$

Proof: See Appendix C, available online.

Remark 1: As suggested in Lemma 3, the in-situ sensing action $a = A + 1$ (i.e., sensing) should not be chosen if the sensing reward is no larger than the threshold specified in (22), as the reward cannot compensate for the energy and time consumed to complete the sensing task. The threshold of selecting action $a = A + 1$ depends on the unit reward $\mu ,$ flight speed, and power = + 1consumption, which are salient parameters of the optimal policy and thresholds.

Next, we introduce the definitions and important properties of subadditivity in Definition 1 [41], [42].

Definition 1: Function $g ( i , j , k )$ is subadditive in ${ \mathcal { T } } \times { \mathcal { T } } .$ , for given k, $\mathrm { i f } \forall i ^ { + } , i ^ { - } \in \mathcal { T } , i ^ { + } > i ^ { - }$ ), and $\forall j ^ { + } , j ^ { - } \in \mathcal { I } , j ^ { + } > j ^ { - }$

$$
g ( i ^ { + } , j ^ { + } , k ) - g ( i ^ { + } , j ^ { - } , k ) \leq g ( i ^ { - } , j ^ { + } , k ) - g ( i ^ { - } , j ^ { - } , k ) .\tag{)(23}
$$

If $g ( i , j , k )$ is subadditive in $\mathcal { T } \times \mathcal { I }$ for a given k, then

$$
f ( i , k ) = \arg \operatorname* { m i n } _ { j \in \mathcal { T } } g ( i , j , k )\tag{24}
$$

decreases monotonically with the increase of i.

Following Definition 1, we can show the subadditivity of $K _ { t } ( m , l , a )$ , and the optimal action $\pi _ { t } ^ { * } ( m , l )$ in (15) is monotone in regards of the remaining distance m and the elapsed time t. By pairwise comparing the actions in the action set, we find two thresholds regarding m and t, at which a switch of the droneâs optimal actions takes place.

Theorem 2: Suppose two candidate actions, $a ^ { + } , a ^ { - } \in \widetilde { \mathcal { A } } ^ { ( l ) }$ with $a ^ { + } > a ^ { - } ;$

i) (Distance threshold) If $d _ { a ^ { + } } \leq d _ { a ^ { - } }$ â and $\zeta _ { a ^ { + } } \leq \zeta _ { a ^ { - } }$ , then $K _ { t } ( m , l , a )$ yields subadditivity in M $\times \{ a ^ { - } , a ^ { + } \}$ and $\pi _ { t } ^ { * } ( m , l )$ )decreases monotonically with m. The following ( )threshold of m exists: $\exists m ^ { * } ( l , t ) \geq 0$

$$
\pi _ { t } ^ { * } ( m , l ) = \left\{ a ^ { + } , \mathrm { i f } m \leq m ^ { * } ( l , t ) ; \right.\tag{25}
$$

ii) (Time threshold) If $d _ { a ^ { + } } \leq d _ { a ^ { - } }$ and $\zeta _ { a ^ { + } } \leq \zeta _ { a ^ { - } }$ , then $K _ { t } ( m , l , a )$ yields subadditivity in $\mathcal { T } \times \{ a ^ { - } , a ^ { + } \}$ and $\pi _ { t } ^ { * } ( m , l )$ )decreases monotonically with t. The following threshold of t exists: $\exists t ^ { * } ( l , m ) \geq 0$ ,

$$
\pi _ { t } ^ { * } ( m , l ) = { \binom { a ^ { + } , { \mathrm { ~ i f ~ } } t \leq t ^ { * } ( l , m ) } { a ^ { - } , { \mathrm { ~ o t h e r w i s e . ~ } } } }\tag{26}
$$

Proof: See Appendix D, available online.

With the thresholds discovered in Theorem 2, the optimal monotone deterministic Markovian policy of the droneâs action selection can be achieved by evaluating m and t with the thresholds, as stated in Theorem 3.

Theorem 3: Suppose that the drone can take the actions of full speed, cruise speed, and in-situ sensing for illustration convenience $( \mathrm { i . e . , } A = 2 )$ . The optimal policy $\pi ^ { * } = \{ \pi _ { t } { } ^ { * } ( m , l )$ , âm â $\mathcal { M } , l \in \mathcal { L } , t \in \mathcal { T } \}$ can be given as

1) For $l \in \mathcal { L } ^ { ( 0 ) }$ and $a \in \mathcal { A } ^ { ( l ) } = \{ 1 , 2 \}$ , we have

$$
\pi _ { t } { } ^ { * } ( m , l ) = \ { \left\{ \begin{array} { l l } { 2 } & { { \mathrm { i f } } \ m \leq m _ { 1 } ^ { * } ( l , t ) ; } \\ { 1 } & { { \mathrm { o t h e r w i s e } } ; } \end{array} \right. }\tag{27}
$$

$$
\pi _ { t } { } ^ { * } ( m , l ) = { \left\{ \begin{array} { l l } { 2 } & { { \mathrm { i f ~ } } t \leq t _ { 1 } ^ { * } ( l , m ) ; } \\ { 1 } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }\tag{28}
$$

Algorithm 1: Threshold-Based Action Selection Algorithm.   
1: Planning Stage: M, T , and L.   
2: Run Generation of the thresholding   
3: Selection Stage:   
4: Set $t \gets 1 , m \gets M$   
5: while $t \leq T$ and $m > 0$ do   
6: 0Collect the current location of the drone and obtain   
the current state $\mathbf { \boldsymbol { s } } _ { t } = ( m , l )$   
7: Obtain $\pi _ { t } { } ^ { * } ( m , l )$ = ( )by comparing $\mathbf { } _ { s _ { t } }$ and the thresholds   
$\{ m ^ { * } , t ^ { * } \}$   
8: $a ^ { * } \gets { \pi _ { t } } ^ { * } ( m , l )$   
9: ( Update m $ [ m - d _ { a ^ { * } } ] ^ { + } , t  t + 1$   
10: end while

2) For $l \in \mathcal { L } ^ { ( 1 ) }$ and $a \in \mathcal { A } ^ { ( l ) } = \{ 1 , 2 , 3 \}$ , we have

$$
\pi _ { t } { } ^ { * } ( m , l ) = \left\{ \begin{array} { l l } { { 3 } } & { { \mathrm { i f } \ m \leq m _ { 1 } ^ { * } ( l , t ) ; } } \\ { { 2 } } & { { \mathrm { i f } \ m _ { 1 } ^ { * } ( l , t ) < \ m \leq m _ { 2 } ^ { * } ( l , t ) ; } } \\ { { 1 } } & { { \mathrm { o t h e r w i s e . } } } \end{array} \right.\tag{29}
$$

$$
\pi _ { t } { } ^ { * } ( m , l ) = \ \left\{ { \begin{array} { l l } { 3 } & { { \mathrm { i f ~ } } t \leq t _ { 1 } ^ { * } ( l , m ) ; } \\ { 2 } & { { \mathrm { i f ~ } } t _ { 1 } ^ { * } ( l , m ) < \ t \leq t _ { 2 } ^ { * } ( l , m ) ; } \\ { 1 } & { { \mathrm { o t h e r w i s e } } . } \end{array} } \right.\tag{30}
$$

Here, $m _ { n } ^ { * } ( l , t )$ represents the n-th threshold of the remaining ( )flight distance m at slot $t . ~ t _ { n } ^ { * } ( l , m )$ is the n-th threshold of the ( )elapsed time t at the remaining distance m. $n \in \{ 1 , 2 \}$ . This theorem can be readily generalized to the case of $A > 2$

Proof: Refer to Appendix D, available online.

Remark 2: Theorem 3 reveals the optimal policy of problem (11), which can be produced by making a comparison between the state $\mathbf { \boldsymbol { s } } _ { t }$ and the two thresholds $m _ { n } ^ { * } ( l , t )$ and $t _ { n } ^ { * } ( l , m )$ ï¼ ( ) ( )rather than searching the state space. Algorithm 1 describes the optimal policy based on the thresholds generated using Algorithm 2 (as described below). The computational complexity of the optimal policy can be reduced from $\mathcal { O } ( A M T / \lambda )$ of the standard DP method [44] to $\mathcal { O } ( A \cdot \operatorname* { m a x } \{ M / \lambda , T \} )$ ), since Algorithm 2 only needs to generate $A \cdot \operatorname* { m a x } \{ M / \lambda , T \}$ )threshmaxolds (as described below) and Algorithm 1 only needs to compare the current action of the drone with up to A other actions for each of the $\{ M / \lambda , T \}$ slots/segments.

## C. Threshold-Based Action Selection

Theorem 2 exhibits the threshold-based, monotone structure of the optimal policy in m and t, and remains unchanged as long as neither of the two thresholds about m and t is satisfied. To derive the thresholds, we first present conditions of the thresholds, as specified in Corollary 1.

Corollary 1: The distance threshold $m _ { n } ^ { * } ( l , t )$ does not increase with the elapsed time t, i.e.,

$$
m _ { n } ^ { * } ( l , t ) \geq m _ { n } ^ { * } ( l , t + 1 ) , \forall l \in \mathcal { L } .\tag{31}
$$

The time threshold $t _ { n } ^ { * } ( l , m )$ does not increase with the remaining flight distance $m ,$ i.e.,

$$
t _ { n } ^ { * } ( l , m ) \geq t _ { n } ^ { * } ( l , m + \lambda ) , \forall l \in \mathcal { L } .\tag{32}
$$

Proof: See Appendix E, available online.

Algorithm 2: Generation of the Thresholds.   
1: Calculate the total number of thresholds   
$N _ { \mathrm { T h r e s } } = \vert \mathcal { A } ^ { ( l ) } \vert - 1$   
2: =for action $\dot { n }  \dot { \{ 1 , \dots , | \tilde { \mathcal { A } } ^ { ( l ) } | \} }$ do   
3: Set m $ m _ { n } ^ { * } ( l , t + 1 )$   
4: ( + 1)Set the threshold indicator $f l a g \gets 0$   
5: while $m \leq M$ and $f l a g = 0$ do   
6: Compute $K _ { t } ( m , l , a )$ = 0using (13);   
7: Set $\pi _ { t } ^ { * } ( m , l ) \gets \mathrm { a r g m i n } _ { a \in \{ n , n + 1 \} } K _ { t } ( m , l , a )$   
8: Set $V _ { t } ( m , l ) \gets K _ { t } ( m , l , \tilde { \pi _ { t } ^ { * } } ( m , \dot { l ) } )$   
9: if $\pi _ { t } ^ { * } ( m , l ) = n + 1$ ( then   
10: $m _ { n } ^ { * } ( l , t ) \gets m$   
11: $f l a g \gets 1 ;$   
12: end if   
13: m $ m + \lambda$   
14: end while   
15: end for

From Corollary 1, the thresholds, $m _ { n } ^ { * } ( l , t )$ and $t _ { n } ^ { * } ( l , m )$ , are ( ) ( )generated with the following steps. We start by determining the irreducible set, ${ \tilde { \cal A } } ,$ based on Lemma 2, and decide (the number of thresholds needed per slot t, $N _ { \mathrm { T h r e s } } = \vert \tilde { \mathcal { A } } ^ { ( l ) } \vert - 1$ = 1The indexes to the actions are reordered in the descending order of $d _ { a }$ in the set $\{ 1 , \ldots , | \tilde { \mathcal { A } } ^ { ( l ) } | \}$ . Then, we assess the n-th threshold, $m _ { n } ^ { * } ( l , t )$ 1, between the n-th and the $( n + 1 )$ -th ( ) ( + 1)action. According to Corollary 1, the drone can start evaluating the distance threshold based on the threshold at slot t , i.e., $m \gets m _ { n } ^ { * } ( l , t + 1 )$ + 1. With the growth of m, the action that (satisfies $\mathfrak { l } _ { a \in \{ n , n + 1 \} } K _ { t } ( m , l , a )$ changes from the n-th to the n -th in the action set $\tilde { \mathcal { A } } ^ { ( l ) }$ . The value of $m$ when the ( + 1)drone changes its action is the threshold $m _ { n } ^ { * } ( l , t )$ . Likewise, the time threshold $t _ { n } ^ { * } ( l , m )$ can be generated.

( )Remark 3: The complexity of the proposed approach is dominated by the generation of the thresholds at which the drone shall optimally change its action. In the worst-case scenario, the irreducible set $\tilde { \mathcal { A } } ^ { ( l ) }$ in Lemma 2 contains all $A + 1$ possible actions, i.e., the number of thresholds is $N _ { \mathrm { T h r e s } } = \vert \tilde { A } ^ { ( l ) } \vert - 1 = A$ per = 1 =slot. According to Theorem 2, the generation of the thresholds needs to evaluate (15) for $A \times \operatorname* { m a x } \{ M / \lambda , T \}$ times. Every time max(15) is evaluated for a given street block, the expected cost function (18) needs to be evaluated for two successive actions, i.e., the current action and a potential candidate for the next, to obtain the respective minimum expected costs of the two actions and subsequently the threshold for the potential switch between the actions. Hence, (18) needs to be evaluated twice, each involving four floating point operations (FLOPs), i.e., two real-value multiplications and two real-value additions. As a result, the worst-case complexity requires $8 A \times \operatorname* { m a x } \{ M / \lambda , T \}$ FLOPs. 8 maxFor example, 32,640 FLOPs are needed, when $T = 3 0$ slots, $M = 1 0 . 2 \times 1 0 ^ { 3 } ~ \mathrm { m } .$ , and Î» m. A commercially available = 10 2 10 = 10drone flight computer, e.g., Raspberry Pi-zero, can execute 319 million FLOPs per second. Suppose that 10% of the FLOPs are spared to run the proposed algorithm. The optimal policy can be generated within about 1.03 ms.

Remark 4: It may not be possible to acquire all sensing requests beforehand in practice [45]. For example, a POI-free street block can become a POI street block when a new demand arises for in-situ sensing in the street block. Algorithm 1 suits online applications. Specifically, when a new request of in-situ sensing is generated along the drone flight, we first compare the unit reward of the new in-situ sensing request with the low bound of the unit reward $\mu _ { \mathrm { L o w } }$ in (22). If the unit reward is lower than $\mu _ { \mathrm { L o w } }$ , the in-situ sensing is not performed and the drone maintains the current schedule. If the unit reward is higher than $\mu _ { \mathrm { L o w } }$ and the sufficient condition in Lemma 3 is satisfied, Algorithm 2 is executed to update the thresholds of the optimal policy, followed by Algorithm 1 to compare the droneâs current state $\mathbf { \Delta } _ { s _ { t } }$ with the thresholds to decide if the new in-situ sensing task can be performed without jeopardizing the timely delivery. In this way, the algorithms can run online to update the droneâs schedule in response to new in-situ sensing requests arising.

Remark 5: Our proposed approach focuses on the task selection of a multi-task drone under the constraint of a strict delivery deadline. The approach can ensure timely goods delivery, minimize the droneâs energy consumption, and maximize the reward for sensing tasks conducted. While the proposed speed control and task scheduling policy of the multi-task drone for joint delay-bounded goods delivery and in-situ sensing is promising, many challenges are yet to be addressed, such as weather impact, obstacle detection, collision avoidance, flight range, etc. For example, weather conditions, e.g., rain, snow, wind, and extreme temperatures, can affect the droneâs operation, making it difficult to deliver goods or perform sensing [38]. The stability of the drone is critical, especially when it needs to approach targets on the ground for in-situ sensing. Given the route and sensing tasks selected, the drone needs to carry out finer-grained flight control and manoeuvre to address weather impact [46], collision avoidance [47], and noise pollution [48].

## V. NUMERICAL AND SIMULATION RESULT

In this section, we validate the new threshold-based optimal policy in terms of optimality. Then, we evaluate the policy based on real-life drone flight parameters from DJI Agras [49]. Comparison studies with identified benchmarks are given in terms of the droneâs energy consumption, in-situ sensing reward, and timely flight completion ratio [50].

## A. Threshold Structure Verification

Fig. 2 verifies the new threshold-based optimal policy, i.e., the proposed Algorithm 1 by comparing with the DP-based optimal policy described at the end of Section III. Fig. 2(a) plots the total cost of the flight under the different values of the required arrival T when the distance M . km. The total cost of the flight = 10 2is defined in (4), consisting of the energy usage and overtime penalty. The new threshold-based policy coincides with the results obtained from the conventional optimal DP-based approach, yet with a significantly lower computational complexity. In other words, the optimality of the new threshold-based policy is validated. As also observed in Fig. 2(a), the penalty of late arrival dominates the total cost when the required delay time is $T < 1 8$ min, since the flight cannot finish in time.

<!-- image-->

<!-- image-->  
(a) Total cost with the increase of required arrival time Tfor $M = 1 0 . 2$ km

(b) $l \in \mathcal { L } ^ { ( 0 ) } , d _ { 1 } > d _ { 2 } , \zeta _ { 1 } > \zeta _ { 2 }$  
<!-- image-->  
(c)lâC(1),d1>d2>d3,S1>S2>S3  
Fig. 2. Validation of the new threshold-based optimal policy, where (b) and (c) are achieved when M = 6 km, and T = 20 min; blue circle â¦, yellow star â, and red stars â stand for actions a = 1 (full speed), $a = 2$ (cruise speed), and $a = 3$ (in-situ sensing), respectively.

TABLE I  
PARAMETERS FOR THE ROTARY-WING DRONE PROPULSION MODEL
<table><tr><td>Parameter</td><td>Description</td><td>Value</td></tr><tr><td> $\overline { { P _ { 0 } } }$ </td><td>Blade profile power</td><td>1850W</td></tr><tr><td> $P _ { i }$ </td><td>Induced hovering power</td><td>150W</td></tr><tr><td> $Q _ { \mathrm { t i p } }$ </td><td>Tip speed of the rotor blade</td><td>12.6 m/s</td></tr><tr><td> $\kappa$ </td><td>Thrust-to-weight ratio</td><td>1.1</td></tr><tr><td> $f _ { 0 }$ </td><td>Fuselage drag ratio</td><td>1.5</td></tr><tr><td> $g$ </td><td>Rotor solidity</td><td>0.05</td></tr><tr><td> $\chi$ </td><td>Air density</td><td> $1 . 2 2 5 \mathrm { k g } / \mathrm { m } ^ { 3 }$ </td></tr><tr><td> $W$ </td><td>Rotor disc area</td><td> $0 . 7 8 5 \mathrm { \stackrel { \sim } { m } { } ^ { 2 } }$ </td></tr><tr><td> $\omega$ </td><td>Total weight</td><td> $2 5 \mathrm { k g }$ </td></tr></table>

18Fig. 2(b) and (c) exhibit the threshold-based structure of the optimal monotone deterministic Markovian policy. Fig. 2(b) shows that, for $l \in \mathcal { L } ^ { ( 0 ) } , \mathcal { A } ^ { ( 0 ) } = \{ 1 , 2 \} . \pi _ { t } ^ { * } ( \bar { m } , l )$ decreases as = 1 2 ( )the remaining distance m grows (i.e., from 1 to 2), when $d _ { 1 } > d _ { 2 }$ and $\zeta _ { 1 } > \zeta _ { 2 }$ . We can see such $m ^ { * } ( l , t ) \ge 0$ that $\pi _ { t } ^ { * } ( m , l ) =$ when $m \leq m ^ { * } ( l , t )$ , and $\pi _ { t } ^ { * } ( m , l ) = 1$ 0when $m > m ^ { * } ( l , t )$ $m ^ { * } ( l , t )$ ( ) ( ) = 1 ( )provides the y-coordinate value of the switching point where the optimal switches from action a  (yellow star â) to action $a = 1$ = 2(blue circle â¦), as the growth of the remaining flight = 1distance m. This validates the new threshold-based structure in a POI-free street block, i.e., $l \in \mathcal { L } ^ { ( 0 ) }$ , as stated in Theorem 3â1). It is also observed that the value of the threshold $m ^ { * } ( l , t )$ is monotonic to the elapsed time t, which characterizes the monotonic property of the threshold, as described in Corollary 1. The case of a POI street block described in Theorem 3â2) can be verified in the same way in Fig. 2(c), and is suppressed for brevity.

## B. Performance Comparison

We assess the proposed algorithms based on real-life drone flight parameters from DJI Agras [49]. The parameters of the rotary-wing drone propulsion model are summarized in Table I. The full speed is $v _ { 1 } = 1 0$ m/s, the cruise speed is $v _ { 2 } = 6 ~ \mathrm { m / s }$ and the hover speed is $v _ { 3 } = 1 \mathrm { m / s }$ = 6. The power consumptions are $p _ { 1 } = 5 9 7 1 . 3 \mathrm { ~ W ~ }$ and $p _ { 2 } = 3 8 7 9 . 1 6$ W for flying the full speed = 5971 3 = 3879 16and cruise speed, respectively. The total power consumption of hovering for in-situ sensing is $p _ { 3 } + p _ { s } = 3 3 0 0 \ \mathrm { W } .$ The weight of the drone and goods is 20 kg and 5 kg. The time slot length is $\tau = 1$ min.

TABLE II  
PARAMETERS OF THE PROPOSED ALGORITHMS
<table><tr><td>Parameter</td><td>Description</td><td>Value</td></tr><tr><td>T  $\bar { \mu }$ </td><td>Time slot length Average unit sensing reward per second</td><td>1 min 3500W</td></tr><tr><td></td><td></td><td></td></tr><tr><td> $\Phi ( m )$ </td><td>Overtime penalty for delayed delivery</td><td> $1 0 m ^ { 2 }$ </td></tr><tr><td> $\lambda$ </td><td>Segment length</td><td>10 m</td></tr><tr><td> $\overline { { \tau } } _ { s }$ </td><td>Average sensing time</td><td>48s</td></tr></table>

In-situ sensing can acquire fine-grained information about a target area by flying the drone considerably close to the target area and obtaining an excellent view of the area, e.g., traffic conditions or crowd density at a road intersection. Without loss of generality, we parameterize the in-situ sensing tasks by associating each sensing task with a location, start time, required sensing duration, and reward. Assume that the location of a sensing task is randomly selected from the road intersections in the considered area with an average sensing reward $\bar { \mu } ,$ and the arrivals of the tasks follow a constant arrival time model with a Poisson distribution [51]. Also assume that the average task density $( \mathrm { i . e . }$ , arrival rate) of the Poisson distribution is $\bar { \rho ( \mathcal { L } ^ { ( 1 ) } ) }$ , ( )and the sensing durations yield the exponential distribution with the average duration of $\bar { \tau } _ { s } .$ . The reward for a task is measured by Â¯the amount of electricity that can be purchased, where $\mu$ denotes the unit reward per second for a sensing task. In this paper, the average unit sensing reward per second is Î¼ ,  W, with an average sensing time of $\bar { \tau } _ { s } = 4 8 ~ \mathrm { s } .$ Â¯ = 3 000. The density of street blocks Â¯ =with sensing requirements is $\rho ( \mathcal { L } ^ { ( 1 ) } ) = 0 . 4 ;$ unless specified ( ) = 0 4otherwise. Without loss of generality, we set the overtime penalty for delayed delivery $\Phi ( m ) = 1 0 m ^ { 2 }$ in our simulation [42]. The segment length is $\lambda = 1 0 1$ m. Other parameters of the proposed algorithms are summarized in Table II.

To the best of our knowledge, the problem studied in this paper has never been studied in the literature. No existing algorithm is directly comparable. We extend relevant state-of-the-art approaches originally developed for drone delivery, and make them comparable with our proposed method. Specifically, we simulate the following benchmarks for our proposed algorithms:

- MP-ILP [26]: The speed control and sensing task selection were jointly cast as an ILP problem to minimize the flight time for delivery and maximize the sensing rewards. The method developed in [26] is adopted to solve the ILP.

<!-- image-->  
Fig. 3. The energy usage against the required delivery distances, when the specified delay T is 30 min.

<!-- image-->  
Fig. 4. A screenshot of the simulation of the optimal drone control for delayaware goods delivery and in-situ sensing.

GD-ACO [28]: The sensing task is selected based on a greedy allocation strategy. The route planning was optimized based on ACO to minimize the energy consumption and maximize the sensing rewards.

Stochastic-geometry-based task selection (SGO-TS) [31]: The sensing task is selected based on rewards and locations, assuming a uniform task distribution. SGO-TS also adjusts the flight speed to minimize flight time.

- JSP-MIP [29]: The joint sensing task selection and routing (JSR) problem is solved using mixed-integer programming (MIP) to minimize both route distance and energy consumption.

By comparing Figs. 3, 5, and 6, we observe that the proposed Algorithm 1 achieves a better trade-off between energy consumption and task rewards while ensuring timely goods delivery.

Energy Consumption: Fig. 3 plots the energy usage under different required delivery distances when the specified delay T is 30 min. The triangle  represents the utmost flight distance ( )of the drone that each scheme can reach by T . To minimize the flight time, the drones using MP-ILP and SGO-TS are inclined to choose the high speed. Hence, the energy consumption of the drone undergoes the steepest growth. In contrast, the drones utilizing GD-ACO and JSP-MIP prioritize energy savings by opting to cruise, which conserves more energy but restricts the flight distance within the given time. Specifically, the drone conducts in-situ sensing at all POI street blocks and fails to deliver goods in time. Consequently, GD-ACO is the first to be restrained by the delivery deadline as the required flight distance M increases, resulting in the shortest flight distance of 8.1 km among all schemes. In contrast, Algorithm 1 dynamically chooses actions for the drone by assessing the remaining distance and elapsed time, while ensuring timely delivery with the minimum energy consumption. Fig. 3 demonstrates that Algorithm 1 can save 19.8% and 24.1% of the droneâs energy, compared to MP-ILP and SGO-TS, respectively.

<!-- image-->  
Fig. 5. The timely flight completion ratio of the flight distance M = 8.4 km, as the allowed flight time T increases.

<!-- image-->  
Fig. 6. The normalized in-situ sensing rewards for M = 8.4 km, as T increases.

To visualize the droneâs actions optimized by Algorithm 1 and used to plot Fig. 3, we take the flight distance of 7.8 km on Fig. 3 as an example and implement the algorithm in a popular, computer-based robotic simulator, i.e., CoppeliaSim robot simulator. CoppeliaSim has been broadly used to demonstrate the designs and concepts of drone applications and controls; see [52], [53], [54], [55], [56]. The optimal drone control policy produced by the proposed algorithm is available at https://www.youtube.com/watch?v=UgP9mKvNLLA, with a screenshot provided in Fig. 4.

<!-- image-->  
Fig. 7. The timely flight completion ratio under different POI densities $\rho ( \mathcal { L } ^ { ( 1 ) } )$ .

Sensing Tasks: Figs. 5 and 6 plot the flight completion rate and the normalized rewards over the flight distance $M = 8 . 4$ km, = 8 4respectively, as T grows. In Fig. 5, only Algorithm 1 can accomplish the flight within 18 min. Being aware of the delivery deadline, Algorithm 1 dynamically chooses actions for the drone in accordance with the remaining distance and elapsed time, and the drone performs in-situ sensing when it does not compromise the timely delivery. In Fig. 6, Algorithm 1 only performs in-situ sensing when $T > 2 4$ min. By contrast, MP-ILP and GD-ACO 24prioritize sensing for rewards whenever possible. While more rewards are returned, arrival is longer delayed. Herein, the rewards are normalized over the unit sensing reward Î¼. MP-ILP and SGO-TS require the drone to fly persistently at full speed to minimize its flight time, leading to a higher completion rate at the expense of higher energy consumption; see Fig. 3.

Fig. 7 plots the completion rate of drone flight under different POI densities $\rho ( \mathcal { L } ^ { ( 1 ) } )$ , where the required flight distance is $M = 8 . 4$ ( )km and the allowed flight time is $T = 2 8$ min. = 8 4 = 28Algorithm 1 can dynamically choose to perform in-situ sensing and hence complete the flight within the allowed delay T . The flight completion rates of MP-ILP and GD-ACO drop rapidly, as the POI density grows. This is because performing in-situ sensing consumes time and may prevent timely delivery.

Fig. 8 evaluates the normalized sensing rewards of the drone obtained under different flight distances, with the growth of the allowed flight time T . The longer flight time T grants the drone more flexibility to choose in-situ sensing. With the same T , a shorter flight distance allows the drone to obtain a higher reward through performing in-situ sensing. In the proposed Algorithm 1, the drone starts to perform in-situ sensing, when the allowed flight time is $T > 1 8$ min under the flight distance $M = 7$ km. 18 = 7No in-situ sensing is performed when the allowed flight time is shorter than $T = 2 6$ min under $M = 9$ km.

<!-- image-->  
Fig. 8. The normalized in-situ sensing rewards under different flight distances, as the allowed flight time T increases.

<!-- image-->  
Fig. 9. Total energy consumption under different payloads of the drone, as T increases.

= 26 = 9Figs. 9 and 10 evaluate the energy consumption and rewards of the drone under different payloads, with the growth of the allowed flight time T . The requested flight distance is $M =$ =. km. As the payload increases, the power consumption of 7 5the drone also rises. To execute sensing tasks of equal duration, drones with heavier payloads consume significantly more energy than those with lighter loads, leading to a reduced number of sensing tasks performed, as shown in Fig. 10. This effect becomes more pronounced when T shortens. On the one hand, the drone needs to accelerate to reach its destination faster, which demands more energy. The added payload further exacerbates this energy consumption. On the other hand, executing more sensing tasks requires fast flight speeds, which increases energy consumption under heavier payloads.

<!-- image-->  
Fig. 10. The normalized in-situ sensing rewards under different payloads of the drone, as T increases.

Another observation is that when T  minutes and the = 26payload exceeds 3 kg, the energy consumption is higher compared to the cases with $T = 2 4$ minutes. This is because the more relaxed time constraint allows the drone to perform additional sensing tasks, leading to greater energy consumption. Since task execution also takes time, the drone opts for high-speed flight more frequently to compensate, further increasing the overall energy usage.

## C. Case Study

We carry out a case study of the proposed drone control algorithm and the four benchmarks by considering delivery and sensing activities around the campus of the University of Technology Sydney, New South Wales (NSW), Australia. The drone is expected to deliver goods 4.55 km away within 14 min. There are 25 street blocks along the droneâs flight. We assume that the location of a sensing task is randomly selected from the road intersections along the flight path, and the sensing task arrivals follow the Poisson distribution with the average task density $\rho ( \mathcal { L } ^ { ( 1 ) } ) = 0 . 1 6$ . The average duration (of a sensing task is set to $\bar { \tau } _ { s } = 4 8 \mathrm { ~ s ~ }$ 16. The unit reward for the sensing tasks is $\mu = 3 0 0 0 \mathrm { ~ W ~ }$ = 48 per second. The trajectory and = 3000sensing task selections produced by the algorithms are recorded at https://www.youtube.com/watch?v=4VBrOtJESWw, with a screenshot provided in Fig. 11.

In this case study, Algorithm 1 allows the drone to complete delivery within 14 minutes, achieving optimal energy efficiency with a consumption of only 862.15 Wh and the highest possible task rewards. On the other hand, MP-ILP prioritizes speed, with the drone flying at its full speed to reach its destination, performing sensing whenever feasible. This approach secures equivalent rewards to Algorithm 1 but at a much higher energy cost. In contrast, GD-ACO not only prioritizes in-situ sensing at each POI but also opts for a lower flight speed, which ultimately causes delays and prevents timely delivery. SGO-TS and JSP-MIP consume less energy, as both algorithms prefer fewer in-situ sensing tasks, although this leads to lower sensing rewards for the drone.

<!-- image-->  
Fig. 11. The map of the on-campus case study: the required delivery distance $\bar { M } = 4 . 5 5$ km when the specified delay T is 14 min.

## VI. CONCLUDING REMARK

In this paper, we established a new multi-task drone control framework, where the drone can dynamically choose its action from different speeds or in-situ sensing. We reveal the optimal control framework is a monotone deterministic Markovian policy with a simple threshold-based structure of the optimal policy. An optimal switch of the droneâs flight speed or in-situ sensing is only activated when the thresholds concerning the flight distance or time is met. By comparing its state with the thresholds, the drone can decide its action optimally in response to in-situ sensing requests arising. Extensive simulations demonstrated that the proposed algorithm can guarantee the droneâs timely delivery, minimize its energy consumption, and maximize its sensing reward, as validated by comparison with the computationally expensive, DP-based alternative; and substantially reduce the energy consumption of the drone, as compared to existing approaches.

## REFERENCES

[1] D. Cavaliere, V. Loia, A. Saggese, S. Senatore, and M. Vento, âSemantically enhanced UAVs to increase the aerial scene understanding,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 49, no. 3, pp. 555â567, Mar. 2019.

[2] Z. Hu, Z. Bai, Y. Yang, Z. Zheng, K. Bian, and L. Song, âUAV aided aerial-ground IoT for air quality sensing in smart city: Architecture, technologies, and implementation,â IEEE Netw., vol. 33, no. 2, pp. 14â22, Mar./Apr. 2019.

[3] J. Cao et al., âTrajectory optimization and pick-up and delivery sequence design for cellular-connected cargo UAVs,â IEEE Trans. Mobile Comput., vol. 24, no. 3, pp. 1402â1416, Mar. 2025.

[4] D. Saha, D. Pattanayak, and P. S. Mandal, âSurveillance of uneven surface with self-organizing unmanned aerial vehicles,â IEEE Trans. Mobile Comput., vol. 21, no. 4, pp. 1449â1462, Apr. 2022.

[5] A. Albanese, V. Sciancalepore, and X. Costa-PÃ©rez, âSARDO: An automated search-and-rescue drone-based solution for victims localization,â IEEE Trans. Mobile Comput., vol. 21, no. 9, pp. 3312â3325, Sep. 2022.

[6] Z. Sun et al., âMission planning for energy-efficient passive UAV radar imaging system based on substage division collaborative search,â IEEE Trans. Cybern., vol. 53, no. 1, pp. 275â288, Jan. 2023.

[7] B. Liu, W. Ni, R. P. Liu, Y. J. Guo, and H. Zhu, âPrivacy-preserving routing and charging scheduling for cellular-connected unmanned aerial vehicles,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 54, no. 8, pp. 4929â4941, Aug. 2024.

[8] F. Tao and Q. Qi, âNew IT driven service-oriented smart manufacturing: Framework and characteristics,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 49, no. 1, pp. 81â91, Jan. 2019.

[9] H. Sun, C. Peng, D. Yue, Y. L. Wang, and T. Zhang, âResilient load frequency control of cyber-physical power systems under QoS-dependent event-triggered communication,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 51, no. 4, pp. 2113â2122, Apr. 2021.

[10] M. Kishk et al., âAerial base station deployment in 6G cellular networks using tethered drones: The mobility and endurance tradeoff,â IEEE Veh. Technol. Mag., vol. 15, no. 4, pp. 103â111, Dec. 2020.

[11] R. G. Ribeiro, L. P. Cota, T. A. EuzÃ©bio, J. A. RamÃ­rez, and F. G. GuimarÃ£es, âUnmanned-aerial-vehicle routing problem with mobile charging stations for assisting search and rescue missions in postdisaster scenarios,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 52, no. 11, pp. 6682â6696, Nov. 2022.

[12] R. G. Ribeiro, J. R. C. JÃºnior, L. P. Cota, T. A. M. EuzÃ©bio, and F. G. GuimarÃ£es, âUnmanned aerial vehicle location routing problem with charging stations for belt conveyor inspection system in the mining industry,â IEEE Trans. Intell. Transp. Syst., vol. 21, no. 10, pp. 4186â4195, Oct. 2020.

[13] K. Li, W. Ni, and F. Dressler, âContinuous maneuver control and data capture scheduling of autonomous drone in wireless sensor networks,â IEEE Trans. Mobile Comput., vol. 21, no. 8, pp. 2732â2744, Aug. 2022.

[14] Y. Qu et al., âService provisioning for UAV-enabled mobile edge computing,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3287â3305, Nov. 2021.

[15] F. Santoso, M. A. Garratt, and S. G. Anavatti, âHybrid pd-fuzzy and PD controllers for trajectory tracking of a quadrotor unmanned aerial vehicle: Autopilot designs and real-time flight tests,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 51, no. 3, pp. 1817â1829, Mar. 2021.

[16] G. Qi, X. Li, and Z. Chen, âProblems of extended state observer and proposal of compensation function observer for unknown model and application in UAV,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 52, no. 5, pp. 2899â2910, May 2022.

[17] F. Santoso, M. A. Garratt, S. G. Anavatti, and I. Petersen, âRobust hybrid nonlinear control systems for the dynamics of a quadcopter drone,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 50, no. 8, pp. 3059â3071, Aug. 2020.

[18] H. Huang, J. Su, and F.-Y. Wang, âThe potential of lowaltitude airspace: The future of urban air transportation,â IEEE Trans. Intell. Veh., vol. 21, no. 9, pp. 3312â3325, Aug. 2024.

[19] S. K. K. Hari, S. Rathinam, S. Darbha, K. Kalyanam, S. G. Manyam, and D. Casbeer, âOptimal UAV route planning for persistent monitoring missions,â IEEE Trans. Robot., vol. 37, no. 2, pp. 550â566, Apr. 2021.

[20] S. Zhao, X. Wang, Z. Lin, D. Zhang, and L. Shen, âIntegrating vector field approach and input-to-state stability curved path following for unmanned aerial vehicles,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 50, no. 8, pp. 2897â2904, Aug. 2020.

[21] N. Bartolini, A. Coletta, G. Maselli, and A. Khalifeh, âA multi-trip task assignment for early target inspection in squads of aerial drones,â IEEE Trans. Mobile Comput., vol. 20, no. 11, pp. 3099â3116, Nov. 2021.

[22] S. Kim and I. Moon, âTraveling salesman problem with a drone station,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 49, no. 1, pp. 42â52, Jan. 2019.

[23] Y. Liu, Z. Liu, J. Shi, G. Wu, and W. Pedrycz, âTwo-echelon routing problem for parcel delivery by cooperated truck and drone,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 51, no. 12, pp. 7450â7465, Dec. 2021.

[24] C. H. Liu et al., âDistributed and energy-efficient mobile crowdsensing with charging stations by deep reinforcement learning,â IEEE Trans. Mobile Comput., vol. 20, no. 1, pp. 130â146, Jan. 2021.

[25] L. Zhang, A. Celik, S. Dang, and B. Shihada, âEnergy-efficient trajectory optimization for UAV-assisted IoT networks,â IEEE Trans. Mobile Comput., vol. 21, no. 12, pp. 4323â4337, Dec. 2022.

[26] M. Khosravi, S. Enayati, H. Saeedi, and H. Pishro-Nik, âMulti-purpose drones for coverage and transport applications,â IEEE Trans. Wireless Commun., vol. 20, no. 6, pp. 3974â3987, Jun. 2021.

[27] F. Hong, G. Wu, Q. Luo, H. Liu, X. Fang, and W. Pedrycz, âLogistics in the sky: A two-phase optimization approach for the drone package pickup and delivery system,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 9, pp. 9175â9190, Sep. 2023.

[28] J. Li, Y. Xiong, and J. She, âUAV path planning for target coverage task in dynamic environment,â IEEE Internet Things J., vol. 10, no. 20, pp. 17734â17745, Oct. 2023.

[29] M. Y. Arafat and S. Moh, âJRCS: Joint routing and charging strategy for logistics drones,â IEEE Internet Things J., vol. 9, no. 32, pp. 21751â21764, Nov. 2022.

[30] Y. Qin, M. A. Kishk, and M.-S. Alouini, âStochastic-geometry-based analysis of multi-purpose UAVs for package and data delivery,â IEEE Internet Things J., vol. 10, no. 5, pp. 4664â4676, Mar. 2023.

[31] Y. Qin, M. A. Kishk, and M.-S. Alouini, âStochastic geometry-based trajectory design for multi-purpose UAV: Package and data delivery,â IEEE Trans. Veh. Technol., vol. 73, no. 63, pp. 4136â4150, Mar. 2024.

[32] B. Liu, W. Ni, R. P. Liu, Y. J. Guo, and H. Zhu, âDecentralized, privacypreserving routing of cellular-connected unmanned aerial vehicles for joint goods delivery and sensing,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 9, pp. 9627â9641, Sep. 2023.

[33] D. P. Bertsekas, âAffine monotonic and risk-sensitive models in dynamic programming,â IEEE Trans. Autom. Control, vol. 64, no. 8, pp. 3117â3128, Aug. 2019.

[34] B. Liu, W. Ni, R. P. Liu, and H. Zhu, âOptimal selection of heterogeneous network interfaces for high-speed rail communications,â IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 15005â15018, Dec. 2020.

[35] B. Liu, W. Ni, R. P. Liu, Q. Zhu, Y. J. Guo, and H. Zhu, âNovel integrated framework of unmanned aerial vehicle and road traffic for energy-efficient delay-sensitive delivery,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 10692â10707, Aug. 2022.

[36] B. Liu, W. Ni, R. P. Liu, and H. Zhu, âOptimal electric vehicle charging strategies for long-distance driving,â IEEE Trans. Veh. Technol., vol. 73, no. 4, pp. 4949â4960, Apr. 2024.

[37] J. K. Stolaroff, C. Samaras, E. R. OâNeill, A. Lubers, A. S. Mitchell, and D. Ceperley, âEnergy use and life cycle greenhouse gas emissions of drones for commercial package delivery,â Nature Commun., vol. 9, no. 1, pp. 1â13, 2018.

[38] D.-H. Tran et al., âCoarse trajectory design for energy minimization in UAV-enabled wireless communications with latency constraints,â IEEE Trans. Veh. Technol., vol. 69, no. 9, pp. 9483â9496, Sep. 2020.

[39] X. Li et al., âA novel UAV-enabled data collection scheme for intelligent transportation system through UAV speed control,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 4, pp. 2100â2110, Apr. 2021.

[40] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[41] M. L. Puterman, Markov Decision Processes: Discrete Stochastic Dynamic Programming. New York, NY USA: Wiley, 2014.

[42] V. Krishnamurthy, Partially Observed Markov Decision Processes. Cambridge, U.K.: Cambridge Univ. Press, 2016.

[43] D. Liu, S. Xue, B. Zhao, B. Luo, and Q. Wei, âAdaptive dynamic programming for control: A survey and recent advances,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 51, no. 1, pp. 142â160, Jan. 2021.

[44] N. Bauerle and D. Lange, âOptimal control of partially observable piecewise deterministic markov processes,â SIAM J. Control Optim., vol. 56, no. 2, pp. 1441â1462, 2018.

[45] Y. Yang, W. Liu, E. Wang, and J. Wu, âA prediction-based user selection framework for heterogeneous mobile crowdsensing,â IEEE Trans. Mobile Comput., vol. 18, no. 11, pp. 2460â2473, Nov. 2019.

[46] Z. Yu, Y. Zhang, B. Jiang, J. Fu, Y. Jin, and T. Chai, âComposite adaptive disturbance observer-based decentralized fractional-order fault-tolerant control of networked UAVs,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 52, no. 2, pp. 799â813, Feb. 2022.

[47] M. C. P. Santos et al., âA novel null-space-based UAV trajectory tracking controller with collision avoidance,â IEEE/ASME Trans. Mechatron., vol. 22, no. 6, pp. 2543â2553, Dec. 2017.

[48] L. Wang and A. Cavallaro, âA blind source separation framework for egonoise reduction on multi-rotor drones,â IEEE/ACM Trans. Audio, Speech, Lang. Process, vol. 28, pp. 2523â2537, 2020.

[49] DJI, AGRAS MG-1. Accessed: Jun. 2021. [Online]. Available: https:// www.dji.com/be/mg-1

[50] H. Wang, J. Wang, G. Ding, J. Chen, and J. Yang, âCompletion time minimization for turning angle-constrained UAV-to-UAV communications,â IEEE Trans. Veh. Technol., vol. 69, no. 4, pp. 4569â4574, Apr. 2020.

[51] H. Huang, C. Hu, J. Zhu, M. Wu, and R. Malekian, âStochastic task scheduling in UAV-based intelligent on-demand meal delivery system,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 13040â13054, Aug. 2022.

[52] L. Jin, G. Zhang, Y. Wang, and S. Li, âRNN-based quadratic programming scheme for tennis-training robots with flexible capabilities,â IEEE Trans. Syst., Man, Cybern. Syst, vol. 53, no. 2, pp. 838â847, Feb. 2023.

[53] A. M. Rezende, V. M. Goncalves, and L. C. Pimenta, âConstructive timevarying vector fields for robot navigation,â IEEE Trans. Robot., vol. 38, no. 2, pp. 852â867, Apr. 2022.

[54] H. Huang, A. V. Savkin, and W. Ni, âOnline UAV trajectory planning for covert video surveillance of mobile targets,â IEEE Trans. Autom. Sci. Eng., vol. 19, no. 2, pp. 735â746, Apr. 2022.

[55] X. Oh, R. Lim, L. Loh, C. H. Tan, S. Foong, and U.-X. Tan, âMonocular UAV localisation with deep learning and uncertainty propagation,â IEEE Robot. Autom. Lett., vol. 7, no. 3, pp. 7998â8005, Jul. 2022.

[56] H. Huang, A. V. Savkin, and W. Ni, âNavigation of a UAV team for collaborative eavesdropping on multiple ground transmitters,â IEEE Trans. Veh. Technol., vol. 70, no. 10, pp. 10450â10460, Oct. 2021.

<!-- image-->

Bin Liu (Member, IEEE) received the PhD degree in electrical engineering from KU Leuven, Belgium, in 2024. He is a senior researcher with Barkhausen Institut and Technische UniversitÃ¤t Dresden, Germany. He was a research scientist with the Technical University of Darmstadt, Germany, from November 2023 to June 2024. He was a visiting scholar with the Delft University of Technology, the Netherlands, from March to October 2022. He worked as a research assistant with Global Big Data Technologies Centre, University of Technology Sydney, Ultimo, NSW, Australia. from

2017 to 2019. His research interests encompass signal processing in low-altitude intelligent network, massive MIMO, reconfigurable intelligent surfaces, and mmWave communications. He was awarded the Best Paper at the IEEE ICC 2023.

<!-- image-->

Wei Ni (Fellow, IEEE) received the BE and PhD degrees in electronic engineering from Fudan University, Shanghai, China, in 2000 and 2005, respectively. He is a principal research scientist with CSIRO, Sydney, Australia. He is also a conjoint professor with the University of New South Wales, an adjunct professor with the University of Technology Sydney, and an honorary professor with Macquarie University. He also serves as a technical expert with Standards Australia in support of the ISO standardization of AI and Big Data. He was a postdoctoral research

fellow with Shanghai Jiaotong University from 2005 to 2008; deputy project manager with Bell Labs, Alcatel/Alcatel-Lucent from 2005 to 2008; and a senior researcher with Devices R&D, Nokia from 2008 to 2009. He has co-authored one book, ten book chapters, more than 300 journal papers, more than 100 conference papers, 26 patents, ten standard proposals accepted by IEEE, and three technical contributions accepted by ISO. His research interests include 6G security and privacy, machine learning, stochastic optimization, and their applications to system efficiency and integrity. He has been an editor for IEEE Transactions on Wireless Communications since 2018, an editor for IEEE Transactions on Vehicular Technology since 2022, and an editor for IEEE Transactions on Information Forensics and Security and IEEE Communications Surveys and Tutorials since 2024. He served first as the secretary, then the vice-chair and chair of the IEEE VTS NSW Chapter from 2015 to 2022, track chair for VTC-Spring 2017, track co-chair for IEEE VTC-Spring 2016, publication chair for BodyNet 2015, and student travel grant chair for WPMC 2014.

<!-- image-->

Ren Ping Liu (Senior Member, IEEE) received the BE degree from the Beijing University of Posts and Telecommunications, China, and the PhD degree from the University of Newcastle, Australia, in 1985 and 1996, respectively. He is a professor and head of Discipline of Network & Cybersecurity with the University of Technology Sydney (UTS). As a research leader, a certified network professional, and a full stack web developer, he has delivered networking and cybersecurity solutions to government agencies and industry customers. His research interests in-

clude wireless networking, 5G, IoT, vehicular networks, 6G, cybersecurity, and blockchain. He has supervised more than 30 PhD students, and has more than 200 research publications. He was the winner of NSW iAwards 2020 for leading the BeFAQT (Blockchain enabled Fish provenance And Quality Tracking) project. He was awarded the Australian Engineering Innovation Award 2012 and CSIRO Chairmanâs medal for his contribution in the Wireless Backhaul project. He was the founding chair of IEEE NSW VTS Chapter.

<!-- image-->

Y. Jay Guo (Fellow, IEEE) received the PhD degree from Xiâan Jiaotong University, Xiâan, China, in 1987. He is a distinguished professor and the funding director of Global Big Data Technologies Centre, University of Technology Sydney, Ultimo, NSW, Australia. He is the founding technical director of the New South Wales (NSW) Connectivity Innovation Network (CIN). His research interests include antennas, mm-wave and THz communications and sensing systems, and Big Data technologies. He is a fellow of the Australian Academy of Engineering and

Technology. He has won a number of the most prestigious Australian national awards including the Australian Engineering Excellence Awards in 2007, 2012, and CSIRO Chairmanâs Medal in 2007, 2012. He was named one of the top researchers across all fields, Australia, in 2020, 2021, and 2022, respectively.

<!-- image-->

Hongbo Zhu (Member, IEEE) received the BS degree in communications engineering from the Nanjing University of Posts and Telecommunications, Nanjing, China, and the PhD degree in information and communications engineering from the Beijing University of Posts and Telecommunications, Beijing, China, in 1982 and 1996, respectively. He is presently a professor and vice-president with the Nanjing University of Posts and Telecommunications, Nanjing, China. He is also the head of the Coordination Innovative Center of IoT Technology and

Application (Jiangsu), which is the first governmental authorized Coordination Innovative Center of IoT in China. He also serves as a referee or expert in multiple national organizations and committees.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Liu-2025-Delay-Sensitive Goods Delivery and In/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Liu-2025-Delay-Sensitive Goods Delivery and In/page_10_img_1.png|page_10_img_1]]
3. [[../extracted_images/Liu-2025-Delay-Sensitive Goods Delivery and In/page_12_img_1.jpeg|page_12_img_1]]
4. [[../extracted_images/Liu-2025-Delay-Sensitive Goods Delivery and In/page_14_img_1.jpeg|page_14_img_1]]
5. [[../extracted_images/Liu-2025-Delay-Sensitive Goods Delivery and In/page_14_img_2.jpeg|page_14_img_2]]
6. [[../extracted_images/Liu-2025-Delay-Sensitive Goods Delivery and In/page_14_img_3.jpeg|page_14_img_3]]
7. [[../extracted_images/Liu-2025-Delay-Sensitive Goods Delivery and In/page_14_img_4.jpeg|page_14_img_4]]
8. [[../extracted_images/Liu-2025-Delay-Sensitive Goods Delivery and In/page_14_img_5.jpeg|page_14_img_5]]

---

