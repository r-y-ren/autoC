# Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks: A Multi-Agent Deep Reinforcement Learning Approach

Muhammad Morshed Alam and Sangman Moh , Member, IEEE

AbstractâCollaborative unmanned aerial vehicle (UAV) swarm networks can effectively execute various emerging missions such as surveillance and communication coverage. However, due to high mobility and constrained transmission range, packet routing encounters mutual interferences, link breakages, and unexpected delays. In such networks, routing performance is coupled with trajectory control, frequency allocation, and relay selection. In this study, we propose a joint trajectory control, frequency allocation, and packet routing (JTFR) algorithm, in which link utility is maximized by considering the link stability, signal-to-interference-plus-noise ratio, queuing delay, and residual energy of UAVs. The proposed JTFR employs adaptive distributed multi-agent deep deterministic policy gradient coupled with the swarming behavior to obtain the optimal solution. For each UAV, an actor network is established by utilizing a long short-term memory-based state representation layer containing two-hop neighbor information to adopt the dynamic time-varying topology. Subsequently, a scalable multi-head attentional critic network is set up to adaptively adjust the actor network policy of each UAV by collaborating with neighbors. The extensive simulation results show that JTFR outperforms existing routing protocols by 30â60% less end-to-end delay, 15â32% better packet delivery ratio, and 20â46% less energy consumption.

Index TermsâMulti-agent deep deterministic policy gradient, frequency allocation, routing, trajectory control, UAV swarm network.

## I. INTRODUCTION

C OLLABORATIVE unmanned aerial vehicle (UAV)swarm networks (UAVSNs) have the capability to conduct ï¼swarm networks (UAVSNs) have the capability to conduct the real-time monitoring of post-disaster areas and to deliver on-demand communication and computation services [1], [2]. In general, UAVSNs require collaborative trajectory control to maximize coverage and ensure the quality of services (QoS) [3], [4]. Since UAVs have limited transmission power, data packet transmission from remote UAVs to base station (BS) requires a multi-hop path that involves a series of relay UAVs. However, due to the highly dynamic topology and limited energy, packet routing from UAVs to the BS suffers frequent link breakages, higher delays, routing loops, and energy holes. Although the line-of-sight (LOS) access in UAV-to-UAV link ensures communication quality, its exposure during simultaneous transmission generates strong mutual interferences. Consequently, the performance of routing depends on multiple link quality metrics such as signal-to-interference-plus-noise ratio (SINR), relative trajectory knowledge, queuing delay, and residual energy (RE) of a relaying UAV [2], [5], [6].

To achieve high SINR, trajectory control according to physical layer transmission range and frequency resource allocation in the medium access control (MAC) layer are prerequisites [6], [7], [8]. Additionally, link duration (LD) can be utilized to alleviate the effect of the highly time-varying topology [2], [9]. The LD offers a predictable time at which two adjacent UAVs remain within their communication range. In UAVSNs, the UAVs are required to periodically adjust their mobility not only based on its own previous mobility but also based on the mobility of nearby UAVs to maintain stable LD. UAVSN topology should be selfhealing to retrieve the connectivity with remaining UAVs in the case of UAV failure or departure due to energy depletion.

To overcome the above challenges, researchers have attempted to integrate the behavior of swarm intelligence, such as bird flocks or fish schools, to design self-organized, selfhealing, and distributed collaborative trajectories [7], [10], [11]. UAVSNs can maintain a robust topology by generating collective motion according to the Reynolds motion model [9]. The trajectory control of UAVs based on their physical layer transmission range inspired by behavior-based motion can obtain the optimal aerial node density [2]. It guarantees aerial coverage and safe flight distance between UAVs. Moreover, it can effectively minimize mutual interference. Although a higher node density enhances connectivity, it simultaneously intensifies mutual interference and contention among neighboring UAVs to access the shared medium. Consequently, the optimal allocation of frequency resources in the MAC layer can significantly reduce the mutual interferences [5], [6]. Thus, in this study, a joint trajectory control, frequency allocation, and packet routing (JTFR) algorithm is proposed by leveraging the cross-layer design.

Nevertheless, behavior-based motion obtains mobility at the next timeslot based on the mobility at the current timeslot. The uncertainties in communication can cause UAVs to compute the motion component using the outdated mobility information of neighboring UAVs. The historical information of the UAV trajectory generated by the motion model can be utilized to precisely predict the mobility of the UAV. Subsequently, allocating the frequency blocks according to the historical frequency state of each UAV and its neighboring UAVs can result in selecting a better frequency state to avoid mutual interference. Consequently, based on the historical information, UAVs can select a better next hop to relay a packet toward the BS.

Recently, reinforcement learning (RL) has been widely used for designing the trajectory of UAVs [12], allocating resources, and selecting relay UAVs for packet routing [5], [13] owing to the adaptability to dynamic environment. Data-driven deep reinforcement learning (DRL) can efficiently solve sequential decision-making problems by adopting the Markov decision process (MDP). Q-learning (QL) and deep Q-network (DQN) can only handle low-dimensional discrete action spaces [14]. Therefore, actor-critic learning is introduced to obtain the optimal policy for both continuous and discrete actions by converting discrete action to continuous action probability distribution using softmax activation [15], [16], [17]. An off-policy actor-critic framework based on the deep deterministic policy gradient (DDPG) can efficiently deal with the large state and action space [13], [18]. However, the single-agent DDPG attempts to independently maximize its own reward without considering the influence of neighboring agents. Thus, the environment appears non-stationary from the perception of any individual agent [19]. Fortunately, the extension of a single-agent DDPG to multiagent DDPG (MA-DDPG) can solve the problems by adopting centralized training and distributed execution [20], [21]. However, collecting the global information of large-scale UAVSNs in a centralized server increases computational complexity. Conversely, distributed cooperative training can overcome such challenges. However, only considering the observation from the one-hop neighboring agent may trap in local optima [2], [22].

Collaborative UAVSNs are similar to a multi-agent system, where each UAV acts as a learning agent. Here, actions taken by the neighboring agent significantly impact the reward of a particular agent. For instance, if two neighboring UAVs select the same frequency band, it generates mutual interference. Similarly, if most neighboring UAVs select the same UAV to relay data packets, it can create network congestion. If the neighboring UAVs randomly choose velocity and flying direction, the LD may be reduced significantly, which results in link breakages. In JTFR, the decision-making for each UAV to control the trajectory, select the frequency band, and select the relay UAV is highly coupled with the neighboring UAVs. Thus, distributed MA-DDPG (DMA-DDPG) is envisioned as the best option to efficiently solve this cooperative sequential decision-making problem.

In MA-DDPG, the actor-network solely depending on the fully connected layer (FCL) cannot deal with time-series data. In JTFR, historical information needs to be exploited to make a sequential decision. Fortunately, recurrent neural networks, such as the long short-term memory (LSTM)-based actor-network, can store historical sequential information and utilize the information to predict the more precise state in the next timeslot by mining the temporal relationship [23]. The critic network using only the FCL, or even LSTM cannot estimate the value function to adaptively adjust its actor action policy by prioritizing its neighbors. Thus, to overcome these challenges, a multi-head attention mechanism is utilized for each agent critic network to adaptively pay attention to its neighbors by generating attention weights using dot product similarity of their state-action features. The adaptive adjustment of each agent policy according to changes in the neighboring agent policy helps to avoid environmental non-stationarity. Moreover, multi-head attention introduces parallelization in the critic value-function estimation, which delivers faster convergence.

The major contributions of this study are as follows:

- We propose JTFR by formulating a link utility maximization problem for UAVSNs to route data packets toward BS by jointly considering UAV trajectory control, frequency resource allocation, and relay UAV selection. The link utility contains a link stability metric defined by predictive three-dimensional (3D) maximum-minimum LD, link SINR, queuing delay, and relay UAV RE level under several key constraints. Solving the problem poses a significant challenge because of the large action spaces, which are interconnected in both the objective function and the dynamic constraints.

- The adaptive DMA-DDPG-based algorithm coupled with swarming behavior is proposed to obtain the optimal link utility. To adopt the dynamic topology and avoid local optima, the MDP observation state at each UAV comprises both one-hop and two-hop neighborsâ dynamic state. Each UAV actor network is represented by three LSTM-based state representation layers (SRLs) and an FCL. The key state parameters of UAVSNs are embedded into the LSTMbased SRLs to introduce better state representation to the actor FCL, which is for obtaining optimal action policy by extracting the temporal continuity in the historical states of the time-varying topology.

- A multi-head attentional critic network is designed for each UAV to adaptively adjust its actor network policy in a multi-agent dynamic environment. It precisely estimates the value function for the action taken by the actor network by selectively assigning attention weights only to its neighboring agents according to the influence of their state-action spaces. Hence, it delivers better scalability, learning stability, and accelerates convergence for optimal decision-making.

Extensive simulation shows that the proposed DMA-DDPG-based JTFR outperforms existing routing protocols in terms of traveling distance fairness, packet delivery ratio, average end-to-end delay, and energy consumption.

The remainder of this paper is organized as follows. Section II presents a literature review. In Section III, the system model of this study is provided along with channel, delay, energy model, problem formulation, and motion model. In Section IV, the formulated link utility maximization problem is solved by employing DMA-DDPG based JTFR framework. Based on the extensive simulations, a rigorous comparison study with existing baseline protocols is given in Section V. Finally, this paper is concluded in Section VI.

## II. RELATED WORKS

The literature review is divided into two subsections. First, the joint optimizations of trajectory control and communication resource allocation are reviewed. Subsequently, existing routing protocols are reviewed. Our investigation is addressed with an emphasis on the gap between our work and the existing ones.

## A. Joint Optimization of Trajectory Control and Communication Resource Allocation

Extensive researches have been conducted to perform the joint optimization of trajectory control and communication resource allocation in UAVSNs. In [6], [8], mean field game theory was utilized to minimize mutual interference by controlling physical layer transmission power according to the relative trajectory of UAVs, and allocating MAC layer timeslot [8] or frequency resources between UAVs [6]. However, it requires to solve two partial differential equations simultaneously. In [5], a multi-agent deep Q-mixing network was utilized to minimize transmission delay in a multi-hop packet routing problem by jointly considering the trajectory design, frequency band allocation, and next-hop selection. However, the Q-mixing network estimates the global Q-value for the actions taken, without taking into account the extent of influence from nearby agentsâ actions [24]. In [25], the authors employed distributed deep recurrent graph attention network to jointly optimize coverage fairness and energy consumption by controlling UAV movement in two-dimensional (2D) discrete action space. The designed graph attentional recurrent neural network can capture key hidden features of ground user distribution and dynamic UAVSN topology up to two-hop neighbors for making optimal flight decisions. All of these algorithms discretize UAV movement to simplify the action space, whereas realistic trajectory control of UAVs should be continuous [26].

In [12], the single-agent DDPG optimizes network throughput while ensuring service fairness by jointly considering the 3D trajectory optimization of a single UAV in a continuous action space and the allocation of frequency bands in a discrete action space. In [27], the authors employed independent proximal policy optimization to optimize UAVâs energy consumption and to achieve queue stability by controlling the task offloading ratio and the trajectory of UAVs. In [16], the decentralized MA-DDPG was employed to optimize the energy consumption of UAVs and ground devices by controlling UAVâs 2D continuous trajectory. In [24], the authors investigated quasi-distributed actor-critic Q-mixing network and attentional critic network-based MA-DDPG to maximize communication capacity by jointly controlling bandwidth allocation and 2D trajectory of UAVs. Simulation results in [23] show that attentional critic network-based MA-DDPG provides better learning stability.

## B. Routing Protocols in UAVSNs

Existing routing protocols can be classified as topologybased and position-based forwarding techniques [28], [29]. The topology-based routing protocols are categorized as proactive, reactive, and hybrid. Table-driven proactive routing protocols such as optimized link state routing (OLSR) has slow response to time-varying topology, thus it encounters higher link breakage, latency, overhead, and routing loop. Reactive routing protocols such as dynamic source routing (DSR) and ad hoc on-demand distance vector routing encounters higher delay, overhead, and link breakage due to on-demand route discovery. Additionally, these routing protocols trace the shortest path, which can trigger energy holes and network congestion.

In [9], the path stability metric defined by the LD was first introduced to overcome the link breakages and trade-off between topology prediction accuracy and control overhead by adaptively maintaining the hello interval in OLSR. However, the uncertainty in UAV communications caused by delay and limited energy are not considered. Li et al. [6] proposed a routing protocol for UAVSNs by leveraging the cross-layer design and introducing a link quality metric in DSR jointly considering link SINR, relative velocity, and queuing delay. However, reactive DSR produces a large overhead and delay because of the proportional increase in the routing discovery header along with a long path. Grag et al. [30] proposed mobility and congestion aware OLSR (MCA-OLSR) for UAV networks by leveraging a cross layer design. In MCA-OLSR, each UAV makes a routing decision based on multiple link quality metrics, such as LD, hop count, delay, and number of interfacing links. Owing to priority-aware packet queue management and multi-metric routing decision, MCA-OLSR outperforms existing OLSR protocols.

Wang et al. [31] proposed a low complexity two-hop connected dominating set (CDS)-based topology management for UAVSNs by adopting a Boids flocking-based mobility model. In [32], a CDS-based dynamic topology management was proposed to maximize the throughput by jointly optimizing transmission power, CDS number, and UAV position using particle swarm optimization (PSO). In [33], joint single-shot localization, clustering, and multi-hop routing techniques were proposed using a bounding box and PSO. However, these types of CDS and cluster-based dynamic topology management require frequent topology construction and management, which triggers a higher overhead [34]. Moreover, all these methods assume MAC layer resources (i.e., timeslots or frequency) are allocated optimally to prevent interference.

Position-based routing can be categorized as single-path and multi-path forwarding [29], [35]. Single-path forwarding includes greedy forwarding, most forwarding, and compass forwarding [35]. These single-path forwarding strategies are only based on distance progress, and they face higher link breakages, network congestion, and loops. Multi-path forwarding strategies broadcast a similar copy of data packets in deterministic or randomized directions, which produces an extremely higher overhead [35]. To mitigate these challenges in position-based forwarding, researchers have been incorporating RL and DRL to perform multi-objective optimization. In [36], the queuing theory was applied to perform neighbor discovery and adaptively adjust the hello interval to adopt the dynamic topology. Subsequently, they utilized QL to trace the optimal path for UAV communication in terms of the minimal delay and communication energy consumption. In [37], adaptive QL is applied to minimize delay and UAV communication energy consumption by using two-hop information. By using the extended knowledge about dynamic topology, each UAV iteratively obtains the optimal paths.

Zang et al. [38] proposed a centralized data-driven adaptive routing protocol for UAV communications, where a weighted link quality metric is defined by considering the inter-UAV distance, packet arrival rate, queue backlog length, and the number of hops. To avoid network congestion, they predicted the packet arrival at each UAV by leveraging the LSTM. Nevertheless, mobility prediction solely based on the inter-UAV distance in a centralized server may not provide an optimal solution. In [22], an extended MDP formulation was proposed by considering the state of both the current node and its one-hop neighbor, to select a relay UAV for minimizing delay. Owing to the large state space and discrete next-hop selection action space, they adopted DQN to make a routing decision. In [39], adaptive hello interval adjustment techniques were proposed using DQN to improve the link reliability.

Qiu et al. [40] applied MA-DDPG-LSTM to make routing decisions by considering link SINR, LD, and queuing delay together, which involves adopting centralized training and distributed execution. To cope with the dynamic topology, they considered the LSTM-based actor and critic network. However, trajectory control according to the physical layer transmission range was not considered, and they assumed that frequency resources are allocated optimally in the MAC layer. In a multiagent scenario, critic network solely based on LSTM cannot provide adaptive attention to the neighborsâ policy and LSTM does not support parallelization in the critic value function computation, which can trigger slow convergence and unstable training. Moreover, in the fully centralized training, the stateaction dimensionality in centralized critic network becomes excessively large with increasing number of UAVs, which can cause higher computational complexity and less scalability.

All of the above-mentioned routing protocols consider generic mobility models such as random waypoint and Gauss-Markov. Such mobility models cannot adopt the properties of UAVSNs and their aerodynamics [7]. Moreover, all RL/DRL-based algorithms control the UAV trajectory by defining UAV movements in the discrete or continuous action space without synchronizing the mobility with neighboring UAVs [5], [41]. Such trajectory control cannot provide realistic trajectory because of the chaotic movement.

In UAVSNs, the swarming behavior-based mobility models can autonomously maintain optimal node density, coverage, connectivity, stable LD, and inter-UAV collision avoidance [2], [11]. Therefore, we utilized swarming behavior coupling adaptive DMA-DDPG with two-hop neighbor information to control UAV trajectory in continuous action space, allocate frequency resources, and select relay UAVs. Here, to generate a realistic trajectory, a behavior-based motion model is applied under the sensor noise and wind disturbance. Subsequently, the key observed state of the dynamic UAVSNs such as the motion rules generated by the relative mobility, link SINR, frequency state, queue backlog size, and LD up to two-hop neighbors are fed into the actor LSTM-based SRL. LSTM-based SRL forwards a better state to the actor FCL by mining temporal correlations between the current state and a finite amount of the previous state. Moreover, a multi-head attentional critic network is utilized to generate action value function and adaptively adjust the actor policy by paying attention only to its one-hop neighbors. The normalized attention weights guide each agent to which neighbor it should pay more attention.

<!-- image-->  
Fig. 1. An example of UAV swarm networks.

## III. SYSTEM MODEL

We consider $\mathcal { U } = \{ 1 , 2 , \cdots , u \}$ as a set of quad ro-= 1 2tor UAVs having global positioning system (GPS), inertial measurement unit, camera, and wireless interface. They are deployed to execute surveillance mission over a threedimensional (3D) post-disaster mission area, as shown in Fig. 1. The dimension of the 3D mission area is bounded by $( x _ { \mathrm { m i n } } \le x \le x _ { \mathrm { m a x } } , \ y _ { \mathrm { m i n } } \le y \le y _ { \mathrm { m a x } } , z _ { \mathrm { m i n } } \le z \le z _ { \mathrm { m a x } } )$ . To (track the mission, the overall surveillance time $\mathcal { T }$ )is divided into t equal timeslots represented as $\mathcal { T } = \{ 1 , 2 , \cdots , t \}$ , where = 1 2the length of each t is adequately small denoted as $\delta _ { t }$ . Hence, UAVSNs topology can be expressed as a time-dependent undirected graph $\mathcal { G } ( t ) = ( \mathcal { V } ( t ) , \mathcal { E } ( t ) )$ , where ${ \mathcal { V } } ( t ) \in \{ { \mathcal { U } } ( t ) \cup { \mathrm { B S } } \}$ ( ) = ( ( ) ( )) ( ) ( )represents the vertex set comprising the active UAV set $\mathcal { U } ( t )$ ( )and a location-fixed BS. An emergency response vehicle acts as the BS, which can function as a mission control center and edge server. Each $\mathrm { U A V } u _ { i }$ can localize its position $\vec { p _ { i } } ( t ) = ( x _ { i } , y _ { i } , z _ { i } )$ by using GPS and being aware of the position of the ${ \mathrm { B S } } , \vec { p _ { \mathrm { B S } } } .$

The communication range of each UAV is separated into two regions: the repulsion range $R _ { r }$ and attraction range $A _ { r } .$ Therefore, to satisfy the safe distance and communication range constraints, the distance between two neighboring $\operatorname { U A V s } d _ { i j } ( t )$ must be retained within $R _ { r } \leq d _ { i j } ( t ) \leq A _ { r } . \mathrm { ~ I f ~ } d _ { i j } ( t ) \leq \dot { A _ { r } } ,$ a direct edge $\mathcal { E } ( t )$ between two neighboring UAVs is considered. ( )Consequently, the source UAV ui selects a series of relay UAV represented as $( u _ { j } , u _ { k } \cdot \cdot \cdot , \mathbf { B S } )$ to transmit packets toward BS, as illustrated in Fig. 1.

Notations: $\| \bullet \| _ { 2 }$ represents the Euclidean norm, $\| \bullet \|$ represents the absolute value, and $| \bullet |$ represents the cardinality of a set.

## A. Channel Model

Owing to the high altitude and 3D mobility adjustment, the UAV-to-UAV links and UAV-to-BS links are dominated by LOS links. Thus, the channel gain between two $\mathrm { U A V s } \ ( u _ { i } , u _ { j } )$ in free-space path can be stated as $g _ { i j } ( t ) = \rho _ { 0 } d _ { i j } ( t ) ^ { - \alpha }$ , where $\rho _ { 0 }$ ( ) = ( )denotes the LOS channel gain within a reference distance of $m ,$ and Î± represents the path-loss exponent. For a given transmit power $P _ { i } ^ { \mathrm { t x } }$ from $\mathrm { U A V } ~ u _ { i }$ , the received power at UAV $u _ { j }$ can be expressed as $P _ { i j } ^ { \mathrm { r x } } ( t ) = P _ { i } ^ { \mathrm { t x } } ( t ) g _ { i j } ( t )$

( ) = ( ) ( )The network bandwidth divided into $f _ { K }$ orthogonal frequency bands can be denoted as $f = \left( f _ { 1 } , f _ { 2 } , \cdot \cdot \cdot , f _ { K } \right)$ . The bandwidth of each frequency band $f _ { K }$ = ( )is equal and denoted by $B .$ Each UAV selects a relay UAV and transmits a packet from its queue buffer by following the first in first out approach by choosing a transmission frequency band $f _ { K }$ . The index of the frequency band selected by UAV $u _ { i }$ is represented as $f _ { K , i } ( t )$ . If a UAV $u _ { i }$ selects frequency band $f _ { K }$ ( )to transmit a packet to UAV $u _ { j }$ at time $t ,$ then the corresponding binary channel association $\phi _ { f _ { K , i } } ( t ) = 1$ ; otherwise, $\phi _ { f _ { K , i } } ( t ) = 0$ ( ) = 1. Since UAVs share the frequency band $f _ { K }$ ( ) = 0during simultaneous transmission, the interference from the neighboring UAV $u _ { \mathscr { k } } \left( \mathscr { k } \neq i , j \right)$ to UAV $u _ { j }$ over the frequency band $f _ { K }$ can be expressed as

$$
I _ { \mathcal { k } j } ^ { f _ { K } } \left( t \right) = \sum _ { \mathcal { k } \neq i , j } \phi _ { f _ { K , \mathcal { k } } } \left( t \right) P _ { \mathcal { k } j } ^ { \mathrm { t x } } \left( t \right) \rho _ { 0 } d _ { \mathcal { k } j } ( t ) ^ { - \alpha } ,\tag{1}
$$

where $[ \phi _ { f _ { K , \hbar } } ( t ) ]$ represents an ${ \mathcal { U } } _ { \mathscr { k } } ( t ) \times K$ binary frequency [ ( )]band paring matrix. Here, $\mathcal { U } _ { \hbar } ( t ) = [ u _ { 1 } , u _ { 2 } , \cdot \cdot \cdot , u _ { \ell } ]$ represents ( ) = [ ]the set of active UAVs within the one and two-hop neighborhood of UAV $u _ { i }$ that performs simultaneous transmissions at time t. The SINR $\gamma _ { i j } ( t )$ at UAV $u _ { j }$ can be obtained as

$$
\gamma _ { i j } \left( t \right) = 1 0 \log \frac { P _ { i j } ^ { \mathrm { r x } } \left( t \right) } { I _ { \mathscr { k } j } ^ { f _ { K } } \left( t \right) + \sigma ^ { 2 } \left( t \right) } ,\tag{2}
$$

where $\sigma ^ { 2 } ( t )$ represents additive white Gaussian noise power. ( )UAV-to-UAV links can be established successfully if $\gamma _ { i j } ( \mathrm { t } ) \geq$ $\gamma _ { \mathrm { t h } } ,$ where $\gamma _ { \mathrm { t h } }$ (t)represents SINR threshold. Thus, the maximum communication range for UAV $u _ { i }$ to communicate with UAV $u _ { j }$ is $\begin{array} { r } { d _ { i j } ( t ) \leq d _ { i j } ^ { \mathrm { t h } } = \bigg [ \frac { \rho _ { o } P _ { i } ^ { \mathrm { t x } } ( t ) } { ( I _ { \mathbb { A } ^ { j } } ^ { f _ { K } } ( t ) + \sigma ^ { 2 } ( t ) ) 1 0 ^ { \frac { \gamma _ { \mathrm { t h } } } { 1 0 } } } \bigg ] ^ { 1 / \alpha } } \end{array}$ . For each UAV with an omnidirectional antenna, the attainable communication range can be represented as a sphere with radius $A _ { a } = d _ { i j } ^ { \mathrm { t h } }$ . The data transmission rate between two UAVs $C _ { i j } ( t )$ =is estimated as $C _ { i j } ( t ) = B \mathrm { l o g } _ { 2 } [ 1 + \gamma _ { i j } ( t ) ]$

## B. Delay Model

For each UAV $u _ { i }$ the queue backlog size $q _ { i } ( t + 1 )$ is represented as follows:

$$
q _ { i } \left( t + 1 \right) = \operatorname* { m i n } \left[ \left[ q _ { i } \left( t \right) - D _ { i } \left( t \right) \right] + A _ { i } \left( t \right) , q _ { \operatorname* { m a x } } \right] ,\tag{3}
$$

where $\begin{array} { r } { D _ { i } ( t ) = C _ { i j } ( t ) \delta _ { t } } \end{array}$ represents the amount of packets that ( ) = ( )were successfully transmitted from the queue buffer to the next relay UAV. $A _ { i } ( t )$ represents the process of new packet arrival ( )in the queue at timeslot t and $q _ { \mathrm { m a x } }$ represents the maximum queue buffer size. Each source UAV $u _ { i }$ prefers the next relay UAV $u _ { j }$ having a small queue backlog size $q _ { j }$ given by (3) to avoid long queuing delay and network congestion. Considering a sufficiently large queue buffer size, we adopt M/M/1 queuing, where $A _ { i }$ obeys the Poisson process. Thus, the average waiting time of each packet in the queue can be approximated as $t _ { q } = \sp 1 / ( D _ { i } - A _ { i } )$ [2], [30]. Finally, the total time required to ( )successfully reach the next relay UAV can be approximated as

$$
t _ { d } = t _ { q } + \frac { P _ { \mathrm { s i z e } } } { C _ { i j } \left( t \right) } ,\tag{4}
$$

where $P _ { \mathrm { s i z e } }$ denotes the size of a packet.

## C. Energy Model

UAV energy consumption has two key portions: propulsion and communication energy consumption. The propulsion energy consumption is considerably higher than the communication energy. The propulsion power $\mathrm { P P } _ { i }$ of UAV $u _ { i }$ generates thrust PPto fly in the air by overcoming drag forces and gravity. Thus, $\mathrm { P P } _ { i }$ is a function of velocity $\vec { v } _ { i }$ of each UAV and proportional to PPthe distance traveled by each UAV. The $\mathrm { P P } _ { i }$ for quadrotor UAVs are obtained according to [42] as follows:

$$
\begin{array} { r l r } { \mathrm { P P } _ { i } \left( \vec { v } _ { i } \left( t \right) , t \right) = P _ { \mathrm { b f } } \left( 1 + \frac { 3 \| \vec { v } _ { i } \left( t \right) \| ^ { 3 } } { U _ { \mathrm { t p } } ^ { 2 } } \right) } & { } & \\ { + P _ { \mathrm { i n } } \left( \sqrt { \left( 1 + \frac { \| \vec { v } _ { i } \left( t \right) \| ^ { 4 } } { 4 v _ { o } ^ { 4 } } \right) } - \frac { \| \vec { v } _ { i } \left( t \right) \| ^ { 2 } } { 2 v _ { o } ^ { 2 } } \right) ^ { 1 / 2 } } & { } & \\ { + \frac { 1 } { 2 } d _ { 0 } \sigma s A \| \vec { v } _ { i } \left( t \right) \| ^ { 3 } , } & { } & { { \displaystyle ( 5 ) } } \end{array}
$$

where $P _ { \mathrm { b f } }$ and $P _ { \mathrm { i n } }$ represent the blade profile and induced power in the hovering state, respectively, and $U _ { \mathrm { t i p } }$ and $v _ { o }$ denotes the tip speed of the rotor blade and the mean rotor induced velocity in the hovering state, respectively. Additionally, $d _ { o } , \sigma , s .$ and A represent the fuselage drag ratio, air density, rotor solidity, and rotor disk area, respectively. The communication energy consumption depends on the transmitted packet size $P _ { \mathrm { s i z e } }$ at each timeslot. The transmitting energy $E _ { i } ^ { \mathrm { t x } }$ can be computed as $E _ { i } ^ { \mathrm { t x } } =$ $\frac { n P _ { i } ^ { \mathrm { t x } } P _ { \mathrm { s i z e } } } { C _ { i j } ( t ) }$ , where n denotes the number of retransmissions. For a given maximum energy level $E _ { \mathrm { m a x } }$ , the RE level $E _ { i } ( t + 1 )$ of ( +each UAV at the next timeslot can be tracked as follows:

$$
 { E _ { i } } \left( t + 1 \right) =  { E _ { \mathrm { m a x } } } - \sum _ { t } \left[ \left\{  { \mathrm { P P } } _ { i } \left( t \right) \delta _ { t } +  { E _ { i } ^ { \mathrm { t x } } } \left( t \right) \right\} \right]\tag{6}
$$

When the $E _ { i } ( t + 1 )$ is less than the threshold $E _ { \mathrm { t h } }$ , UAV can ( + 1)return to BS for battery replacement.

## D. Problem Formulation

Owing to the limited communication range, the source UAV $u _ { i }$ selects a series of relay UAVs to relay the data packet toward the BS. Hence, the end-to-end path becomes $( { u _ { i } } , { u _ { j } } , { u _ { k } } \cdot \cdot \cdot , { \bf B } { \bf S } )$ , which comprises m hops. To avoid the detour and network congestion, each UAV $u _ { i }$ explores relay

UAV $u _ { j } \in N _ { i } ^ { 1 } ( t )$ in the direction of Euclidean distance progress toward BS $\Delta _ { i j } = [ \| \vec { p _ { i } } - \vec { p _ { \mathrm { B S } } } \| _ { 2 } - \| \vec { p _ { j } } - \vec { p _ { \mathrm { B S } } } \| _ { 2 } ] > 0$ and queue Î = [backlog difference $( q _ { i } - q _ { j } ) > 0$ , where $i \neq j$ 0. Additionally, ( ) 0during forwarding, the link utility $\mathrm { L U } _ { i j }$ given in (7) is main-LUtained, which jointly considers LD (to avoid link breakage), link SINR (to achieve highest data rate), small queue backlog size (to minimize delay), and the highest RE level of relaying UAV (to avoid energy holes). Notably, each term in $\mathrm { L U } _ { i j } ( t )$ is normalized LU ( )by utilizing the corresponding maximum value found within the neighbor information.

$$
\mathrm { L U } _ { i j } \left( t \right) = a \frac { \mathrm { L D } _ { i j } } { \mathrm { m a x } \mathrm { L D } _ { i j } } + b \frac { \gamma _ { i j } } { \mathrm { m a x } \gamma _ { i j } } + c e ^ { - q _ { j } } + d \frac { E _ { j } } { E _ { \mathrm { m a x } } } ,\tag{7}
$$

where $a , b , c ,$ and d represent the weight of each link quality metric and $a + b + c + d = 1$ .The $\mathrm { L U } _ { i j }$ maximization problem + + + = 1 LUin the end-to-end path is represented as

$$
\operatorname* { m a x } \sum _ { j = 0 } ^ { m - 1 } \mathrm { L U } _ { i j } ,\tag{8}
$$

Subject to the following constraints:

$$
R _ { r } \leq d _ { i j } \left( t \right) \leq A _ { r } ,\tag{8A}
$$

$$
\operatorname* { m i n } \mathrm { L D } _ { i j } > t _ { d } ,\tag{8B}
$$

$$
- a _ { \mathrm { m a x } } \leq \left. \vec { a } _ { i } \left( t \right) \right. \leq a _ { \mathrm { m a x } } ,\tag{8C}
$$

$$
\| \vec { v } _ { i } \left( t \right) \| \le v _ { \operatorname* { m a x } } ,\tag{8D}
$$

$$
x _ { \operatorname* { m i n } } \le x \le x _ { \operatorname* { m a x } } , \ y _ { \operatorname* { m i n } } \le y \le y _ { \operatorname* { m a x } } , z _ { \operatorname* { m i n } } \le z \le z _ { \operatorname* { m a x } }\tag{8E}
$$

$$
f = \left( f _ { 1 } , f _ { 2 } , \cdot \cdot \cdot , f _ { K } \right) ,\tag{8F}
$$

$$
\gamma _ { i j } \geq \gamma _ { \mathrm { t h } } ,\tag{8G}
$$

$$
q _ { j } \left( t + 1 \right) \leq q _ { \operatorname* { m a x } } ,\tag{8H}
$$

$$
E _ { j } \left( t + 1 \right) \leq E _ { \mathrm { t h } } ,\tag{8I}
$$

Here, (8A) ensures optimal node density by satisfying the minimum separating distance $R _ { r }$ and maximum communication range constraint $A _ { r } .$ . (8B) helps to avoid link breakage during data transmission by ensuring that $\mathrm { L D } _ { i j }$ is sufficiently larger than packet traveling time $t _ { d } .$ LD. (8C) and (8D) expresses that the acceleration and velocity should not exceed the maximum threshold. (8E) indicates that UAVs should not fly away from the bounded 3D mission area. In particular, the altitude constraint is provided to avoid the ground obstacles. (8F) represents available frequency resources. (8G) represents the SINR constraint in the UAV-to-UAV links. (8H) represents the queue backlog size of the relaying UAV, which should not exceed the maximum buffer size to avoid packet loss due to buffer overflow and network congestion. Finally, (8I) represents the RE level constraint for UAVs to stay in the air. According to problem (8) and its constraints (8A)â(8I), $\mathrm { L U } _ { i j }$ maximization is tightly coupled LUwith trajectory control, frequency resource allocation, and suitable relay UAV selection. Here, sequential decision making is required using historical states of time-varying topology. Thus, we integrated behavior-based motion properties with an adaptive DMA-DDPG algorithm to efficiently solve JTFR problem (8). The model-free DMA-DDPG does not require convexity to solve the complex optimization problem. By designing a multi-objective reward function with penalty terms, it can meet optimization objective.

<!-- image-->  
Fig. 2. Behavior-based motion model of UAVs in UAVSNs.

$$
D . \ B e h a \nu i o r { - } B a s e d M o t i o n M o d e l
$$

Behavior-based motion obeys three rules: cohesion (attraction), alignment (velocity matching), and separation (repulsion). Each rule generates a motion vector, and the weighted addition of these motion vectors defines the mobility of UAVs. The motion rules solely based on the one-hop neighbors may create partition in the UAVSN topology. Hence, two-hop mobility information is utilized to maintain the connected topology. The cohesion rule $\overrightarrow { \mathrm { C R } } _ { i } ( t )$ specifies each UAV attracted toward the average centroid position of its neighbor. Each UAV $u _ { i }$ computes $\overrightarrow { \mathrm { C R } } _ { i } ( t )$ using the relative position with one-hop neighboring UAV $u _ { j } \in N _ { i } ^ { 1 } ( t )$ located within $R _ { r } \leq d _ { i j } ( t ) \leq A _ { \ i }$ ( )r and two-hop neighbor UAVs $u _ { k } \in N _ { i } ^ { 2 } ( t )$ , as given in Fig. 2. The $\overrightarrow { \mathrm { C R } } _ { i } ( t )$ is computed as follows:

$$
\begin{array} { r l } & { \overrightarrow { \mathrm { C R } } _ { i } \left( t \right) = w _ { 1 } \left[ \frac { \sum _ { j \in N _ { i } ^ { 1 } \left( t \right) } \left\{ \overrightarrow { p _ { j } } \left( t \right) - \overrightarrow { p _ { i } } \left( t \right) \right\} } { \left. N _ { i } ^ { 1 } \left( t \right) \right. } \right] } \\ & { ~ + w _ { 2 } \left[ \frac { \sum _ { k \in N _ { i } ^ { 2 } \left( t \right) } \left\{ \overrightarrow { p _ { k } } \left( t \right) - \overrightarrow { p _ { i } } \left( t \right) \right\} } { \left. N _ { i } ^ { 2 } \left( t \right) \right. } \right] , } \end{array}\tag{9}
$$

where $w _ { 1 } + w _ { 2 } = 1$ indicates the weight of the one-hop and two-+ = 1hop neighbor motion elements. To prioritize one-hop neighbor $w _ { 1 } > w _ { 2 }$ is considered.

The alignment rule $\overrightarrow { \mathrm { A R } } _ { i } ( t )$ guides each UAV to perform ve-( )locity matching with neighboring UAVs. It helps UAVs to avoid chaotic movement. According to Fig. 2, each UAV $u _ { i }$ computes $\overrightarrow { \mathrm { A R } } _ { i } ( t )$ by using relative velocity with one-hop $u _ { j } \in N _ { i } ^ { 1 } ( t )$ and ( )two-hop neighbor $u _ { k } \in N _ { i } ^ { 2 } ( t )$ as follows:

$$
\overrightarrow { A R } _ { i } \left( t \right) = w _ { 3 } \left[ \frac { \sum _ { j \in N _ { i } ^ { 1 } \left( t \right) } \left\{ \vec { v } _ { j } \left( t \right) - \vec { v } _ { i } \left( t \right) \right\} } { \left| N _ { i } ^ { 1 } \left( t \right) \right| } \right]
$$

$$
 + w _ { 4 } [ \frac { \sum _ { k \in N _ { i } ^ { 2 } ( t ) } \{ \vec { v } _ { k } ( t ) - \vec { v } _ { i } ( t ) \} } { | N _ { i } ^ { 2 } ( t ) | } ] ,\tag{10}
$$

where $w _ { 3 } + w _ { 4 } = 1$ is the weight of the velocity alignment and $w _ { 3 } > w _ { 4 }$ + = 1is considered.

The separation rule $\overrightarrow { \mathrm { S R } } _ { i } ( t )$ guarantees the threshold of sepa-( )rating distance with nearby UAVs to prevent inter-UAV collision, as shown in Fig. 2. Moreover, it assists UAVs to preserve an optimal routing path length, while forwarding packets toward BS. Each UAV $u _ { i }$ computes $\overrightarrow { \mathrm { S R } } _ { i } ( t )$ according to the relative ( )distance with one-hop neighboring UAVs $u _ { j } \in N _ { i } ^ { r } ( t )$ located within $d _ { i j } ( t ) \leq R _ { r }$ , which is expressed as

$$
\overrightarrow { \mathrm { S R } } _ { i } \left( t \right) = \frac { \sum _ { j \in N _ { i } ^ { r } \left( t \right) } \left[ \vec { p _ { i } } \left( t \right) - \vec { p _ { j } } \left( t \right) \right] } { \left| N _ { i } ^ { r } \left( t \right) \right| }\tag{11}
$$

The above three rules assist UAVs to satisfy constraint $( 7 \mathrm { A } )$ To maintain connectivity with BS, an additional force is applied to detect the motion of each UAV $u _ { i }$ as follows:

$$
\overrightarrow { \mathbf { B S } } _ { i } \left( t \right) = \left[ \vec { p } _ { \mathrm { B S } } - \vec { p _ { i } } \right]\tag{12}
$$

Finally, the resultant force $\vec { F } _ { i } ( t )$ also known as control input is ( )obtained by applying the weighted sum of the motion rules given by (9)â(12). In JTFR, we feed these motion rules to the actor neural network, which can adaptively adjust the force weights according to the network condition. Additionally, LSTM-based actor neural network can compute each force more accurately by using the historical information of relative distance and relative velocity with nearby UAVs. According to the Newtonâs second law of motion, acceleration $\vec { a } _ { i } ( t )$ of UAV $u _ { i }$ along with flying ( )direction is computed as follows:

$$
\vec { a } _ { i } ( t ) = \frac { [ \frac { \vec { F } _ { i } ( t ) } {  \vec { F } _ { i } ( t  } ] \operatorname { t a n h } [  \vec { F } _ { i } ( t )  ] a _ { \operatorname* { m a x } } } { m _ { i } } ,\tag{13}
$$

where $m _ { i }$ denotes the mass of each UAV. tanh â¢ represents the activation function to satisfy the constraint (8C). Subsequently, the velocity of each UAV in the next timeslot can be obtained as ${ \vec { v } } _ { i } ( t + 1 ) = { \vec { v } } _ { i } ( t ) + { \vec { a } } _ { i } ( t ) \delta _ { t }$ . To satisfy constraint (8D), $\vec { v } _ { i } ( t + 1 )$ ( + 1) = ( ) + ( )is further adjusted as follows:

$$
\vec { v } _ { i } ( t + 1 ) =  \begin{array} { c } { \vec { v } _ { i } ( t + 1 ) , \qquad \vec { v } _ { i } ( t + 1 )   < v _ { \operatorname* { m a x } } } \\ { [ \frac { \vec { v } _ { i } ( t + 1 ) } { \| \vec { v } _ { i } ( t + 1 ) \| } ] \times v _ { \operatorname* { m a x } } , \| \vec { v } _ { i } ( t + 1 ) \| \geq v _ { \operatorname* { m a x } } } \end{array} \tag{14}
$$

The position at next timeslots is updated as follows:

$$
\vec { p _ { i } } \left( t + 1 \right) = \vec { p _ { i } } \left( t \right) + \left[ \vec { v } _ { i } \left( t \right) \delta _ { t } + \frac { 1 } { 2 } \vec { a } _ { i } \left( t \right) \delta _ { t } ^ { 2 } \right]\tag{15}
$$

Notably, the position vector $\vec { p _ { i } } ( t + 1 )$ can be decoupled into ( + 1)three corresponding coordinate axes along with their projection angles $( - \pi \le \sigma _ { i } ( t ) \le \pi , - ^ { \pi } / 2 \le \varphi _ { i } ( t ) \le ^ { \pi } / 2 )$ with horizontal 2 2xy-plane and z-axis, which can be further utilized to estimate the $\mathrm { L D } _ { i j }$ . Let two neighboring $\mathrm { U A V s } \left( u _ { i } , u _ { j } \right.$ have positions $p _ { i } =$ $( x _ { i } , y _ { i } , z _ { i } )$ and $p _ { j } = ( x _ { j } , y _ { j } , z _ { j } )$ (, velocities $v _ { i }$ and $v _ { j }$ =, and flying ( )directions $( \sigma _ { i } , \varphi _ { i } )$ = (and $( \sigma _ { j } , \varphi _ { j } )$ ). Once time $\Delta t$ elapses, $d _ { i j } ( \Delta t )$

is given as follows:

$$
d _ { i j } \left( \Delta t \right) = \sqrt { \left( \mathcal { X } + A \Delta t \right) ^ { 2 } + \left( \mathcal { Y } + B \Delta t \right) ^ { 2 } + \left( \mathcal { Z } + C \Delta t \right) ^ { 2 } } ,\tag{)(16}
$$

where $\mathscr X = ( x _ { i } - x _ { j } ) , ~ \mathscr Y = ( y _ { i } - y _ { j } ) , ~ \mathscr Z = ( z _ { i } - z _ { j } )$ $A =$ $( v _ { i }$ = Ïi $\varphi _ { i } - v _ { j }$ sin $\sigma _ { j }$ cos $\varphi _ { j } )$ $B = ( v _ { i }$ sin $\sigma _ { i }$ sin $\varphi _ { i } -$ vj $\sigma _ { j }$ sin $\varphi _ { j } )$ , and $C = ( v _ { i } \cos \sigma _ { i } - v _ { j } \cos \varphi _ { j } )$ in sin. Since $\mathrm { L D } _ { i j }$ sin sin ) = ( cosis bounded by the inter-UAV distance $d _ { i j } = A _ { r } ,$ LD, substituting $d _ { i j } = A _ { i }$ r in (16) yields

$$
\begin{array} { l } { \Delta t ^ { 2 } \left( A ^ { 2 } + B ^ { 2 } + C ^ { 2 } \right) + \Delta t \left( 2 A \mathcal { X } + 2 B \mathcal { Y } + 2 C \mathcal { Z } \right) } \\ { \qquad + \mathcal { X } ^ { 2 } + \mathcal { Y } ^ { 2 } + \mathcal { Z } ^ { 2 } - A _ { r } { } ^ { 2 } = 0 . } \end{array}\tag{17}
$$

The positive root solution of (17) in terms of $\Delta t$ specifies the $\mathrm { L D } _ { i j }$ Î, which can predict the link lifetime. The hello interval $\mathrm { H I } _ { i }$ LD HIfor each UAV can be adjusted adaptively according to minimum $\mathrm { L D } _ { i j }$ found within one-hop neighbor to improve the topology prediction accuracy and optimize the control overhead, which can be expressed as follows:

$$
\mathrm { H I } _ { i } = \psi \times \left[ \operatorname* { m i n } _ { j \in N _ { i } ^ { 1 } ( t ) } \mathrm { L D } _ { i j } \right] ,\tag{18}
$$

where $\psi$ symbolizes the hello frequency rate, we set 0.5 in this study. At each $\operatorname { H I } _ { i } ,$ each UAV broadcast hello packet that HIincludes a hello sequence number, unique ID, mobility information (3D position, velocity, LD, RE, frequency state, SINR, and queue backlog size) of it and its neighbors. Based on the received hello packets, each UAV $u _ { i }$ updates its one-hop and two-hop neighbor tables and motion rules as in [2].

## IV. DMA-DDPG-BASED JTFR ALGORITHM

In this section, a DMA-DDPG-based JTFR algorithm is proposed to obtain the optimal solution for the problem given in Section III-D.

## A. Necessary Preliminaries of DRL

In DRL, the agent learns to obtain an optimal policy to maximize a long-term cumulative reward by interacting with the dynamic environment without any prior knowledge. JTFR problem is treated as a multi-agent Markov game having a MDP tuple $( \mathcal { U } , O , A , R , O ^ { \prime } )$ . Here, $\mathcal { U } \in u _ { i }$ represents the set ( )of UAVs acting as learning agent, $O \in o _ { i } ( t )$ represents the observation space, $A \in a _ { i } ( t )$ represents the action space, $R \in$ $r _ { i } ( t )$ ( )represents the immediate reward after UAV $u _ { i }$ executes ( )action $a _ { i } ( t )$ , and $O ^ { \prime } \in o _ { i } { } ^ { \prime }$ represents the next observation at timeslot $( t + 1 )$ . In this game, each UAV $u _ { i }$ obtains an op-( +timal policy $\pi _ { i } : o _ { i } ( t ) \times a _ { i } ( t )$ to maximize an expected dis-: ( )counted cumulative reward $\begin{array} { r } { G _ { i } ( t ) = \sum _ { k = 0 } ^ { \infty } \lambda ^ { k } r _ { i } ( t + k ) } \end{array}$ , where $\lambda \in [ 0 1 ]$ represents the discount factor. The values of actions for sequential historical observations are measured by utilizing the state-action value function known as the Q-value. The Q-value is formulated as $Q ( o _ { i } ( t ) , a _ { i } ( t ) ) = \mathbb { E } ( G _ { i } ( t ) ) =$ $\mathbb { E } [ r _ { i } ( t ) + \lambda G _ { i } ( t + 1 ) ] = \mathbb { E } [ r _ { i } ( t ) + \lambda Q ( o _ { i } ^ { \prime } , a _ { i } ^ { \prime } ) ]$ ) = ( ( )) =. In JTFR, the [ ( ) + ( + 1)] = [ ( ) + ( )]environmental state transition, specially the behavior-based motion, updates the mobility of each UAV in the next timeslot based on the mobility in the current timeslot. This property satisfies the Markov property and can be easily integrated with MDP formulation, including most recent historical observation states, to efficiently solve the JTFR.

## B. MDP Formulation for JTFR

- Observation space: For each UAV $u _ { i } .$ the extended partial observationoi t comprises three components. The first component $o _ { i } ^ { 1 } ( t ) = \{ \overrightarrow { \mathbf { C } \mathbf { R } } _ { i } , \overrightarrow { \mathbf { A } \mathbf { R } } _ { i } , \overrightarrow { \mathbf { S } \mathbf { R } } _ { i } , \overrightarrow { \mathbf { B } \mathbf { S } } _ { i } \}$ encom-( ) =passes cohesion, alignment, separation, and connectivity with BS rule given by (9)â(12). The second component $o _ { i } ^ { 2 } ( t ) = \{ \phi _ { f _ { K , i } } , \phi _ { f _ { K , \mathscr { k } } } \}$ contains the frequency state $\phi _ { f _ { K } , }$ i ( ) =of UAV $u _ { i }$ and binary frequency band paring matrix up to two-hop neighbor $\phi _ { f _ { K , \hbar } } .$ Finally, the third component $o _ { i } ^ { 3 } ( t ) = \{ ( \mathrm { L D } _ { i j } , \mathrm { L D } _ { j k } ) , \gamma _ { i j } , E _ { j } , q _ { j } \}$ contains two-hop LD $\left( \mathrm { L D } _ { i j } , \mathrm { L D } _ { j k } \right)$ LD, SINR $\gamma _ { i j } .$ RE level $E _ { j }$ , and queue backlog (LDsize $q _ { j }$ LD )of one-hop neighboring UAVs $u _ { j }$ . Thus, the $o _ { i } ( t )$ is expressed as $o _ { i } ( t ) = [ o _ { i } ^ { 1 } ( t ) , o _ { i } ^ { 2 } ( t ) , o _ { i } ^ { 3 } ( \bar { t } ) ]$

( ) = [ ( )- Action space: The action space $a _ { i } ( t )$ comprises three components. The first component is the control input $\vec { F } _ { i }$ . Then, $\vec { a } _ { i } , \vec { v } _ { i }$ , and $\vec { p _ { i } }$ of UAV $u _ { i }$ is updated according to the motion model given by (13)â(15). The second component is UAV $u _ { i }$ selecting the frequency band $\phi _ { f _ { K , i } }$ to transmit data packet while avoiding mutual interference given by (1). The third component is relay UAV selection $u _ { j } \in N _ { i } ^ { 1 } ( t )$ in the exploration direction $\Delta _ { i j } > 0$ and $( q _ { i } - q _ { j } ) > 0$ Thus, $a _ { i } ( t ) = [ \vec { F } _ { i } , \phi _ { f _ { K , i } } , u _ { j } \in N _ { i } ^ { 1 } ]$

( ) = [Reward: The reward function $r _ { i } ( t )$ ] is designed according to $\mathrm { L U } _ { i j }$ ( )given by (7) and its constraints are considered as LUpenalties. Thus, the first component in $r _ { i } ( t )$ is a reward for the maximum-minimum LD $r _ { \mathrm { L D } } ( t )$ ( )given by (17). In ( )a multi-hop path, the minimum LD between two adjacent UAVs specifies the link lifetime. Thus, if there are several links to reach the destination BS from a particular UAV, the maximum of the minimum LD along with these multi-hop links returns the best stable link. Thus, $r _ { \mathrm { L D } } ( t )$ for up to two neighbors $\left( \mathrm { L D } _ { i j } , \mathrm { L D } _ { j k } \right)$ ( )is computed as follows:

$$
r _ { \mathrm { L D } } \left( t \right) = \frac { \mathrm { m a x } _ { j \in N _ { i } ^ { 1 } \left( t \right) , ~ k \in N _ { i } ^ { 2 } \left( t \right) } \left[ \mathrm { m i n } \{ \mathrm { L D } _ { i j } , ~ \mathrm { L D } _ { j k } \} \right] } { \mathrm { m a x } \left[ \mathrm { m i n } \{ \mathrm { L D } _ { i j } , ~ \mathrm { L D } _ { j k } \} \right] }\tag{19}
$$

The second component is the reward for link SINR rSINR t given by (2). Each UAV selects the link with highest $\gamma _ { i j } ( t ) \geq$ Î³th to achieve the highest data rate. $\mathrm { I f } \gamma _ { i j } ( t ) < \gamma _ { \mathrm { t h } }$ ( ), rSINR t is zero and computed as follows:

$$
r _ { \mathrm { S I N R } } \left( t \right) = \left\{ \begin{array} { c c } { \frac { \gamma _ { i j } \left( t \right) } { \operatorname* { m a x } _ { j \in N _ { i } ^ { 1 } \left( t \right) } \gamma _ { i j } \left( t \right) } , } & { \gamma _ { i j } \left( t \right) \geq \gamma _ { \mathrm { t h } } } \\ { 0 , } & { \mathrm { o t h e r w i s e } } \end{array} \right.\tag{20}
$$

The third component of the reward is $r _ { q } ( t )$ to ensure minimum queuing delay given by (3). Accordingly, each UAV selects the relay UAV that has smaller queue backlog size. The $r _ { q } ( t )$ is computed as follows:

$$
r _ { q } \left( t \right) = e ^ { - q _ { j } \left( t \right) }\tag{21}
$$

The fourth component of the reward is $r _ { E } ( t )$ to avoid energy ( )holes. Each UAV selects the relay UAV that has highest RE level given by (6). If the relay UAV RE level does not satisfy

constraint (8I), $r _ { E } ( t )$ is set to zero. Otherwise, $r _ { E } ( t )$ is computed as follows:

$$
r _ { E } \left( t \right) = \frac { E _ { j } } { E _ { \operatorname* { m a x } } }\tag{22}
$$

Finally, the total reward $r _ { i } ( t )$ is computed as follows:

$$
\begin{array} { r l } & { r _ { i } \left( t \right) = a r _ { \mathrm { L D } } + b r _ { \mathrm { S I N R } } + c r _ { q } + d r _ { E } - \mu _ { \mathrm { l m } } r _ { \mathrm { l m } } } \\ & { ~ - \mu _ { \mathrm { p l } } r _ { \mathrm { p l } } - \mu _ { \mathrm { m o } } r _ { \mathrm { m o } } , } \end{array}\tag{23}
$$

where $r _ { \mathrm { l m } } , \mathrm { \Delta } r _ { \mathrm { p l } } ,$ and $r _ { \mathrm { m o } }$ represent positive constants as penalties for trapping in the local minimum, violating constraint (8H), (8A) and (8E), respectively. Accordingly, $\mu _ { \mathrm { l m } } , \ \mu _ { \mathrm { p l } } ,$ , and $\mu _ { \mathrm { m o } }$ represent the binary coefficient for respective penalty terms, whose value turns into one, when associated constraints are violated, otherwise set to zero. The local minimum penalty term $r _ { \mathrm { l m } }$ considers three different cases. First, since JTFR selects the relay UAV in the direction of $\Delta _ { i j } > 0$ with maximum $\mathrm { L U } _ { i j }$ ï¼ Î 0 LUUAV will detect it as local minimum if the relay UAV has no further relaying UAV within its communication range to forward the packet toward BS. Second, if the routing loop is detected by tracing the previously visited hops in the end-to-end path. Third, if link breakage occurs for violating (8B) and UAV failure.

## C. Adaptive DMA-DDPG for JTFR

As shown in Fig. 3, each agent utilizes an adaptive DMA-DDPG algorithm with cooperative training to solve JTFR. Each agent consists of actor-critic neural network frameworks. To stabilize the learning process and make it convergent, the actor network and critic network of each agent consists of an online network and a target network. The target networks for both actor and critic have a similar neural network structure. The actor network is responsible for the approximate action policy and produce actions by mapping its own historical observation. The actor network contains three LSTM-based SRLs and an FCL, as shown in Fig. 4. The details of the neural network structures of the actor network are discussed in Section IV-C-1.

The critic network evaluates the performance of the action by generating a Q-value function. We design an adaptive multi-head attentional critic network that generates a Q-value of the actions taken by the actor network. It is achieved by considering the influence of the neighboring agentsâ state-action according to the generated attention weight, as depicted in Fig. 5. The Qvalue estimation in the critic network via cooperative training is briefly discussed in Section IV-C-2. For each $\operatorname { U A V } u _ { i } , \theta _ { i }$ and $\omega _ { i }$ represent the learnable parameters of the online actor and critic network. Similarly, $\theta _ { i } ^ { \prime }$ and $\omega _ { i } ^ { \prime }$ represent the learnable parameters of the target actor and citric networks, respectively. The actor action policy function is defined as $a _ { i } ( t ) = \mu _ { \theta _ { i } } [ o _ { i } ( t ) ]$ for the observation state $o _ { i } ( t )$ and parameter $\theta _ { i } .$ . Since each agent UAV ( )intends to maximize the long-term cumulative reward by obtaining an optimal action policy, the objective function for the actor policy can be expressed as $J ( \theta _ { i } ) = \mathbb { E } _ { \theta _ { i } } [ G _ { i } ( t ) ]$ . Accordingly, the optimal action policy $\pi _ { i } \approx \mu _ { \theta , } ^ { * }$ ) = [ ( )]can be obtained by maximizing $J ( \theta _ { i } )$ with respect to $\theta _ { i }$ as follows: $\mu _ { \theta _ { i } } ^ { * } = \arg \operatorname* { m a x } _ { \theta _ { i } } J ( \theta _ { i } )$

( ) = arg ( )As discussed in Section IV-A, a state-action value function Q-value is utilized to evaluate the expected discounted cumulative reward $\mathbb { E } ( G _ { i } ( t ) )$ . In DMA-DDPG, the Q-value of each UAV $u _ { i }$ is not only related to its own observation state and action $( o _ { i } ( t ) , a _ { i } ( t ) )$ ; it is also related to the ob-( ( ) ( ))servation and action of one-hop neighbor $\mathrm { U A V s ~ } u _ { j } \in N _ { i } ^ { 1 } ( t )$ represented as $( o _ { j } ( t ) , a _ { j } ( t ) )$ ( ), as shown in Fig. 3. Thus, in distributed cooperative training, Q-value given by the onlinecritic network of UAV $u _ { i }$ with parameter $\omega _ { i }$ is represented as $Q _ { i } ( o _ { i } ( t ) , o _ { j } ( t ) , a _ { i } ( t ) , a _ { j } ( t ) ; \omega _ { i } )$ . For simplicity, we consider $Q _ { i } ( S _ { i } , A _ { i } ; \omega _ { i } )$ ( ) ( ), where $S _ { i } = ( o _ { i } ( t ) , o _ { j } ( t ) )$ , and $A _ { i } =$ $( a _ { i } ( t ) , a _ { j } ( t ) )$ ; ) = ( ( ) ( )) =. To obtain the optimal action policy in the actor ( ( ) ( ))network gradient ascent is applied. According to the estimated $Q _ { i } ( S _ { i } , A _ { i } ; \omega _ { i } )$ , the gradient of $J ( \theta _ { i } )$ is obtained with respect to $\theta _ { i }$ as follows:

<!-- image-->  
Fig. 3. Adaptive DMA-DDPG training process and neural network architecture of an agent UAV.

<!-- image-->  
Fig. 4. Structure of an actor network.

<!-- image-->  
Fig. 5. Structure of a multi-head attentional critic network.

$$
\begin{array} { c } { \nabla _ { \theta _ { i } } J ( \theta _ { i } ) = \mathbb { E } _ { \theta _ { i } } [ \nabla G _ { i } ( t ) ] } \\ { = \mathbb { E } _ { \theta _ { i } } [ \nabla _ { \theta _ { i } } \mu _ { \theta _ { i } } ( o _ { i } ( t ) ) \nabla _ { a _ { i } } Q _ { i } ( S _ { i } , A _ { i } ; \omega _ { i } ) | _ { a _ { i } = \mu _ { \theta _ { i } } ( o _ { i } ) } ] } \end{array}\tag{24}
$$

Then, $\nabla _ { \theta _ { i } } J ( \theta _ { i } )$ given by (23) are backpropagated to the ( )online actor network with learning rate $\xi \in [ 0 1 ]$ to update $\theta _ { i }$ as follows:

$$
\theta _ { i }  \theta _ { i } + \xi \nabla _ { \theta _ { i } } J ( \theta _ { i } )\tag{25}
$$

The online critic network is updated by using the temporal difference error given by the critic loss function as follows:

$$
L \left( \omega _ { i } \right) = \mathbb { E } _ { \omega _ { i } } \left[ \left( y _ { i } ^ { t } - Q _ { i } \left( S _ { i } , { A } _ { i } ; \omega _ { i } \right) \right) ^ { 2 } \right]\tag{26}
$$

where $y _ { i } ^ { t } = r _ { i } ( t ) + \lambda Q _ { i } ^ { \prime } ( S _ { i } { } ^ { \prime } , { \pmb { A } } _ { i } { } ^ { \prime } ; \omega _ { i } ^ { \prime } ) | _ { a _ { i } ^ { \prime } = \mu _ { \theta ^ { \prime } } ( o _ { i } ^ { \prime } ) }$ represents the target value given by the target critic network.

The online critic network is updated by minimizing $L ( \omega _ { i } )$ ( )given by (26) according to gradient descent with respect to Ïi as follows:

$$
\begin{array} { r l } & { \nabla _ { \omega _ { i } } L \left( \omega _ { i } \right) = - 2 \mathbb { E } _ { \omega _ { i } } \left[ r _ { i } + \lambda Q _ { i } ^ { \prime } \left( S _ { i } ^ { \prime } , A _ { i } ^ { \prime } ; \omega _ { i } ^ { \prime } \right) \right. } \\ & { \left. - Q _ { i } \left( S _ { i } , A _ { i } ; \omega _ { i } \right) \right] \nabla _ { \omega _ { i } } Q _ { i } \left( S _ { i } , A _ { i } ; \omega _ { i } \right) } \end{array}\tag{27}
$$

According to $\nabla _ { \omega _ { i } } L ( \omega _ { i } )$ and critic network learning rate Ï, Ïi is updated as follows:

$$
\omega _ { i } \gets \omega _ { i } - \varsigma \nabla _ { \omega _ { i } } L \left( \omega _ { i } \right)\tag{28}
$$

The target actor and critic network parameters are then updated by slowly tracking the learned online network parameters

by updating rate Ï as follows:

$$
\{ \begin{array} { l l } { \theta _ { i } ^ { \prime }  \tau \theta _ { i } + ( 1 - \tau ) \theta _ { i } ^ { \prime } } \\ { \omega _ { i } ^ { \prime }  \tau \omega _ { i } + ( 1 - \tau ) \omega _ { i } ^ { \prime } } \end{array} \tag{29}
$$

Finally, to stabilize the training process, a replay buffer $\mathcal { R } _ { i }$ is employed to save the state transition samples and it is utilized to efficiently update the network parameters, as given in Fig. 3. In each training epoch, we randomly pick a mini batch M containing l samples experience dataset denoted as $( S _ { i } ^ { l } , A _ { i } ^ { l } , r _ { i } ^ { l } , S _ { i } ^ { l ^ { \prime } } )$ . According to (24) and (27), $\nabla _ { \theta _ { i } } J ( \theta _ { i } )$ and $\nabla _ { \omega _ { i } } L ( \omega _ { i } )$ )is approximated as follows:

$$
\begin{array} { l } { \displaystyle \nabla _ { \theta _ { i } } J \left( \theta _ { i } \right) \approx \frac { 1 } { M } \sum _ { l = 1 } ^ { M } } \\ { \displaystyle \times \left[ \nabla _ { \theta _ { i } } \mu _ { \theta _ { i } } \left( o _ { i } \left( t \right) \right) \nabla _ { a _ { i } } Q _ { i } \left( S _ { i } ^ { l } , A _ { i } ^ { l } ; \omega _ { i } \right) \big | _ { a _ { i } = \mu _ { \theta _ { i } } \left( o _ { i } \right) } \right] , } \end{array}\tag{30}
$$

$$
\begin{array} { c } { { \nabla _ { \omega _ { i } } L \left( \omega _ { i } \right) \approx - \displaystyle \frac { 2 } { M } \sum _ { l = 1 } ^ { M } \left[ \left[ r _ { i } ^ { l } + \lambda Q _ { i } ^ { \prime } \left( S _ { i } ^ { l ^ { \prime } } , { A _ { i } } ^ { l ^ { \prime } } ; \omega _ { i } ^ { \prime } \right) \right. \right. } } \\ { { \left. \left. - Q _ { i } \left( S _ { i } ^ { l } , { A _ { i } ^ { l } } ; \omega _ { i } \right) \right] \nabla _ { \omega _ { i } } Q _ { i } \left( S _ { i } ^ { l } , { A _ { i } ^ { l } } ; \omega _ { i } \right) \right] } } \end{array}\tag{31}
$$

1) LSTM-Based Actor Network: The actor network considers $o _ { i } ( t )$ as input, then it forwards its three components $o _ { i } ^ { 1 } ( t ) =$ $\{ \overrightarrow { \mathrm { C R } } _ { i } , \overrightarrow { \mathrm { A R } } _ { i } , \overrightarrow { \mathrm { S R } } _ { i } , \overrightarrow { \mathrm { B S } } _ { i } \} , ~ o _ { i } ^ { 2 } ( t ) = \{ \phi _ { f _ { K , i } } , \phi _ { f _ { K , \mathscr { A } } } \}$ , and $o _ { i } ^ { 3 } ( t ) =$ $\{ ( \mathrm { L D } _ { i j } , \mathrm { L D } _ { j k } ) , \gamma _ { i j } , E _ { j } , q _ { j } \}$ ) = ( ) =to three different LSTM-based (LD LD )SRLs, as illustrated in Fig. 4. LSTM utilizes cell memory to store summary of the previous inputs sequence, and gating mechanisms to control the information flow between forget gate, input gate, output gate, and cell memory. Accordingly, LSTM can adaptively learn the long-term dependency relationships between time-series data of UAVSN topology. Due to space limitations, we will not provide detailed explanations of the internal cell structure of LSTM. More details on the structure of LSTM can be found in [23].

The decoupling of observation state $o _ { i } ( t )$ through three dif-( )ferent LSTM-based SRL forwards better environmental state representation to the actor FCL, which is conducive to achieving a better deterministic policy. If all the observation states are mixed and forwarded as input to one FCL or LSTM-based SRL in actor network, it may hardly distinguish them, which leads to learning an undesirable policy. At each time, the LSTM-based SRL-1 takes the input $o _ { i } ^ { 1 } ( t )$ and based on the previous hidden state $o _ { i } ^ { h , 1 } ( t - 1 )$ , it returns the next hidden state $\mathbf { \ } _ { i } ^ { h , 1 } ( t ) = \mathrm { L S T M } [ o _ { i } ^ { 1 } ( t ) , o _ { i } ^ { h , 1 } ( t - 1 ) ]$ as output. Similar procedures are applied to obtain $o _ { i } ^ { h , 2 } ( t )$ , and $\hat { o } _ { i } ^ { h , 3 } ( t )$ for $o _ { i } ^ { 2 } ( t )$ and $o _ { i } ^ { 3 } ( t )$ ( ) ( ) ( ), respectively. Finally, the outputs given by three ( )LSTM-based SRLs are fed into FCL to produce the action $a _ { i } ( t ) = [ \vec { F } _ { i } , \phi _ { f _ { K , i } } , u _ { j } \in N _ { i } ^ { 1 } ]$

( ) = [ ]In the offline training process to explore the optimal action under current historical observation, we applied a Gaussian noise $W _ { n }$ with zero mean and limited variance as follows $a _ { i } ( t ) = [ \vec { F _ { i } } + W _ { n } , \phi _ { f _ { K , i } } , u _ { j } \in N _ { i } ^ { 1 } ]$ . Combining the Gaussian noise with action $\vec { F } _ { i }$ enhances the adaptability of JTFR to the realistic UAVSN environment, including sensor noise, positional disturbance caused by the wind, and communication delays.

Notably, the parameters of actor LSTM-based SRLs and FCL are updated according to the (24), (25), and (30).

2) Multi-Head Attentional Critic Network: The attentional critic network estimates the Q-value to evaluate the actor network performance not only by considering the observationaction of the current UAV but also by selectively paying attention to the one-hop neighboring UAVsâ observation-action. Notably, in large-scale UAVSNs, it is impractical for each UAV to pay attention to all the remaining UAVs, particularly as some UAVs may stay very far away (i.e., outside communication range), and their local observation-actions have an extremely low impact on the current UAV. Thus, to reduce computational complexity and increase scalability, we applied distributed cooperative training by only considering one-hop neighbor UAVâs observationaction. The attention mechanism generates normalized attention weight by checking the similarity between query and key vector [43].

In our multi-head attentional critic network, the query $Q =$ $g _ { h } ( o _ { i } ( t ) , a _ { i } ( t ) )$ =contains the features of the observation state-( ( ) ( ))action of a particular UAV $u _ { i } .$ , where key $K = g _ { h } ( o _ { j } ( t ) , a _ { j } ( t ) )$ and $V = g _ { h } ( o _ { j } ( t ) , a _ { j } ( t ) )$ = ( ( ) ( ))are the features of state-action of its one-hop neighbors $u _ { j } \in N _ { i } ^ { 1 } ( t )$ . Here, $g _ { h } ( \bullet )$ represents a single-( )layer FCL with learnable weights $\omega _ { Q } ^ { h } , \omega _ { K } ^ { h }$ ), and $\omega _ { V } ^ { h }$ , as shown in Fig. 5.

Subsequently, based on the scaled dot product similarity between query $Q$ and key K, the critic network generates weights to adaptively pay attention to the different one-hop neighbor UAVs. A softmax operation was performed to normalize the attention weight before multiplying with the V value to compute the context Q-value $e _ { h }$ for each head h given by (32). Finally, the output of each attention head is concatenated and passed through another two layers of multi-layer perceptron (MLP) to generate a final Q-value $Q _ { i } ( S _ { i } , A _ { i } ; \omega _ { i } )$ given by (33) to update the critic ( ; )loss and actor network parameters. We use three attention heads to focus on the features related to trajectory control, frequency band selection, and relay selection. Thus,

$$
e _ { h } = \mathrm { A T T } \left( Q , K , V \right) = \left[ \mathrm { s o f t m a x } \left( \frac { Q K ^ { T } } { \sqrt { d _ { K } } } \right) \right] \times V ,\tag{32}
$$

$$
Q _ { i } \left( S _ { i } , A _ { i } ; \omega _ { i } \right) = f _ { i } \left( g _ { i } \left( o _ { i } , a _ { i } \right) , \mathrm { c o n c a t } \left( e _ { 1 } , \cdot \cdot \cdot , e _ { h } \right) \right)\tag{33}
$$

where $d _ { K }$ represents the dimension of the key K, which is used as a scaling factor. $f _ { i } ( \bullet )$ denotes two-layers of MLP with $\omega _ { h }$ learnable weight and $g _ { i } ( \bullet )$ is a single FCL. The two-layers of ( )MLP helps to extract the features and reduce the dimension of the concatenated matrix. Notably, the critic network parameters $\omega _ { i } \cong \{ \omega _ { Q } ^ { h } , \omega _ { K } ^ { h } , \omega _ { V } ^ { h } , \ \omega _ { h } \}$ are updated according to procedures =(27), (28), and (31). The above-mentioned training process is systematically outlined in Algorithm 1.

## D. Computational Complexity

The complexity of the LSTM-based actor SRL layer is $\mathcal { O } ( N _ { L } I _ { D } S _ { L } )$ , where $N _ { L }$ denotes the number of LSTM units, $I _ { D }$ )indicates the dimension of the input observation, and $S _ { L }$ represents the sequence length remembered by the LSTM. Here, $I _ { D }$ is directly related to the number of UAVs in the swarm. The actor FCL will then have a complexity of $\mathcal { O } ( L N I O )$ , where L, N , I , and O represent the number of layers, number of neurons per layer, input features, and output features, respectively. For the multi-head attentional critic networks, complexity is $\mathcal { O } ( h \mathcal { U } ^ { 2 } I _ { A } )$ , where h denotes the number of heads (we set $h = 3 ) , \overline { { u ^ { 2 } } }$ )is for = 3performing the dot product between query, key, and value of ??

Algorithm 1: DMA-DDPG-Based JTFR Algorithm.   
Input: UAV set ??, frequency band f, and BS location $\vec { p } _ { B S }$   
Output: Optimal mobility, frequency band, and relay UAV   
selection   
1: Initialize each agent online actor and critic, and target   
actor and critic with parameters $\theta _ { i } , \omega _ { i } , \theta _ { i } ^ { \prime } ,$ , and $\omega _ { i } ^ { \prime } ,$   
respectively;   
2: Initialize each agent replay buffer $\mathcal { R } _ { i }$   
3: for each episode $= 0$ max_episode do   
= 0 :4: Randomly initialize the position and velocity of each   
$\mathrm { U A V } ;$   
5: for each timeslot $\mathcal { T } = 0 : t$ do   
6: for each UAV $u _ { i } \in \mathcal { U }$ do   
7: Obtain the motion rules using (9)â(12) and initial   
$o _ { i } ( t ) ;$   
8: ( ) Decouple $o _ { i } ( t )$ into $o _ { i } ^ { 1 } ( t ) , o _ { i } ^ { 2 } ( t )$ , and $o _ { i } ^ { 3 } ( t )$ ;   
9: Input $o _ { i } ^ { 1 } ( t ) , o _ { i } ^ { 2 } ( t )$ , and $o _ { i } ^ { 3 } ( t )$ ( ) ( )to actor LSTM-based   
( ) ( )SRLs to obtain output $o _ { i } ^ { \check { h } , 1 } ( t ) , o _ { i } ^ { h , 2 } ( t )$ , and $o _ { i } ^ { h , 3 } ( t )$ ï¼   
respectively;   
10: Forward $o _ { i } ^ { \check { h } , 1 } ( t ) , o _ { i } ^ { h , 2 } ( t )$ , and $o _ { i } ^ { h , 3 } ( t )$ to actor FCL   
( ) ( )to obtain output action   
$a _ { i } ( t ) = [ \vec { F _ { i } } , \bar { \phi } _ { f _ { K , i } } , u _ { j } \in N _ { i } ^ { 1 } ] ;$   
11: ( ) = [ Execute action   
$a _ { i } ( t ) = [ \vec { F _ { i } } + W _ { n } , \phi _ { f _ { K , i } } , u _ { j } \in N _ { i } ^ { 1 } ] \colon$   
12: ( ) = Update $\vec { a } _ { i } , \vec { v } _ { i }$ , and $\vec { p _ { i } }$ ]using motion model   
(13)â(15);   
13: Update $\mathrm { L D } _ { i j }$ using (16)â(17) and adjust $\mathrm { H I } _ { i }$ using   
(18);   
14: Update SINR $\gamma _ { i j }$ using (2);   
15: Update queue backlog size using (3) and delay   
using (4);   
16: Update residual energy level $E _ { i }$ using (6);   
17: Get reward $r _ { i } ( t )$ by using (19)â(23) and obtain $o _ { i } ^ { \prime } ;$   
18: Obtain $( o _ { j } , a _ { j } , o _ { j } ^ { \prime } )$ from $u _ { j } \in N _ { i } ^ { 1 }$ and construct   
$( S _ { i } , A _ { i } , r _ { i } , S _ { i } ^ { ' } ) ;$   
19: ( ) Store state transition data $( S _ { i } , A _ { i } , r _ { i } , S _ { i } ^ { ' } )$ in   
replay buffer $\mathcal { R } _ { i } ;$   
20: Overwrite oldest transition data if replay buffer $\mathcal { R } _ { i }$   
is full;   
21: Select a random mini batch M with l samples   
$( S _ { i } ^ { l } , A _ { i } ^ { l } , r _ { i } ^ { l } , S _ { i } ^ { l ^ { \prime } } )$ ;   
22: ( Compute $Q _ { i } ( S _ { i } , A _ { i } ; \omega _ { i } )$ according to (32)â(33);   
23: ( ; ) Update online critic network using (28), and (31);   
24: Update online actor network using (25), and (30);   
25: Update both target actor and critic network using   
(29);   
26: end for   
27: end for   
28: end for

UAVs, and $I _ { A }$ denotes the dimension of the observation-action spaces of each UAV.

Because the actor network only has the observation by considering one-hop and two-hop neighboring UAVs and the attentional critic network pays attention to only one-hop neighboring UAVs with the increased number of UAVs, the observationaction dimensionality should remain less compared to the fully centralized MA-DDPG. Additionally, in the critic network, observation-action space features extraction via single-layer FCL (in query, key, and value matrix) helps to adopt training adaptivity and avoid curse of dimensionality with the increased number of UAVs. Thus, DMA-DDPG provides higher scalability and lower computational complexity compared to the fully centralized MA-DDPG.

## V. PERFORMANCE EVALUATION

In this section, the performance of the proposed JTFR is evaluated and compared to the existing routing schemes via extensive computer simulation. For comparison, the following existing algorithms are considered:

We consider JTFR variation DMA-DDPG-1, in which both the actor and critic network has only one-hop neighbor information. DMA-DDPG-1 has a similar MDP formulation and neural network architecture as discussed in Section IV.

We consider MA-DDPG-LSTM [40], in which both actor, critic, and their target network are developed by only the LSTM cell. MDP is then formulated using the one-hop neighbor information according to the procedure given in [40].

Finally, we consider the MCA-OLSR [30], which is a recently published novel topology-based proactive crosslayer routing protocol, to validate the effectiveness of the adaptive learning-based algorithm in packet routing. MCA-OLSR is used according to the test environment to obtain the optimal multi-hop routing path between a remote UAV and BS using a table-driven method. Notably, MA-DDPG-LSTM [40] and MCA-OLSR [30] utilize the Gaussian Markov and smooth turn mobility models, respectively. To compare in a fair environment, we consider the behavior-based mobility model proposed in [2].

## A. Simulation Environment

Discrete event network simulator NS-3 version 3.35 is used to develop the UAVSN environment, and DRL frameworks are developed in PyTorch version 1.7.1. Both parts are integrated using OpenAIâs GYM framework [44]. In JTFR, each LSTM-based SRL in actor network contains 64 LSTM units. Then, the actor FCL has one input layer, two hidden layers with 256 and 128 neurons, and one output layer with 5 neurons. In the hidden layer, the rectified linear unit is used as activation function to avoid the vanishing gradient problem. In the output layers of actor FCL, we used tanh activation function to predict $\check { \vec { F _ { i \cdot } } }$ , and the softmax activation function to select the frequency band and relay UAV. The weights value for each link quality metric in (23) is set to 0.25. During training, for the trajectory control input, Gaussian noise exploration parameter was annealed exponentially from the initial value 1.0 to the minimum value 0.05. The values for the constant penalty terms $r _ { \mathrm { l m } } , \ : r _ { \mathrm { p l } } .$ , and $r _ { \mathrm { m o } }$ in (23) are set to $^ { 2 , }$ 4, and 5, respectively. The summary of hyper-parameter values in off-line training of JTFR are listed in Table I.

TABLE I  
HYPER-PARAMETERS IN DMA-DDPG OF JTFR
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Discount factor ()</td><td rowspan=1 colspan=1>0.95</td></tr><tr><td rowspan=1 colspan=1>max_episode</td><td rowspan=1 colspan=1>1000</td></tr><tr><td rowspan=1 colspan=1>Maximum timeslot per episode(J)</td><td rowspan=1 colspan=1>1000</td></tr><tr><td rowspan=1 colspan=1>Replay buffer memory size (R)</td><td rowspan=1 colspan=1>50000</td></tr><tr><td rowspan=1 colspan=1>Mini batch size (M)</td><td rowspan=1 colspan=1>256</td></tr><tr><td rowspan=1 colspan=1>Target network soft update rate (t)</td><td rowspan=1 colspan=1>0.05</td></tr><tr><td rowspan=1 colspan=1>Online actor learning rate ()</td><td rowspan=1 colspan=1>0.0001</td></tr><tr><td rowspan=1 colspan=1>Online critic learning rate(s)</td><td rowspan=1 colspan=1>0.0002</td></tr><tr><td rowspan=1 colspan=1>Optimizer</td><td rowspan=1 colspan=1>ADAM</td></tr></table>

TABLE II

ENVIRONMENT PARAMETERS OF UAVSNS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Dimension of 3D mission area</td><td rowspan=1 colspan=1> $2 5 0 0 \times 2 5 0 0 \times [ 1 0 0 - 4 0 0 ] m ^ { 3 }$ </td></tr><tr><td rowspan=1 colspan=1>Number of UAVs (U)</td><td rowspan=1 colspan=1>(30-100)</td></tr><tr><td rowspan=1 colspan=1>Channelbandwidth</td><td rowspan=1 colspan=1>20MHz</td></tr><tr><td rowspan=1 colspan=1>Bandwidth per sub-carrier (B)</td><td rowspan=1 colspan=1>1 MHz</td></tr><tr><td rowspan=1 colspan=1>UAV maximum energy $( E _ { \mathrm { m a x } } )$ </td><td rowspan=1 colspan=1>2 Ã105 Joules</td></tr><tr><td rowspan=1 colspan=1>Path loss exponent (Î±)</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>SINR threshold $( \gamma _ { \mathrm { t h } } )$ </td><td rowspan=1 colspan=1>2dB</td></tr><tr><td rowspan=1 colspan=1>CBR rate</td><td rowspan=1 colspan=1>2 Mbps</td></tr><tr><td rowspan=1 colspan=1>Packet arrival model</td><td rowspan=1 colspan=1>Poisson</td></tr><tr><td rowspan=1 colspan=1>Transportlayer</td><td rowspan=1 colspan=1>User datagram protocol</td></tr><tr><td rowspan=1 colspan=1>Maximum queue buffer size $( q _ { \mathrm { m a x } } )$ </td><td rowspan=1 colspan=1>1000Mb</td></tr></table>

Initially, UAVs were randomly positioned within a 3D mission area with dimensions $2 5 0 0 \times 2 5 0 0 \times [ 1 0 0 - 4 0 0 ] m ^ { 3 }$ . For each UAV, the value of $A _ { r }$ and $R _ { r }$ were set to m and $m ,$ respectively. The entire surveillance duration is $\mathcal { T } = 1 0 0 0 \mathrm { s } ,$ and $\delta _ { t } = 1 \mathrm { ~ s ~ }$ = 1000. The threshold value to calculate the LD was set to 1 = 1s. Initially, i was set to . s and later adaptively adjusted HI 0 5according to (18). Additionally, the values of $v _ { \mathrm { m a x } }$ and $a _ { \mathrm { m a x } }$ for each UAV are set to 20 m/s and $5 ~ \mathrm { m / s ^ { 2 } }$ , respectively. For producing data traffic, we assumed a constant bitrate (CBR)- based video streaming application operating on each UAV. At each timeslot, each UAV sends the data packet toward BS. Other important simulation parameters to set the UAVSN environment are listed in Table II.

In our simulation study, the following performance metrics are evaluated and compared.

- Average reward versus number of episodes: It visualizes the learning process of all the UAVs and the algorithm convergence over time. As the number of episodes increase, the average reward given by (23) should increase as the UAVs interact with the UAVSN environment and gradually learn to improve their action policy.

- Traveling distance fairness (TDF): The TDF for each UAV justifies the motion fairness between UAVs. It is calculated $\mathrm { { a s } } \frac { { ( \sum _ { i = 1 } ^ { u } D _ { i } ) } ^ { 2 } } { u \times { \sum _ { i = 1 } ^ { u } { ( D _ { i } ) } ^ { 2 } } }$ , where $D _ { i }$ represents the distance traveled by each UAV over the collaborative mission. Notably, $D _ { i }$ is calculated by using (15). A TDF value close to 1 implies that the travel distance of each UAV is similar. A balance in the travel distance ensures equal energy consumption for every UAV. The performance metrics to evaluate the routing protocol performance are as follows:

<!-- image-->  
Fig. 6. Average reward of all agents.

- Packet delivery ratio (PDR): PDR indicates the ratio between successfully transmitted data packets at the BS and the total number of data packets generated by all UAVs.

- Average end-to-end delay (AE2ED): AE2ED refers to the average time required to successfully transmit data packets to the BS from a particular UAV given by (4).

Normalized control overhead (NCO): NCO corresponds to the ratio between the total size of hello packets required by UAVSN and the total traffic load in the UAVSN transmitted throughout the simulation.

- Normalized residual energy (NRE): NRE for each UAV is computed using $E _ { i }$ given by (6) and normalized as $\frac { E _ { i } } { E _ { \operatorname* { m a x } } }$ A lower NRE specifies the higher energy consumption of UAVs.

## B. Simulations Results and Discussion

In this section, the simulation results are visualized and comparatively discussed.

1) Convergence Analysis: Fig. 6 demonstrates the average reward of all agents versus the number of episodes during training of 100 UAVs.

Both JTFR and its variation DMA-DDPG-1 obtain better average reward and stable learning curves compared to the MA-DDPG-LSTM. It can be attributed to the fact that each UAVâs multi-head attentional critic network pays attention to one-hop neighbor UAVs and adaptively adjusts its policy according to the neighboring UAVs policy changes, which helps to overcome the environmental non-stationarity. Through the multi-head attention in the critic network, each UAV can learn to obtain only the important features from the neighboring UAVs related to trajectory control, frequency band, and relay UAV selection, which is conducive to making better collaborative decisions. Moreover, owing to the parallelization in feature extraction and adaptive attention weight assignment to neighbor UAVs, UAVs can precisely estimate the value-function in muti-agent collaborative UAVSNs. Accordingly, it enables UAVs to obtain better action policies and accelerate the convergence for making the optimal decision.

<!-- image-->  
Fig. 7. Traveling distance fairness (TDF).

JTFR obtains the highest average reward and reaches convergence state after approximately 220 episodes because of three crucial reasons. First, owing to the benefit of expanded knowledge about dynamic topology, JTFR obtains a better observation and can avoid local optima. Second, in JTFR, each observation related to trajectory control, frequency allocation, and relay UAV selection is embedded to the three different LSTM-based SRLs in actor network to mine the temporal relationship. Consequently, LSTM-based actor SRLs output features forward better observation state to the actor FCL, which assists to obtain an optimal action policy. Finally, due to the relay UAV selection considering maximum-minimum 3D LD up to two-hop neighbors help UAVs to avoid unexpected link breakages. Since DMA-DDPG-1 utilizes only one-hop neighbor information, it provides less average reward compared to the JTFR. In contrast, MA-DDPG-LSTM did not consider the trajectory control, frequency band allocation, and two crucial constraints (8B) and (8I) in the action selection process; thus, it obtains a smaller reward. Additionally, MA-DDPG-LSTMâs critic network is solely based on LSTM units. As a result, its learning encounters more oscillations in dynamic multiagent scenarios. However, MA-DDPG-LSTM average reward is slowly increasing with the number of episodes as LSTM units are gradually updating their parameters.

Fig. 7 depicts TDF for the different number of UAVs, considering three distinct network sizes of 30 UAVs (low), 50 UAVs (medium), and 100 UAVs (high). Within each box, the horizontal line and circle represent the median and average of TDF, respectively.

Because MA-DDPG-LSTM [40] and MCA-OLSR [30] do not consider the trajectory control, we exclude it from the TDF comparison. Instead, the mobility model of the behavior-based adaptive flocking control algorithm (AFCA) [2] is considered, in which the control input is generated by performing simple vector addition of motion rules without using any LSTM/DRL method in predicting the mobility of UAVs. Moreover, in AFCA, the weight of each motion rule is adaptively adjusted by computing the changes in inter-UAV distances within the consecutive timeslots. In Fig. 7, with the increased number of UAVs, JTFR provides a better TDF value, which indicates better motion fairness and swarm cohesion in the collaborative motion task. Both JTFR and its variation DMA-DDPG-1 provide better TDF compared to the AFCA because of two key reasons. First, in JTFR, the motion rules for each UAV at a particular timeslot are treated as the observation state and forwarded to the LSTM-based actor SRL-1. The LSTM-based actor SRL-1 utilized the most recent historical state of relative distance and relative velocity to precisely predict each motion rules, which is conducive to obtaining a smoother trajectory for each UAV. Second, attention weights in the attentional critic network help to improve trajectory control policy in actor network of each UAV through collaborative decision-making. Since the mobility of each UAV at next timeslot in AFCA is estimated only based on the current timeslot mobility, AFCA provides less accuracy in mobility prediction and less TDF value.

2) Performance Comparison: In this section, the performance of JTFR is compared with that of existing schemes.

a) Varying the Number of UAVs: Fig. 8 demonstrates the network performance (PDR, AE2ED, and NCO) for different number of UAVs. According to Fig. 8(a), JTFR exhibits better PDR performance due to two major reasons. First, owing to the trajectory control according to the physical layer transmission range, UAVSN maintains optimal node density and connectivity with BS. Here, both trajectory control and optimal frequency band allocation are conducive to achieving higher SINR. Since JTFR produces the motion rules and frequency band using twohop neighbor information, it makes better decisions compared to its variation DMA-DDPG-1. Additionally, the attentional critic network improves the decision-making process to generate trajectory control input and select frequency band in actor network by paying adaptive attention to the one-hop neighbor of each UAV. In contrast, MA-DDPG-LSTM and MCA-OLSR exhibit less PDR, primarily because they did not consider trajectory control and frequency resource allocation in the physical and MAC layer. Second, unlike other routing protocols, JTFR selects the relay UAV according to the maximum-minimum 3D LD while satisfying the constraint (8B), which is conducive to obtaining a more stable path and a smaller number of retransmissions.

According to Fig. 8(b), JTFR provides less AE2ED compared to others because of three vital reasons. First, JTFR selects the relay UAV that has a small queue backlog length while satisfying constraint (8H), which helps to reduce the queuing delay. Moreover, JTFR only explores the relay UAV in the direction given by $\Delta _ { i j } > 0$ and $( q _ { i } - q _ { j } ) > 0$ to avoid excessive Î 0 ( ) 0detours of data traffic while ensuring a smaller number of hops in the end-to-end path. Second, the attentional critic network pays attention to other UAVs relay selections, which helps each UAV actor-network to avoid similar actions in relay selection. It is because if most of the UAVs choose the same relay that may congest the network. Third, owing to the advantage of trajectory control using two-hop knowledge according to the imposed communication range constraint (8A), JTFR maintains an optimal aerial node density during the entire collective motion task. In association with the optimal node density and frequency band allocation, each UAV achieves a higher SINR and less contention during simultaneous transmission. Such features are not considered by both MA-DDPG-LSTM and MCA-OLSR, thus, they encounter higher AE2ED. Moreover, MCA-OLSR utilizes carrier sense multiple access with collision avoidance, which encounters more contentions and retransmissions.

<!-- image-->  
(a) Packet delivery ratio (PDR)

<!-- image-->  
(b) Average end-to-end delay (AE2ED)

<!-- image-->  
(c) Normalized control overhead (NCO)

Fig. 8. Network performance for different number of UAVs.  
<!-- image-->  
(a) Packet delivery ratio (PDR)

<!-- image-->  
(b) Average end-to-end delay (AE2ED)

<!-- image-->  
(c) Normalized control overhead (NCO)  
Fig. 9. Network performance for different velocity of UAVs.

Fig. 8(c) illustrates the NCO performance for the different number of UAVs. JTFR and its variation DMA-DDPG-1 exhibits higher NCO compared to others. JTFR utilizes two-hop neighbor information and, thus, it requires a little higher control overhead compared to DMA-DDPG-1. However, both MA-DDPG-LSTM and MCA-OLSR broadcast hello packets in the fixed hello interval without sensing the mobility changes. As a result, they have less adaptivity to time-varying topology. Consequently, the NCO for both MA-DDPG-LSTM and MCA-OLSR increases almost linearly with the increased number of UAVs. In contrast, in JTFR and its variation DMA-DDPG-1, NCO exhibits a lesser increment in the slope. Therefore, it can be stated that JTFR has better adaptivity and scalability compared to others with a reasonable cost in control overhead.

b) Varying the Velocity of UAVs: Fig. 9 illustrates the network performance for the different maximum achievable velocities for 100 UAVs. Fig. 9(a) and (b) show that JTFR offers significantly higher PDR and less AE2ED compared to others owing to three vital reasons. First, in JTFR, to control the trajectory, each UAV computes its motion rules utilizing two-hop neighbor mobility information, and each motion rules are fed into the LSTM-based actor SRL-1 as observation at each timeslot. The LSTM-based actor SRL-1 utilizes previous historical information of relative distance and relative velocity with neighboring UAVs to represent a better state to the actor FCL to predict the control input for each UAV for updating the mobility. Moreover, the attentional critic network generates a more precise Q-value to adaptively update the learning parameters in LSTM-based actor SRLs and actor FCL according to network condition defined by the link utility maximization problem (8) and its constraints (8A)â(8I). Second, in the reward function given by (23), JTFR gives more reward for selecting the relay UAV that has stable mobility intimacy with neighboring UAVs defined by the maximum-minimum 3D LD. Third, in JTFR, since each UAV selects a frequency band by paying attention to the neighboring UAVs participating in the simultaneous transmissions, each UAV can significantly minimize mutual interference, which helps to achieve higher data rate. Furthermore, the relay UAV selection considering less queuing backlog size with imposed constraint (8H) and packet travel time constraint (8B) helps to not only exhibit less network congestion and delay but also avoid unexpected link breakages. Thus, it helps to reduce the unnecessary retransmissions of data packets. Neither MA-DDPG-LSTM nor MCA-OLSR support the aforementioned features, resulting in lower PDR and higher AE2ED.

According to Fig. 9(c), JTFR and its variation DMA-DDPG-1 exhibit higher NCO compared to other baseline protocols. It is because, with the increased velocity, each UAV encounters a higher degree of changes in mobility and, thus, residual LD changes. Consequently, in JTFR, the hello interval frequency given by (19) becomes smaller and triggers higher control overhead compared to the others to achieve the dynamic topology. Additionally, JTFR requires collecting mobility information from one-hop and two-hop neighbors and, thus, it encounters higher NCO. Because both MA-DDPG-LSTM and MCA-OLSR use a fixed hello interval, they have not only less sensitivity to dynamic topology changes but also less NCO. In particular, because the advantages of multi-point relay selection in MCA-OLSR reduce redundancy in hello packet broadcasting, MCA-OLSR exhibits less NCO than the others.

<!-- image-->  
Fig. 10. Normalized residual energy (NRE).

However, for both MA-DDPG-LSTM and MCA-OLSR, the NCO increases almost linearly with the increased velocity. In contrast, JTFR and DMA-DDPG-1 have less increment in control overhead, owing to its adaptive learning. Therefore, considering this reasonable cost in NCO, it can be stated that JTFR offers a significant improvement in network performance.

In Fig. 10, the NRE of all UAVs are depicted for different routing protocols, with considerations for network size scenarios of 30 UAVs (low), 50 UAVs (medium), and 100 UAVs (high). The horizontal line and circle within each NRE distribution box represent the median and average of NRE, respectively. According to Fig. 10, the proposed JTFR provides better NRE status (less energy consumption) owing to the following two vital reasons. In JTFR, we notice better TDF that each UAV travels almost a similar distance to execute the collective motion task by obeying the behavior-based motion rules. Since propulsion energy consumption is directly proportional to the flying distance, and it is significantly higher than communication energy consumption, balancing the flying distance between UAVs is equivalent to obtaining equal and minimal UAV energy consumption. Second, in the link utility function, JTFR jointly considers the relay UAV RE and mobility prediction metric LD, which facilitates obtaining stable end-to-end paths with fewer retransmissions. Thus, it significantly reduces the packet transmission energy consumption. Because both MA-DDPG-LSTM and MCA-OLSR do not consider the trajectory control and UAV RE level in the routing metric, they produce less NRE status (higher energy consumption).

Notably, the computational energy cost to train the JTFR model is not considered, because the entire training process will be performed in offline mode. Following the training, the trained model will be uploaded to each UAV to execute the mission online. During the training process, we introduced the Gaussian noise with a control input to achieve adaptivity to the dynamic UAVSNs. Moreover, during online execution, the trained model of each UAV collects the observation from one-hop and two-hop neighbors using hello packets and constructs its MDP to make optimal real-time decisions. Subsequently, JTFR can also utilize the attentional critic network to improve its policy.

c) Summary of Performance Improvement: In this subsection, a comparative summary on the performance improvement over the baseline protocols is presented. In the scalability test, JTFR exhibits 23.71%, and 13.40% better average TDF compared to AFCA and DMA-DDPG-1, respectively. JTFR then gives 15.20%, 25.03%, and 32.42% better average PDR compared to DMA-DDPG-1, MA-DDPG-LSTM, and MCA-OLSR, respectively. JTFR provides 30.82%, 51.46%, and 60.23% less AE2ED compared to DMA-DDPG-1, MA-DDPG-LSTM, and MCA-OLSR, respectively. Nevertheless, JTFR exhibits 8.18%, 13.15%, and 19.35% higher average NCO compared to DMA-DDPG-1, MA-DDPG-LSTM, and MCA-OLSR, respectively.

In the velocity increment test varying the velocity of UAVs, JTFR exhibits 14.51%, 22.37%, and 24.02% better average PDR compared to DMA-DDPG-1, MA-DDPG-LSTM, and MCA-OLSR, respectively. Moreover, JTFR provides 30.04%, 51.46%, and 57.25% better AE2ED compared to DMA-DDPG-1, MA-DDPG-LSTM, and MCA-OLSR, respectively. However, JTFR exhibits 5.63%, 6.80%, and 10.37% higher average NCO compared to DMA-DDPG-1, MA-DDPG-LSTM, and MCA-OLSR, respectively. Additionally, JTFR exhibits 20%, 36%, and 46% less average energy consumption compared to DMA-DDPG-1, MA-DDPG-LSTM, and MCA-OLSR, respectively. Owing to the remarkable performance enhancement in PDR, AE2ED, and energy consumption, such reasonable cost in control overhead is acceptable.

## VI. CONCLUSION

In this study, we formulated a link utility maximization problem by jointly considering the 3D LD, link SINR, delay, and UAV RE level under several practical constraints to route data packets from UAVSNs to BS. To solve this problem, the adaptive DMA-DDPG-based JTFR algorithm coupled with swarming behavior is proposed, in which each UAV actor network obtains the adaptivity with time-varying topology by using its LSTM-based SRLs. Subsequently, critic networks obtain the precise Q-value to train each UAV actor policy and minimize the critic loss by adaptively paying attention to the neighboring UAVs. Joint consideration of collaborative trajectory control and frequency band selection maximizes both link SINR and link stability in UAVSNs as they are highly coupled. Additionally, owing to the consideration of 3D maximum-minimum LD, queue backlog size, and RE level of relaying UAV in JTFR is conducive to achieving significant improvements in packet routing in terms of PDR, AE2ED, and energy consumption. As our future work, we will design machine learning-based adaptive routing protocols for heterogeneous UAVSNs.

## ACKNOWLEDGMENT

The authors thank the editor and anonymous referees for their comments that helped improve the quality of this manuscript. This article is based on the first author M. M. Alamâs Ph.D. thesis supervised by the second author S. Moh [45].

## REFERENCES

[1] Q. Zhang, M. Jiang, Z. Feng, W. Li, W. Zhang, and M. Pan, âIoT enabled UAV: Network architecture and routing algorithm,â IEEE Internet Things J, vol. 6, no. 2, pp. 3727â3742, Apr. 2019, doi: 10.1109/JIOT.2018.2890428.

[2] M. M. Alam and S. Moh, âQ-learning-based routing inspired by adaptive flocking control for collaborative unmanned aerial vehicle swarms,â Veh. Commun., vol. 40, Apr. 2023, Art. no. 100572, doi: 10.1016/j.vehcom.2023.100572.

[3] M. M. Alam and S. Moh, âJoint topology control and routing in a UAV swarm for crowd surveillance,â J. Netw. Comput. Appl., vol. 204, Aug. 2022, Art. no. 103427, doi: 10.1016/j.jnca.2022.103427.

[4] M. M. Alam and S. Moh, âJoint optimization of trajectory control, task offloading, and resource allocation in airâground integrated networks,â IEEE Internet Things J., early access, Apr. 17, 2024, doi: 10.1109/JIOT.2024.3390168.

[5] R. Ding, J. Chen, W. Wu, J. Liu, F. Gao, and X. Shen, âPacket routing in dynamic multi-hop UAV relay network: A multi-agent learning approach,â IEEE Trans. Veh. Technol., vol. 71, no. 9, pp. 10059â10072, Sep. 2022, doi: 10.1109/TVT.2022.3182335.

[6] T. Li et al., âA mean field game-theoretic cross-layer optimization for multi-hop swarm UAV communications,â J. Commun. Netw., vol. 24, no. 1, pp. 68â82, Feb. 2022, doi: 10.23919/JCN.2021.000035.

[7] M. M. Alam, M. Y. Arafat, S. Moh, and J. Shen, âTopology control algorithms in multi-unmanned aerial vehicle networks: An extensive survey,â J. Netw. Comput. Appl., vol. 207, Nov. 2022, Art. no. 103495, doi: 10.1016/j.jnca.2022.103495.

[8] T. Li et al., âJoint power control and scheduling for high-dynamic multihop UAV communication: A robust mean field game,â IEEE Access, vol. 9, pp. 130649â130664, 2021, doi: 10.1109/ACCESS.2021.3113909.

[9] L. Hong, H. Guo, J. Liu, and Y. Zhang, âToward swarm coordination: Topology-aware inter-UAV routing optimization,â IEEE Trans. Veh. Technol., vol. 69, no. 9, pp. 10177â10187, Sep. 2020, doi: 10.1109/TVT.2020.3003356.

[10] J. Wu et al., âAutonomous cooperative flocking for heterogeneous unmanned aerial vehicle group,â IEEE Trans. Veh. Technol., vol. 70, no. 12, pp. 12477â12490, Dec. 2021, doi: 10.1109/TVT.2021.3124898.

[11] G. Shen et al., âDeep reinforcement learning for flocking motion of multi-UAV systems: Learn from a digital twin,â IEEE Internet Things J, vol. 9, no. 13, pp. 11141â11153, Jul. 2022, doi: 10.1109/JIOT.2021. 3127873.

[12] J. Xiao, G. Yuan, J. He, K. Fang, and Z. Wang, âGraph attention mechanism based reinforcement learning for multi-agent flocking control in communication-restricted environment,â Inf. Sci., vol. 620, pp. 142â157, Jan. 2023, doi: 10.1016/j.ins.2022.11.059.

[13] R. Ding, F. Gao, and X. S. Shen, â3D UAV trajectory design and frequency band allocation for energy-efficient and fair communication: A deep reinforcement learning approach,â IEEE Trans. Wirel. Commun., vol. 19, no. 12, pp. 7796â7809, Dec. 2020, doi: 10.1109/TWC.2020.3016024.

[14] X. Chu and H. Ye, âParameter sharing deep deterministic policy gradient for cooperative multi-agent reinforcement learning,â Oct. 2017. [Online]. Available: http://arxiv.org/abs/1710.00336

[15] S. Iqbal and F. Sha, âActor-attention-critic for multi-agent reinforcement learning,â in Proc. 36th Int. Conf. Mach. Learn., 2019, pp. 5261â5270.

[16] P. Qin, Y. Fu, Y. Xie, K. Wu, X. Zhang, and X. Zhao, âMulti-agent learning-based optimal task offloading and UAV trajectory planning for AGIN-power IoT,â IEEE Trans. Commun., vol. 71, no. 7, pp. 4005â4017, Jul. 2023, doi: 10.1109/TCOMM.2023.3274165.

[17] S. Zhang, A. Liu, C. Han, X. Liang, X. Xu, and G. Wang, âMulti-agent reinforcement learning-based orbital edge offloading in sagin supporting Internet of Remote Things,â IEEE Internet Things J., vol. 10, no. 23, pp. 20472â20483, Dec. 2023, doi: 10.1109/JIOT.2023.3287737.

[18] B. Chen, D. Liu, and L. Hanzo, âDecentralized trajectory and power control based on multi-agent deep reinforcement learning in UAV networks,â in Proc. IEEE Int. Conf. Commun., 2022, pp. 3983â3988, doi: 10.1109/ICC45855.2022.9838637.

[19] H. Mao, Z. Zhang, Z. Xiao, and Z. Gong, âModelling the dynamic joint policy of teammates with attention multi-agent DDPG,â in Proc. Int. Conf. Auton. Agents Multiagent Syst., 2019, pp. 1108â1116.

[20] R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, and I. Mordatch, âMultiagent actor-critic for mixed cooperative-competitive environments,â in Proc. Adv. Neural Inf. Process. Syst., 2017, pp. 6380â6391.

[21] J. Tian, Q. Liu, H. Zhang, and D. Wu, âMultiagent deep-reinforcementlearning-based resource allocation for heterogeneous QoS guarantees for vehicular networks,â IEEE Internet Things J., vol. 9, no. 3, pp. 1683â1695, Feb. 2022, doi: 10.1109/JIOT.2021.3089823.

[22] J. Liu, Q. Wang, and Y. Xu, âAR-GAIL: Adaptive routing protocol for FANETs using generative adversarial imitation learning,â Comput. Netw., vol. 218, Dec. 2022, Art. no. 109382, doi: 10.1016/j.comnet.2022. 109382.

[23] R. W. Liu, M. Liang, J. Nie, W. Y. B. Lim, Y. Zhang, and M. Guizani, âDeep learning-powered vessel trajectory prediction for improving smart traffic services in maritime Internet of Things,â IEEE Trans. Netw. Sci. Eng., vol. 9, no. 5, pp. 3080â3094, Sep./Oct. 2022, doi: 10.1109/TNSE.2022.3140529.

[24] J. Wang, X. Zhang, X. He, and Y. Sun, âBandwidth allocation and trajectory control in UAV-assisted IoV Edge computing using multiagent reinforcement learning,â IEEE Trans. Reliab., vol. 72, no. 2, pp. 599â608, Jun. 2023, doi: 10.1109/TR.2022.3192020.

[25] Z. Ye, K. Wang, Y. Chen, X. Jiang, and G. Song, âMulti-UAV navigation for partially observable communication coverage by graph reinforcement learning,â IEEE Trans. Mobile Comput., vol. 22, no. 7, pp. 4056â4069, Jul. 2023, doi: 10.1109/TMC.2022.3146881.

[26] D. Chen, Q. Qi, Z. Zhuang, J. Wang, J. Liao, and Z. Han, âMean field deep reinforcement learning for fair and efficient UAV control,â IEEE Internet Things J., vol. 8, no. 2, pp. 813â828, Jan. 2021, doi: 10.1109/JIOT.2020.3008299.

[27] W. Lee and T. Kim, âMulti-agent reinforcement learning in controlling offloading ratio and trajectory for multi-UAV mobile edge computing,â IEEE Internet Things J, vol. 11, no. 2, pp. 3417â3429, Jan. 2024, doi: 10.1109/JIOT.2023.3296774.

[28] D. Shumeye Lakew, U. Saâad, N.-N. Dao, W. Na, and S. Cho, âRouting in flying Ad Hoc networks: A comprehensive survey,â IEEE Commun. Surv. Tut., vol. 22, no. 2, pp. 1071â1120, Second Quarter 2020, doi: 10.1109/COMST.2020.2982452.

[29] O. S. Oubbati, A. Lakas, F. Zhou, M. GÃ¼neÂ¸s, and M. B. Yagoubi, âA survey on position-based routing protocols for flying Ad hoc networks (FANETs),â Veh. Commun., vol. 10, pp. 29â56, Oct. 2017, doi: 10.1016/j.vehcom.2017.10.003.

[30] S. Garg, A. Ihler, E. S. Bentley, and S. Kumar, âA cross-layer, mobility, and congestion-aware routing protocol for UAV networks,â IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 4, pp. 3778â3796, Aug. 2023, doi: 10.1109/TAES.2022.3232322.

[31] B. Wang, Y. Sun, T. Do-Duy, E. Garcia-Palacios, and T. Q. Duong, âAdaptive D-hop connected dominating set in highly dynamic flying Ad-Hoc networks,â IEEE Trans. Netw. Sci. Eng., vol. 8, no. 3, pp. 2651â2664, Third Quarter 2021, doi: 10.1109/TNSE.2021.3103873.

[32] X. Qi, P. Yuan, Q. Zhang, and Z. Yang, âCDS-based topology control in FANETs via power and position optimization,â IEEE Wirel. Commun. Lett., vol. 9, no. 12, pp. 2015â2019, Dec. 2020, doi: 10.1109/LWC.2020.3009666.

[33] M. Y. Arafat and S. Moh, âLocalization and clustering based on swarm intelligence in UAV networks for emergency communications,â IEEE Internet Things J, vol. 6, no. 5, pp. 8958â8976, Oct. 2019, doi: 10.1109/JIOT.2019.2925567.

[34] J. Guo et al., âICRA: An intelligent clustering routing approach for UAV Ad Hoc networks,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 2, pp. 2447â2460, Feb. 2023, doi: 10.1109/TITS.2022.3145857.

[35] A. Bujari, C. E. Palazzi, and D. Ronzani, âA comparison of stateless position-based packet routing algorithms for FANETs,â IEEE Trans. Mob. Comput., vol. 17, no. 11, pp. 2468â2482, Nov. 2018, doi: 10.1109/TMC.2018.2811490.

[36] Y. Cui, Q. Zhang, Z. Feng, Z. Wei, C. Shi, and H. Yang, âTopology-aware resilient routing protocol for FANETs: An adaptive Q -learning approach,â IEEE Internet Things J., vol. 9, no. 19, pp. 18632â18649, Oct. 2022, doi: 10.1109/JIOT.2022.3162849.

[37] M. Y. Arafat and S. Moh, âA Q -learning-based topology-aware routing protocol for flying Ad Hoc networks,â IEEE Internet Things J., vol. 9, no. 3, pp. 1985â2000, Feb. 2022, doi: 10.1109/JIOT.2021.3089759.

[38] M. Zhang, C. Dong, P. Yang, T. Tao, Q. Wu, and T. Q. S. Quek, âAdaptive routing design for flying Ad Hoc networks,â IEEE Commun. Lett., vol. 26, no. 6, pp. 1438â1442, Jun. 2022, doi: 10.1109/LCOMM.2022.3152832.

[39] X. Qiu, Y. Yang, L. Xu, J. Yin, and Z. Liao, âMaintaining links in the highly dynamic FANET using deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 2804â2818, Mar. 2023, doi: 10.1109/TVT.2022.3217888.

[40] X. Qiu, L. Xu, P. Wang, Y. Yang, and Z. Liao, âA data-driven packet routing algorithm for an unmanned aerial vehicle swarm: A multi-agent reinforcement learning approach,â IEEE Wirel. Commun. Lett., vol. 11, no. 10, pp. 2160â2164, Oct. 2022, doi: 10.1109/LWC.2022.3195963.

[41] X. Liu, Y. Liu, Y. Chen, and L. Hanzo, âTrajectory design and power control for multi-UAV assisted wireless networks: A machine learning approach,â IEEE Trans. Veh. Technol., vol. 68, no. 8, pp. 7957â7969, Aug. 2019, doi: 10.1109/TVT.2019.2920284.

[42] S. Park, C. Park, and J. Kim, âLearning-based cooperative mobility control for autonomous drone-delivery,â IEEE Trans. Veh. Technol., vol. 73, no. 4, pp. 4870â4885, Apr. 2024, doi: 10.1109/TVT.2023.3330460.

[43] A. Vaswani et al., âAttention is all you need,â in Proc. Adv. Neural Inf. Process. Syst., 2017, pp. 5999â6009.

[44] P. Gawlowicz and A. Zubow, âns3-gym : Extending OpenAI gym for networking,â 2018, arXiv1810.03943.

[45] M. M. Alam, âRouting algorithms based on reinforcement learning for unmanned aerial vehicle swarm networks,â Ph.D. thesis, Dept. Comput. Eng., Chosun Univ., Gwangju, South Korea, Aug. 2023.

<!-- image-->

Muhammad Morshed Alam received the BSc degree in electrical and electronic engineering from Independent University, Bangladesh, in 2013, the MSc degree in electrical and electronic engineering from Islamic University of Technology, Bangladesh, in 2018, and the PhD degree in computer engineering from Chosun University, South Korea, in 2023. During his doctoral study, he was a grantee of the Korean Government Scholarship Program. Since 2023, he is an assistant professor with the Department of Electrical and Electronic Engineering, American Interna-

tional University Bangladesh (AIUB). His current research interests include unmanned aerial vehicle swarm networks with a focus on network architectures and protocols.

<!-- image-->

Sangman Moh (Member, IEEE) received the MSc degree in computer science from Yonsei University, South Korea, in 1991, and the PhD degree in computer engineering from Korea Advanced Institute of Science and Technology (KAIST), South Korea, in 2002. Since late 2002, he is a professor with the Department of Computer Engineering, Chosun University, South Korea. From 2006 to 2007, he was on leave with Cleveland State University, USA. Until 2002, he had been with Electronics and Telecommunications Research Institute (ETRI), South Korea, where he

served as a project leader. His research interests include mobile computing and networking, ad hoc and sensor networks, unmanned aerial vehicle networks, and mobile-edge computing. He is a member of the ACM, the IEICE, the KIISE, the IEIE, the KIPS, the KICS, the KMMS, the IEMEK, the KISM, and the KPEA.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_6_img_1.jpeg|page_6_img_1]]
3. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_9_img_1.jpeg|page_9_img_1]]
4. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_9_img_2.jpeg|page_9_img_2]]
5. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_9_img_3.jpeg|page_9_img_3]]
6. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_12_img_1.jpeg|page_12_img_1]]
7. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_13_img_1.jpeg|page_13_img_1]]
8. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_14_img_1.jpeg|page_14_img_1]]
9. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_14_img_2.png|page_14_img_2]]
10. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_15_img_1.jpeg|page_15_img_1]]
11. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_17_img_1.jpeg|page_17_img_1]]
12. [[../extracted_images/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De/page_17_img_2.jpeg|page_17_img_2]]

---

