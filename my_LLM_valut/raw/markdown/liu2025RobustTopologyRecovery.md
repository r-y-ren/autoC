# On the Robust Topology Recovery of UAV Swarm for Detection and Localization of Electronic Signals

Linfeng Liu , Wenzhe Zhang, Xingyu Li , and Jia Xu , Senior Member, IEEE

AbstractâAt present, Unmanned Aerial Vehicle (UAV) swarm has been extensively applied in various fields. In the application of detection and localization of electronic signals, some UAVs could become disabled due to some abnormal events (e.g. electromagnetic interference and battery electricity exhaustion), and the topology connectivity of UAV swarm could be impaired, i.e., the topology of UAV swarm could be partitioned. For the topology recovery issue, we first propose Robust Topology Recovery Algorithm of UAV swarm (RTRA) to recover the topology connectivity of UAV swarm and enhance the topology robustness (reduce the number of potential topology recoveries in future) by relocating some UAVs to new positions with shortest flight distance. Furthermore, we note that the relocated UAVs are easy to exhaust the battery electricity and fail due to the extra flight movements for the topology recoveries, which affects the topology robustness. To this end, we present Cascading Robust Recovery Topology Algorithm of UAV swarm (CRTRA), which adopts a cascading movement strategy to share the flight movements among multiply relocated UAVs, thus avoiding the battery electricity exhaustion of the relocated UAVs. Extensive simulations and comparisons demonstrate that our proposed CRTRA can effectively recover the topology connectivity of UAV swarm while enhancing the topology robustness and shortening the flight distance of relocated UAVs, and CRTRA is especially suitable for some missions such as the detection and localization of electronic signals where UAVs are prone to fail.

Index TermsâUAV swarm, topology robustness, topology connectivity, detection and localization of electronic signals.

## I. INTRODUCTION

U NMANNED Aerial Vehicle (UAV) has achieved rapidadvancements and is increasingly employed in a variety advancements and is increasingly employed in a variety of applications due to the versatility and cost-effectiveness [1], [2]. Single UAV often faces some limitations when it carries out some complex missions. For example, both the computation/communication capabilities and mission coverage of single UAV are typically limited, which leads to the inefficiencies of the complex missions. This fact has spurred much interest in the concept of UAV swarm [3], [4], which denotes a group of UAVs operating in a cooperative manner. UAV swarm enhances the computation/communication capabilities significantly, and enables broad mission coverage and complex missions, e.g. Detection and Localization of Electronic Signals (DLES) [5].

<!-- image-->  
Fig. 1. Detection and localization of electronic signals.

As shown in Fig. 1, in DLES missions, some UAVs are deployed to detect and locate the surrounding electronic signals, such as those emitted by aircrafts or base stations. Each UAV utilizes the onboard detector to detect the surrounding electronic signals. Once a UAV detects a beam of electronic signal, it relays the relevant data (e.g. the strength and direction of the electronic signal) to other UAVs that have also detected the same electronic signal to facilitate the data collection. Finally, a UAV is selected to compute the location of the electronic signal based on the collected data.

The cooperations among UAVs make the topology connectivity of UAV swarm become a vital issue [6], [7]. Particularly, for DLES missions, it is important for UAVs to maintain the communications links among them, either through one-hop connection or multi-hop connections, because the topology connectivity ensures that any electronic signals detected by a UAV can be promptly relayed to others, realizing the rapid data collection and DLES missions.

In DLES missions, some UAVs could fail and exit UAV swarm due to some abnormal events, such as electromagnetic interference, mechanical fault, and battery electricity exhaustion, which make some communication links between UAVs destroyed and the topology connectivity of UAV swarm impaired. As illustrated in Fig. 2, a UAV swarm is employed to detect and localize the electronic signals, and it is confronted with abnormal events, and some communication links become invalid, thus resulting in the topology partition. Therefore, it is necessary to investigate the topology recovery issue to defend against the topology partition of UAV swarm.

<!-- image-->  
Fig. 2. A UAV swarm for DLES missions.

The electricity consumption of UAVs is another primary concern, and the electricity consumption required for data transmission is much smaller than that for flight movements. Note that the electricity consumption for flight movements is comprised of two parts: the electricity consumption for hovering which is considered as a fixed component, and the electricity consumption for position alteration which is related to the flight distance [8], [9]. Therefore, our work focuses on minimizing the flight distance of UAVs to reduce the electricity consumption. Additionally, some UAVs could become disabled in DLES missions, which easily leads to the topology partition. However, the existing topology recovery algorithms typically concentrate on recovering the current topology, while overlooking the topology robustness against the potential topology partition [10], [11] in future. Our proposed algorithms will address the topology recovery issue in UAV swarm, and also attempt to enhance the topology robustness by considering the potential topology partition (more UAVs could be disabled in future).

In this paper, we investigate the topology recovery issue of UAV swarm to enhance the topology robustness, particularly for DLES missions. Fig. 3 shows the framework of our methodology, and the main innovations of this paper are summarized as follows: (i) We propose two topology recovery algorithms by categorizing UAVs (nodes) into three types: cut vertices, ordinary nodes, and redundant nodes, based on their roles and impacts on the topology connectivity. The proposed algorithms can recover the topology connectivity of UAV swarm by relocating one or some redundant nodes when the failures of some UAVs result in new cut vertices. The relocated UAVs are selected by minimizing the flight distance and avoiding the potential topology partition. (ii) To achieve stable topology connectivity in UAV swarm, we incorporate algebraic connectivity into the selection process of relocated UAVs, which can effectively enhance the topology robustness and reduce the number of potential topology recoveries in future. (iii) To balance the electricity consumption of UAVs spent on flight movements for topology recoveries, we adopt a cascading movement strategy. This strategy properly distributes the flight movements to some

<!-- image-->  
Fig. 3. Framework of our methodology.

UAVs (the flight movements can be shared by some relocated UAVs), thus balancing the electricity consumption among the relocated UAVs and avoiding the failures of relocated UAVs due to battery electricity exhaustion.

The remainder of this paper is organized as follows: Section II briefly surveys some existing related studies. Section III elaborates on the problem model. Section IV describes the details of our proposed topology recovery algorithms. Theoretical analyses of the proposed algorithms are reported in Section V. Section VI presents extensive simulation results to evaluate the performance of the proposed algorithms. Finally, Section VII concludes the paper.

## II. RELATED WORK

## A. Node Classification

In previous work, there has already been some research on the cut vertices and redundant nodes. For the cut vertices, Xiong et al. introduce a distributed algorithm that identifies the cut vertices by traveling through nodes in parallel [12]. This algorithm applies an interval-coded spanning tree for the edge coloring, and then determines the cut vertices by counting the number of edge colors. [13] proposes a distributed algorithm that uses an adapted meta heuristic method to identify the cut vertices in the minimum vertex cuts set. [14] ensures the integrity of link monitoring and the virtual backbone by identifying the cut vertices and including them in the weighted connected vertex cover. Furthermore, the cut vertices are selected as the monitoring nodes, which can enhance the coverage efficiency.

Different from the cut vertices, the definitions of redundant nodes are quite different. In [15], the function of redundant nodes is similar to that in our work, where the potential data loss and communication interruptions due to the failures of nodes can be reduced by moving some redundant nodes. [16] labels a node as redundant if there exists a larger node which can cover a certain percentage of the nodeâs volume. Wang et al. [17] define the redundant nodes as those deployed to ensure the continuous coverage and communication, and they utilize these redundant nodes to construct a covered redundant path between the original monitoring area and the extended area. In [18], the redundant nodes are categorized into two types: active redundancies and inactive redundancies, and the redundancy configuration enhances the network reliability while ensuring the visual coverage.

## B. Topology Recovery

The topology connectivity of UAV swarm is crucial in complex missions, necessitating a topology recovery algorithm to mitigate the impacts of UAV failures. Extensive research has been conducted on developing some algorithms which focus on the topology recovery issue. Generally, the existing topology recovery algorithms can be categorized into two primary types: reactive algorithms and proactive algorithms.

Reactive topology recovery algorithms initiate the topology recovery process once the sensor network becomes partitioned due to the failures of some nodes. For example, Akkaya et al. propose PADRA [19], which identifies the potential cut vertices through the connected dominating set and designates a failure handler to launch the connectivity restoration process. Ref. [20] introduces a topology construction and maintenance algorithm based on three-stage connected dominating set topology control scheme. Ref. [21] proposes a node importance estimation algorithm termed DACPE to consider the influence of incident edges between the neighbors of disabled nodes. In [10], a heuristic for maintaining the topology connectivity of UAV swarm is presented. This heuristic is based on the connected dominating set and helps to properly select the relocated UAVs. In [22], Zhang et al. develop a topology-control-based recovery strategy that dynamically categorizes the surviving UAVs into backbone ones and cruising ones. This arrangement forms a reliable backbone network that achieves the stable topology connectivity. Ref. [23] establishes some fault recoverability conditions to analyze the recoverability after the nodes failures, and presents an effective self-healing topology control approach.

Proactive topology recovery algorithms enhance the network resilience by employing some backup nodes or establishing the k-connected topology. For example, [11] presents a coverageaware distributed k-connectivity maintenance algorithm that generates the minimum-cost movements of active nodes after a node failure to satisfy the coverage conservation criterion. In [24], a centralized algorithm named MCCR uses a k-connectivity test and a maximum weighted matching algorithm to find the best possible movements for k-connectivity restoration. This algorithm is improved in [25], where it relocates a failed node which does not affect the k-connectivity on the shortest path tree to replace another failed node. Besides, DP k CR is proposed in [26], and DP k CR proactively maintains the k-connectivity by identifying and addressing the potential node failures that could disrupt the missions of UAV swarm. In [27], a k-connectivity recovery algorithm and a partial recovery algorithm are proposed, which can preserve the k-connectivity among original nodes when $k = 2$ and $k = 3 .$ = 2, respectively. In [28], Akram et al. gives a distributed k-connectivity recovery strategy that selects the most costeffective nodes based on the movement cost to replace the failed nodes.

## C. Detection and Localization of Electronic Signals

For DLES missions, some approaches have been developed to enhance the accuracy and efficiency of DLES missions. For example, in [29], an effective method is proposed based on the dechirp-keystone transform and frequency-selective reweighted trace minimization. Shi et al. [30] improve the performance of UAV detection and localization by applying a detection fusion algorithm and a TDOA estimation algorithm based on Bayesian filter. Hu et al. [31] propose a trajectory planning framework for UAV-on-UAV tracking and surveillance, which jointly optimizes the power consumption while improving the disguising performance through distance keeping and altitude variation strategies. [32], [33], and [34] utilize the unique characteristics of various signal sources (e.g. acoustics and radio frequency) to conduct the detection and accurate localization. In [35], Zheng et al. integrate a coprime array radar system with advanced signal processing techniques to improve the accuracy of detection and localization.

## D. Motivation of Our Work

In the execution of DLES missions, various internal or external events can lead to the failures of UAVs. More importantly, the failures of UAVs at key positions could lead to the topology partition of UAV swarm and even disrupt the continuation of DLES missions. However, the existing literature on DLES typically overlooks the UAV failures. Furthermore, selecting appropriate UAVs for topology recoveries to enhance the topology robustness against potential connectivity disruptions is also crucial. To deal with these challenges, this paper focuses on the topology recovery issue which is essential for maintaining the topology connectivity and functionality of UAV swarm for DLES missions.

## III. PRELIMINARIES

## A. System Model and Assumptions

We consider a UAV swarm performing DLES missions. The topology of UAV swarm is modeled as a three-dimensional undirected graph $G = ( U , E )$ , where $U = \{ u _ { i } | \ i = 1 , \dots , N \}$ = ( ) = = 1denotes the set of UAVs (nodes), and N denotes the number of UAVs in the swarm. The set ${ \boldsymbol { E } } = \{ e _ { i j } | \ e _ { i j } \in { \boldsymbol { U } } \times { \boldsymbol { U } } , u _ { i } , u _ { j } \in$ $U \}$ =denotes the communication links between UAVs, and $( u _ { i } , \ldots , u _ { j } )$ denotes a communication path from $u _ { i }$ to $u _ { j } .$ ( )The current positions of $u _ { i }$ and $u _ { j }$ are denoted by $p _ { i }$ and $p _ { j }$ , respectively. The euclidean distance between $u _ { i }$ and $u _ { j }$ is written as: $d ( i , j ) = \| p _ { i } - p _ { j } \|$ . Assuming that each UAV has ( ) =the same communication range R. If $\mathbf { \dot { \theta } } d ( i , j ) \leqslant R$ , there exists the communication link $e _ { i j }$ ( ). Typically, UAVs in the swarm maintain their current positions by hovering when the UAV swarm is carrying out DLES missions. In addition, we have the following definitions:

Definition 1 (Topology connectivity): A graph G is connected if there is at least one communication path between any two distinct UAVs (nodes).

Definition 2 (One-hop neighbors and two-hop neighbors): In a connected graph $G ,$ the set of nodes that can directly communicate with $u _ { i }$ are taken as the one-hop neighbors of $u _ { i } .$ , denoted by $N _ { i }$ . The set of nodes that can directly communicate with the nodes in $N _ { i }$ but are not in the set $N _ { i } \bigcup u _ { i }$ are taken as the two-hop neighbors of $u _ { i } .$ , denoted by $N _ { i } ^ { 2 } .$ 1

Definition 3 (Cut vertices): In a connected graph $G ,$ a node is taken as a cut vertex if the failure of the node makes G divided into some disconnected subgraphs.

Definition 4 (Redundant nodes): In a connected graph G, a node is taken as a redundant node if the failure of the node does not affect the topology connectivity of G and result in any new cut vertices.

Definition 5 (Ordinary nodes): In a connected graph G, if a node is neither a cut vertex nor a redundant node, it is taken as an ordinary node.

Supposing that each UAV in UAV swarm has a unique ID and knows the current position through the equipped GPS device. Each UAV periodically broadcasts a heartbeat message to the neighbors, which includes the current position and the set of neighbors. Thus, each UAV can obtain the two-hop neighbors according to the received heartbeat messages.

If the heartbeat message of a UAV is not received by the neighbors during a fixed period, the UAV is considered to fail. In DLES missions, UAVs in the swarm hover or move while maintaining the fixed relative positions, the topology recovery is launched when a UAV fails, the UAVs selected as relocated nodes calculate their optimal speed that minimize the electricity consumption according to [36] and proceed to the target positions. When a UAV detects a surrounding electronic signal, it identifies the Pulse Waveform (PW) and Frequency Hopping (FH) of the electronic signal to determine the signal source [37]. The values of PW and FH, along with the strength and direction of the detected signal, are encapsulated into the next heartbeat message. Among all the UAVs detecting the electronic signal, the one with the largest ID will perform the localization of the signal source based on the received heartbeat messages.

Fig. 4 shows an example of the node classifications in a graph, where $u _ { 1 }$ is a cut vertex. The failure of $u _ { 1 }$ will partition the graph into two disjoint subgraphs: $\{ u _ { 2 } , u _ { 3 } , u _ { 4 } , u _ { 5 } , u _ { 6 } , u _ { 7 } , u _ { 8 } \}$ and $\{ u _ { 9 } , u _ { 1 0 } , u _ { 1 1 } , u _ { 1 2 } , u _ { 1 3 } , u _ { 1 4 } \}$ . u9 and $u _ { 1 3 }$ are cut vertices. $u _ { 2 }$ is an ordinary node since the failure of $u _ { 2 }$ will result in a new cut vertex $u _ { 5 } . \ u _ { 3 } , u _ { 4 } , u _ { 5 } , u _ { 7 } , u _ { 1 0 }$ , and $u _ { 1 2 }$ are ordinary nodes. $u _ { 6 }$ is a redundant node, as the failure of $u _ { 6 }$ does not affect the topology connectivity of the graph. Likewise, $u _ { 8 } , u _ { 1 1 }$ , and $u _ { 1 4 }$ are redundant nodes.

<!-- image-->  
Fig. 4. An example of node classifications.

## B. Problem Objectives

Supposing N UAVs forms a connected graph G. For the failures of some UAVs, the problem objectives of robust topology recovery of UAV swarm include: 1) Recovery of topology connectivity: The topology connectivity of UAV swarm is recovered by relocating some UAVs to new positions when the UAV failures result in some new cut vertices or even the topology partition. 2) Reduction of flight distance: The relocated UAVs are selected to recover the topology connectivity by shortening the flight distance. 3) Enhancement of topology robustness: The topology robustness of UAV swarm is enhanced to reduce the number of potential topology recoveries in future. The problem objectives are formulated as follows:

$$
\left\{ \begin{array} { l l } { \sum _ { u _ { i } \in U } C v ( u _ { i } ) = 0 , } \\ { \operatorname* { m i n } \sum _ { u _ { i } \in U _ { r } } d _ { f } ( u _ { i } ) , } \\ { \operatorname* { m i n } N _ { t r } ( T ) , } \end{array} \right.\tag{1}
$$

where $U _ { r }$ denotes the set of relocated UAVs. $C v ( u _ { i } ) = 1$ if $u _ { i }$ is a cut vertex; Otherwise, $C v ( u _ { i } ) = 0 . \ N _ { t r } ( T )$ ( ) = 1denotes the ( ) = 0 ( )number of required topology recoveries during the future time period $( t _ { s }$ time slots).

$\begin{array} { r } { \sum _ { u _ { i } \in U } C v ( u _ { i } ) = 0 } \end{array}$ implies that the cut vertices in UAV ( ) = 0swarm need to be eliminated. $\textstyle \sum _ { u _ { i } \in U _ { r } } d _ { f } ( u _ { i } )$ indicates that min ( )the flight distance of relocated UAVs during the topology recoveries needs to be shortened as much as possible, and $N _ { t r } ( T )$ min ( )indicates that the number of required topology recoveries needs to be reduced (the topology robustness is enhanced) as much as possible. Essentially, these three objectives aim to recover the topology connectivity of UAV swarm with shortest flight distance of relocated UAVs, and enhance the topology robustness of UAV swarm against the potential topology partition in future.

## IV. ROBUST TOPOLOGY RECOVERY ALGORITHMS

As outlined in Section I, when some UAVs fail it is crucial to recover the topology connectivity of UAV swarm while enhancing the topology robustness and shortening the flight distance of relocated UAVs. To this end, we propose two robust topology recovery algorithms, and the relocated UAVs are selected based on the types of UAVs (nodes). We first introduce the node classification method.

<!-- image-->  
Fig. 5. An example of cut vertex determination.

## A. Node Classification Method

We classify the nodes based on their roles and potential impacts on the topology connectivity into three types: cut vertices, ordinary nodes, and redundant nodes.

Once the topology of UAV swarm is constructed, each UAV in the UAV swarm utilizes the Connection Adjacency Matrix (CAM) [38] to determine whether it is a cut vertex: at the beginning of the generation of CAM graph, the cut vertex candidate assigns a unique numerical identifier (referred to as the connection number) to each of its connections. Then, it sends out a probe message to each of its neighbors, which includes a timestamp, a TTL threshold, and the corresponding connection number. When a node detects that a recently received probe message shares the same timestamp as an earlier one but has a different connection number, it sends back an arrival message to the cut vertex candidate. After that, the cut vertex candidate constructs a CAM graph where the nodes represent the neighbors of the cut vertex candidate. If the cut vertex candidate receives some arrival messages containing the connection numbers of two nodes $u _ { i }$ and $u _ { j }$ , an edge will be added between $u _ { i }$ and $u _ { j }$ into the CAM graph. The cut vertex candidate decides whether it is a cut vertex based on the topology connectivity of the CAM graph. If the CAM graph consists of more than one component, then the cut vertex candidate is taken as a cut vertex.

Fig. 5 provides an example of the cut vertex determination, where $u _ { 0 }$ is a cut vertex candidate. In Fig. 5(a), $u _ { 0 }$ assigns a connection number to each of the neighbors $\{ u _ { 1 } , u _ { 2 } , u _ { 3 } , u _ { 4 } \}$ and sends the probe messages to them. In Fig. 5(b), u1, u2, $u _ { 3 }$ , and $u _ { 4 }$ then forward the received probe messages to their neighbors, decrementing the TTL value by 1 with each hop. Finally, $u _ { 5 }$ and $u _ { 6 }$ receive the probe messages and send the arrival messages back to $u _ { 0 }$ , as shown in Fig. 5(c). When the

<!-- image-->

<!-- image-->  
(a) ul is a redundant node  
(b) u2 is an ordinary node  
Fig. 6. An example of redundant node determination.

TTL value is decreased to 0, u0 constructs a CAM graph based on the received arrival messages, as illustrated in Fig. 5(d). Since the CAM graph of $u _ { 0 }$ is disconnected, u0 becomes a cut vertex.

If a node determines that it is not a cut vertex, it proceeds to determine whether it is a redundant node. The redundant node candidate u sends an explore message to the neighbors that includes a timestamp, a TTL threshold, and the traversed communications paths. Then, these neighbors search for the communication paths to other neighbors of u that do not pass through the redundant node candidate and record the nodes along these communication paths. Upon finding a communication path, the node at the end of the traversed communication path sends back a path response message to u that includes the details of the communication path. If u receives multiple path response messages, it identifies the common nodes and instructs them to perform a cut vertex determination in $G \setminus \{ u \}$ , where G \ {u} represents the communication graph obtained by removing u and its connected edges from G. If u receives only one such message, it evaluates the classification of each node along the communication path contained in the message. If any one of these nodes is a cut vertex, then some new cut vertices could be produced by removing u, and thus u is taken as an ordinary node; Otherwise, u is taken as a redundant node.

Fig. 6 illustrates an example of the redundant node determination. In Fig. 6(a), $u _ { 2 }$ and $u _ { 4 } ,$ , the neighbors of a redundant node candidate, search for the communication paths between them that do not pass through $u _ { 1 }$ . With a TTL of $3 , u _ { 1 }$ identifies the following communication paths: $( u _ { 2 } , u _ { 3 } , u _ { 4 } ) , ( u _ { 2 } , u _ { 4 } )$ , and $( u _ { 2 } , u _ { 3 } , u _ { 5 } , u _ { 4 } )$ ( ) ( ). Subsequently, the common nodes u2, u3, and $u _ { 4 }$ )carry out the cut vertex determination in $G \setminus \{ u _ { 1 } \}$ , and $u _ { 1 }$ is determined to be a redundant node. However, in Fig. 6(b), taking a pair of neighbors $u _ { 1 }$ and $u _ { 3 }$ of the redundant node candidate $u _ { 2 }$ as an example, $u _ { 2 }$ identifies the following communication paths: $( u _ { 1 } , u _ { 4 } , u _ { 3 } )$ and $( u _ { 1 } , u _ { 4 } , u _ { 5 } , u _ { 3 } )$ . Subsequently, the common (nodes $u _ { 1 } , \ u _ { 4 }$ , and $u _ { 3 }$ )carry out the cut vertex determination in $G \backslash \{ u _ { 2 } \}$ . Since $u _ { 4 }$ is determined to be a cut vertex, $u _ { 2 }$ is classified as an ordinary node.

When a UAV fails, the surviving UAVs must reassess their classifications and determine whether there are some new cut vertices. If there are not any new cut vertices, the UAV swarm maintains the topology and continues to conduct DLES mission; Otherwise, the UAV swarm launches the topology recovery process.

## B. Robust Topology Recovery Algorithm

When the failure of a node $u _ { f a i l }$ leads to the existence of some new cut vertices, the cut vertex $u _ { k }$ first broadcasts a cut vertex declaration message. Upon receiving this message, the neighbor of $u _ { f a i l }$ with the largest ID reports the position $p _ { f a i l }$ (the current position of $u _ { f a i l } )$ to $u _ { k }$ . We designate $p _ { f a i l }$ as $p _ { t a r } .$ , i.e., the target position for the topology recovery. Then, $u _ { k }$ sends a request message to the nodes in $N _ { k }$ . The request message, expressed as Request $( I D _ { k } , p _ { t a r } , p a t h _ { k } )$ , includes the ID of $u _ { k }$ , the target position $p _ { t a r } .$ ), and the communication path to $u _ { k } \left( p a t h _ { k } \right)$ . Moreover, $u _ { k }$ starts a respond timer to receive the respond messages from redundant nodes over a specified period of ts.

Once receiving a request message from a cut vertex, $u _ { i }$ appends itself to $p a t h _ { k }$ in the request message and forwards this message to its neighbors. Additionally, if $u _ { i }$ is a redundant node, it calculates the weight as follows:

$$
W ( i ) = d ( i , t a r ) ^ { \alpha } ( \Omega ) ^ { \beta } ,\tag{2}
$$

where $d ( i , t a r )$ denotes the distance between $p _ { i }$ and $p _ { t a r }$ . The exponents Î± and $\beta$ are preset parameters, and inspired by [39], the value of  is determined by:

$$
\begin{array} { r } { \Omega = \left\{ \frac { 1 } { | A C _ { f } - A C _ { b } | } , \quad \mathrm { ~ i f ~ } A C _ { f } - A C _ { b } > 0 , \right. } \\ { \left. | A C _ { f } - A C _ { b } | , \quad \mathrm { i f ~ } A C _ { f } - A C _ { b } \le 0 . \right. } \end{array}\tag{3}
$$

In (3), we introduce the metric of Algebraic Connectivity (AC) to measure the topology robustness of UAV swarm. AC quantifies the strength of connections between nodes. In this paper, the AC value 0 indicates that UAV swarm is disconnected, and a larger AC value signifies the better topology connectivity and increased topology robustness against the potential topology partition. Distributed algorithms for calculating AC have been already proposed in several existing works such as [40], [41]. In $( 3 ) , A C _ { f }$ denotes the AC value of UAV swarm after $u _ { i }$ has moved to the position $p _ { t a r } .$ , and $A C _ { b }$ denotes the initial $\mathrm { A C }$ value of UAV swarm. (3) suggests that prioritizing the flight movements of redundant nodes that can improve the topology connectivity of UAV swarm. If there are not any redundant nodes which can improve the topology connectivity of UAV swarm, (3) attempts to decrease the descent of AC value as much as possible.

In Robust Topology Recovery Algorithm of UAV swarm (RTRA), after calculating $W ( i ) , u _ { i }$ sends $u _ { k }$ with a respond message which ( ) is expressed as: $R e s p o n d ( I D _ { k } , I D _ { i } , p a t h ( i , k ) , W ( i ) )$ . Note that the failure (of the node $u _ { f a i l }$ ( ) ( ))could lead to the existence of several new cut vertices. In such case, we select the cut vertex with the largest ID to execute the aforementioned operations: the cut vertices independently send the request messages to their neighbors, when a node receives multiple request messages, it only responds to the cut vertex with the largest ID $u _ { k }$ , while sending the refuse messages to other cut vertices.

After the respond timer expires, $u _ { k }$ stops receiving the respond messages. Then, uk searches the respond queue for the message sent by the node with the smallest weight, and sends an ask message $( A s k ( I D _ { k } , I D _ { i } , p _ { t a r } ) )$ to the redundant node $u _ { i }$ ( )following path i, k . Upon receiving the ask message from $u _ { k }$ $u _ { i }$ is relocated to the target position $p _ { t a r }$ to eliminate the cut vertex. Once the topology recovery has been completed, $u _ { i }$ sends a confirmation to $u _ { k }$

Fig. 7 presents a sequential diagram example regarding the message exchanges in RTRA. The failure of $u _ { f a i l }$ leads to the existence of new cut vertices $u _ { w }$ and $u _ { k }$ . Each of these cut vertices independently sends the request messages to its neighbors. After receiving the request messages, $u _ { o }$ (not a redundant node) continues to forward the request messages. Besides, the redundant node $u _ { i }$ compares the IDs of $u _ { k }$ and $u _ { w } ,$ sends a respond message to $u _ { k }$ with the larger ID and sends a refuse message to $u _ { w } .$ After the respond timer expires, $u _ { k }$ identifies the respond message sent by the node with the smallest weight, and sends an ask message to the corresponding node. Then, $u _ { i }$ is relocated to $p _ { t a r }$ and sends back a confirmation to $u _ { k }$ .

## C. Cascading Robust Recovery Topology Algorithm

We note that the relocated UAVs are easy to exhaust the battery electricity and fail due to the extra flight movements for the topology recoveries, which affects the topology robustness of UAV swarm as well. To this end, we improve RTRA and then present Cascading Robust Recovery Topology Algorithm of UAV swarm (CRTRA), which adopts a cascading movement strategy to share the flight movements among multiply relocated UAVs, thus avoiding the battery electricity exhaustion of the relocated UAVs.

In CRTRA, when new cut vertices exist, the cut vertices initiate the topology recovery process by broadcasting a request message to the neighbors of $u _ { f a i l }$ . The neighbors of $u _ { f a i l }$ record the target position $p _ { t a r }$ (the current position of $u _ { f a i l } )$ and proceed with the topology recovery based on the two-hop neighbors. Thus, the following three cases are discussed:

Case A: When the neighbors of $u _ { f a i l }$ include some redundant nodes, the selection of the relocated node is expressed as (4). The redundant nodes in $N _ { f a i l }$ independently calculate their weights, and the node with the smallest weight $( u _ { m o v e } )$ is selected to move to the position $p _ { t a r }$ :

$$
\boldsymbol { u _ { m o v e } } = \arg \operatorname* { m i n } _ { \boldsymbol { u _ { i } \in N _ { f a i l } } \cap \boldsymbol { S _ { r } } } \boldsymbol { W } ( i ) ,\tag{4}
$$

where $S _ { r }$ denotes the set of redundant nodes.

Case B: When the neighbors of $u _ { f a i l }$ do not include any redundant nodes, and the redundant nodes are found among the two-hop neighbors of $u _ { f a i l }$ . As shown in (5), the neighbor that has redundant node neighbors is selected to move to the position $p _ { t a r } \mathbf { \hat { . } }$

$$
u _ { m o v e } = \arg \operatorname* { m i n } _ { u _ { i } \in N _ { f a i l } } \{ W ( i ) \ | \ \exists u _ { j } \in N _ { i } \cap S _ { r } \} .\tag{5}
$$

Case C: When the neighbors (one-hop neighbors) and twohop neighbors of $u _ { f a i l }$ do not contain any redundant nodes, the neighbor with the smallest weight is selected to move to the position $p _ { t a r }$ :

$$
u _ { m o v e } = \arg \operatorname* { m i n } _ { u _ { i } \in N _ { f a i l } } W ( i ) .\tag{6}
$$

Fig. 8 illustrates the sequence diagram of messages received by an ordinary node $u _ { i }$ , which is a neighbor of the failed node $u _ { f a i l }$ . Before the execution of CRTRA, each node including $u _ { i }$ in UAV swarm clears its weight queue and sets the isMove status flag to 0. When $u _ { i }$ receives a request message from the cut vertex $u _ { k } .$ , it initiates the topology recovery process. If a redundant node $u _ { w }$ exists in $N _ { f a i l } , u _ { w }$ sends an IsR_msg to other nodes in $N _ { f a i l }$ . Once $u _ { i }$ receives IsR_msg from any of its neighbors during $t _ { s }$ time slots (e.g., a time slot is a second), it compares the weights stored in weight queue, and then the node with the smallest weight in the weight queue is selected as the relocated node. If the nodes in $N _ { f a i l }$ do not receive an $I s R \_ m s g$ during $t _ { s }$ time slots, indicating that there are not any redundant nodes in $N _ { f a i l }$ . In this case, the node in $N _ { f a i l }$ proceeds to check its neighbors, which are also the two-hop neighbors of $u _ { f a i l }$ for the presence of redundant nodes. If a neighbor $u _ { j }$ finds that one of its neighbors is a redundant node, then $u _ { j }$ sends a NextR_msg to the other nodes in $N _ { f a i l }$ . If no redundant nodes are found among its neighbors, $u _ { j }$ sends a NoR_msg. When $u _ { i }$ receives a $N e x t R \_ m s g .$ , it evaluates the weights of the nodes that have sent the message and selects the node with smallest weight as the relocated node. On the contrary, if $u _ { i }$ only receives $N o R \_ m s g .$ , the node with the smallest weight in $N _ { f a i l }$ is taken as the relocated node. Note that the relocated node should set its isMove status flag to 1 to prevent the cyclic movements (e.g., ua prompts $u _ { b }$ to be relocated, and then $u _ { b }$ prompts $u _ { a }$ to be relocated). The above steps repeat until a redundant node is selected, and then the redundant node broadcasts a F inish_msg to finish the topology recovery.

<!-- image-->  
Fig. 7. A sequential diagram example of message exchanges in RTRA.

<!-- image-->  
Fig. 8. A sequential diagram example of message exchanges in CRTRA.

<!-- image-->  
Fig. 9. Topology recovery in extreme case where massive UAVs fail.

## D. Extreme Case of CRTRA

Note that in DLES missions, the following scenario may occur: some external events such as electromagnetic interference could cause the failures of many UAVs, leading to the serious topology partition of UAV swarm, which significantly affects the performance of DLES missions.

In such case, the ground station is needed to maintain the topology connectivity among different partitions, as shown in Fig. 9. When a node detects the loss of heartbeat messages from a large number of neighbors, it initiates a topology partition detection process. The node sends an enquire_msg to the ground station and broadcasts an occupy_msg within the partition (the node belongs to this partition) to prevent other nodes in the same partition from sending enquire_msgs to the ground station. If the ground station does not receive other enquire_msgs during ts time slots, it sends back a deny_msg to $u _ { i } .$ . Conversely, multiple enquire_msgs indicate that a partition has occurred in the UAV swarm. Then, the ground station sends an aff irm_msg to $u _ { i } ,$ containing the positions of the nodes in other partitions. Upon receiving an aff irm_msg, the nodes within each partition continue to maintain the local connectivity (the connectivity in each partition) while executing CRTRA to recover the topology connectivity.

Specifically, if different partitions can be bridged by a small number of UAVs, the ground station constructs a minimum spanning tree and selects several redundant UAVs to recover the topology connectivity. On the contrary, if these partitions cannot be bridged due to severe topology damage, the ground station instructs UAVs from different partitions to converge spatially and reconstruct the topology of UAV swarm.

## V. THEORETICAL ANALYSIS

## A. Communication Complexity

As analyzed in [38], CAM has the communication complexity of $O ( N )$ for detecting the cut vertices. For the determination of redundant nodes, each redundant node candidate could send some explore messages to the neighbors to identify the communication paths between neighbors. The worst case occurs when a communication path that passes all N nodes in UAV swarm is found with no common nodes, requiring a cut vertex determination for each node. Therefore, the communication complexity of determining the redundant nodes is of $O ( N ^ { 2 } )$ , ( )and the communication complexity of node classification in the worst case is of $O ( N ^ { 2 } )$ as well. Furthermore, in RTRA, ( )the topology recovery is launched when a UAV fails, each cut vertex first broadcasts a cut vertex declaration message to obtain $p _ { f a i l }$ (also denoted by $p _ { t a r } )$ . After that, the cut vertices send the request messages to their neighbors. Upon receiving the request messages, each redundant node sends a respond message back to the cut vertex with the largest ID, and then this cut vertex relocates a redundant node. After that, the redundant node sends a confirmation message back to the cut vertex. Thus, in the worst case, a total of N messages will be sent, and the total (3 + 2)communication complexity of RTRA is of $O ( N ^ { 2 } )$ .

( )Additionally, CRTRA introduces a cascading movement strategy, after each cut vertex initially broadcasts a request message, the nodes in $N _ { f a i l }$ perform the topology recovery based on the local topology consisting of the neighbors (one-hop neighbors) and two-hop neighbors. Generally, each neighbor of $u _ { f a i l }$ needs to send messages to other nodes in $N _ { f a i l }$ , with a communication complexity of $O ( c ^ { 2 } )$ , where c denotes the number of neighbors. ( )In the worst case, the communication complexity of a topology recovery in UAV swarm is of $O ( c ^ { 2 \sim } N )$ . Typically c is much smaller than N, and therefore CRTRA has a total communication complexity of $O ( N ^ { 2 } )$ .

## B. Flight Distance

In this section, we analyze the flight distance of UAV swarm required for each topology recovery. Specially, we also verify that the proposed algorithms RTRA and CRTRA can successfully eliminate the cut vertices.

Proposition 1: Both RTRA and CRTRA can eliminate the cut vertices in UAV swarm and guarantee that each topology recovery can be finished in limited time.

Proof: Since the failure of $u _ { f a i l }$ results in some new cut vertices, a redundant node is selected as a relocated node if more cut vertices will not be produced when it moves to the position $p _ { f a i l }$ , and the relocation mechanism can successfully eliminate the cut vertices. Additionally, in CRTRA, we set an isMove status flag to prevent the cyclic movements, thus ensuring that each relocated node moves only once. Therefore, both RTRA and CRTRA guarantee that each topology recovery can be finished in limited time. 

In CRTRA, each node exploits the local topology. The optimal solution (a centralized decision approach) would exploit the global topology consisting of all nodes and then can select a set of relocated nodes and minimize the total flight distance.

Proposition 2: In CRTRA, the maximum flight distance for the relocation of a single node is R.

Proof: Since a failed node could be replaced by one of the neighbors, the maximum flight distance in the worst case is equal to the communication range of UAVs (i.e. R).

<!-- image-->  
Fig. 10. Worst Case in CRTRA.

Proposition 3: In the worst case, the total flight distance of relocated UAVs in CRTRA is $( N - 6 ) R ,$ , and the approximation ratio to the optimal solution is $\frac { 4 ( N - 6 ) } { ( N - 2 ) }$

Proof. One worst case for the total flight distance of relocated UAVs in CRTRA is depicted in Fig. 10. In Fig. 10, $u _ { 1 }$ and uN $( N { > } 6 )$ are redundant nodes, and the failures of any other nodes would result in new cut vertices. Considering the failure of $u _ { 6 }$ the nodes in $N _ { f a i l }$ can only receive NoR_msg. u7 is relocated to the position of $u _ { 6 }$ . The topology recovery process involves each node (from $u _ { 7 }$ to $u _ { N } )$ moving to the position of the node immediately preceding it, concluding with $u _ { N }$ being relocated to the position of $u _ { N - 1 }$ . The total flight distance in this case is written as: $\begin{array} { r } { \sum _ { i = 6 } ^ { N } R = ( N - 6 ) R } \end{array}$

= ( 6)For the optimal solution, the worst case occurs when a node $( u _ { m } ,$ which is located in the middle of the topology) fails, i.e., m $\begin{array} { r l } { \mathrm { ~ } } & { { } = \frac { N } { 2 } } \end{array}$ . When m is even, the optimal topology recovery process would involve each node (from $u _ { m + 2 } \ \mathrm { t o } \ u _ { N } )$ moving to the position of the node immediately preceding it, concluding with uN moving to the position of $u _ { N - 2 }$ . Thus, the total flight distance is expressed as: $\begin{array} { r } { \big ( \frac { \hat { N } - m } { 2 } \big ) R = \big ( \frac { N } { 4 } \big ) R } \end{array}$ . As for m is odd, the optimal topology recovery process involves each node (from $u _ { m - 2 }$ to $u _ { 1 } )$ moving to the position of the node immediately preceding it, concluding with $u _ { 3 }$ moving to the position of $u _ { 1 }$ . Then, the total flight distance is expressed as: $\begin{array} { r } { ( \frac { \bar { m } - 1 } { 2 } ) R = ( \frac { { N } - 2 } { 4 } ) R } \end{array}$

( ) = ( )Therefore, in the worst case, the approximation ratio of the total flight distance of relocated UAVs between CRTRA and the optimal solution is written as: $\begin{array} { r } { \frac { ( N - 6 ) R } { ( \frac { N - 2 } { 4 } ) R } = \frac { 4 ( N - 6 ) } { ( N - 2 ) } } \end{array}$ . 

Proposition 4: The worst-case time complexity of CRTRA is $O ( \frac { \tilde { (} N - 6 ) R } { v } )$ (v is the flight speed of UAVs).

Proof: According to Proposition 3, in the worst case, the total flight distance of the relocated UAVs in CRTRA is written as $( N - 6 ) R$ . Notice that communication delay in UAV swarm ( 6)is typically small. Therefore, the time consumed for messages exchanges is negligible compared to the movement time of relocated UAVs [42]. Assuming UAVs fly at a constant speed v, the worst-case time complexity of CRTRA is expressed as $O ( \frac { ( N - 6 ) R } { v } )$ 

## C. Algebraic Connectivity by Relocating Nodes

Since AC quantifies the strength of connections between nodes, this section analyzes the impacts of the node relocation on AC. We denote the Laplacian matrix of graph G as $L ,$ , and the second smallest eigenvalue of L as $\lambda _ { F } ,$ , which is also the AC of G. The eigenvector corresponding to $\lambda _ { F }$ is denoted by vF . For the eigenpair $( \lambda , \mathbf { v } )$ of L, there is ${ \cal L } { \bf v } = \lambda _ { F } { \bf v } .$ . Then, when the positions of relocated nodes in UAV swarm are altered, the following equation is satisfied according to [43]:

$$
( L + \Delta L ) ( \mathbf { v } + \Delta \mathbf { v } ) = ( \lambda + \Delta \lambda ) ( \mathbf { v } + \Delta \mathbf { v } ) ,\tag{7}
$$

where $\Delta L , \Delta \mathbf { v } ,$ , and $\Delta \lambda$ represent the changes of $L , \mathbf { v } ,$ and $\lambda$ Î Î Îrespectively. Consequently, the change of Î» can be expressed as:

$$
\Delta \lambda = \frac { \mathbf { v } ^ { T } \Delta L ( \mathbf { v } + \Delta \mathbf { v } ) } { \mathbf { v } ^ { T } ( \mathbf { v } + \Delta \mathbf { v } ) } .\tag{8}
$$

The Laplacian matrix of graph G is denoted by $L _ { i }$ after relocating the node $u _ { i } ,$ and $L _ { i }$ can be obtained by $L _ { i } = L + \Delta L _ { i } ,$ where $\Delta L _ { i }$ = + Îdenotes the change in the Laplacian matrix after Îrelocating $u _ { i } .$ . Substituting $L _ { i }$ into (8), and the change of $\Delta \lambda _ { F }$ is expressed as:

$$
\Delta \lambda _ { F } = \frac { \mathbf { v } _ { F } ^ { T } \Delta L _ { i } \mathbf { v } _ { F , i } } { \mathbf { v } _ { F } ^ { T } \mathbf { v } _ { F , i } } ,\tag{9}
$$

where ${ \bf v } _ { F , i }$ denoted the obtained eigenvector after relocating $u _ { i }$ In practical applications, we can select the appropriate nodes to move to target positions (i.e., relocate the appropriate nodes), ensuring that $\Delta L _ { i }$ in the Laplacian matrix of graph G is positive, Îthereby increasing the AC of UAV swarm and enhance the topology robustness.

Furthermore, in (9), ${ \bf v } _ { F , i }$ can be calculated by ${ \bf v } _ { F , i } = { \bf v } _ { F } + { \bf \Delta }$ $\partial { \bf v } _ { F , i }$ , and it is evident that the i-th element of $\partial { \bf v } _ { F , i }$ = +is equal to 0. Then, $\partial { \bf v } _ { F , i }$ is rewritten as:

$$
\begin{array} { r } { \partial { \bf v } _ { F , i } = \delta { \bf v } _ { F } - v _ { F , i } { \bf e } _ { i } , } \end{array}\tag{10}
$$

where $\delta \mathbf { v } _ { F }$ is an n-dimensional vector where the elements are quite small compared with that in ${ \bf V } _ { F , i } . \mathrm { ~ } v _ { F , i }$ is the i-th element of $\mathbf { v } _ { F }$ and $\mathbf { e } _ { i }$ is a unit vector with its i-th element being 1. By ignoring $\delta { \bf v } _ { F } , { \bf v } _ { F , i }$ can be expressed as:

$$
\mathbf { v } _ { F , i } = \mathbf { v } _ { F } - v _ { F , i } \mathbf { e } _ { i } .\tag{11}
$$

Additionally, we define the following matrix:

$$
W _ { i } = I - \eta L _ { i } - \frac { \mathbf { 1 1 } ^ { T } } { N } - \mathbf { e } _ { i } \mathbf { e } _ { i } ^ { T } ,\tag{12}
$$

where I represents the n-dimensional identity matrix, 1 denotes a vector with all its elements equal to 1. Î· is an appropriate value to ensure that ${ \bf v } _ { F , i }$ is the dominant eigenvector of $W _ { i }$ , thereby the corresponding eigenvalue is $1 - \eta \lambda _ { F , i }$ [21]. Then, ${ \bf v } _ { F , i }$ is obtained by:

$$
{ \bf v } _ { F , i } = W _ { i } \left( { \bf v } _ { F } - v _ { F , i } { \bf e } _ { i } \right) .\tag{13}
$$

Consequently, the change of $\Delta \lambda _ { F }$ caused by the relocation of $u _ { i }$ is further expressed as:

$$
\begin{array} { r l } & { \Delta \lambda _ { F } = \frac { \mathbf { v } _ { F } ^ { T } \Delta L _ { i } \mathbf { v } _ { F , i } } { \mathbf { v } _ { F } ^ { T } \mathbf { v } _ { F , i } } } \\ & { \qquad = \frac { \mathbf { v } _ { F } ^ { T } \Delta L _ { i } \left( I - \eta L _ { i } - \frac { 1 \mathbf { 1 } ^ { T } } { N } - \mathbf { e } _ { i } \mathbf { e } _ { i } ^ { T } \right) \left( \mathbf { v } _ { F } - v _ { F , i } \mathbf { e } _ { i } \right) } { \mathbf { v } _ { F } ^ { T } \left( I - \eta L _ { i } - \frac { 1 \mathbf { 1 } ^ { T } } { N } - \mathbf { e } _ { i } \mathbf { e } _ { i } ^ { T } \right) \left( \mathbf { v } _ { F } - v _ { F , i } \mathbf { e } _ { i } \right) } } \\ & { \qquad = \frac { ( 1 - \eta \lambda _ { F } ) \mathbf { v } _ { F } ^ { T } \Delta L _ { i } \mathbf { v } _ { F } - \eta \mathbf { v } _ { F } ^ { T } \Delta L _ { i } ^ { 2 } \mathbf { v } _ { F } - \Delta L _ { i } v _ { F , i } ^ { 2 } } { ( 1 - \eta \lambda _ { F } ) \mathbf { v } _ { F } ^ { T } \mathbf { v } _ { F } - \eta \mathbf { v } _ { F } ^ { T } \Delta L _ { i } \mathbf { v } _ { F } - v _ { F , i } ^ { 2 } } , } \end{array}\tag{14}
$$

where $\mathbf { v } _ { F } , \lambda _ { F } ,$ , and Î· are determined by the topology of UAV swarm after UAV failures, and the value of Î· falls into the interval $( 0 , \textstyle { \frac { 1 } { \lambda _ { F } } } ]$ , as described in [43]. In (14), there can be $\begin{array} { r } { \eta = \frac { 1 } { \lambda _ { F } } } \end{array}$ , and then the value of $( 1 - \eta \lambda _ { F } )$ in both numerator = (1 )and denominator is equal to 0. In this case, (14) is rewritten as $\begin{array} { r } { \Delta \lambda _ { F } = \frac { \mathbf { v } _ { F } ^ { T } \Delta L _ { i } ^ { 2 } \mathbf { v } _ { F } + \lambda _ { F } \mathbf { \dot { \Delta } } \Delta L _ { i } v _ { F , i } ^ { 2 } } { \mathbf { v } _ { F } ^ { T } \Delta L _ { i } \mathbf { v } _ { F } + \lambda _ { F } v _ { F , i } ^ { 2 } } } \end{array}$ , indicating that selecting appropriate relocated nodes can make $\Delta L _ { i }$ positive, i.e, the algebraic Îconnectivity of UAV swarm is increased.

## VI. PERFORMANCE EVALUATIONS

In this section, we provide comprehensive performance evaluations of our proposed robust topology recovery algorithms, RTRA and CRATA. The performance evaluations are carried out using a simulator developed by Python language. In the following simulations, UAVs are assumed to deployed in an airspace with the size of $4 0 0 \ \mathrm { m } \times 4 0 0 \ \mathrm { m } \times 4 0 0 \ \mathrm { m } ,$ the communication range of each UAV is set to 20 meters. We assume that one UAV newly fails every 20 seconds, thus we set $T$ as the time period from the start of the DLES missions until the failures of a preset number of UAVs. The following simulations results are the average of the results from 100 simulation runs.

## A. Impacts of Î± and Î²

In RTRA and CRATA, before selecting the appropriate relocated nodes, the redundant nodes calculate their weights according to (2). Thus, it is essential to properly set the values of the parameters Î± and $\beta$ in (2) to ensure that the weight calculation is reasonable. First, 100 UAVs are deployed in the airspace, and 60 UAVs are assumed to fail sequentially. By varying the values of Î± and $\beta ,$ we observe the performance variation in terms of average flight distance of topology recoveries (the average flight distance is obtained as the average flight distance of relocated UAVs required by a topology recovery during the future time period of T ) and average increase in algebraic connectivity. The simulation results are shown in Fig. 11.

Fig. 11 illustrates the variation of the average flight distance of UAVs under different values of Î± and $\beta .$ It is evident that with the increase of Î± or the decrease of $\beta ,$ the average flight distance decreases (Fig. 11(a)), also indicating that the electricity consumption spent on the flight movements is reduced. This is because according to (2), an increase in Î± or a decrease in $\beta$ makes the flight distance of each relocated node become more important in setting the weight. On the contrary, a decrease in Î± or an increase in $\beta$ makes AC (topology robustness) become more important in setting the weight. Consequently, a preferable tradeoff between the reduction of flight distance and enhancement of topology robustness can be made by properly setting the values of Î± and $\beta .$ In the following simulations, Î± and $\beta$ are set to 5 and 3, respectively.

## B. Effect of Initial Topology

Since the sphere shape cannot fill three-dimensional airspace without gaps, we model the occupied space of UAVs as Truncated Octahedra (TO), with each UAV located at the center of a TO. Multiple TOs are closely packed together to form the initial topology of UAV swarm. In this initial topology, the maximum number of neighbors for each UAV is 14. Ref. [44] has demonstrated the superiority of TO by comparing the volumetric quotients of several common polyhedra.

<!-- image-->

(a)Average flight distance of topology recoveries  
<!-- image-->  
(b)Average increase in algebraic connectivity

Fig. 11. Impacts of Î± and $\beta .$  
<!-- image-->  
Fig. 12. Effect of initial topology.

To validate performance of the initial topology, we first compare RTRA and CRATA with LINAR [11], E-CDS [10], PADRA [19], and DQMAN [45], which also take TO as the occupied space. Specially, LINAR-R, E-CDS-R, PADRA-R, and DQMAN-R form the initial topology by randomly placing nodes. The topology recoveries during the future time period of $T$ are counted to obtain the average number of topology recoveries.

As shown in Fig. 12, the initial topology constructed by TOs helps to reduce the average number of topology recoveries compared with the random topology, indicating that the enhanced topology robustness can be achieved by carefully determining the initial positions of UAVs. This is because TO structure can maintain the local connectivity as much as possible, thereby reducing the probability of future topology recoveries when some UAVs fail. However, as the number of failed UAV increases, the topology of UAV swarm is seriously impaired, and the distribution of UAVs becomes similar to the random topology.

## C. Comparisons Between RTRA and CRTRA

We observe the performance of RTRA, CRTRA, and C-CRTRA (centralized version of CRTRA) in terms of three metrics: average flight distance, average number of topology recoveries, and average time of topology recoveries, as shown in Fig. 13.

Fig. 13(a) indicates that the average flight distance increases with more failed UAVs. The curve of RTRA is the lowest among these curves, which is attributed to the following facts: (i) As more UAVs fail, the distribution of UAVs in UAV swarm becomes sparser, which accordingly increases the average flight distance of relocated UAVs. (ii) The relocated UAVs in RTRA move directly to the target positions, whereas the relocated UAVs in CRTRA and C-CRTRA perform the cascading movements, and thus some additional flight movements could be produced. However, in the practical DLES missions, as the number of failed UAV increases, RTRA may encounter the following situation: a relocated UAV could undertake a long-distance flight to complete the topology recovery, which causes the battery electricity exhaustion of some relocated UAV. Note that the average flight distance of C-CRTRA is longer than that of CRTRA, because the centralized algorithm can identify a series of more suitable relocated UAVs to conduct the topology recovery and enhance the algebraic connectivity of UAV swarm. Therefore, C-CRTRA obtains the smallest number of topology recoveries (Fig. 13(b)).

In Fig. 13(b), as the number of failed UAVs increases, the probability of topology recoveries of CRTRA is smaller than that of RTRA, since CRTRA adopts a cascading movement strategy, allowing multiple UAVs to participate in the topology recoveries, thereby it enhances the topology robustness by sharing the flight movements among multiply relocated UAVs and avoiding the battery electricity exhaustion of the relocated UAVs. In addition, we compare the average time of topology recoveries, where the recovery time is defined as the period from a cut vertex broadcasts a request message to it receives the F inish_msgs from other UAVs. This process includes the selection of relocated UAVs and the relocation of UAVs (relocated UAVs move to the target positions). In Fig. 13(c), RTRA achieves the shortest recovery time because only one redundant node is relocated for each topology recovery. Furthermore, in C-CRTRA UAVs must exchange a large amount of messages to determine the optimal relocated UAVs and flight movements, hence C-CRTRA obtains the longest recovery time. Note that C-CRTRA is not feasible for the practical DLES missions due to the large communication overhead and long recovery delay. Moreover, the gap between RTRA and CRTRA in terms of average time of topology recoveries is narrowed with the increased number of failed UAVs, implying that CRTRA also has preferable scalability.

<!-- image-->  
(aï¼ Average flight distance of topology recoveries

<!-- image-->  
(bï¼Average number of topology recoveries

<!-- image-->  
(cï¼Average time of topology recoveries  
Fig. 13. Comparisons between RTRA and CRTRA.

Therefore, the simulation results provided in Fig. 13 indicate that: RTRA performs better when the number of failed UAV is very small, and CRTRA is more suitable for DLES missions with more failed UAVs.

We conduct more simulations where the number of UAV failures during each second is assumed to follow a Poisson distribution with Î» . [46], thereby simulating the inherent = 0 05randomness of UAV failures happening in real-world scenarios. The simulation results, presented in Fig. 14, demonstrate that the regularities in these outcomes are basically the same with those obtained when UAVs are assumed to fail at fixed time intervals. Additionally, to evaluate the performance of RTRA and CRTRA under consecutive UAV failures, we assume that a new UAV fails every 5 seconds, and the average flight distance and average number of topology recoveries are illustrated in Fig. 15. It can be observed that our proposed algorithms can still effectively complete the topology recoveries under the condition of consecutive UAV failures.

<!-- image-->  
Fig. 14. Performance of RTRA and CRTRA (UAV failures follow a probabilistic distribution).

<!-- image-->  
Fig. 15. Performance of RTRA and CRTRA under consecutive UAV failures.

## D. Energy Consumption on Flights Movements

The topology recovery is launched when a UAV fails, the relocated UAVs calculate their flight speeds that minimize the electricity consumption according to the following equation and move to the obtained target positions. UAV propulsion power [36] is expressed as:

$$
P = P _ { 0 } \left( 1 + \frac { 3 V ^ { 2 } } { U _ { t i p } ^ { 2 } } \right) + P _ { 1 } \left( \sqrt { 1 + \frac { V ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { V ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) + \frac { 1 } { 2 } d _ { f } \rho s A V ^ { 3 } ,\tag{15}
$$

where $P$ and V represent the electricity consumption and flight speed of a relocated UAV, respectively. $P _ { 0 }$ and $P _ { 1 }$ denote the fixed blade and induced powers for hovering, $U _ { t i p }$ is the rotor tip velocity, $v _ { 0 }$ is the mean rotor velocity at hover, $d _ { f }$ represents the fuselage drag fraction, and s is the rotor solidity. $\rho$ and A are the gaseous density and rotor disc area, respectively.

We conduct some simulations regarding the energy consumption for flight movements of RTRA and CRTRA, and the simulation results are given in Fig. 16. Table I shows the parameter settings. From Fig. 16, it can be observed that CRTRA effectively reduces the number of topology recoveries, thereby resulting in lower electricity consumption compared to RTRA.

<!-- image-->  
Fig. 16. Electricity consumption on flight movements for topology recoveries.

TABLE I  
PARAMETER SETTINGS OF UAV PROPULSION POWER
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Fixed blade power, $\overline { { P _ { 0 } } }$ </td><td rowspan=1 colspan=1>3.4W</td></tr><tr><td rowspan=1 colspan=1>Induced power, $\overline { { P _ { 1 } } }$ </td><td rowspan=1 colspan=1>118W</td></tr><tr><td rowspan=1 colspan=1>Rotor tip velocity, $\overline { { U _ { t i p } } }$ </td><td rowspan=1 colspan=1>60 m/s</td></tr><tr><td rowspan=1 colspan=1>Mean rotor velocity, vo</td><td rowspan=1 colspan=1>5.4 m/s</td></tr><tr><td rowspan=1 colspan=1>Fuselage drag fraction, $\overline { { d _ { f } } }$ </td><td rowspan=1 colspan=1>0.3</td></tr><tr><td rowspan=1 colspan=1>Rotor solidity, s</td><td rowspan=1 colspan=1>0.02</td></tr><tr><td rowspan=1 colspan=1>Gaseous density, $\underline { { \boldsymbol { \rho } } }$ </td><td rowspan=1 colspan=1> $1 . 2 2 5 ~ \mathrm { k g / m ^ { 3 } }$ </td></tr><tr><td rowspan=1 colspan=1>Rotor disc area, $\overline { { A } }$ </td><td rowspan=1 colspan=1> $\overline { { 0 . 5 \mathrm { ~ m } ^ { 2 } } }$ </td></tr></table>

## E. Comparisons With Related Works

To verify the merits of RTRA and CRTRA, we compare them with PADRA, LINAR, E-CDS and DQMAN. PADRA is selected as a classical topology recovery algorithm. LINAR is included as a new distributed algorithm that preserves kconnectivity with minimal movement and communication overhead. E-CDS is chosen for its representative use of connected dominating sets to perform the topology recovery. DQMAN is taken as a deep reinforcement learningâbased method for UAV swarm topology recovery. Both RTRA and CRTRA obtain superior results and outperform the other algorithms, in terms of average flight distance of topology recoveries (Fig. 17), average number of topology recoveries (Fig. 18), and average success rate of topology recoveries (Fig. 19).

To observe and compare the topology recovery effect of different algorithms on the UAV swarm with different number of UAVs, we perform the evaluations in UAV swarm consisting of 50 UAVs, 100 UAVs, and 150 UAVs, respectively, and at most 80% of UAVs are assumed to fail sequentially. As shown in Fig. 17, although PADRA outperforms our proposed algorithms in terms of the average flight distance of topology recoveries by specially focusing on the flight distance, it results in the largest average number of topology recoveries (the topology robustness is not satisfactory). Nevertheless, both RTRA and CRTRA perform better than LINAR, E-CDS, and DQMAN, because LINAR aims to balance the topology connectivity and topology coverage which is measured on a two-dimensional plane, and E-CDS focuses on the communication architecture of UAV swarm to optimize some metrics such as end to end delay. In addition, DQMAN primarily considers the backhaul capacity of the UAV swarm, emphasizing the minimization of the backhaul distance between UAV swarms and the ground station.

<!-- image-->  
Comparisons under N = 50

<!-- image-->  
Comparisons under N = 100

<!-- image-->  
Comparisons under N = 150

Fig. 17. Average flight distance of topology recoveries.  
<!-- image-->  
Comparisons under N = 50

<!-- image-->  
Comparisons under N = 100

<!-- image-->  
Comparisons under N = 150

Fig. 18. Average number of topology recoveries.  
<!-- image-->  
Comparisons under N = 50

<!-- image-->  
Comparisons under N = 100

<!-- image-->  
Comparisons under N = 150  
Fig. 19. Average success rate of topology recoveries.

Fig. 18 compares the average number of topology recoveries under different numbers of UAVs. Since both RTRA and CRTRA incorporate the algebraic connectivity to enhance the topology robustness and reduce the number of potential topology recoveries as much as possible, they achieve satisfactory results in terms of the average number of topology recoveries. Note that when the number of failed UAVs becomes large (especially larger than $\textstyle { \frac { N } { 2 } } )$ , LINAR requires fewer topology recoveries than RTRA and

CRTRA. However, as the number of failed UAVs grows, the total flight distance required for each topology recovery in LINAR is prolonged significantly.

During the execution of DLES missions, when some UAVs fail, the topology connectivity could be irreparable. Therefore, we observe the average success rate of topology recoveries of these algorithms. As shown in Fig. 19, when $N = 5 0$ , after =80% of UAVs fail, the number of surviving UAVs is very small, making the topology quite fragile, and thus the average success rate of most algorithms is smaller than 95% (Fig. 19(a)). Note that DQMAN achieves a recovery success rate of 100%, as it is based on deep reinforcement learning, allowing UAVs to autonomously relocate and recover the topology connectivity. In contrast, when $N = 1 5 0$ , there are enough surviving UAVs (even =though 80% of UAVs fail) to maintain the topology connectivity, enabling all algorithms can recover the topology connectivity successfully (Fig. 19(c)).

<!-- image-->  
(a) Average number of signal-detecting UAVs

<!-- image-->  
(b)RMSE of DLES missions  
Fig. 20. Performance comparisons among different algorithms of DLES missions.

## F. Performance Comparisons of DLES Missions

To analyze the merits of our proposed RTRA and CRTRA in DLES missions, we compared RTRA and CRTRA with other algorithms by observing the performance of DLES missions. First, the signal strength is measured by [47]: $f ( p _ { i } ) =$ $\left\{ \begin{array} { l l } { W - { \check { d } } ( \frac { W } { r } ) , } & { \mathrm { i f } \check { d } \leq r } \\ { 0 , } & { \mathrm { i f } \check { d } > r } \end{array} \right.$ , where W denotes the maximum sig-0nal strength at the signal source, r denotes the maximum propagation distance after attenuation, and d denotes the distance from the UAV to the signal source. Considering the impact of noise on the received signal strength, the actual signal strength received by the i-th UAV in UAV swarm is calculated by: $\begin{array} { r } { f ( u _ { i } ) = \operatorname* { m a x } \{ 0 , ( W - \check { d } ( \frac { W } { r } ) + X _ { \delta } ) \} } \end{array}$ , where $X _ { \delta }$ is a random ( ) = max 0 ( ( ) + )variable with a mean of 0 and a standard deviation of Î´. For the convenience, we set the signal detection range of each UAV equal to the communication range, and if the signal strength detected by a UAV is greater than zero, the UAV is considered to have detected the electronic signal.

When multiple UAVs in UAV swarm detect the same electronic signal, the UAV with the largest ID adopts the least squares method to compute the location of the signal source. The maximum signal strength W is set to 200 mW, and the maximum propagation distance r is set to 200 m. The comparison results are illustrated in Fig. 20, which indicates that the average number of signal-detecting UAVs is almost linearly decreased with the increase of the number of failed UAVs. Specially, LINAR performs the best (the average number of signal-detecting UAVs is the largest) among these algorithm due to the emphasis on the topology coverage.

We assess the accuracy of electronic signal localization using the root mean square error (RMSE) between the detected signal locations and true signal locations, a smaller RMSE indicates more accurate detection and localization of electronic signals. Specifically, in Fig. 20(b), PADRA, E-CDS, and DQMAN yield larger RMSE when the number of failed UAVs is larger than 50, and the three curves have some drastic fluctuations, due to the fact that the electronic signal could not be effectively detected and localized by them when there are more failed UAVs, which tallies with the aforementioned phenomena, i.e., PADRA and DQMAN must conduct larger average number of topology recoveries (Fig. 18), and E-CDS has the worst average success rate of topology recoveries (Fig. 19). In contrast, the RMSE of RTRA and CRTRA is better, and the curve fluctuations are much slighter, because they can effectively recover the topology connectivity of UAV swarm.

## VII. CONCLUSION

In this paper, we have studied the robust topology recovery of UAV swarm for the detection and localization of electronic signals. we first propose Robust Topology Recovery Algorithm of UAV swarm (RTRA) to recover the topology connectivity of UAV swarm and enhance the topology robustness by relocating some UAVs to new positions with shortest flight distance. Furthermore, we present Cascading Robust Recovery Topology Algorithm of UAV swarm (CRTRA), which adopts a cascading movement strategy to share the flight movements among multiply relocated UAVs, thus avoiding the battery electricity exhaustion of the relocated UAVs, and the topology robustness can be further enhanced.

RTRA achieves the shorter flight distance and recovery time in the topology recoveries, and CRTRA achieves the better topology robustness. Hence, RTRA performs better when the number of failed UAV is very small, and CRTRA is more suitable for the DLES missions with large proportion of failed UAVs.

In practical DLES missions, the mission coverage of UAV swarm is also crucial. A larger mission coverage can enhance the performance of DLES missions and reduce the mission delays. Furthermore, the performance of UAV swarm in dynamic environments, such as those involving moving obstacles, also deserves further investigation. Therefore, we will extend the proposed algorithms in future work to evaluate their adaptability and robustness in dynamic environments.

## REFERENCES

[1] B. Alzahrani et al., âUAV assistance paradigm: State-of-the-art in applications and challenges,â J. Netw. Comput. Appl., vol. 166, 2020, Art. no. 102706.

[2] Z. Wei et al., âUAV-assisted data collection for Internet of Things: A survey,â IEEE Internet Things J., vol. 9, no. 17, pp. 15460â15483, Sep. 2022.

[3] S. Javed et al., âState-of-the-art and future research challenges in UAV swarms,â IEEE Internet Things J., vol. 11, no. 11, pp. 19023â19045, Jun. 2024.

[4] P. Chi et al., âA bio-inspired decision-making method of UAV swarm for attack-defense confrontation via multi-agent reinforcement learning,â Biomimetics, vol. 8, no. 2, 2023, Art. no. 222.

[5] J. Milewski, R. Urban, K. Wilgucki, and P. Gr Ëadzki, âDetection, direction finding and localization of selected radio emissions with swarm technology,â in Proc. 12th Conf. Reconnaissance Electron. Warfare Syst., 2019, pp. 431â439.

[6] B. E. Tegicho, T. E. Bogale, A. Eroglu, Z. Xie, and W. Edmonson, âIntra-UAV swarm connectivity in unstable environment,â IEEE Trans. Veh. Technol, vol. 72, no. 11, pp. 13929â13939, Nov. 2023.

[7] B. E. Tegicho, T. E. Bogale, A. Eroglu, and W. Edmonson, âConnectivity and safety analysis of large scale UAV swarms: Based on flight scheduling,â in Proc. IEEE 26th Int. Workshop Comput. Aided Model. Des. Commun. Links Netw., 2021, pp. 1â6.

[8] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[9] N. Lin, H. Tang, L. Zhao, S. Wan, A. Hawbani, and M. Guizani, âA PDDQNLP algorithm for energy efficient computation offloading in UAV-assisted MEC,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8876â8890, Dec. 2023.

[10] A. Kurt, N. Saputro, K. Akkaya, and A. S. Uluagac, âDistributed connectivity maintenance in swarm of drones during post-disaster transportation applications,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 9, pp. 6061â6073, Sep. 2021.

[11] V. K. Akram, O. Dagdeviren, and B. TavlÄ±, âA coverage-aware distributed k-connectivity maintenance algorithm for arbitrarily large k in mobile sensor networks,â IEEE/ACM Trans. Netw., vol. 30, no. 1, pp. 62â75, Feb. 2022.

[12] S. Xiong and J. Li, âAn efficient algorithm for cut vertex detection in wireless sensor networks,â in Proc. IEEE 30th Int. Conf. Distrib. Comput. Syst., 2010, pp. 368â377.

[13] O. Dagdeviren, V. K. Akram, and A. Farzan, âA distributed evolutionary algorithm for detecting minimum vertex cuts for wireless ad hoc and sensor networks,â J. Netw. Comput. Appl., vol. 127, pp. 70â81, 2019.

[14] Z. A. Dagdeviren, âA metaheuristic algorithm for vertex cover based link monitoring and backbone formation in wireless ad hoc networks,â Expert Syst. Appl., vol. 213, 2023, Art. no. 118919.

[15] G. Khayat, C. X. Mavromoustakis, A. Pitsillides, J. M. Batalla, and E. K. Markakis, âRedundant weighted clustered scheme with dynamic weights adjustment for damaged S-UAV,â in Proc. IEEE Int. Conf. Commun., 2024, pp. 3371â3376.

[16] T. Musil, M. PetrlÃ­k, and M. Saska, âSphereMap: Dynamic multi-layer graph structure for rapid safety-aware UAV planning,â IEEE Trans. Robot. Autom., vol. 7, no. 4, pp. 11007â11014, Oct. 2022.

[17] M. Wang and C. Zhai, âNode collaborative sensing-based redundant path construction for multiarea coverage in MWSNs,â IEEE Internet Things J., vol. 9, no. 11, pp. 8763â8773, Jun. 2022.

[18] E. O. Rangel, D. G. Costa, and A. Loula, âOn redundant coverage maximization in wireless visual sensor networks: Evolutionary algorithms for multi-objective optimization,â Appl. Soft Comput., vol. 82, 2019, Art. no. 105578.

[19] K. Akkaya, F. Senel, A. Thimmapuram, and S. Uludag, âDistributed recovery from network partitioning in movable sensor/actor networks via controlled mobility,â IEEE Trans. Comput., vol. 59, no. 2, pp. 258â271, Feb. 2010.

[20] X. Qi, P. Yuan, Q. Zhang, and Z. Yang, âCDS-based topology control in FANETs via power and position optimization,â IEEE Wireless Commun. Lett., vol. 9, no. 12, pp. 2015â2019, Dec. 2020.

[21] C. Liu and Z. Zhang, âTowards a robust FANET: Distributed node importance estimation-based connectivity maintenance for UAV swarms,â Ad Hoc Netw., vol. 125, 2022, Art. no. 102734.

[22] L. Zhang, Y. Du, J. Xu, and X. Wang, âUAV-enabled IoT: Cascading failure model and topology-control-based recovery scheme,â IEEE Internet Things J., vol. 11, no. 12, pp. 22562â22577, Jun. 2024.

[23] Z. Pan, J. Feng, T. T. Yu, B. Cui, and Y. Xia, âDistributed recursive grouping based fault self-healing of UAV swarm with individuals failure,â IEEE Trans. Aerosp. Electron. Syst., vol. 61, no. 2, pp. 2996â3008, Apr. 2025.

[24] S. Wang, X. Mao, S.-J. Tang, X. Li, J. Zhao, and G. Dai, âOn âmovementassisted connectivity restoration in wireless sensor and actor networksâ,â IEEE Trans. Parallel Distrib. Syst., vol. 22, no. 4, pp. 687â694, Apr. 2011.

[25] V. K. Akram et al., âPINC: Pickup non-critical node based k-connectivity restoration in wireless sensor networks,â Sensors, vol. 21, no. 19, 2021, Art. no. 6418.

[26] M. Tosun, U. C. Cabuk, E. Haytaoglu, O. Dagdeviren, and Y. Ozturk, âDPkCR: Distributed proactive k-connectivity recovery algorithm for UAV-Based MANETs,â IEEE Trans. Rel., vol. 73, no. 4, pp. 1918â1932, Dec. 2024.

[27] Y. Zeng, L. Xu, and Z. Chen, âFault-tolerant algorithms for connectivity restoration in wireless sensor networks,â Sensors, vol. 16, no. 1, 2015, Art. no. 3.

[28] V. K. Akram, O. Dagdeviren, and B. Tavli, âDistributed k-connectivity restoration for fault-tolerant wireless sensor and actuator networks: Algorithm design and experimental evaluations,â IEEE Trans. Rel., vol. 70, no. 3, pp. 1112â1125, Sep. 2021.

[29] J. Zheng, T. Yang, H. Liu, T. Su, and L. Wan, âAccurate detection and localization of unmanned aerial vehicle swarms-enabled mobile edge computing system,â IEEE Trans. Ind. Inform., vol. 17, no. 7, pp. 5059â5067, Jul. 2021.

[30] Z. Shi, X. Chang, C. Yang, Z. Wu, and J. Wu, âAn acousticbased surveillance system for amateur drones detection and localization,â IEEE Trans. Veh. Technol, vol. 69, no. 3, pp. 2731â2739, Mar. 2020.

[31] S. Hu, W. Ni, X. Wang, A. Jamalipour, and D. Ta, âJoint optimization of trajectory, propulsion, and thrust powers for covert UAV-on-UAV video tracking and surveillance,â IEEE Trans. Inf. Forensics Secur., vol. 16, pp. 1959â1972, 2021.

[32] Q. Zhang et al., âE-Argus: Drones detection by side-channel signatures via electromagnetic radiation,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 11, pp. 18978â18991, Nov. 2024.

[33] J. A. Paredes et al., âA Gaussian process model for UAV localization using millimetre wave radar,â Expert Syst. Appl., vol. 185, 2021, Art. no. 115563.

[34] A. Sedunov, D. Haddad, H. Salloum, A. Sutin, N. Sedunov, and A. Yakubovskiy, âStevens drone detection acoustic system and experiments in acoustics UAV tracking,â in Proc. IEEE Int. Symp. Technol. Homeland Secur., 2019, pp. 1â7.

[35] J. Zheng et al., âAn efficient strategy for accurate detection and localization of UAV swarms,â IEEE Internet Things J., vol. 8, no. 20, pp. 15372â15381, Oct. 2021.

[36] S. Hu, X. Yuan, W. Ni, and X. Wang, âTrajectory planning of cellular-connected UAV for communication-assisted radar sensing,â IEEE Trans. Commun., vol. 70, no. 9, pp. 6385â6396, Sep. 2022.

[37] Y. Xie, P. Jiang, Y. Gu, and X. Xiao, âDual-source detection and identification system based on UAV radio frequency signal,â IEEE Trans. Instrum. Meas., vol. 70, 2021, Art. no. 2006215.

[38] X. Liu, L. Xiao, and A. Kreling, âA fully distributed method to detect and reduce cut vertices in large-scale overlay networks,â IEEE Trans. Comput., vol. 61, no. 7, pp. 969â985, Jul. 2012.

[39] Y. Kim, âBisection algorithm of increasing algebraic connectivity by adding an edge,â IEEE Trans. Autom. Control, vol. 55, no. 1, pp. 170â174, Jan. 2010.

[40] P. Di Lorenzo and S. Barbarossa, âDistributed estimation and control of algebraic connectivity over random graphs,â IEEE Trans. Signal Process., vol. 62, no. 21, pp. 5615â5628, Nov. 2014.

[41] Y. Zhang, S. Li, and J. Weng, âDistributed estimation of algebraic connectivity,â IEEE Trans. Cybern., vol. 52, no. 5, pp. 3047â3056, May 2022.

[42] Q. Zhang, J. Chen, L. Ji, Z. Feng, Z. Han, and Z. Chen, âResponse delay optimization in mobile edge computing enabled UAV swarm,â IEEE Trans. Veh. Technol, vol. 69, no. 3, pp. 3280â3295, Mar. 2020.

[43] H. Liu et al., âDistributed identification of the most critical node for average consensus,â IEEE Trans. Signal Process., vol. 63, no. 16, pp. 4315â4328, Aug. 2015.

[44] S. M. N. Alam and Z. J. Haas, âCoverage and connectivity in threedimensional networks,â in Proc. 12th Annu. Int. Conf. Mobile Comput. Netw., 2006, pp. 346â357.

[45] J. Zhang et al., âMulti-UAV collaborative surveillance network recovery via deep reinforcement learning,â IEEE Internet Things J., vol. 11, no. 21, pp. 34528â34540, Nov. 2024.

[46] Y. Peng et al., âLargest recoverable component based fault recoverability of UAV swarm with removal of faulty individuals,â Aerosp. Sci. Technol., vol. 118, 2021, Art. no. 107059.

[47] J. Zhang et al., âPSO-based sparse source location in large-scale environments with a UAV swarm,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 5, pp. 5249â5258, May 2023.

Linfeng Liu received the BS and PhD degrees in computer science from Southeast University, Nanjing, China, in 2003 and 2008, respectively. Currently, he is a professor with the School of Computer Science and Technology, the Nanjing University of Posts and Telecommunications, China. His research interests include deep learning, vehicular ad hoc networks, mobile computing, and multi-hop mobile wireless networks. He has published more than 150 peer-reviewed papers in prestigious journals and conferences, such as IEEE Transactions on Mobile Computing, IEEE Transactions on Knowledge and Data Engineering, IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Information Forensics and Security, IEEE Transactions on Intelligent Transportation Systems, IEEE Transactions on Affective Computing, IEEE Transactions on Vehicular Technology, IEEE Transactions on Services Computing, ACM Transactions on Autonomous and Adaptive Systems, ACM Transactions on Internet Technology, Computer Networks, and Elsevier Journal of Parallel and Distributed Computing. He has served as an editorial board member for Scientific Reports, and served as a TPC member for several conferences, including GlobeCom, ICONIP, SmartGridComm, VTC, and WCSP.

Wenzhe Zhang received the BS degree in information security from the Nanjing University of Posts and Telecommunications, in 2023, where he is currently working toward the MS degree in electronic information. His current research interest includes UAV networks and topological repair.

Xingyu Li received the BS degree in information security from the Nanjing University of Posts and Telecommunications, in 2023, where he is currently working toward the PhD degree in cyberspace security. His current research interest includes vehicular ad-hoc networks and UAV networks.

Jia Xu (Senior Member, IEEE) received the PhD degree from the School of Computer Science and Engineering from Nanjing University of Science and Technology, Jiangsu, China, in 2010. He is currently a professor with the Jiangsu Key Laboratory of Big Data Security and Intelligent Processing, Nanjing University of Posts and Telecommunications. His main research interests include crowdsourcing, edge computing and wireless sensor networks.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_2_img_2.png|page_2_img_2]]
3. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_4_img_1.jpeg|page_4_img_1]]
4. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_5_img_1.jpeg|page_5_img_1]]
5. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_5_img_2.jpeg|page_5_img_2]]
6. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_7_img_1.jpeg|page_7_img_1]]
7. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_7_img_2.jpeg|page_7_img_2]]
8. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_8_img_1.jpeg|page_8_img_1]]
9. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_9_img_1.jpeg|page_9_img_1]]
10. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_10_img_1.png|page_10_img_1]]
11. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_10_img_2.png|page_10_img_2]]
12. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_11_img_1.png|page_11_img_1]]
13. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_12_img_1.png|page_12_img_1]]
14. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_12_img_2.png|page_12_img_2]]
15. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_12_img_3.png|page_12_img_3]]
16. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_13_img_1.jpeg|page_13_img_1]]
17. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_13_img_2.jpeg|page_13_img_2]]
18. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_13_img_3.png|page_13_img_3]]
19. [[../extracted_images/Liu-2025-On the Robust Topology Recovery of UA/page_14_img_1.png|page_14_img_1]]

---

