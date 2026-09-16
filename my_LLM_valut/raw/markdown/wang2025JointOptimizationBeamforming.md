# Joint Optimization of Beamforming and Trajectory for UAV-RIS-Assisted MU-MISO Systems Using GNN and SD3

Shumo Wang , Student Member, IEEE, Xiaoqin Song , Tiecheng Song , Member, IEEE, and Yang Yang , Fellow, IEEE

AbstractâIn urban environments, direct communication links between a base station (BS) and user equipment (UEs) are often obstructed by buildings. To mitigate these blockages, we integrate uncrewed aerial vehicles (UAVs) and reconfigurable intelligent surfaces (RISs) to enhance system flexibility and improve transmission efficiency. This paper investigates an RIS-assisted multi-user multiple-input single-output (MU-MISO) downlink system, where the RIS is mounted on a UAV. To maximize the system rate while minimizing the UAVâs energy consumption and flight duration, we formulate a multi-objective optimization problem. To address this problem, we propose a hybrid algorithm that integrates the soft deep deterministic policy gradient (SD3) algorithm with a graph neural network (GNN) architecture, named SD3-GNN-RIS. The original problem is decomposed into two subproblems: joint active beamforming at the BS and passive beamforming at the RIS, optimized via a GNN-based approach, and three-dimensional (3D) UAV trajectory optimization, formulated as a Markov decision process and solved using the SD3 algorithm. Simulation results demonstrate the superior performance of the proposed algorithm compared to baseline methods in terms of system rate, energy efficiency, and UAV trajectory optimization.

Index TermsâUncrewed aerial vehicle, reconfigurable intelligent surface, trajectory optimization, deep reinforcement learning, graph neural network.

Received 8 September 2024; revised 19 March 2025; accepted 15 April 2025. Date of publication 21 April 2025; date of current version 3 September 2025. This work was supported in part by the Postgraduate Research and Practice Innovation Program of Jiangsu Province under Grant SJCX24_0062, in part by the SEU Innovation Capability Enhancement Plan for Doctoral Students under Grant CXJH-SEU24075, in part by the Open Research Fund of National Mobile Communications Research Laboratory, Southeast University under Grant 2024D13, in part by the National Key R&D Program of China under Grant 2024YFE0200500, in part by the Key Research and Development Special Project of School and Local Cooperation in Lvliang under Grant 2023XDHZ18, and in part by the Jinhua Science and Technology Bureau under Grant 2024-4-056. Recommended for acceptance by J. Lee. (Corresponding authors: Tiecheng Song; Xiaoqin Song.)

Shumo Wang and Tiecheng Song are with National Mobile Communications Research Laboratory, Southeast University, Nanjing 211189, China (e-mail: 230238214@seu.edu.cn; songtc@seu.edu.cn).

Xiaoqin Song is with the College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing 211106, China, and also with the National Mobile Communications Research Laboratory, Southeast University, Nanjing 211189, China (e-mail: xiaoqin.song@163.com).

Yang Yang is with the IoT Thrust and the Research Center for Digital World with Intelligent Things (DOIT), Hong Kong University of Science and Technology (Guangzhou), Guangzhou 511453, China, also with Peng Cheng Laboratory, Shenzhen 518055, China, and also with Terminus Group, Beijing 100027, China (e-mail: yyiot@hkust-gz.edu.cn).

Digital Object Identifier 10.1109/TMC.2025.3563072

## I. INTRODUCTION

uncrewed aerial vehicles (UAVs) are increasingly regarded as an encouraging technology for supporting air-to-ground (A2G) communications due to their high mobility, cost-effectiveness, and operational flexibility [1], [2]. When terrestrial infrastructure becomes inaccessible or compromised, UAVs can act as base stations (BSs), delivering communication services to user equipment (UE). The intrinsic flexibility allows for rapid deployment to targeted areas, thereby facilitating essential on-demand coverage [3]. Furthermore, UAVs can function as relays to help mitigate disruptions in wireless networks impeded by dense obstacles, particularly in urban environments [4], [5]. In [6], the three-dimensional (3D) UAV relay trajectory and transmit power are optimized to maximize throughput. Meanwhile, a UAV-assisted vehicular communication environment is considered in [7], and UAV hovering position optimization is studied to enhance system capacity. However, acting as relays requires UAVs to transmit signals from ground terminals at high power, consequently depleting their limited energy resources [8].

Reconfigurable intelligent surfaces (RISs) present an encouraging prospect for concurrently conserving transmission power and enhancing communication performance. RIS is composed of multiple low-cost passive reflectors, which can intelligently adjust incident signals through a controller, thereby reconfiguring the wireless propagation environment [9], [10]. RIS enables the establishment of additional channels between the transmitter and the receiver, making it a favorable option for enhancing transmission performance. Extensive testing is undertaken in [11] to evaluate RIS-assisted communication, demonstrating high potential for RIS in advancing future wireless communication networks. Moreover, [12] considers a multi-user multi-input single-output (MU-MISO) system with the assistance of RIS. The authors propose a joint beamforming optimization method based on an iterative algorithm to maximize the weighted overall throughput. The authors in [13] formulate a joint optimization problem for the BSâs active and RISâs passive coefficients and propose a deep reinforcement learning (DRL) algorithm.

Recently, many researchers are interested in integrating RIS and UAV communication [14], [15], [16]. Particularly in urban settings, exploiting the synergies between RIS and UAVs shows great potential for alleviating building blockage effects and consequently enhancing system rate.

## A. Relate Work

The previous works on the integration of RIS and UAV communication are broadly categorized into two category depending on how RIS is deployed: terrestrial and aerial configurations. In the terrestrial configuration, RISs are primarily mounted on building exteriors to reflect signals between UAVs and UEs. In [17], the RIS is used to enhance communication quality by reflecting signals between UAVs and ground terminals, particularly when direct links between them are obstructed by obstacles. The optimization of the RIS coefficients and UAV trajectory is performed to maximize UAV transfer rates along with minimizing UAV propulsion energy consumption. The scope is extended to multi-UAV scenarios in [18], where joint optimization of computation offloading decision, UAV trajectories, and RIS beamforming is conducted. The authors in [19] utilize tranditional optimization method to simultaneously optimize UAV heights and RIS phase shifts, focusing on improving system throughput performance. In [20], the study addresses an RIS-assisted downlink communication system, which includes a multi-antenna UAV and several UEs. The authors optimize joint transmit beamforming, RIS parameters, and UAV position using an effective algorithm that combines block coordinate ascent with successive convex approximation (SCA). In [21], the authors aim to reduce long-term energy consumption while maintaining system stability by jointly optimizing computing resources, time slot allocation, transmit power, RIS phase angles, and UAV trajectory, and they provide an approximate optimal solution. The authors in [22] employ the non-orthogonal multiple access technique and consider imperfect successive interference cancellation at each UE in an RIS-assisted multi-UAV system, proposing a two-step method to maximize system throughput. The authors in [23] consider mobile multi-user scenarios and propose a multi-agent DRL algorithm to maximize communication coverage and ensure satisfactory average achievable data rates.

In the aerial configuration, RISs are mounted on UAVs to enhance wireless communication quality, a concept known as UAV-RIS [24]. The RIS-assisted communication capability and coverage area can be enhanced by optimizing the position of the UAV-RIS [25]. In [26], a three-node communication model is considered, while UAV trajectory, source power allocation, and RIS beamforming are simultaneously optimized to maximize throughput. The UAV trajectory and RIS coefficients are refined to enhance system throughput while adhering to UAV energy consumption constraints in [27]. In [28], the authors seek to increase average overall throughout by cooperatively adjusting BS beamforming vectors, RIS reflection matrix, and UAV trajectory. The primary problem is divided into three subproblems, which are tackled with block coordinate descent (BCD), semidefinite relaxation (SDR), and SCA. In [29], the authors two DRL algorithms based dueling double deep Qnetwork(D3QN) to optimize the RIS beamforming, BS beamforming and 3D UAV deployment to maximize system energy efficiency. In [30], a multiple-input multiple-output (MIMO) system with RIS assistance is studied, optimizing the average weighted system throughput by jointly designing UE scheduling, UAV trajectory, and beamforming. A tractable 3D channel model for UAV-RIS-assisted networks with UAV jitter is established in [31], where the authors propose two max-min deployment schemes for static UAV-RIS and mobile UAV-RIS. The authors in [32] formulate a problem of maximizing the minimum ergodic rate of UEs and propose an efficient iterative algorithm to jointly optimize multi-BS beamforming, RIS phase shifts, user scheduling, and UAV trajectory using the BCD method. However, the direct path from the BS to UEs is not accounted for in [29], [30], [31], [32].

## B. Motivations

The work of [13], [33] investigates UAV-RIS-assisted MU-MISO systems, focusing primarily on optimizing the active and passive beamforming to maximize system data rate. Nevertheless, the work does not take into account the UAV trajectory, which plays a critical factor for comprehensive system optimization. Furthermore, most existing studies assume the path from UAV-RIS to UEs is line-of-sight (LoS), which is impractical in urban scenarios. The probabilistic LoS model [34], a widely recognized ground-to-air (G2A) channel model, has been utilized in [18], [34], [35] as an alternative approach that accounts for both LoS and Non-LoS (NLoS) paths based on certain probabilities. Nevertheless, in real-world scenarios, the presence of a LoS link should be determined by the practical environmental conditions rather than relying solely on probabilistic or simplified LoS channel models. Furthermore, the majority of existing works on UAV-RIS optimization tend to focus on single-objective optimization, often aiming solely to maximize system throughput. These studies typically overlook the joint consideration of UAV energy consumption and the constraints on the UAVâs starting and ending positions.

Moreover, machine learning-based methods have been increasingly adopted to address the joint optimization problem of BS beamforming and RIS beamforming with lower complexity. In [36], a deep neural network (DNN) model is proposed to design joint beamforming. However, DNNs are generally suited for processing data with fixed structures, such as vectors or matrices, where the output of each neuron relies solely on the input features, failing to effectively leverage the relationships between data points. Additionally, DNNs often require the network structure to be redesigned or retrained when applied to data of varying sizes or structures. To overcome these limitations, graph neural networks (GNNs), which combine graph computation with DNNs, have been proposed for handling irregular data structures. GNNs can process graph data directly, consisting of nodes and edges [37]. Through a message-passing mechanism, they effectively capture both local and global relationships within the graph, enabling the development of more robust strategies [38]. Furthermore, the parameters of GNNs are independent of the number of nodes, enhancing their transferability across graphs of different sizes and structures. A GNN model is proposed in [39] to optimize joint beamforming using uplink pilots, demonstrating its capability to handle complex interdependencies. GNNs have shown potential for achieving high performance, reducing sample complexity and space complexity, and supporting scalability and generalizability across various graph structures [40], [41]. DRL and GNN have exhibited significant potential for improving performance and reducing complexity. However, there is currently a lack of studies that integrate GNN and DRL to jointly optimize BS beamforming, RIS passive beamforming, and UAV trajectory.

TABLE I  
COMPARISON OF RELATED WORKS WITH OUR WORK
<table><tr><td rowspan=1 colspan=2>ParameterReferences</td><td rowspan=1 colspan=1>ChannelModel</td><td rowspan=1 colspan=1>UAVOptimization</td><td rowspan=1 colspan=1>BeamformingOptimization</td><td rowspan=1 colspan=1>BS-UE link</td><td rowspan=1 colspan=1>OptimizationObjective</td><td rowspan=1 colspan=1>OptimizationMethod</td></tr><tr><td rowspan=7 colspan=1>TerrestrialRIS</td><td rowspan=1 colspan=1>Ref. [17]</td><td rowspan=1 colspan=1>ProbabilisticLoS model</td><td rowspan=1 colspan=1>3D UAVtrajectory</td><td rowspan=1 colspan=1>Passivebeamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize UAV transfer ratesand minimize UAV propulsionenergy consumption</td><td rowspan=1 colspan=1>DDQN and DDPG</td></tr><tr><td rowspan=1 colspan=1>Ref.[18]</td><td rowspan=1 colspan=1>ProbabilisticLoS model</td><td rowspan=1 colspan=1>2D UAVtrajectory</td><td rowspan=1 colspan=1>Passivebeamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To minimize the system delayand achieve fairness</td><td rowspan=1 colspan=1>MATD3 and AO</td></tr><tr><td rowspan=1 colspan=1>Ref. [19]</td><td rowspan=1 colspan=1>SimplifiedLoSmodel</td><td rowspan=1 colspan=1>3DUAVPlacement</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize the sum rate</td><td rowspan=1 colspan=1>CG and PSO</td></tr><tr><td rowspan=1 colspan=1>Ref. [20]</td><td rowspan=1 colspan=1>SimplifiedLoS model</td><td rowspan=1 colspan=1>2D UAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize the minimumrate of UEs</td><td rowspan=1 colspan=1>BCA and SCA</td></tr><tr><td rowspan=1 colspan=1>Ref. [21]</td><td rowspan=1 colspan=1>ProbabilisticLoS model</td><td rowspan=1 colspan=1>2D UAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To reduce long-termenergy consumption</td><td rowspan=1 colspan=1>Lyapunav method</td></tr><tr><td rowspan=1 colspan=1>Ref. [22]</td><td rowspan=1 colspan=1>ProbabilisticLoSmodel</td><td rowspan=1 colspan=1>3D UAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize thesystem throughput</td><td rowspan=1 colspan=1>DDQN</td></tr><tr><td rowspan=1 colspan=1>Ref. [23]</td><td rowspan=1 colspan=1>SimplifiedLoSmodel</td><td rowspan=1 colspan=1>3D UAVtrajectory</td><td rowspan=1 colspan=1>Passive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize thecommunication coverage</td><td rowspan=1 colspan=1>Multi-agent DDQN</td></tr><tr><td rowspan=9 colspan=1>AerialRIS</td><td rowspan=1 colspan=1>Ref. [25]</td><td rowspan=1 colspan=1>ProbabilisticLoS model</td><td rowspan=1 colspan=1>3D UAVtrajectory</td><td rowspan=1 colspan=1>Passive beamforming</td><td rowspan=1 colspan=1>Only reflecting link</td><td rowspan=1 colspan=1>To maximize the energy efficiency</td><td rowspan=1 colspan=1>TD3</td></tr><tr><td rowspan=1 colspan=1>Ref. [26]</td><td rowspan=1 colspan=1>SimplifiedLoS model</td><td rowspan=1 colspan=1>2D UAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize the throughput</td><td rowspan=1 colspan=1>Convex optimization</td></tr><tr><td rowspan=1 colspan=1>Ref. [27]</td><td rowspan=1 colspan=1>SimplifiedLoS model</td><td rowspan=1 colspan=1>2DUAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize the minimumrate of UEs</td><td rowspan=1 colspan=1>DDQN</td></tr><tr><td rowspan=1 colspan=1>Ref. [28]</td><td rowspan=1 colspan=1>SimplifiedLoS model</td><td rowspan=1 colspan=1>2D UAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize the average sum rate</td><td rowspan=1 colspan=1>BCD,SDRand SCA</td></tr><tr><td rowspan=1 colspan=1>Ref. [29]</td><td rowspan=1 colspan=1>SimplifiedLoSmodel</td><td rowspan=1 colspan=1>3D UAVplacement</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Only reflecting link</td><td rowspan=1 colspan=1>To maximize systemenergy efficiency</td><td rowspan=1 colspan=1>D3QN</td></tr><tr><td rowspan=1 colspan=1>Ref. [30]</td><td rowspan=1 colspan=1>SimplifiedLoSmodel</td><td rowspan=1 colspan=1>2DUAVplacement</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Only reflecting link</td><td rowspan=1 colspan=1>To maximize the achievanleaverage weighted sum rate</td><td rowspan=1 colspan=1>Conic relaxation,ADMM and SCA</td></tr><tr><td rowspan=1 colspan=1>Ref. [31]</td><td rowspan=1 colspan=1>Tractable3D channel model</td><td rowspan=1 colspan=1>3DUAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Only reflecting link</td><td rowspan=1 colspan=1>To maximize the minimumrate of each UE</td><td rowspan=1 colspan=1>BCD and SCA</td></tr><tr><td rowspan=1 colspan=1>Ref. [32]</td><td rowspan=1 colspan=1>Simplified3D channel model</td><td rowspan=1 colspan=1>2D UAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize the minimumapproximately average ergodic rate</td><td rowspan=1 colspan=1>BCD</td></tr><tr><td rowspan=1 colspan=1>Our work</td><td rowspan=1 colspan=1> 3D urban model</td><td rowspan=1 colspan=1>3D UAVtrajectory</td><td rowspan=1 colspan=1>Both active andpassive beamforming</td><td rowspan=1 colspan=1>Both direct andreflecting link</td><td rowspan=1 colspan=1>To maximize the achievableaverage sum rate,minimizeUAV energy consumption,and reduce flight time slots.</td><td rowspan=1 colspan=1> SD3 and GNN</td></tr></table>

DDQN:Doublpetok;OeatigiCGgateadintSrttatoADeait method of multipliers; See the paper for the full names of other abbreviations in the table.

In this paper, we propose an aerial-RIS-assisted MU-MISO downlink system, where the RIS is mounted on a UAV that flies from an initial position to a final position. We consider an actual 3D urban environment where the paths from the UAV-RIS to UE depend on the real environment. Moreover, while prior studies, such as [42], [43], often focus on maximizing the rate or minimizing UAV energy consumption (or both), we formulate a multi-objective problem to simultaneously maximize the system rate, minimize UAV energy consumption, and reduce flight time slots. As for the UAV trajectory optimization issue, DRL has emerged as a powerful method that can dynamically learn from real-world scenarios. GNN has shown low complexity in optimizing joint active and passive beamforming. We propose a state-of-the-art algorithm that combines the soft deep deterministic policy gradient (SD3) and GNN to address the multi-objective problem by jointly optimizing BS beamforming, RIS passive beamforming, and UAV trajectory.

For clarity, a comparison of our work with related studies is summarized in Table I.

## C. Contribution and Organization

The contributions of this paper can be summarized as follows:

Problem Formulation: We consider a novel UAV-RISassisted MU-MISO downlink system and formulate a multi-objective optimization problem to jointly optimize the active beamforming at the BS, the passive beamforming at the RIS, and the 3D trajectory of the UAV, with the objectives of maximizing the system rate, minimizing the UAVâs energy consumption, and minimizing its flight time slots, subject to the constraint that the UAV travels from its initial position to the destination.

Proposed Solution: To solve the multi-objective optimization problem, we decompose the original problem into two subproblems: the first is joint passive and active beamforming, and the second is 3D UAV trajectory optimization. A GNN-based approach is proposed to optimize the joint passive and active beamforming. Subsequently, an advanced SD3 algorithm is introduced for UAV trajectory optimization.

<!-- image-->  
Fig. 1. Schematic of UAV-RIS-assisted MU-MISO system.

Simulation Results: We provide comprehensive validation through extensive numerical simulations to assess the efficacy of the SD3-GNN-RIS solution. The results reveal that our SD3-GNN-RIS-based solution surpasses existing benchmark solutions regarding system rate.

The structure of this paper is detailed below. We describe the system model and the sum rate maximization problem in Section II. Our proposed SD3-GNN-RIS approach is shown in Section III. Section IV is dedicated to providing simulation results, and the paper concludes with Section V.

## D. Notations

This paper employs the following notations throughout. a, a, and A denote a scalar, a column vector, and a matrix in that order. The notation a[i] refers to the elements from the i-th to the j-th position in a. $( \mathbf { A } ) _ { i , j }$ denotes the element located in the i-th row and j-th column of $\mathbf { A } . \mathbf { A } ^ { T }$ and $\mathbf { A } ^ { H }$ indicate the transpose and conjugate transpose of A in that order.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

As illustrated in Fig. 1, we focus on the downlink transmission of an RIS-assisted MU-MISO system within an urban environment. The BS is outfitted for $N _ { B }$ antennas to concurrently support M single-antenna UEs, which are distributed randomly within a designated area of $D \times D \ m ^ { 2 }$ and represented by $\mathcal { M } = \{ 1 , 2 , . . . , M \}$ . Let $\mathbf { C } _ { B S } = ( x _ { B S } , y _ { B S } , h _ { B S } ) ^ { T }$ and $\mathbf { C } _ { m } = ( x _ { m } , y _ { m } , 0 ) ^ { T }$ represent the positions of the BS and each UE m, respectively. Moreover, to improve the overall system rate, one UAV is outfitted with an RIS comprising K reflective elements to strengthen the communication links from the BS to the UEs.

## A. UAV Movement

Assume the UAV flight period T consists of N time slots, indicated by $\boldsymbol { n } \in \mathcal { N } = \{ 1 , 2 , \dots , N \}$ . Let $\mathbf { C } _ { n } = ( x _ { n } , y _ { n } , h _ { n } ) ^ { T }$ denote the position of the UAV at time slot n, which is computed

from its position at the previous time slot, i.e.,

$$
\begin{array} { r c l } { { } } & { { } } & { { x _ { n } = x _ { n - 1 } + d _ { n } \cos ( \xi _ { n } ) \cos ( \phi _ { n } ) , } } \\ { { } } & { { } } & { { y _ { n } = y _ { n - 1 } + d _ { n } \cos ( \xi _ { n } ) \sin ( \phi _ { n } ) , } } \\ { { } } & { { } } & { { h _ { n } = h _ { n - 1 } + d _ { n } \sin ( \xi _ { n } ) , } } \end{array}\tag{1}
$$

where $d _ { n }$ represents the distance the UAV travels, determined by its speed $v _ { n } \in [ 0 , V _ { m a x } ]$ and the duration of the time slot $\delta _ { n } .$ such that $d _ { n } = v _ { n } \delta _ { n }$ . The azimuth angle and elevation angle are represented by $\xi _ { n }$ and $\phi _ { n }$ , respectively.

Moreover, the UAV can only move within a given geographical region of $D \times D m ^ { 2 }$ and maintain a height between $h _ { m i n }$ and $h _ { m a x }$ . We designate the starting and final coordinates for the entire flight duration to be $\mathbf { C } ^ { 0 }$ and ${ \bf { C } } ^ { T e r }$ , respectively.

## B. Channel Model

Within the RIS-assisted MU-MISO system, the communication channel between the BS and UEs includes two segments: the direct link (BS-UE link) and the reflecting link (BS-RIS-UE link).

1) BS-UE Link: Assume the channel from BS to UE m, $\mathbf { h } _ { m } ^ { d } \in \mathbb { C } ^ { 1 \times N _ { B } }$ , is blocked and modeled as Rayleigh fading, i.e.,

$$
\boldsymbol { h } _ { m } ^ { d } = \beta _ { 0 , m } \tilde { \boldsymbol { h } } _ { m } ^ { d } ,\tag{2}
$$

where $\beta _ { 0 , m }$ represents the pathloss of the direct link from the BS to UE m, determined by the distance between them, $d _ { B S , m } =$ $| | \mathbf { C } _ { B S } - \mathbf { C } _ { m } | |$ , and given in dB by

$$
\beta _ { 0 , m } = 3 2 . 6 + 3 6 . 7 l o g ( d _ { B S , m } ) ,\tag{3}
$$

with $\tilde { \boldsymbol { h } } _ { m } ^ { d } \sim \mathcal { C N } ( \mathbf { 0 } , I )$

2) BS-RIS-UE Link: The reflecting link is composed of the BS-RIS and RIS-UE segments. The likelihood of the LoS link from the BS to the RIS being obstructed is extremely low, due to the flight altitude of the UAV being higher than that of the BS. Consequently, assume the BS-RIS link has a LoS connection and follows a Rician fading model. Then, the channel gain for the BS-RIS link, $\mathbf { G } _ { n } \in \mathbb { C } ^ { \breve { K } \times N _ { B } }$ , is represented as

$$
G _ { n } = \beta _ { n } ^ { B , R } \left( \sqrt { \frac { K _ { 1 } } { 1 + K _ { 1 } } } \tilde { G } _ { n , \mathrm { L O S } } + \sqrt { \frac { 1 } { 1 + K _ { 1 } } } \tilde { G } _ { n , \mathrm { N L O S } } \right) ,\tag{4}
$$

where $K _ { 1 }$ is the Rician factor, $\begin{array} { r } { \beta _ { n } ^ { B , R } = \sqrt { \frac { \alpha } { ( d _ { n } ^ { B , R } ) ^ { \eta } } } } \end{array}$ is the path loss (in dB) from the BS to the RIS. It is determined by the path loss exponent Î·, loss at 1m, Î±, and the distance between them, $d _ { n } ^ { B , R } = | | \mathbf { C } _ { B S } - \mathbf { C } _ { n } | |$ . Moreover, the LoS part and NLoS part are represented by $G _ { n , \mathrm { L O S } }$ and $\bar { G } _ { n , \mathrm { N L O S } }$ , respectively. $\tilde { G } _ { n , \mathrm { N L O S } }$ follows an i.i,d standard Gaussian distribution, i.e., $[ \tilde { G } _ { n , \mathrm { N L O S } } ] _ { i j } \sim \mathcal { C N } ( 0 , 1 ) . \tilde { G } _ { n , \mathrm { L O S } }$ is a function of RIS location. Let $\vartheta _ { 1 , n } ^ { * }$ and $\varphi _ { 1 , n } ^ { * }$ represent the azimuth and elevation angles of arrival (AOA) of the BS, correspondingly. The BS steering vector is then computed as

$$
a _ { \mathrm { B S } } \big ( \vartheta _ { 1 , n } ^ { * } , \varphi _ { 1 , n } ^ { * } \big ) = [ 1 , \ldots , e ^ { j \frac { 2 \pi ( N _ { B } - 1 ) d _ { 0 } } { \lambda _ { c } } \cos ( \vartheta _ { 1 , n } ^ { * } ) \cos ( \varphi _ { 1 , n } ^ { * } ) } ] ,\tag{5}
$$

where $d _ { 0 }$ denotes the spacing between adjacent BS antennas, and $\lambda _ { c }$ represents the carrier wavelength. Additionally, let $\varphi _ { 2 , n } ^ { * }$ and

<!-- image-->  
Fig. 2. 3D map of a dense urban area.

$\vartheta _ { 2 , n } ^ { * }$ represent the azimuth and elevation angles of departure (AoD) from the RIS to the BS. The k-th element of the RIS steering vector aRIS $( \vartheta _ { 2 , n } ^ { \ast } , \varphi _ { 2 , n } ^ { \ast } )$ is then given by

$$
\begin{array} { r l } & { \left[ a _ { \mathrm { R I S } } ( \vartheta _ { 2 , n } ^ { * } , \varphi _ { 2 , n } ^ { * } ) \right] _ { k } } \\ & { \qquad = e ^ { j \frac { 2 \pi d ^ { \mathrm { R I S } } } { \lambda _ { c } } \left\{ i _ { 1 } ( k ) \sin ( \vartheta _ { 2 , n } ^ { * } ) \cos ( \varphi _ { 2 , n } ^ { * } ) + i _ { 2 } ( k ) \sin ( \varphi _ { 2 , n } ^ { * } ) \right\} } , } \end{array}\tag{6}
$$

where $d ^ { \mathrm { R I S } }$ denotes the distance between two adjacent RIS elements, and $i _ { 1 } ( k )$ = mod $( k - 1 , 1 0 )$ , and $i _ { 2 } ( k ) = \lfloor ( k - 1 ) / 1 0 \rfloor$ Then $\tilde { G } _ { n , \mathrm { L O S } }$ is described as

$$
\begin{array} { r } { \tilde { G } _ { n , \mathrm { L O S } } = \mathbf { a } _ { \mathrm { B S } } ( \vartheta _ { 1 , n } ^ { * } , \varphi _ { 1 , n } ^ { * } ) \mathbf { a } _ { \mathrm { R I S } } ( \vartheta _ { 2 , n } ^ { * } , \varphi _ { 2 , n } ^ { * } ) ^ { H } . } \end{array}\tag{7}
$$

Regarding the RIS-UE link, instead of relying on statistical channel models like simplified LoS or probabilistic LoS channels commonly used in other works, we describe the A2G urban channel model using considering realistic structural obstacles [14], [44]. The buildings are spatially designed as a collection of cubes, as depicted in Fig. 2. To determine if the RIS-UE link is obstructed, We check if the link connecting the UAV and the UE intersects any of these cuboids (representing buildings). The RIS-UE link will be classified into either LoS or NLoS transmission based on the locations of the UAV and UEs. The channel from the RIS to UE m is represented as

$$
\mathbf { h } _ { n , m } ^ { R } = \beta _ { n , m } ^ { R } \boldsymbol { \Omega } _ { n , m } ^ { R } ,\tag{8}
$$

where $\beta _ { n , m } ^ { R }$ and $\Omega _ { n , m } ^ { R }$ respect the pathloss and small scale fading, respectively.

$$
\begin{array}{c} \beta _ { n , m } ^ { R } = \bigg \{ P L _ { n , m } ^ { R } + \eta _ { L o S } , \quad \mathrm { i f ~ L o S } ,  \\ { P L _ { n , m } ^ { R } + \eta _ { N L o S } , \quad \mathrm { i f ~ N L o S } , } \end{array}\tag{9}
$$

where $\eta _ { L o S }$ and $\eta _ { N L o S }$ indicate the transmission loss of LoS and NLoS paths, and let $d _ { n , m } ^ { R } = | | \mathbf { C } _ { n } - \mathbf { C } _ { m } | |$ denote the distance from UE m to the UAV, then

$$
P L _ { n , m } ^ { R } = 2 0 \log _ { 1 0 } d _ { n , m } ^ { R } + 2 0 \log _ { 1 0 } f _ { c } + 2 0 \log _ { 1 0 } \left( \frac { 4 \pi } { c } \right) .\tag{10}
$$

The small-scale fading $\Omega _ { n , m } ^ { R }$ is modeled using Rayleigh fading, where $[ \tilde { G } _ { n , \mathrm { N L O S } } ] _ { i j } \sim \mathcal { C N } ( 0 , 1 )$ ). Under LoS propagation scenarios, $\Omega _ { n , m } ^ { R ^ { - } }$ follows a Rician fading model with a factor of

$K _ { 2 } .$ , expressed as

$$
\Omega _ { n , m } ^ { R } = \left( \sqrt { \frac { K _ { 2 } } { 1 + K _ { 2 } } } \tilde { h } _ { n , m } ^ { \mathrm { L O S } } + \sqrt { \frac { 1 } { 1 + K _ { 2 } } } \tilde { h } _ { n , m } ^ { \mathrm { N L O S } } \right) ,\tag{11}
$$

where

$$
\tilde { h } _ { n , m } ^ { \mathrm { L O S } } = \mathbf { a } _ { R I S } ( \vartheta _ { 3 , n } ^ { m } , \varphi _ { 3 , n } ^ { m } ) ,\tag{12}
$$

where $\vartheta _ { 3 , n } ^ { m }$ and $\varphi _ { 3 , n } ^ { m }$ represent the azimuth and elevation AOA from UE m to the RIS. and $\widetilde { h } _ { n , m } ^ { \mathrm { N L O S } }$ is modeled as i.i.d. standard Gaussian distribution, i.e., $[ \tilde { h } _ { n , m } ^ { \mathrm { N L O S } } ] _ { i } \sim \mathcal { C N } ( 0 , 1 )$

Consequently, the channel $\mathbf { h } _ { n , m } ^ { B R U }$ for BS-RIS-UE link can be written as

$$
\mathbf { h } _ { n , m } ^ { B R U } = \mathbf { h } _ { n , m } ^ { R } \boldsymbol { \Theta } _ { n } \mathbf { G } _ { n } ,\tag{13}
$$

where $\Theta _ { n } = \mathrm { d i a g } \{ \theta _ { n } ^ { 1 } , \ldots , \theta _ { n } ^ { k } , \ldots , \theta _ { n } ^ { K } \}$ denotes the RIS phase shift matrix at time slot n, with $\theta _ { n } ^ { k } = \eta _ { n } ^ { k } e ^ { j \vartheta _ { n } ^ { k } }$ . Here, for the k-th reflecting element, $\eta _ { n } ^ { k } \in [ 0 , 1 ]$ denotes the amplitude reflection parameter, and $\vartheta _ { n } ^ { k } \in [ 0 , 2 \pi ]$ indicates the phase shift. The phase shift $\vartheta _ { n } ^ { k }$ is restricted to a discrete range of values because of hardware limitations [45], [46], specifically $\vartheta _ { n } ^ { k } \in$ $\begin{array} { r } { \mathbb { f } = \{ 0 , \frac { 2 \pi \cdot 1 } { 2 ^ { F } } , \dots , \frac { 2 \pi \cdot ( 2 ^ { F } - 1 ) } { 2 ^ { F } } \} } \end{array}$ , where F denotes the quantity of quantization bits. Consequently, phase shift of each RIS element can be adjusted to any of $2 ^ { F }$ possible values.

The achievable rate $R _ { n , m }$ for each UE m at time slot n is represented as

$$
\mathcal { R } _ { n , m } = \log _ { 2 } \left( 1 + \frac { \big | \left( \mathbf { h } _ { m } ^ { d } + \mathbf { h } _ { n , m } ^ { B R U } \right) \mathbf { w } _ { n , m } \big | ^ { 2 } } { \sum _ { i = 1 , i \ne m } ^ { M } \big | \left( \mathbf { h } _ { m } ^ { d } + \mathbf { h } _ { n , m } ^ { B R U } \right) \mathbf { w } _ { n , i } \big | ^ { 2 } + \sigma _ { m } ^ { 2 } } \right) ,\tag{14}
$$

where $\mathbf { w } _ { m } \in \mathbb { C } ^ { N _ { B } \times 1 }$ denotes the active beamforming for UE $m ,$ $\sigma _ { m } ^ { 2 }$ represents the noise variance of the received signal at UE m. The noise follows a zero-mean, circularly symmetric complex Gaussian distribution with variance $\sigma _ { m } ^ { 2 }$

## C. Energy Consumption Model of UAV

For a rotary-wing UAV, the energy model in 3D space can be approximately expressed as follows [42], [43]:

$$
\begin{array} { l } { E ( V ) \approx \displaystyle \int _ { 0 } ^ { T } P ( V ( t ) ) d t + \frac { M _ { U A V } \left( V ( T ) ^ { 2 } - V ( 0 ) ^ { 2 } \right) } { 2 } } \\ { \displaystyle \qquad + M _ { U A V } g \left( H ( T ) - H ( 0 ) \right) } \end{array}\tag{15}
$$

where $V ( t )$ denotes the instantaneous UAV speed at time $t , T$ is the total flight time, $M _ { U A V }$ is the UAV mass, and g is the gravitational acceleration. $H ( T ) - H ( 0 )$ represents the altitude change of the UAV from the initial position to the deployed position. The energy consumption model $P ( V )$ in 2D horizontal space is given by:

$$
\begin{array} { l } { { P ( V ) = P _ { o } \left( 1 + \frac { { 3 V ^ { 2 } } } { { U _ { t i p } ^ { 2 } } } \right) + P _ { I } \left( \sqrt { 1 + \frac { { V ^ { 4 } } } { { 4 v _ { 0 } ^ { 4 } } } } - \frac { { V ^ { 2 } } } { { 2 v _ { 0 } ^ { 4 } } } \right) ^ { \frac { 1 } { 2 } } } } \\ { { \displaystyle ~ + \frac { 1 } { 2 } d _ { 1 } \rho s A V ^ { 3 } } } \end{array}\tag{16}
$$

where $P _ { o }$ is the basic power consumption, $U _ { t i p }$ is the rotor tip speed, $P _ { I }$ is the induced power, $v _ { 0 }$ is a constant related to the UAVâs aerodynamics, and $d _ { 1 } , \rho , s ,$ , and A represent various UAV parameters, such as air density, wing span, and cross-sectional area. Therefore, considering that the UAV maintains an average speed $v _ { n }$ during each time slot, the energy consumption of the rotary-wing UAV over N time slots can be expressed as:

$$
E _ { N } = \sum _ { n = 1 } ^ { N } P ( v _ { n } ) \delta _ { n } + \frac { M _ { U A V } v _ { N } ^ { 2 } } { 2 } + M _ { U A V } g \left( h _ { t e r } - h _ { 0 } \right)\tag{17}
$$

where $h _ { t e r } - h _ { 0 }$ represents the change in altitude from the initial position to the target position.

## D. Problem Formulation

In this study, we investigate a multi-objective optimization problem aimed at optimizing the 3D UAV trajectory C from the starting to the target position, while simultaneously optimizing the active beamforming matrix W of the BS and the passive beamforming matrix Î of the RIS, with the following objectives: maximizing the achievable average sum rate $\begin{array} { r } { { \frac { 1 } { N } } \sum _ { n = 1 } ^ { \tilde { N } } \sum _ { m = 1 } ^ { M } \mathcal { R } _ { n , m } } \end{array}$ , minimizing the total number of time slots N, and reducing the UAVâs energy consumption $E _ { N }$ . To combine these objectives, we adopt a linear weighting approach, where the weight coefficients b and c balance the maximization of the achievable average sum rate and the minimization of the UAVâs energy consumption. A larger value of a weight coefficient indicates a higher relative importance of the corresponding objective. The optimization problem is formulated as follows:

$$
\operatorname* { m a x } _ { \mathbf { W } , \boldsymbol { \Theta } , \mathbf { C } , N } \quad F = - N + b \frac { 1 } { N } \sum _ { n = 1 } ^ { N } \sum _ { m = 1 } ^ { M } \mathcal { R } _ { n , m } - c E _ { N }
$$

s.t.

$$
C 1 : v _ { n } \in [ 0 , V _ { m a x } ] , \forall n
$$

$$
C 2 : \xi _ { n } \in [ - \pi , \pi ] , \forall n
$$

$$
C 3 : \phi _ { n } \in [ - \pi , \pi ] , \forall n
$$

$$
C 4 : h _ { \operatorname* { m i n } } \leq h _ { n } \leq h _ { \operatorname* { m a x } } , \forall n
$$

$$
C 5 : 0 \leq x _ { n } \leq D , \forall n
$$

$$
C 6 : 0 \leq y _ { n } \leq D , \forall n
$$

$$
C 7 : { \bf C } _ { 0 } = { \bf C } ^ { 0 } , { \bf C } _ { N } = { \bf C } ^ { T e r }
$$

$$
C 8 : \vartheta _ { n } ^ { k } \in \{ 0 , \frac { 2 \pi } { 2 ^ { F } } , \ldots , \frac { 2 \pi \cdot ( 2 ^ { F } - 1 ) } { 2 ^ { F } } \} , \forall k , n
$$

$$
C 9 : \sum _ { m = 1 } ^ { M } \| \mathbf { w } _ { n , m } \| ^ { 2 } \leq P _ { \mathrm { B } } , \forall n\tag{18}
$$

where C1 â C6 limit the UAV movement, C7 constrains the UAV to fly from the starting to the final coordinate, C8 specifies the range of the phase shift of all RIS elements, and C9 limits the active beamforming of the BS within the maximum transmit power $P _ { B }$

The above problem involves the joint optimization of UAV trajectory, RIS phase shifts, active beamforming, and time slot allocation, leading to significant computational complexity. The problem is fundamentally non-convex due to the intricate coupling among beamforming, trajectory, and RIS phase shifts, as these variables interact in complex ways [26], [30]. Moreover, the problem involves optimizing both continuous variables (e.g., positions, velocities, beamforming) and discrete variables (e.g., RIS phase shifts), which corresponds to a mixed-integer nonlinear programming (MINLP) problem. Therefore, the problem is NP-hard due to its combinatorial nature, non-convex constraints, and mixed-variable optimization characteristics.

Although convex relaxation techniques, such as SCA and BCD, can be employed, they often lead to suboptimal solutions and rely on strong assumptions that may not hold in practical scenarios, as the UAV system state is dynamically changing, which makes the proposed solutions computationally expensive and challenging to deploy in real-time [17]. Heuristic approaches, such as genetic algorithms and particle swarm optimization, may provide feasible solutions but generally suffer from excessive computational overhead in large-scale networks and require extensive parameter tuning across different scenarios. DRL provides an effective alternative by efficiently handling high-dimensional, sequential decision-making problems [29]. Unlike traditional optimization methods, DRL can learn optimal policies through direct interaction with the environment, adapt to dynamic network conditions, and generalize to previously unseen scenarios. Furthermore, the integration of DRL with GNNs has demonstrated significant potential in improving performance while mitigating computational complexity.

## III. PROPOSED SOLUTION: SD3-GNN-RIS

Combining GNN and DRL, we propose an algorithm named SD3-GNN-RIS. As shown in Fig. 3, our proposed SD3-GNN-RIS framework decomposes the original problem into two subproblems: joint active beamforming at the base station and passive beamforming at the RIS, which is solved using the GNN algorithm, and 3D UAV trajectory optimization, which is addressed using the SD3 algorithm. First, the joint optimization of active and passive beamforming using the GNN model is described.

## A. GNN for Joint Beamforming

Let $\pmb { \theta } _ { n } = [ \theta _ { n } ^ { 1 } , \theta _ { n } ^ { 2 } , \dots , \theta _ { n } ^ { K } ] ^ { H } \in \mathbb { C } ^ { 1 \times K }$ denote the passive beamforming vector of RIS, the channel $\mathbf { h } _ { n , m } ^ { B R U }$ takes the form

$$
\mathbf { h } _ { n , m } ^ { B R U } = \pmb { \theta } _ { n } ^ { H } \mathbf { H } _ { n , m } ,\tag{19}
$$

where $\mathbf { H } _ { n , m } = d i a g ( \mathbf { h } _ { n , m } ^ { R } ) \mathbf { G } _ { n } \in { \mathbb { C } } ^ { K \times N _ { B } }$ denotes the cascaded channel. When the UAV trajectory is fixed, each time slot n, given the UAVâs current position, the joint active and

<!-- image-->  
Fig. 3. Schematic of proposed solution: SD3-GNN-RIS.

passive beamforming can be achieved through

$$
\begin{array} { r l r } {  { \operatorname* { m a x } _ { W _ { n } , \theta _ { n } } \sum _ { k = 1 } ^ { K } \mathcal { R } _ { n , m } } } \\ & { } & { \mathrm { s . t . } \vartheta _ { n } ^ { k } \in \{ 0 , \frac { 2 \pi } { 2 ^ { F } } , \ldots , \frac { 2 \pi \cdot ( 2 ^ { F } - 1 ) } { 2 ^ { F } } \} , \forall k = \{ 1 , \ldots , K \} , } \\ & { } & { \displaystyle \sum _ { m = 1 } ^ { M } \| \mathbf { w } _ { n , m } \| ^ { 2 } \leq P _ { \mathrm { B } } , } \end{array}\tag{20}
$$

where $\mathbf { W } _ { n } = [ \mathbf { w } _ { n , 1 } ^ { T } , \mathbf { w } _ { n , 2 } ^ { T } , \ldots , \mathbf { w } _ { n , M } ^ { T } ] ^ { T } \in \mathbb { C } ^ { N _ { B } \times M }$ denotes active beamforming of BS, which is restricted by the maximum transmit power limit: $\begin{array} { r } { \sum _ { m = 1 } ^ { M } \| \mathbf { w } _ { n , m } \| ^ { 2 } \leq P _ { \mathrm { B } } } \end{array}$

As illustrated in Fig. 3, we create a unweighted, fully connected, undirected graph with M + 1 nodes. This includes one node for one RIS, which learns passive beamforming $\theta _ { n } .$ , and M nodes for the UEs, each of which learns the BS beamforming for their respective UE, $\mathbf { i . e . , w } _ { n , m } , m = 1 , 2 , . . . , M$ . The proposed GNN-based learning structure is composed of an input layer, several update layers, and an output layer.

1) Initial Layer: The initial features of the mth UE node are derived from ${ \bf { H } } _ { n , m } ^ { I }$ using a feature extractor $g _ { u } ^ { ( 0 ) } : \mathbb { R } ^ { 2 N _ { B } ( K + 1 ) \times 1 } \mapsto \mathbb { R } ^ { q \times 1 }$ , where q is an preset parameter, based on the inputs of the GNN model $\{ \mathbf { H } _ { n , m } ^ { I } =$ $[ \mathbf { H } _ { d , m } ^ { T } , \mathbf { H } _ { n , m } ^ { T } ] ^ { T } \} _ { m = 1 , \dots , M }$

$$
\begin{array} { r } { \mathbf { u } _ { m } ^ { ( 0 ) } = g _ { u } ^ { ( 0 ) } ( \left[ \mathfrak { R } ( \mathrm { v e c } ( \mathbf { H } _ { n , m } ^ { \mathrm { I } } ) ) , \mathbb { S } ( \mathrm { v e c } ( \mathbf { H } _ { n , m } ^ { \mathrm { I } } ) ) \right] ^ { \mathrm { T } } ) \in \mathbb { R } ^ { q \times 1 } . } \end{array}\tag{21}
$$

The initial attributes of the RIS node are determined as

$$
{ \bf u } _ { R } ^ { ( 0 ) } = \varphi _ { m e a n } ( \{ { \bf u } _ { m , n _ { B } } ^ { ( 0 ) } \} _ { n _ { B } = 1 , 2 , . . . , N _ { B } , m = 1 , 2 , . . . , M } ) \in \mathbb { R } ^ { q \times 1 } ,\tag{22}
$$

where

$$
\begin{array} { r } { \mathbf { u } _ { m , n _ { B } } ^ { ( 0 ) } = g _ { R } ^ { ( 0 ) } ( \left[ \Re ( ( \mathbf { H } _ { n , m } ^ { \mathrm { I } } [ n _ { B } ] ) ^ { T } , \mathbb { S } ( \mathbf { H } _ { n , m } ^ { \mathrm { I } } [ n _ { B } ] ) ^ { T } \right] ^ { \mathrm { T } } ) \in \mathbb { R } ^ { q \times 1 } , } \end{array}\tag{23}
$$

where $g _ { R } ^ { ( 0 ) } : \mathbb { R } ^ { 2 ( K + 1 ) \times 1 } \mapsto \mathbb { R } ^ { q \times 1 }$ is the feature extractor of RIS node and ${ \bf H } _ { n , m } ^ { \mathrm { I } } [ n _ { B } ]$ denotes the $n _ { B } \cdot$ -th row of ${ \bf { H } } _ { n , m } ^ { \mathrm { I } }$

2) Node Update Layers: Consider the proposed GNN model consists L update layers, the update of RIS node in l-th update layer is

$$
\begin{array} { r } { \mathbf { u } _ { R } ^ { ( l ) } = [ g _ { R } ^ { ( l ) } ( \mathbf { u } _ { R } ^ { ( l - 1 ) } , \varphi _ { m e a n } ( \{ \mathbf { u } _ { m } ^ { ( l - 1 ) } \} _ { m = 1 , 2 , \dots , M } ) , \mathbf { u } _ { R } ^ { ( l - 1 ) } ] } \\ { \in \mathbb { R } ^ { q ( l + 1 ) \times 1 } , } \end{array}\tag{24}
$$

where $g _ { R } ^ { ( l ) } : \mathbb { R } ^ { 2 q l \times 1 } \mapsto \mathbb { R } ^ { q \times 1 }$ is the aggregated function which is intended to combine information from both the UE and RIS nodes. The RIS node receives a uniform share of feature from each UE node through an element-wise mean function. To preserve prior information, the node concatenates features from the previous layer $\mathbf { u } _ { R } ^ { ( l - 1 ) }$

Similarily, The mth UE nodeâs features are revised by

$$
\begin{array} { r } { \mathbf { u } _ { m } ^ { ( l ) } = [ g _ { m } ^ { ( l ) } ( \mathbf { u } _ { m } ^ { ( l - 1 ) } , \varphi _ { m a x } ( \{ \mathbf { u } _ { j } ^ { ( l - 1 ) } \} _ { \forall j \neq m } , \mathbf { u } _ { R } ^ { ( l - 1 ) } ) , \mathbf { u } _ { m } ^ { ( l - 1 ) } ] } \\ { \mathbf { \epsilon } \qquad } \\ { \mathbf { \epsilon } \in \mathbb { R } ^ { q ( l + 1 ) \times 1 } , } \end{array}\tag{25}
$$

where $g _ { m } ^ { ( l ) } : \mathbb { R } ^ { 3 q l \times 1 } \mapsto \mathbb { R } ^ { q \times 1 }$ is the aggregation function designed to combine information from the UE node experiencing dominant interference from other UEs using $\varphi _ { m a x } ,$ along with the RIS node. Additionally, we concatenate features from the preceding layer.

3) Output Layer: There exists an output layer after L update layers, which convert the final attributes of RIS and UE nodes to the active beamforming W and passive beamforming Î¸. This output layer is denoted as

$$
\mathbf { u } _ { R } ^ { ( L + 1 ) } = g _ { R } ^ { ( L + 1 ) } ( \mathbf { u } _ { R } ^ { ( L ) } ) \in \mathbb { R } ^ { 2 K \times 1 } ,\tag{26}
$$

$$
\mathbf u _ { m } ^ { ( L + 1 ) } = g _ { m } ^ { ( L + 1 ) } ( \mathbf u _ { m } ^ { ( L ) } ) \in \mathbb { R } ^ { 2 N _ { B } \times 1 } .\tag{27}
$$

The RIS beamforming $\pmb { \theta } = [ \theta _ { n } ^ { 1 } , \theta _ { n } ^ { 2 } , \dots , \theta _ { n } ^ { K } ] ^ { H }$ is obtained by

$$
\widetilde { \theta } ^ { k } = \frac { \left( u _ { R } ^ { ( L + 1 ) } [ k ] + j u _ { R } ^ { ( L + 1 ) } [ K + k ] \right) } { \sqrt { \left( u _ { R } ^ { ( L + 1 ) } [ k ] \right) ^ { 2 } + \left( u _ { R } ^ { ( L + 1 ) } [ K + k ] \right) ^ { 2 } } } ,\tag{28}
$$

where the phase of Î¸k is continuous, the practical phase $\widetilde { \theta } ^ { k }$ $\theta ^ { k }$ is quantized from $\widetilde { \theta } ^ { k }$ to the nearest discrete value in f .

The BS beamforming vector for user m is given by $\mathbf { w } _ { m } =$ $[ w _ { m , n _ { B } } ] _ { n _ { B } = 1 , . . . , N _ { B } }$ , and is derived as follows:

$$
w _ { m , n _ { B } } = { \bf u } _ { m } ^ { ( L + 1 ) } [ n _ { B } ] + j { \bf u } _ { m } ^ { ( L + 1 ) } [ n _ { B } + N _ { B } ] ,\tag{29}
$$

which is adjusted to comply with the power limitation.

The proposed GNN model undergoes offline training in an unsupervised manner. The training samples are generated based on practical building blockages, with UE and UAV positions randomly placed to produce diverse channel information for training, aiming to enable the trained GNN model to be applied to the training of SD3, facilitating the joint optimization of beamforming and UAV trajectory. To maximize the system throughout align with the design objective, the loss function is designed as

$$
\mathcal { L } = - \sum _ { m = 1 } ^ { M } \mathcal { R } _ { m } .\tag{30}
$$

During testing and deployment, the conventional quantization function is applied.

## B. MDP Formulation

The UAV trajectory optimization problem is reformulated as a Markov Decision Process (MDP) and solved using the DRL algorithm. Treating the UAV as an agent, the state, action, and reward for the UAV trajectory optimization problem are defined as follows:

State: The state of the UAV ${ \bf s } _ { n }$ is composed of three key components, i.e., self-position information $I n f o _ { s e l f }$ target position information $I n f o _ { t a r } ,$ and UE information $I n f o _ { u e } \mathrm { . }$ , denoted as:

$$
\mathbf { s } _ { n } = \{ I n f o _ { s e l f } , I n f o _ { t a r } , I n f o _ { u e } \} ,\tag{31}
$$

In $f o _ { s e l f }$ includes the position of the UAV $\mathbf { C } _ { n } .$ , flight azimuth angle $\xi _ { n }$ , elevation angle $\theta _ { n }$ , and flight speed $v _ { n }$ Mathematically, this can be expressed as:

$$
I n f o _ { s e l f } = \{ { \bf C } _ { n } , \xi _ { n } , \theta _ { n } , v _ { n } \} ,\tag{32}
$$

$I n f o _ { t a r }$ includes the final coordinate of the UAV ${ \bf C } ^ { T e r }$ , the azimuth angle $\xi _ { n } ^ { F }$ and elevation angle $\theta _ { n } ^ { F }$ from the UAV to the final coordinate, and the distance to the final coordinate $d _ { n } ^ { F }$ . This component assists the UAV in navigating towards the final coordinate:

$$
I n f o _ { t a r } = \{ { \bf C } ^ { T e r } , \xi _ { n } ^ { F } , \theta _ { n } ^ { F } , d _ { n } ^ { F } \} ,\tag{33}
$$

$I n f o _ { u e }$ includes the transmission rates of all UEs, which are crucial for the UAV to adjust its flight parameters to

maximize the system rate:

$$
I n f o _ { u e } = \{ \mathcal { R } _ { n , 1 } , \mathcal { R } _ { n , 2 } , . . . , \mathcal { R } _ { n , M } \} .\tag{34}
$$

- Action: The action of the UAV includes the speed $v _ { n }$ , the azimuth angle $\xi _ { n }$ , and the elevation angle $\phi _ { n }$ , denoted as:

$$
\mathbf { a } _ { n } = \{ v _ { n } , \xi _ { n } , \phi _ { n } \} .\tag{35}
$$

Moreover, we apply the normalized representation for the action:

$$
v _ { n } = \lambda _ { v } v _ { m a x } ,\tag{36}
$$

$$
\xi _ { n } = \lambda _ { \xi } \pi ,\tag{37}
$$

$$
\phi _ { n } = \lambda _ { \phi } \pi ,\tag{38}
$$

where $\lambda _ { v } \in [ 0 , 1 ]$ and $\lambda _ { \xi } , \lambda _ { \phi } \in [ - 1 , 1 ]$

- Reward: Our objective comprises three key components: ensuring the UAV reaches its destination in fewer flight time slots, maximizing the total system rate, and minimizing the UAVâs energy consumption. Accordingly, the reward is designed to reflect these objectives and is divided into four components, denoted as:

$$
r _ { n } = a r _ { n } ^ { t a r } + b r _ { n } ^ { u e } + c r _ { n } ^ { e n } + r _ { n } ^ { m o v } ,\tag{39}
$$

where $a , b ,$ and c are coefficients used to balance the importance of the UAV reaching its destination, improving the system rate, and reducing the UAVâs energy consumption. Regarding the objective of ensuring the UAV reaches the final point by the end of the flight period and arrives at the destination in the shortest number of time slots, the agent is unable to receive a positive reward before arriving at the destination. Therefore, there is no reward for reaching the destination in each time slot. Even with initial random exploration included in the reinforcement learning algorithm, the presence of sparse rewards makes it difficult to collect experiential data of the UAV reaching the target point solely through random exploration of actions during the training process. This leads to low training efficiency for the agent. Therefore, reward reshaping is employed to distribute the single-step reward of reaching the target point across each step. The reshaped reward is represented as:

$$
r _ { n } ^ { t a r } = \frac { d _ { n - 1 } ^ { F } - d _ { n } ^ { F } } { v _ { m a x } \delta _ { n } } + \beta _ { p e n a l t y } ,\tag{40}
$$

where $\beta _ { p e n a l t y }$ is a negative value. The UAV receives a negative reward for flying a time slot, thereby encouraging the UAV to reach the target point in fewer time slots.

Moreover, $r _ { n } ^ { u e }$ denotes system rate at time slot n, as follows:

$$
r _ { n } ^ { u e } = \sum _ { m = 1 } ^ { M } \mathcal { R } _ { n , m } ,\tag{41}
$$

At each time slot, BS beamforming and RIS beamforming are applied using the acquired channel state information, with the pre-trained GNN model loaded. The transmission rate $r _ { n } ^ { u e }$ is subsequently computed. This process ensures optimized communication performance for the UAV based on real-time environmental data, leveraging the trained model for efficient beamforming strategies. $\boldsymbol { r } _ { n } ^ { e n }$ denotes the UAVâs energy consumption at each time slot, $r _ { n } ^ { m o v }$ encourages the UAV to avoid collisions with buildings and remain within specified boundaries and altitude limits. If the UAV collides with a building, flies beyond the prescribed range or exceeds the allowable altitude, it will receive a negative reward; otherwise, it will be zero.

## C. The Proposed SD3-GNN-RIS Algorithm

Our proposed SD3-GNN-RIS method is presented in this section. It is based on the SD3 approach, a DRL algorithm utilizing an actor-critic architecture. As shown in Fig. 3, SD3 utilizes two policy networks and two Q networks. The two policy networks generate actions based on the received state, denoted as Ï1 and $\pi _ { 2 } .$ , with parameters $\theta _ { 1 } ^ { a }$ and $\theta _ { 2 } ^ { a }$ , respectively. The Q networks evaluate the action-value function under the actor policy $\pi _ { j } ( \mathbf { s } ; \theta _ { j } ^ { a } ) , j = 1 , 2$ , denoted as $Q _ { 1 }$ and $Q _ { 2 }$ with parameters $\phi _ { 1 }$ and Ï2, respectively. Like most DRL algorithms, our proposed SD3-GNN-RIS algorithm includes two phases: training and testing. The SD3 algorithm incorporates three fundamental techniques commonly employed in DRL during training: experience replay, target networks, and random noise. Additionally, SD3 integrates advanced methodologies, specifically a pair of critic networks and the softmax Q-value approach. The inclusion of dual critic networks mitigates overestimation bias, resulting in more accurate value estimates. Moreover, the application of the softmax Q-value method enhances the stability and convergence of the learning process, thereby improving overall performance. Moreover, the training phase of our proposed algorithm consists of two parts: experience generation, and training and updating the network, as follows.

1) Experence Generation: The UAV observes the state $s _ { n }$ at each time slot n. Leveraging this state information, each actor network generates an action $a _ { n } .$ , as expressed by the equation:

$$
\mathbf { a } _ { n } = \pi _ { j } ( \mathbf { s } _ { n } ) + \mathcal { N } , j = 1 , 2 ,\tag{42}
$$

where N represents Gaussian noise, serving to facilitate the agentâs exploration of a wider range of actions. Subsequently, the UAV receives reward $r _ { n } .$ , and the state transitions to $\mathbf { s } _ { n + 1 }$ The corresponding experience $\left( \mathbf { s } _ { n } , \mathbf { a } _ { n } , r _ { n } , \mathbf { s } _ { n + 1 } , d o n e _ { n } \right)$ is then stored in an experience replay B to facilitate network training.

2) Training and Update the Network: When the number of state transition samples in the experience replay buffer exceeds the predetermined capacity, a mini-batch of B transitions (s, a, r, s , done) is sampled from B for training and updating the network.

The Q network estimates the $Q$ value and is updated through gradient descent to minimize the loss between the target and the predicted Q-value. The target Q-value is denoted as

$$
y _ { j } = r + ( 1 - d o n e ) \gamma \mathrm { s o f t m a x } _ { \beta } \{ Q ( \mathbf { s } ^ { \prime } , \cdot ) \} , \quad j = 1 , 2 ,\tag{43}
$$

where the softmax function is applied, with $\beta$ being its parameter. The softmax function can smooth the optimization landscape

Algorithm 1: Training Phase of Proposed SD3-GNN-RIS   
Algorithm.   
1: Initialize $\mathbf { C } _ { B S }$ and $\mathbf { C } _ { m }$ for m $\overline { { \in \mathcal { M } ; } }$   
2: Initialize two policy network $\pi _ { 1 } ( \mathbf { s } )$ and $\pi _ { 2 } ( \mathbf { s } )$ with pa  
rameters $\theta _ { 1 } ^ { a }$ and $\theta _ { 2 } ^ { a }$ and two Q networks $Q _ { 1 } ( \mathbf { s } , \mathbf { a } )$ and $Q _ { 2 } ( \mathbf { s } , \mathbf { a } )$   
with parameters $\phi _ { 1 }$ and $\phi _ { 2 } ;$   
3: Initialize two target policy network $\pi _ { j } ^ { \prime } ( \mathbf { s } )$ with parameters   
$\theta _ { i } ^ { a ^ { \prime } }  \theta _ { a }$ and two target Q networks $Q _ { 1 } ^ { \prime } ( \mathbf { s } , \mathbf { a } )$ and   
$\tilde { Q } _ { 2 } ^ { \prime } ( \mathbf { s } , \mathbf { a } ) ^ { . }$ with parameters $\phi _ { 1 } ^ { \prime }  \phi _ { 1 }$ and $\phi _ { 2 } ^ { \prime }  \phi _ { 2 } ;$   
4: Initialize experience replay buffer $\begin{array} { r } { B ; { } } \end{array}$   
5: while $i \leq N _ { e p o c h }$ do   
6: Generate $\dot { N _ { b a t c h } }$ UAV positions randomly;   
7: Calculate corresponding $N _ { b a t c h }$ groups of channels   
$\{ \mathbf { h } _ { d , m } , \mathbf { H } _ { n , m } \}$ for $m \in \mathcal { M }$ according to (2) and (13);   
8: Output the continous phase $\{ \widetilde { \theta } ^ { k } \} _ { k = 1 , 2 , \dots , K }$ and BS;   
beamforming W based the proposed GNN model;   
9: Update the parameters of the GNN model using   
backpropagation to minimize the loss;   
10: end   
11: for episode = 1 to $N _ { e p i s o d e }$ do   
12: Initialize the UAV position, joint active and passive   
beamforming, and done flag done = 0;   
13: for $n = 1$ to N do   
14: The UAV recieves the state ${ \bf s } _ { n }$ and selects action   
with Gaussian noise based Ï1 and Ï2; $\pi _ { 1 }$   
15: The UAV excutes the action ${ \bf a } _ { n }$ and apply joint   
beamforming based trained GNN model;   
16: The UAV gets reward $r _ { n } ,$ next state ${ \mathbf { s } } _ { n + 1 } ,$ and   
done flag done;   
17: if done = 1 then the episode is terminated in   
advanced;   
18: end if   
19: Store $( \mathbf { s } _ { n } , \mathbf { a } _ { n } , \mathbf { s } _ { n + 1 } , r _ { n } .$ , done) into $\begin{array} { r } { B ; { } } \end{array}$   
20: if B > 2000 then   
21: for $j = 1 , 2$ do   
22: Sample from B a mini-batch of B experience   
{(s, a, s , r, done)};   
23: Calculate the corresponding action $\hat { \mathbf { a } } _ { j } ^ { \prime }$ in   
state $\mathbf { s } ^ { \prime }$ according to (45);   
24: Calculate sof tmax $; _ { Q }$ according to (44);   
25: Update the critic $\phi _ { j }$ according to (46);   
26: Update the actor $\theta _ { j } ^ { a }$ according to (47);   
27: Update target actor and critic network by   
soft update as (48) and (49);   
28: end for   
29: end if   
30: end for   
31: end for

and empirically facilitate learning, and it is defined as

$$
\begin{array} { r } { \mathrm { s o f t m a x } _ { \beta , j } \left( \hat { Q } ( \mathbf { s } ^ { \prime } , \cdot ) \right) = \frac { \mathbb { E } _ { \hat { \mathbf { a } } _ { j } ^ { \prime } \sim p } \left[ \frac { \exp ( \beta \hat { Q } ( \mathbf { s } ^ { \prime } , \hat { \mathbf { a } } _ { j } ^ { \prime } ) ) \hat { Q } ( \mathbf { s } ^ { \prime } , \hat { \mathbf { a } } _ { j } ^ { \prime } ) } { p ( \hat { \mathbf { a } } _ { j } ^ { \prime } ) } \right] } { \mathbb { E } _ { \hat { \mathbf { a } } _ { j } ^ { \prime } \sim p } \left[ \frac { \exp ( \beta \hat { Q } ( \mathbf { s } ^ { \prime } , \hat { \mathbf { a } } _ { j } ^ { \prime } ) ) } { p ( \hat { \mathbf { a } } _ { j } ^ { \prime } ) } \right] } , } \end{array}\tag{44}
$$

where $p ( \mathbf { a } )$ represents the Gaussian distributionâs probability density function. $\begin{array} { r } { \hat { Q } ( \mathbf { s } ^ { \prime } , \hat { \mathbf { a } } _ { j } ^ { \prime } ) = \operatorname* { m i n } _ { i = 1 , 2 } \{ Q _ { i } ^ { \prime } ( \mathbf { s } ^ { \prime } , \hat { \mathbf { a } } _ { j } ^ { \prime } ) \} } \end{array}$ , and $Q _ { i } ^ { \prime }$ is the target Q network with parameter $\phi _ { i } ^ { \prime } , i = 1 , 2$ . Moreover, $\hat { \mathbf { a } } _ { j } ^ { \prime }$ is the action obtained by adding noise sampled from the Gaussian distribution $\mathcal { N } ( 0 , \tilde { \omega } )$ to the target policy network, and the introduced noise is constrained to ensure that the target remains close to the original action, which is denoted as

<!-- image-->  
Fig. 4. Training convergence of the proposed GNN algorithm under different number of RIS elements.

$$
\hat { \mathbf { a } } _ { j } ^ { \prime } = \pi _ { j } ^ { \prime } \left( \mathbf { s } ^ { \prime } \right) + \epsilon , \epsilon \sim \mathrm { c l i p } ( \mathcal { N } ( 0 , \tilde { \omega } ) , - c , c ) , j = 1 , 2 ,\tag{45}
$$

where $\pi _ { j } ^ { \prime }$ is the target policy network with parameter $\phi _ { j } ^ { \prime }$ . Consequently, the loss function for the critic network is denoted as:

$$
L ( \phi _ { j } ) = \frac { 1 } { B } \sum _ { \bf s } \left[ y _ { j } - Q _ { j } ( { \bf s } , { \bf a } ) \right] ^ { 2 } , ~ j = 1 , 2 .\tag{46}
$$

The actor $\theta _ { j } ^ { a }$ is updated using the policy gradient method, defined as follows:

$$
\frac { 1 } { B } \sum _ { s } \nabla _ { \theta _ { j } ^ { a } } \pi _ { j } ( \mathbf { s } ) \nabla _ { \mathbf { a } } Q _ { j } ( \mathbf { s } , \mathbf { a } ; \phi _ { j } ) \bigg \vert _ { a = \pi _ { j } ( \mathbf { s } ) } .\tag{47}
$$

The target networks are updated using a soft update rule that gradually blends the target network parameters with the current network parameters every d time steps through

$$
\theta _ { j } ^ { a ^ { \prime } } = \tau \theta _ { j } ^ { a } + ( 1 - \tau ) \theta _ { j } ^ { a ^ { \prime } } , ~ j = 1 , 2 ,\tag{48}
$$

$$
\phi _ { j } ^ { \prime } = \tau \phi _ { j } + ( 1 - \tau ) \phi _ { j } ^ { \prime } , \quad j = 1 , 2 ,\tag{49}
$$

where $\tau$ is the updating rate.

The training phase of the proposed SD3-GNN-RIS algorithm is presented in Algorithm 1.

In the testing phase, the UAV loads the trained SD3 model, while the BS and RIS controllers load the trained GNN model. The BS acquires the knowledge of the cascaded channel ${ \bf { H } } _ { n , m }$ and the direct channel $h _ { m } ^ { d }$ . The active and passive beamforming are then adjusted according to the outputs of the GNN model. Subsequently, the BS calculates the achievable rate for each UE, which is then utilized by the UAV. The UAV, along with the state achieved, acts based on the trained SD3 model to determine its flight speed and direction. The test phase of the proposed SD3-GNN-RIS algorithm is outlined in Algorithm 2.

Algorithm 2: Testing Phase of Proposed SD3-GNN-RIS   
Algorithm.   
1: Load the trained GNN model and SD3 model;   
2: for episode = 1 to $N _ { e p i s o d e } ^ { t e s t }$ do   
3: Initialize UAV position and set done flag to   
done = 0;   
4: for $n = 1$ to N do   
5: Apply joint active and passive beamforming using   
the trained GNN model, and the BS calculates   
the achievable rate for each UE;   
6: The UAV recieves the state ${ \bf s } _ { n } ;$   
7: Based on the state $\mathbf { s } _ { n } .$ , the policy networks $\pi _ { 1 } ( \mathbf { s } )$   
and $\pi _ { 2 } ( \mathbf { s } )$ from the trained SD3 model output two   
actions, a1 and $\mathbf { a } _ { 2 } .$ and the corresponding Q-net  
works, $Q _ { 1 } ( \mathbf { s } , \mathbf { a } )$ and $Q _ { 2 } ( \mathbf { s } , \mathbf { a } )$ , output Q-values;   
8: The UAV executes the action with higher Q-value;   
9: The UAV gets next state $\mathbf { s } _ { n + 1 }$ , and done flag done;   
10: if done = 3 then the episode is terminated in   
advanced;   
11: end if   
12: end for   
13: end for

TABLE II SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Thenumber of BSantennas $\overline { { N _ { B } } }$ </td><td rowspan=1 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>Thenumber of RIS elements $\overline { { K } }$ </td><td rowspan=1 colspan=1>100</td></tr><tr><td rowspan=1 colspan=1>The number of quantization bits F</td><td rowspan=1 colspan=1>2 bits</td></tr><tr><td rowspan=1 colspan=1>Noise power $\overline { { \sigma _ { m } ^ { 2 } } }$ </td><td rowspan=1 colspan=1>-80 dBm</td></tr><tr><td rowspan=1 colspan=1>Path loss at 1m</td><td rowspan=1 colspan=1>-20 dB</td></tr><tr><td rowspan=1 colspan=1>Path loss exponentrelated forBS-RIS link</td><td rowspan=1 colspan=1>2.8</td></tr><tr><td rowspan=1 colspan=1>Progagation loss forLoS $\eta _ { L o S }$ </td><td rowspan=1 colspan=1>0.1 dB</td></tr><tr><td rowspan=1 colspan=1>Progagation loss for NLoS $\underline { { \eta _ { N L o S } } }$ </td><td rowspan=1 colspan=1>20 dB</td></tr><tr><td rowspan=1 colspan=1>Rician factor $\overline { { K _ { 1 } } }$ </td><td rowspan=1 colspan=1>10 dB</td></tr><tr><td rowspan=1 colspan=1>The maximum transmit power of BS</td><td rowspan=1 colspan=1>20 dBm</td></tr></table>

## IV. SIMULATION RESULTS

## A. Simultation Settings

We examine an urban area measuring $2 0 0 \times 2 0 0 ~ \mathrm { ~ m } ^ { 2 }$ with building placements determined according to the statistical model in [14], using parameters $\alpha = 0 . 3 , \ \beta = 2 0 0$ buildings/km2, and $\lambda = 5 0 \mathrm { m }$ . The height of the buildings is constrained to $h \in [ 1 0 , 7 0 ]$ m. And the UAV flys on the urban area, the maximum number of time slots is set to $N = 3 0$ , the height of UAV is set as [50,100] m with maximum flight speed $v _ { m a x } = 2 0$ m/s. Moreover, there are 10 users randomly distributed in an urban area. The height of BS is 25m, the position of the BS $\mathbf { C } _ { B S } = ( - 1 0 0 , 1 0 0 , 2 5 ) ^ { T }$ . The initial position of the UAV is set to (194, 194, 50)T , and its destination is set to $( 1 0 , 1 0 , 5 0 ) ^ { T }$ . The initial and destination altitudes of the UAV are set to 50 m. Other parameters about UAV energy consumption in (16) and (17) refer to [47]. Moreover, we assume $d _ { 0 } = 2 \lambda$ c and $d ^ { R I S } = 2 \lambda ,$ c [39]. The major simulation parameters are summarized in Table II.

<!-- image-->  
Fig. 5. Training convergence of the proposed algorithm.

## B. GNN Training and Testing

For the GNN used in joint beamforming optimization, we employ a GNN model with 3 update layers, i.e., L = 3. In the initial layer, $g _ { u } ^ { ( 0 ) }$ consists of two convolutional layers. The first convolutional layer has an input size of $2 N _ { B } ( K + 1 )$ and outputs 2q channels, where $q = 1 2 8$ , with ReLU as the activation function. The second convolutional layer has an input size of 2q and outputs q channels. Following this, global average pooling is applied. On the other hand, $g _ { R } ^ { ( 0 ) }$ consists of two fully connected layers with sizes $2 ( K + 1 ) \times 2 M$ and $2 M \times q ,$ with ReLU as the activation function. For the update layers, $g _ { R } ^ { ( l ) }$ and $g _ { u } ^ { ( l ) }$ both consist of two fully connected layers, with sizes 2ql Ã ql and $q l \times q ,$ , with ReLU as the activation function. As for the readout layers, $g _ { R } ^ { ( l ) }$ and $g _ { u } ^ { ( l ) }$ are simple linear layers with the corresponding sizes.

We implement the proposed network using the deep learning library PyTorch. The neural network is trained using the Adam optimizer with a learning rate of $1 0 ^ { - 3 }$ and weight decay of $1 \bar { 0 } ^ { - 6 }$ . The training process runs for 200 epochs to update the parameters of the neural network, with 512 training samples used to compute the gradients in each iteration. The runtime of the GNN training phase for joint beamforming optimization is 2.18 hours, while the testing phase takes 7.2 seconds for a test sample size of 5,120. In comparison, the DNN training phase requires 2.48 hours, and the testing phase takes 27.4 seconds for the same test sample size. The implementation was performed on a PC running Windows 11, equipped with an Intel Core i7-12700F CPU @ 2.10GHz.

The parameters for the training phase of the SD3-GNN-RIS algorithm are summarized in Table III.

## C. Benchmark Schemes

To assess the performance of the proposed âSD3-GNN-RISâ algorithm, we compare it against the following benchmark algorithms.

TABLE III  
SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Number of GNN update layers (L)</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>Adjustable parameter (q)</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1>Number of training epochs of GNN $\overline { { ( N _ { e p o c h } ) } }$ </td><td rowspan=1 colspan=1>200</td></tr><tr><td rowspan=1 colspan=1>Batch size of GNN</td><td rowspan=1 colspan=1>512</td></tr><tr><td rowspan=1 colspan=1>Discount factor</td><td rowspan=1 colspan=1>0.99</td></tr><tr><td rowspan=1 colspan=1>Learning rate of actor network</td><td rowspan=1 colspan=1> $\overline { { 1 \times 1 0 ^ { - 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Learning rate of critic network</td><td rowspan=1 colspan=1> $\overline { { 1 \times 1 0 ^ { - 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Softmax operatorparameter $\overline { { \beta } }$ </td><td rowspan=1 colspan=1>500</td></tr><tr><td rowspan=1 colspan=1>Batch size of SD3</td><td rowspan=1 colspan=1>256</td></tr></table>

1) SD3-DNN-RIS: In this approach, the BS beamforming and RIS beamforming are managed by a DNN [48]. The SD3 algorithm is adopted to optimize 3D UAV trajectory.

2) SD3-NO-RIS: In this scheme, without RIS assistance, the UAV trajectory is obtained using the SD3 algorithm.

3) TD3-GNN-RIS: TD3 is a cutting-edge method grounded in DRL [49]. To assess the effectiveness of the TD3 algorithm for our problem, we use it to learn the UAV trajectory. Additionally, the joint optimization of BS and RIS beamforming is achieved by our proposed GNN algorithm.

4) TD3-DNN-RIS: In this scheme, the BS beamforming and RIS phase shifts are configured by DNN [48]. Moreover, 3D UAV trajectory is obtained by the TD3 algorithm [49].

5) PPO-GNN-RIS: To assess the effectiveness of the proximal policy optimization (PPO) algorithm [50] for our problem, we use it to learn the UAV trajectory. Additionally, the joint optimization of BS and RIS beamforming is achieved by our proposed GNN algorithm.

6) DDPG-GNN-RIS: To assess the effectiveness of the DDPG algorithm [17] for our problem, we use it to learn the UAV trajectory. Additionally, the joint optimization of BS and RIS beamforming is achieved by our proposed GNN algorithm.

7) SD3-WMMSE-Random: In this scheme, the RIS coefficients are initialized with random value, and the beamforming of BS is optimized by a weight minimum mean square error (WMMSE) optimization form [51]. Moreover, the UAV trajectory is obtained by the SD3 algorithm.

## D. Results and Discussions

Fig. 4 illustrates the sum rate obtained using the proposed GNN algorithm versus the training epoch for varying numbers of RIS elements. The sum rate demonstrates a consistent increase with the progression of training epochs as observed from Fig. 4. The algorithm achieves convergence at approximately 100 epochs. Furthermore, the figure clearly indicates that an enhancement in the sum rate is associated with a rise in the number of RIS elements.

The convergence of the reward for the eight algorithms in terms of smoothed reward, is illustrated in Fig. 5. The coefficients used to balance the importance of the UAV reaching its destination, improving the system rate, and reducing the UAVâs energy consumption are denoted as a, b, and c, with values set to 20, 2, and 0.5, respectively. The smoothing window size is 20. As shown in the figure, the smoothed reward of both TD3-GNN-RIS algorithm and SD3-GNN-RIS algorithm rises with the number of training episodes. The TD3-GNN-RIS algorithm converges at around 50 episodes, while the SD3-GNN-RIS algorithm converges at around 100 episodes. After convergence, the smoothed reward of the SD3-GNN-RIS algorithm is slightly greater compared to the other algorithm.

<!-- image-->  
(a) M is 4.

<!-- image-->  
(b) M is 10.

<!-- image-->  
(c) M is 12.

Fig. 6. 2D UAV trajectory under different number of UEs.  
<!-- image-->  
(a) M is 4.

<!-- image-->  
(b) M is 10.

<!-- image-->  
(c) M is 12.

Fig. 7. 3D UAV trajectory under different number of UEs.  
<!-- image-->  
Fig. 8. Sum rate versus $P _ { B }$ for different algorithms.

<!-- image-->  
Fig. 9. Sum rate versus K for different algorithms.

Figs. 6 and 7 respectively illustrate the 2D and 3D UAV trajectories for the SD3-GNN-RIS and TD3-GNN-RIS algorithm across different amounts of UEs. The yellow star represents the initial position of the UAV, while the blue star represents the UAVâs destination. Fig. 6 shows that the proposed SD3-GNN-RIS algorithm enables UAVs to reach their destination in fewer time steps. Fig. 7 demonstrates that, to maximize the sum reward, our algorithm dynamically adjusts the UAVâs altitude according to environmental conditions, successfully guiding the UAV from its initial position to destination while avoiding collisions with buildings.

<!-- image-->  
Fig. 10. Sum rate versus F for different algorithms.

<!-- image-->

Fig. 11. Sum rate versus M for different algorithms.  
<!-- image-->  
Fig. 12. Energy consumption versus M for different algorithms.

We consider varying maximum transmit power $P _ { B } ,$ , numbers of RIS elements K, phase shift quantization bits F , and numbers of UEs M to analyze the robustness of the algorithms under different scenarios. As depicted in Figs. 8, 9, 10, and 11, By harnessing the strengths of DRL and GNN methods, our proposed SD3-GNN-RIS algorithm reliably exceeds the performance of other algorithms in all scenarios. The rise in sum rate corresponds to the increase in maximum transmit power, as depcited in Fig. 8. A greater sum rate can be obtained with the assistance of RIS, demonstrating the advantage of RIS in enhancing the sum rate. Additionally, SD3-GNN-RIS delivers a greater sum rate than TD3-GNN-RIS, PPO-GNN-RIS, and DDPG-GNN-RIS indicating that SD3 has a greater advantage over TD3, PPO, and DDPG in learning and planning UAV trajectory.

Fig. 9 illustrates how the overall rate varies with varying quantities of RIS elements across various algorithms. Notably, our proposed SD3-GNN-RIS algorithm was trained with 100 RIS elements. Observations indicate that the proposed GNN algorithm is applicable across scenarios with varying numbers of RIS elements without requiring specific training for each different number of RIS elements, as is necessary for DNN algorithms. This demonstrates that the GNN exhibits higher robustness.

Fig. 10 depicts the effectiveness of different algorithms under the discrete constraint of RIS phase shifts, which is suitable for a practical environment. The sum rate for RIS-assisted algorithms improves as the quantity of discrete bits rises. Compared with others, the proposed algorithm consistently delivers better performance. The x-axis is labeled âinf,â indicating the case where phase shifters are adjusted continuously. Importantly, the performance improvements become minimal when the amount of phase shift quantization bits exceeds 5, suggesting that too many phase shifter bits may lead to unnecessary energy consumption for RIS without providing additional benefits.

As the quantity of UEs rises, the overall rate declines, as shown in Fig. 11. The reason is that in RIS-assisted MISO systems, each additional UE introduces more interference to the individual users. Fig. 11 demonstrates that our proposed algorithm surpasses others in handling varying numbers of UEs, exhibiting superior performance regarding the increased overall rate.

Fig. 12 illustrates the energy consumption of various algorithms under different numbers of UEs. The energy consumption is calculated based on the UAVâs velocity, as formulated in (17). The SD3-NO-RIS algorithm achieves the lowest energy consumption as its sole objective is to minimize energy usage, and the UAV trajectory does not impact its sum rate. Although the proposed SD3-GNN-RIS consumes slightly more energy than the SD3-WMMSE-RIS algorithm, as observed in Fig. 11, SD3-GNN-RIS achieves a higher system sum rate at relatively lower energy consumption. Furthermore, SD3-GNN-RIS demonstrates significantly lower energy consumption and higher system sum rates compared to the other three algorithms.

## V. CONCLUSION

In this paper, we investigated an RIS-assisted MU-MISO downlink system, where the RIS is attached to a UAV that flies from the initial position to the end position. We developed a joint optimization approach for the active beamforming of the BS, passive beamforming of the RIS, and 3D UAV trajectory to maximize system rate, minimize the UAVâs energy consumption and flight time slots. We proposed the SD3-GNN-RIS algorithm, which combines a GNN model and the SD3 algorithm. The GNN model is utilized for optimizing joint active and passive beamforming, while the SD3 algorithm is employed to optimize the 3D UAV trajectory. Simulation results illustrate the effectiveness of the proposed algorithm in maximizing the achievable overall rate. Furthermore, if multiple RISs are mounted on multiple UAVs to assist the MU-MISO system, additional improvements can be obtained by collectively optimizing beamforming and UAV trajectories.

## REFERENCES

[1] X. Song, Q. Chen, S. Wang, T. Song, and L. Xu, âHybrid multi-server computation offloading in airâground vehicular networks empowered by federated deep reinforcement learning,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 6, pp. 5175â5189, Nov./Dec. 2024.

[2] C.-X. Wang et al., âOn the road to 6G: Visions, requirements, key technologies, and testbeds,â IEEE Commun. Surv. Tut., vol. 25, no. 2, pp. 905â974, Second Quarter 2023.

[3] C. Zhang, L. Zhang, L. Zhu, T. Zhang, Z. Xiao, and X.-G. Xia, â3D deployment of multiple UAV-mounted base stations for UAV communications,â IEEE Trans. Commun., vol. 69, no. 4, pp. 2473â2488, Apr. 2021.

[4] Z. Na, C. Ji, B. Lin, and N. Zhang, âJoint optimization of trajectory and resource allocation in secure UAV relaying communications for Internet of Things,â IEEE Internet Things J., vol. 9, no. 17, pp. 16284â16296, Sep. 2022.

[5] J. Chen, U. Mitra, and D. Gesbert, â3D urban UAV relay placement: Linear complexity algorithm and analysis,â IEEE Trans. Wireless Commun., vol. 20, no. 8, pp. 5243â5257, Aug. 2021.

[6] Z. Wang, F. Zhou, Y. Wang, and Q. Wu, âJoint 3D trajectory and resource optimization for a UAV relay-assisted cognitive radio network,â China Commun., vol. 18, no. 6, pp. 184â200, 2021.

[7] Y. Su, M. Liwang, Z. Chen, and X. Du, âToward optimal deployment of UAV relays in UAV-assisted internet of vehicles,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13392â13405, Oct. 2023.

[8] S. Ahmed, M. Z. Chowdhury, and Y. M. Jang, âEnergy-efficient UAV relaying communications to serve ground nodes,â IEEE Commun. Lett., vol. 24, no. 4, pp. 849â852, Apr. 2020.

[9] E. Shi et al., âRIS-aided cell-free massive MIMO systems for 6G: Fundamentals, system design, and applications,â Proc. IEEE, vol. 112, no. 4, pp. 331â364, Apr. 2024.

[10] T. Wang, F. Fang, and Z. Ding, âAn SCA and relaxation based energy efficiency optimization for multi-user RIS-assisted NOMA networks,â IEEE Trans. Veh. Technol., vol. 71, no. 6, pp. 6843â6847, Jun. 2022.

[11] R. Zhong, Y. Liu, X. Mu, Y. Chen, and L. Song, âAI empowered RIS-assisted NOMA networks: Deep learning or reinforcement learning?,â IEEE J. Sel. Areas Commun., vol. 40, no. 1, pp. 182â196, Jan. 2022.

[12] W. Jin, J. Zhang, C.-K. Wen, S. Jin, X. Li, and S. Han, âLow-complexity joint beamforming for RIS-assisted MU-MISO systems based on modeldriven deep learning,â IEEE Trans. Wireless Commun., vol. 23, no. 7, pp. 6968â6982, Jul. 2024.

[13] Y. Lin, Y. Shen, and A. Li, âSimultaneous transmission and reflection beamforming design for RIS-aided MU-MISO,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 4040â4045, Mar. 2023.

[14] X. Fan, M. Liu, Y. Chen, S. Sun, Z. Li, and X. Guo, âRIS-assisted UAV for fresh data collection in 3D urban environments: A deep reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 72, no. 1, pp. 632â647, Jan. 2023.

[15] Y. Yu, X. Liu, Z. Liu, and T. S. Durrani, âJoint trajectory and resource optimization for RIS assisted UAV cognitive radio,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13643â13648, Oct. 2023.

[16] J. Sun et al., âLeveraging UAV-RIS reflects to improve the security performance of wireless network systems,â IEEE Netw. Lett., vol. 5, no. 2, pp. 81â85, Jun. 2023.

[17] H. Mei, K. Yang, Q. Liu, and K. Wang, â3D-trajectory and phase-shift design for RIS-assisted UAV systems using deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 71, no. 3, pp. 3020â3029, Mar. 2022.

[18] S. Wang, X. Song, T. Song, and Y. Yang, âFairness-aware computation offloading with trajectory optimization and phase-shift design in RISassisted multi-UAV MEC network,â IEEE Internet Things J., vol. 11, no. 11, pp. 20547â20561, Jun. 2024.

[19] M. Misbah, Z. Kaleem, W. Khalid, C. Yuen, and A. Jamalipour, âPhase and 3-D placement optimization for rate enhancement in RIS-assisted UAV networks,â IEEE Wireless Commun. Lett., vol. 12, no. 7, pp. 1135â1138, Jul. 2023.

[20] N. T. Nguyen et al., âFairness enhancement of UAV systems with hybrid active-passive RIS,â IEEE Trans. Wireless Commun., vol. 23, no. 5, pp. 4379â4396, May 2024.

[21] Z. Yao, Q. Zhu, Y. Zhang, H. Huang, and M. Luo, âMinimizing long-term energy consumption in RIS-assisted UAV-enabled MEC network,â IEEE Internet Things J., early access, Feb. 25, 2025, doi: 10.1109/JIOT.2025.3545252.

[22] R. Tang, J. Wang, Y. Zhang, F. Jiang, X. Zhang, and J. Du, âThroughput maximization in NOMA enhanced RIS-assisted multi-UAV networks: A deep reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 74, no. 1, pp. 730â745, Jan. 2025.

[23] B. A. Tesfaw, R.-T. Juang, H.-P. Lin, G. B. Tarekegn, and W. N. Kabore, âMulti-agent deep reinforcement learning based optimizing joint 3D trajectories and phase shifts in RIS-assisted UAV-enabled wireless communications,â IEEE Open J. Veh. Technol., vol. 5, pp. 1712â1726, 2024.

[24] H. Yang, K. Lin, L. Xiao, Y. Zhao, Z. Xiong, and Z. Han, âEnergy harvesting UAV-RIS-assisted maritime communications based on deep reinforcement learning against jamming,â IEEE Trans. Wireless Commun., vol. 23, no. 8, pp. 9854â9868, Aug. 2024.

[25] B. Adhikari, A. S. Khwaja, M. Jaseemuddin, A. Anpalagan, and A. Nallanathan, âEnergy efficient RIS-assisted UAV networks using twin delayed DDPG technique,â IEEE Trans. Wireless Commun., vol. 23, no. 12, pp. 18423â18439, Dec. 2024.

[26] X. Liu, Y. Yu, F. Li, and T. S. Durrani, âThroughput maximization for RIS-UAV relaying communications,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 10, pp. 19569â19574, Oct. 2022.

[27] H. Zhang, M. Huang, H. Zhou, X. Wang, N. Wang, and K. Long, âCapacity maximization in RIS-UAV networks: A DDQN-based trajectory and phase shift optimization approach,â IEEE Trans. Wireless Commun., vol. 22, no. 4, pp. 2583â2591, Apr. 2023.

[28] Q. Huang, Z. Song, Z. Xiong, G. Xu, N. Zhao, and D. Niyato, âJoint resource and trajectory optimization in active IRS-aided UAV relaying networks,â IEEE Trans. Wireless Commun., vol. 23, no. 10, pp. 13082â13094, Oct. 2024.

[29] Y. Yao, K. Lv, S. Huang, and W. Xiang, â3D deployment and energy efficiency optimization based on DRL for RIS-assisted air-to-ground communications networks,â IEEE Trans. Veh. Technol., vol. 73, no. 10, pp. 14988â15003, Oct. 2024.

[30] S. Li, H. Du, D. Zhang, and K. Li, âJoint UAV trajectory and beamforming designs for RIS-assisted MIMO system,â IEEE Trans. Veh. Technol., vol. 73, no. 4, pp. 5378â5392, Apr. 2024.

[31] J. Liu and H. Zhang, âThroughput optimization in aerial RIS-assisted networks with 3D imperfect reflection,â IEEE Trans. Veh. Technol., early access, Feb. 19, 2025, doi: 10.1109/TVT.2025.3543663.

[32] J. Liu and H. Zhang, âDynamic aerial reconfigurable intelligent surface aided multi-cell multi-user communications,â IEEE Trans. Wireless Commun., vol. 23, no. 11, pp. 16453â16465, Nov. 2024.

[33] A. S. Abdalla and V. Marojevic, âDDPG learning for aerial RIS-assisted MU-MISO communications,â in Proc. IEEE 33rd Annu. Int. Symp. Pers. Indoor Mobile Radio Commun., 2022, pp. 701â706.

[34] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[35] Y. He et al., âAir-to-ground integrated internet of vehicles enhanced by LAPSs and RISs: Location, power, and phase shift optimization,â IEEE Internet Things J., vol. 11, no. 10, pp. 18020â18034, May 2024.

[36] C. Hu, Y. Lu, H. Du, M. Yang, B. Ai, and D. Niyato, âAI-empowered RIS-assisted networks: CV-enabled RIS selection and DNN-enabled transmission,â IEEE Trans. Veh. Technol., vol. 73, no. 11, pp. 17854â17858, Nov. 2024.

[37] J. Guo and C. Yang, âLearning power allocation for multi-cell-multi-user systems with heterogeneous graph neural networks,â IEEE Trans. Wireless Commun., vol. 21, no. 2, pp. 884â897, Feb. 2022.

[38] Y. Shen, J. Zhang, S. H. Song, and K. B. Letaief, âGraph neural networks for wireless communications: From theory to practice,â IEEE Trans. Wireless Commun., vol. 22, no. 5, pp. 3554â3569, May 2023.

[39] T. Jiang, H. V. Cheng, and W. Yu, âLearning to reflect and to beamform for intelligent reflecting surface with implicit channel estimation,â IEEE J. Sel. Areas Commun., vol. 39, no. 7, pp. 1931â1945, Jul. 2021.

[40] B. Zhao and C. Yang, âLearning beamforming for RIS-aided systems with permutation equivariant graph neural networks,â in Proc. IEEE 97th Veh. Technol. Conf., 2023, pp. 1â5.

[41] Z. Wang, Y. Zhou, Y. Zou, Q. An, Y. Shi, and M. Bennis, âA graph neural network learning approach to optimize RIS-assisted federated learning,â IEEE Trans. Wireless Commun., vol. 22, no. 9, pp. 6092â6106, Sep. 2023.

[42] H. Pan, Y. Liu, G. Sun, P. Wang, and C. Yuen, âResource scheduling for UAVs-aided D2D networks: A multi-objective optimization approach,â IEEE Trans. Wireless Commun., vol. 23, no. 5, pp. 4691â4708, May 2024.

[43] H. Pan, Y. Liu, G. Sun, J. Fan, S. Liang, and C. Yuen, âJoint power and 3D trajectory optimization for UAV-enabled wireless powered communication networks with obstacles,â IEEE Trans. Commun., vol. 71, no. 4, pp. 2364â2380, Apr. 2023.

[44] Y. Wang et al., âTrajectory design for UAV-based Internet of Things data collection: A deep reinforcement learning approach,â IEEE Internet Things J., vol. 9, no. 5, pp. 3899â3912, Mar. 2022.

[45] J. Sang et al., âQuantized phase alignment by discrete phase shifts for reconfigurable intelligent surface-assisted communication systems,â IEEE Trans. Veh. Technol., vol. 73, no. 4, pp. 5259â5275, Apr. 2024.

[46] T.-H. Vu and S. Kim, âPerformance analysis of full-duplex two-way RISbased systems with imperfect CSI and discrete phase-shift design,â IEEE Commun. Lett., vol. 27, no. 2, pp. 512â516, Feb. 2023.

[47] G. Sun, J. Li, A. Wang, Q. Wu, Z. Sun, and Y. Liu, âSecure and energy-efficient UAV relay communications exploiting collaborative beamforming,â IEEE Trans. Commun., vol. 70, no. 8, pp. 5401â5416, Aug. 2022.

[48] H. Jiang, L. Dai, M. Hao, and R. MacKenzie, âEnd-to-end learning for RIS-aided communication systems,â IEEE Trans. Veh. Technol., vol. 71, no. 6, pp. 6778â6783, Jun. 2022.

[49] H. Sun, Y. Zhou, J. Tang, Z. Kang, X. Wang, and T. Q. S. Quek, âAverage AoI-minimal trajectory design for UAV-assisted IoT data collection system: A safe-TD3 approach,â IEEE Wireless Commun. Lett., vol. 13, no. 2, pp. 530â534, Feb. 2024.

[50] B. I.-D. Ghomri, M. Y. Bendimerad, and F. T. Bendimerad, âDRL-driven optimization for energy efficiency and fairness in NOMA-UAV networks,â IEEE Commun. Lett., vol. 28, no. 5, pp. 1048â1052, May 2024.

[51] H. Guo, Y.-C. Liang, J. Chen, and E. G. Larsson, âWeighted sum-rate maximization for reconfigurable intelligent surface aided wireless networks,â IEEE Trans. Wireless Commun., vol. 19, no. 5, pp. 3064â3076, May 2020.

<!-- image-->

Shumo Wang (Student Member, IEEE) received the bachelorâs degree from the Nanjing University of Aeronautics and Astronautics, Nanjing, China. She is currently working toward the PhD degree with National Mobile Communications Research Laboratory, Southeast University, Nanjing, China. Her research interests mainly focus on intelligent wireless communications.

<!-- image-->

Xiaoqin Song received the bachelor, master, and PhD degrees in communication engineering from Southeast University, Nanjing, China in 1995, 1998, and 2008, respectively. She was engaged in mobile communication network technology research with Siemens, China in 1999. From 2018 to 2019, she was a visiting scholar with the School of Engineering, University of Toronto. She is currently an associate professor of the College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing, China. She authored six books and more than 60 papers. She holds more than 50 granted patents. Her current research interests include resource allocation, computation offloading, Internet of Vehicles, and wireless networks.

<!-- image-->

Tiecheng Song (Member, IEEE) received the BS degree in radio technology, and the MS and PhD degrees in communication and information system from Southeast University, Nanjing, China, in 1989, 1992, and 2006, respectively. He became an associate professor and a professor with the National Mobile Communications Research Laboratory, Southeast University, in 2000 and 2005, respectively. He has won four times of the Science and Technology Award from Jiangsu Province. He published five books and more than 100 papers. He is the main inventor of more than 20 patents in China. His research interests include cognitive radio, wireless sensor networks, and vehicle networks.

<!-- image-->

Yang Yang (Fellow, IEEE) is a professor with the IoT Thrust, the director of Research Center for the Digital World with Intelligent Things (DOIT), and the associate vice president for teaching and learning with the Hong Kong University of Science and Technology (Guangzhou), China. He is also an adjunct professor with the Department of Broadband Communication, Peng Cheng Laboratory, and the chief scientist of IoT at Terminus Group, China. Before joining HKUST (GZ), he has held faculty positions with the Chinese University of Hong Kong, Brunel University, U.K.,

University College London (UCL), U.K., CAS-SIMIT, and ShanghaiTech University, China. His research interests include multi-tier computing networks, 5 G/6 G systems, AIoT technologies, intelligent services and applications, and advanced wireless testbeds. He has published more than 300 papers and filed more than 120 technical patents in these research areas.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_5_img_1.jpeg|page_5_img_1]]
3. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_7_img_1.jpeg|page_7_img_1]]
4. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_10_img_1.jpeg|page_10_img_1]]
5. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_11_img_1.jpeg|page_11_img_1]]
6. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_12_img_1.jpeg|page_12_img_1]]
7. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_12_img_2.jpeg|page_12_img_2]]
8. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_12_img_3.jpeg|page_12_img_3]]
9. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_12_img_4.jpeg|page_12_img_4]]
10. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_13_img_1.jpeg|page_13_img_1]]
11. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_13_img_2.jpeg|page_13_img_2]]
12. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_13_img_3.jpeg|page_13_img_3]]
13. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_15_img_1.jpeg|page_15_img_1]]
14. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_15_img_2.jpeg|page_15_img_2]]
15. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_15_img_3.jpeg|page_15_img_3]]
16. [[../extracted_images/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3/page_15_img_4.jpeg|page_15_img_4]]

---

