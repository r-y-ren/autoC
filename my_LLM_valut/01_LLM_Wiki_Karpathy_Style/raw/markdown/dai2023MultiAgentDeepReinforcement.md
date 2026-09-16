# UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning

Saichao Liu, Geng Sun\*, Member, IEEE, Jiahui Li\*, Student Member, IEEE, Shuang Liang, Qingqing Wu, Senior Member, IEEE, Pengfei Wang, Member, IEEE, and Dusit Niyato, Fellow, IEEE

AbstractâIn this paper, we investigate an unmanned aerial vehicle (UAV)-assistant air-to-ground communication system, where multiple UAVs form a UAV-enabled virtual antenna array (UVAA) to communicate with remote base stations by utilizing collaborative beamforming. To improve the work efficiency of the UVAA, we formulate a UAV-enabled collaborative beamforming multi-objective optimization problem (UCBMOP) to simultaneously maximize the transmission rate of the UVAA and minimize the energy consumption of all UAVs by optimizing the positions and excitation current weights of all UAVs. This problem is challenging because these two optimization objectives conflict with each other, and they are non-concave to the optimization variables. Moreover, the system is dynamic, and the cooperation among UAVs is complex, making traditional methods take much time to compute the optimization solution for a single task. In addition, as the task changes, the previously obtained solution will become obsolete and invalid. To handle these issues, we leverage the multi-agent deep reinforcement learning (MADRL) to address the UCBMOP. Specifically, we use the heterogeneous-agent trust region policy optimization (HATRPO) as the basic framework, and then propose an improved HATRPO algorithm, namely HATRPO-UCB, where three techniques are introduced to enhance the performance. Simulation results demonstrate that the proposed algorithm can learn a better strategy compared with other methods. Moreover, extensive experiments also demonstrate the effectiveness of the proposed techniques.

Index TermsâUnmanned aerial vehicle, collaborative beamforming, energy efficiency, trust region learning, multi-agent deep reinforcement learning.

## 1 INTRODUCTION

U NMANNED aerial vehicles (UAVs) are aircraft withoutpilots, which are flying by remote or autonomous con- pilots, which are flying by remote or autonomous control [1]. With the advantages of high mobility, low cost and line-of-sight (LoS) communications, UAVs can be applied in many wireless communication scenarios. For instance, a UAV can act as an aerial base station (BS) to provide emergency communication service for ground users when the ground BSs are unavailable [2], [3]. Moreover, a UAV can serve as a relay to improve the coverage and connectivity of wireless networks [4]. In addition, the UAVs can be regarded as the new aerial users which is able to deliver packages [5].

Despite the application prospect of UAVs being promising, many challenges still exist. Specifically, the limited battery capacity will affect the work efficiency of a UAV [6] [7], thus some relevant optimizations (e.g., flight trajectory [8] and mission execution time [9]) are necessary to prolong the working time of UAVs. Besides, a UAV is difficult to communicate with remote BSs due to its limited transmission power [10], and it cannot fly close to the BSs because of the finite energy capacity. Therefore, it is significant to improve the transmission ability of a UAV.

Collaborative beamforming (CB) has been justified to efficiently improve the transmission performance of distributed systems with limited resources [11]. Specifically, the UAVs can form a virtual antenna array (VAA), where each UAV is regarded as a single antenna element, then the UAVassisted VAA (UVAA) can produce a high-gain mainlobe toward the remote BS by utilizing CB, such that achieving the long distance air-to-ground (A2G) communication between the UAVs and remote BS. To obtain an optimal beam pattern so that achieving a higher receiving rate of the BS, all UAVs need to fly to more appropriate positions and adjust their excitation current weights [12]. However, for communicating with different BSs, all UAVs need to adjust their positions constantly, which will consume extra energy. Hence, in addition to improving the transmission rate, the optimization to the motion energy consumption of UVAA is also required so as to prolong the lifespan of UVAA.

Previous studies usually optimize the communication performance or energy efficiency separately by using the traditional methods (e.g., convex optimization, or evolutionary computation). However, it is difficult to achieve optimal performance of these two optimization objectives simultaneously because they conflict with each other. Furthermore, since the cooperation among UAVs is very complex and the number of UAVs is usually large in the UVAA system, traditional methods will take much time to compute the optimization results. Besides, the system is dynamic, causing the currently obtained optimization results will become invalid when the system status changes. Therefore, it is inappropriate to apply traditional methods to simultaneously optimize the two objectives of the UVAA system.

Deep reinforcement learning (DRL) is an effective approach to solve complex and dynamic optimization problems without prior knowledge, and it has been proven to be an effective method to deal with complex optimization problems with high-dimensional continuous spaces [13]. Several studies have applied DRL to solve single-UAV communication optimization problems [14] [15]. However, DRL methods usually consider only single-agent learning frameworks, which are inappropriate for dealing with the UAV-enabled CB optimization problem. Thus, multi-agent deep reinforcement learning (MADRL) can be regarded as a potential approach to obtain the optimal policies since the learned policy of each agent involves the cooperation with other agents in MADRL. Specifically, all agents use the deep neural network (DNN) for policy learning. Benefiting from the powerful learning ability of DNN, all agents can learn excellent strategies. Meanwhile, compared with traditional methods, all agents can make corresponding decision directly without consuming much computing resource when the environment changes.

In this work, we utilize MADRL to deal with the UAV-enabled CB optimization problem. Consider that the cooperation is very complex among UAVs, we use the heterogeneous-agent trust region policy optimization (HA-TRPO) [16] as the main MADRL framework. Besides, the number of UAVs is usually large in the UVAA, which may cause the curse of dimensionality for MADRL algorithm. Furthermore, the policy gradient estimation problem may exists. Therefore, we propose an improved algorithm for solving our constructed problem well. The main contributions are summarized as follows:

UAV-enabled CB Multi-objective Optimization Formulation: We study a UAV-assistant A2G communication system, where a swarm of UAVs form a UVAA to perform CB for communicating with remote BSs. Then, we formulate a UAV-enabled CB multi-objective optimization problem (UCBMOP), aiming at simultaneously maximizing the transmission rate of UVAA and minimizing the energy consumption of the UAV elements by optimizing the positions and the excitation current weights of all UAVs. The problem is difficult to address because the two optimization objectives conflict with each other, and they are non-concave with respect to the optimization variables, such as the coordinates and the excitation current weights of UAVs.

New MADRL Approach: We model a multi-agent Markov decision process, called Markov game, for characterizing the formulated UCBMOP. Then, we propose an improved HATRPO algorithm, namely HATRPO-UCB, to solve the UCBMOP. Specifically, three techniques are proposed to enhance the performance of conventional HATRPO, which are observation enhancement, agent-specific global state and Beta distribution for policy, respectively. The first technique is to combine the algorithm with the problem well, so as to learn the better strategy for UCBMOP. The other two techniques are used to enhance the learning performance of critic and actor network, respectively.

Simulation and Performance Analysis: Simulation results show that the proposed HATRPO-UCB learns the best strategy compared with two classic antenna array solutions, three baseline MADRL algorithms and the conventional HATRPO. Besides, ablation experiments also demonstrate the effectiveness of our proposed techniques.

The rest of the paper is organized as follows. Section 2 discusses the related works. The system model and problem formulation are presented in Section 3. Section 4 proposes HATRPO-UCB. Simulation results and analysis are provided in Section 5. Finally, Section 7 concludes the paper.

## 2 RELATED WORK

Several previous works have studied the energy optimization in UAV-based communication scenarios. For example, Zeng et al. [8] considered a scenario where a UAV needs to communicate with multiple ground nodes, then proposed an efficient algorithm to achieve the energy minimization by jointly optimizing the hovering locations and durations, as well as the flying trajectory connecting these hovering locations. Cai et al. [17] studied the energy-efficient secure downlink UAV communication problem, with the purpose of maximizing the system energy efficiency. The authors divided the optimization problem into two subproblems, and proposed an alternating optimization-based algorithm to jointly optimize the resource allocation strategy, the trajectory of information UAV, and the jamming policy of jammer UAV. Wang et al. [18] investigated a multiple UAVsassisted mobile edge computing (MEC) system, where a natural disaster has damaged the edge server. The authors proposed two game theory-based algorithms, where the first algorithm is used to minimize the total energy consumption of multiple UAVs, and the second one is designed to achieve the utility trade-off between the UAV-MEC server and mobile users.

Except for adopting traditional methods, some works also use DRL to optimize the energy consumption of UAV. For optimizing the energy consumption of cellularconnected UAV, Zhan et al. [9] developed a DRL algorithm based on dueling deep Q network (DQN) with multi-step double Q-learning to jointly optimize the mission completion time, trajectory of UAV and associations to BSs. Abedin et al. [19] propose an agile deep reinforcement learning algorithm to achieve an energy-efficient trajectory optimization for multiple UAVs so as to improve the data freshness and connectivity to the Internet of Things (IoT) devices. Liu et al. [20] proposed a decentralized DRL-based framework to control multiple UAVs for achieving the long-term communication coverage in an area. The goal is to simultaneously maximize the temporal average coverage score achieved by all UAVs in a task, maximize the geographical fairness of all considered point-of-interests (PoIs), and minimize the total energy consumption.

UAV communications enabled by CB are also investigated in previous works. For example, Garza et al. [12] proposed the differential evolution method for a UAVbased 3D antenna array, aiming at achieving a maximum performance with respect to directivity and sidelobe level (SLL). Mozaffari et al. [21] considered a UAV-based linear antenna array (LAA) communication system and proposed two optimization algorithms, where the first algorithm is used to minimize the transmission time for ground users, and the second one is designed to optimize the control time of UAV-based LAA. Sun et al. [22] developed a multiobjective optimization algorithm to simultaneously minimize the total transmission time, total performing time of UVAA, and total motion and hovering energy consumption of UAVs. Moreover, the authors in [23] studied a secure and energy-efficient relay communication problem, where the UVAA serves as an aerial relay for providing communications to the blocked or low-quality terrestrial networks. The authors designed an improved evolutionary computation method to jointly circumvent the effects of the known and unknown eavesdroppers and minimize the propulsion energy consumption of UAVs.

Likewise, Sun et al. [24] considered a UAV-enabled secure communication scenario, where multiple UAVs form a UVAA to perform CB for communicating with the remote BSs, and multiple known and unknown eavesdroppers exist to wiretap the information. Li et al. [25] studied the UAV-assisted IoT and introduced CB into IoTs and UAVs simultaneously to achieve energy and time-efficient data harvesting and dissemination from multiple IoT clusters to remote BSs. Huang et al. [26] studied a dual-UAVs jammingaided system to implement physical layer encryption in maritime wireless communication. Li et al. [27] considered a UAV-enabled data collection scenario, where CB is adopted to mitigate the interference of the LoS channel of UAV to the terrestrial network devices. Moorthy et al. [28] aimed at achieving the high data rate of CB of UAV swarm, and then designed a distributed solution algorithm based on a combination of echo state network learning and online reinforcement learning to maximize the throughput of UAV swarm. However, all of these abovementioned methods will take much time to compute the solution for a task. More seriously, when the task changes, the previous optimization solution is invalid, causing a longer latency for recalculation.

DRL has been an effective way to solve the online computation problems about UAV communications. For example, Wang et al. [14] investigated a UAV-assisted IoT system, and they proposed a twin-delayed deep deterministic policy gradient (TD3)-based method that optimizes the trajectory of UAV to efficiently collect data from IoT ground nodes. Xie et al. [15] proposed a multi-step dueling double DQN (multistep D3QN)-based method to optimize the trajectory of cellular-connected UAV while guaranteeing the stable connectivity of UAV to the cellular network during its flight. Besides, MADRL can be also applied to solve the communication problems involving multiple UAVs. For instance, Zhang et al. [29] proposed a continuous action attention multiagent deep deterministic policy gradient (CAA-MADDPG) algorithm to operate a UAV transmitter to communicate with ground users and multiple UAV jammers. Dai et al. [30] studied the joint decoupled uplink-downlink association and trajectory design problem for full-duplex UAV network, with the purpose of maximizing the sum-rate of user equipments in both uplink and downlink. The authors proposed a MADRL-based approach and developed an improved clip and count-based proximal policy optimization (PPO) algorithm. However, in the above works, the cooperation pattern among UAVs is only the coordination, which is less complex than CB, and the completion of CB involves more UAVs. Hence, these abovementioned MADRL algorithms are not suitable for solving our formulated optimization problem.

<!-- image-->  
Fig. 1. Sketch map of the considered UVAA communication system.

In summary, different from the above works, we investigate a joint problem about communication performance and energy consumption under a scenario where multiple UAVs perform CB. Then, the MADRL is adopted to efficiently solve our formulated optimization problem.

## 3 SYSTEM MODEL AND PROBLEM FORMULATION

As shown in Fig. 1, a UAV-assisted A2G wireless communication system is considered. Specifically, there are N UAVs flying in a square area with length L, where the set of UAVs is denoted as $\mathcal { N } \triangleq \{ i = 1 , 2 , \dots , N \}$ . Some BSs are distributed in the far-field region, and their positions are assumed to be known by all UAVs. Each UAV is equipped with a single omni-directional antenna, and they will perform the communication tasks with these BSs. For example, their stored data or some generated emergency data needs to be uploaded to BSs. However, each UAV is not able to support such the long-distance communication due to the limited transmission ability, and they also can not fly to these BSs because of their own limited battery energy capacity. Note that for all UAVs, the distances among them are much shorter than those to BSs, which means that they are close to each other. Thus, all UAVs can fly closer to form an UVAA for performing CB to complete communication tasks. Moreover, the UVAA only communicates with one BS at each time as performing CB.

In the considered system, the 3D Cartesian coordinate system is utilized. Specifically, the positions of the i-th UAV and the target BS are denoted as $( x _ { i } , y _ { i } , z _ { i } )$ and (xBS, yBS, 0), respectively. Furthermore, the elevation and azimuth angles from each UAV to the target BS can be computed by $\begin{array} { r } { \tilde { \theta _ { i } } \ = \ \cos ^ { - 1 } ( \frac { 0 - z _ { i } ^ { \cup } } { \sqrt { ( x _ { \mathrm { B S } } - x _ { i } ) ^ { 2 } + ( y _ { \mathrm { B S } } - y _ { i } ) ^ { 2 } + ( 0 - z _ { i } ) ^ { 2 } } } ) } \end{array}$ and $\begin{array} { r } { \phi _ { i } = \sin ^ { - 1 } ( \frac { y _ { \mathrm { B S } } - y _ { i } ^ { \star } } { \sqrt { ( x _ { \mathrm { B S } } - x _ { i } ) ^ { 2 } + ( y _ { \mathrm { B S } } - y _ { i } ) ^ { 2 } } } ) } \end{array}$ , respectively.

TABLE 1 Summary of main notations
<table><tr><td>Notation</td><td>Definition</td></tr><tr><td colspan="2">Notationused in systemmodel</td></tr><tr><td> ${ \overline { { A F ( \theta , \phi ) } } }$ </td><td>Arrayfactor</td></tr><tr><td> $B$ </td><td>Transmission bandwidth</td></tr><tr><td> $d _ { \mathrm { B S } }$ </td><td>Distance from origin ofUVAA to target BS</td></tr><tr><td> $d _ { m i n }$ </td><td>Minimal distance between two UAVs</td></tr><tr><td> $E$ </td><td>Total energy consumption of UAV</td></tr><tr><td> $E _ { G }$ </td><td>Energy consumed by gravity during UAV flight</td></tr><tr><td> $E _ { K }$ </td><td>Energy consumption from kinetic energy during</td></tr><tr><td></td><td>UAV flight</td></tr><tr><td> $f _ { c }$ </td><td>Carrier frequency</td></tr><tr><td> $G ( \cdot )$ </td><td>Array gain ofUVAA</td></tr><tr><td> $g _ { c }$ </td><td>Channel power gain</td></tr><tr><td> $H _ { m i n }$ </td><td>Minimum flight altitude of UAV</td></tr><tr><td> $H _ { m a x }$ </td><td>Maximum flightaltitude ofUAV</td></tr><tr><td> $I _ { i }$   $L$ </td><td>Excitation currentweightof thei-thUAV</td></tr><tr><td></td><td>Length of monitor area</td></tr><tr><td> $m _ { \mathrm { U A V } }$   $N$ </td><td>Mass of UAV</td></tr><tr><td> $P _ { \mathrm { L o S } }$ </td><td>Number of UAVs</td></tr><tr><td> $P _ { \mathrm { N L o S } }$ </td><td>LoS probability</td></tr><tr><td> $P _ { t }$ </td><td>NLoS probability</td></tr><tr><td> $R ( \cdot )$ </td><td>Total transmit power of UVAA</td></tr><tr><td> $w ( \theta , \phi )$ </td><td>Transmission rate</td></tr><tr><td> $_ \alpha$ </td><td>Magnitudeof far-fieldbeampatternofUVAelement</td></tr><tr><td> $\eta$ </td><td>Pathloss exponent</td></tr><tr><td> $\theta _ { \mathrm { B S } }$ </td><td>Antenna array efficiency</td></tr><tr><td> $\lambda$ </td><td>Elevationangle between UVAA and target BS</td></tr><tr><td> $\mu _ { \mathrm { L o S } }$ </td><td>Wavelength</td></tr><tr><td></td><td>Attenuation factor for LoS link</td></tr><tr><td> $\mu _ { \mathrm { N L o S } }$   $\sigma ^ { 2 }$ </td><td>Attenuation factor forNLoS link</td></tr><tr><td></td><td>Noise power</td></tr><tr><td> $\phi _ { \mathrm { B S } }$ </td><td>Azimuth angle between UVAA and target BS</td></tr><tr><td> $\Psi _ { i }$ </td><td>Initial phase of thei-th UAV</td></tr><tr><td></td><td>Notation used in reinforcement learning</td></tr><tr><td> $a _ { i }$ </td><td>Action of thei-thagent</td></tr><tr><td> $\textbf { \em a }$ </td><td>Joint action of all agents</td></tr><tr><td> $\mathbf { \mathcal { A } } _ { i }$ </td><td>actionspace of the i-th agent</td></tr><tr><td> $A ^ { \pi } ( s ^ { t } , a ^ { t } )$ </td><td>Advantage function for joint policyÏ</td></tr><tr><td> $\mathrm { D } _ { \mathrm { K L } } ^ { \mathrm { m a x } } ( \cdot , \cdot )$ </td><td>Maximal KL-divergence between two policies</td></tr><tr><td> $\mathbf { \pmb { g } } _ { i } ^ { k }$ </td><td>Gradient of maximization objective of the i-th agent</td></tr><tr><td> $\pmb { H } _ { i } ^ { k }$ </td><td>Hessian of expected KL-divergence of the i-th agent</td></tr><tr><td> $J ( \bar { \pi } )$ </td><td>Expected total reward for all agents</td></tr><tr><td> $L _ { 1 : i } ^ { \pi } ( \cdot , \cdot )$ </td><td>Surrogate equationof thei-thagent</td></tr><tr><td> $o _ { i }$ </td><td>Local observation of the i-th agent</td></tr><tr><td> $\mathcal { O } _ { i }$ </td><td>Observation space of the i-th agent</td></tr><tr><td> $Q ^ { \pi } ( s ^ { t } , \pmb { a } ^ { t } )$ </td><td>State-action value function for joint policy</td></tr><tr><td> $r _ { i }$ </td><td>Reward of thei-th agent</td></tr><tr><td> $s$ </td><td>Global state</td></tr><tr><td> $s$ </td><td>Global state space</td></tr><tr><td> $V ^ { \pi } ( s ^ { t } )$ </td><td>State value function for joint policyÏ</td></tr><tr><td> $\alpha ^ { j }$ </td><td>A coefficient is found by backtracking line search</td></tr><tr><td>Y</td><td>Discount factor</td></tr><tr><td> $\delta$ </td><td>KL constraint threshold</td></tr><tr><td> $\rho _ { \pi }$ </td><td>Marginal state distribution for joint policy Ï</td></tr></table>

## 3.1 UVAA Communication Model

The goal of UVAA is to enable multiple UAVs to simulate the classical beamforming for achieving the far-field communication with remote BSs. The gain towards the target BS will be enhanced by the superposition of electromagnetic waves emitted from all UAVs through CB. Before the CBenabled communication, all UAVs can be synchronized in terms of the carrier frequency, time and initial phase [31], and then send the same data to the target BS.

Benefiting from the high altitude of UAV, a higher LoS probability between the UVAA and BS can be achieved. Additionally, the LoS probability depends also on the propagation environment and the statistic modeling of the building density. Hence, the LoS probability can be modeled as [32]

$$
P _ { \mathrm { L o S } } = \frac { 1 } { 1 + C \exp ( - D [ \theta _ { \mathrm { r e c } } - C ] ) } ,\tag{1}
$$

where C and D are the parameters that depend on the propagation environment. $\theta _ { \mathrm { r e c } }$ is the elevation angle from the UVAA to the target BS. Then, the non-LoS (NLoS) probability is given by $\dot { P } _ { \mathrm { N L o S } } = 1 - P _ { \mathrm { L o S } }$

According to the probability of LoS and NLoS, the channel power gain can be expressed as

$$
g _ { c } = K _ { o } ^ { - 1 } d _ { \mathrm { B S } } ^ { - \alpha } [ P _ { \mathrm { L o S } } \mu _ { \mathrm { L o S } } + P _ { \mathrm { N L o S } } \mu _ { \mathrm { N L o S } } ] ^ { - 1 } ,\tag{2}
$$

where $\begin{array} { r } { K _ { o } = ( \frac { 4 \pi f _ { c } } { c } ) ^ { 2 } , d _ { \mathrm { B S } } } \end{array}$ is the distance from the origin of UVAA to the target BS, $\mu _ { \mathrm { L o S } }$ and $\mu _ { \mathrm { N L o S } }$ are different attenuation factors for the LoS and NLoS links, respectively, Î± is a constant representing the path loss exponent, $f _ { c }$ is the carrier frequency, and c is the speed of light.

Combining the above channel model, the UVAA will perform CB to generate a beam pattern with a sharp mainlobe for the target BS. Then, the transmission rate can be expressed as [21]

$$
R ( \mathbf { X } , \mathbf { Y } , \mathbf { Z } , \mathbf { I } ) = B \log _ { 2 } \left( 1 + \frac { g _ { c } P _ { t } G ( \mathbf { X } , \mathbf { Y } , \mathbf { Z } , \mathbf { I } ) } { \sigma ^ { 2 } } \right) ,\tag{3}
$$

where $\mathbf { X } = \{ x _ { i } \} _ { i = 1 } ^ { N } , \mathbf { Y } = \{ y _ { i } \} _ { i = 1 } ^ { N } , \mathbf { Z } = \{ z _ { i } \} _ { i = 1 } ^ { N } , \mathbf { I } = \{ I _ { i } \} _ { i = 1 } ^ { N }$ represent the 3D coordinates and excitation current weights of all UAVs while communicating with the BS, B is the transmission bandwidth, $P _ { t }$ is the total transmit power of UVAA, and $\sigma ^ { 2 }$ is the noise power. In addition, G(X, Y, Z, I) is the array gain of UVAA toward the location of BS, which is given by [21]

$$
G ( \mathbf { X } , \mathbf { Y } , \mathbf { Z } , \mathbf { I } ) = \frac { 4 \pi \vert A F ( \theta _ { \mathrm { B S } } , \phi _ { \mathrm { B S } } ) \vert ^ { 2 } w ( \theta _ { \mathrm { B S } } , \phi _ { \mathrm { B S } } ) ^ { 2 } } { \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \pi } \vert A F ( \theta , \phi ) \vert ^ { 2 } w ( \theta , \phi ) ^ { 2 } \sin \theta d \theta d \phi } \eta ,\tag{4}
$$

where $\eta \in [ 0 , 1 ]$ is the antenna array efficiency, $( \theta _ { \mathrm { B S } } , \phi _ { \mathrm { B S } } )$ represents the direction toward the target BS, and $w ( \theta , \phi )$ is the magnitude of the far-field beam pattern of each UAV element. Note that the array gain is equal to the array directivity multiplied by Î·. The array directivity $\begin{array} { r c l } { \overline { { \cal D } } } & { = } & { U ( \bar { \theta } _ { \mathrm { B S } } , \phi _ { \mathrm { B S } } ) \big / U _ { 0 . } } \end{array}$ , where $\begin{array} { r l } { U ( \theta _ { \mathrm { B S } } , \phi _ { \mathrm { B S } } ) } & { = } \end{array}$ $| A F ( \dot { \theta _ { \mathrm { B S } } } , \dot { \phi _ { \mathrm { B S } } } ) | ^ { 2 } w ( \dot { \theta _ { \mathrm { B S } } } , \dot { \phi _ { \mathrm { B S } } } ) ^ { 2 }$ is the maximum radiation intensity produced by the array factor (AF) to the BS, and $\begin{array} { r } { U _ { 0 } = \dot { 1 } / 4 \pi \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \pi } \ d \lvert A F ( \theta , \phi ) \rvert ^ { 2 } w ( \theta , \phi ) ^ { 2 } } \end{array}$ sin Î¸dÎ¸dÏ is the average radiation intensity. Besides, $w ( \theta , \phi )$ is always equal to 0 dB in this work because the omni-directional antenna equipped on the UAV has the identical power constraints.

As for the AF, it is an important index to describe the status of beam pattern, which is written as [12] [33]

$$
A F ( \theta , \phi ) = \sum _ { i = 1 } ^ { N } { I _ { i } e ^ { j \Psi _ { i } } e ^ { j [ \frac { 2 \pi } { \lambda } ( x _ { i } \sin { \theta } \cos { \phi } + y _ { i } \sin { \theta } \sin { \phi } + z _ { i } \cos { \theta } ) ] } } ,\tag{5}
$$

where $\theta \in [ 0 , \pi ]$ and $\phi ~ \in ~ [ - \pi , \pi ]$ are the elevation and azimuth angles, respectively. Î» is the wavelength and $\frac { 2 \pi } { \lambda }$ denotes the wave number. Additionally, $I _ { i }$ and $\Psi _ { i }$ are the excitation current weight and initial phase of the i-th UAV, where the phase synchronization is completed by compensating the distance between an UAV and the origin of UVAA [34]. Hence, $\Psi _ { i }$ is expressed as

$$
\begin{array} { l } { { \displaystyle \Psi _ { i } = } } \\ { { \displaystyle - \frac { 2 \pi } { \lambda } \big ( x _ { i } \sin \theta _ { \mathrm { B S } } \cos \phi _ { \mathrm { B S } } + y _ { i } \sin \theta _ { \mathrm { B S } } \sin \phi _ { \mathrm { B S } } + z _ { i } \cos \theta _ { \mathrm { B S } } \big ) . } } \end{array}\tag{6}
$$

As can be seen, the locations and excitation current weights of UAVs are directly related to the AF.

## 3.2 UAV Energy Consumption Model

In this work, we adopt a typical rotary-wing UAV. This is due to the fact that rotary-wing UAVs have the inherent benefit of hovering capabilities, which simplifies the difficulty of beam alignment and handling Doppler effects during transmission. In this work, the considered communication system is required to provide a stable and highrate communication service for the far-field BSs. In this case, rotary-wing UAVs are more suitable for the considered scenario since they can hover for collecting and forwarding data. In general, the total energy consumption of a UAV includes two main components that are the propulsion and communication [8]. Specifically, the propulsion energy consumption is related to the hovering and movement of the UAVs, and communication-related energy consumption is used for signal processing, circuits, transmitting and receiving, respectively. Typically, the propulsion energy consumption is much more than communication-related energy consumption (e.g., hundreds of watts (w) versus a few w) [8] [35]. Thus, the communication-related energy consumption is neglected in this work. Then, the propulsion power consumption of UAV with speed v during the straight and horizontal flight is calculated as [8]

$$
\begin{array} { l } { { \displaystyle { P ( v ) = P _ { B } \left( 1 + \frac { 3 v ^ { 2 } } { v _ { t i p } ^ { 2 } } \right) + P _ { I } \left( \sqrt { 1 + \frac { v ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { v ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } } } } \\ { { \displaystyle { \phantom { \frac { 1 } { 1 } } } + \frac { 1 } { 2 } d _ { 0 } \rho s A v ^ { 3 } , } } \end{array}\tag{7}
$$

where $P _ { B }$ and $P _ { I }$ are blade profile power and induced power under the hovering condition, respectively. $v _ { t i p }$ is the tip speed of rotor blade, and $v _ { 0 }$ is mean rotor induced velocity in hovering. $d _ { 0 } , \rho , s ,$ and A denote the fuselage drag ratio, air density, rotor solidity and rotor disc area, respectively. Besides, the additional/less energy consumption caused by the acceleration/deceleration of horizontal flight is ignored because it only takes a small proportion of the total operation time of UAV manoeuvring duration [8].

For arbitrary 3D UAV trajectory with UAV climbing and descending over time, the heuristic closed-form approximation of energy consumption is derived as [1]

$$
\begin{array} { c } { \displaystyle { E ( T ) \approx \int _ { 0 } ^ { T } P ( v ( t ) ) d t + \frac { 1 } { 2 } m _ { \mathrm { U A V } } ( v ( T ) ^ { 2 } - v ( 0 ) ^ { 2 } ) } } \\ { \displaystyle { + m _ { \mathrm { U A V } } g ( h ( T ) - h ( 0 ) ) , } } \end{array}\tag{8}
$$

<!-- image-->  
Fig. 2. Energy consumption of UAV in the horizontal and vertical flights under different speeds.

where T is the total flight time. v(t) is the instantaneous UAV speed at time t. The second and third parts represent the kinetic energy consumption and potential energy consumption, respectively. mUAV is the mass of UAV, and $g$ is the gravitational acceleration. As can be seen, Eq. (8) has more terms than Eq. (7), meaning that more energy will be consumed in the vertical direction. Moreover, Fig. 2 shows that the motion energy consumption of UAV per second in the vertical directioon is more than that in the horizontal direction under different speeds.

In this work, the UAV follows the flight rule that it first flies along the horizontal direction, then in the vertical direction, which is a common adopted flight strategy [36] [37] [38]. Therefore, when a UAV reaches the target position, the corresponding energy consumption can be expressed as

$$
E = P _ { H } ( v _ { H } ) t _ { H } + P _ { C } ( v _ { C } ) t _ { C } + P _ { D } ( v _ { D } ) t _ { D } ,\tag{9}
$$

where $t _ { H } = \Delta d / v _ { H } , t _ { C } = | \Delta h _ { C } | / v _ { C }$ and $t _ { D } = | \Delta h _ { D } | / v _ { D }$ $\{ P _ { H } , P _ { C } , P _ { D } \}$ are the horizontal, climbing and descending flight powers, respectively, and $\{ \Delta d , \Delta \bar { h _ { C } } , \Delta h _ { D } \}$ are the corresponding flying distance during the horizontal, climbing and descending flights. Furthermore, $\{ v _ { H } , v _ { C } , v _ { D } \}$ represent the maximum-endurance (ME) speed of the horizontal, climbing and descending flights, respectively, which are the optimal UAV speed that maximizes the UAV endurance with any given onboard energy [1].

Remark 1. The challenge of adopting this type of rotarywing UAVs lies in their weak transmission abilities and limited service time. To solve this issue, we correspondingly introduce the CB and give the problem formulation as follows.

## 3.3 Problem Formulation

In the system, the UVAA is required to communicate with more than one BS before the battery runs out. To achieve the maximum transmission performance, all UAVs need to fly to better locations and adjust their excitation current weights. However, the motion energy consumption of UAVs will be increased during their movements, which will reduce the lifespan of UVAA. Therefore, the optimization problems about transmission rate and energy consumption should be considered simultaneously.

In this work, we aim to maximize the transmission rate of UVAA for communicating with the BS and minimize the motion energy consumption of all UAVs simultaneously, through optimizing the hovering positions and excitation current weights of all UAVs. Then, the UCBMOP can be formulated as

$$
\operatorname* { m a x } _ { { \bf X } , { \bf Y } , { \bf Z } , { \bf I } } \qquad f = \{ R _ { T } , - E _ { t o t a l } \}\tag{10a}
$$

$$
\begin{array} { r } { \mathrm { s . t . } \qquad C 1 : - L / 2 \leq x _ { i } \leq L / 2 , \forall i \in \mathcal { N } , } \end{array}\tag{10b}
$$

$$
C 2 : - L / 2 \leq y _ { i } \leq L / 2 , \forall i \in \mathcal { N } ,\tag{10c}
$$

$$
C 3 : H _ { m i n } \leq z _ { i } \leq H _ { m a x } , \forall i \in \mathcal { N } ,\tag{10d}
$$

$$
C 4 : 0 \leq I _ { i } \leq 1 , \forall i \in \mathcal { N } ,\tag{10e}
$$

$$
C 5 : d _ { i , j } \geq d _ { m i n } , \forall i , j \in N ,\tag{10f}
$$

where $R _ { T }$ is the transmission rate of UVAA to a specific BS defined by Eq. (3). The motion energy consumption of all UAVs is $\begin{array} { r } { E _ { t o t a l } = \sum _ { i = 1 } ^ { N } E _ { i } } \end{array}$ , where $E _ { i }$ is the motion energy consumption of UAV i that can be obtained according to the Eq. (9). Constraints C1, C2 and C3 together specify the flight area of UAV, where L is the length of monitor area, and $H _ { m i n }$ and $H _ { m a x }$ are altitude constraints of the UAVs. Constraint C4 specifies the adjustment range of excitation current weight. Moreover, Constraint C5 requires any two adjacent UAVs to keep a certain distance to avoid the collision, where $d _ { m i n }$ is set as the minimum distance.

## 4 MADRL-BASED UAV-ENABLED COLLABORA-TIVE BEAMFORMING

The formulated UCBMOP is challenging and cannot be solved by traditional optimization methods, and the reasons are as follows:

UCBMOP is a non-convex and long-term optimization problem. Specifically, due to the complex non-linear relationship between UAV coordinates and excitation current weights with antenna gain, the optimization of the virtual antenna array transmission performance is a non-convex optimization problem. Meanwhile, UCBMOP involves long-term optimization objectives and needs an effective algorithm that can achieve long-term optimal solutions. As such, UCBMOP is challenging and cannot be solved by traditional convex optimization.

UCBMOP is an NP-hard problem. Specifically, UCB-MOP can be simplified as a typical nonlinear multidimensional 0-1 knapsack problem that has been demonstrated to be NP-hard [39]. Therefore, the proposed UCBMOP is also NP-hard. Such NP-hard problems are challenging for traditional optimization methods to solve in polynomial time.

UCBMOP is a complex large-scale optimization problem. Specifically, the considered scenarios often involve a large number of UAVs, while each UAV also has multiple variables to be optimized (i.e., 3D coordinates and excitation current weights). In addition, the completion of CB also needs the complex cooperation of all UAVs. Hence, the complexity and massive dimension of decision variables make the traditional optimization method unable to solve it efficiently.

UCBMOP operates within a dynamic environment. In particular, UAVs in these scenarios must make decisions to adapt to highly dynamic channel conditions and the unpredictability of natural surroundings.

Additionally, real-time response is crucial for UAVs, as prolonged hovering in the air results in significant energy consumption. Consequently, conventional offline algorithms or approaches reliant on temporary calculations cannot solve this problem.

Different from the traditional optimization methods, deep reinforcement learning can have real-time responses and handle the complexity and large-scale decision variables of UCBMOP. However, in the considered system, UAVs need to collaborate to achieve transmission gain while simultaneously competing to minimize their individual energy consumption. Such tasks are distributed and require multiple UAVs to work together to achieve common objectives. Standard reinforcement learning assumes individual agents to be isolated, making it less suitable for the scenario involving multiple decision-makers.

Remark 2. In this case, MADRL has the capability to decentralize decision-making and adaptability for the changing environments, and enabling effective responses to complex interactions among multiple agents [40]. Moreover, MADRL allows agents to access the global state of the UAV collaborative beamforming system, providing them with information about the entire system and reducing non-stationarity. In addition, the scalability and robustness of MADRL to partial observability also enhance its applicability in the considered dynamic and distributed scenarios. Thus, we propose an MADRL-based method that is able to solve the formulated UCBMOP by learning the strategy in the considered dynamic scenario.

## 4.1 Markov Game for UCBMOP

In this section, the formulated UCBMOP is transformed into a Markov game [41] that is defined as $\langle \mathcal { N } , \mathcal { S } , \{ \mathcal { O } _ { i } \} _ { i \in \mathcal { N } } , \{ \mathcal { A } _ { i } \} _ { i \in \mathcal { N } } , \bar { P } , \{ R _ { i } \} _ { i \in \mathcal { N } } , \gamma \rangle$ . At time slot $t ,$ all agents are with state $s ^ { t } \in S ,$ each agent uses its policy $\pi _ { \boldsymbol { \theta } _ { i } }$ to take an action $a _ { i } ^ { t } \in \mathcal A _ { i }$ according to its local observation $o _ { i } ^ { t } \in \mathcal { O } _ { i } ,$ and it will receive a reward $r _ { i } ^ { t } = R _ { i } ( s ^ { t } , { \pmb a } ^ { t } )$ from the environment, where $\textbf { \em a } ^ { t } ~ = ~ \{ a _ { 1 } ^ { t } , \ldots , \hat { a } _ { N } ^ { t } \}$ denotes the joint action. Then, all agents move to the next state $s ^ { t + 1 }$ with probability $\left. P ( s ^ { t + 1 } \vert s ^ { t } , \pmb { a } ^ { t } ) \right.$ and each of them receives its local observation $o _ { i } ^ { t + 1 }$ correlated with the state. All agents aim to maximize their own expected total reward $\breve { J ( } \pi _ { \theta _ { i } } ) = \mathbb { E } _ { s ^ { 0 } , a ^ { 0 } , \ldots } [ \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } r _ { i } ^ { t } ]$ . The details about the state and observation space, the action space and the reward function are introduced as follows.

## 4.1.1 State and Observation Space

At each time slot, every agent observes its own local state information to make the decision. In the system, the local observation of any agents (i.e., UAVs) includes three parts that are its own related information, the relevant information of other UAVs and the related information of BS. Specifically, the local observation of the i-th agent can be expressed as

$$
o _ { i } = \{ \theta _ { i } , \phi _ { i } , d _ { i } , d _ { i , o } , I _ { i } , \{ d _ { j , i } , I _ { j } \} _ { j \in { \cal N } , j \neq i } , x ^ { \prime } , y ^ { \prime } , z ^ { \prime } \} ,\tag{11}
$$

where $( \theta _ { i } , \phi _ { i } , d _ { i } )$ is the spherical coordinate of the target BS relative to the i-th UAV. However, when the UVAA will communicate with more than one BS, then the gap among different BSs regarding $d _ { i }$ is very large. Furthermore, all

<!-- image-->  
Fig. 3. The transmission rate of UVAA to BSs at different distances when performing CB communication. The parameters about LoS probability C and D are set as 10 and 0.6, respectively.

UAVs only fly in the fixed area. To eliminate the gap and let the UAV make decisions more efficiently, we compute a reference point in the monitor area that is closest to the target BS, where the coordinate of reference point is denoted as $( x ^ { \prime } , y ^ { \prime } , z ^ { \prime } )$ . Then, the distance between the i-th UAV and the reference point is regarded as $d _ { i }$ . Moreover, $d _ { i , o }$ is the distance between the i-th UAV and the origin of UVAA, and $I _ { i }$ is the excitation current weight of the i-th UAV. The information of other UAVs contains their own excitation current weights and the distances to the i-th UAV. As for the information about the target BS, its coordinate is replaced by the reference point, which will be beneficial for the agent to learn the better strategy.

As for the global state of the i-th agent $s _ { i } ,$ instead of using the concatenation of local observations or the environment-provided global state, we propose an agentspecific global state that combines some agent-related features $( \mathrm { e . g . , ~ } ( \theta _ { i } , \phi _ { i } , d _ { i } ) , d _ { i , o } , d _ { j , i } )$ and the global information provided from the environment which includes the coordinates and excitation current weights of all UAVs, as well as the coordinate of reference point, which is inspired from [42].

## 4.1.2 Action Space

According to the local observation of UAVs, each UAV will take an action to fly to a certain location with the optimized excitation current weight for performing CB. Then, the action of each agent can be defined by

$$
a _ { i } = \{ x _ { i } , y _ { i } , z _ { i } , I _ { i } \} ,\tag{12}
$$

where $( x _ { i } , y _ { i } , z _ { i } )$ is the location to which the i-th UAV is going to fly, and $I _ { i }$ is the excitation current weight of the i-th UAV in the next time slot.

## 4.1.3 Reward Function

The reward function is used to evaluate how well an agent executes the actions. Specifically, a suitable reward function can make the agent learn the best strategy. UCBMOP involves two optimization objectives, which are maximizing the transmission rate of UVAA for communicating with the $\mathrm { B S } , \mathrm { i } . \mathrm { e } . , R _ { T } ,$ and minimizing the motion energy consumption of all $\mathrm { U A V s , i . e . , } E _ { t o t a l }$ . To this end, we design a reward function by considering the following aspects:

1) Reward Function for Optimizing $R _ { T }$ . We find that there are three key components that affect the transmission rate $R _ { T }$ , which are the transmit power and gain of

UVAA, transmission distance, and A2G communication angle. Specifically, the transmit power and gain of UVAA determine the transmission performance of UVAA, the transmission distance indicates the signal fading degree, and the air-to-ground communication angle affects the A2G channel condition. Note that we do not directly set the transmission rate as a reward since it changes significantly with the transmission distance, making the DRL method unstable and decreasing the applicability of the model.

According to the analysis above, first, we regard the multiplication of the array gain and the total transmit powers as a reward, i.e., $r ^ { \mathrm { \large { T R } } } = G P _ { t }$ . Note that this reward is shared by all agents. Then, we set the distance between the UAV and BS as a penalty for each agent. However, the UAV only flies within a fixed area, and then the aforementioned distance is replaced by the one between the UAV and the reference point of target ${ \mathrm { B S } } ,$ which is denoted as $r _ { i } ^ { \mathrm { U 2 B } } ~ = ~ - d _ { i , r } ^ { \bullet }$ . Finally, as shown in Eq. (1), the LoS probability is determined mainly by the height of the UAVs. Therefore, we set a reward to optimize the flight altitude of each UAV, denoted as $r _ { i } ^ { \dot { \mathrm { H } } } ~ = ~ z _ { i }$ . As such, the designed reward function considers all controllable components of the transmission rate, thereby achieving the optimization of the first objective.

2) Reward Function for Optimizing $E _ { t o t a l }$ . To achieve this goal, we regard the energy consumption of each UAV as a penalty, which is denoted as $r _ { i } ^ { \mathrm { E C } ^ { \bullet } } = - E _ { i }$ . As such, the optimization of the second objective can be achieved by the reward function.

3) Reward Function for Coordinating $R _ { T }$ and $E _ { t o t a l }$ . To this end, we aim to enhance the connectivity among UAVs. Compared with $R _ { T }$ , the optimization of $E _ { t o t a l }$ is more directly tied to the action space (i.e., reducing the movement of the UAVs), which may lead the algorithm to prioritize the optimization of $E _ { t o t a l }$ and under-optimize $R _ { T }$ . To overcome this issue, we try to concentrate the array elements $( \mathrm { i . e . , }$ the UAVs in UVAA) on an applicable distance to achieve a higher CB performance [43] [23], thereby facilitating the optimization of $R _ { T }$ . Specifically, we design a reward to coordinate the UAVs by minimizing the cumulative distances between the current UAV and other UAVs, as well as between the current UAV and the origin of the UVAA, i.e.,

$$
r _ { i } ^ { \mathrm { U 2 U } } = - \frac { 1 } { \kappa } \big ( \sum _ { j \in \mathcal { N } , j \ne i } d _ { j , i } + d _ { i , o } \big ) ,\tag{13}
$$

where Îº is a large constant for scaling. Since this reward decreases the difficulty of optimizing $R _ { T }$ , the designed reward function can well coordinate the optimization processes of the two optimization objectives.

In summary, the whole reward function of each agent is

$$
r _ { i } = \omega _ { 1 } r ^ { \mathrm { T R } } + \omega _ { 2 } r _ { i } ^ { \mathrm { H } } + \omega _ { 3 } r _ { i } ^ { \mathrm { E C } } + \omega _ { 4 } r _ { i } ^ { \mathrm { U 2 B } } + \omega _ { 5 } r _ { i } ^ { \mathrm { U 2 U } } ,\tag{14}
$$

where $\omega _ { 1 } , \omega _ { 2 } , \omega _ { 3 } , \omega _ { 4 } ,$ , and Ï5 represent weight coefficients of different parts. Moreover, it is also worth noting that when any two UAVs violate the minimum separation constraint, they will receive a negative reward. These weighting coefficient values can be determined by considering their value ranges, importance, and characteristics. Specifically, larger weights are assigned to rewards with wider ranges to appropriately reflect their significance in optimization. Moreover, higher weights are allocated to rewards that play a more critical role in achieving the optimization objectives. In addition, the weights can also be adjusted based on the unique characteristics of each reward, ensuring that the optimization process addresses their specific complexities.

## 4.2 HATRPO-UCB Algorithm

In this section, we propose a HATRPO-UCB, which extends from conventional HATRPO to find the solution strategy for UCBMOP. Specifically, each UAV acts as an agent that has an actor network and a critic network consisting of DNNs. The algorithm uses the sequential policy update scheme to train all agents. The scheme can make the update of the current agent includes the updates of previous agents, and thus our algorithm can make the actor networks of all agents learn the joint policy. Moreover, each agent has not only the individual rewards $( \mathrm { i . e . , } r _ { i } ^ { \mathrm { H } } , r _ { i } ^ { \mathrm { E C } } .$ , etc.) but also the shared rewards $( \mathrm { i } . \mathrm { e } . , \ r ^ { \mathrm { T R } } )$ . Meanwhile, we design an agent-specific global state that contains global information provided by the environment and some features from the local observation. As such, each UAV is guided by the shared rewards, and considers the global information and local observation, thereby obtaining a policy associated to the global state. We begin with introducing the conventional HATRPO.

## 4.2.1 Conventional HATRPO

HATRPO was proposed by Kuba et al. [16], which has the better performance than other baseline MADRL algorithms in many multi-agent tasks (e.g., Multi-Agent MuJoCo [44], StarCraftII Multi-Agent Challenge (SMAC) [45]). HATRPO applies the trust region learning [46] to MADRL successfully, achieving the monotonic improvement guarantee for joint policy of multiple agents such as the trust region policy optimization (TRPO) algorithm [47]. The detailed theory of HATRPO is introduced in the following.

In the beginning, a cooperative Markov game with N agents exists. A joint policy $\pmb { \pi } = ( \pi _ { 1 } , \ldots , \pi _ { N } )$ to all agents exists. At time slot $t ,$ the agents are at state $s ^ { t }$ . Each agent utilizes its own policy $\pi _ { i }$ to take an action $a _ { i } ^ { t } ,$ and then the actions of all agents form the joint action $\pmb { a } ^ { t } = ( a _ { 1 } ^ { t } , \dots , a _ { N } ^ { t } )$ Afterwards, all agents receive a joint reward $\boldsymbol { r } ^ { t } ,$ and move to a new state $s ^ { t + \breve { 1 } }$ with probability $P ( s ^ { t + 1 } | s ^ { t } , \mathbf { \boldsymbol { a } } ^ { t } )$ . The goal of all agents is to maximize the expected total reward:

$$
J ( \pi ) = \mathbb { E } _ { s ^ { 0 : \infty } \sim \rho _ { \pi } ^ { 0 : \infty } , a ^ { 0 : \infty } \sim \pi } \left[ \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } r ^ { t } \right] ,\tag{15}
$$

where $\gamma \in [ 0 , 1 )$ is the discount factor and $\rho _ { \pi }$ is the marginal state distribution [16]. Besides, the state value function and the state-action value function are defined as $\begin{array} { r l r } { V ^ { \pi } ( s ^ { t } ) } & { { } = } & { { \mathbb { E } } _ { a ^ { t : \infty } \sim \pi , s ^ { t + 1 : \infty } \sim P } \left[ \sum _ { l = 0 } ^ { \infty } \gamma ^ { l } r ^ { t + l } \right] } \end{array}$ and $\begin{array} { r } { Q ^ { \pi } ( s ^ { t } , \pmb { a } ^ { t } ) = \mathbb { E } _ { s ^ { t + 1 : \infty } \sim P , \pmb { a } ^ { t + 1 : \infty } \sim \pi } \left[ \sum _ { l = 0 } ^ { \infty } \hat { \gamma } ^ { l } \overline { { r } } ^ { i + l } \right] } \end{array}$ . The advantage function is written as $A ^ { \pi } ( s ^ { t } , \bar { a ^ { t } } ) = Q ^ { \pi } ( s ^ { t } , \bar { a ^ { t } } ) - V ^ { \pi } ( s ^ { t } )$ Â·

To extend the key idea of TRPO to MADRL, a sequential policy update scheme [16] is introduced. Then, the following inequality can be derived to achieve the monotonic improvement guarantee for joint policy.

$$
J ( \bar { \pi } ) \geq J ( \pi ) + \sum _ { i = 1 } ^ { N } [ L _ { 1 : i } ^ { \pi } ( \bar { \pi } _ { 1 : i - 1 } , \bar { \pi } _ { i } ) - C \mathrm { D } _ { \mathrm { K L } } ^ { \operatorname* { m a x } } ( \pi _ { i } , \bar { \pi } _ { i } ) ] .\tag{16}
$$

where ÏÂ¯ is the next candidate joint policy. $\mathrm { D } _ { \mathrm { K L } } ^ { \mathrm { m a x } } ( \pi _ { i } , \bar { \pi } _ { i } ) =$ $\begin{array} { r } { \operatorname* { m a x } _ { s } \mathrm { D } _ { \mathrm { K L } } ( \pi _ { i } ( \cdot | s ) , \bar { \pi } ( \cdot | s ) ) } \end{array}$ is the maximal KL-divergence to measure the gap between two policies. $\begin{array} { r l } { \bar { C } } & { { } = } \end{array}$ $\begin{array} { r } { \frac { 4 \gamma \operatorname* { m a x } _ { s , a } \left| A ^ { \pi } \left( s , \pmb { a } \right) \right| } { \check { \iota } _ { \pmb { \cdot } } } } \end{array}$ (1âÎ³)2 is the penalty coefficient. Moreover, $L _ { 1 : i } ^ { \pi } ( \dot { \bar { \pi } } _ { 1 : i - 1 } , \bar { \pi } _ { i } )$ is a surrogate equation of the i-th agent, which is expressed as

$$
\begin{array} { r l } & { L _ { 1 : i } ^ { \pi } \big ( \bar { \pi } _ { 1 : i - 1 } , \bar { \pi } _ { i } \big ) } \\ & { \qquad = \mathbb { E } _ { s \sim \rho _ { \pi } , a _ { 1 : i - 1 } \sim \bar { \pi } _ { 1 : i - 1 } , a _ { i } \sim \bar { \pi } _ { i } } \big [ A _ { i } ^ { \pi } ( s , a _ { 1 : i - 1 } , a _ { i } ) \big ] , } \end{array}\tag{17}
$$

where $A _ { i } ^ { \pi } ( s , \pmb { a } _ { 1 : i - 1 } , \ b { a } _ { i } )$ is the local advantage function of each agent. Based on the above theory, all agents can update their policies sequentially, and the updating procedure is given as

$$
\pi _ { i } ^ { k + 1 } = \underset { \pi _ { i } } { \operatorname { a r g m a x } } \big ( L _ { 1 : i } ^ { \pi ^ { k } } ( \pi _ { 1 : i - 1 } ^ { k + 1 } , \pi _ { i } ) - C \mathrm { D } _ { \mathrm { K L } } ^ { \operatorname* { m a x } } ( \pi _ { i } ^ { k } , \pi _ { i } ) \big ) .\tag{18}
$$

Furthermore, the sequential updating scheme does not require that the updating order of all agents is fixed, meaning that the updating order can be flexibly adjusted at each iteration. As such, the algorithm can adapt to dynamic changes in the environment and progressively assimilate new information in non-static conditions.

To implement the above procedure for parameterized joint policy $\pmb \theta = ( \theta _ { 1 } , \dots , \theta _ { N } )$ in practice, in HATRPO, the amendment similar to TRPO is performed. As the maximal KL-divergence penalty $\mathrm { D } _ { \mathrm { K L } } ^ { \mathrm { m a x } } ( \pi _ { \theta _ { i } ^ { k } } , \pi _ { \theta _ { i } } )$ is hard to compute, it is replaced by the expected KL-divergence constraint $\mathbb { E } _ { s \sim \rho _ { \pi _ { a k } } } \mathrm { \hat { [ D _ { K L } ( } } \pi _ { \theta _ { i } ^ { k } } ( \cdot | s ) , \pi _ { \theta _ { i } } \hat { ( } \cdot | s ) ) ] \le \delta _ { \iota }$ , where Î´ is a threshold hyperparameter. Then, at the k+1-th iteration, given a permutation, all agents can optimize their policy parameters sequentially according to the method as follows:

$$
\begin{array} { r l } & { \theta _ { i } ^ { k + 1 } = } \\ & { \underset { \theta _ { i } } { \arg \operatorname* { m a x } } \mathbb { E } _ { s \sim \rho _ { \pi _ { \theta ^ { k } } } , a _ { 1 : i - 1 } \sim \pi _ { \theta _ { 1 : i - 1 } ^ { k + 1 } } , a _ { i } \sim \pi _ { \theta _ { i } } } [ A _ { i } ^ { \pi _ { \theta ^ { k } } } ( s , a _ { 1 : i - 1 } , a _ { i } ) ] , } \\ & { \mathrm { ~ s . ~ t . ~ } \mathbb { E } _ { s \sim \rho _ { \pi _ { \theta ^ { k } } } } [ \mathrm { D } _ { \mathrm { K L } } ( \pi _ { \theta _ { i } ^ { k } } ( \cdot | s ) , \pi _ { \theta _ { i } } ( \cdot | s ) ) ] \leq \delta . } \end{array}\tag{19}
$$

For the computation of the above equation, similar to TRPO, the linear approximation to the objective function and the quadratic approximation to KL constraint are applied, derivating a closed-form updating scheme that is shown as

$$
\theta _ { i } ^ { k + 1 } = \theta _ { i } ^ { k } + \alpha ^ { j } \sqrt { \frac { 2 \delta } { g _ { i } ^ { k } ( H _ { i } ^ { k } ) ^ { - 1 } g _ { i } ^ { k } } } ( H _ { i } ^ { k } ) ^ { - 1 } g _ { i } ^ { k } .\tag{20}
$$

$\alpha ^ { j } \in ( 0 , 1 )$ is a coefficient that is found via backtracking line search. $\begin{array} { c c l } { \pmb { { \dot { H } } } _ { i } ^ { k } } & { = } & { \nabla _ { \theta _ { i } } ^ { 2 } \mathbb { E } _ { s \sim \rho _ { \pi _ { a k } } } [ \mathrm { D } _ { \mathrm { K L } } ( \pi _ { \theta _ { i } ^ { k } } ( \cdot | s ) , \pi _ { \theta _ { i } } ( \cdot | s ) ) ] | _ { \theta _ { i } = \theta _ { i } ^ { k } } ^ { } } \end{array}$ Î¸   is the Hessian of the expected KL-divergence. $\mathbf { \Delta } _ { \mathbf { \it { g } } _ { i } ^ { k } }$ is the gradient of the objective in Eq. (19), whose computation requires the estimation about $\mathbb { E } _ { a _ { 1 : i - 1 } \sim \pi _ { \theta _ { \star } ^ { k + 1 } } , a _ { i } \sim \pi _ { \theta _ { i } } } [ A _ { i } ^ { \pi _ { \theta ^ { k } } } \widehat ( s , a _ { 1 : i - 1 } , a _ { i } ) ]$ According to the derivation in [16], given a batch B of trajectories with length $T , g _ { i } ^ { k }$ can be computed as

$$
g _ { i } ^ { k } = \frac { 1 } { B } \sum _ { b = 1 } ^ { B } \sum _ { t = 0 } ^ { T } M _ { 1 : i } ( s ^ { t } , \pmb { a } ^ { t } ) \nabla _ { \theta _ { i } } \log \pi _ { \theta _ { i } } ( a _ { i } ^ { t } | s ^ { t } ) | _ { \theta _ { i } = \theta _ { i } ^ { k } } ,\tag{21}
$$

<!-- image-->  
Fig. 4. Flowchart of HATRPO-UCB algorithm for UAV-enabled CB.

where

$$
M _ { 1 : i } ( s ^ { t } , { \pmb a } ^ { t } ) = \frac { \pi _ { \pmb { \theta } _ { 1 : i - 1 } ^ { k + 1 } } ( { \pmb a } _ { 1 : i - 1 } ^ { t } | s ^ { t } ) } { \pi _ { \pmb { \theta } _ { 1 : i - 1 } ^ { k } } ( { \pmb a } _ { 1 : i - 1 } ^ { t } | s ^ { t } ) } { \cal A } ^ { \pi _ { \pmb { \theta } ^ { k } } } ( s ^ { t } , { \pmb a } ^ { t } ) .\tag{22}
$$

$\frac { \pi _ { \theta _ { 1 : i - 1 } ^ { k + 1 } } ( \boldsymbol { a } _ { 1 : i - 1 } ^ { t } | \boldsymbol { s } ^ { t } ) } { \pi _ { \theta _ { 1 : i - 1 } ^ { k } } ( \boldsymbol { a } _ { 1 : i - 1 } ^ { t } | \boldsymbol { s } ^ { t } ) }$ is the compound policy ratio about the previous agents $1 : i - 1$ , which can be computed easily after these agents complete their updates.

Although HATRPO has the excellent performance, it still faces many challenges in solving the UCBMOP. First, the formulated problem involves the complex cooperation among UAVs. Furthermore, only one time slot exists for each episode in the problem, which is different from other traditional MADRL tasks. Thus, it is necessary to take measures to connect the algorithm with the problem closely. Second, there are many UAVs in the problem, which may increase the input dimension of critic network substantially, influencing the critic learning. Finally, the conventional HATRPO uses the Gaussian distribution to sample actions. However, all actions have the finite range in the problem. Thus, using the Gaussian distribution may induce the bias to the policy gradient estimation. Accordingly, these reasons motivate us to propose the HATRPO-UCB, and the details are described in the following sections.

## 4.2.2 Algorithm Design of HATRPO-UCB

In the proposed HATRPO-UCB, we take conventional HA-TRPO as the foundation algorithm framework, and propose three techniques that are observation enhancement, agentspecific global state and Beta distribution for policy, to enhance the performance of the algorithm.

Observation enhancement: In MADRL, the environmental information is usually the state that guides the agents to take action. However, in UCBMOP, each episode only has one time slot, and the UVAA may communicate with different remote BSs at various episodes. In this case, the state consisting of the simple Cartesian coordinates of the UAVs and BSs may not precisely characterize their positional relationship. This is because the distance between the UVAA and BSs is significantly larger than the relative distance between the UAVs, and even the same set of UAV coordinates may represent different environmental states when serving various BSs (e.g., transmission angle and distance). To overcome this issue, we propose two observation enhancement strategies as follows. First, we design a spherical coordinate enhancement strategy with dynamically changing origins to represent the UAV positions. Instead of the Cartesian coordinate of each UAV, we set the state to the spherical coordinates with the BS in the current episode as the origin. In this way, the state can adequately express the information about the orientation and distance between the BS and the UVAA. Second, we propose a position representation based on reference points to characterize the BS locations. Specifically, we regard the closest point to the target BS in the monitor area as the reference point and then adopt this reference point to replace the target BS as the state. This adjustment retains the BS information but amplifies the position differences between the UAVs, which better expresses the relative positions of the UAVs. The enhanced state and observation contain representative and adaptive information about the environment, which ensures the proposed method remains effective when the location of the served BS at different episodes changes significantly.

Agent-specific global state: In general, the global state employed by MADRL algorithms has two forms, which are the concatenation of all local observations and environmentprovided global state. However, in the considered scenarios, the number of agents (i.e., UAVs) is often large, which means that the input dimension of the critic network grows a lot when using the concatenation of all local observations. This condition will increase the learning burden, thereby making the performance of critic learning degrade. Additionally, the environment-provided global state is also not an appropriate choice because its contained information is not sufficient, which only contains the coordinates and excitation current weights of all UAVs, as well as the coordinates of the reference point. Inspired by [42], we design an agentspecific global state that combines the global information provided by the environment and some features from local observation, such as the spherical coordinate of the target BS that is relative to the UAV $( \theta _ { i } , \phi _ { i } , d _ { i } )$ and the distance between two UAVs $d _ { j , i } ,$ as the input of the critic network. This agent-specific global state can improve the fitting performance of critic learning and thus achieve better MADRL performance.

Beta distribution for policy: In the conventional HA-TRPO, the actor uses the Gaussian distribution to sample actions. However, the Gaussian distribution has been demonstrated to have the negative impact on reinforcement learning [48]. Specifically, for an action with the finite interval, the Gaussian distribution with infinite support will define the action range out of its boundary. Furthermore, the probability density of all actions is greater than 0, but the probability of actions beyond boundary should equal to 0. Hence, in our scenario where all actions of UAV have the finite interval, it is inevitable that some actions sampled from the Gaussian distribution will be truncated, leading to the boundary effect. Then, the boundary effect may cause bias about policy gradient estimation.

To handle the above issue, the authors of [48] conducted the research on Beta distribution for reinforcement learning. The study indicates that the Beta distribution does not have a bias because the Beta distribution has a finite range (i.e., [0, 1]), and thus the probability density of actions beyond the boundary is guaranteed to be 0. Furthermore, experimental results show that the Beta distribution can make reinforcement learning algorithms converge faster and obtain higher rewards. Thus, in this paper, we choose the Beta distribution instead of the original Gaussian distribution, and then the Beta distribution is defined as

$$
f ( x ; \alpha , \beta ) = { \frac { \Gamma ( \alpha + \beta ) } { \Gamma ( \alpha ) \Gamma ( \beta ) } } x ^ { \alpha - 1 } ( 1 - x ) ^ { \beta - 1 } ,\tag{23}
$$

where Î± and $\beta$ are the shape parameters, and $\Gamma ( \cdot )$ is the Gamma function that extends factorial to real numbers. In addition, Î± and $\beta$ are set to be not less than $1 \left( \mathrm { i . e . , } \alpha , \beta \geq 1 \right)$ in the work, which are modeled by softplus and then add a constant 1 [48].

## 4.2.3 Algorithm Workflow

Fig. 4 displays the framework of the proposed HATRPO-UCB algorithm, which has two phases that are the training phase and the implementation phase. Each UAV as an agent has a replay buffer and two networks (i.e., the actor network and critic network). The replay buffer is used to collect the data about the interaction between the UAV and the environment. Then, a central server is deployed with the replay buffers and networks of all agents for training.

In the beginning, the central server will initialize the parameters of networks. Then, at each time slot, the central server will exchange the information with UAVs and then control them, where the amount of the information is very small because it only includes the observation information of UAVs and actions required to be done by UAVs, and the communication distance is very short compared with that between the UAVs and the BS. Hence, for performing the communication tasks, the above communication overhead is very small and acceptable. Then, for illustrating the specific process at each time slot, taking the i-th agent as an example, after the central server receives the information, the actor network $\pi _ { \boldsymbol { \theta } _ { i } }$ utilizes the observation $o _ { i }$ to generate a Beta distribution about action, and then an action $a _ { i }$ is sampled from the Beta distribution and sent to the UAV. The critic network is used to predict the Q-value of current global state $s _ { i } .$ . After executing the sampled action, the i-th agent receives a reward $r _ { i }$ from the environment and observes the next local state $o _ { i } ^ { \prime }$ and global state $s _ { i } ^ { \prime } .$ After that, the above information tuple $\langle o _ { i } , s _ { i } , a _ { i } , r _ { i } \rangle$ will be stored in the replay buffer $B _ { i }$

Algorithm 1 Heterogeneous-Agent Trust Region Policy Op  
timization for UCBMOP (HATRPO-UCB)   
Input: Number of episodes $N ^ { \mathrm { E p i } }$ , number of agents $N ,$   
batch size $B ,$ stepsize $\alpha ,$ possible steps in line search $L ,$ line   
search acceptance threshold $\kappa .$   
Initialize: Actor networks $\{ \theta _ { i } ^ { 0 } , \forall i \in \mathcal { N } \}$ , Critic networks   
$\{ \phi _ { i } ^ { 0 } , \forall i \in \mathcal { N } \}$ , Replay buffers $\{ B _ { i } , \forall i \in \mathcal { N } \}$   
1: for episode $\mathbf { \Psi } = 1 , \dots , N ^ { \mathrm { E p i } }$ do   
2: Initialize the environment, acquire local observations   
and global states of all agents $\{ ( o _ { i } , s _ { i } ) , \forall i \in \mathcal { N } \}$ .   
3: Each UAV selects its own action $a _ { i } = \pi _ { \theta _ { i } ^ { k } } ( o _ { i } )$ from   
the Beta distribution.   
4: All UAVs execute actions to complete CB and then   
receive their rewards $\{ r _ { i } , \forall i \in \mathcal { N } \}$   
5: Push transition of each agent $\langle o _ { i } , s _ { i } , a _ { i } , r _ { i } \rangle$ into   
its own replay buffer $B _ { i }$   
6: if the training condition is met then   
7: Draw a random permutation of agents $i _ { 1 : N } .$   
8: for agent $i = 1 , \ldots , N$ do   
9: Sample a random mini-batch of B transitions   
from $\boldsymbol { B } _ { i }$   
10: Compute advantage function $A _ { i } ( s _ { i } , \pmb { a } )$ based   
on the critic network.   
11: Obtain the compound policy ratio of the   
previous agents $\begin{array} { r } { \prod _ { l = 1 } ^ { i - 1 } \frac { \bar { \pi } _ { \theta _ { l } ^ { k + 1 } } \bar { ( a _ { l } | o _ { l } ) } } { \pi _ { \theta _ { l } ^ { k } } ( a _ { l } | o _ { l } ) } , } \end{array}$ set   
$\begin{array} { r } { M _ { i } ( s _ { i } , \pmb { a } ) = A _ { i } ( s _ { i } , \pmb { a } ) \prod _ { l = 1 } ^ { i - 1 } \frac { \pi _ { \theta _ { l } ^ { k + 1 } } ( a _ { l } | o _ { l } ) } { \pi _ { \theta _ { l } ^ { k } } ( a _ { l } | o _ { l } ) } . } \end{array}$   
12: Use $M _ { i } ( s _ { i } , \pmb { a } )$ to estimate the gradient of   
maximization objective of agent $\mathbf { \Delta } _ { g _ { i } ^ { k } }$ according   
to Eq. (21).   
13: Compute the Hessian of the expected   
KL-divergence $\pmb { H } _ { i } ^ { k }$ to approximate the KL   
constraint.   
14: $\mathbf { \Delta } _ { g _ { i } ^ { k } } ^ { k }$ and $\pmb { H } _ { i } ^ { k }$ are introduced to update the   
parameter of actor network $\theta _ { i } ^ { k + 1 }$ according to   
$\mathrm { { \bar { E } q } . }$ (20).   
15: Update critic network by the following   
equation:   
$\phi _ { i } ^ { k + 1 } = :$ argminÏi 1B $\sum _ { b = 1 } ^ { B } \big ( V _ { \phi _ { i } } ( s _ { i } ^ { b } ) - R _ { i } ^ { b } ) ^ { 2 } ,$   
where $R _ { i } ^ { b }$ is the discounted return at state $s _ { i } ^ { b } .$   
16: end for   
17: end if   
18: end for   
Output: Trained models of all agents.

All agents will execute more time slots until their replay buffers accumulate enough data, and then the replay buffers will randomly select a mini-batch of tuples for training networks. The sequential updating scheme is adopted to update policies of all agents. In each training, all agents are updated sequentially in a randomly generated order. For the i-th agent, the first step is to estimate the gradient $\mathbf { \Delta } _ { \mathbf { \it { g } } _ { i } ^ { k } } ^ { k }$ , before that, the advantage function of i-th agent $A _ { i } ( s _ { i } , \pmb { a } )$ and the compound policy ratio of the previous agents $\begin{array} { r } { \prod _ { l = 1 } ^ { i - 1 } \frac { \pi _ { \theta _ { l } ^ { k + 1 } } \left( a _ { l } | o _ { l } \right) ^ { \star } } { \pi _ { \theta _ { l } ^ { k } } \left( a _ { l } | o _ { l } \right) } } \end{array}$ are required to compute. Then, the Hessian of the expected KL-divergence $\pmb { H } _ { i } ^ { k }$ is computed to approximate the KL constraint. After completing the computation of $\mathbf { \Delta } _ { \mathbf { \it { g } } _ { i } ^ { k } }$ and $\pmb { H } _ { i } ^ { k } ,$ , the parameter of actor network $\theta _ { i }$ can be updated via backtracking line search. $\mathrm { A s }$ for the critic network $V _ { \phi _ { i } }$ , the update of network parameter can be achieved by optimizing the following loss function: $\begin{array} { r } { \frac { 1 } { B } \sum _ { b = 1 } ^ { B } ( V _ { \phi _ { i } } ( s _ { i } ^ { b } ) - { R } _ { i } ^ { b } ) ^ { 2 } } \end{array}$ . Therefore, the above updating procedure will be repeated until HATRPO-UCB converges. The whole training process can be seen in Algorithm 1.

During the implementation stage, only the trained actor network is deployed to the UAV. In each communication mission, all UAVs receive the local observations from the environment, and then select actions through the actor networks. Afterwards, according to the selected actions, all UAVs move to the target locations and adjust the excitation current weights for performing CB. Compared with the training stage, the implementation stage is completed online and does not need much computational resource. In contrast, the training stage costs much computational resource, which is conducted offline in a central server.

## 4.2.4 Analysis of HATRPO-UCB

In this section, the computational complexity of the training and implementation stage of the proposed HATRPO-UCB is discussed.

Complexity of training. For $n _ { \mathrm { u a v } }$ agents, each agent is equipped with an actor network and a critic network that are formed by DNNs. A DNN consists of an input layer, L fully connected layers and an output layer, where $z _ { 0 } , z _ { i }$ and $z _ { L + 1 }$ denote the number of neurons of input layer, i-th fully connected layer and output layer, respectively. Then, the computational complexity of DNN at each time slot is $O ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot z _ { i } )$

At each training process, a mini-batch of data with $n _ { \mathrm { e p i } }$ episodes is sampled from the replay buffer, but each episode only contains one time slot. Additionally, the critic network is updated by the stochastic gradient methods, thus the total computational complexity of critic network is $\begin{array} { r } { O ( n _ { \mathrm { e p i } } \cdot ( \sum _ { i = 1 } ^ { L + 1 } \hat { z _ { i - 1 } } \cdot z _ { i } ) ) } \end{array}$ . However, the actor network is updated using the backtracking line search. In Eq. (20), the gradient $\mathbf { \Delta } _ { g _ { i } ^ { k } }$ is first computed, whose computational complexity is $\begin{array} { r } { O ( n _ { \mathrm { e p i } } \cdot ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot z _ { i } ) ) } \end{array}$ . Then the Hessian of expected KL-divergence $\pmb { H } _ { i } ^ { k }$ is computed to approximate the KL constraint. The computational complexity of expected KL-divergence is $O ( n _ { \mathrm { e p i } } \cdot ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot z _ { i } ) \stackrel { \cdot } { ) }$ , and the computational one of Hessian matrix is $O ( ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot z _ { i } ) ^ { 2 } ) .$ . Hence, the computational complexity of $\pmb { H } _ { i } ^ { k }$ is $O ( n _ { \mathrm { e p i } } \cdot ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 }$ $\begin{array} { r } { z _ { i } ) + ( \sum _ { i = 1 } ^ { \cdot { \hat { L } } + 1 } z _ { i - 1 } { \cdot { z _ { i } } } ) ^ { 2 } ) } \end{array}$ . For computing $( H _ { i } ^ { k } ) ^ { - 1 } g _ { i } ^ { k }$ , the conjugate gradient algorithm is adopted, which obtains result by searching iteratively until convergence. The computational complexity of each iteration is $O \big ( ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot \hat { z _ { i } } ) ^ { 2 } \big )$ . Then the total computational complexity of $( H _ { i } ^ { k } ) ^ { - 1 } g _ { i } ^ { k }$ is $O ( n _ { \mathrm { e p i } }$ $\textstyle \bigl ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot \dot { z } _ { i } \bigr ) + l _ { \mathrm { c o n j } } \cdot \bigl ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot z _ { i } \bigr ) ^ { 2 } \bigr )$ , where $l _ { \mathrm { c o n j } }$ is the number of iterations. During the backtracking line search, the computational complexity is $O ( l _ { \mathrm { b t } } { \cdot } n _ { \mathrm { e p i } } { \cdot } ( \sum _ { i = 1 _ { \cdot } } ^ { { \bar { L } } + 1 } z _ { i - 1 } { \cdot } z _ { i } ) )$ , where $l _ { \mathrm { b t } }$ is the search number and $O ( n _ { \mathrm { e p i } } \cdot ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot z _ { i } ) )$ is the computational complexity in each search. Hence, the total computational complexity of actor network is $O ( l _ { \mathrm { b t } } \cdot n _ { \mathrm { e p i } } \cdot ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot z _ { i } ) ^ { \cdot } + l _ { \mathrm { c o n j } } \cdot ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } \cdot z _ { i } ) ^ { 2 } )$ Assume that HATRPO-UCB needs to be trained $l _ { \mathrm { t } }$ times for convergence, the overall computational complexity in the training phase is $\begin{array} { r } { O ( l _ { \mathrm { t } } \cdot n _ { \mathrm { u a v } } \cdot \hat { ( } l _ { \mathrm { b t } } \cdot n _ { \mathrm { e p i } } \cdot ( \sum _ { i = 1 } ^ { L \hat { + } 1 } z _ { i - 1 } \cdot z _ { i } ) + } \end{array}$ $l _ { \mathrm { c o n j } } \cdot ( \stackrel {  } { \sum _ { i = 1 } ^ { L + 1 } } z _ { i - 1 } \cdot z _ { i } ) ^ { 2 } ) )$

Complexity of inference. In the implementation phase, all UAVs only use the trained actor networks to make decisions. Therefore, the computational complexity of HATRPO-UCB in the implementation stage is $\begin{array} { r } { \hat { O ( } n _ { \mathrm { u a v } } \cdot ( \sum _ { i = 1 } ^ { L + 1 } z _ { i - 1 } } \end{array}$ $z _ { i } ) )$ .

Remark 3. Note that determining the theoretical bounds and convergence of the proposed MADRL-based algorithm confronts significant challenges [49]. Specifically, MADRL involves tuning numerous hyperparameters, such as learning rates, network architectures, and exploration strategies, resulting in an explosion of potential combinations. Thus, analyzing theoretical bounds and convergence becomes nearly infeasible given the vast parameter space. Moreover, DNNs introduce approximation errors when modeling complex functions, particularly in high-dimensional state spaces of the formulated optimization problem. These errors can lead to suboptimal performance in certain states, complicating the analysis of theoretical bounds and convergence. In addition, MADRL models interact with environments that introduce uncertainty factors, including noise and randomness. These uncertainties can yield different outcomes in various interaction trajectories, further complicating the analysis of the theoretical bounds and convergence [50]. Thus, we evaluate the performance of the proposed HATRPO-UCB by conducting extensive simulations like the works in [40], [51] in the following.

## 5 SIMULATION RESULTS

In this section, we evaluate the performance of the proposed HATRPO-UCB algorithm for UCBMOP.

## 5.1 Simulation Configuration

We implement simulations in an environment with Python 3.8 and Pytorch 1.10, and perform all experiments on a server with AMD EPYC 7642 48-Core CPU, NVIDIA GeForce RTX 3090 GPU and 128GB RAM.

In the simulation, a 100 m Ã 100 m square area is considered, where 16 UAVs are flying in the area. The mass (mUAV ), the minimum and maximum flying heights $( H _ { m i n }$ and $H _ { m a x } )$ of each UAV are set as 2 kg, 100 m and 120 m [22], respectively. The minimum distance between any UAVs $( d _ { m i n } )$ is 0.5 m. Moreover, the transmit power of each UAV, the carrier frequency (fc) and the total noisy power spectral density are 0.1 W, 2.4 GHz and -157 dBm/Hz, respectively [21] [52]. The path loss exponent (Î±), as well as the attenuation factors of LoS and NLoS links $( \mu _ { L o S } , \mu _ { N L o S } )$ are 2, 3 dB and 23 dB, respectively [53]. Other parameter configurations about system model are summarized in Table 2. Based on these settings and the mathematical models shown in Section 3, we build a simulation environment for the DRL model to interact and collect data.

TABLE 2 Parameter settings
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Fuselage drag ratio (do)</td><td>0.6</td></tr><tr><td>Air density (p)</td><td> $1 . 2 2 5 \mathrm { k m } / \mathrm { m } ^ { 3 }$ </td></tr><tr><td>Rotor solidity (s)</td><td>0.05</td></tr><tr><td>Rotor disc area (A)</td><td>0.503mÂ²</td></tr><tr><td>Tip speed of the rotor blade  $( v _ { t i p } )$ </td><td> $1 2 0 ~ \mathrm { m / s }$ </td></tr><tr><td>Mean rotor induced velocity in hover (vo)</td><td>4.03</td></tr><tr><td>Blade profile power (PB)</td><td>79.76</td></tr><tr><td>Induced power (P1)</td><td>88.66</td></tr><tr><td>Discount factor (Î³)</td><td>0.99</td></tr><tr><td>Number of line searches</td><td>10</td></tr><tr><td>Clip parameter for loss value</td><td>0.2</td></tr><tr><td>Max norm of gradients</td><td>10</td></tr><tr><td>Accept ratio of loss improve</td><td>0.5</td></tr><tr><td>Weight initialization gain for actor network</td><td>0.01</td></tr><tr><td>Weight initialization for neural network</td><td>Orthogonal</td></tr></table>

In the MADRL stage, an environment is built according to the UCBMOP. The MADRL algorithm learns by interacting with the environment. During the training stage, the environment will run $4 \times 1 0 ^ { 5 }$ episodes, where each episode only has one time slot. For the settings of reward weight coefficients, we first set the weight coefficients by normalizing each reward to make the rewards on the same order of magnitude. Then, we fine-tune the reward weights by considering their importance and characteristics (the tuning process and results are shown in Appendix A of the supplemental material). As such, the reward weight coefficients Ï1, Ï2, Ï3, Ï4, and $\omega _ { 5 }$ are set to 100, 4, 30, 12 and 5, respectively.

In HATRPO-UCB, all actor and critic networks are threelayer fully connected neural networks (i.e., two hidden layers and one output layer). Each hidden layer contains 64 neurons, which is initialized by orthogonal initialization, and it is equipped with ReLU activation function. The actor network is updated by the backtracking line search, meanwhile, the KL-divergence between the new actor network and the old one must meet the KL-threshold which is set as 0.001. The Adam optimizer [54] is employed to update the critic network, where the learning rate is 0.005. The value setting of other related parameters is also presented in Table 2.

In addition, to verify the effectiveness and performance of HATRPO-UCB, except for conventional HATRPO, the following baseline methods are also introduced for comparison.

LAA: All UAVs form a linear antenna array (LAA), and they are symmetrically excited and located about the origin of the array [21].

RAA: A rectangular antenna array (RAA) is formed by all UAVs, where all UAVs are also symmetrically excited and located about the origin of the array.

MADDPG: Multi-Agent Deep Deterministic Policy Gradient (MADDPG) is based on the centralized training with decentralized execution (CTDE)

paradigm, extending Deep Deterministic Policy Gradient (DDPG) to MADRL [55].

IPPO: Independent Proximal Policy Optimization (IPPO) is that the single-agent PPO algorithm is adopted directly to solve multi-agent tasks [56]. The IPPO has been justified that it can achieve excellent performance on SMAC.

MAPPO: Multi-Agent Proximal Policy Optimization (MAPPO) is an extension of PPO [42]. MAPPO utilizes parameter-sharing trick, then all agents jointly use a policy network and a value network. The global state is the input of the value network.

Note that the proposed observation enhancement technique are added to these abovementioned MADRL algorithms, so that making sure that they can solve the UCB-MOP properly. Furthermore, they are also tuned continuously and achieve the convergence.

## 5.2 Convergence Analysis

In practice, DRL-based models are usually deployed only after achieving convergence through training. Even if the practical environment changes dynamic, we also need to re-train and fine-tune the model before deploying it. Thus, the convergence performance of HATRPO-UCB is vital. As such, in the section, we compare the convergence performance of HATRPO-UCB with other algorithms. Fig. 5 shows the convergence performance of all algorithms. It can be observed that all algorithms converge successfully. HATRPO-UCB achieves the fastest convergence at approximately 750 epoch, then the second algorithm is HATRPO. MAPPO, IPPO and MADDPG are slowest, which all begin to converge at about 1400 epoch. However, in the performance, the reward obtained by HATRPO is higher than that of the HATRPO-UCB, reaching about 85. IPPO and MAPPO are both worse than HATRPO-UCB. MADDPG has the poorest performance, which only converges to around 80. The reasons are that the introduced observation enhancement provides representative and adaptive information for the agents to take action, the agent-specific global state is able to improve the fitting performance of critic learning, and the Beta distribution overcomes the boundary effect issue. Such improvements could effectively address the major issues in the training process, thus facilitating the algorithm in achieving reliable and high-performance outcomes and converging rapidly.

To further analyze these algorithms, we also depict the optimization process of all alogrithms to the UAV energy consumption in Fig. 6. It can be observed that HATRPO-UCB obtains the best optimization performance, making the energy consumption of UAV reduce to about 700 J and achieving the convergence at approximately 1000 epochs. Then, HATRPO has the certain optimization performance, but it does not have the obvious optimization effect like HATRPO-UCB and the ultimate optimization result is not better than that of HATRPO-UCB. In addition, MAPPO, IPPO and MADDPG have no optimization effect, whose optimization performance becomes worse continously with the training process. The more details about performance of all algorithms will be introduced in the following sections.

TABLE 3  
Numerical optimization results of different methods
<table><tr><td rowspan="2">Method</td><td colspan="2">First BS</td><td colspan="2">Second BS</td></tr><tr><td>Transmission rate (bps)</td><td>Energy consumption (J)</td><td>Transmission rate (bps)</td><td>Energy consumption (J)</td></tr><tr><td>LAA</td><td> $\overline { { 1 . 0 2 0 \times 1 0 ^ { 6 } } }$ </td><td>15208</td><td> $\overline { { 1 . 7 9 3 \times 1 0 ^ { 7 } } }$ </td><td>/</td></tr><tr><td>RAA</td><td> $0 . 9 9 8 \times 1 0 ^ { 6 }$ </td><td>14217</td><td> $1 . 7 8 8 \times 1 0 ^ { 7 }$ </td><td>/</td></tr><tr><td>MADDPG</td><td> $1 . 0 2 7 \times 1 0 ^ { 6 }$ </td><td>22319</td><td> $\mathbf { 1 . 9 0 4 \times 1 0 ^ { 7 } }$ </td><td>17913</td></tr><tr><td>IPPO</td><td> $1 . 0 2 2 \times 1 0 ^ { 6 }$ </td><td>15790</td><td> $1 . 8 6 7 \times 1 0 ^ { 7 }$ </td><td>21110</td></tr><tr><td>MAPPO</td><td> $\mathbf { 1 . 0 3 5 \times 1 0 ^ { 6 } }$ </td><td>15025</td><td> $1 . 8 9 6 \times 1 0 ^ { 7 }$ </td><td>23252</td></tr><tr><td>HATRPO</td><td> $1 . 0 3 2 \times 1 0 ^ { 6 }$ </td><td>13765</td><td> $1 . 8 3 8 \times 1 0 ^ { 7 }$ </td><td>11779</td></tr><tr><td>HATRPO-UCB</td><td> $1 . 0 2 9 \times 1 0 ^ { 6 }$ </td><td>13401</td><td> $1 . 8 2 5 \times 1 0 ^ { 7 }$ </td><td>10261</td></tr></table>

<!-- image-->  
Fig. 5. Convergence performance of different methods.

<!-- image-->  
Fig. 6. Optimization results of the UAV energy consumption obtained by different methods.

## 5.3 Performance Comparison

The practical performance of all approaches is compared in the section. In our system, all UAVs have other kinds of tasks after completing CB, but they may continue to perform CB for communicating with another BS. Thus, we will analyze the actual performance of UVAA communicating continuously with two BSs. Table 3 shows the numerical optimization results of various methods. It can be observed that HATRPO-UCB achieves the best performance on the optimization of energy consumption of UVAA, and obtains the outstanding results on the transmission rate optimization. The highest transmission rates to the two BSs are achieved by MAPPO and MADDPG, respectively, but they consume more energy. Furthermore, remaining MADRL approaches also outperform HATRPO-UCB in terms of the optimization of transmission rate. The reason may be that all UAVs optimized by these algorithms fly higher and closer to BS, thus the UVAA can get the lower path loss and shorter distance with BS. However, the more energy consumption will be induced.

We also show the flight paths of UAVs in the Appendix B of supplemental material. Benefiting from the DNN, the UVAA optimized by MADRL methods can directly perform CB for the second BS without consuming the much computation resource. Besides, we can also observe that all UAVs optimized by other MADRL approaches can achieve the higher altitude and the shorter distance with BS compared with HATRPO-UCB, and thus, they can obtain the higher transmission rate but will consume more energy as shown in Table 3. In summary, HATRPO-UCB learns the best strategy, making UVAA obtain the great transmission rate and save the energy at the same time.

## 5.4 Ablation Analysis

For verifying the effectiveness of proposed techniques, we conduct some ablation experiments. Fig. 7a displays some convergence performance as HATRPO-UCB is not implemented with some techniques. When HATRPO-UCB is not equipped with observation enhancement, we can observe that the performance is decreased. For further analysis, we present the practical performance of UVAA whether adopting observation enhancement or not in Fig. 8. As can be seen, when using observation enhancement, all UAVs can cooperate better, and they can also fly toward the BS to shorten the communication distance. On the contrary, without observation enhancement, all UAVs are scattered and have no clear flight targets. Furthermore, the CB performance is also influenced. The UVAA gets 24.85 reward about the transmission rate that is smaller than 25.05 obtained by the algorithm with observation enhancement. Therefore, the observation enhancement technique can significantly enable UVAA to learn the better strategy.

For testing the effectiveness of agent-specific global state, we replace the agent-specific global state, then use the environment-provided global state to evaluate the algorithm performance. As shown in Fig. 7a, HATRPO-UCB suffers from the performance degradation, which is because the information contained in the environment-provided global state is insufficient. Likewise, the critic learning is also influenced. Fig. 7b shows the learning curves of the critic network based on different global states, where the concatenation of all local observations is also added for comparison. It can be observed that the loss based on the agent-specific global state is lower than those under the other two global states. The reason is that the concatenation of local observations contains much redundant information, increasing the training burden, thus the learning process becomes very unstable and performance degrades. Then, the environment-provided global state also influences the training efficiency due to the insufficient information. However, according to the two figures, the influence produced by the two global states looks small. The reason could be that each episode only has one time slot in the UCBMOP, which distinctly differs from the regular MADRL tasks that require sequential decision-making. Hence, the role of critic network is not as significant as that in the regular tasks.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(c)

Fig. 7. Effectiveness of different techniques. (Observation enhancement, agent-specific global state and Beta distribution for policy).  
<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 8. The impact of the first technique to UVAA when communicating with a BS. (a) Without observation enhancement; (b) With observation enhancement.

As for Beta distribution for policy, an action sampled from the Beta distribution is not beyond its setting range, which is beneficial for the policy gradient estimation so that no bias occurs. We show the impact of Beta distribution for policy to the optimization about the energy consumption of UAV in Fig. 7c. It can be seen that Beta distribution for policy can make HATRPO-UCB optimize the UAV energy consumption well, reducing the energy consumption to around 700 J. However, without Beta distribution for policy, the optimization effect is substantially weakened, and the ultimate performance is not better than the algorithm with Beta distribution for policy. Therefore, according to [48], adopting the Beta distribution can help the agent learn the better strategy compared with the Gaussian distribution.

<!-- image-->

<!-- image-->  
(b)

<!-- image-->  
(c)

<!-- image-->  
(d)  
Fig. 9. Impact of different hyperparameter settings.

## 5.5 Impact of Hyperparameter Setting

The appropriate hyperparameter setting is critical to the algorithm. In HATRPO-UCB, the following hyperparameters are closely related to the algorithm performance that are the Optimizer, Learning rate, KL-threshold and Number of neurons. Hence, we analyze the impact of different values of each hyperparameter to HATRPO-UCB and simultaneously verify the reasonableness of our setting.

Algorithm performance under different optimizers. We first analyze the influence of various optimizers. Four optimizers are adopted to optimize the critic network, which are SGD [57], AdaGrad [58], RMSProp [59] and Adam [54], respectively. Their optimization results about the critic loss are shown in Fig. 9a. We can observe that, following the above order of optimizers, the optimized result becomes better. The performance of SGD is the worst, and the performance degradation appears in the following training. In the other optimizers, the training process also becomes unstable, resulting in an oscillating training curve. Then, when using Adam, the optimization performance is best and the training curve is smoothest. Therefore, Adam is choosen as the optimizer of HATRPO-UCB.

<!-- image-->  
Fig. 10. Transmission rate of UVAA under different phase errors.

Algorithm performance under different learning rates. Except for determining the optimizer, the critic network is also optimized based on a certain learning rate. Hence, Fig. 9b shows the learning process of critic network based on Adam under four learning rates. It can be observed that the optimization performance is best and the critic loss curve is smoothest as the learning rate is 0.005. When equaling to 0.05 or 0.0005, the curve oscillates slightly, which demonstrates that they are not appropriate under the current hyperparameter configuration. However, as the learning rate is 0.5, the training process gets very unstable and the performance degrades seriously at the end of training. The probable reason is that the learning rate is too large to produce the fluctuation.

Algorithm performance under different KL-thresholds. As for the KL-threshold, it is related to the update of actor network, but the KL-threshold also influences the learning speed of the critic network. Fig. 9c describes the critic loss curve under various KL-thresholds. We can observe that critic network begins to converge at approximately 1000 epoch as the KL-threshold is 0.001. Then, when the KLthreshold equals 0.1 and 0.01, the convergence speed of critic network becomes faster. However, these large KLthresholds also cause the instability to the critic learning in the second half of the whole process, and then also make the actor learning unstable. At last, 0.0001 KL-threshold makes the critic network learn so slowly that it converges at about 2000 epoch. Therefore, 0.001 KL-threshold is the best choice, which can make the critic network converge properly.

Algorithm performance under different neuron numbers. The number of neurons of hidden layer has the important effect to the DNN. Hence, Fig. 9d displays the performance of HATRPO-UCB under various numbers of neurons. We can observe that the convergence of critic network becomes slower as the number of neurons increases. The reason is that the large number of neurons makes the DNN big and complex, increasing the training burden. Hence, the number of neurons should be set to 64. In conclusion, according to all the above analysis, the hyperparameter setting with Adam, 0.005 learning rate, 0.001 KL-threshold and 64 neurons can make HATRPO-UCB achieve the best performance.

## 5.6 Impact of Imperfect Synchronization

The imperfect synchronization exists in CB, where the phase errors may be generated to influence the CB performance. Thus, we evaluate the impact of phase errors to the transmission performance of UVAA in the section.

The phase error at i-th UAV antenna is denoted as $\epsilon _ { i } ,$ and then the AF of UVAA can be rewritten as [60]

$$
\begin{array} { l } { { A F ( \theta , \phi ) = } } \\ { { \displaystyle \sum _ { i = 1 } ^ { N } { I _ { i } e ^ { j \Psi _ { i } } e ^ { j [ \frac { 2 \pi } { \lambda } ( x _ { i } \sin \theta \cos \phi + y _ { i } \sin \theta \sin \phi + z _ { i } \cos \theta ) + \epsilon _ { i } ] } } , } } \end{array}\tag{24}
$$

which $\epsilon _ { i }$ is assumed to follow a Tikhonov (or von Mises) distribution [60] [61]. The Tikhonov distribution is described as

$$
f _ { \epsilon } ( \epsilon ) = \frac { 1 } { 2 \pi I _ { 0 } ( \gamma ) } e ^ { \gamma c o s ( \epsilon ) } ,\tag{25}
$$

where $| \epsilon | < \pi , I _ { 0 } ( x )$ is the zero-th order modified Bessel function of the first kind, and Î³ is the inverse of the variance of the phase error. Then, the impact of phase errors to the transmission rate of UVAA under different values of $\gamma$ is shown in Fig. 10. It can be seen that the phase errors make the UVAA transmission performance decline. However, the generated phase errors become smaller as Î³ gets large, weakening the influence. For tackling the imperfect synchronization, there has been many works proposing various closed-loop or open-loop methods [31]. Furthermore, as the better synchronization algorithms are being proposed continuously, the impact of the imperfect synchronization will become less and less.

## 6 DISCUSSION

In this section, we discuss possible issues and solutions when deploying the proposed method in actual scenarios.

## 6.1 The Impact of UAV Collision

In this part, we discuss the impact of UAV collisions. As shown in Eq. (10), we set the minimum separation between two UAVs in UCBMOP. Following this, we set a penalty in the reward. Specifically, when any two UAVs violate the minimum separation constraint, they will get a tiny negative reward. As such, the proposed algorithm is able to make UAVs keep the minimum separation.

Moreover, many mature methods of UAV collision avoidance can also help the UAVs avoid violating the minimum separation in reality. For example, cameras, infrared, radar, LiDAR, sonar, etc, can be utilized by UAVs for obstacle detection. Based on this, the existing methods such as sense & avoid [62] can be appropriately embedded in the proposed optimization framework. This type of method focuses on reducing the computational cost with a short response time, deviating the UAVs from their original paths when needed, and then turning the UAVs to the previous flight state quickly. Since this method only consumes very little computational resources, energy, and time, it does not have a significant effect on the results of our work. As such, UAV collisions do not affect the effectiveness of the proposed method.

## 6.2 Additional Energy Consumption in Synchronization

In the considered system, there is additional energy consumption in the synchronization process for beacon signal reception (for closed loop) and location estimation (for open loop). However, this additional energy consumption is minor and can be ignored, and the reasons are as follows.

First, the closed-loop synchronization methods are based on feedback, whose energy consumption is quite small compared to the transmission or motion energy consumption of the UAVs. Specifically, the closed-loop synchronization approaches mainly include two types that are the iterative bit feedback and rich feedback methods. In the considered UAV-enabled CB scenarios, both of these closed-loop methods result in negligible energy consumption. This is because the recently proposed methods, such as iterative bit feedback approaches and rich feedback methods, can achieve rapid convergence with minimal energy consumption (less than 1 Joule in most cases). As such, this additional energy consumption is much smaller than the motion energy of UAVs (often several hundred Joules each second).

To demonstrate, we select a representative method, i.e., D1BF [63], to implement and evaluate. Following this, we introduce the energy consumption of point-to-point sending and broadcast receiving models from [64]. As shown in Fig. 11(a), the energy consumption of the closed-loop synchronization is not larger than even 1 Joule. Thus, we can demonstrate that the additional energy consumption of closed-loop synchronization in the considered system is quite small and can be ignored.

Second, compared to the closed-loop synchronization methods, the open-loop synchronization methods are not based on iterative feedback and have less energy consumption. Specifically, the open-loop synchronization approaches can be divided into two categories that are the intra-node communication and blind method. On the one hand, the intra-node methods are mostly based on the master-slave architecture [65]. We also use the energy model above and assume that the master node sends a reference beacon to all slave nodes and then the slaves synchronize their own phases. In this case, the energy consumption of synchronization of the UAVs can be shown in Fig. 11(b). As can be seen, it is also not larger than 1 Joule and can be omitted. On the other hand, blind methods allow the nodes to synchronize among themselves and do not require feedback from the receiver or the reference nodes. Hence, the overhead of the blind method can be smaller. Thus, the additional energy consumption of open-loop synchronization in the considered system is also small and can be ignored.

Overall, the additional energy consumption for synchronization does not have an evident impact on the availability of the proposed method.

## 7 CONCLUSION

In this paper, a UAV-assistant A2G communication system is investigated, where multiple UAVs form a UVAA to perform CB for communicating with remote BSs. Then, we formulate a UCBMOP, aiming at simultaneously maximizing the transmission rate of UVAA and minimizing the energy consumption of all UAVs. Consider that the system is dynamic and the cooperation among UAVs is complex, we propose the HATRPO-UCB, which is an MADRL algorithm to address the problem. Except for combining conventional HATRPO, three techniques are proposed to enhance the performance of the proposed algorithm. Simulation results demonstrate that the proposed HATRPO-UCB learns the better strategy than other baseline methods including LAA, RAA, MADDPG, IPPO, MAPPO and conventional HA-TRPO, making UVAA achieve the best transmission performance and save the energy consumption simultaneously. Furthermore, the effectiveness of three techniques is also verified by the ablation experiments.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 11. Energy consumption of the UAVs for the synchronization process. (a) Closed loop. (b) Open loop. These synchronization methods need no more than one hundred times generation to complete synchronization tasks. As can be seen, the energy consumption of each generation is very small and can be ignored.

## REFERENCES

[1] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, 2019.

[2] N. Zhao, W. Lu, M. Sheng, Y. Chen, J. Tang, F. R. Yu, and K.- K. Wong, âUAV-assisted emergency networks in disasters,â IEEE Wirel. Commun., vol. 26, no. 1, pp. 45â51, 2019.

[3] S. Chen, J. Zhang, E. Bjornson, J. Zhang, and B. Ai, âStructured massive access for scalable cell-free massive MIMO systems,â IEEE J. Sel. Areas Commun., vol. 39, pp. 1086â1100, Apr. 2021.

[4] S. Ahmed, M. Z. Chowdhury, and Y. M. Jang, âEnergy-efficient uav relaying communications to serve ground nodes,â IEEE Commun. Lett., vol. 24, no. 4, pp. 849â852, 2020.

[5] M. Khosravi and H. Pishro-Nik, âUnmanned aerial vehicles for package delivery and network coverage,â in Proc. VTC2020-Spring, pp. 1â5, IEEE, 2020.

[6] Y. Zeng, R. Zhang, and T. J. Lim, âWireless communications with unmanned aerial vehicles: Opportunities and challenges,â IEEE Commun. Mag., vol. 54, no. 5, pp. 36â42, 2016.

[7] M. Li, L. Liu, Y. Gu, Y. Ding, and L. Wang, âMinimizing energy consumption in wireless rechargeable UAV networks,â IEEE Internet Things J., vol. 9, no. 5, pp. 3522â3532, 2021.

[8] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, 2019.

[9] C. Zhan and Y. Zeng, âEnergy minimization for cellular-connected uav: From optimization to deep reinforcement learning,â IEEE Trans. Wireless Commun., 2022.

[10] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surv. Tutorials, vol. 21, no. 3, pp. 2334â2360, 2019.

[11] S. Liang, Z. Fang, G. Sun, Y. Liu, G. Qu, S. Jayaprakasam, and Y. Zhang, âA joint optimization approach for distributed collaborative beamforming in mobile wireless sensor networks,â Ad Hoc Netw., vol. 106, p. 102216, 2020.

[12] J. Garza, M. A. Panduro, A. Reyna, G. Romero, and C. d. Rio, âDesign of UAVs-based 3D antenna arrays for a maximum performance in terms of directivity and SLL,â Int. J. Antenn. Propag., vol. 2016, 2016.

[13] S. Fujimoto, H. Hoof, and D. Meger, âAddressing function approximation error in actor-critic methods,â in Proc. ICML, pp. 1587â 1596, PMLR, 2018.

[14] Y. Wang, Z. Gao, J. Zhang, X. Cao, D. Zheng, Y. Gao, D. W. K. Ng, and M. Di Renzo, âTrajectory design for UAV-based internet of things data collection: A deep reinforcement learning approach,â IEEE Internet Things J., vol. 9, no. 5, pp. 3899â3912, 2021.

[15] H. Xie, D. Yang, L. Xiao, and J. Lyu, âConnectivity-aware 3D UAV path design with deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 70, no. 12, pp. 13022â13034, 2021.

[16] J. G. Kuba, R. Chen, M. Wen, Y. Wen, F. Sun, J. Wang, and Y. Yang, âTrust region policy optimisation in multi-agent reinforcement learning,â arXiv preprint arXiv:2109.11251, 2021.

[17] Y. Cai, Z. Wei, R. Li, D. W. K. Ng, and J. Yuan, âJoint trajectory and resource allocation design for energy-efficient secure uav communication systems,â IEEE Trans. Commun., vol. 68, no. 7, pp. 4536â4553, 2020.

[18] M. Wang, L. Zhang, P. Gao, X. Yang, K. Wang, and K. Yang, âStackelberg game-based intelligent offloading incentive mechanism for a multi-UAV-assisted mobile edge computing system,â IEEE Internet Things J., 2023.

[19] S. F. Abedin, M. S. Munir, N. H. Tran, Z. Han, and C. S. Hong, âData freshness and energy-efficient UAV navigation optimization: A deep reinforcement learning approach,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 9, pp. 5994â6006, 2020.

[20] C. H. Liu, X. Ma, X. Gao, and J. Tang, âDistributed energy-efficient multi-uav navigation for long-term communication coverage by deep reinforcement learning,â IEEE Trans. Mob. Comput., vol. 19, no. 6, pp. 1274â1285, 2019.

[21] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âCommunications and control for wireless drone-based antenna array,â IEEE Trans. Commun., vol. 67, no. 1, pp. 820â834, 2018.

[22] G. Sun, J. Li, Y. Liu, S. Liang, and H. Kang, âTime and energy minimization communications based on collaborative beamforming for UAV networks: A multi-objective optimization method,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3555â3572, 2021.

[23] G. Sun, J. Li, A. Wang, Q. Wu, Z. Sun, and Y. Liu, âSecure and energy-efficient UAV relay communications exploiting collaborative beamforming,â IEEE Trans. Commun., vol. 70, no. 8, pp. 5401â 5416, 2022.

[24] G. Sun, X. Zheng, Z. Sun, Q. Wu, J. Li, Y. Liu, and V. C. Leung, âUAV-enabled secure communications via collaborative beamforming with imperfect eavesdropper information,â IEEE Trans. Mob. Comput., vol. 23, no. 4, pp. 3291â3308, 2024.

[25] J. Li, G. Sun, L. Duan, and Q. Wu, âMulti-objective optimization for UAV swarm-assisted iot with virtual antenna arrays,â IEEE Trans. Mob. Comput., pp. 1â18, 2024.

[26] J. Huang, A. Wang, G. Sun, and J. Li, âJamming-aided maritime physical layer encrypted dual-UAVs communications exploiting collaborative beamforming,â in Proc. CSCWD, IEEE, 2023.

[27] H. Li, D. Wei, G. Sun, J. Wang, J. Li, and H. Kang, âInterference mitigation via collaborative beamforming in UAV-enabled data collections: A multi-objective optimization method,â 2022.

[28] S. Krishna Moorthy, N. Mastronarde, S. Pudlewski, E. S. Bentley, and Z. Guan, âSwarm UAV networking with collaborative beamforming and automated ESN learning in the presence of unknown blockages,â Comput. Netw., vol. 231, p. 109804, 2023.

[29] Y. Zhang, Z. Mou, F. Gao, J. Jiang, R. Ding, and Z. Han, âUAVenabled secure communications by multi-agent deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 11599â 11611, 2020.

[30] C. Dai, K. Zhu, and E. Hossain, âMulti-agent deep reinforcement learning for joint decoupled user association and trajectory design in full-duplex multi-UAV networks,â IEEE Trans. Mob. Comput., 2022.

[31] S. Jayaprakasam, S. K. A. Rahim, and C. Y. Leow, âDistributed and collaborative beamforming in wireless sensor networks: Classifications, trends, and research directions,â IEEE Commun. Surv. Tutorials, vol. 19, no. 4, pp. 2092â2116, 2017.

[32] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal lap altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, 2014.

[33] G. Sun, Y. Liu, Z. Chen, A. Wang, Y. Zhang, D. Tian, and V. C. M. Leung, âEnergy efficient collaborative beamforming for reducing sidelobe in wireless sensor networks,â IEEE Trans. Mob. Comput., vol. 20, no. 3, pp. 965â982, 2021.

[34] S. Jayaprakasam, S. K. Abdul Rahim, C. Y. Leow, and T. O. Ting, âSidelobe reduction and capacity improvement of open-loop collaborative beamforming in wireless sensor networks,â PloS one, vol. 12, no. 5, p. e0175510, 2017.

[35] Y. Zeng, X. Xu, and R. Zhang, âTrajectory design for completion time minimization in UAV-enabled multicasting,â IEEE Trans. Wireless Commun., vol. 17, no. 4, pp. 2233â2246, 2018.

[36] S.-F. Chou, A.-C. Pang, and Y.-J. Yu, âEnergy-aware 3D unmanned aerial vehicle deployment for network throughput optimization,â IEEE Trans. Wireless Commun., vol. 19, no. 1, pp. 563â578, 2019.

[37] Z. Yang, W. Xu, and M. Shikh-Bahaei, âEnergy efficient UAV communication with energy harvesting,â IEEE Trans. Veh. Technol., vol. 69, no. 2, pp. 1913â1927, 2019.

[38] C. You and R. Zhang, âHybrid offline-online design for UAVenabled data harvesting in probabilistic LoS channels,â IEEE Trans. Wireless Commun., vol. 19, no. 6, pp. 3753â3768, 2020.

[39] P. Goos, U. Syafitri, B. Sartono, and A. Vazquez, âA nonlinear multidimensional knapsack problem in the optimal design of mixture experiments,â Eur. J. Oper. Res., vol. 281, no. 1, pp. 201â 221, 2020.

[40] A. Feriani and E. Hossain, âSingle and multi-agent deep reinforcement learning for ai-enabled wireless networks: A tutorial,â IEEE Commun. Surv. Tutorials, vol. 23, no. 2, pp. 1226â1252, 2021.

[41] M. L. Littman, âMarkov games as a framework for multi-agent reinforcement learning,â in Machine learning proceedings 1994, pp. 157â163, Elsevier, 1994.

[42] C. Yu, A. Velu, E. Vinitsky, Y. Wang, A. Bayen, and Y. Wu, âThe surprising effectiveness of ppo in cooperative, multi-agent games,â arXiv preprint arXiv:2103.01955, 2021.

[43] D. Salama, T. K. Sarkar, M. N. Abdallah, X. Yang, and M. Salazar-Palma, âAdaptive processing at multiple frequencies using the same antenna array consisting of dissimilar nonuniformly spaced elements over an imperfectly conducting ground,â IEEE Trans. Antennas Propag., vol. 67, pp. 622â625, Jan. 2019.

[44] C. S. de Witt, B. Peng, P.-A. Kamienny, P. Torr, W. Bohmer, Â¨ and S. Whiteson, âDeep multi-agent reinforcement learning for decentralized continuous cooperative control,â arXiv preprint arXiv:2003.06709, 2020.

[45] M. Samvelyan, T. Rashid, C. S. De Witt, G. Farquhar, N. Nardelli, T. G. Rudner, C.-M. Hung, P. H. Torr, J. Foerster, and S. Whiteson, âThe starcraft multi-agent challenge,â arXiv preprint arXiv:1902.04043, 2019.

[46] S. Kakade and J. Langford, âApproximately optimal approximate reinforcement learning,â in Proc. of ICML, p. 267â274, 2002.

[47] J. Schulman, S. Levine, P. Abbeel, M. Jordan, and P. Moritz, âTrust region policy optimization,â in Proc. ICML, pp. 1889â1897, 2015.

[48] P.-W. Chou, D. Maturana, and S. Scherer, âImproving stochastic policy gradients in continuous control with deep reinforcement learning using the beta distribution,â in Proc. ICML, pp. 834â843, 2017.

[49] W. Zhou, Z. Cao, N. Deng, K. Jiang, and D. Yang, âIdentify, estimate and bound the uncertainty of reinforcement learning for autonomous driving,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 8, pp. 7932â7942, 2023.

[50] K. Zhang, Z. Yang, and T. BasÂ¸ar, Multi-Agent Reinforcement Learning: A Selective Overview of Theories and Algorithms, pp. 321â384. Springer International Publishing, 2021.

[51] T. Li, K. Zhu, N. C. Luong, D. Niyato, Q. Wu, Y. Zhang, and B. Chen, âApplications of multi-agent reinforcement learning in future internet: A comprehensive survey,â IEEE Commun. Surv. Tutorials, vol. 24, no. 2, pp. 1240â1279, 2022.

[52] J. Li, H. Kang, G. Sun, S. Liang, Y. Liu, and Y. Zhang, âPhysical layer secure communications based on collaborative beamforming for UAV networks: A multi-objective optimization approach,â in Proc. IEEE INFOCOM 2021, pp. 1â10, IEEE, 2021.

[53] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âWireless communication using unmanned aerial vehicles (UAVs): Optimal transport theory for hover time optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 12, pp. 8052â8066, 2017.

[54] D. P. Kingma and J. Ba, âAdam: A method for stochastic optimization,â arXiv preprint arXiv:1412.6980, 2014.

[55] R. Lowe, Y. I. Wu, A. Tamar, J. Harb, O. Pieter Abbeel, and I. Mordatch, âMulti-agent actor-critic for mixed cooperative-competitive environments,â Advances in neural information processing systems, vol. 30, 2017.

[56] C. S. de Witt, T. Gupta, D. Makoviichuk, V. Makoviychuk, P. H. Torr, M. Sun, and S. Whiteson, âIs independent learning all you need in the starcraft multi-agent challenge?,â arXiv preprint arXiv:2011.09533, 2020.

[57] L. Bottou et al., âStochastic gradient learning in neural networks,â Proceedings of Neuro-NÄ±mes, vol. 91, no. 8, p. 12, 1991.

[58] J. Duchi, E. Hazan, and Y. Singer, âAdaptive subgradient methods for online learning and stochastic optimization.,â Journal of machine learning research, vol. 12, no. 7, 2011.

[59] T. Tieleman, G. Hinton, et al., âLecture 6.5-rmsprop: Divide the gradient by a running average of its recent magnitude,â COURS-ERA: Neural networks for machine learning, vol. 4, no. 2, pp. 26â31, 2012.

[60] A. Minturn, D. Vernekar, Y. L. Yang, and H. Sharif, âDistributed beamforming with imperfect phase synchronization for cognitive radio networks,â in Proc. ICC, pp. 4936â4940, IEEE, 2013.

[61] Y. S. Shmaliy, âVon mises/tikhonov-based distributions for systems with differential phase measurement,â Signal Process., vol. 85, no. 4, pp. 693â703, 2005.

[62] Y. Zeng, Y. Hu, S. Liu, J. Ye, Y. Han, X. Li, and N. Sun, âRt3d: Realtime 3-d vehicle detection in lidar point cloud for autonomous driving,â IEEE Robot. Autom. Lett., vol. 3, no. 4, pp. 3434â3440, 2018.

[63] I. Thibault, G. E. Corazza, and L. Deambrogio, âRandom, deterministic, and hybrid algorithms for distributed beamforming,â in 2010 5th Advanced Satellite Multimedia Systems Conference and the 11th Signal Processing for Space Communications Workshop, IEEE, 2010.

[64] J. Feng, Y.-H. Lu, B. Jung, and D. Peroulis, âEnergy efficient collaborative beamforming in wireless sensor networks,â in 2009 IEEE International Symposium on Circuits and Systems, IEEE, May 2009.

[65] F. Quitin, M. M. Ur Rahman, R. Mudumbai, and U. Madhow, âDistributed beamforming with software-defined radios: Frequency synchronization and digital feedback,â in Proc. IEEE GLOBECOM, 2012.

<!-- image-->  
Saichao Liu received a BS degree and an MS degree in Software Engineering from Henan University, China, in 2019 and 2022, respectively. He is currently pursuing the Ph.D. degree with the College of Computer Science and Technology, Jilin University, Changchun, China. His research interests include wireless communications, UAV networks, antenna arrays and reinforcement learning.

<!-- image-->

Geng Sun (Sâ17-Mâ19) received the B.S. degree in communication engineering from Dalian Polytechnic University, and the Ph.D. degree in computer science and technology from Jilin University, in 2011 and 2018, respectively. He was a Visiting Researcher with the School of Electrical and Computer Engineering, Georgia Institute of Technology, USA. He is an Associate Professor in College of Computer Science and Technology at Jilin University, and His research interests include wireless networks, UAV communications, collaborative beamforming and optimizations.

<!-- image-->

Shuang Liang received the B.S. degree in Communication Engineering from Dalian Polytechnic University, China in 2011, the M.S. degree in Software Engineering from Jilin University, China in 2017, and the Ph.D. degree in Computer Science from Jilin University, China in 2022. She is a post-doctoral in the School of Information Science and Technology, Northeast Normal University, and her research interests focus on wireless communication and UAV networks.

Qingqing Wu (Sâ13-Mâ16-SMâ21) received the B.Eng. and the Ph.D. degrees in Electronic Engineering from South China University of Technology and Shanghai Jiao Tong University (SJTU) in 2012 and 2016, respectively. From 2016 to 2020, he was a Research Fellow in the Department of Electrical and Computer Engineering at National University of Singapore. He is currently an Associate Professor with Shanghai Jiao Tong University. His current research interest includes intelligent reflecting surface (IRS), unmanned aerial vehicle (UAV) communications, and MIMO transceiver design. He has coauthored more than 100 IEEE journal papers with 26 ESI highly cited papers and 8 ESI hot papers, which have received more than 18,000 Google citations. He was listed as the Clarivate ESI Highly Cited Researcher in 2022 and 2021, the Most Influential Scholar Award in AI-2000 by Aminer in 2021 and Worldâs Top 2% Scientist by Stanford University in 2020 and 2021.

<!-- image-->

<!-- image-->

<!-- image-->

Pengfei Wang (Member, IEEE) received the B.S., M.S., and Ph.D. degrees in software engineering from Northeastern University (NEU), China, in 2013, 2015, and 2020, respectively. From 2016 to 2018, he was a Visiting Ph.D. Student with the Department of Electrical Engineering and Computer Science, Northwestern University, IL, USA. He is currently an Associate Professor with the School of Computer Science and Technology, Dalian University of Technology (DUT), China. He has authored more than 30

papers on high-quality journals and conferences, such as IEEE/ACM TRANSACTIONS ON NETWORKING, IEEE INFOCOM, IEEE TRANS-ACTIONS ON INTELLIGENT TRANSPORTATION SYSTEMS, DAC, IEEE ICNP, IEEE ICDCS, IEEE INTERNET OF THINGS JOURNAL, and JSA. He also holds a series of patents in U.S. and China. His research interests are ubiquitous computing, big data, and AIoT.

Jiahui Li (Sâ21) received a BS degree in Software Engineering, and an MS degree in Computer Science and Technology from Jilin University, Changchun, China, in 2018 and 2021, respectively. He is currently studying Computer Science at Jilin University to get a Ph.D. degree, and also a visiting Ph. D. at Singapore University of Technology and Design (SUTD), Singapore. His current research focuses on UAV networks, antenna arrays, and optimization.

<!-- image-->

Dusit Niyato (Fellow, IEEE) received the B.Eng. degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand, in 1999, and the Ph.D. degree in electrical and computer engineering from the University of Manitoba, Canada, in 2008. He is currently a Professor with the School of Computer Science and Engineering, Nanyang Technological University, Singapore. His research interests include the Internet of Things (IoT), machine learning, and incentive mechanism design.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_9_img_1.png|page_9_img_1]]
3. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_1.png|page_14_img_1]]
4. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_2.png|page_14_img_2]]
5. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_3.png|page_14_img_3]]
6. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_4.png|page_14_img_4]]
7. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_5.png|page_14_img_5]]
8. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_6.png|page_14_img_6]]
9. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_7.png|page_14_img_7]]
10. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_8.png|page_14_img_8]]
11. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_9.png|page_14_img_9]]
12. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_10.png|page_14_img_10]]
13. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_11.png|page_14_img_11]]
14. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_12.png|page_14_img_12]]
15. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_13.png|page_14_img_13]]
16. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_14.png|page_14_img_14]]
17. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_15.png|page_14_img_15]]
18. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_16.png|page_14_img_16]]
19. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_17.png|page_14_img_17]]
20. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_18.png|page_14_img_18]]
21. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_19.png|page_14_img_19]]
22. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_20.png|page_14_img_20]]
23. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_21.png|page_14_img_21]]
24. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_22.png|page_14_img_22]]
25. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_23.png|page_14_img_23]]
26. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_24.png|page_14_img_24]]
27. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_25.png|page_14_img_25]]
28. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_26.png|page_14_img_26]]
29. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_27.png|page_14_img_27]]
30. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_28.png|page_14_img_28]]
31. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_29.png|page_14_img_29]]
32. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_30.png|page_14_img_30]]
33. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_31.png|page_14_img_31]]
34. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_32.png|page_14_img_32]]
35. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_33.png|page_14_img_33]]
36. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_34.png|page_14_img_34]]
37. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_35.png|page_14_img_35]]
38. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_36.png|page_14_img_36]]
39. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_37.png|page_14_img_37]]
40. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_38.png|page_14_img_38]]
41. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_39.png|page_14_img_39]]
42. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_40.png|page_14_img_40]]
43. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_41.png|page_14_img_41]]
44. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_42.png|page_14_img_42]]
45. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_43.png|page_14_img_43]]
46. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_44.png|page_14_img_44]]
47. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_45.png|page_14_img_45]]
48. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_46.png|page_14_img_46]]
49. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_47.png|page_14_img_47]]
50. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_48.png|page_14_img_48]]
51. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_49.png|page_14_img_49]]
52. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_14_img_50.png|page_14_img_50]]
53. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_18_img_1.jpeg|page_18_img_1]]
54. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_18_img_2.jpeg|page_18_img_2]]
55. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_18_img_3.jpeg|page_18_img_3]]
56. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_18_img_4.jpeg|page_18_img_4]]
57. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_18_img_5.jpeg|page_18_img_5]]
58. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_18_img_6.jpeg|page_18_img_6]]
59. [[../extracted_images/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning/page_18_img_7.jpeg|page_18_img_7]]

---

