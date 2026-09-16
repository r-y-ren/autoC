# Delay-Aware Cooperative Task Offloading for Multi-UAV Enabled Edge-Cloud Computing

Zhuoyi Bai , Yifan Lin, Yang Cao , Member, IEEE, and Wei Wang, Senior Member, IEEE

AbstractâUnmanned aerial vehicle (UAV) has received tremendous attention in the area of edge computing due to its flexible deployment and wide coverage accessibility. In weak infrastructure scenarios, multiple UAVs can form on-site edge computing clusters to handle the real-time tasks. Further, a multi-UAV enabled edge-cloud computing system is coined by cooperating the UAVs with remote cloud, which provides superior computing capability. However, the uneven distribution of tasks makes it difficult to meet the realtime requirements when load balancing is unavailable. To address above issue, a delay minimization problem for multi-UAV enabled edge-cloud cooperative offloading is investigated in this paper. The problem is formulated as a non-convex problem based on models that reflect characteristics of the system, such as ubiquitous network congestion, air-to-ground wireless channel and cooperative parallel computing. An efficient cooperative offloading algorithm is proposed to address the problem. Specifically, convex approximation is applied to make the original problem tractable, and Lyapunov optimization is utilized to make online task offloading decisions. Finally, the correctness of the models are verified through a practical UAV-edge computing platform. Simulations based on measurement results and real-world datasets indicate that, the proposed algorithm fully utilizes the available energy to significantly reduce the tasksâ completion delay.

Index TermsâTask offloading, unmanned aerial vehicle-enabled edge computing, delay optimization

## 1 INTRODUCTION

UNMANNED aerial vehicle (UAV) has been widely used inspecial scenarios by telecommunication companies performing monitoring and rescuing missions in the postnatural disaster scenarios (e.g., fixed infrastructures have been disrupted by earthquakes), UAV is able to fly to the site to collect essential data for subsequent risk assessment. The missions demand for the real-time analysis of the complicated data. Therefore, the concept of UAV-EC (i.e., UAV enabled edge computing) has been proposed [2]. The main feature of edge computing (EC) is to push computing to the network edges (e.g., base stations and access points) so as to enable computation-intensive and latency-critical applications at the resource-limited scenarios. Compared to cloud computing, UAV-enabled edge computing can effectively reduce the transmission delay caused by extremely long distance [3]. As Huaweiâs whitepaper shows, UAV technology combined with edge computing will enable emerging areas like AI and remote sensing to new levels of automation and new types of analytic solutions [4].

Extending single node UAV-EC to multiple UAVs is an effective method to strengthen the available computation capability [5]. Moreover, a multi-UAV enabled EC system can be further augmented by connecting to the remote cloud, which forms a multi-UAV enabled edge-cloud computing system. The system does not violate the post-natural disaster scenarios assumption. Multi-hop UAV relay network enables the UAVs to communicate with the remote Base Station (BS) [6]. Besides, the combination of UAV-EC and cloud computing is to realize complementary advantages. Edge computing has extremely low transmission delay, and cloud computing has abundant computation capability. When the load of tasks exceeds the computation capability of the UAV cluster, the exceeded tasks will be offloaded to the ground BS through air-to-ground link. Then the BS forwards the tasks to the remote cloud through the wired link.

Nevertheless, computation capabilities and task loads among UAVs are commonly following uneven distribution [7]. The unbalanced loads make part of UAVs endure a large amount of tasks with others in idle. Then the most taskheavy edge node leads to an extremely long computation delay. As a consequence, the real-time requirements may not be satisfied. In order to reduce the system delay, several theoretical researches have been proposed formerly from different perspectives such as trajectory optimization, resource allocation, etc [8], [9]. However, the methods are unable to adjust the computation loads among UAVs fundamentally. Thereby, in this paper, we investigate the task cooperative offloading strategy to balance the loads. Cooperative task offloading is not well investigated in the scenario of multi-UAV enabled edge-cloud system, but it has been proved as a critical factor for the performance improvement in EC systems [10]. UAVs with less computation capability can offload part of workload to other UAVs to improve the overall efficiency of the system. Though cooperative offloading algorithms has been studied in the traditional ground edge-cloud systems [11]. the algorithms are not compatible with the multi-UAV enabled edgecloud systems. The two kinds of systems have different characteristic in terms of communication, computing and power supply.

Compared to traditional edge-cloud computing at the ground, introducing UAVs brings new challenges: (i) Network congestion is ubiquitous in UAV wireless networks, especially when the UAV is streaming data [12]. (ii) Air-toground wireless backhaul is different from the wireless communications at ground. Accurate air-to-ground channel should be adopted to model the communication between UAV and the BS. (iii) Unlike the ground scenarios with massive tasks, multiple UAVs usually work together to handle a single mission. New model of mission completion delay should be carefully designed when the cooperation among UAVs are available. (iv) The difficulty of recharging UAVsâ batteries during a mission results in more strict energy constraints.

Besides, existing researches which consider the UAVenabled edge computing also have some aspects that are not covered. Multi-UAVs edge computing neglects the cooperation with the remote cloud [5], [13], [14], [15], resulting in an extremely different model from multi-UAV enabled edgecloud computing systems. Meanwhile, although some researches consider the UAV enabled edge-cloud systems, most of them are with the objective to minimize the energy consumption [16], [17]. Few researches focus on the delay optimization in UAV enabled edge-cloud computing [18], but the essential factors (e.g., topology, network congestion, resource reservation based on virtualization, and the stochastic occurrence of practical tasks) have not been considered. As a consequence, an efficient cooperative offloading scheme in multi-UAV enabled edge-cloud computing should take into account more aspects than in existing researched scenarios.

In this paper, we comprehensively consider the characteristics of the UAV-EC systems, and propose a cooperative framework to solve the problem of uneven tasks distribution. Meanwhile, according to our knowledge, this is the first time to utilize online tasks offloading to minimize the total service delay in the multi-UAV enabled edge cloud computing framework. The main contributions of this paper are summarized as follows:

A more comprehensive and realistic model focusing on multi-UAV enabled edge-cloud tasks offloading is proposed. Essential aspects corresponding to the practical systems have been introduced, to avoid the deviation from reality.

Online optimization is adopted for the first time to optimize the service delay of multi-UAV enabled edge-cloud computing systems. An algorithm based on Lyapunov optimization and convex approximation is proposed to obtain the delay-optimal task offloading decision, with rigorous mathematical proofs.

A real-world UAV enabled edge computing platform is constructed to guide the model verification. Measurements based on the platform indicate the correctness of the proposed model. Furthermore, utilizing the real-world datasets, data-driven simulation experiments have been performed to corroborate that the proposed algorithm can reach a nearoptimal performance on system delay.

The remainder of the paper is organized as follows. Section 2 reviews related work. Section 3 presents the system model, then Section 4 formulates the delay-aware cooperative offloading problem and proposes the Lyapunov optimal-based cooperative algorithm. Performance evaluation has been implemented in Section 5. Finally, conclusions are provided in Section 6.

## 2 RELATED WORK

UAV-enabled edge computing attracts the wide attention of industry and academia. DJI, as the largest consumer rotary-wing UAV company in the world, has launched the Manifold 2 high-performance onboard computer1 in 2019, to perform complex computing tasks and advanced image processing literally on the fly. Qualcomm produced the Flight RB5 5 G platform2 as the worldâs first 5 G and AIenabled UAV platform for accurate edge inferencing that reduces processing time for mission-critical UAV applications. Meanwhile, Verizonâs researchers are testing how edge computing and artificial intelligence can help UAVs detect, interpret and respond to changing weather conditions in real time [19]. In addition, multiple UAV-enabled edge nodes can be utilized to explore larger areas in the scenarios.

Several schemes are also proposed to improve the UAVenabled edge computing systemâs performance. Zhou et al., focused on the secrecy capacity problem of the UAVenabled EC systems to explore the trade-off between the security and latency [8]. Trajectory optimization of the UAV edge nodes has been considered in [9], [20], [21] to jointly design the computation and communication strategies. Similarly, UAVâs placement problem in the UAV-aided EC networks was investigated in [22]. Different from these work, this paper attempts to achieve performance improvement from the perspective of task offloading.

Zhou et al., studied the offloading algorithm of single UAV-enabled EC system to achieve computation rate maximization [2]. However, computation capacity of the edge computing units carried by single UAV may be insufficient to meet the requirement of large amount of computation tasks. Extending single UAV to multiple UAVs is an effective solution to reinforce the computation capacity. Specifically, Ma et al., modeled the multi-UAV EC system and proposed a potential game-based cooperative offloading algorithm, in which UAVs can offload the tasks to each other, to achieve the optimal computation delay [5]. However, game-based cooperative offloading ignores that, extending the EC system causes the parallel computing, i.e., the tasks completion delay depends on slowest edge node among multiple UAVs. The ignorance leads to a disconnect between the algorithm and the actual scenario. Apart from multi-UAV enabled edge nodes, another method was proposed to expand the computation capacity by incorporating cloud server. The wide coverage of UAVâs communication module enables UAV to offload part of task workload to the remote cloud for alleviating the computation pressure [23].

As a consequence, Luo et al., requested the multiple UAVs for offloading all the computation tasks to the cloud server [24]. However, the long-distance and multi-hop communication brings a large overhead. For this consideration, Jeong et al., introduced an offloading strategy that single UAV can not only offload tasks to the remote cloud but also compute part of the tasks locally [21]. Combining the multi-UAV edge nodes and the cloud server, a multi-UAV enabled edge-cloud system occurs. In the system, UAVs are able to offload the tasks to other UAVs or the cloud server. Several researches have focused on the multi-UAV enabled edgecloud system. A decentralized computation offloading mechanism for such system was proposed to achieve the energy cost minimization in [16]. Meanwhile, Xu et al., formulated a stochastic optimization problem with the goal of minimizing the energy consumption in cellular-connected multi-UAV edge computing networks [17]. Energy cost minimization is absolutely a key factor to maintain the reliability, while the computation delay minimization should also be considered in the strategy as a basis for judging whether the critical mission is successfully executed [25]. Compared with [16], [17], we focus on the delay optimization while meeting the energy constraints to satisfy the real-time requirements. Although some literatures considered delay as a metric while using multi-UAV to assist the edge-cloud computing [26], [27], UAVs in those literatures were not treated as edge nodes but communication relays. The scenarios of [18] is similar to this study, which considers delay-optimal tasks offloading for UAV-enabled edge-cloud computing systems. However, essential factors (e.g., topology, network congestion, resource reservation based on virtualization) are not considered, making the algorithm infeasible to deploy in practical scenarios.

Consequently, it is foreseen that UAV-enabled edgecloud computing system will be an important trend for edge computing scenarios due to the significantly improved performance upper bound, the flexible deployment and the wide coverage. However, research on multi-UAV enabled edge-cloud cooperative task offloading is still limited. Especially, the cooperative offloading for delay minimization has not been investigated well in the practical multi-UAV enabled edge-cloud computing. Minimizing the service delay of the UAV-enabled edge-cloud system is still a challenge remains to be handled. To make up the gap, this work aims to reduce the system delay to meet the real-time requirements of delay-critical missions in special scenarios from the perspective of cooperative offloading strategy.

## 3 SYSTEM MODEL

As depicted in Fig. 1, we consider an edge-cloud computing system consisted with a BS/ground station (connected with remote cloud) and U rotary-wing UAVs acting as edge computing nodes. All UAVs are executing delay-critical missions and carrying edge computing units. The UAVs are indexed by $\mathcal { U } = \{ 1 , 2 , . . . , U \}$ and the BS is indexed by 0. We consider a sys-U Â¼ f gtem with an expected running time of T slots, and in each slot there will be a number of new data processing tasks generated.

<!-- image-->  
Fig. 1. Multi-UAV enabled edge-cloud computing system.

There are two possible sources of the tasks in practical scenarios. One is ground users/devices. For example, when the desert scientific research mission needs UAVs to enhance computation capability to analyze the complicated data, the ground researchers will generate the tasks and offload them to the nearby UAVs. The other source is UAV itself. Considering the reconnaissance scenario, the UAVs collect large amounts of image and video data for analysis. Thus, UAVs are task generators as well as mission executors. Both sources can be assumed in our model that, the UAV has some tasks to be handled at the beginning of the slot. The length of each time slot is set as to tdepict the real-time requirement of the tasks. In general, a newly generated/received task is considered to be successfully executed only when it is accomplished in the current time slot. However, it is unrealistic for all tasks to be completed in one slot when the number of tasks extremely exceeds the available computing capability. Thereby, the objective for the cooperative offloading is to maximize the probability that tasks can be completed in one slot. Define the delay for UAV iâs tasks completion in slot t as service delay $D _ { i } [ t ]$ , then the objective is

$$
\operatorname* { m a x } _ { i \in \mathcal { U } } \operatorname* { P r } \{ D _ { i } [ t ] < \tau \} ,\tag{1}
$$

is set to depict the real-time requirement, i.e., the length of tthe time slot. The value of depends on the feature of the tpractical mission. In other words, can be adjusted accordting to different missions. However, $D _ { i } [ t ]$ is a subjective vari-Â½ able, determined by the practical offloading strategy, which means its probability density function is difficult to obtain. Therefore, we adjust the objective from optimizing a probability to an exact value. No matter how large is, minimizting the service delay will guarantee the maximal probability for tasksâ real-time completion. Thus, the optimization objective can be transformed to an alternative form.

$$
\operatorname* { m i n } _ { i \in \mathcal { U } } D _ { i } [ t ] .\tag{2}
$$

$D _ { i } [ t ]$ reflects the individual UAV iâs service delay. In Â½ order to reflect the overall system service quality, we further define system delay as the summation of service delays of all tasks in all time slots. In summary, the objective set as to minimize the system delay

$$
\operatorname* { m i n } \sum _ { t = 0 } ^ { T - 1 } \sum _ { i = 1 } ^ { U } D _ { i } [ t ] .\tag{3}
$$

After T slots, the UAV swarm will fly back and terminate the mission. Considering that there is a center controller executing the scheduler algorithm to decide the taskon July 16,2024 at 03:14:22 UTC from IEEE Xplore. Restrictions apply.

offloading strategy. The center controller may be one of the UAVs or the ground station, who has the global information at the beginning of each slot, i.e., the number of tasks generated and the computation capability of each UAV. Thus, when a new task is received by a UAV, the controller will decide which device is most suitable for offloading, then claim the UAV to offload the task to the selected device. Therefore, a task would experience a two-stage delay before its completion, namely the communication delay and the computation delay. The communication delay is the latency caused by task transmission from a UAV to other devices, while the computation delay is caused by task computation.

- t and $\pi _ { i j } [ t ]$ are used to describe UAV iâs task arrival rate Â½  p Â½ and the number of tasks offloaded to UAV j (or BS) from i in time slot $t ,$ respectively, of which $t \in \{ 1 , 2 , \dots , T \} , i \in \mathcal { U }$ and $j \in \mathcal { U } \cup \{ 0 \}$ 2 f g 2 U. The tasks are assumed to be divisible, i.e., partial 2 U [ f goffloading is allowed in our work. In other words, $\pi _ { i j } [ t ]$ is not p Â½ always an integer. For example, when executing video monitoring mission, UAV i has 1,000 frames for an analysis task. Then UAV i has the chance to offload 300 frames to $\operatorname { U A V } j$ to alleviate the computation pressure, i.e., $\pi _ { i j } [ t ] = 0 . 3$ . Moreover, we have $\pmb { \lambda } [ t ] = \{ \hat { \lambda } _ { 1 } [ t ] , \lambda _ { 2 } [ t ] , \allowbreak , \allowbreak \dots , \lambda _ { U } [ t ] \}$ ; $\pmb { \pi } [ \tilde { t } ] = \{ \pmb { \pi } _ { 1 } [ t ] , \pmb { \pi } _ { 2 } [ t ] , \dots ,$ $\pi _ { U } [ t ] \}$ Â½and ${ \pmb \pi } _ { i } [ t ] = \{ \pi _ { i 0 } [ t ] , \pi _ { i 1 } [ t ] , . . . , \pi _ { i U } [ t ] \}$ Â¼ fp Â½  p Â½ . Assume that all p Â½ g p Â½  Â¼ fp Â½  p Â½  p Â½ gUAVs have the ability to communicate with the BS, i.e., all tasks received by UAVs can be offloaded to the remote cloud.

UAVâs flight trajectory is not considered in our model because the UAVs are assumed to be static to execute the mission. Though the UAVs keep hovering through all time slots, they have the ability to handle most of computation missions, and moving objects can still be handled by static UAVs. Considering that UAVs are monitoring the ground or collect ground sensorsâ information. Due to the development of high speed camera and the matureness of a variety of sensors born for high speed environment, it is convenient for UAVs to complete the mission. Even in the case of forest fires, UAVs can also take advantage of their camera to obtain infrared images.3 Considering another scenarios that UAVs serve as base stations in the air to provide wireless link or computing service. The coverage capability and the stability of hovering UAV-BS has been verified by AT&T.4 The capability can fully meet moving usersâ service requirements.

The key notations of the model are presented in Table 1 for clarity. Next, we will present mathematical models to describe the delay and energy consumption on communication and computation.

## 3.1 UAV-to-UAV Transmission Model

Due to the fewer obstacles and the closer distance between UAVs, we assume that the wireless links are Line-of-Sight (LoS) during UAVs interacting with each other. Without loss of generality, we denote $R _ { i }$ as the UAV-to-UAV achievable rate. In addition, the network topology should be considered when modeling the UAV-to-UAV channel. There are two kinds of network topology for UAV-to-UAV transmission, i.e., star network topology and mesh network topology. In the star network topology, a node acting as the hotspot forwards the information to other nodes. In the mesh network topology, nodes relay traffic for other nodes on the path. Mesh [28] has been widely used in fixed-wing aircraft networking and several studies have investigated the rotary-wing UAV mesh networks [29]. However, the mainstream communication protocol for rotary-wing UAV communication, i.e., MAVLink [30], is still based on the control station system to execute the UAV-to-UAV communication, which corresponds to the star network topology. Thereby, in this subsection, star-shape network is used to describe the UAV-to-UAV network. Existing work [31], [32] commonly consider the delay of task transmission among edge nodes as a linear model, i.e., in the Local Area Network (LAN) consists of UAVs, transmission delay is proportional to the number of offloaded task, as Equation (4) depicts.

TABLE 1 Summary of Frequency Used Notations
<table><tr><td>Notation</td><td>Definition</td></tr><tr><td> $\boldsymbol { \mathcal { U } }$ </td><td>The set of UAVs carrying EC units  $\{ 1 , 2 , \ldots U \}$ </td></tr><tr><td> $\gamma$ </td><td>Coefficient to describe the network congestion</td></tr><tr><td> $\omega$ </td><td>Energy consumption for UAV-to- UAV transmission</td></tr><tr><td> $\lambda _ { i } [ t ]$ </td><td>Number of UAV i&#x27;s tasks before</td></tr><tr><td> $\beta _ { i } [ t ]$ </td><td>offloading Number of tasks offloaded by UAV</td></tr><tr><td> $\mu _ { i } [ t ]$ </td><td>i at time slot t Numberof tasksoffloaded to UAV i at time slot t</td></tr><tr><td> $\pi _ { i j } [ t ]$ </td><td>Numberof tasksoffloadedfromi</td></tr><tr><td> $P _ { i }$ </td><td>to j at time slot t Transmit power of UAV i for</td></tr><tr><td> $g _ { u }$ </td><td>communicating with BS Power gain of wireless channel at a</td></tr><tr><td> $\sigma ^ { 2 }$ </td><td>referencedistance The noise power of UAV-to-BS</td></tr><tr><td> $\Gamma$ </td><td>channel SNR gap between practical and</td></tr><tr><td>Î±</td><td>theoretical signaling The path loss exponent of large-</td></tr><tr><td> $\mathbf { a } _ { i } [ t ]$ </td><td>scale fading UAV i&#x27;s horizontal location at time</td></tr><tr><td>S</td><td>slot t Number of bits to be processed for</td></tr><tr><td>1</td><td>a task Number of CPU cycles for</td></tr><tr><td> $D _ { B S }$ </td><td>computing one bit data Delay for interaction between the</td></tr><tr><td> $\xi$ </td><td>BS and the cloud Energy consumption for UAV-to-</td></tr><tr><td> $f _ { i }$ </td><td>BS transmission CPU frequency of UAV i&#x27;s EC unit</td></tr><tr><td> $\kappa$ </td><td>CPU&#x27;s parameter depends on chip</td></tr><tr><td> $q _ { i } [ t ]$ </td><td>architecture The virtual energy deficit of UAV i</td></tr><tr><td> $\bar { E } _ { i }$ </td><td>at time slot t Expected energy budget for UAV i</td></tr></table>

$$
D _ { i , L i n e a r } ^ { L A N } = \beta _ { i } [ t ] \frac { s } { R _ { i } } .\tag{4}
$$

$D _ { i } ^ { L A N }$ is the transmission delay caused by UAV i offloading its tasks to other UAVs. $\beta _ { i } [ t ]$ is the number of tasks that be b Â½ offloaded to other UAVs by UAV i, denoted by $\beta _ { i } [ t ] =$ $\textstyle \sum _ { j = 1 , j \neq i , j \neq 0 } ^ { U } \pi _ { i j } [ t ]$ . s is the expected number of bits to be proc-Â¼ 6Â¼ 6Â¼ p Â½ essed for a task. Define $\beta [ t ]$ as the total number of offloaded bÂ½ tasks by all UAVs during time slot $t ,$ which can be described as $\begin{array} { r } { \beta [ t ] \stackrel { \cdot } { = } \sum _ { i = 1 } ^ { U } \beta _ { i } [ t ] } \end{array}$

<!-- image-->  
Fig. 2. Queue of data in the star-shape network.

bÂ½  Â¼ Â¼ b Â½ When multiple UAVs offload their tasks concurrently in the star-shape network, congestion occurs because the bandwidth and the buffer are limited, which affects transmission latency critically. Multiple UAVs construct a LAN through the center node (i.e., the hotspot) who realizes the resource sharing. As Fig. 2 depicts, the tasksâ data from UAVs form a queueing model in the hotspot, and the hotspot forwards the data to other UAVs basing on the offloading decision. The limited bandwidth and buffer cause the service rate lower than arrival rate, which makes the length of the queue increase in a non-linear pattern [33]. Therefore, congestion which depends on the total traffic in the LAN should be taken into account in the transmission model. Here we only consider the queue at hotspot. There are two main reasons. (i) The star-shape topology determines the hotspot will be the bottleneck link. A queue is formed when the service rate is less than arrival rate. Even a UAV receives tasks from several other UAVs, the traffic on it will not more than the traffic on the hotspot. Thus, the hotspot holds the highest arrival rate. Meanwhile, the service rate of the hotspot is the lowest because it is responsible for forwarding while others only need restore the tasks in local buffer. Therefore, the bottleneck should be the hotspot, which leads to the network congestion. (ii) Compared to sending, receiving tasks is not time-consuming. Existing methods make data receiving efficiently. For example, I/O multiplexing in Linux (e.g., epoll) can monitor the incoming data of multiple ports in batches, and the multi-coroutines are able to handle the jobs for receiving data concurrently. Industrial enterprises have widely adopted the methods (e.g., I/O multiplexing and multi-coroutines) to reduce the delay of receiving significantly. In conclusion, the effect of UAV iâs queue delay will not show up in our system.

M/M/1 model [34] was previously adopted by [35], [36] to describe the network congestion in the LAN make up of several wireless devices. The authors assume that the service rate of the LAN is a variable following exponential distribution and the data size of computation tasks offloaded to each device follows the exponential distribution. Nevertheless, most of the modern remote procedure call (RPC) protocols (e.g., Googleâs gRPC [37]) using in the distributed system, or the commonly used messaging protocol $( \mathrm { e . g . }$ , MQTT protocol [38]) in M2M (machine to machine) scenario, are both based on TCP protocol. TCP protocol has its own congestion control and avoidance mechanisms. Thus, congestion happens inevitably but the impact will not be as severe as the M/M/1 model due to the mechanisms. TCP alleviates the network congestion at the cost of transmission performance. Thereby, comparing with the linear model, a coefficient should be added to reflect the loss of performance.

$$
D _ { i } ^ { L A N } = \gamma \cdot \beta _ { i } [ t ] \frac { s } { R _ { i } } .\tag{5}
$$

Nevertheless, $\gamma$ is not a constant. As network traffic gincreases, so does the overhead for controlling congestion. Thereby, it can be considered that $\gamma$ is a function whose argument is the overall traffic t

$$
\gamma = \gamma _ { 1 } \beta [ t ] s + \gamma _ { 2 } .\tag{6}
$$

Therefore, the UAV-to-UAV transmission delay of UAV i in the system can be denoted as

$$
D _ { i } ^ { L A N } = ( \gamma _ { 1 } \beta [ t ] s + \gamma _ { 2 } ) \frac { \beta _ { i } [ t ] s } { R _ { i } } .\tag{7}
$$

Once a task is offloaded, UAV who receives the task will immediately start computing because of the asynchronous multithreading method [39]. To verify the UAV-to-UAV transmission delay model, measurement has been done on a practical experiment platform. Related results are recorded in Section 5.1.2. The results indicate that the model in Equation (7) is more relevant to reality compared with the linear model and the M/M/1 model.

Define the expected average energy consumption for transmitting a task between UAVs as $\omega ,$ then in time slot $t ,$ UAV $i \prime \mathrm { s }$ v energy consumption for offloading tasks to other UAVs can be modeled as

$$
E _ { i } ^ { L A N } [ t ] = \omega \cdot \beta _ { i } [ t ] ,\tag{8}
$$

is an expected value of the average energy consumption vfor transmitting a task via the LAN. Since all UAVs complete a mission together, the tasks of each UAV are assumed to be isomorphic. Thus, differences in tasks of various UAVs are considered small. Without loss of generality, even if the tasksâ sizes are not as the same, the operation of taking expected value will ignore those differences. The idea of taking the expected value is also used in the following subsections.

## 3.2 UAV-to-Cloud Transmission Model

In recent years, there have been many researches on UAV communications, and the modeling of the UAV-to-Ground channel is relatively mature. So in this subsection, classical UAV-to-Ground wireless channel is adopted to model the transmission delay between UAV edge node and the cloud server when offloading the tasks. Assume that all UAVs hovers at a constant altitude $H ,$ BS locates at ${ \bf a } _ { B S } =$ $( x _ { B S } , y _ { B S } )$ and UAV $i \prime \mathrm { s }$ Â¼horizontal location at time slot t is ${ \bf a } _ { i } [ t ] = ( x _ { i } [ t ] , y _ { i } [ t ] )$ . The tasks offloaded by UAVs to the cloud Â½  Â¼ Ã° Â½  Â½ Ãwill arrive at the nearby BS then will be forwarded to the remote cloud. The environment between UAV and BS is complicated, both the Line of Sight (LoS) channel and the Non-Line of Sight (NLoS) channel should be considered.

Considering LoS channel, free space transmission loss was used to depict the air-to-ground channel [40]. The channel power gain between the UAV and the BS, denoted by $h _ { i } [ t ]$ , can be given as

$$
h _ { i } [ t ] = g _ { u } d _ { i , 0 } ^ { - 2 } = \frac { g _ { u } } { H ^ { 2 } + \left\| \mathbf { a } _ { i } [ t ] - \mathbf { a } _ { B S } \right\| ^ { 2 } } ,\tag{9}
$$

$g _ { u }$ is the channel power gain at a reference distance $d _ { 0 } = 1 \mathbf { m }$ Â¼Thus, the achievable rate of LoS channel can be denoted as

$$
R _ { i , L o S } ^ { s } [ t ] = { \cal B } \mathrm { l o g } _ { 2 } \bigg ( 1 + { \frac { h _ { i } [ t ] { \cal P } _ { i } } { \sigma ^ { 2 } } } \bigg ) ,\tag{10}
$$

B is the bandwidth allocated to UAVs to communicate with BS, $P _ { i }$ is the transmit power of UAV $i ,$ and $\sigma ^ { 2 }$ denotes the noise power.

Considering NLoS channel, there are tall buildings as obstacles between UAV and BS, and distance is far, so large-scale fading and small-scale fading should be taken into account. In this case, we adopt classical air-to-ground channel model in [41], which uses block fading channels to model the link, so data rate of the link between UAV i and BS can be modeled as

$$
R _ { i , N L o S } ^ { s } [ t ] = { \cal B } { \log } _ { 2 } \left( 1 + \frac { F ^ { - 1 } ( \epsilon ) P _ { i } g _ { u } } { \sigma ^ { 2 } \Gamma \Big ( H ^ { 2 } + { \| { \bf { a } } _ { i } [ t ] - { \bf { a } } _ { B S } \| ^ { 2 } } \Big ) ^ { \alpha / 2 } } \right) ,\tag{11}
$$

$F ( \cdot )$ denotes the identical cumulative distribution function Ã°Ã(CDF) of small-scale fading block. In this paper, we consider the Rician fading channels with Rician factor $K _ { c } ,$ and the CDF function can be expressed by $F ( z ) = 1$ $Q _ { 1 } ( \sqrt { 2 K _ { c } } , \sqrt { 2 ( K _ { c } + 1 ) z } )$ where $Q _ { 1 } ( a , b )$ Ã° Ã Â¼ is the Marcum-Q Ã°function, $\dot { K _ { c } } = 1 0 \left[ 4 1 \right]$ Ã Ã° Ã.  means the maximum tolerable out-Â¼age probability, $\Gamma > 1$ is the SNR gap between the practical modulation schemes and the theoretical Gaussian signaling, $\alpha \geq 2$ is the path loss exponent of large-scale fading.

Both LoS channel and NLos channel should be involved to describe the complicated UAV-to-Ground channel. For this reason, the method proposed by [42] is adopted which regards the UAV-to-Ground channel as the weighted sum of LoS and NLoS channel. The weight is adapted to the terrain environment such as urban, suburban, etc.

$$
R _ { i } ^ { s } [ t ] = \operatorname* { P r } ( L o S , \theta ) \cdot R _ { i , L o S } ^ { s } [ t ] + \operatorname* { P r } ( N L o S , \theta ) \cdot R _ { i , N L o S } ^ { s } [ t ] .\tag{12}
$$

$\operatorname* { P r } ( L o S , \theta )$ is the probability of LoS channel. $\operatorname* { P r } ( N L o S , \theta ) =$ $1 - \operatorname* { P r } ( L o S , \theta )$ and the probability is given as

$$
\operatorname* { P r } ( L o S , \theta ) = \frac { 1 } { 1 + a e ^ { - b ( \theta - a ) } } ,\tag{13}
$$

a and b are parameters contingent on different environments $( \mathrm { e . g . , }$ suburban, urban, dense urban). The model predicts the expectation of channel path loss from the perspective of statistics.

The model mentioned above considers several scenarios. However, an essential scenario for UAVâs mission execution has not been considerd, i.e., forest. Near Line of Sight (nLoS) has been proposed to depict the air-to-ground channel under the forest scenario. Therefore, we adopted a classical nLoS air-to-ground model to improve our model [43]. The path loss in nLoS channel is denoted as

<!-- image-->  
Fig. 3. Achievable rate of UAV-to-cloud link.

$$
\begin{array} { r l } & { L _ { \mathrm { F I T U - R } } ( \mathrm { d B } ) = 0 . 3 9 f ^ { 0 . 3 9 } d ^ { 0 . 2 5 } } \\ & { \quad L _ { \mathrm { F G R } } ( \mathrm { d B } ) = 1 0 n \mathrm { l o g } _ { 1 0 } ( d ) - 2 0 \mathrm { l o g } _ { 1 0 } ( h _ { T } ) - 2 0 \mathrm { l o g } _ { 1 0 } ( h _ { R } ) } \\ & { L _ { \mathrm { f o r e s t } } ( \mathrm { d B } ) = L _ { \mathrm { F I T U - R } } + L _ { \mathrm { F G R } } . } \end{array}\tag{14}
$$

The model is named as âFITU-R+FGRâ. f is the frequency of the radio wave (in MHz). d is the distance between the isotropic transmit and receive antennas in meters. n is a parameter related to $f . \ h _ { T }$ and $h _ { R }$ are the height of transmitter and receiver, respectively. However, we found that Eq. (12) actually includes the âFITU-R+FGRâ model. nLoS can be approximately considered as an intermediate state between LoS and NLoS. Through fitting the model, $a = 4 . 0 5 1 0 3 7 4 , b = 0 . 0 4 7 8 9 6 3$ are set. When setting Â¼ Â¼the parameters, the rate that Eq. (12) achieves is almost identical to the rate âFITU-R+FGRâ achieves, as Fig. 3 shows. In Fig. 3, the curve âForest-fittedâ is the results when setting a and b in $\operatorname { E q . }$ (12), with $P _ { i } = 0 . 1$ Watts assumed. Â¼Therefore, the achievable rate of UAV-to-Cloud channel in our system can still be set as $\operatorname { E q } .$ . (12). The parameters $a =$ 4:0510374 and $b = 0 . 0 4 7 8 9 6 3$ Â¼are needed when the scenario is in forest.

In addition, Remote cloud is supposed to be far from the BS. Thus, when the BS forwards tasks to the cloud through a wired link, latency is inevitable. The latency caused by one task offloaded from UAV to the cloud can be denoted as

$$
D _ { i } ^ { d } [ t ] = \frac { s } { R _ { i } ^ { s } [ t ] } + D _ { B S } ,\tag{15}
$$

$s / R _ { i } ^ { s } [ t ]$ is the delay while offloading a task from UAV i to the Â½ BS, and $D _ { B S }$ is the delay for exchanging data (bits to be processed and the computation results) between the BS and the cloud. It is necessary to set the $D _ { B S }$ . Though BS forwards the tasks to the remote cloud exchanges data through wired link, there is still high latency due to the distance. Using Ping command to measure the Round-Trip Time (RTT) between local host (Wuhan City) and a cloud server (Hong Kong), the average latency is 200.625 ms (with the distance of 1105 km). Due to the fact that data amount of computation results is tiny, delay caused by feedback from the BS to the UAV is not considered.

Furthermore, define the expected average energy consumption for transmitting a task from a UAV to the BS as $\xi ,$ then UAV iâs energy consumption for offloading tasks to the cloud is

$$
E _ { i } ^ { d } [ t ] = \xi \cdot \pi _ { i 0 } [ t ] .\tag{16}
$$

<!-- image-->  
Fig. 4. Tasks of UAV1 computed by the UAV cluster.

## 3.3 Computation Model

The computation time of the cloud is neglected since it has much stronger computation capability than the UAVmounted EC unit. The energy consumption of the cloud is not involved in the multi-UAV system. Thereby, in this section, only the delay and the energy consumption caused by UAVâs computation are taken into account. Define the CPU frequency of each UAV-mounted EC unit, as $\mathbf { f } = \{ f _ { 1 } , f _ { 2 } , . . . , f _ { U } \}$ . It is Â¼ fassumed that each EC unit has multiple cores.

To overcome the incompatibility when executing the programs in UAVs with heterogeneous specs, the UAV cluster (formed by U UAVs) is assumed to leverage the virtualization technology or containerization technology [44]. The virtual machines within a UAV are prepared to complete the tasks from other UAVs. For example, UAV $\mathrm { \nabla } _ { i ^ { ' } s }$ virtual machine, which prepares for UAV ${ \mathrm { ~ \it ~ { ~ j ~ } ~ } } ,$ will remain idle and hardly occupy the CPU until $j ^ { \prime } \mathbf { s }$ tasks offloaded to i. Assuming that each virtual machine or container has the ability to occupy single thread, a UAV can compute the tasks from different UAVs concurrently, and tasks for single virtual machine are still executed in sequence. As illustrated in Fig. 4, the task of UAV 1 is divided into four subtasks, each subtask is offloaded to the corresponding UAV j which is represented by the corresponding color. Owing to Time Division Multiplexing mechanism and the fact that computation delay is much longer than communication delay, the starting point of different virtual machines (or containers) in UAV i for tasks computation can be considered almost simultaneously (the validity of the assumption is verified in Section 5.1.3.), then the completion time of whole task depends on the slowest subtask of the computation.

Considering the multi-UAV edge-cloud system as a distributed system, the tasks offloaded by UAV i are executed in parallel by other UAVs but not in sequence. Thus, the computation delay of UAV iâs tasks in the slot depends on the longest delay among the devices, as Fig. 4 depicts. For this reason, computation delay for all tasks offloaded by UAV i in time slot t can be modeled as

$$
D _ { i } ^ { c a l } [ t ] = \operatorname* { m a x } _ { j \in \mathcal { U } } \bigg \{ \pi _ { i j } [ t ] \frac { s \cdot l } { f _ { j } } \bigg \} ,\tag{17}
$$

l is the expected number of CPU cycles to compute 1 b data. The verification of the computation delay model can be found in Section 5.1.3, and the verification results indicate the model is corresponding with the practical scenario.

Denote $\begin{array} { r } { \mu _ { i } = \sum _ { k = 1 } ^ { U } \pi _ { k i } [ t ] } \end{array}$ as the number of tasks that offm Â¼ Â¼ p Â½ loaded to UAV i by other UAVs at time slot t. Energy consumption caused by computation is proportional to the square of CPU frequency [2], so UAV iâs energy consumption for computation at time slot t is denoted by

$$
E _ { i } ^ { c a l } [ t ] = \kappa f _ { i } ^ { 2 } \cdot \mu _ { i } [ t ] ,\tag{18}
$$

is the parameter depends on effective switched capaciktance of CPUâs chip architecture and computation task itself.

## 4 PROBLEM FORMULATION AND SOLUTION

## 4.1 Problem Formulation

In our assumption, a UAV is unable to communicate with several UAVs and the BS simultaneously due to singleantenna. Therefore, we assume that each UAV occupies the channel in a CSMA (Carrier Sense Multiple Access) manner during UAV-to-UAV communication. Meanwhile, multiple UAV-to-BS links are in time-sharing manner, i.e., TDMA (Time Division Multiple Access). Thus, different UAVs within the LAN can offload the tasks to each other in concurrently, while the tasks from a UAV to the cloud are sent in order. More specifically, multi-hop communication is still in the form of summation. From the above, UAV iâs service delay (i.e., delay to accomplish all tasks generated/received by i in time slot t) can be donated by

$$
D _ { i } ( { \pmb \pi } [ t ] ) = D _ { i } ^ { L A N } [ t ] + D _ { i } ^ { c a l } [ t ] + { \pi } _ { i 0 } [ t ] D _ { i } ^ { d } [ t ] ,\tag{19}
$$

and its energy consumption is

$$
E _ { i } ( { \pmb \pi } [ t ] ) = E _ { i } ^ { L A N } [ t ] + E _ { i } ^ { c a l } [ t ] + E _ { i } ^ { d } [ t ] ,\tag{20}
$$

$E _ { i } ( { \pmb \pi } [ t ] )$ contains two kinds of energy consumption. One is Ã°pÂ½ Ãcaused by computation for the tasks offloaded by all UAVs (other UAVs and itself), while the other energy consumption is caused by transmitting part of tasks to other devices (other UAVs or the BS).

The purpose is to minimize the system delay within the battery budget. Problem can be formulate as follow:

$$
\begin{array} { r l } & { \displaystyle \mathbf { P } \mathbf { 1 } \operatorname* { m i n } _ { \pi } \displaystyle \operatorname* { l i m } _ { T \to \infty } \overline { { T } } \sum _ { t = 0 } ^ { T - 1 } \sum _ { i = 1 } ^ { U } D _ { i } ( \pi [ t ] ) } \\ & { \displaystyle s . t . \begin{array} { r l } & { 1 } \\ & { T \to \infty } \\ & { C 2 : \pi _ { i j } [ t ] \geq 0 , \forall i \in U [ t ] ) \leq \bar { E } _ { i } , \forall i \in U } \end{array} } \\ & { \begin{array} { r l } & { C 2 : \pi _ { i j } [ t ] \geq 0 , \forall i \in U , \forall j \in \{ 0 \} \cup \mathcal { U } , \forall i } \\ & { C 3 : \displaystyle \sum _ { j = 0 } ^ { U } \alpha _ { i j } [ t ] = \lambda _ { i } [ t ] , \forall i \in \mathcal { U } , \forall i } \end{array} } \\ & { \begin{array} { r l } & { C 4 : \mu _ { i } [ t ] \leq \frac { f _ { j } T } { s ! } , \forall i \in \mathcal { U } , \forall i . } \end{array} } \end{array}\tag{21}
$$

Constraint C1 means UAVâs energy consumption cannot violate the long term energy constraint, $\bar { E } _ { i }$ is the expected energy budget for UAV i at each time slot. C2 avoids invalid values in cooperative offloading decision. C3 guarantees that tasks offloaded from UAV i is equal to the tasks on July 16,2024 at 03:14:22 UTC from IEEE Xplore. Restrictions apply.

generated by the UAV, and C4 guarantees that the tasks offloaded to UAV i will not exceed its computation capability.

The energy consumption for UAV hovering is not considered in our system. The system does not involve energy sharing between flight control modules $( \mathrm { e . g . }$ , motors) and edge computing modules $( \mathrm { e . g . }$ , communication and computation modules) because we utilize two separate power supply. Through the separate power supply, energy consumed by edge computing will not affect the power supply for flight control, and several hazards $( \mathrm { e . g . } ,$ , overcurrent damage) can also be avoided. Meanwhile, formulating hovering energy consumption will not affect the problem. Assuming the power for maintaining hovering is $\bar { \kappa }$ Watts and the length of Ka time slot is  seconds, energy consumption caused by hov-Xering can be seemed as a fixed value ${ \bar { \kappa \cdot x } }$ . The fixed value K  Xwill not affect the correction of constraint C1. Therefore, the energy budget in this study is prepared for edge computing but not flight control. And in the problem 1, the energy consumption for hovering is not considered.

## 4.2 Lyapunov Optimization-Based Approach

In each slot, the number of tasks arrived at UAVs is supposed to be random. Therefore, it is infeasible to know the exact number of tasks at the beginning of system operation. In this section, we transform the global optimization problem into an online optimization problem by Lyapunov optimization method. Then, convex approximation is utilized to make the non-convex online optimization problem tractable. The approximated problem can be handled by existing convex optimization tools.

1) Transformation to Online Problem: The Lyapunov optimization method can make a tradeoff between system delay and the energy consumption under the premise of unknown number of tasks generated in future time slots. Original problem can be transformed to Lyapunov optimization form as follow using the Lyapunov drift-plus-penalty technique [45]:

$$
\begin{array} { l } { { \displaystyle { \bf P } 2 : \operatorname* { m i n } _ { { \pmb { \pi } } } \sum _ { i = 1 } ^ { U } \{ V \cdot D _ { i } ( { \pmb { \pi } } [ t ] ) + q _ { i } [ t ] \cdot E _ { i } ( { \pmb { \pi } } [ t ] ) \} } } \\ { { \displaystyle s . t . ~ C 2 , C 3 , C 4 , } } \end{array}\tag{22}
$$

$\pmb q [ t ] = \{ q _ { i } [ t ] \} _ { i \in \mathcal { U } }$ are the virtual energy deficit queues, let $q _ { i } [ 0 ] = 0 , \forall i \in \mathcal { U } . q _ { i } [ t ]$ denotes the queue length in time slot $t ,$ Â½  Â¼ 8 2 U Â½ which evolves as follow:

$$
q _ { i } [ t ] = \operatorname* { m a x } \{ q _ { i } [ t - 1 ] + E _ { i } ( \pmb { \pi } [ t - 1 ] ) - \bar { E } _ { i } , 0 \} .\tag{23}
$$

Theorem 1. Consider $D _ { L } ^ { * }$ as the optimal value of problem P2, and $D ^ { * }$ as the optimal value of problem P1 with the global information, i.e., the theoretical lower bound. Then the gap between $D _ { L } ^ { * }$ and $D ^ { * }$ is $O ( \textstyle { \frac { 1 } { V } } )$ . And the time-average Ã° Ãlength of virtual energy deficit queues are $O ( V )$

Proof. See Appendix A, available online.

â¡

The theorem above shows that, as the parameter V increases, the optimal solution obtained by the Lyapunov optimization will get closer to the theoretical lower bound, yet the length of the energy deficit queue will increase accordingly, resulting in ascending energy consumption.

2) Convex Approximation: Discontinuity of the objective function still exists in problem P2, making it hard to solve using traditional algorithm like Newton Method. To make the problem tractable, the discontinuity part, i.e., max function, should be approximated to convex form.

Theorem 2. Given a large enough parameter $\eta ,$ computation delay $\mathrm { m a x } _ { j \in \mathcal { U } } \{ \frac { \pi _ { i j } } { f _ { j } } \}$ can be approximated to $\begin{array} { r } { \frac { 1 } { \eta } \mathrm { l g } ( \sum _ { j = 1 } ^ { U } e ^ { \eta \pi _ { i j / } f _ { j } } ) } \end{array}$ Proof. [46] shows that max function meets the inequality max $\begin{array} { r } { \{ x _ { 1 } , . . . , x _ { n } \} \leq \mathrm { l g } ( \sum _ { i = 1 } ^ { n } e ^ { x _ { i } } ) \leq \operatorname* { m a x } \{ x _ { 1 } , . . . , x _ { n } \} + \mathrm { l g } n , } \end{array}$ thus, through introducing parameter $\eta , \operatorname* { m a x } _ { j \in \mathcal { U } } \{ \frac { \pi _ { i j } } { f _ { j } } \}$ satisfies

$$
\begin{array} { r l } {  { \operatorname* { m a x } _ { j \in \mathcal { U } } \{ \frac { \pi _ { i j } } { f _ { j } } \} = \frac { 1 } { \eta } \operatorname* { m a x } _ { j \in \mathcal { U } } \{ \eta \frac { \pi _ { i j } } { f _ { j } } \} } } \\ & { \leq \frac { 1 } { \eta } \mathrm { l g } ( \sum _ { j = 1 } ^ { U } e ^ { \eta \pi _ { i j } / f _ { j } } ) } \\ & { \leq \operatorname* { m a x } _ { j \in \mathcal { U } } \{ \frac { \pi _ { i j } } { f _ { j } } \} + \frac { 1 } { \eta } \mathrm { l g } U . } \end{array}\tag{24}
$$

Consequently, $\begin{array} { r } { \operatorname* { l i m } _ { \eta  \infty } \frac { 1 } { \eta } \mathrm { l g } ( \sum _ { j = 1 } ^ { U } e ^ { \eta \pi _ { i j } / f _ { j } } ) = \operatorname* { m a x } _ { j \in \mathcal { U } } \{ \frac { \pi _ { i j } } { f _ { i } } \} } \end{array}$ h Â¼With being larger, degree of approximation will be better, hso we can define a parameter and convert the original hfunction to the form of log-sum-exp function, while the latter is convex.

Algorithm 1. LOC: Lyapunov-Based Online Cooperative   
Input: V;   
hOutput: Offloading decision   
1: pInitialize energy deficit queue $q _ { i } [ 0 ] = 0 , \forall i \in \mathcal { U }$   
2: for t 0 to T 1 do   
3: Â¼ Count the arrival rate of each UAV $\lambda _ { i } [ t ]$   
4: Solve P3 by SCS solver   
5: $q _ { i } [ t + 1 ] = \operatorname* { m a x } \{ q _ { i } [ t ] + E _ { i } ( \pmb { \pi } [ t ] ) - \bar { E } _ { i } , 0 \} , \forall i \in \mathcal { U }$   
Â½ Ã¾6: return

Now, we can transform problem P2 to convex optimization problem P3, which can be solved by optimization tools. Based on the above derivation, the Lyapunov optimizationbased Online Cooperative (LOC) task offloading algorithm is proposed. Before system running, the energy deficit queue of each UAV should be initialized. At each time slot, problem P3 is solved by SCS solver5 which calculates the optimal solution through ADMM approach, and then the energy deficit queue would be updated. The process should be repeated from one slot to another until the last. The algorithm is executed by the central controller of UAVs, who has a global view of each UAVâ s state at the beginning of each time slot.

$$
\begin{array} { l } { { \displaystyle { \bf P } 3 : \operatorname* { m i n } _ { \pi } \sum _ { i = 1 } ^ { U } [ V \cdot ( \frac { s \cdot l } { \eta } \mathrm { l g } ( \sum _ { j = 1 } ^ { U } e ^ { \eta \pi _ { i j } [ t ] / f _ { j } } ) + \pi _ { i 0 } [ t ] D _ { i } ^ { d } [ t ]   } } \\ { { \displaystyle   + D _ { i } ^ { L A N } [ t ] ) + q _ { i } [ t ] \cdot E _ { i } ( \pi [ t ] ) ] } } \\ { { \displaystyle \vphantom { \frac { 1 } { \eta ^ { L A N } } \sum _ { i = 1 } ^ { U } [ \eta \cdot ( \frac { s \cdot l } { \eta } \mathrm { l g } ( \sum _ { j = 1 } ^ { U } e ^ { \eta \pi _ { i j } [ t ] / f _ { j } } ) + \pi _ { i 0 } [ t ] D _ { i } ^ { d } [ t ]   } } } \\ { { \displaystyle   s . t . \ C 2 , C 3 , C 4 .  } } \end{array}\tag{25}
$$

<!-- image-->  
Fig. 5. UAV-enabled edge computing platform.

The choice of solver is not unique. Actually, all solvers that has the ability to solve the convex problem are suitble to LOC. We choose the SCS solver because it is free, efficient and flexible.

The key parameters in Eq. (7), i.e., $\gamma _ { 1 }$ and $\gamma _ { 2 } ,$ will be given g glater in Section 5.1.2. We have measured the congestionrelated parameters in our testbed. However, in practical scenarios, the parameters may need to be adjusted. Therefore, a method is also given later to guide how to obtain $\gamma _ { 1 } , \gamma _ { 2 }$ in practical scenarios.

## 5 PERFORMANCE EVALUATION

This section focuses on the performance evaluation. Section 5.1 introduces the construction of our UAV-EC experimental platform, and utilizes the practical platform to verify the correctness of the proposed model. After the model verification, Section 5.2 will implement simulation experiments based on real-world datasets, to explore the performance of LOC algorithm from different perspectives.

## 5.1 Model Verification Through a UAV-EC Platform 5.1.1 UAV-Enabled Edge Computing Platform

A UAV-enabled edge computing platform is presented as Fig. 5. Using Pixhawk46 as the flight control unit, a rotary-wing UAV is assembled. The edge computing unit which undertake the obligation of computation is Jetson Nano.7 Jetson Nano is a computer with a GPU produced by Nvidia and the GPU makes it be able to perform deep learning inference tasks as a lightweight, lowpower edge computing node. T2088 is used to guarantee the power supply of Jetson Nano. MorningCoreâs dedicated UAV star network transmission module9 is chosen to exchange data among the UAVs. After selecting the appropriate motor (AXI 4120 brushless motor), the UAV edge node is able to fly smoothly and hover stably as a powerful computation unit. The components selected have been widely used in existing UAV systems. For example, Pixhawk is the hardware standard for opensource autopilots and it is the worldâs most popular open source flight controllers available, and Jetson has been used to deploy a wide range of popular DNN models and ML frameworks to the edge with high performance inferencing.10 MorningCoreâs module is also an industrial product which has a certain market share in China.

<!-- image-->  
Fig. 6. Jetson Nano simulating a UAV swarm.

Due to the field area restriction and the safety regulations, we cannot assemble too many UAVs and fly them in a wide space for testing. Therefore, we measure the achievable data rate between two UAV edge nodes, then use several Jetson Nanos at the ground to simulate the UAVs on the air (Fig. 6). Two UAV-enabled edge nodes were constructed and the achievable rate between them is measured using $\mathrm { i p e r f } ^ { 1 1 }$ tool when they are flying. Then, using $\mathrm { t c } ^ { 1 2 }$ provided by Linux, the maximum data rate among Jetson Nanos at the ground is restricted to imitate the situation in the air. We performed the measurements between two UAVs in an open environment, as Fig. 7 shows (marked with Google Maps). Then, we repeated the measurements for 10 times, and the average results is recorded in Fig. 8. It can be observed that, the achievable rate is always higher than 15 Mbps when the distance is smaller than 400 meters. Thus, to simulate the worst wireless communication condition literally in the fly, the average data rate among Jetson Nanos at the ground is restricted to 15 Mbps. Then the nodes are able to simulate a UAV-enabled edge computing cluster.

Apart from that, we have utilized the UAV-EC platform to measure an air-to-ground channel. The measured results are leveraged to imitate the practical UAV-to-BS c

hannel. Keeping a UAV-EC platform at the height of 20 meters, we enable the communication between it and the equipment on the ground. Setting the transmission power as 0.2 W, the achievable rate between UAV and the ground equipment is measured, and the results are recorded in Fig. 9. Then, we explore the consistency between measured rate and our model, i.e., Eq. (12). Fitting the parameters, we found that our model is conform to the reality when a 2:05983; b Â¼ Â¼0:44375. We measured the air-to-ground channel in campus environment, whose rate should be between urban and suburban, and the results are in line with the theoretical expectation.

It is worth mentioning that, MorningCoreâs modules on the UAVs request the topology of the network to be the shape of star, i.e., there is a hotspot among them to organize a Local Area Network (LAN). Meanwhile, in the ground system shown in Fig. 6, the devices are connected within a LAN and there is also a hotspot to make the systemâs topology as star shape. Thereby, the topology of the ground Jetson

<!-- image-->  
Fig. 7. Environment for measurement.

<!-- image-->  
Fig. 8. Achievable rate between two UAVs.

<!-- image-->  
Fig. 9. Air-to-ground Achievable rate.

Nanosâ system is keep unchanged compared with the UAVs in the air. The hotspot becomes the bottleneck of UAV-to-UAV transmission when large amount of data is offloaded. Network congestion occurs due to the bottleneck [47].

## 5.1.2 Verification for UAV-to-UAV Transmission Model

The verification experiment is designed as Fig. 10. UAV 0 is the hotspot, UAV 1 sends data to UAV 2 through the hotspot with the data amount changing from 500 KBytes to 15 MBytes. Meanwhile, there is an another node (i.e., UAV 4) sending data to all nodes except itself. The amount of data sent to other nodes by UAV 4 are the same as the amount sent by UAV 1. Thus, UAV 1 and UAV 4 compete the network resource in the star-shape network with UAV 1 as the bottleneck. According to Section 5.1.1, the average data rate of each UAV is restricted to 15 Mbps. The transmission delay of UAV 1 was measured to observe the most suitable congestion model of the UAV cluster.

<!-- image-->  
Fig. 10. Experiment designed to verify the proposed UAV-to-UAV model.

<!-- image-->  
Fig. 11. Different models comparing with measured result.

Measurement results are recorded in Fig. 11. Measured values are the transmission delay for offloading UAV 1âs data under the congestion. Traffic amount means the amount of data sent by UAV 1, according to the $\beta _ { i } [ t ] \cdot s$ item in Equab Â½  tion (7). The amount has the range from 500 KBytes to 15 MBytes. Fitting the Equation (7) through least squares method, it can be observed that the proposed model is much more related to the measured results than linear model and M/M/1 model. In other words, the proposed $\mathrm { U A V  â t o â U A V }$ transmission model is more relevant to the reality. $\gamma _ { 1 }$ and $\gamma _ { 2 }$ are calculated as $4 . 2 1 9 8 9 7 6 \times 1 0 ^ { - 9 }$ g gand 1.022729, respectively.

Two key prerequisites are met in real world multi-UAV system: (i) there is a hotspot as bottleneck within the cluster, and (ii) there is a central controller to control the entire system. The central controller is able to trigger the bandwidth probe, and the hotspot is definitely the cause of congestion. Thus, if $\gamma _ { 1 }$ and $\gamma _ { 2 }$ are tended to be modified according to g gthe practical scenarios, the framework for the verification experiment is suitable. An algorithm is provided for reference in appendix B, available in the online supplemental material. The algorithm refers to BBR algorithm [47], and could be used to obtain $\gamma _ { 1 }$ and $\gamma _ { 2 }$ in practical scenarios.

## 5.1.3 Verification for Computation Model

$\mathrm { D o c k e r } ^ { 1 3 }$ has been deployed in the test platform as the containerization technology to observe whether the computation delay model fits the practical application. In this subsection, we select object detection as the computation tasks among the UAVs. Object detection is a typical task for UAV in reconnaissance, search, rescue or other missions. YOLOX [48] is a novel object detection algorithm which has the ability to achieve accurate detection results. In our work, YOLOX is packaged as docker image and each node (i.e., Jetson Nano) has the image. During the system initialization, the container will be constructed through the image to execute the object detection. Five frames of a video with the size of 1280x720 are sent to the nodes concurrently, and each picture accords to one node. Once a node finishes its job, the coordinate of the object detected will be send back in form of text for integration. Thus, the amount of task data transmitted by the initiator (i.e., the node generate the tasks) is far more than the computation result received. In order to make the verification results more convincing, GPU in each node has been disabled and the available CPUs for the task of 5 nodes are restricted to 0:2; 0:5; 0:5; 0:8; 1:0 cores by cgroups14 tool (The maxif gmum value of available CPU is 4.0 because there are four cores in the Jetson Nanoâs processor). The achievable rate among nodes is set to 15 Mbps to simulate the worst communication condition according to Section 5.1.1.

The timestamp of each node is recorded in Table 2. Start time in the table means the node started to execute the task at that time. Once the task data has been received completely, the node begins the computation. The Start time column shows the starting point of several containers is nearly the same, which fits our assumption mentioned in Section 3.

Finish time means the time when the task had been accomplished. At that time, the detection result was sent back. The initiator needs all computation results to integrate, so the computation delay depends on the slowest node. In this case, the slowest node is Node 1, who has only 20% CPU available. In Table 2, under the condition of the nearly same starting point, tasksâ finishing point is the finish time of Node 1, which is in agreement with the max item in Equation (13).

Time cost is the difference between Start time and Finish time. From the Time cost column, it can be observed that task execution delay is approximately inversely proportional to the CPU frequency, fitting the $s \cdot l / f _ { j }$ item in Equation (13). To make the results for Time cost more convincing, 20 more measurements have been done, and the average time cost for all nodes are recorded in Table 3. The average measurement results still fit the Equation (13). In conclusion, the test of the real computation task on practical platform, indicates that our computation delay model (16) is consistent with reality.

## 5.2 Data-Driven Simulation Experiments

Section 5.1 has verified that the mathematical model is relevant to reality. Thereby, the proposed algorithm based on the model can be easily applied to real-world scenarios. However, several factors result in the difficulty for the algorithmâs practical performance test. The factors involve experiment field restriction and safety regulations. Thus, in this section, simulation experiments would be carried out to evaluate the performance of proposed algorithm in multi-UAV enabled edge-cloud systems. The proposed algorithm is compared with several strategies in terms of system delay and energy consumption. To make the simulation as realistic as possible, two real-world datasets have been adopted to imitate the real-world tasksâ generation.

TABLE 2  
Computation Delay of the Edge Cluster Platform
<table><tr><td>Node</td><td>Available CPU(%)</td><td>Start time</td><td>Finish time</td><td>Time cost</td></tr><tr><td>1</td><td>20%</td><td>07:50:43.32</td><td>07:53:24.92</td><td>161.60 s</td></tr><tr><td>2</td><td>50%</td><td>07:50:42.12</td><td>07.51:40.97</td><td>58.85 s</td></tr><tr><td>3</td><td>50%</td><td>07:50:43.10</td><td>07:51:43.33</td><td>60.23 s</td></tr><tr><td>4</td><td>80%</td><td>07:50:42.03</td><td>07:51:21.82</td><td>39.79 s</td></tr><tr><td>5</td><td>100%</td><td>07:50:43.33</td><td>07:51:17.92</td><td>34.59 s</td></tr></table>

## 5.2.1 Dataset Description

The two real-world datasets [49] has been frequently adopted by cluster computing system researches for the workloads analysis [50], [51]. The datasets report network traffic data (in bits) time series from two different ISPs, denoted as A and B. The essence of the computation tasks offloaded by UAVs is network traffic. Actually, all the data ISP received can be considered as tasks to be executed because the data is the trigger of the tasks. The size of network traffic can be considered as s times than the number of tasks. Thus, we use the ISPâs traffic time series to imitate the tasks generated/received by UAVs at all time slots and scale down the value to a reasonable order of magnitude. The dataset A belongs to a private ISP with centres in 11 European cities. The data was collected from 06:57 hours on 7 June to 11:17 hours on 29 July 2005. Dataset B comes from UKERNA (United Kingdom education and research networking association) and represents aggregated traffic in the United Kingdom academic network backbone. It was collected between 19 November 2004, at 9:30 hours and 27 January 2005, at 11:11 hours. Both the datasets were collected by SNMP scripts and were recorded every 5 minutes.

## 5.2.2 Experiment Setup

Assume that the whole system is deployed in a 1000m 1000 m area and the BS locates at ${ \bf a } _ { B S } = ( 0 , 0 )$ . The number Â¼ Ã° Ãof UAVs was drawn from a random sampling, which followed Poisson distribution with parameter - 10 and the sampling result is 9. The horizontal positions of UAVs are randomly drawn from the area following uniform distribution. Once sampled from the uniform distribution, UAVsâ positions keep still through all time slots. The height of UAVs is fixed as 50 m. The whole time slice is split to 50 slots and the length of each slot is 3 minutes. Nine subsequences of length 50 are randomly drawn (following uniform distribution) from dataset A and $\scriptstyle \mathrm { \mathrm { B } , }$ to describe the tasks generated by the UAVs. The maximum value of the subsequences is scaled down to 20, i.e., each UAV will generate up to 20 tasks from per slot. To avoid the uncertainty of the experiment result, simulation experiment will be repeated 1,000 times. And the mean values of the 1,000 experiments are reported.

TABLE 3  
Average Time Cost From Multiple Measurements
<table><tr><td>Node</td><td>Available CPU(%)</td><td>Time cost</td></tr><tr><td>1</td><td>20%</td><td>158.36 s</td></tr><tr><td>2</td><td>50%</td><td>62.77 s</td></tr><tr><td>3</td><td>50%</td><td>63.12 s</td></tr><tr><td>4</td><td>80%</td><td>38.64 s</td></tr><tr><td>5</td><td>100%</td><td>31.85 s</td></tr></table>

<!-- image-->  
Fig. 12. System cumulative delay under different strategies.

Assume the CPU carried by each UAV has 4 cores, and the CPU frequency $f _ { i }$ is taken from 0; 5 GHz randomly from uni-Â½ form distribution. The available energy each UAV has is $9 \times$ $1 0 ^ { 4 } \ \mathrm { J } ,$ , i.e., the average power is 10 W which is a typical supply power of an onboard edge node [52]. Then $\bar { E } _ { i }$ can be calculated as $\bar { E } _ { i } = \frac { 9 * 1 0 ^ { 4 } } { 5 0 } = 1 8 0 0$ J.  30 J/per task, i.e., transmitting a Â¼ Â¼ Â¼task to the BS will consume 30 J energy. The same task will cost $\omega = 1 0$ J when transmitting it to other UAV. Delay caused by v Â¼long-distance wired communication is $D _ { B S } = 2 0 0$ ms. Here, Â¼we consider the face recognition application in [53], where the computation task has 3000; 500 with the units of Megacycles and ${ \mathrm { K B } } , { \mathrm { i . e . } } , s = 0 . 5$ Ã° Ã MB. Energy consumption for one bit computation is $\kappa = 1 0 ^ { - 2 5 } \mathrm { { J / b i t } }$ . Parameters to describe the air-tok Â¼ground channel are set as: $g _ { u } = - 6 0$ dB; B 1 MHz; $P _ { i } =$ 0.1 W; $\sigma ^ { 2 } = - 1 1 0$ dBm; $\Gamma = 7$ dB [41].

s Â¼ Â¼The performance of LOC algorithm is compared with four benchmarks: 1) Non-cooperative Computing (NcC): UAV in the system would execute all tasks locally. 2) Cloud offloading Computing (CoC): All tasks would be forwarded to the remote cloud. 3) Random offloading Computing (RoC): Each UAV choose random part of tasks to offload to a random device. 4) Delay Lower Bound (DLB): Infinite energy consumption is allowed to achieve the system delay lower bound. The difference from LOC is that it ignores the energy queue in each time slot, reflecting the upper bound of the systemâs computation capability for scheduling. The simulation experiments are implemented in Python 3.9 and performed on a laptop with AMD Ryzen 7 4800 U CPU and 16 GB RAM.

<!-- image-->  
Fig. 13. System remaining energy under different strategies.

## 5.2.3 Numerical Results

First, setting $V = 1 0 ^ { 7 } , \ \eta = 1 0 ^ { 5 }$ and terrain environment as urban $( \mathrm { i . e . , ~ \ } a = 9 . 6 1 , b = 0 . 1 5$ in the Equation (13)), we Â¼ Â¼explore the performance on system delay and energy consumption of proposed algorithm in Figs. 12 and 13, respectively. Cumulative delay is the service delay cumulated from previous time slots of all UAVs. Define cumulative delay as $D _ { c u m }$ and service delay of each slot as $D _ { s e r v } ,$ then $D _ { c u m } [ t ] =$ $D _ { s e r v } [ 0 ] + \cdot \cdot \cdot + D _ { s e r v } [ t - 1 ] + D _ { s e r v } [ t ]$ Â½  Â¼. Remaining energy is the Â½  Ã¾    Ã¾ Â½   Ã¾ Â½ energy available for future computation or transmission, i.e., Remaining energy = Energy budget - Consumed energy. It is worth mentioning that, the energy budget means the energy can be used for computation and transmission but not for hovering or flying. When the energy consumed equals the budget, offloading and computation will not be allowed but UAVs will still have enough energy to fly back.

âDDLâ in Fig. 12 means the cumulative completion deadline of each slot. The length of each slot is 3 minutes, so the ith slotâs cumulative deadline is $i \times 3 \times 6 0$ seconds. When a strategyâs cumulative delay is above the $' \mathrm { D D L } , ^ { \prime \prime }$ it is indicated that the strategy would time out. In Fig. 12, LOC achieves the minimum cumulative delay compared to other strategies except DLB. But in Fig. 13, remaining energy attracts an attention that DLB causes mission terminated prematurely due to insufficient energy (The delay of DLB after energy exhaustion is still presented in Fig. 12 to reflect the difference more intuitively). Other three strategies leave lots of energy unused. As mentioned in Section 2, UAVs will terminate the mission after T slots. Thus, saving energy is unnecessary for the system because energy for flying has been reserved in advance. A better algorithm should fully utilize the available energy to reduce the delay. From Figs. 12 and 13, it is obvious that only LOC has the ability to realize it. Compared to non-cooperative task execution (i.e., NcC), the proposed algorithm can significantly reduce the system delay by 41.7% according to the Fig. 12.

Accordingly, adjusting the length of a slot from 2.5 tminutes to 4.0 minutes, the success rate for real-time task completion is reported in Fig. 14. We define the success rate as the ratio of tasks accomplished in the current time slot. $\operatorname { A s } \operatorname { F i g } .$ 14 shows, when is large, the success rates of LOC,

<!-- image-->  
Fig. 14. Success rate under different .

<!-- image-->  
Fig. 15. Load occupancy rate of NcC.

<!-- image-->  
Fig. 16. Load occupancy rate of LOC.

CoC and NcC are high. However, when decreases, i.e., the treal-time requirement is more strict, only LOC has the ability to maintain a high success rate. Therefore, LOC has the ability to cope with more stringent real-time requirements. And the objective that minimizes system delay is effective for elevating the success rate. When deploying on the practical scenarios, LOC will process the complicated data in real time with higher probability.

Next, the computation load management ability of LOC can be observed from Figs. 15 and 16. We select one of the 1,000 experimentsâ results randomly, and enumerate the load of all UAVs in all time slots. Load occupancy rate is the ratio calculated by Number of tasks to be computed locallyf = s l , which means how Ã°  Ãmuch CPU resources have been occupied. In Fig. 15, the rates sometimes exceed 1, which indicates the UAVs endured tasks beyond their capability. Then, the UAVs will be unable to accomplish the tasks in the current slot. In other words, executing all the tasks locally will not satisfy the real-time requirements. But in Fig. 16, the rate is always below 1 which means LOC can make an adjustment to avoid overloading situation happening. Therefore, it is necessary to utilize the LOC algorithm rather than execute the computation locally to assure that the tasks can be accomplished in time.

Then, whether LOC has the ability to adapt different terrain environment is investigated. Three environments (suburban, dense urban and Highrise urban) are tested by adjusting a and b of Equation (13). As Fig. 17 depicts, comparing to the CoC, whose efficiency depends on the air-to-ground channel critically, drastic changes have not happened on LOC.

<!-- image-->  
Fig. 17. Adaptability to different environments.

<!-- image-->  
Fig. 18. Impact of parameter V .

<!-- image-->  
Fig. 19. System delay under increasing number of tasks.

In other words, though the terrain environment changes, LOC can still achieve stable performance in terms of system delay. The results illustrate that LOC has strong adaptability to the environment. LOC will allocate system resources rationally according to the communication condition to maintain stable system delay.

After that, the role of parameter V has also been explored in Fig. 18. Adjusting V from $1 0 ^ { 4 }$ to $1 0 ^ { 9 }$ , the system delay reduced remarkably while energy consumption has an observable increment. The phenomenon is consistent with Theorem 1 (Section 4.2). As V becomes larger, the system on July 16,2024 at 03:14:22 UTC from IEEE Xplore. Restrictions apply.

<!-- image-->  
Fig. 20. The proportion of cloud offloading delay in system delay.

delay of LOC is more approximate to the theoretical lower bound. But the energy consumption is also proportional to V . Therefore, V is the key to achieve the trade-off between delay and energy consumption. When deploying the algorithm in a practical scenario, parameter V should be well designed to adapt the requirement for delay and energy consumption.

Apart from task management capability, whether LOC is able to cope with greater computational pressure has also been studied. Selecting time series of length 50 randomly from dataset A and B, the maximum value of the series is set to 20; 30; 40; 50; 60 to realize more tasks for computaf gtion. Fig. 19 indicates that with the greater computational pressure, LOC can still achieve better performance than NcC and CoC. The results imply that LOC has the ability to cope with heavy missionâs stress. Higher number of tasks results in more computation than multi-UAV system capability. Therefore, more tasks have to be offloaded to the cloud, corresponding to the Fig. 20. The Cloud offloading delay term in Fig. 20 means the delay caused by offloading to the cloud in LOCâs decision. However, delay caused by offloading to the cloud does not become the main ingredient of the system delay, which means that LOC still attempts to fully utilize the computation capability of the multi-UAV system for delay minimization.

Finally, the efficiency of the algorithm has been investigated. In all the experiments mentioned above, the execution time required for making a cooperative offloading decision in each slot is counted. Statistics are recorded in Table 4, involving the minimum, first quartile, median, third quartile, maximum and average value for executing LOC. It can be observed that executing LOC requires 167:7 231:2ms with the average time 198 ms. The LOC algorithm was executed by single CPU core, and the execution delay is small enough to be negligible compared to the time slot length 3 minutes. 3 minutes is a typical value of task offloading period in edge computing scenarios [35]. Actually, the execution time can be reduced remarkably through some acceleration schemes, e.g., C++ implementation, etc. Furthermore, LOC utilizes one CPU core for an extremely small time slice while the computation tasks are more likely to dominate all cores and all time slices. In other words, rare resource competition between LOC and the actual computation tasks happens in the real world. Thus, executing LOC will not restrict the system performance. Apart from that, additional experiment has been done. As Fig. 21 illustrates, expanding the scale of the UAV cluster, the execution delay of LOC does not exceed 1% of single time slot duration.

TABLE 4  
Execution Delay of LOC
<table><tr><td>min</td><td>25%</td><td>median</td><td>75%</td><td>max</td><td>avg</td></tr><tr><td>167.7 ms</td><td>185.3 ms</td><td>193.6 ms</td><td>207.0 ms</td><td>231.2 ms</td><td>198.0 ms</td></tr></table>

<!-- image-->  
Fig. 21. Execution delay for LOC.

In summary, the LOC algorithm is able to make a better trade-off between delay and energy consumption. System delay can be reduced significantly to satisfy the real-time requirements under the energy budget. In addition, LOC has the ability to adjust the workload to avoid the overload of each node, and scenariosâ diversity will not restrict its performance. When facing greater computational pressure, LOC still achieves better performance. Its computational efficiency allows LOC to be deployed in real-world multi-UAV edge-cloud systems.

## 6 CONCLUSION

This paper has investigated the delay-aware cooperative task offloading problem for the multi-UAV enabled edgecloud computing system. Specifically, network congestion in UAV-to-UAV communications and the complicated airto-ground channel are considered to construct the transmission delay model. The feature of parallel computing in distributed system is considered to model the computation delay. Furthermore, the delay-optimal cooperative task offloading problem is formulated and a sub-optimal algorithm is proposed accordingly. Based on Lyapunov optimization and convex approximation, the proposed algorithm has the ability to solve the problem efficiently within limited energy budget. To validate the accuracy of the model, a practical UAV-enabled edge computing platform is constructed. Measurements performed on the platform verify that the model is consistent with reality. Data-driven simulation experiments prove that the proposed algorithm can fully utilize available system energy to satisfy the real-time requirements. The performance of the algorithm is stable when facing different environments and greater computation pressure. Future efforts are worthy doing to investigate the flight trajectory optimization algorithm to coordinate 1onJuly16224at03:14:22UTCfromIEEEXplore.Restrictionsapply.

with LOC. Besides, deploying the proposed algorithm in real world thoroughly is also on the agenda.

## REFERENCES

[1] G. Zhang, Q. Wu, M. Cui, and R. Zhang, âSecuring UAV communications via joint trajectory and power control,â IEEE Trans. Wireless Commun., vol. 18, no. 2, pp. 1376â1389, Feb. 2019.

[2] F. Zhou, Y. Wu, R. Q. Hu, and Y. Qian, âComputation rate maximization in UAV-enabled wireless-powered mobile-edge computing systems,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1927â1941, Sep. 2018.

[3] Q. Hu, Y. Cai, G. Yu, Z. Qin, M. Zhao, and G. Y. Li, âJoint offloading and trajectory design for UAV-enabled mobile edge computing systems,â IEEE Internet of Things J., vol. 6, no. 2, pp. 1879â1892, Apr. 2019.

[4] K. R. Lakhani and M. Creaner, âConnected drones: A new perspective on the digital economy,â 2017. [Online]. Available: https:// www.huawei.com/en/technology-insights/industry-insights/ outlook/mobile-broadband/xlabs/insights-whitepapers/ connected-drones-a-new-perspective-on-the-digital-economy

[5] W. Ma, X. Liu, and L. Mashayekhy, âA strategic game for task offloading among capacitated UAV-mounted cloudlets,â in Proc. IEEE Int. Congr. Internet Things, 2019, pp. 61â68.

[6] S. Hosseinalipour, A. Rahmati, and H. Dai, âInterference avoidance position planning in dual-hop and multi-hop UAV relay networks,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7033â7048, Nov. 2020.

[7] I. Valiulahi and C. Masouros, âMulti-UAV deployment for throughput maximization in the presence of co-channel interference,â IEEE Internet Things J., vol. 8, no. 5, pp. 3605â3618, Mar. 2021.

[8] Y. Zhou et al., âSecure communications for UAV-enabled mobile edge computing systems,â IEEE Trans. Commun., vol. 68, no. 1, pp. 376â388, Jan. 2020.

[9] M. Li, N. Cheng, J. Gao, Y. Wang, L. Zhao, and X. Shen, âEnergyefficient UAV-assisted mobile edge computing: Resource allocation and trajectory optimization,â IEEE Trans. Veh. Technol., vol. 69, no. 3, pp. 3424â3438, Mar. 2020.

[10] Z. Xu, W. Liang, M. Jia, M. Huang, and G. Mao, âTask offloading with network function requirements in a mobile edge-cloud network,â IEEE Trans. Mobile Comput., vol. 18, no. 11, pp. 2672â2685, Nov. 2019.

[11] G. Qu, H. Wu, R. Li, and P. Jiao, âDMRO: A deep meta reinforcement learning-based task offloading framework for edge-cloud computing,â IEEE Trans. Netw. Service Manag., vol. 18, no. 3, pp. 3448â3459, Sep. 2021.

[12] Z. M. Fadlullah, D. Takaishi, H. Nishiyama, N. Kato, and R. Miura, âA dynamic trajectory control algorithm for improving the communication throughput and delay in UAV-aided networks,â IEEE Netw., vol. 30, no. 1, pp. 100â105, Jan./Feb. 2016.

[13] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and L. Hanzo, âMultiagent deep reinforcement learning-based trajectory planning for multi-UAV assisted mobile edge computing,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 1, pp. 73â84, Mar. 2021.

[14] Y. Wang, Z.-Y. Ru, K. Wang, and P.-Q. Huang, âJoint deployment and task scheduling optimization for large-scale mobile users in multi-UAV-enabled mobile edge computing,â IEEE Trans. Cybern., vol. 50, no. 9, pp. 3984â3997, Sep. 2020.

[15] L. Yang, H. Yao, J. Wang, C. Jiang, A. Benslimane, and Y. Liu, âMulti-UAV-enabled load-balance mobile-edge computing for IoT networks,â IEEE Internet of Things J., vol. 7, no. 8, pp. 6898â6908, Aug. 2020.

[16] B. Chen, H. Zhou, J. Yao, and H. Guan, âRESERVE: An energyefficient edge cloud architecture for intelligent multi-UAV,â IEEE Trans. Serv. Comput., vol. 15, no. 2, pp. 819â832, Mar./Apr. 2022.

[17] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âCellularconnected multi-UAV MEC networks: An online stochastic optimization approach,â IEEE Trans. Commun., vol. 70, no. 10, pp. 6630â6647, Oct. 2022.

[18] J. Almutairi, M. Aldossary, H. A. Alharbi, B. A. Yosuf, and J. M. H. Elmirghani, âDelay-optimal task offloading for UAV-enabled edgecloud computing systems,â IEEE Access, vol. 10, pp. 51575â51586, May 2022.

[19] C. Ashraf, âVerizon 5G ultra wideband and edge compute enable smart drones to navigate weather,â 2022. [Online]. Available: https://www.verizon.com/about/news/verizon-5g-smartdrones-navigate-weather

[20] T. Zhang, Y. Xu, J. Loo, D. Yang, and L. Xiao, âJoint computation and communication design for UAV-assisted mobile edge computing in IoT,â IEEE Trans. Ind. Inform., vol. 16, no. 8, pp. 5505â5516, Aug. 2020.

[21] S. Jeong, O. Simeone, and J. Kang, âMobile edge computing via a UAV-mounted cloudlet: Optimization of bit allocation and path planning,â IEEE Trans. Veh. Technol., vol. 67, no. 3, pp. 2049â2063, Mar. 2018.

[22] L. Zhang and N. Ansari, âOptimizing the operation cost for UAVaided mobile edge computing,â IEEE Trans. Veh. Technol., vol. 70, no. 6, pp. 6085â6093, Jun. 2021.

[23] M. Aazam, S. Zeadally, and K. A. Harras, âFog computing architecture, evaluation, and future research directions,â IEEE Commun. Mag., vol. 56, no. 5, pp. 46â52, May 2018.

[24] F. Luo, C. Jiang, S. Yu, J. Wang, Y. Li, and Y. Ren, âStability of cloud-based UAV systems supporting Big Data acquisition and processing,â IEEE Trans. Cloud Comput., vol. 7, no. 3, pp. 866â877, Third Quarter 2019.

[25] H.-P. Shiang and M. van der Schaar, âOnline learning in autonomic multi-hop wireless networks for transmitting mission-critical applications,â IEEE J. Sel. Areas Commun., vol. 28, no. 5, pp. 728â741, Jun. 2010.

[26] B. Liu, W. Zhang, W. Chen, H. Huang, and S. Guo, âOnline computation offloading and traffic routing for UAV swarms in edgecloud computing,â IEEE Trans. Veh. Technol., vol. 69, no. 8, pp. 8777â8791, Aug. 2020.

[27] R. Duan, J. Wang, C. Jiang, Y. Ren, and L. Hanzo, âThe transmitenergy vs computation-delay trade-off in gateway-selection for heterogenous cloud aided multi-UAV systems,â IEEE Trans. Commun., vol. 67, no. 4, pp. 3026â3039, Apr. 2019.

[28] N. Toorchi, F. Hu, S. Pudlewski, E. Bentley, and S. Kumar, âVolcano routing: A multi-pipe high-throughput routing protocol with hole avoidance for multi-beam directional mesh networks,â IEEE Trans. Mobile Comput., vol. 19, no. 12, pp. 2981â2996, Dec. 2020.

[29] O. Esrafilian, R. Gangula, and D. Gesbert, âAutonomous UAVaided mesh wireless networks,â in Proc. IEEE Conf. Comput. Commun. Workshops, 2020, pp. 634â640.

[30] A. Koub^aa, A. Allouch, M. Alajlan, Y. Javed, A. Belghith, and M. Khalgui, âMicro air vehicle link (MAVLink) in a nutshell: A survey,â IEEE Access, vol. 7, pp. 87658â87680, 2019.

[31] Q. Luo, C. Li, T. Luan, and W. Shi, âMinimizing the delay and cost of computation offloading for vehicular edge computing,â IEEE Trans. Serv. Comput., vol. 15, no. 5, pp. 2897â2909, Sep./Oct. 2022.

[32] X. He, R. Jin, and H. Dai, âMulti-hop task offloading with on-thefly computation for multi-UAV remote edge computing,â IEEE Trans. Commun., vol. 70, no. 2, pp. 1332â1344, Feb. 2022.

[33] Y. Zhuang et al., âData collection with accuracy-aware congestion control in sensor networks,â IEEE Trans. Mobile Comput., vol. 18, no. 5, pp. 1068â1082, May 2019.

[34] S. K. Kaul and R. D. Yates, âTimely updates by multiple sources: The M/M/1 queue revisited,â in Proc. 54th Annu. Conf. Inf. Sci. Syst., 2020, pp. 1â6.

[35] L. Chen, S. Zhou, and J. Xu, âComputation peer offloading for energy-constrained mobile edge computing in small-cell networks,â IEEE/ACM Trans. Netw., vol. 26, no. 4, pp. 1619â1632, Aug. 2018.

[36] S. Wang, X. Zhang, Z. Yan, and W. Wenbo, âCooperative edge computing with sleep control under nonuniform traffic in mobile edge networks,â IEEE Internet of Things J., vol. 6, no. 3, pp. 4295â4306, Jun. 2019.

[37] Google, âgRPC,â 2018. [Online]. Available: https://grpc.io/

[38] R. A. Light, âMosquitto: Server and client implementation of the MQTT protocol,â J. Open Source Softw., vol. 2, no. 13, 2017, Art. no. 265.

[39] J. Yang, Z. Shan, and Z. Chen, âResearch and practice of swoole asynchronous multithreading design method,â in Proc. 4th IEEE Int. Conf. Comput. Commun., 2018, pp. 2163â2169.

[40] Z. Yang, C. Pan, K. Wang, and M. Shikh-Bahaei, âEnergy efficient resource allocation in UAV-enabled mobile edge computing networks,â IEEE Trans. Wireless Commun., vol. 18, no. 9, pp. 4576â4589, Sep. 2019.

[41] C. Zhan, Y. Zeng, and R. Zhang, âEnergy-efficient data collection in UAV enabled wireless sensor network,â IEEE Wireless Commun. Lett., vol. 7, no. 3, pp. 328â331, Jun. 2018.

[42] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[43] Y. S. Meng, Y. H. Lee, and B. C. Ng, âEmpirical near ground path loss modeling in a forest at VHF and UHF bands,â IEEE Trans. Antennas Propag., vol. 57, no. 5, pp. 1461â1468, May 2009.

[44] R. Dua, A. R. Raja, and D. Kakadia, âVirtualization versus containerization to support PaaS,â in Proc. IEEE Int. Conf. Cloud Eng., 2014, pp. 610â614.

[45] D. Zhang et al., âNear-optimal and truthful online auction for computation offloading in green edge-computing systems,â IEEE Trans. Mobile Comput., vol. 19, no. 4, pp. 880â893, Apr. 2020.

[46] S. Boyd, S. P. Boyd, and L. Vandenberghe, Convex Optimization. Cambridge, U.K.: Cambridge Univ. Press, 2004.

[47] N. Cardwell, Y. Cheng, C. S. Gunn, S. H. Yeganeh, and V. Jacobson, âBBR: Congestion-based congestion control: Measuring bottleneck bandwidth and round-trip propagation time,â Queue, vol. 15, no. 5, pp. 20â53, Dec. 2016. [Online]. Available: https:// queue.acm.org/detail.cfm?id 3022184

Â¼[48] Z. Ge, S. Liu, F. Wang, Z. Li, and J. Sun, âYOLOX: Exceeding YOLO series in 2021,â Aug. 2021, arXiv:2107.08430.

[49] P. Cortez, M. Rio, M. Rocha, and P. Sousa, âMulti-scale internet traffic forecasting using neural networks and time series methods,â Expert Syst., vol. 29, no. 2, pp. 143â155, 2012.

[50] K. Cetinski and M. B. Juric, âAME-WPC: Advanced model for efficient workload prediction in the cloud,â J. Netw. Comput. Appl., vol. 55, pp. 191â201, Sep. 2015.

[51] J. Xue, F. Yan, A. Riska, and E. Smirni, âScheduling data analytics work with performance guarantees: Queuing and machine learning models in synergy,â Cluster Comput., vol. 19, no. 2, pp. 849â864, Apr. 2016.

[52] F. Kaup, P. Gottschling, and D. Hausheer, âPowerPi: Measuring and modeling the power consumption of the raspberry Pi,â in Proc. 39th Annu. IEEE Conf. Local Comput. Netw., 2014, pp. 236â243.

[53] T. Soyata, R. Muraleedharan, C. Funai, M. Kwon, and W. Heinzelman, âCloud-vision: Real-time face recognition using a mobilecloudlet-cloud acceleration architecture,â in Proc. IEEE Symp. Comput. Commun., 2012, pp. 59â66.

<!-- image-->  
Zhuoyi Bai received the BE degree in electronic information and communications from the Huazhong University of Science and Technology, Wuhan, China, in 2020. He is currently working toward the MS degree with the School of Electronic Information and Communications, Huazhong University of Science and Technology, Wuhan. His current research interests include edge/distributed computing and the real-time video transmission.

<!-- image-->

Yifan Lin received the BE degree in electronic information and communications from the Huazhong University of Science and Technology, Wuhan, China, in 2021. He is currently working toward the MS degree with the School of Electronic Information and Communications, Huazhong University of Science and Technology, Wuhan. His current research interests include edge computing and the Internet of Things.

<!-- image-->

Yang Cao (Member, IEEE) is currently an associate professor with the School of Electronic Information and Communications, Huazhong University of Science and Technology, Wuhan, China. From 2011 to 2013, he was with the School of Electrical, Computer, and Energy Engineering, Arizona State University, Tempe, Arizona, as a visiting scholar. His research interests include video transmission and edge/ distributed computing. He has coauthored 50 papers on refereed IEEE journals and conferences. He was awarded CHINACOM Best Paper Award, in 2010 and awarded Microsoft Research Fellowship, in 2011.

<!-- image-->

Wei Wang (Senior Member, IEEE) received the PhD degree from the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology. He is currently a professor with the School of Electronic Information and Communications, Huazhong University of Science and Technology. His research interests include PHY/MAC design and mobile computing in wireless systems. He served on TPC of INFOCOM and GLOBECOM. He served as editors for International Journal of Communication

Systems, China Communications, and guest editors for Wireless Communications and Mobile Computing and the IEEE COMSOC MMTC Communications.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/csdl.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_5_img_1.jpeg|page_5_img_1]]
3. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_7_img_1.jpeg|page_7_img_1]]
4. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_9_img_1.jpeg|page_9_img_1]]
5. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_9_img_2.png|page_9_img_2]]
6. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_10_img_1.jpeg|page_10_img_1]]
7. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_10_img_2.jpeg|page_10_img_2]]
8. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_13_img_1.jpeg|page_13_img_1]]
9. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_13_img_2.png|page_13_img_2]]
10. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_13_img_3.jpeg|page_13_img_3]]
11. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_16_img_1.jpeg|page_16_img_1]]
12. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_16_img_2.jpeg|page_16_img_2]]
13. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_16_img_3.jpeg|page_16_img_3]]
14. [[../extracted_images/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-/page_16_img_4.jpeg|page_16_img_4]]

---

