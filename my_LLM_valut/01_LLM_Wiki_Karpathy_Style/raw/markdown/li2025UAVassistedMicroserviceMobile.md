# UAV-Assisted Microservice Mobile Edge Computing Architecture: Addressing Post-Disaster Emergency Medical Rescue

Ji Li , Qiang He , Associate Member, IEEE, Xingwei Wang , Ammar Hawbani , Keping Yu , Senior Member, IEEE, Yuanguo Bi , Member, IEEE, and Liang Zhao ï¼

AbstractâIn post-disaster emergency medical rescue operations, rapidly establishing an adaptive and flexible edge computing (EC) network, balancing data offloading with energy consumption, and ensuring the stable operation of the network have become urgent priorities. To address these challenges, we proposed an unmanned aerial vehicle (UAV)-assisted microservice mobile edge computing (MEC) architecture. The architecture can be rapidly deployed to provide temporary network coverage and EC services in disasterstricken areas. A transformer-based resource management (TBRM) approach is utilized to optimize data offloading efficiency and reduce energy consumption, thereby maximizing the service time of the architecture. To enhance the security and reliability of the architecture, four microservices are designed to manage the full UAV lifecycle, and UAV identity authentication is implemented through dual digital signature certificates. Large-scale simulation experiments have demonstrated the effectiveness of the architecture in complex rescue scenarios, providing strong technical support for post-disaster medical rescue efforts.

Index TermsâUnmanned aerial vehicle, mobile edge computing, transformer, Lyapunov optimization, post-disaster emergency medical rescue.

## I. INTRODUCTION

N recent years, the growing frequency of natural disasters, I such as volcanic eruptions and earthquakes, has frequently resulted in large numbers of casualties and missing persons. Postdisaster emergency medical rescue is crucial in the aftermath of such events. However, in the face of severe natural disasters, fundamental service infrastructures such as networks and power supplies are often severely damaged. Therefore, rapidly constructing an adaptive and flexible EC network [1], [2] in such an environment to support post-disaster emergency medical rescue [3], [4], [5], [6] remains a significant challenge. Fortunately, the flexibility and mobility of UAVs [7], [8], [9] offer an opportunity to achieve this goal. UAVs can move flexibly within an area and, when equipped with mobile base stations, can quickly adjust their positions to provide network service coverage. Additionally, UAVs can be equipped with MEC devices and sensor equipment, thereby providing essential computational capabilities for postdisaster emergency medical rescue.

Advances from heavyweight to lightweight convolutional neural network (CNN) architectures [10], [11], [12], [13], [14] have made it feasible to deploy deep learning models on resource-limited mobile edge devices. The Transformer [15], a foundational component of large models, incorporates a selfattention mechanism that can effortlessly handle input sequences of varying lengths and complexities without requiring predefined rules or boundaries. In the complex environment of post-disaster rescue, this capability enables rapid acquisition of critical information, accurate situation assessment, and dynamic adjustment of rescue strategies, thereby ensuring the most effective response in the shortest possible time and gaining valuable time for lifesaving operations. Moreover, microservices have shown remarkable potential [16], [17], [18] in recent years through their deep integration with fields such as edge computing and the Internet of Things (IoT). It not only decomposes the system into independent services, ensuring high availability and fault isolation, but also facilitates rapid scaling and deployment based on demand. Especially in the context of emergency medical rescue, microservices can rapidly respond to and recover from unforeseen events. It is based on the immense potential of UAVs, Transformers, and microservices in post-disaster emergency medical rescue that we have conducted research on a UAV-assisted microservice MEC architecture. The main contributions can be summarized as follows:

1) We proposed a UAV-assisted microservice MEC architecture for post-disaster emergency medical rescue. The architecture can self-organize, automatically manage the entry and exit of UAVs, and provide long-term, secure, stable, and efficient EC services to disaster-affected users (briefly noted as users).

2) We proposed a Transformer-based resource management method, which comprehensively considers data offloading, energy consumption, and response latency. This approach employs the Transformer-based channel allocation generator (TCAG) to generate offloading decisions and a dynamic resource optimization allocator (DROA) to execute various optimizations. A generator optimization strategy (GOS) is designed to update TCAG parameters, aiming to maximize the service time of the architecture.

3) We conducted a detailed analysis of the post-disaster emergency medical rescue scenario and subsequently designed four microservices. These four microservices encompass the full UAV lifecycle. In particular, dual digital signature certificates are utilized to ensure the security of UAVs registration, networking, and exit processes.

4) Unlike existing simulation validations, which only consider a small number of users and short service durations, we conducted extensive simulations with several times more users and longer service durations. This verified the effectiveness of the proposed method and demonstrated the feasibility of the proposed framework in real rescue environments.

The rest of this paper is organized as follows. Section II provides a review of previous research and literature related to the topic of the paper. Section III presents the system model and clearly defines the problem that the paper aims to solve. In Section IV, the paper presents the detailed design of the proposed method, namely the TBRM. Section V describes the experiments conducted to validate and evaluate the effectiveness of the proposed method. Section VI concludes the paper.

## II. RELATED WORK

## A. Edge Computing in Emergency Medical Rescue

In recent years, scholars have begun to apply EC technology to disaster rescue scenarios. Liu et al. [19] utilized the computational power of edge servers to perform real-time preprocessing and analysis of disaster images, thereby supporting emergency response and rescue operations. Mao et al. [20] designed a space-aerial-assisted hybrid cloud-edge computing framework, which utilizes UAVs and satellites to provide low-latency services for IoT devices, optimizing resource scheduling to minimize computational delays. The studies [21], [22] explored the feasibility of UAV-assisted intelligent EC from the perspective of supporting rescue personnel. Zhang et al. [23] studied the issues of fault tolerance and rapid response of computing services in disaster scenarios. They designed a fault-tolerant distributed task offloading scheme to minimize task execution time and system energy consumption using a multi-agent proximal policy optimization algorithm.

The aforementioned studies explore various aspects of using EC to assist in disaster relief in natural disaster environments from different perspectives. However, existing research still has limitations, particularly when considering disaster-affected users as the service target. It fails to adequately take into account the sustainable operational capacity of emergency medical rescue in large-scale disaster scenarios.

## B. Microservice-Based Edge Computing

Microservice architecture can decompose applications into multiple small, independent services, each of which can be developed, deployed, and scaled independently. Researchers have already integrated it with EC in various scenarios. The studies [24], [25], [26] explore microservice deployment and resource allocation from different perspectives, including microservice edge computing resource configuration methods, optimization of microservice instance selection, and deployment strategy optimization to reduce communication overhead based on deep Q-learning. Guo et al. [27] optimized microservice selection and scheduling in cloud-edge environments using the Markov decision process and the deep deterministic policy gradient algorithm, creating an experience pool to reduce user access latency. Tang et al. [28] proposed an adaptive microservice deployment method for IoT in MEC, using the Adam and weighted round-robin scheduling to minimize resource costs, meet delay constraints, and balance edge server workloads. Ray et al. [29] proposed a proactive mechanism based on reinforcement learning and learning automata for microservice deployment and migration in multi-access EC, tracking user mobility and server capacity to trigger migration and prevent overload.

From the above, it is clear that existing architectures combining microservices and EC primarily focus on the deployment, operation, and optimization of microservices. However, few studies have utilized microservice characteristics to design specialized applications in EC frameworks.

## C. Resource Management Algorithms

Efficient management of computing resources and optimization of energy consumption are critical aspects in any MEC framework. Hoang et al. [30] proposed an online resource management framework based on dual-channel links. Their simulation, involving 8 users, 1 cellular base station, and 1 UAV, demonstrated the frameworkâs ability to optimize average system power consumption. Zhang et al. [31] introduced a greedystrategy-based orbital EC task allocation algorithm. It aims to utilize multiple access EC servers in low earth orbit satellite networks to serve ground users. Ding et al. [32] proposed a novel online edge learning offloading scheme for secure communication in UAV-assisted MEC, improving the performance of secure computing. Hasan et al. [33] explored the application of 6G networks in supporting autonomous driving and vehicle edge computing, emphasizing the role of computational offloading and resource management in reducing communication costs, protecting privacy, and reducing training processes. Zhang et al. [34] presented an action-constrained deep reinforcement learning approach for secure computation resource allocation, aimed at addressing the limited computing resources available on user devices.

Overall, resource management algorithms are numerous and varied, designed to address complex and changing scenarios.

<!-- image-->  
Fig. 1. UAV-assisted microservice MEC architecture.

However, for post-disaster rescue scenarios, due to their unique nature, no algorithm currently exists that minimizes system energy consumption by accounting for both UAV flight energy consumption and computing resource allocation.

## III. SYSTEM MODEL

## A. UAV-Assisted Microservice MEC Architecture

The overall structure of the UAV-assisted microservice MEC architecture is illustrated in Fig. 1. The UAV search queue equipped with MEC servers, along with the rescue team, constitute the primary forces in the search and rescue area. The UAV search queue provides temporary network and EC services in the search and rescue area, enabling users to contact rescue personnel, friends, and family for assistance. Furthermore, we propose four distinct microservices deployed on each UAV-MEC server involved in the rescue operation. These four microservices collaborate to support the full lifecycle of the UAVs. Behind the disaster area, trucks equipped with mobile base stations and edge devices provide network communication and real-time computing capabilities for the temporary medical center and the command center. They also receive real-time rescue data from the search area, and then employ advanced artificial intelligence models to analyze data and assist rescue coordination. Mobile power vehicles support the logistical operations by providing electricity for the entire area. Backup UAV units and battery packs remain on standby based on frontline rescue conditions to ensure the stability of the architecture. For ease of reference, key notations used in the paper are summarized in Table I.

## B. Task Execution Model

In the UAV-assisted microservice MEC architecture, we consider that all requests from users can either be processed locally or offloaded to a UAV-MEC server. The decision between local computation or hybrid computation depends on a balance algorithm between latency and energy consumption. The scenario considered is depicted in Fig. 2: UAV-MEC servers are stationed at a height of 50 meters, providing services within a $2 k m \times 2 k m$ area using five UAVs. Users beyond the 2km  2km area can have UAV-MEC servers dispatched to their location through microservices control. Alternatively, a similar UAV-MEC server array can be deployed to provide the same computing offload services. In this scenario, a user may simultaneously fall within the coverage range of three UAV-MEC servers. However, in this architecture, we stipulate that a user can only offload tasks to one UAV-MEC server. This approach aims to minimize the complexity of the system, ensuring that the energy optimization and data offloading are performed within a fixed system environment. Specifically, we adopt the idea of load balancing to distribute users who are simultaneously covered by multiple UAV-MEC servers.

TABLE I  
SUMMARY OF KEY NOTATIONS
<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $\overline { { S } }$ </td><td>The setofUAV-MEC servers</td></tr><tr><td> $N$ </td><td>The set of users in the search area</td></tr><tr><td> $f _ { n }$ </td><td>The number of CPU cycles for user n</td></tr><tr><td> $T a s k _ { n }$ </td><td>The computational task generated by user n</td></tr><tr><td> $m$ </td><td>The data size of  $T a s k _ { r }$ </td></tr><tr><td> $L _ { n }$ </td><td>Required CPU cycles for user n to process 1 bit of data</td></tr><tr><td> $f _ { s , n }$ </td><td>CPU computation resources allocated by UAV-MEC server s to user n</td></tr><tr><td> $L _ { s }$ </td><td>Required CPU cycles for UAV-MEC server s to process 1 bit of data</td></tr><tr><td> $w t r _ { s , n }$ </td><td>The wireless transmission data rate between s and n</td></tr><tr><td> $\lambda$ </td><td>The ratio of  $T a s k _ { n }$  offloaded locally</td></tr><tr><td> $\xi _ { n }$ </td><td>Effective switched capacitance of user n</td></tr><tr><td> $\xi _ { s }$ </td><td></td></tr><tr><td></td><td>Effective switched capacitance of UAV-MEC server s</td></tr><tr><td> $p _ { n }$ </td><td>The transmission power of user n&#x27;s device</td></tr><tr><td> $\psi$ </td><td>Scaling factor</td></tr><tr><td> $t _ { d }$ </td><td>Hovering time</td></tr><tr><td> $H$ </td><td>Relative hover/rise/fall height</td></tr><tr><td> $M _ { g }$ </td><td>The total weight of the UAV carrying various equipment</td></tr><tr><td> $\tau$ </td><td>Time slot length</td></tr><tr><td> $\nu$   $t$ </td><td>UAV&#x27;s velocity vector Time slot</td></tr><tr><td> $\beta _ { s , n } ^ { t }$ </td><td>The link between user n and UAV-MEC server s in time</td></tr><tr><td></td><td>slot t</td></tr><tr><td> $\boldsymbol { \mathfrak { x } } _ { s , n } ^ { t }$ </td><td>The ratio of bandwidth allocated to user n by UAV-MEC server s in time slot t</td></tr><tr><td> $r _ { s , n } ^ { t }$ </td><td>The volume of tasks ofloaded by user n to UAV-MEC server</td></tr><tr><td></td><td>s in time slot t</td></tr><tr><td> $f _ { \underline { { n } } } ^ { t }$ </td><td>The local CPU frequency of user n in time slot t</td></tr><tr><td> $f _ { s , n } ^ { \prime }$ </td><td>The ratio of computational resources allocated to user n by</td></tr><tr><td></td><td>UAV-MEC server s in time slot t</td></tr><tr><td> $Q _ { n } ^ { L } ( t )$ </td><td>The task execution queue for user n in time slot t</td></tr><tr><td> $\ddot { D } _ { n } ^ { t }$ </td><td>The volume of tasks departing from the user n&#x27;s local queue in</td></tr><tr><td> $l _ { n } ^ { t }$ </td><td>time slot t The volume of tasks processed locally by user n in time slot t</td></tr><tr><td>A</td><td>The volume of newly arrived tasks generated by user n in time</td></tr><tr><td> $Q _ { s } ^ { U } ( t )$ </td><td>slot t The task execution queue for UAV-MEC server s in time</td></tr><tr><td></td><td>slot t The volume of user n&#x27;s tasks processed by UAV-MEC server s</td></tr><tr><td> $c _ { n } ^ { t }$ </td><td>in time slot t</td></tr><tr><td> $Z _ { n } ^ { L } ( t )$ </td><td>The virtual task execution queue for user n in time slot t</td></tr><tr><td> $Z _ { s } ^ { U } ( t )$ </td><td>The virtual task execution queue for UAV-MEC server s in time slot t</td></tr><tr><td> $h _ { s , n } ^ { t }$ </td><td>The channel power gain between user n and MEC server s in</td></tr><tr><td></td><td>time slot t</td></tr><tr><td></td><td></td></tr><tr><td> $W _ { s }$ </td><td>The total bandwidth of UAV-MEC server s</td></tr></table>

<!-- image-->  
Fig. 2. Service Area of UAV-MEC servers.

let ${ \cal { S } } = \{ S _ { 1 } , S _ { 2 } , S _ { 3 } , S _ { 4 } , S _ { 5 } \}$ represent the set of UAV-MEC servers in the initial state, $N _ { i } = \{ 1 , 2 , 3 , . . . , n \} , i \in \{ 1 , 2 , 3 , 4 , 5 \}$ represent the set of users within the range of UAV-MEC server $S _ { i } .$ In the field of MEC, CPU cycles are a crucial metric for measuring the computational capacity of a device. For any user n, we denote $f _ { n } ( \mathrm { c y c l e s } / \mathrm { s } )$ as the number of CPU cycles of that userâs device. The latest mobile CPU architectures utilize advanced dynamic frequency and voltage scaling technology, which can increase or decrease CPU cycles. Hence, $f _ { n } \leq f _ { n } ^ { \mathrm { m a x } }$ According to [35], for the computational task $T a s k _ { n }$ generated by user n with a data size of $m ,$ the total execution time $T ^ { L }$ for $T a s k _ { n }$ to be fully executed locally can be expressed as:

$$
T ^ { L } = \frac { m L _ { n } } { f _ { n } }\tag{1}
$$

For example, in EC scenarios such as object detection or other machine learning tasks that process camera frames, execution time is typically proportional to data size. When the frame resolution matches the machine learning model input, higher resolution results in longer inference times due to increased computational workload. Similarly, let $f _ { s , n } ( \mathrm { c y c l e s } / \mathrm { s } ) , s \in S _ { i } , n \in N _ { i }$ represent the Ã° Ã 2 2CPU computation resources allocated by UAV-MEC server s to user n, and $w t r _ { s , n }$ is the wireless transmission data rate between UAV-MEC server s and user n. The total execution time $T ^ { S }$ for user n to offload $T a s k _ { n }$ entirely to UAV-MEC server s can be expressed as:

$$
T ^ { S } = \frac { m L _ { s } } { f _ { s , n } } + \frac { m } { w t r _ { s , n } }\tag{2}
$$

In the designed architecture of this paper, multiple users can offload their tasks to the same UAV-MEC server, but one user cannot offload tasks to multiple UAV-MEC servers simultaneously. Suppose the ratio of local computation and offloading for user n is $\lambda ~ ( 0 \leq \lambda \leq 1 )$ and $1 - \lambda .$ , respectively. The total execution time $T ^ { j o i n t }$ can be expressed as:

$$
T ^ { j o i n t } = \frac { \lambda m L _ { n } } { f _ { n } } + \frac { ( 1 - \lambda ) m L _ { s } } { f _ { s , n } } + \frac { ( 1 - \lambda ) m } { w t r _ { s , n } } .\tag{3}
$$

## C. Energy Consumption for Data Offloading

After a natural disaster, users cannot ensure the continuous power supply for their devices. Therefore, minimizing the energy consumption of user devices is essential for enabling timely and proactive rescue-seeking in energy-constrained scenarios. According to [36], the energy consumption per CPU cycle for user n is $\xi _ { n } f _ { n } ^ { 2 }$ , where $\xi _ { n }$ is the effective switched capacitance, depending on n nthe chip architecture. Hence, the energy consumption $E ^ { L }$ for user n to process the computational Taskn locally can be expressed as:

$$
E ^ { L } = \xi _ { n } m L _ { n } f _ { n } ^ { 2 }\tag{4}
$$

Similarly, the energy consumption $E ^ { T o t a l }$ for user n to offload the entire task data to UAV-MEC server s is:

$$
E ^ { T o t a l } = E ^ { S } + E ^ { L , T r a n s }\tag{5a}
$$

$$
E ^ { S } = \xi _ { s } m L _ { s } f _ { s , n } ^ { 2 }\tag{5b}
$$

$$
E ^ { L , T r a n s } = p _ { n } \frac { m } { w t r _ { s , n } }\tag{5c}
$$

Next, consider the energy consumption for user n to offload the computing Taskn in a hybrid manner. Suppose the ratio of local computation and offloading for user n is  and 1 â , respectively. The energy consumption $E _ { m i x } ^ { T o t a l }$ can be expressed as:

$$
E _ { m i x } ^ { T o t a l } = E _ { m i x } ^ { S } + E _ { m i x } ^ { L } + E _ { m i x } ^ { L , T r a n s }
$$

$$
E _ { m i x } ^ { S } = ( 1 - \lambda ) \xi _ { s } m L _ { s } f _ { s , n } ^ { 2 }\tag{6a}
$$

(6b)

$$
E _ { m i x } ^ { L } = \lambda \xi _ { n } m L _ { n } f _ { n } ^ { 2 }\tag{6c}
$$

$$
E _ { m i x } ^ { L , T r a n s } = p _ { n } \frac { ( 1 - \lambda ) m } { w t r _ { s , n } } .\tag{6d}
$$

## D. Energy Consumption for Flying

Another factor that impacts the overall service time of the architecture is the UAV flight energy consumption. Unlike [37] and [38], we take into account a energy consumption model that better reflects real-world application scenarios. Specifically, we draw on the validated conclusions of [39]. However, as the UAV model considered in [39] is lightweight, its direct application to rescue missions is limited. To overcome these limitations, we scaled up the flight energy consumption in [39] proportionally based on the UAVâs weight to preserve the core properties and conclusions of the original energy consumption function. We stipulate that when the UAV departs from the command center base to reach a designated service area, the UAV will sequentially experience three flight states: vertical ascent, horizontal flight, and vertical ascent. If the service time in the current area ends, we only consider horizontal flight when the UAV moves from the current area to the next service area. When the battery is depleted and needs to return for recharging, the UAV will execute horizontal flight, and vertical descent. Next, we will introduce the energy consumption of each flight state using scaling factor $\psi .$ . Firstly, the energy consumption $E _ { h }$ for hovering is given by:

$$
E _ { h } = \int _ { 0 } ^ { t } \psi t _ { d } ( a _ { 1 } H + a _ { 2 } )\tag{7}
$$

Where $t _ { d }$ is the hovering time, H is the hovering height, $a _ { 1 }$ and $a _ { 2 }$ are constants. The energy consumption $E _ { u p }$ for vertical ascent is given by:

$$
E _ { u p } = \psi ( b _ { 1 } H ^ { 2 } + b _ { 2 } H + b _ { 3 } )\tag{8}
$$

Where $b _ { 1 } , b _ { 2 }$ and $b _ { 3 }$ are constants. The energy consumption $E _ { d o w n }$ for vertical descent is given by:

$$
E _ { d o w n } = \psi ( c _ { 1 } H ^ { 2 } + c _ { 2 } H + c _ { 3 } )\tag{9}
$$

Where $c _ { 1 } , c _ { 2 }$ and $c _ { 3 }$ are constants. For horizontal flight energy consumption $E _ { f } ,$ since the flight speed is not mentioned in [39], we consider using the simplified model from [38], which is represented as:

$$
E _ { f } = 0 . 5 M _ { \mathrm { g } } \tau \Vert \nu \Vert ^ { 2 }\tag{10a}
$$

$$
\nu = \frac { | | l o c ( t + 1 ) - l o c ( t ) | | } { \tau }\tag{10b}
$$

In the above equation, $M _ { \mathrm { g } }$ represents the total weight of the UAV carrying various equipment,  is the time slot length. v is sthe UAVâs velocity vector, defined as the ratio of the distance increment to the time increment in the horizontal plane. loc t Ã° Ã¾1 represents the UAVâs position coordinates in the horizontal plane at time t  1, and loc t represents the UAVâs position Ã¾ Ã° Ãcoordinates in the horizontal plane at time t (Please note that t here represents a specific time instant with zero duration).

## E. Task Queue

In this architecture, two types of execution queues are considered: the local task execution queue $Q _ { n } ^ { L }$ and the UAV-MEC server task execution queue $Q _ { s } ^ { U }$ . The update process of $Q _ { n } ^ { L } ( t )$ and $Q _ { s } ^ { U } ( t )$ can be expressed as:

$$
Q _ { n } ^ { L } ( t + 1 ) = \operatorname* { m a x } \{ Q _ { n } ^ { L } ( t ) - D _ { n } ^ { t } , 0 \} + A _ { n } ^ { t } , n \in N _ { i } , t \in \mathbb { T }\tag{11}
$$

$$
Q _ { s } ^ { U } ( t + 1 ) = \operatorname* { m a x } \{ Q _ { s } ^ { U } ( t ) - c _ { n } ^ { t } , 0 \} + r _ { s , n } ^ { t } , n \in N _ { i } , s \in S _ { i } , t \in \mathrm { T }\tag{12}
$$

Where $D _ { n } ^ { t } \triangleq l _ { n } ^ { t } + r _ { s , n } ^ { t } , ~ Q _ { n } ^ { L } ( 0 ) = Q _ { s } ^ { U } ( 0 ) = 0 .$ . To ensure that Ã¾ Ã° Ã Â¼ Ã° Ã Â¼users are not adversely affected by high latency, we define the average queue lengths for user n and UAV-MEC server s as $\overline { { Q } } _ { n } ^ { L }$ and $\breve { \overline { { Q } } } _ { s } ^ { U }$ , respectively.

$$
\overline { { { Q } } } _ { n } ^ { L } = \operatorname* { l i m } _ { T  \infty } \frac { 1 } { T } { \sum _ { t = 0 } ^ { T } } E [ Q _ { n } ^ { L } ( t ) ] \leq Q _ { n } ^ { t h }\tag{13a}
$$

$$
\overline { { \ u { Q } } } _ { s } ^ { U } = \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } { \sum _ { t = 0 } ^ { T } } E [ \ u { Q } _ { s } ^ { U } ( t ) ] \leq { Q } _ { s } ^ { t h }\tag{13b}
$$

In the above equations, $Q _ { n } ^ { t h }$ and $Q _ { s } ^ { t h }$ are the threshold values for the average queue lengths of user n and UAV-MEC server s, respectively.

## F. Microservice Design

Given that the architecture must maintain continuous operation for extended periods in real-world application scenarios, the transmission of information and UAV scheduling become particularly crucial. We analyzed the post-disaster emergency medical rescue scenario in detail and proposed four distinct microservices to address its specific needs. Next, we will introduce the four microservices in terms of their functionality, key design points, and specific implementation.

1) UAV Registration and Authentication Service:

Functionality: This service handles UAV registration requests, verifies the identities of newly added UAVs, and ensures that only authorized UAVs are admitted into the system.

Key Design Points: The base command center is likened to a Root Certificate Authority (CA). Newly added UAVs are regarded as Subordinate CA. We designed a dual digital signature certificate system. This includes Digital Signature Registration Certificate (DSRC), Digital Signature Networking Certificate (DSNC), and Digital Signature Decommissioning Certificate (DSDC).

Specific Implementation: The full lifecycle of a UAV includes three stages: registration, networking, and exit, as shown in Fig. 3. During the registration phase, the UAV first generates a DSRC using its private key. The Root CA decrypts this certificate using the UAVâs public key. Only when Root CA confirms that the signature of the DSRC is from the UAV applying for registration, will the Root CA sign the certificate with its private key, while also recording the information of the UAV. Next, the UAV begins networking. In the networking phase, we adopt a âwho verifies, who signsâ principle to ensure security and traceability. The first registered UAV must obtain a DSNC from both the Root CA and itself. Subsequently, newly added UAVs can utilize their DSRC and self-signed DSNC to initiate networking requests with nearby UAVs that have already formed a network. Once the requested UAV verifies the authenticity of DSRC and DSNC, it will use its private key to add its digital signature to the applicantâs DSNC, while simultaneously informing other UAVs of the networking information. When a UAVâs battery is about to run out or it can no longer provide service, it needs to request exiting the network. Prior to this, it needs to sign a DSNC for the replacement UAV, allowing the new UAV to take over its duties and continue working. Additionally, it needs to synchronize relevant information with the replacement UAV. After the information synchronization is complete, the UAV that needs to exit uses its DSNC and selfsigned DSDC to submit an exit request to the newly added UAV. After the request is approved, the new UAV adds its digital signature to the DSDC of the UAV requesting to exit. Once the exiting UAV returns to the base, it completes secure decommissioning by validating its DSDC.

<!-- image-->  
Fig. 3. UAV lifecycle diagram.

2) UAV States Management Service:

Functionality: The real-time collection, storage, and updating of UAV status information, such as location, battery level, health status, provide data support for other services.

Key Design Points: Utilize the lightweight message queue framework Kafka to achieve real-time collection of UAV status information, providing comprehensive support for the architecture with relevant UAV data.

Specific Implementation: Since the MEC architecture decomposes optimization tasks into deterministic problems for each time slot, the UAV status management service can update and collect the UAV status information after the optimization for each time slot is completed.

3) UAV Scheduling Service:

Functionality: Based on task requirements and UAV status, a scheduling plan is formulated to achieve automatic allocation and collaboration among UAVs.

Key Design Points: This service needs to ensure that the energy consumption error during UAV scheduling remains within a certain range and maximizes the service time of UAVs.

Specific Implementation: Under the proposed architecture, the UAV scheduling problem focuses mainly on two aspects. One aspect involves the entry and exit of UAVs, while the other concerns the overall movement of the UAVsâ service areas. The latter only requires specifying the target position and following a predetermined flight route. However, the former requires establishing entry and exit rules, along with energy calculations, to fulfill specified requirements. We utilize long-term CPU utilization (For 100 consecutive time slots, the average CPU utilization exceeds 90%) as an evaluation metric to determine whether new UAVs need to be deployed. It should be noted that newly added UAVs may exit the system only after completing service in the current area or when their power is nearly depleted. This is to avoid energy consumption caused by repeated joining and exiting of UAVs. The newly added UAVs will fly to a location near the UAV that made the request to maintain the stability of the rescue network. Simultaneously, we calculate the energy consumption for returning to the base using the UAV status indicators provided by the UAV status management service, which defines the minimum battery level indicator for formulating UAV exit plans.

4) Communication With Edge Computing Service:

Functionality: Ensure communication between UAVs to support data transmission and collaborative work, while leveraging the computational capabilities of UAV-MEC servers to provide EC services for disaster-affected areas.

Key Design Points: Ensure low-latency and reliable communication between UAVs, while also embedding essential computational resource management within this service.

Specific Implementation: We employ the lightweight constrained application protocol (CoAP). CoAP is selected because it requires minimal network bandwidth and device resources, and its non-persistent connection mode reduces energy consumption. Additionally, CoAP provides a secure transmission layer based on datagram transport layer security, ensuring the confidentiality and integrity of data during transmission. The computational resource management is implemented using the TBRM method discussed in Section IV.

## G. Cost Optimization Problem

The systemâs energy consumption $E _ { s y s }$ comprises local execution energy consumption by the user, UAV-MEC server execution energy consumption, data transmission energy consumption, and UAV flight energy consumption. This can be formulated as:

$$
E _ { s y s } = E _ { m i x } ^ { T o t a l } + E _ { s } ^ { T o t a l }\tag{14}
$$

$E _ { s } ^ { T o t a l } ( s \in S )$ represents the flight energy consumption of all UAVs participating in the rescue operation. The factors affecting energy consumption $( \mathrm { i . e . }$ , the variables that need to be optimized) are summarized as follows:

1) The link between users and UAV-MEC servers in time slot t.

2) The bandwidth resources allocated by UAV-MEC servers to each user in time slot t.

3) The volume of tasks offloaded by users to the UAV-MEC servers in time slot t.

4) The local CPU frequency of users in time slot t.

5) The computational resources allocated by UAV-MEC servers to each user in time slot t.

We denote the aforementioned factors as $\beta _ { s } ^ { t } , \alpha _ { s } ^ { t } , r _ { s } ^ { t } , f _ { n } ^ { t } \mathrm { . }$ , and $f _ { s } ^ { t }$ respectively. Let $X ^ { t } = \{ \beta _ { s } ^ { t } , \alpha _ { s } ^ { t } , r _ { s } ^ { t } , f _ { n } ^ { t } , f _ { s } ^ { t } \}$ b arepresent the combination of all optimization vectors of user n and UAV-MEC server s in time slot t. Let $X = \left\{ X ^ { t } \right\} _ { t \in T }$ represent the combination of all Â¼ f g 2optimization variables over time. Our objective is to minimize the long-term average system energy consumption to maximize the systemâs service time and the usersâ connectivity duration. Therefore, the optimization problem can be formulated as follows:

$$
P 1 \operatorname* { m i n } _ { X } \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } { \sum _ { \mathrm { t } = 0 } ^ { T - 1 } } E [ E _ { s y s } ( t ) ]\tag{15}
$$

$$
\begin{array} { c } { s . t . ~ \beta _ { s } ^ { t } = \{ \beta _ { s , 1 } ^ { t } , \beta _ { s , 2 } ^ { t } , . . . , \beta _ { s , n } ^ { t } \} , \beta _ { s , n } ^ { t } = \{ 0 , 1 \} , } \\ { n \in N _ { i } , s \in S _ { i } , t \in T } \end{array}\tag{16a}
$$

$$
\alpha _ { s } ^ { t } = \{ \alpha _ { s , 1 } ^ { t } , \alpha _ { s , 2 } ^ { t } . . . \alpha _ { s , n } ^ { t } \} , 0 \leq \alpha _ { s , n } ^ { t } , \sum _ { n = 1 } ^ { N _ { i } } \alpha _ { s , n } ^ { t } \leq 1 ,
$$

$$
n \in N _ { i } , s \in S _ { i } , t \in T\tag{16b}
$$

$$
\begin{array} { c } { r _ { s } ^ { t } = \{ r _ { s , 1 } ^ { t } , r _ { s , 2 } ^ { t } , . . . , r _ { s , n } ^ { t } \} , \ 0 \leq r _ { s , n } ^ { t } \leq r _ { s , n } ^ { m a x } , } \\ { n \in N _ { i } , s \in S _ { i } , t \in T } \end{array}\tag{16c}
$$

$$
0 \leq f _ { n } ^ { t } \leq f _ { n } ^ { \operatorname* { m a x } } , n \in N _ { i } , t \in T\tag{16d}
$$

$$
\sum _ { n = 1 } ^ { N _ { i } } f _ { s , n } ^ { t } \le f _ { s } ^ { \operatorname* { m a x } } , s \in S _ { i } , n \in N _ { i } , t \in T\tag{16e}
$$

13a and 13b

(16f)

It is important to note that the above constraints ensure that the user set $N _ { i }$ is within the coverage area of the UAV-MEC server $S _ { i }$ . Constraint (16a) limits whether the userâs computational tasks require the involvement of the UAV-MEC server. Constraint (16b) stipulates that the transmission bandwidth allocated by the UAV-MEC server to each user cannot exceed the maximum resource limit of the UAV-MEC server. Constraint (16c) limits the maximum offloading volume by user n to UAV-MEC server s in time slot t. Constraint (16d) indicates that the change in the userâs frequency should remain within the maximum allowable range. Constraint (16e) restricts the computational resources allocated by the UAV-MEC server to the users within its coverage area, ensuring it does not exceed the maximum permissible frequency. (13a) and (13b) are delay constraints.

To address the optimization problem P1, it is essential to analyze its time complexity. The number of optimization variables is crucial in determining the time complexity. According to the modelâs setup, in each time slot t, the variables $\beta _ { s } ^ { t } , \alpha _ { s } ^ { t } , r _ { s } ^ { t } , f _ { n } ^ { t }$ and $f _ { s } ^ { t }$ must be optimized. Since users can only offload tasks to a UAV-MEC server, it follows that for each time slot, the number of variables for each type is $O ( N )$ . Considering T time slots, the total number Ã° Ãof variables accumulates to ${ \cal O } ( T \times N )$ . In this case, the typical Ã°  Ãtime complexity for a linear programming solver is between $O ( ( T \times \bar { N ) } ^ { 3 } )$ and $O ( ( T \times N ) ^ { 3 . 5 } )$ , which is often impractical. On Ã°Ã°  Ã Ã Ã°Ã°  Ã Ãthe other hand, dynamic programming methods tend to exhibit a drastic increase in time complexity as the number of state transitions grows, potentially leading to a form like ${ \cal O } ( T \times N \times$ Ã°  state transitions , which could impose a significant computational Ãburden. In contrast, the lyapunov method offers a more efficient solution. By decomposing the global optimization problem into a series of local optimization subproblems, this approach simplifies the optimization process at each time step while avoiding the complexity of directly tackling the global optimization problem.

## H. Lyapunov-Guided Problem Transformation

We employ the lyapunov framework to transform the above optimization problem P1 into a deterministic problem for each time slot. To satisfy constraints (13a) and (13b), we introduce two virtual queues:

$$
Z _ { n } ^ { L } ( t + 1 ) = \operatorname* { m a x } \{ Z _ { n } ^ { L } ( t ) + Q _ { n } ^ { L } ( t + 1 ) - Q _ { n } ^ { t h } , 0 \}\tag{17a}
$$

$$
Z _ { s } ^ { U } ( t + 1 ) = \operatorname* { m a x } \{ Z _ { s } ^ { U } ( t ) + Q _ { s } ^ { U } ( t + 1 ) - Q _ { s } ^ { t h } , 0 \}\tag{17b}
$$

Specifically, $Z _ { n } ^ { L } ( 0 ) = Z _ { s } ^ { U } ( 0 )$ . Additionally, we define the sysÃ° Ã Â¼temâs state in time slot t as $\Theta ( t ) \triangleq \{ Q _ { n } ^ { L } , Q _ { s } ^ { U } , Z _ { n } ^ { L } , Z _ { s } ^ { U } \} _ { n \in N _ { i } , s \in S _ { i } }$ . The Ã° Ã flyapunov function is defined as follows:

$$
L ( \Theta ( t ) ) \triangleq \frac { 1 } { 2 } \sum _ { n \in N _ { i } , s \in S _ { i } } [ Q _ { n } ^ { L } ( t ) ^ { 2 } + Q _ { s } ^ { U } ( t ) ^ { 2 } + Z _ { n } ^ { L } ( t ) ^ { 2 } + Z _ { s } ^ { U } ( t ) ^ { 2 } ]\tag{18}
$$

At this point, the lyapunov drift function can be expressed as:

$$
\Delta ( \Theta ( t ) ) \triangleq E \lbrack L ( \Theta ( t + 1 ) ) - L ( \Theta ( t ) ) \vert \Theta ( t ) \rbrack\tag{19}
$$

To minimize the long-term average energy consumption while ensuring queue stability constraints, we define the lyapunov-driftplus-penalty as:

$$
\Delta _ { V } ( \Theta ( t ) ) \triangleq \Delta ( \Theta ( t ) ) + V E [ E _ { s y s } ( t ) | \Theta ( t ) ]\tag{20}
$$

Where V is a positive parameter that controls the trade-off between system energy consumption and average queue delay. We provide the upper bound of $\Delta _ { V } \big ( \Theta ( t ) \big )$ in Theorem 1, which Ã° Ã° ÃÃis very important for transforming the multistage problem P1 into the deterministic problem of each time slot. With the support of Theorem 1, we can use the technique of opportunistic expectation minimization to transform problem P1 into a deterministic problem solvable for each time slot.

Theorem 1: The Lyapunov-drift-plus-penalty $\Delta _ { V } ( \Theta ( t ) )$ is bounded as

$$
\begin{array} { r l } {  { \Delta _ { V } ( \Theta ( t ) ) \le \hat { B } - \sum _ { n \in N _ { i } } E [ ( Q _ { n } ^ { L } ( t ) + Z _ { n } ^ { L } ( t ) ) ( D _ { n } ^ { t } - A _ { n } ^ { t } ) | \Theta ( t ) ] } } \\ & { - \sum _ { n \in N _ { i } , s \in S _ { i } } E [ ( Q _ { s } ^ { U } ( t ) + Z _ { s } ^ { U } ( t ) ) ( c _ { n } ^ { t } - r _ { s , n } ^ { t } ) | \Theta ( t ) ] } \\ & { + V E [ E _ { s y s } ( t ) | \Theta ( t ) ] } \end{array}\tag{21}
$$

<!-- image-->  
Fig. 4. Transformer-based resource management.

Specifically, by removing the constant term in Theorem 1 and minimizing the upper bound of $\Delta _ { V } ( \Theta ( t ) )$ , the deterministic Ã° Ã° ÃÃproblem for each time slot is represented as follows:

$$
\begin{array} { c } { { P 2 \displaystyle \operatorname* { m i n } _ { X ^ { t } } G ( X ^ { t } ) } } \\ { { s . t . } } \end{array}\tag{22}
$$

The objective function $G ( X ^ { t } )$ can be expressed as follows:

$$
\begin{array} { l } { \displaystyle { G ( X ^ { t } ) = - \sum _ { n \in N _ { i } } [ ( Q _ { n } ^ { L } ( t ) + Z _ { n } ^ { L } ( t ) ) ( l _ { n } ^ { t } + r _ { s , n } ^ { t } ) ] } } \\ { \displaystyle { ~ - \sum _ { n \in N _ { i } , s \in S _ { i } } [ ( Q _ { s } ^ { U } ( t ) + Z _ { s } ^ { U } ( t ) ) ( c _ { n } ^ { t } - r _ { s , n } ^ { t } ) ] } } \\ { \displaystyle { ~ + V ( E _ { \mathrm { s y s } } ( t ) ) } } \end{array}\tag{23}
$$

## IV. TRANSFORMER-BASED RESOURCE MANAGEMENT

We propose the TBRM method to solve the optimization problem P2 in each time slot. This method consists of three components, as shown in Fig. 4.

1) Transformer-Based Channel Allocation Generator

2) Dynamic Resource Optimization Allocator

3) Generator Optimization Strategy

The input of the TCAG is $[ Q _ { n } ^ { L } ( t ) , Q _ { s } ^ { U } ( t ) , Z _ { n } ^ { L } ( t ) , Z _ { s } ^ { U } ( t ) ] _ { n \in N _ { i } , s \in S _ { i } } .$ Â½The output can be represented as $\{ \tilde { x } _ { m , s } ^ { t } \} _ { m = 1 } ^ { k }$ 2 2, which denotes the k f g Â¼channel allocation decisions for the current server s. Once the temporary channel allocations are determined, P2 can be decomposed into several subproblems with independent objectives and constraints. Subsequently, the DROA conducts detailed optimization on the k generated potential channel allocation decisions, determining the optimal offloading volume, bandwidth allocation, and other parameters under the current channel allocation decision. By selecting the sub-optimal allocation decision, user tasks are processed through offloading. Next, the GOS uses the suboptimal channel allocation decision as pseudo-labels to update the TCAG. In the following sections, we will provide a detailed introduction to each component.

## A. Transformer-Based Channel Allocation Generator

The TCAG consists of transformer multi-head attention layers, normalization operations, regularization, fully connected layers, global average pooling layer, and sigmoid activation functions. The overall network structure is shown as the TCAG in Fig. 4. The TCAG first uses fully connected layers to linearly combine the input features using its weights and biases, which helps to capture interactions and combinations between features. By introducing the ReLU activation function, the network model can learn complex nonlinear relationships. Next, the TCAG adds TransformerBlock layers (the structure of a TransformerBlock is shown in Fig. 5.) in a loop, enabling the model to capture long-term dependencies in the input sequence. Each TransformerBlock includes a multi-head attention mechanism, residual connections, normalization, and dropout layers. The multi-head attention mechanism splits the input into multiple âheadsâ to process in parallel, with each head learning different parts of the input, thereby enhancing the modelâs ability to capture information. The residual connections introduce an identity mapping that helps mitigate the vanishing or exploding gradient problem. The normalization layer stabilizes the training process and accelerates convergence, while the dropout layer prevents overfitting by randomly dropping out some neuronsâ outputs. Afterward, the TCAG uses a global average pooling layer to average the feature sequence along the sequence dimension, reducing the number of parameters and computational load while retaining the most important features. Finally, the TCAG employs successive fully connected layers to map the extracted features to the final output classes. After generating the channel allocation probability decisions for each user using TCAG, the decisions are ranked according to these probabilities to obtain one channel allocation decision. To obtain the remaining k â 1 channel allocation decisions, Gaussian noise is added to the channel allocation probabilities followed by the same selection process. The mean of the gaussian noise is 0, the variance is $\sigma _ { n } ^ { 2 } \mathbf { I }$ , and I represents the identity matrix.

<!-- image-->  
Fig. 5. Structure of the TransformerBlock.

## B. Dynamic Resource Optimization Allocator

After obtaining the temporary allocation decisions predicted by the TCAG, we decompose $P 2$ into four sub-problems. Using a model-based approach, we can precisely determine the suboptimal solution $y ^ { t } = [ \alpha _ { s } ^ { t } , r _ { s } ^ { t } , f _ { n } ^ { t } , f _ { s } ^ { t } ] _ { n \in N _ { i } , s \in S _ { i } }$ in time slot t.

Â¼ Â½a  2 21) Optimize Offload and Bandwidth Allocation: For a given channel allocation, the optimization variables for the UAV-MEC servers include bandwidth allocation $\alpha _ { s } ^ { t } \triangleq \{ \alpha _ { s , n } ^ { t } | n \in N _ { i } , \ s \in S _ { i } \}$ and offloading volume $r _ { s } ^ { t } \triangleq \{ r _ { s , n } ^ { t } | n \in N _ { i } , s \in S _ { i } \}$ j 2. Let $x ^ { t } \triangleq \{ \alpha _ { s } ^ { t } , r _ { s } ^ { t } \}$ f j 2 2 g farepresent this set of variables. The optimization decision with $x ^ { t }$ gas the independent variable can then be represented as P2.1:

$$
\begin{array} { r l } & { P 2 . 1 } \\ & { \underset { x ^ { t } } { \operatorname* { m i n } } - { \displaystyle \sum _ { n \in N _ { i } , s \in S _ { i } } } [ ( Q _ { n } ^ { L } ( t ) + Z _ { n } ^ { L } ( t ) - Q _ { s } ^ { U } ( t ) - Z _ { s } ^ { U } ( t ) ) r _ { s , n } ^ { t } ] } \\ & { \quad \quad + V { \displaystyle \sum _ { n \in N _ { i } } } E _ { m i x } ^ { L , T r a n s } } \end{array}\tag{24}
$$

$E _ { m i x } ^ { L , T r a n s }$ can be calculated using the Shannon-Hartley theorem:

$$
E _ { m i x } ^ { L , T r a n s } ( t ) = \sum _ { n \in N _ { i } , s \in S _ { i } } ( 2 ^ { \frac { r _ { s , n } ^ { t } } { W _ { s } x _ { s , n } ^ { t } \tau } } - 1 ) \frac { N _ { 0 } W _ { s } } { h _ { s , n } ^ { t } }\tag{25}
$$

To ensure the differentiability of equation (24), we artificially set a lower bound $\alpha _ { s , n } ^ { t } ,$ , denoted as $\varepsilon \le \mathsf { a } _ { s , n } ^ { t }$ . As long as  is suffia e  a eciently small, the result will approximate the original equation (24) closely. Under this condition, we can rewrite P2.1 and specify its constraints as follows:

$$
P 2 . 2 \mathrm { m i n - } \sum _ { x ^ { t } } [ ( Q _ { n } ^ { L } ( t ) + Z _ { n } ^ { L } ( t ) - Q _ { s } ^ { U } ( t ) - Z _ { s } ^ { U } ( t ) ) r _ { s , n } ^ { t } ]
$$

$$
+ V \sum _ { n \in N _ { i } , s \in S _ { i } } ( 2 ^ { \frac { r _ { s , n } ^ { r } } { W _ { s } x _ { s , n } ^ { t } \tau } } - 1 ) \frac { N _ { 0 } W _ { s } } { h _ { s , n } ^ { t } }\tag{26}
$$

$$
s . t . \quad \quad \varepsilon \leq \alpha _ { s , n } ^ { t } , \sum _ { n \in N _ { i } , s \in S _ { i } } \alpha _ { s , n } ^ { t } \leq 1\tag{27a}
$$

$$
0 \leq r _ { s , n } ^ { t } \leq \operatorname* { m i n } \{ Q _ { n } ^ { L } ( t ) , r _ { s , n } ^ { t , \operatorname* { m a x } } \}\tag{27b}
$$

Where $\begin{array} { r } { r _ { s , n } ^ { t , \operatorname* { m a x } } = W _ { s } \alpha _ { s , n } ^ { t } \tau \mathrm { l o g } _ { 2 } \Big ( 1 + \frac { p ^ { \operatorname* { m a x } } h _ { s , n } ^ { t } } { N _ { 0 } W _ { s } } \Big ) } \end{array}$ represents the upper bound of $r _ { s , n } ^ { t } ,$ , which corresponds to the scenario with maximum transmission power $p ^ { \mathrm { m a x } }$ . For users without an established channel allocation, $r _ { s , n } ^ { t , \operatorname* { m a x } } = 0$ and $\boldsymbol { \alpha } _ { s , n } ^ { t } = 0$ . To solve P2.2, we employ the gauss-seidel method to alternately optimize the offloading volume and bandwidth allocation. In each iteration, the offloading volume is determined in a closed-form solution, while the bandwidth allocation is determined using the lagrangian method. This alternating approach ensures convergence to the optimal solution because P2.2 is convex and the feasible region is the cartesian product of $r _ { s } ^ { t }$ and $\boldsymbol { \alpha } _ { s } ^ { t }$

aa) Optimal offloading volume: For a feasible bandwidth allocation, the optimal offloading volume for each user can be determined by solving the following problem:

$$
\begin{array} { r l } { P 2 . 2 . 1 \quad } & { { \mathrm { m i n i m i z e } } ( 2 6 ) } \\ & { \qquad r _ { s } ^ { t } } \\ & { { \mathrm { s u b j e c t } } \quad \mathrm { t o } ( 2 7 \mathrm { b } ) } \end{array}\tag{28}
$$

The optimal solution to P2.2.1 is either a stationary point of (26) or one of its boundary points. Specifically, when $Q _ { n } ^ { L } ( t ) + Z _ { n } ^ { L } ( t ) \leq Q _ { s } ^ { U } ( t ) + Z _ { s } ^ { U } ( t )$ , the optimal solution for $r _ { s , n } ^ { t }$ is 0. Otherwise, $( r _ { s , n } ^ { t } ) ^ { \dag } =$ max min $\{ \widehat { r } _ { s , n } ^ { t } , \ r _ { s , n } ^ { t , \operatorname* { m a x } } \} , 0 \}$ The superscript â  denotes the optimal solution, which is the same in the following context. Here, $\widehat { r } _ { s , n } ^ { t } = W _ { s } \alpha _ { s , n } ^ { t } \tau$ $\begin{array} { r } { \times \log _ { 2 } \left( \frac { Q _ { n } ^ { L } ( t ) + Z _ { n } ^ { L } ( t ) - Q _ { s } ^ { U } ( t ) + Z _ { s } ^ { U } ( t ) ) \alpha _ { s , n } ^ { t } \tau h _ { s , n } ^ { t } } { V \ln ( 2 ) N _ { 0 } } \right) } \end{array}$

b) Optimal bandwidth allocation: For feasible offloading optimization decisions $r _ { s } ^ { t } ,$ the optimal bandwidth allocation can be obtained by solving the following optimization problem:

$$
P 2 . 2 . 2 \operatorname* { m i n } _ { \alpha _ { s } ^ { t } } \sum _ { n \in N _ { i } , s \in S _ { i } } E _ { m i x } ^ { L , T r a n s } ( t )\tag{29}
$$

$$
s . t . \quad \quad \varepsilon \leq \alpha _ { s , n } ^ { t } , \sum _ { n \in N _ { i } , s \in S _ { i } } \alpha _ { s , n } ^ { t } \leq 1\tag{30a}
$$

$$
E _ { m i x } ^ { L , T r a n s } ( t ) \leq E _ { m i x } ^ { L , T r a n s , \operatorname* { m a x } }\tag{30b}
$$

The equation (30b) is equivalent to $\alpha _ { s , n } ^ { t } \geq \alpha _ { s , n } ^ { t , \mathrm { m i n } }$

$$
\alpha _ { s , n } ^ { t , \mathrm { m i n } } \triangleq \frac { r _ { s , n } ^ { t } } { W _ { s } \tau \mathrm { l o g } _ { 2 } \bigg ( 1 + \frac { E _ { m i x } ^ { L , T r a n s , \mathrm { m a x } } h _ { s , n } ^ { t } } { N _ { 0 } W _ { s } } \bigg ) }\tag{31}
$$

From this, it can be concluded that the partial lagrange function related to the above problems can be expressed as:

$$
\begin{array} { r l } & { \displaystyle { { \cal L } ( \alpha _ { s , n } ^ { t } , \lambda _ { s } ^ { t } ) \triangleq \sum _ { n \in { \cal N } _ { i } , s \in { \cal S } _ { i } } \left( 2 ^ { \frac { r _ { s , n } ^ { t } } { w _ { s } x _ { s , n } ^ { t } \tau } } - 1 \right) \frac { N _ { 0 } W _ { s } } { h _ { s , n } ^ { t } } } } \\ & { \quad \quad \quad \quad + \lambda _ { s } ^ { t } \left( \sum _ { n \in { \cal N } _ { i } , s \in { \cal S } _ { i } } \alpha _ { s , n } ^ { t } - 1 \right) } \end{array}\tag{32}
$$

$\lambda _ { s } ^ { t } \ge 0$ is the lagrange multiplier associated with constraint $\begin{array} { r l } { \sum } & { { } \alpha _ { s , n } ^ { t } \leq 1 } \end{array}$ . Based on the karush-kuhn-tucker condi  
n Ni, s Si   
tions, $( \boldsymbol { \alpha } _ { s } ^ { t } ) ^ { \dagger }$ and $\left( \lambda _ { s } ^ { t } \right) ^ { \dagger }$ should satisfy the following set of   
equations.

$$
\left\{ \underset { n \in N _ { i } , s \in S _ { i } } { \sum } ( \alpha _ { s , n } ^ { t } ) ^ { \dagger } = 1 \right. \qquad \\  \left. ( \alpha _ { s , n } ^ { t } ) ^ { \dagger } = \operatorname* { m a x } \{ \widehat { \varepsilon } , R _ { s , n } ( ( \lambda _ { s } ^ { t } ) ^ { \dagger } ) \} , n \in N _ { i } , s \in S _ { i } \right.\tag{33}
$$

Where $\widehat { \varepsilon } = \operatorname* { m a x } \{ \varepsilon , \alpha _ { s , n } ^ { t , \mathrm { m i n } } \}$ , and $R _ { s , n } ( \lambda _ { s } ^ { t } )$ represents the root of $\begin{array} { r } { \frac { \partial L ( \alpha _ { s , n } ^ { t } , \lambda _ { s } ^ { t } ) } { \partial \alpha _ { s , n } ^ { t } } = 0 } \end{array}$ . The following proposition provides a closed-form expression for $R _ { s , n } ( \lambda _ { s } ^ { t } )$   
Proposition 1: Given $\lambda _ { s } ^ { t } \ge 0$ Ã° Ã, the root of $\frac { \partial L ( \alpha _ { s , n } ^ { t } , \lambda _ { s } ^ { t } ) } { \partial \alpha _ { s , n } ^ { t } } = 0$ is non-negative and unique.

$$
R _ { s , n } ( \lambda _ { s } ^ { t } ) = \frac { r _ { s , n } ^ { t } \ln ( 2 ) } { 2 W _ { s } \tau \omega \left( \frac { r _ { s , n } ^ { t } \ln ( 2 ) } { 2 W _ { s } \tau } \sqrt { \frac { \lambda _ { s } ^ { t } h _ { s , n } ^ { t } W _ { s } \tau } { \sigma _ { s } ^ { 2 } r _ { s , n } ^ { t } \ln ( 2 ) } } \right) }\tag{34}
$$

Where $\omega ( \cdot )$ represents the lambert-w function. Note that $\frac { \partial L ( \alpha _ { s , n } ^ { t } , \lambda _ { s } ^ { t } ) } { \partial \alpha _ { s , n } ^ { t } }$ is a monotonic function of $\alpha _ { s , n } ^ { t } ,$ , hence $\left( \lambda _ { s } ^ { t } \right) ^ { \dagger }$ can be found using a bisection method within the interval

$\begin{array} { r l } { [ \lambda _ { s } ^ { L } ( t ) ; } & { { } \lambda _ { s } ^ { U } ( t ) ] } \end{array}$ . The selected $\lambda _ { s } ^ { L } ( t )$ and $\lambda _ { s } ^ { U } ( t )$ ensure   
that $\displaystyle \sum$ max $\{ \widehat \varepsilon , R _ { s , n } ( \lambda _ { s } ^ { L } ( t ) ) \} > 1$ and $\sum _ { n \in N _ { i } , s \in S _ { i } }$ max $\textstyle \left\{ { \widehat { \varepsilon } } , \right.$ n N, s Si   
$R _ { s , n } ( \lambda _ { s } ^ { U } ( t ) ) \} < 1$ . The calculation method for $\lambda _ { s } ^ { L } ( t )$ and   
$\lambda _ { s } ^ { U } ( t )$ is shown below.

$$
\left\{ \begin{array} { l } { \displaystyle \lambda _ { s } ^ { L } ( t ) = \operatorname* { m a x } _ { n \in N _ { i } , s \in S _ { i } } \frac { - \partial E _ { m i x } ^ { L , T r a n s } ( t ) } { \partial \alpha _ { s , n } ^ { t } } \bigg \vert _ { \alpha _ { s , n } ^ { t } = 1 } } \\ { \displaystyle \lambda _ { s } ^ { U } ( t ) = \operatorname* { m a x } _ { n \in N _ { i } , s \in S _ { i } } \frac { - \partial E _ { m i x } ^ { L , T r a n s } ( t ) } { \partial \alpha _ { s , n } ^ { t } } \bigg \vert _ { \alpha _ { s , n } ^ { t } = \hat { \varepsilon } } } \end{array} \right.\tag{35}
$$

When $\left| \sum _ { n \in N _ { i } , s \in S _ { i } } \operatorname* { m a x } \{ \widehat { \varepsilon } , R _ { s , n } ( \lambda _ { s } ^ { U } ( t ) ) \} - 1 \right| < \eta ,$ the search

process for $\left( \lambda _ { s } ^ { t } \right) ^ { \dagger }$ terminates, with  representing the search precision.

2) Optimization on Userâs Local Computation: Given the offloading volume for each user, the local computation resource allocation problem can be decomposed into independent subproblems for each user.

$$
P 2 . 3 \qquad \operatorname* { m i n } _ { f _ { n } ^ { t } } \sum _ { n \in N _ { i } } ( - Q _ { n } ^ { L } ( t ) \tau f _ { n } ^ { t } L _ { n } ^ { - 1 } + V \xi _ { \mathfrak { n } } ( f _ { n } ^ { t } ) ^ { 3 } )\tag{36}
$$

$$
s . t . \qquad 0 \leq { f } _ { n } ^ { t } \leq { f } _ { n } ^ { \operatorname* { m a x } } , n \in N _ { i } , t \in T\tag{37a}
$$

$$
l _ { n } ^ { t } \leq Q _ { n } ^ { l } ( t ) - ( r _ { s , n } ^ { t } ) ^ { \dagger } , n \in N _ { i } , s \in S _ { i }\tag{37b}
$$

Itâs evident that equation (36) represents a convex problem with all constraints being linear. Specifically, the optimal solution to problem P2.3 either lies at a stationary point of the objective function (36) or at a boundary point of the feasible region $\begin{array} { r } { ( f _ { n } ^ { t } ) ^ { \dagger } = \operatorname* { m i n } \Bigl \{ F _ { n } , \sqrt { \frac { Q _ { n } ^ { L } ( t ) \tau } { 3 \xi _ { n } V L _ { n } } } \Bigr \} , n \in N _ { i } } \end{array}$ , where $F _ { n } =$ min $\{ f _ { n } ^ { \mathrm { m a x } } , ~ ( Q _ { n } ^ { L } ( t ) - { ( r _ { s , n } ^ { t } ) } ^ { \dagger } ) L _ { n } / \tau \}$

3) Optimization on UAV-MEC Computational Resource Scheduling: Similar to the optimization of local computation resources for each user, the optimization of UAV-MEC computing frequency $f _ { s } ^ { \dagger } ( t )$ can be obtained by solving problem P2.4.

$$
\begin{array} { r l } & { \underset { f _ { s } ^ { \dagger } ( t ) } { \mathrm { m i n } } \displaystyle \sum _ { n \in N _ { i } , s \in S _ { i } } - Q _ { s } ^ { U } ( t ) \tau f _ { s , n } ^ { t } L _ { s } ^ { - 1 } + } \\ { P 2 . 4 } \end{array}\tag{38}
$$

$$
s . t . \quad \quad 0 \leq f _ { s , n } ^ { t } \leq f _ { s } ^ { \operatorname* { m a x } } , n \in N _ { i } , s \in S _ { i }\tag{39a}
$$

$$
\tau f _ { s , n } ^ { t } L _ { s } ^ { - 1 } \leq Q _ { s } ^ { U } ( t ) , n \in N _ { i } , s \in S _ { i }\tag{39b}
$$

The solution of P2.4 is similar to that of P2.3. Specifically, the optimal solution of problem P2.4 is either at the stationary point of the objective function (38) or at some boundary point of $\begin{array} { r } { ( f _ { s , n } ^ { t } ) ^ { \dagger } = \operatorname* { m i n } \Bigl \{ f _ { s , n } ^ { \operatorname* { m a x } } , \sqrt { \frac { Q _ { s } ^ { U } ( t ) \tau } { 3 \xi _ { s } V L _ { s } } } \Bigr \} , n \in N _ { i } , s \in S _ { i } } \end{array}$ , where $f _ { s , n } ^ { \operatorname* { m a x } } = \operatorname* { m i n } \{ f _ { s } ^ { \operatorname* { m a x } } , ~ Q _ { s } ^ { U } ( t ) L _ { s } / \tau \}$

## C. Generator Optimization Strategy

After optimization through DROA, the sub-optimal decision is generated. At this time, GOS treats the optimized offloading decisions as labels and the TCAG-generated sub-optimal channel allocations as input data. The binary cross-entropy loss function is employed to calculate the loss, providing a basis for analyzing TCAGâs predictive capabilities. Additionally, both the labels and data are stored in a fixed-size experience pool, providing a solid foundation for model updates, iterations, and optimizations. Specifically, the system is configured to randomly sample a portion of data from the experience pool after a fixed number of iterations and apply normalization to the sampled data. This batch of data is then utilized to train the TCAG and update its model parameters, improving the accuracy of the generator model in subsequent predictions.

## D. Computational Complexity Analysis

The computation mainly comes from DROA, as this component has to examine k TCAG-generated potential channel allocation decisions in each time slot and select the best one among them.

The complexity of joint optimization on offloading volume and bandwidth allocation: After given the feasible offloading volume, each UAV-MEC server needs $O ( \log _ { 2 } ( N _ { i } / \eta ) )$ iterations to Ã° Ã° gÃÃfind the optimal bandwidth allocation. Given a feasible bandwidth allocation, the optimization of the offload volume per user can be obtained in closed form. Thus, the complexity is in $O ( N _ { i } )$ considering $N _ { i }$ users. Finally, the complexity of gaussÃ° Ãseidel joint optimization is $O ( I _ { \mathrm { m a x } } ( N _ { i } + \log _ { 2 } ( N _ { i } / \eta ) ) ) ~ ( I _ { \mathrm { m a x } }$ is Ã°the maximum number of iterations).

The complexity of optimization on the computation of the user and the UAV-MEC server: Since solutions to P2.3 and P2.4 can both be obtained in closed forms, the optimization is with complexity O 1 for each user.

Ã° ÃIn summary, the complexity of each UAV-MEC server evaluating a channel allocation decision is $O ( I _ { \operatorname* { m a x } } ( N _ { i } + \log _ { 2 } ( N _ { i } / \eta ) ) )$ . Ã° Ã° Ã¾ Ã° gÃÃÃSince DROA examines k potential decisions at each time slot, the overall computational complexity of the proposed method is $O ( k I _ { \mathrm { m a x } } ( \sum _ { i = 1 } ^ { s } N _ { i } + \sum _ { i = 1 } ^ { s } \log _ { 2 } ( N _ { i } / \eta ) ) )$

## V. SIMULATIONS AND PERFORMANCE EVALUATIONS

## A. Parameter Settings

We set the UAV takeoff position at a distance of 2 km from the center of the service area. The maximum number of connections for each UAV-MEC server is set to 2. For all users, their tasks follow a poisson distribution, denoted as $E ( A _ { n } ^ { t } ) = 1 5 \mathrm { k b } ;$ Ã° Ã Â¼N  40;   6:03125; a1 13:0397; a2 196:849; $b _ { 1 } =$ Â¼ w Â¼ Â¼ Â¼ Â¼â16:9396; b2 216:6944; b3 â157:9473; c1 4:6817; Â¼ Â¼ Â¼c2  â11:9708; c3  135:3118; Mg  9:65kg;   10ms; Â¼ Â¼ Â¼ s Â¼f maxs 4GHz; Ws 4GHz; f maxn 1GHz; N0 â174dBm=Hz; $L _ { n } = L _ { s } = 7 3 7$ Â¼ Â¼ Â¼:5cycles=bit; Qth Qth 45kb; k  16; V  1 $1 0 ^ { 9 } ; \xi _ { n } = \xi _ { s } = 1 0 ^ { - 2 8 } \mathrm { W s ^ { 3 } / c y c l e ^ { 3 } }$

## B. Comparison Method Setup

To demonstrate the effectiveness of our proposed method, we compare it with four different methods. These methods are as follows:

1) Deep Reinforcement Learning (DRL): Derived from recent study [30] that publicly released simulation code.

<!-- image-->  
(a) Long-term average queue length of users

<!-- image-->  
(b) Long-term average queue length of UAV-MEC servers

<!-- image-->  
(c) Long-term average power consumption of UAV-MEC servers

<!-- image-->  
(d) Long-term average system power consumption

Fig. 6. Comparison of different methods under scenario I.  
<!-- image-->  
(a) Total number of UAVs

<!-- image-->  
(b) Number of UAVs joining

<!-- image-->  
(c) Number of UAVs exiting  
Fig. 7. Change in the number of UAVs in scenario II.

2) Exhaustive Search Method (Exhaustive): Exploring all possible combinations of channel allocation and resource scheduling to select the best-performing decision.

3) Channel Gain-based Greedy Strategy (CG-based): This strategy adopts an intuitive greedy approach, prioritizing communication resources for users with the highest channel gains.

4) Random Allocation Strategy (Random): The random allocation strategy assigns users to UAVs for communication and performs corresponding resource scheduling randomly.

## C. Performance Evaluation

To systematically and comprehensively evaluate the suboptimality and convergence characteristics of the proposed method, we set scenario I (i.e., a 30-minute service cycle, with the UAV battery capacity for one hour of hovering flight). In this scenario, we specifically observed the long-term average queue length of users $\underset { N \times T } { \sum _ { n = 1 } ^ { N } \sum _ { t = 1 } ^ { T } } Q _ { n } ^ { L } ( t )$ , the long-term average queue length of UAV-MEC servers $\underset { S \times T } { \sum _ { s = 1 } ^ { S } \sum _ { t = 1 } ^ { T } } Q _ { s } ^ { U } ( t )$ , the long-term average power consumption of UAV-MEC servers $\underset { \leq \times T } { \sum _ { s = 1 } ^ { S } \sum _ { t = 1 } ^ { T } } E _ { m i x } ^ { s } ( t )$ , and the long-term average system power consumption $\underset { ( \frac { t = 1 } { T } } { \overset { T } { \sum } } E _ { m i x } ^ { T o t a l } ( t )$ excluding UAV flight power consumption (Note: Once the system requires additional UAV support, this method will inevitably become suboptimal, as the flight power consumption far exceeds the total computational offloading power consumption). From Fig. 6(a), the Random and CG-Based methods initially show high levels, followed by a gradual decline. This phenomenon is attributed to their dynamic introduction of a new UAV into the network for offloading. In contrast, both our proposed method and the Exhaustive method demonstrate more stable queue length growth, with minimal differences between them. The DRL method introduces a new UAV for offloading from the start, but it exhibits significant long-term queue length growth. From Fig. 6(b), our proposed method and the Exhaustive method perform similarly, both maintaining stable states. From Fig. 6(c), we observe that the Random, CG-Based, and DRL methods are higher than the other two methods. From Fig. 6(d), our proposed method and the Exhaustive method yield similar results, indicating that our method effectively control overall system power consumption while maintaining service quality. In conclusion, our proposed method demonstrates energy consumption performance comparable to the Exhaustive method, while maintaining stability in both the user and UAV-MEC server queues, thereby validating its superiority and practicality.

<!-- image-->  
Fig. 8. CPU resource utilization comparison.

To visually demonstrate the entry and exit behavior of UAVs, we set the UAV battery capacity to support 30 minutes of hovering flight (scenario II). From Fig. 7(a), our proposed method and the Exhaustive method consistently maintain a stable number of 5 UAVs. In contrast, the DRL, CG-Based, and Random methods increase the number of UAVs to 6 at different timesâ1 minute, 3 minutes, and 4 minutes after the service begins, respectively. From Fig. 7(b) and 7(c), we observed that at 14 minutes and 24 minutes, pairs of UAVs joined and exited, which was caused by the battery running low. This behavior demonstrates the effectiveness of the microservice management component.

<!-- image-->  
(a)Long-term average queue length of users

<!-- image-->  
(b) Long-term average queue length of UAV-MEC servers

<!-- image-->  
(c)Long-term average system power consumption

Fig. 9. Influence of control parameter V on long-term queues and long-term power consumption.  
<!-- image-->  
(a) Long-term average queue length of users

<!-- image-->  
(b) Long-term average power consumption of UAV-MEC servers

<!-- image-->  
(c)Long-term average system power consumption  
Fig. 10. Effect of TransformerBlock layers on long-term queue and long-term power consumption in TCAG.

## D. Comparison With the Overhead of the Exhaustive

To further demonstrate the superiority of the proposed method, we compared the CPU resource utilization of the Exhaustive method during system operation. The simulation results are shown in Fig. 8. The proposed method exhibits lower CPU resource overhead on all five UAV-MEC servers compared to the Exhaustive method. Specifically, the difference is more pronounced on UAV-MEC servers 3 and 5 (About 5%). It is worth noting that, under the current settings, the computational complexity of the proposed method for each UAV-MEC server is $O ( k I _ { \operatorname* { m a x } } ( N _ { i } + \log _ { 2 } ( N _ { i } / \eta ) ) )$ , where the parameter k is set to 16. In Ã° Ã° Ã¾ Ã° gÃÃÃcontrast, the computational complexity of the Exhaustive method exhibits significantly different characteristics. Since the maximum number of connections for each UAV-MEC server is limited to 2, in a scenario where the number of users is Ni, the parameter k of the Exhaustive method can be expressed as $k = C _ { N _ { i } } ^ { 2 }$ . This charac-Â¼teristic causes the computational complexity of the Exhaustive method to increase rapidly as the number of users grows. When the above conditions are determined, calculations show that when $N _ { i } = 6 ,$ , the computational complexity of both the proposed Â¼method and the Exhaustive method become numerically similar. However, when the Exhaustive method is applied to larger-scale rescue scenarios, with more user connection requirements and wider user distribution, its computational complexity increases dramatically, making the consumption of computing resources unsustainable. In summary, our method is more efficient in resource utilization, reducing the CPU burden under the same conditions and improving the overall operational efficiency of the system.

## E. Influence Analysis of Important Parameters

1) Effect of the Parameter V: In Fig. 9, we investigate the impact of different sizes of the parameter V on various system performance metrics, with all other settings remaining consistent with the conditions of scenario I. From Fig. 9(a) and 9(b), we observe that smaller values of V have a greater impact on the queue, stabilizing the queue length at a lower level. However, as seen in Fig. 9(c), larger values of V place more weight on power consumption, resulting in lower power consumption.

2) Effect of TransformerBlock Layers: In Fig. 10, we investigate the impact of the number of TransformerBlock layers on queue and power consumption. From Fig. 10(a) and 10(b), it is evident that a smaller number of TransformerBlock layers has opposite effects on the two queues. In contrast, when the number of TransformerBlock layers is appropriate, the two queues remain relatively stable. From Fig. 10(c), An appropriate number of TransformerBlock layers has a positive effect on reducing system power consumption. Therefore, it is essential to find a balance between model complexity and system power consumption during the design process. Additionally, we analyzed the effect of the number of TransformerBlock layers on inference speed, and the results are shown in Fig. 11. As the number of layers increases, the average inference time of TCAG gradually increases. Therefore, in practical applications, it is necessary to balance model complexity and inference speed to ensure efficient inference while improving model performance.

<!-- image-->  
Fig. 11. Effect of TransformerBlock layers on inference time.

## VI. CONCLUSION

In response to the urgent needs of emergency medical rescue after natural disasters, we proposed a UAV-assisted microservice MEC architecture. This architecture leverages the flexibility and mobility of UAVs, the modularity and rapid scalability of the microservice framework, and the efficiency of lightweight neural network models. It aims to provide stable, efficient, realtime computing and data support for rescue operations in scenarios where network and power infrastructure are damaged by natural disasters. The architecture ensures long-term stability through mechanisms for self-organizing networks and the automatic management of UAVs joining and exiting. Additionally, the TBRM method effectively balances data offloading, energy consumption, and latency, thereby maximizing the architectureâs service time. Furthermore, we design four microservices to manage the full UAV lifecycle and introduce dual digital signature certificates to enhance system security. Extensive simulation results demonstrate the effectiveness of the proposed method. We also provide recommendations for key parameter settings, which further verify its feasibility in real rescue environments. In summary, this study provides a technological support solution for post-disaster emergency medical rescue, with both theoretical significance and practical value.

## REFERENCES

[1] C. Luo, J. Zhang, X. Cheng, Y. Hong, Z. Chen, and X. Xing, âComputation off-loading in resource-constrained edge computing systems based on deep reinforcement learning,â IEEE Trans. Comput., vol. 73, no. 1, pp. 109â122, Jan. 2024.

[2] H. Lin, L. Yang, H. Guo, and J. Cao, âDecentralized task offloading in edge computing: An offline-to-online reinforcement learning approach,â IEEE Trans. Comput., vol. 73, no. 6, pp. 1603â1615, Jun. 2024.

[3] D. Zhang, Z. Zhang, J. Zhang, T. Zhang, L. Zhang, and H. Chen, âUavassisted task offloading system using dung beetle optimization algorithm & deep reinforcement learning,â Ad Hoc Netw., vol. 156, 2024, Art. no. 103434. [Online]. Available: https://www.sciencedirect.com/science/article/ pii/S1570870524000453

[4] H. Sun, X. Zhang, B. Zhang, K. Sha, and W. Shi, âOptimal task offloading and trajectory planning algorithms for collaborative video analytics with UAV-assisted edge in disaster rescue,â IEEE Trans. Veh. Technol., vol. 73, no. 5, pp. 6811â6828, May 2024.

[5] H. Zeng, Z. Zhu, Y. Wang, Z. Xiang, and H. Gao, âPeriodic collaboration and real-time dispatch using an actorâcritic framework for UAV movement in mobile edge computing,â IEEE Internet Things J., vol. 11, no. 12, pp. 21 215â21 226, Jun. 2024.

[6] H. Wang, H. Xu, H. Huang, M. Chen, and S. Chen, âRobust task offloading in dynamic edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 500â514, Jan. 2023.

[7] F. Li, J. Luo, Y. Qiao, and Y. Li, âJoint uav deployment and task offloading scheme for multi-UAV-assisted edge computing,â Drones, vol. 7, no. 5, p. 284, 2023. [Online]. Available: https://www.mdpi.com/ 2504-446X/7/5/284

[8] K. Cheng, X. Fang, and X. Wang, âEnergy efficient edge computing and data compression collaboration scheme for UAV-assisted network,â IEEE Trans. Veh. Technol., vol. 72, no. 12, pp. 16 395â16 408, Dec. 2023.

[9] B. Xu, Z. Kuang, J. Gao, L. Zhao, and C. Wu, âJoint offloading decision and trajectory design for uav-enabled edge computing with task dependency,â IEEE Trans. Wireless Commun., vol. 22, no. 8, pp. 5043â5055, Aug. 2023.

[10] A. Krizhevsky, I. Sutskever, and G. E. Hinton, âImagenet classification with deep convolutional neural networks,â Commun. ACM, vol. 60, no. 6, pp. 84â90, May 2017, doi: 10.1145/3065386.

[11] K. Simonyan and A. Zisserman, âVery deep convolutional networks for large-scale image recognition,â 2014, arXiv:1409.1556.

[12] K. He, X. Zhang, S. Ren, and J. Sun, âDeep residual learning for image recognition,â in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2016, pp. 770â778.

[13] A. Howard et al., âSearching for mobilenetv3,â in Proc. IEEE/CVF Int. Conf. Comput. Vis., 2019, pp. 1314â1324.

[14] N. Ma, X. Zhang, H.-T. Zheng, and J. Sun, âShufflenet v2: Practical guidelines for efficient cnn architecture design,â in Proc. Eur. Conf. Comput. Vis. (ECCV), 2018, pp. 116â131.

[15] A. Vaswani et al., âAttention is all you need,â in Advances in Neural Information Processing Systems, vol. 30, Long Beach, CA, USA: Curran Associates, Inc., 2017.

[16] K. Cheng et al., âProScale: Proactive autoscaling for microservice with time-varying workload at the edge,â IEEE Trans. Parallel Distrib. Syst., vol. 34, no. 4, pp. 1294â1312, Apr. 2023.

[17] Y. Zhao, J. Wang, and B. Li, âA deep reinforcement learning approach to online microservice deployment in mobile edge computing,â in Proc. Int. Conf. Service-Oriented Comput., Cham: Springer, 2023, pp. 127â142.

[18] M. D. Hossain et al., âThe role of microservice approach in edge computing: Opportunities, challenges, and research directions,â ICT Exp., vol. 9, no. 6, pp. 1162â1182, 2023. [Online]. Available: https:// www.sciencedirect.com/science/article/pii/S2405959523000760

[19] F. Liu, Y. Guo, Z. Cai, N. Xiao, and Z. Zhao, âEdge-enabled disaster rescue: A case study of searching for missing people,â vol. 10, no. 6, pp. 1â21, Dec. 2019. [Online]. Available: https://doi.org/10.1145/3331146

[20] S. Mao, S. He, and J. Wu, âJoint UAV position optimization and resource scheduling in space-air-ground integrated networks with mixed cloud-edge computing,â IEEE Syst. J., vol. 15, no. 3, pp. 3992â4002, Sep. 2021.

[21] S. H. Alsamhi et al., âUAV computing-assisted search and rescue mission framework for disaster and harsh environment mitigation,â Drones, vol. 6, no. 7, p. 154, 2022. [Online]. Available: https://www. mdpi.com/2504-446X/6/7/154

[22] G. Faraci, S. A. Rizzo, and G. Schembra, âGreen edge intelligence for smart management of a fanet in disaster-recovery scenarios,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 3819â3831, Mar. 2023.

[23] H. Zhang et al., âDecentralized and fault-tolerant task offloading for enabling network edge intelligence,â IEEE Syst. J., vol. 18, no. 2, pp. 1459â1470, Jun. 2024.

[24] B. Cen et al., âA configuration method of computing resources for microservice-based edge computing apparatus in smart distribution transformer area,â Int. J. Electr. Power Energy Syst., vol. 138, 2022, Art. no. 107935. [Online]. Available: https://www.sciencedirect.com/ science/article/pii/S0142061521011455

[25] F. Guo, B. Tang, and M. Tang, âJoint optimization of delay and cost for microservice composition in mobile edge computing,â World Wide Web, vol. 25, no. 5, pp. 2019â2047, 2022.

[26] W. Lv et al., âMicroservice deployment in edge computing based on deep q learning,â IEEE Trans. Parallel Distrib. Syst., vol. 33, no. 11, pp. 2968â2978, Nov. 2022.

[27] F. Guo, B. Tang, M. Tang, and W. Liang, âDeep reinforcement learning-based microservice selection in mobile edge computing,â Cluster Comput., vol. 26, no. 2, pp. 1319â1335, 2023.

[28] B. Tang, F. Guo, B. Cao, M. Tang, and K. Li, âCost-aware deployment of microservices for IoT applications in mobile edge computing environment,â IEEE Trans. Netw. Service Manag., vol. 20, no. 3, pp. 3119â3134, Sep. 2023.

[29] K. Ray, A. Banerjee, and N. C. Narendra, âLearning-based microservice placement and migration for multi-access edge computing,â IEEE Trans. Netw. Service Manag., vol. 21, no. 2, pp. 1969â1982, Apr. 2024.

[30] L. T. Hoang, C. T. Nguyen, and A. T. Pham, âDeep reinforcement learning-based online resource management for UAV-assisted edge computing with dual connectivity,â IEEE/ACM Trans. Netw., vol. 31, no. 6, pp. 2761â2776, Dec. 2023.

[31] Y. Zhang, C. Chen, L. Liu, D. Lan, H. Jiang, and S. Wan, âAerial edge computing on orbit: A task offloading and allocation scheme,â IEEE Trans. Netw. Sci. Eng., vol. 10, no. 1, pp. 275â285, Jan./Feb. 2023.

[32] Y. Ding et al., âOnline edge learning offloading and resource management for UAV-assisted MEC secure communications,â IEEE J. Sel. Topics Signal Process., vol. 17, no. 1, pp. 54â65, Jan. 2023.

[33] M. K. Hasan et al., âFederated learning for computational offloading and resource management of vehicular edge computing in 6g-v2x network,â IEEE Trans. Consum. Electron., vol. 70, no. 1, pp. 3827â3847, Feb. 2024.

[34] H. Zhang, J. Wang, H. Zhang, and C. Bu, âSecurity computing resource allocation based on deep reinforcement learning in serverless multicloud edge computing,â Future Gener. Comput. Syst., vol. 151, pp. 152â 161, 2024.

[35] Zhang, Y. Mobile Edge Computing. Berlin, Germany: Springer Nature, 2022.

[36] Y. Dai, D. Xu, S. Maharjan, and Y. Zhang, âJoint computation offloading and user association in multi-task mobile edge computing,â IEEE Trans. Veh. Technol., vol. 67, no. 12, pp. 12 313â12 325, 2018.

[37] S. Jeong, O. Simeone, and J. Kang, âMobile edge computing via a UAV-mounted cloudlet: Optimization of bit allocation and path planning,â IEEE Trans. Veh. Technol., vol. 67, no. 3, pp. 2049â2063, Mar. 2018.

[38] J. Zhang et al., âStochastic computation offloading and trajectory scheduling for UAV-assisted mobile edge computing,â IEEE Internet Things J., vol. 6, no. 2, pp. 3688â3699, Apr. 2019.

[39] H. V. Abeywickrama, B. A. Jayawickrama, Y. He, and E. Dutkiewicz, âEmpirical power consumption model for UAVs,â in Proc. IEEE 88th Veh. Technol. Conf. (VTC-Fall), Piscataway, NJ, USA: IEEE Press, 2018, pp. 1â5.

<!-- image-->  
Ji Li received the B.S. and M.S. degrees from Taiyuan University of Science and Technology, China, He is currently working toward the Ph.D. degree with the Northeastern University, Shenyang, China. His research interests include social network, edge computing, and computer vision.

<!-- image-->

<!-- image-->

Xingwei Wang received the B.S., M.S., and Ph.D. degrees in computer science from the Northeastern University, Shenyang, China, in 1989, 1992, and 1998, respectively. Currently, he is a Professor with the College of Computer Science and Engineering, Northeastern University, Shenyang, China. His research interests include cloud computing and future Internet.

<!-- image-->

Keping Yu (Senior Member, IEEE) received the M.E. and Ph.D. degrees from the Graduate School of Global Information and Telecommunication Studies, Waseda University, Japan, in 2012 and 2016, respectively. He was a Research Associate, a Junior Researcher, a Researcher with the Global Information and Telecommunication Institute, Waseda University, from 2015 to 2019, 2019 to 2020, and 2020 to 2022, respectively. Currently, he is an Associate Professor, the Vice Director of Institute of Integrated Science and Technology, and the Director of the

Qiang He (Associate Member, IEEE) received the Ph.D. degree in computer application technology from the Northeastern University, Shenyang, China, in 2020. He also worked with the School of Computer Science and Technology, Nanyang Technical University, Singapore as a visiting Ph.D. Researcher from 2018 to 2019. Currently, he is an Associated Professor with the College of Medicine and Biological Information Engineering, Northeastern University, Shenyang, China. His research interests include machine learning, social network analytic, data min-

Ammar Hawbani received the B.S., M.S., and Ph.D. degrees in computer software and theory from the University of Science and Technology of China (USTC), Hefei, China, in 2009, 2012, and 2016, respectively. He is an Associate Professor of networking and communication algorithms with the School of Computer Science and Technology, USTC. From 2016 to 2019, he worked as a Postdoctoral Researcher with the School of Computer Science and Technology, USTC.

Network Intelligence and Security Laboratory (YU Lab), Hosei University, Japan.

ing, health care, infectious diseases informatics, etc.

<!-- image-->

<!-- image-->

Yuanguo Bi (Member, IEEE) received the Ph.D. degree in computer science and technology from the Northeastern University, Shenyang, China, in 2010. He was a visiting Ph.D. student with the BroadBand Communications Research (BBCR) Lab, Department of Electrical and Computer Engineering, University of Waterloo, Waterloo, ON, Canada, from 2007 to 2009. Currently, he is a Professor with the School of Computer Science and Engineering, Northeastern University, China.

<!-- image-->

Liang Zhao received the Ph.D. degree from the School of Computing, Edinburgh Napier University, in 2011. He is a Professor with Shenyang Aerospace University, China. Before joining Shenyang Aerospace University, he worked as an Associate Senior Researcher with Hitachi (China) Research and Development Corporation, from 2012 to 2014. He is also a JSPS Invitational Fellow (2023).

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue/page_6_img_1.jpeg|page_6_img_1]]
2. [[../extracted_images/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue/page_14_img_1.png|page_14_img_1]]
3. [[../extracted_images/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue/page_14_img_2.jpeg|page_14_img_2]]
4. [[../extracted_images/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue/page_14_img_3.jpeg|page_14_img_3]]
5. [[../extracted_images/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue/page_14_img_4.jpeg|page_14_img_4]]
6. [[../extracted_images/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue/page_14_img_5.jpeg|page_14_img_5]]
7. [[../extracted_images/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue/page_14_img_6.jpeg|page_14_img_6]]
8. [[../extracted_images/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue/page_14_img_7.jpeg|page_14_img_7]]

---

