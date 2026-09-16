# Multi-Agent Reinforcement Learning in Adversarial Game Environments: Personalized Anti-Interference Strategies for Heterogeneous UAV Communication

Yeguang Qin , Graduate Student Member, IEEE, Jie Tang , Graduate Student Member, IEEE, Fengxiao Tang , Senior Member, IEEE, Ming Zhao , Member, IEEE, and Nei Kato , Fellow, IEEE

AbstractâExisting anti-jamming strategies for unmanned aerial vehicle (UAV) networks largely assume homogeneity among UAVs, neglecting the differences in hardware configurations, task requirements, and environmental adaptability. In the face of such heterogeneity, these strategies often fail to effectively counter intelligent jamming and co-channel interference. To address this issue, this paper proposes an intelligent anti-jamming framework designed specifically for the heterogeneous UAV network, allowing each UAV to autonomously adjust its transmission channel and power based on its hardware capabilities and task requirements in a distributed environment. This aims to optimize communication efficiency and reduce energy consumption. We formulate the anti-jamming problem as an adversarial game and confirm the existence of a unique equilibrium point within this model. Moreover, we introduce the novel Personalized Federated Soft Actor-Critic (PFSAC) algorithm, which combines the global model with local models to customize personalized anti-jamming strategies for each UAV, significantly enhancing network performance in complex jamming environments. Simulation results indicate that compared to other methods, our proposed algorithm significantly enhances the anti-jamming capability of heterogeneous UAV networks and performs better than them.

Index TermsâUnmanned aerial vehicle, personalized federated learning, reinforcement learning, anti-jamming.

## I. INTRODUCTION

networks [1], [2], [3], [4] perform critical tasks such as monitoring, rescue, and logistics distribution. Their performance heavily depends on the stability and reliability of the communication system. Malicious interference can weaken signal strength or increase environmental noise, thus reducing the signal-to-interference-plus-noise ratio (SINR) and severely impacting communication quality. Therefore, developing efficient anti-jamming techniques to ensure the communication reliability of UAV networks in various environments has become a significant challenge.

Traditional anti-jamming strategies rely on predefined interference patterns and fixed response strategies, including spectrum sensing, frequency hopping, and [5], [6]. However, the high mobility of UAVs and the unpredictability of interference sources pose significant challenges. Traditional strategies often struggle with incomplete channel information. To overcome these limitations, reinforcement learning (RL) techniques have been proposed as an innovative solution. By continuously interacting with the environment, RL techniques can gradually learn and adapt to changing environmental conditions, significantly enhancing the anti-jamming capabilities of UAV networks in complex environments. Although single-agent RL algorithms have been explored in [7], [8], [9], [10], [11], [12], [13], the increasing action-state space may hinder their effective convergence, thereby limiting their applicability in solving complex multi-agent anti-jamming problems. Moreover, relying on a single centralized control to coordinate the actions of multiple agents is impractical, as it increases communication delays and significantly raises communication overhead.

In multi-UAV communication anti-jamming scenarios, each UAV needs to adjust its behavior to adapt to environmental changes and infer the behavioral strategies of other UAVs. Without central control, UAVs might unintentionally select the same communication channels, leading to mutual interference. Independent training multi-agent reinforcement learning (MARL) provides a framework where each agent relies solely on local information for independent decision-making [14], [15]. However, the lack of information sharing among agents may hinder the formation of effective collaborative strategies.

Federated learning (FL), as a privacy-preserving collaborative machine learning paradigm, has garnered significant attention across various fields in recent years. By enabling local training and aggregating model parameters, FL allows for the construction of a global model without the need for data sharing, providing an effective solution for addressing anti-jamming communication challenges in UAV networks operating in dynamic and complex network environments [17]. However, due to the diversity in environmental conditions, hardware capabilities, and task requirements, the communication needs of individual UAVs may differ. Therefore, it is crucial to develop personalized anti-jamming strategies for each UAV to better adapt to the changing environment. Additionally, game theory has become an essential mathematical framework for modeling the complex dependencies between strategic network entities and analyzing their optimal interaction strategies. The Stackelberg game is particularly well-suited for describing the sequential interactions between wireless users and intelligent jammers. In this framework, the jammer acts as the leader, initiating interference attacks first, while wireless users, as followers, respond by optimizing resource allocation in multiple domains [8], [18], [19], [20], [21], [22], [23] such as power, time, frequency, and beam to adjust their anti-jamming communication strategies effectively and counter the interference.

In this paper, we model the anti-intelligent jamming problem in heterogeneous UAV networks as a stochastic Stackelberg game and propose a personalized federated reinforcement learning algorithm to address this issue. We focus on UAV-UAV communication [24], [25], considering both their collaboration and competition. The primary contributions of this paper are summarized as follows:

For the first time, we consider the heterogeneity of UAVs in the study of UAV anti-jamming communication networks. We have developed a theoretical framework based on stochastic Stackelberg games, where the jammer assumes the role of the leader, initiating jamming attacks, while the heterogeneous UAV network functions as the follower, enabling communication between UAV pairs.

We propose an innovative Personalized Federated Soft Actor-Critic (PFSAC) algorithm, which enables UAVs to integrate the global model parameters downloaded from the central server with their local models. This fusion strategy allows each UAV to implement personalized decisions based on its specific needs and configurations in complex communication environments, thereby substantially enhancing anti-jamming performance.

To verify the performance of our proposed algorithm, we compared it with other deep RL-based methods, including Federated SAC (FSAC), FD3PG [26], Independent SAC (ISAC), and Independent Deep Q-network (IDQN) [27]. Simulation results indicate that the proposed PFSAC effectively enables UAV pairs in heterogeneous UAV networks to collaboratively select appropriate channels and power levels for anti-jamming.

The remainder of this paper is organized as follows. Section II presents the related work. In Section III, we describe the system model and formulate the problem. Section IV formulates the strategic dynamics between the jammer and the heterogeneous UAV network within a stochastic Stackelberg game framework and introduces the PFSAC algorithm as a solution to this game. Simulation results are provided in Section V, followed by conclusions in Section VI. Additionally, the main notations are summarized in Table I.

<table><tr><td>Notations</td><td>Definitions</td></tr><tr><td> $\mathcal { N }$ </td><td>The set of UAV pairs.</td></tr><tr><td> $\mathcal { K }$ </td><td>The set of jammers.</td></tr><tr><td> $\mathcal { M }$ </td><td>The set of tasks.</td></tr><tr><td> $\mathcal { C }$ </td><td>The set of channels.</td></tr><tr><td> $d _ { \mathrm { t x , r x } }$ </td><td>The distance between transmitter tx and receiver rx. The channel power gain from transmitter tx to</td></tr><tr><td> $g _ { \mathrm { t x , r x } }$ </td><td>receiver rx.</td></tr><tr><td> $B$ </td><td>The bandwidth of each channel.</td></tr><tr><td> $c _ { n }$ </td><td>The channel used by UAV pair n.</td></tr><tr><td> $c _ { k }$ </td><td>The channel used by jammer k.</td></tr><tr><td> $\smash { \ddot { P } } ^ { U }$   $\smash { \overset { \boldsymbol { \cdot } } { \boldsymbol { \mathbf { \mathit { r } } } } } _ { 0 } ^ { n }$ </td><td>The transmit power of UAV pair n.</td></tr><tr><td> $P _ { k } ^ { J }$ </td><td>The transmit power of jammer k.</td></tr><tr><td> $P _ { \operatorname* { m i n } , n } ^ { U } , P _ { \operatorname* { m a x } , n } ^ { U }$ </td><td>The minimum and maximum power of UAV</td></tr><tr><td> $V _ { n } ^ { U } , V ^ { J }$ </td><td>pairs n. The total power levels of UAV pair n and jammers.</td></tr><tr><td> $v _ { n } , v _ { k }$ </td><td>The selected power level of UAV pair n and</td></tr><tr><td> $\mathrm { S I N R } _ { n }$ </td><td>jammer k. The SINR of UAV pair n.</td></tr><tr><td> ${ \mathrm { R a t e } } _ { n }$ </td><td>The rate of UAV pais n.</td></tr><tr><td> $\mathrm { R a t e } _ { n } ^ { t h }$ </td><td>The rate threshold of UAV pair n.</td></tr></table>

TABLE I MAIN NOTATIONS

## II. RELATED WORK

## A. Traditional Anti-Jamming

Wu et al. [5] proposed an algorithm that integrates block coordinate descent (BCD) and successive convex approximation (SCA) techniques to optimize UAV trajectories and transmission power, significantly increasing end-to-end throughput and enhancing system performance in environments with malicious interference. Zhang et al. [28] introduced a cooperative antijamming scheme that enhances the quality of interfered links in distributed environments by adjusting channel access probabilities and employing multiple-input single-output (MISO) techniques. A multi-domain anti-jamming strategy that combines Stackelberg game theory with an exponential distribution genetic algorithm was presented in [29], which greatly improves the performance of amplify-and-forward relay systems in intelligent jamming environments by optimizing frequency hopping speed and transmission power. Yang et al. [18] further explored interference defence mechanisms against intelligent jammers by proposing an algorithm that calculates optimal transmission power and jamming response strategies; their simulations validated the effectiveness of this theoretical framework. Xu et al. [30] addressed the anti-jamming transmission problem in UAV communication networks under conditions of incomplete information and co-channel interference by modeling it as a Bayesian Stackelberg game, developing a subgradient Bayesian Stackelberg iterative algorithm that efficiently customizes power control strategies for both jammers and users. However, these traditional algorithms often rely on idealized environmental assumptions that do not fully account for the complexities of real-world scenarios, such as incomplete information, channel state uncertainty, and multi-user interference.

## B. Intelligent Anti-Jamming

Intelligent anti-jamming algorithms can learn from environmental interactions, allowing them to adapt to complex conditions with unknown information. Jia et al. [7] explored the application of discrete power adjustment strategies in combating intelligent jamming by establishing a Stackelberg game model. They developed a hierarchical power control algorithm based on single-agent Q-learning to optimize the dynamic interaction between users and jammers. In another study [12], a deep neural network (DNN)-based Stackelberg game framework was proposed to optimize power allocation for intelligent jammers and cluster head nodes under both single-channel and multichannel conditions, defending against intelligent jamming attacks on computation task offloading links. However, using a single-agent centralized coordinator to control multiple users may lead to the curse of dimensionality, as the action space significantly expands with an increasing number of agents. Han et al. [14] propose a distributed dynamic anti-jamming scheme based on a hierarchical anti-jamming Stackelberg game and selflearning algorithms, effectively reducing energy consumption and improving performance in satellite-enabled army Internet of Things (SaIoT) under intelligent jamming environments. Li et al. [16] developed an adaptive strategy based on a DQN to address the challenges posed by intelligent jammers. This strategy allows for effective anti-jamming measures to be implemented directly in the frequency and power domains through independent decision-making by multiple agents. These studies propose multi-agent anti-jamming algorithms where each agent independently trains its model and treats other agents as part of the environment. However, the lack of an effective informationsharing mechanism limits the cooperative capabilities among agents, making it difficult to achieve global optimization goals. Yin et al. [17] proposed a novel UAV network anti-intelligent jamming framework by integrating the DQN algorithm with FL, enabling UAVs to adaptively adjust channels and power in a distributed environment. Although FL effectively facilitates information exchange between multiple agents, this federated reinforcement learning (FRL) research has not yet fully considered the heterogeneity issue faced by UAV communication networks.

## III. SYSTEM MODEL

We consider a heterogeneous UAV network consisting of multi-UAVs and intelligent jammers. In this network, UAVs are organized into coalitions to collaboratively execute various tasks. Each UAV is assigned a specific task, after which it establishes a communication link with the coalition leader to transmit task-related information, thereby forming UAV pairs, as illustrated in Fig. 1. There exist N UAV pairs, represented by the set $\mathcal { N } \triangleq \{ 1 , 2 , \dots , N \}$ . The set of jammers is denoted by ${ \mathcal { K } } \triangleq \{ 1 , 2 , \dots \dots , K \}$ . The number of tasks is M , with the set of tasks is denoted by $\mathcal { M } \triangleq \{ 1 , 2 , \dots , M \}$ . In this paper, 1 2UAVs are regarded as heterogeneous, with their heterogeneity primarily manifested in each UAV having different power ranges and power selections being discretized into different levels. Furthermore, as each task imposes specific transmission rate requirements, the system must ensure that each UAV meets the rate demands of its assigned tasks, e.g., the communication threshold of UAV pair n can be denoted as $\mathrm { R a t e } _ { n } ^ { t h }$ . The set of channels is denoted by ${ \mathcal { C } } \triangleq \{ 1 , 2 , \dots , C \}$ . Both UAVs and 1 2jammers share this set of channels, allowing the jammers to disrupt the transmission channels utilized by the UAVs.

<!-- image-->  
Fig. 1. The framework of the heterogeneous UAV anti-jamming network consists of N UAV pairs, K jammers and M tasks.

<!-- image-->  
Fig. 2. Illustration of the transmission slot structure.

As shown in Fig. 2, we illustrate a UAV pair n and an intelligent jammer k, each operating on its own time base [31]. In this system, time is discretized into specific time slots, represented as $t = 1 , 2 , \dots , T$ . UAVs are equipped with intelligent = 1 2capabilities for spectrum sensing, learning, and autonomous decision-making [32]. At the beginning of each discrete time slot t, UAV pair n performs spectrum sensing to measure its local channel state information (CSI), including the channel power gain $g _ { n , n } ( t )$ between its transmitter and receiver, as well ( )as interference levels $( I _ { n } ^ { U }$ and $I _ { n } ^ { J } )$ . This CSI is obtained through distributed, onboard sensing capabilities, eliminating the need for global or perfectly known CSI, which is often infeasible in dynamic UAV environments due to mobility and jamming [17]. Although real-time continuous CSI provides more accurate information, it is difficult to achieve continuous measurements in real UAV systems due to hardware performance and latency, so we used a periodic update of CSI [33]. Based on the sensing results, it then selects the appropriate transmission channels and power levels. Following this, UAV pair n transmits task information using the selected channels and transmission power. After completing the transmission, the UAV pair n moves to the next location, preparing to initiate a new communication task.

Considering the high mobility of UAVs, and based on [34] where the flight trajectory of UAVs is pre-designed, we represent the predetermined trajectory using a set of discrete threedimensional coordinates. We denote the transmitter and receiver as tx and rx, respectively. In the network, ordinary coalition members act as transmitters for the UAV pair, responsible for relaying data relevant to the task. Meanwhile, the coalition leader serves as the receiver for the UAV pair, specifically tasked with receiving data from the transmitters.

## A. Channel Model

We adopted a comprehensive path loss model that considers the effects of both line-of-sight (LoS) and non-line-ofsight (NLoS) links. Based on the standards of the International Telecommunication Union (ITU), it provides a detailed characterization of air-to-air and air-to-ground communication links, accounting for terrain, building structures, and weather conditions that impact signal propagation. The probability of establishing a LoS link is formulated as follows:

$$
\begin{array} { l } { \displaystyle \operatorname* { P r } \left( d _ { \mathrm { t x } , \mathrm { r x } } \right) } \\ { \displaystyle = \prod _ { \zeta = 0 } ^ { \chi } \left[ 1 - \exp \left( - \frac { \left[ H _ { \mathrm { t x } } - \frac { \left( \varsigma + 0 . 5 \right) \left( H _ { \mathrm { t x } } - H _ { \mathrm { r x } } \right) } { \chi + 1 } \right] ^ { 2 } } { 2 \mathrm { a } _ { 3 } ^ { 2 } } \right) \right] , } \end{array}\tag{1}
$$

where $d _ { \mathrm { t x , r x } }$ represents the distance between the transmitter tx and the receiver rx. $H _ { \mathrm { t x } }$ and $H _ { \mathrm { r x } }$ denote heights of the transmitter tx and receiver rx, respectively. The terms $\mathrm { a _ { 1 } , a _ { 2 } }$ , and 3 are environmental parameters and $\begin{array} { r } { \chi = \lfloor \frac { d _ { \mathrm { t x , r x } } \sqrt { \mathrm { a _ { 1 } a _ { 2 } } } } { 1 0 0 0 } - 1 \rfloor } \end{array}$ a. The =probability of establishing an NLoS link is given by:

$$
\begin{array} { r } { \stackrel { \mathrm { N L o S } } { \mathrm { P r } } \left( d _ { \mathrm { t x , r x } } \right) = 1 - \stackrel { \mathrm { L o S } } { \mathrm { P r } } \left( d _ { \mathrm { t x , r x } } \right) . } \end{array}\tag{2}
$$

The path loss $\Theta ( d _ { \mathrm { t x , r x } } )$ in this model can be expressed as:

$$
\Theta ( d _ { \mathrm { t x } , \mathrm { r x } } ) = \left\{ \begin{array} { l l } { D _ { \mathrm { L o S } } \times d _ { \mathrm { t x } , \mathrm { r x } } ^ { \delta _ { \mathrm { L o S } } } } & { \mathrm { w i t h ~ p r o b a b i l i t y ~ ( 1 ) } } \\ { D _ { \mathrm { N L o S } } \times d _ { \mathrm { t x } , \mathrm { r x } } ^ { \delta _ { \mathrm { N L o S } } } } & { \mathrm { w i t h ~ p r o b a b i l i t y ~ ( 2 ) } } \end{array} , \right.\tag{3}
$$

where $\delta _ { \mathrm { L o S } }$ and $\delta _ { \mathrm { N L o S } }$ are the path loss exponents for LoS and NLoS conditions, respectively. Similarly, $D _ { \mathrm { L o S } }$ and $D _ { \mathrm { N L o S } }$ denote the path loss coefficients per unit distance for each scenario. Consequently, the channel power gain, incorporating both the path loss model and Nakagami-m fading, can be formulated as:

$$
g _ { \mathrm { t x , r x } } = \frac { h _ { \mathrm { t x , r x } } } { \Theta ( d _ { \mathrm { t x , r x } } ) } ,\tag{4}
$$

where $h _ { \mathrm { t x , r x } }$ signifies the small-scale fading between the transmitter tx and receiver rx.

## B. Interference Model

In our heterogeneous UAV network, the UAV pair primarily considers interference from the co-channel transmissions of other UAVs and the disruptions from intelligent jammers.

When the UAV pair n communicates, its received co-channel interference is defined as follows:

$$
I _ { n } ^ { U } = \sum _ { m \in \mathcal { N } , m \ne n } g _ { m , n } P _ { n } ^ { U } \ d \mathbf { k } \{ c _ { m } = c _ { n } \} ,\tag{5}
$$

where $P _ { n } ^ { U }$ represents the transmission power of UAV pair n, $c _ { n }$ denotes the selected channel, and ${ \nVdash } _ { \{ c _ { m } = c _ { n } \} }$ is an indicator function that takes the value of 1 when UAV pair m and n are using the same channel, and 0 otherwise.

Similarly, the external malicious interference $I _ { n } ^ { J }$ to UAV pair n can be expressed as:

$$
I _ { n } ^ { J } = \sum _ { k \in \mathcal { K } } g _ { k , n } P _ { k } ^ { J } \mathbb { K } _ { \{ c _ { k } = c _ { n } \} } ,\tag{6}
$$

where $P _ { k } ^ { J }$ indicates the transmission power of jammer $k , c _ { k }$ is the channel, and $\nVdash _ { \{ c _ { k } = c _ { n } \} }$ is an indicator function.

## C. Communication Model

In this research, we propose a discretization technique for both transmission and jamming power across our framework, facilitating the segmentation of power into quantifiable increments. This method accounts for the inherent diversity among UAV pairs, with each UAV pair characterized by a distinct range of power levels, delineated by minimum and maximum thresholds, denoted as $P _ { \mathrm { m i n } } ^ { U }$ and $P _ { \mathrm { m a x } } ^ { \breve { U } }$ , respectively. Consequently, the transmission power of UAV pair n is discretized into $V _ { n } ^ { U }$ levels. The selected level $v _ { n } ,$ where $v _ { n } \in [ 0 , V _ { n } ^ { U } ]$ represents the chosen [0 ]power level and determines the specific transmission power, is calculated as follows:

$$
P _ { n } ^ { U } = P _ { \operatorname* { m i n } , n } ^ { U } + \frac { v _ { n } } { V _ { n } ^ { U } } ( P _ { \operatorname* { m a x } , n } ^ { U } - P _ { \operatorname* { m i n } , n } ^ { U } ) ,\tag{7}
$$

where $P _ { \operatorname* { m i n } , n } ^ { U }$ and $P _ { \operatorname* { m a x } , n } ^ { U }$ are the minimum and maximum power of UAV pair $n ,$ respectively.

Similarly, the jamming power is discretized into $V ^ { J }$ levels. The power level of the jammer $k , v _ { k }$ within the range $[ 0 , V ^ { J } ]$ ï¼ is given by:

$$
P _ { k } ^ { J } = P _ { \mathrm { m i n } } ^ { J } + \frac { v _ { k } } { V ^ { J } } \left( P _ { \mathrm { m a x } } ^ { J } - P _ { \mathrm { m i n } } ^ { J } \right) ,\tag{8}
$$

where $P _ { \operatorname* { m i n } } ^ { J }$ and $P _ { \operatorname* { m a x } } ^ { J }$ are the minimum and maximum power of the jammer $k ,$ respectively. The efficacy of the transmission power and the impact of jamming power are then incorporated into a combined channel and interference model to compute the SINR for the UAV pair n as follows:

$$
\mathrm { S I N R } _ { n } = \frac { P _ { n } ^ { U } g _ { n , n } } { I _ { n } ^ { U } + I _ { n } ^ { J } + N _ { 0 } } ,\tag{9}
$$

where $N _ { 0 }$ signifies the environment additive white Gaussian noise power. Subsequently, the attainable communication rate for UAV pair n is determined, encapsulating the bandwidth B efficiency of the system:

$$
\mathrm { R a t e } _ { n } = B \log _ { 2 } ( 1 + \mathrm { S I N R } _ { n } ) .\tag{10}
$$

The design of the network takes into account the needs of different missions, resulting in different communication thresholds between UAV pairs. We posit that UAV pairs allied within the same network share a standardized communication threshold. Moreover, the threshold communication rate, $\mathrm { R a t e } _ { n } ^ { t h }$ , acts as a pivotal criterion for determining the successful transmission between UAV pair n. A binary variable $\phi _ { n }$ is introduced to represent the communication outcome for UAV pair $n ,$ defined as:

$$
\phi _ { n } \triangleq \left\{ { \begin{array} { l l } { 1 , } & { \mathrm { R a t e } _ { n } \geq \mathrm { R a t e } _ { n } ^ { t h } , } \\ { 0 , } & { \mathrm { R a t e } _ { n } < \mathrm { R a t e } _ { n } ^ { t h } . } \end{array} } \right.\tag{11}
$$

Moreover, the impact of jammer kâs interference on UAV pair n is quantified through the binary variable $\eta ( c _ { k } , c _ { n } )$ , formulated as:

$$
\eta \left( c _ { k } , c _ { n } \right) = \left\{ \begin{array} { l l } { 1 , } & { c _ { k } = c _ { n } , \phi _ { n } = 0 , \forall n , } \\ { 0 , } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{12}
$$

## D. Problem Formulation

In the proposed framework, we develop an optimization problem for heterogeneous UAV networks. This problem is designed to pinpoint the most effective channel and power allocation strategies that not only maximize the overall network communication rates for the heterogeneous UAV network but also minimize the energy expended on transmissions. The optimization problem is formulated as follows:

$$
\begin{array} { r l } & { ( \mathcal { P } 1 ) : \displaystyle \operatorname* { m a x } _ { \{ c _ { n } , P _ { n } ^ { U } \forall n \} } \mathbb { E } \left[ \displaystyle \sum _ { n = 1 } ^ { N } ( \phi _ { n } \mathrm { R a t e } _ { n } - \beta _ { n } P _ { n } ^ { U } ) \right] } \\ & { \mathrm { s . t . } C 1 : \mathrm { R a t e } _ { n } \geq \mathrm { R a t e } _ { n } ^ { t h } , \forall n , } \\ & { C 2 : P _ { n } ^ { U } \in \left[ P _ { \operatorname* { m i n } , n } ^ { U } , P _ { \operatorname* { m a x } , n } ^ { U } \right] , \forall n , } \\ & { C 3 : c _ { n } \in \mathcal { C } , \forall n , } \end{array}\tag{13}
$$

where $\beta _ { n }$ denotes the transmission cost per unit power of the UAV pair n, constraint C ensures that UAV pairs 1achieve the requisite minimum communication rate. C and C 2define the power and channel constraints for each UAV pair $n ,$ respectively.

## IV. MULTI-AGENT RL-BASED ANTI-JAMMING COMMUNICATIONS

In this paper, we formulate a complex multi-leader, multifollower stochastic Stackelberg game that delineates the interactions between jammers and a heterogeneous network of UAVs. As illustrated in Fig. 3, the jammers initiate interference actions, and subsequently, the heterogeneous UAV network selects the optimal response to these actions. Drawing inspiration from [12] and [17], we model this interaction as an anti-intelligence jamming stochastic Stackelberg game, methodically encapsulated by the tuple $G = \left. \Gamma , S , \mathcal { A } , \mathcal { F } , r , \gamma \right.$

- $\Gamma = \{ \mathcal { K } , \mathcal { N } \}$ Î :represents the set of players, with K the set Î =of intelligent jammers as the leader, and $\mathcal { N }$ denotes the set of the heterogeneous UAV network as the followers.

State: The state space, denoted as $\boldsymbol { S } = \{ \boldsymbol { S } ^ { J } , \boldsymbol { S } ^ { U } \}$ , includes =all potential environmental conditions. The set $S ^ { J }$ represents the joint state of all jammers, which is constructed as the Cartesian product $\bar { \mathcal { S } } ^ { \bar { J } } = \otimes _ { k \in \mathcal { K } } \mathcal { S } _ { k } ^ { J }$ . At any given time slot t, the joint state of jammers is described by $\mathbf { s } ^ { J } ( t ) =$ $\otimes _ { k \in { \mathcal { K } } } s _ { k } ^ { J } ( t )$ . Here, ${ \bf s } _ { k } ^ { J } ( t )$ ( ) =includes both the results of prior ( )interactions, $\eta ( c _ { k } ( t - 1 ) , c _ { n } ( t - 1 ) )$ , and the current channel conditions $\{ g _ { k , n } ( t ) \} _ { n \in \mathcal { N } }$ 1)). The set $ { \boldsymbol { S } } ^ { U }$ represents the ( )joint state of all UAV pairs, denoted as $S ^ { U } = \otimes _ { n \in \mathcal { N } } S _ { n } ^ { U }$ ï¼ =which includes indicators of communication success or failure in the previous time slot and the channel states between each UAV transmitter and receiver. The term $\mathbf { s } ^ { U } ( t ) = \otimes _ { n \in \mathcal { N } } \mathbf { s } _ { n } ^ { U } ( t )$ represents the joint state of UAVs at ( ) =time t, where $\mathbf { s } _ { n } ^ { U } ( t ) = \{ \phi _ { n } ( t - 1 ) , g _ { n , n } ( t ) \} \forall n \in \mathcal { N }$

<!-- image-->  
Fig. 3. Illustration of the Stackelberg model.

( ) = ( 1) (- Action: The action sets, represented as $\overset { \triangledown } { \mathcal { A } } = \{ \mathcal { A } ^ { J } , \mathcal { A } ^ { U } \}$ =including all possible actions for jammers and the heterogeneous UAV network. For jammers, the action set $\mathcal { A } ^ { J }$ consists of the combined action sets of all jammers, represented as $\mathcal { A } ^ { J } = \otimes _ { k \in \mathcal { K } } \mathcal { A } _ { k } ^ { J }$ . At a particular time slot t, $\mathbf { a } ^ { J } ( t ) = \otimes _ { k \in \mathcal { K } } \mathbf { a } _ { k } ^ { J } ( t )$ , where ${ \mathbf { a } } _ { k } ^ { J } ( t )$ includes selections for ( ) = ( ) ( )channels and power levels, expressed as $\{ c _ { k } ( t ) , P _ { k } ^ { J } ( t ) \}$ }. ( )Conversely, for the heterogeneous UAV network, $A ^ { U }$ ( )denotes the joint action set, which is the Cartesian product of all UAV pairs actions, defined as $\mathcal { A } ^ { U } = \otimes _ { n \in \mathcal { N } } \mathcal { A } _ { n } ^ { U }$ . In =each given time slot t, the action for a UAV pair involves strategic selections of channel and power settings. Consequently, the aggregated action set for this slot denoted as $\bar { \mathbf { a } } ^ { U } ( t ) = \otimes _ { n \in \mathcal { N } } \mathbf { a } _ { n } ^ { U } ( t )$ , is constituted by ${ \bf a } _ { n } ^ { U } ( t )$ , defined as $\{ c _ { n } ( t ) , P _ { n } ^ { U } ( t ) \}$ ( )for each UAV pair n.

( ) ( )- Transition Probability: $\mathcal { F }$ represents the state transition probability function, which is contingent upon the actions executed by both jammers and UAV pairs.

- Reward: The rewards for the system are represented by $\boldsymbol { r } = \{ r ^ { J } , r ^ { U } \}$ . The jammersâ rewards, $r ^ { J } { } _ { ; }$ , are calculated as $\begin{array} { r } { \sum _ { k = 1 } ^ { K } \sum _ { n = 1 } ^ { N } \eta ( c _ { k } , c _ { n } ) \mathrm { R a t e } _ { n } - \sum _ { k = 1 } ^ { K } \beta _ { k } P _ { k } ^ { J } } \end{array}$ . Conversely, ( )the sum rewards of all UAV pairs can be denoted as $r ^ { U } =$ ${ \begin{array} { r l } { ~ } & { { } \sum _ { n = 1 } ^ { N } ( \phi _ { n } \mathbf { R a t e } _ { n } - \beta _ { n } P _ { n } ^ { U } ) } \end{array} }$

(- Discount Factor: $\gamma \in [ 0 , 1 ]$ denotes the discount factor, [0 1]which quantifies the significance of immediate versus future rewards.

## A. Equilibrium Analysis

Within the framework of stochastic Stackelberg games, this analysis elucidates the optimization processes undertaken by intelligent jammers to adjust their strategies to maximize expected cumulative rewards, formally expressed as $\pi ^ { \mathrm { J } } = \otimes \pi _ { k } ^ { \mathrm { J } }$ =Simultaneously, UAV pairs refine their anti-jamming strategies, represented as $\pi ^ { \mathrm { U } } = \otimes \pi _ { n } ^ { \mathrm { U } }$ , to maximize their aggregated =expected reward. The resolution of this game referred to as the Stackelberg Equilibrium (SE) [35], [36], indicates a state in which no player can unilaterally improve their payoff by adjusting their strategy independently.

Definition 1: In the Stackelberg framework, the strategy pair $( \pi _ { * } ^ { J } , \bar { \pi } _ { * } ^ { U } )$ achieves SE, if and only if no player can increase ( )their respective reward by unilaterally altering their strategy. Mathematically, this condition is represented by:

$$
\begin{array} { r } { \hat { r } ^ { J } ( \pi _ { * } ^ { J } , \pi _ { * } ^ { U } ) \geq \hat { r } ^ { J } ( \pi ^ { J } , \pi _ { * } ^ { U } ) , } \\ { \hat { r } ^ { U } ( \pi _ { * } ^ { J } , \pi _ { * } ^ { U } ) \geq \hat { r } ^ { U } ( \pi _ { * } ^ { J } , \pi ^ { U } ) . } \end{array}\tag{14}
$$

The strategic configurations $\pi _ { * } ^ { J }$ and $\pi _ { * } ^ { U }$ of intelligent jammers and UAV pairs represent a SE within the context of the described stochastic Stackelberg game.

## B. PFSAC-Based Anti-Jamming Algorithm

The solution to the SE problem in anti-jamming games for dynamically, heterogeneous UAV networks, characterized by uncertain channel states and unpredictable jamming strategies, presents a significant challenge. We propose a model-free, multiagent reinforcement learning approach, namely the Personalized Federated Soft Actor-Critic (PFSAC), which empowers UAVs to devise personalized strategies. This method optimizes the collective anti-jamming strategy within the heterogeneous UAV network, effectively addressing the stochastic Stackelberg game.

The proposed PFSAC algorithm builds on the SAC [37] and FL framework. The SAC algorithm is a maximum entropy-based reinforcement learning approach that consists of a policy network (Actor), which determines the appropriate action based on the current state, a Q-network (Critic) that estimates the Q-values of state-action pairs, and a target value network that helps stabilize the training process. The primary objective of SAC is to enhance both learning stability and efficiency by maximizing the entropy of the expected rewards and the policy, thereby promoting exploration and avoiding premature convergence. In contrast to traditional reinforcement learning algorithms, SAC not only optimizes the expected reward of the policy but also promotes greater exploration of the policyâs behavior to avoid converging to local optima. This feature makes SAC particularly well-suited for discovering optimal policies in heterogeneous UAV networks. Furthermore, to better adapt to our specific environment, we employ the discrete SAC variant [38], which tackles the decision-making problem by optimizing discrete policies, rather than relying on Gaussian distribution sampling in a continuous action space as in conventional SAC. Therefore, we have selected the discrete SAC algorithm as the foundation for PFSAC. Furthermore, to facilitate information sharing while preserving privacy, we utilize FL. However, the adoption of a single global model in the heterogeneous UAV network may obstacle the ability to generate personalized anti-jamming strategies for each UAV pair. To address this challenge, we train personalized models for each UAV pair, guiding the actorâs decision-making process by integrating both local and global critic networks.

In our PFSAC algorithm, we calculate the entropy $\mathcal { H } ( P )$ of a ( )random variable x, where x follows the probability distribution P , defined as:

$$
\begin{array} { r } { \mathcal { H } ( P ) = \underset { x \sim P } { \mathrm { E } } \left[ - \log P ( x ) \right] , } \end{array}\tag{15}
$$

where E denotes the expectation over the distribution P . Considering the entropy component of the SAC algorithm, we incorporate the entropy term from (15) into our framework. Consequently, the target policy for UAV pair n that maximizes the entropy objective can be expressed as:

$$
\begin{array} { l } { \displaystyle \pi _ { n * } ^ { U } = \arg \operatorname* { m a x } _ { \pi _ { n } ^ { U } } \sum _ { t = 0 } ^ { T } \mathbb { E } \left[ r _ { n } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) , \mathbf { a } _ { n } ^ { U } ( t ) \right) \right. } \\ { \left. + \alpha ^ { n } \mathcal { H } \left( \pi _ { n } ^ { U } \left( \cdot \mid \mathbf { s } _ { n } ^ { U } ( t ) \right) \right) \right] , } \end{array}\tag{16}
$$

where the $\alpha ^ { n }$ is a hyperparameter adjusting the weight accorded to the entropy, thereby calibrating the importance of exploratory behavior in the policyâs performance. The soft Q-value function is defined as:

$$
\begin{array} { r l } & { T ^ { \pi } Q _ { n } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) , \mathbf { a } _ { n } ^ { U } ( t ) \right) : = \gamma E _ { \mathbf { s } _ { n } ^ { \prime U } ( t + 1 ) \sim p } \left[ V \left( \mathbf { s } _ { n } ^ { \prime U } \left( t + 1 \right) \right) \right] } \\ & { \qquad + r _ { n } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) , \mathbf { a } _ { n } ^ { U } ( t ) \right) , \qquad ( 1 } \end{array}
$$

and the soft value function V is denoted as:

7)

$$
\begin{array} { r l r } & { } & { V \left( { \bf s } _ { n } ^ { U } ( t ) \right) : = \pi _ { n } ^ { U } \left( { \bf s } _ { n } ^ { U } ( t ) \right) ^ { T } \left[ Q _ { n } ^ { U } \left( { \bf s } _ { n } ^ { U } ( t ) \right) \right. } \\ & { } & { \left. - \alpha ^ { n } \log \left( \pi _ { n } ^ { U } \left( { \bf s } _ { n } ^ { U } ( t ) \right) \right) \right] . } \end{array}\tag{18}
$$

Then, the policy can be improved by minimizing the Kullback-Leibler (KL) divergence, indicative of the deviation between the old and the improved policies:

$$
= \underset { \pi _ { n } ^ { U ^ { \prime } } \in \pi ^ { U } } { \mathrm { a r g m i n } } D _ { \mathrm { K L } } \bigg ( \pi _ { n } ^ { U ^ { \prime } } \left( \cdot | \left( \mathbf { s } _ { n } ^ { U } ( t ) \right) \right) \bigg | \bigg | \frac { \mathrm { e x p } \left( \frac { 1 } { \alpha ^ { n } } Q _ { n } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) , \cdot \right) \right) } { Z \left( \mathbf { s } _ { n } ^ { U } ( t ) \right) } \bigg ) ,\tag{19}
$$

where $\pi _ { n , \mathrm { n e w } } ^ { U }$ is the improved policy, $\pi _ { n } ^ { U ^ { \prime } }$ is the old policy, $D _ { \mathrm { K L } } ( \cdot | | \cdot )$ denotes the KL divergence, and $Z ( \mathbf { s } _ { n } ^ { U } ( t ) ) =$ $\sum _ { \mathbf { a } _ { n } ^ { U } }$ exp $\left( Q _ { n } ^ { U } ( \mathbf { s } _ { n } ^ { U } ( t ) ) , \cdot ) \right)$ ( ( )) =denotes partition function normalizes the distribution. The loss function $J _ { Q _ { n } ^ { U } } ( \theta _ { i } ^ { n } )$ for the critic net-( )work in the Q-value learning process, utilizing neural network parameters $\theta _ { i } ^ { n } ( i \in \{ 1 , 2 \} )$ , is formulated as:

$$
\begin{array} { r l r } { \mathcal { I } _ { Q _ { n } ^ { U } } \left( \boldsymbol { \theta } _ { i } ^ { n } \right) = \mathbb { E } _ { ( \mathbf { s } _ { n } ^ { U } ( t ) , \mathbf { a } _ { n } ^ { U } ( t ) ) \sim D ^ { U } } \left[ \displaystyle \frac { 1 } { 2 } \left( Q _ { n , \theta } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) , \mathbf { a } _ { n } ^ { U } ( t ) \right) \right. \right. } & \\ { \displaystyle \left. \left. - \left( \gamma \mathbb { E } _ { s _ { n } ^ { \prime U } \left( t + 1 \right) \sim p } \left[ V _ { \bar { \boldsymbol { \theta } } } \left( \mathbf { s } _ { n } ^ { \prime U } ( t + 1 ) \right) \right] \right. \right. \right. } & \\ { \displaystyle \left. \left. \left. + r _ { n } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) , \mathbf { a } _ { n } ^ { U } ( t ) \right) \right) \right) ^ { 2 } \right] , } & { } & { ( } \end{array}\tag{20}
$$

where $D ^ { U }$ is the replay buffer and $V _ { \bar { \theta } } ( \mathbf { s } _ { n } ^ { \prime U } ( t + 1 ) )$ is estimated ( ( + 1))using a target network for Q and a Monte Carlo estimate of (18) after sampling experience from the replay buffer. Additionally,

<!-- image-->  
Fig. 4. Framework of the proposed PFSAC algorithm.

according to (19), the loss function when training the policy can be expressed as:

$$
\begin{array} { r l } & { \mathcal { I } _ { \boldsymbol { \pi } _ { n } ^ { U } } ( \mu _ { n } ) = E _ { \mathbf { s } _ { n } ^ { U } ( t ) \sim D ^ { U } } \left[ \pi _ { n } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) \right) ^ { T } \left[ \alpha ^ { n } \log \left( \pi _ { n , \mu } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) \right) \right) \right. \right. } \\ & { \quad \quad \quad \quad \left. \left. - Q _ { n , \theta } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) \right) \right] \right] . } \end{array}
$$

Moreover, the policy network and soft Q-network update processes are described by the following update equations:

$$
\theta _ { i } ^ { n }  \theta _ { i } ^ { n } - \lambda _ { C } ^ { U } \nabla _ { \theta _ { i } ^ { n } } \mathcal { I } ( \theta _ { i } ^ { n } ) , i \in \{ 1 , 2 \} ,\tag{22}
$$

$$
\mu _ { n }  \mu _ { n } - \lambda _ { A } ^ { U } \nabla _ { \mu _ { n } } \mathcal { I } ( \mu _ { n } ) ,\tag{23}
$$

where $\lambda _ { C } ^ { U }$ and $\lambda _ { A } ^ { U }$ represent the learning rates for the online soft Q-networks and policy network, respectively. The coefficient $\alpha ^ { n }$ is updated by minimizing the loss function, given by:

$$
\mathcal { I } ( \alpha ^ { n } ) = \pi _ { t } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) \right) ^ { T } \left[ - \alpha ^ { n } \left( \log \left( \pi _ { t } ^ { U } \left( \mathbf { s } _ { n } ^ { U } ( t ) \right) \right) + \bar { H } \right) \right] ,\tag{24}
$$

where $\bar { H }$ is a constant vector equal to the hyperparameter representing the target entropy. The parameters of the target soft Q-network can be softly updated as follows:

$$
\bar { \theta } _ { i } ^ { n }  \tau ^ { U } \theta _ { i } ^ { n } + ( 1 - \tau ^ { U } ) \bar { \theta } _ { i } ^ { n } , i \in \{ 1 , 2 \} ,\tag{25}
$$

where $\tau ^ { U }$ is the update coefficient.

1) Model Personalization: We predicated on the assumption of dependable communication links between each UAV pair and the satellite server. Each UAV pair capitalizes on its local dataset for model training, subsequently transmitting the locally trained model to the satellite server. Following each training iteration, the server amalgamates the received models and constructs the overarching global model through federated averaging. This global model is then disseminated back to each UAV pair.

However, a notable limitation of traditional FL is its assumption that all users operate with a unified global model. Within the context of the heterogeneous UAV network, different UAV pairs might use the global model to forge cooperative strategies for anti-jamming and mitigating co-channel interference. Nevertheless, due to variations in hardware configurations, mission requirements, and communication environments of each UAV pair, transmission rate requirements fluctuate based on specific mission demands. When all UAV pairs rely on a single global model, it may fall short of meeting the diverse communication needs essential for effective collaborative operations.

To address this heterogeneity, our algorithm enhances the online soft Q-network optimization to suit the individual goals of each UAV pair. This optimization is formulated as:

$$
\operatorname* { m i n } \mathcal { I } \left( \tau \theta _ { i } ^ { n } + ( 1 - \tau ) ( \theta _ { i } ^ { g l o b a l } - \theta _ { i } ^ { n } ) \right) , i \in \{ 1 , 2 \} ,\tag{26}
$$

where $\tau$ is a mixed weighting factor, and the term $\tau \theta _ { i } ^ { n } + ( 1 -$ $\tau ) ( \theta _ { i } ^ { g l o b a l } - \theta _ { i } ^ { n } )$ represents a convex combination of the local and global models, hence forming the personalized model. This enables the training of the personalized model to effectively update the online soft Q-networks.

The framework of the PFSAC algorithm is shown in Fig. 4, each UAV trains a local model based on its observed environment and uploads the model parameters to the satellite server. The global parameters of the online soft Q-networks are computed as follows:

$$
\theta _ { i } ^ { g l o b a l } = \sum _ { n } \rho _ { n } \theta _ { i } ^ { n } , i \in \{ 1 , 2 \} ,\tag{27}
$$

where $\rho _ { n }$ is the weight of the n-th UAV pair network. After obtaining the model parameters of the global Q-networks, the global and local models are aggregated according to a certain weight ratio Ï to the personalized model. After incorporating the global model, the personalized local model for each UAV pair is updated as:

$$
\theta _ { i } ^ { n * } = \tau \theta _ { i } ^ { n } + ( 1 - \tau ) ( \theta _ { i } ^ { g l o b a l } - \theta _ { i } ^ { n } ) , i \in \{ 1 , 2 \} ,\tag{28}
$$

where $\theta _ { i } ^ { n * }$ are the personalized model parameters, $( \theta _ { i } ^ { g l o b a l } - \theta _ { i } ^ { n } )$ ( )denotes the difference between the global model parameters and the local parameters. This approach allows each pair of UAVs to generate personalized anti-jamming strategies by integrating global model parameters from a central server with their locally assessed network model adaptations, thereby assessing the effectiveness of the current strategy and guiding updates to the strategy network, enhancing the overall effectiveness of the collaborative mission.

Based on the above discussion and the PFSAC framework, the complete PFSAC algorithm is shown in Algorithm 1.

## C. Complexity Analysis

In this subsection, we will briefly analyze the computational complexity of the proposed PFSAC during the training and testing process. The complexity is evaluated in terms of the number of operations required, which depends on the neural network architecture, the number of UAV pairs, and the training or inference iterations. The training phase of PFSAC involves local SAC training for each UAV pair, federated aggregation of model parameters, and personalization to adapt to heterogeneous UAV configurations.

For SAC local training, we define the actor network to have $G _ { a }$ layers, with $u _ { a } ^ { g }$ neurons in the g-th layer $( g = 0 , 1 , \ldots , G _ { a } - 1 )$ and critic network to have $G _ { c }$ (layers, with $u _ { c } ^ { g }$ 0 1 1)neurons in the g-th layer $( g = 0 , 1 , \ldots , G _ { a } - 1 )$ . The computational complexity of ( = 0 1 1)the g-th layer in the actor network is dominated by matrix multiplications between consecutive layers, given by $O ( u _ { a } ^ { g } u _ { a } ^ { g + 1 } )$ Similarly, the complexity of the $g \cdot$ ( )-th layer in the critic network is $O ( u _ { c } ^ { g } u _ { c } ^ { g + 1 } )$ . With N UAV pairs, the complexity of training over T time slots is $O ( N T ( \bar { \sum _ { g = 0 } ^ { G _ { a } - 1 } } u _ { a } ^ { g } u _ { a } ^ { g + 1 } + 2 \bar { \sum _ { g = 0 } ^ { G _ { c } - 1 } } u _ { c } ^ { g } \bar { u _ { c } ^ { g } + 1 } ) )$ ( ( + 2 ))The target critic network does not need to be trained and its weights are usually replicated for the critic network through soft updates. In the federated aggregation phase, critic parameters $\theta _ { i } ^ { n }$ from all pairs of N UAVs are uploaded to a central server, averaged, and redistributed. Assuming the total number of parameters in the critic networks is P , the total complexity of this step is O N T P . The personalization step adapts the ( )global model to each UAV pairâs local data by combining the aggregated global parameters with local updates using a weighting factor Ï . This step incurs a complexity of $O ( P )$ ( )per UAV pair per time slot. For N pairs over T time slots, the total personalization complexity is O NT P . The overall ( )computational complexity of PFSAC during the training phase is $\begin{array} { r }  \hat { O ( N T ( \sum _ { q = 0 } ^ { G _ { a } - 1 } \hat { u _ { a } ^ { g } u _ { a } ^ { g + \bar { 1 } } } + 2 \sum _ { q = 0 } ^ { G _ { c } - 1 } u _ { c } ^ { g } u _ { c } ^ { \bar { g } + 1 } ) + N T \bar { P } ) } \end{array}$

( ( + 2 ) + )During the testing phase, each UAV pair uses its personalized actor network to predict actions (e.g. channel $c _ { n }$ and power level $v _ { n } )$ based on the current state. Therefore, the complexity of a single inference is mainly the forward propagation overhead of the actor network $O ( \sum _ { q = 0 } ^ { \tilde { G } _ { a } - 1 } u _ { a } ^ { g } u _ { a } ^ { g + 1 } )$ .

Algorithm 1: PFSAC-Based Anti-Jamming Algorithm.   
1: Input: the number of UAV pairs N , the number of tasks   
M, the number of channels C, the number of the slots $T$   
and the number of power levels $V _ { n } ^ { U } , \forall n .$   
2: Output: the channel $c _ { n } .$ , and power level $v _ { n } , \forall n .$   
3: Initialize: the parameters of each UAV pairâs policy   
network, 2 soft Q-networks, and target soft Q-networks.   
4: Initialize: each UAV pairâs experience replay buffer.   
5: for $t = 1$ to $T$ do   
6: for $n = 1$ to $N$ do   
7: = 1Observe the current ${ \bf s } _ { n } ^ { U } ( t )$ of the environment.   
8: ( ) Sample action from the policy   
$\mathbf { a } _ { n } ^ { U } ( { \dot { t } } ) \sim \pi _ { n } ^ { U } ( \mathbf { a } _ { n } ^ { U } ( t ) | \mathbf { s } _ { n } ^ { U } ( { \dot { t } } ) )$   
9: ( )end for   
10: for $n = 1$ to $N$ do   
11: = 1 Obtain the reward $r _ { n } ^ { U } ( t )$ and next state ${ \bf s } _ { n } ^ { \prime U } ( t + 1 )$   
12: ( ) ( Sample the transition from the environment   
$\mathbf { s } _ { n } ^ { \prime U } ( \bar { t } + 1 ) \sim p ( \mathbf { s } _ { n } ^ { \prime U } ( t + 1 ) \mid \mathbf { s } _ { n } ^ { U } ( t ) , \mathbf { a } _ { n } ^ { U } ( t ) )$   
13: ( + 1) ( ( + 1) ( ) Store the transition in the replay pool   
$D _ { n } ^ { U } \gets D _ { n } ^ { U } \cup \{ ( \mathbf { s } _ { n } ^ { U } ( t ) , \mathbf { a } _ { n } ^ { U } ( \dot { t } ) , \dot { r } _ { n } ^ { U } ( t ) , \mathbf { s } _ { n } ^ { \prime U } ( t + 1 ) ) \}$   
14: ( ( ) ( ) ( ) ( + 1)) Calculate the MSE loss of the soft Q-network by   
(20) and update its weights by (22).   
15: Calculate the policy gradient by (21) and update its   
weight parameters by (23).   
16: Update temperature $\alpha ^ { n }$ by (24).   
17: end for   
18: Aggregate the model parameters of the soft Q-network   
of each UAV pair:   
19: $\begin{array} { r } { \theta _ { i } ^ { g l o b a l }  \sum _ { n } \rho _ { n } \theta _ { i } ^ { n } , i \in \{ 1 , 2 \} } \end{array}$   
20: for $n = 1$ to N do   
21: = 1 Model personalized training:   
22: $\theta _ { i } ^ { n * }  \stackrel { \cdot } {  } \eta _ { i } ^ { n } + ( 1 - \tau ) ( \theta _ { i } ^ { g l o \overline { { b } } a l } - \theta _ { i } ^ { n } ) , i \in \{ 1 , 2 \} .$   
23: + (1 )( ) 1 Update parameters of target soft Q-networks:   
24: $\bar { \theta } _ { i } ^ { \bar { n } }  \tau ^ { \bar { U } } \theta _ { i } ^ { n * } + ( 1 - \tau ^ { U } ) \bar { \theta } _ { i } ^ { n } , i \in \{ 1 , 2 \}$   
25: end for   
26: end for

( )In summary, the complexity of the training phase of the PFSAC algorithm mainly comes from the parallel SAC training process of multiple agents with the federated aggregation personalization operation, and increases with the growth of the depth and width of the neural network as well as the number of training rounds; whereas, in the testing phase, the UAV pairs need to perform only the forward propagation of the Actor network, which has a relatively low amount of computation, and is able to meet the real-time demand of online decision-making better.

## D. DQN-Based Jamming Algorithm

The primary objective of malicious intelligent jammers is to dynamically adjust their channel selection and transmission power to optimize the disruption of UAV communication rates

TABLE II THE DEFAULT SIMULATION PARAMETERS
<table><tr><td>Parameters</td><td>Values</td></tr><tr><td>Activity area of UAVs</td><td> $1 0 0 \mathrm { m } \times 1 0 0 \mathrm { m }$ </td></tr><tr><td>Velocity range of UAVs</td><td>[10,30]m/s</td></tr><tr><td>UAV flight height range</td><td>[10,35]m&#x27;</td></tr><tr><td>Number of jammer</td><td>1</td></tr><tr><td>Number of tasks</td><td>3</td></tr><tr><td>UAV minimum power</td><td>0.01W</td></tr><tr><td>UAV maximum power</td><td> $\{ 0 . 1 \mathrm { W } , 0 . 1 5 \mathrm { W } , 0 . 2 \mathrm { W } , 0 . 2 5 \mathrm { W } \}$ </td></tr><tr><td>UAV power level</td><td> $\{ 4 , 5 , 6 \}$ </td></tr><tr><td>Jammer power range</td><td> $[ 0 . 0 1 , 0 . 3 ] \mathrm { W }$ </td></tr><tr><td>AWGN power</td><td>-114dBm</td></tr><tr><td>ITU model factors</td><td> $a _ { 1 } = 0 . 3 , a _ { 2 } = 5 0 0 , a _ { 3 } = 2 0$ </td></tr><tr><td>Path loss exponent</td><td> $\delta _ { \mathrm { L o S } } = 2 . 2 , \delta _ { \mathrm { N L o S } } = 4 . 6 - 0 . 7 l o g _ { 1 0 } H _ { n }$ </td></tr><tr><td>Path loss per unit distance</td><td> $D ^ { \mathrm { L o S } } = 3 4 . 0 2 \mathrm { d B } , D ^ { \mathrm { N o S } } = 2 0 . 9 6 \mathrm { d B }$ </td></tr><tr><td>Channel bandwidth</td><td>1MHz</td></tr><tr><td>Rate threshold</td><td> $\{ \mathrm { 1 M b p s , 3 M b p s , 5 M b p s } \}$ </td></tr></table>

while simultaneously minimizing transmission costs. Accordingly, the optimization problem for the ground intelligent jammers can be formulated as follows:

$$
\begin{array} { r l r } { ( \mathcal { P } 2 ) : \displaystyle \operatorname* { m a x } _ { \{ c _ { k } , P _ { k } ^ { J } \forall k \} } \mathbb { E } \left[ \sum _ { k = 1 } ^ { K } \sum _ { n = 1 } ^ { N } \eta \left( c _ { k } , c _ { n } \right) \mathrm { R a t e } _ { n } - \sum _ { k = 1 } ^ { K } \beta _ { k } P _ { k } ^ { J } \right] } & \\ { \mathrm { s . t . } \ C 1 : P _ { k } ^ { J } \in \left[ P _ { \operatorname* { m i n } } ^ { J } , P _ { \operatorname* { m a x } } ^ { J } \right] , \forall k , } & \\ { \displaystyle C 2 : c _ { k } \in \mathcal { C } , \forall k , } & {  ( 2 \mathring { \eta } ^ { J } \in \mathcal { C } , \forall k , } \end{array}\tag{9}
$$

where $\beta _ { k }$ is the transmission cost per unit power of the malicious intelligent jammer k, C and C define the power and channel 1 2constraints for the malicious intelligent jammer k, respectively.

To achieve this goal, the intelligent jammer uses the DQN algorithm [39] for policy optimization. DQN enhances training stability by incorporating an experience replay buffer along with a target network. The Q-value function is approximated using a neural network whose parameters are iteratively updated via gradient descent, effectively mitigating issues associated with correlated training data and non-stationary environments. Moreover, the intelligent jammerâs strategy update process aligns with its role as the leader in the Stackelberg game framework, aiming to maximize long-term cumulative rewards through dynamic learning.

## V. SIMULATION RESULTS

## A. Settings

In this section, we evaluate the performance of the PFSAC algorithm through simulations conducted across a variety of scenarios. The default parameters for the heterogeneous UAV network are detailed in Table II. In PFSAC, the Actor network predicts action probabilities using a combination of convolutional and dense layers with softmax output. Concurrently, the Critic network estimates state values using a similar structure but with a single linear output. Both models are finely tuned using the Adam optimizer, supplemented by precisely defined loss functions. We configure the discount factor at 0.9, the learning rate at 0.003, and the exploration rate at 0.1. All simulations are executed in Python, PyCharm and TensorFlow environments.

<!-- image-->  
Fig. 5. The average reward of the UAV pairs for different algorithms when $\bar { N = 6 , M } = 3 , C \overset { \circ } { = } 7 , V ^ { J } = 5$

To verify the performance of the proposed anti-jamming algorithm, we consider the following benchmarks:

- FSAC is a method that combines FL with the SAC algorithm [38]. The algorithm performs SAC locally across multiple distributed agents to optimize anti-jamming strategies for all UAV pairs by periodically aggregating and sharing model updates to protect data privacy.

FD3PG is a method based on Federated Distributed Deep Deterministic Policy Gradient (DDPG), designed to optimize decision-making in multi-agent systems through distributed training and federated parameter aggregation. Originally developed for mixed action spaces in [26].

- ISAC uses the SAC algorithm [38] in a multi-agent environment, where each UAV pair independently runs SAC without exchanging information or collaborating with other UAV pairs, following the independent Q-learning paradigm in [16].

- IDQN [27]: Similar to ISAC, IDQN adapts the DQN [39] algorithm for use in a multi-agent environment where each UAV pair operates independently.

- Random: Under this approach, UAV pairs randomly select their transmission channels and power settings at each decision step.

## B. Performance Evaluation

Fig. 5 illustrates the comparative analysis of average rewards accrued by UAV pairs under various anti-jamming algorithms, with an intelligent jammer deploying a DQN-based strategy. Our PFSAC algorithm demonstrates superior performance by facilitating information sharing among UAV pairs within an FL framework, thereby avoiding co-channel interference and enabling UAV pairs to make adaptive decisions based on network heterogeneity through trained personalized models. In contrast, FSAC and FD3PG also enable channel information sharing, but all UAV pairs use a uniform global model for decision-making, neglecting environmental differences and thus not achieving optimal performance. FSAC demonstrates slightly better performance compared with FD3PG, primarily due to its native compatibility with discrete action spaces, and its enhanced exploration capacity through entropy regularization mechanisms, enabling better adaptation to dynamic and heterogeneous environments like UAV networks. ISAC and IDQN allow UAV pairs to make decisions independently without information exchange, making it difficult to avoid mutual interference. Notably, ISAC surpasses IDQN by enhancing exploration dynamics and policy stability through an entropy regularization technique, thereby bolstering its anti-jamming proficiency. Additionally, we compared these methods with a random approach, which, by merely selecting actions randomly, generally fails to ensure optimization or suitability to the current environment, resulting in the poorest performance.

<!-- image-->  
Fig. 6. The average reward of the jammer for different algorithms when $N =$ $6 , \mathbf { \check { M } } = 3 , C = 7 , \mathbf { \check { V } } ^ { J } = 5$

Fig. 6 displays the average rewards when the intelligent jammer uses the DQN algorithm to interfere, while UAV pairs employ various anti-jamming strategies. The results clearly demonstrate that the jammerâs interference effectiveness is markedly reduced when UAV pairs implement the PFSAC algorithm, followed by the FSAC algorithm. Both strategies promote collaborative information sharing via a global model, enabling UAV pairs to effectively cooperate and mitigate co-frequency interference. Notably, PFSAC outperforms FSAC and FD3PG by enhancing decision-making through personalized model aggregation. Conversely, when UAV pairs adopt the ISAC and IDQN algorithms, the jammerâs performance notably improves, especially with IDQN, which exhibits the highest interference effectiveness. This is due to the independent mode of operation of each pair of UAVs, which precludes cooperation and complicates the task of avoiding co-channel interference and jammer attacks.

When evaluating the performance of anti-jamming strategies, we examined the impact of network scale and jammer quantity variations on system performance. The experimental results are shown in Figs. 7 and 8 respectively. In Fig. 7, as the number of

<!-- image-->  
Fig. 7. The average reward of UAV pairs under varying numbers of UAV pairs.

<!-- image-->  
Fig. 8. The average reward of UAV pairs under varying numbers of jammers.

UAV pairs increases from 4 to 12 with a fixed jammer count of 1, all tested algorithms exhibit a declining trend in average rewards. This phenomenon is primarily attributed to significantly intensified channel interference caused by the increased UAV pairs. Nevertheless, PFSAC consistently maintains the highest average reward across all test scenarios, significantly outperforming other baseline methods. Similarly, in Fig. 8, when the number of UAV pairs remains fixed at 6 while jammer quantities increase from 1 to 4, all strategies show reduced average rewards. This occurs because multiple jammers leverage shared channels to generate adversarial interference, further impeding communications. Despite these adverse conditions, PFSAC still sustains the highest average reward. The superior performance of PFSAC under network expansion and increasing jammer numbers stems from its unique design advantages. The algorithm employs a federated coordination mechanism that enables UAVs to collaboratively learn interference patterns while preserving autonomy in local decision-making. This design effectively balances system robustness and adaptability, enabling simultaneous mitigation of internal competition among UAVs and external interference threats. In contrast, non-cooperative methods like ISAC and IDQN demonstrate significant performance degradation due to lack of coordination, while random strategies completely fail in complex environments.

<!-- image-->  
Fig. 9. The average reward of UAV pairs across different channel numbers.

Fig. 9 distinctly illustrates the influence of channel count on the average rewards accrued by UAV pairs within a heterogeneous UAV network. The analysis reveals that increasing the channels from 5 to 10 for UAV pairs numbered 6, 8, and 10 correlates with a substantial enhancement in average rewards. This enhancement is indicative of the reduced channel interference and subsequent improvement in overall system performance that additional channels provide. However, as the channel count continues to rise, the growth rate of rewards decelerates, indicating that beyond a certain threshold, each UAV pair possesses adequate resources, thus the incremental benefits of additional channels in terms of interference resistance begin to diminish. Furthermore, scenarios where the number of channels is fewer than the number of UAV pairs result in diminished average rewards due to resource limitations. This outcome underscores the critical necessity of scaling channel resources commensurate with the specific demands of the heterogeneous UAV network. Particularly in environments prone to frequent interference, strategic allocation of channel resources is paramount for ensuring system stability and enhancing operational efficiency.

Fig. 10 delineates the correlation between the flying altitudes of UAV pairs and their average rewards under the FSAC and PFSAC algorithms. It is discernible that the average reward escalates as the flying altitude increases, signifying an enhancement in interference resistance. Particularly in the altitude range of 10 to 20 meters, the average reward significantly increases, demonstrating that raising the flying height in this range is particularly effective in reducing interference. However, when the flying altitude exceeds 25 meters, the growth in average rewards tends to plateau, possibly due to increased path loss and weakened interference signal strength at higher altitudes, which relatively reduces the interference among UAV pairs, thus limiting the gains in interference resistance from further altitude increases. Comparing the two strategies, the PFSAC strategy achieves higher average rewards at all tested altitudes than the FSAC strategy, indicating that PFSAC is more effective in combating interference in heterogeneous UAV networks.

<!-- image-->  
Fig. 10. Variation in average reward of UAV pairs at different flying altitudes.

<!-- image-->  
Fig. 11. Performance Comparison of PFSAC algorithms with different mixed weights.

Fig. 11 evaluates the efficiency of the PFSAC algorithm by exploring its performance across different mixed weight ratios between the local and global models, designated as L:G. The ratios examined include 3:7, 5:5, 7:3, and 9:1, and compare them with the FSAC algorithm. The results elucidate that the mixed weight ratio exerts a significant impact on the performance of the PFSAC algorithm. The data presented in the figureâs curves reveal that, while performance for all ratios initially escalates rapidly, the 7:3 ratioâs efficiency progressively stabilizes and outperforms other configurations over time, achieving a superior reward value. Therefore, in the heterogeneous UAV network, the best ratio is approximately 7:3, indicating the importance of a higher proportion of the local model in improving efficiency. However, determining the optimal mixed weight is challenging due to multiple systemic factors. Therefore, further research and discussion on the weight distribution between local and global models are needed in the future.

## VI. CONCLUSION

This paper presents an anti-jamming algorithm for heterogeneous UAV communication networks, aimed at maximizing the communication rate of UAV pairs while minimizing transmission costs through the design of joint channel and power allocation. Intelligent jammers disrupt UAV communications by dynamically selecting interference channels and power levels. We have established a theoretical framework based on stochastic Stackelberg games, where the jammer plays the role of the leader initiating interference attacks, and the heterogeneous UAV network acts as the follower facilitating communication between UAV pairs. We propose a novel PFSAC algorithm that allows each UAV to make personalized decisions based on its specific needs and configuration in a complex communication environment, thereby enhancing interference resistance to some extent. Intelligent jammers optimize their interference strategies using the DQN algorithm. Simulation results indicate that PFSAC offers better interference resistance performance than FSAC, FD3PG, ISAC, IDQN, and random methods.

## REFERENCES

[1] W. Liu et al., âJoint trajectory design and resource allocation in UAVenabled heterogeneous MEC systems,â IEEE Internet Things J., vol. 11, no. 19, pp. 30817â30832, Oct. 2024.

[2] W. Liu et al., âUAV-Enabled wireless networks with movableantenna array: Flexible beamforming and trajectory design,â 2024, arXiv:2405.20746.

[3] Y. Wu, X. Guan, W. Yang, and Q. Wu, âUAV swarm communication under malicious jamming: Joint trajectory and clustering design,â IEEE Wireless Commun. Lett., vol. 10, no. 10, pp. 2264â2268, Oct. 2021.

[4] L. Xiao, C. Xie, M. Min, and W. Zhuang, âUser-centric view of unmanned aerial vehicle transmission against smart attacks,â IEEE Trans. Veh. Technol., vol. 67, no. 4, pp. 3420â3430, Apr. 2018.

[5] Y. Wu, W. Yang, X. Guan, and Q. Wu, âUAV-enabled relay communication under malicious jamming: Joint trajectory and transmit power optimization,â IEEE Trans. Veh. Technol., vol. 70, no. 8, pp. 8275â8279, Aug. 2021.

[6] Y. Wu, W. Fan, W. Yang, X. Sun, and X. Guan, âRobust trajectory and communication design for multi-UAV enabled wireless networks in the presence of jammers,â IEEE Access, vol. 8, pp. 2893â2905, 2020.

[7] L. Jia, F. Yao, Y. Sun, Y. Xu, S. Feng, and A. Anpalagan, âA hierarchical learning solution for anti-jamming Stackelberg game with discrete power strategies,â IEEE Wireless Commun. Lett., vol. 6, no. 6, pp. 818â821, Dec. 2017.

[8] C. Han and Y. Niu, âCross-layer anti-jamming scheme: A hierarchical learning approach,â IEEE Access, vol. 6, pp. 34874â34883, 2018.

[9] C. Han, L. Huo, X. Tong, H. Wang, and X. Liu, âSpatial anti-jamming scheme for internet of satellites based on the deep reinforcement learning and stackelberg game,â IEEE Trans. Veh. Technol., vol. 69, no. 5, pp. 5331â 5342, May 2020.

[10] N. Gao, Z. Qin, X. Jing, Q. Ni, and S. Jin, âAnti-intelligent UAV jamming strategy via deep Q-networks,â IEEE Trans. Commun., vol. 68, no. 1, pp. 569â581, Jan. 2020.

[11] L. Xiao, Y. Li, C. Dai, H. Dai, and H. V. Poor, âReinforcement learningbased NOMA power allocation in the presence of smart jamming,â IEEE Trans. Veh. Technol., vol. 67, no. 4, pp. 3377â3389, Apr. 2018.

[12] J. Liu et al., âIntelligent jamming defense using DNN Stackelberg game in sensor edge cloud,â IEEE Internet Things J., vol. 9, no. 6, pp. 4356â4370, Mar. 2022.

[13] J. Zhang et al., âHow often channel estimation is required for adaptive IRS beamforming: A bilevel deep reinforcement learning approach,â IEEE Trans. Wireless Commun., vol. 23, no. 8, pp. 8744â8759, Aug. 2024.

[14] C. Han, A. Liu, H. Wang, L. Huo, and X. Liang, âDynamic antijamming coalition for satellite-enabled army IoT: A distributed game approach,â IEEE Internet Things J., vol. 7, no. 11, pp. 10932â10944, Nov. 2020.

[15] Z. Yin, Z. Wang, J. Li, M. Ding, W. Chen, and S. Jin, âDecentralized federated reinforcement learning for user-centric dynamic TFDD control,â IEEE J. Sel. Topics Signal Process., vol. 17, no. 1, pp. 40â53, Jan. 2023.

[16] Y. Li, J. Wang, and Z. Gao, âLearning-based multi-domain anti-jamming communication with unknown information,â Electronics, vol. 12, no. 18, 2023, Art. no. 3901.

[17] Z. Yin et al., âUAV communication against intelligent jamming: A Stackelberg game approach with federated reinforcement learning,â IEEE Trans. Green Commun. Netw., vol. 8, no. 4, pp. 1796â1808, Dec. 2024.

[18] D. Yang, G. Xue, J. Zhang, A. Richa, and X. Fang, âCoping with a smart jammer in wireless networks: A Stackelberg game approach,â IEEE Trans. Wireless Commun., vol. 12, no. 8, pp. 4038â4047, Aug. 2013.

[19] L. Xiao, T. Chen, J. Liu, and H. Dai, âAnti-jamming transmission stackelberg game with observation errors,â IEEE Commun. Lett., vol. 19, no. 6, pp. 949â952, Jun. 2015.

[20] L. Jia, F. Yao, Y. Sun, Y. Niu, and Y. Zhu, âBayesian stackelberg game for antijamming transmission with incomplete information,â IEEE Commun. Lett., vol. 20, no. 10, pp. 1991â1994, Oct. 2016.

[21] S. dâOro, L. Galluccio, G. Morabito, S. Palazzo, L. Chen, and F. Martignon, âDefeating jamming with the power of silence: A game-theoretic analysis,â IEEE Trans. wireless Commun., vol. 14, no. 5, pp. 2337â2352, May 2015.

[22] Y. Zhang et al., âA multi-leader one-follower Stackelberg game approach for cooperative anti-jamming: No pains, no gains,â IEEE Commun. Lett., vol. 22, no. 8, pp. 1680â1683, Aug. 2018.

[23] Z. Shen, K. Xu, and X. Xia, âBeam-domain anti-jamming transmission for downlink massive MIMO systems: A stackelberg game perspective,â IEEE Trans. Inf. Forensics Security, vol. 16, pp. 2727â2742, 2021.

[24] L. A. b. Burhanuddin, X. Liu, Y. Deng, U. Challita, and A. Zahemszky, âQoE optimization for live video streaming in UAV-to-UAV communications via deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 71, no. 5, pp. 5358â5370, May 2022.

[25] M. M. Azari, G. Geraci, A. Garcia-Rodriguez, and S. Pollin, âUAV-to-UAV communications in cellular networks,â IEEE Trans. Wireless Commun., vol. 19, no. 9, pp. 6130â6144, Sep. 2020.

[26] H. Zhou, H. Wang, Z. Yu, G. Bin, M. Xiao, and J. Wu, âFederated distributed deep reinforcement learning for recommendation-enabled edge caching,â IEEE Trans. Serv. Comput., vol. 17, no. 6, pp. 3640â3656, Nov./Dec. 2024.

[27] A. Tampuu et al., âMultiagent cooperation and competition with deep reinforcement learning,â PLoS One, vol. 12, no. 4, 2017, Art. no. e0172395.

[28] L. Zhang, Z. Guan, and T. Melodia, âUnited against the enemy: Antijamming based on cross-layer cooperation in wireless networks,â IEEE Trans. Wireless Commun., vol. 15, no. 8, pp. 5733â5747, Aug. 2016.

[29] Y. Li, S. Bai, and Z. Gao, âA multi-domain anti-jamming strategy using stackelberg game in wireless relay networks,â IEEE Access, vol. 8, pp. 173609â173617, 2020.

[30] Y. Xu et al., âA one-leader multi-follower Bayesian-Stackelberg game for anti-jamming transmission in UAV communication networks,â IEEE Access, vol. 6, pp. 21697â21709, 2018.

[31] F. Du, J. Li, Y. Lin, Z. Wang, and Y. Qian, âMean-field multi-agent reinforcement learning for adaptive anti-jamming channel selection in UAV communications,â in Proc. IEEE 14th Int. Conf. Wireless Commun. Signal Process., 2022, pp. 910â915.

[32] F. Yao and L. Jia, âA collaborative multi-agent reinforcement learning anti-jamming algorithm in wireless networks,â IEEE Wireless Commun. Lett., vol. 8, no. 4, pp. 1024â1027, Aug. 2019.

[33] Z. Yin, Y. Lin, Y. Zhang, Y. Qian, F. Shu, and J. Li, âCollaborative multiagent reinforcement learning aided resource allocation for UAV anti-jamming communication,â IEEE Internet Things J., vol. 9, no. 23, pp. 23995â24008, Dec. 2022.

[34] J. Cui, Y. Liu, and A. Nallanathan, âMulti-agent reinforcement learningbased resource allocation for UAV networks,â IEEE Trans. Wireless Commun., vol. 19, no. 2, pp. 729â743, Feb. 2020.

[35] D. Fudenberg, Game Theory. Cambridge, MA, USA: MIT Press, 1991.

[36] Z. Han et al., Game Theory in Wireless and Communication Networks: Theory, Models, and Applications. Cambridge, U.K.: Cambridge Univ. Press, 2011.

[37] T. Haarnoja et al., âSoft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor,â in Proc. Int. Conf. Mach. Learn., PMLR, 2018, pp. 1861â1870.

[38] P. Christodoulou, âSoft actor-critic for discrete action settings,â 2019, arXiv: 1910.07207.

[39] V. Mnih et al., âHuman-level control through deep reinforcement learning,â Nature, vol. 518, no. 7540, pp. 529â533, 2015.

<!-- image-->  
Yeguang Qin (Graduate Student Member, IEEE) received the ME degree from the Department of Software Engineering, Xinjiang University, in 2023. He is currently working toward the PhD degree with the Department of Computer Science and Technology, Central South University, advised by Prof. Ming Zhao. His research work focuses on wireless networks, network traffic control, and machine learning algorithm.  
Jie Tang (Graduate Student Member, IEEE) received the MS degree from Hunan Normal University, Changsha, China, in 2023, and is currently working toward the PhD degree with the School of Computer Science and Engineering, Central South University, Changsha. His current research interests include SA-GIN, LLM, and IoT.

<!-- image-->

<!-- image-->

Fengxiao Tang (Senior Member, IEEE) received the BE degree in measurement and control technology and instrument from the Wuhan University of Technology, Wuhan, China, in 2012 and the MS degree in software engineering from the Central South University, Changsha, China, in 2015 and the PhD degree from the Graduate School of Information Science, Tohoku University, Japan. Currently, He is an full professor with the School of Computer Science and Engineering of Central South University. He has been an assistant professor from 2019 to 2020 and an

associate professor from 2020 to 2021 with the Graduate School of Information Sciences (GSIS) of Tohoku University. His research interests are unmanned aerial vehicles system, IoT security, game theory optimization, network traffic control and machine learning algorithm. He was a recipient of the prestigious Deanâs and Presidentâs Awards from Tohoku University in 2019, and several best paper awards at conferences including IC-NIDC 2018/2023, GLOBECOM 2017/2018. He was also a recipient of the prestigious Funai Research Award in 2020, IEEE ComSoc Asia-Pacific (AP) Outstanding Paper Award in 2020 and IEEE ComSoc AP Outstanding Young Researcher Award in 2021.

<!-- image-->

Ming Zhao (Member, IEEE) received the MSc and PhD degrees in computer science from Central South University, Changsha, China, in 2003 and 2007, respectively. He is currently a professor with the School of Computer Science and Engineering, Central South University. His main research focuses on wireless networks. He is also a member of the China Computer Federation.

<!-- image-->

Nei Kato (Fellow, IEEE) is a full professor and the dean with the Graduate School of Information Sciences, Tohoku University. He has researched on computer networking, wireless mobile communications, satellite communications, ad hoc and sensor and mesh networks, UAV networks, smart grid, AI, IoT, Big Data, and pattern recognition. He has published more than 500 papers in prestigious peerreviewed journals and conferences. He served as the vicepresident (member and Global Activities) of IEEE Communications Society from 2018 to 2021, and the editor-in-chief for IEEE Transactions on Vehicular Technology from 2017 to 2021. He is the editor-in-chief for IEEE Internet of Things Journal. He is a fellow of the Engineering Academy of Japan and IEICE.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_3_img_4.jpeg|page_3_img_4]]
2. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_5_img_1.png|page_5_img_1]]
3. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_7_img_1.png|page_7_img_1]]
4. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_9_img_1.png|page_9_img_1]]
5. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_10_img_1.png|page_10_img_1]]
6. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_10_img_2.png|page_10_img_2]]
7. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_10_img_3.png|page_10_img_3]]
8. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_11_img_1.png|page_11_img_1]]
9. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_11_img_2.png|page_11_img_2]]
10. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_11_img_3.png|page_11_img_3]]
11. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_13_img_1.jpeg|page_13_img_1]]
12. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_13_img_2.jpeg|page_13_img_2]]
13. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_13_img_3.jpeg|page_13_img_3]]
14. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_13_img_4.jpeg|page_13_img_4]]
15. [[../extracted_images/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication/page_13_img_5.jpeg|page_13_img_5]]

---

