# Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Scheduling

Xuanhan Zhou , Jun Xiong , Haitao Zhao , Senior Member, IEEE, Chao Yan , and Jibo Wei , Member, IEEE

AbstractâUnmanned aerial vehicles (UAVs) as mobile base stations are recognized as effective means for emergency communications. The performance of such systems depends on the movement of UAVs and scheduling of ground users (GUs). However, devising an efficient algorithm to jointly optimize UAV trajectories and user scheduling is still challenging, especially in real-time scenarios lacking central controllers. Multi-agent deep reinforcement learning (MADRL) provides a promising solution to this problem. Nevertheless, as the numbers of UAVs and GUs increase, existing MADRL algorithms encounter scalability and sample efficiency issues. In this paper, we develop a novel symmetry-augmented MADRL approach for learning scalable UAV trajectory design and user scheduling policies. The core idea is to utilize symmetries to reduce the multi-agent state-action space and enhance sample efficiency. Specifically, we design a family of neural networks to learn individual policies, namely entity permutation equivariant policy networks (EP2Nets). EP2Nets effectively leverage the permutation symmetry to reduce redundancy in the state-action space. Additionally, we achieve data augmentation by exploiting rotational and reflection symmetries, further boosting sample efficiency. Finally, a Symmetric QMIX (SymmQMIX) algorithm is proposed by integrating the EP2Net and data augmentation method into the QMIX algorithm. Simulation results indicate that SymmQMIX significantly outperforms QMIX and other symmetry-enhanced algorithms, achieving a 4.5-fold increase in converged performance and a 100-fold improvement in sample efficiency.

Index TermsâMulti-agent deep reinforcement learning (MADRL), symmetry, trajectory design, unmanned aerial vehicle (UAV).

## I. INTRODUCTION

U NMANNED aerial vehicles (UAVs) as mobile base sta-tions (BSs) have emerged as an effective solution for

Digital Object Identifier 10.1109/TMC.2024.3437679 emergency communications [1]. Compared with terrestrial infrastructures, UAVs can be rapidly deployed to any location. Besides, their exceptional maneuverability enables real-time adjustments in their positions to accommodate evolving communication needs [2]. However, individual UAVs have limited power and communication capacity. To overcome these limitations, deploying multiple UAVs to cooperatively serve ground users (GUs) has become a common strategy to extend the network coverage and enhance overall communication capability [3].

In multi-UAV assisted communications, the quality of service received by GUs depends on the positions of UAVs and the communication scheduling of GUs, which are closely coupled [4]. Therefore, the joint optimization of UAV trajectories and user scheduling can significantly enhance system performance. However, this problem exhibits high complexity, especially in scenarios involving numerous UAVs and GUs. Traditional optimization-based algorithms pre-design UAV trajectories and communication parameters offline, relying on static models and prior information [5], [6], [7], [8], [9]. They encounter difficulties in adapting to unexpected environmental variations [10]. Moreover, these methods necessitate centralized control and global information, rendering them impractical in multi-UAV systems lacking central controllers [11].

Multi-agent deep reinforcement learning (MADRL) [12], [13], [14], [15] offers a promising solution to the above challenges. In MADRL methods, UAVs are treated as individual agents, and a policy network is trained for each agent using experience gathered through their interactions with the environment [16]. After sufficient training, these policy networks can be utilized to make UAV trajectory and communication decisions in real time. This approach not only facilitates distributed and online decision-making but also promotes cooperation among UAVs.

Great efforts have been devoted to developing MADRL algorithms for the joint UAV trajectory and communication optimization problems [17], [18], [19], [20]. While these algorithms demonstrate satisfactory performance in small-scale problems, they encounter scalability and sample efficiency issues [21]. In the joint UAV trajectory design and user scheduling problem, the combined actions associated with trajectories and scheduling contribute to a substantial action space. Furthermore, both state and action dimensions scale with the increase in the number of UAVs and GUs, resulting in an explosive expansion of the state-action space. Consequently, existing MADRL algorithms

Chao Yan is with the College of Automation Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing, Jiangsu 211106, China (e-mail: yanchao@nuaa.edu.cn).

<!-- image-->  
Fig. 1. An illustration of the proposed symmetry-augmented MADRL approach. The permutation symmetry is incorporated into entity permutation policy networks to remove redundancy caused by different entity permutations. Additionally, the rotational and reflection symmetries are exploited to augment experience samples for more sample-efficient network updates.

require a substantial number of experience samples to achieve convergence in large scale scenarios. This renders them susceptible to getting trapped in local optima, leading to deterioration of converged performance [22].

Multi-UAV assisted communication systems possess various symmetries that can be exploited to reduce the state-action space. In this context, symmetries refer to transformations of stateaction pairs that leave the rewards and state transition probabilities invariant [23]. Fig. 1 illustrates three symmetries inherent in multi-UAV assisted communications: permutation symmetry, rotational symmetry, and reflection symmetry. These symmetries establish equivalence between the original state-action pairs and their transformed counterparts, enabling experience gained from one pair to improve the policy for all equivalent pairs. By leveraging these symmetries, we can remove redundancy in the state-action space, thereby enhancing sample efficiency and converged performance.

The effectiveness of leveraging symmetries has been demonstrated in deep reinforcement learning (DRL), either through encoding symmetries into policy networks [24], [25], [26], or by employing data augmentation to expand experience samples [27]. These approaches rely on global symmetries in the joint state-action space. This limitation restricts their applicability in MADRL, where symmetries exist at both the global environment and individual agent levels [28]. A few studies have explored the utilization of permutation symmetry in MADRL [29], [30], [31], [32]. However, beyond permutation symmetry, multiple other symmetries exist in multi-UAV assisted communications, including rotational and reflection symmetries. Therefore, a more comprehensive MADRL approach is necessary to leverage diverse symmetries.

In this paper, we propose a novel symmetry-augmented MADRL approach to solve the UAV trajectory and user scheduling optimization problem. As illustrated in Fig. 1, the core idea of our approach is to incorporate the permutation symmetry into policy networks, and exploit the rotational and reflection symmetries to augment experience samples. These techniques result in a substantial reduction of the state-action space, thereby improving sample efficiency and scalibility. To the best of our knowledge, this marks the initial endeavor to harness symmetries in MADRL-based UAV trajectory and communication optimization problems. The main contributions are summarized as follows:

We convert the problem into a decentralized partially observable Markov decision process (Dec-POMDP), where states, observations, and actions are represented in an entity-factored manner. This formulation allows us to transform the global symmetries into distributed symmetries at the agent level, laying the foundation for subsequent method design.

We design a family of neural networks for learning decentralized UAV trajectory design and user scheduling policies, namely entity permutation equivariant policy networks (EP2Nets). EP2Nets effectively reduce redundancy in the state-action by utilizing the permutation symmetry, thereby improving sample efficiency and algorithm performance.

- We achieve data augmentation by leveraging rotational and reflection symmetries. This method facilitates efficient learning from limited experience samples, reducing the need for costly agents-environment interactions.

We propose a Symmetric QMIX (SymmQMIX) algorithm by integrating the EP2Net and data augmentation method into the QMIX algorithm. Extensive simulations demonstrate that SymmQMIX significantly outperforms QMIX and other symmetry-enhanced algorithms [12] in terms of sample efficiency and converged performance.

The rest of this paper is organized as follows. Section II reviews existing research on multi-UAV assisted communications and related MADRL techniques. Section III-A defines the system model and formulates the joint UAV trajectory and user scheduling optimization problem. Section IV converts the problem into a Dec-POMDP and formulates the mathematical model for symmetries. Section V presents the details of the proposed approach. Section VI tests the effectiveness of the proposed approach through extensive simulations. Finally, Section VII concludes this work.

## II. RELATED WORK

Early research on multi-UAV assisted communications primarily solves UAV trajectory and communication problems using optimization-based algorithms. In [5], Wu et al. jointly optimize UAV trajectories, user scheduling, and power control to maximize the minimum throughput of all GUs. They employ block coordinate descent (BCD) [33] and successive convex optimization (SCA) [34] techniques to solve this nonconvex problem. BCD and SCA have also been successfully applied in other contexts, such as UAV-aided data collection [6] and UAV-assisted mobile edge computing (MEC) [7]. To reduce the computational complexity of the joint UAV trajectory and power control problem, Shen et al. [8] develop a parallel algorithm utilizing alternating direction method of multipliers technique. In [9], the UAV placement and movement optimization problem is studied for the multi-UAV coordinated multipoint communications. These studies optimize UAV trajectories and communication variables offline, restricting their applicability in dynamic environments. Moreover, global information and centralized control are required in these approaches, which are often unavailable in multi-UAV systems.

MADRL is considered as a promising technology for realtime applications, especially in situations when central controllers are absent. In [17] and [18], independent deep Q-network (IDQN) algorithm [35] is adopted to train policies for UAV agents. These policies are then utilized for online trajectory control. Given predefined UAV trajectories, Yuan et al. [19] employ actor-critic algorithm [36] to train UAVsâ user scheduling policies. Yin et al. [37] apply the QMIX algorithm [12] to optimize UAVsâ trajectory design and user scheduling policies. Ding et al. [20] model UAVs and GUs as heterogeneous agents, and learn their policies using multi-agent deep deterministic policy gradient (MADDPG) algorithm [14]. These approaches provide various real-time and decentralized solutions, demonstrating satisfactory performance in small-scale problems. However, as the number of UAVs and GUs increases, the state-action space grows explosively, resulting in poor sample efficiency and scalibility of these methods.

Recent research has demonstrated the potential of leveraging symmetries to improve sample efficiency in DRL problems, mainly through policy network design and data augmentation. In [23], Zinkevich et al. examine the notion of symmetries in Markov decision processes (MDPs). Clark et al. [24] encode symmetries related to playing Go into convolutional neural networks (CNNs). Simm et al. [25] propose a covariant actor-critic architecture for designing 3D symmetric molecules. Vanderpol et al. [26] introduce MDP homomorphic, a family of deep architectures that tie weights over symmetric state-action pairs. In [27], Lin et al. generate synthetic experience samples by applying symmetry transformations to real experience samples. These approaches depend on symmetries in the joint state-action space, and are not applicable in MADRL problems, where symmetries exist at both the global environment and individual agent levels.

In MADRL, research on symmetry is still relatively limited, but the application of permutation invariance [38] has begun to attract attention. In many multi-agent tasks, there is no specific order among entities. Changing the order of entity features in states and observations should maintain invariance of actions. Therefore, the policy network needs to satisfy permutation invariance, which is a special case of permutation symmetry. Efforts have been made to enhance sample efficiency of MADRL through the utilization of permutation invariance [29], [30], [31], [32]. In these studies, homogeneous entities are treated as anonymous, ensuring that permuting entity orders does not affect agentsâ policies. This is achieved by employing natural permutation-invariant architectures, such as DeepSets [38], Attention [39], and graph neural networks (GNNs) [40]. However, in the joint UAV trajectory design and user scheduling problem, the permutation of entity orders leads to synchronous changes in the input observations and output actions of the policy network, necessitating the consideration of more general permutation equivariance rather than invariance. Currently, permutation equivariance has received limited attention in the field of MADRL, with only preliminary exploration conducted by [31]. Moreover, these studies lack a comprehensive theoretical analysis for symmetries in MADRL, making it challenging to accommodate more types of symmetries.

<!-- image-->  
Fig. 2. An illustrative example of system model. Four UAVs are providing communication services for four GUs. The communication range and sensing range for each UAV are $R _ { \mathrm { c o m m } }$ and $R _ { \mathrm { s e n s e } } ,$ , respectively.

In contrast to the aforementioned research, this paper establishes a theoretical foundation for symmetries in MADRL by extending the concepts of symmetries from DRL. Based on this foundation, we consider multiple symmetries inherent in multi-UAV assisted communications and incorporate them into both policy networks and the learning process. As far as we know, no prior work has investigated symmetries in the joint UAV trajectory and communication problems. This research gap serves as the primary motivation for our study.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

## A. System Model

Fig. 2 illustrates a multi-UAV assisted communication system, where UAVs serve as mobile base stations to cooperatively provide communication services for GUs. Our objective is to improve the overall communication performance by jointly optimizing UAV trajectories and user scheduling.

We consider a square area of size $D \times D$ . The sets of UAVs and GUs are denoted as $\mathcal { N } = \{ 1 , . . . , N \}$ and $\mathcal { M } = \{ 1 , . . . , M \}$ , respectively. We divide the entire service duration into multiple equal time slots, each with a slot length Ï . These time slots are represented as $\mathcal { T } = \{ 1 , . . . , T \}$ . UAVs maintain a constant speed $V$ and flying altitude H. A 2-D Cartesian coordinate system is established to describe horizontal locations of UAVs and GUs, where the central point of the area is located at $[ 0 , 0 ] ^ { T }$ . As a result, the horizontal positions of UAV-n and GU-m are denoted as $\mathbf { q } _ { t } ^ { n }$ and $\mathbf { w } _ { t } ^ { n }$ , respectively.

tIn air-to-ground communications, obstacles such as terrain or buildings often hinder wireless signal propagation, leading to both line-of-sight (LoS) and non line-of-sight (NLoS) links. Therefore, we employ the elevation angle-dependent probabilistic LoS model [11] to calculate channel gain, which considers both LoS and NLoS links. At time slot t, the elevation angle from

GN-m to UAV-n is $\begin{array} { r } { \Theta _ { t } ^ { n , m } = \frac { 1 8 0 ^ { \circ } } { \pi } \cdot \arctan ( \frac { H } { | | \mathbf { w } ^ { m } - \mathbf { q } _ { t } ^ { n } | | } ) } \end{array}$ . Then, the t Ïprobability of LoS link is computed by

$$
p _ { t } ^ { \mathrm { L o S } , n , m } = \frac { 1 } { 1 + a \exp { ( - b ( \Theta _ { t } ^ { n , m } - a ) ) } } ,\tag{1}
$$

where a and $b$ are parameters dependent on the environment. The probability of NLoS link is $p _ { t } ^ { \mathrm { \acute { N } L o S } , n , m } = 1 - p _ { t } ^ { \mathrm { L o S } , n , m }$ . For teach case, the channel gain is computed as

$$
g _ { t } ^ { \xi , n , m } = \frac { 1 } { \eta ^ { \xi } } \left( \frac { 4 \pi f ^ { c } l _ { t } ^ { n , m } } { c } \right) ^ { - \alpha } , \xi \in \{ \mathrm { L o S } , \mathrm { N L o S } \} ,\tag{2}
$$

where $f ^ { c }$ is the carrier frequency, Î± is the path loss exponent, $\eta ^ { \xi }$ is the excessive path loss coefficients, and c is the light speed. The final channel gain is computed as the expectation of both LoS and NLoS cases: $\mathcal { G } _ { t } ^ { n , m } = p _ { t } ^ { \mathrm { L o S } , n , m } g _ { t } ^ { \mathrm { L o S } , n , m ^ { \bullet } } + p _ { t } ^ { \mathrm { N L o S } , n , m } g _ { t } ^ { \mathrm { N L o S } , n , m }$

tAt each time slot $t ,$ t t t t each GU associates with the UAV offering the best channel quality to establish a communication link. Each UAV can only serve one associated GU per time slot. We define a user scheduling variable $\beta _ { t } ^ { n , m }$ , where $\beta _ { t } ^ { n , m } = 1$ if GU-m is tscheduled by UAV-n at time slot t and $\beta _ { t } ^ { n , m } = 0$ otherwise. tFollowing references [5], [7], [8], [11], we assume that all UAVs communicate using the same frequency spectrum. To mitigate interference, UAVs employ directional antennas, constraining the transmitted signal within an angle. This results in a coverage range $R _ { \mathrm { { c o m m } } }$ . We define a coverage relation indicator $c _ { t } ^ { n , m } \in$ $\{ 0 , 1 \}$ , where $c _ { t } ^ { n , m } = 1$ tif GU-m is within the coverage area of UAV-n, and $c _ { t } ^ { n , m } = 0$ otherwise. The transmit power of UAVs is denoted as $p ,$ and the bandwidth is represented as B.

The signal-to-noise-plus-interference ratio (SINR) from UAV-n to GU-m is calculated as

$$
\mathrm { S I N R } _ { t } ^ { n , m } = \frac { c _ { t } ^ { n , m } \beta _ { t } ^ { n , m } p g _ { t } ^ { n , m } } { N _ { 0 } B + \sum _ { n ^ { \prime } } \sum _ { m ^ { \prime } \neq m } c _ { t } ^ { n ^ { \prime } , m } \beta _ { t } ^ { n ^ { \prime } , m ^ { \prime } } p g _ { t } ^ { n ^ { \prime } , m } } ,\tag{3}
$$

where $N _ { 0 }$ represents the power spectral density (PSD) of additive white Gaussian noise (AWGN). Then, the achievable throughput from UAV-n to GU-m at time slot t is computed as $\delta _ { t } ^ { n , m } = B \log _ { 2 } ( 1 + \mathrm { S I N R } _ { t } ^ { n , m } ) \tau$ . Consequently, the t ttotal achievable throughput of GU-m and the entire system over t time slots are given by $\begin{array} { r } { \Gamma _ { t } ^ { m } = \sum _ { i = 1 } ^ { t } \sum _ { n = 1 } ^ { N } \delta _ { i } ^ { n , \tilde { m } } } \end{array}$ and $\begin{array} { r } { \Gamma _ { t } = \sum _ { i = 1 } ^ { t } \sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } \delta _ { i } ^ { n , m } } \end{array}$ i n i, respectively. Additionally, the t i m n iaverage throughput achieved by GU-m over the previous t time slots is $\bar { \Gamma } _ { t } ^ { m } = \Gamma _ { t } ^ { m } / t$

## B. Problem Formulation

We aim to maximize the system throughput while ensuring fairness among all GUs. Following reference [11], we introduce Jainâs fairness index to evaluate fairness among GUs. Specifically, we define a throughput fairness index at each time slot t based on each GUâs average throughput over preceding time slots:

$$
\eta _ { t } = \frac { \left( \sum _ { m = 1 } ^ { M } \bar { \Gamma } _ { t } ^ { m } \right) ^ { 2 } } { M \left( \sum _ { m = 1 } ^ { M } ( \bar { \Gamma } _ { t } ^ { m } ) ^ { 2 } \right) } .\tag{4}
$$

$\eta _ { t }$ always satisfies $0 \leq \eta _ { t } \leq 1$ . A higher fairness index indicates t tnarrower variations in throughput among different GUs. The

maximum value of $\eta _ { t }$ is reached when all GUs achieve the same average throughput.

We define the fair throughput as the product of the system throughput and fairness index per time slot, expressed as

$$
\delta _ { t } ^ { \mathrm { f a i r } } = \eta _ { t } \sum _ { m = 1 } ^ { M } \delta _ { t } ^ { m } .\tag{5}
$$

Meanwhile, the total fair throughput during the communication period can be expressed as $\Gamma _ { T } ^ { \mathrm { f a i r } } = \sum _ { t } ^ { T } \delta _ { t } ^ { \mathrm { f a i r } }$

T t tWe represent the variables for UAV trajectories and user scheduling as $\mathbf { q } = \{ \mathbf { q } _ { t } ^ { n } | n \in \mathcal { N } , t \in \mathcal { T } \}$ and $\beta = \{ \beta _ { t } ^ { n , m } | n \in$ $\mathcal { N } , m \in \mathcal { M } , t \in \mathcal { T } \}$ t t, respectively. These variables are jointly optimized to maximize the total fair throughput during the communication period. The corresponding optimization problem can be formulated as follows:

$$
\operatorname* { m a x } _ { \mathbf { q } _ { T } , \beta _ { T } } \Gamma _ { T } ^ { \mathrm { f a i r } }\tag{6}
$$

$$
\mathrm { s . t . } \ | | \mathbf { q } _ { t + 1 } ^ { n } - \mathbf { q } _ { t } ^ { n } | | = V \tau , n \in \mathcal { N } , t \in \mathcal { T }\tag{6a}
$$

$$
\sum _ { m \in \mathcal { M } } \beta _ { t } ^ { n , m } \leq 1 , n \in \mathcal { N } , t \in \mathcal { T } .\tag{6b}
$$

Constraint (6a) enforces constant-speed UAV motion, while constraint (6b) specifies that each UAV can schedule at most one GU at any time slot. This problem is an NP-hard mixed-integer nonlinear programming problem, involving both continuous trajectory variables and discrete user scheduling variables. The coupling among these variables leads to an extensive solution space. Moreover, the non-convex nature of the objective function further adds the complexity.

In multi-UAV assisted communications, gathering global information involves high communication costs, and central controllers may be absent. Therefore, it is essential to employ a decentralized approach for optimization, where each UAV makes individual decisions. Besides, several additional restrictions must be considered:

1) Due to their limited sensing and communication ability, UAVs can only receive partial environment information.

2) To cope with potential sudden changes in the environment, the decisions must be made in real time.

3) Given the substantial population sizes in practical systems, the approach should be scalable.

To tackle these issues, we convert this optimization problem into a Dec-POMDP and propose a MADRL-based solution.

## IV. MADRL FORMULATION WITH SYMMETRIES

In this section, we first formulate a Dec-POMDP and briefly introduce the background knowledge related to symmetries. Subsequently, we employ this formulation to establish a mathematical model for global and distributed symmetries in MADRL. Finally, we identify three symmetries present in multi-UAV assisted communications.

## A. Entity-Factored Dec-POMDP Formulation

Within the Dec-POMDP formulation, we treat UAVs as individual agents. At each time slot, the environment information is described by state $\mathbf { s } _ { t } \in \cal { S }$ . Each UAV agent-n receives an observation $\mathbf { o } _ { t } ^ { n } \in { \mathcal { O } } ;$ , which provides partial information about $\mathbf { s } _ { t } .$ t. Then, it selects an action $a _ { t } ^ { n } \in \mathcal { A }$ based on its policy $\dot { \pi } ( a _ { t } ^ { n } | \mathbf { o } _ { t } ^ { n } ) : \mathcal { O } \times \mathcal { A } \to [ 0 , 1 ]$ t. All agentsâ actions form a joint taction $\mathbf { a } _ { t } = [ a _ { t } ^ { 1 } , . . . , a _ { t } ^ { N } ] \in \mathcal { A } = \mathcal { A } \times \cdot \cdot \cdot \times \mathcal { A }$ . As a result, the t t tenvironment transitions to the next state $\mathbf { s } _ { t + 1 }$ based on the state transition probability function $P ( \mathbf { s } _ { t + 1 } | \mathbf { s } _ { t } , \mathbf { a } _ { t } )$ . Meanwhile, all agents receive a reward $r _ { t } = R ( \mathbf { s } _ { t } , \mathbf { a } _ { t } )$ . The goal of MADRL is to determine the optimal policies for all agents that maximize the expected cumulative reward $\begin{array} { r } { \mathbb { E } _ { \dot { \pi } } [ \sum _ { l = 0 } ^ { \infty } \gamma ^ { \bar { l } } r _ { t + l } ] } \end{array}$ , where $\gamma \in [ 0 , 1 )$ denotes the discount factor.

To facilitate the subsequent conversion of global symmetries into distributed symmetries, we adopt an entity-factored approach to model Dec-POMDP [31]. Specifically, multi-UAV assisted communication systems comprise two types of entities: UAVs as learning agents and GUs as non-learning entities. Each entityâs feature is represented as a vector containing relevant environment information. Specifically, UAV-nâs feature at time slot t contains its current position and whether it schedules any GU at last time slot, i.e.,

$$
\mathbf { x } _ { t } ^ { \mathrm { u a v } , n } = \left[ \mathbf { q } _ { t } ^ { n } , \sum _ { m = 1 } ^ { M } \beta _ { t - 1 } ^ { n , m } \right] .\tag{7}
$$

Similarly, GU-mâs feature includes its position, whether it is scheduled by any UAV at last time slot, and its average throughput achieved over previous t time slots, i.e.,

$$
\mathbf { x } _ { t } ^ { \mathrm { u s e r } , m } = \left[ \mathbf { w } _ { t } ^ { m } , \sum _ { n = 1 } ^ { N } \beta _ { t - 1 } ^ { n , m } , \hat { \Gamma } _ { t } ^ { m } \right] .\tag{8}
$$

In the following, we define entity-factored components of the Dec-POMDP using these features.

1) State: The state encompasses all environment information relevant to the problem, including features of all entities. Consequently, the state is represented as

$$
\begin{array} { r } { \mathbf { s } _ { t } = \left[ \mathbf { x } _ { t } ^ { \mathrm { u a v } , 1 } , . . . , \mathbf { x } _ { t } ^ { \mathrm { u a v } , N } , \mathbf { x } _ { t } ^ { \mathrm { u s e r } , 1 } , . . . , \mathbf { x } _ { t } ^ { \mathrm { u s e r } , M } \right] . } \end{array}\tag{9}
$$

2) Observation: Each UAV agent can observe entity features within a certain range through sensing and information exchange via control channels. This range is referred to as the sensing range, denoted by $R _ { \mathrm { s e n s e } }$ . We define the actual feature of UAV-n / GU-m perceived by UAV-n as $\tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , n ^ { \prime } } / \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , m }$ , which equals to $\mathbf { x } _ { t } ^ { \mathrm { u a v } , n ^ { \prime } } / \mathbf { x } _ { t } ^ { \mathrm { u s e r } , m }$ t tif UAV-n / GU-m is within UAV-nâs sensing t trange and otherwise is set to an all-zero vector. The observation of UAV-n is represented as

$$
\mathbf { o } _ { t } ^ { n } = \left[ \mathbf { x } _ { t } ^ { \mathrm { u a v } , n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , 1 } , . . . , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , N } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , 1 } , . . . , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , M } \right]\tag{10}
$$

3) Action: At each time slot, UAVs should choose a flying direction to adjust their positions and schedule a GU to communicate with. Accordingly, the action taken by UAV-n is defined as

$$
a _ { t } ^ { n } = \left[ \phi _ { t } ^ { n } , m _ { t } ^ { n } \right] ,\tag{11}
$$

where $\phi _ { t } ^ { n } \in [ 0 , 2 \pi )$ denotes UAV-nâs flying direction at time slot $t , m _ { t } ^ { n } \in \dot { \mathcal { M } ^ { + } } = \mathcal { M } \bigcup \{ 0 \}$ is the ID of GU scheduled by UAV-n, and $m _ { t } ^ { n } = 0$ indicates no GU is scheduled. Most MADRL algorithms are designed specifically for either discrete action spaces or continuous action space. Optimizing discrete policies is typically simpler and exhibits better convergence performance compared to continuous policies. Therefore, when agents involve both continuous and discrete actions, the common practice is to discretize the continuous actions [11], [17], [18], [41]. Without loss of generality, we discretize the continuous direction space [0, 2Ï) into 4 directions, denoted as $\Phi = \{ 0 , { \textstyle \frac { \pi } { 2 } } , \pi , { \textstyle \frac { 3 \pi } { 2 } } \} .$ Consequently, each UAVâs action space becomes the Cartesian product of the direction set Î¦ and the GU set M, i.e.,

$$
\mathcal { A } = \Phi \times \mathcal { M } ^ { + } = \Phi \times \left( \mathcal { M } \bigcup \{ 0 \} \right) .\tag{12}
$$

Each action $a ^ { m , \phi } \in { \mathcal { A } }$ is a unique combination of a flying direction Ï from Î¦ and a GU ID m from $\mathcal { M } ^ { + }$ . According to the relationship between actions and entities, we factor the action space into 1 + M subspaces:

$$
{ \mathcal { A } } = { \mathcal { A } } ^ { \mathrm { e n v } } \bigcup \left\{ { \mathcal { A } } ^ { \mathrm { u s e r } , m } | m \in { \mathcal { M } } \right\} .\tag{13}
$$

Here, $\mathcal { A } ^ { \mathrm { e n v } } = \Phi \times \{ 0 \} = \{ a ^ { 0 , 0 } , a ^ { 0 , \frac { \pi } { 2 } } , a ^ { 0 , \pi } , a ^ { 0 , \frac { 3 \pi } { 2 } } \}$ and $\mathcal { A } ^ { \mathrm { u s e r } , m } = \Phi \times \{ m \} = \{ a ^ { m , 0 } , a ^ { m , \frac { \pi } { 2 } } , a ^ { m , \pi } , a ^ { m , \frac { 3 \pi } { 2 } } \}$ represent entity-uncorrelated action subspace and GU-m-correlated action subspace, respectively. Actions in $A ^ { \mathrm { e n v } }$ only select flying directions without scheduling any GUs, thereby impacting the entire environment but not specific entities. In contrast, actions in $A ^ { \mathrm { u s e r } , m }$ correspond to scheduling GU-m and choosing a flying direction from Î¦, thus impacting GU-mâs feature.

4) Reward: Since our goal is to maximize the total fair throughput during the communication period, we define the reward as the fair throughput at each time slot, expressed as

$$
r _ { t } = \eta _ { t } \sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } \delta _ { t } ^ { n , m } \tau .\tag{14}
$$

In MADRL, rewards are utilized to train agentsâ policies and are not necessary for the agentsâ decision-making processes. Therefore, even if the rewards rely on global environmental information, they will not impact the agentsâ decentralized decision-making.

5) Policy: The policy of each agent-n is represented as the probability $\dot { \pi } ( a _ { t } ^ { n } | \mathbf { o } _ { t } ^ { n } )$ of executing action $a _ { t } ^ { n }$ given the observation $\mathbf { o } _ { t } ^ { n }$ t t t. We construct a policy vector for each agent-n by tconcatenating probabilities of all discrete actions:

$$
\dot { \pi } \left( \mathbf { o } _ { t } ^ { n } \right) = \left[ \dot { \pi } \left( a ^ { 0 , 0 } | \mathbf { o } _ { t } ^ { n } \right) , . . . , \dot { \pi } \left( a ^ { M , \frac { 3 \pi } { 2 } } | \mathbf { o } _ { t } ^ { n } \right) \right] ,\tag{15}
$$

where $a ^ { 0 , 0 } , a ^ { 0 , \frac \pi 2 } , a ^ { 0 , \pi } , a ^ { 0 , \frac { 3 \pi } 2 } . . . , a ^ { M , 0 } , a ^ { M , \frac \pi 2 } , a ^ { M , \pi } , a ^ { M , \frac { 3 \pi } 2 }$ are all possible discrete actions in the action space A. According to the factorization of the action space, we similarly partition each individual policy vector into $M + 1$ subpolicy vectors:

$$
\dot { \pi } ( \mathbf { o } _ { t } ^ { n } ) = \left[ \dot { \pi } _ { t } ^ { n , \mathrm { e n v } } , \dot { \pi } _ { t } ^ { n , 1 } , . . . , \dot { \pi } _ { t } ^ { n , M } \right] ,\tag{16}
$$

where

$$
\begin{array} { r } { \dot { \boldsymbol { \pi } } _ { t } ^ { n , \mathrm { e n v } } = \biggl [ \dot { \boldsymbol { \pi } } \left( a ^ { 0 , 0 } \vert \mathbf { o } _ { t } ^ { n } \right) , \dot { \boldsymbol { \pi } } \left( a ^ { 0 , \frac { \pi } { 2 } } \vert \mathbf { o } _ { t } ^ { n } \right) , } \\ { \dot { \boldsymbol { \pi } } \left( a ^ { 0 , \pi } \vert \mathbf { o } _ { t } ^ { n } \right) , \dot { \boldsymbol { \pi } } \left( a ^ { 0 , \frac { 3 \pi } { 2 } } \vert \mathbf { o } _ { t } ^ { n } \right) \biggr ] } \end{array}
$$

and

$$
\begin{array} { r l } & { \dot { \boldsymbol { \pi } } _ { t } ^ { n , m } = \left[ \dot { \boldsymbol { \pi } } \left( a ^ { m , 0 } \vert \mathbf { o } _ { t } ^ { n } \right) , \dot { \boldsymbol { \pi } } \left( a ^ { m , \frac { \pi } { 2 } } \vert \mathbf { o } _ { t } ^ { n } \right) , \right. } \\ & { \qquad \left. \dot { \boldsymbol { \pi } } \left( a ^ { m , \pi } \vert \mathbf { o } _ { t } ^ { n } \right) , \dot { \boldsymbol { \pi } } \left( a ^ { m , \frac { 3 \pi } { 2 } } \vert \mathbf { o } _ { t } ^ { n } \right) \right] } \end{array}
$$

denote subpolicy vectors for entity-uncorrelated actions and GU-m-correlated actions, respectively.

The joint policy ${ \dot { \pi } } ( \mathbf { a } _ { t } | \mathbf { s } _ { t } )$ is the probability of all agent jointly executing the action $\mathbf { a } _ { t } = [ a _ { t } ^ { 1 } , . . . , a _ { t } ^ { N } ]$ given the state $\mathbf { s } _ { t }$ . It can t t t tbe calculated as the product of probabilities of all agentsâ individual actions: $\begin{array} { r } { \dot { \pi } ( \mathbf { a } _ { t } | \mathbf { \dot { s } } _ { t } ) = \prod _ { n = 1 } ^ { N } \dot { \pi } ( a _ { t } ^ { n } | \mathbf { s } _ { t } ) \approx \prod _ { n = 1 } ^ { N } \dot { \pi } ( a _ { t } ^ { n } | \mathbf { o } _ { t } ^ { n } ) } \end{array}$ t t n t t n t tFor the joint policy, we also construct a vector by concatenating all individual agentsâ policy vectors:

$$
\dot { \pi } ( \mathbf { s } _ { t } ) = [ \dot { \pi } ( \mathbf { o } _ { t } ^ { 1 } ) , \dots , \dot { \pi } ( \mathbf { o } _ { t } ^ { N } ) ] .\tag{17}
$$

## B. Preliminaries of Symmetries

Group theory [42] provides a mathematical framework for describing symmetries. This subsection briefly introduces the core concepts of group theory related to symmetries.

1) Groups and Transformations: First, the concepts of the group and group action are introduced.

Definition 1 (Group): A group is an algebraic structure containing a set of elements G and a binary operation Â· defined between elements, satisfying the following group axioms:

. Closure: For any two elements $g _ { 1 }$ and $g _ { 2 }$ within the set, the operation result $g _ { 1 } \cdot g _ { 2 }$ also belongs to the set.

- Associativity: For any three elements $g _ { 1 } , g _ { 2 }$ , and $g _ { 3 }$ within the set, it holds that $\left( g _ { 1 } \cdot g _ { 2 } \right) \cdot g _ { 3 } = g _ { 1 } \cdot \left( g _ { 2 } \cdot g _ { 3 } \right)$

- Identity Element: There exists an identity element e such that for any element g in the set, $e \cdot g = g \cdot e = g .$

- Inverse Element: Every element g in the set has an inverse element $g ^ { - 1 }$ , satisfying $g \cdot g ^ { - 1 } = g ^ { - 1 } \cdot g = e$

Each element in the group can represent a specific transformation. In symmetry analysis, a group represents the set of all symmetric transformations, including permutations, rotations, reflections, etc. Group action describes how the transformations in a group map elements of a specific set (or space) to other elements within the same set (or space).

Definition 2 (Group Action): The action of a group $G$ on a set (or space) X is a mapping $G \times X \to X$ , typically denoted as $( g , x ) \mapsto L _ { g } [ x ]$ , satisfying the following two conditions:

gCompatibility: For all $g _ { 1 } , g _ { 2 } \in G$ and all $x \in X$ , it holds that $L _ { g _ { 1 } \cdot g _ { 2 } } [ x ] = L _ { g _ { 1 } } [ L _ { g _ { 2 } } [ x ] ]$

g g g g- Identity Transformation: For all $x \in X$ , it holds that $L _ { e } [ x ] = x$ , where e is the identity element of G.

e2) Invariance and Equivariance: Invariance and equivariance are two concepts closely related to symmetries.

Definition 3 (Invariance): Given a transformation $L _ { q } : \mathcal { X } $ $\mathcal { X }$ within a group G, and a function $f : \mathcal { X }  \mathcal { V }$ g, if for all $g \in G$ and $x \in \mathcal { X } , f$ satisfies the following condition:

$$
f ( x ) = f ( L _ { g } [ x ] )\tag{18}
$$

then $f$ is said to be invariant or symmetric with respect to $\{ L _ { g } \} _ { g \in G }$ . The set $\{ L _ { g } \} _ { g \in G }$ constitutes a group of symmetric g g G g g Gtransformations, and G is called the symmetry group of $f .$

Definition 4 (Equivariance): Given a transformation $L _ { g }$ $\mathcal { X }  \mathcal { X }$ in a group G and a function $f : \mathcal { X }  \mathcal { Y }$ g, if there exists another transformation $K _ { q } : \mathcal { V }  \mathcal { V }$ such that for all $g \in G$ and $x \in \mathcal { X }$ g, the following condition is satisfied:

$$
K _ { g } [ f ( x ) ] = f ( L _ { g } [ x ] )\tag{19}
$$

then f is said to be equivariant with respect to $L _ { g }$

gEssentially, symmetry refers to the property of a function where the output remains unchanged after the input undergoes a specific transformation, making invariance a key aspect of symmetry analysis. Equivariance ensures that transformed data maintain the same form across different spaces, which is equally significant in symmetry analysis.

## C. Mathematical Model for Symmetries in Dec-POMDP

In this subsection, we first define global symmetries in the joint state-action and then distribute them into symmetries at the agent level.

1) Global Symmetries in Dec-POMDP: We define global symmetries using an approach similar to that employed for constructing symmetries in a single-agent MDP [23].

Definition 5: (Symmetric Dec-POMDP): A symmetric Dec-POMDP is a Dec-POMDP in which the following conditions are satisfied for at least one group G of transformations $L _ { g } : S \to S$ and $K _ { g } : { \mathcal { A } }  { \mathcal { A } } :$

$$
\begin{array} { r l } & { P ( \mathbf { s } _ { t + 1 } | \mathbf { s } _ { t } , \mathbf { a } _ { t } ) = P \left( L _ { g } [ \mathbf { s } _ { t + 1 } ] | L _ { g } [ \mathbf { s } _ { t } ] , K _ { g } [ \mathbf { a } _ { t } ] \right) , } \\ & { R ( \mathbf { s } _ { t } , \mathbf { a } _ { t } ) = R \left( L _ { g } [ \mathbf { s } _ { t } ] , K _ { g } [ \mathbf { a } _ { t } ] \right) , \forall g \in G , \forall \mathbf { s } _ { t } \in \mathcal { S } , \forall \mathbf { a } _ { t } \in \mathcal { A } . } \end{array}\tag{20}
$$

Then, we say $\{ ( L _ { g } , K _ { g } ) \} _ { g \in G }$ is a group of symmetry transforg g g Gmations, and G is a symmetry group of this Dec-POMDP.

In a symmetric Dec-POMDP, applying symmetry transformations to a state-action pair results in a set of equivalent state-action pairs sharing the same reward and state transition probability. Next, we will demonstrate that the optimal policy for a symmetric Dec-POMDP remains invariant to these equivalent pairs.

Theorem 1 (Invariant Joint Policy): For a symmetric Dec-POMDP with respective to $\{ ( L _ { g } , K _ { g } ) \} _ { g \in G }$ , the optimal joint g g g Gpolicy satisfies the following invariance constraint:

$$
\begin{array} { r } { \dot { \pi } ^ { * } ( \mathbf { a } _ { t } | \mathbf { s } _ { t } ) = \dot { \pi } ^ { * } ( K _ { g } [ \mathbf { a } _ { t } ] | L _ { g } [ \mathbf { s } _ { t } ] ) , \ : \forall g \in G , \ : \forall \mathbf { s } _ { t } \in \mathcal { S } , \ : \forall \mathbf { a } _ { t } \in \mathcal { A } . } \end{array}\tag{21}
$$

Proof: Please refer to the proof of Theorem 2 in [23].

Theorem 1 reveals that the optimal joint policy for a symmetric Dec-POMDP is invariant to the state-action transformations $\{ ( L _ { g } , K _ { g } ) \} _ { g \in G } . \mathrm { G i v } \epsilon$ n $\{ ( L _ { g } , K _ { g } ) \} _ { g \in G }$ , we can incorporate the g g g G g g g Ginvariance constraint (21) into the joint policy, thereby reducing the solution space. However, since our task is to determine each agentâs individual policy, we have to transform global symmetries into distributed symmetries.

2) Distributed Symmetries in Dec-POMDP: Next, we convert the global symmetries into a set of distributed symmetries at the agent level and establish a corresponding equivariance constraint for individual policies.

In Dec-POMDPs, since the observation of each agent represents part of the state, the transformation of $\mathbf { s } _ { t }$ with $L _ { g }$ results tin corresponding transformations in observations:

$$
L _ { g } [ \mathbf { s } _ { t } ] \Rightarrow U _ { g } [ \mathbf { o } _ { t } ^ { n } ] , \forall n \in \mathcal { N } ,\tag{22}
$$

where $U _ { g }$ represents the observation transformation. Consegquently, transforming $\mathbf { s } _ { t }$ leads to the following transformation tof the joint policy vector:

$$
\dot { \pi } \left( \cal L _ { g } [ { \bf s } _ { t } ] \right) = \left[ \dot { \pi } \left( \cal U _ { g } [ { \bf o } _ { t } ^ { 1 } ] \right) , . . . , \dot { \pi } \left( \cal U _ { g } [ { \bf o } _ { t } ^ { N } ] \right) \right] .\tag{23}
$$

Regarding the joint action, acting on $\mathbf { a } _ { t }$ with transformation $K _ { g }$ t gis equivalent to acting on individual actions with transformation $k _ { g } \mathrm { : }$

$$
K _ { g } [ \mathbf { a } _ { t } ] = \left[ k _ { g } \left[ a _ { t } ^ { 1 } \right] , . . . , k _ { g } \left[ a _ { t } ^ { N } \right] \right] .\tag{24}
$$

For discrete actions, an action transformation $k _ { g }$ maps a disgcrete action to another discrete action invertibly, leading to the permutation of elements within each agentâs policy vector:

$$
\mathbf { k } _ { g } \dot { \pi } ( \mathbf { o } _ { t } ^ { n } ) = \left[ \dot { \pi } \left( k _ { g } [ a ^ { 0 , 0 } ] | \mathbf { o } _ { t } ^ { n } \right) , . . . , \dot { \pi } \left( k _ { g } [ a ^ { M , \frac { 3 \pi } { 2 } } ] | \mathbf { o } _ { t } ^ { n } \right) \right]\tag{25}
$$

where $\mathbf { k } _ { g }$ represents the individual policy permutation matrix gresulting from the action transformation $k _ { g }$ . Correspondingly, gthe joint policy vector is also permuted as follows:

$$
{ \bf K } _ { g } \dot { \pi } ( { \bf s } _ { t } ) = \left[ { \bf k } _ { g } \dot { \pi } \left( { \bf o } _ { t } ^ { 1 } \right) , . . . , { \bf k } _ { g } \dot { \pi } \left( { \bf o } _ { t } ^ { N } \right) \right] ,\tag{26}
$$

where $\mathbf { K } _ { g }$ denotes the joint policy permutation matrix caused gby permutations of individual policy vectors.

The above derivations lead to an equivariance property of individual policies, as stated below.

Proposition 1 (Equivariant Individual Policies): For a symmetric Dec-POMDP, the optimal individual policies satisfy the following equivariance constraint:

$$
\mathbf { k } _ { g ^ { - 1 } } \dot { \pmb { \pi } } ^ { * } ( \mathbf { o } _ { t } ^ { n } ) = \dot { \pmb { \pi } } ^ { * } \left( U _ { g } [ \mathbf { o } _ { t } ^ { n } ] \right) , \forall g \in G , \forall n \in \mathcal { N } , \forall \mathbf { o } _ { t } ^ { n } \in \mathcal { O } ,\tag{27}
$$

where ${ \bf k } _ { g ^ { - 1 } }$ 1 represents the inverse matrix of $\mathbf { k } _ { g }$

g gProof: Since we use the joint policy vector to represent the joint policy, the invariance constraint (21) can be written as

$$
\begin{array} { r } { \dot { { \boldsymbol \pi } } ^ { * } ( { \bf s } _ { t } ) = { \bf K } _ { g } \dot { { \boldsymbol \pi } } ^ { * } \left( L _ { g } [ { \bf s } _ { t } ] \right) . } \end{array}\tag{28}
$$

Based on equations (23) and (26), this expression can be further represented as

$$
\begin{array} { r l } & { [ \dot { \boldsymbol { \pi } } ^ { * } ( \mathbf { o } _ { t } ^ { 1 } ) , \ldots , \dot { \boldsymbol { \pi } } ^ { * } ( \mathbf { o } _ { t } ^ { N } ) ] } \\ & { = \left[ \mathbf { k } _ { g } \dot { \boldsymbol { \pi } } ^ { * } \left( U _ { g } [ \mathbf { o } _ { t } ^ { 1 } ] \right) , \ldots , \mathbf { k } _ { g } \dot { \boldsymbol { \pi } } ^ { * } \left( U _ { g } [ \mathbf { o } _ { t } ^ { N } ] \right) \right] . } \end{array}\tag{29}
$$

Therefore, we have $\dot { \pi } ^ { * } ( \mathbf { o } _ { t } ^ { n } ) = \mathbf { k } _ { g } \dot { \pi } ^ { * } ( U _ { g } [ \mathbf { o } _ { t } ^ { n } ] )$ , which can be t gfurther transformed into constraint (27). -

Proposition 1 indicates that the optimal individual policies for a symmetric Dec-POMDP are equivariant to the observationpolicy transformation $( U _ { g } , \mathbf { k _ { g } } )$ , i.e., the transformation of the observation with $U _ { g }$ results in a corresponding transformation gof individual policy vector with $\mathbf { k } _ { \mathbf { g } } .$ . Given $\{ ( U _ { g } , { \bf k } _ { g } ) \} _ { g \in G }$ , we can incorporate the equivariance constriant (27) into individual policies, reducing the solution space.

## D. Symmetries in Multi-UAV Assisted Communications

Based on the Dec-POMDP model constructed in Section IV-A, we identify three symmetries present in multi-UAV assisted communications: permutation symmetry, rotational symmetry, and reflection symmetry.

1) Permutation Symmetry: In multi-UAV assisted communications, UAVs and GUs do not have a natural order. Therefore, state-action pairs with identical entity features but different entity orders are equivalent. According to this prior knowledge, we define the permutation symmetry.

All permutations of N UAVs and M GUs form a symmetry group $G ^ { \mathrm { p t } }$ . Given any permutation-pair $( \omega _ { g } ^ { \mathrm { u a v } } , \omega _ { g } ^ { \mathrm { u s e r } } ) \in G ^ { \mathrm { p t } }$ : $\mathcal { N } \times \mathcal { M }  \mathcal { N } \times \mathcal { M }$ g g, the orders of UAV-n and GU-m become $n ^ { \prime \prime } = \omega _ { q } ^ { \mathrm { u a v } } [ n ]$ and $\omega _ { g } ^ { \mathrm { u s e r } } [ m ]$ , respectively. Additionally, entity g gfeatures within the observation vector is also permuted, resulting in a new observation vector $\bar { \mathbf { o } } _ { t } ^ { n ^ { \prime \prime } }$ . We denote the inverse operation of $\omega _ { g } ^ { \mathrm { u a v } }$ and $\omega _ { g } ^ { \mathrm { u s e r } }$ as $\omega _ { g ^ { - 1 } } ^ { \mathrm { u a v } }$ tand $\omega _ { g ^ { - 1 } } ^ { \mathrm { u s e r } }$ , respectively. Then, the g g g gobservation transformation can be represented as

$$
\bar { \mathbf { o } } _ { t } ^ { n ^ { \prime \prime } } = U _ { g } ^ { \mathrm { p t } } \big [ \mathbf { o } _ { t } ^ { n } \big ] = \bigg [ \mathbf { x } _ { t } ^ { \mathrm { u a v } , n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , \omega _ { g ^ { - 1 } } ^ { \mathrm { u a v } } [ 1 ] } , . . . , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , \omega _ { g ^ { - 1 } } ^ { \mathrm { u a v } } [ N ] } ,
$$

$$
\tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , \omega _ { g ^ { - 1 } } ^ { \mathrm { u s e r } } [ 1 ] } , . . . , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , \omega _ { g ^ { - 1 } } ^ { \mathrm { u s e r } } [ M ] } \Bigg ] .
$$

It should be noted that $\bar { \mathbf { o } } _ { t } ^ { n ^ { \prime \prime } }$ is obtained by reordering entity features in $\mathbf { o } _ { t } ^ { n }$ t, without changing individual entity features.

(30)

tAccording to (16), each agentâs policy vector consists of an entity-uncorrelated subpolicy vector and M GU-correlated subpolicy vectors. On the one hand, due to the correspondence between each GU-m-correlated subpolicy vector and GU-m, permuting GUsâ order leads to the same permutation among different subpolicy vectors related to these GUs. On the other hand, the choice of flying direction is independent of the UAV and GU orders. Therefore, permuting UAVs or GUsâ features does not change the action probabilities related to different flying directions within each subpolicy. Consequently, the corresponding individual policy permutation matrix can be represented as

$$
\mathbf { k } _ { g } ^ { \mathrm { p t } } \dot { \pi } ( \mathbf { o } _ { t } ^ { n } ) = \left[ \dot { \pi } _ { t } ^ { n , \mathrm { e n v } } , \dot { \pi } _ { t } ^ { n , \omega _ { g } ^ { \mathrm { u s e r } } [ 1 ] } , . . . , \dot { \pi } _ { t } ^ { n , \omega _ { g } ^ { \mathrm { u s e r } } [ M ] } \right] .\tag{31}
$$

Based on the above formulation, the equivariance constraint (27) can be specified as the following permutation equivariance constraint:

$$
\mathbf { k } _ { g ^ { - 1 } } ^ { \mathrm { p t } } \dot { \pi } \big ( \mathbf { o } _ { t } ^ { n } \big ) = \dot { \pi } \left( U _ { g } ^ { \mathrm { p t } } \big [ \mathbf { o } _ { t } ^ { n } \big ] \right) , \forall g \in G ^ { \mathrm { p t } } , \forall n \in \mathcal { N } , \forall \mathbf { o } _ { t } ^ { n } \in \mathcal { O } .\tag{32}
$$

2) Rotational and Reflection Symmetries: In multi-UAV assisted communications, rotational and reflection symmetries demonstrate the systemâs invariant properties under specific spatial transformations. As described in Section III-A, in the probabilistic LoS model, the channel gain between UAVs and

<!-- image-->  
Fig. 3. Illustrations of rotational and reflection symmetries, where UAVs and GUs are projected onto the same plane.

GNs is determined solely by their relative positions, not by their absolute positions.2 Consequently, as long as the relative positions between UAVs and GNs remains unchanged, UAVsâ policies should also remain unchanged.

The space encompassing all UAVs and GUs forms a cuboid, where UAVs and GUs operate on planes at different altitudes, restricted to horizontal movement only. In this case, positional changes in three-dimensional space are reduced to movements on a two-dimensional plane. Specifically, when the planes containing UAVs and GUs rotate around the central point by the same angle or reflect along the same symmetry axis, the horizontal positions of these entities change accordingly. However, their relative positions remain constant, preserving the quality of the ground-to-air communication channel. As a result, the scheduling relationship between UAVs and GUs, as well as the UAVsâ flying direction relative to their service area should also remain unchanged. This indicates that the state-action pairs, after symmetric rotations or reflections, are equivalent in terms of the systemâs reward and state transition probabilities. Leveraging this prior knowledge, we can construct the corresponding symmetry group.

To clarify, we project the positions of UAVs and GUs onto a single plane, representing their movements as horizontal shifts on this plane. As illustrated in Fig. 3, within this plane, all symmetric rotations and reflections for a square area form a symmetry group. This group comprises an identity transformation $g _ { e } ,$ rotations at three angles: $g _ { \pi / 2 } , g _ { \pi }$ , and $g _ { 3 \pi / 2 } ,$ as well e Ï/ Ïas reflections across four symmetry axis: horizontal $g _ { H }$ , vertical $^ { g } V ^ { , }$ , diagonal g 1, and antidiagonal $g _ { D 2 }$ H. We represent this group as $G ^ { \mathrm { r t } } = \left\{ g _ { e } , g _ { \pi / 2 } , g _ { \pi } , g _ { 3 \pi / 2 } , g _ { H } , g _ { V } , g _ { D 1 } , g _ { D 2 } \right\}$

A rotation by an angle Ï acting on a point ${ \bf z } = [ z _ { 1 } , z _ { 2 } ] ^ { T }$ can be achieved using a $2 \times 2$ matrix:

$$
\begin{array} { r } { R _ { g _ { \psi } } [ \mathbf { z } ] = \left[ \begin{array} { c c } { \cos \psi } & { - \sin \psi } \\ { \sin \psi } & { \cos \psi } \end{array} \right] \mathbf { z } . } \end{array}\tag{33}
$$

Similarly, the reflections can be achieved using $2 \times 2$ matrices as follows:

$$
\begin{array}{c} \begin{array}{c} \begin{array}{c} \begin{array}{c} \begin{array} { r l } { { \cal R } _ { g _ { H } } [ { \bf z } ] = \left[ { 1 } & { 0 } \\ { 0 } & { - 1 } \end{array} \right] { \bf z } , ~ } & { { \cal R } _ { g _ { V } } [ { \bf z } ] = \left[ { - 1 } & { 0 } \\ { 0 } & { 1 } \end{array} \right] { \bf z } , } \\ { { \cal R } _ { g _ { D 1 } } [ { \bf z } ] = \left[ { 0 } & { 1 } \\ { 1 } & { 0 } \end{array} \right] { \bf z } , ~ } & { { \cal R } _ { g _ { D 2 } } [ { \bf z } ] = \left[ { \bf 0 } & { - 1 } \\ { - 1 } & { 0 } \end{array} \right] { \bf z } . } \end{array}\tag{34}
$$

Rotating or reflecting coordinates of all entities with $g \in G ^ { \mathrm { r t } }$ results in the following transformations for each UAV and GUâs features:

$$
\begin{array} { r l } & { l _ { g } ^ { \mathrm { u a v } } \left[ \mathbf { x } _ { t } ^ { \mathrm { u a v } , n } \right] = \left[ R _ { g } \left[ \mathbf { q } _ { t } ^ { n } \right] , \displaystyle \sum _ { m = 1 } ^ { M } \beta _ { t - 1 } ^ { n , m } \right] , \ : \forall n \in \mathcal { N } } \\ & { l _ { g } ^ { \mathrm { u s e r } } \left[ \mathbf { x } _ { t } ^ { \mathrm { u s e r } , m } \right] = \ : \left[ R _ { g } \left[ \mathbf { w } _ { t } ^ { m } \right] , \displaystyle \sum _ { n = 1 } ^ { N } \beta _ { t - 1 } ^ { n , m } , \bar { \Gamma } _ { t } ^ { m } \right] , \ : \forall m \in \mathcal { M } . } \end{array}\tag{35}
$$

Consequently, the state transformation can be represented as

$$
\begin{array} { r } { L _ { g } ^ { \mathrm { r t } } [ \mathbf { s } _ { t } ] = \left[ l _ { g } ^ { \mathrm { u a v } } \left[ \mathbf { x } _ { t } ^ { \mathrm { u a v } , 1 } \right] , . . . , l _ { g } ^ { \mathrm { u a v } } \left[ \mathbf { x } _ { t } ^ { \mathrm { u a v } , N } \right] , \right. } \\ { \left. l _ { g } ^ { \mathrm { u s e r } } \left[ \mathbf { x } _ { t } ^ { \mathrm { u s e r } , 1 } \right] , . . . , l _ { g } ^ { \mathrm { u s e r } } \left[ \mathbf { x } _ { t } ^ { \mathrm { u s e r } , M } \right] \right] . } \end{array}\tag{36}
$$

Similarly, the observation transformation can be represented as

$$
U _ { g } ^ { \mathrm { r t } } \left[ \mathbf { o } _ { t } ^ { n } \right] = \left[ l _ { g } ^ { \mathrm { u a v } } \left[ \mathbf { x } _ { t } ^ { \mathrm { u a v } , n } \right] , l _ { g } ^ { \mathrm { u a v } } \left[ \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , 1 } \right] , . . . , l _ { g } ^ { \mathrm { u a v } } \left[ \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , N } \right] , \right.
$$

$$
l _ { g } ^ { \mathrm { u s e r } } [ \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , 1 } ] , . . . , l _ { g } ^ { \mathrm { u s e r } } [ \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , M } ] ] .\tag{37}
$$

For the individual action, a rotation of $\psi$ transforms the flying direction Ï corresponding to each discrete action $a ^ { m , \phi }$ to $( \phi + \psi )$ mod 2Ï, where mod denotes the modulus operation. Consequently, their corresponding individual action transformation can be represented as

$$
k _ { g _ { \psi } } ^ { \mathrm { r t } } [ a ^ { m , \phi } ] = a ^ { m , ( \phi + \psi ) \mathrm { ~ m o d ~ } 2 \pi } , \forall m \in \mathcal { M } ^ { + } , \forall \phi \in \Phi .\tag{38}
$$

The horizontal reflection, vertical reflection, and two diagonal reflection transform the flying direction $\phi$ to $( 2 \pi - \phi )$ mod 2Ï, $( \pi - \phi )$ mod 2Ï, $\left( { \frac { \pi } { 2 } } - \phi \right)$ mod 2Ï, and $\bigl ( \frac { 3 \pi } { 2 } - \phi \bigr )$ mod 2Ï, respectively. As a result, their corresponding individual action transformation can be represented as

$$
\left\{ \begin{array} { l l } { k _ { g _ { H } } ^ { \mathrm { r f } } [ a ^ { m , \phi } ] = a ^ { m , ( 2 \pi - \phi ) \bmod 2 \pi } } \\ { k _ { g _ { V } } ^ { \mathrm { r f } } [ a ^ { m , \phi } ] = a ^ { m , ( \pi - \phi ) \bmod 2 \pi } } \\ { k _ { g _ { D 1 } } ^ { \mathrm { r f } } [ a ^ { m , \phi } ] = a ^ { m , ( \frac { \pi } { 2 } - \phi ) \bmod 2 \pi } } & { \forall m \in \mathcal { M } ^ { + } , \forall \phi \in \Phi } \\ { k _ { g _ { D 2 } } ^ { \mathrm { r f } } [ a ^ { m , \phi } ] = a ^ { m , ( \frac { 3 \pi } { 2 } - \phi ) \bmod 2 \pi } } \end{array} \right.\tag{39}
$$

In the next section, we will develop a MADRL approach based on these symmetries.

<!-- image-->  
Fig. 4. Overview of the symmetry-augmented MADRL approach. Key distinctions between the proposed and standard MADRL approaches include: (a) The introduction of EP2Nets as policy networks for agents. (b) The incorporation of data augmentation into the learning process.

## V. SYMMETRY-AUGMENTED MADRL APPROACH

The typical learning process of MADRL involves two main steps: (1) The collection of experience samples through interactions between agents and the environment. (2) The iterative update of network parameters using these experience samples [36]. As illustrated in Fig. 4, the proposed symmetry-augmented MADRL approach differs from the standard MADRL approaches in two aspects: (1) The introduction of a family of neural networks for learning individual policies, namely entity permutation equivariant policy networks (EP2Nets). (2) The incorporation of data augmentation to expand experience samples. Both aspects leverage symmetries in multi-UAV assisted communications.

In this section, we first outline the structure of EP2Net and its two implementation methods. Subsequently, we discuss the data augmentation method that leverages rotational and reflection symmetries. Finally, we integrate these symmetry methods with the QMIX algorithm to introduce the SymmQMIX algorithm.

## A. Entity Permutation Equivariant Policy Networks

An entity permutation equivariant network (EP2Net) estimates the optimal individual policy for a UAV agent-n. It receives the agentâs observation vector as input and generates all action probabilities. Based on these probabilities, the final action can be selected stochastically. Compared to traditional policy networks, EP2Nets leverage permutation symmetry to reduce the state-action space, as elaborated below. For more details about permutation symmetry, see Section IV-D1.

1) The Architecture of EP2Nets: To ensure that the policy network for each agent remains unchanged when the order of agents changes, an EP2Net is shared across all UAV agents. Then, we only need to guarantee that permuting entity features in the observation vector results in a corresponding permutation in the policy vector. This is achieved by establishing correspondence between entity features and actions.

Fig. 5 illustrates the architecture of an EP2Net, which consists of an input module, a middle module, and an output module. We denote the functions of these layers as $f _ { \mathrm { i n } } ( \cdot ) , f _ { \mathrm { m i d } } ( \cdot )$ , and $f _ { \mathrm { o u t } } ( \cdot )$ , respectively. Moreover, the function of the whole EP2Net is represented as ${ \dot { \pi } } ( \mathbf { o } _ { t } ^ { n } ) = f _ { \mathrm { e p } } ( \mathbf { o } _ { t } ^ { n } )$

t tThe input module aggregates information from all perceivable entity features in the observation vector to generate an embedding feature. As shown in Fig. 5(a), EP2Net first generate an individual embedding for each entity feature using three distinct functions. Specifically, $f _ { \mathrm { i n } } ^ { \mathrm { o w n } } ( \cdot )$ is utilized to produce the embedding for the agentâs own feature, while $f _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ and $f _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot )$ are shared across different UAVs and GUs to generate their respective embeddings. This process can be expressed as

$$
\begin{array} { r l } & { \mathbf { z } _ { t } ^ { n , \mathrm { o w n } } = f _ { \mathrm { i n } } ^ { \mathrm { o w n } } \big ( \mathbf { x } _ { t } ^ { \mathrm { u a v } , n } \big ) , } \\ & { } \\ & { \mathbf { z } _ { t } ^ { n , \mathrm { u a v } , n ^ { \prime } } = f _ { \mathrm { i n } } ^ { \mathrm { u a v } } \left( \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , n ^ { \prime } } \right) , \ \forall n ^ { \prime } \in \mathcal { N } \backslash n , } \\ & { \mathbf { z } _ { t } ^ { n , \mathrm { u s e r } , m } = f _ { \mathrm { i n } } ^ { \mathrm { u s e r } } \left( \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , m } \right) , \ \forall m \in \mathcal { M } . } \end{array}\tag{40}
$$

Then, all $\mathrm { U A V s / G U s ^ { \prime } }$ individual embeddings are aggregated using a summation operation and further processed using $g _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ $/ \ : g _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot )$ to generate a group embedding:

$$
\begin{array} { r l } & { \mathbf { z } _ { t } ^ { n , \mathrm { u s e r } } = g _ { \mathrm { i n } } ^ { \mathrm { u s e r } } \left( \displaystyle \sum _ { n ^ { \prime } \neq n } \mathbf { z } ^ { n , \mathrm { u s e r } , n ^ { \prime } } \right) , } \\ & { \mathbf { z } _ { t } ^ { n , \mathrm { u s e r } } = g _ { \mathrm { i n } } ^ { \mathrm { u s e r } } \left( \displaystyle \sum _ { m } \mathbf { z } ^ { n , \mathrm { u s e r } , m } \right) . } \end{array}\tag{41}
$$

Finally, $g _ { \mathrm { i n } } ^ { \mathrm { e m b } } ( \cdot )$ takes the agentâs own embedding, UAVsâ group embedding, and GUsâ group embedding as input, and produces the final embedding feature:

$$
\begin{array} { r } { \mathbf { z } _ { t } ^ { n } = g _ { \mathrm { i n } } ^ { \mathrm { e m b } } \left( \mathbf { z } _ { t } ^ { n , \mathrm { o w n } } , \mathbf { z } _ { t } ^ { n , \mathrm { u a v } } , \mathbf { z } _ { t } ^ { n , \mathrm { u s e r } } \right) . } \end{array}\tag{42}
$$

The middle module further extracts information from the embedding feature. Following a minimal modification principle, we impose no restrictions on its structure. As in most policy networks, the middle layer produces a hidden state by taking the emebedding feature as input:

$$
\mathbf { h } _ { t } ^ { n } = f _ { \mathrm { m i d } } ( \mathbf { z } _ { t } ^ { n } ) .\tag{43}
$$

The output module infers the action probabilities by integrating information from the input and middle modules. As depicted in Fig. 5(b), the output module comprises two different functions, denoted as $f _ { \mathrm { o u t } } ^ { \mathrm { e n v } } ( \cdot )$ and $f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ , respectively. We utilize $f _ { \mathrm { o u t } } ^ { \mathrm { e n v } } ( \cdot )$ to generate entity-uncorrelated subpolicy vectors by taking the hidden state as input:

$$
\dot { \pi } _ { t } ^ { n , \mathrm { e n v } } = [ \dot { \pi } ( a ^ { 0 , 0 } \vert \mathbf { o } _ { t } ^ { n } ) , \dots , \dot { \pi } ( a ^ { 0 , \frac { 3 \pi } { 2 } } \vert \mathbf { o } _ { t } ^ { n } ) ] = f _ { \mathrm { o u t } } ^ { \mathrm { e n v } } \left( \mathbf { h } _ { t } ^ { n } \right) .\tag{44}
$$

Meanwhile, $f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ is employed to produce M GU-correlated subpolicy vectors separately. To establish the correspondence between each entity and actions related to it, we introduce GUmâs perceivable feature as an additional input of $f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ when generating GU-m-correlated subpolicy vector. Consequently, each $\dot { \pi } _ { t } ^ { n , \overline { { m } } }$ can be calculated as

$$
\begin{array} { r } { \dot { \pi } _ { t } ^ { n , m } = [ \dot { \pi } ( a ^ { m , 0 } | \mathbf { o } _ { t } ^ { n } ) , . . . , \dot { \pi } ( a ^ { m , \frac { 3 \pi } { 2 } } | \mathbf { o } _ { t } ^ { n } ) ] } \\ { = f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \mathbf { h } _ { t } ^ { n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , m } \right) , m \in \mathcal { M } . } \end{array}\tag{45}
$$

These subpolicy vectors are concatenated to form the policy vector ÏË $\mathbf { \nabla } \cdot \left( \mathbf { o } _ { t } ^ { n } \right)$ of agent-n:

$$
\pmb { \dot { \pi } } ( \mathbf { o } _ { t } ^ { n } ) = \left[ \dot { \pmb { \pi } } _ { t } ^ { n , \mathrm { e n v } } , \dot { \pmb { \pi } } _ { t } ^ { n , 1 } , . . . , \dot { \pmb { \pi } } _ { t } ^ { n , M } \right]
$$

<!-- image-->  
Fig. 5. The overall architecture of an EP2Net. (a) The input module generates embeddings for entities individually and then combines them into a final embedding. (b) The structure of the middle module remains unconstrained. (c) The output module generates each subpolicy vector separately.

$$
\begin{array} { r l } & { = \left[ f _ { \mathrm { o u t } } ^ { \mathrm { e n v } } \left( \mathbf { h } _ { t } ^ { n } \right) , f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \mathbf { h } _ { t } ^ { n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , 1 } \right) , . . . , f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \mathbf { h } _ { t } ^ { n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , M } \right) \right] } \\ & { = f _ { \mathrm { o u t } } \left( \mathbf { h } _ { t } ^ { n } , \left[ \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , 1 } , . . . , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , M } \right] \right) = f _ { \mathrm { e p } } ( \mathbf { o } _ { t } ^ { n } ) . } \end{array}
$$

2) Properties of EP2Nets: In the following, we will demonstrate that EP2Net satisfies the permutation equivariance property. Before that, we first present the permutation invariance property of the input module.

Proposition 2 (Permutation Invariance): Given the permutation group $G ^ { \mathrm { p t } }$ and the observation transformation $U _ { g } ^ { p t }$ , the input gmodule satisfies the permutation invariance constraint:

$$
\begin{array} { r } { \mathbf { z } _ { t } ^ { n } = f _ { \mathrm { i n } } \left( U _ { g } ^ { \mathrm { p t } } \left[ \mathbf { o } _ { t } ^ { n } \right] \right) = f _ { \mathrm { i n } } ( \mathbf { o } _ { t } ^ { n } ) , \forall g \in G ^ { \mathrm { p t } } . } \end{array}\tag{48}
$$

Proof: According to the definition of $U _ { g } ^ { \mathrm { p t } } , \ U _ { g } ^ { \mathrm { p t } } [ \mathbf { o } _ { t } ^ { n } ]$ simply reorders $\{ \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , n ^ { \prime } } \} _ { n ^ { \prime } \neq n }$ and $\{ \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , m } \} _ { m }$ . Since the input modtule processes each $\mathrm { U A V / G U }$ t feature separately using a shared function and then merging them through a summation operation, the group embeddings $\mathbf { z } _ { t } ^ { n , \mathrm { u a v } }$ and $\mathbf { z } _ { t } ^ { \breve { n } , \mathrm { u s e r } }$ remain unchanged t tregardless of UAVsâ/GUsâ arrangement. As a result, the final embedding feature $\mathbf { z } _ { t } ^ { n , \mathrm { u s e r } }$ is invariant to $U _ { g } ^ { \mathrm { p t } }$

t gCorollary 1: The cascade of the permutation-invariant input module with the middle module still maintains permutation invariance with respective to the observation vector:

$$
\mathbf { h } _ { t } ^ { n } = f _ { \mathrm { m i d } } \left( f _ { \mathrm { i n } } \left( U _ { g } ^ { \mathrm { p t } } \big [ \mathbf { o } _ { t } ^ { n } \big ] \right) \right) = f _ { \mathrm { m i d } } \left( f _ { \mathrm { i n } } ( \mathbf { o } _ { t } ^ { n } ) \right) , \forall g \in G ^ { \mathrm { p t } } .\tag{49}
$$

Proposition 3 (Permutation Equivariance): Given the permutation group $G ^ { \mathrm { p t } }$ and the observation-policy transformation pair $( U _ { g } ^ { p t } , { \bf k } _ { g } ^ { p t } )$ , an EP2Net satisfies the permutation equivariance

constraint:

$$
\begin{array} { r } { \mathbf { k } _ { g ^ { - 1 } } ^ { \mathrm { p t } } f _ { \mathrm { e p } } ( \mathbf { o } _ { t } ^ { n } ) = f _ { \mathrm { e p } } \left( U _ { g } ^ { \mathrm { p t } } \left[ \mathbf { o } _ { t } ^ { n } \right] \right) , \forall g \in G ^ { \mathrm { p t } } . } \end{array}\tag{50}
$$

Proof: According to Proposition 2 and Corollary 1, the hidden state is invariant to $U _ { g } ^ { p t }$ . By substituting the reordered $\mathrm { G U s } ^ { \prime }$ perceivable features and $\mathbf { h } _ { t } ^ { n }$ into (46), we can obtain the final expression for $f _ { \mathrm { e p } } ( U _ { g } ^ { \mathrm { p t } } [ \mathbf { o } _ { t } ^ { n } ] )$ , as presented in (47) shown at the tbottom of this page. The final equality of (47) is derived based on the definition of $\mathbf { k } _ { g ^ { - 1 } } ^ { \mathrm { p t } }$ , thus establishing the permutation equivariance. -

Proposition 3 reveals that EP2Nets are equivariant to the permutation of entity orders. In other words, when the entity order within the observation vector is permuted according to $U _ { g } ^ { \mathrm { p t } }$ , the action probabilities generated by EP2Net will undergo ga corresponding permutation according to $\mathbf { k } _ { g } ^ { \mathrm { p t } }$ . There are a total of $N ! \times M !$ gpermutations of all UAVs and GUs. Since EP2Nets are equivariant to these permutations, experience gained from one permutation can be utilized to improve the policies for all permutations. Consequently, the state-action space is reduced by a factor of $\frac { 1 } { N ! \times M ! }$

N MBesides the reduced state-action space, EP2Net has the following advantages:

1) Ability to handle dynamic population sizes: EP2Nets perform computations in an entity-wise manner, and the function is shared across homogeneous entities. Consequently, EP2Net can handle an arbitrary number of UAV/GU features.

2) Algorithm-agnostic: In EP2Nets, we only design input and output modules, keeping the backbone middle module unchanged. As a result, EP2Nets can be easily plugged into most MADRL algorithms.

$$
\begin{array} { r l } { f _ { \mathrm { e p } } \left( U _ { g } ^ { \mathrm { p t } } \big [ \mathbf { o } _ { t } ^ { n } \big ] \right) } & { = f _ { \mathrm { o u t } } \left( \mathbf { h } _ { t } ^ { n } , \left[ \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , \omega _ { g } ^ { \mathrm { u s e r } } } \big [ 1 \big ] , \underbrace { \qquad } , \mathbf { \cdot } , \mathbf { \cdot } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , \omega _ { g } ^ { \mathrm { u s e r } } } \big [ M \big ] \right] \right) } \\ & { = \left[ f _ { \mathrm { o u t } } ^ { \mathrm { e n v } } \left( \mathbf { h } _ { t } ^ { n } \right) , f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \mathbf { h } _ { t } ^ { n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , \omega _ { g } ^ { \mathrm { u s e r } } } \big [ 1 \big ] \right) , \mathbf { \cdot } \mathbf { \cdot } , f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \mathbf { h } _ { t } ^ { n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e w } , \omega _ { g } ^ { \mathrm { u s e r } } } \big [ M \big ] \right) \right] } \\ & { = \left[ \dot { \pi } _ { t } ^ { n , \mathrm { e n v } } , \dot { \pi } _ { t } ^ { n , \omega _ { g } ^ { \mathrm { u s e r } } } \big [ 1 \big ] , \mathbf { \cdot } \mathbf { \cdot } , \mathbf { \cdot } , \dot { \pi } _ { t } ^ { n , \omega _ { g } ^ { \mathrm { u s e r } } } \big [ M \big ] \right] = \mathbf { k } _ { g ^ { - 1 } } ^ { \mathrm { p t } } f _ { \mathrm { e p } } \big ( \mathbf { o } _ { t } ^ { n } \big ) } \end{array}\tag{47}
$$

TABLE I  
NETWORK CONFIGURATIONS OF FEP2NET AND HEP2NET
<table><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>FEP2Net</td><td rowspan=1 colspan=1>HEP2Net</td></tr><tr><td rowspan=1 colspan=1> $f _ { \mathrm { i n } } ^ { \mathrm { o w n } } ( \cdot )$ </td><td rowspan=1 colspan=2>A linear layer</td></tr><tr><td rowspan=1 colspan=1> $f _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ </td><td rowspan=1 colspan=1>A linear layer</td><td rowspan=1 colspan=1>Ahypernetwork-based linear layer</td></tr><tr><td rowspan=1 colspan=1> $f _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot )$ </td><td rowspan=1 colspan=1>A linear layer</td><td rowspan=1 colspan=1>Ahypernetwork-based linear layer</td></tr><tr><td rowspan=1 colspan=1> $g _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ </td><td rowspan=1 colspan=2>No processing</td></tr><tr><td rowspan=1 colspan=1> $g _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot )$ </td><td rowspan=1 colspan=2>No processing</td></tr><tr><td rowspan=1 colspan=1> $g _ { \mathrm { i n } } ^ { \mathrm { e m b } } ( \cdot )$ </td><td rowspan=1 colspan=2>Summation operation + Nonlinear activation function</td></tr><tr><td rowspan=1 colspan=1> $f _ { \mathrm { o u t } } ^ { \mathrm { e n v } } ( \cdot )$ </td><td rowspan=1 colspan=2>A linear layer</td></tr><tr><td rowspan=1 colspan=1> $f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ </td><td rowspan=1 colspan=1>A linear layer</td><td rowspan=1 colspan=1>A hypernetwork-based linear layer</td></tr></table>

3) Flexible network design: We do not specify the implementations of $\bar  f _ { \mathrm { i n } } ^ { \mathrm { o w n } } ( \cdot ) , f _ { \mathrm { i n } } ^ { \mathrm { u a \bar { v } } } ( \cdot ) , f _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot ) , g _ { \mathrm { i n } } ^ { \mathrm { u s e } } ( \cdot ) , g _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot ) , \bar { g _ { \mathrm { i n } } ^ { \mathrm { e m b } } ( \cdot ) }$ $f _ { \mathrm { o u t } } ^ { \mathrm { e n v } } ( \cdot )$ , and $f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ in EP2Nets. This grants the flexibility in designing these functions to create different EP2Nets.

## B. Efficient Implementations of EP2Nets

This subsection presents two implementations of EP2Net. First, we introduce the most basic version: the fully-connected EP2Net (FEP2Net), which is primarily implemented using linear layers. Next, by introducing hypernetworks into the FEP2Net, we propose the hypernetwork-based EP2Net (HEP2Net), which offers stronger model representational capabilities. Finally, the computational complexity of FEP2Net and HEP2Net is compared. Table I displays the network configurations of each function in FEP2Net and HEP2Net.

1) Fully-Connected EP2Net: FEP2Net represents the simplest implementation of EP2Nets. Specifically, we set $f _ { \mathrm { i n } } ^ { \mathrm { o w n } } ( \cdot )$ ï¼ $f _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ , and $f _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot )$ as linear layers for calculating embeddings, represented as $\mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { o w n } } ( \cdot ) , \mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ ), and $\mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot )$ , respectively. Each linear layer produces the output embedding by applying a weight matrix multiplication and adding a bias vector. For $g _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ and $g _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot )$ , we set them as identity functions, implying no processing. Regarding $g _ { \mathrm { i n } } ^ { \mathrm { e m b } } ( \cdot )$ , we aggregate the input embeddings and then pass them through a non-linear activation function such as ReLU, denoted as $\sigma _ { \mathrm { i n } } ( \cdot )$ . As a result, the expression for the input module can be written as

$$
\begin{array} { r l } & { \mathbf { z } _ { t } ^ { n } = f _ { \mathrm { i n } } \big ( \mathbf { o } _ { t } ^ { n } \big ) = \sigma _ { \mathrm { i n } } \bigg ( \mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { o w n } } \left( \mathbf { x } _ { t } ^ { \mathrm { u a v } , n } ; \theta _ { \mathrm { i n } } ^ { \mathrm { o w n } } \right) } \\ & { + \displaystyle \sum _ { n ^ { \prime } \neq n } \mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } \left( \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , n ^ { \prime } } ; \theta _ { \mathrm { i n } } ^ { \mathrm { u a v } } \right) + \displaystyle \sum _ { m } \mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u s e r } } \left( \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , m } ; \theta _ { \mathrm { i n } } ^ { \mathrm { u s e r } } \right) \bigg ) , } \end{array}\tag{51}
$$

where $\theta _ { \mathrm { i n } } ^ { \mathrm { o w n } } , \theta _ { \mathrm { i n } } ^ { \mathrm { u a v } }$ , and $\theta _ { \mathrm { i n } } ^ { \mathrm { u s e r } }$ denote the learnable parameters of linear layers including weights and biases. In the output module, we set both $f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ and f envout (Â·) as linear layers, denoted as $\mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { e n v } } ( \cdot )$ , and $\mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ . Consequently, the expression for the output module can be written as

$$
\begin{array} { r l r } & { } & { \dot { \pi } ( \mathbf { o } _ { t } ^ { n } ) = \left[ \mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { e n v } } \left( \mathbf { h } _ { t } ^ { n } ; \theta _ { \mathrm { o u t } } ^ { \mathrm { e n v } } \right) , \mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \mathbf { h } _ { t } ^ { n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , 1 } ; \theta _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \right) , \right. } \\ & { } & { \left. \qquad \cdot \cdot \cdot , \mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \mathbf { h } _ { t } ^ { n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , M } ; \theta _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \right) \right] , \qquad ( } \end{array}\tag{52}
$$

where $\theta _ { \mathrm { o u t } } ^ { \mathrm { e n v } }$ and $\theta _ { \mathrm { o u t } } ^ { \mathrm { u s e r } }$ represent network parameters.

<!-- image-->  
Fig. 6. Illustration of the hypernetwork-based network implementation. (a) In the implementation of $f _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ , the hypernetwork $\mathrm { H N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ takes each UAV feature as input and generates network parameters for the linear layer $\mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ (b) In the implementation of $f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot ) .$ , the hypernetwork $\mathrm { H N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ takes each GU feature as input and generates network parameters for $\mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$

In this setup, the input module essentially functions as an FC layer that shares weights and biases among different UAVs/GUs. Meanwhile, the output module acts as a linear layer that shares weights and biases among different GUs. Compared to standard FC layers/linear layers of equal scale, these modules have fewer parameters, thereby reducing the solution space for the optimal policy. However, despite its advantage, parameter sharing limits model expressiveness. Inspired by [31], HEP2Net addresses this issue by incorporating hypernetworks to generate network parameters for different UAVs/GUs.

2) Hypernetwork-Based EP2Net: Hypernetworks are a type of neural networks that generate parameters for another neural network [43]. As shown in Fig. 6, we employ a shared hypernetwork, denoted as $\mathrm { H N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ , to generate parameters of $\mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ for each $\mathrm { U A V } â n ^ { \prime }$ by taking its feature as input. As a result, the parameters of $\mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ vary across different UAVs and different time slots. Accordingly, the formulation of $f _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ becomes

$$
\begin{array} { r l } & { f _ { \mathrm { i n } } ^ { \mathrm { u a v } } \left( \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , n ^ { \prime } } \right) = \mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } \Bigg ( \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , n ^ { \prime } } ; } \\ & { ~ \mathrm { H N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } \left( \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u a v } , n ^ { \prime } } ; \varrho _ { \mathrm { i n } } ^ { \mathrm { u a v } } \right) \Bigg ) . } \end{array}\tag{53}
$$

Here, the hypernetwork $\mathrm { H N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ is constructed as an FC layer, and $\varrho _ { \mathrm { i n } } ^ { \mathrm { u a v } }$ denote its learnable parameters. The network $\mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u s e r } } ( \cdot )$ for GUs is modified in the same manner with $\mathrm { L N } _ { \mathrm { i n } } ^ { \mathrm { u a v } } ( \cdot )$ . In the output module, we also construct a shared hypernetwork, denoted as $\mathrm { H N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ , to generate parameters of $\mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ by taking each $\mathrm { G U } { - } m ^ { \prime } { \mathrm { s } }$ features as input. As $\tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , m }$ is fed into tthe hypernetwork, it is no longer necessary to be a direct input of $\mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ . Consequently, $f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ can be represented as

$$
\begin{array} { r } { f _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \mathbf { h } _ { t } ^ { n } , \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , m } \right) = \mathrm { L N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \Bigg ( \mathbf { h } _ { t } ^ { n , \mathrm { u s e r } , m } ; } \\ { { } } \\ { { \mathrm { H N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \left( \tilde { \mathbf { x } } _ { t } ^ { n , \mathrm { u s e r } , m } ; \varrho _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } \right) \Bigg ) } , } \end{array}\tag{54}
$$

where $\varrho _ { \mathrm { o u t } } ^ { \mathrm { u s e r } }$ represent the learnable parameters of $\mathrm { H N } _ { \mathrm { o u t } } ^ { \mathrm { u s e r } } ( \cdot )$ . The other part of HEP2Net remains consistent with FEP2Net.

In summary, HEP2Net introduces hypernetworks to generate network parameters, resulting in distinct network parameters for different entities across different time slots. This approach can be seen as a compromise between the parameter sharing of FEP2Net and no parameter sharing of traditional policy networks. As a result, HEP2Net enhances model expressiveness, while still maintaining the EP2Net structure.

3) Computational Complexity: Since EP2Nets only improve the input module and output module, we focus on the computational complexity of these two components. In the case of HEP2Net, both its input module and output module encompass two key processes: the forward computation involving an FC layer/linear layer and the parameter generation via hypernetworks. The computational complexity of the first process mirrors that of a standard FC layer/linear layer and can be calculated as $\mathcal { O } ( d _ { o } d _ { z } )$ for the input module and $\mathcal { O } ( 4 d _ { h } ( M + 1 ) )$ o zfor the output module. Here, $d _ { o } , \ d _ { z }$ and $d _ { h }$ hdenote the dio z hmensions of the observation vector, embedding feature, and hidden state, respectively, while $4 ( M + 1 )$ is the total number of discrete actions. Concerning the parameter generation process, a hypernetwork comprising a linear layer computes network parameters for all UAVs/GUs. Its computational complexity is $\mathcal { O } ( ( N - 1 ) d _ { \mathrm { u a v } } d _ { z } ( d _ { \mathrm { u a v } } + 1 ) + M d _ { \mathrm { u s e r } } d _ { z } ( d _ { \mathrm { u s e r } } + 1 ) )$ for input module and $\mathcal { O } ( 4 M d _ { \mathrm { u s e r } } ( d _ { \mathrm { u s e r } } + 1 ) )$ for the output module. Here, $d _ { z } ( d _ { \mathrm { u a v } } + 1 ) , d _ { z } ( d _ { \mathrm { u s e r } } + 1 )$ , and $4 ( d _ { \mathrm { u s e r } } + 1 ) )$ represent the numz zber of parameters that the hypernetworks need to generate, corresponding to their output dimension. Compared to FEP2Net or traditional policy networks consisting of FC layers and linear layers, the incorporation of hypernetworks adds computational complexity to HEP2Net. Nevertheless, the parameter generation process can be executed in parallel. When fully parallelized, the extra computational complexity remains a constant value independent of the number of UAVs and GUs, thereby rendering it acceptable.

## C. Data Augmentation-Based Learning Process

In this section, we incorporate data augmentation into the learning process by exploiting rotational and reflection symmetries. For more details about rotational and reflection symmetries, see Section IV-D2.

Since the rotation and reflection group $G ^ { \mathrm { r t } }$ is a symmetry group of our formulated Dec-POMDP, the state-observationaction tuples defined by the transformation $( L _ { g } ^ { \mathrm { r t } } , U _ { g } ^ { \mathrm { r t } } , k _ { g } ^ { \mathrm { r t } } )$ share g g gthe same reward and state transition probability. Therefore, we can generate synthetic experience samples by directly applying symmetric rotations and reflections to each real experience sample.

As shown in Fig. 4, during the learning process, all UAV agents interact with the environment by selecting actions according to their EP2Net-based policies. The experience sample generated at each time slot is represented as $( \mathbf { s } _ { t } , \{ \mathbf { o } _ { t } ^ { n } \} _ { n } , \{ a _ { t } ^ { n } \} _ { n } , \mathbf { s } _ { t + 1 } , \{ \mathbf { o } _ { t + 1 } ^ { n } \} _ { n } , r _ { t } )$ . We create an augmented t t texperience sample set by applying symmetric rotations and reflections to each experience sample:

$$
\begin{array} { r l } & { e _ { t } ^ { \mathrm { a u g } } = \Bigg \{ \Bigg ( L _ { g } ^ { \mathrm { r t } } [ \mathbf { s } _ { t } ] , \left\{ U _ { g } ^ { \mathrm { r t } } [ \mathbf { o } _ { t } ^ { n } ] \right\} _ { n } , \left\{ k _ { g } ^ { \mathrm { r t } } [ { a } _ { t } ^ { n } ] \right\} _ { n } , } \\ & { ~ L _ { g } ^ { \mathrm { r t } } [ \mathbf { s } _ { t + 1 } ] , \left\{ U _ { g } ^ { \mathrm { r t } } [ \mathbf { o } _ { t + 1 } ^ { n } ] \right\} _ { n } , r _ { t } \Bigg ) \mid g \in G ^ { \mathrm { r t } } \Bigg \} , } \end{array}\tag{55}
$$

Algorithm 1: Data Augmentation-Based Learning Process:   
Input: initial parameters of EP2Nets, denoted as $\theta ,$ and   
empty replay buffer $\mathcal { D } ^ { \mathrm { a u g } }$   
1: repeat   
2: Reset environment state   
3: for $t = 1 , . . . , T$ do   
4: Obtain the environment state $\mathbf { s } _ { t }$   
5: for all agent $n \in \mathcal N$ do   
6: Observe $\mathbf { o } _ { t } ^ { n }$ and select action $a _ { t } ^ { n }$ according to   
t taction probabilities generated by EP2Net   
7: Execute $a _ { t } ^ { n }$ in the environment   
8: end for   
9: for all agent $n \in \mathcal N$ do   
10: Obtain the next observation $\mathbf { o } _ { t + 1 } ^ { n }$   
11: end for   
12: Obtain the next state $\mathbf { s } _ { t + 1 }$ and team reward $r _ { t }$   
13: t t Generate augmented experience sets according to   
(55), and store them into $\mathcal { D } ^ { \mathrm { a u g } }$   
14: end for   
15: if itâs time to update then   
16: Randomly sample a batch of transitions   
$B = \{ ( \mathbf { s } _ { t } , \{ \mathbf { o } _ { t } ^ { n } \} _ { n } , \{ a _ { t } ^ { n } \} _ { n } , \mathbf { s } _ { t + 1 } , \{ \mathbf { o } _ { t + 1 } ^ { n } \} _ { n } , r _ { t } ) \}$ from   
Daug   
17: Update $\theta$ using arbitrary MADRL algorithm   
18: end if   
19: until Convergence   
Output: well-trained EP2Net parameters $\theta ^ { * }$

These experience samples are stored in an augmented replay buffer $\mathcal { D } ^ { \mathrm { a u g } }$ . Periodically, we take a batch of experience samples from $\mathcal { D } ^ { \mathrm { a u g } }$ to train policies using a specific MADRL algorithm. The complete training procedure is outlined in Algorithm 1. After achieving convergence, the well-trained EP2Net model can be deployed on each UAV, enabling decentralized and realtime decision making.

In traditional MADRL algorithms, the replay buffer only contains true experience samples gathered through the interactions between agents and the environment. In contrast, the proposed augmented replay buffer stores both true experience samples and synthetic samples generated by rotating and reflecting true samples. Transforming existing samples is much simpler than implementing agents-environment interactions, especially in real-world training. Therefore, this data augmentation method is equivalent to expanding true experience samples by $| G ^ { \mathrm { r t } } | = 8 .$ significantly enhancing their utility efficiency. It is noteworthy that the proposed data augmentation-based learning process is also algorithm-agnostic and can be applied to most MADRL algorithms.

## D. SymmQMIX Algorithm

The EP2Net network structure and data augmentation methods do not depend on any specific learning algorithm and can be combined with most MADRL algorithms. The QMIX algorithm [12] has demonstrated state-of-the-art performance in various MADRL tasks. In this section, we incorporate the aforementioned symmetry methods into QMIX, resulting in the SymmQMIX algorithm.

<!-- image-->  
Fig. 7. Illustrations of EP2Net-based local Q-networks in SymmQMIX. Each EP2Net computes individual Q-values for discrete actions. These values are then utilized to produce action probabilities according to an --greedy policy or a greedy policy.

QMIX learns a joint Q-value $Q ( \mathbf { s } _ { t } , \mathbf { a } _ { t } )$ , and factors it into a t tset of individual Q-values for each agent, $\{ Q ( \mathbf { o } _ { t } ^ { n } , a _ { t } ^ { n } ) \} _ { n \in \mathcal { N } }$ . The t tjoint Q-value represents the expected cumulative reward starting from state s , all agents taking the joint action a , and thereafter t tfollowing their respective optimal policies. Differently, the individual Q-value represents the contribution of each agent. To achieve this, QMIX comprises a set of local Q-networks for estimating the individual Q-values, and a mixing network that combines all individual Q-values into a joint Q-value. QMIX adopts a framework of centralized training with decentralized execution. During training, each agent selects actions based on their individual Q-values using an -greedy policy:

$$
\dot { \pi } \left( a _ { t } ^ { n } \mid \mathbf { o } _ { t } ^ { n } \right) = \left\{ \begin{array} { l l } { 1 - \epsilon + \frac { \epsilon } { | A | } , } & { \mathrm { i f ~ } a _ { t } ^ { n } = \arg \operatorname* { m a x } _ { a } Q \left( \mathbf { o } _ { t } ^ { n } , a \right) } \\ { \frac { \epsilon } { | A | } , } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{56}
$$

The training loss for QMIX is formulated using the Bellman equation for the joint Q-value:

$$
\mathcal { L } ( \pmb \theta ) = \mathbb { E } _ { \mathcal { D } } \left[ \left( r _ { t } + \gamma \operatorname* { m a x } _ { { \bf a } _ { t + 1 } } Q _ { \pmb \theta ^ { - } } \left( { \bf s } _ { t + 1 } , { \bf a } _ { t + 1 } \right) - Q _ { \pmb \theta } \left( { \bf s } _ { t } , { \bf a } _ { t } \right) \right) ^ { 2 } \right] .\tag{57}
$$

Here, D represents the experience replay buffer, Î¸ denote all learnable parameters in QMIX, and $\pmb { \theta } ^ { - }$ are periodically copied from Î¸. After convergence, each agent selects actions with the highest Q-values:

$$
{ \dot { \pi } } \left( a _ { t } ^ { n } \mid \mathbf { o } _ { t } ^ { n } \right) = { \left\{ \begin{array} { l l } { 1 , } & { { \mathrm { i f ~ } } a _ { t } ^ { n } = \arg \operatorname* { m a x } _ { a } Q \left( \mathbf { o } _ { t } ^ { n } , a \right) } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }\tag{58}
$$

PF   
In SymmQMIX, the local Q-networks are replaced with any implementation of EP2Nets, such as FEP2Nets or HEP2Nets. Only the input and output modules of QMIX are modified, keeping the backbone middle module remains unchanged. While EP2Nets are designed for generating action probabilities, their structures are also applicable to produce individual Q-values. As illustrated in Fig. 7, we configure each EP2Net to output individual Q-values for discrete actions. Then, the action probabilities can be obtained according to greedy or -greedy policies. During the training process, we employ data augmentation to augment experience samples as described in Section V-C. As a result, the experience replay buffer D is replaced with the augmented

replay buffer $\mathcal { D } ^ { \mathrm { a u g } }$ . All other aspects remain consistent with the original QMIX algorithm.

## VI. SIMULATION RESULTS

In this section, we first validate the effectiveness of the proposed approach by comparing SymmQMIX with benchmark algorithms. Then, we conduct ablation studies to investigate the impact of different components in SymmQMIX. Finally, we verify the scalibility of the proposed approach across various population sizes.

## A. Experiment Setup

1) Environment Parameters: The service region of UAVs is restricted to a square area of 2000 m Ã 2000 m. The service duration is 1500 s, divided into 150 time slots. During the learning process, each training episode corresponds to the entire service duration. At the beginning of each episode, we employ certain rules to randomly generate four non-overlapping hotspots. Within each hotspot, an equal number of GUs are generated. The position of each GU remains unchanged throughout an episode. UAVs are randomly positioned within the whole area, maintaining a constant flying altitude of $H = 1 0 0$ m and a fixed speed of $V = 1 0 \mathrm { m / s }$ . For the channel model, we employ parameters corresponding to the urban scenario [11]: $\alpha = 2 , a =$ $9 . 6 1 , b = 0 . 1 5 , \eta ^ { \mathrm { { L o S } } } = \bar { 1 } \bar { \mathrm { ~ d B } } , \eta ^ { \mathrm { { N L o S } } } = 2 0 \mathrm { { d B } }$ , and $f ^ { c } = 2 \operatorname { G H z }$ The transmit power of UAVs is 0.5 W, while the bandwidth is set as 1 MHz. The PSD of AWGN is â169 dBm/Hz. The communication range and sensing range of UAVs are defined as 200 m and 500 m , respectively. Unless otherwise stated, we set the numbers of UAVs and GUs as 4 and 64 (16in each hotspot). In Section VI-D, we will adjust the population size to evaluate the scalibility of the proposed method.

2) Algorithm Implementations: Regarding the SymmQMIX algorithm, the local Q network defaults to the HEP2Net structure. In Section VI-C, we will further compare the performance of FEP2Net and HEP2Net. For clarity, the algorithms corresponding to these two structures are named SymmQMIX-F and SymmQMIX-H respectively. QMIX serves as the foundational algorithms for all benchmark algorithms. All code and hyperparameters are based on the optimized QMIX implementation from project PyMARL2.

## B. Performance Evaluation of the Proposed Approach

1) Performance Comparison With MADRL Algorithms: In this subsection, we evaluate the performance improvement introduced by the proposed symmetry-augmented MADRL approach when combined with QMIX. We employ the original QMIX algorithm and its variants enhanced by three permutation-invariant networks as benchmarks.

QMIX: The original QMIX algorithm [12]. Both the input and output modules of local Q-networks comprise an FC layer, while the middle module consists of a gated recurrent unit (GRU).

SymmQMIX-H: As described in Section V-D, SymmQMIX is a combination of QMIX and the symmetry-augmented

<!-- image-->  
Fig. 8. Learning curves of SymmQMIX and benchmark algorithms for 200000 episodes. The numbers of UAVs and GUs are set as 4 and 64.

MADRL approach. In SymmQMIX-H, the local Qnetworks in QMIX are replaced with HEP2Nets.

DeepSets-QMIX: Following [30], DeepSets-QMIX incorporates DeepSets [38] into the input modules of local Qnetworks. Specifically, DeepSets applies a shared FC layer to processes each UAV/GU feature individually, followed by aggregation through summation.

- Attention-QMIX: Similar to [32], Attention-QMIX integrates a self-attention mechanism into the input modules of local Q-networks. It processes each entity feature separately and calculates an attention coefficient for each entity to facilitate weighted summation.

GNN-QMIX: Similar to [11], GNN-QMIX incorporates GNN into the input modules of local Q-networks. Specifically, GNN learns a representation for each UAV/GU by aggregating embedding features from other entities. These representations are aggregated by sum pooling.

Fig. 8 illustrates the learning curves of these algorithms concerning the total fair throughput. SymmQMIX-H significantly outperforms all benchmark algorithms in terms of both sample efficiency and converged performance. Specifically, QMIX exhibits the poorest performance, converging at approximately 20000 episodes with an total fair throughput of only 14.42 Gbits. In contrast, SymmQMIX-H achieves this level of performance in only 184 episodes, yielding a remarkable 109-fold improvement in sample efficiency. Furthermore, after convergence, SymmQMIX-H achieves total fair throughput of 66.94 Gbits, representing a 4.6-fold improvement over QMIX. This notable performance improvement can be primarily attributed to SymmQMIX-Hâs utilization of symmetries. QMIX neglects symmetries, leading to an expansive large state-action space that requires a considerable number of experience samples for training and is susceptible to local optima. SymmQMIX-H introduces HEP2Net on top of QMIX, effectively leveraging permutation symmetry to reduce the state-action space, and further enhance sample efficiency through data augmentation. Furthermore, the reduction in the state-action space prevents the algorithm from falling into local optima, resulting in improved converged performance.

<!-- image-->  
Fig. 9. Learning curves of three user scheduling methods, all learned by SymmQMIX-H. The numbers of UAVs and GUs are set as 4 and 64.

DeepSets-QMIX, Attention-QMIX, and GNN-QMIX bring performance improvements of 39.11%, 85%, and 61.6% over QMIX, respectively. However, all of them fall significantly short of SymmQMIXâs performance. These algorithms utilize natural permutation-invariant networks to ensure that changes in the entity order in the states and observations do not alter the policyâs output. These networks utilize a shared network to individually process entity features and then aggregate them in different ways. The permutation invariance property proves effective in tasks where actions are independent of entity order, such as pure UAV trajectory design, as it reduces redundancy in the state space due to entity permutations. Nevertheless, in the joint UAV trajectory design and user scheduling problem, changes in entity order simultaneously affect state and action permutations, leading to transformations in policy outputs. This permutation equivariance property cannot be achieved using DeepSets, Attention, and GNN. In contrast, our proposed EP2Net achieves it by establishing connections between observations and actions, leading to reduced state-action space and improved performance. Moreover, beyond permutation symmetry, SymmQMIX-H also accounts for rotational and reflection symmetries, further enhancing algorithm performance.

2) Performance Comparison With Heuristic Algorithms: In this subsection, we design two benchmark algorithms to validate the effectiveness of utilizing MADRL for learning user scheduling. These benchmark algorithms utilize MADRL solely for UAV trajectory design, while user scheduling decisions are made based on the following schemes:

Channel-prior: UAVs select the GU with the best channel among the associated GUs to provide service.

- Fair-prior: UAVs choose the GU with the lowest average throughput among the associated GUs for service.

We denote the proposed method as âMADRL-basedâ. All three methods employ SymmQMIX-H for learning UAV policies. Learning curves can be observed in Fig. 9. Table II presents the average throughput and fairness index achieved by these algorithms after convergence.

As shown in Table II, the channel-prior method prioritizes higher throughput at the expense of fairness, while the fair-prior method sacrifices system throughput for improved user fairness.

<!-- image-->  
(a) UAV trajectories

<!-- image-->  
(b) User scheduling

<!-- image-->  
(c) GUsâthroughput  
Fig. 10. Illustrative policies: a case study of 4 UAVs and 64 GUs. (a) Four UAVs autonomously move to various hotspot areas to establish communication coverage. (b) UAV-1, UAV-2, UAV-3, and UAV-4 correspond to hotspot areas-2, hotspot areas-4, hotspot areas-3, and hotspot areas-1, respectively. They sequentially serve GUs in their respective areas to ensure equitable coverage. (c) The throughput of all GUs exceeds 0, indicating that each GU has access to communication services. The throughput among GUs is relatively uniform, ensuring a certain level of fairness.

TABLE II  
COMPARISON OF FAIR THROUGHPUT, THROUGHPUT, FAIRNESS INDEX AFTER CONVERGENCE
<table><tr><td rowspan=1 colspan=1>Metrics</td><td rowspan=1 colspan=1>MADRL-based</td><td rowspan=1 colspan=1>Channel-prior</td><td rowspan=1 colspan=1>Fair-prior</td></tr><tr><td rowspan=1 colspan=1>Total Fair throughput (Gbits)</td><td rowspan=1 colspan=1>68.18</td><td rowspan=1 colspan=1>42.62</td><td rowspan=1 colspan=1>50.08</td></tr><tr><td rowspan=1 colspan=1>Total Throughput (Gbits)</td><td rowspan=1 colspan=1>83.45</td><td rowspan=1 colspan=1>73.55</td><td rowspan=1 colspan=1>62.34</td></tr><tr><td rowspan=1 colspan=1>Fairness index</td><td rowspan=1 colspan=1>0.806</td><td rowspan=1 colspan=1>0.567</td><td rowspan=1 colspan=1>0.8</td></tr></table>

The bolded data indicates that these are the results produced by our algorithm.

The total fair throughput achieved by these two algorithms is 42.62 Gbits and 50.08 Gbits, respectively. In contrast, the proposed method outperforms in all metrics, with total throughput being 13.5% higher than channel-prior and fairness metrics also surpassing fairness-prior. It ultimately converges to total fair throughput of 68.18 Gbits, marking a 60 % and 36 % improvement over the channel-prior and fairness-prior scheduling methods, respectively. These results demonstrate the effectiveness of MADRL in learning user scheduling policies that strike a balance between enhancing system throughput and ensuring user fairness. These policies excel across all metrics, highlighting the superiority of MADRL over heuristic approaches.

Fig. 10 present the trajectory design and user scheduling policies learned by UAV agents in an example episode. As illustrated in Fig. 10(a), UAVs cooperatively provide communication services across the entire area. Specifically, four UAVs navigate to distinct hotspot areas, maintaining significant distances between each other to reduce cross-link interference. Each individual UAV patrols within its corresponding region to ensure service coverage for all GUs. Fig. 10(b) presents the outcomes of user scheduling, with GUs categorized into groups labeled 1 â¼ 16, 17 â¼ 32, 33 â¼ 48, and 49 â¼ 64, corresponding to the four hotspot areas. Each UAV sequentially serves GUs within its corresponding hotspot area, ensuring equitable and adequate service. The total throughput achieved by each GU are illustrated in Fig. 10(c), demonstrating that every GU receives service. These findings underscore the optimization of system throughput and fairness among GUs.

<!-- image-->  
Fig. 11. Learning curves of ablation experiments for 200000 episodes. The numbers of UAVs and GUs are set as 4 and 64.

## C. Ablation Studies

In this section, we conduct ablation experiments to assess the contributions of various components within the proposed symmetry-augmented approach. The algorithms under consideration are list as follows:

- FEP2Net-QMIX To isolate the effect of EP2Net, we implement the simplest EP2Net variant, i.e., FEP2NEts, to replace the local Q-networks in QMIX.

HEP2Net-QMIX: To investigate the performance improvement brought about by hypernetworks, we replace the FEP2NEts in FEP2Net-QMIX with HEP2Nets.

- DA-QMIX: To examine the impact of data augmentation, we introduce data augmentation alone into QMIX.

SymmQMIX-F: To further investigate the impact of data augmentation, we introduce data augmentation into FEP2Net-QMIX. The only difference between SymmQMIX-F and SymmQMIX-H is the replacement of HEP2Nets with FEP2Nets.

The corresponding learning curves are displayed in Fig. 11.

1) Performance Improvement of EP2Nets: FEP2Net-QMIX achieves the converged performance of QMIX with just 780 episodes, marking an impressive 25.6-fold improvement in sample efficiency. Ultimately, it converges around 40600 episode, reaching total fair throughput of 47.85 Gbits, which is 3.3 times higher than QMIX. These results indicate that introducing the simplest form of EP2Net alone can lead to a substantial performance enhancement.

2) Performance Improvement of Hypernetworks: HEP2Net introduces hypernetworks into FEP2Net to generate network parameters for different entities, addressing the limitations in representational capacity caused by parameter sharing. This approach further enhances both sample efficiency and converged performance. Specifically, HEP2Net-QMIX attains the converged performance of FEP2Net-QMIX at 4200 episodes, resulting in an 11-fold improvement in sample efficiency. HEP2Net-QMIX reaches convergence at around 44000 episodes, achieving performance on par with SymmQMIX-H and representing a 42.6% improvement over FEP2Net-QMIX.

3) Performance Improvement of Data Augmentation: SymmQMIX-H introduces data augmentation into HEP2Net-QMIX. It converges in just 6800 episodes, resulting in a 6.5-fold improvement in sample efficiency. Additionally, DA-QMIX, which introduces data augmentation into QMIX, achieves a 4.7- fold improvement in sample efficiency and a 32.4% converged performance enhancement. SymmQMIX-F, which integrates data augmentation into FEP2Net-QMIX, results in a 10.6-fold improvement in sample efficiency and achieves converged performance comparable to SymmQMIX.

4) Analysis: The above results demonstrate that EP2Nets, hypernetworks, and data augmentation contribute to varying degrees of performance improvement in SymmQMIX. Specifically, EP2Netâs primary role lies in reducing the state-action space by introducing permutation symmetry. In our simulation scenario involving 4 UAVs and 64 GUs, there are a total of $4 ! \times 6 4 ! = 3 \times 1 { \stackrel { \textstyle \smile } { 0 } } ^ { 9 0 }$ permutations. EP2Net, due to its permutation equivariance, learns the optimal policy for all permutations with just one experience sample. This effectively reduces the state-action space by a factor of $\frac { 1 } { 3 { \times } 1 0 ^ { 9 0 } }$ . Data augmentation further enhances sample efficiency by augmenting each experience sample 8-fold through symmetric rotations and reflections. Hypernetworks play a role to enhance model expressiveness. The most substantial performance improvement comes from permutation symmetry, as the redundancy resulting from entity permutations far outweighs that from rotations and reflections. Introducing hypernetworks or data augmentation separately based on EP2Nets can achieve converged performance comparable to SymmQMIX-H. However, the highest sample efficiency is achieved when all three components are combined.

## D. Performance Comparison Across Different Population Sizes

In this section, we further validate the scalability of the proposed symmetry-based MADRL approach by comparing SymmQMIX-H and QMIX under various population sizes. Additionally, to verify the population invariance of EP2Nets, we also evaluate the performance of pre-trained HEP2Nets directly applied to scenarios with different population sizes. The specific configurations are as follows:

<!-- image-->  
Fig. 12. Comparison of the converged fair throughput with respective to the number of GUs. The number of UAVs is set as 2. The pre-trained model was trained in the scenario with 16 GUs.

- Pre-trained HEP2Net: We apply HPE2Nets trained in a scenario with a specific population size to scenarios with varying population sizes. Specifically, for scenarios involving different numbers of GUs, we utilize the model trained with 16 GUs as the pre-trained model. For scenarios involving different numbers of UAVs, the model trained with 6 UAVs are used as the pre-trained model.

First, we fix the number of UAVs at 2, and vary GU count from 4 to 64. Fig. 12 illustrates the performance comparison in terms of total fair throughput after convergence. Notably, SymmQMIX-H consistently outperforms the QMIX algorithm across different GU counts, with this performance advantage increasing as the number of GUs rises. Specifically, as the number of GUs increases from 4 to 64, the fair throughput of SymmQMIX-H steadily ascends from 25.03 Gbits to 28.35 Gbits. In contrast, this metric for QMIX drops from 19 Gbits to 6 Gbits. Consequently, the performance advantage of SymmQMIX-H relative to QMIX increases from 33.8% to a 4.2-fold improvement. The performance degradation of QMIX can be primarily attributed to the explosive state-action space as the number of GUs increases. SymmQMIX-H mitigates this issue by exploiting symmetries, enabling it learn effective policies even in scenarios with a large number of GUs. These results highlight the superior scalability of SymmQMIX-H.

Next, we keep the GU count at 64 while varying the number of UAVs from 2 to 10. The performance comparison is depicted in Fig. 13. With an increase in UAVs, the fair throughput of all algorithms increases with the rising number of UAVs. However, as the number of UAVs increases, the state space expands exponentially, and the cooperation among UAV agents becomes more complex. This complexity makes it challenging for QMIX to learn effective policies. Therefore, when the number of UAVs increases from 2 to 10, the total fair throughput of QMIX only increases from 6 Gbits to 38.7 Gbits. In contrast, the total fair throughput of SymmQMIX-H surges from 28.64 Gbits to

<!-- image-->  
Fig. 13. Comparison of the converged fair throughput with respective to the number of UAVs. The number of GUs is set as 64. The pre-trained model was trained in the scenario with 6 UAVs.

159.4 Gbits. The performance gap remains stable at around 4.5, further emphasizing the scalability of the proposed approach.

Finally, we observe that the pretrained HEP2Net models achieve satisfactory performance in scenarios with different numbers of GUs and UAVs. For instance, with 2 UAVs and 32 GUs, the total fair throughput of the pretrained HEP2Net is only 17.8% lower than learning from scratch (i.e., SymmQMIX), surpassing QMIX by a factor of 2.8. In the scenarios involving 10 UAVs and 64 GUs, the total fair throughput of the pretrained HEP2Net is only 15.4% lower than learning from scratch, outperforming QMIX by twice the margin. While these pre-trained models may exhibit slight performance degradation compared to learning from scratch, they consistently outperform the QMIX algorithm, demonstrating the HEP2Netâs ability to handle varying population sizes.

## VII. CONCLUSION

In this paper, we present a novel symmetry-augmented MADRL approach to solve UAV trajectory design and user scheduling problems. Compared with existing MADRL-based methods, we uniquely incorporate symmetries into both the policy networks and the learning process. The proposed EP2Nets significantly reduce redundancy in the state-action space caused by different permutations. Moreover, the data augmentationbased learning process further enhances sample efficiency by exploiting rotational and reflection symmetries. Extensive simulation results demonstrate the substantial enhancement in both sample efficiency and converged performance achieved by integrating the proposed approach into QMIX algorithm, especially in scenarios involving large population sizes. In future research, we will explore more symmetries within the environment and address situations involving non-ideal symmetries.

## REFERENCES

[1] L. Gupta, R. Jain, and G. Vaszkun, âSurvey of important issues in UAV communication networks,â IEEE Commun. Surveys Tut., vol. 18, no. 2, pp. 1123â1152, Second Quarter, 2016.

[2] H. Wang et al., âJoint resource allocation on slot, space and power towards concurrent transmissions in UAV ad hoc networks,â IEEE Trans. Wireless Commun., vol. 21, no. 10, pp. 8698â8712, Oct. 2022.

[3] H. Zhao, H. Wang, W. Wu, and J. Wei, âDeployment algorithms for UAV airborne networks toward on-demand coverage,â IEEE J. Select. Areas Commun., vol. 36, no. 9, pp. 2015â2031, Sep. 2018.

[4] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â in Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[5] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for Multi-UAV enabled wireless networks,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2109â2121, Mar. 2018.

[6] C. Zhan, Y. Zeng, and R. Zhang, âEnergy-efficient data collection in UAV enabled wireless sensor network,â IEEE Wireless Commun. Lett., vol. 7, no. 3, pp. 328â331, Jun. 2018.

[7] X. Zhang, J. Zhang, J. Xiong, L. Zhou, and J. Wei, âEnergy-efficient Multi-UAV-Enabled multiaccess edge computing incorporating NOMA,â IEEE Internet Things J., vol. 7, no. 6, pp. 5613â5627, Jun. 2020.

[8] C. Shen, T.-H. Chang, J. Gong, Y. Zeng, and R. Zhang, âMulti-UAV interference coordination via joint trajectory and power control,â IEEE Trans. Signal Process., vol. 68, pp. 843â858, 2020.

[9] L. Liu, S. Zhang, and R. Zhang, âCoMP in the sky: UAV placement and movement optimization for multi-user communications,â IEEE Trans. Commun., vol. 67, no. 8, pp. 5645â5658, Aug. 2019.

[10] X. Zhou, X. Zhang, H. Zhao, J. Xiong, and J. Wei, âConstrained soft actor-critic for energy-aware trajectory design in UAV-Aided IoT networks,â IEEE Wireless Commun. Lett., vol. 11, no. 7, pp. 1414â1418, Jul. 2022.

[11] X. Zhang, H. Zhao, J. Wei, C. Yan, J. Xiong, and X. Liu, âCooperative trajectory design of multiple UAV base stations with heterogeneous graph neural networks,â IEEE Trans. Wireless Commun., vol. 22, no. 3, pp. 1495â1509, Mar. 2023.

[12] T. Rashid, M. Samvelyan, C. Schroeder, G. Farquhar, J. Foerster, and S. Whiteson, âQMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning,â in Proc. Int. Conf. Mach. Learn., 2018, pp. 4295â4304.

[13] P. Sunehag et al., âValue-decomposition networks for cooperative multiagent learning,â in Proc. 17th Int. Conf. Auton. Agents Multiagent Syst.â 2018, pp. 2085â2087.

[14] R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, and I. Mordatch, âMultiagent actor-critic for mixed cooperative-competitive environments,â in Proc. Adv. Neural Inf. Process. Syst., 2017, pp. 6379â6390.

[15] L. Yuan, Z. Zhang, L. Li, C. Guan, and Y. Yu, âA survey of progress on cooperative multi-agent reinforcement learning in open environment,â 2023, arXiv:2312.01058.

[16] C. Yan et al., âCollision-avoiding flocking with multiple fixed-wing UAVs in obstacle-cluttered environments: A task-specific curriculumbased MADRL approach,â IEEE Trans. Neural Netw. Learn. Syst., vol. 35, no. 8, pp. 10894â10908, Aug. 2024.

[17] Q. Wang, W. Zhang, Y. Liu, and Y. Liu, âMulti-UAV dynamic wireless networking with deep reinforcement learning,â IEEE Commun. Lett., vol. 23, no. 12, pp. 2243â2246, Dec. 2019.

[18] W. Zhang, Q. Wang, X. Liu, Y. Liu, and Y. Chen, âThree-dimension trajectory design for Multi-UAV wireless network with deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 600â612, Jan. 2021.

[19] Y. Yuan, L. Lei, T. X. Vu, S. Chatzinotas, S. Sun, and B. Ottersten, âEnergy minimization in UAV-Aided networks: Actor-critic learning for constrained scheduling optimization,â IEEE Trans. Veh. Technol., vol. 70, no. 5, pp. 5028â5042, May 2021.

[20] R. Ding, Y. Xu, F. Gao, and X. Shen, âTrajectory design and access control for airâground coordinated communications system with multiagent deep reinforcement learning,â IEEE Internet Things J., vol. 9, no. 8, pp. 5785â5798, Apr. 2022.

[21] X. Zhou et al., âJoint UAV trajectory and communication design with heterogeneous multi-agent reinforcement learning,â Sci. China Inf. Sci., vol. 67, no. 3, pp. 1â21, 2024.

[22] Q. Long, Z. Zhou, A. Gupta, F. Fang, Y. Wu, and X. Wang, âEvolutionary population curriculum for scaling multi-agent reinforcement learning,â in Proc. Int. Conf. Learn. Representations, 2020.

[23] M. Zinkevich and T. R. Balch, âSymmetry in Markov decision processes and its implications for single agent and multiagent learning,â in Proc. 18th Int. Conf. Mach. Learn., 2001, Art. no. 632.

[24] C. Clark and A. Storkey, âTeaching deep convolutional neural networks to play go,â in Proc. 32nd Int. Conf. Mach. Learn., 2015, pp. 1766â1774.

[25] G. N. C. Simm, R. Pinsler, G. CsÃ¡nyi, and J. M. HernÃ¡ndez-Lobato, âSymmetry-aware actor-critic for 3D molecular design,â in Proc. Int. Conf. Learn. Representations, 2021.

[26] E. van der Pol et al., âMDP homomorphic networks: Group symmetries in reinforcement learning,â in Proc. Adv. Neural Inf. Process. Syst., 2020, pp. 4199â4210.

[27] Y. Lin, J. Huang, M. Zimmer, Y. Guan, J. Rojas, and P. Weng, âInvariant transform experience replay: Data augmentation for deep reinforcement learning,â IEEE Robot. Autom. Lett., vol. 5, no. 4, pp. 6615â6622, Oct. 2020.

[28] E. van der Pol, H. van Hoof, F. A. Oliehoek, and M. Welling, âMulti-agent MDP homomorphic networks,â in Proc. Int. Conf. Learn. Representations, 2022.

[29] W. Wang et al., âFrom few to more: Large-scale dynamic multiagent curriculum learning,â in Proc. AAAI Conf. Artif. Intell., 2020, pp. 7293â7300.

[30] Y. Li et al., âPermutation invariant policy optimization for meanfield multi-agent reinforcement learning: A principled approach,â 2021, arXiv:2105.08268.

[31] J. Hao et al., âBoosting multi-agent reinforcement learning via permutation invariant and permutation equivariant networks,â in Proc. Int. Conf. Learn. Representations, 2022.

[32] C. Yan et al., âPASCAL: PopulAtion-Specific curriculum-based MADRL for collision-free flocking with large-scale fixed-wing UAV swarms,â Aerosp. Sci. Technol., vol. 133, 2023, Art. no. 108091.

[33] Y. Xu and W. Yin, âA block coordinate descent method for regularized multiconvex optimization with applications to nonnegativetensor factorization and completion,â SIAM J. Imag. Sci., vol. 6, pp. 1758â1789, 2013.

[34] B. R. Marks and G. P. Wright, âA general inner approximation algorithm for nonconvex mathematical programs,â Operations Res., vol. 26, no. 4, pp. 681â683, 1978.

[35] J. K. Gupta, M. Egorov, and M. Kochenderfer, âCooperative multi-agent control using deep reinforcement learning,â in Proc. Auton. Agents Multiagent Syst., 2017, pp. 66â83.

[36] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction. Cambridge, MA, USA: MIT Press, 2018.

[37] S. Yin and F. R. Yu, âResource allocation and trajectory design in UAVaided cellular networks based on multiagent reinforcement learning,â IEEE Internet Things J., vol. 9, no. 4, pp. 2933â2943, Feb. 2022.

[38] M. Zaheer, S. Kottur, S. Ravanbakhsh, B. Poczos, R. R. Salakhutdinov, and A. J. Smola, âDeep sets,â in Proc. Adv. Neural Inf. Process. Syst., 2017, pp. 3391â3401.

[39] A. Vaswani et al., âAttention is all you need,â in Proc. Adv. Neural Inf. Process. Syst., 2017, pp. 5998â6008.

[40] P. W. Battaglia et al., âRelational inductive biases, deep learning, and graph networks,â 2018, arXiv: 1806.01261.

[41] R. Zhong, X. Liu, Y. Liu, and Y. Chen, âMulti-agent reinforcement learning in NOMA-aided UAV networks for cellular offloading,â IEEE Trans. Wireless Commun., vol. 21, no. 3, pp. 1498â1512, Mar. 2022.

[42] W. R. Scott, Group Theory. North Chelmsford, MA, USA: Courier Corporation, 2012.

[43] D. Ha, A. Dai, and Q. V. Le, âHyperNetworks,â in Proc. Int. Conf. Learn. Representations, 2017.

<!-- image-->

Jun Xiong received the BS and PhD degrees from the National University of Defense Technology (NUDT), China, in 2009 and 2014, respectively. He is currently an associate professor with the College of Electronic Science and Technology, NUDT. His research interests include AI for communications and networking, physical layer security, and cognitive radio networks, where he has published more than 70 refereed articles.

<!-- image-->

<!-- image-->

Haitao Zhao (Senior Member, IEEE) received the BE, MSc and PhD degrees from the National University of Defense Technology (NUDT), China, in 2002, 2004 and 2009 respectively. And he is currently a professor with the Department of Cognitive Communications, College of Electronic Science and Technology at NUDT. Prior to this, he visited the Institute of ECIT, Queenâs University of Belfast, U.K. and Hong Kong Baptist University. His main research interests include wireless communications, cognitive radio networks and self-organized networks, where he has published more than 100 refereed papers. He has served as a TPC member of IEEE ICCâ14-23, Globecomâ16-23, and guest editor for IEEE Communications Magazine.

<!-- image-->

Chao Yan received the BE degree in electrical engineering and automation from the China University of Mining and Technology, Xuzhou, China, in 2017, and the MS and PhD degrees in control science and engineering from the National University of Defense Technology, Changsha, China, in 2019, and 2023, respectively. He was a visiting PhD degree with the School of Mechanical and Aerospace Engineering, Nanyang Technological University, Singapore, from 2021 to 2022. He is currently an associate professor with the College of Automation Engineering, Nanjing

University of Aeronautics and Astronautics, Nanjing, China. His research interests include deep reinforcement learning, coordination control of UAV swarms.

Xuanhan Zhou received the BE and PhD degrees from National University of Defense Technology (NUDT), China, in 2019 and 2024, respectively. Her research interests include UAV-assisted communication system and reinforcement learning.

<!-- image-->

Jibo Wei (Member, IEEE) received the BS and MS degrees in electronic engineering from the National University of Defense Technology (NUDT), Changsha, China, in 1989 and 1992, respectively, and the PhD in electronic engineering degree from Southeast University, Nanjing, China, in 1998. He is currently a professor with the Department of Cognitive Communications at NUDT. His research interests include Software Defined Radios (SDR), wireless network protocol and signal processing in communications, cooperative communication, and cognitive network,

where he has published more than 200 refereed papers. He is a member of IEEE VTS. He is a council member of China Institute of Communications and an editorial committee member of the Journal on Communications.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_3_img_1.jpeg|page_3_img_1]]
3. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_8_img_1.png|page_8_img_1]]
4. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_9_img_1.png|page_9_img_1]]
5. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_10_img_1.jpeg|page_10_img_1]]
6. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_11_img_1.png|page_11_img_1]]
7. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_13_img_1.png|page_13_img_1]]
8. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_18_img_1.jpeg|page_18_img_1]]
9. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_18_img_2.jpeg|page_18_img_2]]
10. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_18_img_3.jpeg|page_18_img_3]]
11. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_18_img_4.jpeg|page_18_img_4]]
12. [[../extracted_images/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc/page_18_img_5.jpeg|page_18_img_5]]

---

