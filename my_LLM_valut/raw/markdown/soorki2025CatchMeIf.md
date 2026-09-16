# Catch Me If You Can: Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks

Mehdi Naderi Soorki , Hossein Aghajari , Sajad Ahmadinabi, Hamed Bakhtiari Babadegani, Christina Chaccour , Member, IEEE, and Walid Saad , Fellow, IEEE

AbstractâLong-range (LoRa) wireless networks have been widely proposed as efficient wireless access networks for batteryconstrained Internet of Things (IoT) devices. However, applying the LoRa-based IoT network in search-and-rescue (SAR) operations will have limited coverage caused by high signal attenuation due to terrestrial blockages, especially in highly remote areas. To overcome this challenge, using unmanned aerial vehicles (UAVs) as a flying LoRa gateway to transfer messages from ground LoRa nodes to the ground rescue station can be a promising solution. In this paper, an artificial intelligence-empowered SAR operation framework using a UAV-assisted LoRa network in different unknown search environments is designed and implemented. The problem of the flying LoRa (FL) gateway control policy is modeled as a partially observable Markov decision process to move the UAV towards the LoRa transmitter carried by a lost person in the known remote search area. A deep reinforcement learning (RL)-based policy is designed to determine the adaptive FL gateway trajectory in a given search environment. Then, as a general solution, a deep meta-RL framework is used for SAR in any new and unknown environments. The proposed deep meta-RL framework integrates the information of the prior FL gateway experience in the previous SAR environments to the new environment and then rapidly adapts the UAV control policy model for SAR operation in a new and unknown environment. To analyze the performance of the proposed framework in real-world scenarios, the proposed SAR system is experimentally tested in three environments: a university campus, a wide plain, and a slotted canyon at Mongasht mountain ranges, Iran. Experimental results show that if the deep meta-RL-based control policy is applied instead of the deep RL-based one, the number of SAR time slots decreases from 141 to 50. Moreover, in the slotted canyon environment, the UAV energy consumption under the deep meta-RL policy is respectively 57% and 23% less than the deep RL and Actor-Critic RL policies.

Index TermsâDeep meta-reinforcement learning, LoRa technology, search-and-rescue operation, unmanned aerial vehicle.

## I. INTRODUCTION

U NMANNED aerial vehicles (UAVs) are playing an in-creasingly important role in next-generation wireless networks such as 5G and beyond [1]. For instance, UAVs can guarantee ultra-reliable connectivity and extend the cellular network coverage to the three-dimensional (3D) space [2]. In particular, we can temporarily move UAVs to cover Internetof-Things (IoT) devices and establish communications without high-cost conventional network infrastructures. In this regard, UAV-assisted wireless networks can decrease operational expenditures and improve the efficiency of various IoT applications such as smart farming, smart factories, and public safety [3]. However, to support the IoT trend, a reliable wireless access technology with wide reach and low power consumption is required. In this regard, the so-called long-range (LoRa) communication protocol has been proposed as a promising technology for high energy-efficient and long-range communication [3], [4]. These two characteristics make LoRa technology an appropriate solution for battery-constrained IoT devices that are often deployed in remote rural areas. A typical LoRa-based IoT network begins with a LoRa-enabled embedded sensor node that sends data to the LoRa gateway. Then, data can be sent from the LoRa gateway over a cellular network and then routed to application servers located at the network core. One of the key challenges of LoRa-based IoT networks is localization for outdoor environments that is needed for different applications such as navigation and tracking, air traffic control, remote sensing, intelligence, surveillance, and reconnaissance, and search-and-rescue (SAR) operations [5].

## A. Related Works

Existing outdoor localization techniques are mainly based on the received signal strength index (RSSI) scheme in wireless LoRa networks [6]. In the RSSI positioning methods, the enddevice location is estimated by RSSI value when it transmits data to the LoRa gateways without the requirement of clock synchronization. Thus, RSSI-based techniques are vastly employed to develop positioning functions in LoRa networks [7]. Some recent works, such as in [8], [9] and [10], analyze RSSI-based LoRa localization systems for different scenarios. In [8], the authors combine fingerprint-based and model-based RSSI methods to solve the outdoor positioning problem. They adopt an interpolation-based approach to build a 3D model with 36 RSSI sampling points to achieve a higher-accurate localization model. The work in [9] proposed an RSSI-based method to accurately identify the location of a vehicle equipped with a LoRa node traveling along a known path that is divided into

Digital Object Identifier 10.1109/TMC.2024.3468382 defined segments. Values of the RSSI measured by the LoRa gateways are collected and used to characterize each segment. In [10], the RSSI-based method is proposed for the localization of cattle collars communicating with LoRa radios. In particular, the authors developed an RSSI-based distance estimation using real-time adjustment of RSSI-distance mapping. However, the works in [8], [9] and [10] are based on the RSSI method and, thus, they need to deploy a large number of LoRa gateways across large-scale outdoor areas, which is not practical in unknown and highly remote areas.

Some prior works, such as the ones in [11], [12] and [13], have recently introduced LoRa technology as a promising solution for SAR operations in highly remote mountains. A LoRa-based system for SAR operations is presented in [11]. Then, the localization of the persons is obtained through a greedy algorithm based on path-loss (PL) measurements. Radio PL models for the ground-to-ground (G2G) LoRa link of body-worn LoRa devices in harsh mountain environments are derived by measurements. In [12] and [13], the challenging case of mountain SAR operations was investigated, and then the authors highlighted how LoRa-based wireless localization can enable a new generation of SAR devices, significantly outperforming current systems. Mainly, in [13], the authors experimentally evaluate the effectiveness of LoRa for mountain SAR by evaluating three beneficial characteristics: range, battery life, and LoRa link robustness to shadowing. Exiting SAR solutions such as the ones in [11], [12] and [13] apply greedy algorithms to move toward the direction that maximizes the received power over G2G wireless links. However, employing UAV as a flying gateway in localization and tracking systems can bring many attractive advantages due to its high possibility of line-of-sight (LoS) UAV-to-ground (U2G) LoRa links and less path loss compared to the G2G LoRa links. Moreover, using the UAV as an FL gateway makes it possible to move the gateway location in the sky more quickly and flexibly compared to ground gateways [14]. Moreover, in an environment including non-LoS links, such as the slotted canyon, the greedy algorithm may not be able to find the lost person and get stuck in the local optimal solution. On the other hand, deep reinforcement learning models appropriately use helpful information from previous steps to increase the chances of finding the global optimum and avoiding the local optimal points [15], [16]. Moreover, in reinforcement learning, one of the main techniques to avoid local optimal solutions is switching on randomization again for a while, worse values may come at first but may be better in the future [15], [16]. So, instead of a greedy algorithm, we need a much faster, robust to optima issues, and reliable solution based on a deep RL learning framework for UAV control movement in SAR operations.

Several recent works such as [12], [17], [18], [19], [20] and [21] have proposed using UAVs in the LoRa networks. In [17], a UAV-assisted LoRa architecture is suggested in which UAVs act as relays for the traffic generated between LoRa nodes and a base station (BS). Then, they focus on designing a distributed topology control algorithm that periodically updates the UAV topology to adapt to the movement of the groundbased LoRa nodes. In [22], the authors experimentally analyzed and modeled the channel of the U2G LoRa links in urban environments. Then, they discussed the dependencies between transmission power, spread factor (SF), RSSI, and signal-tonoise (SNR). In [12], [19] and [23], the authors studied characterizing radio helmet-to-UAV links in a real mountain area. The authors reported measurements of the excessive aerial path loss seen by a UAV overflying a mountain canyon to derive an equivalent model with the final aim of applying signal-strengthbased localization. In particular, they showed that despite the iced canyonâs walls, there is no significant seasonal difference in the PL wireless link between transmitter LoRa embedded in a helmet and UAV. In [20], the authors presented a drone-aided localization system for LoRa networks in which a UAV is used to improve the estimation of a nodeâs location initially provided by the network. The work in [20] considered a greedy search algorithm to navigate the drones. In [21], the authors proposed a sequential localization algorithm for two single and multiple LoRa terminal scenarios. In the model of [21], the UAV trajectory optimization for positioning is mainly based on the current target position estimation to find the best possible next step following the greedy algorithm. The results of [21] are then validated in different simulation scenarios. Despite being interesting, the localization solutions of [20] and [21] are based on a greedy algorithm and did not propose a general adaptive and smart solution for UAV control movement in SAR operation. Their results are mainly based on simulation. Some recent works such as the ones in [24] and [25] discuss point-of-interest detection and localizations. In [24], the authors focus on the visual tracking supported by UAVs. They propose a hybrid solution: along with the tracked objects, scenes are entirely depicted by adding contextual information, i.e., data describing places and natural features. However, in real SAR scenarios in highly remote areas, for example, when the lost person is located in a narrow-slotted canyon, the UAV camera can not find the target point of interest.

Some recent works, such as the ones in [26] and [27], focused on deep RL-based intelligent control policy in UAV trajectory planning. In [26], the authors have focused on applying deep reinforcement learning (DRL) in UAV resource allocation and trajectory planning. DRL is used to design the decision deployment of UAVs, optimize data transfer rate, throughput, energy efficiency, and other metrics, and learn better path planning strategies to make UAVsâ decisions more intelligent. In [27], the authors explored a UAV-aided SAR operation in indoor environments by sensing the RF signals emitted from a smart device owned by the victim. They leveraged reinforcement learning tools and considered two indoor scenarios using commercial ray-tracing software. However, the key insights from the recent works in [26] and [27] are mainly based on simulation results, and their solution is only evaluated for a given known environment. Thus, there is a need to design an innovative and adaptive policy for the localization method of SAR operation using UAV-assisted LoRa networks, especially in unknown and highly remote areas.

## B. Contributions and Organization

The major contributions of this article can be summarized as follows.

- The main contribution of this paper is implementing and analyzing a novel artificial intelligence-empowered SAR operation framework using a UAV-assisted LoRa network that can be applied to different unknown rescue environments. The proposed approach autonomously adapts the control policy of the UAV trajectory to the spatial geometry of a new search environment, thereby allowing the system to determine the unknown location of a lost person.

We formulate the FL gateway control problem in the UAV-assisted LoRa network as a stochastic optimization problem. This problem aims to maximize the stochastic episodic return that includes the received power from the LoRa node at the FL gateway over future time slots. Next, we model the FL gateway control problem as a partially observable Markov decision process (POMDP). Then, a deep reinforcement learning (RL) policy is proposed to adaptively control the FL gateway trajectory during SAR operation in a given environment. To find a near-optimal solution, a parametric functional form policy is implemented using a deep recurrent neural network (RNN), including long short-term memory (LSTM) layers that can directly search the optimal policies of the FL gateway controllers.

Then, to increase the generalizability of our framework, a control policy using deep meta-RL is designed. By applying deep meta-RL control policy, the controller can integrate the prior FL gateway experience with information collected from the other search environments to rapidly train an adaptive policy model for SAR operation in a new SAR environment.

We conducted real-world experiments and collected training data sets from real measurements to evaluate our proposed framework. We designed and implemented a UAV-assisted LoRa network, including the LoRa end node and the flying and ground LoRa gateways. These experiments were conducted in various urban and remote outdoor scenarios. To evaluate SAR operations under our proposed framework in the urban environment, we deployed the UAV-assisted LoRa network across the campus of the Shahid Chamran University of Ahvaz. Moreover, we deployed the UAV-assisted LoRa network over the Mongasht mountain ranges in Khuzestan province, Iran. Then, we did another SAR in this highly remote area.

C The results of the extensive experimental evaluation demonstrate the effectiveness of our framework in different SAR scenarios. Under the deep meta-RL control policy, the FL gateway hovers over the lost personâs location after 50 time slots, while under the RL control policy, it takes 141 time slots in the slotted canyon environment. Furthermore, the average distance between the UAV trajectories under the deep meta-RL and deep RL-based policies and the UAV trajectory under the optimal policy is 619 and 1930 meters, respectively, during the SAR operation. Moreover, we observe that, on average, the UAV energy consumption under the deep meta-RL policy is 57% and 23% less than the deep RL and Actor-Critic (AC) RL policies, respectively. In addition, the SAR time slots are 19% less for LoRa spread factor 12 than for spread factor 8.

The rest of the paper is organized as follows. Section II describes the system model and problem formulation. Section III proposes a deep meta-RL framework for controlling UAV trajectory in different unknown SAR environments. Section IV introduces our experimental setup, including the hardware that we used to implement our UAV-Assisted LoRa Network and our measurement scenarios. Then, in Section V, we numerically evaluate the practical performance of our SAR system for highly remote areas and our proposed deep meta-RL-based UAV control policy, which is trained by real data. Finally, conclusions are drawn in Section VI.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

## A. System Model

Consider a UAV-Assisted LoRa network composed of a LoRa node, one FL gateway, and one ground LoRa (GL) gateway. Here, a lost person is equipped with a LoRa node that periodically transmits a known signal called a beacon with duration Ï seconds. The transmission power of the LoRa node is $P _ { T x , t }$ in dB at time slot t. The location of the lost person is an unknown point of interest (POI) $\left( x _ { P } , y _ { P } , z _ { P } \right)$ in the 3D search area of interest (SAI), $\mathcal { C } \subset \mathbb { R } ^ { 3 }$

The FL gateway is a LoRa gateway mounted on a UAV. The FL gateway is equipped with GPS and LoRa modules. At each time slot t, the FL gateway transmits a message, $\mathbf { \nabla } m _ { t } =$ $\left[ \beta _ { t } , \gamma _ { t } , x _ { t } , y _ { t } , z _ { t } \right]$ to the GL gateway. This message contains the [RSSI $\beta _ { t }$ ]and SNR $\gamma _ { t }$ of the received LoRa beacon signal from the LoRa node, as well as the FL gateway location, $( x _ { t } , y _ { t } , z _ { t } )$ . Let, the UAV speed is $v _ { t }$ ( )at time slot t. In our model, the control action of UAV is $a _ { t } \in \{ E , W , N , S , H , U , D \}$ where E, W , N, S, H, $U .$ , and D represent the control actions including move east, west, north, south, hover, up, and down. For example, if $a _ { t } = N$ , then =in the next time slot t   and during Ï , the FL gateway will be at $( x _ { t + 1 } , y _ { t + 1 } , , z _ { t + 1 } ) = ( x _ { t } , y _ { t } + v _ { t } \tau , z _ { t } )$ . Following the data of $\beta _ { t } , \gamma _ { t }$ ) = ( + )in the received message mt at the GL gateway, the ground rescue station can compute the received signal power $P _ { R x , t }$ at FL gateway and time slot t as follow [28]:

$$
P _ { R x , t } = \beta _ { t } - 1 0 \log _ { 1 0 } ( 1 + 1 0 ^ { - \frac { \gamma _ { t } } { 1 0 } } ) .\tag{1}
$$

The resulting received power $P _ { R x , t }$ at the FL gateway from an unknown location of the LoRa node is a random variable. This is because the LoRa signals transmitting from the LoRa node antenna often encounter the spatial geometry of SAI, including random obstacles, such as trees and rocks, before reaching a given moving FL gateway receiver. The radiating electromagnetic field is reflected, diffracted, and scattered by these various obstacles, resulting commonly in a random multiplicity of rays impinging on the FL gateway antenna [28]. Thus, spatial geometry directly affects the radio geometry of a given SAI i. Generally, the statistically varying received signal power is $P _ { R x , t } = P _ { T x , t } h _ { t }$ . There are some recent works, such =as the ones in [29], [30] that have focused on U2G channel modeling. However, we use the general U2G channel model, including different channel parameters, which can be generally applied to any unknown remote areas for rescue operations. These general parameters include the path loss exponent, the excessive path loss coefficients in LoS and non-LoS cases, and the shadow-fading random variable. Here, $h _ { t }$ is the channel model for the ground-to-air channel between the ground LoRa node and FL gateway at time slot t, which is given by [31]:

$$
h _ { t } = \left\{ \begin{array} { l l } { \eta _ { \mathrm { L o S } } ^ { - 1 } \nu ^ { 2 } 1 0 ^ { \frac { \omega } { 1 0 } } \big ( \frac { c } { 4 \pi f _ { c } d _ { t } } \big ) ^ { \kappa } , } & { \mathrm { L o S ~ l i n k } , } \\ { \eta _ { \mathrm { n o n - L o S } } ^ { - 1 } \nu ^ { 2 } 1 0 ^ { \frac { \omega } { 1 0 } } \big ( \frac { c } { 4 \pi f _ { c } d _ { t } } \big ) ^ { \kappa } , } & { \mathrm { n o n - L o S ~ l i n k } , } \end{array} \right.\tag{2}
$$

where $f _ { c }$ is the carrier frequency, Îº is the path loss exponent, $\eta _ { \mathrm { L o S } }$ and $\eta _ { \mathrm { n o n - L o S } } ~ ( \eta _ { \mathrm { n o n - L o S } } > \eta _ { \mathrm { L o S } } > 1 )$ are the excessive path 1loss coefficients in LoS and non-LoS cases, and c is the speed of light. Note that the non-LoS probability is $ { \mathrm { P r } } _ { \mathrm { n o n - L o S } , t } =$ $1 - \mathrm { P r } _ { \mathrm { L o S } , t }$ Pr = Here, Ï is the shadow-fading random variable 1 Prdue to the terrain obstructions, such as hills or large rocks, or artificial obstructions, such as buildings. Î½ is called multipath fading, resulting from the signal change rate proportional to FL gateway velocity [28]. In such practical scenarios, we do not have any additional information about the exact locations, heights, and number of obstacles. Therefore, we must consider the randomness associated with the LoS and non-LoS links while designing a SAR system using UAV-assisted LoRa networks. The LoS probability depends on the spatial geometry of the SAI, the location of the LoRa node and the UAV, as well as the elevation angle [31]. One suitable expression for the $\mathrm { L o } \mathrm { S }$ probability is given by $\begin{array} { r } { \mathrm { _ { L o S , } } t = \frac { 1 } { 1 + \varepsilon e ^ { - \sigma ( \varrho _ { t } - \varepsilon ) } } } \end{array}$ [31]. Where Îµ Pr =and Ï are constant values that depend on the carrier frequency and type of environment such as mountain, rural, or urban, and $\varrho _ { t }$ is the elevation angle between LoRa node and UAV at time slot $\begin{array} { r } { t . \ \varrho _ { t } = \frac { 1 8 0 } { \pi } \times \mathrm { s i n } ^ { - 1 } ( \frac { z _ { t } } { d _ { t } } ) } \end{array}$ , where $z _ { t }$ is the UAV altitude, and $d _ { t } = \sqrt { ( x _ { t } - x _ { P } ) ^ { 2 } + ( y _ { t } - y _ { P } ) ^ { 2 } + ( z _ { t } - z _ { P } ) ^ { 2 } }$ represents the = ( ) + ( ) + ( )distance between the FL gateway and the unknown location of lost person at time slot t. Given the random spatial geometry of each SAI, the resulting radio geometry parameters such as Ï, Î½, Î·LoS, Î· non-LoS, Îº and $\varrho _ { t }$ are unknown and depend on the actual geographical situation. In our model, we consider the worst-case scenario in which there is no available model for the radio geometry parameters because the SAI is generally unknown for SAR operations. Next, we define a view circle centered at the FL gateway with radius $d _ { t }$ . The radius of the view circle depends on the LoRa spread factor, transmission power, the UAVâs height, and the SAR environmentâs spatial geometry. The minimum required received signal power $P _ { R x , t } = P _ { T x , t } h _ { t }$ =at the FL gateway from the LoRa node for accurate detection is defined by a threshold $\alpha _ { s }$ over spread factor s, which means that $P _ { R x , t } \geq \alpha _ { s } \left[ 4 \right]$ . The higher spread factor in the LoRa node increases the communication coverage [4]. Hence, we define a view circle centered at the FL gateway with radius $d _ { t }$ for the LoRa ENs transmitting over SF s as follows:

$$
\begin{array} { r } { \mathcal { C } _ { t } = \{ ( x , y , z ) | ( x - x _ { P } ) ^ { 2 } + ( y - y _ { P } ) ^ { 2 } + ( z - z _ { P } ) ^ { 2 } \le d _ { t } ^ { 2 } , } \end{array}
$$

$$
\mathrm { f o r } d _ { t } \mathrm { t h a t } P _ { R x , t } \geq \alpha _ { s } \} .\tag{3}
$$

Indeed, from the point of view of the FL gateway, the possible location of the lost person is on the edge of the view circle $\mathcal { C } _ { t }$ at time slot t. When the FL gateway moves toward the lost person correctly, the radius of the view circle decreases. Based on the spatial geometry of the environment search area, there can be some cases where the UAV is in an NLoS area and moves away from the target location, $d _ { t + 1 } > d _ { t }$ , to bypass the obstacle and provide an LoS link. However, after the UAV finds a location with a LoS link to the target, we can say $h _ { t }$ is a decreasing function concerning $d _ { t }$

<!-- image-->  
Fig. 1. An illustrative example of the system model.

Fig. 1 illustrates our smart SAR system using UAV-assisted LoRa networks during three consecutive time slots t, t  , and $t + 2$ + 1. During these time slots, the portable rescue station equipped with GL gateway receives three messages $m _ { t } , m _ { t + 1 }$ and $\scriptstyle { m _ { t + 2 } } .$ . As we can see in Fig. 1, FL gateway has the view circles of $\mathcal { C } _ { t } , \mathcal { C } _ { t + 1 } ,$ and $\mathcal { C } _ { t + 2 }$ at time slots $t , t + 1$ , and $t + 2 .$ + 1 + 2Following the received message from the FL gateway, the possible locations of the lost person will be on the edges of these view circles. As we can see in Fig. 1, using the FL gateway control algorithm, the FL gateway moves toward the direction to increase the received power $P _ { R x , t }$ during time slots, $P _ { R x , t } <$ $P _ { R x , t + 1 } < P _ { R x , t + 2 }$ . Thus, the FL gateway moves toward the unknown location of the lost person during time slots. During the SAR operation, the GL gateway at the portable rescue station receives data messages from FL gateways over LoRa links. Thus, the FL gateway formation algorithm is run in the portable rescue station, and all the SAR operation details are monitored at the portable rescue in a real-time manner. Considering the stochastic changes in the received power at the FL gateway, designing an FL gateway control policy to move the UAV toward the lost person location is highly challenging, particularly for different SAI scenarios with unknown radio geometry.

## B. Problem Formulation

Our goal is to characterize the FL gateway control policy, which moves the UAV toward the unknown location of the lost person over a future finite horizon $\mathcal { T } _ { t } = \{ t ^ { \prime } | t ^ { \prime } = t + 1 , . . . , t +$ $T \}$ of length $T$ = = + 1 +time slots. The objective of this policy is to minimize the set size of the lost personâs possible location, $| \mathcal { C } _ { t } |$ Following (2) and (3), minimizing the set size of the lost personâs possible location, $| \mathcal { C } _ { t } |$ , is equivalent to increasing the received power, $P _ { R x , t }$ , during the corresponding time slots. The FL gateway control policy at a given slot t depends on the unknown radio geometry of SAI, which is a consequence of the stochastic nature of the wireless channel. Formally, we define a policy $\Pi _ { t } = \{ a _ { t ^ { \prime } } | \forall t ^ { \prime } \in \mathcal { T } _ { t } \}$ for the controller that assigns the following Î  =location of the FL gateway. Consequently, we formulate the FL gateway control problem in our SAR system as follows:

$$
\operatorname* { m a x } _ { \{ \Pi _ { t } \} } \sum _ { t ^ { \prime } = t + 1 } ^ { t + T } \delta ^ { ( t ^ { \prime } - t ) } P _ { R x , t ^ { \prime } } ,\tag{4}
$$

s.t.

$$
a _ { t ^ { \prime } } \in \{ E , W , N , S , H , U , D \} , \forall t ^ { \prime } \in \mathcal { T } _ { t } ,\tag{5}
$$

here, $\delta , 0 < \delta \leq 1$ is a discount factor. Maximizing the objective 0 1function in (4) ensures that the received power at the FL gateway increases while the view circle surface of the FL gateway decreases. Thus, the FL gateways move toward the lost person during the considered time slots.

In practice, the solution of (4) faces the following challenges. First, since the location of the lost person is unknown, it is difficult to obtain the closed expression of the objective function in (4). Second, the received power distribution is a stochastic variable because the radio geometry and wireless channel parameters are random and unknown. The complexity of the stochastic optimization problem in (4) becomes more significant due to the unknown probabilities for possible random network changes, such as the fading over LoRa links and the userâs location. Thus, the FL gateway control problem in (4) is a stochastic optimization problem that does not admit a closed-form solution and has an exponential complexity [32]. Therefore, we propose a framework based on principles of the deep meta-RL for SAR operation in different unknown SAIs to solve the optimization problem in (4) with low complexity and in an adaptive manner. The proposed deep RL method for FL gateway formation in a UAV-assisted LoRa network only takes the UAVâs initial position, the RSSI and SNR of the received LoRa beacon signal as input, then outputs the UAV trajectories after several episodes to move the UAV toward the location of a lost person. By applying deep meta-RL, the controller can integrate the prior FL gateway experience with information collected from the other search environments to rapidly train an adaptive policy model for SAR operation in a new SAR environment.

## III. DEEP META-REINFORCEMENT LEARNINGFOR SAR OPERATION

This section presents the proposed adaptive control policy based on a deep meta-RL framework to solve the FL gateway control problem in (4). Traditional policy gradient-based RL algorithms can only determine the adaptive FL gateway control policy in a given SAI, including a fixed radio geometry. However, the meta-RL framework [33] is a novel learning approach that can integrate the prior FL gateway experience with information collected from the other SAI radio geometry to rapidly train an adaptive policy model for SAR operation in a new SAI. Indeed, the proposed deep meta-RL can obtain the FL gateway control policies that can be quickly updated to adapt to new radio geometry properties using only a few further training steps. Next, we introduce the deep RL algorithm for an adaptive FL gateway control policy in a given environment. Then, we explain the framework of the deep meta-RL algorithm to train an adaptive policy model for a new SAI.

## A. Deep RL Frame Work for a Given Environment

We model the problem in (4) as a partially observable Markov decision process (POMDP) represented by the tuple $\{ S , A , \mathcal { O } , P , R , o _ { 0 } \}$ . where S is the state space, A is the action space, O is the observation space, P is the stochastic state transition function, $P ( s ^ { \prime } , s , a ) = \mathrm { P r } ( s _ { t + 1 } = s ^ { \prime } | s _ { t } =$ $s , a _ { t } = a ) , R _ { t } ( a _ { t } , s _ { t } )$ is the immediate reward function, and $o _ { 0 }$ = ) ( )is the initial observation for the controller of the UAV to move FL gateway [34]. Following POMDP for a given SAI C, the components of our proposed framework are specified as follows:

- Agent: the controller of UAV that moves the FL gateway.

- Actions: the control action of the agent at each time slot t is a $a _ { t } \in A .$ . The UAV can move to any angle in 3D space in the continuous action space setting. Such large action spaces are challenging to explore efficiently and require many training data samples and long hours for tuning the policy parameters of the networks [35]. On the other side, we do not have enough resources and time to gather training data due to the limited UAV battery life, especially in a new and unknown SAR environment. Consequently, the discrete action space is considered as $\mathcal { A } = \{ E , W , N , S , H , U , D \}$ , which includes the set of all =optional actions, including move east, west, north, south, hover, up, and down.

Observations: the observation at time slot t is the RSSI and SNR of received LoRa beacon signal by the FL gateway, and also the current location of UAV, which are received with massage $\mathbf { \nabla } m _ { t }$ . Thus, $\mathbf { \sigma } _ { \pmb { O } _ { t } } = [ \beta _ { t } , \gamma _ { t } , x _ { t } , y _ { t } , z _ { t } ]$ , where $( x _ { t } , y _ { t } ) \in \mathcal { C }$ = [ ]. The observation space O is the set of all possible observations.

. States: the state at time slot t includes the channel parameters such as Ï, Î½, Î·LoS, Î· non-LoS, Îº, and $\varrho _ { t }$ of the LoRa link between FL gateway and the LoRa node which is not observable due to the unknown location of lost person and random radio geometry of SAR environment. In the case of POMDP, we consider the observation history of during H-consecutive previous time slots as the input state [32], [36]. Hence, the state at time slot t in the environment i is $\mathcal { H } _ { t } = \cup _ { h = 0 } ^ { H - 1 } \{ \beta _ { t - h } , \gamma _ { t - h } , a _ { t - h } \}$ containing the RSSI =and SNR of received LoRa beacon signal and the FL gateway control action at time slot t â h. Moreover, these parameters are stored for better future decision-making. The state space S is the set of all possible histories.

- Immediate reward: we define the immediate reward as the received power that FL gateway at time slot t, $R _ { t } = P _ { \mathrm { R x , \mathrm { i } } }$ t which is given by (1).

Episodic return: if $\Lambda _ { t } = \cup _ { \forall t ^ { \prime } \in \mathcal { T } _ { t } } \{ a _ { t ^ { \prime } } , o _ { t ^ { \prime } } \}$ is a trajectory of Î =the POMDP during future T -consecutive time slots, then the stochastic episodic reward function during future T - consecutive time slots is defined as $\begin{array} { r } { R _ { T , t } = \sum _ { t ^ { \prime } = t + 1 } ^ { \bar { t } + T } R _ { t } } \end{array}$

=- Policy: for a given state, the policy is defined as the probability of the agent choosing each action. Our framework uses a functional-form policy parameterized by vector Î¸ to map the input state to the output action. Hence, the policy is expressed as $\pi _ { \pmb { \theta } } ( a _ { t } , \mathcal { H } _ { t } ) = \mathrm { P r } ( a _ { t } | \mathcal { H } _ { t } )$

<!-- image-->  
Fig. 2. The deep RL-based UAV control policy, $\pi _ { \theta } .$

Deep RL aims to find the optimal policy that maximizes episodic return at the FL gateway of UAV-assisted LoRa networks. Given the policy $\pi _ { \theta }$ and stochastic changes over the wireless LoRa link, the unknown probability of trajectory $\Lambda _ { t }$ is equal to $\begin{array} { r } { \operatorname* { P r } ( \Lambda _ { t } , \pmb { \theta } ) = \prod _ { \forall t ^ { \prime } \in \mathcal { T } _ { t } } \pi _ { \pmb { \theta } } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) \operatorname* { P r } \{ o _ { ( t ^ { \prime } + 1 ) } | a _ { t ^ { \prime } } , o _ { t ^ { \prime } } \} } \end{array}$ Pr(Î ) = ( ) Prduring future T -consecutive time slots. For a given SAI, we define the average episodic return for parameter vector Î¸ at time slot t as $\begin{array} { r } { J _ { t } ( \pmb { \theta } ) = \sum _ { \forall \Lambda _ { t } } \operatorname* { P r } ( \Lambda _ { t } , \pmb { \theta } ) R _ { T , t } } \end{array}$ . Given the parametric ( ) =functional-form policy $\pi _ { \pmb { \theta } } .$ Pr(Î ), the goal of the FL gateway controller is to solve the following optimization problem:

$$
\operatorname* { m a x } _ { \{ \pmb { \theta } \in \mathbb { R } ^ { N } \} } J _ { t } ( \pmb { \theta } ) ,\tag{6}
$$

s.t.

$$
0 \leq \pi _ { \pm } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) \leq 1 , \forall a _ { t ^ { \prime } } \in \mathcal { A } , \forall t ^ { \prime } \in \mathcal { T } _ { t } ,\tag{7}
$$

$$
\sum _ { \forall a _ { t ^ { \prime } } \in \mathcal { A } } \pi _ { \pmb { \theta } } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) = 1 , \forall t ^ { \prime } \in \mathcal { T } _ { t } ,\tag{8}
$$

where $T < < N$ and N is the number of parameters in the parametric functional-form policy $\pi _ { \theta }$ . To solve the optimization problem in (6), the FL gateway controller must have full knowledge about the transition probability $\mathrm { P r } ( \Lambda _ { t } , { \boldsymbol { \theta } } )$ , and all possible values of $R _ { T , t }$ Pfor all of the trajectories $\Lambda _ { t }$ )of the POMDP under policy $\pi _ { \theta }$ . However, achieving this knowledge is not feasible, especially for dynamic LoRa wireless channels between mobile FL gateway and LoRa node located at an unknown location. To overcome this challenge, we propose to combine deep neural networks (DNN) with the policy gradient-based RL method. Such a combination was shown in [36], where a DNN learns a mapping from the partially observed state to an action without requiring any lookup table of all trajectories of observation values and policies over time. Consequently, we use a deep RL algorithm that includes a DNN to approximate the policy ÏÎ¸ for solving (6). Our proposed DNN for the deep RL method is presented in Fig. 2. Here, the parameters $\pmb { \theta } \in \bar { \mathbb { R } } ^ { N }$ includes the weights over all connections of the proposed DNN where N is equal to the number of connections [36]. The layers of the proposed deep NN for the implementing policy $\pi _ { \theta }$ are defined as follows:

- Input layer: the input of proposed deep RL policy at time slot t is the history of the POMDP during H-consecutive previous time slots, $\mathcal { H } _ { t }$ . We use an LSTM layer with size H in the input of our policy DNN. This LSTM layer brings the history data of the POMDP during H-consecutive previous time slots, $\mathcal { H } _ { t }$ , for further processing by subsequent layers of artificial neurons. This is because, in our model, the wireless channel affecting POMDP state transitions continuously depends on the spatiotemporal locations of the UAV and the radio geometry of the geographical area of the SAR operation. Thus, we need to use the LSTM layer that aggregates the observations over wireless links during previous time slots of the UAV trajectory and makes a more precise prediction of the next state of the POMDP [16]. Indeed, we use the LSTM layer in the policy function to persist the hidden RSSI and SNR states across the previous FL gateway trajectories for continued adaption to the radio geometry of a given environment.

Hidden layer: the hidden layers are constructed from two Sigmoid layers and three fully connected layers with $H \times$ $\frac { H } { 2 }$ and $\begin{array} { r } { \frac { H } { 2 } \overset { \cdot } { \times } \frac { H } { 4 } } \end{array}$ and $\begin{array} { r } { \frac { H } { 4 } \times T } \end{array}$ connections. A sigmoid layer applies a Sigmoid function to the input such that the output is bounded in the interval (0,1). A fully connected layer multiplies the input by a weight matrix and then adds a bias vector.

Output layer: the output layers include a layer of T Softmax functions as a Classifier layer where each element i in the output vector of size T represents the action index of FL gateway at future time slot t  i. The Softmax layer +applies a Softmax function to the input. A classification layer computes the cross-entropy loss for classification and weighted classification tasks with mutually exclusive classes. In our model, the output shows the index of the actions in the action space A. More precisely, the output $\pmb { y } _ { t } = [ y _ { i , t } ] \in \mathbb { R } ^ { T }$ is a vector of size T actions, where each = [ ]element i in this vector shows the action index of FL gateway at future time slot $t + i .$

+The gradient of objective function in (6) is $\begin{array} { r } { \nabla _ { \theta } J _ { t } ( \theta ) = \sum _ { \forall \Lambda } } \end{array}$ t $\nabla _ { \pmb { \theta } } \operatorname* { P r } ( \Lambda _ { t } , \pmb { \theta } ) R _ { T , t }$ Since âÎ¸ $\begin{array} { r l r } { \mathrm { P r } ( \Lambda _ { t } , \pmb { \theta } ) } & { { } = } & { \frac { \nabla _ { \pmb { \theta } } \mathrm { P r } ( \Lambda _ { t } , \pmb { \theta } ) } { \mathrm { P r } ( \Lambda _ { t } , \pmb { \theta } ) } } \end{array}$ . we can write $\nabla _ { \theta } J _ { t } ( \theta ) = \mathbb { E } _ { \Lambda _ { t } } \nabla _ { \theta }$ Pr( $\mathrm { P r } ( \Lambda _ { t } , { \pmb \theta } ) R _ { T , t }$ . Here, $\begin{array} { r } { \operatorname* { P r } ( \Lambda _ { t } , \pmb { \theta } ) \ = \ \prod _ { t ^ { \prime } = t + 1 } ^ { t + T } \ \pi _ { \pmb { \theta } } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) \operatorname* { P r } \{ \pmb { o } _ { ( ( t ^ { \prime } + 1 ) } | \pmb { o } _ { t ^ { \prime } } , a _ { t ^ { \prime } } \} } \end{array}$ and $\nabla _ { \pmb \theta } \operatorname* { P r } \{ \pmb { o } _ { ( ( t ^ { \prime } + 1 ) } \vert \pmb { o } _ { t ^ { \prime } } , a _ { t ^ { \prime } } \} = 0$ . Thus, $\begin{array} { r } { \nabla _ { \pmb { \theta } } J _ { t } ( \pmb { \theta } ) = \mathbb { E } _ { \Lambda _ { t } } \sum _ { t ^ { \prime } = t + 1 } ^ { t + T } } \end{array}$ PrâÎ¸ $\pi _ { \pmb { \theta } } \big ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } \big ) R _ { T , t }$ = 0 ( ) =. Having enough M samples from log (trajectories $\Lambda _ { t _ { m } }$ , one can approximate the expectation with Îsample-based estimator for $\nabla _ { \pmb { \theta } } J ( \pmb { \theta } ) \ [ 1 6 ]$ . As a result, we use ( )the gradient-ascend algorithm to train the deep RL policy ÏÎ¸ as follows:

$$
\nabla _ { \pmb { \theta } } J _ { t } ( \pmb { \theta } ) \approx \frac { 1 } { M } \sum _ { m = 1 } ^ { M } \left( \sum _ { t ^ { \prime } = t _ { m } + 1 } ^ { t _ { m } + T } \nabla _ { \pmb { \theta } } \log \pi _ { \pmb { \theta } } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) R _ { T , t ^ { \prime } } \right) ,\tag{9}
$$

where $\alpha _ { \mathrm { R L } }$ is the reinforcement learning rate. As shown in Fig. 2, the training batch set $\mathcal { D } _ { \mathrm { R L , t r a i n } }$ is randomly selected from experience memory M. Each training sample m in $\mathcal { D } _ { \mathrm { R L , t r a i n } }$ includes histories during H-consecutive time slots before time slot $t _ { m } , \mathcal { H } _ { t _ { m } }$ , and actions in the trajectory of future T -consecutive time slots after time slot $t _ { m } , \Lambda _ { t _ { m } }$ . In summary, we implement Îthe parametric functional-form policy $\pi _ { \theta }$ with the proposed deep NN in Fig. 2. The proposed deep RL algorithm for FL gateway control is summarized in Algorithm 1. During the SAR time, the deep RL policy is trained with probability Î¶ based on the gradient-ascend algorithm in (9). The deep RL policy is adaptively trained in the training phase using a train data set from experience memory M. In the update phase, the experience memory is updated with history and trajectories during the time slots. The FL gateway moves using this deep RL-based algorithm until the reward $R _ { t }$ becomes more than the defined target reward $R _ { \mathrm { t a r g e t } }$ . This means the UAV is close enough to the lost person, and the received power is more than $R _ { \mathrm { t a r g e t } }$

Algorithm 1: Proposed Deep RL-Based Algorithm for FL   
Gateway Control.   
1: Input: Initial location UAV; RL learning rate $\alpha _ { \mathrm { R L } }$   
training probability $\zeta ;$ a defined deep NN for policy $\pi _ { \theta } ;$   
initial value for $\theta ;$ batch size $M ;$ target reward $R _ { \mathrm { t a r g e t } } .$   
2: Online deep RL   
3: repeat   
4: Exploiting phase: apply deep RL control policy $\pi _ { \theta }$   
depicted in Fig. 2;   
5: Update phase: update the experience memory set   
$\mathcal { M } = \mathcal { M } \cup \left\{ \mathcal { H } _ { t } \cup \Lambda _ { t } \right\}$ ï¼   
= Î6: Training phase: with probability $\zeta ,$ train deep RL   
control policy ÏÎ¸ as follows:   
7: Uniformly select a set of M minibatch samples from   
updated experience memory set M as a training set   
$\mathcal { D } _ { \mathrm { R L , t r a i n } } ;$   
8: Train the deep RL control policy, $\pi _ { \pmb { \theta } } .$ , following the   
gradient-ascend algorithm in (9);   
9: until $R _ { t } > R _ { \mathrm { t a r g e t } }$   
10: Ouput: adaptive control policy $\pi _ { \theta }$ during SAR   
operation time.

Unlike G2G LoRa links, a U2G LoRa link is more robust regarding the fading effects resulting from the spatial geometry. Due to this, the radio geometry characteristics of the U2G LoRa link are more stable in different environments. Thus, given the radio geometry information from the U2G LoRa link, the knowledge gained while learning the FL gateway control policy in a given spacial geometry could be applied when recognizing a new policy in another spacial geometry. Consequently, we will use the knowledge of a trained deep RL policy of FL gateway control in a given environment to design a control policy for a SAR operation in a new SAI.

## B. Deep Meta-RL Framework for New Environments

We introduce the deep meta-RL framework to use the information from a given environment to design a control policy for a new unknown radio geometry. Compared to the deep RL policy, the proposed deep meta-RL policy can integrate the prior experience in one environment with information collected from the FL gateway movement in a new search environment. This leads to a rapid train of an adaptive learning model for FL gateway control. Indeed, the meta-training procedure requires a realization set of state and near-optimal policy [37]. Here, we use the realization set of states and actions in the successful SAR operation in different SAIs to design a policy for the SAI environment. In this case, we define the tasks in our model as follows:

Tasks: given the history of POMDP, task $\tau$ is the realization of FL control policy to solve the optimization problem in (6) in each time slot t at each environment with specific radio geometry. Thus, for a given SAI environment, the $\mathcal { T } _ { t _ { k } } = \{ \mathcal { H } _ { t _ { k } } \cup \Lambda _ { t _ { k } } \}$ includes history and trajectory under = Îcontrol policy at time slot $t _ { k }$ of SAR operation which is accessible from experience memory in Fig. 2.

Meta-train dataset: $\mathcal { D } _ { \mathrm { M e t a - t r a i n } } = \cup _ { k = 1 } ^ { K } \mathcal { T } _ { t _ { k } }$ is defined as K =different tasks in previous successful SAR operation.

Meta-test dataset: $\mathcal { D } _ { \mathrm { M e t a - t e s t } } = \cup _ { e = 1 } ^ { E } \{ \mathcal { H } _ { t _ { e } } \cup a _ { t _ { e } } \}$ is defined =as E different histories and actions in the new environment under target policy $\pi _ { \psi , \phi }$

Here, we use the idea of the most popular policy-gradient meta-RL method, which is called using model agnostic metalearning (MAML) to design the FL gateway control policy in the new search area of interest using the previous successful SAR information [37]. In MAML, the model parameters are explicitly trained such that a small number of gradient steps with a small amount of training data from a new task will produce good generalization performance. In our model, a controller can learn to quickly figure out how to navigate the UAV in a new SAR environment with only a few samples of FL gateway movement and a history of received signal powers. Hence, MAML can be applied to meta-learning for the SAR problem using LoRa UAV networks. During the meta-training procedure, a Meta-train dataset $\mathcal { D } _ { \mathrm { M e t a - t r a i n } }$ is first sampled from experienced memory of previous successful SAR operations. Then, the meta-RL method collects experience information in variable z from $\mathcal { D } _ { \mathrm { M e t a - t r a i n } }$ and uses the deep meta-RL policy function $\pi _ { \phi , \psi }$ to predict actions given the history $\mathcal { H } _ { t }$ of the new environment. Indeed, the deep meta-RL policy function $\pi _ { \phi , \psi } = \pi _ { \psi } \pi _ { \phi , z }$ in which $\pi _ { \psi } = \operatorname* { P r } ( z )$ is the probability of experience information variable z and $\pi _ { \phi , z } = \operatorname* { P r } ( a _ { t } | \mathcal { H } _ { t } , z )$ is the probability of chosen action $a _ { t }$ given the history $\mathcal { H } _ { t }$ )of the new environment and encoded experience information data z from expreince of the previous successful SAR operations. More concretely, the objective of the meta-training procedure is as follows:

$$
\operatorname* { m a x } _ { \{ \pi _ { \phi , \psi } \} } J _ { t } ( \phi , \psi ) ,\tag{10}
$$

s.t.

$$
0 \leq \pi _ { \phi , \psi } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) \leq 1 , \forall a _ { t ^ { \prime } } \in A , \forall t ^ { \prime } \in T ,\tag{11}
$$

$$
\sum _ { \forall a _ { t ^ { \prime } } \in \mathcal { A } } \pi _ { \phi , \psi } \big ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } \big ) = 1 , \forall t ^ { \prime } \in \mathcal { T } ,\tag{12}
$$

where the parametric functional-form $\pi _ { \psi }$ encodes the experience information from tasks in Meta-train dataset $\mathcal { D } _ { \mathrm { M e t a - t r a i n } }$ to help $\pi _ { \phi } ,$ z in finding optimal policy in the new environment. In our deep meta-RL framework, we use a DNN to approximate the policy $\pi _ { \psi }$ , where the parameters Ï include the weights over all connections of the DNN. The proposed deep meta-RL policy for implementing the FL gateway control policy $\pi _ { \phi , \psi }$ includes three main input, hidden, and output layers. The input layer includes two LSTM layers in our proposed deep meta-RL policy. One many-to-one LSTM layer with $H + 1$ cells brings + 1the history of the POMDP during H-consecutive previous time slots of the new environment, $\mathcal { H } _ { t }$ , and also collects experience information in variable z from the previous environment into the subsequent layers of artificial neurons for further processing. Another many-to-one LSTM layer with H cells maps the experience information from the Meta-train dataset $\mathcal { D } _ { \mathrm { M e t a - t r a i n } }$ into a single variable z. The hidden layers include three fully connected and two Sigmoid layers. The three fully connected layers are sequentially with $( \dot { H } + 1 ) \times \frac { H + 1 } { 2 }$ and $\textstyle { \frac { \bar { H } + 1 } { 2 } } \times { \frac { H + 1 } { 4 } }$ and $\textstyle { \frac { H + 1 } { 4 } } \times { \bar { T } }$ connections. The output layer is the final layer in the neural network where desired predictions are obtained. Here, the output layers include a layer of T Softmax functions as a Classifier layer where each element i in the output vector of size T represents the action index of the FL gateway at future time slot $t + i$

+Proposition 1: The gradient of the objective function, $J _ { t } ( \phi , \psi )$ , is approximated by:

$$
\nabla _ { \phi } J _ { t } ( \phi , \psi _ { 0 } ) = \mathbb { E } _ { \Lambda _ { t } } \sum _ { t ^ { \prime } = t _ { m _ { 1 } } + 1 } ^ { t _ { m _ { 1 } } + T } \nabla _ { \phi } \log \pi _ { \phi , z _ { 0 } } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) R _ { T , t ^ { \prime } } ,\tag{13}
$$

$$
\nabla _ { \psi } J _ { t } ( \phi _ { 0 } , \psi ) = \mathbb { E } _ { \Lambda _ { t } } \sum _ { t ^ { \prime } = t + 1 } ^ { t + T } \nabla _ { \psi } \log \pi _ { \phi _ { 0 } , \psi } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) R _ { T , t } ,\tag{14}
$$

where $\pi _ { \phi , \psi } = \pi _ { \psi } \pi _ { \phi , z }$ and $z = \pi _ { \psi }$

= =Proof: The gradient of objective function, $J _ { t } ( \phi , \psi )$ , is $\begin{array} { r } { \nabla _ { \phi , \psi } J _ { t } ( \phi , \psi ) = \sum _ { \forall \Lambda _ { t } } \nabla _ { \phi , \psi } \operatorname* { P r } ( \Lambda _ { t } , \phi , \psi ) R _ { T , t } } \end{array}$ (. Since $\nabla _ { \phi , \psi }$ log $\begin{array} { r } { \operatorname* { P r } ( \Lambda _ { t } , \phi , \psi ) = \frac { \nabla _ { \phi , \psi } \operatorname* { P r } ( \Lambda _ { t } , \phi , \psi ) } { \operatorname* { P r } ( \Lambda _ { t } , \theta ) } } \end{array}$ , we can write $\nabla _ { \phi , \psi } J _ { t }$ $( \phi , \psi ) = \mathbb { E } _ { \Lambda _ { t } } \nabla _ { \phi , \psi } \log \mathrm { P r } ( \Lambda _ { t } , \phi , \psi ) R _ { T , t }$ . Here, $\Pr ( \Lambda _ { t } , \phi , \psi ) =$ $\begin{array} { r } { \prod _ { t ^ { \prime } = t + 1 } ^ { t + T } \pi _ { \phi , \psi } \big ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } \big ) \operatorname* { P r } \{ \pmb { o } _ { \left( ( t ^ { \prime } + 1 ) \right) } \vert \pmb { o } _ { t ^ { \prime } } , a _ { t ^ { \prime } } \} } \end{array}$ and $\nabla _ { \phi , \psi } \mathrm { P r }$ $\{ \pmb { o } _ { ( ( t ^ { \prime } + 1 ) } \vert \pmb { o } _ { t ^ { \prime } } , \ b { a } _ { t ^ { \prime } } \} = 0$ Pr Thus, we have $\nabla _ { \phi , \psi } J _ { t } ( \phi , \psi ) =$ $\begin{array} { r } { \mathbb E _ { \Lambda _ { t } } \sum _ { t ^ { \prime } = t + 1 } ^ { t + T } \nabla _ { \phi , \psi } \log \pi _ { \phi , \psi } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) R _ { T , t } . } \end{array}$

Here, $\nabla _ { \phi } \log \pi _ { \phi , \psi } = \nabla _ { \phi } \log \pi _ { \psi } \pi _ { \phi , z }$ which is equal to $\nabla _ { \phi } \log \pi _ { \psi } + \nabla _ { \phi } \log \pi _ { \phi , z }$ log. Thus, for a given $\psi _ { 0 } , z _ { 0 } = \pi _ { \psi _ { 0 } }$ and $\nabla _ { \phi } \log \pi _ { \phi , \psi _ { 0 } } = \nabla _ { \phi } \log \pi _ { \phi , z _ { 0 } }$ . Thus, we have $\nabla _ { \phi } J _ { t } ( \phi , \psi _ { 0 } ) =$ $\begin{array} { r l } { \mathbb { E } _ { \Lambda _ { t } } \sum _ { t ^ { \prime } = t _ { m _ { 1 } } + 1 } ^ { t _ { m _ { 1 } } + T } \nabla _ { \phi } \log \pi _ { \phi , z _ { 0 } } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) R _ { T , t ^ { \prime } } } & { { } } \end{array}$ , where $z _ { \mathrm { 0 } } = \pi _ { \psi _ { \mathrm { 0 } } } ,$ For a given $\phi _ { 0 } ,$ we have $\nabla _ { \psi } \log \pi _ { \phi _ { 0 } , \psi } = \nabla _ { \psi }$ log $\pi _ { \psi } +$ $\nabla _ { \psi } \log \pi _ { \phi _ { 0 } , z }$ log = log +z which is equal to âÏ ÏÏ. Thus, we have $\begin{array} { r } { \nabla _ { \phi } J _ { t } ( \phi _ { 0 } , \psi ) = \mathbb { E } _ { \Lambda _ { t } } \sum _ { t ^ { \prime } = t _ { m + 1 } } ^ { t _ { m _ { 2 } } + T } \nabla _ { \psi } \log \pi _ { \psi } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) R _ { T , t ^ { \prime } } . } \end{array}$

Having enough $M _ { 1 }$ samples from trajectories $\Lambda _ { t _ { m _ { 1 } } }$ in the dataset $\mathcal { D } _ { \mathrm { M e t a - t e s t } }$ from experienced memory in new $\mathrm { S A I } .$ , one can approximate the expectation with a sample-based estimator for $\nabla _ { \phi , \psi } J _ { t } ( \phi , \psi )$ . Based on Proposition 1, we use the gradient-( )ascend algorithm to train the deep meta-RL policy $\pi _ { \phi , \psi }$ with

<!-- image-->  
Fig. 3. The deep meta-RL-based UAV control policy, $\pi _ { \phi , \psi } .$

respect to Ï as follows:

$$
\begin{array} { r l } & { \nabla _ { \phi } J ( \phi , \psi _ { 0 } ) \approx } \\ & { \frac { 1 } { M _ { 1 } } \displaystyle \sum _ { m = 1 } ^ { M _ { 1 } } ( \displaystyle \sum _ { t ^ { \prime } = t _ { m _ { 1 } } + 1 } ^ { t _ { m _ { 1 } } + T } \nabla _ { \phi } \log \pi _ { \phi , z _ { 0 } } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) R _ { T , t ^ { \prime } } ) , } \\ & { z _ { 0 } = \pi _ { \psi _ { 0 } } ( \mathcal { D } _ { \mathrm { M e t a - t r a i n } } ) , } \\ & { \phi  \phi + \alpha _ { \mathrm { M e t a - R L , 1 } } \nabla _ { \phi } J ( \phi , \psi _ { 0 } ) . } \end{array}\tag{15}
$$

Since the parameters $\phi$ are updated based on collected data in $\mathcal { D } _ { \mathrm { M e t a - t e s t } }$ of the new environment, the phase of updating $\phi$ is called adaption phase. Here, $\alpha _ { \mathrm { M e t a - R L , 1 } }$ is the meta-RL rate for the adaption phase.

Having enough $M _ { 2 }$ samples from trajectories $\Lambda _ { t _ { m _ { 2 } } }$ in the dataset $\mathcal { D } _ { \mathrm { M e t a - t r a i n } }$ Îfrom experienced memory in previous successful SAR operations in the different environments, we use the gradient-ascend algorithm to train the deep meta-RL policy $\pi _ { \phi _ { 0 } , \psi }$ with respect to Ï as follows:

$$
\begin{array} { r l } & { \nabla _ { \psi } J ( \phi _ { 0 } , \psi ) \approx } \\ & { \frac { 1 } { M _ { 2 } } \displaystyle \sum _ { m = 1 } ^ { M _ { 2 } } \left( \sum _ { t ^ { \prime } = t _ { m _ { 2 } } + 1 } ^ { t _ { m _ { 2 } } + T } \nabla _ { \psi } \log \pi _ { \psi } ( a _ { t ^ { \prime } } , \mathcal { H } _ { t ^ { \prime } } ) R _ { T , t _ { m _ { 2 } } } \right) , } \\ & { \psi \gets \psi + \alpha _ { \mathrm { M e t a - R L , 2 } } \nabla _ { \psi } J ( \phi _ { 0 } , \psi ) , } \end{array}\tag{16}
$$

where $\alpha _ { \mathrm { M e t a - R L , 2 } }$ is the meta-RL rate for Meta-train set.

As shown in Fig. 3, the training set $\mathcal { D } _ { \mathrm { M e t a , t r a i n } }$ is randomly selected from experience memory of previous successful SAR operations in different environments. However, each adaptation sample $m _ { 1 }$ includes histories during H-consecutive time slots before time slot ${ t _ { m _ { 1 } } } , \ \mathcal { H } _ { t _ { m _ { 1 } } }$ , and actions in the trajectory of future T -consecutive time slots after time slot $t _ { m _ { 1 } } , \Lambda _ { t _ { m _ { 1 } } }$ in the new environment. In summary, we implement the parametric functional-form policy $\pi _ { \phi , \psi }$ with the proposed deep NN in Fig. 3. The proposed deep meta-RL algorithm for FL gateway control is summarized in Algorithm 2. In the meta-training phase, the deep meta-RL policy is trained using a train data set from experience memory of successful SAR operations in previous environments. In the adaptation phase, the experience memory, including the history and trajectories of the new environment during the SAR operation, is used.

Algorithm 2: Proposed Deep Meta-RL-Based Algorithm   
for FL Gateway Control in New Environment.   
1: Input: Initial location UAV; meta-RL learning rates   
$\alpha _ { \mathrm { M e t a - R L , 1 } }$ and $\alpha _ { \mathrm { M e t a - R L } , 2 } ;$ training probability $\zeta ; \mathbf { a }$   
defined deep NN for policy $\pi _ { \phi , \psi } ;$ initial value for Ï and   
$\psi ;$ batch size $M _ { 1 }$ and $M _ { 2 } ;$ experienced memory $\mathcal { M } _ { I } \mathbf { \dot { \Omega } }$   
target reward $R _ { \mathrm { t a r g e t } }$   
2: Online deep meta-RL   
3: repeat   
4: Exploiting phase: apply deep meta-RL control policy   
$\pi _ { \phi , \psi }$ depicted in Fig. 3;   
5: Update phase: update the experience memory   
$\mathcal { M } = \mathcal { M } \cup \left\{ \mathcal { H } _ { t } \cup \Lambda _ { t } \right\}$   
= Î6: Training phase: with probability $\zeta ,$ train deep   
meta-RL control policy $\pi _ { \phi , \psi }$ as follows:   
7: Uniformly select a set of $M _ { 1 }$ history and action   
samples from $\mathcal { M } _ { 1 }$ as a adaption-training set DMeta-train;   
8: Uniformly select a set of $M _ { 2 }$ history and action   
samples from $\mathcal { M } _ { 2 }$ as a set $\mathcal { D } _ { \mathrm { M e t a } } .$ -test;   
9: Given meta-RL learning rates $\alpha _ { \mathrm { M e t a - R L , 1 } }$ and   
Î±Meta-RL,2, train the deep meta-RL control policy,   
$\pi _ { \phi , \psi } ,$ following the gradient-ascend algorithms in (15)   
to update $\phi$ and (16) to update $\psi ;$   
10: until $R _ { T , t } > R _ { \mathrm { t a r g e t } }$   
11: Ouput: adaptive control policy $\pi _ { \phi , \psi }$ during SAR time   
in the new environment.

The complexity of our approach is determined by the complexity of the deep RL control policy, ÏÎ¸, in Algorithm 1 and the deep meta-RL control policy, $\pi _ { \phi , \psi } .$ , in Algorithm 2. The complexity of the deep RL and meta-RL control policies depends on the number of hidden layers, training examples, features, and nodes at each layer of their NNs [38]. The complexity for training a neural network that has L layers and $n _ { l }$ node in layer l is given by $\begin{array} { r } { \mathcal { O } ( n t \prod _ { l = 1 } ^ { L - 1 } n _ { l } n _ { ( l + 1 ) } ) } \end{array}$ with t training examples and n ( )epochs. Meanwhile, the complexity for one feed-forward propagation will be $\begin{array} { r } { \mathcal { O } ( \prod _ { l = 1 } ^ { L - 1 } n _ { l } \bar { n } _ { ( l + 1 ) } ) } \end{array}$ . On the other hand, LSTM ( )is local in space and time, which means that the input length does not affect the storage requirements of the network [39]. In this case, following the proposed deep NN architectures in Figs. 2 and 3, the complexity of our deep RL and meta-RL algorithms for implementing the FL gateway control policies will be $\mathcal { O } ( M H ^ { 5 } T )$ and $\mathcal { O } ( ( M _ { 2 } H + M _ { 1 } ) H ^ { 5 } T )$ , respectively. ( ) (( + ) )These complexities are polynomial functions of key parameters such as history length, H, number of training samples M, $M _ { 1 }$ , and $M _ { 2 }$ . Moreover, the proposed Algorithms 1 and 2 are categorized as the gradient-based MAML algorithm. Thus, following the mathematical proof in [40], the Algorithms 1 and 2 will converge to an -first-order stationary point for any positive  using the second-order information of loss functions. Moreover, in Algorithm 2 an online meta-learning setting is applied which merges ideas from both the meta-learning and online learning paradigms to capture training data samples iteratively from the new SAR environment. In our proposed framework, if multiple persons are present in a given environment, multiple

LoRa packets including the identification numbers of the persons are received at the flying LoRa gateway. Our proposed algorithm only considers the power of received data packets from the target identification number and moves the UAV in a direction that decreases the received power from that target packet. However, our deep-meta-Rl policy can be extended for multiple-lost-person scenarios. In this regard, we should use deep reinforcement learning to solve multi-objective problems where a vector of multiple received power signals from different lost persons is given. In more detail, the objective of the optimization problem in (4) changes to $\begin{array} { r } { \sum _ { \forall i \in \mathrm { P o I s } } \sum _ { t ^ { \prime } = t + 1 } ^ { \check { t } + T } \delta ^ { ( t ^ { \prime } - t ) } \dot { w _ { i } } P _ { R x , t ^ { \prime } , i } } \end{array}$ . This objective is the weighted summation of the received powers from the different lost persons. Then, based on the weight in the objective function for each victim, $w _ { i }$ , the proposed deep meta-RL-based algorithm moves the UAV toward the victim with the higher priority.

## IV. EXPERIMENTAL SETUP

This section presents and discusses the implementation of our UAV-assisted LoRa networks and environments for our experimental setup.

## A. Considered Hardware

Our experimental setup of the UAV-assisted LoRa network includes the LoRa end node, FL, and GL gateways. In our setup, all the designed nodes and gateways are powered using lithium polymer (Li-Po) batteries with an output voltage of 3.7V and a capacity of 1100 mAh. We have designed our printed circuit boards (PCBs) to assemble LoRa node FL gateways on them. ATmega328, a single-chip microcontroller created by Atmel in the megaAVR family, is used in the LoRa nodes and gateways and programmed in C language [41]. Our setup uses the LoRa Ra-02 module from AI-Thinker, equipped by a LoRa SX1278 Semtech core [41] and [42].

The designed LoRa node transmits a beacon packet using the LoRa module connected to the commercial external folded dipole antenna on the ISM frequency band at 433MHz. The detail of the LoRa node is shown in Fig. 4(a). The FL gateway board is equipped with LoRa Ra-02 and GPS modules. The LoRa Ra-02 module is connected to a 433 Mhz antenna, and the GPS module has a square-shaped receiver GPS antenna. The designed FL gateway board is shown in Fig. 4(b). The dimensions of the FL gateway board are $2 9 5 \times 6 0 \times 2 0$ mm, and its weight is 100 gr. Thus, the designed FL gateway weight is low enough for commercial drones to carry it. We have mounted the FL gateway board over DJI Phantom 4 Pro. We firmly fix the gateway node under DJI Phantom 4 Pro to use the maximum antenna radiation while the LoRa antenna vertically points toward the earthâs surface. Our designed board for the GL gateway consists of a LoRa Ra-02 module connected to a 433MHz antenna. The head of the rescue operation can connect to the GL gateway via a USB cable or Bluetooth wireless link. The GL gateway setup is shown in Fig. 4(c). The GL gateway receives data packets from FL gateways using the LoRa module. It transmits these received packets to the portable computer, such as a laptop, over a USB cable or to the mobile phone via Bluetooth. In this case, the rescue operation can be monitored and analyzed using real-time data gathered on a computer or mobile phone. The real-time received data packets are used to run our proposed deep reinforcement algorithms. Following our proposed deep RL algorithms, the control policy determines the subsequent movement of the UAV, and then the pilot moves the drone toward that direction.

<!-- image-->

(a) Assembled LoRa end node.  
<!-- image-->

(b) Assembled Flying LoRa gateway node.  
<!-- image-->  
(c)Assembled ground LoRa gateway node.  
Fig. 4. Assembled nodes of the UAV-Assisted LoRa Network.

Since the battery of the portable wireless end device is a limiting factor in a rescue operation, we use LoRa transmission with robust signals for transmission over long distances and also consume less power consumption in comparison with other modules [43]. Our designed LoRa end node periodically transmits a unique identification code with a low bit rate and power over a high communication range. Our designed LoRa end node, on average, consumes $\begin{array} { r } { \frac { 0 . 1 * 8 . 5 + \stackrel {  } { 0 } . 0 5 * 1 2 0 + 3 . 8 5 * 0 . 0 0 0 3 } { A } = 1 . 7 1 3 \ : \mathrm { m A } } \end{array}$ in each work cycle, where each work cycle takes 4 seconds. So, it can transmit beacon signal for $\mathrm { \frac { 4 0 0 0 m A h } { 1 . 7 1 3 m A } = 2 3 3 5 . 0 2 }$ hours which is around $\begin{array} { r } { \frac { 2 3 3 5 . 0 2 } { 2 4 } = 9 \dot { 7 } } \end{array}$ = 233days or 3 months [44].

= 97We do not use a directional antenna and GPS module in our system for the following reasons. The distance between the antenna at each MIMO LoRa system is 17,27cm and 34,62cm for LoRa frequency bands of 868MHz and 433 MHz [45], [46]. Thus, the LoRa node size equipped with MIMO antenna will be significant, so commercial drones can not carry it. However, one of our goals is to design a practical solution, including lightweight and small LoRa nodes, so that commercial drones can carry them. Moreover, we do not equip the LoRa node with the GPS module for two reasons. First, there is not enough GPS coverage in some outdoor rescue cases, such as when the lost person has fallen in a slotted canyon. In this regard, GPS signal quality can be affected by various things such as mainly rocks and atmospheric conditions. If these things affect the GPS module, it will consume more power as it tries to get a good GPS fix [47]. Second, the GPS module consumes high power compared to LoRa module [47], [48].

## B. Experimental Setup

The experimental tests have been done at the Campus of Shahid Chamran University and the Mongasht mountain ranges, near the areas of Ghaletol city, Khuzestan province, Iran. For the lost person, the LoRa node is held in the studentâs hand while the students move to the unknown location in the target area. Since we want to evaluate our SAR system in the different radio geometry, including both LoS and NLoS links, we have done our experiments on three target areas: a university campus, a wide plain, and a slotted canyon. We locate the lost person in two different locations on the university campus. One of the locations is between closely located campus buildings, which shadow the LoRa node completely. We consider this location to be a non-LoS-covered area. In the other location, the LoRa node is in the open area without any surrounding campus buildings. When the target area of the lost person is a wide plain, there are mostly LoS paths between GL or FL gateways and the LoRa node. However, when the lost person is in the slotted canyon, there are no LoS paths between GL or FL gateways and the LoRa node, and the LoRa node is in the shadowing area of mountain walls around the slotted canyon. In Fig. 5, the geographical map of the experimental scenarios has been shown.

## V. PERFORMANCE ANALYSIS

In this section, we evaluate the performance of our proposed deep meta-RL approach for SAR operation using the real measurements of the UAV-assisted LoRa network for the scenarios at Mongasht mountain ranges. In our measurement, the duration of each time slot is 2 seconds; the maximum UAV speed is 20 meters per second. We used one UAV with a battery lifetime of 20 minutes. Our practical measurement is done every 2 seconds. However, the LoRa node sends a beacon signal every 4 s, and the FL gateway sends a message to the GL gateway every 1 s. This leads to the control movement action being sent to the FL gateway almost every 2 s. The UAV movement direction remains unchanged until the next control action is sent to the UAV. We compare the deep meta-RL policy with optimal, greedy, deep RL, and AC-based RL policies as the benchmarks. In the optimal policy, we give the unknown location of the lost person to the UAV pilot, and then the UAV directly moves toward the target location. Under the greedy policy, there are two phases: sense and action. The UAV starts the sense phase with a probability of 0.1, in which the UAV sequentially moves north, east, south, and west for 3-time slots to measure received power. The UAV starts the action phase with a probability of 0.9, in which the UAV moves toward the direction with the highest received power at the previous sense phase. The AC RL-based policy [49] is an actorcritic algorithm that updates the action-value neural network based on the state-value or critic error. The target state-value function is determined based on $V ^ { * } ( \mathcal { H } _ { t + 1 } ) = R _ { t } + \delta V ^ { * } ( \mathcal { H } _ { t } )$ . If the critic error $V ( \mathcal { H } _ { t } ) - V ^ { * } ( \mathcal { H } _ { t } )$ is positive, then the action $a _ { t }$ is applied in state $\mathcal { H } _ { t }$ is a good option, and the target action-value should be maximized. Otherwise, the probability of selecting $a _ { t }$ applied in state $\mathcal { H } _ { t }$ must be decreased. The value of system parameters and deep NN hyperparameters of our framework are shown in Table I.

<!-- image-->

(a)A wide plain near Qaletol city,Khuzestan province, Iran.  
<!-- image-->

(b)A slotted canyon in the Mongasht mountain ranges, Iran.  
<!-- image-->  
(c) Campus of Shahid Chamran University of Ahvaz, Iran.  
Fig. 5. Google Earth images of the experimental scenarios.

TABLE I LIST OF PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>LoRa spread factor</td><td rowspan=1 colspan=1>12</td></tr><tr><td rowspan=1 colspan=1>Radius of SAI</td><td rowspan=1 colspan=1>8km</td></tr><tr><td rowspan=1 colspan=1>Time slot duration</td><td rowspan=1 colspan=1>2 seconds</td></tr><tr><td rowspan=1 colspan=1>Maximum UAV speed</td><td rowspan=1 colspan=1>20 m/s</td></tr><tr><td rowspan=1 colspan=1>Maximum LoRa node transmission power $( P _ { T x , t } )$ </td><td rowspan=1 colspan=1>20 dBm</td></tr><tr><td rowspan=1 colspan=1>Beacon interval T</td><td rowspan=1 colspan=1>4 second</td></tr><tr><td rowspan=1 colspan=1>Batch size</td><td rowspan=1 colspan=1>32</td></tr><tr><td rowspan=1 colspan=1>Epochs for deep RL NN</td><td rowspan=1 colspan=1>64</td></tr><tr><td rowspan=1 colspan=1>Initial training probability (S)</td><td rowspan=1 colspan=1>0.2</td></tr><tr><td rowspan=1 colspan=1> Initial RL learning rate (QRL)</td><td rowspan=1 colspan=1>0.001</td></tr><tr><td rowspan=1 colspan=1>Initial meta-RL learning rates(QMeta-RL,1,eta-RL,2)</td><td rowspan=1 colspan=1>(0.001,0.01)</td></tr><tr><td rowspan=1 colspan=1>Epochs for deep meta-RL NN</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1>Optimizer algorithm</td><td rowspan=1 colspan=1>Adam</td></tr></table>

<!-- image-->  
Fig. 6. Received power at FL gateway versus rescue time slots in wide plain environment.

In Fig. 6, we show the received power at the FL gateway versus the rescue time slots in the wide plain environment. From Fig. 6, we observe that the received power at the FL gateway increases much faster during SAR operation under the optimal policy than other solutions. However, when the greedy algorithm is used, the received power at the FL gateway increases more slowly. The performance of the proposed deep learning policies is between optimal and greedy policies. As seen from Fig. 6, when the UAV initial location is . R far from the lost person, the received 0 8power at the FL gateway reaches its maximum value around SAR time slot 300, 600, 700, 800 under the optimal, deep AC RL, deep RL, and greedy algorithms, respectively. Under the greedy policy, the UAV moves in the direction with the highest power received in the previous time slots. This may hold the greedy algorithm in the local optimal solution instead of the global one and increase the rescue time needed to find the lost person. However, when we use another algorithm, such as DRL, the UAV will process the UAV locations, movements, and received power values during previous time slots and move toward the target location faster. However, the greedy algorithm does not include any learning strategy and does not use the knowledge of the past received power to choose the subsequent control movement for the UAV. Moreover, the greedy and deep learning policies converge in the plain environment and the UAV hovers over the lost person location. This is because, in contrast to the slotted canyon scenario, there is mostly a LoS link between a lost person and the FL gateway during SAR operation in the plain environment. Under the deep learning policy, when we start the initial location of the UAV at a 0.4 radius of a plain environment, the UAV can find the lost person at time slot 400. In contrast, when the UAVâs initial location is at a 0.8 radius of the plain environment, the lost person is found at time slot 800.

<!-- image-->  
Fig. 7. Received power at FL gateway versus rescue time slots in slotted canyon environment.

In Fig. 7, we show the received power at the FL gateway versus rescue time slots in the slotted canyon environment. For the deep meta-RL policy, we have used the data of previous experiences of different SAR operations in the plain environment, where the initial locations of the UAV have been changed, and the data of SAR has been saved in the memory. Then, this data is used as the $\mathcal { D } _ { \mathrm { M e t a - t r a i n } }$ in Algorithm 1. From Fig. 7, we observe that the received power at the FL gateway under the deep meta-RL policy achieves its maximum value at SAR time slot 50. In contrast, the FL gateway moves to the location with the maximum received power under the deep RL and AC RL policies after around 140 and 121 time slots, respectively. Moreover, on average, the received power at the FL gateway under the deep AC RL policy is 46% more than deep RL. However, on average, the received power at the FL gateway under the deep meta-RL policy is 72% and 63% more than deep RL and AC RL policies, respectively.

In Fig. 8, we show the FL gateway horizontal distance from the lost person during SAR time slots in the slotted canyon environment. From Fig. 8, we observe that the deep RL, AC RL, and meta-RL-based policies can finally find the lost person. However, the greedy algorithm does not converge to the lost personâs location during SAR operation. As shown in Fig. 8, the UAV hovers over the lost person location after 31 time slots under the optimal policy. The deep RL, AC RL, and deep meta-RL-based policies find the lost person at time slots 51, 111, and 141, respectively. Moreover, the FL gateway distance between UAV and lost person under the deep meta-RL-based policy is, on average, 46% and 22% less the deep RL and AC RL policies, respectively.

<!-- image-->  
Fig. 8. UAV horizontal distance from lost person in slotted canyon environment.

<!-- image-->  
Fig. 9. The percentage of SAR time duration difference from optimal policy.

To show the robustness of our proposed scheme, we have changed the initial location of the UAV. This random initial location changes the spatial geometry, including obstacles between the UAV and the victim in the SAR environment. Then, we use the meta-RL-based policy that has been previously trained when the initial location of the UAV was at the edge of the SAR environment. This scenario allows us to evaluate the robustness of our solution to new unknown random changes in the blockages over the radio channel that were not considered in the training dataset. In Fig. 9, we show the percentage of SAR time duration difference from the optimal policy. From Fig. 9, we can see that the percentage of SAR time deviation decreases when we move the initial location of the UAV away from the lost person. This is because when the UAV is far away from the lost person, there is enough time for the deep NN-based policy to adapt itself to the new random changes over the wireless channel. Moreover, as we can see in Fig. 9, on average, the percentage of SAR time difference between optimal and deep meta-RL policies is 34% and 45% less than SAR time difference between optimal and deep RL policies for plain and canyon environments, respectively. This means that the meta-RL policy is more robust to the random changes in the environments because, compared to the deep RL policy, the performance of the deep meta-RL policy is much closer to the optimal policy.

<!-- image-->  
Fig. 10. UAV energy consumption versus rescue time slots in slotted canyon environment.

<!-- image-->  
Fig. 11. UAV trajectory during SAR operation at a slotted canyon. Lost person location is 31o35 18.24N and 50o1 37.44E.

One of the main critical limitations in UAV-assisted SAR operation is flight endurance, which is limited due to the limited power supply provided by UAV batteries. In Fig. 10, we show the UAV energy consumption versus the rescue time slots in the slotted canyon environment. From Fig. 10, the UAV consumes the highest energy under the greedy control policy, around kJ during SAR time. Moreover, we observe that, on average, the UAV energy consumption under the deep meta-RL policy is 57% and 23% less than the deep RL and AC RL policies, respectively. The UAV energy consumption under the proposed deep meta-RL is closest to the optimal policy.

In Fig. 11, we show the UAV trajectory at a slotted canyon during SAR operation. From Fig. 11, we observe that the UAV under the deep meta-RL and RL-based policies finally hovers over the lost personâs location. The greedy algorithm moves the UAV toward the lost personâs location, while the UAV cannot hover over the exact target location during SAR operation time. As shown in Fig. 11, the average distance between UAV trajectories under the deep meta-RL and deep RL-based policies from the UAV trajectory under optimal policy are 619 and 1930 meters during the SAR operation time.

<!-- image-->  
Fig. 12. UAV horizontal distance from lost person in the campus of Shahid Chamran University of Ahvaz, Iran.

<!-- image-->  
Fig. 13. UAV trajectories during SAR operation in the campus of Shahid Chamran University of Ahvaz, Iran.

In Fig. 12, we show the FL gateway horizontal distance from the lost person during SAR time slots for the non-LoS scenarios in the campus area. As shown in Fig. 12, the UAV hovers over the lost personâs location after the 80 time slots when the optimal and deep meta-RL-based policies are used. The deep and AC RL policies find the lost person in time slot 150. Moreover, the FL gateway distance between UAV and lost person under the deep meta-RL-based policy is, on average, 32% and 21% less the deep RL and AC RL policies, respectively.

In Fig. 13, we show the UAV trajectory during SAR operation over the campus of Shahid Chamran University. From Fig. 13, we observe that the UAV under the deep meta-RL policy hovers over the lost personâs location much sooner than the greedy algorithm. As we can see in Fig. 13, the average distance between

<!-- image-->  
Fig. 14. SAR time slots versus, spreading factors at Shahdi Chamran university campus.

TABLE II  
SAR DURATION AND CV OF FL GATEWAY DISTANCE
<table><tr><td>Policy Parameters</td><td>SAR duration</td><td>Cv</td></tr><tr><td> $H = 1 0 , \zeta = 0 . 1$ </td><td>=</td><td>-</td></tr><tr><td> $H = 4 0 , \zeta = 0 . 1$ </td><td>83</td><td>0.903</td></tr><tr><td> $H = 1 0 , \zeta = 0 . 6$ </td><td>102</td><td>0.524</td></tr><tr><td> $H = 4 0 , \zeta = 0 . 6$ </td><td>61</td><td>0.706</td></tr></table>

UAV trajectories under the greedy algorithm and deep meta-RLbased policy is 58 and 180 m during the SAR operation time for LoS and non-LoS scenarios, respectively.

We have evaluated the effect of the spread factor in our new measurement at the campus of Shahid Chamran University for two LoS and non-LoS scenarios (See Fig. 5(c)). In Fig. 14, we show the SAR time slots to find the lost person in the LoS and non-LoS scenarios over the campus of Shahid Chamran University. As shown in Fig. 14, the SAR time slots are 19% less for spread factor 12 than for spread factor 8. This is because when the higher spread factor is used in the LoRa transmission, the LoRa node achieves a greater coverage range. From Fig. 13, we observe that the SAR time slots in the non-LoS scenario are 52% more than in the LoS scenario because there are blocking obstacles and also shadowing areas that the UAV requires to bypass them to find the lost person location in the non-LoS scenario.

In Table II, we show the effect of observation history length, H, and training probability, Î¶, of the proposed meta-RL-based policy on the SAR operation. Here, we calculate the coefficient of variation (CV) of the FL gateway distance to the lost person over the campus of Shahid Chamran University for the non-LoS scenarios. The CV is a statistical metric to compare the degree of variation from the FL gateway distance to the lost person location during SAR operation. When the observation history length and the training probability are low, $H = 1 0 , \zeta = 0 . 1$ , the UAV gets stuck in the local optimal solution, which is not the exact location of the lost person. As we increase the observation history length and the training probability to $H = 4 0 , \zeta = 0 . 6 .$ , the variance of the search time decreases, and the UAV finds the target location.

Besides this, increasing the observation history length and the training probability increases the total search time.

## VI. CONCLUSION

In this paper, we have introduced an intelligent SAR system based on a UAV-assisted LoRa network for highly remote areas such as mountain ranges. Specifically, we have designed and implemented an artificial intelligence-empowered SAR operation framework for different unknown SAR environments. We have modeled the problem of the FL gateway control in the SAR system using the UAV-assisted LoRa network as a partially observable Markov decision process. Then, we proposed a deep meta-RL-based policy to control the FL gateway trajectory during SAR operation. To initialize our deep meta-RL-based policy, a deep RL-based policy determines the adaptive FL gateway trajectory in a given radio geometry. Then, as a general solution, our deep meta-RL framework is used for SAR in any new environment. Indeed, deep meta-RL-based policy integrates the information of the prior FL gateway experiences from the previous SAR operation and then rapidly adapts the SAR policy model for SAR operation in a new environment. We have experimentally implemented a UAV-assisted LoRa network. Then, we tested our proposed SAR system in three different areas: the Shahid Chamran University campus, a wide plain, and a slotted canyon at Mongasht mountain ranges, Iran. Practical results show that if the deep meta-RL policy is applied instead of the deep RL one to control the UAV, the number of SAR time slots decreases from 141 to 50 in the slotted canyon environment. Moreover, we observe that, on average, the UAV energy consumption under the deep meta-RL policy is 57% and 23% less than the deep RL and AC RL policies, respectively. In addition, the SAR time slots are 19% less for LoRa spread factor 12 than for spread factor 8.

## REFERENCES

[1] W. Saad, M. Bennis, and M. Chen, âA vision of 6G wireless systems: Applications, trends, technologies, and open research problems,â IEEE Netw., vol. 34, no. 3, pp. 134â142, May/Jun. 2020.

[2] A. Fotouhi et al., âSurvey on UAV cellular communications: Practical aspects, standardization advancements, regulation, and security challenges,â IEEE Commun. Surv. Tut., vol. 21, no. 4, pp. 3417â3442, Fourth Quarter 2019.

[3] L. Chettri and R. Bera, âA comprehensive survey on Internet of Things (IoT) toward 5G wireless systems,â IEEE Internet Things J., vol. 7, no. 1, pp. 16â32, Jan. 2020.

[4] L. Alliance, âWhite paper: A technical overview of LoRa and LoRaWAN,â in Proc. IEEE Conf. Comput. Commun., San Ramon, CA, USA, 2015, pp. 7â11.

[5] K.-H. Lam, C.-C. Cheung, and W.-C. Lee, âRSSI-based LoRa localization systems for large-scale indoor and outdoor environments,â IEEE Trans. Veh. Technol, vol. 68, no. 12, pp. 11 778â11 791, Dec. 2019.

[6] N. Podevijn et al., âTDoA-based outdoor positioning in a public LoRa network,â in Proc. Eur. Conf. Antennas Propag., London, UK, 2018, pp. 1â4.

[7] Y.-C. Lin, C.-C. Sun, and K.-T. Huang, âRSSI measurement with channel model estimating for IoT wide range localization using lora communication,â in Proc. Int. Symp. Intell. Signal Process. Commun. Syst., Taipei, Taiwan, 2019, pp. 1â2.

[8] J. Fang, L. Wang, Z. Qin, and B. Lu, âLoRa-based outdoor 3D localization,â in Proc. IEEE Conf. Comput. Commun. Workshops, New York, NY, USA, 2022, pp. 1â2.

[9] F. Mazzola et al., âTaormina: A LoRa-based localization scheme for smart road scenarios,â in Proc. Int. Conf. Elect. Comput. Commun. Mech. Eng., Mauritius, Mauritius, 2021, pp. 1â6.

[10] O. Dieng, C. Pham, and O. Thiare, âOutdoor localization and distance estimation based on dynamic RSSI measurements in LoRa networks: Application to cattle rustling prevention,â in Proc. Int. Conf. Wirel. Mobile Comput. Netw. Commun., Barcelona, Spain, 2019, pp. 1â6.

[11] G. M. Bianco, R. Giuliano, G. Marrocco, F. Mazzenga, and A. Mejia-Aguilar, âLoRa system for search and rescue: Path-loss models and procedures in mountain scenarios,â IEEE Internet Things J., vol. 8, no. 3, pp. 1985â1999, Feb. 2021.

[12] G. M. Bianco and G. Marrocco, âRadio frequency identification and localization by wearable LoRa for search and rescue in mountains,â in Proc. IEEE Int. Conf. RFID, Las Vegas, NV, USA, 2022, pp. 120â125.

[13] G. M. Bianco, A. Mejia-Aguilar, and G. Marrocco, âPerformance evaluation of LoRa LPWAN technology for mountain search and rescue,â in Proc. Int. Conf. Smart Sustain. Technol., Split, Croatia, 2020, pp. 1â4.

[14] J. Gu, H. Wang, G. Ding, Y. Xu, and Y. Jiao, âUAV-enabled mobile radiation source tracking with deep reinforcement learning,â in Proc. Int. Conf. Wirel. Commun. Signal Process., Nanjing, China, 2020, pp. 672â678.

[15] O. Mihatsch and R. Neuneier, âRisk-sensitive reinforcement learning,â Mach. Learn., vol. 49, pp. 267â290, Nov. 2002.

[16] I. Goodfellow, Y. Bengio, and A. Courville, Deep Learning. Cambridge, MA, USA: MIT Press, 2016, http://www.deeplearningbook.org

[17] O. A. Saraereh, A. Alsaraira, I. Khan, and P. Uthansakul, âPerformance evaluation of UAV-enabled LoRa networks for disaster management applications,â Sensors, vol. 20, no. 8, Apr. 2020, Art. no. 2396.

[18] V. A. Dambal, S. Mohadikar, A. Kumbhar, and I. Guvenc, âImproving LoRa signal coverage in urban and sub-urban environments with UAVs,â in Proc. Int. Workshop Antenna Technol., Miami, FL, USA, 2019, pp. 210â213.

[19] G. M. Bianco, A. Mejia-Aguilar, and G. Marrocco, âMeasurements and modeling of radiohelmet-UAV LoRa links in a mountain canyon,â in Proc. Eur. Conf. Antennas Propag., Madrid, Spain, 2022, pp. 1â4.

[20] V. Delafontaine, F. Schiano, G. Cocco, A. Rusu, and D. Floreano, âDroneaided localization in LoRa IoT networks,â in Proc. IEEE Int. Conf. Robot. Automat., Paris, France, 2020, pp. 286â292.

[21] B. Jia, W. Qiao, B. Huang, H. Yang, and E. Wang, âSequentially localizing lora terminals with a single UAV,â in Proc. IEEE Wirel. Commun. Netw. Conf., Glasgow, U.K., 2023, pp. 1â6.

[22] H. Aghajari, S. Ahmadinabi, H. B. Babadegani, and M. N. Soorki, âEmpirical performance analysis and channel modeling of UAV-assisted LoRa networks,â in Proc. Int. Conf. Elect. Eng., 2022, pp. 463â468.

[23] G. M. Bianco, A. Mejia-Aguilar, and G. Marrocco, âNumerical and experimental evaluation of radiohelmet-to-UAV LoRa links,â in Proc. Gen. Assem. Sci. Symp. Int. Union Radio Sci., Rome, Italy, 2021, pp. 1â4.

[24] D. Cavaliere, V. Loia, A. Saggese, S. Senatore, and M. Vento, âSemantically enhanced UAVs to increase the aerial scene understanding,â IEEE Trans. Syst., Man, Cybern. Syst., vol. 49, no. 3, pp. 555â567, Mar. 2019.

[25] X. Lin, Y. Zhou, Y. Liu, and C. Zhu, âLevel line guided interest point detection,â IEEE Signal Process. Lett., vol. 30, pp. 863â867, 2023.

[26] Y. Cai, E. Zhang, Y. Qi, and L. Lu, âA review of research on the application of deep reinforcement learning in unmanned aerial vehicle resource allocation and trajectory planning,â in Proc. Int. Conf. Mach. Learn. Big Data Bus. Intell., Shanghai, China, 2022, pp. 238â241.

[27] S. Kulkarni, V. Chaphekar, M. M. Uddin Chowdhury, F. Erden, and I. Guvenc, âUAV aided search and rescue operation using reinforcement learning,â SoutheastCon, Raleigh, NC, USA, vol. 2, pp. 1â8, Mar. 2020.

[28] M. Schwartz, Mobile Wireless Communications. Cambridge, U.K.: Cambridge Univ. Press, 2004.

[29] B. Hua et al., âChannel modeling for UAV-to-ground communications with posture variation and fuselage scattering effect,â IEEE Trans. Commun., vol. 71, no. 5, pp. 3103â3116, May 2023.

[30] A. Al-Hourani, âLine-of-sight probability and holding distance in nonterrestrial networks,â IEEE Commun. Lett., vol. 28, no. 3, pp. 622â626, Mar. 2024.

[31] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âMobile unmanned aerial vehicles (UAVs) for energy-efficient Internet of Things communications,â IEEE Trans. Wireless Commun., vol. 16, no. 11, pp. 7574â7589, Nov. 2017.

[32] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction. 2nd ed. Cambridge, MA, USA: MIT Press, 2018.

[33] T. Hospedales, A. Antoniou, P. Micaelli, and A. Storkey, âMeta-learning in neural networks: A survey,â IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 9, pp. 5149â5169, Sep. 2022.

[34] M. Hausknecht and P. Stone, âDeep recurrent Q-learning for partially observable MDPs,â Jan. 2017, arXiv:1507.06527v4.

[35] L. Metz, J. Ibarz, N. Jaitly, and J. Davidson, âDiscrete sequential prediction of continuous actions for deep RL,â Jun. 2019, arXiv:1705.05035v3.

[36] A. P. A. Torres, C. B. D. Silva, and H. T. Filho, âAn experimental study on the use of LoRa technology in vehicle communication,â IEEE Access, vol. 9, pp. 26 633â26 640, 2021.

[37] C. Finn, P. Abbeel, and S. Levine, âModel-agnostic meta-learning for fast adaptation of deep networks,â in Proc. Int. Conf. Mach. Learn., Sydney, Australia, 2017, pp. 1126â1135.

[38] P. Orponen, âComputational complexity of neural networks: A survey,â Nordic J. Comput., vol. 1, pp. 94â110, May 2000.

[39] E. Tsironi, P. Barros, C. Weber, and S. Wermter, âAn analysis of convolutional long-short term memory recurrent neural networks for gesture recognition,â Neurocomputing, vol. 268, pp. 76â86, Dec. 2017.

[40] A. Fallah, A. Mokhtari, and A. Ozdaglar, âOn the convergence theory of gradient-based model-agnostic meta-learning algorithms,â in Proc. Int. Conf. Artif. Intell. Statist., 2020, pp. 1082â1092.

[41] Arduino Uno description. Oct. 2024. [Online]. Available: https://docs. arduino.cc/resources/datasheets/A000066-datasheet.pdf

[42] lora-core SX1278 description. May 2020. [Online]. Available: https: //www.semtech.com/products/wireless-rf/lora-core/sx1278

[43] LoRa and LoRaWAN timing. 2021. [Online]. Available: https://ecsxtal. com/lora-lorawan-timing/

[44] LoRa module datasheet: Stm32wle5xx stm32wle4xx. Dec. 2022. [Online]. Available: https://www.st.com/resource/en/datasheet/stm32wle5c8.pdf

[45] H. Ma, G. Cai, Y. Fang, P. Chen, and G. Han, âDesign and performance analysis of a new STBC-MIMO LoRa system,â IEEE Trans. Commun., vol. 69, no. 9, pp. 5744â5757, Sep. 2021.

[46] J.-M. Kang, âMIMO-LoRa for high-data-rate IoT: Concept and precoding design,â IEEE Internet Things J., vol. 9, no. 12, pp. 10 368â10 369, Jun. 2022.

[47] K. Chen, G. Tan, J. Cao, M. Lu, and X. Fan, âModeling and improving the energy performance of GPS receivers for location services,â IEEE Sensors J., vol. 20, no. 8, pp. 4512â4523, Apr. 2020.

[48] J. Finnegan, S. Brown, and R. Farrell, âModeling the energy consumption of LoRaWAN in ns-3 based on real world measurements,â in Proc. Glob. Inf. Infrastructure Netw. Symp., Thessaloniki, Greece, 2018, pp. 1â4.

[49] V. Mnih et al., âAsynchronous methods for deep reinforcement learning,â in Proc. Int. Conf. Mach. Learn., New York City, NY, USA, 2016, pp. 1928â1937.

<!-- image-->

Mehdi Naderi Soorki received the PhD degree in telecommunication networks from the Isfahan University of Technology, Iran, in 2018. He held a research scholar position with the Wireless at VTGroup, Virginia Polytechnic Institute and State University, USA, from 2015 to 2018. Currently, he is an assistant professor with the engineering faculty of Shahid Chamran University (SCU) of Ahvaz, Iran. Where he directs the intelligent wireless networks (IWiN) research laboratory, within the Electrical Engineering group at SCU. He is also the entrepreneurial leader of the research group for wireless networks-based intelligent applications (Winiapp), the advanced technologies incubator Center of SCU. His main research interests include designing algorithms and architectures for next generation wireless networks. In addition to these, he also focuses on developing artificial intelligence-empowered solutions for smart applications in future smart cities and smart nomadic villages.

<!-- image-->

Hossein Aghajari received the BSc degree in electrical engineering from SCU, Iran 2019. He is currently working toward the masterâs degree with the department of Electronics, information, and Bioengineering, the Politecnico di Milano University, Italy. He currently works as a remote researcher with Winiapp, where he mainly focuses on the latest wireless technologies combined with embedded systems for future smart cities.

<!-- image-->

Sajad Ahmadinabi received the BSc degree in electrical engineering from SCU, Iran, in 2020 and the masterâs degree in biomedical engineering from the Sharif University of Technology, starting in 2021. From 2020 to 2023, he worked as a researcher and developer on digital systems for wireless telecommunication networks with Winiapp. Now, he is working toward the graduate degree in neuroscience with Vanderbilt University, where he is engaged in research on brain-computer interfaces in Professor Womlesdorfâs lab. His research interests are diverse, focusing on the

biomedical Internet of Things, computational neuroscience, electrophysiology, and the interplay between learning in biological systems and machine programs. Through his academic and research experiences, His aims to contribute to advancements at the intersection of technology and neuroscience.

<!-- image-->

Hamed Bakhtiari Babadegani received the BSc degree in electrical engineering from SCU, Iran, in 2020. From 2020 until 2023, he worked as a remote researcher with Winiapp. He started a graduate program focusing on applied cryptography and network security with the electrical engineering department, Sharif University of Technology in 2021. His main research interests include network security, cryptography, and secure communication in IoT.

<!-- image-->

<!-- image-->

Christina Chaccour (Member, IEEE) received the PhD degree in electrical engineering from Virginia Tech. Currently holds the position of Network Solutions manager with Ericsson, Inc. In her role, she seamlessly bridges product solutions and research, spearheading developments in 5G Advanced, 6G networks, and AI-integrated solutions while ensuring the responsible and innovative use of AI, addressing both policy and technical dimensions. She actively represents Ericsson as a delegate in prominent industry bodies and committees, including 5G Americas, Next

G Alliance, and the FCC CSRIC. Her academic journey yielded significant contributions, particularly in 6G systems at THz frequencies for next-gen XR and holographic systems, alongside seminal work in AI-native networks and semantic communications. She was awarded the Best Paper at the 10th IFIP Conference on New Technologies, Mobility, and Security (NTMS) in 2019. Her paper in IEEE Communication Surveys and Tutorials was also featured in the Top Access article listing from June to November 2022. In 2021, she received the Exemplary Reviewer Award from IEEE Transactions on Communications (fewer than 2%). Currently, she serves on the editorial board for IEEE Transactions on Machine Learning in Communications and Networking, IEEE Transactions on Cognitive Communications and Networking, as well as Wireless Personal Communications by Springer. Her achievements extend to being named among the âTop 100 Brilliant and Inspiring Women in 6Gâ in 2024. Moreover, her entrepreneurial initiatives, exemplified by co-founding the startup âInternet of Treesâ, have garnered numerous local and international awards.

Walid Saad (Fellow, IEEE) received the PhD degree from the University of Oslo, Norway in 2010. He is currently a professor with the Department of Electrical and Computer Engineering, Virginia Tech, where he leads the Network sciEnce, Wireless, and Security (NEWS) laboratory. His research interests include wireless networks (5G/6G/beyond), machine learning, game theory, quantum communications/learning, security, UAVs, semantic communications, cyberphysical systems, and network science. He is also the recipient of the NSF CAREER award in 2013, the

AFOSR summer faculty fellowship in 2014, and the Young Investigator Award from the Office of Naval Research (ONR) in 2015. He was the (co)author of twelve conference best paper awards at IEEE WiOpt in 2009, ICIMP in 2010, IEEE WCNC in 2012, IEEE PIMRC in 2015, IEEE SmartGridComm in 2015, EuCNC in 2017, IEEE GLOBECOM (2018 and 2020), IFIP NTMS in 2019, IEEE ICC (2020 and 2022), and IEEE QCE in 2023. He is the recipient of the 2015 and 2022 Fred W. Ellersick Prize from the IEEE Communications Society, of the IEEE Communications Society Marconi Prize Award in 2023, and of the IEEE Communications Society Award for Advances in Communication in 2023. He was also a coauthor of the papers that received the IEEE Communications Society Young Author Best Paper award in 2019, 2021, and 2023. Other recognitions include the 2017 IEEE ComSoc Best Young Professional in Academia award, the 2018 IEEE ComSoc Radio Communications Committee Early Achievement Award, and the 2019 IEEE ComSoc Communication Theory Technical Committee Early Achievement Award. From 2015-2017, he was named the Stephen O. Lane junior faculty fellow with Virginia Tech, in 2017, he was named College of Engineering Faculty fellow. He received the Deanâs award for Research Excellence from Virginia Tech in 2019. He was also an IEEE distinguished lecturer in 2019-2020. He has been annually listed in the Clarivate Web of Science Highly Cited Researcher List since 2019. He currently serves as an area editor for IEEE Transactions on Communications. He is the editor-in-chief for IEEE Transactions on Machine Learning in Communications and Networking.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_6_img_1.png|page_6_img_1]]
3. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_8_img_1.jpeg|page_8_img_1]]
4. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_10_img_1.jpeg|page_10_img_1]]
5. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_11_img_1.jpeg|page_11_img_1]]
6. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_13_img_1.jpeg|page_13_img_1]]
7. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_13_img_2.jpeg|page_13_img_2]]
8. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_15_img_1.jpeg|page_15_img_1]]
9. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_15_img_2.jpeg|page_15_img_2]]
10. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_16_img_1.jpeg|page_16_img_1]]
11. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_16_img_2.jpeg|page_16_img_2]]
12. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_16_img_3.jpeg|page_16_img_3]]
13. [[../extracted_images/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks/page_16_img_4.jpeg|page_16_img_4]]

---

