# An Online Joint Optimization Approach for QoE Maximization in UAV-Enabled Mobile Edge Computing

â¡School of Computer Science and Technology, Dalian University of Technology, Dalian 116024, China

wangpf@dlut.edu.cn, liangshuang@nenu.edu.cn, dniyato@ntu.edu.sg

âCorresponding author: Geng Sun

AbstractâGiven flexible mobility, rapid deployment, and low cost, unmanned aerial vehicle (UAV)-enabled mobile edge computing (MEC) shows great potential to compensate for the lack of terrestrial edge computing coverage. However, limited battery capacity, computing and spectrum resources also pose serious challenges for UAV-enabled MEC, which shorten the service time of UAVs and degrade the quality of experience (QoE) of user devices (UDs) without effective control approach. In this work, we consider a UAV-enabled MEC scenario where a UAV serves as an aerial edge server to provide computing services for multiple ground UDs. Then, a joint task offloading, resource allocation, and UAV trajectory planning optimization problem (JTRTOP) is formulated to maximize the QoE of UDs under the UAV energy consumption constraint. To solve the JTRTOP that is proved to be a future-dependent and NP-hard problem, an online joint optimization approach (OJOA) is proposed. Specifically, the JTRTOP is first transformed into a per-slot real-time optimization problem (PROP) by using the Lyapunov optimization framework. Then, a two-stage optimization method based on game theory and convex optimization is proposed to solve the PROP. Simulation results validate that the proposed approach can achieve superior system performance compared to the other benchmark schemes.

## I. INTRODUCTION

W ITH artificial intelligence and wireless communica- tions development, many intelligent applications with strict requirements on computing resources and latency have emerged explosively [1], such as real-time video analysis [2], virtual reality/augmented reality [3], and interactive online games [4]. However, the limited battery capacity and computing capability of user devices (UDs) make it difficult to maintain a high-level quality of experience (QoE) for these intelligent applications [5]. To overcome this challenge, mobile edge computing (MEC) has emerged as a promising paradigm to offer cloud computing resources in close proximity to UDs [6], [7]. Specifically, UDs can offload latency-sensitive and computation-hungry tasks to edge servers to improve the QoE. Equipped with cloud computing capabilities, the edge servers can concurrently provide real-time and energy-efficient computing services for multiple UDs. However, conventional terrestrial MEC still faces the challenges of limited network coverage and high deployment cost due to the dependence on ground infrastructures, especially in remote areas [8].

The limitations of conventional terrestrial MEC have prompted a paradigm shift toward UAV-enabled MEC due to the line-of-sight (LoS) communication, high maneuverability, and flexible deployment of UAVs [9]â[11]. First, the high probability LoS links of UAVs boost the communication coverage, network capacity, and reliable connectivity [12], [13]. Furthermore, their flexible mobility enables rapid and on-demand deployment, especially in distant areas where terrestrial infrastructures are unavailable. Besides, the integration of UAV and MEC offers flexible computing capabilities to improve the QoE of UDs.

However, several fundamental challenges should be overcome to fully exploit the benefits of UAV-enabled MEC. i) Resource Allocation. Various tasks of UDs are generally heterogeneous and time-varying, and they have stringent requirements for the offloading service. However, the limited computing resources and scarce spectrum resources of UAVenabled MEC and the stringent demands of UDs could lead to the competition for resources inside the MEC server, especially during peak times. Thus, under resource constraints, it is challenging for the MEC server to determine an efficient resource allocation strategy to meet the demands of various tasks. ii) Task Offloading. The offloading decision of each UD depends not only on its own offloading demand but also on the offloading decisions of the other UDs, which makes the offloading decisions among UDs coupling and complex. iii) Trajectory Planning. Although the mobility of UAVs increases the flexibility and elasticity of MEC, it also brings significant difficulties in UAV trajectory planning. iv) Energy Constraint. The limited onboard battery capacity of UAVs leads to finite service time, which makes it challenging to balance the service time of UAVs and the QoE of UDs. In addition, under the constraints of UAVâs resources and energy, the resource allocation strategy of UAVs, the task offloading decisions of UDs, and the trajectory planning of UAVs have mutual effects on each other, leading to the complexity of the decision-making process.

To overcome the aforementioned challenges, we propose an online approach for joint optimization of task offloading, resource allocation, and UAV trajectory planning to maximize the QoE of UDs under the UAV energy consumption constraint. The main contributions are summarized as follows:

â¢ System Architecture. We consider a stochastic UAVenabled MEC system with energy and resource constraints consisting of a UAV and multiple ground UDs. Specifically, the UAV is employed as an aerial edge server relying on limited battery capacity, computing and communication resources to provide computing services to UDs with time-varying computation requirements and dynamic mobility.

â¢ Problem Formulation. We formulate a novel joint task offloading, resource allocation, and UAV trajectory planning optimization problem (JTRTOP) with the aim of maximizing the QoE of UDs under the UAV energy consumption constraint. Specifically, the QoE of UDs is theoretically measured by synthesizing the completion delay of the tasks and energy consumption of UDs.

â¢ Algorithm Design. Since the JTRTOP not only requires future information but is also non-convex and NP-hard, we propose an online joint optimization approach (OJOA) to solve the problem. Specifically, we first transform the JTRTOP into a per-slot real-time optimization problem (PROP) by using the Lyapunov optimization framework. Then, we propose a two-stage method to optimize the task offloading, resource allocation, and UAV position of PROP by using convex optimization and game theory.

â¢ Validation. Both theoretical analysis and simulation experiments are performed to verify the effectiveness and performance of the proposed OJOA. Specifically, theoretical analysis demonstrates that the OJOA not only satisfies the UAV energy consumption constraint but also converges to a sub-optimal solution in polynomial time. Moreover, simulation results indicate that the proposed OJOA outperforms other benchmark schemes.

The remainder of the work is organized as follows. Section II summarizes the related work. Section III details the relevant system models and problem formulation. Section IV describes the Lyapunov-based problem transformation. Section V presents the two-stage optimization algorithm and theoretical analysis. In Section VI, simulation results are displayed and analyzed. Finally, Section VII concludes the overall paper.

## II. RELATED WORK

Most existing studies on UAV-enabled MEC are devoted to the design of offline algorithms to plan the entire task offload, resource allocation, and UAV trajectory, which assume that the locations of UDs are invariant and the computing requirements of UDs are fixed or known in advance [14]â[16]. However, many edge computing scenarios change dynamically over time, such as real-time video analysis and interactive online games, which means that the computing tasks arrive stochastically, the computing requirements of UDs are timevarying and the UDs are dynamically mobile. Therefore, it is necessary to design real-time decision-making algorithms without future information.

There are also some works studying real-time decisionmaking. For example, Yang et al. [17] studied the UAVenabled MEC system with random task arrival and user mobility. Specifically, the UAV trajectory and resource allocation were decided in real time to minimize the average energy consumption of all users through online algorithms based on Lyapunov optimization. Considering the time-varying computing requirements of user equipment, Wang et al. [18] jointly optimized the user association, resource allocation and trajectory of UAVs with the aim of minimizing energy consumption of all user equipment. To minimize the average power consumption of the system with randomly arriving user tasks, Hoang et al. [19] developed a Lyapunov-guided deep reinforcement learning framework. Zhou et al. [20] proposed an alternating optimization-based algorithm by leveraging the Lyapunov optimization approach and dependent rounding technique to minimize the service delay.

In practice, due to the limited energy and computing resources of UDs, task completion delay and energy consumption are important indicators to measure the QoE of UDs. However, the abovementioned works mainly focus on minimizing the task completion delay and energy consumption of users (or the whole system) separately, which could not provide a high-level QoE for users. Furthermore, these works consider resource allocation from either the communication or the computation aspects, which may lead to severe performance degradation in practical UAV-enabled MEC systems where both communication and computing resources are insufficient. Motivated by these issues, in this work, we consider a stochastic UAV-enabled MEC system with timevarying computation requirements and dynamic mobility of UDs to minimize the user energy consumption and task completion latency simultaneously. Furthermore, the computing and communication resource allocation are jointly optimized.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

As illustrated in Fig. 1, we considered a UAV-enabled MEC system that consists of a rotary-wing UAV u and M UDs with the set $\mathcal { M } = \{ 1 , 2 , \dots , M \}$ . Equipped with MEC capability, the UAV is employed as an aerial edge server relying on limited battery capacity to provide computing offloading services to the UDs within a finite system timeline. Moreover, we discretize the system timeline into equal T time slots [21], i.e., $t \in \mathcal { T } = \{ 1 , 2 , \dots , T \}$ , wherein each slot duration is denoted as Ï .

## A. Basic Model

UD Model. We assume that each UD generates one computing task per time slot [18], [22]. For $\mathrm { U D } \ m \in { \mathcal { M } } ,$ , the $\mathrm { U D } ^ { \prime } \mathrm { s }$ attributes at time slot t can be characterized as $\mathbf { S } \mathbf { t } _ { m } ^ { \mathrm { U D } } ( t ) =$ $\left( f _ { m } ^ { \mathrm { U D } } , \Phi _ { m } ( t ) , \mathbf { P } _ { m } ( t ) \right)$ , where $f _ { m } ^ { \mathrm { U D } }$ denotes the local computing capability of UD m. The computing task generated by UD m is characterized as $\Phi _ { m } ( t ) ~ = ~ \{ D _ { m } ( t ) , \eta _ { m } ( t ) , T _ { m } ^ { \mathrm { m a x } } ( t ) \}$ at time slot t, wherein $D _ { m } ( t )$ represents the input data size (in bits), $\eta _ { m } ( t )$ denotes the computation intensity (in cycles/bit), and $T _ { m } ^ { \mathrm { m a x } } ( t )$ is the maximum tolerable delay. $\mathbf P _ { m } ( t ) = [ x _ { m } ( t ) , \ddot { y _ { m } } ( t ) ]$ represents the location coordinates of UD m at time slot t. Similar to [23], [24], the mobility of UDs is modeled as a Gauss-Markov mobility model, which is widely employed in cellular communication networks [25]. Specifically, the velocity of UD m at time slot t+1 are updated as follows:

<!-- image-->  
Fig. 1. The UAV-enabled MEC consists a UAV and multiple ground UDs. The UAV provides computing services to UDs by allocating communication and computing resources. Each UD independently decides to compute its task locally or offload the task to the UAV.

$$
\begin{array} { r } { \mathbf { v } _ { m } ( t + 1 ) = \alpha \mathbf { v } _ { m } ( t ) + ( 1 - \alpha ) \overline { { \mathbf { v } } } _ { m } + \sqrt { 1 - \alpha ^ { 2 } } \mathbf { w } _ { m } ( t ) , } \end{array}\tag{1}
$$

where $\mathbf { v } _ { m } ( t ) \ = \ ( v _ { m } ^ { x } ( t ) , v _ { m } ^ { y } ( t ) )$ denotes the velocity vector at time slot t. Î± represents the memory level, which reflects the temporal-dependent degree and $\overline { { \mathbf { v } } } _ { m }$ is the asymptotic means of velocity. $\mathbf { w } _ { m } ( t )$ is the uncorrelated random Gaussian process $N ( 0 , \sigma _ { m } ^ { 2 } )$ , where $\sigma _ { m }$ denotes the asymptotic standard deviation of velocity. Therefore, the mobility of UD m can be updated as follows:

$$
\mathbf P _ { m } ( t + 1 ) = \mathbf P _ { m } ( t ) + \mathbf v _ { m } ( t ) \boldsymbol { \tau } .\tag{2}
$$

UAV Model. UAV u is characterized by $\begin{array} { r l } { \mathbf { S t } ^ { u } ( t ) } & { { } = } \end{array}$ $( \mathbf { P } _ { u } ( t ) , H , F _ { u } ^ { \operatorname* { m a x } } , B )$ , wherein $\mathbf { P } _ { u } ( t ) ~ = ~ \left[ x _ { u } ( t ) , y _ { u } ( t ) \right]$ and H represent the horizontal coordinate and flight height of the UAV at time slot t, respectively. $F _ { u } ^ { \mathrm { m a x } }$ represents the total computing resources and B denotes the total bandwidth resources.

Decision Variables. The following decisions need to be made jointly. i) Task Offloading Decision. For task $\Phi _ { m } ( t )$ we define a binary variable $a _ { m } ( t )$ to represent the offloading decision of UD m at time slot t, where $a _ { m } ( t ) = 0$ indicates that the task is processed locally, and $a _ { m } ( t ) = 1$ indicates that the task is offloaded to the UAV for processing. ii) Resource Allocation Decision. For the UAV, the resources allocated to task $\Phi _ { m } ( t )$ are denoted as $\{ F _ { m } ( t ) , w _ { m } ( t ) \}$ at time slot t, where $F _ { m } ( t )$ is the amount of allocated computing resources and $w _ { m } ( t )$ is the proportion of allocated bandwidth resources. iii) UAV Trajectory Planning. For the UAV, trajectory planning can be expressed as a sequence of optimal positions for each time slot, i.e., $\mathbf { P } _ { u } = \{ \mathbf { P } _ { u } ( t ) \} _ { t \in \mathcal { T } }$

## B. Communication Model

The probabilistic line-of-sight (LoS) channel model is employed to model the communication between the UAV and UDs [26]. First, the LoS probability $P _ { m , u } ^ { \mathrm { L o S } } ( t )$ between UD m and the UAV at time slot t can be defined as [27]

$$
P _ { m , u } ^ { \mathrm { L o S } } ( t ) = \frac { 1 } { 1 + \xi _ { 1 } \exp ( - \xi _ { 2 } ( \theta _ { m , u } ( t ) - \xi _ { 1 } ) ) } ,\tag{3}
$$

where $\xi _ { 1 }$ and $\xi _ { 2 }$ are constants depending on the propagation environment, $\theta _ { m , u } ( t ) ~ = ~ \frac { 1 8 0 } { \pi }$ arcsin $\frac { H } { d _ { m , u } ( t ) }$ denotes the elevation angle and $d _ { m , u } ( t )$ represents the straight-line distance between UD m and the UAV. Similar to [17], [28], the channel power gain can be calculated as

$$
\begin{array} { r l r } {  { g _ { m , u } ( t ) = P _ { m , u } ^ { \mathrm { L o S } } ( t ) \beta _ { 0 } d _ { m , u } ^ { - \tilde { \mu } } ( t ) + ( 1 - P _ { m , u } ^ { \mathrm { L o S } } ( t ) ) \kappa \beta _ { 0 } d _ { m , u } ^ { - \tilde { \mu } } ( t ) } } \\ & { } & { = \tilde { P } _ { m , u } ^ { \mathrm { L o S } } ( t ) \beta _ { 0 } d _ { m , u } ^ { - \tilde { \mu } } ( t ) , } \end{array}\tag{4}
$$

where $\tilde { P } _ { m , u } ^ { \mathrm { L o S } } ( t ) \triangleq P _ { m , u } ^ { \mathrm { L o S } } ( t ) + ( 1 - P _ { m , u } ^ { \mathrm { L o S } } ( t ) ) \kappa _ { \mathrm { r } }$ Îº is the additional attenuation factor, $\beta _ { 0 }$ denotes the channel gain at the reference distance 1 m, and ÂµË is the path loss exponent. Therefore, the spectral efficiency of UD m can be expressed as

$$
r _ { m , u } ( t ) = \log _ { 2 } \left( 1 + \frac { \phi _ { m } ( t ) } { ( | | \mathbf { P } _ { u } ( t ) - \mathbf { P } _ { m } ( t ) | | ^ { 2 } + H ^ { 2 } ) ^ { \mu } } \right) ,\tag{5}
$$

where $\begin{array} { r } { \phi _ { m } ( t ) = \frac { P _ { m } \beta _ { 0 } \tilde { P } _ { m , u } ^ { \mathrm { L o S } } ( t ) } { N _ { \mathrm { 0 } } } , \mu = \frac { \tilde { \mu } } { 2 } , P _ { m } } \end{array}$ is the transmission power of UD m, and ${ \check { N } } _ { 0 }$ represents the noise power.

Moreover, the widely used orthogonal frequency-division multiple access (OFDMA) is employed in the communication models. Therefore, the communication rate of UD m at time slot t can be presented as [29]

$$
R _ { m , u } ( t ) = w _ { m } ( t ) B r _ { m , u } ( t ) ,\tag{6}
$$

## C. Computation Model

For task $\Phi _ { m } ( t )$ generated by UD m, the task can be processed either locally on the UD or remotely on the UAV, which is determined by the UDâs offloading decision $a _ { m } ( t )$

Local Computing. UD m processes task $\Phi _ { m } ( t )$ locally (i.e., $a _ { m } ( t ) = 0 )$ . The local completion latency of the task at time slot t can be calculated as

$$
T _ { m } ^ { \mathrm { l o c } } ( t ) = \frac { \eta _ { m } ( t ) D _ { m } ( t ) } { f _ { m } ^ { \mathrm { U D } } } ,\tag{7}
$$

Accordingly, the energy consumption of UD m to execute task $\Phi _ { m } ( t )$ locally at time slot t is calculated as [15]

$$
E _ { m } ^ { \mathrm { l o c } } ( t ) = k ( f _ { m } ^ { \mathrm { U D } } ) ^ { 3 } T _ { m } ^ { \mathrm { l o c } } ( t ) ,\tag{8}
$$

where k denotes the effective switched capacitance cofficient that depends on the hardware architecture of the UD.

Edge Computing. Task $\Phi _ { m } ( t )$ is offloaded to the UAV for processing $( \mathrm { i } . \mathrm { e } . , a _ { m } ( t ) = 1 )$ . In this case, the UAV allocates computing and communication resources to perform the task. The edge processing delay includes transmission delay and edge execution delay, which can be calculated as

$$
T _ { m } ^ { \mathrm { e c } } ( t ) = \frac { D _ { m } ( t ) } { R _ { m , u } ( t ) } + \frac { \eta _ { m } ( t ) D _ { m } ( t ) } { F _ { m } ( t ) } .\tag{9}
$$

The energy consumption generated by processing the task at time slot t consists of the transmission energy consumption of UD m and the computation energy consumption of the UAV. The transmission energy consumption of UD m at time slot t can be calculated as

$$
\begin{array} { c c c } { \displaystyle { \big | E _ { m } ^ { \mathrm { e c } } ( t ) = P _ { m } \frac { D _ { m } ( t ) } { R _ { m , u } ( t ) } . } } \end{array}\tag{10}
$$

Then, the computation energy consumption of the UAV to execute task $\Phi _ { m } ( t )$ can be given as [22]

$$
\begin{array} { r } { E _ { m , u } ^ { \mathrm { c } } ( t ) = \varpi \eta _ { m } ( t ) D _ { m } ( t ) . } \end{array}\tag{11}
$$

where Ï represents the UAV energy consumption per unit CPU cycle. Therefore, the total computation energy consumption of the UAV at time slot t can be given as

$$
E _ { u } ^ { \mathrm { c } } ( t ) = \sum _ { m \in \mathcal { M } } a _ { m } ( t ) E _ { m , u } ^ { \mathrm { c } } ( t ) .\tag{12}
$$

## D. Cost Model

UD Cost. In this work, we consider that each UDâs cost at time slot t consists of the task completion delay and the UDâs energy consumption, which reflects the UDâs QoE. The completion delay of task Î¦ $\dot { \cdot } _ { m } ( t )$ can be presented as

$$
T _ { m } ( t ) = ( 1 - a _ { m } ( t ) ) T _ { m } ^ { \mathrm { l o c } } ( t ) + a _ { m } ( t ) T _ { m } ^ { \mathrm { e c } } ( t ) .\tag{13}
$$

Then, the energy consumption of UD m can be given as

$$
E _ { m } ( t ) = ( 1 - a _ { m } ( t ) ) E _ { m } ^ { \mathrm { l o c } } ( t ) + a _ { m } ( t ) E _ { m } ^ { \mathrm { e c } } ( t ) .\tag{14}
$$

Similar to [30], [31], the cost of UD m at time slot t can be formulated as

$$
\begin{array} { r } { C _ { m } ( t ) = \gamma _ { m } T _ { m } ( t ) + ( 1 - \gamma _ { m } ) E _ { m } ( t ) , } \end{array}\tag{15}
$$

where $\gamma _ { m }$ and $1 - \gamma _ { m }$ represent the weighted parameters of delay and energy consumption of UD m respectively, which can be flexibly set based on the UDâs preference for delay and energy consumption. Obviously, minimizing the cost of UDs is equivalent to maximizing the QoE of UDs.

UAV Energy Cost. Here, the cost of the UAV at time slot t is expressed as the energy consumption, which includes the computing energy consumption and propulsion energy consumption. Similar to [28], [32], the propulsion power consumption for a rotary-wing UAV with speed $v _ { u }$ can be expressed as

$$
P _ { u } ( v _ { u } ) = \underbrace { C _ { 1 } \left( 1 + \frac { 3 v _ { u } ^ { 2 } } { U _ { \mathrm { p } } ^ { 2 } } \right) } _ { \mathrm { b l a d e ~ p r o f l e } } + \underbrace { C _ { 2 } \sqrt { \sqrt { C _ { 3 } + \frac { v _ { u } ^ { 4 } } { 4 } } } - \frac { v _ { u } ^ { 2 } } { 2 } } _ { \mathrm { i n d u c e d } } + \underbrace { C _ { 4 } v _ { u } ^ { 3 } } _ { \mathrm { p a r a s i t e } } ,\tag{16}
$$

where $U _ { \mathfrak { p } }$ refers to the rotorâs tip speed, and C1, C2, C3, and C4 are constants described in [17]. Therefore, the energy consumption of the UAV at time slot t can be given as

$$
\begin{array} { r } { E _ { u } ( t ) = E _ { u } ^ { \mathrm { c } } ( t ) + E _ { u } ^ { \mathrm { p } } ( t ) . } \end{array}\tag{17}
$$

where $\begin{array} { r } { E _ { u } ^ { \mathrm { p } } ( t ) \ = \ P _ { u } ( v _ { u } ( t ) ) \tau } \end{array}$ denotes the propulsion energy consumption at time slot t. To guarantee service time, we define the UAV energy consumption constraint as follows:

$$
\operatorname* { l i m } _ { T  + \infty } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \mathbb { E } \{ E _ { u } ( t ) \} \leq \bar { E } _ { u } ,\tag{18}
$$

where $\bar { E } _ { u }$ is the energy budget of the UAV per time slot.

## E. Problem Formulation

The objective of this work is to minimize the average costs of all UDs over time (i.e., time-average UD cost), by jointly optimizing the task offloading strategy ${ \bf A } \quad = \quad$ $\{ \mathcal { A } ^ { t } | \mathcal { A } ^ { t } = \{ a _ { m } ( t ) \} _ { m \in \mathcal { M } } \} _ { t \in \mathcal { T } }$ , computing resource allocation $\mathbf { F } = \{ \mathcal { F } ^ { t } | \mathcal { F } ^ { t } = \{ F _ { m } ( t ) \} _ { m \in \mathcal { M } } \} _ { t \in \mathcal { T } }$ , communication resource allocation $\mathbf { W } = \{ { \mathcal { W } } ^ { t } | { \mathcal { W } } ^ { t } = \{ w _ { m } ( t ) \} _ { m \in { \mathcal { M } } } \} _ { t \in { \mathcal { T } } }$ , and trajectory planning $\mathbf { P } _ { u } = \{ \mathbf { P } _ { u } ( t ) \} _ { t \in \mathcal { T } }$ . Therefore, the problem can be formulated as follows:

$$
\operatorname* { m i n } _ { \mathbf { A } , \mathbf { F } , \mathbf { W } , \mathbf { P } _ { u } } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { m = 1 } ^ { M } C _ { m } ( t )\tag{19}
$$

$$
\mathrm { s . t . } \quad \operatorname* { l i m } _ { T  + \infty } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \mathbb { E } \{ E _ { u } ( t ) \} \leq \bar { E } _ { u } ,\tag{19a}
$$

$$
a _ { m } ( t ) \in \{ 0 , 1 \} , \forall m \in \mathcal { M } , t \in \mathcal { T } ,
$$

$$
a _ { m } ( t ) T _ { m } ^ { \mathrm { e c } } ( t ) \leq T _ { m } ^ { \mathrm { m a x } } , \forall m \in \mathcal { M } , t \in \mathcal { T } ,\tag{19b}
$$

(19c)

$$
0 \leq F _ { m } ( t ) \leq F _ { u } ^ { \operatorname* { m a x } } , \forall m \in \mathcal { M } , t \in \mathcal { T } ,\tag{19d}
$$

$$
\sum _ { m = 1 } ^ { M } a _ { m } ( t ) F _ { m } \leq F _ { u } ^ { \operatorname* { m a x } } , \forall t \in \mathcal { T } ,\tag{19e}
$$

$$
0 \leq w _ { m } ( t ) \leq 1 , \forall m \in \mathcal { M } , \forall t \in \mathcal { T } ,\tag{19f}
$$

$$
\sum _ { m = 1 } ^ { M } a _ { m } ( t ) w _ { m } ( t ) \leq 1 , \forall t \in \mathcal { T } ,\tag{19g}
$$

$$
\mathbf { P } _ { u } ( 1 ) = \mathbf { P } _ { I } ,\tag{19h}
$$

$$
\| \mathbf { p } _ { u } ( t + 1 ) - \mathbf { p } _ { u } ( t ) \| \leq v _ { u } ^ { \operatorname* { m a x } } \tau , \forall t \in T ,\tag{19i}
$$

Constraint (19a) is the long-term energy consumption constraint of the UAV. Constraint (19b) indicates that each UD can only select one strategy as its offloading decision. Constraint (19c) means that the completion delay of edge computing should not exceed the maximum tolerance delay. Constraints (19d) and (19e) imply that the allocated computing resources should be a positive value and not exceed the total amount of computing resources owned by the UAV. Constraints (19f) and (19g) limit the allocation of communication resources. Constraints (19h)-(19i) are the constraints on trajectory planning.

Challenges. There are two main challenges to obtain the optimal solution of problem P. i) Future-dependent. Optimally solving problem P requires complete future information, e.g., task computing demands and locations of all UDs across all time slots. However, obtaining the future information is very challenging in the considered time-varying scenario. ii) Nonconvex and NP-hard. Problem P contains both binary variables (i.e., task offloading decision A) and continuous variables (i.e., resource allocation {F, W} and UAVâs trajectory $\mathbf { P } _ { u } )$ is an mixed-integer non-linear programming (MINLP) problem, which is non-convex and NP-hard [33], [34]. Therefore, solving the problem directly remains challenging even with knowledge of the future information.

## IV. LYAPUNOV-BASED PROBLEM TRANSFORMATION

Since problem P is future-dependent, an online approach is necessary to make real-time decisions without foreseeing the future. Lyapunov-based optimization framework is a commonly adopted method for designing online algorithms [17], [35], which has the advantage of being simple and effective. To this end, we first transform problem P into a per-slot real-time optimization problem based on the Lyapunov optimization framework.

Firstly, to satisfy the UAV energy constraint (19a), we define two virtual energy queues $Q _ { u } ^ { \mathrm { c } } ( t )$ and $Q _ { u } ^ { \mathrm { p } } ( t )$ to represent the computing energy queue and the propulsion energy queue at time slot t based on Lyapunov optimization technique, respectively. We assume that the queues are set as zero at the initial time slot, i.e., $Q _ { u } ^ { \mathrm { c } } ( 1 ) = 0$ and $Q _ { u } ^ { \mathrm { p } } ( 1 ) = 0$ . Therefore, the virtual energy queues can be updated as

$$
\begin{array}{c} \left\{ Q _ { u } ^ { \mathrm { c } } ( t + 1 ) = \operatorname* { m a x } \left\{ Q _ { u } ^ { \mathrm { c } } ( t ) + E _ { u } ^ { \mathrm { c } } ( t ) - \bar { E } _ { u } ^ { \mathrm { c } } , 0 \right\} , \forall t \in \mathcal { T } ,  \\ { Q _ { u } ^ { \mathrm { p } } ( t + 1 ) = \operatorname* { m a x } \left\{ Q _ { u } ^ { \mathrm { p } } ( t ) + E _ { u } ^ { \mathrm { p } } ( t ) - \bar { E } _ { u } ^ { \mathrm { p } } , 0 \right\} , \forall t \in \mathcal { T } , } \end{array} \right.\tag{20}
$$

where $\bar { E } _ { u } ^ { \mathrm { c } }$ and $\bar { E } _ { u } ^ { \mathfrak { p } }$ represent the computation and propulsion energy budgets per slot, respectively and $\bar { E } _ { u } ^ { \mathrm { c } } + \bar { E } _ { u } ^ { \mathrm { p } } = \bar { E _ { u } } .$ Secondly, we define the Lyapunov function $L ( \mathbf { Q } _ { u } ( t ) )$ , which represents a scalar measure of the queue backlogs, i.e.,

$$
L ( \mathbf { Q } _ { u } ( t ) ) = \frac { ( Q _ { u } ^ { \mathrm { c } } ( t ) ) ^ { 2 } + ( Q _ { u } ^ { \mathrm { p } } ( t ) ) ^ { 2 } } { 2 } .\tag{21}
$$

where $\mathbf { Q } _ { u } ( t ) = \{ Q _ { u } ^ { \mathrm { c } } ( t ) , Q _ { u } ^ { \mathrm { p } } ( t ) \}$ is the vector of current queue backlogs. Thirdly, we define the conditional Lyapunov drift for time slot t as:

$$
\Delta L ( \mathbf { Q } _ { u } ( t ) ) \triangleq \mathbb { E } \{ L ( \mathbf { Q } _ { u } ( t + 1 ) ) - L ( \mathbf { Q } _ { u } ( t ) ) \mid \mathbf { Q } _ { u } ( t ) \} .\tag{22}
$$

Finally, similar to [17], [22], [36], the drift-plus-penalty can be given as

$$
D ( \mathbf { Q } _ { u } ( t ) ) = \Delta L ( \mathbf { Q } _ { u } ( t ) ) + V \mathbb { E } \left\{ C _ { s } ( t ) \mid \mathbf { Q } _ { u } ( t ) \right\} ,\tag{23}
$$

where $\begin{array} { r } { C _ { s } ( t ) = \sum _ { m = 1 } ^ { M } C _ { m } ( t ) } \end{array}$ is the total cost of all UDs at time slot t, and $V$ is a parameter that trades off the total cost and queue stability.

Theorem 1. For all t and all possible queue backlogs $\mathbf { Q } _ { u } ( t )$ the drift-plus-penalty is upper bounded as

$$
\begin{array} { r l } & { \bar { D } ( \mathbf { Q } _ { u } ( t ) ) \leq \bar { W } + \bar { Q } _ { u } ^ { \bar { \mathrm { c } } } ( t ) ( E _ { u } ^ { \mathrm { c } } ( t ) - \bar { E } _ { u } ^ { \mathrm { c } } ) } \\ & { \qquad + Q _ { u } ^ { \mathrm { p } } ( t ) ( E _ { u } ^ { \mathrm { p } } ( t ) - \bar { E } _ { u } ^ { \mathrm { p } } ) + V \times C _ { s } ( t ) , } \end{array}\tag{24}
$$

$$
\begin{array} { r l r } { W } & { { } \ = \ } & { \frac { 1 } { 2 } \operatorname* { m a x } \left\{ \left( \bar { E _ { u } ^ { \mathrm { c } } } \right) ^ { 2 } , \left( E _ { \mathrm { m a x } } ^ { \mathrm { c } } - \bar { E _ { u } ^ { \mathrm { c } } } \right) ^ { 2 } \right\} \ + } \end{array}
$$

$$
\begin{array} { r } { \frac { 1 } { 2 } \operatorname* { m a x } \left\{ \left( \bar { E _ { u } ^ { \mathrm { p } } } \right) ^ { 2 } , \left( \bar { E _ { \mathrm { m a x } } ^ { \mathrm { p } } } - \bar { E _ { u } ^ { \mathrm { p } } } \right) ^ { 2 } \right\} i s \ a f t n i t e \ c o n s t a n t . } \end{array}
$$

Proof. The proof can refer to Theorem 1 in [17]. Due to the space limit, we omit the details. â 

According to the Lyapunov optimization framework, we minimize the right-hand side of inequality (24). Therefore, problem P that relies on future information is transformed into the real-time optimization problem Pâ² solvable with only current information, which is given as follows:

$$
\mathbf { P } ^ { \prime } : \operatorname* { m i n } _ { \substack { A ^ { t } , \mathcal { F } ^ { t } , \mathcal { W } ^ { t } , \mathbf { P } _ { u ^ { \prime } } } } Q _ { u } ^ { \mathrm { c } } ( t ) E _ { u } ^ { \mathrm { c } } ( t ) + Q _ { u } ^ { \mathrm { p } } ( t ) E _ { u } ^ { \mathrm { p } } ( t ) + V \sum _ { m = 1 } ^ { M } C _ { m } ( t )\tag{25}
$$

$$
\mathrm { s . t . ~ ( 1 9 b ) - ( 1 9 i ) }
$$

where $\mathbf { P } _ { u ^ { \prime } } = \mathbf { P } _ { u } ( t + 1 )$ represents the UAV position at time slot t+1. However, problem $\mathbf { P } ^ { \prime }$ is still an MINLP problem and the decision variables are coupled to each other. Therefore, a large amount of computational overhead caused by seeking the optimal solution for problem $\mathbf { P } ^ { \prime }$ may not be suitable for real-time decision making. To this end, we design a two-stage optimization method that obtains a sub-optimal solution in polynomial time complexity. Furthermore, similar to [37], we drop the time index for variables for the convenience of the following description.

## V. TWO-STAGE OPTIMIZATION ALGORITHM

In the section, a two-stage optimization method is proposed to solve the transformed problem $\mathbf { P ^ { \prime } }$ . In the first stage, assuming a feasible $\mathbf { P } _ { u ^ { \prime } }$ , we optimize the task offloading decision A and resource allocation $\{ \mathcal { F } , \mathcal { W } \}$ . In the second stage, based on the obtained task offloading decision $\mathcal { A } ^ { \ast }$ and resource allocation $\{ \mathcal { F } ^ { * } , \mathcal { W } ^ { * } \}$ , we optimize the UAV position $\mathbf { P } _ { u ^ { \prime } }$

## A. Stage 1: Task Offloading and Resource Allocation

Assuming a feasible $\mathbf { P } _ { u ^ { \prime } }$ and removing irrelevant constant terms, $\mathbf { P } ^ { ' }$ can be transformed into a subproblem P1 to decide task offloading and resource allocation, which is given as

$$
\begin{array} { r l } { \displaystyle } & { \displaystyle \mathbf { P 1 } : \quad V \cdot \operatorname* { m i n } _ { A , \mathcal { F } , \mathcal { W } } \left( \frac { Q _ { u } ^ { \mathrm { c } } } { V } E _ { u } ^ { \mathrm { c } } + \sum _ { m = 1 } ^ { M } C _ { m } \right) } \\ { \mathrm { s . t . } \quad } & { ( 1 9 \mathfrak { b } ) - ( 1 9 \mathfrak { g } ) } \end{array}\tag{26}
$$

Problem P1 is still an MINLP problem, and the decisions of task offloading and resource allocation are coupled with each other. Considering that the UAV is dominant in the considered UAV-enabled MEC system, we prioritize resource allocation strategies for the UAV. Then, based on the resource allocation strategy, we optimize the UDsâ offloading decisions.

1) Resource Allocation: Given an arbitrary task offloading decision profile A of the UDs, the UAV decides resource allocation strategies to minimize problem P1. Define $\begin{array} { r } { s _ { m } = \frac { F _ { m } } { F _ { u } ^ { \mathrm { m a x } } } . } \end{array}$ the resource allocation problem can be formulated as

$$
\mathbf { P 1 . 1 } : \operatorname* { m i n } _ { S , \mathcal { W } } \sum _ { m \in \mathbf { M } _ { 1 } } \left[ \gamma _ { m } \big ( \frac { D _ { m } } { w _ { m } B r _ { m , u } } + \frac { \eta _ { m } D _ { m } } { s _ { m } F _ { u } ^ { \operatorname* { m a x } } } \big ) \right.
$$

$$
+ ( 1 - \gamma _ { m } ) \frac { P _ { m } D _ { m } } { w _ { m } B r _ { m , u } } \Biggr ]
$$

$$
\mathrm { s . t . } s _ { m } \geq 0 , \forall m \in  { \mathbf { M } } _ { 1 } ,\tag{27}
$$

(27a)

$$
\sum _ { m \in \mathbf { M } _ { 1 } } s _ { m } \leq 1 ,\tag{27b}
$$

$$
w _ { m } \ge 0 , \forall m \in \mathbf { M } _ { 1 } ,
$$

$$
\sum _ { m \in \mathbf { M } _ { 1 } } w _ { m } \leq 1 ,\tag{27c}
$$

(27d)

where ${ \cal { S } } = \{ s _ { m } \} _ { m \in { \bf { M } } _ { 1 } }$ , and ${ { \bf { M } } _ { 1 } }$ represents the set of UDs who offload tasks to the UAV, which is determined by the offloading decisions A.

## Lemma 1. Problem P1.1 is convex.

Proof. Since the constraints are linear, Lemma 1 can be proved by showing that the Hessian matrix of the objective function (27) is positive semi-definite. â 

Theorem 2. The optimal resource allocation coefficient, i.e., the solution of problem P1.1, can be given as follows:

$$
\left\{ \begin{array} { l l } { s _ { m } ^ { * } = \frac { \sqrt { \frac { \gamma _ { m } \eta _ { m } D _ { m } } { F _ { u } ^ { \mathrm { m a x } } } } } { \sum _ { i \in \mathbf { M } _ { 1 } } \sqrt { \frac { \gamma _ { i } \eta _ { i } D _ { i } } { F _ { u } ^ { \mathrm { m a x } } } } } , } \\ { w _ { m } ^ { * } = \frac { \sqrt { \frac { \gamma _ { m } D _ { m } + ( 1 - \gamma _ { m } ) P _ { m } D _ { m } } { B r _ { m , u } } } } { \sum _ { i \in \mathbf { M } _ { 1 } } \sqrt { \frac { \gamma _ { i } D _ { i } + ( 1 - \gamma _ { i } ) P _ { i } D _ { i } } { B r _ { i , u } } } } . } \end{array} \right.\tag{28}
$$

Proof. Since problem P1.1 is convex, the above conclusion can be obtained by KKT conditions [33].

2) Task Offloading: For UD m, let us define $U _ { m } ^ { \mathrm { l o c } }$ as the utility of local computing and $U _ { m } ^ { \mathrm { e c } }$ as the utility of edge computing, which can be given as follows:

$$
\begin{array} { r } { U _ { m } ^ { \mathrm { l o c } } = \gamma _ { m } T _ { m } ^ { \mathrm { l o c } } + ( 1 - \gamma _ { m } ) E _ { m } ^ { \mathrm { l o c } } , } \end{array}\tag{29}
$$

$$
U _ { m } ^ { \mathrm { e c } } = \frac { Q _ { u } ^ { \mathrm { c } } } { V } E _ { m , u } ^ { \mathrm { c } } + \gamma _ { m } T _ { m } ^ { \mathrm { e c } } + ( 1 - \gamma _ { m } ) E _ { m } ^ { \mathrm { e c } } .\tag{30}
$$

Therefore, we can design the utility function of UD m as follows:

$$
U _ { m } ( A ) = { \binom { U _ { m } ^ { \mathrm { l o c } } , a _ { m } = 0 , } { U _ { m } ^ { \mathrm { e c } } , a _ { m } = 1 . } }\tag{31}
$$

According to the optimal resource allocation policy $\{ \mathcal { F } ^ { * } , \mathcal { W } ^ { * } \}$ and removing irrelevant constant terms, problem P1 can be transformed into a task offloading problem as follows:

$$
\begin{array} { r l } { \mathbf { P 1 . 2 : } } & { \underset { \mathcal { A } } { \operatorname* { m i n } } \displaystyle \sum _ { m \in \mathcal { M } } U _ { m } ( \mathcal { A } ) } \\ { \mathrm { s . t . } } & { ( \mathrm { 1 9 b } ) \mathrm { a n d } ( \mathrm { 1 9 c } ) . } \end{array}\tag{32}
$$

The offloading decision of UD m depends not only on its own demand but also on the offloading decisions of the other UDs. Considering the competitive nature of task offloading among UDs, game theory is employed to solve the task offloading decision problem.

(1) Game Formulation. We first model the task offloading decision problem as a multi-UDs task offloading game (MU-TOG). Specifically, the MU-TOG can be defined as a triplet $\Gamma = \{ \mathcal { M } , \mathbb { A } , ( U _ { m } ) _ { m \in \mathcal { M } } \}$ , which is detailed as follows:

$\mathcal { M } = \{ 1 , 2 , \dots , M \}$ denotes the set of players, i.e., all UDs.

$\mathbb { A } = \mathbf { A } _ { 1 } \times \cdot \cdot \cdot \times \mathbf { A } _ { M }$ denotes the strategy space, wherein $\mathbf { A } _ { m } = \{ 0 , 1 \}$ is the set of offloading strategies for player m $( m \in \mathcal { M } ) , a _ { m } \in \mathbf { A } _ { m }$ denotes the offloading decision of player m, and $\pmb { \mathcal { A } } = ( a _ { 1 } , \dotsc , a _ { M } ) \in \mathbb { A }$ is the strategy profile.

$( U _ { m } ) _ { m \in \mathcal { M } }$ is the utility function of player m that maps each strategy profile A to a real number.

Each player aims to minimize its utility by choosing a proper offloading strategy. Mathematically, the MU-TOG can be described by the following distributed optimization problem:

$$
U _ { m } ( a _ { m } , a _ { - m } ) , \forall m \in \mathcal { M } ,\tag{33)(33}
$$

am where $\begin{array} { l } { \displaystyle { a _ { - m } ~ = ~ \left( a _ { 1 } , \ldots , a _ { m - 1 } , a _ { m + 1 } , \ldots , a _ { M } \right) } } \end{array}$ denotes the offloading decisions of the other players except player m.

(2) The solution to MU-TOG. To determine the solution of MU-TOG, we first introduce the concept of Nash equilibrium, which describes a situation where no player has any incentive to unilaterally deviate from the current strategy.

Definition 1. The strategy profile $\mathcal { A } ^ { * } = ( a _ { 1 } ^ { * } , \ldots , a _ { M } ^ { * } )$ is a pure-strategy Nash equilibrium of game Î if and only if

$$
U _ { m } ( a _ { m } ^ { * } , a _ { - m } ^ { * } ) \leq \bar { U _ { m } } ( a _ { m } ^ { \prime } , a _ { - m } ^ { * } ) \quad \forall a _ { m } ^ { \prime } \in \dot { \bf A } _ { m } , m \in \dot { \mathcal { M } } .\tag{34}
$$

Next, we introduce a powerful tool, known as exact potential game [38], to help us study the existence of Nash equilibrium and how to obtain a Nash equilibrium solution for the MU-TOG.

Definition 2. A game is called an exact potential game if and only if a potential function $F ( \mathcal { A } ) : \mathbb { A } \mapsto$ R exists such that

$$
\begin{array} { r l } { \mathrm { ~ } } & { { } = F ( \boldsymbol { a } _ { m } , \boldsymbol { a } _ { - m } ) - F ( \boldsymbol { b } _ { m } , \boldsymbol { a } _ { - m } ) , \forall ( \boldsymbol { a } _ { m } , \boldsymbol { a } _ { - m } ) , ( \boldsymbol { b } _ { m } , \boldsymbol { a } _ { - m } ) \in \mathbb { A } . } \end{array}\tag{35}
$$

Definition 3. The exact potential game with finite strategy sets always has a Nash equilibrium and the finite improvement property (FIP) [38], [39].

The FIP implies that a Nash equilibrium can be obtained in a finite number of iterations by any asynchronous better response update process.

Theorem 3. The MU-TOG is an exact potential game where the potential function $F ( A )$ can be given as

$$
\begin{array} { r l } & { \displaystyle { F ( A ) = \sum _ { i \in \mathcal { M } } a _ { i } \left( \frac { Q _ { u } ^ { \mathrm { c } } } { V } E _ { i , u } ^ { \mathrm { c } } + \beta _ { i } \sum _ { j \leq i } a _ { j } \beta _ { j } + \phi _ { i } \sum _ { j \leq i } a _ { j } \phi _ { j } \right) } } \\ & { \qquad \quad + \displaystyle { \sum _ { i \in \mathcal { M } } ( 1 - a _ { i } ) U _ { i } ^ { \mathrm { l o c } } , \forall j \in \mathcal { M } , } } \\ & { \displaystyle { w h e r e \ \beta _ { i } = \sqrt { \frac { \gamma _ { i } \eta _ { i } D _ { i } } { F _ { \mathrm { m a x } } ^ { \mathrm { m a x } } } } \ a n d \ \phi _ { i } = \sqrt { \frac { \gamma _ { i } D _ { i } + ( 1 - \gamma _ { i } ) P _ { i } D _ { i } } { B r _ { i , u } } } . } } \end{array}\tag{36}
$$

Proof. The proof can refer to Theorem 3 in [40].

Then, let us consider the effect of constraint (19c) on the game. We can infer that imposing the constraint may render some strategy profiles infeasible. Suppose $\mathbb { A } ^ { \prime }$ is the feasible strategy space, this leads to a new game $\begin{array} { r l } { \Gamma ^ { \prime } } & { { } = } \end{array}$ $\{ \mathcal { M } , \mathbb { A } ^ { \prime } , ( U _ { m } ) _ { m \in \mathcal { M } } \}$

Theorem 4. Îâ² is also an exact potential game and has the same potential function as Î.

Proof. The proof can refer to Theorem 2.23 in [39].

The key idea of the MU-TOG is to utilize the FIP to update the offloading strategies of the players iteratively until the Nash equilibrium is reached, which is shown in Algorithm 1. The main steps of implementing the MU-TOG are described as follows. i) All UDs choose local computing for the initial setting (Line 1). ii) Each iteration is divided into N decision slots (Lines 4-15). At each decision slot, one UD is selected to update its offloading decision while the offloading decisions of the other UDs remain unchanged (Line 5). iii) If lower utility is achieved and constraint (19c) is satisfied, the UDâs offloading decision is updated; otherwise, the original offloading decision is maintained (Lines 6-14). iv) When no UD changes its offloading decision, the MU-TOG reaches the Nash equilibrium.

## B. Stage 2: UAV Trajectory Planning

Given the optimal task offloading decisions $\ b { A } ^ { * }$ and resource allocation $\{ \mathcal { F } ^ { * } , \mathcal { W } ^ { * } \}$ , while removing irrelevant constant terms, problem Pâ² can be converted into the subproblem P2 to decide the UAV trajectory planning, which is expressed as follows:

$$
\begin{array} { r l } & { \mathbf { P 2 } : \underset { \mathbf { P } _ { u ^ { \prime } } } { \mathrm { m i n } } V \displaystyle \sum _ { m \in \mathbf { M } _ { 1 } } \frac { \gamma _ { m } D _ { m } + ( 1 - \gamma _ { m } ) P _ { m } D _ { m } } { w _ { m } ^ { * } B \log _ { 2 } ( 1 + \frac { \phi _ { m } } { ( \| \mathbf { P } _ { u ^ { \prime } } - \mathbf { P } _ { m } \| ^ { 2 } + H ^ { 2 } ) ^ { \mu } } ) } + } \\ & { Q _ { u } ^ { \tt p } \left( C _ { 1 } \left( 1 + \frac { 3 v _ { u } ^ { 2 } } { U _ { \mathrm { p } } ^ { 2 } } \right) + C _ { 2 } \sqrt { \sqrt { C _ { 3 } + \frac { v _ { u } ^ { 4 } } { 4 } } - \frac { v _ { u } ^ { 2 } } { 2 } + C _ { 4 } v _ { u } ^ { 3 } } \right) \tau } \\ & { \mathrm { s . t . } \left( 1 9 \mathbf { h } \right) - ( 1 9 \mathbf { i } ) } \end{array}\tag{37}
$$

Algorithm 1: The First Stage Algorithm   
Input: The UD information $\overline { { \{ \bf S t } _ { m } ^ { \mathrm { U D } } ( t ) \} } _ { m \in \mathcal { M } }$ and the   
current UAV location $\mathbf { P } _ { u } .$   
Output: The optimal task offloading and resource   
allocation decisions $\{ \mathcal { A } ^ { \ast } , \mathcal { F } ^ { \ast } , \mathcal { W } ^ { \ast } \}$   
1 Initialization: The iteration number $l = \dot { 1 , } A ^ { 0 } = \varnothing$   
and $\mathcal { A } ^ { 1 } = \{ 0 , \ldots , 0 \}$ ;   
2 repeat   
3 $\begin{array} { r } { \mathcal { A } ^ { l - 1 } = \mathcal { A } ^ { l } ; } \end{array}$   
4 for $U D \ m \in { \mathcal { M } }$ do   
5 $\mathbf { A } ^ { l } ( m ) = a _ { m } ^ { \mathrm { e c } } = 1 ;$   
6 Obtain $F _ { m } ^ { * }$ and $w _ { m } ^ { * }$ based on Eq. (28);   
7 Calculate $T _ { m } ^ { \mathrm { e c } }$ based on Eq. (9);   
8 Calculate $U _ { m } ^ { \mathrm { e c } }$ based on Eq. (30);   
9 if $T _ { m } ^ { \mathrm { e c } } \geq T _ { m } ^ { \mathrm { m a x } }$ then   
10 $\mathbf { A } ^ { l } ( m ) = a _ { m } ^ { \mathrm { l o c } } = 0 ;$   
11 end   
12 if $U _ { m } ^ { \mathrm { e c } } \leq U _ { m } ^ { \mathrm { l o c } }$ then   
13 $\mathbf { A } ^ { l } ( m ) = a _ { m } ^ { \mathrm { l o c } } = 0 ;$   
14 end   
15 end   
16 Update $l = l + 1 ;$   
17 until $\mathbf { \bar { \mathcal { A } } } ^ { l - 1 } = \mathcal { A } ^ { l } ;$   
18 $\mathcal { A } ^ { \ast } = \mathcal { A } ^ { l } ;$   
19 Obtain $\{ \mathcal { F } ^ { * } , \mathcal { W } ^ { * } \}$ based on Eq. (28);   
20 return $\{ \mathcal { A } ^ { \ast } , \mathcal { F } ^ { \ast } , \mathcal { W } ^ { \ast } \}$

where $\begin{array} { r } { v _ { u } ~ = ~ { } \frac { \| \mathbf { P } _ { u ^ { \prime } } - \mathbf { P } _ { u } \| } { \tau } } \end{array}$ . Obviously, the objective function (37) is non-convex with respect to $\mathbf { P } _ { u ^ { \prime } }$ due to the nonconvex terms $\begin{array} { r } { T M _ { 0 } = C _ { 2 } \sqrt { \sqrt { C _ { 3 } + \frac { v _ { u } ^ { 4 } } { 4 } } } - \frac { v _ { u } ^ { 2 } } { 2 } } \end{array}$ and $\{ T M _ { m } =$ $\frac { 1 } { \log _ { 2 } \left( 1 + \frac { \phi _ { m } } { ( \| \mathbf { P } _ { u ^ { \prime } } - \mathbf { P } _ { m } \| ^ { 2 } + H ^ { 2 } ) ^ { \mu } } \right) } \} _ { m \in \mathbf { M } _ { 1 } }$ . Therefore, it is difficult to directly solve problem Pâ². We next transform the objective function into a convex function by introducing slack variables.

For the non-convex term $T M _ { 0 }$ , we introduce the slack variable y such that $y = T M _ { 0 }$ and add the following constraint:

$$
y \geq { \sqrt { { \sqrt { C _ { 3 } + { \frac { v _ { u } ^ { 4 } } { 4 } } } } - { \frac { v _ { u } ^ { 2 } } { 2 } } } } \Longrightarrow { \frac { C _ { 3 } } { y ^ { 2 } } } \leq y ^ { 2 } + v _ { u } ^ { 2 } .\tag{38}
$$

For the non-convex term $T M _ { m } .$ , we introduce the slack variable $z _ { m }$ such that $z _ { m } \ = \ T M _ { m }$ and add the following constraint:

$$
z _ { m } \leq \log _ { 2 } \left( 1 + \frac { \phi _ { m } } { \left( H ^ { 2 } + \left\| \mathbf { P } _ { u ^ { \prime } } - \mathbf { P } _ { m } \right\| ^ { 2 } \right) ^ { \mu } } \right) .\tag{39}
$$

According to the above-mentioned relaxation transformation, problem P2 can be equivalently transformed as follows:

$$
\begin{array} { r l } & { \mathbf { P 2 ^ { \prime } } \colon \displaystyle \operatorname* { m i n } _ { \mathbf { P } _ { u ^ { \prime } } , y , z _ { m } } Q _ { u } \left( P _ { 0 } \left( 1 + \frac { 3 v _ { u } ^ { 2 } } { U _ { \mathrm { t p } } ^ { 2 } } \right) + C _ { 2 } y + C _ { 3 } v _ { u } ^ { 3 } \right) \tau } \\ & { \qquad + V \displaystyle \sum _ { m \in \mathbf { M } _ { 1 } } \frac { \gamma _ { m } D _ { m } + ( 1 - \gamma _ { m } ) P _ { m } D _ { m } } { w _ { m } ^ { * } B z _ { m } } } \\ & { \qquad \mathrm { s . t . } \ ( 1 9 \mathbf { i } ) , ( 3 8 ) a n d \ ( 3 9 ) } \end{array}\tag{40}
$$

Theorem 5. Problem $\mathbf { P 2 } ^ { \prime }$ is equivalent to problem P2.

Proof. Suppose $\{ \mathbf { P } _ { u ^ { \prime } } ^ { * } , y ^ { * } , z _ { m } ^ { * } \}$ is the optimal solution of prob-

lem $\mathbf { P 2 } ^ { \prime }$ . The following equation holds:

$$
\begin{array} { l } { { \displaystyle y ^ { * } = \sqrt { \sqrt { C _ { 3 } + \frac { ( v _ { u } ^ { * } ) ^ { 4 } } { 4 } } - \frac { ( v _ { u } ^ { * } ) ^ { 2 } } { 2 } } } , } \\ { { \displaystyle z _ { m } ^ { * } = \log _ { 2 } \left( 1 + \frac { \phi _ { m } } { \left( H ^ { 2 } + \left| \left| \mathbf { P } _ { u ^ { \prime } } ^ { * } - \mathbf { P } _ { m } \right| \right| ^ { 2 } \right) ^ { \mu } } \right) , } } \end{array}\tag{41}
$$

where $\begin{array} { r } { v _ { u } ^ { * } = \frac { \| \mathbf { P } _ { u ^ { \prime } } ^ { * } - \mathbf { P } _ { u } \| } { \tau } } \end{array}$ . Otherwise, we can further reduce the objective function by choosing a smaller y or a larger $z _ { m }$ without violating the constraints (38) and (39). Therefore, $\mathbf { P } _ { u ^ { \prime } } ^ { * }$ is also the optimal solution to problem P2. â 

For problem $\mathbf { P 2 } ^ { \prime }$ , the optimization objective (40) is convex but the additional constraints (38) and (39) are still nonconvex. Similar to [15], [17], [41], the successive convex approximation (SCA) method is adopted to solve the nonconvexity of (38) and (39).

Theorem 6. Let $f ( \mathbf { P } _ { u ^ { \prime } } , y ) = y ^ { 2 } + v _ { u } ^ { 2 }$ and given a local point $\mathbf { P } _ { u ^ { \prime } } ^ { ( l ) }$ at the l-th iteration, we can obtain a global concave lower bound for $f ( \mathbf { P } _ { u ^ { \prime } } , y )$ as

$$
\begin{array} { l } { { f ^ { ( l ) } ( { \bf P } _ { u ^ { \prime } } , y ) \triangleq \left( y ^ { ( l ) } \right) ^ { 2 } + 2 y ^ { ( l ) } \left( y - y ^ { ( l ) } \right) + \frac { \Vert { \bf p } _ { u ^ { \prime } } ^ { ( l ) } - { \bf p } _ { u } \Vert ^ { 2 } } { \tau ^ { 2 } } } } \\ { { \phantom { f ^ { ( l ) } ( { \bf P } _ { u ^ { \prime } } , y ) \triangleq } + \frac { 2 } { \tau ^ { 2 } } ( { \bf p } _ { u ^ { \prime } } ^ { ( l ) } - { \bf p } _ { u } ) ^ { T } \left( { \bf p } _ { u ^ { \prime } } - { \bf p } _ { u } \right) , } } \end{array}\tag{42}
$$

where $y ^ { ( l ) }$ is defined as

$$
y ^ { ( l ) } = \sqrt { \sqrt { C _ { 3 } + \frac { \| \mathbf { p } _ { u ^ { \prime } } ^ { ( l ) } - \mathbf { p } _ { u } \| ^ { 4 } } { 4 \tau ^ { 4 } } } } - \frac { \| \mathbf { p } _ { u ^ { \prime } } ^ { ( l ) } - \mathbf { p } _ { u } \| ^ { 2 } } { 2 \tau ^ { 2 } } .\tag{43}
$$

Proof. Since $f ( \mathbf { P } _ { u ^ { \prime } } , y )$ is a convex quadratic form, the firstorder Taylor expansion of $f ( \mathbf { P } _ { u ^ { \prime } } , y )$ at local point $\mathbf { P } _ { u ^ { \prime } } ^ { ( l ) }$ is a global concave lower bound. â 

Theorem 7. Let $\begin{array} { r } { g _ { m } ( \mathbf { P } _ { u ^ { \prime } } ) = \log _ { 2 } \left( 1 + \frac { \phi _ { m } } { \left( H ^ { 2 } + \parallel \mathbf { P } _ { u ^ { \prime } } - \mathbf { P } _ { m } \parallel ^ { 2 } \right) ^ { \mu } } \right) } \end{array}$ we can obtain a global concave lower bound for $g _ { m } ( \mathbf { P } _ { u ^ { \prime } } )$ as

$$
\begin{array} { r l } & { g _ { m } ^ { ( l ) } ( \mathbf { P } _ { u ^ { \prime } } ) \triangleq \log _ { 2 } \left( 1 + \frac { \phi _ { m } } { \left( H ^ { 2 } + \| \mathbf { p } _ { u ^ { \prime } } ^ { ( l ) } - \mathbf { p } _ { m } \| ^ { 2 } \right) ^ { \mu } } \right) } \\ & { - \frac { \mu \phi _ { m } ( \log _ { 2 } e ) ( \| \mathbf { p } _ { u ^ { \prime } } - \mathbf { p } _ { m } \| ^ { 2 } - \| \mathbf { p } _ { u ^ { \prime } } ^ { ( l ) } - \mathbf { p } _ { m } \| ^ { 2 } ) } { [ \phi _ { m } + ( H ^ { 2 } + \| \mathbf { p } _ { u ^ { \prime } } ^ { ( l ) } - \mathbf { p } _ { m } \| ^ { 2 } ) ^ { \mu } ] ( H ^ { 2 } + \| \mathbf { p } _ { u ^ { \prime } } ^ { ( l ) } - \mathbf { p } _ { m } \| ^ { 2 } ) } . } \end{array}\tag{44}
$$

Proof. The proof can refer to Proposition 1 in [17].

According to Theorems 6 and 7, at the l-th iteration, constraints (38) and (39) can be approximated as:

$$
\frac { C _ { 3 } } { y ^ { 2 } } \leq f ^ { ( l ) } ( \mathbf { P } _ { u ^ { \prime } } , y ) ,
$$

$$
z _ { m } \leq g _ { m } ^ { ( l ) } ( \mathbf { P } _ { u ^ { \prime } } ) ,\tag{45}
$$

(46)

which are convex. Therefore, problem $\mathbf { P 2 } ^ { \prime }$ is converted into a convex optimization problem, which can be efficiently resolved by off-the-shelf optimization tools such as CVX [42]. We summarize the second stage algorithm in Algorithm 2.

## C. Main Steps of OJOA and Performance Analysis

In this section, the main steps of OJOA are described in Algorithm 3, and the corresponding analysis is given.

Algorithm 2: The Second Stage Algorithm   
Input: The optimal task offloading and resource   
allocation decisions $\{ \mathcal { A } ^ { \ast } , \mathcal { F } ^ { \ast } , \mathcal { W } ^ { \ast } \}$   
Output: The next location $\mathbf { P } _ { u ^ { \prime } }$   
1 Initialization: The accuracy threshold $\varepsilon = 0 . 0 1$ , the   
local point $\mathbf { P } _ { u ^ { \prime } } ^ { ( 0 ) } = \mathbf { P } _ { u } ,$ the iterative number $l = 1$ and   
the objective function value $G ^ { ( 0 ) } = 0 ;$   
2 repeat   
3 Calculate $y ^ { ( l ) }$ based on Eq. (43);   
4 Obtain the optimal position $\mathbf { P } _ { u ^ { \prime } } ^ { * }$ and the objective   
value $G ^ { ( l ) }$ by solving problem $\mathbf { P 2 ^ { \prime } } ;$   
5 Update the local point $\mathbf { P } _ { u ^ { \prime } } ^ { ( l ) } = \mathbf { P } _ { u ^ { \prime } } ^ { * }$ ;   
6 Update $l = l + 1 ;$   
7 until $\begin{array} { r } { | G ^ { ( l ) } - G ^ { ( l - 1 ) } | < \varepsilon ; } \end{array}$   
8 return $\mathbf { P } _ { u ^ { \prime } } ^ { * } .$   
Theorem 8. Assume that the proposed algorithm produces an   
optimality gap $C \geq 0$ in solving Pâ² and $C _ { s } ^ { \mathrm { { o p t } } }$ denotes the   
optimal time-average UD cost that problem P can achieve   
over all policies given full knowledge of the future computing   
demands and locations for all UDs, the time-average UD cost   
achieved by the proposed algorithm is bounded by   
$\frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { m = 1 } ^ { M } C _ { m } ( t ) \leq C _ { s } ^ { \mathrm { o p t } } + \frac { W T + C } { V } ,$ (47)   
where W is defined in Theorem 1.   
Proof. According to Lemma 4.11 in [36], the T-slot drift-plus  
penalty achieved by the proposed algorithm ensures that   
$L ( \mathbf { Q } _ { u } ( T ) ) - L ( \mathbf { Q } _ { u } ( 1 ) ) + V \sum _ { t = 1 } ^ { T } C _ { s } ( t ) \leq W T ^ { 2 } + C T + V T C _ { s } ^ { \mathrm { o p t } } .$   
(48)   
Using the fact that $L ( \mathbf { Q } _ { u } ( T ) ) \geq 0$ and $L ( \mathbf { Q } _ { u } ( 1 ) ) = 0$ , and   
dividing by V T for the above inequality, we can prove the   
theorem. â 

Theorem 9. The proposed algorithm can satisfy the UAV energy consumption constraint defined in (18).

Proof. The proof can refer to Theorem 2 in [22].

Theorem 10. The proposed OJOA has a polynomial worst-case complexity in each time slot, i.e., $\mathcal { O } ( I _ { c } M ~ + ~ $ $M ^ { 3 . 5 } \log _ { 2 } \bigl ( \frac { 1 } { \varepsilon } \bigr ) \bigr )$ , where $I _ { c }$ represents the number of iterations required for Algorithm 1 to converge to the Nash equilibrium, M denotes the number of UDs and Îµ is the accuracy of SCA for solving problem P2â².

Proof. OJOA contains two phases in each time slot, i.e., Algorithm 1 and Algorithm 2. In Algorithm 1, assuming that the outer iteration (i.e., Lines 2 â 17) converges after $I _ { c }$ iterations, the computational complexity of the algorithm can be calculated as $\mathcal { O } ( I _ { c } M )$ . In Algorithm 2, according to the analysis in [18], the computational complexity is $\mathcal { O } ( M ^ { 3 . 5 } \log _ { 2 } \left( \frac { 1 } { \varepsilon } \right) )$ . Therefore, the computational complexity of OJOA is $\begin{array} { r } { \mathcal { O } ( I _ { c } M + M ^ { 3 . 5 } \log _ { 2 } ( \frac { 1 } { \varepsilon } ) ) } \end{array}$ in the worst case. â 

Accordingly, it is proven that the proposed algorithm can effectively guarantee the performance of the system, meet the

UAV energy consumption constraint and have low computational complexity.

Algorithm 3: OJOA   
Input: The energy queue $Q _ { u } ^ { \mathrm { c } } ( 1 ) = 0 , Q _ { u } ^ { \mathrm { p } } ( 1 ) = 0$ and   
the control parameter V .   
Output: time-average UD cost T SC.   
1 Initialization: Initialize $T S C = 0$ and the initial   
position of the UAV $\mathbf { P } _ { u } ( 1 ) = \mathbf { P } _ { I } ;$   
2 for t = 1 to $t = T$ do   
3 Acquire the UD information $\{ \mathbf { S } \mathbf { t } _ { m } ^ { \mathrm { U D } } ( t ) \} _ { m \in \mathcal { M } } ;$   
4 With fixed $\mathbf { P } _ { u } ( t )$ , call Algorithm 1 to obtain   
$\{ \mathcal { A } ^ { \ast } , \mathcal { F } ^ { \ast } , \mathcal { W } ^ { \ast } \} ;$   
5 With fixed $\{ \mathcal { A } ^ { \ast } , \mathcal { F } ^ { \ast } , \mathcal { W } ^ { \ast } \}$ , call Algorithm 2 to   
obtain $\mathbf { P } _ { u ^ { \prime } } ^ { * } ;$   
6 All UDs perform their tasks based on $\ b { A } ^ { * }$ and   
obtain corresponding cost $C _ { m } ^ { * } ( t ) ;$   
7 The UAV provides MEC service to the UDs and   
flies towards position $\mathbf { P } _ { u ^ { \prime } } ^ { * } ;$   
8 System cost $\begin{array} { r } { C _ { s } ( t ) = \sum _ { m = 1 } ^ { M } C _ { m } ^ { * } ( t ) \colon } \end{array}$   
9 $\mathit { T S C } = \mathit { T S C } + \mathit { C _ { s } } ( t ) ;$   
10 Update the energy queue $\mathbf { Q } _ { u } ( t + 1 )$ according to   
Eq. (20);   
11 Update $t = t + 1 ;$   
12 end   
13 $T S C = T S C / T ;$   
14 return T SC.

## VI. SIMULATION RESULTS

In this section, we perform simulations to validate the effectiveness of our proposed OJOA.

## A. Simulation Setup

We consider a UAV-enabled MEC system consisting of a UAV and 20 UDs, where the initial horizontal position of the UAV is set as $\mathbf { P } _ { I } = [ 2 0 0 , 2 0 0 ]$ , the fixed height is $H = 1 0 0 \mathrm { m } ,$ and the initial positions of UDs are distributed in the area of $4 0 0 \times 4 0 0 ~ \mathrm { m ^ { 2 } }$ . The system timeline is discretized into 80 time slots and the length of each time slot is 1 s [18]. The maximum speed of the UAV is set to $v _ { u } ^ { \operatorname* { m a x } } = 3 0$ m/s [17] and the total computing resources of the UAV are defined as $F _ { u } ^ { \mathrm { m a x } } = 2 0$ GHz. The computing capacity of UDs is randomly taken from {1, 1.5, 2} GHz, and the transmit power is set to $P _ { m } = 0 . 1$ W. Each UD generates a computing task per time slot with input data size $D _ { m } ( t ) \in [ 0 . 1 , 1 ]$ Mb, computation intensity $\eta _ { m } ( t ) \in [ 5 0 0 , 1 5 0 0 ]$ cycles/bit [43], and maximum tolerable delay $T _ { m } ^ { \mathrm { m a x } } = 1 \mathrm { ~ s ~ } [ 1 8 ]$ . The channel bandwidth is set to B = 4 MHz. Moreover, we compare OJOA with the following four benchmark schemes:

â¢ Entire local computing (ELC): All UDs process their tasks locally.

â¢ Equal resource allocation (ERA) [44]: The UAV allocates computing and communication resources equally.

<!-- image-->  
(a) Time-average UD cost

<!-- image-->  
(b) Time-average UAV energy consumption

<!-- image-->  
(c) Time-average UAV workload

Fig. 2. System performance with respect to the time slots. (a) Time-average UD cost. (b) Time-average UAV energy consumption. (c) Time-average UAV workload.  
<!-- image-->  
(a) Time-average UD cost

<!-- image-->  
(b) Time-average UAV energy consumption

<!-- image-->  
(c) Time-average UAV workload  
Fig. 3. System performance with respect to the task data size. (a) Time-average UD cost. (b) Time-average UAV energy consumption. (c) Time-average UAV workload.

â¢ Fixed location deployment (FLP): The UAV hovers over the center of the service area to provide edge computing services.

â¢ Only consider QoE (OCQ) [22]: Ignoring the UAV energy consumption constraint, all decisions are made only to minimize the time-average UD cost.

## B. Evaluation Results

Impact of Time. Figs. 2(a), 2(b), and 2(c) show the dynamics of time-average UD cost, time-average UAV energy consumption, and time-average UAV workload among the five schemes. First, ELC exhibits the worst performance for timeaverage UD cost. Obviously, this is because all tasks are executed locally on UDs. Furthermore, ERA shows poorer performance in terms of time-average UD cost compared to FLP, OCQ, and OJOA. The reason is that due to UDsâ heterogeneous computing requirements, the average resource allocation strategy cannot effectively utilize the limited computing and communication resources. It also explains that ERA has the lowest time-average UAV workload and time-average UAV energy consumption. In addition, it can be observed that OCQ achieves higher time-average UD cost compared to FLP and OJOA. This is mainly because of the game theorybased task offloading algorithm, which is detailed in Section V-A2. Specifically, regardless of the UAV energy consumption constraint, more UDs choose to offload tasks to the UAV, which leads to a heavier UAV workload. Finally, OJOA shows superior performance in the time-average UD cost among the five schemes and satisfies the UAV energy consumption constraint. This is because OJOA optimizes the trajectory of the UAV and adopts the optimal resource allocation strategy.

Impact of Data Size. Figs. 3(a), 3(b) and 3(c) show the impact of the task data size on time-average UD cost, timeaverage UAV energy consumption, and time-average UAV workload among the comparative schemes, respectively. First, it can be observed that the time-average UD cost, time-average energy consumption, and time-average UAV workload show an upward trend with the increasing task data size. This is expected as the larger task data size leads to higher overheads on computing, communication, and energy consumption for UDs and the UAV. Furthermore, we can see that ERA, OCQ, and OJOA achieve similar time-average UD cost when the task data size is relatively small (less than 0.4 Mb). The reason is the UAV has enough resources to process the tasks of UDs when the data size is small. Finally, it can be observed that the proposed OJOA is able to adapt to varying task data sizes with relatively superior performances in time-average UD cost, especially in the heavy workload scenario.

## VII. CONCLUSION

In this work, we study task offloading, resource allocation, and UAV trajectory planning in an energy-constrained UAVenabled MEC system. A JTRTOP is formulated to maximize the QoE of all UDs while satisfying the UAV energy consumption constraint. Since the JTRTOP is future-dependent and NPhard, we propose the OJOA to solve the problem. Specifically, the future-dependent JTRTOP is firstly transformed into the PROP by using Lyapunov optimization methods. Furthermore, a two-stage optimization algorithm is proposed to solve the PROP. Simulation results show that OJOA outperforms the conventional approaches in terms of time-average UD cost while meeting the UAV energy consumption constraint.

## ACKNOWLEDGEMENT

This study is supported in part by the National Natural Science Foundation of China (62172186, 62002133, 61872158, 62272194), and in part by the Science and Technology Development Plan Project of Jilin Province (20230201087GX).

[1] C. Dong, Y. Shen, Y. Qu, K. Wang, J. Zheng, Q. Wu, and F. Wu, âUAVs as an intelligent service: Boosting edge intelligence for airground integrated networks,â IEEE Netw., vol. 35, no. 4, pp. 167â175, 2021.

[2] B. Hou, S. Yang, F. A. Kuipers, L. Jiao, and X. Fu, âEAVS: Edgeassisted adaptive video streaming with fine-grained serverless pipelines,â in Proc. of IEEE INFOCOM, 2023.

[3] L. Liu, H. Li, and M. Gruteser, âEdge assisted real-time object detection for mobile augmented reality,â in Proc. of ACM MobiCom, 2019, pp. 1â16.

[4] W. Shi, J. Cao, Q. Zhang, Y. Li, and L. Xu, âEdge computing: Vision and challenges,â IEEE Internet Things J., vol. 3, no. 5, pp. 637â646, 2016.

[5] A. Hekmati, P. Teymoori, T. D. Todd, D. Zhao, and G. Karakostas, âOptimal mobile computation offloading with hard deadline constraints,â IEEE Trans. Mob. Comput., vol. 19, no. 9, pp. 2160â2173, 2020.

[6] Y. Mao, C. You, J. Zhang, K. Huang, and K. B. Letaief, âA survey on mobile edge computing: The communication perspective,â IEEE Commun. Surv. Tutorials, vol. 19, no. 4, pp. 2322â2358, 2017.

[7] Y. Qu, H. Dai, L. Wang, W. Wang, F. Wu, H. Tan, S. Tang, and C. Dong, âCoTask: Correlation-aware task offloading in edge computing,â World Wide Web, vol. 25, no. 5, pp. 2185â2213, 2022.

[8] M. Mozaffari, W. Saad, M. Bennis, Y. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surv. Tutorials, vol. 21, no. 3, pp. 2334â 2360, 2019.

[9] J. Li, G. Sun, L. Duan, and Q. Wu, âMulti-objective optimization for UAV swarm-assisted IoT with virtual antenna arrays,â IEEE Trans. Mob. Comput., 2023.

[10] J. Li, G. Sun, H. Kang, A. Wang, S. Liang, Y. Liu, and Y. Zhang, âMultiobjective optimization approaches for physical layer secure communications based on collaborative beamforming in UAV networks,â IEEE/ACM Trans. Networking, 2023.

[11] Y. Qu, H. Sun, C. Dong, J. Kang, H. Dai, Q. Wu, and S. Guo, âElastic collaborative edge intelligence for UAV swarm: Architecture, challenges, and opportunities,â IEEE Commun. Mag., 2023.

[12] P. A. Apostolopoulos, G. Fragkos, E. Tsiropoulou, and S. Papavassiliou, âData offloading in UAV-assisted multi-access edge computing systems under resource uncertainty,â IEEE Trans. Mob. Comput., vol. 22, no. 1, pp. 175â190, 2023.

[13] P. Vamvakas, E. Tsiropoulou, and S. Papavassiliou, âOn the prospect of UAV-assisted communications paradigm in public safety networks,â in Proc. of IEEE INFOCOM, 2019, pp. 762â767.

[14] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âUAV-assisted MEC networks with aerial and ground cooperation,â IEEE Trans. Wirel. Commun., vol. 20, no. 12, pp. 7712â7727, 2021.

[15] X. Zhang, J. Zhang, J. Xiong, L. Zhou, and J. Wei, âEnergy-efficient multi-UAV-enabled multiaccess edge computing incorporating NOMA,â IEEE Internet Things J., vol. 7, no. 6, pp. 5613â5627, 2020.

[16] Q. Hu, Y. Cai, G. Yu, Z. Qin, M. Zhao, and G. Y. Li, âJoint offloading and trajectory design for UAV-enabled mobile edge computing systems,â IEEE Internet Things J., vol. 6, no. 2, pp. 1879â1892, 2019.

[17] Z. Yang, S. Bi, and Y. A. Zhang, âOnline trajectory and resource optimization for stochastic UAV-enabled MEC systems,â IEEE Trans. Wirel. Commun., vol. 21, no. 7, pp. 5629â5643, 2022.

[18] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAVassisted mobile edge computing,â IEEE Trans. Mob. Comput., vol. 21, no. 10, pp. 3536â3550, 2022.

[19] L. T. Hoang, C. T. Nguyen, and A. T. Pham, âDeep reinforcement learning-based online resource management for UAV-assisted edge computing with dual connectivity,â IEEE/ACM Trans. Networking, 2023.

[20] R. Zhou, X. Wu, H. Tan, and R. Zhang, âTwo time-scale joint service caching and task offloading for UAV-assisted mobile edge computing,â in Proc. of IEEE INFOCOM, 2022, pp. 1189â1198.

[21] Y. Qu, H. Dai, H. Wang, C. Dong, F. Wu, S. Guo, and Q. Wu, âService provisioning for UAV-enabled mobile edge computing,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3287â3305, 2021.

[22] H. Jiang, X. Dai, Z. Xiao, and A. Iyengar, âJoint task offloading and resource allocation for energy-constrained mobile edge computing,â IEEE Trans. Mob. Comput., vol. 22, no. 7, pp. 4000â4015, 2023.

[23] B. Liang and Z. J. Haas, âPredictive distance-based mobility management for PCS networks,â in Proc. of IEEE INFOCOM, 1999, pp. 1377â 1384.

[24] Q. Liu, L. Shi, L. Sun, J. Li, M. Ding, and F. Shu, âPath planning for UAV-mounted mobile edge computing with deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 69, no. 5, pp. 5723â5728, 2020.

[25] S. Batabyal and P. Bhaumik, âMobility models, traces and impact of mobility on opportunistic routing algorithms: A survey,â IEEE Commun. Surv. Tutorials, vol. 17, no. 3, pp. 1679â1707, 2015.

[26] L. Zhang, Z. Zhang, L. Min, C. Tang, H. Zhang, Y. Wang, and P. Cai, âTask offloading and trajectory control for UAV-assisted mobile edge computing using deep reinforcement learning,â IEEE Access, vol. 9, pp. 53 708â53 719, 2021.

[27] G. Sun, X. Zheng, Z. Sun, Q. Wu, J. Li, Y. Liu, and V. C. Leung, âUAV-enabled secure communications via collaborative beamforming with imperfect eavesdropper information,â IEEE Trans. Mob. Comput., 2023.

[28] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wirel. Commun., vol. 18, no. 4, pp. 2329â2345, 2019.

[29] A. Ndikumana, N. H. Tran, T. M. Ho, Z. Han, W. Saad, D. Niyato, and C. S. Hong, âJoint communication, computation, caching, and control in big data multi-access edge computing,â IEEE Trans. Mob. Comput., vol. 19, no. 6, pp. 1359â1374, 2020.

[30] Y. Chen, J. Zhao, Y. Wu, J. Huang, and X. S. Shen, âQoE-aware decentralized task offloading and resource allocation for end-edge-cloud systems: A game-theoretical approach,â IEEE Trans. Mob. Comput., 2022.

[31] Y. Ding, K. Li, C. Liu, and K. Li, âA potential game theoretic approach to computation offloading strategy optimization in end-edgecloud computing,â IEEE Trans. Parallel Distributed Syst., vol. 33, no. 6, pp. 1503â1519, 2022.

[32] H. Pan, Y. Liu, G. Sun, J. Fan, S. Liang, and C. Yuen, âJoint power and 3D trajectory optimization for UAV-enabled wireless powered communication networks with obstacles,â IEEE Trans. Commun., vol. 71, no. 4, pp. 2364â2380, 2023.

[33] S. Boyd, S. P. Boyd, and L. Vandenberghe, Convex optimization. Cambridge university press, 2004.

[34] P. Belotti, C. Kirches, S. Leyffer, J. Linderoth, J. Luedtke, and A. Mahajan, âMixed-integer nonlinear optimization,â Acta Numerica, vol. 22, pp. 1â131, 2013.

[35] C. Ding, J. Wang, M. Cheng, M. Lin, and J. Cheng, âDynamic transmission and computation resource optimization for dense LEO satellite assisted mobile-edge computing,â IEEE Trans. Commun., vol. 71, no. 5, pp. 3087â3102, 2023.

[36] M. J. Neely, Stochastic Network Optimization with Application to Communication and Queueing Systems, ser. Synthesis Lect. Commun. Netw. Morgan & Claypool Publishers, 2010.

[37] G. Cui, Q. He, X. Xia, F. Chen, F. Dong, H. Jin, and Y. Yang, âOL-EUA: Online user allocation for NOMA-based mobile edge computing,â IEEE Trans. Mob. Comput., vol. 22, no. 4, pp. 2295â2306, 2023.

[38] D. Monderer and L. S. Shapley, âPotential Games,â Games Econ. Behav., vol. 14, no. 1, pp. 124â143, 1996.

[39] D. L. Quang, Y. H. Chew, and B. H. Soong, âPotential games,â Springer International Publishing, 2016.

[40] S. Josilo and G. Dan, âWireless and computing resource allocation for Â´ selfish computation offloading in edge computing,â in Proc. of IEEE INFOCOM, 2019, pp. 2467â2475.

[41] J. Ji, K. Zhu, C. Yi, and D. Niyato, âEnergy consumption minimization in UAV-assisted mobile-edge computing systems: Joint resource allocation and trajectory design,â IEEE Internet Things J., vol. 8, no. 10, pp. 8570â8584, 2021.

[42] M. Grant and S. Boyd, âCVX: Matlab software for disciplined convex programming, version 2.1,â http://cvxr.com/cvx, Mar. 2014.

[43] Z. Sun, G. Sun, Y. Liu, J. Wang, and D. Cao, âBARGAIN-MATCH: A game theoretical approach for resource allocation and task offloading in vehicular edge computing networks,â IEEE Trans. Mob. Comput., pp. 1â18, 2023.

[44] S. Josilo and G. Dan, âSelfish decentralized computation offloading for Â´ mobile cloud computing in dense wireless networks,â IEEE Trans. Mob. Comput., vol. 18, no. 1, pp. 207â220, 2019.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/1570937393/page_3_img_1.png|page_3_img_1]]

---

