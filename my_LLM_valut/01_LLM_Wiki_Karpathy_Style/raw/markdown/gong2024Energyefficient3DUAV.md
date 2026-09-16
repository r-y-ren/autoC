# Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs

Hao Gong , Baoqi Huang , Member, IEEE, and Bing Jia , Member, IEEE

AbstractâCooperative multiple unmanned aerial vehicles (UAVs) have been widely exploited in various applications, including data collection, forest monitoring, edge computing, and so on. Due to limited onboard storage and expensive hardware costs, reducing both the energy consumption and the number of UAVs is critical for these multi-UAV applications. However, existing studies primarily revolved around energy minimization in two-dimensional (2-D) scenarios, given a sufficient but fixed number of UAVs, and most of them considered specific application scenarios, resulting in poor generality. In contrast, this paper defines a generalized application scenario, in which multiple ground nodes (GNs) are accessed by multiple UAVs in three-dimensional (3-D) scenarios, and aims to minimize the energy consumption by employing the necessary (or equivalently minimum) number of UAVs and formulating a mix-integer nonconvex problem. To this end, this paper decomposes the problem into two subproblems: energy consumption minimization for a single UAV consecutively accessing any two GNs and energy-efficient multi-UAV GN-accessing path planning employing the minimum number of UAVs. The first subproblem is solved by applying the successive convex approximation (SCA) technique and the path discretization method, while the second subproblem is addressed by designing a three-stage approximation framework based on modified particle swarm optimization (MPSO) and greedy path assignment (GPA). Comprehensive simulations demonstrate the superior performance of the proposed method in terms of optimality and efficiency compared to several other counterparts.

Index TermsâMultiple UAVs, energy consumption, number of UAVs, GN-accessing, MPSO, GPA.

## I. INTRODUCTION

N THE past few years, unmanned aerial vehicles (UAVs), I especially multi-rotor UAVs, have experienced an unprecedented level of growth due to their great mobility. There emerge many of their applications, such as search and rescue [1], [2], data collection [3], [4], cargo delivery [5], public safety [6], [7], and edge computing [8]. Multi-UAV cooperation plays an important role in these applications, which has triggered numerous studies dedicated to minimizing the energy consumption and the number of UAVs due to limited onboard storage and hardware costs. However, these studies often employ complex constraints for specific scenarios to minimize the UAV energy consumption, thereby restricting the wide applications of relevant optimization schemes and narrowing the scope for UAV energy minimization.

Existing UAV studies have highlighted the importance of minimizing the energy consumption and the number of UAVs [9], [10]. First, due to the limitation of onboard storage capacity, energy consumption minimization is beneficial to improve the range of UAVs. [11], [12], [13] minimized the energy consumption by a trajectory optimization method, but this method is only applicable to single-rotor UAVs in two-dimensional (2-D) scenarios. In [14], [15], [16], the authors solved the energy consumption minimization problem for UAVs in three-dimensional (3-D) scenarios but did not consider the case of multiple UAVs. Therefore, great efforts have to be devoted to minimizing the 3-D flight energy consumption of multiple UAVs, especially popular multi-rotor UAVs. Second, due to the expensive purchase and maintenance costs of UAVs, minimizing the number of UAVs can avoid additional overhead. However, in most existing studies [17], [18], [19], the number of UAVs was considered to be fixed (usually sufficient) rather than minimum. Although [8] minimized the number of UAVs, the UAV positions were fixed, restricting its broader applicability in multi-UAV scenarios. Thus, a more adaptable optimization method for UAV number minimization is warranted.

In summary, there are two shortcomings in the above studies. First, these optimization schemes regarding the energy consumption or the number of UAVs lack generality. Second, to the best of our knowledge, no related work has addressed the more practical problem of minimizing the total energy consumption while employing the minimum number of UAVs for task fulfillments.

Consequently, to develop more applicable optimization schemes and to explore in depth the energy-efficient performance of UAVs, this paper first generalizes current popular multi-UAV application scenarios and defines a generic multi-UAV application scenario, termed ground node (GN) accessing scenario, as shown in Fig. 1. Concretely, in this scenario, multiple UAVs are scheduled to depart from a depot to access a set of GNs and return to the same depot. GNs are accessed only when UAVs are directly above them, diminishing the impact of factors such as communication range on UAV trajectories, and in this way effectively harnesses trajectory planning to fully explore the potential space for UAV energy consumption minimization.

<!-- image-->  
Fig. 1. An overview of the GN-accessing scenario.

On this basis, this paper formulates a problem of minimizing the energy consumption for GN-accessing tasks while employing the minimum number of UAVs. Given the complexity of this mix-integer nonconvex problem, it is divided into two subproblems for ease of resolution. To be specific, the first subproblem aims to minimize the 3-D energy consumption required for a single UAV to access any two GNs consecutively, which is formulated based on the 3-D energy consumption model for multi-rotor UAVs in our previous work [20], the successive convex approximation (SCA) technique [12] and the path discretization method [11] are applied to solve this subproblem. The second subproblem aims to plan energy-efficient multi-UAV GN-accessing paths employing the minimum number of UAVs, and an approximation algorithm integrating modified particle swarm optimization (MPSO) and greedy path assignment (GPA), namely MPSO-GPA, is proposed to solve this subproblem.

For the purpose of performance evaluation, extensive simulations were performed. It is shown that the optimized trajectory demonstrates up to a 16% reduction in UAV energy consumption compared to a linear trajectory, confirming the effectiveness of the SCA-based trajectory optimization method. In addition, the superiority of the proposed approximation algorithm for minimizing the energy consumption and the number of UAVs is demonstrated by comparing it with benchmarks. The feasibility of the overall algorithms is further emphasized by analyzing the optimization results of energy-efficient multi-UAV GNaccessing.

To sum up, the main contributions of this work are summarized as follows.

- In the context of the designed multi-UAV GN-accessing scenario, an optimization problem aiming to minimize the energy consumption while employing the minimum number of UAVs is formulated. This problem is proved to be mix-integer nonconvex, and is decomposed into two subproblems to solve.

- The SCA-based algorithm is applied to solve the first subproblem, i.e., minimizing the 3-D flight energy consumption required for a multi-rotor UAV to access any two GNs consecutively. Without loss of generality, this algorithm is broadly applicable to other energy-efficient multi-rotor UAV applications.

The approximation framework MPSO-GPA is developed to solve the second subproblem, i.e., planning energyefficient multi-UAV GN-accessing paths by employing the minimum number of UAVs. This algorithm is also generic enough to be applied to other economical multi-UAV path planning.

Extensive simulations are conducted to evaluate the utility of the proposal, and the results demonstrate that the proposed methods outperform benchmarks.

## II. RELATED WORK

In this section, literature on energy consumption minimization in common UAV-assisted applications including data collection, wireless communication, and edge computing is briefly introduced.

In data collection applications, [21] applied classic linear programming and heuristic algorithms to design energy-efficient path planning for data collection. In [22], the task area was segmented into grids, each with a central wireless charging device for UAVs; reinforcement learning was utilized to optimize the selection of charging points, flying altitude, and connected sensor nodes, thereby enhancing UAV energy efficiency. Furthermore, as mentioned in [23], a fixed-wing UAV was deployed for secure data collection, minimizing the combined energy consumption of the UAV and sensor devices (SDs) by jointly optimizing the UAVâs 3D trajectory and the SDsâ transmission schedule. [24] demonstrated a strategy involving multiple UAVs with pre-planned trajectories to collect sensory data from stationary devices, effectively reducing energy consumption.

In wireless communication applications, to overcome the limitations of onboard batteries for UAV-aided communication applications, [25] formulated an optimization problem aiming to minimize the UAVâs energy procurement costs. The authors in [26] treated the UAV placement issue as a constrained optimization problem, aiming to optimize for maximum equitable coverage and minimum energy consumption while adhering to backhaul requirements at specific time nodes. In [13], the authors focused on establishing the energy model for singlerotor UAVs, and under the premise of limited UAV energy, they jointly optimized sensor communication scheduling, transmit power allocation, and UAV trajectory to minimize the maximum energy consumption of the UAV and sensors. Moreover, [27] investigated the problem of scheduling the movement of multiple UAVs to fairly provide energy-efficient communication services to mobile ground users for a given period, by using the deep reinforcement learning (DRL) methods.

In edge computing applications, [28] studied the energy consumption in terminals on the ground and UAVs and came up with the idea of UAV trajectory adjustment in solving the trade-off brought by flight propulsion. In [29], the authors proposed an attention-based multi-agent proximal policy optimization (MAPPO) algorithm to pursue the optimal computation offloading policy of UAVs to minimize the weighted energy consumption while considering service fairness. To minimize the

TABLE I  
CONTRIBUTION COMPARISONS OF PREVIOUS WORKS AND THIS WORK
<table><tr><td>Elements</td><td>this work</td><td>[17]</td><td>[26]</td><td>[27]</td><td>[28]</td><td>[29]</td><td>[30]</td><td>[31]</td><td>[32]</td><td>[33]</td><td>[34]</td><td>[35]</td><td>[36]</td></tr><tr><td>Multi-UAV</td><td>â</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>â</td><td>Ã</td><td>â</td><td>Ã</td><td>Ã</td><td>â</td><td>â</td><td>â</td></tr><tr><td>3-D mobility</td><td></td><td>Ã</td><td>Ã</td><td>Ã</td><td>â</td><td>Ã</td><td>â</td><td>Ã</td><td>â</td><td>â</td><td>â</td><td>â</td><td>Ã</td></tr><tr><td>Multi-rotor UAV</td><td></td><td>Ã</td><td>â</td><td>â</td><td>Ã</td><td>ä¸</td><td>Ã</td><td>â</td><td>â</td><td>Ã</td><td>Ã</td><td>â</td><td>â</td></tr><tr><td>Accurate energy model</td><td>&lt;&gt;&gt;</td><td>â</td><td>â</td><td>Ã</td><td>â</td><td>â</td><td>â</td><td>â</td><td>Ã</td><td>â</td><td>â</td><td>Ã</td><td>â</td></tr><tr><td>Minimum UAV number</td><td>â</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td></tr></table>

UAV energy consumption, [30] introduced a cellular-connected UAV mobile edge computing (MEC) system, optimizing bit allocation, power allocation, and the trajectories of multiple UAVs. In [31], to reduce the energy consumption, the authors optimized the trajectory planning of UAVs and computation resource allocation by converting these two problems into convex ones, and solved them with an efficient iterative algorithm.

Nevertheless, the above research suffers from the following two critical limitations. First, current UAV energy consumption minimization schemes are typically tailored to specific scenarios and struggle to tackle problems that simultaneously incorporate common elements like multi-rotor UAVs, multi-UAV cooperation, 3-D mobility, and accurate energy consumption models, thereby restricting their broader applicability. Second, the number of UAVs in multi-UAV-assisted applications is often predetermined, not minimized, resulting in extra hardware costs. Table I delineates the differences between this paper and the prior studies. Hence, it is imperative to develop a generalized multi-UAV application scenario in which a thorough UAV energy consumption minimization scheme is designed while taking into account UAV number minimization.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

This section first introduces the system model and the UAV energy consumption model in multi-UAV GN-accessing scenarios, and then formulates an optimization problem aimed at minimizing the energy consumption for GN-accessing tasks while employing the minimum number of UAVs; recognizing the high complexity of direct solutions, this problem is efficiently decomposed into two subproblems, finally, a detailed examination of approximation executionsâ feasibility in optimization problems is given. To clarify, Fig. 2 illustrates the optimization problems and their main decision variables in this paper.

## A. System Model

Considering a GN-accessing scenario in which $M \in \mathbb { Z } ^ { + }$ homogeneous multi-rotor UAVs are assigned to access $N \in \mathbb { Z } ^ { + }$ GNs distributed over a task space, where a GN can be a wireless sensor, a facility, or a mobile device. Assume that M UAVs are deployed, where the value of M is unknown and will be determined later. The UAVs and GNs are denoted by the sets $\mathcal { M } { = } \{ 1 , { \ldots } . . . , M \}$ and $\mathcal { N } { = } \{ 1 , { \ldots } . , N \}$ , respectively. The horizon-= =tal location and the access altitude of the nth GN with $n \in \mathcal N .$ denoted as $\mathbf { w } _ { n } \in \mathbb { R } ^ { 2 \times 1 }$ and $H _ { n } ,$ respectively, are pre-known before task assignment. All UAVs are assumed to depart from the same depot at the same time and return to that depot after the task is fulfilled, namely that all GNs are accessed. Let T denote the total time for the UAVs to fulfill the task. Moreover, for harmonization, the horizontal location of the depot is denoted as $\mathbf { w } _ { 0 } \in \mathbb { R } ^ { 2 \times 1 }$ , and the flight altitude of the UAVs departing from or to the depot is defined as $H _ { 0 }$ . The overall scenario of GN-accessing tasks is shown in Fig. 1.

<!-- image-->  
Fig. 2. Problem decomposition and main decision variables.

## B. The Generic Energy Consumption Model

In this subsection, a generic power consumption model for multi-rotor UAVs is given and further applied to calculate 3-D UAV energy consumption.

Simplifying UAV power consumption models, while ensuring their reasonableness, significantly enhances the efficiency of energy consumption minimization. Since communication-related energy consumption is significantly less than propulsion energy consumption [32], and acceleration/deceleration energy consumption forms a minor part of overall energy consumption [11], the two are ignored. To this end, an efficient 3-D propulsion power consumption model for UAVs in steady status [20], which is mainly determined by the horizontal velocity V and the vertical velocity $\mathbf { V } ^ { \perp }$ , is presented as (1) shown at the bottom of the next page, where sgn is a sign function and other parameters are described in Table II.

On that basis, the corresponding 3-D propulsion energy consumption of multi-rotor ${ \mathrm { U A V s } } ,$ denoted as $E _ { 1 }$ , can be heuristically modeled as

$$
E _ { 1 } \left( \{ \mathbf { q } ( t ) \} , \{ h ( t ) \} , T ^ { t } \right) = \int _ { 0 } ^ { T ^ { t } } P _ { t o t a l } \left( \mathbf { V } ^ { \parallel } ( t ) , \mathbf { V } ^ { \perp } ( t ) \right) d t ,\tag{2}
$$

where ${ \bf q } ( t ) \in \mathbb { R } ^ { 2 \times 1 }$ and $h ( t )$ define the horizontal and vertical ( ) ( )coordinates corresponding to the UAV trajectory at time instant

TABLE II  
MAIN NOTATIONS OF THE ENERGY CONSUMPTION MODEL
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Physical meaning</td><td rowspan=1 colspan=1>Simulation value</td></tr><tr><td rowspan=1 colspan=1>nr</td><td rowspan=1 colspan=1>Number of rotors</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Profile drag coefficient</td><td rowspan=1 colspan=1>0.011</td></tr><tr><td rowspan=1 colspan=1>p</td><td rowspan=1 colspan=1>Air density in $\overline { { \mathrm { k g / m ^ { 3 } } } }$ </td><td rowspan=1 colspan=1>1.168</td></tr><tr><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>Rotor solidity</td><td rowspan=1 colspan=1>0.045</td></tr><tr><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>Rotordiscarea in $\overline { { { \bf m } ^ { 2 } } }$ </td><td rowspan=1 colspan=1>0.214</td></tr><tr><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>UAV weight in Newton</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=1>U0</td><td rowspan=1 colspan=1>Mean rotor induced velocity inhover</td><td rowspan=1 colspan=1>6.325</td></tr><tr><td rowspan=1 colspan=1> $\overline { { C _ { t } } }$ </td><td rowspan=1 colspan=1>Thrust coefficient</td><td rowspan=1 colspan=1>0.001195</td></tr><tr><td rowspan=1 colspan=1> $S _ { F P \parallel }$ </td><td rowspan=1 colspan=1>Fuselageequivalent flat platearea in horizontal status in mÂ²</td><td rowspan=1 colspan=1>0.009</td></tr><tr><td rowspan=1 colspan=1> $S _ { F P \perp }$ </td><td rowspan=1 colspan=1>Fuselageequivalent flatplatearea in vertical status in $\mathrm { m ^ { 2 } }$ </td><td rowspan=1 colspan=1>0.19</td></tr><tr><td rowspan=1 colspan=1> $P _ { b l }$ </td><td rowspan=1 colspan=1>Blade profile power forUAVs inhovering status</td><td rowspan=1 colspan=1>133.9869</td></tr><tr><td rowspan=1 colspan=1> $P _ { i n }$ </td><td rowspan=1 colspan=1>Induced power for UAVs in hov-ering status</td><td rowspan=1 colspan=1>70.2132</td></tr></table>

t, respectively, $T ^ { t }$ is the UAV flight time, moreover, $\mathbf { V } ^ { \parallel } ( t )$ and $\mathbf { V } ^ { \perp } ( t )$ satisfy $\mathbf { V } ^ { \parallel } ( t ) \triangleq { \dot { \mathbf { q } } } ( t )$ and $\mathbf { \bar { V } } ^ { \perp } ( t ) \triangleq \dot { h } ( t )$ ( ), respectively.

## C. Problem Formulation

Regarding the optimization problem of minimizing the energy consumption for GN-accessing tasks while employing the minimum number of UAVs, this subsection first gives the decision variables and constraints related to the optimization problem, and then formulates the optimization problem in closed form.

1) Decision Variables and Constraints: First, to describe the association status and sequence of the mth UAV among the GNs, a binary decision $x _ { i j } [ m ] , i , j \in \mathcal { N } \cup \{ 0 \}$ is introduced, which [ ] 0equals 1 if the mth UAV accesses GN (or depot) j after GN (or depot) i, and equals 0 otherwise. In this case, the flow constraints can be expressed as

$$
\sum _ { i \in N } x _ { i 0 } [ m ] = 1 , ~ \forall m \in \mathcal { M } ,\tag{3}
$$

$$
\sum _ { j \in \mathcal { N } } x _ { 0 j } [ m ] = 1 , ~ \forall m \in \mathcal { M } ,\tag{4}
$$

$$
\sum _ { m \in \mathcal { M } } \sum _ { i \in \mathcal { N } } x _ { i j } [ m ] = 1 , \forall j \in \mathcal { N } ,\tag{5}
$$

$$
\sum _ { i \in \mathcal { N } } x _ { i v } [ m ] = \sum _ { j \in \mathcal { N } } x _ { v j } [ m ] , \forall v \in \mathcal { N } \cup \{ 0 \} , \forall m \in \mathcal { M } ,\tag{6}
$$

$$
x _ { i j } [ m ] \in \{ 0 , 1 \} , \forall i , j \in \mathcal { N } \cup \{ 0 \} , \forall m \in \mathcal { M } ,\tag{7}
$$

where constraints (3) and (4) ensure that all UAVs depart from the depot as tasks start and return to the same depot after tasks are fulfilled. Constraint (5) states that each GN is accessed once by one UAV. Constraint (6) guarantees that each UAV leaves a GN if and only if it arrives at that GN. Constraint (7) specifies the possible values $x _ { i j } [ m ]$ can take.

[ ]Then, for the purpose of representing the set of GNs accessed by the mth UAV, $O _ { m } \in \mathbf { O }$ is introduced to denote the corresponding tour1 of the mth UAV, where O is the full set of tours and its value, denoted as |O|, equals M. The set of GNs covered by $O _ { m }$ , denoted as $S _ { O _ { m } }$ , satisfies the following condition

$$
\begin{array} { c } { { \displaystyle \sum _ { i \in S _ { O _ { m } } } \sum _ { j \in S _ { O _ { m } } } x _ { i j } [ m ] = | S _ { O _ { m } } | - 1 , } } \\ { { S _ { O _ { m } } \subseteq { \mathcal N } , } } \end{array}\tag{8}
$$

Moreover, the energy spent by the mth UAV on the tour $O _ { m }$ ï¼ namely $E _ { O _ { m } }$ , can be expressed as

$$
\begin{array} { l } { { \displaystyle { \cal E } _ { O _ { m } } = \sum _ { i \in S _ { O _ { m } } } \left( x _ { 0 i } [ m ] { \cal E } _ { 0 i } + x _ { i 0 } [ m ] { \cal E } _ { i 0 } \right) } } \\ { { \displaystyle ~ + \sum _ { i \in S _ { O _ { m } } } \sum _ { j \in S _ { O _ { m } } } x _ { i j } [ m ] { \cal E } _ { i j } } , } \end{array}\tag{9}
$$

where $E _ { i j }$ represents the energy consumption for a UAV consecutively accessing GN i and GN j, and is calculated as

$$
\begin{array} { l } { { \displaystyle E _ { i j } = E _ { 1 } \left( \{ \tilde { \mathbf { q } } _ { i j } ( t _ { i j } ) \} , \{ \tilde { h } _ { i j } ( t _ { i j } ) \} , \tilde { T } _ { i j } ^ { t } \right) } } \\ { { \displaystyle \ = \ \int _ { 0 } ^ { \tilde { T } _ { i j } ^ { t } } P _ { t o t a l } \left( \tilde { \mathbf { V } } _ { i j } ^ { \parallel } ( t _ { i j } ) , \tilde { \mathbf { V } } _ { i j } ^ { \perp } ( t _ { i j } ) \right) d t _ { i j } } , } \end{array}\tag{10}
$$

where $\tilde { \mathbf { q } } _ { i j } ( t _ { i j } ) , \tilde { h } _ { i j } ( t _ { i j } ) , \tilde { \mathbf { V } } _ { i j } ^ { \parallel } ( t _ { i j } )$ and $\tilde { \mathbf { V } } _ { i j } ^ { \perp } ( t _ { i j } )$ define the hor-Ë ( ) ( ) ( ) ( )izontal coordinates, vertical coordinates, horizontal velocity, and vertical velocity of a UAV at instant time $t _ { i j }$ under the flight trajectory between consecutively accessed GNs i and j,

1A tour is a feasible and complete path for a UAV to cover all GNs assigned to it.

$$
\begin{array} { l } { { \displaystyle P _ { t o t a l } ( { \bf V } ^ { \parallel } , { \bf V } ^ { \perp } ) = P _ { b l } + \frac { 3 } { 8 } \sqrt { n _ { r } } \delta \sqrt { \displaystyle \frac { W \rho A } { C _ { t } } } s \| { \bf V } ^ { \parallel } \| ^ { 2 } + P _ { i n } \left( \sqrt { 1 + \frac { \| { \bf V } ^ { \parallel } \| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \| { \bf V } ^ { \parallel } \| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } + \frac { n _ { r } } { 2 } S _ { F P \parallel } \rho \| { \bf V } ^ { \parallel } \| ^ { 3 } + \frac { 1 } { 2 } W \| { \bf V } ^ { \perp } \| } } \\ { { \displaystyle \qquad + s g n ( { \bf V } ^ { \perp } ) \frac { n _ { r } } { 4 } S _ { F P \perp } \rho \| { \bf V } ^ { \perp } \| ^ { 3 } + \left( \frac { W } { 2 } + s g n ( { \bf V } ^ { \perp } ) \frac { n _ { r } } { 4 } S _ { F P \perp , \rho } \rho \| { \bf V } ^ { \perp } \| ^ { 2 } \right) } } \\ { { \displaystyle \qquad \times \sqrt { \| { \bf V } ^ { \perp } \| ^ { 2 } + s g n ( { \bf V } ^ { \perp } ) \frac { S _ { F P \perp } } { A } \| { \bf V } ^ { \perp } \| ^ { 2 } + \frac { 2 W } { n _ { r } \rho A } } } } \\ { { \displaystyle \qquad + \left( s g n ( \| { \bf V } ^ { \perp } \| ) - 1 \right) \frac { W } { 2 } \sqrt { \frac { 2 W } { n _ { r } \rho A } } , } } \end{array}\tag{1}
$$

respectively; in addition, $\tilde { T } _ { i j } ^ { t }$ is the UAV flight time spent in this trajectory.

Furthermore, given the maximum energy limit $E _ { \mathrm { m a x } }$ for a UAV, $E _ { O _ { m } }$ of the mth UAV must not exceed this threshold. Thus, the following constraint should be satisfied

$$
E _ { O _ { m } } \leq E _ { \mathrm { m a x } } , \quad \forall O _ { m } \in \mathbf { O } .\tag{11}
$$

2) Mathematical Formulation: Prior to formulating the optimization problem, the structural relationship between the two key optimization metrics in it is examined. While this optimization problem emphasizes two minimums, i.e., the minimum total energy consumption and the minimum number of UAVs, this problem treats only the former as the optimization objective due to the UAV number being a prerequisite for calculating total energy consumption, with the latter serving as a decision variable, termed the total energy consumption minimization problem employing the minimum number of UAVs.

Consequently, based on (9), the total energy consumption minimization problem involving five optimization variables, i.e., the UAV path $\Upsilon = \{ x _ { i j } [ m ] , \forall m \in \mathcal { M } , \forall i , j \in \mathcal { N } \}$ , Î¥the UAV horizontal trajectory $\mathbf { Q } = \{ \tilde { \mathbf { q } } _ { i j } ( t _ { i j } ) , \forall i , j \in \mathcal { N } , \forall t _ { i j } \in$ $[ 0 , \tilde { T } _ { i j } ^ { t } ] \}$ , the UAV vertical trajectory $\mathbf { H } = \{ \tilde { h } _ { i j } ( t _ { i j } ) , \forall i , j \in$ $\mathcal { N } , \forall t _ { i j } \in [ 0 , \tilde { T } _ { i j } ^ { t } ] \}$ , the UAV flight time $\mathbf { T } = \{ \tilde { T } _ { i j } ^ { t } , \forall i , j \in \mathcal { N } \}$ [0 ] =and the UAV number M (as aforementioned, M discussed below is restricted to its lower bound, representing the minimum UAV number required for task fulfillments), can be formulated as

$$
\begin{array} { r } { { \displaystyle ( \mathrm { P 1 } ) : \operatorname* { m i n } _ { \Upsilon , \mathbf { Q } , \mathbf { H } } \sum _ { O _ { m } \in O } E _ { O _ { m } } } \ ~ } \\ { { \mathrm { s . t . ~ } \displaystyle \sum _ { j \in \mathcal { N } } \displaystyle \sum _ { m \in \mathcal { M } } x _ { 0 j } [ m ] = M , } } \\ { { \ \ \ } ( 3 ) - ( 7 ) , \ ( 1 1 ) . } \end{array}\tag{12}
$$

Thereby, to deal with Problem ( ), these five variables need P1to be determined. Fortunately, following the similar analysis in [17], given Q, H and T, Problem ( ) can be approximated as P1an easily solvable multiple traveling salesmen problem (MTSP), and the proof can be found in Proposition 1. Obviously, Q, H and T should be prioritized, thereafter, the remaining parameters and M can be tackled by solving the approximated MTSP. Î¥As such, solving Problem ( ) equates to addressing two subproblems with respect to {Q, H, T} and { , M }, respectively.

Î¥First, it can be easily known from (10) that Q, H and T can be obtained by minimizing $E _ { i j }$ , hence the first subproblem can be expressed as

$$
( \mathrm { P 2 } ) : \operatorname* { m i n } _ { \mathbf { Q } , \mathbf { H } , \mathbf { T } } E _ { i j }
$$

$$
\mathrm { s . t . } \quad \| \dot { \tilde { \mathbf { q } } } _ { i j } ( t _ { i j } ) \| \leq V _ { \operatorname* { m a x } } ^ { \| } , \quad | \dot { \tilde { h } } _ { i j } ( t _ { i j } ) | \leq V _ { \operatorname* { m a x } } ^ { \perp } ,
$$

$$
\forall t _ { i j } \in \left[ 0 , \tilde { T } _ { i j } ^ { t } \right] ,\tag{13}
$$

$$
\begin{array} { r } { \tilde { \bf q } _ { i j } ( 0 ) = { \bf w } _ { i } , \tilde { \bf q } _ { i j } ( \tilde { T } _ { i j } ^ { t } ) = { \bf w } _ { j } , } \end{array}\tag{14}
$$

$$
\tilde { h } _ { i j } ( 0 ) = H _ { i } , ~ \tilde { h } _ { i j } ( \tilde { T } _ { i j } ^ { t } ) = H _ { j } ,\tag{15}
$$

where $V _ { \mathrm { m a x } } ^ { \parallel }$ and $V _ { \mathrm { m a x } } ^ { \perp }$ are the maximum UAV horizontal speed and maximum vertical speed, respectively.

Apparently, the first subproblem is still difficult to solve directly since it involves an infinite number of variables with respect to $t _ { i j }$ and contains a complex energy consumption cost function. In Section IV, a solution based on SCA technique and path discretization is proposed to deal with Problem ( ).

P2To this end, the determination of Q, H and T enables Problem ( ) to be further transformed into the second subproblem, P1which is described as

$$
( \mathrm { P 3 } ) : \operatorname* { m i n } _ { \Upsilon , M } \sum _ { O _ { m } \in O } E _ { O _ { m } }
$$

Second, M needs to be prioritized as a way to obtain  and the Î¥minimum total UAV energy consumption. As previously stated, given M , Problem ( ) transforms into a variant MTSP with P3determined energy weights aiming to minimize the total UAV energy consumption, yielding the path planning results as . In Î¥Section V, a framework is proposed to calculate the minimum number of UAVs and further applied to solve Problem ( ).

## D. Analysis of Approximation Executions in Optimization Problems

To explain the approximation executions carried out in formulating the above optimization problems, the following theoretical analysis is provided.

Proposition 1: Given Q, H and T, Problem ( ) is closely analogous to a MTSP.

Proof: Dissecting the relationship between variables and optimization problems is crucial to simplifying optimization problems. To be specific, Problem ( ) contains five variables, i.e., P1Q, H, T,  and M, where Q, H and T are UAV trajectory Î¥variables that directly affect UAV propulsion energy consumption, while  and M can determine flight paths of multiple Î¥UAVs based on the determination of these three. Therefore, given Q, H and T, Problem ( ) is essentially approximated P1to an energy-efficient multi-UAV path planning problem with established energy weights $( \mathrm { i . e . , } E _ { i j } , i , j \in \mathcal { N } )$ , which is closely analogous to a MTSP. 

## IV. PATH DISCRETIZATION AND SCA BASED SOLUTION FOR SOLVING PROBLEM (P2)

In this section, path discretization approaches are first applied to transform Problem ( ) into a more solvable form, and then a P2SCA based algorithm is proposed to obtain a suboptimal solution of Problem ( ), finally, an analysis of proposed optimization problem and algorithm is presented.

## A. Path Discretization to Problem (P2)

Problem ( ) is reformulated as a more tractable discretized form by path discretization. To be specific, the path of the UAV accessing GN i and GN j sequentially is discretized into $U + 1$ line segments [11], whose horizontal and vertical projections are represented by U   horizontal waypoints $\{ \tilde { \mathbf { q } } _ { i j } ^ { u } \} _ { u = 0 } ^ { \bar { U } + 1 }$ and

$U + 2$ vertical waypoints $\{ \tilde { h } _ { i j } ^ { u } \} _ { u = 0 } ^ { U + 1 }$ , respectively, where $\tilde { \mathbf { q } } _ { i j } ^ { 0 } =$ $\mathbf { w } _ { i } , \tilde { \mathbf { q } } _ { i j } ^ { U + 1 } = \mathbf { w } _ { j } , \tilde { h } _ { i j } ^ { 0 } = H _ { i }$ and $\tilde { h } _ { i i } ^ { U + 1 } = H _ { j }$ . For ease of pre-Ë =sentation, define $\mathcal { U } \overset { \vartriangle } { = } \{ 0 , \ldots , U + \overset { \vartriangle } { 1 } \}$ =. Note that $\sum _ { { \boldsymbol { u } } \in { \boldsymbol { \mathcal { U } } } } \tilde { \mathbf { q } } _ { i j } ^ { u }$ and $\textstyle \sum _ { u \in { \mathcal { U } } } { \tilde { h } } _ { i j } ^ { u }$ are equal to $\int _ { 0 } ^ { \tilde { T } _ { i j } ^ { t } } \tilde { \mathbf { q } } _ { i j } ( t _ { i j } ) d t _ { i j }$ and $\begin{array} { r } { \int _ { 0 } ^ { \tilde { T } _ { i j } ^ { t } } \tilde { h } _ { i j } ( t _ { i j } ) d t _ { i j } } \end{array}$ respectively. Besides, the duration $\{ \tilde { T } _ { i j } ^ { u } \} _ { u = 0 } ^ { U }$ is expressed as the time spent by the UAV on the uth line segment, the sum of which is equal to $\bar { \tilde { T } } _ { i j } ^ { t }$ . The following constraints are imposed:

$$
\begin{array} { r } { \left\| \tilde { \mathbf { q } } _ { i j } ^ { u + 1 } - \tilde { \mathbf { q } } _ { i j } ^ { u } \right\| \leq \Delta _ { \operatorname* { m a x } } ^ { \| } , \quad | \tilde { h } _ { i j } ^ { u + 1 } - \tilde { h } _ { i j } ^ { u } | \leq \Delta _ { \operatorname* { m a x } } ^ { \perp } , \quad \forall u \in \mathcal { U } , } \end{array}\tag{16}
$$

where $\Delta _ { \mathrm { m a x } } ^ { \parallel }$ and $\Delta _ { \mathrm { m a x } } ^ { \perp }$ are appropriately chosen values to ensure Î Îthat horizontal and vertical velocities of UAVs can be assumed to be constant in each line segment, and U is usually chosen to be large enough to ensure the completion of the flight. Furthermore, the UAV horizontal velocity and the UAV vertical velocity along the uth line segment are thus given by $\begin{array} { r } { \tilde { \mathbf { v } } _ { i j } ^ { \parallel u } = \frac { \tilde { \mathbf { q } } _ { i j } ^ { u + 1 } - \tilde { \mathbf { q } } _ { i j } ^ { u } } { \tilde { T } _ { i j } ^ { u } } } \end{array}$ and $\begin{array} { r } { \tilde { \mathbf { v } } _ { i j } ^ { \perp u } = \frac { \tilde { h } _ { i j } ^ { u + 1 } - \tilde { h } _ { i j } ^ { u } } { \tilde { T } _ { i j } ^ { u } } } \end{array}$ , respectively.

As a result, the optimization variables Q, H and T are replaced by $\mathbf { Q } _ { 1 } = \{ \tilde { \mathbf { q } } _ { i j } ^ { u } , \forall u \in \mathcal { U } \} , \mathbf { H } _ { 1 } = \{ \tilde { h } _ { i j } ^ { u } , \forall u \in \mathcal { U } \}$ , and $\mathbf { T } _ { 1 } = \{ \tilde { T } _ { i j } ^ { u } , \forall u \in \mathcal { U } \}$ , respectively, the energy minimization =Problem ( ) can be expressed in the discrete form as

$$
\begin{array} { r l } & { \underset { { \bf { Q } } _ { 1 } , { \bf { H } } _ { 1 } , { \bf { T } } _ { 1 } } { \mathrm { m i n } } E _ { 1 } \left( { \bf { Q } } _ { 1 } , { \bf { H } } _ { 1 } , { \bf { T } } _ { 1 } \right) } \\ & { \quad \mathrm { s . t . } \quad \left\| { \tilde { \bf { q } } } _ { i j } ^ { u + 1 } - { \tilde { \bf { q } } } _ { i j } ^ { u } \right\| \leq \operatorname* { m i n } \left\{ \Delta _ { \operatorname* { m a x } } ^ { \parallel } , \tilde { T } _ { i j } ^ { u } V _ { \operatorname* { m a x } } ^ { \parallel } \right\} , } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad ( 1 7 \times \Delta ) ^ { 2 } } \\ & { \quad \quad \quad \quad \quad \quad \left| { \tilde { h } } _ { i j } ^ { u + 1 } - { \tilde { h } } _ { i j } ^ { u } \right| \leq \operatorname* { m i n } \left\{ \Delta _ { \operatorname* { m a x } } ^ { \perp } , \tilde { T } _ { i j } ^ { u } V _ { \operatorname* { m a x } } ^ { \perp } \right\} , } \end{array}\tag{}
$$

$$
\forall u \in \mathcal { U } ,\tag{18}
$$

$$
\begin{array} { r } { \tilde { \mathbf q } _ { i j } ^ { 0 } = { \mathbf w } _ { i } , \tilde { \mathbf q } _ { i j } ^ { U + 1 } = { \mathbf w } _ { j } , } \end{array}\tag{19}
$$

$$
\tilde { h } _ { i j } ^ { 0 } = H _ { i } , \tilde { h } _ { i j } ^ { U + 1 } = H _ { j } ,\tag{20}
$$

where

$$
\begin{array} { c l } { { { \cal K } _ { 1 } ( Q _ { 1 } , { \bf H } _ { 1 } , { \bf T } _ { 1 } ) = } } & { { \displaystyle \sum _ { s = 0 } ^ { \infty } | R _ { s } { \hat { \cal U } } _ { 2 } ^ { s } ( { \frac { 1 } { 2 s } } ( P _ { 2 } ^ { s } + P _ { 1 } \| \frac { \Delta _ { \hat { \theta } } } { \hat { \cal U } _ { 2 } } | ^ { 2 s } )  } } \\ { { } } & { { } } \\ { { } } & { { \displaystyle  \mathrm { ~  ~ } + P _ { \mathrm { a s } } \| \sqrt { \hat { \cal T } _ { 2 \mathrm { a } } ^ { s } + \frac { 1 } { 4 s ! } \frac { \| \Delta _ { \hat { \theta } } \| ^ { 4 } } { 4 s } - \frac { \| \Delta _ { \hat { \theta } } \| ^ { 2 } } { 2 9 s _ { 0 } ^ { 2 } } } \| ^ { 2 s } } } \\ { { } } & { { } } \\ { { } } & { { \displaystyle - P _ { 2 } \frac { \| \Delta _ { \hat { \theta } } \| ^ { 2 } } { 4 s ^ { 2 } } + P _ { \mathrm { t } } | \Delta _ { \hat { \theta } } ^ { \mathrm { b a } } \| ^ { 2 s } } } \\ { { } } & { { } } \\ { { } } & { { \displaystyle + P _ { 4 } \frac { \Delta _ { \hat { \theta } } } { 7 } \sum _ { \hat { \theta } ^ { \prime } } ^ { \Delta _ { \hat { \theta } ^ { \prime } } } ( P _ { 3 } + P _ { 4 } \| \frac { \Delta _ { \hat { \theta } ^ { \prime } } } { \hat { \cal T } _ { 2 } ^ { s } } | \frac { \Delta _ { \hat { \theta } ^ { \prime } } } { 4 s ^ { 2 } }  ) } } \\ { { } } &   \displaystyle \times \sqrt  \hat { \cal N } _ { 3 \mathrm { t } } \Delta _ { \hat { \theta } ^ { \prime } } ^  \mathrm \end{array}
$$

and $P _ { d }$ with $d = 1 , . . . , 7$ , is combinatorial constant corresponding to (1); $P _ { 7 }$ = 1is related to the magnitude of $\tilde { \mathbf { v } } _ { i j } ^ { \perp u } , \mathrm { i . e . , i f } \tilde { \mathbf { v } } _ { i j } ^ { \perp u }$ is 0, $P _ { 7 }$ is equal to $- \frac { W } { 2 } \sqrt { \frac { 2 W } { n _ { r } \rho A } }$ , otherwise $P _ { 7 }$ is equal to 0. (17) and (18) correspond to the maximum UAV speed constraint as well as the maximum segment length constraint. $\Delta _ { i j } ^ { u } \triangleq { \tilde { \mathbf { q } } } _ { i j } ^ { u + 1 } - { \tilde { \mathbf { q } } } _ { i j } ^ { u }$ and $\Delta _ { i j } ^ { h u } \triangleq \tilde { h } _ { i j } ^ { u + 1 } - \tilde { h } _ { i j } ^ { u }$ define the projection lengths of the uth line Îsegment in the horizontal and vertical directions, respectively.

According to the perspective operation preserver convexity [33], the third and seventh terms of (21) with respect to $\mathbf { Q } _ { 1 }$ $\mathbf { H } _ { 1 }$ and ${ \bf T } _ { 1 }$ are nonconvex, thus Problem ( . ) is nonconvex.

## B. SCA-Based Solution to Problem (P2.1)

To solve Problem ( . ), slack variables are introduced to P2 1convert this nonconvex problem into a convex one, and the SCA technique is further applied to address it.

The convexity of the third and seventh terms in (21) is changed by introducing three slack variables, including $\mathbf { B } = \{ B _ { i j } ^ { u } \geq$ $0 , \forall u \in \mathcal { U } \} , \mathbf { C } ^ { \bar { } } = \{ C _ { i j } ^ { u } \geq 0 , \forall u \in \mathcal { U } \}$ and $\mathbf { D } = \{ D _ { i j } ^ { u } \ge 0$ , âu â $\mathcal { U } \}$ , such that

$$
B _ { i j } ^ { u } = \sqrt { \sqrt { \tilde { T } _ { i j } ^ { u ^ { 4 } } + \frac { \Delta _ { i j } ^ { u ^ { 4 } } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \Delta _ { i j } ^ { u ^ { 2 } } } { 2 v _ { 0 } ^ { 2 } } } , \quad \forall u \in \mathcal { U } ,\tag{22}
$$

which is equivalent to

$$
\frac { \tilde { T } _ { i j } ^ { u ^ { 4 } } } { B _ { i j } ^ { u ^ { 2 } } } = { B _ { i j } ^ { u ^ { 2 } } } + \frac { \left\| \tilde { \mathbf { q } } _ { i j } ^ { u + 1 } - \tilde { \mathbf { q } } _ { i j } ^ { u } \right\| ^ { 2 } } { v _ { 0 } ^ { 2 } } , \quad \forall u \in \mathcal { U } ,\tag{23}
$$

$$
\begin{array} { r } { C _ { i j } ^ { u } = \sqrt { \Delta _ { i j } ^ { h u ^ { 2 } } + P _ { 5 } \left| \Delta _ { i j } ^ { h u } \right| \Delta _ { i j } ^ { h u } + P _ { 6 } \tilde { T } _ { i j } ^ { u ^ { 2 } } } , \forall u \in \mathcal { U } , } \end{array}
$$

and

(24)

$$
D _ { i j } ^ { u } = C _ { i j } ^ { u } \left( \frac { \tilde { h } _ { i j } ^ { u + 1 } - \tilde { h } _ { i j } ^ { u } } { \tilde { T } _ { i j } ^ { u } } \right) ^ { 2 } , ~ \forall u \in \mathcal { U } .\tag{25}
$$

Therefore, the third term of (21) can be replaced by the linear expressions $P _ { i n } B _ { i j } ^ { u }$ , with the additional Constraint (23). Besides, the seventh term of (21) can also replaced by $\begin{array} { r } { P _ { 8 } \left( \frac { C _ { i j } ^ { u ^ { 3 } } } { \tilde { T } _ { i j } ^ { u ^ { 2 } } } - D _ { i j } ^ { u } \right) } \end{array}$ , where $P _ { 8 }$ is equal to $\frac { n _ { r } A \rho } { 4 }$

By substituting the above slack variables, Problem ( . ) can be rewritten as

$$
\begin{array} { r l } { \langle \mathrm { P 2 2 } . 0 \rangle : \underset { \mathbf { Q } _ { \mathbf { b } } , \mathbf { H } , \mathbf { i } , \mathbf { i } , \mathbf { T } _ { 1 } } { \operatorname* { m i n } } \frac { U } { \delta } \Bigg [ P _ { b } \hat { I } _ { b , \mathbf { a } } ^ { \dagger \alpha } + P _ { 1 } \frac { \left. \Delta _ { b } ^ { \alpha } \right. ^ { 2 } } { \hat { I } _ { b , \mathbf { d } } ^ { \dagger \alpha } } + P _ { i h } B _ { i h } ^ { \alpha } } \\ & { \qquad + P _ { 2 } \frac { \left. \Delta _ { b } ^ { \alpha } \right. ^ { 3 } } { \hat { I } _ { b , \mathbf { b } } ^ { \dagger \alpha } } + P _ { 3 } \left. \Delta _ { b } ^ { \alpha } \right. + P _ { 4 } \frac { \Delta _ { b } ^ { \alpha } u ^ { \alpha } } { \hat { I } _ { b , \mathbf { a } } ^ { \dagger \alpha } } } \\ & { \qquad + P _ { 8 } \left( \frac { C _ { 8 } ^ { \alpha } } { \hat { I } _ { b , \mathbf { b } } ^ { \alpha } } - D _ { 9 } ^ { \alpha } \right) + P _ { 7 } \tilde { T } _ { 0 } ^ { \alpha } \Bigg ] , } \\ { \mathrm { s . t . } \frac { \hat { I } _ { 9 } ^ { \alpha + 1 } } { \Delta _ { \mathbf { b } } ^ { \alpha } u _ { 9 } ^ { \alpha } } \leq B _ { 0 } ^ { \alpha } + \frac { \left. \left. \tilde { \mathbf { q } } _ { 4 } ^ { \alpha } \right. ^ { 2 } - \tilde { \mathbf { q } } _ { 4 } ^ { \alpha } u _ { j } ^ { \alpha } \right. ^ { 2 } } { \hat { V } _ { 0 } ^ { \alpha } } , } \\ & { \qquad \quad \forall \mathrm { u } \in \mathcal { U } . } \end{array}\tag{26}
$$

$$
\begin{array} { r l r } & { C _ { i j } ^ { u } \geq \sqrt { \Delta _ { i j } ^ { h u ^ { 2 } } + P _ { 5 } \left| \Delta _ { i j } ^ { h u } \right| \Delta _ { i j } ^ { h u } + P _ { 6 } \tilde { T } _ { i j } ^ { u ^ { 2 } } } , } & \\ & { \forall u \in \mathcal { U } , } & { ( 2 \pi ^ { \circ } \mathbb { 1 } ^ { } \mathrm { ~ c ~ } } \end{array}\tag{7}
$$

$$
\begin{array} { r l } & { D _ { i j } ^ { u } \le C _ { i j } ^ { u } \left( \frac { \widetilde { h } _ { i j } ^ { u + 1 } - \widetilde { h } _ { i j } ^ { u } } { \widetilde { T } _ { i j } ^ { u } } \right) ^ { 2 } , } \\ & { \forall u \in \mathcal { U } , } \\ & { B _ { i j } ^ { u } \ge 0 , C _ { i j } ^ { u } \ge 0 , D _ { i j } ^ { u } \ge 0 , } \\ & { \forall u \in \mathcal { U } , } \\ & { ( 1 7 ) { - } ( 2 0 ) . } \end{array}\tag{28}
$$

(29)

Note that in Problem ( . ), constraints (26)â(28) are derived P2 2from (23)â(25) by replacing equalities with inequalities. This does not affect the equivalence between Problem ( . ) and P2 1Problem ( . ). The reason is that there always exists an optimal P2 2solution to Problem ( . ) that makes all constraints satisfied with strict equality.

Problem ( . ) is still nonconvex since constraints (26) and P2 2(28) are nonconvex. However, using the global lower/upper bounds of at a given local point to update these two nonconvex constraints can induce them to be convex. Due to the fact that the first-order Taylor expansion is a global lower bound of a convex function, the following inequality can be obtained for the right hand side (RHS) convex function of the nonconvex constraint (26) as

$$
\begin{array} { l } { \displaystyle B _ { i j } ^ { u ^ { 2 } } + \frac { \big \| \tilde { \mathbf { q } } _ { i j } ^ { u + 1 } - \tilde { \mathbf { q } } _ { i j } ^ { u } \big \| ^ { 2 } } { v _ { 0 } ^ { 2 } } \geq B _ { i j } ^ { u ( r ) ^ { 2 } } + 2 B _ { i j } ^ { u ( r ) } \left( B _ { i j } ^ { u } - B _ { i j } ^ { u ( r ) } \right) } \\ { \displaystyle \qquad - \frac { \big \| \tilde { \mathbf { q } } _ { i j } ^ { u + 1 ( r ) } - \tilde { \mathbf { q } } _ { i j } ^ { u ( r ) } \big \| ^ { 2 } } { v _ { 0 } ^ { 2 } } } \\ { \displaystyle \qquad + \frac { 2 } { v _ { 0 } ^ { 2 } } \left( \tilde { \mathbf { q } } _ { i j } ^ { u + 1 ( r ) } - \tilde { \mathbf { q } } _ { i j } ^ { u ( r ) } \right) ^ { T } } \\ { \displaystyle \qquad \times \left( \tilde { \mathbf { q } } _ { i j } ^ { u + 1 } - \tilde { \mathbf { q } } _ { i j } ^ { u } \right) } \\ { \displaystyle \qquad \triangleq a _ { i j } ^ { u } ( B _ { i j } ^ { u } , \tilde { \mathbf { q } } _ { i j } ^ { u } ) , } \end{array}\tag{0}
$$

where $B _ { i j } ^ { u ^ { ( r ) } }$ and $\tilde { \mathbf { q } } _ { i j } ^ { u ^ { ( r ) } }$ are the current values of the corresponding variables at the rth iteration.

Furthermore, it can be found that the RHS of the nonconvex Constraint (28) is a joint nonconvex function with respect to $C _ { i j } ^ { u } , \Delta _ { i j } ^ { h u }$ and $\tilde { T } _ { i j } ^ { u }$ . Following a similar analysis in the work [34], Îthe first-order Taylor expansion is a global upper bound of nonconvex functions, hence it can be obtained that

$$
\begin{array} { r } { C _ { i j } ^ { u } \left( \frac { \tilde { h } _ { i j } ^ { u + 1 } - \tilde { h } _ { i j } ^ { u } } { \tilde { T } _ { i j } ^ { u } } \right) ^ { 2 } \le \left( \frac { \tilde { h } _ { i j } ^ { u + 1 ^ { ( r ) } } - \tilde { h } _ { i j } ^ { u ^ { ( r ) } } } { \tilde { T } _ { i j } ^ { u ^ { ( r ) } } } \right) ^ { 2 } C _ { i j } ^ { u } + 2 C _ { i j } ^ { u ^ { ( r ) } } } \\ { \times \frac { \tilde { h } _ { i j } ^ { u + 1 ^ { ( r ) } } - \tilde { h } _ { i j } ^ { u ^ { ( r ) } } } { \tilde { T } _ { i j } ^ { u ^ { ( r ) } } } \left( \tilde { h } _ { i j } ^ { u + 1 } - \tilde { h } _ { i j } ^ { u } \right. } \\ { \left. - \tilde { h } _ { i j } ^ { u + 1 ^ { ( r ) } } + \tilde { h } _ { i j } ^ { u ^ { ( r ) } } \right) - 2 C _ { i j } ^ { u ^ { ( r ) } } } \end{array}
$$

$$
\begin{array} { r l r } {  { \times \frac { ( \tilde { h } _ { i j } ^ { u + 1 ^ { ( r ) } } - \tilde { h } _ { i j } ^ { u ^ { ( r ) } } ) ^ { 2 } } { \tilde { T } _ { i j } ^ { u ^ { ( r ) } ^ { 3 } } } ( \tilde { T } _ { i j } ^ { u } - \tilde { T } _ { i j } ^ { u ^ { ( r ) } } ) } } \\ & { \triangleq b _ { i j } ^ { u ^ { ( r ) } } ( C _ { i j } ^ { u } , \tilde { h } _ { i j } ^ { u } , \tilde { T } _ { i j } ^ { u } ) , } & { ( 3 1 } \end{array}
$$

where $\tilde { h } _ { i j } ^ { u ^ { ( r ) } } , \tilde { T } _ { i j } ^ { u ^ { ( r ) } }$ and $C _ { i j } ^ { u ^ { ( r ) } }$ are also the current values of corresponding variables at the rth iteration.

By replacing the RHS of the nonconvex constraints (26) and (28) with their corresponding lower bound $a _ { i j } ^ { u ^ { ( r ) } } ( B _ { i j } ^ { u } , \tilde { \mathbf { q } } _ { i j } ^ { u } )$ and upper bound $b _ { i j } ^ { u ^ { ( r ) } } ( C _ { i j } ^ { u } , \tilde { h } _ { i j } ^ { u } , \tilde { T } _ { i j } ^ { u } )$ at the rth iteration, respectively, it can be verified that Problem ( . ) is convex. P2 2Therefore, standard convex optimization techniques or existing software toolbox (e.g., CVX) can be used to solve Problem ( . ) efficiently. The SCA-based algorithm is summarized in P2 2Algorithm 1.

## C. Convexity Analysis of Inequality Constraints

The Hessian matrix is applied to confirm the convexity of inequality constraints. Concretely, confirming the convexity of standardized inequality constraints involves verifying the semidefiniteness of their LHS functionsâ Hessian matrices [35]; they are convex if semi-definite, and nonconvex otherwise. Since the work [11], [12] has analyzed the convexity of constraints similar to constraints (26) and (29), only the convexity of constraints (27) and (28) shall be discussed at this point.

Proposition 2: Constraint (27) is convex.

Proof: The LHS function of the standardized Constraint (27), denoted as $f ( C _ { i j } ^ { u } , \Delta _ { i j } ^ { h u } , \tilde { T } _ { i j } ^ { u } )$ , can be expressed as

$$
\begin{array} { r } { f ( C _ { i j } ^ { u } , \Delta _ { i j } ^ { h u } , \tilde { T } _ { i j } ^ { u } ) = \sqrt { \Delta _ { i j } ^ { h u ^ { 2 } } + P _ { 5 } \left| \Delta _ { i j } ^ { h u } \right| \Delta _ { i j } ^ { h u } + P _ { 6 } \tilde { T } _ { i j } ^ { u ^ { 2 } } } - C _ { i j } ^ { u } , } \end{array}\tag{32}
$$

where $- C _ { i j } ^ { u }$ is convex [33], and the convexity corresponding to the first term of (32), denoted as $f _ { 1 } ( \Delta _ { i j } ^ { h u } , \tilde { T } _ { i j } ^ { u } )$ , is validated by the Hessian matrix.

For ease of description, $\Delta _ { i j } ^ { h u }$ and $\tilde { T } _ { i j } ^ { u }$ are replaced by x and Îy, respectively, and the Hessian matrix of $f _ { 1 } ( \mathbf { x } , \mathbf { y } )$ , denoted as Hes1, is as follows

$$
H e s _ { 1 } = \left[ \begin{array} { l l } { \nabla _ { \mathbf { x } \mathbf { x } } ^ { 2 } f _ { 1 } } & { \nabla _ { \mathbf { x } \mathbf { y } } ^ { 2 } f _ { 1 } } \\ { \nabla _ { \mathbf { y } \mathbf { x } } ^ { 2 } f _ { 1 } } & { \nabla _ { \mathbf { y } \mathbf { y } } ^ { 2 } f _ { 1 } } \end{array} \right] .\tag{33}
$$

By calculating the second-order derivative, the closed-form expression of Hes1 is given as

$$
\begin{array} { r l } & { \nabla _ { \mathbf x \mathbf x } ^ { 2 } f _ { 1 } = \frac { P _ { 6 } ( 1 + s g n ( \mathbf x ) P _ { 5 } ) \mathbf y ^ { 2 } } { ( ( 1 + s g n ( \mathbf x ) P _ { 5 } ) \mathbf x ^ { 2 } + P _ { 6 } \mathbf y ^ { 2 } ) ^ { \frac { 3 } { 2 } } } , } \\ & { \nabla _ { \mathbf y \mathbf y } ^ { 2 } f _ { 1 } = \frac { P _ { 6 } ( 1 + s g n ( \mathbf x ) P _ { 5 } ) \mathbf x ^ { 2 } } { ( ( 1 + s g n ( \mathbf x ) P _ { 5 } ) \mathbf x ^ { 2 } + P _ { 6 } \mathbf y ^ { 2 } ) ^ { \frac { 3 } { 2 } } } , } \\ & { \nabla _ { \mathbf x \mathbf y } ^ { 2 } f _ { 1 } = \nabla _ { \mathbf y \mathbf x } ^ { 2 } f _ { 1 } = \frac { P _ { 6 } ( 1 + s g n ( \mathbf x ) P _ { 5 } ) \mathbf x \mathbf y } { ( ( 1 + s g n ( \mathbf x ) P _ { 5 } ) \mathbf x ^ { 2 } + P _ { 6 } \mathbf y ^ { 2 } ) ^ { \frac { 3 } { 2 } } } , } \end{array}\tag{34}
$$

where $\nabla _ { \mathbf x \mathbf x } ^ { 2 } f _ { 1 }$ is greater than 0 due to that $| s g n ( { \bf x } ) P _ { 5 } |$ is less than 1 [36].

On this basis, the size of $H e s _ { 1 }$ , defined as $| H e s _ { 1 } | .$ , satisfies

$$
| H e s _ { 1 } | = \nabla _ { \mathbf { x } \mathbf { x } } ^ { 2 } f _ { 1 } \nabla _ { \mathbf { y } \mathbf { y } } ^ { 2 } f _ { 1 } - \nabla _ { \mathbf { x } \mathbf { y } } ^ { 2 } f _ { 1 } \nabla _ { \mathbf { y } \mathbf { x } } ^ { 2 } f _ { 1 } = 0 .\tag{35}
$$

Thus, $H e s _ { 1 }$ is semi-definite on account of $\nabla _ { \mathbf { x } \mathbf { x } } ^ { 2 } f _ { 1 }$ and $| H e s _ { 1 } |$ being non-negative, and the constraint (27) is convex.

Proposition 3: Constraint (28) is nonconvex.

Proof: Likewise, as $D _ { i j } ^ { u }$ is convex, demonstrating that the negative of Constraint (28)âs RHS function, represented by $f _ { 2 } ( C _ { i j } ^ { u } , \Delta _ { i j } ^ { h u } , \tilde { T } _ { i j } ^ { u } )$ , is nonconvex can confirm the non-convexity ( Î )of (28). This entails proving that the Hessian matrix of $f _ { 2 } ( C _ { i j } ^ { u } , \Delta _ { i j } ^ { h u } , \tilde { T } _ { i j } ^ { u } )$ , denoted as Hes2, is non-semi-definite, which ( Î )can be expressed as

$$
H e s _ { 2 } = \left[ \begin{array} { c c c } { \nabla _ { \mathbf { a a } } ^ { 2 } f _ { 2 } } & { \nabla _ { \mathbf { a b } } ^ { 2 } f _ { 2 } } & { \nabla _ { \mathbf { a c } } ^ { 2 } f _ { 2 } } \\ { \nabla _ { \mathbf { b a } } ^ { 2 } f _ { 2 } } & { \nabla _ { \mathbf { b b } } ^ { 2 } f _ { 2 } } & { \nabla _ { \mathbf { b c } } ^ { 2 } f _ { 2 } } \\ { \nabla _ { \mathbf { c a } } ^ { 2 } f _ { 2 } } & { \nabla _ { \mathbf { c b } } ^ { 2 } f _ { 2 } } & { \nabla _ { \mathbf { c c } } ^ { 2 } f _ { 2 } } \end{array} \right] ,\tag{36}
$$

where a, b and c stand for $C _ { i j } ^ { u } , \Delta _ { i j } ^ { h u }$ and $\tilde { T } _ { i j } ^ { h }$ , respectively.

By computing $\nabla _ { \mathbf { a a } } ^ { 2 } f _ { 2 } , \nabla _ { \mathbf { a b } } ^ { 2 } \mathbf { \bar { f } } _ { 2 } , \omega _ { \mathbf { b a } } ^ { 2 } f _ { 2 }$ and $\nabla _ { \mathbf { b } \mathbf { b } } ^ { 2 } f _ { 2 }$ , the size of Hes2âs second-order principal subform, denoted as $| H e s _ { 2 , 2 } | ,$ can be expressed in closed form as

$$
\begin{array} { c } { { | H e s _ { 2 , 2 } | = \nabla _ { \mathbf { a a } } ^ { 2 } f _ { 2 } \nabla _ { \mathbf { b b } } ^ { 2 } f _ { 2 } - \nabla _ { \mathbf { a b } } ^ { 2 } f _ { 2 } \nabla _ { \mathbf { b a } } ^ { 2 } f _ { 2 } } } \\ { { \ } } \\ { { \displaystyle = 0 \times \left( - \frac { 2 \mathbf { a } } { \mathbf { c } ^ { 2 } } \right) - \left( - \frac { 2 \mathbf { b } } { \mathbf { c } ^ { 2 } } \right) \times \left( - \frac { 2 \mathbf { b } } { \mathbf { c } ^ { 2 } } \right) } } \\ { { \ } } \\ { { \displaystyle = - \frac { 4 \mathbf { b } ^ { 2 } } { \mathbf { c } ^ { 4 } } . } } \end{array}\tag{37}
$$

Since $| H e s _ { 2 , 2 } |$ is negative, $| H e s _ { 2 } |$ is non-semi-definite, thus Constraint (28) is nonconvex.

## D. Performance Analysis of Algorithm 1

To further demonstrate the feasibility of Algorithm 1, the performance of Algorithm 1 is analyzed in terms of complexity and convergence, respectively.

1) Convergence Analysis: Inspired by convergence analysis in [37], it can be concluded that Algorithm 1 provides a sequence of non-increasing values over the iteration, and its convergence is guaranteed. The proof is as follows, Problem ( . ) is transformed as Problem ( . ); the nonconvex Problem ( . ) is approximated with convex surrogate Problem ( . ) in each P2 2iteration and Problem ( . ) is solved iteratively. According to P2 2the characteristics of the SCA technique, it follows that

$$
E _ { 1 } \left( { \bf Q } _ { 1 } ^ { u } , { \bf H } _ { 1 } ^ { u } , { \bf T } _ { 1 } ^ { u } \right) \ge E _ { 1 } \left( { \bf Q } _ { 1 } ^ { u + 1 } , { \bf H } _ { 1 } ^ { u + 1 } , { \bf T } _ { 1 } ^ { u + 1 } \right) .\tag{38}
$$

Therefore, the objective value of Problem ( . ) is non-P2 1increasing. Since the objective value of Problem ( . ) is lower P2 1bounded by a finite value, Algorithm 1 is guaranteed to converge.

2) Complexity Analysis: According to the analysis in [38], since Problem ( . ) is solved by the CVX solver, the overall P2 2computational complexity of Algorithm 1 can be easily given as $\bar { \mathcal { O } } ( U ^ { 3 . 5 } \log \frac { 1 } { \epsilon } )$ , where  is a given threshold that determines ( log )the termination of Algorithm 1, i.e., the algorithm halts when the percentage decrease in the objective values of the solutions generated during its execution falls below this threshold.

Remark 1: Based on Algorithm 1, the energy consumption of UAVs accessing GN i and GN j sequentially in linear flight (which is considered in Section VI) can also be minimized by adding a constraint, i.e., $\| \tilde { \mathbf { q } } _ { i j } ^ { u + 1 } - \tilde { \mathbf { q } } _ { i j } ^ { u } \| \cdot | H _ { j } - H _ { i } | = \| \mathbf { w } _ { j } - \mathbf  \bar $ $\mathbf { w } _ { i } \| \cdot | \tilde { h } _ { i j } ^ { u + 1 } - \tilde { h } _ { i j } ^ { u } | , \forall u \in \mathcal { U } .$ , to Problem (P 2.2).

Algorithm 1: SCA-Based Algorithm.   
1: Initialization: obtain a feasible $\{ \tilde { \mathbf { q } } _ { i j } ^ { u ^ { ( 0 ) } } \} , \{ \tilde { T } _ { i j } ^ { u ^ { ( 0 ) } } \}$   
$\{ \tilde { h } _ { i j } ^ { u ^ { ( 0 ) } } \} , ~ { \{ B _ { i j } ^ { u ^ { ( 0 ) } } \} } , ~ { \{ C _ { i j } ^ { u ^ { ( 0 ) } } \} }$ and $\{ D _ { i j } ^ { u ^ { ( 0 ) } } \}$ of Problem   
( . ). Set $r \stackrel { } { = } 0$   
P2 22: repeat   
3: Replace the right hand side of (26) and (28) with   
$a _ { i j } ^ { u ^ { ( r ) } } ( B _ { i j } ^ { u } , \tilde { \mathbf { q } } _ { i j } ^ { u } )$ and $b _ { i j } ^ { u ^ { ( r ) } } ( C _ { i j } ^ { u } , \tilde { h } _ { i j } ^ { u } , \tilde { T } _ { i j } ^ { u } )$ , respectively.   
4: Solve the convex Problem ( . ), and denote the   
opti- mal solution as $\{ \tilde { \mathbf { q } } _ { i j } ^ { u ^ { * } } \} , \{ \tilde { T } _ { i j } ^ { u ^ { * } } \} , \{ \tilde { h } _ { i j } ^ { u ^ { * } } \} , \{ B _ { i j } ^ { u ^ { * } } \}$   
$\{ C _ { i j } ^ { u ^ { * } } \}$ and $\{ D _ { i j } ^ { u ^ { * } } \}$ Â·   
5: Update the local point $\tilde { \mathbf { q } } _ { i j } ^ { u ^ { ( r + 1 ) } } = \tilde { \mathbf { q } } _ { i j } ^ { u ^ { * } } ,$   
$\tilde { T } _ { i j } ^ { u ^ { ( r + 1 ) } } = \tilde { T } _ { i j } ^ { u ^ { * } } , \tilde { h } _ { i j } ^ { u ^ { ( r + 1 ) } } = \tilde { h } _ { i j } ^ { u ^ { * } } , B _ { i j } ^ { u ^ { ( r + 1 ) } } = B _ { i j } ^ { u ^ { * } } .$   
$C _ { i j } ^ { u ^ { ( r + 1 ) } } = C _ { i j } ^ { u ^ { * } }$ and $D _ { i j } ^ { u ^ { ( r + 1 ) } } = D _ { i j } ^ { u ^ { * } }$   
6: Update $r = r + 1 .$   
7: = + 1until the percentage decrease of the objective value of   
( . ) is below a given threshold  or the number of   
P2 2iterations reaches $N _ { \epsilon }$

## V. MPSO AND GPA FOR SOLVING PROBLEM (P3)

This section provides a novel framework to solve Problem ( ) to obtain the minimum number of UAVs and the minimum total UAV energy consumption.

## A. Preliminaries

Prior to presenting the proposed framework, a two-stage scheme for minimizing the number of UAVs designed in [39] is introduced. It is specified as follows, first, obtaining an optimal tour, which consists of the path points passed by a UAV with sufficient energy to fulfill tasks with the minimum flight distance; second, decomposing the optimal tour into several short tours, and ensuring that the UAV energy consumption of each short tour does not exceed a fixed energy consumption upper bound. More importantly, calculating the minimum number of these short tours to approximate the minimum number of UAVs.

Inspired by this, a three-stage framework based on MPSO and GPA is developed to solve Problem ( ). Concretely, in the P3first stage, the MPSO algorithm is proposed to obtain an optimal sequence, namely $O ^ { * }$ , which minimizes the energy consumption required for all GNs to be accessed by a UAV. In the second stage, the GPA algorithm is designed to decompose $O ^ { * }$ into $M _ { p }$ subsequences, i.e., $O _ { 1 } , O _ { 2 } , . . . , O _ { M _ { p } }$ , the minimum $M _ { p }$ is served as the minimum number of UAVs. On this basis, in the third stage, given that Problem ( ) is approximated as a MTSP (see details in Proposition 1), the MPSO algorithm is reused to solve Problem ( ) to derive the minimum total UAV energy consumption.

In the following, the two algorithms involved in the proposed framework are described.

<!-- image-->  
Fig. 3. Schematics of the crossover and mutation operations.

## B. Modified Particle Swarm Optimization

The MPSO algorithm focuses on improving the search capability of the traditional PSO algorithm by introducing crossover and mutation operations from the genetic algorithm (GA). For ease of understanding, the MPSO algorithm is explained in four parts as follows. The overall algorithm is summarized in Algorithm 2.

1) Initialization: Initialization determines the initial population and the initial optimal solutions of the algorithm. The initial population, composed of L particles, denoted as $P _ { a } ^ { l } ,$ $l = 1 , . . . , L ,$ each with a GN-accessing sequence of dimension = 1N , collectively forms the initial local optima (termed lbest); moreover, the global optima (termed gbest) are initialized as the particles with the smallest fitness value. The sequences of local optima and global optima, namely $l b e s t _ { r e c o r d }$ and gbestrecord, respectively, are recorded.

2) Fitness: Fitness guides the optimization search direction of the algorithm. In the algorithm, particlesâ fitness is gauged by the energy required for UAVs to execute tasks corresponding to those particlesâ GN-accessing sequences, as calculated using (9). The particles with the smallest fitness value are chosen as the optimal particles in each iteration, concurrently, the GNaccessing sequences in these optimal particles are treated as the current optimal solutions.

3) Crossover: Crossover improves the global search capability of the algorithm. In each iteration, the partially matched crossover (PMX) strategy is employed to mix the current particlesâ solutions (i.e., the GN-accessing sequences) with $l b e s t _ { r e c o r d }$ (or $g b e s t _ { r e c o r d } )$ to generate crossed particles. This approach preserves the superior traits of the parent particles while introducing new particles to increase diversity, broadening the global search range of the algorithm. See the left side of Fig. 3 for details.

4) Mutation: Mutation improves the local search capability of the algorithm. In each iteration, the GNs at any two positions in the crossed particlesâ GN-accessing sequences are swapped, introducing new variants. This prevents the algorithm from converging prematurely to local optima. On this basis, the particles with the smallest fitness value are chosen to update gbest, lbest, $g b e s t _ { r e c o r d }$ and $l b e s t _ { r e c o r d }$ . See the right side of Fig. 3 for details.

Remark 2: The third stageâs MPSO algorithm for solving MTSP, readily inferable from Algorithm 2, is omitted here for clarity.

Algorithm 2: MPSO Algorithm.   
1: Input: L random particles $P _ { a } ^ { l } , l = 1 , . . . , L$ , the   
number of iterations $i t _ { n } , E _ { \mathrm { m a x } } ,$ = 1lbest, lbestrecord,   
gbest, gbestrecord.   
2: Output: tour $O ^ { * } .$   
3: while $i t _ { n } \neq 0$ do   
4: for $i \gets 1$ 0to L do   
5: Cross $P _ { a } ^ { i }$ and $l b e s t ^ { i } ;$   
6: Judge constraints and calculate the fitness values   
by using (9);   
7: if $E _ { P _ { a } ^ { i } } < E _ { l b e s t ^ { i } }$ then   
8: Update $E _ { l b e s t ^ { i } }$ and $l b e s t _ { r e c o r d } ^ { i } ;$   
9: end if   
10: if $E _ { l b e s t ^ { i } } < E _ { g b e s t ^ { i } }$ then   
11: Update $E _ { g b e s t ^ { i } }$ and $g b e s t _ { r e c o r d } ^ { i } ;$   
12: end if   
13: Cross $P _ { a } ^ { i }$ and $g b e s t ^ { i } ;$   
14: Repeat, calculate and update by using (9);   
15: Mutate $P _ { a } ^ { i } ;$   
16: Repeat, calculate and update by using (9);   
17: end for   
18: $i t _ { n } \gets i t _ { n } - 1 ;$   
19: end while   
20: Find minimum $E _ { g b e s t } ^ { * }$ and corresponding $g b e s t _ { r e c o r d } ^ { * } ;$   
21: $O ^ { * } \gets g b e s t _ { r e c o r d } ^ { * } ;$   
22: return $O ^ { * } ;$

## C. Greedy Path Assignment

In the GPA algorithm, the global optimal GN-accessing sequence obtained by the MPSO algorithm is divided into several local optimal GN-accessing subsequences via path assignment, and the number of local optimal subsequences represents the minimum number of UAVs. In each path assignment round, the GPA algorithm selects the first longest subsequence of the current global optimal sequence, with corresponding UAV energy consumption under $E _ { \mathrm { m a x } }$ , as the local optimal subsequence. Note that after each path assignment, the global optimal sequence is updated by removing the GNs in the local optimal subsequence selected in the current round.

The following lemma and theorem will further prove the feasibility of the GPA algorithm.

Lemma 1: The problem of minimizing the energy consumed by a UAV to access N GNs has the optimal substructure.

Proof: First, considering the optimal solution sequence, namely $O ^ { * } = \{ g _ { 1 } , g _ { 2 } , . . . , g _ { N } \}$ , for this problem. It is assumed that for any $k \in [ 1 , N ]$ , the set $G = \left\{ g _ { 1 } , g _ { 2 } , \ldots , g _ { k } \right\}$ , including [1 ] =the first k GNs, is proven to have an optimal substructure.

Then, incorporating $g _ { k + 1 }$ to the set G results in the expanded the set $G ^ { \prime } = \left\{ g _ { 1 } , g _ { 2 } , \ldots , g _ { k } , g _ { k + 1 } \right\}$ . Among all possible paths =leading to gk+1 except for $g _ { k + 1 }$ itself, the path from $g _ { k } \operatorname { t o } g _ { k + 1 }$ is the one with the minimum energy consumption. This is because the existence of any other GN $g _ { i } , i \in \{ 1 , \ldots , k , k + 2 , \ldots , N \}$ 1that offers a smaller energy consumption path to $g _ { k + 1 }$ would contradict the optimal $O ^ { * }$

As a result, the set $G ^ { \prime }$ consisting of the first $k + 1$ GNs is + 1optimal and also has an optimal substructure. Therefore, this problem has an optimal substructure. â¡

Theorem $\mathit { l } \cdot$ The first longest subsequence satisfying the $E _ { \mathrm { m a x } }$ constraint is the first optimal subsequence.

Proof: Following Lemma 1, the sequence consisting of any consecutive $k \in [ 1 , N ]$ GNs in the optimal GN sequence $O ^ { * }$ is an [1 ]optimal subsequence. Therefore, the first optimal subsequence containing k GNs is the first k terms of $O ^ { * }$ . If k is related to $E _ { \mathrm { m a x } }$ at this point, i.e., it satisfies conditions $\begin{array} { r } { E _ { 0 1 } + \sum _ { i = 1 , j = i + 1 } ^ { k - 2 } E _ { i j } + } \end{array}$ $E _ { ( k - 1 ) 0 } \leq E _ { \operatorname* { m a x } }$ , and $\begin{array} { r } { E _ { 0 1 } + \sum _ { i = 1 , j = i + 1 } ^ { k - 1 } E _ { i j } + \bar { E } _ { k 0 } > { E _ { \mathrm { m a x } } } , } \end{array}$ +the first longest subsequence satisfying the $E _ { \mathrm { m a x } }$ constraint is the first k-term optimal subsequence. Note that i and $j$ in $E _ { i j }$ correspond to the ith and jth terms in $O ^ { * }$ at this point, respectively. 

## D. Performance Analysis of MPSO-GPA

In this subsection, the convergence analysis and the complexity analysis of MPSO-GPA are provided.

1) Convergence Analysis: The convergence of MPSO-GPA mainly depends on the convergence of the MPSO algorithm and the convergence of the GPA algorithm. Specifically, first, following the analysis of the traditional PSO algorithm in [40], it can be known that the convergence of the MPSO algorithm is mainly related to the particle updating, i.e., crossover and mutation; moreover, [41] has elaborated that crossover and mutation can guarantee the convergence of the genetic algorithm. Hence, the MPSO algorithm is convergent. Second, since the greedy-based algorithm is convergent [42], the GPA algorithm is convergent. Thus, MPSO-GPA is convergent.

2) Complexity Analysis: The computational complexity of MPSO-GPA is correspondingly associated with both the MPSO and GPA algorithms. In MPSO-GPA, the MPSO algorithm deals with a TSP and a MTSP, and the GPA algorithm deals with a path assignment problem. The two computational complexities corresponding to the former are $\mathcal { O } ( N \cdot L \cdot i t _ { n } )$ and $\mathcal { O } ( M \cdot N \cdot L \cdot i t _ { n } )$ ( ), respectively, while the latter corre-( )sponds to the computational complexity of O N . Therefore, ( )the computational complexity of MPSO-GPA is $\mathcal { O } ( M \cdot N$ $L \cdot i t _ { n } )$

## VI. SIMULATION SETUP AND RESULTS

In this section, simulations are performed to evaluate the effectiveness of the proposed methods. First, the simulation setup is given. Then, the minimum energy consumption and the minimum energy consumption rate of UAVs under linear trajectories and optimized trajectories are compared. Next, the performance of the MPSO algorithm and the MPSO-GPA algorithm in solving single-UAV and multi-UAV GN-accessing problems are evaluated, respectively, and finally, the feasibility of the overall algorithms is further emphasized. All methods are implemented in MATLAB and the detailed simulation results are presented as follows.

Algorithm 3: GPA Algorithm.   
1: Input: tour $\overline { { O ^ { * } , E _ { \mathrm { m a x } } } } .$   
2: $/ / O ^ { * }$ is obtained based on Algorithm 2 and expressed   
as $\left\{ g _ { 0 } , g _ { 1 } , g _ { 2 } , . . . , g _ { N } , g _ { 0 } \right\}$   
3: Output: minimum number of UAVs $M _ { p } .$   
4: Initialization: $M _ { p } \gets 0 , i \gets 1$ and $j  1$ , where i   
and $j$ 0 1 1are indexes of the first and last GNs in the next   
tour, respectively.   
5: while $j \leq N$ do   
6: $O _ { M _ { p } } \gets \{ g _ { 0 } , g _ { i } , g _ { i + 1 } , . . . , g _ { j } , g _ { 0 } \} ;$   
7: if ${ \cal E } _ { { \cal O } _ { M _ { p } } } \leq { \cal E } _ { \mathrm { m a x } }$ then   
8: $\mathbf { i f } \ j = = N$ then   
9: $/ /$ ==The last energy-efficient tour.   
10: $O _ { M _ { p } } \gets \{ g _ { 0 } , g _ { i } , g _ { i + 1 } , . . . , g _ { N } , g _ { 0 } \} ;$   
11: else   
12: $/ /$ Contain one more GN.   
13: $j  j + 1 ;$   
14: end if   
15: else   
16: $j  j - 1 ;$   
17: $O _ { M _ { p } } \gets \{ g _ { 0 } , g _ { i } , g _ { i + 1 } , . . . , g _ { j } , g _ { 0 } \} ;$   
18: $M _ { p } \gets M _ { p } + 1 ;$   
19: $/ /$ + 1Initialize the next energy-efficient tour.   
20: ${ \cal O } _ { M _ { p } } \gets \{ g _ { 0 } , g _ { 0 } \} ;$   
21: $j  j + 1 ;$   
22: $i  j ;$   
23: end if   
24: end while   
25: return $M _ { p } ;$

## A. Simulation Setup

The parameters involved in the simulation are illustrated as follows. The maximum flight altitude of the UAV $H _ { \mathrm { m a x } }$ is set to 500 m, which is consistent with the altitude setting in [43]. Regarding GN-accessing, a large number of GNs are randomly deployed in a $1 0 0 0 \mathrm { ~ m ~ } \times \mathrm { ~ } 1 0 0 0$ m square area, and the altitude required to access each GN is random. Regarding UAV trajectories, referring to the setup in [11], [12], $\Delta _ { \mathrm { m a x } } ^ { \mathrm { \bar { \parallel } } }$ and $\Delta _ { \mathrm { m a x } } ^ { \perp }$ are set Î Îto 30 m and 5 m, respectively, and the number of line segments U is set to 200. Regarding the MPSO algorithm, the maximum number of iterations is set to 1000, the initial population size is set to 200, and the crossover probability and mutation probability are 0.9 and 0.1, respectively. The parameter values related to the UAV propulsion energy consumption are derived from experimental measurements in our previous work [20] (see Table II). The maximum UAV horizontal speed $V _ { \mathrm { m a x } } ^ { \parallel }$ and the maximum UAV vertical speed $V _ { \mathrm { m a x } } ^ { \perp }$ are set to 30 m/s and 5 m/s [20], [44], respectively.

## B. Performance Evaluation of the UAV Trajectory Optimization for Energy Minimization

The minimum energy consumption and the minimum energy consumption rate of a UAV consecutively accessing two GNs under the optimized trajectory and linear trajectory are analyzed.

<!-- image-->  
Fig. 4. Energy consumption optimization percentage versus $k _ { I F }$ for a UAV in two statuses.

First, two sets of GN pairs are designed to facilitate the discussion of the UAV trajectory in the ascent and descent statuses. Taking the ascent status as an example, the first term and the second term of a GN pair represent the initial and final points, respectively, and the corresponding 3-D coordinates of the first term are set to (0,0,0), while the magnitude of the 2-D coordinates and the height corresponding to the second term are set to $H _ { \mathrm { m a x } }$ and $H _ { \operatorname* { m a x } } / k _ { I F } ,$ , respectively, where $k _ { I F }$ is defined as the ratio of the relative height and the relative horizontal distance between these two points. Moreover, the GN pairs designed for the UAV in the descent status are determined by interchanging the terms of the above GN pairs.

Then, to evaluate the difference of the minimum energy consumption for UAVs under these two trajectories, define $\frac { E _ { l } ^ { * } - E _ { o } ^ { * } } { E _ { l } ^ { * } } \times 1 0 0 \%$ to be the energy consumption optimization percentage, where $E _ { l } ^ { * }$ and $E _ { o } ^ { * }$ are the minimum energy consumption for UAVs under the linear trajectory and the optimized trajectory, respectively. Fig. 4 plots the energy consumption optimization percentages for the UAV in the ascent and descent flight statuses versus $k _ { I F }$ , respectively.

As can be seen, in most cases, the energy consumed by the UAV under the optimized trajectory is less than that consumed under the linear trajectory (i.e., the energy consumption optimization percentage is greater than 0). Specifically, in the ascent status, the energy optimization percentage is always greater than 0 and increases to around 8.5% with increasing $k _ { I F }$ before leveling off; in the descent status, the energy optimization percentage of the UAV is also not less than 0, and only when $k _ { I F }$ is less than / , the energy optimization percentage of the UAV is equal to 0, indicating that the optimized trajectory of the UAV is linear at this time.

Next, in the same way, to evaluate the difference of the minimum energy consumption rates for UAVs under these two trajectories, define $\frac { E _ { l } ^ { * } } { D _ { l } } - \frac { \mathbf { \hat { \boldsymbol { E } } } _ { o } ^ { * } } { D _ { o } }$ to be the energy consumption rate optimization, where $\dot { D } _ { l }$ and $D _ { o }$ are the flight distances of UAVs under the linear trajectory and the optimized trajectory, respectively. Fig. 5 plots the energy consumption rate optimization for UAVs in the ascent and descent statuses versus $k _ { I F } ,$ respectively.

It can be found that the energy consumption rate optimization of the UAV is always positively related to $k _ { I F }$ . Interestingly, given the same $k _ { I F }$ , the energy consumption rate optimization of the UAV in the ascent status is usually larger than that in the descent status since the UAV requires more energy in the ascent status [20]. This phenomenon becomes more significant as $k _ { I F }$ increases.

<!-- image-->  
Fig. 5. Energy consumption rate optimization versus $k _ { I F }$ for a UAV in two statuses.

## C. Performance Evaluation of MPSO-GPA

In order to fully evaluate the performance of MPSO-GPA, three efficiencies are analyzed from three perspectives. First, the efficiency of the MPSO algorithm and benchmarks is compared. Second, the efficiency of MPSO-GPA and the algorithms that integrate benchmarks and GPA is compared. Third, the efficiency of MPSO-GPA in two multi-UAV flight planning problems is compared. The following six optimization algorithms are introduced as benchmarks:

- Genetic Algorithm (GA) [45]: GA is an efficient and parallel global search algorithm.

Branch-and-Bound (BnB) [17]: BnB is a popular exact algorithm that searches for the optimal solution by constructing a search tree.

- Nearest Neighbour (NN) [18]: NN is the simplest heuristic algorithm and usually has a fast execution speed.

- Particle Swarm Optimization (PSO) [46]: PSO is a simple algorithm and has a fast search speed.

- Modified Ant Colony Optimization (MACO) [47]: MACO is a varied type of the ACO algorithm characterized by superior search efficacy and faster convergence speed.

- Modified Genetic Algorithm (MGA) [48]: MGA is a varied type of GA characterized by a stronger global search capability.

First, considering energy-efficient single-UAV path planning problems with different GN sizes, the performance of the MPSO algorithm and benchmarks in solving these problems is evaluated. The size of GNs varies from 30 to 300, and the position of each GN is random, the maximum energy each UAV can utilize is set to $E _ { \mathrm { m a x } } = \infty$ . To improve the reliability of the simulation =results, each simulation is repeated 30 times, and the average value is shown in Fig. 6.

As illustrated in Fig. 6(a), the MPSO algorithm minimizes energy consumption better than benchmarks. Specifically, compared with the PSO algorithm, the energy optimization efficiency of the MPSO algorithm is improved by an average of around 46.07%. Interestingly, it can be observed from Fig. 6(b) that the algorithms with better energy consumption optimization also tend to derive less UAV flight time; meanwhile, the energy consumption and the flight time of UAVs obtained by these algorithms show an approximately linear relationship proportional to the number of GNs, reflecting the stability of these algorithms. In addition, it can be intuitively found from Fig. 6(c) that the MACO algorithm consistently exhibits the longest execution time, while the simpler NN algorithm maintains the shortest duration. Apart from the aforementioned extremes, the MPSO algorithm consistently ranks high in execution time, only outpaced by the BnB algorithm when the number of GNs exceeds 240. Although the execution time of the MPSO algorithm is not small, this high computational complexity in exchange for the significant reduction in energy consumption and flight time of UAVs makes the MPSO algorithm more feasible in practice.

<!-- image-->  
(a) The UAV energy consumption.

<!-- image-->  
(b) The UAV flight time.

<!-- image-->  
(c) The algorithm execution time.

Fig. 6. Algorithm performance comparison for single-UAV path planning problems.  
<!-- image-->  
(a) $E _ { \mathrm { m a x } } = 1 2 0 \mathrm { \ k J } .$

<!-- image-->  
(b) $E _ { \mathrm { m a x } } = 1 6 0 ~ \mathrm { k J } .$

<!-- image-->  
(c) $E _ { \mathrm { m a x } } = 2 0 0 ~ \mathrm { k J } .$  
Fig. 7. Algorithm performance comparison for the minimum number of UAVs in multi-UAV path planning problems with different $E _ { \mathrm { m a x } } .$

Second, considering energy-efficient multi-UAV path planning problems with different GN sizes, the results obtained by the seven integrated approximation algorithms in solving these problems are presented. Following the similar setup as above (modifications are restricted to the GN range from 100 to 500), the minimum number of UAVs in three $E _ { \mathrm { m a x } }$ cases, i.e., 120 kJ, 160 kJ, and 200 kJ, are shown in Fig. 7, and the bars in Fig. 8 record corresponding energy consumption and flight time of UAVs. Expectedly, in terms of energy consumption and flight time, the stability of algorithms such as the MPSO algorithm and GA pushes the frameworks based on them to maintain similar performance in multi-UAV path planning; only GA-GPA shows fatigue with increasing GN size. Therefore, more attention is paid to analyzing the minimum number of UAVs.

In Fig. 7(a), the good performance of the MPSO algorithm leads MPSO-GPA to minimize the number of UAVs efficiently as expected. As $E _ { \mathrm { m a x } } = 1 2 0 \mathrm { k J }$ , this phenomenon becomes more =significant as the number of GNs increases.

Interestingly, it can be found from Fig. 7(b) and (c) that the minimum number of UAVs required remains constant when the number of GNs is within some specific interval. For example, when $E _ { \mathrm { m a x } } = 1 6 0$ kJ and the number of GNs is between 100 and = 160150, the minimum number of UAVs obtained by MPSO-GPA remains constant; when $E _ { \mathrm { m a x } } = 2 0 0$ kJ and the number of GNs = 200is between 200 and 250, the minimum number of UAVs obtained by GA-GPA remains constant. The reason is that the increase of $E _ { \mathrm { m a x } }$ expands the coverage of UAVs.

Overall, regarding the three $E _ { \mathrm { m a x } }$ cases, the efficiency of MPSO-GPA in minimizing the number of UAVs compared to other algorithms is up to around 47.83%, 50% and 46.15%, respectively.

Lastly, to further highlight the performance of MPSO-GPA, the minimum energy consumption and the minimum number of UAVs obtained by MPSO-GPA in solving two multi-UAV path planning problems, i.e., considering energy consumption costs and considering path distance costs, are compared. The results (see Table III) show that the former involves more than 50% reduction in both the energy consumption and the number of UAVs after optimization compared to the latter. In addition, the optimization efficiency of MPSO-GPA is less affected by the fluctuation of the GN number, verifying the robustness of the algorithm.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼

<!-- image-->  
(d)

<!-- image-->  
(e)

<!-- image-->  
(f)  
Fig. 8. Mean UAV energy consumption and mean UAV flight time for three $E _ { \mathrm { m a x } }$ cases in multi-UAV flight planning problems ((a), (b) and (c) represent the mean energy consumption for three $\bar { E } _ { \mathrm { m a x } }$ cases, i.e., 120 kJ, 160 kJ, and 200 kJ, respectively, likewise, (d), (e), and (f) correspond to the mean flight time for each of these three cases).

TABLE III  
MEAN UAV ENERGY CONSUMPTION AND MEAN NUMBER OF UAVS REQUIRED FOR TWO MULTI-UAV PATH PLANNING PROBLEMS
<table><tr><td colspan="3">Instance</td><td colspan="2">Energy (kJï¼</td><td colspan="2">Number</td></tr><tr><td>num</td><td>N</td><td> $\overline { { E _ { \mathrm { m a x } } } }$  (kJ)</td><td>energy- based</td><td>distance- based</td><td>energy- based</td><td>distance- based</td></tr><tr><td>1</td><td>100</td><td>120</td><td>279.3</td><td>670.7</td><td>3</td><td>7</td></tr><tr><td>2</td><td>100</td><td>160</td><td>278.2</td><td>671.8</td><td>2</td><td>5</td></tr><tr><td>3</td><td>100</td><td>200</td><td>279.8</td><td>675.3</td><td>2</td><td>4</td></tr><tr><td>4</td><td>200</td><td>120</td><td>558.6</td><td>1341.4</td><td>6</td><td>12</td></tr><tr><td>5</td><td>200</td><td>160</td><td>556.3</td><td>1343.6</td><td>4</td><td>9</td></tr><tr><td>6</td><td>200</td><td>200</td><td>559.7</td><td>1350.7</td><td>4</td><td>8</td></tr><tr><td>7</td><td>300</td><td>120</td><td>837.9</td><td>2012.1</td><td>8</td><td>18</td></tr><tr><td>8</td><td>300</td><td>160</td><td>834.5</td><td>2015.5</td><td>6</td><td>14</td></tr><tr><td>9</td><td>300</td><td>200</td><td>839.5</td><td>2026</td><td>5</td><td>11</td></tr><tr><td>10</td><td>400</td><td>120</td><td>1117.1</td><td>2680.8</td><td>10</td><td>23</td></tr><tr><td>11</td><td>400</td><td>160</td><td>1111.5</td><td>2685.9</td><td>8</td><td>18</td></tr><tr><td>12</td><td>400</td><td>200</td><td>1120.3</td><td>2702.9</td><td>6</td><td>15</td></tr><tr><td>13</td><td>500</td><td>120</td><td>1390.8</td><td>3353.5</td><td>12</td><td>29</td></tr><tr><td>14</td><td>500</td><td>160</td><td>1390.8</td><td>3359.1</td><td>10</td><td>22</td></tr><tr><td>15</td><td>500</td><td>200</td><td>1399.1</td><td>3376.7</td><td>8</td><td>18</td></tr></table>

## D. Performance Evaluation of the Overall Algorithms

Synthesizing the above analysis, an example is used to corroborate the overall algorithmsâ utility in solving energy-efficient GN-accessing tasks, with subsequent analysis of UAV energy consumption and UAV altitude therein. First, the process of such a task is outlined in Fig. 9. To be specific, this GN-accessing task involves 15 GNs, the 3-D coordinates of the depot and $E _ { \mathrm { m a x } }$ are set to (550,475,250) and 90 kJ, respectively. It is calculated that at least two UAVs, namely UAV 1 and UAV 2, are required to fulfill this task, where UAV 1 covers the GNs numbered 1 to 7 along the red curve, and UAV 2 covers the GNs numbered 8 to

<!-- image-->  
Fig. 9. 3-D trajectories of UAVs.

15 along the blue curve. The details of the two UAVsâ flying paths are given in Table IV.

Then, the energy consumption and the flight altitude of UAVs 1 and 2 on their respective trajectories (i.e., the red and blue curves in Fig. 9) are presented.

Energy-efficient multi-UAV GN-accessing manifests in the reasonable utilization of UAV energy. As can be seen in Figs. 10 and 11, despite their distinct tasks, both UAV 1 and UAV 2 adopt a moderate onboard storage utilization approach, which is characterized by controlling UAV energy consumption to maintain small fluctuations, as evidenced during their respective trajectories from segment 0 to 1400 and segment 200 to 1800. This approach not only mitigates hardware wear in UAVs caused by frequent energy consumption variations, but also reduces extra energy consumption by decreasing the number of vertical flight status alterations, thereby enhancing GN access efficiency.

The flight altitude has an impact on the UAV energy consumption. Figs. 10 and 11 reveal a trend where larger altitude variations in UAV flights are associated with higher energy consumption. This is understandable since UAV vertical energy consumption is a major component of total UAV flight energy consumption, significant altitude changes leading to increased vertical energy consumption are directly reflected in increased total energy consumption [20]. Interestingly, in some special cases, the change in UAV flight altitude can cause transient changes in UAV energy consumption, e.g., the rapid decrease in energy consumption of UAV 2 at segment 200. This is mainly because the change in UAV flight status at this time brings a large energy consumption difference. However, these energy consumption transients are negligible in the long-term steady flight of UAVs.

TABLE IV FLYING PATHS OF THE TWO UAVS
<table><tr><td rowspan=1 colspan=1>UAV No.</td><td rowspan=1 colspan=1>Numberof GNs</td><td rowspan=2 colspan=1>Flyingpath(550,475,250)-&gt;(260,450,300)-&gt;(700,465,315)-&gt;(400,900,300)-&gt;(800,500,410)-&gt;(200,700,500)-&gt;(635,525,500)-&gt;(600,250,500)-&gt;(550,475,250)</td></tr><tr><td rowspan=1 colspan=1>1 (red)</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=1>2 (blue)</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>(550,475,250)-&gt;(650,650,50)-&gt;(750,400,100)-&gt;(500,400,110)-&gt;(900,300,130)-(625,375,175)-&gt;(450,750,200)-&gt;(415,415,215)-&gt;(350,280,200)-&gt;(550,475,250)</td></tr></table>

<!-- image-->  
Fig. 10. UAV 1âs instantaneous altitude and energy consumption versus line segments.

<!-- image-->  
Fig. 11. UAV 2âs instantaneous altitude and energy consumption versus line segments.

## VII. CONCLUSION

This paper proposed a generic multi-UAV application scenario, namely the GN-accessing scenario, and formulated a problem to minimize the energy consumption for GN-accessing tasks while employing the minimum number of UAVs. To solve this problem, this paper decomposed it into two subproblems. The first subproblem is to minimize the energy required for UAVs to access any two GNs consecutively, which was solved by applying the SCA technique and path discretization method. The second subproblem is to plan optimal energy-efficient GNaccessing paths employing the minimum number of UAVs, which was solved by designing a three-stage approximation framework based on MPSO and GPA. The simulation results showed that the UAV flying with the optimized trajectory can effectively reduce energy consumption by up to about 16% compared to the linear trajectory; in addition, the proposed MPSO-GPA algorithm has more than 45% improvement in minimizing the number of UAVs compared to benchmarks. In the future, improving the MPSO algorithm and updating the energy consumption model for UAV acceleration/deceleration will be further considered.

## REFERENCES

[1] A. Albanese, V. Sciancalepore, and X. Costa-PÃ©rez, âSARDO: An automated search-and-rescue drone-based solution for victims localization,â IEEE Trans. Mobile Comput., vol. 21, no. 9, pp. 3312â3325, Sep. 2022.

[2] L. Wu et al., âUAV-assisted maritime legitimate surveillance: Joint trajectory design and power allocation,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13701â13705, Oct. 2023.

[3] C. Zhan and Y. Zeng, âCompletion time minimization for multi-UAVenabled data collection,â IEEE Trans. Wireless Commun., vol. 18, no. 10, pp. 4859â4872, Oct. 2019.

[4] Y. Zhang, Z. Mou, F. Gao, L. Xing, J. Jiang, and Z. Han, âHierarchical deep reinforcement learning for backscattering data collection with multiple UAVs,â IEEE Internet Things J., vol. 8, no. 5, pp. 3786â3800, Mar. 2021.

[5] Y.-H. Hsu and R.-H. Gau, âReinforcement learning-based collision avoidance and optimal trajectory planning in UAV communication networks,â IEEE Trans. Mobile Comput., vol. 21, no. 1, pp. 306â320, Jan. 2022.

[6] Y. Zhang, Z. Mou, F. Gao, J. Jiang, R. Ding, and Z. Han, âUAV-enabled secure communications by multi-agent deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 11599â11611, Oct. 2020.

[7] W. Wang et al., âRobust 3D-trajectory and time switching optimization for dual-UAV-enabled secure communications,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3334â3347, Nov. 2021.

[8] Y. Wang, Z.-Y. Ru, K. Wang, and P.-Q. Huang, âJoint deployment and task scheduling optimization for large-scale mobile users in multi-UAVenabled mobile edge computing,â IEEE Trans. Cybern., vol. 50, no. 9, pp. 3984â3997, Sep. 2020.

[9] S. Hayat, E. Yanmaz, T. X. Brown, and C. Bettstetter, âMulti-objective UAV path planning for search and rescue,â in Proc. IEEE Int. Conf. Robot. Automat., 2017, pp. 5569â5574.

[10] J. Wu, C. Luo, Y. Luo, and K. Li, âDistributed UAV swarm formation and collision avoidance strategies over fixed and switching topologies,â IEEE Trans. Cybern., vol. 52, no. 10, pp. 10969â10979, Oct. 2022.

[11] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[12] Z. Yang, W. Xu, and M. Shikh-Bahaei, âEnergy efficient UAV communication with energy harvesting,â IEEE Trans. Veh. Technol., vol. 69, no. 2, pp. 1913â1927, Feb. 2020.

[13] C. Zhan and H. Lai, âEnergy minimization in internet-of-things system based on rotary-wing UAV,â IEEE Wireless Commun. Lett., vol. 8, no. 5, pp. 1341â1344, Oct. 2019.

[14] B. Li, Q. Li, Y. Zeng, Y. Rong, and R. Zhang, â3D trajectory optimization for energy-efficient UAV communication: A control design perspective,â IEEE Trans. Wireless Commun., vol. 21, no. 6, pp. 4579â4593, Jun. 2022.

[15] C. You and R. Zhang, â3D trajectory optimization in rician fading for UAV-enabled data harvesting,â IEEE Trans. Wireless Commun., vol. 18, no. 6, pp. 3192â3207, Jun. 2019.

[16] Z. Sun, G. G. Yen, J. Wu, H. Ren, H. An, and J. Yang, âMission planning for energy-efficient passive UAV radar imaging system based on substage division collaborative search,â IEEE Trans. Cybern., vol. 53, no. 1, pp. 275â288, Jan. 2023.

[17] J. Xie and J. Chen, âMultiregional coverage path planning for multiple energy constrained UAVs,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 10, pp. 17366â17381, Oct. 2022.

[18] J. Li, Y. Xiong, J. She, and M. Wu, âA path planning method for sweep coverage with multiple UAVs,â IEEE Internet Things J., vol. 7, no. 9, pp. 8967â8978, Sep. 2020.

[19] J. Fu, G. Sun, J. Liu, W. Yao, and L. Wu, âOn hierarchical multi-UAV dubins traveling salesman problem paths in a complex obstacle environment,â IEEE Trans. Cybern., vol. 54, no. 1, pp. 123â135, Jan. 2024.

[20] H. Gong, B. Huang, B. Jia, and H. Dai, âModeling power consumptions for multirotor UAVs,â IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 6, pp. 7409â7422, Dec. 2023.

[21] M. B. Ghorbel, D. Rodr Ã­guez-Duarte, H. Ghazzai, M. J. Hossain, and H. Menouar, âJoint position and travel path optimization for energy efficient wireless data gathering using unmanned aerial vehicles,â IEEE Trans. Veh. Technol., vol. 68, no. 3, pp. 2165â2175, Mar. 2019.

[22] S. Fu et al., âEnergy-efficient UAV-enabled data collection via wireless charging: A reinforcement learning approach,â IEEE Internet Things J., vol. 8, no. 12, pp. 10209â10219, Jun. 2021.

[23] X. Xiong, C. Sun, W. Ni, and X. Wang, âThree-dimensional trajectory design for unmanned aerial vehicle-based secure and energy-efficient data collection,â IEEE Trans. Veh. Technol., vol. 72, no. 1, pp. 664â678, Jan. 2023.

[24] C. H. Liu, C. Piao, and J. Tang, âEnergy-efficient UAV crowdsensing with multiple charging stations by deep learning,â in Proc. IEEE Conf. Comput. Commun., 2020, pp. 199â208.

[25] F. H. Panahi and F. H. Panahi, âReliable and energy-efficient UAV communications: A cost-aware perspective,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 4038â4049, May 2024.

[26] Y. Liu, W. Huangfu, H. Zhou, H. Zhang, J. Liu, and K. Long, âFair and energy-efficient coverage optimization for UAV placement problem in the cellular network,â IEEE Trans. Commun., vol. 70, no. 6, pp. 4222â4235, Jun. 2022.

[27] P. Yang, X. Cao, X. Xi, W. Du, Z. Xiao, and D. Wu, âThree-dimensional continuous movement control of drone cells for energy-efficient communication coverage,â IEEE Trans. Veh. Technol., vol. 68, no. 7, pp. 6535â6546, Jul. 2019.

[28] D. Yang, Q. Wu, Y. Zeng, and R. Zhang, âEnergy tradeoff in ground-to-UAV communication via trajectory design,â IEEE Trans. Veh. Technol., vol. 67, no. 7, pp. 6721â6726, Jul. 2018.

[29] M. Hua, Y. Huang, Y. Wang, Q. Wu, H. Dai, and L. Yang, âEnergy optimization for cellular-connected multi-UAV mobile edge computing systems with multi-access schemes,â J. Commun. Inf. Netw., vol. 3, no. 4, pp. 33â44, 2018.

[30] X. Zhang, J. Zhang, J. Xiong, L. Zhou, and J. Wei, âEnergy-efficient multi-UAV-enabled multiaccess edge computing incorporating NOMA,â IEEE Internet Things J., vol. 7, no. 6, pp. 5613â5627, Jun. 2020.

[31] W. Liu, B. Li, W. Xie, Y. Dai, and Z. Fei, âEnergy efficient computation offloading in aerial edge networks with multi-agent cooperation,â IEEE Trans. Wireless Commun., vol. 22, no. 9, pp. 5725â5739, Sep. 2023.

[32] Y. Zhang and Q. Li, âExploiting ZigBee in reducing WiFi power consumption for mobile devices,â IEEE Trans. Mobile Comput., vol. 13, no. 12, pp. 2806â2819, Dec. 2014.

[33] S. P. Boyd and L. Vandenberghe, Convex Optimization. Cambridge, U.K.: Cambridge Univ. Press, 2004.

[34] A. Konar and N. D. Sidiropoulos, âFast approximation algorithms for a class of non-convex QCQP problems using first-order methods,â IEEE Trans. Signal Process., vol. 65, no. 13, pp. 3494â3509, Jul. 2017.

[35] A. M. Sasson, F. Viloria, and F. Aboytes, âOptimal load flow solution using the hessian matrix,â IEEE Trans. Power App. Syst., vol. PAS-92, no. 1, pp. 31â41, Jan. 1973.

[36] A. Filippone, Flight Performance of Fixed and Rotary Wing Aircraft. Amsterdam, Netherlands: Elsevier, 2006.

[37] C. Hao, Y. Chen, Z. Mai, G. Chen, and M. Yang, âJoint optimization on trajectory, transmission and time for effective data acquisition in UAVenabled IoT,â IEEE Trans. Veh. Technol., vol. 71, no. 7, pp. 7371â7384, Jul. 2022.

[38] C. Zhan and Y. Zeng, âEnergy-efficient data uploading for cellularconnected UAV systems,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7279â7292, Nov. 2020.

[39] Q. Zhang, W. Xu, W. Liang, J. Peng, T. Liu, and T. Wang, âAn improved algorithm for dispatching the minimum number of electric charging vehicles for wireless sensor networks,â Wireless Netw., vol. 25, pp. 1371â1384, 2019.

[40] W. Zhang and W. Zhang, âAn efficient UAV localization technique based on particle swarm optimization,â IEEE Trans. Veh. Technol., vol. 71, no. 9, pp. 9544â9557, Sep. 2022.

[41] G. Rudolph, âConvergence analysis of canonical genetic algorithms,â IEEE Trans. Neural Netw., vol. 5, no. 1, pp. 96â101, Jan. 1994.

[42] J. W. Siegel and J. Xu, âOptimal convergence rates for the orthogonal greedy algorithm,â IEEE Trans. Inf. Theory, vol. 68, no. 5, pp. 3354â3361, May 2022.

[43] F. Shan, J. Huang, R. Xiong, F. Dong, J. Luo, and S. Wang, âEnergyefficient general PoI-visiting by UAV with a practical flight energy model,â IEEE Trans. Mobile Comput., vol. 22, no. 11, pp. 6427â6444, Nov. 2023.

[44] C. Luo, M. N. Satpute, D. Li, Y. Wang, W. Chen, and W. Wu, âFine-grained trajectory optimization of multiple UAVs for efficient data gathering from WSNs,â IEEE/ACM Trans. Netw., vol. 29, no. 1, pp. 162â175, Feb. 2021.

[45] R. Shivgan and Z. Dong, âEnergy-efficient drone coverage path planning using genetic algorithm,â in Proc. IEEE 21st Int. Conf. High Perform. Switching Routing, 2020, pp. 1â6.

[46] J. Chen, H. Zhao, and L. Wang, âThree dimensional path planning of UAV based on adaptive particle swarm optimization algorithm,â J. Phys. Conf. Ser., vol. 1846, no. 1, Mar. 2021, Art. no. 012007, doi: 10.1088/1742-6596/1846/1/012007.

[47] J. Li, Y. Xiong, and J. She, âUAV path planning for target coverage task in dynamic environment,â IEEE Internet Things J., vol. 10, no. 20, pp. 17734â17745, Oct. 2023.

[48] J. Zheng, M. Ding, L. Sun, and H. Liu, âDistributed stochastic algorithm based on enhanced genetic algorithm for path planning of multi-UAV cooperative area search,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 8, pp. 8290â8303, Aug. 2023.

<!-- image-->  
Hao Gong received the BE degree in computer science from the Beijing University of Chemical Technology, Beijing, China, in 2019. He is currently working toward the PhD degree in computer science with Inner Mongolia University, Hohhot, China. His research interests include UAV energy modeling and UAV path planning.

<!-- image-->

Baoqi Huang (Member, IEEE) received the BE degree in computer science from Inner Mongolia University (IMU), Hohhot, China, the MS degree in computer science from Peking University, Beijing, China, and the PhD degree in information engineering from Australian National University, Canberra, ACT, Australia, in 2002, 2005, and 2012, respectively. He is with the College of Computer Science, IMU, where he is currently a professor. His research interests include indoor localization and navigation, wireless sensor networks, and mobile computing. He was a recipient

of the Chinese Government Award for Outstanding Chinese Students Abroad, in 2011.

<!-- image-->

Bing Jia (Member, IEEE) received the PhD degree from Jilin Univesity, Changchun, China, in 2013. She is with the College of Computer Science, Inner Mongolia University, Hohhot, China, where she is currently an associate professor. Her current research interests include indoor localization, crowdsourcing, wireless sensor networks and mobile computing.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs/page_2_img_1.png|page_2_img_1]]
2. [[../extracted_images/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs/page_13_img_1.png|page_13_img_1]]
3. [[../extracted_images/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs/page_15_img_1.jpeg|page_15_img_1]]
4. [[../extracted_images/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs/page_15_img_2.jpeg|page_15_img_2]]
5. [[../extracted_images/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs/page_15_img_3.jpeg|page_15_img_3]]

---

