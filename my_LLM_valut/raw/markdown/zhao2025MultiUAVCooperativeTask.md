# A Multi-UAV Cooperative Task Scheduling in Dynamic Environments: Throughput Maximization

Liang Zhao , Member, IEEE, Shuo Li , Zhiyuan Tan , Ammar Hawbani ,

Stelios Timotheou , Senior Member, IEEE, and Keping Yu

AbstractâUnmanned aerial vehicle (UAV) has been considered a promising technology for advancing terrestrial mobile computing in the dynamic environment. In this research field, throughput, the number of completed tasks and latency are critical evaluation indicators used to measure the efficiency of UAVs in existing studies. In this paper, we transform these metrics to a single optimization objective, i.e., throughput maximization. To maximize the throughput, we consider realizing this goal in two respects. The first is to adapt the formation of the UAVs to provide cooperative computing service in a dynamic environment, we integrate a policy-based gradient algorithm and the task factorization network as a new reinforcement learning algorithm to improve the cooperation of UAVs. The second is to optimize the association process between UAVs and users, where the heterogeneity of tasks is considered. This algorithm is modified from the Gale-Shapley stability concept to optimize the appropriate association between tasks and UAVs in a dynamic time-varying condition to get the near-optimal association with few iterations. The scheduling of dependent tasks and independent tasks jointly also has to be considered. Finally, simulation results demonstrate the improvement of cooperation performance and the practicability of the association process.

Received 13 May 2024; revised 14 September 2024; accepted 8 October 2024. Date of publication 21 October 2024; date of current version 20 January 2025. This work was supported in part by the National Natural Science Foundation of China under Grant 62372310, in part by Liaoning Province Applied Basic Research Program under Grant 2023JH2/101300194, and in part by LiaoNing Revitalization Talents Program under Grant XLYC2203151. The work of Ammar Hawbani was supported in part by the Open Fund of Anhui Engineering Research Center for Intelligent Applications and Security of Industrial Internet, under Grant IASII24-04, and in part by Shenyang Aerospace University Talent Research Start-up Fund under Grant 502/120423005. Recommended for acceptance by T. Jones. (Corresponding authors: Ammar Hawbani; Stelios Timotheou.)

Keping Yu is with the Computer Science Department, Community College, King Saud University, Riyadh 11437, Saudi Arabia, and also with the Graduate School of Science and Engineering, Hosei University, Tokyo 184- 8584, Japan (e-mail: KepingYu@ksu.edu.sa; keping.yu@ieee.org).

This article has supplementary downloadable material available at https:// doi.org/10.1109/TC.2024.3483636, provided by the authors.

Digital Object Identifier 10.1109/TC.2024.3483636

Index TermsâThroughput maximization, multi-UAV cooperation, task scheduling, reinforcement learning.

## I. INTRODUCTION

T HE hlyellowuse of Unmanned aerial vehicles (UAV) toprovide computation service arises significant concerns provide computation service arises significant concerns [1]. Compared with traditional terrestrial edge computing (EC), UAVs-assisted computation can break the constraint of topographic limitation to fly to the uncovered area by the edge servers to provide service, and the lack of the computation capacity of edge servers can be compensated by UAVs [2], [3]. Existing studies of UAVs-assisted computation are mainly divided into two categories. One prefers to study the trajectory or deployment optimization to adjust the location of UAVs to provide better service, and another prefers to optimize the association policy, such as the scheduling policy or the combination policy to maximize the computation efficiency of UAVs while satisfying the demand of tasks.

In the first category, by optimizing the flight trajectories or the deployment policy, UAVs can fly on more energy-efficient trajectories or deploy in more suitable locations while providing computation service. Existing studies focus on optimizing the cooperative trajectory or cooperative deployment policy [4], [5], [6], [7], [8]. However, there are still some challenges to solve. For example, one UAV cannot observe the whole environment due to the limited coverage area, and the environments of existing studies are assumed to be static. These solutions cannot be applied to practice directly. For the training process of the cooperation model, existing studies only combine the observation from each UAV, this makes the algorithm unable to converge stable with the increasing number of UAVs.

The second category ignores the cooperative flight of UAVs but focuses on the association process optimization, as well as optimizing the resource allocation policy, task scheduling policy and other metrics to improve the completed ratio or the completed latency of tasks [9], [10], [11], [12], [13], [14]. Reasonable combination policy and task scheduling policy between tasks and UAVs all can reduce the process latency of tasks and the energy consumption of UAV. However, existing studies only consider a static environment, the details of tasks are ignored, and the set of tasks are unchanged. In practice, tasks generated by mobile devices (MDs) generally have a strong randomness. Although we believe that the arrival of a task follows the Poisson distribution, the sudden creation, withdrawal, and details

Stelios Timotheou is with the KIOS Research and Innovation Center of Excellence and the Department of Electrical and Computer Engineering, University of Cyprus, Nicosia 1678, Cyprus (e-mail: stimo@ucy.ac.cy).

of many tasks cannot be predicted in a complex environment. Thus, we need to design a converge-quickly and convergestable algorithm, and it is insensitive to the change of tasks.

To sum up, many previous studies contribute to the optimization of throughput, latency and other metrics. However, some problems still have not been solved. For example, the dynamic of the environment has not been considered, the global information of MDs and tasks is assumed to be known, the heterogeneity of tasks has been ignored, the association process is too complex. These shortages all make the solutions cannot be applied in practice. To solve these problems, we propose a UAVs-assisted terrestrial computing framework to cope with differentiated tasks in a dynamic environment. To improve the cooperation of UAVs, we especially optimize the global optimal action selection process to guarantee cooperative performance. In addition, we propose an association algorithm between UAVs and MDs, called Many-to-One Gale-Shapley (MOGS), which is improved by the Gale-Shapley algorithm. This algorithm can realize direct association optimization without the help of a third party such as the edge server. Thus, the communication latency can be reduced significantly. Finally, the throughput can be improved further. Our contributions are summarized as follows.

â¢ Throughput Maximization Problem Formulation: A UAVs-aided offloading system in a continuous dynamic environment has been formulated, with the constraint of tolerant latency of tasks generated by terrestrial MDs and the limitation observation of UAVs. The locations of MDs change all the time in this environment and the stochastic generation of tasks has no rules to follow, while the volume, generation time slot, tolerant latency are also. The UAVs can serve terrestrial MDs with limited coverage and computation capacity. The objective is to maximize the throughput, maximize the completed number of tasks and minimize the completed latency of tasks, which is shown to be a non-convex problem. To solve this problem, UAVs must find a cooperative deployment location to maximize the transmission efficiency for air-to-terrestrial and inner communication and cover maximized MDs. These metrics are used to measure the cooperation performance of UAVs.

â¢ DRL-based Multi-UAV Cooperation Policy: To solve the optimization problem mentioned above, the relationship between latency, the number of completed tasks, and another metric throughput has been analyzed. Then, the optimization has been transformed into maximizing the throughput. This optimization problem has been solved by two solutions, one is to optimize the trajectory and cooperation of UAVs, another solution is to optimize the association between UAVs and MDs to process more tasks as soon as possible. To optimize the deployment and cooperation of UAVs, a deep reinforcement learning algorithm, i.e., proximal policy optimization (PPO) has been adopted. To improve convergence speed and optimal action selection policy between UAVs, a novel action-value function factorization approach has been combined with PPO.

â¢ GS-based Tasks Scheduling Algorithm: An improved association algorithm, Many-to-One Gale-Shapley (MOGS), has been proposed to realize fast task scheduling in a complex environment in continuous time. It is inspired by the Gale-Shapley (GS) algorithm to realize the association between UAVs and tasks directly without the assistance of a third party, i.e., some edge servers or central servers. It consumes very little computation power, and the constraint of the number of two sides in GS is broken. Some rules of association are proposed to optimize the computation load of each UAV to guarantee the performance of cooperation. Some simulation comparisons demonstrate the advantage of MOGS.

The organization of this paper later is as follows. Section II introduces some related studies in recent years. The system model and problem formulation are described in Section III and Section IV, respectively. In Section V, the solution of the problem is introduced. In Section VI, we introduce the simulation environment and present the results. Finally, the whole work in this paper is concluded.

## II. RELATED WORK

In this section, we will review existing studies, which include UAV-centric studies and task-centric studies. Also, we briefly summarize the shortages of them to demonstrate the motivation of this work.

UAV-centric studies mainly research how to optimize the trajectory, cooperation policy and other metrics to improve the efficiency of UAV [4], [5], [6], [7], [8]. In these studies, the experience of users usually has not been considered in detail. The authors Zhang et al. use the DRL algorithm to plan the cooperative trajectory of UAVs-BSs to guarantee the throughput maximization of users in an emergency environment [4]. Guan et al. [5] use the PPO algorithm and K-means algorithm to plan the trajectory of UAV while minimizing the interaction consumption and improving the deployment efficiency. Furthermore, Table I summarizes the comparison between our study and previous studies [15], [16], [17], [18], [19], [20], [21], [22], [23], [24]. For task-centric research, focus on improving the association process between UAVs and tasks, such as optimizing the task collecting policy, task scheduling policy, etc [2], [9], [10], [11], [12], [13], [14]. These studies can improve the QoE of users in the considered environment. Some studies consider using UAVs to provide offloading service for devices [10], [11], where the Wang et al. use Generative Adversarial Networks (GANs) and the gradient-based policy to train a policy for online scheduling with partial observation [10]. Some studies focus on optimizing the energy-efficiency ratio and some other metrics to optimize these two shortages. Wang et al. and Hua et al. in [13] and [14] all maximize the throughput by optimizing the trajectory of UAVs and offloading decisions.

The studies mentioned above all contribute to optimizing UAV-assisted MEC. However, they only consider optimizing some metrics for a static time slot but ignore the continuity of time in practice. In a complex environment, a huge number of tasks will be generated and canceled in a continuous time irregularly, and the location of some users will also change. How to train a cooperation model to adapt to the dynamic environment while guaranteeing offloading efficiency needs to be solved. There still are some problems to be solved in the taskcentric research. For example, during a training process, the task set generated at the beginning of a one-time slot may change and the final result cannot guarantee optimality. The training process of the result also consumes a period, the latency-sensitive task may not be served due to the low-latency constraint. Thus, a lightweight and fast convergence task scheduling algorithm needs to be designed.

TABLE I  
A COMPARISON WITH EXISTING STUDIES
<table><tr><td rowspan=2 colspan=1>Reference</td><td rowspan=2 colspan=1>Scheme</td><td rowspan=1 colspan=2>Environment</td><td rowspan=1 colspan=2>Observation</td><td rowspan=1 colspan=4>Objectives</td></tr><tr><td rowspan=1 colspan=1>Static</td><td rowspan=1 colspan=1>Dynamic</td><td rowspan=1 colspan=1>Local</td><td rowspan=1 colspan=1>Complete</td><td rowspan=1 colspan=1>Latency</td><td rowspan=1 colspan=1>Throughput</td><td rowspan=1 colspan=1>Task Number</td><td rowspan=1 colspan=1>Joint</td></tr><tr><td rowspan=1 colspan=1>[15]</td><td rowspan=1 colspan=1>A*</td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[16]</td><td rowspan=1 colspan=1>CO</td><td rowspan=1 colspan=1> $\overline { { \checkmark } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[17]</td><td rowspan=1 colspan=1>DRL</td><td rowspan=1 colspan=1> $\overline { { \checkmark } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[18]</td><td rowspan=1 colspan=1>DRL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[19]</td><td rowspan=1 colspan=1>DRL</td><td rowspan=1 colspan=1> $\overline { { \checkmark } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1>DRL</td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[21]</td><td rowspan=1 colspan=1>DRL</td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>DRL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1>CO</td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>BCD</td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\bigtriangledown$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\bigtriangledown$ </td></tr><tr><td rowspan=1 colspan=1>Our work</td><td rowspan=1 colspan=1>DRL,MOGS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\checkmark$ </td></tr></table>

Fig. 1. An illustration of a UAV-assisted computation environment, the upper part represents the real world. The lower left and lower right parts represent the training of the UAV cooperation model and the task scheduling model for this environment, respectively.

<!-- image-->

## III. SYSTEM MODEL

In this work, we consider using multiple UAVs to serve moving MDs, which is shown in Fig. 1, and the number of MDs is much higher than the number of UAVs. MDs are moving all the time and tasks are generated by them. UAVs need to move cooperatively to cover MDs and compute tasks. The system model includes three parts, i.e., the environment model, transmission model and energy consumption model. Then we introduce these models in detail.

## A. Environment Model

This model is used to describe some fundamental characters including the state of UAV and the details of tasks. We use $\mathcal { U } = \{ u _ { 1 } , . . . , u _ { k } , . . . , U \}$ to denote the set of UAVs. The UAVs in U can communicate with each other to transmit tasks, results, and the topology information of the whole swarm. We consider a time horizon $\tau$ in time interval $[ \mathcal { T } _ { s } , \mathcal { T } _ { e } ]$ and discretize it into T equal-size time slots by the length of $t _ { i \cdot }$ which are indexed by the set $\mathcal { T } = \{ t _ { 1 } , t _ { 2 } , . . . , T \}$ . There are $\mathcal { M } _ { t _ { i } } = \left\{ \tau _ { d _ { 1 } , t _ { i } } , . . . , \tau _ { d _ { j } , t _ { i } } , . . . , \tau _ { d _ { D } , t _ { i } } \right\}$ tasks generated by MDs $\mathcal { D } = \{ d _ { 1 } , d _ { 2 } , . . . , D \}$ in the $t _ { i }$ time slot.

The main properties of the UAV $u _ { k }$ are denoted as $u _ { k } \overset { \triangle } { = }$ $< < \chi _ { u _ { k } , t _ { i } } ^ { l o } , \chi _ { u _ { k } } ^ { m a x } > , < \varphi _ { u _ { k } , x , t _ { i } } ^ { c o o r } , \varphi _ { u _ { k } , y , t _ { i } } ^ { c o o r } , \varphi _ { u _ { k } , z , t _ { i } } ^ { c o o r } > > ,$ where $\varphi _ { u _ { k } , t _ { i } } ^ { c o o r }$ denote the 3D coordination in the $t _ { i }$ time slot of the UAV $u _ { k } , \ \chi _ { u _ { k } , t _ { i } } ^ { l o }$ and $\chi _ { u _ { k } } ^ { m a x }$ denote the real-time computation load condition in the time slot $t _ { i }$ and the maximum computation capacity of the UAV $u _ { k }$ , respectively. We use $d _ { j } \triangleq < < \psi _ { d _ { i } , x , t _ { i } } ^ { c o o r } , \psi _ { d _ { i } , y , t _ { i } } ^ { c o o r } > , \tau _ { j , t _ { i } } > \mathrm { ~ t ~ }$ o describe the properties of one MD, where $\tau _ { j , t _ { i } }$ is a task generated by this MD, $\psi _ { d _ { j } , x , t _ { i } } ^ { c o o r }$ and $\psi _ { d _ { j } , y , t _ { i } } ^ { c o o r }$ are the 2D coordination of this MD in the $t _ { i }$ time slot. The main properties of the task $\tau _ { j , t _ { i } }$ are denoted as $\tau _ { d _ { j } , t _ { i } } \triangleq < v _ { \tau _ { d _ { j } , t _ { i } } } , \gamma _ { \tau _ { d _ { j } , t _ { i } } } , \omega _ { \tau _ { d _ { j } , t _ { i } } } , \sigma _ { \tau _ { d _ { j } , t _ { i } } } , <$ $\psi _ { d _ { j } , x , t _ { i } } ^ { c o o r } , \psi _ { d _ { j } , y , t _ { i } } ^ { c o o r } > >$ , where $v _ { \tau _ { d _ { j } , t _ { i } } }$ denotes the volume of task $\tau _ { d _ { j } , t _ { i } } , \gamma _ { \tau _ { d _ { j } , t _ { i } } } , \omega _ { \tau _ { d _ { j } , t _ { i } } }$ and $\sigma _ { \tau _ { d _ { i } , t _ { i } } }$ denote the size of result data, the number of CPU cycles to process and the tolerant latency of task $\tau _ { d _ { j } , t _ { i } } ,$ respectively. We suppose that the coordination of MD and UAVs is static during a one-time slot, the distance between $d _ { j }$ and UAV $u _ { k }$ can be represented by (1). The expression of the notations in this paper are listed in Table II.

$$
\begin{array} { r } { \delta _ { d _ { j } , u _ { k } , t _ { i } } ^ { d i s } = [ ( \varphi _ { u _ { k } , x , t _ { i } } ^ { c o o r } - \psi _ { d _ { j } , x , t _ { i } } ^ { c o o r } ) ^ { 2 } + ( \varphi _ { u _ { k } , y , t _ { i } } ^ { c o o r } - \psi _ { d _ { j } , y , t _ { i } } ^ { c o o r } ) ^ { 2 } } \\ { + ( \varphi _ { u _ { k } , z , t _ { i } } ^ { c o o r } ) ^ { 2 } ] ^ { \frac { 1 } { 2 } } \qquad ( } \end{array}\tag{1}
$$

## B. Transmission Model

The transmission model is used to describe some details of the communication process, such as the calculation of transmission rate, etc. We use $P _ { u _ { k } } ^ { t r a n s }$ to denote the transmitting power of the UAV $u _ { k }$ . Thus, the radius of the coverage area $R _ { u _ { k } } ^ { r a d }$ of each UAV $u _ { k }$ is limited, which means the MD cannot connect to the UAV if the distance between MD and UAV surpasses $R _ { u _ { k } } ^ { r a d }$ . The uplink model is similar to the ground-to-air link, we need to consider the LoS and NLoS transmissions. Then we use a two-piece function $\zeta ( \delta )$ to model the path loss [25], it is shown in (2), where the $A ^ { L }$ and $A ^ { N L }$ are the path losses with the reference distance $\delta = 1 , \alpha ^ { L }$ and $\alpha ^ { N L }$ are the path loss exponents with respect to LoS and NLoS.

TABLE II  
MAIN NOTATIONS USED IN SYSTEM MODEL
<table><tr><td>Notations</td><td>Expression</td></tr><tr><td> $\mathcal { U }$ </td><td>The set of UAVs</td></tr><tr><td> $s$ </td><td>The set of ESs</td></tr><tr><td> $\mathcal { M } _ { t _ { i } }$ </td><td>The set of tasks generated in  $t _ { i }$  time slot</td></tr><tr><td> $\mathcal { D }$ </td><td>The set of MDs</td></tr><tr><td> $\chi _ { u _ { k } } ^ { m a x }$ </td><td>The computation capacity of the UAV  $u _ { k }$ </td></tr><tr><td> $\varphi _ { u _ { k } , t _ { i } } ^ { c o o r }$ </td><td>The 3D coordination in the  $t _ { i }$  time slot of UAV â  $u _ { k }$ </td></tr><tr><td> $\chi _ { u _ { k } , t _ { i } } ^ { l o }$ </td><td>The real-time computation load condition in time slot  $t _ { i }$  of the UAV  $u _ { k }$ </td></tr><tr><td> $< \psi _ { d _ { j } , x , t _ { i } } ^ { c o o r } , \psi _ { d _ { j } , y , t _ { i } } ^ { c o o r } >$ </td><td>The 2D coordinate of the MD  $d _ { j }$  ï¼20 in the time slot  $t _ { i }$ </td></tr><tr><td> $\tau _ { d _ { j } , t _ { i } }$ </td><td>The task generated by MD  $d _ { j }$  in the time slot  $t _ { i }$ </td></tr><tr><td> $v _ { \tau _ { d _ { j } , t _ { i } } } , \gamma _ { \tau _ { d _ { j } , t _ { i } } }$ </td><td>The volume, size of result data of task</td></tr><tr><td> $\omega _ { \tau _ { d _ { j } , t _ { i } } } , \sigma _ { \tau _ { d _ { j } , t _ { i } } }$ </td><td> $\tau _ { d _ { j } , t _ { i } }$  The number of CPU cycles to process and the tolerant latency</td></tr><tr><td> $R _ { u _ { k } } ^ { r a d }$ </td><td>The coverage area radius UAV uk</td></tr><tr><td> $r _ { d _ { j } , u _ { k } } ^ { u p } , r _ { u _ { k } , d _ { j } } ^ { d o w n } , \xi , B$ </td><td>The achievable upload and download rate of MD  $d _ { j }$  to UAV  $u _ { k }$  the Signal-to-Noise Ratio and</td></tr><tr><td> $\Omega ^ { u _ { k } }$ </td><td>the bandwidth of the current channel The throughput of the UAV  $u _ { k }$ </td></tr><tr><td> $\Gamma _ { u _ { k } , d _ { j } } , E _ { u _ { k } } ^ { t r a n s }$ </td><td>The latency and energy consumption to transmit task by the UAV  $u k$ </td></tr><tr><td> $\mathcal { E } _ { \tau _ { d _ { j } } , t _ { i } } , E _ { u _ { k } } ^ { c o m p }$ </td><td> $\tau _ { d _ { j } , t _ { i } }$  The latency and energy consumption</td></tr><tr><td> $C _ { \tau _ { d _ { j } , t _ { i } } }$ </td><td>to process task  $\tau _ { d _ { j } , t _ { i } }$  by the UAV  $u _ { k }$  The finish time of the task  $\tau _ { d _ { j } , t _ { i } }$ </td></tr><tr><td> $\mathcal { F } _ { u _ { k } } , E _ { u _ { k } } ^ { m o v e }$ </td><td>The latency of the UAV  $u _ { k }$  to fly a distance  $\mathcal { l } _ { \alpha ^ { a n g } } ^ { d i s }$  and the energy</td></tr><tr><td> $v _ { u _ { k } }$ </td><td>consumption of this process The velocity of UAV  $u _ { k }$ </td></tr><tr><td> $P _ { u _ { k } } ^ { t r a n s } , P _ { u _ { k } } ^ { c o m p } , P _ { u _ { k } } ^ { m o v e }$ </td><td>The transmission, computation and flying power of the UAV  $u _ { k }$ </td></tr></table>

$$
\zeta ( \delta ) = \left\{ \begin{array} { c } { { \zeta ^ { L } ( \delta ) = A ^ { L } \delta ^ { - \alpha ^ { L } } , f o r L o S } } \\ { { \zeta ^ { N L } ( \delta ) = A ^ { N L } \delta ^ { - \alpha ^ { N L } } , f o r N L o S } } \end{array} \right.\tag{2}
$$

We use $P L o S ( \theta ( u _ { k } , d _ { j } ) )$ to represent the LoS probability from a transmitter to a receiver, i.e., the $u _ { k }$ to $d _ { j }$ or $d _ { j }$ to $u _ { k }$ This probability can be expressed as in (3), where Î» and $\sigma$ are coefficients determined by the specific environment, and Î¸ is a function to describe the elevation angle between UAV $u _ { k }$ and MD $d _ { j }$ . The NLoS probability can be calculated by $P N L o S ( \theta ( u _ { k } , d _ { j } ) ) = 1 - P L o S ( u _ { k } , d _ { j } )$

$$
P L o S ( \theta ( u _ { k } , d _ { j } ) ) = \frac { 1 } { 1 + \sigma e ^ { - \lambda [ \theta ( l , k ) - \sigma ] } }\tag{3}
$$

In this environment, the MD only communicates with at most one UAV to transmit its task to avoid repeated calculation. Some constraints have been defined as in (4) and (5).

$$
\sum _ { k = 1 } ^ { U } a _ { d _ { j } , u _ { k } } \leqslant 1 , \forall j \in D , k \in U\tag{4}
$$

$$
a _ { d _ { j } , u _ { k } } \in \left\{ 0 , 1 \right\} , \ \forall j \in D , k \in U\tag{5}
$$

Then the achievable upload rate of MD $d _ { j }$ to UAV $u _ { k }$ is shown in (6) [9], where $\xi$ is the Signal-to-Noise Ratio (SNR), the difference between the receiving and sending process has been ignored. B is the bandwidth of the current channel.

$$
r _ { d _ { j } , u _ { k } } ^ { u p } = B \log _ { 2 } \left( 1 + \frac { \xi p _ { u _ { k } } ^ { t r a n s } } { ( \delta _ { d _ { j } , u _ { k } } ^ { d i s } ) ^ { 2 } } \right)\tag{6}
$$

The downlink rate between UAV $u _ { k }$ to MD $d _ { j }$ is also given in $( 7 )$ , where $h ( u _ { k } , d _ { j } )$ is the power gain between the UAV $u _ { k }$ and MD $d _ { j } , N$ is the power spectral density.

$$
r _ { u _ { k } , d _ { j } } ^ { d o w n } = B \log _ { 2 } \left( 1 + \frac { p _ { u _ { k } } ^ { t r a n s } h ( u _ { k } , d _ { j } ) } { B N } \right)\tag{7}
$$

Then we can calculate the throughput of the UAV $u _ { k }$ in a fixed length of time, as in (8), where the former term denotes an idea condition that all the tasks can be transmitted successfully and the UAV can receive tasks all the time. The latter term denotes the realistic condition, including discontinuous and uncompleted transmission during the fixed time.

$$
\begin{array} { r } { \Omega ^ { u _ { k } } = m i n \left\{ \underset { i = 0 } { \overset { T } { \sum } } \displaystyle \sum _ { j = 0 } ^ { D } a _ { d _ { j } , u _ { k } } ~ v _ { \tau _ { d _ { j } , t _ { i } } } + \sum _ { i = 0 } ^ { T } \sum _ { j = 0 } ^ { D } a _ { d _ { j } , u _ { k } } \gamma _ { \tau _ { d _ { j } , t _ { i } } } ; \right. } \\ { \left. \displaystyle \sum _ { i = 1 } ^ { T } \sum _ { j = 0 } ^ { D } a _ { d _ { j } , u _ { k } } r _ { d _ { j } , u _ { k } } ^ { u p } + \sum _ { i = 1 } ^ { T } \sum _ { j = 0 } ^ { D } a _ { d _ { j } , u _ { k } } r _ { u _ { k } , d _ { j } } ^ { d o w n } \right\} } \end{array}\tag{8}
$$

Based on the transmission rate, the transmission latency $\Gamma _ { u _ { k } , d _ { j } }$ between UAV $u _ { k }$ and MD $d _ { j }$ by (9).

$$
\Gamma _ { u _ { k } , d _ { j } } = \frac { \mathcal { V } _ { \tau _ { d _ { j } , t _ { i } } } } { r _ { d _ { j } , u _ { k } } ^ { u p } } + \frac { \gamma _ { \tau _ { d _ { j } , t _ { i } } } } { r _ { u _ { k } , d _ { j } } ^ { d o w n } }\tag{9}
$$

For simplicity, we set the size of $\gamma _ { \tau _ { d _ { j } , t _ { i } } }$ to be a proportional reduction of $v _ { \tau _ { d _ { j } , t _ { i } } }$

## C. Energy Consumption Model

The energy consumption model mainly includes three parts, transmission consumption, computation consumption, and movement consumption. The transmission energy consumption of UAV $u _ { k }$ and MD $d _ { j }$ can be denoted as in (10).

$$
E _ { u _ { k } , \tau _ { d _ { j } , t _ { i } } } ^ { t r a n s } = \Gamma _ { u _ { k } . d _ { j } } * P _ { u _ { k } } ^ { t r a n s }\tag{10}
$$

Besides, the computation latency and computation energy consumption of task $\tau _ { d _ { j } , t _ { i } }$ are also considered, they can be denoted as in (11) and (12), where $P _ { u _ { k } } ^ { c o m p }$ denotes the computation power of UAV $u _ { k }$

$$
\mathcal { E } _ { \tau _ { d _ { j } , t _ { i } } } = \frac { \chi _ { u _ { k } } ^ { m a x } } { \omega _ { \tau _ { d _ { j } , t _ { i } } } }\tag{11}
$$

and

$$
E _ { u _ { k } } ^ { c o m p } = \mathcal { E } _ { \tau _ { d _ { j } , t _ { i } } } * P _ { u _ { k } } ^ { c o m p }\tag{12}
$$

We set the flying height of the UAV to under 400 feet, this obeys the rule of the Federal Aviation Administration of the US [26]. In the movement model, each UAV in this environment can choose a direction $\alpha ^ { a n g } \in [ 0 , 2 \pi ]$ in a 2D plane and fly for a distance $l _ { \alpha ^ { a n g } } ^ { d i s }$ . Thus, the flying latency can be calculated by (13), where $v _ { u _ { k } }$ denotes the velocity of UAV $u _ { k }$ . Then, the movement energy consumption of UAV $u _ { k }$ can be denoted as in (14).

$$
\mathcal { F } _ { u _ { k } } = \frac { l _ { \alpha ^ { a n g } } ^ { d i s } } { v _ { u _ { k } } }\tag{13}
$$

$$
E _ { u _ { k } } ^ { m o v e } = \mathcal { F } _ { u _ { k } } * P _ { u _ { k } } ^ { m o v e }\tag{14}
$$

## IV. PROBLEM FORMULATION

Based on the models mentioned above, our aim is to maximize throughput, as well as the number of completed tasks, and minimize the latency consumption of tasks in a fixed time T with the constraint of latency tolerance of tasks and the limited computation capacity of UAVs. We formulate this problem as a non-convex mixed integer programming problem which can be denoted as in (15).

$$
\begin{array} { r } { ( P ) : \ m a x \left\{ \displaystyle \sum _ { k = 1 } ^ { U } \Omega ^ { u _ { k } } , \displaystyle \sum _ { k = 1 } ^ { U } \sum _ { i = 1 } ^ { T } ( \hat { \mathcal { C } } _ { t _ { i } } ^ { i n } + \hat { \mathcal { C } } _ { t _ { i } } ^ { d e } ) , \right. } \\ { \left. \displaystyle \sum _ { k = 1 } ^ { U } \sum _ { j = 1 } ^ { D } \frac { 1 } { \Gamma _ { u _ { k } , d _ { j } } } \right\} } \end{array}\tag{15}
$$

These three metrics are coupled with each other, and the throughput dominates the other two metrics. For example, suppose that the optimization objective is to maximize the number of completed tasks in a fixed time. In that case, throughput can be maximized with the increase of the completed number if the fairness of tasks with different volumes can be guaranteed. To simplify the problem $P ,$ , we transform it into a subproblem P 1, which only needs to optimize the throughput in a fixed time while guaranteeing the fairness of different tasks. The problem

P 1 is shown as in (16).

$$
( P 1 ) : \mathop { m a x } _ { \hat { \mathcal { C } } _ { t _ { i } } ^ { i n } , \hat { \mathcal { C } } _ { t _ { i } } ^ { d e } , \frac { 1 } { \Gamma _ { u _ { k } } , d _ { j } } } \sum _ { k = 1 } ^ { U } \sum _ { j = 1 } ^ { D } \Omega ^ { u _ { k } }\tag{16}
$$

$$
\begin{array} { r } { \mathrm { s . t . } \quad 0 \leq \varphi _ { u _ { k } , x , t _ { i } } ^ { c o o r } \leq x _ { m a x } , \forall k \in U , i \in T } \end{array}\tag{16a}
$$

$$
0 \leq \varphi _ { u _ { k } , y , t _ { i } } ^ { c o o r } \leq y _ { m a x } , \forall k \in U , i \in T\tag{16b}
$$

$$
\boldsymbol { \chi } _ { u _ { k } , t _ { i } } ^ { l o } \le \boldsymbol { \chi } _ { u _ { k } } ^ { m a x } , \forall i \in T\tag{16c}
$$

$$
\sum _ { k = 1 } ^ { U } \chi _ { u _ { k } , t _ { i } } ^ { l o } \le \sum _ { k = 1 } ^ { U } \chi _ { u _ { k } } ^ { m a x } , \forall i \in T , k \in U\tag{16d}
$$

$$
C _ { \tau _ { d _ { j } , t _ { i } } } \leq \sigma _ { \tau _ { d _ { j } , t _ { i } } , \forall j } , \forall j \in U , i \in T\tag{16e}
$$

$$
\sum _ { k = 1 } ^ { U } a _ { d _ { j } , u _ { k } } \leqslant 1 , \forall k \in U\tag{16f}
$$

$$
r _ { d _ { j } , u _ { k } } ^ { u p } \ge 0 , \forall j \in D , k \in U\tag{16g}
$$

$$
r _ { u _ { k } , u _ { k + 1 } } ^ { u p } \ge 0 , \forall k \in U\tag{16h}
$$

In the optimization problem P 1, Constraint (16a) and Constraint (16b) constrain the flight area of UAVs. Constraint (16c) and Constraint (16d) guarantee each UAV has a normal computation load, the high-loaded state may cause transmission failure, computation failure and even cooperation failure. Constraint (16e) is used to guarantee the task can be finished in time, where $C _ { \tau _ { d _ { i } , t _ { i } } }$ can be calculated by (17). Constraint (16f) constrains each MD only can communicate with one UAV. Constraint (16g) is used to help the UAV judge whether to communicate with one MD. Constraint (16h) guarantees the UAV can communicate with other UAVs, no matter whether it communicates directly or relay by the second UAV.

$$
C _ { \tau _ { d _ { j } , t _ { i } } } = m i n \left\{ t _ { i } + \Gamma _ { u _ { k } , d _ { j } } + \mathcal { E } _ { \tau _ { d _ { j } , t _ { i } } } , t _ { i } + \sigma _ { \tau _ { d _ { j } , t _ { i } } } \right\}\tag{17}
$$

## V. PROPOSED SOLUTION

In this section, we give our solutions to the cooperation of UAVs and task scheduling problems, respectively. In the first problem, UAVs need to coordinate their formation according to the moving MDs which move with no regularity, and the observation of each UAV is limited, the cooperation metrics include transmission performance between UAVs and UAVs-to-MDs, etc. The second problem focuses mainly on optimizing the association between UAVs and MDs with latency and computation capacity constraints. To solve these two subproblems, we introduce a multi-agent reinforcement learning algorithm TF-PPO, which combines proximal policy gradient (PPO) [27] and task factorization network [28] with a deep neural network. After transmission from MDs to UAVs, UAVs need to schedule tasks to improve the completed ratio while balancing the computation load. This process influences the performance of UAVs and the QoE of MDs in the next. Then, we explain some specifics of these two algorithms.

## A. The Cooperation Policy of UAVs

In this subsection, we first explain the components of the TF-PPO algorithm, the architecture is shown in Fig. 2. Then we introduce how to combine the task factorization network with the PPO algorithm in this environment.

<!-- image-->  
Fig. 2. The architecture of TF-PPO. The top part represents the global network to train the cooperation model of multiple UAVs, The bottom part represents the individual model training process of each UAV.

1) The Components of TF-PPO: To solve the multi-UAV cooperation problem under limited observation, we formulate it as a Partially Observable Markov Decision Process (POMDP) [10], which is defined as an eight-tuple $< S , A , T , O , R , \mathcal { Z } , \pi _ { \theta } , \gamma ^ { d i s } >$

â¢ States: $S \triangleq \{ s _ { i } \}$ is the state of UAVs which is shown in the lower left corner of Fig. 2, which includes the state of UAVs, and the number of MDs within the coverage of each UAV. We use $s _ { i } = [ s _ { u _ { 1 } , i } , . . . , s _ { u _ { k } , i } , . . . , s _ { u _ { U } , i } ]$ to denote the states of UAVs at step i in the training process. For example, in the $i - t h$ step, the state of UAV $u _ { k }$ can be denoted by $s _ { u _ { k } , i } = < < \varphi _ { u _ { k } , x , t _ { i } } ^ { c o o r } , \varphi _ { u _ { k } , y , t _ { i } } ^ { c o o r } , \varphi _ { u _ { k } , z , t _ { i } } ^ { c o o r } > ,$ $a _ { u _ { k } , i } , r _ { u _ { k } , i } , s _ { u _ { k } , i + 1 } >$ . After storing this state, the UAV can be transited to the next state $s _ { u _ { k } , i + 1 }$ . This transition process can be used to measure whether the selected action is useful, then the action value $\widetilde { Q } _ { u _ { k } }$ of this action can be updated.

â¢ Action: $A \triangleq \{ a _ { i } \}$ is the set of actions of all the UAVs. The matrix of all the joint-action of UAVs in the step i can be denoted as $a _ { i } = [ a _ { u _ { 1 } , i } , . . . , a _ { u _ { k } , i } . . . , a _ { u _ { U } , i } ]$ where $a _ { u _ { k } , i } = [ \alpha ^ { a n g } , l _ { \alpha ^ { a n g } } ^ { d i s } ]$ includes the direction $a ^ { d i r }$ and angle $a ^ { a n g }$ . These two sub-actions determine the 3D coordinate of the UAV in the next step together. The change in altitude can help UAVs to avoid collisions. The UAV needs to select the direction and angle accurately to cover more MDs when the coordinates of MDs change. The core of this model is to get an optimal cooperation trajectory, where the trajectory is determined by the action selection in each state. The selection of action is related to the action value directly. If one action can achieve a higher reward during one step, the action value of this action will be updated to higher.

â¢ Transition Probability Function: $T ( S \times A \to S )$ is the probability of state $s ^ { \prime } \in S$ after execute the joint action $[ a _ { u _ { 1 } } , . . . , a _ { u _ { k } } , . . . , a _ { u _ { U } } ]$ at the previous state $s \in S .$

â¢ Observation Probability Function: O is the probability to observe $o \in O$ after executing a under the state s.

â¢ Partial Observation: Z contains all the observations and $S \times A \times O \to { \mathcal { Z } }$ means the probability of getting the observation $z \in { \mathcal { Z } }$ according to the previous state s and action a.

â¢ Policy Function: ÏÎ¸ is the policy function, which is a deep neural network with parameter $\theta _ { u _ { k } , a }$ to train the policy of selecting action a for the UAV uk.

â¢ Discount Factor: The notation $\gamma ^ { d i s } \in [ 0 , 1 )$ is the discount factor, which is used to adjust the influence of the future reward to the calculation.

â¢ Reward: $S \times A \to R$ denotes the immediate reward according to $a \in A$ to measure the selection of a. And the next state $s ^ { \prime } \in S$ also influences the value of $r \in R .$ . To maximize the reward, i.e., to maximize the coverage and keep the cooperation of UAVs, the global reward of the state $s _ { i }$ has been defined in (18).

$$
r = \sum _ { k = 1 } ^ { U } \Omega ^ { u _ { k } }\tag{18}
$$

In this formula, $\Omega ^ { u _ { k } }$ denotes the covered MDs by each UAV. Therefore, the total reward with discounted factor $\gamma ^ { d i s } \in [ 0 , 1 ]$ in the future can be shown as in (19).

$$
m a x \mathbb { E } \left[ \sum _ { t = 0 } ^ { T - 1 } \sum _ { \forall u _ { k } \in \mathcal { U } } \gamma ^ { d i s } r ( s _ { i } , a _ { i } ) \right]
$$

$$
{ \mathrm { s . t . ~ } } s _ { i } \in S , \pi _ { \theta } ( s _ { i } ) \in A\tag{19}
$$

(19a)

$$
\sum _ { i = 0 } ^ { T } \sum _ { k = 1 } ^ { U } u _ { k } \delta _ { u _ { k } } ^ { i s } = U T\tag{19b}
$$

Constraint (19a) denotes the state $s _ { i }$ and the action $a _ { i }$ belong to S and A. Constraint (19b) means UAVs cannot lose contact with each other in every time slot $t _ { i } , \delta _ { u \kappa } ^ { i s } = 1$ indicates that $u _ { k }$ can connect to either UAV, and $\delta _ { u _ { K } } ^ { i s } = 0$ otherwise. If one UAV is isolated, its observation will be deduced, and the cooperation computation is unsustainable. To optimize this process, we use the task factorization network to train the global optimal action selection, and it will be introduced next.

2) Task Factorization Network in TF-PPO: Proximal Policy Optimization(PPO) reinforcement learning algorithm is developed from the actor-critic architecture [21] and the policy gradient technique [10]. The objective of this algorithm is to search for an optimal policy that can generate the optimal actions of the agents, which can be denoted as in (20), where  is a clip fraction, and $A _ { i } =$ is generalized advantage estimator(GAE) [27], which is used to optimize the advantage function. The clip() function returns the upper and lower limits if the importance sampling [29] result is out of range. This equation directly limits the range of changes that the policy can make, then the stability during the training process has been improved.

$$
\begin{array} { r l } & { J ^ { C L I P } ( \pi _ { \theta } ) = \mathbb { E } [ m i n ( \frac { \pi _ { \theta ( a _ { u _ { k } } , i \mid s _ { i } ) } } { \pi _ { \theta _ { o l d } } ( a _ { u _ { k } , i } \mid s _ { i } ) } A _ { i } ,  } \\ & { ~  c l i p ( \frac { \pi _ { \theta ( a _ { u _ { k } } , i \mid s _ { i } ) } } { \pi _ { \theta _ { o l d } } ( a _ { u _ { k } , i } \mid s _ { i } ) } , 1 - \epsilon , 1 + \epsilon ) A _ { i } ] } \end{array}\tag{20}
$$

The network architecture of PPO is developed from Actor-Critic (AC) architecture, it also has two network models to train, i.e., the actor network and the critic network. The actor network is used to select an appropriate action $a _ { u _ { k } , i }$ for UAV $u _ { k }$ in the $i - t h$ step by policy gradient function, and the critic network is used to evaluate the result after executing action $a _ { u _ { k } , i }$ by valuebased function. These two networks can act as an athlete and a judge to improve performance, respectively. The loss functions of these two networks in this paper are listed in (21) and (22).

$$
L _ { a } ( \theta ) = J ^ { C L I P } ( \pi _ { \theta } )\tag{21}
$$

and

$$
L _ { c } ( \phi ) = E [ ( V ( s _ { t } ) - ( r _ { t } + \gamma V ( s _ { t + 1 } ) ) ^ { 2 } ]\tag{22}
$$

In MARL, each agent selects the optimal action by individual model according to the limited observation. As a result, the global optimal action set cannot be guaranteed. To compensate for this disadvantage, centralized training with decentralized execution (CTDE) has been proposed to expand the observation range of agents. However, the optimal joint action of all the agents still needs to be solved. In this background, the value decomposition network (VDN) [6] has been proposed to optimize the optimal joint-action selection process. VDN decomposes the actions of all the agents by assigning appropriate action value from the global value which is feedbacked from the jointaction execution. The idea of decomposition can be summarized as in (23), where $Q _ { t o t a l } ( a _ { i } )$ is the sum of all the individual function $\widetilde { Q } ( a _ { u _ { k } , i } )$ . Then a value decomposition neural network is trained to update the $Q _ { t o t a l } ( a _ { i } )$ and $\widetilde { Q } ( a _ { u _ { k } , i } )$

$$
Q _ { t o t a l } ( a _ { i } ) = \sum _ { k = 1 } ^ { U } \widetilde { Q } ( a _ { u _ { k } , i } )\tag{23}
$$

The loss function during the updating process can be shown as in (24), where the notation $y _ { i }$ and $\bar { Q } _ { t o t a l } ^ { p r e } ( a _ { i - 1 } )$ are calculated by $r _ { i } + \gamma a r g m a x Q _ { t o t a l } ^ { p r e } ( a _ { i - 1 } )$ and $\textstyle \sum _ { k = 1 } ^ { U } Q ^ { p r e } ( a _ { u _ { k } , i - 1 } )$ ï¼ respectively. This decomposition network can optimize the a $Q$ function of each agent significantly. However, VDN cannot process complex tasks due to the accumulation, i.e., the sum of $\widetilde { Q }$ function cannot adapt to all the relationships between individual $\widetilde { Q }$ function and global $Q _ { t o t a l }$ function. Then the task factorization network has been proposed, which can cope with more complex relationships.

$$
L ( \theta ) = \frac { 1 } { U } ( y _ { i } - Q _ { t o t a l } ^ { p r e } ( a _ { i } ) ) ^ { 2 }\tag{24}
$$

The core of the task factorization network is to construct the relationship between the individual $\widetilde { Q }$ function and the global $Q _ { t o t a l }$ function. In this paper, in order to factorize $Q _ { t o t a l }$ to ${ \widetilde { Q } } ,$ the individual-global-max (IGM) principle should be guaranteed. IGM is used to describe the equivalency of the individual optimality and the global optimality, which can be denoted as in (25).

$$
\underset { a } { a r g m a x } Q _ { t o t a l } ( a _ { i } ) = [ a r g m a x \widetilde { Q } ( a _ { u _ { k } } ) ] _ { k = 1 } ^ { U }\tag{25}
$$

It is the goal of the task factorization network, that can assign an appropriate reward value to each individual network from the global network. Then we need to find a set of individual $\widetilde { Q }$ to approximate the optimal $Q _ { t o t a l }$ , which can be shown as in (26), which means the sum of every optimal $\widetilde { Q } ( \boldsymbol { a } _ { u _ { k } } )$ must higher than the sum of $\widetilde { Q } ( \boldsymbol { a } _ { u _ { k } } )$ with other actions. If a set of $\bar { Q }$ functions satisfy this constraint, the IGM is also satisfied. To search for a $\widetilde { Q }$ set that meets this constraint, we combine the task factorization network with PPO as a multi-agent algorithm to estimate, the structure of this idea is shown in Fig. 2.

$$
\large [ a r g m a x \widetilde { Q } ( a _ { u _ { k } } ) \large ] _ { k = 1 } ^ { U } \geq [ \widetilde { Q } ( a _ { u _ { k } } ) \large ] _ { k = 1 } ^ { U }\tag{26}
$$

From Fig. 2, we can see the TF-PPO consists of two main networks, i.e., the individual network model in each UAV and a global network model for UAVs. The individual network model is mainly used to interact with the environment, monitor changes in the environment and choose appropriate action $a _ { u _ { k } , i }$ for UAV $u _ { k }$ in the i â th step. This individual network model consists of two sub-network models, i.e., the actor network and the critic network. The actor-network is used to select action $a _ { u _ { k } , i }$ and the critic network evaluates the performance of action $a _ { u _ { k } , i }$ to improve the actor network. The global network includes two sub-network models, the first model is the joint actionvalue network model, which is used to approximate joint actionvalue $Q _ { t o t a l } , \mathrm { i }$ t receives the selected action by each UAV and outputs the Qvalue of them. Another model is the state-value network model, which is used to compute a state-value $V ( s )$ to reduce the gap between $\widetilde { Q }$ and $Q _ { t o t a l }$ . Pseudocode is shown in Algorithm 1 and Algorithm 2.

## B. The Association Policy Between UAVs and Tasks

In the dynamic environment, the generation of tasks is random and difficult to predict. Therefore, MOGS focuses on achieving a near-optimal association between UAVs and tasks under constraints such as delay and computing capacity in dynamic environments through a few iterations.

In order to solve this problem, we propose an improved many-to-one association algorithm based on Gale-Shapley [30], which is called Many-to-One Gale-Shapley (MOGS). This idea is inspired by [31] and the association process has been improved. The GS algorithm is also called the deferred-acceptance algorithm. It is usually used to solve the stable association problem. In an association problem, the two sidesâ agents to associate have an equal number and each agent has a rank list to select the preferred agent on the other side. During this process, if one agent has been selected by two agents on another side simultaneously, it will select the preferred agent and release the original agent that has matched with it. The GS algorithm can realize a stable association with few iterations although it cannot guarantee the result is optimal. In this work, the MOGS inherits the advantages of the GS to realize a stable association and break its disadvantages, i.e., constrain the number of members on both sides. Next, the components and the association of MOGS are introduced.

Algorithm 1 Individual Model   
1: Input: MD locations, UAV locations   
2: Output: The cooperation model   
3: Initialize actor network $A _ { \theta }$ and critic $C _ { \phi }$ network randomly   
with parameters $\theta$ and $\phi$   
4: Initialize old actor network $A _ { \theta , o l d }  \theta$ with parameter $\theta _ { o l d }$   
5: Initialize buffer $\mathcal { D }  \oslash .$ , mini-batch $k _ { m i n i }$   
6: Set the position of $u _ { k }$ randomly   
7: for Episode in $1 , 2 , . . . , N$ do   
8: $t \gets 0$   
9: for t in $1 , 2 , . . . , T$ do   
10: Observe current state $s _ { t }$   
11: Select an action $a _ { t }$ by the old actor network $A _ { \theta , o l d }$   
12: Obtain the next state $s _ { t + 1 }$ , reward $r _ { t }$   
13: Collect previous trajectory $\mathcal { D }  \mathcal { D }$ âª   
$\left\{ s _ { t } , a _ { t } , r _ { t } , s _ { t + 1 } \right\}$   
14: Update the position of $u _ { k }$   
15: if $| \mathcal { D } | = D$ then   
16: Sample mini-batch $k _ { m i n i }$ data from D   
17: Send data to Global model and wait for the   
result   
18: Update $A _ { \theta }  \theta$ by Loss function   
19: Update $C _ { \phi } \gets \phi$ bu Loss function   
20: Update old actor $A _ { \theta , o l d }$ by $\theta _ { o l d }  \theta$   
21: Clear the buffer $\mathcal { D }  \oslash$   
22: end if   
23: end for   
24: end for

Algorithm 2 Global Model   
1: Input: Total observations from UAVs   
2: Output: Factorized $Q _ { j t }$ to each UAV   
3: Initialize replay memory D   
4: Initialize $[ Q _ { i } ] , Q _ { j t } , V _ { j t }$ with random parameters $\theta$   
5: Initialize target parameters $\theta ^ { - } = \theta$   
6: for episode $= 1 , . . . , N$ do   
7: Collect initial state $s ^ { 0 }$ and observation   
$o ^ { 0 } = [ O ( s ^ { 0 } , i ) ] _ { i = 1 } ^ { N }$ from each agent i   
8: for t = 1 to $T$ do   
9: With probability  select a random action $a _ { i } ^ { t }$   
10: Update $\theta ^ { - } = \theta$ with fixed period   
11: end for   
12: end for

1) The Components of MOGS Algorithm:

â¢ Active Party: The active party in MOGS is the set of tasks $\mathcal { M } _ { t _ { i } }$ generated by MDs in $t _ { i } .$ , every task has a rank list to sort the UAVs which can process ${ \mathrm { i t } } ,$ and it requests to associate with the first UAV in its list.

â¢ Passive Party: The passive party in MOGS is the set of UAVs U , it only receives the tasks from MDs but does not select the tasks actively. Every UAV also has an equality to rank different types of tasks; this equality is the criterion to judge whether a task is suitable to process and will be introduced below.

â¢ Procedure: The process of association mainly consists of three steps, and we use UAV $u _ { k }$ to denote the first UAV in the rank list of MD $d _ { j }$ here. First, in the $t _ { i }$ time slot, UAVs send the topology information and the state information to MDs in their coverage area. Then, after receiving the information from UAVs, every MD computes the rank list and sends its task to the UAV which is the first in the rank list. Finally, the UAV $u _ { k }$ receives the task $\tau _ { d _ { j } , t _ { i } }$ generated by MD $d _ { j }$ due to the highest level in the rank list of MD $d _ { j }$ The UAV $u _ { i }$ judges whether to process or relay $\tau _ { d _ { j } , t _ { i } }$ to other UAVs according to the latency constraint of $\tau _ { d _ { j } , t _ { i } }$ and the optimization formula which will be introduced below. To avoid some tasks being transmitted to another high-loaded UAV, we divide UAVs into two categories, i.e., ${ { \lambda } _ { l o w } }$ and $\mathcal { U } _ { h i g h } . \ \mathcal { U } _ { h i g h }$ includes high-loaded UAVs, another category ${ { \lambda } _ { l o w } }$ includes low-loaded UAVs. Highloaded UAVs in $\mathcal { U } _ { h i g h }$ transmit tasks in their task queue to low-loaded UAVs ${ { \mathcal { U } } _ { l o w } }$ under the latency constraint. This process can avoid task collision while guaranteeing the tasks transmitted can be computed.

â¢ Rule: To solve the problem $P$ while realizing the MOGS association under the constraints, some rules have been proposed to solve the subproblems during the association process. The first subproblem is to assign a suitable UAV to process the sudden tasks. The UAV can provide a higher transmission rate at closer distances, however, the UAV that is the closest to the task may not provide process capacity due to the overlong task queue and limited computation capacity. Thus, how to find a suitable UAV from the whole swarm within the constraint of tolerant latency of tasks under a dynamic environment needs to be solved. We propose an equation as a rule to help construct the association between UAVs and tasks, which can be formulated as in (27), where $\alpha ^ { r } , \beta ^ { r }$ are coefficients to trade the weight of uplink rate, downlink between UAV and task, $\gamma ^ { l }$ is used to adjust the weight of the computation load of UAV. This equation mainly focuses on selecting the most suitable UAV for the task $\tau _ { d _ { j } , t _ { i } }$ , the other UAVs will also be sorted based on this equation. However, its shortcomings are also obvious, the cooperation performance of UAVs may be degraded due to the overload of some UAVs. Then we consider proposing a rule to help UAVs get better cooperative task scheduling, it is also the second subproblem.

$$
u ^ { o r d } = \left\{ \begin{array} { c } { { ( m a x \left\{ \alpha ^ { r } r _ { d _ { j } , u _ { k } } ^ { u p } + \beta ^ { r } r _ { u _ { k } , d _ { j } } ^ { d o w n } + \gamma ^ { l } \chi _ { u _ { k } , t _ { i } } ^ { l o } \right\} } } \\ { { \forall j , k , i ) , 1 } } \\ { { o t h e r , 0 } } \end{array} \right.\tag{27}
$$

The second subproblem is to coordinate the cooperation between UAVs to avoid overloading a single UAV. The concurrency of tasks happens frequently in practice, and an overloaded UAV may cause optimization performance degradation while receiving overmuch tasks. To help the UAV $u _ { k }$ to judge whether a task $\tau _ { d _ { j } , t _ { i } }$ can be processed by itself or transmitted to UAV $u _ { k + 1 }$ , we design a rule as in (28).

Algorithm 3 MOGS Algorithm   
1: Input: The set of tasks and UAVs   
2: Output: The association result of tasks and UAVs   
3: Initialization Data: The set of UAVs U , the set of tasks $\boldsymbol { \mathcal { M } } _ { t _ { i } }$   
4: Compute the preference order $P _ { \tau _ { d _ { j } , t _ { i } } } ^ { U A V }$ of UAVs U by each   
task $\tau _ { d _ { j } , t _ { i } } , j \in M$ according to $\dot { \alpha ^ { r } } r _ { d _ { j } , u _ { k } } ^ { u p } + \beta ^ { r } r _ { u _ { k } , d _ { j } } ^ { d o w n } +$   
$\gamma ^ { l } \chi _ { u _ { k } , t _ { i } } ^ { l o }$   
5: for $u _ { k } \in \mathcal { U }$ do   
6: Compute the computation load of each UAV   
7: end for   
8: for steps=[1, ..., N ] do   
9: for $u _ { k } \in \mathcal { U }$ do   
10: Divide U into ${ { \lambda } _ { l o w } }$ and ${ { \mathcal { U } } _ { h i g h } }$ according to the   
computation load   
11: end for   
12: for $\tau _ { d _ { j } , t _ { i } } \in u _ { k } , u _ { k } \in \mathcal { U } _ { h i g h }$ do   
13: if Priority is satisfied then   
14: if Latency is satisfied then   
15: Transmit $\tau _ { d _ { j } , t _ { i } }$ to $u _ { k }$   
16: end if   
17: end if   
18: end for   
19: end for

$$
\begin{array} { r } { u ^ { s u } = \left\{ \begin{array} { l l } { \Gamma _ { u _ { k + 1 } , d _ { j } } + \frac { \gamma _ { \tau _ { d _ { j } } , t _ { i } } + \chi _ { u _ { k + 1 } , t _ { i } } ^ { l o } } { \mathcal { E } _ { u _ { k + 1 } } } + \Delta ^ { l } \frac { \chi _ { u _ { k + 1 } } ^ { m a x } } { \chi _ { u _ { k + 1 } , t _ { i } } ^ { l o } } } \\ { \qquad \leq \sigma _ { \tau _ { d _ { j } , t _ { i } } } } \\ { \quad o t h e r } \end{array} \right. } \end{array}\tag{, 1}
$$

, 0

(28)

From the Equation (28), the UAV uk can judge whether $u _ { k + 1 }$ is suitable for computing task $\tau _ { d _ { j } , t _ { i } }$ . We additionally add a term $\Delta ^ { l } \frac { \chi _ { u _ { k + 1 } } ^ { m a x } } { \chi _ { u _ { k + 1 } , t _ { i } } ^ { l o } } \leq \sigma _ { \tau _ { d _ { j } , t _ { i } } }$ to denote the queue latency before computing $\tau _ { d _ { j } , t _ { i } }$ if it is transmitted to $u _ { k + 1 }$ ï¼ where the $\Delta ^ { l } \in 0 , 1$ can be set based on the environment, the more complex the environment, it closer to 1 if the environment is more complex.

Algorithm 3 describes the whole process of constructing association between UAVs and tasks, and how to schedule tasks between UAVs in detail. To construct an association relationship, tasks need to sort UAVs according to the transmission rate and the state of UAVs (Line 3). After sorting, some UAVs may be in the overload state and some tasks need to be scheduled (Line 5). To balance the computation load of UAVs, they are divided into ${ { \lambda } _ { l o w } }$ and $\mathcal { U } _ { h i g h }$ to transmit tasks (Lines 7-18). To select appropriate next UAV for one task $\tau _ { d _ { j } , t . }$ i in the queue of UAV uk, the Equation (27) and Equation (28) are used to judge whether one UAV is suitable for $\tau _ { d _ { j } , t }$ (Line 11-15). More details on the stability analysis and the complexity analysis are provided in the Supplemental material.

TABLE III  
SIMULATION PARAMETERS
<table><tr><td>Parameters</td><td>Value</td></tr><tr><td>Computation capacity of UAV</td><td>100MHz</td></tr><tr><td>Transmission bandwidth</td><td>50Mbps</td></tr><tr><td>The volume of task</td><td>0.1MB~1MB</td></tr><tr><td>The length of task set</td><td>1000</td></tr><tr><td>The1 number of UAVs</td><td>2~12</td></tr><tr><td>The propel power of UAV</td><td>7W</td></tr><tr><td>The coverage radius of UAV</td><td>20m~140m</td></tr><tr><td>The flight speed of UAV</td><td>25km/h</td></tr><tr><td>The computation power of UAV</td><td>5W</td></tr><tr><td>The transmission power of UAV</td><td>1W</td></tr><tr><td>The value of  $\Delta ^ { l }$ </td><td>0.8</td></tr></table>

## VI. SIMULATION RESULTS AND DISCUSSION

In this section, we demonstrate the effectiveness of TF-PPO and MOGS through extensive simulations. These simulations are conducted on a DELL workstation with one RTX3090 graphic card and Intel(R) Xeon(R) Gold 6226R @2.90GHz, and the operation system is Win10 21H2. We set the size of the environment as a 2km Ã 2km, the MDs are distributed in this area and follow a PPP distribution. The number of UAVs ranges from 2 to 12 to demonstrate the performance of the TF-PPO. The coverage radius of UAV ranges from 30m to 130m, the bigger coverage radius means more UAVs can communicate with MDs directly without moving. The initial position of UAVs is not the same, and we guarantee each UAV can communicate with at least one UAV. The number of MDs is set as 800, dependent tasks and independent tasks are generated by other MDs and follow a normal distribution. Some more specific information on parameters are listed in Table III.

## A. Performance Verification and Discussion of TF-PPO

To verify the performance of TF-PPO, we use some metrics to measure, including the throughput and the energy consumption of UAVs, the computation latency of tasks and the number of completed tasks. Some reinforcement learning algorithms including VDN [6], QMIX [32], QTRAN [33], MADDPG [17] and MAPPO [18] are additionally selected to compare with TF-PPO. More details on these algorithms are provided in the Supplemental Material.

While training these algorithms, the maximum iteration steps are all set as 5000, and 100 steps in each episode. First, we compare the influence of energy efficiency and the throughput with different coverage radii of UAVs. The result is shown in Fig. 3.

In Fig. 3(a) and 3(b), The VDN algorithm has the worst performance. It cannot achieve a good performance due to its value decomposition function, which only relies on the accumulation from every individual Q value, it cannot reflect the complex environment accurately. The QMIX algorithm also has a disadvantage during the value decomposition process, it leverages the monotonicity between individual $Q _ { i }$ value and global $Q _ { t o t a l }$ value. They still cannot approximate the complex environment. The performance of the QTRAN algorithm is close to the MAD-DPG but better than VDN and QMIX. It alternatively constructs a deep neural network for task factorizing, which is adapted to the TF-PPO. This network can train a model to study the $Q _ { t o t a l }$ value which is very close to the real $Q _ { t o t a l }$ value, this can make sure the global $Q _ { t o t a l }$ is right. The final two algorithms, i.e., the MADDPG and the MAPPO, their performance are very close to the TF-PPO. However, the TF-PPO still has an advantage while the coverage radius is 30m, which means the TF-PPO can cope with a more complex environment. With the help of the task factorization network, the TF-PPO can construct the right relationship between individual $Q _ { i }$ value and global $Q _ { t o t a l }$ value. The architecture of the TF-PPO is very similar to the MAPPO. They all adopt the centralized training and decentralized execution mode, and we especially optimize the global network by integrating the task factorization network. Thus, the TF-PPO can trade the decomposition between each individual action selection, and then the joint action selection process of all the UAVs can be optimized.

<!-- image-->

<!-- image-->  
(b)  
Fig. 3. The energy efficiency and throughput comparison with different coverage radii of UAVs.

By observing Fig. 3, We can observe that the TF-PPO algorithm can achieve the upper bound efficiency while the radius is 30m, 90m and 130m, and the upper bound throughput while the radius is 30m, 90m, 110m and 130m in Fig. 3(a) and 3(b), respectively. We also discuss some disadvantages of the TF-PPO alternatively. For example, it cannot play to its strengths to achieve the upper bound energy efficiency when the coverage radius is 50m and 70m. We speculate the alternative task factorization network may influence the efficiency during the training process or the factorization of $Q _ { t o t a l }$ value still needs to be improved. We will continue executing more simulations to verify our idea.

We additionally verify the impact of the number of UAVs on the TF-PPO. The metrics are still energy efficiency and throughput. We additionally add a comparison respect, i.e., the convergence curve to observe the difference during the training process. The result can be summarized as follows.

Fig. 4(a) depicts the change of the energy efficiency under different numbers of UAVs, we can observe that the VDN algorithm has the worst performance, as well as the QMIX algorithm. The reason can be concluded that the value decomposition function cannot adapt to the complex environment. When the number of UAVs is increased, the state space and joint action space grow exponentially. Therefore, the training result cannot be improved quickly. Finally, their result is the worst under limited episodes. The efficiency of the MAPPO is higher than the MADDPG, the reason can be summarized as the optimization of the convergence process, especially the clip() function, which limits the update range to get a more stable result. We adapt this advantage and combine the task factorization network in the global network so that the performance of the TF-PPO can be better than the other algorithms.

Fig. 4(b) describes the throughput result achieved by these six algorithms. When the number of UAVs is 2, the throughput achieved by these algorithms is very similar. This result is because the movement of UAVs is not directly related to the throughput. After increasing the number of UAVs, more MDs can be covered, the performance of the cooperation policy decides the throughput significantly. From Fig. 4(b), we can find the throughput increases observably. However, the TF-PPO cannot achieve the best performance when the number of UAVs is 4, 6 and 8. We speculate that the MADDPG and the MAPPO still have some advantages when the environment is not very complex. When the number of UAVs increases to 10 and 12, the advantage of the task factorization network can be highlighted, i.e., the complex relationship between global $Q _ { t o t a l }$ value and individual Qican be constructed and the cooperation policy can be optimized. We can conclude that the TF-PPO is more suitable for the complex multi-agent environment.

Fig. 4(c) and 4(d) are the convergence curves of these six algorithms. Fig.4(c) describes the curve when the number of UAVs is 2. We can observe that the TF-PPO and the MAPPO can achieve the highest reward. However, the converge speed of the TF-PPO is slower than the MAPPO. We speculate the training of the task factorization network consumes some resources and the MAPPO is easier to train than the TF-PPO. From Fig. 4(d), we can observe the convergence of the TF-PPO is much quicker than other algorithms. The task factorization network makes the cooperative joint action selection improved, then the cooperative training is also improved.

In summary, we demonstrate the advantages of TF-PPO from five aspects, i.e., the energy efficiency and the throughput with different coverage radii, the energy efficiency and the throughput with different numbers of UAVs, the convergence curve with different numbers of UAVs. In these simulations, TF-PPO can construct the relationship between global $Q _ { t o t a l }$ and individual $Q _ { i }$ more accurately than the VDN, the QMIX and the QTRAN. And the TF-PPO can adapt to a more complex environment than the MADDPG and the MAPPO, especially in a multiagent environment. Next, we will verify the performance of the MOGS by extensive simulations.

## B. Performance Verification and Discussion of MOGS

In the second simulation, we verify the effectiveness of MOGS by comparing it with other algorithms, which include the Genetic algorithm, Ant Colony Optimization (ACO), Particle Swarm Optimization (PSO) and Greedy algorithm. We verify the performance of the MOGS compared with other algorithms from two aspects, the first metric is the completed ratio. It is calculated by dividing the number of tasks completed by the total number of tasks. The completed ratio reflects whether a task queue of one UAV is suitable for this UAV to compute. The second metric is the computation load of each UAV. The results of these two metrics are shown in Fig. 5.

<!-- image-->  
(a)

<!-- image-->  
(bï¼

<!-- image-->  
(c)

<!-- image-->  
(d)

Fig. 4. Some comparisons with different numbers of UAVs.  
<!-- image-->

<!-- image-->  
(bï¼

<!-- image-->  
ï¼Cï¼  
Fig. 5. The completed ratio and computation load comparison.

Fig. 5(a) describes the completed ratio and the average completed ratio of each UAV in these algorithms. Where the 10 points on the left side denote the completed ratio of each UAV in these five algorithms, and the point on the far right denotes the average completed ratio of 10 UAVs in these 5 algorithms. We can observe that the Greedy algorithm has the worst performance. The performance of the PSO and the genetic algorithm are close to the MOGS. While the PSO is a bit higher than the genetic algorithm, we speculate the reason is that the PSO is better than the genetic algorithm in the global search respect. The genetic algorithm may fall into the local optimization although it has the mutation ability. The ACO has the best performance in the completed ratio, it can search for the optimal solution globally. However, we find it converges more slowly than others. Thus, the PSO may not be applied for practice although it has the best performance.

<!-- image-->

Fig. 5(b) describes the computation load of each UAV in these five algorithms. The smoother curve denotes the more balanced load of UAVs. The balanced status of UAVs can avoid the overloading of some UAVs to a certain extent. We can find the ACO is the most stable, and the MOGS has a relatively poor performance but is better than PSO and GA.

(a) The initial state of the MOGS.  
(b) The final state of the MOGS.  
<!-- image-->  
Fig. 6. Visualizations of the MOGS.

In this simulation, although the MOGS has not achieved the best performance in the above simulations, we still hold the point that the MOGS is the most suitable for the dynamic environment. Compared with the other four heuristic algorithms, the MOGS is extremely simple to achieve the result. The convergence process of the MOGS has been shown in Fig. 5(c). We can observe the MOGS only needs 12 iterations to be converged. The task set can be transmitted to UAVs and canceled all the time due to the insensitivity of the MOGS.

We also visualize the environment at the initial and final states in Fig. 6. In Fig. 6(a), we can observe that the computation load range of the UAV is 0 to 350, with different loads of the

UAV with different colors. We can find that there is a high-load UAV, and three normal-load UAVs, the rest of the low-load. This situation reflects what happens if the task is only transmitted to the selected optimal UAV, that is, some UAVs are overloaded and some are under-loaded. The computation efficiency will be reduced in this situation. In Fig. 6(b), we can observe that the computation load of UAVs has been balanced. The computation load ranges from 95 to 135. There are merely two UAVs with high and low loads respectively. From this figure, it can be verified that MOGS is highly effective in balancing the loads of UAVs.

There are still some limitations of MOGS. It is impossible to transmit tasks multiple times due to the constraint of latency. The final matching result can not guarantee that all tasks can be completed, which is also related to the latency constraint, but in the case of high concurrency, it is difficult to ensure that all tasks are completed due to the computation power limitation of the UAV. This is consistent with previous studies.

## VII. CONCLUSION

In this paper, we focus on optimizing multiple objectives within a dynamic and complex environment. The multiple objectives encompass the latency of the computation process of tasks, the energy consumption of UAVs, and the number of completed tasks. We convert these objectives into a single objective, i.e., maximizing throughput. This single-optimization problem is addressed through two processes: one is to optimize the cooperation among UAVs, and the other is to optimize the association process between tasks and UAVs. To optimize the cooperation of UAVs, we integrate the task factorization network with a deep reinforcement learning algorithm to train a multi-agent algorithm. To optimize the scheduling process of tasks, we propose an improved Gale-Shapley algorithm to enhance the performance of the association process. Finally, some simulations illustrate the performance of our solutions. In the future, we will continue to research a superior solution to optimize the multi-agent cooperation and task scheduling process.

## REFERENCES

[1] Y. Zeng, R. Zhang, and T. J. Lim, âWireless communications with unmanned aerial vehicles: Opportunities and challenges,â IEEE Commun. Mag., vol. 54, no. 5, pp. 36â42, May 2016.

[2] Z. Sun, G. Sun, Y. Liu, J. Wang, and D. Cao, âBARGAIN-MATCH: A game theoretical approach for resource allocation and task offloading in vehicular edge computing networks,â IEEE Trans. Mobile Comput., vol. 23, no. 2, pp. 1655â1673, Feb. 2024.

[3] H. Pan, Y. Liu, G. Sun, P. Wang, and C. Yuen, âResource scheduling for UAVs-aided D2D networks: A multi-objective optimization approach,â IEEE Trans. Wireless Commun., vol. 23, no. 5, pp. 4691â4708, May 2024.

[4] J. Zhang et al., âStochastic computation offloading and trajectory scheduling for UAV-assisted mobile edge computing,â IEEE Internet Things J., vol. 6, no. 2, pp. 3688â3699, Apr. 2019.

[5] R. Liu, A. Liu, Z. Qu, and N. N. Xiong, âAn UAV-enabled intelligent connected transportation system with 6G communications for internet of vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 2, pp. 2045â 2059, Feb. 2023.

[6] Y. Hu, M. Chen, W. Saad, H. V. Poor, and S. Cui, âDistributed multiagent meta learning for trajectory design in wireless drone networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3177â3192, Oct. 2021.

[7] S. Mao, S. He, and J. Wu, âJoint UAV position optimization and resource scheduling in space-air-ground integrated networks with mixed cloud-edge computing,â IEEE Syst. J., vol. 15, no. 3, pp. 3992â4002, Sep. 2021.

[8] Y. Shi, J. Wu, L. Liu, D. Lan, and A. Taherkordi, âEnergy-aware relay optimization and power allocation in multiple unmanned aerial vehicles aided satellite-aerial-terrestrial networks,â IEEE Syst. J., vol. 16, no. 4, pp. 5293â5304, Dec. 2022.

[9] W. Zhou et al., âPriority-aware resource scheduling for UAV-mounted mobile edge computing networks,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 9682â9687, Jul. 2023.

[10] X. Wang, Z. Ning, S. Guo, M. Wen, L. Guo, and H. V. Poor, âDynamic UAV deployment for differentiated services: A multi-agent imitation learning based approach,â IEEE Trans. Mobile Comput., vol. 22, no. 4, pp. 2131â2146, Apr. 2023.

[11] Z. Ning et al., âDynamic computation offloading and server deployment for UAV-enabled multi-access edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 5, pp. 2628â2644, May 2023.

[12] R. Zhou, X. Wu, H. Tan, and R. Zhang, âTwo time-scale joint service caching and task offloading for UAV-assisted mobile edge computing,â in Proc. - IEEE Conf. Comput. Commun. (INFOCOM), Jun. 2022, pp. 1189â1198.

[13] C. Wang, D. Zhai, R. Zhang, H. Li, H. Cao, and A. Jindal, âJoint UAVs position optimization and offloading decision for blockchain-enabled intelligent transportation,â in Proc. IEEE Conf. Comput. Commun. Workshops (INFOCOM WKSHPS), Jun. 2022, pp. 1â6.

[14] M. Hua, L. Yang, C. Pan, and A. Nallanathan, âThroughput maximization for full-duplex UAV aided small cell wireless systems,â IEEE Wireless Commun. Lett., vol. 9, no. 4, pp. 475â479, Apr. 2020.

[15] B. Zhu, E. Bedeer, H. H. Nguyen, R. Barton, and Z. Gao, âUAV trajectory planning for AoI-minimal data collection in UAV-aided IoT networks by transformer,â IEEE Trans. Wireless Commun., vol. 22, no. 2, pp. 1343â1358, Feb. 2023.

[16] P. Qin, X. Wu, Z. Cai, X. Zhao, Y. Fu, M. Wang, and S. Geng, âJoint trajectory plan and resource allocation for UAV-enabled C-NOMA in air-ground integrated 6G heterogeneous network,â IEEE Trans. Netw. Sci. Eng., vol. 10, no. 6, pp. 3421â3434, Nov./Dec. 2023.

[17] J. Wu, D. Li, Y. Yu, L. Gao, J. Wu, and G. Han, âAn attention mechanism and adaptive accuracy triple-dependent MADDPG formation control method for hybrid UAVs,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 9, pp. 11648â11663, Sep. 2024.

[18] J. Kang et al., âUAV-assisted dynamic avatar task migration for vehicular metaverse services: A multi-agent deep reinforcement learning approach,â IEEE/CAA J. Automatica Sinica, vol. 11, no. 2, pp. 430â445, Feb. 2024.

[19] X. Zhang, H. Zhao, J. Wei, C. Yan, J. Xiong, and X. Liu, âCooperative trajectory design of multiple UAV base stations with heterogeneous graph neural networks,â IEEE Trans. Wireless Commun., vol. 22, no. 3, pp. 1495â1509, Mar. 2023.

[20] Y. Zhang, Z. Mou, F. Gao, L. Xing, J. Jiang, and Z. Han, âHierarchical deep reinforcement learning for backscattering data collection with multiple UAVs,â IEEE Internet Things J., vol. 8, no. 5, pp. 3786â3800, Mar. 2021.

[21] J. Hu, H. Zhang, L. Song, R. Schober, and H. V. Poor, âCooperative internet of UAVs: Distributed trajectory design by multi-agent deep reinforcement learning,â IEEE Trans. Commun., vol. 68, no. 11, pp. 6807â 6821, Nov. 2020.

[22] T. Ren et al., âEnabling efficient scheduling in large-scale UAVassisted mobile-edge computing via hierarchical reinforcement learning,â IEEE Internet Things J., vol. 9, no. 10, pp. 7095â7109, May 2022.

[23] Q. Tang, Z. Yu, C. Jin, J. Wang, Z. Liao, and Y. Luo, âCompleted tasks number maximization in UAV-assisted mobile relay communication system,â Comput. Commun., vol. 187, pp. 20â34, Apr. 2022.

[24] Z. Hu et al., âJoint resources allocation and 3D trajectory optimization for UAV-enabled space-air-ground integrated networks,â IEEE Trans. Veh. Technol., vol. 72, no. 11, pp. 14214â14229, Nov. 2023.

[25] C. Liu, M. Ding, C. Ma, Q. Li, Z. Lin, and Y.-C. Liang, âPerformance analysis for practical unmanned aerial vehicle networks with LoS/NLoS transmissions,â in Proc. IEEE Int. Conf. Commun. Workshops (ICC Workshops), pp. 1â6, Jul 2018.

[26] F. A. Administration, âPART 107âSMALL UNMANNED AIRCRAFT SYSTEMS.â Website, Jun. 2016. [Online]. Available: https://www.ecfr. gov/current/title-14/chapter-I/subchapter-F/part-107#107.41

[27] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, âProximal policy optimization algorithms,â 2017, arXiv:1707.06347.

[28] K. Son, D. Kim, W. J. Kang, D. E. Hostallero, and Y. Yi, âQTRAN: Learning to factorize with transformation for cooperative multi-agent reinforcement learning,â in Proc. 36th Int. Conf. Mach. Learn., K. Chaudhuri and R. Salakhutdinov, Eds., vol. 97, PMLR, Jun. 2019, pp. 5887â5896.

[29] A. R. Mahmood, H. P. Van Hasselt, and R. S. Sutton, âWeighted importance sampling for off-policy learning with linear function approximation,â in Proc. Adv. Neural Inf. Process. Syst., vol. 27, 2014, pp. 3014â3022.

[30] D. Gale and L. S. Shapley, âCollege admissions and the stability of marriage,â Amer. Math. Monthly, vol. 69, no. 1, pp. 9â15, 1962.

[31] H. Hydher, D. N. K. Jayakody, K. T. Hemachandra, and T. Samarasinghe, âUAV deployment for data collection in energy constrained WSN system,â in Proc. IEEE Conf. Comput. Commun. Workshops (INFOCOM WKSHPS), Piscataway, NJ, USA: IEEE Press, Jun. 2022, pp. 1â6.

[32] T. Rashid, M. Samvelyan, C. S. De Witt, G. Farquhar, J. Foerster, and S. Whiteson, âMonotonic value function factorisation for deep multiagent reinforcement learning,â J. Mach. Learn. Res., vol. 21, no. 178, pp. 1â51, 2020.

[33] K. Zhang, Z. Yang, and T. BaÂ¸sar, âMulti-agent reinforcement learning: A selective overview of theories and algorithms,â Handbook of Reinforcement Learning and Control, vol. 325, K. G. Vamvoudakis, Y. Wan, F. L. Lewis and D. Cansever, Eds., Cham, Switzerland: Springer, 2021, pp. 321â384.

<!-- image-->

Liang Zhao (Member, IEEE) received the Ph.D. degree from the School of Computing, Edinburgh Napier University, in 2011. He is a Professor with Shenyang Aerospace University, China. He is also a JSPS Invitational Fellow (2023). He was listed as Top 2% of scientists in the world by Standford University (2022 and 2023). He served as the Chair of several international conferences and workshops, including 2022 IEEE BigDataSE (Steering Co-Chair), 2021 IEEE TrustCom (Program Co-Chair), 2019 IEEE IUCC (Program Co-Chair), and 2018â

2022 NGDN workshop (Founder). He is an Associate Editor of Frontiers in Communications and Networking and Journal of Circuits Systems and Computers. He has been a Guest Editor of IEEE TRANSACTIONS ON NETWORK SCIENCE AND ENGINEERING, Springer Journal of Computing, etc.

<!-- image-->

Shuo Li received the B.S. degree from Zaozhuang University, Zaozhuang, China, in 2019. He is currently working toward the M.S. degree with Shenyang Aerospace University. His research interests include edge computing, UAV trajectory planning, and digital twin.

<!-- image-->

Zhiyuan Tan received the Ph.D. degree from the University of Technology Sydney, Australia, in 2014. He is an Associate Professor with the School of Computing, Engineering and the Built Environment, Edinburgh Napier University, U.K. He was a Postdoctoral Researcher with the University of Twente, NL between 2014 and 2016. He is an Associate Editor of IEEE TRANSACTIONS ON RELIABILITY, IEEE OPEN JOURNAL OF THE COMPUTER SOCIETY, Journal of Ambient Intelligence and Humanized Computing, and the Journal

of Ambient Intelligence and Humanized Computing, as well as an Academic Editor of Security and Communication Networks. He is a Member of the ACM.

<!-- image-->

Ammar Hawbani received the B.S. degree in computer software and theory from the University of Science and Technology of China (USTC), in 2009, and the M.S. and Ph.D. degrees from USTC, in 2012 and 2016, respectively. He is a Full Professor with the School of Computer Science, Shenyang Aerospace University. He served as a Postdoctoral Researcher with the School of Computer Science and Technology, USTC from 2016 to 2019. He worked as an Associate Researcher with the School of Computer Science and Technology, USTC from

2019 to 2023. Currently, he holds the position of a Full Professor with the School of Computer Science, Shenyang Aerospace University. His research interests span IoT, WSNs, WBANs, WMNs, VANETs, and SDN.

<!-- image-->

Stelios Timotheou (Senior Member, IEEE) received the Ph.D. degree in intelligent systems and networks from Imperial College London. He is an Associate Professor with the Department of Electrical and Computer Engineering, University of Cyprus, Nicosia, Cyprus. He is a faculty member with the KIOS Research and Innovation Center of Excellence. His research interests include monitoring, control, and optimization of critical infrastructure systems, with an emphasis on intelligent transportation systems and communication systems.

<!-- image-->

Keping Yu received the M.E. and Ph.D. degrees from the Graduate School of Global Information and Telecommunication Studies, Waseda University, Tokyo, Japan, in 2012 and 2016, respectively. He was a Research Associate from 2015 to 2019, a Junior Researcher from 2019 to 2020, and a Researcher from 2020 to 2022 with the Global Information and Telecommunication Institute, Waseda University. Currently, he is an Associate Professor, the Vice Director of Institute of Integrated Science and Technology, and the Director of the Network

Intelligence and Security Laboratory (YU Lab), Hosei University, Japan.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization/page_6_img_1.jpeg|page_6_img_1]]
2. [[../extracted_images/A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization/page_11_img_1.jpeg|page_11_img_1]]
3. [[../extracted_images/A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization/page_13_img_1.jpeg|page_13_img_1]]
4. [[../extracted_images/A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization/page_13_img_2.jpeg|page_13_img_2]]
5. [[../extracted_images/A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization/page_13_img_3.jpeg|page_13_img_3]]
6. [[../extracted_images/A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization/page_13_img_4.jpeg|page_13_img_4]]
7. [[../extracted_images/A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization/page_13_img_5.jpeg|page_13_img_5]]
8. [[../extracted_images/A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization/page_13_img_6.jpeg|page_13_img_6]]

---

