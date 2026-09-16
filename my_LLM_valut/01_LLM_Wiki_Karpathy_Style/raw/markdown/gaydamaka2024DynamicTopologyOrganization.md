# Dynamic Topology Organization and Maintenance Algorithms for Autonomous UAV Swarms

Anna Gaydamaka , Graduate Student Member, IEEE, Andrey Samuylov , Dmitri Moltchanov Mateen Ashraf , Bo Tan , Member, IEEE, and Yevgeni Koucheryavy

AbstractâThe swarms of unmanned aerial vehicles (UAV) are nowadays finding numerous applications in different fields. While performing their missions, UAVs have to rely on external positioning information to maintain connectivity and communications between units in a swarm. However, some of the critical applications such as rescue missions are performed in locations, where this information is partially or fully not available, e.g., deep woods, mountains, indoors. In this paper, we propose a method for dynamic topology organization and maintenance in UAV swarms. In addition to the baseline functionality, we also design advanced features required for dynamic swarms merging and disjoining, making it suitable for practical applications. Specifically, the proposal is based on the virtual coordinates system allowing for the utilization of conventional geographical routing algorithms. We test the proposed algorithm in different swarm conditions to illustrate that: (i) it is insensitive to distance estimates up to at least 30% allowing for simple estimation techniques, (ii) the accuracy of the topology inference is at least 90% even under impairments caused by mobility and temporal loss of connectivity, and (iii) the impact of the developed merging algorithm for swarms lasts for multiple tens of time steps that correspond to just few seconds in practice. The set of developed algorithms can be utilized to ensure always connected topology in conditions where positioning information is partially or fully unavailable.

Index Termsâ5G, autonomous operation, GNSS-denied, geographical routing, topology construction and maintenance, UAV swarms.

## I. INTRODUCTION

U NMANNED aerial vehicles (UAV) are nowadays consid-ered as an effective platform to implement various services without direct human involvement. UAVs facilitate and sometimes even replace human labor in many areas, from agriculture and forestry [1], [2] to search and rescue and healthcare [3], [4]. Nowadays, these platforms have already taken over some of the tasks in telecommunications, both technical, e.g., monitoring equipment on top of towers, and more intellectual such as using UAV as a flying base station (BS), relay or anchor [5], [6].

Therefore, both ITU and 3GPP consider UAVs as future network users and aim at developing standards for their direct support in fifth generation (5G) and beyond-5G networks [7], [8].

Once the potential of individual UAVs has been discovered, the idea of using joint systems, UAV swarms, started to appear. UAV swarms have been utilized in a diverse range of applications, including precision agriculture, search and rescue in disaster response, inspection and surveillance of infrastructure, and logistics and delivery in the urban area. Thanks to an ability to perform tasks collectively, such systems have striking advantages, e.g., to search and monitor a wider area, possibilities to carry heavier goods, perform tasks in a parallel mode and thus complete them faster [9], and allow to solve more complex intellectual tasks that are beyond the power of a single UAV. Still, a successful and safe launch of UAV swarms poses several challenges and technical issues, i.e., in-flight swarm localization and control, coordination of UAVs within the swarm, level of UAV autonomy for navigation, choreography of swarm actions, etc.

To enable the deployment of UAV swarms for versatile applications, we have identified several technical gaps that require addressing, such as developing a low-complexity and resilient network within the swarm, implementing a precise sensing and perception system for each individual node, designing a robust and agile formation control algorithm, and ensuring the scalability of the swarm. This paper emphasizes the merging and disjoining functions that are crucial for the formation control and scalability of UAV swarms, especially in autonomous missions where external infrastructures may be unavailable. The term âmergingâ implies the process of combining two or more sub-swarm groups (clusters) of UAVs into a single coordinated swarm. âDisjoiningâ alludes to the process of breaking apart the swarm or separating individual drones from the group.

While performing autonomous missions, UAV swarms typically not only gather information but collectively process it to make decisions in real-time [10], [11], [12]. These tasks require efficient routing of data flows between members of the swarm. Development of efficient routing of data flows is a challenging problem, especially for large swarms, where the efficiency of conventional routing protocols is affected by multiple factors such as: (i) complex three-dimensional (3D) topology of UAV swarms, (ii) constantly changing swarm topology due to relative mobility of UAVs within the swarm when avoiding collisions or performing reformations, (iii) temporal loss of connectivity due to changing propagation conditions.

One of the potential ways to overcome the above-mentioned issues is to utilize topology organization and maintenance algorithms that would dynamically keep the swarm topology up-to-date. In presence of external positioning information, such as GPS-based, one can utilize conventional geographic routing algorithms that are known to be very effective in terms of overheads and routing performance, e.g., Greedy Perimeter Stateless Routing (GPSR) [13] or Compass [14]. However, when this information is not available, for example, when performing search and rescue operations in places inaccessible to Global Positioning System (GPS) or cellular infrastructure (deep woods, mountains, indoors), one needs to resort to conventional routing solutions based on either periodic exchange of routing tables or flooding-based on-demand routing. The former protocols are long known to produce excessive communications overheads [15], [16] while the latter introduces significant delay prior to the actual exchange of data [17]. As a result, both approaches are not suitable for mission-critical UAV swarm applications.

In this paper, we specifically target environmental and functional conditions for UAV swarm applications, where no external positioning information is available. For such types of use cases, we develop a completely distributed topology organization and maintenance algorithm that utilizes only two pieces of information: (i) possibly erroneous distance estimates to its one-hop neighbors that can be deduced by utilizing the propagation model and (ii) availability information about one-hop and two-hop neighbors that can be exchanged regularly in beacon packets. Owing to the dynamic nature of tasks and environments, UAV swarms necessitate adaptive merging or disjoining (splitting) capabilities. Typically, the merging function is employed to enhance capabilities, such as expanding coverage areas, amassing greater amounts of data, or transporting heavier loads over longer distances. Conversely, the disjoining function is utilized for searching and navigating specific targeted areas, routes, and hard-to-reach zones that are inaccessible to large-scale swarms. This paper devises both basic functionality related to maintaining a consistent view of the network at all the UAVs and advanced algorithms related to swarms merging and disjoining. To compare the performance of the proposed algorithms, we then develop topological and routing metrics and proceed assessing performance of the proposed technique. The proposed algorithm explicitly take into account environmental specifics such as mobility of UAVs and inaccuracy of distance estimates as well as use case specific impairments such as temporal loss of connectivity between UAVs in a swarm due to loss of spatial and temporal synchronization.

The main contributions of the study are:

The virtual coordination system (VCS) is introduced for 3D topology construction, maintenance, and message routing for autonomous UAV swarms. The VCS integrates geographical and link quality dynamics to enhance the resilience of swarming operations, particularly during the merging.

- A set of fully distributed, real-time and VCS-based topology construction and maintenance algorithms are proposed to support the essential swarming functions, e.g., merging and disjoining. In addition, the proposed algorithms improve the swarm autonomy level by using only the lightweight local (within the swarm) information and casting off the dependence on external location and connectivity infrastructure.

- The topological and routing metrics are introduced to gauge the performance of the proposed algorithms when the UAV swarm is used for collective tasks.

- Numerical results show that the proposed algorithm is robust to the positioning error, mobility variance and fluctuating UAV behaviour while achieving more than 90% match within the original physical topology. The simulation results also illustrate that the performance of VCS-based algorithms is resilient during the merging of swarms.

The rest of the paper is organized as follows. First, in Section II, the review of related work is presented. The system model is introduced in Section III. The proposed approach is formalized in Section IV. Section V introduces the metrics utilized for further performance assessment of the proposed approach. Numerical results are provided in Section VI. Finally, conclusions are drawn in Section VII.

## II. RELATED WORK

This section presents the related work. We start with modern approaches to topology control in UAV swarms, followed by the outlook of VCS-based approaches proposed so far. Concluding the section, a brief classification of routing protocols that can be utilized in UAV swarms is provided.

The approach considered in our paper is designed for efficient routing in swarms of UAVs, where the external information is unavailable. It allows to infer the topology of the swarm (i.e., graph) based on limited information that can be exchanged between UAVs in âHelloâ packets. Since the developed approach is only needed when the external positioning information is not available, Section II-A describes existing approaches for inferring the coordinates of nodes in a swarm. A special approach that received considerable attention in the past in the context of mesh networks and can be applied to the case of UAVs swarms is VCS that is discussed in Section II-B. Finally, since the proposed approach is in fact developed for routing in UAV swarms, a brief account of existing routing protocols is provided in Section II-C.

## A. Topology Control in UAV Swarms

One of the cornerstones in successful UAV swarming is maintaining the connectivity of the swarm. The straightforward approach for supporting connectivity and coordination in drone swarms is to rely upon some global navigation satellite system (GNSS) for UAV positioning, such as Global Positioning System (GPS). By following this approach, the authors in [18] consider the application of UAV swarm in disaster management, where the positions of individual UAVs in a swarm are detected via GPS. The authors in [19] introduce a system for monitoring and controlling the safety of structures based on computer vision. Using video images photographed by UAV, the system determines the cracking status of internal and external structures. The connectivity within the swarm is also controlled by GPS. The main advantages of this approach are the reduction of maintenance costs and inspection time of the building. The study in [20] targets a problem of packet forwarding in aerial networks, more precisely a way to keep connectivity even in a moving swarm. The suggested algorithm routes a packet using the shortest path to the destination, if it exists. The information about the location of UAVs is provided by GPS. The authors tested the algorithm in a real UAV swarm and concluded that it decreases the delay and number of hops to the destination while keeping the delivery ratio high.

When performing their missions, UAVs may suddenly experience the loss of GPS signals, which can cause the absence of position information. To continue a safe flight without collisions in the so-called GPS-denied environments [21], the authors in [22] proposed to use a method of dead reckoning. The idea of dead reckoning is to calculate new coordinates using known initial coordinates and motion parameters estimated by utilizing the interval inertial positioning system based on a gyroscope and accelerometer. After conducting a number of experiments on simulated data of swarm trajectories and comparing the predicted position with the real, zero collisions were observed.

One more option when GNSS systems are not available is to rely upon a cellular infrastructure. In [23], the authors sum up the current state-of-the-art on the use of cellular networks as the communication infrastructure for UAV swarms and propose their own high-level architecture for swarm autonomy. They provide an UAV-to-UAV (U2U) network communication testbed, where a swarm of UAVs was able to follow the master UAV on a predefined path. A survey [24] focuses on synergies of 5G/B5G innovations for cellularly connected UAVs. The paper covers a wide range of topics from UAV swarm applications to network architectures and channel modeling.

One of the challenging use cases for autonomous swarm missions is operations in locations when GNSS and cellular infrastructure is not available or damaged, e.g., disaster situations, indoors, in deep woods and mountains, etc. In this case, UAVs need to rely upon swarm-internal methods for topology organization and maintenance. One of the approaches is to utilize internal positioning systems and/or radars [25]. In [26], the authors introduced a relative localization sensor system based on gyroscopes and accelerometers. In spite of positioning errors accumulating over time, it is demonstrated that the proposed approach allows to maintain swarm topology over long periods of time when GPS and/or cellular infrastructure is not available. The study [27] aims at reducing the number of isolated drones in a highly dynamic topology network. The approach is inspired by biological natural swarms, like swarms of dragonflies, and reinforces it with machine learning. The authors considered a case when UAVs are equipped with GPS, radar mechanisms, and altitude sensors to support connectivity. In general, the use of radars allows for precise topology maintenance but requires additional equipment to be available at each drone in the swarm which limits the application of this approach [28], [29].

The paper [30] proposes an integrated vehicular system using UAVs and UGVs for autonomous exploration, mapping, and navigation. It implements a two-layered exploration strategy, with a coarse exploration layer using UGVs and a fine mapping layer using UAVs. The authors in [31] focus on path planning algorithms in the absence of GPS signals, leveraging range information from stationary objects called Landmarks (LMs). The optimization problem for LM placement and vehicle routing is posed as an integer program, and two fast heuristics are presented to find feasible solutions. The paper [32] tackles the issue of persistent excitation-based relative localization for multi-UAVs in GPS-denied environments. It introduces synchronized sensor sample prediction and redesigns RL estimation to avoid error accumulation and achieve greater precision. Together, these works demonstrate the potential of unmanned systems to operate autonomously and collaboratively, using innovative approaches to overcome challenges in navigation and perception.

The authors in [33] develop a self-organizing flying network using a hybrid multitask algorithm for UAV swarms in communication relay networks and surveillance missions. To address three principal challenges of UAV topology maintenance and communications, the authors propose a hybrid solution based on market auction paradigms and a biologically inspired pheromone map. Even though the proposed solution depends on the correct parametrization, the numerical results demonstrate that it effectively serves the outlined performance goals.

## B. Virtual Coordinate Systems

An alternative to the radars and inertial positioning systems in absence of GNSS and cellular infrastructure is to utilize virtual topologies that closely resemble physical ones. The research on such systems dates back to the seminal paper by Rao et al. [34], where the authors proposed to utilize virtual coordinate systems (VCS) for topology construction and further routing in wireless sensor networks (WSN). Motivated by the use of geographical routing on top of VCSs, the authors in [35] considered a static 2D network with several sink nodes acting as static anchors and devised a VCS utilizing the number of hops to the sinks as the main input parameter. Their numerical results show that the mean path length of greedy geographical routing algorithms running on top of the developed VCS exceeds the shortest path by just a few percent.

The study [36] presents Greedy Embedding Spring Coordinates (GSpring), a geographical routing algorithm that proposes the solution for the issue of packets stuck at dead ends. In their proposed approach, nodes detect situations that lead to dead ends during greedy forwarding and adjust their coordinates so as to increase the degree of connectivity of existing voids in the routing topology. Though GSpring improves the routing efficiency when compared to existing geographic routing algorithms, e.g., GPSR [13] or Compass [14], it operates only in networks with static nodes. Further, the study in [37] considers a network, where external positioning information is not available at the nodes. Using local connectivity information, they build a logical topology, on top of which the lightweight geographic routing protocol is applied. The authors test the proposed framework by using the packet delivery ratio and node power consumption.

Along these lines, a number of approaches for VCS construction have been proposed in the past. In general, they can be classified to anchor-driven [35], [36], [37], [38], [39] and anchorless ones [40], [40], [41]. The former group assumes the presence of static nodes in the system which serve as universal virtual references. Anchorless systems rely upon either modern algorithms such as distributed hash tables (DHT) [40] or produce simple topologies such as chain formations [42], or circular ones [41]. Most of these systems are tailored to static deployment use cases such as those typical for WSNs. However, recently, the use of VCSs for topology construction in mobile mesh networks has been demonstrated in [43], where gradual algorithms have been proposed. This paper extends the work of [43] proposing an algorithm suitable for fully dynamic systems such as UAV swarms and develop enhancements such as merging and disjoining that are critical for the considered use case.

## C. Routing in UAV Swarms

Over time, a considerable body of literature has addressed research on routing in communication networks [44]. These protocols can be classified into three categories: (i) proactive or table-driven, (ii) reactive or on-demand, and (iii) hybrid protocols that combine features of proactive and reactive mechanisms. The main advantage of proactive protocols is low route acquisition latency as the routes are always kept up-to-date. However, due to the need for regular updates, table-driven protocols are not well suited for mobile networks such as UAV swarms since the routing table updates happen often and create significant overheads. Typical examples of proactive protocols are Destination-Sequenced Distance Vector (DSDV) [45] and Optimized Link State Routing Protocol (OLSR) [46].

As opposed to the proactive design, reactive protocols find the routes on-demand. The process consists of two steps: broadcasting the route request packets to the network and receiving return messages with a route response. To avoid duplication, each packet has a sequence number. In the second step, when the destination node receives the packet, it responds with a route reply message that takes the reverse path in the network. The downside of this approach is the latency of route acquisition that might be critical for UAV applications [47]. The AODV protocol, proposed in [48] and standardized in RFC 3651, is an example of an on-demand routing protocol.

Hybrid routing protocols combine the functions of proactive and reactive routing protocols. Typically, they are used to determine optimal network destination routes and to report changes in network topology data. One possible implementation of this combination is to keep the routing tables from table-driven routing protocol for nodes in close proximity and use on-demand routing protocol for nodes on the periphery [49].

A separate class of routing protocols relies upon the use of external information to make routing decisions. For example, geographic routing protocols [50] use GPS locations instead of network addresses. In this case, the source sends packets to the destination based on its geographic location. This solves the problem of storage and communications overheads associated with table-driven protocols and alleviates long route acquisition delay of on-demand protocols. Nevertheless, the availability of external information is a basic requirement in these protocols.

Nowadays machine learning techniques are being employed in various fields, and routing protocols are no exception. A new routing protocol called Q-FANET for Flying Ad-Hoc Networks (FANETs) utilizes an improved Q-learning algorithm to reduce network delay in high-mobility scenarios [51]. To suit the dynamic behavior of FANETs, the proposed Q-FANET combines two routing protocols (QMR and Q-Noise+) and uses reinforcement learning on top of it. The results of the performance evaluation show that Q-FANET outperforms the other reinforcement learning-based routing protocols in terms of lower delay, lower jitter, and a minor increase in packet delivery ratio. The proposed protocol is relevant for UAV swarm organization as it can enhance the reliability and performance of communication networks between drones and ground control stations, which is critical for the safe and effective operation of drone swarms.

<!-- image-->  
Fig. 1. UAV deployment model (red crosses in the bottom represent the loss of GNSS signal).

In this study, it is presumed that the developed VCS will provide location-related information to all the network nodes in a fully distributed manner. More specifically, the developed approach is in fact a VCS that does not rely upon anchor nodes as compared to most of the algorithms reviewed in Section II-B. Thus, the developed VCS provides the routing nodes with geo-location of the destination node, and then any geo-routing protocols can be utilized. Since the choice of the geo-routing protocol is not important for our paper, we have compared the performance of routing over the developed VCS by specifying a general routing protocol independent metric.

## III. SYSTEM MODEL

In this section, we formalize the system model. We start with the network graph inference problem with a constrained set of readability information. Then, we proceed with specifying models of impairments affecting UAV connectivity in the swarm including loss of temporal/spatial synchronization, mobility model, etc. The section is concluded by the definition of metrics of interest.

## A. Deployment Model

Consider the deployment model illustrated in Fig. 1. The swarm is assumed to move in a certain direction with an average speed $v _ { S }$ m/s. Specifically, we consider an area of size $L _ { 1 } \times L _ { 2 } \times L _ { 3 }$ cubic meters with N nodes uniformly distributed within. It is assumed that no external GNSS information is provided for the swarm and that no UAVs within the swarm have cellular connectivity. The typical use cases considered are disaster management, indoors, deep woods, and mountain operations, where this information is completely unavailable or temporarily blocked.

In UAV swarms, the inter-node links are inherently dynamic due to wireless propagation specifics that may lead to the temporal loss of connectivity due to, e.g., loss of synchronization between nodes. This situation is modeled by randomly chosen nodes appearing and disappearing in the swarm, i.e., switching between connected and disconnected states. These processes are assumed to be mutually independent at all the UAVs comprising the swarm.

Another impairment related to internal UAV mobility inside the swarm occurs while performing a mission task or going around obstacles. Often the movements of UAVs within the swarm are limited to small changes in the UAV locations for a subset of units. To capture this effect, it is assumed that at any given instant of time, no more than g percentage of UAVs are involved in relative movements with respect to the swarm movement. The relative speed of these units with respect to $( 1 - g ) \%$ of UAVs is denoted by $v _ { R }$ . These UAVs move within (1 )the cubic compartments with sizes $l _ { 1 } \times l _ { 2 } \times l _ { 3 }$ cubic meters centered around UAVâs randomly chosen location according to the random direction mobility model (RDM, [52]). According to this model, UAV selects a direction of movement randomly and uniformly within , Ï and then moves toward the selected (0 2direction at constant speed $v _ { R }$ for exponentially distributed time with mean $\beta ^ { - 1 }$ . The process is then repeated. We assume a peculiar reflection of the compartment boundaries.

The proposed algorithms in this paper are independent of the transmission technology utilized by the UAVs and hence can be used for any particular transmission technology. The transmission ranges $r _ { i }$ of radios equipped at $\mathrm { U A V s \ } i = 1 , 2 , \dotsc , N ,$ are = 1 2known apriori or can be estimated by utilizing radio part parameters, e.g., carrier frequency, transmit and receive gains, receiver sensitivity, and noise floor. All the neighbors within the coverage radius $r _ { i }$ are assumed to hear and decode transmissions. If millimeter wave communications with highly directional antennas are utilized it is assumed that UAV may maintain connectivity with as many neighbors as needed.

## B. Network Graph Inference Problem

It is assumed that each UAV possesses information about (i) distance estimates to the one-hop neighbors within its coverage area $r _ { i }$ and (ii) information about the two-hop neighbors. The former can be obtained by utilizing the information about at least the received signal strength and subsequently applying the propagation model for the considered carrier frequency, such as free-space path loss (FSPL). More comprehensive distances estimation algorithms can be utilized such as those based on the angle/zenith of arrival (AoA/ZoA) and the associated times of arrival if available. The use of radars for distance estimation is not precluded as well. To capture a wide range of potential distance estimate methods, we model the positioning error as $\alpha D ,$ where D is the actual distance between neighbors and $\alpha \in ( 0 , 1 )$ is the error factor. Specifically, the (0 1)information about the two-hop neighbors actually include IDs of UAVs that are directly connected to one-hop neighbors of a certain UAV and distances to them. This information is directly available at one-hop neighbors and is assumed to be delivered to the considered UAV in âHelloâ packets. No other local or global information is assumed to be available at each UAV locally.

The information about the neighbors can be exchanged in âHelloâ packets or in specifically designated âBeaconâ packets exchanged on regular intervals, $i = 0 , 1 , \ldots ,$ , of duration $T ,$ i.e., $T = t _ { i } - t _ { i - 1 }$ = 0 1, âi. The latter variable defines the time step =of algorithm execution at different nodes. These time steps are not necessarily synchronized between all the UAVs in a swarm.

To keep the application as wide as possible, we assume that directions towards neighbors is not explicitly utilized in the algorithm. However, observe that the information about twohop neighbors allows to implicitly capture not only principle reachability but the directionality as well in a very simple form. In this way, a certain UAV running the algorithm sees branches of UAVs connected to different single-hop neighbors.

Having the above-mentioned information, the algorithm is expected to be executed independently at each node at each time step. Since the main usage is to maintain UAV swarm topology there are two types of tasks to be solved: (i) assignment of virtual coordinates within the swarm and (ii) enabling seamless realtime merging and disjoining of different swarms.

1) Assignment of Virtual Coordinates: Essentially the task is to construct distributed graph mapping physical space to a virtual one. To find virtual coordinates it is convenient to formulate the problem in terms of graph theory. We denote an oriented graph $G = ( V , A )$ with a set of vertices $V = \{ 1 , 2 , . . . , N \}$ , a set of edges $A \subset \{ ( i , j ) | i , j \in V , i \neq j \}$ = 1 2, and edge lengths $d _ { i , j } >$ $0 , ( i , j ) \in A$ ( ) =. That is, the goal is to find nodesâ virtual coordinates $\mathbf { s } _ { i } = ( x _ { i } , y _ { i } , z _ { i } ) \in \mathbb { R } ^ { 3 } , i = 1 , 2 , \ldots , N$ at any time step $t _ { i } ,$ , such = ( )that for all edges $( i , j ) \in A$ 1 2the distance between $\mathbf { s } _ { i }$ and ${ \bf \nabla } _ { \bf S } { } _ { j }$ should be close to $d _ { i , j }$

2) Merging and Disjoining: When performing autonomous missions, there might be the need to change UAV swarm formations by adding individual UAVs or swarms of UAVs to the original swarm. Alternatively, some of the UAVs might be lost during the mission. For this reason, for the VCS to be of practical interest, it has to allow for smooth swarm merging and disjoining. Note that there might be no need for special algorithms for disjoining as nodes leaving the swarm functionality can be incorporated into the VCS maintenance procedure.

<!-- image-->  
Fig. 2. Illustration of a solution to the VCS addressing the problem.

## C. Metrics of Interest

As the main goal of this paper is to introduce VCS topology organization and maintenance algorithms for efficient geographical routing without the use of GNSS systems, topological and routing-related metrics of interest are considered. The topological metric is represented by the Pearson correlation coefficient between pairwise distances in virtual and physical topologies. Observe that since the aim is to enable efficient routing in dynamic UAV swarms, the developed algorithm may not produce the virtual topology exactly matching a physical one although it is preferable. Further, to benchmark the routing performance without resorting to details of specific routing protocols proposed to date, in Section V, we propose a generic routing metric.

## IV. THE PROPOSED ALGORITHMS

In this section, we first develop our algorithm for VCS address allocations. Then, we proceed with specifying the algorithms for swarm merging.

## A. VCS Address Allocation Problem

1) Problem Formulation: Consider a UAV swarm represented as a finite graph $G = ( V , A )$ whose vertices may in = ( )general be dynamic, e.g., may disappear and move. The following notation is proposed. The vertices of the graph, $V =$ $\{ 1 , 2 , . . . , N \}$ =, are the UAVs. UAV i is able to receive a signal 1 2from other devices within its transmission range $r _ { i } , i \in V$ , which is defined by the UAV radio characteristics. The UAVs are connected by an edge if they are within the transmission range of each other. The set of edges is denoted by

$$
A \subset \{ ( i , j ) | i , j \in V , i \neq j \} ,\tag{1}
$$

and also define edge lengths as $d _ { i , j } > 0 , ( i , j ) \in A$

0 ( )Fig. 2 illustrates the intuitive solution to the VCS address allocation problem. Specifically, it highlights the process of adjusting the virtual coordinates of node k. Here, node $j ,$ , as a one-hop neighbor of k, affects the choice of virtual coordinates of node k, denoted by sk. Ideally, node k should move to the point $\mathbf { s } _ { k } ^ { \prime } .$ . However, in a real scenario, node k has multiple one-hop neighbors (not shown in Fig. 2) which also affect the choice of virtual coordinates. Thus, making this process non-trivial.

Let $S _ { i } = \{ j \in V | ( i , j ) \in A \}$ be the set of vertices that are = ( )endpoints of the edges associated with vertex $i , i \in V$ . We denote by $\bar { S } _ { i } ^ { - 1 } = \{ i \in V | \bar { j } \in A \}$ the set of vertices which are incident to the edges of vertex $j .$ . Further, let

$$
r ( \mathbf { s } _ { i } , \mathbf { s } _ { j } ) = { \sqrt { ( x _ { i } - x _ { j } ) ^ { 2 } + ( y _ { i } - y _ { j } ) ^ { 2 } + ( z _ { i } - z _ { j } ) ^ { 2 } } } ,\tag{2}
$$

be the distance between $\mathbf { s } _ { i }$ and $\mathbf { s } _ { j } , \pmb { \sigma } = ( \mathbf { s } _ { 1 } , \ldots , \mathbf { s } _ { N } )$

= (As an example, consider an arbitrary vertex $\mathbf { s } _ { k }$

$$
\begin{array} { l } { { \displaystyle { \bf s } _ { k } ^ { \prime } = { \bf s } _ { j } + d _ { k , j } \frac { { \bf s } _ { k } - { \bf s } _ { j } } { r ( { \bf s } _ { k } , { \bf s } _ { j } ) } = { \bf s } _ { k } + } } \\ { { \displaystyle ~ + \left( 1 - \frac { d _ { k , j } } { r ( { \bf s } _ { k } , { \bf s } _ { j } ) } \right) ( { \bf s } _ { j } - { \bf s } _ { k } ) } , } \end{array}\tag{3}
$$

at a distance $d _ { k , j }$ from ${ \bf s } _ { j } .$ , see Fig. 2.

To make the distance between j and k close or equal to $d _ { k , j }$ the node $\mathbf { s } _ { k }$ should be moved to the new position $\mathbf { s } _ { k } ^ { \prime }$ . If one averages the desired positions of the node $\mathbf { s } _ { k }$ with respect to all surrounding nodes $j \in S _ { k }$ , then

$$
\mathbf { s } _ { k } ^ { \prime } = \mathbf { s } _ { k } + \frac { 1 } { | S _ { k } | } \sum _ { j \in S _ { k } } \left( \frac { 1 - d _ { k , j } } { r ( \mathbf { s } _ { k } , \mathbf { s } _ { j } ) } \right) ( \mathbf { s } _ { n , j } - \mathbf { s } _ { n , k } ) .\tag{4}
$$

This leads to the following iterative procedure

$$
\begin{array} { l } { { \displaystyle { \bf s } _ { n + 1 , k } = { \bf s } _ { n , k } + \frac { \varepsilon _ { n } } { | S _ { k } | } \sum _ { j \in S _ { k } } \left( 1 - \frac { d _ { k , j } } { r ( { \bf s } _ { n , j } , { \bf s } _ { n , k } ) } \right) } \ ~ } \\ { { \displaystyle ~ \times \left( { \bf s } _ { n , j } - { \bf s } _ { n , k } \right) = { \bf s } _ { n , k } - \frac { \varepsilon _ { n } } { | S _ { k } | } } \ ~ } \\ { { \displaystyle ~ \times \sum _ { j \in S _ { k } } \left( 1 - \frac { d _ { k , j } } { r ( { \bf s } _ { n , j } , { \bf s } _ { n , k } ) } \right) \left( { \bf s } _ { n , j } - { \bf s } _ { n , k } \right) } , } \end{array}\tag{5}
$$

for any $k = 1 , 2 , \ldots , N , n = 1 , 2 , \ldots$ , where $0 < \varepsilon _ { n } < 1$ is the = 1 2 = 1 2 0parameter determining how drastically the new value $\mathbf { s } _ { n + 1 , k }$ of the vector $\mathbf { s } _ { k }$ differs from its previous value $\mathbf { s } _ { n , k }$

2) Convergence Properties: The iterations in (5) are very similar to those utilized to minimize some function $F ( \pmb { \sigma } )$ using iterations of the form

$$
{ \pmb \sigma } _ { n + 1 } = { \pmb \sigma } _ { n } - \varepsilon _ { n } { \pmb \pi } _ { n } , n = 1 , 2 , . . . .\tag{6}
$$

There are various methods for choosing the parameters $\varepsilon _ { n }$ and vectors $\pi _ { n }$ . The classic method is the fast descent method [53], [54], [55], where the gradient $\pi _ { n }$ is taken as a vector $\pi _ { n } =$ $\nabla F ( \pmb { \sigma } _ { n } )$ , â denotes the gradient.

( )Consider the problem of minimizing a function

$$
F ( \pmb { \sigma } ) = \sum _ { i = 1 } ^ { N } \sum _ { j \in S _ { i } } F _ { i , j } ( r ( \mathbf { s } _ { i } , \mathbf { s } _ { j } ) ) ,\tag{7}
$$

with differentiable terms $F _ { i , j } ( x )$

The gradient $\nabla F ( \pmb { \sigma } _ { n } )$ ( )of this function is

$$
\nabla F ( { \pmb \sigma } ) = ( \nabla _ { 1 } F ( { \pmb \sigma } ) , \nabla _ { 2 } F ( { \pmb \sigma } ) , \dots , \nabla _ { N } F ( { \pmb \sigma } ) ) ,\tag{8}
$$

where the individual gradient terms are given by

$$
\begin{array} { l } { \nabla _ { k } F ( { \boldsymbol \sigma } ) = \displaystyle \sum _ { j \in S _ { k } } \frac { f _ { k , j } ( r ( { \bf s } _ { k } , { \bf s } _ { j } ) ) } { r ( { \bf s } _ { k } , { \bf s } _ { j } ) } { } } \\ { + \displaystyle \sum _ { j \in S _ { k } ^ { - 1 } } \frac { f _ { k , j } ( r ( { \bf s } _ { k } , { \bf s } _ { j } ) ) } { r ( { \bf s } _ { k } , { \bf s } _ { j } ) } , } \end{array}\tag{9}
$$

and $\begin{array} { r } { f _ { i , j } ( x ) = \frac { d } { d x } F _ { i , j } ( x ) } \end{array}$

Note an important special case of graphs $G = ( V , A )$ with = ( )symmetric adjacency matrix A, for which the following conditions are satisfied

$$
S _ { i } ^ { - 1 } = S _ { i } , i \in V , F _ { i , j } ( x ) = F _ { j , i } ( x ) , j \in S _ { i } , i \in V .\tag{10}
$$

For such graphs (9) takes the form

$$
\nabla _ { k } F ( \pmb { \sigma } ) = 2 \sum _ { j \in E _ { k } } \frac { f _ { k , j } \big ( r ( \mathbf { s } _ { k } , \mathbf { s } _ { j } ) \big ) } { r ( \mathbf { s } _ { k } , \mathbf { s } _ { j } ) } ( \mathbf { s } _ { k } - \mathbf { s } _ { j } ) .\tag{11}
$$

Let the graph $G = ( V , A )$ have symmetric adjacency matrix A and $d _ { i , j } = d _ { j , }$ = (i for all $( i , j ) \in A .$ . Consider two versions of =the functions $F _ { k , j } ( x )$ and the corresponding gradients of the function F Ï

$$
F _ { k , j } ( x ) = \frac { A _ { k } } { 4 } ( x - d _ { k , j } ) ^ { 2 } , f _ { k , j } ( x ) = \frac { A _ { k } } { 2 } ( x - d _ { k , j } ) ,
$$

$$
\nabla _ { k } F ( \pmb { \sigma } ) = A _ { k } \sum _ { j \in S _ { k } } \left( \frac { 1 - d _ { k , j } } { r ( \mathbf { s } _ { k } , \mathbf { s } _ { j } ) } \right) ( \mathbf { s } _ { k } - \mathbf { s } _ { j } ) ,\tag{12}
$$

and also

$$
{ \begin{array} { l } { { \displaystyle F _ { k , j } ( x ) = \frac { A _ { k } } { 8 } ( x ^ { 2 } - { d _ { k , j } } ^ { 2 } ) ^ { 2 } , f _ { k , j } ( x ) = \frac { A _ { k } } { 2 } x ( x ^ { 2 } - { d _ { k , j } } ^ { 2 } ) , } } \\ { { \nabla _ { k } F ( { \pmb \sigma } ) = A _ { k } \displaystyle \sum _ { j \in S _ { k } } \big ( r ^ { 2 } ( { \bf s } _ { k } , { \bf s } _ { j } ) - { d _ { k , j } } ^ { 2 } \big ) ( { \bf s } _ { k } - { \bf s } _ { j } ) . \qquad ( 1 3 ) } } \end{array} }
$$

It is easy to see that the considered intuitive solution (5) of the VCS address allocation problem is equivalent to the solution of the minimization problem of function in (7) with components in the form (12), where $A _ { k } = | S _ { k } | ^ { - 1 }$

=3) Single-Step Address Allocation: The iterative procedure in (5) can be implemented in different ways. One of the algorithms, called single step allocation, constructs a target optimization function that incorporates distance assessments to one-hop neighbors. The optimization problem is solved to obtain the most fitting virtual address for each UAV at each step independently of other UAVs.

Consider the following utility function

$$
\begin{array} { l } { { \displaystyle F _ { o } ( { \bf s } _ { k , j } ) = \sum _ { j \in S _ { i } } \bigg [ F _ { 1 } ( r ( { \bf s } _ { i } , { \bf s } _ { j } ) , d _ { i , j } ) } } \\ { { \displaystyle ~ + \sum _ { j \in M _ { i } } F _ { 2 } ( r ( { \bf s } _ { i } , { \bf s } _ { j } ) , d _ { i , j } ) \bigg ] , } } \end{array}\tag{14}
$$

where $S _ { i }$ is the set of one-hop neighbors, and $M _ { i }$ is the set of two-hop neighbors.

The main idea of (14) is to find the virtual coordinates of UAV i by minimizing the penalty assigned to it when a set of rules is not obeyed. The first rule is that the distance between the UAV i and one-hop neighbors should be within a certain predefined range $d _ { n }$ . Specifically, UAV i should not be closer than a physical distance estimation and, at the same time, should not move away too far, as it is a directly connected neighbor. The second rule is that the distance between the UAV i and two-hop neighbors should be greater than or equal to a certain predefined limit $d _ { m }$ Otherwise, a two-hop neighbor falls inside the area where UAV i is capable to receive a signal from UAV j, and UAV j becomes a one-hop neighbor by definition.

<!-- image-->  
Fig. 3. Visual illustration of single step address allocation algorithm.

In order to implement the first rule we defince a function $F _ { 1 } ( r ( \mathbf { s } _ { i } , \mathbf { s } _ { j } ) , d _ { i , j } ) , j \in N _ { i }$ which operates with the current UAV ( ( ) )i and its one-hop neighbors which are denoted by $N _ { i }$ . It compares the virtual distance $r ( \mathbf { s } _ { i } , \mathbf { s } _ { j } )$ between UAV i and its one-hop neighbor $j$ ( )and the estimation of physical distance between i and $j$ and assigns a certain penalty based on its difference. In general, the function is defined as

$$
\begin{array} { r } { F _ { 1 } ( d , d _ { n } ) = \left\{ \begin{array} { l l } { | | d - D _ { L } | | } & { d \leq D _ { L } ( d _ { n } ) , } \\ { 0 } & { D _ { L } ( d _ { n } ) < d \leq D _ { H } ( d _ { n } ) , } \\ { | | d - D _ { H } | | } & { D _ { H } ( d _ { n } ) < d . } \end{array} \right. } \end{array}\tag{15}
$$

where $| | \cdot | |$ denotes euclidean distance. The limit points of the penalty-free interval are denoted as $D _ { L }$ and $D _ { H }$ , where the former stimulates the virtual coordinates of the node i not to overlap with its one-hop neighborâs, and the latter indicates the transmission range of the current one-hop neighbor.

Similarly to (15), $F _ { 2 } ( r ( \mathbf { s } _ { i } , \mathbf { s } _ { j } ) , d _ { i , j } )$ penalizes the current ( ( ) )UAV i for being too close to its two-hop neighbors $j \in M _ { i }$ as they are not in the coverage. It is given by

$$
F _ { 2 } ( d , d _ { m } ) = \left\{ \begin{array} { l l } { | | d - D _ { T } | | } & { d \leq D _ { T } ( d _ { m } ) , } \\ { 0 } & { d > D _ { T } ( d _ { m } ) . } \end{array} \right.\tag{16}
$$

An illustration of the penalty function (16) is shown in Fig. 3. The nodes with coordinates $\mathbf { s } _ { t , j }$ are two-hop neighbors of the node i. Knowing that $D _ { T }$ is the transmission range of two-hop neighbors, the optimal coordinates of the node i should be outside of it. The three-dimensional nature of the illustration reflects the fact that three coordinates $( x , y , z )$ are searched, ( )while the color represents the value of the penalty function.

Algorithm 1: VCS Update Algorithm.   
Input:   
1ï¼ signaling data packets $p _ { j } \in P _ { i }$ with data:   
Â· $j \cdot \mathrm { I D }$ of the one-hop neighbor of UAV i   
$\mathbf { s } _ { n , j }$ - virtual coordinates of UAV j at iteration n   
. $N _ { j } \textrm { - a }$ list of one-hop neighbors' IDs of UAV j   
Â·a set of virtual coordinates of $N _ { j }$   
2) $d _ { i , j }$ - an estimate of the physical distance between   
UAVs i and j   
Result: virtual coordinates   
${ \bf s } _ { n + 1 , i } = ( x _ { n + 1 , i } , y _ { n + 1 , i } , z _ { n + 1 , i } )$ of UAV i at   
iteration n of the algorithm   
1 During a specified time interval â³t UAV i may   
receive signaling data packets $p _ { i } ;$   
2 Calculate $\mathbf { s } _ { n + 1 , i } ;$   
3if $P _ { i } = \emptyset$ then   
4 if $\mathbf { s } _ { n , i } \neq N U L L$ then   
5 ${ \bf s } _ { n + 1 , i } = { \bf s } _ { k , i }$   
6 else   
7 $\underline { { | } } \ \mathbf { s } _ { k + 1 , i } = r a n d ( )$   
8else   
9 if low mobility then   
10 Single step Address Allocation   
11 else   
12 Gradual Address Convergence   
13 Broadcast $p _ { i } , p _ { i } = \{ i , \mathbf { s } _ { n , i } , N _ { i } , \mathbf { s } _ { n , j } , j \in N _ { i } \}$   
14 Repeat from point 1.

## B. Proposed Algorithms

Recall that UAV calculates its virtual coordinates in three cases: (i) when UAV just joined the network and obtains its first virtual coordinates, (ii) when UAV needs to update its virtual coordinates at iteration n, (iii) on-demand when merging procedure is initiated. In this section, we introduce a VCS update Algorithm 1 and describe how it can be utilized to determine and dynamically update the virtual coordinates of UAV i at step n of algorithm iteration. The merging procedure is described in Section IV-C.

To initiate the algorithm, UAV i within a certain period of time receives a signaling data packet from UAV that is in the set $V \cap S _ { i }$ (line 1). Assume that UAV j is within the transmission range of UAV i. Then, UAV i will receive a signaling packet $p _ { j }$ with information about (i) UAV $j ^ { \prime } \mathrm { s } \ W .$ (ii) virtual coordinates of UAV j, (iii) the list of one-hop neighbors of $\mathrm { U A V } ~ j$ and their coordinates. In addition to the signaling data packets, UAV i estimates the physical distance to its one-hop neighbors, $d _ { i , j } ,$ $j = 1 , 2 , \dots , N _ { j }$ . The signaling data packets from the one-hop neighbors and the physical distance estimate are the two inputs to Algorithm 1. When the input data is collected, UAV i computes its virtual coordinates based on (15) and (16) (line 2). Once virtual coordinates are obtained, UAV i starts broadcasting signal packets with updated virtual coordinates (line 3).

```latex
Algorithm 2: Swarms Merging: Merging UAV 0.
Input:
1) 0 - ID of the merging UAV
2) $( x _ { i , 0 } , y _ { i , 0 } )$ - virtual coordinated of UAV 0 in the
coordinate system of swarm i
3) $N _ { 0 } - \mathrm { a }$ list of one-hop neighborsâ IDs of UAV 0 in
swarm i
1: For all $i , i \in C \colon$
2: Send a message polar $( 0 , x _ { i , 0 } , y _ { i , 0 } )$ to all $j , j \in N _ { 0 } .$
(0 )3: After receiving a response message angles $( j , \varphi , \psi )$
from all $j , j \in N _ { 0 } ,$ update parameters $\varphi _ { i , 0 }$ and $\psi _ { i , k } \colon$
4: $\begin{array} { r } { \varphi _ { i , 0 } = \operatorname* { m i n } _ { n \in C _ { i } } \theta _ { i , n } , } \end{array}$
$\mathfrak { H } ; \psi _ { i , 0 } = \operatorname* { m a x } _ { n \in C _ { i } } \theta _ { i , n } , i = { 1 , 2 , . . . c } .$
= m6: Calculate
7: $\theta _ { i } = \theta _ { i }$ ,min,
8: $\begin{array} { r } { \delta _ { i } = \sum _ { j = 1 } ^ { i - 1 } ( \theta _ { j , \mathrm { m i n } } - \theta _ { j , \mathrm { m i n } } ) . } \end{array}$
= ( )9: Send a message cartesian $\left( 0 , \theta _ { i } , \delta _ { i } \right)$ to all j,
$j \in N _ { 0 } ;$
10: After receiving a response message ready j from all
$j , j \in N _ { 0 } ,$ take the coordinates (0,0).
```

UAV may not receive any signaling data packets. This means that UAV does not have any one-hop neighbors. This can either be because UAV is the first UAV to join the network or UAV is far from the connected component of the network. In the first case, UAV is assigned random virtual coordinates, while in the second case, the UAV keeps its previous virtual coordinates until the next update.

## C. UAV Swarms Merging

We now proceed specifying the merging procedure by proposing an algorithm to recalculate virtual UAV coordinates in case a UAV belonging to more than one swarm appears. In practice, this procedure shall be initiated when UAV having a different swarm ID joins the current swarm formed by one or more UAVs. The proposed algorithm specifies two separate parts: (i) the operations of UAV belonging to several swarms (âmergingâ UAV), and (ii) the operations of all other UAVs.

Consider a network consisting of multiple, $c > 2 ,$ , UAV 2swarms represented by a disjoint graph, where UAV swarms are connectivity components of the graph. The set $C = 0 , 1 , \ldots , c$ = 0 1denotes the set of all swarms. It is assumed that there are $N ( i )$ UAVs in the swarm $i \in C .$ ( ). We denote the virtual coordinates of the nth UAV within ith swarm by $( x _ { i , n } , y _ { i , n } )$ . Further, assume that a randomly chosen UAV in swarm i comes in the transmission range of a UAV that belongs to a different swarm. We denote the virtual coordinates of this UAV in the swarm i by $( x _ { i , 0 } , y _ { i , 0 } )$ The polar coordinates of the vector $( x _ { i , n } - x _ { i , 0 } , y _ { i , n } - y _ { i , 0 } )$ are denoted by $( r _ { i , n } , \theta _ { i , n } )$ . The task is to determine new virtual ( )coordinates of the UAVs in the new joint swarm.

Algorithm 3: Polar Coordinates: UAV n.   
Input:   
1) $( x _ { i , n } , y _ { i , n } )$ - virtual coordinated of UAV n in the   
coordinate system of swarm i   
2) $N _ { n } - \mathbf { a }$ list of one-hop neighborsâ IDs of UAV n   
1: UAV n received a message polar $\cdot ( k , x _ { i , 0 } , y _ { i , 0 } )$ from   
$\mathrm { U A V ~ } k , k \in N _ { n } .$   
2: If the message $\mathtt { p o l a r } ( l , x _ { i , 0 } , y _ { i , 0 } )$ was received earlier   
( )from some UAV l, send a message   
angles $( n , \varphi _ { i , n } , \psi _ { i , n } )$ to UAV l.   
( )3: Calculate the polar coordinates $( r _ { i , n } , \theta _ { i , n } )$ , save the   
parameters $\varphi _ { i , n } = \theta _ { i , n } , \psi _ { i , n } = \theta _ { i , n } .$   
=4: Send a message polar $( n , x _ { i , 0 } , y _ { i , 0 } )$ to $N _ { n } ,$ except $k .$   
( )5: After receiving a response message angles $( n , \varphi , \psi )$   
update the parameters $\varphi _ { i , k } = \operatorname* { m i n } ( \varphi , \varphi _ { i , k } )$   
$\psi _ { i , k } = \operatorname* { m a x } ( \psi , \psi _ { i , k } ) .$   
= max( )6: After receiving a response message angles $( j , \varphi , \psi )$   
from all $j , j \in N _ { n } , j \neq k ,$ send angles $( n , \varphi , \psi )$ to   
UAV k.

The idea of coordinate reassignment is to first convert the coordinates of all UAVs into a single coordinate system. Since for Cartesian coordinates such an operation is not straightforward, we propose to use a polar coordinate system, $( r _ { i , n } , \theta _ { i , n } )$ . It sim-( )plifies the algorithm by the fact that only the second coordinate, $\theta _ { i , n } .$ , needs to be recalculated, while the first coordinate is determined by calculating the distance to the reference âmergingâ UAV. Finally, at the last step, the merged polar coordinates are recalculated into Cartesian coordinates and broadcasted in both swarms. To avoid ambiguity, the merging UAV is marked by 0.

The merging procedure is considered from the point of view of the merging UAV combining the swarms. The operations that need to be performed on the merging UAV are presented in Algorithm 2, while those that need to be performed at all the other UAVs â in Algorithms 3 and 4.

In Algorithm 2, the merging UAV initiates a Cartesian coordinate recalculation operation in each swarm i to which it belongs. The merging UAV sends a polar $( 0 , x _ { i , 0 } , y _ { i , 0 } )$ message to all (0 )its neighbors in swarm i (line 2). The polar message contains the ID of the UAV from which the message is sent and the virtual coordinates of the merging UAV in swarm i. Once other UAVs receive polar, they calculate their polar coordinates, taking the merging UAV as the center of coordinates, see Algorithm 3. Then, the merging UAV waits for a response message angles $( j , \varphi , \psi )$ from all its neighbors (line 3). When the merging UAV has received angles from all its neighbors, it updates the $\varphi$ (line 4) and Ï (line 5) parameters and calculates the polar angles of the UAVs from all the swarms (line 7,8). This operation is required further to recalculate the polar coordinates of all the UAVs in the same coordinate system. Next, the merging UAV converts the polar coordinates into Cartesian coordinates by initiating this process with a cartesian $( 0 , \theta _ { i } , \delta _ { i } )$ message (0 )(line 9), starting Algorithm 4. When the last UAV has performed the Cartesian translation, the merging UAV receives the message ready j and assigns itself the coordinates (0,0) (line 10).

Algorithm 4: Cartesian Coordinates: UAV n.   
Input:   
1) $N _ { n } - \mathbf { a }$ list of one-hop neighborsâ IDs of UAV n   
1: UAV n received a message $\mathsf { c a r t e s i a n } ( k , \theta _ { i } , \Delta _ { i } )$   
from UAV $k , k \in N _ { n }$   
2: If the message cartesian $( l , \theta _ { i } , \Delta _ { i } )$ was received   
( Î )earlier from some UAV l, send a message ${ \tt r e a d y } ( n )$ to   
UAV l.   
3: Send a message cartesian $( n , \theta _ { i } , \Delta _ { i } )$ to $N _ { n } ,$ except   
k .   
4: Calculate the Cartesian coordinates $( x _ { n } , y _ { n } )$ using the   
polar coordinates $( r _ { i , k } , \theta _ { i , k } - \theta _ { i } + \Delta _ { i } )$   
( +5: Broadcast the Cartesian coordinates $( x _ { n } , y _ { n } )$ to all $j ,$   
$j \in N _ { n } .$   
6: After receiving a response message $\mathtt { r e a d y } ( j )$ from all   
$j , j \in N _ { n } , j \neq k ,$ (, send ready n to UAV k.

Algorithm 3 describes the actions for any UAV in the merging swarms that receives a polar message. UAV n, after receiving this message for the first time (line 1), determines its polar coordinates $( r _ { i , n } , \theta _ { i , n } )$ and saves parameters $\varphi _ { i , n } , \psi _ { i , n }$ (line 3). ( )These parameters will be further utilized to create a unified polar coordinate system. Finally, UAV n sends a polar message to all its neighbors except for the UAV from which it received a polar message (line 4), and then waits for a response message angles. If UAV n receives a polar message again, it immediately sends an angles message to the sending UAV. When UAV n receives angles m, Ï, Ï from its neighbor m, it updates the values $\varphi ,$ ( ) Ï (line 5). The update is designed to find the minimum and maximum polar angles. When the angles message is received from all the neighbors of UAV n except for the UAV from which it received polar message, UAV n sends the angles message to the UAV from which it received polar (line 6). Repeating recursively, the message angles reaches the merging UAV.

Once the described procedures in Algorithms 2 and 3 are performed, all UAVs in the merging swarms have a pair of coordinates â Cartesian coordinates in the original swarms and polar coordinates computed with the help of the merging UAV. The goal of Algorithm 4 is to assign Cartesian coordinates to all UAVs in a new joint swarm. The steps are similar to Algorithm 3, but now the process is initiated by the cartesian message (line 1). After converting the coordinates to the Cartesian system (line 4), UAV n informs all its neighbors and sends them the message ready (line 5). This message is needed to notify the merging UAV that the transition to Cartesian coordinates is now complete.

## V. TOPOLOGICAL AND ROUTING METRICS

We now introduce metrics of interest reflecting the topological and routing performance of the proposed algorithm. First, the correlation metric is specified, and then we proceed with the routing one.

## A. Topological Metric

As an indicator of the similarity between physical and virtual network topologies, the so-called topology similarity index is used. This index is defined as the Pearson correlation coefficient between pairwise distances in the virtual and physical topologies, i.e.,

$$
K = \frac { c o v ( D _ { p h y s } , D _ { v i r t } ) } { \sigma _ { D _ { p h y s } } \sigma _ { D _ { v i r t } } } ,\tag{17}
$$

where $D _ { p h y s }$ and $D _ { v i r t }$ are the pairwise distance matrix for physical and virtual graphs respectively, cov is the covariance, and Ï is the standard deviation.

## B. Routing Metric

The main goal of the designed VCS system is to serve as a routing underlay for geographical routing. Observe that perfect matching of the physical and virtual topologies ensures that routing performance over them will be the same. However, when non-perfect matching is observed it is difficult to make definitive conclusions. To this aim, below we define a general routing metric that can be utilized for benchmarking the routing performance without resorting to specific details of various routing algorithms proposed so far.

Recall, that the network is represented by graph $G = ( V , A )$ The virtual coordinates of a UAV $i , i \in V$ = (, are denoted as $\mathbf { s } _ { i } =$ $( x _ { i } , y _ { i } , z _ { i } )$ =. All the vertices that are associated with UAV i are ( )contained in the set $S _ { i }$ . We introduce a set ${ \overline { { S _ { i } } } } .$ , such that ${ \overline { { S _ { i } } } } =$ $S _ { i } \cup \{ i \}$ =. The goal of the routing algorithm is to determine the path from the UAV i to the UAV k in a swarm over virtual and physical topologies. Further, let $n _ { k } ( i )$ be UAV to which data ( )is sent from UAV i over the path from i to k, $n _ { k } ( i ) \in \overline { { S _ { i } } }$ . To determine the route to UAV $n _ { k } ( i )$ , the following optimization problem should be solved

$$
n _ { k } ( i ) = \underset { j \in S _ { i } } { \arg \operatorname* { m i n } } r ( \mathbf { s } _ { j } , \mathbf { s } _ { k } ) , i \neq j .\tag{18}
$$

Basically, the solution for (18) looks for a UAV from $S _ { i }$ that is closest in a geographical sense to the destination, i.e., UAV k. Each UAV sends a message with probability $1 / N$ to 1one of the arbitrary N UAVs. We define a stochastic matrix $\mathbf { P } = [ P ( i , j ) ]$ and a unit vector $\mathbf { u } = ( 1 , 1 , \dots , 1 )$ . Matrix P = [ ( )] = (1characterizes routing and its elements are

$$
P ( i , j ) = \left\{ { \begin{array} { l l } { { \frac { 1 } { N } } \sum _ { k = 1 } ^ { N } \delta _ { n _ { k } ( i ) , j } , } & { i \neq j , } \\ { 1 / N , } & { i = j , } \end{array} } \right.\tag{19}
$$

where $j \in S _ { i } , \delta _ { n _ { k } ( i ) , j }$ takes a value of 1 if the routing from UAV i to UAV k includes a certain UAV and 0 otherwise.

By solving the matrix equation $\mathbf { p } \mathbf { P } = \mathbf { p } , \mathbf { p } ^ { T } \mathbf { u } = 1$ , the so-= = 1called routing vector p is derived. The ith element of p represents the proportion of the time UAV i is involved in the routing. The final metric is defined as

$$
\rho = \left\| \mathbf { p } _ { 1 } - \mathbf { p } _ { 2 } \right\| ,\tag{20}
$$

where $\mathbf { p } _ { 1 }$ and $\mathbf { p } _ { 2 }$ are vectors for physical and virtual graphs.

If the virtual graph exactly matches the physical one, then the routing will be performed over the same UAVs. Accordingly, the frequency of visiting UAVs in both graphs will be the same. In this ideal case $\mathbf { p } _ { 1 } = \mathbf { p } _ { 2 }$ and the metric $\| \mathbf { p } _ { 1 } - \mathbf { p } _ { 2 } \| = 0$ . When = = 0matching is imperfect, the constructed routes will be different and some components $\mathbf { p } _ { 1 }$ and $\mathbf { p } _ { 2 }$ will not coincide. It means that the routs in physical and virtual graphs are different, which influences the frequencies of visiting nodes. In the worst case, the routing in the graphs follows completely different routes and the metric takes value 2. It is caused by the low accuracy of virtual coordinates.

TABLE I  
SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N } }$ </td><td rowspan=1 colspan=1>NumberofUAVs</td><td rowspan=1 colspan=1>50 units</td></tr><tr><td rowspan=1 colspan=1> $\overline { { R } }$ </td><td rowspan=1 colspan=1>Transmission range</td><td rowspan=1 colspan=1>30,50m</td></tr><tr><td rowspan=1 colspan=1> $\overline { { L _ { 1 } , L _ { 2 } } }$ </td><td rowspan=1 colspan=1>Sides of the area</td><td rowspan=1 colspan=1>100m</td></tr><tr><td rowspan=1 colspan=1> $\overline { { L _ { 3 } } }$ </td><td rowspan=1 colspan=1>Topology (flat or 3D)</td><td rowspan=1 colspan=1>5 m,30 m</td></tr><tr><td rowspan=1 colspan=1> $g$ </td><td rowspan=1 colspan=1>Percentage of movingUAVs</td><td rowspan=1 colspan=1>100%</td></tr><tr><td rowspan=1 colspan=1> $v _ { R }$ </td><td rowspan=1 colspan=1>Relative UAV speed</td><td rowspan=1 colspan=1>0.1,3 m/s</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Positioning error</td><td rowspan=1 colspan=1>1,30 %</td></tr><tr><td rowspan=1 colspan=1>f</td><td rowspan=1 colspan=1>Synchronization impairment</td><td rowspan=1 colspan=1>On/Off</td></tr></table>

## VI. NUMERICAL RESULTS

In this section, we elaborate on our numerical results by assessing the performance of the proposed approach. We start with single UAV swarm performance by assessing the impact of different densities of UAVs, different types of topologies, relative mobility, and inaccuracy of distance estimates. As performance metrics of interest, we will utilize topological and routing metrics defined in Section V. The results of the single-step algorithm are compared with those reported in [43], where the gradual convergence approach has been proposed.

The system parameters are provided in Table I. We note that such parameters as the number of UAVs and sides of the considered area can vary depending on the application scenario. Transmission range values are based on the IEEE 802.11n/ac standards. The standardization efforts are still ongoing with respect to the UAV traffic regulations. As for the percentage of moving UAVs, we consider the worst case, when all the UAVs move with respect to each other. We underline that by introducing the relative speed of UAVs, we consider scenarios where UAVs have to dynamically change their trajectories due to presence of obstacles and thus move with respect to other UAVs in the swarm. For positioning error we consider the best case (1%) corresponding to the use of advanced localization techniques (e.g., based on time and angles of arrival) and worst case (30%) when the FSPL model is utilized for estimating the distance to the neighbors. Finally, we also consider that UAVs might lose connectivity with their neighbors due to imperfections of the communication technology. We take such scenarios into account by introducing a synchronization impairment parameter.

The considered scenario for performance assessment is as follows. In the initial phase, the UAVs are added one by one to the swarm every second corresponding to typical swarm initiation. Once all the considered number of UAVs are added, we introduce various impairments, such as mobility and loss of synchronization. First, the behavior of the single swarm system is observed for various realizations (trajectories) of UAV swarm in terms of topological and routing metrics. Here, the metrics of interest are topological and routing performance before and after merging.

<!-- image-->  
(a) Positioning error 1%

<!-- image-->  
(b) Positioning error 30%  
Fig. 4. Topological metric as a function of positioning error.

The Cartesian coordinate system is used to simulate mobility. Once all UAVs are connected to the network, a certain percentage of UAVs, g, is selected to be mobile. Here, we consider the worst-case scenario, where all UAVs are mobile, i.e., $g = 1 0 0 \%$ . The movement of UAVs is characterized by two = 100%parameters: the range of mobility and the relative UAV speed. The range of mobility of one UAV is limited by a compartment with dimensions $l _ { 1 } \times l _ { 2 } \times l _ { 3 }$ . In addition to mobility, UAVs in the network may suddenly lose synchronization (connectivity) with their neighbors. This process is simulated as follows. At each algorithm iteration dictated by the frequency of message exchanges between UAVs, a randomly selected UAV is removed from the swarm. The remaining UAVs in the network redefine their virtual coordinates without the removed UAV. In the next time step, the removed UAV appears in the swarm again and the network adapts its virtual coordinates according to the new information.

## A. Single Swarm Performance

We start with characterizing the sensitivity of the proposed approach to the accuracy of the positioning information. To this aim, Fig. 4 illustrates the topological characteristic as a function of time, for N   UAVs each having coverage of 50 m, where the height of the swarm is 5 m, there is no mobility and under perfect synchronization. Here, Fig. 4(a) shows the case of 1% positioning error that can be attained using advanced localization algorithms, while Fig. 4(b) corresponds to the 30%, i.e., the accuracy attained by the simple approaches such as those based on FSPL model. As one may observe, the proposed approach drastically outperforms the gradual convergence originally proposed in [43] by, e.g., 3-5 times. In fact, for the considered set of parameters, the proposed approach achieves a similarity of more than 90% between virtual and physical topologies. Note that this holds not only for static swarm behavior but also holds true during the UAV swarm formation phase, where UAVs are added one by one to the swarm.

<!-- image-->  
(a) Positioning error 1%

<!-- image-->  
(b) Positioning error 30%  
Fig. 5. Routing metric as a function of positioning error.

Analyzing the data presented in Fig. 4 further, one may observe that the accuracy of the distance estimates between UAVs utilized for virtual topology construction does not affect the performance of the proposed algorithm. That is, even introducing a positioning error of 30% only slightly deteriorates the considered metrics during both swarm formation and operational phases. Importantly, once the swarm is formed, the metric jumps to approximately 1.0.

Recall that topology matching does not ensure identical routing. Fig. 5 illustrates the corresponding routing performance of the proposed approach for the same set of chosen parameters. Recall that the range of the metric is (0,2) where 0 implies perfect matching of the shortest path routing. As one may observe, for both 1% and 30% of positioning error, the considered metric is close to zero with a slight increase observed for 30% case. Importantly, it holds for both formation and operational phases implying that data can be routed even when the swarm formation is not finalized. Finally, we highlight that the proposed approach outperforms the gradual convergence significantly.

<!-- image-->  
(aï¼ Topological metric

<!-- image-->  
(b) Routing metric  
Fig. 6. Topological and routing metrics for swarm height of 30 m.

The swarm topology considered in Figs. 4 and 5 assumes a nearly flat swarm formation with a height of just 5 m. When performing real missions, the formation may dynamically change, e.g., when avoiding obstacles. To this aim, Fig. 6 shows topological and routing metrics for swarm height of 30 m as compared to the Figs. 4 and 5, where the height is 5 m. The rest of the parameters and swarm behavior are the same. By cross comparing the illustrations, one may observe that both metrics slightly degrade. The reason is that higher swarm height leads to fewer one- and two-hop neighbors utilized by the drones to compute their locations in the virtual topology. One may observe similar behavior when the communications range of UAV decreases (not shown here). Thus, we may conclude that the proposed approach is best suited for dense UAV swarms.

The first typical impairment we consider is the relative mobility of UAVs in the swarm shown in Fig. 7 for topological metric and two relative mobilities 0.1 m/s and 3 m/s. Here, N = 50UAVs in the swarm, positioning error of 1%, swarm height of 5 m, and no temporal loss of synchronization between UAVs. There are two important observations. First by cross comparing the results in Fig. 7(a) and 4(a), one may deduce that slight relative mobility actually improves algorithms performance as an absolutely perfect topology match is observed in Fig. 7(a). This is due to the additional location relaxation factor for the optimization problem that is solved at each UAV. However, when the relative speed increases to 3 m/s the mobility becomes a deteriorating factor. Albeit, the topological metric still remains higher than 0.8.

<!-- image-->  
(a) Mobility speed is 0.1 m/s

<!-- image-->  
(b) Mobility speed is 3.0 m/s  
Fig. 7. Topological metric as a function of UAVsâ mobility speed.

Note that one may observe two types of âjumpsâ in the plots. The first âlargerâ type of jumps are caused by swarm topology changes. In the initial phase, the UAVs are added one by one to the swarm. Since the proposed algorithm depends on the number of neighboring UAVs and their location, continuously changing the number and location of neighbors affects the accuracy of the algorithm. However, once the swarm is formed, the algorithm is able to calculate the coordinates more precisely, which causes a significant improvement (jump) in the plot. The second type of jump is less significant and appears due to certain orientations of the UAVs. It may appear for several reasons: specific geometric positions of UAVs in the swarm (for instance, when a certain subset of drones make a âlineâ), lack of a sufficient number of neighbors at any given instant of time, etc.

Yet another impairment for UAV swarms is temporal loss of synchronization between UAVs. Recall that we model it by temporarily putting UAVs âoffâ and âonâ with a duration of 1 s. Fig. 8 illustrates the topological and routing metrics for N = 50UAVs in the swarm, positioning error of 1%, swarm height of 5 m, relative mobility of 1 m/s, and temporal flashing on/off UAV behavior. Similarly to the case of low mobility, flashing helps to improve the correlation between the physical and the virtual graph, making them more similar. A rationale for this behavior is again additional location relaxation in the virtual domain induced by the partial absence of connected UAVs. One may observe that once the swarm is formed, the correlation value remains close to 1 for the rest of the experiments.

<!-- image-->  
(a) Positioning error 1%

<!-- image-->  
(b) Positioning error 10%  
Fig. 8. Topological metric as a function of UAVsâ mobility speed.

Another important impairment is the loss of packets utilized for exchange of the sets of neighbors between adjacent UAVs in a swarm. These losses may happen as a result of e.g., fast fading phenomenon. Fig. 9 demonstrates the algorithm behavior in the case when the packets are lost with the probability 0.05 and 0.1. Numerical results reveal that the proposed algorithm isnât affected significantly by packetsâ loss. With a loss probability of 0.05, the proposed algorithm achieves a similarity of more than 90% between virtual and physical topologies (Fig. 9(a)). The probability of 0.1 slows down the process, nevertheless, the final value of correlation is more than 90%. Fig. 9(b) shows behavior of the routing-based metric. With the range of (0, 2), where 0 implies perfect matching of the shortest path routing in physical and virtual graphs, the metric is close to zero.

Finally, Fig. 10 illustrates the impact of swarm density on topological and routing-based metrics. As one may note, the suggested algorithm is more suitable for dense swarms. The correlation between topologies increases together with the number of UAVs. The same can be said about the routing-based metric â the metric shows the worst results for sparse swarms, while swarms with 70 and 100 UAVs provide better results.

<!-- image-->  
(a) Topological metric

<!-- image-->  
(b) Routing-based metric

Fig. 9. Topological and routing metrics as a function of packet loss.  
<!-- image-->  
(a) Topological metric

<!-- image-->  
(b) Routing-based metric  
Fig. 10. Topological and routing metrics as a function of UAVsâ density.

<!-- image-->  
(a) Positioning error 1%

<!-- image-->  
(b) Positioning error 10%  
Fig. 11. Topological metric during the merging of two clusters.

(a) Positioning error 1%  
<!-- image-->  
(b) Positioning error 10%

<!-- image-->  
Fig. 12. Routing metric during the merging of two clusters.

## B. Merging Performance

We now proceed assessing the merging performance of the proposed algorithm. The assumed scenario is where two UAV swarms are gradually formed by adding one node at a time until the number of UAVs in each swarm reaches 25. Then, each swarm has 10 time steps to update their virtual coordinates, after which the merging process starts. Initially, each swarm, called cluster hereafter, has its own VCS, thereby the task is to translate the virtual coordinates of the two clusters into a unified system.

Fig. 11 presents the topological correlation metric before and after the merging of clusters for 1% and 10% positioning errors in Fig. 11(a) and (b), respectively. We consider the case of the merging of two clusters, each containing 25 nodes, swarm height of 5 m. Two cases are compared: positioning error of 1% and 10%. For the first 25 time steps, the nodes of the clusters exist separately, as reflected by the orange and blue curves. From 26 to 35 time steps the virtual coordinates are recalculated according to the proposed algorithm. Starting from 40th time step, one may observe the green curves which show the correlation metric for the joint cluster.

First of all, observe that there is no principal difference between 1% and 10% of positioning error which is in line with previous observations for single swarm performance. Further, the considered metric for initial clusters having 25 UAVs reaches approximately 0.5 and 0.6 for 1% and 10% of positioning error, respectively, and then, once all UAVs have joined the overlay, the correlation metric improves to 0.9. The merging process initially incurs imperfections into VCS address allocations that is reflected by the topological metric being smaller than 0.8 in both cases just after the merging is complete. However, immediately after it starts to increase reaching the value of 0.9 for 1% of positioning error already after 10 time steps. For 10% error, it remains almost intact. Thus, one may conclude that the merging process does not affect long-lasting performance degradation in the VCS operation. Fig. 12 presents the routing metric before and after the merging process for the same set of chosen parameters. It is noticeable that this metric has greater values right after the merging but, nevertheless, they are well below 1. The rationale is that the topology changes and so do the routes, thus, further updates are required to improve the value.

## VII. CONCLUSION

To enable timely coordination and information exchange, the swarms of UAVs performing the missions in GNSS-denied environments such as deep woods, mountains, or indoors, need to be able to maintain their topology at all times. Motivated by this task, in this paper, we developed a set of algorithms for topology organization and maintenance without the use of external positioning information for UAV swarms. The developed algorithms are entirely distributed, utilize limited information about the proximity of UAVs that can be exchanged in link control messages such as âhelloâ beacons, and may tolerate inherent dynamics of UAV swarms in terms of loss of link synchronization and mobility. The developed algorithm is complemented with essential UAV swarms merging and disjoining functionality delivering the whole package for reliable UAV operation in hostile environments.

The performance of the proposed algorithm was investigated using both topological and routing performance metrics. Our results reveal that the algorithm is robust to the positioning error for directly connected UAV nodes and may tolerate up to 30% of error. Both mobility and synchronization loss events are handled with limited performance degradation. Finally, we showed that the merging functionality does not affect the algorithm performance and its impact lasts for 20-50 times steps which is equivalent to a few seconds or even less in real-time scenarios.

Several directions for future research are considered. First, the algorithmâs sensitivity to the loss of signal packets is to be investigated. The threshold of acceptable losses is of particular interest. Second, frequent disconnection and connection of drones results in significant overhead, which could potentially be avoided by applying some heuristics on top of the algorithm. Lastly, the algorithm should be tested in real-life settings to analyze its scalability and robustness in different environments with various numbers of UAVs and obstacles. The goal is to refine the algorithmâs parameters and identify potential limitations.

## SOURCE ACCESS

The source code used to produce results for this paper is available at https://github.com/gaydamanya/GAR.git.

## REFERENCES

[1] A. LÃ³pez, J. M. Jurado, C. J. Ogayar, and F. R. Feito, âA framework for registering UAV-based imagery for crop-tracking in precision agriculture,â Int. J. Appl. Earth Observ. Geoinformation, vol. 97, 2021, Art. no. 102274. [Online]. Available: https://www.sciencedirect.com/ science/article/pii/S030324342030917X

[2] T. Hu et al., âDevelopment and performance evaluation of a very lowcost UAV-Lidar system for forestry applications,â Remote Sens., vol. 13, no. 1, 2021, Art. no. 77. [Online]. Available: https://www.mdpi.com/2072- 4292/13/1/77

[3] C. Liu and T. SzirÃ¡nyi, âReal-time human detection and gesture recognition for on-board UAV rescue,â Sensors, vol. 21, no. 6, 2021, Art. no. 2180. [Online]. Available: https://www.mdpi.com/1424--8220/21/6/2180

[4] H. S. Munawar, H. Inam, F. Ullah, S. Qayyum, A. Z. Kouzani, and M. A. P. Mahmud, âTowards smart healthcare: UAV-Based optimized path planning for delivering COVID-19 self-testing kits using cutting edge technologies,â Sustainability, vol. 13, no. 18, 2021, Art. no. 10426. [Online]. Available: https://www.mdpi.com/2071--1050/13/18/10426

[5] E. Montero et al., âProactive radio- and QoS-aware UAV as BS deployment to improve cellular operations,â Comput. Netw., vol. 200, 2021, Art. no. 108486. [Online]. Available: https://www.sciencedirect.com/ science/article/pii/S138912862100431X

[6] Z. Xiao, H. Dong, L. Bai, D. O. Wu, and X.-G. Xia, âUnmanned aerial vehicle base station (UAV-BS) deployment with millimeter-wave beamforming,â IEEE Internet Things J., vol. 7, no. 2, pp. 1336â1349, Feb. 2020.

[7] S. K. Khan, U. Naseem, H. Siraj, I. Razzak, and M. Imran, âThe role of unmanned aerial vehicles and mmWave in 5G: Recent advances and challenges,â Trans. Emerg. Telecommun. Technol., vol. 32, no. 7, 2021, Art. no. e4241.

[8] Q. Wu et al., âA comprehensive overview on 5G-and-beyond networks with UAVs: From communications to sensing and intelligence,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 2912â2945, Oct. 2021.

[9] J. Wubben, F. Fabra, C. T. Calafate, J.-C. Cano, and P. Manzoni, âA novel resilient and reconfigurable swarm management scheme,â Comput. Netw., vol. 194, 2021, Art. no. 108119. [Online]. Available: https: //www.sciencedirect.com/science/article/pii/S138912862100195X

[10] Y. Zhou, B. Rao, and W. Wang, âUAV swarm intelligence: Recent advances and future trends,â IEEE Access, vol. 8, pp. 183856â183878, 2020.

[11] A. Sharma, S. Shoval, A. Sharma, and J. K. Pandey, âPath planning for multiple targets interception by the swarm of UAVs based on swarm intelligence algorithms: A. review,â IETE Tech. Rev., vol. 39, pp. 675â697, 2022.

[12] A. Puente-Castro, D. Rivero, A. Pazos, and E. Fernandez-Blanco, âA review of artificial intelligence applied to path planning in UAV swarms,â Neural Comput. Appl., vol. 34, pp. 153â170, 2022.

[13] B. Karp and H.-T. Kung, âGPSR: Greedy perimeter stateless routing for wireless networks,â in Proc. 6th Annu. Int. Conf. Mobile Comput. Netw., 2000, pp. 243â254.

[14] S. Medjiah, T. Ahmed, and F. Krief, âAGEM: Adaptive greedy-compass energy-aware multipath routing protocol for WMSNs,â in Proc. IEEE 7th Consum. Commun. Netw. Conf., 2010, pp. 1â6.

[15] S.-J. Lee, M. Gerla, and C.-K. Toh, âA simulation study of table-driven and on-demand routing protocols for mobile ad hoc networks,â IEEE Netw., vol. 13, no. 4, pp. 48â54, Jul./Aug. 1999.

[16] P. Jacquet, P. Muhlethaler, T. Clausen, A. Laouiti, A. Qayyum, and L. Viennot, âOptimized link state routing protocol for ad hoc networks,â in Proc. IEEE Int. Multi Topic Conf., 2001, pp. 62â68.

[17] C. E. Perkins, E. M. Royer, S. R. Das, and M. K. Marina, âPerformance comparison of two on-demand routing protocols for ad hoc networks,â IEEE Pers. Commun., vol. 8, no. 1, pp. 16â28, Feb. 2001.

[18] H. Saha et al., âA low cost fully autonomous GPS (global positioning system) based quad copter for disaster management,â in Proc. IEEE 8th Annu. Comput. Commun. Workshop Conf., 2018, pp. 654â660.

[19] S.-S. Choi and E.-K. Kim, âDesign and implementation of vision-based structural safety inspection system using small unmanned aircraft,â in Proc. 17th Int. Conf. Adv. Commun. Technol., 2015, pp. 562â567.

[20] M. Asadpour, K. A. Hummel, D. Giustiniano, and S. Draskovic, âRoute or carry: Motion-driven packet forwarding in micro aerial vehicle networks,â IEEE Trans. Mobile Comput., vol. 16, no. 3, pp. 843â856, Mar. 2017.

[21] S. Ashraf, P. Aggarwal, P. Damacharla, H. Wang, A. Y. Javaid, and V. Devabhaktuni, âA low-cost solution for unmanned aerial vehicle navigation in a global positioning systemâdenied environment,â Int. J. Distrib. Sensor Netw., vol. 14, no. 6, 2018, Art. no. 1550147718781750, doi: 10.1177/1550147718781750.

[22] W. Power, M. Pavlovski, D. Saranovic, I. Stojkovic, and Z. Obradovic, âAutonomous navigation for drone swarms in GPS-denied environments using structured learning,â in Artificial Intelligence Applications and Innovations, I. Maglogiannis, L. Iliadis, and E. Pimenidis, Berlin, Germany: Springer, 2020, pp. 219â231.

[23] M. Campion, P. Ranganathan, and S. Faruque, âUAV swarm communication and control architectures: A review,â J. Unmanned Veh. Syst., vol. 7, no. 2, pp. 93â106, 2019, doi: 10.1139/juvs-2018â0009.

[24] D. Mishra and E. Natalizio, âA survey on cellular-connected UAVs: Design challenges, enabling 5G/B5G innovations, and experimental advancements,â Comput. Netw., vol. 182, 2020, Art. no. 107451. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S1389128620311324

[25] X. Chen, J. Tang, and S. Lao, âReview of unmanned aerial vehicle swarm communication architectures and routing protocols,â Appl. Sci., vol. 10, 05 2020, Art. no. 3661.

[26] A. Kohlbacher, J. Eliasson, K. Acres, H. Chung, and J. C. Barca, âA low cost omnidirectional relative localization sensor for swarm applications,â in Proc. IEEE 4th World Forum Internet Things, 2018, pp. 694â699.

[27] S. Hameed et al., âConnectivity of drones in FANETs using biologically inspired dragonfly algorithm (DA) through machine learning,â Wireless Commun. Mobile Comput., vol. 2022, pp. 1â11, 2022.

[28] W. Wang, P. Bai, Y. Zhou, X. Liang, and Y. Wang, âOptimal configuration analysis of AOA localization and optimal heading angles generation method for UAV swarms,â IEEE Access, vol. 7, pp. 70117â70129, 2019.

[29] J. Zheng et al., âAn efficient strategy for accurate detection and localization of UAV swarms,â IEEE Internet Things J., vol. 8, no. 20, pp. 15372â15381, Oct. 2021.

[30] H. Qin et al., âAutonomous exploration and mapping system using heterogeneous UAVs and UGVs in GPS-denied environments,â IEEE Trans. Veh. Technol., vol. 68, no. 2, pp. 1339â1350, Feb. 2019.

[31] S. Misra, B. Wang, K. Sundar, R. Sharma, and S. Rathinam, âSingle vehicle localization and routing in GPS-denied environments using range-only measurements,â IEEE Access, vol. 8, pp. 31004â31017, 2020.

[32] F. She, Y. Zhang, D. Shi, H. Zhou, X. Ren, and T. Xu, âEnhanced relative localization based on persistent excitation for multi-UAVs in GPS-denied environments,â IEEE Access, vol. 8, pp. 148136â148148, 2020.

[33] R. Moraes and E. Pignaton de Freitas, âDistributed control for groups of unmanned aerial vehicles performing surveillance missions and providing relay communication network services,â J. Intell. Robotic Syst., vol. 92, pp. 645â656, 2018.

[34] A. Rao, S. Ratnasamy, C. Papadimitriou, S. Shenker, and I. Stoica, âGeographic routing without location information,â in Proc. 9th Annu. Int. Conf. Mobile Comput. Netw., 2003, pp. 96â108.

[35] T. Watteyne, I. AugÃ©-Blum, M. Dohler, S. UbÃ©da, and D. Barthel, âCentroid virtual coordinatesâa novel near-shortest path routing paradigm,â Comput. Netw., vol. 53, no. 10, pp. 1697â1711, 2009. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S1389128608004325

<!-- image-->

[36] B. Leong, B. Liskov, and R. Morris, âGreedy virtual coordinates for geographic routing,â in Proc. IEEE Int. Conf. Netw. Protoc., 2007, pp. 71â80.

[37] A. Karima, B. Mohammed, and B. Azeddine, âNew virtual coordinate system for improved routing efficiency in sensor network,â Int. J. Comput. Sci. Issues, vol. 9, no. 3, 2012, Art. no. 59.

[38] N. Filardi, A. Caruso, and S. Chessa, âVirtual naming and geographic routing on wireless sensor networks,â in Proc. IEEE 12th Symp. Comput. Commun., 2007, pp. 609â614.

[39] J.-P. Sheu, K.-Y. Hsieh, and M.-L. Ding, âRouting with hexagonal virtual coordinates in wireless sensor networks,â Wireless Commun. Mobile Comput., vol. 9, no. 9, pp. 1206â1219, 2009.

[40] S. Ratnasamy, I. Stoica, and S. Shenker, âRouting algorithms for DHTs: Some open questions,â in Proc. Int. Workshop Peer-to-Peer Syst., 2002, pp. 45â52.

[41] R. Anwit, P. Kumar, and M. Singh, âVirtual coordinates routing using VCP-M in wireless sensor network,â in Proc. Int. Conf. Comput. Intell. Commun. Netw., 2014, pp. 402â407.

[42] A. Awad, R. German, and F. Dressler, âExploiting virtual coordinates for improved routing performance in sensor networks,â IEEE Trans. Mobile Comput., vol. 10, no. 9, pp. 1214â1226, Sep. 2011.

[43] A. Samuylov, D. Moltchanov, R. Kovalchukov, A. Gaydamaka, A. Pyattaev, and Y. Koucheryavy, âGAR: Gradient assisted routing for topology self-organization in dynamic mesh networks,â Comput. Commun., vol. 190, pp. 10â23, 2022.

Anna Gaydamaka (Graduate Student Member, IEEE) received the MSc degree in computer science, program data science and business informatics) from Universita di Pisa, Italy, in 2021. She is currently working toward the PhD degree in computing and electrical engineering and working as a doctoral researcher with Tampere University, Finland. Her research interests include resource planning of the fifth and sixth-generation wireless network, mathematical models for performance KPIs optimization, and machine learning techniques.

[44] S. Chahal and M. Singh, âAn extensive literature review of various routing protocols in delay tolerant networks,â Int. Res. J. Eng. Technol., vol. 4, no. 7, pp. 1309â1312, 2017.

[45] G. He, âDestination-sequenced distance vector (DSDV) protocol,â Netw. Lab. Helsinki Univ. Technol., vol. 135, pp. 1â9, 2002.

[46] T. Clausen and P. Jacquet, âOptimized link state routing protocol (OLSR),â IETF, Tech. Rep., 2003.

[47] S. Mohapatra and P. Kanungo, âPerformance analysis of AODV, DSR, OLSR and DSDV routing protocols using NS2 simulator,â Procedia Eng., vol. 30, pp. 69â76, 2012.

[48] C. E. Perkins and E. M. Royer, âAd-hoc on-demand distance vector routing,â in Proc. IEEE 2nd Workshop Mobile Comput. Syst. Appl., 1999, pp. 90â100.

[49] G. Pei, M. Gerla, and T.-W. Chen, âFisheye state routing: A routing scheme for ad hoc wireless networks,â in Proc. IEEE Int. Conf. Commun. Glob. Convergence Through Commun. Conf. Rec., 2000, pp. 70â74.

[50] F. Cadger, K. Curran, J. Santos, and S. Moffett, âA survey of geographical routing in wireless ad-hoc networks,â IEEE Commun. Surv. Tut., vol. 15, no. 2, pp. 621â653, Second Quarter 2013.

[51] L. A. L. da Costa, R. Kunst, and E. Pignaton de Freitas, âQ-FANET: Improved Q-learning based routing protocol for FANETs,â Comput. Netw., vol. 198, 2021, Art. no. 108379. [Online]. Available: https://www. sciencedirect.com/science/article/pii/S1389128621003595

[52] P. Nain, D. Towsley, B. Liu, and Z. Liu, âProperties of random direction models,â in Proc. IEEE 24th Annu. Joint Conf. IEEE Comput. Commun. Societies., 2005, pp. 1897â1907.

[53] S. Ruder, âAn overview of gradient descent optimization algorithms,â 2016. [Online]. Available: https://arxiv.org/abs/1609.04747

[54] C.-J. Hsieh and I. S. Dhillon, âFast coordinate descent methods with variable selection for non-negative matrix factorization,â in Proc. 17th ACM SIGKDD Int. Conf. Knowl. Discov. Data Mining, New York, NY, USA, 2011, pp. 1064â1072, doi: 10.1145/2020408.2020577.

<!-- image-->

[55] R. S. Sutton et al., âFast gradient-descent methods for temporal-difference learning with linear function approximation,â in Proc. 26th Annu. Int. Conf. Mach. Learn., New York, NY, USA, 2009, pp. 993â1000, doi: 10.1145/1553374.1553501.

Andrey Samuylov received the MsC degree in applied mathematics and the CandSc degree in physics and mathematics from the RUDN University, Russia, in 2012 and 2015, respectively. Since 2015 he is working with Tampere University as a researcher, working on analytical performance analysis of various 5G wireless networks technologies. His research interests include P2P networks performance analysis, performance evaluation of wireless networks with enabled D2D communications, and mmWave-band communications.

<!-- image-->

Dmitri Moltchanov received the MSc and CandSc degrees from the St. Petersburg State University of Telecommunications, Russia, in 2000 and 2003, respectively, and the PhD degree from TUT, in 2006. He is a university lecturer with Tampere University. He has authored more than 150 publications and has taught more than 60 courses on several topics in telecommunications. His current research interests include research and development of 5G/5G+ systems, industrial IoT applications, mission-critical V2V/V2X systems, and blockchain technologies.

<!-- image-->

Mateen Ashraf received PhD degree in wireless communication engineering, in 2017. He is currently working as a research fellow with Tampere University. His current research interests include beamforming design for integrated sensing and communication (ISAC) systems for 6G networks and wireless energy harvesting systems. He has published several journal and conference papers in leading IEEE journals and conferences. He is an active reviewer of many leading journals and has acted as a TPC member for prestigious IEEE conferences.

<!-- image-->

Bo Tan (Member, IEEE) received the PhD degree from the Institute for Digital Communications, The University of Edinburgh, U.K., in 2013. From 2012 to 2016, he was a postdoctoral researcher at the University College London and the University of Bristol, U.K., contributing to passive radar research and applications in healthcare and security. From 2017 to 2018, he was a lecturer at Coventry University, U.K.; since 2019, he has been a Tenure Track assistant professor with Tampere University, Finland. His research interests include radio signal processing, sensing and

connectivity for intelligent machines. He is PI and coordinator of multiple Academy of Finland, Business Finland and Horizon European research projects on distributed machine learning, mmWave, positioning, surveillance, physical layer security, and radio sensing for healthcare. He is the reviewer of multiple IEEE/IET/ACM journals and conferences in wireless communications, radar, pervasive computing, and sensing.

<!-- image-->

Yevgeni Koucheryavy received the PhD degree from the Tampere University of Technology (TUT), Finland. He is currently a professor with the Laboratory of Electronics and Communications Engineering, TUT. He is the author of numerous publications in the field of advanced wired and wireless networking and communications. His current research interests include various aspects in heterogeneous wireless communication networks and systems, the Internet of Things and its standardization, and nanocommunications. He is associate technical editor of IEEE

Communications Magazine and an editor of IEEE Communications Surveys and Tutorials.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_7_img_1.jpeg|page_7_img_1]]
3. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_14_img_1.png|page_14_img_1]]
4. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_14_img_2.png|page_14_img_2]]
5. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_16_img_1.jpeg|page_16_img_1]]
6. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_16_img_2.jpeg|page_16_img_2]]
7. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_16_img_3.jpeg|page_16_img_3]]
8. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_16_img_4.jpeg|page_16_img_4]]
9. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_17_img_1.jpeg|page_17_img_1]]
10. [[../extracted_images/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo/page_17_img_2.jpeg|page_17_img_2]]

---

