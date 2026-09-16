# Wireless Powered Metaverse: Joint Task Scheduling and Trajectory Design for Multi-Devices and Multi-UAVs

Xiaojie Wang , Senior Member, IEEE, Jiameng Li, Zhaolong Ning , Senior Member, IEEE, Qingyang Song , Senior Member, IEEE, Lei Guo , and Abbas Jamalipour , Fellow, IEEE

Abstractâ To support the running of human-centric metaverse applications on mobile devices, Unmanned Aerial Vehicle (UAV)- assisted Wireless Powered Mobile Edge Computing (WPMEC) is promising to compensate for limited computational capabilities and energy supplies of mobile devices. The high-speed computational processing demands and significant energy consumption of metaverse applications require joint resource scheduling of multiple devices and UAVs, but existing WPMEC solutions address either device or UAV scheduling due to the complexity of combinatorial optimization. To solve the above challenge, we propose a two-stage alternating optimization algorithm based on multi-task Deep Reinforcement Learning (DRL) to jointly allocate charging time, schedule computation tasks, and optimize trajectory of UAVs and mobile devices in a wireless powered metaverse scenario. First, considering energy constraints of both UAVs and mobile devices, we formulate an optimization problem to maximize the computation efficiency of the system. Second, we propose a heuristic algorithm to efficiently perform time allocation and charging scheduling for mobile devices. Following this, we design a multi-task DRL scheme to make charging scheduling and trajectory design decisions for UAVs. Finally, theoretical analysis and performance results demonstrate that our algorithm exhibits significant advantages over representative methods in terms of convergence speed and average computation efficiency.

Index Termsâ Human centric metaverse, wireless powered mobile edge computing, unmanned aerial vehicles, multi-task deep reinforcement learning.

Manuscript received 15 March 2023; revised 1 August 2023; accepted 31 August 2023. Date of publication 21 December 2023; date of current version 1 March 2024. This work was supported in part by the Natural Science Foundation of China under Grant 61971084, Grant 62025105, Grant 62001073, Grant 62221005, and Grant 62272075; in part by the National Natural Science Foundation of Chongqing under Grant CSTB2022BSXM-JCX0109 and Grant CSTB2022BSXMJCX0110; in part by the Science and Technology Research Program for Chongqing Municipal Education Commission under Grant KJZD-K202300608 and Grant KJZDM202200601; in part by the Support Program for Overseas Students to Return to China for Entrepreneurship and Innovation under Grant cx2021003 and Grant cx2021053; and in part by the Youth Innovation Group Support Program of Information and Communication Engineering (ICE) Discipline of Chongqing University of Posts and Telecommunications (CQUPT) under Grant SCIE-QN-2022-03. (Corresponding author: Zhaolong Ning.)

## I. INTRODUCTION

HE metaverse, referred as the successor of mobile Inter-T net [1], is gaining popularity as a concept. It is the materialized version of the Internet, which includes a humancentric, immersive, and interoperable virtual ecosystem that can be navigated by virtual characters controlled by users [2]. In the metaverse, users can interact with the virtual world through body movements or sound, and experience comprehensive human-centric virtual services. For example, users can explore the virtual world in the metaverse with the help of technologies such as virtual reality, augmented reality and mixed reality. However, the key characteristic of these technologies is timely rendering of images to quickly generate perceptual images based on usersâ thoughts, requiring devices to have high computing capability and sufficient energy.

With the development of metaverse-related technologies and the rising demand of users to perceive virtual worlds dynamically in real time, traditional wired devices cannot realize ubiquitous network access to the metaverse. Instead, running programs developed for the metaverse at mobile devices held by users can create a human-centric and dynamic virtual world perceiving usersâ needs in real time [1]. Each user creates his customized avatar and interacts with other avatars and digital objects for a more realistic experience in the metaverse anytime and anywhere, inevitably posing significant challenges to the computing capability and battery capacity of each terminal.

Currently, due to production costs and technological limitations, computing capability and battery life of mobile devices are always constrained [3]. In recent years, Mobile Edge Computing (MEC) [4] has been regarded as a key solution to support real-time rendering and become one of the feasible solutions to provide real-time virtual reality videos through wireless networks. It works as a strong supplement to the computing capability of mobile devices by offloading computation tasks to nearby MEC servers [5]. Additionally, with the development of Wireless Power Transfer (WPT) technology, the energy constraint of mobile devices has been alleviated. Therefore, with the integration of WPT and MEC, Wireless Powered Mobile Edge Computing (WPMEC) lifts the burden of battery life while enhancing the computing capability for sustaining the metaverse [6]. With the aid of the WPMEC technology, running human-centric programs developed for the metaverse at mobile devices becomes smooth

Digital Object Identifier 10.1109/JSAC.2023.3345433 and easy, and we refer to this paradigm as wireless powered metaverse.

Due to their flexibility and controllability, Unmanned Aerial Vehicles (UAVs) with controllable trajectories are often used as airborne edge servers that can dynamically provide computing services to mobile devices [7], [8]. Although some studies have discussed UAV-assisted WPMEC ( [9], [10], [11], [12]), they cannot be directly applied to support human-centric metaverse applications due to the following reasons:

â¢ First, there is an urgent requirement to provide timely energy supply and efficient allocation of network resources, especially when large-scale dynamic coexistence of mobile devices with metaverse access requirements. However, existing research usually only considers charging and task scheduling issues of mobile devices, while ignoring or simplifying the similar issues of UAVs. Therefore, it is necessary to design a novel trajectory optimization and task scheduling scheme for both UAVs and mobile devices.

â¢ Second, human-centric metaverse applications require significant computational resources and high computing speeds. However, the half-duplex characteristic of devices and the charging requirement of UAVs can cause instability in the amount of computational resources in a WPMEC network. Therefore, it is worth studying how to allocate the charging time of UAVs and mobile devices reasonably, to maximize the computation efficiency of the system.

â¢ Finally, to address the optimization problem of UAV-assisted WPMEC systems, existing research mostly adopts classical convex optimization methods or heuristic algorithms. However, in human-centric metaverse scenarios, multiple coupled scheduling parameters and rapidly changing network states make the traditional optimization algorithms inefficient. Therefore, to enable smooth operations of metaverse programs at mobile devices, efficient learning algorithms are needed for rational resource scheduling.

To address the above challenges, we propose a multitask deep reinforcement learning based two-stage alternating optimization algorithm, named MURAL, which can be applied to a multi-UAV-assisted WPMEC network with human-centric metaverse devices. With the optimization goal of maximizing the computation efficiency of the system, this algorithm allows for joint charging time allocation, computation offloading, and UAV trajectory design. To the best of our knowledge, this is the first work that considers joint charging time allocation, computation task scheduling and trajectory optimization for both UAVs and mobile devices. A summary of our contribution can be found below:

â¢ We construct a system model based on WPMEC, which allows simultaneous charging of both UAVs and mobile devices, providing support for the operation of programs developed for the metaverse. To achieve efficient utilization of system resources, we propose a novel time allocation model for UAVs and mobile devices by considering their half-duplex characteristics.

â¢ Given energy constraints of mobile devices and UAVs, we formulate an optimization problem for maximizing the long-term system computation efficiency. To solve this problem, we first decompose it into two subproblems: time allocation and charging scheduling for mobile devices, and charging scheduling and trajectory design for UAVs. We propose a two-stage alternating optimization algorithm based on multi-task Deep Reinforcement Learning (DRL) to solve these subproblems.

â¢ For the first subproblem, we design a heuristic and effective algorithm and theoretically prove the existence of an optimal solution. For the second subproblem, we propose a learning algorithm based on multi-task DRL to learn strategies for different UAVs, and theoretically show that the complexity of this approach is polynomial time.

â¢ We conduct performance evaluation of the designed algorithm based on the Manhattan city map and compare it against several representative algorithms. The evaluation results verify the effectiveness of our approach in terms of convergence speed, average computation efficiency, average numbers of computation bits and average energy consumption.

The rest of this paper is organized as follows: In Section II, we illustrate the related work; we construct the system model and formulate the optimization problem in Section III; In Section IV, we design the two-stage alternating optimization algorithm based on multi-task DRL; The performance evaluation is conducted in Section V; Finally, we conclude this work in Section VI.

## II. RELATED WORK

In this section, we review the related work including UAV-assisted WPMEC and multi-task DRL.

## A. UAV-Assisted WPMEC

Integrating UAV communication technology with WPMEC systems can mitigate the drawbacks of fixed energy supply and user mobility [9], [10], [11], [12]. Considering the randomness of energy and computation tasks in the spatial domain, authors in [9] investigated resource allocation of UAV-assisted WPMEC networks to minimize UAV energy consumption subject to stable data and energy queues. In [10], authors applied non-orthogonal multiple access and hybrid beamforming techniques to maximize the computation efficiency of UAV-assisted WPMEC systems. While the aforementioned studies focused on optimizing UAV trajectories and resource allocation for UAV-assisted WPMEC systems, none of them considered UAV charging scheduling.

Recently, a few researchers have utilized laser charging to alleviate energy consumption in UAV-assisted WPMEC networks. Authors in [11] designed a UAV-assisted user offloading scheme and employed laser charging for UAVs. They formulated a resource allocation and trajectory optimization problem, considering the UAVâs service time and task completion time. In addition, authors in [12] assumed UAVs as information and energy relay stations to assist with task offloading and energy transfer. Although the above studies considered the UAV charging issue, they only investigated a single UAV-assisted WPMEC network and used traditional optimization algorithms that are not suitable for dynamic environments.

## B. Multi-Task DRL

Due to the limitation of traditional DRL that only learns the control policies of a single task, and cannot solve multiple related problems simultaneously or sequentially with reasonable time consumption and satisfactory performance, researchers ([13], [14], [15]) have begun to explore multi-task DRL that allows agents to learn multiple sequential decision tasks at once and performs well on different tasks [15]. The multi-task DRL approach has the natural advantage of solving multiple tasks with the same structure and interconnections in parallel, and can increase the generalization capability of the model with shared knowledge learned by intelligences.

Distral [14] is a classic multi-task DRL approach that combines knowledge distillation and transfer learning, purifying strategies learned on each task to obtain a shared strategy, and then using this shared strategy to guide the strategy on each specific task for better learning. $\begin{array} { r l } { \pi _ { i } } & { { } = } \end{array}$ $( S , A , p _ { i } ( s ^ { \prime } | s , a ) , \gamma , R _ { i } ( a , s ) )$ denotes the policy for corresponding task i, and $\pi _ { 0 }$ represents the shared policy obtained after refinement of tasks $\{ \pi _ { i } \} _ { i = 1 } ^ { n }$ . Therefore, the objective to be maximized is defined as follows:

$$
\begin{array} { r l } & { J ( \pi _ { 0 } , \{ \pi _ { i } \} _ { i = 1 } ^ { n } ) } \\ & { \quad = \displaystyle \sum _ { i } \mathbb { E } _ { \pi _ { i } } \sum _ { t \geq 0 } \Big ( \gamma ^ { t } R _ { i } \left( a _ { t } | s _ { t } \right) - c _ { K L } \gamma ^ { t } \log \pi _ { 0 } \left( a _ { t } | s _ { t } \right) } \\ & { \quad \quad - \left( c _ { E n t } - c _ { K L } \right) \gamma ^ { t } \log \pi _ { i } \left( a _ { t } | s _ { t } \right) \Big ) , } \end{array}\tag{1}
$$

where variables $c _ { K L }$ and $c _ { E n t }$ are scalar factors determining the strengths of Kullback-Leibler (KL) and entropy regularization, respectively.

The multi-task DRL approach has a wide range of applications, such as the modelling of partial differential equations [16] and the embedding of knowledge graphs [17]. Authors in [18] proposed a parallel task scheduling algorithm based on multi-task DRL in the Internet of things, taking the correlation among tasks into account. Authors in [19] used a multi-task DRL algorithm based on graph convolutional networks to achieve network slicing and routing. In addition, authors in [20] proposed an intelligent resource allocation framework based on multi-task DRL to implement distributed computing. Although multi-task DRL has great potential in solving resource allocation problems of wireless networks, there has been little research on joint task scheduling and trajectory design based on multi-task DRL in UAV-assisted WPMEC networks.

In this paper, we propose MURAL, a joint scheduling algorithm suitable for multi-UAV assisted WPMEC networks, which is designed for mobile devices supporting for the running of human-centric programs developed for the metaverse and aims to maximize the computation efficiency of the system. To the best of our knowledge, this is the first work that considers joint charging time allocation, computation task scheduling and trajectory design for both UAVs and mobile devices.

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $q _ { m } ^ { t }$ </td><td>The coordinate of mobile device m in</td></tr><tr><td> $q _ { u } ^ { t }$ </td><td>time slot t; The coordinate of UAV u in time slot t;</td></tr><tr><td> $h _ { m u } ^ { t }$ </td><td>The channel gain between UAV u and</td></tr><tr><td></td><td>mobile device m in time slot t;</td></tr><tr><td> $\alpha _ { m } ^ { t }$ </td><td>The scheduling variable of device m in</td></tr><tr><td> $\beta _ { u } ^ { t }$ </td><td>time slot t; The scheduling variable of UAV u in</td></tr><tr><td></td><td>time slot t;</td></tr><tr><td> $\tau ^ { t }$ </td><td>The time allocation variable in time slot t;</td></tr><tr><td> $\varepsilon$ </td><td>The energy conversion efficiency of mobile devices;</td></tr><tr><td> $\epsilon$ </td><td>The energy conversion efficiency for UAVs;</td></tr><tr><td> $\mathcal { P } _ { 1 }$ </td><td>The transmission power of the laser;</td></tr><tr><td> $P _ { m }$ </td><td>The transmission power of device m;</td></tr><tr><td> $T$ </td><td>The duration of a time slot;</td></tr><tr><td> $C _ { 1 }$ </td><td>The number of CPU cycles required to</td></tr><tr><td> $f _ { m }$ </td><td>compute each data bit;</td></tr><tr><td> $f _ { u }$ </td><td>The CPU frequency of device m;</td></tr><tr><td> $k _ { m }$ </td><td>The CPU frequency of UAV u;</td></tr><tr><td></td><td>The coefficient related to the computation efficiency of device m;</td></tr><tr><td> $k _ { u }$ </td><td>The coefficient related to the computation</td></tr><tr><td></td><td>efficiency of UAV u;</td></tr><tr><td> $E _ { m } ^ { t , r }$ </td><td>The residual battery energy of mobile</td></tr><tr><td> $\mathbb { E } _ { u } ^ { t , r }$ </td><td>device m in time slot t;</td></tr><tr><td></td><td>The residual battery energy of UAV u in</td></tr><tr><td> $\ v { s } _ { u } ^ { t }$ </td><td>time slot t;</td></tr><tr><td>S</td><td>The state of UAV u in time slot  $t ;$ </td></tr><tr><td> $a _ { u } ^ { t }$ </td><td>The state of all UAVs in time slot t;</td></tr><tr><td> $a ^ { t }$ </td><td>The action of UAV u in time slot t;</td></tr><tr><td></td><td>The joint action of UAVs in time slot t;</td></tr><tr><td> $R _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right)$ </td><td>The immediate reward received by UAV u</td></tr><tr><td></td><td>after taking action  $a _ { u } ^ { t }$  at state  $s ^ { t } ;$ </td></tr><tr><td> $\pi _ { 0 }$ </td><td>The shared policy in the</td></tr><tr><td></td><td>designed learning algorithm;</td></tr><tr><td> $\pi _ { u }$ </td><td>The task-specific policy of UAV u in the</td></tr><tr><td></td><td></td></tr><tr><td></td><td>designed learning algorithm;</td></tr><tr><td> $\theta _ { 0 } , \{ \theta _ { u } \} _ { u \in \mathbb { U } }$ </td><td>Optimization parameters of the shared policy network and task-specific policy</td></tr></table>

TABLE I  
MAIN NOTATIONS

## III. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, we present the constructed system model and formulate the long-term computation efficiency maximization problem. The main notations can be found in Table I.

## A. System Model

We consider a UAV-assisted WPMEC system, which can provide support for running programs developed for the metaverse. As shown in Fig. 1, we consider a three-dimensional region containing Access Points (APs), laser emitters, U UAVs, denoted by $\mathbb { U } = \{ 1 , \dots , u , \dots , U \}$ , and M mobile devices, represented by $\mathbb { M } = \{ 1 , \dots , m , \dots , M \}$ . According to the time allocation model proposed in subsection III-B, we can classify M mobile devices and U UAVs as type-1 and type-2 devices as well as type-1 and type-2 UAVs, respectively. Both UAVs and mobile devices are equipped with communication, computation, and energy harvesting units, and UAVs have stronger computing capabilities than mobile devices. Mobile devices randomly moving in this region can perform local computing or offload tasks using the energy collected from all APs. UAVs driven by the laser emitter provide computing services for mobile devices on the ground, each of which is equipped with a single antenna. Similar to [21], we assume that mobile devices is half-duplex, which means that energy harvesting and communication cannot be performed simultaneously.

<!-- image-->  
Fig. 1. The illustrative system model.

Furthermore, we model locations of UAVs and mobile devices by three-dimensional Euclidean coordinates. To facilitate exposition, the time range is divided into a set of time slots with equal duration T . In time slot t, the coordinate of mobile device m is denoted by $\boldsymbol { q } _ { m } ^ { t } = ( x _ { m } ^ { t } , y _ { m } ^ { t } , 0 )$ , while that of UAV u is denoted by $\boldsymbol { q } _ { u } ^ { t } = ( x _ { u } ^ { t } , y _ { u } ^ { t } , H )$ . It is assumed that UAV u flies at uniform speed $\mathbb { V } _ { u } ^ { t } = ( q _ { u } ^ { t } - q _ { u } ^ { t - 1 } ) / T$ and altitude H. Similar to [22], [23], and [24], we assume that the channel between UAV u and mobile device m is line-of-sight, and the channel gain is given by:

$$
h _ { m u } ^ { t } = \xi _ { 0 } ( d _ { m u } ^ { t } ) ^ { - 2 } = \frac { \xi _ { 0 } } { H ^ { 2 } + \left\| q _ { u } ^ { t } - q _ { m } ^ { t } \right\| ^ { 2 } } ,\tag{2}
$$

where $\xi _ { 0 }$ is the channel power gain at reference distance $d _ { 0 } =$ 1 m, and â¥.â¥ denotes the Euclidean norm. Variable $d _ { m u } ^ { t }$ is the horizontal plane distance between UAV u and mobile device m in time slot t.

## B. Time Allocation Model

Considering half-duplex characteristics of UAVs and mobile devices, we design a time allocation model for the joint scheduling of UAVs and mobile devices. As shown in Fig. 2, the design principle is as follows:

<!-- image-->  
Fig. 2. The time allocation model.

From the perspective of UAVs, we first divide them into two types, i.e., type-1 and type-2 in each time slot. Specifically, type-1 UAVs provide computing services to mobile devices, while type-2 UAVs perform charging operations. By optimizing locations of UAVs in each time slot, type-1 and type-2 UAVs can achieve high offloading and charging efficiency, respectively. From the perspective of mobile devices, each time slot is divided into two phases, and all devices can be classified into type-1 and type-2 ones. Type-1 devices refer to those who perform task offloading operations in the first phase and charging operations in the second phase, while type-2 devices do the opposite.

In time slot t, the scheduling of mobile devices and UAVs is determined by binary variables $\alpha _ { m } ^ { t }$ and $\beta _ { u } ^ { t }$ , respectively. If the values of $\alpha _ { m } ^ { t }$ and $\beta _ { u } ^ { t }$ are both 1, it means that device m and UAV u are one type-1 mobile device and one type-1 UAV, respectively. Conversely, if both $\alpha _ { m } ^ { t }$ and $\beta _ { u } ^ { t }$ are 0, device m and UAV u are one type-2 mobile device and one type-2 UAV, respectively. The time slot can be divided into two periods by time allocation variable $\tau ^ { t }$ , where $\tau ^ { t } \in ( 0 , 1 )$ . In the first period of size $\tau ^ { t }$ , type-1 devices offload their computation tasks to type-1 UAVs while type-2 devices collect energy from APs. In the second period of size 1âÏ t, type-2 devices offload their tasks to type-1 UAVs while type-1 devices collect energy. It is noteworthy that in each time slot, type-1 UAVs always provide computing services to mobile devices, while type-2 UAVs collect energy from the laser transmitter.

Different from existing studies that perform charging or task offloading operations for all devices simultaneously [10], our time allocation model allows two types of mobile devices to perform different operations in the same period, thus making better utilization of network resources, such as computing resources of type-1 UAVs.

## C. Energy Harvesting and Consumption Model

1) Energy Harvesting and Consumption of Mobile Devices: Since our focus is on joint time scheduling and UAV trajectory design, we adopt the linear energy harvesting model for our system [21]. Similar to [25], we view all APs as an integrated virtual transmitter. Therefore, the harvested energy for device m in time slot t can be expressed by:

$$
E _ { m } ^ { t , h } = \varepsilon ( 1 - \alpha _ { m } ^ { t } ) \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \tau ^ { t } T + \varepsilon \alpha _ { m } ^ { t } \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } ( 1 - \tau ^ { t } ) T ,\tag{3}
$$

where $\varepsilon \in ( 0 , 1 )$ is the energy conversion efficiency of mobile devices. Variables $\mathcal { P } _ { 0 }$ and $\widetilde { \widehat { h } } _ { m } ^ { t }$ are the transmit power of the virtual transmitter and the downlink channel gain from device m to the virtual transmitter, respectively. It should be noted that if device m is type-2, its harvested energy in time slot t is $\varepsilon \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \tau ^ { t } T$ . In case it is of type-1, the collected energy is $\varepsilon \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } ( 1 - \tau ^ { t } ) T$

We consider partial offloading models, where mobile devices can perform local computation during the entire time slot. Specifically, in time slot t, the amount of local computation bits of device m can be denoted by $L _ { m } ^ { t , l } = f _ { m } T / C _ { 1 }$ Symbol $C _ { 1 }$ represents the number of CPU cycles required to compute each data bit, and variable $f _ { m }$ is the CPU frequency of device m. In addition, similar to [9], [10], and [25], energy consumption of device m for local computation is described by the form of the cube of its CPU frequency: $E _ { m } ^ { t , l } = k _ { m } \dot { f } _ { m } ^ { 3 } T$ . Symbol $k _ { m }$ is a coefficient related to the computation efficiency of device m.

Similar to [25] and [26], the communication between mobile devices and UAVs is based on orthogonal frequency division multiple access technology. The amount of offloading data bits of device m to UAV u in time slot t can be represented as:

$$
\begin{array} { r l } & { L _ { m } ^ { t , o } = ( \alpha _ { m } ^ { t } \tau ^ { t } + ( 1 - \alpha _ { m } ^ { t } ) ( 1 - \tau ^ { t } ) ) \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m u } ^ { t } } { \delta ^ { 2 } } \right) T } \\ & { \quad \quad = ( 1 - \tau ^ { t } - \alpha _ { m } ^ { t } + 2 \alpha _ { m } ^ { t } \tau ^ { t } ) \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m u } ^ { t } } { \delta ^ { 2 } } \right) T , } \end{array}\tag{4}
$$

where variables B and $\delta ^ { 2 }$ represent the channel bandwidth and the noise power, respectively. Variable $P _ { m }$ denote the transmission power of device m. In addition, the amount of its consumed energy for data transmission of device m in time slot t can be computed by:

$$
\begin{array} { c } { E _ { m } ^ { t , o } = ( \alpha _ { m } ^ { t } \tau ^ { t } + ( 1 - \alpha _ { m } ^ { t } ) ( 1 - \tau ^ { t } ) ) T P _ { m } } \\ { = ( 1 - \tau ^ { t } - \alpha _ { m } ^ { t } + 2 \alpha _ { m } ^ { t } \tau ^ { t } ) T P _ { m } . } \end{array}\tag{5}
$$

We select the UAV with the best channel condition as the target UAV of device m. The amount of computation bits of device m in time slot t can be represented as $L _ { m } ^ { t } = L _ { m } ^ { t , l } + L _ { m } ^ { t , o }$

Similarly, the amount of its consumed energy is $E _ { m } ^ { t } = E _ { m } ^ { t , l } +$ $E _ { m } ^ { t , o }$

2) Energy Harvesting and Consumption of UAVs: Similar to [11] and [12], taking into account the high energy consumption of flying UAVs, we use the laser charging to improve the charging efficiency of UAVs. Based on the linear energy harvesting model, the harvested energy of UAV u in time slot t can be represented as:

$$
\mathbb { E } _ { u } ^ { t , h } = \epsilon ( 1 - \beta _ { u } ^ { t } ) g _ { \mathrm { u a } } ^ { t } \mathcal { P } _ { 1 } T ,\tag{6}
$$

where $\epsilon \in ( 0 , 1 )$ is the energy conversion efficiency for UAVs, and $\mathcal { P } _ { 1 }$ is the transmission power of the laser. The laser charging channel from the laser transmitter to UAV u can be calculated by expression $g _ { u a } ^ { t } = { ( G \vartheta e ^ { - \phi d _ { u a } ^ { t } } ) } / { ( F + \nu d _ { u a } ^ { t } ) } ^ { 2 }$ ï¼ where variables G and $\phi$ represent the area of the telescope (or collector) of the laser receiver and the attenuation coefficient of the channel medium, respectively. Additionally, variable Ï denotes the optical efficiency of the combined transmission receiver, and variable $d _ { u a } ^ { t }$ represents the distance between UAV u and the laser transmitter. Variable F denotes the size of the initial laser beam, and variable Î½ denotes the angle diffraction [12].

In each time slot, the energy consumption of one type-1 UAV includes both propulsion and computation energy consumption, while that of one type-2 UAV only includes propulsion energy consumption. The computation energy consumption of type-1 UAV u in time slot t can be calculated by $\mathbb { E } _ { u } ^ { t , c } = k _ { u } { f _ { u } } ^ { 3 } \bar { T }$ , where variable $k _ { u }$ is the efficiency coefficient of UAV u for processing each data bit, and variable $f _ { u }$ is the CPU frequency of UAV u. By considering fixed-wing UAVs [12], the flight energy consumed by UAV u in time slot t is:

$$
\mathbb { E } _ { u } ^ { t , f } = T \left( \zeta _ { 1 } \| \mathbb { V } _ { u } ^ { t } \| ^ { 3 } + \frac { \zeta _ { 2 } } { \| \mathbb { V } _ { u } ^ { t } \| } \right) ,\tag{7}
$$

where variables $\zeta _ { 1 }$ and $\zeta _ { 2 }$ are fixed parameters related to the specifications of UAVs [12]. Finally, the energy consumption of UAV u in time slot t can be expressed by:

$$
\mathbb { E } _ { u } ^ { t } = \mathbb { E } _ { u } ^ { t , f } + \beta _ { u } ^ { t } \mathbb { E } _ { u } ^ { t , c } = T \left( \zeta _ { 1 } \| \mathbb { V } _ { u } ^ { t } \| ^ { 3 } + \frac { \zeta _ { 2 } } { \| \mathbb { V } _ { u } ^ { t } \| } + \beta _ { u } ^ { t } k _ { u } { f _ { u } } ^ { 3 } \right) .\tag{8}
$$

As a result, we can define system computation efficiency $\eta _ { C E } ^ { t }$ by the ratio of the total amount of computation bits to that of energy consumed by both mobile devices and UAVs in time slot t, i.e.,

$$
\eta _ { C E } ^ { t } = \frac { \sum _ { m = 1 } ^ { M } L _ { m } ^ { t } } { \sum _ { m = 1 } ^ { M } E _ { m } ^ { t } + \sum _ { u = 1 } ^ { U } \mathbb { E } _ { u } ^ { t } } .\tag{9}
$$

## D. Problem Formulation

In time slot $t ,$ mobile devices and UAVs can be classified into different types based on variables $\alpha _ { m } ^ { t }$ and $\beta _ { u } ^ { t }$ , as described in subsection III-B, and their energy harvesting and consumption models are defined in subsection III-C. Considering time allocation variable $\tau ^ { t }$ , device scheduling variable $\alpha _ { m } ^ { t } ,$ UAV scheduling variable $\beta _ { u } ^ { t }$ and UAV location $q _ { u } ^ { t }$ , we formulate the computation efficiency maximization problem as follows:

Objective:

Our objective is to maximize the average computation efficiency over all time slots, i.e.,

$$
\mathrm { P } 1 : \operatorname* { m a x } _ { \tau ^ { t } , \alpha _ { m } ^ { t } , \beta _ { u } ^ { t } , q _ { u } ^ { t } } \operatorname* { l i m } _ { t  \infty } \frac { 1 } { t } \sum _ { j = 1 } ^ { t } \eta _ { C E } ^ { j } ,\tag{10}
$$

$$
\begin{array} { r l r } & { \mathrm { s . t . } \ } & { ( \alpha _ { m } ^ { t } P _ { m } + k _ { m } f _ { m } ^ { 3 } ) \tau ^ { t } T \leq E _ { m } ^ { t - 1 , r } , m \in \mathbb { M } , } \end{array}
$$

$$
t \in \{ 1 , 2 , 3 \ldots \} ,\tag{10a}
$$

$$
E _ { m } ^ { t } \leq E _ { m } ^ { t - 1 , r } + E _ { m } ^ { t , h } , m \in \mathbb { M } , t \in \{ 1 , 2 , 3 \dots \} ,\tag{10b}
$$

$$
\mathbb { E } _ { u } ^ { t } \le \mathbb { E } _ { u } ^ { t - 1 , r } + \mathbb { E } _ { u } ^ { t , h } , u \in \mathbb { U } , t \in \{ 1 , 2 , 3 \dots . . . \} .\tag{10c}
$$

Input:

UAV set U, mobile device set M, CPU frequencies $\{ f _ { m } \} _ { m \in \mathbb { M } }$ and $\{ f _ { u } \} _ { u \in \mathbb { U } } ,$ , channel bandwidth B, noise power $\delta ^ { 2 }$ , transmission power $\mathcal { P } _ { 1 }$ , energy conversion efficiencies Îµ and Ïµ, computation efficiency coefficients $\{ k _ { m } \} _ { m \in \mathbb { M } }$ and $\{ k _ { u } \} _ { u \in \mathbb { U } }$ , device transmission power $\{ P _ { m } \} _ { m \in \mathbb { M } }$ , device residual battery energy $\{ E _ { m } ^ { t - 1 , r } \} _ { m \in \mathbb { M } }$ , UAV residual battery energy $\big \{ \mathbb { E } _ { u } ^ { t - 1 , r } \big \} _ { u \in \mathbb { U } } .$

Output:

1) Time allocation variable $\tau ^ { t } \in ( 0 , 1 ) , t \in \{ 1 , 2 , 3 \dots \}$

$$
\alpha _ { m } ^ { t } \in \{ 0 , 1 \}
$$

$$
\beta _ { u } ^ { t } \in
$$

$$
m \in \mathbb { M }
$$

$$
t \in \{ 1 , 2 , 3 \ldots \}
$$

3) The trajectory of UAVs, i.e., $q _ { u } ^ { t }$ for UAV u, $u \in \mathbb { U }$ and $t \in \left\{ 1 , 2 , 3 \ldots \right\}$

Constraints:

During the first $\tau ^ { t }$ period of time slot t, the energy consumed by type-1 device m should be less than its remaining energy in time slot t â 1, as shown in equation (10a). In time slot t, mobile devices must satisfy inequality constraint (10b), where the energy consumed by device m should not exceed the sum of its remaining energy in time slot t â 1 and the energy harvested in time slot t. Similarly, the energy consumed by UAVs should also be less than the sum of its remaining energy in time slot t â 1 and the energy harvested in time slot t, as shown in inequality constraint (10c).

Based on constraints (10a)-(10c), it can be observed that device scheduling variable $\alpha _ { m } ^ { t }$ influences the choice of time allocation variable $\tau ^ { t }$ , while UAV scheduling variable $\beta _ { u } ^ { t }$ and UAV location $q _ { u } ^ { t }$ are strongly coupled. Therefore, we can derive the following theorem.

Theorem 1: Problem P1 is a mixed integer nonconvex fractional problem that is NP-hard.

Please refer to Appendix A for the proof of Theorem 1.

## IV. ALGORITHM DESIGN

In this section, to address Problem P1 defined in subsection III-D, we first decompose P1 into two subproblems based on the coupling relationship among variables. Then, we propose a two-stage alternating optimization algorithm based on multi-task DRL, which can effectively solve the above two subproblems. Specifically, in order to support the running of human-centric metaverse applications at mobile devices, we first optimize device scheduling variable $\alpha _ { m } ^ { t }$ and time allocation variable Ï t according to the requirements of mobile devices in subsection IV-B, and then optimize UAV scheduling variable $\beta _ { u } ^ { t }$ and location $q _ { u } ^ { t }$ based on multi-task DRL in subsection IV-C.

## A. Problem Decomposition

The problem we have formulated as a mixed nonlinear long-term optimization problem belongs to the class of NP-hard problems and involves numerous optimization variables coupled among time slots. The traditional heuristic algorithm is not suitable for solving Problem P1 due to its properties such as high complexity and inability to adapt to the dynamic network environment. Moreover, we observe that from the perspective of UAVs, Problem P1 can be decomposed into a series of interrelated subtasks. Therefore, we utilize multi-task DRL to solve these subtasks concurrently.

However, it is challenging to solve Problem P1 directly by multi-task DRL approach because of the large number of complex decision variables involved in it. On the one hand, in our considered scenario of WPMEC assisted by UAVs, device scheduling variable $\alpha _ { m } ^ { t }$ is a binary decision for each device. Modeling device scheduling variable $\alpha _ { m } ^ { t }$ as actions, with the presence of merely 20 mobile devices, the dimensionality of the candidate action space will be $2 ^ { 2 0 }$ . Such a large action space makes it difficult to achieve convergence in algorithm training. Therefore, device scheduling variable $\alpha _ { m } ^ { t }$ cannot be directly solved by multi-task DRL. On the other hand, since Problem P1 has four optimization variables, it is difficult to solve them simultaneously by a multi-task DRL algorithm without sacrificing complexity.

To solve the above challenges, we decompose Problem P1 into two subproblems. Subproblem 1 is to optimize device scheduling and WPT time allocation in time slot t, which can be expressed by:

$$
\begin{array} { r l } { \mathrm { P 2 : ~ } } & { \underset { \tau ^ { t } , \alpha _ { m } ^ { t } } { \operatorname* { m a x } } \quad \eta _ { C E } ^ { t } , } \\ & { \mathrm { s . t . } \quad \mathrm { i n e q u a t i o n s ~ ( 1 0 a ) ~ a n d ~ ( 1 0 b ) . } } \end{array}\tag{11}
$$

Subproblem 2 is the charging scheduling and trajectory design for UAVs with the optimization objective of maximizing the average computation efficiency, which can be expressed by:

$$
\mathrm { P 3 : } \quad \operatorname* { m a x } _ { \beta _ { u } ^ { t } , q _ { u } ^ { t } } \operatorname* { l i m } _ { t \to \infty } \frac { 1 } { t } \sum _ { j = 1 } ^ { t } \eta _ { C E } ^ { j } , \quad \tag{12}
$$

We design an efficient heuristic algorithm to solve subproblem 1 in subsection IV-B and design a novel multi-task DRL algorithm to solve subproblem 2 in subsection IV-C. It is worth noting that subproblem 2 requires the solution of subproblem 1 as input, and the solution of subproblem 2 also affects the solution of subproblem 1. Therefore, the long-term optimization of computation efficiency in Problem P1 can be achieved by alternative optimization between subproblem 1 and subproblem 2.

## B. Device Scheduling and Time Allocation

The focus of Problem P2 is to maximize the computation efficiency by scheduling charging and computation offloading for mobile devices. Due to the coupling between device scheduling variable $\alpha _ { m } ^ { t }$ and time allocation variable $\tau ^ { t } ,$ , Problem P2 is a mixed-integer nonlinear programming problem that is difficult to solve. Similar to [27] and [28], we consider a device scheduling strategy based on the remaining energy of mobile devices, where devices with high remaining energy above a threshold are classified as type-1 ones, and those with relatively low remaining energy below the threshold are classified as type-2 ones. The details are as follows:

$$
\alpha _ { m } ^ { t * } = \left\{ \begin{array} { l l } { 1 , } & { E _ { m } ^ { t - 1 , r } > \Theta _ { s } ; } \\ { 0 , } & { \mathrm { e l s e } , } \end{array} \right.\tag{13}
$$

where $\Theta _ { s }$ is a threshold and $E _ { m } ^ { t - 1 , r }$ is the residual energy of device m in time slot t â 1. We set threshold Îs based on whether the remaining energy of device m is sufficient for critical operations (e.g., local computation and task offloading). Based on constraint (10a), it can be observed that during the first $\tau ^ { t }$ time period of time slot t, the consumed energy of type-1 device m should be less than its remaining energy in time slot t â 1. In addition, if device m does not conduct WPT charging operation in time slot t, rather it spends the whole time of the time slot for offloading tasks as well as local computation, it can be derived that its maximum energy consumption in time slot t is $( k _ { m } f _ { m } ^ { 3 } + P _ { m } ) T$ . Therefore, setting threshold Îs to the maximum energy consumption of type-1 device m, denoted as $\Theta _ { s } = ( k _ { m } f _ { m } ^ { 3 } + P _ { m } ) T$ , can make constraint (10a) hold under any value of time allocation variable $\tau ^ { t }$ Â·

In addition, based on optimal device scheduling variable $\alpha _ { m } ^ { t * }$ , the number of computation bits, energy consumption and harvesting of device m can be updated to $\bar { L } _ { m } ^ { t ^ { \prime } } , E _ { m } ^ { t ^ { \prime } }$ and $E _ { m } ^ { t , h ^ { \prime } }$ by:

$$
{ L _ { m } ^ { t } } ^ { \prime } = \frac { f _ { m } T } { C _ { 1 } } + ( 1 - \tau ^ { t } - \alpha _ { m } ^ { t * }
$$

$$
+ ~ 2 \alpha _ { m } ^ { t * } \tau ^ { t } ) \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m u } ^ { t } } { \delta ^ { 2 } } \right) T ,\tag{14}
$$

$$
{ E _ { m } ^ { t } } ^ { \prime } = k _ { m } f _ { m } ^ { 3 } T + ( 1 - \tau ^ { t } - \alpha _ { m } ^ { t * } + 2 \alpha _ { m } ^ { t * } \tau ^ { t } ) T P _ { m } ,\tag{15}
$$

$$
E _ { m } ^ { t , h ^ { \prime } } = \varepsilon ( 1 - \alpha _ { m } ^ { t * } ) \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \tau ^ { t } T + \varepsilon \alpha _ { m } ^ { t * } \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } ( 1 - \tau ^ { t } ) T .\tag{16}
$$

Furthermore, Problem P2 can be transformed into Problem P2â² with optimal device scheduling variable $\alpha _ { m } ^ { t * }$ for time allocation, which can be expressed by:

$$
\begin{array} { r l }  { \mathrm { P } } 2 ^ { \prime } : { \mathrm { ~ } \begin{array} { l l l } { \operatorname* { m a x } } & { \displaystyle { ~ \sum _ { m = 1 } ^ { M } L _ { m } ^ { t } } ^ { \prime } } \\ { \tau ^ { t } } & { \displaystyle { ~ \sum _ { m = 1 } ^ { M } E _ { m } ^ { t } } ^ { \prime } + \sum _ { u = 1 } ^ { U } \mathbb { E } _ { u } ^ { t } } \end{array} } , \end{array}\tag{17}
$$

$$
\begin{array} { r l r } { \mathrm { s . t . } } & { { } } & { ( \alpha _ { m } ^ { t * } P _ { m } + k _ { m } f _ { m } ^ { 3 } ) \tau ^ { t } T \le E _ { m } ^ { t - 1 , r } , m \in \mathbb { M } , } \end{array}\tag{17a}
$$

$$
{ E _ { m } ^ { t } } ^ { \prime } \leq E _ { m } ^ { t - 1 , r } + E _ { m } ^ { t , h ^ { \prime } } , m \in \mathbb { M } .\tag{17b}
$$

It is a linear fractional problem related to time allocation variable $\tau ^ { t }$ . Particularly, we can obtain explicit results of Problem P2â², which is described in Theorem 2.

Theorem 2: The optimal value of time allocation variable $\tau ^ { t }$ can be obtained by:

$$
\tau ^ { t * } = \left\{ \begin{array} { l l } { \operatorname* { m i n } \{ \displaystyle \frac { E _ { m } ^ { t - 1 , r } } { T ( \alpha _ { m } ^ { t * } P _ { m } + k _ { m } f _ { m } ^ { 3 } ) } \} , } & { A D - B C > 0 ; } \\ { \operatorname* { m a x } \{ \displaystyle \frac { k _ { m } f _ { m } ^ { 3 } + ( 1 - \alpha _ { m } ^ { t * } ) P _ { m } } { ( 1 - 2 \alpha _ { m } ^ { t * } ) \left( P _ { m } + \varepsilon \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \right) } } \\ { + \displaystyle \frac { - E _ { m } ^ { t - 1 , r } - \varepsilon T \alpha _ { m } ^ { t * } \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } } { T ( 1 - 2 \alpha _ { m } ^ { t * } ) \left( P _ { m } + \varepsilon \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \right) } \} , } & { A D - B C < 0 , } \end{array} \right.\tag{18}
$$

where $\begin{array} { r } { A = \sum _ { m = 1 } ^ { M } { ( 2 \alpha _ { m } ^ { t * } - 1 ) \mathbb { B } { l o g } _ { 2 } \left( { 1 + P _ { m } h _ { m u } ^ { t } / { \delta ^ { 2 } } } \right) } } \end{array}$ , B = $\begin{array} { r l } { \sum _ { m = 1 } ^ { M } \big ( f _ { m } / C _ { 1 } + ( 1 - \alpha _ { m } ^ { t * } ) \mathbb { B } l o g _ { 2 } ( 1 + \underline { { P _ { m } } } h _ { m u } ^ { t } / \delta ^ { 2 } ) \big ) , \ C } & { = } \end{array}$ $\begin{array} { r } { \sum _ { m = 1 } ^ { M } P _ { m } ( 2 \alpha _ { m _ { * } } ^ { t * } - 1 ) } \end{array}$ and $\begin{array} { r } { D ~ = ~ \sum _ { m = 1 } ^ { M } ( k _ { m } f _ { m } ^ { 3 } + P _ { m } ( 1 - } \end{array}$ $\begin{array} { r } { \alpha _ { m } ^ { t * } ) ) + \sum _ { u = 1 } ^ { U } \left( \beta _ { u } ^ { t } k _ { u } { f _ { u } } ^ { 3 } + \zeta _ { 1 } \| \mathbb { V } _ { u } ^ { t } \| ^ { 3 } + \zeta _ { 2 } / \| \mathbb { V } _ { u } ^ { t } \| \right) } \end{array}$

In addition, we can obtain the relationship among variables $A , B , C$ and D defined in Theorem 2, which is helpful for us to derive the final results of Problem $\mathbf { P } 2 ^ { \prime }$ and the corollary is as follows:

Corollary 1: The polarity of AD â BC is determined by variable A, where A = $\begin{array} { r l r } { \sum _ { m = 1 } ^ { M } { ( 2 \alpha _ { m } ^ { t * } - 1 ) \mathbb { B } \bar { l o } g _ { 2 } ( 1 } } & { { } + } & { P _ { m } h _ { m u } ^ { t } / \delta ^ { 2 } ) } \end{array}$ ï¼ B $\begin{array} { r l r } { \sum _ { m = 1 } ^ { M } \left( f _ { m } / C _ { 1 } + ( 1 - \alpha _ { m } ^ { t * } ) \mathbb { B } l o g _ { 2 } ( 1 + P _ { m } h _ { m u } ^ { t } / \delta ^ { 2 } ) \right) , } & { { } C } & { = } \end{array}$ $\begin{array} { r } { \sum _ { m = 1 } ^ { M } P _ { m } ( 2 \alpha _ { m _ { . } } ^ { t * } - 1 ) } \end{array}$ and $\begin{array} { r } { D ~ = ~ \sum _ { m = 1 } ^ { M } ( k _ { m } f _ { m } ^ { 3 } + P _ { m } ( 1 - } \end{array}$ $\begin{array} { r l } { \alpha _ { m } ^ { t * } ) ) + \sum _ { u = 1 } ^ { U } \Big ( \beta _ { u } ^ { t } { k _ { u } } { f _ { u } } ^ { 3 } + \zeta _ { 1 } \| \mathbb { V } _ { u } ^ { t } \| ^ { 3 } + \zeta _ { 2 } / \| \mathbb { V } _ { u } ^ { t } \| \Big ) } \end{array}$

Based on Corollary 1, we can further analyze and obtain Theorem 3 as follows:

Theorem 3: In time slot t, if the sum of channel capacity of all type-1 devices is greater than that of all type-2 devices, we choose the larger value as the optimal solution for $\tau ^ { t }$ . Conversely, we choose the smaller value as the optimal solution.

Please refer to Appendix D for the proof of Theorem 3.

Based on Theorem 2 and Theorem 3, the optimal solution of Problem $\mathbf { P } 2 ^ { \prime }$ can be obtained.

## C. UAV Scheduling and Trajectory Design

Since $\beta _ { u } ^ { t }$ is a binary variable and coupled with $q _ { u } ^ { t } ,$ , Problem P3 is a mixed integer nonlinear programming problem, and hard to be solved by traditional optimization algorithms or DRL methods for the following reasons: First, traditional heuristic algorithms cannot detect and adapt to the dynamics of the network environment, resulting in poor performance; Second, given the large action space of UAVs, solving Problem P3 by traditional DRL such as policy-based gradients may face slow convergence and large time complexity.

Therefore, we divide the charging scheduling and trajectory design task for all UAVs into U subtasks. Specifically, subtask u aims to complete the charging scheduling and trajectory design for UAV u, where $u \in \mathbb { U }$ . This significantly reduces the dimensionality of the action space, since only candidate actions for one UAV need to be considered for each subtask. However, the interactions among the U subtasks cause them to be not able to develop separate strategies. Therefore, we design a multi-task DRL-based scheduling algorithm that can learn the relationships among different subtasks and process them simultaneously to maximize the computation efficiency of the system. First, we transfer Problem P3 into a Markov Decision Process (MDP), which is presented as follows:

<!-- image-->  
Fig. 3. The structure of the designed learning algorithm.

1) MDP Problem Formulation: The observable Markov game can be formulated by tuple $( S _ { u } , \mathbb { A } _ { u } , \mathbb { P } _ { u } , R _ { u } , \gamma )$ , where $u \in \mathbb { U }$ . The learning agent interacts with a dynamic environment that is characterized by action space $\overset { \cdot } { A } \triangleq \left\{ \mathbb { A } _ { u } , u \in \mathbb { U } \right\}$ and state space $\mathcal { S } \triangleq \{ S _ { u } , \overset { \cdot } { u } \in \mathbb { U } \}$ , where $\mathbb { A } _ { u }$ and $S _ { u }$ are the action space and state space of UAV $u ,$ respectively. The transfer from the current state of UAVs to its next state is based on probability $\mathcal { P } \triangleq \{ \mathbb { P } _ { u } , u \in \mathbb { U } \}$ . In addition, symbol $\gamma \in \mathsf { \Gamma } ( 0 , 1 )$ refers to the discount coefficient. We define $\pi _ { u }$ as the task-specific stochastic policy for charging scheduling and trajectory design of UAV u. Considering that charging scheduling and trajectory design among UAVs are interactive, we define $\pi _ { 0 }$ as a shared policy to learn knowledge among multiple UAVs. As shown in Fig. 3, during the training process, the action of each UAV is output by a separate policy network, and the shared policy network can extract information from all the policy networks to assist them in formulating a rational policy. Thus, each UAV knows not only its private information when selecting an action according to policy $\pi _ { u } .$ , but also the additional information about other UAVs (e.g., their coordinates and scheduling variables). In the following, we describe different elements of the formulated Markov game.

States: State space $S _ { u }$ of each UAV composes state space $\mathcal { S } \triangleq \{ S _ { u } , u \in \mathbb { U } \}$ . It is observed that $\begin{array} { l c l } { { S _ { u } } } & { { = } } & { { \{ s _ { u } ^ { t } \ = \ } }  \end{array}$ $( q _ { u } ^ { t - 1 } , \dot { \mathbb { E } } _ { u } ^ { t - 1 , r } , \{ q _ { m } ^ { t } , E _ { m } ^ { t - 1 , r } \} _ { m \in \mathbb { M } } ) \}$ . Set $\{ q _ { m } ^ { t } \} _ { m \in \mathbb { M } }$ includes coordinates of all devices in time slot $t ,$ and $q _ { u } ^ { t - 1 }$ is the coordinate of UAV u in time slot t â 1. Set $\{ E _ { m } ^ { t - 1 , r } \} _ { m \in \mathbb { M } }$ and symbol $\mathbb { E } _ { u } ^ { t - 1 , r }$ are the residual energy of all devices and UAV u in time slot t â 1, respectively. In addition, the state of all UAVs in time slot t is denoted as $s ^ { t } = ( s _ { 1 } ^ { t } , \ldots , s _ { u } ^ { t } , \ldots , s _ { U } ^ { t } )$

Actions: The action space of UAV u can be expressed by $\mathbb { A } _ { u } ~ = ~ \{ a _ { u } ^ { t } ~ = ~ ( \beta _ { u } ^ { t } , q _ { u } ^ { t } ) \}$ Variables $\beta _ { u } ^ { t }$ and $q _ { u } ^ { t }$ are the scheduling variable and the coordinate of UAV u in time slot t, respectively. Then, the joint action of UAVs in time slot t is represented by $a ^ { t } = ( a _ { 1 } ^ { t } , \dots , a _ { u } ^ { t } , \dots , a _ { U } ^ { t } )$ . After executing action $a _ { u } ^ { t }$ , UAV u receives reward $R _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right)$ and the private state of UAV u is updated to the new state.

State Transition: Probability $\mathbb { P } _ { u } \left( s _ { u } ^ { t + 1 } \middle | s _ { u } ^ { t } , a _ { u } ^ { t } \right)$ denotes the state transition probability for UAV u, when state $\ v { s } _ { u } ^ { t }$ shifts to state $s _ { u } ^ { t + 1 }$ by taking action $a _ { u } ^ { t }$

Reward: The main goal of this work is to maximize the computation efficiency of the system, i.e., to maximize the system computation bits and minimize the total system energy consumption. Therefore, UAV u can obtain the reward according to the defined computation efficiency as follows:

$$
R _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) = \sum _ { j = 1 } ^ { t } \eta _ { C E } ^ { j } .\tag{19}
$$

Furthermore, the reward of the learning agent is the sum of rewards of all UAVs, i.e., $\begin{array} { r } { R \left( a ^ { t } | s ^ { t } \right) = \bar { \sum _ { u = 1 } ^ { U ^ { - } } } R _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right) } \end{array}$

Constraint Relaxation: During the execution of the multi-task DRL algorithm, it is difficult to satisfy the energy constraint of UAVs. Thus, we add penalty term $l _ { u } ^ { t }$ to reward $R _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right)$ , expressed by:

$$
l _ { u } ^ { t } = \left\{ \begin{array} { l l } { 0 , } & { \mathbb { E } _ { u } ^ { t } - \mathbb { E } _ { u } ^ { t - 1 , r } - \mathbb { E } _ { u } ^ { t , h } \leq 0 , } \\ { \lambda _ { u } ^ { t } , } & { \mathrm { e l s e } , } \end{array} \right.\tag{20}
$$

where symbol $\lambda _ { u } ^ { t }$ is an adjustment parameter for UAV u. This penalty is to ensure that the energy constraint of UAV u can be satisfied, i.e., the sum of the residual energy of UAV u in time slot $t - 1$ and the energy collected in time slot t is higher than the energy consumed in time slot t. Thus, when the above constraint is satisfied, $l _ { u } ^ { t } = 0 ;$ otherwise, $l _ { u } ^ { t } = \lambda _ { u } ^ { t }$ Then, the reward is updated by $\begin{array} { r } { R _ { u } ^ { \prime } \left( a _ { u } ^ { t } | s ^ { t } \right) = R _ { u } \left( a _ { u } ^ { t } | \bar { s } ^ { t } \right) - l _ { u } ^ { \bar { t } } } \end{array}$ ï¼ where $u \in \mathbb { U }$

2) Optimization Problem Formulation: It is worth noting that for reinforcement learning, maintaining a trade-off between exploration and exploitation is intuitively important to obtain good training results. Therefore, to encourage exploration and avoid premature trapping in local optima, we regulate each task-specific policy by Î³-discount KL difference [14] for shared policies, i.e.,

$$
\mathbb { E } _ { \pi _ { u } } \left[ \sum _ { t \geq 0 } \gamma ^ { t } \log \frac { \pi _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) } { \pi _ { 0 } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) } \right] , u \in \mathbb { U } .\tag{21}
$$

We need to find shared policy $\pi _ { 0 }$ and task-specific policy $\{ \pi _ { u } \} _ { u \in \mathbb { U } }$ to achieve the long-term minimization of system energy consumption and the long-term maximization of system computation bits, i.e., to solve Problem P3. In other words, we take maximizing all UAV expected rewards as the optimization objective. To avoid local optima, we also introduce Î³-discount entropy regularization. As a result, we formulate Problem P4 as follows:

$$
\begin{array} { r l r } {  { \mathbb { P } 4 : \operatorname* { m a x } _ { ( \pi _ { 0 } , \{ \pi _ { u } \} _ { u \in \mathbb { U } } ) } \sum _ { u = 1 } ^ { U } \mathbb { E } _ { \pi _ { u } } \sum _ { t \geq 0 } \Big ( \gamma ^ { t } R _ { u } ^ { \prime } ( a _ { u } ^ { t } \Big | s ^ { t } ) - c _ { K L } \gamma ^ { t } \log \pi _ { 0 } } } \\ & { } & { \times ( a _ { u } ^ { t } \Big | s ^ { t } ) - ( c _ { E n t } - c _ { K L } ) \gamma ^ { t } \log \pi _ { u } ( a _ { u } ^ { t } \Big | s ^ { t } ) \Big ) , } \end{array}\tag{22}
$$

where variables $c _ { K L } , c _ { E n t } \geq 0$ are scalar factors determining the strengths of the KL and entropy regularization.

Then, we introduce two variables, $\lambda = c _ { K L } / ( c _ { K L } + c _ { E n t } )$ and $\mu = 1 / ( c _ { K L } + c _ { E n t } )$ , and input them into equation (22) and obtain equation (23), which is expressed by:

$$
\begin{array} { r l } & { \displaystyle \mathrm { P } 4 : \operatorname* { m a x } _ { \left( \pi _ { 0 } , \left\{ \pi _ { u } \right\} _ { u \in \mathbb { U } } \right) } \sum _ { u = 1 } ^ { U } \mathbb { E } _ { \pi _ { u } } \sum _ { t \geq 0 } \left( \gamma ^ { t } R _ { u } ^ { \prime } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) \right. } \\ & { \qquad \displaystyle \left. + \frac { \gamma ^ { t } \lambda } { \mu } \log \pi _ { 0 } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) - \frac { \gamma ^ { t } } { \mu } \log \pi _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) \right) . } \end{array}\tag{23}
$$

To overcome the exploration and exploration bottleneck, log $\pi _ { 0 } \left( a _ { u } ^ { t } | s ^ { t } \right)$ in equation (23) can be viewed as a reward-shaping term that encourages the selection of actions with high probability under shared policy $\pi _ { 0 } ,$ while entropy term $- \log \pi _ { u } \left( a _ { u } ^ { t } | s ^ { \bar { t } } \right)$ encourages the agent to select other actions.

With respect to the optimization of the objective function, we utilize an alternating maximization procedure, which optimizes over UAV-specific policy $\{ \pi _ { u } \} _ { u \in \mathbb { U } }$ given shared policy $\pi _ { 0 }$ and over shared policy $\pi _ { 0 }$ given UAV-specific policies $\{ \pi _ { u } \} _ { u \in \mathbb { U } }$ , respectively. Deep Neural Networks (DNNs) are used to parameterize shared policy $\pi _ { 0 }$ and task-specific policies $\{ \pi _ { u } \} _ { u \in \mathbb { U } }$ . First, by fixing shared policy $\pi _ { 0 } .$ , Problem P4 is decomposed into separate maximization problem P4â² for each task, which is shown by:

$$
\begin{array} { r } { \mathrm { P 4 ^ { \prime } : } \displaystyle \operatorname* { m a x } _ { \{ \pi _ { u } \} _ { u \in \mathbb { U } } } \displaystyle \sum _ { u = 1 } ^ { U } \mathbb { E } _ { \pi _ { u } } [ \displaystyle \sum _ { t \geq 0 } R _ { u } ^ { \prime \prime } ( a _ { u } ^ { t } \middle | s ^ { t } ) - \displaystyle \frac { \gamma ^ { t } } { \mu } \log \pi _ { u } ( a _ { u } ^ { t } \middle | s ^ { t } ) ) ] , } \\ { u \in \mathbb { U } , \qquad ( 2 4 ) } \end{array}
$$

where the regularization reward is redefined by:

$$
R _ { u } ^ { \prime \prime } \left( a _ { u } ^ { t } { \left| s ^ { t } \right. } \right) = R _ { u } ^ { \prime } \left( a _ { u } ^ { t } { \left| s ^ { t } \right. } \right) + \frac { \lambda } { \mu } \log { \pi _ { 0 } \left( a _ { u } ^ { t } { \left| s ^ { t } \right. } \right) } , u \in \mathbb { U } .\tag{25}
$$

Problem $\mathsf { P } 4 ^ { \prime }$ can be optimized by soft Q learning, which is based on the following âsoftenedâ Bellman updates for states and actions [29]:

$$
V _ { u } \left( s ^ { t } \right) = \frac { 1 } { \mu } \log \sum _ { a _ { u } ^ { t } } \pi _ { 0 } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) \exp \left[ \mu Q _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) \right] ,\tag{26}
$$

where Q function $Q _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right)$ can be computed by:

$$
\begin{array} { r } { Q _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) = \gamma ^ { t } R _ { u } ^ { \prime } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) + \frac { \gamma ^ { t } \lambda } { \mu } \log \pi _ { 0 } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) } \\ { + \gamma \displaystyle \sum _ { s _ { u } ^ { t + 1 } } \mathbb { P } _ { u } \left( s _ { u } ^ { t + 1 } \middle | s _ { u } ^ { t } , a _ { u } ^ { t } \right) V _ { u } \left( s ^ { t + 1 } \right) . } \end{array}\tag{27}
$$

Through the derivation of equations (26) and (27), it can be derived that optimal policy $\pi _ { u }$ is a Boltzmann policy at inverse temperature Âµ [14]:

$$
\begin{array} { c } { { \pi _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) = \pi _ { 0 } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) \exp \left[ \mu Q _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) - \mu V _ { u } ( s ^ { t } ) \right] } } \\ { { = \pi _ { 0 } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) \exp \left[ \mu A _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) \right] , } } \end{array}\tag{28}
$$

where $A _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right) = Q _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right) - V _ { u } ( s ^ { t } )$ is a softened advantage function.

By observing $\mathsf { P } 4 ^ { \prime }$ , it is clear that only $- \gamma ^ { t }$ log $\pi _ { u } ( a _ { u } ^ { t } \vert s ^ { t } ) / \mu$ is related to $\pi _ { u }$ . Therefore, optimizing $\mathrm { P } 4 ^ { \prime }$ with a fixed shared policy $\pi _ { 0 }$ is equivalent to optimizing Q function $Q _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right)$ Then, when task-specific policy $\{ \pi _ { u } \} _ { u \in \mathbb { U } }$ is fixed, the term in equation (23) depending on shared policy $\pi _ { 0 }$ is:

$$
\frac { \lambda } { \mu } \sum _ { u = 1 } ^ { U } \mathbb { E } _ { \pi _ { u } } \sum _ { t \geq 0 } \gamma ^ { t } \log \pi _ { 0 } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) .\tag{29}
$$

In order to obtain the solution of this problem, we can use stochastic gradient ascent [14], which precisely leads to an update for extracting all UAV task-specific policies $\{ \pi _ { u } \} _ { u \in \mathbb { U } }$ as shared policy $\pi _ { 0 } .$

3) The Whole Algorithm: We construct $U + 1$ neural networks corresponding to $U + 1$ optimization parameters in Problem P4, i.e., the shared policy network with optimization parameter $\theta _ { 0 } .$ , and specific policy networks with $\{ \theta _ { u } \} _ { u \in \mathbb { U } } .$ To learn charging scheduling and trajectory design policies for UAVs, the current state, the action, the next state, the reward and the number of rounds of each UAV task are recorded in memory. Then, the learning agent extracts the collected data in batches to train those neural networks.

We train the $U + 1$ networks by two steps. First, we solve Problem $\mathrm { P } 4 ^ { \prime }$ with fixed $\pi _ { 0 }$ and obtain learning values $\{ \theta _ { u } \} _ { u \in \mathbb { U } }$ by training specific policy networks. We set the loss function of specific policy network u by:

$$
L ( \theta _ { u } ) = \mathbb { E } _ { \pi _ { u } } \left[ \left( Q _ { u } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) - \widetilde { Q _ { u } } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) \right) ^ { 2 } \right] , u \in \mathbb { U } ,\tag{30}
$$

where $\widetilde { Q _ { u } } \left( a _ { u } ^ { t } | s ^ { t } \right)$ and $Q _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right)$ are the real Q value of the output of specific policy network u and the expected Q value computed by equation (27), respectively. After that, we train shared policy $\pi _ { 0 }$ to learn parameter $\theta _ { 0 }$ with fixed policy $\pi _ { u } ,$ with the purpose of solving Problem P4. The corresponding loss function is set by:

$$
L ( \theta _ { 0 } ) = \sum _ { u = 1 } ^ { U } \mathbb { E } _ { \pi _ { u } } \sum _ { t \geq 0 } \gamma ^ { t } \log \pi _ { 0 } \left( a _ { u } ^ { t } \middle | s ^ { t } \right) .\tag{31}
$$

Finally, we use the Adma optimizer [14] to train the above neural networks. The training process for the learning agent can be found in Algorithm 1.

Overall, the execution process of the designed algorithm, MURAL, is as follows: First, in time slot t, we obtain optimal device scheduling variable $\{ \alpha _ { m } ^ { t * } \} _ { m \in \mathbb { M } }$ according to the device scheduling policy based on the remaining energy of mobile devices. Second, we design both heuristic and multi-task DRL algorithms. By alternating iterations of heuristic algorithm and multi-task DRL algorithm, we obtain optimal time allocation variable $\tau ^ { t * }$ , optimal UAV scheduling variable $\{ \beta _ { u } ^ { t * } \} _ { u \in \mathbb { U } }$ and optimal UAV coordinate $\{ q _ { u } ^ { t * } \} _ { u \in \mathbb { U } }$ in time slot t. In addition, the execution process of MURAL algorithm can be found in Algorithm 2.

Algorithm 1 Pseudo-Code of Training Processes for The Algorithm 2 Pseudo-Code of MURAL   
Learning Agent   
Input: $\{ f _ { m } \} _ { m \in \mathbb { M } } , \ \{ f _ { u } \} _ { u \in \mathbb { U } } , \ \mathbb { B } , \ N , \delta ^ { 2 } , \ \mathcal { P } _ { 1 } , \varepsilon , \ \epsilon , \ \{ k _ { m } \} _ { m \in \mathbb { M } } .$   
Input: Batch size B, initial shared policy parameter $\theta _ { 0 }$ and $\{ k _ { u } \} _ { u \in \mathbb { U } } , \ \mathring { \{ P }  _ { m } \} _ { m \in \mathbb { M } } , \ \mathring { \{ E }  _ { m } ^ { t - 1 , r } \} _ { m \in \mathbb { M } } , \ \mathring { \{ \mathbb { E } } _ { u } ^ { t - 1 , r } \} _ { u \in \mathbb { U } }$ and tol  
specific policies parameters $\theta _ { 1 } , . . . , \theta _ { u } , . . . , \theta _ { U }$ erance errors $\psi _ { 1 } , \psi _ { 2 }$ and $\psi _ { 3 }$   
Output: Learned policy $\pi _ { 0 } , \pi _ { 1 } , . . . , \pi _ { u } , . . . , \pi _ { U } .$ Output: Average computation efficiency $\begin{array} { r } { \frac { 1 } { t } \sum _ { j = 1 } ^ { t } \eta _ { E E } ^ { j } . } \end{array}$   
1: Initialize initial state and empty memory. 1: Initialize UAV scheduling variable $\{ \beta _ { u } ^ { 0 * } \} _ { u \in \mathbb { U } }$ and UAV   
2: for round $t = 1 , 2 .$ . do location $\{ q _ { u } ^ { 0 * } \} _ { u \in \mathbb { U } } .$ .   
3: for $\mathrm { U A V } \ u = 1 , 2 , \dotsc , U$ do 2: for time slot $t = 1 , 2 \dots$ do   
4: Obtain $Q _ { u }$ and $\pi _ { 0 }$ through UAV-specific policy and 3: Get device scheduling variables $\{ \alpha _ { m } ^ { t * } \} _ { m \in \mathbb { M } }$ based on   
shared policy networks, respectively. the residual energy of devices.   
5: $V _ { u }$ is calculated according to equation (26). 4: for round $i = 1 , 2 \dots$ do   
6: $\pi _ { u }$ is calculated according to equation (28). 5: $\beta _ { u } ^ { t , 0 } = \beta _ { u } ^ { ( t - 1 ) * } , q _ { u } ^ { t , 0 } = q _ { u } ^ { ( t - 1 ) * }$   
7: Select action $a _ { u } ^ { t }$ based on UAV-specific policy $\pi _ { u }$ 6: Obtain time allocation variable $\tau ^ { t , i }$ by solving   
and state $s ^ { t } = \bar { ( } s _ { 1 } ^ { t } , \bar { } . . . , s _ { u } ^ { t } , \bar { } . . . , s _ { U } ^ { \bar { t _ { } } } ) .$ Problem P2 based on $\{ \alpha _ { m } ^ { t * } \} _ { m \in \mathbb { M } } , \{ \beta _ { u } ^ { t , ( i - 1 ) } \} _ { u \in \mathbb { M } }$ and   
8: Obtain device scheduling variable $\{ \alpha _ { m } ^ { t * } \} _ { m \in \mathbb { M } }$ and $\{ q _ { u } ^ { t , ( i - 1 ) } \} _ { u \in \mathbb { M } } .$   
time allocation variable $\tau ^ { t * }$ by solving Problem P2 7: Solve Problem P3 by the learned policy (obtained   
based on action $a _ { u } ^ { t }$ and state $s ^ { t } .$ by Algorithm 1) for given $\{ \alpha _ { m } ^ { t * } \} _ { m \in \mathbb { M } }$ and $\tau ^ { t , i }$   
9: Obtain state $s _ { u } ^ { t + 1 }$ and reward $R _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right)$ by 8: Update $i = i + 1 , \{ \beta _ { u , } ^ { t , i } \} _ { u \in \mathbb { U } }$ and $\{ q _ { u } ^ { t , i } \} _ { u \in \mathbb { U } } .$   
$\{ \alpha _ { m } ^ { t * } \} _ { m \in \mathbb { M } }$ and $\tau ^ { t * }$ 9: $\begin{array} { r } { \mathbf { I f } \sum _ { i ^ { \prime } = 1 } ^ { i } \| \beta _ { u } ^ { t , i ^ { \prime } } - \dot { \beta } _ { u } ^ { t , ( \bar { i } ^ { \prime } - 1 ) } \| \leq \psi _ { 1 } , \sum _ { i ^ { \prime } = 1 } ^ { i } \| q _ { u } ^ { t , i ^ { \prime } } - } \end{array}$   
10: Store experience $\left\{ s _ { u } ^ { t } , a _ { u } ^ { t } , s _ { u } ^ { t + 1 } , R _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right) , t \right\}$ in the $q _ { u } ^ { t , ( i ^ { \prime } - 1 ) } \| \leq \psi _ { 2 }$ and $\begin{array} { r } { \sum _ { i ^ { \prime } = 1 } ^ { i } \| \tau ^ { t , i ^ { \prime } } - \tau ^ { t , ( i ^ { \prime } - 1 ) } \| \le \psi _ { 3 } } \end{array}$   
replay memory. 10: $\beta _ { u } ^ { t * } \stackrel { \cdot \cdot } { = } \beta _ { u } ^ { t , i } , q _ { u } ^ { t * } = \overline { { q } } _ { u } ^ { t , i } , \tau ^ { t * } = \tau ^ { t , i } .$   
11: sitionwith size 11: Break.   
$\{ s _ { u } ^ { t } , \bar { a } _ { u } ^ { t } , s _ { u } ^ { t + 1 } , R _ { u } \left( a _ { u } ^ { t } | s ^ { t } \right) , t \}$ $B .$ 12: end if   
12: Derive gradient $\nabla _ { \boldsymbol { \theta } _ { u } }$ for all of the episodes in the 13: end for   
batch based on equation (30).   
13: Train UAV-specific policy network u with gradient 14: Update 15: end for $t = t + 1 .$   
$\nabla _ { \boldsymbol { \theta } _ { u } }$ by Adam optimizer.   
14: end for   
15: Sample a batch of state transition fully connected layers of each UAV-specific policy network   
$\{ s ^ { t } , \stackrel { \cdot } { a ^ { t } } , s ^ { t + 1 } , R \left( a ^ { t } | s ^ { t } \right) , t \}$ with size B. and the shared policy network. Meanwhile, variables E, L   
16: Derive gradient $\nabla _ { \theta _ { 0 } }$ for all of the episodes in the batch and B refer to the number of training episodes, the number of   
by equation (31). time slots per episode and the training batch size, respectively.   
17: Train the shared policy network with gradient $\nabla _ { \boldsymbol { \theta } _ { 0 } }$ by Please refer to Appendix E for the proof of Theorem 4.   
Adam optimizer. Theorem 5: The complexity of Algorithm 2 Theorem 5: The complexityofAlgorithm 2 is is   
18: end for

4) Algorithm Complexity Analysis: We perform theoretical analysis of the complexity of the designed multi-task DRL-based algorithm (Algorithm 1) and MURAL algorithm (Algorithm 2) as follows.

Theorem 4: The complexity of Algorithm 1 is ${ \mathcal { O } } { ( L \times E \times } $

$$
B \times \Big ( \sum _ { u = 1 } ^ { U } \sum _ { i = 1 } ^ { \Re - 1 } \iota _ { u , i } \times \iota _ { u , i + 1 } + \sum _ { j = 1 } ^ { \mathbb { S } - 1 } \iota _ { 0 , i } \times \iota _ { 0 , i + 1 } \Big ) \Big ) .
$$

Variables $\ i _ { u , i }$ and $\ i _ { 0 , i }$ represent the number of neurons at layer i of UAV-specific policy network u and the shared policy network, respectively. Variables â and â are the number of $\mathcal { O } \Big ( \sum _ { t = 1 } ^ { N } L _ { t } \Big ( \sum _ { n = 1 } ^ { U } \sum _ { i = 1 } ^ { \mathcal { K } - 1 } \iota _ { u , i } \times \iota _ { u , i + 1 } + M \Big ) \Big )$ Symbol N denotes the number of time slots required for the execution of MURAL algorithm. Meanwhile, $L _ { t } , \ t \in ( 0 , N )$ denotes the number of iterations required to obtain the optimal scheduling results for both UAVs and mobile devices in time slot t.

Please refer to Appendix F for the proof of Theorem 5.

## V. PERFORMANCE EVALUATION

## A. Simulation Setup

In order to evaluate the performance of MURAL, we conducted a set of experiments by Python 3.9 and Pytorch 1.8.1. As shown in Fig. 4, we verify the performance utilizing a city map of Manhattan. We choose an area of 1km Ã1km indicated by the red line, where the laser emitter is positioned in the area center, and APs are uniformly distributed in this area. According to Manhattan mobility model [25], pedestrians holding mobile devices are treated as mobile devices. The settings of simulated parameters are based on [11], [25] and [12], and can be found in Table II.

Because existing studies fail to take into account joint task scheduling and trajectory optimization for multiple UAVs and multiple devices in UAV-assisted WPMEC networks, we evaluate the proposed algorithm, MURAL, versus the following four solutions:

<!-- image-->  
Fig. 4. The city map of Manhattan.

â¢ TEAM [30]: It is a multi-agent DRL-based scheduling algorithm for multiple UAVs, tending to minimize energy consumption of UAVs by charging scheduling and trajectory design.

â¢ SCR [31]: It is a DRL-based resource allocation algorithm to improve system throughput. We apply it in our system. For the time allocation variable, we use a DNN to optimize it. For others, we use a Lagrangian duality method to solve them.

â¢ No Scheduling of Devices (NSD): UAV charging scheduling and trajectory design are set the same with our algorithm, while without device charging scheduling.

â¢ Offloading Only (OO): All tasks are offloaded to UAVs for processing without local computation.

## B. Simulation Results

1) Learning Performance Evaluation: The training curve of MURAL in Fig. 5 is obtained by deploying 4 APs and 4 UAVs to serve 40 devices. Note that the reward is set according to the objective function defined in equation (19), which includes the total number of computation bits of devices, energy consumption of both devices and UAVs. It is clearly shown that the obtained reward for each episode remains under $2 . 5 \times 1 0 ^ { 6 }$ at the beginning and increases from episode 10, iterating to convergence in episode 380. First, at the beginning, the learning agent selects random actions to explore the environment and its dynamics. Second, the shared policy network and UAV-specific policy networks are trained by all the experiences learned from exploration steps to optimally serve mobile devices. These two steps allow the learning agent to avoid different penalties and optimize placements of UAVs. This can significantly increase the rewards obtained by UAVs. Furthermore, it is worth noting that the designed MURAL algorithm has good convergence performance, with rewards gradually achieving convergence when the training episodes reach about 380, where dynamic environmental features and strategy exploration lead to fluctuations in rewards.

<!-- image-->  
Fig. 5. Reward per episode in MURAL (the number of UAVs, APs and mobile devices is 4, 4 and 40, respectively).

TABLE II  
SIMULATION PARAMETERS
<table><tr><td>Parameter description</td><td>Value</td></tr><tr><td>The number of UAVs</td><td>{4,5,6,7,8}</td></tr><tr><td>The number of APs</td><td>{4,5,6,7,8,9}</td></tr><tr><td>The number of mobile devices</td><td>{20,40,60,80,100}</td></tr><tr><td>The length of each time slot</td><td>1s</td></tr><tr><td>The bandwidth</td><td>1MHz</td></tr><tr><td>Transmission power of mobile devices</td><td>0.1W</td></tr><tr><td>CPU frequency of each mobile device</td><td>500MHz</td></tr><tr><td>CPU frequency of each UAV</td><td>2.5 GHz</td></tr><tr><td>Required CPU of tasks</td><td>50 cycles/bit</td></tr><tr><td>Transmission power of APs</td><td>60W</td></tr><tr><td>Transmission power of the laser emitter</td><td>200W</td></tr><tr><td>Energy harvesting efficiency of mobile devices</td><td></td></tr><tr><td>Energy harvesting efficiency of UAVs</td><td>0.5</td></tr><tr><td>The flight altitude of the each UAV</td><td>0.8</td></tr><tr><td>The maximum moving speed of mobile</td><td>10m</td></tr><tr><td>devices</td><td>20 km/h</td></tr><tr><td>The learning rate for training models</td><td>0.001</td></tr><tr><td>The batch size</td><td>128</td></tr></table>

2) Performance Under Different Numbers of Mobile Devices: Fig. 6a shows the performance of average computation efficiency as defined by equation (10) for TEAM, SCR, NSD, OO and the proposed algorithm, MURAL, under different numbers of mobile devices. We can discover that the average computation efficiency of MURAL is higher than the other four algorithms. It is because our algorithm aims to maximize the average computation efficiency by joint resource scheduling and UAV trajectory control. TEAM algorithm uses multi-agent DRL to determine scheduling variables and trajectories of UAVs, aiming at minimizing the UAVâs energy consumption. Therefore, its performance on average computation efficiency is not as good as that of MURAL algorithm.

SCR is a DRL-based time allocation and resource scheduling algorithm that first fixes the energy collection period and device scheduling, and then solves the charging scheduling and trajectory design problem for UAVs by Lagrangian duality method. Then, the energy collection period and device scheduling are derived by an approximation algorithm. However, only the maximum computation bits per device is considered in the optimization process, without considering the long-term computation efficiency. Therefore, its performance on average computation efficiency is close to that of TEAM.

<!-- image-->  
(a) Average energy efficiency

<!-- image-->  
(b) Average numbers of computation bits

<!-- image-->  
(cï¼ Average energy consumption  
Fig. 6. Performance with different numbers of mobile devices (the number of UAVs and APs is 4 and 4, respectively).

Although NSD shares the same UAV charging scheduling and trajectory design with our algorithm, it uses a fixed energy collection period and does not consider computation scheduling for devices. Since it does not fully utilize computational resources in the system, its average computation efficiency is lower than that of MURAL, TEAM and SCR algorithms. Finally, the OO algorithm only relies on computation offloading from devices to UAVs without considering the deviceâs local computational capability, which leads to lower performance than the other four algorithms. When the number of mobile devices increases, the average computation efficiency of all algorithms increases. The reason for this is that more mobile devices generate more computation tasks. Compared to energy consumption of devices and UAVs, the flight energy consumption caused by UAVs to reach the optimal communication location is relatively large and only varies slightly with the increasing number of devices. Thus, the average computation efficiency of the five algorithms increases with the number of devices.

The performance of average numbers of computation bits under different amounts of mobile devices is shown in Fig. 6b. Average numbers of computation bits are defined by lim $\begin{array} { r } { \frac { 1 } { t } \sum _ { j = 1 } ^ { t } \sum _ { m = 1 } ^ { M } L _ { m } ^ { j } } \end{array}$ . We note that the average numtââ bers of computation bit of MURAL is higher than those of TEAM, NSD and OO algorithms, while lower than that of SCR algorithm. Thatâs because SCR algorithm solves a deterministic optimization problem by DRL to maximize the computation bits. Whereas, our work aims to maximize average computation efficiency by a designed multi-task learning algorithm. In addition, TEAM, which focuses on reducing the energy consumption of UAVs based on multi-agent DRL, and NSD, which does not conduct device charging scheduling, have moderate performance. Finally, the OO algorithm, which considers only computation offloading, has the worst performance, because it ignores the local computing power of mobile devices.

The performance of the average energy consumption for different amounts of mobile devices is illustrated in Fig. 6c, which is defined by lim $\begin{array} { r } { \frac { 1 } { t } \sum _ { j = 1 } ^ { t } ( \sum _ { m = 1 } ^ { M } E _ { m } ^ { j } + \sum _ { u = 1 } ^ { U } \mathbb { E } _ { u } ^ { j } ) } \end{array}$ tââ We can find that the average energy consumption of TEAM algorithm is the lowest, because it always chooses UAV location that have the minimum energy consumption of the flight. In order to maximize the computation bit, SCR algorithm usually selects UAV locations with better communication conditions, resulting in higher UAV flight energy consumption compared to the other four algorithms. Both NSD and OO algorithms have lower average energy consumption than our proposed algorithm, due to merely considering computation offloading without local processing. Therefore, the average energy consumption of MURAL is less than that of SCR algorithm and more than that of TEAM, NSD and OO.

3) Performance Under Different Numbers of APs: Fig. 7 shows the impact of different numbers of APs on system performance. The performance of the average computation efficiency under different numbers of APs is shown in Fig. 7a. When the number of APs increases, the average computation efficiency increases as well. It can be found that the average computation efficiency of all algorithms tends to be stable when the number of APs is 7. This is because the number of APs mainly affects the energy collection process of devices. When the number of APs is 7, most devices can collect enough energy to meet the energy demand in each time slot. Therefore, when the maximum CPU frequency and the maximum transmission power of the device are fixed, the number of APs can be chosen by 7 to reach good system performance under current settings.

Fig. 7b and Fig. 7c show the trend of average numbers of computation bits and average energy consumption with different numbers of APs, respectively. Similarly, it can be found that the average numbers of computation bits and the average energy consumption gradually increase with the increasing number of APs when it is less than 7. This is because with the increasing number of APs, the amount of energy collected by devices for local computation and task offloading also increases. Thus, the computation bits increase with the number of APs.

Likewise, with the increase in the collected energy of devices, its computation and transmission energy consumption gradually increases, and UAVs also needs to consume more energy for more offloaded data. Therefore, the energy consumption of each algorithm is proportional with the amount of APs. In addition, the average numbers of computation bits and the average energy consumption tend to be stable when the number of APs is bigger than 7. This is because when the number of APs is bigger than or equal to 7, the majority of devices can collect enough energy to support their operations. Thus, when the number of APs changes from 7 to 9, the variation of the average energy consumption and average numbers of computation bits of the system tends to be smooth out.

<!-- image-->  
(a) Average energy efficiency

<!-- image-->  
(b) Average numbers of computation bits

<!-- image-->  
(cï¼ Average energy consumption

Fig. 7. Performance with different numbers of APs (the number of UAVs and mobile devices is 4 and 40, respectively).  
<!-- image-->  
(a) Average energy efficiency

<!-- image-->  
(b) Average numbers of computation bits

<!-- image-->  
(cï¼ Average energy consumption  
Fig. 8. Performance with different numbers of UAVs. (The number of APs and mobile devices is 4 and 40, respectively.)

4) Performance Under Different Numbers of UAVs: The performance of average computation efficiency under different numbers of UAVs is illustrated in Fig. 8a, while Fig. 8b and Fig. 8c show the trend of average numbers of computation bits and average energy consumption under different amount of UAVs, respectively. By observing Fig. 8a, it can be found that the performance of all algorithms is similar with that shown in Fig. 6a, i.e., MURAL has the lowest average computation efficiency, and TEAM algorithm is the next, while SCR, NSD and OO are less efficient. By observing Fig. 8b, it can be noticed that the average numbers of computation bits increase gradually when the number of UAVs increases. The reason is that, devices have more options to offload tasks with more UAVs. In addition, we can find that the performance of all algorithms in Fig. 8c is also similar to that of Fig. 6c, i.e., the SCR algorithm has the highest average energy consumption, and MURAL algorithm is the second, and NSD, OO, and TEAM algorithms are the lowest.

Moreover, the flight energy consumption of one UAV is usually higher than computation and transmission energy consumption of devices (e.g., 5 W for one UAV flying in one time slot and 0.0625 W for one device in total). Therefore, as shown in Fig. 8c, the average energy consumption of each algorithm increases significantly with the increasing number of UAVs. It can be observed that when the amount of UAVs is increasing, the average computation efficiency is decreasing, as shown in Fig. 8a. Compared to the average energy consumption, the average numbers of computation bits fluctuate less with the change in the number of UAVs. Thus, it reflects the fact that the average computation efficiency decreases when the amount of UAVs increases.

5) The Performance of Execution and Convergence Time: The execution time of the five algorithms is illustrated in Fig. 9a. MURAL contains U + 1 neural networks and trains them based on the collected data batches, so it has the longest execution time. Next, due to the fact that TEAM also requires training multiple neural networks to predict the trajectories of UAVs, its execution time is only lower than that of our proposed algorithm. By considering that SCR algorithm only uses 1 DNN, it results in lower execution time than MURAL and TEAM algorithms. However, NSD and OO algorithms do not have the training process. The NSD algorithm does not consider computation scheduling of devices, while the OO algorithm only takes into account the offloading of tasks to the UAV and does not concern charging scheduling and time allocation of mobile devices. The execution time of the five algorithms also becomes long when the number of mobile devices increases. This is due to the fact that when the number of devices grows, the determination of device scheduling and time allocation variables becomes more complex, and the decision of charging scheduling and location coordinates of UAVs becomes more difficult and thus takes more time.

<!-- image-->

<!-- image-->  
Fig. 9. Performance of execution and convergence time.

Fig. 9b shows the convergence time of MURAL, TEAM and SCR algorithms. We can observe that the convergence time of the three algorithms becomes longer when the number of mobile devices increases. Thatâs because more devices result in more complex task scheduling, time allocation and UAV trajectory design, with correspondingly longer convergence time. Furthermore, we can note that the convergence speed of MURAL is between those of TEAM and SCR algorithms. This is because TEAM algorithm is based on multi-agent DRL, which requires distributed training of multiple agents to optimize trajectories of UAVs. As a result, it has the slowest convergence speed. In addition, our proposed MURAL algorithm is based on multi-task DRL, which requires only one learning agent to learn charging scheduling and trajectory design of multiple UAVs simultaneously. Therefore, MURAL algorithm has a faster convergence speed than TEAM algorithm. Finally, SCR algorithm uses only one DNN to predict time allocation variable, resulting in a faster convergence speed than MURAL and TEAM algorithms.

## VI. CONCLUSION

In this paper, we considered a UAV-assisted WPMEC system that can provide support for human-centric metaverse applications running on mobile devices, and proposed a solution to enable joint charging time allocation, computation task scheduling and trajectory design for both UAVs and mobile devices, with the objective of maximizing the average computation efficiency of the system in a long-term perspective. First, we formulated the computation efficiency maximization problem by considering energy constraints of mobile devices and UAVs. Then, we decomposed it into two subproblems, i.e., optimizing time allocation and charging scheduling of mobile devices, and optimizing charging scheduling and location coordinates of UAVs. After that, we designed a two-stage alternating optimization algorithm based on multi-task DRL, where a heuristic algorithm and a multi-task DRL framework were alternatively used to optimize device and UAV scheduling variables. Finally, the theoretical analysis and performance results demonstrated that our solution has obvious advantages in convergence speed and average computation efficiency.

## APPENDIX A

## PROOF OF THEOREM 1

In Problem P1, scheduling variables $\alpha _ { m } ^ { t }$ and $\beta _ { u } ^ { t }$ are binary. The objective function is the ratio of long-term system computation bits to system energy consumption, expressed by equation (9). Constraints (10a) and (10b) are non-convex functions about device scheduling variable $\alpha _ { m } ^ { t }$ and time allocation variable $\tau ^ { t }$ , and constraint (10c) is a non-convex function about UAV scheduling variable $\beta _ { u } ^ { t }$ and UAV location $q _ { u } ^ { t } .$ Meanwhile, the objective function is a non-convex function about $\alpha _ { m } ^ { t } , \tau ^ { t } , \beta _ { u } ^ { t }$ and $q _ { u } ^ { t }$ . Thus, Problem P1 is a mixed integer non-convex fractional optimization problem. Even without considering time allocation variable $\tau ^ { t }$ and UAV location $q _ { u } ^ { t } ,$ Problem P1 is still an integer linear fractional programming problem, which is also NP-hard [27]. As a result, Problem P1 is NP-hard.

## APPENDIX B

## PROOF OF THEOREM 2

Inequation (10a) can be transformed into the following inequation:

$$
\tau ^ { t } \leq \frac { E _ { m } ^ { t - 1 , r } } { ( \alpha _ { m } ^ { t * } P _ { m } + k _ { m } f _ { m } ^ { 3 } ) T } .\tag{B.1}
$$

In addition, the detailed expression of inequation (10b) is inequation (B.2), as shown at the bottom of the next page, and can be further converted to inequation (B.3), as shown at the bottom of the next page, by mathematical deformation.

Therefore, a further representation of Problem $\mathbf { P } 2 ^ { \prime }$ can be found in equation (B.4), as shown at the bottom of the next page.

By observing inequations (B.4a) and (B.4b), as shown at the bottom of the next page, it can be noted that, to meet energy constraints of both type-1 and type-2 devices, time allocation variable $\tau ^ { t }$ can be confined to the range as expressed in equation (B.5), as shown at the bottom of the next page.

Furthermore, we define A PMm=1 $\begin{array} { r } { ( 2 \alpha _ { m } ^ { t * } - 1 ) \mathbb { B } l o g _ { 2 } \left( 1 + P _ { m } h _ { m u } ^ { t } / \delta ^ { 2 } \right) , B = \sum _ { m = 1 } ^ { M } \Big ( f _ { m } / C _ { 1 } + } \end{array}$ $\begin{array} { r } { ( 1 - \alpha _ { m } ^ { t * } ) \mathbb { B } l o g _ { 2 } ( 1 + P _ { m } h _ { m u } ^ { t } / \delta ^ { 2 } ) \Big ) , C = \sum _ { m = 1 } ^ { M } P _ { m } ( 2 \alpha _ { m } ^ { t * } - 1 ) } \end{array}$ and $\begin{array} { r } { D = \sum _ { m = 1 } ^ { M } ( k _ { m } f _ { m } ^ { 3 } + P _ { m } ( 1 - \alpha _ { m } ^ { t * } ) ) + \sum _ { u = 1 } ^ { U } \Big ( \beta _ { u } ^ { t } k _ { u } { f _ { u } } ^ { 3 } + } \end{array}$ $\zeta _ { 1 } \| \mathbb { V } _ { u } ^ { t } \| ^ { 3 } + \zeta _ { 2 } / \| \mathbb { V } _ { u } ^ { t } \| \Big )$ . Then, we can obtain function $f ( \tau ^ { t } )$ for Problem $\mathbf { P } 2 ^ { \prime }$ as equation (B.6), as shown at the bottom of the next page.

Further, the first-order derivative of $f ( \tau ^ { t } )$ can be computed by:

$$
f ^ { \prime } \left( \tau ^ { t } \right) = \frac { A D - B C } { \left( C \tau ^ { t } + D \right) ^ { 2 } } .\tag{B.7}
$$

By observing equation (B.7), we can find that $f ^ { \prime } \left( \tau ^ { t } \right)$ has no zero point, and thus $f ( \tau ^ { t } )$ is a monotonic function. Since the denominator of $f ^ { \prime } \left( \tau ^ { t } \right)$ is constantly bigger than 0, the polarity of $f ^ { \prime } \left( \tau ^ { t } \right)$ depends on the polarity of $A D - B C$ . When $A D - B C > 0 , \ f ( \tau ^ { t } )$ is a monotonically increasing function and the maximum value is obtained at the upper bound. On the contrary, when $A D - B C < 0 , f ( \tau ^ { t } )$ is a monotonically decreasing function and the maximum value is obtained at the lower bound. The case of $A D - B C = 0$ does not exist, which is further explained in the proof of Corollary 1. Therefore, the optimal solution of Problem $\mathbf { P } 2 ^ { \prime }$ is:

$$
\tau ^ { t * } = \left\{ \begin{array} { l l } { \operatorname* { m i n } \{ \displaystyle \frac { E _ { m } ^ { t - 1 , r } } { T ( \alpha _ { m } ^ { t * } P _ { m } + k _ { m } f _ { m } ^ { 3 } ) } \} , } & { A D - B C > 0 ; } \\ { \operatorname* { m a x } \{ \displaystyle \frac { k _ { m } f _ { m } ^ { 3 } + ( 1 - \alpha _ { m } ^ { t * } ) P _ { m } } { ( 1 - 2 \alpha _ { m } ^ { t * } ) \left( P _ { m } + \varepsilon \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \right) } } \\ { + \displaystyle \frac { - E _ { m } ^ { t - 1 , r } - \varepsilon T \alpha _ { m } ^ { t * } \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } } { T \left( 1 - 2 \alpha _ { m } ^ { t * } \right) \left( P _ { m } + \varepsilon \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \right) } \} , } & { A D - B C < 0 . } \end{array} \right.\tag{B.8}
$$

## APPENDIX C

## PROOF OF COROLLARY 1

According to Theorem 2, we know that the optimal value of $\tau ^ { t }$ is a segmental function concerning the polarity of $A D - B C .$ , in which, variables A, B, C, and D are defined in Theorem 2. Observing the expressions for variables A and C, we find that $\mathbb { B } l o g _ { 2 } \left( 1 + P _ { m } h _ { m u } ^ { t } / \delta ^ { 2 } \right)$ and $P _ { m }$ are constantly bigger than 0, and variables A and C have common factorization $( 2 \alpha _ { m } ^ { t * } - 1 )$ . Therefore, variables A and C have the same polarity.

By multiplying B by time interval T , the following equation can be obtained by:

$$
B \times T = \sum _ { m = 1 } ^ { M } { \left( \frac { f _ { m } T } { C _ { 1 } } + ( 1 - \alpha _ { m } ^ { t * } ) T \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m u } ^ { t } } { \delta ^ { 2 } } \right) \right) } .\tag{C.1}
$$

The physical meaning of equation (C.1) is the number of local computation bits for all devices plus the number of offloaded data bits for type-2 devices. Therefore, variable B is constantly bigger than 0.

By multiplying D by time interval T , the following equation can be obtained by:

$$
\begin{array} { l } { { \displaystyle D \times T = \sum _ { m = 1 } ^ { M } T ( k _ { m } f _ { m } ^ { 3 } + P _ { m } ( 1 - \alpha _ { m } ^ { t * } ) ) } } \\ { { \displaystyle \quad \quad + \sum _ { u = 1 } ^ { U } T \bigg ( \beta _ { u } ^ { t } k _ { u } f _ { u } ^ { 3 } + \zeta _ { 1 } \| \mathbb { V } _ { u } ^ { t } \| ^ { 3 } + \frac { \zeta _ { 2 } } { \| \mathbb { V } _ { u } ^ { t } \| } \bigg ) } } \\ { { \displaystyle \quad = \sum _ { m = 1 } ^ { M } ( E _ { m } ^ { t , l } + T P _ { m } ( 1 - \alpha _ { m } ^ { t * } ) ) + \sum _ { u = 1 } ^ { U } \mathbb { E } _ { u } ^ { t } } , } \end{array}\tag{C.2}
$$

where $E _ { m } ^ { t , l }$ and $E _ { u } ^ { t }$ denote the local energy consumption of device m and the total energy consumption of UAV u in time slot t, respectively. Furthermore, expression $T P _ { m } \left( 1 - \alpha _ { m } ^ { t * } \right)$

(B.2)

$$
\begin{array} { r l r } & { } & { k _ { m } f _ { m } ^ { 3 } T + ( 1 - \tau ^ { t } - \alpha _ { m } ^ { t * } + 2 \alpha _ { m } ^ { t * } \tau ^ { t } ) T P _ { m } \leq E _ { m } ^ { t - 1 , r } + \varepsilon ( 1 - \alpha _ { m } ^ { t * } ) \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \tau ^ { t } T + \varepsilon \alpha _ { m } ^ { t * } \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } ( 1 - \tau ^ { t } ) T , } \\ & { } & { \tau ^ { t } \geq \frac { T k _ { m } f _ { m } ^ { 3 } + T ( 1 - \alpha _ { m } ^ { t * } ) { P _ { m } } - E _ { m } ^ { t - 1 , r } - \varepsilon T \alpha _ { m } ^ { t * } \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } } { T \left( 1 - 2 \alpha _ { m } ^ { t * } \right) \Big ( P _ { m } + \varepsilon \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \Big ) } . } \end{array}\tag{B.3}
$$

$$
\begin{array} { r l } { \mathsf { P 2 ^ { \prime } } : } & { \overset { \mathrm { a n } } { \underset { \tau ^ { i } } { \sum } } \quad \overset { \sum _ { m = 1 } ^ { M } } { \sum } \frac { L _ { m } ^ { t } } { m ! } \overset { L _ { m } ^ { t } } { \sum _ { m = 1 } ^ { M } } \frac { \prime } { L _ { u } ^ { t } } } \\ & { = \operatorname* { m a x } \frac { \tau ^ { t } \sum _ { m = 1 } ^ { M } ( 2 \alpha _ { m } ^ { t _ { * } } - 1 ) \mathbb { B } l o g _ { 2 } ( 1 + \frac { P _ { m } h _ { m } ^ { t } } { \delta ^ { 2 } } ) + \sum _ { m = 1 } ^ { M } ( \frac { f _ { m } } { C _ { 1 } } + ( 1 - \alpha _ { m } ^ { t _ { * } } ) \mathbb { B } l o g _ { 2 } ( 1 + \frac { P _ { m } h _ { m } ^ { t } } { \delta ^ { 2 } } ) ) } { \tau ^ { t } \sum _ { m = 1 } ^ { M } \int _ { m } ( 2 \alpha _ { m } ^ { t _ { * } } - 1 ) + \sum _ { m = 1 } ^ { M } ( k _ { m } f _ { m } ^ { 3 } + P _ { m } ( 1 - \alpha _ { m } ^ { t _ { * } } ) ) + \sum _ { u = 1 } ^ { U } ( \beta _ { u } ^ { t } k _ { u } f _ { u } ^ { 3 } + \zeta _ { 1 } \| \nabla _ { u } ^ { t } \| ^ { 3 } + \frac { \zeta _ { 2 } } { \| \nabla _ { u } ^ { t } \| } ) } , } \\ &  \overset { \mathrm { s . t . } } { \underset { \tau ^ { t } } { \sum } } \quad \overset { \sum _ { m = 1 } ^ { t } }  \frac { \underset { P _ { m } ^ { t - 1 } , r } { \sum _ { m = 1 } ^ { M } } }  \frac { \sum _ { m } ^ { t - 1 } }  ( \alpha _ { m } ^ { t _ { * } } P _ { m } + k _ { m } f _  \end{array}\tag{B.4}
$$

(B.4a)

(B.4b)

$$
\tau ^ { t } \in ( \operatorname* { m a x } _ { m } \{ \frac { T k _ { m } f _ { m } ^ { 3 } + T \left( 1 - \alpha t _ { m } ^ { \star } \right) P _ { m } - E _ { m } ^ { t - 1 , r } - \varepsilon T \alpha _ { m } ^ { t * } \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } } { T \left( 1 - 2 \alpha t _ { m } ^ { \star * } \right) \left( P _ { m } + \varepsilon \widehat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \right) } \} , \operatorname* { m i n } _ { m } \{ \frac { E _ { m } ^ { t - 1 , r } } { \left( \alpha _ { m } ^ { t _ { m } } P _ { m } + k _ { m } f _ { m } ^ { 3 } \right) T } \} ) .\tag{B.5}
$$

$$
\begin{array} { r l } & { f ( \tau ^ { t } ) = \frac { \tau ^ { t } \sum _ { m = 1 } ^ { M } \left( 2 \alpha _ { m } ^ { t * } - 1 \right) \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m * } ^ { t } } { \delta ^ { 2 } } \right) + \sum _ { m = 1 } ^ { M } \left( \frac { f _ { m } } { C _ { 1 } } + ( 1 - \alpha _ { m } ^ { t * } ) \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m * } ^ { t } } { \delta ^ { 2 } } \right) \right) } { \tau ^ { t } \sum _ { m = 1 } ^ { M } P _ { m } \left( 2 \alpha _ { m } ^ { t * } - 1 \right) + \sum _ { m = 1 } ^ { M } \left( k _ { m } f _ { m } ^ { 3 } + P _ { m } \left( 1 - \alpha _ { m } ^ { t * } \right) \right) + \sum _ { u = 1 } ^ { U } \left( \beta _ { u } ^ { t } k _ { u } f _ { u } ^ { 3 } + \zeta _ { 1 } \left\| \nabla _ { u } ^ { t } \right\| ^ { 3 } + \frac { \zeta _ { 2 } } { \| \nabla _ { u } ^ { t } \| } \right) } } \\ & { \qquad = \frac { A \tau ^ { t } + B } { C \tau ^ { t } + D } . } \end{array}\tag{B.6}
$$

is denoted as the transmission energy consumption of type-2 device m in time slot t. Therefore, variable D is constantly bigger than 0.

By multiplying variable C by time interval T , the following equation can be obtained by:

$$
\begin{array} { r l } { \displaystyle } & { \displaystyle { C \times T } = \sum _ { m = 1 } ^ { M } T P _ { m } ( 2 \alpha _ { m } ^ { t * } - 1 ) } \\ & { \displaystyle \phantom { \frac { A ^ { * } } { B ^ { * } \alpha _ { m } ^ { m } } } = \sum _ { m = 1 } ^ { M } ( \alpha _ { m } ^ { t * } T P _ { m } - ( 1 - \alpha _ { m } ^ { t * } ) T P _ { m } ) . } \end{array}\tag{C.3}
$$

The physical meaning of variable C times T is the sum of the transmission energy consumption of all type-1 devices minus the sum of the transmission energy consumption of all type-2 devices. The flight energy consumption of UAVs is known to be one or two orders of magnitude bigger than the transmission energy consumption of the mobile device [9]. Furthermore, $D T - C T$ is constantly bigger than 0. Therefore, variable D is constantly bigger than variable C. By observing the expressions of variables A and B, we find that they belong to the same order of magnitude.

As a result, the polarity of AD â BC depends only on the polarity of variables A and C. By the previous derivation, we can find that the polarity of variable C is consistent with variable A. Therefore, Corollary 1 is proved.

## APPENDIX D

## PROOF OF THEOREM 3

Based on Theorem 2 and Corollary 1, we can derive the following equations:

$$
\tau ^ { t * } = \left\{ \begin{array} { l l } { \operatorname* { m i n } \{ \displaystyle \frac { E _ { m } ^ { t - 1 , r } } { T ( \alpha _ { m } ^ { t * } P _ { m } + k _ { m } f _ { m } ^ { 3 } ) } \} , } & { A D - B C > 0 ; } \\ { \operatorname* { m a x } \{ \displaystyle \frac { k _ { m } f _ { m } ^ { 3 } + ( 1 - \alpha _ { m } ^ { t * } ) P _ { m } } { ( 1 - 2 \alpha _ { m } ^ { t * } ) \left( P _ { m } + \varepsilon \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \right) } } \\ { + \displaystyle \frac { - E _ { m } ^ { t - 1 , r } - \varepsilon T \alpha _ { m } ^ { t * } \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } } { T \left( 1 - 2 \alpha _ { m } ^ { t * } \right) \left( P _ { m } + \varepsilon \hat { h } _ { m } ^ { t } \mathcal { P } _ { 0 } \right) } \} , } & { A D - B C < 0 . } \end{array} \right.\tag{D.1}
$$

It is known that the expression for variable A is denoted by:

$$
\begin{array} { l } { { \displaystyle { \cal A } = \sum _ { m = 1 } ^ { M } ( 2 \alpha _ { m } ^ { t * } - 1 ) \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m u } ^ { t } } { \delta ^ { 2 } } \right) } } \\ { ~ = \displaystyle { \sum _ { m = 1 } ^ { M } \left( \alpha _ { m } ^ { t * } \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m u } ^ { t } } { \delta ^ { 2 } } \right) \right. } } \\ { { \displaystyle \left. - ( 1 - \alpha _ { m } ^ { t * } ) \mathbb { B } l o g _ { 2 } \left( 1 + \frac { P _ { m } h _ { m u } ^ { t } } { \delta ^ { 2 } } \right) \right) } . } \end{array}\tag{D.2}
$$

It is known that expression $\mathbb { B } l o g _ { 2 } \left( 1 + P _ { m } h _ { m u } ^ { t } / \delta ^ { 2 } \right)$ is denoted as the maximum channel capacity between UAV u and mobile device m in time slot t, and $\alpha _ { m } ^ { t * }$ is equal to 1 or 0 indicating that device m is classified as the type-1 device or the type-2 device, respectively. Then, variable A defined in equation (D.2) can be regarded by the sum of channel capacity of all type-1 devices in time slot t minus that of all type-2 devices. When the sum of channel capacity of all type-1 devices equals to that of all type-2 devices, variable A equals to 0. In that case, $\tau ^ { t }$ does not affect the value of $f ( \tau ^ { t } )$ defined in equation (B.6). However, since we consider the scenario where devices move randomly within the region, it is almost impossible that the sum of channel capacity of all type-1 devices happens to be equal to that of all type-2 devices. Therefore, we do not consider the case when variable A equals to 0.

Finally, when variable A is bigger than 0, it means that the sum of channel capacity of type-1 devices is bigger than that of all type-2 devices, $\mathrm { i . e . , ~ } A D - B C > 0 .$ , and time allocation variable $\tau ^ { t * }$ can reach the upper bound of the value domain. Conversely, when variable A is less than 0, it means that the sum of channel capacity of type-1 devices is less than that of all type-2 devices, i.e., $A D \mathrm { ~ - ~ } B C \mathrm { ~ < ~ } 0$ , and time allocation variable $\tau ^ { t * }$ can reach the lower bound of the value domain.

## APPENDIX E

## PROOF OF THEOREM 4

Similar to [30], the complexity of the learning agent is mainly related to the configuration of the neural network. Let $\boldsymbol { \imath } _ { u , i }$ and $\ i _ { 0 , i }$ represent the number of neurons at layer i of UAV-specific policy network u and the shared policy network, respectively. Thus, the total complexity of the shared policy network and UAV-specific policy networks is $\mathcal { O } \Big ( \sum _ { u = 1 } ^ { U } \sum _ { i = 1 } ^ { \infty - 1 } \iota _ { u , i } \times \iota _ { u , i + 1 } + \sum _ { j = 1 } ^ { \mathbb { S } - 1 } \iota _ { 0 , i } \times \iota _ { 0 , i + 1 } \Big )$ , where â and â are the number of fully connected layers of each UAV-specific policy network and the shared policy network. Since UAVspecific policy networks and the shared policy network are alternately optimized and B experience is extracted from replay buffer, the complexity of the training process of the designed multi-task DRL-based algorithm is ${ \mathcal O } \big ( L \times E \times$ $B \times \Big ( \sum _ { u = 1 } ^ { U } \sum _ { i = 1 } ^ { \Re - 1 } \iota _ { u , i } \times \iota _ { u , i + 1 } + \sum _ { j = 1 } ^ { \mathbb { S } - 1 } \iota _ { 0 , i } \times \iota _ { 0 , i + 1 } \Big ) \Big )$ . Therefore, Theorem 4 is proved.

## APPENDIX F

## PROOF THEOREM 5

The complexity of Algorithm 2 comes from two aspects. The first aspect is from computation scheduling and time allocation for mobile devices. The second aspect is from the execution of the learning algorithm to obtain UAV scheduling and trajectory design decision. Let N denote the number of time slots required for the execution of MURAL algorithm. Meanwhile, $L _ { t } , \ t \in ( 0 , N )$ , denotes the number of iterations required to obtain the optimal scheduling results for both UAVs and mobile devices in time slot t. The complexity of the designed heuristic algorithm to realize computation scheduling and time allocation for mobile devices is $\mathcal O ( M )$ , where M is the number of mobile devices. In addition, charging scheduling and trajectory design decision for UAVs can be obtained from trained UAV-specific networks with the complexity of $\mathcal { O } \Big ( \sum _ { u = 1 } ^ { U } \sum _ { i = 1 } ^ { \Re - 1 } \iota _ { u , i } \times \iota _ { u , i + 1 } \Big )$ . Therefore, the complexity of Algorithm 2 is $\mathcal { O } \Big ( \sum _ { t = 0 } ^ { N } L _ { t } \Big ( \sum _ { u = 1 } ^ { U } \sum _ { i = 1 } ^ { \Re - 1 } \iota _ { u , i } \times \iota _ { u , i + 1 } + M \Big ) \Big )$ .

## REFERENCES

[1] M. Xu et al., âA full dive into realizing the edge-enabled metaverse: Visions, enabling technologies, and challenges,â IEEE Commun. Surveys Tuts., vol. 25, no. 1, pp. 656â700, 1st Quart., 2023.

[2] R. Hare and Y. Tang, âHierarchical deep reinforcement learning with experience sharing for metaverse in education,â IEEE Trans. Syst. Man, Cybern. Syst., vol. 53, no. 4, pp. 2047â2055, Apr. 2023.

[3] Y. Zhan, S. Guo, P. Li, and J. Zhang, âA deep reinforcement learning based offloading game in edge computing,â IEEE Trans. Comput., vol. 69, no. 6, pp. 883â893, Jun. 2020.

[4] S. Pan, P. Li, C. Yi, D. Zeng, Y.-C. Liang, and G. Hu, âEdge intelligence empowered urban traffic monitoring: A network tomography perspective,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 4, pp. 2198â2211, Apr. 2021.

[5] Q. Xu, Z. Su, K. Zhang, and P. Li, âIntelligent cache pollution attacks detection for edge computing enabled mobile social networks,â IEEE Trans. Emerg. Topics Comput. Intell., vol. 4, no. 3, pp. 241â252, Jun. 2020.

[6] X. Wang et al., âWireless powered mobile edge computing networks: A survey,â ACM Comput. Surv., vol. 55, no. 13s, pp. 1â37, Jul. 2023, doi: 10.1145/3579992.

[7] Q. Liu, L. Shi, L. Sun, J. Li, M. Ding, and F. Shu, âPath planning for UAV-mounted mobile edge computing with deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 69, no. 5, pp. 5723â5728, May 2020.

[8] Z. Ning, Y. Yang, X. Wang, Q. Song, L. Guo, and A. Jamalipour, âMultiagent deep reinforcement learning based UAV trajectory optimization for differentiated services,â IEEE Trans. Mobile Comput., pp. 1â17, Sep. 2023, doi: 10.1109/TMC.2023.3312276.

[9] Z. Yang, S. Bi, and Y. A. Zhang, âStable online offloading and trajectory control for UAV-enabled MEC with EH devices,â in Proc. IEEE Global Commun. Conf. (GLOBECOM), Dec. 2021, pp. 1â7.

[10] W. Feng et al., âHybrid beamforming design and resource allocation for UAV-aided wireless-powered mobile edge computing networks with NOMA,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3271â3286, Nov. 2021.

[11] W. Liu, S. Zhang, and N. Ansari, âJoint laser charging and DBS placement for drone-assisted edge computing,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 780â789, Jan. 2022.

[12] X. Hu, K.-K. Wong, and Y. Zhang, âWireless-powered edge computing with cooperative UAV: Task, time scheduling and trajectory design,â IEEE Trans. Wireless Commun., vol. 19, no. 12, pp. 8083â8098, Dec. 2020.

[13] Z. Xu, K. Wu, Z. Che, J. Tang, and J. Ye, âKnowledge transfer in multitask deep reinforcement learning for continuous control,â in Proc. NIPS, vol. 33, Dec. 2020, pp. 15146â15155.

[14] Y. W. Teh et al., âDistral: Robust multitask reinforcement learning,â in Proc. NIPS, vol. 30, Dec. 2017, pp. 1â11.

[15] M. Hessel, H. Soyer, L. Espeholt, W. Czarnecki, S. Schmitt, and H. van Hasselt, âMulti-task deep reinforcement learning with PopArt,â in Proc. AAAI, vol. 33, no. 1, Feb. 2019, pp. 3796â3803.

[16] F. Belletti, D. Haziza, G. Gomes, and A. M. Bayen, âExpert level control of ramp metering based on multi-task deep reinforcement learning,â IEEE Trans. Intell. Transp. Syst., vol. 19, no. 4, pp. 1198â1207, Apr. 2018.

[17] Z. Zhang et al., âTowards robust knowledge graph embedding via multitask reinforcement learning,â IEEE Trans. Knowl. Data Eng., vol. 35, no. 4, pp. 4321â4334, Apr. 2023.

[18] Q. Qi et al., âScalable parallel task scheduling for autonomous driving using multi-task deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13861â13874, Nov. 2020.

[19] T. Dong et al., âIntelligent joint network slicing and routing via GCNpowered multi-task deep reinforcement learning,â IEEE Trans. Cognit. Commun. Netw., vol. 8, no. 2, pp. 1269â1286, Jun. 2022.

[20] J. Chen, S. Chen, Q. Wang, B. Cao, G. Feng, and J. Hu, âIRAF: A deep reinforcement learning approach for collaborative mobile edge computing IoT networks,â IEEE Internet Things J., vol. 6, no. 4, pp. 7011â7024, Aug. 2019.

[21] L. Huang, S. Bi, and Y. A. Zhang, âDeep reinforcement learning for online computation offloading in wireless powered mobile-edge computing networks,â IEEE Trans. Mobile Comput., vol. 19, no. 11, pp. 2581â2593, Nov. 2020.

[22] F. Zhou, Y. Wu, R. Q. Hu, and Y. Qian, âComputation rate maximization in UAV-enabled wireless-powered mobile-edge computing systems,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1927â1941, Sep. 2018.

[23] Z. Ning et al., âDynamic computation offloading and server deployment for UAV-enabled multi-access edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 5, pp. 2628â2644, May 2023.

[24] X. Wang, Z. Ning, S. Guo, M. Wen, L. Guo, and H. V. Poor, âDynamic UAV deployment for differentiated services: A multi-agent imitation learning based approach,â IEEE Trans. Mobile Comput., vol. 22, no. 4, pp. 2131â2146, Apr. 2023.

[25] X. Wang, Z. Ning, L. Guo, S. Guo, X. Gao, and G. Wang, âOnline learning for distributed computation offloading in wireless powered mobile edge computing networks,â IEEE Trans. Parallel Distrib. Syst., vol. 33, no. 8, pp. 1841â1855, Aug. 2022.

[26] Z. Ning et al., â5G-enabled UAV-to-community offloading: Joint trajectory design and task scheduling,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3306â3320, Nov. 2021.

[27] W. Ejaz, M. Naeem, and S. Zeadally, âOn-demand sensing and wireless power transfer for self-sustainable industrial Internet of Things networks,â IEEE Trans. Ind. Informat., vol. 17, no. 10, pp. 7075â7084, Oct. 2021.

[28] A. Tomar, L. Muduli, and P. K. Jana, âA fuzzy logic-based ondemand charging algorithm for wireless rechargeable sensor networks with multiple chargers,â IEEE Trans. Mobile Comput., vol. 20, no. 9, pp. 2715â2727, Sep. 2021.

[29] O. Nachum, M. Norouzi, K. Xu, and D. Schuurmans, âBridging the gap between value and policy based reinforcement learning,â in Proc. NIPS, vol. 30, Dec. 2017, pp. 2772â2782.

[30] O. S. Oubbati, M. Atiquzzaman, H. Lim, A. Rachedi, and A. Lakas, âSynchronizing UAV teams for timely data collection and energy transfer by deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 71, no. 6, pp. 6682â6697, Jun. 2022.

[31] S. Zhang, H. Gu, K. Chi, L. Huang, K. Yu, and S. Mumtaz, âDRL-based partial offloading for maximizing sum computation rate of wireless powered mobile edge computing network,â IEEE Trans. Wireless Commun., vol. 21, no. 12, pp. 10934â10948, Dec. 2022.

<!-- image-->

Xiaojie Wang (Senior Member, IEEE) received the Ph.D. degree from the Dalian University of Technology, Dalian, China, in 2019. After that, she was a Post-Doctoral Researcher with The Hong Kong Polytechnic University. Currently, she is a Full Professor with the School of Communication and Information Engineering, Chongqing University of Posts and Telecommunications, Chongqing, China. She has published over 60 scientific papers in international journals and conferences, such as IEEE TRANSACTIONS ON MOBILE COMPUTING,

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, IEEE TRANSACTIONS ON PARALLEL AND DISTRIBUTED SYSTEMS, and IEEE COMMUNICATIONS SURVEYS AND TUTORIALS. Her research interests are wireless networks, mobile edge computing, and machine learning.

<!-- image-->

Jiameng Li received the B.E. degree in electronic information science and technology from Chongqing Normal University, Chongqing, China, in 2021. She is currently pursuing the M.E. degree with the School of Communication and Information Engineering, Chongqing University of Posts and Telecommunications, Chongqing. Her research interests include mobile edge computing, unmanned aerial vehicle, and wireless power transfer.

<!-- image-->

Zhaolong Ning (Senior Member, IEEE) received the Ph.D. degree from Northeastern University, China, in 2014. He was a Research Fellow with Kyushu University, Japan, from 2013 to 2014. Currently, he is a Full Professor with the School of Communication and Information Engineering, Chongqing University of Posts and Telecommunications, Chongqing, China. He has published over 150 scientific papers in international journals and conferences. His research interests include mobile edge computing, 6G networks, machine learning,

and resource management. He has been a Highly Cited Researcher (Web of Science), since 2020. He serves as an Associate Editor and a Guest Editor for several journals, such as IEEE TRANSACTIONS ON VEHICU-LAR TECHNOLOGY, IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, IEEE TRANSACTIONS ON SOCIAL COMPUTATIONAL SYSTEMS, and IEEE INTERNET OF THINGS JOURNAL.

<!-- image-->

Qingyang Song (Senior Member, IEEE) received the Ph.D. degree in telecommunications engineering from The University of Sydney, Australia, in 2007. From 2007 to 2018, she was with Northeastern University, China. She joined the Chongqing University of Posts and Telecommunications in 2018, where she is currently a Professor. She has authored more than 100 papers in major journals and international conferences. Her current research interests include cooperative resource management, edge computing, and connected and autonomous vehicles systems.

She serves on the editorial boards of two journals, including an Area Editor of IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY and an Academic Editor of Digital Communications and Networks.

<!-- image-->

<!-- image-->

Lei Guo received the Ph.D. degree from the University of Electronic Science and Technology of China, Chengdu, China, in 2006. He is currently a Full Professor with the Chongqing University of Posts and Telecommunications, Chongqing, China. He has authored or coauthored more than 200 technical papers in international journals and conferences. His current research interests include communication networks, optical communications, and wireless communications. He is an Editor of several international journals.

Abbas Jamalipour (Fellow, IEEE) received the Ph.D. degree in electrical engineering from Nagoya University, Nagoya, Japan, in 1996. He is a Professor of ubiquitous mobile networking with The University of Sydney. He has authored nine technical books, 11 book chapters, over 550 technical papers, and five patents, all in the area of wireless communications and networking. He is a fellow of the Institute of Electrical, Information, and Communication Engineers (IEICE) and the Institution of Engineers Australia, an ACM Professional Member,

and an IEEE Distinguished Speaker. He has been an Elected Member of the Board of Governors of the IEEE Vehicular Technology Society, since 2014. He was a recipient of the number of prestigious awards, such as the 2019 IEEE ComSoc Distinguished Technical Achievement Award in Green Communications, the 2016 IEEE ComSoc Distinguished Technical Achievement Award in Communications Switching and Routing, the 2010 IEEE ComSoc Harold Sobol Award, the 2006 IEEE ComSoc Best Tutorial Paper Award, and over 15 best paper awards. He has been the General Chair and the Technical Program Chair of several prestigious conferences, including IEEE ICC, GLOBECOM, WCNC, and PIMRC. He was the President of the IEEE Vehicular Technology Society, from 2020 to 2021. Previously, he held the positions of the Executive Vice-President and the Editor-in-Chief of VTS Mobile World. He was the Vice President-Conferences and a member of Board of Governors of the IEEE Communications Society. He sits on the editorial board of IEEE ACCESS and several other journals. He is a member of Advisory Board of IEEE INTERNET OF THINGS JOURNAL. Since January 2022, he has been the Editor-in-Chief of IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY. He was also the Editor-in-Chief of IEEE WIRELESS COMMUNICATIONS.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_2.jpeg|page_4_img_2]]
3. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_3.jpeg|page_4_img_3]]
4. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_4.png|page_4_img_4]]
5. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_5.png|page_4_img_5]]
6. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_6.jpeg|page_4_img_6]]
7. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_7.jpeg|page_4_img_7]]
8. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_8.png|page_4_img_8]]
9. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_9.png|page_4_img_9]]
10. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_10.jpeg|page_4_img_10]]
11. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_11.png|page_4_img_11]]
12. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_12.png|page_4_img_12]]
13. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_13.png|page_4_img_13]]
14. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_14.jpeg|page_4_img_14]]
15. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_15.png|page_4_img_15]]
16. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_16.png|page_4_img_16]]
17. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_17.png|page_4_img_17]]
18. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_18.png|page_4_img_18]]
19. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_19.png|page_4_img_19]]
20. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_20.png|page_4_img_20]]
21. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_21.jpeg|page_4_img_21]]
22. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_22.png|page_4_img_22]]
23. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_23.png|page_4_img_23]]
24. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_24.png|page_4_img_24]]
25. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_25.jpeg|page_4_img_25]]
26. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_26.png|page_4_img_26]]
27. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_27.png|page_4_img_27]]
28. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_28.png|page_4_img_28]]
29. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_29.png|page_4_img_29]]
30. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_30.png|page_4_img_30]]
31. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_31.jpeg|page_4_img_31]]
32. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_32.png|page_4_img_32]]
33. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_33.png|page_4_img_33]]
34. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_34.png|page_4_img_34]]
35. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_35.png|page_4_img_35]]
36. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_36.png|page_4_img_36]]
37. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_37.png|page_4_img_37]]
38. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_38.png|page_4_img_38]]
39. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_39.png|page_4_img_39]]
40. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_40.jpeg|page_4_img_40]]
41. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_41.png|page_4_img_41]]
42. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_42.png|page_4_img_42]]
43. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_43.png|page_4_img_43]]
44. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_44.png|page_4_img_44]]
45. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_45.png|page_4_img_45]]
46. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_46.jpeg|page_4_img_46]]
47. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_47.png|page_4_img_47]]
48. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_48.png|page_4_img_48]]
49. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_49.jpeg|page_4_img_49]]
50. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_50.png|page_4_img_50]]
51. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_51.png|page_4_img_51]]
52. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_52.png|page_4_img_52]]
53. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_53.png|page_4_img_53]]
54. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_54.jpeg|page_4_img_54]]
55. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_55.png|page_4_img_55]]
56. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_56.jpeg|page_4_img_56]]
57. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_57.png|page_4_img_57]]
58. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_58.jpeg|page_4_img_58]]
59. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_59.png|page_4_img_59]]
60. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_60.png|page_4_img_60]]
61. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_61.jpeg|page_4_img_61]]
62. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_62.png|page_4_img_62]]
63. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_63.png|page_4_img_63]]
64. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_64.png|page_4_img_64]]
65. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_65.png|page_4_img_65]]
66. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_66.png|page_4_img_66]]
67. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_67.jpeg|page_4_img_67]]
68. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_68.jpeg|page_4_img_68]]
69. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_69.png|page_4_img_69]]
70. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_70.png|page_4_img_70]]
71. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_71.png|page_4_img_71]]
72. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_72.png|page_4_img_72]]
73. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_73.png|page_4_img_73]]
74. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_74.jpeg|page_4_img_74]]
75. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_75.png|page_4_img_75]]
76. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_76.png|page_4_img_76]]
77. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_77.png|page_4_img_77]]
78. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_78.png|page_4_img_78]]
79. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_79.jpeg|page_4_img_79]]
80. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_80.png|page_4_img_80]]
81. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_81.png|page_4_img_81]]
82. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_82.png|page_4_img_82]]
83. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_83.png|page_4_img_83]]
84. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_84.png|page_4_img_84]]
85. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_85.jpeg|page_4_img_85]]
86. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_86.png|page_4_img_86]]
87. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_87.png|page_4_img_87]]
88. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_88.png|page_4_img_88]]
89. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_89.png|page_4_img_89]]
90. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_90.jpeg|page_4_img_90]]
91. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_91.png|page_4_img_91]]
92. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_92.png|page_4_img_92]]
93. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_93.png|page_4_img_93]]
94. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_94.png|page_4_img_94]]
95. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_95.png|page_4_img_95]]
96. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_96.png|page_4_img_96]]
97. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_97.jpeg|page_4_img_97]]
98. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_98.png|page_4_img_98]]
99. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_99.png|page_4_img_99]]
100. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_100.png|page_4_img_100]]
101. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_101.png|page_4_img_101]]
102. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_102.jpeg|page_4_img_102]]
103. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_103.png|page_4_img_103]]
104. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_104.png|page_4_img_104]]
105. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_105.png|page_4_img_105]]
106. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_106.png|page_4_img_106]]
107. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_107.png|page_4_img_107]]
108. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_108.png|page_4_img_108]]
109. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_109.jpeg|page_4_img_109]]
110. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_110.png|page_4_img_110]]
111. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_111.png|page_4_img_111]]
112. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_112.png|page_4_img_112]]
113. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_113.png|page_4_img_113]]
114. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_114.jpeg|page_4_img_114]]
115. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_115.png|page_4_img_115]]
116. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_116.png|page_4_img_116]]
117. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_117.png|page_4_img_117]]
118. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_118.png|page_4_img_118]]
119. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_119.png|page_4_img_119]]
120. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_120.png|page_4_img_120]]
121. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_121.jpeg|page_4_img_121]]
122. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_122.png|page_4_img_122]]
123. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_123.png|page_4_img_123]]
124. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_124.png|page_4_img_124]]
125. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_125.jpeg|page_4_img_125]]
126. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_126.png|page_4_img_126]]
127. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_127.png|page_4_img_127]]
128. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_128.jpeg|page_4_img_128]]
129. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_129.png|page_4_img_129]]
130. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_130.png|page_4_img_130]]
131. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_131.png|page_4_img_131]]
132. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_132.png|page_4_img_132]]
133. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_133.jpeg|page_4_img_133]]
134. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_134.png|page_4_img_134]]
135. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_135.png|page_4_img_135]]
136. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_136.jpeg|page_4_img_136]]
137. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_137.jpeg|page_4_img_137]]
138. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_138.png|page_4_img_138]]
139. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_139.jpeg|page_4_img_139]]
140. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_140.png|page_4_img_140]]
141. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_141.png|page_4_img_141]]
142. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_142.png|page_4_img_142]]
143. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_143.png|page_4_img_143]]
144. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_144.jpeg|page_4_img_144]]
145. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_145.png|page_4_img_145]]
146. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_146.png|page_4_img_146]]
147. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_147.jpeg|page_4_img_147]]
148. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_148.jpeg|page_4_img_148]]
149. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_149.png|page_4_img_149]]
150. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_150.jpeg|page_4_img_150]]
151. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_151.png|page_4_img_151]]
152. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_152.png|page_4_img_152]]
153. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_153.png|page_4_img_153]]
154. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_154.jpeg|page_4_img_154]]
155. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_155.png|page_4_img_155]]
156. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_156.jpeg|page_4_img_156]]
157. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_157.png|page_4_img_157]]
158. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_158.png|page_4_img_158]]
159. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_159.png|page_4_img_159]]
160. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_160.png|page_4_img_160]]
161. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_161.jpeg|page_4_img_161]]
162. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_162.png|page_4_img_162]]
163. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_163.png|page_4_img_163]]
164. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_164.jpeg|page_4_img_164]]
165. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_165.png|page_4_img_165]]
166. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_166.png|page_4_img_166]]
167. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_167.png|page_4_img_167]]
168. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_168.jpeg|page_4_img_168]]
169. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_169.png|page_4_img_169]]
170. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_170.png|page_4_img_170]]
171. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_171.png|page_4_img_171]]
172. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_172.png|page_4_img_172]]
173. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_173.png|page_4_img_173]]
174. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_174.png|page_4_img_174]]
175. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_175.png|page_4_img_175]]
176. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_176.png|page_4_img_176]]
177. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_177.jpeg|page_4_img_177]]
178. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_178.png|page_4_img_178]]
179. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_179.png|page_4_img_179]]
180. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_180.png|page_4_img_180]]
181. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_181.png|page_4_img_181]]
182. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_182.jpeg|page_4_img_182]]
183. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_183.png|page_4_img_183]]
184. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_184.png|page_4_img_184]]
185. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_185.png|page_4_img_185]]
186. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_186.png|page_4_img_186]]
187. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_187.png|page_4_img_187]]
188. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_188.jpeg|page_4_img_188]]
189. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_189.png|page_4_img_189]]
190. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_190.png|page_4_img_190]]
191. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_191.png|page_4_img_191]]
192. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_192.png|page_4_img_192]]
193. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_193.jpeg|page_4_img_193]]
194. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_194.jpeg|page_4_img_194]]
195. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_195.png|page_4_img_195]]
196. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_196.png|page_4_img_196]]
197. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_197.png|page_4_img_197]]
198. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_198.png|page_4_img_198]]
199. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_199.png|page_4_img_199]]
200. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_200.png|page_4_img_200]]
201. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_201.png|page_4_img_201]]
202. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_202.png|page_4_img_202]]
203. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_203.jpeg|page_4_img_203]]
204. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_204.png|page_4_img_204]]
205. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_205.jpeg|page_4_img_205]]
206. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_206.png|page_4_img_206]]
207. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_207.png|page_4_img_207]]
208. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_208.png|page_4_img_208]]
209. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_209.png|page_4_img_209]]
210. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_210.jpeg|page_4_img_210]]
211. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_211.jpeg|page_4_img_211]]
212. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_212.jpeg|page_4_img_212]]
213. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_213.png|page_4_img_213]]
214. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_214.png|page_4_img_214]]
215. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_4_img_215.png|page_4_img_215]]
216. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_1.png|page_8_img_1]]
217. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_2.png|page_8_img_2]]
218. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_3.jpeg|page_8_img_3]]
219. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_4.png|page_8_img_4]]
220. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_5.jpeg|page_8_img_5]]
221. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_6.png|page_8_img_6]]
222. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_7.png|page_8_img_7]]
223. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_8.png|page_8_img_8]]
224. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_9.png|page_8_img_9]]
225. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_10.png|page_8_img_10]]
226. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_11.jpeg|page_8_img_11]]
227. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_12.png|page_8_img_12]]
228. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_13.png|page_8_img_13]]
229. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_14.png|page_8_img_14]]
230. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_15.png|page_8_img_15]]
231. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_16.png|page_8_img_16]]
232. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_17.png|page_8_img_17]]
233. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_18.png|page_8_img_18]]
234. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_19.png|page_8_img_19]]
235. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_20.png|page_8_img_20]]
236. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_21.png|page_8_img_21]]
237. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_22.png|page_8_img_22]]
238. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_23.png|page_8_img_23]]
239. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_24.png|page_8_img_24]]
240. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_25.png|page_8_img_25]]
241. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_26.png|page_8_img_26]]
242. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_27.jpeg|page_8_img_27]]
243. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_28.png|page_8_img_28]]
244. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_29.jpeg|page_8_img_29]]
245. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_30.png|page_8_img_30]]
246. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_31.png|page_8_img_31]]
247. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_32.jpeg|page_8_img_32]]
248. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_33.png|page_8_img_33]]
249. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_34.png|page_8_img_34]]
250. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_35.png|page_8_img_35]]
251. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_36.png|page_8_img_36]]
252. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_37.png|page_8_img_37]]
253. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_38.png|page_8_img_38]]
254. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_39.png|page_8_img_39]]
255. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_40.jpeg|page_8_img_40]]
256. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_41.png|page_8_img_41]]
257. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_42.png|page_8_img_42]]
258. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_43.jpeg|page_8_img_43]]
259. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_44.png|page_8_img_44]]
260. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_45.png|page_8_img_45]]
261. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_46.png|page_8_img_46]]
262. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_47.jpeg|page_8_img_47]]
263. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_48.png|page_8_img_48]]
264. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_49.png|page_8_img_49]]
265. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_50.jpeg|page_8_img_50]]
266. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_51.png|page_8_img_51]]
267. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_52.png|page_8_img_52]]
268. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_53.png|page_8_img_53]]
269. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_54.jpeg|page_8_img_54]]
270. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_55.png|page_8_img_55]]
271. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_56.png|page_8_img_56]]
272. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_57.png|page_8_img_57]]
273. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_58.png|page_8_img_58]]
274. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_59.png|page_8_img_59]]
275. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_60.png|page_8_img_60]]
276. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_61.jpeg|page_8_img_61]]
277. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_62.png|page_8_img_62]]
278. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_63.png|page_8_img_63]]
279. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_64.jpeg|page_8_img_64]]
280. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_65.jpeg|page_8_img_65]]
281. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_66.jpeg|page_8_img_66]]
282. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_67.png|page_8_img_67]]
283. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_68.jpeg|page_8_img_68]]
284. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_69.png|page_8_img_69]]
285. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_8_img_70.png|page_8_img_70]]
286. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_11_img_1.jpeg|page_11_img_1]]
287. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_11_img_2.jpeg|page_11_img_2]]
288. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_12_img_1.jpeg|page_12_img_1]]
289. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_12_img_2.jpeg|page_12_img_2]]
290. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_12_img_3.jpeg|page_12_img_3]]
291. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_13_img_1.jpeg|page_13_img_1]]
292. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_13_img_2.jpeg|page_13_img_2]]
293. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_13_img_3.jpeg|page_13_img_3]]
294. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_13_img_4.jpeg|page_13_img_4]]
295. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_13_img_5.jpeg|page_13_img_5]]
296. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_13_img_6.jpeg|page_13_img_6]]
297. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_14_img_1.jpeg|page_14_img_1]]
298. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_14_img_2.jpeg|page_14_img_2]]
299. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_17_img_1.jpeg|page_17_img_1]]
300. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_17_img_2.jpeg|page_17_img_2]]
301. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_18_img_1.jpeg|page_18_img_1]]
302. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_18_img_2.jpeg|page_18_img_2]]
303. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_18_img_3.jpeg|page_18_img_3]]
304. [[../extracted_images/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling /page_18_img_4.jpeg|page_18_img_4]]

---

