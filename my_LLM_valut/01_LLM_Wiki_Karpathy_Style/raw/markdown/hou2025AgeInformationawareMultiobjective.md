# Age of Information-Aware Multi-Objective Optimization for Heterogeneous UAV-USV-UUV Networks in Underwater Target Hunting

Xiangwang Hou , Member, IEEE, Tianyu Xing, Jingjing Wang , Senior Member, IEEE, Jun Du , Senior Member, IEEE, Chunxiao Jiang , Fellow, IEEE, Yong Ren , Senior Member, IEEE, and Dusit Niyato , Fellow, IEEE

AbstractâUnderwater target hunting (UTH) is a critical and complex mission involving the search, tracking, and hunting of targets in an underwater environment. However, the unpredictable trajectories and flexibility of these targets, along with complex underwater environments, significantly impede the efficiency and success of traditional methods that depend solely on unmanned underwater vehicles (UUVs). Consequently, this paper presents the â3U networkâ, a novel heterogeneous framework integrating unmanned aerial vehicles (UAVs), unmanned surface vehicles (USVs), and UUVs for UTH. Within this framework, a UAV identifies the target, a USV acts as a communication relay, and a swarm of UUVs hunts the target. Moreover, to improve the timeliness of target detection, we incorporate the age of information (AoI) concept into the UAVâs search strategy. Additionally, we develop a constrained multi-objective optimization problem to minimize energy consumption and mission duration by optimizing vehiclesâ trajectories, considering mobility limitations, safety, and connectivity

constraints. Furthermore, to tackle this problem, we design an AoIand energy-aware multi-vehicle twin-delayed deep deterministic policy gradient algorithm (AE-MVTD3) to optimize control policies for heterogeneous vehicles. The experimental results show that the proposed method performs effectively across diverse complex scenarios.

Index TermsâAge of information (AoI), heterogeneous networks, multi-agent reinforcement learning (MARL), trajectory design, underwater target hunting (UTH).

## I. INTRODUCTION

U NDERWATER target hunting (UTH) is integral to a vari-ety of maritime operations, such as emergency rescues, biological observations, and military missions. The UTH mission, encompassing stages of target search, identification, tracking, and directional capture, presents substantial challenges, particularly in adverse underwater environments.

Currently, unmanned underwater vehicles (UUVs) are extensively employed in the UTH mission [1], [2], due to their flexibility. On this basis, orchestrating multiple UUVs to form a UUV swarm can further improve the success rate with high efficiency, which has been widely studied in recent years [3], [4], [5], [6], [7]. However, the unpredictable escape behaviors of targets directly oppose the limited observation range of UUV swarms. This inherent conflict diminishes the effectiveness of traditional strategies that depend solely on UUV swarm, resulting in lower success rates and operational efficiency.

The integration of unmanned aerial vehicles (UAVs), unmanned surface vehicles (USVs), and UUVs into a cross-domain â3U networkâ has recently garnered significant attention [8], [9], [10], [11], [12], offering substantial improvements in UTH performance compared to traditional UUV-centric approaches. Specifically, UAVs conduct extensive area searches and provide high-precision monitoring, thereby elevating the search success rate. Concurrently, UUV swarms execute precise hunting operations. However, the effectiveness of UAVs is constrained in underwater conditions due to significant attenuation of radio communications, which hampers the transfer of target positioning information to UUV swarm. To bridge this gap, USVs serve as communication relays, receiving data from UAVs via radio communications and relaying it to UUV swarms through underwater acoustic communication, thus ensuring a robust information exchange link. However, the existing studies [8], [9], [10], [11], [12] lack proper modeling of the dynamics of these vehicles and overlook the impact of harsh underwater environment, such as irregular currents and vortex regions in environments with different depths, which significantly deteriorates the effectiveness of the designed strategies in real-world environments [13].

Therefore, this paper presents a novel practical â3U networkâ for the UTH mission, which incorporates the kinematics and dynamics modeling of all vehicles, as well as the impacts of underwater environments characterized by obstacles and turbulence. Moreover, given that the timeliness of search information critically influences the effectiveness of strategies, we integrate the concept of the age of information (AoI) into the UAVâs search strategy. AoI [14], [15], [16], [17], [18], [19] is an essential metric for assessing the timeliness of information within a network, defined as the duration from when information is generated to the current moment. Unlike conventional latency, AoI considers not only transmission delays but also the waiting time at the source node and the residence time at the destination node.

Besides, optimizing the multiple objectives including energy efficiency and operational time, under constraints such as mobility limitations, complex environments, network connectivity, and collision avoidance, is a complex, high-dimensional, multiobjective sequential decision-making problem. Traditional optimization methods [8], [9], [10] and basic reinforcement learning-based (RL) approaches [11], [20], [21] prove insufficient for addressing this issue. Consequently, in this paper, we present a multi-agent reinforcement learning (MARL)-based algorithm specifically designed to tackle this problem.

The main contributions of this paper can be summarized as follows:

- To the best of our knowledge, it is the first work to introduce the concept of AoI into 3U network for the UTH mission to improve the strategyâs effectiveness.

We conceive a multi-objective optimization framework for 3U network to perform the UTH mission, considering the kinematics and dynamics modeling of all vehicles, and the complex underwater environments. Thus, the framework can be applied into practical scenarios.

C We design an AoI- and energy-aware multi-vehicle twin-delayed deep deterministic policy gradient-based (AE-MVTD3) algorithm to solve the formulated problem. Experimental results show that the proposed scheme outperforms the state-of-the-art baselines significantly.

The rest of the paper is organized as follows. Section II reviews the related works. Section III introduces the system model, while Section IV presents the design details of AE-MVTD3. Experimental results are analyzed in Section V, and finally, conclusions are drawn in Section VI.

## II. RELATED WORKS

In the early stage, researchers have focused on collaborative hunting methods solely relying on UUV swarms [3], [4], [5]. Ni et al. [3] constructed a two-stage hunting scheme that uses the spinal neural system to ensure the safe search of UUVs and the genetic algorithm to assign hunting directions to UUVs. To improve the hunting success rate for escaping targets, Wei et al. [4] explored a different game-based target hunting approach, which introduces Leibnizâs formula-based Hamiltonian function into a feedback control strategy in the context of dynamic environments incorporating currents, winds, and signals. Besides, Wang et al. [5] developed an environment-aware hunting scheme that maximizes the search area and enables revisit search. The aforementioned studies coordinate multiple UUVs for target search and directional hunting but overlook the vehiclesâ limited perception and communication range, resulting in reduced search efficiency.

Consequently, several studies have highlighted the use of heterogeneous vehicles to support UUVs in the UTH mission. Lin et al. [22] proposed a USV-UUV-based hunting scheme, utilizing USVs as communication relays to share collected data with UUVs, which intensely enhances the search efficiency while ignoring the mission failure due to excessive energy consumption. To further enhance search efficiency, UAVs were introduced into the UTH mission. Shirakura et al. [23] developed a UAV-UUV target hunting scheme that leveraged UAVsâ high flexibility to conduct wide-range searches, reducing search time and improving the efficiency of target hunting. However, radio communication between UAVs and UUVs is severely attenuated underwater, leading to unstable connections. Therefore, a communication relay is essential to transmit information from UAVs to UUVs.

Recently, the 3U network, combining the high mobility and cost-effectiveness of UAVs, the flexibility and communication conversion capability of USVs, and the hunting capability of UUVs, has been widely studied [8], [9], [10], [11], [12]. Wu et al. [8] constructed a UAV-USV-UUV collaborative scheduling framework that employs a particle swarm optimization (PSO) algorithm to maximize the search range and minimize the final errors. To enhance the 3U networkâs search capability, Ke et al. [9] provided a detection capability for each vehicle and adopted an improved PSO algorithm to perform the vehicleâs obstacle avoidance and path planning, minimizing the search time and path length. However, these schemes overlook the critical need for communication connectivity between 3U vehicles, potentially limiting their effectiveness in practical applications. To optimize the scheduling trajectories of heterogeneous vehicles while keeping radio and hydroacoustic communications connected, Cao et al. [10] designed a UAV-USV-UUV path planning scheme based on gray wolf optimization, which achieves UAVâs full-coverage search, shares collected data, reduces the vehicleâs mobile energy consumption and improves endurance. However, previous 3U studies rely on traditional optimization methods to address multi-vehicle scheduling, potentially leading to significant increases in computation time for finding optimal solutions. Hence the RL-based approaches have emerged. Focusing on RL-based collaborative hunting schemes, in [11], Wei et al. designed an energy-oriented UAV-USV-UUV trajectory scheduling method that utilizes the optimal solution of radio communication and the connectivity map of acoustic communication to synchronize the environmental information, decrease the redundant motions and improve energy efficiency of heterogeneous vehicles. Similarly, Dong et al. [12] developed a multi-strategy RL algorithm to tackle the 3U networkâs multivehicle control problem, enhancing the mission success rate and reducing mission time. However, the studies mentioned [8], [9], [10], [11], [12] overlook environmental factors such as turbulence and obstacles, as well as the impact of vehicle dynamics on the hunting process. As a result, these strategies demonstrate ineffective in real-world scenarios.

<!-- image-->  
Fig. 1. The 3U network framework for UTH mission.

Hence, to compensate for the insufficient utility of previous works, we construct a multi-objective optimization framework considering the kinematics and dynamics modeling of all vehicles and the complex underwater environment. Moreover, we introduce the concept of AoI to further enhance the search efficiency.

## III. SYSTEM MODEL

## A. Heterogeneous Network Model

The 3U network is composed of a UAV, a USV, and M UUVs. The coordinates of the UAV, USV, and UUV i are defined as $A = ( x ^ { \mathrm { A } } , y ^ { \mathrm { A } } , h ) , S = ( x ^ { \mathrm { S } } , y ^ { \mathrm { S } } , 0 ) , P _ { i } = ( x _ { i } ^ { \mathrm { U } } , y _ { i } ^ { \mathrm { U } } , z _ { i } ^ { \mathrm { U } } ) , i \in$ $U = \{ 1 , 2 , \dots , M \}$ , respectively. Fig. 1 illustrates the framework of the 3U network, where UAV searches and tracks the underwater target, the UUV swarm conducts target-hunting missions, and the USV acts as a communication relay between UAV and UUVs to transmit target information. Additionally, the set of USV and M UUVs is defined as $V = \{ 1 , 2 , \dots , \mathcal { H } \}$ , where $\mathcal { H } =$ $M + 1$ and the H -th vehicle represents the USV. Moreover, the vehicle set of 3U network is defined as $\pmb { \mathcal { M } } = \{ 1 , \dots , \# , \pmb { \mathcal { M } } \}$ where $\mathcal { M } = \mathcal { H } + 1$ and the M-th vehicle represents the UAV. Besides, the oceanic environment contains K obstacles, defined as the set $K = \{ 1 , 2 , \dots , K \}$ , where the center coordinate of the obstacle k is $P _ { k } = ( x _ { k } ^ { \mathrm { O } } , y _ { k } ^ { \mathrm { O } } , z _ { k } ^ { \mathrm { O } } )$ . Moreover, there are N vortices in the oceanic environment, represented by the set $N = \{ 1 , 2 , \dots , N \}$ , where the center coordinate of vortex n is $\overset { \triangledown } { \boldsymbol { P } _ { n } } = ( x _ { n } ^ { \mathrm { V } } , y _ { n } ^ { \mathrm { V } } ) . \ \overset { \triangledown } { \boldsymbol { T } } = ( x ^ { \mathrm { T } } , y ^ { \mathrm { T } } , z ^ { \mathrm { T } } )$ denotes the position of the underwater target.

The operation of the 3U network consists of two phases: the search phase and the hunting phase. In the search phase, a UAV with altitude h and square view angle 2Î¸ lattices the environment, and the AoI of a lattice grows over time within a threshold range. The UAV searches for underwater targets by utilizing the collected environmental AoI and transmits the collected oceanographic information to the USV via radio communication. Once the target is detected at the moment $T _ { s }$ , i.e., $\{ \| x ^ { \mathrm { A } } - x ^ { \mathrm { T } } \| \leq h \}$ Â· tan $\theta ~ \& \| y ^ { \mathrm { A } } - y ^ { \mathrm { T } } \| \le h \cdot \tan \theta \}$ , the UAV switches from target search to target tracking, and the 3U network transitions into the hunting phase. Then, in the hunting phase, the UAV continuously monitors the target, the USV relays target information from the UAV to the UUV swarm via underwater acoustic communication, and the UUV swarm initiates the target hunting process. If $\| P _ { i } - T \| \leq b _ { 0 } , \forall i \in U$ is satisfied at the moment $T _ { u } ,$ , the target hunting mission is successful. Here, $b _ { 0 }$ is the hunting radius, typically set to 14 m. Additionally, the USV and UUVs should avoid obstacles and vortices to ensure safety during the mission. Table I summarizes main notations.

<table><tr><td rowspan=1 colspan=1>Nitation</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>NumberofUUVs</td></tr><tr><td rowspan=1 colspan=1>U</td><td rowspan=1 colspan=1>Set ofUUV</td></tr><tr><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>Total numberofUUVsandUSV</td></tr><tr><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>SetofUUVandUSV</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>Total numberofUUVs,USVandUAV</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>SetofUUVUSVandUA</td></tr><tr><td rowspan=1 colspan=1>K</td><td rowspan=1 colspan=1>Setof obstacle</td></tr><tr><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=1>Setofvortex</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>ViewangleofUAV</td></tr><tr><td rowspan=1 colspan=1>h</td><td rowspan=1 colspan=1>FlightaltitudeofUAV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { T _ { s } } }$ </td><td rowspan=1 colspan=1>Total time of target search</td></tr><tr><td rowspan=1 colspan=1> $\overline { { T _ { h } } }$ </td><td rowspan=1 colspan=1>Total timeofUTHmission</td></tr><tr><td rowspan=1 colspan=1> $\overline { V }$ </td><td rowspan=1 colspan=1>Vehicle velocity</td></tr><tr><td rowspan=1 colspan=1> $a _ { c }$ </td><td rowspan=1 colspan=1>Vehicleacceleration</td></tr><tr><td rowspan=1 colspan=1> $\underline { { p } }$ </td><td rowspan=1 colspan=1>Vehiclepitchangularvelocity</td></tr><tr><td rowspan=1 colspan=1> $q$ </td><td rowspan=1 colspan=1>Vehicleyawangularvelocity</td></tr><tr><td rowspan=1 colspan=1> $A _ { w }$ </td><td rowspan=1 colspan=1>AoI oflattice w</td></tr><tr><td rowspan=1 colspan=1> $\underline { { r _ { d } } }$ </td><td rowspan=1 colspan=1>Maximum distance of sonardetection</td></tr><tr><td rowspan=1 colspan=1> $\underline { { r _ { s } } }$ </td><td rowspan=1 colspan=1>Perceived distanceof USVand UUV to thedangerousarea</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \Theta } }$ </td><td rowspan=1 colspan=1>Vortexstrength</td></tr><tr><td rowspan=1 colspan=1> $\varrho$ </td><td rowspan=1 colspan=1>Disturbanceradius</td></tr></table>

TABLE I LIST OF NOTATIONS

Remark: In the search phase, underwater targets may be detected first by UUVs, a USV, or a UAV. The case in which UUVs or a USV detect the target first, and then UUVs perform the hunting mission is relatively straightforward. The case we study is that a UAV detects an underwater target and sends the target information to UUVs via a USV, and subsequently, the UUVs perform the hunting mission.

## B. Motion Model

In the inertial coordinate system, all vehicles are treated as moving particles in the 3D space. We assume that a USV moves on the sea surface and a UAV flies at a fixed altitude h, simplifying their movements to the 2D plane. The dynamics model for all vehicles and the underwater target in the inertial coordinate system is defined as

$$
\left\{ \begin{array} { l l } { \dot { x } = V \cos \xi \cos \varphi , } \\ { \dot { y } = V \cos \xi \sin \varphi , } \\ { \dot { z } = V \sin \xi , } \\ { \dot { V } = a _ { c } , } \\ { \dot { \xi } = p , } \\ { \dot { \varphi } = q . } \end{array} \right.\tag{1}
$$

In (1), the state vector $\begin{array} { r } { \pmb { s } _ { v } = [ x , y , z , V , \xi , \varphi ] ^ { \operatorname { T } } } \end{array}$ and the motion control vector $\boldsymbol { F } _ { 3 } = [ a _ { c } , p , q ] ^ { \mathrm { \tilde { T } } }$ contain all the information of the vehicle, where $[ x , y , z ] ^ { \mathrm { T } }$ and V represent the vehicleâs position and velocity, while Î¾ and $\varphi$ denote the vehicleâs pitch and steering angles, respectively. Besides, $a _ { c } , p$ and q denote the acceleration, pitch and yaw angular velocities of the vehicle motion, respectively. $\pmb { s } _ { v } ^ { \mathrm { A } } = [ x ^ { \mathrm { A } } , y ^ { \mathrm { A } } , z ^ { \mathrm { A } } , V ^ { \mathrm { A } } , \xi ^ { \mathrm { A } } , \varphi ^ { \mathrm { A } } ] ^ { \mathrm { T } }$ and $\pmb { F } _ { 3 } ^ { \mathrm { A } } = [ a _ { c } ^ { \mathrm { A } } , p ^ { \mathrm { A } } , q ^ { \mathrm { A } } ] ^ { \mathrm { T } }$ represent the UAVâs state and motion controller, respectively. Besides, $\pmb { s } _ { v } ^ { \mathrm { S } } = [ x ^ { \mathrm { S } } , y ^ { \mathrm { S } } , z ^ { \mathrm { S } } , V ^ { \mathrm { S } } , \xi ^ { \mathrm { S } } , \varphi ^ { \mathrm { S } } ] ^ { \mathrm { T } }$ and $F _ { 3 } ^ { \mathrm { S } } = [ \dot { a } ^ { \mathrm { S } } , p ^ { \mathrm { S } } , \dot { q } ^ { \mathrm { S } } ] ^ { \mathrm { T } }$ represent the USVâs state and motion controller, respectively. Furthermore, $\begin{array} { r } { \pmb { s } _ { v , i } ^ { \mathrm { U } } = [ x _ { i } ^ { \mathrm { U } } , y _ { i } ^ { \mathrm { U } } } \end{array}$ $z _ { i } ^ { \mathrm { U } } , V _ { i } ^ { \mathrm { U } } , \xi _ { i } ^ { \mathrm { U } } , \varphi _ { i } ^ { \mathrm { U } } ] ^ { \mathrm { T } }$ and $\begin{array} { r } { \mathbf { { F } } _ { 3 , i } ^ { \mathrm { U } } = [ a _ { c , i } ^ { \mathrm { U } } , p _ { i } ^ { \mathrm { U } } , q _ { i } ^ { \mathrm { U } } ] ^ { \mathrm { T } } } \end{array}$ represent the state and motion controller of UUV i, respectively. Additionally, $\pmb { s } _ { v } ^ { \mathrm { T } } = [ x ^ { \mathrm { T } } , y ^ { \mathrm { T } } , z ^ { \mathrm { T } } , V ^ { \mathrm { T } } , \xi ^ { \mathrm { T } } , \varphi ^ { \mathrm { T } } ] ^ { \mathrm { T } }$ and $\pmb { F } _ { 3 } ^ { \mathrm { T } } = [ a _ { c } ^ { \mathrm { T } } , p ^ { \mathrm { T } } , q ^ { \mathrm { T } } ] ^ { \mathrm { T } }$ represent the targetâs state and motion controller, respectively. Hence, based on the vehiclesâ dynamics, we have $| V ^ { \mathrm { A } } | \leq | V _ { \mathrm { m a x } } ^ { \mathrm { A } } | , | a _ { c } ^ { \mathrm { A } } | \leq | a _ { \mathrm { m a x } } ^ { \mathrm { A } } | , | p ^ { \mathrm { A } } | \ = \ 0 , | q ^ { \mathrm { \bar { A } } } | \leq | q _ { \mathrm { m a x } } ^ { \mathrm { A } } | , | V ^ { \mathrm { S } } | \leq$ $\lvert V _ { \mathrm { m a x } } ^ { \mathrm { S } } \rvert , \lvert a _ { c } ^ { \mathrm { S } } \rvert \le \lvert a _ { \mathrm { m a x } } ^ { \mathrm { S } } \rvert , \lvert p ^ { \mathrm { S } } \rvert = 0 , \lvert q ^ { \mathrm { S } } \rvert \le \lvert q _ { \mathrm { m a x } } ^ { \mathrm { S } } \rvert , \quad \lvert V ^ { \mathrm { U } } \rvert \le \lvert V _ { \mathrm { m a x } } ^ { \mathrm { U } } \rvert .$ $\lvert a _ { c } ^ { \mathrm { U } } \rvert \leq \lvert a _ { \operatorname* { m a x } } ^ { \mathrm { U } } \rvert , \lvert p ^ { \mathrm { U } } \rvert \leq \lvert p _ { \operatorname* { m a x } } ^ { \mathrm { U } } \rvert , \lvert q ^ { \mathrm { U } } \rvert \leq \lvert q _ { \operatorname* { m a x } } ^ { \mathrm { U } } \rvert , \lvert V ^ { \mathrm { T } } \rvert \leq \lvert V _ { \operatorname* { m a x } } ^ { \mathrm { T } } \rvert ,$ $| { a } _ { c } ^ { \mathrm { T } } | \leq | { a } _ { \mathrm { m a x } } ^ { \mathrm { T } } | , | { p } ^ { \mathrm { T } } | \leq | { p } _ { \mathrm { m a x } } ^ { \mathrm { T } } | ,$ and $\lvert q ^ { \mathrm { T } } \rvert \leq \lvert q _ { \mathrm { m a x } } ^ { \mathrm { T } } \rvert .$ where the subscripts A, S, U and T indicate the UAV, USV, UUV and target, respectively. Furthermore, $V _ { \mathrm { m a x } } , \ a _ { \mathrm { m a x } } , \ p _ { \mathrm { m a x } } .$ , and $q _ { \mathrm { m a x } }$ represent the maximum values of velocity, acceleration, pitch angle, and yaw angular velocities of the corresponding vehicle, respectively, which indicates that each vehicle must not exceed its physical limitations. Moreover, considering the game properties, the UUV has higher power, and the target has better maneuverability, so the conditions should be satisfied as $V _ { \mathrm { m a x } } ^ { \mathrm { U } } > V _ { \mathrm { m a x } } ^ { \mathrm { T } } , p _ { \mathrm { m a x } } ^ { \mathrm { U } } < \dot { p } _ { \mathrm { m a x } } ^ { \mathrm { T } } , q _ { \mathrm { m a x } } ^ { \mathrm { U } } < q _ { \mathrm { m a x } } ^ { \mathrm { T } }$

## C. Communication and Connection Models

1) UAV to USV: According to [24], the radio communication is used to transmit information between UAV and USV, and a line-of-sight assures the communication link. Therefore the achievable transmission rate is expressed as:

$$
\mathbb { R } _ { \mathrm { A } , \mathrm { S } } ( t ) = \log _ { 2 } \left( 1 + \frac { \mathcal { P } _ { 0 } \left\| A - S \right\| ^ { - \nu } } { \sigma _ { 2 } } \right)\tag{2}
$$

where $\mathcal { P } _ { 0 } , \nu$ and $\sigma _ { 2 }$ represent the product of signal transmission power and power gain, attenuation factor, and power density of white noise, respectively. To satisfy the requirement of channel quality, the $\mathbb { R } _ { \mathrm { A } , \mathrm { S } }$ should be greater than some threshold $\chi _ { t h } .$ Therefore, the communication distance is subject to $\| A - S \| <$ $\big ( \frac { \mathcal { P } _ { 0 } } { \sigma ^ { 2 } ( 2 ^ { \chi _ { t h } } - 1 ) } \big ) ^ { 1 / \nu }$

2) USV and UUVs: The USV and UUVs communicate via underwater acoustic channel. As an important underwater acoustic equipment, sonar has been used to communicate and detect obstacles. The sonar equation for underwater environments can be expressed as [25]

$$
E M = S L + T S + D I - ( N L + D T + 2 T L ( f , d ) ) ,\tag{3}
$$

where $S L , T S , D I , N L , D T ,$ , and T L indicate the emission strength of the information source, target strength related to the reflection area, directivity index of the sonar, ambient noise level, recognition threshold of the received information, and transmission loss, respectively. Additionally, f and d represent the center acoustic frequency and detection distance, respectively. Besides, EM denotes the echo margin of the emitted signal by the active sonar. We use $r _ { a }$ to represent the detection radius.

Subsequently, the signal-to-noise ratio between USV and UUVs in underwater communication is denoted as

$$
\rho _ { i , j } = S L - T L - N L + D I ,\tag{4}
$$

where $\rho _ { i , j } > D T , \forall i , j \in V$ , represents the connected communication.

## D. UAV Search Model Based on AoI

We assume that the condition of the UAV successfully discovering an underwater target is $\{ \| x ^ { \mathrm { A } } - x ^ { \mathrm { T } } \| \leq h \cdot \tan \theta \ { \overset { } { \& } } \| y ^ { \mathrm { A } } -$ $y ^ { \mathrm { T } } \| \leq h \cdot \tan \theta \}$ , so we can define the topology of the UAVâs search as a 2D scenario in the Cartesian coordinate system. To facilitate the classification of the search area and storage of area information, the search environment is modeled as a 2D lattice map, with a map resolution of Î¹. Specifically, we denote the lattice set as $\Omega = \{ 1 , \dots , w , \dots , L _ { \iota } \}$ , where $L _ { \iota }$ is the number of lattices. Consequently, the UAV creates a lattice information table C to store and update the collected lattice information, and the information C at the moment t is denoted as $\mathbb { C } ( t ) = \{ c _ { 1 } ( t ) , \ldots , c _ { w } ( t ) , \ldots , c _ { L _ { \iota } } ( t ) \}$ . As Î¹ is sufficiently small, the center coordinates $P _ { w } ^ { 2 } = ( x _ { w } , y _ { w } )$ of lattice w can be used to represent the lattice position. Furthermore, for lattice $w , \mathrm { i f } d _ { \mathrm { A , w } } ( t )$ satisfies $\{ \| x ^ { \mathrm { A } } - x _ { w } \| \leq h$ Â· tan Î¸ $\begin{array} { r } { \& \| y ^ { \mathrm { A } } - y _ { w } \| \le } \end{array}$ $h \cdot \tan \theta \}$ at the moment t, the area is searched by the UAV. Specifically, using current Laser-based detection technology, UAV can obtain accurate 3D underwater information.1 When lattice w is searched, it means UAV has gathered complete information for the area with coordinates $P _ { w } ^ { 3 } = ( x _ { w } , y _ { w } , g )$ , where g represents an arbitrary value in the underwater environment.

During the search target, the UAV lacks a metric for the degree of environmental search, so we introduce the AoI to characterize the timespan since each lattice was last searched [5]. Thus, the areas that have been unsearched for a long time urgently need to be searched. We use AoI to denote the search degree of the lattice w as

$$
{ A _ { w } ( t ) } = \operatorname* { m i n } \left\{ { A _ { \operatorname* { m a x } } , \kappa \times \operatorname* { m a x } \left\{ { t - T _ { w } , 0 } \right\} \cdot \varDelta t } \right\} ,\tag{5}
$$

where $A _ { \mathrm { m a x } }$ is the maximum AoI. Îº and $T _ { w }$ are the growth factor and latest searched time of lattice w, respectively. Thus, the AoI value of the lattice grows linearly with the timespan since it was last searched, up to a maximum value. Since UAV continuously searches the target during the search phase, it must update the real-time lattice information table C. Herein, the UAV updates the stored AoI for lattice w

$$
\begin{array} { r } { A _ { w } ( t ) = \left\{ ^ { \operatorname* { m i n } \big \{ A _ { w } ( t - 1 ) + \kappa \times \varDelta t , A _ { \mathrm { m a x } } \big \} , \quad w \not \in \mathcal { V } _ { A } ( t ) , } _ { \mathrm { 0 } , } \right. } \\ { \mathrm { 0 , ~ } \qquad w \in \zeta _ { A } ( t ) , } \end{array}\tag{6}
$$

where the set -A = {w | {xA â xw â¤ h Â· tan Î¸& $\| y ^ { \mathrm { A } } - y _ { w } \| \leq h \cdot \tan \theta \} , w \in \Omega \}$ indicates that lattice w satisfies the search condition at the moment $t ,$ which means that the AoI of lattice w stored in UAV is returned to zero. If lattice w is not searched, the current AoI will increase over time. The metric for the environment search can be expressed by the average AoI of the environment at time t [5], [27]

$$
\overline { { A } } ( t ) = \frac { \sum _ { w = 1 } ^ { L _ { \iota } } A _ { w } ( t ) } { L _ { \iota } \times A _ { \operatorname* { m a x } } } .\tag{7}
$$

## E. Obstacle-Avoidance and Turbulence Models

In oceanic environments, obstacles pose a threat to the safe navigation of USV and UUVs. These vehicles utilize sonar technology to detect underwater obstacles and assess the success of the hunting mission. Thus, we set the maximum detection distances of UUV and USV as $r _ { a }$ . Subsequently, given that potential field theory is widely used for obstacle avoidance, we apply an improved artificial potential field method to ensure the safety of USV and UUVs during target hunting [28], [29]. Therefore, for vehicle $j , \forall j \in V$ , the improved field of obstacle and target is formulated as

$$
\begin{array} { r } { U _ { k } = \left\{ \begin{array} { l l } { \frac { 1 } { 2 } k _ { r e p 1 } \left( \frac { 1 } { d _ { k , j } } - \frac { 1 } { r _ { d } } \right) ^ { 2 } d _ { j , \mathrm { T } } ^ { n } + \frac { 1 } { 2 K } \chi d _ { j , \mathrm { T } } ^ { 2 } , } & { \exists d _ { k , j } \le r _ { d } , } \\ { \frac { 1 } { K } \chi r _ { d } d _ { j , \mathrm { T } } , } & { \forall d _ { k , j } > r _ { d } , } \end{array} \right. } \end{array}\tag{8}
$$

where $d _ { k , j } = \| P _ { k } - P _ { j } \|$ and $d _ { j , \mathrm { T } } = \| \boldsymbol { P } _ { j } - \boldsymbol { T } \| . \boldsymbol { k } _ { r e p 1 }$ represents the repulsion factor, Ï and $r _ { d }$ denote the attraction factor and repulsive range, and n is a positive number. Furthermore, the total potential field of the obstacle set K and the target is $\begin{array} { r } { U _ { K } = \dot { \sum _ { k = 1 } ^ { K } } U _ { k } } \end{array}$

The oceanic environment contains currents, waves, vortices, and other factors that continuously influence the real-time movement of USVs and UUVs. A complex vortex field is formed by the superposition of all sub-vortex fields. Therefore, we use the vortex model based on Navier-Stokes equations to construct the vortice environment2, and the ocean current field is formulated as [31]

$$
\frac { \partial \omega } { \partial t } + ( \vec { V } _ { c } \nabla ) \omega = \rho \Delta \omega ,\tag{9}
$$

where $\vec { V _ { c } } = \left( V _ { x } , V _ { y } \right)$ , Ï and Ï represent the velocity field, the vorticity of the vortex, and the fluid viscosity, respectively. Besides, â is the gradient operator, and $\Delta$ represents the Laplacian operator. To simplify the Navier-Stokes equation [32], we concisely describe the vortex field model of vortex as

$$
\left\{ \begin{array} { l l } { V _ { x } ( \pmb { P } _ { j } ) = - \frac { \Theta \cdot ( y _ { j } - y _ { 0 } ) } { 2 \pi \left\| \pmb { P } _ { j } ^ { 2 } - \pmb { P } _ { 0 } \right\| ^ { 2 } } \left( 1 - e ^ { - \frac { \left\| \pmb { P } _ { j } ^ { 2 } - \pmb { P } _ { 0 } \right\| ^ { 2 } } { \varrho ^ { 2 } } } \right) , } \\ { V _ { y } ( \pmb { P } _ { j } ) = \frac { \Theta \cdot ( x _ { j } - x _ { 0 } ) } { 2 \pi \left\| \pmb { P } _ { j } ^ { 2 } - \pmb { P } _ { 0 } \right\| ^ { 2 } } \left( 1 - e ^ { - \frac { \left\| \pmb { P } _ { j } ^ { 2 } - \pmb { P } _ { 0 } \right\| ^ { 2 } } { \varrho ^ { 2 } } } \right) , } \end{array} \right.\tag{10}
$$

and

$$
\omega ( P _ { j } ) = \frac { \Theta } { \pi \varrho ^ { 2 } } e ^ { - \frac { \left\| P _ { j } - P _ { 0 } \right\| ^ { 2 } } { \varrho ^ { 2 } } } ,\tag{11}
$$

where $P _ { j } ^ { 2 } = P _ { j } ( x , y ) , \forall j \in V$ , denotes the position of vehicle $j ,$ and $\dot { P _ { 0 } }$ is the coordinates of the center of the Lamb vortex. Besides, Î and $\varrho$ represent the vortex strength and the radius of the Lamb vortex, respectively. Furthermore, the total velocity field of the vortex set N in the oceanic environment is modeled as

$$
\vec { V } _ { N } = \sum _ { n = 1 } ^ { N } \vec { V } _ { n } .\tag{12}
$$

The motion velocity of vehicle $j$ with original velocity $\vec { V } _ { j o }$ in the oceanic environment with obstacles and vortices is expressed to be

$$
\vec { V } _ { j } = \vec { V } _ { j o } - \vec { V } _ { c } , \forall j \in V .\tag{13}
$$

According to the classical computational fluid dynamics theory [33], the moving resistance of vehicle j is expressed as

$$
F _ { j } = \frac { 1 } { 2 } \rho C _ { a , j } C _ { d , j } \left. \left. \vec { V } _ { j } ( \pmb { P } _ { j } ) \right. \right. ^ { 2 } ,\tag{14}
$$

where $\rho$ and $C _ { d , j }$ indicate the seawater density and vehicle propulsion efficiency coefficient, respectively, and $C _ { a , j }$ is the equivalent forward area of vehicle $j .$ . Moreover, vehicle j should avoid the dangerous areas of vortex. According to (8), we model the repulsive potential field of vortex set N as

$$
\begin{array}{c} \begin{array} { r } { U _ { N } = \left\{ \sum _ { n = 1 } ^ { N } \frac { 1 } { 2 } k _ { r e p 2 } \left( \frac { 1 } { d _ { n , j } } - \frac { 1 } { r _ { s } } \right) ^ { 2 } d _ { j , \mathrm { T } } ^ { n } , \quad \exists d _ { n , j } \leq r _ { s } , \right.} \\ { 0 , \qquad \forall d _ { n , j } > r _ { s } , } \end{array}   \end{array}\tag{15}
$$

where $d _ { n , j } = \| P _ { n } - P _ { j } ^ { 2 } \|$ and $k _ { r e p 2 }$ represents the repulsion factor. $r _ { s }$ denotes the distance at which the vehicle perceives the dangerous area.

To describe the safety distance for USV and UUVs, we define the safety distance of vehicle $j ,$ , which is denoted as

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { d _ { v , j } = \operatorname* { m i n } \big \{ \| P _ { j } ( x , y ) - P _ { n } ( x , y ) \| - r _ { n } ^ { \mathrm { v } } \big \} > 0 , \forall j \in V , } \\ { d _ { o , j } = \operatorname* { m i n } \big \{ \| P _ { j } - P _ { k } \| - r _ { k } ^ { \mathrm { O } } \big \} > 0 , \forall j \in V , } \end{array} \right. } \end{array}\tag{16}
$$

where $r _ { k } ^ { \mathrm { O } } , \forall k \in K$ is the radius of the obstacle $k ,$ and $r _ { n } ^ { \mathrm { V } } , \forall n \in$ N is the dangerous area radius of vortex n. Specifically, vehicle j canât come out of the danger area of vortex n once it enters. Furthermore, $d _ { o , j }$ represents the obstacle safety distance for USV and UUVs, which is the closest distance from the vehicleâs current position to the obstacle k. Consequently, $d _ { v , j }$ is the vortex safety distance for USV and UUVs, defined as the shortest distance between the vehicleâs current position and the vortex n. Moreover, if (16) is satisfied, the USV and UUVs meet the safe navigation.

## F. Energy Consumption Model

The total energy consumption of the 3U network arises from UAV, USV, and UUV, with the majority of energy use stemming from motion and communication activities. Additionally, the communication energy consumption is negligible compared to the motion energy consumption [34]. Therefore, we focus on analyzing the motion energy consumption of all vehicles as follows.

1) UAV: The rotary-wing UAV is set to fly at a height h. Therefore, the UAV must overcome both resistance and gravity during its motion. According to [35], we can derive the propulsion power of a UAV with velocity $\vec { V } ^ { \mathrm { A } }$ at moment t as

$$
\left\{ \begin{array} { l l } { P _ { \mathrm { A } } ( \vec { V } ^ { \mathrm { A } } ( t ) ) = \hat { P } _ { 0 } ( \vec { V } ^ { \mathrm { A } } ( t ) ) + \hat { P } _ { i } ( \vec { V } ^ { \mathrm { A } } ( t ) ) + \hat { P } _ { a } ( \vec { V } ^ { \mathrm { A } } ( t ) ) , } \\ { \hat { P } _ { 0 } ( \vec { V } ^ { \mathrm { A } } ( t ) ) = P _ { 0 } \left( 1 + \frac { 3 \left\| \vec { V } ^ { \mathrm { A } } ( t ) \right\| ^ { 2 } } { U _ { \mathrm { i p } } ^ { 2 } } \right) , } \\ { \hat { P } _ { i } ( \vec { V } ^ { \mathrm { A } } ( t ) ) = P _ { i } \left( \sqrt { 1 + \frac { \left\| \vec { V } ^ { \mathrm { A } } ( t ) \right\| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \left\| \vec { V } ^ { \mathrm { A } } ( t ) \right\| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { \frac 1 2 } , } \\ { \hat { P } _ { a } ( \vec { V } ^ { \mathrm { A } } ( t ) ) = \frac { 1 } { 2 } \eta \tau _ { 0 } \varphi _ { 0 } \hat { A } \left\| \vec { V } ^ { \mathrm { A } } ( t ) \right\| ^ { 3 } . } \end{array} \right.\tag{17}
$$

In (17), the blade profile power $\hat { P } _ { 0 } ( \vec { V } ^ { \mathrm { A } } ( t ) )$ ), induced power $\hat { P } _ { i } ( \vec { V } ^ { \mathrm { A } } ( t ) )$ ), and parasite power $\hat { P } _ { a } ( \vec { V } ^ { \mathrm { A } } ( t ) )$ comprise the propulsion power. Besides, $P _ { 0 }$ and $P _ { i }$ represent the blade profile power and induced power in hovering status, respectively. Specifically, $U _ { \mathrm { t i p } }$ is the tip velocity of the rotor blade and $v _ { 0 }$ denotes the average rotor velocity in the hovering state. Morever, Î· and $\tau _ { 0 }$ are the air density and rotor solidity, respectively, and $\varphi _ { 0 }$ and AË indicate the fuselage drag ratio and rotor disc area, respectively.

2) USV: The energy consumption of USV is primarily used to maintain velocity ${ \dot { V } } ^ { \mathrm { { S } } }$ relative to the water current [31]. According to (13) and (14), we calculate the electrical power generated by the moving USV at moment t as

$$
P _ { \mathrm { S } } ( \vec { V } ^ { \mathrm { S } } ( t ) ) = \left. F ^ { \mathrm { S } } ( t ) \cdot \vec { V } ^ { \mathrm { S } } ( \boldsymbol { S } ( t ) ) \right. .\tag{18}
$$

3) UUV: Similarly, the energy consumption of the UUV i is primarily used to maintain velocity ${ \vec { V } } _ { i } ^ { \mathrm { U } }$ relative to the water current. According to (13) and (14), we can calculate the energy consumption power of the moving UUV i as

$$
P _ { \mathrm { U _ { i } } } ( \vec { V } _ { i } ^ { \mathrm { U } } ( t ) ) = \left. F _ { i } ^ { \mathrm { U } } ( t ) \cdot \vec { V } _ { i } ^ { \mathrm { U } } ( \pmb { P } _ { i } ( t ) ) \right. .\tag{19}
$$

Consequently, the total energy consumed by the 3U network during performing the mission is expressed as

$$
\begin{array} { r } { E _ { s y s } = \sum _ { 0 } ^ { T _ { h } } \varDelta t \cdot P _ { \mathrm { A } } + \sum _ { T _ { s } } ^ { T _ { h } } \varDelta t \cdot P _ { \mathrm { S } } + \sum _ { i = 1 } ^ { M } \sum _ { T _ { s } } ^ { T _ { h } } \varDelta t \cdot P _ { \mathrm { U _ { i } } } . } \end{array}\tag{20}
$$

## G. Target Escape Strategy

We consider that the target employs a gaming strategy for its escape and can perceive all vehicles in the 3U network [36]. Consequently, during the target-search phase, we define the targetâs escape strategy as

$$
\vec { V } ^ { \mathrm { T } } = V ^ { \mathrm { T } } \cdot \vec { e } _ { 1 } ,\tag{21}
$$

where $\vec { e } _ { 1 } ( t ) = ( x ^ { \mathrm { T } } - x ^ { \mathrm { A } } , y ^ { \mathrm { T } } - y ^ { \mathrm { A } } , 0 )$ is employed so that the target can avoid the search from UAV. Moreover, in the target

hunting phase, the target dynamics can be simplified as

$$
\left\{ \begin{array} { l l } { \vec { V } ^ { \mathrm { T } } = V ^ { \mathrm { T } } \cdot \vec { e } _ { 2 } , } \\ { \vec { e } _ { 2 } = \frac { T - C } { \lVert T - C \rVert } , } \end{array} \right.\tag{22}
$$

where $\begin{array} { r } { C = \frac { 1 } { M } \sum P _ { i } , i \in U } \end{array}$ denotes the center of the UUV swarm at moment $T _ { s }$ , and the target employs this escape strategy to escape desperately from the hunting of the UUV swarm.

## H. Optimization Problem Formulation

Our optimization objectives are minimizing the energy consumption and execution duration to complete the UTH mission. The constraints include AoI, network connectivity, vehicle safety, and mobility requirements. To efficiently complete the UTH mission, vehicle mË generates corresponding action $a _ { \tilde { m } } ( t )$ and reward $r _ { \tilde { m } } ( t )$ based on its own observed state $o _ { \tilde { m } } ( t )$ and policy $\pi _ { \phi _ { \tilde { m } } }$ . Thus, the optimization problem is described as

$$
O P \mathrm { : \quad } \operatorname* { m i n } \left( E _ { s y s } , T _ { h } \right)\tag{23a}
$$

$$
\begin{array} { r } { \mathrm { s . t . } \quad A \le A _ { w } ( t ) \le A _ { \operatorname* { m a x } } , \forall w \in \Omega , } \end{array}\tag{23b}
$$

$$
d _ { o , j } > 0 , \forall j \in V , \forall k \in K ,\tag{23c}
$$

$$
d _ { v , j } > 0 , \forall j \in V , \forall n \in N ,\tag{23d}
$$

$$
V _ { \operatorname* { m a x } } ^ { \mathrm { U } } > V _ { \operatorname* { m a x } } ^ { \mathrm { T } } , p _ { \operatorname* { m a x } } ^ { \mathrm { U } } < p _ { \operatorname* { m a x } } ^ { \mathrm { T } } , q _ { \operatorname* { m a x } } ^ { \mathrm { U } } < q _ { \operatorname* { m a x } } ^ { \mathrm { T } } .\tag{23e}
$$

Equation (23a) denotes the optimization objective, including the networkâs energy consumption $E _ { s y s }$ and mission duration $T _ { h }$ . Besides, (23b) represents the boundary constraints of the real-time AoI stored by UAV, which requires UAV to be constantly updated and maintained. Furthermore, (23c) and (23d) represent the real-time safe distances of USV and UUVs from obstacles and vortices, respectively, which guarantee the safety of USV and UUVs during hunting missions. Moreover, (23e) represents the mobility constraints of UUVs and the target.

## IV. ALGORITHM DESIGN

In this section, we first model the UTH mission as Markov decision processes (MDPs). Then, we elaborately design the reward function. Finally, we present detail design of the proposed AE-MVTD3-based algorithm.

## A. State Space and Action Space

The OP seeks to find the optimal solution for multiple objectives under various constraints, a task typically intractable for traditional optimization algorithms. Specifically, we transform each phase into an MDP, which can be represented as a tuple [37]

$$
\Phi = ( S , { \mathcal { A } } , { \mathcal { P } } , { \mathcal { R } } , \gamma ) ,\tag{24}
$$

where $\mathcal { P }$ represents the state transition probability, R represents the reward function, and $\gamma \in ( 0 , 1 )$ is the discount factor. Consequently, the state space $\boldsymbol { s }$ and action space A of all vehicles are denoted as

State Space: At moment t, the observed state space of vehicle mË in the UTH mission, $o _ { \tilde { m } } ( t ) \in \mathcal { S } ( t )$ , is denoted as

$$
\begin{array} { r } { o _ { \tilde { m } } ( t ) = \Bigl \{ \hat { P } _ { \tilde { m } } ( t ) , P _ { \tilde { m } , k } ( t ) , P _ { \tilde { m } , n } ( t ) , \pmb { T } ( t ) , \forall k \in \pmb { K } , \forall n \in \pmb { N } \Bigr \} , } \end{array}\tag{25}
$$

where $\hat { P } _ { \tilde { m } }$ is the motion states of vehicle mË and its connected vehicles. $P _ { \tilde { m } , k }$ and $P _ { \tilde { m } , n }$ represent the positions of obstacle k and vortex n observed by vehicle $\tilde { m } ,$ respectively. T indicates the position of the target. UAVâs observation includes its motion state and view information.

Action Space: At moment t, vehicle mË chooses the action $\pmb { a } _ { \tilde { m } } ( t ) \in \mathcal { A } ( t )$ based on the observed state, where $\mathbf { } a _ { \tilde { m } } ( t )$ is expressed as

$$
\pmb { a } _ { \tilde { m } } ( t ) = \left\{ \dot { V } _ { \tilde { m } } ( t ) , p _ { \tilde { m } } ( t ) , q _ { \tilde { m } } ( t ) \right\} ,\tag{26}
$$

where $\dot { V } _ { \tilde { m } }$ is the acceleration of vehicle mË . In addition, $p _ { \tilde { m } }$ and $q _ { \tilde { m } }$ are the pitch and yaw angular velocities, respectively.

## B. Reward Function Design

The design of the reward function needs to consider the search and facilitate the obstacle and vortexâs dangerous aera avoidance, energy saving, communication connectivity, collaboration hunting, and collision avoidance. Therefore, we design reward functions based on the constraints and optimization objectives outlined in the previous sections. These functions help the vehicles learn optimal strategies.

AoI-based Search Rewards: In the search phase, to prevent UAV from halting its search and to encourage them to approach areas requiring attention, we use the reduction in the average stored AoI as a search reward for UAV

$$
\begin{array} { r } { r } { r _ { 1 } ( t ) = \left\{ \begin{array} { c c } { R _ { \mathrm { d e t } } , } & { \mathrm { t a r g e t d e t e c t e d } , } \\ { \frac { \sum _ { w = 1 } ^ { L _ { \iota } } \left\{ l - c l i p _ { 0 } ^ { A _ { \mathrm { m a x } } } A _ { w } ( t ) \right\} } { L _ { \iota } A _ { \mathrm { m a x } } } } & { \mathrm { o t h e r w i s e } , } \end{array} \right. } \end{array}\tag{27}
$$

where $R _ { \mathrm { d e t } }$ represents the reward for the target being detected. To minimize the average AoI, the UAV progressively explores unknown areas to search the target.

Obstacle and Vortexâs Dangerous Area Avoidance: In order to ensure that USV and UUVs avoid obstacles and dangerous areas, we define the movement rewards for dangerous areas of the vortex and obstacles as

$$
r _ { 2 } ^ { u } ( t ) = \left\{ R _ { \mathrm { u s f } } ^ { \mathrm { U } } , \quad u = \mathrm { U } _ { i } \mathrm { d e n o t e s } \mathrm { U U V } \mathrm { i } , \right.\tag{28}
$$

where $R _ { \mathrm { u s f } } ^ { \mathrm { U } }$ and $R _ { \mathrm { u s f } } ^ { \mathrm { S } }$ are the rewards for the unsafe movement of UUV and USV, respectively.

Energy Saving: All vehicles expend energy during search and hunting missions. To incentivize the 3U network to complete the mission efficiently, we define the energy consumption reward of vehicles as

$$
r _ { 3 } ^ { u } ( t ) = \left\{ \begin{array} { c c } { { - P _ { \mathrm { A } } ( t ) , } } & { { u = \mathrm { A d e n o t e s ~ U A V } , } } \\ { { - P _ { \mathrm { S } } ( t ) , } } & { { u = \mathrm { S } \mathrm { d e n o t e s ~ U S V } , } } \\ { { - P _ { \mathrm { U } _ { i } } ( t ) , } } & { { u = \mathrm { U } _ { i } \mathrm { d e n o t e s ~ U U V } \ i . } } \end{array} \right.\tag{29}
$$

Communication Connectivity: The network must maintain communication connectivity at all times during the mission. Therefore, we define the communication reward in the 3U

network as

$$
r _ { 4 } ( t ) = d _ { \mathrm { A , S } } ( t ) ,\tag{30}
$$

and

$$
r _ { 5 } ^ { \mathrm { U } _ { \mathrm { i } } } ( t ) = \sum _ { j = 1 , i \neq j } ^ { \mathcal { H } } d _ { i , j } ( t ) .\tag{31}
$$

Collaboration Hunting: UAV need reduce search time. Target hunting, the primary function of the 3U network, is performed by the UUVs. Additionally, USV needs collaborative movements. To incentivize UUVs to successfully complete the mission, we correspondingly formulate the reward to guide the movements of UUVs and USV

$$
r _ { 6 } ^ { u } ( t ) = \left\{ \begin{array} { c c } { R _ { \mathrm { m o v } } ^ { \mathrm { U } _ { i } } ( t ) + \hbar \times \Xi ( t ) , } & { u = \mathrm { U } _ { i } \mathrm { d e n o t e s ~ U U V } \ i , } \\ { R _ { \mathrm { m o v } } ^ { \mathrm { S } } ( t ) , } & { u = \mathrm { S } \mathrm { d e n o t e s ~ U S V } , } \\ { R _ { \mathrm { t } } ^ { \mathrm { S } } ( t ) , } & { u = \mathrm { A d e n o t e s ~ U A V } , } \end{array} \right.\tag{32}
$$

where $R _ { \mathrm { m o v } } ^ { \mathrm { U } _ { i } } ( t )$ and $R _ { \mathrm { m o v } } ^ { \mathrm { S } } ( t )$ represent the corresponding vehiclesâ movement rewards. Furthermore, $\hbar , \Xi ( t )$ , and $R _ { \mathrm { t } } ^ { \mathrm { S } } ( t )$ are the adjustment factor, duration of UUV hunting, and search duration, respectively.

Collision Avoidance: UUVs should avoid collisions with each other. Thus, we define this reward as

$$
r _ { 7 } ^ { \mathrm { U } _ { i } } ( t ) = \left\{ \begin{array} { r l } { R _ { \mathrm { c o l } } , } & { { } d _ { i , j } < d _ { \mathrm { c o l } } , } \\ { R _ { \mathrm { a v o } } , } & { { } \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{33}
$$

where $R _ { \mathrm { c o l } }$ and $d _ { \mathrm { c o l } }$ denote the collision reward and the collision distance, respectively. $R _ { \mathrm { a v o } }$ is collision avoidance reward.

Safe Navigation and Mission Success: In order to ensure that USV and UUVs navigate safely in the oceanic environment as well as rewarding mission successes, we define the corresponding rewards as

$$
r _ { 8 } ( t ) = \left\{ \begin{array} { c c } { { R _ { \mathrm { s a f } } , } } & { { \mathrm { i f ~ U S V ~ o r ~ U U V ~ i s ~ u n s a f e } , } } \\ { { R _ { \mathrm { h u n } } , } } & { { \mathrm { i f ~ m i s s i o n ~ s u c c e e d s } , } } \end{array} \right.\tag{34}
$$

where $R _ { \mathrm { s a f } }$ is a reward for the unsafe navigation of UUV and USV. $R _ { \mathrm { h u n } }$ represents the mission success reward.

Therefore, at moment t, the total reward obtained for the 3U network can be summarized by weighting the above sub-rewards

$$
\begin{array} { r l } & { \left( r ( t ) = \zeta ^ { 0 } r ^ { \mathrm { { A } } } ( t ) + \lambda ^ { 0 } r ^ { \mathrm { { S } } } ( t ) + \sum _ { i = 1 } ^ { M } o ^ { 0 } r _ { i } ^ { \mathrm { { U } } } ( t ) , \right. } \\ & { \left. r ^ { \mathrm { { A } } } ( t ) = \zeta ^ { 1 } r _ { 1 } ( t ) + \zeta ^ { 2 } r _ { 3 } ^ { \mathrm { { A } } } ( t ) + \zeta ^ { 3 } r _ { 4 } ( t ) + \zeta ^ { 4 } r _ { 6 } ^ { \mathrm { { A } } } ( t ) , \right. } \\ & { \left. r ^ { \mathrm { { S } } } ( t ) = \lambda ^ { 1 } r _ { 2 } ^ { \mathrm { { S } } } ( t ) + \lambda ^ { 2 } r _ { 3 } ^ { \mathrm { { S } } } ( t ) + \lambda ^ { 3 } r _ { 4 } ( t ) + \lambda ^ { 4 } r _ { 6 } ^ { \mathrm { { S } } } ( t ) + \lambda ^ { 5 } r _ { 8 } ( t ) , \right. } \\ & { \left. r _ { i } ^ { \mathrm { { U } } } ( t ) = o ^ { 1 } r _ { 2 } ^ { \mathrm { { U } } _ { \mathrm { { i } } } } ( t ) + o ^ { 2 } r _ { 3 } ^ { \mathrm { { U } _ { \mathrm { i } } } } ( t ) + o ^ { 3 } r _ { 5 } ^ { \mathrm { { U } _ { \mathrm { i } } } } ( t ) \right. } \\ & { \left. \qquad + o ^ { 4 } r _ { 6 } ^ { \mathrm { { U } _ { \mathrm { i } } } } ( t ) + o ^ { 5 } r _ { 7 } ^ { \mathrm { { U } _ { \mathrm { i } } } } ( t ) + o ^ { 6 } r _ { 8 } ( t ) , \right. } \end{array}\tag{35}
$$

where r is the total reward. $r ^ { \mathrm { A } } , r ^ { \mathrm { S } }$ , and $r _ { i } ^ { \mathrm { U } }$ represent the rewards of UAV, USV, and UUV i, respectively. Besides, Î¶, Î» and o are the weighting factors of the sub-awards, respectively.

## C. AE-MVTD3 Algorithm

The framework of the proposed AE-MVTD3 algorithm is shown in Fig. 2, where each vehicle is regarded as an independent agent. Within this framework, the input to the actor network is the local observation of every vehicle, with each vehicle assigned a distinct reward. The observation and action of each vehicle vary over time. Specifically, in the search phase, the stored AoI information in A(t) varies over time, which drives UAV to search the target and update the map information continuously. Moreover, in the hunting phase, the USV and UUVs determine their next actions based on oceanic environment data collected via sonar and target information provided by UAV. During the training phase, all vehicles are trained based on observed information. In the execution phase, they use their respective actor networks to perform the UTH mission. For simplicity, the action space of vehicle can be converted to accelerations.

<!-- image-->  
Fig. 2. The AE-MVTD3 framework in UTH mission.

The actor and critic networks are employed to construct the AE-MVTD3 algorithm. The critic network Q(Â·) represents the evaluation result of the observed state $s = \{ o _ { 1 } , \ldots , o _ { \mathcal { H } } \}$ producing the corresponding action $a = \{ a _ { 1 } , \ldots , a _ { \mathcal { H } } \}$ based on the actor network Ï(Â·). Each vehicle learns a policy to maximize the discount return, which can be expressed as $\begin{array} { r } { \dot { J ^ { t } } = \sum _ { \mathrm { t = 0 } } ^ { T } \gamma ^ { \mathrm { t } } r ^ { t + \mathrm { t } } } \end{array}$ The AE-MVTD3 algorithm uses clipped double-Q learning to solve the suboptimal updating problem caused by overestimating the Q value. For vehicle m, âm â V , the smaller value between the twin estimates $Q _ { \theta _ { m , } ^ { Q } }$ and $Q _ { \theta _ { m , 2 } ^ { Q } }$ is used to compute the target value of vehicle m as

$$
y _ { m } = r _ { m } + \gamma \operatorname* { m i n } _ { i = 1 , 2 } Q _ { \theta _ { m , i } ^ { Q ^ { \prime } } } ( s ^ { \prime } , a ^ { \prime } ) ,\tag{36}
$$

where $Q _ { \theta _ { m . . } ^ { Q ^ { \prime } } } .$ ,i denotes the i-th target critic network. Î³ is the discount factor, which connects the next observed state $s ^ { \prime }$ and action $a ^ { \prime }$ to the current step. To avoid the local optimum, the vehicle balances exploration and exploitation by adding noise while exploring the environment, which allows achieving a better action to be expressed as

$$
\begin{array} { r } { \left\{ a _ { m } ^ { \prime } = \pi _ { \phi _ { m } ^ { \prime } } ( o _ { m } ^ { \prime } ) + \epsilon , \right. } \\ { \left. \epsilon \sim c l i p \left( \mathcal { N } ( 0 , \sigma ^ { 2 } ) , - c , c \right) , \right. } \end{array}\tag{37}
$$

Algorithm 1: AE-MVTD3 Algorithm (Hunting Phase).   
1: Initialize network parameters of all vehicles and   
experience replay buffer Î¨.   
2: for $w = 1$ to $L _ { \iota }$ do   
3: Initialize AoI value of lattice w.   
4: end for   
5: for $m = 1$ to H do   
6: Initialize position and velocity of vehicle m.   
7: end for   
8: Initialize target position T and velocity $V ^ { \mathrm { T } }$   
9: Reset the environment and state of vehicle m.   
10: for t = 0 to T do   
11: Based on observed state $o _ { m } .$ , the vehicle m obtains   
action $a _ { m } = \pi _ { \phi _ { m } } ( o _ { m } ) + \epsilon .$   
12: Execute action a(t), obtain reward r(t), and new   
state $s ( t + 1 )$   
13: Store transition $\{ s ( t ) , r ( t ) , a ( t ) , s ( t + 1 ) \}$ into Î¨.   
14: Randomly sample a minibatch samples j from Î¨.   
15: // Parallel learning.   
ym $ r _ { m } + \gamma \mathrm { m i n } _ { i = 1 , 2 } Q _ { \theta _ { m . i } ^ { Q ^ { \prime } } } ( s ^ { \prime } , a ^ { \prime } ) ,$   
16: Loss $( \theta _ { m , i } ^ { Q } ) \gets \mathbb { E } [ ( Q _ { \theta _ { m } ^ { Q } } \mathrm { \Pi } _ { i } ( s , a ) - y _ { m } ) ^ { 2 } ] ,$   
17: // Delayed policy updating.   
$\nabla _ { \phi _ { m } } J ( \phi _ { m } ) \gets \mathbb { E } \big [ \nabla _ { a _ { m } } Q _ { \theta _ { m , 1 } ^ { Q } } ( s , a ) \big | _ { a _ { m } = \pi _ { \phi _ { m } } ( o _ { m } ) }$   
$\times ~ \nabla \phi _ { m } ~ \pi _ { \phi _ { m } } ( a _ { m } \mid o _ { m } ) ] .$   
18: $\phi _ { \underline { { { m } } } } ^ { \prime }  \tau \phi _ { m } + ( 1 - \tau ) \phi _ { m } ^ { \prime } ,$   
19: $\theta _ { m , i } ^ { Q ^ { \prime } }  \tau \theta _ { m , i } ^ { Q } + ( 1 - \tau ) \theta _ { m , i } ^ { Q ^ { \prime } } , i = 1 , 2 .$   
20: end for

where $\pi _ { \phi _ { m } ^ { \prime } }$ denotes the target actor network. Besides, noise  smoothes the Q value. $\sigma ^ { 2 }$ and c denote the noise variance and clipped threshold, respectively. Thus, the loss function considering improved artificial potential field in the hunting phase algorithm is denoted as

$$
L o s s ( \theta _ { m , i } ^ { Q } ) = \mathbb { E } [ ( Q _ { \theta _ { m , i } ^ { Q } } ( s , a ) - y _ { m } ) ^ { 2 } ] .\tag{38}
$$

Consequently, the actor network of vehicle m is updated by the policy gradient method by

$$
\begin{array} { r l } & { \nabla \phi _ { m } J \big ( \phi _ { m } \big ) = \mathbb { E } \big [ \nabla a _ { m } Q _ { \theta _ { m , 1 } ^ { Q } } ( s , a ) \big | _ { a _ { m } = \pi _ { \phi _ { m } } ( o _ { m } ) } } \\ & { \qquad \times \ : \bigtriangledown \phi _ { m } \pi _ { \phi _ { m } } \big ( a _ { m } \mid o _ { m } \big ) \big ] , } \end{array}\tag{39}
$$

where $o _ { m }$ represents the observed state of vehicle m. The clipped double-Q learning method allows the target network to have a smaller Q-value variance. Furthermore, the target actor and critic networks gradually update the network parameters as

$$
\left\{ \begin{array} { l } { { \phi _ { m } ^ { \prime } = \tau \phi _ { m } + ( 1 - \tau ) \phi _ { m } ^ { \prime } , } } \\ { { \theta _ { m , i } ^ { Q ^ { \prime } } = \tau \theta _ { m , i } ^ { Q } + ( 1 - \tau ) \theta _ { m , i } ^ { Q ^ { \prime } } , i = 1 , 2 , } } \end{array} \right.\tag{40}
$$

where $\tau < 1$ is the update rate. The hunting phase of the $\mathrm { A E _ { \overline { { \mathbf { \delta } } } } }$ MVTD3 algorithm is summarized in Algorithm 1. The complexity is $\mathcal { O } ( \mathcal { H } \times ( 2 \times D _ { C } \times W _ { C } ^ { 2 } + D _ { A } \times W _ { A } ^ { 2 } ) )$ , where $D _ { C } \left( D _ { A } \right)$ represents the number of layers of the critic (actor) network and $W _ { C } \left( W _ { A } \right)$ denotes the number of neurons in the widest layer of the critic (actor) network.

TABLE II EXPERIMENTAL PARAMETERS
<table><tr><td></td><td>Parameters</td><td>Value</td></tr><tr><td></td><td>Numbersof UAVs,UVs,UUVs Viewangle0 ofUAV</td><td> $\overline { { [ 1 , 1 , 3 ] } }$  45Â°</td></tr><tr><td></td><td></td><td>40m</td></tr><tr><td></td><td>Flight altitude h of UAV</td><td></td></tr><tr><td></td><td>Velocity range VA of UAV</td><td> $[ 0 , 5 ] m / s$ </td></tr><tr><td></td><td></td><td> $0 . 7 r a d / s$ </td></tr><tr><td></td><td>Velocity rangeVSof USV</td><td> $[ 0 , 2 ] m / s$ </td></tr><tr><td></td><td>Velocity range  $V ^ { \mathrm { U } } \ \mathrm { o f } \ \mathrm { U U V s }$ </td><td> $0 . 7 r a d / s$ </td></tr><tr><td></td><td>Maximum pitch and yaw</td><td> $[ 0 . 4 , 2 ] m / s$ </td></tr><tr><td></td><td>angular velocity  $p _ { \operatorname* { m a x } } ^ { \cup } , q _ { \operatorname* { m a x } } ^ { \cup }$ </td><td> $0 . 7 r a d / s , 0 . 7 r a d / s$ </td></tr><tr><td></td><td>Velocity set  $V ^ { \mathrm { { T } } }$  of target Maximum pitch and yaw</td><td> $\{ 0 . 1 2 , 0 . 1 6 , 0 . 2 \} m / s$ </td></tr><tr><td></td><td>angular velocity  $p _ { \operatorname* { m a x } } ^ { \mathrm { T } } , q _ { \operatorname* { m a x } } ^ { \mathrm { T } }$ </td><td> $0 . 8 r a d / s , 0 . 8 r a d / s$ </td></tr><tr><td></td><td>Hunting radius  $b _ { 0 }$ </td><td>4m  $( 4 0 , 8 0 ) m ,$ </td></tr><tr><td>System</td><td></td><td> $( 1 0 0 , 3 0 ) m ,$ </td></tr><tr><td>parameters</td><td>Locations of vortex centers</td><td>(160,150)m,</td></tr><tr><td></td><td></td><td> $( 6 0 , 1 6 0 ) \dot { m }$ </td></tr><tr><td></td><td>Vortex strength </td><td>1</td></tr><tr><td></td><td>Disturbance radius @</td><td>100m</td></tr><tr><td></td><td>Dangerous area radius</td><td>{9,9,9,9} m</td></tr><tr><td></td><td> $\{ r _ { 1 } ^ { \mathrm { V } } , r _ { 2 } ^ { \mathrm { V } } , r _ { 3 } ^ { \mathrm { V } } , r _ { 4 } ^ { \mathrm { V } } \}$  Number N of vortex</td><td>4</td></tr><tr><td></td><td></td><td> $( 1 4 0 , 7 0 , - 7 0 ) m ,$ </td></tr><tr><td></td><td>Locations of obstacle centers</td><td>(100,100,-60)m,</td></tr><tr><td></td><td></td><td> $( 1 1 0 , 1 8 0 , - 8 0 ) m ,$  (190,100,-60) m</td></tr><tr><td></td><td>Obstacle radius</td><td>{16,14,18,16} m</td></tr><tr><td></td><td> $\{ r _ { 1 } ^ { \mathrm { O } } , r _ { 2 } ^ { \mathrm { O } } , r _ { 3 } ^ { \mathrm { O } } , r _ { 4 } ^ { \mathrm { O } } \}$ </td><td></td></tr><tr><td></td><td> $\mathrm { A i r \ d e n s i t y \ } \eta _ { 0 }$ </td><td> $1 . 2 2 5 k g / m ^ { 3 }$ </td></tr><tr><td></td><td> $\mathrm { R o t o r ~ s o l i d i t y } ~ \tau _ { 0 }$ </td><td>0.05</td></tr><tr><td></td><td> $\mathrm { F u s e l a g e ~ d r a g ~ } \varphi _ { 0 }$ </td><td>0.6 1.0</td></tr><tr><td></td><td>Maximum AoI Amax</td><td> $1 0 2 0 k g / m ^ { 3 }$ </td></tr><tr><td></td><td>Seawater density p Propulsion effciency Cd</td><td>0.117</td></tr><tr><td>Number</td><td></td><td>14400</td></tr><tr><td></td><td> $L _ { \iota } \ \mathrm { o f } \ \mathrm { l a t t i c e s }$ </td><td>234m</td></tr><tr><td></td><td>Communication radius rc</td><td></td></tr><tr><td></td><td>Timeintervalâ³t</td><td>1s</td></tr><tr><td></td><td>Training episodes</td><td>150</td></tr><tr><td></td><td>Learning rate lr</td><td> $1 \times 1 0 ^ { - 4 }$ </td></tr><tr><td></td><td>Discounting factor y</td><td>0.99</td></tr><tr><td>AE-MVTD3</td><td>Update rate T</td><td> $5 \times 1 0 ^ { - 3 }$ </td></tr><tr><td>parameters</td><td>Batch size</td><td>64</td></tr><tr><td></td><td>Memory capacity</td><td> $1 \times 1 0 ^ { 6 }$ </td></tr><tr><td></td><td>Clipped threshold c</td><td>0.5</td></tr></table>

## V. SIMULATION RESULTS AND DISCUSSIONS

In the experiments, we consider one UAV, one USV, and three UUVs in the 3U network. Besides, we set the UAV with square view angle $\theta = 4 5 ^ { \circ }$ and flight altitude $h = 4 0 \mathrm { m }$ , and the number of lattices searched in the 2D Cartesian coordinate system is set as 14400. For the velocities of the different vehicles, we set $V ^ { \mathrm { A } } \in [ 0 , 5 ] \mathrm { m } / \mathrm { s } , V ^ { \mathrm { S } } \in [ 0 , 2 ] \mathrm { m } / \mathrm { s } , V ^ { \mathrm { U } } \in [ 0 . 0 4 , 2 ] \mathrm { m } / \mathrm { s } .$ $V ^ { \mathrm { T } } \in [ 0 . 1 2 , 0 . 2 ] \mathrm { { m } / \mathrm { { s } } }$ . Moreover, the parameters $r _ { a }$ and  are set to 100 m. Additionally, the time interval Ît is set as 1s. According to [11], [31], the experimental parameters are provided in Table II. Specifically, in the training phase, the training episodes are 1500 times, the network learning rate lr is (0.5, 1, 2, 2) Ã $1 0 ^ { - 4 }$ , the discount factor parameter Î³ is 0.99, and the soft update rate Ï is chosen as 0.005. Additionally, to illustrate the effectiveness of the proposed scheme, we evaluate its performance against the following state-of-the-art schemes:

MADDPG [25], [38]: In the search phase, the UAV marks the lattice and searches underwater targets. It employs the multiagent deep deterministic policy gradient (MADDPG) algorithm to control the vehicles of the 3U network, and all the vehicles satisfy the constraints above.

MATD3 [39]: In the search phase, the UAV searches underwater targets by full-coverage method. It uses the multi-agent TD3 (MATD3) algorithm to control the vehicles of the 3U network, and all vehicles satisfy the aforementioned constraints.

Fig. 3(a) illustrates the 3D trajectories of all vehicles generated by the proposed algorithm. The vehicles initially start far from the target but eventually converge near it. The UUV swarm and USV gradually approach the target and avoid obstacles and dangerous areas in the hunting phase. Additionally, Fig. 3(b) presents the trajectories of the UUV swarm and underwater target in the hunting phase. Specifically, the distances between UUVs decrease over time as the hunting reward promotes collaborative movement, while the communication reward minimizes the spacing between them. Furthermore, obstacle and dangerous area avoidance rewards keep the vehicle safe.

Fig. 4 illustrates the mission success rates and average AoI at time $T _ { s }$ of the three algorithms. The proposed algorithm has the highest success rate and superior average AoI. This is because it considers energy, dangerous area avoidance, mission success and AoI search rewards compared to baselines. The UTH mission is considered to be a failure if the vehicles run out of energy or fail to navigate safely. Compared to the baseline algorithms, the proposed algorithm performs better in terms of optimizing the average AoI and mission success rate, which demonstrates superior vehicle control and search efficiency, indirectly improving the success rate of target hunting.

Fig. 5 presents the 3U networkâs mission duration and total energy consumption. It is observed that the total energy consumption of the 3U network increases with the targetâs velocity, and the total mission duration also changes accordingly. The proposed algorithm demonstrates lower total energy consumption and shorter mission duration compared to the baseline algorithms. The reason behind this is that higher target velocity adds complexity to the mission, necessitating an expanded search range for UAV and longer tracking distances for the UUV swarm. This increase in complexity leads to higher overall energy consumption and a moderate rise in mission duration. The proposed algorithm defines the rewards related to energy and duration compared to baselines, which allow it to focus on decreasing energy consumption and duration to complete the mission.

Fig. 6 presents the trajectories of the UUV swarm and USV under the environment-aware free (EAF) condition. Specifically, the EAF-based AE-MVTD3 algorithm fails to ensure the safety of UUV swarms and USVs while tracking a target moving at 0.2 m/s, resulting in mission failure. This occurs because the UUV swarm and USV cannot perceive real-time environmental information and focus solely on avoiding collisions with obstacles while tracking the target. Consequently, they move as far away from obstacles as possible during the UTH mission, neglecting the vortex, which led to the UUVs entering the vortexâs danger area.

Fig. 7(a) and (b) demonstrates the USVâs and UUV swarmâs safety distances min $\{ d _ { o , j } , d _ { v , j } \}$ . In the search phase, the UUV swarm and the USV are stationary, so the safety distance remains constant. In the hunting phase, the UUV swarm and the USV collaboratively hunt the target, so the safety distance varies as the vehicles move. Specifically, the USV needs to avoid dangerous areas, while the UUV swarm needs to avoid obstacles and dangerous areas. Compared to the baseline algorithms, the proposed algorithm performs well regarding safety distance. This is because it considers the corresponding rewards, which require that the planned paths are as far away as possible from obstacles and dangerous areas.

<!-- image-->  
(a) 3D trajectories of vehicles in the 3U network.

<!-- image-->  
(b) Top view of the trajectories of the UUVsand target.

Fig. 3. The trajectories of vehicles generated by the proposed algorithm in the 3U network.  
<!-- image-->  
Fig. 4. Mission success rate and average AoI at time Ts of different algorithms.

<!-- image-->  
Fig. 5. Mission duration and total energy consumption versus $V ^ { \mathrm { T } }$ of different algorithms.

<!-- image-->  
Fig. 6. The trajectories of the UUVs, USV and target of EAF-based MVTD3 algorithm.

Fig. 8 shows the closest distance from the UUV swarm to the target, i.e., min $\{ \| P _ { i } - { \pmb T } \| , i \in { \pmb U } \}$ . During the hunting phase, the UUV swarm moves gradually towards the target, which causes the closest distance from the UUV swarm to the target to decrease over time. The proposed algorithm performs better in this aspect than the baseline algorithms. This is because it considers the corresponding rewards in target hunting, which makes the UUV swarms most likely to approach the target quickly.

Fig. 9 shows the average AoI at time $T _ { s }$ versus the growth factor Îº. As Îº increases, the average AoI rises accordingly. The proposed AE-MVTD3 algorithm achieves a lower average AoI, reflecting higher environmental search efficiency. Additionally, the proposed AE-MVTD3 algorithm exhibits a slower growth rate in average AoI compared to baseline algorithms. The reason behind this is that the proposed AE-MVTD3 algorithm possesses AoI-based search rewards, which allow it to focus on the average AoI in the search phase, thus effectively improving the search efficiency and reducing the impact of the growth factor Îº.

<!-- image-->

(a) Safe distances of USV versus mission duration of different algorithms.  
<!-- image-->  
(b) Safe distances of UUV swarm versus mission duration of different algorithms.

Fig. 7. Safe distances of USV and UUV swarm versus mission duration of different algorithms.  
<!-- image-->  
Fig. 8. The closest distance from the UUV swarm to the target of three algorithms.

<!-- image-->  
Fig. 9. Average AoI at time $T _ { s }$ versus growth factor Îº of different algorithms.

## VI. CONCLUSION

In this paper, we have proposed a novel â3U networkâ framework that integrates UAVs, USVs, and UUVs for the UTH mission. By incorporating the concept of AoI into the UAVâs search strategy, we enhanced the timeliness and effectiveness of target detection. We have formulated a constrained multi-objective optimization problem aiming to minimize energy consumption and mission duration while considering the kinematics and dynamics of all vehicles, as well as complex underwater environments characterized by obstacles and turbulence. To solve this problem, we have developed the AE-MVTD3 algorithm, which optimizes control policies for heterogeneous vehicles under mobility limitations, safety requirements, and connectivity constraints. Experimental results have demonstrated that the proposed method outperforms state-of-the-art schemes across diverse complex scenarios, achieving higher success rates and operational efficiency. In the future, we will work on 3U networks containing multiple UAVs, multiple USVs, and multiple UUVs to facilitate more complex underwater missions.

## REFERENCES

[1] C. Lin, G. Han, J. Jiang, C. Li, S. B. H. Shah, and Q. Liu, âUnderwater pollution tracking based on software-defined multi-tier edge computing in 6G-based underwater wireless networks,â IEEE J. Sel. Areas Commun., vol. 41, no. 2, pp. 491â503, Feb. 2023.

[2] S. Zhu, G. Han, and C. Lin, âA software-defined MARL-based architecture for AUV cluster network to enable cooperative and smart underwater target tracking,â in IEEE Wireless Commun., vol. 31, no. 6, pp. 56â62, Dec. 2024, doi: 10.1109/MWC.001.2400025.

[3] J. Ni, L. Yang, L. Wu, and X. Fan, âAn improved spinal neural systembased approach for heterogeneous AUVs cooperative hunting,â Int. J. Fuzzy Syst., vol. 20, pp. 672â686, 2018.

[4] W. Wei, J. Wang, J. Du, Z. Fang, Y. Ren, and C. L. P. Chen, âDifferential game-based deep reinforcement learning in underwater target hunting task,â IEEE Trans. Neural Netw. Learn. Syst., vol. 36, no. 1, pp. 462â474, Jan. 2025, doi: 10.1109/TNNLS.2023.3325580.

[5] Z. Wang, J. Du, C. Jiang, Z. Xia, Y. Ren, and Z. Han, âTask scheduling for distributed AUV network target hunting and searching: An energy-efficient AoI-aware DMAPPO approach,â IEEE Internet Things J., vol. 10, no. 9, pp. 8271â8285, May 2023.

[6] M. Dai, Z. Luo, Y. Wu, L. Qian, B. Lin, and Z. Su, âIncentive oriented two-tier task offloading scheme in marine edge computing networks: A hybrid Stackelberg-auction game approach,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8603â8619, Dec. 2023.

[7] C. Lin, G. Han, J. Du, Y. Bi, L. Shu, and K. Fan, âA path planning scheme for AUV flock-based internet-of-underwater-things systems to enable transparent and smart ocean,â IEEE Internet Things J., vol. 7, no. 10, pp. 9760â9772, Oct. 2020.

[8] Y. Wu, K. H. Low, and C. Lv, âCooperative path planning for heterogeneous unmanned vehicles in a search-and-track mission aiming at an underwater target,â IEEE Trans. Veh. Technol., vol. 69, no. 6, pp. 6782â6787, Jun. 2020.

[9] C. Ke and H. Chen, âCooperative path planning for airâsea heterogeneous unmanned vehicles using search-and-tracking mission,â Ocean Eng., vol. 262, 2022, Art. no. 112020.

[10] X. Cao, W. Liu, and L. Ren, âUnderwater target capture based on heterogeneous unmanned system collaboration,â in IEEE Trans. Intell. Veh., vol. 9, no. 10, pp. 6049â6062, Oct. 2024, doi: 10.1109/TIV.2024.3362358, 2024.

[11] W. Wei, J. Wang, Z. Fang, J. Chen, Y. Ren, and Y. Dong, âU: Joint design of UAV-USV-UUV networks for cooperative target hunting,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 4085â4090, Mar. 2023.

[12] S. Dong, M. Liu, S. Dong, R. Zheng, and P. Wei, âHierarchical heterogeneous multi-agent cross-domain search method based on deep reinforcement learning,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 11, pp. 18872â18883, Nov. 2024, doi: 10.1109/TITS.2024.3417698.

[13] C. Singhal and S. De, Resource Allocation in Next-Generation Broadband Wireless Access Networks. Hershey, PA, USA: IGI Global, 2017.

[14] B. Yu, X. Chen, and Y. Cai, âAge of information for the cellular Internet of Things: Challenges, key techniques, and future trends,â IEEE Commun. Mag., vol. 60, no. 12, pp. 20â26, Dec. 2022.

[15] A. Jeganathan, B. Dhayabaran, T. D. P. Perera, D. N. K. Jayakody, and P. Muthuchidambaranathan, âHarvest-on-sky: An AoI-driven UAV-assisted wireless communication system,â IEEE Internet Things Mag., vol. 5, no. 1, pp. 142â146, Mar. 2022.

[16] J. Cao et al., âToward industrial metaverse: Age of information, latency and reliability of short-packet transmission in 6G,â IEEE Wireless Commun., vol. 30, no. 2, pp. 40â47, Apr. 2023.

[17] J. Wang, L. Bai, Z. Fang, R. Han, J. Wang, and J. Choi, âAge of information based URLLC transmission for UAVs on pylon turn,â IEEE Trans. Veh. Technol., vol. 73, no. 6, pp. 8797â8809, Jun. 2024.

[18] Z. Fang, J. Wang, C. Jiang, Q. Zhang, and Y. Ren, âAoI-inspired collaborative information collection for AUV-assisted Internet of Underwater Things,â IEEE Internet Things J., vol. 8, no. 19, pp. 14559â14571, Oct. 2021.

[19] B. Jiang, J. Du, C. Jiang, Z. Han, and M. Debbah, âUnderwater searching and multiround data collection via AUV swarms: An energy-efficient AoI-aware MAPPO approach,â IEEE Internet Things J., vol. 11, no. 7, pp. 12768â12782, Apr. 2024.

[20] J. Chen, J. Wang, Z. Wei, Y. Ren, C. Masouros, and Z. Han, âJoint autonomous underwater vehicle trajectory and energy optimization for underwater covert communications,â IEEE Trans. Commun., vol. 72, no. 11, pp. 7327â7341, Nov. 2024, doi: 10.1109/TCOMM.2024.3412782.

[21] G. Han, Z. Feng, H. Wang, Y. Hou, and F. Zhang, âUnderwater multi-target node path planning in hybrid action space: A deep reinforcement learning approach,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 13033â13047, Dec. 2024.

[22] C. Lin, G. Han, T. Zhang, S. B. H. Shah, and Y. Peng, âSmart underwater pollution detection based on graph-based multi-agent reinforcement learning towards AUV-based network ITS,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 7, pp. 7494â7505, Jul. 2023.

[23] N. Shirakura, T. Kiyokawa, H. Kumamoto, J. Takamatsu, and T. Ogasawara, âCollection of marine debris by jointly using UAV-UUV with GUI for simple operation,â IEEE Access, vol. 9, pp. 67432â67443, 2021.

[24] Z. Wang, J. Du, C. Jiang, Y. Ren, and X. -P. Zhang, âUAV-assisted target tracking and computation offloading in USV-based MEC networks,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 11389â11405, Dec. 2024.

[25] Z. Yang, J. Du, Z. Xia, C. Jiang, A. Benslimane, and Y. Ren, âSecure and cooperative target tracking via AUV swarm: A reinforcement learning approach,â in Proc. 2021 IEEE Glob. Commun. Conf., Madrid, Spain, 2021, pp. 1â6.

[26] A. Yang et al., âFiltering of airborne LiDAR bathymetry based on bidirectional cloth simulation,â ISPRS J. Photogrammetry Remote Sens., vol. 163, pp. 49â61, 2020.

[27] H. Hu, K. Xiong, H. -C. Yang, P. Fan, and K. B. Letaief, âAge of information analysis of WPCN over Rician fading channel with nonlinear penalty,â IEEE Internet Things J., vol. 11, no. 4, pp. 5854â5866, Feb. 2024.

[28] R. Szczepanski, âSafe artificial potential field - novel local path planning algorithm maintaining safe distance from obstacles,â IEEE Robot. Automat. Lett., vol. 8, no. 8, pp. 4823â4830, Aug. 2023.

[29] X. Meng and X. Fang, âA UGV path planning algorithm based on improved A\* with improved artificial potential field,â Electronics, vol. 13, no. 5, 2024, Art. no. 972.

[30] Z. Zeng, K. Sammut, A. Lammas, F. He, and Y. Tang, âEfficient path replanning for AUVs operating in spatiotemporal currents,â J. Intell. Robotic Syst., vol. 79, pp. 135â153, 2015.

[31] X. Hou, J. Wang, T. Bai, Y. Deng, Y. Ren, and L. Hanzo, âEnvironmentaware AUV trajectory design and resource management for multi-tier underwater computing,â IEEE J. Sel. Areas Commun., vol. 41, no. 2, pp. 474â490, Feb. 2023.

[32] Z. Fang, J. Wang, J. Du, X. Hou, Y. Ren, and Z. Han, âStochastic optimization-aided energy-efficient information collection in Internet of Underwater Things networks,â IEEE Internet Things J., vol. 9, no. 3, pp. 1775â1789, Feb. 2022.

[33] M. M. Bhatti, M. Marin, A. Zeeshan, and S. I. Abdelsalam, âRecent trends in computational fluid dynamics,â Front. Phys., vol. 8, 2020, Art. no. 593111.

[34] Z. Xia et al., âMulti-agent reinforcement learning aided intelligent UAV swarm for target tracking,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 931â945, Jan. 2022.

[35] J. Li et al., âMulti-objective optimization approaches for physical layer secure communications based on collaborative beamforming in UAV networks,â IEEE/ACM Trans. Netw., vol. 31, no. 4, pp. 1902â1917, Apr. 2023.

[36] J. Li, M. Li, Y. Li, L. Dou, and Z. Wang, âCoordinated multi-robot target hunting based on extended cooperative game,â in Proc. 2015 IEEE Int. Conf. Inf. Automat., Lijiang, Chinaâ 2015, pp. 216â221.

[37] M. Chaudhary, N. Goyal, A. Benslimane, L. K. Awasthi, A. Alwadain, and A. Singh, âUnderwater wireless sensor networks: Enabling technologies for node deployment and data collection challenges,â IEEE Internet Things J., vol. 10, no. 4, pp. 3500â3524, Feb. 2023.

[38] Y. Yu, J. Tang, J. Huang, X. Zhang, D. K. C. So, and K. -K. Wong, âMultiobjective optimization for UAV-assisted wireless powered IoT networks based on extended DDPG algorithm,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6361â6374, Sep. 2021.

[39] Z. Shao, H. Yang, L. Xiao, W. Su, Y. Chen, and Z. Xiong, âDeep reinforcement learning-based resource management for UAV-assisted mobile edge computing against jamming,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 13358â13374, Dec. 2024, doi: 10.1109/TMC.2024.3432491.

<!-- image-->

Xiangwang Hou (Member, IEEE) received his BS degree from the Shandong University of Technology, in 2017, the MS degree from Xidian University, in 2020, and the PhD degree from Tsinghua University, Beijing, China, in 2025. From 2020 to 2021, he was an algorithm engineer with Huawei Technologies Company Ltd. and Tsinghua University. From 2023 to 2024, he was a joint PhD student with the School of Computer Science and Engineering, Nanyang Technological University, Singapore, under the supervision of Prof. Dusit Niyato. He is currently a post-

doctoral researcher with the Department of Electronic Engineering, Tsinghua University. His research interests include edge intelligence, federated learning, wireless AI, and UAV/AUV networks. He was the recipient of the Best Paper Award of IEEE ICC.

<!-- image-->

Tianyu Xing received the BS degree in mechanical engineering from Zhengzhou University, Zhengzhou, China, in 2019, and the MS degree in electronic information engineering from Tsinghua University, Beijing, China, in 2024. His research includes federated learning, wireless networks, and deep reinforcement learning for multi-agent systems.

<!-- image-->

Jingjing Wang (Senior Member, IEEE) received the BSc degree (with highest honors) in electronic information engineering from the Dalian University of Technology, Dalian, China, in 2014, and the PhD degree (with highest honors) in information and communication engineering from Tsinghua University, Beijing, China, in 2019. From 2017 to 2018, he was with the next generation wireless group chaired by Prof. Lajos Hanzo from the University of Southampton, U.K. He is currently a professor with the School of Cyber Science and Technology, Beihang Univer-

sity, Beijing, China, and also a researcher with Hangzhou Innovation Institute, Beihang University, Hangzhou, China. He has authored or coauthored more than 100 IEEE Journal/Conference papers. His research interests include AI enhanced next-generation wireless networks, UAV networking, and swarm intelligence. He is currentlythe editor of IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY, IEEE INTERNET OF THINGS JOURNAL, and IEEE WIRELESS COMMUNICATIONS LETTER. Dr. Wang was the recipient of the Best Journal Paper Award of IEEE ComSoc Technical Committee on Green Communications & Computing, Best

<!-- image-->

Jun Du (Senior Member, IEEE) received the BS degree in information and communication engineering from the Beijing Institute of Technology, in 2009, and the MS and PhD in information and communication engineering from Tsinghua University, Beijing, China, in 2014 and 2018, respectively. From 2016 to 2017, she was a sponsored researcher, and visited Imperial College London. She is currently an associate professor with the Department of Electrical Engineering, Tsinghua University. Her research interests include communications, networking, resource allo-

cation and system security problems of heterogeneous networks and space-based information networks. Dr. Du was the recipient of the Best Student Paper Award from IEEE GlobalSIP in 2015, Best Paper Award from IEEE ICC 2019 and 2025, and Best Paper Award from IWCMC in 2020.

<!-- image-->

Yong Ren (Senior Member, IEEE) received the BS, MS, and PhD degrees in electronic engineering from the Harbin Institute of Technology, Harbin, China, in 1984, 1987, and 1994, respectively. He was a postdoctoral fellow with the Department of Electronics Engineering, Tsinghua University, Beijing, China. He is currently a professor with the Department of Electronics Engineering and the Director of the Complexity Engineered Systems Lab. He holds 60 patents and has authored or coauthored more than 300 technical papers in communication and signal

processing. His research interests include maritime information networks and swarm intelligence.

<!-- image-->

Chunxiao Jiang (Fellow, IEEE) received the BS degree (with highest honors) in information engineering from Beihang University, Beijing, China, in 2008, and the PhD degree (with highest honors) in electronic engineering from Tsinghua University, Beijing, in 2013. From 2011 to 2012 (as a Joint PhD) and 2013 to 2016 (as a Postdoc), he was with the Department of Electrical and Computer Engineering, University of Maryland College Park under the supervision of Prof. K. J. Ray Liu. He is an associate professor with the School of Information Science and Technology, Tsinghua University. His research interests include application of game theory, optimization, and statistical theories to communication, networking, and resource allocation problems, in particular space networks and heterogeneous networks. Dr. Jiang was the editor of IEEE TRANSACTIONS ON COMMUNICATIONS, IEEE INTERNET OF THINGS JOURNAL, IEEE WIRELESS COMMUNICATIONS, IEEE TRANSACTIONS ON NETWORK SCIENCE AND ENGINEERING, IEEE NETWORK, IEEE COMMUNICATIONS LETTERS, and Guest Editor of IEEE COMMUNICATIONS MAGAZINE, IEEE TRANSACTIONS ON NETWORK SCIENCE AND ENGINEERING, and IEEE TRANSACTIONS ON COGNITIVE COMMUNICATIONS AND NETWORK-ING. He was also a member of the technical program committee as well as the Symposium Chair for a number of international conferences. Dr. Jiang was the recipient of the Best Paper Award from IEEE GLOBECOM in 2013, IEEE Communications Society Young Author Best Paper Award in 2017, Best Paper Award from ICC 2019, IEEE VTS Early Career Award 2020, IEEE ComSoc Asia-Pacific Best Young Researcher Award 2020, IEEE VTS Distinguished Lecturer 2021, and IEEE ComSoc Best Young Professional Award in Academia 2021. He received the Chinese National Second Prize in Technical Inventions Award in 2018. He is a fellow of IET.

<!-- image-->

Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkutâs Institute of Technology Ladkrabang (KMITL), Thailand, and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada. He is currently a professor with the College of Computing and Data Science, Nanyang Technological University, Singapore. His research interests include mobile generative AI, edge intelligence, quantum computing and networking, and incentive mechanism design.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_3_img_1.png|page_3_img_1]]
2. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_8_img_1.jpeg|page_8_img_1]]
3. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_10_img_1.png|page_10_img_1]]
4. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_10_img_2.png|page_10_img_2]]
5. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_10_img_3.jpeg|page_10_img_3]]
6. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_10_img_4.png|page_10_img_4]]
7. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_11_img_1.png|page_11_img_1]]
8. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_11_img_2.jpeg|page_11_img_2]]
9. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_11_img_3.png|page_11_img_3]]
10. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_12_img_1.jpeg|page_12_img_1]]
11. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_12_img_2.jpeg|page_12_img_2]]
12. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_12_img_3.jpeg|page_12_img_3]]
13. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_13_img_1.jpeg|page_13_img_1]]
14. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_13_img_2.jpeg|page_13_img_2]]
15. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_13_img_3.jpeg|page_13_img_3]]
16. [[../extracted_images/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting/page_13_img_4.jpeg|page_13_img_4]]

---

