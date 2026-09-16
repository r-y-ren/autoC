# Online Energy and Interference Management for Dynamic Target Tracking With Cellular-Connected UAV

Cheng Zhan , Member, IEEE, Huan Yan, Graduate Student Member, IEEE, Rongfei Fan , Member, IEEE, Han Hu , Member, IEEE, Shubin Xu, and Jian Yang , Senior Member, IEEE

AbstractâCellular-connected Unmanned Aerial Vehicles (UAVs) have significant potential for target tracking in future cellular networks due to their broad coverage and operational flexibility. In this paper, we consider a multi-cell cellular network with a cellular-connected UAV for target tracking, which encounters challenges such as unpredictable flight energy consumption from the stochastic movements of the tracking target and severe uplink interference from ground devices (GDs). To tackle these challenges, we propose a multi-stage stochastic optimization framework focused on energy-efficient target tracking with interference coordination. Our objective is to optimize the long-term average uplink throughput of both aerial users and GDs by jointly optimizing the UAVâs trajectory, power allocation, and cell association across multiple orthogonal communication resource blocks (RBs). The formulated stochastic non-convex problem is first transformed into a deterministic problem for each time slot by using the Lyapunov optimization framework. An online optimization strategy is proposed, utilizing the optimal structure, alternative optimization, and successive convex approximation (SCA) techniques. Simulation results show that the proposed approach significantly enhances network throughput and UAV energy queue stability compared to existing baseline schemes.

Index TermsâCellular connected UAV, dynamic target tracking, energy management, Lyapunov optimization.

Received 19 August 2024; revised 9 January 2025; accepted 17 January 2025. Date of publication 21 January 2025; date of current version 7 May 2025. This work was supported in part by the National Natural Science Foundation of China under Grant 62172339 and Grant 62171034, in part by the Joint Funds of the National Natural Science Foundation of China under Grant U23A20275 and Grant U2336211, in part by the Natural Science Foundation of Chongqing under Grant CSTB2022NSCQ-MSX0338, and in part by the Chongqing Graduate Research and Innovation Project under Grant CYS23206. Recommended for acceptance by D. Yang. (Corresponding author: Han Hu.)

## I. INTRODUCTION

(UAVs) are becoming key elements in the advancement of future cellular networks as novel aerial users with a variety of applications, such as remote sensing, cargo transportation, and aerial target tracking [1], [2], [3], [4]. Unlike traditional UAVs with limited visual line-of-sight (VLoS) communications, cellular-connected UAVs improve remote communication and control by enhancing reliability, security, and throughput through the use of existing high-capacity cellular backhaul links. Recent studies have leveraged these UAVs for aerial target tracking in regional monitoring to ensure public safety. The work in [5] employed UAVs for ocean target tracking using a lightweight energy-saving scheme, which optimized real-time tracking with an Elman neural network, thus reducing energy consumption while ensuring high tracking success and data stability. The work in [6] proposed a cooperative multi-agent reinforcement learning (MARL) framework for regional target tracking to enhance tracking efficiency and accuracy through optimizing power consumption and extending UAV lifetimes.

The challenge in UAV tracking arises from the stochastic nature of target movements, which makes energy consumption unpredictable. This unpredictability arises from several factors, including sudden changes in the UAVâs trajectory and varying speeds required to maintain target tracking. Traditional deterministic methods are insufficient for managing such uncertainties in practical scenarios. The work in [7] proposed an online learning strategy for optimizing task completion delays in UAV-enabled mobile edge computing (MEC) systems, where dynamic user movements and task arrivals were addressed using reduced complexity methods. The work in [8] proposed online computation offloading strategies in MEC systems, where task execution delay and energy consumption were optimized by leveraging nearby access points (APs) and server selection algorithms under communication dynamics. In [9], UAVs in a MEC network optimized energy consumption by dynamically allocating resources and trajectories through a velocity-triggered penalty term without considering the air-to-ground interference.

Integrating UAVs into cellular networks presents fundamental challenges, particularly due to potential interference. The high altitude of UAVs creates a line-of-sight (LoS) communication channel with base stations (BSs), which offers both benefits and challenges. While LoS channels ensure steadier communication and enable UAVs to link with multiple BSs for network diversity enhancement, they also complicate interference management by increasing potential uplink interference across a broader set of BSs. Prior works [10], [11], [12] have explored various strategies for interference mitigation in UAV networks, including full-dimensional antenna arrays and multicell beamforming. However, these works have primarily focused on interference coordination technologies, overlooking the unpredictability of energy consumption in random target tracking flights. Integrating such unpredictability with cellular-connected UAVs presents several challenges. First, the UAVs must effectively track randomly moving targets, which requires dynamic adaptability. Second, it is essential to manage energy consumption efficiently to prolong UAV operational times. Lastly, resource allocation must be controlled to minimize air-to-ground interference while ensuring balanced throughput for both aerial user and ground devices (GDs).

To tackle these challenges, in this paper, we develop a design framework for cellular-connected UAV target tracking. This framework addresses the unpredictability of flight energy consumption by considering the stochastic nature of target movements while incorporating interference coordination for throughput improvement with both aerial users and GDs. The main contributions of this paper are summarized as follows:

- We develop a multi-stage stochastic optimization framework for interference-aware cellular-connected UAV target tracking to enhance uplink throughput for both aerial and ground users while ensuring energy efficiency. This is achieved by simultaneously optimizing UAV tracking trajectory, BS association, and power allocation across multiple orthogonal resource blocks (RBs).

C We first transform the formulated problem into a deterministic model for each time slot by employing Lyapunov optimization techniques. By treating energy constraint as virtual energy-aware queue dynamics and balancing average network throughput and energy consumption with a penalty factor, we develop a comprehensive framework that effectively manages the tradeoff between communication performance and energy efficiency.

C We propose an efficient online strategy that decouples the deterministic optimization problem into subproblems for UAV trajectory design, transmit power control, and BS association optimization. These subproblems are iteratively solved by optimal structure analysis and successive convex approximation (SCA) techniques.

. Simulation results show that compared to the baseline schemes, the proposed solution effectively reduces interference between aerial users and GDs to improve overall network throughput. Additionally, the results show that the proposed solution ensures energy efficiency and enhances system stability.

The rest of this paper is organized as follows. Section II presents related work. Section III describes the system model and formulates the optimization problem. In Section IV, we present the Lyapunov optimization based online control algorithm. In Section V, we address the single time slot problem.

TABLE I LIST OF NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>J</td><td rowspan=1 colspan=1>The set of BSs</td></tr><tr><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=1>The set of time slots</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>The set of all RBs</td></tr><tr><td rowspan=1 colspan=1>g</td><td rowspan=1 colspan=1>The horizontal coordinate of BS j</td></tr><tr><td rowspan=1 colspan=1>sr</td><td rowspan=1 colspan=1>Thehorizontal coordinateof the target at time slot n</td></tr><tr><td rowspan=1 colspan=1>UAV $\underline { { \mathbf { s } } } _ { ( n ) } ^ { \mathrm { u } , \mathrm { u } , \mathrm { v } }$ </td><td rowspan=1 colspan=1>The horizontal coordinate of the UAV at time slot n</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Thetargetrandomnesslevel</td></tr><tr><td rowspan=1 colspan=1> $\overline { { v _ { n } ^ { \mathrm { T a r } } } }$ </td><td rowspan=1 colspan=1>The speed of the target at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \theta _ { n } ^ { \mathrm { T a r } } } }$ </td><td rowspan=1 colspan=1>The direction of the target at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\scriptstyle { \frac { \scriptscriptstyle 1 6 } { \scriptscriptstyle { \overline { { v } } } } }$ </td><td rowspan=1 colspan=1>Thetargetmeanspeed and direction</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \theta } }$ </td><td rowspan=1 colspan=1>The target mean direction</td></tr><tr><td rowspan=1 colspan=1> $\smash { \overline { { d _ { \cdots } ^ { \mathrm { I a r } } } } }$ </td><td rowspan=1 colspan=1>The distance between the UAV and the target at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\displaystyle \frac { n } { d ^ { \mathrm { U A V } } }$  $\underline { d } _ { j , ( n ) } ^ { \cup \mathrm { A v } }$ </td><td rowspan=1 colspan=1>The distance between the UAV and BS j at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\overleftarrow { D }$ </td><td rowspan=1 colspan=1>The tracking range</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathcal { N } _ { q } ^ { j } } }$ </td><td rowspan=1 colspan=1>The set of first q-tierneighboringcells forBS j</td></tr><tr><td rowspan=1 colspan=1> $\underline { { H _ { j , m , n } } }$ </td><td rowspan=1 colspan=1>TheGD-BSchannel coefficient forBSj withRB m at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\underline { { G _ { m , n } ^ { \jmath } } }$ </td><td rowspan=1 colspan=1>The UAV-BS channel coefficient for BS j with RB m at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \hat { p } _ { j , m , n } } }$ </td><td rowspan=1 colspan=1>The transmit power of the GD for BS j with RB m at time slot n</td></tr><tr><td rowspan=1 colspan=1> ${ \underline { { \beta _ { 0 } } } }$ </td><td rowspan=1 colspan=1>The channel power gain</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \alpha } }$ </td><td rowspan=1 colspan=1>The path loss exponent</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \sigma _ { j , m , n } ^ { 2 } } }$ </td><td rowspan=1 colspan=1>The total background noise power for BS j with RB m at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { g } ( m , n ) } }$ </td><td rowspan=1 colspan=1>The G2G throughput for RB m at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { u } ( m , n ) } }$ </td><td rowspan=1 colspan=1>The A2G throughput forRB m at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { Q ( n ) } }$ </td><td rowspan=1 colspan=1>The virtual energy queue</td></tr><tr><td rowspan=1 colspan=1> $\dot { \overline { { \mathbf { v } _ { n } ^ { \mathrm { U A V } } } } }$ </td><td rowspan=1 colspan=1>The flight velocity of the UAV at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P ^ { \mathrm { f } } ( n ) } }$ </td><td rowspan=1 colspan=1>The flight power during flight at time slot n</td></tr><tr><td rowspan=1 colspan=1> $E _ { ( n ) } ^ { \mathrm { t } }$ </td><td rowspan=1 colspan=1>The flight energy consumption at time slot n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { E _ { \mathrm { m a x } } ^ { \mathrm { f } } } }$ </td><td rowspan=1 colspan=1>The maximum allowable average energy consumption</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Thepenaltyfactor</td></tr></table>

Simulation results are presented in Section VI. Finally, conclusions are drawn in Section VII. The main notations used throughout the paper are summarized in Table I.

## II. RELATED WORK

In this section, we review the existing literature on cellularconnected UAVs, focusing on aspects such as target tracking, interference management, and energy consumption.

## A. Target Tracking With Cellular-Connected UAVs

Cellular-connected UAVs have been extensively studied for their ability to leverage existing cellular infrastructure for communication, control, and target tracking across various applications. In [13], a two-phase command and control transmission scheme was proposed. This scheme optimizes message relays under latency and energy constraints using a decentralized constrained graph attention multi-agent Deep-Q-network approach. A three dimensional (3D) path planning framework for cellular-connected UAVs was proposed in [14], which optimizes flying distance while maintaining communication quality with ground BSs using signal-to-interference-plus-noise ratio (SINR) maps and grid quantization. Furthermore, the authors in [15] examined coordinated multi-point non-orthogonal multiple access (CoMP-NOMA) integration in cellular-connected UAV networks to enhance reliability and average ergodic rates for both aerial and terrestrial users.

Target tracking using cellular-connected UAVs has gained significant attention due to its potential in surveillance, search and rescue, and disaster management. In [16], a cooperative mission strategy was proposed using UAVs for a search-and-track mission of underwater targets, which optimizes path planning considering maneuverability and communication constraints.

The work in [17] proposed a deep reinforcement learning (DRL) approach for multi-UAV tracking of first responders in complex 3D environments for enhanced tracking accuracy. Furthermore, the authors in [18] proposed a DRL-based deep deterministic policy gradient (DDPG) model for visual UAV tracking, optimizing energy efficiency and tracking accuracy. In [19], [20], methods were proposed to enhance UAV target tracking, collision avoidance, and trajectory prediction using UAV swarmbased cooperative architecture and distributed model predictive control (DMPC)-based approaches. The work in [21] presented a framework for optimizing the energy-efficient 3D trajectory of a solar-powered UAV monitor for autonomous tracking of suspicious UAVs. However, these studies overlook the practical challenges posed by interference and energy issues in cellularconnected UAVs.

## B. Interference Management for Cellular-Connected UAVs

Interference management is essential for cellular-connected UAVs, especially in densely populated urban areas. In [22], a novel UAV enabled reconfigurable intelligent surface (RIS)- aided interference management scheme for space-air-ground integrated networks was proposed, which leverages various types of channel state information (CSI) and employs interference alignment, beamforming, and space-time precoding to improve system capacity. The study in [23] developed an alternatingmaximization approach to optimize 3D UAV trajectories and transmission powers, aiming to maximize data throughput while mitigating interference from existing communication networks. In [24], an optimization algorithm was proposed for joint IRSuser association, UAV trajectory optimization, successive interference cancellation (SIC) decoding order scheduling, and power allocation to maximize energy efficiency in multi-IRS UAV communications. Additionally, the work in [25] proposed an interference-aware path planning scheme using deep reinforcement learning to optimize energy efficiency and reduce interference in cellular-connected UAV networks. This scheme achieves adaptive UAV altitude adjustment for enhanced performance. Despite these advancements, the specific impact of interference on UAV-enabled target tracking with energy consideration remains inadequately explored.

## C. Energy Issues for Cellular-Connected UAVs

Efficient energy management is a critical challenge for cellular-connected UAVs. In [26], an algorithm combining DRL and linear programming was proposed to maximize energy efficiency and ensure offloading fairness in UAV-assisted MEC by optimizing UAV trajectory, flight time, and offloading decisions of terminal devices. The research in [27] presented a 3D energy-efficient trajectory optimization framework for rotary-wing UAVs in downlink communication, which adapts to stochastic wind effects using an offline-based online adaptive approach. In [28], an energy-efficient data collection method using RIS and UAVs was proposed, optimizing UAV trajectory and sensor schedules to minimize energy consumption. Furthermore, the work in [29] explored a control-based 3D trajectory optimization method for UAV-aided wireless communication, ensuring smooth trajectories and validating an improved energy consumption model through simulations. However, these studies did not consider energy consumption in the context of UAVenabled target tracking, particularly considering the targetâs randomness and the air-to-ground interference environment.

<!-- image-->  
Fig. 1. Target tracking with cellular-connected UAV.

Different from the above works, we investigate a comprehensive framework for scalable target tracking with random movements using cellular-connected UAVs. We address both interference management and energy efficiency by jointly optimizing UAV trajectory, power allocation, and BS association. Our method ensures reliable target tracking despite the targetâs randomness and minimizes interference to maximize both aerial and ground throughput. This approach conserves energy consumption, providing a robust solution for practical deployment.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

## A. Network Model

As shown in Fig. 1, we investigate a hybrid air-to-ground (A2G) communication network with a cellular-connected UAV. In the area $\xi ,$ there are J BSs, denoted by $\mathcal { T } \triangleq \{ 1 , 2 , \dots , J \}$ 1 2Each BS j covers a certain number of GDs, denoted by $K _ { j }$ where $K _ { j } \geq 1$ j. Consequently, the total number of GDs in the area Î¾ is $\begin{array} { r } { K = \sum _ { j = 1 } ^ { J } K _ { j } } \end{array}$ . These GDs, situated at fixed locations, = j jcontinuously transmit data to their corresponding BSs through ground-to-ground (G2G) uplink channels. In addition, a cellularconnected UAV is deployed above them to track a moving target, such as a vehicle or a person of interest, where the data captured (e.g., image, video) are transmitted to ground BSs via A2G uplink channels [30], [31]. The UAV flies at a fixed altitude of H to avoid the high energy consumption associated with constant altitude variation [32]. The total flight time of the UAV is denoted as $T ,$ , which is subdivided into N discrete time slots, each with a duration of $\begin{array} { r } { \delta = \frac { T } { N } } \end{array}$ . These time slots are represented by the set $\mathcal { N } \triangleq \{ 1 , 2 , \dots , N \}$ . The horizontal plane coordinates of jth 1 2BS is denoted as $\mathbf { s } _ { i } ^ { \mathrm { B S } } \in \mathbb { R } ^ { 2 \times 1 }$ . The horizontal plane coordinates jof the UAV and the tracked target at time slot n are denoted as $\mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , \mathbf { s } _ { n } ^ { \mathrm { T a r } } \in \mathbb { R } ^ { 2 \times 1 }$ , respectively. In particular, $\mathbf { s } _ { ( 0 ) } ^ { \mathrm { U A V } }$ and ${ \bf s } _ { 0 } ^ { \mathrm { T a r } }$ n ndenote the initial positions of the UAV and the tracked target, respectively. Let $v _ { \mathrm { m a x } }$ represent the UAVâs maximum flight speed. Consequently, at each time slot, the UAVâs flight distance must meet the maximum flight distance constraint, i.e.,

$$
\| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { ( n - 1 ) } ^ { \mathrm { U A V } } \| \leq v _ { \operatorname* { m a x } } \delta , \forall n \geq 1 ,\tag{1}
$$

where  Â·  denotes the euclidean norm. The distance between the UAV and the BS j in time slot n is calculated as $d _ { j , ( n ) } ^ { \mathrm { U A V } } =$ $\sqrt { H ^ { 2 } + \| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { j } ^ { \mathrm { B S } } \| ^ { 2 } } .$

nThe terrestrial mobile target moves according to the Gauss-Markov mobility model [33], [34]. In particular, the direction and speed of the tracked target at time slot n are given by

$$
v _ { n } ^ { \mathrm { T a r } } = \kappa v _ { n - 1 } ^ { \mathrm { T a r } } + ( 1 - \kappa ) \bar { v } + \sqrt { 1 - \kappa ^ { 2 } } v _ { x } ^ { \mathrm { T a r } } ,\tag{2}
$$

$$
\theta _ { n } ^ { \mathrm { T a r } } = \kappa \theta _ { n - 1 } ^ { \mathrm { T a r } } + ( 1 - \kappa ) \bar { \theta } + \sqrt { 1 - \kappa ^ { 2 } } \theta _ { x } ^ { \mathrm { T a r } } .\tag{3}
$$

In this model, $\kappa \in [ 0 , 1 ]$ shows the degree of randomness in [0 1]the tracked targetâs motion, while $\bar { \theta }$ and v denote the targetâs average direction and speed, respectively. Specifically, higher Îº values lead to smoother trajectories that are more influenced by past states, whereas lower Îº values introduce greater variability and unpredictability in the targetâs movement. The variables $v _ { x } ^ { \mathrm { T a } }$ and $\theta _ { x } ^ { \mathrm { T a r } }$ xare Gaussian random variables with zero mean and unit xvariance. These Gaussian random variables introduce stochastic elements into the targetâs motion, capturing real-world uncertainties and ensuring that the instantaneous speed and direction fluctuate around the long-term mean behavior. As a result, the tracked targetâs position at time slot n can be calculated as

$$
\begin{array} { r } { x _ { n } ^ { \mathrm { T a r } } = x _ { n - 1 } ^ { \mathrm { T a r } } + v _ { n - 1 } ^ { \mathrm { T a r } } \delta \cos \theta _ { n - 1 } ^ { \mathrm { T a r } } , } \end{array}\tag{4}
$$

$$
\begin{array} { r } { y _ { n } ^ { \mathrm { T a r } } = y _ { n - 1 } ^ { \mathrm { T a r } } + v _ { n - 1 } ^ { \mathrm { T a r } } \delta \sin \theta _ { n - 1 } ^ { \mathrm { T a r } } . } \end{array}\tag{5}
$$

Although the Gauss-Markov model may not capture all realworld target movement complexities, it balances mathematical tractability and flexibility through the correlation factor Îº, making it suitable for our optimization framework. Additionally, our framework is model-agnostic, allowing seamless integration with more sophisticated mobility models in future work to better represent real-world dynamics. The horizontal distance between the tracked target and the UAV during time slot n is denoted as $d _ { ( n ) } ^ { \mathrm { T a r } } = \parallel \mathbf { s } _ { n } ^ { \mathrm { T a r } ^ { \mathbf { - } } } - \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } \mid$ . In every time slot, the UAV n = n nmaintains reliable tracking by keeping the moving target within its designated tracking radius D, which can be given by

$$
( d _ { ( n ) } ^ { \mathrm { T a r } } ) ^ { 2 } + H ^ { 2 } \leq D ^ { 2 } , ~ \forall n .\tag{6}
$$

## B. Communication Model

For uplink communication resources, the total number of orthogonal RBs (e.g., frequency band) assigned is denoted by M . In practical scenarios, it is common to have $M < K$ due to the reuse of frequencies among the K GDs [35]. The notation $\mathcal { M } \triangleq \{ 1 , 2 , \dots , M \}$ represents the set of RBs. During uplink 1 2data transmission from the UAV to ground BSs, two types of interference are observed: one is A2G interference, caused by the LoS dominance of the A2G channel affecting GDs sharing the same RB; the other is terrestrial interference, resulting from the shared use of RBs among GDs. To mitigate terrestrial interference, an terrestrial interference aware RB allocation strategy is adopted wherein each BS assigns RBs to its GDs with interference mitigation consideration [30]. Specifically, the set of first q-tier neighboring BSs of BS j is defined as $\textstyle { \mathcal { N } } _ { q } ^ { j } , q \geq 1$ . Before assigning an RB to a new GD within the q 1coverage of BS $j ,$ it is essential to verify that the RB is not allocated within the neighboring set $\mathcal { N } _ { q } ^ { j }$ . If the RB is not in use qwithin this neighboring set, it can then be assigned to the GD, thereby minimizing potential terrestrial interference. We define a RB allocation BS set $\mathcal { J } _ { m , n } .$ , where $j \in \mathcal { I } _ { m , n }$ indicates that m,n m,nRB m is allocated to a GD in the cell of BS j during time slot n. This ensures that RB allocation minimizes terrestrial interference among GDs sharing the same RB by keeping track of which BSs have been assigned RB m during each time slot. On the other hand, to alleviate A2G interference, we calculate the complement set $\mathcal { T } _ { m , n } ^ { c } = \mathcal { I } \backslash \mathcal { I } _ { m , n }$ , which represents the set of m,n = m,nBSs not currently utilizing RB m at time slot n. The complement set $\mathcal { T } _ { m , n } ^ { c }$ is essential for mitigating A2G interference as it allows m,nthe UAV to select a ground BS from the set $\mathcal { J } _ { m , n } ^ { c }$ for transmission m,nwith RB m at time slot n, thereby reducing the likelihood of interference. It is worth noting that for any RB m and time slot $n ,$ , the set $\mathcal { J } _ { m , n } ^ { c }$ is always non-empty. The reason is that each BS, m,nand its q-tier neighboring BSs, cannot simultaneously allocate the same RB to their respective covered GDs due to the terrestrial interference aware RB allocation strategy. Following the 3GPP standards, the modeling of G2G and A2G channels is conducted under the Urban Macro (UMa) scenario [36], [37].

1) Ground-to-Ground Channel: Let $k _ { j , m , n }$ denote the index of the GD within the coverage of BS $j ,$ j,m,n, which uploads data to BS j using RB m during time slot n. The channel coefficient between GD $k _ { j , m , n }$ and BS j at time slot n with RB m is represented by $H _ { j , m , n } . H _ { j , m , n }$ is influenced by several factors, j,m,n j,m,nincluding path loss, the antenna gain of the BS, and small-scale fading, which follows the Rayleigh fading model. The uplink data rate for GD $k _ { j , m , n }$ at time slot n with RB m is given by:

$$
R _ { g } ^ { j } ( m , n ) = B \log _ { 2 } \left( 1 + \frac { \hat { p } _ { j , m , n } H _ { j , m , n } } { \sigma _ { j , m , n } ^ { 2 } + p ( m , n ) G _ { m , n } ^ { j } } \right) ,\tag{7}
$$

where $G _ { m , n } ^ { j }$ denotes the channel coefficient between the UAV m,nand BS j for time slot n with RB m. $\hat { p } _ { j , m , n }$ represents the transmit power of the GD $k _ { j , m , n }$ . Term $p ( m , n ) G _ { m , n } ^ { j }$ exists j,m,n ( ) m,nin (7) due to the A2G interference affecting GDs sharing the same RB. B denotes the bandwidth allocated per RB, measured in Hertz (Hz), and $\sigma _ { j , m , n } ^ { 2 }$ signifies the total background noise j,m,npower and remaining interference from other terrestrial cells at cell j for the given time slot n with RB $m .$ . The transmit power of the UAV at time slot n with RB m is denoted as $p ( m , n )$ ( )Subsequently, the cumulative data rate of all GDs at time slot n with RB m is

$$
R _ { g } ( m , n ) = \sum _ { j \in \mathcal { J } _ { m , n } } R _ { g } ^ { j } ( m , n ) .\tag{8}
$$

Then, the G2G throughput for all GDs at time slot n can be calculated as $\Sigma _ { m \in \mathcal { M } } \delta R _ { g } ( m , n )$

m g( )2) Air-to-Ground Channel: Note that $G _ { m , n } ^ { j }$ is the channel m,ncoefficient between the UAV and BS j at time slot n with RB m. Similar to [38], the A2G channel exhibits flat frequency characteristics due to the existance of LoS propagation. Therefore, for each time slot $n ,$ we have $G _ { m , n } ^ { j } = G _ { n } ^ { j } , \forall j \in \mathcal { I } , m \in \mathcal { M }$ m,n = nWe adopt a Rician fading channel model [39], [40], incorporating both LoS and non-Line-of-Sight (NLoS) components, to accurately represent A2G channels in practical urban environments where obstacles affect signal propagation. The channel coefficient $G _ { n } ^ { j }$ is defined as

$$
G _ { n } ^ { j } = \frac { \beta _ { 0 } | \mu _ { n } | ^ { 2 } } { ( H ^ { 2 } + \| s _ { ( n ) } ^ { \mathrm { U A V } } - s _ { j } ^ { \mathrm { B S } } \| ^ { 2 } ) ^ { \alpha / 2 } } ,\tag{9}
$$

where $\begin{array} { r } { \mu _ { n } = \sqrt { \frac { K _ { c } } { K _ { c } + 1 } } \overline { { g } } + \sqrt { \frac { 1 } { K _ { c } + 1 } } \tilde { g } } \end{array}$ , with g representing the deterministic LoS component (with $| \overline { { g } } | = 1 )$ and $\tilde { g }$ denoting the = 1 Ërandom scattered NLoS component, modeled as a zero-mean unit-variance circularly symmetric complex Gaussian (CSCG) random variable. $K _ { c }$ is the Rician factor that quantifies the ratio of power in the LoS component to that in the NLoS components. $\beta _ { 0 }$ is the channel power gain with $d _ { 0 } = 1$ m and $\alpha \geq 2$ is the pass loss component.

For each RB $m \in \mathcal { M }$ at time slot n, we denote $j ( m , n )$ as the ( )index of BS associated with the UAV for uplink transmission, where $j ( m , n ) \in \mathcal { J } _ { m , n } ^ { c }$ is a design variable in this paper. In this ( ) m,ncase, the substantial A2G interference can be mitigated between the UAV and GDs that are covered by BSs in $\mathcal { J } _ { m , n }$ . To evaluate m,ntransmission reliability, we incorporate an outage probability tolerance 	 as described in [41], [42]. The transmission rate from the UAV to BS $j ( m , n )$ using RB m at time slot n is then calculated as

$$
R _ { u } ( m , n ) = B \log _ { 2 } \left( 1 + \frac { F ^ { - 1 } ( \epsilon ) p ( m , n ) G _ { n } ^ { j } } { \Gamma \sigma _ { j ( m , n ) , m , n } ^ { 2 } } \right) ,\tag{10}
$$

where $\sigma _ { j ( m , n ) , m , n } ^ { 2 }$ signifies the total background noise power. $F ( \cdot )$ j m,n ,m,nis the cumulative distribution function (CDF) of the Ri-( )cian fading coefficient while $F ^ { - 1 } ( \cdot )$ is the inverse function, ( )and  represents the SNR gap between practical modulation Îschemes and theoretical Gaussian signaling. Therefore, the A2G throughput of the UAV during time slot n is calculated as $\textstyle \sum _ { m \in { \mathcal { M } } } \delta R _ { u } ( m , n )$

## C. Energy Consumption Model

Energy consumption of the UAV includes both flight energy consumption and communication energy consumption. However, flight energy consumption is vastly greater than communication energy, often by several orders of magnitude, with flight energy typically measured in kilojoules and communication energy in mere joules [43]. Consequently, the overall energy consumption is primarily driven by the flight energy, which is the main focus of this paper. Let $\mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } }$ represent the UAVâs flight velocity during time slot n, where $\begin{array} { r } { \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } = ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { ( n - 1 ) } ^ { \mathrm { U A V } } ) / \delta . } \end{array}$ n = ( n n )The flight power consumption during flight at time slot n is expressed as, i.e.,

$$
P _ { ( n ) } ^ { \mathrm { f } } = \underbrace { C _ { 1 } \left( 1 + \frac { 3 \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \| ^ { 2 } } { U _ { \mathrm { t i p } } ^ { 2 } } \right) } _ { \mathrm { b l a d e p r o f l e } } +
$$

$$
{ \underbrace { C _ { 2 } \sqrt { \sqrt { C _ { 3 } + \frac { \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \| ^ { 4 } } { 4 } } } - \frac { \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \| ^ { 2 } } { 2 } } _ { \mathrm { i n d u c e d } } } + \underbrace { C _ { 4 } \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \| ^ { 3 } } _ { \mathrm { p a r a s i t e } } ,\tag{11}
$$

where $U _ { \mathrm { t i p } }$ refers to the rotorâs tip speed, and $C _ { 1 } , C _ { 2 } , C _ { 3 }$ , and $C _ { 4 }$ are constants related to the UAVâs weight and its aerodynamic parameters [7]. As such, the flight energy consumption at time slot n is given by

$$
E _ { ( n ) } ^ { \mathrm { f } } = P _ { ( n ) } ^ { \mathrm { f } } \delta .\tag{12}
$$

Denote $\overline { { E } } ^ { \mathrm { f } }$ the mean flight energy consumption during the flight, which is calculated as

$$
\overline { { E } } ^ { \mathrm { f } } = \operatorname* { l i m } _ { N  \infty } \frac { 1 } { N } \sum _ { n = 0 } ^ { N - 1 } E _ { ( n ) } ^ { \mathrm { f } } .\tag{13}
$$

Given the UAVâs limited energy budget, flight energy consumption must remain within acceptable limits. The constraint on flight energy consumption is

$$
\overline { { E } } ^ { \mathrm { f } } \leq \overline { { E } } _ { \mathrm { m a x } } ^ { \mathrm { f } } .\tag{14}
$$

Here, $\overline { { E } } _ { \mathrm { m a x } } ^ { \mathrm { f } }$ represents the maximum permissible mean energy consumption. Constraint (14) ensures that the UAV operates within its energy budget, which allows for efficient and sustainable flight operations.

## D. Problem Formulation

To mitigate the significant uplink interference caused by the UAV to non-associated BSs and to balance the trade-off between A2G and G2G uplink throughput. We consider the weighted throughput at time slot $n ,$ which is given by:

$$
\begin{array} { r l } & { \displaystyle Z ( \{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \} ) \triangleq } \\ & { \displaystyle \lambda _ { u } \sum _ { m \in \mathcal { M } } \delta R _ { u } ( m , n ) + \lambda _ { g } \sum _ { m \in \mathcal { M } } \delta R _ { g } ( m , n ) . } \end{array}\tag{15}
$$

Here, $\lambda _ { u } \geq 0$ and $\lambda _ { g } \geq 0$ represent constant weights allocated to u 0 g 0the A2G and G2G throughput, respectively. Due to the randomness introduced by the targetâs movements, our objective is to maximize the long-term average weighted throughput by optimizing the UAVâs trajectory $\{ \mathbf { s } _ { ( n ) } ^ { \mathbf { \overline { { U } } A V } } \}$ }, the uplink BS associations $\{ j ( m , n ) \}$ n, and UAVâs transmit power allocation $\{ p ( m , n ) \}$ ( ) ( )This problem is formulated as a multi-stage stochastic optimization problem:

$$
( \mathrm { P 1 } ) : \operatorname* { m a x } _ { \{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \} } \operatorname* { l i m } _ { N \to + \infty } \operatorname* { m a x } _ { N } \frac { \sum _ { n \in \mathcal { N } } \mathrm { Z } ( \{ \mathbf { s } _ { ( n ) ^ { \flat } } ^ { \mathrm { U A V } } j ( m , n ) , p ( m , n ) \} ) } { N }
$$

s.t. (1), (6), (14),

$$
j ( m , n ) \in \mathcal { I } _ { m , n } ^ { c } , p ( m , n ) \geq 0 , \forall m \in \mathcal { M } , n \in \mathcal { N } ,\tag{16}
$$

$$
\sum _ { m \in \mathcal { M } } p ( m , n ) \leq P _ { \operatorname* { m a x } } , \forall n \in \mathcal { N } ,\tag{17}
$$

where $P _ { \mathrm { m a x } }$ represents the maximum transmit power of the UAV. Constraint (6) ensures that the UAV keeps the moving target within its reliable tracking range D. Constraint (16)

ensures that the UAV can associate with BS $j ( m , n )$ during ( )time slot n only if the RB m is not occupied by any GD. By enforcing this constraint, we prevent potential collisions and ensure efficient use of communication resources between the UAV and the BSs. Constraint (17) represents the maximum transmit power $P _ { \mathrm { m a x } }$ constraint for the UAV. This constraint directly influences communication energy consumption, which balances communication performance with energy efficiency, thus influencing the UAVâs operational behavior and network performance.

Problem (P1) is inherently non-convex and characterized by the randomness of the targetâs movements. Such variability necessitates sophisticated management to ensure that the UAV operates efficiently within its limited energy budget. Solving (P1) requires knowledge of energy consumption across all N time slots, which is impractical to predict in advance. To address this challenge, we develop an optimization framework based on Lyapunov theory [44] that only utilizes energy information from past and current time slots. In the following, Section IV introduces the theoretical framework necessary for transforming and tackling the multi-stage stochastic optimization problem to manageable deterministic problems for each time slot, Section V details the practical implementation of the optimization within each time slot.

## IV. PROPOSED LYAPUNOV-BASED OPTIMIZATION FRAMEWORK

In this section, we develop a Lyapunov-based optimization framework to solve the problem (P1). This framework is particularly effective in addressing the uncertainties and dynamics inherent in stochastic optimization problems by focusing on long-term stability. First, we convert the multi-stage stochastic problem into a single time-slot deterministic problem using Lyapunov optimization theory. To achieve this, we establish a virtual energy-sensitive queue $\{ Q [ n ] \}$ for the constraint (14), which is [ ]designed to track and manage the UAVâs energy consumption over time. This queue evolves as follows:

$$
Q [ n + 1 ] = \operatorname* { m a x } \bigg \{ Q [ n ] - \overline { { E } } _ { \operatorname* { m a x } } ^ { \mathrm { f } } , 0 \bigg \} + E _ { ( n ) } ^ { \mathrm { f } } ,\tag{18}
$$

where $Q [ n ]$ represents the cumulative energy imbalance and $Q [ 0 ] = 0$ [ ]. In (18), the energy consumption $E _ { ( n ) } ^ { \mathrm { f } }$ acts as the arrival rate of $Q [ n ]$ , while $\overline { { E } } _ { \mathrm { m a x } } ^ { \mathrm { f } }$ acts as the service rate of $Q [ n ]$ By maintaining the stability of $Q [ n ]$ , the Lyapunov framework ensures that the system can adapt to stochastic variations in energy consumption. The evolution of this queue helps in monitoring whether the UAVâs energy usage is within acceptable limits. According to [44], queue stability is defined as follows:

Definition 1: A discrete-time queue $\{ Q [ n ] \}$ achieves strong stability if:

$$
\operatorname* { l i m } _ { N \to \infty } { \frac { 1 } { N } } \sum _ { n = 0 } ^ { N - 1 } \mathbb { E } [ Q [ n ] ] \leq + \infty .\tag{19}
$$

Based on this definition, we provide the following lemma.

Lemma 1: Stability of the virtual queue $\{ Q [ n ] \}$ ensures that constraint (14) is met.

Proof: From the evolution of $\{ Q [ n ] \}$ , we have

$$
Q [ n + 1 ] \geq Q [ n ] - \overline { { E } } _ { \operatorname* { m a x } } ^ { \mathrm { f } } + E _ { ( n ) } ^ { \mathrm { f } } , \forall n .\tag{20}
$$

Taking the sum of both sides of (20) and dividing it by N , we obtain:

$$
\frac { Q [ N ] - Q [ 0 ] } { N } + \overline { { { E } } } _ { \mathrm { m a x } } ^ { \mathrm { f } } \geq \frac { 1 } { N } \sum _ { n = 0 } ^ { N - 1 } E _ { ( n ) } ^ { \mathrm { f } } .\tag{21}
$$

According to Definition 1, if the virtual queue $Q [ n ]$ is stable, then we obtain $\begin{array} { r } { \mathfrak { l } _ { n \to \infty } ( \mathbb { E } [ Q [ n ] ] / n ) = 0 . \mathrm { A s } N \to \infty , \frac { Q [ N ] } { N } \mathrm { a p } - } \end{array}$ lproaches zero if $Q [ n ]$ ( [ [ ]] ) = 0 Nis stable, which confirms that the constraint [ ](14) is satisfied due to (21). â¡

We define a quadratic Lyapunov function to measure queue congestion as

$$
J ( Q [ n ] ) = { \frac { 1 } { 2 } } ( Q [ n ] ) ^ { 2 } .\tag{22}
$$

This quadratic form is chosen for its ability to effectively capture queue congestion severity by imposing higher penalties on larger queue states, ensuring mathematical tractability and facilitating the derivation of stability guarantees [7], [8]. In particular, a lower $J ( Q [ n ] )$ suggests that $Q [ n ]$ remains small, thereby guaranteeing the stability of $Q [ n ]$ [ ]. To ensure stability over all N time slots, $J ( Q [ n ] )$ [ ]must be kept small in each slot. To achieve ( [ ])this, we define the conditional Lyapunov drift function, which measures the change in $J ( Q [ n ] )$ between two consecutive time slots, i.e.,

$$
\Delta ( Q [ n ] ) = \mathbb { E } \left[ J ( Q [ n + 1 ] ) - J ( Q [ n ] ) \mid Q [ n ] \right] .\tag{23}
$$

Following (23), we establish the drift-plus-penalty function as

$$
\begin{array} { r l } & { \Delta _ { V } ( Q [ n ] ) = \Delta ( Q [ n ] ) } \\ & { - V \mathbb { E } [ Z ( \{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \} ) | Q [ n ] ] . } \end{array}\tag{24}
$$

Here, $V \geq 0$ represents the Lyapunov parameter, balancing 0the tradeoff between the weighted network throughput and the Lyapunov drift function. This balance is crucial for optimizing performance while maintaining system stability under stochastic conditions. Thus, optimizing trajectory and resource allocation for maximum weighted network throughput and queue stability is achieved by minimizing the drift-plus-penalty function at each time slot. Notably, the conditional Lyapunov drift function defined in (23) is relatively complex to compute. To tackle such issue, we first derive its upper bound by using the following Theorem 1.

Theorem 1: Assume that $\{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \}$ is a feansible solution to problem P , we can obtain an upper bound ( 1)for the drift-plus-penalty function as follows:

$$
\Delta _ { V } ( Q [ n ] ) \leq D _ { n } - \mathbb { E } \biggl [ Q [ n ] \biggl ( \overline { { E } } _ { \mathrm { m a x } } ^ { \mathrm { f } } - E _ { ( n ) } ^ { \mathrm { f } } \biggr ) \bigg | Q [ n ] \biggr ]
$$

$$
- V \mathbb { E } \{ Z ( \{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \} ) | Q [ n ] \} ,\tag{25}
$$

where $D _ { n }$ is a constant.

nProof: By squaring the update rule for $Q [ n ]$ in (18), we obtain

$$
( Q [ n + 1 ] ) ^ { 2 } = \bigg ( \operatorname* { m a x } \bigg \{ Q [ n ] - \overline { { E } } _ { \operatorname* { m a x } } ^ { \mathrm { f } } , 0 \bigg \} + E _ { ( n ) } ^ { \mathrm { f } } \bigg ) ^ { 2 } .\tag{26}
$$

By using the inequality $\{ a - b , 0 \} + c ) ^ { 2 } \leq a ^ { 2 } + b ^ { 2 }$ $c ^ { \bar { 2 } } + 2 a ( \bar { c } - b )$ , we derive

$$
\begin{array} { r } { ( Q [ n + 1 ] ) ^ { 2 } \leq ( Q [ n ] ) ^ { 2 } + \biggl ( \overline { { E } } _ { \operatorname* { m a x } } ^ { \mathrm { f } } \biggr ) ^ { 2 } + \biggl ( E _ { ( n ) } ^ { \mathrm { f } } \biggr ) ^ { 2 } } \\ { + 2 Q [ n ] \biggl ( E _ { ( n ) } ^ { f } - \overline { { E } } _ { \operatorname* { m a x } } ^ { \mathrm { f } } \biggr ) . } \end{array}\tag{27}
$$

Based on (27) and the definition provided in (22), we obtain

$$
\begin{array} { r l r } {  { J ( Q [ n + 1 ] ) - J ( Q [ n ] ) = \frac { 1 } { 2 } ( Q [ n + 1 ] ) ^ { 2 } - \frac { 1 } { 2 } ( Q [ n ] ) ^ { 2 } } } \\ & { } & { \leq D _ { n } + Q [ n ] \bigg ( E _ { ( n ) } ^ { f } - \overline { { E } } _ { \operatorname* { m a x } } ^ { \mathrm { f } } \bigg ) , } \end{array}\tag{28}
$$

where $D _ { n }$ is a constant, given by:

$$
D _ { n } = \frac { 1 } { 2 } \bigg ( \overline { { E } } _ { \mathrm { m a x } } ^ { \mathrm { f } } \bigg ) ^ { 2 } + \frac { 1 } { 2 } \bigg ( E _ { \mathrm { m a x } } ^ { \mathrm { f } } \bigg ) ^ { 2 } ,\tag{29}
$$

where $E _ { \mathrm { m a x } } ^ { \mathrm { f } }$ represents the maximum flight energy consumption of a UAV across all time slots. Therefore, the upper bound for the conditional Lyapunov drift function is:

$$
\begin{array} { r } { \Delta ( Q [ n ] ) \leq D _ { n } - \mathbb { E } \bigg [ Q [ n ] \bigg ( \overline { { E } } _ { \operatorname* { m a x } } ^ { \mathrm { f } } - E _ { ( n ) } ^ { \mathrm { f } } \bigg ) \bigg | Q [ n ] \bigg ] . } \end{array}\tag{30}
$$

The upper bound derived in (30) can be employed to derive the upper bound expression in (25) and the proof concludes.

Inspired by Theorem 1, we minimize the upper bound from (25) rather than directly minimizing the drift-plus-penalty function at each time slot. By removing the constant term $D _ { n }$ , we minimize the following term at each time slot n, i.e.,

$$
\begin{array} { l } { { { \cal F } ( \{ s _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \} ) \triangleq Q [ n ] { \cal E } _ { ( n ) } ^ { \mathrm { f } } } } \\ { { \quad \quad \quad - V Z ( \{ s _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \} ) . } } \end{array}\tag{31}
$$

As a result, solving problem (P1) can be transformed to solving the following problem (P2) for each time slot:

$$
\begin{array} { l } { { ( \mathrm { P 2 } ) : \displaystyle \operatorname* { m i n } _ { \{ s _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \} } F ( \{ s _ { ( n ) } ^ { \mathrm { U A V } } , j ( m , n ) , p ( m , n ) \} ) } } \\ { { \mathrm { s . t . } \quad ( 1 ) , ( 6 ) , ( 1 6 ) , ( 1 7 ) . } } \end{array}
$$

The overall online control algorithm for solving (P1) is summarized in Algorithm 1. To illustrate the overall workflow of our solution, Algorithm 1 operates over discrete time slots to manage the UAVâs operations efficiently. At each time slot $n ,$ the algorithm retrieves the current state of the virtual energy queue $Q [ n ]$ , solves the deterministic optimization problem (P2) [ ]to determine the optimal UAV trajectory, BS associations, and power allocations, and then updates $Q [ n ]$ based on the UAVâs energy consumption. This process ensures online adaptability, maintains energy constraints, and minimizes interference. The Lyapunov framework plays a crucial role in enforcing the energy constraint. By updating the virtual energy queue $Q [ n ]$ based on [ ]the UAVâs energy consumption during each time slot, the framework ensures that the long-term average energy consumption remains within the permissible limits defined by constraint (14), as shown in Lemma 1.

Algorithm 1: Lyapunov-Based Online Control Algorithm   
for Problem (P1).   
1: while $\overline { { n \leq N } }$ do   
2: Obtain Q n ;   
3: [ ] Solve problem (P2) to obtain optimized solution   
$\{ s _ { ( n ) } ^ { \mathrm { U A V } } , \dot { j ( m , n ) } , p ( m , n ) \}$ ;   
4: n ( ) ( ) Update the queue Q n according to (18);   
5: Update $n = n + 1 ;$   
6: end while

## V. SINGLE TIME SLOT OPTIMIZATION

In this section, we focus on solving the deterministic per-slot optimization problem (P2) at time slot n. Though problem (P2) remains non-convex, it can be split into two subproblems and solved iteratively using alternating optimization technique until convergence. Specifically, the two subproblems are: 1) The $\mathrm { U A V } _ { \mathrm { \Delta } }$ trajectory optimization subproblem, 2) The BS association and transmit power allocation subproblem. In the following, we will explain how each subproblem is addressed.

## A. UAVâs Trajectory Optimization Subproblem

Given the transmission power allocation $\{ p ( m , n ) \}$ and BS association $\{ j ( m , n ) \}$ ( ), the UAV trajectory design subproblem is written as

$$
\begin{array} { r l r } { \left. { \mathrm { ( P 3 ) } : \operatorname* { m i n } _ { \{ \stackrel { \mathrm { v i n } } { \infty } , \stackrel { \mathrm { v i n } } { \infty } } \} \mathrm { Q } \mathrm { I n } \big | \delta \bigg ( \mathrm { C } _ { 1 } \left( 1 + \frac { 3 \mathrm { I } \mathrm { V } _ { ( n ) } ^ { \mathrm { U N } } } { \mathrm { I } _ { 0 } ^ { \mathrm { d p } } } \right) ^ { 2 } \bigg ) + } } \\ & { } & \\ & { C _ { 2 } \left( \sqrt { C _ { 3 } + \frac { \mathrm { I } \mathrm { V } _ { ( n ) } ^ { \mathrm { U N } } \mathrm { V } _ { \parallel } ^ { \mathrm { I I } } } { 4 } } - \frac { \mathrm { I } \mathrm { V } _ { ( n ) } ^ { \mathrm { U M N } } { \mathrm { I } _ { 0 } ^ { 2 } } } { 2 } \right) ^ { 1 / 2 } + C _ { 4 } \| \mathrm { V } _ { ( n ) } ^ { \mathrm { U M } } \| ^ { 3 } \right) } \\ & { } & \\ & { } & { - V \sum _ { m \in \cal { M } } \delta ( \lambda _ { m } R _ { n } ( m , n ) + \lambda _ { g } R _ { g } ( m , n ) ) } \\ & { } & { \mathrm { s . t . } \ ( \mathrm { l } ) , \ ( \mathrm { l } ) , } \\ & { } & { \mathrm { v } _ { ( n ) } ^ { \mathrm { U M } } = ( \mathrm { v } _ { ( n ) } ^ { \mathrm { U M } } - \mathrm { s } _ { ( n - 1 ) } ^ { \mathrm { U M } } ) / \delta , \ \forall n . } \end{array}\tag{2}
$$

The objective function in (P3) is non-convex with respect to $\mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } }$ due to the non-convex terms $T M _ { ( n ) } \triangleq$ $\sqrt { \left( \sqrt { C _ { 3 } + \frac { \Vert \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \Vert ^ { 4 } } { 4 } } - \frac { \Vert \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \Vert ^ { 2 } } { 2 } \right) }$ and $T M _ { ( m , n ) } \triangleq - ( \lambda _ { u } R _ { u }$ $( { \dot { m } } , n ) + \lambda _ { g } R _ { g } ( m , n ) ) , m \in { \mathcal { M } }$ $n \in { \mathcal { N } } .$ . We first transform ( ) + g g( ))the objective function into a convex function by introducing slack variables. Specifically, for the non-convex term $T M _ { ( n ) }$ , we introduce the slack variable $\tau _ { ( n ) }$ such that:

$$
\tau _ { ( n ) } \geq \sqrt { \left( \sqrt { C _ { 3 } + \frac { \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \| ^ { 4 } } { 4 } } - \frac { \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \| ^ { 2 } } { 2 } \right) } ,
$$

then we have

$$
\frac { C _ { 3 } } { \tau _ { ( n ) } ^ { 2 } } \leq \tau _ { ( n ) } ^ { 2 } + \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \| ^ { 2 } .\tag{33}
$$

To handle the non-convex term $T M _ { ( m , n ) }$ , we introduce slack variables $y _ { ( m , n ) }$ and $z _ { ( m , n ) }$ m,n, and have the following constraints:

$$
y _ { ( m , n ) } \geq \big \| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { j ( m , n ) } ^ { \mathrm { B S } } \big \| ^ { 2 } , ~ \forall m , n ,\tag{34}
$$

$$
z _ { ( m , n ) } \geq ( H ^ { 2 } + \big \| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { j ( m , n ) } ^ { \mathrm { B S } } \big \| ^ { 2 } ) ^ { - 1 } , \forall m , n .\tag{35}
$$

With such relaxation, problem (P3) can be transformed into

$$
\begin{array} { r l } {  { ( \mathrm { P 4 } ) : \underbrace { \operatorname* { m i n } _ { \{ \begin{array} { c } { { \scriptstyle \mathbf { u } } ^ { W M } , \mathbf { v } } \\ { { \scriptstyle \mathbf { u } } ^ { W } , \mathbf { v } } \\ { { \scriptstyle \mathbf { u } } ^ { W } , \mathbf { v } } \\ { { \scriptstyle \mathbf { u } } ^ { W } , \mathbf { v } } \\ { { \scriptstyle \mathbf { u } } ^ { W } , \mathbf { v } } \end{array} } } \operatorname { Q } [ \mathrm { n } ] \delta \bigg ( \mathrm { C } _ { 1 } + \frac { 3 C _ { 1 } \| \mathbf { v } _ { ( 1 ) } ^ { W M } \| ^ { 2 } } { \mathrm { U } _ { ( 1 ) } ^ { \omega } } } } \\ & { \ } \\ &  \ +  \begin{array} { l } { \gamma _ { ( 4 ) } , } \\ { C _ { 4 } \| \mathbf { v } _ { ( n ) } ^ { W M } \| ^ { 3 } + C _ { 2 } \tau _ { ( n ) } \bigg ) - V \delta \sum _ { \begin{array} { c } { { \scriptstyle \mathbf { \hat { u } } } } \\ { { \scriptstyle \mathbf { m } \in { \cal A } } } \end{array} } B } \\ & { \ } \\ & { \times [ \lambda _ { \mathrm { u } } \log _ { 2 } ( 1 + \frac { p ( m , n ) \beta _ { 0 } } { \sigma _ { j , ( m , n ) , ( m , n ) } ^ { 2 } \times ( \bar { H } ^ { 2 } + y _ { ( m , n ) } ) ^ { \omega / 2 } } )  } \\ &   + \lambda _ { g } \sum _ { \begin{array} { c } { { \scriptstyle \mathbf { \hat { l } } } } \\ { { \scriptstyle \mathbf { \hat { l } } } ^ { W M } , \mathbf { n } } \\ { { \scriptstyle \mathbf { u } } ^ { W } , \mathbf { n } } \end{array} } \mathrm { l o g } _ { 2 } ( 1 + \frac { \hat { p } _ { j , m , n } H _ { j , m , n } } { \sigma _ { j , ( m , n ) } ^ { 2 } + p ( m , n ) \beta _ { 0 } \sigma _ { ( m , n ) } ^ { 2 } }  \end{array} \end{array}
$$

s.t. (1), (6), (32)â(35).

Theorem 2: Problem (P4) is equivalent to problem (P3). Proof: Suppose $\{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V , * } } , \tau _ { ( n ) } ^ { * } , \boldsymbol { \dot { y } } _ { ( m , n ) } ^ { * } , z _ { ( m , n ) } ^ { * } \}$ is the optimal n n m,n m,nsolution of problem (P4), then the following equation holds:

$$
\begin{array} { r l } & { \tau _ { ( n ) } ^ { * } = \sqrt { \left( \sqrt { C _ { 3 } + \frac { \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } , * } \| ^ { 4 } } { 4 } } - \frac { \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } , * } \| ^ { 2 } } { 2 } \right) } , ~ \forall n , } \\ & { y _ { ( m , n ) } ^ { * } = \| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , * } - \mathbf { s } _ { j ( m , n ) } ^ { \mathrm { B S } } \| ^ { 2 } , ~ \forall m , n , } \\ & { z _ { ( m , n ) } ^ { * } = \big ( H ^ { 2 } + \| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , * } - \mathbf { s } _ { j ( m , n ) } ^ { \mathrm { B S } } \| ^ { 2 } \big ) ^ { - 1 } , ~ \forall m , n , } \end{array}\tag{36}
$$

where $\begin{array} { r } { \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V , * } } = ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V , * } } - \mathbf { s } _ { ( n - 1 ) } ^ { \mathrm { U A V } } ) / \delta . } \end{array}$ . Since otherwise, we can n = ( n n )further reduce the objective value by choosing a smaller $\tau _ { ( n ) } , y _ { ( m , n ) }$ and $z _ { ( m , n ) }$ without violating the constraints (33)â n m,n m,n(35). Therefore, problem (P4) is equivalent to the problem (P3) due to (36). 

For problem (P4), the objective function and the constraints (33) and (35) remain non-convex. Similar to [7], the SCA method is adopted to tackle the non-convexity. The central concept of SCA involves approximating the non-convex problem as a convex one at each local point in every iteration. We achieve a locally optimal solution for (P4) through iterative resolution of a series of approximated convex optimization problems.

Proposition 1: For any vector $\mathbf { x } \in \mathbb { R } ^ { n }$ with a given point $\mathbf { x } ^ { l } \in$ $\mathbb { R } ^ { n }$ , the norm squared $| | \dot { \bf x } | | ^ { 2 }$ is lower-bounded by

$$
| | \mathbf { x } | | ^ { 2 } \geq | | \mathbf { x } _ { } ^ { l } | | ^ { 2 } + 2 ( \mathbf { x } _ { } ^ { l } ) ^ { \top } ( \mathbf { x } _ { } - \mathbf { x } _ { } ^ { l } ) ,\tag{37}
$$

where $[ \cdot ] ^ { \top }$ denotes the transpose.

[ ]Proof: Consider the function $g ( \mathbf { x } ) = | | \mathbf { x } | | ^ { 2 }$ , which is a convex ( ) =function. The first-order Taylor expansion of g at $\mathbf { x } ^ { l }$ is given by

$$
g ( \mathbf { x } ) \geq g ( \mathbf { x } ^ { l } ) + \nabla g ( \mathbf { x } ^ { l } ) ^ { \top } ( \mathbf { x } - \mathbf { x } ^ { l } ) ,\tag{38}
$$

where $\nabla g ( \mathbf { x } ^ { l } ) = 2 \mathbf { x } ^ { l }$ . Substituting $g ( \mathbf { x } ) = | | \mathbf { x } | | ^ { 2 }$ and $g ( \mathbf { x } ^ { l } ) =$ $| | \mathbf { x } ^ { l } | | ^ { 2 }$ ( ) = 2, we obtain the conclusion.

Given the function $f ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , \tau _ { ( n ) } ) \triangleq \tau _ { ( n ) } ^ { 2 } + \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A V } } \| ^ { 2 }$ , and a local point ${ \mathbf s } _ { ( n ) } ^ { { \mathrm { U A V } } , l }$ at the lth iteration, we can obtain the lower bound $f ^ { l } ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , \tau _ { ( n ) } )$ by applying Proposition 1 as: $f ^ { l } ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , \tau _ { ( n ) } ) \triangleq$ $\begin{array} { r } { ( \tau _ { ( n ) } ^ { l } ) ^ { 2 } + 2 \tau _ { ( n ) } ^ { l } ( \tau _ { ( n ) } - \tau _ { ( n ) } ^ { l } ) + \frac { \| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , l } - \mathbf { s } _ { ( n - 1 ) } ^ { \mathrm { U A V } } \| ^ { 2 } } { \delta ^ { 2 } } + \frac { 2 } { \delta ^ { 2 } } \big ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , l } - \mathbf { s } _ { ( n - 1 ) } ^ { \mathrm { U A V } , l } \big ) ^ { 2 } , } \end{array}$ $\mathbf { s } _ { ( n - 1 ) } ^ { \mathrm { U A V } } \Big ) ^ { \top } \left( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , l } \right)$ , where $\tau _ { ( n ) } ^ { l }$ is defined as: $\tau _ { ( n ) } ^ { l } =$ $\begin{array} { r } { \sqrt { \left( \sqrt { C _ { 3 } + \frac { \| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { ( n - 1 ) } ^ { \mathrm { U A V } } \| ^ { 4 } } { 4 \delta ^ { 4 } } } - \frac { \| \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { ( n - 1 ) } ^ { \mathrm { U A V } } \| ^ { 2 } } { 2 \delta ^ { 2 } } \right) } } \end{array}$ . Similarly, for the function $\phi ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } ) \triangleq H ^ { 2 } + \Vert \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { j ( m , n ) } ^ { \mathrm { B S } } \Vert ^ { 2 }$ and a local point ${ \mathbf s } _ { ( n ) } ^ { { \mathrm { U A V } } , l }$ at the lth iteration, we obtain the lower bound by applying Proposition 1 as: $\phi ^ { l } ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } ) \triangleq H ^ { 2 } + \Vert \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , l } -$ $\mathbf { s } _ { j ( m , n ) } ^ { \mathrm { B S } } \Vert ^ { 2 } + 2 ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , l } - \mathbf { s } _ { j ( m , n ) } ^ { \mathrm { B S } } ) ^ { \top } ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } - \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , l } )$ . âm, n. m,n n j m,n n nBased on the above analysis, at the lth iteration, constraints (33) and (35) can be approximated as:

$$
\frac { C _ { 3 } } { \tau _ { ( n ) } ^ { 2 } } \leq f ^ { l } ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , \tau _ { ( n ) } ) , ~ \forall n ,\tag{39}
$$

$$
\frac { 1 } { z _ { ( m , n ) } } \leq \phi ^ { l } ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } ) , \forall m , n ,\tag{40}
$$

where $f ^ { l } ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } , \tau _ { ( n ) } )$ and $\phi ^ { l } ( \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } )$ are linear functions, thus ( n n ) ( n )ensuring (39) and (40) are convex constraints.

Proposition 2: For any variable x with a given point $x ^ { l }$ and $\alpha \geq 2 ,$ the function $\begin{array} { r } { \dot { \log _ { 2 } } ( 1 + \frac { A } { C + { x ^ { \alpha / 2 } } } ) } \end{array}$ is lower-bounded as 2follows:

$$
\begin{array} { l } { { \log _ { 2 } \left( 1 + \frac { A } { C + x ^ { \alpha / 2 } } \right) \geq \log _ { 2 } \left( 1 + \frac { A } { C + ( x ^ { l } ) ^ { \alpha / 2 } } \right) } } \\ { { + \frac { A \cdot \frac { \alpha } { 2 } ( x ^ { l } ) ^ { \alpha / 2 - 1 } } { \ln ( 2 ) \left( C + ( x ^ { l } ) ^ { \alpha / 2 } \right) \left( 1 + \frac { A } { C + ( x ^ { l } ) ^ { \alpha / 2 } } \right) } ( x - x ^ { l } ) . } } \end{array}\tag{41}
$$

Proof: Consider the function $\begin{array} { r } { f ( x ) = \log _ { 2 } \left( 1 + \frac { A } { C + x ^ { \alpha / 2 } } \right) } \end{array}$ Due to (38), we compute the derivative $\begin{array} { r } { f ^ { \prime } ( x ) = \frac { 1 } { \ln ( 2 ) } } \end{array}$ $\frac { - A \cdot { \frac { \alpha } { 2 } } x ^ { \alpha / 2 - 1 } } { ( C + x ^ { \alpha / 2 } ) ( 1 + { \frac { A } { C + x ^ { \alpha / 2 } } } ) }$ . Then, substituting $f ( x ^ { l } )$ and $f ^ { \prime } ( x ^ { l } )$ into (38), we obtain the result in (41).

Given functions $g _ { 1 } ( y _ { ( m , n ) } ) \triangleq \lambda _ { u } \log _ { 2 } ( 1 +$ $\frac { p ( m , n ) \beta _ { 0 } } { \sigma _ { j ( m , n ) , m , n } ^ { 2 } ( H ^ { 2 } + y _ { ( m , n ) } ^ { \alpha / 2 } ) } \Big )$ and $\begin{array} { r } { g _ { 2 } \mathopen { } \mathclose \bgroup \left( z _ { ( m , n ) } \aftergroup \egroup \right) \triangleq \lambda _ { g } \sum _ { j \in \mathcal { J } _ { m , n } } \log _ { 2 } } \end{array}$ $\begin{array} { r } { ( 1 + \frac { \hat { p } _ { j , m , n } H _ { j , m , n } } { \sigma _ { j , m , n } ^ { 2 } + p ( m , n ) \beta _ { 0 } z _ { ( m , n ) } ^ { \alpha / 2 } } ) } \end{array}$ . By using Proposition 2, we can Ïapproximate $g _ { 1 }$ m,n Î²and $g _ { 2 }$ to obtain the desired lower bounds, i.e.,

$$
\begin{array} { r l } & { g _ { 1 } ^ { l } ( y _ { ( m , n ) } ) \triangleq \lambda _ { u } \log _ { 2 } \Biggl ( 1 + \frac { p ( m , n ) \beta _ { 0 } } { \sigma _ { j ( m , n ) , m , n } ^ { 2 } ( H ^ { 2 } + ( y _ { ( m , n ) } ^ { l } ) ^ { \alpha / 2 } ) } \Biggr ) } \\ & { \qquad - \lambda _ { u } \cdot \frac { \alpha } { 2 \ln ( 2 ) } \cdot \frac { p ( m , n ) \beta _ { 0 } } { \sigma _ { j ( m , n ) , m , n } ^ { 2 } } \cdot \frac { ( y _ { ( m , n ) } - y _ { ( m , n ) } ^ { l } ) } { ( H ^ { 2 } + ( y _ { ( m , n ) } ^ { l } ) ^ { \alpha / 2 + 1 } ) } } \\ & { \qquad \times \frac { 1 } { 1 + \frac { p ( m , n ) \beta _ { 0 } } { \sigma _ { j ( m , n ) , m , n } ^ { 2 } ( H ^ { 2 } + ( y _ { ( m , n ) } ^ { l } ) ^ { \alpha / 2 } ) } } , } \end{array}
$$

Algorithm 2: Iterative Algorithm to UAVâs Trajectory Op  
timization.   
1: Initialize $\{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , 1 } , S ^ { 1 } \}$ .;   
2: Set $l \gets 1 ;$   
3: repeat   
4: Obtain the optimal solution for (P5) as   
$\{ \mathbf s _ { ( n ) } ^ { \mathrm { U A V } , l + 1 } , S ^ { \bar { l } + 1 } \}$ based on $\{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , l } \}$ ;   
n5: Update $l \gets l + 1 ;$   
6: until $\frac { | S ^ { l + 1 } - S ^ { l } | } { S ^ { l } } \leq \epsilon ,$ where 	 denotes the accuracy.

$$
g _ { 2 } ^ { l } { \left( z _ { \left( m , n \right) } \right) } \triangleq
$$

$$
\begin{array} { r l r } { \mathrm { ( P 5 ) } : \underset { \{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A } } , \tau _ { ( n ) } , \mathbf { y } _ { ( m , n ) } , z _ { ( m , n ) } \} } { \mathrm { m i n } } \mathrm { Q } [ \mathrm { n } ] \delta \Bigg ( \mathrm { C } _ { 1 } + \frac { 3 \mathrm { C } _ { 1 } \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A } } \| ^ { 2 } } { \mathrm { U } _ { \mathrm { i p } } ^ { 2 } } } & \\ { \quad } & { } & \\ { \quad } & { \quad + C _ { 4 } \| \mathbf { v } _ { ( n ) } ^ { \mathrm { U A } } \| ^ { 3 } + C _ { 2 } \tau _ { ( n ) } \Bigg ) } \\ { \quad } & { } & \\ { \quad } & { \quad - V B \delta \sum _ { m \in \cal { M } } \bigg ( g _ { 1 } ^ { l } ( y _ { ( m , n ) } ) + g _ { 2 } ^ { l } ( z _ { ( m , n ) } ) \bigg ) } \\ { \quad } & { } & \\ { \mathrm { s . t . } \ ( 1 ) , ( 6 ) , ( 3 2 ) , ( 3 4 ) , ( 3 9 ) , ( 4 0 ) . } & \end{array}
$$

Problem (P5) is convex and standard convex optimization solvers such as CVX [45] can be utilized to solve (P5) efficiently. Note that due to the global lower bounds established in (39) and (40) and Proposition 2, satisfying the constraints of problem (P5) ensures that the constraints of the original problem (P4) are also met. By iteratively updating the local points at each iteration through solving (P5) with SCA technique, we develop an efficient algorithm for addressing the non-convex problem (P4) or its original form (P3), as outlined in Algorithm 2, where $S ^ { l }$ represent the objective value for (P5) in the lth iteration. By following similar arguments in [43], [46], it can be demonstrated that Algorithm 2 with SCA technique is guaranteed to converge to a solution that satisfies the Karush-Kuhn-Tucker (KKT) conditions of problem (P4).

## B. The BS Association and Transmit Power Allocation Subproblem

For given UAVâs trajectory $\{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } } \}$ , the BS association and ntransmit power allocation subproblem can be expressed as

$$
\operatorname* { m i n } _ { \{ j ( m , n ) , p ( m , n ) \} } - V \biggl ( \lambda _ { u \in \mathcal { M } } \delta R _ { u } ( m , n ) + \lambda _ { g \sum _ { m \in \mathcal { M } } } \delta R _ { g } ( m , n ) \biggr )\tag{P6}
$$

s.t. (16), (17).

From the following Theorem, we can easily obtain the optimal BS association for (P6).

Theorem 3: The optimal BS association to problem (P6) can be obtained as $\begin{array} { r } { j ^ { * } ( m , n ) = \arg \operatorname* { m a x } _ { j \in \mathcal { I } _ { m , n } ^ { c } } \frac { G _ { n } ^ { j ( m , n ) } } { \sigma _ { j ( m , n ) , m , n } ^ { 2 } } , } \end{array}$ âm $\in { \mathcal { M } } .$

Proof: We prove it by contradiction. Assume that $j ^ { * } ( m , n )$ is ( )not the optimal BS association. Note that the BS association $\{ j ( m , n ) \}$ is only related to A2G uplink transmission rate $R _ { u } ( \boldsymbol { m } , n )$ . This assumption implies that there exists another u( )feasible cell association solution, denoted by $j ^ { 0 } ( m , n )$ , such that the A2G throughput with $j ^ { 0 } ( m , n )$ ( )is higher than that with $j ^ { * } ( m , n )$ . Thus, we have

$$
\begin{array} { r } { \displaystyle \sum _ { m \in \mathcal { M } } \log _ { 2 } \left( 1 + \frac { p ( m , n ) G _ { n } ^ { j ^ { 0 } ( m , n ) } } { \sigma _ { j ^ { 0 } ( m , n ) , m , n } ^ { 2 } } \right) > } \\ { \displaystyle \sum _ { m \in \mathcal { M } } \log _ { 2 } \left( 1 + \frac { p ( m , n ) G _ { n } ^ { j ^ { * } ( m , n ) } } { \sigma _ { j ^ { * } ( m , n ) , m , n } ^ { 2 } } \right) . } \end{array}\tag{42}
$$

However, due to the definition of $j ^ { * } ( m , n )$ , we have $\begin{array} { r } { \frac { G _ { n } ^ { j ^ { * } ( m , n ) } } { \sigma _ { j ^ { * } ( m , n ) , m , n } ^ { 2 } } \geq \frac { G _ { n } ^ { j ^ { 0 } ( m , n ) } } { \sigma _ { j ^ { 0 } ( m , n ) , m , n } ^ { 2 } } , \forall m \in \mathcal { M } } \end{array}$ . Since $\log _ { 2 } ( x )$ is a monotonically increasing function, this implies that $\scriptstyle \sum _ { m \in { \mathcal { M } } } \log _ { 2 } ( 1 +$ $\begin{array} { r } { \frac { p ( m , n ) G _ { n } ^ { j ^ { * } ( m , n ) } } { \sigma _ { j ^ { * } ( m , n ) , m , n } ^ { 2 } } ) \geq \sum _ { m \in \mathcal { M } } \log _ { 2 } \bigl ( 1 + \frac { p ( m , n ) G _ { n } ^ { j ^ { 0 } ( m , n ) } } { \sigma _ { j ^ { 0 } ( m , n ) , m , n } ^ { 2 } } \bigr ) } \end{array}$ . This directly contradicts (42) that the A2G throughput with $j ^ { 0 } ( m , n )$ is higher than that with $j ^ { * } ( m , n )$ . Therefore, $j ^ { * } ( m , n )$ ( )is the ( ) ( )optimal BS association to problem (P6), which concludes the proof. 

Theorem 3 demonstrates that the optimal BS association remains unaffected by the UAVâs transmit power allocation $\{ p ( m , n ) \}$ , which simplifies the optimization process. For brevity, we introduce notation $\begin{array} { r } { G _ { m , n } ^ { * } \triangleq \frac { { G _ { n } ^ { j } } ^ { * } \left( m , n \right) } { \sigma _ { j ^ { * } \left( m , n \right) , m , n } ^ { 2 } } , \forall m \in } \end{array}$ $\mathcal { M } , n \in \mathcal { N }$ , and (P6) is simplified as

$$
\begin{array} { r l } {  { ( \mathrm { P } ^ { 7 } ) : \operatorname* { m a x } _ { \{ p ( m , n ) \} } } } & { \lambda _ { u } \sum _ { m \in \mathcal { M } } \delta \log _ { 2 } ( 1 + p ( m , n ) G _ { m , n } ^ { * } ) } \\ & { \quad \quad \quad + \lambda _ { g } \sum _ { m \in \mathcal { M } } \delta R _ { g } ( m , n ) } \\ & { \mathrm { s . t . } \quad \sum _ { m \in \mathcal { M } } p ( m , n ) \le P _ { \operatorname* { m a x } } , \forall n \in \mathcal { N } , } \\ & { \quad \quad p ( m , n ) \ge 0 , \forall m \in \mathcal { M } , n \in \mathcal { N } . } \end{array}\tag{43}
$$

(44)

Due to its non-concave objective function, problem (P7) is a non-convex optimization problem. To address this challenge, we employ the SCA technique to achieve a locally optimal solution. In the rth iteration, we introduce $p ^ { r } ( m , n )$ as the power allocation for the UAV. Given $\{ p ^ { r } ( m , n ) \}$ ( ), we can obtain a lower bound for $R _ { g } ( m , n )$ ( )by employing first-order Taylor approximation, i.e.,

$$
R _ { g } ( \boldsymbol { m } , \boldsymbol { n } ) \geq \sum _ { j \in \mathcal { I } _ { \boldsymbol { m } , \boldsymbol { n } } } B \log _ { 2 } \left( 1 + \frac { \hat { p } _ { j , \boldsymbol { m } , \boldsymbol { n } } H _ { j , \boldsymbol { m } , \boldsymbol { n } } } { \sigma _ { j , \boldsymbol { m } , \boldsymbol { n } } ^ { 2 } E ^ { r } ( \boldsymbol { m } , \boldsymbol { n } ) } \right)
$$

Algorithm 3: Iterative Algorithm to Transmit Power Allo  
cation.   
1: Initialize $\{ p ^ { 1 } ( m , n ) , P ^ { 1 } \}$   
2: Set $r \gets 1 ;$   
3: repeat   
4: Obtain the optimal solution for (P8) as   
$\{ p ^ { r + 1 } ( m , n ) , P ^ { r + 1 } \}$ based on $\{ p ^ { r } ( m , n ) \}$   
(5: Update $r  r + 1 ;$   
6: until $\begin{array} { r } { \frac { | P ^ { r + 1 } - P ^ { r } | } { P ^ { r } } \leq \epsilon , } \end{array}$ where 	 denotes the accuracy.

Algorithm 4: Alternative Optimization Algorithm (AOA)   
for Problem (P2).   
1: Initialize $\{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , 0 } , j ^ { 0 } ( m , n ) , p ^ { 0 } ( m , n ) \}$   
n ( ) ( )2: Set the iteration index and the threshold parameter as   
$r = 0$ and $\epsilon = 1 0 ^ { - 4 } $ ;   
= 03: repeat   
4: With the given $\{ p ^ { r } ( m , n ) \}$ and $\{ j ^ { r } ( m , n ) \}$ , solve the   
( ) ( )UAV trajectory design subproblem (P3) and obtain the   
updated UAV position $\{ \mathbf { s } _ { ( n ) } ^ { \mathbf { U A V } , r + 1 } \}$ using Algorithm 2;   
5: With the given $\{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , r + 1 } \}$ , obtain the optimal cell   
association solution $\{ j ^ { r + 1 } ( m , n ) \}$ for (P6) according   
to Theorem 3;   
6: With the given $\{ \mathbf { s } _ { ( n ) } ^ { \mathrm { U A V } , r + 1 } \}$ and $\{ j ^ { r + 1 } ( m , n ) \}$ , update   
the transmission power $\{ p ^ { r + 1 } ( m , n ) \}$ using   
Algorithm 3;   
7: Update the objective value of problem (P2) to $F ^ { r + 1 }$   
using the updated variables $\{ \mathbf { s } _ { ( n ) } ^ { \mathbf { \bar { U } A V } , r + 1 } \}$ ï¼   
$\{ j ^ { r + 1 } ( m , n ) \}$ , and $\{ p ^ { r + 1 } ( m , \stackrel { . } { n } ) \}$   
(8: Update $r = r + 1 ;$   
9: until $\begin{array} { r } { \frac { | F ^ { r + 1 } - F ^ { r } | } { F ^ { r } } \leq \epsilon . } \end{array}$

$$
- C ^ { r } ( m , n ) ( p ( m , n ) - p ^ { r } ( m , n ) ) , \forall m , n ,\tag{45}
$$

where $\begin{array} { r } { E ^ { r } ( m , n ) = 1 + \frac { p ^ { r } ( m , n ) G _ { n } ^ { j } } { \sigma _ { j , m , n } ^ { 2 } } , C ^ { r } ( m , n ) = \sum _ { j \in \mathcal { I } _ { m , n } } } \end{array}$ $\frac { \smile \sim \ n F \gamma , m , n ^ { \perp \cdot \lambda } \jmath , m , n } { ( \ln 2 ) ( \sigma _ { \jmath , m , n } ^ { 2 } E ^ { r } ( m , n ) + \hat { p } _ { \jmath , m , n } H _ { \jmath , m , n } ) \sigma _ { \jmath , m , n } ^ { 2 } E ^ { r } ( m , n ) }$ j Ë H . Therefore, in Ï E m,n p H Ï E m,nthe rth iteration, (P7) is approximated as the following problem, i.e.,

$$
\begin{array} { r } { ( \mathrm { P 8 } ) : \underset { \{ \mathrm { p } ( \mathrm { m } , \mathrm { n } ) \} } { \mathrm { m a x } } \ \lambda _ { u } \delta \underset { m \in \mathcal { M } } { \sum } B \log _ { 2 } ( 1 + p ( m , n ) G _ { m , n } ^ { u } ) } \\ { - \lambda _ { g } \delta \underset { m \in \mathcal { M } } { \sum } C ^ { r } ( m , n ) p ( m , n ) } \\ { \mathrm { s } . \mathrm { t } . \ ( 4 3 ) , ( 4 4 ) , } \end{array}
$$

where the objective function omits the constant term for brevity. Note that (P8) is a convex optimization problem and can be solved efficiently by existing optimization tools such as CVX. Let $P ^ { r }$ represent the objective value for (P8) in the rth iteration. The following Algorithm 3 summarizes the proposed iterative approach.

To effectively solve problem (P2) at each time slot, we propose an iterative algorithm which optimizes the subproblems (P3)

and (P6) alternatively, and the details are summarized in Algorithm 4. Note that Algorithm 1 simplifies the complex stochastic optimization problem by converting it into a deterministic problem for each time slot. In each time slot, the two subproblems are transformed into convex optimization problems, which are then alternately optimized using Algorithms 2 and 3, both of which employ the interior point method. The computational complexity of this process is primarily influenced by the number of variables [47]. Consequently, the overall computational complexity of Algorithm 4 for each time slot is $\mathcal { O } ( L M ^ { 3 . 5 } )$ , where L denotes (the number of iterations with the order $\mathcal { O } ( \log ( \frac { 1 } { \epsilon } ) )$ . To further enhance computational efficiency, we note the potential of employing advanced optimization tools such as CVXGEN [48]. CVXGEN is capable of reducing computation times by up to 1000 times compared to standard CVX-based implementations, potentially bringing the running time down to the order of milliseconds. This significant improvement would ensure that the algorithms remain highly efficient and practically affordable for UAV online operations.

## VI. SIMULATION RESULTS

In this section, simulations are conducted to evaluate the performance of the proposed schemes for target tracking and communication optimization in cellular-connected UAV networks. The simulations aim to demonstrate the effectiveness of the algorithm in various scenarios, highlighting improvements in network throughput, queue stability, and energy efficiency.

## A. Simulation Setup

As shown in Fig. 2, we have set up $J = 6 1 ~ \mathrm { B S s }$ , each with = 61a height of 25 meters and an adjacent level set at $q = 2$ , with a = 2cell radius of 500 meters. The BSs are distributed across four layers of cellular networks, covering an area with $K = 7 0 \mathrm { G D s }$ = 70whose positions are randomly generated. The network operates over $M = 4 0$ RBs across $T = 3 0 0 { \mathrm { s } }$ for target tracking tasks, = 40 = 300with the UAV operating at an altitude of $H = 1 0 0$ m and a time interval of $\delta = 1 \mathrm { s } .$ = 100. For target tracking, the tracking range is set to $D = 3 0 0 \mathrm { m }$ 1. We consider the practical Rician fading chan-= 300nels [40] with Rician factor $K _ { c } ,$ and the CDF function $F ( \cdot )$ can be expressed as $F ( z ) = 1 - Q _ { 1 } ( \sqrt { 2 K _ { c } } , \sqrt { 2 ( K _ { c } + 1 ) z } )$ ( ), where $Q _ { 1 } ( a , b )$ ( ) = 1 ( 2 c 2is the Marcum-Q function, with $K _ { c } = 3 0 \mathrm { d B } , \Gamma =$ $5 \mathrm { d B } , \epsilon = 0 . 1 $ . The noise power density is $\sigma ^ { 2 } = 1 0 ^ { - 1 4 } \mathrm { W / H z }$ 5 = 0 1with a path loss exponent of $\alpha = 2$ = 10, and the channel power gain is $\beta _ { 0 } = - 5 0 \mathrm { d B }$ = 2. Each RB is allocated a bandwidth of $B = 1 \mathrm { k H z }$ = 50GDs transmit at a power of $\hat { p } _ { j , m , n } = 2 0$ = 1dBm, while the maximum UAV transmit power is $P _ { \mathrm { m a x } } = 3 0$ dBm. The UAVâs maximum flight speed is $V _ { \mathrm { m a x } } = 5 0$ = 30m/s, with a maximum average energy consumption of $\overline { E } _ { \mathrm { m a x } } ^ { f } = 8 0 0$ Joule. Similar to [33], the = 800targetâs movement follows the Gauss-Markov mobility model, with a mean speed of $\overline { { v } } = 4 0 \mathrm { { m } / \mathrm { { s } } }$ , a mean direction of $\theta = \pi / 4$ ï¼ and a target randomness level set to $\kappa = 0 . 8 .$

For energy related parameters, we set $C _ { 1 } = 7 . 9 9 \mathrm { W }$ and $C _ { 2 } =$ =. W, as well as aerodynamic constants $C _ { 3 } = 2 6 3 . 7 6$ =and $C _ { 4 } = 0 . 0 0 9 2$ . The rotor blade tip speed is $U _ { \mathrm { t i p } } = 1 2 0$ 263 76m/s. Unless otherwise stated, the throughput weights are set to $\lambda _ { u } = 1$ and $\lambda _ { g } = 1$ , and the penalty weight value is $V = 1 0$ u = 1. The parameter settings are referenced from relevant literature [3], [4], [30], [32]. All simulations were conducted using MATLAB R2022a with the CVX package and SeDuMi solver on a standard dual-core 3.20 GHz CPU with 32 GB memory.

<!-- image-->  
(a)Î¸=0

<!-- image-->  
(c)Î¸=-Ï  
Fig. 2. Optimized trajectory for target tracking.

## B. Optimized Tracking Trajectory and Power Allocation With BS Association

Fig. 2 shows the optimized trajectories of the UAV while tracking the target under various movement scenarios. The targetâs speed v is set to 40 m/s, with the direction Î¸ varying among $\{ 0 , - \pi / 2 , - \pi , \pi / 2 \}$ . These parameters represent differ-0 2 2ent movement patterns of the target, including up, down, left, and right directions. In all scenarios depicted in Fig. 2, the UAV successfully tracks the target, maintaining it within the specified tracking range D. The UAVâs trajectory adapts dynamically to the targetâs movements, ensuring continuous observation. The online adjustment of the UAVâs trajectory highlights the algorithmâs robustness and responsiveness, which is crucial for reliable target tracking.

<!-- image-->  
(b) $\bar { \theta } = - \pi / 2$

<!-- image-->  
(d) $\bar { \theta } = \pi / 2$

Based on the target movement in Fig. 2(d), Fig. 3 shows the optimized power allocation to different RBs at various time slots, aimed at maximizing throughput within the energy budget. The curves indicate that the UAV dynamically adjusts its power distribution among different RBs to maximize throughput with interference avoidance. Significant variations in power allocation are observed at time slots 60, 120, 180, and 240, with specific RBs receiving higher power to ensure higher throughput with less interference.

Fig. 4 illustrates the BS association under different time slots and RBs in the scenario of Fig. 2(d). Results for other similar scenarios have been omitted for brevity. The UAVâs association with various BSs changes over time, which reflects its strategy to connect to the optimal BS with the least interference. For example, at time slot 240, the UAV is associated with BS 20 through RB 18 and RB 29, while the remaining RBs are associated with BS 10. This dynamic association demonstrates the UAVâs ability to select BSs that offer better communication quality, even if they are not the closest in proximity. The UAV dynamically adjusts its trajectory and power allocation in response to the targetâs movements and the network conditions, demonstrating the robustness and efficiency of the proposed algorithm.

<!-- image-->  
Fig. 3. The power allocation to different RBs at different time slots.

<!-- image-->  
Fig. 4. The BS association under different time slots and RBs.

## C. Benchmark Comparisons

To better illustrate the superiority of the proposed scheme with AOA, we compare it with several benchmark schemes: 1) Target path following benchmark (TPF) [49], where the UAV follows the same trajectory as the target; 2) High-speed tracking benchmark (HST), where the UAV flies at the maximum speed that corresponds to the average maximum flight energy consumption while still satisfying tracking requirements; 3) Energy-efficient predicted tracking benchmark (EEPT) [5], where the target location is predicted based on Elman neural network with the aim of energy minimization. 4) No Lyapunov benchmark (NL) [27], which strictly requires the energy consumption to meet the target value for each time slot, without utilizing the Lyapunov method. 5) Nearest BS maximum power benchmark (NBMP) [50], where the UAV associates with the nearest BS and selects an available RB not occupied by any GDs with maximum transmit power; 6) Equal power allocation benchmark (EPA) [51], where the UAV allocates the transmit power equally across all RBs; 7) Interference-free scheme benchmark (IF) [30], where the UAV transmits in the RBs which are not utilized by any GDs in any cells.

<!-- image-->  
Fig. 5. Performance comparisons between the proposed solution and benchmark schemes.

Fig. 5 demonstrates the relationship between system throughput and the UAVâs maximum transmit power $P _ { \mathrm { m a x } } .$ . It is observed that the proposed AOA consistently outperforms the benchmark schemes, showing a higher throughput as $P _ { \mathrm { m a x } }$ increases. The TPF benchmark maintains a consistent path, which limits its adaptability and potential communication improvements through UAV trajectory optimization. The HST benchmark ensures maximum speed but fails to balance throughput and energy consumption. The EEPT benchmark prioritizes energy efficiency over communication performance, resulting in lower throughput as it focuses on tracking performance based on predicted tracking, which limits its optimization for communication. The NL benchmark shows relatively lower throughput as it strictly enforces energy consumption limits for each time slot, which results in suboptimal communication performance while ensuring compliance with energy constraints. The NBMP benchmark and EPA benchmark show relatively lower throughput due to inefficient power allocation with more interference. The IF benchmark avoids interference but results in lower throughput due to inefficient use of available RBs. Thus, the proposed solution effectively balances power allocation, interference management, and adaptation to the current communication environment, which results in superior performance in terms of throughput under limited energy budget.

## D. Analysis of System Stability and Flight Speed

Fig. 6 shows that while the average queue length (AQL) gradually increases with a higher Lyapunov control parameter V , it remains lower than most of the benchmark schemes, except for the EEPT benchmark, which achieves the smallest AQL by sacrificing throughput. The observed increase in AQL for the proposed AOA as $V$ increases is due to the system prioritizing throughput more as V grows, which inevitably impacts queue stability. In contrast, other benchmarks show constant AQLs because they do not use V to balance throughput and queue length. The EEPT benchmark focuses solely on minimizing energy consumption, leading to the lowest queue length at the expense of throughput. The proposed AOA, while not achieving the minimum AQL, strikes a balance between queue length and throughput, offering a more stable and energy-efficient solution. Other benchmarks, such as the TPF benchmark, HST benchmark and NL benchmark, exhibit larger queue lengths due to their less adaptive nature in handling dynamic communication environments.

<!-- image-->  
Fig. 6. The average queue length versus control parameter V .

<!-- image-->  
Fig. 7. Optimized UAVâs speed under different time slots.

Fig. 7 illustrates the UAVâs speed during flight for various schemes. Based on the tracking trajectory in Fig. 2(a), our proposed scheme AOA dynamically adjusts the UAVâs speed in response to the communication environment, maintaining a moderate average speed compared to other benchmarks. This adaptability ensures stable and energy-efficient operation. For the TPF benchmark scheme, the UAVâs speed closely follows the targetâs trajectory, resulting in an average speed of 40 m/s. The HST benchmark scheme maintains a constant maximum speed of 41 m/s, always moving at its highest possible speed while satisfying energy constraints. The EEPT benchmark scheme focuses on minimizing energy usage, resulting in the propulsion power efficient speed of 12.9 m/s. Although it is energy-efficient, it sacrifices throughput performance as previously shown in the performance comparisons. Our proposed scheme achieves an average speed of 33.5 m/s, striking a balance between maximizing throughput and minimizing energy consumption. This online adjustment to environmental conditions contributes to overall system stability and performance.

Fig. 8. The throughput versus control parameter V .  
<!-- image-->

<!-- image-->  
Fig. 9. The average UAVâs speed versus control parameter V .

The proposed scheme AOA also demonstrates superior performance across various metrics as the Lyapunov control parameter V varies. Fig. 8 shows that it consistently achieves the highest average throughput, highlighting its effectiveness in optimizing communication performance. As the Lyapunov control parameter V increases, the system progressively shifts its focus towards enhancing throughput. This is reflected in the figure, where a noticeable and steady increase in throughput is observed as V becomes larger, indicating the systemâs capacity to significantly improve throughput as the control parameter is adjusted. In contrast, the TPF benchmark achieves the lowest throughput due to its lack of an optimized trajectory planning strategy, which limits its ability to effectively manage communication resources. The EEPT benchmark prioritizes minimizing energy consumption through predicted tracking, but this comes at the expense of throughput, resulting in significantly lower throughput values. These benchmarks, by not adequately balancing throughput with their respective goals, fall short in optimizing overall communication performance compared to the proposed scheme. Fig. 9 illustrates the UAVâs dynamic speed adjustment, maintaining a moderate average speed compared to other benchmarks, thus balancing throughput and energy efficiency. We can observe that as V increases, the speed of the proposed algorithm also shows an increasing trend, further confirming that with a higher V , the system prioritizes throughput more heavily, leading to increased energy consumption and impacting queue stability as previously discussed.

## VII. CONCLUSION

This paper explores the challenges of integrating cellularconnected UAV for dynamic target tracking, with a particular focus on managing unpredictable flight energy consumption and mitigating uplink interference. We develope a multi-stage stochastic optimization framework to enhance communication performance by optimizing the long-term average of uplink throughput for both aerial and ground users. By employing the Lyapunov optimization technique, we transformed the complex, stochastic problem into a deterministic format manageable for each time slot. Our proposed online strategy optimizes BS association, power allocation, and UAV trajectory by leveraging the optimal structure and the SCA method. Simulation results demonstrate that the proposed solution not only improves network throughput but also ensures stability in the UAV energy queue compared with baseline schemes. Future research directions include exploring more sophisticated mobility models and dynamic spectrum allocation, extending the framework to larger-scale networks to facilitate real-world implementations, and addressing perception and computation losses to enhance system performance.

## REFERENCES

[1] Y. Li and A. H. Aghvami, âRadio resource management for cellularconnected UAV: A learning approach,â IEEE Trans. Commun., vol. 71, no. 5, pp. 2784â2800, May 2023.

[2] G. Chen, C. Cheng, X. Xu, and Y. Zeng, âMinimizing the age of information for data collection by cellular-connected UAV,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 9631â9635, Jul. 2023.

[3] Y. Zeng, X. Xu, S. Jin, and R. Zhang, âSimultaneous navigation and radio mapping for cellular-connected UAV with deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 20, no. 7, pp. 4205â4220, Jul. 2021.

[4] C. Zhan and Y. Zeng, âEnergy minimization for cellular-connected UAV: From optimization to deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5541â5555, Jul. 2022.

[5] Z. Wang, J. Du, C. Jiang, Y. Ren, and X.-P. Zhang, âUAV-assisted target tracking and computation offloading in USV-based MEC networks,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 11389â11405, Dec. 2024.

[6] Z. Xia et al., âMulti-agent reinforcement learning aided intelligent UAV swarm for target tracking,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 931â945, Jan. 2022.

[7] Z. Yang, S. Bi, and Y.-J. A. Zhang, âOnline trajectory and resource optimization for stochastic UAV-enabled MEC systems,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5629â5643, Jul. 2022.

[8] K. Guo, R. Gao, W. Xia, and T. Q. S. Quek, âOnline learning based computation offloading in MEC systems with communication and computation dynamics,â IEEE Trans. Commun., vol. 69, no. 2, pp. 1147â1162, Feb. 2021.

[9] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âCellularconnected multi-UAV MEC networks: An online stochastic optimization approach,â IEEE Trans. Commun., vol. 70, no. 10, pp. 6630â6647, Oct. 2022.

[10] Y. Zeng, J. Lyu, and R. Zhang, âCellular-connected UAV: Potential, challenges, and promising technologies,â IEEE Wireless Commun., vol. 26, no. 1, pp. 120â127, Feb. 2019.

[11] R. Amorim et al., âMeasured uplink interference caused by aerial vehicles in LTE cellular networks,â IEEE Wireless Commun. Lett., vol. 7, no. 6, pp. 958â961, Dec. 2018.

[12] W. Tang, H. Zhang, Y. He, and M. Zhou, âPerformance analysis of multi-antenna UAV networks with 3D interference coordination,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5145â5161, Jul. 2022.

[13] Y. Su, H. Zhou, Y. Deng, and M. Dohler, âEnergy-efficient cellularconnected UAV swarm control optimization,â IEEE Trans. Wireless Commun., vol. 23, no. 5, pp. 4127â4140, May 2024.

[14] S. Zhang and R. Zhang, âRadio map-based 3D path planning for cellular-connected UAV,â IEEE Trans. Wireless Commun., vol. 20, no. 3, pp. 1975â1989, Mar. 2021.

[15] H. Sun, L. Zhang, J. Hou, T. Q. S. Quek, X. Wang, and Y. Zhang, âCoMP transmission in downlink NOMA-based cellular-connected UAV networks,â IEEE Trans. Wireless Commun., vol. 23, no. 7, pp. 7392â7407, Jul. 2024.

[16] Y. Wu, K. H. Low, and C. Lv, âCooperative path planning for heterogeneous unmanned vehicles in a search-and-track mission aiming at an underwater target,â IEEE Trans. Veh. Technol., vol. 69, no. 6, pp. 6782â6787, Jun. 2020.

[17] J. Moon, S. Papaioannou, C. Laoudias, P. Kolios, and S. Kim, âDeep reinforcement learning multi-UAV trajectory control for target tracking,â IEEE Internet Things J., vol. 8, no. 20, pp. 15441â15455, Oct. 2021.

[18] S. Hu, X. Yuan, W. Ni, X. Wang, and A. Jamalipour, âVisual-based moving target tracking with solar-powered fixed-wing UAV: A new learning-based approach,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 8, pp. 9115â9129, Aug. 2024.

[19] L. Zhou, S. Leng, Q. Liu, and Q. Wang, âIntelligent UAV swarm cooperation for multiple targets tracking,â IEEE Internet Things J., vol. 9, no. 1, pp. 743â754, Jan. 2022.

[20] Y. Yu et al., âDistributed multi-agent target tracking: A nash-combined adaptive differential evolution method for UAV systems,â IEEE Trans. Veh. Technol., vol. 70, no. 8, pp. 8122â8133, Aug. 2021.

[21] S. Hu, W. Ni, X. Wang, A. Jamalipour, and D. Ta, âJoint optimization of trajectory, propulsion, and thrust powers for covert UAV-on-UAV video tracking and surveillance,â IEEE Trans. Inf. Forensics Secur., vol. 16, pp. 1959â1972, 2021.

[22] J. Li et al., âUAV-RIS-aided space-air-ground integrated network: Interference alignment design and DoF analysis,â IEEE Trans. Wireless Commun., vol. 23, no. 9, pp. 11678â11692, Sep. 2024.

[23] A. Rahmati et al., âDynamic interference management for UAV-assisted wireless networks,â IEEE Trans. Wireless Commun., vol. 21, no. 4, pp. 2637â2653, Apr. 2022.

[24] Z. Ning et al., âJoint user association, interference cancellation and power control for multi-IRS assisted UAV communications,â IEEE Trans. Wireless Commun., vol. 23, no. 10, pp. 13408â13423, Oct. 2024.

[25] U. Challita, W. Saad, and C. Bettstetter, âInterference management for cellular-connected UAVs: A deep reinforcement learning approach,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2125â2140, Apr. 2019.

[26] N. Lin, H. Tang, L. Zhao, S. Wan, A. Hawbani, and M. Guizani, âA PDDQNLP algorithm for energy efficient computation offloading in UAV-assisted MEC,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8876â8890, Dec. 2023.

[27] X. Dai, B. Duo, X. Yuan, and M. D. Renzo, âEnergy-efficient UAV communications in the presence of wind: 3D modeling and trajectory design,â IEEE Trans. Wireless Commun., vol. 23, no. 3, pp. 1840â1854, Mar. 2024.

[28] J. Liu and H. Zhang, âHeight-fixed UAV enabled energy-efficient data collection in RIS-aided wireless sensor networks,â IEEE Trans. Wireless Commun., vol. 22, no. 11, pp. 7452â7463, Nov. 2023.

[29] B. Li, Q. Li, Y. Zeng, Y. Rong, and R. Zhang, â3D trajectory optimization for energy-efficient UAV communication: A control design perspective,â IEEE Trans. Wireless Commun., vol. 21, no. 6, pp. 4579â4593, Jun. 2022.

[30] W. Mei, Q. Wu, and R. Zhang, âCellular-connected UAV: Uplink association, power control and interference coordination,â IEEE Trans. Wireless Commun., vol. 18, no. 11, pp. 5380â5393, Nov. 2019.

[31] C. Zhan, H. Hu, J. Wang, Z. Liu, and S. Mao, âTradeoff between age of information and operation time for UAV sensing over multi-cell cellular networks,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2976â2991, Apr. 2024.

[32] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for multi-UAV enabled wireless networks,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2109â2121, Mar. 2018.

[33] H. Saito, âTheoretical analysis of nonlinear energy harvesting from wireless mobile nodes,â IEEE Trans. Wireless Commun. Lett, vol. 10, no. 9, pp. 1914â1918, Sep. 2021.

[34] Y. Zhang, Z. Kuang, Y. Feng, and F. Hou, âTask offloading and trajectory optimization for secure communications in dynamic user Multi-UAV MEC systems,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 14427â14440, Dec. 2024.

[35] Z. Wang, J. Zong, Y. Zhou, Y. Shi, and V. W. S. Wong, âDecentralized multi-agent power control in wireless networks with frequency reuse,â IEEE Trans. Commun., vol. 70, no. 3, pp. 1666â1681, Mar. 2022.

[36] C. A. Ballanis, Antenna Theory: Analysis and Design. New York, NY, USA: Wiley, 2016.

[37] Study on enhanced LTE support for aerial vehicles, document TR-36.7773 GPP, 2017. [Online]. Available: https://www.3gpp.org/dynareport/36777. htm

[38] H. Rao, S. Xiao, S. Yan, J. Wang, and W. Tang, âOptimal geometric solutions to UAV-enabled covert communications in line-of-sight ccenarios,â IEEE Trans. Wireless Commun., vol. 21, no. 12, pp. 10633â10647, Dec. 2022.

[39] H. Yang, Y. Ye, X. Chu, and S. Sun, âEnergy efficiency maximization for UAV-enabled hybrid backscatter-harvest-then-transmit communications,â IEEE Trans. Wireless Commun., vol. 21, no. 5, pp. 2876â2891, May 2022.

[40] Y. Zeng, X. Xu, and R. Zhang, âTrajectory design for completion time minimization in UAVâenabled multicasting,â IEEE Trans. Wireless Commun., vol. 17, no. 4, pp. 2233â2246, Apr. 2018.

[41] Z. Yang, S. Bi, and Y.-J. A. Zhang, âDeployment optimization of dual-functional UAVs for integrated localization and communication,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 9672â9687, Dec. 2023.

[42] C. Zhan, Y. Zeng, and R. Zhang, âEnergy-efficient data collection in UAV enabled wireless sensor network,â IEEE Wireless Commun. Lett., vol. 7, no. 3, pp. 328â331, Jun. 2018.

[43] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[44] M. J. Neely, âStochastic network optimization with application to communication and queueing systems,â Synth. Lect. Commun. Netw., vol. 3, no. 1, pp. 1â211, 2010.

[45] M. Grant and S. Boyd, âCVX: MATLAB software for disciplined convex programming, version 2.1,â 2016. [Online]. Available: http://cvxr.com/cvx

[46] A. Zappone, E. BjÃ¶rnson, L. Sanguinetti, and E. Jorswieck, âGlobally optimal energy-efficient power control and receiver design in wireless networks,â IEEE Trans. Signal Process., vol. 65, no. 11, pp. 2844â2859, Jun. 2017.

[47] T. Ma et al., âUAV-LEO integrated backbone: A ubiquitous data collection approach for B5G internet of remote things networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3491â3505, Nov. 2021.

[48] J. Mattingley and S. Boyd, âCVXGEN: A code generator for embedded convex optimization,â Optim. Eng., vol. 13, no. 1, pp. 1â27, Mar. 2012.

[49] T. Dang, C. Liu, and M. Peng, âLow-latency mobile virtual reality content delivery for unmanned aerial vehicle-enabled wireless networks with energy constraints,â IEEE Trans. Veh. Technol., vol. 72, no. 2, pp. 2189â2201, Feb. 2023.

[50] K. Meng, Q. Wu, S. Ma, W. Chen, K. Wang, and J. Li, âThroughput maximization for UAV-enabled integrated periodic sensing and communication,â IEEE Trans. Wireless Commun., vol. 22, no. 1, pp. 671â687, Jan. 2023.

[51] F. Pervez, L. Zhao, and C. Yang, âJoint user association, power optimization and trajectory control in an integrated satellite-aerial-terrestrial network,â IEEE Trans. Wireless Commun., vol. 21, no. 5, pp. 3279â3290, May 2022.

<!-- image-->

Cheng Zhan (Member, IEEE) received the BEng and PhD degrees in computer science from the School of Computer Science, University of Science and Technology of China, Anhui, China, in 2006 and 2011 respectively. From 2009 to 2010, he was a research assistant with the Department of Computer Science, City University of Hong Kong. From 2016 to 2017, he was a visiting scholar with the Department of Electrical and Computer Engineering, National University of Singapore. He is currently a Professor with the School of Computer and Information Science, Southwest University, China. His research interests include unmanned aerial vehicle communications, multimedia communications, wireless sensor networks, and network coding. He served as a TPC Member for the ICC, GLOBECOM, WCNC, and UIC.

<!-- image-->

Huan Yan (Graduate Student Member, IEEE) received the bachelorâs degree from the School of Computer and Information Science, Southwest University, in 2022. She is currently working toward the masterâs degree in computer science and technology. Her research interests primarily focus on unmanned aerial vehicle (UAV) communications and multimedia communications.

<!-- image-->

<!-- image-->

Rongfei Fan (Member, IEEE) received the BE degree in communication engineering from the Harbin Institute of Technology, Harbin, China, in 2007, and the PhD degree in electrical engineering from the University of Alberta, Edmonton, Alberta, Canada, in 2012. Since 2013, he has been a faculty member with the Beijing Institute of Technology, Beijing, China, where he is currently an associate professor with the School of Cyberspace Science and Technology. His research interests include edge computing, federated learning, resource allocation in wireless networks, and statistical signal processing.

2013, etc. He served as an associate editor of IEEE Transactions on Multimedia and Ad Hoc Networks, and a TPC Member of Infocom, ACM Multimedia, AAAI, IJCAI, etc.

Han Hu (Member, IEEE) received the BE and PhD degrees from the University of Science and Technology of China, China, in 2007 and 2012, respectively. He is currently a professor with the School of Information and Electronics, Beijing Institute of Technology, China. His research interests include multimedia networking, edge intelligence and space-air-ground integrated network. He received several academic awards, including Best Paper Award of IEEE TCSVT 2019, Best Paper Award of IEEE Multimedia Magazine 2015, Best Paper Award of IEEE Globecom

<!-- image-->

Shubin Xu received the PhD degree from the University of Science and Technology of China, Hefei, China, in 2009. He is currently a research professor with CETC Advanced Mobile Communication Innovation Center, Beijing, China. His research interests include network security, deep-learning-enabled network flow control, and the Internet of Things security.

<!-- image-->

Jian Yang (Senior Member, IEEE) received the BS and PhD degrees from the University of Science and Technology of China (USTC), Hefei, China, in 2001 and 2006, respectively. He is currently a professor in the School of Information Science and Technology, USTC. His research interests include future network, distributed system design, modeling and optimization, multimedia over wired and wireless and stochastic optimization. Dr. Yang received Lu Jia-Xi Young Talent Award from Chinese Academy of Sciences, in 2009.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV/page_11_img_1.jpeg|page_11_img_1]]
3. [[../extracted_images/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV/page_15_img_1.jpeg|page_15_img_1]]
4. [[../extracted_images/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV/page_15_img_2.jpeg|page_15_img_2]]
5. [[../extracted_images/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV/page_15_img_3.jpeg|page_15_img_3]]
6. [[../extracted_images/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV/page_15_img_4.jpeg|page_15_img_4]]
7. [[../extracted_images/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV/page_15_img_5.jpeg|page_15_img_5]]
8. [[../extracted_images/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV/page_15_img_6.jpeg|page_15_img_6]]

---

