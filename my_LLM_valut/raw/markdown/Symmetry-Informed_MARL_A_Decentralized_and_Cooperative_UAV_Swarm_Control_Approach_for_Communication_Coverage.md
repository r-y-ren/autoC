# Symmetry-Informed MARL: A Decentralized and Cooperative UAV Swarm Control Approach for Communication Coverage

Rongye Shi , Member, IEEE, Xin Yu , Yandong Wang, Yongkai Tian , Zhenyu Liu , Member, IEEE, Wenjun Wu , Member, IEEE, Xiao-Ping Zhang , Fellow, IEEE, and Manuela M. Veloso, Fellow, IEEE

AbstractâUncrewed aerial vehicle-mounted base stations (UAV-MBSs) provide flexible wireless connectivity, extending communication coverage in underserved areas. Recently, multi-agent reinforcement learning (MARL) has shown great potential for cooperative UAV swarm control to support efficient communication coverage in dynamic and complex environments. However, existing MARL-based methods often suffer from low sample efficiency due to its trial-and-error training characteristics, limiting its ability to control large UAV swarms with continuous state-action space and partial observation. We notice that UAV swarm systems in communication coverage tasks exhibit a spatial symmetry property, e.g., a rotation in the spatial observation of a UAV results in a same rotation in its optimal action. Exploiting this property, we formulate the task as a symmetric decentralized partially observable Markov decision process and introduce symmetry-informed MARL, featuring a novel network called the symmetry-informed graph neural network (SiGNN) to serve as the policy/value networks. SiGNN leverages the inherent symmetry in multi-UAV systems by embedding the symmetry into the network structure, thereby enhancing the training efficiency to handle large swarms with continuous control. Theoretical analysis shows that the SiGNN strictly preserves symmetry properties, which guarantees the effectiveness of the approach. Experiments in simulation were conducted to handle communication coverage using up to 20 UAVs with continuous control. Experimental results demonstrate that SiGNN-based MARL outperforms advanced baselines, verifying its superior sample efficiency, scalability and robustness.

Index TermsâReinforcement learning, graph neural network, symmetry, UAV swarm, communication coverage.

## I. INTRODUCTION

U NCREWED aerial vehicle (UAV) swarms, enabled byadvanced technologies such as artificial intelligence and advanced technologies such as artificial intelligence and mobile computing, have exhibited great potential in a variety of applications, ranging from civilian to military domains [1]. In particular, UAV-mounted base stations (UAV-MBSs) employ UAV to provide flexible and rapid-deployment wireless communication coverage for ground users and points of interest (PoIs) [2], [3]. Thanks to fast development of UAV technologies [4], [5], swarms of UAV-MBSs are able to operate cooperatively for communication coverage to provide high quality of service (QoS) in underserved areas such as disaster region, battlefields and congested places [6], [7], [8], [9]. As the demand for UAV swarms grows, it becomes crucial to develop robust control strategies that can enhance their operational capabilities and reliability in terms of coverage rate, energy and scalability.

Some existing studies for UAV swarm-based communication coverage focus on non-learning-based methods such as heuristic methods, approximation algorithms, and rule-based optimizations [10], [11], [12], [13]. These approaches rely extensively on human expertise and iterative solving process, limiting there practicability to real-time deployment and control in complex and dynamic environments. A promising approach to overcoming these limitations involves utilizing learning-based methods, such as multi-agent reinforcement learning (MARL). In recent years, MARL has shown a considerable promise for UAV swarm-based communication coverage, training deep policy networks to control UAVs in a decentralized and cooperative manner [14], [15], [16], [17], [18], [19]. Despite their demonstrated success, MARL-based methods often suffer from low sample efficiency due to its trial-and-error training characteristics, limiting its ability to control large UAV swarms in continuous state-action space and under partial observation, instead of operating in small number of UAVs [14], [15], [16], [18], simplified discrete space [17] or under global observation [14], [19].

Inspired by physics-informed machine learning, an emerging paradigm that seamlessly integrates data-driven learning models with physics [20], this paper explores the possibility of integrating prior knowledge (e.g., the physical properties of the environment and multi-UAV systems) into MARL. This integration aims to facilitate MARL-based UAV control to address the practical and challenging scenarios.

<!-- image-->  
Fig. 1. Illustration of UAV swarm communication coverage tasks in underserved areas. The task generally exhibits spatial symmetry property, i.e., rotating a UAVâs spatial observation by 90â¦ leads to the same 90â¦ rotation in the UAVâs optimal action.

As shown in Fig. 1, we observe that UAV swarm systems engaged in communication coverage tasks often exhibit a property known as spatial symmetry. For example, a rotation in the spatial observation of a UAV results in a corresponding rotation in its optimal action. Symmetry in UAV swarm systems facilitates a more uniform and predictable behavior among individual UAVs, which is crucial for maintaining formation integrity and operational coherence in dynamic environments. This uniformity allows the swarm to respond collectively and efficiently to environmental variables, which enhances the systemâs overall stability and reliability.

By leveraging the symmetry property, we formulate the task as a symmetric decentralized partially observable Markov decision process (symmetric Dec-POMDP) and introduce a novel network structure called the symmetry-informed graph neural network (SiGNN), which serves as the backbone of policy and value network in the MARL framework. SiGNN leverages the inherent symmetry in multi-UAV systems by integrating this symmetry into its network structure, thus improving training and sample efficiency for coordinating large swarms with continuous control. Additionally, SiGNN includes an adjacency processing module that utilizes aggregation embedding to adapt to varying numbers of adjacent UAVs and PoIs under partial observation. Theoretical analysis shows that our network structure strictly preserves the symmetry, thereby providing a theoretical guarantee of the methodâs effectiveness.

The main contributions are as follows:

- Introduce the concept of spatial symmetry into the UAV swarm-based communication coverage task and newly formulate the task as a symmetric Dec-POMDP;

Propose the SiGNN and the corresponding MARL, which integrates the symmetry inherently to the network structure for improving training efficiency and performance;

- Theoretically analyze that the proposed network structure strictly preserves the symmetry property, showing that our design is theoretically sound; and

- Design and conduct evaluation experiments using up to 20 UAVs with continuous control. Comprehensive comparison against advanced baselines are made to demonstrate our methods, in terms of coverage rate, energy consumption, coverage redundancy, and other performance on scalability and robustness.

## II. RELATED WORKS

## A. UAV Swarms for Coverage Problem

The area/communication coverage problem can be solved in part by UAV swarm techniques, which involves UAV scheduling [21], [22], path planning [23], [24], navigation control [25], [26], and other related tasks [27], [28]. Approaches in the literature can be broadly categorized into two main groups: nonlearning-based and learning-based methods. Because there exist comprehensive surveys on this topic, we narrow our discussion to heuristic, rule-based and approximation techniques for the former, and multi-agent reinforcement learning for the latter. For more comprehensive surveys, one may refer to [1] and [29].

1) Heuristic, Rule-Based and Approximation Techniques: The coverage problem is usually formulated as an optimization problem. Related literature on solving the area and communication coverage with UAVs reveals a rich diversity of methods aimed at optimizing resource deployment. Heuristic methods such as the artificial bee colony (ABC) algorithm have been effectively used to minimize the number of UAVs required while ensuring optimal coverage and QoS [30]. As a combined method, the ordered ABC-based placement (OAP) algorithm clusters users and determines the optimal 3D positions of UAVs [12], [31]. Separate heuristics can be operated in a hierarchical manner to reduce computational time [32] while optimizing coverage efficiency for crowded areas, such as stadium environments [10].

Genetic algorithms (GA) and particle swarm optimization (PSO)-based methods are also widely used. For example, a multi-population GA method was introduced to enhance the optimization of a UAVâs 2D position, aiming to maximize the number of users that the UAV can serve [33]. PSO has been leveraged to adjust UAV flight paths by simulating the social behavior of bird flocks to maximize area coverage and minimize resource usage for rescue operation [34]. An improved multi-objective particle swarm optimization (MOPSO) algorithm based on the adaptive angle area division was proposed to concern the threat constraint for improved multi-UAV task assignment [35].

Rule-based techniques are proposed to guide the scheduling of vehicle-mounted systems to optimize the coverage [36], [37]. For example, the edge-prior placement (EPP) for selecting users based on UAVsâ proximity to the boundary of uncovered areas [38]. Rule-based methods are simple and fast to implement, albeit less adaptive to dynamic changes in the environments [13].

To handle more practical, constrained and scalable scenarios, approximation algorithms are introduced, especially for fair communications in UAV networks [6], [39], [40]. These approaches involve iterative solving processes and have to draw a balance between processing time and optimality, limiting their practicability to large-scale and real-time deployment in complex and dynamic environments.

2) MARL-Based Swarm Techniques: UAV swarms function as multi-agent systems, and advanced multi-agent approaches, such as MARL,1 are gaining increasing attention, particularly for large-scale control and highly dynamic coverage tasks. The most straightforward MARL-based manner to control UAV swarms at scale is the use of decentralized training with decentralized execution (DTDE) paradigm, in which agents are trained and executed independently without shared information. Independent proximal policy optimization (IPPO) has been applied to UAVassisted fair communications [19], and techniques like reward shaping and parameter sharing were used to obtain multi-UAV coordination and high scalability (e.g., up to 20 UAVs). [17] refrained the use of global information in the training phase and applied recurrent graph network to aggregate multi-hop neighbors for inter-UAV collaboration. However, a complete independent training is impractical to achieve cooperative swarm control, and these works either more or less make use of global information in training, such as all UAVsâ and ground usersâ positions [19], or simplify the task setting to operate in discrete state and action spaces [17].

The mainstream MARL framework is the centralized training with decentralized execution (CTDE), which trains agents using a shared, centralized information structure but executes them independently [41]. This is also the main MARL-based framework for multi-UAV coverage problems, offering improved training stability and coordination capabilities, which is of great importance when addressing practical multi-UAV control with continuous state and action spaces. Advanced CTDE MARL methods for UAV swarm coverage tasks involve the use of transformer MARL (T-MARL) for variable input dimensions [18], state-based game with actor-critic algorithm (SBG-AC) which features modeling the interactions among UAVs using game theory [42], hypergraph convolution mix DDPG for improved coordination in UAV deployment [43], graph convolution MARL [15] and state-action spaces [15], [44]. In addition, Xu et al. proposed a MARL algorithm that combines intrinsic reward based on feedback from large language models (LLM) and a grouped parameter sharing mechanism to effectively improve network coverage [45].

Unfortunately, these methods do not yet scale well for controlling even a relatively small number of UAVs (3 to 10 UAVs), indicating that controlling a large number of UAVs for communication coverage tasks in continuous spaces remains a challenging task.

## B. Knowledge-Informed MARL

A major difficulty preventing MARL from scaling effectively for practical tasks lies in its low sample efficiency, due to the MARLâs trial-and-error training characteristics. Extensive research has been conducted on improving the training efficiency of MARL [46], [47], [48], [49]. With the advent of physics-informed machine learning [20], it is believed that incorporating external domain knowledge into learning models can enhance sample and training efficiency. Recent research has been conducted to improve machine learning models with domain knowledge, such as embedding the traffic models, seismic wave equations and fluid mechanics into neural networks for prediction and estimation purpose [50], [51], [52], [53].

## C. Progress of Symmetry Property-Related Studies

Symmetry is a general property exhibited in the UAV swarm systems and can be leveraged to improve the MARL-based UAV control. Although still relatively scarce, symmetry-guided learning is emerging as a frontier of the deep learning field [54]. Related works include symmetry-guided data augmentation, which creates extra data by applying permutation transformations to homogeneous agents [55]. Symmetry consistency loss was proposed to leverage symmetry to regularize the MARL training [48], while this method has been extended to partial symmetric environments [49]. These methods learn the symmetry in a soft constrained manner, and heavy training overhead and hyperparamenter tuning are involved though the requirement for the absolute trial-and-error sample data is relaxed. Hard symmetry constraint can encode symmetry into networks to decompose global symmetries into local symmetries that each agent can handle, while this method is reported suitable for discrete spaces [47].

Permutation symmetry is a type of non-geometric symmetry that describes a systemâs equivariance when its inputs or components are rearranged (permuted) in different orders. Recent studies have encoded permutation symmetry into policy networks to boost MARL [56]. Such permutation equivariant policy networks have been applied to the UAV communication scheduling of ground users, where the UAV trajectory design is boosted by data augmentation by exploiting rotational and reflection symmetries [57]. However, the exploration of spatial symmetry networks in UAV swarm tasks remains lacking which constitutes the primary contribution of this paper.

To our knowledge, this paper is the first to leverage the spatial symmetry-informed networks to the UAV swarm coverage tasks using MARL. The proposed SiGNN leads to an efficient symmetry-informed MARL framework, suitable for more practical and challenging settings. The paper will simultaneously concern continuous control space, partial observation (varying numbers of adjacent UAVs and PoIs) and a large number of UAVs (up to 20 UAVs), verifying our methodâs superior sample efficiency, scalability and robustness.

## III. SYSTEM MODEL AND RESEARCH OBJECTIVE

## A. System Model of the UAV Swarm

In this paper, we describe the UAV swarm control scenario for communication coverage on a 2D plane, as shown in Fig. 1. Let $\mathcal { N } = \{ i | i = 1 , 2 , . . . , N \}$ be the set of UAVs = = 1 2equipped with base stations cooperating to support the communication needs of ground users and other PoIs. The plane is a continuous target area: $\{ ( x , y ) | 0 \leq x \leq L _ { \mathrm { l e n g t h } } , 0 \leq y \leq$ $L _ { \mathrm { w i d t h } } ; L _ { \mathrm { l e n g t h } } , L _ { \mathrm { w i d t h } } \in \mathbb { R } ^ { + } \}$ ( ) 0 0. The PoIs in the PoI set, $\kappa =$ $\{ k | k = 1 , 2 , . . . , K \}$ =, are randomly distributed across the target = 1 2area. Each UAV launches from a random location and performs the communication coverage task over $T$ time steps (each time step is indexed by t). Each UAV has a fixed coverage radius $R _ { \mathrm { c o } }$ and observation radius $R _ { \mathrm { { o b s } } }$ on the 2D plane. We usually have $R _ { \mathrm { { o b s } } } \geq R _ { \mathrm { { c o v } } }$

1) UAV Model: In this scenario, each UAV i is located at position $( x _ { i } , y _ { i } )$ . The dynamics of the UAVs are driven by ( )the velocities in the horizontal and vertical directions, denoted as $v _ { i } = ( v _ { x _ { i } } , v _ { y _ { i } } )$ with $\lvert \lvert v _ { i } \rvert \rvert \le v _ { \mathrm { m a x } }$ . Consequently, the UAV = ( )system adheres to the kinematic model as follows:

$$
\left\{ \begin{array} { l l } { \dot { x } _ { i } = v _ { x _ { i } } , } \\ { \dot { y } _ { i } = v _ { y _ { i } } . } \end{array} \right.\tag{1}
$$

This dynamics of UAVs is implemented as $\boldsymbol { x } _ { i } ^ { t + 1 } = \boldsymbol { x } _ { i } ^ { t } + \boldsymbol { v } _ { x _ { i } } ^ { t }$ and $y _ { i } ^ { t + 1 } = y _ { i } ^ { t } + v _ { y _ { i } } ^ { t }$ in the simulation engine, where the superscript = +indicates the specific time step t. The controller of each UAV determines the velocity to be executed, i.e., the action of UAV i at time t is given as

$$
a _ { i } ^ { t } = \left( v _ { x _ { i } } ^ { t } , v _ { y _ { i } } ^ { t } \right) .\tag{2}
$$

From the viewpoint of UAV i, global observation is not available. Instead, a local observation $o _ { i } ^ { t }$ is accessible, consisting of four elements: 1) The position element ${ \bf o } _ { i } ^ { \mathrm { p o s } } = ( x _ { i } ^ { t } , y _ { i } ^ { t } )$ = ( )containing the location information of the UAV itself, 2) the velocity element $\mathbf { o } _ { i } ^ { \mathrm { v e l } } = ( v _ { x _ { i } } ^ { t - 1 } , v _ { y _ { i } } ^ { t - 1 } ) = a _ { i } ^ { t - 1 } , 3 )$ the element $\mathbf { o } _ { i } ^ { \mathrm { { U A V } } }$ = ( ) =regarding the adjacent UAVs within the observable region, and 4) the element $\mathbf { o } _ { i } ^ { \mathrm { { P o l } } }$ regarding the adjacent PoIs within the coverage region.

Specifically, a UAV j is included into the adjacency set of UAV i if the relative distance $d _ { i j } \leq R _ { \mathrm { o b s } }$ . Thus, we can define the adjacent element as $\mathbf { o } _ { i } ^ { \mathrm { U A V } } = \{ ( d _ { i j } , \sin \theta _ { i j }$ , $\theta _ { i j } ) | j \in$ $N _ { / i } , d _ { i j } \leq R _ { \mathrm { o b s } } \}$ , where $\theta _ { i j }$ = ( sin cos )is the angle between the line segment from UAV i to UAV j and the heading direction of UAV i. Note, $\mathcal { N } _ { / i }$ is the set with element i excluded. Similarly, the PoI related element is defined on the adjacent PoIs, i.e., $\mathbf { o } _ { i } ^ { \mathrm { P o I } } = \{ ( d _ { i k } , \sin \theta _ { i k } , \cos \theta _ { i k } ) | k \in K , d _ { i k } \leq \bar { R _ { \mathrm { c o v } } } \}$ . As a result, = ( sin cos )the local observation of UAV i is represented as:

$$
o _ { i } ^ { t } = \left\{ \mathbf { o } _ { i } ^ { \mathrm { p o s } } , \mathbf { o } _ { i } ^ { \mathrm { v e l } } , \mathbf { o } _ { i } ^ { \mathrm { U A V } } , \mathbf { o } _ { i } ^ { \mathrm { P o I } } \right\} .\tag{3}
$$

The PoIs within the coverage region of one of the UAVs will be automatically served. To encourage cooperation among UAV swarm, it is assumed that each UAV can share their position information with its adjacent UAVs. We use the adjacency matrix $E \in \{ 0 , 1 \} ^ { N \times N }$ to indicate the connection between UAVs and 0 1it is a symmetric matrix.

2) Evaluation Metrics: An important part of the UAV swarm model is the evaluation metric system. Similar to [15], we introduce three key metrics to comprehensively evaluate the coverage effectiveness, distribution rationality and energy efficiency of the UAV swarm control in the tasks. The first metric is coverage index, measuring the average number of time steps that each PoI is covered and served by any UAV in one episode with T time steps. To normalize this value into [0,1], we further divide it by the number of time steps past, i.e., T . At any time step t, a PoI k is indicated as covered if its distance to the closest the UAV i is smaller than the coverage radius $R _ { \mathrm { c o v } }$ . Therefore, the normalized coverage index $c _ { \mathrm { c o v e r a g e } }$ of an episode with T time steps is defined as the follow:

$$
c _ { \mathrm { c o v e r a g e } } = \frac { \sum _ { t = 1 } ^ { T } \sum _ { k = 1 } ^ { K } \mathbb { 1 } _ { \mathrm { c o v } } ^ { t } ( k ) } { K T } ,\tag{4}
$$

where $\mathbb { 1 } _ { \mathrm { c o v } } ^ { t } ( k )$ is the indicator function $\mathbb { 1 } ( \exists i \in \mathcal { N } , s . t . , d _ { i k } \leq$ $R _ { \mathrm { c o v } } )$ ( ) (, indicating whether the PoI k is covered and served at the )time step t. An indicator function 1 Â· returns one if a specified condition is met, and zero otherwise. This index guarantees $c _ { \mathrm { c o v e r a g e } } \in [ 0 , 1 ]$ and evaluates how often each PoI is connected [0 1]to one of the UAVs, quantifying the coverage performance of the UAV swarm in one episode.

However, the coverage index may score equally high as long as a fixed majority of PoIs are covered, and several UAVs may overlap to serve the same PoI. This is discouraged because, in emergency response scenarios such as flooding, it is crucial that each PoI is evenly served by the UAV swarm to mitigate situations where a large number of victims gather in the same place and a single UAV struggles to support the overwhelming communication demands. Here, we introduce the following anti-overlap index:

$$
c _ { / \mathrm { o v e r l a p } } = 1 - \frac { \sum _ { t = 1 } ^ { T } \sum _ { i = 1 } ^ { N } \mathbb { 1 } _ { \mathrm { o v e r l a p } } ^ { t } ( i ) } { N T } ,\tag{5}
$$

where $\mathbb { 1 } _ { \mathrm { o v e r l a p } } ^ { t } ( i )$ is the indicator function 1 count $\{ j \in$ $\mathcal { N } _ { / i } \mid d _ { i j } \leq \dot { R _ { \mathrm { c o v } } } \} \geq n _ { \mathrm { t h r d } } )$ (, regarding whether the UAV i overlaps with more than $n _ { \mathrm { t h r d } }$ )other UAVs. Here, we set the overlapping threshold $n _ { \mathrm { t h r d } } = 3$ . Obviously, we have $c _ { / \mathrm { o v e r l a p } } \in [ 0 , 1 ]$ and a larger $c _ { / \mathrm { o v e r l a p } }$ = 3 [0 1]implies a more fair spatial distribution of UAVs when serving the PoIs in the area.

Finally, we consider the energy consumption of the UAV swarm to construct the third index. Following the power consumption model in [58], we decompose energy consumption of the UAV i into three parts when executing an action $a _ { i } ^ { t }$ at time t: 1) the base energy used to maintain the UAVâs basic functioning status, which is a constant $e _ { 0 } > 1 , 2 )$ the energy consumed to 1overcome air resistance due to flight speed, which is proportional to ||vti ||, and 3) the additional energy used due to acceleration (changes in speed), which is proportional to $\lvert | v _ { i } ^ { t } - v _ { i } ^ { t - 1 } \rvert |$ . It is noted that the power to support auxiliary communication is another part of the UAV energy consumption. However, this consumed energy is often smaller compared with the movement energy [42], especially when limited UAV communication resources are distributed to each PoI for light weight data transmission in emergent scanarios, such as disaster relief. Therefore, we focus on energy consumption for UAV movements and ignore the consumption for auxiliary communication for simplification. Specifically, the energy consumption of UAV i at time t is:

$$
e _ { i } ^ { t } = e _ { 0 } + \beta _ { \mathrm { s p e e d } } \times | | \boldsymbol { v } _ { i } ^ { t } | | + \beta _ { \mathrm { a c c } } \times | | \boldsymbol { v } _ { i } ^ { t } - \boldsymbol { v } _ { i } ^ { t - 1 } | | ,\tag{6}
$$

where $\beta _ { \mathrm { s p e e d } }$ and $\beta _ { \mathrm { a c c } } \in \mathbb { R } ^ { + }$ are the coefficients converting the speed and acceleration to energy consumption, respectively. Because a UAV has a maximal speed $v _ { \mathrm { m a x } }$ , the energy consumption rate is bounded by $e _ { \mathrm { m a x } } = e _ { 0 } + \beta _ { \mathrm { s p e e d } } | | v _ { \mathrm { m a x } } | | + \beta _ { \mathrm { a c c } } | | v _ { \mathrm { m a x } } - 0 | |$

For an undertrained UAV, its behavior could be irrational, leading to aimless flying around, which results in very high energy consumption. However, such extreme cases are rare as the training continues, and we are more concerned with how to distinguish the energy consumption between optimal and suboptimal strategies. Therefore, we leverage the logarithmic scaling to make extreme energy consumption less significant. The energy index is then defined as the follow:

$$
c _ { \mathrm { e n e r g y } } = \log _ { e _ { \mathrm { m a x } } } { \frac { \sum _ { t = 1 } ^ { T } \sum _ { i = 1 } ^ { N } e _ { i } ^ { t } } { N T } } .\tag{7}
$$

Because $e _ { i } ^ { t } \in ( 1 , { e _ { \operatorname* { m a x } } } ]$ , the index is normalized to (0,1]. The closer the energy index $c _ { \mathrm { e n e r g y } }$ is to one, the more severe the energy consumption becomes.

We combine all the three indexes to define the comprehensive evaluation index, i.e. the coverage anti-overlap energy (CAE) score of the UAV swarm control performance in an episode, defined as:

$$
C A E = { \frac { c _ { \mathrm { c o v e r a g e } } \times c _ { \mathrm { / o v e r l a p } } } { c _ { \mathrm { e n e r g y } } } } .\tag{8}
$$

3) Research Objective: The overall research objective the paper concerned is to find an optimal UAV swarm control policy $\pi ^ { * }$ that can maximize the expected CAE score in an episode, i.e.,

$$
\pi ^ { * } = \arg \operatorname* { m a x } _ { \pi } \mathbb { E } _ { \pi } [ C A E ] ,\tag{9}
$$

where $\mathbb { E } _ { \pi } [ C A E ]$ is the episodic expectation of the CAE score [ ]when the UAV swarm is controlled under the policy Ï. For a UAV swarm system, the policy Ï is composed of individual policies $\pi _ { i } , \mathrm { i . e . , } \pi = ( \pi _ { 1 } , . . . , \pi _ { N } )$ . Based on the CAE score, a more = ( )reasonable policy should obtain a higher coverage index while mitigating overlapping situations and energy consumption.

## B. Preliminaries of Symmetric Dec-POMDP

1) Definition of Dec-POMDP: We first provide the definition of the decentralized partially observable Markov decision process (Dec-POMDP) [48].

An N-agent cooperative task can be formulated as an Dec-POMDP, represented using a tuple $( \mathcal { N } , \mathcal { S } , \mathcal { O } , \mathcal { A } , \mathcal { T } , r , \gamma , \Omega )$ ( Î©)Here, N denotes the set of agents, S is the state space, O is the joint observation space, and $\mathcal { A } = \mathcal { A } _ { 1 } \times \cdot \cdot \cdot \times \mathcal { A } _ { N }$ is the joint =action space consisting of the individual action space $\mathbf { \mathcal { A } } _ { i }$ of each agent $i \in \mathcal N .$ . The transition function $\mathcal { T } : \mathcal { S } \times \mathcal { A } \times \mathcal { S }  [ 0 , 1 ]$ : [0 1]describes the underlying dynamics of the environment. The (joint) reward function $r : S \times \mathcal { A }  \mathbb { R }$ can be predefined and :shaped to adapt to the task characteristics. The joint return is defined by $\textstyle \sum _ { t = 0 } ^ { \mathrm { \tilde { \infty } } } ( \gamma ) ^ { t } r ( s ^ { t } , a ^ { t } )$ , where $\gamma \in [ 0 , 1 ]$ is the discount ( ) ( ) [0 1]factor. Each agent i has an individual observation space ${ \mathcal { O } } _ { i }$ and a corresponding observation function $\Omega _ { i } : { \cal S }  { \mathcal { O } } _ { i }$ . At state $s ^ { t } .$ each agent i receives a partial observation $o _ { i } ^ { t } = \Omega _ { i } ( s ^ { t } ) \in \mathcal { O } _ { i }$ The joint observation is denoted as $o ^ { t } = ( o _ { 1 } ^ { t } , . . . , o _ { N } ^ { t } ) \in \mathcal { O }$ , with the observation function set $\Omega = ( \Omega _ { 1 } , . . . , \Omega _ { N } )$ ). Each agent i follows its individual policy $\pi _ { i } : \mathcal { O } _ { i } \times \mathcal { A } _ { i } \to [ 0 , 1 ]$ . The policy takes the partial observation $o _ { i } ^ { t }$ as input and generates an action distribution, from which an executable action is sampled, $\mathrm { i . e . , } a _ { i } ^ { t } \sim \pi _ { i } ( \cdot | o _ { i } ^ { t } )$ . For a deterministic policy, $a _ { i } ^ { t } = \pi _ { i } ( o _ { i } ^ { t } )$ . A ( ) = (MARL algorithm aims to learn an optimal joint policy $\pi ^ { * } =$ $( \pi _ { 1 } ^ { * } , . . . , \pi _ { N } ^ { * } )$ , enabling all agents to cooperate to maximize the ( )expected joint return, defined as $\begin{array} { r } { \mathbb { E } _ { \pi } [ \sum _ { t = 0 } ^ { \infty } ( \gamma ) ^ { t } r ( s ^ { t } , a ^ { t } ) ] } \end{array}$

[ ( ) ( )]2) Definition of Mathematical Symmetry: The mathematical symmetry is a property that an object, such as state and geometric shape, remain unchanged after a transformation. To fully define this property, it is necessary to provide an overview of the concepts of groups and transformations. A group G in math is a set with a binary operator that satisfies the four mathematical properties (also known as group axioms): identity, inverse, closure, and associativity. According to the characteristics of the UAV swarm-based coverage task, this paper primarily lies its interest in the group âE(2)â, which consists of group actions such as translations, rotations, reflections, and their finite combinations in 2D.

A group action is also called a transformation. For a function $f : \mathcal { X }  \mathcal { V }$ , if there exist two transformation operators $L _ { g } : \mathcal { X }  \mathcal { X }$ and $K _ { q } : \mathcal { V }  \mathcal { V }$ associated with a group element $g \in G ,$ , such that $\Breve { K _ { g } } [ f ( x ) ] = f ( L _ { g } [ x ] )$ for any $x \in \mathcal { X }$ , then [ (we say that the function $f$ = ( [ ])is equivariantly symmetric under the transformations $L _ { g }$ and $K _ { g }$ . When $K _ { g } = I ,$ the identity =function, then we say that the function f is invariantly symmetric under the transformation $L _ { g }$ . The equivariant symmetry and the invariant symmetry constitutes the concepts of symmetry in this paper.

3) Definition of Symmetric Dec-POMDP: The symmetric Dec-POMDP is a subclass of Dec-POMDP, of which the optimal policy possesses the symmetry property. Specifically, let $\pi ^ { * } = ( \pi _ { 1 } ^ { * } , . . . , \pi _ { N } ^ { * } )$ be the optimal joint policy following which the agents can operate cooperatively to maximize the expected joint return. Then, we call the Dec-POMDP a symmetric Dec-POMDP if $\pi ^ { * }$ is equivariantly-symmetric, i.e.,

$$
\pi _ { i } ^ { * } \left( L _ { g } [ o _ { i } ] \right) = K _ { g } \left[ \pi _ { i } ^ { * } \left( o _ { i } \right) \right] = K _ { g } [ a _ { i } ^ { * } ] , \forall i \in \mathcal { N } ,\tag{10}
$$

under some transformations $L _ { g } : \mathcal { O } \to \mathcal { O }$ and $K _ { g } : { \mathcal { A } }  { \mathcal { A } }$ on : :the observation space and action space, respectively.

## C. Modeling UAV Coverage Task as Symmetric Dec-POMDP

The physical meaning of âsymmetryâ in a UAV swarm system defined in this paper is that when the UAVâs physical observation features are altered by a specific transformation $L _ { g }$ , the UAVâs control action should change through a corresponding transformation $K _ { g }$ to maintain consistent performance. Fig. 2 provides a simple yet highly practical transformation operationârotation.

Specifically, the rotation transformation through an angle Î¸ in a 2D system around a specific point is written as a matrix $R _ { \theta } = [ c o s \theta , - s i n \theta ; s i n \theta , c o s \theta ]$ , and the set of $R _ { \theta }$ is called a rotation group g. By operating the rotation on the observation vector x of a UAV in the swarm, we are conducting the calculation: $L _ { g } [ \mathbf { x } ] = R _ { \theta } \mathbf { x } = \mathbf { x } ^ { \prime }$ . In the original state depicted on the left, [ ] = =the optimal policy Ï directs UAV1 to move downward to avoid overlapping coverage with UAV3, i.e., $\mathbf { a } = \pi ( \mathbf { x } )$ . When the = ( )whole state, encompassing the features of UAV swarm systems and PoIs, undergoes a rotation $L _ { g }$ with $\theta = 9 0 ^ { \circ }$ , the UAV1âs observation rotates $9 0 ^ { \circ }$ , accordingly, and the optimal action for UAV1 becomes moving leftward, resulting in the same 90â¦ rotation in UAV1âs action. Because we have $\mathbf { a } ^ { \prime } = \pi ( R _ { \theta } \mathbf { x } ) =$ $\pi ( L _ { g } [ \mathbf { x } ] ) = L _ { g } [ \pi ( \mathbf { x } ) ] = L _ { g } [ \mathbf { a } ]$ , by setting $K _ { g } = L _ { g }$ , the policy ( [ ]) = [ ( )] = [ ] =Ï is equivariantly symmetric to the rotation transformation $R _ { \theta }$

<!-- image-->  
Fig. 2. Illustration of rotation symmetry in UAV swarm communication coverage tasks.

In practical applications such as communication coverage and drone arts, the symmetry property typically holds. Particularly when UAV swarms perform missions based on symmetrical structures, e.g., formation patterns (circles, hexagons, or grids), the symmetry property is inherent to the tasks. In such cases, leveraging the symmetry as prior knowledge to train the policy can reduce the need for additional learning efforts, improving the training and mission execution efficiency.

Without special notice, we focus on rotational transformations in this paper, although several other transformation operations such as reflections and translations can also apply. Please note that, in this paper, the rotation operation transforms only the states of UAVs and the locations of PoIs. The rotation of other environmental positions is irrelevant as they are not part of the observation.

Based on the symmetry property, we can model the UAV swarm control task for communication coverage as a symmetric Dec-POMDP. We set the discounted factor Î³ to 0.99 and use the kinematic model in (1) as the core of the transition function T to generate the state of the next time step. To fully formulate the symmetric Dec-POMDP, we define the state/observation, action and reward, accordingly.

1) State Space S and Observation Space O: The state space S includes the positions of all the UAVs and PoIs on the 2D area as well as all the velocity information of UAVs. The observation function $\Omega _ { i }$ maps the state $s ^ { t }$ into the individual observation $o _ { i } ^ { t }$ of Î©UAV i as defined in (3). The set of all feasible joint observation defines the observation space O.

2) Action Space A: The action space A jointly includes all the individual velocity spaces Ai. A feasible action $a _ { i } ^ { t }$ is defined by (2).

3) Reward Function r: The remaining element is the reward function r. Although we can directly use the CAE score in (8) as the reward, it is unpractical to the partially observable settings. Also, it can be difficult to determine the contribution each agent made when directly using the CAE score. Designing individual rewards can clarify the impact of each agentâs actions, making it easier to train and optimize their behaviors. Furthermore, the

CAE score requires post-processing, including averaging and normalization, which can obfuscate the distinction between suboptimal actions, making it challenging to train a satisfactory policy. Here, we design the individual reward function $r _ { i } ^ { t }$ , which consists of three terms: coverage term, energy term and overlap term.

The coverage term calculates the independent coverage reward for each agent:

$$
r _ { i } ^ { \mathrm { c o v } } = \lambda ^ { \mathrm { c o v } } \times \frac { | \mathbf { o } _ { i } ^ { \mathrm { P o I } } | } { | \mathcal { N } | \times | \mathcal { K } | } ,\tag{11}
$$

where $| \mathbf { o } _ { i } ^ { \mathrm { P o I } } |$ counts the number of PoIs covered and served by UAV i as defined in (3). This value encourages the UAV to serve the area with dense PoIs. The more PoIs each UAV covers, the more likely that each PoI k can be served, i.e., the probability of $\mathbb { 1 } _ { \mathrm { c o v } } ^ { t } ( k ) = 1$ at each time slot is large. And this contributes to a ( ) =larger coverage index $c _ { c o v e r a g e }$ in (4). The energy term penalizes the energy consumption:

$$
r _ { i } ^ { \mathrm { e n e r g y } } = - \lambda _ { 1 } ^ { \mathrm { e g } } \times | | a _ { i } ^ { t } | | - \lambda _ { 2 } ^ { \mathrm { e g } } \times | | v _ { i } ^ { t } | | .\tag{12}
$$

Obviously, it is a direct modification with a negative sign of the individual energy consumption given in (6), and is negatively contributing to the energy index $c _ { e n e r g y }$ in (7). The overlap term is to prevent UAVs from overly concentrating in the same area, ensure reasonable distribution, and avoid redundant coverage:

$$
\begin{array} { r } { r _ { i } ^ { \mathrm { o v e r l a p } } = - \lambda ^ { \mathrm { o l } } \times \mathbb { 1 } _ { \mathrm { o v e r l a p } } ^ { t } ( i ) , } \end{array}\tag{13}
$$

where each UAV can observe its local coverage redundancy with other UAVs, indicated using $\mathbb { 1 } _ { o v e r l a p } ^ { t } ( i )$ , which is an individual version of the anti-overlap index $c _ { / \mathrm { o v e r l a p } }$ in $( 5 ) . \lambda ^ { \mathrm { c o v } } , \lambda _ { 1 } ^ { \mathrm { e g } } , \lambda _ { 2 } ^ { \mathrm { e g } }$ $\lambda ^ { \mathrm { o l } }$ are coefficients in R+. Taking all the three terms into account, the individual reward function is defined as

$$
r _ { i } ^ { t } = r _ { i } ^ { \mathrm { c o v } } + r _ { i } ^ { \mathrm { e n e r g y } } + r _ { i } ^ { \mathrm { o v e r l a p } } .\tag{14}
$$

Thus far, the UAV swarm control task for communication coverage has been formulated as a symmetric Dec-POMDP model. Here, the joint return becomes $\begin{array} { r } { \dot { \sum { \ i { \ i } } } _ { i = 1 } ^ { N } \sum _ { t = 1 } ^ { T } ( \gamma ) ^ { t } r _ { i } ^ { t } } \end{array}$ , which ( )is approximately proportional to the CAE score of an episode. The goal of a MARL method is to find a UAV swarm control policy Ï to maximize the expected joint return.

## IV. PROPOSED SYMMETRY-INFORMED GRAPH NEURAL NETWORK BASED APPROACH

This section introduces the proposed SiGNN framework in Fig. 3 and provides its design details. We also presents the MARL training framework based on SiGNN. As a main contribution of the paper, the proposed SiGNN-based networks automatically preserve the rotation symmetry property, which is an intrinsic property in symmetric Dec-POMDP. These symmetry-preserving networks positively impact the RL process by eliminating the need for additional trial-and-error to learn a symmetry-preserving policy. This allows the policy to better align with the symmetric Dec-POMDP during training.

For ease of describing the SiGNN, we further divide the features of UAV iâs individual observation $o _ { i } ^ { t } =$ $\{ \mathbf { o } _ { i } ^ { \mathrm { p o s } } , \mathbf { o } _ { i } ^ { \mathrm { v e l } } , \mathbf { o } _ { i } ^ { \mathrm { U A V } } , \mathbf { o } _ { i } ^ { \mathrm { P o I } } \}$ into two parts: the absolute spatial features $P _ { i }$ and the ego-centered relative features $Q _ { i }$ . The absolute spatial features $\bar { P } _ { i } = \{ \mathbf { o } _ { i } ^ { \mathrm { p o s } } , \mathbf { o } _ { i } ^ { \mathrm { v e l } } \}$ includes features defined in =the absolute coordinate system, i.e., the absolute position and velocity, which will change after rotation $L _ { g } , { \mathrm { i . e . , } } P _ { i } \neq L _ { g } [ P _ { i } ]$ The ego-centered relative features $Q _ { i } = \{ \mathbf { o } _ { i } ^ { \mathrm { U A V } } , \mathbf { o } _ { i } ^ { \mathrm { P o I } } \}$ [ ]includes =features defined in the ego-centered coordinate system, i.e., the relative distances and direction angles of the adjacent UAVs and PoIs within the observable region. Obviously, $Q _ { i }$ is invariant to the rotation $L _ { g } , \mathrm { i . e . , } Q _ { i } = L _ { g } [ Q _ { i } ]$ , because the relative distances and direction angles remain the same after rotation from the viewpoint of UAV i. Here, the time step symbol t is omitted for simplifying the representation.

<!-- image-->  
Fig. 3. Overview of the SIGNN framework, which constitutes the core network to train and control the behaviors of UAV i.

Please note that the adjacency matrix E includes the information about which UAVs are observable and connectable by UAV i, such that their position information is shareable with each other. $E _ { i }$ denotes the i-th column of E.

## A. SiGNN Framework Overview

As illustrated in Fig. 3, the overall architecture of SiGNN consists of two primary modules: the Adjacency Processing Module (APM) and the Symmetry-Informed Module (SIM). The APM is designed to pre-process the ego-centered relative features $Q _ { i }$ . These features are unfriendly to policy networks because their dimensions keep changing as the adjacent UAVs and PoIs move in and out of UAV iâs observation. To address this issue, APM employs two sub-modules to pre-process the features ${ \bf o } _ { i } ^ { \mathrm { U A V } }$ and $\mathbf { o } _ { i } ^ { \mathrm { { P o I } } }$ respectively, converting them to the transformed egocentered relative features $\tilde { Q } _ { i }$ , an embedding of fixed dimension.

The SIM takes $\{ P _ { i } , \tilde { Q } _ { i } , E _ { i } \}$ as its input for further processing. It also contains two sub-modules to process the $P _ { i }$ and $\tilde { Q } _ { i }$ jointly. An important note is that the outputs $\{ \underset { \sim } { P } _ { i } ^ { ( 1 ) } , \tilde { Q } _ { i } ^ { ( 1 ) } \}$ are the transformed counterparts of the original $P _ { i } , \bar { Q } _ { i }$ , maintaining the same dimension and form. Then, the $\{ P _ { i } ^ { ( 1 ) } , \tilde { Q } _ { i } ^ { ( 1 ) } , E _ { i } \}$ are fed forward to the next SIM as inputs. There are L SIMs to construct a L-layer feed-forward network structure and we call it as L-layer SIM. Note that $E _ { i }$ consistently serves as part of the inputs of the SIM in each layer.

The SIM of layer L â  releases the final output $\{ P _ { i } ^ { ( L ) } , \tilde { Q } _ { i } ^ { ( L ) } \}$ , and we formulate the whole process of SiGNN

paremeterized by $\theta _ { i }$ as:

$$
\Big \{ P _ { i } ^ { ( L ) } , \tilde { Q } _ { i } ^ { ( L ) } \Big \} = \mathrm { S i G N N } \left( P _ { i } , Q _ { i } , E _ { i } ; \theta _ { i } \right) .\tag{15}
$$

Here, we can extract ${ \mathbf o } _ { i } ^ { \mathrm { v e l } \left( L \right) }$ from $P _ { i } ^ { ( L ) }$ , the counterparts of the original velocity features $\mathbf { o } _ { i } ^ { \mathrm { v e l } }$ , as the action $a _ { i }$ . In this way, the SiGNN serves as a policy network of UAV i, i.e., $a _ { i } = \pi _ { \mathrm { S i G N N } , i } ( o _ { i } , E _ { i } ; \theta _ { i } )$ , mapping the individual observation $o _ { i }$ =to action $a _ { i }$ ( ; )for operation in the current time step.

## B. Adjacency Processing Module (APM)

The APM pre-processes the ego-centered relative features $Q _ { i } = \{ \mathbf { o } _ { i } ^ { \mathrm { U A V } } , \mathbf { \bar { o } } _ { i } ^ { \mathrm { P o I } } \}$ , which are rotation-invariant. Features $Q _ { i }$ =include partially observational information from the viewpoint of UAV i, guiding its intention to cooperate with surrounding UAVs and serve the nearby PoIs for the best coverage. In contrast to global observation with fixed numbers of UAVs and PoIs, the dimension of $Q _ { i }$ keeps varying. The APM is able to deal with the varying inputs and aggregate the adjacency information by employing two adjacency processing sub-modules (sub-APMs): a UAV-related sub-APM and a PoI-related sub-APM.

1) UAV-Related Sub-APM: The UAV-related sub-APM processes $\mathbf { o } _ { i } ^ { \mathrm { { U A V } } }$ , the features of adjacent UAVs. Let $\mathcal { N } ( i )$ be the set of UAVs in the observable region, i.e., $j \in \mathcal { N } ( i )$ (if $d _ { i j } \leq R _ { \mathrm { o b s } }$ ( )This sub-module leverages a multi-layer perceptron $( \mathrm { M L P } ) \phi _ { u a v }$ to calculate a weight for each adjacent UAV j and then makes weighted sum as its output $\tilde { \mathbf { o } } _ { i } ^ { \mathrm { U A V } }$ . The $\mathbf { M L P } \ \phi _ { u a v }$ has multiple hidden layers using rectified linear unit (ReLU) as the activation function. Without special notice, all the MLPs use this structural design. Specifically, this sub-module is formulated as

$$
\tilde { \mathbf { o } } _ { i } ^ { \mathrm { U A V } } = \frac { 1 } { N } \sum _ { j \in \mathcal { N } ( i ) } \left[ \phi _ { u a v } \left( \mathbf { o } _ { i j } ^ { \mathrm { U A V } } \right) \right] \cdot \mathbf { o } _ { i j } ^ { \mathrm { U A V } } ,\tag{16}
$$

where $\mathbf { o } _ { i j } ^ { \mathrm { U A V } }$ denotes the features of adjacent UAV j and N is the number of all UAVs for scaling the output. Because this aggregation is a linear combination of adjacent UAVs, the outputted $\bar { \tilde { \mathbf { o } } } _ { i } ^ { \mathrm { U A V } }$ enjoys a fixed dimension and rotation invariancy is ensured Ëin this sub-module. The weights are sophisticatedly assigned by $\phi _ { u a v } .$ , which is parameterized, enabling this sub-module to process the information of adjacent UAVs in a learnable manner.

2) PoI-Related Sub-APM: The PoI-related sub-APM processes $\mathbf { o } _ { i } ^ { \mathrm { { P o I } } }$ , the features of adjacent PoIs. Let $\kappa ( i )$ be the set of PoIs in the coverage region, i.e., $k \in \mathcal { K } ( i )$ if $d _ { i k } \leq R _ { \mathrm { c o v } }$ . We equip this sub-module with MLP $\phi _ { p o i }$ ( )for aggregation:

$$
\tilde { \mathbf { o } } _ { i } ^ { \mathrm { P o I } } = \frac { 1 } { K } \sum _ { k \in \mathcal { K } ( i ) } \left[ \phi _ { p o i } \left( \mathbf { o } _ { i k } ^ { \mathrm { P o I } } \right) \right] \cdot \mathbf { o } _ { i k } ^ { \mathrm { P o I } } ,\tag{17}
$$

where $\mathbf { o } _ { i k } ^ { \mathrm { P o I } }$ denotes the features of adjacent PoI k and K is the number of all PoIs for scaling the output. Obviously, this submodule is also rotation-invariant.

3) The Outputs of APM: The outputs of the two sub-modules are then concatenated to form the aggregated embedding $\tilde { Q } _ { i } =$ $\{ \tilde { \mathbf { o } } _ { i } ^ { \mathrm { U A V } } , \tilde { \mathbf { o } } _ { i } ^ { \mathrm { P o I } } \}$ . The $\tilde { Q } _ { i }$ =released by the APM along with the absolute spatial features $P _ { i }$ and adjacency matrix $E _ { i }$ forms the input of the SIM.

There are L layers of SIMs in the SiGNN architecture, and we denote the input of the SIM in layer l as $\{ P _ { i } ^ { ( l ) } , \tilde { Q } _ { i } ^ { ( l ) } , E _ { i } \}$ to emphasize the layer-wise information using superscripts, which is initialized by setting $P _ { i } ^ { ( 0 ) } = P _ { i }$ and $\tilde { Q } _ { i } ^ { ( 0 ) } = \tilde { Q } _ { i } , E _ { i }$ =is a constant matrix and superscript is unnecessary.

## C. Symmetry-Informed Module (SIM)

The SIM in layer l jointly processes the hidden absolute spatial features $P _ { i } ^ { ( l ) }$ and transformed ego-centered relative features ${ \tilde { Q } } _ { i } ^ { ( l ) }$ to compute $\{ P _ { i } ^ { ( l + 1 ) } , \tilde { Q } _ { i } ^ { ( l + 1 ) } \}$ with same dimension, serving as part of the input to the next SIM layer.

A SIM also contains two sub-modules: a spatial feature processing (SFP) sub-module and a relative feature processing (RFP) sub-module, which are denoted as $\mathcal { H } _ { \mathrm { s f p } } ^ { ( \lfloor \bar { l } ) }$ and $\mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) }$ , respectively. The feed forward process is described as :

$$
\left( \tilde { Q } _ { i } ^ { ( l + 1 ) } , m _ { i } ^ { ( l ) } \right) = \mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) } \left( P _ { i } ^ { ( l ) } , \tilde { Q } _ { i } ^ { ( l ) } , E _ { i } \right) ,\tag{18}
$$

$$
P _ { i } ^ { ( l + 1 ) } = \mathcal { H } _ { \mathrm { s f p } } ^ { ( l ) } \left( P _ { i } ^ { ( l ) } , \tilde { Q } _ { i } ^ { ( l ) } , E _ { i } , m _ { i } ^ { ( l ) } \right) .\tag{19}
$$

Because $\mathcal { H } _ { \mathrm { s f p } } ^ { ( l ) }$ requires some information $m _ { i } ^ { ( l ) }$ generated from $\mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) }$ to continue its processing, we describe the $\mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) }$ first.

1) Relative Feature Processing $\mathcal { H } _ { r f p } ^ { ( l ) }$ : The RFP sub-module $\mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) }$ takes $\{ P _ { i } ^ { ( l ) } , \tilde { Q } _ { i } ^ { ( l ) } , E _ { i } \}$ as inputs and is equipped with two MLPs $\phi _ { e } ^ { ( l ) }$ and $\phi _ { q } ^ { ( l ) }$ . We leverage $\phi _ { e } ^ { ( l ) }$ to calculate the message $m _ { i j } ^ { ( l ) }$ from each adjacent UAV j and merge all the adjacent messages to calculate the next ${ \tilde { Q } } _ { i } ^ { ( l + 1 ) }$ based on another MLP $\phi _ { q } ^ { ( l ) }$ This technique is called message-passing, which is commonly used in graph network-based methods [54]. Specifically, the $\mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) }$ is formulated as:

$$
m _ { i j } ^ { ( l ) } = \phi _ { e } ^ { ( l ) } \left( \tilde { Q } _ { i } ^ { ( l ) } , \tilde { Q } _ { j } ^ { ( l ) } , \left. P _ { i } ^ { ( l ) } - P _ { j } ^ { ( l ) } \right. ^ { 2 } \right) ,\tag{20}
$$

$$
\tilde { Q } _ { i } ^ { ( l + 1 ) } = \phi _ { q } ^ { ( l ) } \left( \tilde { Q } _ { i } ^ { ( l ) } , \sum _ { j \in \mathcal { N } ( i ) } m _ { i j } ^ { ( l ) } \right) ,\tag{21}
$$

where the term $\lvert | P _ { i } ^ { ( l ) } - P _ { j } ^ { ( l ) } \rvert | ^ { 2 }$ gives the relative squared distance between two vectors. The set of messages received by UAV i from adjacent UAVs is denoted as $m _ { i } ^ { ( l ) } = \{ m _ { i j } ^ { ( l ) } | j \in N ( i ) \}$ $\mathcal { N } ( i )$ is extracted from $E _ { i }$ = (, and this is why we make use of $E _ { i }$ as part of input. Both (20) and (21) define the core operation of the RFP sub-module $\mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) }$ in (18)

TABLE I  
COMPUTATIONAL COMPLEXITY ANALYSIS OF SIGNN ON EACH UAV
<table><tr><td>Module/Sub-Module</td><td>ApproximateMACCs</td></tr><tr><td>APM  $\overline { { { \tilde { Q } } _ { i } ^ { ( 0 ) } } }$  in  $\mathrm { E q . ( 1 6 ) , E q . ( 1 7 ) }$ </td><td> $\xi _ { 1 } = d _ { o _ { i j } } \times d _ { h i d } \times ( N _ { i } + K _ { i } )$ </td></tr><tr><td>Message-passing mij in Eq.(20)</td><td> $\xi _ { 2 } = d _ { P } + ( 2 d _ { \tilde { Q } } + 1 ) \times d _ { h i d } \times d _ { m }$ </td></tr><tr><td>Relative feature  $\tilde { Q } _ { i } ^ { ( l + 1 ) }$  in Eq.(21)</td><td> $\xi _ { 3 } = ( d _ { \tilde { Q } } + 1 ) \times d _ { h i d } \times d _ { \tilde { Q } }$ </td></tr><tr><td>Spatial feature  $P _ { i } ^ { ( l + 1 ) }$  in  $\operatorname { E q . } ( 2 2 )$ </td><td> $\xi _ { 4 } = d _ { \tilde { Q } } \times d _ { h i d } \times 1 \times d _ { P }$   $+ \ N _ { i } \times \ l [ d _ { m } \times d _ { h i d } \times 1 \times d _ { P } ]$ </td></tr></table>

2) Spatial Feature Processing $\mathcal { H } _ { s f p } ^ { ( l ) }$ : With the messages $m _ { i } ^ { ( l ) }$ of adjacent UAVs, the SFP sub-module $\mathcal { H } _ { \mathrm { s f p } } ^ { ( l ) }$ employs two MLPs $\phi _ { m } ^ { ( l ) }$ and $\phi _ { p } ^ { ( l ) }$ to update the spatial features, which is formulated as

$$
\begin{array} { r l r } {  { P _ { i } ^ { ( l + 1 ) } = \phi _ { p } ^ { ( l ) } ( \tilde { Q } _ { i } ^ { ( l ) } ) \cdot P _ { i } ^ { ( l ) } + C \sum _ { j \in \mathcal { N } ( i ) } \phi _ { m } ^ { ( l ) } ( m _ { i j } ^ { ( l ) } ) } } \\ & { } & \\ & { } & { \cdot ( P _ { i } ^ { ( l ) } - P _ { j } ^ { ( l ) } ) , } \end{array}\tag{22}
$$

where C is a constant to control the scale of the second term, involving the influence from adjacent UAVs. (22) indicates that the spatial features $P _ { i } ^ { ( l ) }$ is iteratively updated by a linear combination of itself and its differences from all the adjacent UAVs, with the weights calculated by $\phi _ { p } ^ { ( l ) }$ and $\phi _ { m } ^ { ( l ) }$ , respectively. The weight from $\phi _ { p } ^ { ( l ) }$ is determined by the transformed ego-centered relative features ${ \tilde { Q } } _ { i } ^ { ( l ) }$ to modulate the current $\bar { P _ { i } ^ { ( l ) } }$ and the weights from $\phi _ { m } ^ { ( l ) }$ are mapped from the corresponding messages to regulate the relative features $( P _ { i } ^ { ( l ) } - { P _ { j } ^ { ( l ) } } )$ from the nearby UAV j.

After L-layer feed forward SIM processing, we obtain the final output $\{ \boldsymbol { P } _ { i } ^ { ( L ) } , \boldsymbol { \tilde { Q } } _ { i } ^ { ( L ) } \}$ }, in which $\mathbf { \bar { \rho } } _ { P _ { i } ^ { ( L ) } } = \{ \mathbf { \bar { o } } _ { i } ^ { \mathrm { p o s } ( L ) } , \mathbf { o } _ { i } ^ { \mathrm { v e l } ( L ) } \}$ . The UAV i takes ${ \mathbf o } _ { i } ^ { \mathrm { v e l } \left( L \right) }$ as its action $a _ { i }$ at the current time step and the SiGNN has now been fully defined.

The multiply-accumulate operations (MACCs) of SiGNN on each UAV is presented in Table I. It can be seen that the MLP components, such as $\phi _ { q } .$ , contribute to the most computational complexity due to the involvement of multiply layers. The overall MACC of a SiGNN with L layers is: $\xi _ { 1 } + L \times [ \xi _ { 2 } \times N _ { i } + \xi _ { 3 } + \xi _ { 4 } ]$ , which has the complexity of $O ( L N _ { i } d _ { m } d _ { h i d } + K _ { i } d _ { h i d } )$

## D. Symmetry-Informed MARL Based on SiGNN

The SiGNN framework can serve not only as the policy network (actor) but also as the core component of the value network (critic) to support the centralized training with decentralized execution (CTDE) paradigm in MARL. In CTDE, UAVs are trained on a global and centralized critic, where information from all UAVs can be utilized to evaluate the behaviors. However, during execution, each UAV operates independently, using local observation and individual actor. It is straightforward to employ SiGNN as the actor. Parameter sharing technique can apply because UAVs are homogeneous to share the same individual actor. The remaining component is the centralized critic.

Algorithm 1: Procedure of Symmetry-Informed MARL.   
Input: Number of UAVs N, episode length T , episode   
batch size M.   
Output: Optimized SiGNN-based policy networks ÏSiGNN.   
1: Initialize $\theta = \lbrace \theta _ { i } \rbrace _ { i = 1 } ^ { N }$ , the parameters of   
=SiGNN-based actors ÏSiGNN, and $\psi ,$ the parameters for   
SiGNN-based critic $\Psi _ { \mathrm { S i G N N } }$ and replay buffer D.   
2: for each episode do   
3: for each timestep t from 1 to $T$ do   
4: Get global observation $o ^ { t }$ and adjacency matrix $E ^ { t }$   
5: for each agent i from 1 to N do   
6: Get individual observation $o _ { i } ^ { t }$ and $E _ { i } ^ { t }$   
7: Get action $a _ { i } ^ { t } = \pi _ { \mathrm { S i G N N } , i } ( o _ { i } ^ { t } , \dot { E } _ { i } ^ { t } ; \theta _ { i } )$ on (15).   
8: Execute action $a _ { i } ^ { t } .$ , get $o _ { i } ^ { t + 1 }$ ; )from simulation (1)   
and receive $r _ { i } ^ { t }$ on (14).   
9: Obtain an individual transition $( o _ { i } ^ { t } , a _ { i } ^ { t } , r _ { i } ^ { t } , o _ { i } ^ { t + 1 } )$   
10: end for   
11: Store global transition $\{ ( o _ { i } ^ { t } , a _ { i } ^ { t } , r _ { i } ^ { t } , o _ { i } ^ { t + 1 } ) \} _ { i = 1 } ^ { N }$ into   
replay buffer D.   
12: end for   
13: if episode mod $M = 0$ then   
14: = 0for each mini-batch do   
15: Sample mini-batch $\begin{array} { r } { B \sim \mathcal { D } . } \end{array}$   
16: Update parameters Î¸ of the actors ÏSiGNN on $B .$   
17: Update parameters Ï of the critic SiGNN on $B .$   
18: end for   
19: end if   
20: end for

Let $P = ( P _ { 1 } , \ldots , P _ { N } ) , Q = ( Q _ { 1 } , \ldots , Q _ { N } )$ , and $o = \{ { \cal P } , { \cal Q } \}$ = ( )be the global observation, and $J = [ 1 ] ^ { N \times N }$ ) =be the all-one matrix = [1]denoting a fully observable condition. We introduce the following SiGNN-based centralized value network (critic) SiGNN, parameterized by $\psi = \{ \psi _ { 1 } , \psi _ { 2 } \}$

$$
V = \Psi _ { \mathrm { S i G N N } } \left( o , J ; \psi \right) = \Psi _ { \mathrm { S i G N N } } \left( P , Q , J ; \psi \right) ,\tag{23}
$$

Specifically, the criticâs calculation is broken down as follows:

$$
\left\{ P _ { i } ^ { ( L ) } , \tilde { Q } _ { i } ^ { ( L ) } \right\} = \mathrm { S i G N N } \left( P _ { i } , Q _ { i } , J _ { i } ; \psi _ { 1 } \right) ,\tag{24}
$$

$$
\begin{array} { r } { U = ( U _ { 1 } , . . . , U _ { N } ) , U _ { i } = | | \mathbf { o } _ { i } ^ { \mathrm { v e l } ( L ) } | | ^ { 2 } , } \end{array}\tag{25}
$$

$$
V = \mathrm { F C } \left( \operatorname { t a n h } ( U , Q ) ; \psi _ { 2 } \right) ,\tag{26}
$$

where Â· is the element-wise hyperbolic function and $\operatorname { F C } ( \cdot )$ is the one-layer fully connected network. The designed critic makes an ample use of the velocity and the transformed ego-centred relative features to calculate the centralized value. The squared velocity counterparts in (25) are used to reflect the energy situation. The position counterparts are not used in (26) because it was found to have a trivial impact in practice.

The MARL that leverages the SiGNN-based actor and critic is called a symmetry-informed MARL. By default, we use the popular multi-agent proximal policy optimization (MAPPO) [59] as the backbone of the MARL, though other CTDE MARL frameworks can also apply. The MAPPO learns policy by maximizing the objective: ${ \mathcal { I } } _ { \pi } ( \theta ) =$ $\begin{array} { r l } & { \sum _ { i = 1 } ^ { N } \mathbb { E } _ { \pi _ { \theta _ { \mathrm { o l d } , i } } } [ \frac { \pi _ { \theta _ { i } } ( a _ { i } ^ { t } | { o } _ { i } ^ { t } ) } { \pi _ { \theta _ { \mathrm { o l d } , i } } ( a _ { i } ^ { t } | { o } _ { i } ^ { t } ) } A _ { \theta _ { \mathrm { o l d } , i } } ( { o } _ { i } ^ { t } , a _ { i } ^ { t } ) ] } \end{array}$ , where $\pi _ { \boldsymbol { \theta } _ { i } }$ denotes the $\pi _ { \mathrm { S i G N N } , i } ( \cdot ; \theta _ { i } )$ of agent i, which is the current policy to optimize. $\pi _ { \boldsymbol { \theta } _ { \mathrm { o l d } , i } }$ )is the behavior policy of trajectory experiences. $A _ { \theta _ { \mathrm { o l d } , i } } \left( o _ { i } ^ { t } , a _ { i } ^ { t } \right)$ denotes the advantage function, computed by Gen-( )eralized Advantage Estimation (GAE) on the trajectory. The critic network is trained to maximize the objective: $\mathcal { I } _ { V } ( \psi ) =$ $- \mathbb { E } _ { \pi } [ V _ { \mathrm { t a r g e t } } ^ { \pi } ( o ^ { t } ) - V _ { \psi } ^ { \pi } ( o ^ { t } ) ] ^ { 2 }$ , where $V _ { \mathrm { t a r g e t } } ^ { \pi } \left( o ^ { t } \right)$ ( ) =denotes the target [ ( ) ( )] ( )value (temporal difference target or reward-to-go target) for the global observation $o ^ { t }$ and $V _ { \psi } ^ { \pi }$ denotes $\psi _ { \mathrm { { S i G N N } } } ( \cdot ; \psi )$ to evaluate ( ; )the current policy Ï. The actor and critic networks are updated using $\nabla _ { \boldsymbol { \theta } } \mathcal { I } _ { \pi }$ and $\nabla _ { \psi } \mathcal { J } _ { V }$ , respectively, with gradient clipping. Pseudocode for the symmetry-informed MARL is presented in Algorithm 1.

## V. THEORETICAL ANALYSIS OF SYMMETRY IN SIGNN-BASED POLICY AND VALUE NETWORKS

This section theoretically shows that the proposed SiGNNbased policy and value networks are able to strictly preserve the symmetry property under the rotation transformation $L _ { g } .$ Specifically, we show that each SiGNN-based policy network ÏSiGNN,i is equivariantly symmetric under the rotation transformation $L _ { g } .$ , and the SiGNN-based value network ÏSiGNN is invariantly symmetric under $L _ { g }$ . The first claim regarding the SiGNN-based policy network states as:

Proposition 1: The SiGNN-based policy network $a _ { i } =$ $\pi _ { \mathrm { S i G N N } , i } ( o _ { i } , E _ { i } ; \theta _ { i } )$ is equivariantly symmetric under the rotation (transformation $L _ { g }$ ), which satisfies:

$$
L _ { g } [ a _ { i } ] = \pi _ { \mathrm { S i G N N } , i } ( L _ { g } [ o _ { i } ] , L _ { g } [ E _ { i } ] ; \theta _ { i } ) , \forall i \in \mathcal { N } .\tag{27}
$$

Proof: Because the action $a _ { i } = \mathbf { o } _ { i } ^ { \mathrm { v e l } ( L ) }$ is extracted from $P _ { i } ^ { ( L ) }$ =in (15), which is part of the output of the SiGNN network, we can focus on analyzing the symmetry property of SiGNN. By imposing the rotation transformation $L _ { g }$ on SiGNN, we can make a stronger claim that

$$
\left\{ L _ { g } \left[ P _ { i } ^ { ( L ) } \right] , \tilde { Q } _ { i } ^ { ( L ) } \right\} = \mathrm { S i G N N } \left( L _ { g } \left[ \left\{ P _ { i } , Q _ { i } , E _ { i } \right\} \right] ; \theta _ { i } \right) ,\tag{28}
$$

which is a sufficient condition to (27). Because the rotation does not change the relative features, the ego-centered relative features $Q _ { i }$ and the adjacency matrix E are rotation-invariant, $\mathrm { i . e . , } Q _ { i } = L _ { g } [ Q _ { i } ]$ and $E _ { i } = L _ { g } [ E _ { i } ]$

= [ ] = [ ]The APM is the first module in SiGNN to convert the $Q _ { i }$ to the transformed embedding $\tilde { Q } _ { i } . \tilde { Q } _ { i }$ inherits the rotation invariancy because it is a linear combination of features in $Q _ { i }$ Therefore, we have $\tilde { Q } _ { i } = L _ { g } [ \tilde { Q } _ { i } ]$ . Then, the SIM in layer 0 takes $\{ L _ { g } [ P _ { i } ^ { ( 0 ) } ] , \tilde { Q } _ { i } ^ { ( 0 ) } , E _ { i } \}$ as inputs and feed the results to the SIM [ ]in the next layer.

In each layer l, the RFP sub-module $\mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) }$ is invariantly symmetric, i.e.,

$$
\begin{array} { r } { \left( \tilde { Q } _ { i } ^ { ( l + 1 ) } , m _ { i } ^ { ( l ) } \right) = \mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) } \left( L _ { g } \left[ P _ { i } ^ { ( l ) } \right] , L _ { g } \left[ \tilde { Q } _ { i } ^ { ( l ) } \right] , E _ { i } \right) . } \end{array}\tag{29}
$$

This is because

$$
\begin{array} { r l } { L _ { g } [ m _ { i j } ^ { ( l ) } ] = \phi _ { e } ^ { ( l ) } ( L _ { g } [ \tilde { Q } _ { i } ^ { ( l ) } ] , L _ { g } [ \tilde { Q } _ { j } ^ { ( l ) } ] ,  L _ { g } [ P _ { i } ^ { ( l ) } ]   } & { } \\ {   - L _ { g } [ P _ { j } ^ { ( l ) } ]  ^ { 2 } ) } & { } \\ {  = \phi _ { e } ^ { ( l ) } ( \tilde { Q } _ { i } ^ { ( l ) } , \tilde { Q } _ { j } ^ { ( l ) } ,  L _ { g } [ P _ { i } ^ { ( l ) } - P _ { j } ^ { ( l ) } ]  ^ { 2 } ) } & { } \\ {  = \phi _ { e } ^ { ( l ) } ( \tilde { Q } _ { i } ^ { ( l ) } , \tilde { Q } _ { j } ^ { ( l ) } ,  P _ { i } ^ { ( l ) } - P _ { j } ^ { ( l ) }  ^ { 2 } ) = m _ { i j } ^ { ( l ) } . } \end{array}
$$

The derivation holds because the relative squared distance between two absolute spatial vectors does not change with $L _ { g }$ Also, we have

$$
\begin{array} { r l r } & { } & { L _ { g } \left[ \tilde { Q } _ { i } ^ { ( l + 1 ) } \right] = \phi _ { q } ^ { ( l ) } \left( L _ { g } \left[ \tilde { Q } _ { i } ^ { ( l ) } \right] , \displaystyle \sum _ { j \in \mathcal { N } ( i ) } L _ { g } \left[ m _ { i j } ^ { ( l ) } \right] \right) } \\ & { } & { = \phi _ { q } ^ { ( l ) } \left( \tilde { Q } _ { i } ^ { ( l ) } , \displaystyle \sum _ { j \in \mathcal { N } ( i ) } m _ { i j } ^ { ( l ) } \right) = \tilde { Q } _ { i } ^ { ( l + 1 ) } . } \end{array}
$$

Therefore, we have (29) satisfied and $\mathcal { H } _ { \mathrm { r f p } } ^ { ( l ) }$ is invariantly symmetric. Now, we move forward to show that the SFP sub-module $\mathcal { H } _ { \mathrm { s f p } } ^ { ( l ) }$ is equivariantly symmetric, i.e.,

$$
\begin{array} { r } { L _ { g } \left[ P _ { i } ^ { ( l + 1 ) } \right] = \mathcal { H } _ { \mathrm { s f p } } ^ { ( l ) } \left( L _ { g } [ P _ { i } ^ { ( l ) } ] , L _ { g } \left[ \tilde { Q } _ { i } ^ { ( l ) } \right] , E _ { i } , L _ { g } \left[ m _ { i } ^ { ( l ) } \right] \right) _ { \Omega } } \end{array}\tag{30}
$$

We apply the transformation $L _ { g }$ to the $\mathcal { H } _ { \mathrm { s f p } } ^ { ( l ) }$ in (22):

$$
\begin{array} { r l } { \left. \hat { a } _ { p } ^ { [ s ] } \left( \hat { L } _ { q } \left[ \hat { Q } _ { s } ^ { [ s ] } \right] \right) - \hat { L } _ { q } \left[ P _ { s } ^ { [ s ] } \right] } \\ { + C \sum _ { s \in \mathcal { N } _ { s } ^ { [ s ] } } \delta _ { s } ^ { [ s ] } \left( L _ { s } \left[ m _ { s } ^ { [ q ] } \right] \right) \cdot \left( L _ { s } \left[ P _ { s } ^ { [ q ] } \right] - L _ { s } \left[ P _ { s } ^ { [ q ] } \right] \right) } \\ { = \displaystyle \phi _ { p } ^ { [ s ] } \left( \hat { Q } _ { s } ^ { [ s ] } \right) \cdot \lambda _ { s } \left[ P _ { s } ^ { [ q ] } \right] + C \sum _ { s \in \mathcal { N } _ { s } ^ { [ s ] } } \delta _ { n } ^ { [ s ] } \left( m _ { s } ^ { [ q ] } \right) } \\ { \cdot L _ { s } \left[ P _ { s } ^ { [ q ] } - P _ { s } ^ { [ q ] } \right] } \\ { = L _ { s } \left[ \phi _ { p } ^ { [ s ] } \left( \hat { Q } _ { s } ^ { [ s ] } \right) - P _ { s } ^ { [ q ] } \right) } \\ { \cdot \left( P _ { s } ^ { [ q ] } - P _ { s } ^ { [ q ] } \right) } \\ { \cdot \left( P _ { s } ^ { [ q ] } - P _ { s } ^ { [ q ] } \right) \right] } \\ { = L _ { s } \left[ P _ { s } ^ { [ q ] } \left( \hat { P } _ { s } ^ { [ q ] } \right) \right] . } \end{array}
$$

Therefore, we have (30) satisfied. Combining both conditions (29) and (30), the equivariant symmetry in $P _ { i } ^ { ( l ) }$ and the invariant symmetry in $Q _ { i } ^ { ( l ) }$ are inherited through SIM layers in SiGNN, and thus, (28) is satisfied. As the sufficient condition (28) is met, (27) holds and the equivariant symmetry of policy ÏSiGNN,i has been proved. -

The second claim regarding the SiGNN-based value network states as:

Proposition 2: The SiGNN-based value network $V =$ $\psi _ { \mathrm { S i G N N } } ( o , J ; \psi )$ =is invariantly symmetric under the rotation ( ; )transformation $L _ { g }$ , which satisfies:

$$
V = \psi _ { \mathrm { S i G N N } } \left( L _ { g } [ o ] , L _ { g } [ J ] ; \psi \right) .\tag{31}
$$

Proof: The all-one matrix J is a constant matrix which is invariant to $L _ { g } .$ . Also, Q is invariant. Thus,

$$
V = \psi _ { \mathrm { S i G N N } } ( L _ { g } [ o ] , L _ { g } [ J ] ; \psi ) = \psi _ { \mathrm { S i G N N } } ( L _ { g } [ P ] , Q , J ; \psi ) .
$$

Inside the value network ÏSiGNN, the SiGNN releases $L _ { g } [ P _ { i } ^ { ( L ) } ]$ [ ]via (24) and feeds it to (25) to calculate the hidden embedding $U _ { i }$ using ${ \cal L } _ { g } [ { \bf o } _ { i } ^ { \mathrm { v e l } ( L ) } ]$ in $L _ { g } [ P _ { i } ^ { ( L ) } ]$ . The hidden embedding $U _ { i }$ is invariant to $L _ { g }$ because:

$$
L _ { g } [ U _ { i } ] = \left\| L _ { g } [ \mathbf { o } _ { i } ^ { \mathrm { v e l } ( L ) } ] \right\| ^ { 2 } = \left\| \mathbf { o } _ { i } ^ { \mathrm { v e l } ( L ) } \right\| ^ { 2 } = U _ { i } .
$$

Note that the squared norm of a vector is equivalent to the relative squared distance between itself and the origin vector, which does not change with $L _ { g }$ . As a result, $L _ { g } [ U ] = U$ . Then,

$$
\begin{array} { r l } & { \psi _ { \mathrm { S i G N N } } ( L _ { g } [ P ] , Q , J ; \psi ) = \mathrm { F C } \left( \operatorname { t a n h } ( L _ { g } [ U ] , Q ) ; \psi _ { 2 } \right) } \\ & { ~ = \mathrm { F C } \left( \operatorname { t a n h } ( U , Q ) ; \psi _ { 2 } \right) = V . } \end{array}
$$

The proposition 2 has been proved.

## VI. EXPERIMENTS AND EVALUATION

This section presents the experiments conducted to evaluate the performance of the proposed SiGNN-based MARL method. Experimental results in comparison with baselines are discussed in detail. Supplementary is available at https://rongyeshi.github. io/SiGNNSupplementary.pdf.

## A. Experimental Settings

We implement a simulation environment using Python for the UAV swarm communication coverage task on a workstation equipped with 1 NVIDIA 4090 GPU, 1 Intel Core i9-12900KF @3.50 GHz CPU and Ubuntu 18.04 operating system. The control models are implemented and trained using PyTorch 1.3.0. We set the continuous target area as a 2D plane with $L _ { \mathrm { l e n g t h } } =$ $L _ { \mathrm { l e n g t h } } = 1 0 0$ =units. In each episode, 30 PoIs are sampled from = 100a mixture of three Gaussian distributions, whose means are uniformly generated from the target area. We employ the parametersharing technique to train a swarm with { , , , } UAVs 5 10 15 20in the training phase to examine the scalability. We consider both global and partial observation scenarios in the experiments, where the partial observation involves $R _ { \mathrm { o b s } } \in \{ 3 0 , 5 0 , 7 0 \}$ . The coverage radius is $R _ { \mathrm { c o v } } = 8$ . We set $e _ { 0 } , \beta _ { \mathrm { s p e e d } } , \beta _ { \mathrm { a c c } } = \{ 1 . 1 , 0 . 1$ 0.05}.

By default, the proposed symmetry-informed MARL integrates the SiGNN to the MAPPO framework. The implementation details are provided in Table II. Specifically, we train the models one million steps (i.e., 50,000 episodes). The CAE scores and expected accumulated rewards (joint returns) are calculated every 100 episodes, with 5 test rollouts. We also record their coverage, energy and overlap breakdowns to facilitate a comprehensive evaluation of the proposed methodâs performance and comparison with baseline methods.

TABLE II  
COEFFICIENTS AND HYPERPARAMETERS IN EXPERIMENTS
<table><tr><td>Coefficients and Hyperparameters</td><td>value</td></tr><tr><td>episodelength T</td><td>200</td></tr><tr><td> $\lambda ^ { \mathrm { c o v } } , \lambda _ { 1 } ^ { \mathrm { e g } } , \lambda _ { 2 } ^ { \mathrm { \check { e } g } } , \lambda ^ { \mathrm { o l } }$ </td><td>{15,0.05,0.1, 10}</td></tr><tr><td>total training steps</td><td>10,000,000</td></tr><tr><td>MLP hidden size</td><td>[128,128]</td></tr><tr><td>activation function</td><td>ReLU</td></tr><tr><td>discount factor </td><td>0.99</td></tr><tr><td>critic loss</td><td>huber loss</td></tr><tr><td>huber delta</td><td>10</td></tr><tr><td>optimizer</td><td>Adam</td></tr><tr><td>optimizer epsilon</td><td>1e-5</td></tr><tr><td>network initialization</td><td>orthogonal</td></tr><tr><td>number of SIM layers L</td><td>2</td></tr><tr><td>gradient clip parameter</td><td>0.2</td></tr><tr><td>actor/critic learning rate</td><td>0.0002</td></tr><tr><td>buffer length</td><td>2000</td></tr></table>

<!-- image-->  
Fig. 4. Visualization of the UAV positions and dynamics in the simulation.

Fig. 4 illustrates UAV positioning and dynamics in the 2D simulation for the communication coverage task with 5 UAVs. The left part shows the initial UAV positions, while the right part displays the UAVs moving to cover PoIs under a control policy. The UAV swarm aims to achieve a high CAE score in serving the PoIs.

## B. Learning-Based and Non-Learning-Based Baselines

We benchmark our SiGNN-based model against a range of baseline methods with classic and state-of-the-art network architectures, including:

1) GraphSAGE: GraphSAGE [60] is a straightforward yet robust graph neural network, extensively applied in tasks like social network analysis and traffic management using graph neural networks. It generates node embeddings by iteratively aggregating and transforming feature information from fixed-size local neighborhoods using trainable neural networks. Because the interactions between UAVs can be modeled as a graph, GraphSAGE is well-suited to swarm control tasks.

2) MLP: Multi-Layer Perceptrons (MLPs) are widely used in various standard algorithms within the MARL framework. The comparison with MLPs is intended to emphasize our benefits over traditional baseline algorithms.

3) RNN: Recurrent Neural Networks (RNNs) possess a structure that models temporal information and are widely employed in MARL to tackle problems of partial observability. We included RNNs in the comparisons to highlight the effectiveness of our method in scenarios with partial observations.

<!-- image-->  
(a) Global observation

<!-- image-->  
(bï¼Partial observation  
Fig. 5. Curves of expected episode rewards for global observation scenario and partial observation scenario.

4) ESP: A recent innovation, Exploitation of Symmetry Prior (ESP) method incorporates symmetry into the MARL training with soft regularization through data augmentation and specialized design of loss functions [48]. Our comparison with ESP aims to demonstrates the superior performance of our method.

Additionally, we also make comparison against three nonlearning baselines:

1) Random: The random policy controls each UAV to select an action randomly at each time step t.

2) MB-Greedy: The Model-Based Greedy (MB-Greedy) method attempts to identify the action that maximizes the reward $r _ { i } ^ { t }$ within all possible actions in the simulated environment. Because the simulator is required to calculate an action, it is a model-based method. Unlike the typical approach, we discretize the continuous action space of $[ - v _ { \operatorname* { m a x } } , v _ { \operatorname* { m a x } } ]$ into ten values for sampling.

3) MB-GA: Genetic Algorithm (GA) is employed to approximate the optimal joint action at at each timestep t that that maximizes the total return $\begin{array} { r } { \sum _ { t } ( \gamma ) ^ { t } r ( s ^ { t } , a ^ { t } ) } \end{array}$ . It iteratives ( ) ( )selection, crossover, and mutation on a population of candidate actions. This strategy also relies on a environment model and is model-based. Similar to MB-Greedy, we discretize the continuous action space.

## C. Convergence and Performance on Global Observation

The proposed symmetry-informed MARL integrates SiGNN as the core component. As a learning-based method, it is important to evaluate the convergence efficiency in the training phase. The expected episode reward is the direct metric to evaluate the training stability and convergence. We first discuss the global observation case, i.e., $R _ { \mathrm { { o b s } } } = 1 0 0$ The curves of = 100expected episode rewards are showed in Fig. 5(a).

From Fig. 5(a), it is observed that SiGNN exhibites a faster, superior and more stable convergence than other learning-based algorithms. Specifically, SiGNN achieves high rewards above 650 and stabilizes there after 0.4 million training steps. Other baselines need about 0.9 millon steps to stabilize at around the rewards 400â¼500.

Regardless of the superior performance of SiGNN in episode rewards, another concern arises from the fact that the reward function is adjusted from the metrics to decompose the individual influences of each UAV to enlarge the subtle difference among sub-optimal policies during training. Therefore, a high reward does not guarantee the performance with respect to CAE (coverage, anti-overlap, energy). Consequently, it is necessary to examine the performance in terms of CAE scores and corresponding component indexes.

<!-- image-->  
(a) CAE score curves

<!-- image-->  
(b) Coverage index curves

<!-- image-->  
(cï¼ Energy index curves

<!-- image-->  
(d) Anti-overlap index curves  
Fig. 6. The curves of CAE scores and corresponding indexes for scenario with global observation.

The experimental results are presented in Fig. 6. The CAE scores in Fig. 6(a) show that the SiGNN-based method significantly outperforms the baselines. Although there are slight changes in the final CAE scoresâ ranking, the overall curve trends are similar to the episode reward performance in Fig. 5(a) and the SiGNN-based method consistently and significantly outperforms the baselines. These findings confirm that the designed reward function positively correlates with the CAE score, and the distinction becomes more clear when using the reward metric (at a scale of 2). Among baselines, the ESP method leverages the symmetry prior in a soft constrained manner, achieving a better CAE score curve.

Fig. 6(b), (c), and (d) display the coverage, energy, and anti-overlap indexes, respectively, revealing more refined details in training. Specifically, regarding the coverage index, all methods incrementally learn to effectively serve the PoIs. The energy index of the curves consistently increases because of the energy consumption in an episode, and a flattened energy curve suggests that the UAVs maintain their positions without abrupt movements. The anti-overlap index curves exhibit an interesting pattern: At the beginning, the curves start from one as all UAVs are randomly distributed and no overlapping occurs. When the training takes effects, some methods tend to gather with each other and the anti-overlap index is negatively effected. Finally, as the UAVs are penalized by the overlapping, they learn to avoid redundant serving, and the index converges back to value one.

A closer look into the curves reveals that the GraphSAGE method performs well in coverage index and anti-overlap index due to its ability to effectively capture the spatial relationships among UAVs using graph-processing techniques. However, it fails to learn to hover while serving PoIs, leading to a deterioration in the energy index. The ESP, RNN, and MLP need to learn to recognize the environmental symmetry and then to avoid overlapping, which results in initial declining trends in the anti-overlap index during the early stages of training. In contrast, SiGNN quickly learns to provide communication coverage with greater energy efficiency. Although some initial overlap occurs during the initial stages of training, SiGNN adapts to avoid redundant coverage faster than baselines. This might be attributed to the fact that SiGNN does not need to learn symmetry, allowing itself to concentrate more on enhancing energy performance during training.

## D. Convergence and Performance on Partial Observation

Next, we turn to the more practical scenarios where each UAV can access to partial observation. We exemplify the discussion using $R _ { \mathrm { 0 b s } } = 5 0$ . Scenarios with other radii exhibit similar pat-= 50terns, which are shown in supplementary Section I.

As shown in Fig. 5(b), under the partial observation, the GraphSAGE method performs the worst (i.e., the lowest reward and largest variance) among the baselines, probably because it adheres to local information processing and fails to learn cooperative behaviors. This disadvantage might be mitigated by using multi-hop techniques. The RNN method benefits more from the setting, because it is able to process sequential and temporal observation effectively, integrating temporal context and past events in memory to learn the symmetry property to coordinate the UAV swarm. The SiGNN-based method still maintains the highest training efficiency, demonstrating its ability to overcome the disadvantage of local observation. Compared with the global scenario in Fig. 5(a), the partial observation setting presents challenges to cooperation, resulting in relatively spiky learning curves and generally lower rewards.

Similar trends are also displayed in CAE scores and corresponding indexes in Fig. 7, where by limiting the observable information, the overall CAE scores reduce, and the index curves are generally noisy. The GraphSAGEâs performance deteriorates more sharply compared to other baseline models. The proposed SiGNN-based method continues to excel in terms of CAE score and the three indexes.

In both global and partial observation settings shown in Fig. 5(a) and (b), by integrating the rotation symmetry into the value/policy networksâ structure, the SiGNN-based method presents significantly improved efficiency compared to those without using symmetry-preserving networks (e.g., MLP, RNN). And this echoes the fact that, thanks to the symmetry-preserving networks, there is no need for additional trial-and-error to learn the symmetry property within the symmetric Dec-POMDP, resulting in notably higher training efficiency.

<!-- image-->  
(a) CAE score curves

<!-- image-->  
(b) Coverage index curves

<!-- image-->  
(c) Energy index curves

<!-- image-->  
(d) Anti-overlap index curves  
Fig. 7. The curves of CAE scores and corresponding indexes for scenario with partial observation.

TABLE III  
THE METRIC PERFORMANCE OF NON-LEARNING AND LEARNING-BASED METHODS
<table><tr><td>Policy model</td><td> $\overline { { \mathrm { ~ C A E ~ S c o r e } } }$ </td><td> $\overline { { \mathrm { C o v e r a g e ~ I n d e x } } }$ </td><td> $\overline { { \mathrm { E n e r g y ~ I n d e x } } }$ </td><td> $\overline { { \mathrm { A n t i - O v e r l a p ~ I n d e x } } }$ </td></tr><tr><td>Random</td><td> $\overline { { 0 . 1 9 6 7 \pm 0 . 1 8 5 3 } }$ </td><td> $\overline { { 0 . 1 5 6 0 \pm 0 . 1 4 3 3 } }$ </td><td> $\overline { { 0 . 7 1 5 2 \pm 0 . 1 2 4 8 } }$ </td><td> $\overline { { 0 . 8 5 1 1 \pm 0 . 1 1 3 3 } }$ </td></tr><tr><td>MB-Greedy</td><td> $0 . 3 4 2 6 \pm 0 . 2 2 3 8$ </td><td> $0 . 1 8 3 6 \pm 0 . 0 5 4 8$ </td><td> $\mathbf { 0 . 4 9 5 6 \pm 0 . 0 8 7 3 }$ </td><td> $0 . 9 2 4 7 \pm 0 . 0 3 4 4$ </td></tr><tr><td>MB-GA</td><td> $0 . 5 4 7 5 \pm 0 . 1 6 7 3$ </td><td> $0 . 3 3 2 9 \pm 0 . 0 7 3 2$ </td><td> $0 . 5 7 8 4 \pm 0 . 0 6 2 4$ </td><td> $0 . 9 5 1 3 \pm 0 . 0 2 3 3$ </td></tr><tr><td>GraphSAGE</td><td> $0 . 4 3 7 9 \pm 0 . 0 8 9 3$ </td><td> $0 . 4 0 6 5 \pm 0 . 0 5 3 7$ </td><td> $0 . 9 3 8 7 \pm 0 . 0 6 4 5$ </td><td> $0 . 9 9 8 5 \pm 0 . 0 0 1 5$ </td></tr><tr><td>MLP</td><td> $0 . 6 3 1 3 \pm 0 . 0 9 3 6$ </td><td> $0 . 4 3 0 4 \pm 0 . 0 7 5 2$ </td><td> $0 . 6 3 8 2 \pm 0 . 0 0 8 4$ </td><td> $0 . 9 4 2 0 \pm 0 . 0 6 7 3$ </td></tr><tr><td>RNN</td><td> $0 . 7 0 1 7 \pm 0 . 0 8 1 0$ </td><td> $0 . 4 5 2 9 \pm 0 . 0 5 2 8$ </td><td> $0 . 6 2 0 8 \pm 0 . 0 0 4 7$ </td><td> $0 . 9 6 3 5 \pm 0 . 0 5 2 8$ </td></tr><tr><td>ESP</td><td> $0 . 6 6 6 3 \pm 0 . 0 4 7 1$ </td><td> $0 . 4 4 3 9 \pm 0 . 0 1 4 2$ </td><td> $0 . 6 3 7 3 \pm 0 . 0 0 5 3$ </td><td> $0 . 9 5 7 2 \pm 0 . 0 6 9 1$ </td></tr><tr><td>SiGNN</td><td> $\mathbf { 0 . 9 3 1 3 \pm 0 . 0 3 7 6 }$ </td><td> $\mathbf { 0 . 5 6 5 5 \pm 0 . 0 1 0 9 }$ </td><td> $0 . 6 0 7 8 \pm 0 . 0 1 8 1$ </td><td> $\mathbf { 1 . 0 0 0 0 } \pm \mathbf { 0 . 0 0 0 0 }$ </td></tr></table>

The best model is indicated by bold.More results are available in supplementary Sec II.

## E. Learning-Based Versus Non-Learning-Based Approaches

We compare the learning-based and non-learning-based approaches under the partial observation setting. The learningbased approaches are trained through 1 million steps. Each method are measured using 10 test episodes and we use Table III to display the CAE scores and the three indexes.

The Random method selects actions arbitrarily, resulting in highly unstable performance characterized by large variance and the poorest metric scores. The MB-Greedy exploits the simulator to determine the one-step action with maximal immediate reward. However, it fails to fully capture the cooperative relationships among UAVs which involves planning in multiple steps, the final performance of MB-greedy is limited. The MB-GA method demonstrates clear advantages over the other two traditional methods. It leverages genetic evolution heuristics to find near-optimal joint actions, performing well with CAE scores around 0.5. The two model-based methods give the best energy performance, probably because they tend to stay still after reaching one of the the PoIs. However, it struggles to achieve global optimality and the computation load is high, preventing it from real-time application.

<!-- image-->  
Fig. 8. Percentage Improvements over MB-Greedy Baseline.

The learning-based methods generally perform better than the non-learning-based baselines (generally with CAE scores $> 0 . 5 )$ . They can conduct trial-and-errors to model the envi-0 5ronment and learn to cooperate among UAVs, achieving more comprehensive and efficient strategy. Remarkably, the SiGNNbased method consistently presents higher and more stable performance in the CAE score and most indexes, underscoring the crucial role that the symmetry-informed network structure plays in learning optimal policies. Its energy performance is also the best among learning-based methods.

To highlight the advantages of the SiGNN-based method, we employ a histogram (see Fig. 8) to illustrate the percentage improvements in CAE scores with respect to the MB-Greedy baseline. In this representation, blue rectangles indicate the average improvements and black lines depict the variances. It is observable that, except for the Random algorithm, all tested algorithms exhibit improvements in performance compared to the MB-Greedy algorithm. Particularly notable is the SiGNN-based method, which not only achieves the highest improvement but also demonstrates consistent superior performance, highlighting the robustness of the algorithm.

## F. Sensitivity to Different Hyperparameters

We study the sensitivity of the SiGNN-based method to different hyperparameters, including the MLP hidden size, learning rate, and the number of SiGNN layers L.

For the MLP hidden size, shown in Fig. 9(a), reducing the size to 1/4 of the default configuration (i.e., [32, 32]) results in a slower learning curve, implying that an overly simplified model may experience reduced performance. Increasing the size to 4 times (i.e., [512,512]) does not bring significant performance improvement compared to the default size.

As shown in Fig. 9(b), the learning rate lr plays an important role in achieving high training efficiency and overall performance. The curve with an overly small learning rate (lr =0.00002) grows steadily but stabilizes at a lower reward level, whereas the curve with an overly large learning rate $( l r = 0 . 0 0 2 )$

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
Fig. 9. Left: Performance under different hyperparameters, including (a) MLP hidden size, (b) learning rate, (c) SiGNN layer number. Right: (d) Comparison between rotational data augmentation-based methods and SiGNN-based method.

exhibits faster initial progress but fails to achieve high reward levels, indicating a deteriorated convergence.

Finally, as shown in Fig. 9(c), a significant improvement in training efficiency and performance is achieved by introducing Symmetry-Informed Module with $L = 1 ,$ , compared to the L 0 configuration (correspond to the standard MAPPO). Further increasing L to 2 does not yield significant performance improvements; however, a smoother learning curve is observed, suggesting that additional SiGNN layers may enhance the symmetry property and the training stability.

## G. Rotational Data Augmentation Versus SiGNN

Rotational symmetry is considered a basis of data augmentation in reinforcement learning, which can expand the original small amount of data. In Fig. 9(d), we compare the performance of data augmentation-based methods with the SiGNNbased method. Specifically, the ESP method proposed in [48] integrates rotational symmetry-based data augmentation into a backbone model (i.e., MLP) to enhance performance. To provide a more comprehensive analysis, we also apply the data augmentation technique to the GraphSAGE method, forming the ESP-GraphSAGE baseline for comparison.

Experimental results indicate that both the ESP and ESP-GraphSAGE methods consistently outperform their respective backbone models, MLP and GraphSAGE. This improvement is attributed to the data augmentation technique, which provides additional trial-and-error samples to learn the symmetry property in the UAV swarm environment, thereby enhancing traditional schemes. In contrast, the SiGNN method significantly outperforms the data augmentation-based approaches. This superiority stems from the intrinsic embedding of symmetry within the network structure, eliminating the need for additional trialand-error processes to learn the symmetry property, and ultimately resulting in superior training efficiency.

## H. Robustness Against Communication Drop

This subsection examines the robustness of SiGNN in scenarios where communication connections and information sharing among UAVs may fail with different probabilities.

In real world, besides partial observability, we should realize that various factors can disrupt communication among UAVs and it is more practical to assume that information sharing could be interrupted with a dropping probability p. In this experiment, we set $p = \{ 0 , 0 . 2 , 0 . 4 , . . . , 1 . 0 \}$ and test the CAE performance of = 0 0 2 0 4SiGNN and baselines.

<!-- image-->

<!-- image-->

<!-- image-->  
Fig. 10. CAE scores under different dropping rates, PoI numbers, and episode lengths.

The experimental results are showed in Fig. 10(a), from which we observe a consistent decline in CAE with increasing drop rates, indicating that reduced connectivity and information sharing adversely affect inter-UAV cooperation. An interesting phenomenon is that all the learning-based methods are still able to effectively perform coverage tasks even under $p = 1$ (i.e., no information sharing among UAVs), reaching a proper CAE above 0.5 (except for GraphSAGE).

Although the performance of the SiGNN-based method significantly deteriorates as p increases to 0.2, it stabilizes thereafter and consistently outperforms all other learning-based methods, demonstrating the robustness of the proposed SiGNN. Our insight into this phenomenon is that the communication between UAVs is inherently symmetric. Consequently, the information missing from some adjacent UAVs can be compensated and inferred from other connectable UAVs.

## I. Performance Under Different PoIs and Episode Lengths

For further evaluation, the proposed SiGNN-based method is tested under different numbers of PoIs and episode lengths. With 5 UAVs, the number of PoIs is increased from 20 to 50. As shown in Fig. 10(b) , the CAE scores generally show an upward trend as the number of PoIs increases. This is because a higher density of PoIs makes it more convenient for UAVs to locate and serve users. However, the CAE scores begin to flatten between 40 and

TABLE IV  
SCALABILITY PERFORMANCE UNDER PARTIAL OBSERVATION
<table><tr><td>Number</td><td>Steps</td><td>SiGNN</td><td>MLP</td><td>RNN</td><td>ESP</td><td> $\overline { { \mathrm { G r a p h S A G E } } }$ </td></tr><tr><td rowspan="2">5</td><td>300k</td><td> $\mathbf { 6 1 9 . 7 6 \pm 2 6 . 4 3 }$ </td><td> $\overline { { 2 8 6 . 2 2 \pm 3 2 . 6 0 } }$ </td><td> $\overline { { 3 3 1 . 6 8 \pm 4 4 . 2 1 } }$ </td><td> $\overline { { 1 9 8 . 5 9 \pm 2 9 . 3 0 } }$ </td><td> $2 8 8 . 2 4 \pm 3 8 . 5 0$ </td></tr><tr><td>1000k</td><td> ${ \bf 6 4 9 . 6 1 \pm 2 6 . 1 1 }$ </td><td> $4 8 9 . 3 8 \pm 5 2 . 2 4$ </td><td> $5 1 7 . 6 8 \pm 2 9 . 9 0$ </td><td> $5 0 1 . 3 4 \pm 3 4 . 1 4$ </td><td> $3 6 4 . 6 9 \pm 5 4 . 2 4$ </td></tr><tr><td rowspan="2">10</td><td>300k</td><td> $\mathbf { 3 7 8 . 0 6 \pm 2 3 . 4 5 }$ </td><td> $3 9 . 8 4 \pm 3 8 . 2 6$ </td><td> $\overline { { 5 3 . 4 1 \pm 3 8 . 8 9 } }$ </td><td> $- 6 . 6 2 \pm 5 1 . 9 2$ </td><td> $- 6 . 5 7 \pm 5 4 . 1 4$ </td></tr><tr><td>1000k</td><td> ${ \bf 4 6 2 . 5 9 \pm 3 3 . 4 2 }$ </td><td> $7 5 . 7 1 \pm 5 5 . 9 6$ </td><td> $9 0 . 7 7 \pm 4 9 . 1 7$ </td><td> $8 3 . 4 7 \pm 4 8 . 5 3$ </td><td> $- 2 3 5 . 1 7 \pm 7 8 . 4 2$ </td></tr><tr><td rowspan="2">15</td><td>300k</td><td> $\mathbf { 2 3 5 . 3 1 \pm 3 1 . 5 0 }$ </td><td> $- 2 0 2 . 6 6 \pm 4 1 . 6 8$ </td><td> $- 2 1 4 . 5 5 \pm 4 4 . 5 0$ </td><td> $- 1 0 4 . 3 9 \pm 6 7 . 4 3$ </td><td> $- 1 4 4 . 9 5 \pm 8 7 . 3 1$ </td></tr><tr><td>1000k</td><td> $\mathbf { 2 2 6 . 8 3 \pm 4 1 . 2 2 }$ </td><td> $- 5 8 . 4 4 \pm 6 0 . 1 3$ </td><td> $4 3 . 0 1 \pm 6 9 . 5 5$ </td><td> $5 5 . 6 8 \pm 4 1 . 7 7$ </td><td> $- 5 2 6 . 7 3 \pm 9 3 . 4 7$ </td></tr><tr><td rowspan="2">20</td><td>300k</td><td> $\mathbf { 5 0 . 6 8 \pm 3 7 . 3 2 }$ </td><td> $- 3 2 2 . 4 6 \pm 8 4 . 6 1$ </td><td> $- 3 3 6 . 5 9 \pm 5 2 . 3 6$ </td><td> $- 4 2 6 . 2 5 \pm 7 6 . 1 5$ </td><td> $- 5 5 8 . 1 8 \pm 9 5 . 1 2$ </td></tr><tr><td>1000k</td><td> $\mathbf { 1 2 2 . 1 4 \pm 5 7 . 2 1 }$ </td><td> $- 3 7 8 . 8 2 \pm 7 6 . 3 2$ </td><td> $- 7 8 . 1 4 \pm 8 2 . 2 3$ </td><td> $- 1 1 8 . 5 4 \pm 4 5 . 5 0$ </td><td> $- 9 4 3 . 2 3 { \pm } 1 5 4 . 3 3$ </td></tr></table>

50 PoIs, indicating that the UAV swarmâs coverage capacity may reach its limit due to the finite number of UAVs available.

A similar phenomenon can be observed as the episode length increases from 150 to 300, shown in Fig. 10(c). With short episode lengths (e.g., T  150), the UAV swarm is still in =the process of locating the PoIs, preventing efficient coverage. As the episode length increases, the policy has more time to coordinate the UAVs and maximize coverage. Eventually, the CAE scores plateau, as further improvements cannot be achieved simply by extending the episode time.

## J. Scalability

INFERENCE TIME ON EDGE COMPUTING DEVICES

TABLE V

This experiment was conducted to verify the scalability of various methods. The scalability refers to the ability of an algorithm to maintain high performance when the number of UAVs is increased.

## K. Computational Overhead on Edge Computing Devices

In the simulation environment, we keep 30 PoIs constant and gradually increase the number of UAVs from 5 to 20. The performance of each method was evaluated in two phases of training: early stage at 300 k and later stage at 1000 k. This setup allows a comprehensive understanding of how SiGNN and other baseline methods perform under different training stages and scale conditions. Here, to make the the performance difference more visible, we choose the expected episode reward as the metric for comparison. The results are presented in Table IV.

<table><tr><td>Policy</td><td>Mean (s)</td><td>STD (s)</td><td>FPS</td></tr><tr><td>SiGNN_global</td><td>0.0243</td><td>0.0002</td><td>41</td></tr><tr><td>SiGNN_local</td><td>0.0239</td><td>0.0012</td><td>42</td></tr><tr><td>MLP_global</td><td>0.0125</td><td>0.0138</td><td>79</td></tr><tr><td>MLP_local</td><td>0.0144</td><td>0.0152</td><td>69</td></tr><tr><td>RNN_global</td><td>0.0227</td><td>0.0113</td><td>37</td></tr><tr><td>RNN_local</td><td>0.0231</td><td>0.0098</td><td>43</td></tr><tr><td>ESP_global</td><td>0.0138</td><td>0.0018</td><td>72</td></tr><tr><td>ESP_local</td><td>0.0151</td><td>0.0023</td><td>66</td></tr><tr><td>GraphSAGE_global</td><td>0.0279</td><td>0.0213</td><td>36</td></tr><tr><td>GraphSAGE_local</td><td>0.0286</td><td>0.0185</td><td>35</td></tr></table>

All the methods show a trend of decreasing performance as the number of UAVs increases. For example, the MLP method significantly drops from 286 to -378. Despite the increased complexity and instability of larger swarms, the SiGNN-based method generalizes well and consistently achieves significantly higher reward values across various numbers of UAVs. In the task with 20 UAVs, the performance of all baseline models dropped to negative rewards, while SiGNN is the only model that consistently maintains its performance above 100. These results demonstrate the scalability advantages of the proposed method. More results are available in supplementary Section III.

In communication coverage tasks, MARL-based methods are used to control UAVs in a distributed manner. These methods involve expressing the communication protocols among UAVs through neural networks, which may require more computational resources than traditional RL. Such a requirement for increased resources brings up concerns regarding computational efficiency.

To demonstrate the practicality of our method on mobile computing devices, we implemented all the learning-based UAV swarm control models on the Jetson Nano, a device frequently utilized for controlling autonomous UAVs [61]. We evaluate their real-time performance on this platform to evaluate their real-world applicability. Each model executed 1000 steps to compute the average of inference times. The experimental results are displayed in Table V, including the inference times and frames per second (FPS) of different policy models on the Jetson Nano board. These experimental results reflect the real-time performance and computational complexity among different methods.

It is observed that the inference times of SiGNN-based series are very close across different observation distances, averaging between 0.0239 s and 0.0243 s, with a stable FPS of 41â¼42. The changes in local observation distance have little impact on inference time, indicating that observation distance is not the main bottleneck in the inference process. The SiGNN-based methods maintains high real-time performance, making it suitable for real-time UAV controlling tasks.

## VII. CONCLUSION AND FUTURE WORK

This paper presents symmetry-informed MARL, leveraging a novel symmetry-informed graph neural network (SiGNN) as the policy and value networks. SiGNN embeds the inherent symmetry of multi-UAV systems into its structure, improving training efficiency for managing large swarms with continuous control. It includes an adjacency processing module to accommodate varying numbers of adjacent UAVs in partial observations. Theoretical analysis confirms that SiGNN preserves symmetry properties, ensuring the methodâs effectiveness. Simulation experiments for communication coverage show that SiGNN-based MARL surpasses advanced baselines in sample efficiency, scalability, and robustness.

In the future, we plan to extend the SiGNN-based framework to encompass a broader type of symmetry to handle more scenarios, such as swarms with heterogeneous UAVs and consider other types of multi-agent systems, such as combining UAVs with autonomous ground vehicles and robotic swarms for the communication coverage, disaster rescue and asteroid exploration tasks. Real-world testing and deployment of SiGNNbased method will be essential to validate its effectiveness outside of simulated environments and to ensure its practical utility in operational settings. Finally, how to properly share PoI information among UAVs to enhance performance while balancing computational and communication overhead is a promising topic for future research.

## ACKNOWLEDGMENT

The author would like to thank Professor JosÃ© M. F. Moura and Professor Peter Steenkiste from Carnegie Mellon University for providing valuable comments. Thank Gangzheng Ai for his contributions to the preparation and revision of this paper.

## REFERENCES

[1] P. Cao et al., âComputational intelligence algorithms for UAV swarm networking and collaboration: A comprehensive survey and future directions,â IEEE Commun. Surv. Tut., vol. 26, no. 4, pp. 2684â2728, Fourth Quarter 2024.

[2] G. Geraci et al., âWhat will the future of UAV cellular communications be? A flight from 5G to 6G,â IEEE Commun. Surv. Tut., vol. 24, no. 3, pp. 1304â1335, Third Quarter 2022.

[3] J. Ren, Y. Xu, Z. Li, C. Hong, X.-P. Zhang, and X. Chen, âScheduling uav swarm with attention-based graph reinforcement learning for ground-to-air heterogeneous data communication,â in Proc. 2023 ACM Int. Joint Conf. Pervasive Ubiquitous Comput.-2023 ACM Int. Symp. Wearable Comput., 2023, pp. 670â675.

[4] X. Chen et al., âDesign experiences in minimalistic flying sensor node platform through sensorfly,â ACM Trans. Sensor Netw., vol. 13, no. 4, pp. 1â37, 2017.

[5] H. Wang et al., âTransformLoc: Transforming MAVs into mobile localization infrastructures in heterogeneous swarms,â 2024, arXiv: 2403.08815.

[6] Q. Shen et al., âFair communications in UAV networks for rescue applications,â IEEE Internet Things J., vol. 10, no. 23, pp. 21013â21025, Dec. 2023.

[7] J. Agrawal, M. Kapoor, and R. Tomar, âA novel unmanned aerial vehiclesink enabled mobility model for military operations in sparse flying ad-hoc network,â Trans. Emerg. Telecommun. Technol., vol. 33, no. 4, pp. 1â23, 2021.

[8] Z. Zhao et al., âPredictive UAV base station deployment and service offloading with distributed edge learning,â IEEE Trans. Netw. Service Manag., vol. 18, no. 4, pp. 3955â3972, Dec. 2021.

[9] L. Yin, N. Zhang, and C. Tang, âOn-demand UAV base station deployment for wireless service of crowded tourism areas,â Pers. Ubiquitous Comput., vol. 26, no. 4, pp. 1137â1149, 2022.

[10] H. Jafaripour, M. Fathi, and A. Shariatpanah, âCommunication coverage maximization in stadium environments using UAVs,â TeleCommun. Syst., vol. 86, pp. 691â703, 2024.

[11] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âEfficient deployment of multiple unmanned aerial vehicles for optimal wireless coverage,â IEEE Commun. Lett., vol. 20, no. 8, pp. 1647â1650, Aug. 2016.

[12] C. Zhang, L. Zhang, L. Zhu, T. Zhang, Z. Xiao, and X.-G. Xia, â3D deployment of multiple UAV-mounted base stations for UAV communications,â IEEE Trans. Commun., vol. 69, no. 4, pp. 2473â2488, Apr. 2021.

[13] A. M. Said, M. Marot, C. Boucetta, H. Afifi, H. Moungla, and G. Roujanski, âReinforcement learning versus rule-based dynamic movement strategies in UAV assisted networks,â Veh. Commun., vol. 48, pp. 1â17, 2024.

[14] C. H. Liu, Z. Chen, J. Tang, J. Xu, and C. Piao, âEnergy-efficient UAV control for effective and fair communication coverage: A deep reinforcement learning approach,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 2059â2070, Sep. 2018.

[15] C. H. Liu, X. Ma, X. Gao, and J. Tang, âDistributed energy-efficient multi-UAV navigation for long-term communication coverage by deep reinforcement learning,â IEEE Trans. Mobile Comput., vol. 19, no. 6, pp. 1274â1285, Jun. 2020.

[16] D. Chen, Q. Qi, Z. Zhuang, J. Wang, J. Liao, and Z. Han, âMean field deep reinforcement learning for fair and efficient UAV control,â IEEE Internet Things J., vol. 8, no. 2, pp. 813â828, Jan. 2021.

[17] Z. Ye, K. Wang, Y. Chen, X. Jiang, and G. Song, âMulti-UAV navigation for partially observable communication coverage by graph reinforcement learning,â IEEE Trans. Mobile Comput., vol. 22, no. 7, pp. 4056â4069, Jul. 2023.

[18] D. Chen, Q. Qi, Q. Fu, J. Wang, J. Liao, and Z. Han, âTransformerbased reinforcement learning for scalable multi-UAV area coverage,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 8, pp. 10062â10077, Aug. 2024.

[19] X. Luo, J. Xie, L. Xiong, Z. Wang, and Y. Liu, âUAV-assisted fair communications for multi-pair users: A multi-agent deep reinforcement learning method,â Comput. Netw., vol. 242, 2024, Art. no. 110277.

[20] G. E. Karniadakis, I. G. Kevrekidis, L. Lu, P. Perdikaris, S. Wang, and L. Yang, âPhysics-informed machine learning,â Nat. Rev. Phys., vol. 3, no. 6, pp. 422â440, 2021.

[21] X. Chen et al., âDDL: Empowering delivery drones with large-scale urban sensing capability,â IEEE J. Sel. Topics Signal Process., vol. 18, no. 3, pp. 502â515, Apr. 2024.

[22] X. Chen et al., âDeliversense: Efficient delivery drone scheduling for crowdsensing with deep reinforcement learning,â in Proc. 2022 ACM Int. Joint Conf. Pervasive Ubiquitous Comput.-2022 ACM Int. Symp. Wearable Comput., 2023, pp. 403â408.

[23] X. Chen et al., âSOScheduler: Toward proactive and adaptive wildfire suppression via multi-UAV collaborative scheduling,â IEEE Internet Things J., vol. 11, no. 14, pp. 24858â24871, Jul. 2024.

[24] H. Wang, X. Chen, Y. Cheng, C. Wu, F. Dang, and X. Chen, âH-SwarmLoc: Efficient scheduling for localization of heterogeneous MAV swarm with deep reinforcement learning,â in Proc. 20th ACM Conf. Embedded Netw. Sensor Syst., 2023, pp. 1148â1154.

[25] X. Chen, A. Purohit, C. R. Dominguez, S. Carpin, and P. Zhang, âDrunk-Walk: Collaborative and adaptive planning for navigation of micro-aerial sensor swarms,â in Proc. 13th ACM Conf. Embedded Netw. Sensor Syst., 2015, pp. 295â308.

[26] X. Chen et al., âH-DrunkWalk: Collaborative and adaptive navigation for heterogeneous mav swarm,â ACM Trans. Sen. Netw., vol. 16, no. 2, pp. 1â27, 2020.

[27] C.-C. Hsia, Y. Xu, J. Ren, and X. Chen, âDemo abstract: CARL: Collaborative altitude-adaptive reinforcement learning for active search with UAV swarms,â in Proc. 23rd ACM/IEEE Int. Conf. Inf. Process. Sensor Netw., 2024, pp. 249â250.

[28] Y. Cheng, X. Chen, Y. Yang, H. Wang, Y. Liu, and X. Chen, âPoster: Olfactory sensing in turbulent airflow via collaborative robots,â in Proc. 25th Int. Workshop Mobile Comput. Syst. Appl., 2024, pp. 135â135.

[29] R. Shakeri et al., âDesign challenges of multi-UAV systems in cyberphysical applications: A comprehensive survey and future directions,â IEEE Commun. Surv. Tut., vol. 21, no. 4, pp. 3340â3385, Fourth Quarter 2019.

[30] B. Hu, Z. Sun, H. Hong, and J. Liu, âUAV-aided networks with optimization allocation via artificial bee colony with intellective search,â EURASIP J. Wirel. Commun. Netw., vol. 2020, pp. 1â17, 2020.

[31] J. Lyu, Y. Zeng, R. Zhang, and T. J. Lim, âPlacement optimization of UAV-mounted mobile base stations,â IEEE Commun. Lett., vol. 21, no. 3, pp. 604â607, Mar. 2017.

[32] Z. Li, F. Man, X. Chen, B. Zhao, C. Wu, and X. Chen, âTract: Towards large-scale crowdsensing with high-efficiency swarm path planning,â in Proc. 2022 ACM Int. Joint Conf. Pervasive Ubiquitous Comput.-ACM Int. Symp. Wearable Comput., 2023, pp. 409â414.

[33] Y. Chen, N. Li, C. Wang, W. Xie, and J. Xv, âA 3D placement of unmanned aerial vehicle base station based on multi-population genetic algorithm for maximizing users with different QoS requirements,â in Proc. IEEE 18th Int. Conf. Commun. Technol., 2018, pp. 967â972.

[34] H. S. Munawar, A. W. Hammad, and S. T. Waller, âDisaster region coverage using drones: Maximum area coverage and minimum resource utilisation,â Drones, vol. 6, no. 4, pp. 1â28, 2022.

[35] , âImproved multi-objective particle swarm optimization algorithm based on area division with application in multi-UAV task assignment,â IEEE Access, vol. 11, pp. 123519â123530, 2023.

[36] X. Chen et al., âPAS: Prediction-based actuation system for city-scale ridesharing vehicular mobile crowdsensing,â IEEE Internet Things J., vol. 7, no. 5, pp. 3719â3734, May 2020.

[37] S. Xu, X. Chen, X. Pi, C. Joe-Wong, P. Zhang, and H. Y. Noh, âiLOCuS: Incentivizing vehicle mobility to optimize sensing distribution in crowd sensing,â IEEE Trans. Mobile Comput., vol. 19, no. 8, pp. 1831â1847, Aug. 2020.

[38] J. Qin, Z. Wei, C. Qiu, and Z. Feng, âEdge-prior placement algorithm for UAV-mounted base stations,â in Proc. IEEE Wirel. Commun. Netw. Conf., 2019, pp. 1â6.

[39] W. Xu et al., âThroughput maximization of UAV networks,â IEEE/ACM Trans. Netw., vol. 30, no. 2, pp. 881â895, Apr. 2022.

[40] S. Li et al., âCoverage maximization of heterogeneous UAV networks,â in Proc. IEEE 43rd Int. Conf. Distrib. Comput. Syst., 2023, pp. 120â130.

[41] R. Lowe, Y. I. Wu, A. Tamar, J. Harb, P. Abbeel, and I. Mordatch, âMultiagent actor-critic for mixed cooperative-competitive environments,â in Proc. 31st Conf. Neural Inf. Process. Syst., 2017, pp. 120â130.

[42] I. A. Nemer, T. R. Sheltami, S. Belhaiza, and A. S. Mahmoud, âEnergyefficient UAV movement control for fair communication coverage: A deep reinforcement learning approach,â Sensors, vol. 22, no. 5, pp. 1â27, 2022.

[43] H. He, F. Zhou, Y. Zhao, W. Li, and L. Feng, âHypergraph convolution mix DDPG for multi-aerial base station deployment,â J. Cloud Comput., vol. 12, no. 3, pp. 1â11, 2023.

[44] J. Liu, H. Luo, R. Ruby, H. Wang, H. Tao, and K. Wu, âUAV-based reliable optical wireless communication via cooperative multi-agent reinforcement learning approach,â in Proc. IEEE 29th Int. Conf. Parallel Distrib. Syst., 2023, pp. 856â863.

[45] Y. Xu, Z. Jian, J. Zha, and X. Chen, âEmergency networking using UAVs: A reinforcement learning approach with large language model,â in Proc. 23rd ACM/IEEE Int. Conf. Inf. Process. Sensor Netw., 2024, pp. 281â282.

[46] D. Yarats, A. Zhang, I. Kostrikov, B. Amos, J. Pineau, and R. Fergus, âImproving sample efficiency in model-free reinforcement learning from images,â in Proc. 35th AAAI Conf. Artif. Intell., 2021, pp. 10674â10681.

[47] E. van der Pol, H. van Hoof, F. A. Oliehoek, and M. Welling, âMulti-agent MDP homomorphic networks,â in Proc. 10th Int. Conf. Learn. Representations, 2022, pp. 1â19.

[48] X. Yu, R. Shi, P. Feng, Y. Tian, J. Luo, and W. Wu, âESP: Exploiting symmetry prior for multi-agent reinforcement learning,â in Proc. 26th Eur. Conf. Artif. Intell., 2023, pp. 2946â2953.

[49] X. Yu et al., âLeveraging partial symmetry for multi-agent reinforcement learning,â in Proc. 38th AAAI Conf. Artif. Intell., 2024, pp. 17583â17590.

[50] R. Shi, Z. Mo, K. Huang, X. Di, and Q. Du, âA physics-informed deep learning paradigm for traffic state and fundamental diagram estimation,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 11688â11698, Aug. 2022.

[51] R. Shi, Z. Mo, and X. Di, âPhysics-informed deep learning for traffic state estimation: A hybrid paradigm informed by second-order traffic models,â in Proc. 35th AAAI Conf. Artif. Intell., 2021, pp. 540â547.

[52] M. Rasht-Behesht, C. Huber, K. Shukla, and G. E. Karniadakis, âPhysicsinformed neural networks (PINNs) for wave propagation and full waveform inversions,â J. Geophysical Res., Solid Earth, vol. 127, no. 5, pp. 1â21, 2022.

[53] S. Cai, C. Gray, and G. E. Karniadakis, âPhysics-informed neural networks enhanced particle tracking velocimetry: An example for turbulent jet flow,â IEEE Trans. Instrum. Meas., vol. 73, 2024, Art. no. 2519109.

[54] V. G. Satorras, E. Hoogeboom, and M. Welling, âE(n) equivariant graph neural networks,â in Proc. 38th Int. Conf. Mach. Learn., 2021, pp. 9323â9332.

[55] Z. Ye, Y. Chen, X. Jiang, G. Song, B. Yang, and S. Fan, âImproving sample efficiency in multi-agent actor-critic methods,â Appl. Intell., vol. 52, pp. 3691â3704, 2022.

[56] H. A. O. Jianye et al., âBoosting multiagent reinforcement learning via permutation invariant and permutation equivariant networks,â in Proc. 11th Int. Conf. Learn. Representations, 2023, pp. 1â18.

[57] X. Zhou, J. Xiong, H. Zhao, C. Yan, and J. Wei, âSymmetry-augmented multi-agent reinforcement learning for scalable UAV trajectory design and user scheduling,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 14127â14144, Dec. 2024.

[58] R. Alyassi, M. Khonji, A. Karapetyan, S. C.-K. Chau, K. Elbassioni, and C.-M. Tseng, âAutonomous recharging and flight mission planning for battery-operated autonomous drones,â IEEE Trans. Autom. Sci. Eng., vol. 20, no. 2, pp. 1034â1046, Apr. 2023.

[59] C. Yu et al., âThe surprising effectiveness of PPO in cooperative multiagent games,â in Proc. 36th Annu. Conf. Neural Inf. Process. Syst., 2022, pp. 1â14.

[60] W. L. Hamilton, Z. Ying, and J. Leskovec, âInductive representation learning on large graphs,â in Proc. 31st Annu. Conf. Neural Inf. Process. Syst., 2017, pp. 1â11.

[61] P. A. Rad, D. Hofmann, S. A. Pertuz Mendez, and D. Goehringer, âOptimized deep learning object recognition for drones using embedded GPU,â in Proc. 26th IEEE Int. Conf. Emerg. Technol. Factory Automat., 2021, pp. 1â7.

<!-- image-->

Rongye Shi (Member, IEEE) received the PhD degree in electrical and computer engineering from Carnegie Mellon University, Pittsburgh, PA USA, in 2019. He was a postdoctoral scientist with Columbia University from 2019-2020. He is currently an associate professor with the School of Artificial Intelligence, Beihang University, Beijing, China. His research focuses on physics-informed AI, collective intelligence, multi-agent reinforcement learning, and their applications to smart cities, communications, mobile computing and AI for Sciences. He received

the 2019 Amazon AWS Machine Learning Research Award, Huawei âInnovation Pioneerâ Presidentâs Award, Outstanding Reviewers (Top 10%) for ICML 2022, NSF Travel Award for BDCATâ17, and the Best Paper Award for ACM GLSVLSIâ17. He served as a program committee member for IEEE ICHMSâ20, ECML-PKDD 2021/2022 and a regular session co-chair for IEEE ITSCâ18. He is a member of ACM.

<!-- image-->

Xin Yu is currently working toward the PhD degree with the School of Computer Science and Engineering, Beihang University, Beijing, China. He will join the Institute of Automation, Chinese Academy of Sciences, Beijing, China, as an assistant professor in Spring, 2025. His research focuses on multi-agent reinforcement learning, aiming to enhance sample efficiency by integrating domain knowledge.

<!-- image-->

Yandong Wang is currently working toward the MS degree with the School of Artificial Intelligence, Beihang University, Beijing, China. His research interests include multi-agent reinforcement learning and its applications to UAV swarm-based communication coverage.

<!-- image-->

Yongkai Tian is currently working toward the PhD degree with the School of Computer Science and Engineering at Beihang University, Beijing, China. His research focuses on multi-agent reinforcement learning.

<!-- image-->

Zhenyu Liu (Member, IEEE) received the BS (with honor) and MS degrees in electronic engineering from Tsinghua University in 2011 and 2014, respectively. and the PhD degree in networks and statistics from the Massachusetts Institute of Technology (MIT) in 2022. Currently, he is an assistant professor with Tsinghua Shenzhen International Graduate School, Tsinghua University. His research interests include wireless communications, network localization, distributed inference and learning, networked control, and quantum information science. He received the first prize of the IEEE Communications Societyâs Student Competition in 2016 and 2019, a Research and Development 100 Award for Peregrine System in 2018, and the Best Paper Award at the IEEE Latin-American Conference on Communications in 2017.

<!-- image-->

Wenjun Wu (Member, IEEE) received the PhD degree in computer science from Beihang University, Beijing, China, in 2001. From 2002-2010, he was a research scientist with Indiana University, Bloomington, IN USA, and the Argonne National Laboratory, the University of Chicago, Chicago, IL USA. He is now a full professor with the School of Artificial Intelligence, Beihang University. His research interests include multi-agent reinforcement learning, swarm intelligence, crowdsourcing, cloud computing, and AI for Science. During his time in the USA, he

focused on research in the field of advanced scientific computing and collaborative network platforms, leading and participating in scientific research projects including: the Computational Social and Behavioral Science Grid, the Drosophila Gene Regulatory Network Computing Environment, and the Multimedia Interactive Collaborative Environment. He has published more than 180 academic papers in international journals and conferences, and led in more than 30 national key projects, including the National Key R&D Program of China, NSFC Key Project. He received the Beijing Educational Achievement Award (First Prize).

<!-- image-->

Xiao-Ping Zhang (Fellow, IEEE) received the BS and PhD degrees in electronic engineering from Tsinghua University, in 1992 and 1996, respectively, and the MBA (honors) degree in finance, economics and entrepreneurship from the University of Chicago Booth School of Business, Chicago, IL. He is chair professor with Tsinghua Shenzhen International Graduate School (SIGS) and Tsinghua-Berkeley Shenzhen Institute (TBSI), Tsinghua University. He was the founding dean with the Institute of Data and Information (iDI), Tsinghua SIGS. He had

been with the Department of Electrical, Computer and Biomedical Engineering, Toronto Metropolitan University (Formerly Ryerson University), Toronto, ON, Canada, as a professor and the director of the Communication and Signal Processing Applications Laboratory (CASPAL), and has served as the program director of Graduate Studies. His research interests include sensor networks and IoT, machine learning/AI/robotics, statistical signal processing, image and multimedia content analysis, and applications in big data, finance, and marketing. He is fellow of the Canadian Academy of Engineering, fellow of the Engineering Institute of Canada, a registered professional engineer in Ontario, Canada, and a member of Beta Gamma Sigma Honor Society. He is the general co-chair for the IEEE International Conference on Acoustics, Speech, and Signal Processing, 2021. He is the general co-chair for 2017 GlobalSIP Symposium on Signal and Information Processing for Finance and Business, and the general co-chair for 2019 GlobalSIP Symposium on Signal, Information Processing and AI for Finance and Business. He was an elected member of the ICME steering committee. He is the general chair for ICME2024 and BioCAS2023. He is editor-in-chief for the IEEE Journal of Selected Topics in Signal Processing. He is senior area editor of the IEEE Transactions on Image Processing. He served as senior area editor of the IEEE Transactions on Signal Processing and associate editor of the IEEE Transactions on Image Processing, IEEE Transactions on Multimedia, IEEE Transactions on Circuits and Systems for Video Technology, IEEE Transactions on Signal Processing, and IEEE Signal Processing Letters. He was selected as IEEE distinguished lecturer by the IEEE Signal Processing Society and by the IEEE Circuits and Systems Society.

<!-- image-->

Manuela M. Veloso (Fellow, IEEE) received the PhD degree in computer science from Carnegie Mellon University, Pittsburgh, PA USA, in 1992. She is the Herbert A. Simon University professor Emerita with the School of Computer Science, Carnegie Mellon University, and the Past head of Machine Learning Department. She had led research in AI, with a focus on robotics and machine learning, having concretely researched and developed a variety of autonomous robots, including teams of soccer robots, and mobile service robots. Her robot soccer teams have been

RoboCup world champions several times, and the CoBot mobile robots have autonomously navigated for more than 1,000 km in university buildings. She extended her research to improve human life in cities with the focus to capture and process data about cities and people in them to have an impact on the universal quality of life. She is a member of the U.S. National Academy of Engineering (NAE) for her contributions to artificial intelligence and its applications in robotics and the financial service industry. She is the Past president of AAAI (the Association for the Advancement of Artificial Intelligence), and the co-founder, trustee, and Past president of RoboCup, one of the most prestigious and influential robotics competitions globally. She is the recipient of several best paper awards, the Einstein chair of the Chinese Academy of Science, the ACM/SIGART Autonomous Agents Research Award, the NSF Career Award, and the Allen Newell Medal for Excellence in Research. She is a fellow of ACM, AAAI, and AAAS.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_2_img_1.png|page_2_img_1]]
2. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_6_img_1.png|page_6_img_1]]
3. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_7_img_1.png|page_7_img_1]]
4. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_11_img_1.jpeg|page_11_img_1]]
5. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_17_img_1.jpeg|page_17_img_1]]
6. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_17_img_2.jpeg|page_17_img_2]]
7. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_17_img_3.jpeg|page_17_img_3]]
8. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_17_img_4.jpeg|page_17_img_4]]
9. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_17_img_5.jpeg|page_17_img_5]]
10. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_18_img_1.jpeg|page_18_img_1]]
11. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_18_img_2.jpeg|page_18_img_2]]
12. [[../extracted_images/Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage/page_18_img_3.jpeg|page_18_img_3]]

---

