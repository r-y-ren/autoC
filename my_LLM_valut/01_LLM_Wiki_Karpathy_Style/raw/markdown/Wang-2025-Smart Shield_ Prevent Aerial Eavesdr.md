# Smart Shield: Prevent Aerial Eavesdropping via Cooperative Intelligent Jamming Based on Multi-Agent Reinforcement Learning

Qubeijian Wang , Member, IEEE, Shiyue Tang, Wen Sun , Senior Member, IEEE,

Yin Zhang , Senior Member, IEEE, Geng Sun , Senior Member, IEEE, Hong-Ning Dai , Senior Member, IEEE, and Mohsen Guizani , Fellow, IEEE

AbstractâThe spotlight on autonomous aerial vehicles (AAVs) is to enhance wireless communications while ignoring the potential risk of AAVs acting as adversaries. Due to their mobility and flexibility, AAV eavesdroppers pose an immeasurable threat to legitimate wireless transmissions. However, the existing fixed jamming scheme without cooperation cannot counter the flexible and dynamic AAV eavesdropping. In this article, a cooperative intelligent jamming scheme is proposed, authorizing ground jammers (GJs) to interfere with AAV eavesdroppers, generating specific jamming shields between AAV eavesdroppers and legitimate users. Toward this end, we formulate a secrecy capacity maximization problem and model the problem as a decentralized partially observable Markov decision process (Dec-POMDP). To address the challenge of the huge state space and action space with network dynamics, we leverage a deep reinforcement learning (DRL) algorithm with a dueling network and double-Q learning (i.e., dueling double deep Qnetwork) to train policy networks. Then, we propose a multi-agent mixing network framework (QMIX)-based collaborative jamming algorithm to enable GJs to independently make decisions without sharing local information. Additionally, we perform extensive simulations to validate the superiority of our proposed scheme and present useful insights into practical implementation by elucidating the relationship between the deployment settings of GJs and the instantaneous secrecy capacity.

Index TermsâAnti-eavesdropping, collaborative jamming, MARL, power allocation, trajectory design, AAV.

Digital Object Identifier 10.1109/TMC.2024.3505206

## I. INTRODUCTION

W ITH advancements in intelligent control, precision guid-ance, and energy supply technologies [1], Autonomous ance,and energy supply technologies [1], Autonomous Aerial Vehicles (AAVs) have become invaluable in various fields, including environmental monitoring, military operations, and civilian applications. Their ability to perform rapid deployment and flexible networking makes them powerful assets in wireless communications [2], [3]. However, the increasing number of deployed AAVs, if controlled or disguised by adversaries, poses significant and unpredictable threats to wireless communication security [4]. Due to their high mobility and flexibility, AAVs can hover at strategic positions to intercept confidential data on wireless channels, acting as eavesdroppers. This threat is particularly critical in sensitive environments such as military operations, where AAV eavesdropping can compromise mission-critical information, and in civilian sectors, where it can lead to breaches of personal and corporate data. Moreover, AAV eavesdroppers benefit from high eavesdropping channel quality due to dominant line-of-sight (LoS) gain, enhancing their interception capabilities. Recent research has demonstrated the potential risks and technical challenges associated with AAV eavesdropping, emphasizing the need for robust security measures [5], [6]. Therefore, developing effective countermeasures against AAV eavesdroppers is both imperative and vital to protect the integrity of systems for wireless communication across various domains.

The physical layer security (PLS) technology has been demonstrated its superiority in mitigating the threat of eavesdropping by destroying eavesdropping channels [7], [8], which can be composed as complementary to traditional encryption. In particular, friendly jamming, as a classical approach to PLS techniques, reduces the signals to interference plus noise ratio (SINR) of the eavesdropping channel by emitting artificial noise [9]. Compared to other PLS techniques such as beamforming, friendly jamming can be more effective in countering AAV eavesdropping, since it is flexibly deployed according to the location of the AAV eavesdropper, the network size and channel quality. Additionally, since the air-to-ground (A2G) link always has better channel quality than the ground-to-ground (G2G) link (A2G links are dominated by LoS gain), the jamming effect of ground jammers interfering with AAVs outweighs the effect on ground users at certain jamming locations and jamming powers. Therefore, we utilize mobile ground jammers (GJs) to find the optimal moving trajectory (i.e., jamming trajectory) and power to counter AAV eavesdropping while ensuring the quality of legitimate communications [10].

Nevertheless, existing studies on mobile ground jamming encounter several significant challenges in countering AAV eavesdropping. First, real-time dynamics in wireless channels contribute to increased complexity in task allocation for GJs [11]. Particularly, conventional optimization methods, e.g., successive convex approximation (SCA) and block coordinate descent (BCD) algorithms, struggle to accommodate the dynamics of networks and fulfill the intelligence of GJs. Furthermore, the trajectory design of the GJ is contingent upon having access to the complete eavesdropping trajectory, but owing to the unpredictability of the trajectory of the AAV eavesdropper, the complete and accurate eavesdropping trajectory is barely obtained in advance. It is inaccurate to speculate the optimal jamming trajectory through the AAV eavesdropperâs positional information at the moment. Therefore, calculating the optimal jamming trajectory based on the real-time acquired AAV eavesdropperâs position needs to be solved urgently. Additionally, the mobility speed of the GJ is obviously lower than that of the AAV eavesdropper, which leads to diminished effectiveness in a single GJ and fails to guarantee the secrecy capacity of the system.

Deep reinforcement learning (DRL), exploring the optimal sequential decisions through interactions between the agent and the environment [12], empowers GJs with intelligence against AAV eavesdropping in dynamic networks. Then, to improve the accuracy of predicting the optimal jamming trajectory, we utilize the real-time trajectory sequence of the AAV eavesdropper as the basis and dynamically compute the jamming trajectory through DRL. To overcome the unequal speed between the AAV eavesdropper and the jammer, collaborative jamming by multiple GJs becomes a key issue. Multi-agent reinforcement learning (MARL) provides a promising solution for GJs to execute collaborative jamming tasks, because MARL can facilitate collaboration between agents by sharing observations and decisions [13]. However, sharing information during collaborative jamming among GJs is challenging. Real-time AAV eavesdropper trajectory information will cause lag after being shared among GJs. Moreover, information-sharing also hampers the decision-making efficiency of GJs, as it is operated as a basis for decision-making in dynamic environments.

To overcome the aforementioned challenges, a collaborative intelligent jamming scheme is proposed as shown in Fig. 1. Through the collaboration of GJs emitting jamming signals, an invisible shield is generated between the AAV eavesdropper and the user. Each GJ can independently make decisions with its own observation, while jointly forming the best jamming strategy. This paper has the following major innovations.

We first propose a cooperative intelligent jamming scheme to prevent AAV eavesdropping. Specifically, multiple GJs dynamically optimize their trajectories and jamming power to generate specific jamming shields between AAV eavesdroppers and legitimate users. Then, we formulate a joint

<!-- image-->  
Jamming Eavesdropping Legitimate Communication UAV Trajectory Jammer Trajectory

Fig. 1. Cooperative intelligent jamming scheme.

optimization problem of trajectory and jamming power for GJs to maximize the secrecy capacity.

We then transform the optimization problem into a Dec-POMDP, owing to the non-convexity of the problem. GJs can adapt their jamming trajectories and jamming power, without complete information from the dynamic networks. Moreover, to overcome the huge state space and action space, we employ a DRL algorithm featuring a dueling network and double-Q learning (i.e., dueling double deep Q-network) to train policy networks.

We also propose a multi-agent mixing network framework (QMIX)-based collaborative jamming algorithm to enhance the effectiveness of collaboration among multiple GJs. The algorithm enables GJs to independently design their own trajectories and jamming power without sharing local information. However, the ultimate objective for all GJs is to maximize the overall security capacity.

C We further validate the performance of the proposed cooperative intelligent jamming scheme by simulations. Results show that the proposed scheme can maximumly prevent AAV eavesdropping in the premise of ensuring legitimate transmissions, outperforming benchmark schemes. Our results also reveal the relationship between the deployment settings of GJs and the instantaneous secrecy capacity with different parameters.

The rest of this paper is organized as follows. Section II briefly summarizes the related work. In Section III, the system model and problem formulation are introduced in detail. In Section IV, we formulate the optimization problem as Dec-POMDP and introduce our proposed QMIX-based collaborative jamming algorithm with the dueling double deep Qnetwork (dueling DDQN) to realize collaborative jamming. In Section V, we also present the numerical results with analysis. In Section VI, we discuss the implementation of our scheme and future work with promising techniques. Finally, Section VII gives a conclusion of this paper.

TABLE I  
THE COMPARISON OF EXISTING WORKING ANTI-EAVESDROPPING SCHEMES
<table><tr><td rowspan=2 colspan=1>Anti-Eavesdropping scheme</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>Eavesdroppercategory</td><td rowspan=1 colspan=1>Number ofeavesdroppers</td><td rowspan=1 colspan=1>Eavesdroppinglocation</td><td rowspan=1 colspan=1>Mobility ofeavesdroppers</td><td rowspan=1 colspan=1>Extrarelay</td><td rowspan=1 colspan=1>Scalability ofprotected area</td></tr><tr><td rowspan=1 colspan=1>Friendly jammingand aerial relay [14]</td><td rowspan=1 colspan=1>Ground</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>Known</td><td rowspan=1 colspan=1>Fixed</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Flexible</td></tr><tr><td rowspan=1 colspan=1>Beamforming and aerial relay [18]</td><td rowspan=1 colspan=1>Ground</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>Unknown</td><td rowspan=1 colspan=1>Fixed</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Flexible</td></tr><tr><td rowspan=1 colspan=1>Intelligent reflecting surfaceand beamforming [19]</td><td rowspan=1 colspan=1>Ground</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Known</td><td rowspan=1 colspan=1>Fixed</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Inflexible</td></tr><tr><td rowspan=1 colspan=1>Intelligent reflecting surfaceand friendly jamming [20]</td><td rowspan=1 colspan=1>Ground</td><td rowspan=1 colspan=1> Multiple</td><td rowspan=1 colspan=1>Known</td><td rowspan=1 colspan=1>Fixed</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Flexible</td></tr><tr><td rowspan=1 colspan=1>Intelligent reflecting surfaceand aerial relay [21]</td><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>Unknown</td><td rowspan=1 colspan=1>Mobile</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Inflexible</td></tr><tr><td rowspan=1 colspan=1>Friendly jammingand trajectory optimization [16]</td><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>Known</td><td rowspan=1 colspan=1>Mobile</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Inflexible</td></tr><tr><td rowspan=1 colspan=1>Mobile friendly jamming[10]</td><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>Known</td><td rowspan=1 colspan=1>Mobile</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Flexible</td></tr><tr><td rowspan=1 colspan=1>Our scheme</td><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Unknown</td><td rowspan=1 colspan=1>Mobile</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Flexible</td></tr></table>

## II. RELATED WORK

Recently, many studies focused on terrestrial eavesdropping, while ignoring the threat from aerial eavesdropping [14], [15]. However, some studies [16], [8] have noticed that the AAV eavesdropper can bring unpredictable threats to future networks. As a physical layer security technology, friendly jamming has been proven to be an effective method to improve the security of wireless communications [17], [6]. The traditional jamming method for countering eavesdropping is to deploy fixed jammers or relays [14]. Meanwhile, some works also focus on beamforming [18] as well as intelligent reflecting surfaces (IRS) [19], [20] to dynamically adjust the beam of jamming signals. Then, to effectively prevent flexible AAV eavesdroppers, a secure aerial relay method is proposed by the orchestration of AAV and IRS [21]. However, a large number of active antennas and extra devices bring heavy hardware costs and system complexity. In [16], the authors propose a secure transmission scheme supported by a fixed-ground jammer to disturb AAV eavesdroppers. Nevertheless, the effectiveness of a single fixed-ground jammer is limited due to the flexibility of AAV eavesdroppers and their extensive eavesdropping range. Meanwhile, an increased number of jammers increases extra costs. Therefore, a mobile ground jammer scheme is proposed [10], to dynamically follow the trajectory of the AAV eavesdropper and interfere with it. Then, they explored optimal jamming strategies by the alternative-optimization method. However, the existing work has ignored the mobility limitations of mobile ground jammers, i.e., the speed of the mobile ground jammer is much lower than that of the AAV eavesdropper. Furthermore, dynamic networks with AAVs also increase the complexity of task assignments for jamming strategies. We summarize the differences between our work and relevant literature on anti-AAV eavesdropping in Table I.

Model-free DRL is regarded as a pivotal technology to handle dynamic environments, promoting intelligent networks [22], [23]. To fully utilize the flexibility of mobile nodes, some studies focus on DRL-based trajectory design and resource allocation. In [24], deep deterministic policy gradient (DDPG) is utilized to achieve real-time scheduling of the trajectory of a AAV base station (BS) by solving the problem of an infinite number of state-action pairs. Moreover, a DRL-based joint trajectory design and power allocation scheme is investigated to further enhance the performance of an aerial BS [25]. Additionally, DRL is also adopted in friendly jamming to secure wireless communications [26]. The authors in [27] designed an algorithm based on DDPG to address the joint optimization problem of jamming trajectory and jamming power for a single AAV jammer. However, the huge state and action space challenge and overestimation of action values by the policy network, arising from joint trajectory design and power allocation, makes convergence more prone to falling into a local optimum [28], [29]. Dueling DDQN is considered to be effective in addressing these challenges. In [11], the authors optimized the trajectory of the AAV using dueling DDQN, obtaining an improvement in convergence and performance compared to standard deep Qnetwork (DQN). Nevertheless, since eavesdroppers often appear in groups, a single jammer cannot withstand the attacks of many eavesdroppers from different. Besides, the mobility speed of GJs is obviously lower than that of AAV eavesdroppers, leading to diminished effectiveness in a single GJ.

The application of MARL in wireless networks for optimizing trajectory design and power allocation of flexible network nodes has been studied. In [30], the authors utilized the DQNemployed MARL framework to enable AAV base stations to move between multiple target service areas according to service requirements. Then, to enhance the mobility of AAV base stations (allowing them to move freely without being bounded in a specific region), a multi-agent deep deterministic policy gradient (MADDPG)-based algorithm is proposed in [31]. The collaboration of AAV base stations in [30], [31] is implemented with information sharing among each agent. However, sharing information challenges the effectiveness of collaborative jamming when using GJs against AAV eavesdroppers. Trajectory information of AAV eavesdroppers is hard to share between GJs in real-time, leading to a trajectory information lag. Besides, the efficiency of decision-making for GJs relies on the quality of information sharing. Therefore, MARL with information sharing is not suitable for collaborative problems of GJs, such as MADDPG, multi-agent proximal policy optimization, etc.

Considering the training cost and scalability, value function factorization (VFF) is demanded as a promising method for MARL [32], [33]. For large-scale multi-agent systems, traditional MARL algorithms face huge computational complexity. VFF can decompose the learning problem of the joint policy network into multiple small-scale learning problems of the local policy network, thereby reducing computational complexity and improving learning efficiency [34]. Furthermore, when the new agent joins the system, it only needs to learn its own local policy network, and then combining with the other local policy networks [32]. By this approach, the scalability of MARL can be further enhanced. Therefore, MARL with VFF framework is wildly investigated in non-information sharing multi-agent learning algorithms, e.g., independent Q-learning (IQL), value decomposition networks (VDNs) [32], and QMIX. Particularly, the framework of the Actor-Critic network [35] and the idea of centralized training and decentralized execution have been integrated into QMIX, which has shown significant superiority [33].

<!-- image-->  
Fig. 2. Cooperative intelligent jamming system model.

From the aforementioned studies, we can observe that the implementation of cooperative intelligent jamming still faces obstacles. Especially, AAV eavesdropping with speed advantages and unpredictable eavesdropping trajectories challenge the effectiveness of collaboration jamming. Motivated by the superiority of QMIX, we proposed a QMIX-based collaborative jamming algorithm with the dueling network and double-Q learning for GJs to independently make decisions without sharing observations.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, we first present a system model of our cooperative intelligent jamming scheme to protect the AAV eavesdropper wiretapped wireless terrestrial networks, as depicted in Fig. 2. Then, we optimally deploy GJs with the appropriate location and jamming power by formulating a problem to maximize overall secrecy capacity.

## A. Network Model

In this paper, we mainly focus on a wiretapped terrestrial network, in which K legitimate users transmit confidential information to the BS while M malicious AAV eavesdroppers are present. AAV eavesdroppers hover in the air at the height H with flight speed $V _ { e } .$ , wiretapping on legal transmissions. To continuously prevent such wiretapping from AAV eavesdroppers, we propose a ground mobile jamming scheme. Specifically, N GJs are responsible for degrading the eavesdropping channel to protect legitimate transmissions. GJs dynamically and intelligently adjust their moving trail with speed $V _ { j }$ and emit directional disturbing signals to AAV eavesdroppers according to their real-time locations and channel state information (CSI). Then, the location of AAV eavesdropper m projected on the ground is denoted as $q _ { e , m } = \{ x _ { e , m } , y _ { e , m } \}$ . The location of user k can be represented by $q _ { u , k } = \{ x _ { u , k } , y _ { u , k } \}$ . The location of GJ n is denoted as $q _ { j , n } = \{ x _ { j , n } , y _ { j , n } \}$ . The locations of the BS can be represented by $q _ { b } = \{ x _ { b } , y _ { b } \}$

## B. Channel Model

In this paper, there are two types of communication links, including the G2G communication link and the A2G communication link.

G2G link: It is the transmission on the ground, which predominantly experiences Rayleigh fading and path loss effects, including transmissions from legitimate users to the BS and interference from jammers to the BS. Then, The received power of the BS is described, which can be described as $P _ { t } h _ { U B } d _ { U B } ^ { - \alpha } ,$ where $P _ { t }$ denotes the userâs transmit power, $d _ { U B }$ is the Euclidean distance between the user and the BS calculated by $d _ { U B } = \sqrt { | | q _ { u , k } - q _ { b } | | ^ { 2 } }$ , the channel coefficient is denoted by $h _ { U B }$ between the BS and the user, and the path loss factory represented by $\alpha .$ . Correspondingly, the interference at the BS is represented as $P _ { j } G _ { s } h _ { J B } d _ { J B } ^ { - \alpha }$ , where $P _ { j }$ denotes the jamming power, the Euclidean distance is expressed by $d _ { J B }$ between the GJ and the BS calculated by $d _ { J B } = \sqrt { | | q _ { j , n } - q _ { b } | | ^ { 2 } }$ , and the channel coefficient is denoted by $h _ { J B }$ between the BS and the GJ, and $G _ { s }$ represents the side/back-lobe gain of antennas at GJs. Note that this interference is caused by leaked jamming signals from directional antennas deployed at GJs.

A2G link: It is modeled by the transmission from the ground nodes (i.e., the user or the jammer) to the AAV eavesdropper. A2G communication mainly includes a Line-of-sight (LoS) link and a None LoS (NLoS) link. In particular, we denote the probability of LoS link as

$$
\mathbb { P } _ { \mathrm { L o S } } = \frac { 1 } { 1 + \tau \exp { \left( - \psi \left( \varphi - \tau \right) \right) } } ,\tag{1}
$$

where $\begin{array} { r } { \varphi = \frac { 1 8 0 } { \pi } \arctan ( \frac { H } { d _ { U E } } ) } \end{array}$ represents the elevation angle of the $\mathrm { A A V } , \psi$ and Ï are constant values depending on the environment. Moreover, we further calculate the probability of NLoS link $\mathbb { P } _ { \mathrm { N L o S } } = 1 - \mathbb { P } _ { \mathrm { L o S } }$ . Referring to [36], NLoS links are affected by small-scale fading as well as path loss, while LoS links only experience path loss effect. Accordingly, the received power of the AAV can be given by

$$
P _ { e } = \mathbb { P } _ { \mathrm { L o S } } P _ { t } G _ { e } d _ { U E } ^ { - \alpha _ { e } } + \mathbb { P } _ { \mathrm { N L o S } } h _ { U E } P _ { t } G _ { e } d _ { U E } ^ { - \alpha _ { e } } ,\tag{2}
$$

where $G _ { e }$ is the received antenna gain at the AAV eavesdropper, and the Euclidean distance between is represented as $d _ { U E }$ the

AAV eavesdropper and the user, which is calculated by $d _ { U E } =$ $\sqrt { | | q _ { u } - q _ { e } | | ^ { 2 } + H ^ { 2 } } , \alpha _ { \epsilon }$ is the path loss factor, and $h _ { U E }$ is the small-scale fading factor. Similarly, we denote the interference received by the AAV eavesdropper as

$$
\mathcal { T } _ { j } = \mathbb { P } _ { \mathrm { N L o S } } P _ { j } G _ { e } G _ { j } h _ { J E } d _ { J E } ^ { - \alpha _ { e } } + \mathbb { P } _ { \mathrm { L o S } } P _ { j } G _ { e } G _ { j } d _ { J E } ^ { - \alpha _ { e } } ,\tag{3}
$$

where $G _ { j }$ is the antenna gain at the GJ, and the Euclidean distance is denoted by $d _ { J E }$ from the user to the AAV eavesdropper, calculated by $d _ { J E } = \sqrt { | | q _ { j } - q _ { e } | | ^ { 2 } + H ^ { 2 } }$ , the channel coefficient is represented by $h _ { J E }$ between the jammer and the eavesdropper.

Therefore, the SINR of the BS is represented by $\zeta _ { b }$ , being denoted as follows

$$
\zeta _ { b } = \frac { P _ { t } h _ { U B } d _ { U B } ^ { - \alpha } } { \sigma ^ { 2 } + P _ { j } G _ { s } h _ { J B } d _ { J B } ^ { - \alpha } } ,\tag{4}
$$

where $\sigma ^ { 2 }$ is the Gaussian noise. In addition, the SINR of the AAV eavesdropper, represented by $\zeta _ { e } ,$ , is denoted by

$$
\zeta _ { e } = \frac { P _ { e } } { \sigma ^ { 2 } + \mathcal { T } _ { j } } .\tag{5}
$$

Then, we define the instantaneous secrecy capacity, which is represented as

$$
C ( q _ { j , n } , P _ { j } ) = \left[ \log \left( 1 + \zeta _ { b } \right) - \log \left( 1 + \zeta _ { e } \right) \right] ^ { + } ,\tag{6}
$$

where $C ( q _ { j , n } , P _ { j } )$ is non-negative, and $[ x ] ^ { + } \triangleq$ max(x, 0).

## C. Problem Formulation

To assure the quality of the secure transmission, GJs are required to degrade the effect on the legitimate transmission (i.e., the transmission between the user and the BS) while enhancing the interference on the wiretapped transmission (i.e., the transmission between the AAV eavesdropper and the BS). In this case, GJs need to move toward the AAV eavesdropper as close as possible, meanwhile, away from the legitimate user. Additionally, to minimize the effect on legitimate transmissions, GJs need to efficiently and reasonably allocate the jamming power. Therefore, to maximize the secrecy capacity, an optimization problem is formulated through joint trajectory design and jamming power allocation. Then, our overall secrecy capacity maximization problem is expressed as

$$
( \mathrm { P 0 } ) : \operatorname* { m a x } _ { \{ q _ { j , n } , P _ { j } \} } \sum _ { k = 1 } ^ { K } \overline { { C } } _ { k } \left( q _ { j , n } , P _ { j } \right) ,\tag{7}
$$

$$
{ \mathrm { s . t . ~ } } V _ { j } \leq V _ { \operatorname* { m a x } } ,\tag{7a}
$$

$$
r _ { \operatorname* { m i n } } \leq \| q _ { j , n } \| _ { 2 } \leq r _ { \operatorname* { m a x } } ,\tag{7b}
$$

$$
0 \leq P _ { j } \leq P _ { \operatorname* { m a x } } ,\tag{7c}
$$

$$
\zeta _ { b } > \zeta _ { t h } ,\tag{7d}
$$

where $\overline { { C } } _ { k } ( q _ { j , n } , P _ { j } )$ represents the overall secrecy capacity of user k. Herein, constraint (7a) ensures that the movement speed of the GJ is within the maximum speed $V _ { \mathrm { m a x } }$ . Constraint (7b) ensures that the GJ moves within the target region. Note that $r _ { \mathrm { m i n } }$ represents the minimum radius of the movement range (centered on the BS) to reduce the degradation of the legitimate transmission. Meanwhile, $r _ { \mathrm { m a x } }$ represents the maximum radius of the movement range (centered on the BS) to guarantee the effectiveness of GJs since they can quickly respond to the next eavesdropping. In the constraint (7c), the jamming power is limited by the maximum jamming power $P _ { \mathrm { m a x } }$ . Finally, in constraint (7d), to assure essential transmission quality, the $\zeta _ { b }$ need exceed a threshold value $\zeta _ { t h }$ . Obviously, the problem (P0) is highly non-convex and challenging to solve directly, owing to the dynamic network topology resulting from the mobility of both jammers and AAV eavesdroppers. However, DRL enables agents to make near-optimal decisions in dynamic networks with highdimensional state spaces by modeling the optimization problem as a Markov decision process. Consequently, DRL effectively addresses the overall secrecy capacity maximization problem by leveraging its powerful prediction and decision-making in jamming trajectory design and jamming power allocation.

## IV. REINFORCEMENT LEARNING SOLUTION

In this section, we propose a DRL-based solution to solve our overall secrecy capacity maximization problem. As shown in Fig. 3, the policy network is organized into agent networks and a mixing network. Specifically, each GJ deploys an agent network, and agent networks enable collaborative decision making through mixing networks. To solve (P0) using the DRL-based solution, the optimization problem (P0) is reformulated into a Dec-POMDP. Then, we present a dueling DDQN-based algorithm of each independent agent network. Finally, we introduced a mixing network based on the QMIX framework to enable collaborative jamming for all GJs.

## A. Cooperative Markov Game Formulation

To model the Markov decision process, we first decompose the eavesdropping period into T time steps with a certain interval $\Delta t$ . Note that $\Delta t$ is small enough to ensure that the location $q _ { j } [ t ]$ of GJs, the location $q _ { e } [ t ]$ of AAV eavesdroppers and the jamming power $P _ { j } [ t ]$ of GJs are approximately unchanged within a time step $t \in [ 1 , 2 , 3 , \ldots , T ]$ . Then, $\| q _ { j } [ t ] - q _ { j } [ t - 1 ] \| \leq \Delta s ,$ ât, where $\Delta s = V _ { \operatorname* { m a x } } \Delta t$ is the maximum movement distance per step. Theoretically, the optimal solution of (P0) requires that the GJs quickly move close to the AAV eavesdropper with the maximum speed. Therefore, the constraint (7a) can be rewritten as

$$
q _ { j } [ t + 1 ] = q _ { j } [ t ] + \overrightarrow { V _ { j } } [ t ] \triangle s , \forall t\tag{8}
$$

where $\vec { V _ { j } } [ t ]$ is the direction vector at the time step t, satisfying $\| \vec { V _ { j } } \| = \bar { 1 }$ . In addition, constraint (7c) can be rewritten as

$$
0 \leq P _ { j } [ t ] \leq P _ { \operatorname* { m a x } } , \forall t\tag{9}
$$

where $P _ { j } [ t ]$ represents the jamming power of the GJ n at time step t. Since the location of the GJs and the eavesdroppers are quasi-static in each time step t, the overall secrecy capacity $\bar { \overline { { { C } } } } _ { k } ( q _ { j , n } [ t ] , P _ { j } [ t ] )$ for user k is approximately given as follows

$$
\overline { { C } } _ { k } \left( q _ { j , n } [ t ] , P _ { j } [ t ] \right) = \sum _ { t } ^ { T } C _ { k } \left( q _ { j , n } [ t ] , P _ { j } [ t ] \right) , \forall t\tag{10}
$$

<!-- image-->  
Fig. 3. Cooperative intelligent jamming framework for GJs.

where $C _ { k } ( q _ { j , n } [ t ] , P _ { j } [ t ] )$ represents the instantaneous secrecy capacity of user k. Consequently, (P0) is approximately expressed as

$$
( \mathrm { P 1 } ) : \operatorname* { m a x } _ { \{ q _ { j , n } [ t ] , P _ { j } [ t ] \} } \sum _ { t } ^ { T } \sum _ { k } ^ { K } C _ { k } \left( q _ { j , n } [ t ] , P _ { j } [ t ] \right) ,\tag{11}
$$

$$
\mathrm { ~ s . t . ~ } q _ { j , n } [ t + 1 ] = q _ { j , n } [ t ] + \overrightarrow { V _ { j } } [ t ] \triangle s , \forall t\tag{11a}
$$

$$
r _ { \operatorname* { m i n } } \le \| q _ { j , n } [ t ] \| _ { 2 } \le r _ { \operatorname* { m a x } } , \forall t\tag{11b}
$$

$$
0 \leq P _ { j } [ t ] \leq P _ { \operatorname* { m a x } } , \forall t\tag{11c}
$$

$$
\zeta _ { b } [ t ] > \zeta _ { t h } , \ \forall t\tag{11d}
$$

In our scheme, all GJs are independently coordinated in a decentralized way for cooperative jamming against eavesdropping, hence, the observations and decisions cannot be shared among GJs. This cooperative multi-agent task is determined as Dec-POMDP, which is defined by the five-tuple $\{ S , \mathbb { A } , { \mathcal { O } } , { \mathcal { P } } , r \}$ , where S represents the global state space, and O is the observation space. At each time step, the state of the environment is given as $s \in S$ and the observations of the agents in the environment are denoted as $o \in \mathcal { O }$ . The joint action space of all GJs is denoted as $\mathbb { A } = \mathcal { A } _ { 1 } \times \times \ldots \mathcal { A } _ { n } \ldots \times \mathcal { A } _ { N }$ , where $A _ { n }$ denotes the set of independent action space of GJ n. Furthermore, P is the state transition probability. Then, $\mathcal { P } ( s [ t + 1 ] | s [ t ] , a [ t ] )$ ) specifies the probability of transitioning from the state $s [ t ]$ to the next state $s [ t + 1 ] \in S$ by the action $a [ t ] \in \mathbb { A }$ . Then, the single-step reward at time t is given as $r [ t ] = r ( s [ t ] , a [ t ] )$ , which is determined by the state $s [ t ]$ and action a[t]. Additionally, the action of the GJ is governed by its policy Ï, where the probability of taking action a in state s is given by $\pi ( a | s )$

To model the joint trajectory design and the jamming power selection problem strength into the DRL framework, we define the necessary elements in Dec-POMDP.

1) State: To find the optimal trajectory design and jamming power allocation, the GJ needs to observe necessary environmental information, including locations and transmit power. Since the speed of the GJ is much smaller than that of the AAV eavesdropper, the GJ is difficult to keep up with the AAV eavesdropper. To efficiently deploy GJs for enhancement of jamming performance, predicting the future location of the

AAV eavesdropper is a reasonable method. However, relying solely on the current location $q _ { e } [ t ]$ is difficult to predict the future location $q _ { e } [ t + 1 ]$ . Consequently, we take the part of the trajectory sequence of the AAV eavesdropper as a part of the observation o[t]. The trajectory sequence $w _ { e } [ t ]$ is defined by

$$
w _ { e } [ t ] = \left\{ q _ { e } [ t - Z + 1 ] , q _ { e } [ t - Z + 2 ] , \dots , q _ { e } [ t ] \right\} , \forall t .\tag{12}
$$

where Z denotes the maximum length of the trajectory sequence. Note that the length of the trajectory sequence is equal to t when the time step $t < Z$ . Then, the trajectory sequence of all AAV eavesdroppers can be represented as

$$
\mathcal { W } _ { n } \left[ t \right] = \left\{ w _ { e , 1 } \left[ t \right] , w _ { e , 2 } \left[ t \right] , \ldots , w _ { e , M } \left[ t \right] \right\} , \forall t\tag{13}
$$

Likewise, the locations of all users can be presented by

$$
\mathcal { X } _ { n } [ t ] = \{ q _ { u , 1 } [ t ] , q _ { u , 2 } [ t ] , . . . , q _ { u , K } [ t ] \} , \forall t\tag{14}
$$

The GJ n can easily obtain the jamming power $P _ { j , n } [ t ]$ emitted by itself. Then, the observation of GJ n at time step t can be expressed

$$
o _ { n } \left[ t \right] = \left\{ \mathcal { X } _ { n } \left[ t \right] , q _ { j , n } \left[ t \right] , q _ { b } , \mathcal { W } _ { n } \left[ t \right] , P _ { j , n } \left[ t \right] \right\} , \forall t\tag{15}
$$

Note that the observation of a GJ is different from observations of others since the private information, i.e., location ${ q _ { j , n } }$ and the jamming power $P _ { j , n } [ t ]$ are not shared. Then, the global state is constituted by the observations of all GJs, which can be expressed as

$$
\mathbf { s } \left[ t \right] = \left\{ o _ { 1 } \left[ t \right] , o _ { 2 } \left[ t \right] , \ldots , o _ { N } \left[ t \right] \right\} , \forall t\tag{16}
$$

2) Action: To effectively resist eavesdropping, the GJ needs to take action by dynamically adjusting its flight trajectory and jamming power. Therefore, the movement direction $\overrightarrow { v _ { j , n } } [ t ]$ and jamming power allocation $P _ { j , n } [ t ]$ are defined as the action of the GJ n at time step t. The action a of the GJ is denoted as

$$
a _ { n } \left[ t \right] = \{ \overrightarrow { v _ { j , n } } [ t ] , P _ { j , n } \left[ t \right] \} , \forall t\tag{17}
$$

3) Reward: In addition, to perform the contribution of each GJ from the overall secrecy capacity maximization problem (P1), in our solution, the reward function r includes a penalty item and a reward item. Specifically, the penalty item enhances the guidance of the reward function to the GJ actions while facilitating the convergence of the algorithm. Since the increase in instantaneous secrecy capacity can only indicate that $\zeta _ { b } - \zeta _ { e }$ is increasing, it does not guarantee the minimum transmission requirement for legitimate transmissions, i.e., $\zeta _ { b } > \zeta _ { t h }$ . Therefore, we set a penalty item $W _ { b }$ according to constraint (11d) to guarantee the legitimate transmission, which is represented as

$$
W _ { b } [ t ] = \left\{ { \begin{array} { l l } { \log { \{ 1 + \zeta _ { b } [ t ] \} } , } & { { \mathrm { i f } \quad \zeta _ { b } [ t ] \leq \zeta _ { t h } , } } \\ { 0 , } & { { \mathrm { o t h e r w i s e } , } } \end{array} } \right.\tag{18}
$$

Additionally, we set a penalty item $W _ { r }$ according to the constraint (11b) to rapidly respond to the next episode, which is represented as

$$
W _ { r } [ t ] = \left\{ { \begin{array} { l } { 0 , \mathrm { ~ i f ~ } r _ { 0 } \leq \| q _ { j , n } [ t ] \| _ { 2 } \leq r _ { t h } , } \\ { \varrho , \mathrm { ~ o t h e r w i s e } , } \end{array} } \right.\tag{19}
$$

where 	 is the penalty constant coefficient.

Furthermore, the reward item specifics the bonus of the action selection to maximize the secrecy capacity. As the intuitive feedback for the contribution of overall secrecy capacity maximization, we leverage the instantaneous secrecy capacity $C$ as a reward item. However, when the eavesdropping channel exhibits superior quality compared to the legitimate channel, the feedback of the instantaneous secrecy capacity becomes invalid (the value is always zero), i.e., if $\zeta _ { b } \leq \zeta _ { e } , C = 0$ . Consequently, the jammer is unable to obtain effective feedback on the contribution of its own policy Ï for (P1) from the instantaneous secrecy capability. Therefore, we reformulate (6) as

$$
C [ t ] = \log { ( 1 + \zeta _ { b } [ t ] ) } - \log { ( 1 + \zeta _ { e } [ t ] ) } ,\tag{20}
$$

Then, the reward function $r [ t ]$ can be intuitively represented by

$$
r [ t ] = \sum _ { k } ^ { K } C _ { k } [ t ] - \xi W _ { b } [ t ] - \delta W _ { r } [ t ] , \forall t\tag{21}
$$

where $\xi \in [ 0 , 1 ]$ and $\delta \in [ 0 , 1 ]$ are the penalty coefficients of $W _ { b }$ and $W _ { r }$ respectively. To prevent the algorithm converging to a local optimal solution, the initialization setting of the penalty coefficients cannot exceed 1. Excessive punishment may cause GJs to consistently choose prudent actions to avoid punishment, causing GJs to ignore the optimal policy $\pi ( a [ t ] | o [ t ] )$ based on the current observation o[t]. In conclusion, with such a reward function, the GJ can make a decision such that $\zeta _ { b } > \zeta _ { \epsilon }$ can get a reward to encourage the GJ to increase the instantaneous secrecy capacity. Besides, if the action causes $\zeta _ { b } < \zeta _ { t h }$ or exceeds the target region, an additional penalty will be incurred to reduce the probability of this policy occurring.

For the DRL solution, the goal of GJs is to maximize accumulative reward by improving its policy Ï, which is given as $\scriptstyle \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } r [ t ]$ . Thus, after being devised as a Dec-POMDP, (P1) can be further reformulated as

$$
( \mathrm { P 2 } ) : \operatorname* { m a x } _ { \{ q _ { j , n } [ t ] , P _ { j } \} } \sum _ { t } ^ { T } r [ t ] .
$$

Then, (P2) can be solved by applying the DRL algorithm. In Section IV-B, we first introduce a DRL-based algorithm in agent networks to solve the challenge of learning the optimal policy

for each GJ, and then in Section IV-C propose a mixing networkbased collaborative jamming solution to solve (P2).

## B. Dueling DDQN Algorithm

In this work, multiple AAV eavesdroppers and GJs cause problems of huge global state space S and action space A, which degrade the convergence of standard DQN. Fortunately, DQN with the dueling network (dueling DQN) can effectively solve such problems [28]. Dueling DQN incentivizes GJs to enhance their comprehension of the potential interrelations between jamming strategies, specific states, and secrecy capabilities. However, since both dueling DQN and standard DQN tend to choose the next action that maximizes the reward value, they suffer from overestimation bias. In intricate environments characterized by the presence of multiple collaborative jammers, overestimation bias becomes unavoidable and demands thorough attention. Currently, double Q-learning, which has been extensively employed, can alleviate the issue of overestimation bias. Consequently, the DQN algorithm with dueling network and double-Q learning (i.e., dueling DDQN) is applied in the agent network.

1) Dueling Network: The key feature of dueling DDQN is to split the action-value function in standard DQN into the value function and the advantage function [28]. In particular, the value function is to map the contribution of a specific observation $o _ { n } [ t ]$ to the optimization problem (P2). The advantage function is to map the contribution of each action a to the optimization problem (P2) in a specific observation $o _ { n } [ t ]$ . Then, combining the outputs of the value function and the advantage function, an estimate of the action-value function can be given. With the dueling network, the GJ can more efficiently learn the state value function. Especially, when the action-value gap between different actions of the same state is small, the action-value function derived from the dueling network demonstrates robustness to approximation errors.

In Fig. 3, we depict the dueling DDQN framework for the GJ. At each time step t, the observation $o _ { n }$ of the GJ n is set as an input to the network, and then the network outputs the action-value of all actions for the observation $o _ { n } .$ . Particularly, the hidden layer consists of the state value layer and the advantage layer. We utilize the state value layer and the advantage layer to estimate the value function $V ^ { \pi } ( o )$ and the advantage function $A ^ { \pi } ( o , a )$ , respectively. Then, the action-value function $Q ^ { \pi } { \bigl ( } o _ { n } , a _ { n } { \bigr ) }$ is obtained by a linear combination of the outputs of the state value function and the advantage function, which can be expressed as

$$
\begin{array} { r l } & { Q ( o _ { n } [ t ] , a _ { n } [ t ] ; \omega , \mu , \nu ) } \\ & { \quad = V \left( o _ { n } [ t ] ; \omega , \mu \right) + A \left( o _ { n } [ t ] , a _ { n } [ t + 1 ] ; \omega , \nu \right) , } \end{array}\tag{22}
$$

where $\omega$ denotes the parameter of the hidden layers, $\mu$ denotes the parameter of the state value layer, and Î½ is the parameter of the advantage layer. Note that the expected value of the advantage function $\mathbb { E } _ { a \sim \pi ( o ) } \{ A ^ { \pi } ( o _ { n } , a _ { n } ) \} = 0$ Since $Q ( o _ { n } , a _ { n } ; \omega , \mu , \nu )$ is a parametric approximation value of the action-value function, it is difficult for us to uniquely deduce the values of $V ( o _ { n } ; \omega , \mu )$ and $A ( o _ { n } , a _ { n } ; \omega , \nu )$ from $Q ( o _ { n } , a _ { n } ; \omega , \mu , \nu )$ . It means that the roles of $V ( o _ { n } ; \omega , \mu )$ and

```latex
Algorithm 1: Dueling DDQN for Ground Jamming Anti-
AAV Eavesdropping.
1: Initialize: the maximum number of episodes $N _ { e }$ , the
capacity of the replay buffer $\mathcal { R } _ { : }$ the number of replay
starts $N _ { 0 } ,$ the step size of the synchronization network
parameters $N _ { t a r } ,$ , set exploration $\epsilon = \epsilon _ { 0 } .$ , decaying rate $\alpha .$
2: Initialize: the reward function $^ { r , }$ the penalty coefficient
Î¾ and $\delta ,$ the threshold $\zeta _ { t h } , r _ { 0 }$ and $r _ { t h }$
3: Initialize: the Dueling network parameters $\omega$ and, the
target network parameters $\omega ^ { - } = \omega .$
4: for each episode $i = 1 , 2 , \ldots , N _ { e }$ do
5: Initialize the environmental information.
6: for each time step $t = 1 , 2 , \dots , T$ do
7: GJ n locally stores the location $q _ { e } [ t ]$ of the AAV
eavesdropper observed in one-step t;
8: if $t \geq Z$ then
9: Obtain the $\mathcal { W } _ { n }$ , and then obtain observation $o _ { n } [ t ] ;$
10: end if
11: Choose action $\overrightarrow { V _ { j } } [ t ]$ and $P _ { j , n } [ t ]$ . Specifically, for all
GJs, actions are taken randomly based on the
âgreedy policy starting from ${ \mathcal { A } } ,$ or following (25)
with probability $1 - \epsilon ;$
12: GJ n obtain reward r[t] by executing $a _ { n } [ t ] .$ , where
$\begin{array} { r } { r [ t ] = \sum _ { k = 1 } ^ { K } C _ { k } [ t ] - \bar { \xi } W _ { b } [ t ] - \delta W _ { r } [ t ] , \bar { t } \in T ; } \end{array}$
13: Update the environmental information, GJ n obtain
$o _ { n } [ t + 1 ] ;$
14: Store $\{ o _ { n } [ t ] , a _ { n } [ t ] , r _ { n } [ t ] , o _ { n } [ t + 1 ] \}$ to R;
15: if $n > N _ { 0 }$ then
16: Sample a batch of experience from $\mathcal { R } ;$
17: Update target Q-value by
$Y _ { t } ^ { \mathrm { [ { \hat { O } o u b l e Q } } } = { \stackrel { \smile } { r } } + \gamma { \hat { Q } } { ( o _ { n } [ t + \mathrm { \bar { 1 } } ] } , a _ { \mathrm { m a x } } { ( o _ { n } [ t + 1 ] } ; \omega { ) } ; \omega ^ { - } { ) }$
18: Update $\omega , \epsilon = ( 1 - \alpha ) \epsilon ;$
19: end if
20: if n mod $N _ { t a r } = = 0$ then
21: Update $\omega ^ { - } = \omega ;$
22: end if
23: end for
24: end for
```

$A ( o _ { n } , a _ { n } ; \omega , \nu )$ cannot be distinguished during the training process. To address the above challenge, we can centralize the advantage function. Therefore, the action-value function in dueling DDQN can be further represented by

$$
\begin{array} { l } { \displaystyle Q \left( o _ { n } [ t ] , a _ { n } [ t ] ; \omega , \mu , \nu \right) } \\ { \displaystyle = V \left( o _ { n } [ t ] ; \omega , \mu \right) + \Biggl ( A \left( o _ { n } [ t ] , a _ { n } [ t ] ; \omega , \nu \right) } \\ { \displaystyle \quad - \frac { 1 } { | A | } \sum _ { a [ t + 1 ] } A ( o _ { n } [ t ] , a _ { n } [ t + 1 ] ; \omega , \nu ) \Biggr ) . } \end{array}\tag{23}
$$

2) Double-Q Learning: The overestimation is caused by that the policy always chooses the action with the maximum target action-value, which can be solved by the double Q-learning. Specifically, the double-Q learning decouples the selection of actions for the target action-value and the estimation of the target action-value into two steps. Herein, we denote the target action-value as

$$
Y ^ { \mathrm { D o u b l e Q } } = r + \gamma \hat { Q } \left( o _ { n } [ t + 1 ] , a _ { \mathrm { m a x } } \big ( o _ { n } [ t + 1 ] ; \omega \big ) ; \omega ^ { - } \right) ,\tag{24}
$$

$$
a _ { \mathrm { m a x } } ( o _ { n } [ t + 1 ] ; \omega ) = \arg \operatorname* { m a x } _ { a _ { n } [ t + 1 ] } Q \left( o _ { n } [ t + 1 ] , a _ { n } [ t ] ; \omega \right) ,\tag{25}
$$

where $\hat { Q }$ is target action-value function, and $\gamma$ is the discount coefficient. In addition, $a _ { \mathrm { m a x } } ( o _ { n } [ t + 1 ] ; \omega )$ represents obtaining the action $a _ { n } [ t ]$ with the largest action-value in the current action-value function $Q ( o _ { n } [ t + 1 ] , a _ { n } [ t ] ; \omega )$ , i.e., the most valuable trajectory and jamming power strength of the GJ n in the next observation $o _ { n } [ t + 1 ]$ . Note that we use the dueling network $Q$ with coefficient Ï in (25) to select actions, while we employ the target dueling network $\hat { Q }$ with coefficient $\omega ^ { - }$ in (24) to evaluate the actions by the greedy method.

The proposed algorithm for ground Jamming anti-AAV eavesdropping with dueling DDQN is summarized in Algorithm 1. It is worth mentioning that we utilize the experience replay technique to enhance the train performance of the dueling DDQN. By using an experience replay buffer, the past experience and the current experience are mixed to reduce data correlation. Furthermore, experience replay enhances learning efficiency by making samples reusable. Due to the huge state space $\boldsymbol { s }$ in the environment, the initial value of the exploration coefficient  needs to be large enough for the GJ to abundantly and effectively explore the environment. Then, the GJ is possible to try more directions of movement and the strengths of the jamming power for the same observations $o _ { n }$ . With the accumulation of exploration experience, the GJ will relieve random exploration while focusing on learning. Therefore, it is necessary to initialize a suitable exploration decay coefficient Î±. Furthermore, as depicted in step 8 of Algorithm 1, the GJ can obtain the complete AAV trajectory $\mathcal { W } _ { n }$ when the time step $t \geq Z ,$ , so that predicting the future AAV trajectory. Thus, to ensure the effective prediction of AAV trajectory, the GJ will continue to observe the eavesdropping trajectory until it obtains the complete $\mathcal { W } _ { n }$

## C. Cooperative MARL: QMIX-Based Framework

As previously mentioned, each GJ moves and emits jamming signals only depending on its own local observations. Hence, the GJ disturbs eavesdroppers without information (e.g., without the observations and actions) exchange with others, resulting in low-efficiency jamming. Towards this end, we proposed a collaborative jamming scheme based on the QMIX-based collaborative MARL to further improve the collaborative jamming performance of GJs without information. We deploy a global action-value estimator to evaluate the contribution of the joint actions, preventing the GJ from greedily choosing an action based on its own independent action-value Q. The QMIX framework is used to efficiently deal with collaborative MARL in our collaborative jamming algorithm.

As depicted in Fig. 3, the cooperative intelligent jamming framework includes the mixing network and the agent network. Specifically, the mixing network acts as an estimator to evaluate the joint actions of GJs. The agent network consists of all GJs (regarded as agents) which was introduced in Section IV-B. We leverage the mixing network to aggregate all action-values from the agent network, obtaining the global action-value ${ \overline { { Q } } } .$ , which is given as

$$
{ \overline { { Q } } } = f ( Q ; \theta ) ,\tag{26}
$$

where Î¸ represents the parameter of the mixing network, and $f ( Q ; \theta )$ is used to approximate the mapping relationship between global action-value $\overline { { Q } }$ and the local action-value $Q$ of each GJ.

With the assistance of the mixing network, we can realize that the optimal joint action u is composed of the optimal local actions which are greedily selected by GJs according to their local observations. In particular, we need to ensure that the set composed of actions a obtained by arg max $Q$ is equivalent to the joint action u obtained by arg max ${ \overline { { Q } } } .$ i.e.,

$$
\begin{array} { r l } & { \arg \operatorname* { m a x } _ { a } \overline { { Q } } ( s , u ) } \\ & { \quad = \left( \begin{array} { c } { \arg \operatorname* { m a x } Q _ { 1 } ( o _ { 1 } , a _ { 1 } ) } \\ { \vdots } \\ { \arg \operatorname* { m a x } Q _ { N } ( o _ { N } , a _ { N } ) } \end{array} \right) , } \end{array}\tag{27}
$$

where $s = \{ o _ { 1 } , o _ { 2 } , . . . , o _ { N } \}$ is the global state, and $u =$ $\{ a _ { 1 } , a _ { 2 } , \dotsc , a _ { N } \}$ is the joint action. To satisfy (27), the global action-value $\overline { { Q } }$ need to monotonically increases with the local action-value $Q$ of each GJ, i.e.,

$$
\frac { \partial \overline { { Q } } } { \partial Q _ { n } } \geq 0 , \forall n\tag{28}
$$

As shown in Fig. 3, the parameters of the mixing network $\theta = \{ w _ { 1 } , w _ { 2 } , b _ { 1 } , b _ { 2 } \}$ are determined by hypernetworks $\mathbf { W _ { 1 } } ( s )$ $\mathbf { W _ { 2 } } ( s ) , \mathbf { b _ { 1 } } ( s )$ , and $\mathbf { b _ { 2 } } ( s )$ . In addition, the hypernetwork W mainly includes a linear and an absolute activation function to generate non-negative weights w, $w \geq 0$ , to ensure the monotonicity (28). The hypernetwork b is similar to the hypernetwork W but necessitates no absolute activation function. Then, to improve the nonlinearity of the mixing network, we introduce the activation function ReLU between $\mathbf { b _ { 1 } } ( s )$ and $\mathbf { W _ { 2 } } ( s )$

Finally, we denote the loss function as follows

$$
\boldsymbol { l } ( \boldsymbol { \theta } ) = \sum _ { i = 1 } ^ { B } \left( \hat { Y _ { i } } - \overline { { Q } } \left( \boldsymbol { s } [ t ] , \boldsymbol { u } [ t ] ; \boldsymbol { \theta } \right) \right) ^ { 2 } ,\tag{29}
$$

where B denotes the number of samples randomly in a batch training, and $\hat { Y _ { i } }$ is the target action-value for the mixing network, which can be represented as

$$
\hat { Y _ { i } } = r [ t ] + \gamma \operatorname* { m a x } _ { a [ t + 1 ] } \overline { { Q } } \left( s [ t + 1 ] , u [ t + 1 ] ; \theta ^ { - } \right) ,\tag{30}
$$

The QMIX-based collaborative jamming algorithm is given by Algorithm 2. In particular, for updating the parameter Î¸ of the mixing network, s[t] and u[t] are also stored in the replay buffer R, in step 4. The update dueling network parameter Ï is also performed by the loss function in step 8. Note that in the environment of multi-GJs, we set the initial location of each GJ to be at a certain distance from each other, and decentralized initial locations allow GJs to learn cooperative interference faster and improve secrecy capacity.

Algorithm 2: QMIX-based Collaborative Jamming Algo  
rithm.   
1: Initialize: Step 1â5 of Algorithm 1;   
2: Initialize the AAV eavesdroppersâ flight path   
$\{ q _ { e , 1 } , q _ { e , 2 } , \ldots , q _ { e , M } \} ;$   
3: Steps 7-14 of Algorithm 1;   
4: Then the global state $s [ t ] = \{ o _ { 1 } [ t ] , o _ { 2 } [ t ] , \ldots , o _ { N } [ t ] \}$ , the   
joint action $u [ t ] = \{ a _ { 1 } \hat { [ } t \hat { ] } , a _ { 2 } \hat { [ } t ] , \hat { . . . } , a _ { N } \hat { [ } t ] \}$   
5: Store $\{ s [ t ] , u [ t ] , \{ r _ { 1 } [ t ] , r _ { 2 } [ t ] , \dots , r _ { N } [ t ] \} , s [ t + 1 ] \}$ to $\mathcal { R } ;$   
6: Steps 16â19 of Algorithm 1;   
7: Update the target action-value of the critic network   
mixing network by   
$\begin{array} { r } { \hat { Y _ { i } } = \overline { { r [ t ] } } + \gamma \operatorname* { m a x } _ { a [ t + 1 ] } \overline { { Q } } ( s [ t + 1 ] , u [ t + 1 ] ; \theta ^ { - } ) . } \end{array}$   
8: Update the parameter Ï of each agent network, and   
update the parameter Î¸ of the mixing network. Then, the   
loss function is given by   
$l ( \theta ) = \sum _ { i = 1 } ^ { B } ( \hat { Y _ { i } } - \overline { { Q } } ( s [ t ] , u [ t ] ; \theta ) ) ^ { 2 } ,$   
9: Step 20 of Algorithm 1;   
10: if t mod $N _ { t a r } = = 0$ then   
11: Synchronize the parameters $\theta ^ { - } = \theta$ of the critic target   
network   
12: For each GJ, update $\omega ^ { - } = \omega ;$   
13: end if   
14: Steps 24â26 of Algorithm 1.

## D. Analysis of Algorithm Complexity

In this subsection, we analyze the computational complexity of the QMIX-based collaborative jamming algorithm in terms of the training and execution phases.

Complexity analysis in training phase: For the agent network, each GJ is equipped with a dueling network. The computational complexity of the dueling network mainly includes the complexity of forward-propagation and back-propagation. The complexity of forward-propagation depends on the structure of the neural network. Assuming the network has $L$ layers and the i layer has $\iota _ { i }$ neurons, the complexity of forward-propagation is $O ( \stackrel { \cdot  } { \sum } { } _ { i = 1 } ^ { L + 1 } \iota _ { i } \cdot \iota _ { i - 1 } )$ . Back-propagation involves computing gradients and updating network weights. Its complexity is similar to forward-propagation, which is also $O ( \sum _ { i = 1 } ^ { L + \bar { 1 } } \iota _ { i } \cdot \bar { \iota _ { i - 1 } } )$ . Then, the complexity of experience replay mainly depends on the process of sampling from the replay buffer, which is usually $O ( 1 )$ since the sampling is typically random. For each agent, it is necessary to update the parameters of two neural networks: the primary network and the target network. The complexity of each update is $O ( \sum _ { i = 1 } ^ { L + 1 } \iota _ { i } \cdot \iota _ { i - 1 } \big )$

Additionally, since actions of all GJs are aggregated into a global action-value, the collaborative jamming algorithm uses a mixing network to achieve this aggregation. For mixing network, assuming the mixing network has D layers and the $j$ layer has $\varpi _ { i }$ neurons, the complexity of forward and back-propagation is

$O ( \sum _ { i = 1 } ^ { D + 1 } \varpi _ { i } \cdot \varpi _ { i - 1 } )$ . Therefore, the overall complexity of the training phase is $O ( N \cdot ( \textstyle \sum _ { i = 1 } ^ { L + 1 } \iota _ { i } \cdot \iota _ { i - 1 } + \textstyle \sum _ { j = 1 } ^ { D + 1 } \varpi _ { i } \cdot \varpi _ { j - 1 } ) )$ where N is number of GJs.

Complexity analysis in the execution phase: The complexity of the execution phase mainly considers the computational cost of forward propagation, as no parameter updates occur during execution. The overall complexity of the execution phase is $\begin{array} { r } { O ( N \cdot \sum _ { i = 1 } ^ { L + 1 } \iota _ { i } \cdot \iota _ { i - 1 } + \sum _ { j = 1 } ^ { \bar { D } + 1 } \varpi _ { i } \cdot \varpi _ { j - 1 } ) } \end{array}$

## V. SIMULATION RESULTS

In this section, we evaluate the superiority of our cooperative intelligent jamming scheme through comparison with existing benchmarks. Furthermore, we investigate the effects of parameters on security performance in accordance with the number of GJs, mobility speed, and penalty coefficient.

## A. Simulation Settings

In the simulation, we concentrate on an area of $1 0 0 \mathrm { m } \times 1 0 0 \mathrm { m }$ where a single BS is fixed at $q _ { b } = \{ 5 0 \mathrm { m } , 5 0 \mathrm { m } \}$ . Users randomly appear in the network area. Note that the number of users is randomly chosen from 6 to 9. AAV eavesdroppers wiretap legitimate transmissions at the flight altitude $H = 5 0$ m with speed $V _ { e } = 1 0 \mathrm { m / s }$ . For GJs, the maximum jamming power is $P _ { \mathrm { m a x } } = 2 5 \ : \mathrm { m W }$ , the maximum movement range is $r _ { \operatorname* { m a x } } =$ 45 m and the minimum movement range is $r _ { \mathrm { m i n } } = 5 \mathrm { m }$ , respectively. It is worth mentioning that the specific parameters of AAV networks, such as flight speed and flight altitude of the AAV, are set referring to the 3rd Generation Partnership Project (3GPP) [37]. For the sake of illustration, we set the movement direction of GJ n as four types: up, down, left, and right.

For the proposed QMIX-based collaborative jamming algorithm, the agent network consists of 3 hidden layers, each of which uses a ReLU activation function. The first 2 hidden layers have 128 and 128 neurons, respectively. The last hidden layer is a dueling layer with |A| + 1 neurons (|A| denotes the number of actions), where one neuron corresponds to the estimation of the state value and the other $| { \cal { A } } |$ neurons correspond to the action advantage of the $| { \cal { A } } |$ actions. Additionally, the mixing network consists of 4 hypernetworks, as introduced in Section IV. Each hypernetwork consists of 2 fully connected layers and a ReLU activation function. Furthermore, the simulations are performed with Python 3.8 and PyTorch 1.11 under the PyCharm platform. All experiments are implemented on a computer equipped with Intel Core i7-1165G7 2.80GHz. Note that the simulation results are processed with the policy network trained and converged after 5000 episodes. Unless specified otherwise, the values for all other key simulation parameters [38] are provided in Table II.

## B. Analysis of Algorithm Effectiveness and Convergence

Herein, we verify the effectiveness of the proposed collaborative jamming algorithm and cooperative intelligent jamming scheme. First, we exhibit the effectiveness of the proposed algorithm for joint trajectory and jamming power optimization. Then, the effectiveness and convergence of the proposed algorithm are evaluated. Finally, the performance between different schemes as well as interference trajectories are compared.

TABLE II MARL-RELATED PARAMETERS
<table><tr><td rowspan=1 colspan=1>Simulationparameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Maximum episodes $N _ { e }$ </td><td rowspan=1 colspan=1>5000</td></tr><tr><td rowspan=1 colspan=1>Initialize exploration e</td><td rowspan=1 colspan=1>0.9</td></tr><tr><td rowspan=1 colspan=1>Exploration decay rate Î±</td><td rowspan=1 colspan=1>0.9998</td></tr><tr><td rowspan=1 colspan=1>Batch size</td><td rowspan=1 colspan=1>32</td></tr><tr><td rowspan=1 colspan=1>Batch learning frequency</td><td rowspan=1 colspan=1>200</td></tr><tr><td rowspan=1 colspan=1>penalty coefficient </td><td rowspan=1 colspan=1>0.7</td></tr><tr><td rowspan=1 colspan=1>penalty coefficient Î´</td><td rowspan=1 colspan=1>0.6</td></tr><tr><td rowspan=1 colspan=1>Learning rate (agent network)</td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 4 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Learning rate (mixing network)</td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 4 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Replay buffer capacity R</td><td rowspan=1 colspan=1>2000</td></tr><tr><td rowspan=1 colspan=1>Trajectory sequence size Z</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>Jamming power set</td><td rowspan=1 colspan=1> $\overline { { [ 0 , 1 , 2 , . . . , P _ { \mathrm { m a x } } ] } }$ </td></tr><tr><td rowspan=1 colspan=1>Update frequency for target network $N _ { t a r }$ </td><td rowspan=1 colspan=1>200</td></tr><tr><td rowspan=1 colspan=1>Hypernetwork(Number of hidden layer neurons)</td><td rowspan=1 colspan=1>[128,128]</td></tr></table>

Fig. 4 shows QMIX-based collaborative jamming against different eavesdropping trajectories. Fig. 4(a) to (d) illustrate different eavesdropping scenarios. Specifically, as shown in Fig. 4(a1) and (b1), when eavesdropping trajectories overlap with usersâ location, to degrade interference to legitimate transmissions, GJs are usually preferentially moved away from users. Then, as AAV eavesdroppers approach users, GJs move as close as possible to the eavesdropper while maintaining a distance from users. In Fig. 4(c1), even if the eavesdropping trajectory is close to users, the jamming trajectory still maintains a certain distance from users to avoid undesirable interference. It can be seen from Fig. 4(d1) that when eavesdropping trajectories are far away from users, the jammer is positioned between eavesdroppers and users to efficiently interfere with eavesdropping. Hence, the optimal jamming trajectory is always close to the eavesdropper and far from the BS, subject to safeguarding the quality of legitimate transmissions. When multiple GJs collaborate to design jamming trajectories, the GJ decides its jamming trajectories based on the observation. Taking Fig. 4(b1) as an example, the initial locations of $\mathrm { G J _ { 1 } }$ and $\mathrm { G J _ { 3 } }$ are near the eavesdroppers. However, when $\mathrm { G J _ { 1 } }$ approaches the eavesdropper, $\mathrm { G J _ { 3 } }$ moves toward the future possible eavesdropping location of the eavesdropper. Furthermore, we can observe that, from Fig. 4(a1) to (d1), the jamming trajectories do not overlap with each other, verifying the effectiveness of our collaborative jamming algorithm.

Furthermore, we can see from Fig. 4(a2), the $\mathrm { G J _ { 1 } }$ and $\mathrm { G J _ { 3 } }$ gradually increase the jamming power as its location moves away from the user and close to the AAV eavesdropper (depicted in Fig. 4(a1)). Then, as the AAV eavesdropper moves away from the GJs, the jamming power of jammer $\mathrm { G J _ { 2 } }$ and jammer $\mathrm { G J _ { 3 } }$ decreases by 0 to avoid the effect on the users. However, due to the proximity of the $\mathrm { G J _ { 1 } }$ and $\mathrm { G J _ { 4 } }$ to the AAV eavesdroppers after time step 30, the jamming is maintained at a high power. Therefore, when the GJ is in proximity to the user, it consistently reduces jamming power to maintain the quality of legitimate

<!-- image-->

<!-- image-->  
(a) Eavesdropping trajectories overlap with users' locations,while GJs are near the initial location of the eavesdroppers.

<!-- image-->

<!-- image-->  
(b) Eavesdropping trajectories overlap with users' locations,but GJs are far away from the initial location of eavesdroppers.

<!-- image-->

<!-- image-->

$$
{ \mathrm { G J } } _ { 2 }
$$

$$
\mathrm { G J } _ { 4 }
$$

transmissions, otherwise, the jamming power is increased. The same variation can also be observed in Fig. 4(b2) to (d2). Additionally, the GJs collaboratively adjust their own jamming power according to the location of other jammers. Particularly, when GJs are in proximity to the same AAV eavesdropper (in Fig. 4(b1) and (b2)), the main jamming power is emitted by the GJ which is close to the AAV eavesdropper by the collaborative jamming algorithm. Then, the jamming power is decreased, when the AAV eavesdroppers are positioned on both sides of the users and close to the users (as shown in Fig. 4(c1) and (c2)). Meanwhile, the jamming power is increased, when the AAV eavesdroppers are positioned on both sides of the users and far away from the users (as shown in Fig. 4(d1) and (d2)).

Fig. 4. QMIX-based collaborative jamming trajectories and jamming power.

$$
{ \mathrm { G J } } _ { 3 }
$$

To verify the effectiveness of our proposed QMIX-based collaborative jamming algorithm (using QMIX framework with Dueling DDQN), we compared it with the other five benchmarks.

1) QMIX-dueling DQN: QMIX framework with the dueling network.

2) QMIX-DDQN: QMIX framework with double Q learning.

3) QMIX-DQN: QMIX framework with standard DQN.

5) Theoretical Optimization: Alternating optimization algorithm with known system information (eavesdropping trajectories, channel parameters, etc.).

4) VDNs: MARL algorithm based on VDNs.

$$
{ \mathrm { G J } } _ { 3 }
$$

<!-- image-->  
Fig. 5. Comparison of cumulative rewards among different algorithms over 5000 training episodes.

Fig. 5 compares accumulative rewards for different algorithms in 5000 training episodes. It is observed that all algorithms gradually converge after 2000 episodes. Compared to other MARL algorithms, our proposed algorithm has stable convergence. It means that the agent network with the dueling network has dominated superiority in the huge state space and action space for preventing multiple AAV eavesdropping. Then, the proposed algorithm obtains a higher accumulative reward compared to other algorithms, including non-information sharing MARL (i.e., VDNs). This shows that our proposed algorithm based on the QMIX framework is reasonable and effective. Moreover, it is evident that the proposed algorithm closely approximates the theoretical optimization. To summarize, the proposed QMIX-Dueling DDQN algorithm enables GJs to collaboratively interfere with eavesdropping by making the optimal decision without sharing their local observations.

<!-- image-->  
Fig. 6. Comparison of instantaneous secrecy capacity among different schemes.

Fig. 6 illustrates the variation of instantaneous secrecy capacity for different schemes in an episode. We compare our cooperative intelligent jamming scheme (denoted as proposed CIJ in Fig. 6) with the fixed location scheme, the fixed jamming power scheme and the no jammer scheme. Specifically, in the fixed location scheme, GJs can only change the strength of jamming power to disturb eavesdropping. Meanwhile, in the fixed jamming power scheme, GJs can change their positions to interfere with eavesdropping with a fixed jamming power. The no jammer scheme means that there are no jamming protection measures. It is noteworthy that GJs in the aforementioned schemes are driven by our proposed MARL algorithm. Since GJs are initiated at the same location, the instantaneous secrecy capacities of the three jamming schemes using GJ are the same when t = 0. Compared to the proposed scheme, the instantaneous secrecy capacity at the fixed location scheme drops significantly after time step 40. This decrease is caused by the fixed GJâs lack of mobility, and the AAV moves away from the GJ resulting in diminishing the jamming effect. Moreover, compared to the no jammer scheme, the other schemes can be effective against AAV eavesdropping. Furthermore, results also reveal that the proposed cooperative intelligent jamming scheme outperforms other jamming schemes, achieving higher instantaneous secrecy capacity. This superiority is attributed to the joint optimization of trajectory and jamming power, providing GJs with increased flexibility to adapt to complex locations and dynamic networks.

Fig. 7 demonstrates the variation of trajectories for different schemes. In the CIJ scheme, GJs can compensate for the lack of speed problem by dynamically adjusting the jamming power. In the fixed jamming power scheme, the speed resources of the GJs with higher jamming power are wasted away from the users, and GJs with lower jamming power consume the speed resources close to the eavesdropper. However, due to the limited speed resource $( V _ { j } < V _ { e } )$ , the CIJ scheme outperforms the other schemes.

<!-- image-->  
Fig. 7. Comparison of jamming trajectories among different schemes.

## C. Performance Analysis With Various Settings

Then, we evaluate the performance of the proposed collaborative jamming algorithm with different learning rates. The learning rate of the agent network is set to three values, $\mathrm { i } . \mathrm { e } . , 1 0 ^ { - 3 }$ (denoted as the red line), $1 0 ^ { - 4 }$ (denoted as the blue line), and $1 0 ^ { - 5 }$ (denoted as the green line) in Fig. 8(a). We can see that the red line initially exhibits a higher reward than the others. However, with the increasing number of episodes, the blue line rapidly surpasses the red line and converges after approximately 3000 episodes. The reason is that a large learning rate (e.g., the learning rate $= 1 0 ^ { - 3 } )$ can induce significant fluctuations in the training model, rendering it difficult to find the optimal policy. Additionally, a small learning rate $( \mathrm { e . g . }$ , the learning rate $= 1 0 ^ { - 5 } )$ can result in excessively long training times for the model. Therefore, a reasonable learning rate is necessary for the practical implementation of our proposed algorithm, i.e., the learning rate is set to $1 0 ^ { - 4 }$

To assess the impact of varying numbers of neurons in the agent network on the algorithmâs performance. We set the number of neurons in the hidden layer with (64, 64), (128, 128) and (256, 256), respectively. In Fig. 8(b), a large number of neurons (ranging from (64, 64) to (128, 128)) results in higher rewards and faster convergence. However, configuring an excessive number of neurons (e.g., (256, 256)) results in diminished rewards. This is because the potential overfitting of the neural network and the accompanying increase in the computational cost of training can result in a deterioration of the reward. Consequently, selecting a reasonable number of neurons in the agent network is essential for the proposed algorithm, i.e., the number of neurons is set as (128, 128).

<!-- image-->  
(a) Algorithm performance under diferent learning rates.

<!-- image-->  
(b)Algorithm performance under different number of neurons.

<!-- image-->  
(cï¼ Algorithm performance under different batch sizes.  
Fig. 8. Algorithm performance analysis with various settings.

Furthermore, we analyze the performance of the proposed algorithm with different batch sizes. As shown in Fig. 8(c) , a small batch size (i.e., batch size = 16) fails to learn all of the training data, resulting in the smallest accumulated reward for convergence. A large batch size (i.e., batch size = 64) results in repeatedly learning the training data. Additionally, a large batch size can consume more computing capability and increase the training time. Then, a trade-off between convergence speed and training time is significant. As a consequence, the training batch size is set to 32 in the simulation.

<!-- image-->  
Fig. 9. Comparison of different GJ speeds on the instantaneous secrecy capacity.

Fig. 9 plots the instantaneous secrecy capacity of our proposed scheme in different GJ speeds. The blue, red, and green lines represent GJ speeds of $V _ { j } = V _ { e } , V _ { j } = V _ { e } / 5$ and $V _ { j } = V _ { e } / 1 0 $ respectively. It is observed that an increased GJ speed can result in a high instantaneous secrecy capacity. The reason is that the increased speed enables GJs to rapidly move to a reasonable location to disturb eavesdroppers. Moreover, in Fig. 9, despite the secrecy capacities of the red and green lines being lower than that of the blue line at each time step, there is little difference among these secrecy capacities. This result demonstrates the effectiveness of our proposed algorithm in preventing AAV eavesdropping, even when the speed of the GJ is lower than that of the AAV eavesdropper.

In Fig. 10, the overall secrecy capacity of our collaborative jamming algorithm is depicted, concerning the number of AAV eavesdroppers versus the number of GJs. Note that the dueling DDQN algorithm is employed when the number of GJs is $N = 1$ . We observe that the secrecy capacity diminishes progressively with the rise in the number of AAV eavesdroppers. In Fig. 10, increasing the number of GJs effectively enhances jamming performance against eavesdropping. Moreover, when the number of GJ is less than the number of eavesdroppers, GJs can still provide a certain level of overall secrecy capacity. However, it is noticeable that the line for N = 4 exhibits the slowest decline trend as the number of eavesdroppers increases. This is because more GJs can rapidly respond to jamming deployment, enabling effective interference with AAV eavesdroppers.

Then, the impact of the penalty coefficient Î¾ for the penalty item $W _ { b }$ on the overall secrecy capability and the quality of legitimate transmissions is analyzed in Fig. 11. We set the number of GJs to $N = 2$ , the number of AAV eavesdropping to $M = 2$ , and $\zeta _ { t h } = 0$ dBm. As shown in Fig. 11(a), we illustrate the overall secrecy capability with different penalty coefficients Î¾. Then, we can find that as the penalty coefficient gradually increases, the overall secrecy capacity continuously decreases. Additionally, to investigate the effect on the quality of legitimate transmissions, we introduce legitimate connectivity which is defined as the probability that $\zeta _ { b } [ t ] > \zeta _ { t h }$ . As illustrated in Fig. 11(b), the legitimate connectivity increases, with the increase in the penalty coefficient. When $\xi = 1$ , the penalty item $W _ { b }$ can elevate the legitimate connectivity of the cooperative intelligent jamming scheme to a maximum value of 99.6%. Meanwhile, $\xi = 0$ indicates that the reward function is not required to guarantee the legitimate connectivity, thus, GJs can obtain a large secrecy capacity as a reward. Hence, the setting of the penalty coefficient should trade-off the legitimate connectivity and the secrecy capacity.

<!-- image-->  
Fig. 10. Overall secrecy capacity versus the number of AAV eavesdroppers for different numbers of GJs.

<!-- image-->  
(a) Penalty coeficient versus overall secrecy capacity.

<!-- image-->  
(b) Penalty coefficient versus legitimate connectivity.

Fig. 11. Comparison of the penalty coefficient $\xi .$  
<!-- image-->  
Fig. 12. Comparison of the penalty coefficient Î´.

Finally, in Fig. 12, we analyze the overall secrecy capability with different penalty coefficients Î´ for the penalty item $W _ { r }$ . We set the number of GJs as $N = 2$ , the number of AAV eavesdroppers as $M = 2 , r _ { \mathrm { m i n } } = 5$ m, and $r _ { \operatorname* { m a x } } = 4 5$ m. From Fig. 12, we can observe that as the penalty coefficient Î´ gradually increases, the overall secrecy capability is first improved and then stabilized. In particular, in the absence of the penalty item $W _ { r }$ $( \mathrm { i . e . }$ , the penalty coefficient $\delta = 0 )$ , the overall secrecy capacity is significantly lower than that in the presence of the penalty item $W _ { r }$ . This is because, over multiple training episodes, the penalty item $W _ { r }$ ensures that the GJ never moves away from the protection region (i.e., the service region of the base station). Therefore, the GJ can timely respond to the next eavesdropping attack. This result shows that the penalty item $W _ { r }$ is essential in enhancing the overall secrecy capacity in the reward function.

## VI. DISCUSSION AND FUTURE WORK

In this section, we discuss the potential challenges of the implementation of our cooperative jamming scheme. Moreover, we deliberate future work with promising techniques to further enhance the performance of cooperative intelligent jamming.

## A. Discussion on the Implementation of GJs

In the current study, we have analyzed that our collaborative jamming scheme can be used to prevent wiretapping from AAV eavesdroppers. Besides, with the QMIX-based collaborative jamming algorithm, the effectiveness of collaboration among multiple GJs can be further enhanced. Despite the advantages, we are aware of some challenges of multi-ground jamming collaboration in real-world deployments. In this subsection, we discuss these potential challenges as follows.

Hardware constraints: The ground jammer, as an extra device, faces limitations in both energy and computing capability. Particularly, insufficient energy makes the GJ unable to achieve the optimal jamming power and movement speed, degrading the collaborative effectiveness of jamming. Inaccurate execution impacts the controllability of the policy network, as the actions output by the network are not aligned with the actions that the GJ performs. Moreover, limited computing capability prolongs both the training time and decision-making process, reducing algorithm stability and compromising the real-time effectiveness of jamming.

Environmental factors: The deployment terrains can influent the performance of our cooperative jamming scheme. For example, some complex terrains, including steep slopes and obstructions, can impede the movement speed of GJs and alter the angle of their jamming emissions. Additionally, obstacles such as buildings and trees can significantly attenuate the jamming signal and disrupt the jamming trajectory, causing a lack of stability in the jamming performance.

Scalability: To adapt the diverse deployment scenarios, the deployed number of GJs is varied with the task requirement (e.g., the number of eavesdroppers). The training time for newly integrated GJs can hinder the effectiveness of collaboration among existing GJs, thereby diminishing overall secrecy capacity. Additionally, the interdependence of GJ policies often results in convergence to a local optimum, particularly as the number of GJs increases. Furthermore, the complexity of finding a globally optimal policy also rises, thereby reducing algorithmic convergence.

## B. Discussion on Future Work

As a promising technology, the cooperative intelligent jamming scheme provides secure data transmission in the presence of AAV eavesdroppers. To promote the implementation of this scheme, several future research directions are outlined as follows.

Tradeoff between energy consumption and jamming efficiency: The jamming efficiency of GJs is extremely determined by energy resources. Investigating the tradeoff between energy consumption and jamming efficiency is an essential problem for the implementation of our scheme. The goal is to make GJs maintain high jamming effectiveness while degrading energy consumption (i.e., ensuring performance under constrained power resources). Through various energy allocation strategies generated by techniques like generative artificial intelligence algorithms, the optimal balance between jamming efficiency and energy consumption can be identified.

Multimodal data-driven collaborative jamming: For practical deployment, complex environments hinder the performance of cooperative jamming. Therefore, multimodal data (including position and terrestrial data) is significant for collaborative jamming strategy. By collecting and analyzing data from multiple sensors, GJs make more informed and coordinated decisions in response to complex environments. For example, we can model complex environments, including building complexes and irregular terrain, by incorporating additional sensors to capture and process diverse types of environmental data. The modeled environment data refines the collaborative jamming strategy, enhancing its adaptability and effectiveness in challenging real-world implementation.

- Game between jamming and eavesdropping: With advancements in artificial intelligence, future eavesdroppers are foreseen to be intelligent, resulting in unpredictable eavesdropping trajectories. The AAV eavesdropper dynamically adjusts its trajectory by observing GJs, including the distribution of GJs, jamming trajectory, and jamming power. To counter intelligent eavesdroppers, the study of games between eavesdroppers and GJs is critical. By leveraging game theory, the current collaborative jamming algorithm can be further optimized, empowering GJs to effectively counter the sophisticated strategies employed by AAV eavesdroppers.

## VII. CONCLUSION

In this paper, we proposed a cooperative intelligent jamming scheme to prevent AAV eavesdropping. We formulate an overall secrecy capability maximization problem with the constrained mobility of GJs. Then, we proposed a QMIX-based collaborative jamming algorithm with dueling DDQN for GJs to independently make decisions without sharing observations. The proposed scheme efficiently realizes the jamming trajectory design and jamming power allocation among multiple GJs, as indicated by the simulation results. Furthermore, the convergence of our proposed collaborative jamming algorithm for multiple ground jammers outperforms other benchmarks. Then, the designed penalty item effectively mitigates the interference of ground jammers on legitimate transmissions, while ensuring the secrecy capability. Moreover, the overall secrecy capability can be effectively guaranteed even if the movement speeds of GJs and AAV eavesdroppers are extremely uneven.

## REFERENCES

[1] B. Alzahrani, O. S. Oubbati, A. Barnawi, M. Atiquzzaman, and D. Alghazzawi, âUAV assistance paradigm: State-of-the-art in applications and challenges,â J. Netw. Comput. Appl., vol. 166, 2020, Art. no. 102706.

[2] S. Chai and V. K. N. Lau, âMulti-UAV trajectory and power optimization for cached UAV wireless networks with energy and content rechargingdemand driven deep learning approach,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3208â3224, 2021.

[3] L. Wang, H. Zhang, S. Guo, and D. Yuan, âDeployment and association of multiple UAVs in UAV-Assisted cellular networks with the knowledge of statistical user position,â IEEE Trans. Wireless Commun., vol. 21, no. 8, pp. 6553â6567, Aug. 2022.

[4] V.-L. Nguyen, P.-C. Lin, B.-C. Cheng, R.-H. Hwang, and Y.-D. Lin, âSecurity and privacy for 6G: A survey on prospective technologies and challenges,â IEEE Commun. Surv. Tut., vol. 23, no. 4, pp. 2384â2428, Fourth Quarter, 2021.

[5] H. Wu, M. Li, Q. Gao, Z. Wei, N. Zhang, and X. Tao, âEavesdropping and anti-eavesdropping game in UAV wiretap system: A differential game approach,â IEEE Trans. Wireless Commun., vol. 21, no. 11, pp. 9906â9920, Nov. 2022.

[6] H. V. Poor and R. F. Schaefer, âWireless physical layer security,â in Proc. Nat. Acad. Sci., vol. 114, no. 1, pp. 19â26, 2017.

[7] Y. Zhou et al., âSecure communications for UAV-Enabled mobile edge computing systems,â IEEE Trans. Commun., vol. 68, no. 1, pp. 376â388, Jan. 2020.

[8] W. Lu et al., âSecure NOMA-Based UAV-MEC network towards a flying eavesdropper,â IEEE Trans. Commun., vol. 70, no. 5, pp. 3364â3376, May 2022.

[9] B. Li, Y. Zou, J. Zhou, F. Wang, W. Cao, and Y.-D. Yao, âSecrecy outage probability analysis of friendly jammer selection aided multiuser scheduling for wireless networks,â IEEE Trans. Commun., vol. 67, no. 5, pp. 3482â3495, May 2019.

[10] Q. Wang, Y. Liu, H. Dai, M. Imran, and N. Nasser, âEar in the sky: Terrestrial mobile jamming to prevent aerial eavesdropping,â in Proc. 2021 IEEE Glob. Commun. Conf., 2021, pp. 01â06.

[11] Y. Zeng, X. Xu, S. Jin, and R. Zhang, âSimultaneous navigation and radio mapping for cellular-connected UAV with deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 20, no. 7, pp. 4205â4220, Jul. 2021.

[12] J. Chen, H. Xing, Z. Xiao, L. Xu, and T. Tao, âA DRL agent for jointly optimizing computation offloading and resource allocation in MEC,â IEEE Internet Things J., vol. 8, no. 24, pp. 17508â17524, Dec. 2021.

[13] K. Zhang, Z. Yang, and T. BaÂ¸sar, âMulti-agent reinforcement learning: A selective overview of theories and algorithms,â in Handbook of Reinforcement learning and Control. Berlin, Germany: Springer, 2021, pp. 321â384.

[14] H. Dang-Ngoc et al., âSecure swarm UAV-Assisted communications with cooperative friendly jamming,â IEEE Internet Things J., vol. 9, no. 24, pp. 25596â25611, Dec. 2022.

[15] Y. Zhou et al., âCaching and UAV friendly jamming for secure communications with active eavesdropping attacks,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 11251â11256, Oct. 2022.

[16] W. Lu et al., âResource and trajectory optimization for secure communications in dual unmanned aerial vehicle mobile edge computing systems,â IEEE Trans. Ind. Inform., vol. 18, no. 4, pp. 2704â2713, Apr. 2022.

[17] R. Jin, K. Zeng, and K. Zhang, âA reassessment on friendly jamming efficiency,â IEEE Trans. Mobile Comput., vol. 20, no. 1, pp. 32â47, Jan. 2021.

[18] A. S. Abdalla, A. Behfarnia, and V. Marojevic, âUAV trajectory and multi-user beamforming optimization for clustered users against passive eavesdropping attacks with unknown CSI,â IEEE Trans. Veh. Technol., vol. 72, no. 11, pp. 14426â14442, Nov. 2023.

[19] H. Yang, Z. Xiong, J. Zhao, D. Niyato, L. Xiao, and Q. Wu, âDeep reinforcement learning-based intelligent reflecting surface for secure wireless communications,â IEEE Trans. Wireless Commun., vol. 20, no. 1, pp. 375â388, Jan. 2021.

[20] X. Tang, H. He, L. Dong, L. Li, Q. Du, and Z. Han, âRobust secrecy via aerial reflection and jamming: Joint optimization of deployment and transmission,â IEEE Internet Things J., vol. 10, no. 14, pp. 12562â12576, Jul. 2023.

[21] E. T. Michailidis, M.-G. Volakaki, N. I. Miridakis, and D. Vouyioukas, âOptimization of secure computation efficiency in UAV-Enabled RIS-Assisted MEC-IoT networks with aerial and ground eavesdroppers,â IEEE Trans. Commun., vol. 72, no. 7, pp. 3994â4009, Jul. 2024.

[22] N. Gao, Z. Qin, X. Jing, Q. Ni, and S. Jin, âAnti-intelligent UAV jamming strategy via deep Q-networks,â IEEE Trans. Commun., vol. 68, no. 1, pp. 569â581, Jan. 2020.

[23] L. Xiao, H. Li, S. Yu, Y. Zhang, L.-C. Wang, and S. Ma, âReinforcement learning based network coding for drone-aided secure wireless communications,â IEEE Trans. Commun., vol. 70, no. 9, pp. 5975â5988, Sep. 2022.

[24] T. Ren et al., âEnabling efficient scheduling in large-scale UAV-Assisted mobile-edge computing via hierarchical reinforcement learning,â IEEE Internet Things J., vol. 9, no. 10, pp. 7095â7109, May 2022.

[25] N. Zhao, Y. Cheng, Y. Pei, Y.-C. Liang, and D. Niyato, âDeep reinforcement learning for trajectory design and power allocation in UAV networks,â in Proc. 2020 IEEE Int. Conf. Commun., 2020, pp. 1â6.

[26] W. Chen, X. Qiu, T. Cai, H.-N. Dai, Z. Zheng, and Y. Zhang, âDeep reinforcement learning for Internet of Things: A comprehensive survey,â IEEE Commun. Surv. Tut., vol. 23, no. 3, pp. 1659â1692, Third Quarter, 2021.

[27] H. Kang, X. Chang, J. MiÅ¡iÂ´c, V. B. MiÅ¡iÂ´c, J. Fan, and J. Bai, âImproving Dual-UAV aided Ground-UAV bi-directional communication security: Joint UAV trajectory and transmit power optimization,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 10570â10583, Oct. 2022.

[28] Z. Wang, T. Schaul, M. Hessel, H. Hasselt, M. Lanctot, and N. Freitas, âDueling network architectures for deep reinforcement learning,â in Proc. Int. Conf. Mach. Learn., 2016, pp. 1995â2003.

[29] H. Van Hasselt, A. Guez, and D. Silver, âDeep reinforcement learning with double Q-learning,â in Proc. AAAI Conf. Artif. Intell., 2016, pp. 2094â 2100.

[30] W. Shi, J. Li, H. Wu, C. Zhou, N. Cheng, and X. Shen, âDrone-cell trajectory planning and resource allocation for highly mobile networks: A hierarchical DRL approach,â IEEE Internet Things J., vol. 8, no. 12, pp. 9800â9813, Jun. 2021.

[31] R. Ding, F. Gao, and X. S. Shen, â3D UAV trajectory design and frequency band allocation for energy-efficient and fair communication: A deep reinforcement learning approach,â IEEE Trans. Wireless Commun., vol. 19, no. 12, pp. 7796â7809, Dec. 2020.

[32] Q. Wei, Y. Li, J. Zhang, and F.-Y. Wang, âVGN: Value decomposition with graph attention networks for multiagent reinforcement learning,â IEEE Trans. Neural Netw. Learn. Syst., vol. 35, no. 1, pp. 182â195, Jan. 2024.

[33] T. Rashid, M. Samvelyan, C. S. De Witt, G. Farquhar, J. Foerster, and S. Whiteson, âMonotonic value function factorisation for deep multiagent reinforcement learning,â J. Mach. Learn. Res., vol. 21, no. 1, pp. 7234â7284, 2020.

[34] R. Pina, V. D. Silva, J. Hook, and A. Kondoz, âResidual Q-networks for value function factorizing in multiagent reinforcement learning,â IEEE Trans. Neural Netw. Learn. Syst., vol. 35, no. 2, pp. 1534â1544, Feb. 2024.

[35] Z. Wang et al., âSample efficient actor-critic with experience replay,â 2016, arXiv:1611.01224.

[36] Y. Zhou et al., âImproving physical layer security via a UAV friendly jammer for unknown eavesdropper location,â IEEE Trans. Veh. Technol., vol. 67, no. 11, pp. 11280â11284, Nov. 2018.

[37] Unmanned Aerial System (UAS) support in 3GPP, document TS 22.125 V19.2.0, 3GPP, Jun. 2024.

[38] S. Yin and F. R. Yu, âResource allocation and trajectory design in UAV-Aided cellular networks based on multiagent reinforcement learning,â IEEE Internet Things J., vol. 9, no. 4, pp. 2933â2943, Feb. 2022.

<!-- image-->

Qubeijian Wang (Member, IEEE) received the BE degree in electrical engineering from the University of Liverpool, U.K., in 2015, the ME degree in telecommunications from the University of Melbourne, Australia, in 2017, and the PhD degree in electronic information technology from the Macau University of Science and Technology, Macau, in 2020. He is currently an assistant professor with the School of Cybersecurity, Northwestern Polytechnical University, China. His research interests include UAV-aided communications, physical-layer security, and large-scale

network performance analysis. He serves as a TPC Member for conferences, including GLOBECOM2021-2023 and ICC 2024; and a reviewer for various prestigious IEEE journals.

<!-- image-->

Shiyue Tang received the BEng degree in network engineering from the Xiâan University of Posts & Telecommunications, XiÃ¢an, China, in 2022. He is currently working toward the MEng degree in network and information security from Northwestern Polytechnical University, Xiâan, in 2025. His research interests include UAV aided communications and wireless communication security.

<!-- image-->

Wen Sun (Senior Member, IEEE) received the BE degree from the Harbin Institute of Technology, in 2009, and the PhD degree in electrical and computer engineering from the National University of Singapore, in 2014. She is currently a full professor with Northwestern Polytechnical University, China. Her research interests include cover a wide range of areas including wireless mobile communications, IoT, 5 G, and blockchain. She has published more than 50peer reviewed papers in various prestigious IEEE journals and conferences, including IEEE Transactions on

Industrial Informatics, IEEE Transactions on Wireless Communications, IEEE Network, IEEE Wireless Communications. She was the recipient of the best paper award of GlobeCom2019.

<!-- image-->

Hong-Ning Dai (Senior Member, IEEE) received the PhD degree in computer science and engineering from the Department of Computer Science and Engineering, The Chinese University of Hong Kong. Currently, he is an associate professor with the Department of Computer Science, Hong Kong Baptist University, Hong Kong. His current research interests include the Internet of Things, Big Data, and blockchain technology. He has served as an editor for Computer Communications (Elsevier), Connection Science (Taylor & Francis), and IEEE Access, and a

guest editor for IEEE Transactions on Industrial Informatics, IEEE Transaction Emerging Topics in Computing, and IEEE Open Journal of The Computer Society.

<!-- image-->

Yin Zhang (Senior Member, IEEE) is currently a full professor with the School of Information and Communication Engineering, University of Electronic Science and Technology of China, Chengdu, China. He is the co-chair of the IEEE Computer Society Big Data Special Technical Community (STC). He serves as an editor or an associate editor for IEEE Network, IEEE Systems Journal, Information Fusion, and Journal of Circuits Systems and Computers.

<!-- image-->

Geng Sun (Senior Member, IEEE) received the BS degree in communication engineering from Dalian Polytechnic University, and the PhD degree in computer science and technology from Jilin University, in 2011 and 2018, respectively. He was a visiting researcher with the School of Electrical and Computer Engineering, Georgia Institute of Technology, USA. He is an associate professor with College of Computer Science and Technology, Jilin University. His research interests include wireless networks, UAV communications, collaborative beamforming, and optimizations.

<!-- image-->

Mohsen Guizani (Fellow, IEEE) received the BS (with distinction), MS and PhD degrees in electrical and computer engineering from Syracuse University, Syracuse, NY, USA, in 1985, 1987, and 1990, respectively. He is currently a professor in machine learning with the Mohamed Bin Zayed University of Artificial Intelligence (MBZUAI), Abu Dhabi, UAE. Previously, he worked in different institutions in the USA. His research interests include applied machine learning and artificial intelligence, smart city, Internet of Things (IoT), intelligent autonomous systems, and

cybersecurity. He was listed as a Clarivate Analytics Highly Cited Researcher in Computer Science in 2019, 2020, 2021 and 2022. He has won several research awards including the â2015 IEEE Communications Society Best Survey Paper Awardâ, the Best ComSoc Journal Paper Award in 2021 as well 5 Best Paper Awards from ICC and Globecom Conferences. He is the author of 11 books, more than 1000 publications and several US patents. He is also the recipient of the 2017 IEEE Communications Society Wireless Technical Committee (WTC) Recognition Award, the 2018 AdHoc Technical Committee Recognition Award, and the 2019 IEEE Communications and Information Security Technical Recognition (CISTC) Award. He served as the editor-in-chief of IEEE Network and is currently serving on the Editorial Boards of many IEEE Transactions and Magazines. He was the chair of the IEEE Communications Society Wireless Technical Committee and the chair of the TAOS Technical Committee. He served as the IEEE Computer Society Distinguished Speaker and is currently the IEEE ComSoc Distinguished Lecturer.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_4_img_1.png|page_4_img_1]]
3. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_6_img_1.png|page_6_img_1]]
4. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_14_img_1.png|page_14_img_1]]
5. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_14_img_2.png|page_14_img_2]]
6. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_16_img_1.jpeg|page_16_img_1]]
7. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_16_img_2.jpeg|page_16_img_2]]
8. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_17_img_1.jpeg|page_17_img_1]]
9. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_17_img_2.jpeg|page_17_img_2]]
10. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_17_img_3.jpeg|page_17_img_3]]
11. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_17_img_4.jpeg|page_17_img_4]]
12. [[../extracted_images/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr/page_17_img_5.jpeg|page_17_img_5]]

---

