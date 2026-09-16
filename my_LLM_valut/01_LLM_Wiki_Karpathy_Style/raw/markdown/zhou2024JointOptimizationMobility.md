# Joint Optimization of Mobility and Reliability-Guaranteed Air-to-Ground Communication for UAVs

Jianshan Zhou , Daxin Tian , Senior Member, IEEE, Yaqing Yan, Xuting Duan , and Xuemin Shen , Fellow, IEEE

AbstractâAerial unmanned vehicles (UAVs) play a significant role in improving the connectivity and coverage of terrestrial communication networks. However, UAV-assisted air-to-ground (A2G) data transmissions usually encounter several fundamental challenges, such as terminal mobility, random nature in channel fading and contention, resource constraints, and application-specific transmission requirements. To tackle these challenges, we formulate a bi-level optimization problem that jointly considers the control of the UAV mobility and transmission power and the scheduling of A2G data transmissions. The objective is to optimize energy consumption and maximize A2G transmission reliability. Particularly, we first theoretically characterize the A2G transmission reliability from a probabilistic perspective concerning the effects of channel fading, channel access contention, and application requirements. We then derive a closed-form expression for the optimal expected transmission reliability. Using the closed-form reliability, we transform the bi-level optimization into a mathematically-tractable optimal control problem and propose an efficient iterative algorithm to solve it. Simulation results show that our approach provides a comprehensive improvement in terms of both energy utilization and A2G transmission reliability, in particular, with a reduction of more than 12.1% in energy consumption and an increase of 7.53% in reliability on average, compared to several baselines.

Index TermsâAir-to-ground communication, data transmission scheduling, trajectory design, unmanned aerial vehicle

## 1 INTRODUCTION

HE successful deployment of aerial-ground cooperative Tnetworks (AGCNs) relies on high-performance aerial platforms such as aerial unmanned vehicles (UAVs). In particular, UAV-assisted air-to-ground (A2G) transmissions are crucial for AGCN applications, such as remote sensing, aerial Internet of Things (IoT), and aerial computing. UAVassisted A2G data transmissions need to adapt to highly dynamic topologies, account for inherent randomness in the physical-layer channel, and meet application-specific deadline and integrity requirements. However, several significant challenges are to be addressed for the practical realization of UAV-assisted A2G data transmissions. These challenges arise from the complicated constraints on both the kinematics and energy resource of a UAV, applicationlayer transmission requirements, stochastic channel fading, and stochastic multi-user access contention. More critically, the AGCN network should provide A2G transmission reliability guarantees in terms of satisfaction of application deadline and data integrity requirements.

Energy efficiency is one of the most important optimization goals in UAV-assisted communication and networking systems. Thus, it has been widely investigated in the recent literature. Currently, many researchers are engaged in designing various energy-efficient UAV-assisted networks by jointly optimizing UAV trajectory and some other decision-making factors such as transmission power and bit allocation [1], [2], [3], [4]. In addition to the energy efficiency of the network, the reliability of data transmission links is another significant design goal. To be specific, the communication reliability can be usually represented by the possibility that a node can complete data transmissions by a required deadline [5]. That is, the application data should be fully transmitted from a source to a destination to guarantee the integrity of application representation in the application layer. Fragmented data cannot be effectively used by upper-layer applications. Due to the dynamic and stochastic nature of A2G channels, the issue of unreliable data transmissions (incurring data fragmentation) tends to be even more severe in UAV-assisted networks. In this regard, the reliability-oriented A2G transmission optimization poses a great challenge to the practical realization of a UAV-assisted network.

Despite the presence of many high-quality research works in the context of joint UAV trajectory and resource optimization, limited efforts have been dedicated to the joint optimization of kinematic control and reliability-guaranteed communication of the UAV. Besides, since the A2G channel not only involves a stochastic fading process but also depends on the time-varying relative distance between a UAV and a ground node, the probability that a UAV succeeds in transmitting all the required data to the ground node within a restricted time duration is inherently coupled with the channel fading characteristics and the UAV mobility control. The exogenous factors, including the total data load and the given transmission period, also affect the success probability of A2G data transmission completion. However, due to the above factors, it remains unexplored that how to characterize the UAV-assisted A2G transmission reliability from a probabilistic perspective and how to join the reliability factor and the energy efficiency into an optimization framework for a UAV-assisted network.

Toward this end, we investigate a UAV-assisted A2G network in this paper, where a UAV needs to fly from an initial position to a specified terminal point under a sequence of autonomous acceleration control inputs. The UAV acts as an aerial mobile sensor offloading its application or massive sensor data to several ground base stations. The goal of the aerial autonomous system is to minimize its energy consumption in motion and communication meanwhile maximizing the reliability of A2G data transmissions. To achieve this goal, we propose a joint optimization framework that incorporates the UAV mobility control and data transmission scheduling. In particular, we jointly control the acceleration input and transmission power of the UAV and schedule A2G data transmissions during its flight, meanwhile satisfying the boundary conditions of the trajectory and the deadline and integrity requirements of the data transmissions. To tackle the problem, we theoretically characterize the expected A2G data transmission reliability and propose a bi-level optimization model. Additionally, we derive a closed-form expression for the maximum expected reliability and transform the non-convex problem into a mathematically-tractable one. We also propose an efficient iterative optimization. We compare our method with other typical methods to show its effectiveness and superior performance. Specifically, the main novel contributions of the paper are as follows:

We formulate a bi-level optimization model to minimize the motion and communication energy consumption of the UAV in the upper layer and maximize the A2G transmission reliability in the lower layer. Different from most of the recent literature, we take into account controlling the UAVâs mobility and transmission power and scheduling its data transmissions at the same time.

We theoretically characterize the UAV-assisted A2G transmission reliability from a probabilistic perspective regarding the effects of Non-Line-of-Sight (NLoS) channel fading, stochastic channel contention, and Authorized licensed use limited to: Beijing Normal University. Downloade application-specified deadline and integrity restrictions. We derive a closed-form expression for the optimal expected A2G transmission reliability and incorporate it into an -constraint to transform the bilevel optimization model into a mathematically-tractable optimal control model. The obtained model enables the practical design and implementation of optimization algorithms.

We propose an efficient iterative algorithm by combining a direct multi-shooting approach and a successive convex approximation technique. We theoretically prove the convergence and complexity of the proposed algorithm. Simulation results also demonstrate that the proposed method provides a remarkable improvement in both energy utilization and transmission reliability.

The rest of our paper is as follows. We review related works in Section 2. We present the overall system model and formulate the problem in Section 3. In Section 4, we propose a joint optimization method and analyze the convergence and the computational complexity of the proposed method. Simulation results are provided to validate our method in Section 5. Finally, Section 6 concludes the paper and remarks our future work.

## 2 LITERATURE REVIEW

Recently, a wide variety of joint resource allocation and trajectory optimization schemes have been developed for enabling UAV-assisted communications and networking. For instance, M. Li et al. aim to maximize the energy efficiency of a UAV-assisted edge computing system and present a successive convex approximation (SCA) approach to jointly optimize the trajectory of a UAV, the transmission power of ground users, and computation load allocation [3]. From considerable recent literature [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], the SCA technique is witnessed as a powerful tool to solve various complicated non-convex joint optimization problems. For example, the SCA technique is combined with a problem-based decomposition scheme to address the joint optimization of the power allocation and trajectory of a UAV and the communication scheduling of ground vehicles in [6]. [7] considers a mobile edge computing system consisting of a UAV and a vehicle platoon and proposes an SCA-based iterative optimization algorithm to maximize the system computation rate. Since it is usually difficult or even impossible to solve a general non-convex optimization problem, many researchers propose different decomposition schemes. That is, they first decompose joint optimization problems into several subproblems, where a part of decision variables are fixed while the rest are optimized, and then exploit SCA-based techniques such as [8], [9], [10], [11]. In some other works such as [12], researchers integrate wireless information and power transfer (SWIFT) into UAV-enabled sensor networks and develop geometry-based optimization algorithms to determine the suboptimal UAV trajectory. In [13], the SCA technique is combined with some combinational optimization schemes, such as the cutting-plane method, to find the optimal uploading power of ground sensors and the optimal hovering position of a UAV. In [14], a neighborhood search on July 16,2024 at 03:12:15 UTC from IEEE Xplore. Restrictions apply.

technique applied for the well-known traveling salesman problem (TSP) and convex optimization are combined to jointly optimize the UAV hovering locations, communication durations, and trajectory. The goal is to minimize the whole energy consumption of the UAV. Other successful cases of the SCA-based joint optimization approach can also be founded in the cellular-connected UAV networks [15], [16]. Additionally, the SCA technique is combined with a block alternating descent scheme to solve the problem of joint trajectory and resource optimization in UAV-assisted networks [17], [18]. Although there already exist a wide variety of SCA-based schemes to tackle the joint design and optimization problem of UAV trajectory, computing, and communication, few studies provide deep insights into the reliability-oriented optimization, in particular, the theoretical characterization of data transmission reliability from a probabilistic perspective.

Another promising direction that currently sees much activity is dealing with joint optimization problems of UAV-enabled edge computing and communication with policy optimization- or learning-based techniques, e.g., Deep Reinforcement Learning (DRL) that models a system problem as a kind of sequential decision-making process following a Markovian property [4], [19], [20], [21], [22], [23], [24], [25], [26]. For example, L. Wang et al. combine DRL with a block coordinate descent scheme to minimize the overall energy consumption of ground mobile users, in which the usersâ association, resource allocation and multiple UAVsâ trajectories are treated as joint optimization variables [19]. A. Al-Hilo et al. exploit policy optimization techniques to maximize the overall throughput of a UAV-assisted network, in which their joint solution for the trajectory and power allocation of UAVs is represented by a policy [20]. In [21], S. Xu et al. combine the Kmeans cluster algorithm and DRL technique to jointly design the trajectories of multiple UAVs. DRL in the multi-agent settings, i.e., multi-agent deep reinforcement learning, is also employed for optimization of multiple UAVsâ trajectories, computation offloading policies, and power allocation [22], [23]. Even though DRL provides a powerful technique to approximate near-optimal policies in stochastic dynamic environments, such a paradigm that depends on carefully-tuned deep neural networks encounters some inherent challenges such as high training cost and sensitivity to both hyperparameters and initial conditions. Therefore, different DRL techniques (e.g., deep Q-learning, deep deterministic policy gradient (DDPG), and advanced actor-critic algorithms like A2C and A3C) are usually integrated into other optimization architectures, such as mixed-integer nonlinear programming [24], coverage maximization [25], dynamic spatialtemporal configuration [4], and alternative iterative optimization [26]. However, from the point of view of practical applications with UAVs, there still are many issues to be addressed for various DRL-based UAV systems, among which convergence efficiency, scalability, and physical satisfaction significantly affect the practical deployment of DRL in the real world.

Due to network resource constraints, concurrent data transmissions from multiple UAVs and ground users usually incur serious channel contention. To realize resource allocation in the multi-node competition context, many researchers propose novel optimization approaches based on game theory [27], [28], [29], [30]. In these works, a Nash equilibrium strategy is treated as their system solution that aims to achieve the global fairness in resource allocation among ground and aerial nodes [29]. Besides, different game-theoretical models are also developed, such as a coalition formation game model [27], a fuzzy payoffs game [28], and a stochastic game [29]. The game-theoretical approaches are promising tools to tackle the large-scale resource management problem in UAV networks, but it is still a challenge to map a multi-variable joint optimization problem into a game formulation.

Different from the literature mentioned above, many works focus on the development of approximation algorithms for the optimization of UAV deployment [31], [32], [33], [34]. In [31], [32], W. Xu et al. propose a constant factor approximation algorithm to search for the minimum number of UAVs deployed to find their data collection tours that can guarantee the information freshness. In [32], a similar approximation algorithm is presented to maximize the throughput of a multi-UAV network in a disaster area. Indeed, different variants of the constant factor approximation algorithm are applied to tackle the problem of collaborative data collection and fine-grained trajectory planning of multiple UAVs [33] and that of UAVsâ placement for directional coverage in a three-dimension space [34]. Nonetheless, the fundamental problem of multi-UAV cooperative trajectory planning to meet the spatially-temporally distributed demands of end-users is usually intractable due to its extremely large search space. Thus, some other works model a directed acyclic graph of a UAV-state transition diagram and transform the problem into a linear integer program that can be addressed by using an approximation algorithm [35]. [36] transforms the min-max problem into a dynamic program problem to minimize the worst-case deployment delay of UAVs. In this way, the optimal deployment solution for UAVs is obtained by using a polynomial-time approximation algorithm. In [37], the multi-user multiple-input-multiple-output (MU-MIMO) technique is considered in a UAV-enabled network, and a sensor-assisted channel prediction algorithm and a rate adaptation algorithm are combined to enhance the uplink throughput. In [38], UAV-to-UAV communications are integrated with UAV-tonetwork communications. The joint optimization of multi-UAV sub-channel allocations and speeds is decomposed into several subproblems, such that the subproblems are solved by using an iterative optimization algorithm. However, limited research efforts have been made on theoretically characterizing the UAV-assisted A2G transmission reliability, accounting for the A2G channel and application-layer requirement satisfaction. Few works consider optimizing the UAVâs mobility while properly scheduling data transmissions to improve energy utilization and communication reliability simultaneously.

## 3 SYSTEM MODEL AND PROBLEM FORMULATION

As shown in Fig. 1, we consider a UAV, denoted by U, that would like to transmit its massive sensor data to several ground base stations (BSs) in a heavily built-up on July 16,2024 at 03:12:15 UTC from IEEE Xplore. Restrictions apply.

urban environment.1 The set of BSs is denoted by . For Dcontrol modeling, we divide the time horizon into a series of slots, each with a duration of Dt seconds. $t \in \mathbb { Z } _ { + }$ 2is used to denote the index of time slots, where $Z _ { + }$ denotes the set of positive integers, i.e., $Z _ { + } = \{ 1 , 2 , 3 , . . . \}$ Ã¾ Â¼ f1 2 3 . . .gTo account for the transmission deadline and content integrity of an application, we introduce two parameters to characterize the application requirements, $\mid T$ and $Q .$ Here, T denotes the maximal number of time slots that can be exploited by the application to send its data. That is, the application transmission must be completed during T time slots. Q is the total application data to be offloaded from the UAV to the ground BSs during the limited time slots. The UAV needs to properly partition the whole Q-bit data into a sequence of smaller pieces and transmit each data piece in each time slot. Thus, a data transmission scheduling solution is represented by $\{ x ( t ) , t = 1 , 2 , . . . , T \}$ where $x ( t ) \geq 0$ denotes the data bits f Ã° Ã Â¼ 1 2 . . . g Ã° Ã  0to be sent in slot t and each scheduling solution should satisfy the integrity constraint, i.e., $\textstyle \sum _ { t = 1 } ^ { T } x ( t ) = Q$

## 3.1 UAV Mobility Model

The time-varying position of the UAV in time slot t is represented by a three-dimension Cartesian coordinate vector $\pmb { l } ( t ) = [ l _ { x } ( \dot { t } ) , l _ { y } ( t ) , l _ { z } ( t ) ] ^ { \mathrm { T } }$ , where x, y and z denote the longituÃ° Ã Â¼ Â½ Ã° Ã Ã° Ã Ã° Ãdinal, latitudinal and height components, respectively. The velocity and acceleration of the UAV are represented by v t and ${ \pmb a } ( t )$ , respectively. The bound constraints on ${ \pmb v } ( t )$ Ã° Ãand ${ \pmb a } ( t )$ Ã° Ãare denoted by $\mathcal { V } = [ \pmb { v } _ { \mathrm { m i n } } , \pmb { v } _ { \mathrm { m a x } } ]$ and $\begin{array} { r } { \pmb { \mathcal { A } } = [ \pmb { a } _ { \mathrm { m i n } } , \pmb { a } _ { \mathrm { m a x } } ] , } \end{array}$ Ã° Ãrespectively, where ${ \pmb v } _ { \mathrm { m i n } }$ Â¼ Â½ mand ${ \pmb v } _ { \mathrm { m a x } }$ ax A Â¼ Â½ min maxare the allowable minimin maxmum and maximum velocities of the UAV, and ${ \pmb a } _ { \mathrm { m i n } }$ and $\pmb { a } _ { \mathrm { m a x } }$ minare the minimum and maximum accelerations. We use maxa time-discrete second-order model to describe its mobility

$$
\left\{ \begin{array} { l l } { { \pmb l } ( t + 1 ) = { \pmb l } ( t ) + \Delta { \pmb \tau } { \pmb v } ( t ) + \frac { ( \Delta \tau ) ^ { 2 } } { 2 } { \pmb a } ( t ) ; } \\ { { \pmb v } ( t + 1 ) = { \pmb v } ( t ) + \Delta { \pmb \tau } { \pmb a } ( t ) } \end{array} \right. ,\tag{}
$$

for $t = 1 , 2 , \dots , T$ . In (1), we treat a t as the control input of Â¼ 1 2 . . . Ã° Ãthe UAV during its flight, which should be optimized to adapt the UAVâs mobility. Additionally, the motion state of the UAV at t can be represented by $\mathbf { \widetilde { \mathbf { s } } } ( t ) = \left[ l ( t ) , \pmb { v } ( t ) \right] ^ { \mathrm { T } }$ . The Ã° Ã Â¼ Â½ Ã° Ã Ã° Ãkinematic model of the UAV is rearranged into a state-space form as follows

$$
\pmb { \mathscr { s } } ( t + 1 ) = \pmb { A } \pmb { \mathscr { s } } ( t ) + \pmb { B } \pmb { \mathscr { a } } ( t ) ,\tag{}
$$

where A and B are the coefficient matrix of the state and of the control, respectively,

$$
A = \left[ \begin{array} { r r } { I _ { 3 \times 3 } } & { \Delta \tau I _ { 3 \times 3 } } \\ { \mathbf { 0 } _ { 3 \times 3 } } & { I _ { 3 \times 3 } } \end{array} \right] , B = \left[ \begin{array} { r r } { 0 . 5 \Delta \tau ^ { 2 } I _ { 3 \times 3 } } \\ { \Delta \tau I _ { 3 \times 3 } } \end{array} \right] ,\tag{}
$$

where $I _ { \mathrm { 3 } \times \mathrm { 3 } }$ denotes a $3 \times 3$ identity matrix while $\mathbf { 0 } _ { 3 \times 3 }$ is a $3 \times 3$ 33 3  3 033zero matrix. In reality, the UAV usually has a specific 3  3initial state and a terminal state as the boundary conditions on its trajectory. Let $\pmb { s } _ { 0 }$ and $\pmb { s } _ { f }$ be the initial and terminal 0states, respectively. We can present the boundary constraints by $\pmb { s } ( 1 ) = \pmb { s } _ { 0 }$ and $\pmb { \mathscr { s } } ( T + 1 ) = \pmb { \mathscr { s } } _ { f } ,$ . Additionally, we Ã°1Ã Â¼ 0 Ã° Ã¾ 1Ã Â¼can calculate the relative distance between the UAV and the base station in close proximity by

$$
d ( t ) = \operatorname* { m i n } _ { i \in \mathcal { D } } \lVert \pmb { l } ( t ) - \pmb { l } _ { \mathrm { B S } _ { i } } \rVert _ { 2 } ,\tag{}
$$

where $ { \boldsymbol { l } } _ { \mathrm { B S } _ { i } }$ is the position of the ith base station, $i \in \mathcal { D }$

3.2 A2G Channel and Transmission Reliability Model Similar to [3], we consider an orthogonal access channel for A2G transmissions and the data rate can be formulated by

$$
\pi ( t ) = \frac { B } { N } \mathrm { l o g } _ { 2 } \bigg \{ 1 + \frac { p ( t ) g _ { \mathrm { A 2 G } } ^ { 2 } ( t ) } { \sigma ^ { 2 } } \bigg \} ,\tag{}
$$

where B is the total available bandwidth, $p ( t )$ is the transmission power, and $\sigma ^ { 2 }$ Ã° Ãis the average noise power. $g _ { \mathrm { A 2 G } } ^ { 2 } ( t )$ A2GÃ° Ãdenotes the channel gain. N denotes the total number of users accessing the same channel at the same time.

According to the recent literature [39], [40], [41], Non-Line-of-Sight (NLoS) propagation usually dominates the channel in a heavily built-up urban area where there are many obstacles, such as high-rise buildings and trees, that can scatter the radio signal. In these situations, the channel fading can be well described by the Rayleigh distribution. In this study, we focus on the heavily built-up urban environment as the UAV deployment scenario and thus exploit the Rayleigh distribution to characterize the channel fading.2

<!-- image-->  
Fig. 1. A typical UAV-assisted A2G transmission network.

The random channel gain $g _ { \mathrm { A 2 G } } ^ { 2 } ( t )$ follows an exponential dis-A2tribution with the parameter $\mathbf { \mathcal { \hat { d } } } ^ { \beta } ( t )$ where $\beta$ is the path loss Ã° Ãexponent. Therefore, the probability that x t -bit data can be Ã° Ãsuccessfully transmitted by the UAV at time slot t can be formulated by [5]

$$
\mathrm { P r o b } \bigg \{ \pi ( t ) \geq \frac { x ( t ) } { \Delta \tau } \bigg \} = \exp \Bigg \{ - \frac { 2 ^ { \frac { x ( t ) N } { B \Delta \tau } } - 1 } { q ( t ) } d ^ { \beta } ( t ) \Bigg \} ,\tag{}
$$

where $q ( t ) = p ( t ) / \sigma ^ { 2 }$ denotes the normalized tranmission Ã° Ã Â¼ Ã° Ãpower. Let the upper and the lower bounds on the power be $p _ { \mathrm { m i n } }$ and $p _ { \mathrm { m a x } } ,$ respectively. The bound constraint for $q ( t )$ minis then $q ( t ) \in \mathcal { P } = [ \hat { p _ { \operatorname* { m i n } } } / \sigma ^ { 2 } , \hat { p _ { \operatorname* { m a x } } } / \sigma ^ { 2 } ]$ Ã° Ã. Now, we further define Ã° Ã 2 P Â¼ Â½ min max the A2G transmission reliability as the possibility that the UAV can successfully send the overall Q-bit data over T time slots, i.e., the success probability of transmission completion,

$$
R ( { \pmb q } , { \pmb a } , { \pmb x } ; N ) = \prod _ { t = 1 } ^ { T _ { \mathrm { A 2 G } } } \exp \left\{ - \frac { 2 ^ { \frac { x ( t ) N } { B \Delta \tau } } - 1 } { { \pmb q } ( t ) } { } d ^ { \beta } ( t ) \right\} ,\tag{}
$$

where for brevity we let the power control, the mobility control and the data transmission scheduling solutions be $\pmb q = [ q ( 1 ) , q ( 2 ) , \dots , q ( T ) ] ^ { \mathrm { T } } , \pmb a = [ \pmb a ( 1 ) , \pmb a ( 2 ) , \dots , \pmb a ( T ) ] ^ { \mathrm { T } }$ and ${ \pmb x } = [ x ( 1 ) , x ( 2 ) , \ldots , x ( T ) ] ^ { \mathrm { T } }$ Ã Â¼ Â½ Ã°1Ã, respectively.

Â¼ Â½ Ã°1Ã Ã°2Ã . . . Ã° ÃAdditionally, we take into account the random characteristics of the concurrent channel access. In other words, the number of channel users, $N ,$ is indeed a random variable, which can be modeled by using a Poisson point process like [47]. Let the average channel access number be n. The -probability of N users sharing the same channel can be

$$
f _ { N } ( n ) = \frac { \bar { n } ^ { n } } { n ! } \exp ( - \bar { n } ) .\tag{}
$$

Based on (8), we can further have the expected reliability as

$$
\bar { R } _ { \mathrm { U A V } } ( \pmb q , \pmb a , \pmb x ) = \sum _ { n = 1 } ^ { n _ { \operatorname* { m a x } } } f _ { N } ( n ) R ( \pmb q , \pmb a , \pmb x ; N = n ) ,\tag{}
$$

where $n _ { \mathrm { m a x } }$ denotes the allowed maximum number of chanmaxnel access users. It is remarked that the allowed maximum number of channel access users, $n _ { \mathrm { m a x } } ,$ is indeed a system maxparameter, which can be pre-specified according to the channel capacity. The channel access users can be mobile users on the ground who are allowed to share the same channel with the flying UAV.

## 3.3 Energy Consumption Model

The energy consumed by the UAV is mainly dominated by two parts, one of which is the motion energy consumption and the other is the communication energy consumption. According to [3], the motion energy consumption can be approximated by

$$
E _ { \mathrm { m o t } } ( t ) = \theta _ { 1 } \| \pmb { v } ( t ) \| ^ { 3 } + \frac { \theta _ { 2 } } { \| \pmb { v } ( t ) \| } \left( 1 + \frac { \| \pmb { a } ( t ) \| ^ { 2 } } { g ^ { 2 } } \right) ,\tag{}
$$

in which $\theta _ { 1 }$ and $\theta _ { 2 }$ are two constants about the aerodynam-1 2ics profile of the UAV. g represents the acceleration of gravity, which is $9 . 8 \mathrm { m } / \mathrm { s } ^ { 2 } .$ In addition, the communication 9 8 m senergy consumption is $E _ { \mathrm { t r a n s } } ( t ) = p ( t ) \Delta \tau$ . Thus, the overall transÃ° Ã Â¼ Ã° Ãenergy consumption of the UAV over the time slots is

$$
 { E _ { \mathrm { U A V } } } (  { \pmb q } ,  { \pmb a } ,  { \pmb x } ) = \sum _ { t = 1 } ^ { T _ { \mathrm { A 2 G } } } [ E _ { \mathrm { m o t } } ( t ) + E _ { \mathrm { t r a n s } } ( t ) ] .\tag{}
$$

## 3.4 Joint Optimization Model

In general, the acceleration control and transmission power of the UAV explicitly determine the overall energy consumption in mobility and communication. The data transmission scheduling of the UAV determines the success probability of data transmissions and should be adapted according to the temporal-spatial position information and transmission power of the UAV. Besides, the acceleration control and transmission power of the UAV can also affect the A2G transmission reliability since the channel quality is heavily dependent on the UAVâs mobility and transmission power. Therefore, energy utilization should allow for a communication reliability guarantee. We incorporate the A2G transmission reliability-oriented optimization into the optimization of UAV energy utilization. To jointly control the UAV mobility and transmission power meanwhile guaranteeing the A2G transmission reliability, we propose a bi-level optimal control model as follows

$$
\operatorname* { m i n } _ { \pmb { q } , \pmb { a } , \pmb { x } } \quad E _ { \mathrm { U A V } } ( \pmb { q } , \pmb { a } , \pmb { x } )\tag{12a}
$$

$$
\operatorname* { m a x } _ { \pmb q , \pmb a , \pmb x } \quad \bar { R } _ { \mathrm { U A V } } ( \pmb q , \pmb a , \pmb x )\tag{12b}
$$

$$
{ \mathrm { s . t . ~ } } \sum _ { t = 1 } ^ { T } x ( t ) = Q , \ x ( t ) \geq 0 , t = 1 , \ldots , T ;\tag{12c}
$$

$$
\pmb { \mathscr { s } } ( t + 1 ) = \pmb { A \mathscr { s } } ( t ) + \pmb { B \mathscr { a } } ( t ) , t = 1 , \ldots , T ;\tag{12d}
$$

$$
q ( t ) \in \mathcal { P } , \pmb { a } ( t ) \in \mathcal { A } , \pmb { v } ( t ) \in \mathcal { V } , t = 1 , \dots , T ;
$$

$$
\pmb { \mathscr { s } } ( 1 ) = \pmb { \mathscr { s } } _ { 0 } , \pmb { \mathscr { s } } ( T + 1 ) = \pmb { \mathscr { s } } _ { f } .\tag{12e}
$$

(12f)

In (12), the upper-level objective (12a) is to minimize the overall energy consumption while the lower-level (12b) aims to maximize the expected A2G transmission reliability. (12c) represents the constraint on the data transmission deadline and integrity. (12d) characterizes the kinematics of the UAV. (12e) and (12f) denote the bound and the terminal constraints, respectively. In general, it is difficult or even impossible to solve the bi-level model directly. Thus, in the following, we will further transform the bi-level model into a mathematically-tractable one and propose an efficient solving algorithm.

## 4 JOINT OPTIMIZATION METHOD

## 4.1 Model Transformation

Let the feasible region for data transmission scheduling be $\mathcal { X } = \{ \pmb { x } : \pmb { x } ^ { \mathrm { T } } \mathbf { 1 } = Q , \pmb { x } \geq 0 \}$ where denotes a column vector X Â¼ f : 1 Â¼  0g 1whose elements are all 1. When a and q are treated as exogenous parameters for the lower-level optimization model maximizing the reliability objective $\bar { R } _ { \mathrm { U A V } } ( \pmb q , \pmb a , \pmb x )$ with Urespect to x, we derive the following results

Given q and a, suppose that there exists an interior heorem 1.feasible optimal point ${ \pmb x } ^ { * } ( { \pmb q } , { \pmb a } ) \in \mathrm { i n t } ( { \pmb \chi } )$ such that

$$
\begin{array} { l } { { \displaystyle { \pmb x } ^ { * } ( { \pmb q } , { \pmb a } ) \in \arg \operatorname* { m a x } _ { { \pmb x } } \quad \bar { R } _ { \mathrm { U A V } } ( { \pmb q } , { \pmb a } , { \pmb x } ) } } \\ { { \displaystyle \qquad \mathrm { s . t . } \sum _ { t = 1 } ^ { T } x ( t ) = Q ; } } \\ { { \qquad \quad \qquad \quad { \ b x } ( t ) \geq 0 , t = 1 , \dots , T . } } \end{array}\tag{13}
$$

The optimal expected A2G transmission reliability under ${ \pmb x } ^ { * } ( { \pmb q } , { \pmb a } )$ can be expressed as follows

$$
\begin{array} { r l } & { \bar { R } _ { \mathrm { U A V } } ^ { * } ( \boldsymbol { q } , \boldsymbol { a } ) } \\ & { = \displaystyle \sum _ { n = 1 } ^ { n _ { \operatorname* { m a x } } } f _ { N } ( n ) \mathrm { e x p } \left\{ \frac { \sum _ { t = 1 } ^ { T } d ^ { \beta } ( t ) - T 2 ^ { \frac { n Q } { T B \Delta \tau } } \left( \prod _ { t = 1 } ^ { T } d ^ { \beta } ( t ) \right) ^ { \frac { 1 } { T } } } { q ( t ) } \right\} . } \end{array}\tag{14}
$$

In fact, given q and a, to solve an optimal data schedroof.uling solution ${ \pmb x } ^ { * } ( { \pmb q } , { \pmb a } )$ from (13) is equivalent to solving Ã° Ãthe following minimization problem for all n

$$
\begin{array} { l l } { \displaystyle \operatorname* { m i n } _ { \pmb { x } } } & { \displaystyle { F ( \pmb { x } ) } = \sum _ { t = 1 } ^ { T } d ^ { \beta } ( t ) 2 ^ { \frac { x ( t ) n } { B \Delta \tau } } } \\ { \mathrm { s . t . } } & { \pmb { x } \in \mathrm { i n t } ( \pmb { \chi } ) . } \end{array}\tag{15}
$$

From (15), we get the Lagrangian function with a set of Lagrangian multipliers $\lambda = \operatorname { c o l } \{ \lambda _ { t } \in \mathbb { R } _ { \geq 0 } , t = 1 , 2 , \ldots , T \}$ and $\mu \in \mathbb { R }$ as follows

$$
L ( \pmb { x } , \lambda , \mu ) = F ( \pmb { x } ) - \sum _ { t = 1 } ^ { T } \lambda _ { t } x ( t ) - \mu \left( \sum _ { t = 1 } ^ { T } x ( t ) - Q \right) .\tag{16}
$$

According to the well-known Karush-Kuhn-Tucker (KKT) conditions, the feasible optimal point ${ \pmb x } ^ { * } ( { \pmb q } , { \pmb a } )$ Ã° Ãmust satisfy the following first-order optimal condition (i.e., the gradient condition) and the complementary slackness

$$
\left\{ \begin{array} { l l } { \nabla _ { x ( t ) } F ( { \pmb x } ^ { * } ( { \pmb q } , { \pmb a } ) ) - \lambda _ { t } - \mu = 0 ; } \\ { \lambda _ { t } { \pmb x } ^ { * } ( t ) = 0 } \end{array} \right. ,\tag{}
$$

for $t = 1 , 2 , \dots , T ,$ where $x ^ { * } ( t )$ is the tth entity of ${ \pmb x } ^ { * } ( { \pmb q } , { \pmb a } )$ Â¼ 1Recalling $\pmb { x } ^ { * } ( \pmb { q } , \pmb { a } ) \in \mathrm { i n t } ( \pmb { \chi } ) , \mathrm { i . e . , } \ x ^ { * } ( t ) > 0 ,$ and $\lambda _ { t } \geq 0$ Ãfor all $t ,$ Ã° Ã 2 intÃ°X it can be seen that $\lambda _ { t }$ Ã° Ã 0must satisfy $\lambda _ { t } = 0$  0for all t. Â¼ 0Hence, we can further derive from the gradient condition

$$
\left\{ \begin{array} { l l } { \mu = \nabla _ { x ( t ) } F ( { \pmb x } ^ { * } ( { \pmb q } , { \pmb a } ) ) = d ^ { \beta } ( t ) 2 ^ { x ^ { * } ( t ) \kappa } \kappa \ln 2 } \\ { x ^ { * } ( t ) = \frac { 1 } { \kappa } ( \log _ { 2 } ( \mu ) - \log _ { 2 } ( d ^ { \beta } ( t ) ) - \log _ { 2 } ( \kappa \ln 2 ) ) } \end{array} \right. ,\tag{}
$$

for all $t ,$ where $\kappa = n / ( B \Delta \tau )$ . Substituting (18) into the equality constraint $\textstyle \sum _ { \prime = 1 } ^ { T } x ^ { * } ( t ) = Q \cos \operatorname { v i e l d }$

$$
x ^ { * } ( t ) = \frac { B \Delta \tau } { n } \left( \frac { \sum _ { t = 1 } ^ { T } \log _ { 2 } d ^ { \beta } ( t ) } { T } - \log _ { 2 } d ^ { \beta } ( t ) \right) + \frac { Q } { T } ,\tag{19}
$$

for all t. Finally, substituting (19) into the objective (9) can immediately obtain (14). Hence, the theorem is proven.

Besides, a higher transmission power q t can improve Ã° Ãthe reliability as indicated by (6). Thus, it is further observed that $\bar { R } _ { \mathrm { U A V } } ^ { * } ( \pmb q , \pmb a ) \leq \bar { R } _ { \mathrm { U A V } } ^ { * } ( \pmb q _ { \mathrm { m a x } } , \pmb a ) \leq \bar { R } _ { \mathrm { U A V } } ^ { * } ( \pmb q _ { \mathrm { m a x } } , \pmb a )$ where ${ \pmb q } _ { \mathrm { m a x } }$ UAVÃ° Ã  UAVÃ° max Ã  UAVÃ° max eÃ maxdenotes the upper bound of the transmission power solution q and a is a feasible optimal control obtained by

$$
\begin{array} { r l } & { \tilde { \pmb { a } } \in \displaystyle \operatorname* { m a x } _ { \pmb { a } } \quad \bar { R } _ { \mathrm { U A V } } ^ { * } ( \pmb { q } _ { \operatorname* { m a x } } , \pmb { a } ) } \\ & { \qquad \mathrm { s . t . } ~ \pmb { s } ( t + 1 ) = \pmb { A s } ( t ) + \pmb { B a } ( t ) , t = 1 , \ldots , T ; } \\ & { \qquad \ \pmb { a } ( t ) \in \mathcal { A } , \pmb { v } ( t ) \in \mathcal { V } , t = 1 , \ldots , T ; } \\ & { \qquad \ \pmb { s } ( 1 ) = \pmb { s } _ { 0 } , \pmb { s } ( T + 1 ) = \pmb { s } _ { f } . } \end{array}\tag{20}
$$

We treat $\bar { R } _ { \mathrm { U A V } } ^ { * } ( \pmb q _ { \mathrm { m a x } } , \widetilde { \pmb a } )$ as an upper bound on the expected UAVÃ° max ÃA2G transmission reliability objective. Motivated by the -constraint method, we can transform the bi-level optimization model (12) into the following optimal control model in which the expected A2G transmission reliability is bounded by $( 1 - \epsilon ) \bar { R } _ { \mathrm { U A V } } ^ { * } ( \pmb { q } _ { \mathrm { m a x } } , \widetilde { \pmb { a } } )$ where $\epsilon \in [ 0 , 1 ]$ is a paramÃ°1  Ã -UAVÃ° max eÃ 2 Â½0 1eter used to control the satisfaction of the trajectory-dependent reliability

$$
\begin{array} { r l } & { \displaystyle \operatorname* { m i n } _ { \boldsymbol { q } , \boldsymbol { a } , \boldsymbol { x } } E _ { \mathrm { U A V } } ( \boldsymbol { q } , \boldsymbol { a } , \boldsymbol { x } ) } \\ & { \mathrm { s . t . } \boldsymbol { x } ^ { \mathrm { T } } \mathbf { 1 } = \boldsymbol { Q } , \boldsymbol { x } \geq 0 ; } \\ & { \quad \quad \quad \bar { R } _ { \mathrm { U A V } } ( \boldsymbol { q } , \boldsymbol { a } , \boldsymbol { x } ) \geq ( 1 - \epsilon ) \bar { R } _ { \mathrm { U A V } } ^ { * } ( q _ { \operatorname* { m a x } } , \widetilde { \boldsymbol { a } } ) ; } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \boldsymbol { q } ( t ) \in \mathcal { P } , \boldsymbol { a } ( t ) \in \mathcal { A } , \boldsymbol { v } ( t ) \in \mathcal { V } , t = 1 , \dots , T ; } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \end{array}\tag{21}
$$

From (21), we further have the following results:

A feasible solution of the -constraint model (21) is emma 1.weakly Pareto-optimal and this feasible solution is Pareto-optimal if and only if it is a unique feasible solution.

The results follow the theorems presented in [48] (see roof.Chapter 3.2 of [48]) and can be proven by mathematical contradiction and the concept of Pareto optimality. â¡

We remark that Lemma 1 ensures the Pareto-optimality of a feasible solution to the proposed model (21) above. However, due to the complexity of the model that has a non-convex optimization objective function and a non-convex nonlinear constraint, it is challenging to obtain a feasible solution of the model by using standard convex optimization techniques directly. Moreover, it is usually difficult or even impossible to search a global optimizer of a non-convex nonlinear optimization problem, and thus many recent works exploit a successive convex approximation technique to obtain a local optimal solution [3], [9], [12], [16]. In the following, building upon the -constraint method above, we proceed to develop a novel solving algorithm to search a feasible local optima efficiently.

## 4.2 Solving Algorithm Design

The obtained optimal control model (21) only involves one optimization objective and thus allows us to design an efficient solving algorithm. To deal with the mixed linear and nonlinear constraints and the strongly non-convex objective function in (21), we propose an iterative numerical optimization algorithm by combining a direct multi-shooting method and a successive quadratic programming (SQP) technique. Specifically, the kinematic states of the UAV at different time slots, $\{ \pmb { s } ( t ) , t = 2 , 3 , \ldots , T + 1 \}$ , are also treated as decision f Ã° Ã Â¼ 2 3 . . . Ã¾ 1gvariables and incorporated into the optimization process. We introduce an augmented optimization variable set as w $\operatorname { c o l } \{ \pmb q , \pmb { a } , \pmb { x } , \pmb { s } \}$ where $\pmb { \mathscr { s } } = \mathrm { c o l } \{ \pmb { \mathscr { s } } ( t ) , t = 2 , 3 , \ldots , T + 1 \}$ Â¼and lift colf g Â¼ colf Ã° Ã Â¼ 2 3 . . . Ã¾ 1gthe problem to a higher dimension that is sparsely structured and usually improves convergence. We denote the global optimization objective in (21) by $E _ { \mathrm { U A V } } ( \pmb { w } ) = E _ { \mathrm { U A V } } ( \pmb { q } , \pmb { a } , \pmb { x } )$ . UAVÃ°Furthermore, we define a column vector $\pmb { G } ( \pmb { w } )$ UAVÃ° Ãconsisting of all the equality constraints in (21) as

$$
\pmb { G } ( \pmb { w } ) = \mathrm { c o l } \left\{ \begin{array} { l l } { \pmb { x } ^ { \mathrm { T } } \mathbf { 1 } - \pmb { Q } ; } \\ { \pmb { s } ( 1 ) - \pmb { s } _ { 0 } ; } \\ { \pmb { s } ( T + 1 ) - \pmb { s } _ { f } ; } \\ { \pmb { s } ( t + 1 ) - \pmb { A } \pmb { s } ( t ) + \pmb { B } \pmb { a } ( t ) , t = 1 , \dots , T } \end{array} \right\} ,\tag{22}
$$

and a column vector $\mathbf { \nabla } I ( \mathbf { \boldsymbol { w } } )$ lumping all the inequality constraints in (21) as

$$
\begin{array} { r } { I ( \pmb { w } ) = \mathrm { c o l } \left\{ \begin{array} { l l } { \bar { R } _ { \mathrm { U A V } } ( \pmb { q } , \pmb { a } , \pmb { x } ) - ( 1 - \epsilon ) \bar { R } _ { \mathrm { U A V } } ^ { * } ( \pmb { q } _ { \mathrm { m a x } } , \widetilde { \pmb { a } } ) ; } \\ { \pmb { u } - \pmb { u } _ { \mathrm { m i n } } ; } \\ { \pmb { u } _ { \mathrm { m a x } } - \pmb { u } ; } \\ { \pmb { x } } \end{array} \right\} , } \end{array}\tag{23}
$$

where let $\pmb { \upsilon } = \mathrm { c o l } \{ \pmb { v } ( t ) , t = 1 , 2 , . . . , T \}$ and $\pmb { u } = \mathrm { c o l } \{ \pmb { q } , \pmb { a } , \pmb { v } \}$ Â¼for simplicity. ${ \pmb u } _ { \mathrm { m i n } }$ Ã° Ãand $\pmb { u } _ { \mathrm { m a x } }$ 2 . . . g Â¼ colf gare the lower and the upper bounds on ${ \pmb u } ,$ min max respectively, which can be constructed by combining $\mathcal { P } , A$ and . Let the index sets of $\pmb { G } ( \pmb { w } )$ and $\pmb { I } ( \pmb { w } )$ be and $\mathcal { T } ,$ P A V Ã° Ã Ã° Ã respectively. We denote the lth component of $\pmb { G } ( \pmb { w } )$ Iand $\pmb { I } ( \pmb { w } )$ by $\dot { G _ { l } } ( \pmb { w } )$ and $I _ { l } ( { \pmb w } )$ , respectively. The Ã° Ã Ã° Ã Ã° Ã Ã° ÃLagrangian function of (21) can be formulated as follows

$$
\mathcal { L } ( \pmb { w } , \pmb { \phi } ) = E _ { \mathrm { U A V } } ( \pmb { w } ) - \sum _ { l \in \mathcal { G } } \phi _ { l } G _ { l } ( \pmb { w } ) - \sum _ { l \in \mathcal { T } } \phi _ { l } I _ { l } ( \pmb { w } ) ,\tag{}
$$

where f is a column vector collecting Lagrangian multipliers, ${ \mathrm { , i . e . , } } \phi = \mathrm { c o l } \{ \phi _ { l } \in \mathbb { R } , l \in { \mathcal { G } } ; \phi _ { l ^ { \prime } } \in \mathbb { R } _ { \ge 0 } , l ^ { \prime } \in { \mathcal { T } } \}$

Â¼ colf 2 2 G; 0 2 0 2 IgNow, using (24), we can design a numerical iterative algorithm inspired by sequential quadratic programming, which generate a sequence of feasible iterations $\{ \pmb { w } _ { k } , k =$ $0 , 1 , \ldots \}$ f Â¼to approach a locally optimal solution to (21). To be 0 1 . . .gspecific, given a feasible solution to (21) and the Lagrangian multipliers at an iteration k, wk and $\phi _ { k } .$ , we can establish a quadratic programming subproblem to obtain an optimal search direction $\Delta { \pmb w } _ { k }$ and a set of new Lagrangian multipliers $\pmb { \phi } _ { k + 1 }$

$$
\begin{array} { c } { \displaystyle \operatorname* { m i n } _ { \Delta { \pmb w } } \quad \nabla E _ { \mathrm { U A V } } ( { \pmb w } _ { k } ) ^ { \mathrm { T } } \Delta { \pmb w } + \displaystyle \frac { 1 } { 2 } \Delta { \pmb w } ^ { \mathrm { T } } { \pmb H } _ { k } \Delta { \pmb w } } \\ { \mathrm { s . t . } G _ { l } ( { \pmb w } _ { k } ) + \nabla G _ { l } ( { \pmb w } _ { k } ) ^ { \mathrm { T } } \Delta { \pmb w } = 0 , \forall l \in { \mathcal G } ; } \\ { I _ { l } ( { \pmb w } _ { k } ) + \nabla I _ { l } ( { \pmb w } _ { k } ) ^ { \mathrm { T } } \Delta { \pmb w } \geq 0 , \forall l \in { \mathcal T } , } \end{array}\tag{25}
$$

where $\pmb { H } _ { k }$ denotes the positive-definite quasi-Newton approximation of the Hessian matrix of $\mathcal { L } ( \pmb { w } , \pmb { \phi } )$ . Solving the Authorized licensed use limited to:Beijing Normal University.Downloade

subproblem (25) to get a feasible descent direction $\Delta { \pmb w } _ { k }$ and $\pmb { \phi } _ { k + 1 } ,$ , we can construct a new iteration by

$$
\pmb { w } _ { k + 1 } = \pmb { w } _ { k } + \alpha _ { k } \Delta \pmb { w } _ { k } ,\tag{}
$$

where $\alpha _ { k }$ denotes the search step size that can be obtained by using a line search approach. For instance, we can get an optimal step size by $\alpha _ { k } \in \mathrm { a r g m i n } _ { \alpha } \{ \Phi ( \pmb { w } _ { k } + \alpha \Delta \pmb { w } _ { k } , \pmb { \mu } _ { k } ) \}$ , where $\Phi ( w , \bar { \pmb { \mu } } )$ 2 argmin f Ã°is an â -type merit function like

$$
\begin{array} { r } { \Phi ( \pmb { w } , \pmb { \mu } ) = E _ { \mathrm { U A V } } ( \pmb { w } ) + \displaystyle \sum _ { l \in \mathcal { G } } \mu _ { l } \lvert G _ { l } ( \pmb { w } ) \rvert } \\ { + \displaystyle \sum _ { l \in \mathcal { T } } \mu _ { l } \mathrm { m a x } \{ 0 , - I _ { l } ( \pmb { w } ) \} , } \end{array}\tag{27}
$$

in which $\pmb { \mu } = \mathrm { c o l } \{ \mu _ { l } \in \mathbb { R } _ { \ge 0 } , \forall l \in \mathcal { G } \cup \mathcal { T } \}$ is a column vector Â¼ colf 2 0 8 2 G [ Igconsisting of nonnegative penalty coefficients. Given $\phi _ { k } ,$ these penalty factors are adapted at each time slot k according to

$$
\mu _ { l , k } = \left\{ \begin{array} { l l } { \displaystyle \big | \phi _ { l , k } \big | , k = 1 ; } \\ { \operatorname* { m a x } \bigg \{ \big | \phi _ { l , k } \big | , \frac { \big | \mu _ { l , k - 1 } \big | + \big | \phi _ { l , k } \big | } { 2 } \bigg \} , k \geq 2 ; } \end{array} \right.\tag{}
$$

where $\mu _ { l , k }$ and $\phi _ { l , k }$ are the lth element of $\pmb { \mu } _ { k }$ and $\phi _ { k }$ at time slot $k ,$ respectively. (28) can guarantee that $| \phi _ { l , k } | \le \mu _ { l , k }$ is j j always held for all k and Dwk is also a decreasing direction of $\Phi ( { \pmb w } , { \pmb \mu } )$ [7]. Besides, we let $\pmb { y } _ { k } = \nabla \mathcal { L } ( \pmb { w } _ { k + 1 } , \pmb { \phi } _ { k + 1 } )$ $\nabla \mathcal { L } ( \pmb { w } _ { k } , \pmb { \phi } _ { k + 1 } )$ Â¼ rLÃ° Ã¾1 Ã¾. To guarantee the positive definiteness of $\pmb { H } _ { k } ,$ rLÃ° Ã¾1Ãwe adopt a modified Broyden-Fletcher-Goldfarb-Shanno (BFGS) formula to update $\pmb { H } _ { k }$ . To be specific, we introduce a weight $\delta \in [ 0 , 1 ]$ as follows

$$
\begin{array} { r } { \boldsymbol \delta = \left\{ \begin{array} { l l } { \boldsymbol 1 , \pmb { y } _ { k } ^ { \mathrm { T } } \Delta \pmb { w } _ { k } \geq \theta \Delta \pmb { w } _ { k } ^ { \mathrm { T } } \pmb { H } _ { k } \Delta \pmb { w } _ { k } ; } \\ { \frac { ( 1 - \theta ) \Delta \pmb { w } _ { k } ^ { \mathrm { T } } \pmb { H } _ { k } \Delta \pmb { w } _ { k } } { \Delta \pmb { w } _ { k } ^ { \mathrm { T } } \pmb { H } _ { k } \Delta \pmb { w } _ { k } - \pmb { y } _ { k } ^ { \mathrm { T } } \Delta \pmb { w } _ { k } } , \quad \mathrm { o t h e r w i s e } , } \end{array} \right. } \end{array}\tag{}
$$

where $\theta \in ( 0 , 1 )$ and u is usually set to 0.2. Thus, let $z _ { k } =$ $\begin{array} { r } { \delta \pmb { y } _ { k } + ( 1 - \delta ) \pmb { H } _ { k } \Delta \pmb { w } _ { k } } \end{array}$ . The matrix $\pmb { H } _ { k }$ can be updated by

$$
\pmb { H } _ { k + 1 } = \pmb { H } _ { k } - \frac { \pmb { H } _ { k } \Delta \pmb { w } _ { k } \Delta \pmb { w } _ { k } ^ { \mathrm { T } } \pmb { H } _ { k } } { \Delta \pmb { w } _ { k } ^ { \mathrm { T } } \pmb { H } _ { k } \Delta \pmb { w } _ { k } } + \frac { z _ { k } z _ { k } ^ { \mathrm { T } } } { z _ { k } ^ { \mathrm { T } } \Delta \pmb { w } _ { k } } .\tag{}
$$

Based on (25) to (30), we propose our solving algorithm as summarized in Algorithm 1. The algorithm consists of three main steps, i.e., solving $( \Delta { \pmb w } _ { k } , \pmb { \phi } _ { k + 1 } )$ by quadratic programÃ° Ã¾1Ãming, performing line search to get an optimal step size $\alpha _ { k } ,$ and updating the Hessian matrix $H _ { k } .$ The overall algorithm approaches the solution to the original optimal control model (21) by transforming it into a series of simpler quadratic programming (QP) subproblems (25). It is remarked that since there already exist many efficient QP algorithms, Algorithm 1 can leverage any advanced QP algorithms $( \mathrm { e . g . , }$ the well-known interior-point method and active set method) for the practical implementation.

## 4.3 Algorithm Convergence Analysis

Using the first-order optimality theory and inequality analysis, we show the guaranteed convergence of Algorithm 1 to a Karush-Kuhn-Tucker (KKT) point as follows.

$$
\{ \pmb { w } _ { k } \}
$$

Iterative Optimization Algorithm   
A numerical tolerance $0 < \xi \ll 1$ and a feasible initial   
guess w and $H _ { 0 }$   
0 0Optimal joint solution ${ \pmb w } _ { k }$   
R1: $k \gets 0 ;$   
2: repeat   
3: epeat Solve (25) to get $( \Delta { \pmb w } _ { k } , \pmb \phi _ { k + 1 } ) ;$   
4: Solve (27) to get $\alpha _ { k } ;$   
5: Set $\pmb { w } _ { k + 1 } = \pmb { w } _ { k } + \alpha _ { k } \Delta \pmb { w } _ { k } ;$   
6: Ã¾1 Â¼ Ã¾ Update Hk by (30);   
7: $k \gets k + 1$   
8: until $\left\| \nabla \mathcal { L } ( \pmb { w } _ { k } , \pmb { \phi } _ { k } ) \right\| \leq \xi$

In the first case, we have $\Delta { \pmb w } _ { k } = { \pmb 0 }$ at a certain iteraroof. Â¼ 0tion k. Thus, the KKT conditions of (25), i.e.,

$$
\left\{ \begin{array} { l l } { \nabla E _ { \mathrm { U A V } } ( { \pmb w } _ { k } ) + \pmb { H } _ { k } \Delta { \pmb w } _ { k } } \\ { \quad - \sum _ { l \in \mathcal { G } } \phi _ { l , k } G _ { l } ( { \pmb w } _ { k } ) - \sum _ { l \in \mathcal { T } } \phi _ { l , k } I _ { l } ( { \pmb w } _ { k } ) = \bf 0 ; } \\ { G _ { l } ( { \pmb w } _ { k } ) + \nabla G _ { l } ( { \pmb w } _ { k } ) ^ { \mathrm { T } } \Delta { \pmb w } _ { k } = 0 , l \in \mathcal { G } ; } \\ { \phi _ { l , k } \geq 0 , \ I _ { l } ( { \pmb w } _ { k } ) + \nabla I _ { l } ( { \pmb w } _ { k } ) ^ { \mathrm { T } } \Delta { \pmb w } _ { k } \geq 0 , l \in \mathcal { T } ; } \\ { \phi _ { l , k } \Big ( I _ { l } ( { \pmb w } _ { k } ) + \nabla I _ { l } ( { \pmb w } _ { k } ) ^ { \mathrm { T } } \Delta { \pmb w } _ { k } \Big ) = 0 , l \in \mathcal { T } , } \end{array} \right.\tag{}
$$

are equivalent to those of the original problem (21). Hence, ${ \pmb w } _ { k }$ is a KKT point of (21) in the case of $\Delta { w _ { k } } = 0$

In the other case where $\Delta { w } _ { k } \neq 0$ for every $k , ~ \{ \pmb { w } _ { k } \}$ 6Â¼ 0 f gbecomes an infinite sequence that has an accumulation point. We let $\pmb { w } ^ { * }$ denote the accumulation point. Additionally, $\pmb { H } _ { k }$ is a positive-definite matrix. $\nabla E _ { \mathrm { U A V } } ( \pmb { w } _ { k } )$ , $\nabla G _ { l } ( \pmb { w } _ { k } )$ and $\nabla I _ { l } ( \pmb { w } _ { k } )$ r UAVÃ° Ãfor all l and k are continuous funcr Ã°tions of ${ \pmb w } _ { k } .$ r Ã° Ã. Hence, as $\Delta { \pmb w } _ { k }$ satisfies the KKT conditions as in (31), it also has an accumulation point. Let the accumulation point of $\Delta { \pmb w } _ { k }$ be $\Delta { w } ^ { * }$ . Now, we prove by contradiction that such an accumulation point $\Delta \dot { w } ^ { * }$ must be $\Delta { w } ^ { * } = 0$ such that the accumulation point $\pmb { w } ^ { * }$ is a KKT Â¼point.

Suppose $\Delta { \pmb w } _ { k } \neq { \pmb 0 }$ . There is an $\bar { \alpha } > 0$ such that

$$
\Phi ( { \pmb w } ^ { * } + \bar { \alpha } \Delta { \pmb w } ^ { * } , { \pmb \mu } ) = \operatorname* { m i n } _ { \alpha \in \mathrm { R } _ { \geq 0 } } \Phi ( { \pmb w } ^ { * } + \alpha \Delta { \pmb w } ^ { * } , { \pmb \mu } ) .\tag{}
$$

As $\Delta { w } ^ { * }$ is a decreasing direction of $\Phi ( { \pmb w } ^ { * } , { \pmb \mu } )$ and $\bar { \alpha } > 0 ,$ we can further have

$$
\Phi ( { \pmb w } ^ { * } + \bar { \alpha } \Delta { \pmb w } ^ { * } , { \pmb \mu } ) < \Phi ( { \pmb w } ^ { * } , { \pmb \mu } ) .\tag{}
$$

Thus, letting $\Delta \Phi = \Phi ( { \pmb w } ^ { * } , { \pmb \mu } ) - \Phi ( { \pmb w } ^ { * } + \bar { \alpha } \Delta { \pmb w } ^ { * } , { \pmb \mu } ) > 0$ and according to $\pmb { w } _ { k } + \bar { \alpha } \Delta \pmb { w } _ { k }  \pmb { w } ^ { * } + \bar { \alpha } \Delta \pmb { w } ^ { * }$ -under $k  \infty ,$ , we Ã¾ - !yield the following inequality

$$
\Phi ( { \pmb w } _ { k } + \bar { \alpha } \Delta { \pmb w } _ { k } , { \pmb \mu } ) + \frac { \Delta \Phi } { 2 } < \Phi ( { \pmb w } ^ { \ast } , { \pmb \mu } ) ,\tag{}
$$

for a sufficiently large k.

On the other side, the line search for a step length at each $k , \alpha _ { k } ,$ guarantees that a sequence $\{ \zeta _ { k } \ge \bar { 0 } \}$ exists to make

$\Phi ( { \pmb w } _ { k } + \alpha _ { k } \Delta { \pmb w } _ { k } , { \pmb \mu } ) \leq \operatorname* { m i n } _ { - \infty } \ \Phi ( { \pmb w } _ { k } + \alpha \Delta { \pmb w } _ { k } , { \pmb \mu } ) + \zeta _ { k } ,$ (35) mina R where $\begin{array} { r } { \sum _ { k = 1 } ^ { \infty } \zeta _ { k } < + \infty , } \end{array}$ 2 0and $\textstyle \sum _ { i = k } ^ { \infty } \zeta _ { i } < \Delta \Phi / 2$ when k is Â¼1 Ã¾1sufficiently large. (35) implies

$$
\Phi ( \pmb { w } _ { k + 1 } , \pmb { \mu } ) \leq \Phi ( \pmb { w } _ { k } , \pmb { \mu } ) + \zeta _ { k } ,\tag{}
$$

for all k. Combining the results above, we derive

$$
\begin{array} { l } { \displaystyle \Phi ( { \pmb w } ^ { * } , { \pmb \mu } ) \leq \Phi ( { \pmb w } _ { k + 1 } , { \pmb \mu } ) + \sum _ { i = k + 1 } ^ { \infty } \zeta _ { i } } \\ { \displaystyle \qquad \leq \operatorname* { m i n } _ { \alpha \in \mathbb { R } _ { \geq 0 } } \Phi ( { \pmb w } _ { k } + \alpha \Delta { \pmb w } _ { k } , { \pmb \mu } ) + \zeta _ { k } + \sum _ { i = k + 1 } ^ { \infty } \zeta _ { i } } \\ { \displaystyle \qquad < \Phi ( { \pmb w } _ { k } + \bar { \alpha } \Delta { \pmb w } _ { k } , { \pmb \mu } ) + \frac { \Delta \Phi } { 2 } . } \end{array}\tag{37}
$$

It is seen that (37) is contradictory to (34). Such a contradiction implies that the hypothesis $\Delta { w } ^ { * } \neq 0$ is not true. In summary, $\pmb { w } ^ { * }$ 6Â¼ 0is also a KKT point of (21) in the case of $\Delta { w } ^ { \ast } = 0 .$ â¡

Theorem 2 provides an insight into the guaranteed convergence of the proposed algorithm to a KKT point. However, we remark that this result does not mean that the proposed algorithm is guaranteed to converge to a global optimal point. That is, the KKT point of the problem model, i.e., (21), can be a local optimal point or a global point since it is a non-convex optimization problem. In general, nonconvex optimization is at least NP-hard, so it is challenging to obtain a global optimal point of a non-convex problem. Additionally, theoretical guarantees of the global optimality of an algorithm are usually weak or even non-existent.3 At this point, our proposed algorithm can only guarantee the local optimality rather than the global optimality here.

## 4.4 Algorithm Complexity Analysis

From Algorithm 1, the computational complexity consists of two parts, including the convex quadratic programing and the line search. The line search only involves a one-dimension decision variable $\alpha _ { k }$ and the complexity of the line search with the accuracy of  is ${ \mathcal { O } } ( \ln \xi ^ { - 1 } )$ . Note that the total size of the decision variables $q ( t ) , \mathbf { \delta } \mathbf { a } ( t )$ Ãand $x ( t )$ at a time slot t is $n _ { \mathrm { v a r } } = 1 + 3 + 1 = 5$ Ã° Ã Ã° Ã Ã° Ãand that of the kinematic state $\pmb { s } ( t )$ is $n _ { \mathrm { s t a t e } } = 3 \times 2 = 6$ Â¼ 5 Ã° Ã. Thus, the total length of the augmented state Â¼ 3  2 Â¼ 6optimization variables w is $T ( n _ { \mathrm { v a r } } + n _ { \mathrm { s t a t e } } )$ . We can adopt the Ã° var Ã¾ stateÃwell-known interior-point method to solve the QP subproblem, which will require the number of iterations in the order of $\mathcal { O } ( \sqrt { T ( n _ { \mathrm { v a r } } + \hat { n _ { \mathrm { s t a t e } } } ) } \ln \xi ^ { - 1 } )$ for convergence with the

3. In mathematical optimization, the KKT conditions are known as the local optimality conditions. Some researchers have provided global optimality conditions for some special optimization problems that have special mathematical structures, such as weakly convex minimization problems [49] and bivalent non-convex quadratic programs [50]. However, it is difficult or even impossible to derive global optimality conditions for a general non-convex optimization problem [51]. In this work, our targeted problem does not fall into the special class of global optimality-guaranteed problems. It remains an open question to obtain a global optimal solution to the joint optimization model (21). Some advanced heuristic mechanisms or stochastic multi-start search techniques, such as simulated annealing and particle swarm optimization, may be integrated with the proposed optimization method in this work to find a global optimum. Here we left the design of a global optimization algorithm as our future work.

TABLE 1 Parameter Settings
<table><tr><td>Symbol</td><td>Value</td></tr><tr><td> $\boldsymbol { l } _ { \mathrm { B S _ { 1 } } } , \boldsymbol { l } _ { \mathrm { B S _ { 2 } } }$ </td><td> $\overline { { [ 8 0 , 4 0 , 0 ] ^ { \mathrm { T } } \mathrm { m } , [ 1 6 0 , - 3 0 , 0 ] ^ { \mathrm { T } } \mathrm { m } } }$ </td></tr><tr><td> $\boldsymbol { l } _ { \mathrm { B S } _ { 3 } } , \boldsymbol { l } _ { \mathrm { B S } _ { 4 } }$ </td><td> $[ 2 4 0 , 3 0 , 0 ] ^ { \mathrm { T } } \mathrm { m } , [ 3 2 0 , - 4 0 , 0 ] ^ { \mathrm { T } } \mathrm { m }$ </td></tr><tr><td> $B , \sigma ^ { 2 } , \beta , \bar { n }$ </td><td> $1 0 \mathrm { M H z } , - 9 5 \mathrm { d B m } , 2 . 7 5 , 1 3 9$ </td></tr><tr><td> $\theta _ { 1 } , \theta _ { 2 } , \xi$ </td><td> $9 . 2 6 \times 1 0 ^ { - 4 } , 2 2 5 0 , 1 \times 1 0 ^ { - 3 }$ </td></tr><tr><td> $p _ { \operatorname* { m i n } } , p _ { \operatorname* { m a x } }$ </td><td> $- 2 3 \mathrm { d B m , 2 3 \mathrm { d B m } }$ </td></tr><tr><td> $v _ { \mathrm { m i n } } , v _ { \mathrm { m a x } }$ </td><td> $[ - 2 0 , - 2 0 , 0 ] ^ { \mathrm { T } } \mathrm { m } / \mathrm { s } , [ 2 0 , 2 0 , 0 ] ^ { \mathrm { T } } \mathrm { m } / \mathrm { s }$ </td></tr><tr><td> $a _ { \mathrm { m i n } } , a _ { \mathrm { m a x } }$ </td><td> $[ - 3 0 , - 3 0 , 0 ] ^ { \mathrm { T } } \mathrm { m } / \mathrm { s } ^ { 2 } , [ 3 0 , 3 0 , 0 ] ^ { \mathrm { T } } \mathrm { m } / \mathrm { s } ^ { 2 }$ </td></tr></table>

accuracy  [52]. Besides, the arithmetic complexity of each iteration is $\mathcal { O } ( T ^ { 3 } ( n _ { \mathrm { v a r } } + n _ { \mathrm { s t a t e } } ) ^ { 3 } )$ [52]. Therefore, the computa-OÃ° Ã° var Ã¾ stateÃ Ãtional complexity of the convex quadratic programing is $\mathcal { O } ( T ^ { 3 . 5 } ( n _ { \mathrm { v a r } } ^ { } + n _ { \mathrm { s t a t e } } ^ { } ) ^ { 3 . 5 } \ln \xi ^ { - 1 } )$ . Besides, the complexity of the OÃ° Ã° var Ã¾ stateÃdescent iterations with ${ \pmb w } _ { k }$ is $\mathcal { O } ( \ln \xi ^ { - 1 } )$ regarding the accuracy OÃ°ln Ãof . Hence, the total computational complexity of Algorithm 1 is $\mathcal { O } ( T ^ { 3 . 5 } ( n _ { \mathrm { v a r } } + n _ { \mathrm { s t a t e } } ) ^ { 3 . 5 } \ln ^ { 2 } \xi ^ { - 1 } )$ , which can be handled in OÃ° Ã° var Ã¾ stateÃ lnthe order of polynomial time.

## 5 SIMULATION EVALUATION

## 5.1 Parameter Setting

In this section, we conduct simulations to evaluate the performance of our proposed method. We consider that there are several base stations on the ground and these base stations are placed along a road. Following many existing studies [1], [2], [3], [10], [11], [14], [16], [17], [46], we consider to fix the flight height of the simulated UAV at a constant altitude for the sake of demonstration, i.e., $l _ { z } ( t ) = 5 0 \mathrm { m }$ for all $t ,$ Ã° Ã Â¼ 50 msuch that the mobility control is operated in a twodimension plane. We remark that a similar simulation scenario has also been adopted in the recent literature such as [16], [42], [46], since it is reasonable enough to observe the performance variation of the UAV-assisted network in such simulation scenario. Following [46], the number of the base stations on the ground is set to 4. In addition, the initial and the terminal kinematic states of the UAV are specified as $\pmb { \mathscr { s } } _ { 0 } = \left[ 0 , 0 , 5 0 , 1 , 1 , 0 \right] ^ { \mathrm { T } }$ and $\pmb { \mathscr { s } } _ { f } = \left[ 4 0 0 , 0 , 5 0 , 0 , 1 , 0 \right] ^ { \mathrm { T } }$ , respec-0 Â¼ Â½0 0 50 1 1 0 Â¼ Â½400 0 50 0 1 0tively. The application data volume is , and the time 30 Mbithorizon for A2G data transmissions is limited within ; . The time slot is set to $\Delta \tau = 0 . 5$ such that the avail-Â½0 30 sable slot number is $T = 6 0$ Â¼ 0 5 s. According to the 3GPP Release-Â¼ 6015 study on the enhanced LTE technology for UAVs [53], a carrier frequency of with bandwidth can be 2 GHz 10 MHzadopted for low-altitude UAVs in urban crowded areas. The same bandwidth setting is also adopted in the simulation study of the recent literature such as [54]. Without special statement, we use the parameters summarized in Table 1 throughout our simulation experiments.

## 5.2 Algorithm Validation

Figs. 2 and 3 show the convergence of our proposed algorithm under different . As can be seen from Fig. 2, the optimization objective function can converge after about 100 iterations. Fig. 3 shows that the first-order measure of the Lagrangian function arrives at a near-zero level finally. These results indicate that the algorithm cony erges toalocal optimum. Fig. 4 shows the optimal trajectories with different . It is found that a smaller  leads to a trajectory closer to the base stations. The underlying reason is that reducing  results in a much higher requirement on the transmission reliability and that the UAV needs to reduce the transmission distance to satisfy the reliability requirement. Fig. 5 shows the energy consumption and the transmission reliability. We can see that increasing  reduces the transmission reliability since the UAV tends to follow a straight trajectory when the reliability restriction becomes lower. In this way, the energy consumption related to the UAV motion is reduced.

<!-- image-->  
Fig. 2. The convergence of the objective function.

In Fig. 6, we compare the optimal trajectories under different  in a more complicated scenario to further validate our algorithm. In this complicated scenario, we consider that there exist eight base stations that are distributed within a region irregularly. A similar result 400 m  400 mcan also be observed that reducing  can drive the UAV to fly closer to the base stations. This is because the UAV with a smaller  needs to satisfy a higher A2G transmission reliability. The -reliability constraint can be met by reducing its relative distance to the base stations. Fig. 7 shows the convergence of the energy consumption function in this complicated scenario. It is seen that the objective function is decreasing and converges to a stationary point after about

<!-- image-->  
Fig. 3. The convergence of the first-order measure of the Lagrangian function.

<!-- image-->  
Fig. 4. The optimal trajectories under different .

<!-- image-->

<!-- image-->  
Fig. 5. The bi-objective performance under different .

<!-- image-->  
Fig. 6. The optimal trajectories in a scenario where more base stations are considered.

600 iterations. To examine the local optimality of the stationary point the objective function arrives at, we illustrate the first-order measure of the corresponding Lagrangian function in Fig. 8. It is observed that the first-order measure of the Lagrangian function converges to zero after about 600 iterations. Hence, the algorithm has obtained a local optimal point that satisfies the KKT conditions. Combining the above figures we can see that the prosed algorithm can decrease the energy consumption and guarantee the convergence to a local optimum.

<!-- image-->  
Fig. 7. The convergence of the objective function in a scenario where more base stations are considered.

<!-- image-->  
Fig. 8. The convergence of the first-order measure of the Lagrangian function in a scenario where more base stations are considered.

## 5.3 Performance Comparison

We further compare our joint optimization method (marked by âJOMâ) with several other conventional methods, including an averaged data transmission method (âADTâ), a max-power ADT method (âMATâ) and a max-power joint optimization method (âMPTâ). ADT uniformly allocates the transmission data over all the time slots and jointly optimizes the mobility and the transmission power of the UAV. MAT is similar to ADT but uses the maximum transmission power for data transmissions. MPT also employs the maximum power while jointly optimizing the UAV mobility and the data allocation. Additionally, we follow the existing work [46] to adopt the simulation scenario as in Fig. 4 for performance comparison.

## 5.3.1 Effect of Flight Height

In Fig. 9, we first compare the energy consumption of different methods under different flight heights when the UAV meets the A2G transmission reliability constraint. The UAV data to be offloaded is set to and the mission comple-30 Mbtion time is given as . We also configure $\epsilon = 5 \times 1 0 ^ { - 2 }$ for 30 s Â¼ 5  10the -constraint on the A2G transmission reliability. We can find that the other methods, ADT, MAT and MPT, achieve on July 16,2024 at 03:12:15 UTC from IEEE Xplore. Restrictions apply.

<!-- image-->  
Fig. 9. The performance comparison under different flight heights.

the similar energy efficiency. Our joint optimization, JOM, has the lowest energy consumption on average, which is about $\mathrm { 1 . 3 5 1 2 \times 1 0 ^ { 4 } J }$ . By comparison, our method can reduce the 1 3512  10 Jenergy consumption by about 12.1% on average when compared to the others. Besides, from Fig. 9, it is seen that the energy consumption of our joint optimization method is less sensitive to the variation of the flight height when compared to the other methods. The reason is that the data transmission scheduling of our method can adapt to the variation of the A2G transmission distance incurred by changing the flight height.

## 5.3.2 Effect of Data Load and Mission Completion Time

Furthermore, we also examine the effects of the data load and the mission completion time on the performance of different methods. We fix the mission completion time of the UAV, i.e., the allowable time horizon for computation offloading, at , and vary the data volume of the application to be off-30 sloaded. The flight height of the UAV is fixed at .  is set to $\epsilon = 5 \times 1 0 ^ { - 2 }$ 50 mfor the -constraint reliability condition. In Â¼ 5  10Fig. 10, the energy consumption of different methods is compared under different data loads. It is seen that increasing the volume of application data to be offloaded leads to higher energy consumption. Nevertheless, our proposed method can achieve the best energy saving. When compared to ADT, MAT, and MPT, JOM reduces the energy consumption by about 33.71%, 33.14%, and 17.58% on average, respectively.

<!-- image-->

<!-- image-->  
Fig. 11. The performance comparison under different mission completion times.

Next, we vary the mission completion time of the UAV while setting the data load to . We configure the parameter  as $\epsilon = 1 \stackrel { \smile } { \times } 1 0 ^ { - 2 }$ 30 Mbto increase the reliability restriction. Fig. 11 illus-Â¼ 1  10trates the energy consumption of these methods under different mission completion times. We can find that more energy will be consumed with increased mission time. This is logical since the UAV needs to consume more energy when the flight duration becomes longer. Interestingly, when compared the results of Fig. 11 with those of Fig. 10, it is observed that the energy consumption of the comparative methods in Fig. 11 is higher than that in Fig. 10. The main reason is that all the comparative methods need to meet higher A2G transmission reliability when the -constraint on the reliability is configured with a much smaller $\epsilon , \mathrm { i . e . , } \epsilon = 1 \times 1 0 ^ { - 2 }$ in Fig. 11 while $\epsilon = 5 \times$ $1 0 ^ { - 2 }$ Â¼ 1  10 Â¼ 5 in Fig. 10. Additionally, from Fig. 11, our method can still 10outperform the other methods under different mission completion times. Specifically, it provides an average decrease of about 17.97% in the total energy consumption under the same transmission reliability condition as that of the other methods.

## 5.3.3 Effect of Path Loss Exponent

To examine the effect of the path loss exponent, we set the flight height to  and $\epsilon = \dot { 1 } \times 1 0 ^ { - 2 }$ as in Fig. 11. The vol-50 m Â¼ 1  10ume of application data to be offloaded is given as 30 Mband the mission completion time is . Fig. 12 compares the performance of different methods under different path loss exponents. It is also observed that our method can achieve the lowest energy consumption among the comparative methods. Compared to the others, JOM provides a significant decrease of about 43.37% in energy consumption on average meanwhile satisfying the transmission reliability requirement. The main reason is that the proposed optimization method can utilize the energy more efficiently by optimizing the UAV mobility, transmission power, and data allocation simultaneously. The other methods, e.g., ADT and MAT, do not schedule the data transmissions of the UAV adaptively according to the mobility.

<!-- image-->  
Fig. 10. The performance comparison under different data loads. exponents. exponents. Authorized licensed use limited to: Beijing Normal University. Downloaded on July 16,2024 at 03:12:15 UTC from IEEE Xplore. Restrictions apply.  
Fig. 12. The performance comparison under different path loss

<!-- image-->  
Fig. 13. The comparison of computation time.

## 5.3.4 Comparison of Computation Time

To analyze the computation efficiency of different methods, we further conduct Monte Carlo simulations. To be specific, Monte Carlo simulations of each method have been carried out with 500 replications under the condition that the data load is set to , the mission completion time is , and 30 Mb 30 sthe flight height is fixed at . The distribution of compu-50 mtation time per iteration during the Monte Carlo simulation of different optimization methods is illustrated in Fig. 13. The average computation time per optimization iteration of different methods and the corresponding standard deviation are summarized in Table 2. By comparison, we can see that the proposed joint optimization method, JOM, takes on average for each iteration execution, which is 415.2 mshigher than that of the other methods. This result is logical and expected since the computational complexity of the proposed joint optimization is higher than that of the other methods. Recalling the problem model (21) and the analysis in Section 4.4, the computational complexity of the algorithm relies on the dimension of the decision variables and the state variables, $n _ { \mathrm { v a r } }$ and $n _ { \mathrm { s t a t e } } .$ On one side, the dimenvar statesion of the state variables involved in the comparative methods is identical. On the other side, the proposed joint optimization method needs to jointly search for the optimal transmission power ${ \pmb q } ,$ the optimal acceleration control ${ \pmb a } ,$ and the optimal data transmission scheduling strategy x. The overall dimension of the decision variables, $n _ { \mathrm { v a r } } ,$ is varhigher than that of the others that only optimize partial decision variables. For example, MAT only aims at optimizing the mobility of the UAV while the transmission power and the data transmission strategy are fixed. Thus, MAT has the lowest computation time on average. However, it is noted from the recent literature (e.g., References [1], [2], [3], [10], [11], [14], [16], [17], [46], [54]) that the joint optimization can be operated off-line and thus the average computation time in the order of several seconds to several hundreds of seconds is allowable in actual application scenarios.4 At this point, the joint optimization method is applicable and, even at the price of a bit higher computation time, provides higher energy utilization under the A2G transmission reliability guarantee when compared to ADT, MAT, and MPT.

TABLE 2  
The Mean and Standard Deviation of Computation Time per Iteration of Different Optimization Methods
<table><tr><td>Methods</td><td>Avg. Time [ms]</td><td>Sth. Time [ms]</td></tr><tr><td>ADT</td><td>251.5</td><td>2.8</td></tr><tr><td>MAT</td><td>207.5</td><td>8.1</td></tr><tr><td>MPT</td><td>251.5</td><td>9.8</td></tr><tr><td>JOM</td><td>415.2</td><td>20.4</td></tr></table>

<!-- image-->  
Fig. 14. The performance comparison under different methods.

## 5.3.5 Trade-Off Between Energy Consumption and Transmission Reliability

To further illustrate the advantage of our method, we compare JOM with other optimization methods that exploit different strategies to transform the multiple objective functions into a single objective [48]. One comparative method is the weighting method (marked by âWTâ) that aims at optimizing the weighted sum of two objectives, v $E _ { \mathrm { U A V } } ( \pmb q , \pmb a , \pmb x ) + ( 1 - \omega ) \times ( - \bar { R } _ { \mathrm { U A V } } ( \pmb q , \pmb a , \pmb x ) )$ with v ranging UAVfrom $1 0 ^ { - 4 }$ Ã Ã¾ Ã°1  Ã  Ã° -UAVÃ° ÃÃto 0.9, while the other (marked by $^ { \prime \prime } \mathrm { F T ^ { \prime \prime } } )$ lumps 10the objectives into a single fractional form as the

687 9 s Authorized licensed use limited to: Beijing Normal University. Downloaded on July 16,2024 at 03:12:15 UTC from IEEE Xplore. Restrictions apply.

optimization objective, $E _ { \mathrm { U A V } } ( \pmb q , \pmb a , \pmb x ) / \bar { R } _ { \mathrm { U A V } } ( \pmb q , \pmb a , \pmb x )$ . We vary the parameter  from $1 0 ^ { - 3 }$ VÃ°to $1 0 ^ { - 1 }$ UAVÃ° Ãand obtain the Pareto 10 10frontier by the proposed method. Fig. 14 compares the different results. It is observed that the proposed method allows us to identify non-dominated points and the UAV is more likely to consume more energy when reaching higher transmission reliability. Our method achieves higher transmission reliability with almost the same energy consumption as that of WT and FT methods. Specifically, compared to WT and FT under the same energy consumption, our method can improve the transmission reliability by about 7.53% on average.

## 6 CONCLUSION AND FUTURE WORK

In this paper, we have investigated a UAV-assisted A2G communication network with the goal to reduce the mobility and communication energy consumption of the UAV while guaranteeing transmission reliability. We develop a bi-level optimization model for jointly controlling the acceleration and the transmission power of the UAV and scheduling the data transmissions. We have derived a closed-form expression for the transmission reliability and proposed an efficient iterative optimization algorithm to solve the problem. We have also performed simulations and validated the proposed algorithm. The empirical evaluation has shown that the proposed joint optimization method can significantly reduce the energy consumption meanwhile guaranteeing the A2G transmission reliability. In the future work, we will consider multi-UAV kinematics and extend the proposed optimization method to the joint optimization of multi-UAV control and communication. In this direction, a multi-UAV swarm mobility model will be described by using a multiple-inputmultiple-output (MIMO) state-space model, which is further incorporated into our -constraint optimization framework. Besides, we will also take into account different channel models characterizing different channel fading characteristics, including both large-scale and small-scale fading. We also expect to extend the A2G transmission reliability model to incorporate the stochastic characteristics of both non-lineof-sight and line-of-sight channel fading in a more complicated environment.

## REFERENCES

[1] S. Sekander, H. Tabassum, and E. Hossain, âStatistical performance modeling of solar and wind-powered UAV communications,â IEEE Trans. Mobile Comput., vol. 20, no. 8, pp. 2686â2700, Aug. 2021.

[2] Z. Dai, C. H. Liu, R. Han, G. Wang, K. Leung, and J. Tang, âDelaysensitive energy-efficient UAV crowdsensing by deep reinforcement learning,â IEEE Trans. Mobile Comput., early access, Sep. 16, 2021, doi: 10.1109/TMC.2021.3113052.

[3] M. Li, N. Cheng, J. Gao, Y. Wang, L. Zhao, and X. Shen, âEnergyefficient UAV-assisted mobile edge computing: Resource allocation and trajectory optimization,â IEEE Trans. Veh. Technol., vol. 69, no. 3, pp. 3424â3438, Mar. 2020.

[4] L. Zhang, A. Celik, S. Dang, and B. Shihada, âEnergy-efficient trajectory optimization for UAV-assisted IoT networks,â IEEE Trans. Mobile Comput., vol. 21, no. 12, pp. 4323â4337, Dec. 2022.

[5] J. Zhou, D. Tian, Y. Wang, Z. Sheng, X. Duan, and V. C. Leung, âReliability-optimal cooperative communication and computing in connected vehicle systems,â IEEE Trans. Mobile Comput., vol. 19, no. 5, pp. 1216â1232, May 2020.

[6] X. Liu, B. Lai, B. Lin, and V. C. M. Leung, âJoint communication and trajectory optimization for multi-UAV enabled mobile Internet of Vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 15354â15366, Sep. 2022.

[7] Y. Liu et al., âJoint communication and computation resource scheduling of a UAV-assisted mobile edge computing system for platooning vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 8435â8450, Jul. 2022.

[8] X. Liu, Y. Yu, F. Li, and T. S. Durrani, âThroughput maximization for RIS-UAV relaying communications,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 10, pp. 19569â19574, Oct. 2022.

[9] A. Hajihoseini Gazestani, S. A. Ghorashi, Z. Yang, and M. Shikh-Bahaei, âResource allocation in full-duplex UAV enabled multismall cell networks,â IEEE Trans. Mobile Comput., vol. 21, no. 3, pp. 1049â1060, Mar. 2022.

[10] Y. Zeng and R. Zhang, âEnergy-efficient UAV communication with trajectory optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 6, pp. 3747â3760, Jun. 2017.

[11] M. D. Nguyen, L. B. Le, and A. Girard, âIntegrated UAV trajectory control and resource allocation for UAV-based wireless networks with co-channel interference management,â IEEE Internet of Things J., vol. 9, no. 14, pp. 12754â12769, Jul. 2022.

[12] J. Baek, S. I. Han, and Y. Han, âOptimal UAV route in wireless charging sensor networks,â IEEE Internet Things J., vol. 7, no. 2, pp. 1327â1335, Feb. 2020.

[13] Y. Wang, M. Chen, C. Pan, K. Wang, and Y. Pan, âJoint optimization of UAV trajectory and sensor uploading powers for UAVassisted data collection in wireless sensor networks,â IEEE Internet Things J., vol. 9, no. 13, pp. 11214â11226, Jul. 2022.

[14] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[15] W. Mei, Q. Wu, and R. Zhang, âCellular-connected UAV: Uplink association, power control and interference coordination,â IEEE Trans. Wireless Commun., vol. 18, no. 11, pp. 5380â5393, Nov. 2019.

[16] C. Zhan and Y. Zeng, âEnergy-efficient data uploading for cellular-connected UAV systems,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7279â7292, Nov. 2020.

[17] J. Ji, K. Zhu, D. Niyato, and R. Wang, âJoint trajectory design and resource allocation for secure transmission in cache-enabled UAV-relaying networks with D2D communications,â IEEE Internet Things J., vol. 8, no. 3, pp. 1557â1571, Feb. 2021.

[18] H. Mei, K. Yang, Q. Liu, and K. Wang, âJoint trajectory-resource optimization in UAV-enabled edge-cloud system with virtualized mobile clone,â IEEE Internet Things J., vol. 7, no. 7, pp. 5906â5921, Jul. 2020.

[19] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[20] A. Al-Hilo, M. Samir, C. Assi, S. Sharafeddine, and D. Ebrahimi, âUAV-assisted content delivery in intelligent transportation systems-joint trajectory planning and cache management,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 8, pp. 5155â5167, Aug. 2021.

[21] S. Xu, X. Zhang, C. Li, D. Wang, and L. Yang, âDeep reinforcement learning approach for joint trajectory design in multi-UAV IoT networks,â IEEE Trans. Veh. Technol., vol. 71, no. 3, pp. 3389â3394, Mar. 2022.

[22] A. Gao, Q. Wang, W. Liang, and Z. Ding, âGame combined multiagent reinforcement learning approach for UAV assisted offloading,â IEEE Trans. Veh. Technol., vol. 70, no. 12, pp. 12888â12901, Dec. 2021.

[23] X. Liu, Y. Liu, Y. Chen, and L. Hanzo, âTrajectory design and power control for multi-UAV assisted wireless networks: A machine learning approach,â IEEE Trans. Veh. Technol., vol. 68, no. 8, pp. 7957â7969, Aug. 2019.

[24] P. Luong, F. Gagnon, L.-N. Tran, and F. Labeau, âDeep reinforcement learning-based resource allocation in cooperative UAVassisted wireless networks,â IEEE Trans. Wireless Commun., vol. 20, no. 11, pp. 7610â7625, Nov. 2021.

[25] M. Samir, D. Ebrahimi, C. Assi, S. Sharafeddine, and A. Ghrayeb, âLeveraging UAVs for coverage in cell-free vehicular networks: A deep reinforcement learning approach,â IEEE Trans. Mobile Comput., vol. 20, no. 9, pp. 2835â2847, Sep. 2021.

[26] X. Zhong, Y. Guo, N. Li, and Y. Chen, âJoint optimization of relay deployment, channel allocation, and relay assignment for UAVsaided D2D networks,â IEEE/ACM Trans. Netw., vol. 28, no. 2, pp. 804â817, Apr. 2020.

[27] N. Qi, Z. Huang, F. Zhou, Q. Shi, Q. Wu, and M. Xiao, âA task-driven sequential overlapping coalition formation game for resource allocation in heterogeneous UAV networks,â IEEE Trans. Mobile Comput., early access, Apr. 12, 2022, doi: 10.1109/TMC.2022.3165965.

[28] C. Fan, B. Li, J. Hou, Y. Wu, W. Guo, and C. Zhao, âRobust fuzzy learning for partially overlapping channels allocation in UAV communication networks,â IEEE Trans. Mobile Comput., vol. 21, no. 4, pp. 1388â1401, Apr. 2022.

[29] Z. Ning et al., âDynamic computation offloading and server deployment for UAV-enabled multi-access edge computing,â IEEE Trans. Mobile Comput., early access, Nov. 23, 2021, doi: 10.1109/ TMC.2021.3129785.

[30] Y. Wang et al., âTask offloading for post-disaster rescue in unmanned aerial vehicles networks,â IEEE/ACM Trans. Netw., vol. 30, no. 4, pp. 1525â1539, Aug. 2022.

[31] W. Xu et al., âMinimizing the deployment cost of UAVs for delaysensitive data collection in IoT networks,â IEEE/ACM Trans. Netw., vol. 30, no. 2, pp. 812â825, Apr. 2022.

[32] W. Xu et al., âThroughput maximization of UAV networks,â IEEE/ ACM Trans. Netw., vol. 30, no. 2, pp. 881â895, Apr. 2022.

[33] C. Luo, M. N. Satpute, D. Li, Y. Wang, W. Chen, and W. Wu, âFine-grained trajectory optimization of multiple UAVs for efficient data gathering from WSNs,â IEEE/ACM Trans. Netw., vol. 29, no. 1, pp. 162â175, Feb. 2021.

[34] W. Wang et al., âPlacement of unmanned aerial vehicles for directional coverage in 3D space,â IEEE/ACM Trans. Netw., vol. 28, no. 2, pp. 888â901, Apr. 2020.

[35] K. Wang, X. Zhang, L. Duan, and J. Tie, âMulti-UAV cooperative trajectory for servicing dynamic demands and charging battery,â IEEE Trans. Mobile Comput., early access, Sep. 08, 2021, doi: 10.1109/ TMC.2021.3110299.

[36] X. Zhang and L. Duan, âFast deployment of UAV networks for optimal wireless coverage,â IEEE Trans. Mobile Comput., vol. 18, no. 3, pp. 588â601, Mar. 2019.

[37] X. Xiao, W. Wang, and T. Jiang, âSensor-assisted rate adaptation for UAV MU-MIMO networks,â IEEE/ACM Trans. Netw., vol. 30, no. 4, pp. 1481â1493, Aug. 2022.

[38] S. Zhang, H. Zhang, B. Di, and L. Song, âCellular UAV-to-X communications: Design and optimization for multi-UAV networks,â IEEE Trans. Wireless Commun., vol. 18, no. 2, pp. 1346â1359, Feb. 2019.

[39] S. Chen, J. Hu, Y. Shi, L. Zhao, and W. Li, âA vision of C-V2X: Technologies, field testing, and challenges with chinese development,â IEEE Internet Things J., vol. 7, no. 5, pp. 3872â3881, May 2020.

[40] M. Alzenad and H. Yanikomeroglu, âCoverage and rate analysis for vertical heterogeneous networks (VHetNets),â IEEE Trans. Wireless Commun., vol. 18, no. 12, pp. 5643â5657, Dec. 2019.

[41] H. Lei et al., âSafeguarding UAV IoT communication systems against randomly located eavesdroppers,â IEEE Internet Things J., vol. 7, no. 2, pp. 1230â1244, Feb. 2020.

[42] Y. Pan et al., âJoint optimization of trajectory and resource allocation for time-constrained UAV-enabled cognitive radio networks,â IEEE Trans. Veh. Technol., vol. 71, no. 5, pp. 5576â5580, May 2022.

[43] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âMobile unmanned aerial vehicles (UAVs) for energy-efficient Internet of Things communications,â IEEE Trans. Wireless Commun., vol. 16, no. 11, pp. 7574â7589, Nov. 2017.

[44] I. Y. Abualhaol and M. M. Matalgah, âPerformance analysis of cooperative multi-carrier relay-based UAV networks over generalized fading channels,â Int. J. Commun. Syst., vol. 24, no. 8, pp. 1049â1064, 2011. [Online]. Available: https://onlinelibrary. wiley.com/doi/abs/10.1002/dac.1212

[45] M. Simunek, F. P. Fontan, and P. Pechac, âThe UAV low elevation propagation channel in urban areas: Statistical analysis and timeseries generator,â IEEE Trans. Antennas Propag., vol. 61, no. 7, pp. 3850â3858, Jul. 2013.

[46] C. Zhan, Y. Zeng, and R. Zhang, âEnergy-efficient data collection in UAV enabled wireless sensor network,â IEEE Wireless Commun. Lett., vol. 7, no. 3, pp. 328â331, Jun. 2018.

[47] Y. Zhang, D. Niyato, and P. Wang, âOffloading in mobile cloudlet systems with intermittent connectivity,â IEEE Trans. Mobile Comput., vol. 14, no. 12, pp. 2516â2529, Dec. 2015. [Online]. Available: https://doi.org/10.1109/TMC.2015.2405539

[48] K. Miettinen, A Posteriori Methods. Boston, MA, USA: Springer, 1998, pp. 77â113. [Online]. Available: https://doi.org/10.1007/ 978â1-4615-5563-6_4

[49] Z. Y. Wu, âSufficient global optimality conditions for weakly convex minimization problems,â J. Glob. Optim., vol. 39, no. 3, pp. 427â440, Nov. 2007. [Online]. Available: https://doi.org/ 10.1007/s10898â007-9147-z

[50] Z. Y. Wu, V. Jeyakumar, and A. M. Rubinov, âSufficient conditions for global optimality of bivalent nonconvex quadratic programs with inequality constraints,â J. Optim. Theory Appl., vol. 133, no. 1, pp. 123â130, Apr. 2007. [Online]. Available: https://doi.org/10.1007/s10957â007-9177-1

[51] A. S. Strekalovsky, âGlobal optimality conditions for nonconvex optimization,â J. Glob. Optim., vol. 12, no. 4, pp. 415â434, Jun. 1998. [Online]. Available: https://doi.org/10.1023/A:1008277314050

[52] S. A. Vavasis, Complexity Theory: Quadratic Programming Complexity Theory: Quadratic Programming. Boston, Boston, MA, USA: Springer, 2001, pp. 304â307. [Online]. Available: https://doi.org/ 10.1007/0-306-48332-7_65

[53] 3GPP, âStudy on enhanced LTE support for aerial vehicles,â Sophia Antipolis Valbonne, France, Tech. Rep. TR 36.777 V15.0.0, 2017.

[54] C. Shen, T.-H. Chang, J. Gong, Y. Zeng, and R. Zhang, âMulti-UAV interference coordination via joint trajectory and power control,â IEEE Trans. Signal Process., vol. 68, pp. 843â858, Jan. 2020.

[55] X. Lin, C. Wang, K. Wang, M. Li, and X. Yu, âTrajectory planning for unmanned aerial vehicles in complicated urban environments: A control network approach,â Transp. Res. C: Emerg. Technol., vol. 128, 2021, Art. no. 103120. [Online]. Available: https://www. sciencedirect.com/science/article/pii/S0968090X2100139X

[56] S. Sharif Azadeh, M. Bierlaire, and M. Maknoon, âA two-stage route optimization algorithm for light aircraft transport systems,â Transp. Res. C: Emerg. Technol., vol. 100, pp. 259â273, 2019. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S0968090X18311628

<!-- image-->

Jianshan Zhou received the BSc, MSc, and PhD degrees in traffic information engineering and control from Beihang University, Beijing, China, in 2013, 2016 and 2020, respectively. From 2017 to 2018, he was a visiting research fellow with the School of Informatics and Engineering, University of Sussex, Brighton, U.K. He is currently a postdoctoral research fellow supported by the Zhuoyue Program of Beihang University and the National Postdoctoral Program for Innovative Talents, and is or was the Technical Program Session chair with the IEEE EDGE 2020, the TPC member with the IEEE VTC2021-Fall track, and the Youth editorial board member of the Unmanned Systems Technology. He is the author or coauthor of more than 20 international scientific publications. His research interests include the modeling and optimization of vehicular communication networks and airâground cooperative networks, the analysis and control of connected autonomous vehicles, and intelligent transportation systems. He was the recipient of the First Prize in the Science and Technology Award from the China Intelligent Transportation Systems Association, in 2017, the First Prize in the Innovation and Development Award from the China Association of Productivity Promotion Centers, in 2020, the National Scholarships, in 2017 and 2019, the Outstanding Top-Ten PhD Candidate Prize from Beihang University, in 2018, the Outstanding China-SAE Doctoral Dissertation Award, in 2020, and the Excellent Doctoral Dissertation Award from Beihang University, in 2021.

<!-- image-->

Daxin Tian (Senior Member, IEEE) received the PhD degree in technology of computer application from Jilin University, China, in 2007. He is currently a professor with the School of Transportation Science and Engineering, Beihang University, Beijing, China. His current research interests include mobile computing, intelligent transportation systems, vehicular ad hoc networks, and swarm intelligence. He leads about 11 research projects such as the projects funded by the National Natural Science Foundation and the

National Key Research and Development Program. He has authored/coauthored about 213 journal/conference papers, published 7 monographs and 2 translations, and authorized 34 invention patents. He was the recipient of the Second Prize of the National Science and Technology Award, in 2015 and 2018, the First Prize of the Technical Invention Award of the Ministry of Education, in 2017, the First Prize of the Science and Technology Award from the China Intelligent Transportation Association, in 2017, the First Prize of the Innovation and Development Award from the China Association of Productivity Promotion Centers, in 2020, and seven other ministerial and provincial science and technology awards. He also received the Changjiang Youth Scholars Program of China, in 2018 and the Outstanding Youth Fund from the National Natural Science Foundation of China, in 2019, the Forum Keynote Award from the 2019 Cyberspace Congress, the Outstanding Invited Speaker from the 2020 International Conference on Blockchain and Trustworthy Systems, and the Distinguished Young Investigator of China Frontiers of Engineering from Chinese Academy of Engineering, in 2018. He was also awarded the Exemplary reviewer for IEEE Wireless Communications Letters. He is a senior member of CCF, and ITSC, and was or is the editor-in-chief of International Journal of Vehicular Telematics and Infotainment Systems, the associate editor of IEEE Transactions on Intelligent Vehicles, IEEE Internet of Things Journal, Complex System Modeling and Simulation, and Journal of Intelligent and Connected Vehicles.

<!-- image-->

Yaqing Yan received the BSc degree in traffic engineering from the Beijing University of Technology, Beijing, China, in 2020. She is currently working toward the MSc degree with Beihang University. Her research interests include air-ground cooperative networks and wireless communications.

<!-- image-->

Xuting Duan received the PhD degree in traffic information engineering and control from Beihang University, Beijing, China, in 2017. He is currently an assistant professor with the School of Transportation Science and Engineering, Beihang University. His current research interests are focused on vehicular ad hoc networks.

<!-- image-->

Xuemin Shen (Fellow, IEEE) received the PhD degree in electrical engineering from Rutgers University, New Brunswick, New Jersey, in 1990. He is currently a University professor with the Department of Electrical and Computer Engineering, University of Waterloo, Canada. His research focuses on network resource management, wireless network security, Internet of Things, 5G and beyond, and vehicular ad hoc and sensor networks. He is a registered professional engineer of Ontario, Canada, an Engineering Institute of Canada fellow, a Canadian Academy of

Engineering fellow, a Royal Society of Canada fellow, a Chinese Academy of Engineering Foreign member, and a distinguished lecturer of the IEEE Vehicular Technology Society and Communications Society. He received the R.A. Fessenden Award, in 2019 from IEEE, Canada, Award of Merit from the Federation of Chinese Canadian Professionals (Ontario), in 2019, James Evans Avant Garde Award, in 2018 from the IEEE Vehicular Technology Society, Joseph LoCicero Award, in 2015 and Education Award, in 2017 from the IEEE Communications Society, and Technical Recognition Award from Wireless Communications Technical Committee (2019) and AHSN Technical Committee (2013). He has also received the Excellent Graduate Supervision Award, in 2006 from the University of Waterloo and the Premierâs Research Excellence Award (PREA), in 2003 from the Province of Ontario, Canada. He served as the Technical Program Committee chair/co-chair for IEEE Globecomâ16, IEEE Infocomâ14, IEEE VTCâ10 Fall, IEEE Globecomâ07, and the chair for the IEEE Communications Society Technical Committee on Wireless Communications. He is the elected IEEE Communications Society vice president for Technical & Educational Activities, vice president for Publications, Member-at-Large on the Board of Governors, chair of the Distinguished Lecturer Selection Committee, member of IEEE ComSoc Fellow Selection Committee. He was/is the editor-in-chief of the IEEE IoT Journal, IEEE Network, IET Communications, and Peer-to-Peer Networking and Applications.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/csdl.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua/page_5_img_1.jpeg|page_5_img_1]]
2. [[../extracted_images/Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua/page_14_img_1.jpeg|page_14_img_1]]
3. [[../extracted_images/Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua/page_15_img_1.jpeg|page_15_img_1]]
4. [[../extracted_images/Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua/page_15_img_2.jpeg|page_15_img_2]]
5. [[../extracted_images/Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua/page_15_img_3.jpeg|page_15_img_3]]
6. [[../extracted_images/Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua/page_15_img_4.jpeg|page_15_img_4]]

---

