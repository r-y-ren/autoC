# Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdroppers in UAV-Enabled Mobile Edge Computing

Xulong Li , Student Member, IEEE, Wei Huangfu , Member, IEEE, Xinyi Xu , Jiahao Huo , and Keping Long , Senior Member, IEEE

AbstractâMobile edge computing (MEC) has attracted widespread attention due to its ability to effectively alleviate the cloud computing load and significantly reduce latency. However, the potential eavesdroppers challenge the security of the MEC systems and the rapid development of artificial intelligence (AI) has made this security situation more severe. In most existing studies, the eavesdroppers are non-intelligent and it is assumed that they are fixed or move in a simple manner. Obviously, there is a gap from such an assumption to the real conditions that the eavesdropping unmanned aerial vehicles (UAVs) may adjust their flight paths intelligently. To better reflect real-world scenarios, we consider a multi-UAV-assisted MEC system in the presence of intelligent eavesdroppers and propose an adversarial multi-agent reinforcement learning (MARL)-based scheme for secure computational offloading and resource allocation. With this scheme, we aim to solve the zero-sum game between the legitimate UAVs and the eavesdropping UAVs, in which the two types of UAVs take turns acting as the agents of MARL to alternately optimize their respective opposing objectives. The simulation experimental results indicate that the proposed scheme significantly outperforms the existing baseline methods in dealing with the intelligent eavesdropping UAVs, and ensures high energy efficiency of Internet of Things (IoT) devices even in the worst-case scenario when dealing with potential eavesdropping threats.

Index TermsâMobile edge computing (MEC), multi-agent reinforcement learning (MARL), resource allocation, unmanned aerial vehicle (UAV).

## I. INTRODUCTION

N TRADITIONAL centralized cloud computing network architectures, data usually needs to be transmitted from devices to remote data centers or cloud servers for processing and analysis. However, with the explosive growth of Internet of Things (IoT) devices and the diversification of mobile applications, the demand for low latency, high bandwidth, and high reliability challenges centralized cloud computing. Fortunately, mobile edge computing (MEC) has emerged, which reduces the latency of data transmission by deploying servers and computing resources at the edge of the network [1], [2].

However, the resource allocation problem in MEC is more challenging compared to centralized cloud service networks [3]. First, the users in MEC environments are highly dynamic, resource demands may change rapidly, and resource allocation policies need to be adapted in real-time. Second, the resources of edge servers in MEC are usually very limited and may contain many different types of resources, increasing the complexity of resource allocation. Third, MEC resource allocation needs to consider multiple objectives, such as energy efficiency, response time, and cost, which may sometimes be conflicting [4]. Fourth, resource allocation policies also need to ensure data security and user privacy. Finally, as the number of users and devices increases, MEC systems need to be well scalable, and resource allocation policies should be able to scale to large-scale networks without significantly sacrificing performance [5].

As an emerging airborne device with high mobility and flexibility, unmanned aerial vehicles (UAVs) can be rapidly deployed into various complex environments to provide real-time and efficient data acquisition and transmission services for ground users. The combination of MEC and UAV technology provides a new solution for a variety of real-time demanding and computationally intensive mobile applications. UAVs can be used as relay nodes and aerial base stations to assist wireless communications, which are already widely used in MEC [6], [7]. Compared with ground-based MEC, the communication links in UAV-enabled MEC are dominated by line-of-sight (LoS) links, which can bring better communication connectivity and coverage, and thus can provide a better quality of service (QoS) to users [8], [9]. However, due to the broadcast nature of wireless communications, the privacy and security of user data is as a result more serious, and protecting against eavesdropping has become a key challenge in computation offloading in UAVs-enabled MEC. On one hand, it is because MEC sends data to edge servers, which are more prone to data leakage than centralized cloud computing [10]; on the other hand, it is because airborne wireless channels are more vulnerable to eavesdropping and interception by malicious jammers than ground channels [11].

To overcome the above challenges, more and more scholars [12], [13], [14] for secure computational offloading of UAVassisted MEC have proposed reinforcement learning (RL)-based schemes, which adapt to new network environments through learning without the need for an explicit problem model.

## A. Related Work

1) Security of UAV-Enabled Wireless Network With Eavesdroppers: There are two main ways to improve data security in wireless communication, the first is by encrypting the data using encryption algorithms [15]. However, as the computational power increases, this approach becomes less and less confidential and is made more challenging by the payload-constrained nature of UAVs [16], [17]. Another approach based on physical layer security (PLS) is considered a promising technique to improve the security of UAV-enabled wireless communication networks, mainly by varying the relative distance of the data transmission source from the eavesdropper and the target user, and adding artificial noise [18].

The problem of secure communication in the presence of location-fixed eavesdroppers was investigated in [19], [20], [21]. In [19], a secure communication network assisted by a communication UAV and multiple jamming UAVs working together is investigated, where multiple ground eavesdroppers are present. The authors propose a scheme based on an attention mechanism and multi-agent reinforcement learning to maximize the sum of secure data rates for all ground users. The authors study a secure communication network aided by a UAV equipped with an intelligent reflective surface in [20] and propose a DQNbased scheme to maximize the secrecy rate while guaranteeing the quality of service (QoS) requirements of legitimate users. The authors in [21] investigated a terrestrial fixed IRS-assisted wireless secure communication system to protect the communications of multiple legitimate users in the presence of multiple terrestrial eavesdroppers and proposed a secure beamforming method based on reinforcement learning to maximize the secure transmission rate.

Further, to investigate the effect of the eavesdropperâs positional movement on the performance of the secure communication system, the authors in [22], [23], [24], [25], [26] made different assumptions about the eavesdropperâs position and movement trajectory. The eavesdropper is assumed to roam randomly in a specific area in [22], [23]. In [22], the authors investigate the confidentiality performance of an air-to-ground communication network in the presence of multiple random walk eavesdroppers. In [23], the authors investigate the problem of secure communication over a terrestrial link in a limited space region where there are multiple friendly jamming drones and an illegal random wandering eavesdropping UAV. The eavesdropper is assumed to move according to a fixed trajectory in [24], [25], [26]. In [24], the authors investigate a single legitimate UAV-assisted secure communication network in which an illegitimate eavesdropper UAV is present. The authorsâ goal is to maximize the secure data rate between ground users and legitimate UAVs by jointly optimizing the UAVâs trajectory, transmit power, and user scheduling. A dual UAV (one base station UAV and one auxiliary jamming UAV)assisted secure communication network with multiple ground eavesdroppers and one air eavesdropper UAV is studied in [25]. In order to maximize the minimum average secrecy rate for all ground users, the authors propose an efficient algorithm based on successive convex approximation (SCA) and block coordinate descent (BCD) to jointly optimize the base station UAV trajectory, the auxiliary jamming UAV trajectory, the transmit power control and the user scheduling. The authors in [26] study a novel, multi-UAV-assisted wireless information surveillance scenario in which multiple UAV eavesdroppers are present. In order to maximize the userâs secure data rate, the authors propose a reinforcement learning-based solution. In [27], the authors consider the impact of location-fixed eavesdroppers and mobile eavesdroppers on the performance of secure communication systems between UAVs and ground users, respectively, and propose corresponding UAV trajectory planning schemes.

All of the above studies made different assumptions about the eavesdropperâs location or movement trajectory without considering a more realistic scenario, i.e., that the eavesdropper is intelligent and can dynamically adjust its trajectory according to its surroundings in order to perform more efficient eavesdropping. In [28], the authors study a secure communication system in the presence of a legitimate UAV and an intelligent eavesdropping UAV, and in order to maximize the sum of the secure rates for all ground users, the authors propose a multi-agent reinforcement learning based scheme which takes both the legitimate UAV and the eavesdropping UAV as agents simultaneously to optimize their policies according to their respective objectives. However, research on secure communication for smart eavesdroppers is still insufficient and especially scarce for scenarios where multiple smart eavesdroppers exist.

2) Reinforcement Learning: RL is when agents interact with the environment in a trial-and-error manner and optimize their actions to maximize long-term rewards based on the reward information feedback from the environment [29]. Single-agent reinforcement learning algorithms, such as deep Q-network (DQN) [30], proximal policy optimization (PPO) [31], are widely used in games and other fields, and have achieved great success. Due to the instability of the environment and the credit allocation of multiple agents, it is impossible to learn effective strategies in a multi-agent environment. Therefore, some researchers have proposed many multi-agent reinforcement learning (MARL) algorithms based on the centralized training distributed execution (CTDE) framework, such as multi-agent deep deterministic policy gradient (MADDPG) [32], valuedecomposition networks (VDN) [33], and multi-agent proximal policy optimization (MAPPO), which mainly use a critic with access to global information to guide the actor learning during training, while the actor only has access to incomplete local information so that it can be executed in a distributed manner. There are some scenarios where the optimal policy of the agent depends on the behavior of the opponent in the environment, such as Go, so it is very difficult and important to set a suitable opponent for the agent. Therefore, a general framework for self-play training is proposed in [34], which uses the historical strategies generated by the agent during the training process as the adversaryâs strategies to train the agent.

## B. Motivation and Contributions

Most of the existing studies [19], [20], [21], [22], [23], [24], [25], [26], [27] optimize the performance of the system under the assumption that the eavesdropper has a fixed location or moves based on simple rules.

In practice, however, the eavesdropper is intelligent, and can dynamically adjust its position according to the surrounding environment to improve the eavesdropping efficiency. We consider directly applying prior methods to deal with the intelligent eavesdropper and formally found that the performance suddenly dropped. The model is trained and performs well according to certain fixed eavesdroppers, while the performance suddenly drops when the eavesdropper starts changing its position according to the surroundings in order to eavesdrop more efficiently during the evaluation phase. This is because the obtained model suffers from severe overfitting issues and cannot be adapted to intelligent moving eavesdroppers.

Based on the above motivation, we consider a multi-UAVenabled MEC scenario with multiple intelligent eavesdroppers and propose an adversarial multi-agent reinforcement learning method to solve it. The main contributions of this paper are summarized as follows.

1) We consider the problem that the eavesdroppers are intelligent, in other words, not only can they dynamically adjust their flight trajectories according to different surroundings but also collaborate to eavesdrop more effectively. Such a assumption is very different from those in the existing research that the eavesdroppers are fixed or move in a simple manner. We also consider the restricted communication among the UAVs. Thus, the problem concerned in this paper is closer to the real-world attack and defense scenarios than those studied in the literature.

2) We address the adversarial between two types of intelligent UAVs and introduce a min-max optimization objective reflecting the zero-sum game equilibrium, where the legitimate UAVs try to increase the energy efficiency of the IoT devices but the eavesdropping UAVS try to decrease it.

3) We propose a scheme based on an adversarial multi-agent reinforcement learning algorithm that uses the MARL algorithm as the base algorithm. In the proposed scheme, the legitimate UAVs and the eavesdropping UAVs take turns acting as the agents of the MARL, alternately optimizing their respective policies with the objectives of maximizing and minimizing the energy efficiency of IoT devices, respectively.

4) Simulation results are provided to demonstrate that the proposed solution based on adversarial multi-agent reinforcement learning has a significant advantage over prior solutions in dealing with the intelligent eavesdropping problem. Specifically, compared to previous solutions, the proposed solution has the maximum worst-case energy efficiency of IoT devices in the fight against intelligent eavesdropping UAVs in all the scenarios with different numbers of eavesdropping UAVs.

The rest of the paper is organized as follows. In Section II, we introduce the system model and the optimization objective. The problem is reformulated and a solution is proposed in Section III. Simulation experiments and analysis are performed in Section IV, and conclusions are finally drawn in Section V.

## II. SYSTEM MODEL AND PROBLEM DESCRIPTION

In this section, we first present the system model of the multi-UAV-enabled MEC network with intelligent eavesdropping UAVs. Then the communication model and the computational model are discussed. Finally, the optimization problem of the system is formulated.

## A. System Model

In this paper, we consider a multi-UAV-enabled MEC network against intelligent eavesdropping UAVs as depicted in Fig. 1, which includes N legitimate UAVs $\{ \mathrm { U A V } _ { n } | n \in \texttt { N } = \{ 1 , . . . , N \} \}$ , K eavesdropping UAVs $\left\{ \operatorname { E a v } _ { k } | k \in \mathbb { K } = \left\{ 1 , \dots , K \right\} \right\}$ , and M IoT devices $\{ \mathrm { I o T } _ { m } | m \in$ $\mathbb { M } = \{ 1 , \dots , M \} \}$ }. In this system, IoT devices generate computational tasks and then offload some or all of them to legitimate UAVs to utilize their computational resources for more efficient execution of computational tasks. Meanwhile, during the offloading of computational tasks, the eavesdropping UAVs dynamically adjust their trajectories according to the surrounding environment to perform more effective eavesdropping, which should be guarded against.

Specifically, we discretize the time that duration T seconds into equal T time slots, each time slot duration $\mathcal { T } / T$ second. In each time slot $t \in \mathbb { T } = \{ 1 , . . . , T \}$ , the $\mathrm { I o T } _ { m }$ generates a computational task $D _ { m } ( t ) = \{ S _ { m } ( t ) , C _ { m } ( t ) , L _ { m } ( t ) \}$ , where $S _ { m } ( t )$ is the bit size of data, $C _ { m } ( t )$ is the number of CPU cycles required to execute the computational task, and $L _ { m } ( t ) < \mathcal { T } / T$ is the maximum latency constraint in second. $D _ { m } ( t )$ should be accomplished within $L _ { m } ( t )$ . We omit the index t of the time slot in the absence of ambiguity to simplify the following. To accomplish $D _ { m } , \mathrm { I o T } _ { m }$ can offload it to the legitimate UAVs for processing. We define a variable $\alpha _ { I } = ( \alpha _ { I } ^ { 1 } , \dots , \alpha _ { I } ^ { M } )$ to encode the offloading scheme for IoT devices. Specifically, for Io $\Gamma _ { m } , \alpha _ { I } ^ { m } = ( \alpha _ { I } ^ { m , 1 } , \cdot \cdot \cdot , \alpha _ { I } ^ { m , N } )$ is a N-dimension vector with all elements being binary, where $\alpha _ { I } ^ { m , n } = 1$ means offloading to $\mathrm { U A V } _ { n } .$ . Note that, IoT devices can select at most one location to offload computational tasks in each time slot, i.e. $\textstyle \sum _ { n } \alpha _ { I } ^ { m , n } \leq 1$ Â· And the number of IoT devices that select the same $\mathrm { U A V } _ { n }$ for computational offloading cannot exceed C in each time slot, i.e., $\Sigma _ { m } \alpha _ { I } ^ { m , n } \leq C$

In addition, the legitimate UAVs are equipped with double antennas, one of which is used to receive computing tasks offloaded by the IoT devices, and the other antenna is used to send artificial noise signals against eavesdropping by eavesdropping UAVs [35].

<!-- image-->  
Fig. 1. Multi-UAV-enabled MEC network model in the presence of intelligent eavesdropping UAVs.

## B. Communication Model

In this section, we introduce how data communicates in our system and find out the communication latency and energy consumption, which are two vital metrics related to our final optimization objective.

In our system, data communication happens among the IoT devices, the legitimate UAVs, and the eavesdropping UAVs when offloading tasks. Specifically, the IoT devices offload computational tasks to the legitimate UAV (I2U), during which the eavesdropping UAVs eavesdrop on the data (I2E), and the legitimate UAV emits artificial noise to interfere with its eavesdropping (U2E).

We introduce a three-dimensional Cartesian Coordinate System (CCS) to encode the distance among devices. For each time slot, the positions of IoT $\mathbf { \Phi } _ { m } , \mathbf { \Lambda } _ { \mathrm { U A V } _ { n } }$ , and $\mathrm { E a v } _ { k }$ are denoted by $Q _ { I } ^ { m } = \{ x _ { I } ^ { m } , y _ { I } ^ { m } , 0 \} , Q _ { U } ^ { n } = \{ x _ { U } ^ { n } , y _ { U } ^ { n } , z _ { U } ^ { n } \}$ , and $Q _ { E } ^ { k } = $ $\{ x _ { E } ^ { k } , y _ { E } ^ { k } , z _ { E } ^ { k } \}$ , respectively. Note that, the legitimate and eavesdropping UAVs are able to move, which can fly within the range of altitudes from $Z _ { \mathrm { m i n } } \mathrm { t o } Z _ { \mathrm { m a x } }$ above the square target area with side length G. Due to the limited communicable area of ${ \mathrm { U A V s } } .$ $\mathrm { I o T } _ { m }$ can offload computational tasks to $\mathrm { U A V } _ { n }$ only when their horizontal distance $d _ { I U } ^ { \bar { m } , n }$ satisfies

$$
d _ { I U } ^ { m , n } \leq \frac { z _ { U } ^ { n } } { t a n ( \theta _ { n } ) } ,\tag{1}
$$

where $d _ { I U } ^ { m , n } = \sqrt { ( x _ { U } ^ { n } - x _ { I } ^ { m } ) ^ { 2 } + ( y _ { U } ^ { n } - y _ { I } ^ { m } ) ^ { 2 } }$ and $\theta _ { n }$ is the elevation angle of the legitimate UAV n antenna.

The channel between $\mathrm { I o T } _ { m }$ and $\mathrm { U A V } _ { n } , \mathrm { I o T } _ { m }$ and $\mathrm { E a v } _ { k }$ , and $\mathrm { U A V } _ { n }$ and $\mathrm { E a v } _ { k }$ be modeled by the Rician fading channel, which can be expressed as [36]

$$
h _ { I U } ^ { m , n } = \sqrt { \rho L _ { I U } ^ { m , n - \xi } } \left( \sqrt { \frac { \beta } { \beta + 1 } } g _ { I U } ^ { m , n } + \sqrt { \frac { 1 } { \beta + 1 } } \tilde { g } _ { I U } ^ { m , n } \right) ,
$$

$$
\begin{array} { r l } & { { \displaystyle h _ { I E } ^ { m , k } = \sqrt { \rho { \cal L } _ { I E } ^ { m , k ^ { - \xi } } } \left( \sqrt { \frac { \beta } { \beta + 1 } } g _ { I E } ^ { m , k } + \sqrt { \frac { 1 } { \beta + 1 } } \tilde { g } _ { I E } ^ { m , k } \right) } , } \\ & { { \displaystyle h _ { U E } ^ { n , k } = \sqrt { \rho { \cal L } _ { U E } ^ { n , k ^ { - \xi } } } \left( \sqrt { \frac { \beta } { \beta + 1 } } g _ { U E } ^ { n , k } + \sqrt { \frac { 1 } { \beta + 1 } } \tilde { g } _ { U E } ^ { n , k } \right) } , } \end{array}\tag{2}
$$

where Ï is the power gain at the reference distance of 1 m, Î¾ is the path loss factor, $L _ { I U } ^ { m , \bar { n } } = \Vert Q _ { I } ^ { m } - Q _ { U } ^ { n } \Vert _ { 2 } , L _ { I E } ^ { m , k } = \Vert Q _ { I } ^ { m } - Q _ { E } ^ { k } \Vert _ { 2 }$ and $L _ { U E } ^ { n , k } = \Vert Q _ { U } ^ { n } - Q _ { E } ^ { k } \Vert _ { 2 }$ are the distance between $\mathrm { I o T } _ { m }$ and $\mathrm { U A V } _ { n } , \mathrm { I o T } _ { m }$ and $\mathrm { E a v } _ { k } ,$ k, and $\mathrm { U A V } _ { n }$ and $\mathrm { E a v } _ { k }$ , respectively, $\beta$ is the Rician factor, $g _ { I U } ^ { m , n } , ~ g _ { I E } ^ { m , k }$ , and $g _ { U E } ^ { n , k }$ are light of sight (LoS) components of the channels with $| \bar { g _ { I U } ^ { m , n } } | = 1 , | g _ { I E } ^ { m , k } | = 1$ , and $| g _ { U E } ^ { n , k } | = 1$ , and $\tilde { g } _ { I U } ^ { m , n } \sim C N ( 0 , 1 ) , \tilde { g } _ { I E } ^ { m , k } \sim C N ( 0 , 1 )$ , and $\tilde { g } _ { U E } ^ { n , k } \sim C N ( 0 , 1 )$ are nonlight of sight (NLoS) components of the channels.

After obtaining the channel gain, we compute the data transfer rate for each data communication by Shannonâs formula. Specifically, legitimate UAVs reuse spectrum resources with total channel bandwidth ${ \widehat { B } } ,$ , and the data transfer rate between $\mathrm { I o T } _ { m }$ and $\mathrm { U A V } _ { n }$ can be expressed as

$$
R _ { I U } ^ { m , n } = b _ { I U } ^ { m , n } \widehat { B } l o g _ { 2 } \left( 1 + \frac { p _ { I U } ^ { m , n } h _ { I U } ^ { m , n } } { I _ { U } ^ { n } + I _ { I U } ^ { m , n } + \sigma ^ { 2 } } \right) ,\tag{3}
$$

where $I _ { U } ^ { n } = \omega P _ { J } ^ { n }$ is self-interference caused by $\mathrm { U A V } _ { n }$ using two antennas to receive and transmit signals at the same time, Ï is self-interference coefficient, $p _ { J } ^ { n }$ is the power of the artificial noise emitted by $\mathrm { U A V } _ { n } , \ b _ { I U } ^ { m , n }$ is the proportion of channel bandwidth allocated to Io $\Gamma _ { m }$ by $\mathrm { U A V } _ { n }$ to the total available channel bandwidth $\widehat { B } , p _ { I U } ^ { m , n }$ is the transmission power of $\mathrm { I o T } _ { m } ,$ $\begin{array} { r } { I _ { I U } ^ { m , n } = \sum _ { j \in \mathbb { N } / n } \sum _ { i \in \mathbb { M } } \bar { \alpha } _ { I } ^ { i , j } p _ { I } ^ { i } h _ { I U } ^ { i , n } } \end{array}$ is the interference noise received by $\mathrm { { \bar { U } A } } { \dot { \mathrm { { V } } } } _ { n }$ from other IoT devices that choose different locations for computational offloading [37], [38], and $\sigma ^ { 2 }$ is the Gaussian noise power. The data transfer rate between $\mathrm { I o T } _ { m }$ and

Evak can be expressed as

$$
R _ { I E } ^ { m , k } = b _ { I U } ^ { m , n } \widehat { B } l o g _ { 2 } \left( 1 + \frac { p _ { I U } ^ { m , n } h _ { I E } ^ { m , k } } { I _ { J } ^ { k } + I _ { I E } ^ { m , k } + \sigma ^ { 2 } } \right) ,\tag{4}
$$

where $\begin{array} { r } { I _ { J } ^ { k } = \sum _ { n \in \mathbb { N } } p _ { J } ^ { n } h _ { U E } ^ { n , k } } \end{array}$ is the artificial noise interference received by Eavk from the legitimate UAVs, and $I _ { I E } ^ { m , n } =$ $\begin{array} { r } { \sum _ { j \in \mathbb { N } / n } \sum _ { i \in \mathbb { M } } \alpha _ { I } ^ { i , j } p _ { I } ^ { i } h _ { I E } ^ { i , k } } \end{array}$ is the interference noise received by $\mathrm { E a v } _ { k }$ from other IoT devices that choose different locations for computational offloading.

After obtaining the transfer rate of those communication device pairs, we compute the communication. Particularly, communication latency of $\mathrm { I o T } _ { m }$ offloading computational tasks to $\mathrm { U A V } _ { n }$ is

$$
T _ { I U } ^ { m , n } = \frac { \beta _ { I U } ^ { m , n } S _ { m } } { \left[ R _ { I U } ^ { m , n } - \operatorname* { m a x } _ { k } R _ { I E } ^ { m , k } \right] _ { + } } ,\tag{5}
$$

where $[ R _ { I U } ^ { m , n } - \operatorname* { m a x } _ { k } { R _ { I E } ^ { m , k } } ] _ { + }$ + is the secure data transfer rates that can be achieved when $\mathrm { I o T } _ { m }$ offloading computational tasks to $\mathrm { U A V } _ { n }$ , and $[ x ] .$ + is defined as max $\{ x , 0 \}$ . The corresponding communication energy consumption is

$$
E _ { I U } ^ { m , n } = T _ { I U } ^ { m , n } p _ { I U } ^ { m , n } .\tag{6}
$$

The $\mathrm { U A V } _ { n }$ emits artificial jamming noise at a constant power $p _ { J } ^ { n }$ throughout the time slot of duration $\mathcal { T } / T$ to interfere with eavesdropping, so the corresponding energy consumption is

$$
E _ { U E } ^ { n } = \frac { \mathcal { T } } { T } p _ { J } ^ { n } .\tag{7}
$$

Since the data size of the computation results is much smaller than the input for most mobile applications, we ignore the communication latency and energy consumption caused by legitimate UAVs returning the computation results to the IoT devices [39].

## C. Computational Model

In this section, we compute the computational latency and energy consumption of the IoT devices and legitimate UAVs.

After offloading some of the computational tasks to $\mathrm { U A V } _ { n } .$ the computational latency $T _ { I } ^ { m }$ and energy consumption $E _ { I } ^ { m }$ for $\mathrm { I o T } _ { m }$ to process the remaining computational tasks are

$$
T _ { I } ^ { m } = \frac { \left( 1 - \beta _ { I U } ^ { m , n } \right) C _ { m } } { f _ { I } ^ { m } } ,\tag{8}
$$

and

$$
E _ { I } ^ { m } = g _ { I } ^ { m } \left( f _ { I } ^ { m } \right) ^ { 2 } T _ { I } ^ { m } ,\tag{9}
$$

where $f _ { I } ^ { m }$ is the CPU frequency of $\mathrm { I o T } _ { m }$ , and $g _ { I } ^ { m }$ is the constant associated with the chip architecture of $\mathrm { I o T } _ { m }$

After receiving the computational task offloaded by IoT ${ \dot { \mathbf { \zeta } } } _ { m } ,$ the computational latency $T _ { U } ^ { \bar { m , n } }$ and energy consumption $E _ { U } ^ { m , n }$ for $\mathrm { U A V } _ { n }$ to process it are

$$
T _ { U } ^ { m , n } = \frac { \beta _ { I U } ^ { m , n } C _ { m } } { f _ { I U } ^ { m , n } F _ { U } ^ { n } } ,\tag{10}
$$

and

$$
E _ { U } ^ { m , n } = g _ { U } ^ { n } \left( f _ { I U } ^ { m , n } F _ { U } ^ { n } \right) ^ { 2 } T _ { U } ^ { m , n } ,\tag{11}
$$

where $g _ { U } ^ { n }$ is the constant associated with the chip architecture of $\mathrm { U A V } _ { n } , \mathbf { \check { \Pi } } _ { f _ { I U } } ^ { m , n }$ is the proportion of the CPU frequency assigned by $\mathrm { U A V } _ { n }$ to the computational task offloaded by $\mathrm { I o T } _ { m }$ , and $F _ { U } ^ { n }$ is the CPU frequency of $\mathrm { U A V } _ { n }$

## D. Total Latency and Energy Consumption

In this section, we compute the total latency and energy consumption based on the communication latency and energy consumption introduced in Section II-B, and the computational latency and energy consumption introduced in Section II-C.

Specifically, the IoT device offloads some of its computational tasks to the legitimate UAV and its local processing of the remaining computational tasks in parallel, so the total latency $T _ { m }$ for processing the computational tasks $D _ { m }$ of $\mathrm { I o T } _ { m }$ is

$$
T _ { m } = \operatorname* { m a x } \{ T _ { I } ^ { m } , T _ { I U } ^ { m , n } + T _ { U } ^ { m , n } \} .\tag{12}
$$

We also compute the total energy consumption of the IoT devices and the legitimate UAVs. Specifically, the total energy consumption of the IoT device consists of the energy consumption used to send part of the computational tasks to a legitimate UAV and the energy consumption used to process the remaining computational tasks, So the total energy consumption of $\mathrm { I o T } _ { m }$ is

$$
E _ { I o T } ^ { m } = E _ { I } ^ { m } + E _ { I U } ^ { m } .\tag{13}
$$

Here, we additionally consider the flying energy consumption $E _ { F } ^ { n }$ of $\mathrm { U A V } _ { n } .$ . We use the same UAV flight energy model as in [36]. So $\mathrm { U A V } _ { n } \mathrm { ' s }$ total energy consumption of accomplishing $D _ { m }$ is

$$
E _ { U A V } ^ { n } = \sum _ { m \in \mathbb { M } _ { n } } E _ { U } ^ { m , n } + E _ { U E } ^ { n } + E _ { F } ^ { n } ,\tag{14}
$$

where $\mathbb { M } _ { n }$ is the set of indexes of IoT devices that have chosen to offload computational tasks to $\mathrm { U A V } _ { n }$ . For $\mathrm { U A V } _ { n }$ , one constraint should be always satisfied: the energy consumption should not be greater than its remaining energy $E _ { R } ^ { n }$

In conclusion, the total delay of the computational tasks and the total energy consumption of UAVs and IoT devices are related to the trajectory planning policy of the UAVs and the spectrum, computational, and energy resource allocation policies.

## E. Problem Formulation

In this paper, we aim to achieve multi-objective optimization by optimizing the flight trajectories of UAVs and the resource allocation policy, including maximizing the execution success rate of computational tasks and minimizing the execution latency of computational tasks and the energy consumption of IoT devices. In order to deal with these interrelated optimisation objectives in an integrated manner, we propose a new metric, the energy efficiency of IoT devices, which is defined as the ratio of the weighted sum of the execution success and execution delay of a computational task to the energy consumption of an IoT device, i.e.

$$
E E = \sum _ { m = 1 } ^ { M } \frac { \eta _ { m } - \omega _ { 1 } T _ { m } } { E _ { I o T } ^ { m } } ,\tag{15}
$$

where $\omega _ { 1 } > 0$ is the weighting factor, and $\eta _ { m }$ is the execution success rate of the computational tasks from time slot 1 to time slot t, which can be expressed as

$$
\eta _ { m } ( t ) = \sum _ { i = 1 } ^ { t } { \frac { \mathbb { 1 } \left( T _ { m } ( i ) \leq L _ { m } ( i ) \right) } { t } } ,\tag{16}
$$

where 11(X) is the indicator function, whose value is 1 when X is true and 0 otherwise, which can be formulated as

$$
\mathbb { I } \left( T _ { m } ( i ) \leq L _ { m } ( i ) \right) = \left\{ 1 , T _ { m } ( i ) \leq L _ { m } ( i ) , \right.\tag{17}
$$

In addition, we consider both the legitimate UAVs (legitimate UAV cluster) and the eavesdropping UAVs (eavesdropping UAV cluster) to be intelligent and they can optimize their decisions in achieving their respective goals. Specifically, the legitimate UAVs maximize the energy efficiency of IoT devices by optimizing their decisions $\mathbb { X } _ { U }$ , which include trajectory, spectrum resource, and computational resource allocation, as well as the transmission power of IoT devices and the power of artificial noise, i.e. $\mathbb { X } _ { U } = \{ Q _ { U } ^ { n } , b _ { I U } ^ { m , n } , f _ { I U } ^ { m , n } , \beta _ { I U } ^ { m , n } , p _ { I U } ^ { m , n } , p _ { J } ^ { n }$ , ân â N, $m \in \mathbb { M } \}$ , while the eavesdropping UAVs optimize their decision (trajectory) $\mathbb { X } _ { E } = \{ Q _ { E } ^ { k } , \forall k \in \mathbb { K } \}$ with the opposite objective. This process can be modeled as a max-min optimization problem, which is formulated as

$$
P \mathbf { 1 } : \operatorname* { m a x } _ { \mathbb { X } _ { U } } \operatorname* { m i n } _ { \mathbb { X } _ { E } } \sum _ { t = 1 } ^ { T } E E \left( \mathbb { X } _ { U } , \mathbb { X } _ { E } \right)\tag{18}
$$

$$
\mathrm { s . t . } \ \frac { - G } { 2 } \leq x _ { U } ^ { n } , y _ { U } ^ { n } \leq \frac { G } { 2 } , \forall n \in \mathbb { N } ,\tag{18a}
$$

$$
Z _ { \operatorname* { m i n } } \le z _ { U } ^ { n } \le Z _ { \operatorname* { m a x } } , \forall n \in \mathbb { N } ,\tag{18b}
$$

$$
\frac { - G } { 2 } \leq x _ { E } ^ { k } , y _ { E } ^ { k } \leq \frac { G } { 2 } , \forall n \in \mathbb { N } ,\tag{18c}
$$

$$
Z _ { \operatorname* { m i n } } \le z _ { E } ^ { k } \le Z _ { \operatorname* { m a x } } , \forall n \in \mathbb { N } ,\tag{18d}
$$

$$
\beta _ { I U } ^ { m , n } , b _ { I U } ^ { m , n } , f _ { I U } ^ { m , n } \in \left[ 0 , 1 \right] , \forall m \in \mathbb { M } , n \in \mathbb { N } ,\tag{18e}
$$

$$
\sum _ { m = 1 } ^ { M } b _ { I U } ^ { m , n } \leq 1 , \sum _ { m = 1 } ^ { M } f _ { I U } ^ { m , n } \leq 1 , \forall n \in \mathbb { N } ,\tag{18f}
$$

$$
\sum _ { n = 1 } ^ { N } \alpha _ { I } ^ { m , n } \leq 1 , \forall m \in \mathbb { M } ,\tag{18g}
$$

$$
\sum _ { m = 1 } ^ { M } \alpha _ { I } ^ { m , n } \leq C , \forall n \in \mathbb { N } ,\tag{18h}
$$

$$
0 \leq p _ { J } ^ { n } \leq p _ { J } ^ { \operatorname* { m a x } } , \forall n \in \mathbb { N } ,
$$

$$
0 \leq p _ { I U } ^ { m , n } \leq p _ { I } ^ { \operatorname* { m a x } } , \forall n \in \mathbb { N } ,\tag{18i}
$$

$$
\sum _ { t = 1 } ^ { T } E _ { U A V } ^ { n } \leq E _ { \operatorname* { m a x } } ^ { n } , \forall n \in \mathbb { N } ,\tag{18j}
$$

(18k)

where constraints (18a)â(18d) indicate that all legitimate UAVs and eavesdropping UAVs can only fly within the range of altitudes $Z _ { \mathrm { m i n } }$ to $Z _ { \mathrm { m a x } }$ above a square target area with side length G, constraints (18i) and (18j) indicate that the artificial noise power $p _ { J } ^ { n }$ of the legitimate UAV and the transmission power $p _ { I U } ^ { m , n }$ of the IoT device must not exceed its corresponding maximum power $p _ { J } ^ { \mathrm { m a x } }$ and $p _ { I } ^ { \mathrm { m a x } }$ , respectively, and constraint (18k) indicates that the energy consumption of the legitimate UAV cannot exceed its maximum energy $E _ { \mathrm { m a x } } ^ { n }$

It is worth noting that we cannot simply maximize the energy efficiency of IoT devices as in previous studies that considered scenarios with non-intelligent eavesdroppers. This is because the energy efficiency of an IoT device depends on the behavior of the eavesdropper, whereas the intelligent eavesdropping UAV can dynamically change its trajectory based on the surrounding communication environment to enable effective eavesdropping. Therefore, we will next focus on maximizing the worst-case energy efficiency of IoT devices in the fight against intelligent eavesdropping UAVs, i.e., maximizing min $\begin{array} { r } { \mathfrak { l } _ { \mathbb { X } _ { E } } \sum _ { t = 1 } ^ { T } E E ( \mathbb { X } _ { U } , \mathbb { X } _ { E } ) } \end{array}$ .

## III. PROBLEM RECONSTRUCTION AND PROPOSED SOLUTION

P1 cannot be solved by traditional optimization methods, or the latency caused by solving is unacceptable. On the one hand, it is a mixed-integer nonlinear programming (MINLP) problem, and the network environment is dynamic and partially observable, which means that the problem needs to be solved based on incomplete information. On the other hand, it is a max-min problem, which makes the problem even more challenging to solve. Therefore, we first reformulate it in the framework of RL and then propose a novel adversarial multi-agent reinforcement learning scheme in this section.

## A. Problem Reformulation

To solve the max-min problem of P1, we decompose it into two subproblems for the legitimate UAVs and the eavesdropping UAVs and optimize them alternatively. Specifically, we first fix the decision of eavesdropping UAVs and maximize the energy efficiency of IoT devices by optimizing the decision of legitimate UAVs, then fix the decision of legitimate UAVs and minimize the energy efficiency of IoT devices by optimizing the decision of eavesdropping UAVs, and finally, repeat the above two steps of alternate optimization until convergence.

For legitimate UAVs, the optimization objective is to maximize the energy efficiency of IoT devices, so for any given optimization variable $\mathbb { X } _ { E }$ of the eavesdropping UAVs, the subproblem of legitimate UAVs can be represented as

$$
P \mathbf { 2 } : \operatorname* { m a x } _ { \mathbb { X } _ { U } } \sum _ { t = 1 } ^ { T } E E ( \mathbb { X } _ { U } | \mathbb { X } _ { E } )\tag{19}
$$

$$
{ \mathrm { s . t . ~ } } ( 1 8 { \mathrm { a } } ) - ( 1 8 { \mathrm { i } } ) .\tag{19a}
$$

For eavesdropping UAVs, we set the optimization objective to minimize the energy efficiency of IoT devices, although the goal in the real world may be to maximize the eavesdropping rate. This is because the goal of this paper is to find a strategy for legitimate UAVs that maximizes the worst-case energy efficiency of IoT devices in the fight against smart eavesdropping UAVs, and with this setup, the performance of the policies for legitimate UAVs can be evaluated more effectively. In addition, eavesdropping UAVs maximizing the eavesdropping rate tend to reduce the energy efficiency of IoT devices. Therefore, while minimizing the energy efficiency of IoT devices and maximizing the eavesdropping rate may appear to be different on the surface, but are both similar for anti-eavesdropping policies of legitimate UAVs. So for any given optimization variable $\mathbb { X } _ { U }$ of the legitimate UAVs, the subproblem of eavesdropping UAVs can be represented as

$$
P \mathbf { 3 } : \operatorname* { m i n } _ { \mathbb { X } _ { E } } \sum _ { t = 1 } ^ { T } E E \left( \mathbb { X } _ { E } | \mathbb { X } _ { U } \right)\tag{20}
$$

$$
{ \mathrm { s . t . ~ } } ( 1 8 { \mathrm { j } } ) , ( 1 8 { \mathrm { k } } ) .\tag{20a}
$$

Then, we transform the problem of competition between legitimate UAV cluster and eavesdropping UAV cluster into a zero-sum game with two players (two UAV clusters), which can be viewed as the legitimate UAV cluster maximizes the long-term energy efficiency $\scriptstyle \sum _ { t = 1 } ^ { T } E E$ of IoT devices by optimizing decision $\mathbb { X } _ { \mathbb { U } }$ (the subproblems P2), while the eavesdropping UAV cluster minimizes it by optimizing decision $\mathbb { X } _ { \mathbb { E } }$ (the subproblems P3).

Finally, to solve subproblems P2 and P3, we transform them into two partially observable Markov games, which include N and K agents, respectively. Each UAV is an agent and can make decisions independently based on its own incomplete observation information. Both partially observable Markov games consist of a shared global state S, a set of observations $\mathbb { O } _ { U } =$ $\{ O _ { U } ^ { 1 } , \ldots , O _ { U } ^ { N } \}$ and ${ \mathbb O } _ { E } = \{ O _ { E } ^ { 1 } , . . . , O _ { E } ^ { K } \}$ , a set of actions $\mathbb { A } _ { U } = \{ A _ { U } ^ { 1 } , \ldots , A _ { U } ^ { N } \}$ and $\mathbb { A } _ { E } = \{ A _ { E } ^ { 1 } , \ldots , A _ { E } ^ { K } \}$ , and a set of rewards $\mathbb { R } _ { U } = \hat { \{ { R _ { U } ^ { 1 } , . . . , R _ { U } ^ { N } \} } }$ and $\mathbb { R } _ { E } = \{ \bar { R } _ { E } ^ { 1 } , \dots , R _ { E } ^ { K } \}$ ï¼ which we describe separately below.

1) State: The shared global state $s \in S$ of the system can be expressed as

$$
\begin{array} { r } { s = \left\{ Q _ { I } ^ { 1 } , \dots , Q _ { I } ^ { M } , L _ { 1 } , \dots , L _ { M } , S _ { 1 } , \dots , S _ { M } , C _ { 1 } , \dots , \right. } \\ { \left. \qquad \quad \right. \left. C _ { M } , Q _ { E } ^ { 1 } , \dots , Q _ { E } ^ { K } , Q _ { U } ^ { 1 } , \dots , Q _ { U } ^ { N } , E _ { R } ^ { 1 } , \dots , E _ { R } ^ { N } \right\} . } \end{array}\tag{21}
$$

2) Observation: Both the legitimate UAVs and the eavesdropping UAVs can only get incomplete observation information, where the legitimate UAV can obtain observation information including its location, remaining energy, location of the nearest C IoT devices within its communicable coverage, and the generated computational tasks, and the eavesdropping UAV can obtain observation information including its location. So the observation $o _ { U } ^ { n } \in O _ { U } ^ { n }$ and $o _ { E } ^ { k } \in O _ { E } ^ { k }$ of $\mathrm { U A V } _ { n }$ and Eavk can be expressed as

$$
\begin{array} { l } { { o _ { U } ^ { n } = \left\{ Q _ { I } ^ { N _ { n , 1 } } , \dots , Q _ { I } ^ { N _ { n , C } } , L _ { N _ { n , 1 } } , \dots , L _ { N _ { n , C } } , S _ { N _ { n , 1 } } , \right. } } \\ { { \mathrm { ~ } } } \\ { { \left. \dots , S _ { N _ { n , C } } , C _ { N _ { n , 1 } } , \dots , C _ { N _ { n , C } } , Q _ { U } ^ { n } , E _ { R } ^ { n } \right\} } } \end{array}\tag{22}
$$

and

$$
o _ { E } ^ { k } = \left\{ Q _ { E } ^ { k } \right\} ,\tag{23}
$$

<!-- image-->  
Fig. 2. The scheme based on adversarial multi-agent reinforcement learning algorithm.

where $\{ N _ { n , 1 } , \ldots , N _ { n , C } \}$ is the indexes of the nearest C IoT devices within the communicable coverage of the $\mathrm { U A V } _ { n }$ Â·

3) Action: According to optimization variables $\mathbb { X } _ { U }$ and $\mathbb { X } _ { E }$ in subproblems P2 and P3, the action $a _ { U } ^ { n } \in A _ { U } ^ { n }$ and $a _ { E } ^ { k } \in A _ { E } ^ { k }$ of $\mathrm { U A V } _ { n }$ and $\mathrm { E a v } _ { k }$ can be expressed as

$$
\begin{array} { c } { { a _ { U } ^ { n } = \left\{ p _ { J } ^ { n } , f _ { I U } ^ { N _ { n , 1 } , n } , \ldots , f _ { I U } ^ { N _ { n , C } , n } , \beta _ { I U } ^ { N _ { n , 1 } , n } , \ldots , \right. } } \\ { { \left. \beta _ { I U } ^ { N _ { n , C } , n } , b _ { I U } ^ { N _ { n , 1 } , n } , \ldots , b _ { I U } ^ { N _ { n , C } , n } , p _ { I U } ^ { N _ { n , 1 } , n } , \ldots , \right. } } \\ { { \left. p _ { I U } ^ { N _ { n , C } , n } , \Delta Q _ { U } ^ { n } \right\} } } \end{array}\tag{24}
$$

and

$$
a _ { E } ^ { k } = \left\{ \Delta Q _ { E } ^ { k } \right\} ,\tag{25}
$$

where $\Delta Q _ { U } ^ { n } ( t ) = Q _ { U } ^ { n } ( t + 1 ) - Q _ { U } ^ { n } ( t )$ and $\Delta Q _ { E } ^ { k } ( t ) = Q _ { E } ^ { k }$ $( t + 1 ) - Q _ { E } ^ { k } ( t )$ are the displacements of $\mathrm { U A V } _ { n }$ and Eavk at time slot t, respectively. When the IoT device is within the communicable coverage of multiple legitimate UAVs, it will select the closest legitimate UAV for offloading the computational task.

4) Reward: According to the subproblems P2 and P3, the optimization objectives of the legitimate UAV cluster and the eavesdropping UAV cluster are to maximize and minimize the energy efficiency of IoT devices, respectively. So the reward $r _ { U } ^ { n } \in R _ { U } ^ { n }$ and $r _ { E } ^ { k } \in R _ { E } ^ { k }$ of $\mathrm { U A V } _ { n }$ and Eavk can be expressed as

$$
r _ { U } ^ { n } = E E \left( a _ { U } ^ { n } | o _ { U } ^ { n } \right)\tag{26}
$$

and

$$
r _ { E } ^ { k } = - E E \left( a _ { E } ^ { k } | o _ { E } ^ { k } \right) .\tag{27}
$$

## B. Proposed Scheme

As shown in Fig. 2, we propose a scheme based on an adversarial multi-agent reinforcement learning algorithm, which solves the partially observable Markov game between the above two UAV clusters separately with the MARL algorithm as the base algorithm, and solves the zero-sum game between the above legitimate UAV clusters and the eavesdropping UAV clusters in an alternate optimization manner. Next, we introduce the proposed scheme using MAPPO [40] as the base algorithm as an example.

1) MAPPO: In a multi-agent reinforcement learning environment, all agents improve their policies to maximize cumulative returns by interacting with the environment based on their incomplete observations. MAPPO is a multi-agent reinforcement learning algorithm based on a centralized training distributed execution framework with PPO [31] as the base algorithm. In MAPPO, each agent i has a policy network $\pi _ { \boldsymbol { \theta } _ { i } }$ with the parameter of $\theta _ { i }$ and a critic network $V _ { i }$ with the parameter of $\phi _ { i }$ ï¼ where the policy network takes incomplete observations $o _ { i }$ as input and outputs the action $a _ { i }$ , and the critic network is used to fit the agentâs state-value function, which takes the global state s as input in the centralized training phase.

There is also an experience replay buffer D that stores the experience tuples $( s , o , a , r )$ generated by the interaction between the agents and the environment, where $s , o = \{ o _ { 1 } , \ldots , o _ { i } , \ldots \}$ $a = \{ a _ { 1 } , \ldots , a _ { i } , \ldots \} , r = \{ r _ { 1 } , \ldots , r _ { i } , \ldots \}$ are the global state, observations, joint actions, rewards for all agents, respectively. The experience tuple in the experience replay pool is used for updates to the agentsâ policy network and critic network.

The advantage function estimates the advantage of taking a particular action over other actions in the current state or observation, i.e., the extent to which the action is expected to produce higher or lower returns compared to other actions. Each agent maximizes the advantage function to ensure that $o _ { i }$ selected by $\pi _ { \boldsymbol { \theta } _ { i } } ( o _ { i } )$ under $o _ { i }$ is superior to the other possible actions. We use generalized advantage estimation (GAE) to estimate more accurately the advantage function, which can be expressed as [41]

$$
\hat { A } _ { i } ( t ) = \sum _ { t ^ { \prime } = t } ^ { T } ( \gamma \lambda ) ^ { t ^ { \prime } - t } \delta _ { i } ( t ^ { \prime } ) ,\tag{28}
$$

where $\gamma \in [ 0 , 1 )$ is the discount factor, $\delta _ { i } ( t ) = r _ { i } ( t ) +$ $\gamma V _ { \phi _ { i } } ( s ( t + 1 ) ) - V _ { \phi _ { i } } ( s ( t ) )$ ) is the temporal-difference residual, and Î» is used to adjust the biasâvariance tradeoff.

Considering that the policy of MAPPO is on-policy, this means that the updated policy has to be the same as the one for the sampled data. In order to make the adopted data reproducible, an important sampling method is introduced. So we calculate the clipped surrogate objective function of the policy network by

$$
J \left( \theta _ { i } \right) = \mathbb { E } \left[ \operatorname* { m i n } \{ d _ { \theta _ { i } } \hat { A } _ { i } , \operatorname { c l i p } \left( d _ { \theta _ { i } } , 1 - \epsilon , 1 + \epsilon \right) \hat { A } _ { i } \} \right] ,\tag{29}
$$

where clip $( X , 1 - \epsilon , 1 + \epsilon )$ clips X from $1 - \epsilon \mathrm { t o } 1 + \epsilon$ , this is to avoid over-modification of the target value to ensure the stability of the update, $d _ { \theta _ { i } }$ i is the policy probability ratio, we calculate it by

$$
d _ { \theta _ { i } } = \frac { \pi _ { \theta _ { i } } \left( a _ { i } | o _ { i } \right) } { \pi _ { \theta _ { i } ^ { o l d } } \left( a _ { i } | o _ { i } \right) } ,\tag{30}
$$

where $\theta _ { i } ^ { o l d }$ is the policy network parameter when agent i samples data.

The critic network can update its parameters by minimizing the mean square error (MSE), we calculate it by

$$
L ( \phi _ { i } ) = \mathbb { E } \left[ ( \hat { V } ( s ) - V _ { \phi _ { i } } ( s ) ) ^ { 2 } \right] ,\tag{31}
$$

Algorithm 1: The Scheme Based on ARL-MAPPO.   
Input: For all legitimate UAVs and eavesdropping UAVs,   
initialize the parameters of policy network $\pi _ { \mathbf { U } }$ and $\pi _ { \mathbf { E } } .$ the   
parameters of critic network $\mathbf { V _ { U } }$ and $\mathbf { V _ { E } } .$   
1: Initialize the adversary policy set $\pi ^ { o } = [ \pi _ { \mathbf { E } } ] .$   
2: for i in $\left\{ 1 , . . . , N _ { i t e r } \right\}$ do   
3: $/ / \mathbf { P 2 }$ : LegitimateUAVsasagents.   
4: for j in $\{ 1 , . . . , N _ { i t e r } ^ { U } \}$ do   
5: $D = D a t a C o l l e c t i o n ( \pi _ { \mathbf { U } } , \pi _ { \mathbf { E } } ) .$   
6: $\pi _ { \bf U } , { \bf V _ { U } } = P a r a m e t e r U p d a t e ( { P } , \pi _ { \bf U } , { \bf V _ { U } } ) .$   
7: for w in $\{ 1 , \dots , W \}$ do   
8: Obtain $E E _ { \pi _ { \mathbf { E } } ^ { \mathbf { w } } }$ for $\pi _ { \mathbf { E } } ^ { \mathbf { w } }$ in $\pi ^ { o }$ with $\pi _ { \mathbf { U } } .$   
9: Calculate $P _ { \pi _ { \mathrm { E } } ^ { \mathrm { w } } }$ according to (32).   
10: end for   
11: Policy sampling $\pi _ { \mathbf { E } } \sim \pi ^ { o } ( \mathbf { P } _ { \pi _ { \mathbf { E } } } )$   
12: end for   
13: $/ / \mathbf { P 3 }$ : EavesdroppingUAVsasagents.   
14: for j in $\{ 1 , . . . , N _ { i t e r } ^ { E } \}$ do   
15: $D = D a t a C o l l e c t i o n ( \pi _ { \bf U } , \pi _ { \bf E } ) .$   
16: $\pi _ { \mathbf { E } } , \mathbf { V _ { E } } = P a r a m e t e r U p d a t e ( D , \pi _ { \mathbf { E } } , \mathbf { V _ { E } } ) .$   
17: end for   
18: $\pi ^ { o } = [ \pi ^ { o } \cup \pi _ { \mathbf { E } } ]$   
19: end for   
Ensure: $\boldsymbol { \mathsf { r } } _ { \mathbf { U } } = \bigl [ \pi _ { \theta _ { U } ^ { 1 } } , \dots , \pi _ { \theta _ { U } ^ { N } } \bigr ] .$

where $\begin{array} { r } { \hat { V } ( s ( t ) ) = \sum _ { t ^ { \prime } = t } ^ { T } \gamma ^ { t ^ { \prime } - t } r _ { i } ( t ^ { \prime } ) } \end{array}$ is the state-value of i agent, i.e., the expected cumulative discount rewards starting from state $s ( t )$

2) ARL-MAPPO: In this section, we propose an adversarial multi-agent reinforcement learning-based scheme, i.e., ARL-MAPPO, with the above introduced MAPPO as the base algorithm. This is because most existing schemes optimize the performance of the system under the assumption that the behavior of the eavesdropping UAVs is fixed, and they fail to handle the case where the eavesdropping UAVs are agents.

Specifically, the optimal policy of the legitimate UAVs and the performance of the system relies heavily on the behavior of the eavesdropping UAVs. It is critical and challenging to choose the appropriate behavioral policy for eavesdropping UAVs when optimizing the policy for legitimate UAVs. If the selected policy of eavesdropping UAVs is too strong, it may be difficult for legitimate UAVs to receive effective positive feedback, resulting in their inability to learn effective policy. If the selected policy of eavesdropping UAVs is too weak, although good system performance can be obtained, when the eavesdropping UAVs changes its policy, the system performance may deteriorate sharply. This is because the policy learned by the legitimate UAVs over-fit the policy used by the eavesdropping UAVs during training.

Therefore, an alternating optimization approach is used in the proposed ARL-MAPPO-based scheme, which maximises the worst-case energy efficiency of IoT devices against intelligent eavesdropping UAVs by alternating between legitimate UAV policies and eavesdropping UAV policies. In the first phase, we learn the legitimate UAVsâ policy while holding the eavesdropping UAVsâ policy fixed. Then in the second phase, the legitimate UAVsâ policy is fixed and the eavesdropping UAVsâ policy is learned. This sequence is repeated until convergence.

Algorithm 2: DataCollection.   
Input: $\pi _ { \mathbf { U } } = [ \pi _ { \theta _ { U } ^ { 1 } } , \dots , \pi _ { \theta _ { U } ^ { N } } ]$ , and $\pi _ { \mathbf { E } } = [ \pi _ { \theta _ { E } ^ { 1 } } , \dots , \pi _ { \theta _ { E } ^ { K } } ] .$   
1: $D = \{ \}$   
2: while $N _ { b s } > | D |$ do   
3: Initialize global state s and observation o.   
4: for t in $\{ 1 , . . . , T \}$ do   
5: for n in $\{ 1 , . . . , N \}$ do   
6: $a _ { U } ^ { n } \sim \pi _ { \theta _ { U } ^ { n } } ( \cdot | o _ { U } ^ { n } )$   
7: end for   
8: $a _ { U } = \{ a _ { U } ^ { 1 } , \ldots , a _ { U } ^ { N } \} .$   
9: for k in $\{ 1 , . . . , K \}$ do   
10: $a _ { E } ^ { k } \sim \pi _ { \theta _ { E } ^ { k } } ( \cdot | o _ { E } ^ { k } )$   
11: end for   
12: $a _ { E } = \{ a _ { E } ^ { 1 } , \ldots , a _ { E } ^ { K } \}$   
13: Execute joint actions $a = \{ a _ { U } , a _ { E } \}$ , and observe r,   
o and $s ^ { \prime } .$   
14: Store $\{ s , o , a , r \}$ in D.   
15: $s  s ^ { \prime } , o  o ^ { \prime } .$   
16: end for   
17: end while   
Output: D

Algorithm 1 outlines the ARL-MAPPO algorithm in detail. First, initialize the parameters of policy network $\pi _ { \mathbf { U } } =$ $[ \pi _ { \theta _ { U } ^ { 1 } } , \dots , \pi _ { \theta _ { U } ^ { N } } ]$ and $\pi _ { \mathbf { E } } = [ \pi _ { \theta _ { E } ^ { 1 } } , \dots , \pi _ { \theta _ { E } ^ { K } } ]$ , the critic network $\mathbf { V _ { U } } = [ V _ { \phi _ { U } ^ { 1 } } , \dots , V _ { \phi _ { U } ^ { N } } ]$ and $\mathbf { V _ { E } } ^ { - } = [ V _ { \phi _ { E } ^ { 1 } } , \mathbf { \Omega } , \mathbf { \Omega } , \mathbf { \Omega } , V _ { \phi _ { E } ^ { K } } ]$ for all legitimate UAVs and eavesdropping UAVs. Then, in each of the $N _ { i t e r }$ iterations, we perform a two-step (alternating) process to optimize problems P2 and P3, respectively. In the first step (i.e. lines 4 to 12 of Algorithm 1), we optimise problem P2 by taking legitimate UAVs as agents. In each of the $\overset { \cdot } { N } _ { i t e r } ^ { U }$ iteration, the legitimate UAVs and the eavesdropping UAVs use policy networks ÏU and $\pi _ { E }$ to interact with the environment and collect experience tuples (the DataCollection function). Then, the parameters of the eavesdropping UAVsâ network are fixed, while the parameters of the legitimate UAVsâ network are updated (the P arameterU pdate function). Conversely, the second step (i.e. lines 14 to 17 of Algorithm 1), we optimise problem P3 by taking eavesdropping UAVs as agents. In each of the $N _ { i t e r } ^ { E }$ iteration, the parameters of the legitimate UAVsâ network are fixed, while the parameters of the eavesdropping UAVsâ network are updated. The parameters of the policy network and critic network for legitimate and eavesdropping UAVs are updated according to (28)â(31), the details of which are shown as the P arameterU pdate function in Algorithm 3.

The details of the DataCollection function are shown in Algorithm 2. At each time slot, the policy network of each legitimate UAV and eavesdropping UAV obtains action based on its local observation, then performs joint actions a and obtains the corresponding rewards r, state $s ^ { \prime }$ and observation $o ^ { \prime }$ for the next time slot, and finally puts the generated experience tuples $\{ s , o , a , r \}$ into the experience replay pool $D ,$ where $o =$ $\bigl \{ o _ { U } ^ { 1 } , \dotsc , o _ { U } ^ { N } , o _ { E } ^ { 1 } , \dotsc , o _ { E } ^ { K } \bigr \} , \quad a = \bigl \{ a _ { U } ^ { 1 } , \dotsc , a _ { U } ^ { N } , a _ { E } ^ { 1 } , \dotsc , a _ { E } ^ { K } \bigr \}$ $r = \{ r _ { U } ^ { 1 } , \ldots , r _ { U } ^ { N } , r _ { E } ^ { 1 } , \ldots , r _ { E } ^ { K } \}$ The process continues to be cycled until the number |D| of experience tuples in the experience replay pool D is greater than the batch size $N _ { b s }$

Algorithm 3: P arameterU pdate.   
Input: ${ \overline { { D , \pi , \mathbf { V } } } } .$   
1: for $\{ \pi _ { \theta _ { i } } , V _ { \phi _ { i } } \}$ in {Ï, V} do   
2: $\theta _ { i } { } ^ { o l d }  \theta _ { i }$   
3: Calculate estimated advantage ${ \hat { A } } _ { i }$ according to (28)   
based on $V _ { \tilde { \phi } _ { i } }$   
4: for l in $\{ 1 , \ldots , L \}$ do   
5: Sample a mini-batch B of transitions from $D .$   
6: Update parameter $\theta _ { i }$ by maximizing $J ( \theta _ { i } )$ according   
to (29).   
7: Update parameter $\phi _ { i }$ by minimizing $L ( \phi _ { i } )$   
according to (31).   
8: end for   
9: end for   
Output: Ï, V.

In addition, to improve the generalization of the obtained policies of the legitimate UAVs and to avoid over-fitting to the particular policy of the eavesdropping UAVs. Here is an adversary (the eavesdropping UAV cluster) policy set $\pi ^ { o }$ and add the historical policies of the eavesdropping UAV cluster to it [34]. After each parameter update of the legitimate UAVs in $N _ { i t e r } ^ { U }$ iterations, a policy is randomly selected from the adversary policy set $\pi ^ { o }$ with probability distribution $P _ { \pi ^ { \mathbf { E } } }$ as the eavesdropping UAVsâ policy.

Our goal is to maximize the worst-case energy efficiency of IoT devices in the fight against intelligent eavesdropping UAVs. Therefore, we prefer to focus on policies that lead to lower energy efficiency of IoT devices when fighting against legitimate UAVs. That is, these policies should be selected with a higher probability of being sampled, thus ensuring that legitimate UAVsâ policies are better able to adapt and defend against potential eavesdropping threats.

Therefore, we define the probability that the policy $\pi _ { \mathbf { E } } ^ { \mathbf { w } }$ of the w-th eavesdropping UAVs in the adversary policy set $\pi _ { o }$ is sampled as

$$
P _ { \pi _ { \mathbf { E } } ^ { \mathbf { w } } } = \frac { e ^ { - \alpha E E _ { \pi _ { \mathbf { E } } ^ { \mathbf { w } } } } } { \sum _ { i = 1 } ^ { \mathbf { W } } e ^ { - \alpha E E _ { \pi _ { \mathbf { E } } ^ { \mathbf { i } } } } } , \forall \mathbf { w } \in [ 1 , \ldots , \mathbf { W } ] ,\tag{32}
$$

where Î± is temperature, $E E _ { \pi _ { \mathbf { E } } ^ { \mathbf { w } } }$ is the energy efficiency of IoT devices when the eavesdropping UAVs use policy policies $\pi _ { \mathbf { E } } ^ { \mathbf { w } }$ against the current legitimate UAVsâ policy $\pi _ { \mathbf { U } }$ , and W is the number of policies of the eavesdropping UAVs in the adversary policy set $\pi _ { o } ,$ and $\mathbf { P } _ { \pi _ { \mathbf { E } } } = [ P _ { \pi _ { \mathbf { E } } ^ { 1 } } , \dots , P _ { \pi _ { \mathbf { E } } ^ { \mathbf { W } } } ]$

The process of obtaining $E \breve { E _ { \pi _ { \mathrm { F } } ^ { \mathrm { w } } } } ( \mathrm { i } . \mathrm { e } .$ ., line 8 of Algorithm 1) is similar to Algorithm 2. Specifically, the legitimate UAVs use the current policy $\pi _ { U }$ for trajectory planning and resource allocation to assist in the computational offloading of the IoT devices, while the eavesdropping UAVs use the policy $\pi _ { E } ^ { w }$ in the adversary policy set $\pi _ { o }$ for trajectory planning for effective eavesdropping. After completing the process of repeating multiple episodes of the above, the average energy efficiency of the IoT devices will be recorded as the result $E E _ { \pi _ { E } ^ { w } }$

After training is complete, the critic network will no longer be needed during the evaluation (actual deployment) phase and the legitimate UAVs can make decisions independently without exchanging information with other UAVs using the policy network $\pi _ { \mathbf { U } } = [ \pi _ { \theta _ { U } ^ { 1 } } , \dots , \pi _ { \theta _ { U } ^ { N } } ]$ based on incomplete local information.

## C. Constraint Satisfaction Analysis

The constraints in Problem P1 are all independent of each other, they can be made to satisfy simultaneously using different approaches.

Specifically, for constraints (18a)â(18d) (i.e., positional constraints on UAVs), we satisfy them by truncating the position coordinates of the UAV after it flies out of the boundary. For constraints (18e) and (18f) (i.e., resource allocation variable constraints), we satisfy them by applying the Softmax normalization to the outputs of the policy network. For constraints (18g) and (18h) (i.e., association variable constraints), we satisfy them by applying the argmax operation to the output of the policy network and assuming that the UAV selects at most the nearest C IoT devices. For constraints (18i) and (18j) (i.e., power constraints), we satisfy them by mapping the output of the policy network to the interval 0 to $p _ { J } ^ { \mathrm { m a x } }$ or $p _ { I } ^ { \mathrm { m a x } }$ . For constraint (18k) (i.e., energy consumption constraint of legitimate UAVs), we satisfy it by assuming that the UAVs cease operation once their energy is depleted.

## IV. SIMULATION EXPERIMENTS AND ANALYSIS

In this section, we first introduce the simulation parameter settings and then verify the effectiveness of the proposed algorithm with a large number of simulation experiments.

## A. Simulation Parameter Setting

In this paper, we simulate a multi-UAV-enabled MEC scenario with the presence of intelligent eavesdropping UAVs, whose target area is a square area with a side length. There are M = 20 IoT devices randomly distributed in the target area, and N = 3 legitimate UAVs and $K = 3$ eavesdropping UAVs fly at an altitude of $Z _ { \mathrm { m i n } } = 5 0$ m to $Z _ { \operatorname* { m a x } } = 1 2 0$ m above the target area. The initial coordinates of the legitimate UAVs are (â125, â125, 85), (125, â125, 85), (0, 125, 85), and the initial coordinates of the eavesdropping UAVs are (â125, 125, 85), (0, â125, 85), (125, 125, 85), respectively. The IoT device generates a computational task in each time slot with data size ranging from 10000 to 20000 bits, CPU cycles required to process it ranging from $1 0 ^ { 6 }$ to $1 0 ^ { 7 }$ cyc/bit, and maximum latency constraint ranging from 20 to 40 ms. We mark the latency as 80 ms when the computational task is not successfully processed within the maximum latency constraint. The programming language used in the experiments is Python and the deep learning framework used is Pytorch. The policy networks and critic networks for all legitimate UAVs and eavesdropping UAVs are multilayer perception (MLP) networks with three hidden layers, whose number of nodes per hidden layer is 64 and 128, respectively. The details of the other simulation hyperparameters are summarized in Table I.

TABLE I  
LIST OF THE SIMULATION HYPERPARAMETERS
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Number T of time slots per episode</td><td>50</td></tr><tr><td>Learning rate of policy network</td><td>0.0001</td></tr><tr><td>Learning rate of critic network</td><td>0.001</td></tr><tr><td>Discount factor  $\gamma$ </td><td>0.96</td></tr><tr><td>GAE parameters  $\lambda$ </td><td>0.95</td></tr><tr><td>Clip ratio â</td><td>0.2</td></tr><tr><td>Batch size  $N _ { b s }$ </td><td>2048</td></tr><tr><td>Mini batch size  $| B |$ </td><td>64</td></tr><tr><td>Gaussian noise power  $\sigma ^ { 2 }$ </td><td> $1 0 ^ { - 1 1 } \mathrm { ~ W ~ }$ </td></tr><tr><td>Maximum CPU frequencies of IoT devices</td><td>0.4 GHz</td></tr><tr><td>Maximum CPU frequencies of legitimate UAVs</td><td>2.0 GHz</td></tr><tr><td>Elevation angle  $\theta _ { n }$ </td><td>56.31Â°</td></tr><tr><td>Total channel bandwidth  $\widehat { B }$ </td><td>6MHz</td></tr><tr><td>Maximum transmission power  $p _ { I } ^ { \mathrm { m a x } }$ </td><td>0.1W</td></tr><tr><td>Maximum artificial noise power  $p _ { J } ^ { \operatorname* { m a x } }$ </td><td>1W</td></tr><tr><td> $g _ { I } ^ { m }$  of IoT device m</td><td>10-20</td></tr><tr><td> $g _ { U } ^ { n }$  of legitimate UAV n</td><td>10-19</td></tr><tr><td>Side length G of the square target area</td><td>1000m</td></tr><tr><td>Rician factor  $\beta$ </td><td>10 dB</td></tr><tr><td>Power gain  $\rho$  at the reference distance of 1 m Path loss factor </td><td>20 dB 2.2</td></tr></table>

In order to verify the effectiveness and superiority of the proposed algorithm, we take the following four existing schemes introduced in the introduction of this paper as baseline schemes.

1) Baseline1: All eavesdropping UAVs are fixed at their initial positions, i.e., the scheme in [19], [20], [21].

2) Baseline2: All eavesdropping UAVs fly randomly, i.e., the scheme in [22], [23].

3) Baseline3: All eavesdropping UAVs follow a fixed circular trajectory, i.e., the scheme in [24], [25], [26].

4) Baseline4: All eavesdropping UAVs update their policies network as agents of the MAPPO algorithm just like the legitimate UAVs, i.e., the scheme in [28].

All four baseline schemes are based on the MAPPO algorithm for policy optimization of legitimate UAVs, differing only in the policy of the eavesdropping UAVs selected for training.

## B. Experimental Result

Fig. 3 shows the trend of the energy efficiency of IoT devices with the number of episodes during the training process of the proposed ARL-MAPPO algorithm. The red part of the curve represents legitimate UAVs as agents, while the blue part of the curve represents eavesdropping UAVs as agents. It can be seen that in the first phase (approximately 0 to 600 episodes), as the number of episodes increases, the parameters of the policy network of the legitimate UAVs are constantly updated and the energy efficiency of IoT devices is gradually improved. However, in the second phase (approximately 600 to 1000 episodes), the energy efficiency of IoT devices rapidly deteriorates as the parameters of the policy network of the eavesdropping UAVs are updated. In the subsequent phases, the energy efficiency of IoT devices continues to oscillate and gradually stabilize as the policy network parameters of the legitimate UAVs and the eavesdropping UAVs are updated alternately. In the final phase of training when the eavesdropping UAVs are agents, the worst case of the energy efficiency of IoT devices is also significantly improved, which indicates that the robustness of the policies learned by the legitimate UAVs is also improved.

<!-- image-->  
Fig. 3. The relationship between the energy efficiency of IoT devices and the number of episodes during the training phase of the proposed algorithm.

Fig. 4(a)â(c) show the trends of the average execution delay of the computational tasks, the average execution success rate, and the average energy consumption of the IoT devices with the number of training sets during the training of the proposed ARL-MAPPO algorithm, respectively. Similar to Fig. 3, the three metrics shake violently at first and then gradually stabilize as the policy network parameters of the legitimate and eavesdropping UAVs are updated alternately. In the final phase of training when the eavesdropping UAVs as agents, there is a significant reduction in the maximum average execution latency of the computational tasks, a significant increase in the minimum average execution success rate of the computational tasks, and a significant reduction in the average energy consumption of the IoT devices.

Fig. 5(a) and (b) show the 2D and 3D trajectories of legitimate and eavesdropping UAVs and the locations of IoT devices within one episode, respectively. It can be seen that the legitimate UAVs are trying to get as close as possible to the IoT devices to improve the quality of the links offloaded by their computation tasks, while trying to get as far as possible from the eavesdropping UAVs to reduce the quality of the eavesdropping links. This indicates that the policies of legitimate UAVs obtained by the proposed algorithm can make sensible and effective trajectory planning strategies based on incomplete observation information.

Then, in order to evaluate the worst-case energy efficiency of the IoT devices when the policies of the legitimate UAVs obtained in the training phase of the four baseline algorithms are fighting against intelligent eavesdropping UAVs, we switch perspectives, fix the parameters of the policy network of the legitimate UAVs, and consider the eavesdropping UAVs as agents of the MAPPO algorithm and adjust their policy network parameters with the aim of minimizing the energy efficiency of the IoT devices. This approach allows us to simulate the worst-case behavior of intelligent eavesdropping UAVs in adversarial environments, thus allowing us to critically evaluate the policies of legitimate UAVs and ensure that their IoT devices remain highly energy efficient in the face of potential eavesdropping threats. Through this approach, we are able to thoroughly evaluate and optimize the policies of legitimate UAVs for challenges that may be encountered in real-world operations. In the training phase of the proposed algorithm, the phase in which the eavesdropping UAVs are used as agents of MAPPO (the blue curved part of Fig. 3) is essentially the same as the evaluation phase described above. Therefore, it is reasonable and consistent to consider the stage of eavesdropping UAVs as agents at the end of the algorithmâs training as the evaluation phase, which ensures the validity of the evaluation results and the robustness of the policies.

Fig. 6(a)â(d) shows the curves that the average energy efficiency of IoT devices in the training phase and the evaluation phase of the four baseline algorithms changes with the increase of the number of episodes, respectively. In addition, we specifically intercepted the data from the first 2000 training episodes in which the proposed scheme in Fig. 3 average energy efficiency curves of IoT devices during the training process. This part of the data is plotted separately in Fig. 6(e) to facilitate a more rigorous and intuitive comparison with the baseline schemes. In the training phase (red part of the curve), the four baseline algorithms update the parameters of the policy network of the legitimate UAVs according to their own training methods, respectively. In the evaluation phase (blue part of the curve), we fix the parameters of the obtained legitimate UAVsâ policy network and take the eavesdropping UAVs as agents of MAPPO to optimize the parameters of their policy network with the goal of minimizing the energy efficiency of IoT devices.

It can be seen that Baseline1, Baseline2, and Baseline3 are able to converge to the satisfactory energy efficiency of IoT devices during the training phase as the policy of the legitimate UAVs is optimized when the eavesdropping UAVsâ policy is fixed. However, the energy efficiency of IoT devices of these three algorithms decreased dramatically during the evaluation phase as the policy of the eavesdropping UAVs was optimized. This is because, during the legitimate UAVsâ policy learning process of the three algorithms, the policies of the eavesdropping UAVsâ trajectory planning are fixed, so their learned policies all over-fit the policies of the eavesdropping UAVs in training. When the eavesdropping UAVsâ policies change in the evaluation phase, the learned legitimate UAVsâ policies cannot be adapted to the new eavesdropping UAVsâ policies. Although the energy efficiency of IoT devices of the Baseline4 algorithm and the proposed algorithm also decreased during the evaluation phase, the reduction was smaller. This is because the trajectory planning policies of the eavesdropping UAVs are dynamically changing during the policy learning process of the legitimate UAVs, which can alleviate the overfitting problem to some extent. Compared with the four baseline algorithms, the proposed algorithm has the smallest reduction in the energy efficiency of IoT devices in the evaluation phase, and the minimum energy efficiency of IoT devices is the maximum, which indicates the obvious advantages of the proposed algorithm.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 4. The relationship between execution delay, execution success rate of the computational tasks, and energy consumption of IoT devices and the number of episodes during the training phase of the proposed algorithm. (a) Execution delay. (b) Execution success rate. (c) Energy consumption.

TABLE II  
PERFORMANCE OF THE PROPOSED ALGORITHM FOR SCENARIOS WITH DIFFERENT NUMBERS OF LEGITIMATE UAVS
<table><tr><td>Number of legitimateUAVs</td><td>Energyefficiency</td><td>Execution delay/s</td><td>Energyconsumption/MJ</td><td>Execution successrate</td></tr><tr><td>1</td><td>24.94</td><td>0.0561</td><td>0.5213</td><td>0.610</td></tr><tr><td>2</td><td>28.52</td><td>0.0502</td><td>0.4932</td><td>0.673</td></tr><tr><td>3</td><td>30.74</td><td>0.0425</td><td>0.4458</td><td>0.712</td></tr><tr><td>4</td><td>31.56</td><td>0.0385</td><td>0.4133</td><td>0.756</td></tr><tr><td>5</td><td>32.41</td><td>0.0371</td><td>0.4012</td><td>0.802</td></tr></table>

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 5. The trajectories of legitimate UAVs and eavesdropping UAVs and the location of IoT devices within an episode. (a) 2D. (b) 3D.

To further investigate the impact of the number of eavesdropping UAVs on the performance of the proposed algorithm and the four baseline algorithms, Fig. 7(a)â(e) show the average energy efficiency of IoT devices of the proposed algorithm and the four baseline algorithms when training and evaluation with different numbers of eavesdropping UAVs, respectively. It can be seen that as the number of eavesdropping UAVs increases, the average energy efficiency of IoT devices during training and evaluation of all five algorithms gradually decreases. In the scenario with different numbers of eavesdropping UAVs, the four baselines have a higher average energy efficiency of IoT devices during training, whereas the average energy efficiency of IoT devices during evaluation decreased significantly. However, the proposed algorithm has a higher average energy efficiency of IoT devices for computational tasks during training and evaluation, and a smaller decrease in energy efficiency of IoT devices during evaluation. In addition, in the scenario with different numbers of eavesdropping UAVs, the proposed algorithm has a significant advantage in the average energy efficiency of IoT devices during evaluation.

Finally, the performance of the proposed algorithm is shown for scenarios with different numbers of legitimate UAVs in Table II. It can be seen that as the number of legitimate UAVs increases, the average energy efficiency of IoT devices gradually increases, while the average execution delay of the computational tasks decreases, the average execution success rate increases, and the average energy consumption of IoT devices decreases. This is because as the number of legitimate UAVs increases, the total communicable coverage area for legitimate UAVs becomes larger and more IoT devices can be covered. In addition, as the number of legitimate UAVs increases, each legitimate UAV can focus on only a smaller area of IoT devices so that the energy efficiency of the IoT devices is better, which means that the flight energy consumption of the legitimate UAVs is significantly reduced to the extent that more energy can be used by the legitimate UAVs to send artificial interference noise, so there is a significant increase in the secure data transmission rate between the IoT devices and the legitimate UAVs.

In conclusion, the proposed ARL-MAPPO based scheme compared to the baseline schemes has slower convergence and higher training costs though. However, the proposed scheme is advantageous in the fact that it can give the best performance in fighting against intelligent eavesdropping UAVs, i.e., it can achieve the highest worst-case energy efficiency of IoT devices. This indicates that the proposed algorithm performs best against potential eavesdropping threats and can ensure that IoT devices can be highly energy efficient even in the worst-case scenario. Moreover, the working cost of the proposed scheme and the baseline schemes is the same after actual deployment, i.e., all legitimate UAVs can make decisions using only the policy network, and the benefit after actual deployment is much higher than the training cost. Therefore, the algorithm scheme is more superior and effective compared to the baseline schemes.

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

Fig. 6. The relationship between the energy efficiency of IoT devices and the number of episodes during the training (legitimate UAVs as agents) and evaluation phases (eavesdropping UAVs as agents) of the four baseline algorithms. (a) Baseline1. (b) Baseline2. (c) Baseline3. (d) Baseline4. (e) ARL-MAPPO.  
<!-- image-->  
(a)

<!-- image-->

<!-- image-->  
(b)

<!-- image-->  
(d)

<!-- image-->  
(e)  
Fig. 7. The average energy efficiency of IoT devices during training and evaluation of the proposed algorithm and four baseline algorithms for different numbers of eavesdropping UAV scenarios. (a) With 1 eavesdropping UAV. (b) With 2 eavesdropping UAVs. (c) With 3 eavesdropping UAVs. (d) With 4 eavesdropping UAVs. (e) With 5 eavesdropping UAVs.

## V. CONCLUSION

In this paper, we consider the problem of secure computational offloading in a realistic multi-UAV-enabled MEC scenario with the presence of multiple intelligent eavesdropping UAVs. The optimization objective of the system is to obtain the optimal policy for legitimate UAVs that maximizes the worst-case energy efficiency of IoT devices in the fight against intelligent eavesdropping UAVs. To solve this max-min problem, we propose a solution based on adversarial multi-agent reinforcement learning with MAPPO as the base algorithm, namely ARL-MAPPO. In the proposed scheme, the legitimate UAVs and the eavesdropping UAVs alternate as agents of MARL to optimize their policies with the objectives of maximizing and minimizing the energy efficiency of IoT devices, respectively. Simulation experiments show that the proposed scheme has a significant advantage over the four baseline schemes in dealing with the intelligent eavesdropping problem. Specifically, compared to the four baseline scenarios, the policies for legitimate UAVs obtained by the proposed algorithms in this paper have the highest worst-case energy efficiency of IoT devices when fighting against intelligent eavesdropping drones in scenarios with varying numbers of legitimate UAVs and eavesdropping UAVs. In addition, secure computational offloading against intelligent eavesdropping is a relevant and challenging topic, which is currently not sufficiently researched. To this end, this paper proposes an adversarial multi-agent reinforcement learning-based scheme, in which legitimate UAVs and eavesdropping UAVs are allowed to act as agents of MARL alternately to optimize their respective policies, which provides an efficient and feasible solution to the problem of anti-intelligent eavesdropping.

## REFERENCES

[1] P. Ranaweera, A. D. Jurcut, and M. Liyanage, âSurvey on multi-access edge computing security and privacy,â IEEE Commun. Surv. Tut., vol. 23, no. 2, pp. 1078â1124, Second Quarter 2021.

[2] W. Saad, M. Bennis, and M. Chen, âA vision of 6G wireless systems: Applications, trends, technologies, and open research problems,â IEEE Netw., vol. 34, no. 3, pp. 134â142, May/Jun. 2020.

[3] C. W. Zaw, N. H. Tran, Z. Han, and C. S. Hong, âRadio and computing resource allocation in co-located edge computing: A generalized nash equilibrium model,â IEEE Trans. Mobile Comput., vol. 22, no. 4, pp. 2340â 2352, Apr. 2023.

[4] H. Wang, H. Zhang, X. Liu, K. Long, and A. Nallanathan, âJoint UAV placement optimization, resource allocation, and computation offloading for THz band: A DRL approach,â IEEE Trans. Wirel. Commun., vol. 22, no. 7, pp. 4890â4900, Jul. 2023.

[5] H. Djigal, J. Xu, L. Liu, and Y. Zhang, âMachine and deep learning for resource allocation in multi-access edge computing: A survey,â IEEE Commun. Surveys Tut., vol. 24, no. 4, pp. 2449â2494, Fourth Quarter 2022.

[6] M. Mozaffari, A. T. Z. Kasgari, W. Saad, M. Bennis, and M. Debbah, âBeyond 5G with UAVs: Foundations of a 3D wireless cellular network,â IEEE Trans. Wirel. Commun., vol. 18, no. 1, pp. 357â372, Jan. 2019.

[7] Y. Zeng, R. Zhang, and T. J. Lim, âWireless communications with unmanned aerial vehicles: Opportunities and challenges,â IEEE Commun. Mag., vol. 54, no. 5, pp. 36â42, May 2016.

[8] F. Zhou, R. Q. Hu, Z. Li, and Y. Wang, âMobile edge computing in unmanned aerial vehicle networks,â IEEE Wirel. Commun., vol. 27, no. 1, pp. 140â146, Feb. 2020.

[9] Y. Mao, C. You, J. Zhang, K. Huang, and K. B. Letaief, âA survey on mobile edge computing: The communication perspective,â IEEE Commun. Surveys Tut., vol. 19, no. 4, pp. 2322â2358, Fourth Quarter 2017.

[10] Y. C. Hu, M. Patel, D. Sabella, N. Sprecher, and V. Young, âMobile edge computingâa key technology towards 5G,â ETSI White Paper, vol. 11, no. 11, pp. 1â16, 2015.

[11] Y. Sun, N. Li, and X. Tao, âPrivacy preserved secure offloading in the multi-access edge computing network,â in Proc. IEEE Wirel. Commun. Netw. Conf. Workshops, 2021, pp. 1â6.

[12] H. Peng and X. Shen, âMulti-agent reinforcement learning based resource management in MEC- and UAV-assisted vehicular networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 1, pp. 131â141, Jan. 2021.

[13] S. Hwang, H. Lee, J. Park, and I. Lee, âDecentralized computation offloading with cooperative UAVs: Multi-agent deep reinforcement learning perspective,â IEEE Wirel. Commun., vol. 29, no. 4, pp. 24â31, Aug. 2022.

[14] Z. Ren et al., âIntelligent adaptive gossip-based broadcast protocol for UAV-MEC using multi-agent deep reinforcement learning,â IEEE Trans. Mobile Comput., vol. 23, no. 6, pp. 6563â6578, Jun. 2024.

[15] U. A. Khan, W. Khalid, and S. Saifullah, âEnergy efficient resource allocation and computation offloading strategy in a UAV-enabled secure edge-cloud computing system,â in Proc. IEEE Int. Conf. Smart Internet Things, 2020, pp. 58â63.

[16] S. Goel and R. Negi, âGuaranteeing secrecy using artificial noise,â IEEE Trans. Wirel. Commun., vol. 7, no. 6, pp. 2180â2189, Jun. 2008.

[17] G. Zheng, I. Krikidis, J. Li, A. P. Petropulu, and B. Ottersten, âImproving physical layer secrecy using full-duplex jamming receivers,â IEEE Trans. Signal Process., vol. 61, no. 20, pp. 4962â4974, Oct. 2013.

[18] Y.-S. Shiu, S. Y. Chang, H.-C. Wu, S. C.-H. Huang, and H.-H. Chen, âPhysical layer security in wireless networks: A tutorial,â IEEE Wirel. Commun., vol. 18, no. 2, pp. 66â74, Apr. 2011.

[19] Y. Zhang, Z. Mou, F. Gao, J. Jiang, R. Ding, and Z. Han, âUAV-enabled secure communications by multi-agent deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 11 599â11 611, Oct. 2020.

[20] H. Yang, S. Liu, L. Xiao, Y. Zhang, Z. Xiong, and W. Zhuang, âLearningbased reliable and secure transmission for UAV-RIS-assisted communication systems,â IEEE Trans. Wirel. Commun., vol. 23, no. 7, pp. 6954â6967, Jul. 2024.

[21] H. Yang, Z. Xiong, J. Zhao, D. Niyato, L. Xiao, and Q. Wu, âDeep reinforcement learning-based intelligent reflecting surface for secure wireless communications,â IEEE Trans. Wirel. Commun., vol. 20, no. 1, pp. 375â 388, Jan. 2021.

[22] H. Wu, H. Li, Z. Wei, N. Zhang, and X. Tao, âSecrecy performance analysis of air-to-ground communication with UAV jitter and multiple random walking eavesdroppers,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 572â584, Jan. 2021.

[23] J. Tang, G. Chen, and J. P. Coon, âSecrecy performance analysis of wireless communications in the presence of UAV jammer and randomly located UAV eavesdroppers,â IEEE Trans. Inf. Forensics Secur., vol. 14, no. 11, pp. 3026â3041, Nov. 2019.

[24] C. Wen, L. Qiu, and X. Liang, âSecuring UAV communication with mobile UAV eavesdroppers: Joint trajectory and communication design,â in Proc. IEEE Wirel. Commun. Netw. Conf., 2021, pp. 1â6.

[25] Z. Zhu, G. Su, B. Chen, M. Dai, X. Lin, and H. Wang, âJoint trajectory and power control for secure dual-UAV communications against air and ground eavesdropping,â in Proc. 31st Wirel. Opt. Commun. Conf., 2022, pp. 175â180.

[26] D. Guo, L. Tang, X. Zhang, and Y.-C. Liang, âJoint optimization of trajectory and jamming power for multiple UAV-aided proactive eavesdropping,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 5770â5785, May 2024.

[27] A. V. Savkin, H. Huang, and W. Ni, âSecuring UAV communication in the presence of stationary or mobile eavesdroppers via online 3D trajectory planning,â IEEE Wirel. Commun. Lett., vol. 9, no. 8, pp. 1211â1215, Aug. 2020.

[28] C. Wen, Y. Fang, and L. Qiu, âSecuring UAV communication based on multi-agent deep reinforcement learning in the presence of smart UAV eavesdropper,â in Proc. IEEE Wirel. Commun. Netw. Conf., 2022, pp. 1164â1169.

[29] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction. Cambridge, MA, USA: MIT Press, 2018.

[30] V. Mnih et al., âPlaying atari with deep reinforcement learning,â 2013, arXiv:1312.5602.

[31] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, âProximal policy optimization algorithms,â 2017, arXiv: 1707.06347.

[32] R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, and I. Mordatch, âMulti-agent actor-critic for mixed cooperative-competitive environments,â 2017, arXiv: 1706.02275.

[33] P. Sunehag et al., âValue-decomposition networks for cooperative multiagent learning,â 2017, arXiv: 1706.05296.

[34] D. Hernandez et al., âA generalized framework for self-play training,â in Proc. IEEE Conf. Games, 2019, pp. 1â8.

[35] D. Han and T. Shi, âSecrecy capacity maximization for a UAV-assisted MEC system,â China Commun., vol. 17, no. 10, pp. 64â81, 2020.

[36] X. Li, Y. Qin, J. Huo, and W. Huangfu, âComputation offloading and trajectory planning of multi-UAV-enabled MEC: A knowledge-assisted multiagent reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 73, no. 5, pp. 7077â7088, May 2024.

[37] H. Peng and X. Shen, âMulti-agent reinforcement learning based resource management in MEC-and UAV-assisted vehicular networks,â IEEE J. Select. Areas Commun., vol. 39, no. 1, pp. 131â141, Jan. 2021.

[38] N. N. Ei, S. W. Kang, M. Alsenwi, Y. K. Tun, and C. S. Hong, âMulti-UAV-assisted MEC system: Joint association and resource management framework,â in Proc. IEEE Int. Conf. Inf. Netw., 2021, pp. 213â218.

[39] X. Chen, H. Zhang, C. Wu, S. Mao, Y. Ji, and M. Bennis, âOptimized computation offloading performance in virtual edge computing systems via deep reinforcement learning,â IEEE Internet Things J., vol. 6, no. 3, pp. 4005â4018, Jun. 2019.

[40] C. Yu, A. Velu, E. Vinitsky, Y. Wang, A. M. Bayen, and Y. Wu, âThe surprising effectiveness of MAPPO in cooperative, multi-agent games,â vol. abs/2103.01955, 2021. [Online]. Available: https://api. semanticscholar.org/CorpusID:263870652

[41] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel, âHighdimensional continuous control using generalized advantage estimation,â 2015, arXiv:1506.02438.

<!-- image-->  
Xulong Li (Student Member, IEEE) is currently working toward the PhD degree in information and communication engineering with the School of Computer and Communication Engineering, University of Science and Technology Beijing (USTB). His current research interests include mobile edge computing, the Internet of Things, and deep reinforcement learning.

<!-- image-->  
Wei Huangfu (Member, IEEE) received the MS and PhD degrees in electronic engineering from Tsinghua University, Beijing, China in 1998 and 2001, respectively. He is currently a full professor with the School of Computer and Communication Engineering, the University of Science and Technology Beijing (USTB). His main research interests include statistical signal processing, the Internet of Things, cooperative communications networks, and wireless sensor network.

<!-- image-->

<!-- image-->

Xinyi Xu received the BS degree in electronic science and technology from Xidian University, China, in 2014 and the PhD degree from the School of Electronic Engineering, Xidian University, China, in 2021. Currently, she is working as an associate professor with the School of Computer and Communication Engineering, University of Science and Technology Beijing, China. Her research interests include computer vision, machine learning, and the applications of deep learning.

Jiahao Huo received the PhD degree from the University of Science and Technology Beijing, in 2019. He is currently a lecturer with the University of Science and Technology Beijing. His research interests include high-capacity IM/DD systems for optical interconnect, UAV secure communication, and digital signal processing techniques for advanced modulation formats.

<!-- image-->

Keping Long (Senior Member, IEEE) received the MS and PhD degrees in electric circuit and system from University of Electronic Science and Technology of China (UESTC), Chengdu, China in 1995 and 1998, respectively. He is currently a professor with the School of Computer and Communication Engineering, the University of Science and Technology Beijing (USTB). His main research interests include statistical signal processing, channel estimation in multiple-input multiple-output (MIMO) orthogonal frequency division multiplexing (OFDM) systems, cooperative communications and computer networks.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp/page_7_img_1.png|page_7_img_1]]
3. [[../extracted_images/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp/page_13_img_1.png|page_13_img_1]]
4. [[../extracted_images/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp/page_15_img_1.jpeg|page_15_img_1]]
5. [[../extracted_images/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp/page_15_img_2.jpeg|page_15_img_2]]
6. [[../extracted_images/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp/page_15_img_3.jpeg|page_15_img_3]]
7. [[../extracted_images/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp/page_15_img_4.jpeg|page_15_img_4]]
8. [[../extracted_images/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp/page_15_img_5.jpeg|page_15_img_5]]

---

