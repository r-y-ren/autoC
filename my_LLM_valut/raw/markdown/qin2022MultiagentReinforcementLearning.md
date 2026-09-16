# Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Computing for the Internet-of-Things

Zeyu Qin, Student Member, IEEE, Haipeng Yao , Senior Member, IEEE, Tianle Mai , Member, IEEE, Di Wu, Student Member, IEEE, Ni Zhang, and Song Guo , Fellow, IEEE

AbstractâLEO satellite networks have become a necessary supplement to terrestrial networks aiming to provide worldwide, ubiquitous connectivity, especially in complicated areas (e.g., mountains, oceans, and disaster areas) where terrestrial network infrastructures are typically sparingly distributed or unavailable. However, the increasing computation-intensive Internet-of-Things (IoT) applications (e.g., real-time remote monitoring, intelligent transportation) require not only efficient and reliable communication but also massive computing capabilities. Constrained by the battery and computing resources, the computing tasks and data of applications have to be transmitted to remote cloud servers. This bandwidth limitation and high transmission delay in LEO networks will reduce the quality-of-service (QoS) of IoTapplications. Recently, the combination of LEO networks and edge computing (i.e., Satellite Mobile Edge Computing, SMEC) offers significant opportunities to address these problems. The IoT devices can directly get the computing resources directly from satellites rather than remote servers, thus avoiding long-distance transmission. Considering the resource constraints on satellites, offloading policy plays a crucial role in whole system performance. In this paper, we design a hybrid offloading architecture, which applies a centralized training and distributed execution framework. Also, we propose a multi-agent actor-critic reinforcement learning algorithm, where a centralized âcriticâ is augmented with the global network state to ease the training procedure of distributed user equipments (UE) by evaluating the benefits of their decisions, while the UEs can adjust their policies according to the criticâs evaluation and choose their own decisions relying on their observations.

Index TermsâAerial computing, computation offloading, deep reinforcement learning, mobile edge computing, multi-agent system

## 1 INTRODUCTION

HE past few years have witnessed an exponential Tgrowth of various satellites as well as compelling space applications ranging from intelligent transport, and disaster rescue to military surveillance [1]. Satellite networks, particularly low earth orbit (LEO) satellite networks, have become an important complement to terrestrial networks due to their unique benefits, such as global coverage, high resilience, and excellent bandwidth availability. The satellite network could meet global demands for âubiquitous connectionâ of users, particularly in rough terrains like hills and seas [2]. It can also help with emergency communication if the terrestrial network infrastructure is destroyed by natural disasters. Many countries have recently launched over 8800 satellites into orbit, and the number continues to rise [3]. For example, SpaceX Starlink plans to launch 42000 satellites to supply people in need with communication assistance all over the world [4]. Hence, we can infer that LEO satellite networks have incomparable superiority beyond terrestrial networks, realize seamless coverage globally, and display an essential part of daily human life.

However, the growing number of computation-intensive applications (e.g., real-time remote monitoring, intelligent transportation) requires not only efficient and reliable communication but also vast computational power. While the processing capabilities of IoT devices have substantially improved, they are still constrained by the battery and computing resources, especially the lightweight IoT devices [5]. The computation tasks in remote areas must be transmitted to the remote cloud servers for further processing and storage through LEO satellite networks. Considering the large transmission delay and limited bandwidth in the LEO networks, this processing architecture faces challenges in terms of performance, scalability, and efficiency, making it complicated to satisfy the real-time demands of some latencysensitive applications (e.g., self-driving, hotspot tracking) [6].

<!-- image-->  
Fig. 1. Computation offloading architecture in SMEC.

The combination of LEO networks and edge computing (SMEC) networks has recently received a large quantity of attention from both academia and industry [7]. As shown in Fig. 1, the SMEC architecture could take full advantage of the computing resources of satellites, where UEs can directly get the computing resources directly from satellites rather than remote servers, thus avoiding long-distance transmission. While this offloading mechanism can enhance application performance and reduce power consumption for IoT devices, it is not a panacea for improving performance [8]. On the one hand, satellitesâ computing and storage capacities are still limited, so that it is impractical to offload all tasks to satellites. On the other hand, the offloading process also incurs extra power consumption (i.e., transmitting power) and transmission delays (e.g., fronthaul link transmission delay). Therefore, how to design effective computation offloading schemes plays a crucial role.

Current offloading schemes largely rely on the centralized framework, where a centralized scheduler constantly gathers global system information and then calculates the optimal offloading decisions [9]. While the advantages of centralized architecture are obvious (e.g., quick convergence, global optimum), it incurs too much communication and computation overhead, especially to the large scale LEO network [10]. Whenever the requirements of UEs changes, the scheduler has to collect massive information across the entire system and recalculate the offloading decision. Besides, when the scheduler node experience a hardware failure or is attacked, the entire system may be paralyzed [11].

To handle these challenges, there has been an increasing amount of literature focusing on distributed offloading schemes. Compared to the centralized schemes, each UE can make the offloading decision only according to its local observation [12]. However, as a distributed system, learning from nodes with only local observation and control is difficult, especially when the goal is global optimization [13]. The distributed solutions are confronted with the seriously non-convergence problem.

Therefore, in this paper, we design a hybrid computation offloading architecture and adopt a centralized training and distributed execution framework [14]. In our architecture, we introduced a centralized platform to gather global information and all UEsâ actions to facilitate the learning procedure whilst all distributed actors are able to perform functions independently, relying on their local observations. Benefiting from the framework, multiple UEs can work cooperatively, while each UE can still select and perform its action only according to their local observation independently. In order to compare our algorithm with other stateof-the-art solutions, we performed extensive and in-depth simulations to evaluate our proposed algorithm.

The main contributions of our paper are summarized as follows.

We consider a three-tier computation offloading architecture in LEO satellite networks. The offloading optimization problem is formulated with two objectives, minimizing task delay and reducing energy consumption.

We proposed a hybrid computation offloading architecture and adopted a centralized training and distributed execution framework. The centralized platform takes advantage of global system states to ease the training procedure of the distributed UEs whilst the distributed UEs can make decisions according to their local observations.

We conducted extensive simulations to illustrate the convergence and efficiency of our algorithm.

The rest of this paper is organized as follows. We discuss the related work in Section 2. Then, we discuss the system model and problem formulation in Section 3. In Section 4, we proposed the multi-agent deep reinforcement learning algorithm aided computation offloading problem. In Section 5, the simulation result is presented to demonstrate the feasibility and performance of our algorithm. and the conclusion is in Section 6.

## 2 RELATED WORK

Lately, a significant number of literature has been published on computation offloading in satellite networks. In the following, we would like to talk about the related works from the aspect of satellite networks and machine learning-based schemes.

## 2.1 Computation Offloading in Satellite Networks

Recently, a significant and growing body of literature has looked into computation offloading in satellite networks. And lots of work has been done on the ground-air-space merged network. In [15], Alsharoa et al. proposed a frequency partitioning algorithm to optimize resource allocations in the short-term stage and a shrink-and-realign algorithm to optimize locations of high-altitude platforms in the long-term stage. In [16], Cheng et al. proposed a corporate virtual machine(VM) assignment mechanism in the groundair-space merged network to allocate the computational resources to the virtual machines efficiently. In [17], Liu et al. introduced a task-oriented approach to the ground Cair Cspace unified network to decrease response time and implement smart networking capacities. Meanwhile, a large number of scholars have achieved important progress in the comprehensive optimization of various conditions of the satellite network. In [18], Han et al. took the dynamic and complex characteristics of space-based information networks into consideration and introduced a scheduling algorithm loaded on December 24,2025 at 04:12:49 UTC from IEEE Xplore. Restrictions apply for LEOs. In [19], Zhang et al. designed an effective network virtualization technique to jointly allocate the network resources to promote the communication quality of the mobile equipment. In [20], Wang et al. introduced a computation offloading framework and designed an iterative approach to seek the Nash equilibrium. In [21], Guo et al. proposed an intelligent computation offloading scheme to reduce the systemâs energy cost by jointly optimizing spectrum, and energy, including computation resource allocation. In [22], Guo et al. proposed an offline dynamic programming approach to achieve optimal energy efficiency, and the approach shows good adaptability. Current solutions mainly focus on the task offloading from satellites to ground devices and do not consider the need for offloading computation tasks from IoT devices in remote areas.

TABLE 1 List of Main Notations
<table><tr><td>Parameter Definition</td><td></td></tr><tr><td> $M$ </td><td>Number of LEOs</td></tr><tr><td> $K$ </td><td>NumberofUEs</td></tr><tr><td> $p _ { i , n } ^ { S }$ </td><td>Transmission power when offloading  $T _ { i , n }$  to LEOs</td></tr><tr><td> $p _ { i , n } ^ { M }$ </td><td>Transmission power when offloading  $T _ { i , n }$  to cloud server</td></tr><tr><td> $R _ { i , j } ^ { S }$ </td><td>Transmission rate between UEi and LEOj</td></tr><tr><td> $R _ { i } ^ { M }$ </td><td>Transmission rate between  $U E _ { i }$  andcloud server</td></tr><tr><td> $D _ { S } ^ { t r }$ </td><td>Transmission delay between UEi and LEOj</td></tr><tr><td> $D _ { M } ^ { t r }$ </td><td>Transmission delaybetween UEi andcloud server</td></tr><tr><td> $E _ { S } ^ { t r }$ </td><td>Transmission energy consumption between UEi and LEOj</td></tr><tr><td> $E _ { M } ^ { t r }$ </td><td>Transmission energy consumption between UEi and cloud server</td></tr><tr><td> $D _ { l } ^ { c o m }$ </td><td>Computation delay for processing the task locally</td></tr><tr><td> $D _ { S } ^ { c o m }$ </td><td>Computation delay for processing the task on  $L E O _ { j }$ </td></tr><tr><td> $D _ { M } ^ { c o m }$ </td><td>Computation delay for processing the task on cloud server</td></tr><tr><td> $E _ { l } ^ { c o m }$ </td><td>Computation energy consumption for processing the task locally</td></tr><tr><td> $E _ { S } ^ { c o m }$ </td><td>Computation energy consumption for processing the task on  $L E O _ { j }$ </td></tr><tr><td> $E _ { M } ^ { c o m }$ </td><td>Computation energy consumption for processing the task on cloud server</td></tr><tr><td> $C _ { i , n } ^ { l }$ </td><td>Total cost for processing  $T _ { i , n }$  locally</td></tr><tr><td> $C _ { i , j , n } ^ { S }$ </td><td>Total cost for offloading  $T _ { i , n }$  to  $L E O _ { j }$ </td></tr><tr><td> $C _ { i , n } ^ { M }$ </td><td>Total cost for offloading  $T _ { i , n }$  to the cloud server</td></tr></table>

## 2.2 Computation Offloading With Machine Learning

Besides, we notice that lots of works have studied multi-tier task offloading problems. Current solutions can be roughly divided into two categories: centralized and distributed. The centralized algorithm decides the offloading location based on global information and it is thus easy to converge to the global optimum. In [23], Huang et al. proposed applying deep reinforcement learning to solve the binary computation offloading problem in radio-powered mobile edge computing(MEC). In [24], Song et al. decomposed the computation offloading problem in satellite networks into twolayered subproblems and proposed the resource allocation algorithm. The outcomes of the proposed simulation revealed that the introduced algorithm betters complete offloading and local computing entirely. In [25], Chen et al.

<!-- image-->  
Fig. 2. Offloading system model.

and proposed a high-efficiency distributed algorithm to offload computation-intensive tasks in blockchain-empowered IoT to the MEC servers based on potential game theory and prove to reach a Nash equilibrium. In [26], Zhao et al. constructed a three-tier task offloading algorithm to optimize the task computing delay and energy cost based on a discrete particle swarm optimization algorithm. However, the centralized controller needs to collect a lot of information, which will lead to excessive communication overhead. This disadvantage is more obvious in large-scale LEO networks. Therefore, some research focuses on the distributed architecture, where the agents can decide the offloading location independently and immediately. In [27], Zhan et al. proposed applying proximal policy optimization to help making decisions on how to offload tasks and when to offload tasks. In [28], Liu et al. proposed a distributed task transfer method based on the counterfactual multi-agent reinforcement learning algorithm to solve the task transfer problem caused by mobility of distributed users. However, in distributed algorithms, agents often face the problem of slow convergence and difficulty in achieving global optimality.

## 3 SYSTEM MODEL AND PROBLEM FORMULATION

In the section, we firstly introduce the SMEC architecture. Then, we discuss the system model and problem formulation. For better perception, we list the notations that appeared in the paper in Table 1.

## 3.1 Network Model

In this paper, we consider a SMEC system consisting of multiple LEO satellites and cloud servers [29]. As shown in Fig. 2, a three-tier SMEC is presented, where tier1 consists of several $U E s = \{ U E _ { 1 } , U E _ { 2 } , \cdot . . . , U E _ { K } \}$ , tier2 consists of multiple $L E O s = \{ L E O _ { 1 } , L E O _ { 2 } , . . . , L E O _ { M } \}$ , and tier3 consists Â¼ f gof several cloud servers. We make the assumption that every UE can directly communicate with the LEO satellite, and each LEO satellite can directly connect to the cloud server. The MEC servers are deployed at each satellite, which has varying computing and storage capabilities. Notably, we consider the optimization of computation task offloading decisions on small time scales in this paper. Therefore, we treat the satellite as quasi-static and ignore the task handover between the satellites.

<!-- image-->  
Fig. 3. Dependency among computational tasks.

## 3.2 Task Dependency Model

We assume that the applications on UEs are constantly generating computing tasks. The task of $U E _ { i }$ is denoted as $T _ { i } ,$ which can be split into a sequence of sub-tasks (e.g., user interaction task, image compression task, and sensor data processing task), and each sub-task is interdependent on the others. The dependencies indicate what needs to be done before a sub-task can begin, which can be divided into two categories: timing dependency and data dependency. The timing dependency refers to the relationship between nearby computing tasks in terms of time sequence. One sub-task cannot be completed until the sub-tasks on which it is dependent have been completed. Data dependency refers to the relationship between nearby computing subtasks in terms of data transport. The computation result of the first sub-task is required for the processing of the second.

In this section, the dependencies are denoted by a directed acyclic graph (DAG) $g = ( T _ { i } , L ) ,$ , where $T _ { i } = \{ T _ { i , 1 } { : }$ $T _ { i , 2 } , T _ { i , 3 } , . . . \dot { , } T _ { i , n } \}$ Â¼ Ã° Ã Â¼represents a set of sub-tasks and $L =$ $\{ l ( T _ { i , p } , T _ { i , q } ) | T _ { i , p } , T _ { i , q } \in T \}$ Â¼represents the set of dependencies f Ã° Ãj 2 gamong the computing sub-tasks. $l ( T _ { i , p } , T _ { i , q } ) = \mathsf { 0 }$ denotes Ã° Ãthere is no dependency relationship between $T _ { i , p }$ and $T _ { i , q }$ while $l ( T _ { i , p } , T _ { i , q } ) = 1$ denotes that $T _ { i , q }$ could not be processed before $T _ { i , p }$ Ã Â¼is executed. As shown in Fig. 3, the task could be split into seven sub-tasks, and the sub-task $t _ { 1 }$ must first be processed, and the sub-task $t _ { 7 }$ must be processed at last. For every step, the tasks that can be processed form an available task set M and when M is not empty, the UEs will choose one of them to process.

Besides, the n-th sub-task of $U E _ { i }$ is denoted as $T _ { i , n } =$ $\{ r _ { i , n } , c _ { i , n } , t _ { i , n } ^ { m a x } \}$ , where $r _ { i , n }$ is the data size, $c _ { i , n }$ Â¼is the total f gcomputation resource requirement, which is quantified as the number of CPU cycles in this paper, and $t _ { i , n } ^ { m a x }$ is the maximum latency constraints.

Besides, we denote the offloading decision of $U E _ { i }$ for $T _ { i , n }$ as $X _ { i , n } = \{ x _ { i , n , 0 } , x _ { i , n , 1 } , x _ { i , n , 2 } \}$ , where $x _ { i , n , 0 } = 1$ means to exe-Â¼ fcute the sub-task locally, $x _ { i , n , 1 } = 1$ Â¼means to offload the Â¼computing sub-task to the satellites, and $x _ { i , n , 2 } = 1$ means Â¼to offload the sub-task to the cloud server. It is worth noting that every UE can only offload the sub-task to a certain satellite if the UE decided to offload the task to satellites. When $X _ { i , n , 1 } = 1$ , the UE will offload the sub-task to the Â¼nearest satellites. Correspondingly, we define a transmission power vector $P _ { i , n } = \stackrel { \bullet } { \{ p _ { i , n } ^ { S } , p _ { i , n } ^ { M } \} }$ , where $p _ { i , n } ^ { S }$ denotes the Â¼ f gtransmission power when the sub-task is offloaded to the satellites, and $p _ { i , n } ^ { M }$ denotes when the sub-task is offloaded to the cloud server.

## 3.3 Communication Model

In this paper, we consider two offload schemes as discussed above. The UEs can directly offload the task to the satellites or to the cloud server [30]. To calculate the end-to-end latency and energy consumption, we present the communication model in this part. Since the computation resultâs data size is much smaller than that of the task, we do not consider the resultâs transmission delay and the transmission power [31]. We denote the transmission rate between the i-th user equipment UE and m-th LEO $L E O _ { m }$ as $R _ { i , m } ^ { T } ,$ which can be denoted as:

$$
R _ { i , m } ^ { T } = W _ { i , m } l o g _ { 2 } \Biggl ( 1 + \frac { p _ { i , s } ^ { S } g _ { i , s } } { \sigma ^ { 2 } + \sum _ { l = 1 } ^ { M } \sum _ { k = 1 , k \neq i } ^ { K } p _ { k , l } ^ { S } g _ { i , m } } \Biggr ) ,\tag{1}
$$

where $W _ { i , m }$ is the link bandwidth of $U E _ { i }$ to $L E O _ { j } , \sigma ^ { 2 }$ is the noise power, and $g _ { i , m }$ sis the channel gain. Then, the transmission delay can be calculated by:

$$
D _ { T } ^ { t r } = \frac { r _ { i , n } } { R _ { i , j } ^ { S } } ,\tag{2}
$$

where $r _ { i , n }$ is the data size of the task. Besides, the transmission energy consumption can be formulated as:

$$
E _ { T } ^ { t r } = p _ { i , s } ^ { S } \times D _ { S } ^ { t r } .\tag{3}
$$

In contrast, when UEi decides to offload $T _ { i , n }$ to cloudserver, the transmission rate of $U E _ { i }$ to $L E O _ { j }$ can be formulated as:

$$
R _ { i , j } ^ { S } = W _ { i , j } l o g _ { 2 } \bigg ( 1 + \frac { p _ { i , s } ^ { M } g _ { i , s } } { \sigma ^ { 2 } + \sum _ { l = 1 } ^ { M } \sum _ { k = 1 , k \neq i } ^ { K } p _ { k , l } ^ { S } g _ { i , s } } \bigg ) ,\tag{4}
$$

where $W _ { i , j }$ denotes the link bandwidth of $U E _ { i }$ to $L E O _ { j }$ and $g _ { i , s }$ is the channel gain. Similarly, we can calculate the transmission rate of $L E O _ { j }$ to cloudserver as:

$$
R _ { j } ^ { M } = W l o g _ { 2 } \bigg ( 1 + \frac { p _ { s , m } g _ { s , m } } { \sigma ^ { 2 } + \sum _ { q = 1 } ^ { N } \sum _ { l = 1 , l \ne s } ^ { M } p _ { l , q } g _ { l , q } } \bigg ) .\tag{5}
$$

In full-duplex two-hop computation offloading, the LEO serves as the relay node and is capable of transmitting and receiving at the same time. In this way, the transmission rate of the UE is limited by the lower transmission rate of the two links. Therefore, the transmission rate $R _ { i } ^ { M }$ of $U E _ { i }$ to cloudserver can be re-formulated as:

$$
R _ { i } ^ { M } = M i n ( R _ { i , j } ^ { S } , R _ { j } ^ { M } ) .\tag{6}
$$

Then, the transmission delay between $U E _ { i }$ to cloudserver can be calculated by:

$$
D _ { M } ^ { t r } = \frac { r _ { i , n } } { R _ { i } ^ { M } } .\tag{7}
$$

In addition, the transmission power consumption can be formulated by:

$$
E _ { M } ^ { t r } = p _ { i , s } ^ { M } \times D _ { M } ^ { t r } .\tag{8}
$$

## 3.4 Computation Model

We next discuss the computing task, processing model. When a task is executed locally, the processing delay of the task could be calculated by:

$$
D _ { l } ^ { c o m } = \frac { c _ { i , n } } { f _ { i } ^ { l } } ,\tag{9}
$$

where $c _ { i , n }$ denotes the total computation resource requirement, $f _ { i } ^ { l }$ denotes local computing resources of $U E _ { i }$ . The energy consumption can be formulated as:

$$
E _ { l } ^ { c o m } = e _ { i } ^ { l } \times c _ { i , n } ,\tag{10}
$$

where $e _ { i } ^ { l }$ is the energy consumption of the unit computing resource of $U E _ { i }$ .

When $U E _ { i }$ decides to offload the task to $L E O _ { j } ,$ the processing delay can be calculated by:

$$
D _ { S } ^ { c o m } = \frac { c _ { i , n } } { f _ { i , j } ^ { S } } ,\tag{11}
$$

where $f _ { i , j } ^ { S }$ is the computing resources allocated to $U E _ { i }$ . The computation energy consumption can be calculated by:

$$
E _ { i , j , n } ^ { c o m } = e _ { j } ^ { S } \times c _ { i , n } ,\tag{12}
$$

where $e _ { j } ^ { S }$ represents the energy consumption per unit computing resource of $L E O _ { j }$

When $U E _ { i }$ decides to offload the task to cloudserver, the processing delay can be calculated by:

$$
D _ { M } ^ { c o m } = \frac { c _ { i , n } } { f _ { i } ^ { M } } ,\tag{13}
$$

where $f _ { i } ^ { M }$ represents the computing resources allocated to $U E _ { i }$ . The computation energy consumption can be calculated by:

$$
E _ { i , n } ^ { c o m } = e _ { j } ^ { M } \times c _ { i , n } ,\tag{14}
$$

where $e _ { j } ^ { M }$ represents the energy consumption per unit computing resource of cloudserver.

## 3.5 Problem Formulation

In this paper, the offloading optimization problem can be formulated with two objectives, minimizing task delay and reducing energy consumption. And to evaluate the offloading strategy, the cost function is defined as follows. When UEi decides to execute Taskn locally, the cost can be defined as: $C _ { i , n } ^ { l } = \phi _ { 1 } D _ { l } ^ { c o m } + \phi _ { 2 } E _ { l } ^ { c o m } .$ ; when $U E _ { i }$ decides to offload Taskn to $L E O _ { j } .$ Ã¾ f, the cost can be calculated by: $C _ { i , i , n } ^ { S } = \phi _ { 3 } ( D _ { S } ^ { t r } +$ $D _ { S } ^ { c o m } + D _ { T } ^ { t r } ) \stackrel { \cdot } { + } \phi _ { 4 } ( E _ { S } ^ { t r } + E _ { S } ^ { c o m } + E _ { T } ^ { t r } ) .$ ; when $U E _ { i }$ Â¼ f Ã° Ã¾decides to offÃ¾ Ã Ã¾ f Ã° Ã¾ Ã¾ Ãload Taskn to cloudserver, the cost can be defined as: $C _ { i , n } ^ { M } =$ $\phi _ { 5 } ( D _ { M } ^ { t r } + D _ { M } ^ { c o m } + D _ { T } ^ { t r } ) + \phi _ { 6 } ( E _ { M } ^ { t r } + E _ { M } ^ { c o m } + E _ { T } ^ { t r } )$ , where $\phi _ { 1 } , \phi _ { 2 } ,$ $\phi _ { 3 } , \phi _ { 4 } , \phi _ { 5 } , \phi _ { 6 }$ Ã¾ Ã Ã¾ f Ã° Ã¾ Ã¾ Ã f fare the weights for computation and transmisf f f fsion. Then we can define the cost function of $U E _ { i }$ as:

$$
C o s t _ { i } = x _ { i , n , 0 } C _ { i , n } ^ { l } + x _ { i , n , 1 } C _ { i , j , n } ^ { S } + x _ { i , n , 2 } C _ { i , j , n } ^ { M } ,\tag{15}
$$

Therefore, the offloading optimization problem of task offloading can be formulated as:

$$
m i n \sum _ { i = 1 } ^ { T a s k _ { n u m } } \sum _ { n = 1 } ^ { N } x _ { i , n , 0 } C _ { i , n } ^ { l } + x _ { i , n , 1 } C _ { i , j , n } ^ { S } + x _ { i , n , 2 } C _ { i , j , n } ^ { M } ,\tag{16}
$$

st.

$$
\begin{array} { r l } & { C _ { 1 } : \langle x _ { i , n , 0 } , x _ { i , n } , x _ { i , n } , z \in \{ 0 , 1 \} } \\ & { C _ { 2 } : \langle x _ { i , n , 0 } , + x _ { i , n , 1 } + x _ { i , n , 2 } = 1 } \\ & { C _ { 3 } : \langle x _ { i , n , 0 } D _ { i } ^ { ( i \setminus j ) } + x _ { i , n , 1 } ( D _ { i } ^ { ( i \setminus j ) } + D _ { S } ^ { ( m ) } ) + } \\ & { \qquad x _ { i , n , 2 } ( D _ { i } ^ { ( i \setminus j ) } + D _ { i } ^ { ( i \setminus j ) } ) \leq t _ { i , n } ^ { \operatorname* { m a x } } } \\ & { C _ { 4 } : \rho _ { i , n } ^ { \beta } , p _ { i , n } ^ { \lambda \beta } \leq P _ { i } ^ { m a x } } \\ & { C _ { 5 } : \displaystyle \sum _ { i = 1 } ^ { K _ { j } } x _ { i , n , 1 } f _ { i , j } ^ { \lambda } < f _ { S _ { j } } ^ { m a x } } \\ & { C _ { 6 } : \displaystyle \sum _ { i = 1 } ^ { K } x _ { i , n , 2 } f _ { i } ^ { \lambda \beta } < f _ { M } ^ { m a x } } \end{array}\tag{17}
$$

where $C _ { 1 }$ indicates that the offloading decisions variables are 0-1 binary, $C _ { 2 }$ indicates that each user can choose only one offloading decision for each task, $C _ { 3 }$ indicates that the delay of each offloading method cannot exceed the maximum acceptable delay of the task, $C _ { 4 }$ indicates that the UEâs transmission power couldnât go beyond the maximum power for transmission, $C _ { 5 }$ indicates that the computational resource occupied cannot exceed the total computational resources of the LEO when multiple UEs offload tasks to the same LEO, and $C _ { 6 }$ indicates that the computation resource occupied couldnât go beyond the total computing resources of the cloud server when multiple UEs offload tasks to cloud servers.

## 4 MULTI-AGENT DEEP REINFORCEMENT LEARNING ALGORITHM

In this section, we first formulate the cooperation of UEs as a Partially Observable Markov Decision Process (POMDP). Then, we design a multi-agent reinforcement learning-based algorithm to solve the computation offloading problem.

## 4.1 Partially Observable Markov Decision Process

We can model the multiple computation tasks offloading decision process on the UEs as a partially observable Markov decision process (POMDP) [32]. Formally, a POMDP model can be described as a 6-tuple

$$
P = ( S , A , T , R , O , \gamma ) ,
$$

where $S = \{ s _ { 1 } , s _ { 2 } , . . . , s _ { n } \}$ denotes the state space, $A =$ $\{ a _ { 1 } , a _ { 2 } , . . . . , a _ { m } \}$ g Â¼denotes the action space, T denotes the conf  gditional transition probabilities $T ( \bar { s } ^ { \prime } | s , a )$ , R denotes the immediate reward function $R : S \times A = R , O = \{ o _ { 1 } , o _ { 2 } , . . . - , o _ { n } \}$  Â¼denotes the agentâs local observation, and $\gamma \in [ 0 , 1 ]$  gis the disg 2 Â½ count factor. For every step, every UE obtains its own observation $o _ { i }$ and then chooses its action $a _ { i }$ based on current policy $\pi _ { i } .$ . After each UE performing its actions, the environpment would produce an immediate reward R. Meanwhile, the state of s will change to a new state $s ^ { \prime } .$ The object of RL agents is to learn a strategy that will maximize the discounted cumulative reward $\begin{array} { r } { R _ { i } = \sum _ { t = 0 } ^ { T } \gamma ^ { t } r _ { i } ^ { t } } \end{array}$

Â¼ Â¼ gSpecifically, in the proposed scenario, the observation space could be defined as $\bar { o _ { i , n } } = \{ P _ { i } ^ { m a x } , e _ { i } ^ { l } , f _ { i } ^ { l } , g _ { i , j } , T _ { i , n } \}$ , where

<!-- image-->  
Fig. 4. Multi-agent system of computation offloading.

$P _ { i } ^ { m a x }$ represents the maximum transmission power of $U E _ { i } , e _ { i } ^ { l }$ represents the energy consumption of per unit computing resource of $U E _ { i } , f _ { i } ^ { l }$ represents the total amount of computing resources of $U E _ { i } , g _ { i , j }$ j represents the channel gain of the wireless link between $U E _ { i }$ and $L E O _ { j } ,$ and $T _ { i , n } = \{ r _ { i , n } , c _ { i , n } , t _ { i , n } ^ { m a x } \}$ Â¼ f grepresents the requirements of the task. The action space of actori can be defined as a $\ c t i o n _ { i , n } = \{ x _ { i , n } , p _ { i , n } \}$ , where $x _ { i , n } =$ $\{ x _ { i , n , 0 } , x _ { i , n , 1 } , x _ { i , n , 2 } \}$ Â¼ f g Â¼represents the userâs offloading decision, $p _ { i , n } = \{ p _ { i , n } ^ { s } , p _ { i , n } ^ { m } \}$ gindicates the transmission power, $x _ { i , n , 0 } .$ $x _ { i , n , 1 } , x _ { i , n , 2 } \in \{ 0 , 1 \}$ indicates the three locations can use to 2 f gexecute the computation tasks, and $\{ p _ { i , n } ^ { s } , p _ { i , n } ^ { m } \} \in \left( 0 , p _ { i } ^ { m a x } \right)$ f g 2 Ã° Ãdenotes the transmission power when offloading tasks to satellites and cloud servers. Itâs worth mentioning that the three actions in the action space is not optional at all times. For example, when the computational resource is not sufficient to complete the task, the $x _ { i , n , 2 }$ could not be set to 1. In addition, we set the reward as ${ r _ { i , n } } = - ( { x _ { i , n , 0 } } { c _ { i , n } ^ { l } } + { x _ { i , n , 1 } } { c _ { i , j , n } ^ { s } } +$ $x _ { i , j , 2 } c _ { i , j , n } ^ { m } )$ Â¼ Ã° Ã¾ Ã¾. The goal of each agent is learning a strategy to Ãchoose the best action $\{ x _ { i , n } , p _ { i , n } \}$ according to the current f gstate to maximize the discounted reward $\begin{array} { r } { R _ { i } = \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } r _ { i } ^ { t } } \end{array}$

## 4.2 Multi Agent Deep Reinforcement Learning Algorithm

Learning in the multi-agent system is far more complicated than in the single-agent system, caused by the non-stationary problem [33]. In this paper, we design a multi-agent deep reinforcement learning algorithm (MADRL) to enable each UE to get the optimal offloading strategy. MADRL adopts the actor-critic-based framework. A critic is used to evaluate the action chosen by the actor function, where the critic is responsible for estimating the value function, and the actor is responsible for updating the policy distribution according to the criticâs advise. As shown in Fig. 4, the MADRL architecture consists of multiple distributed actors and a logically centralized critic. In this paper, the actors are deployed at each UE, and the centralized critic platform is deployed at the cloud servers.

During the execution, each actor observes the environment and then selects the corresponding action according to the current strategy. As mentioned above, it is unrealistic to enable each UE to obtain global network information in the actual deployment. Therefore, the observation of each UE only contains local information. Besides, each UE does not know other UEsâ actions and the MEC serversâ current load. This is because of the assumption that each UE may not be willing to share its actions with other UEs. Therefore, Actoriâs local observation $o _ { i , n }$ contains the computational capability and energy consumption per unit computing resource of the UE, the required resource of the task, and the current conditions of the wireless channel.

We consider N agents with policies $\boldsymbol \mu = [ \mu _ { 1 } , \mu _ { 2 } , . . . , \mu _ { N } ] ,$ which parameterized by $\theta = [ \theta _ { 1 } , \theta _ { 2 } , . . . , \theta _ { N } ]$ Â¼ Â½m m m. For each actor $i ,$ u Â¼ Â½u u u the gradient of the expected reward for a certain agent can be calculated by:

$$
\begin{array} { r l } & { \nabla _ { \theta _ { i } } J ( \mu _ { i } ) = E _ { x , a \sim D } [ \nabla _ { \theta _ { i } } \mu _ { i } ( a _ { i } | o _ { i } ) G r a d _ { Q } ] , } \\ & { w h e r e \ G r a d _ { Q } = \nabla _ { a _ { i } } Q _ { i } ^ { \mu } ( x , a _ { 1 } , . . . , a _ { n } ) | _ { a _ { i } = \mu _ { i } ( o _ { i } ) } , } \end{array}\tag{18}
$$

where the $x = ( o _ { 1 } , o _ { 2 } , . . . , o _ { n } )$ is the global network information and the $a _ { 1 } , . . . . , a _ { n }$ Ãis the joint action. Note that a replay buffer $D = \{ x , x ^ { \prime } , a _ { 1 } , \ldots , a _ { n } , r _ { 1 } , \ldots , r _ { n } \}$ is adopted to handle Â¼ f gthe non-stationary data distribution issue.

In Eq. (18), the $Q _ { i } ^ { \mu } ( x , a _ { 1 } , . . , a _ { n } )$ is the centralized $' \mathrm { c r i t i c ^ { \prime \prime } C } \mathrm { - }$ Ã° Ãfunction, which takes as input the globe network information $x = ( o _ { 1 } , o _ { 2 } , . . . , o _ { n } )$ and joint actions $a _ { 1 } , . . . . , a _ { n } .$ . In our architec-Â¼ Ã° Ãture, the centralized critic is deployed at the cloud server, which is used to guide each actor to work in a cooperative way. The loss function of $Q _ { i } ^ { \mu } ( x , a _ { 1 } , . . , a _ { n } )$ can be calculated by:

$$
\begin{array} { r l } & { L ( \theta _ { i } ) = E _ { x , a , r , x ^ { \prime } } [ ( Q _ { i } ^ { \mu } ( x , a _ { 1 } , a _ { 2 } , \ldots , a _ { n } ) - y ) ^ { 2 } ] , } \\ & { w h e r e \ y = r _ { i } + \gamma Q _ { i } ^ { \mu ^ { \prime } } ( x ^ { \prime } , a _ { 1 } ^ { \prime } , a _ { 2 } ^ { \prime } , \ldots , a _ { N } ^ { \prime } ) . } \end{array}\tag{19}
$$

As shown in Eq. (19), we adopt the target network $Q _ { i } ^ { \mu ^ { \prime } }$ to make the learning processing more stable, where $\mu ^ { \prime } =$ $\{ \mu _ { 1 } ^ { \prime } , \mu _ { 2 } ^ { \prime } , . . . , \mu _ { n } ^ { \prime } \}$ m Â¼denotes the parameter of delayed updated fm m m gtarget network. Besides, for each criticâs Q-function, note that we assume that each critic knows the strategies of other actors. Considering the privacy issues, the UEs may not be willing to share their offloading strategies with each other. Therefore, to meet this requirement, we maintain the estimates of other agentsâ strategies. Concretely, we use $\hat { \mu } _ { \phi _ { \cdot } ^ { j } }$ to denote the estimation of $A g e n t _ { i } { ' } \mathbf { s }$ strategy to $A g e n t _ { j } ,$ mfi where $\phi _ { i } ^ { j }$ denotes the parameter of the estimation strategy. We take fadvantage of maximum likelihood estimation to estimate the strategy, and we add an entropy of the policy distribution H to it so that the policy wonât be too certain. Then the loss function can be calculated by:

$$
L ( \phi _ { i } ^ { j } ) = - E _ { o _ { j } , a _ { j } } [ l o g { \hat { \mu } _ { \phi _ { i } ^ { j } } } ( a _ { j } | o _ { j } ) + \lambda H ( { \hat { \mu } _ { \phi _ { i } ^ { j } } } ) ] .\tag{20}
$$

Through minimizing this cost function, we can obtain an estimate of the strategy of other agents. Then, the Eq. (19) can be reformulated as:

$$
\hat { y } = r _ { i } + \gamma Q _ { i } ^ { \mu ^ { \prime } } ( x ^ { \prime } , \mu _ { i } ^ { ' 1 } ( o _ { 1 } ) , \mu _ { i } ^ { ' 2 } ( o _ { 2 } ) , . . . , \mu _ { i } ^ { ' n } ( o _ { n } ) ) .\tag{21}
$$

As mentioned above, since each agentâs strategy is constantly updated in the multi-agent setting, the underlying environment is not stable for a particular agent anymore. In the face of the competitive tasks proposed in this article that may compete for bandwidth and computing resources, the agent may learn an overly strong and fragile strategy. The overly strong strategy is only effective for the current strategy adopted by other agents, so when other agents update their loaded on December 24,2025 at 04:12:49 UTC from IEEE Xplore. Restrictions apply.

TABLE 2  
Simulation Parameters Configuration
<table><tr><td>Simulation Parameter</td><td>Value</td></tr><tr><td>Bandwidth of the wireless channel between UEsand LEOs</td><td>15-30 MHz</td></tr><tr><td>Bandwidth of the wireless channel between LEOs and cloud servers</td><td>50-100 MHz</td></tr><tr><td>Computation tasks&#x27;data size Amount of CPU cycles demanded by task</td><td>7-15Mb</td></tr><tr><td>Transimission power of UEs</td><td> $0 . 5 - 0 . 9 \times 1 0 ^ { 9 }$  50-100 mW</td></tr><tr><td>Transimission power of LEOs</td><td>200-300mW</td></tr><tr><td>Computational ability of UEs</td><td>0.1-1GHz</td></tr><tr><td>Computational ability of LEOs</td><td></td></tr><tr><td>Computational ability of cloud server</td><td>5-6 GHz</td></tr><tr><td>Energy cost of UEs</td><td>14-18GHz</td></tr><tr><td></td><td>0.5-1J/GHz</td></tr><tr><td>Energy cost of LEOs Energy cost of cloud server</td><td>0.3-0.5J/GHz 0.1-0.3J/GHz</td></tr></table>

strategies, the effectiveness of this strong strategy may become very poor. To solve this problem, we train K in different strategies for each agent. That is, the strategy $\mu _ { i }$ of the i-th magent is a set of K sub-strategies. During every training episode, we just use one sub-strategy $\mu _ { i } ^ { ( k ) }$ . For each agent, we maim to maximize the total reward of its strategy set.

$$
\begin{array} { c } { { \nabla _ { \theta _ { i } ^ { ( k ) } } J ( \mu _ { i } ) = \displaystyle \frac { 1 } { K } E _ { x , a \sim D } [ \nabla _ { \theta _ { i } ^ { ( k ) } } \mu _ { i } ^ { ( k ) } ( a _ { i } | o _ { i } ) G r a d _ { Q } , } } \\ { { w h e r e \ G r a d _ { Q } = \nabla _ { a _ { i } } Q _ { i } ^ { \mu } ( x , a _ { 1 } , . . . , a _ { n } ) | _ { a _ { i } = \mu _ { i } ^ { ( k ) } ( o _ { i } ) } ] } } \end{array}\tag{22}
$$

The multi-agent reinforcement learning aided computation offloading algorithm is shown in Algorithm 1.

Algorithm 1. The MADRL Algorithm for Computation   
Offloading in SMEC   
1: Randomly initialize the parameters of the critic network   
and the actor network   
2: Initialize the parameters of the target network and replay   
buffer R   
3: for episode 1 to episodes amount do   
4: Â¼  Initialize the SMEC scenario with randomly parameters   
5: for step 1 to max episode length do   
6: Â¼  Each IoT device get its local observation o   
7: Each IoT device chooses an action a according to o and   
current policy   
8: Each IoT device receives the immediate reward r from   
environment, and obtains the next observation o   
9: Save $( o , a , r , o ^ { \prime } )$ to the replay buffer R   
10: end for   
11: for agent k 1 to agent number do   
12: Â¼  Randomly sample a minibatch $( o _ { j } , a _ { j } , r _ { j } , x _ { j } ^ { \prime } )$ from the   
replay buffer R   
13: Update critic network through minimizing the loss   
function $( \theta _ { ) } = E _ { x , a , r , x ^ { \prime } } [ ( Q _ { i } ^ { \mu } ( x , a _ { 1 } , a _ { 2 } , \ldots , a _ { n } ) - y ) ^ { 2 } ]$   
14: Ã°uÃ Â¼ Â½Ã° Ã°Update actor network by the function   
$\begin{array} { r } { \hat { \nabla _ { \theta _ { i } } } J ( \mu _ { i } ) = E _ { x , a \sim D } [ \nabla _ { \theta _ { i } } \hat { \mu _ { i } } ( a _ { i } | o _ { i } ) G r a d _ { Q } ] , } \end{array}$   
$\underset { \ldots } { w h e r e } \ G r a d _ { Q } = \nabla _ { a _ { i } } Q _ { i } ^ { \mu } ( x , a _ { 1 } , . . . , a _ { n } ) | _ { a _ { i } = \mu _ { i } ( o _ { i } ) }$   
15: end for   
16: Update the parameters of the target network of the critic   
and the agents $\theta _ { i } ^ { Q ^ { \prime } }  \tau \theta _ { i } ^ { Q } + ( 1 - \overline { { \tau } } ) \theta _ { i } ^ { Q ^ { \prime } }$   
$\theta _ { i } ^ { \mu ^ { \prime } }  \tau \theta _ { i } ^ { \mu ^ { \prime } } + ( 1 - \bar { \tau } ) \theta _ { i } ^ { \mu ^ { \prime } }$   
u 17: end for

TABLE 3 MADRL Parameters Configuration
<table><tr><td>Parameter</td><td>MADRL</td></tr><tr><td>Maximum step per episode</td><td>25</td></tr><tr><td>Maximum episode number</td><td>15000</td></tr><tr><td>Discount factor (y)</td><td>0.96</td></tr><tr><td>number of network layers</td><td>3</td></tr><tr><td>Learning rate for Adam optimizer (Î±)</td><td>0.01</td></tr><tr><td>Experience batch size</td><td>500 episodes</td></tr><tr><td>number of neurons per layer</td><td>64</td></tr><tr><td>Target network</td><td>True</td></tr><tr><td>Action Space</td><td>Discrete</td></tr><tr><td>Savemodel rate</td><td>1000</td></tr><tr><td>batch size</td><td>1024</td></tr></table>

## 5 SIMULATION RESULTS

In this section, we present simulation results to evaluate the feasibility and performance of our algorithm. We run the simulation on a host with a GPU installed, where the CPU is an Intel(R) Xeon(R) Gold 5218R CPU @ 2.10 GHz. The size of the hard disk is 512 G. We set up the simulation environment with python 3.5.4 and we implement the algorithm by TensorFlow 1.8.0. In our experiment, the bandwidth of the wireless channel between UEs and LEOs is equally distributed between 15 MHz to 30 MHz. The bandwidth of wireless channels between LEOs and cloud servers is equally distributed between 50 MHz to 100 MHz. The computation tasksâ data size is equally distributed between 7Mb to 15Mb. The amount of CPU cycles demanded by the task is equally distributed between $\mathrm { 0 . 5 \times 1 0 ^ { 9 } }$ to $0 . 9 \times 1 0 ^ { 9 }$

## 5.1 Experiment Configuration

In our experiment, with the cloud server on the earth, the LEOs are evenly distributed within the range of 500 km to 2000 km from the cloud server, and the UEs are evenly distributed within the range of 500 km to 2000 km from the LEOs. To evaluate the convergence performance of our algorithm under different load conditions, we set up the following four experiment topology. The first topology contains 1 cloud server, 1 LEO, and 2UEs. The second topology contains 1 cloud server, 2 LEOs, and 4UEs. The third topology contains 1 cloud server, 3 LEOs, and 9UEs. The fourth topology contains 1 cloud server, 4 LEOs, and 16UEs. The detailed parameters in the experiment are given in Table 2 and We randomly choose the bandwidth, noise power, and channel gain within the range.

## 5.2 Convergence Analysis

Besides, the parameters of our MADRL algorithm is given in Table 3 and the architecture of MADRL algorithm is shown in Fig. 5.

## 5.3 Baseline Algorithms

In this paper, we set three baseline algorithms to evaluate the effectiveness of our algorithm. The first baseline algorithm is Deep Deterministic Policy Gradient (DDPG) [34]. DDPG is a classical single-agent actor-critic reinforcement learning algorithm, where the actor and critic share the same state space. The connection between actor and critic in DDPG is as follows: The actor observes the environment and chooses an exact action while the critic takes the actorâs action and observation as input and outputs the value of the chosen action. The goal of the critic update is to accurately evaluate the value of the actorâs actions, while the goal of the actor update is to maximize the criticâs evaluation. The second baseline algorithm is the Local Execution algorithm (LE) [35]. In LE, every user chooses to execute the tasks locally. The third baseline algorithm is Random Action (RA) [36]. In RA, the user randomly selects the offloading decision to execute tasks and randomly allocates transmission power.

<!-- image-->  
Fig. 5. MADRL algorithm architecture.

<!-- image-->

(a) 1X2agent  
<!-- image-->  
(c) 3X3agent

Fig. 7. Total reward under different topologies.  
<!-- image-->  
Fig. 6. Cost per step of each UE under 3 rd Topology.

The convergence of our algorithm is firstly evaluated and presented in this section. We select the third network topology, where the network consists of a cloud server, 3 LEOs, and 9 UEs. As shown in Fig. 6, we notice that the learning cost can quickly converge to stable at approximately 2 k iteration times and the cost function is defined in Eq. (15). And it is worth mentioning that each UE has one computation task to process in every iteration. For each task, the actor will choose the offloading location and determine the transmission power

<!-- image-->  
(b) 2X2agent

<!-- image-->  
(d) 4X4agent

<!-- image-->  
(a) 3X2agent

<!-- image-->  
(c)3x4agent  
Fig. 8. Offloading behavior under different topologies.

for the UE. In addition, we can conclude that the convergency value of different UE is not much different. The reason is that the centralized critic, which is augmented with the global network state, can effectively alleviate the distributed agent learning procedure. These experimental results illustrate that our proposed algorithm presents a good convergence and fairness.

## 5.4 Performance Analysis

(b)3X3agent

In order to fully demonstrate the effect of the proposed algorithm, we compare its performance with the baseline algorithms in different topologies by comparing the total cost, which is the sum of all the UEsâ costs in one thousand iteration times. We set four topologies where the number of LEOs and UEs differ from each other and we denote them with the figure note such as 2X3agent, which means the topology contains 2 LEOs and each LEO is connected with 3 UEs. As shown in Fig. 7, when the number of UEs is small, we notice the reinforcement learning-based algorithms (i.e., MADRL, DDPG) exhibit better performance compared to the two other algorithms. The reason is that reinforcement learning can automatically adapt to environmental dynamics and learn optimal strategy directly from experience. As the number of UEs increases, the MADRL algorithm presents performance benefits gradually reflected compared to the DDPG adopts a centralized âcriticâ that maintains the global state and joint action of all UEs to revise each UEâs training process. This revised signal can effectively enhance the distributed agent collaboration ability, and therefore increase the whole network utility. In contrast, the DDPG adopts a selfish scheme to update the offloading strategy only according to local reward rather than global reward. While this selfish scheme will bring high returns quickly, it leads to the nonconvergence of the learning procedure, especially with the number of agents increasing.

<!-- image-->

<!-- image-->  
(d) 3X5agent

## 5.5 Behavior Analysis

Then, we demonstrate the behavior of each UE during the training process and show how the proposed algorithm guide the offloading behavior in different load conditions. In this experiment, we set up a network scenario, which contains one cloud server and three LEOs. Then, we increase the number of UEs under each LEO to analyze each UEâs offloading behavior. As shown in Fig. 8, we notice that as the number of UEs increasing, the UEs are more willing to execute the tasks locally rather than in the cloud server. This is caused by that too many UEs will carry the computing pressure to cloud servers and LEO.

Besides, we notice that the willingness to offload tasks to LEO slightly increased at first and then decreased. That is because that when UEâs number is increasing, the computation pressure of the MEC server on the cloud server increases as well. Then, the cost of offloading tasks to the cloud servers grows above the cost of offloading to LEO. However, with the UEâs number continuously increasing, the MEC serverâs pressure on LEO also increases, and therefore significantly increases the offloading cost. Then, UEs are more likely to execute the tasks locally. Therefore, we can tell that the algorithm can help the UEs avoid congestion and choose the optimal offloading decision for it.

<!-- image-->  
Fig. 9. Average cost under different topologies.

## 5.6 Average Cost Vs. UE Numbers

Next, we evaluate the performance of our algorithm under different UE numbers. As shown in Fig. 9, the algorithm has achieved good performance in different scenarios. As the number of UEs increasing, the MEC serverâs load in the network increases and therefore increases the processing delay. Thus, the average cost increases slightly as the amount of UEs increasing.

## 6 CONCLUSION

In this paper, we investigate the characteristics of computation offloading under the LEO network architecture and model the UEâs offloading decision problem as a distributed decision problem, which, we think, is closer to the real situation of the network. We then proposed a joint three-tier computation offloading framework, including offloading location selection and transmission energy allocation issues. We chose to apply the multi-agent deep reinforcement learning (MADRL) algorithm in our proposed architecture. In the algorithm, an actor is deployed on each UE. It can make decisions independently based on local observations. And a logically centralized critic platform is deployed on the cloud servers. The platform collects the information of the network, MEC servers, and UEs and gives updating advice to agents, aiding them to maximize the cumulative expected reward. The experiment results illustrated that the algorithm can converge quickly and outperforms other algorithms.

## REFERENCES

[1] M. Centenaro, C. E. Costa, F. Granelli, C. Sacchi, and L. Vangelista, âA survey on technologies, standards and open challenges in satellite IoT,â IEEE Commun. Surveys Tuts., vol. 23, no. 3, pp. 1693â 1720, Jul.-Sep. 2021.

[2] Q. Li et al., âService coverage for satellite edge computing,â IEEE Internet Things J., vol. 9, no. 1, pp. 695â705, Jan. 2022.

[3] S. Yu, X. Gong, Q. Shi, X. Wang, and X. Chen, âEC-SAGINs: Edge computing-enhanced space-air-ground integrated networks for internet of vehicles,â IEEE Internet Things J., vol. 9, no. 8, pp. 5742â5754, Apr. 2022.

[4] Q. Tang, Z. Fei, B. Li, and Z. Han, âComputation offloading in LEO satellite networks with hybrid cloud and edge computing,â IEEE Internet Things J., vol. 8, no. 11, pp. 9164â9176, Jun. 2021.

[5] Y. Mao, J. Zhang, and K. B. Letaief, âDynamic computation offloading for mobile-edge computing with energy harvesting devices,â IEEE J. Sel. Areas Commun., vol. 34, no. 12, pp. 3590â3605, Dec. 2016.

[6] R. Xie, Q. Tang, Q. Wang, X. Liu, F. R. Yu, and T. Huang, âSatellite-terrestrial integrated edge computing networks: Architecture, challenges, and open issues,â IEEE Netw., vol. 34, no. 3, pp. 224â231, May/Jun. 2020.

[7] Y. Gong, H. Yao, J. Wang, M. Li, and S. Guo, âEdge intelligencedriven joint offloading and resource allocation for future 6G industrial Internet of Things,â IEEE Trans. Netw. Sci. Eng., to be published, doi: 10.1109/TNSE.2022.3141728.

[8] T. Mai, H. Yao, J. Xu, N. Zhang, Q. Liu, and S. Guo, âAutomatic double-auction mechanism for federated learning service market in Internet of Things,â IEEE Trans. Netw. Sci. Eng., to be published, doi: 10.1109/TNSE.2022.3170336.

[9] C. Xian, Y.-H. Lu, and Z. Li, âAdaptive computation offloading for energy conservation on battery-powered systems,â in Proc. Int. Conf. Parallel Distrib. Syst., 2007, pp. 1â8.

[10] J. Liu, K. Kumar, and Y.-H. Lu, âTradeoff between energy savings and privacy protection in computation offloading,â in Proc. ACM/ IEEE Int. Symp. Low-Power Electron. Des., 2010, pp. 213â218.

[11] S. Chen, X. Zhu, H. Zhang, C. Zhao, G. Yang, and K. Wang, âEfficient privacy preserving data collection and computation offloading for fog-assisted IoT,â IEEE Trans. Sustain. Comput., vol. 5, no. 4, pp. 526â540, Oct.âDec. 2020.

[12] X. Xu, C. He, Z. Xu, L. Qi, S. Wan, and M. Z. A. Bhuiyan, âJoint optimization of offloading utility and privacy for edge computing enabled IoT,â IEEE Internet Things J., vol. 7, no. 4, pp. 2622â2629, Apr. 2020.

[13] T. Mai, H. Yao, N. Zhang, L. Xu, M. Guizani, and S. Guo, âCloud mining pool aided blockchain-enabled Internet of Things: An evolutionary game approach,â IEEE Trans. Cloud Comput., to be published, doi: 10.1109/TCC.2021.3110965.

[14] J. Wang, J. Hu, G. Min, W. Zhan, Q. Ni, and N. Georgalas, âComputation offloading in multi-access edge computing using a deep sequential model based on reinforcement learning,â IEEE Commun. Mag., vol. 57, no. 5, pp. 64â69, May 2019.

[15] A. Alsharoa and M.-S. Alouini, âImprovement of the global connectivity using integrated satellite-airborne-terrestrial networks with resource optimization,â IEEE Trans. Wireless Commun., vol. 19, no. 8, pp. 5088â5100, Aug. 2020.

[16] N. Cheng et al., âSpace/aerial-assisted computing offloading for IoT applications: A learning-based approach,â IEEE J. Sel. Areas Commun., vol. 37, no. 5, pp. 1117â1129, May 2019.

[17] J. Liu, X. Du, J. Cui, M. Pan, and D. Wei, âTask-oriented intelligent networking architecture for the spaceâairâgroundâaqua integrated network,â IEEE Internet Things J., vol. 7, no. 6, pp. 5345â5358, Jun. 2020.

[18] J. Han, H. Wang, S. Wu, J. Wei, and L. Yan, âTask scheduling of high dynamic edge cluster in satellite edge computing,â in Proc. IEEE World Congr. Serv., 2020, pp. 287â293.

[19] Z. Zhang, W. Zhang, and F.-H. Tseng, âSatellite mobile edge computing: Improving QoS of high-speed satellite-terrestrial networks using edge computing techniques,â IEEE Netw., vol. 33, no. 1, pp. 70â76, Jan./Feb. 2019.

[20] Y. Wang, J. Yang, X. Guo, and Z. Qu, âA game-theoretic approach to computation offloading in satellite edge computing,â IEEE Access, vol. 8, pp. 12510â12520, 2019.

[21] F. Guo, H. Zhang, H. Ji, X. Li, and V. C. Leung, âAn efficient computation offloading management scheme in the densely deployed small cell networks with mobile edge computing,â IEEE/ACM Trans. Netw., vol. 26, no. 6, pp. 2651â2664, Jun. 2018.

[22] J. Guo, H. Zhang, L. Yang, H. Ji, and X. Li, âDecentralized computation offloading in mobile edge computing empowered smallcell networks,â in Proc. IEEE Globecom Workshops, 2017, pp. 1â6.

[23] L. Huang, S. Bi, and Y.-J. A. Zhang, âDeep reinforcement learning for online computation offloading in wireless powered mobile-edge computing networks,â IEEE Trans. Mobile Comput., vol. 19, no. 11, pp. 2581â2593, Nov. 2020.

[24] Z. Song, Y. Hao, Y. Liu, and X. Sun, âEnergy-efficient multiaccess edge computing for terrestrial-satellite Internet of Things,â IEEE Internet Things J., vol. 8, no. 18, pp. 14202â14218, Sep. 2021.

[25] W. Chen et al., âCooperative and distributed computation offloading for blockchain-empowered industrial Internet of Things,â IEEE Internet Things J., vol. 6, no. 5, pp. 8433â8446, May 2019.

[26] Z. Zhao et al., âA novel framework of three-hierarchical offloading optimization for MEC in industrial IoT networks,â IEEE Trans. Ind. Informat., vol. 16, no. 8, pp. 5424â5434, Aug. 2019.

[27] W. Zhan et al., âDeep-reinforcement-learning-based offloading scheduling for vehicular edge computing,â IEEE Internet Things J., vol. 7, no. 6, pp. 5449â5465, Jun. 2020.

[28] C. Liu, F. Tang, Y. Hu, K. Li, Z. Tang, and K. Li, âDistributed task migration optimization in MEC by extending multi-agent deep reinforcement learning approach,â IEEE Trans. Parallel Distrib. Syst., vol. 32, no. 7, pp. 1603â1614, Jul. 2020.

[29] H. Zhang, J. Guo, L. Yang, X. Li, and H. Ji, âComputation offloading considering fronthaul and backhaul in small-cell networks integrated with mec,â in Proc. IEEE Conf. Comput. Commun. Workshops, 2017, pp. 115â120.

[30] G. Liu, F. R. Yu, H. Ji, and V. C. Leung, âVirtual resource management in green cellular networks with shared full-duplex relaying and wireless virtualization: A game-based approach,â IEEE Trans. Veh. Technol., vol. 65, no. 9, pp. 7529â7542, Sep. 2015.

[31] J. Dai and S. Wang, âClustering-based spectrum sharing strategy for cognitive radio networks,â IEEE J. Sel. Areas Commun., vol. 35, no. 1, pp. 228â237, Jan. 2017.

[32] G. Shani, J. Pineau, and R. Kaplow, âA survey of point-based pomdp solvers,â Auton. Agents Multi-Agent Syst., vol. 27, no. 1, pp. 1â51, 2013.

[33] Y. Mao, C. You, J. Zhang, K. Huang, and K. B. Letaief, âA survey on mobile edge computing: The communication perspective,â IEEE Commun. Surveys Tuts., vol. 19, no. 4, pp. 2322â2358, Oct.âDec. 2017.

[34] T. P. Lillicrap et al., âContinuous control with deep reinforcement learning,â 2015, arXiv:1509.02971.

[35] M. Liu and Y. Liu, âPrice-based distributed offloading for mobileedge computing with computation capacity constraints,â IEEE Wireless Commun. Lett., vol. 7, no. 3, pp. 420â423, Jun. 2018.

[36] Y. Liu, F. R. Yu, X. Li, H. Ji, and V. C. Leung, âDistributed resource allocation and computation offloading in fog and cloud networks with non-orthogonal multiple access,â IEEE Trans. Veh. Technol., vol. 67, no. 12, pp. 12137â12151, Dec. 2018.

<!-- image-->  
Zeyu Qin (Student Member, IEEE) is currently working toward the masterâs degree in the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His research interests include future network architecture, programmable data plane, network artificial intelligence, multi-agent system, network resource allocation and dedicated networks.

<!-- image-->

Haipeng Yao (Senior Member, IEEE) is received the PhD in the Department of Telecommunication Engineering, University of Beijing University of Posts and Telecommunications, in 2011. He is a professor in Beijing University of Posts and Telecommunications. His research interests include future network architecture, network artificial intelligence, networking, space-terrestrial integrated network, network resource allocation and dedicated networks. He has published more than 150 papers in prestigious peer-reviewed journals and conferences. He has served as an editor of IEEE Network, IEEE Transactions on Sustainable Computing, IEEE Access, and a guest editor of IEEE Open Journal of the Computer Society and Springer Journal of Network and Systems Management. He has also served as a member of the technical program committee as well as the Symposium chair for a number of international conferences, including IWCMC 2019 Symposium Chair, ACM TUR-C SIGSAC2020 Publication Chair.

<!-- image-->

Tianle Mai (Member, IEEE) is currently working toward the PhD degree in the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His research interests include future network architecture, network artificial intelligence, multiagent system, space-terrestrial integrated network, network resource allocation and dedicated networks.

<!-- image-->

Di Wu (Student Member, IEEE) (Student Member, IEEE) receieved the masterâs degree in computer system engineering from the University of Houston, in 2020. He is currently working toward the PhD degree in Beijing University of Posts and Telecommunications. His research interests include future network architecture, network artificial intelligence, space-terrestrial integrated network, and Big Data.

<!-- image-->

Ni Zhang received the PhD with the Institute of Computing Technology, Chinese Academy of Sciences, in 2007. He currently serves with the Sixth Research Institute of China Electronic Corporation, Beijing, China. His research interests are in the area of future Internet architecture, network security and artificial intelligence.

<!-- image-->

Song Guo (Fellow, IEEE) is a full professor and associate head with the Department of Computing, The Hong Kong Polytechnic University. His research interests are mainly in the areas of Big Data, cloud computing, mobile computing, and distributed systems. He is the recipient of the 2019 IEEE TCBD Best Conference paper award, 2018 IEEE TCGCC Best Magazine paper award, 2017 IEEE Systems Journal Annual best paper award, and other 6 best paper awards from IEEE/ACM conferences. His work was also recognized by the

2016 annual best of computing: Notable Books and Articles in Computing in ACM Computing Reviews. He was an IEEE ComSoc Distinguished Lecturer (2017-2018) and served in IEEE ComSoc Board of Governors (2018-2019). He has also served as General and Program chair for numerous IEEE conferences. He is an IEEE editor-in-chief of IEEE Open Journal of the Computer Society, and associate editor of IEEE Transactions on Cloud Computing, IEEE Transactions on Sustainable Computing, and IEEE Transactions on Green Communications and Networking.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/csdl.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_6_img_1.jpeg|page_6_img_1]]
3. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_8_img_1.jpeg|page_8_img_1]]
4. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_8_img_2.jpeg|page_8_img_2]]
5. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_8_img_3.jpeg|page_8_img_3]]
6. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_9_img_1.jpeg|page_9_img_1]]
7. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_10_img_1.jpeg|page_10_img_1]]
8. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_11_img_1.jpeg|page_11_img_1]]
9. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_11_img_2.jpeg|page_11_img_2]]
10. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_11_img_3.jpeg|page_11_img_3]]
11. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_11_img_4.jpeg|page_11_img_4]]
12. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_11_img_5.jpeg|page_11_img_5]]
13. [[../extracted_images/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things/page_11_img_6.jpeg|page_11_img_6]]

---

