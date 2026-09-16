# UAV-Assisted Wireless Cooperative Communication and Coded Caching: A Multiagent Two-Timescale DRL Approach

Bingxin Tian , Li Wang , Senior Member, IEEE, Lianming Xu, Wen Pan, Huaqing Wu , Member, IEEE, Liang Li , Member, IEEE, and Zhu Han , Fellow, IEEE

AbstractâIn emergency scenarios, strong mobility and serious interference cause unstable transmission of on-site information such as close-up photos and high resolution videos, which requires a robust temporary communication network. In this paper, we focus on a UAV-assisted wireless cooperative communication and coded caching network, where emergency command vehicles and a UAV serve as content providers (CPs) to cache and transmit coded fragments or complete files for rescuers regarded as content requesters (CRs). The delivery success probability and content hit ratio are theoretically derived by incorporating the physical connectivity and social relationship between CPs and CRs. Aiming at maximizing the overall content hit ratio, we propose a multiagent two-timescale deep reinforcement learning (MA2T-DRL) algorithm to jointly optimize the transmission power and caching strategies for CPs. Specifically, we develop a two tier

deep-Q networks (DQNs) framework integrating a slow-timescale DQN (ST-DQN) and a fast-timescale DQN (FT-DQN) for caching decision-making and power decision-making respectively, and then the QMIX framework is leveraged to aggregate all the outputs from local ST-DQNs. Considering the cooperative characteristics of coded caching, we further propose a novel clustering method for CPs such that CPs in the same cluster have the same willingness to serve CRs, and each cluster is regarded as the agent for training which further reduces the aggregation scale of the mixing network. Simulation results show that the proposed MA2T-DRL algorithm is efficient in model training, and presents the advantages in performance and complexity compared with the single-agent centralized training and the multiagent independent distributed training.

Index TermsâWireless coded caching, resource allocation, deep reinforcement learning, social relationship.

## I. INTRODUCTION

I N EMERGENCY scenarios, such as floods, earthquakes,and urban fires in mega-cities, it is often difficult to achieve and urban fires in mega-cities, it is often difficult to achieve reliable communications between victims and rescuers due to complex onsite situations, so it is vital to develop robust emergency networks. A mission cognitive wireless emergency network (MCWEN) in [1] has addressed these challenges by leveraging edge-based technologies, including edge caching, edge computing, and edge learning. Among them, wireless edge caching can reduce the burden of temporary networks and improve the services [2]. The popular files can be intelligently cached at network edge, such as emergency command vehicles or UAVs [3].

The wireless edge caching network enables direct content sharing via device-to-device (D2D) communications without routing through any infrastructure, thereby decreasing access latency and backhaul cost [4]. However, the caching performance can be significantly affected by mobility because the contact duration between mobile users is limited and may not be able to support the entire file delivery [5]. Coded caching can offer redundancy by splitting the file into several small pieces and storing these coded fragments in several CPs to improve caching reliability [6]. In particular, D2D coded caching was first considered in [7], where centralized and decentralized caching schemes have been proposed for the case when users have equal cache sizes. However, in emergency scenarios, there are command relationships between commanders and rescuers

This article has supplementary downloadable material available at https://doi.org/10.1109/TMC.2023.3298641, provided by the authors.

<!-- image-->  
Fig. 1. UAV-assisted wireless coded caching network in emergency communications.

when sharing files, which can be regarded as social relationships. Commanders are more willing to share files with professional forces as they have strong social ties [8], but they may refuse to share with non-governmental organizations. The social relationship between D2D users has been considered in [9] to optimize the deployment of cache placement, which achieves a better performance in more practical scenarios. A social-aware spectrum sharing and caching helper selection strategy in [10] exploits the resources of the mobile users, including downlink spectrum resources and caching storage resources, to offload the videos in dense D2D 5 G networks. Therefore, the social-aware D2D coded caching can effectively ensure communication reliability, service scalability and trustworthiness of acquired data.

Besides wireless caching of D2D users, cache-enabled UAVs can dynamically cache the popular contents, track the mobility patterns of ground users, and then effectively serve them. A cache-enabled UAV network framework has been presented in [11] to alleviate the heavy traffic on congested backhauls. The UAVs can serve mobile users through cache units instead of fetching the contents from the internet. The joint optimization of UAV deployment, caching placement, and user association has been studied in [12] to maximize the quality of experience (QoE) of users, which is evaluated by mean opinion score. In addition to caching resources, the resource allocation considering the communications and computing resources in UAV-assisted wireless network has been studied in [13]. The optimal user task offloading to the available computing choices is formulated as a maximization problem of each userâs satisfaction, and confronted as a non-cooperative game. However, the data offloading in UAV-assisted wireless network focuses on the uplinks, where the ground users offload their tasks to neighboring UAVs, while the caching service focuses on the downlinks, where UAVs deliver files to ground users. Thus, cache-enabled UAVs can effectively make up for the deficiency of ground D2D caching. However, as the environment becomes more and more random and dynamic, it is challenging to develop flexible optimization algorithms for UAV or D2D users to optimize their caching strategies.

Model-free reinforcement learning (RL) is an efficient solution to tackle the above issue. Compared with the single agent RL [14], a multiagent system involves computational agents that are homogeneous or heterogeneous, and they may involve activity on the part of agents having common goals or distinct goals [15]. The current multiagent algorithms are mainly categorized into centralized training with the decentralized execution (CTDE) framework and the centralized critic distributed actors (CCDA) framework, which are applicable to deep-Q network (DQN) and actor critic (AC) networks, respectively. As the model structure of the CCDA framework is more complex with higher training cost, we employ the QMIX algorithm [15], which adopts the CTDE framework. Specifically, the central unit makes use of the global environment information to train the neural network parameters, while each agent makes independent decisions only based on its local observations. The QMIX framework has been leveraged in [16] to aggregate multiple UAVsâ local parameterized deep Q-network (P-DQN) for resource allocation and trajectory design. A QMIX-aided routing in social-based delay-tolerant networks has been proposed in [17] for nodes to cooperatively learn the routing policy. The QMIX algorithm has also been used in D2D underlay cache-enabled networks [18], where each requesting user is an agent capable of deciding which cache device to pair with. Although these works can guide us to learning-based caching, it remains unclear how to leverage state-of-the-art RL to make decisions with diverse delay sensitivities (e.g., wireless resource allocation and content caching placement).

The dynamic update of power allocation and content placement requires different system costs, which also lead to different delay sensitivities. Specifically, the power allocation is determined in a fast timescale while the content placement is performed in a slow timescale. However, to the best of our knowledge, there is little work considering the diverse delay sensitivity when training different strategies by QMIX. In this work, we investigate a distributed coded caching strategy in D2D-enabled heterogeneous networks. The D2D-enabled CPs apply $( n , k )$ MDS code [19] to improve the robustness of content ( )delivery, and we propose a QMIX-aided MA2T-DRL algorithm to achieve the joint optimization of the communication and caching for ground CPs. The cache-enabled UAV is dispatched to provide proactive caching when CRs cannot retrieve the requested files from ground CPs. The particle swarm optimization (PSO) algorithm and the greedy algorithm are used to obtain the content placement and trajectory of the UAV due to their low computational cost and fast convergence [20].

The main contributions of this paper are three-folds:

1) We design a distributed coded caching scheme in D2Denabled emergency communication networks and formulate a joint communication and caching optimization problem, where the analysis and derivation of the delivery success probability and content hit ratio are, respectively, presented by incorporating the characteristics of physical connectivity and social relationship.

2) Targeting at maximizing the overall content hit ratio, we propose a multiagent DRL framework MA2T-DRL as a solution. To handle the diverse delay sensitivities of power allocation and content placement, we leverage two tier DQNs operating in two different timescales. The FT-DQN in the bottom tier makes delay-sensitive decisions (i.e., the power allocation strategies) in a fast timescale, whereas the ST-DQN in the top tier makes delay-insensitive decisions (i.e., the content placement strategies) in a slow timescale.

3) We leverage the QMIX framework to aggregate the local ST-DQNs, where joint action value is computed by a mixing network with the global state as input. As the centralized training generally has high complexity with the increase of agents, we further propose a novel clustering method for CPs, under which the CPs in the same cluster have the same willingness to serve CRs and one of the CPs in each cluster is regarded as the agent to reduce the aggregation scale of the mixing network.

The remainder of this paper is organized as follows: In Section II, the system model is presented and the general problem formulation is given. In Section III, the detailed derivation on maximizing the overall content hit ratio is analyzed. The overall optimization process is described in Section IV, where the MA2T-DRL algorithm is proposed. Numerical results are carried out in Section V. Finally, the conclusions are drawn in Section VI. For convenience, Table I lists the main notations used in this paper.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

## A. System Description

We investigate the problem of UAV-assisted edge caching in emergency scenarios as illustrated in Fig. 1, which consists of typical scenarios with different mobility and content preference of ground users. For example, scenario 1 is an emergency power grid patrol scenario. The power transmission lines are always seriously damaged due to extreme weather. Considering the geographical extent and overhanging nature, the combination of emergency vehicles and UAV power line patrol mode is particularly suitable for the emergency high-voltage line patrol [21]. Both of them are equipped with thermal imaging cameras, and the ground workers tend to download the images of damaged surfaces of high-voltage lines. Scenarios 2 and 3 in Fig. 1 are disaster scenarios with high mobility, and people prefer messages or audio data of safety instruction information to guide their escapes. Emergency communication services are very important. However, the existing communication networks may be severely damaged or congested. Therefore, users in each scenario need edge caching to reduce transmission latency and backhaul load.

TABLE I NOTATION SUMMARY
<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $r e q _ { j , f }$ </td><td>Probability that file f is requested by  ${ \overline { { N _ { C R , j } } } } .$ </td></tr><tr><td> $\Delta$ </td><td>Time length of one time slot [sec].</td></tr><tr><td> $\mathbf { Q }$ </td><td>UAV flying trajectory  $\mathbf { Q } = [ \mathbf { q _ { 1 } } , \mathbf { q _ { 2 } } , \dots , \mathbf { q _ { T } } ] .$ </td></tr><tr><td> $v _ { \mathrm { m a x } }$ </td><td>Maximum speed of UAV [m/sec].</td></tr><tr><td> $R _ { i , j }$ </td><td>Data rate between  $N _ { C P , i }$  and  $N _ { C R , j }$  [bits/sec].</td></tr><tr><td> $R _ { u , j }$ </td><td>Data rate betweenUAV and  $N _ { C R , j }$  [bits/sec].</td></tr><tr><td> $T _ { i , j }$ </td><td>Contact duration between  $N _ { C P , i }$  and  $N _ { C R , j } \ [ \mathrm { s e c } ] .$ </td></tr><tr><td> $P r ^ { s d }$ </td><td>Delivery success probability.</td></tr><tr><td> $P r ^ { H i t }$ </td><td>Content hit ratio.</td></tr><tr><td> $h$ </td><td>UAV flying height [m].</td></tr><tr><td> $R$ </td><td>UAV coverage radius [m].</td></tr><tr><td> $P ( V )$   $E _ { p }$ </td><td>UAV propulsion power consumption [J].</td></tr><tr><td></td><td>UAV propulsion energy consumption [J].</td></tr><tr><td> ${ \bf A } _ { \underline { { N } } \times F } ^ { c p }$ </td><td>Content placement vector of CPs.</td></tr><tr><td> $\mathbf { A } ^ { \mathbf { U } }$ </td><td>Content placement vector of UAV.</td></tr><tr><td> $\mathbf { a _ { i } ^ { c p } }$ </td><td> $N _ { C P , i } \mathbf { a _ { i } ^ { c p } } = \left\lceil a _ { i , 1 } ^ { c p } , a _ { i , 2 } ^ { c p } , \dots , a _ { i , F } ^ { c p } \right\rceil$  Caching status of</td></tr><tr><td> $\mathcal { A } _ { N _ { C P } } ^ { f }$ </td><td>Set of CPs who have cached the coded fragments of</td></tr><tr><td> $w _ { i , j }$ </td><td> $f .$  Cooperation willingness between  $N _ { C P , i }$  and  $N _ { C R , j }$ </td></tr><tr><td> $S _ { i }$ </td><td>Set of CRs that can be served by  $N _ { C P , i } .$ </td></tr><tr><td></td><td></td></tr></table>

The line-of-sight channels of the UAV communication links are much more predominant than other channel impairments, such as small scale fading or shadowing. Therefore, the UAV cache files without coding and deliver them to ground CRs directly, as illustrated in Fig. 1. But on the ground, the CP communication links are seriously blocked due to the complex on-site situation, the file is thus encoded into file fragments, which are cached at different CPs in a distributed manner to avoid content loss caused by transmission failure of fragile nodes. Without loss of generality, we focus on local areas in the first scenario in this paper, so that a single UAV can provide the services. As illustrated above, the ground users are divided into CPs and CRs. Let $\mathcal { N } _ { \mathrm { C P } } = \{ N _ { C P , 1 } , \ldots , N _ { C P , i } , \ldots , N _ { C P , N } \}$ denote the set of =CPs in the scenario, where $N _ { C P , i }$ refers to the i-th CP and N is the number of CPs. $\mathcal { N } _ { \mathrm { C R } } = \{ N _ { C R , 1 } , \ldots , N _ { C R , j } , \ldots , N _ { C R , M } \}$ =denotes the set of mobile CRs, where $N _ { C R , j }$ refers to the j-th CR and M is the number of CRs. The content library is denoted by $\mathcal { F } = \{ f _ { 1 } , f _ { 2 } , \ldots , f _ { F } \}$ with $| { \mathcal { F } } | { = } F$ . CPs can share the cached = =coded fragments with CRs through D2D communications. As the signal strength decreases with distance, the maximum D2D communication distance is denoted by $d _ { \mathrm { m a x } }$ . Only when the distance between the CP and the CR is smaller than $d _ { \mathrm { m a x } }$ , the CR has the opportunity to be served by the CP.

Erasure coding can offer redundancy by encoding complete files into small pieces and storing these coded fragments in several CPs. Notice that different coding schemes lead to different redundancy-reliability tradeoffs. With the same coding parameters, the MDS code performs the best in terms of the redundancy-reliability-complexity tradeoff [22], the minimum storage regenerating (MSR) code consumes the minimum storage [23], and the minimum bandwidth regenerating (MBR) code requires the lowest repair bandwidth [24]. In this paper, each file is encoded by a n, k MDS code. Specifically, each file ( )is encoded into n fragments and cached at different CPs in a distributed manner. We consider each CP can only store one of the n fragments for a given file to ensure the maximum fault tolerance. Considering the straggling effect, the CPs may fail, but as long as no less than k nodes are valid, there is an opportunity to recover the source file, as illustrated in the upper right of Fig. 1. The size of the coded fragment is considered to be the same and denoted by $Z _ { f } , \forall f \in F$ . Each CP owns $C _ { S }$ caching units and each caching unit can store one coded fragment. The UAV can cache no more than $C _ { U }$ files without coding.

Consider that the CRs are highly dynamic with spatiotemporal variance for user densities and content request distributions. According to the analysis on many real datasets [25], the file requests can be modeled as the Zipf distribution. However, users in emergency scenarios usually have different preferences (video, image or audio data), which causes the content request distributions to vary spatially and temporally. According to [26], the probability that file f is requested by $N _ { C R , j }$ at time slot t can be calculated as:

$$
r e q _ { j , f } ( t ) = p _ { f } \frac { g \left( \phi _ { j , t } , \vartheta _ { f } \right) } { \sum _ { j ^ { \prime } \in \mathcal { N } _ { \mathrm { C R } } } g \left( \phi _ { j ^ { \prime } , t } , \vartheta _ { f } \right) } ,\tag{1}
$$

where $\begin{array} { r } { p _ { f } = \frac { 1 / f ^ { \xi } } { \sum _ { m \in \mathcal { F } } 1 / m ^ { \xi } } } \end{array}$ is the popularity of file $f ,$ and $g ( \phi _ { j , t } , \vartheta _ { f } )$ is a kernel function with features $\phi _ { j , i }$ t and $\vartheta _ { f }$ , which ( )is used to control the correlation between $N _ { C R , j }$ and file $f .$ Various kernel functions can be applied, e.g., Gaussian, logarithmic and power kernels. To control the average similarity among the user preferences by introducing a parameter Î¶ in the kernel function, we choose power kernel with expression $g ( \phi _ { j , t } , \vartheta _ { f } ) = ( 1 - | \phi _ { j , t } - \vartheta _ { f } | ) ^ { \frac { 1 } { \zeta ^ { 3 } } - 1 } \in [ 0 , 1 ]$ , where $\zeta \in ( 0 , 1 ]$

( ) = (1 ) [0 1] (0 1]In this paper, the altitude of the UAV H is obtained by calculating the partial derivative of the maximum allowable path loss in (8), which is the altitude with the maximum coverage radius $R _ { \mathrm { m a x } } .$ . Then, we divide the horizon area into small square grids with a side length of w. When the UAV hovers at the central point above a grid square, its coverage area can approximately equal to the square area. Thus, we set the side length of each square as $w = \sqrt { 2 } R _ { \mathrm { m a x } }$ according to the Pythagorean Theorem. = 2Each grid square is represented by its central point and denoted by $( x , y ) , x \in [ 1 , X _ { \mathrm { r o w } } ] , y \in [ 1 , Y _ { c o l } ]$ , which means that the grid ( ) [1 ] [1 ]locates in the x-th row and y-th column. $X _ { \mathrm { r o w } }$ and $Y _ { \mathrm { c o l } }$ are the numbers of rows and columns in the target area. The UAV endurance is divided into T time slots, each with a time length of . $\mathbf { Q } = [ \mathbf { q _ { 1 } } , \dots , \mathbf { q _ { t } } , \dots , \mathbf { q _ { T } } ]$ denotes the flying trajectory, where $\mathbf { q _ { t } } = ( x , y )$ is the discrete time location at time slot t. = ( )Then the UAV trajectory constraints are given by

$$
\mathbf { q _ { 1 } } = \mathbf { q _ { T } } ,\tag{2}
$$

$$
\frac { \| \mathbf { q } _ { t + 1 } - \mathbf { q } _ { t } \| } { \Delta } \leq v _ { \operatorname* { m a x } } , \forall t \in [ 1 , T ] ,\tag{3}
$$

where (2) indicates that the UAV should go back to its initial position at the end of the endurance for battery charging. (3) denotes that the flying speed of the UAV cannot exceed its maximum speed $v _ { \mathrm { m a x } }$

## B. Communication Model

In this part, we introduce the models for ground-to-ground (G2G) and UAV-to-ground (U2G) communications.

1) G2G Communications: As shown in Fig. 1, CPs can share the cached coded fragments with CRs through D2D communications. Let $\mathbf { P _ { G } ( t ) } = [ P _ { 1 } ( t ) , P _ { 2 } ( t ) , \ldots , P _ { N } ( t ) ]$ be the transmit ( ) = [ ( ) (power of CPs at time slot t, where $P _ { i } ( t )$ ( )]is the transmit power of $N _ { C P , i }$ ( )at time slot t. Generally, channel state information (CSI) is required to assess the quality of physical links. However, it is impractical to acquire instantaneous CSI of all links due to the mobility. Therefore, in this paper, we consider that only statistical CSI of all involved channel links is available, and the frequency-division multiple access (FDMA) is adopted, i.e., the available system bandwidth is divided into many nonoverlapping frequency bands, where each communication channel is assigned to a ground CR. Thus, the CPs communicating with the same CR share the same channel and accordingly they experience intra-channel interference, while avoiding the inter-channel interference stemming from CPs communicate with other CRs. The achievable data rate of the link between $N _ { C P , i }$ and $N _ { C R , j }$ at time slot t is

$$
R _ { i , j } ( t ) = B \log _ { 2 } \left( 1 + \frac { P _ { i } ( t ) h _ { i , j } } { I _ { i , j } + N _ { 0 } } \right) ,\tag{4}
$$

where B denotes the bandwidth, $h _ { i , j }$ denotes the channel power gain between $N _ { C P , i }$ and $N _ { C R , j }$ , which is exponentially distributed with mean value $\gamma _ { i , j } , \ I _ { i , j }$ denotes the interference received by $N _ { C R , j }$ when communicating with $N _ { C P , i }$ , which is exponentially distributed with mean value $\lambda _ { i , j }$ , and $N _ { 0 }$ is the power of additive white Gaussian noise.

In this paper, we consider that a D2D pair of the CP and the CR may be configured only if a coded fragment can be successfully delivered. Traditional scenarios consider static D2D links between CPs and CRs. However, such an assumption is unreasonable in emergency scenarios. Consequently, a mobility-impacted user interaction is considered when evaluating the success probability of content transmission, i.e., the success probability of receiving enough coded fragments. We characterize the user interaction using the contact duration, i.e., each D2D pair can stay in contact and actively transmit coded fragments for, at most, a given time duration. The contact duration between $N _ { C P , i }$ and $N _ { C R , j }$ is denoted by $T _ { i , j }$

The D2D links should guarantee the transmission of a coded fragment with a success probability above $P _ { \operatorname* { m i n } } ^ { s d }$ , which is the minimum threshold of the delivery success probability. We term such a probability as the delivery success probability, which is denoted by $P r ^ { s d }$ . The delivery success probability at which $N _ { C R , j }$ can successfully receive a coded fragment of f from $N _ { C P , i }$ at time slot t is expressed as

$$
P r _ { i , j , f } ^ { s d } ( t ) = P r \left\{ T _ { i , j } \ge \frac { Z _ { f } } { R _ { i , j } ( t ) } \right\} = P r \left\{ R _ { i , j } ( t ) \ge \frac { Z _ { f } } { T _ { i , j } } \right\} ,\tag{5}
$$

and the specific derivation of $P r _ { i , j , f } ^ { s d } ( t )$ will be discussed in Section III.

2) U2G Communications: Since the data volume of service requests is relatively small compared to the data volume of download files [27], we only consider the downlink transmission in the following. The path loss of line-of-sight (LoS) and non-line-of-sight (NLoS) links are modeled according to the log-normal shadowing model by choosing specific channel parameters, which is given by $\begin{array} { r } { \mathrm { P L } _ { \mathrm { L o s } } = 2 0 \log ( \frac { 4 \pi f _ { c } d } { c } ) + \eta _ { L o S } } \end{array}$ and $\begin{array} { r } { \mathrm { P L } _ { \mathrm { N L o s } } = 2 0 \log ( \frac { 4 \pi f _ { c } d } { c } ) + \eta _ { N L o S } } \end{array}$ with d being the distance PL = 20 log( )from the UAV to the receiving $\mathrm { C R } , f _ { c }$ being the carrier frequency and c being the speed of light. $\eta _ { L o S }$ and $\eta _ { N L o S }$ are shadowing and diffraction losses about LoS and ${ \mathrm { N L o S } } .$ , respectively.

The probability of the LoS connection is an important factor in modeling channels, which depends on the location of the UAV, the environment, and the density of users. It can be expressed as

$$
P r ( \mathrm { L o S } ) = \frac { 1 } { 1 + a \exp \left( - b \left( \frac { 1 8 0 } { \pi } \tan ^ { - 1 } \left( \frac { h } { r } \right) - a \right) \right) } ,\tag{6}
$$

where a and b denote constants relying on different environments including urban, suburban, dense urban, and highrise urban [28]. r denotes the horizontal distance between UAV and ground users, and h denotes the flying height of the UAV. In summary, the total path loss is expressed as

$$
\mathrm { P L } _ { \mathrm { t o t a l } } = P r \mathrm { ( L o S ) } \times \mathrm { P L } _ { \mathrm { L o s } } + P r \mathrm { ( N L o S ) } \times \mathrm { P L } _ { \mathrm { N L o s } } ,\tag{7}
$$

where the probability of NLoS is $P r ( \mathrm { N L o S } ) = 1 - P r ( \mathrm { L o S } )$

(NLoS) = 1 (LoS)The UAV coverage radius, denoted by R, can be constrained by the total path loss. We define the maximum allowable path loss as:

$$
\begin{array} { r l } { \mathrm { P L } _ { \mathrm { m a x } } = \displaystyle \frac { \eta _ { \mathrm { L o s } } - \eta _ { \mathrm { N I o S } } } { 1 + a \exp \left( - b \left[ \arctan \left( \frac { H } { R } \right) - a \right] \right) } } & { } \\ { \displaystyle + 1 0 \log \left( H ^ { 2 } + R ^ { 2 } \right) + 2 0 \log \left( \frac { 4 \pi f } { c } \right) + \eta _ { N \mathrm { L o S } } . } \end{array}\tag{8}
$$

The above equation is implicit, where neither R nor H can be written as an explicit function of each other. In order to obtain the optimum altitude H that yields the best coverage, we need to search for the value of R that satisfies the equation of the critical point: $\partial \mathrm { R } / \partial \mathrm { H } { = } 0 [ 2 8 ]$ . Then we have the UAV maximum coverage radius $R _ { \mathrm { m a x } }$

We consider that the spectrum of UAV is orthogonal to the ground users, and thus, the ground interference is ignored. The UAV communicates with ground CRs in the maximum allowable transmit power $P _ { U }$ . The data rate between the UAV and $N _ { C R , j }$ in time slot t can be expressed as

$$
R _ { u , j } ( t ) = W \log _ { 2 } \left( 1 + \frac { P _ { U } \mathrm { P L } _ { u , j } ( t ) } { N _ { 0 } } \right) ,\tag{9}
$$

where W denotes the bandwidth allocated to the UAV, and $\mathrm { P L } _ { u , j } ( t )$ is the path loss defined in (7) between the UAV and $N _ { C R , j } .$

## C. UAV Energy Consumption Model

The energy consumption of the cache-enabled UAV mainly includes two parts: the propulsion energy required to support its movement and the communication energy for content delivery. However, in actual reality, the propulsion energy of the UAV is much more than communication energy [29]. Therefore, we only consider the propulsion energy in this work.

According to [30] and [31], for a rotary-wing UAV with speed V , the propulsion power consumption and the propulsion energy consumption during one time slot can be respectively expressed as:

$$
\begin{array} { l } { { P ( V ) = P _ { 0 } \left( 1 + \displaystyle \frac { 3  V ^ { 3 } } { V _ { 0 } ^ { 2 } } \right) + P _ { 1 } \left( \left( 1 + \displaystyle \frac { V ^ { 4 } } { 4 V _ { 1 } ^ { 4 } } \right) ^ { \frac { 1 } { 2 } } - \displaystyle \frac { V ^ { 2 } } { 2 V _ { 1 } ^ { 2 } } \right) ^ { \frac { 1 } { 2 } } } } \\ { { { } } } \\ { { + \displaystyle \frac { 1 } { 2 } P _ { 2 } V ^ { 3 } , } } \\ { { E _ { p } ( x ) = \displaystyle \frac { x } { V } P ( V ) + \operatorname* { m a x } \left\{ \Delta - \displaystyle \frac { x } { V } , 0 \right\} \cdot \left( P _ { 0 } + P _ { 1 } \right) , ~ ( 1 0 \leq N ) ~ } } \end{array}\tag{}
$$

where $x \in \{ 0 , w , \sqrt { 2 } w \}$ is the flying distance within one time slot, $P _ { 0 } , P _ { 1 } , P _ { 2 } , V _ { 0 }$ , and $V _ { 1 }$ are constant parameters related to the UAV weight, rotor disc area, air density, fuselage drag ratio and rotor solidity.

## D. Problem Formulation

We define the content placement vector of CPs as ${ \bf A } _ { N \times F } ^ { c p } =$ $[ \mathbf { a _ { 1 } ^ { c p } } , \mathbf { a _ { 2 } ^ { c p } } , \dots , \mathbf { a _ { N } ^ { c p } } ]$ , where $\mathbf { a } _ { \mathbf { i } } ^ { \mathbf { c p } } = [ a _ { i , 1 } ^ { c p } , a _ { i , 2 } ^ { c p } , \ldots , a _ { i , F } ^ { c p } ]$ represents the caching status of $N _ { C P , i \cdot } a _ { i , f } ^ { c p } = 1$ if one of the coded fragments of file $f$ is cached in $N _ { C P , i } ;$ otherwise, $a _ { i , f } ^ { c p } \ =$ =0. The content placement vector of the UAV is denoted by $\mathbf { A } ^ { \mathbf { U } } = [ a _ { 1 } ^ { U } , a _ { 2 } ^ { U } , \cdot \cdot \cdot , a _ { F } ^ { U } ]$ , where $a _ { f } ^ { U } = 1$ if file $f$ is cached in the $\mathrm { U A V } ; a _ { f } ^ { U } = 0 .$ , otherwise.

=We consider the $\mathrm { C R s } ^ { \prime }$ requests are first responded by the ground CPs. If the CR can obtain enough fragments from the ground CPs and recover the requested file, it is not necessary to request the same file from the UAV. If the CR cannot recover the requested file from the ground CPs, it sends a request to the UAV. Thus, CRs can retrieve the required files from ground CPs or the UAV. Consequently, we define the content hit ratio of CPs and the UAV as $\hat { P r } _ { C P } ^ { H i t } ( t )$ and $P r _ { U A V } ^ { H i t } ( t )$ , and the overall content hit ( )ratio at time slot t is given by

$$
P r ^ { H i t } ( t ) = 1 - \left( 1 - P r _ { C P } ^ { H i t } ( t ) \right) \cdot \left( 1 - P r _ { U A V } ^ { H i t } ( t ) \right) .\tag{11}
$$

To maximize the overall content hit ratio, the content placement, transmit power of CPs and the content placement, trajectory of the UAV should be jointly optimized. Therefore, the

problem can be formulated as

$$
\mathcal { P } _ { 1 } : \operatorname* { m a x } _ { A ^ { c p } , P _ { G } ( t ) , A ^ { U } , X } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } P r ^ { H i t } ( t )\tag{12a}
$$

$$
\begin{array} { r } { \mathrm { s . t . } \ \sum _ { f \in \mathcal { F } } a _ { i , f } ^ { C P } \leq C _ { S } , \forall i , } \end{array}\tag{12b}
$$

$$
\begin{array} { r } { \sum _ { f \in \mathcal { F } } a _ { f } ^ { U } \le C _ { U } , } \end{array}\tag{12c}
$$

$$
\sum _ { t = 1 } ^ { T } P _ { i } ( t ) \leq P _ { \operatorname* { m a x } } , \forall i ,\tag{12d}
$$

$$
\sum _ { t = 1 } ^ { T } E _ { P } \left( \left\| \mathbf { q _ { t } } - \mathbf { q _ { t - 1 } } \right\| \right) \leq E _ { u , \operatorname* { m a x } } ,\tag{12e}
$$

$$
\frac { \| \mathbf { q _ { t + 1 } } - \mathbf { q _ { t } } \| } { \Delta } \leq v _ { \operatorname* { m a x } } ,\tag{12f}
$$

where (12b) and (12c) restrict the maximum number of coded fragments cached in CPs and the maximum number of files cached in the UAV, respectively. (12d) denotes that the overall transmit power of each CP should be less than the threshold. (12e) and (12f) regulate the maximum allowable UAV energy consumption and velocity, respectively. Targeting the general objective function formulated above, in the next section, we will perform a detailed analysis of the expression for the delivery success probability and the content hit ratio.

## III. ANALYTICAL RESULTS FOR THE CONTENT HIT RATIO

In this section, we first derive the delivery success probability between CPs and CRs $P r _ { i , j , f } ^ { s d } ( t )$ , and then provide the closedform expression of the content hit ratio of CPs $P r _ { C P } ^ { H i t } ( t )$ and the overall content hit ratio $\mathit { P r } ^ { H i t } ( t )$

## A. Delivery Success Probability

The expression of the delivery success probability is given in Section II-B. In (5), the Cumulative Distribution Function (CDF) of $R _ { i , j } ( t )$ can be expressed by

$$
\begin{array} { r l } & { F _ { R _ { i , j } ( t ) } ( r ) = \operatorname* { P r } \left\{ R _ { i , j } ( t ) \le r \right\} } \\ & { \quad \quad \quad = \operatorname* { P r } \left\{ B \log _ { 2 } \left( 1 + \frac { P _ { i } ( t ) \mathrm { h } _ { i , j } } { I _ { i , j } + \mathrm { N } _ { 0 } } \right) \le r \right\} } \\ & { \quad \quad \quad = \operatorname* { P r } \left\{ \frac { \frac { P _ { i } ( t ) \gamma _ { i , j } } { \frac { N _ { 0 } } { \gamma _ { i , j } } } \cdot \frac { \mathrm { h } _ { i , j } } { \gamma _ { i , j } } } { \frac { \lambda _ { i , j } } { \mathrm { N } _ { 0 } } \cdot \frac { I _ { i , j } } { \lambda _ { i , j } } + 1 } \le 2 ^ { \frac { r } { B } } - 1 \right\} . } \end{array}\tag{13}
$$

Denote $\begin{array} { r } { \mathrm { Y } \triangleq \frac { c _ { 1 } \cdot \frac { \mathrm { h } _ { i , j } } { \gamma _ { i , j } } } { c _ { 2 } \cdot \frac { I _ { i , j } } { \lambda _ { i } \mathrm { ~ } _ { i } } + 1 } } \end{array}$ , where $\begin{array} { r } { c _ { 1 } = \frac { P _ { i } ( t ) \gamma _ { i , j } } { \mathrm { N } _ { 0 } } , ~ c _ { 2 } = \frac { \lambda _ { i , j } } { \mathrm { N } _ { 0 } } } \end{array}$ , its CDF is evaluated with Lemma 1.

Lemma 1: Let 1 and $\Phi _ { 2 }$ follow independent exponential Î¦ Î¦distributions with mean value 1. Then, the CDF of $\begin{array} { r } { \Psi = \frac { q _ { 1 } \Phi _ { 1 } } { ( q _ { 2 } \Phi _ { 2 } + 1 ) } } \end{array}$ with $q _ { 1 } , q _ { 2 } \geq 0$ is given by

$$
F _ { \Psi } ( \psi ) = 1 - \frac { q _ { 1 } } { q _ { 1 } + q _ { 2 } \psi } \exp \left( - \frac { \psi } { q _ { 1 } } \right) .\tag{14}
$$

Proof: The proof is presented in Appendix A, available online.

According to Lemma 1, the CDF of $R _ { i , j } ( t )$ can be rewritten as

$$
F _ { R _ { i , j } ( t ) } ( r ) = F _ { \mathrm { Y } } ( 2 ^ { \frac { r } { B } } - 1 )
$$

$$
= 1 - \frac { c _ { 1 } } { c _ { 1 } + c _ { 2 } \cdot \left( 2 ^ { \frac { r } { B } } - 1 \right) } \exp \left( - \left( \frac { 2 ^ { \frac { r } { B } } - 1 } { c _ { 1 } } \right) \right)\tag{15}
$$

To analyze the delivery success probability, we can rewrite it from (5) as

$$
P r _ { i , j , f } ^ { s d } ( t ) = \frac { c _ { 1 } } { c _ { 1 } + c _ { 2 } \cdot \left( 2 ^ { \frac { Z _ { f } } { B \cdot T _ { i , j } } } - 1 \right) }
$$

$$
\times \exp \left( - \left( \frac { 2 ^ { \frac { Z _ { f } } { B \cdot T _ { i , j } } } - 1 } { c _ { 1 } } \right) \right) .\tag{16}
$$

The delivery success probability, $P r _ { i , j , f } ^ { s d } ,$ , depends on the contact duration, $T _ { i , j }$ , and there are two types of $T _ { i , j }$ . In emergency scenarios, there are two types of CRs with known and unknown moving directions, respectively. The motivation of this setting is that, in emergency scenarios, rescue and medical teams, or fire fighters, rush towards a target scene with known moving direction while the population may be moving along random ways [32]. CPs in our scenario are considered to be static, such as emergency command vehicles, to provide stable communication services for CRs. Considering the two types of CRs, the contact duration $T _ { i , j }$ can be analyzed in two categories.

1) CRs With Known Moving Direction: When the moving direction of CRs is known, the contact duration is a constant that can be calculated through the geographical relationship between the CP and the CR, as illustrated in Fig. 1. Let $d _ { i j }$ be the initial distance between $N _ { C P , i }$ and $N _ { C R , j }$ . Only when $d _ { i j } \leq d _ { \operatorname* { m a x } } ,$ $N _ { C R , j }$ has the opportunity to be served by the $N _ { C P , i }$ . According to the sine theorem, $\begin{array} { r } { \beta = \arcsin ( \frac { d _ { i j } \sin \alpha } { d _ { \mathrm { m a x } } } ) } \end{array}$ , where Î± is known in the triangle. Then, we have $\begin{array} { r } { d _ { j j } = \frac { d _ { i j } \cdot \sin \theta } { \sin \beta } } \end{array}$ , where $\theta = \pi - \alpha -$ $\beta ,$ and the contact duration $\begin{array} { r } { T _ { i , j } = \frac { d _ { j j } } { v } } \end{array}$ , where v is the velocity =of the CR. Thus, when the moving direction of CRs is known, we can rewrite the delivery success probability as

$$
\begin{array} { r l } & { P r _ { i _ { \partial , j } ^ { k } } ^ { \alpha _ { i _ { 1 , j } } ^ { k + 1 } } ( t ) = \frac { c _ { 1 } } { c _ { 1 } + c _ { 2 } \cdot \left( 2 ^ { 2 \frac { \pi ^ { \alpha _ { i _ { 1 , j } } } } { c _ { 1 } } } - 1 \right) } } \\ & { \qquad \times \exp \left( - \left( \frac { 2 ^ { \frac { \pi ^ { \alpha _ { i _ { 1 , j } } } } { c _ { 1 } } } - 1 } { c _ { 1 } } \right) \right) } \\ & { = \frac { c _ { 1 } } { c _ { 1 } + c _ { 2 } \cdot \left( 2 ^ { \frac { \pi ^ { \alpha _ { i _ { 1 , j } } } } { c _ { 1 } } + \alpha _ { 1 } \alpha _ { 1 } \alpha _ { 1 } } - 1 \right) } } \\ & { \qquad \times \exp \left( - \left( \frac { 2 ^ { \frac { \pi ^ { \alpha _ { i _ { 1 , j } } } } { c _ { 1 } } \sin \alpha _ { 1 } \alpha _ { 1 } } - 1 } { c _ { 1 } } \right) \right) } \end{array}\tag{17}
$$

2) CRs With Unknown Moving Direction: When the moving direction of CRs is unknown, the contact duration is random, and we consider that CRs arrive and depart according to the Poisson process [33]. Then the contact duration, $T _ { i , j }$ , is exponentially distributed with mean value $t _ { i , j }$ . Using the conditional probability, we rewrite the delivery success probability as

$$
\begin{array} { r l } { P r _ { i , j , f } ^ { s d _ { 2 } } ( t ) = P r \left\{ R _ { i , j } ( t ) \geq \frac { Z _ { f } } { T _ { i , j } } \right\} } & { } \\ { = \displaystyle \int _ { 0 } ^ { + \infty } \left[ 1 - F _ { R _ { i , j } ( t ) } \left( \frac { Z _ { f } } { t } \right) \right] \frac { 1 } { t _ { i , j } } e ^ { - \frac { t } { t _ { i , j } } } d t , } & { } \\ { = \displaystyle \int _ { 0 } ^ { + \infty } \frac { c _ { 1 } } { t _ { i , j } \cdot \left( c _ { 1 } + c _ { 2 } \cdot \left( \frac { z _ { f } ^ { s } } { 2 ^ { \frac { s } { \beta \varepsilon } } - 1 } \right) \right) } \qquad } & { } \\ { \times \exp \left( - \left( \frac { 2 \frac { \varepsilon _ { f } ^ { s } } { \beta \varepsilon _ { 1 } } - 1 } { c _ { 1 } } + \frac { t } { t _ { i , j } } \right) \right) d t . } & { } \end{array}\tag{18}
$$

## B. Content Hit Ratio

The above derivation of delivery success probability is about a single coded fragment between CPs and CRs. However, to retrieve the required file f from CPs, CRs need to successfully receive no less than $k _ { f }$ coded fragments. Thus, in the following, we further derive the content hit ratio of CPs and the UAV.

1) Content Hit Ratio of CPs: Let $I _ { j , f } ^ { c p }$ denote the indices indicating whether $N _ { C R , j }$ can successfully find sufficient CPs to download coded fragments of file $f .$ . We have

$$
I _ { j , f } ^ { C P } = \varepsilon \left( \left\lfloor \frac { \sum _ { i \in N _ { C P } } a _ { i , f } ^ { c p } \cdot w _ { i , j } } { k _ { f } } \right\rfloor \right) , \varepsilon ( t ) = \left\{ \begin{array} { l l } { 1 , } & { t > 0 , } \\ { 0 , } & { t \leq 0 , } \end{array} \right.\tag{19}
$$

where 
x denotes the largest integer no larger than x. In emergency scenarios, there are social relationships between emergency command vehicles and rescuers, i.e., CPs and CRs in our settings. Whether $N _ { C P , i }$ is willing to share coded fragments with $N _ { C R , j }$ is restricted by the cooperation willingness, which is defined as $w _ { i , j } . \mathrm { ~ I f ~ } w _ { i , j } = 1 , N _ { C P , i }$ is willing to transmit the cached coded fragments to $N _ { C R , j }$ ; otherwise, $w _ { i , j } = 0 .$

Let ${ \mathcal { A } _ { N _ { C P } , j } ^ { f } } = \{ i \mid a _ { i , f } ^ { c p } \cdot w _ { i , j } = 1 , \forall i \in N _ { C P } \}$ denote the set = = 1of CPs that have cached the coded fragments of file f and are willing to share with $N _ { C R , j }$ , with cardinality $| \mathcal { A } _ { N _ { C P } , j } ^ { f } | { = } \mathrm { N } _ { f , j }$ According to $( n , k )$ MDS code, $N _ { C R , j }$ =Ncan successfully retrieve the required file $f$ from nearby CPs if it obtains no less than $k _ { f }$ and no more than $n _ { f }$ coded fragments of the file $f ,$ and thus there are $C _ { \mathrm { N } _ { f , j } } ^ { k _ { f } } + \bar { C } _ { \mathrm { N } _ { f , j } } ^ { k _ { f } + 1 } + \cdot \cdot \cdot , + C _ { \mathrm { N } _ { f , j } } ^ { n _ { f } }$ possible permutations and combinations to obtain the required coded fragments. Let $\mathcal { U } _ { j } ^ { f } = \{ A _ { u , j } ^ { f } | k _ { f } \leq | A _ { u , j } ^ { f } | \leq n _ { f } , \dot { \mathcal { A } _ { u , j } ^ { f } } \subseteq$ $\mathcal { A } _ { N _ { C P } , j } ^ { f } , u = 1 , 2 , \dotsc , | \mathcal { U } _ { j } ^ { f } | \}$ denote these possible combinations of CPs in $A _ { N _ { C P } , j } ^ { f } ,$ , with cardinality $| \mathcal { U } _ { j } ^ { f } | = C _ { \mathrm { N } _ { f , j } } ^ { k _ { f } } +$ $C _ { \mathrm { N } _ { f , j } } ^ { k _ { f } + 1 } + \cdot \cdot \cdot , + C _ { \mathrm { N } _ { f , j } } ^ { n _ { f } } { = } \mathrm { U }$ . Hence, the probability that $N _ { C R , j }$ + + =Usuccessfully retrieves file f from CPs at time slot t can be given as

$$
\begin{array} { r l } & { P r _ { C P , \beta , f } ^ { H G } ( t ) = \frac { I _ { \hat { \mathcal { S } } , f } ^ { G P } \cdot \sum _ { u = 1 } ^ { \mathrm { U } } \prod _ { i \in \mathcal { U } _ { i , j } ^ { d } } ( n ) P r _ { i \cdot , j } ^ { s d } ( t ) } { \mathbb { U } } , } \\ & { = \frac { I _ { \hat { \mathcal { S } } , f } ^ { G P } } { \mathbb { U } } \cdot \left[ C _ { \mathrm { M } _ { i , f } , \frac { 1 } { \mathrm { R e } } , f } ^ { k _ { f } ^ { 3 d } } ( t ) \cdot P r _ { 2 , j , f } ^ { s \delta , d } ( t ) \cdot \dots , \cdot P r _ { k , f , f } ^ { s k _ { f , f } ^ { d } } ( t ) \right] } \\ & { \qquad \quad \times \mathrm { ~  { [ u s p a b a b i u g ~  { H a n } } ~ } N e x _ { i , j } \mathrm { ~ s u c s s i a l y ~ r e s i e s ~ i f i c ~ f r o m ~ } A _ { i , j } ^ { t } , } \\ & { + C _ { \mathrm { N } _ { f , j } ^ { d } } ^ { k _ { f } ^ { d } } \cdot P r _ { 1 , j , f } ^ { s d } ( t ) \cdot P r _ { 2 , j , f } ^ { s d } ( t ) \cdot \dots , \cdot P r _ { k , f + 1 , j , f } ^ { s d } ( t ) + \dots , } \\ &  + C _ { \mathrm { N } _ { f , j } ^ { d } } ^ { n _ { d } ^ { d } } \cdot \underbrace { P r _ { 1 , j , f } ^ { s d } ( t ) \cdot P r _ { 2 , j , f } ^ { s d } ( t ) } _ { \mathrm { ~  { \mathrm { H e } \mathcal { R } \mathrm { R } \mathrm { R } \mathrm { R e } \mathrm { R e } \mathrm { R e } \mathrm { S u s e s s i o n } \mathrm { V o r } \mathrm { S u p s i o n } \mathrm { V o r } \mathrm { S u p } \mathrm { I m } } \mathrm { ~ , ~ } } } \end{array}\tag{20}
$$

where $P r _ { i , j , f } ^ { s d } ( t )$ is the delivery success probability of a single ( )coded fragment between $N _ { C P , i }$ and $N _ { C R , j }$ at time slot t.

As illustrated in (17) and (18), when the moving direction of $C R _ { j }$ is known, $P r _ { i , j , f } ^ { s d } ( t )$ is denoted by $P r _ { i , j , f } ^ { s \breve { d } _ { 1 } } ( t )$ , and $P r _ { C P , j , f } ^ { H i t } ( t )$ is denoted by $\dot { P r } _ { C P , j , f } ^ { H i t _ { 1 } } ( t ) ;$ ; otherwise, $P r _ { i , j , f } ^ { s d } ( t ) =$ $P r _ { i . i . f } ^ { s d _ { 2 } } ( t )$ , and $P r _ { C P , j , f } ^ { H i t } ( t ) = P r _ { C P , j , f } ^ { H i t _ { 2 } } ( t )$ J

( ) ( ) = ( )We consider that a CR only requests one file at each time slot and $\rho _ { 1 } \ M$ of CRsâ moving direction is known, and the other CRsâ moving direction is unknown. Therefore, the content hit ratio of CPs at time slot t is given by (21) shown at the bottom of this page, where $M _ { 1 } = \lfloor \rho _ { 1 } M \rfloor , r e q _ { j , f } ( t )$ is illustrated in (1), = ( )which denotes the probability that file f is requested by $N _ { C R , j }$ at time slot t.

2) Content Hit Ratio of UAV: Recall that CRs will request the files from the UAV only if they cannot retrieve the required files from ground CPs. As the LoS channels of the UAV communication links are much more predominant, the UAV can transmit the complete files without coding. When the data rate is greater than the threshold $R _ { \mathrm { m i n } } .$ , CRs can successfully receive the files from the UAV. Therefore, the content hit ratio of UAV at time slot t is given by (22) shown at the bottom of this page, where $a _ { f } ^ { U }$ is the content placement decision of the UAV, which is defined in Section III-B. $\mathbb { I } _ { c o n d i t i o n } = 1$ if the condition is true, and $\mathbb { I } _ { c o n d i t i o n } = 0 .$ , otherwise.

= 0So far, we can obtain the closed-form expression of $\mathit { P r } ^ { H i t } ( t )$ in Section II-D. After the derivation, we find that problem $\mathcal { P } _ { 1 }$

$$
P r _ { C P } ^ { H i t } ( t ) = \frac { \sum _ { j = 1 } ^ { M _ { 1 } } \sum _ { f = 1 } ^ { F } r e q _ { j , f } ( t ) \cdot P r _ { C P ; j , f } ^ { H i t _ { 1 } } ( t ) + \sum _ { j = M _ { 1 } + 1 } ^ { M } \sum _ { f = 1 } ^ { F } r e q _ { j , f } ( t ) \cdot P r _ { C P ; j , f } ^ { H i t _ { 2 } } ( t ) } { \sum _ { j = 1 } ^ { M } \sum _ { f = 1 } ^ { F } r e q _ { j , f } ( t ) } ,\tag{21}
$$

$$
P r _ { U A V } ^ { H i t } ( t ) = \frac { \sum _ { j = 1 } ^ { M } \sum _ { f = 1 } ^ { F } r e q _ { j , f } ( t ) \cdot a _ { f } ^ { U } \cdot \mathbb { I } _ { P r _ { C P , j , f } ^ { H i t } ( t ) = 0 } g _ { \mathcal { E } } R _ { u , j } ( t ) \geq R _ { \operatorname* { m i n } } } { \sum _ { j = 1 } ^ { M } \sum _ { f = 1 } ^ { F } r e q _ { j , f } ( t ) } ,\tag{22}
$$

<!-- image-->  
Fig. 2. The solution framework of the formulated problem.

is a mixed integer nonlinear programming problem that is challenging to be directly solved, and the decision-making entities include both CPs and the UAV. The centralized approaches always need global CSI with large computation complexity that are limited in dynamic multi-entity networks. Therefore, intelligent decentralized approaches are needed to cope with these challenges.

## IV. DESIGN OF MULTIAGENT TWO-TIMESCALE DRL

To address the above challenges, we divide problem $\mathcal { P } _ { 1 }$ into two parts: a) sub-problem of ground CPs $\mathcal { P } _ { 2 }$ and b) sub-problem of the UAV $\mathcal { P } _ { 3 }$ to separately maximize the content hit ratio. As shown in Fig. 2, given the network information, ground CPs use coded caching to ensure transmission reliability, while the UAV uses uncoded caching as the air-ground communication link is dominated by the LoS channel with little interference. In sub-problem $\mathcal { P } _ { 2 }$ , we jointly optimize the power allocation and content placement for CPs by the MA2T-DRL algorithm, which includes two steps: CPs clustering and multiagent QMIX architecture. In CPs clustering, both physical connectivity and social relationship between CPs and CRs are utilized when constructing the weighted graph. In each cluster, we select a CP as the agent that adopts a two-timescale DRL algorithm to obtain the policies of content placement and power allocation for all the CPs in the same cluster. Then, the mixing network takes the agent network outputs as input and mixes them monotonically. In sub-problem $\mathcal { P } _ { 3 }$ , we adopt a vertical decomposition that divides $\mathcal { P } _ { 3 }$ into trajectory-sub-problem $\mathcal { P } _ { 3 1 }$ and caching-sub-problem $\mathcal { P } _ { 3 2 }$ and solve them by greedy algorithm and the PSO algorithm respectively.

## A. Physical and Social Characteristics-Based Content Providers Clustering

In problem $\mathcal { P } _ { 1 }$ , the power and caching decisions of CPs are only constrained by (12b) and (12d), and thus we can extract the sub-problem $\mathcal { P } _ { 2 }$ as follows:

$$
\mathcal { P } _ { 2 } : \operatorname* { m a x } _ { A ^ { c p } , P _ { G } ( t ) } \frac { 1 } { T } { \sum } _ { t = 1 } ^ { T } P r ^ { H i t } ( t )\tag{23a}
$$

$$
\sum _ { f \in \mathcal { F } } a _ { i , f } \le C _ { s } , \forall i ,\tag{23b}
$$

$$
\sum _ { t = 1 } ^ { T } P _ { i } ( t ) \leq P _ { \operatorname* { m a x } } , \forall i .\tag{23c}
$$

Due to the mobility of CRs and complicated time-varying environments, it is very difficult to solve $\mathcal { P } _ { 2 }$ by employing the traditional methods. DRL can be a promising alternative for uncertain or unknown environments [34]. The centralized DRL algorithm can be adopted by regarding all CPs as an agent, which leads to a large-scale action-and-state space with high computational complexity. Therefore, to reduce the DRL complexity, we propose a clustering method that CPs are divided into multiple clusters, and one of the CPs in each cluster is regarded as an independent agent with its actions and states containing all CPsâ in the cluster.

The rationality of CPs clustering is two-fold: i) reduce the DRL complexity, and ii) exploit the team-working characteristics of emergency command vehicles. In coded caching, multiple CPs are required to serve one CR, and thus a reasonable clustering method helps to improve the robustness of coded caching. Considering the content sharing between CPs and CRs not only depends on physical link conditions, but takes social relationships into account simultaneously, as illustrated in Fig. 3, we develop a physical and social characteristics-based clustering method. Since the identities of CRs are different in emergency scenarios, the CPs are more willing to share files with professional forces as they have strong social ties, but they may refuse to share with non-governmental organizations, which can be regarded as social relationships. Compared with the existing clustering schemes based solely on the physical distance, this paper consider social characteristics to further harvest more performance gain in terms of hit ratio.

The content sharing can be accomplished via D2D communications. A stable D2D link must satisfy the following conditions:

â¢ The physical distance between CP and CR is no larger than $d _ { \mathrm { m a x } }$ (the maximum allowable distance for D2D communication), as shown in the top layer (i.e., physical domain) on the left part of Fig. 3.

â¢ The partner of CP and CR should be trusted and tightly connected. Practically, mobile CRs are socially related to CPs as shown in the bottom layer (i.e., social domain) on the left part of Fig. 3. There is a link between CP and CR in the social domain only if CP is willing to transmit the coded fragments to

<!-- image-->  
Fig. 3. The proposed framework of the 2T-DRL algorithm.

CR. Moreover, users with strong social ties are generally more willing to do content sharing. Based on the discussion of G2G communications in Section II-B, $N _ { C P , i }$ and $N _ { C R , j }$ have a strong social tie if the delivery success probability $P _ { i , j } ^ { s d } \ge P _ { \operatorname* { m i n } } ^ { s d }$ . On the contrary, $P _ { i , j } ^ { s d } < P _ { \operatorname* { m i n } } ^ { s d }$ means $N _ { C R , j }$ has a weak social tie with $N _ { C P , i } .$

The more common CRs that can be served by two CPs, the more important to jointly optimize the decisions of these two CPs. Therefore, in this paper, we model CPs as an undirected graph as illustrated in the middle part of Fig. 3. CPs represent the vertices of the graph. The edge weight is denoted as the number of CRs establishing stable D2D links with the adjacent vertices. Let $S _ { i } = \{ j \in \mathcal { N } _ { \mathrm { C R } } : d _ { i , j } \leq d _ { \operatorname* { m a x } } \wedge w _ { i , j } =$ $1 \wedge P _ { i , j } ^ { s d } \geq P _ { \operatorname* { m i n } } ^ { s d } \}$ = : =denote the set of CRs that can be served by $N _ { C P , i } ,$ , which is constrained by both physical and social characteristics. Then the edge weight between $N _ { C P , i }$ and $N _ { C P , i ^ { \prime } }$ is $\mathcal { W } _ { i i ^ { \prime } } { = } \| S _ { i } \cap S _ { i ^ { \prime } } \|$ . The larger edge weight between two CPs, the =more CRs these two CPs may share together. Then the weighted graph is divided into subgraphs according to the minimum cut of the weighted graph. For example, as illustrated in the middle part of Fig. 3, there are two CRs located within the overlapped communication coverage of $N _ { C P , 1 }$ and $N _ { C P , 2 }$ in the physical domain. However, from the perspective of the social domain, one of the two CRs has weak social ties with the two CPs. Therefore, there is an edge between $N _ { C P , 1 }$ and $N _ { C P , 2 }$ with $\mathcal { W } _ { 1 2 } = 1$ , while the edge weight $\mathcal { W } _ { 2 3 }$ and $\mathcal { W } _ { 3 4 }$ both equal 2. = 1Then the weighted graph is divided into two clusters, and one of the CPs in each cluster is regarded as an independent agent and deploys the two-timescale DRL. The action space of each agent contains all the decisions of CPs in the same cluster.

## B. Multiagent Two-Timescale Deep Reinforcement Learning

As the power allocation and content placement strategies have different delay sensitivities [35], we develop a two tier structure deep-Q network (DQN) for each agent as shown in the right part of Fig. 3, which operates in two timescales. Specifically, content placement is determined in a slow timescale while the power allocation is performed in a fast timescale. Without loss of generality, we discretize the operational timeline into two types of time slots, namely, slow timescale slots (i.e., episodes) and fast timescale slots (i.e., timeslots). Each episode consists of $T _ { d }$ time slots that are indexed by $\mathcal { T } = \{ 1 , \dots , i , \dots , T _ { d } \}$ . The top = 1tier is the ST-DQN that updates caching placement strategies at the beginning of each episode, whereas the bottom tier is the FT-DQN that updates power allocation strategies at each time slot.

Specifically, we define the state space, action space, and reward function of the two-timescale DRL as follows.

1) The Fast Timescale DRL: Taking cluster k as an example, we consider that the set of CPs contained in cluster k is $\mathcal { N } _ { \mathrm { C P , k } } = \{ N _ { C P , 1 } , \dots , N _ { C P , N _ { k } } \}$ . The essential elements of the =fast timescale DQN, i.e., state, action, and reward, are defined as follows.

â¢ State: The state at time slot i is expressed as:

$$
\begin{array} { r } { \pmb { s } _ { i } = \left[ \pmb { P } ( i - 1 ) , \pmb { q } ( i ) \right] , } \end{array}\tag{24}
$$

where $P ( i - 1 ) = [ { P _ { N _ { C P , 1 } } ( i - 1 ) } , { P _ { N _ { C P , 2 } } ( i - 1 ) } , . . . , { P _ { N _ { C P , N _ { L } } } }$ ( 1)=[ ( 1) ( 1)i â  is the transmit power vector of all CPs in cluster $\mathcal { N } _ { C P , k }$ ( 1)]in the previous time slot, and $\pmb { q } ( i ) = [ q _ { 1 } ( i ) , . . . , q _ { j } ( i ) , . . . , q _ { M } ( i ) ]$ ( ) = [ ( ) ( )is the content requirement vector of all CRs at time slot i.

â¢ Action: The action at time slot i, which is denoted by ${ { a } _ { i } } ,$ is defined as the transmit power of CPs. Here we consider discretizing the transmit power of the CP into L optional values $\mathcal { P } = \{ P _ { 1 } , \ldots , P _ { L } \}$ . Therefore, the action can be expressed as:

$$
a _ { i } = \left[ P _ { N _ { C P , 1 } } ( i ) , P _ { N _ { C P , 2 } } ( i ) , . . . , P _ { \mathrm { N } _ { C P , N _ { k } } } ( i ) \right] ,\tag{25}
$$

where $P _ { \mathrm { N } _ { C P , k } ( i ) } \in \mathcal { P }$

â¢ Reward: The reward at time slot i is defined as a linear function of the content hit ratio $P r _ { k } ^ { H i t } ( i )$ of the k-th cluster ( )observed at the end of time slot i, which is denoted by $r _ { i } =$ $\eta P r _ { k } ^ { H i t } ( i )$ , where Î· is a constant.

2) The Slow Timescale DRL: The essential elements of the slow timescale DQN for cluster k are defined as follows,

â¢ State: The state at episode t is expressed as:

$$
\begin{array} { r } { \pmb { s } _ { t } = [ \pmb { C } ( t - 1 ) , \pmb { q } ( t ) ] , } \end{array}\tag{26}
$$

where

$$
C ( t - 1 ) = [ C _ { N _ { C P , 1 } } ( t - 1 ) , C _ { N _ { C P , 2 } } ( t -
$$

$( t - 1 ) ]$ is the content placement vector of all CPs in cluster $\mathcal { N } _ { C P , k }$ ]in the previous episode.

â¢ Action: The action at episode t is defined as the caching strategies of CPs in the cluster. Hence, the action can be expressed as:

$$
\pmb { a } _ { t } = \left[ C _ { N _ { C P , 1 } } ( t ) , C _ { N _ { C P , 2 } } ( t ) , . . . , C _ { N _ { C P , N _ { k } } } ( t ) \right] .\tag{27}
$$

â¢ Reward: The reward at episode t is also denoted by $r _ { t } =$ $\eta P r _ { k } ^ { H i t } ( t )$

( )Fig. 3 clarifies the information and control flow within the designed 2T-DQNs. The ST-DQN inputs the neural network with the observed system parameters $\left( { { s _ { t } } , { a _ { t } } , { r _ { t } } , { s _ { t + 1 } } , { a _ { i } } } \right)$ , including the current system state $s _ { t } ,$ (, the action taken $\mathbf { \Gamma } _ { a _ { t } . }$ ), the immediate reward $r _ { t } ,$ the next system state $\mathbf { \delta } _ { s + 1 }$ in slow timescale, and the current action taken $\mathbf { \alpha } _ { a _ { i } }$ in fast timescale. The FT-DQN inputs the neural network with the observed system parameters $\left( { { s _ { i } } , { a _ { i } } , { r _ { i } } , { s _ { i + 1 } } , { a _ { t } } } \right)$ , including the system state, the action, the ( )immediate reward, the next system state in current time slot i of fast timescale, and the action taken $\mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf \Psi \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf \Psi \mathbf { } \mathbf \mathbf { } \mathbf \Psi \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf \mathbf { } \mathbf \mathbf \Psi \Psi \Psi \mathbf { } \mathbf \mathbf \Psi \Psi \mathbf { } \mathbf \mathbf \Psi \mathbf \Psi \Psi \mathbf \Psi \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \mathbf \Psi \mathbf \Psi \mathbf \Psi \mathbf \Psi \mathbf \mathbf \Psi \mathbf \Psi \mathbf \Psi \mathbf \mathbf \Psi \mathbf \mathbf $ in current episode t of slow timescale that contains the time slot i. The weights $\theta _ { s }$ of the ST-DQN and the $\theta _ { f }$ of FT-DQN will be updated during the training process. The updating process of Î¸ may result in instability caused by the correlation of samples. In DQN, experience replay is employed to eliminate the correlation among all the samples. A fundamental assumption in DQN is that training samples are i.i.d. with each other. In each decision episode and time slot, the agent does not directly update Î¸ with the current sample. The current sample is stored in the pool of the ST-DQN and FT-DQN. Instead, the agent randomly selects some historical samples for training.

The parameters of the 2T-DQNs will be updated after certain iterations of training to reduce correlation. By fixing the weights Î¸ for several training iterations, the instability of the training and weight updating processes can be reduced, thereby leading to lower risk of divergence in training. As for the execution order of the 2T-DQNs, the parameters $\theta _ { s }$ of the ST-DQN will be updated at the beginning of each episode in slow timescale. Meanwhile, within the episode, the parameters $\theta _ { f }$ of the FT-DQN will be updated at each time slot in fast timescale. As each episode consists of $T _ { d }$ time slots, one update of parameters $\theta _ { s }$ includes $T _ { d }$ updates of parameters $\theta _ { f }$

3) Multiagent QMIX Framework: As previously discussed, each agent makes the decision on power allocation and content placement based only on $\mathrm { C P s } ^ { \mathrm { \prime } }$ observations in the same cluster, without knowing the observations and decisions of other clusters. In the multiagent reinforcement learning setting, a global action value estimator is necessary to preclude each agent from greedily choosing action solely according to its individual action values $Q _ { n . }$ s and $Q _ { n _ { - } f }$

In QMIX, we leverage a mixing network to extend and aggregate all the outputs from local 2T-DQNs. As shown in Fig. 4, weights $W _ { 1 } , W _ { 2 }$ and biases $b _ { 1 } , b _ { 2 }$ are generated based on the current environment state $S _ { t }$ . Then, the global action value $Q _ { t o t }$ can be expressed as

$$
Q _ { \mathrm { t o t } } = f _ { s } ( Q _ { s } )\tag{28}
$$

where $f _ { s }$ denotes the mixing network that characterizes the mapping function from local action values to the global action value, i.e., the mapping function defined by the mixing network structure in Fig. 4. Moreover, function $^ { 6 6 } f ^ { 5 }$ joins the two layers and introduces nonlinearity to the mixing network such that it can fit a variety of mapping functions. In this article, âRe $\boldsymbol { \mathbf { \ell } } \boldsymbol { \mathbf { u } } ^ { \flat }$ i s used as the nonlinear function in Fig. 4.

In Fig. 4, an absolute activation function is employed to ensure that weights for mixing Q-values are nonnegative, which makes the global action value always monotonically increasing with local action value $Q _ { n _ { - } s }$ of each agent, i.e.,

$$
\frac { \partial Q _ { \mathrm { t o t } } } { \partial Q _ { n _ { - } s } } \geq 0\tag{29}
$$

for $n = 1 , \ldots , N$ . Thus, for consistency, we only need to ensure that a global  performed on $Q _ { t o t }$ yields the same result as argmaxa set of individual operations performed on each $Q _ { n _ { - } s } \colon$

$$
\underset { \mathbf { a } } { \arg \operatorname* { m a x } } Q _ { t o t } ^ { \omega } ( s , \mathbf { a } ) = \left( \begin{array} { c } { \underset { a ^ { 1 } } { \arg \operatorname* { m a x } } Q _ { 1 _ { - } s } ^ { \theta _ { 1 } } \left( s ^ { 1 } , a ^ { 1 } \right) } \\ { \vdots } \\ { \underset { a ^ { N } } { \vdots } } \end{array} \right)\tag{30}
$$

where the global parameters $\pmb { \theta } = \{ \pmb { \theta } _ { 1 } , \dots , \pmb { \theta } _ { N } , \pmb { \omega } \}$ include the =mixing network parameters Ï as well as that of each agentâs local 2T-DQN.

During the training process, the global parameters $\pmb { \theta }$ are updated by minimizing the following loss:

$$
\mathcal { L } ( \theta ) = \sum _ { i = 1 } ^ { b } \left[ \left( y _ { i } ^ { \mathrm { t o t } } - Q _ { \mathrm { t o t } } ( s , \mathbf { a } ; \theta ) \right) ^ { 2 } \right]\tag{31}
$$

where b is the batch size of transitions sampled from the replay buffer, the target action value is defined as $y ^ { t o t } = r +$ Î³ Qtot s , a Î¸â and $\theta ^ { - }$ = +are the parameters of a target a   
network as in DQN. The training algorithm of the MA2T-DRL is described in Algorithm 1.

## C. Caching and Trajectory Design of UAV

After obtaining the power and caching decisions of CPs, the problem $\mathcal { P } _ { 1 }$ can be transformed as problem $\mathcal { P } _ { 3 }$ without taking CPs into consideration:

$$
\mathcal { P } _ { 3 } : \operatorname* { m a x } _ { A ^ { U } , X } \frac { 1 } { T } { \sum * { T } _ { t = 1 } ^ { T } } P r ^ { H i t } ( t )\tag{32a}
$$

$$
\begin{array} { r } { \sum _ { f \in \mathcal { F } } a _ { f } ^ { U } \le C _ { U } , } \end{array}\tag{32b}
$$

$$
\sum _ { t = 1 } ^ { T } E _ { P } \left( \left\| \mathbf { q _ { t } } - \mathbf { q _ { t - 1 } } \right\| \right) \leq E _ { u , \operatorname* { m a x } } ,\tag{32c}
$$

<!-- image-->  
Fig. 4. The overall MA2T-DRL structure.

$$
\frac { \| \mathbf { q _ { t + 1 } } - \mathbf { q _ { t } } \| } { \Delta } \leq v _ { \operatorname* { m a x } } .\tag{32d}
$$

$\mathcal { P } _ { 3 }$ can be divided into a sub-problem of trajectory and a subproblem of UAV caching adopting a vertical decomposition, which has been discussed in [20]. The sub-problem of trajectory can be reformulated as:

$$
\mathcal { P } _ { 3 1 } : \operatorname* { m a x } _ { X } \frac { 1 } { T } { \sum _ { t = 1 } ^ { T } } P r ^ { H i t } ( t )\tag{33a}
$$

$$
\sum _ { t = 1 } ^ { T } E _ { P } \left( \left\| \mathbf { q _ { t } } - \mathbf { q _ { t - 1 } } \right\| \right) \leq E _ { u , \operatorname* { m a x } } ,\tag{33b}
$$

$$
\frac { \| \mathbf { q _ { t + 1 } } - \mathbf { q _ { t } } \| } { \Delta } \leq v _ { \operatorname* { m a x } } .\tag{33c}
$$

The sub-problem of UAV caching can be reformulated as:

$$
\mathcal { P } _ { 3 2 } : \operatorname* { m a x } _ { A ^ { U } } \sum _ { t = 1 } ^ { T } \frac { 1 } { T } P r ^ { H i t } ( t )\tag{34a}
$$

$$
\sum _ { f \in { \mathcal { F } } } a _ { f } ^ { U } \leq C _ { U } .\tag{34b}
$$

Both sub-problems $\mathcal { P } _ { 3 1 }$ and $\mathcal { P } _ { 3 2 }$ have been widely investigated in [20]. In this paper, we use greedy algorithm and the PSO algorithm to solve them respectively. The performance of these algorithms will be elaborated in Section V.

## V. PERFORMANCE EVALUATION

## A. Simulation Settings

In our simulation, CPs are randomly distributed in the range of $1 , 0 0 0 \mathrm { ~ m ~ } \times \mathrm { ~ 1 , 0 0 0 }$ m square area. The region is divided into a square grid of $1 0 \times 1 0$ cells. Thus, the total number of grids is 100 and the size of each grid is $1 0 0 \times 1 0 0 \mathrm { m ^ { 2 } }$ . Such division yields a suitable distribution matrix for the number of CRs in cells. Note that increasing the number of cells also increases the algorithmâs computational complexity. The update interval $\Delta$ and UAV flying height H are set to 5 s and 15 m unless otherwise specified. The number of CPs is 4, and the number of CRs is 100. The distribution of CRs varies significantly over time $\Delta$ and between grids $( 1 0 \times 1 0 )$ . The (3,2) MDS code is Îapplied and each CP has equal storage space.

For DRL model training, we use the Adam optimizer with a learning rate of 0.001 and the hyper-parameters $\gamma = 0 . 9 5$ = 0 95The replay memory size, denoted by |M|, is set to be 2,000, whereas the size of memory is around 30 MB and the batch size is 200. The DQN1 and DQN2 are designed as 3-hidden-layer with 256-128-32 units neural networks. These values for the hyperparameters are chosen empirically after extensive experiments. Other simulation parameters and their values are shown in Table II. All experiments are carried out on a laptop with 8.00 GB RAM and the processor configuration is: Intel(R) Core(TM) i7-7500 U CPU @ 2.70 GHz.

## B. Performance Evaluation of MA2T-DRL

In this subsection, the achievable performance of the proposed MA2T-DRL algorithm is evaluated. The following benchmark schemes are used for performance comparison to evaluate the performance of the MA2T-DRL algorithm. As the benchmark schemes are all two-timescales DRL, we simplify MA2T-DRL to MA-DRL to reflect the difference between different algorithms.

Centralized deep reinforcement learning (C-DRL): We choose one CP as the agent for centralized training, and the agent is able to access all the CPsâ joint observations and make joint decisions for all the CPs. This can be done by concatenating the state and action of each agent and defining reward as the sum of the reward in the multiagent framework.

â¢ Independent deep reinforcement learning (I-DRL): All CPs are divided into different clusters based on the proposed clustering method. We choose one of the CPs in each cluster as an independent agent for distributed training, and the multiagent problem is decomposed into multiple single-agent problems that work in parallel.

â¢ Random cluster scheme (RCS): All CPs are divided into different clusters randomly, and the training process is the same as I-DRL.

Fig. 5 demonstrates a 2,000-episode training process of the MA-DRL, C-DRL (i.e., a single agent DRL approach) and I-DRL (i.e., independent multiagent RL approach). We can see that both MA-DRL and C-DRL approaches are able to level off and efficiently converge to a global optimum, which indicates that, learning with the multiagent algorithm, the CPs are able to cooperatively make the best decisions to achieve the common goal even without sharing their local observations with each other. However, it is noteworthy that during the training process, the cumulative rewards might drop after attaining some higher values for the MA-DRL approach. Such nonstationary convergence is a normal case in multiagent RL model training due to action exploration and inevitable randomness. Compared to MA-DRL and C-DRL approaches, training of I-DRL is less efficient due to the independent training of each agent with the goal of attaining its local optimum rather than the global optimum. However, both the I-DRL and MA-DRL approaches are faster than C-DRL to converge due to the smaller state and action spaces. I-DRL and our proposed MA-DRL converge almost simultaneously in less than 750 episodes, reducing the convergence time of more than 700 episodes compared with the C-DRL. The corresponding execution time that the algorithms converge to the optimum is demonstrated on the upper horizontal axis of Fig. 5.

```powershell
Algorithm 1: Multiagent Two-Timescale DRL.
Input: Number of CRs M; number of CPs $N _ { k }$ in each
cluster $k .$
Output: $\mathrm { C P } ^ { \prime } \mathrm { s }$ transmit power $P _ { i } ( t )$ and caching status $a _ { i , f } ^ { c p }$
Initialize the mixing network with weights $\{ \omega \}$ and replay
memory $\mathcal { R } .$
For each agent, initialize 2T-DQN with weights $\{ \theta _ { s } \} , \{ \theta _ { f } \}$
and the replay memory $D _ { s } , D _ { f }$
for epoch $j { \dot { = } } { \dot { I } } , . . . , J$ do
The slow timescale ST-DQN
Initialize the beginning state $s _ { 0 }$ for ST-DQN and the
global state $\begin{array} { r } { { \cal S } _ { 0 } . } \end{array}$
for episode $t = I , . . . , T$ do
For all agents,take action randomly from $D _ { s }$ with
probabilityÎµor select $a _ { t } = \arg \operatorname* { m a x } _ { \alpha . } Q _ { s } ^ { \theta _ { s } } ( s _ { t } , a _ { t } ; \theta _ { s } ) ,$
Execute action $a _ { t }$ in emulator and observe reward
$r _ { t }$ and new state $s _ { t + 1 }$
Store the experience $\left( { { s _ { t } } , { a _ { t } } , { r _ { t } } , { s _ { t + 1 } } } \right)$ to ${ \mathcal { R } } .$
$\mathbf { i f } \ j \ge N _ { s a m }$ then
Get a random minibatch of $N _ { s a m }$ samples
$\left\{ \left( s _ { t } , a _ { t } , r _ { t } , s _ { t + 1 } \right) \right\}$ from replay memory $\mathcal { R } .$
Update $\omega : \omega  \omega - \alpha _ { \omega } \nabla _ { \omega } \mathcal { L } ( \omega )$
For each agent $n ,$ update
$\theta _ { n - s }  \theta _ { n - s } - \alpha _ { \theta } \nabla _ { \theta _ { n _ { - } s } } \mathcal { L } ( \theta _ { n _ { - } s } )$
end
The fast timescale FT-DQN
Initialize the beginning state $s _ { 0 }$ for FT-DQN.
for time slot $i = I , . . . , T _ { d }$ do
For all agents,take action randomly from $D _ { f }$ with
probability Îµ or select $a _ { i } = \arg \operatorname* { m a x } _ { a _ { i } } Q _ { f } ^ { \theta _ { f } } \left( s _ { i } , a _ { i } ; \theta _ { f } \right)$
Execute action $a _ { i }$ in emulator and observe
reward $r _ { i }$ and new state $s _ { i + 1 }$
Store the experience $( s _ { i } , a _ { i } , r _ { i } , s _ { i + 1 } )$ to $D _ { f }$
Get a random minibatch of $N _ { s a m }$ samples
$\left\{ \left( s _ { i } , a _ { i } , r _ { i } , s _ { i + 1 } \right) \right\}$ from replay memory $D _ { f } .$
Set $y _ { i } = r _ { i } + \gamma \mathrm { { m a x } } Q _ { f } \left( s _ { i + 1 } , a ^ { \prime } ; \theta _ { f } ^ { \prime } \right)$ ,and
$\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } _ { f } ) = \sum _ { i = 1 } ^ { N _ { s a m } } \left\lceil \left( y _ { i } - Q _ { f } \left( s _ { i } , a _ { i } ; \boldsymbol { \theta } _ { f } \right) \right) ^ { 2 } \right\rceil } \end{array}$
For each agent n, update
$\theta _ { n - f }  \theta _ { n - f } - \alpha _ { \theta } \overline { { \nabla } } { \theta _ { n _ { - } f } } \mathcal { L } ( \theta _ { n _ { - } f } )$
end
end
end
return optimal policy $P _ { i } ( t )$ and $a _ { i , f } ^ { c p } .$
```

TABLE II EXPERIMENTAL PARAMETERS
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Bandwidth of CPs and theUAV B</td><td>1 Hz</td></tr><tr><td>Transition power of CPs</td><td>{1 W, 1.5 W}</td></tr><tr><td>Transition power of the UAV Caching storage capacity of CP  $C _ { S }$ </td><td>1W</td></tr><tr><td>Caching storage capacity of UAV  $C _ { U }$ </td><td>2</td></tr><tr><td> $H$ </td><td>5</td></tr><tr><td>UAV flying height Update interval  $\Delta$ </td><td>15 m</td></tr><tr><td> Maximum speed of UAV Vmax</td><td> $5 \mathrm { ~ s ~ }$ </td></tr><tr><td>Maximum allowable path loss of UAV PLmax</td><td>15 m/s -138 dBm</td></tr><tr><td>Coefficient of blade profile power  $P _ { 0 }$ </td><td></td></tr><tr><td>Coefficient of induced power  $P _ { 1 }$ </td><td>79.85 J/s</td></tr><tr><td>Coefficient of parasite power</td><td>88.63 J/s</td></tr><tr><td> $P _ { 2 }$ </td><td>0.018 kg/m</td></tr><tr><td>Tip speed of the rotor blade  $V _ { 0 }$ </td><td>120 m/s</td></tr><tr><td>Mean rotor induced velocity in hover  $V _ { 1 }$ </td><td>4.03 m/s</td></tr><tr><td>Maximum energy consumption of UAV  $E _ { u , \mathrm { m a x } }$ </td><td>100 KJ</td></tr><tr><td>The constants of  $( 6 ) a , b$ </td><td>10, 0.6</td></tr><tr><td>Path loss exponent @</td><td>3.7</td></tr><tr><td>Noise power for all users  $N _ { 0 }$ </td><td> $1 0 ^ { - 1 0 } \mathrm { d B m }$ </td></tr><tr><td>Zipf exponent Îµ</td><td>0.7</td></tr><tr><td>Constant coefficient of reward  $\eta$ </td><td>300</td></tr></table>

<!-- image-->  
Fig. 5. Training processes of different algorithms.

Fig. 6(a)â(d) demonstrate a 300-episode training process at different time scales of C-DRL and I-DRL. In Fig. 6(a) and (b), one episode contains 100 time slots. In Fig. 6(c) and (d), one episode contains 200 time slots. Fig. 6(a) and (c) illustrate that I-DRL can shorten the convergence time of more than 100 episodes in slow timescale training compared with the C-DRL. Fig. 6(b) and (d) illustrate that I-DRL converges faster more than 4,000 time slots than C-DRL in fast timescale training.

<!-- image-->  
(a) Slow timescale DRL.

<!-- image-->  
(b) Fast timescale DRL.

<!-- image-->

<!-- image-->  
(c) Slow timescale DRL.  
(d) Fast timescale DRL.  
Fig. 6. Training processes of different time scales.

Thus, I-DRL is faster than C-DRL to converge, but the cumulative rewards of I-DRL is suboptimal, which are less than C-DRL. Additionally, fast timescale DRL converges faster than the slow timescale DRL through transverse comparison since fast timescale DRL has smaller state and action spaces. Besides, the number of timeslots we set in one episode depends on the action-and-state space of fast timescale training. If the space is not large, setting too many timeslots in one episode will waste computing resources. Instead, if the space is large, one episode should contain more timeslots to ensure the convergence of fast timescale training. By comparing Fig. 6(b) and (d), when one episode contains 200 time slots in our settings, both of the I-DRL and C-DRL have already converged, which may lead to a waste of computing resources.

Fig. 7 shows the scalability of our proposed MA-DRL algorithm under different CR loads. The scalability of a RL algorithm can be evaluated by measuring its convergence time over varying dataset sizes or user loads. As the number of users increases, the algorithm should be able to handle the load without a significant increase in convergence time. In Fig. 7, the MA-DRL algorithm converge almost simultaneously at 15.33 min when handling 100, 200, and 300 CR requests, indicating that our proposed MA-DRL algorithm is scalable and can effectively adjust to the changing demands of multiple CRs while maintaining an acceptable level of performance.

Fig. 8(a)â(c) show the performance comparisons among the proposed scheme and all the benchmarks as the system parameters change. Fig. 8(a) and (b) show the impact of the bandwidth B. Fig. 8(a) demonstrates the content hit ratio under different bandwidth sets. We see that the content hit ratio tends to increase as the bandwidth increases. This is because the more bandwidth the CPs allocate, the larger the data rate and the delivery success probability, which will improve the content hit ratio. Moreover, the transmission delay is affected by the content hit ratio as shown in Fig. 8(b). The higher content hit ratio means that CRs can retrieve more required files from CPs through D2D communications, which is time-saving. However, the lower content hit ratio results in CRs having to fetch the required files from a remote base station in a time-consuming manner. Fig. 8(c) shows the impact of the CR density. As expected, the increasing CR density indeed contributes to the growth in content hit ratio for all the schemes, since CPs still have sufficient storage space to cache coded fragments when the CR density is not too large. However, CPs can serve up to 40 CRs as the content hit ratio decreases dramatically when $M > 3 0$ . Besides, Fig. 8(c) indicates that 30the MA-DRL algorithm can always perform optimally as the CR continues to grow, which also shows the efficiency and robustness of our proposed framework. As illustrated in Fig. 8(a)â(c), MA-DRL and C-DRL always outmatch I-DRL and RCS no matter which metric is used. The reason lies in the fact that I-DRL and RCS train CPs independently, but C-DRL jointly optimizes the content placement and transmit power of all CPs through centralized training. The MA-DRL also follows the centralized training and decentralized execution paradigm to allow CPs to run separately while training jointly. The performance of RCS is the worst because CPs are clustered randomly without considering the delivery success probability between the CP and CR. CPs in a random cluster cannot satisfy the requests of CRs around them.

<!-- image-->  
Fig. 7. Training processes under different CR loads.

## C. Performance Evaluation of MA2T-DRL With Air-Ground Cooperation

After obtaining the decisions of CPs in problem ${ \mathcal { P } } _ { 2 } ,$ we optimize the UAV trajectory in $\mathcal { P } _ { 3 1 }$ and the content placement in $\mathcal { P } _ { 3 2 }$ by the greedy algorithm and the PSO algorithm respectively. In the greedy algorithm, the UAV flies to neighboring grids leading to the maximum content hit ratio in each step and flies back as long as the remaining energy is barely sufficient for returning. In the PSO algorithm, we first generate a group of particles, each of which has a position indicating a potential caching scheme. Then the fitness values of these particles are calculated based on the achievable content hit ratio.

<!-- image-->  
(a) Content hit ratio versus the bandwidth.

<!-- image-->  
(b) Transmission delay versus the bandwidth.

<!-- image-->  
(c) Content hit ratio versus the CR density.

Fig. 8. Performance comparison in terms of content hit ratio and transmission delay.  
<!-- image-->  
(a) Content hit ratio versus H(â³=5s).

<!-- image-->  
(b) Content hit ratio versus â³(H=15m).

<!-- image-->  
(c) Simulation running time.  
Fig. 9. Performance comparison under different UAV parameters.

In order to further evaluate the impact of UAV flying height H and update interval on the performance of content hit Îratio. We compare the greedy algorithm and the PSO algorithm with the exhaustive search (ES) algorithm at different flying heights and update intervals. Fig. 9(a)â(c) show the performance comparisons under different algorithm combinations.

Fig. 9(a) shows the performance comparison with different values of H. Basically, low UAV flying height implies a smaller UAV coverage area and leads to a refined division of the target area in the spatial domain. Therefore, with a smaller H, the hit ratio improvement for both algorithms increases due to the more sophisticated design of the caching scheme and UAV trajectory.

Fig. 9(b) shows the achievable content hit ratio with different values of $\Delta$ (The UAV endurance is equally discretized into $T$ Îtime slots, each with a time length of ). A small  indicates a Î Îfine-grained joint optimization in the time domain, while a large (e.g.,  equals the UAV endurance time) is more related to the Î Îcase of UAV deployment instead of trajectory design. Therefore, as shown in Fig. 9(b), when $\Delta$ is small, the UAV has more Îfreedom to serve CRs in different grids, and more contents can be transmitted to CRs, leading to the increase of the content hit ratio. When  is larger than 15 s, the UAV will hover in a fixed Îgrid, which is far away from CRs in other grids. In this situation, the content hit ratio will be small since CRs will obtain a small portion of contents from the UAV due to the low data rate. As illustrated in Fig. 9(a)â(b), the performance gap between the Greedy+PSO scheme and the ES only scheme is less than 10 , %which is almost negligible, and the gap gradually decreases with smaller H and .

Fig. 9(c) shows the execution time of the Greedy+PSO scheme and the ES only scheme. The execution time of the Greedy+PSO scheme is lower than 1 s, while the execution time of the ES only scheme is almost ,  s, with the difference more than 1 0003 orders of magnitude. Thus, the Greedy+PSO scheme is much less time-consuming than the ES only scheme. To sum up, the combination of greedy algorithm and PSO algorithm is both time-saving and effective.

## VI. CONCLUSION

In this work, we have investigated a joint communication and caching optimization problem in a UAV-assisted distributed coded caching network. Aiming at maximizing the overall content hit ratio, we have proposed a novel multiagent DRL algorithm MA2T-DRL for the power allocation and content placement of CPs. The CPs have been clustered by a weighted graph with edge weights determined by both physical link conditions and social ties between CPs and CRs. One of the CPs in each cluster was regarded as an agent, and we have leveraged two tier DQNs as local networks for each agent and the QMIX framework as the global aggregator. Furthermore, the trajectory and content placement of the UAV have been optimized by the greedy and PSO algorithms. Simulation results have shown that the content hit ratio can be effectively improved with our algorithms. The transmission delay and the simulation time of the proposed algorithms have also been demonstrated as well, which shows the advantage of low complexity of our algorithms.

## REFERENCES

[1] L. Wang, J. Zhang, J. Chuan, R. Ma, and A. Fei, âEdge intelligence for mission cognitive wireless emergency networks,â Wireless Commun., vol. 27, no. 4, pp. 103â109, Aug. 2020.

[2] B. Jedari, G. Premsankar, G. Illahi, M. D. Francesco, A. Mehrabi, and A. YlÃ¤-JÃ¤Ã¤ski, âVideo caching, analytics, and delivery at the wireless edge: A survey and future directions,â IEEE Commun. Surveys Tuts., vol. 23, no. 1, pp. 431â471, First Quarter 2021.

[3] F. Zhang, G. Han, L. Liu, M. MartÃ­nez-GarcÃ­a, and Y. Peng, âJoint optimization of cooperative edge caching and radio resource allocation in 5G-enabled massive IoT networks,â IEEE Internet Things J., vol. 8, no. 18, pp. 14156â14170, Sep. 2021.

[4] Y. Fu, L. SalaÃ¼n, X. Yang, W. Wen, and T. Q. S. Quek, âCaching efficiency maximization for device-to-device communication networks: A recommend to cache approach,â IEEE Trans. Wireless Commun., vol. 20, no. 10, pp. 6580â6594, Oct. 2021.

[5] M. Zhang, M. EI-Hajjar, and S. X. Ng, âIntelligent caching in UAVaided networks,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 739â752, Jan. 2022.

[6] F. Yin, M. Zeng, Z. Zhang, and D. Liu, âCoded caching for smart grid enabled HetNets with resource allocation and energy cooperation,â IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 12058â12071, Oct. 2020.

[7] M. Ji, G. Caire, and A. F. Molisch, âFundamental limits of caching in wireless D2D networks,â IEEE Trans. Inf. Theory, vol. 62, no. 2, pp. 849â869, Feb. 2016.

[8] H. Wu, L. Wang, T. Svensson, and Z. Han, âResource allocation for wireless caching in socially-enabled D2D communications,â in Proc. IEEE Int. Conf. Commun., Kuala Lumpur, Malaysia, 2016, pp. 1â5.

[9] C. Ma et al., âSocially aware caching strategy in device-to-device communication networks,â IEEE Trans. Veh. Technol., vol. 67, no. 5, pp. 4615â4629, May 2018.

[10] N.-S. Vo, T.-M. Phan, M.-P. Bui, X.-K. Dang, N. T. Viet, and C. Yin, âSocial-aware spectrum sharing and caching helper selection strategy optimized multicast video streaming in dense D2D 5G networks,â IEEE Syst. J., vol. 15, no. 3, pp. 3480â3491, Sep. 2021.

[11] N. Zhao et al., âCaching unmanned aerial vehicle-enabled small-cell networks: Employing energy-efficient methods that store and retrieve popular content,â IEEE Veh. Technol. Mag., vol. 14, no. 1, pp. 71â79, Mar. 2019.

[12] T. Zhang, Y. Wang, Y. Liu, W. Xu, and A. Nallanathan, âCache-enabling UAV communications: Network deployment and resource allocation,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7470â7483, Nov. 2020.

[13] P. A. Apostolopoulos, G. Fragkos, E. E. Tsiropoulou, and S. Papavassiliou, âData offloading in UAV-assisted multi-access edge computing systems under resource uncertainty,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 175â190, Jan. 2023.

[14] Z. Xiong et al., âUAV-assisted wireless energy and data transfer with deep reinforcement learning,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 1, pp. 85â99, Mar. 2021.

[15] T. Rashid, M. Samvelyan, C. Schroeder, G. Farquhar, J. Foerster, and S. Whiteson, âQMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning,â in Proc. Int. Conf. Mach. Learn., Stockholm, Sweden, 2018, pp. 4292â4301.

[16] S. Yin and F. Yu, âResource allocation and trajectory design in UAVaided cellular networks based on multiagent reinforcement learning,â IEEE Internet Things J., vol. 9, no. 4, pp. 2933â2943, Feb. 2022.

[17] C. Han, H. Yao, T. Mai, N. Zhang, and M. Guizani, âQMIX aided routing in social-based delay-tolerant networks,â IEEE Trans. Veh. Technol., vol. 71, no. 2, pp. 1952â1963, Feb. 2022.

[18] A. Mseddi, W. Jaafar, A. Moussaid, H. Elbiaze, and W. Ajib, âCollaborative D2D pairing in cache-enabled underlay cellular networks,â in Proc. IEEE Glob. Commun. Conf., Madrid, Spain, 2021, pp. 1â6.

[19] J. Rosenthal and R. Smarandache, âMaximum distance separable convolutional codes,â Appl. Algebra Eng. Commun. Comput., vol. 10, no. 1, pp. 15â32, Aug. 1999.

[20] H. Wu, F. Lyu, C. Zhou, J. Chen, L. Wang, and X. Shen, âOptimal UAV caching and trajectory in aerial-assisted vehicular networks: A learning-based approach,â IEEE J. Sel. Areas Commun., vol. 38, no. 12, pp. 2783â2797, Dec. 2020.

[21] Y. Liu, H. Huo, J. Fang, J. Mai, and S. Zhang, âUAV transmission line inspection object recognition based on mask R-CNN,â J. Phys., Conf. Ser., vol. 1345, no. 6, Nov. 2019, Art. no. 062043.

[22] L. Wang, H. Wu, Z. Han, P. Zhang, and H. V. Poor, âMulti-hop cooperative caching in social IoT using matching theory,â IEEE Trans. Wireless Commun., vol. 17, no. 4, pp. 2127â2145, Apr. 2018.

[23] A. G. Dimakis, K. Ramchandran, Y. Wu, and C. Suh, âA survey on network codes for distributed storage,â in Proc. IEEE, vol. 99, no. 3, pp. 476â489, Mar. 2011.

[24] A. G. Dimakis, P. B. Godfrey, Y. Wu, M. J. Wainwright, and K. Ramchandran, âNetwork coding for distributed storage systems,â IEEE Trans. Inf. Theory, vol. 56, no. 9, pp. 4539â4551, Sep. 2010.

[25] E. BaÂ¸stu Ëg et al., âBig data meets telcos: A proactive caching perspective,â J. Commun. Netw., vol. 17, no. 6, pp. 549â557, Dec. 2015.

[26] B. Chen and C. Yang, âCaching policy for cache-enabled D2D communications by learning user preference,â IEEE Trans. Commun., vol. 66, no. 12, pp. 6586â6601, Dec. 2018.

[27] Q. Hu, Y. Cai, G. Yu, Z. Qin, M. Zhao, and G. Y. Li, âJoint offloading and trajectory design for UAV-enabled mobile edge computing systems,â IEEE Internet Things J., vol. 6, no. 2, pp. 1879â1892, Apr. 2019.

[28] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[29] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â in Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[30] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[31] H. Wu, J. Chen, F. Lyu, L. Wang, and X. Shen, âJoint caching and trajectory design for cache-enabled UAV in vehicular networks,â in Proc. IEEE 11th Int. Conf. Wireless Commun. Signal Process., Xiâan, China, 2019, pp. 1â6.

[32] R. Li, C. Zhang, P. Patras, R. Stanica, and F. Valois, âLearning driven mobility control of airborne base stations in emergency networks,â ACM SIGMETRICS Perform. Eval. Rev., vol. 46, no. 3, pp. 163â166, Jan. 2019.

[33] L. Wang, H. Tang, and M. Cierny, âDevice-to-device link admission policy based on social interaction information,â IEEE Trans. Veh. Technol., vol. 64, no. 9, pp. 4180â4186, Sep. 2015.

[34] L. T. Tan and R. Q. Hu, âMobility-aware edge caching and computing in vehicle networks: A deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 67, no. 11, pp. 10190â10203, Nov. 2018.

[35] S. Yu, X. Chen, Z. Zhou, X. Gong, and D. Wu, âWhen deep reinforcement learning meets federated learning: Intelligent multi-timescale resource management for multi-access edge computing in 5G ultra dense network,â IEEE Internet Things J., vol. 8, no. 4, pp. 2238â2251, Feb. 2021.

<!-- image-->  
Bingxin Tian received the BE degree from Qingdao University, Qingdao, China, in 2019. He is currently working toward the PhD degree with the School of Electronic Engineering, Beijing University of Posts and Telecommunications (BUPT), Beijing, China. His research interests include edge caching, mobile edge computing, wireless resource management, and application of deep reinforcement learning for wireless networks.

<!-- image-->

Li Wang (Senior Member, IEEE) received the PhD degree from the Beijing University of Posts and Telecommunications (BUPT), Beijing, China, in 2009. She is currently a full professor with the School of Computer Science, National Pilot Software Engineering School, BUPT, where she is also an associate dean and the head of the High Performance Computing and Networking Laboratory. She is also a rotating director of the Key Laboratory of Application Innovation in Emergency Command Communication Technology, Ministry of Emergency Management,

China. She is also a member of the Key Laboratory of the Universal Wireless Communications, Ministry of Education, China. She also held visiting positions with the School of Electrical and Computer Engineering, Georgia Tech, Atlanta, GA, USA, from December 2013 to January 2015, and with the Department of Signals and Systems, Chalmers University of Technology, Gothenburg, Sweden, from August to November 2015 and July to August 2018. She has authored or coauthored almost 70 journal papers and four books. Her research interests include wireless communications, distributed networking and storage, vehicular communications, social networks, and edge AI. She currently serves on the editorial boards of the IEEE Transactions on Vehicular Technology, IEEE Transactions on Cognitive Communications and Networking, IEEE Internet of Things Journal, and China Communications. She was an associate editor of the IEEE Transactions on Green Communications and Networking, the symposium chair of IEEE ICC 2019 on Cognitive Radio and Networks Symposium and a tutorial chair of IEEE VTC 2019. She also is the chair of the Special Interest Group (SIG) on Sensing, Communications, Caching, and Computing (C3) in Cognitive Networks for IEEE Technical Committee on Cognitive Networks. She was the vice chair of Meetings and Conference Committee (MCC) for IEEE Communication Society (ComSoc) Asia Pacific Board (APB) for the term of 2020â2021. She was the recipient of the 2013 Beijing Young Elite Faculty for Higher Education Award, best paper awards from several IEEE conferences, IEEE ICCC 2017, IEEE GLOBECOM 2018, IEEE WCSP 2019. She was also the recipient of the Beijing Technology Rising Star Award in 2018. She has served on TPC of multiple IEEE conferences, including IEEE Infocom, Globecom, International Conference on Communications, IEEE Wireless Communications and Networking Conference, and IEEE Vehicular Technology Conference in recent years.

<!-- image-->  
Lianming Xu received the BE degree from the Hefei University of Technology, Hefei, China, in 2003, and the PhD degree from the Beijing University of Posts and Telecommunications (BUPT), Beijing, China, in 2009. He is currently an assistant professor with the School of Electronic Engineering, BUPT. His research interests include edge intelligence, Internet of Things, caching, and collaborative computing.

<!-- image-->

Wen Pan received the BE degree from Shandong University, Jinan, China, in 2007. She is currently working as a senior software R&D engineer with Beijing Xiaomi Mobile Software Co., Ltd. Her research interests include front-end application frameworks, IoT distributed systems, and edge intelligent application.

<!-- image-->

Huaqing Wu (Member, IEEE) received the BE and ME degrees from the Beijing University of Posts and Telecommunications, Beijing, China, in 2014 and 2017, respectively, and the PhD degree from the University of Waterloo, Ontario, Canada, in 2021. She received the prestigious Natural Sciences and Engineering Research Council of Canada (NSERC) Postdoctoral Fellowship Award in 2021 and worked as a postdoctoral fellow with the Department of Electrical and Computer Engineering, MacMaster University, from 2021 to 2022. She is currently an assistant pro-

fessor with the Department of Electrical and Software Engineering, University of Calgary, Alberta, Canada. Her current research interests include B5G/6 G, space-air-ground integrated networks, Internet of vehicles, mobile/edge computing/caching, artificial intelligence (AI) for future networking. She received the Best Paper Awards at IEEE GLOBECOM 2018, Chinese Journal on Internet of Things 2020, and IEEE GLOBECOM 2022.

<!-- image-->

Liang Li (Member, IEEE) received the PhD degree from the School of Telecommunications Engineering, Xidian University, Xiâan, China, in 2021. She is currently a postdoctoral faculty member with the School of Computer Science (National Pilot Software Engineering School), Beijing University of Posts and Telecommunications, Beijing, China. She was also a visiting PhD student with the Department of Electrical and Computer Engineering, University of Houston, Houston, TX, USA, from 2018 to 2020. Her research interests include edge computing, federated learning, data-driven robust optimization, and differential privacy.

<!-- image-->

Zhu Han (Fellow, IEEE) received the BS degree in electronic engineering from Tsinghua University, in 1997, and the MS and PhD degrees in electrical and computer engineering from the University of Maryland, College Park, in 1999 and 2003, respectively. From 2000 to 2002, he was an R&D engineer of JDSU, Germantown, Maryland. From 2003 to 2006, he was a research associate with the University of Maryland. From 2006 to 2008, he was an Assistant Professor with Boise State University, Idaho. Currently, he is a John and Rebecca Moores professor with the Electrical and Computer Engineering Department as well as in the Computer Science Department, University of Houston, Texas. His main research targets on the novel game-theory related concepts critical to enabling efficient and distributive use of wireless networks with limited resources. His other research interests include wireless resource allocation and management, wireless communications and networking, quantum computing, data science, smart grid, security, and privacy. He received an NSF Career Award in 2010, the Fred W. Ellersick Prize of the IEEE Communication Society in 2011, the Best Paper Award for the EURASIP Journal on Advances in Signal Processing in 2015, the IEEE Leonard G. Abraham Prize in the field of Communications Systems (Best Paper Award in IEEE JOURNAL ON SELECTED AREAS IN COMMUNICA-TIONS) in 2016, and several best paper awards in IEEE conferences. He was an IEEE Communications Society distinguished lecturer from 2015 to 2018, AAAS fellow since 2019, and ACM distinguished member since 2019. He is a 1% highly cited researcher since 2017 according to Web of Science. He is also the Winner of the 2021 IEEE Kiyo Tomiyasu Award, for outstanding early to mid-career contributions to technologies holding the promise of innovative applications, with the following citation: âfor contributions to game theory and distributed management of autonomous communication networks.â

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_9_img_1.jpeg|page_9_img_1]]
3. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_12_img_1.jpeg|page_12_img_1]]
4. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_13_img_1.png|page_13_img_1]]
5. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_13_img_2.jpeg|page_13_img_2]]
6. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_15_img_1.jpeg|page_15_img_1]]
7. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_16_img_1.jpeg|page_16_img_1]]
8. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_16_img_2.jpeg|page_16_img_2]]
9. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_16_img_3.jpeg|page_16_img_3]]
10. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_16_img_4.jpeg|page_16_img_4]]
11. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_16_img_5.jpeg|page_16_img_5]]
12. [[../extracted_images/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an/page_16_img_6.jpeg|page_16_img_6]]

---

