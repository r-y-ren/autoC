# Reliability-Optimal UAV-Assisted Mobile Edge Computing: Joint Resource Allocation, Data Transmission Scheduling and Motion Control

Jianshan Zhou , Mingqian Wang, Daxin Tian , Fellow, IEEE, Kaige Qu , Member, IEEE, Guixian Qu , Xuting Duan , and Xuemin Shen , Fellow, IEEE

AbstractâUncrewed aerial vehicles (UAVs) play a crucial role in mobile edge computing (MEC) within space-air-ground integrated networks. They serve as aerial cloudlets, enabling task processing in close proximity to ground users. While numerous joint trajectory design and resource allocation schemes aim to enhance energy efficiency or computation rate, few focus on improving system reliability, which is often challenged by stochastic channels and node mobility. This paper presents a stochastic modeling perspective to derive a system reliability expression. Our reliability formulation incorporates the impacts of stochastic Line-of-Sight (LoS) and Non-Line-of-Sight (NLoS) air-to-ground communication channels, application data load, available bandwidth, offloading time, and transmission power. This comprehensive approach leads to a reliability-oriented joint optimization model that considers not only resource allocation and user data transmission scheduling but also the motion of UAVs. To solve this problem, we propose a low-complexity algorithm. By utilizing augmented Lagrangian multipliers, the algorithm transforms nonlinear constraints into a tractable formulation, enabling the utilization of legacy unconstrained optimization techniques. We provide a proof of convergence for this algorithm. Through simulations, we demonstrate that our proposed method guarantees convergence within finite iterations and improves the average communication reliability in comparison with several other joint optimization schemes.

Index TermsâUncrewed aerial vehicle, mobile edge computing, reliability optimization, motion control, resource allocation.

## I. INTRODUCTION

U NCREWED aerial vehicles (UAVs) are widely recognizedas an essential component in numerous Internet-of-Things (IoT) applications and envisioned information architectures, including space-air-ground integrated networks, aerial-ground cooperative vehicular networks, and mobile edge-computing (MEC) systems. Due to their highly flexible deployment, UAVs can significantly extend the coverage of conventional terrestrial networks, creating positive social impacts and business opportunities for the future. By integrating UAVs with terrestrial networks, it is possible to transform traditional information communication systems into a new paradigm that meets the emerging requirements of mission-critical services such as enhanced mobile broadband (eMBB), massive machine-type communications (mMTC), and ultra-reliable and low-latency communications (URLLC) in 5G and Beyond [1]. In particular, addressing the challenges that arise in the context of UAV-based air-to-ground (A2G) communication networks is crucial for the practical realization of URLLC requirements. These challenges include intermittent connectivity, stochastic A2G channel fading, and concurrent physical-layer interference [2], [3]. The challenges arise from multiple coupled effects, including the high mobility of UAVs, probabilistic path-loss switching between Line-of-Sight (LoS) and Non-Line-of-Sight (NLoS) propagation links, stochastic multi-user channel contention, and stringent resource constraints imposed by the physical limitations of UAVs [4], [5]. To improve the performance of UAVassisted communication networks, extensive research efforts have been dedicated to various joint optimization paradigms. Most recent studies have focused on optimizing various system goals, including resource utilization [6], energy efficiency [7], [8], [9], time efficiency [10], [11], [12], [13], [14], [15], [16], energy consumption [17], [18], [19], [20], [21], [22], [23], network throughput and sum transmission rate [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], and aggregate cost [34], [35], [36]. However, there is a lack of research on developing reliability-oriented modeling and optimization methodologies for UAV-assisted MEC systems.

Communication reliability is an essential metric for UAVassisted networks, which depends on the mobility of nodes, A2G channel quality, and transmission demands of upperlayer applications. Specifically, during task execution, the transmission links between a UAV and ground users often experience different fading effects [3]. When the UAV operates in a low-altitude and densely built-up urban environment, where there are no dominant LoS propagation paths, the A2G radio signal can be scattered by various objects, resulting in NLoS channel fading that typically follows a Rayleigh distribution. On the other hand, A2G transmission links may also encounter LoS channels due to the UAVâs mobility. In situations where at least one dominant propagation path exists between the UAV and ground users, the A2G channel fading follows a Rician distribution. Consequently, the A2G channel between the UAV and a ground user can randomly exhibit either Rayleigh or Rician fading as the UAVâs position changes over time. Characterizing communication reliability becomes challenging in the presence of time-varying channel fading behaviors, and deterministic modeling approaches are insufficient for this purpose [2]. Furthermore, from the userâs perspective, resource allocation, including bandwidth and time allocation among users, also affects the capacity of the A2G link. The UAV needs to allocate appropriate bandwidth and computation offloading time for each ground user based on their task load in upper-layer applications [31]. Considering the limited energy capacity of the UAV, it is crucial to adhere to energy consumption constraints associated with both motion and communication while effectively allocating transmission power. These factors contribute to the challenge of providing reliability guarantees for UAV-assisted networks.

This paper proposes a stochastic model to capture the reliability of A2G communication from a probabilistic perspective, taking into account both LoS and NLoS channels between a UAV and ground users. Existing studies that follow a deterministic modeling approach focus exclusively on the Rayleigh fading effect for LoS channels or the Rician fading effect for NLoS channels, thereby neglecting the possibility that the fading behavior of some A2G links may transit from one type to the other during UAV flight. By contrast, we characterize the probability of an A2G channel experiencing Rayleigh and Rician fading by incorporating relative azimuth angle, relative distance, and other location-dependent geometrical measures between the UAV and ground users. Additionally, we consider factors such as the number of data bits to be served in each time interval, transmission power and bandwidth allocation among users, and usersâ local computation time allocation. By combining decision-making factors related to application data bit allocation and resource allocation (i.e., power, bandwidth, and time) with a location-dependent probabilistic modeling approach, we are able to effectively characterize the reliability of the UAV-assisted MEC system. To maximize system reliability, we propose a reliability-oriented joint optimization model that encompasses the scheduling of data bits, allocation of transmission power and bandwidth, local computation time allocation, and control of UAV motion. The main contributions of this paper can be summarized as follows:

i) We derive a closed-form expression that characterizes the system reliability by quantifying the probability of successfully offloading data bits from ground users to a UAV acting as an aerial edge server within a given deadline. Our stochastic modeling incorporates the probability conditioned on both LoS and NLoS fading channels, while considering load and resource allocation for A2G transmission links.

ii) We formulate a joint optimization model that maximizes system reliability under both LoS and NLoS fading channels. This model allows for the joint optimization of the UAVâs acceleration, transmission power, bandwidth allocation, data offloading, and time allocation. Additionally, the model integrates a set of physical constraints, including UAV kinematic constraints, resource restrictions, and data volume limitations, to ensure the feasibility of UAV motion and energy self-sufficiency while preserving the integrity of upper-layer applications.

iii) To solve the model, we propose an iterative optimization algorithm with polynomial time complexity. This algorithm equivalently transforms the multi-variable constrained optimization problem into a sequence of unconstrained problems, making it mathematically tractable and efficiently solvable. The algorithm also enables the utilization of legacy unconstrained optimization techniques.

iv) We validate the effectiveness of the joint optimization method through simulations. Comparative performance analysis against state-of-the-art methods demonstrates that our proposed approach achieves the highest system reliability for the UAV-assisted MEC system, even in the presence of stochastic fading channels.

We summarize the remainder of the paper as follows. In the next section, we provide a detailed review of the related literature. In Section III, we formulate the kinematics, communication, and edge computing models for the target system and describe the problem. In Section IV, we propose a joint optimization method. In Section V, we conduct simulations to compare the performance and present the results. Finally, in Section VI, we provide concluding remarks.

## II. RELATED WORK

UAVs have recently proven successful in many application scenarios due to their high flexibility. The field of UAV-assisted communication and MEC has experienced rapid growth in activity in recent years, with numerous studies making great efforts to develop various optimization solutions to improve UAV-assisted networks or MEC systems. Different optimization goals have led to a wide variety of system designs and solutions. We categorize related works and provide a comprehensive review of each class of studies as follows.

Energy Consumption Minimization: [18] combines an encoding mechanism with a dandelion algorithm to jointly optimize the UAVâs deployment and trajectory. Their essential goal is to minimize the energy consumption of a UAV-assisted Internet-of-Things (IoT) system during data collection. In [19], block coordinate descent and deep reinforcement learning-based algorithms are proposed to optimize multiple UAVsâ trajectories and resource allocation while making user association decisions. They aim to minimize all usersâ energy consumption when performing computation offloading. In [20], the system goal is to minimize the energy consumption of both UAVs and ground users. To achieve this goal, the researchers formulate the energy consumption minimization problem as a mixed-integer programming model and use a block successive upper-bound minimization algorithm to obtain a near-optimal solution. In [21], the researchers propose a distributed optimization algorithm based on fractional programming and primal-dual optimization techniques, which can reduce the whole energy consumption of flying ad hoc networks considering nodes with multi-packet reception capability. In [22], a decomposition approach is presented to handle the energy consumption minimization problem in UAV-assisted networks. They develop a gradient projectionbased iterative algorithm to jointly optimize the UAVâs longitudinal acceleration and transmission power to minimize the UAVâs total energy consumption. In [23], the researchers treat UAVs as wireless power charging stations and formulate a network cost function that is minimized using a backward induction optimization technique. In summary, the aforementioned works demonstrate impressive performance in minimizing the energy consumption of UAV-assisted networks. However, they primarily focus on either LoS channels or NLoS channels when modeling UAV-assisted A2G communications. Few solutions for energy consumption minimization consider the stochastic characteristics of A2G linksâ state transition between LoS and NLoS propagation and the impact of coexisting LoS and NLoS propagation.

Energy-Efficiency Optimization: Resource allocation and power control are popular techniques to enhance the energy efficiency of UAV-assisted networks. Advanced optimization and game-theoretical methods such as the Lagrange multiplier method, successive convex approximation (SCA), block coordinate descent (BCD), evolutionary game theory, mean-field game theory, and their variants have been extensively employed to address energy-efficiency optimization problems. In [6], a cost function for UAV-base stations is designed based on quality of service (QoS) and energy consumption. The authors propose a hierarchical mean-field game framework to adapt UAVsâ transmission power and channel access. Similarly, [7] decomposes the energy-efficiency optimization problem in UAV-assisted non-orthogonal multiple access (NOMA) networks into three sub-problems and presents an alternating algorithm to jointly optimize transmission power, communication scheduling, and UAVsâ motion parameters. In the context of intelligent reflecting surface (IRS)-assisted UAV communication systems, [8] formulates the energy-efficiency optimization problem as a Markov decision process (MDP) and develops a deep deterministic policy gradient (DDPG) algorithm to optimize the UAVâs trajectory and the IRS phase shifts. Another study in [9] also employs the Markov decision process methodology and proposes proximal policy optimization (PPO) to obtain a near-optimal UAV trajectory while optimizing content caching decisions and radio resource allocation. In the cited literature above, the energy efficiency metric is commonly defined as the ratio of network-wide throughput or system capacity to total energy consumption, with the aim of increasing the number of transmitted bits per unit of energy consumed. However, these studies primarily model

LoS channels while neglecting the probabilistic effects of NLoS propagation. Existing energy-efficiency optimization methods do not account for the stochastic state transition between LoS and NLoS channels in their system models.

Time-Oriented Optimization: The optimization of a UAVâs flight duration or transmission time is another crucial performance metric. In [11], researchers propose a method that combines clustering and trajectory planning for UAVs with the goal of minimizing flight time and enhancing data collection efficiency. Similarly, [10] formulates a conditional auction game model and designs a group-buying coalition auction scheme to improve UAVsâ data collection efficiency, yielding a significant reduction in the average age of information (AoI) of sensors. To reduce a UAVâs energy consumption and task completion time, [12] formulates a mixed-integer optimization model and employs a combination of the BCD and SCA algorithms to solve the problem. In [13], researchers aim to minimize content acquisition delay for ground users and propose a PPO-based deep reinforcement learning method to jointly optimize usersâ association, cache placement, UAVâs trajectory, and transmission power. Several other studies have developed fractional programming algorithms [14] and heuristic algorithms [15], [16] to address the problem of minimizing UAV-assisted transmission time. In the aforementioned studies, researchers widely adopt a deterministic modeling approach. They typically model transmission time or end-to-end latency without considering the probabilistic state transition of the A2G communication links. Consequently, the optimization methods presented may be less efficient or may fail when UAVs encounter various fading paths.

Sum Rate Maximization: In [17], researchers developed a UAV-enabled multi-hop routing framework to facilitate collaborative fog computing. They integrated a UAV selection algorithm with Benders decomposition and SCA techniques to maximize the system throughput utility. In [24], BCD and SCA techniques were employed to solve a non-convex sum rate maximization model, providing an optimal UAV trajectory and resource allocation solution. In contrast, [25] aims to maximize the sum of computation bits. The researchers introduced an alternative optimization algorithm to jointly adjust user association and UAV trajectories, optimizing CPU frequencies, transmission power, and offloading time of UAVs and ground users simultaneously [25]. [26] focuses on a UAV-assisted covert communication scenario with guaranteed privacy and establishes a probability model for Willieâs minimum detection error. In their target relaying network, they developed an SCA algorithm incorporating penalties on detection errors to maximize the minimum average covert transmission rate. A similar SCA technique is also employed to enhance the throughput of multi-UAV-assisted connected vehicles [28]. The basic idea is to decompose the primal problem into several sub-problems, including UAV communication scheduling, power allocation, and trajectory optimization [28]. Building on the SCA technique, many other works have developed various joint optimization solutions to enhance the sum rate of UAV-assisted systems, such as joint communication and computing resource scheduling solutions [31], joint power and trajectory design solutions [32], and joint placement and resource allocation solutions [33].

In [27], researchers combined a channel allocation algorithm with a data delivery scheme to maximize the overall throughput of a UAV-assisted post-disaster network. In [29], researchers developed a multi-agent deep reinforcement learning (MADRL) solution based on the PPO algorithm, aiming to maximize usersâ sum rates by jointly making decisions on downlink and uplink association of a multi-tier UAV communication network and optimizing UAV trajectories. Using a similar MADRL approach, [30] maximizes usersâ sum rates by enabling ratesplitting multiple access (RSMA) in UAV-assisted networks. In the aforementioned literature, numerous studies have focused on developing solutions to maximize either the sum transmission or computation rates, as these rates significantly influence the overall service capacity of UAV-assisted systems. However, few efforts have incorporated the stochastic nature of A2G fading channels into system modeling and optimization. The exploration of stochastic modeling and optimization to ensure computation offloading reliability in UAV-assisted networks is an area that remains largely unexplored.

Aggregate Cost Minimization: To minimize system costs, advanced heuristic optimization algorithms, such as differential evolution algorithms, have been integrated with legacy optimization techniques, including BCD and SCA techniques. This integration facilitates the joint optimization of UAV trajectories, user association, and passive beamforming of IRS components [34]. In addressing the aggregate cost optimization problem, game-theoretical and reinforcement learning approaches have been widely employed. For example, [35] models the joint channel and link selection problem of UAV-assisted networks as a two-way consensus game. The study applies a minimum spanning tree algorithm and a distributed best response algorithm to manage the consensus game, wherein UAVs strive to minimize their aggregate cost. In [36], researchers develop a reinforcement learning-based joint solution to optimize a UAVâs trajectory and jamming power. This approach aims to enhance the capacity of UAV-assisted eavesdropping channels in surveillance scenarios. In the literature above, researchers formulate an aggregate cost function that encompasses various system performance metrics, such as energy consumption, task completion time, and maintenance costs associated with ground nodes or UAVs. Nevertheless, few works jointly optimize UAV acceleration control and resource and data bit allocations.

In UAV-assisted MEC scenarios, ensuring the communication reliability of an air-ground integrated network stands out as a primary objective. This importance arises from the reliance of many emerging autonomous and connected applications, such as real-time environment perception of autonomous vehicles, real-time digital twins for vehicular diagnostics, and online road traffic monitoring, on dependable communication within the network. Reviewing the literature cited above, it becomes evident that existing joint optimization solutions, while successful in addressing UAV trajectory design, resource allocation, communication and computation scheduling, and user association, do not adequately account for reliability-oriented modeling and optimization. Specifically, most current studies employ deterministic modeling approaches to characterize the average transmission rate over LoS or NLoS links, overlooking the potential for A2G links to switch between LoS and NLoS propagation scenarios. In instances where both LoS and NLoS propagation scenarios occur, it becomes crucial to incorporate the probability of each fading case into the modeling of A2G communication reliability. To bridge this gap, we propose a system model from the stochastic modeling perspective, incorporating both LoS and NLoS channel characteristics, which distinguishes our study from the related works above. Unlike the existing literature, we characterize communication reliability by modeling the probability that ground nodes can successfully offload their computation to the UAV given a set of resource and latency constraints. This reliability formulation establishes a connection between node mobility, resource allocation, and data transmission scheduling, thereby leading to the development of a reliability-oriented joint optimization model that considers multi-dimensional decision variables. Furthermore, we propose a convergence-guaranteed and low-complexity optimization algorithm. This algorithm effectively optimizes resource allocation, including bandwidth, offloading time, and transmission power, as well as user data partitioning and UAV motion control.

<!-- image-->  
Fig. 1. A typical UAV-assisted mobile edge computing scenario where ground vehicles offload their application data to the UAV for remote processing using both LoS and NLoS wireless links.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

Consider a UAV-assisted MEC network as demonstrated in Fig. 1. A flying UAV equipped with a computing server can offer edge computing services for ground users, including IoT nodes and connected vehicles. This type of UAV is also known as an aerial cloudlet. It has the ability to flexibly plan its trajectory and control its motion to collect and execute computation tasks from a group of ground users. Let the set of ground users requesting to offload computation tasks to the UAV for remote processing be I, $\mathcal { T } = \{ 1 , 2 , \dots , N \}$ . Without loss of generality, we use = 1 2the well-known Orthogonal Frequency Division Multiplexing (OFDM) technique to enable multiple ground users to access the UAV without interferences simultaneously. Besides, computation offloading and edge computing are operated in a Time Division Multiplexing (TDM) manner. Namely, the continuous time horizon is discretized into a sequence of intervals each with an equal duration of $\Delta t$ seconds. Each time interval is indexed by k, with k $\in \mathbb { Z } _ { \geq 0 }$ . For each time interval k, it is further divided into three stages, including a multi-access computation offloading stage, a computation processing stage, and a result feedback stage. In the offloading stage, N ground users offload their application input data to the UAV. Then, the UAV processes the input data in the computation processing stage. In the result feedback stage, the UAV sends the computation output back to the ground users. In this system, the UAV needs to jointly determine optimal motion control, resource allocation (including the duration of different stages, bandwidth and transmission power), and data transmission scheduling strategies. Here, it is remarked that the size of computation outcome is usually much smaller than that of data to be offloaded for many applications (e.g., the output of an AI-based object classification application is simple indication data, the size of which is much smaller than that of the input data like images and videos). At this point, the time and energy cost for the UAV to transmit the computation output back to the ground users can be neglected as in the recent literature [37], [38], [39], [40], [41].

## A. UAVâs Mobility Model

To characterize the mobility of the flying UAV, we adopt a three-dimensional (3D) euclidean coordinate framework to present the nodeâs geometric position. In the kth time interval, the 3D position of user i $( i \in \mathcal { T } )$ is denoted by $s _ { i } [ k ] =$ $[ x _ { i } [ k ] , y _ { i } [ k ] , \bar { z } _ { i } [ k ] ] ^ { \mathrm { T } }$ , where $x _ { i } [ k ] , \ y _ { i } [ k ]$ and $z _ { i } [ k ]$ represent [ [ ] [ ] [ ]] [ ] [ ] [ ]the longitudinal, the latitudinal, and the altitudinal positions, respectively. The 3D position of the UAV is denoted by $\pmb { \mathscr { s } } [ \bar { k } ] = [ x [ \bar { k } ] , y [ k ] , z [ k ] ] ^ { \bar { \mathrm { T } } }$ . The 3D velocity and the 3D accels[ ] = [ [ ] [ ] [ ]]eration of the UAV in time interval k are denoted by $v [ k ] =$ $[ v _ { x } [ k ] , v _ { y } [ k ] , v _ { z } [ k ] ] ^ { \mathrm { T } }$ and $\mathbf { \boldsymbol { a } } [ k ] = [ a _ { x } [ k ] , a _ { y } [ k ] , a _ { z } [ k ] ] ^ { \mathrm { \scriptscriptstyle T } }$ , respec-[ [ ] [ ] [ ]] a[ ] = [ [ ] [ ] [ ]]tively. Hence, the mobility of the UAV can be described by using a time-discrete double-integral model as follows

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { \pmb { s } [ k + 1 ] = \pmb { s } [ k ] + \Delta t \pmb { v } [ k ] + \frac { ( \Delta t ) ^ { 2 } } { 2 } \pmb { a } [ k ] ; } \\ { \pmb { v } [ k + 1 ] = \pmb { v } [ k ] + \Delta t \pmb { a } [ k ] . } \end{array} \right. } \end{array}\tag{1}
$$

Similar to considerable current literature [37], [38], [39], [40], [41], [42], [43], [44], [45], we consider fixing the height of the flying UAV, i.e., setting $a _ { z } [ k ] = 0 \mathrm { m } / \mathrm { s } ^ { 2 } , v _ { z } [ k ] = 0 \mathrm { m } / \mathrm { s }$ and $z [ k ] = H _ { \mathrm { U A V } }$ for all $k \in \mathbb { Z } _ { \geq 0 } ,$ , such that its motion can be sim-[ ] =plified to the two-dimensional kinematic process. $H _ { \mathrm { U A V } }$ is a prespecified flight height of the $\mathrm { U A V . } ^ { 1 }$ In our work, $\{ \pmb { a } [ k ] , k \in \mathbb { Z } _ { \geq 0 } \}$ a[ ]are treated as the real-time mobility control inputs for the UAV, i.e., decision variables, which remain to be optimized.

Now, let $\begin{array} { r } { \pmb q [ k ] = \mathrm { c o l } \{ \pmb { s } [ k ] , \pmb { v } [ k ] \} } \end{array}$ represent a mobility state of q[ ] = s[ ] v[ ]the UAV in time interval k. We are allowed to rearrange (1) into a state-space form as follows

$$
\begin{array} { r } { \pmb q [ k + 1 ] = \pmb { A } \pmb q [ k ] + \pmb { B } \pmb { a } [ k ] , } \end{array}\tag{2}
$$

where  and  are the coefficient matrices associated with the A Bstate variable and the control variable, respectively, i.e.,

$$
A = \left[ { \begin{array} { c c } { 1 } & { \Delta t } \\ { 0 } & { 1 } \end{array} } \right] \otimes I _ { 3 } , B = \left[ { \begin{array} { c } { { \frac { 1 } { 2 } } \left( \Delta t \right) ^ { 2 } } \\ { \Delta t } \end{array} } \right] \otimes I _ { 3 } .\tag{3}
$$

In (3), â denotes the Kronecker product operator. $\boldsymbol { I } _ { 3 }$ is a $3 \times 3$ identity matrix.

Additionally, the initial position and velocity of the UAV are given as $\begin{array} { r } { \pmb { s } _ { c } = [ x _ { c } , y _ { c } , H _ { \mathrm { U A V } } ] ^ { \mathrm { T } } } \end{array}$ and $\pmb { v } _ { c } = [ v _ { x , c } , v _ { y , c } , 0 ] ^ { \mathrm { T } }$ , res = [ ] v = [ 0]spectively. The terminal position and velocity are specified as $\begin{array} { r } { \pmb { s } _ { f } = [ x _ { f } , y _ { f } , H _ { \mathrm { U A V } } ] ^ { \mathrm { T } } } \end{array}$ and $\boldsymbol { v } _ { f } = [ v _ { x , f } , v _ { y , f } , 0 ] ^ { \mathrm { T } }$ , respectively. s = [ ] v = [ 0]The initial state and the final state can be represented by $\pmb q _ { c } = \mathrm { c o l } \{ s _ { c } , v _ { c } \}$ and $\pmb { q } _ { f } = \mathrm { c o l } \{ \pmb { s } _ { f } , \pmb { v } _ { f } \}$ , respectively. Due to q = s v q = s vthe physical limit, the velocity and the acceleration of the UAV should be bounded within a proper interval. At this point, we let the upper and the lower bounds on the UAVâs velocity be $v _ { \mathrm { m i n } }$ and $v _ { \mathrm { m a x } } .$ v, respectively, and the allowed acceleration bounds be $a _ { \mathrm { m i n } }$ vand $\mathbf { \em a } _ { \mathrm { m a x } } .$ , respectively. We also consider that the UAVâs trajectory is bounded within a finite space. The upper and lower bounds of the position are given as $s _ { \mathrm { m i n } }$ and $s _ { \mathrm { m a x } }$ , respectively. s sHence, the motion control of the UAV needs to satisfy the following state and control constraints

$$
\left\{ \begin{array} { l l } { q [ k ] \in \left[ q _ { \mathrm { m i n } } , { \pmb q } _ { \mathrm { m a x } } \right] ; } \\ { a [ k ] \in \left[ { \pmb a } _ { \mathrm { m i n } } , { \pmb a } _ { \mathrm { m a x } } \right] , } \end{array} \right.\tag{4}
$$

for all $k \in \mathbb { Z } _ { \geq 0 } ,$ , where $\pmb q _ { \mathrm { m i n } } = \mathrm { c o l } \{ s _ { \mathrm { m i n } } , v _ { \mathrm { m i n } } \}$ and $q _ { \mathrm { m a x } } =$ col $\{ s _ { \operatorname* { m a x } } , v _ { \operatorname* { m a x } } \}$

## B. Delay-Constrained Application and Computation Model

For each ground user $i \in \mathcal { T }$ , we use two parameters to characterize their computation tasks, the delay requirement (in the number of time intervals) for a user to offload computation tasks for remote processing, Ti, and the total volume of input data bits (also referred to as the total computation demand), Ci [41], [48], [49], [50]. To facilitate edge computing, each ground user $i \in \mathcal { Z }$ partitions the total input data, $C _ { i }$ , into a sequence of smallersize pieces, i.e., denoted by $\pmb { u } _ { i } = \mathrm { c o l } \{ u _ { i } [ k ] , \bar { k } = 1 , 2 , \ldots , T _ { i } \} .$ Each data piece $u _ { i } [ k ]$ u = [ ] = 1 2should be fully transmitted to the UAV [ ]in the offloading stage of the kth time interval and processed in the computation stage of the kth time interval. The overall data transmission scheduling is required to strictly ensure the integrity of the application data and the application deadline, which can be presented by the following equality and inequality

constraints for all $i \in \mathcal { T }$

$$
\left\{ \begin{array} { l l } { \sum _ { k = 1 } ^ { T _ { i } } u _ { i } [ k ] = C _ { i } ; } \\ { u _ { i } [ k ] \in [ 0 , C _ { i } ] , \ k = 1 , 2 , \dots , T _ { i } . } \end{array} \right.\tag{5}
$$

Utilizing the dynamic voltage and frequency scaling (DVFS) technique, the UAV-mounted cloudlet can dynamically adjust its CPU cycle frequency in the time interval $k ,$ denoted as $f [ k ]$ [ ](in cycles per second), to complete the computation execution within this interval [37], [38], [40]. Let the total mission time horizon of the UAV be $T = \operatorname* { m a x } \{ T _ { i } , i \in \mathcal { I } \}$ . Denote by $\varpi _ { i }$ the = maxnumber of CPU cycles required to process 1-bit input data of user $i \in \mathcal { T }$ . From the UAVâs perspective, the CPU cycle frequency $f [ k ]$ in the kth time interval is given as follows

$$
f [ k ] = \frac { \sum _ { i = 1 } ^ { N } \varpi _ { i } u _ { i } [ k ] } { \kappa [ k ] \Delta t } , \mathrm { ~ } k = 1 , 2 , \dots , T ,\tag{6}
$$

where $\kappa [ k ]$ is the ratio of time allocated for the computation processing stage in time interval k, with $\kappa [ k ] \in ( 0 , 1 )$ . Typically, [ ] (0 1)the CPU-cycle frequency f k should have an upper bound denoted by $f _ { \mathrm { m a x } } , \mathrm { i . e . , } f [ k ] \le f _ { \mathrm { m a x } }$ , which imposes additional [ ]constraints on decision variables $u _ { i } [ k ]$ and $\kappa [ k ]$ as follows

$$
f _ { \operatorname* { m a x } } \kappa [ k ] \Delta t - \sum _ { i = 1 } ^ { N } \varpi _ { i } u _ { i } [ k ] \ge 0 , k = 1 , 2 , \ldots , T .\tag{7}
$$

## C. Channel Model and Communication Reliability

The radio signal propagation heavily affects the wireless communication performance, which is more complicated in the airground integrated network. In many current research works such as [5], [40], [45], [52], [53], [54], [55], [56], [57], a simple assumption that the wireless channel is dominated by the LoS links is commonly adopted. However, when considering the heavily built-up urban environments, i.e., there exist many obstacles scattering the radio signal and no dominant propagation between the UAV and the ground users, the LoS channel assumption may not be feasible. At this point, the communication channel is more likely to be characterized by the NLoS links. Therefore, in our paper, we explicitly take into account the effects of both the LoSand the NLoS-type channels, more specifically, the dynamics of the stochastic transition between the LoS and the NLoS links. Let $\operatorname* { P r } _ { \mathrm { L o S } } ( d _ { i } [ k ] )$ denote the probability that the transmission channel ( [ ])between the UAV and ground user $i \in \mathcal { Z }$ in time interval k is in the LoS propagation state. According to [46], PrL $\phantom { } _ { . 0 5 } ( d _ { i } [ k ] )$ can be evaluated by

$$
\operatorname* { P r } _ { \operatorname { L o S } } \left( d _ { i } [ k ] \right) = \frac { 1 } { 1 + \theta _ { 1 } \exp \left( - \theta _ { 2 } \left( \frac { 1 8 0 } { \pi } \arcsin \left( \frac { z [ k ] } { d _ { i } [ k ] } \right) - \theta _ { 1 } \right) \right) }\tag{8}
$$

for all $i \in \mathcal { T }$ , where $\theta _ { 1 }$ and $\theta _ { 2 }$ are two constants whose settings depend on the flight environment, $d _ { i } [ k ]$ denote the geometric [ ]distance between the UAV and user i in time interval k, i.e.,

$$
\begin{array} { r } { d _ { i } [ k ] = \| \pmb { s } [ k ] - \pmb { s } _ { i } [ k ] \| _ { 2 } , } \end{array}\tag{9}
$$

where $s _ { i } [ k ]$ denotes the position of user i in time interval k. s [ ]It is noted that the positions of the UAV and ground users can be accessed through their onboard Global Positioning System (GPS) modules. The UAV collects the position information of users via a common broadcasting channel (e.g., the dedicated short-range communication channel 178 for control signaling). Following (8), the probability of the NLoS situation is

$$
\operatorname* { P r } _ { \mathrm { N L o S } } \left( { d _ { i } [ k ] } \right) = 1 - \operatorname* { P r } _ { \mathrm { L o S } } \left( { d _ { i } [ k ] } \right) , i \in \mathcal { T } .\tag{10}
$$

To proceed, we investigate the effects of both the LoS and the NLoS propagation channels, respectively, as follows.

1) The LoS Propagation Channel: When computation offloading is performed over the LoS propagation channel, the signal attenuation mainly results from the potential combined effect of the small-scale fading over the LoS link and the multi-path scatterers [5], [58], [59]. In this case, the stochastic channel fading can be well characterized by using a Rician distribution [60]. Thus, letting the power gain of the LoS-type A2G channel be $G _ { \mathrm { L o S } } ,$ , the probability density function (PDF) of $G _ { \mathrm { L o S } }$ can be formulated as [60]

$$
f _ { G _ { \mathrm { L o s } } } ( x ) = \alpha ^ { 2 } \exp \left( - \left( \alpha ^ { 2 } x + K _ { \mathrm { R i c i a n } } \right) \right) I _ { 0 } \left( 2 \alpha \sqrt { K _ { \mathrm { R i c i a n } } x } \right)\tag{11}
$$

for $\forall x \geq 0 .$ , where Î± denotes the strength coefficient of the LoS propagation path, $K _ { \mathrm { R i c i a n } }$ is the Rician factor used to reflect the ratio of the signal power in the LoS component to the average power in the multi-path scatters, and $I _ { 0 } ( \cdot )$ represents the refined ( )first-kind Bessel function with the zero order. Besides, the strength coefficient Î± of the Rician fading is further expressed as follows

$$
\alpha = \sqrt { \frac { K _ { \mathrm { R i c i a n } } + 1 } { \omega _ { \mathrm { L o S } } } } ,\tag{12}
$$

where $\omega _ { \mathrm { L o S } }$ is the variance of the fading radio signal.

2) The NLoS Propagation Channel: In the case of the NLoS propagation situation, where there exists no dominant propagation along an LoS path between the UAV and the ground users, the well-known Rayleigh fading is considered as a most suitable model for capturing the large-scale fading, dense obstacles, and frequently scattering effects. Thus, we denote the power gain of the NLoS propagation channel by $G _ { \mathrm { N L o S } }$ and the PDF of $G _ { \mathrm { N L o S } }$ can be formulated as follows, according to the Rayleigh distribution [60],

$$
f _ { G _ { \mathrm { N L o S } } } ( x ) = \exp ( - x ) , \forall x \geq 0 .\tag{13}
$$

Based on (11) and (13), the transmission capacity of the channel allocated to ground user $i \in \mathcal { T }$ can be formulated as follows

$$
\pi _ { i } [ k ] = \lambda _ { i } [ k ] B \log _ { 2 } \left( 1 + \frac { p _ { i } [ k ] G _ { l } } { \sigma _ { l } ^ { 2 } d _ { i } ^ { \beta _ { l } } [ k ] } \right) , l \in \{ \mathrm { L o S } , \mathrm { N L o S } \} ,\tag{14}
$$

where $B > 0$ is the total available bandwidth and $\lambda _ { i } [ k ] \geq 0$ 0 [ ] 0denotes the bandwidth allocation ratio for user i in time interval k. For all the ground users, we have $\begin{array} { r } { \sum _ { i = 1 } ^ { N } \lambda _ { i } [ k ] = 1 } \end{array}$ . In (15), $p _ { i } [ k ]$ [ ] = 1denotes the transmission power of user i in time interval $k , \sigma _ { l } ^ { 2 }$ and $\beta _ { l }$ represent the average background noise power and the path-loss exponent for wireless link case $l \in \{ \mathrm { L o S } , \mathrm { N L o S } \}$ ï¼ respectively. For both the LoS and the NLoS propagations, we also obtain the following results:

Lemma 1: Given the time allocation ratio for computation processing $\kappa [ k ]$ , the bandwidth allocation ratio $\lambda _ { i } [ k ]$ , the adopted transmission power $p _ { i } [ k ]$ [ ], the scheduled data to be transmitted $u _ { i } [ k ]$ and the relative distance between the UAV and user i $d _ { i } [ k ]$ , [ ] [ ]the probability of successful transmission completion for user i in time interval k for the LoS propagation channel is

$$
\begin{array} { r l } & { \operatorname* { P r } _ { \mathrm { L o S } } \left( \kappa [ k ] , \lambda _ { i } [ k ] , p _ { i } [ k ] , u _ { i } [ k ] , d _ { i } [ k ] \right) } \\ & { = \operatorname* { P r } _ { \mathrm { L o S } } \Bigg \{ \pi _ { i } [ k ] \geq \frac { u _ { i } [ k ] } { \left( 1 - \kappa [ k ] \right) \Delta t } \Bigg \} } \\ & { = Q _ { 1 } \left( \sqrt { 2 K _ { \mathrm { R i c i a n } } } , \alpha \sqrt { \frac { 2 \left( 2 ^ { \phi _ { i } [ k ] } - 1 \right) \sigma _ { _ { \mathrm { L o S } } } ^ { 2 } d _ { i } ^ { \beta _ { \mathrm { L o S } } } [ k ] } { p _ { i } [ k ] } } \right) , } \end{array}\tag{15}
$$

where $\phi _ { i } [ k ]$ is given by

$$
\phi _ { i } [ k ] = \frac { u _ { i } [ k ] } { ( 1 - \kappa [ k ] ) \Delta t \lambda _ { i } [ k ] B } ,\tag{16}
$$

and $Q _ { 1 } ( \cdot , \cdot )$ is the first-order Marcum Q-function defined as

$$
Q _ { 1 } ( x , y ) = \int _ { y } ^ { \infty } s \exp \left( - \frac { x ^ { 2 } + s ^ { 2 } } { 2 } \right) I _ { 0 } ( x s ) d s ,\tag{17}
$$

where $x , y \geq 0$ , and $I _ { 0 } ( \cdot )$ is the modified first-kind Bessel func-0 ( )tion with the zero order as in (11).

For the NLoS propagation channel, the probability of successful transmission completion for user i in interval k is

$$
\begin{array} { r l } & { \mathsf { P r } _ { \mathrm { N L o S } } \left( \kappa [ k ] , \lambda _ { i } [ k ] , p _ { i } [ k ] , u _ { i } [ k ] , d _ { i } [ k ] \right) } \\ & { = \mathsf { P r } _ { \mathrm { N L o S } } \left\{ \pi _ { i } [ k ] \ge \frac { u _ { i } [ k ] } { \left( 1 - \kappa [ k ] \right) \Delta t } \right\} } \\ & { = \exp \left( - \frac { \left( 2 ^ { \phi _ { i } [ k ] } - 1 \right) \sigma _ { \mathrm { N L o S } } ^ { 2 } d _ { i } ^ { \beta _ { \mathrm { N L o S } } } [ k ] } { p _ { i } [ k ] } \right) . } \end{array}\tag{18}
$$

Proof: The proof of Lemma 1 is provided in Appendix A of the online supplementary material.

Lemma 2: For each $i \in \mathcal { T }$ , the probability of successful transmission completion via the LoS propagation channel in time interval k can be approximated as

$$
\begin{array} { r l } & { \operatorname* { P r } _ { \mathrm { L o S } } \left( \boldsymbol { \kappa } [ k ] , \lambda _ { i } [ k ] , p _ { i } [ k ] , u _ { i } [ k ] , d _ { i } [ k ] \right) } \\ & { ~ \approx \exp \left( - \exp \left( b _ { 1 } \left( \mu _ { 1 } \right) \right) \mu _ { 2 , i } ^ { b _ { 2 } \left( \mu _ { 1 } \right) } [ k ] \right) , } \end{array}\tag{19}
$$

where $\mu _ { 1 }$ and $\mu _ { 2 , i } [ k ]$ are defined according to (15) as follows

$$
\left\{ \begin{array} { l l } { \mu _ { 1 } = \sqrt { 2 K _ { \mathrm { R i c i a n } } } ; } \\ { \mu _ { 2 , i } [ k ] = \alpha \sqrt { \frac { 2 \left( 2 ^ { \phi _ { i } [ k ] } - 1 \right) \sigma _ { \mathrm { L o S } } ^ { 2 } d _ { i } ^ { \beta _ { \mathrm { L o S } } } [ k ] } { p _ { i } [ k ] } } . } \end{array} \right.\tag{20}
$$

In (19), $b _ { 1 } ( \mu _ { 1 } )$ and $b _ { 2 } ( \mu _ { 1 } )$ are two n-order polynomials.

( ) ( )Proof: This lemma follows the approximation of the firstorder Marcum Q-Function proposed in [61]. -

Using the lemmas above, we derive a closed-form expression for characterizing the communication reliability with the consideration of the stochastic fading effect of both the LoS and the NLoS propagations as follows.

Theorem 1: For each user $i \in \mathcal { Z }$ , the communication reliability in each time interval k is

$$
\mathsf { P r } _ { i } [ k ] = \sum _ { l \in \mathcal { N } } \mathsf { P r } _ { l } \left( \kappa [ k ] , \lambda _ { i } [ k ] , p _ { i } [ k ] , u _ { i } [ k ] , d _ { i } [ k ] \right) \mathsf { P r } _ { l } \left( d _ { i } [ k ] \right) ,\tag{21}
$$

where $\mathcal { N }$ is used to denote the set of the different link types, $\mathcal { N } = \{ \mathrm { L o S } , \mathrm { N L o S } \}$ . The overall communication reliability for =supporting computation offloading during $T _ { i }$ time intervals is

$$
R _ { i } = \prod _ { k = 1 } ^ { T _ { i } } \operatorname* { P r } _ { i } [ k ] , i \in \mathcal { T } .\tag{22}
$$

Proof: As the ground user partitions the entire data demand into a series of data pieces for offloading, the offloading of these data pieces is independent across different time intervals [48], [49]. Therefore, the results (21) and (22) can be derived immediately by utilizing the law of total probability and multiplication in probability theory. -

As indicated by Theorem 1, the communication reliability formulation incorporates the impacts of resource allocation (including bandwidth and offloading time), transmission power, data partitions, and node mobility in the UAV-assisted MEC system. It is regarded as the primary system objective to be maximized. Therefore, we refer to the communication reliability formulation as the reliability metric of this communication system in this work.

## D. Energy Consumption Model

1) Propulsion Energy Consumption Model: We consider a fixed-wing UAV, whose propulsion energy consumption in time interval k can be estimated by

$$
E _ { \mathrm { p r o } } [ k ] = \theta _ { 3 } \left\| \pmb { v } [ k ] \right\| _ { 2 } ^ { 3 } + \frac { \theta _ { 4 } } { \left\| \pmb { v } [ k ] \right\| _ { 2 } } \left( 1 + \frac { \left\| \pmb { a } [ k ] \right\| _ { 2 } ^ { 2 } } { g ^ { 2 } } \right) ,\tag{23}
$$

where $g$ is the constant gravitational acceleration with a conventional value of $9 . 8 ~ \mathrm { m } / \bar { \mathrm { s } ^ { 2 } }$ . The two parameters $\theta _ { 3 }$ and $\theta _ { 4 }$ can be 9 8 m sspecified based on the UAVâs weight, aerodynamic shape and air-fluid dynamics [62].

Given the limited energy of the UAV, we denote the total energy budget for the UAV flight as $E _ { \mathrm { p r o , m a x } }$ . Then, we impose the following constraint on the propulsion energy consumption of the UAV:

$$
\sum _ { k = 1 } ^ { T } E _ { \mathrm { p r o } } [ k ] \leq E _ { \mathrm { p r o , m a x } } .\tag{24}
$$

2) Offloading Energy Consumption Model: The ground users consume energy for transmitting the offloaded data to the UAV. Specifically, for each user $i \in \mathcal { T }$ , the offloading energy consumption in time interval k is calculated as

$$
E _ { i , \mathrm { o f f } } [ k ] = ( 1 - \kappa [ k ] ) \Delta t p _ { i } [ k ] , \forall k .\tag{25}
$$

There is an upper bound of the offloading energy consumption of $i \in \mathcal { T } , E _ { i , \operatorname* { m a x } }$ , which is expressed as

$$
\sum _ { k = 1 } ^ { T _ { i } } E _ { i , \mathrm { o f f } } [ k ] \leq E _ { i , \mathrm { m a x } } .\tag{26}
$$

In addition, the transmission power for each user $i \in \mathcal { T }$ is also bounded as

$$
p _ { i } [ k ] \in [ p _ { i , \operatorname* { m i n } } , p _ { i , \operatorname* { m a x } } ] , \forall k .\tag{27}
$$

3) Computing Energy Consumption Model: Let the effective switched capacitance of the computing hardware architecture of the UAV-mounted cloudlet be $\zeta .$ According to [40], the energy consumption for processing the tasks offloaded from user $i \in \mathcal { Z }$ in time interval k is calculated by

$$
E _ { i , \mathrm { c o m } } [ k ] = \zeta \varpi _ { i } u _ { i } [ k ] ( f [ k ] ) ^ { 2 } , k = 1 , 2 , \ldots , T _ { i } ; i \in \mathbb { Z } .\tag{28}
$$

We further denote the energy budget of the UAV for edge computing by $E _ { \mathrm { c , m a x } }$ . Then, we should have

$$
\sum _ { i = 1 } ^ { N } \sum _ { k = 1 } ^ { T _ { i } } E _ { i , \mathrm { c o m } } [ k ] \leq E _ { c , \mathrm { m a x } } .\tag{29}
$$

## E. Joint Optimization Problem Formulation

For notation simplicity, we let

$$
\left\{ \begin{array} { l l } { a = \operatorname { c o l } \left\{ \pmb { a } [ k ] , k = 1 , 2 , \ldots , T \right\} ; } \\ { \kappa = \operatorname { c o l } \left\{ \kappa [ k ] , k = 1 , 2 , \ldots , T \right\} ; } \\ { \lambda _ { i } = \operatorname { c o l } \left\{ \lambda _ { i } [ k ] , k = 1 , 2 , \ldots , T _ { i } \right\} , i \in \mathbb { Z } ; } \\ { p _ { i } = \operatorname { c o l } \left\{ p _ { i } [ k ] , k = 1 , 2 , \ldots , T _ { i } \right\} , i \in \mathbb { Z } . } \end{array} \right.\tag{30}
$$

To guarantee the reliability of the UAV-assisted MEC system in the presence of probabilistic LoS and NLoS channel fading, we propose a joint optimization model that aims to maximize the overall communication reliability by jointly optimizing the motion control inputs of the UAV, , the time allocation for edge computing, , the bandwidth allocation for the ground users, $\{ \lambda _ { i } , i \in \mathcal { I } \}$ , the transmission power allocation for the ground users, $\{ p _ { i } , i \in \mathcal { I } \}$ , and the data transmission scheduling strategies of the users, $\{ u _ { i } , i \in \mathcal { I } \}$ . The joint optimization problem ucan be formulated by combining the above models as follows

$$
\begin{array} { l } { { \displaystyle \mathcal { M } _ { 1 } : \operatorname* { m a x } _ { w } \mathcal { R } \left( w \right) = \sum _ { i = 1 } ^ { N } R _ { i } = \sum _ { i = 1 } ^ { N } \left( \prod _ { k = 1 } ^ { T _ { i } } \mathbf { P r } _ { i } [ k ] \right) } } \\ { ~ } \\ { { \displaystyle \mathrm { s . t . } \left\{ \begin{array} { l l } { { \displaystyle ( 2 ) , \left( 4 \right) , \left( 5 \right) , \left( 7 \right) } ; } \\ { { \displaystyle ( 2 4 ) , \left( 2 6 \right) , \left( 2 7 \right) , \left( 2 9 \right) } ; } \\ { { \displaystyle q [ 1 ] = q _ { c } , \ q [ T + 1 ] = q _ { f } ; } } \\ { { \displaystyle \sum _ { i = 1 } ^ { N } \lambda _ { i } [ k ] = 1 , \forall k ; } } \\ { { \displaystyle ( k [ k ] \in \left( 0 , 1 \right) , \lambda _ { i } [ k ] \geq 0 , \forall i , k ; } } \end{array} \right. } } \end{array}\tag{31}
$$

where  is a column vector that collects all the decision variables, $\mathrm { i . e . , } w = \mathrm { c o l } \{ a , \kappa , \lambda _ { i } , p _ { i } , \boldsymbol { { u } } _ { i } , i \in \mathcal { T } \}$ Â·

$\mathcal { M } _ { 1 }$ is a strongly non-convex problem since different devision variables, $a , \kappa , \{ \lambda _ { i } , i \in \mathcal { T } \} , \{ p _ { i } , i \in \mathcal { T } \}$ , and $\{ u _ { i } , i \in \mathcal { I } \}$ , are a Îº pcoupled in the non-concave objective function $\mathcal { R } ( \pmb { x } )$ . Another challenge in dealing with problem $\mathcal { M } _ { 1 }$ (x)is that the state-space equations in (2) introduces recursive couplings among the motion control variables in different time intervals. To address this problem, we proceed to design a model transformation approach and an effective iterative algorithm in the following section.

## IV. JOINT OPTIMIZATION METHOD

To tackle problem $\mathcal { M } _ { 1 }$ , we propose a joint optimization method that transforms the original constrained optimization problem into a sequence of unconstrained optimization subproblems by combining a set of augmented Lagrangian multipliers. The subproblems can be effectively solved by using unconstrained optimization techniques (such as Newtonâs methods).

## A. Model Transformation

Since the original problem $\mathcal { M } _ { 1 }$ involves the recursive coupling among the motion state variables, $\{ \pmb q [ k ] , \forall k \}$ , and the control variables, $\{ { \pmb a } [ k ] , \forall k \}$ q[ ], as shown in (2), we are inspired by a[ ]the direct multiple shooting method to include the state variables in successive time intervals as decision variables. Thus, the state-space equations in (2) can be treated as equality constraints. We let $\pmb q = \mathrm { c o l } \{ \pmb q [ k ] , k = 2 , 3 , \ldots , T + 1 \}$ and introduce an q = q[ ] = 2 3 + 1augmented decision variable vector to collect all the decision variables as $\psi = \mathrm { c o l } \{ q , w \}$ . For simplicity, the lower bound Ï = q wand the upper bound of the augmented decision variable  are given as $\psi _ { \mathrm { m i n } }$ and $\psi _ { \mathrm { m a x } }$ , respectively, i.e.,

$$
\psi _ { \mathrm { m i n } } = \left[ \begin{array} { c } { \mathbf { 1 } _ { T } \otimes \pmb { q } _ { \mathrm { m i n } } } \\ { \pmb { w } _ { \mathrm { m i n } } } \end{array} \right] , \psi _ { \mathrm { m a x } } = \left[ \begin{array} { c } { \mathbf { 1 } _ { T } \otimes \pmb { q } _ { \mathrm { m a x } } } \\ { \pmb { w } _ { \mathrm { m a x } } } \end{array} \right] ,\tag{32}
$$

where ${ \pmb w } _ { \mathrm { m i n } }$ and ${ \pmb w } _ { \mathrm { m a x } }$ are given by

$$
\begin{array}{c} { w } _ { \mathrm { m i n } } = [ \begin{array} { c } { \mathbf { 1 } _ { T } \otimes \boldsymbol { a } _ { \mathrm { m i n } } } \\ { \mathbf { 0 } _ { | \kappa | } } \\ { \phantom { [ \boldsymbol { 1 } _ { \mathrm { l } } ] } \mathbf { 0 } _ { | \lambda | } } \\  \phantom { [ \boldsymbol { p } _ { \mathrm { m i n } } ] } \boldsymbol { [ \begin{array} { l } { \mathbf { 1 } _ { T } \otimes \boldsymbol { a } _ { \mathrm { m a x } } } \\ { \phantom { [ \boldsymbol { 1 } _ { T } \otimes \boldsymbol { a } _ { \mathrm { m a x } } } \end{array} ] } \end{array} ] } , \ : \ : { w } _ { \mathrm { m a x } } = [ \begin{array} { c } { \mathbf { 1 } _ { T } \otimes \boldsymbol { a } _ { \mathrm { m a x } } } \\ { \mathbf { 1 } _ { | \kappa | } } \\ { \phantom { [ \boldsymbol { 1 } _ { \lambda | } ] } \mathbf { 1 } _ { \rho } } \\ { \phantom { [ \boldsymbol { p } _ { \mathrm { m a x } } } \boldsymbol { [ \begin{array} { l } { \boldsymbol { 1 } _ { T } } \\ { \boldsymbol { u } _ { \mathrm { m a x } } } \end{array} ] } } \\ { \phantom { [ \boldsymbol { u } _ { \mathrm { m a x } } } \end{array} ] } \end{array} ] ,\tag{33}
$$

where $| \cdot |$ represents the set cardinality, 0 and 1 are all-zero and all-one vectors, and $p _ { \operatorname* { m i n } } , p _ { \operatorname* { m a x } } , u _ { \operatorname* { m i n } } , u _ { \operatorname* { m a x } }$ are the lower p p u uand upper bounds of all the transmission power allocation and transmission scheduling decision variables.

Let $g _ { 1 } ( \psi ) = \psi - \psi _ { \mathrm { m i n } } , g _ { 2 } ( \psi ) = \psi _ { \mathrm { m a x } } - \psi , g _ { 3 } ( \psi ) =$ $\begin{array} { r } { E _ { \mathrm { p r o , m a x } } - \sum _ { k = 1 } ^ { T } E _ { \mathrm { p r o } } [ k ] , g _ { 4 } ( \psi ) = E _ { c , \mathrm { m a x } } - \sum _ { i = 1 } ^ { N } \sum _ { k = 1 } ^ { T _ { i } } \zeta } \end{array}$ $\varpi _ { i } u _ { i } [ k ] ( f [ k ] ) ^ { 2 }$ , and $\begin{array} { r } { \pmb { g } _ { 5 , i } ( \pmb { \psi } ) = E _ { i , \mathrm { m i n } } - \sum _ { k = 1 } ^ { T _ { i } } ( 1 - \kappa [ k ] ) \Delta t p _ { i } } \end{array}$ [ ]( [k for each $i \in \mathcal { T }$ g (Ï) = (1 [ ])Î. From the constraints in (7), we also have $\begin{array} { r } { g _ { 6 } ( \psi ) = \cot \{ f _ { \operatorname* { m a x } } \kappa [ k ] \Delta t - \sum _ { i = 1 } ^ { N } \varpi _ { i } u _ { i } [ k ] , k = 1 , 2 , \ldots , T \} } \end{array}$ g (Ï) = [ ]Î [ ] = 1 2Now, we can lump all the inequalities involved in the original problem $\mathcal { M } _ { 1 }$ into a column vector function, $\mathbf { \nabla } _ { \mathbf { \boldsymbol { g } } \left( \psi \right) }$ , as follows

$$
g ( \psi ) = \cot \left\{ g _ { 1 } ( \psi ) , \ldots , g _ { 4 } ( \psi ) , g _ { 5 , i } ( \psi ) , i \in \mathcal { T } , g _ { 6 } ( \psi ) \right\} ,\tag{34}
$$

so that we can represent the whole inequalities as $\mathbf { \nabla } \mathbf { \mathbf { } } g ( \psi ) \geq \mathbf { 0 }$ Following the same logic above, we let $\begin{array} { r } { h _ { 1 } ( \psi ) = \pmb q [ 1 ] - \pmb q _ { c } , } \end{array}$ $h _ { 2 } ( \psi ) = { \pmb q } [ T + 1 ] - { \pmb q } _ { f }$ , and

$$
h _ { 3 , k } ( \psi ) = \pmb q [ k + 1 ] - ( A \pmb q [ k ] + B \pmb a [ k ] )\tag{35}
$$

for $k = 1 , 2 , \dots , T .$ . We also introduce

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { h _ { 4 , i } ( \psi ) = C _ { i } - \sum _ { k = 1 } ^ { T _ { i } } u _ { i } [ k ] , i \in \mathbb { Z } } \\ { h _ { 5 , k } ( \psi ) = 1 - \sum _ { i = 1 } ^ { N } \lambda _ { i } [ k ] , k = 1 , 2 , . . . , T . } \end{array} \right. } \end{array}\tag{36}
$$

Using the notations, we can lump all the equalities into a column vector function, $h ( \psi )$ , as follows

$$
\begin{array} { r } { h ( \psi ) = \cot \left\{ \begin{array} { l } { h _ { 1 } ( \psi ) , h _ { 2 } ( \psi ) , h _ { 3 , k } ( \psi ) , h _ { 4 , i } ( \psi ) , h _ { 5 , k } ( \psi ) , } \\ { i \in \mathcal { T } , k = 1 , 2 , \ldots , T } \end{array} \right\} . } \end{array}\tag{37}
$$

Hence, the whole equalities of $\mathcal { M } _ { 1 }$ can be represented in a more compact fashion, i.e., $\pmb { h } ( \psi ) = \mathbf { 0 }$

h(Ï) =Let the size of the function vectors $\mathbf { \nabla } _ { \mathbf { \boldsymbol { g } } \left( \psi \right) }$ and $h ( \psi )$ be $m _ { g }$ and $m _ { h }$ , respectively. We use $g _ { l } ( \psi )$ g(Ï) h(Ï)to denote the lth entity in $\mathbf { \nabla } _ { \mathbf { \boldsymbol { g } } \left( \psi \right) }$ for $l = 1 , 2 , \ldots , m _ { g } .$ , and $h _ { l } ( \psi )$ in $h ( \psi )$ for $l = 1 , 2 , \ldots , m _ { h }$ = 1 2 (We have the following result:

Lemma 3: The original problem $\mathcal { M } _ { 1 }$ has an augmented Lagrangian function as follows

$$
\begin{array} { l } { { \displaystyle { \mathcal { L } } _ { \sigma } ( \psi , \nu , \vartheta ) = - \sum _ { i = 1 } ^ { N } R _ { i } } } \\ { { \displaystyle \qquad + \frac { 1 } { 2 \sigma } \sum _ { l = 1 } ^ { m _ { g } } \left\{ \left[ \operatorname* { m a x } \big ( 0 , \nu _ { l } - \sigma g _ { l } ( \psi ) \big ) \right] ^ { 2 } - \nu _ { l } ^ { 2 } \right\} } } \\ { { \displaystyle \qquad - \sum _ { l = 1 } ^ { m _ { h } } \vartheta _ { l } h _ { l } ( \psi ) + \frac { \sigma } { 2 } \sum _ { l = 1 } ^ { m _ { h } } h _ { l } ^ { 2 } ( \psi ) } , \qquad ( 3 8 ) }  \end{array}\tag{}
$$

where $\pmb { \nu } = \mathrm { c o l } \{ \nu _ { l } \in \mathbb { R } , l = 1 , 2 , \dots , m _ { q } \}$ and col $\{ \vartheta _ { l } \in$ ${ \mathbb R } , l = 1 , 2 , \dots , m _ { h } \big \}$ = 1 2 Ïare Lagrangian multipliers. $\sigma > 0$ is a = 1 2positive penalty factor.

Proof: The proof of Lemma 3 is provided in Appendix B of the online supplementary material.

## B. Successive Unconstrained Optimization

From Lemma 3, we can see that the penalty factor, Ï, scales the effect of unsatisfied equality constraints on the augmented Lagrangian function, $\mathcal { L } _ { \sigma } ( \psi , \nu , \vartheta )$ . A fundamental question arises (Ï Î½ Ï)when incorporating such penalty factor into $\mathcal { L } _ { \sigma } ( \psi , \nu , \vartheta )$ : how (Ï Î½ Ï)to configure the penalty factor such that we can solve a local optimal point of the original problem $\mathcal { M } _ { 1 }$ by solving the following unconstrained optimization problem

$$
\mathcal { M } _ { 3 } : \operatorname* { m i n } _ { \psi } \mathcal { L } _ { \sigma } ( \psi , \nu , \vartheta ) .\tag{39}
$$

To answer this question, we turn to prove the equivalence between a local optimal solution of $\mathcal { M } _ { 1 }$ and a strict local minima of $\mathcal { M } _ { 3 } \left( \mathrm { o r } \mathcal { M } _ { 2 } \right)$ under certain conditions. For simplicity, we collect both the inequalities and equalities into a function vector, $H ( \psi )$ ï¼ as follows

$$
\begin{array} { r } { H ( \psi ) = \bigg [ \frac { g ( \psi ) - \varsigma \odot \varsigma } { h ( \psi ) } \bigg ] , } \end{array}\tag{40}
$$

where  is given by (S.8) in Lemma 3, and  denotes the elementwise product operator. Let $H _ { l } ( \psi )$ be the lth entity of $H ( \psi )$ , with $l = 1 , 2 , \ldots , m _ { g } + m _ { h }$ (Ï), and let $v = \mathrm { c o l } \{ \nu , \vartheta \}$ H(Ï). Then, the

augmented Lagrangian function (38) can be rewritten as

$$
\begin{array} { l } { \displaystyle \mathcal { L } _ { \boldsymbol { \sigma } } ( \boldsymbol { \psi } , \boldsymbol { v } ) = - \sum _ { i = 1 } ^ { N } R _ { i } } \\ { \displaystyle - \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } v _ { l } H _ { l } ( \boldsymbol { \psi } ) + \frac { \sigma } { 2 } \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } H _ { l } ^ { 2 } ( \boldsymbol { \psi } ) } \\ { = - \sum _ { i = 1 } ^ { N } R _ { i } - \boldsymbol { v } ^ { \mathrm { T } } H ( \boldsymbol { \psi } ) + \frac { \sigma } { 2 } H ( \boldsymbol { \psi } ) ^ { \mathrm { T } } H ( \boldsymbol { \psi } ) . } \end{array}\tag{41}
$$

Besides, the traditional Lagrangian function is given as

$$
L ( \psi , v ) = - \sum _ { i = 1 } ^ { N } R _ { i } - v ^ { \mathrm { T } } H ( \psi ) .\tag{42}
$$

Let $\hat { \psi }$ be a local optimal solution of the original problem $\mathcal { M } _ { 1 }$ that Ïsatisfies the second-order sufficient optimality condition, i.e., a set of Lagrangian multipliers, $\bar { \boldsymbol { v } } = \operatorname { c o l } \{ \bar { v } _ { l } , l = 1 , 2 , \dots , m _ { g } +$ $m _ { h } \}$ , exist such that

$$
\left\{ \begin{array} { l l } { - \sum _ { i = 1 } ^ { N } \nabla R _ { i } - W \bar { \boldsymbol { v } } = \mathbf { 0 } ; } \\ { H ( \bar { \boldsymbol { \psi } } ) = \mathbf { 0 } , } \end{array} \right.\tag{43}
$$

where $W = [ \nabla H _ { 1 } ( \bar { \psi } ) , \ldots , \nabla H _ { m _ { q } + m _ { h } } ( \bar { \psi } ) ]$ , and for any nonzero vector $\varrho \neq \mathbf { 0 }$ gsatisfying $\varrho ^ { \mathrm { T } } \nabla H _ { l } ( \bar { \psi } ) = 0$ $l =$ , $, 2 , \ldots , m _ { g } + m _ { h }$  =, it holds that

$$
\varrho ^ { \mathrm { T } } \nabla _ { \psi } ^ { 2 } L ( \bar { \psi } , \bar { v } ) \varrho > 0 .\tag{44}
$$

For such $\hat { \psi }$ and , we have the following result:

Ï ÏÂ¯Theorem 2: Suppose that $\bar { \psi }$ and  satisfy the second-order Ï ÏÂ¯sufficient condition for a local optimal solution of the original problem $\mathcal { M } _ { 1 }$ . There exists a nonnegative constant, $\sigma ^ { \prime } \geq 0 ;$ , such that for all Ï satisfying $\sigma > \sigma ^ { \prime }$ 0, is a strict local minima of the unconstrained optimization problem $\mathcal { M } _ { 3 }$

Proof: From (41), we can first have

$$
\begin{array} { l } { \displaystyle \nabla _ { \psi } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { \upsilon } ) = - \sum _ { i = 1 } ^ { N } \nabla _ { \psi } R _ { i } - \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } \bar { \upsilon } _ { l } \nabla _ { \psi } H _ { l } ( \bar { \psi } ) } \\ { \displaystyle + \sigma \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } H _ { l } ( \bar { \psi } ) \nabla _ { \psi } H _ { l } ( \bar { \psi } ) . } \end{array}\tag{45}
$$

Since $\hat { \psi }$ is a local optimum that meets the second-order sufficient Ïcondition, it is also a Karush-Kuhn-Tucker (KKT) point of $\mathcal { M } _ { 1 }$ Recalling (43), we can see

$$
\nabla _ { \psi } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { v } ) = \mathbf { 0 } .\tag{46}
$$

In the following, we only need to prove that the Hessian matrix of $\mathcal { L } _ { \sigma } ( \psi , \bar { v } )$ at the point  , $\nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { v } )$ , is a positive-definite (Ï ÏÂ¯) Ïmatrix. From (45), we have

$$
\begin{array} { l } { { \nabla _ { \psi } ^ { 2 } { \mathcal { L } } _ { \sigma } ( \psi , \bar { v } ) = \displaystyle - \sum _ { i = 1 } ^ { N } \nabla _ { \psi } ^ { 2 } R _ { i } } } \\ { \displaystyle - \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } \left( \bar { v } _ { l } - \sigma H _ { l } ( \psi ) \right) \nabla _ { \psi } ^ { 2 } H _ { l } ( \psi ) } \end{array}
$$

$$
\begin{array} { r l } {  { m _ { g } + m _ { h } } } \\ & { + \sigma \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } \nabla _ { \psi } H _ { l } ( \psi ) \nabla _ { \psi } H _ { l } ( \psi ) ^ { \mathrm { T } } } \\ & { } \\ & { = \pmb { Q } + \sigma \pmb { W W } ^ { \mathrm { T } } , } \end{array}\tag{47}
$$

where $Q$ is given by

$$
\pmb { Q } = - \sum _ { i = 1 } ^ { N } \nabla _ { \psi } ^ { 2 } R _ { i } - \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } \left( \bar { v } _ { l } - \sigma H _ { l } ( \psi ) \right) \nabla _ { \psi } ^ { 2 } H _ { l } ( \psi ) .\tag{48}
$$

Substituting $\hat { \psi }$ into (47), we obtain

$$
\nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { v } ) = \bar { Q } + \sigma \bar { W } \bar { W } ^ { \mathrm { T } } .\tag{49}
$$

Let rank $\bar { ( W ) } = r \le m _ { g } + m _ { h }$ and n be the size of $\hat { \psi } .$ . We (W ) = + Ïintroduce a matrix â RnÃr that is an orthogonal matrix with respect to  , $V ^ { \mathrm { T } } V = I ,$ , i.e., the r column vectors of $V$ are W V V = I Va group of orthogonal bases of a subspace generated from the $m _ { g } + m _ { h }$ column vectors of  . Thus, we can have

$$
\bar { \cal W } = { \cal V } Z ,\tag{50}
$$

where $\boldsymbol { Z } = \boldsymbol { V } ^ { \mathrm { T } } \bar { \boldsymbol { W } }$ and rank $( Z ) = r .$

Z = VBesides, let $\boldsymbol { \xi }$ W (Z) =be any nonzero column vector, $\pmb { \xi } \in \mathbb { R } ^ { n \times 1 }$ , such Î¾that it can be expressed as

$$
\pmb { \xi } = \pmb { \xi } _ { 1 } + \pmb { V } \pmb { \xi } _ { 2 } ,\tag{51}
$$

where $\xi _ { 1 }$ satisfies $V ^ { \mathrm { T } } \pmb { \xi } _ { 1 } = \mathbf { 0 }$ . We also have $\bar { \boldsymbol { W } } ^ { \mathrm { T } } \boldsymbol { \xi } _ { 1 } = \mathbf { 0 } .$ , i.e.,

$$
\nabla H _ { l } ( \bar { \psi } ) ^ { \mathrm { T } } \pmb { \xi } _ { 1 } = \mathbf { 0 } , l = 1 , 2 , \ldots , m _ { g } + m _ { h } .\tag{52}
$$

Using the above notations, we can rewrite $\xi ^ { \mathrm { T } } \nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { v } ) \xi$ as

$$
\begin{array} { r l } & { \xi ^ { \mathrm { T } } \nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { \upsilon } ) \xi } \\ & { = ( \xi _ { 1 } + V \xi _ { 2 } ) ^ { \mathrm { T } } \left( \bar { Q } + \sigma \bar { W } \bar { W } ^ { \mathrm { T } } \right) ( \xi _ { 1 } + V \xi _ { 2 } ) } \\ & { = \xi _ { 1 } ^ { \mathrm { T } } \bar { Q } \xi _ { 1 } + 2 \xi _ { 1 } ^ { \mathrm { T } } \bar { Q } V \xi _ { 2 } + \xi _ { 2 } ^ { \mathrm { T } } V ^ { \mathrm { T } } \bar { Q } V \xi _ { 2 } + \sigma \xi _ { 2 } ^ { \mathrm { T } } Z Z ^ { \mathrm { T } } \xi _ { 2 } . } \end{array}\tag{Î¾(53}
$$

Since $\hat { \psi }$ is a local optimal solution of the original problem $\mathcal { M } _ { 1 }$ that satisfies the second-order sufficient condition, there exists a positive constant $c _ { 1 } > 0$ such that

$$
\begin{array} { r } { \pmb { \xi } _ { 1 } ^ { \mathrm { T } } \bar { \pmb { Q } } \pmb { \xi } _ { 1 } \geq c _ { 1 } \| \pmb { \xi } _ { 1 } \| _ { 2 } ^ { 2 } . } \end{array}\tag{54}
$$

Let $c _ { 2 }$ be the maximum singular value of the matrix $\bar { Q } V$ and $c _ { 3 } = \| \mathbf { V } ^ { \mathrm { T } } { \bar { \cal Q } } { \cal V } \| _ { 2 } .$ . Additionally, let $c _ { 4 } > 0$ QVbe the minimum = V Qeigenvalue of $\boldsymbol { Z } \boldsymbol { Z } ^ { \mathrm { T } }$ . Then, we have

$$
\begin{array} { r l } & { \xi ^ { \mathrm { T } } \nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { v } ) \xi } \\ & { \geq c _ { 1 } \| \xi _ { 1 } \| _ { 2 } ^ { 2 } - 2 c _ { 2 } \| \xi _ { 1 } \| _ { 2 } \| \xi _ { 2 } \| _ { 2 } + ( \sigma c _ { 4 } - c _ { 3 } ) \| \xi _ { 2 } \| _ { 2 } ^ { 2 } . } \end{array}\tag{55}
$$

Since $\pmb { \xi } \neq \mathbf { 0 } , \pmb { \xi } _ { 1 }$ and $\xi _ { 2 }$ must not be zero vectors simultaneously. Î¾ = Î¾ Î¾Therefore, if Ï is sufficiently large such that

$$
\sigma c _ { 4 } - c _ { 3 } - \frac { c _ { 2 } ^ { 2 } } { c _ { 1 } } > 0 ,\tag{56}
$$

i.e.,

$$
\sigma > \frac { c _ { 2 } ^ { 2 } + c _ { 1 } c _ { 3 } } { c _ { 1 } c _ { 4 } } ,\tag{57}
$$

we have

$$
\begin{array} { r l r } & { } & { \pmb { \xi } ^ { \mathrm { T } } \nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { \upsilon } ) \pmb { \xi } > c _ { 1 } \| \pmb { \xi } _ { 1 } \| _ { 2 } ^ { 2 } - 2 c _ { 2 } \| \pmb { \xi } _ { 1 } \| _ { 2 } \| \pmb { \xi } _ { 2 } \| _ { 2 } + \frac { c _ { 2 } ^ { 2 } } { c _ { 1 } } \| \pmb { \xi } _ { 2 } \| _ { 2 } ^ { 2 } } \\ & { } & { = \bigg ( \sqrt { c _ { 1 } } \| \pmb { \xi } _ { 1 } \| _ { 2 } - \frac { c _ { 2 } } { \sqrt { c _ { 1 } } } \| \pmb { \xi } _ { 2 } \| _ { 2 } \bigg ) ^ { 2 } \geq 0 . ~ ( 5 8 } \end{array}
$$

The above result indicates that

$$
\xi ^ { \mathrm { T } } \nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { v } ) \pmb { \xi } > 0\tag{59}
$$

always holds true and there exists $\sigma ^ { \prime }$ , i.e.,

$$
\sigma ^ { \prime } = \frac { c _ { 2 } ^ { 2 } + c _ { 1 } c _ { 3 } } { c _ { 1 } c _ { 4 } } ,\tag{60}
$$

such that $\nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { v } )$ is positive definite when $\sigma > \sigma ^ { \prime }$ . Combining (46) and (59), we can conclude that $\bar { \psi }$ is a strict local minima of $\mathcal { M } _ { 3 }$

In Theorem 2, we show the necessary condition for the local optimal solution of the original problem $\mathcal { M } _ { 1 }$ . On the other hand, we also have the sufficient condition as follows.

Theorem 3: Suppose that there exists a feasible point, $\widetilde { \psi } _ { ; }$ , such that $H _ { l } ( \widetilde { \boldsymbol { \psi } } ) = 0 \mathrm { f o r } l = 1 , 2 , \dots , m _ { g } + m _ { h } , \widetilde { \boldsymbol { \psi } }$ is a local minima (Ï) = 0 = 1 2 +of the unconstrained optimization problem $\mathcal { M } _ { 3 }$ with a certain , i.e., $\widetilde { \psi } \in \mathrm { a r g m i n } \mathcal { L } _ { \sigma } ( \psi , \widetilde { v } )$ , and $\widetilde { \psi }$ also satisfies the second-order sufficient condition for the local minima of $\mathcal { M } _ { 3 }$ . Then, $\widetilde { \psi }$ is a strict local optimal solution of $\mathcal { M } _ { 1 }$

Proof: Since $\widetilde { \psi }$ is a local minima of $\mathcal { L } _ { \sigma } ( \psi , \widetilde { \upsilon } )$ and satisfies Ï (Ïthe second-order sufficient condition, we have

$$
\nabla _ { \psi } \mathcal { L } _ { \sigma } ( \widetilde { \psi } , \widetilde { v } ) = 0 ,\tag{61}
$$

and, for any nonzero vector $\xi \neq \mathbf { 0 } ,$ , we have

$$
\xi ^ { \mathrm { T } } \nabla _ { \psi } ^ { 2 } \mathcal { L } _ { \sigma } ( \widetilde { \psi } , \widetilde { v } ) \xi > 0 .\tag{62}
$$

Recalling (45), (61) and $H _ { l } ( \widetilde { \boldsymbol { \psi } } ) = 0 \mathrm { f o r } l = 1 , 2 , \dots , m _ { g } + m _ { h }$ we yield

$$
- \sum _ { i = 1 } ^ { N } \nabla _ { \psi } R _ { i } - \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } \widetilde { v } _ { l } \nabla _ { \psi } H _ { l } ( \widetilde { \psi } ) = \mathbf { 0 } .\tag{63}
$$

At this point, $\widetilde { \psi }$ is a KKT point of $\mathcal { M } _ { 1 }$

ÏRecalling (47) and (62), for any nonzero vector  satisfying

$$
\begin{array} { r } { \pmb { \xi } ^ { \mathrm { T } } \nabla _ { \pmb { \psi } } H _ { l } ( \widetilde { \pmb { \psi } } ) = 0 , l = 1 , 2 , \dots , m _ { g } + m _ { h } , } \end{array}\tag{64}
$$

we can get

$$
\pmb { \xi } ^ { \mathrm { T } } \left( - \sum _ { i = 1 } ^ { N } \nabla _ { \psi } ^ { 2 } R _ { i } - \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } \widetilde { v } _ { l } \nabla _ { \psi } ^ { 2 } H _ { l } ( \widetilde { \psi } ) \right) \pmb { \xi } > 0 .\tag{65}
$$

According to (63) and (65), $\widetilde { \psi }$ is a strict local optimal solution of $\mathcal { M } _ { 1 }$

Based on Theorems 2 and 3, we do not need to set the penalty factor Ï to be infinite. Given the Lagrangian multipliers, we can obtain a local optimal solution of the original problem $\mathcal { M } _ { 1 }$ by minimizing the unconstrained optimization objective function $\mathcal { L } _ { \sigma } ( \psi , v )$ with a sufficiently large Ï.

(Ï Ï)Next, we further propose an iterative estimation scheme to find the optimal Lagrangian multipliers  and the corresponding local optimal solution $\bar { \psi }$ . Let j be the index of iterations, and $\psi _ { j }$ and $v _ { j }$ Ïbe the jth iterate of the solution and the Lagrangian Ï Ïmultipliers, respectively. When $\psi _ { j }$ is a minimizer of $\mathcal { L } _ { \sigma } ( \psi , v _ { j } )$ , i.e., $\psi _ { j } \in$ argmin $\mathcal { L } _ { \sigma } ( \psi , v _ { j } )$ Ï, we have

$$
\begin{array} { c c } { { \nabla _ { \psi } \mathcal { L } _ { \sigma } ( \psi _ { j } , v _ { j } ) = { } - \displaystyle \sum _ { i = 1 } ^ { N } \nabla _ { \psi } R _ { i } } } & { { } } \\ { { } } & { { - \displaystyle \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } \left( v _ { l , j } - \sigma H _ { l } ( \psi _ { j } ) \right) \nabla _ { \psi } H _ { l } ( \psi _ { j } ) } } \\ { { } } & { { } } \\ { { } } & { { = { } { \bf 0 } . } } \end{array}
$$

For the original problem $\mathcal { M } _ { 1 }$ , a local optimal solution $\hat { \psi }$ and a set of optimal Lagrangian multipliers  should satisfy

$$
\begin{array} { c } { { \nabla _ { \psi } \mathcal { L } _ { \sigma } ( \bar { \psi } , \bar { v } ) = ~ - \displaystyle \sum _ { i = 1 } ^ { N } \nabla _ { \psi } R _ { i } } } \\ { { ~ - ~ \displaystyle \sum _ { l = 1 } ^ { m _ { g } + m _ { h } } \bar { v } _ { l } \nabla _ { \psi } H _ { l } ( \bar { \psi } ) = 0 . } } \end{array}\tag{67}
$$

From (66) and (67), we see that if $\psi _ { j } = \bar { \psi }$ , we have $\bar { v } _ { l } = v _ { l , j } -$ $\sigma H _ { l } ( \psi _ { j } )$ for $l = 1 , 2 , \ldots , m _ { g } + \bar { m _ { h } }$ = Ï Â¯ =. This formula inspires the (Ï ) = 1 2 +following update equation to iteratively adjust the Lagrangian multipliers

$$
v _ { l , j + 1 } = v _ { l , j } - \sigma H _ { l } ( \psi _ { j } ) , l = 1 , 2 , \ldots , m _ { g } + m _ { h } .\tag{68}
$$

Recalling (S.8) and (40), we can rewrite the updates of these Lagrangian multipliers based on (68) as follows

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { \nu _ { l , j + 1 } = \operatorname* { m a x } \left( 0 , \nu _ { l , j } - \sigma g _ { l } ( \psi _ { j } ) \right) , } & { l = 1 , 2 , \dots , m _ { g } ; } \\ { \vartheta _ { l , j + 1 } = \vartheta _ { l , j } - \sigma h _ { l } ( \psi _ { j } ) , } & { l = 1 , 2 , \dots , m _ { h } . } \end{array} \right. } \end{array}\tag{69}
$$

Based on Lemma 3 and Theorems 2 and 3, the overall solving algorithm is summarized in Algorithm 1. In this algorithm, we adapt the penalty factor Ï by multiplying it with a constant $C _ { \sigma } > 1$ to increase its value. We have $\varepsilon _ { 1 } >$ denote the tolerant 1numerical error, and $\varepsilon _ { 2 } \in ( 0 , 1 )$ is a constant threshold to adjust (0 1)the penalty factor. The unconstrained optimization problem can be solved by using legacy unconstrained optimization methods, such as Newtonâs methods and the conjugate gradient descent methods.

## C. Algorithm Complexity Analysis

As demonstrated in Theorem 2, the penalty factor Ï does not need to be infinite. Therefore, by utilizing the sufficient conditions outlined in [63], the sequence of penalty factors generated by Algorithm 1, denoted as $\{ \sigma _ { j } , j = 0 , 1 , \ldots \}$ , possesses an upper bound $\sigma _ { \mathrm { u p p e r } } ,$ i.e., $\sigma _ { j } \le \sigma _ { \mathrm { u p p e r } }$ = 0 1. Additionally, due to the continuity of $h ( \psi )$ and the compactness of the solution domain of $\psi , \| h ( \psi ) \| _ { 2 }$ )remains bounded throughout iterations. Ï h(Ï)We denote the upper bound of $\| h ( \psi ) \| _ { 2 }$ by $h _ { \mathrm { u p p e r } } .$ . According to algorithm complexity theory, the time complexity of an algorithm is typically characterized by a function representing the worst-case number of iterations for convergence. We can employ the big-O notation to describe the time complexity. Hence, based on the complexity analysis provided in [64] (refer to Theorem 3.1 in [64]), the time complexity of Algorithm 1 is characterized as follows:

```perl
Algorithm 1: Iterative Optimization Algorithm.
Data: An initial guess $\psi _ { 0 } .$ , the penalty factor $\sigma ,$ the error
tolerance $\varepsilon _ { 1 } > 0 ,$ constants $C _ { \sigma } > 1$ and
$\varepsilon _ { 2 } \in ( 0 , 1 )$
Result: Optimal solution $\psi _ { j }$
1 $j  0 ;$
2 repeat
3 Solve $\mathcal { M } _ { 3 }$ with the initial $\psi _ { j - 1 }$ to obtain $\psi _ { j }$
$\psi _ { j } \in$ argmin $\mathcal { L } _ { \sigma } ( \psi , \nu _ { j } , \vartheta _ { j } )$
4 if $\frac { | | h ( \psi _ { j } ) | | _ { 2 } } { | | h ( \psi _ { j - 1 } ) | | _ { 2 } } \geq \varepsilon _ { 2 }$ then
5 $\sigma  C _ { \sigma } \sigma ;$
6 end
Calculate $\nu _ { j + 1 }$ and $\vartheta _ { j + 1 }$ by (69);
8 $j  j + 1 .$
9 until $\| h ( \psi _ { j } ) \| _ { 2 } < \varepsilon _ { 1 } ;$
```

Corollary 1: Let the worst-case running time for Algorithm 1 be $T _ { \mathrm { w o r s t } } .$ . Algorithm 1 has

$$
T _ { \mathrm { w o r s t } } \in \mathcal { O } \left( N ( \varepsilon _ { 1 } ) \frac { \log { \left( \frac { \sigma _ { \mathrm { u p p e r } } } { \sigma _ { 0 } } \right) } } { \log { ( C _ { \sigma } ) } } \frac { \log { \left( \frac { \varepsilon _ { 1 } } { h _ { \mathrm { u p p e r } } } \right) } } { \log { ( \varepsilon _ { 2 } ) } } \right) ,\tag{71}
$$

where $N ( \varepsilon _ { 1 } )$ denotes the worst-case number of iterations re-( )quired to achieve the given numerical accuracy Îµ1 in solving the unconstrained optimization $\mathcal { M } _ { 3 } , \mathrm { i . e . }$ ., solving (70).

Proof: The proof of Corollary 1 is provided in Appendix C of the online supplementary material.

Moreover, according to [65], a cubically regularized Newtonâs method can achieve an $\mathcal { O } ( \varepsilon _ { 1 } ^ { - \frac { 3 } { 2 } } )$ complexity bound, i.e., $N ( \varepsilon _ { 1 } ) \in$ $\mathcal { O } ( \varepsilon _ { 1 } ^ { - \frac { 3 } { 2 } } )$ . Substituting this result into (71) in Corollary 1, we ( )further have

$$
T _ { \mathrm { w o r s t } } \in \mathcal { O } \left( \varepsilon _ { 1 } ^ { - \frac { 3 } { 2 } } \frac { \log { \left( \frac { \sigma _ { \mathrm { u p p e r } } } { \sigma _ { 0 } } \right) } } { \log { ( C _ { \sigma } ) } } \frac { \log { \left( \frac { \varepsilon _ { 1 } } { h _ { \mathrm { u p p e r } } } \right) } } { \log { ( \varepsilon _ { 2 } ) } } \right) .\tag{72}
$$

The result (72) indicates that the algorithm can efficiently solve the problem, as it exhibits polynomial time complexity.

## V. SIMULATION EVALUATION

## A. Simulation Setup

We conduct simulations to validate the performance of the proposed joint optimization method and demonstrate its superiority over several other optimization approaches. We integrate MATLAB with SUMO [66], a well-known microscopic traffic simulator, to develop a simulation environment. Specifically, we utilize real traffic data from the city of Bologna to emulate ground traffic flows in a real-world road traffic scenario [67]. Fig. 2 illustrates the local road network and a UAVâs source and destination. Table I presents the primary parameters related to the UAV mobility [40].

<!-- image-->  
Fig. 2. A local road traffic network in the city of Bologna. In this scenario, the UAV, operating within constraints of limited energy and computing resources, optimizes its motion through acceleration control. Concurrently, it manages bandwidth allocation and offloading time among numerous ground vehicles, guided by the optimal resource allocation strategy derived from our joint optimization algorithm. At the user end, ground vehicles adapt their transmission power and effectively allocate data bits for offloading within designated time intervals, aligning with the optimal power and data partition strategies facilitated by our optimization algorithm. In this manner, both the aerial edge node and ground nodes contribute to enhancing overall system performance within the confines of resource limitations.

TABLE I  
PARAMETERS RELATED TO UAV MOBILITY
<table><tr><td>Parameter</td><td>Value</td><td>Parameter</td><td>Value</td></tr><tr><td> $[ \pmb { a } _ { \mathrm { m i n } } , \pmb { a } _ { \mathrm { m a x } } ]$ </td><td> $[ - 5 , 5 ] ( \mathrm { m } / \mathrm { s } ^ { 2 } )$ </td><td>g</td><td> $\overline { { 9 . 8 \mathrm { m } / \mathrm { s } ^ { 2 } } }$ </td></tr><tr><td> $[ \boldsymbol { v } _ { \mathrm { m i n } } , \boldsymbol { v } _ { \mathrm { m a x } } ]$ </td><td> $[ - 3 0 , 3 0 ] ( \mathrm { m / s } )$ </td><td>â³t</td><td>1s</td></tr><tr><td> $[ x _ { \mathrm { m i n } } , x _ { \mathrm { m a x } } ]$ </td><td>[300,800](m)</td><td> $\theta _ { 3 }$ </td><td>0.0037</td></tr><tr><td> $[ y _ { \mathrm { m i n } } , y _ { \mathrm { m a x } } ]$ </td><td>[50,300] (m)</td><td> $\theta _ { 4 }$ </td><td>500.206</td></tr></table>

TABLE II

PARAMETERS RELATED TO ALGORITHM DESIGN
<table><tr><td>Parameter</td><td>Value</td><td>Parameter</td><td>Value</td></tr><tr><td> $E _ { \mathrm { p r o , m a x } }$ </td><td> $\mathrm { 3 . 0 \times 1 0 ^ { 3 } J }$ </td><td> $E _ { i , \mathrm { m a x } }$ </td><td>10J</td></tr><tr><td> $f _ { \mathrm { m a x } }$ </td><td> $2 . 2 \mathrm { G H z }$ </td><td> $C _ { i }$ </td><td>45 Mbit</td></tr><tr><td> $H _ { \mathrm { U A V } }$ </td><td>50m</td><td> $C _ { \sigma }$ </td><td>1.5</td></tr><tr><td> $\varepsilon _ { 1 }$ </td><td> $1 . 0 \times 1 0 ^ { - 4 }$ </td><td> $\varepsilon _ { 2 }$ </td><td>0.8</td></tr></table>

The required number of CPU cycles for processing per bit data of ground vehicle $i , \varpi _ { i }$ , is uniformly generated within $[ 1 \times 1 0 ^ { 3 } , 2 \times 1 0 ^ { 3 } ]$ (cycle/bit) once before simulation and fixed [1 10 2 10 ]during each simulation experiment. The values of $\varpi _ { i }$ with $i \in \mathcal { T }$ are randomly changed during different sets of experiments. We refer to [61] to specify the approximate first-order marcum Q-functions as follows

$$
\begin{array} { c } { { b _ { 1 } ( \mu _ { 1 } ) = 2 . 1 7 4 - 0 . 5 9 2 \mu _ { 1 } + 0 . 5 9 3 \mu _ { 1 } ^ { 2 } } } \\ { { { } } } \\ { { - 0 . 0 9 2 \mu _ { 1 } ^ { 3 } + 0 . 0 0 5 \mu _ { 1 } ^ { 4 } , } } \end{array}\tag{73}
$$

$$
\begin{array} { c } { { b _ { 2 } ( \mu _ { 1 } ) = \mathrm { ~ - ~ } 0 . 8 4 0 + 0 . 3 2 7 \mu _ { 1 } - 0 . 7 4 0 \mu _ { 1 } ^ { 2 } } } \\ { { { } } } \\ { { + 0 . 0 8 3 \mu _ { 1 } ^ { 3 } - 0 . 0 0 4 \mu _ { 1 } ^ { 4 } . } } \end{array}\tag{74}
$$

The entire simulation duration spans 50 seconds, and some other parameters are given in Table II. The remaining LoS and NLoS channel characteristics and communication parameters are presented in Table III, as referenced in [46], [68], [69].

TABLE III  
PARAMETERS ASSOCIATED WITH CHANNEL AND COMMUNICATION
<table><tr><td>Parameter</td><td>Value</td><td>Parameter</td><td>Value</td></tr><tr><td>s</td><td> $\overline { { 1 \times 1 0 ^ { - 2 8 } } }$ </td><td>B</td><td>1 MHz</td></tr><tr><td> $\theta _ { 1 }$ </td><td> $^ \mathrm { 1 1 . 9 5 }$ </td><td> $K _ { \mathrm { R i c i a n } }$ </td><td>10</td></tr><tr><td> $\theta _ { 2 }$ </td><td>0.14</td><td> $\sigma _ { l } ^ { 2 }$ </td><td>-103dBm</td></tr><tr><td> $[ p _ { i , \mathrm { m i n } } , p _ { i , \mathrm { m a x } } ]$ </td><td>[0,30] (dBm)</td><td> $G _ { l }$ </td><td>-60dB</td></tr><tr><td> $\beta _ { \mathrm { L o S } }$ </td><td>2</td><td> $\beta _ { \mathrm { N L o S } }$ </td><td>2.7</td></tr></table>

<!-- image-->  
Fig. 3. Comparison of the UAVâs trajectories at different altitudes.

## B. Method Validation

To validate the algorithm performance, we vary the altitude of the UAV, denoted by $H _ { \mathrm { U A V } }$ , from to with an in-10 m 100 mcrement of . Fig. 3 presents the UAVâs trajectories obtained 10 musing our joint optimization method under different altitudes. The line plots shown at $z = 0$ correspond to the trajectories = 0 mof various ground vehicles, and the color intensity of each line represents the speed of a node at a spatial location. Fig. 3 illustrates that when the UAVâs altitude is below , it moves 90 mcloser to the ground vehicles on the bottom road to ensure reliable ground-to-air communication. Simultaneously, it maintains connectivity with the vehicles on the top road. However, as the altitude reaches $z = 1 0 0 \mathrm { m }$ , the UAV adjusts its trajectory by = 100 mmoving closer to the top road in order to remain connected with the ground vehicles there. The underlying reason is that the link distance between the UAV and the ground vehicles on the top road increases more rapidly. This adjustment compensates for the more pronounced degradation of link reliability among the top road vehicles when the UAV operates at higher altitudes. Consequently, the UAV guarantees uninterrupted and stable communication with all ground vehicles on both roads.

Fig. 4 displays the convergence of the implemented algorithm across various altitudes. We observe that the average communication reliability stabilizes within a limited number of iterations at each altitude setting. Moreover, the optimal communication reliability increases as the altitude decreases. This trend arises from the UAVâs closer proximity to the ground vehicles when operating at lower altitudes, resulting in enhanced communication reliability.

<!-- image-->  
Fig. 4. Algorithm convergence performance.

## C. Performance Comparison

We compare our method with a benchmark scheme that focuses solely on UAV trajectory optimization (TO) [45]. Additionally, we evaluate our approach against several advanced schemes: i) Joint Trajectory and Time Allocation Optimization (TKO), which optimizes both UAV motion and the offloading time allocation for ground users, similar to the method in [38]; ii) Joint Trajectory and Bandwidth Allocation Optimization (TLO), which optimizes both UAV motion and the bandwidth allocation for ground users [55]; iii) Joint Trajectory and Power Optimization (TPO), which adjusts the transmission power of ground users in conjunction with UAV trajectory optimization [32]; iv) Joint Trajectory and Resource Optimization (TKLPO), which considers transmission power, bandwidth, and offloading time allocations while optimizing UAV trajectory [25], [31], [40]. To facilitate a clear comparison between our proposed method and the comparison methods, we have included two tables in the supplementary material. Table S.1 outlines the differences in optimization focus, while Table S.2 highlights the distinctions in algorithm design.

Recall that $\operatorname* { P r } _ { i } ( k )$ represents the probability of vehicle i suc-( )cessfully offloading its data piece, $u _ { i } [ k ]$ , to the UAV for remote processing in time interval k. Since $\operatorname* { P r } _ { i } ( k ) \in [ 0 , 1 ]$ , there exists a positive real number, $n _ { i } ( k )$ , such that $\mathrm { P r } _ { i } ( k ) \bar { = } \dot { 1 } - 1 0 ^ { - n _ { i } ( k ) }$ The exponent $n _ { i } ( k ) = - \log _ { 1 0 } ( 1 - n _ { i } ( k ) )$ ( ) = 1 10is a monotone increasing function of $\operatorname* { P r } _ { i } ( k )$ og (1 ( )), which is utilized as a performance ( )indicator to demonstrate the time-varying communication reliability for computation offloading. Fig. 6 shows the performance of the computation offloading links between four ground vehicles and the UAV. The flight height of the UAV is fixed at $H _ { \mathrm { U A V } } = 5 0 \mathrm { m }$ . Fig. 5 illustrates the LoS and NLoS probabilities = 50 mof each communication link under different methods. We observe that LoS propagation predominates most of the time, and the compared methods display distinct dynamics in LoS and NLoS propagation probabilities. This contrast is particularly noticeable in Link #1. The discrepancy arises from the fact that these methods yield different UAV trajectories, resulting in greater variation in the distance of Link #1 as the UAV follows different trajectories. Additionally, Fig. 5 shows that the link probability curves experience some inflection points. The main reason is that the channel state of each link transits between the LoS propagation and the NLoS propagation. The transition probabilities of different links are dependent on the time-varying relative distances between the ground vehicles and the UAV as indicated by (8) and (10). When the LoS propagation dominates the communication link (e.g., Link #2), the LoS probability dramatically increases, while the NLoS probability decreases. Conversely, increasing relative link distance can lead to an increase in the NLoS probability and a reduction in the LoS probability, as shown in Link #1. These figures implicitly demonstrate the significant impact of the mobility of ground and aerial nodes on the characteristics of the links.

<!-- image-->

<!-- image-->  
(b) Link #2

<!-- image-->

<!-- image-->  
Fig. 5. Time-varying LoS and NLoS probabilities of individual links.

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
Fig. 6. Time-varying communication reliability of individual links.

<!-- image-->  
Fig. 7. Performance comparison under different altitudes.

Furthermore, Fig. 6 shows the time-varying reliability of various links under different methods. It can be observed that there are several inflection points in the curve of each methodâs exponent value. The underlying reason is that each method modifies the UAVâs acceleration, as well as the resource and bit allocations across different time intervals. When the communication link is allocated with more bandwidth or less data load, and the link distance decreases, the probability that a ground vehicle succeeds in offloading its computation in a time interval rises from a low point to a high one. Conversely, the success probability drops from a high point to a low one when the communication link becomes unreliable for realizing computation offloading. By comparison, our method, as well as the TPO and TKLPO schemes, maintains an exponent value of over 2.5 for each computation offloading link throughout the flight. This indicates that the success probability of computation offloading for the vehicles is guaranteed to be higher than $1 - 1 0 ^ { - 2 . 5 } \approx 0$ .9968 1 10 0 9968on average. From Fig. 6(a) and (b), it is evident that our method outperforms the others regarding the reliability of vehicle 1 and 2 most of the time. However, TPO occasionally achieves a higher exponent value for vehicles 3 and 4, as shown in Fig. 6(c) and (d). None of the methods can achieve the highest reliability for all individual users at all times. Nonetheless, our method, TPO, and TKLPO schemes experience less fluctuation in individual communication reliability than the other schemes.

Fig. 7 compares the average communication reliability of the system at different altitudes. Our method exhibits the highest communication reliability among the methods when considering the overall performance of the ground vehicles. Specifically, at $H _ { \mathrm { U A V } } = 9 0 \mathrm { m }$ and  , our method provides a significantly higher reliability guarantee in comparison with both the TPO and TKLPO schemes. At these altitude settings, our method achieves an average performance that is 17.82% and 64.89% higher than TPO and TKLPO, respectively. The primary reason is that our method can optimize not only the resource allocation and the UAVâs trajectory but also adapt the data partition for computation offloading.

<!-- image-->  
Fig. 8. Performance comparison under different computing demands.

<!-- image-->  
Fig. 9. Performance comparison under different computing energy allocations.

Fig. 8 illustrates the average communication reliability under different offloading demands of ground vehicles. It is observed that an increase in the volume of each vehicleâs application data offloaded to the UAV results in a degradation of communication reliability. This outcome is expected because a higher communication load increases the likelihood of communication link failure during the offloading of the entire application data. Specifically, the reliability performance sharply decreases when the offloading demand, $C _ { i } .$ , increases from 40 Mbit to 70 Mbit. However, in such a scenario, our joint optimization method can provide the best reliability performance. In particular, our method achieves approximately 19.54% and 10.36% higher communication reliability than the TLO and TPO schemes, respectively.

To show the impact of computing resource allocation, we evaluate the reliability performance under different computing energy budget, $E _ { c , \mathrm { m a x } }$ . Fig. 9 illustrates that the TO, TLO, and TPO schemes exhibit low sensitivity to changes in the computing energy budget. This lack of sensitivity stems from the fact that these solutions do not aim to optimize the decision variables associated with the UAVâs computing energy consumption, namely $\{ \kappa [ k ] , k = 1 , 2 , \ldots , T \}$ . In these compared methods, Îº[ ] = 1 2the time allocation ratios are set to 0.5, indicating that they allocate equal time for both computation offloading and processing. In comparison, increasing the computing energy resource can enhance reliability performance in the other methods. Our proposed method and the TKLPO scheme achieve comparable communication reliability, resulting in an average improvement of 27.42% over the TKO scheme.

<!-- image-->  
Fig. 10. Performance comparison under different offloading energy allocations.

Fig. 10 depicts the impact of the offloading energy budget, $E _ { i , \mathrm { m a x } }$ , on the average communication reliability. It can be observed that changes in the energy budget do not affect the TO and TLO schemes. This is because their decision variables do not consider communication energy consumption. By contrast, increasing the offloading energy resource can enhance the performance of other methods, including TKO, TPO, and TKLPO. In comparison, our joint optimization method achieves the highest reliability performance. Specifically, when the offloading energy budget is below . , our method guarantees a reliability 5 0 Jperformance above 0.66, which is significantly higher than the performance of the TKO, TPO, and TKLPO methods.

We also investigate the impact of the number of ground vehicles and the energy reserved for UAV motion. Fig. 11 compares the average communication reliability of different methods under various numbers of ground vehicles. It can be observed that more vehicles can reduce the system reliability since the bandwidth and time resources allocated per vehicle decrease. However, our method achieves the highest average communication reliability. Furthermore, the reliability performance under different UAV propulsion energy budgets is presented in Fig. 12. Except for TLO, increasing the propulsion energy budget enables the UAV to adjust its trajectory with greater flexibility, resulting in improved reliability for ground vehiclesâ computation offloading. The average reliability of TLO fluctuates around 0.7 due to numerical instability. However, it can offer a performance gain over the TO and TKO methods.

<!-- image-->  
Fig. 11. Performance comparison under different numbers of ground vehicles.

<!-- image-->  
Fig. 12. Performance comparison under different propulsion energy budgets.

This suggests that the UAV can derive greater benefits from the joint optimization of trajectory and bandwidth allocation compared to optimizing only the trajectory or jointly optimizing the trajectory and time allocation. By comparison, our method outperforms the TPO and TKLPO schemes by 5.5% and 3.9%, respectively. These reliability performance gains demonstrate that joint data transmission scheduling, resource allocation, and motion control can benefit the UAV-assisted edge computing system.

## VI. CONCLUSION AND FUTURE WORK

In this paper, we present a joint optimization model for UAVassisted edge computing systems. Our objective is to maximize the system reliability when ground users offload their application data to a UAV for remote processing. Specifically, we derive a closed-form expression of the system reliability that captures the characteristics of both LoS and NLoS communication links. The reliability formulation also incorporates upper-layer application data bit allocation, bandwidth and offloading time resource allocations, as well as the mobility of the node. This comprehensive formulation leads to a novel objective for joint optimization that goes beyond resource allocation, integrating user data transmission scheduling and UAV motion control within a unified optimization framework. To solve the problem, we propose a low-complexity optimization algorithm. This algorithm leverages augmented Lagrangian multipliers, enabling the utilization of legacy unconstrained optimization techniques and demonstrating well-guaranteed convergence performance. Simulation results validate the effectiveness of the proposed method, highlighting its superior performance in comparison with several existing schemes in terms of enhancing system reliability. For future work, the system model will be extended to encompass a UAV swarm-cooperative scenario and jointly optimize the utilization rates of resources across multiple UAVmounted cloudlets.

## REFERENCES

[1] J. Zhou, D. Tian, Y. Yan, X. Duan, and X. Shen, âJoint optimization of mobility and reliability-guaranteed air-to-ground communication for UAVs,â IEEE Trans. Mobile Comput., vol. 23, no. 1, pp. 566â580, Jan. 2024.

[2] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surv. Tut., vol. 21, no. 3, pp. 2334â2360, Third Quarter 2019.

[3] W. Khawaja, I. Guvenc, D. W. Matolak, U.-C. Fiebig, and N. Schneckenburger, âA survey of air-to-ground propagation channel modeling for unmanned aerial vehicles,â IEEE Commun. Surv. Tut., vol. 21, no. 3, pp. 2361â2391, Third Quarter 2019.

[4] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[5] M. M. Azari, F. Rosas, K.-C. Chen, and S. Pollin, âUltra reliable UAV communication using altitude and cooperation diversity,â IEEE Trans. Commun., vol. 66, no. 1, pp. 330â344, Jan. 2018.

[6] R. Chen et al., âJoint channel access and power control optimization in large-scale UAV networks: A hierarchical mean field game approach,â IEEE Trans. Veh. Technol., vol. 72, no. 2, pp. 1982â1996, Feb. 2023.

[7] Z. Liu, X. Liu, V. C. M. Leung, and T. S. Durrani, âEnergy-efficient resource allocation for Dual-NOMA-UAV assisted Internet of Things,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 3532â3543, Mar. 2023.

[8] L. Wang, K. Wang, C. Pan, and N. Aslam, âJoint trajectory and passive beamforming design for intelligent reflecting surface-aided UAV communications: A deep reinforcement learning approach,â IEEE Trans. Mobile Comput., vol. 22, no. 11, pp. 6543â6553, Nov. 2023.

[9] A. Al-Hilo, M. Samir, C. Assi, S. Sharafeddine, and D. Ebrahimi, âUAVassisted content delivery in intelligent transportation systems-joint trajectory planning and cache management,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 8, pp. 5155â5167, Aug. 2021.

[10] N. Qi, Z. Huang, W. Sun, S. Jin, and X. Su, âCoalitional formationbased group-buying for UAV-enabled data collection: An auction game approach,â IEEE Trans. Mobile Comput., vol. 22, no. 12, pp. 7420â7437, Dec. 2023.

[11] R. Chai, Y. Gao, R. Sun, L. Zhao, and Q. Chen, âTime-oriented joint clustering and UAV trajectory planning in UAV-assisted WSNs: Leveraging parallel transmission and variable velocity scheme,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 11, pp. 12092â12106, Nov. 2023.

[12] C. Hao, Y. Chen, Z. Mai, G. Chen, and M. Yang, âJoint optimization on trajectory, transmission and time for effective data acquisition in UAVenabled IoT,â IEEE Trans. Veh. Technol., vol. 71, no. 7, pp. 7371â7384, Jul. 2022.

[13] J. Ji, K. Zhu, and L. Cai, âTrajectory and communication design for cache-enabled UAVs in cellular networks: A deep reinforcement learning approach,â IEEE Trans. Mobile Comput., vol. 22, no. 10, pp. 6190â6204, Oct. 2023.

[14] N. Ye, L. Chen, Q. Ouyang, and J. An, âTime-efficient data download for emergency UAV: Joint optimization of on-board computation and communication under energy constraint,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13718â13722, Oct. 2023.

[15] J. Li et al., âJoint optimization of relay selection and transmission scheduling for UAV-aided mmWave vehicular networks,â IEEE Trans. Veh. Technol., vol. 72, no. 5, pp. 6322â6334, May 2023.

[16] L. Sun, L. Wan, J. Wang, L. Lin, and M. Gen, âJoint resource scheduling for UAV-enabled mobile edge computing system in Internet of Vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 12, pp. 15624â15632, Dec. 2023.

[17] S. Tong, Y. Liu, J. MiÅ¡iÂ´c, X. Chang, Z. Zhang, and C. Wang, âJoint task offloading and resource allocation for fog-based intelligent transportation systems: A UAV-enabled multi-hop collaboration paradigm,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 11, pp. 12933â12948, Nov. 2023.

[18] S. Han, K. Zhu, M. Zhou, and X. Liu, âJoint deployment optimization and flight trajectory planning for UAV assisted IoT data collection: A bilevel optimization approach,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 11, pp. 21492â21504, Nov. 2022.

[19] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[20] N. N. Ei, M. Alsenwi, Y. K. Tun, Z. Han, and C. S. Hong, âEnergy-efficient resource allocation in Multi-UAV-Assisted two-stage edge computing for beyond 5G networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 16421â16432, Sep. 2022.

[21] J. Zhou, D. Tian, G. Qu, Z. Sheng, X. Duan, and V. C. M. Leung, âEnergy-efficiency optimization with model convexification for wireless ad hoc networks with multi-packet reception capability,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2864â2881, Apr. 2024.

[22] J. Zhou, D. Tian, Z. Sheng, X. Duan, and X. Shen, âJoint mobility, communication and computation optimization for UAVs in air-ground cooperative networks,â IEEE Trans. Veh. Technol., vol. 70, no. 3, pp. 2493â2507, Mar. 2021.

[23] W. C. Ng et al., âStochastic resource optimization for wireless powered hybrid coded edge computing networks,â IEEE Trans. Mobile Comput., vol. 23, no. 3, pp. 2022â2038, Mar. 2024.

[24] Y. Liang, L. Xiao, D. Yang, Y. Liu, and T. Zhang, âJoint trajectory and resource optimization for UAV-aided two-way relay networks,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 639â652, Jan. 2022.

[25] H. Hu, Z. Chen, F. Zhou, Z. Han, and H. Zhu, âJoint resource and trajectory optimization for heterogeneous-UAVs enabled aerial-ground cooperative computing networks,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 8812â8826, Jul. 2023.

[26] M. Li, X. Tao, H. Wu, and N. Li, âJoint trajectory and resource optimization for covert communication in UAV-enabled relaying systems,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 5518â5523, Apr. 2023.

[27] M. Dai, T. H. Luan, Z. Su, N. Zhang, Q. Xu, and R. Li, âJoint channel allocation and data delivery for UAV-assisted cooperative transportation communications in post-disaster networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 16676â16689, Sep. 2022.

[28] X. Liu, B. Lai, B. Lin, and V. C. M. Leung, âJoint communication and trajectory optimization for Multi-UAV enabled mobile Internet of Vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 15354â15366, Sep. 2022.

[29] C. Dai, K. Zhu, and E. Hossain, âMulti-agent deep reinforcement learning for joint decoupled user association and trajectory design in full-duplex multi-UAV networks,â IEEE Trans. Mobile Comput., vol. 22, no. 10, pp. 6056â6070, Oct. 2023.

[30] J. Ji, L. Cai, K. Zhu, and D. Niyato, âDecoupled association with rate splitting multiple access in UAV-assisted cellular networks using multiagent deep reinforcement learning,â IEEE Trans. Mobile Comput., vol. 23, no. 3, pp. 2186â2201, Mar. 2024.

[31] Y. Liu et al., âJoint communication and computation resource scheduling of a UAV-assisted mobile edge computing system for platooning vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 8435â8450, Jul. 2022.

[32] Y. Wu, W. Yang, X. Guan, and Q. Wu, âUAV-enabled relay communication under malicious jamming: Joint trajectory and transmit power optimization,â IEEE Trans. Veh. Technol., vol. 70, no. 8, pp. 8275â8279, Aug. 2021.

[33] Y. Guo, S. Yin, and J. Hao, âJoint placement and resources optimization for multi-user UAV-relaying systems with underlaid cellular networks,â IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 12374â12377, Oct. 2020.

[34] M. Asim, M. ELAffendi, and A. A. A. El-Latif, âMulti-IRS and multi-UAV-assisted mec system for 5G/6G networks: Efficient joint trajectory optimization and passive beamforming framework,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 4, pp. 4553â4564, Apr. 2023.

[35] J. Chen et al., âJoint channel and link selection in formation-keeping UAV networks: A two-way consensus game,â IEEE Trans. Mobile Comput., vol. 21, no. 8, pp. 2861â2875, Aug. 2022.

[36] D. Guo, L. Tang, X. Zhang, and Y.-C. Liang, âJoint optimization of trajectory and jamming power for multiple UAV-aided proactive eavesdropping,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 5770â5785, May 2024.

[37] F. Zhou, Y. Wu, R. Q. Hu, and Y. Qian, âComputation rate maximization in UAV-enabled wireless-powered mobile-edge computing systems,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1927â1941, Sep. 2018.

[38] S. Bi and Y. J. Zhang, âComputation rate maximization for wireless powered mobile-edge computing with binary computation offloading,â IEEE Trans. Wireless Commun., vol. 17, no. 6, pp. 4177â4190, Jun. 2018.

[39] F. Wang, J. Xu, X. Wang, and S. Cui, âJoint offloading and computing optimization in wireless powered mobile-edge computing systems,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 1784â1797, Mar. 2018.

[40] M. Li, N. Cheng, J. Gao, Y. Wang, L. Zhao, and X. Shen, âEnergy-efficient UAV-assisted mobile edge computing: Resource allocation and trajectory optimization,â IEEE Trans. Veh. Technol., vol. 69, no. 3, pp. 3424â3438, Mar. 2020.

[41] J. Zhou, D. Tian, Y. Wang, Z. Sheng, X. Duan, and V. C. Leung, âReliability-optimal cooperative communication and computing in connected vehicle systems,â IEEE Trans. Mobile Comput., vol. 19, no. 5, pp. 1216â1232, May 2020.

[42] S. Sekander, H. Tabassum, and E. Hossain, âStatistical performance modeling of solar and wind-powered UAV communications,â IEEE Trans. Mobile Comput., vol. 20, no. 8, pp. 2686â2700, Aug. 2021.

[43] Z. Dai, C. H. Liu, R. Han, G. Wang, K. K. Leung, and J. Tang, âDelaysensitive energy-efficient UAV crowdsensing by deep reinforcement learning,â IEEE Trans. Mobile Comput., vol. 22, no. 4, pp. 2038â2052, Apr. 2023.

[44] J. Ji, K. Zhu, D. Niyato, and R. Wang, âJoint trajectory design and resource allocation for secure transmission in cache-enabled UAV-relaying networks with D2D communications,â IEEE Internet Things J., vol. 8, no. 3, pp. 1557â1571, Feb. 2021.

[45] Y. Zeng and R. Zhang, âEnergy-efficient UAV communication with trajectory optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 6, pp. 3747â3760, Jun. 2017.

[46] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal lap altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[47] H. Wu, X. Tao, N. Zhang, and X. Shen, âCooperative UAV cluster-assisted terrestrial cellular networks for ubiquitous coverage,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 2045â2058, Sep. 2018.

[48] W. Zhang, Y. Wen, K. Guan, D. Kilper, H. Luo, and D. O. Wu, âEnergyoptimal mobile cloud computing under stochastic wireless channel,â IEEE Trans. Wireless Commun., vol. 12, no. 9, pp. 4569â4581, Sep. 2013.

[49] Z. Sheng, C. Mahapatra, V. C. M. Leung, M. Chen, and P. K. Sahu, âEnergy efficient cooperative computing in mobile wireless sensor networks,â IEEE Trans. Cloud Comput., vol. 6, no. 1, pp. 114â126, Jan.-Mar. 2018.

[50] J. Zhou, D. Tian, Y. Wang, Z. Sheng, X. Duan, and V. C. M. Leung, âReliability-oriented optimization of computation offloading for cooperative vehicle-infrastructure systems,â IEEE Signal Process. Lett., vol. 26, no. 1, pp. 104â108, Jan. 2019.

[51] B. Heintz, A. Chandra, R. K. Sitaraman, and J. Weissman, âEnd-to-End optimization for Geo-distributed mapreduce,â IEEE Trans. Cloud Comput., vol. 4, no. 3, pp. 293â306, Jul.-Sep. 2016.

[52] Y. Liu, K. Xiong, Q. Ni, P. Fan, and K. B. Letaief, âUAV-assisted wireless powered cooperative mobile edge computing: Joint offloading, CPU control, and trajectory optimization,â IEEE Internet Things J., vol. 7, no. 4, pp. 2777â2790, Apr. 2020.

[53] L. Xie, J. Xu, and R. Zhang, âThroughput maximization for UAV-enabled wireless powered communication networks,â IEEE Internet Things J., vol. 6, no. 2, pp. 1690â1703, Apr. 2019.

[54] Q. Hu, Y. Cai, G. Yu, Z. Qin, M. Zhao, and G. Y. Li, âJoint offloading and trajectory design for UAV-enabled mobile edge computing systems,â IEEE Internet Things J., vol. 6, no. 2, pp. 1879â1892, Apr. 2019.

[55] X. Hu, K.-K. Wong, K. Yang, and Z. Zheng, âUAV-assisted relaying and edge computing: Scheduling and trajectory optimization,â IEEE Trans. Wireless Commun., vol. 18, no. 10, pp. 4738â4752, Oct. 2019.

[56] T. Zhang, Y. Xu, J. Loo, D. Yang, and L. Xiao, âJoint computation and communication design for UAV-assisted mobile edge computing in IoT,â IEEE Trans. Ind. Inform., vol. 16, no. 8, pp. 5505â5516, Aug. 2020.

[57] J. Ji, K. Zhu, C. Yi, and D. Niyato, âEnergy consumption minimization in UAV-assisted mobile-edge computing systems: Joint resource allocation and trajectory design,â IEEE Internet Things J., vol. 8, no. 10, pp. 8570â8584, May 2021.

[58] D. W. Matolak, âAir-ground channels & models: Comprehensive review and considerations for unmanned aircraft systems,â in Proc. 2012 IEEE Aerosp. Conf., 2012, pp. 1â17.

[59] S. Kandeepan, K. Gomez, L. Reynaud, and T. Rasheed, âAerial-terrestrial communications: Terrestrial cooperation and energy-efficient transmissions to aerial base stations,â IEEE Trans. Aerosp. Electron. Syst., vol. 50, no. 4, pp. 2715â2735, Oct. 2014.

[60] Proakis, Digital Communications 5th ed.. New York, NY, USA: McGraw Hill, 2007.

[61] M. Z. Bocus, C. P. Dettmann, and J. P. Coon, âAn approximation of the first order Marcum Q-function with application to network connectivity analysis,â IEEE Commun. Lett., vol. 17, no. 3, pp. 499â502, Mar. 2013.

[62] A. Filippone, Flight Performance of Fixed and Rotary Wing Aircraft. Oxford, U.K.: Elsevier Butterworth-Heinemann, 2006.

[63] R. Andreani, E. G. Birgin, J. M. MartÃ­nez, and M. L. Schuverdt, âOn augmented Lagrangian methods with general lower-level constraints,â SIAM J. Optim., vol. 18, no. 4, pp. 1286â1309, 2008.

[64] E. G. Birgin and J. M. MartÃ­nez, âComplexity and performance of an augmented Lagrangian algorithm,â Optim. Methods Softw., vol. 35, no. 5, pp. 885â920, 2020.

[65] C. Cartis, N. I. M. Gould, and P. L. Toint, âOn the complexity of steepest descent, Newtonâs and regularized Newtonâs methods for nonconvex unconstrained optimization problems,â SIAM J. Optim., vol. 20, no. 6, pp. 2833â2852, 2010.

[66] P. A. Lopez et al., âMicroscopic traffic simulation using sumo,â in Proc. 21st Int. Conf. Intell. Transp. Syst., 2018, pp. 2575â2582.

[67] L. Bieker, D. Krajzewicz, A. Morra, C. Michelacci, and F. Cartolano, âTraffic simulation for all: A real world traffic scenario from the city of Bologna,â in Modeling Mobility With Open Data. Berlin, Germany: Springer, 2015, pp. 47â60.

[68] C. Zhan, Y. Zeng, and R. Zhang, âEnergy-efficient data collection in UAV enabled wireless sensor network,â IEEE Wireless Commun. Lett., vol. 7, no. 3, pp. 328â331, Jun. 2018.

[69] W. Mei, Q. Wu, and R. Zhang, âCellular-connected UAV: Uplink association, power control and interference coordination,â IEEE Trans. Wireless Commun., vol. 18, no. 11, pp. 5380â5393, Nov. 2019.

<!-- image-->

Jianshan Zhou received the BSc, MSc, and PhD degrees in traffic information engineering and control from Beihang University, Beijing, China, in 2013, 2016, and 2020, respectively. He is an associate professor with the school of transportation science and engineering with Beihang University. From 2017 to 2018, he was a visiting research Fellow with the School of Informatics and Engineering, University of Sussex, Brighton, U.K. He was a postdoctoral research fellow supported by the Zhuoyue Program of Beihang University and the National Postdoctoral

Program for Innovative Talents from 2020 to 2022. He is or was the Technical Program Session Chair with the IEEE EDGE 2020, the IEEE ICUS 2022-2024, the ICAUS 2022, the TPC member with the IEEE VTC2021-Fall track, and the Youth Editorial Board Member of the Uncrewed Systems Technology. He is the author or co-author of more than 50 international scientific publications. His research interests include the modeling and optimization of vehicular communication networks and airâground cooperative networks, the analysis and control of connected autonomous vehicles, and intelligent transportation systems.

<!-- image-->

Mingqian Wang received the BSc degree in transportation engineering from the Shandong University of Technology, Shandong, China, in 2019, the MSc degree from the Beijing University of Technology, Beijing, China, in 2023. He is currently working toward the PhD degree with Beihang University. His research interests include uncrewed systems, dynamics modeling and control, and distributed optimization.

<!-- image-->

Daxin Tian (Fellow, IEEE) received the PhD degree in computer application technology from Jilin University, Changchun, China, in 2007. He is currently a professor with the School of Transportation Science and Engineering, Beihang University, Beijing, China. His research interest include intelligent transportation systems, autonomous connected vehicles, swarm intelligent and mobile computing. He was the recipient of the Changjiang Scholars Program (Young Scholar) of Ministry of Education of China, in 2017, National Science Fund for Distinguished Young Scholars in

<!-- image-->

Xuting Duan received the PhD degree in traffic information engineering and control from Beihang University, Beijing, China, in 2017. He is currently an associate professor with the School of Transportation Science and Engineering, Beihang University. His current research interests are focused on vehicular ad hoc networks and autonomous systems.

2018, and Distinguished Young Investigator of China Frontiers of Engineering, in 2018. He was the Technical Program Committee Member/Chair/Co-Chair for several international conferences which include EAI 2018, ICTIS 2019, IEEE ICUS 2019, IEEE HMWC 2020, and GRAPH-HOC 2020.

<!-- image-->

Kaige Qu (Member, IEEE) received the BS degree in communication engineering from Shandong University, Jinan, China, in 2013, the MS degree in integrated circuits engineering and electrical engineering from Tsinghua University, Beijing, China, and KU Leuven, Leuven, Belgium, in 2016, and the PhD degree in electrical and computer engineering from the University of Waterloo, Waterloo, Canada, in 2021. Since February 2021, she has been a post-doctoral fellow with the Department of Electrical and Computer Engineering, University of Waterloo. She is currently an associate professor with the school of transportation science and engineering with Beihang University. Her research interests include network slicing, edge intelligence, machine learning for wireless networks, connected autonomous vehicles, and digital twin assisted network automation.

<!-- image-->

Guixian Qu received the BSc degree in transportation engineering from the Shandong University of Technology, Shandong, China, in 2012, the MSc and PhD degrees from the Beijing University of Technology, Beijing, China, in 2014 and 2019, respectively. She is currently a research fellow of Research Institute of Aero-Engine, Beihang University. Her research interests include uncrewed systems, dynamics modeling and control, and distributed optimization.

<!-- image-->

Xuemin (Sherman) Shen (Fellow, IEEE) received the PhD degree in electrical engineering from Rutgers University, New Brunswick, NJ, USA, in 1990. He is an University Professor with the Department of Electrical and Computer Engineering, University of Waterloo, Canada. His research interests include network resource management, wireless network security, the Internet of Things, 5G and beyond, and vehicular ad hoc and sensor networks. He is a registered Professional Engineer of Ontario, Canada; a fellow of the Engineering Institute of Canada, the Canadian

Academy of Engineering, and the Royal Society of Canada; a Foreign Member of the Chinese Academy of Engineering; and a Distinguished Lecturer of the IEEE Vehicular Technology Society and the IEEE Communications Society. He received the Premierâs Research Excellence Award (PREA) from the Province of Ontario, Canada, in 2003, and the Excellent Graduate Supervision Award from the University of Waterloo, in 2006. He has also received the Joseph LoCicero Award, in 2015 and the Education Award, in 2017 from the IEEE Communications Society, the James Evans Avant Garde Award from the IEEE Vehicular Technology Society, in 2018, the R.A. Fessenden Award from IEEE, Canada, in 2019, the Award of Merit from the Federation of Chinese Canadian Professionals (Ontario), in 2019, and the Technical Recognition Award from the AHSN Technical Committee, in 2013 and the Wireless Communications Technical Committee, in 2019. He served as the Technical Program Committee Chair/Co-Chair for IEEE Globecomâ16, IEEE Infocomâ14, IEEE VTCâ10 Fall, and IEEE Globecomâ07, and the Chair for the IEEE Communications Society Technical Committee on Wireless Communications. He is the President of the IEEE Communications Society. He was the vice president for Technical and Educational Activities, the vice president for Publications, a Member-at-Large on the Board of Governors, the Chair of the Distinguished Lecturer Selection Committee, and a member of IEEE Fellow Selection Committee of the ComSoc. He served as the editor-in-chief for the IEEE Internet of Things Journal, IEEE Network, and IET Communications.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_12_img_1.jpeg|page_12_img_1]]
3. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_12_img_2.png|page_12_img_2]]
4. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_17_img_1.jpeg|page_17_img_1]]
5. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_17_img_2.jpeg|page_17_img_2]]
6. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_18_img_1.jpeg|page_18_img_1]]
7. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_18_img_2.jpeg|page_18_img_2]]
8. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_18_img_3.jpeg|page_18_img_3]]
9. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_18_img_4.jpeg|page_18_img_4]]
10. [[../extracted_images/Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control/page_18_img_5.jpeg|page_18_img_5]]

---

