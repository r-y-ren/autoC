# Fission Spectral Clustering Strategy for UAV Swarm Networks

Gepeng Zhu , Haipeng Yao , Senior Member, IEEE, Tianle Mai , Member, IEEE, Zunliang Wang , Graduate Student Member, IEEE, Di Wu , Student Member, IEEE, and Song Guo , Fellow, IEEE

AbstractâThe flying ad hoc networks (FANETs) have attracted a large amount of attention from both academia and industry. Benefiting from the flexibility, the FANETs have been widely deployed in various scenarios, ranging from agricultural production to emergency rescue. However, in FANETs, the mobility of unmanned aerial vehicles (UAVs) has led to critical challenges for the stability of communications. Especially, the routing flooding mechanism extremely limits the scalability of FANET. To overcome these technical challenges, constructing a hierarchy and clustering structure in FANETs is considered a promising solution. In this paper, we propose the fission spectral clustering (FSC) strategy for UAV swarm networks. We model the UAV clustering problem as a graph cut problem. The time-sequential attributes weight of nodes and edges will be input to the FSC algorithm. Then, it will construct the Laplace matrix and calculate the first k-th eigenvectors of it. We apply the K-Means algorithm into this feature space to cut the graph by clustering the eigenvectors. Each cluster will constantly fission with this strategy until it satisfies the size and structure constraints in the UAV clusters. Some simulations are implemented to evaluate our proposed algorithm in comparison to the other state-of-the-art solutions.

Index Termsâflying ad hoc networks (FANETs), spectral clustering, UAV swarm networks.

## I. INTRODUCTION

T HE unmanned aerial vehicle (UAV) swarm as the mostpowerful and exciting technology has quickly become a powerful and exciting technology has quickly become a disruptive force reshaping how we live and work. UAV swarm refers to a coordinated unit of UAVs that work together to accomplish a specific task. Advantages to UAV swarm include easy deployable, time-savings, and reduction in operational expenses. Benefiting from the above advantages, the UAV swarm can be widely used in many fields ranging from disaster management to military operations [1]. However, compared to the terrestrial networks, UAV swarm networks possess the characteristic of dynamic topology, unstable links, self-organizing, and lack of central control. These characteristics result in a new network paradigm, termed flying ad-hoc networks (FANETs).

However, because of its unique nature, many network protocols of fixed networks will be no longer suitable in FANETs. Especially, the current flooding-based routing protocol extremely limits the scale of FANET. Once the network topology changes, flooding will be triggered to establish the new routing table, and therefore bring huge communication overhead in such dynamic networks.

Clustering, as a network organization method, can effectively prevent wide-range network flooding. The UAVs swarm is divided into several clusters, where each cluster is composed of one elected Cluster Head (CH) and several Cluster Members (CMs) [2]. In the UAV network, CH is responsible for cooperative information sharing between clusters and the management of all the CMs within the same cluster [3]. Based on this clustered structure, information transmission is hierarchical, which greatly reduces flooding overhead.

The typical UAV swarm clustering algorithms include the lowest ID algorithm (LOWID) [4], the highest node degree algorithm (HIGHD) [5], and the weight-based clustering algorithm (WCA) [6]. However, these algorithms neglect wireless link attributes (e.g. wireless link quality, wireless link connection duration, etc.). Therefore, the communication performance of the UAV swarm is always unsatisfactory after clustering. How to maintain high communication performance in the clustered UAV swarm is a critical challenge.

To address this challenge, spectral clustering (SC) becomes a viable option. SC is an unsupervised technology based on graph theory [7], which has been applied in the network field, such as load balancing [8], wireless communication [9], and so on. It treats UAVs as graphâs vertexes and the wireless link between UAVs as graphâs edges. The weight value of the edge reflects the communication quality of the link. SC transforms the UAV clustering problem into a graph cut problem. It aims to maximize the edge weights in the subgraph and minimize the edge weights between the subgraphs. Therefore, the high-performance communication link will be retained during clustering.

However, the SC algorithm is unstable in the clustering process, which performs in uncontrollable size and structure of each cluster. To achieve a more reasonable cluster result, in this paper, we design a fission spectral clustering (FSC) strategy for UAV networks. FSC generates clusters by fission and stops the cluster fission process when it satisfies the constraints of size and structure. Moreover, the traditional SC algorithm adopts a static clustering scheme, and therefore cannot be applied to dynamic networks. Therefore, we propose that the effective value of the link represents the communication capability of the link within a specific time slot, enabling the capture of time-sequential wireless link attributes.

The major contributions of this paper can be summarized as follows:

We model the time-sequential attributes of nodes and edges as the link effective value, which can be further applied to the proposed FSC clustering algorithm.

We propose the FSC algorithm to cluster the UAV swarm. FSC continuously clusters the UAV swarm by cutting off the edges with small weight values and keeping the edges with large weight values, where the cluster will fission until it satisfies the constraints of size and structure.

We propose an on-demand cluster maintenance mechanism. It decides whether each cluster needs to fission by considering its size and structure in each time slot, therefore greatly reducing the computing overhead.

The rest of this paper is organized as follows. In Section II, we review the related works. In Section III, we present the system model and present the optimization problem. In Section IV, we propose the FSC algorithm to solve the UAV swarm clustering problem. In Section V, we present the simulation results. Finally, Section VI discusses the conclusion.

## II. RELATED WORKS

Recently, a large and growing body of literature has investigated the clustering strategies for UAV networking. Concurrently, the research of spectral clustering algorithms in networking has garnered growing interest from both industry and academia. This section provides a concise overview of the existing methods in these domains.

## A. Energy Efficiency-Based UAV Swarm Clustering

In [10], Lv et al. proposed a low-energy uneven clustering (LEUC) based topology control algorithm. The algorithm adopts a three-stage (the election of candidate cluster heads, the competition of temporary cluster heads, the generation of formal cluster heads) cluster head election mechanism. In [11], Wang et al. examined joint beamforming and power allocation schemes as well as trajectory learning and clustering mechanisms for dynamically connectable unmanned aerial vehicle (UAV) base stations (BSs). On this basis, they proposed a dynamic UAV moving and clustering policy where the expected sum rate of the system is maximized while adapting to changes in the usersâ locations and environment. In [12], Qu et al. proposed an improved K-Means(UB-KMeans) algorithm to achieve our goals of minimizing the number of UAVs and minimizing the maximum deployment delay in the emergency response scenario.

## B. Mobility-Based UAV Swarm Clustering

In [13], Pathak et al. proposed an optimized stable clustering algorithm that will provide more stability to the network by minimizing the cluster head changes and reducing clustering overhead. In [14], Arafat et al. propose an energy-efficient swarm-intelligence based clustering (SIC) algorithm based on PSO, in which the particle fitness function is exploited for inter-cluster distance, intra-cluster distance, residual energy, and geographic location. In [15], Wang et al. proposed a clustering strategy based on bandwidth equalization. The strategy calculated the best number of clusters in the current network based on bandwidth balance and then used the K-means algorithm to quickly cluster the entire network.

## C. Energy Efficiency and Mobility-Based UAV Swarm Clustering

In [16], Ahmad et al. proposed a clustering algorithm based on a memetic algorithm (MA). MA used local exploration techniques to reduce the likelihood of early convergence. The local search function in MA was to find the optimal local solution before other evolutionary algorithms. In [17], Xiao et al. proposed a clustering algorithm based on communication overhead and link stability. The algorithm contained two sub-stages, a clustering method based on multi-parameter-limited overhead to select resource directory index nodes for resource information management in the clustering stage and a network clustering adaptive adjustment algorithm based on link stability in the maintenance stage. In [18], Sun et al. proposed an adaptive enhanced weighted clustering algorithm. This algorithm is not only based on the consideration of the optimal node degree and the distance between the cluster head and neighbor nodes, but also introduces the average link retention rate between UAVs and energy consumption. In [19], Sousa et al. proposed a framework for the decentralized distribution of multi-UAV fleets for on-demand aerial services, addressing strategic and tactical decision-making related to dimensioning and design of aerial networks. They used a soft clustering approach to handling data uncertainty, which resulted in increasing the flexibility and faulttolerance of the networked system. In [20], Duan et al. proposed an optimized weighted clustering algorithm. The algorithm is used to divide the network into clusters and assign different weights to different nodes to form clusters. Experiments showed that the algorithm can improve the performance of large-scale mobile ad hoc networks effectively.

## D. The Application of Spectral Clustering in Networking

In [21], chen et al. proposed hyper-graph spectral clustering based (HGSC) algorithm to deal with the strong interference and severe cumulative interference in dense heterogeneous network. The algorithm constructed the hyper-graph of user pairs and clusters them. Experiments showed that this algorithm can effectively eliminate the interferences between clusters and improve the system throughput. In [22], Jabbar et al. proposed vehicularhypergraph-based spectral clustering model. This model constructed the distance proximity matrix and clustered the vehicular nodes. This clustering method improved the stability of CH and reduced the overhead caused by CH shifting. In [23], Lin et al. proposed a detailed one-way two-lane vehicle mmWave communication network model. In this model, the sub-networks are decomposed by spectral clustering algorithm to solve the beam resource allocation optimization problem. The simulation results showed that proposed model can achieve a significant improvement in spectrum utilization and system throughput. In [24], Atev et al. proposed a method that was suitable for clustering of vehicle trajectories obtained by an automated vision system. The method combined ideas from two spectral clustering algorithms and designed a trajectory-similarity measure based on the Hausdorff distance, which can improve its robustness. Experiments showed that proved algorithm can improve the trajectory similarity of vehicles.

<!-- image-->  
Fig. 1. UAV network clustering.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, we first introduce the network system model. Then, we model the channel and relevant properties. Finally, we present the optimization problem of communication performance. For a clear exposition, the primary notations are summarized in Table I.

## A. System Model

As shown in Fig. 1, N UAVs are deployed in a 3D space. The set of UAVs are indicated as $\mathcal { N } = \{ 1 , 2 , . . . , N \}$ . N UAVs are = 1 2divided into several clusters. In each UAV cluster, we elect one CH to gather the information of CMs in the network. We abstract the UAV network as a graph $G = ( V , E )$ , where V represents = ( )the N UAV nodes and E represents the set of edges. We define $( i , j ) \in E ^ { t }$ if UAV i and UAV j are neighbors. Otherwise, $( i , j ) \notin E ^ { t }$ . The neighbors are conditioned on the minimum ( )threshold value of the signal-to-noise ratio (SINR) between two UAVs.

In high dynamic UAV networks, the perception of features is discrete with a one-cycle interval [25]. Therefore, in this paper, we analyze the UAV network based on the time slot. We set the maximum flight time of all UAVs as T and divide it into several equally spaced time slots. Let Ï denote the length of each time slot and the s-th time slot is denoted by $( T _ { s } , T _ { s } + \tau )$ . To further ( + )describe the connection relationship between UAVs, we model the mobility and channel as follows.

## B. Mobility Model

UAVs are deployed in a three-dimensional space and the range is $( x _ { \mathrm { m i n } } , y _ { \mathrm { m i n } } , z _ { \mathrm { m i n } } ) \sim ( x _ { \mathrm { m a x } } , y _ { \mathrm { m a x } } , z _ { \mathrm { m a x } } )$ , where xmin, ymin, zmin, xmax, ymax, $z _ { \mathrm { m a x } }$ represent the minimum and maximum values for the x-axis, y-axis, and z-axis, respectively. The position $\mathbf { p } _ { i , T _ { s } }$ and speed $\mathbf { u } _ { i , T _ { s } }$ of UAV i at time $T _ { s }$ can be denoted by

TABLE I RELATED DEFINITIONS
<table><tr><td rowspan=1 colspan=1>Notations</td><td rowspan=1 colspan=1>Descriptions</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>Total flight time of UAV</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>Length of each time-slot</td></tr><tr><td rowspan=1 colspan=1> $\mathcal { N }$ </td><td rowspan=1 colspan=1>The set of N UAVs</td></tr><tr><td rowspan=1 colspan=1> $G = ( V , E )$ </td><td rowspan=1 colspan=1>UAV network graph, where V represents the NUAV nodes and E represents the set of edges</td></tr><tr><td rowspan=1 colspan=1> $P$ </td><td rowspan=1 colspan=1>The transmission power of UAV</td></tr><tr><td rowspan=1 colspan=1> $h$ </td><td rowspan=1 colspan=1>Channel gain</td></tr><tr><td rowspan=1 colspan=1> $\alpha$ </td><td rowspan=1 colspan=1>Mean path-loss exponent</td></tr><tr><td rowspan=1 colspan=1> $\sigma ^ { 2 }$ </td><td rowspan=1 colspan=1>Noise power</td></tr><tr><td rowspan=1 colspan=1> $d _ { i , j , T _ { s } }$ </td><td rowspan=1 colspan=1>Physical distance between UAV i and UAV j attime $T _ { s }$ </td></tr><tr><td rowspan=1 colspan=1> $B$ </td><td rowspan=1 colspan=1>Channel bandwidth</td></tr><tr><td rowspan=1 colspan=1> $\gamma$ </td><td rowspan=1 colspan=1>SINR threshold</td></tr><tr><td rowspan=1 colspan=1>E</td><td rowspan=1 colspan=1>The maximum efective communication rangeof UAVs</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { p } _ { i , T _ { s } }$ </td><td rowspan=1 colspan=1>Three-dimensional position vector of UAV i attime $T _ { s }$ </td></tr><tr><td rowspan=1 colspan=1> ${ \bf u } _ { i , T _ { s } }$ </td><td rowspan=1 colspan=1>Three-dimensional speed vector of UAV i attime $T _ { s }$ </td></tr><tr><td rowspan=1 colspan=1> $L _ { i , j , T _ { s } }$ </td><td rowspan=1 colspan=1>The link connection duration of UAV i and UAVj in time-slot T from $T _ { s }$ </td></tr><tr><td rowspan=1 colspan=1> $\varepsilon _ { f s }$ </td><td rowspan=1 colspan=1>Energy consumption of the amplifier</td></tr><tr><td rowspan=1 colspan=1> $E _ { e l e c }$ </td><td rowspan=1 colspan=1>Energy consumed by the transmitter</td></tr><tr><td rowspan=1 colspan=1> $E _ { i , j , T _ { s } }$ </td><td rowspan=1 colspan=1>Energy consumption of sending data packets intime $\stackrel { \cup } { T } _ { s }$ </td></tr><tr><td rowspan=1 colspan=1> $\underline { { \beta _ { i , j , T _ { s } } ^ { s } } }$ </td><td rowspan=1 colspan=1>Stability effectiveness factor</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \beta _ { i , j , T _ { s } } ^ { e } } }$ </td><td rowspan=1 colspan=1>Cost effectiveness factor</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Effectivenessadjustable factor</td></tr><tr><td rowspan=1 colspan=1> $\beta _ { i , j , T _ { s } }$ </td><td rowspan=1 colspan=1>Effectiveness factor</td></tr><tr><td rowspan=1 colspan=1> $l _ { i , j , T _ { s } }$ </td><td rowspan=1 colspan=1>The number of bits sent between UAVs in time $T _ { s }$ </td></tr><tr><td rowspan=1 colspan=1> $n _ { \mathrm { m a x } }$ </td><td rowspan=1 colspan=1>The maximum UAV number in the cluster</td></tr><tr><td rowspan=1 colspan=1> $Q _ { i , j , T _ { s } }$ </td><td rowspan=1 colspan=1>The link effective value of the channel in $( T _ { s } , T _ { s } + \tau )$ </td></tr></table>

$$
\begin{array} { r } { \{ \mathbf { p } _ { i , T _ { s } } = ( p _ { i , T _ { s } } ^ { x } , p _ { i , T _ { s } } ^ { y } , p _ { i , T _ { s } } ^ { z } )  } \\ { \mathbf { u } _ { i , T _ { s } } = ( u _ { i , T _ { s } } ^ { x } , u _ { i , T _ { s } } ^ { y } , u _ { i , T _ { s } } ^ { z } ) } \end{array}  ,\tag{1}
$$

where $p _ { i , T _ { s } } ^ { x } , p _ { i , T _ { s } } ^ { y } , p _ { i , T _ { s } } ^ { z } , u _ { i , T _ { s } } ^ { x } , u _ { i , T _ { s } } ^ { y } , u _ { i , T _ { s } } ^ { z }$ represent the position component and speed component of UAV i for the x-axis, y-axis, z-axis respectively. Thus, the position $\mathbf { p } _ { i , T _ { s + 1 } }$ of UAV i at time $T _ { s + 1 }$ can be denoted by

$$
p _ { i , T _ { s + 1 } } ^ { \kappa } = p _ { i , T _ { s } } ^ { \kappa } + u _ { i , T _ { s } } ^ { \kappa } ,\tag{2}
$$

where $\kappa \in \{ x , y , z \}$ . In order to prevent UAVs from moving beyond the boundaries, a bouncing mechanism is designed. If

a position component at time $T _ { s + 1 }$ exceeds the boundary, the speed component need to be reversed, which can be denoted by

$$
p _ { i , T _ { s + 1 } } ^ { \kappa } = \left\{ p _ { i , T _ { s } } ^ { \kappa } + u _ { i , T _ { s } } ^ { \kappa } \quad p _ { i , T _ { s } } ^ { \kappa } + u _ { i , T _ { s } } ^ { \kappa } \in ( \kappa _ { \operatorname* { m i n } } , \kappa _ { \operatorname* { m a x } } ) \right.\tag{3}
$$

In order to simulate the heterogeneity in the mobility of different UAVs, parameters with different distributions are employed to adjust the speed changes of UAVs. The speed $\mathbf { u } _ { i , T _ { s } } = ( u _ { i , T _ { s } } ^ { x } , u _ { i , T _ { s } } ^ { y } , u _ { i , T _ { s } } ^ { z } )$ can be transformed from a three-= ( )dimensional coordinate system to a spherical coordinate system, which can be denoted by

$$
\left\{ \begin{array} { l l } { u _ { i , T _ { s } } ^ { x } = | \mathbf { u } _ { i , T _ { s } } | \sin \theta _ { i } \cos \varphi _ { i } } \\ { u _ { i , T _ { s } } ^ { y } = | \mathbf { u } _ { i , T _ { s } } | \sin \theta _ { i } \sin \varphi _ { i } } \\ { u _ { i , T _ { s } } ^ { z } = | \mathbf { u } _ { i , T _ { s } } | \cos \varphi _ { i } } \end{array} \right. .\tag{4}
$$

$\vert \mathbf { u } _ { i , T _ { s } } \vert$ is magnitude of the speed vector, which obeys the Gaussian distribution $\lvert \mathbf { u } _ { i , T _ { s } } \rvert \sim N ( \mu _ { i } , \sigma _ { i } ^ { 2 } ) . \theta _ { i }$ is the angle between the ( )speed of UAV and the z-axis, which obeys a uniform distribution $\theta _ { i } \sim U ( 0 , \pi ) . \ \varphi _ { i }$ is the angle between the speed of UAV and (0 )the x-axis, which obeys a uniform distribution $\varphi _ { i } \sim U ( 0 , 2 \pi )$ (0 2 )Compared to a uniform speed UAV model, this kind of modeling adheres more closely to physical principles, accounting for phenomena such as sharp turns, sudden braking, and body vibrations.

## C. Channel Model

When UAV i transmits signals to UAV j at time $T _ { s }$ , the SINR of UAV j can be denoted by

$$
S I N R _ { i , j , T _ { s } } = \frac { P h d _ { i , j , T _ { s } } ^ { - \alpha } } { \sigma ^ { 2 } } ,\tag{5}
$$

where P is the transmission power, and h is the channel gain. $d _ { i , j , T _ { s } } ^ { - \alpha }$ is the distance between two UAVs and Î± is the mean path loss exponent. $\sigma ^ { 2 }$ is the power of additive white Gaussian noise. Therefore, the instantaneous transmission rate per bit of the channel can be calculated by the Shannon formula

$$
C _ { i , j , T _ { s } } = B \log ( 1 + S I N R _ { i , j , T _ { s } } ) .\tag{6}
$$

Moreover, SINR is used to judge the neighbor relationship. If SINR is too small, the information from the sender cannot be decoded successfully by the receiver. Two UAVs are not neighbors when their air distance exceeds the communication range. Given a threshold Î³, the maximum communication range Îµ can be calculated by

$$
S I N R _ { i , j , T _ { s } } = \frac { P h \varepsilon ^ { - \alpha } } { \sigma ^ { 2 } } = \gamma \Longrightarrow \varepsilon = \sqrt [ \alpha ] { \frac { P h } { \gamma \sigma ^ { 2 } } } .\tag{7}
$$

## D. Link Connection Duration Model

The channel capacity calculated by the Shannon formula gives the maximum speed of data transportation. However, it is an instantaneous value. Therefore, to calculate the throughput in the time slot, we need to consider the mobility of the UAV swarm and evaluate the link connection duration of UAVs. Meanwhile, the link connection duration among different UAVs can be considered as a reference indicator for the stability of the UAV network [25].

<!-- image-->  
Fig. 2. Change of relative distance between two nodes.

The link connection duration of UAV swarm is evaluated in $( T _ { s } , T _ { s } + \tau )$ . As shown in Fig. 2, we assume that UAV j is a ( + )neighbor of UAV i at time $T _ { s }$ . We define $\Delta d _ { i , j , T _ { s } }$ as the relative distance difference between i and $\cdot j$ Îfrom time $T _ { s - 1 }$ to $T _ { s } ,$ , which can be denoted by

$$
\begin{array} { l } { \Delta d _ { i , j , T _ { s } } = d _ { i , j , T _ { s } } - d _ { i , j , T _ { s - 1 } } } \\ { \qquad = \lVert \mathbf { p } _ { i , T _ { s } } - \mathbf { p } _ { j , T _ { s } } \rVert _ { 2 } - \lVert \mathbf { p } _ { i , T _ { s - 1 } } - \mathbf { p } _ { j , T _ { s - 1 } } \rVert _ { 2 } . } \end{array}\tag{8}
$$

When $\Delta d _ { i , j , T _ { s } } < 0$ , the maximum relative distance that can stay connection is $\varepsilon + d _ { i , j , T _ { s } }$ , where Îµ is the maximum communica-+tion range in (7). Otherwise, the maximum relative distance is $\varepsilon - d _ { i , j , T _ { s } }$

Then, the connection time $L _ { i , j , T _ { s } }$ between i and $j$ can be denoted by

$$
L _ { i , j , T _ { s } } = \left\{ \begin{array} { l l } { \frac { \varepsilon + d _ { i , j , T _ { s } } } { { \overline { { u _ { i , j , T _ { s } } } } } } } & { \Delta d _ { i , j , T _ { s } } < 0 } \\ { \infty } & { \Delta d _ { i , j , T _ { s } } = 0 } \\ { \frac { \varepsilon - d _ { i , j , T _ { s } } } { { \overline { { u _ { i , j , T _ { s } } } } } } } & { \Delta d _ { i , j , T _ { s } } > 0 } \end{array} \right. .\tag{9}
$$

$\overline { { u _ { i , j , T _ { s } } } }$ is the relative speed, which is the absolute value of the projection of the UAV speed difference in the relative position direction

$$
\overline { { u _ { i , j , T _ { s } } } } = \left| \frac { \left( \mathbf { p } _ { i , T _ { s } } - \mathbf { p } _ { j , T _ { s } } \right) \cdot \left( \mathbf { u } _ { i , T _ { s } } - \mathbf { u } _ { j , T _ { s } } \right) } { \left\| \mathbf { p } _ { i , T _ { s } } - \mathbf { p } _ { j , T _ { s } } \right\| _ { 2 } } \right| .\tag{10}
$$

Finally, we analyze the connection duration in a time slot, and (9) is revised to

$$
L _ { i , j , T _ { s } } = \left\{ \begin{array} { l l } { L _ { i , j , T _ { s } } } & { L _ { i , j , T _ { s } } < \tau } \\ { \tau } & { L _ { i , j , T _ { s } } \geq \tau } \end{array} \right. .\tag{11}
$$

Therefore, the throughput between UAV i and j can be denoted by

$$
l _ { i , j , T _ { s } } = \int _ { T _ { s } } ^ { T _ { s } + L _ { i , j , T _ { s } } } B \log ( 1 + S I N R _ { i , j , t } ) d t .\tag{12}
$$

## E. Link Effective Value Model

The instantaneous throughput $C _ { i , j , T _ { s } }$ can be calculated by (6). However, it is deviant when we use $C _ { i , j , T _ { s } }$ to reflect channel status in the $( T _ { s } , T _ { s } + \tau )$ . To better describe the channel status in the time slot, we propose the link effective value $Q _ { i , j , T _ { s } }$ based on the $C _ { i , j , T _ { s } }$ , which describes the wireless link attributes in the $( T _ { s } , T _ { s } + \tau )$ . The link effective value $Q _ { i , j , T _ { s } }$ is denoted by

$$
Q _ { i , j , T _ { s } } = \beta _ { i , j , T _ { s } } C _ { i , j , T _ { s } } ,\tag{13}
$$

where $\beta _ { i , j , T _ { s } }$ is effectiveness factor. The design of $\beta _ { i , j , T _ { s } }$ is based on two considerations. On the one hand, UAVs are willing to communicate with other UAVs which can keep the connection for more time because persistent connection contributes to the stability of the UAV swarm. On the other hand, it is unwise to send packets over long distances because it needs higher energy overhead. Therefore, effectiveness factor $\beta _ { i , j , T _ { s } }$ includes stability effectiveness factor $\beta _ { i , j , T } ^ { s }$ and cost effectiveness factor $\beta _ { i , j , T _ { s } } ^ { e }$

Stability effectiveness factor $\beta _ { i , j , T _ { s } } ^ { s }$ derives from the link time $L _ { i , j , T _ { s } }$ in the Section III-D, which are denoted by

$$
\beta _ { i , j , T _ { s } } ^ { s } = \frac { L _ { i , j , T _ { s } } } { \tau } .\tag{14}
$$

Cost effectiveness factor $\beta _ { i , j , T _ { s } } ^ { e }$ consider the energy consumption of transmitting packets. In [26], the sending energy $E _ { i , j , T _ { s } }$ in the free space model can be formulated as

$$
E _ { i , j , T _ { s } } = l E _ { e l e c } + l \varepsilon _ { f s } d _ { i , j , T _ { s } } ^ { 2 } ,\tag{15}
$$

where $E _ { e l e c }$ is the energy consumed by the transmitter, $\varepsilon _ { f s }$ is the energy consumption of the amplifier and l is the number of bits. Here, we will set l as 1 b when calculating the cost effectiveness factor. In the Section III-C, we give the maximum effective communication range Îµ. The sending energy when the communication range is Îµ can be the measure of cost. The maximum energy consumes $E _ { \varepsilon }$ is

$$
E _ { \varepsilon } = l E _ { e l e c } + l \varepsilon _ { f s } \varepsilon ^ { 2 } .\tag{16}
$$

Therefore, the cost effectiveness factor $\beta _ { i , j , T _ { s } } ^ { e }$ is denoted by

$$
\beta _ { i , j , T _ { s } } ^ { e } = 1 - \frac { E _ { i , j , T _ { s } } } { E _ { \varepsilon } } .\tag{17}
$$

The effectiveness factor $\beta _ { i , j , T _ { s } }$ is a weighted value, which is denoted by

$$
\beta _ { i , j , T _ { s } } = \theta \beta _ { i , j , T _ { s } } ^ { s } + ( 1 - \theta ) \beta _ { i , j , T _ { s } } ^ { e } ,\tag{18}
$$

where $\theta$ is an adjustable factor. The link effective value $Q _ { i , j , T _ { s } }$ reflects wireless link attributes of UAV swarm in the $( T _ { s } , T _ { s } +$ Ï .

## F. Problem Formulation

Our goal is to find an excellent UAV cluster structure to maximize the average cluster throughput in the UAV swarm network. The throughput of the cluster is the information amount that CH gathers from CMs in the time slot. Therefore our objective problem is mathematically formulated as follows

$$
\begin{array} { r l } & { \operatorname* { m a x } \cfrac { 1 } { k } \underset { k \in \mathit { K } _ { i } \in \mathit { C } _ { k } / \left\{ k \right\} } { \sum } l _ { k , i , T _ { s } } , } \\ { \mathrm { ~ } _ { s . t . } } & { C _ { 1 } : S I N R _ { k , i } \geq \gamma , } \\ & { ~ C _ { 2 } : \Big \bigcup _ { k = 1 } ^ { K } C _ { k } = N , } \\ & { ~ C _ { 3 } : \displaystyle \bigcap _ { k = 1 } ^ { K } C _ { k } = \phi , } \\ & { ~ C _ { 4 } : 1 \leq \left| C _ { k } \right| \leq n _ { \operatorname* { m a x } } , \forall k \in \mathcal { K } . } \end{array}\tag{19}
$$

where ${ \mathcal { K } } = \{ 1 , 2 , \ldots , K \}$ is CH set and $C = \{ C _ { 1 } , \ldots , C _ { K } \}$ is =cluster set.

$C _ { 1 }$ constraint shows that a large enough SINR is the premise of the communication between CH and CMs. $C _ { 2 }$ constraint and $C _ { 3 }$ constraint propose that all UAVs must belong to one cluster and can only belong to one cluster. $C _ { 4 }$ constraint limits the number of UAVs in each cluster, where $n _ { \mathrm { m a x } }$ is the maximum UAV number in the cluster. On the one hand, it can prevent a high collision rate in areas with very high node density when setting a limit UAV number value [27]. On the other hand, CH will cost a lot of energy when gathering information from too many CMs.

## IV. FISSION SPECTRUM CLUSTERING

In this part, we propose a clustering algorithm called fission spectrum clustering (FSC). The proposed clustering algorithm includes the initial clustering stage and cluster maintenance stage. The initial clustering stage includes cluster establishment and the CH selections. The cluster maintenance stage includes cluster changing, partial clustering, and re-clustering. When the network is first established, the initial clustering scheme is performed. Then, we implement maintaining clustering at the beginning of each time slot.

## A. Initial Clustering Stage Based on Fission Spectrum Clustering

FSC is designed based on SC and SC is uesd to perform the first round of clustering. The SC involves selecting a cluster number, constructing a similarity matrix, creating a Laplace matrix, decomposing eigenvalues and clustering. To restrict the size of the cluster while ensuring throughput, the cluster number K is set to $\left\lceil \frac { N } { n _ { \mathrm { m a x } } } \right\rceil$ , where 
- is rounding up. Similarity matrix $W \in R ^ { N \times N }$ is the important parameter, which quantitatively describes the link between nodes. In order to improve the network throughput after clustering, the link effective value $Q _ { i , j , T _ { s } }$ is used to construct the similarity matrix W . Therefore, W is set to

$$
w _ { i , j } = \left\{ \begin{array} { l l } { Q _ { i , j , T _ { s } } } & { S I N R _ { i , j , T _ { s } } > \gamma } \\ { 0 } & { S I N R _ { i , j , T _ { s } } \leq \gamma } \end{array} \right. ,\tag{20}
$$

Algorithm 1: Fission Spectral Clustering.   
Input: Graph $G = ( V , E )$ , Maximum UAV number $n _ { \mathrm { m a x } }$   
= ( )Output: Clustering results C, The number of clusters K   
1: Cluster result set results â   
2: = Compute similarity matrix W of all UAVs by using   
(20)   
3: Compute degree matrix D of all UAVs by using (22)   
4: Compute Laplacian matrix L of all UAVs by using (21)   
5: $\begin{array} { r } { K = \bigg \lceil \frac { N } { n _ { \mathrm { m a x } } } \bigg \rceil } \end{array}$   
6: Compute the smallest K eigenvalues of L and get   
eigenvector matrix $F = \{ f _ { 1 } , f _ { 2 } , \dots , f _ { K } \}$   
7: = Decompose matrix F by row into $\left\{ y _ { 1 } , y _ { 2 } , \ldots , y _ { N } \right\}$   
8: Cluster $\left\{ y _ { 1 } , y _ { 2 } , \ldots , y _ { N } \right\}$ in K-Means and get the   
clustering result.   
9: Put the result into the result and check the result in   
results   
10: while result in results do   
11: while the size of result than $n _ { \mathrm { m a x } }$ do   
12: $\begin{array} { r } { K ^ { \prime } = \left\lceil \frac { | r e s u l t | } { n _ { \mathrm { m a x } } } \right\rceil } \end{array}$   
13: Split result into $K ^ { \prime }$ sub-cluster   
14: Update results   
15: end while   
16: end while   
17: while result in results do   
18: while there are no CH candidates in result do   
19: $K ^ { \prime } = 2$   
20: = 2 Split result into $K ^ { \prime }$ sub-cluster   
21: Update results   
22: end while   
23: end while   
24: The number of clusters K is the size of results   
25: $C = \{ C _ { 1 } , \ldots , C _ { K } \} =$ results   
26: = =returnClustering results C and the number of clusters   
K

Then, the normalized Laplacian matrix L can be described as

$$
L = I - D ^ { - { \frac { 1 } { 2 } } } W D ^ { - { \frac { 1 } { 2 } } } ,\tag{21}
$$

where D is called the degree matrix and it is a diagonal matrix formed by $D _ { i i } . D _ { i i }$ is denoted as

$$
D _ { i i } = \sum _ { j = 1 } ^ { N } w _ { i , j } .\tag{22}
$$

Compute the first K generalized eigenvalue problem $L f =$ $\lambda D f$ , then take eigenvectors $f _ { 1 } , f _ { 2 } , \dots , f _ { K }$ =as the columns of eigenvector matrix $F \in N \times K$ . Each row in F is also considered a K-dimensional vector. Therefore F is decomposed into $y _ { 1 } , y _ { 2 } , \dotsc , y _ { N }$ . Then cluster the vectors $y _ { i } ( i = 1 , 2 , . . . , N )$ ( = 1 2 )with the traditional K-Means clustering algorithm into clusters $A = \{ A _ { 1 } , \ldots , A _ { K } \}$ . Finally, the clustering results can be ob-=tained according to the corresponding position

$$
C _ { j } = \{ j | y _ { j } \in A _ { i } \} .\tag{23}
$$

<!-- image-->  
Fig. 3. Fission process of FSC. A cluster needs to fission when it doesnât satisfy the size and structure constraints.

However, the initial clustering results were unsatisfactory, as they failed to ensure the validity of $C _ { 1 }$ and $C _ { 4 }$ constraint in (19) for each cluster. For constraint $C _ { 1 }$ , such a rough clustering method cannot ensure that a CH exists in the cluster which can communicate with all CMs. For constraint $C _ { 4 }$ , the number of UAVs in the cluster is likely to surpass the limit value.

Hence, FSC enhances traditional SC and conducts fission clustering on the results to satisfy the constraints of UAV swarm clustering. On the basis of the first clustering result, FSC algorithm will check whether each cluster satisfies our constraints. Supposed that the number of UAVs in cluster $C _ { k }$ is more than the limit value $n _ { \mathrm { m a x } } ,$ this cluster will be split. The method of splitting this cluster $C _ { k }$ is executing SC algorithm again and this time K is $\left\lceil \frac { N _ { C _ { k } } } { n _ { \operatorname* { m a x } } } \right\rceil$ . The clusters will undergo continuous fission and inspection iterations until the constraints are met $C _ { 4 } .$ Next, our proposed algorithm will check whether there are CH candidates in each cluster. CH candidates are the UAVs in the cluster that can communicate with all CMs. Each cluster should exist one or more CH candidates. If there are no CH candidates, this cluster will be split into two, i.e K is 2. The choice of $K = 2$ is made to maximize the cluster size while ensuring satisfaction of the $C _ { 4 }$ constraint, aiming to enhance the throughput of each cluster. The clusters will undergo continuous fission and inspection iterations until the constraints are met $C _ { 1 }$ Fig. 3 and Algorithm 1 describes this process.

Then it is the turn to elect CH from CH candidates. CH is responsible for gathering the information of CMs in the cluster and therefore the selection of CH is related to the throughput of the cluster. Therefore, CH should have the maximum link effective value in the CH candidates, and it is denoted by

$$
k = \underset { k \in c a n d } { \arg \operatorname* { m a x } } \sum _ { i \in C _ { k \backslash \{ k \} } } Q _ { k , i , T _ { t } } ,\tag{24}
$$

where cand is CH candidates set. Algorithm 2 describes this process.

## B. Cluster Maintenance Stage Based on Partial Fission Spectrum Clustering

The high dynamics of UAVs reduce the stability of the cluster structure. For this reason, we check our UAV network at intervals Ï . We can choose to cluster the UAV swarm every Ï by FSC. However, this method will cause a heavy computation overhead. Our proposed algorithm belongs to a centralized algorithm, which needs to build a complex UAV network and requires a great deal of calculation.

Algorithm 2: CH Selection.   
Input: Cluster $\overline { { C _ { k } } }$   
Output: The CH k of $C _ { k }$   
1: CH candidates set cand $= \phi$   
2: for i in $C _ { k }$ do   
3: count   
4: for $j$ in $C _ { k }$ do   
5: if i $\neq j$ SIN $R _ { i , j } \geq \gamma$ then   
6: = &&count count   
7: end if   
8: end for   
9: if count len Ck â then   
10: == put i into cand   
11: end if   
12: end for   
13: k   kâcandâ©iâCk\{k} Qk,i,Ts   
14: = arg maxreturn CH k

Although the UAV network is dynamic, many UAVs can still maintain communication with their clusters in the next time slot. These UAVs are unnecessary to be clustered again. Therefore, in the cluster maintenance stage, we only need to focus on the UAVs which are out of communication with their clusters. Note that the unconnected network is not considered in this article, i.e. there are no outlier UAVs in the network when UAVs move.

The cluster maintenance stage includes three steps: cluster changing, partial clustering, and re-clustering.

Cluster changing: The established association between a CM and its CH may be broken after the initial clustering stage because of the limited transmission range and random node mobility [27]. At the next time slot, if a CM UAV i finds that it moves out of its CHâs coverage area, it will consider joining another cluster. It searches its new neighbors in its coverage scope Îµ and calculates the link effective values of them by (13). Suppose that UAV j has the maximal link effective value in the neighbors of UAV i. Then UAV i modifies its cluster number to UAV jâs cluster number.

Partial clustering: After updating some UAVsâ cluster numbers, our proposed algorithm will check the status of each cluster again. Each cluster can be regarded as a partial UAV network. If a cluster doesnât satisfy the constraints $C _ { 1 }$ or $C _ { 4 } .$ , it will execute the FSC algorithm. Compared with the initial clustering stage, the scale of the network is small and the computational complexity will be reduced a lot.

Re-clustering: In our proposed algorithm, clusters will persistently fission. As a consequence, the size of each cluster will smaller and smaller, which will reduce the capability of each cluster. The algorithm takes the average cluster throughput in the initial clustering stage as the standard and stipulates a half of the standard is the threshold. If the average cluster throughput is under the threshold in a certain time slot, the capability of the current cluster structure is considered inefficient. Then, in the next time slot, all UAVs need to be clustered and the UAV swarm returns to the initial clustering stage. Algorithm 3 describe cluster maintenance stage.

Algorithm 3: Cluster Maintenance.   
Input: Cluster $\overline { { C = \{ C _ { 1 } , \ldots , C _ { K } \} } }$ , Simulation duration T   
1: = Calculate the throughput throughput of initial   
clustering   
2: Set threshold . â throughput   
3: = 0 5 Set new_throughput  throughput   
4: $t = \tau$   
5: =while $t \leq T$ do   
6: if new_throughput < threshold then   
7: Execute Algorithm 1 for this cluster.   
8: $t = t + \tau$   
9: =break   
10: end if   
11: Update the position of all UAVs.   
12: while a CM UAV cannot communicate with its CH   
do   
13: Get its new neighbor set new_neighbor by (5).   
14: Calculate link effective values of UAVs in   
new_neighbor and change itself own cluster   
number to the cluster number of the UAV which   
has the maximum effective value, i.e.   
cluster_numberj   iânew_neighbor $Q _ { i , j , t }$   
15: end while   
16: Check the statue of clusters   
17: if the size of the cluster than $n _ { \mathrm { m a x } }$ or there are no   
CH candidates in cluster then   
18: Execute Algorithm 1 for this cluster.   
19: end if   
20: $t = t + \tau$   
21: = + Calculate the new average cluster throughput   
new_throughput of the current UAV swarm.   
22: end while

## V. SIMULATION RESULTS

In this section, we present the simulation results to evaluate the validity of the proposed algorithm. Our experiments simulate with Windows 10 operating system, which configuration is Intel Core i5 10400 central processing unit (CPU), 2.9 GHz.

For the proposed algorithm, we evaluate its performance, convergence, and stability. Then FSC is compared with other algorithms. Four UAV network clustering algorithms, termed Weighted Clustering Algorithm (WCA) [28], Gaussian mixture model (GMM) [29], Affinity Propagation (AP) [30], and Agglomerative Clustering (AC) [31] are set as the baseline.

## A. Simulation Settings

In our experiment, the simulation environment is set to 2000 m Ã 2000 m square area. The flight altitude of UAVs is between 100 m and 150 m. The SINR threshold Î³ is defined by 0 dB which limits the communication range of UAVs. The noise power $\sigma ^ { 2 }$ is â dBm. The transmission power P of UAV is set to 20 dBm and the mean path-loss exponent Î± is set to 4. The channel bandwidth B is set to 10 MHz and the channel gain h is set to 0.5. The time slot Ï is set to 10 s and we check the status of the network every 10 seconds. The simulation duration T is 300 s.

<!-- image-->

<!-- image-->

<!-- image-->  
(a) Initial UAV swarm distribution (b) $n _ { \mathrm { m a x } } = 1 5 ,$ cluster number = 10 (c) $n _ { \mathrm { m a x } } = 2 0 _ { , }$ ,cluster number = 7 (d) $n _ { \mathrm { m a x } } = 2 5 ,$ cluster number= 6

<!-- image-->  
Fig. 4. Clustering results of UAV swarm under different $n _ { \mathrm { m a x } }$

TABLE II SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Simulation area</td><td rowspan=1 colspan=1>1000 m*1000 m*(100ï¼ 150) m</td></tr><tr><td rowspan=1 colspan=1>Number of UAVs</td><td rowspan=1 colspan=1>50-250</td></tr><tr><td rowspan=1 colspan=1>The Speed of UAVs</td><td rowspan=1 colspan=1>10-30m/s</td></tr><tr><td rowspan=1 colspan=1>SINR threshold ()</td><td rowspan=1 colspan=1>0dbm</td></tr><tr><td rowspan=1 colspan=1>Transmission power (P)</td><td rowspan=1 colspan=1>20 dbm</td></tr><tr><td rowspan=1 colspan=1>Mean path-loss exponent (Î±)</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>Channel bandwidth (B)</td><td rowspan=1 colspan=1>10 MHz</td></tr><tr><td rowspan=1 colspan=1>Channel gain (h)</td><td rowspan=1 colspan=1>0.5</td></tr><tr><td rowspan=1 colspan=1>Noise power $( \sigma ^ { 2 } )$ </td><td rowspan=1 colspan=1>-100 dbm</td></tr><tr><td rowspan=1 colspan=1>Energy consumption of the am-plifier $( \varepsilon _ { f s } )$ </td><td rowspan=1 colspan=1> $1 0 \times 1 0 ^ { - 1 2 } \mathrm { J } / \mathrm { b i t } ^ { * } m ^ { 2 }$ </td></tr><tr><td rowspan=1 colspan=1>Energy consumed by the trans-mitter $( E _ { e l e c } )$ </td><td rowspan=1 colspan=1> $5 0 \times 1 0 ^ { - 9 } \mathrm { J / b i t }$ </td></tr><tr><td rowspan=1 colspan=1>Adjustable factor (0)</td><td rowspan=1 colspan=1>0.5</td></tr><tr><td rowspan=1 colspan=1>Time slot (ð)</td><td rowspan=1 colspan=1>10 s</td></tr><tr><td rowspan=1 colspan=1>Simulation duration (T)</td><td rowspan=1 colspan=1>300 s</td></tr></table>

The detailed parameters setting can be found in Table II. In the experiments, the defaults of UAVsâ number, UAVsâ speed and $n _ { \mathrm { m a x } }$ are 100, 20 m/s, 20 unless otherwise noted.

## B. Cluster Result

As shown in Fig. 4, we present cluster results in different maximum UAV numbers $n _ { \mathrm { m a x } }$ in the initial clustering stage. Fig. 4(a) shows the initial distribution of 100 UAVs at $T _ { s }$ . Then we set $n _ { \mathrm { m a x } }$ as 15, 20, 25 and observe the change of cluster structure in (b), (c) and (d), where the 
 represents CH in each cluster. As the $n _ { \mathrm { m a x } }$ increases and decreases, clusters can flexibly merge and fission, which is corresponding to tasks of different scales. What is more, we can notice that the ascription of UAVs in the high-density area is easier to change when $n _ { \mathrm { m a x } }$ changes. It indicates that our clustering algorithm is an effective measure to reduce flooding interference in a high-density area.

<!-- image-->  
Fig. 5. Average cluster throughput under different $n _ { \mathrm { m a x } }$ when using FSC in the initial clustering stage.

## C. Performance Analysis

In this part, we evaluate the algorithmâs performance. The performance indicator is the average cluster throughput and we take the number of bits per cluster as the average cluster throughput by using (19).

Fig. 5 shows the average cluster throughput of the different $n _ { \mathrm { m a x } }$ when we execute the FSC algorithm in the initial clustering stage. Generally, a lower $n _ { \mathrm { m a x } }$ will lead to more clusters when the number of UAVs is the same, which is an effective measure to reduce flooding interference. However, it cost the communication performance of the UAV swarm. Besides, with the number of UAVs increasing, the average cluster throughput increases. However, this increasing trend is converging because the number of clusters also increases with the average cluster throughput increasing.

Fig. 6 shows the average cluster throughput under different $n _ { \mathrm { m a x } }$ varies with time. With the $n _ { \mathrm { m a x } }$ increasing, the average cluster throughput increases. This is mainly caused by the decrease in the number of clusters with the $n _ { \mathrm { m a x } }$ increasing. At the beginning of simulation time, the UAV network maintains its cluster structure by fissioning the cluster. However, the average cluster throughput decreases as the increase of clusters. We have to re-cluster to improve the average cluster throughput when the average cluster throughput is lower than the threshold, which is a cycle process. The dotted line represents the re-clustering of the UAV swarm in this time slot.

<!-- image-->  
Fig. 6. Average cluster throughput under different $n _ { \mathrm { m a x } }$ when using FSC in the cluster maintenance stage.

<!-- image-->  
Fig. 7. Number of clusters under different $n _ { \mathrm { m a x } }$ when using FSC in the initial clustering stage.

## D. Convergence Analysis

Our proposed algorithm is an adaptive fission algorithm. Clusters will stop fission when the UAV network structure satisfies the constraints. We donât expect unrestricted fission because too many clusters will decrease the amount of UAVs in each cluster, which weakens the communication performance of each cluster. Therefore, our algorithm is convergent.

Fig. 7 shows the number of clusters in the different numbers of UAVs and $n _ { \mathrm { m a x } }$ . The number of clusters increases with the number of UAVs increasing. We can notice that usually the actual number of clusters is more than $\left\lceil \frac { | U A V s | } { n _ { \operatorname* { m a x } } } \right\rceil$ . This is because UAVs have high dynamics and the UAV network has irregularity. If we cannot satisfy the constraints when we get a clustering result, we must continue to split this cluster.

<!-- image-->  
Fig. 8. Number of clusters under different $n _ { \mathrm { m a x } }$ when using FSC in the cluster maintenance stage.

<!-- image-->  
Fig. 9. Average cluster throughput under different speeds when using FSC in the cluster maintenance stage.

Fig. 8 shows the number of clusters under different $n _ { \mathrm { m a x } }$ varies with time, which is corresponding to the Fig. 6. From Fig. 8, We find that the UAV network in our algorithm tries its best to maintain the current cluster structure and Only a small number of clusters that donât meet the constraints will undergo fission.

## E. Stability Analysis

In this part, we discuss the stability of the UAV network and mainly analyze how mobility affects the clustering results.

Fig. 9 shows the average cluster throughput under different speed varies with time. When time is 0 s, the UAV network is in the initial clustering stage. In the three experiments, their $n _ { \mathrm { m a x } }$ are the same. Therefore their initial clustering results are the same at the beginning when executing the FSC algorithm. Then the UAVs begin to move, which leads to different graphs. From Fig. 9, we can conclude that the faster the speed is, the shorter the cluster maintenance stage will be. In a high-speed environment, cluster structure is unstable and we have to fission the cluster frequently to maintain cluster structure, which leads to the falling average cluster throughput rapidly.

<!-- image-->  
Fig. 10. Number of clusters under different speeds when using FSC in the cluster maintenance stage.

Fig. 10 shows the number of clusters under different speed varies with time, which is corresponding to the Fig. 9. We can find from the figure that cluster fissions frequently in a highly dynamic environment. Contrarily, a cluster structure can keep for several time slots.

## F. Comparison

In this part, we compare our proposed algorithm FSC with WCA, GMM, AP, and AC. When the number of UAVs is N and the number of clusters is k, the complexity analysis of these algorithms is as follows. WCA is essentially a K-Means algorithm with a time complexity of O tN k , where t is the number of iterations. The GMM process is similar to K-Means, but it falls under soft clustering and the output consists of probabilities of belonging. The computational complexity of GMM is high, with each iteration being greater than K-Means. The AP algorithm can automatically cluster based on sample data. However, it is necessary to calculate the similarity between each pair of data objects in advance, which requires a large amount of computation. Its time complexity is $O ( N ^ { 2 } t )$ , where t is the number of ( )iterations. AC is a method of clustering analysis by establishing a hierarchical structure of clusters. AC requires N iterations, each of which requires updating and storing the similarity matrix. Therefore, the time complexity is the cubic order of the number of samples N, which is $O ( N ^ { 3 } )$ . The core of FSC is SC. The time complexity of SC comes from constructing similarity matrix $O ( N ^ { 2 } )$ and decomposing eigenvalues $O ( N ^ { 3 } )$ . Thus, the time complexity of FSC is $O ( N ^ { 3 } t )$ , where t is the number of fission. ( )The time complexity of FSC is the highest during the initial clustering stage. However, during the cluster maintenance stage, FSC pre-detects the state of the cluster and only performs partial fission on clusters which donât meet the constraints. Therefore, the number of samples N has been significantly reduced, greatly saving computational costs. Additionally, FSC considers the dynamics of the UAV swarm, enhancing the stability of the cluster and reducing the number of re-clustering.

<!-- image-->  
Fig. 11. Average cluster throughput when using different algorithms in the initial clustering stage.

<!-- image-->  
Fig. 12. Number of UAVs in each cluster when using different algorithms in the initial clustering stage.

As shown in Fig. 11, we present the average cluster throughput in the network of the different algorithms. With the number of UAVs increasing, the average cluster throughput increases. This is mainly caused by the increase in communication between UAVs with the number of clusters increasing. FSC algorithm considers the network status in the time slot and has a time effect, which is an advantage over other algorithms. Fig. 11 demonstrates the validity of our proposed algorithm.

As shown in Fig. 12, we present the number of UAVs in each cluster when using different algorithms. In the box boxplot, we consider two aspects: one is the difference between the maximum value and minimum value, and the other is the median number. From the perspective of maximum value and minimum value, the effect of $\mathbf { A P }$ is the best. However, the median number of AP is significantly lower than the other four algorithms. It demonstrates the size of clusters in the AP algorithm. This clustering strategy will affect the average cluster throughput. Excluding AP, FSC, GMM, and AC all have the second small difference. Although the maximum value of AC reaches the $m _ { \mathrm { m a x } }$ , FSC has the largest median number, which demonstrates the clustering results of FSC distributes more uniformly.

<!-- image-->  
Fig. 13. Average cluster throughput when using different algorithms in the cluster maintenance clustering stage.

<!-- image-->  
Fig. 14. Number of clusters when using different algorithms in the cluster maintenance clustering stage.

Fig. 13 shows the average cluster throughput under different algorithms varies with time. When the simulation time is 100 s, 80 s, 100 s, 90 s, 90 s, FSC, GMM, WCA, AP, and AC respectively reach the threshold for the first time. Then, in the next time slot, they return to the initial clustering stage and re-clustering. A longer cluster maintenance stage will save computing overhead. In addition, although FSC and WCA both keep the cluster structure for 100 s, the average cluster throughput of FSC is significantly higher than WCA.

Fig. 14 shows the number of clusters under different algorithms varies with time, which is corresponding to the Fig. 13. Within 300 s of simulation time, the re-clustering number of FSC, GMM, WCA, AP, AC are respectively 3, 4, 4, 3 and 4. In addition, compared with other algorithms, FSC has less clusters, which means that the size of the cluster in the FSC algorithm is larger and therefore each cluster has a stronger capability.

## VI. CONCLUSION

This article aims to improve the communication performance of UAV swarm after clustering. We abstract the UAV swarm into a graph and propose the link effective value to describe the timesequential attributes of nodes and edges. Next, we propose the FSC algorithm. FSC achieves UAVs clustering by decomposing the Laplacian matrix formed by link effectiveness. Each cluster will constantly fission with this strategy until it satisfies the size and structure constraints in the UAV clusters. FSC can be both applied to the initial clustering stage and the cluster maintenance stage. The experimental result shows that the application of FSC in UAV clustering has superior communication performance and longer cluster maintenance time.

## REFERENCES

[1] J. Wang, Z. Jiao, J. Chen, X. Hou, T. Yang, and D. Lan, âBlockchain-aided secure access control for UAV computing networks,â IEEE Trans. Netw. Sci. Eng., to be published, doi: 10.1109/TNSE.2023.3324639.

[2] H. Feng, J. Wang, Z. Fang, J. Chen, and D.-T. Do, âEvaluating AoI-centric HARQ protocols for UAV networks,â IEEE Trans. Commun., vol. 72, no. 1, pp. 288â301, Jan. 2024.

[3] M. Aissa, M. Abdelhafidh, and A. B. Mnaouer, âEMASS: A novel energy, safety and mobility aware-based clustering algorithm for FANETs,â IEEE Access, vol. 9, pp. 105506â105520, 2021.

[4] Y. Zeng, J. Cao, S. Guo, Y. Kai, and X. Li, âSWCA: A secure weighted clustering algorithm in wireless ad hoc networks,â in Proc. IEEE Wireless Commun. Netw. Conf., 2009, pp. 2426â2431.

[5] S. K. Dhurandher and G. V. Singh, âWeight based adaptive clustering in wireless adhoc networks,â in Proc. Int. Conf. Pers. Wireless Commun., 2005, pp. 95â100.

[6] M. Chatterjee, âAn on-demand weighted clustering algorithm (WCA) for ad hoc networks,â in Proc. IEEE Glob. Telecommun. Conf., 2000, pp. 1697â1701.

[7] Z. JingMao and S. YanXia, âReview on spectral methods for clustering,â in Proc. 34th Chin. Control Conf., 2015, pp. 3791â3796.

[8] R. Van Driessche and D. Roose, âAn improved spectral bisection algorithm and its application to dynamic load balancing,â Parallel Comput., vol. 21, no. 1, pp. 29â48, 1995.

[9] K. Hou, Q. Xu, X. Zhang, Y. Huang, and L. Yang, âUser association and power allocation based on unsupervised graph model in ultra-dense network,â in Proc. IEEE Wireless Commun. Netw. Conf., 2021, pp. 1â6.

[10] Y. Lv, M. Zhuo, D. Zhang, and A. Li, âA low energy uneven clustering topology control algorithm for wireless networks,â in Proc. Int. Conf. Inf. Sci. Control Eng., 2016, pp. 1203â1207.

[11] Y. S. Wang, Y. Hong, and W. T. Chen, âDynamically connectable UAV base stations with cooperative energy sharing,â in Proc. IEEE Glob. Commun. Conf., 2018, pp. 1â6.

[12] H. Qu, W. Zhang, J. Zhao, Z. Luan, and C. Chang, âRapid deployment of UAVs based on bandwidth resources in emergency scenarios,â in Proc. Inf. Commun. Technol. Conf., 2020, pp. 86â90.

[13] S. Pathak and S. Jain, âAn optimized stable clustering algorithm for mobile ad hoc networks,â EURASIP J. Wireless Commun. Netw., vol. 2017, no. 1, 2017, Art. no. 51.

[14] M. Y. Arafat and S. Moh, âLocalization and clustering based on swarm intelligence in UAV networks for emergency communications,â IEEE Internet Things J., vol. 6, no. 5, pp. 8958â8976, Oct. 2019.

[15] J. Wang, Q. Zhang, G. Feng, S. Qin, and L. Cheng, âClustering strategy of UAV network based on deep Q-learning,â in Proc. IEEE 20th Int. Conf. Commun. Technol., 2020, pp. 1684â1689.

[16] M. Ahmad et al., âCluster optimization in mobile ad hoc networks based on memetic algorithm: Memehoc,â Complex, vol. 2020, pp. 1â12, 2020.

[17] K. Xiao, S. Xu, S. Guo, X. Qiu, and K. Guo, âA clustering algorithm based on communication overhead and link stability for cloud-assisted mobile adhoc networks,â in Proc. 15th Int. Wireless Commun. Mobile Comput. Conf., 2019, pp. 278â283.

[18] Y. Sun, Z. Mi, H. Wang, F. Lu, and N. Zhao, âAdaptive enhanced weighted clustering algorithm for UAV swarm,â in Proc. IEEE 20th Int. Conf. Commun. Technol., 2020, pp. 709â714.

[19] M. J. Sousa, A. Moutinho, and M. Almeida, âDecentralized distribution of UAV fleets based on fuzzy clustering for demand-driven aerial services,â in Proc. IEEE Int. Conf. Fuzzy Syst., 2020, pp. 1â8.

[20] H. Duan, Z. Wang, Y. Liu, X. Li, and H. Zhao, âIWCA algorithm for clustered drone information transmission network,â in Proc. 5th Int. Conf. Soft Comput. Mach. Intell., 2018, pp. 119â122.

[21] L. Chen, L. Ma, Y. Xu, and V. C. Leung, âHypergraph spectral clustering based spectrum resource allocation for dense NOMA-hetnet,â IEEE Wireless Commun. Lett., vol. 8, no. 1, pp. 305â308, Feb. 2018.

[22] M. K. Jabbar and H. Trabelsi, âA novelty of hypergraph clustering model (HGCM) for urban scenario in VANET,â IEEE Access, vol. 10, pp. 66672â66693, 2022.

[23] Z. Lin, Y. Zhao, L. Huang, and Z. Shi, âSpectral clustering based millimeter-wave beam management in V2I networks,â in Proc. Int. Conf. Intell. Comput. Hum.- Comput. Interaction, 2020, pp. 142â145.

[24] S. Atev, G. Miller, and N. P. Papanikolopoulos, âClustering of vehicle trajectories,â IEEE Trans. Intell. Transp. Syst., vol. 11, no. 3, pp. 647â657, Sep. 2010.

[25] L. Hong, H. Guo, J. Liu, and Y. Zhang, âToward swarm coordination: Topology-aware inter-UAV routing optimization,â IEEE Trans. Veh. Technol., vol. 69, no. 9, pp. 10177â10187, Sep. 2020.

[26] W. B. Heinzelman, A. P. Chandrakasan, and H. Balakrishnan, âAn application-specific protocol architecture for wireless microsensor networks,â IEEE Trans. Wireless Commun., vol. 1, no. 4, pp. 660â670, Oct. 2002.

[27] M. Ni, Z. Zhong, and D. Zhao, âMPBC: A mobility prediction-based clustering scheme for ad hoc networks,â IEEE Trans. Veh. Technol., vol. 60, no. 9, pp. 4549â4559, Nov. 2011.

[28] M. Chatterjee, S. K. Das, and D. Turgut, âWCA: A weighted clustering algorithm for mobile ad hoc networks,â Cluster Comput., vol. 5, no. 2, pp. 193â204, 2002.

[29] C. Stauffer and W. E. L. Grimson, âAdaptive background mixture models for real-time tracking,â in Proc. IEEE Comput. Soc. Conf. Comput. Vis. Pattern Recognit., 1999, pp. 246â252.

[30] B. J. Frey and D. Dueck, âClustering by passing messages between data points,â Science, vol. 315, no. 5814, pp. 972â976, 2007.

[31] D. MÃ¼llner, âModern hierarchical, agglomerative clustering algorithms,â 2011, arXiv:1109.2378.

<!-- image-->  
Gepeng Zhu received the masterâs degree from the Beijing University of Posts and Telecommunications. His research interests include artificial intelligence and high dynamic UAV swarm networking.

<!-- image-->

<!-- image-->

Haipeng Yao (Senior Member, IEEE) received the PhD degree from the Department of Telecommunication Engineering, University of Beijing University of Posts and Telecommunications, in 2011. He is a professor with the Beijing University of Posts and Telecommunications. His research interests include future network architecture, network artificial intelligence and space-terrestrial integrated network. He has published more than 150 papers in prestigious peer-reviewed journals and conferences. He has served as a member of the technical program

Tianle Mai (Member, IEEE) is working toward the PhD degree with the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His main research interests are in the areas of artificial intelligence, multi-agent system, and future network architecture.

<!-- image-->

committee as well as the symposium chair for a number of international conferences, including IWCMC 2019 symposium chair, ACM TUR-C SIGSAC2020 publication chair.

<!-- image-->

<!-- image-->

Di Wu (Student Member, IEEE) received the masterâs degree in computer system engineering from the University of Houston, in 2020. He is currently working toward the PhD degree with the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His research interests include future network architecture, network artificial intelligence and space-terrestrial integrated network.

Zunliang Wang (Graduate Student Member, IEEE) is working toward the PhD degree with the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His research interests include future network architecture, network routing, network artificial intelligence, multiagent system, and flying ad-hoc networks.

Song Guo (Fellow, IEEE) received the PhD degree in computer science from the University of Ottawa, Ottawa, ON, Canada. He is currently a full professor with the Department of Computing, The Hong Kong Polytechnic University, Hong Kong. Prior to joining PolyU, he was a full professor with the University of Aizu, Aizuwakamatsu, Japan. His research interests include the areas of cloud and green computing, Big Data, wireless networks, and cyber-physical systems. He has authored or co-authored more than 300 conference and journal papers in these areas and received

multiple best paper awards from IEEE/ACM conferences. His research has been sponsored by JSPS, JST, MIC, NSF, NSFC, and industrial companies. He has served as an editor of several journals, including IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Emerging Topics in Computing, IEEE Transactions on Green Communications and Networking, IEEE Communications Magazine, and Wireless Networks. He has been actively participating in international conferences as a general chair and TPC chair. He is a senior member of ACM, and an IEEE Communications Society distinguished lecturer.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Fission Spectral Clustering Strategy for UAV Swarm Networks/page_12_img_1.jpeg|page_12_img_1]]
2. [[../extracted_images/Fission Spectral Clustering Strategy for UAV Swarm Networks/page_12_img_2.jpeg|page_12_img_2]]
3. [[../extracted_images/Fission Spectral Clustering Strategy for UAV Swarm Networks/page_12_img_3.jpeg|page_12_img_3]]
4. [[../extracted_images/Fission Spectral Clustering Strategy for UAV Swarm Networks/page_12_img_4.jpeg|page_12_img_4]]
5. [[../extracted_images/Fission Spectral Clustering Strategy for UAV Swarm Networks/page_12_img_5.jpeg|page_12_img_5]]
6. [[../extracted_images/Fission Spectral Clustering Strategy for UAV Swarm Networks/page_12_img_6.jpeg|page_12_img_6]]

---

