# Federated Meta-Learning Based Computation Offloading Approach With Energy-Delay Tradeoffs in UAV-Assisted VEC

Chunlin Li , Chaoyue Deng, Yong Zhang, and Shaohua Wan , Senior Member, IEEE

AbstractâFederated learning (FL) provides an applicable solution for computation offloading in Unmanned Aerial Vehicle(UAV)- assisted Vehicular Edge Computing (VEC) by preserving privacy. However, the heterogeneity of clients brings challenges to the generalization of models. Therefore, we propose a federated metalearning (FML) framework to solve computation offloading for UAV-assisted VEC. In this paper, we are concerned with computation offloading of temporary hotspot regions due to traffic congestion. First, we construct a computation offloading problem with energy-delay tradeoffs and convert the problem to a Markov Decision Process (MDP). Then, we use FML to train personalized models for different vehicles while enhancing the generalization, we propose a Graph neural network-based FL Probabilistic Embedding for Actor-critic RL (GFL-PEARL) algorithm. We model the context as a Directed Acyclic Graph (DAG) and use GNN to reconstruct the inference network of the PEARL algorithm to extract the correlation between contexts fully. We dynamically adjust the task priority during the FML training process to improve the sampling efficiency. Finally, we verify the performance of the algorithm through simulation and physical experiments. Experimental results show that our algorithm can reduce average cost and task overtime rate by 31% and 56% respectively compared with the benchmarks.

Index TermsâComputation offloading, UAV-assisted VEC, energy-latency tradeoffs, GFL-PEARL, FML.

## I. INTRODUCTION

## A. Background and Motivations

T HE rapid development of intelligent connected vehicles T has brought about intelligent vehicle applications such as

Received 7 April 2024; revised 15 May 2025; accepted 21 May 2025. Date of publication 23 May 2025; date of current version 3 September 2025. This work was supported in part by the National Natural Science Foundation of China (NSFC) under Grant 62372344, Grant 62171330, and Grant 62172438, in part by the National Key R&D Program of China under Grant 2023YFB3308701, in part by the Key Research and Development Plan of Hubei Province under Grant 2023BAB075, in part by the International Science and Technology Cooperation Project of Hubei Province under Grant 2024EHA042, in part by Wuhan Key RD Program Projects under Grant 2024050702030091, in part by Shenzhen Science and Technology Program under Grant JCYJ20220818103200002, and in part by the Natural Science Foundation of Guangdong Province of China under Grant 2024A1515011155. Recommended for acceptance by M. Segata. (Corresponding author: Chunlin Li.)

Chunlin Li, Chaoyue Deng, and Yong Zhang are with the School of Computer and Artificial Intelligence, Wuhan University of Technology, Wuhan 430063, China (e-mail: chunlinli2020@163.com).

Shaohua Wan is with the Shenzhen Institute for Advanced Study, University of Electronic Science and Technology of China, Shenzhen 518110, China (e-mail: shaohua.wan@uestc.edu.cn).

Digital Object Identifier 10.1109/TMC.2025.3573278 autonomous driving, path planning, and road condition prediction. These applications rely on technologies such as highprecision positioning and radar sensing and have extremely strict requirements on computing resources and latency. In addition, real-time analysis of driver behavior can provide early warning services for drivers, which also has extremely stringent requirements on low latency. However, the computing power of terminal vehicles is limited, and it is difficult to meet the demands of these computationally intensive and latency-sensitive tasks. For this reason, vehicle edge computing (VEC) has become an ideal solution for computation offloading in the Internet of Vehicles (IoV). VEC shortens response time and improves quality of service by deploying edge servers on roadside units (RSUs) close to the road.

When RSU and nearby vehicles are overloaded or inaccessible, such as temporary congestion and RSU failure, the offloading task cannot be received and completed within the delay requirement, which reduces the quality of experience for drivers [1]. Compared with fixed RSUs, unmanned aerial vehicle (UAV), with the high mobility, flexible deployment and strong adaptability, has been employed as an optional candidate to receive offloading tasks from vehicles and provide flexible offloading services in VEC. It provided an economical and efficient computation paradigm known as UAV-assisted VEC. Recent studies [2], [3] in the academic community have explored the potential of UAVs in VEC, even considering these limitations. With the developments of UAV battery and computing power, UAVs have substantial potential as a offloading platform and should be further explored.

Computation offloading has become a key means to solve the performance bottlenecks of resource-constrained devices. Unlike traditional distributed training methods, federated learning (FL)-based offloading approaches reduce communication overhead and achieve better data privacy protection [27]. However, in UAV-assisted VEC, the global model is difficult to consider the personalized needs of different vehicles, and exhibits poor generalization ability in the scenarios with large differences in data distribution and diverse tasks [28]. Diffirent from FL, federated meta-learning (FML) improves the efficiency of computation offloading by rapidly adapting to new tasks, implementing personalized optimization strategies, and facilitating cross-device collaborative computing [30]. However, there are still some challenges to be addressed.

- How to perform efficient computation offloading under limited communication bandwidth and computing resources in UAV-assisted VEC?

How to improve the generalization and robustness of the model while addressing potential security and privacy concerns of the training phase in complex and dynamic UAV-assisted VEC?

With the challenges mentioned above, this work focuses on solving the computation offloading problem in UAV-assisted VEC using an FML framework. In this framework, although some studies [16], [18] have considered the trade-off between energy consumption and latency in offloading, to the best of our knowledge, no study has exhaustively considered the total energy consumption of the system. Although location and trajectory optimizations of UAV have been discussed in previous studies [16], [17], [18], [19], [20], there is no work to consider the RSSI optimization in UAV deployment. In current works on computation offloading optimization, most existing studies rely on simple linear or independent assumptions when dealing with constraints between tasks, and do not fully consider complex dependencies between tasks, resulting in poor adaptability of the model in dynamic environments. In addition, task sampling strategy of traditional methods is usually statically allocated, and the sampling priority cannot be flexibly adjusted, which limits the speed of model convergence.

## B. Contributions

The main contributions and innovations are as follows:

1) FML-based Computation Offloading Framework for UAVassisted VEC: In this framework, local model on vehicleside only needs to upload the intermediate parameters or gradients without sharing the vehicle data, which protects user privacy during the training phase. We consider offloading tasks to nearby vehicles, UAVs and edge nodes to fully utilize computing resources and improve task execution efficiency. Then, we built a UAV deployment problem with goal of maximizing Received Signal Strength Indication (RSSI), which effectively improve the communication quality between UAVs and vehicles. We consider the transmission and execution energy consumption, the hovering and flight energy consumption of UAVs, and establish an optimization problem with energy consumption-latency tradeoffs. Experimental results show that when number of vehicles is 50, GFL-PEARL reduces task timeout rate by up to 31.72% than baselines.

2) GFL-PEARL Algorithm for Computation Offloading Optimization: In the GFL-PEARL algorithm, the context that refers to task constraints is modeled as Directed Acyclic Graph (DAG) and we reconstruct the reasoning network using Graph Neural Network (GNN) to fully extract the correlation between contexts, so the model can quickly adapt to different tasks, thereby improving robustness. Meanwhile, through information sharing and variational inference between tasks, it can better capture the uncertainty in task distribution, reduce overfitting, and thus improve the generalization of the model. In addition, we dynamically adjust the task sampling priority to accelerate the convergence speed. Experimental results show that compared with baselines, GFL-PEARL algorithm only needs 300 iterations before the reward tends to a stable value, which significantly improves computation offloading efficiency in dynamic traffic scenario.

TABLE I  
COMPARISON OF OUR APPROACH WITH RELATED WORKS
<table><tr><td>Reference</td><td></td><td></td><td></td><td>[4],[5], [6],[7][8],[9],[10],[11][12],[13],[14],[15][16],[17],[18],[19],[20]Our work</td><td></td></tr><tr><td>Edge-only offloading</td><td>â</td><td></td><td></td><td></td><td></td></tr><tr><td>Nearby vehicles-only offloading</td><td></td><td>â</td><td></td><td></td><td></td></tr><tr><td>Collaborative offloading</td><td></td><td></td><td>â</td><td>â</td><td></td></tr><tr><td>UAV-assisted offloading</td><td></td><td></td><td></td><td>â</td><td></td></tr><tr><td>RSSI optimization</td><td></td><td></td><td></td><td></td><td>&gt;&gt;&gt;</td></tr><tr><td>UAV energy consumption</td><td></td><td></td><td></td><td>â</td><td>â</td></tr><tr><td>System energy consumption</td><td></td><td></td><td></td><td></td><td>â</td></tr><tr><td>Energy-latency tradeoffs</td><td></td><td></td><td></td><td>â</td><td>â</td></tr><tr><td rowspan="2">Offloading mode</td><td>full</td><td>full</td><td>partial</td><td>partial</td><td>full</td></tr><tr><td>offloading</td><td>offloading</td><td>offloading</td><td>full offloading</td><td>offloading</td></tr></table>

The rest of paper are organized as follows. Section II introduces related works. Section III presents the system model and framework. Section IV presents the algorithms. Section V provides experimental results. Section VI concludes the paper.

## II. RELATED WORK

In VEC, when RSU computing resources are scarce, optimizing server deployment and utilizing idle devices are efficient solutions to alleviate server computing overload [19]. However, above two solutions cannot avoid RSU overload or unaccessed. When the vehicle needs to handle complex and computationally intensive tasks such as driver behavior detection, due to the limited computing resources of the vehicle, it cannot perform all tasks independently, so some tasks need to be offloaded to RSU or nearby vehicles for execution. In this section, we review the related works including computation offloading in VEC, and solutions for computation offloading.

## A. Computation Offloading Strategy

Computation offloading addresses computation overload by transferring vehicle-side tasks from resource-constrained devices to edge nodes or cloud, reducing local burden and improving efficiency. The comparison of proposed computation offloading scheme with related works is shown in Table I.

1) Edge-Only Offloading: To improve the efficiency of computation offloading, Abadi et al. [4] proposed a Deep Reinforcement Learning (DRL) algorithm to optimize computing and network resources in edge layer. Liang et al. [5] proposed a double deep Q-network for single-task source nodes and multitask destinations, which. Yan et al. [6] utilized Q-Learning and DRL for multi-task source nodes and single-task destinations, optimizing offloading and resource allocation to improve task execution efficiency. Shi et al. [7] presented deep deterministic policy gradient algorithms for edge offloading in multi-user scenarios.

2) Nearby Vehicles-Only Offloading: Chen et al. [8] introduced a computation offloading scheme in vehicle-mounted networks that enhances efficiency by offloading tasks to nearby vehicles, thereby reducing both load and latency. Chen et al. [9] proposed a decentralized computation offloading mechanism that facilitates efficient coordination of offloading among mobile users. Huang et al. [10] developed a deep reinforcement learning framework aimed at optimizing offloading and resource allocation, demonstrating adaptability in dynamic environments. Zhang et al. [11] presented a dynamic offloading scheme that integrates vehicle-to-vehicle collaboration with energy collection to minimize energy consumption and improve computational efficiency.

3) Collaborative Offloading: Peng et al. [12] reformulated computation offloading and resource allocation as reinforcement learning problems, solved using distributed deep learning algorithms. Bi et al. [13] utilized RSUs and vehicle resources for task offloading in the Internet of Vehicles, enabling vehicles to also participate in data relay and computation. Zhang et al. [14] introduced a DRL algorithm that combines mobile edge computing nodes, base stations, vehicles, and RSUs to minimize energy consumption and transmission delays. Lastly, Wang et al. [15] proposed a vehicle-coordinated offloading strategy, allowing vehicles to migrate unfinished tasks to others before leaving traffic infrastructure coverage.

4) UAV-Assisted Offloading: In temporary hotspot scenarios, UAV-assisted vehicle networks have been explored for computation offloading. Zhao et al. [16] examined a UAV-assisted vehicle edge computing network to minimize mobile device energy consumption while meeting latency requirements. Feng et al. [17] combined UAV-assisted vehicle networks with machine learning to enhance communication efficiency and adaptability. Hu et al. [18] proposed a strategy where UAVs facilitate data transmission and provide wireless charging, improving offloading capability and energy efficiency. Ning et al. [19] optimized UAV flight trajectories to enhance energy collection and reduce latency, stabilizing computation offloading. Finally, Zhang et al. [20] aimed to maximize system throughput by dynamically adjusting UAV flight paths and resource allocation, thereby improving overall performance.

In summary, above offloading schemes provide an effective solution for improving the execution efficiency of vehicle tasks. However, [4], [5], [6], [7], [8], [9], [10], [11] are more suitable for relatively static scenes, and do not work well in dynamic traffic environments. [12], [13], [14], [15] ignore the special cases of RSU unaccessed or vehicle overload, which are not suitable for the proposed scenario. [16], [17], [18], [19], [20] introduce UAVs into special scenarios for computation offloading, but they rarely consider RSSI optimization in UAV deployment, leading to cannot guarantee the link quality between UAV and vehicles. Finally, [16], [17], [18], [19], [20] only consider the UAV energy consumption instead of whole energy consumption, resulting in a decrease in overall system energy efficiency. Different from the above mentioned studies, we built a UAV deployment problem with goal of maximizing RSSI, aiming to improve the communication quality between UAVs and vehicles. We formulate the computation offloading problem as total energy consumption and latency trade-off problem, with the goal of minimizing the service delay and maximizing the system energy efficiency.

TABLE II  
COMPARISON OF OUR APPROACH WITH RELATED WORKS
<table><tr><td>Reference</td><td>[21], [22], [23]</td><td>[24], [25], [26]</td><td>[27],[28],[29]</td><td>[30],[31]</td></tr><tr><td>MathematicalProgramming</td><td>â</td><td></td><td></td><td></td></tr><tr><td>Deep Learning</td><td></td><td>â</td><td></td><td></td></tr><tr><td>Reinforcement Learning</td><td></td><td>â</td><td></td><td></td></tr><tr><td>Meta-Reinforcement Learning</td><td></td><td></td><td>â</td><td>1</td></tr><tr><td>Federated Learning</td><td></td><td></td><td>â</td><td></td></tr><tr><td>Method</td><td>IPSGA</td><td>DRL,DDPG, Estimation, Ant colony Q-learning, DCOM</td><td>FL</td><td>Pearl</td></tr></table>

## B. Solution for Computation Offloading

Previous studies have investigated different solutions for computation offloading in MEC environments, There are basically included mathematical optimization, deep learning, federated learning, and meta-reinforcement learning. The comparison of the proposed computation offloading algorithm with related works is shown in Table II.

1) Mathematical Programming: Li et al. [21] proposed an improved particle swarm genetic algorithm (IPSGA) to solve the offloading decision. Shan et al. [22] proposed a load balance-based computing offloading framework to obtain offloading strategies through covariance-based hierarchical analysis method and potential game. Chuang et al. [23] proposed a real-time, two-stage ant colony algorithm.

2) Deep Learning and Reinforcement Learning: To improve generalization, deep learning-based offloading algorithms have emerged. Geng et al. [24] proposed a multi-intelligent DRL computing offloading framework with improved actor and criterion networks for feature extraction. Li et al. [25] proposed a distributed-based DRL method and solved the offloading decision by an improved D3QN. Zhao et al. [26] proposed an optimization framework based on multi-agent DRL to minimize latency and energy consumption in UAV-assisted mobile edge computing.

3) Federated Learning: In the dynamic Internet of Vehicles, extensive state representation can hinder training speeds. Federated learning approaches have been explored. Hou et al. [27] introduced a dual-time scale DRL model for varied delay tasks, optimizing offloading and resource usage. Tang et al. [28] proposed a model-free distributed DRL algorithm for independent offloading strategies, reducing delays and abandonment rates. Li et al. [29] proposed an improved federated deep deterministic policy gradient (DDPG) algorithm to solve the computing offloading problem by improving the exploration noise and the experience pool.

4) Meta-Reinforcement Learning: The PEARL algorithm [30], a context-based meta-reinforcement learning method, has gained traction. The FedMetaR2Ag algorithm [31] is a meta-reinforcement learning algorithm that obtains satisfactory results with a small number of samples and iterations.

In summary, above works efficiently solves the optimization problem of offloading with the mathematical optimization, deep learning, and reinforcement learning schemes. However, [20], [21], [22] are usually based on static parameters, which is not flexible in dynamic UAV assisted scenarios. [23], [24], [25], [26], [27], [28] take a long time to converge to the optimal strategy, which affects the real-time requirements. [29], [30] rarely consider their intrinsic connections when processing context, thus limiting the generalization ability of the model across different tasks. In view of the above limitations, we propose an GFL-PEARL algorithm, which improves the generalization and robustness of the model, reduce average cost and task timeout rate.

<!-- image-->  
Fig. 1. UAV-assisted VEC FML framework.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

## A. System Overview

Fig. 1 shows the proposed FML framework in UAV-assisted VEC, which includes four roles: vehicles, RSU with edge server (ES), UAVs, and cloud server (CS). Each RSU is equipped with an ES, therefore, in the subsequent content, RSU refers to the RSU and the equipped ES. We describe the workflow of the framework: Step 1 inputs the coordinates of all the vehicles in a certain time slot. Step 2 obtains the optimal position of the UAV through the GA algorithm by iterating continuously. Step 3 inputs the optimal position into the computation offloading problem. The step 4-step 6 indicates the flow of computation offloading. Table III shows the definition of key symbols.

## B. Federated Meta-Learning Framework

In the proposed framework, the clients of FML consist of RSUs and vehicles. Before each training round, each vehicle downloads the parameters from the server. After a training period, each RSU performs local aggregation, and then upload the parameters and losses to the cloud server for global aggregation. The training goal for FML are as follows:

$$
\operatorname* { m i n } _ { \mathbf { \Theta } } L ( \boldsymbol { \zeta } ) = \frac { 1 } { | I | } \sum _ { i = 1 } ^ { | I | } l _ { i } ( \boldsymbol { \zeta } - \alpha \nabla l _ { i } ( \boldsymbol { \zeta } ) ) .\tag{1}
$$

where $| I |$ is the number of RSUs, $l _ { i }$ is the loss function for the parameter Î¶, Î± is the connection ratio.

Each RSU uploads its gradient and meta loss to the cloud server at the end of the training phase. The update is done as follows:

$$
\zeta ^ { t } = \zeta ^ { t - 1 } + \sum _ { i = 1 } ^ { | I | } \omega _ { i } \Delta \zeta _ { i } ^ { t } ,\tag{2}
$$

TABLE III SYMBOL DEFINITION

Symbol Definition k,m Request vehicle k, Service vehicle m $u , i$ UAVu,RSU i $C o _ { k } , C o _ { i } , C o _ { u }$ Device's coordination $d _ { u _ { i } } ^ { v 2 r } , d _ { u _ { i } } ^ { v 2 v } , d _ { u _ { i } } ^ { v 2 u }$ $d _ { k , i } ^ { \mathrm { v } \sim } , d _ { k , m } ^ { \mathrm { v } \sim \mathrm { v } } , d _ { k , u } ^ { \mathrm { v } \sim \mathrm { u } }$ Distance between devices $r _ { k , m } ^ { v 2 v } , r _ { k , i } ^ { v 2 r } , r _ { k , u } ^ { v 2 u }$ Transmission rate between devices $K , { \dot { U } } , I$ The set of vehicle,UAV,RSU   
$R _ { i } ^ { v } = \{ 1 , 2 , . . . , | R _ { i } ^ { v } | \}$ The set of vehicles within the coverage of RSU i   
$f _ { k , \operatorname* { m a x } } , f _ { u , \operatorname* { m a x } } , f _ { i , \operatorname* { m a x } }$ Max Computation resource $f _ { k _ { \bar { \lambda } } u } , f _ { k , i } , \underline { { f _ { k , m } } }$ Computation resource allocated to vehicle k $p _ { k } ^ { t r a n s } , p _ { k } ^ { e x e c }$ Transmission and executing power of vehicle k $\boldsymbol { Q } _ { k } , \stackrel { \vartriangle } { \boldsymbol { S } } _ { k } ^ { \vartriangle }$ Computation tasks and task size of vehicle k $u _ { k }$ Resource required for vehicle k unit sized tasks $v _ { k }$ The velocity of vehicle k $t _ { k , m a x }$ Maximum tolerance time of vehicle k $t _ { c o n }$ Communication time T Path loss exponent $T _ { \iota \circ } ^ { l o c a l } , E _ { \iota \circ } ^ { l o c a l }$ Local delay,energy consumption $T _ { k , u } ^ { t r a n s } , E _ { k , u } ^ { t r a n s }$ Transmission delay,energy consumption $E _ { u } ^ { h o v e r } , E _ { k , u } ^ { \bar { f } l y }$ Hover and fly energy consumption $\begin{array} { c } { { d _ { m a x } ^ { u } } } \\ { { R } } \end{array}$ Maximum distance of a single movement Radius of coverage of the UAV W Channel bandwidth $\underbrace { \kappa _ { L o S } , \kappa _ { N L o S } } _ { }$ Excessive path loss

$$
\omega _ { i } = { \frac { c _ { i } + \lambda \cdot d _ { i } } { \displaystyle { \sum _ { j = 1 } ^ { | I | } } c _ { j } + \lambda \cdot d _ { j } } } , c _ { i } = { \frac { | D _ { i } | } { \displaystyle { \sum _ { j = 1 } ^ { | I | } } | D _ { j } | } } , d _ { i } = { \frac { \displaystyle { \left( \sum _ { k = 1 } ^ { | K | } f _ { k } ^ { i } \right) ^ { \beta } } } { \displaystyle { \sum _ { j = 1 } ^ { | I | } } \left( \sum _ { k = 1 } ^ { | K | } f _ { k } ^ { j } \right) ^ { \beta } } } ,\tag{3}
$$

where $\zeta ^ { t }$ is the parameters at the t-th training round, $\omega _ { i }$ is the aggregation weights, $D _ { i }$ is the amount of data and $f _ { k } ^ { i }$ is the meta loss, Î» and $\beta$ are the aggregation parameters.

## C. UAV Deployment Model

We assume that the UAV is flying at a fixed altitude and that its state can be viewed as stationary at time slot t. Fixing the flight altitude of UAVs can simplify the deployment problem while avoiding unnecessary energy costs associated with the frequent ascent and descent of UAVs [2]. The coordinate of the UAV u is $\begin{array} { r } { C o _ { u } ( t ) = ( x _ { u } ( t ) , y _ { u } ( t ) , H ) } \end{array}$ , H is the fixed altitude at which UAVs can fly. At the next time slot, the coordinate of the UAV u is $C o _ { u } ( t + 1 ) = ( x _ { u } ( t + 1 ) , y _ { u } ( t + 1 ) , H )$ . Therefore, we can get the following reasonableness constraints:

$$
0 \leq | | C o _ { u } ( t + 1 ) - C o _ { u } ( t ) | | | \leq d _ { \operatorname* { m a x } } ^ { u } , t \in T ,\tag{4}
$$

where $d _ { \mathrm { m a x } } ^ { u }$ is the maximum distance traveled by the UAV in a maxsingle movement.

Because the UAV can fly within a specific rectangular area with x-axis range $[ 0 , x _ { \mathrm { m a x } } ]$ and y-axis range $[ 0 , y _ { \mathrm { m a x } } ]$ so that max maxthe coordinates of the UAVs satisfy the following constraints:

$$
0 \leq x _ { u } \leq x _ { \operatorname* { m a x } } , 0 \leq y _ { u } \leq y _ { \operatorname* { m a x } } .\tag{5}
$$

In order to ensure that the UAV can finally return for a successful periodic flight, we give the following constraints:

$$
C o ( T + 1 ) = C o ( 1 ) .\tag{6}
$$

Similar to [32], we ensure that the coverage of UAVs does not overlap in order to avoid UAV collisions and reduce interference between UAVs. Therefore the distance between UAVs needs to satisfy the following constraint:

$$
| | C o _ { u ^ { \prime } } ( t ) - C o _ { u } ( t ) | | \geq R , u ^ { \prime } \neq u ,\tag{7}
$$

where R is radius of coverage of UAV.

We adjust the position of UAVs based on the Received Signal Strength Indicator (RSSI) [33]:

$$
\begin{array} { r } { R S S I _ { u , k } = p _ { k } ^ { t r a n s } - 2 0 \log ( d _ { k , u } ^ { v 2 u } f _ { c } 4 \pi / c ) , } \end{array}\tag{8}
$$

where $p _ { k } ^ { t r a n s }$ is the transmission power of the vehicle k, $f _ { c }$ is the carrier frequency, $d _ { k , u }$ is the distance between vehicle k and UAV u,and c is the velocity of light.

Within the communication coverage area of the UAV u, each vehicle may establish a connection with UAV u. Therefore, the optimization objective is as follows:

$$
\mathbf { P 1 } : \mathrm { M a x } \quad \frac { 1 } { N _ { u } ^ { v } } \sum _ { k = 1 } ^ { N _ { u } ^ { v } } { R S S I _ { u , k } } ,\tag{9}
$$

$$
{ \mathrm { s . t . } } \quad ( 4 ) - ( 7 ) ,\tag{9a}
$$

where $N _ { u } ^ { v }$ is the number of vehicles in the Communication coverage area of the UAV u.

## D. Computing Offloading Model in UAV-Assisted VEC

In time slot t, vehicle k generate a driving behavior recognition task $Q _ { k } \overset { \Delta } { = } \{ v _ { k } , t _ { k , \operatorname* { m a x } } , S _ { k } , u _ { k } \}$ Vehicle k will only select a maxdevice for offloading that has the best quality of communication with it. We set the variable $x _ { k } ^ { v 2 x }$ to indicate whether vehicle chooses to offload the task to device x. Therefore, the variables must satisfy the following:

$$
x _ { k } ^ { l o c a l } + x _ { k } ^ { v 2 r } + x _ { k } ^ { v 2 u } + x _ { k } ^ { v 2 v } = 1 .\tag{10}
$$

It is assume that the coordinate of the vehicle k is $C o _ { k } =$ $( x _ { k } , y _ { k } , 0 )$ , and it travels at $v _ { k }$ speed along the $\theta _ { k }$ direction. The coordinate of the other device e is $\displaystyle C o _ { e } = ( x _ { e } , y _ { e } , h _ { e } )$ , the speed is $v _ { e }$ along the $\theta _ { e }$ direction. Therefore, the distance in the y-axis direction is $d _ { y } = y _ { k } - y _ { e }$ , and the velocity difference is $v _ { k , e , y } =$ $v _ { k }$ cos $\theta _ { k } - v _ { e }$ cos $\theta _ { e }$ . The x-axis distance is $d _ { x } = x _ { k } - x _ { e }$ , and the velocity difference is $v _ { k , e , x } = v _ { k }$ sin $\theta _ { k } - v _ { e }$ sin $\theta _ { e }$ . Therefore, the distance between vehicle k and device e must satisfy

the following constraint:

$$
( d _ { y } + v _ { k , e , y } t _ { c o n } ) ^ { 2 } + ( d _ { x } + v _ { k , e , x } t _ { c o n } ) ^ { 2 } + h _ { e } ^ { 2 } \le d _ { \operatorname* { m a x } } ^ { 2 } .\tag{11}
$$

Since the result after the execution of the task is smaller than the task itself, we ignore the return delay [14]. Our system employs a binary offloading model [34], [35], meaning tasks are either fully processed locally or offloaded to external entities, such as UAVs, RSUs, or other nearby vehicles. The system needs to select the optimal offloading decision, and we propose a federated meta-learning algorithm to optimize the offloading decisions. The detailed operations for different computation modes, based on the decisions derived from the federated meta-learning algorithm, are as follows.

1) Locally Executing: When a task is executed locally, the execution delay and execution energy consumption of vehicle k are calculated as follows:

$$
T _ { k } ^ { e x e c } = \frac { N _ { k } } { f _ { k } ^ { e x e c } } ,\tag{12}
$$

$$
E _ { k } ^ { e x e c } = p _ { k } ^ { e x e c } T _ { k } ^ { e x e c } ,\tag{13}
$$

where $N _ { \mathrm { k } } = u _ { k } \times S _ { \mathrm { k } } , \ f _ { k } ^ { e x e c }$ is the allocated computation rek ksource for executing task of vehicle k. Since vehicles need to participate in the training process of FML, the FML training delay and training energy consumption of vehicle k are as follows:

$$
T _ { k , t r a i n } ^ { F M L } = \frac { D _ { k } \times u _ { k } } { f _ { k } ^ { t r a i n } } ,\tag{14}
$$

$$
E _ { k , t r a i n } ^ { F M L } = p _ { k } ^ { e x e c } T _ { k , t r a i n } ^ { F M L } ,\tag{15}
$$

where $D _ { k }$ is the local dataset size of vehicle k and $f _ { k } ^ { t r a i n }$ is the allocated computation resources for training of vehicle k.

Therefore, the total delay and total energy consumption of vehicle k are calculated as follows:

$$
T _ { k } ^ { l o c a l } = T _ { k } ^ { e x e c } + T _ { k , t r a i n } ^ { F M L } ,\tag{16}
$$

$$
E _ { k } ^ { l o c a l } = E _ { k } ^ { e x e c } + E _ { k , t r a i n } ^ { F M L } .\tag{17}
$$

2) Offloading to UAVs: When offloading to UAV, the communication mode is divided into LoS and NLoS. The LoS link and NLoS link probability are calculated as follows:

$$
P r _ { k , u } ^ { L o S } = \left( 1 + \mu _ { a } \exp { \left( - \mu _ { b } \left( \arcsin { \left( \frac { H } { d _ { k , u } ^ { v 2 u } } \right) } - \mu _ { a } \right) \right) } \right) ^ { - 1 } ,\tag{18}
$$

$$
P r _ { k , u } ^ { N L o S } = 1 - P r _ { k , u } ^ { L o S } ,\tag{19}
$$

where $\mu _ { a }$ and $\mu _ { b }$ are environmental constants.

The path loss consists of free space path loss and excessive path loss, calculated as follows:

$$
L _ { k , u } ^ { L o S } = 2 0 \log ( d _ { k , u } ^ { v 2 u } f _ { c } 4 \pi / c ) + \kappa _ { L o S } ,\tag{20}
$$

$$
L _ { k , u } ^ { N L o S } = 2 0 \log ( d _ { k , u } ^ { v 2 u } f _ { c } 4 \pi / c ) + \kappa _ { N L o S } ,\tag{21}
$$

where $\kappa _ { L o S }$ and $\kappa _ { N L o S }$ correspond to the excessive path loss of the different communication modes, respectively.

Therefore, the average path loss [18] and signal-to-noise ratio (SNR) ratio are calculated as follows:

$$
\overline { { L _ { k , u } } } = P r _ { k , u } ^ { L o S } L _ { k , u } ^ { L o S } + P r _ { k , u } ^ { N L o S } L _ { k , u } ^ { N L o S } ,\tag{22}
$$

$$
\omega _ { k , u } = \frac { p _ { k } ^ { t r a n s } 1 0 ^ { - \overline { { L _ { k , u } } } / 1 0 } } { \sigma ^ { 2 } + \sum _ { j = 1 , j \neq k } ^ { V } p _ { j } ^ { t r a n s } 1 0 ^ { - \overline { { L _ { j , u } } } / 1 0 } } ,\tag{23}
$$

where $\sigma ^ { 2 }$ is the Gaussian noise power. The transmission rate between vehicle k and UAV u can be calculated as follows:

$$
r _ { k , u } ^ { v 2 u } = W _ { k , u } \mathrm { l o g } _ { 2 } ( 1 + \omega _ { k , u } ) ,\tag{24}
$$

where $W _ { k , u }$ is channel bandwidth between vehicle k and UAV u. During the vehicle transmission task to UAV, the transmission delay and energy consumption are as follows:

$$
T _ { k , u } ^ { t r a n s } = \frac { S _ { k } } { r _ { k , u } ^ { v 2 u } } ,\tag{25}
$$

$$
E _ { k , u } ^ { t r a n s } = p _ { k } ^ { t r a n s } T _ { k , u } ^ { t r a n s } .\tag{26}
$$

The execution delay and execution energy consumption of the UAV are calculated as follows:

$$
T _ { k , u } ^ { e x e c } = \frac { N _ { k } } { f _ { k , u } ^ { v 2 u } } ,\tag{27}
$$

$$
E _ { k , u } ^ { e x e c } = \omega ^ { u a v } ( f _ { k , u } ^ { v 2 u } ) ^ { 3 } T _ { k , u } ^ { e x e c } ,\tag{28}
$$

where $f _ { k , u } ^ { v 2 u }$ is the allocated computation resource by UAV u to vehicle $k . \omega ^ { u a v }$ is the energy coefficient of the UAV [2], which is related to the chip structure.

The UAV is assumed to hover for a finite amount of time during transmission and execution. Therefore, the hovering energy consumption is calculated as follows:

$$
E _ { u } ^ { h o v e r } = \psi _ { u } ( T _ { k , u } ^ { t r a n s } + T _ { k , u } ^ { e x e c } ) ,\tag{29}
$$

where $\psi _ { u }$ [17] is a constant energy value.

The flying energy consumption is calculated as follows:

$$
E _ { u } ^ { f l y } = \varpi ( | | C o _ { u } ( t + 1 ) - C o _ { u } ( t ) | | / \Delta t ) ^ { 2 } ,\tag{30}
$$

where  [18] is related to the weight of the UAV.

Therefore, the total delay and total energy consumption of UAV are calculated as follows:

$$
T _ { k , u } ^ { v 2 u } = T _ { k , u } ^ { t r a n s } + T _ { k , u } ^ { e x e c } ,\tag{31}
$$

$$
E _ { k , u } ^ { v 2 u } = E _ { k , u } ^ { t r a n s } + E _ { k , u } ^ { e x e c } + E _ { u } ^ { h o v e r } + E _ { u } ^ { f l y } .\tag{32}
$$

3) Offloading to RSUs: When offloading to RSU, the transmission rate between vehicle k and RSU i is as follows:

$$
r _ { k , i } ^ { v 2 r } = W _ { k , i } { \log _ { 2 } } \left[ 1 + \frac { { { \left( { d _ { k , i } ^ { v 2 r } } \right) } ^ { - \tau } } { p _ { k } ^ { t r a n s } } } { { { \sigma } ^ { 2 } } + \sum _ { j = 1 , j \ne k } ^ { V } { { { \left( { d _ { j , i } ^ { v 2 r } } \right) } ^ { - \tau } } { p _ { j } ^ { t r a n s } } } } \right] ,\tag{33}
$$

where Ï is the path loss exponent.

In the process of FML, the vehicle needs to upload the locally trained model to the RSUs. The FML parameter upload delay of vehicle kis calculated as follows:

$$
T _ { k , u p } ^ { F M L } = \frac { Q } { r _ { k , i } ^ { v 2 r } } ,\tag{34}
$$

where Q is the size of the upload model parameter.

The FML parameter upload delay depends on the maximum value of the upload delay, so the upload delay and upload energy consumption are calculated as follows:

$$
T _ { u p } ^ { F M L } = \operatorname* { m a x } \{ T _ { k , u p } ^ { F M L } \} , k \in K ,\tag{35}
$$

$$
E _ { u p } ^ { F M L } = p _ { k } ^ { t r a n s } T _ { u p } ^ { F M L } .\tag{36}
$$

Therefore, the total delay and energy consumption of RSU are calculated as follows:

$$
T _ { k , i } ^ { v 2 r } = T _ { k , i } ^ { t r a n s } + T _ { k , i } ^ { e x e c } + T _ { u p } ^ { F M L } ,\tag{37}
$$

$$
E _ { k , i } ^ { v 2 r } = E _ { k , i } ^ { t r a n s } + E _ { k , i } ^ { e x e c } + E _ { u p } ^ { F M L } ,\tag{38}
$$

the rest of the equation is calculated similarly to (12), (13), (25), and (26).

4) Offloading to Other Vehicles: When offloading to the other vehicle, the transmission rate is calculated as follows:

$$
r _ { k , m } ^ { v 2 v } = W _ { k , m } \mathrm { l o g } _ { 2 } \left[ 1 + \frac { \left( d _ { k , m } ^ { v 2 v } \right) ^ { - \tau } p _ { k } ^ { t r a n s } } { \sigma ^ { 2 } } \right] .\tag{39}
$$

Therefore, the total delay and total energy consumption of task processing vehicle m are calculated as follows:

$$
T _ { k , m } ^ { v 2 v } = T _ { k , m } ^ { t r a n s } + T _ { k , m } ^ { e x e c } ,\tag{40}
$$

$$
E _ { k , m } ^ { v 2 v } = E _ { k , m } ^ { t r a n s } + E _ { k , m } ^ { e x e c } ,\tag{41}
$$

the rest of the equation is calculated similarly to (12), (13), (25), and (26).

Therefore, the total delay and total energy consumption of the vehicle k executing task $Q _ { k }$ are calculated as follows:

$$
T _ { k } = x _ { k } ^ { l o c a l } T _ { k } ^ { l o c a l } + x _ { k } ^ { v 2 r } T _ { k , i } ^ { v 2 r } + x _ { k } ^ { v 2 u } T _ { k , u } ^ { v 2 u } + x _ { k } ^ { v 2 v } T _ { k , m } ^ { v 2 v } ,\tag{42}
$$

$$
E _ { k } = x _ { k } ^ { l o c a l } E _ { k } ^ { l o c a l } + x _ { k } ^ { v 2 r } E _ { k , i } ^ { v 2 r } + x _ { k } ^ { v 2 u } E _ { k , u } ^ { v 2 u } + x _ { k } ^ { v 2 v } E _ { k , m } ^ { v 2 v } .\tag{43}
$$

The optimization goal and constraints of the computation offloading problem of UAV-assisted VEC are as follows:

$$
\mathbf { P 2 } : \operatorname* { m i n } _ { X , F } \left( \frac { 1 } { \sum _ { i = 1 } ^ { I } R _ { i } ^ { v } } \sum _ { i = 1 } ^ { I } \sum _ { k = 1 } ^ { R _ { i } ^ { v } } ( \kappa _ { t } T _ { k } + \kappa _ { e } E _ { k } ) \right) ,\tag{44}
$$

$$
\mathrm { s . t . } \quad \kappa _ { t } + \kappa _ { e } = 1 ,\tag{44a}
$$

$$
\begin{array} { r } { x _ { k } ^ { l o c a l } , x _ { k } ^ { v 2 r } , x _ { k } ^ { v 2 v } , x _ { k } ^ { v 2 u } \in \{ 0 , 1 \} , } \end{array}\tag{44b}
$$

$$
x _ { k } ^ { l o c a l } + x _ { k } ^ { v 2 r } + x _ { k } ^ { v 2 u } + x _ { k } ^ { v 2 v } = 1 , \forall k \in { \cal K } ,\tag{44c}
$$

$$
\sum _ { k = 1 } ^ { K } f _ { k , u } \leq f _ { u , \operatorname* { m a x } } , \sum _ { k = 1 } ^ { K } f _ { k , i } \leq f _ { i , \operatorname* { m a x } } , \sum _ { k = 1 } ^ { K } f _ { k , m } \leq f _ { m , \operatorname* { m a x } } ,\tag{44de}
$$

$$
T _ { k } \leq t _ { k , \mathrm { m a x } } , T _ { k } \leq t _ { \mathrm { c o n } } ,\tag{44e}
$$

where (44a) indicates the sum of the weights is 1, (44b) and (44c) indicate that a task can choose only one offloading mode. (44d) indicate the sum of the computing resources allocated cannot exceed the maximum amount. (44e) indicates that the total delay does not exceed the maximum tolerable time, and the total delay does not exceed the connection delay.

## IV. PROBLEM SOLUTION AND ALGORITHM DESCRIPTION

## A. Outline of Proposed Solution

The goal of P1 is to optimize the deployment position of the UAV by maximizing RSSI. By optimizing the deployment position of the UAV, the data transmission rate can be greatly improved. The purpose of P2 is to reduce the system energy consumption and latency of the vehicle to process all computation tasks under acceptable delay constraints. Reasonable deployment of the UAV position during computation offloading can ensure the communication quality of vehicle and reduce the latency and energy consumption of completing the task by reducing the communication cost between the UAV and the vehicle. For P1, we use the GA to solve for the optimal deployment coordinates of the UAV in different time slots (Algorithm 1). The P2 has constraints on continuous variables, such as the coordinates $C o _ { u }$ of the UAV, and constraints on discrete variables, such as $x _ { k } ^ { l o c a l }$ . Also, it has nonlinear constraints such as constraint (44e). Therefore, the P2 is a mixed-integer nonlinear programming (MINLP) problem, and it is difficult to find the optimal solution in polynomial time [36]. However, the P2 can be modeled as an MDP $M = ( S , A , P , R )$ . In our GFL-PEARL algorithm, the positions and velocities of UAVs and vehicles, as well as the positions of RSUs, are used as state inputs for the neural network. By learning from these input features, the neural network can capture various factors affecting communication quality, including the impact of the distance between devices on RSSI. This approach enables the system to address signal fluctuations in complex urban environments, ensuring successful task completion and connectivity for full task offloading.

1) State Space: At the time slot t, the state space can be expressed as $S _ { t } = \{ H _ { t } , C O _ { t } , F _ { t } \}$ , where $H _ { t } = \{ h _ { 1 } , h _ { 2 } , . . . , h _ { K } \}$ ï¼ $h _ { k } = \{ Q _ { k } , p _ { k } , v _ { k } , \theta _ { k } \} . \ C O _ { t } = \{ C o _ { k } , C o _ { u } , C o _ { i } \} . \ F _ { t } = \{ F _ { k } $ . $F _ { u } , F _ { i } \}$ is the computing resource set.

2) Action Space: In time slot t, the action space $a _ { t }$ is defined as $a _ { t } = \{ X _ { k } , F _ { k } \} , \forall k \in K .$ , where $X _ { k } =$ $\{ x _ { k } ^ { l o c a l } , x _ { k } ^ { v 2 r } , x _ { k } ^ { v 2 u } , x _ { k } ^ { v 2 v } \}$ and $F _ { k } = \{ f _ { k } ^ { l o c a l } , f _ { k , i } ^ { v 2 r } , f _ { k , u } ^ { v 2 u } , f _ { k , m } ^ { v 2 v } \}$ denote the offloading and resource allocation decision, respectively.

3) Reward Function: The optimization objective is to minimize the weighted delay and energy consumption. Therefore, the reward function is as follows:

$$
R ( s _ { t } , a _ { t } ) = - \sum _ { i = 1 } ^ { I } \sum _ { k = 1 } ^ { R _ { i } ^ { v } } ( \kappa _ { t } t _ { k } + \kappa _ { e } E _ { k } ) .\tag{45}
$$

The state space and optimization objective are coupled with the coordinates of the UAV. Therefore, after obtaining the UAV coordinates, we input them into P2 and use the GFL-PEARL algorithm to solve offloading strategy (Algorithm 2).

## B. UAV Deployment Optimization Algorithm

In the GA, the cost function is same as (9). In initialization phase, the population is generated randomly, and the fitness function is same as (8). The algorithmâs pseudo-code is shown in Algorithm 1. The main time expense of the Algorithm 1 is incurred by the two-level loop structure, so the time complexity of UAV trajectory optimization algorithm based on genetic algorithm is $O ( I t e r \times P o p s i z e )$ , where Iter is the number of iterations and P opsize is the population size.

Algorithm 1: UAV Deployment Optimization Based on GA.   
Input: Number of iterations Iter, population size   
$P o p S i z e , C o _ { k }$ , lower   
bound P os_M in, upper bound P os_M ax.   
Output:UAVâs optimal positions.   
1: for $\mathrm { i } { = } 1 { : } P o p S i z e$ do   
2: posi = rand(P os_M in, P os_M ax)   
3: Calculating RSSIi   
4: end for   
5: for k=1:Iter do   
6: for i=1:P opSize do   
7: Chromosome crossover, mutation   
8: Get next generation $p o s _ { i } = p o s _ { i + 1 }$   
9: Calculating RSSIi   
10: CurrBestRSSIi = M ax(RSSIi)   
11: CurrBestposi = posi   
12: end for   
13: GlobalBestRSSIi = M ax(CurrBestRSSIi)   
14: GlobalBestBestposi = M ax(CurrBestposi)   
15: end for   
16: returnUAVâs optimal positions

## C. GFL-PEARL-Based Computation Offloading

The PEARL algorithm introduces a task belief Z to help agents make reasonable decisions, so its policy function is $\pi _ { \boldsymbol { \theta } } \big ( a _ { t } | s _ { t } , z \big )$ PEARL learns and inference Z by variational inference methods [37], and its core process is defining and training an inference network $q _ { \eta } ( z | c )$ . The variational lower bound on the objective function is:

$$
E _ { T } [ E _ { z \sim q _ { \eta } ( z | c ^ { T } ) } [ R ( T , z ) + \beta D _ { K L } ( q _ { \eta } ( z | c ^ { T } ) | | p ( z ) ) ] ] ,\tag{46}
$$

where $R ( T , z )$ is the objective function, and $p ( z )$ is the prior Gaussian distribution of Z. According to the replacement invariance, $q _ { \eta } ( z | c )$ is denoted as:

$$
q _ { \eta } ( z | c _ { 1 : N } ) \propto \prod _ { n = 1 } ^ { N } \mathcal { N } ( f _ { \eta } ^ { u } ( c _ { n } ) , f _ { \eta } ^ { \sigma } ( c _ { n } ) ) ,\tag{47}
$$

where $f _ { \eta }$ is a neural network with parameter Î·. Network $f _ { \eta } ^ { u } ( c _ { n } )$ estimates the mean. Network $f _ { \eta } ^ { \sigma } ( c _ { n } )$ estimates the variance. The PEARL loss function is as follows:

$$
L _ { a c t o r } = E _ { \underbrace { ( s _ { t } , a _ { t } ) \sim D } _ { a \sim \pi _ { \theta } ( z | c ) } } \left[ D _ { K L } \bigg ( \pi ( a _ { t } | s _ { t } , \overline { { z } } ) \bigg | \bigg | \frac { \exp ( Q ^ { \pi } ( s _ { t } , a _ { t } , \overline { { z } } ) ) } { Z ^ { \pi } ( s _ { t } ) } \bigg ) \right] ,\tag{48}
$$

$$
L _ { c r i t i c } = E _ { ( s _ { t } , a _ { t } ) \sim D } [ \frac { 1 } { 2 } ( Q _ { \theta } ( s _ { t } , a _ { t } , z ) 
$$

$$
- \mathbf { \nabla } \big ( R ( s _ { t } , a _ { t } ) + \gamma E _ { s _ { t } ^ { \prime } \sim p } [ V _ { \overline { { \theta } } } ( s _ { t } ^ { \prime } , \overline { { z } } ) ] ) \big ) ^ { 2 } \bigg ] ,\tag{49}
$$

$$
L _ { K L } = \beta D _ { K L } \big ( q ( z | c ) | | p ( z ) \big ) .\tag{50}
$$

For meta-learning, multiple tasks are faced; hence, meta-loss is used to update the parameters. The meta-loss is as follows:

$$
f ^ { \theta } = \sum _ { n = 1 } ^ { N } L _ { c r i t i c } ^ { n } , f ^ { \phi } = \sum _ { n = 1 } ^ { N } L _ { a c t o r } ^ { n } , f ^ { \eta } = \sum _ { n = 1 } ^ { N } { ( L _ { c r i t i c } ^ { n } + L _ { K L } ^ { n } ) } ,\tag{51}
$$

where M is the size of a batch of tasks.

We model context c as a DAG and reconstruct the inference network using the graph network. For a sampling process $c ^ { i }$ during training, we model it as $C ^ { i } = ( c ^ { i } , g ^ { i } )$ , $c ^ { i }$ containing several transitions. $g ^ { i }$ corresponds to the adjacency matrix of these transitions. If there is $s _ { t _ { 1 } + 1 }$ equal to $s _ { t _ { 2 } }$ for the transition $\left( { { s _ { t } } _ { 1 } } , { { a } _ { t } } _ { 1 } , { { r } _ { t } } _ { 1 } , { { s } _ { t } } _ { 1 + 1 } \right)$ and $\left( { { s _ { t _ { 2 } } } , { a _ { t _ { 2 } } } , { r _ { t _ { 2 } } } , { s _ { t _ { 2 } + 1 } } } \right)$ in $c ^ { i } .$ , then +1the value of the corresponding position $( t _ { 1 } , t _ { 2 } )$ in $g ^ { i }$ will be 1.

$$
g ^ { i } ( t _ { 1 } , t _ { 2 } ) = { \left\{ \begin{array} { l l } { 1 } & { i f \ s _ { t _ { 1 } + 1 } = s _ { t _ { 2 } } } \\ { 0 } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }\tag{52}
$$

The node features in the DAG, i.e., the features $F _ { i }$ of the state transfer process $\left( { { s _ { i } } , { a _ { i } } , { r _ { i } } , { s _ { i + 1 } } } \right)$ and the adjacency matrix of the directed graph, are inputted into the GNN to obtain the high-dimensional features of the node $F _ { i } ^ { \prime }$ :

$$
a t t e n _ { i j } = \frac { \exp ( \mathrm { L e a k y R e L U } ( a ^ { T } [ W F _ { i } | | W F _ { j } | ) ) } { \sum _ { k \in N o d e _ { i } } \exp ( \mathrm { L e a k y R e L U } ( a ^ { T } [ W F _ { i } | | W F _ { k } ] ) ) } ,\tag{53}
$$

$$
F _ { i } ^ { \prime } = \prod _ { k = 1 } ^ { K } { \mathrm { S i g m o i d } } \left( \sum _ { j \in N o d e _ { i } } a t t e n _ { i j } ^ { k } W ^ { k } F _ { j } \right) ,\tag{54}
$$

where $a t t e n _ { i j }$ is the attention coefficient, representing the weight of the state transfer process $t _ { j }$ in the set of neighboring nodes of $t _ { i } , \ N o d e _ { i }$ denotes the set of neighboring points of $t _ { i } .$ . After obtaining $F _ { i } ^ { \prime }$ , it is inputted into the encoder network constructed through LSTM according to the processing order of DAG nodes. The encoding result depends on its characteristics and the previous state, and the encoding result is denoted as $\mathrm { e c } = [ \mathrm { e c } _ { 1 } , \mathrm { e c } _ { 2 } , . . . , \mathrm { e c } _ { n } ]$

$$
\mathrm { e c } _ { i } = e n c o d e r ( F _ { i } ^ { \prime } , e c _ { i - 1 } ) .\tag{55}
$$

After obtaining the encoding of each transfer process, we define the input of the decoder as follows:

$$
d c _ { i } = d e c o d e r ( c t _ { i } , d c _ { i - 1 } , a _ { i - 1 } ) ,\tag{56}
$$

$$
c t _ { i } = \sum _ { j = 0 } ^ { n } \alpha _ { i j } e c _ { j } ,\tag{57}
$$

$$
\alpha _ { i j } = \frac { \exp ( e v a l ( d c _ { i - 1 } , e c _ { j } ) ) } { \displaystyle \sum _ { k = 1 } ^ { n } \exp ( e v a l ( d c _ { i - 1 } , e c _ { k } ) ) } ,\tag{58}
$$

where $c t _ { i }$ is the feature vector of the i-th step, $\alpha _ { i j }$ is the attention coefficient, eval is a network for evaluating the degree of match

between the output at the i-1-th position and the input at the j-th position. The final output is into a three-layer MLP using the Softmax function.

$$
A _ { D A G } = s o f t m a x ( i n p u t ) .\tag{59}
$$

We improve the sampler of the PEARL algorithm by proposing a reward-based prioritization sampler $R S _ { \mathrm { c } }$ , makcing the algorithm more likely to reach those highly rewarded states [38]. Therefore, we use a simple way to prioritize sampling:

$$
\overline { { r _ { \mathrm { t } } } } = e ^ { \mu r \left( s _ { t } , a _ { t } \right) } + \varepsilon ,\tag{60}
$$

where $\overline { { r _ { \mathrm { t } } } }$ is the sampling priority of transition $( s _ { t } , a _ { t } ,$ $r ( s _ { t } , a _ { t } ) , s _ { t } ^ { \prime } ) , \mu$ is a constant greater than $0 ,$ and Îµ constant greater than 0 to prevent a situation where the priority tends to zero. After the introduction of priority sampling, due to greedy strategy of intelligent body, it may lead to some transitions with low priority not being sampled all the time, thus falling into local optimum or even divergence. It is necessary to introduce sampling weights, before which sampling probability of a sample is

$$
P R _ { \mathrm { t } } = { \frac { { \overline { { \mathrm { r _ { t } } } } } } { \sum _ { \mathrm { s } } { \overline { { \mathrm { r _ { s } } } } } } } .\tag{61}
$$

According to the sampling probability, the sampling weight of the sample is defined as:

$$
W _ { \mathrm { t } } = \frac { [ N _ { \mathrm { s a m p l e } } \times P R _ { \mathrm { t } } ] ^ { - \beta } } { \mathrm { m a x _ { s } } \{ W _ { s } \} } ,\tag{62}
$$

where $\beta \in ( 0 , 1 ]$ is used to control the number, $N _ { s a m p l e }$ is the number of samples, and when calculating $W _ { t } .$ , it is necessary to replace $W _ { s }$ with $\overline { { r _ { s } } } .$ . Algorithm 2 show the pseudo-code, and the computation offloading framework based on FML is shown in Fig. 2.

Complexity analysis: The GFL-PEARL based computational offloading algorithm requires a total of $O ( I t )$ iterations, during each iteration, the RSU obtains the global parameters and sends them down to the vehicles in the coverage area, hence the time complexity is $O ( I t * ( I + K ) )$ . Then, each vehicle needs to collect data for different meta-tasks to populate the experience playback pool, hence the time complexity is $O ( N * T * P )$ , where P is a model parameter. Finally, each vehicle needs to select data from the playback pool to update the model parameters in reverse, with a time complexity of $O ( S * N * P )$ . Without considering aggregation and uploading, the total time complexity is about $O ( I t * ( I + K ) * ( \mathrm { T } + \mathrm { S } )$ $* N * P )$ .

## D. Offloading Decision Algorithm

As shown in Algorithm 3, after the training stage, an offloading decision-making algorithm will be executed. Let n represent the number of iterations and m represent the number of steps in each iteration. We assume that the complexity of the sampling operation is $O ( p )$ , where $p$ is the number of sampled data points. The complexity of the action selection operation is $O ( a )$ , where p is the size of the action space. The complexity of executing the action and obtaining the reward is O(e), and the complexity of the state update operation is O(s). Therefore, the overall complexity of Algorithm 3 can be expressed as $O ( n \times m \times ( p + a + e + s ) )$ .

<!-- image-->  
Fig. 2. The computation offloading framework based on FML.

<!-- image-->  
Fig. 3. UAV-assisted VEC experimental framework.

## V. EXPERIMENTAL RESULTS AND ANALYSIS

## A. Experimental Setup

To verify the UAV deployment algorithm proposed in this paper, we used OMNet+SUMO to simulate real traffic scenarios. In details, the OMNet is a network simulator that simulates wireless network communication, and SUMO is a traffic simulator that generates real network scenarios and is available to other programs. The main parameters of the experiment are shown in Table IV.

To verify the computation offloading algorithm proposed in this paper, we built a laboratory-level drone-assisted vehiclemounted edge computing platform, and the experiment framework is shown in Fig. 3, where the UAV carries a Raspberry Pi to provide computing resources for the requesting vehicle. We use the classical DNN model YOLOv2 to recognize driversâ driving behaviors and perform computation offloading experiments using the trained model. The experimental datasets are the YawDD [40] and Kaggle State Farm [41] datasets. These datasets contain images and videos of abnormal driving behaviors. To protect the user privacy, these images are preprocessed locally on the device, such as through feature extraction [42], before being used for further analysis. The main parameters of the simulation experiment are shown in Table V. The experiment results shown are the averages of 30 simulations, together with 95 percent confidence intervals.

<!-- image-->  
Fig. 4. UAV deployment.

To measure the performance of the algorithms, we choose average delay, average energy consumption, average cost, and task timeout rate as evaluation metrics. We choose IGPSO [13], DCOM [24], FedMetaR2Ag [31] and FedAvg [46] as comparison algorithms. IGPSO algorithm combines the diversity of GA algorithms with the fast convergence of PSO algorithms, thus has a better performance compared to traditional heuristic algorithms. DCOM is a multi-agent reinforcement learning algorithm, which improves the actor-critic network structure by considering the correlation between experiences. FedMetaR2Ag combines FL with the MAML algorithm and aggregates gradients by averaging losses. Both of them are similar to the proposed algorithm in terms of optimization objective, algorithmic type, or application scenarios, but are essentially different. Hence, we choose them as benchmarks.

## B. Results and Analysis

1) The Simulation Results of UAV Deployment: As shown in Fig. 4, we set up four UAVs and fifty vehicles and iteratively solve optimal deployment location of UAVs by GA algorithm. It can be seen that the four UAVs all provide good coverage for ground vehicles in the area, providing communication and computing services for the vehicles.

2) The Experimental Results of Computation Offloading: This study is conducted under following scenario: when RSU is overloaded or unavailable, the frequency of offloading to UAVs increases; conversely, the usage frequency of UAVs is lower.

Fig. 5 shows the convergence performance of all algorithms. From Fig. 5, we can see that GFL-PEARL is better than the benchmark algorithm and FedAvg. GFL-PEARL converges after about 300 iterations and is faster compared to DCOM and FedAvg, because meta-learning is able to adapt to dynamic and complex VEC environments and train personalized models for different users in the face of different data distributions. Moreover, it performs better than FedMetaR2Ag, because we use a graph neural network to better capture the correlation between experiences. In conclusion, our proposed GFL-PEARL algorithm is more suitable for dynamic and complex in-vehicle edge computing scenarios.

Fig. 5. Convergence performance.  
Algorithm 2: GFL-PEARL-Based Computation Algorithm 3: Offloading Decision.   
Offloading. Input: Global parameters $\overline { { { \theta ^ { g } } , \phi ^ { g } } }$ and $\eta ^ { g } ,$ the number of   
Input: Training rounds It; $C o _ { u } \mathrm { ; }$ Batch of training task iterations K, the number of steps per iteration T.   
$\{ \tau _ { i } \} _ { i = 1 \dots N } ;$ Learning Rate $\lambda _ { 1 } , \lambda _ { 2 } , \lambda _ { 3 } ;$ Time Step $T ;$ Output: Offloading and Allocation Strategies $X ^ { * } , F ^ { * }$   
=1Training Step S. 1: for each episode $k = 1 , 2 , . . . , K$ do   
Output: Global parameters for pre-training $\theta ^ { g } , \phi ^ { \mathrm { g } } ,$ , and $\eta ^ { g } .$ 2: Initialize networks and get the state $s _ { t } .$   
1: for $s = 1 , 2 , . . . , I t$ do 3: for each slot $t = 1 , 2 , . . . , T$ do   
2: for Each RSU $i , i \in I$ do 4: Sample $z \sim q _ { \eta } ( z | c ^ { k } )$ by inference network.   
3: i gets parameters $\theta ^ { i }  \theta ^ { g } , \phi ^ { i }  \phi ^ { g } , \eta ^ { i } ,  \eta ^ { g }$ 5: Get the action $a _ { t }$ from $\pi _ { \boldsymbol { \theta } } ( a | s , z )$   
4: for Each vehicle k, $k \in K$ do 6: Execute the action $a _ { t }$ and get the reward $r _ { t } .$   
5: $\theta ^ { k }  \theta ^ { i } , \phi ^ { k }  \phi ^ { i } , \eta ^ { k }  \eta ^ { i }$ 7: Update status $s _ { t } ^ { \prime } .$   
6: for each $\tau _ { i }$ do 8: end for   
7: Initialize replay buffer $D _ { i } , c ^ { i } = \{ \}$ 9: end for   
8: for $t = 1 , . . . , T$ do 10: returnXâ, Fâ.   
9: Sampling $z \sim q _ { \eta } ( z | c ^ { i } )$   
10: $a _ { t } \sim \pi _ { \theta } ( a | s , z ) , r _ { t } \sim R ( s , a ) .$ TABLE IV   
11: $s _ { t } ^ { \prime } \sim p ( s _ { t } ^ { \prime } | s _ { t } , a _ { t } ) , ( s _ { t } , a _ { t } , r _ { t } , s _ { t } ^ { \prime } )  D _ { i } .$ UAV DEPLOYMENT PARAMETERS   
12: 13: $c ^ { i } = \{ ( s _ { t } , a _ { t } , s _ { t } ^ { \prime } , r _ { t } ) \} _ { t : 1 \dots T } \sim D _ { i } .$   
end for The ineliertK) Value   
14: end for The UAV's amount (U) 4   
15: for step in training steps do The vehicle's transmission power $\overline { { ( p _ { k } ^ { t r a n s } ) } }$ 30dBm   
16: for each $\tau _ { i }$ do The Mamr frauey ed 3g 2GHs   
17: $c ^ { i } \sim R S _ { c } ( D _ { i } ) , ( s , a , r , s ^ { \prime } ) ^ { i } \sim D _ { i } .$ The maximum distance $\overline { { d _ { m a x } ^ { u } [ 3 9 ] } }$ 30m   
18: Sample $z \sim q _ { \eta } ( z | c ^ { i } )$ boundary Xmax,ymax 200mï¼200m   
19: Calculate $L _ { a c t o r } ^ { i } , L _ { c r i t i c } ^ { i } , L _ { K L } ^ { i }$ Coverage radius R 45m   
20: 21: end forCalculate $f ^ { \theta } , f ^ { \phi } , f ^ { \eta } . \theta \gets \theta - \lambda _ { 1 } \nabla _ { \theta } f ^ { \theta } ,$ 0.5002   
22: $\phi  \phi - \lambda _ { 2 } \nabla _ { \phi } f ^ { \phi } . \eta  \eta - \lambda _ { 3 } \nabla _ { \eta } f ^ { \eta } .$ COMPUTATION OFFLOADING PARAMETERS   
23: end for   
24: The k uploads meta-losses to i. Parameter Value   
25: end for ThThountofUA caed RSu(d) [10.50]   
26: i calculates loss and uploads parameter and loss. Total Channel bandwidth W 10MHz   
27: end for The vehicle's CPU frequency femax 2GHz   
28: The cloud server aggregate globally (2). The CU reqoUAfdRSU $\underline { { f _ { i , \mathrm { m a x } } } }$ 15GHzs4Mz   
29: end for The task's volume ration (uk) 50cycles/bit   
30: returnglobal network parameters $\theta ^ { g } , \phi ^ { g }$ and $\eta ^ { g } .$ FML aggregation parameter $[ 4 3 ] \lambda , \beta$ 10,1.5   
FML connection ratio 0.8   
The learning rate [31] $\overline { { \lambda _ { 1 } , \lambda _ { 2 } , \lambda _ { 3 } } }$ 0.003   
-60 The AC targetsothiootmt 0.008   
$\overline { { [ 5 ] \ ( \omega ^ { u a v } ) } }$   
The task's maximum tolerable time [1.5,5.0]s   
The task batch size M 128   
The UAV's hovering power $\overline { { \psi _ { u } \left[ 2 \right] } }$ 80W   
Training epoch 600   
FedAvg Proposed FedMetaR2Ag attenuation factor Encoder time-steps [44] $\overline { { \kappa _ { L o S } , \kappa _ { N L o S } \ [ 4 5 ] } }$ 1.7,24 64   
-140 DCOM Gaussian Noise power g -110dBm   
100 200 Train Episode 300 400 500 600 Environmental constants The UAV's flying height H $\mu _ { a } , \mu _ { b }$ 11.61, 0.12 60m   
The time slot t 0.5s

<!-- image-->

As shown in Fig. 6, with the number of iterations increases, the performance of the four algorithms improves. When the number of iterations reaches 600, in terms of task timeout rate, the GFL-PEARL algorithm is 87.7% lower than the IGPSO algorithm, 75% lower than the DCOM algorithm, and 54.5% lower than the FedMetaR2Ag algorithm. When the number of iterations reaches about 150, the IGPSO algorithm falls into a local optimum. The proposed algorithm is more effective than the DCOM algorithm because the deterministic policy in the DCOM algorithm is not conducive to action exploration and may also fall into local optimality. The proposed algorithm has a better performance compared to the FedMetaR2Ag algorithm, which is based on the SAC algorithm, which uses stochasticity policy, which outputs the policy in the algorithm in a way that not only ensures that the rewards are maximized but also ensures that the entropy of the information is maximized, and thus is able to explore more space than the FedMetaR2Ag algorithm.

<!-- image-->  
(a) Average Delay

<!-- image-->  
(bï¼Average Energy Consumption

<!-- image-->  
(cï¼ Average Cost

<!-- image-->  
(d) Task Timeout Rate  
Fig. 6. The impact of the number of iterations on performance.

In Fig. 7, with the increasing number of vehicles, all metrics of different algorithms are increasing. When number of intelligent vehicles reaches 50, in terms of task timeout rate, the GFL-PEARL algorithm is 31.72% lower than the IGPSO algorithm, 22.03% lower than the DCOM algorithm, and 12.39% lower than the FedMetaR2Ag algorithm. As the number of intelligent vehicles increases, the IGPSO algorithm cannot reasonably unload tasks that cannot be handled locally by the vehicles, resulting in these tasks being unable to be completed within the tolerable time. The deterministic gradient of the DCOM algorithm limits its exploration ability. The FedMetaR2Ag algorithm combines the characteristics of meta-reinforcement learning, and its performance is similar to that of the algorithm in this paper. The proposed algorithm is based on the SAC algorithm, which takes into account the information entropy of the strategy and has a strong ability to explore strategies. It is not easy to fall into the local optimum when the number of intelligent vehicles increases and the Markov space becomes complex. The metrics of the proposed algorithm increase smoothly with minimal fluctuations, indicating that the system exhibits good stability. Moreover, as the number of vehicles increases from 10 to 50, the task timeout rate remains below 18%.

<!-- image-->  
(a) Average Delay

<!-- image-->  
Number of Smart Vehicles

(bï¼ Average Energy Consumption  
<!-- image-->  
(cï¼ Average Cost

<!-- image-->  
(d) Task Timeout Rate

Fig. 7. The impact of the number of intelligent vehicles on performance.  
<!-- image-->  
(a) Average Delay

<!-- image-->  
(b) Task Timeout Rate  
Fig. 8. The impact of the maximum tolerable time on performance.

Fig. 8 shows that as the maximum tolerable time increases, the average delay of tasks completed within the tolerable time also gradually increases. When the tolerable time is 1.5 s, the average delay of tasks completed within the tolerable time of the four algorithms is similar. Because tolerable time is short, to complete the task more quickly, more computing resources need to be allocated, and computing resources are short. Hence, tasks completed on time are close to the completion time limit. As the tolerable time increases, the computing resources that need to be allocated to process each task decrease, and the performance gap of the algorithm begins to appear. When the maximum tolerable time reaches 5 s, the GFL-PEARL algorithm is 30.76% lower than the IGPSO algorithm, 25.21% lower than the DCOM algorithm, and 9.34% lower than the FedMetaR2Ag algorithm in terms of average time delay. In addition, our algorithm takes approximately 0.57 milliseconds to make a decision on the RSU server,ch is far below the maximum tolerance time.

As shown in Fig. 9, the average cost of different algorithms and the task timeout rate continue to increase as the task size increases. This is because the increase in the task size leads to an increase in the computing resources required to process the task, and hence, the cost and task timeout rate required to process the task increases continuously. As the task size increases, the

<!-- image-->  
(a) Average Cost

<!-- image-->  
(b) Task Timeout Rate

Fig. 9. The impact of the task size on performance.  
<!-- image-->

<!-- image-->  
(a) Average Delay

(b) Task Timeout Rate  
<!-- image-->  
(c) Average Delay

<!-- image-->  
(d) Task Timeout Rate  
Fig. 10. The impact of the maximum tolerable time at different SNR.

IGPSO algorithm adapts poorly to changes in the environment and has the largest increase in average cost and task timeout. When the task size reaches 6.8 Mbit, the GFL-PEARL algorithm is 28.45% lower than the IGPSO algorithm, 21.9% lower than the DCOM algorithm, and 14.82% lower than the FedMetaR2Ag algorithm in terms of average cost.

We added Gaussian noise to the wireless channel with different SNR values to study the performance under different channel conditions. Fig. 10 shows the impact of the maximum tolerance time on the release delay and the task completion rate under twochannel conditions (SNR = 2 dB or 20 dB). When the channel condition is poor, the average delay and task timeout rate of the four algorithms increase. This is because when the power of the vehicle transmitting data remains unchanged, the poor channel condition will lead to a decrease in the transmission rate, thus increasing the offload delay. Under a certain maximum tolerance time, the increase in the offloading delay will inevitably lead to an increase in the task timeout rate. When channel conditions are poor, the task timeout rate of the algorithm proposed in this paper is reduced by 56. 3%, 49. 3% and 16. 6% compared to the IGPSO, DCOM and FedMetaR2Ag algorithms. The algorithm proposed in this paper is relatively less affected by changes in channel conditions. This is because the algorithm is based on the SAC algorithm, which ensures the maximization of information entropy. Therefore, it has better adaptability to environmental changes than the other three algorithms.

<!-- image-->  
(a) Task Completion Rate

<!-- image-->  
(b) Average Delay  
Fig. 11. UAV ablation study: Task completion rate and average delay.

To verify the behavior and usage frequency of UAVs in the system, we conducted an ablation study, as shown in Fig. 11. In both the full UAV and full RSU offloading scenarios, task completion rates dropped sharply. In the scenarios without UAVs and in the scenario with UAVs, the task completion rate gradually decreased with increase in vehicle numbers. When number of vehicles is 50, the task completion rate with UAVs was 90.6%, compared to only 84.52% without UAVs. This trend indicates that as vehicle numbers grow, UAV usage frequency increases, helping alleviate high RSU loads. Regarding task latency, the latency for full local vehicle computing remained relatively stable, around 4.57 seconds. The full UAV offloading scenario saw a latency increase of nearly 198% with 50 vehicles, while the full RSU offloading scenario experienced a 64% latency increase. In vehicle-RSU collaboration scenario, latency showed a 72% reduction compared to all-local vehicle computing. Although the computing power of UAVs is inferior compared to vehicles, when the RSU load is high, they are as candidate options, considerably improving task completion rate and reducing delay.

## VI. CONCLUSION AND FUTURE WORKS

In this paper, we analyze the computation offloading problem in UAV-assisted VEC. We built a computation offloading model with goal of minimizing the system delay and energy consumption. Besides, we also constructed a UAV movement model to dynamically adjust the UAVâs deployment position to be more realistic. Finally, we convert the offloading decision problem into an MDP problem and solve it using GFL-PEARL algorithm. The experimental results verify the superiority of GFL-PEARL algorithm compared with the benchmark algorithm. In the future, we will focus on extending the framework to multi-UAV cooperative scenarios and incorporating more sophisticated energy harvesting and security mechanisms to further enhance system performance and resilience. In the future, we will focus on extending the framework to multi-UAV cooperative scenarios and incorporating more sophisticated energy harvesting and security mechanisms to further enhance system performance and resilience.

## REFERENCES

[1] Z. Han, Y. Yang, W. Wang, L. Zhou, T. N. Nguyen, and C. Su, âAge efficient optimization in UAV-aided VEC network: A game theory viewpoint,â IEEE Trans. Intell. Transp. Syst, vol. 23, no. 12, pp. 25287â25296, Dec. 2022.

[2] X. Dai, Z. Xiao, H. Jiang, and J. C. Lui, âUAV-assisted task offloading in vehicular edge computing networks,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2520â2534, Apr. 2024.

[3] C. Yang, B. Liu, H. Li, B. Li, K. Xie, and S. Xie, âLearning based channel allocation and task offloading in temporary UAV-assisted vehicular edge computing networks,â IEEE Trans. Veh. Technol, vol. 71, no. 9, pp. 9965â9977, Sep. 2022.

[4] J. K. Abadi, Z. Zahra, N. Mansouri, and M. M. Javidi, âDeep reinforcement learning-based scheduling in distributed systems: A critical review,â Knowl. Inf. Syst., vol. 66, pp. 5709â5782, 2024.

[5] S. Liang, H. Wan, T. Qin, J. Li, and W. Chen, âMulti-user computation offloading for mobile edge computing: A deep reinforcement learning and game theory approach,â in Proc. IEEE Int. Conf. Commun. Technol., 2020, pp. 1534â1539.

[6] J. Yan, S. Bi, and Y. J. A. Zhang, âOffloading and resource allocation with general task graph in mobile edge computing: A deep reinforcement learning approach,â IEEE Trans. Wireless Commun, vol. 19, no. 8, pp. 5404â5419, Aug. 2020.

[7] B. Shi, Y. Pan, and L. Huang, âDeep reinforcement learning based task offloading and resource allocation strategy across multiple edge servers,â Service Oriented Comput. Appl., vol. 14, no. 1, pp. 1â14, 2024.

[8] R. Chen, Y. Fan, S. Yuan, and Y. Hao, âVehicle collaborative partial offloading strategy in vehicular edge computing,â Mathematics, vol. 12, no. 10, May 2024, Art. no. 1466.

[9] X. Chen, âDecentralized computation offloading game for mobile cloud computing,â IEEE Trans. Parallel Distrib. Syst., vol. 26, no. 4, pp. 974â983, Apr. 2015.

[10] Y. Huang et al., âMulti-agent-deep-reinforcement-learning-enabled offloading scheme for energy minimization in vehicle-to-everything communication systems,â Electronics, vol. 13, no. 3, Feb. 2024, Art. no. 663.

[11] J. Zhang, H. Guo, and J. Liu, âAdaptive task offloading in vehicular edge computing networks: A reinforcement learning based scheme,â Mobile Netw. Appl., vol. 25, no. 5, pp. 1736â1745, 2020.

[12] H. Peng and X. Shen, âDeep reinforcement learning-based resource management for multi-access edge computing in vehicular networks,â IEEE Trans. Netw. Sci. Eng., vol. 7, no. 4, pp. 2416â2428, Fourth Quarter 2020.

[13] J. Bi, H. Yuan, S. Duanmu, M. Zhou, and A. Abusorrah, âEnergy optimized partial computation offloading in mobile-edge computing with genetic simulated-annealing-based particle swarm optimization,â IEEE Internet Things J., vol. 8, no. 5, pp. 3774â3785, Mar. 2021.

[14] H. Zhang, X. Liu, Y. Xu, D. Li, C. Yuen, and Q. Xue, âPartial offloading and resource allocation for MEC-Assisted vehicular networks,â IEEE Trans. Veh. Technol., vol. 73, no. 1, pp. 1276â1288, Jan. 2024.

[15] J. Wang, J. Hu, G. Min, W. Zhan, Q. Ni, and N. Georgalas, âComputation offloading in multi-access edge computing using a deep sequential model based on reinforcement learning,â IEEE Commun. Mag, vol. 57, no. 5, pp. 64â69, May 2019.

[16] P. Zhao, Z. Kuang, Y. Guo, and F. Hou, âTask offloading and resource allocation in UAV-assisted vehicle platoon system,â IEEE Trans. Veh. Technol, vol. 74, no. 1, pp. 1584â1596, Jan. 2025.

[17] G. Feng, C. Wang, and B. Li, âUAV-assisted wireless relay networks for mobile offloading and trajectory optimization,â Peer-to-Peer Netw. Appl, vol. 12, no. 6, pp. 1820â1834, Nov. 2019.

[18] Q. Hu, Y. Cai, G. Yu, Z. Qin, M. Zhao, and G. Y. Li, âJoint offloading and trajectory design for UAV-enabled mobile edge computing systems,â IEEE Internet Things J, vol. 6, no. 2, pp. 1879â1892, Apr. 2019.

[19] Z. Ning et al., âDynamic computation offloading and server deployment for UAV-enabled multi-access edge computing,â IEEE Trans. Mobile Comput, vol. 22, no. 5, pp. 2628â2644, May 2023.

[20] H. Zhang, W. Wu, C. Wang, M. Li, and R. Yang, âDeep reinforcement learning-based offloading decision optimization in mobile edge computing,â in Proc. IEEE Wireless Commun. Netw. Conf., 2019, pp. 1â7.

[21] C. Li, L. Chai, K. Jiang, Y. Zhang, J. Liu, and S. Wan, âDNN partition and offloading strategy with improved particle swarm genetic algorithm in VEC,â IEEE Trans. Intell. Veh, early access, Dec. 25, 2023, doi: 10.1109/TIV.2023.3346506.

[22] N. Shan, Y. Li, and X. Cui, âA multilevel optimization framework for computation offloading in mobile edge computing,â Math. Problems Eng., vol. 2020, no. 1, 2020, Art. no. 412479.

[23] Y.-T. Chuang et al., âA real-time and ACO-based offloading algorithm in edge computing,â J. Parallel Distrib. Comput., vol. 179, 2023, Art. no. 104703.

[24] L. Geng, H. Zhao, J. Wang, A. Kaushik, S. Yuan, and W. Feng, âDeep reinforcement-learning-based distributed computation offloading in vehicular edge computing networks,â IEEE Internet Things J., vol. 10, no. 14, pp. 12416â12433, Jul., 2023.

[25] C. Li, K. Jiang, Y. Zhang, L. Jiang, and S. Wan, âDeep reinforcement learning-based mining task offloading scheme for intelligent connected vehicles in UAV-Aided MEC,â ACM Trans. Des. Autom. Electron. Syst, vol. 29, no. 3, pp. 1â29, 2024.

[26] N. Zhao, Z. Ye, Y. Pei, Y. -C. Liang, and D. Niyato, âMulti-agent deep reinforcement learning for task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Wireless Commun., vol. 21, no. 9, pp. 6949â6960, Sep. 2022.

[27] P. Hou et al., âDistributed DRL-based intelligent over-the-air computation in unmanned aerial vehicle swarm-assisted intelligent transportation system,â IEEE Internet Things J., vol. 11, no. 21, pp. 34382â34397, Nov. 2024.

[28] C. Li, K. Jiang, G. He, F. Bing, and Y. Luo, âA computation offloading method for multi-UAVs assisted MEC based on improved federated DDPG algorithm,â IEEE Trans. Ind. Inf., vol. 20, no. 12, pp. 14062â14071, Dec. 2024.

[29] A. M. Seid, G. O. Boateng, B. Mareri, G. Sun, and W. Jiang, âMulti-agent DRL for task offloading and resource allocation in multi-UAV enabled IoT edge network,â IEEE Trans. Netw. Serv. Manage, vol. 18, no. 4, pp. 4531â4547, Dec. 2021.

[30] H. Hu, G. Huang, X. Li, and S. Song, âMeta-reinforcement learning with dynamic adaptiveness distillation,â IEEE Trans. Neural Netw. Learn. Syst, vol. 34, no. 3, pp. 1454â1464, Mar. 2023.

[31] B. A. Adoum et al., âFederated meta-learning for task offloading and resource allocation in MEC-IoT,â in Proc. Int. Conf. Radar Antenna Microw. Electron. Telecommun, 2023, pp. 122â128.

[32] H. Huang, A. V. Savkin, and C. Huang, âDecentralized autonomous navigation of a UAV network for road traffic monitoring,â IEEE Trans. Aerosp. Electron. Syst, vol. 57, no. 4, pp. 2558â2564, Aug. 2021.

[33] V. Teeda, S. Moro, D. Scazzoli, L. Reggiani, and M. Magarini, âDifferentiation and localization of ground RF transmitters through RSSI measures from a UAV,â IEEE Trans. Veh. Technol, vol. 74, no. 1, pp. 1000â1009, Jan. 2025.

[34] S. Bi and Y. J. Zhang, âComputation rate maximization for wireless powered mobile-edge computing with binary computation offloading,â IEEE Trans. Wireless Commun, vol. 17, no. 6, pp. 4177â4190, Jun. 2018.

[35] J. Zhang et al., âComputation-efficient offloading and trajectory scheduling for multi-UAV assisted mobile edge computing,â IEEE Trans. Veh. Technol, vol. 69, no. 2, pp. 2114â2125, Feb. 2020.

[36] Y. Sahni, J. Cao, L. Yang, and Y. Ji, âMulti-hop multi-task partial computation offloading in collaborative edge computing,â IEEE Trans. Parallel Distrib. Syst, vol. 32, no. 5, pp. 1133â1145, May 2021.

[37] D. P. Kingma et al., âAuto-encoding variational bayes,â in Proc. Int. Conf. Learn. Representations, 2014, pp. 1â14. [Online]. Available: https://doi. org/10.48550/arXiv.1312.6114

[38] Y. Li, J. Li, Z. Lv, H. Li, Y. Wang, and Z. Xu, âGASTO: A fast adaptive graph learning framework for edge computing empowered task offloading,â IEEE Trans. Netw. Service Manag., vol. 20, no. 2, pp. 932â944, Jun. 2023.

[39] F. Song et al., âEvolutionary multi-objective reinforcement learning based trajectory control and task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 12, pp. 7387â7405, Dec. 2023.

[40] 2014. [Online]. Available: https://ieee-dataport.org/open-access/yawddyawning-detection-dataset

[41] 2016. [Online]. Available: https://www.kaggle.com/datasets/rightway11/ state-farm-distracted-driver-detection

[42] S. A. Osia et al., âA hybrid deep learning architecture for privacypreserving mobile analytics,â IEEE Internet Things J., vol. 7, no. 5, pp. 4505â4518, May 2020.

[43] J. Wicaksana et al., âFedMix: Mixed supervised federated learning for medical image segmentation,â IEEE Trans. Med. Imag, vol. 42, no. 7, pp. 1955â1968, Jul. 2023.

[44] Z. Bing, L. Knak, L. Cheng, F. O. Morin, K. Huang, and A. Knoll, âMetareinforcement learning in nonstationary and nonparametric environments,â IEEE Trans. Neural Netw. Learn. Syst, vol. 35, no. 10, pp. 13604â13618, Oct. 2024.

[45] A. Gupta, A. Trivedi, and B. Prasad, âB-GWO based multi-UAV deployment and power allocation in NOMA assisted wireless networks,â Wireless Netw., vol. 28, no. 7, pp. 3199â3211, Jul. 2022.

[46] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. Y. Arcas, âCommunication-efficient learning of deep networks from decentralized data,â in Proc. Int. Conf. Artif. Intell. Statist., 2017, pp. 1273â1282.

<!-- image-->

Yong Zhang received the MS degree from Tiangong University, in 2020. He is currently working toward the PhD degree with the School of Computer Science and Technology, Wuhan University of Technology. His research interests include cloud computing and artifcial intelligence.

<!-- image-->  
Chunlin Li received the BS and MSc degrees in computer science from the Wuhan University of Technology (WUT), China, in 1996 and 2000, respectively, and the PhD degree in computer software and theory from the Huazhong University of Science and Technology (HUST), Wuhan, China, in 2003. She is currently a professor and PhD tutor of computer science with WUT. Her research interests include edge computing.

<!-- image-->  
Chaoyue Deng received the bachelorâs degree from the Wuhan Institute of Technology, in 2022. He is currently working toward the MS degree with the School of Computer Science and Technology, Wuhan University of Technology. His research interests include cloud computing and artifcial intelligence.

<!-- image-->

Shaohua Wan (Senior Member, IEEE) received the PhD degree from the School of Computer, Wuhan University, Wuhan, China, in 2010. He is currently a full professor with the Shenzhen Institute for Advanced Study, University of Electronic Science and Technology of China, Shenzhen, China. From 2016 to 2017, he was a visiting professor with the Department of Electrical and Computer Engineering, Technical University of Munich, Munich, Germany. He is the author of more than 150 peer-reviewed research papers and books, including more than 50

IEEE/ACM Transactions papers, such as IEEE Transactions on Mobile Computing, IEEE Transactions on Wireless Communications, IEEE Transactions on Communications, IEEE Transactions on Intelligent Transportation Systems, ACM Transactions on Internet Technology, IEEE Transactions on Network Science and Engineering, IEEE Transactions on Network and Service Management, IEEE Transactions on Multimedia, ACM Transactions on Embedded Computing Systems, ACM Transactions on Multimedia Computing, Communications, and Applications, IEEE Transactions on Automation Science and Engineering, and many top conference papers in the fields of edge intelligence. His research interests mainly include deep learning for intelligent transportation systems.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_9_img_1.png|page_9_img_1]]
3. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_9_img_2.jpeg|page_9_img_2]]
4. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_9_img_3.jpeg|page_9_img_3]]
5. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_9_img_4.png|page_9_img_4]]
6. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_14_img_1.jpeg|page_14_img_1]]
7. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_14_img_2.jpeg|page_14_img_2]]
8. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_14_img_3.jpeg|page_14_img_3]]
9. [[../extracted_images/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC/page_14_img_4.jpeg|page_14_img_4]]

---

