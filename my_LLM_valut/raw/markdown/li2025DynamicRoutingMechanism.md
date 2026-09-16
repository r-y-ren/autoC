# Dynamic Routing Mechanism for Load Distribution in UAV Swarm Networks With Edge Caching

Qun Li , Student Member, IEEE, Zunliang Wang , Student Member, IEEE, Haipeng Yao , Senior Member, IEEE, Tianle Mai , Member, IEEE, Zhipei Li , and Mohsen Guizani , Fellow, IEEE

AbstractâThe rapid advancement of the UAV swarm network has made its widespread application across a multitude of domains. However, the inherently dynamic nature of the network often gives rise to intermittent connectivity issues, leading to a significant reduction in data transmission capacity. To address this challenge, this study explores the integration of Information-centric Network (ICN) with the delay-tolerant network (DTN). This design aims to enhance message delivery rates by caching content data packets in UAV nodes. Building upon this architecture, we study the congestion control and load balancing problem. We design an on-demand collaborative communication routing algorithm. In our design, we first propose a routing decision model that incorporates multiple routing metrics to capture the dynamic evolution patterns of network nodes, effectively controlling local congestion issues. Subsequently, we employ Lyapunov optimization techniques to achieve network load balancing. By integrating the Lyapunov drift function, we ensure the stability of the feasible solution space within the model. Additionally, considering the high communication overhead caused by the sparse communication characteristics of DTN, we deploy a Multi-Agent Incentivized Communication (MAIC) algorithm to optimize routing scheduling strategies. Within the MAIC framework, each agent develops unique models for its teammates to generate customized information and minimize network information redundancy. Simulation results demonstrate that this algorithm effectively ensures congestion control and load balancing within the UAV swarm network while maintaining communication overhead in routing computations at a minimal level.

Index TermsâDelay tolerant network, lyapunov optimization, on-demand communication, information-centric network, UAV swarm.

## I. INTRODUCTION

I N THE past few decades, the development of UAV net-works has been rapid. According to the 2021 report from works has been rapid. According to the 2021 report from

Fortune Business Insights, the market value of commercial UAVs is estimated to exceed 8.5 billion by 2027. From single \$UAV to the formation of UAV swarm networks, the concept of Flying Ad-Hoc Network (FANET) has emerged. FANET is characterized by high-speed mobility, on-the-fly networking, and automated management, this renders it widely applicable in military operations, disaster detection, and other contexts [1]. However, owing to the rapid dynamics inherent in UAV swarm networks, the network topology of the UAV network is unstable, constantly changing with the nodesâ positions and relative locations. As a result, it cannot form continuous transmission links like fixed network, leading to a significant decrease in data packet transmission efficiency.

To address the issues above, Delay Tolerant Network (DTN), with its storage, carry, and forward features, can effectively operate in UAV swarm that lack continuous network connectivity. Specifically, DTN is an end-to-end communication network architecture that is well-suited for environments characterized by time-varying complexity, elevated error rates, and high latency [2]. In particular, the edge caching strategy of the information-centric network (ICN) is introduced into the delay-tolerant network (DTN). By caching content data packets at specific nodes in the network and using interest packets to locate the nodes storing these content data packets, the âmessage inflationâ (DTN will perform redundant replication of messages to increase the success rate of transmission during data transmission.) problem in DTN can be effectively alleviated. This method further improves the retransmission efficiency and reduces network delay. More specifically, they share common characteristics and synergies, including data transmission mechanisms and data packet storage capabilities for loop prevention. DTN focuses on data persistence and interruption tolerance, while the content-oriented edge caching strategy in the ICN system aims to reduce latency, enhance reliability, and improve overall network performance [3]. Therefore, the introduction of edge caching strategy in DTN architecture has gradually become an effective communication method in future UAV swarm networks.

In recent years, the design of efficient routing algorithms under the DTN architecture has attracted extensive attention in the academic community. In [3], Duarte et al. developed a novel routing protocol, termed PIFP (Probabilistic Interest Forwarding Protocol), which leverages the converged architecture to estimate the probability of information exchange between nodes. In [4], Lu et al. designed a content retrieval scheme based on social relationships to support delay-tolerant MANETs. In [5],

Digital Object Identifier 10.1109/TMC.2025.3589569

Li employed an SDN architecture to substantially enhance DTN data delivery performance and enable efficient processing through centralized control. In [6], Cong proposed a LEO satellite network routing model-based on auction game, using the auction model to use space propagation loss, node remaining storage space, and hop count as a critical criterion for route determination. However, the existing literature aims to transmit data packets efficiently. Due to the size, weight, and power (SWAP) limitations of UAVs, each node is subject to capacity and queue length constraints during the data transmission process. This easily leads to unbalanced loads, causing insufficient processing capabilities at some nodes, resulting in data backlogs and delays, which significantly affect overall network performance.

To solve this problem, we deploy a DTN architecture in the UAV cluster network and combined it with the content-oriented edge caching strategy of ICN. Content data with high request frequency is cached at network nodes, and the nodes storing the content are quickly located through interest packets. This approach improves the overall performance and robustness of the network, reduces dependence on the source server, enhances the likelihood of successful message delivery, and reduces network latency. On this basis, we propose an on-demand collaborative communication routing algorithm (LAMAIC). In this algorithm, we consider social centrality, relationship strength, connection strength, and the remaining cache space of nodes to form a comprehensive selection index to avoid local congestion problems caused by a single measurement index. Then, we utilize Lyapunov techniques to construct a model of UAV network node queues, incorporating the Lyapunov drift to ensure that the feasible solution space of the model is stable. Considering the sparse communication in the UAV swarm network, traditional optimization algorithms can impose an excessive communication burden. In this paper, we leverage the Multi-Agent Incentive Communication (MAIC) algorithm to optimize routing scheduling policies. Within the MAIC framework, each agent constructs distinct models for its different teammates, generates customized information, and reduces information redundancy. Based on this, the LAMAIC can achieve congestion control and load balancing in the UAV swarm network, while maintaining low communication overhead in routing computation. Our simulation outcomes demonstrate that the LAMAIC algorithm attains optimal performance across a range of UAV swarm sizes. The main contributions of this work include:

1) We propose an edge caching mechanism within the DTN architecture, integrating features of DTN and ICN. By storing data packets in distributed UAV nodes, this architecture effectively retrieves and transmits information, enhancing network resilience against unstable connections and significant delays in UAV swarm. Additionally, it addresses issues such as âmessage inflationâ to improve data packet transmission rates.

2) We present an on-demand collaborative communication routing algorithm (LAMAIC) specifically crafted to ensure congestion control and load balancing in the UAV swarm network. First, this algorithm utilizes Lyapunov techniques to construct a model of UAV network node queues, incorporating the Lyapunov drift to characterize network load balancing and prevent network mutations (e.g., excessive queues at any single node). Furthermore, the algorithm leverages the MAIC algorithm to optimize routing scheduling policies. Within the MAIC framework, each agent constructs distinct models for its different teammates, generates customized information, and reduces information redundancy.

3) We perform a comprehensive theoretical analysis to assess the efficacy and benefits of the LAMAIC algorithm within network environments. Extensive simulation outcomes reveal that our LAMAIC scheme outperforms existing benchmarks, delivering enhanced performance in network delay, delivery rate, and load balancing.

This paper adopts the following organizational structure: Section II reviews prior research on DTN methodologies and Lyapunov-based optimization approaches. The architectural framework integrating UAV swarm with DTN routing mechanisms is presented in Section III. Section IV formally establishes the constrained optimization formulation, succeeded by Section V detailing the Lyapunov-driven adaptive routing protocol. Comprehensive performance evaluations are conducted in Section VI, culminating in concluding remarks and future directions in Section VII.

## II. RELATED WORK

Recently, there has been a substantial number of publications about DTN. In [7], Sobin et al. conducted a comprehensive survey of DTN and discussed future research challenges. Next, we will briefly discuss related work from existing solutions and Lyapunov optimization methods in the DTN scenario.

## A. DTN-Based Routing Algorithm

Currently, there are many designs of routing algorithms in DTN networks. They can be broadly classified into opportunistic routing and social-based routing. For opportunistic routing, in [8], Leguay et al. established a Euclidean virtual space to complete routing decisions by forwarding packets to relay nodes with mobility patterns similar to those of the destination node. In [9], Chen proposed a probability-based forwarding scheme, inserting a probability into the algorithm. When a node detects another node with an elevated probability metric, it initiates the transmission of a data packet. Geography-based routing methods in opportunistic networks have also attracted widespread attention. In [10] and [11], Peng et al. developed a communication scheme incorporating UAV kinematic states (trajectory, positioning, and mobility patterns). As for the social routing algorithm, in [12], Gao et al. based on the social centrality metric, which simultaneously considered mobile usersâ social contact patterns and interests to ensure effective relay selection. In [13], Bulut et al. introduced the node relationship quality. This criterion enables nodal communities to emerge through the identification of strongly connected social graphs, where community membership requires multi-hop intimacy verification, consequently driving the development of socially cognizant packet forwarding strategies. In addition, some routing is based on intelligent algorithms. In [14], Wang et al. used ant colony optimization algorithm. During message transmission, pheromones are utilized to select relay nodes, improving the likelihood of successful message transmission and alleviating network congestion. In [15], Xia et al. implemented an artificial bee colony optimization approach for enhanced route selection, explicitly integrating node social relationships and vehicular interaction patterns from the transportation social graph. In [16], Han Established a federated multi-agent decision-making architecture employing decentralized partially observable Markov processes, where next-hop reliability assurance is conceptualized as a distributed optimal control problem, with routing policies emerging from hybrid learning paradigms combining global experience pooling and localized policy deployment. In addition, research on the combination of DTN and ICN. In [17], Hayamizu et al. applies CCN technology in DTN environments to achieve efficient content retrieval, proposing corresponding protocols and methods. In [18], Monticelli et al. targets disaster management scenarios by introducing a delay-tolerant informationcentric network (DID), which addresses long and variable delays through the separation of interest and data transmission paths. In [19], Islam et al. designs a BP-based CIDOR architecture that combines CCNâs content retrieval advantages with DTNâs delay tolerance and opportunistic communication features, enabling efficient content distribution and retrieval in sparse networks. In [20], Anastasiades et al. proposes an application module called ACR, which provides information-centric functionality for DTNs without modifying ICN message processing, and can be combined with multi-hop routing to adapt to varying node densities.

## B. Network Control Based on Lyapunov Optimization

Recently, Lyapunov applications have achieved remarkable results in network optimization. In [21], Gong et al. considered using Lyapunov to establish a virtual queue to represent node energy consumption in a dynamic network environment to solve the problem of computational offloading. They introduced the MAPPO algorithm, a multi-agent proximal strategy optimization scheme guided by Lyapunov principles, to effectively tackle challenges in task scheduling, and resource allocation. In [22], Bi et al. employed Lyapunov optimization in conjunction with Deep Reinforcement Learning (DRL) to simplify multi-stage stochastic MILP into deterministic MILP sub-problems. In [23], Qiu et al. focused on optimizing network data processing capabilities while ensuring stability in data queues and conforming to average power restrictions in addressing the offloading challenge. The author utilized virtual queues in conjunction with Lyapunov optimization principles to transform the problem of long-term average optimization into one of minimizing drift plus penalty, thus simplifying the optimization problem. In [24], in environments where link delays are highly variable, the routing control problem is addressed using a Lyapunov optimization framework. By incorporating a reinforcement learning algorithm with a Markov arrival process for network traffic modeling, this approach effectively lowers the upper bound of the Lyapunov drift, thereby enhancing the stability of queues within the network system. In [25], Wu et al. used Lyapunov optimization technology to build a virtual queue to solve the computing offloading problem. The issue of adhering to task deadlines was reformulated as a congestion control problem associated with the virtual queue, which led to reduced network latency. In [26], Asheralieva and Niyato address the issue of wireless channel allocation. They utilized Lyapunov optimization to derive an upper bound for the total queue backlog to enhance average revenue and maintain stability in the queuing system. The experimental findings demonstrated the feasibility of attaining sustainable revenue optimization through balanced congestion equilibrium maintenance in queuing systems. In [27], Han et al. uses Lyapunov drift theory for IGW selection and vehicle packet forwarding, proving network stability and capacity. In [28], Liu et al. develops a feasible UAV computation offloading strategy using Lyapunov optimization to manage migration cost under dynamic conditions. In [29], Kim et al. Introduces a stochastic control framework employing Lyapunov drift analysis to optimize trajectory diversity in UAV communication networks, establishing fundamental energy-versus-reliability constraints. In [30], Kumar et al. presents a Lyapunov-based multi-agent DDPG approach for optimal resource allocation in mobile IoV, jointly minimizing energy consumption and delay. In [31], Qiu et al. solves resource allocation problem through the Liyapunov optimization algorithm based on context immersive learning. In [32] Tian aims at the routing and scheduling problems in interstellar networks, and uses Lyapunov optimization to transmit interstellar data transmission in a distributed manner, and experiments have proved that this method can reasonably adjust the average end-to-end delay and transmission success rate. trade-off relationship.

## III. SYSTEM MODEL

This section first introduces the network model and the UAV system model, followed by the conditions necessary to achieve network load balancing. Second, the integrated routing decision model in DTN is presented.

## A. System Model

In Fig. 1, we demonstrate the integration of the edge caching strategy in ICN with the DTN architecture, deployed in the UAV cluster network. In this architecture, each UAV is equipped with a queuing model, caching space, and a hash storage table. The UAV swarm is clustered into $\mathcal { K } = [ 1 , 2 , . . . K _ { k } ]$ clusters based = [1 2 ]on the centrality of each node, this will be described in detail in the clustering algorithm section. The nodes within the cluster inform each other of their cache contents and map them into the nodeâs hash table. Network service delivery is implemented through optimal aerial node selection, where user-associated data payloads are routed to geographically proximal UAVs. We consider the UAV swarm to consist of a set of UAV, denoted as N . Thus, it is denoted as $\mathbb { N } = [ 1 , 2 , . . . N _ { n } ]$ , the communication = [1 2links between UAVs are represented as $\mathcal { L } = [ l _ { 1 } , l _ { 2 } , . . . L _ { f } ] .$ , and = [the maximum bandwidth of communication link $u v \in { \mathcal { L } }$ is bw uv . Each UAV caches a portion of the content data packets $\mathcal { D } = [ 1 , 2 , . . . D _ { d } ]$ . The interest packets correspond to each content data packet $\mathbf { \bar { \mathcal { I } } } = [ 1 , 2 , . . . I _ { i } ]$ . We define $X _ { n } ^ { d }$ to represent a = [1 2 ]UAV node n caching data packet d. Define a hash table to maintain node cache information within the cluster. In the scenario, we assume that requests for data packets appear periodically. When users have a request, interest packet i is first generated, and the corresponding content data packet d is searched for in the UAV swarm network. When the corresponding content data packet is found, it is routed to the UAV node n near the user using the DTN forwarding mechanism. We model a time slot model in which the total duration is divided into T equal intervals, each represented by Ï0. This segmentation can be denoted as $\mathcal { T } = \{ 1 , 2 , . . . t , . . . , T \}$ . Within each of these intervals, there are several packet requests, as indicated by the variable num.

<!-- image-->  
Fig. 1. UAV swarm network system model.

1) UAV Swarm Network Model: The UAV swarm networkâs structure is represented as an undirected graph $G = ( \mathcal { N } , \mathcal { L } )$ , where $( u , v ) \in \mathcal { N }$ = ( )represents any two adjacent UAV nodes. The ( )communication links between UAV nodes are represented by uv â L, and we consider that a communication link is established when the distance between UAVs is less than communication range C. Each UAV has a three-dimensional position and velocity:

$$
\begin{array} { r } { \{ P _ { x y z } ^ { n } = ( p _ { x } ^ { n } ( t ) , p _ { y } ^ { n } ( t ) , p _ { z } ^ { n } ( t ) ) } \\ { V _ { x y z } ^ { n } = ( v _ { x } ^ { n } ( t ) , v _ { y } ^ { n } ( t ) , v _ { z } ^ { n } ( t ) ) } \end{array} ,\tag{1}
$$

where $p _ { x } ^ { n } ( t ) , p _ { y } ^ { n } ( t ) , p _ { z } ^ { n } ( t )$ represents the position of UAV n in the ( ) ( ) ( )3-dimensional coordinate system. $v _ { x } ^ { n } ( t ) , v _ { y } ^ { n } ( t ) , v _ { z } ^ { n } ( t )$ represents the velocity of UAV node n in the $x , y , z$ ( ) (direction.

2) Gaussian Markov Mobility Model: To accurately model the dynamic topological variations in UAV formations and quantify DTN performance indicators, we refer to the open source code in [33] to simulate our UAV swarm network. we use a 3-D smooth mobility model, which exhibits correlations in the x, y, z direction. Before selecting a new maneuvering plane and rotation center, the UAV maintains a hover state around a randomly chosen turning center on the maneuvering plane for a predetermined duration. The new center of rotation is positioned on a plane that is perpendicular to the UAVâs current trajectory, facilitating smoother transitions during turns. Within the maneuvering plane, the tangential and normal acceleration components are characterized [26]:

$$
\begin{array} { r } { a _ { t } ( t ) = D ( t ) - g \sin \left( \alpha ( t ) \right) } \\ { a _ { n } ( t ) = L ( t ) \cdot \sin \left( \beta ( t ) \right) . } \end{array}\tag{2}
$$

The new rotation centerâs position is determined by selecting a specific turning radius, denoted as $R [ T _ { i } ]$ , and the corresponding height of the center $c _ { z } [ T _ { i } ]$ [ ]. The calculation of the turning center $p _ { c } [ T _ { i } ]$ is given by the following equation:

$$
\begin{array} { r } { v [ T _ { i } ] \cdot ( p _ { c } [ T _ { i } ] - p [ T _ { i } ] ) = 0 } \\ { | | p _ { c } [ T _ { i } ] - p [ T _ { i } ] | | = R [ T _ { i } ] , } \end{array}\tag{3}
$$

where $p [ T _ { i } ]$ and $v [ T _ { i } ]$ respectively denote the spatial coordinates [ ] [ ]and kinematic vectors. The height $c _ { z } [ T _ { i } ]$ formula of the new turning center is as follows:

$$
p _ { z } \left[ T _ { i } \right] - K \leqslant c _ { z } \left[ T _ { i } \right] \leqslant p _ { z } \left[ T _ { i } \right] + K ,\tag{4}
$$

where $\begin{array} { r } { K = \frac { R [ T _ { i } ] \sqrt { V ^ { 2 } [ T _ { i } ] - v _ { z } ^ { 2 } [ T _ { i } ] } } { V [ T _ { i } ] } } \end{array}$ . The velocity update of UAV =nodes follows a Gaussian Markov mobility model:

$$
\begin{array} { r l r } & { } & { V _ { x y z } ^ { n } ( t ) = \alpha \cdot V _ { x y z } ^ { n } ( t - 1 ) + ( 1 - \alpha ) } \\ & { } & \\ & { } & { \cdot \mu + \sigma \cdot \Big ( \sqrt { 1 - a ^ { 2 } } \Big ) w _ { n - 1 } , } \end{array}\tag{5}
$$

where $\mu$ and Ï represent the mean and variance of the velocity, respectively. $V _ { x y z } ^ { n }$ denotes the velocity of the $\mathrm { U A V } , w _ { n - 1 }$ follows an uncorrelated Gaussian process, and Î± is the correlation factor.

3) UAV Swarm Cache Model: Due to the limited buffer space in UAV nodes, when the buffer space is full, nodes cannot provide service, which may even lead to network congestion. Therefore, optimal relay node selection must incorporate realtime buffer occupancy evaluations during packet forwarding operations. The cache space utilization of node n is defined as:

$$
u t i l _ { n } = \frac { M A X _ { m e m } - R E S _ { m e m } } { M A X _ { m e m } } ,\tag{6}
$$

where $M A X _ { m e m }$ represents the total cache space size, and $R E S _ { m e m }$ represents the remaining cache space size.

In the case of caching partial content data packets in the nodes of the UAV swarm, it is constrained that the cache size should not exceed the maximum cache space. Therefore, the constraint is defined as:

$$
B _ { i } \cdot X _ { k _ { n ^ { \prime } } } ^ { d _ { i } } \leqslant M A X _ { m e m } ,\tag{7}
$$

where $B _ { i }$ represents the size of the i data packet. $X _ { k _ { n ^ { \prime } } } ^ { d _ { i } }$ indicates that in the kth cluster, if the $n ^ { \prime } { \mathrm { t h } }$ node caches data packet $d _ { i }$ , the value is 1. For network transmission links, the amount of data transmitted should be less than the maximum bandwidth of the link. The formula is described as follows:

$$
\sum _ { d } X _ { u v } ^ { d } ( t ) \cdot s i z e ( d ) \leqslant b w ( u v ) ,\tag{8}
$$

At time t,the cumulative payload volume of transmitted packets is subject to bandwidth limitations. Here, size d defines the size of packet $d ,$ and $X _ { u v } ^ { d } ( t )$ captures the routing state of packet d ( )through link uv, with the left-hand term representing the per-slot link throughput intensity. And bw uv represents the maximum ( )bandwidth of the current transmission queue.

4) Content Popularity: Cached Data Selection depends on both cache space availability and content popularity: When Cache Space is Available: Any data can be cached without restrictions when the cache buffer has space. When Cache Space is Full: Data selection becomes increasingly discerning, with popular content given priority, and popularity is assessed based on both the frequency and the recency of content requests, using the formula:

$$
P _ { i } = \sum _ { k = 1 } ^ { n } F \left( t _ { b a s e } - t _ { k } \right) ,
$$

where $\begin{array} { r } { F ( x ) = ( \frac { 1 } { 2 } ) ^ { \lambda x } } \end{array}$ functions as the weighting mechanism, $t _ { k }$ ( ) = ( )indicates the arrival time of previous content requests, $t _ { b a s e }$ denotes the current time, and $x = t _ { b a s e } - t _ { k }$ represents the elapsed time between a requestâs arrival and the current moment. It is used to measure the freshness of the requests, so as to calculate the content popularity by comprehensively considering the frequency and freshness, and Î» is a parameter that controls the balance between frequency and freshness. When Î» is closer to 0, frequency has more weight; when it approaches 1, freshness is more important. Based on this, more popular content is cached first. Based on this formula, the content cache in the UAV changes dynamically.

5) UAV Queueing Model: For each node in the network, in addition to the caching model of the UAV, it is crucial to track the lifecycle of data packets due to their delivery deadlines (TTL). Additionally, by constructing a queue model for data packet transmission at each node, the queue stability of the entire cluster network can be effectively monitored and analyzed. We partition a workload queue for each UAV node to store packets waiting for transmission.

Tasks generated at each node are processed through corresponding queues following a first-in-first-out scheduling discipline. By employing this queueing model, we establish the Lyapunov drift function that transforms queue delays into queue length metrics, thereby reformulating the network load distribution problem as a queue stability optimization challenge. Our proposed scheduling strategy aims to regulate waiting times by limiting queue lengths, and the propagation delay in each link is assumed to be negligible [34]. For a data packet forwarding queue with destination d at node n, its queue model is modeled as follows:

$$
\mu _ { n , d } ^ { b } ( t ) = \sum _ { b \epsilon \mathcal { N } } \mu _ { n , b , d } ( t ) ,\tag{9}
$$

where $\mu _ { n , d } ^ { b } ( t )$ represents the service rate of a data packet with ( )destination d being transmitted from node n to node b.

$$
\lambda _ { n , d } ^ { a } ( t ) = \sum _ { a \epsilon \mathcal { N } } \lambda _ { a , n , d } ( t ) ,\tag{10}
$$

where $\lambda _ { n , d } ^ { a } ( t )$ represents the arrival rate of a packet from UAV ( )a to UAV n with destination d.

The dynamic backlog variation $Q _ { n , d } ( t + 1 )$ of the entire queue is defined as follows:

$$
Q _ { n , d } ( t + 1 ) = Q _ { n , d } ( t ) + A _ { n , d } ( t + 1 ) + \lambda _ { n , d } ^ { a } ( t ) - \mu _ { n , d } ^ { d } ( t ) ,\tag{)(11}
$$

where $Q _ { n , d } ( t )$ represents the backlog queue size from UAV n ( )to destination UAV d at time slot t.

The above expression represents the overall dynamic queue situation of node n, where the backlog $Q _ { n , d } ( t + 1 )$ at time $t + 1$ is equal to the sum of the backlog $Q _ { n , d } ( t )$ ( + 1) + 1at time t and the newly arrived data packet $A _ { n , d } ( t + 1 )$ at time $t + 1 . \lambda _ { n , d } ^ { a } ( t ) - \mu _ { n , d } ^ { b } ( t )$ represents the difference between the arrival rate and the service rate.

Definition 1. (strongly stable): A strongly stable queue satisfies [35]:

$$
\operatorname* { l i m } _ { T \to \infty } { \frac { 1 } { t } } \sum _ { t = 0 } ^ { T - 1 } \operatorname { E } \left[ Q ( t ) \right] < \infty ,\tag{12}
$$

where $Q ( t )$ represents the queue length at time t. If all the queues $Q _ { n } ( t ) , \forall n \in \mathcal { N }$ in the network satisfy the strong stability

Algorithm 1: Clustering Algorithm.   
Input: Global centrality of each UAV Cnglobal.   
Output: Divide the UAV swarm into K clusters.   
1: Configure the UAV swarm network environment and   
initialize the parameters of the proposed algorithm.   
2: Execute the Gaussian Markov mobility model and   
calculate $V _ { x y z } ^ { n } ( t )$ according to (5), and the UAV   
positions $P _ { x y z } ^ { n } .$   
3: Calculate centrality according to (13), (14).   
4: for UAV $n \in \{ 1 , 2 , . . . \mathcal { N } \}$ do   
5: 1 2 UAV n broadcast global centrality to neighbors.   
6: if another UAV i receive the global centrality   
information then   
7: Compare with own global centrality $C _ { \mathrm { g l o b a l } } ^ { i } .$   
8: if i has the highest global centrality then   
9: Claim to be a cluster head and form a cluster   
with neighbors.   
10: else   
11: Clustered with neighbors with high centrality.   
12: end if   
13: end if   
14: end for

condition, the entire system queue is considered stable, thereby achieving load balancing control.

## B. DTN Routing Decision Model

In DTN routing model, we adopt the previously constructed mobility model for the UAV swarm and consider its mobility pattern as a social network structure with social attributes within the DTN. social networks may consist of multiple clusters with weak relationships among them, where the source node and all its direct contacts have no direct connection to the destination node. Consequently, relying on a single routing parameter proves insufficient for guaranteeing prompt data delivery. When a network node exhibits elevated metric values, the majority of data packets within the system are attracted to that particular node, resulting in traffic bottlenecks and processing congestion. Therefore, relying on a single routing metric can lead to congestion at certain nodes, resulting in an imbalance in network load. Among the currently available routing metrics, centrality is effective for pathfinding in static networks; however, it fails to accommodate the dynamic nature of link availability. The issue is alleviated by relationship strength, which prioritizes links with a greater probability of being available. Although connection strength assesses links in a time-varying network, it does not completely capture the networkâs overall dynamics. When the underlying network is characterized by a social structure, we propose an integrated routing decision model that combines centrality, relationship strength, and connection strength to dynamically represent the evolution patterns of node social relationships [36], [37]. This approach enables link prediction and mitigates local congestion.

1) Local Centrality (Betweenness Centrality): Betweenness centrality quantifies how frequently a node appears on the shortest routes connecting other nodes in a network. Consequently, a node that appears on a larger number of these shortest paths exhibits a higher betweenness centrality. The betweenness centrality metric for UAV n is mathematically formulated as $C _ { l } ^ { n } .$

$$
C _ { l o c a l } ^ { n } ( p _ { n } ) = \sum _ { u = 1 } ^ { N } \sum _ { v = 1 } ^ { N } \frac { g _ { u v } ( p _ { n } ) } { g _ { u v } } , u \ne v ,\tag{13}
$$

where $u \in \mathcal { N } , v \in \mathcal { N } , p _ { n } \in \mathcal { L } .$ $g _ { u v }$ represent the paths between UAV u and UAV v, and $g _ { u v } ( p _ { n } )$ represents node n in the shortest ( )path between UAV v and UAV u.

2) Global Centrality: Since betweenness centrality only estimates the centrality of a node in its local neighborhood, nodes with high betweenness centrality values can fail to transmit messages to their destination nodes successfully. Therefore, we introduce a global centrality measure of $C _ { g l o b a l } ^ { n }$ on top of betweenness centrality to address this limitation:

$$
C _ { \mathrm { g l o b a l } } ^ { n } = \frac { C _ { \mathrm { l o c a l } } ^ { n } \cdot \sqrt { \Sigma _ { u = 1 } ^ { N } c _ { n u } } } { C _ { \mathrm { l o c a l } } ^ { n } \cdot \sqrt { \Sigma _ { u = 1 } ^ { N } c _ { n u } } + C _ { \mathrm { l o c a l } } ^ { u } \cdot \sqrt { \Sigma _ { n = 1 } ^ { N } c _ { n u } } } ,\tag{14}
$$

where $c _ { n u }$ denotes the frequency with which node n has encountered node u in the past, N denotes the total number of UAVs, and $C _ { l o c a l } ^ { n }$ indicates the local centrality of a node. This local centrality measure quantifies a nodeâs social attributes by counting its connections with all other nodes in the network, thereby enabling more accurate predictions of future interactions.

3) Relationship Strength: The stronger the association between a node in the network and its destination node, the higher the probability of successful data packet transmission [38], so we use relationship strength to measure the degree of association between nodes. The relationship strength between node n and node d is defined as:

$$
C _ { T S } ^ { n d } = \frac { f ( n ) } { F ( n ) - f ( n ) } ,\tag{15}
$$

where $f ( n )$ represents the total number of interactions between ( )node n and node $d ,$ while $F ( n )$ denotes the total number of ( )encounters that node n has with all other nodes.

4) Connection Strength: The connection strength is quantified by counting the number of mutual neighbors shared between the current node n and the destination node d, indicates the probability of successful transmission. The local connection strength $\Psi _ { l o c a l } ^ { n d }$ is defined as:

$$
\Psi _ { l o c a l } ^ { n d } = | F _ { n } ( t ) \cap F _ { d } ( t ) | + 1 ,\tag{16}
$$

where $F _ { n } ( t )$ represents the total number of neighbors of node ( )n at time t, and $F _ { d } ( t )$ represents the total number of neighbors of destination node d at time t. One is added to the values to prevent situations where there are no common neighbors.

5) Integrated Routing Decision Model: By integrating (14), (15) and (16), we have developed a decision model that dynamically captures the social structure characteristics and spatial evolution patterns of the UAV swarm network. This model not only allows for real-time monitoring of current network conditions but also enables the prediction of future connectivity relationships between nodes, thereby enabling proactive routing choices and optimizing network performance.

$$
S y n u t i l _ { n } ( \textit { d } ) = \frac { \alpha \cdot \Psi _ { \mathrm { l o c a l } } ^ { n d } + \beta \cdot C _ { g l o b a l } ^ { n } + \gamma \cdot C _ { T S } ^ { n d } } { u t i l _ { n } } ,\tag{17}
$$

where $\alpha , \beta , \gamma$ represents the weight coefficient of the metric.

## C. Clustering Algorithm

Since interest packets must propagate across the entire UAV network topology to locate corresponding content data packets, direct broadcasting approaches introduce significant network overhead challenges. To mitigate these issues, we initially organize the UAV fleet into clustered formations and distribute packets to adjacent UAV nodes. Following packet reception, each UAV evaluates its centrality metrics relative to neighboring nodes. If a UAV has the highest centrality, it declares itself as the cluster head and forms a cluster with its neighbors. Otherwise, it joins a cluster with neighbors having higher centrality. Within each cluster, nodes broadcast information about the content data packets they have cached to each other. The recipient nodes of these broadcasts map the corresponding UAV nodes and packet types to a hash table data structure $\bar { H a s h } _ { n } ^ { k }$ [39]. Define hash table $H a s h _ { n } ^ { k } = \{ X _ { k _ { n 1 } } ^ { d _ { i } } , X _ { k _ { n 2 } } ^ { d _ { i } } , . . . X _ { k _ { n ^ { \prime } } } ^ { d _ { i } } \}$ to represent the cache =information that member n knows about other members in the k cluster, where $X _ { k _ { n 1 } } ^ { d _ { i } }$ represents the cached data packet $d _ { i }$ of member n in the k cluster with node $n .$ . When the interest 1packet is transmitted in the cluster network, it only needs to be transmitted between clusters. Once the interest packet reaches a UAV in a cluster, the cache information of all UAVs in the current cluster can be retrieved through the hash table. The interest packet can then find the corresponding cache node with the minimum transmission cost. Therefore, using a clustering algorithm avoids the flood search of content data packets; by maintaining the hash table, each slave node in the cluster knows the type of data packets cached by cluster members. The process is shown in Algorithm 1.

## IV. PROBLEM FORMATION

In this section, we outline the optimization goals of the network. Then we derive the Lyapunov optimization function and combine it with the optimization objective in order to maintain the stability of the modelâs feasible solution space.

## A. Objective Equation

Each data packet has an initial lifetime TTL for the queuing delay in the entire network. When the data packet is successfully transmitted, the transmission delay is denoted as $d _ { q u e u e } =$ $T T L - t _ { t o t a l }$ , where $\begin{array} { r } { t _ { t o t a l } = \sum _ { t \in T } \tau _ { 0 } } \end{array}$ represents the number =of time slots the data packet has experienced.

We aim to maximize the success rate of data packet transmission while minimizing network transmission delay, thus improving user quality of service. Based on this, we formulate it as a stochastic optimization problem $P 1$

$$
\begin{array} { c } { { \operatorname* { m i n } \left\{ \bar { E } \right\} = \displaystyle \operatorname* { l i m } _ { T \to \infty } s u p \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } E \left[ \left\{ d e l a y _ { d } - d e l i v e r y _ { d } \right\} \right] } } \\ { { \mathrm { s . t . : } \ ( 7 ) , \ ( 8 ) , \ ( 1 2 ) , } } \end{array}\tag{18}
$$

TABLE I SUMMARY OF NOTATIONS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1> $C _ { l o c a l } ^ { n } ( p _ { n } )$ </td><td rowspan=1 colspan=1>Local centrality of node n</td></tr><tr><td rowspan=1 colspan=1> $C _ { g l o b a l } ^ { n }$ </td><td rowspan=1 colspan=1>Global centrality of node n</td></tr><tr><td rowspan=1 colspan=1> $C _ { T S } ^ { n d }$ </td><td rowspan=1 colspan=1>Strength of the connection betweennodes n and d</td></tr><tr><td rowspan=1 colspan=1> $\Psi _ { l o c a l } ^ { n d }$ </td><td rowspan=1 colspan=1>Relationshipstrengthbetweennodes n and d</td></tr><tr><td rowspan=1 colspan=1> $S y n u t i l _ { n } ( d )$ </td><td rowspan=1 colspan=1>Outing metrics between nodes nand d</td></tr><tr><td rowspan=1 colspan=1> $\mu _ { n , d } ^ { b } ( t )$ </td><td rowspan=1 colspan=1>Service rate of node n</td></tr><tr><td rowspan=1 colspan=1> $\lambda _ { n , d } ^ { a } ( t )$ </td><td rowspan=1 colspan=1>Arrival rate of node n</td></tr><tr><td rowspan=1 colspan=1> $Q _ { n , d } ( t )$ </td><td rowspan=1 colspan=1>Backlog queue size from node n tothe destination node d in time slott</td></tr><tr><td rowspan=1 colspan=1> $\Delta L$ </td><td rowspan=1 colspan=1>Lyapunov function drift term</td></tr><tr><td rowspan=1 colspan=1> $L \left( t \right)$ </td><td rowspan=1 colspan=1>Lyapunov optimization function</td></tr><tr><td rowspan=1 colspan=1> $A _ { n , d } ( t + 1 )$ </td><td rowspan=1 colspan=1>Slot $t + 1$ isfor newly arrivedpackets in destination d node n</td></tr><tr><td rowspan=1 colspan=1> $p _ { x } ^ { n } ( t ) , p _ { y } ^ { n } ( t ) , p _ { z } ^ { n } ( t )$ </td><td rowspan=1 colspan=1>Position of the UAV n in the $x , y , z$ coordinate axis</td></tr></table>

where $\begin{array} { r } { d e l a y _ { d } = \sum _ { \mathfrak { T } } \sum _ { \mathfrak { D } } d _ { q u e u e } } \end{array}$ represents the packet queuing delay. delive $\begin{array} { r } { r y _ { d } = \sum _ { \mathcal { T } } \frac { N _ { d e l i v e r y } } { N _ { t o t a l } } } \end{array}$ represents the delivery rate = of data packets in the network, where $N _ { d e l i v e r y }$ represents the number of successfully transmitted data packets in time slot $\tau _ { 0 }$ and $N _ { t o t a l }$ represents the total number of data packets in time slot $\tau _ { 0 } .$ , as listed in Table I for reference.

The optimization objective simultaneously reduces end-toend latency while improving packet delivery reliability. Equation (7) enforces strict buffer capacity constraints to maintain UAV storage viability. (8) represents the constraint on the transmission bandwidth. (12) imposes the constraint that the entire network queue follows a strongly stable process.

## B. Lyapunov Optimization

We recast the network load balancing problem within the framework of Lyapunov optimization. As per Definition 1, achieving effective load distribution necessitates maintaining strong stability across all network nodes. This optimization problem presents inherent computational difficulties. To resolve this, we adopt the quadratic form of queue backlog magnitude as an instability metric for network systems, formally expressed through the Lyapunov candidate function:

$$
L \left( t \right) = \frac { 1 } { 2 } \sum _ { n = 0 } ^ { \ N - 1 } \sum _ { d = 0 } ^ { N - 1 } Q _ { n , d } ^ { 2 } ( t ) ,\tag{19}
$$

where $L ( t )$ represents a scalar that indicates the overall conges-( )tion of the queue, serving as a measure of workload latency.

The magnitude of this scalar effectively reflects the queueâs status [25].

Next, we define $\Delta L$ as the conditional Lyapunov drift for a Îsingle step, given by:

$$
\begin{array} { r l } { \Delta t \Delta \cdot \left( \mathbf { J } \cdot \mathbf { \Phi } \right) } & { = \displaystyle \frac { 1 } { 2 } \sum _ { k = 0 } ^ { N - 1 } \left( \eta _ { k } ^ { ( 1 ) } - E _ { k } ^ { ( 1 ) } ( t + 1 ) - Q _ { k , k } ^ { ( 2 ) } ( t ) \right) } \\ & { = \displaystyle \frac { 1 } { 2 } \sum _ { k = 0 } ^ { N - 1 } \sum _ { i = 0 } ^ { N - 1 } \left( Q _ { k , i } ^ { ( 2 ) } \alpha _ { k } ^ { ( 1 ) } + 1 \right) - Q _ { k , i } ^ { ( 2 ) } \alpha _ { k } ^ { ( 2 ) } } \\ & { = \displaystyle \frac { 1 } { 2 } \sum _ { k = 0 } ^ { N - 1 } \sum _ { i = 0 } ^ { N - 1 } \left( Q _ { k , i } \alpha _ { k } ^ { ( 1 ) } + \lambda _ { \mathrm { a } , \mathrm { a } } ( t + 1 ) \right) } \\ &  \quad \quad | \mathbf { \Phi } | _ { { \mu } _ { \alpha } } ^ { \mathrm { L } } ( t ) \left( \mathbf { \Phi } \right) \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi } \mathbf { \Phi }  \end{array}
$$

where

$$
+ \left[ \mu _ { n , d } ^ { b } ( t ) \right] ^ { 2 } \biggr ] .\tag{20}
$$

$$
\begin{array} { r l } & { B = \frac { 1 } { 2 } \sum _ { n = 0 } ^ { \mathcal { N } - 1 } \sum _ { d = 0 } ^ { \mathcal { N } - 1 } \bigg [ \Big [ A _ { n , d } ( t + 1 ) + \lambda _ { n , d } ^ { a } ( t ) \Big ] ^ { 2 } } \\ & { \bigg ] . } \end{array}
$$

Taking the expectation on both sides of the above equation at the same time, we get the Lyapunov preliminary boundary:

$$
\begin{array} { l } { \displaystyle E \left[ \Delta L | Q _ { n , d } ( t ) \right] \leqslant \sum _ { n = 0 } ^ { \mathcal { N } - 1 } \sum _ { d = 0 } ^ { \mathcal { N } - 1 } Q _ { n , d } ( t ) \cdot } \\ { \displaystyle E \left[ A _ { n , d } ( t + 1 ) + \lambda _ { n , d } ^ { a } ( t ) - \mu _ { n , d } ^ { b } ( t ) | Q _ { n d } ( t ) \right] . } \end{array}\tag{21}
$$

If the packet traffic in the network is within the load range, the expected value on the right side of $\Delta L$ is negative, that is, assuming $\varepsilon > 0 , E [ A _ { i , j } ( t + 1 ) + \lambda _ { i , j } ^ { a } ( t ) - \mu _ { i , j } ^ { b } ( t ) | Q _ { n d } ( t ) ] < - \varepsilon _ { \mathrm { t } }$

0 [ ( + 1) + ( ) (According to the above formula, $E \big [ \Delta L | Q _ { n d } ( t ) \big ] \leq$ $\begin{array} { r } { B + \sum _ { i = 0 } ^ { n - 1 } \sum _ { i = 0 } ^ { n - 1 } Q _ { n , d } ( t ) \cdot ( - \varepsilon ) \leqslant 0 , } \end{array}$ Î That is, $\begin{array} { r } { \sum _ { n = 0 } ^ { \mathcal { N } - 1 } \sum _ { d = 0 } ^ { \mathcal { N } - 1 } Q _ { n , d } ( t ) \geqslant B \Big / \varepsilon } \end{array}$ shows that when the queue backlog is sufficiently large, the Lyapunov drift $\Delta L$ remains Înon-positive, ensuring asymptotic convergence to equilibrium states.

The main goal of minimizing the Lyapunov drift $\Delta L$ is to reduce fluctuations in the Lyapunov function $L ( t )$ , pushing the ( )queue state towards low congestion and stability. The contraction of queue length metrics below critical thresholds demonstrates the systemâs convergence toward equilibrium [40], Lyapunov drift represents the difference of system queue status between two continuous time slots, and negative drift indicates queue reduction, system stability and congestion relief. Positive drift indicates an increase in queues, suggesting congestion and instability. A queue value of âsmallâ indicates that the system effectively distributes traffic and prevents nodes from being overloaded, thus achieving load balancing, and ensuring the entire UAV swarm system is load-balanced and provides stable network services. Although solely minimizing the drift function can maintain queues at low congestion levels during content packet delivery, it may also undermine transmission success rates. Likewise, a forwarding strategy devoted exclusively to load balancing can induce packets to circulate endlessly among nodes without ever arriving at their destination. To overcome these trade-offs and identify an optimal forwarding policy for delay-tolerant networks, we therefore adopt the drift-pluspenalty framework, which jointly regulates load distribution and enhances overall network performance.

## C. Lyapunov Drift Plus Penalty Function

This optimization process pursues dual objectives: stabilizing network queues through Lyapunov drift reduction while enhancing operational performance via penalty function minimization. Specifically, the mechanism concurrently maintains load distribution equilibrium, optimizes end-to-end latency, and maximizes packet delivery ratio across temporal intervals. In order to find the balanced relationship between them, (18) and (20) are combined into a drift plus penalty function:

$$
\begin{array} { l } { { f = V \cdot P + \Delta L } } \\ { { \displaystyle \quad = d e l a y _ { d } - d e l i v e r y _ { d } } } \\ { { \displaystyle \quad + B + \sum _ { n = 0 } ^ { \mathcal { N } - 1 } \sum _ { d = 0 } ^ { \mathcal { N } - 1 } Q _ { n , d } ( t ) } } \\ { { \displaystyle \qquad \cdot \left[ A _ { n , d } ( t + 1 ) + \lambda _ { n , d } ^ { a } ( t ) - \mu _ { n , d } ^ { b } ( t ) \right] , } } \end{array}\tag{22}
$$

where $V \geqslant 0$ is the weight measuring the âimportanceâ of the penalty.

Transform the optimization problem of P into the following objectives $P 2 \mathrm { : }$

$$
\begin{array} { c } { { \operatorname* { m i n } \{ f \} } } \\ { { { } } } \\ { { s . t . : ( 7 ) , \ ( 8 ) , \ ( 1 2 ) . } } \end{array}\tag{23}
$$

## V. ON-DEMAND COLLABORATION ROUTING ALGORITHM BASED ON LYAPUNOV

This section introduces LAMAIC, an on-demand cooperative routing mechanism grounded in Lyapunov optimization theory. The inter-UAV packet forwarding mechanism is formally modeled as a Markov decision process, with subsequent subsections systematically developing the algorithmic implementation within this framework.

## A. Lyapunov-Based Markov Decision Process

The optimization problem of $P 2$ can be defined Dec-2POMDP. The process is represented by an 8-tuple sequence as $\mathfrak { M } = \langle \ N , \ \mathcal { S } , \mathcal { A } , P , \Omega , O , \mathcal { R } , \gamma \rangle [ 4 1 ]$ , where $\mathcal { N } = [ 1 , 2 , . . . N ]$ de-= Î© = [1 2 ]notes the set of agents, S denotes the global state information, and $\mathcal { A } = [ a _ { 1 } , a _ { 2 } , . . . a _ { N } ]$ represents the action set of all agents, $\Omega = [ o _ { 1 } , o _ { 2 } , . . . o _ { N } ]$ represents a series of observation Î© =spaces [42], $\gamma \in [ 0 , 1 )$ represents the discounted reward, in each time slot $\tau _ { 0 } ,$ [0 1) each agent $n \in \mathcal N$ captures an observation $o _ { n } \in \Omega$ , obtained from the observation function $O ( s , n )$ , where $s \in { \mathcal { S } } .$ . Following this, it chooses an action $a _ { n } \in { \mathcal { A } }$ . The joint actions $\pmb { a } = \langle a _ { 1 } , . . . , a _ { n } \rangle$ then guide the system to the subsequent state $s ^ { \prime } \sim P ( s ^ { \prime } | s , \pmb { a } )$ and generate the global reward $\mathcal { R } = [ r _ { 1 } , r _ { 2 } , . . . , r _ { N } ]$ ( ). The ultimate goal is to establish a joint pol-=icy Ï $\cdot ( \tau ^ { \prime } , a )$ ]such that $Q _ { \mathrm { t o t } } ^ { \pi } ( \tau ^ { \prime } , \pmb { a } ) = \mathbb { E } _ { s , \pmb { a } } [ \sum _ { s , \pmb { a } } ^ { \infty } \gamma ^ { t } R ( s , \pmb { a } ) \mid s _ { 0 } =$ $s , \mathbf { } a _ { 0 } = \mathbf { } a , \pi ]$ where $\tau _ { n } ^ { \prime } = ( o _ { n } ^ { 1 } , a _ { n } ^ { 1 } , \ldots , o _ { n } ^ { t - 1 } , a _ { n } ^ { t - 1 } , o _ { n } ^ { t } )$ repre-= ] = (sents some historical information.

The observation, action, and reward settings for the agent in reinforcement learning are as follows:

1) Observation Space: As mentioned in Section IV, our goal is network load balancing and efficient packet transmission. Therefore, we consider not only the routing indicators of DTN, which are solely based on transmission efficiency, but also the queue status of each node [43]. When transmitting specific data packets, we use an integrated routing decision model to represent the encounter probability between nodes, thereby improving transmission success rates. Additionally, we achieve load balancing across the entire UAV swarm system by controlling the state of system queues. We define the observation space of any agent at time t as:

$$
\begin{array} { c } { o _ { n } ^ { t } = \left[ Q _ { n } ( t ) , \lambda _ { n , d } ^ { a } ( t ) , \mu _ { n , d } ^ { b } ( t ) , S y n u t i l _ { n } ( d ) \right] } \\ { { \phantom { \frac { 1 } { 2 } } } } \\ { { a \neq n , b \neq n , \forall a , b , n \in \mathbb { N } , } } \end{array}\tag{24}
$$

where $Q _ { n } ( t )$ represents the queue backlog of the current node n, $\lambda _ { n , d } ^ { a } ( t )$ ( )represents that all data packets from UAV a to destination UAV d exist in UAV $n , \mu _ { n , d } ^ { b } ( t )$ represents that node n sends a data packet with destination d to node $b , S y n u t i l _ { n } ( d )$ is a $1 \times \mathsf { N } -$ ( ) 1dimensional array, which represents the DTN routing metric index of node n for node d.

2) Action Space: Therefore, for each agent n, By jointly considering the node queue congestion status and routing metrics based on observed state values, we define the action as selecting the next-hop relay node and learning it through interaction with the environment.

$$
\mathcal { A } = [ \mathcal { N } _ { x 1 } , \mathcal { N } _ { x 2 } , . . . \mathcal { N } _ { x n } ] .\tag{25}
$$

3) Reward: As designed by $P 2 .$ , we consider forming a 2multi-objective optimization equation to minimize the Lyapunov optimization function and transmission delay and maximize the transmission success rates. For agent n, we set the reward to this optimization equation:

$$
\begin{array} { r l r } {  { { \boldsymbol { r } } _ { n } = \Delta L + V \cdot P } } \\ & { } & { \quad \mathrm { ~ } \mathrm { ~ } } \\ & { } & { = B + \sum _ { n = 0 } ^ { \mathcal { N } - 1 } \sum _ { d = 0 } ^ { \mathcal { N } - 1 } Q _ { n , d } ( t ) \cdot \big [ A _ { n , d } ( t + 1 ) + \lambda _ { n , d } ^ { a } ( t ) - \mu _ { n , d } ^ { b } ( t ) \big ] } \\ & { } & { \quad \mathrm { ~ } + V \cdot P . } \end{array}
$$

## B. On-Demand Collaborative Reinforcement Learning-Based Routing Algorithm

The architecture of our proposed routing algorithm is illustrated in Fig. 2, which is based on the literature [44]. Fig. 2 shows the on-demand collaborative routing algorithm we propose based on Lyapunov. It is a collaborative partial observation multi-agent reinforcement learning algorithm. Each agent focuses on the historical observation information of different teammates and the current agent. Establish different teammate models. Due to the characteristics of sparse communication in the DTN, more efficient interaction can be achieved under limited communication conditions by establishing different teammate models, and the comprehensive global information pertaining to the UAV swarm network can be indirectly used to achieve joint scheduling and transmission of data packets.

Algorithm 2: On-Demand Collaboration Routing Algo  
rithm Based on Lyapunov (LAMAIC).   
1: Configure the multi-UAV networked system and   
initialize the parameters of the proposed algorithm.   
2: for episode  to $M A X _ { e p i s o d e }$ do   
3: = 1 Reset the environment.   
4: for t   to $M A X _ { \mathcal { T } }$ do   
5: = 1 Get initial state ${ \mathcal S } ,$ local observation $o _ { n } ^ { t } ,$ , and   
available actions A as predata.   
6: Use predata to update buffer $D _ { b u f f e r } .$   
7: Calculate communication weight $\alpha _ { n j } ,$ teammate   
modeling $z _ { n j } .$ , customized message $v _ { n j }$ to   
generate the final message $m _ { n j } .$   
8: Predict the transmission actions ${ \mathcal { A } } .$   
9: Calculate $V _ { x y z } ^ { n } ( t )$ according to (5), then Calculate   
( )the UAV positions $P _ { x y z } ^ { n } .$   
10: Calculate DTN metrics for UAV swarm according   
to (13) to (17).   
11: Execute clustering Algorithm 1.   
12: Users generates interest pack $\mathfrak { I } = [ 1 , 2 , \dots I _ { n } ]$ and   
= [1 2propagates within each cluster to find the   
corresponding datapacket.   
13: for UAV node n  to N do   
14: = 1if designated UAV in the communication range   
then   
15: Send datapackets.   
16: end if   
17: end for   
18: According to actions to send datapacket.   
19: for UAV node $n = 1$ to N do   
20: = 1if queue is not empty and the next hop uav   
according to the actions in the communication   
range then   
21: $T T L - = 1$ then transmit packets.   
22: = 1 Calculate the $\mu _ { n , d } ^ { d } ( t ) , \lambda _ { n , d } ^ { a } ( t )$ and $Q _ { n , d } ( t + 1 )$   
( ) (by according to (9) to (11).   
23: end if   
24: end for   
25: Calculate the reward.   
26: Gets the local observation $o _ { n } ^ { t }$ and R as postdata.   
27: Use predata to update buffer $D _ { b u f f e r } .$   
28: end for   
29: if burn_in_period < episode_buffer then   
30: Start train, Calculate the estimated Q Values, target   
Q Values and update the loss function by (31).   
31: end if   
32: end for

<!-- image-->  
Fig. 2. On-demand collaborative algorithm framework based on Lyapunov (LAMAIC).

In Fig. 2, each agentâs local network graph (b) includes both a teammate-modeled network graph (a) and a customized message generator graph (c). Each agent inputs its recent observations and prior actions into the GRU unit, which processes this data to extract historical insights and compute local Q values using the multi-layer perceptron (MLP). LAMAIC agents utilize sampled representations of teammate models to generate communication weights and customized message content. Then, the customized messages directly affect the action strategies of other agents in an incentive manner. In this way, efficient, sparse communication is achieved for DTN.

1) Teammate Model: First, for each agent n, the local information $o _ { n } ^ { t }$ of its surrounding neighbors in observation time slot t and the action $a _ { n } ^ { t - 1 }$ taken by the current agent in the previous time slot are input to the MLP. Then, historical information $\tau _ { n } ^ { t - 1 }$ and the output from the multilayer perceptron are merged and fed into a GRU (Gated Recurrent Unit) cell to generate all prior historical information up to time slot t, which is then input into the teammate model generator. Currently, for each teammate, the teammate number j and all the historical information owned by the current agent are input, and they are encoded and Gaussian sampling $N ( \mu _ { n j } , \sigma _ { n j } ^ { 2 } )$ to get teammate model $z _ { n j }$

2) Customized Information: Similar to Fig. 2(a), first obtain all historical information $\tau _ { n }$ observed by the current agent through MLP and GRU, and at the same time input the teammate model $z _ { n j }$ for a specific teammate, generate customized information ${ \pmb v } _ { n j } = f _ { m } ( \tau _ { n } , z _ { n j } )$ through a multi-layer linear neural network, and use $\begin{array} { r } { \alpha _ { n j } = \frac { \mathrm { ~ \normalsize ~ e x p ~ } ( \lambda q _ { i } ^ { T } k _ { n j } ) } { \Sigma _ { m \neq n } \exp \left( \lambda q _ { n } ^ { T } k _ { n m } \right) } } \end{array}$ to generate communication weights. Reduce useless communication and redundant information through $\alpha _ { n j }$ , because unnecessary information may reduce the receiverâs learning efficiency. Where Î» is the scaling parameter, $q _ { n } ^ { T }$ and $k _ { n j }$ are calculated through simple linear functions of the fully connected layer, then the customized information is $m _ { n j } = \alpha _ { n j } v _ { n j }$

TABLE II  
REINFORCEMENT LEARNING ALGORITHM PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>gamma r</td><td rowspan=1 colspan=1>0.99</td></tr><tr><td rowspan=1 colspan=1>batch_size</td><td rowspan=1 colspan=1>32</td></tr><tr><td rowspan=1 colspan=1>buffer_size</td><td rowspan=1 colspan=1>32</td></tr><tr><td rowspan=1 colspan=1>Learning rate for agents $l r$ </td><td rowspan=1 colspan=1>0.0006</td></tr><tr><td rowspan=1 colspan=1>Learning rate for critics</td><td rowspan=1 colspan=1>0.0006</td></tr><tr><td rowspan=1 colspan=1>RMSProp alpha</td><td rowspan=1 colspan=1>0.98</td></tr></table>

=In addition, for the teammate model, the learned teammate model can directly act on the action selection of each teammate to intuitively represent the collaborative relationship between agents, thereby controlling the stability of the network and providing continuous sustainable services. Therefore, the algorithm introduces the loss function of the teammate model generator to guide the generation of the teammate model, namely:

$$
\zeta _ { m } \left( \pmb { \theta } _ { m } \right) = \sum _ { n \neq j } E _ { \mathcal { D } } \left[ D _ { K L } ( p ( z _ { n j } | \tau _ { n } , d _ { j } ) \ | | \ q _ { \xi } ( z _ { n j } | \tau _ { n } , a _ { j } , d _ { j } ) ) \right] ,\tag{27}
$$

where $D _ { K L }$ represents the Kullback-Leibler divergence [45], p represents the conditional distribution, $q _ { \xi }$ represents the variational distribution, which are all extracted from $D _ { b u f f e r }$ , and $\theta _ { m }$ represents a series of parameters of the teammate model generator. Similarly, the communication weight loss function in the message generator is:

$$
\mathcal { L } _ { c } \left( \pmb { \theta } _ { c } \right) = - \sum _ { n \neq j } ^ { n } \alpha _ { n j } \log \alpha _ { n j } ,\tag{28}
$$

where $\theta _ { c }$ represents message generator parameters.

Each agent has a $Q _ { n } ^ { l o c }$ . The $Q$ value is determined by the historical information and actions of the agent itself. When the customized information of other agents acts on $Q _ { n } ^ { l o c }$ , it directly affects its next action selection, expressed as:

$$
Q _ { n } \left( \tau _ { n } ^ { \prime } , \cdot \right) = Q _ { n } ^ { \mathrm { l o c } } \left( \tau _ { n } ^ { \prime } , \cdot \right) + \sum _ { j \neq n } m _ { j n } ,\tag{29}
$$

where $\textstyle \sum _ { j \neq n } m _ { j n }$ represents the sum of customized information of other agents for the current agent n.

Since the algorithm is a CTDE framework, the algorithm input the local Q values into the hybrid network QPLEX to form the global $\begin{array} { r } { Q _ { t o t } ( \tau ^ { \prime } , a ) = \sum _ { n \in \mathbb { N } } Q _ { n } ( \tau _ { n } ^ { \prime } , a _ { n } ) } \end{array}$

$$
\begin{array} { r } { \mathcal { L } _ { \mathrm { T D } } ( \pmb { \theta } ) = \mathbb { E } _ { ( \pmb { \tau } ^ { \prime } , \pmb { a } , \pmb { r } , \pmb { \tau } ^ { \prime \prime } ) \sim \mathcal { D } } \left[ \left( y - Q _ { \mathrm { t o t } } \left( \pmb { \tau } ^ { \prime } , \pmb { a } ; \pmb { \theta } \right) \right) ^ { 2 } \right] , } \end{array}\tag{30}
$$

where $\begin{array} { r } { y = r + \operatorname* { m a x } _ { a ^ { \prime } } Q _ { \mathrm { { t o t } } } ( \pmb { \tau } ^ { \prime } , \pmb { a } ^ { \prime } ; \pmb { \theta } ^ { - } ) } \end{array}$ represents the target and $\theta ^ { - }$ = + max ( ; )is the parameters of the target network that are updated regularly.

The algorithmâs learning objective is to minimize the loss function across all models, defined as:

$$
\mathcal { L } \left( \pmb { \theta } \right) = \mathcal { L } _ { \mathrm { T D } } ( \pmb { \theta } ) + \eta _ { m } \cdot \sum _ { i = 1 } ^ { n } \mathcal { L } _ { m } \left( \pmb { \theta } _ { m } \right) + \eta _ { c } \cdot \sum _ { i = 1 } ^ { n } \mathcal { L } _ { c } \left( \pmb { \theta } _ { c } \right) ,\tag{31}
$$

where $\eta _ { m }$ and $\eta _ { c }$ are the adjustable hyperparameters of teammate modeling loss and sparse regularization, respectively, Î¸ representing all network parameters of the algorithm. The ondemand collaborative communication routing algorithm based on Lyapunov is described in Algorithm 2.

## VI. SIMULATION RESULTS AND DISCUSSIONS

This section presents experimental evidence that substantiates the performance of the proposed method.

TABLE III  
NETWORK ENVIRONMENT SETTING
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Number of interest packages J</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>Number of packets D</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>Maximum cache spaces $M A X _ { m e m }$ </td><td rowspan=1 colspan=1>4GB</td></tr><tr><td rowspan=1 colspan=1>Maximum bandwidth bw (uv)</td><td rowspan=1 colspan=1>85Mbps</td></tr><tr><td rowspan=1 colspan=1>Slot J</td><td rowspan=1 colspan=1> $2 0 0 \tau _ { 0 }$ </td></tr><tr><td rowspan=1 colspan=1>Packet lifetime TTL</td><td rowspan=1 colspan=1> $5 \tau _ { 0 }$ </td></tr><tr><td rowspan=1 colspan=1>Packet size of data</td><td rowspan=1 colspan=1>5-15KB</td></tr><tr><td rowspan=1 colspan=1>UAV number N</td><td rowspan=1 colspan=1>8/10/13</td></tr><tr><td rowspan=1 colspan=1>Communication range C</td><td rowspan=1 colspan=1>500m</td></tr></table>

## A. Simulation Settings

To underscore the effectiveness of our proposed algorithm, we compare its performance against three baseline methods, namely:

1) Traditional algorithm (PROPHET): The PROPHETbased routing algorithm predicts the nodeâs future connection based on the history and transitivity between nodes and formulates routing decisions accordingly. The fundamental principle of the algorithm is that if two nodes have often encountered each other in the past, then the probability of their encounter in the future is also high [46].

2) Genetic algorithm(GA): The GA-based routing algorithm imitates the evolutionary process in natural selection and genetics to solve optimization and search problems [47]. For the selection of UAV relays, it searches for the best mutation method through iterative mutation of genes.

3) MAPPO algorithm: The MAPPO-based routing algorithm policy optimization technology is utilized to limit the degree of policy changes at each update [16]. Its reward, status, and action settings are given in Section V.

In the experiment, the datasets are of different sizes to represent different requests, and each training step is randomly generated data to characterize the robustness and authenticity of the algorithm. We set five data packet types, each has a corresponding interest packet, and the life cycle TTL of the data packet is set to 5 time slots. The remaining parameters are listed in Table III. The reinforcement learning parameter settings are shown in Table II

## B. Convergence Analysis

Fig. 3(a)â(c) shows the network convergence performance curves when the UAV swarm size is 8, 10, and 13. In the different scale network environments, it can be found that the convergence curves of both the heuristic and the traditional algorithms have no apparent fluctuations. The main reason is that these two algorithms do not interact with the UAV network environment when optimizing the strategy and cannot dynamically update their strategies based on the dynamics of the network environment, resulting in a flatter curve. The convergence curves of the other two reinforcement learning algorithms show that their effects are better than those of non-reinforcement learning algorithms.

<!-- image-->  
(a)UAV8

<!-- image-->  
(b)UAV10

<!-- image-->  
(c) UAV13

<!-- image-->  
(d) UAV8

<!-- image-->  
(e) UAV10

<!-- image-->  
(f) UAV13  
Fig. 3. Network convergence analysis and Lyapunov optimization function.

In addition, our proposed algorithm has the optimal effect in all cases. This is because the collaborative reinforcement learning algorithm considers global information through customized teammate models and messages when optimizing and reduces the redundancy of information transmission, resulting in better convergence effects and higher reward values. It is also observed that the convergence value decreases with the increase in the UAV swarm size. This is mainly due to the dominance of the Lyapunov optimization function in the optimization process. As the network scale increases, the difficulty of achieving system queue stability control also rises. That is, it becomes more challenging to organize and coordinate larger-scale UAVs.

## C. Lyapunov Optimization Function

Fig. 3(d)â(f) shows the performance analysis of the Lyapunov optimization function when the network size is 8, 10, and 13. As mentioned in Section IV-B, the primary objective of minimizing the Lyapunov optimization function is to reduce the permissible variation of the Lyapunov function L t ; thereby, queue status ( )is pushed toward low congestion. Moreover, the literature [40] indicates that if diminished parameter magnitude signifies that there is no mutation in the average queue of the entire network; that is, the queue remains in a stable state. The figure shows that the traditional PROPHET algorithm and the heuristic algorithm have the worst final convergence effects under different UAV group sizes. For these two non-intelligent algorithms, the difference in packet transmission success rates and network transmission delay is that the GA is better than the PROPHET algorithm, mainly because the Lyapunov optimization term dominates the rewards. The GA achieves load balancing and network queue congestion control through iterative optimization of genes. The ensuing problem is that data packet transmission âloopsâ are prone to occur, resulting in the worst transmission success rates and network delay performance. At the same time, the PROPHET algorithm aims at the fastest transmission and has the worst effect on network congestion control, and this also proves our analysis in the results below.

The proposed algorithm exhibits optimal performance for artificial intelligence routing, showing enhanced effectiveness with larger networks. This scalability advantage results from its collaborative optimization approach, enabling agents to access mutual state information. When some UAV devices experience queue instability, the remaining UAV devices jointly schedule data packet transmission and optimize the strategy after receiving the message so that the unstable queue gradually returns to a stable state. Traditional reinforcement learning algorithms only observe local information. When specific equipment becomes unstable, decisions cannot be made in time, resulting in worsening network performance. This is perfectly demonstrated when the UAV scale is 10. When the network size is 13, the connectivity of the UAV network reaches a certain level of stability so that traditional algorithms can collect more local information and formulate better decisions. For the same algorithm applied to networks of varying sizes, it is evident that larger network scales, the higher the final value it converges to (it is a negative number in the figure, and the optimization function index is obtained after inversion), which is similar to reward analysis. The drift boundary can be minimized first by minimizing the Lyapunov optimization function. When the network scale increases, the observation information increases significantly. Each time a device is added, every intelligent device in the cluster must add a teammate model. The algorithmâs complexity also increases, resulting in slow convergence and large fluctuations. Eventually, the coordination ability of the entire more extensive network decreases, and the stability of the network becomes more difficult to control so that the convergence value will be higher.

<!-- image-->  
(a)

<!-- image-->  
(b)

Fig. 4. Network performance analysis. (a) Packet Loss Rate. (b) Packet Transmission Delay.  
<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼

<!-- image-->  
(d)  
Fig. 5. Network mean performance analysis. (a) Mean Network Throughput.(b) Mean Lyapunov Drift. (c) Mean Packet Loss Rate.(d) Mean Network Delay.

## D. Network Performance Analysis

1) Transmission Failure Rate: Fig. 4 analyzes the ultimate convergence of network performance metrics once the network stabilizes. Fig. 4(a) presents a comparative analysis of the transmission failure rates of various algorithms across different UAV group network sizes. The figure shows that both the PROPHET algorithm and the GA have high failure rates under different circumstances. When the network size is 8 and 10, the GA is better than the traditional algorithm. The detailed values are in Table IV. This occurs as the heuristic algorithm identifies the optimal individual by evaluating the fitness function, continuously refining its strategy through mutation and iteration. When the network size continues to increase, the increase in network connectivity brings into play the feature of selecting relay nodes with the maximum encounter probability in the PROPHET, that is, a greedy strategy is employed to select the node with the highest forwarding probability.

TABLE IV  
PERFORMANCE COMPARISON OF ALGORITHMS
<table><tr><td rowspan=2 colspan=1>Algorithm</td><td rowspan=2 colspan=1>Index</td><td rowspan=1 colspan=4>UAV Scale</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>14</td></tr><tr><td rowspan=3 colspan=1>LAMAIC-Based</td><td rowspan=1 colspan=1>Suc-Rate</td><td rowspan=1 colspan=1>82.4%</td><td rowspan=1 colspan=1>91.2%</td><td rowspan=1 colspan=1>98.7%</td><td rowspan=1 colspan=1>99.4%</td></tr><tr><td rowspan=1 colspan=1>delay(hop-counts)</td><td rowspan=1 colspan=1>2.02</td><td rowspan=1 colspan=1>1.32</td><td rowspan=1 colspan=1>1.40</td><td rowspan=1 colspan=1>1.50</td></tr><tr><td rowspan=1 colspan=1>Throughput</td><td rowspan=1 colspan=1>846.3</td><td rowspan=1 colspan=1>788.6</td><td rowspan=1 colspan=1>960.5</td><td rowspan=1 colspan=1>973.4</td></tr><tr><td rowspan=3 colspan=1>MAPPO-Based</td><td rowspan=1 colspan=1>Suc-Rate</td><td rowspan=1 colspan=1>84.1%</td><td rowspan=1 colspan=1>73.1%</td><td rowspan=1 colspan=1>90.2%</td><td rowspan=1 colspan=1>92.2%</td></tr><tr><td rowspan=1 colspan=1>delay(hop-counts)</td><td rowspan=1 colspan=1>1.92</td><td rowspan=1 colspan=1>1.36</td><td rowspan=1 colspan=1>2.28</td><td rowspan=1 colspan=1>2.48</td></tr><tr><td rowspan=1 colspan=1>Throughput</td><td rowspan=1 colspan=1>832.3</td><td rowspan=1 colspan=1>750.5</td><td rowspan=1 colspan=1>893</td><td rowspan=1 colspan=1>935.3</td></tr><tr><td rowspan=3 colspan=1>GA-Based</td><td rowspan=1 colspan=1>Suc-Rate</td><td rowspan=1 colspan=1>57.3%</td><td rowspan=1 colspan=1>59.2%</td><td rowspan=1 colspan=1>18.5%</td><td rowspan=1 colspan=1>12.5%</td></tr><tr><td rowspan=1 colspan=1>delay(hop-counts)</td><td rowspan=1 colspan=1>1.92</td><td rowspan=1 colspan=1>2.03</td><td rowspan=1 colspan=1>3.60</td><td rowspan=1 colspan=1>3.80</td></tr><tr><td rowspan=1 colspan=1>Throughput</td><td rowspan=1 colspan=1>553.3</td><td rowspan=1 colspan=1>613.5</td><td rowspan=1 colspan=1>146.5</td><td rowspan=1 colspan=1>134.2</td></tr><tr><td rowspan=3 colspan=1>PROPHET-Based</td><td rowspan=1 colspan=1>Suc-Rate</td><td rowspan=1 colspan=1>55.7%</td><td rowspan=1 colspan=1>56.2%</td><td rowspan=1 colspan=1>38.3%</td><td rowspan=1 colspan=1>27.6%</td></tr><tr><td rowspan=1 colspan=1>delay(hop-counts)</td><td rowspan=1 colspan=1>2.07</td><td rowspan=1 colspan=1>1.99</td><td rowspan=1 colspan=1>2.67</td><td rowspan=1 colspan=1>2.77</td></tr><tr><td rowspan=1 colspan=1>Throughput</td><td rowspan=1 colspan=1>575.5</td><td rowspan=1 colspan=1>596.4</td><td rowspan=1 colspan=1>381.2</td><td rowspan=1 colspan=1>243.4</td></tr></table>

In the context of multi-agent reinforcement learning, our proposed algorithm consistently achieves optimal performance across various cluster sizes. This is primarily because in the algorithm we proposed, each agent constructs different teammate models for different teammates and generates customized messages to inform other agents of its current status information, including queue backlog status, DTN routing metrics, service rate, and arrival rate information. Through this process, each UAV obtains the status information of other agents, which can be combined with global status information for scheduling to ensure the successful transmission of data packets. The MAPPO algorithm can only update the strategy based on part of the observation information. Therefore, in the case of small-scale UAVs, the observation dimension is small, and it can achieve a performance similar to that of the algorithm we propose. When the scale of UAV increases, the performance of LAMAIC significantly outperforms traditional reinforcement learning algorithms. In the case of a scale of 10, because the network connectivity does not reach the threshold, local optimization caused by local observations of the MAPPO algorithm leads to a sharp deterioration in network performance. It can be seen from the different UAV group sizes of the same algorithm that when the UAV scale increases, moreover,the transmission failure rate is reduced. This is attributable to the enhanced network connectivity that accompanies an increase in scale, and the relay node and the destination UAV have a higher chance of encountering each other. However, because the conventional DTN algorithm does not incorporate the overall network stability in its routing decisions, the transmission failure rate increases as the network scale expands.

2) Network Delay: Fig. 4(b) shows the performance comparison of network delay of different algorithms under different UAV swarm network sizes. The figure demonstrates that the performance of the traditional algorithm and the heuristic algorithm are similar in smaller scenarios. As shown in Fig. 4(a), as the size of the UAV group increases, so does the probability of encounters between nodes. The PROPHET selects the UAV with the highest contact probability with the destination for transmission based on the probabilistic transmission method so that data packets can be transmitted faster. The GA guides the selection of transmission nodes based on the fitness function (based on the objective function) and does not directly consider the encounter probability. The developed multi-agent reinforcement learning (MARL) approach demonstrates superior efficacy compared to conventional single-agent paradigms. This empirical validation aligns with our theoretical proposition regarding comparable performance characteristics between the two methodologies under limited-scale network configurations. This is because the network connectivity is low, and sporadic connections in the network render it impossible to transmit data packets in time, even if global information is available. When the scale of the UAV increases, the algorithm we propose (LAMAIC) has the best effect. The detailed values are in Table IV. In the scenario with a scale of 13 and 14 UAVs, the algorithm we propose has more obvious advantages, mainly because the LAMAIC algorithm has the advantage of generating customized information for different teammates. It directly affects the action selection of other teammates so that it can be achieved. The action of the current agent is based on the status information of other agents in the entire network. In this way, efficient scheduling and transmission of data packets can be realized promptly based on the queue status of the node and the chance of encountering the destination node; that is, global optimization is achieved in a network with intermittent connections. In addition, due to the increase in network scale and the increase in nodes, the traditional algorithm formulates the observation space of each agent larger, rendering it challenging to learn the global optimal routing decision, and the path length increases, further increasing the transmission delay. This is also reflected in LAMAIC, but the algorithm we propose is more robust, with only a tiny increase.

3) Throughput and Other Average Performance Metrics: In Fig. 5, we evaluate different algorithmsâ average network performance metrics under various UAV swarm sizes throughout the training process. The detailed values are in Table IV. In (a), we analyze the throughput of each round of different algorithms in the network. It is clear that throughput performance is linked to the transmission failure rate (c); as the failure rate decreases, throughput increases. This is due to throughput being an indicator of the number of packets successfully transmitted at each step. Observing (a), It is evident that the algorithm we introduce invariably outperforms baseline methods across a range of scenarios, and we note that in (a), when the size of the UAV group increases from 8 to 10, the average throughput is slightly this because the increase in the scale of the UAV leads to slow policy updates in the early stage, rendering it challenging to learn the optimal transmission strategy, so there is a downward trend. However, when the cluster count reaches 13, the scale of the UAV swarm network reaches a certain connectivity threshold, which alleviates the problem of intermittent connection of the UAV swarm, and an upward trend appears. For (b), (c), and (d), we need to analyze them in conjunction with Figs. 3 and 4. From the average value, the algorithm we propose performs best in most cases. However, in (d), When the number of UAVs is 10, its average network delay performance is slightly worse, but based on Fig. 4, its final convergence value is optimal. This can be attributed to the increased number of UAV groups will lead to low learning efficiency of the teammate model in the algorithm, which requires more training rounds to learn the best model, so poor performance appears in the early stage. Its superiority is reflected in the final convergence value. The global optimal performance is finally achieved through efficient communication and joint optimization.

## VII. CONCLUSION

In this paper, we examine the key challenges confronting DTN-based UAV swarm networks, in achieving efficient data transmission while ensuring network congestion control and load balancing. To address these issues, an edge caching mechanism and an on-demand collaborative communication routing algorithm based on Lyapunov stability control are proposed. First, the edge caching mechanism is integrated with the DTN architecture and deployed within the UAV swarm network to enable efficient information transmission. Second, multiple DTN routing metrics are combined to represent the evolution characteristics of nodes in the network structure. Lyapunov techniques are then used to model the queue of UAV network nodes, deriving the Lyapunov drift function and transforming the load balancing issue into a Lyapunov optimization problem. Finally, in consideration of the sparse communication characteristics of DTN, an on-demand collaborative communication routing algorithm is proposed. Each agent constructs different models tailored to its various teammates to generate customized information, achieving more efficient information transmission and enabling a joint scheduling strategy across the entire UAV swarm network. Experimental results demonstrate that the proposed algorithm performs optimally, with its advantages over comparative algorithms becoming even more pronounced as the network scale increases.

## REFERENCES

[1] L. Gupta, R. Jain, and G. Vaszkun, âSurvey of important issues in UAV communication networks,â IEEE Commun. Surv. Tuts., vol. 18, no. 2, pp. 1123â1152, Second Quarter 2016.

[2] L. Wu and X. Liao, âUAV information detection and processing system based on DTN algorithm,â in Proc. 2nd Int. Conf. Innov. Technol., 2023, pp. 1â5.

[3] P. Duarte, J. Macedo, A. D. Costa, M. J. Nicolau, and A. Santos, âA probabilistic interest forwarding protocol for named data delay tolerant networks,â in Proc. 7th Int. Conf. Ad Hoc Netw., San Remo, Italy, Springer, 2015, pp. 94â107.

[4] Y. Lu, X. Li, Y.-T. Yu, and M. Gerla, âInformation-centric delay-tolerant mobile ad-hoc networks,â in Proc. IEEE Conf. Comput. Commun. Workshops, 2014, pp. 428â433.

[5] F. Li et al., âSoftware-defined networking-assisted content delivery at edge of mobile social networks,â IEEE Internet Things J., vol. 7, no. 9, pp. 8122â8132, Sep. 2020.

[6] L. Cong, H. Yang, Y. Wang, and X. Di, âAn auction-gaming based routing model for LEO satellite networks,â in Proc. Int. Conf. Mach. Learn. Intell. Commun., Springer, 2017, pp. 498â508.

[7] C. Sobin, V. Raychoudhury, G. Marfia, and A. Singla, âA survey of routing and data dissemination in delay tolerant networks,â J. Netw. Comput. Appl., vol. 67, pp. 128â146, 2016.

[8] J. Leguay, T. Friedman, and V. Conan, âEvaluating mobility pattern space routing for DTNs,â 2005, arXiv:cs/0511102.

[9] X. Chen, J. Shen, T. Groves, and J. Wu, âProbability delegation forwarding in delay tolerant networks,â in Proc. 18th Int. Conf. Comput. Commun. Netw., 2009, pp. 1â6.

[10] J. Peng, H. Gao, L. Liu, Y. Wu, and X. Xu, âFNTAR: A future network topology-aware routing protocol in UAV networks,â in Proc. 2020 IEEE Wireless Commun. Netw. Conf., 2020, pp. 1â6.

[11] I. Mahmud and Y.-Z. Cho, âLECAR: Location estimation-based congestion-aware routing protocol for sparsely deployed energy-efficient UAVs,â Sensors, vol. 21, no. 21, 2021, Art. no. 7192.

[12] W. Gao and G. Cao, âUser-centric data dissemination in disruption tolerant networks,â in Proc. IEEE Conf. Comput. Commun., 2011, pp. 3119â3127.

[13] E. Bulut and B. K. Szymanski, âExploiting friendship relations for efficient routing in mobile social networks,â IEEE Trans. Parallel Distrib. Syst., vol. 23, no. 12, pp. 2254â2265, Dec. 2012.

[14] C. Wang, B. Zhao, W. Peng, C. Wu, and Z. Gong, âRouting algorithm based on ant colony optimization for DTN congestion control,â in Proc. 15th Int. Conf. Netw.-Based Inf. Syst., 2012, pp. 715â720.

[15] F. Xia, L. Liu, J. Li, A. M. Ahmed, L. T. Yang, and J. Ma, âBEEINFO: Interest-based forwarding using artificial bee colony for socially aware networking,â IEEE Trans. Veh. Technol., vol. 64, no. 3, pp. 1188â1200, Mar. 2015.

[16] C. Han, H. Yao, T. Mai, N. Zhang, and M. Guizani, âQMIX aided routing in social-based delay-tolerant networks,â IEEE Trans. Veh. Technol., vol. 71, no. 2, pp. 1952â1963, Feb. 2022.

[17] Y. Hayamizu, M. Yamamoto, and T. Yagyu, âEnergy and bandwidth efficient content retrieval for content centric networks in DTN environment,â in Proc. 2015 IEEE Globecom Workshops, 2015, pp. 1â6.

[18] E. Monticelli, B. M. Schubert, M. Arumaithurai, X. Fu, and K. Ramakrishnan, âAn information centric approach for communications in disaster situations,â in Proc. IEEE 20th Int. Workshop Local Metrop. Area Netw., 2014, pp. 1â6.

[19] H. M. Islam, D. Lagutin, A. Lukyanenko, A. Gurtov, and A. YlÃ¤-JÃ¤Ã¤ski, âCIDOR: Content distribution and retrieval in disaster networks for public protection,â in Proc. IEEE 13th Int. Conf. Wireless Mobile Comput. Netw. Commun., 2017, pp. 324â333.

[20] C. Anastasiades, T. Schmid, J. Weber, and T. Braun, âInformation-centric content retrieval for delay-tolerant networks,â Comput. Netw., vol. 107, pp. 194â207, 2016.

[21] Y. Gong, H. Yao, D. Wu, W. Yuan, T. Dong, and F. R. Yu, âComputation offloading for rechargeable users in space-air-ground networks,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 3805â3818, Mar. 2023.

[22] S. Bi, L. Huang, H. Wang, and Y.-J. A. Zhang, âLyapunov-guided deep reinforcement learning for stable online computation offloading in mobileedge computing networks,â IEEE Trans. Wireless Commun., vol. 20, no. 11, pp. 7519â7537, Nov. 2021.

[23] C. Qiu, Y. Hu, Y. Chen, and B. Zeng, âLyapunov optimization for energy harvesting wireless sensor communications,â IEEE Internet Things J., vol. 5, no. 3, pp. 1947â1956, Jun. 2018.

[24] Z. Zhuang, J. Wang, Q. Qi, J. Liao, and Z. Han, âAdaptive and robust routing with Lyapunov-based deep RL in MEC networks enabled by blockchains,â IEEE Internet Things J., vol. 8, no. 4, pp. 2208â2225, Feb. 2021.

[25] H. Wu, J. Chen, T. N. Nguyen, and H. Tang, âLyapunov-guided delayaware energy efficient offloading in IIoT-MEC systems,â IEEE Trans. Ind. Informat., vol. 19, no. 2, pp. 2117â2128, Feb. 2023.

[26] A. Asheralieva and D. Niyato, âGame theory and Lyapunov optimization for cloud-based content delivery networks with device-to-device and UAVenabled caching,â IEEE Trans. Veh. Technol., vol. 68, no. 10, pp. 10094â 10110, Oct. 2019.

[27] R. Han, Q. Guan, F. R. Yu, J. Shi, and F. Ji, âCongestion and position aware dynamic routing for the Internet of Vehicles,â IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 16082â16094, Dec. 2020.

[28] B. Liu, W. Zhang, W. Chen, H. Huang, and S. Guo, âOnline computation offloading and traffic routing for UAV swarms in edge-cloud computing,â IEEE Trans. Veh. Technol., vol. 69, no. 8, pp. 8777â8791, Aug. 2020.

[29] Y. Kim and W. Choi, âLyapunov-based energy-efficient path diversity for data transmissions in UAV networks,â IEEE Wireless Commun. Lett., vol. 10, no. 8, pp. 1766â1770, Aug. 2021.

[30] A. S. Kumar, L. Zhao, and X. Fernando, âTask offloading and resource allocation in vehicular networks: A Lyapunov-based deep reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13360â 13373, Oct. 2023.

[31] C. Qiu, Z. Chen, X. Ren, Z. Dai, C. Zhang, and X. Wang, âAimers-6G: AIdriven region-temporal resource provisioning for 6G immersive services,â IEEE Wireless Commun., vol. 30, no. 3, pp. 196â203, Jun. 2023.

[32] X. Tian and Z. Zhu, âOn the distributed routing and data scheduling in interplanetary networks,â in Proc. 2022 IEEE Int. Conf. Commun., 2022, pp. 1131â1136.

[33] J. Xie, Y. Wan, B. Wang, S. Fu, K. Lu, and J. H. Kim, âA comprehensive 3-dimensional random mobility modeling framework for airborne networks,â IEEE Access, vol. 6, pp. 22849â22862, 2018.

[34] T. Wu et al., âProbabilistic shaping four-dimensional modulation with soft decision for self-homodyne coherent detection systems,â IEEE Trans. Commun., vol. 72, no. 8, pp. 4992â5002, Aug. 2024.

[35] M. Neely, Stochastic Network Optimization With Application to Communication and Queueing Systems. San Rafael, CA, USA: Morgan & Claypool, 2010.

[36] E. M. Daly and M. Haahr, âSocial network analysis for routing in disconnected delay-tolerant MANETs,â in Proc. 8th ACM Int. Symp. Mobile Ad Hoc Netw. Comput., 2007, pp. 32â40.

[37] E. M. Daly and M. Haahr, âSocial network analysis for information flow in disconnected delay-tolerant MANETs,â IEEE Trans. Mobile Comput., vol. 8, no. 5, pp. 606â621, May 2009.

[38] A. Mei, G. Morabito, P. Santi, and J. Stefa, âSocial-aware stateless forwarding in pocket switched networks,â in Proc. IEEE Conf. Comput. Commun., 2011, pp. 251â255.

[39] X. Wang, X. Ren, C. Qiu, Z. Xiong, H. Yao, and V. C. Leung, âIntegrating edge intelligence and blockchain: What, why, and how,â IEEE Commun. Surv. Tuts., vol. 24, no. 4, pp. 2193â2229, Fourth Quarter 2022.

[40] T. Yang, L. Kong, N. Zhao, and R. Sun, âEfficient energy and delay tradeoff for vessel communications in SDN based maritime wireless networks,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 6, pp. 3800â3812, Jun. 2021.

[41] Z. Liu, J. Zhang, Z. Liu, H. Xiao, and B. Ai, âDouble-layer power control for mobile cell-free XL-MIMO with multi-agent reinforcement learning,â IEEE Trans. Wireless Commun., vol. 23, no. 5, pp. 4658â4674, May 2024.

[42] Z. Liu et al., âCell-free XL-MIMO meets multi-agent reinforcement learning: Architectures, challenges, and future directions,â IEEE Wireless Commun., vol. 31, no. 4, pp. 155â162, Aug. 2024.

[43] X. Wang, Y. Zhao, C. Qiu, Z. Liu, J. Nie, and V. C. Leung, âInFEDge: A blockchain-based incentive mechanism in hierarchical federated learning for end-edge-cloud communications,â IEEE J. Sel. Areas Commun., vol. 40, no. 12, pp. 3325â3342, Dec. 2022.

[44] L. Yuan et al., âMulti-agent incentive communication via decentralized teammate modeling,â in Proc. AAAI Conf. Artif. Intell., 2022, pp. 9466â 9474.

[45] Z. Liu, Z. Liu, J. Zhang, H. Xiao, B. Ai, and D. W. K. Ng, âUplink power control for extremely large-scale MIMO with multi-agent reinforcement learning and fuzzy logic,â in Proc. IEEE Conf. Comput. Commun. Workshops, 2023, pp. 1â6.

[46] S. Grasic, E. Davies, A. Lindgren, and A. Doria, âThe evolution of a DTN routing protocolâPRoPHETv2,â in Proc. 6th ACM Workshop Challenged Netw., 2011, pp. 27â30.

[47] E. R. Silva and P. R. Guardieiro, âAn efficient genetic algorithm for anycast routing in delay/disruption tolerant networks,â IEEE Commun. Lett., vol. 14, no. 4, pp. 315â317, Apr. 2010.

<!-- image-->  
Qun Li (Student Member, IEEE) is currently working toward the PhD degree with the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His research interests include network artificial intelligence, deterministic network and future networks.

<!-- image-->

Zunliang Wang (Student Member, IEEE) is currently working toward the PhD degree with the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His research interests include network artificial intelligence, wireless network routing, deterministic networking and dedicated networks.

<!-- image-->

Haipeng Yao (Senior Member, IEEE) received the PhD degree from the Department of Telecommunication Engineering, University of Beijing University of Posts and Telecommunications, in 2011. He is a professor with the Beijing University of Posts and Telecommunications. His research interests include future network architecture, network artificial intelligence, networking, space-terrestrial integrated network, network resource allocation and dedicated networks. He has published more than 150 papers in prestigious peer-reviewed journals and conferences.

He has served as an associate editor of IEEE Transactions on Mobile Computing, IEEE Transactions on Sustainable Computing. He has also served as a member of the technical program committee as well as the Symposium chair for a number of international conferences, including IWCMC 2019 Symposium chair, ACM TUR-C SIGSAC2020 Publication chair.

<!-- image-->

Tianle Mai (Member, IEEE) received the PhD degree from the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His research interests include unmanned swarm networks, future network architecture, network artificial intelligence, multiagent system, space-terrestrial integrated network, network resource allocation and dedicated networks. He has published more than 30 papers in prestigious peer-reviewed journals and conferences.

<!-- image-->

Zhipei Li received the PhD degree in electronic science and technology from the Beijing University of Posts and Telecommunications, in 2019. He was with Transmission and Access Research Department of Huawei Technologies Co Ltd for one year. He is currently an associate research fellow with the School of Information and Electronics, Beijing Institute of Technology. He has published more than 60 papers in peer-reviewed journals and conferences. His research interests include broadband communication network, application of artificial intelligence in communication

system, high-speed optical fiber communication systems and coherent digital signal processing techniques.

<!-- image-->

Mohsen Guizani (Fellow, IEEE) received the BS (with distinction), MS, and PhD degrees in electrical and computer engineering from Syracuse University, Syracuse, New York. He is currently a professor and the associate provost with Mohamed Bin Zayed University of Artificial Intelligence (MBZUAI), Abu Dhabi, UAE. Previously, he worked in different institutions in the USA. His research interests include applied machine learning and artificial intelligence, Internet of Things (IoT), intelligent systems, smart city, and cybersecurity. He was listed as a clarivate analytics highly cited researcher in computer science, in 2019, 2020, and 2021, respectively. He has won several research awards including the 2o15 IEEE Communications Society Best Survey Paper Award as well 4 best paper awards from ICC and Globecom Conferences. He is the author of ten books and more than 800 publications. He is also the recipient of the 2017 IEEE Communications Society Wireless Technical Committee (WTC) Recognition Award, the 2018 AdHoc Technical Committee Recognition Award, and the 2019 IEEE Communications and Information Security Technical Recognition (CISTC) Award.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_10_img_1.jpeg|page_10_img_1]]
3. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_12_img_1.jpeg|page_12_img_1]]
4. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_13_img_1.jpeg|page_13_img_1]]
5. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_13_img_2.jpeg|page_13_img_2]]
6. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_16_img_1.jpeg|page_16_img_1]]
7. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_16_img_2.jpeg|page_16_img_2]]
8. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_17_img_1.jpeg|page_17_img_1]]
9. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_17_img_2.jpeg|page_17_img_2]]
10. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_17_img_3.jpeg|page_17_img_3]]
11. [[../extracted_images/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching/page_17_img_4.jpeg|page_17_img_4]]

---

