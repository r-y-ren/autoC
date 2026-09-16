# Reconfigurable Intelligent Surface Assisted UAV-MCS Based on Transformer Enhanced Deep Reinforcement Learning

Qianqian Wu , Qiang Liu , Member, IEEE, Ying He , Senior Member, IEEE, and Zefan Wu

AbstractâMobile crowd sensing (MCS) is an emerging paradigm that enables participants to collaborate on various sensing tasks. UAVs are increasingly integrated into MCS systems to provide more reliable, accurate and cost-effective sensing services. However, optimizing UAV trajectories and communication efficiency, especially under non-line-of-sight (NLoS) channel conditions, remains a significant challenge. This paper proposes TRAIL, a Transformer-enhanced deep reinforcement Learning (DRL) algorithm. TRAIL aims to jointly optimize UAV trajectories and Reconfigurable Intelligent Surface (RIS) phase shifts to maximize data throughput while minimizing UAV energy consumption. The optimization problem is modeled as a Markov Decision Process (MDP), where the Transformer architecture captures long-term dependencies in UAV trajectories, and these features are input into a Double Deep Q-Network with Prioritized Experience Replay (PER-DDQN) to guide the agent in learning the optimal strategy. Simulation results demonstrate that TRAIL significantly outperforms state-of-the-art methods in both data throughput and energy efficiency.

Index TermsâUnmanned aerial vehicles (UAVs), mobile crowd sensing (MCS), reconfigurable intelligent surface (RIS), deep reinforcement learning, transformer.

## I. INTRODUCTION

M OBILE Crowd Sensing (MCS) leverages sensors in mo-bile devices such as smartphones to collect information bile devices such as smartphones to collect information at urban scales. Compared to traditional sensor networks, MCS has made significant strides, enabling a range of applications including environmental monitoring, public safety, urban planning, and disaster management [1], [2]. Despite its considerable potential, MCS faces numerous challenges. For instance, traffic monitoring typically requires continuous data collection from specific road segments. However, in practical scenarios, the autonomously planned movement trajectories of participants often fail to meet the spatiotemporal coverage requirements of the platform [3]. Consequently, traditional human-centered MCS models exhibit limitations including restricted spatial coverage, unpredictable user mobility, and high dependence on voluntary participation. These constraints result in incomplete data collection or delays, particularly pronounced in rural or sparsely populated areas.

To address these limitations, unmanned aerial vehicles (UAVs) have been introduced to MCS, driving the development of UAV-assisted mobile crowd sensing (UCS) frameworks [4], [5]. Unlike conventional human-centered MCS, UAVs offer mobility, flexibility, and access to otherwise challenging locations, thereby enhancing data collection through expanded area coverage and ensuring timely data collection [6], [7], [8]. Studies such as [9] and [10] have demonstrated the capability of UAVs to significantly improve data collection rates in various sensing applications, such as disaster response and environmental monitoring. However, UAV mobility, combined with limitations in battery life and communication range, presents challenges in optimizing performance. These challenges are further exacerbated in non-line-of-sight (NLoS) channel conditions, commonly encountered in urban or cluttered environments [11], [12].

Reconfigurable intelligent surfaces (RIS) have recently been demonstrated to enhance the reliability of communication in wireless networks [13], [14]. Composed of passive reflective elements, RIS can be steered and optimize the signal propagation paths by intelligently adjusting the phase shifts of its elements, especially in the NLoS scenarios [15]. Researchers have explored various methods to configure RIS in UAV-assisted systems. For instance, Qin et al. [16] developed an iterative algorithm using Dinkelbachâs method and Block Coordinate Descent (BCD) to optimize bit allocation, transmission power, phase shifts, and UAV trajectories, maximizing the energy efficiency of RIS-assisted UAV systems. Similarly, in [17], a UCS framework leveraging wireless power transfer (WPT) and RIS was proposed to improve transmission efficiency in challenging channel conditions, while optimizing UAV trajectory and beamforming through a BCD algorithm. Other studies, such as [18], have used iterative algorithms to jointly optimize UAV trajectory, transmission power, and RIS phase shifts for energy-efficient UAV-assisted transmissions. However, traditional gradient-based methods often struggle with managing the expanding search space introduced by the increasing number of optimization parameters. To tackle this, deep reinforcement learning (DRL) has been applied to RIS-UAV systems. Chen et al. [19] employed DRL-based methods to jointly optimize UAV trajectory, ground terminal transmission power, subchannel allocation, and RIS phase shifts, enhancing both data rate and convergence performance. In [20], an improved LSTM-DDQN approach was implemented to optimize UAV trajectory, RIS phase shifts, and transmission beamforming to maximize system throughput. Guo et al. [21] proposed a RIS-assisted secure air-to-ground communication framework wherein a robust reinforcement learning method maximizes the minimum multicast rate by optimizing UAV trajectory and beamforming. However, these studies did not consider the onboard battery capacity constraints of UAVs, which critically impact their endurance and performance in practical scenarios. Pursuing this research direction, Liu et al. [22] employed a Dueling Deep Q-Network (D-DQN) algorithm to jointly optimize UAV mobility, RIS phase shifts, power allocation, and dynamic decoding order to minimize UAV energy consumption. Bhagawat et al. [23] utilized the Two-Delay Deep Deterministic Strategy Gradient (TD3) algorithm to optimize RIS phase shifts and 3D trajectories of UAVs, achieving significant energy savings. Since energy efficiency remains one of the key challenges in UAV-enabled systems, a variety of techniques have been proposed to address this issue [24]. For example, Budhiraja et al. [25] focused on maximizing the energy efficiency of the entire network under time-varying channels by jointly optimizing the UAVâs transmission power and the RIS phase shift matrix using the Deep Deterministic Policy Gradient (DDPG) algorithm. Similarly, Mei et al. [26] proposed a DRL-based method for 3D UAV trajectory and RIS phase shift design, aiming to improve energy efficiency in RIS-assisted UAV systems. In [27], a DRL approach was employed to maximize energy efficiency by jointly optimizing the UAVâs power allocation and the RIS phase configuration in a UAV-RIS integrated network. However, the aforementioned studies primarily focus on optimizing the horizontal trajectories of UAVs, without fully exploiting their three-dimensional mobility. Although Mei et al. [26] considered a 3D spatial model, the widely adopted DRL-based algorithms fail to capture the temporal dependencies inherent in historical states and decisions, which limits their performance in dynamic and uncertain environments. Moreover, most of the existing works concentrate on RIS-assisted UAV communication systems, while limited attention has been given to the joint optimization of UAVs and RIS for MCS applications.

To address these limitations, We propose TRAIL, a Transformer-enhanced DRL algorithm designed for UAV mobile crowd sensing within a RIS-UAV framework. By jointly optimizing UAV trajectories and RIS phase configurations, TRAIL aims to maximize data throughput while minimizing UAV energy consumption. We model the task as a Markov Decision Process (MDP) and deploy TRAIL to solve it. The main contributions of this paper can be summarized as follows:

We propose TRAIL, a Transformer-enhanced DRL algorithm that jointly optimizes UAV trajectories and RIS phase shifts, maximizing data throughput and reducing UAV energy consumption.

<!-- image-->  
Fig. 1. RIS-assisted UCS communication scenarios.

We model the optimization problem as an MDP, utilizing the Transformer architecture to capture long-term dependencies in UAV trajectories and get historical information from the memory units. The extracted features are then fed into a DDQN network with prioritized experience replay (PER) for optimal decision-making. The PER mechanism assigns priority to each transition based on temporal difference (TD) error, enhancing the efficiency of the training process.

We compare our method with state-of-the-art solutions. Our algorithm achieves better throughput than all benchmark strategies while reducing UAV energy consumption. The results further demonstrate the superiority of our approach in terms of energy efficiency.

The remainder of the paper consists of the following sections. Section II presents the system model and problem formulation of the paper. Section III introduces the design and implementation details of the TRAIL. Section IV gives simulation results to evaluate the performance of the proposed approach through simulation experiments, and concludes the paper in Section V.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

We consider a downlink wireless communication system assisted by multi-UAVs and a passive RIS. As illustrated in Fig. 1, the target area Q comprises UAVs acting as aerial base stations, an RIS with M passive reflecting elements deployed on the exterior surface of a building, and a set of Points of Interest (PoIs). Both the UAV and the ground PoIs are assumed to be equipped with single antennas.

Let $\mathcal { G } = \{ 1 , 2 , . . . , G \}$ and $\mathcal { U } = \{ 1 , 2 , . . . , U \}$ denote the set of PoIs and UAVs, respectively. The system is modeled in a 3D Cartesian coordinate system with the UAVâs position at time slot n given as $q _ { u } [ n ] = ( x _ { u } [ n ] , y _ { u } [ n ] , H [ n ] )$ $H _ { \mathrm { m i n } } \leq H [ n ] \leq$ $H _ { \operatorname* { m a x } } , n \in N { \stackrel { \Delta } { = } } \{ 1 , . . . , N \}$ . The position of the g-th ground PoI is given by $q _ { g } [ n ] = ( x _ { g } [ n ] , y _ { g } [ n ] )$ , while the RIS is fixed at height $H _ { r }$ and located at $q _ { r } = ( x _ { r } , y _ { r } , H _ { r } )$ . Additionally, we assume that $\delta _ { u } ^ { n }$ denotes the duration of time slot n, which can be made sufficiently small such that $t _ { \mathrm { m i n } } \le \delta _ { u } ^ { n } \le t _ { \mathrm { m a x } }$ . It is also assumed that the real-time reconfiguration delay of the

RIS (including control circuit response and phase switching time) is significantly shorter than $\delta _ { u } ^ { n }$ , ensuring timely phase adjustment within each slot. The total task completion time for the UAV is given by $\begin{array} { r } { \tau = \sum _ { n = 1 } ^ { N } \delta _ { u } ^ { n } } \end{array}$ . For any two UAVs u and $u ^ { \prime } .$ , defining the collision distance as $d _ { c o l l i s i o n }$ [28], the collision condition can be expressed as follows: $\lVert q _ { u } [ n ] - q _ { u ^ { \prime } } [ n ] \rVert \geq$ $d _ { c o l l i s i o n } .$ âu = u- , ân.

## A. Channel Model

In Fig. 1, the RIS provides a reflective link between the UAV and the ground PoIs. The RIS is typically deployed to establish a LoS link, enhancing the communication channel. However, in environments with scatterers such as buildings and trees, NLoS components cannot be ignored, even with RIS deployment. Therefore, the channels between all communication nodes are modeled as Rician channels. The RIS reflection path consists of two links: the LoS link between the UAV and the RIS, and the LoS link between the RIS and the ground PoIs. At time slot n, the channel gain between the UAV and the RIS [29], [30], $h _ { U R } [ n ] \in \mathbb { C } ^ { M \times \mathbf { \breve { 1 } } }$ , is given by:

$$
\begin{array} { l } { { \displaystyle h _ { U R } \left[ n \right] = \sqrt { \rho _ { U R } d _ { U R } ^ { - \alpha _ { 1 } } \left[ n \right] } \left( \sqrt { \frac { \kappa _ { 1 } } { 1 + \kappa _ { 1 } } } h _ { U R } ^ { L o S } \left[ n \right] \right. } } \\ { { \displaystyle \left. + \sqrt { \frac { 1 } { 1 + \kappa _ { 1 } } } h _ { U R } ^ { N L o S } \left[ n \right] \right) } } \end{array}\tag{1}
$$

where $\rho _ { U R }$ represents the path loss at a reference distance of 1m between the UAV and the RIS, $\alpha _ { 1 }$ is the path loss exponent, and $d _ { U R } [ n ] = \sqrt { \left| q _ { u } [ n ] - q _ { r } \right| ^ { 2 } }$ denotes the distance between the UAV and the RIS at time slot n. $\kappa _ { 1 }$ is the Rician factor, with $h _ { U R } ^ { L o S }$ and $h _ { U R } ^ { N L o S }$ representing the LoS and NLoS components, respectively.

$$
h _ { U R } ^ { L o S } = \left[ 1 , e ^ { j \frac { 2 \pi } { \lambda } d \varphi _ { U R } } , . . . , e ^ { j \frac { 2 \pi } { \lambda } ( M - 1 ) d \varphi _ { U R } } \right]\tag{2}
$$

where, ÏUR = cos $\begin{array} { r } { \theta _ { U R } = \frac { l _ { U R } } { d _ { U R } } } \end{array}$ is the cosine of the angle of arrival $\theta _ { U R }$ at the RIS from the UAV, with $l _ { U R }$ representing the horizontal distance between the UAV and the RIS. Î» is the wavelength. The NLoS component $h _ { R G } ^ { N L o S }$ is assumed to follow an independent and identically distributed (i.i.d.) zeromean complex Gaussian distribution with unit variance.

Similarly, the channel gain between the RIS and the ground PoI at time slot n, $h _ { R G } [ n ] \in \mathbb { C } ^ { M \times 1 }$ , is:

$$
\begin{array} { l } { { \displaystyle h _ { R G } \left[ n \right] = \sqrt { \rho _ { R G } d _ { R G } ^ { - \alpha _ { 2 } } \left[ n \right] } \left( \sqrt { \frac { \kappa _ { 2 } } { 1 + \kappa _ { 2 } } } h _ { R G } ^ { L o S } \left[ n \right] \right. } } \\ { { \displaystyle \left. + \sqrt { \frac { 1 } { 1 + \kappa _ { 2 } } } h _ { R G } ^ { N L o S } \left[ n \right] \right) } } \end{array}\tag{3}
$$

where $d _ { R G } [ n ] = \sqrt { \left| q _ { r } - q _ { g } \right| ^ { 2 } }$ denotes the distance between the PoI and the RIS at time slot n. The LoS component $h _ { R G } ^ { L o S }$ is given by:

$$
h _ { R G } ^ { L o S } = \left[ 1 , e ^ { j \frac { 2 \pi } { \lambda } d \varphi _ { R G } } , . . . , e ^ { j \frac { 2 \pi } { \lambda } ( M - 1 ) d \varphi _ { R G } } \right]\tag{4}
$$

where $\varphi _ { R G } = \cos \theta _ { R G }$ represents the cosine of the angle of departure $\theta _ { R G }$ from the RIS to the ground PoI.

Furthermore, the Rician K-factor of the channel can be adjusted based on the elevation angle of the UAV relative to the ground PoIs, as represented by the LoS probability model:

$$
P _ { L o S } = \frac { 1 } { 1 + a \exp \left[ - b \left( \theta - a \right) \right] }\tag{5}
$$

where a and b are environment-specific parameters. Using this LoS probability, the Rician K-factor is modeled as:

$$
\frac { \kappa } { \kappa + 1 } = P _ { L o S }\tag{6}
$$

which leads to the expression:

$$
\kappa = \frac { P _ { L o S } } { 1 - P _ { L o S } } = \frac { 1 } { a \exp ( - b ( \theta - a ) ) }\tag{7}
$$

In addition to the RIS-reflected link, there is a direct UAV-toground (U-G) link, modeled as a Rayleigh fading channel:

$$
h _ { U G } \left[ n \right] = \sqrt { \rho _ { U G } d _ { U G } ^ { - \alpha _ { 3 } } \left[ n \right] } \tilde { h } \left[ n \right]
$$

where $\tilde { h } [ n ]$ is the random scattering component, which follows a zero-mean complex Gaussian distribution with unit variance.

The received signal y at the PoI is given by:

$$
y = \sqrt { P } \left( h _ { U G } \left[ n \right] + h _ { R G } [ n ] ^ { H } \Theta \left[ n \right] h _ { U R } \left[ n \right] \right) x + n\tag{8}
$$

where $P$ is the transmission power of the base station, with x being the transmitted signal to the PoI. $\Theta [ n ] =$ diag $\left\{ e ^ { j \theta _ { 1 } \left[ n \right] } , e ^ { j \theta _ { 2 } \left[ n \right] } , . . . , e ^ { j \theta _ { M } \left[ n \right] } \right\}$ represents the phase shift matrix of the M reflecting elements at time slot n. To facilitate practical implementation, we assume that each RIS element can adopt only a finite set of discrete phase shift values [31], [32]. These values are obtained by uniformly quantizing the interval $[ 0 , 2 \pi )$ . In actual deployment, the RIS phase shift quantization step is determined by the control circuit. Let b represent the number of bits for phase shift levels D, where $D = 2 ^ { b }$ , and $b = 1$ indicates that the RIS adopts 1-bit discrete phase shifts. Accordingly, the set of discrete phase shifts for each RIS unit is given by:

$$
\theta _ { m } [ n ] \in \{ 0 , \Delta \theta _ { m } [ n ] , . . . , ( D - 1 ) \Delta \theta _ { m } [ n ]\tag{9}
$$

where $\Delta \theta _ { m } [ n ] = 2 \pi / D$

The achievable rate at the ground PoI is influenced by both the direct U-G link and the indirect U-R-G link. Therefore, the achievable rate during time slot n is:

$$
R _ { U G } [ n ] = B \log _ { 2 } \left( 1 + { \frac { P _ { u } \left| h _ { U G } [ n ] + h _ { R G } [ n ] ^ { H } \Theta [ n ] h _ { U R } [ n ] \right| ^ { 2 } } { \sigma ^ { 2 } } } \right)\tag{10}
$$

Where B is the channel bandwidth and $P _ { u }$ is the transmit power of the UAV.

At time slot $n ,$ the achievable rate at the ground PoI is $R _ { U G } [ n ]$ . The throughput $T h _ { g } [ n ]$ can be expressed as the product of the link rate $R _ { U G } [ n ]$ and the time slot duration $\delta _ { u } ^ { n }$

$$
T h _ { g } [ n ] = R _ { U G } [ n ] \cdot \delta _ { u } ^ { n }\tag{11}
$$

## B. Energy Model

The UAVâs energy consumption comprises both propulsion and communication energy. According to [32], [33], we can obtain the blade power $P _ { b p }$ , induced power $P _ { i p }$ and parasitic power $P _ { p p }$

$$
\left\{ \begin{array} { l l } { P _ { b p } = P _ { 0 } \left( 1 + \frac { 3 ( v _ { u } ) ^ { 2 } } { U _ { t i p } ^ { 2 } } \right) } \\ { P _ { i p } = P _ { 1 } \left( \sqrt { 1 + \frac { ( v _ { u } ) ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } - \frac { ( v _ { u } ) ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } } \right) ^ { \frac { 1 } { 2 } } } \\ { P _ { p p } = \frac { 1 } { 2 } d _ { 0 } \imath \varsigma G ( v _ { u } ) ^ { 3 } } \\ { P _ { u } ^ { f l y } = P _ { b p } + P _ { i p } + P _ { p p } } \end{array} \right.\tag{12}
$$

where $P _ { 0 }$ and $P _ { 1 }$ are the power coefficients related to hovering and induced power; $U _ { \mathrm { t i p } }$ is the blade tip speed, $v _ { 0 }$ is the induced velocity during hover, $d _ { 0 }$ and Ï represent the fuselage drag and solidity ratios, and Ä± is the air density. Based on the UAV rotorcraft power consumption model, we can get the propulsion energy:

$$
E _ { u } ^ { f l y } [ n ] = T _ { u } ^ { \mathrm { f l y } } [ n ] P _ { u } ^ { f l y }\tag{13}
$$

where $\begin{array} { r } { T _ { u } ^ { \mathrm { f l y } } [ n ] = \frac { l _ { u } } { v _ { u } } } \end{array}$ denotes the time required for the UAV to fly a distance $l _ { u }$ at a constant speed $v _ { u } . ~ l _ { u } \in [ 0 , l _ { m a x } ] .$ $l _ { m a x }$ represents the maximum flight distance of UAV u in the time slot.

The UAVâs total energy consumption is:

$$
E _ { u } ^ { t o t a l } = \sum _ { n = 1 } ^ { N } \left( E _ { u } ^ { f l y } [ n ] + E _ { u } ^ { c o m m } [ n ] \right)\tag{14}
$$

The energy consumed for propulsion accounts for the vast majority of the total energy consumption (typically exceeding 95%), making the proportion of communication energy consumption negligible. To satisfy the energy constraint, we require: $E _ { u } ^ { t o t a l } < E _ { m a x } . ~ E _ { m a x }$ is battery capacity.

We use Î· to represent the relationship between throughput and energy consumption, i.e., energy efficiency. We can get:

$$
\eta = \frac { T h _ { g } \left[ n \right] } { E _ { u } ^ { f l y } [ n ] + E _ { u } ^ { c o m m } [ n ] }\tag{15}
$$

## C. Problem Definition

The objective is to maximize throughput while minimizing the UAVâs energy consumption by optimizing both the $\mathrm { U A V } _ { \mathrm { \Delta } }$ trajectory and the RIS phase shifts $\theta _ { m } [ n ]$ at each time slot n. The optimization problem is:

$$
\mathbf { P 1 } \colon \operatorname* { m a x } _ { \mathbf { \phi } _ { \in [ n ] , q _ { u } [ n ] } } \eta\tag{16}
$$

$$
s . t . \quad H _ { \mathrm { m i n } } \leq H \leq H _ { \mathrm { m a x } } ,
$$

$$
q _ { u } [ n ] \in \mathcal { Q } , \quad \forall n\tag{16a}
$$

$$
\| q _ { u } [ n ] - q _ { u ^ { \prime } } [ n ] \| > d _ { c o l l i s i o n } , \quad \forall u \neq u ^ { \prime } , \forall n\tag{16b}
$$

$$
R _ { U G } [ n ] \geq R _ { m i n } [ n ] ,\tag{16c}
$$

(16d)

$$
\sum _ { n = 1 } ^ { N } \left( E _ { u } ^ { f l y } [ n ] + E _ { u } ^ { c o m m } [ n ] \right) \leq E _ { \operatorname* { m a x } } ,\tag{16e}
$$

$$
| \Theta | = 1\tag{16f}
$$

where Eq. (16a) and Eq. (16b) indicate that the UAV must fly within a specified range. 16c represents the distance between UAVs to prevent collisions. 16d denotes the minimum rate requirement to guarantee QoS. 16e specifies that the UAVâs energy consumption must be less than its battery capacity. 16f requires that the RIS amplitude must be 1, ensuring that the RIS performs passive reflection without amplifying the received signals. Given that the objective function is nonconvex and Eq. (16c)-(16f) are also non-convex, P1 constitutes a non-convex mixed-integer nonlinear programming (MINLP) problem. While traditional optimization techniques such as Successive Convex Approximation (SCA) could be applied to P1, these methods typically entail high computational complexity and are unsuitable for real-time or online deployment.

## III. TRANSFORMER-ENHANCED DRL ALGORITHM

In this section, we formulate equation (16) as an MDP process and propose the TRAIL algorithm to solve the formulated problem.

## A. MDP Process

We model the joint optimization of the UAV trajectory and RIS phase shifts as a MDP. The MDP process is defined by a tuple $( \mathcal { S } , \mathcal { A } , \mathcal { P } , \mathcal { R } )$ ,

1) State: The state space S is defined as $\boldsymbol { s } \triangleq \boldsymbol { s } | \boldsymbol { n } |$ . The state $s [ n ]$ includes the phase shift values $\theta _ { m } [ n ] \in [ 0 , \hat { 2 \pi } ]$ for each reflecting element, as well as the UAVâs position $q [ n ] =$ $( x [ n ] , y [ n ] , \bar { H [ n ] } )$ .

2) Action: The action space A comprises the phase shift adjustments $\Delta \theta _ { m } [ n ] \in \left\{ - \frac { \bar { \pi } } { 2 } , 0 , \frac { \pi } { 2 } \right\}$ for each reflecting element, the UAVâs movement direction and distance $\triangle q \in$ $\{ ( - 1 , 0 ) , ( 0 , - 1 ) , ( 0 , 0 ) , ( 1 , 0 ) , ( 0 , 1 ) \}$

3) Reward: The reward function $R ( s [ n ] , a [ n ] )$ quantifies the immediate reward obtained by taking action a[n] in state s[n]. Given problem P, the reward for the state-action pair $( s [ n ] , a [ n ] )$ at time slot n can be defined as: $R ( s [ n ] , a [ n ] ) = \eta - p _ { 0 }$ . p0 is the penalty for the UAV going out of bounds or experiencing a collision.

## B. Transformer-Enhanced PER-DDQN Algorithm

In this section, the TRAIL algorithm employs a Transformer encoder to extract the temporal features of the UAV flight trajectory and utilizes a prioritized experience replay-based DDQN to learn the optimal state-action value function.

In dynamic and non-stationary environments, the value estimates in the UCS tend to have high variance. The Transformer effectively captures long-term dependencies in sequential data to mitigate this issue. As shown in Fig. 2, we introduce two gated transformer blocks (Tx Block) to extract temporal features from past UAV trajectories. At time slot $n ,$ the input to the Transformer is the UAVâs state sequence $s _ { 1 } = ( s [ 1 ] , . . . , s [ n ] )$ ï¼ where each state $s _ { i }$ is mapped to a d-dimensional embedded vector $e _ { i } \in \mathbb { R } ^ { d }$ via an embedding layer E:

$$
e _ { i } = \mathbf { E } ( s _ { i } ) , \forall i = 1 , 2 , . . . , n\tag{17}
$$

<!-- image-->  
Fig. 2. Proposed algorithm: TRAIL. The UAV state is combined with positional encoding and fed into a transformer block. This block captures sequence patterns in UAV movement. The output guides action selection, producing Q-values, depending on the reinforcement learning algorithm. Selected actions are executed, and network parameters are updated with prioritized experience replay.

Next, a positional encoding $p _ { i } \in \mathbb { R } ^ { d }$ is added to the embedded vector to obtain the position-encoded state representation $\mathbf { x } _ { i } \mathbf { : }$

$$
\mathbf { x } _ { i } = e _ { i } + p _ { i } , \forall i = 1 , 2 , . . . , n\tag{18}
$$

Once this process is completed, the resulting data is input to the Transformer encoder. Each Transformer block consists of a multi-head self-attention (MSA) block, two layer normalization layers, and a MLP block. Layer normalization is applied before the MSA and MLP blocks. For the h-th attention head, the query matrix $\mathbf Q _ { h }$ , key matrix ${ \bf K } _ { h }$ , and value matrix ${ \bf V } _ { h }$ are given by:

$$
\begin{array} { r } { \mathbf { Q } _ { h } = \mathbf { X } \mathbf { W } _ { h } ^ { Q } } \\ { \mathbf { K } _ { h } = \mathbf { X } \mathbf { W } _ { h } ^ { K } } \\ { \mathbf { V } _ { h } = \mathbf { X } \mathbf { W } _ { h } ^ { V } } \end{array}\tag{19}
$$

where $\mathbf { X } = ( \mathbf { x } [ 1 ] , \ldots , \mathbf { x } [ n ] ) \in \mathbb { R } ^ { n \times d }$ is the position-encoded state sequence, and $\mathbf { W } _ { h } ^ { Q } , \mathbf { \bar { W } } _ { h } ^ { K } , \mathbf { W } _ { h } ^ { V } \in \mathbb { R } ^ { d \times d _ { h } }$ are the projection matrices for attention head $h ,$ with $d _ { h } = d / H$ being the dimension of each attention head, and H is the number of attention heads.

The attention operation for each head is then computed as:

$$
\mathbf { Z } _ { h } = \operatorname { s o f t m a x } \left( { \frac { \mathbf { Q } _ { h } \mathbf { K } _ { h } ^ { T } } { \sqrt { d _ { h } } } } \right) \mathbf { V } _ { h }\tag{20}
$$

The outputs from all attention heads are concatenated and passed through a linear layer to obtain the output of the multihead self-attention:

$$
\mathbf { Z } = ( \mathbf { Z } _ { 1 } \oplus . . . \oplus \mathbf { Z } _ { H } ) \mathbf { W } ^ { O }\tag{21}
$$

where $\oplus$ denotes concatenation, and $\mathbf { W } ^ { O } \in \mathbb { R } ^ { d \times d }$ is the output projection matrix.

Additionally, we introduce a GRU layer $\mathrm { G R U } ( \cdot , \cdot )$ to control the attention of the current state on the historical states. The output of the GRU layer is given by:

$$
\mathbf { G } = \operatorname { G R U } ( \mathbf { Z } , \mathbf { X } ) = \sigma ( \mathbf { Z } \mathbf { W } ^ { G } + \mathbf { X } \mathbf { U } ^ { G } )\tag{22}
$$

where $\sigma ( \cdot )$ is the sigmod activation function, and ${ \bf W } ^ { G } , { \bf U } ^ { G } \in$ $\mathbb { R } ^ { d \times d }$ are the gating layer parameters.

The output of the gating layer is multiplied element-wise with the output of the multi-head attention:

$$
\mathbf { Z } ^ { \prime } = \mathbf { Z } \odot \mathbf { G }\tag{23}
$$

Finally, the output of the Transformer encoder is obtained by applying layer normalization and a feedforward neural network:

$$
\begin{array} { r l } & { \mathbf { Z } ^ { \prime \prime } = \operatorname { L a y e r N o r m } ( \mathbf { Z } ^ { \prime } + \mathbf { X } ) } \\ & { \mathbf { O } = \operatorname { F F N } ( \mathbf { Z } ^ { \prime \prime } ) } \end{array}\tag{24}
$$

where LayerNorm(Â·) denotes layer normalization, and FFN(Â·) represents the feedforward neural network.

Algorithm 1 summarizes the process of using the Transformer encoder to process the state sequence and generate input features for the DDQN.

To improve the sample efficiency and accelerate convergence, we introduce the PER mechanism. PER ranks the samples in the experience pool based on their TD-error, thus prioritizing the training of samples that contribute more to network updates.

In the experience pool, the priority $p _ { i }$ of experience $e _ { i } =$ $( s _ { 1 : n , i } , a _ { i } , r _ { i } , s _ { 1 : n , i } ^ { \prime } )$ is defined based on its TD-error Î´ $\delta _ { i } \mathbf { : }$

$$
p _ { i } = | \delta _ { i } | + \epsilon\tag{25}
$$

where $\delta _ { i }$ is the TD-error, and  is a small positive constant ensuring that all experiences have a non-zero probability of being sampled.

Algorithm 1: State Encoding Using Transformer.   
Input: State sequence $\mathbf { s } _ { 1 : n } ,$ position encoding function,   
and Transformer parameters.   
Output: Encoded state representation $\mathbf { o } [ n ] .$   
for each state $s _ { i }$ in sequence $\mathbf { s } _ { 1 : n }$ do   
Map $s _ { i }$ to embedding vector using an embedding   
layer;   
Add position encoding to obtain position-aware   
state representation;   
for each attention head $h = 1 , \ldots , H$ do   
Compute query, key, and value matrices;   
Compute the output of the gated attention head;   
Concatenate the outputs of all attention heads;   
Pass through the Transformer encoder to obtain   
encoded state representation $\mathbf { o } [ n ] ;$

The sampling probability is computed based on the priority:

$$
\mathcal { P } ( e _ { i } ) = \frac { p _ { i } ^ { \xi } } { \sum _ { j } p _ { j } ^ { \xi } }\tag{26}
$$

where $\xi$ controls the degree of priority influence.

The weighted update of experiences is implemented via importance sampling weights to reduce sampling bias:

$$
w _ { i } = \left( \frac { 1 } { B } \cdot \frac { 1 } { \mathcal { P } ( e _ { i } ) } \right) ^ { \beta }\tag{27}
$$

where $\boldsymbol { B }$ is the size of the experience pool, and $\beta$ controls the strength of importance sampling.

Each time an experience is stored in the buffer, its priority $p _ { i }$ is calculated and used for sampling and updating during training. The priorities of experiences in the buffer are continuously adjusted to ensure sufficient learning from different types of experiences.

Using the Transformer encoder output ${ \mathbf o } [ n ]$ as the input to the DDQN, the outputs of the online and target networks are given by:

$$
Q _ { \theta } \big ( s _ { 1 : n } , a \big ) = w _ { \theta } ^ { T } \mathrm { R e L U } ( \mathbf { W } _ { \theta } \mathbf { o } [ n ] + b _ { \theta } )\tag{28}
$$

where $\mathbf { W } _ { \theta } \in \mathbb { R } ^ { d \times d }$ and $b _ { \theta } \in \mathbb { R } ^ { d ^ { \prime } }$ are the parameters of the Q-network, and $w _ { \theta } ^ { T } \in \mathbb { R } ^ { d ^ { \prime } }$ is the output layer weight, with $d ^ { \prime }$ being the dimension of the hidden layer in the Q-network. Similarly, the target Q-network $Q _ { \phi }$ is given by:

$$
Q _ { \phi } ( s _ { 1 : n } , a ) = w _ { \phi } ^ { T } \mathrm { R e L U } ( \mathbf { W } _ { \phi } \mathbf { o } [ n ] + b _ { \phi } )\tag{29}
$$

For each experience $( s _ { 1 : n } , a , r , s _ { 1 : n } ^ { \prime } )$ sampled with PER, the target Q-value is computed as:

$$
y = r + \gamma Q _ { \phi } ( s _ { 1 : n } ^ { \prime } , \arg \operatorname* { m a x } _ { a ^ { \prime } } Q _ { \theta } ( s _ { 1 : n } ^ { \prime } , a ^ { \prime } ) )\tag{30}
$$

where $\gamma$ is the discount factor. The TD-error is minimized to update the parameters of the online Q-network $Q _ { \theta } \colon$

$$
\mathcal { L } ( \theta ) = \mathbb { E } _ { ( s _ { 1 : n } , a , r , s _ { 1 : n } ^ { \prime } ) \sim \mathcal { D } _ { \operatorname { P E R } } } \left[ w _ { i } \cdot ( y - Q _ { \theta } ( s _ { 1 : n } , a ) ) ^ { 2 } \right]\tag{31}
$$

Every few steps, the parameters of the online network are copied to the target network: $\phi  \theta .$ Algorithm 2 summarizes the decision-making process of the PER-DDQN algorithm.

Algorithm 2: PER-DDQN Algorithm.   
Input: Encoded state representation ${ \mathbf o } [ n ]$ , parameters of   
online Q-network $Q _ { \theta }$ , target Q-network $Q _ { \phi } ,$ and   
replay buffer D.   
Output: Optimized policy Ï.   
Initialize: Initialize $Q _ { \theta } , Q _ { \phi } ,$ and prioritized replay   
buffer $\mathcal { D } ;$   
for each episode do   
Reset environment and obtain initial state   
representation $\mathbf { o } [ 1 ] ;$   
for each time slot $n = 1 , \ldots , N$ do   
Select action a[n] using -greedy policy based   
on $Q _ { \theta } ( \mathbf { o } [ n ] , \mathbf { a } ) ;$   
Execute a[n], observe reward $r [ n ]$ , and next   
state s $\{ [ n + 1 ] \}$   
Encode the next state $\mathbf { s } [ n + 1 ]$ into $\mathbf { o } [ n + 1 ]$   
using the Transformer encoder;   
Compute TD error $\delta ;$   
Store transition $( \mathbf { o } [ n ] , \mathbf { a } [ n ] , r [ n ] , \mathbf { o } [ n + 1 ] )$ in D   
with priority $p _ { i } = | \delta | + \epsilon ;$   
Sample a batch of transitions from $\mathcal { D } ;$   
Compute importance-sampling weights wi;   
Compute target Q-value y and update $Q _ { \theta }$ by   
minimizing weighted TD error;   
Update $Q _ { \phi }$ with $Q _ { \theta } \mathrm { { ^ { \circ } s } }$ parameters

## C. Complexity Analysis

The computational complexity of the TRAIL algorithm is primarily determined by the Transformer encoder and PERbased DDQN. Let l denote the length of the state sequence and d the embedding dimension. The Transformer encoderâs complexity is $O ( l ^ { 2 } d + l d ^ { 2 } )$ . For the PER-DDQN component, sampling from the prioritized experience replay buffer requires O(log |B|) operations, where |B| represents the size of the experience buffer. The computational complexity of the DDQN process is $O ( d ^ { 2 } + d \cdot | { \mathcal { A } } | )$ , where |A| is the action space size. Therefore, the overall training complexity of the proposed algorithm is:

$$
O ( l d ^ { 2 } + l ^ { 2 } d + \log \mathcal { B } + d ^ { 2 } + d \cdot | \mathcal { A } | )\tag{32}
$$

Table II presents the computational complexity of four DRL methods, shown as the time cost for executing a single action per time step. In some large or complex UAV systems, the control loop frequency may decrease to 10-20HZ (with a cycle time of 50-100 ms) [34]. It can be observed that the TRAIL algorithm completes each iteration within milliseconds, well below the typical UAV control cycle time (approximately 100 ms), which is acceptable in real-world UAV operations. Particle swarm optimization(PSO), while capable of obtaining optimal solutions, exhibits significantly higher execution time compared to other methods, particularly running approximately 105 times slower than TRAIL.

TABLE I TABLE OF NOTATIONS
<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>g,u</td><td rowspan=1 colspan=1>Set of PoIs, UAVs.</td></tr><tr><td rowspan=1 colspan=1>Q</td><td rowspan=1 colspan=1>Target area</td></tr><tr><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=1>Number of time slots</td></tr><tr><td rowspan=1 colspan=1> $\delta _ { u } ^ { n }$ </td><td rowspan=1 colspan=1>Duration of each time slot</td></tr><tr><td rowspan=1 colspan=1> $q _ { u } [ n ]$ </td><td rowspan=1 colspan=1>UAV&#x27;s position at time slot n</td></tr><tr><td rowspan=1 colspan=1> $H _ { \mathrm { m i n } } ,$  $H _ { \mathrm { m a x } }$ </td><td rowspan=1 colspan=1>Minimum/Maximum UAV height</td></tr><tr><td rowspan=1 colspan=1> $H _ { r }$ </td><td rowspan=1 colspan=1>Height of the RIS</td></tr><tr><td rowspan=1 colspan=1> $\theta _ { m } [ n ]$ </td><td rowspan=1 colspan=1>Phase shift of the m-th element of the RIS attime slot n</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>Number of RIS elements</td></tr><tr><td rowspan=1 colspan=1> $h _ { U R / R G / U G } [ n ]$ </td><td rowspan=1 colspan=1>Channel gain</td></tr><tr><td rowspan=1 colspan=1>PUR/RG/UG[n]</td><td rowspan=1 colspan=1>Path loss</td></tr><tr><td rowspan=1 colspan=1> $\kappa _ { 1 / 2 }$ </td><td rowspan=1 colspan=1>Rician K-factor for the UAV-RIS/RIS-grounduser channel</td></tr><tr><td rowspan=1 colspan=1>P</td><td rowspan=1 colspan=1>Transmit power</td></tr><tr><td rowspan=1 colspan=1>å¥</td><td rowspan=1 colspan=1>Wavelength of the transmitted signal</td></tr><tr><td rowspan=1 colspan=1> $P _ { L o S }$ </td><td rowspan=1 colspan=1>Probability of the LoS link</td></tr><tr><td rowspan=1 colspan=1> $E _ { \mathrm { u a v } } ^ { \mathrm { f l y } }$ </td><td rowspan=1 colspan=1>UAV propulsion energy consumption</td></tr><tr><td rowspan=1 colspan=1> $E _ { \mathrm { u a v } } ^ { \mathrm { c o m m } }$ </td><td rowspan=1 colspan=1>UAV communication energy</td></tr><tr><td rowspan=1 colspan=1> $\overline { { E _ { u } ^ { \mathrm { t o t a l } } } }$ </td><td rowspan=1 colspan=1>Total UAV energy consumption</td></tr></table>

TABLE II

COMPUTATIONAL COMPLEXITY BY TIME COST (MS)
<table><tr><td>Method</td><td>Times (ms)</td></tr><tr><td>SDRGN-Based Method[10] DDQN-Based Method [26]</td><td>2.98 1.26</td></tr><tr><td>DGRL-Based Method [35]</td><td>2.04</td></tr><tr><td>PSO Methods TRAIL</td><td>423.12 4.03</td></tr></table>

IV. NUMERICAL RESULTS AND DISCUSSIONS

In this section, we evaluate the proposed TRAIL algorithm and compare it with several state-of-the-art methods.

## A. Simulation Setup

The simulation experiments were conducted on a workstation equipped with an Intel Core i9-13900K processor, and the proposed method was implemented using Python 3.7 and PyTorch 1.7.0. We considered a target area of 1000 Ã 1000 meters, where 200 PoIs were randomly distributed. The RIS was configured with M = 60 reflecting elements to assist communication. The default number of UAVs is 4, with each drone flying at a constant velocity of $v [ n ] = 2 5$ m/s in each time slot n, and operating at altitudes ranging between 10m and 100m. The total available bandwidth was B = 2 MHz , and the noise power was $\sigma ^ { 2 } = - 1 6 9$ dBm. The discount factor was set to 0.96, and the buffer size was $1 0 ^ { 5 }$ . Other hyperparameters used in the simulation are listed in Table III. We trained the TRAIL algorithm over 5000 episodes, periodically storing the model weights. During the validation phase, we loaded the pre-trained model and selected actions based on the observed current state to evaluate the modelâs performance in a new environment (the environment was reset for testing purposes).

TABLE III  
EXPERIMENTS PARAMETERS OF SETTINGS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Values (units)</td></tr><tr><td rowspan=1 colspan=1>Length of area</td><td rowspan=1 colspan=1>1 (km)x1 (km)</td></tr><tr><td rowspan=1 colspan=1>Flight height</td><td rowspan=1 colspan=1>10-100 (m)</td></tr><tr><td rowspan=1 colspan=1>Flight speed</td><td rowspan=1 colspan=1>25 (m/s)</td></tr><tr><td rowspan=1 colspan=1>The number of UAVs</td><td rowspan=1 colspan=1>Range from 2 to 5,the default settingis4</td></tr><tr><td rowspan=1 colspan=1>The number of PoIs</td><td rowspan=1 colspan=1>Range from170 to 220,the defaultsetting is 200</td></tr><tr><td rowspan=1 colspan=1>Noise power Ï</td><td rowspan=1 colspan=1>-169 (dBm/Hz)</td></tr><tr><td rowspan=1 colspan=1>Channel power gain</td><td rowspan=1 colspan=1>-60 (dB)</td></tr><tr><td rowspan=1 colspan=1>The rotor disc area G</td><td rowspan=1 colspan=1>0.503m2</td></tr><tr><td rowspan=1 colspan=1>The tip speed of therotor blade $\underline { { U _ { t i p } } }$ </td><td rowspan=1 colspan=1>120m/s</td></tr><tr><td rowspan=1 colspan=1>The rotor solodity so</td><td rowspan=1 colspan=1>0.05</td></tr><tr><td rowspan=1 colspan=1>The air density</td><td rowspan=1 colspan=1>1.225K $\overline { { g / m ^ { 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1>MLP layers</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>Discount factor</td><td rowspan=1 colspan=1>0.96</td></tr><tr><td rowspan=1 colspan=1>Learning rate</td><td rowspan=1 colspan=1>1Ã10-5</td></tr><tr><td rowspan=1 colspan=1>Batch size</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \xi , \beta } }$ </td><td rowspan=1 colspan=1> $\overline { { 0 . 6 , 0 . 4 \sim 1 } }$ </td></tr><tr><td rowspan=1 colspan=1>The number of heads</td><td rowspan=1 colspan=1>3</td></tr></table>

Our proposed method is evaluated by comparison with the following state-of-the-art methods:

DDQN-Based Method [26]: A DDQN-based joint optimization scheme for UAV 3D trajectory and RIS phase shifts.

SDRGN-Based Method [10]: A deep recurrent graph network (SDRGN) based on maximum entropy is designed to provide optimal communication coverage for ground PoIs.

DGRL-Based Method [35]: A deep graph convolutional reinforcement learning (DGRL) method that jointly optimizes communication and computation, enabling UAVs to cooperatively learn the optimal strategy in dynamic environments.

PSO: A classical population-based heuristic optimization algorithm is employed to jointly optimize the trajectory planning of UAVs and the phase shift control of RIS, based on a particle positionâvelocity update mechanism.

â¢ Random Phase: The RIS phase shifts are randomly selected from the interval [0, 2Ï).

TRAIL-without RIS: The UAV performs tasks without the assistance of RIS.

It is worth noting that the scenarios described above are not entirely identical to ours. Therefore, we have adapted these methods to fit our specific setting.

## B. Hyperparameter Selection

We evaluated the impact of batch size and sequence length () of TxBlocks on algorithm performance. The parameter Ï serves to comprehend long-term behavioral patterns of UAVs. From Table IV, it can be seen that energy efficiency is greatest with Batchesize = 128 and  = 10. The current position and future actions of UAVs may be influenced by earlier positions, an insufficient  value leads to decisions overly dependent on recent states, potentially neglecting critical historical information. Conversely, when  is excessively large, past embeddings may contain redundant information and superfluous details, complicating the learning process and resulting in significant performance degradation. As shown in Fig. 3, we also assessed the convergence performance of the TRAIL algorithm under various discount factors (Î³). A higher discount factor indicates that the agent places more emphasis on long-term rewards. $\mathrm { A t } ~ \gamma = 0 . 9 6$ , the reward stabilizes at approximately 8000, with smoother convergence and reduced fluctuations. Consequently, we established the discount factor Î³ at 0.96, achieving an optimal compromise between long-term reward optimization and training stability.

TABLE IV  
IMPACT OF DIFFERENT HYPERPARAMETERS
<table><tr><td rowspan=1 colspan=2>Batchsize</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>256</td></tr><tr><td rowspan=3 colspan=1>l=5</td><td rowspan=1 colspan=1>Thoughput</td><td rowspan=1 colspan=1>18659</td><td rowspan=1 colspan=1>19150</td><td rowspan=1 colspan=1>18610</td><td rowspan=1 colspan=1>18433</td></tr><tr><td rowspan=1 colspan=1>Energy</td><td rowspan=1 colspan=1>75.402</td><td rowspan=1 colspan=1>77.491</td><td rowspan=1 colspan=1>76.039</td><td rowspan=1 colspan=1>75.372</td></tr><tr><td rowspan=1 colspan=1>Energy efficiency</td><td rowspan=1 colspan=1>247.460</td><td rowspan=1 colspan=1>247.125</td><td rowspan=1 colspan=1>244.642</td><td rowspan=1 colspan=1>244.560</td></tr><tr><td rowspan=3 colspan=1>l=10</td><td rowspan=1 colspan=1>Thoughput</td><td rowspan=1 colspan=1>19157</td><td rowspan=1 colspan=1>19437</td><td rowspan=1 colspan=1>19452</td><td rowspan=1 colspan=1>19129</td></tr><tr><td rowspan=1 colspan=1>Energy</td><td rowspan=1 colspan=1>78.329</td><td rowspan=1 colspan=1>79.143</td><td rowspan=1 colspan=1>78.347</td><td rowspan=1 colspan=1>77.402</td></tr><tr><td rowspan=1 colspan=1>Energy effciency</td><td rowspan=1 colspan=1>244.571</td><td rowspan=1 colspan=1>245.593</td><td rowspan=1 colspan=1>247.995</td><td rowspan=1 colspan=1>241.138</td></tr><tr><td rowspan=3 colspan=1>l=15</td><td rowspan=1 colspan=1>Thoughput</td><td rowspan=1 colspan=1>19428</td><td rowspan=1 colspan=1>18691</td><td rowspan=1 colspan=1>19274</td><td rowspan=1 colspan=1>18847</td></tr><tr><td rowspan=1 colspan=1>Energy</td><td rowspan=1 colspan=1>79.329</td><td rowspan=1 colspan=1>75.761</td><td rowspan=1 colspan=1>79.242</td><td rowspan=1 colspan=1>76.430</td></tr><tr><td rowspan=1 colspan=1>Energyeffciency</td><td rowspan=1 colspan=1>244.904</td><td rowspan=1 colspan=1>246.710</td><td rowspan=1 colspan=1>243.223</td><td rowspan=1 colspan=1>246.592</td></tr><tr><td rowspan=3 colspan=1>l=20</td><td rowspan=1 colspan=1>Thoughput</td><td rowspan=1 colspan=1>19323</td><td rowspan=1 colspan=1>18257</td><td rowspan=1 colspan=1>19215</td><td rowspan=1 colspan=1>18511</td></tr><tr><td rowspan=1 colspan=1>Energy</td><td rowspan=1 colspan=1>78.411</td><td rowspan=1 colspan=1>77.530</td><td rowspan=1 colspan=1>80.432</td><td rowspan=1 colspan=1>75.376</td></tr><tr><td rowspan=1 colspan=1>Energy efficiency</td><td rowspan=1 colspan=1>246.432</td><td rowspan=1 colspan=1>235.483</td><td rowspan=1 colspan=1>238.897</td><td rowspan=1 colspan=1>245.582</td></tr></table>

<!-- image-->  
Fig. 3. Convergence of different Î³ values.

## C. Convergence Analysis

We evaluated the convergence behavior of the TRAIL algorithm by analyzing the evolution of reward values over training episodes. As shown in Fig. 4, the reward value shows a significant upward trend during the early stages of training, with the TRAIL algorithm converging to its optimal value around 500 episodes with minimal fluctuation. Although the SDRGN-based algorithm also converges to a stable value, it exhibits more pronounced fluctuations after convergence. The

<!-- image-->  
Fig. 4. Reward curves during the training phase.

DDQN-based algorithm, when operating in stochastic environments, is susceptible to function approximation errors that compromise policy stability. Consequently, it converges to lower reward values and exhibits substantial fluctuations after convergence. Overall, among the compared DRL algorithms, TRAIL demonstrates faster convergence and greater stability, enabling more effective decision-making within a shorter training period.

In addition to analyzing the convergence of reward values, it is essential to evaluate the algorithmâs effectiveness in terms of specific performance metrics. Fig. 5 compares the different algorithms in terms of throughput and energy consumption. As shown in Fig. 5(a), the TRAIL algorithm saturates at around 500 episodes, achieving a throughput of approximately 22,000 Kbps, which is significantly higher than the other algorithms. This result highlights TRAILâs capability to jointly optimize UAV trajectories and RIS phase configurations, thereby enhancing data transmission efficiency. The DDQN algorithm, while demonstrating reasonable performance, converges to a lower throughput value than TRAIL, typically around 17,000 Kbps. This limitation arises from DDQNâs inability to capture temporal dependencies between states, resulting in suboptimal trajectory planning and RIS phase adjustments that degrade overall system performance. In comparison, while the TRAIL(without RIS) variant also exhibits good convergence behavior, its throughput stabilizes at approximately 13,000 Kbps, underscoring the limitations of omitting RIS in improving communication performance. The other baseline algorithms demonstrate inferior adaptability in complex environments, resulting in lower throughput values. Furthermore, as depicted in Fig. 5(b), the TRAIL algorithm also converges around 500 episodes and maintains the lowest energy consumption level among all methods, underscoring its superiority in energyefficient operation.

The TRAIL algorithm incorporates a multi-head selfattention mechanism to enhance the performance of the transformer encoder in extracting temporal features from the UAV trajectory. Following the approach in [10], we assessed convergence by monitoring the weight changes of each attention head. When the weights of all heads gradually stabilize, it indicates that the model has reached a balanced state and achieved effective convergence. Fig. 6 illustrates that the attention weight distributions for head1 and head3 are relatively concentrated, suggesting that these heads converge quickly during training and consistently focus on specific features. In contrast, the weight distributions of head2 and head4 are more dispersed, indicating slower convergence in capturing information. These experimental results underscore the importance of the multihead mechanism, as the variations among the heads highlight its role in effectively capturing diverse aspects of the data.

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 5. (a) Throughout, (b) energy consumption, over time during training. The TRAIL algorithm achieves the highest throughput and the lowest energy consumption compared to other algorithms, demonstrating its efficiency in optimizing UAV trajectories and RIS phase adjustments.  
<!-- image-->  
Fig. 6. After 3000 iterations of updating the graph attention weights. This highlights the importance of the multi-head mechanism in capturing diverse data features.

## D. Performance Analysis

1) Cumulative Distribution of Energy Consumption and Throughput: Fig. 7 presents a comparative analysis of the cumulative distribution functions (CDF) for different algorithms with respect to throughput and energy consumption. As shown in Fig. 7(a), the TRAIL algorithm demonstrates a clear advantage in the high-throughput region, with its CDF curve displaying higher cumulative probability values at greater throughput levels. Notably, the TRAIL curve rises more steeply than those of the baseline algorithms, indicating that its throughput values are more consistently concentrated in the high-performance range. This performance is attributed to TRAILâs ability to capture long-term dependencies in UAV trajectories and dynamically adjust RIS phase shifts in response to changing channel conditions. In contrast, DDQN has limited capacity to model temporal dependencies, struggling to effectively handle high-dimensional state spaces and sequential dependencies, which results in performance inferior to that of TRAIL. Similarly, Fig. 7(b) shows that TRAIL achieves higher cumulative probabilities in the low energy consumption region. While TRAIL(without RIS) also benefits from trajectory optimization, its energy efficiency is diminished due to the lack of RISassisted channel enhancement.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 7. Performance of different algorithms in terms of energy consumption and throughput. The TRAIL algorithm achieves higher CDF values in the higher throughput range and lower energy consumption range.

2) Impact of Number of Reflect Elements: The number of reflecting elements influences the RISâs ability to control the signal. As shown in Fig. 8(a) when the number of reflecting elements is small, the signal control capability of the RIS is limited. Consequently, the UAV needs to use higher transmission power to maintain communication quality, leading to higher energy consumption. As the number of reflecting elements increases, the control capability improves, resulting in a reduction in energy consumption. Once the number of reflecting elements reaches a certain threshold, the control effect saturates, and the energy consumption stabilizes. Although the PSO algorithm achieves global optimization through iterative updates of randomized solutions, it exhibits the highest time complexity among the evaluated methods, as shown in Table II. Moreover, while other algorithms demonstrate varying degrees of performance improvement, none consistently outperform the proposed TRAIL algorithm. The Random Phase Scheme, lacking effective phase control, exhibits higher energy consumption and the poorest optimization effect.

<!-- image-->  
(a) Impact of the number of M on energy consumption.

<!-- image-->  
(b) The relationship between rate and M for different phase shifts.  
Fig. 8. Performance of different algorithms with different number of RIS elements(M ).

Due to hardware limitations, implementing continuous phase shifts in RIS presents significant challenges in practice. Therefore, as described in sec.II, we consider RIS configurations where each unitâs phase shift adopts a finite number of discrete values. As shown in Fig. 8(b), 3-bit quantization outperforms 2-bit quantization in terms of data rate due to smaller phase steps (Ï/4), which reduces quantization error. However, finer quantization expands the action space, potentially increasing the training complexity of TRAIL algorithm. Moreover, increasing from 2-bit to 3-bit quantization doubles the number of phase shift levels (from D = 4 to D = 8), requiring more sophisticated control circuitry (e.g., higher resolution DACs or more PIN diodes per element). This increases both the hardware cost and power consumption of the RIS. Therefore, in our current experiments, we have selected b = 2 as the quantization level.

3) Illustrative Multi-UAV Trajectories: Fig. 9 illustrates UAV flight trajectories in both two-dimensional and threedimensional spaces, comparing scenarios with and without RIS assistance. In Fig. 9, we assume that the set of target PoIs is scattered in a circular area. As shown in Fig. 9(d) and Fig. 9(c), four UAVs take off from distinct initial positions. Notably, UAV1 and UAV3âboth equipped with RIS supportâ exhibit a clear tendency to navigate toward the RIS deployment locations during their trajectories. This behavior is attributed to the RISâs ability to enhance communication link quality through intelligent phase and amplitude modulation of reflected signals. By leveraging this capability, UAVs can maintain stable communication without needing to fly close to the PoIs. In contrast, UAV2 and UAV4, which operate without RIS assistance, must reduce their distance to the PoIs to ensure reliable communication links. Consequently, their trajectories are directed more closely toward their respective targets.

4) Performance of the Algorithm in Environments with Different Densities: We further evaluated the environmental adaptability of various algorithms across three distinct environmentsâsuburban, urban, and dense urban [36]âby examining the effects of varying numbers of PoIs on both throughput and energy consumption. The PoI quantities were set to [170, 180, 190, 200, 210]. As shown in Fig. 10, TRAIL consistently outperforms other methods in terms of throughput across all environments, with the highest throughput observed in suburban areas. In urban areas, TRAIL achieves a 7.67% higher throughput than DDQN, and this improvement increases to 14.24% in dense urban environments. These results suggest that while DDQN performs reasonably well in less obstructed environments, its lack of temporal modeling provided by the transformer architectureâlimits its effectiveness, especially under favorable LoS conditions. TRAIL(without RIS) also demonstrates performance gains, primarily due to trajectory optimization that reduces path loss under LoS scenarios. The Random Phase approach exhibited the lowest performance, due to its inability to effectively enhance channel quality where NLoS components exist, resulting in suboptimal signal reflection.

Fig. 11 illustrates the energy consumption of the TRAIL algorithm in different environments. As the number of PoIs increases, total computational workload grows, resulting in higher energy consumption across all methods. As shown in Fig. 11(a), when the number of PoIs reaches 220, TRAIL reduces energy consumption by 63.4% compared to TRAIL(without RIS). Notably, in dense urban environments, the disparity in energy consumption between the TRAIL algorithm and baseline methods becomes more significant. According to Fig. 11(c), TRAIL achieves a reduction of up to 69.7% in energy consumption compared to TRAIL(without RIS) at the same PoI level. This significant improvement highlights the critical role of RIS phase optimization in complex LoS-dominant environments.

## E. Discussion

In real-world scenarios, PoI often exhibit mobility, such as in mobile devices like smartphones or vehicles in intelligent transportation systems. To evaluate TRAILâs applicability in more dynamic environments, we utilized the KAIST dataset [37]. This dataset contains mobility trajectories from students carrying GPS-equipped smartphones across a university campus, providing authentic representations of mobile PoIs.

1) PoI Mobility Analysis: We selected 80 user trajectories to analyze the impact of PoI mobility on TRAIL algorithm performance. PoI movement alters LoS and NLoS conditions, while frequent changes in PoI positions necessitate dynamic adjustment of RIS phase shifts to maintain optimal signal reflection. However, due to the relatively slow movement speed of PoIs (students), the impact on channel gain and data rates remains minimal. Consequently, as shown in Fig. 12(a), the average throughput only slightly decreases compared to fixed PoI scenarios due to minor channel variations. Nevertheless, TRAIL outperforms baseline methods by leveraging the Transformerâs ability to capture long-term dependencies in UAV trajectories and PoI movement patterns. Notably, TRAILâs computational accuracy may decrease in highly unpredictable mobility scenarios. Future work could incorporate techniques such as Kalman filters or RNNs to predict future PoI positions based on past movements. These predictions could then be fed into the DRL agent to guide its action selection.

<!-- image-->  
(a) Trajectories of two UAVs in 3D.

<!-- image-->  
(b) Trajectories of two UAVs in 2D.

<!-- image-->  
(c) Trajectories of four UAVsin 3D.

<!-- image-->  
(d) Trajectories of four UAVs in 2D.

Fig. 9. 2D and 3D flight trajectories of two and four UAVs. We assume that the set of target PoIs is scattered in a circular area.  
<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼

Fig. 10. Comparison of throughput for varying numbers of PoIs across different urban environments. (a) Suburban. (b) Urban. (c) Dense urban.  
<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 11. Comparison of energy for varying numbers of PoIs across different urban environments. (a) Suburban. (b) Urban. (c) Dense urban.

2) Limitations: We fixed the number of PoI at 200 and varied the deployed UAV count from 1 to 50. As illustrated in Fig. 12(b), the TRAIL algorithm exhibits a higher computational time cost growth rate compared to other baseline algorithms as the number of UAVs increases. This occurs because larger state and action spaces lead to increased computational complexity. While the Transformer architecture effectively captures long-term dependencies, it requires substantial computational resources as the network scale expands. Nevertheless, even under the most extreme test conditions (50 UAVs), the TRAIL algorithm maintains a computational cost of approximately 26ms, which remains acceptable for most practical drone application scenarios. Many commercial and research UAV systems can accommodate decision-making times of 50-100ms [34] within their control loops without performance degradation, demonstrating potential applicability across most real-world scenarios.

<!-- image-->

<!-- image-->  
(b)  
Fig. 12. (a) The throughput and energy consumption performance of different algorithms on the KAIST dataset. (b) Impacts of number of UAVs on computational complexity by time cost (ms).

## V. CONCLUSION

This paper investigated a UAV-assisted MCS system enhanced by RIS to maximize data throughput. We introduced TRAIL, a Transformer-enhanced DRL algorithm designed to jointly optimize UAV trajectories and RIS phase shifts. Our simulation results demonstrate that TRAIL significantly outperforms other benchmark algorithms in both throughput maximization and energy consumption minimization. TRAIL successfully adapts to varying RIS element numbers and different environmental densities, achieving consistent performance gains. Additionally, UAVs tend to fly closer to RIS to benefit from better channel conditions, a behavior markedly different from UAV-enabled MCS systems without RIS assistance.

## REFERENCES

[1] X. Liu et al., âA coverage-aware task allocation method for UAV-assisted mobile crowd sensing,â IEEE Trans. Veh. Technol., vol. 73, no. 7, pp. 10642â10654, Jul. 2024.

[2] H. Wang, H. Zhang, X. Liu, K. Long, and A. Nallanathan, âJoint UAV placement optimization, resource allocation, and computation offloading for THz band: A DRL approach,â IEEE Trans. Wireless Commun., vol. 22, no. 7, pp. 4890â4900, Jul. 2023.

[3] Z. Dai et al., âAoI-minimal UAV crowdsensing by model-based graph convolutional reinforcement learning,â in Proc. IEEE Conf. Comput. Commun. (INFOCOM), 2022, pp. 1029â1038,

[4] W. Jiang, B. Ai, C. Shen, M. Li, and X. Shen, âAge-of-information minimization for UAV-based multi-view sensing and communication,â IEEE Trans. Veh. Technol., vol. 73, no. 1, pp. 1100â1114, Jan. 2024.

[5] Q. Wu, Q. Liu, Y. He, and Z. Wu, âUAV-enabled energy-efficient aerial computing: A federated deep reinforcement learning approach,â IEEE Trans. Rel., early access, 2024.

[6] D. Wu et al., âADDSEN: Adaptive data processing and dissemination for drone swarms in urban sensing,â IEEE Trans. Comput., vol. 66, no. 2, pp. 183â198, Feb. 2017.

[7] S. Wang, X. Song, T. Song, and Y. Yang, âFairness-aware computation offloading with trajectory optimization and phase-shift design in RISassisted multi-UAV MEC network,â IEEE Internet Things J., vol. 11, no. 11, pp. 20547â20561, Jun. 2024.

[8] Y. Wan, Y. Zhong, A. Ma, and L. Zhang, âAn accurate UAV 3-D path planning method for disaster emergency response based on an improved multiobjective swarm intelligence algorithm,â IEEE Trans. Cybern., vol. 53, no. 4, pp. 2658â2671, Apr. 2023.

[9] L. Fu, Z. Zhao, G. Min, W. Miao, L. Zhao, and W. Huang, âEnergyefficient 3-D data collection forMulti-UAV assisted mobile crowdsensing,â IEEE Trans. Comput., vol. 72, no. 7, pp. 2025â2038, Jul. 2023.

[10] Z. Ye, K. Wang, Y. Chen, X. Jiang, and G. Song, âMulti-UAV navigation for partially observable communication coverage by graph reinforcement learning,â IEEE Trans. Mobile Comput., vol. 22, no. 7, pp. 4056â4069, Jul. 2023.

[11] Q. Wu, Q. Liu, W. Zhu, and Z. Wu, âEnergy efficient UAV-assisted IoT data collection: A graph-based deep reinforcement learning approach,â IEEE Trans. Netw. Service Manag., vol. 21, no. 6, pp. 6082â6094, Dec. 2024.

[12] R. Chen, M. Liu, Y. Hui, N. Cheng, and J. Li, âReconfigurable intelligent surfaces for 6G IoT wireless positioning: A contemporary survey,â IEEE Internet Things J., vol. 9, no. 23, pp. 23570â23582, Dec. 2022.

[13] G. Iacovelli, A. Coluccia, and L. A. Grieco, âMulti-UAV IRS-assisted communications: multi-node channel modeling and fair sum-rate optimization via deep reinforcement learning,â IEEE Internet Things J., vol. 11, no. 3, pp. 4470â4482, Feb. 2024.

[14] X. Liu, Y. Liu, and Y. Chen, âMachine learning empowered trajectory and passive beamforming design in UAV-RIS wireless networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 7, pp. 2042â2055, Jul. 2021.

[15] M. Ahmed et al., âActive reconfigurable intelligent surfaces: Expanding the frontiers of wireless communication-a survey,â IEEE Commun. Surveys Tuts., vol. 27, no. 2, pp. 839â869, Apr. 2025.

[16] X. Qin, Z. Song, T. Hou, W. Yu, J. Wang, and X. Sun, âJoint optimization of resource allocation, phase shift, and UAV trajectory for energyefficient RIS-assisted UAV-enabled MEC systems,â IEEE Trans. Green Commun. Netw., vol. 7, no. 4, pp. 1778â1792, Dec. 2023.

[17] Y. Xu, H. Qi, Z. Wang, X. Zhang, Y. Li, and T. Q. Quek, âWireless-powered mobile crowdsensing enhanced by UAV-mounted RIS: Joint transmission, compression, and trajectory design,â 2024, arXiv:2407.21280.

[18] C. Zhao, X. Pang, W. Lu, Y. Chen, N. Zhao, and A. Nallanathan, âEnergy efficiency optimization of IRS-assisted UAV networks based on statistical channels,â IEEE Wireless Commun. Lett., vol. 12, no. 8, pp. 1419â1423, Aug. 2023.

[19] W. Chen, Y. Zou, J. Zhu, and L. Zhai, âJoint trajectory design and phase shift optimization for multi-RIS-assisted UAV relay network using deep reinforcement learning,â IEEE Internet Things J., vol. 12, no. 8, pp. 9759â9774, Apr. 2025.

[20] M. Wu et al., âDeep reinforcement learning-based energy efficiency optimization for RIS-aided integrated satellite-aerial-terrestrial relay networks,â IEEE Trans. Commun., vol. 72, no. 7, pp. 4163â4178, Jul. 2024.

[21] L. Guo, J. Jia, J. Chen, S. Yang, Y. Xue, and X. Wang, âRIS-aided secure A2G communications with coordinated multi-UAVs: A hybrid DRL approach,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 5, pp. 4536â 4550, Sept./Oct. 2024.

[22] X. Liu, Y. Liu, and Y. Chen, âMachine learning empowered trajectory and passive beamforming design in UAV-RIS wireless networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 7, pp. 2042â2055, Jul. 2021.

[23] B. Adhikari, A. S. Khwaja, M. Jaseemuddin, A. Anpalagan, and A. Nallanathan, âEnergy efficient RIS-assisted UAV networks using twin delayed DDPG technique,â IEEE Trans. Wireless Commun., vol. 23, no. 12, pp. 18423â18439, Dec. 2024.

[24] Y. Yao, K. Lv, S. Huang, and W. Xiang, â3D deployment and energy efficiency optimization based on DRL for RIS-assisted air-to-ground communications networks,â IEEE Trans. Veh. Technol., vol. 73, no. 10, pp. 14988â15003, Oct. 2024.

[25] I. Budhiraja, V. Vishnoi, N. Kumar, D. Garg, and S. Tyagi, âEnergyefficient optimization scheme for RIS-assisted communication underlaying UAV with NOMA,â in Proc. IEEE Int. Conf. Commun. (ICC), 2022, pp. 1â6.

[26] H. Mei, K. Yang, Q. Liu, and K. Wang, â3D-trajectory and phase-shift design for RIS-assisted UAV systems using deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 71, no. 3, pp. 3020â3029, Mar. 2022.

[27] K. K. Nguyen, S. R. Khosravirad, D. B. da Costa, L. D. Nguyen, and T. Q. Duong, âReconfigurable intelligent surface-assisted multi-UAV networks: Efficient resource allocation with deep reinforcement learning,â IEEE J. Sel. Topics Signal Process., vol. 16, no. 3, pp. 358â 368, Apr. 2022.

[28] H. V. Abeywickrama, B. A. Jayawickrama, Y. He, and E. Dutkiewicz, âPotential field based inter-UAV collision avoidance using virtual target relocation,â in Proc. IEEE 87th Veh. Technol. Conf. (VTC Spring), 2018, pp. 1â5.

[29] C. You and R. Zhang, â3D trajectory optimization in Rician fading for UAV-enabled data harvesting,â IEEE Trans. Wireless Commun., vol. 18, no. 6, pp. 3192â3207, Jun. 2019.

[30] Y. K. Tun, Y. M. Park, N. H. Tran, W. Saad, S. R. Pandey, and C. S. Hong, âEnergy-efficient resource management in UAV-assisted mobile edge computing,â IEEE Commun. Lett., vol. 25, no. 1, pp. 249â253, Jan. 2021.

[31] Q. Wu and R. Zhang, âBeamforming optimization for wireless network aided by intelligent reflecting surface with discrete phase shifts,â IEEE Trans. Commun., vol. 68, no. 3, pp. 1838â1851, Mar. 2020.

[32] H. Zhang, M. Huang, H. Zhou, X. Wang, N. Wang, and K. Long, âCapacity maximization in RIS-UAV networks: A DDQN-based trajectory and phase shift optimization approach,â IEEE Trans. Wireless Commun., vol. 22, no. 4, pp. 2583â2591, Apr. 2023.

[33] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[34] H. Chao, Y. Cao, and Y. Chen, âAutopilots for small unmanned aerial vehicles: A survey,â Int. J. Control Autom. Syst., vol. 8, pp. 36â44, Feb. 2010.

[35] D. Wang, Y. Bai, G. Huang, B. Song, and F. R. Yu, âCache-aided MEC for IoT: Resource allocation using deep graph reinforcement learning,â IEEE Internet Things J., vol. 10, no. 13, pp. 11486â11496, Jul. 2023.

[36] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[37] I. Rhee, M. Shin, S. Hong, K. Lee, S. Kim, and S. Chong, âCrawdad data set NCSU/Mobilitymodels (v. 2009-07-23),â 2009. [Online]. Available: https://crawdad.org/ncsu/mobilitymodels/20090723

<!-- image-->  
Qianqian Wu received the B.S. degree in computer technology from the North China University of Science and Technology, Tangshan, China, in 2022. She is currently working toward the Ph.D. degree with the School of Computer Science and Technology, Beijing Jiaotong University. Her current research interests include UAV aided networks, mobile crowdsensing, and deep reinforcement learning.

<!-- image-->

Qiang Liu (Member, IEEE) received the B.S. and Ph.D. degrees in communication and information system from Beijing Institute of Technology, Beijing, China, in 2002 and 2007, respectively. From 2007 to 2018, he was an Assistant Professor with the School of Computer Science and Technology, Beijing Jiaotong University, where he has been an Associate Professor, since 2019. He is the author of more than 50 articles and four patents. His research interests include mobile ad-hoc networks, UAV networking, wireless communications, wireless routing, and swarm intelligence.

<!-- image-->  
lite communication.

Ying He (Senior Member, IEEE) received the B.Eng. degree from Beijing University of Posts and Telecommunications, Beijing, China, in 2009, and the Ph.D. degree from the University of Technology Sydney, Australia, in 2017, both in telecommunications engineering. Currently, she is a Senior Lecturer with the School of Electrical and Data Engineering, University of Technology Sydney. Her research interests are physical layer algorithms in wireless communication with machine learning, vehicular communication, spectrum sharing, and satel-

<!-- image-->

Zefan Wu received the B.S. degree in mathematics and applied mathematics and in computer science and technology from Beijing Jiaotong University, in 2023. He is currently working toward the Ph.D. degree with the School of Computer Science and Technology, Beijing Jiaotong University. His current research interests include deep reinforcement learning, mobile edge computing, and UAV communications.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning/page_5_img_1.jpeg|page_5_img_1]]
2. [[../extracted_images/Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning/page_13_img_1.jpeg|page_13_img_1]]
3. [[../extracted_images/Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning/page_13_img_2.jpeg|page_13_img_2]]
4. [[../extracted_images/Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning/page_13_img_3.jpeg|page_13_img_3]]
5. [[../extracted_images/Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning/page_13_img_4.jpeg|page_13_img_4]]

---

