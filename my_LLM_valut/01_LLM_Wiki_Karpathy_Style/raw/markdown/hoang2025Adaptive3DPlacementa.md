# Adaptive 3D Placement of Multiple UAV-Mounted Base Stations in 6G Airborne Small Cells With Deep Reinforcement Learning

Linh T. Hoang , Chuyen T. Nguyen , Hoang D. Le, and Anh T. Pham , Senior Member, IEEE

AbstractâUncrewed Aerial Vehicle-mounted Base Stations (UAV-BSs) have been envisioned as a promising solution to enable high-quality services in next-generation mobile networks. With inherent flexibility, one key challenge is placing the UAV-BSs adaptively to time-varying network conditions to maintain stable connections. Conventional methods mainly focus on optimizing UAV-BS deployment in static networks where users are static or with limited mobility. This study considers a dynamic network where multiple non-stationary UAV-BSs are deployed to serve mobile users with time-varying heterogeneous traffic. Incomplete downloads of users are backlogged in download queues at the UAV-BSs, and together with the newly requested traffic, the download queue size reflects the userâs instantaneous traffic demand. With constraints on the queue stability, we aim to maximize the userâs long-term mean opinion score (MOS), reflecting how the perceived data rate satisfies their traffic demand. Since the usersâ location and traffic demand vary over time, we dynamically group users into clusters using a K-meansbased algorithm and adjust the 3D location of UAV-BSs using an actor-critic deep reinforcement learning (DRL) framework. The actor module is encoded using a deep neural network (DNN) that obtains the UAV-BSâs current location and a traffic heatmap of users to predict the optimal movement for UAV-BSs. The critic module utilizes Lyapunov optimization to control the queue stability constraint and evaluate the actorâs decisions. Extensive simulations demonstrate the proposed methodâs superior performance over conventional rate-maximization approaches.

Index TermsâAerial base stations, UAV-BS deployment, quality of experience, machine learning for communications.

## I. INTRODUCTION

A ERIAL Base Stations (ABS), often implemented usingdrones or uncrewed aerial vehicles (UAVs), are emerging as a critical component of sixth-generation (6G) cellular networks [1], [2], [3]. By providing flexible and adaptable coverage, ABS can address challenges such as network congestion, disaster relief, and rural connectivity in 6G communications. Furthermore, ABSs or UAV-mounted base stations (UAV-BSs) can provide higher LoS probability and reduce the path loss and fading effect compared to groundto-ground communications. A single UAV-BS can cover an area of a 6G small cell, providing Internet connections to ground users in its vicinity [4], [5]. Multiple UAV-BSs can be deployed to form a dense airborne network of access points, acting as a complementary part of the terrestrial infrastructure in the integrated space-air-ground network [4], [5]. In various scenarios, UAV-BSs can be deployed as an on-demand solution in urban areas where the terrestrial infrastructure experiences an unexpected failure or becomes insufficient. In remote areas, UAV-BSs can replace terrestrial BSs to provide Internet connections to ground users, using a backhaul link to the space network (satellites). In emergency situations where the ground BSs are collapsed, such as natural disasters, UAV-BSs can be quickly deployed to facilitate rescue and recovery after the disaster. In large temporary openair events (e.g., festivals and sports games), UAV-BSs can complement the current terrestrial network, working as edge servers with additional computing and storage capabilities or as an interface between the backhaul network and the access network [6].

Besides the potential aspects, the deployment of UAV-BSs also poses various challenges to network management. One key challenge is placing the UAV-BSs dynamically over time in response to time-varying network conditions to provide high quality of service (QoS) [2], [3]. For example, the UAV-BS might adapt its position to the time-varying spatial distribution of mobile users to maintain LoS links with high data rates. Technically, QoS metrics are often non-convex functions of the UAV-BSsâ position [3]. Furthermore, the placement problem with multiple UAV-BSs is NP-hard in large-scale networks [7]. This necessitates efficient algorithms for the optimal dynamic placement of UAV-BSs.

## A. Related Works

There have been extensive efforts in the literature on UAV-BS placement optimization in static networks where users are static or with limited mobility [8], [9], [10], [11], [12], [13], [14], [15]. A summation is given in the first part of Table I. In [8], Lyu et al. propose a polynomial-time algorithm with successive UAV-BS placement to minimize the number of UAV-BSs needed to provide network coverage to a group of distributed users. In [9], Sun and Masouros propose an iterative method to maximize the user coverage probability in a target area, given an instantaneous snapshot of the user distribution. Considering static users, Zhang et al. [10] propose a three-step method to improve the network coverage with a minimum number of required UAV-BSs through optimizing their 3D positions. Shehzad et al. [11] propose a genetic algorithm to place UAVs as aerial hubs in the sky with backhaul links to the ground BSs. Considering the UAV-BS capacity limit and usersâ QoS requirement diversity,

TABLE I  
MAIN CONTRIBUTION OF RELATED WORKS
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Reference</td><td rowspan=1 colspan=1>Year</td><td rowspan=1 colspan=1>Summary</td><td rowspan=1 colspan=1>No.ofUAVs</td><td rowspan=1 colspan=1>Flexibilityof UAVs</td><td rowspan=1 colspan=1>Traffic-aware</td><td rowspan=1 colspan=1>Usermobilty</td><td rowspan=1 colspan=1>Dynamicclustering</td></tr><tr><td rowspan=8 colspan=1>StaticNetwork</td><td rowspan=1 colspan=1>Lyu [8]</td><td rowspan=1 colspan=1>2017</td><td rowspan=1 colspan=1>Minimize the number of UAV-BSs required to provide wireless con-nection to a group of distributed users.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>2D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Sun [9]</td><td rowspan=1 colspan=1>2019</td><td rowspan=1 colspan=1>Maximize the coverage probability for users in a target area.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>2D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Zhang [10]</td><td rowspan=1 colspan=1>2021</td><td rowspan=1 colspan=1>Minimize the number of required UAVs to improve the coverage rate.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Shehzad[]</td><td rowspan=1 colspan=1>2021</td><td rowspan=1 colspan=1>Maximize the network sum rate while considering the backhaul linkbetween UAV-BSsand ground small-cell BSs.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Zhong [12]</td><td rowspan=1 colspan=1>2021</td><td rowspan=1 colspan=1>Maximize the number of covered users with constraints on user data-rate requirements and UAV-BSsâ capacity limit.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Huang [13]</td><td rowspan=1 colspan=1>2022</td><td rowspan=1 colspan=1>Minimize the average UAV-user distance while maintaining LoS links.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>2D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Savkin [14]</td><td rowspan=1 colspan=1>2023</td><td rowspan=1 colspan=1>Maximize the coverage of UAV-BSs in areas with uneven terrains.</td><td rowspan=1 colspan=1> Multiple</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Lai [15]</td><td rowspan=1 colspan=1>2023</td><td rowspan=1 colspan=1>Maximize energy efficiency by optimizing the altitude and Tx powerof the UAV-BS to offload the traffic from overloaded UAV-BSs.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>1D(Altitude)</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=8 colspan=1>DynamicNetwork</td><td rowspan=1 colspan=1>Wang [16]</td><td rowspan=1 colspan=1>2019</td><td rowspan=1 colspan=1>Maximize the user&#x27;s average throughput or successrate by optimizingthe displacement directionand distance of the UAV-BS.</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>2D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Liu [7]</td><td rowspan=1 colspan=1>2019</td><td rowspan=1 colspan=1>Maximize the mean opinion score of roaming users using Q-learning.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Ding [21]</td><td rowspan=1 colspan=1>2020</td><td rowspan=1 colspan=1>Maximize the fair throughput of users via UAV trajectory design andfrequency band allocation with theUAV&#x27;s limited energy.</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Peng [25]</td><td rowspan=1 colspan=1>2021</td><td rowspan=1 colspan=1>Maximize the amount of offloaded data from users while minimizingthe UAV&#x27;s energy consumption via path planning</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>2D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Wang [17]</td><td rowspan=1 colspan=1>2022</td><td rowspan=1 colspan=1>Minimize the energy consumption of edge users through optimizingthe UAV-BS trajectorywith different take-off locations.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>Nasr-Azadani[18]</td><td rowspan=1 colspan=1>2022</td><td rowspan=1 colspan=1>Maximize the downlink rate of users via predicting usersâlocationsandoptimizing UAVs&#x27;initial deploymentand trajectory</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Parvaresh[19]</td><td rowspan=1 colspan=1>2023</td><td rowspan=1 colspan=1>Maximize the_sum data rate of users by optimizing the dynamicplacement of UAV-BSs using actor-critic Deep Q-Learning</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>This work</td><td rowspan=1 colspan=1>2023</td><td rowspan=1 colspan=1>Maximize the user&#x27;s mean opinion score in a dynamic network withcontinuous user movements and heterogeneous trafic demands.</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>3D</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr></table>

Zhong et al. [12] propose a genetic algorithm to maximize the covered users. In [13], Huang and Savkin propose an iterative method to adjust the horizontal positions of UAV-BSs to minimize the average UAV-user distance with LoS requirements. In [14], Savkin et al. consider the deployment of multiple UAV-BSs in uneven terrains to maximize the network coverage.

These methods [8], [9], [10], [11], [12], [13], [14], [15] are all based on iterative algorithms to find the optimal placement of UAV-BSs. Therefore, any changes in the user distribution require these algorithms to restart from the beginning to find the optimal solution, which may cause significant computation overhead with increased time complexity. Moreover, iterative methods are susceptible to the initial positions of UAV-BSs. Therefore, they are not directly applicable to dynamic environments.

In dynamic networks where the userâs spatial distribution and data rate requirement change continuously, the UAV-BS should adapt their 3D position in real time to maintain stable connections with LoS [2], [3]. The problem is challenging since the optimal placement of UAV-BSs is constantly changing, and movement decisions of UAV-BSs are correlated over time. Although some efforts have been made, the problem has not been well-investigated in the literature. The pioneering work is [16], where Wang et al. propose a majority votingbased algorithm for an adaptive deployment: the UAV-BS moves toward the spatial sector with the most users in its cell coverage while remaining at a fixed flying altitude.

Toward adaptive placement of UAV-BSs in dynamic networks, Artificial Intelligence (AI) and Machine Learning (ML) techniques are promising candidate solutions [2].

Reinforcement learning (RL) and deep reinforcement learning (DRL) are the most suitable approaches for sequential decision-making with no training data available in advance. Starting with no prior knowledge about the environment (i.e., the network situation), the RL/DRL agent can learn the optimal movement policy from its experience (by trial and error) to maximize a predefined reward function.

There are several studies following this research direction. In [17], Wang et al. propose a DRL-based trajectory design for UAV-BSs to minimize the edge userâs energy consumption. Convergence was demonstrated given different UAVâs take-off locations, but user mobility was not considered during training and performance evaluation. In [7], Liu et al. propose a Q-learning-based movement design of UAV-BSs with seven flying directions when considering moving users. The work assumes that users do not roam into another UAV-BS cluster after the initial clustering step. In [18], Nasr-Azadani et al. propose an actor-critic algorithm based on Q-learning to optimize the initial deployment and trajectory of UAV-BSs (with 27 flying directions) to maximize the downlink rate of mobile users. In [19], Parvaresh and Kantarci propose an actor-critic RL algorithm to obtain dynamic UAV-BS movements from a continuous action space. In [20], Wang et al. propose a Q-learning method to enhance the sum spectrum efficiency through optimizing the macro BS power allocation, the UAV service zone selection, and the user scheduling in an emergency scenario. Other related works are summarized in the second part of Table I.

Despite efforts have been made, the majority of current RL/DRL-based methods [7], [17], [18], [19], [21] toward

UAV-BS placement in dynamic networks have two fundamental limitations:

1) Unscalable State Space: The state space of RL is often considered the location of all UAVs and users, causing the state space to become exponentially large with the increase of users (e.g., the Q tableâs size in Q learning). This approach exhibits limitations in scalability and adaptability when applying a pre-trained RL agent in practice. Consequently, the common assumption in existing research is that the set of users assigned to each UAV remains unchanged (static association).

2) Discrete Action Space: Conventional DRL-based methods often have a discrete action space where the agent can only select a limited number of moving decisions (e.g., 5 or 7 flying directions with a fixed velocity). This property limits the agility of the UAVs in response to the time-varying network conditions.

Besides, most conventional UAV-BS placement methods utilize the usersâ location to maximize their average data rate [2], [11], [13], [16], [18]. This approach might become suboptimal when the users have heterogeneous traffic demands, causing the spatial distribution of the network traffic not to be highly correlated with the distribution of users. For example, users with heavy-traffic applications (e.g., video streaming and gaming) should be provided higher data rates over those requesting minimal traffic (e.g., e-mail and navigation). To this end, it would be more efficient to transform the objective from maximizing the sum data rate to maximizing the userâs experience based on their data rate requirement. The Mean Opinion Score (MOS) [22], [23], [24] can be used to measure the quality of experience (QoE) perceived by the users, indicating the network service quality from the userâs point of view.

## B. Motivations and Our Contributions

Motivated by the mentioned research gap, in this study, we aim at an effective method for adaptive 3D placement of multiple UAV-BSs in a large-scale dynamic network where the users move continuously and have heterogeneous traffic. The ultimate goal is to improve the QoE of users in terms of the userâs satisfaction score, which is calculated based on their perceived data rate and requested traffic demand. We summarize the current research gaps and our approaches as follows.

1) Toward Adaptive Placement in Dynamic Networks: Conventional approaches usually consider the UAV-BS deployment optimization in a static network where users are static or with limited movements. They can not be applied directly to dynamic networks where the network situation (e.g., user distribution) continuously changes over time. To overcome this gap, we propose an effective movement design enabling UAV-BSs to adjust their 3D locations w.r.t the real-time network condition.

2) Toward Userâs Quality of Experience (QoE): Most current works focus on the average data rate or network coverage of a static network with homogeneous user traffic. The placing problem is often reduced to maximizing the achievable sum rate by minimizing the total distance from the users to the UAV. Practically, users have different data rate requirements. In our research, we aim to maximize the QoE of users in terms of their satisfaction score â MOS, reflecting how the perceived data rate satisfies the traffic demand of each user.

3) Toward Efficient and Scalable DRL-based Placement: Conventional DRL-based methods often limit the UAV-BS with limited moving directions and fixed velocity to reduce the complexity. In this study, the action space is continuous to facilitate more flexibility in UAV movements. The UAV-BS can move freely in any direction (both horizontally and vertically) with flexible speeds in 3D space. Additionally, our method encodes the network state using the user traffic heatmap, whose size is independent of the user cardinality.

This paper considers a large-scale dynamic network where multiple UAV-BSs are deployed to serve many mobile users with highly heterogeneous traffic. The user traffic demand is monitored using backlog queues at the UAV-BSs. Incomplete downloads of each user are backlogged in a separate queue, and together with the newly requested traffic, the download queue size reflects the userâs instantaneous traffic demand. A stochastic optimization problem of UAV-BS placement is formulated to maximize the usersâ long-term satisfaction score (MOS) with constraints on the queue stability of the queueing system. To cope with the long-term perspectives of a dynamic network, we follow a new method integrating a datadriven approach (using DRL) and conventional model-based optimization for queueing systems [26], [27]. An actor-critic DRL framework is proposed in this paper, where the actor module is based on a DNN, and the critic module is backed by the Lyapunov theorem on queue stability.

Our contributions are summarized as follows:

1) Our study tackles the optimization of adaptive 3D placement of multiple UAV-BSs in a large-scale dynamic network. We formulate a stochastic optimization problem to maximize the userâs long-term MOS with constraints on the queue stability. Considering a scenario with heterogeneous user traffic, our study enables the UAV-BSs to adjust their 3D location in realtime w.r.t the usersâ time-varying location and traffic demand.

2) We develop a two-step method to cope with the adaptive placement optimization of UAV-BSs. First, a K-means-based algorithm dynamically associates users to UAV-BSs based on their locations. Afterward, an actor-critic DRL is utilized to adjust the UAV-BSâs 3D position in real-time, corresponding to the usersâ movement and traffic demand in its cluster.

3) We propose an efficient and scalable actor-critic DRL framework for 3D movement optimization of UAV-BSs in dynamic networks. The DNN-based actor module obtains the usersâ traffic heatmap and UAV-BSsâ positions to generate flexible 3D movements for each UAV-BS. The critic module is based on Lyapunov optimization to facilitate faster convergence and cope with the queueing networkâs long-term perspectives.

4) We demonstrate that our method has fast convergence through intensive simulations. In addition, the proposed method outperforms the conventional methods that purely rely on user location in optimization.

The paper is organized as follows. Section II describes the system model. Section III presents the problem formulation and transformation based on Lyapunov optimization. Section IV details the proposed method, followed by time

<!-- image-->  
Fig. 1. Adaptive placement of UAV-BSs: the UAVs continuously adjust their 3D position according to time-varying traffic demand and movements of users. Queues are maintained to backlog usersâ incomplete downloads in each cluster.

TABLE II  
SUMMARY OF NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=1>Number of ground users</td><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>Number of UAV-BSs</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathbb { T } , \mathbb { U } , \mathbb { S } } }$ </td><td rowspan=1 colspan=1>Index sets of the time slot,users,and UAV-BSs</td><td rowspan=1 colspan=1> $t , i , s$ </td><td rowspan=1 colspan=1>Index of time,users and UAV-BSs,tâT,iâU,sâS</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathbb { C } _ { s } ^ { t } } }$ </td><td rowspan=1 colspan=1>Set of users associated with UAV-BS s at time t</td><td rowspan=1 colspan=1> $\overline { { k _ { i } ( t ) } }$ </td><td rowspan=1 colspan=1>Index of the UAV-BS associated with useri at time t</td></tr><tr><td rowspan=1 colspan=1> $\overline { { { \bf p } _ { i } ( t ) } }$ </td><td rowspan=1 colspan=1>Location of useri at time $\underline { { t , \ [ x _ { i } ( t ) , y _ { i } ( t ) ] ^ { \intercal } } }$ </td><td rowspan=1 colspan=1> $\overline { { \mathbf { p } _ { k _ { i } } ( t ) } }$ </td><td rowspan=1 colspan=1>Horizontal coordinates of the UAV-BS, $\overline { { [ x _ { k _ { i } } ( t ) , y _ { k _ { i } } ( t ) ] ^ { \intercal } } }$ </td></tr><tr><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>The coverage zone of interest is $\overline { { 2 R \times 2 R ~ \mathrm { m } ^ { 2 } } }$ </td><td rowspan=1 colspan=1> $z _ { k _ { i } } ( t )$ </td><td rowspan=1 colspan=1>Flying altitude of the UAV-BSat time t</td></tr><tr><td rowspan=1 colspan=1> $\hat { d } _ { i } ( t )$ </td><td rowspan=1 colspan=1>Distance from user i to its UAV-BS</td><td rowspan=1 colspan=1> $\| \cdot \|$ </td><td rowspan=1 colspan=1>Euclidean norm of the vector</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \theta _ { i } ( t ) } }$ </td><td rowspan=1 colspan=1>Elevation angle for userito see its UAV-BSat time t</td><td rowspan=1 colspan=1> $\overline { { \mathrm { P } _ { \mathrm { L o S } } ( \theta _ { i } ( t ) ) } }$ </td><td rowspan=1 colspan=1>The LoS probability of useriat time t</td></tr><tr><td rowspan=1 colspan=1> $\overline { { h _ { i } ( t ) } }$ </td><td rowspan=1 colspan=1>Channel power gain of the user</td><td rowspan=1 colspan=1> $a _ { 1 } , b _ { 1 }$ </td><td rowspan=1 colspan=1>Coefficients related to the LoSprobability</td></tr><tr><td rowspan=1 colspan=1> $\gamma _ { i } ( t )$ </td><td rowspan=1 colspan=1>Path loss exponent of the user</td><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>Attenuation coefficient of the Non-LoS link</td></tr><tr><td rowspan=1 colspan=1>a2,b2</td><td rowspan=1 colspan=1>Coefficients related to the path loss exponent</td><td rowspan=1 colspan=1> $\overline { { P _ { t } } }$ </td><td rowspan=1 colspan=1>Fixed transmit power of the UAV-BS</td></tr><tr><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>Reference signal gain at $\overline { { d _ { 0 } = 1 \mathrm { ~ m ~ } } }$ </td><td rowspan=1 colspan=1> $\overline { { N _ { 0 } } }$ </td><td rowspan=1 colspan=1>Total noise power of the downlink channel</td></tr><tr><td rowspan=1 colspan=1> $\overline { { Q _ { i } ( t ) } }$ </td><td rowspan=1 colspan=1>Backlog queue of the user</td><td rowspan=1 colspan=1> $\overline { { A _ { i } ( t ) , R _ { i } ( t ) } }$ </td><td rowspan=1 colspan=1>Arrival traffic and downlink rate of the user at time t</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathrm { M O S } _ { i } ( t ) } }$ </td><td rowspan=1 colspan=1>QoE rating of the user</td><td rowspan=1 colspan=1> $\overline { { d _ { i } ( t ) } }$ </td><td rowspan=1 colspan=1>Web session time of the user at time t</td></tr><tr><td rowspan=1 colspan=1> $C _ { 1 } , C _ { 2 }$ </td><td rowspan=1 colspan=1>Coefficients related to the QoE model</td><td rowspan=1 colspan=1> $\mathbb { U } _ { t } ^ { + }$ </td><td rowspan=1 colspan=1>Set of users in the ON state at time t</td></tr><tr><td rowspan=1 colspan=1> $d _ { \operatorname* { m i n } } , d _ { \operatorname* { m a x } }$ </td><td rowspan=1 colspan=1>Minimum and maximum acceptable delay</td><td rowspan=1 colspan=1> $\overline { { \Delta ( \mathbf { Q } ( t ) ) } }$ </td><td rowspan=1 colspan=1>Lyapunov drift function</td></tr><tr><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>Lyapunov control parameter</td><td rowspan=1 colspan=1> $\overline { { \Delta _ { V } ( \mathbf { Q } ( t ) ) } }$ </td><td rowspan=1 colspan=1>Lyapunov-drift-minus-reward function</td></tr><tr><td rowspan=1 colspan=1> $\overline { { K } }$ </td><td rowspan=1 colspan=1>Number of decisions generated by the actor module</td><td rowspan=1 colspan=1> $\delta _ { T }$ </td><td rowspan=1 colspan=1>Periodic training cycle of the DNN in time slots</td></tr></table>

## II. SYSTEM MODEL

This work considers a multi-UAV-assisted downlink communication system, as illustrated in Fig. 1. Multiple UAV-BSs are deployed to provide many network services to ground users with mobility and heterogeneous traffic. Users are grouped into clusters, each served by one UAV-BS. The clustering is dynamic with the movement of users. In each cluster, users are with different services, and the network traffic is assumed to be highly heterogeneous among them. The UAV-BSs consider not only the usersâ spatial distribution but also heterogeneous traffic to adjust their 3D position (horizontal coordinates and flying altitude) accordingly.

complexity and convergence analysis in Section V. Numerical results are provided in Section VI. Finally, Section VII concludes the paper with conclusions and future directions.

Each UAV-BS maintains backlog queues, one for each user, to backlog incomplete downloads of its users over time. Time is slotted, and depending on the traffic load and channel condition, the user might need several time slots to receive the requested data completely. The downlink channel is limited in bandwidth and equally shared between all users with non-empty queues using frequency division multiple access (FDMA). The UAV-BSs are assumed to have directional backhaul links to the core network via a nearby terrestrial base station and have interconnection with each other.

For convenience, the index sets of the time slots, the users, and the UAV-BSs are denoted as $\mathbb { T } \triangleq \{ 0 , 1 , 2 , \dots , T - 1 \}$ , $\mathbb { U } \triangleq \{ 1 , 2 , \dots , N \}$ , and $\mathbb { S } \triangleq \{ 1 , 2 , \dots , \hat { M } \}$ , where $T , N ,$ and M denote the total number of time slots, users, and UAV-BSs, respectively. Correspondingly, let $i \in \mathbb { U } , s \in \mathbb { S } .$ , and $t \in \mathbb { T }$ denote the index of the user, UAV-BS, and time slot. In addition, let $\mathbb { C } _ { s } ^ { t } \triangleq \left\{ \textit { i } | i \in \mathbb { N } , s \in \mathbb { S } , \kappa _ { i , s } ( t ) = 1 \right\}$ denote the cluster of users associated with UAV-BS s in time slot t. $\kappa _ { i , s } ( t ) \in \{ 0 , 1 \}$ is an indicator function: $\kappa _ { i , s } ( t ) = 1$ denotes that user i is associated with UAV-BS s in time slot t, and vice versus. Other notations are summarized in Table II.

## A. User Movement

The ground users are assumed to follow the Gauss-Markov mobility model, which is widely used in the literature [28]. The velocity of user i is correlated over time and modeled as a Gauss-Markov stochastic process as

$$
\mathbf { v } _ { i } ( t + 1 ) = \alpha \mathbf { v } _ { i } ( t ) + ( 1 - \alpha ) \overline { { \mathbf { v } } } _ { i } + \bar { \sigma } \sqrt { 1 - \alpha ^ { 2 } } \mathbf { w } _ { i } ( t ) ,\tag{1}
$$

where $\mathbf { v } _ { i } ( t ) = [ v _ { i } ^ { x } ( t ) , v _ { i } ^ { y } ( t ) ] ^ { \mathsf { T } }$ and $\mathbf { w } _ { i } ( t ) = [ w _ { i } ^ { x } ( t ) , w _ { i } ^ { y } ( t ) ] ^ { \mathsf { T } }$ are the velocity vector and the uncorrelated random Gaussian process $\mathcal { N } \left( 0 , \dot { \sigma } ^ { 2 } \right)$ at time $t ,$ respectively. Parameters Î±, $\bar { \bf { v } } _ { i } =$

TABLE III THE ON/OFF TRAFFIC MODEL
<table><tr><td rowspan=1 colspan=1>State</td><td rowspan=1 colspan=1>Distributions and parameters</td></tr><tr><td rowspan=1 colspan=1>ON</td><td rowspan=1 colspan=1>The user trafc is Pareto distributed with mean Xiin MB,shape $\alpha = 1 . 5 ,$ and scale $x _ { m }$ obtained via Xi and Î±.</td></tr><tr><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>The user is with no traffic.The OFF state duration isexponentially distributed with mean Î¼oFF in seconds.</td></tr></table>

$[ \bar { v } _ { i } ^ { x } , \bar { v } _ { i } ^ { y } ] ^ { \bar { \mathsf { I } } }$ , and ÏÂ¯ represent the memory level, asymptotic mean, and asymptotic standard deviation, respectively [28].

The position of user i is updated over time as

$$
\mathbf { p } _ { i } ( t + 1 ) = \mathbf { p } _ { i } ( t ) + \mathbf { v } _ { i } ( t ) \boldsymbol { \tau } ,\tag{2}
$$

where $\mathbf { p } _ { i } ( t ) = [ x _ { i } ( t ) , y _ { i } ( t ) ] ^ { \intercal }$ denotes the user location at time t, and Ï indicates the time slot length. The users are assumed to be moving within a $2 R \times 2 R$ square target area so that $- R \leq x _ { i } ( t ) , \bar { y } _ { i } ( t ) \leq R , \forall t \in \mathbb { T } , i \in \bar { \mathbb { U } }$

## B. User Traffic

We adopt the ON-OFF traffic model [29], [30] to simulate the heterogeneous downlink traffic among users. The ON-OFF model is preferred for modelling of the Internet Protocol (IP) traffic [29], [30]. Using this model, the downlink traffic is correlated over time and not identically distributed among users. In the ON state, the user has downlink requests following Pareto distribution with different rates, denoted by $\lambda _ { i }$ . In the OFF state, the user has no download request. The ON and OFF state duration is exponentially distributed with mean ÂµON and ÂµON in seconds, respectively. Details of the traffic model are given in Table III.

## C. Communication Model

The communication channel between UAV-BSs and ground users experiences path loss and the attenuation effect of the LoS and Non-LoS links, as illustrated in Fig. 1. The path loss for user i at time t depends on the communication distance to the UAV, given as

$$
\hat { d } _ { i } ( t ) = \sqrt { z _ { k _ { i } } ( t ) ^ { 2 } + \| \mathbf { p } _ { i } ( t ) - \mathbf { p } _ { k _ { i } } ( t ) \| ^ { 2 } } ,\tag{3}
$$

where $k _ { i } ~ = ~ \{ s : \kappa _ { i , s } ( t ) = 1 , s \in \mathbb { S } \}$ denotes the UAV-BS associated with user i at time $t ; \ z _ { k _ { i } } ( t )$ and $\begin{array} { r l } { \mathbf { p } _ { k _ { i } } ( t ) } & { { } = } \end{array}$ $[ x _ { k _ { i } } ( t ) , y _ { k _ { i } } ( t ) ] ^ { \intercal }$ respectively denote the UAV-BSâs flying altitude and horizontal coordinate vector; and $\| \cdot \|$ denotes the Euclidean norm of the vector.

The LoS probability of user i at time t can be approximated to have the form of a sigmoid function as [31]

$$
\operatorname { P } _ { \mathrm { L o S } } ( \theta _ { i } ( t ) ) = \frac { 1 } { 1 + a _ { 1 } \exp \left\{ - b _ { 1 } ( \theta _ { i } ( t ) - a _ { 1 } ) \right\} } ,\tag{4}
$$

where $a _ { 1 }$ and $b _ { 1 }$ are environment-related parameters, and $\theta _ { i } ( t ) = \arcsin \Big ( z _ { k _ { i } } ( t ) / \hat { d } _ { i } ( t ) \Big )$ denotes the elevation angle for user i to see the UAV, as illustrated in Fig. 1.

The channel power gain of the UAV-user i link at time t is given as

$$
h _ { i } ( t ) = \frac { \left[ \mathrm { P } _ { \mathrm { L o S } } ( \theta _ { i } ( t ) ) + \zeta ( 1 - \mathrm { P } _ { \mathrm { L o S } } ( \theta _ { i } ( t ) ) \right] g _ { 0 } } { \left( z _ { k _ { i } } ( t ) ^ { 2 } + \| \mathbf { p } _ { i } ( t ) - \mathbf { p } _ { k _ { i } } ( t ) \| ^ { 2 } \right) ^ { \gamma _ { i } ( t ) / 2 } } ,\tag{5}
$$

where Î¶ represents the attenuation effect of the Non-LoS link $\begin{array} { r } { ( \zeta ~ < ~ 1 ) . ~ g _ { 0 } ~ = ~ \left( \frac { c } { 4 \pi f _ { c } } \right) ^ { 2 } } \end{array}$ denotes the reference signal gain at $d _ { 0 } = 1 \mathrm { ~ m ~ }$ , where $f _ { c }$ and c denotes the carrier frequency and the speed of light, respectively. The path loss exponent $\gamma _ { i } ( t ) = - \dot { a _ { 2 } } \mathrm { P } _ { \mathrm { L o S } } ( \dot { \theta _ { i } ( t ) } ) + \bar { b _ { 2 } }$ is dependent on the LoS; a2 and b2 are environment-dependent coefficients $( 2 \leq \gamma _ { i } ( t ) \leq 3 . 5 )$ [32].

The data rate of user i at time t is approximated using the Shannon-Hartley formula as

$$
\begin{array} { r l } & { R _ { i } ( t ) } \\ & { = W _ { i } \tau \log _ { 2 } ( 1 + \frac { [ \mathrm { P } _ { \mathrm { L o S } } ( \theta _ { i } ( t ) ) + \zeta ( 1 - \mathrm { P } _ { \mathrm { L o S } } ( \theta _ { i } ( t ) ) ] g _ { 0 } P _ { t } } { ( z _ { k _ { i } } ( t ) ^ { 2 } + \| \mathbf { p } _ { i } ( t ) - \mathbf { p } _ { k _ { i } } ( t ) \| ^ { 2 } ) ^ { \gamma _ { i } ( t ) / 2 } N _ { 0 } } ) } \end{array}\tag{6}
$$

where $W _ { i }$ denotes the allocated bandwidth, $P _ { t }$ denotes the transmit power of the UAV-BS, and $N _ { 0 }$ is the total noise power of the downlink channel. The total channel bandwidth W is equally shared among users.

## D. Backlog Queue

The UAV-BS maintains a backlog queue for each user to backlog the userâs incomplete downloads in each time slot. The download is processed until the backlog queue becomes empty. The queue for user i evolves as

$$
Q _ { i } ( t + 1 ) = \operatorname* { m a x } \left\{ Q _ { i } ( t ) + A _ { i } ( t ) - R _ { i } ( t ) , 0 \right\}\tag{7}
$$

where $Q _ { i } ( t ) , A _ { i } ( t )$ , and $R _ { i } ( t )$ denote the queue length, newlyrequested traffic, and data rate of user i at time t, respectively. Under the randomness of the traffic and the wireless channel with user movements, the queue backlog $Q _ { i } ( t )$ plays a critical role in placing the UAV-BSs, which will be discussed in Section IV. Let $\mathbb { 1 } _ { i } ( t )$ denote the indicator function,

$$
\mathbb { 1 } _ { i } ( t ) = \left\{ { \begin{array} { l l } { 1 } & { { \mathrm { i f ~ } } A _ { i } ( t ) > 0 , } \\ { 0 } & { { \mathrm { o t h e r w i s e } } . } \end{array} } \right.
$$

Users with non-empty downlink traffic $( \mathrm { i . e . , ~ } \mathbb { 1 } _ { i } ( t ) = 1 )$ are called active in time slot t, and vice versa.

When considering backlog queues, it is important that all queues remain stable during the process. The definition of strongly stable queues is given as [33, Definition 2.7]:

Definition 1: A discrete-time process Q(t) is strongly stable if

$$
\operatorname* { l i m } _ { T \to \infty } \operatorname* { s u p } _ { T } { \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } \left[ Q ( t ) \right] } < \infty\tag{8}
$$

## E. Quality of Experience

We evaluate the userâs quality of experience (QoE) in terms of their Mean Opinion Score (MOS). The MOS is rated based on their satisfaction level with a five-point rating scale, where 5: excellent, 4: good, 3: fair, 2: poor, and 1: bad [23], [24], [34]. Following the guidance of ITU-T G.11030 [34], we estimate the user satisfaction (i.e., the QoE) based on their perceived QoS measurement with the logarithmic rule, where the QoS reflects the level of disturbance.

We consider the web browsing applications in this paper. The mapping from the web session time (i.e., the QoS) to web browsing quality (i.e., the QoE) can be constructed by defining a minimum $( d _ { m i n } )$ and maximum $( d _ { \mathrm { m a x } } )$ session time and using a logarithmic interpolation between these two extreme values [34]. Let $d _ { i } ( t )$ denote the web session time, the MOS of user i at time slot t can be estimated as [34]:

<!-- image-->  
Fig. 2. General shape of mapping between QoS and QoE [23]. The color represents user satisfaction levels: green signifies high ratings, while red signifies a poor user experience.

$$
\mathrm { M O S } _ { i } ( t ) = \frac { 4 } { \ln \left( d _ { \mathrm { m i n } } / d _ { \mathrm { m a x } } \right) } \Big ( \ln \left( d _ { i } ( t ) \right) - \ln \left( d _ { \mathrm { m i n } } \right) \Big ) + 5 .\tag{9}
$$

Remark 1: A closer observation reveals that the mapping from QoS disturbance to the QoE of users is split into three regions, as illustrated in Fig. 2 [23]. The x-axis denotes the QoS disturbance (the web session time experienced by users), while the QoE rating (the MOS) is denoted. In Area 1, the QoE ratings are quasi-optimal, and small changes in the QoS disturbance have no impact on the user rating.1 In Area 2, the QoE and user satisfaction decrease rapidly with the increase of the QoS disturbance. In Area 3, the QoE becomes unacceptably bad (e.g., the service stops working due to timeouts), and the user might give up using the service.

We assume that the download queue of user $Q _ { i } ( t )$ is firstcome-first-serve, meaning that the previously requested query must be downloaded before a new request is processed. In such a queueing system, by assuming that the queueing delay is dominant over the other delays (denoted by $d _ { 0 } )$ , the web session time of users can be estimated using Littleâs law as

$$
d _ { i } ( t ) = d _ { 0 } + \frac { Q _ { i } ( t ) } { \lambda _ { i } } ,\tag{10}
$$

where $Q _ { i } ( t )$ and $\lambda _ { i }$ denote the instantaneous backlog queue at time t and the average arrival rate of user i, respectively.

Let $\mathbb { U } _ { t } ^ { + }$ and $\lvert \mathbb { U } _ { t } ^ { + } \rvert$ respectively denote the set and the number of active users $( \mathrm { i . e . , ~ } A _ { i } ( t ) > 0 )$ at time slot t. We define the average MOS of these users at t as

$$
\mathrm { M O S } _ { \mathrm { s y s } } ( t ) = \frac { 1 } { | \mathbb { U } _ { t } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \left( - C _ { 1 } \ln \left( d _ { 0 } + \frac { Q _ { i } ( t ) } { \lambda _ { i } } \right) + C _ { 2 } \right) ,\tag{11}
$$

where $\begin{array} { r } { C _ { 1 } = \frac { 4 } { \ln ( d _ { \mathrm { m a x } } / d _ { \mathrm { m i n } } ) } } \end{array}$ and $\begin{array} { r } { C _ { 2 } = 5 + \frac { 4 \ln ( d _ { \mathrm { m i n } } ) } { \ln ( d _ { \mathrm { m a x } } / d _ { \mathrm { m i n } } ) } } \end{array}$ . We assume inactive users will not feed back the MOS since they do not have download requests; meanwhile, the instantaneous MOS is estimated every time slot for active users.

## F. UAV Propulsion Energy

The propulsion power for UAV s with flying speed $V _ { s , t }$ in time slot t is calculated as [35, eq. (12)]:

$$
\begin{array} { l } { { P _ { s } } ( t ) = { P _ { 0 } } \left( 1 + \frac { { 3 V _ { s , t } ^ { 2 } } } { { U _ { \mathrm { t i p } } ^ { 2 } } } \right) + P _ { i } \left( \sqrt { 1 + \frac { { V _ { s , t } ^ { 4 } } } { 4 v _ { 0 } ^ { 4 } } } - \frac { { V _ { s , t } ^ { 2 } } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } } \\ { ~ + \displaystyle \frac { 1 } { 2 } d _ { 0 } \rho s A V _ { s , t } ^ { 3 } = P ( V _ { s , t } ) , ~ } & { ( 1 } \end{array}\tag{2}
$$

where $P _ { 0 }$ and $P _ { i }$ respectively denote the blade profile and induced power in the hovering status, $U _ { \mathrm { t i p } }$ is the tip speed of the rotor blade, $v _ { 0 }$ is the mean velocity induced by rotors in hovering, $d _ { 0 }$ is the fuselage drag ratio, s is the rotor solidity ratio, $\rho$ is the air density, and A is the rotor disc area.

## III. THE MULTI-STAGE MINLP PROBLEM OF USERSATISFACTION MAXIMIZATION

## A. Problem Formulation

We aim to maximize the long-term average MOS of users by optimizing the user clustering and adaptive placement of UAV-BSs. The optimization is under constraints on the stability of usersâ download queues and the limit on the radio (bandwidth) resources. The users continuously move around a target area with time-varying traffic demands. Taking into account the userâs movement and time-evolving traffic, the UAVs continuously adjust their 3D position to maximize the QoE rating of users with constraints on queue stability and the average propulsion energy consumption.

Let $\mathcal { C } \ = \ \{ k _ { i } ( t ) , 0 \leq t \leq T \} , \ Q \ = \ \{ \mathbf { p } _ { s } ( t ) , 0 \leq t \leq T \}$ $\mathcal { H } = \{ z _ { s } ( t ) , 0 \leq t \leq T \}$ denote the over-time user clustering, horizontal coordinate, and flying altitude of all UAV-BSs. Additionally, let $\mathcal { X } = \{ \mathcal { C } , \mathcal { Q } , \mathcal { H } \}$ denote the set of all optimization variables over time. Under the randomness of userâs movements and traffic requests, we formulate a multi-stage stochastic optimization problem as

$$
\mathcal { P } : \operatorname* { m a x } _ { \chi } \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } \left[ \operatorname { M O S } _ { \mathrm { s y s } } ( t ) \right]\tag{13a}
$$

$$
\mathrm { s . t } ~ \kappa _ { i , s } ( t ) \in \{ 0 , 1 \} , \sum _ { s \in \mathbb { S } } \kappa _ { i , s } ( t ) = 1 , \forall i \in \mathbb { U } , t \in \mathbb { T }\tag{13b}
$$

$$
\| \mathbf { p } _ { s } ( t + 1 ) - \mathbf { p } _ { s } ( t ) \| \leq v _ { \mathrm { x y } } ^ { \operatorname* { m a x } } \tau , \forall s \in \mathbb { S } , t \in \mathbb { T }\tag{13c}
$$

$$
| z _ { s } ( t + 1 ) - z _ { s } ( t ) | \leq v _ { \mathrm { z } } ^ { \operatorname* { m a x } } \tau , \forall s \in \mathbb { S } , t \in \mathbb { T }\tag{13d}
$$

$$
z _ { \mathrm { m i n } } \le z _ { s } ( t ) \le z _ { \mathrm { m a x } } , \forall s \in \mathbb { S } , t \in \mathbb { T }\tag{13e}
$$

$$
\operatorname* { l i m } _ { T  \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } [ Q _ { i } ( t ) ] < \infty , \forall i \in \mathbb { U }\tag{13f}
$$

$$
\operatorname* { l i m } _ { T  \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } [ P _ { s } ( t ) ] \leq P _ { s } ^ { \mathrm { t h } } , \forall s \in \mathbb { S }\tag{13g}
$$

In $\mathcal { P } _ { : }$ , (13b) ensures that each user is assigned to exactly one UAV-BS at a time. (13c), (13d), and (13e) are the UAVâs moving speed and placement constraints. $z _ { \mathrm { m i n } }$ and $z _ { \mathrm { m a x } }$ respectively denote the minimum and maximum flying altitude of the UAV-BS. $v _ { \mathrm { x y } } ^ { \mathrm { m a x } }$ and $v _ { \mathrm { z } } ^ { \mathrm { m a x } }$ denote the maximum horizontal and vertical moving speed of the UAV-BS, respectively. (13f) denotes the long-term asymptotic queue stability requirement [33] for all users. (13g) denotes the time-average propulsion power constraint with a predefined threshold $P _ { s } ^ { \mathrm { t h } }$ for all UAVs. $\mathcal { P }$ includes a mixture of discrete (on user clustering) and continuous (on movements of UAV-BSs) decision variables, and the MOS function is a non-linear (indeed, non-convex) function of the decision variables. Solving $\mathcal { P }$ is challenging because the downlink channels of users are interdependent with the 3D position of the UAVs, and the optimal decisions are coupled over time. In the following, we propose an online optimization approach to solve $\mathcal { P }$ using the Lyapunov optimization and reinforcement learning.

Remark 2: P is a multi-stage MINLP problem of a time-evolving system. The UAVs need to make a series of decisions on user clustering and placement over time slots under the randomness of user movement and downlink traffic. The decision-making exhibits temporal correlation, as the network state, influenced by previous decisions, serves as input for optimization in subsequent slots. Indeed, the optimal placement of UAVs continuously changes with the time-varying distribution and traffic demand of users.

## B. Lyapunov-Guided Problem Transformation

To obtain an efficient online solution for asymptotic optimality, we transform the multi-stage problem $\mathcal { \hat { P } }$ into per-time slot sub-problems $\mathcal { P } ^ { \prime }$ based on the Lyapunov optimization framework. The Lyapunov optimization is efficient in coping with time-average maximization constrained on queue stability in dynamic networks [33].

First, to cope with constraint (13g), we introduce the virtual queue $Z _ { s } ( t )$ for controlling the propulsion power as

$$
Z _ { s } ( t + 1 ) = \operatorname* { m a x } \left\{ Z _ { s } ( t ) + P _ { s } ( t ) - P _ { s } ^ { \mathrm { t h } } , 0 \right\}\tag{14}
$$

for each UAV $s \in \mathbb { S } ,$ where $Z _ { s } ( 0 ) = 0$ . By this definition, it is proved in [33] that (13g) is satisfied when $Z _ { s } ( t )$ is mean-rate stable, i.e., lim $_ { 1 \to \infty } Z _ { s } ( t ) / t = 0$

To cope with the queue stability problem, let $\Theta ( t )$ , $\{ Q _ { i } ( t ) , \bar { Z } _ { s } ( t ) , \forall i \in \mathbb { U } , \bar { s } \in \mathbb { S } \}$ be a concatenated vector of all actual and virtual queues at time slot t. We define the Lyapunov function to measure the total queue backlog as

$$
\mathcal { L } ( \boldsymbol { \Theta } ( t ) ) \triangleq \frac { 1 } { 2 } \sum _ { i = 1 } ^ { N } \psi _ { Q } Q _ { i } ( t ) ^ { 2 } + \frac { 1 } { 2 } \sum _ { s = 1 } ^ { M } \psi _ { Z } Z _ { s } ( t ) ^ { 2 } ,\tag{15}
$$

where $\psi _ { Q }$ and $\psi _ { Z }$ are normalization coefficients for $Q _ { i } ( t )$ and $Z _ { s } ( t )$ , respectively. To ensure that all queues are stable as in (13f), we introduce the Lyapunov drift as

$$
\Delta ( \Theta ( t ) ) \triangleq \mathbb { E } \left[ \mathcal { L } ( \Theta ( t + 1 ) ) - \mathcal { L } ( \Theta ( t ) ) \vert \Theta ( t ) \right] .\tag{16}
$$

To maximize the MOS with constraints on queue stability, we define the Lyapunov drift-minus-reward function as

$$
\Delta _ { V } ( \Theta ( t ) ) \triangleq \Delta ( \Theta ( t ) ) - V \mathbb { E } \left[ \mathrm { M O S } _ { \mathrm { s y s } } ( t + 1 ) | \Theta ( t ) \right] ,\tag{17}
$$

where $V > 0$ is the Lyapunov control parameter for balancing between queue stability and maximizing the objective function (13a). The expectation is conducted over the randomness of the wireless channel and the arrival traffic of users.

By using the opportunistic expectation minimization technique introduced in [33], we can transform $\mathcal { P }$ into minimizing the Lyapunov-drift-minus-rewardâs upper bound in each time slot. The upper bound of $\Delta _ { V } ( \mathbf { Q } ( { \bar { t } } ) )$ is essential for the transformation and is given in the following theorem.

Theorem 1: The drift-minus-reward $\Delta _ { V } ( \Theta ( t ) )$ has the following upper bound for all t and any $V > 0 :$

$$
\begin{array} { r l r } {  { \le B + \psi _ { Q } \sum _ { i = 1 } ^ { N } \mathbb { E } [ Q _ { i } ( t ) ( A _ { i } ( t ) - R _ { i } ( t ) ) | \Theta ( t ) ] } } \\ & { } & { + \frac { V C _ { 1 } } { | \mathbb { U } _ { t } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \mathbb { E } [ \ln ( d _ { 0 } \lambda _ { i } + Q _ { i } ( t ) + A _ { i } ( t ) - \tilde { R } _ { i } ( t ) ) \Big | \Theta ( t ) ] } \\ & { } & { + \psi _ { Z } \sum _ { s = 1 } ^ { M } \mathbb { E } [ Z _ { s } ( t ) ( P _ { s } ( t ) - P _ { s } ^ { \mathrm { t h } } ) | \Theta ( t ) ] , \qquad ( 1 8 ) } \end{array}
$$

where $\tilde { R } _ { i } ( t ) = \operatorname* { m i n } \left\{ Q _ { i } ( t ) + A _ { i } ( t ) , R _ { i } ( t ) \right\}$ , and B is a finite positive constant that satisfies

$$
\begin{array} { c } { { \displaystyle B \geq \frac { 1 } { 2 } \psi _ { Q } \displaystyle \sum _ { i = 1 } ^ { N } \mathbb { E } \left[ \left. A _ { i } ( t ) ^ { 2 } + \tilde { R } _ { i } ( t ) ^ { 2 } - 2 A _ { i } ( t ) R _ { i } ( t ) \right| \Theta ( t ) \right] } } \\ { { \displaystyle ~ - \frac { V } { | \mathbb { U } _ { t } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \left( C _ { 1 } \ln \left( \lambda _ { i } \right) + C _ { 2 } \right) - \psi _ { Z } \displaystyle \sum _ { s = 1 } ^ { M } \mathbb { E } \left[ \left. P _ { s } ^ { \mathrm { t h } } P _ { s } ( t ) \right| \Theta ( t ) \right] } } \\ { { \displaystyle ~ + \frac { 1 } { 2 } \psi _ { Z } \displaystyle \sum _ { s = 1 } ^ { M } \mathbb { E } \left[ \left. P _ { s } ( t ) ^ { 2 } + ( P _ { s } ^ { \mathrm { t h } } ) ^ { 2 } \right| \Theta ( t ) \right] , \forall t \in \mathbb { T } } } \end{array}\tag{t)}
$$

19)

Such a constant B exists with the assumption of the boundedness of the arrival and departure rates of all queues, i.e., there exists some finite constant $\sigma ^ { 2 } > 0$ such that E $, [ A _ { i } ( t ) ] <$ $\sigma ^ { 2 } , \mathbb { E } \left[ R _ { i } ( t ) \right] < \sigma ^ { 2 }$ , and $\mathbb { E } \left[ P _ { s } ( t ) \right] < \sigma ^ { 2 } , \forall t \in \mathbb { T } , i \in \dot { \mathbb { N } } , s \in \mathbb { S } .$ Proof: Please see Appendix A.

Taking the system state Q(t) observed at the beginning of a time slot as the input and removing constant terms in (18), we formulate the per-time-slot problem as

$$
\begin{array} { r l r } {  { \mathcal { P } ^ { \prime } : \operatorname* { m i n } _ { \mathbf { x } _ { t } } \ \psi _ { Q } \sum _ { i = 1 } ^ { N } Q _ { i } ( t ) ( A _ { i } ( t ) - R _ { i } ( t ) ) } } \\ & { } & { \mathrm { ~ } + \psi _ { Z } \sum _ { s = 1 } ^ { M } Z _ { s } ( t ) ( P _ { s } ( t ) - P _ { s } ^ { \mathrm { H b } } ) } \\ & { } & { \mathrm { ~ } + \frac { V C _ { 1 } } { | \mathbb { U } _ { t } ^ { + } | } \displaystyle \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \ln ( d _ { 0 } \lambda _ { i } + Q _ { i } ( t ) + A _ { i } ( t ) - \tilde { R } _ { i } ( t ) ) } \\ & { } & { \mathrm { s . t . } ( 1 3 b ) , ( 1 3 c ) , ( 1 3 d ) , ( 1 3 e ) } \end{array}
$$

where ${ \bf X } _ { t } = \{ k _ { i } ( t ) , { \bf p } _ { s } ( t ) , z _ { s } ( t ) , \forall i \in \mathbb { U } , s \in \mathbb { S } \}$ . Solving $\mathcal { P } ^ { \prime }$ is an efficient way to achieve the long-term objective (13a) of $\mathcal { P }$ while ensuring constraints (13f) on the queue stability and (13g) on the average propulsion power. Moreover, solving $\mathcal { P } ^ { \prime }$ requires only the current network information for decisionmaking; future knowledge of usersâ movement and arrival traffic is not required. Thus, the problem transformation from $\mathcal { P }$ to $\mathcal { P } ^ { \prime }$ is an online optimization design. Solving ${ \mathcal P ^ { \prime } }$ is NP-hard as stated in Theorem 2.

Theorem 2: The per-time slot problem $\mathcal { P } ^ { \prime }$ is NP-hard.   
Proof: Please see Appendix B.

## IV. THE PROPOSED LYAPUNOV-GUIDED DRL FRAMEWORK FOR DYNAMIC PLACEMENT OF UAV-BSS

We propose a two-step approach to solve $\mathcal { P } ^ { \prime }$ efficiently in each time slot. First, we utilize the K-means clustering algorithm to associate users to UAV-BSs, i.e., solving for $\kappa _ { i } ( t )$ of $\mathbf { X } _ { t }$ . This clustering step acts as a baseline solution for deploying UAVs for rate maximization. Next, a DRL algorithm built on top of the K-means clustering is utilized to adjust the UAVâs flying altitude and horizontal placements considering the user distribution and traffic demand in each cluster, i.e., solving for $\mathbf { p } _ { s } ( t )$ and $z _ { s } ( t )$ of $\mathbf { X } _ { t }$ . The proposed framework employs a DNN to learn the optimal movement policy for UAV-BSs from its experience with training data labeled by a Lyapunov-guided critic module. The schematic of the proposed two-step method is illustrated in Fig. 3, which is in synchronization with the structure of this section.

<!-- image-->  
Fig. 3. Schematic of the proposed two-step method for adaptive UAV placement.

## A. Dynamic User Clustering

We consider a dynamic network where the users continuously and freely move around the target area. Thus, one user might move out of one UAV-BSâs zone and become closer to another UAV-BS. It is necessary to re-associate users with UAV-BSs during the process. After clustering, each UAV-BS should be responsible for a disjoint set of users, and each user is assigned to exactly one UAV-BS.

We utilize the K-means algorithm to associate users to UAV-BSs based on their instantaneous positions as follows. As the beginning step, M cluster centroids are initialized at the UAVsâ horizontal coordinates $( x _ { s } , y _ { s } )$ . The algorithm proceeds by alternating between two steps:

Cluster Assignment Step: Assign each user to the cluster with the least Euclidean distance from the user to its centroid. Mathematically, this means partitioning all users based on the Voronoi diagram generated by the centroids.

â¢ Centroid Update Step: Recompute the centroids based on the location of users in each cluster.

The clustering algorithm converges when the positions of cluster centroids have changes smaller than a predefined threshold $\epsilon \ > \ 0 .$ . Details of the algorithm are given in Algorithm 1.

Remark 3: By initializing the cluster centroid at the horizontal coordinates of the UAV-BS, Algorithm 1 ensures that each UAV-BS is assigned to one user cluster in its vicinity.

```tcl
Algorithm 1 Dynamic User Clustering
Input: Usersâ location, $\mathbf { u } _ { i } \ \in \ \{ \mathbf { p } _ { i } ( t ) , \forall i \ \in \ \mathbb { U } \}$ , UAV-BSsâ
position, $\mathbf { v } _ { s } \in \{ \mathbf { p } _ { s } ( t ) , \forall s \in \mathbb { S } \}$ , and maximum iterations
$\tau _ { \mathrm { m a x } }$
Output: Users are assigned to UAV-BSs, ki(t), $\forall i \in \mathbb { U }$
1: $\tau = 0 \#$ Iteration index
2: $\mathbf { c } _ { s } ^ { \tau } = \mathbf { v } _ { s }$ for $s = 1 , 2 , \ldots , M \#$ Initialize cluster centroids
3: repeat
4: $\tau = \tau + 1$
5: $\mathbb { C } _ { s } = \emptyset$ for all $s = 1 , 2 , \ldots , M$
6: # Cluster assignment step
7: for each user $i \in \mathbb { U }$ do
8: $s ^ { * }  \mathrm { a r g }$ mins $\left\{ \Vert \mathbf { u } _ { i } - \mathbf { c } _ { s } ^ { \tau } \Vert ^ { 2 } \right\} i$ # The closet cluster
9: $\mathbb { C } _ { s ^ { * } }  \mathbb { C } _ { s ^ { * } } \cup \{ i \} \#$ Assign user i to the closet cluster
10: $k _ { i } \gets s ^ { * }$
11: end for
12: # Centroid update step
13: for each UAV-BS $s \in \mathbb { S }$ do
14: $\begin{array} { r } { \mathbf { c } _ { s } ^ { \tau } \gets \frac { 1 } { | \mathbb { C } _ { s } | } \sum _ { i \in \mathbb { C } _ { s } } } \end{array}$ ui# Recompute cluster centroids
15: end for
16: until $\begin{array} { r } { \sum _ { s = 1 } ^ { M } \| \mathbf { c } _ { s } ^ { \tau } - \mathbf { c } _ { s } ^ { \tau - 1 } \| ^ { 2 } \leq \epsilon ~ \mathrm { o r } ~ \tau \geq \tau _ { \operatorname* { m a x } } } \end{array}$
17: return: $k _ { i }$ for all $i \in \mathbb { U }$
```

As noted, each UAV-BS is assigned to one disjoint set of users after the clustering step in each time slot. The clustering is dynamic based on the instantaneous placement of the users and UAVs. Based on the spatial distribution of the users and their traffic demands, the UAV-BS will adjust its flying altitude and horizontal coordinates using a DRL-based algorithm explained in the following section.

## B. DRL-Based UAV-BS Placement

In the considered dynamic network, the spatial distribution of network traffic continuously changes over time with usersâ random movements and arrival traffic. The 3D position of

UAV-BSs should adapt to the time-varying network situation for better usersâ QoE. We propose a DRL-based framework to adjust the UAV-BS position in each time slot based on the instantaneous spatial distribution of network traffic. The framework obtains the UAV-BSâs flying altitude and horizontal coordinates and the usersâ current location and traffic demand as the input. The framework then outputs a movement decision in 3D for each UAV-BS, which is then used to update network statistics in the next time slot. Note that the userâs location and traffic demand continuously change over time; thus, the optimal placement of UAV-BSs also varies over time.

Fig. 3 illustrates the framework with three core modules, including a DNN-based actor module, a Lyapunov-guided critic module, and a policy update module. The actor module obtains the usersâ location and traffic demands after the clustering step and adopts a DNN and an action quantizer to output K potential movement decisions for each UAV-BS, denoted as $\tilde { \mathbf { v } } _ { 1 } , \ldots , \tilde { \mathbf { v } } _ { K }$ . The critic module evaluates K decisions generated by the actor and selects the best one (denoted as $\mathbf { v } _ { s } ^ { * } )$ that minimizes the Lyapunov drift-minusreward function as specified in ${ \mathcal P ^ { \prime } }$ . Decision $\mathbf { v } _ { s } ^ { * }$ is then used as the training label for the DNNâs input, i.e., the policy update module logs a history of the DNN input and the corresponding optimal UAV movement in a replay memory. A DNN optimizer (e.g., Adam algorithm [36]) is employed to periodically retrain the actor moduleâs DNN, thereby enabling the movement policy to dynamically adapt to the evolving network conditions.

The UAV placement design based on reinforcement learning is summarized in Algorithm 2 with details as follows.2

1) DNN-Based Actor Module: The actor module consists of a heatmap generator, a DNN, and an action quantizer.

Heat Map Generator: For each user cluster, the numerical statistics of users are converted into a graphical form of a heatmap. The heatmap presents the spatial distribution of the user traffic demand in the target area, where $\mathbf { H } _ { s } ^ { t }$ denote the traffic heatmap of the user cluster corresponding to UAV-BS s at time t. To generate a heatmap, we divide the entire area into square grids of size $d _ { s } \times d _ { s }$ (m). The normalized queue length of all users in a certain grid contributes to that gridâs traffic demand. At the output, we obtain one traffic heatmap of size $n _ { s } \times n _ { s }$ for each user cluster, where $n _ { s } = \lceil 2 R / d _ { s } \rceil$

DNN-based Actor: We develop a DNN model to represent the movement policy for UAV-BSs. The DNN has three inputs: the UAVâs propulsion power virtual queue length, $Z _ { s } ( t )$ , the UAVâs 3D coordinates, $( \hat { x } _ { s } ^ { t } , \hat { y } _ { s } ^ { t } , \hat { z } _ { s } ^ { t } )$ , and the traffic heatmap of all users in its cluster, Hts. At the output, the DNN produces a relaxed decision on the $\mathrm { U A V ^ { , } s \ x ^ { - } , \ y ^ { - } }$ , and z-axis velocity, $\mathbf { v } _ { s } = [ v _ { s } ^ { \mathrm { x } } , v _ { s } ^ { \mathrm { y } } , v _ { s } ^ { \mathrm { z } } ] ^ { \intercal }$ . These three variables determine the direction and distance traveled by the UAV in the 3D space.

Fig. 4 illustrates the neural network architecture of the actor module. The userâs traffic heatmap, $\mathbf { H } _ { s } ^ { t } ,$ is first passed through some convolutional and max-pooling layers to reduce the data dimensionality and extract a rich feature vector for the user sideâs situation. This vector is then concatenated with the normalized vector representing the UAVâs virtual queue and coordinates, $\left\{ Z _ { s } ^ { t } , \hat { x } _ { s } ^ { t } , \hat { y } _ { s } ^ { t } , \hat { z } _ { s } ^ { t } \right\}$ , to construct a high-dimensional vector representing the whole system state. After several fully-connected layers, we obtain a three-dimensional vector, $\mathbf { v } _ { s } = [ v _ { s } ^ { x } , v _ { s } ^ { y } , v _ { s } ^ { z } ] ^ { \tau }$ , presenting the prediction for the optimal horizontal movement of the UAV. To ensure constraints (13c) and (13d) on the UAVâs maximum velocity, we utilize the tanh activation function,

Algorithm 2 Adaptive UAV Placement   
1: Initialize empty queues: $Q _ { i } ^ { t } = 0$ for all users at $t = 0$   
2: Initialize the DNN with random parameters   
3: Initialize an empty replay memory   
4: for $t = 0 , 1 , \dots , T - 1$ do   
5: Observe network situation: $( x _ { i } ^ { t } , y _ { i } ^ { t } ) , A _ { i } ^ { t } , Q _ { i } ^ { t }$ for all $i \in$   
U, and $\left( Z _ { s } ^ { t } , x _ { s } ^ { t } , y _ { s } ^ { t } , z _ { s } ^ { t } \right)$ for all $s \in \mathbb { S }$   
6: Cluster users based on Algorithm 1 to obtain $k _ { i } ^ { t }$ and   
$\mathbb { C } _ { s } ^ { t }$   
7: for each UAV-BS $s \in \mathbb { S }$ do   
8: Generate a heatmap $\mathbf { H } _ { s } ^ { t }$ for cluster $\mathbb { C } _ { s } ^ { t }$ based on the   
user location $( x _ { i } ^ { t } , y _ { i } ^ { t } )$ and traffic demand $A _ { i } ^ { t } + Q _ { i } ^ { t }$ ,   
$\forall i \in \mathbb { C } _ { s } ^ { t }$   
9: Normalize the UAV-BS location to obtain   
$( \hat { x } _ { s } ^ { t } , \hat { y } _ { s } ^ { t } , \hat { z } _ { s } ^ { t } )$   
10: Pass $\mathbf { H } _ { s } ^ { t }$ and $( Z _ { s } ^ { t } , \hat { x } _ { s } ^ { t } , \hat { y } _ { s } ^ { t } , \hat { z } _ { s } ^ { t } )$ to the DNN to obtain   
${ \bf v } _ { s }$   
11: Quantize ${ \bf v } _ { s }$ to obtain K actions $\{ \tilde { \mathbf { v } } _ { 1 } , \hdots , \tilde { \mathbf { v } } _ { K } \}$ via   
(22)   
12: Select the best action $\mathbf { v } _ { s } ^ { * }$ that minimizes (20a) of   
$\mathcal { P } ^ { \prime }$   
13: Add data sample $\{ \mathbf { H } _ { s } ^ { t } , ( Z _ { s } ^ { t } , \hat { x } _ { s } ^ { t } , \hat { y } _ { s } ^ { t } , \hat { z } _ { s } ^ { t } ) \}$ with label   
$\mathbf { v } _ { s } ^ { * }$ to the replay memory   
14: if t mod $\delta _ { T } = 0$ then   
15: Retrain the actorâs DNN using data samples   
saved in the replay memory using Adam opti  
mizer   
16: end if   
17: Update $Z _ { s } ^ { t + 1 }$ and $\left( x _ { s } ^ { t + 1 } , y _ { s } ^ { t + 1 } , z _ { s } ^ { t + 1 } \right)$   
18: end for   
19: for each user $i \in \mathbb { U }$ do   
20: Update $R _ { i } ^ { t }$ based on $( x _ { i } ^ { t } , y _ { i } ^ { t } )$ and $( x _ { k _ { i } ^ { t } } ^ { t } , y _ { k _ { i } ^ { t } } ^ { t } , z _ { k _ { i } ^ { t } } ^ { t } )$ via   
(6)   
21: Update $Q _ { i } ^ { t + 1 }$ based on $A _ { i } ^ { t }$ and $R _ { i } ^ { t }$ via (7)   
22: Update user location $( x _ { i } ^ { t + 1 } , y _ { i } ^ { t + 1 } ) ^ { \circ }$ via (2)   
23: end for   
24: end for

$$
\operatorname { t a n h } { ( x ) } = \frac { e ^ { 2 x } - 1 } { e ^ { 2 x } + 1 } ,\tag{21}
$$

at the output layer of the DNN so that the normalized velocities $v _ { s } ^ { x } ,$ $v _ { s } ^ { y } .$ , and $v _ { s } ^ { z }$ are all in range [â1; 1]. Later, we multiply these normalized values with the UAVâs maximum velocity to obtain the practical movement velocity. The normalized velocities are continuous and could be negative, enabling the UAV-BS to fly in any direction with flexible speeds in three dimensions.

Action Quantizer: To facilitate the learning process, we quantize the DNNâs output into several potential movement decisions, which are to be judged by the critic module to determine the best one. From velocity vector ${ \bf v } _ { s }$ , we obtain new decisions by adding Gaussian noises to ${ \bf v } _ { s }$ as

<!-- image-->  
Fig. 4. The actorâs DNN model.

$$
\tilde { \mathbf { v } } _ { k } = \left\{ \begin{array} { l l } { \mathbf { 0 } , } & { \mathrm { f o r } k = 0 } \\ { \mathbf { v } _ { s } , } & { \mathrm { f o r } k = 1 } \\ { \operatorname { t a n h } ( \mathbf { v } _ { s } + \mathbf { n } _ { k } ) , } & { \mathrm { f o r } k = 2 , . . . , K } \end{array} \right.\tag{22}
$$

where Tanh $\left( \mathbf { v } _ { s } + \mathbf { n } _ { k } \right)$ denotes the element-wise tanh function on $\mathbf { v } _ { s } + \mathbf { n } _ { k }$ , and $\mathbf { n } _ { k } \sim \mathcal N ( \mathbf { 0 } , \sigma _ { n } ^ { 2 } \mathbf { I } )$ denotes a three-dimensional zero-mean random vector following the normal distribution with the diagonal covariance matrix $\sigma _ { n } ^ { 2 } { \mathbf I }$ . Here, I denotes the identity matrix, and $\sigma _ { n } ^ { 2 }$ is a hyperparameter specifying the balance between exploration and exploitation of the action quantizer. Small values of $\sigma _ { n } ^ { 2 }$ emphasize exploitation, while large values facilitate exploration in finding the optimal solution of $\mathcal { P } ^ { \prime }$ based on the DNN output.

2) Lyapunov-Guided Critic Module: The critic module obtains the K potential decisions $\{ \tilde { \mathbf { v } } _ { 1 } , \hdots , \tilde { \mathbf { v } } _ { K } \}$ from the actor module, then select among them the best action $\mathbf { v } _ { s } ^ { * }$ that minimizes the Lyapunov-drift-minus-reward function of $\mathcal { P } ^ { \prime }$ The movement decision selected by the critic module is used to update the location of the UAV-BS in the next time slot as

$$
[ x _ { s } ^ { t + 1 } , y _ { s } ^ { t + 1 } , z _ { s } ^ { t + 1 } ] ^ { \intercal } = [ x _ { s } ^ { t } , y _ { s } ^ { t } , z _ { s } ^ { t } ] ^ { \intercal } + \mathbf { v } _ { s } ^ { \ast } \tau .\tag{23}
$$

The decision $\mathbf { v } _ { s } ^ { * }$ is also the training data label for the current input of the DNN, which is the network state specified by the current UAV-BSâs normalized position $( \hat { x } _ { s } ^ { t } , \hat { y } _ { s } ^ { t } , \hat { z } _ { s } ^ { t } )$ and the corresponding user traffic heatmap $\mathbf { H } _ { s } ^ { t }$

As can be observed, our framework leverages the modelbased optimization to evaluate the actor moduleâs decisions instead of using another DNN for the critic module as conventional ones. Guided by the Lyapunov-drift-minus-reward function, the critic module can accurately evaluate which decision is better for the current network situation. This facilitates the convergence in training the actor moduleâs DNN.

It is worth noting that the number of decisions evaluated by the critic module, K, is another hyperparameter for the tradeoff between performance and computational complexity. Large values of K generally result in shorter convergence time but require more computational resources.

3) Policy Update Module: The policy update module exploits training data labeled by the critic module to update the actor moduleâs DNN. A replay memory is maintained to record training data, defined as the pair of the DNNâs input, $\{ \mathbf { H } _ { s } ^ { t } , ( \hat { x } _ { s } ^ { t } , \hat { y } _ { s } ^ { t } , \tilde { z } _ { s } ^ { t } ) \}$ and the critic moduleâs output, $\mathbf { v } _ { s } ^ { * } .$ . The networkâs historical data is stored in two distinct sets, one used for training and the other for validation. The replay memory has a finite size, and new data samples replace the old ones when the memory counter reaches the limit. This technique ensures the training utilizes the most recent observations and the framework can adapt to the new operating situations.

The actor moduleâs DNN is trained periodically once every $\delta _ { T }$ time slots to prevent overfitting and enables the DNN to adapt to new network conditions. For training, the policy update module selects a random batch of samples from the replay memory to train the DNN using Adam optimizer [36]. The Mean Squared Error (MSE) loss function is utilized,

$$
\mathrm { M S E } ( t ) = \frac { 1 } { 3 | \mathcal { B } _ { t } | } \sum _ { \tau \in \mathcal { B } _ { t } } ( \mathbf { v } _ { \tau } - \mathbf { v } _ { \tau } ^ { * } ) ^ { \intercal } \left( \mathbf { v } _ { \tau } - \mathbf { v } _ { \tau } ^ { * } \right) ,\tag{24}
$$

where $B _ { t }$ denotes the index set of data samples selected for training at time $t ; \textbf { v } _ { \tau }$ and $\mathbf { v } _ { \tau } ^ { * }$ respectively denote the flying decision selected by the actorâs DNN and the critic module.

Remark 4: The proposed framework can naturally adapt to new working conditions, such as changes in the total number of users in the target operating zone. The reason is that the numerical statistics of users are translated into heatmaps whose size is unchanged with any number of users.

Remark 5: With the design of a continuous action space, the proposed framework is not limited to any directions as conventional Q-learning-based approaches, e.g., [7]. In fact, with combinations of $( v _ { s } ^ { \mathrm { x } } , v _ { s } ^ { \mathrm { y } } , v _ { s } ^ { \mathrm { z } } ) ,$ the UAV can fly in any direction and at flexible speeds in 3D space.

## V. ALGORITHM ANALYSIS

## A. Computational Complexity

The computational complexity of the proposed method presented in Algorithm 2 is as follows.

â¢ First, the K-means clustering step (Line 6, Algorithm 2) has complexity in $\mathcal { O } ( M N \bar { \tau } _ { \mathrm { m a x } } )$ , where M and N denote the number of UAVs and users, respectively, and $T _ { \mathrm { m a x } }$ denotes the maximum number of iterations in the clustering process (Line 1, Algorithm 1).

â¢ After clustering, the computation load for UAV placement includes two main steps. First, generating the traffic heatmap of N users (Line 16, Algorithm 2) has complexity in O(N ). Next, evaluating K potential decisions of the action quantizer (Line 12, Algorithm 2) has complexity in O(N K) since the evaluation for one decision is in O(N ). For each UAV, the computation is thus in O(NK), and for M UAVs, it takes O(M N K).

Overall, combining the user clustering and UAV placement steps has computational complexity in $\mathsf { \bar { O } } \left( M N \left( \tau _ { \operatorname* { m a x } } + K \right) \right)$ , which is feasible for real-time control.3

## B. Optimality Analysis

We denote by Ï(t) the random traffic of all users, $\omega ( t ) =$ $\{ A _ { i } ( t ) , \forall i \in \mathbb { U } \}$ , and assume that $\omega ( t )$ is an independently and identically distributed (IID) random process. Also, let $\alpha ( t )$ denote the control action in time slot $t , \mathrm { i . e . , } \alpha ( t ) = \mathbf { X } _ { t }$ . We define an Ï-only policy as a policy that observes $\omega ( t )$ in each time slot and makes control decision $\alpha ( t )$ independent of the queues $Q _ { i } ( t ) , \ Z _ { s } ( t )$ . The asymptotic optimality of Algorithm 2 in solving P is provided in the following theorem:

Theorem 3: Suppose that $\omega ( t )$ is IDD over slots, the problem $( { \cal I } 3 a ) â ( { \cal I } 3 g )$ is feasible, and E $[ \mathcal { L } ( \Theta ( 0 ) ) ] < \infty$ . If an algorithm produces a C-additive approximation $( C \ge 0 )$ of the minimum over all possible actions of the right-hand side of (18) every time slot, then the time-average MOS of all users satisfies

$$
\operatorname* { l i m } _ { T  \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } [ \mathrm { M O S } _ { \mathrm { s y s } } ( t ) ] \geq \mathrm { M O S } _ { \mathrm { s y s } } ^ { \ast } - \frac { \hat { B } + C } { V } ,\tag{25}
$$

where $\mathrm { M O S _ { s y s } ^ { * } }$ is the maximum time-average MOS achievable by any policy that meets the required constraints, and $\hat { B } =$ $\begin{array} { r } { \dot { B } + \frac { { \bf \bar { \Delta } } ^ { \prime } } { | \mathbb { I } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \left( C _ { 1 } \ln \left( \lambda _ { i } \right) + C _ { 2 } \right) } \end{array}$ with B given in (19). t  Proof: Please see Appendix C.

## VI. NUMERICAL RESULTS AND DISCUSSIONS

## A. Simulation Setup

This section provides numerical results for evaluating the proposed DRL frameworkâs performance in a dynamic environment. If not otherwise stated, we consider $N = 1 0 0$ users and $M \ = \ 4 \ \mathrm { \ U A V  â B S s }$ in an urban area of $\mathrm { 5 0 0 \times 5 0 0 m ^ { 2 } }$ Initialized at random positions (uniformly distributed), the users move around independently following the Gauss-Markov mobility model [28] with average speed $\bar { v } = 1$ m/s, memory level $\alpha { = } 0 . 5$ , and standard deviation $\sigma = 1 ~ \mathrm { m / s } .$ The downlink traffic of the users is simulated using the ON/OFF traffic model [30]. The arrival traffic in the ON state is Pareto distributed with mean $\lambda \ = \ 2$ Mbps, and the ON/OFF periods are exponentially distributed with mean $\mu _ { \mathrm { O N } } = 5 0 0 ~ \mathrm { s } , \mu _ { \mathrm { O F F } } = 5 0 0$ s. The UAVs fly with the horizontal/vertical maximum speed $v _ { \mathrm { x v } } ^ { \mathrm { m a x } } = 3 0$ m/s and $v _ { \mathrm { z } } ^ { \operatorname* { m a x } } = 3$ m/s, and the flying altitude z ranging from $z _ { \mathrm { m i n } } = 1 0 0$ m to $z _ { \mathrm { m a x } } = 2 0 0$ m. For the UAV propulsion energy model, we set blade angular speed $\omega = 2 0 0$ rad/s, rotor solidity $s = 0 . 1 2$ , aircraft weight $W = 1$ kg, and other parameters following [35, Table I] for rotarywing UAVs. For benchmark methods, we set a constant flying speed that maximizes the UAV endurance, i.e., minimizes the propulsion power consumption, $\begin{array} { r } { V _ { \mathrm { m e } } = \arg \operatorname* { m i n } _ { v \geq 0 } P ( v ) } \end{array}$ [35]. In performance evaluation, Jainâs fairness index [37], defined as $\dot { \mathbb { E } } [ X ] ^ { 2 } / \mathbb { E } [ X ^ { 2 } ]$ ], is adopted to investigate the QoE fairness of users. Other parameters are summarized in Table IV.

We implement the DNN using Tensorflow with regularization factor $\lambda _ { \mathrm { r g } } = 1 0 ^ { - 3 }$ and the Adam optimization algorithm with learning rate $\eta = 5 \times 1 0 ^ { - 4 }$ . To generate heatmaps, we set up a grid size of $2 0 \times 2 0 ~ \mathrm { m } ;$ thus, each heatmap is of size $2 5 \times 2 5$ (as illustrated in Fig. 4). The action quantizer generates $K \ = \ 1 0$ potential decisions based on the CNN output. The memory size for training and validation are 1024 and 256 samples, respectively. The training/validation replay memories are separated and refreshed continuously when the critic module labels new data samples.

For performance evaluation, we consider the following four benchmark approaches for UAV-BS deployment:

1) Stationary: The UAVs are placed at stationary positions. These positions could be optimized for the UAVs at a specific time slot but remain unchanged when users roam. Specifically, the UAVs move towards cluster centroids found by the K-means algorithm at $t ~ = ~ 0$ While this approach achieves rate optimality for static networks, it becomes sub-optimal with user mobility.

SIMULATION PARAMETERS  
TABLE IV
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1> $\overline { { W , f _ { c } } }$ </td><td rowspan=1 colspan=1>Channel bandwidth and carrier frequency</td><td rowspan=1 colspan=1>30 MHz,2 GHz</td></tr><tr><td rowspan=1 colspan=1> $a _ { 1 } , b _ { 1 }$ </td><td rowspan=1 colspan=1>Coefficients for the LoS probability</td><td rowspan=1 colspan=1>12.08,0.11 [32]</td></tr><tr><td rowspan=1 colspan=1> $a _ { 2 } , b _ { 2 }$ </td><td rowspan=1 colspan=1>Coefficients for the path loss exponent</td><td rowspan=1 colspan=1>1.5,3.5 [33]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { d _ { \operatorname* { m i n } } , d _ { \operatorname* { m a x } } } }$ </td><td rowspan=1 colspan=1>QoEcoefficients for web-browsing service</td><td rowspan=1 colspan=1>0.67,6 [35]</td></tr><tr><td rowspan=1 colspan=1> $d _ { 0 }$ </td><td rowspan=1 colspan=1>Minimumdelay forcommunications overhead</td><td rowspan=1 colspan=1>0.5ms</td></tr><tr><td rowspan=1 colspan=1> $S$ </td><td rowspan=1 colspan=1>Attenuation effect of the Non-LoSlink</td><td rowspan=1 colspan=1>0.2</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P _ { t } } }$ </td><td rowspan=1 colspan=1>Transmit power of the UAV-BS</td><td rowspan=1 colspan=1>23dBm</td></tr><tr><td rowspan=1 colspan=1> $g _ { 0 }$ </td><td rowspan=1 colspan=1>Reference signal gain</td><td rowspan=1 colspan=1>-40dB</td></tr><tr><td rowspan=1 colspan=1> $N _ { 0 }$ </td><td rowspan=1 colspan=1>Noise level of the wirelesschannel</td><td rowspan=1 colspan=1>-90 dBm</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \delta _ { T } } }$ </td><td rowspan=1 colspan=1>Periodic training cycle of the DNN</td><td rowspan=1 colspan=1>5 slots</td></tr><tr><td rowspan=1 colspan=1> $\overline { { V } }$ </td><td rowspan=1 colspan=1>Lyapunov control parameter</td><td rowspan=1 colspan=1>5000</td></tr><tr><td rowspan=1 colspan=1> $\overline { { K } }$ </td><td rowspan=1 colspan=1>Number of decisions of the quantizer</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P _ { s } ^ { \mathrm { t h } } } }$ </td><td rowspan=1 colspan=1>Propulsionpowerthreshold forUAVs</td><td rowspan=1 colspan=1>100W</td></tr></table>

TABLE V

COMPLEXITY COMPARISON
<table><tr><td rowspan=1 colspan=1>Algorithm</td><td rowspan=1 colspan=1>Complexity</td><td rowspan=1 colspan=1>Optimality</td><td rowspan=1 colspan=1>Queue Stability</td></tr><tr><td rowspan=1 colspan=1>Centroid-based</td><td rowspan=1 colspan=1> $\overline { { \mathcal { O } ( M N \tau _ { \operatorname* { m a x } } ) } }$ </td><td rowspan=1 colspan=1>Sub-optimal</td><td rowspan=1 colspan=1>No assurance</td></tr><tr><td rowspan=1 colspan=1>Majority-vote</td><td rowspan=1 colspan=1> $\overline { { \mathcal { O } ( M N ) } }$ </td><td rowspan=1 colspan=1>Sub-optimal</td><td rowspan=1 colspan=1>No assurance</td></tr><tr><td rowspan=1 colspan=1>DQL-based</td><td rowspan=1 colspan=1> $\overline { { \mathcal { O } ( M N \tau _ { \operatorname* { m a x } } ) } }$ </td><td rowspan=1 colspan=1>Sub-optimal</td><td rowspan=1 colspan=1>No assurance</td></tr><tr><td rowspan=1 colspan=1>LyDRL (Proposed)</td><td rowspan=1 colspan=1> $\overline { { \mathcal { O } ( M N ( \tau _ { \operatorname* { m a x } } + K ) ) } }$ </td><td rowspan=1 colspan=1>Sub-optimal</td><td rowspan=1 colspan=1>Stable</td></tr><tr><td rowspan=1 colspan=1>Exhaustive search</td><td rowspan=1 colspan=1> $\overline { { { \mathcal { O } } ( N ^ { M } + M N ) } }$ </td><td rowspan=1 colspan=1>Optimal</td><td rowspan=1 colspan=1>Stable</td></tr></table>

2) Centroid-based: The UAV placement is adaptive to the dynamic distribution of users, where the UAVs greedily move toward the centroid of user clusters found by Algorithm 1 every time step. Centroid is a greedy approach that maximizes the userâs sum rate when considering user movements. However, this approach ignores the heterogeneous nature of user traffic demands and, thus, may not be the optimal approach to satisfying user demands.

3) Majority-based: The UAVs are adaptively placed following a majority-vote rule [16] for rate maximization. The displacement factor $\beta = 0 . 1$ is set via [16, Fig. 6] for user density $4 { \times } 1 0 ^ { - 4 } \mathrm { u s e r s / m ^ { 2 } }$ . Four UAVs equally share the target area, each covering a zone of $2 5 0 { \times } 2 5 0 ~ \mathrm { m } ^ { 2 }$

4) DQL-based: The placement of UAVs is adaptive for rate maximization based on the actor-critic Deep Q-Learning (DQL) approach in [19]. While the original method is for single-UAV deployment, we enable an extension for multiple UAVs by incorporating Algorithm 1 into the framework. Furthermore, the user distribution heatmap is employed (instead of raw positions) to enable the method to process user groups with dynamic sizes.

To ensure a fair comparison, all benchmark methods are set to maintain a stable altitude of $z _ { 0 } = 1 5 0$ m, equidistant from the minimum and maximum allowable flying altitudes. These benchmark approaches are to investigate the QoE enhancement achieved by the proposed traffic-aware method over conventional throughput-maximization approaches. Table V compares computational complexity, where all benchmarks are sub-optimal to QoE maximization since they do not consider user traffic demands in optimization. Hereinafter, the proposed method is referred to as LyDRL for conciseness.

<!-- image-->  
Fig. 5. Spatial distribution of the users and UAVs.

<!-- image-->  
Fig. 6. Spectral efficiency of UAV links.

It is noteworthy that comparing the proposed LyDRL approach with other conventional learning-based methods would be beneficial. However, we found that state-of-theart learning-based adaptive placement approaches [7], [16], [17], [18], [19], [25] do not support training a RL agent with dynamic user association to multiple UAVs, i.e., when the cardinality of the user set assigned to each UAV varies continuously over time. The proposed method tackles this issue by converting the network state (the usersâ location and traffic demand) into a traffic heatmap instead of directly using the coordinates of users as the DNNâs input. Due to these reasons, we do not consider other learning-based approaches in simulations.

First, Fig. 5 illustrates the spatial distribution of the users and four UAVs with the proposed LyDRL method at a representative time step. The figure shows four clusters of users, each is served by one UAV. The horizontal placement of UAVs is dependent on the spatial distribution and traffic demands of users in each cluster. The UAV altitude is correlated with the spatial dispersion of users. When users are geographically dispersed, the UAV operates at higher altitudes for efficient coverage (e.g., UAV 2). Conversely, lower UAV altitudes are employed for concentrated user clusters (e.g., UAV 1).

In Fig. 6, we illustrate the corresponding spatial distribution of the downlink rate provided by the four UAVs in Fig. 5. We observe the spectrum efficiency has a bowl-like shape. The peak rate is achieved at the UAVâs horizontal position with a value depending on the UAVâs flying altitude. Flying at lower altitudes results in higher peak rates (due to the path loss reduction). The horizontal and vertical placement of UAVs is discussed in detail in Sections VI-C and VI-D.

Fig. 7 shows the training loss of the learning algorithm (Lines 14-15 in Algorithm 2). The validation loss closely follows the trend of the training loss, indicating an efficient training process without overfitting. Furthermore, the diminishing loss demonstrates the convergence of training, with the DNNâs predicted decisions converging with the optimal solution identified by the Lyapunov-guided critic module.

<!-- image-->  
Fig. 7. Training and validation loss.

## B. Performance Comparison

In Fig. 8, we investigate the proposed methodâs performance compared to its benchmark methods. Four UAVs start moving from the four corners of the target area to serve mobile users with random traffic. All methods are simulated using the same time-series data of the userâs movements and traffic.

Fig. 8a shows that the average MOS of users gradually increases for all methods when the UAVs travel from the four corners to the center of four user clusters. The MOS improvement provided by the proposed method comes out at the end of the process. There is little difference among methods in the beginning (the first 100 steps, Fig. 8a); however, the gap between the proposed method and its benchmark schemes enlarges over time. From Fig. 8b, we further observe that using the proposed method, the number of users with poor QoE scores (MOS ratings of 1 and 2) has significantly shrunk down while the two benchmarks still have a large portion of users with poor ratings in the end.

To further investigate the performance, we plot in Figs. 8d, 8e, and 8f the percentage of unavailability, Jainâs fairness index on the MOS, and the distribution of service response time of users, respectively. Fig. 8d shows that the proposed LyDRL outperforms all rate-maximization methods regarding service availability with an improvement of about 10% of users having the service response time within dmax. In Fig. 8e, the QoE fairness among users is also significantly improved for the proposed LyDRL method, thanks to the fact that the portion of users with poor ratings is greatly shrunk down (Fig. 8b). In Fig. 8f, the service response timeâs upper bound of the proposed LyDRL method is greatly smaller compared to those of benchmark methods, indicating that the userâs download queues are more stable, and the perceived downlink rate is sufficient to accommodate the userâs traffic demand.

There are three main reasons for the superior performance of the proposed LyDRL method. First, LyDRL considers the traffic demand of users to adjust the placement of UAVs, while all benchmark methods are solely based on the spatial information of users. Specifically, LyDRL enables UAVs to prioritize the users with high traffic demands to ensure these users obtain sufficient downlink rates. Second, the proposed method is backed by Lyapunov optimization to ensure queue stability; therefore, the service response time is sufficiently controlled. Note that benchmark methods have no assurance of the stability of queues, resulting in some remote users obtaining insufficient data rates and unacceptably large response times (Figs. 8d and 8f). Finally, while all benchmark methods are limited in 2D adaptive placement, the proposed method is flexible in 3D space, including adjustable flying altitudes. In Section VI-D, we show that the flying altitude is important in balancing the trade-off between maximizing the data rates of close and remote users. In turn, the proposed LyDRL method with a 3D adaptive placement approach enables more flexibility in satisfying the traffic demands of users.

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

<!-- image-->  
(f)

Fig. 8. Performance comparison: (a) Average QoE score (MOS) over time; (b) Cumulative distribution of the MOS in the last 250 steps; (c) Average downlink rate over time; (d) Percentage of users with service response time exceeding threshold dmax; (e) Jainâs fairness index on the MOS over time; and (e) Distribution of service response time (max, min, and median).  
<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 9. Proposed method: horizontal placement of 4 UAV-BSs in correspondence with the spatial distribution of (a) the downlink rate, (b) the traffic demand, and (c) the user at t = 200. Warmer colors in (a), (b), and (c) indicate better downlink rates, higher traffic demand, and higher user density, respectively.

Besides above observations, Figs. 8a and 8c also reveal a weak correlation between the average userâs MOS and the average downlink rate. In spite of the almost similar average downlink rate (Fig. 8c), the average MOS (Fig. 8a) and its distribution (Fig. 8b) are significantly different for different approaches. Consequently, maximizing the sum rate of all users might have little impact on the userâs MOS. The reason is that, from the userâs side, the MOS is evaluated based on their traffic demand satisfaction, i.e., how much data rate they perceived compared to their requested downlink rate. Therefore, the UAVs should consider not only the spatial distribution but also the traffic demand of users to improve the MOS rating. This observation again necessitates QoE-driven methods (i.e., maximizing the MOS) over the QoS-based approach of maximizing the sum rate of users.

## C. Optimal Horizontal Placement of UAVs

In Fig. 9, we show the horizontal placement of four UAV-BSs in correspondence with the traffic distribution using the proposed method. First, Fig. 9a illustrates the downlink rate versus the positions of ground users. We observe that the downlink rate provided by a swarm of UAV-BSs is not identically distributed: users closer to a UAV-BS will obtain a higher downlink rate than those far away in the same cluster. With four UAV-BSs, most users are provided high data rates, but some remote users (at the coverage areaâs corners) obtain lower rates (the blue regions in Fig. 9a). To this end, the UAV-BS placement can be adapted so that users with high demand remain closer while users with minimal traffic could be further away to maintain a high QoE for all users. Fig. 9b shows that users in the low-data rate regions in Fig. 9a have lower downlink demands (they all located in the blue regions, $\mathrm { e . g . }$ ï¼ A0 and C4, in Fig. 9b).

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 10. Optimal flying altitudes of UAV-BSs vs. (a) the number of UAVs (with N = 100 users) and (b) the number of users (with $M = 4 ~ \mathrm { U A V s } )$ (c) Spectral efficiency (b/s/Hz) vs. the radius distance and flying altitude of UAVs.

From Figs. 9b and 9c, we observe that the distribution of users might not be highly correlated with the network traffic, especially when the network traffic is not identically distributed among users. For example, region D0 has many users (Fig. 9c), but the downlink demand is not very high (Fig. 9b). To improve the overall MOS, the UAVs could be placed closer to hotspots with high traffic and further to areas with high user density but minimal downlink demand.

## D. Optimal Vertical Placement of UAVs

In Fig. 10, we investigate the statistics regarding flying altitudes of UAV-BSs with the proposed method. Recall that the UAVs continuously adjust their 3D position, including the flying altitudes, according to changes in the network traffic distribution. Fig. 10a shows that the UAVs tend to fly at lower altitudes when more UAVs are deployed. In addition, when the number of deployed UAVs is fixed, the flying altitudes tend to grow with the increase of ground users (Fig. 10b). The reason is that, on the one hand, increasing the flying altitude results in higher LoS probability due to higher elevation angles. On the other hand, path loss also increases due to the further communication distance with the increase in altitude.

As for illustration, we plot in Fig. 10c the spectral efficiency provided by one UAV flying at different altitudes vs. the radius distance to the ground users. Flying at the minimum altitude $( z _ { \mathrm { m i n } } = 1 0 0$ m) results in a high downlink rate for users in proximity (due to short communication range) but a degraded throughput for users far away (due to poor LoS). In contrast, when flying at the maximum altitude $( z _ { \mathrm { m a x } } = 2 0 0 \ \mathrm { m } )$ , the UAV can provide a better downlink rate for remote users (with better LoS) at the cost of lowering the rate of nearby users (due to longer communication distance).

Return to Fig. 10a, with more UAVs deployed, the user cluster becomes smaller in size and communication range. Thus, the UAV tends to fly at lower altitudes to maintain high downlink rates for users in its vicinity. Conversely, in Fig. 10b, with more users, the user spatial distribution is more spread. Thus, the UAVs increase their altitudes to maintain good downlink rates for remote users.

## VII. CONCLUSION

This paper investigates the joint optimization of dynamic user association and 3D adaptive placement of multiple UAV-BSs to maximize the userâs MOS. The user clustering is dynamic based on the instantaneous positions of users to the UAV-BSs using a K-means-based algorithm. Considering movements and time-varying downlink rate requirements of users, the UAV-BSs learn how to adjust their 3D locations using an actor-critic DRL framework. The normalized UAV-BSâs position and the traffic heatmap of users are passed to the actorâs DNN to predict the optimal movement for each UAV-BS. Numerical results with a simplified QoE model demonstrate the significant potential of the approach for coping with user mobility and heterogeneous data rate requirements. For practical application scenarios, the QoE model, however, should be tailored to various use cases for improvement. In future research, it would be interesting to investigate the optimal placement of UAV-BSs in the space-air-ground integrated networks, considering the backhaul link condition and onboard processing capability for edge computing/content caching services. Another interesting research direction would be forecasting user distribution and network traffic to plan the cardinality and deployment of UAV-BSs.

## APPENDIX A

## PROOF OF THEOREM 1

Proof: To find the upper bound of the Lyapunov driftminus-reward function, $\Delta _ { V } ( \Theta ( t ) )$ , we first derive the upper bounds of the Lyapunov functions for all actual and virtual queues, $\mathbf { Q } ( t )$ and $\mathbf { \bar { z } } ( t )$ Next, we derive the bound of the objective function $\mathrm { M O S } _ { \mathrm { s y s } } ( t )$ . The proof concludes by deriving the bound of $\Delta _ { V } ( \Theta ( t ) )$ by a summation operation.

To begin with, let $\begin{array} { r c l } { \mathbf { Q } ( t ) } & { \triangleq } & { \{ Q _ { i } ( t ) , \forall i \in \mathbb { U } \} } \end{array}$ be a concatenated vector of all usersâ download queues at time slot $t ,$ and $\begin{array} { r } { \mathcal { L } ( \mathbf { Q } ( t ) ) \triangleq \frac { 1 } { 2 } \psi _ { Q } \sum _ { i = 1 } ^ { N } Q _ { i } ( t ) ^ { 2 } } \end{array}$ denote the Lyapunov function of $\mathbf { Q } ( t )$ . By squaring equation (7) and applying the fact that (max $\bar { \{ a - b , 0 \bar { \} } } ) ^ { 2 } \leq \bar { ( a - b ) ^ { 2 } }$ , we obtain $Q _ { i } ( t + 1 ) ^ { 2 } \leq$ $\begin{array} { r l r } { \left( Q _ { i } ( t ) + A _ { i } ( t ) \right) ^ { 2 } } & { { } + } & { R _ { i } ( t ) ^ { 2 } \quad - \quad 2 \left( Q _ { i } ( t ) + A _ { i } ( t ) \right) R _ { i } ( t ) } \end{array}$ Therefore, we have $\begin{array} { r } { \frac { 1 } { 2 } \left( Q _ { i } ( t + \dot { 1 } ) ^ { 2 } - Q _ { i } ( t ) ^ { 2 } \right) } \end{array}$ â¤ ${ \textstyle \frac { 1 } { 2 } } \left( A _ { i } ( t ) ^ { 2 } + R _ { i } ( t ) ^ { 2 } \right) + Q _ { i } ( t ) { \tilde { ( } } { \tilde { A } } _ { i } ( t ) - R _ { i } ( t ) ) - A _ { i } ( t ) R _ { i } ( t )$ Taking conditional expectation of the previous inequation and summing up all users gives us the following bound

$$
\begin{array} { r l } & { \mathbb { E } \left[ \mathcal { L } ( \mathbf { Q } ( t + 1 ) ) - \mathcal { L } ( \mathbf { Q } ( t ) ) | \Theta ( t ) \right] } \\ & { \leq \frac { 1 } { 2 } \psi _ { Q } \sum _ { i = 1 } ^ { N } \mathbb { E } \left[ A _ { i } ( t ) ^ { 2 } + R _ { i } ( t ) ^ { 2 } - 2 A _ { i } ( t ) R _ { i } ( t ) \big | \Theta ( t ) \right] } \end{array}
$$

$$
\begin{array} { c l } { \displaystyle } & { \displaystyle + \psi _ { Q } \sum _ { i = 1 } ^ { N } \mathbb { E } [ Q _ { i } ( t ) ( A _ { i } ( t ) - R _ { i } ( t ) ) | \Theta ( t ) ] } \\ { = } & { \displaystyle B _ { 1 } + \psi _ { Q } \sum _ { i = 1 } ^ { N } \mathbb { E } [ Q _ { i } ( t ) ( A _ { i } ( t ) - R _ { i } ( t ) ) | \Theta ( t ) ] } \end{array}\tag{26}
$$

Assuming there exists a finite constant $\sigma ^ { 2 } > 0$ that satisfies $\mathbb { E } [ A _ { i } ( t ) ] , \ \breve { \mathbb { E } } [ R _ { i } ( t ) ] < \sigma ^ { 2 } , \forall t \in \mathbb { T } , i \in \mathbb { N }$ . With this boundedness assumption of the arrival traffic and downlink rate, $B _ { 1 }$ has an upper bound.

Next, for the propulsion energy constraint, let $\mathbf { Z } ( t ) \triangleq$ $\{ Z _ { s } ( t ) , \forall s \in \mathbb { S } \}$ and $\begin{array} { r } { \dot { \boldsymbol { \mathcal { L } } } ( \mathbf { Z } ( t ) ) \triangleq \frac { 1 } { 2 } \dot { \psi _ { Z } } \sum _ { s = 1 } ^ { M } Z _ { s } ( t ) ^ { 2 } } \end{array}$ denote the concatenated vector of all virtual queues and the Lyapunov function of $\mathbf { Z } ( t )$ , respectively. Using similar derivations with $\mathbf { Q } ( t )$ , we obtain the upper bound of $ { \mathcal { L } } (  { \mathbf { Z } } ( t ) )$ as

$$
\begin{array} { r l } & { \mathbb { E } \left[ \mathcal { L } ( \mathbf { Z } ( t + 1 ) ) - \mathcal { L } ( \mathbf { Z } ( t ) ) | \Theta ( t ) \right] } \\ & { \leq \frac { 1 } { 2 } \psi _ { Z } \displaystyle \sum _ { s = 1 } ^ { M } \mathbb { E } \left[ P _ { s } ( t ) ^ { 2 } + ( P _ { s } ^ { \mathrm { t h } } ) ^ { 2 } - 2 P _ { s } ^ { \mathrm { t h } } P _ { s } ( t ) | \Theta ( t ) \right] } \\ & { \qquad + \psi _ { Z } \displaystyle \sum _ { s = 1 } ^ { M } \mathbb { E } \left[ Z _ { s } ( t ) \left( P _ { s } ( t ) - P _ { s } ^ { \mathrm { t h } } \right) | \Theta ( t ) \right] } \\ & { = B _ { 2 } + \psi _ { Z } \displaystyle \sum _ { s = 1 } ^ { M } \mathbb { E } \left[ Z _ { s } ( t ) \left( P _ { s } ( t ) - P _ { s } ^ { \mathrm { t h } } \right) | \Theta ( t ) \right] } \end{array}\tag{27}
$$

Since the maximum propulsion power consumption of the UAV is bounded, $B _ { 2 }$ also has an upper bound.

To proceed, let $\tilde { R } _ { i } ( t ) = \mathrm { m i n } \left\{ Q _ { i } ( t ) + A _ { i } ( t ) , R _ { i } ( t ) \right\}$ , and we can rewrite the queue evolvement equation (7) as $Q _ { i } ( t +$ $1 ) = Q _ { i } ( t ) + A _ { i } ( t ) - \tilde { R } _ { i } ( t )$ With the definition of $\tilde { R } _ { i } ( t )$ the average MOS in (11) can be written as $\mathrm { M O S } _ { \mathrm { s y s } } ( t { \mathrm { ~ + ~ } }$ $\begin{array} { r l r } { \mathrm { 1 ) } } & { { } = } & { \frac { - C _ { 1 } } { | \mathbb { U } _ { \ast } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \ln \Big ( d _ { 0 } \lambda _ { i } + Q _ { i } ( t ) + A _ { i } ( t ) - \tilde { R } _ { i } ( t ) \Big ) + } \end{array}$ $\begin{array} { r } { \frac { 1 } { | \mathbb { U } _ { t } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \left( \dot { C } _ { 1 } \ln \left( \lambda _ { i } \right) + \mathrm { \dot { C } _ { 2 } } \right) } \end{array}$

Taking conditional expectation given $\Theta ( t )$ yields

$$
\begin{array} { l } { \displaystyle - V \mathbb { E } \left[ \operatorname { M O S } _ { \mathrm { s y s } } ( t + 1 ) | \Theta ( t ) \right] } \\ { = - \frac { V } { | \mathbb { U } _ { t } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \left( C _ { 1 } \ln \left( \lambda _ { i } \right) + C _ { 2 } \right) } \\ { \displaystyle \quad + \frac { V C _ { 1 } } { | \mathbb { U } _ { t } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \mathbb { E } \left[ \ln \left( d _ { 0 } \lambda _ { i } + Q _ { i } ( t ) + A _ { i } ( t ) - \tilde { R } _ { i } ( t ) \right) \Big | \Theta ( t ) \right] } \\ { = { B _ { 3 } + \frac { V C _ { 1 } } { | \mathbb { U } _ { t } ^ { + } | } \sum _ { i \in \mathbb { U } _ { t } ^ { + } } \mathbb { E } \Big [ \ln \left( d _ { 0 } \lambda _ { i } + Q _ { i } ( t ) + A _ { i } ( t ) - \tilde { R } _ { i } ( t ) \right) \Big | \Theta ( t ) \Big ] } } \end{array}\tag{28}
$$

Since $\begin{array} { r l r } { | \mathbb { U } _ { t } ^ { + } | } & { { } \le } & { N } \end{array}$ and $\begin{array} { r l r } { \lambda _ { i } } & { { } < } & { \infty } \end{array}$ , we have $B _ { 3 } \quad \leq$ $\begin{array} { r } { - \frac { V } { N } \sum _ { i \in \mathbb { U } _ { * } ^ { + } } \mathopen { } \mathclose \bgroup \left( \dot { C } _ { 1 } \ln \left( \lambda _ { i } \right) + C _ { 2 } \aftergroup \egroup \right) < \infty . } \end{array}$ To conclude, summing up side by side of (26), (27), and (28) yields (18), where $B \geq B _ { 1 } + B _ { 2 } + B _ { 3 }$

## APPENDIX B PROOF OF THEOREM 2

Proof: We prove the user clustering problem is NP-hard by reducing it to the planar K-means problem [38], [39], which

is a well-known NP-hard problem. To reduce ${ \mathcal { P } } ^ { \prime } ,$ , we first observe that the per-time slot problem is of the form

$$
\begin{array} { r l r } {  { \mathcal { P } ^ { \prime \prime } \colon \operatorname* { m a x } _ { \mathbf { X } _ { t } } \sum _ { i = 1 } ^ { N } \psi _ { i } ^ { t } \times R _ { i } ( t ) } } \\ & { } & { \mathrm { s . t . ~ } ( 1 3 b ) , ( 1 3 c ) , ( 1 3 d ) , ( 1 3 e ) } \end{array}
$$

where $\psi _ { i } ^ { t }$ is proportional to $Q _ { i } ( t ) + A _ { i } ( t )$ , representing the traffic demand of each user. In other words, $\bar { \mathcal { P } ^ { \prime } }$ is equivalent to maximizing a weighted sum of the downlink rate of users, where users with higher demands should achieve a better downlink rate $( \mathcal { P } ^ { \prime \prime } )$

We consider a simplified version of $\mathcal { P } ^ { \prime \prime }$ where the LoS probability is one for all users, and movements of UAV-BSs are without limits (i.e., the UAV-BS can reach the new cluster centroid instantaneously). The downlink rate thus only relates to the communication distance, where the higher the distance, the lower the downlink rate. $\mathcal { P } ^ { \prime \prime }$ is simplified to finding M positions for placing UAVs that minimize the weighted-sum distance from the users to its nearest cluster centroids, i.e.,

$$
\begin{array} { r l r } {  { \mathcal { P } ^ { \prime \prime \prime } : \operatorname* { m i n } _ { { \bf X } _ { t } } \sum _ { i = 1 } ^ { N } \psi _ { i } ^ { t } \times \hat { d } _ { i } ( t ) } } \\ & { } & { \mathrm { s . t . } \ ( 1 3 b ) } \end{array}
$$

$\mathcal { P } ^ { \prime \prime \prime }$ is known as the K-means clustering problem for weighted points [39]. The NP-hardness of this problem can be proved by a reduction from Planar 3-SAT problem [38] or Exact Cover by 3-Sets (X3C) problem [39]. To this end, the per-time slot problem $\mathcal { P } ^ { \prime }$ has been reduced to an NP-hard problem; thus, it is NP-hard. The proof is completed. 

## APPENDIX C PROOF OF THEOREM 3

To begin with, we introduce the following lemma for the feasibility of problem ${ \mathcal P } _ { : }$ , followed by the proof of Theorem 3.

Lemma 1: Suppose the $\omega ( t )$ process is stationary. If problem $\mathcal { P }$ is feasible, then for any $\delta > 0 ,$ , there is an Ï-only policy $\alpha ^ { * } ( t )$ that satisfies constraints (13b)-(13e) for all t, and:

$$
- \mathbb { E } \left[ \mathrm { M O S } _ { \mathrm { s y s } } ( t + 1 ) | \alpha ^ { * } ( t ) , \omega ( t ) \right] \leq - \mathrm { M O S } _ { \mathrm { s y s } } ^ { * } + \delta ,\tag{29}
$$

$$
\mathbb { E } \left[ \left. P _ { s } ( t ) - P _ { s } ^ { \mathrm { t h } } \right| \alpha ^ { * } ( t ) , \omega ( t ) \right] \leq \delta , \forall s \in \mathbb { S }\tag{30}
$$

$$
\mathbb { E } \left[ \left. A _ { i } ^ { t } \right| \alpha ^ { * } ( t ) , \omega ( t ) \right] \leq \mathbb { E } \left[ \left. \tilde { R } _ { i } ^ { t } \right| \alpha ^ { * } ( t ) , \omega ( t ) \right] + \delta , \forall i \in \mathbb { U }\tag{31}
$$

Proof of Lemma 1: Please see [33, Theorem 4.5].

Proof of Theorem 3: Consider an Ï-only polity $\alpha ^ { * } ( t )$ that yields (29)â(29) with a corresponding value $\delta \ > \ 0 .$ . Since the algorithm is independent of the backlog queues $\Theta ( t )$ and produces a C-additive approximation of minimizing the righthand side of (18), we obtain for each time slot:

$$
\begin{array} { r l } {  { \Delta ( \Theta ( t ) ) - V \mathbb { E } [ \mathrm { M O S } _ { \mathrm { s y s } } ( t + 1 ) ] } \quad } & { } \\ & { \leq \hat { B } + C + \psi _ { Q } \sum _ { i = 1 } ^ { N } \mathbb { E } [ Q _ { i } ( t ) ( A _ { i } ( t ) - R _ { i } ( t ) ) ] } \\ & { \quad + \psi _ { Z } \sum _ { s = 1 } ^ { M } \mathbb { E } [ Z _ { s } ( t ) ( P _ { s } ( t ) - P _ { s } ^ { \mathrm { t h } } ) ] - V \mathbb { E } [ \mathrm { M O S } _ { \mathrm { s y s } } ( t + 1 ) ] } \end{array}
$$

$$
\stackrel { \left( \dagger \right) } { \leq } \hat { B } + C + \delta \left( \sum _ { i \in \mathbb { U } } \psi _ { Q } Q _ { i } ( t ) + \sum _ { s \in \mathbb { S } } \psi _ { Z } Z _ { s } ( t ) \right) - V \mathrm { M O S } _ { \mathrm { s y s } } ^ { \ast } ,\tag{32}
$$

where (â ) is obtained by plugging in (29)â(31). Taking $\delta $ 0 in (32) yields $\Delta ( \Theta ( t ) ) - V \mathbb { E } \left[ \operatorname { M O S } _ { \mathrm { s y s } } ( t + 1 ) \right] \leq \hat { B } + C -$ ${ V } \mathrm { M O S } _ { \mathrm { s y s } } ^ { * } .$ . By summing up both sides from t = 0 to $T - 1$ taking iterated expectation and telescoping sums, then diving both sides by TV, we obtain

$$
\begin{array} { r l r } {  { \frac { 1 } { T V } ( \mathbb { E } [ \mathcal { L } ( \Theta ( T ) ) ] - \mathbb { E } [ \mathcal { L } ( \Theta ( 0 ) ) ] ) } } \\ & { } & { \leq \displaystyle \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } [ \mathrm { M O S } _ { \mathrm { s y s } } ( t ) ] + \frac { \hat { B } + C } { V } - \mathrm { M O S } _ { \mathrm { s y s } } ^ { * } . } \end{array}\tag{33}
$$

Taking the limit on both sides of (33) when $T \to \infty$ and neglecting non-negative terms when appropriate, we obtain $\begin{array} { r } { \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathbb { E } \left[ \mathrm { M O S } _ { \mathrm { s y s } } ( t ) \right] ~ \geq ~ \bar { \mathrm { M O S } } _ { \mathrm { s y s } } ^ { * } ~ - ~ \frac { \hat { B } + C } { V } } \end{array}$ . This concludes the proof of Theorem 3. 

## REFERENCES

[1] W. Jiang, B. Han, M. A. Habibi, and H. D. Schotten, âThe road towards 6G: A comprehensive survey,â IEEE Open J. Commun. Soc., vol. 2, pp. 334â366, 2021.

[2] N. Parvaresh, M. Kulhandjian, H. Kulhandjian, C. DâAmours, and B. Kantarci, âA tutorial on AI-powered 3D deployment of drone base stations: State of the art, applications and challenges,â Veh. Commun., vol. 36, Aug. 2022, Art. no. 100474.

[3] P. Q. Viet and D. Romero, âAerial base station placement: A tutorial introduction,â IEEE Commun. Mag., vol. 60, no. 5, pp. 44â49, May 2022.

[4] V. Friderikos, âAirborne urban microcells with grasping end effectors: A game changer for 6G networks?,â in Proc. IEEE Int. Medit. Conf. Commun. Netw. (MeditCom), Sep. 2021, pp. 336â341.

[5] Y. Liao and V. Friderikos, âMax-min rate deployment optimization for backhaul-limited robotic aerial 6G small cells,â in Proc. IEEE Global Commun. Conf. (GLOBECOM), Dec. 2022, pp. 2963â2968.

[6] Z. Song, X. Qin, Y. Hao, Y. Hao, J. Wang, and X. Sun, âA comprehensive survey on aerial mobile edge computing: Challenges, state-of-the-art, and future directions,â Comput. Commun., vol. 191, pp. 233â256, Jul. 2022.

[7] X. Liu, Y. Liu, and Y. Chen, âReinforcement learning in multiple-UAV networks: Deployment and movement design,â IEEE Trans. Veh. Technol., vol. 68, no. 8, pp. 8036â8049, Aug. 2019.

[8] J. Lyu, Y. Zeng, R. Zhang, and T. J. Lim, âPlacement optimization of UAV-mounted mobile base stations,â IEEE Commun. Lett., vol. 21, no. 3, pp. 604â607, Mar. 2017.

[9] J. Sun and C. Masouros, âDeployment strategies of multiple aerial BSs for user coverage and power efficiency maximization,â IEEE Trans. Commun., vol. 67, no. 4, pp. 2981â2994, Apr. 2019.

[10] C. Zhang, L. Zhang, L. Zhu, T. Zhang, Z. Xiao, and X.- G. Xia, â3D deployment of multiple UAV-mounted base stations for UAV communications,â IEEE Trans. Commun., vol. 69, no. 4, pp. 2473â2488, Apr. 2021.

[11] M. K. Shehzad, A. Ahmad, S. A. Hassan, and H. Jung, âBackhaulaware intelligent positioning of UAVs and association of terrestrial base stations for fronthaul connectivity,â IEEE Trans. Netw. Sci. Eng., vol. 8, no. 4, pp. 2742â2755, Apr. 2021.

[12] X. Zhong, Y. Huo, X. Dong, and Z. Liang, âQoS-compliant 3-D deployment optimization strategy for UAV base stations,â IEEE Syst. J., vol. 15, no. 2, pp. 1795â1803, Jun. 2021.

[13] H. Huang and A. V. Savkin, âDeployment of heterogeneous UAV base stations for optimal quality of coverage,â IEEE Internet Things J., vol. 9, no. 17, pp. 16429â16437, Sep. 2022.

[14] A. V. Savkin et al., âOn-demand deployment of aerial base stations for coverage enhancement in reconfigurable intelligent surface-assisted cellular networks on uneven terrains,â IEEE Commun. Lett., vol. 27, no. 2, pp. 666â670, Feb. 2023.

[15] C.-C. L. Bhola, A.-H. Tsai, and L.-C. Wang, âAdaptive and fair deployment approach to balance offload traffic in multi-UAV cellular networks,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 3724â3738, Mar. 2023.

[16] Z. Wang et al., âAdaptive deployment for UAV-aided communication networks,â IEEE Trans. Wireless Commun., vol. 18, no. 9, pp. 4531â4543, Sep. 2019.

[17] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAVassisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[18] M. Nasr-Azadani, J. Abouei, and K. N. Plataniotis, âSingle{-} and multiagent actor-critic for initial UAVâs deployment and 3-D trajectory design,â IEEE Internet Things J., vol. 9, no. 16, pp. 15372â15389, Aug. 2022.

[19] N. Parvaresh and B. Kantarci, âA continuous actorâcritic deep Qlearning-enabled deployment of UAV base stations: Toward 6G small cells in the skies of smart cities,â IEEE Open J. Commun. Soc., vol. 4, pp. 700â712, 2023.

[20] C. Wang, D. Deng, L. Xu, and W. Wang, âResource scheduling based on deep reinforcement learning in UAV assisted emergency communication networks,â IEEE Trans. Commun., vol. 70, no. 6, pp. 3834â3848, Jun. 2022.

[21] R. Ding, F. Gao, and X. S. Shen, â3D UAV trajectory design and frequency band allocation for energy-efficient and fair communication: A deep reinforcement learning approach,â IEEE Trans. Wireless Commun., vol. 19, no. 12, pp. 7796â7809, Dec. 2020.

[22] T. Hossfeld, A. Seufert, F. Loh, S. Wunderer, and J. Davies, âIndustrial user experience index vs. Quality of experience models,â IEEE Commun. Mag., vol. 61, no. 1, pp. 98â104, Jan. 2023.

[23] M. Fiedler, T. Hossfeld, and P. Tran-Gia, âA generic quantitative relationship between quality of experience and quality of service,â IEEE Netw., vol. 24, no. 2, pp. 36â41, Mar. 2010.

[24] P. Reichl, B. Tuffin, and R. Schatz, âLogarithmic laws in service quality perception: Where microeconomics meets psychophysics and quality of experience,â Telecommun. Syst., vol. 52, pp. 587â600, Feb. 2013.

[25] Y. Peng, Y. Liu, and H. Zhang, âDeep reinforcement learning based path planning for UAV-assisted edge computing networks,â in Proc. IEEE Wireless Commun. Netw. Conf. (WCNC), Mar. 2021, pp. 1â6.

[26] X. Li, L. Huang, H. Wang, S. Bi, and Y.-J.-A. Zhang, âAn integrated optimization-learning framework for online combinatorial computation offloading in MEC networks,â IEEE Wireless Commun., vol. 29, no. 1, pp. 170â177, Feb. 2022.

[27] L. T. Hoang, C. T. Nguyen, and A. T. Pham, âDeep reinforcement learning-based online resource management for UAV-assisted edge computing with dual connectivity,â IEEE/ACM Trans. Netw., vol. 31, no. 6, pp. 2761â2776, Dec. 2023.

[28] T. Camp, J. Boleng, and V. Davies, âA survey of mobility models for ad hoc network research,â Wireless Commun. Mobile Comput., vol. 2, no. 5, pp. 483â502, 2002.

[29] M. Marvi, A. Aijaz, and M. Khurram, âOn the use of ON/OFF traffic models for spatio-temporal analysis of wireless networks,â IEEE Commun. Lett., vol. 23, no. 7, pp. 1219â1222, Jul. 2019.

[30] M. Marvi, A. Aijaz, and M. Khurram, âIntegrating stochastic geometry and on/off traffic models: Toward spatio-temporal analysis of wireless networks with heterogeneous services,â IEEE Trans. Netw. Sci. Eng., vol. 9, no. 3, pp. 1668â1679, May 2022.

[31] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[32] M. M. Azari, F. Rosas, K. Chen, and S. Pollin, âUltra reliable UAV communication using altitude and cooperation diversity,â IEEE Trans. Commun., vol. 66, no. 1, pp. 330â344, Jan. 2018.

[33] M. J. Neely, Stochastic Network Optimization With Application To Communication and Queueing Systems. San Rafael, CA, USA: Morgan & Claypool, 2010.

[34] Estimating End-to-end Performance in IP Networks for Data Applications, Standard ITU-T G.1030, Feb. 2014.

[35] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[36] D. P. Kingma and J. Ba, âAdam: A method for stochastic optimization,â 2014, arXiv:1412.6980.

[37] R. Jain, D. Chiu, and W. Hawe, âA quantitative measure of fairness and discrimination for resource allocation in shared computer systems,â DEC, Res. Rep. TR-301, Sep. 1984.

[38] M. Mahajan, P. Nimbhorkara, and K. Varadarajan, âThe planar K-means problem is NP-hard,â Theor. Comput. Sci., vol. 442, pp. 13â21, Jul. 2012.

[39] A. Vattani. (2010). The Hardness of K-means Clustering in the Plane. [Online]. Available: https://api.semanticscholar.org/CorpusID:8497124

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_2.png|page_4_img_2]]
3. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_3.jpeg|page_4_img_3]]
4. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_4.png|page_4_img_4]]
5. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_5.png|page_4_img_5]]
6. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_6.png|page_4_img_6]]
7. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_7.png|page_4_img_7]]
8. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_8.png|page_4_img_8]]
9. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_9.png|page_4_img_9]]
10. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_10.png|page_4_img_10]]
11. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_11.png|page_4_img_11]]
12. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_12.jpeg|page_4_img_12]]
13. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_13.jpeg|page_4_img_13]]
14. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_14.png|page_4_img_14]]
15. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_15.jpeg|page_4_img_15]]
16. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_16.png|page_4_img_16]]
17. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_4_img_17.png|page_4_img_17]]
18. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_6_img_1.png|page_6_img_1]]
19. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_1.jpeg|page_8_img_1]]
20. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_2.png|page_8_img_2]]
21. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_3.jpeg|page_8_img_3]]
22. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_4.png|page_8_img_4]]
23. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_5.png|page_8_img_5]]
24. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_6.png|page_8_img_6]]
25. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_7.png|page_8_img_7]]
26. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_8.png|page_8_img_8]]
27. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_9.png|page_8_img_9]]
28. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_10.png|page_8_img_10]]
29. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_11.png|page_8_img_11]]
30. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_12.png|page_8_img_12]]
31. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_13.png|page_8_img_13]]
32. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_14.png|page_8_img_14]]
33. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_15.png|page_8_img_15]]
34. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_8_img_16.png|page_8_img_16]]
35. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_12_img_1.png|page_12_img_1]]
36. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_13_img_1.jpeg|page_13_img_1]]
37. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_13_img_2.jpeg|page_13_img_2]]
38. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_13_img_3.jpeg|page_13_img_3]]
39. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_14_img_1.jpeg|page_14_img_1]]
40. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_14_img_2.jpeg|page_14_img_2]]
41. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_14_img_3.jpeg|page_14_img_3]]
42. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_14_img_4.jpeg|page_14_img_4]]
43. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_14_img_5.jpeg|page_14_img_5]]
44. [[../extracted_images/Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning/page_14_img_6.jpeg|page_14_img_6]]

---

