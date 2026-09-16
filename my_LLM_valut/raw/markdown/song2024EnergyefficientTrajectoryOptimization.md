# Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-Objective Reinforcement Learning

Fuhong Song , Mingsen Deng , Member, IEEE, Huanlai Xing , Member, IEEE, Yanping Liu , Fei Ye , and Zhiwen Xiao

AbstractâThis paper investigates the problem of energyefficient trajectory optimization with wireless charging (ETWC) in an unmanned aerial vehicle (UAV)-assisted mobile edge computing system. A UAV is dispatched to collect computation tasks from specific ground smart devices (GSDs) within its coverage while transmitting energy to the other GSDs. In addition, a high-altitude platform with a laser beam is deployed in the stratosphere to charge the UAV, so as to maintain its flight mission. The ETWC problem is characterized by multi-objective optimization, aiming to maximize both the energy efficiency of the UAV and the number of tasks collected via optimizing the UAVâs flight trajectories. The conflict between the two objectives in the problem makes it quite challenging. Recently, some single-objective reinforcement learning (SORL) algorithms have been introduced to address the aforementioned problem. Nevertheless, these SORLs adopt linear scalarization to define the user utility, thus ignoring the conflict between objectives. Furthermore, in dynamic MEC scenarios, the relative importance assigned to each objective may vary over time, posing significant challenges for conventional SORLs. To solve the challenge, we first build a multi-objective Markov decision process that has a vectorial reward mechanism. There is a corresponding relationship between each component of the reward and one of the two objectives. Then, we propose a new trace-based experience replay scheme to modify sample efficiency and reduce replay buffer bias, resulting in a modified multi-objective reinforcement learning algorithm. The experiment results validate that the proposed algorithm can obtain better adaptability to dynamic preferences and a more favorable balance between objectives compared with several algorithms.

Index TermsâMobile edge computing, multi-objective reinforcement learning, trajectory optimization, unmanned aerial vehicle, wireless charging.

## I. INTRODUCTION

W ITH the fast development of mobile communicationtechnology, ground smart devices (GSDs) play a sig- technologyï¼ ground smart devices (GSDs) play a significant role in diverse applications, such as intelligent grazing facilitated by high-definition cameras and environmental monitoring utilizing meteorological sensors. [1]. Specifically, GSDs can be distributed to monitor and sense their surroundings, thus offering unprecedented opportunities for emerging intelligent applications, such as augmented reality and infrastructure monitoring. These applications are usually computing-intensive, resulting in a surging demand for computing resources. However, GSDs often suffer from limited computing capability and battery life, due to small physical sizes and stringent production cost constraints [2].

Mobile edge computing (MEC) has been introduced to enhance the computing capability of GSDs by relocating computing resources to the network edge. Within this paradigm, GSDs are empowered to offload their computing-intensive applications to ground base stations (GBSs) situated nearby, thereby enabling them to efficiently support such applications [3]. In general, traditional MEC technologies are based on GBSs, which are placed on the ground and kept fixed. This means the wireless communication coverage of a GBS is limited, which restricts its ability to connect to users located beyond the GBSâs coverage area. Particularly, GBSs may encounter damage due to military attacks or natural disasters, causing a scarcity of computing resources and a decline in offloading performance [4].

Unmanned aerial vehicles (UAVs) have emerged as an efficient solution for extending communication coverage and enhancing deployment efficiency due to their high mobility and excellent maneuverability [5], [6]. For example, UAVs can provide vital communication support when GBS-based infrastructures are either unavailable during disaster rescue operations or sparsely distributed in remote mountainous areas. Moreover, when there is a sudden surge in GSDs that exceeds the capacity of network services, like during a crowded football match, UAVs can serve these GSDs as emergency computing platforms.

Digital Object Identifier 10.1109/TMC.2024.3384405

Therefore, equipped with communication and computing resources, UAVs can collect computation tasks from GSDs nearby and handle them.

Although UAV-assisted MEC offers various potential benefits, the energy constraint impedes its widespread use since UAVs and GSDs have limited battery life [7], [8]. Equipped with the laser beam, a high-altitude platform (HAP) can be strategically deployed in the stratosphere, making it possible for long-distance and high-power charging for UAVs [9]. However, it is unrealistic to directly charge GSDs using laser beams because it poses potential risks to both human safety and ground infrastructures. As an energy relay, a UAV can harvest the laser energy from the HAP and distribute the energy to GSDs by wireless power transfer (WPT). Moreover, the UAV can also adopt the harvested energy to process computation tasks collected by it from GSDs. In other words, the UAV plays two different roles, i.e., an energy relay and an MEC server. Nevertheless, there has been little research on the scenario in the literature.

On the other hand, simultaneously maximizing energy efficiency and the number of collected computation tasks has emerged as significant research attention in UAV-assisted MEC. The two objectives are in conflict with each other. However, most studies transform the multi-objective optimization (MOO) problem into a single-objective optimization (SOO) problem using the weighted sum method. Note that the weights assigned to each objective reflect the preferences between objectives. While the weighted sum method is adequate for situations where weights remain unchanged, it cannot be applied to scenarios with diverse preferences because they may vary over time. The dynamics further intensifies the complexity of the MOO problem, making it difficult to achieve good optimization results.

To improve the energy supply, this paper considers an HAPand-UAV collaborative MEC system including an HAP, a UAV, and many GSDs. Laser charging and WPT technologies are employed to maintain the energy supply of the UAV and GSDs. Specifically, the HAP with a constant height floats in the stratosphere in a quasi-static manner, and it can generate a high-power laser beam to charge the UAV. The UAV can transmit the harvested energy from the HAP to GSDs within its coverage while collecting computation tasks from a specific GSD. In the proposed system, we investigate the problem of energy-efficient trajectory optimization with wireless charging (ETWC). Unlike previous studies that focus on SOO or MOO using the weighted sum method, we concentrate on the simultaneous optimization of two conflicting objectives, i.e., energy efficiency and the number of collected tasks. To adapt to the dynamics of preferences, we address the modeled MOO problem by proposing a modified multi-objective reinforcement learning (MORL) algorithm. We summarize the contributions of this paper as follows.

We consider an HAP-and-UAV collaborative MEC system, which an HAP and a UAV cooperate with each other to provide energy supply and computing services to GSDs. The ETWC problem is formulated as an MOO problem, and its aim is to simultaneously maximize the UAVâs energy efficiency and the number of collected tasks via optimizing the UAVâs flight trajectories. Solving the MOO problem is quite challenging on account of the conflicting objectives, making it difficult to strike a balance between them.

To address the ETWC problem, we establish a multiobjective Markov decision process (MOMDP) model with a vectorial reward of two elements. Each element in the reward is associated with an optimization objective. A modified MORL algorithm with a trace-based experience replay (TER) scheme, namely MORL-TER, is proposed. The TER scheme treats a trace as an atomic unit when considering it for addition in or deletion from the experience buffer, thus can improve sample efficiency and reduce replay buffer bias.

- We perform comprehensive experiments on six generated test instances. The results demonstrate that MORL-TER can adapt to the dynamic preferences and achieve a favorable balance between objectives in most cases, as well as surpasses five state-of-the-art MORLs and two well-known multi-objective evolutionary algorithms regarding multiple evaluation indicators, including the average episodic regret, adaptation error, inverted generational distance, average energy efficiency, average number of tasks, average comprehensive objective indicator, and Friedman test.

The remainder of the paper is organized as follows. Section II provides a review of the related work in the field of UAVassisted networks. The system model and problem formulation are presented in Section III. In Section IV, a concise overview of MOMDP is provided. Section V elaborates the proposed MORL-TER algorithm for addressing the ETWC problem. Section VI analyzes and discusses the simulation results. Finally, Section VII concludes the paper.

## II. RELATED WORK

Considerable researchers have devoted significant attention to investigating diverse aspects of UAV-assisted networks with wireless charging. These investigations can primarily be classified into two categories, namely the traditional methods and reinforcement learning based methods.

## A. Traditional Methods

Recently, traditional methods, such as convex optimization, heuristics, and metaheuristics, have been adopted to optimize UAV-assisted networks, yielding favorable optimization outcomes. The authors in [7] considered a UAV-assisted MEC network with wireless charging. They introduced a convex approximation method to reduce the UAVâs energy consumption. The researchers in [10] investigated the trajectory and power optimization, where a GBS was deployed to charge the UAV. The concave-convex and dual decomposition based approach was introduced to maximize the energy efficiency. Hu et al. [11] studied a GBS and a UAV cooperative network, where the UAV can deliver information and energy to GSDs. They presented a block coordinate descending method to maximize the task-input bits. In [12], a multi-UAV cooperative trajectory optimization problem was studied by considering battery charging and servicing dynamic demands. A fast iterative cooperation method was introduced to plan the trajectories of UAVs. To prolong their battery life, the authors in [13] built a non-disruptive wireless rechargeable network, where a static wireless station charger (WSC) could charge UAVs by the WPT technology. They presented a baseline method to enhance the energy efficiency of UAVs. Similarly, the researchers in [14] also investigated the energy efficiency maximization problem, and adopted the Lagrange multiplier method to address it. In [15], the task offloading and UAV charging problem was studied, and the authors in [15] developed a mixed-integer linear programming model, with the energy consumption minimized. Shi et al. [16] studied a UAV-assisted WPT system, where the UAVâs energy was transmitted to GSDs. They proposed a two-stage scheme to maximize total harvested energy and minimize flight energy consumption. Wang et al. [17] investigated an air-ground integrated MEC network, where a UAV was adopted to offer offloading and charging services for GSDs. They developed a greedy algorithm to optimize the service latency. Li et al. [18] studied a UAV-assisted MEC network with wireless charging and proposed a two-stage alternating iterative algorithm to optimize the computation bits by planning the UAVâs trajectories. Zhang et al. [19] proposed a UAV-assisted MEC system, where the UAV was employed to process the tasks offloaded by the GSDs. The authors developed an iterative algorithm to reduce the total energy consumption. Gu et al. [20] investigated a UAV-assisted energy-efficient MEC network, where a UAV could be charged by a GBS. They adopted the convex optimization method to decrease energy consumption and enhance the energy storage of the UAV. Yang et al. [21] investigated a UAV-assisted wireless communication network with energy harvesting, and adopted the successive convex approximation technique to lower energy consumption by optimizing flight paths. In [22], a heuristic algorithm was adopted to efficiently charge GSDs using the WPT technology. Li et al. [23] presented a multi-UAV-enabled energy harvesting network. They developed a genetic algorithm based user assignment method to improve the UAVâs energy efficiency by planning flight paths.

## B. Reinforcement Learning Based Methods

One of the important functions of reinforcement learning (RL) is to choose actions that can maximize the expected cumulative reward through interactions between it and the environment. Yu et al. [8] introduced a new approach by extending deep deterministic policy gradient (DDPG), which could maximize the total energy harvested by GSDs and energy efficiency of the UAV. However, the algorithm failed to adapt to the scenarios with dynamic preferences. Cheng et al. [9] investigated the task and energy offloading problem in a UAV-assisted 6 G MEC network, where an HAP with a laser beam was adopted to charge UAVs. They introduced a new approach based on multi-agent DDPG, which could improve the total system utility. Zhang et al. [24] proposed an energy-efficient trajectory planning method, where one UAV was powered by both a charging station and solar energy. They developed a module-free RL method to optimize trajectory, aiming at maximizing energy efficiency and average data rate. In [25], the UAV energy transfer optimization was first built as a Markov decision process model. Then, a deep Qnetwork (DQN) based approach was presented to maximize the UAVâs long-term utility. Fu et al. [26] also adopted Q-learning to optimize the UAVâs trajectory when collecting sensor data from ground devices, which could minimize energy consumption. Inspired by aerial refueling, Zhu et al. [27] studied the charging UAV and mission UAV without interrupting the mission. They adopted a DDPG with adaptive parameter space noise to maximize the energy charging efficiency. The authors in [28] studied a stochastic energy harvesting system and proposed a modified DQN algorithm to maximize the long-term utility. In [29], a UAV adopted the radio frequency energy transfer to wirelessly charge GSDs. The researchers in [29] presented a DQN based method to decrease the age of information of GSDs. Oubbati et al. [30] employed a multi-agent RL approach to improve transmission and flight energy, aiming at maximizing the total energy received by UAVs. Zhang et al. [31] investigated an MOO problem, with the throughput, energy consumption, and harvested energy taken into account, and proposed an attentional DDPG algorithm to address the problem. For the task offloading and energy harvesting, Seid et al. [32] adopted a model-free multi-agent DDPG to minimize computation cost and resource price in multi-UAV-enabled IoT networks. Fan et al. [33] investigated a UAV trajectory planning problem in multiple WSCs, where the UAV was charged by WSCs. They proposed a multi-head attention mechanism based RL method to shorten the total travel distance of the UAV.

## C. Analysis and Motivation

In spite of the considerable efforts devoted to UAV-assisted MEC networks, there exist significant challenges with respect to system modeling and optimization techniques.

System Modeling: Many previous studies adopt one or more UAVs to wirelessly charge GSDs [8], [21], [23], [29]. While it can well support the computing needs of small-scale GSDs, such a scenario is unsuitable for large-scale GSD deployment. This is because UAVs have to charge plentiful GSDs and rapidly consume their battery power, resulting in short-distance flight missions and limited application range. Although GBSs can be deployed to maintain the energy supply of UAVs using the WPT technology [11], [25], they may be unavailable in some extreme scenarios such as military attacks and natural disasters.

To overcome the issue above, some studies [9] concentrate on the integration of HAP into UAV-assisted MEC systems. By establishing effective collaboration between HAP and UAV, it becomes possible to provide energy supply and computing services to GSDs. For instance, an HAP equipped with a laser beam can be deployed in the stratosphere to transmit the laser energy to UAVs. These UAVs harness the harvested laser energy to process computation tasks from GSDs. Moreover, UAVs can play an energy relay role to transmit their harvested energy from HAP to GSDs using WPT technology. Therefore, HAP-and-UAV collaborative MEC is a practical scenario. Nevertheless, there has been very little work on the collaborative scenario. Meanwhile, the integration also brings new challenges to the optimization of UAV trajectories. This is because the amount of energy harvested by the UAV from the HAP depends on the distance between them. In general, the amount of harvested energy has a nonlinear relationship with the distance. Further, the distance only relies on the UAVâs positions since the HAP maintains a quasi-static position and fixed floating height. Therefore, it is challenging to optimize the trajectories of the UAV to improve its energy efficiency and collect tasks as many as possible.

TABLE I  
COMPREHENSIVE COMPARISON BETWEEN THE RELATED WORKS AND OURS
<table><tr><td colspan="2">Reference</td><td>[7]</td><td>[8]</td><td>[9]</td><td>[10]</td><td>[11]</td><td>[12]</td><td>[13]</td><td>[14]</td><td>[15]</td><td>[16]</td><td>[17]</td><td>[18]</td><td>[19]</td><td>[20]</td></tr><tr><td rowspan="2">System modeling</td><td rowspan="2">Energy source Single-objective Multi-objective</td><td rowspan="2">UAV â</td><td>UAV</td><td>HAP â</td><td>GBS</td><td>GBS</td><td>UAV â</td><td>WSC</td><td>GBS</td><td>GBS</td><td>UAV</td><td>UAV</td><td>UAV</td><td>GBS</td><td>GBS</td></tr><tr><td></td><td></td><td>â</td><td>â</td><td></td><td>â</td><td>â</td><td>å</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td></tr><tr><td rowspan="2">Optimization technique</td><td rowspan="2">Traditional SORL MORL</td><td rowspan="2">â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2"> System</td><td rowspan="2">Reference Energy source</td><td>[21] UAV</td><td>[22]</td><td>[23]</td><td>[24]</td><td>[25]</td><td>[26]</td><td>[27]</td><td>[28]</td><td>[29]</td><td>[30]</td><td>[31]</td><td>[32]</td><td>[33]</td><td>Ours</td></tr><tr><td>Single-objective â</td><td>UAV â</td><td>UAV â</td><td>Sun</td><td>GBS</td><td>WSC â</td><td>UAV â</td><td>UAV â</td><td>UAV â</td><td>UAV â</td><td>UAV</td><td>UAV</td><td>WSC â</td><td>HAP</td></tr><tr><td rowspan="2">modeling Optimization</td><td rowspan="2">Multi-objective Traditional</td><td>â</td><td></td><td></td><td>â</td><td>â</td><td></td><td></td><td></td><td></td><td></td><td>â</td><td>â</td><td></td><td>â</td></tr><tr><td>SORL</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td></td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td>â</td><td></td></tr></table>

On the other hand, simultaneously optimizing energy efficiency and the number of collected tasks is one of the research hotspots in UAV-assisted MEC with wireless charging. Many previous studies optimize the two objectives separately, ignoring the conflict and easily causing biased optimization results. Furthermore, the preference between objectives may vary over time. For example, when a UAV operates with low battery levels, end-users may prioritize the reduction of energy consumption. Conversely, when UAVs possess ample energy reserves, they may concentrate on maximizing the number of collected tasks. Nevertheless, all existing works neglect the changing preferences, thus their methods are unsuitable for UAV-assisted MEC scenarios with dynamic preferences.

Optimization Technique: Traditional methods, including iterative algorithm [12], convex optimization [10], [21], Lagrange multiplier [14], heuristics [22], and metaheuristics [23], demonstrate satisfactory performance in addressing diverse optimization problem in static MEC networks, such as a UAV remains stationary at a fixed location throughout the entire flight process. Nevertheless, these methods face challenges in adapting to dynamic environments, especially when UAVs exhibit rapid mobility and tasks arrive in an unpredictable manner. The frequent dynamics and uncertainties often necessitate the repeated execution of these methods, causing increased computational overhead and slow response speed. Therefore, these traditional approaches may not be well-suited for quickly responding to the requirements of users in the context of dynamic UAV-assisted MEC network environments.

Unlike traditional methods, RLs are able to solve complex optimization problems using limited prior information from dynamic MEC environments. This is because RL-based methods can quickly adjust their behaviors to adapt to changing environments. Nevertheless, all the RLs, see [8], [9], [24], [25], [26], [27], [28], [29], [30], [31], [32], are single-objective RLs (SORLs), which first convert multiple objectives into a single objective via linear scalarization, and then design a corresponding scalar reward and optimize it. Therefore, these SORLs have limitations to the situation in which the preferences assigned to each objective, are predetermined and remain constant throughout the learning process. That is to say, an SORL solely learns the optimal policy over a given preference after a run. In most cases, however, the preferences between objectives cannot be predetermined and may vary over time, especially when the UAVâs battery level decreases or increases rapidly. For example, when a UAV operates with low battery levels, end-users may prioritize the reduction of energy consumption. On the contrary, when UAVs possess ample energy reserves, they may concentrate on maximizing the number of collected tasks. Therefore, we have to re-execute SORL algorithms over new preferences, which may be time-consuming. As an emerging MOO algorithm, MORLs with dynamic preference settings can adapt to varying preferences by learning weight-dependent multi-objective Q-value vectors [34]. This allows for more efficient adaptation to changing preferences without the need for extensive re-training. This motivates us to adapt MORL to the ETWC problem.

Table I shows a comprehensive comparison between the related works and ours in terms of system modeling and optimization technique. It can be seen that the energy source comes from the HAP in our UAV-assisted MEC system. Moreover, we adopt MORL to handle the modeled multi-objective optimization problem.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

As illustrated in Fig. 1, we study a collaborative MEC system including an HAP and a UAV, which cooperate with each other to provide energy supply and computing services to a set of GSDs, denoted as $\mathcal { M } = \{ 1 , . . . , M \}$ . These GSDs are randomly = 1distributed within a rectangular region and they can generate computation tasks over time. It is assumed that ground-based cellular communication infrastructures are unavailable for GSDs, such as remote areas or disaster areas. This paper adopts the rotary-wing UAV to provide the energy supply and computing service for GSDs because this kind of UAV can maintain close proximity to the GSDs at a low height. The HAP floats in the stratosphere in a quasi-static manner and its floating height is fixed. The UAV can transmit its energy to GSDs, enabling them to sustainably implement specific tasks, such as environmental monitoring. Equipped with a high-power laser beam, the HAP can wirelessly charge the UAV, thus maintaining its flight missions. A discrete-time system is considered in this paper and let Ï denote the time duration in each time slot. Assume the whole flight mission (i.e., a task collection and energy transmission period) has T time slots, denoted by set $\mathcal { T } = \{ 1 , . . . , T \}$ . We suppose that the UAV flies at a constant = 1speed. Table II summarizes the main notations used in system model and reinforcement learning.

<!-- image-->  
â--Task collectionâ--Energy transmissionâ--Flight trajectory  
Fig. 1. UAV-assisted MEC system.

## A. Task Model

In general, a computation task can be represented as a twotuple $\langle \mathcal { T } , \mathcal { C } \rangle$ , where I and C indicate the input data size and computation intensity of the task, respectively. Note that C can reveal how many CPU cycles are required to handle one bit input data. Similar to [2], [35], the arrival of computation tasks in GSD is modeled as a sequence of independent identically distributed Bernoulli stochastic processes. Let $\xi ^ { m } \in [ 0 , 1 ]$ denote [0 1]the parameter of the Bernoulli stochastic process corresponding to GSD m. The parameters for different GSDs may be different because of their heterogeneity. For example, a video monitoring device has a quicker data generation rate than a temperature monitoring device. Let $I _ { t } ^ { m }$ represent whether a computation task is generated by GSD m in time slot t. If the GSD generates a computation task in $t , I _ { t } ^ { m } = 1$ , and $I _ { t } ^ { m } = 0$ , otherwise. A = 1 = 0generated computation task by a GSD can be saved in its task queue. We denote by $\Upsilon _ { t } ^ { m }$ the number of computation tasks in Î¥the queue of GSD m in t, and it is updated by

$$
\Upsilon _ { t + 1 } ^ { m } = \operatorname* { m i n } \{ \Upsilon _ { t } ^ { m } + I _ { t } ^ { m } , \Upsilon _ { \operatorname* { m a x } } \} , \forall t \in \mathcal { T } , m \in \mathcal { M } ,\tag{1}
$$

where $\Upsilon _ { \mathrm { m a x } }$ represents the task queue capacity that limits the Î¥maximum number of tasks that GSD m can store in its task queue. We suppose the task queue capacity is the same for all GSDs. It is worth noting that if the task queue reaches its maximum capacity, newly arrived tasks may overwrite older tasks or be dropped altogether. Consequently, ensuring the timely upload of computation tasks from GSDs to the UAV becomes crucial. Since variations in the number of tasks stored and task generation rates across different devices, their priorities for uploading tasks differ among them. We define the task upload priority $\rho _ { t } ^ { m }$ of GSD m as

MAIN NOTATIONS USED IN SYSTEM MODEL AND REINFORCEMENT LEARNING  
TABLE II
<table><tr><td>Notation</td><td>Definition</td></tr><tr><td colspan="2">Notationusedin system model</td></tr><tr><td> $\overline { { A } }$   $\mathcal { C }$ </td><td>Collectionmirrorarea</td></tr><tr><td></td><td>Computation intensity of a task</td></tr><tr><td> $C ^ { \mathrm { U } }$ </td><td>Energy conversion efficiency of the UAV</td></tr><tr><td> $D$ </td><td>Initial laser beam size</td></tr><tr><td> $E _ { \mathrm { m a x } } ^ { \mathrm { U } }$ </td><td>Maximum battery capacity of the UAV</td></tr><tr><td> $E _ { \mathrm { t o t a l } }$ </td><td>Total energy efficiency of the UAV</td></tr><tr><td> $f ^ { \mathrm { U } }$ </td><td>Computing capability of the UAV</td></tr><tr><td> $g _ { 0 }$ </td><td>Channel power gain</td></tr><tr><td> $\mathcal { T }$ </td><td>Input data size of a task</td></tr><tr><td> $m$ </td><td>The m-th GSD</td></tr><tr><td> $M$ </td><td>Number of GSDs</td></tr><tr><td> $\mathcal { M }$ </td><td>Set of GSDs</td></tr><tr><td> $N _ { \mathrm { m a x } }$ </td><td>Maximum task number the UAV can store</td></tr><tr><td> $N _ { \mathrm { t o t a l } }$ </td><td>Total number of collected tasks</td></tr><tr><td> $P ^ { \mathrm { H } }$ </td><td>Laser transmission power of the HAP</td></tr><tr><td> $P ^ { \mathrm { U } }$ </td><td>Energy transmission power of the UAV</td></tr><tr><td> $R _ { \mathrm { m a x } }$ </td><td>Maximal horizontal coverage of the UAV</td></tr><tr><td> $t$ </td><td>The t-th time slot</td></tr><tr><td> $T$ </td><td>Number of time slots</td></tr><tr><td> $\tau$ </td><td>Set of time slots</td></tr><tr><td> $\mathcal { X }$ </td><td>Combined optical efficiency</td></tr><tr><td> $\eta$ </td><td>Attenuation coefficient</td></tr><tr><td> $\vartheta$ </td><td>Angular spread of laser beam</td></tr><tr><td> $\theta _ { \mathrm { m a x } }$ </td><td>Maximal azimuth angle</td></tr><tr><td> $\xi ^ { m }$ </td><td>Parameter of Bernoulli stochastic process for GSD m</td></tr><tr><td> $\rho _ { t } ^ { m }$ </td><td>Taskupload priority of GSD m in time slot t</td></tr><tr><td></td><td>Notation used in reinforcement learning</td></tr><tr><td> $a$  Action</td><td></td></tr><tr><td> $\boldsymbol { A }$ </td><td>Action space</td></tr><tr><td> $_ { \it B }$ </td><td>Experience replay buffer</td></tr><tr><td> $n$ </td><td></td></tr><tr><td>Nx</td><td>Number of objectives</td></tr><tr><td> $\mathbf { Q } _ { \pi }$ </td><td>Maximum number of episodes</td></tr><tr><td> $\mathbf { r } _ { t }$ </td><td>Multi-objective Q-value vector</td></tr><tr><td> $s$ </td><td>Vectorial reward at time step t State</td></tr><tr><td> $s$ </td><td>State space</td></tr><tr><td> $\gamma$ </td><td>Discount factor</td></tr><tr><td> $\psi$ </td><td>Balance weight</td></tr><tr><td></td><td></td></tr><tr><td> $\Omega$ </td><td>Preference space</td></tr></table>

$$
\boldsymbol { \rho } _ { t } ^ { m } = \xi ^ { m } \frac { \Upsilon _ { t } ^ { m } } { \Upsilon _ { \operatorname* { m a x } } } , \forall t \in \mathcal { T } , m \in \mathcal { M } .\tag{2}
$$

The task upload priority of a GSD is influenced not only by the ratio of the number of tasks generated by the GSD to the queue capacity but also by the task generation rate.

## B. Energy Harvesting Model and Computing Model

Similar to previous studies [2], [8], the Cartesian coordinate system is adopted to model the locations of the HAP, UAV, and GSDs. We assume that the locations of GSDs are static. Let $\mathbf { c } ^ { m } = ( x ^ { m } , y ^ { m } , 0 )$ be the coordinate of GSD $m \in { \mathcal { M } }$ . The UAV = ( 0)cruises with planned trajectories at a constant speed and its flight height U is fixed, where U is a positive constant. Let $\mathbf { c } _ { t } ^ { \mathbf { U } } =$ $( x _ { t } ^ { \mathrm { U } } , y _ { t } ^ { \mathrm { U } } , U )$ =indicate the coordinate of the UAV in time slot t and it may change over time. The HAP can be aware of the UAVâs movement and adjust its laser beam accordingly. Let $\mathbf { c } ^ { \mathrm { H } } = ( x ^ { \mathrm { H } } , y ^ { \mathrm { H } } , H )$ denote the coordinate of the HAP, where H = ( )is the floating height.

Let $P ^ { \mathrm { H } }$ indicate the HAPâs laser transmission power. The HAP employs the fixed transmission power to wirelessly charge the UAV. According to [9], [11], the energy harvested by the UAV from the HAP can be obtained by

$$
E _ { t } ^ { \mathrm { H } } = { C ^ { \mathrm { U } } \tau P ^ { \mathrm { H } } } \frac { A \mathcal { X } e ^ { - \eta d _ { t } ^ { \mathrm { H U } } } } { \left( D + \vartheta d _ { t } ^ { \mathrm { H U } } \right) ^ { 2 } } , \forall t \in \mathcal { T } ,\tag{3}
$$

where $C ^ { \mathrm { U } } \in ( 0 , 1 )$ denotes the UAVâs energy conversion ef-(0 1)ficiency, Ï denotes the time duration in each time slot, A is the collection mirror area of laser beam, X is the combined optical efficiency, Î· is the attenuation coefficient, D is the initial laser beam size, and Ï is the angular spread of laser beam. $d _ { t } ^ { \mathrm { H U } } = \lVert \mathbf { c } ^ { \mathrm { H } } - \mathbf { c } ^ { \mathrm { U } } \rVert _ { 2 }$ is the distance between the HAP and UAV, =where $\| \cdot \| _ { 2 }$ denotes the euclidean 2-norm. According to (3), $E _ { t } ^ { \mathrm { H } }$ mainly relies on Ï and $d _ { t } ^ { \mathrm { H U } }$ under other parameter values are kept constant.

The UAV harvests laser energy from the HAP and transmits the harvested energy to GSDs while it collects computation tasks from a specific GSD. Note that the ranges of the energy transmission and task collection are limited because the UAV owns limited communication coverage. Thus, the UAV can only transmit energy and collect tasks within its communication coverage. This depends on its maximal azimuth angle $\theta _ { \mathrm { m a x } }$ and fixed flight height U. Let $\mathcal { M } _ { t } ^ { \mathrm { C } }$ denote the set of GSDs covered, which is obtained by

$$
\mathcal { M } _ { t } ^ { \mathrm { C } } = \{ m \vert d _ { t } ^ { m } \leq R _ { \mathrm { m a x } } \} , \forall t \in \mathcal { T } , m \in \mathcal { M } ,\tag{4}
$$

where $d _ { t } ^ { m } = \sqrt { ( x _ { t } ^ { \mathrm { U } } - x ^ { m } ) ^ { 2 } + ( y _ { t } ^ { \mathrm { U } } - y ^ { m } ) ^ { 2 } }$ denotes the hori-= ( ) + ( )zontal distance between the UAV and GSD m. $R _ { \mathrm { m a x } } = U$ $\tan ( \theta _ { \mathrm { m a x } } )$ =is the maximal horizontal coverage of the UAV. The tan( )UAV selects a GSD as the specific device for task collection. In time slot t, the specific GSD, denoted by $\tilde { m } _ { t }$ , has largest task upload priority, i.e., $\tilde { m } _ { t } = \arg \operatorname* { m a x } _ { m \in \mathcal { M } _ { t } ^ { \mathrm { C } } } \rho _ { t } ^ { m }$ , where $\rho _ { t } ^ { m }$ is the Ë = arg maxtask upload priority of GSD m in t.

We consider the practical air-to-ground channel model, which combines line-of-sight (LoS) and non-line-of-sight (NLoS) links [8]. LoS signifies the propagation of signals in a direct trajectory from transmitters to receivers, without substantial impediments or reflective occurrences. Conversely, NLoS denotes the necessity for signals to reach receivers through reflections or scattering, often involving obstacles or multiple reflections. The path loss between the UAV and GSD m in t with respect to LoS and NLoS is defined as

$$
\Gamma _ { t } ^ { m } = \left\{ \begin{array} { l l } { { g _ { 0 } ( d _ { t } ^ { m } ) ^ { - \alpha } , } } & { { \mathrm { L o S ~ l i n k } } } \\ { { \eta ^ { \mathrm { N L o S } } g _ { 0 } ( d _ { t } ^ { m } ) ^ { - \alpha } , } } & { { \mathrm { N L o S ~ l i n k } } } \end{array} \right.\tag{5}
$$

where $g _ { 0 }$ is the channel power gain for 1 m reference distance, Î± represents the path loss exponent, and $\eta ^ { \mathrm { N L o S } }$ indicates the additional attenuation coefficients of NLoS link. The LoS probability of GSD m in t is calculated as

$$
P L _ { t } ^ { m } = \frac { 1 } { 1 + c _ { 1 } \cdot e ^ { c _ { 2 } \theta _ { t } ^ { m } - c _ { 1 } } } ,\tag{6}
$$

where $c _ { 1 }$ and $c _ { 2 }$ are two constants that rely on the carrier frequency and environmental conditions. $\begin{array} { r } { \theta _ { t } ^ { m } \dot { = } \frac { 1 8 0 } { \pi } \sin ^ { - 1 } ( U / d _ { t } ^ { m } ) } \end{array}$ = sin ( )is the elevation angle of the UAV and GSD m in degree. $P L _ { t } ^ { m }$ is influenced by the environmental conditions and distance between the UAV and GSD m. Suppose that the uplink and downlink channels exhibit approximate equality. Thus, the channel power gain between the UAV and GSD m in t can be defined as

$$
g _ { t } ^ { m } = ( P L _ { t } ^ { m } + \eta ^ { \mathrm { N L o S } } P N _ { t } ^ { m } ) g _ { 0 } ( d _ { t } ^ { m } ) ^ { - \alpha } ,\tag{7}
$$

where $P N _ { t } ^ { m } = 1 - P L _ { t } ^ { m }$ is the NLoS probability. Based on (7), = 1the signal-to-noise ratio (SNR) between the UAV and GSD m in t is defined as

$$
\Psi _ { t } ^ { m } = \frac { P ^ { \mathrm { G } } \cdot g _ { t } ^ { m } } { \sigma ^ { 2 } } ,\tag{8}
$$

where $P ^ { \mathrm { G } }$ and $\sigma ^ { 2 }$ are the uploading power of GSD and noise power, respectively. The communication outage may arise because there are obstacles at a low altitude. Therefore, $\Psi _ { t } ^ { m }$ is not less than the required threshold SNR $\Psi _ { \mathrm { t h } }$ Î¨for establishing Î¨successful wireless connectivity. At the end of t, the UAV can finish its task collection process. Consider the communication outage, the number of collected tasks, $N _ { t } ^ { \mathrm { C } }$ , is obtained by

$$
N _ { t } ^ { \mathrm { C } } = \left\{ \begin{array} { l l } { \Upsilon _ { t } ^ { \tilde { m } _ { t } } , } & { \quad \mathrm { i f ~ } \Psi _ { t } ^ { m } \geq \Psi _ { \mathrm { t h } } } \\ { 0 , } & { \quad \mathrm { o t h e r w i s e } } \end{array} \right.\tag{9}
$$

Let $P ^ { \mathrm { U } }$ indicate the energy transmission power of the UAV for transmitting radio frequency signals to GSDs. The energy harvested at GSD $m \in { \mathcal { M } } _ { t } ^ { \mathrm { C } } \backslash \{ \tilde { m } _ { t } \}$ from the UAV in t can be expressed as [9]

$$
E _ { t } ^ { m } = C ^ { \mathrm { G } } \tau P ^ { \mathrm { U } } g _ { t } ^ { m } , \forall t \in \mathcal { T } , m \in \mathcal { M } _ { t } ^ { \mathrm { C } } \backslash \{ \tilde { m } _ { t } \} ,\tag{10}
$$

where $C ^ { \mathrm { G } }$ is the energy conversion efficiency of GSD. The total energy for the UAV transmitting energy to GSDs in t is obtained by

$$
E _ { t } ^ { \mathrm { T r } } = \sum _ { m \in \mathcal { M } _ { t } ^ { \mathrm { C } } \backslash \{ \tilde { m } _ { t } \} } E _ { t } ^ { m } , \forall t \in \mathcal { T } .\tag{11}
$$

We consider that the UAV keeps a computing queue in order to store the collected tasks, which are awaiting for further handling. It should note that task collection delay and associated energy consumption can be neglected because the UAV can sufficiently close GSDs. The UAV can only store the specified number of computation tasks due to its limited storage capacity, denoted by $N _ { \mathrm { m a x } }$ . In each time slot, the UAV has to execute the unfinished tasks stored in the computing queue. Let $N _ { t } ^ { \mathrm { U } }$ denote the number of unfinished tasks in the queue, and its value is an integer limited between 0 and $N _ { \mathrm { m a x } }$ . Within a time slot, the UAV can only process a fixed number of computation tasks because of its limited computing capability, denoted by $f ^ { \mathrm { U } }$ . Thus, the number of tasks executed by the UAV within a time slot can be obtained by $\{ N _ { t } ^ { \mathrm { U } } , \varphi \}$ , where $\varphi = \lfloor \tau f ^ { \mathrm { U } } / \mathbb { Z } \mathcal { C } \rfloor$ is maximum number of min =tasks the UAV can process in each time slot. Based on $N _ { t } ^ { \mathrm { U } }$ and $\varphi ,$ the computing queue is updated, and the number of queuing tasks, $N _ { t } ^ { \mathrm { Q } }$ , can be calculated by

$$
N _ { t } ^ { \mathrm { Q } } = \operatorname* { m a x } \{ N _ { t } ^ { \mathrm { U } } - \varphi , 0 \} , \forall t \in \mathcal { T } .\tag{12}
$$

At the end of t, the UAV can finish its task collection procedure. By employing (9) and (12), we update the number of unfinished tasks in $t + 1 , N _ { t + 1 } ^ { \mathrm { U } }$ , expressed as

$$
N _ { t + 1 } ^ { \mathrm { U } } = \operatorname* { m i n } \{ N _ { t } ^ { \mathrm { C } } + N _ { t } ^ { \mathrm { Q } } , N _ { \operatorname* { m a x } } \} , \ \forall t \in \mathcal { T } .\tag{13}
$$

The energy consumption of the UAV for executing min $\{ N _ { t } ^ { \mathrm { U } } , \varphi \}$ computation tasks is calculated as

$$
E _ { t } ^ { \mathrm { P } } = \kappa \cdot \operatorname* { m i n } \{ N _ { t } ^ { \mathrm { U } } , \varphi \} \mathcal { T } \mathcal { C } \cdot ( f ^ { \mathrm { U } } ) ^ { 2 } , \forall t \in \mathcal { T } ,\tag{14}
$$

where Îº denotes the effective capacitance coefficient.

## C. Problem Formulation

In each time slot, the UAV harvests the laser energy from the HAP and transmits the harvested energy to GSDs (except the specific device) within its coverage. Meanwhile, the UAV is in charge of gathering computation tasks from the specific GSD and processing them. Hence, the UAVâs energy consumption encompasses both the energy consumed for transmitting to GSDs and energy consumed for processing collected tasks. Let $E _ { t } ^ { \mathrm { T r } }$ and $E _ { t } ^ { \mathrm { P } }$ denote the transmitting energy consumption and processing energy consumption, respectively. Let $E _ { t } ^ { \mathrm { U } }$ denote the energy level of the UAV at the beginning of t, and it is updated by

$$
\begin{array} { r } { E _ { t + 1 } ^ { \mathrm { U } } \mathrm { { = } } \operatorname* { m i n } \{ E _ { \mathrm { m a x } } ^ { \mathrm { U } } , \operatorname* { m a x } \{ 0 , E _ { t } ^ { \mathrm { U } } + E _ { t } ^ { \mathrm { H } } - E _ { t } ^ { \mathrm { { T r } } } - E _ { t } ^ { \mathrm { P } } \} \} , \ \forall t \in { \mathcal { T } } , } \end{array}\tag{15}
$$

where $E _ { \mathrm { m a x } } ^ { \mathrm { U } }$ is the maximum battery capacity of the UAV. The total energy efficiency of the UAV is defined as

$$
E _ { \mathrm { t o t a l } } = \sum _ { t = 1 } ^ { T } E _ { t } ^ { \mathrm { U } } .\tag{16}
$$

On the basis of (9), the total number of computation tasks collected by the UAV during time duration $T$ can be calculated by

$$
N _ { \mathrm { t o t a l } } = \sum _ { t = 1 } ^ { T } N _ { t } ^ { \mathrm { C } } .\tag{17}
$$

Let $\mathbf { C } = \{ \mathbf { c } _ { t } ^ { \mathrm { U } } | \forall t \in \mathcal { T } \}$ represent the set of the UAVâs coordi-=nates during T time slots. We formulate the ETWC problem as an MOO problem, with $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ maximized simultaneously, via optimizing the UAVâs flight trajectories in each time slot, as follows.

$$
\operatorname* { m a x } _ { \mathbf { C } } ( E _ { \mathrm { t o t a l } } , N _ { \mathrm { t o t a l } } )\tag{18}
$$

subject to:

$$
\begin{array} { r l r } & { \mathrm { C 1 : ~ } 0 \leq x _ { t } ^ { \mathrm { U } } \leq x _ { \operatorname* { m a x } } , } & { \quad \forall t \in \mathcal { T } , } \\ & { \mathrm { C 2 : ~ } 0 \leq y _ { t } ^ { \mathrm { U } } \leq y _ { \operatorname* { m a x } } , } & { \quad \forall t \in \mathcal { T } , } \\ & { \mathrm { C 3 : ~ } E _ { t } ^ { \mathrm { U } } \leq E _ { \operatorname* { m a x } } ^ { \mathrm { U } } , } & { \quad \forall t \in \mathcal { T } , } \\ & { \mathrm { C 4 : ~ } d _ { t } ^ { m } \leq R _ { \operatorname* { m a x } } , } & { \quad \forall m \in \mathcal { M } _ { t } ^ { \mathrm { C } } , t \in \mathcal { T } . } \end{array}
$$

C1 and C2 together show the UAVâs flight region. C3 restricts that the UAVâs energy level is not exceeding its maximum battery capacity. C4 denotes that the UAV can only transmit the harvested energy to GSDs and collects computation tasks from them within its communication coverage. One can understand that to maximize $N _ { \mathrm { t o t a l } } .$ , the UAV should follow a suitable trajectory during its flight mission, so as to it can seek the specific GSD and gather its tasks. However, as the number of collected tasks increases, the UAVâs energy efficiency decreases correspondingly. This is because the UAV needs to handle more computation tasks collected by it. Thus, it is easily understood that two objectives, i.e., maximization of $E _ { \mathrm { t o t a l } }$ and maximization of $N _ { \mathrm { t o t a l } }$ , are inherently conflicting with each other.

## IV. OVERVIEW OF MOMDP

An MOMDP [34] is normally represented by a five-tuple $\langle S , \mathcal { A } , \mathbf { r } , \Omega , f \rangle$ , where S is the state space consisting of possible Î©states in which the environment can be. A is the action space that is the set of actions the agent can take. $\mathbf { r } ( s , a )$ is the vectorial ( )reward function used to evaluate the performance of action a taken by the agent in state s.  is the preference space adopted to simulate various preferences between objectives. $f _ { \mathbf { w } } ( \mathbf { r } ( s , a ) )$ ( ( ))is the scalarization function that can generate a scalar user utility using preference $\mathbf { w } \in \Omega$ . This paper focuses on the linear Î©scalarization function, which aggregates $\mathbf { r } ( s , a )$ into a scalar reward using weighted sum, i.e., $f _ { \mathbf { w } } ( \mathbf { r } ( s , a ) ) = \mathbf { w } \cdot \mathbf { r } ( s , a )$ . It is ( ( )) = ( )seen that if w is held constant at a specific value, the MOMDP simplifies into a single-objective MDP.

A policy Ï is a state-to-action mapping, i.e., $\pi : { \mathcal { S } }  A$ :Through interacting with the environment, an agent gathers information and acquires knowledge to learn an optimal policy that maximizes the expected cumulative reward. The action-value function is the vector of the expected return, which can be described as

$$
\begin{array} { r l } & { \mathbf { Q } _ { \pi } ( s , a ) = \mathbb { E } _ { \pi } \left[ \mathbf { R } _ { t } | s _ { t } = s , a _ { t } = a \right] } \\ & { \quad \quad = \mathbb { E } _ { \pi } \left[ \displaystyle \sum _ { k = t } ^ { T } \gamma ^ { k - t } \cdot \mathbf { r } _ { k } \bigg | s _ { t } = s , a _ { t } = a \right] , } \end{array}\tag{19}
$$

where $\mathbf { R } _ { t }$ represents the cumulative discounted reward at time step $t ; \gamma \in [ 0 , 1 ]$ is the discount factor; $\mathbf { r } _ { k } = ( r _ { k } ^ { 1 } , . . . , r _ { k } ^ { n } )$ in-[0 1] = ( )dicates the immediate vectorial reward received at time step k, where n is the number of objectives. Since each element in $\mathbf { r } _ { k }$ is associated with an individual objective, $\mathbf { Q } _ { \pi } ( s , a )$ is a ( )multi-objective Q-value (MOQ) vector with n elements. For the ETWC problem, we have $n = 2$ , namely, $r _ { k } ^ { 1 }$ and $r _ { k } ^ { 2 }$ are associated with $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } } .$ = 2, respectively.

## V. THE PROPOSED ALGORITHM

## A. MOMDP Model

To tackle the ETWC problem using an MORL algorithm, it is imperative to establish a dedicated MOMDP model tailored to the problem at hand. This involves systematically defining the state space, action space, and reward function.

1) State Space: A state space is the set of possible states in which the UAV-assisted MEC environment can be. It is assumed that the UAV can only observe its own coordinate position cUt , $\mathbf { c } _ { t } ^ { \mathrm { { U } } }$ the number of unfinished tasks $N _ { t } ^ { \mathrm { U } }$ , the number of collected tasks $N _ { t } ^ { \mathrm { C } }$ , and energy level $E _ { t } ^ { \mathrm { U } }$ , in time slot t. To be specific, the state space is defined as

$$
\begin{array} { r } {  { \boldsymbol { S } } = \{ s _ { t } | s _ { t } = (  { \mathbf { c } } _ { t } ^ { \mathrm { U } } , N _ { t } ^ { \mathrm { U } } , N _ { t } ^ { \mathrm { C } } , E _ { t } ^ { \mathrm { U } } ) , \forall t \in  { \mathcal { T } } \} , } \end{array}\tag{20}
$$

where $s _ { t }$ is the MEC system environment state in t.

2) Action Space: We assume that the UAV can select one of four directions to move at its current location in each time slot. Thus, the action space can be defined as

$$
\begin{array} { r } { \mathcal { A } = \{ a _ { t } | a _ { t } \in \{ N , S , E , W \} , \forall t \in \mathcal { T } \} , } \end{array}\tag{21}
$$

where $a _ { t }$ is an action the UAV takes in state $s _ { t } .$ . Actions N , S, E, and $W$ represent that the UAV moves to the north, south, east, and west from the current location, respectively.

3) Reward Function: The ETWC problem aims to maximize $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ simultaneously. As a result, after the agent executes action $a _ { t }$ , we can define the vectorial reward received by it as

$$
\begin{array} { r } { \mathbf { r } _ { t } = ( r _ { t } ^ { \mathrm { E } } , r _ { t } ^ { \mathrm { N } } ) = \left\{ \begin{array} { l l } { \left( \frac { E _ { t } ^ { \mathrm { U } } } { 1 0 } , N _ { t } ^ { \mathrm { C } } \right) , } & { \mathrm { i f } ~ \mathbb { 1 } _ { t } = 0 } \\ { \left( \delta _ { 1 } \frac { E _ { t } ^ { \mathrm { U } } } { 1 0 } , \delta _ { 2 } N _ { t } ^ { \mathrm { C } } \right) , } & { \mathrm { i f } ~ \mathbb { 1 } _ { t } = 1 } \end{array} \right. } \end{array}\tag{22}
$$

where $r _ { t } ^ { \mathrm { E } }$ and $r _ { t } ^ { \mathrm { N } }$ denote the two scalar rewards that are associated with $E _ { t } ^ { \cup }$ and $N _ { t } ^ { \mathrm { C } }$ , respectively. Coefficient $\textstyle { \frac { 1 } { 1 0 } }$ ensures that $r _ { t } ^ { \mathrm { E } }$ and $r _ { t } ^ { \mathrm { N } }$ have the same order of magnitude. This can enable the simultaneous optimization of two objectives without introducing any biases, thus achieving a good balance between them. An indicator variable, 1t can be one if the UAV moves outside of the restricted region in $t ;$ otherwise, $\mathbb { 1 } _ { t } = 0$ . Based on the variable, one can punish the two scalar rewards, $\frac { E _ { t } ^ { \mathrm { U } } } { 1 0 }$ and $N _ { t } ^ { \mathrm { C } }$ when $\mathbb { 1 } _ { t } = 1$ As a result, the penalty coefficients $\delta _ { 1 }$ and $\delta _ { 2 }$ = 1are adopted to decrease $\frac { E _ { t } ^ { \mathrm { U } } } { 1 0 }$ and $N _ { t } ^ { \mathrm { C } }$ , respectively.

Lemma 1: The maximization of the expected vectorial return E $[ \mathbf { R } _ { 1 } ]$ is equal to the simultaneous maximization of $E _ { t o t a l }$ and $N _ { t o t a l } .$

Proof 1: Based on the reward $\mathbf { r } _ { t } = ( r _ { t } ^ { E } , r _ { t } ^ { N } )$ defined in (22), we can obtain the vector of cumulative discount rewards received by the agent during T time slots. It is also known as the vectorial return, ${ \bf R } _ { 1 } = ( R _ { 1 } ^ { E } , R _ { 1 } ^ { N } )$ , which is calculated as

$$
R _ { 1 } ^ { \mathrm { E } } = \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } r _ { t } ^ { \mathrm { E } } = \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } ( 1 - \mathbb { 1 } _ { t } + \delta _ { 1 } \mathbb { 1 } _ { t } ) \frac { E _ { t } ^ { \mathrm { U } } } { 1 0 } ,\tag{23}
$$

$$
R _ { 1 } ^ { \mathrm { { N } } } = \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } r _ { t } ^ { \mathrm { { N } } } = \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } ( 1 - \mathbb { 1 } _ { t } + \delta _ { 2 } \mathbb { 1 } _ { t } ) N _ { t } ^ { \mathrm { { C } } } .\tag{24}
$$

According to $( I 6 ) , ( I 7 ) , ( 2 3 )$ , and (24), the maximization of the expected vectorial return $\mathbb { E } [ \mathbf { R } _ { 1 } ]$ is equal to the simultaneous maximization of $E _ { t o t a l }$ and $N _ { t o t a l } .$

## B. MORL-TER Algorithm

MORLs have attracted increasingly more research attention [34], [36], [37], [38], [39]. Unlike SORL with a scalar reward, MORL has a vectorial reward in which each element corresponds to a specific objective. Through learning weightdependent MOQ vectors, envelope multi-objective Q-learning (EMOQL) has great potential to deal with MEC scenarios with dynamic preferences [34]. This algorithm has demonstrated successful applications across diverse domains, including machine control, task offloading [39], and dialog systems [34]. This motivates us to adapt the EMOQL algorithm to the ETWC problem concerned in the paper.

Algorithm 1: MORL-TER for the ETWC Problem.   
Input: maximum number of episodes $N _ { \mathrm { m a x } } ^ { \mathrm { e p s } }$ , discount factor $\gamma ,$   
balance weight $\psi ,$ greedy exploration Îµ.   
1: Initialize the preference space Î© by the systematic method;   
2: Initialize policy MOQ network $\mathbf { Q } ( s , a , \mathbf { w } ; \theta )$ with parameters   
$\theta ;$   
3: Initialize target MOQ network $\bar { \mathbf { Q } } ( s , a , \mathbf { w } ; \bar { \theta } )$ with $\bar { \theta } = \theta ;$   
4: Set the experience replay buffer $B = \varnothing ;$   
5: for $k = 1 , . . . . , N _ { \mathrm { m a x } } ^ { \mathrm { e p s } }$ do   
6: Sample a preference ${ \bf w } _ { k }$ from Î©;   
7: Set the trace $\Gamma _ { k } = \varnothing ;$   
8: for $t = 1 , . . . , T$ do   
9: Observe current state $s _ { t } ;$   
10: Choose action $a _ { t }$ using (25);   
11: Take action $a _ { t }$ and move the UAV to the next location;   
12: Receive reward $\mathbf { r } _ { t }$ and observe next state $s _ { t + 1 } ;$   
13: Store transition $\left( { { s _ { t } } , { a _ { t } } , { \bf { r } } _ { t } , { s _ { t + 1 } } } \right)$ in $\Gamma _ { k } ;$   
14: if B is full then   
15: Sample $N _ { \mathrm { t r a } }$ transitions from B, denoted by $\mathcal { D } ;$   
16: Sample $N _ { \mathbf { w } }$ preferences from Î©, denoted by $\mathcal { W } ;$   
17: for each transition $( s _ { j } , a _ { j } , \mathbf { r } _ { j } , s _ { j + 1 } ) \in \mathcal { D }$ do   
18: Calculate Loss1(Î¸) and Loss2(Î¸) using (26)   
and (28), respectively;   
19: Perform gradient descent step on (29) to update   
the policy MOQ network;   
20: end for   
21: end if   
22: Every $\bar { N }$ time steps, synchronize target MOQ network,   
i.e., $\bar { \theta } = \theta ;$   
23: Update Ï and Îµ;   
24: end for   
25: Update B based on $\Gamma _ { k }$ by TER $\scriptstyle ( B , \Gamma _ { k } , \gamma ) ;$   
26: end for   
Output: the policy MOQ network $\mathbf { Q } ( s , a , \mathbf { w } ; \theta ) .$

The framework of the proposed MORL-TER, as depicted in Fig. 2, comprises two components: the agent and MEC system environment. The agent can be typically deployed on the UAV and engages in interactive exchanges with the environment. It encompasses both the execution and training stages. In the agent, there are two different MOQ networks (i.e., policy and target MOQ networks), and their architectures are the same. The policy MOQ network is used to choose the actions. The target MOQ network is adopted to avoid overestimation of MOQ values. Note that the policy MOQ network in the execution stage is exactly the same as the one in the training phase for the purpose of presentation. In the execution stage, we use the policy MOQ network to select actions, i.e., the UAVâs flight directions. In the training stage, the multiple transitions are randomly sampled to train the policy MOQ network.

Throughout the execution stage, the agent continually interacts with the environment, enabling it to observe the MEC systemâs states and subsequently make decisions to the movement of the UAV. The architecture of the policy MOQ network is illustrated in Fig. 3, which is a fully connected neural network with L layers. The policy MOQ network first concatenates the observed state $s _ { t } \in S$ and sampled preference w $\in \Omega$ . Before inputting the network, the concatenated results should be normalized because of different dimensionality. Then, the normalized outcomes are fed into the policy MOQ network and it outputs $| { \mathcal { A } } | \times n$ Q-values. Finally, these Q-values are reshaped into a $| { \mathcal { A } } | \times n$ matrix in which each row is associated with a multiobjective Q-value vector with n components. To adopt conventional action choice methods, for instance, Îµ-greedy exploration, an action $a _ { t } \in \mathcal A$ is chosen based on left multiplying the matrix by w. The agent executes $a _ { t }$ to transition the UAV from its current location to the next location based on the observation of the next state $s _ { t + 1 }$ . Meanwhile, it obtains a vectorial reward $\mathbf { r } _ { t }$ from the environment. In the training stage, a mini-batch of transitions and multiple preferences are first sampled from the experience buffer and preference space, respectively. Then, the agent adopts these sampled transitions and preferences to train its policy MOQ network, thereby generalizing various preferences.

<!-- image-->  
Fig. 2. Framework of MORL-TER.

<!-- image-->  
Fig. 3. Network architecture.

The pseudocode of MORL-TER is illustrated in Algorithm 1, which is based on EMOQL [34], with a trace-based experience replay (TER) scheme incorporated. Similar to [40], we adopt the systematic method to produce multiple evenly distributed weight vectors (i.e., preference space), so as to mimic diverse preferences. The method has two important parameters n and $\sigma ,$ where n and Ï are the numbers of objectives and divisions. Based on the two parameters, the systematic method can generate $\Phi = { \bf C } _ { n + \sigma - 1 } ^ { n - 1 }$ uniformly distributed weight vectors, denoted by $\boldsymbol { \Omega } = \{ \mathbf { w } _ { 1 } , . . . , \mathbf { w } _ { \Phi } \}$ . For instance, we have $n = 2$ for the Î© =ETWC problem with two objectives. If $\sigma = 1 4 9$ , the systematic = 149method generates  weight vectors to represent various preferences.

We initialize the policy MOQ network using the random parameters Î¸ (step 2). The parameters of the target MOQ network are initially set to Î¸ (step 3). Once the policy MOQ network is initialized, the agent commences interaction with the environment so that it can observe current environment state $s _ { t }$ (step 9). At the beginning of each episode $k = 1 , . . . . , N _ { \mathrm { m a x } } ^ { \mathrm { e p s } }$ , a current preference $\mathbf { w } _ { k }$ is randomly sampled from , where $N _ { \mathrm { m a x } } ^ { \mathrm { e p s } }$ is the maximum number of episodes. The action $a _ { t }$ is made based on (25), i.e., the Îµ-greedy exploration.

$$
a _ { t } = { \left\{ \begin{array} { l l } { \operatorname { a r a n d o m } \operatorname { a c t i o n } \operatorname { f r o m } \ A , } & { { \mathrm { w i t h } } \operatorname { p r o b a b i l i t y } \ \varepsilon } \\ { \operatorname { a r g m a x } _ { a \in { \mathcal { A } } } \mathbf { w } _ { k } \mathbf { Q } ( s _ { t } , a , \mathbf { w } _ { k } ; \theta ) , } & { { \mathrm { w i t h } } \operatorname { p r o b a b i l i t y } \ 1 \operatorname { - } \varepsilon } \end{array} \right. }\tag{1(25}
$$

where $\varepsilon \in [ 0 , 1 ]$ denotes the probability of random exploration [0 1]and updated over time steps. The agent takes $a _ { t }$ and moves the UAV from current location to next location (step 11). Afterward, it obtains a vectorial reward $\mathbf { r } _ { t }$ from the environment and observe next state $s _ { t + 1 }$ (step 12). In step 13, the transition $\left( { { s _ { t } } , { a _ { t } } , { \bf { r } } _ { t } , { s _ { t + 1 } } } \right)$ is stored in the current trace $\Gamma _ { k }$

)If the buffer B is full, $N _ { \mathrm { t r a } }$ Îtransitions, denoted by ${ \mathcal { D } } ,$ are randomly sampled from B to train the policy MOQ network (step 15). Meanwhile, $N _ { \mathbf { w } }$ preferences, denoted by W, are randomly sampled from the preference space  (step 16). For each sampled transition $( s _ { j } , a _ { j } , \mathbf { r } _ { j } , s _ { j + 1 } ) \in \mathcal { D }$ Î©, we first calculate (the loss function Loss Î¸ , defined as

$$
L o s s 1 ( \theta ) = \mathbb { E } \left[ \| \mathbf { y } _ { j } - \mathbf { Q } ( s _ { j } , a _ { j } , \mathbf { w } _ { i } ; \theta ) \| _ { 2 } ^ { 2 } \right] , \mathbf { w } _ { i } \in \mathcal { W } ,\tag{26}
$$

where $\mathbf { y } _ { j } = \mathbf { r } _ { j }$ if $s _ { j + 1 }$ is the terminal state; otherwise, $\mathbf { y } _ { j }$ is =obtained by

$$
\mathbf { y } _ { j } = \mathbf { r } _ { j } + \gamma \bar { \mathbf { Q } } \left( s _ { j + 1 } , \ \underset { a \in \mathcal { A } , \mathbf { w } ^ { \prime } \in \mathcal { W } } { \operatorname { a r g m a x } } \ \mathbf { w } _ { i } \mathbf { Q } ( s _ { j + 1 } , a , \mathbf { w } ^ { \prime } ; \boldsymbol { \theta } ) , \mathbf { w } _ { i } ; \bar { \boldsymbol { \theta } } \right) .\tag{27}
$$

According to (27), we adopt double Q-learning to train the policy MOQ network, so as to avoid the overestimation of multi-objective Q-values. In addition, preserving the envelope $\begin{array} { r } { \operatorname * { a r g m a x } _ { a \in \mathcal { A } , \mathbf { w } ^ { \prime } \in \mathcal { W } } \mathbf { w } _ { i } \mathbf { Q } \big ( s _ { j + 1 } , a , \mathbf { w } ^ { \prime } ; \theta \big ) } \end{array}$ in our method facilitates ( ;the rapid alignment of a preference $\mathbf { w } ^ { \prime }$ with optimal policy and transitions, even those explored under different preferences. This means the sampled transitions can be well adapted to optimize the preference $\mathbf { w } ^ { \prime }$ , finding the optimal policy corresponding to $\mathbf { w } ^ { \prime }$ . In contrast, scalarized updates optimizing scalar utility lack the ability to leverage $\begin{array} { r } { \operatorname* { m a x } _ { a } { \mathbf { Q } } ( s _ { j } , a , { \mathbf { w } } _ { i } ; \theta ) } \end{array}$ information max ( ; )for updating optimal policies aligned with different preferences. Therefore, the envelope updates can have better sample efficiency.

However, in practice, directly optimizing the loss function Loss Î¸ poses significant challenges because there are a large number of discrete solutions in the optimal frontier. This makes the functionâs landscape become considerably non-smooth. Thus, an auxiliary loss function, Loss Î¸ , is used to solve the issue, and it is defined as

$$
L o s s 2 ( \theta ) = \mathbb { E } \left[ \left| \mathbf { w } _ { i } \mathbf { y } _ { j } - \mathbf { w } _ { i } \mathbf { Q } ( s _ { j } , a _ { j } , \mathbf { w } _ { i } ; \theta ) \right| \right] , \mathbf { w } _ { i } \in \mathcal { W } .\tag{28}
$$

Based on Loss Î¸ and $L o s s 2 ( \theta )$ , the final loss function 1( )Loss Î¸ can be obtained by

$$
L o s s ( \theta ) = \psi \cdot L o s s 1 ( \theta ) + ( 1 - \psi ) \cdot L o s s 2 ( \theta ) ,\tag{29}
$$

where $\psi \in ( 0 , 1 )$ is a weight coefficient adopted to obtain a balance between $L o s s 1 ( \theta )$ and $L o s s 2 ( \theta )$ . We can tardily decrease 1( ) 2( )the value of Ï from 1 to 0, to convert Loss Î¸ from $L o s s 1 ( \theta )$ to $L o s s 2 ( \theta )$ ( ) 1( ). The loss Loss Î¸ initially focuses on narrowing the 2( ) 1( )gap between the predicted Q-values and actual expected rewards.

Algorithm 2: Trace-Based Experience Replay (TER).   
Input: experience replay buffer B, trace Î, discount factor Î³.   
1: Calculate vectorial return of Î, $\begin{array} { r } { { \bf R } _ { t } = \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } { \bf r } _ { t } ; } \end{array}$   
2: if B is not full then   
3: Add Î to B;   
4: else   
5: Add Î to $\begin{array} { r } { B ; { } } \end{array}$   
6: Set $l = | \boldsymbol { B } | ;$   
7: for $i = 1 , . . . , l$ do   
8: Set $B _ { i } ^ { \mathrm { { d i s t } } } = 0 ;$   
9: end for   
// Calculate crowding distance for each trace in B   
10: for each objective n do   
11: B = sort(B, n); // sort using each scalar return   
12: $B _ { 1 } ^ { \mathrm { d i s t } } = B _ { l } ^ { \mathrm { d i s t } } = + \infty ;$   
13: for $i = 2 , . . . , l - 1$ do   
14: $B _ { i } ^ { \mathrm { d i s t } } = B _ { i } ^ { \mathrm { d i s t } } + ( B _ { i + 1 } ^ { n } - B _ { i - 1 } ^ { n } ) / ( f _ { \mathrm { m a x } } ^ { n } - f _ { \mathrm { m i n } } ^ { n } ) ;$   
15: end for   
16: end for   
17: Remove the trace with smallest crowing distance from $\begin{array} { r } { B ; { } } \end{array}$   
18: end if   
Output: experience replay buffer B.

On the other hand, the loss $L o s s 2 ( \theta )$ serves as an auxiliary force, 2( )guiding the optimization toward the direction of better utility.

The original EMOQL algorithm [34] adopts the standard first-in first-out experience replay buffer, which treats transitions as atomic units when considering them for addition in or deletion from the buffer. However, a big challenge to using the standard experience replay is that the obtained experiences by a preferenceâs optimal policy can be harmful to another preferenceâs training process. In other words, if a policy $\pi _ { \mathbf { w } }$ is exclusively trained on experiences obtained via another policy $\pi _ { \mathbf { w } ^ { \prime } } , \pi _ { \mathbf { w } }$ will typically diverge from the optimal policy for preference w.

To overcome the challenge above and enhance the optimization performance of the original EMOQL, we develop a trace-based experience replay (TER) scheme, which treats an episodeâs transitions as one trace. The TER scheme replaces standard transition-based replay with trace-based memorization. Instead of considering each transition independently, the scheme handles traces as atomic units. To grasp the underlying reasons, we examine a trace of experiences that spans from an initial state to a terminal state. In cases where there is a gap in experiences between the initial and terminal states, propagating Q-values from the terminal back to the initial state becomes challenging. This challenge arises because the learning agent must make inferences to bridge the missing link. The standard replay buffers, in their sequential addition and removal of experiences, typically do not encounter this issue. Consequently, for the majority of experiences stored in standard replay buffers, both the preceding and subsequent transitions are readily available. To avoid partial traces, the TER scheme handles traces as atomic units when considering them for addition in or deletion from the experience buffer.

The procedure of the TER scheme is shown in Algorithm 2. We first calculate the vectorial return of the trace , ${ \bf R } _ { 1 } =$ $\sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } \mathbf { r } _ { t }$ Î =. If the experience buffer B is not full, the trace is directly added to B (steps 2â4). Similar to [36], we also Îuse the crowding distance to reflect the relative diversity of a trace in B. The higher the diversity, the more important the trace. This is because those traces with high diversity, obtained by $\pi _ { \mathbf { w } ^ { \prime } }$ , are also used to train another policy $\pi _ { \mathbf { w } }$ , which can better maintain the learned optimal policy for preference w. The following describes how to update the experience buffer B based on the crowding distance of each trace in B.

When the buffer is full, the trace  is first added to B. Then, Îwe obtain the crowding distance of each trace in B (steps 10-16), where $B _ { i } ^ { \mathrm { d i s t } }$ indicates the crowding distance of the i-th trace. $B _ { i } ^ { n }$ represents the n-th scalar return of the i-th trace in B. Parameters $f _ { \mathrm { m a x } } ^ { n }$ and $f _ { \mathrm { m i n } } ^ { n }$ are the maximal and minimal values of the n-th scalar return. After that, we remove the trace with the smallest crowding distance from buffer B, which guarantees the diversity of the experience replay buffer (step 17). Thus, the TER scheme can improve sample efficiency and reduce replay buffer bias.

## C. Complexity Analysis

We analyze MORL-TERâs time complexity in terms of the training and testing stages. Compared with the training complexity of the policy MOQ network, the TER schemeâs time complexity is trivial and can be neglected. Thus, in the training stage, MORL-TERâs time complexity primarily relies on the training complexity of the policy MOQ network. In the light of Fig. 3, the policy MOQ network is comprised of an input layer, an output layer, and L fully connected layers. The number of neurons in the input layer is $n + 6$ , where n is the number of objectives. Let $\beta _ { i }$ + 6represent the number of neurons in the i-th fully connected layer, $i = 1 , . . . , L$ . The output layer has $| { \mathcal { A } } | \times n$ neurons, where $| { \mathcal { A } } | = 4$ 1is the number of actions. Note that we have $\beta _ { 0 } = n + 6$ =and $\beta _ { L + 1 } = | { \mathcal { A } } | \times n$ . MORL-TERâs time complexity is $\begin{array} { r } { O ( N _ { \mathrm { e p s } } ^ { \operatorname* { m a x } } \times T \times ( \sum _ { i = 1 } ^ { L + 1 } \beta _ { i - 1 } \times \beta _ { i } ) \times N _ { \mathrm { t r a } } ) } \end{array}$ in the training stage, where $N _ { \mathrm { e p s } } ^ { \mathrm { m a x } }$ ( ) )is the maximum number of episodes, T is the number of time slots, and $N _ { \mathrm { t r a } }$ is the number of sampled transitions.

In the testing stage, the trained policy MOQ network is employed to plan the UAVâs trajectory of each time slot by network inference. Hence, based on the number of time slots and inference time of the policy MOQ network, MORL-TERâs time complexity is $O ( T \times \bar { ( \sum _ { i = 1 } ^ { L + 1 } \beta _ { i - 1 } \times \beta _ { i } ) } )$ in the testing stage.

## VI. SIMULATION RESULT AND DISCUSSION

We examine the optimization performance of the proposed MORL-TER by conducting extensive experiments. To facilitate this evaluation, we have developed a Python-based simulator using PyTorch 1.7, which helps us to thoroughly evaluate and analyze the performance of the MORL-TER across various experimental scenarios. In the simulation, we define several important experiment parameters. Assume that the number of time slots $T$ is equal to 100. The duration of each time slot is considered as 3 seconds. Thus, we have five minutes for the UAVâs mission period. We consider a square region and its side lengths, $x _ { \mathrm { m a x } }$ and $y _ { \mathrm { m a x } }$ are both restricted to 400 m. The UAVâs flight velocity is set to 10 m/s. For a computation task, we set its

TABLE III  
SIMULATION PARAMETERS
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Valueused in systemmodel</td><td></td></tr><tr><td>Collection mirror area (A)</td><td> $\overline { { 1 0 ^ { - 2 } ~ \mathrm { m } ^ { 2 } } }$ </td></tr><tr><td>Energy conversion efficiency of GSD (CG)</td><td>0.9</td></tr><tr><td>Energy conversion efficiency of the UAV  $\grave { ( } C ^ { \mathrm { U } } )$ </td><td>0.9</td></tr><tr><td>Initial laser beam size (D)</td><td>0.1m</td></tr><tr><td>Computing capability of the UAV (fU)</td><td>1 GHz</td></tr><tr><td>Channel power gain (go)</td><td>-30 dB</td></tr><tr><td>Floating height of the HAP (H)</td><td>20 km</td></tr><tr><td>Maximum task number the UAV can store  $( N _ { \mathrm { m a x } } )$ </td><td>10</td></tr><tr><td>Laser transmission power of the HAP  $( P ^ { \mathrm { H } } )$ </td><td>2000W</td></tr><tr><td>Energy transmission power of the UAV (PU)</td><td>1W</td></tr><tr><td>Combined optical efficiency(X)</td><td>0.2</td></tr><tr><td>Attenuation coefficient (n)</td><td>10  $^ { \cdot 6 } / \mathrm { m }$ </td></tr><tr><td>Angular spread of laser beam (ð£)</td><td> $3 . 4 \times 1 0 ^ { - 5 }$ </td></tr><tr><td>Maximal azimuth angle (0max)</td><td> $\pi / 4$ </td></tr><tr><td>Effective capacitance coefficient (Îº)</td><td> $1 0 ^ { - 2 6 } \mathrm { ~ W ~ }$ </td></tr><tr><td>Value used in reinforcement learning</td><td></td></tr><tr><td>Discount factor(y)</td><td>0.995</td></tr><tr><td></td><td>32</td></tr><tr><td>Number of sampled transitions  $( N _ { \mathrm { t r a } } )$ </td><td></td></tr><tr><td>Number of sampled preferences  $\left( N _ { \mathbf { w } } \right)$  Maximumnumber of episodes  $( N _ { \mathrm { m a x } } ^ { \mathrm { e p s } } )$ </td><td>2 2000</td></tr></table>

TABLE IV

TEST INSTANCES
<table><tr><td>Instance (M,U)</td><td>Number of GSDs (M)</td><td>Flight height (U)</td></tr><tr><td>I-(60,30)</td><td>60</td><td>30</td></tr><tr><td>I-(60,50)</td><td>60</td><td>50</td></tr><tr><td>I-(100,30)</td><td>100</td><td>30</td></tr><tr><td>I-(100,50)</td><td>100</td><td>50</td></tr><tr><td>I-(140,30)</td><td>140</td><td>30</td></tr><tr><td>I-(140,50)</td><td>140</td><td>50</td></tr></table>

I and C to 5 MB and 10 cycles/bit, respectively. The parameter of Bernoulli stochastic process for each GSD is randomly determined by selecting a value from set { . , . , . }. As 0 3 0 5 0 7introduced in Section V-B, we generate 150 evenly distributed weight vectors to mimic diverse objective preferences, i.e., . Î©A promising MORL algorithm should possess the capability to generalize across  while effectively adapting to changing Î©preferences. The policy MOQ network has a two-layer fullconnected neural network. Each layer of the network includes 64 neurons, utilizing rectified linear unit (ReLU) as the activation function. The Adam optimizer is employed with a learning rate of 0.001 for training the policy MOQ network. We adopt the decay rate 0.9995 to reduce the random exploration probability Îµ from 1 to 0.01. The balance weight Ï is initially set to 1, and it is decreased from 1 to 0.01. Table III lists other parameter values used in the experiment.

In order to fully evaluate the optimization performance, we generate various test instances using two important parameters, i.e., the number of GSDs, M , and the UAVâs flight height, U . We specify $M \in \{ 6 0 , 1 0 0 , 1 4 0 \}$ and $U \in \{ 3 0 , 5 0 \}$ . Based on 60 100 140 30 50different combinations between M and U, we can generate six test instances to simulate different UAV-assisted MEC networks, as shown in Table IV.

TABLE V  
RESULTS OF IGD
<table><tr><td>Instance (M,U)</td><td>NSGA-II</td><td>MOEA/D</td><td>Naive</td><td>MODQN</td><td>MORL-DW</td><td>MORL-TS</td><td>EMOQL</td><td>MORL-TER</td></tr><tr><td>I-(60,30)</td><td>0.2067</td><td>0.1957</td><td>0.1220</td><td>0.0602</td><td>0.0479</td><td>0.0485</td><td>0.0343</td><td>0.0056</td></tr><tr><td>I-(60,50)</td><td>0.3287</td><td>0.3819</td><td>0.1429</td><td>0.0989</td><td>0.0748</td><td>0.0558</td><td>0.0453</td><td>0.0064</td></tr><tr><td>I-(100,30)</td><td>0.1438</td><td>0.1272</td><td>0.0863</td><td>0.0716</td><td>0.0432</td><td>0.0552</td><td>0.0516</td><td>0.0059</td></tr><tr><td>I-(100,50)</td><td>0.1664</td><td>0.1168</td><td>0.0818</td><td>0.0598</td><td>0.0450</td><td>0.0427</td><td>0.0283</td><td>0.0126</td></tr><tr><td>I-(140,30)</td><td>0.1349</td><td>0.1273</td><td>0.1087</td><td>0.0921</td><td>0.0893</td><td>0.0853</td><td>0.0378</td><td>0.0111</td></tr><tr><td>I-(140,30)</td><td>0.1467</td><td>0.0915</td><td>0.0815</td><td>0.0724</td><td>0.0437</td><td>0.0343</td><td>0.0252</td><td>0.0098</td></tr></table>

TABLE VI

AVERAGE RANKS AND POSITIONS OF EIGHT ALGORITHMS BASED ON AER, AE, AND IGD
<table><tr><td rowspan="2">Algorithm</td><td colspan="2">AER</td><td colspan="2">AE</td><td colspan="2">IGD</td></tr><tr><td>Averagerank</td><td>Position</td><td>Averagerank</td><td>Position</td><td>Averagerank</td><td>Position</td></tr><tr><td>NSGA-II</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>7.8333</td><td>8</td></tr><tr><td>MOEA/D</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>7.1667</td><td>7</td></tr><tr><td>Naive</td><td>6.0000</td><td>6</td><td>5.0000</td><td>6</td><td>6.0000</td><td>6</td></tr><tr><td>MODQN</td><td>5.0000</td><td>5</td><td>4.8333</td><td>5</td><td>5.0000</td><td>5</td></tr><tr><td>MORL-DW</td><td>3.8333</td><td>4</td><td>4.0000</td><td>4</td><td>3.5000</td><td>4</td></tr><tr><td>MORL-TS</td><td>3.0000</td><td>3</td><td>2.6667</td><td>3</td><td>3.3333</td><td>3</td></tr><tr><td>EMOQL</td><td>2.0000</td><td>2</td><td>2.5000</td><td>2</td><td>2.1667</td><td>2</td></tr><tr><td>MORL-TER</td><td>1.0000</td><td>1</td><td>1.0000</td><td>1</td><td>1.0000</td><td>1</td></tr></table>

TABLE VII

AEE VALUES OF EIGHT ALGORITHMS
<table><tr><td>Instance (M,U)</td><td>NSGA-II</td><td>MOEA/D</td><td>Naive</td><td>MODQN</td><td>MORL-DW</td><td>MORL-TS</td><td>EMOQL</td><td>MORL-TER</td></tr><tr><td>I-(60,30)</td><td>4588.2968</td><td>4417.0441</td><td>4666.2617</td><td>4746.1316</td><td>4750.9198</td><td>4797.2326</td><td>4752.0688</td><td>4756.1426</td></tr><tr><td>I-(60,50)</td><td>4030.9909</td><td>3744.4423</td><td>3842.0415</td><td>4346.1316</td><td>4394.3907</td><td>4430.0549</td><td>4426.8519</td><td>4485.1426</td></tr><tr><td>I-(100,30)</td><td>3955.9134</td><td>3914.8485</td><td>4074.2826</td><td>4559.7300</td><td>4533.0856</td><td>4562.2499</td><td>4568.3572</td><td>4570.2803</td></tr><tr><td>I-(100,50)</td><td>3784.1530</td><td>3550.2815</td><td>3786.3759</td><td>3858.6753</td><td>3880.5634</td><td>3937.7893</td><td>4088.0439</td><td>4176.7917</td></tr><tr><td>I-(140,30)</td><td>3609.0996</td><td>3725.1822</td><td>3634.9195</td><td>4304.6842</td><td>4237.7060</td><td>4456.2557</td><td>4564.8346</td><td>4383.0884</td></tr><tr><td>I-(140,50)</td><td>3032.7680</td><td>2924.0091</td><td>3026.3812</td><td>3302.0170</td><td>3375.0501</td><td>3527.1929</td><td>3667.3174</td><td>3823.1062</td></tr></table>

TABLE VIII

ANT VALUES OF EIGHT ALGORITHMS
<table><tr><td>Instance (M,U)</td><td>NSGA-II</td><td>MOEA/D</td><td>Naive</td><td>MODQN</td><td>MORL-DW</td><td>MORL-TS</td><td>EMOQL</td><td>MORL-TER</td></tr><tr><td>I-(60,30)</td><td>39.2333</td><td>42.7667</td><td>43.1667</td><td>46.0733</td><td>39.6067</td><td>42.9000</td><td>65.4000</td><td>74.2867</td></tr><tr><td>I-(60,50)</td><td>40.2333</td><td>43.5667</td><td>94.9333</td><td>86.1467</td><td>91.3467</td><td>91.6800</td><td>99.7533</td><td>148.8133</td></tr><tr><td>I-(100,30)</td><td>60.1600</td><td>59.2800</td><td>61.2067</td><td>62.8467</td><td>63.3067</td><td>66.3867</td><td>66.1800</td><td>113.4600</td></tr><tr><td>I-(100,50)</td><td>134.6667</td><td>156.7200</td><td>133.1333</td><td>145.8267</td><td>146.8600</td><td>140.1867</td><td>163.9400</td><td>186.0133</td></tr><tr><td>I-(140,30)</td><td>72.1333</td><td>65.5133</td><td>69.6867</td><td>82.2333</td><td>87.1600</td><td>78.6333</td><td>99.3733</td><td>131.8333</td></tr><tr><td>I-(140,50)</td><td>135.3267</td><td>158.4667</td><td>143.6133</td><td>163.2733</td><td>183.2533</td><td>191.8200</td><td>205.6467</td><td>227.7933</td></tr></table>

TABLE IX

ACOI VALUES OF EIGHT ALGORITHMS
<table><tr><td>Instance (M,U)</td><td>NSGA2</td><td>MOEA/D</td><td>Naive</td><td>MODQN</td><td>MORL-DW</td><td>MORL-TS</td><td>EMOQL</td><td>MORL-TER</td></tr><tr><td>I-(60,30)</td><td>2302.2253</td><td>2405.7201</td><td>2472.7192</td><td>2484.5099</td><td>2496.4388</td><td>2501.3396</td><td>2536.4396</td><td>2542.6151</td></tr><tr><td>I-(60,50)</td><td>2201.2253</td><td>2385.7201</td><td>2419.4913</td><td>2355.1503</td><td>2461.9522</td><td>2468.8766</td><td>2469.3586</td><td>2496.7145</td></tr><tr><td>I-(100,30)</td><td>2280.6970</td><td>2387.8461</td><td>2375.7246</td><td>2373.4551</td><td>2470.2029</td><td>2482.1602</td><td>2477.5002</td><td>2487.9340</td></tr><tr><td>I-(100,50)</td><td>1877.9512</td><td>1975.5409</td><td>2016.5750</td><td>2356.4529</td><td>2358.7269</td><td>2359.4886</td><td>2365.9576</td><td>2397.8544</td></tr><tr><td>I-(140,30)</td><td>2243.0598</td><td>2216.3672</td><td>2244.6158</td><td>2337.1092</td><td>2408.7563</td><td>2457.0549</td><td>2460.9904</td><td>2479.8087</td></tr><tr><td>I-(140,50)</td><td>1602.0953</td><td>1762.5290</td><td>1638.4495</td><td>2139.0113</td><td>2213.3376</td><td>2231.9985</td><td>2256.4042</td><td>2358.4983</td></tr></table>

## A. Evaluation Indicator

We adopt five widely used evaluation indicators to comprehensively measure the performance of MORL-TER. These indicators include the average episodic regret [36], adaption error [34], inverted generational distance [41], comprehensive objective indicator [2], and Friedman test [42].

1) Average Episodic Regret: We evaluate the performance of an MORL based on its regret. The regret is defined as the difference between optimal and actual returns [36], as follows.

$$
\begin{array} { l } { { \displaystyle \Delta ( { \bf w } , { \bf R _ { 1 } } ) = { \bf w } \cdot { \bf V _ { w } ^ { * } } - { \bf w } \cdot { \bf R _ { 1 } } } \ ~ } \\ { { \displaystyle ~ = { \bf w } \cdot { \bf V _ { w } ^ { * } } - { \bf w } \cdot \sum _ { t = 1 } ^ { T } \gamma ^ { t - 1 } { \bf r } _ { t } } , } \end{array}\tag{30}
$$

where $\mathbf { V } _ { \mathbf { w } } ^ { * }$ and ${ \bf R } _ { 1 }$ are the optimal and actual returns for preference w at time step t , respectively. $\mathbf { r } _ { t }$ is the immediate vectorial rewards received at the t-th time step, $t = 1 , . . . , T$ Differ from ${ \bf R } _ { 1 }$ , the regret provides a shared $\mathbf { V } _ { \mathbf { w } } ^ { * }$ = 1for preference w. In other words, an optimal policy consistently yields a regret value of 0. Based on (30), the average episodic regret (AER) is calculated as

TABLE X  
AVERAGE RANKS AND POSITIONS OF EIGHT ALGORITHMS BASED ON AEE, ANT, AND ACOI
<table><tr><td rowspan="2">Algorithm</td><td colspan="2">AEE</td><td colspan="2">ANT</td><td colspan="2">ACOI</td></tr><tr><td>Averagerank</td><td>Position</td><td>Average rank</td><td>Position</td><td>Averagerank</td><td>Position</td></tr><tr><td>NSGA-II</td><td>6.8333</td><td>8</td><td>7.3333</td><td>8</td><td>7.8333</td><td>8</td></tr><tr><td>MOEA/D</td><td>7.6667</td><td>7</td><td>6.3333</td><td>7</td><td>6.5000</td><td>7</td></tr><tr><td>Naive</td><td>6.5000</td><td>6</td><td>5.8333</td><td>6</td><td>6.0000</td><td>6</td></tr><tr><td>MODQN</td><td>4.6667</td><td>5</td><td>4.6667</td><td>5</td><td>5.6667</td><td>5</td></tr><tr><td>MORL-DW</td><td>4.3333</td><td>4</td><td>4.5000</td><td>4</td><td>4.0000</td><td>4</td></tr><tr><td>MORL-TS</td><td>2.3333</td><td>3</td><td>4.1667</td><td>3</td><td>2.8333</td><td>3</td></tr><tr><td>EMOQL</td><td>2.1667</td><td>2</td><td>2.6667</td><td>2</td><td>2.1667</td><td>2</td></tr><tr><td>MORL-TER</td><td>1.5000</td><td>1</td><td>1.0000</td><td>1</td><td>1.0000</td><td>1</td></tr></table>

$$
\mathrm { A E R } = \frac { 1 } { N _ { \operatorname* { m a x } } ^ { \mathrm { e p s } } } \sum _ { i = 1 } ^ { N _ { \operatorname* { m a x } } ^ { \mathrm { e p s } } } \Delta ( \mathbf { w } _ { i } , \mathbf { R } _ { i } ) , \mathbf { w } _ { i } \in \Omega ,\tag{31}
$$

where $\mathbf { w } _ { i } , \mathbf { R } _ { i } .$ , and $\Delta ( \mathbf { w } _ { i } , \mathbf { R } _ { i } )$ represent the preference, return, regret in the i-th episode, respectively. An MORL algorithm with a smaller AER has better performance.

2) Adaptation Error: To evaluate the adaptation capability of an MORL algorithm to preference dynamics, we compare ${ \bf R } _ { 1 }$ with $\mathbf { V } _ { \mathbf { w } } ^ { * }$ when a preference $\mathbf { w } \in \Omega$ is provided by the algorithm Î©in the testing stage. The adaptation error (AE) is defined as the average relative error between w Â· $\mathbf { R _ { 1 } }$ and $\mathbf { V } _ { \mathbf { w } } ^ { * }$

$$
{ \mathrm { A E } } = \frac { 1 } { \Phi } \sum _ { \mathbf { w } \in \Omega } \left| \frac { \mathbf { w } \cdot \mathbf { R } _ { 1 } - \mathbf { w } \cdot \mathbf { V } _ { \mathbf { w } } ^ { * } } { \mathbf { w } \cdot \mathbf { V } _ { \mathbf { w } } ^ { * } } \right| .\tag{32}
$$

A smaller AE represents the corresponding MORL is better adaptive to dynamic preferences.

3) Inverted Generational Distance: The Pareto front (PF) can be used to calculate the inverted generational distance (IGD). Let $\mathcal { F } _ { \mathrm { r e f e r } }$ and ${ \mathcal { F } } _ { \mathrm { k n o w n } }$ represent the referenced PF and known PF obtained by an algorithm, respectively. It is noted that $\mathcal { F } _ { \mathrm { r e f e r } }$ may be unknown for highly complex MOO problems, such as the ETWC problem. In such cases, a widely used approach in the literature [2], [41], [42] is to collect the best solutions so far obtained by all algorithms and choose the non-dominated ones from them. The corresponding PF is treated as $\mathcal { F } _ { \mathrm { r e f e r } }$ . IGD is defined as

$$
\mathrm { I G D } = \frac { \sum _ { \mu \in \mathcal { F } _ { \mathrm { r e f e r } } } d ( \mu , \mathcal { F } _ { \mathrm { k n o w n } } ) } { | \mathcal { F } _ { \mathrm { r e f e r } } | } ,\tag{33}
$$

where $d ( \mu , \mathcal { F } _ { \mathrm { k n o w n } } )$ is the euclidean distance between $\mu$ in $\mathcal { F } _ { \mathrm { r e f e r } }$ and its nearest point in $\mathcal { F } _ { \mathrm { k n o w n } }$ . IGD can reflect both the convergence and diversity of a known PF. The smaller IGD value reflects better performance.

4) Comprehensive Objective Indicator: Given the ETWC problem with two objectives, we design a comprehensive objective indicator (COI), with $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ considered simultaneously. For each objective vector, we adopt linear scalarization to aggregate it into a COI. Note that two elements of an objective vector are corresponding to objectives $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ respectively. After a single run, an MORL can achieve many objective vectors for preference $\mathbf { w } = ( w ^ { 1 } , w ^ { 2 } )$ . Let $E N ^ { i } ( \mathbf { w } ) =$ $( E _ { \mathrm { t o t a l } } ^ { i } ( \mathbf { w } ) , N _ { \mathrm { t o t a l } } ^ { i } ( \mathbf { w } ) )$ = ( ) ( ) =represent the i-th objective vector of w, $i = 1 , . . . , n _ { \bf w }$ ( )). The COI of $E N ^ { i } ( \mathbf { w } )$ is defined as

$$
\begin{array} { r l } & { C O I ^ { i } ( \mathbf { w } ) = \mathbf { w } \cdot E N ^ { i } ( \mathbf { w } ) } \\ & { \qquad = w ^ { 1 } \cdot E _ { \mathrm { t o t a l } } ^ { i } ( \mathbf { w } ) + w ^ { 2 } \cdot N _ { \mathrm { t o t a l } } ^ { i } ( \mathbf { w } ) . } \end{array}\tag{34}
$$

The best objective vector for w, $E N ^ { b } ( { \mathbf w } )$ , is obtained by

$$
\begin{array} { r } { E N ^ { b } ( \mathbf { w } ) = \left( E _ { \mathrm { t o t a l } } ^ { b } ( \mathbf { w } ) , N _ { \mathrm { t o t a l } } ^ { b } ( \mathbf { w } ) \right) , b = \underset { i \in \{ 1 , \dots , n _ { \mathbf { w } } \} } { \mathrm { a r g m a x } } \ C O I ^ { i } ( \mathbf { w } ) , } \end{array}\tag{35}
$$

where $E _ { \mathrm { t o t a l } } ^ { b } ( \mathbf { w } )$ and $N _ { \mathrm { t o t a l } } ^ { b } ( \mathbf { w } )$ are the best $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ for w, ( ) ( )respectively. Based on (34) and (35), we calculate the average energy efficiency (AEE), average number of tasks collected (ANT), and average COI (ACOI) for all preferences in , defined as

$$
\mathrm { A E E } = \frac { 1 } { \Phi } \sum _ { \mathbf { w } \in \Omega } E _ { \mathrm { t o t a l } } ^ { b } ( \mathbf { w } ) ,\tag{36}
$$

$$
\mathrm { A N T } = \frac { 1 } { \Phi } \sum _ { \mathbf { w } \in \Omega } N _ { \mathrm { t o t a l } } ^ { b } ( \mathbf { w } ) ,\tag{37}
$$

$$
\mathrm { A C O I } = \frac { 1 } { \Phi } \sum _ { { \bf w } \in \Omega } C O I ^ { b } ( { \bf w } ) .\tag{38}
$$

5) Friedman Test: The test [42] is used to distinguish differences between algorithms in terms of algorithm-related metrics including AER, AE, and IGD, and system-related metrics including AEE, ANT, and ACOI. Consider all test instances, the average ranks of all algorithms are calculated. Based on these average ranks, the relative positions of each algorithm are determined, providing a clear indication of their respective performances.

## B. Performance Evaluation

After running MORL-TER, we can obtain a single parametric policy MOQ network to generalize across the entire preference space. In other words, when providing a given preference, the trained policy MOQ network can output the corresponding optimal policy (i.e., flight trajectory) by simple algebraic calculations. Suppose the decision-makerâs current preferences can be denoted as $\mathbf { w } _ { 1 } = ( 1 . 0 , 0 . 0 ) , \mathbf { w } _ { 2 } = ( 0 . 0 , 1 . 0 )$ , and $\mathbf { w } _ { 3 } =$ . , . . Preference $\mathbf { w } _ { 1 }$ represents that one only focuses on (0 5 0 5)maximizing the total energy efficiency $E _ { \mathrm { t o t a l } }$ without considering objective $N _ { \mathrm { t o t a l } }$ . Similarly, preferences $\mathbf { w } _ { 2 }$ aims at maximizing the number of collected tasks, $N _ { \mathrm { t o t a l } }$ , ignoring objective $E _ { \mathrm { t o t a l } }$

<!-- image-->  
Fig. 4. Trajectories of the UAV under three different preferences.

Preference $\mathbf { w } _ { 3 }$ denotes that two objectives $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ are important equally, i.e., maximizing them simultaneously.

Fig. 4 shows the three trajectories corresponding to the above three preferences in I-(60,30). Note that the UAVâs take-off point is set to the central point. The blue trajectory corresponds to $\mathbf { w } _ { 1 }$ that aims to maximize $E _ { \mathrm { t o t a l } } .$ , neglecting objective $N _ { \mathrm { t o t a l } }$ . One can observe that the UAV operates in the sparsely populated GSD region, contributing to improving the UAVâs energy efficiency. This is attributed to the fewer computation tasks collected, the lower transmitting energy consumption $E _ { t } ^ { \mathrm { { T r } } }$ and processing energy consumption $E _ { t } ^ { \mathrm { P } }$ . The green trajectory is associated with $\mathbf { w } _ { 2 }$ that focuses on maximizing $N _ { \mathrm { t o t a l } }$ individually. It is observed that the UAV moves to the dense GSD area to collect computation tasks as many as possible without considering energy efficiency. The red trajectory corresponds to $\mathbf { w } _ { 3 }$ that concentrates on maximizing $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ simultaneously. The UAV is observed to navigate within the dense GSD region to collect computation tasks. Nevertheless, compared with the blue trajectory, the UAV can avoid collecting excessive tasks because it needs to maintain appropriate energy efficiency. According to the analysis above, the proposed MORL-TER owns the capability to obtain potential control policies based on diverse preferences in a single run.

To fully investigate the performance of MORL-TER, we consider employing five state-of-the-art MORLs and compare the proposed approach with them in terms of AER, AE, IGD, COI, and Friedman test in six test instances. The compared algorithms are listed below.

- Naive: The approach [37] formulates an overall user utility through converting multiple single-objective Q-values into an aggregated function, which is used to select actions.

MODQN : This approach is based on multi-objective deep Q-network [38], which aims to learn the vectorial Q-function, while the Q-network is only activated and learned on the current preference.

- MORL-DW: This approach combines the dynamic weights [36] and MORL, which aims to deal with dynamic preference problems. MORL-DW can adapt to changing preferences through learning and optimizing multiobjective Q-value vectors.

<!-- image-->  
Fig. 5. Average episodic regret of six MORL algorithms.

MORL-TS: This approach combines MORL-DW and the tournament selection scheme [39], to address the task offloading problem with dynamic preferences, aiming at minimizing completion time, energy consumption, and usage charge, simultaneously.

- EMOQL: This approach is introduced in [34], called envelope multi-objective Q-learning, which aims to learn a single parametric representation for optimal policies over the preference space.

- MORL-TER: The proposed EMOQL with the TER scheme in this paper.

Fig. 5 illustrates the AER values of the six MORL algorithms. It is obvious that MORL-TER outperforms the other five algorithms in all test instances since its AER is the smallest. Oppositely, the worst MORL algorithm is Naive because it has the largest AER values in all instances. Naive optimizes multiobjective Q-values separately and adopts an aggregated function to select actions. However, due to the independent updates of Q-values for individual objectives, its learned multi-objective Qvalues may not effectively capture a favorable balance between objectives. Consequently, Naive cannot maximize two objectives, $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ , simultaneously. MODQN is identified as the second worst algorithm across all test instances. The primary reason for its poor performance is that its Q-network cannot incorporate the state and preference as its input. Moreover, the network is trained exclusively on the current preference. Thus, MODQN lacks the ability to retain learned policies for different preferences and fails to effectively adapt to varying preferences in dynamic MEC networks.

On the contrary, MORL-DW concatenates the current state and preference and feeds them into its Q-network, to adapt to the changing preferences. Moreover, the network is trained simultaneously on the current and encountered preferences, preventing it from overfitting to the current preference. Thus, MORL-DW outperforms MODQN regarding AER in almost all instances. However, MORL-DW lacks the ability to prioritize encountered preferences based on their significance, as it equally treats all preferences. Thus, this approach is prone to forgetting previously learned policies. By introducing the TS scheme, MORL-TS is better than MORL-DW in almost all instances. MORL-TS can select those preferences that are more significant with higher probability, which enables its Q-network to memorize the previously learned optimal policies.

<!-- image-->  
Fig. 6. Adaptation error of six MORL algorithms.

EMOQL surpasses MORL-TS in all test instances because it selects multiple preferences from the preference space to train the Q-network. Thus, EMOQL can obtain a reasonable coordination between preferences and corresponding optimal policies, preventing it from over-adapting to one of the preferences. This also demonstrates why EMOQL is selected for solving the ETWC problem. Nevertheless, EMOQL treats transitions as atomic units when considering them for addition in or deletion from the buffer, resulting in that the experiences obtained by a preferenceâs optimal policy can be harmful to another preferenceâs training. Unlike EMOQL, the proposed MORL-TER with the TER scheme treats traces (i.e., a trace consists of an episodeâs transitions) as atomic units when adding and deleting them from the experience buffer. The TER scheme adopts the crowding distance to reflect the relative diversity of a trace in the experience buffer B. A trace with a bigger crowding distance has better diversity. Thus, the trace can be used to train another policy, so as to MORL-TER can maintain the previously learned optimal policies, and improve the MOO performance under dynamic preferences. This is why MORL-TER outperforms EMOQL in all test instances. Fig. 6 illustrates the adaptation error obtained by the six algorithms. It can be seen that MORL-TER exceeds the other five MORLs as it always has the smallest AE values. It means that MORL-TER can better deal with changing preferences in dynamic MEC networks than the other five algorithms.

We also show the cumulative weighted sum of the vectorial return (CWS-VR) in each episode, which can reflect an MORLâs convergence performance and sampling efficiency. Based on the current preference w and vectorial return ${ \bf R } _ { 1 }$ , we can calculate CWS-VR wR1 obtained by an MORL at the end of each episode. Fig. 7 shows CWS-VR versus episode in I-(60,30), which reveals the convergence behaviors of six MORLs. One can observe that the proposed MORL-TER converges at a fast speed, for which around 1000 episodes are required. Moreover, MORL-TER has a faster convergence speed than the other five algorithms, which validates its effectiveness and availability.

<!-- image-->  
Fig. 7. Cumulative weighted sum of vectorial return versus episode.

<!-- image-->  
Fig. 8. Total number of tasks collected versus preference of objective $N _ { \mathrm { t o t a l } }$

In addition, Fig. 8 illustrates the total number of tasks collected versus the preference of objective $N _ { \mathrm { t o t a l } }$ in I-(60,30). It is seen that the overall trend of task number is upward, as preferences of $N _ { \mathrm { t o t a l } }$ increase. The larger preferences of $N _ { \mathrm { t o t a l } }$ signify that the UAV pays more attention to collecting tasks. Furthermore, MORL-TER can obtain a larger number of tasks collected than the other five algorithms for almost all preferences of $N _ { \mathrm { t o t a l } }$ . Thus, MORL-TER can collect more tasks by properly planning the UAVâs flight trajectories.

We also add two well-known multi-objective evolutionary algorithms (MOEAs) into performance comparison, including NSGA-II and MOEA/D. The two algorithms are listed below.

- NSGA-II: The fast and elitist non-dominated sorting genetic algorithm is adopted to balance the task delay and energy consumption, aiming at meeting user requirements of diverse applications [43].

- MOEA/D: The multi-objective evolutionary algorithm based on decomposition is adopted to reduce the application delay and energy consumption in an MEC network [42].

IGD values obtained by eight algorithms are exhibited in Table V. IGD reflects the diversification and convergence of multiple non-dominated policies simultaneously. At first glance, it is evident that two well-recognized algorithms, NSGA-II and MOEA/D, perform suboptimally, failing to discover satisfactory non-dominated policies in all test instances. The primary reason for this underperformance can be attributed to the inherent challenges posed by high-dimensional multi-objective optimization problems within dynamic environments, exemplified by the ETWC problem. MOEAs often expend a substantial amount of time in their pursuit of decent non-dominated policies, making it difficult to achieve convergence within tight time constraints. In particular, MOEAs with extensive encoding lengths, for example, 100, face a time-consuming process in generating acceptable non-dominated policies. Furthermore, the dynamic and uncertain nature of the UAV-assisted MEC environment compounds these challenges. In practical terms, these dynamics and uncertainties frequently necessitate the reinitiation of MOEAs from the beginning, imposing considerable computational overhead and diminishing their convergence speed.

<!-- image-->  
(a) I-(60,30)

<!-- image-->  
(b) I-(60,50)

<!-- image-->  
(c) I-(100,30)

<!-- image-->  
(d) 1-(100,50)

<!-- image-->  
(e) I-(140,30)

<!-- image-->  
(f) I-(140,50)  
Fig. 9. Pareto fronts of eight algorithms.

Second, in all test instances, all MORLs consistently surpass NSGA-II and MOEA/D. A key distinction lies in the decisionmaking process: while MOEAs rely on a single chromosome to make decisions for all time slots, MORLs employ real-time decision-making for each time slot, taking into account the prevailing environmental conditions. Notably, MORLs seamlessly integrate reinforcement learning with deep neural networks, enabling them to tackle sequential decision-making challenges in dynamic MEC environments. This capability stems from their adaptability to environmental changes, achieved through iterative interactions with the MEC environment. Consequently,

MORLs exhibit rapid convergence and responsiveness to user requirements. These attributes render MORLs a superior choice for addressing the ETWC problem in comparison to MOEAs.

Finally, MORL-TER obtains the smallest IGD values in all test instances, validating its superiority over the other seven algorithms. MORL-TER can adapt to various user preferences by learning weight-dependent multi-objective Q-value vectors, thus it can obtain the optimal non-dominated policies corresponding to these preferences. To further support our observation above, the Pareto fronts of eight algorithms are shown in Fig. 9, which demonstrate the excellent performance of MORL-TER.

The Friedman test is employed to clearly reflect the position ranks of the eight algorithms with respect to AER, AE, and IGD. Based on the three metrics values, Table VI shows the average ranks and positions of the eight algorithms. It is clearly seen that MORL-TER achieves the best multi-objective optimization performance.

Tables VII and VIII illustrate the AEE and ANT values of eight algorithms, respectively, where the best results are in bold. Regardless of whether M or U is kept constant, the corresponding AEE values exhibit a tendency to decrease as the other parameter increases. First, if the number of GSDs grows, M, the UAV has to transmit more energy to them. Second, as the flight height increases, U, the coverage of the UAV expands correspondingly, hence it also transmits more energy to the GSDs within the coverage. However, transmitting more energy to GSDs results in lower energy efficiency. Table VII well supports this. On the other hand, no matter whether M or U is fixed, the associated ANT values increase as the other grows up. This is because either more GSDs or higher flight heights

will lead to more computation tasks being collected by the UAV.   
Table VIII also well supports this phenomenon.

In Table VII, it is observed that MORL-TER outperforms the other algorithms without regard to I-(60,30) and I-(140,30). While MORL-TS and EMOQL obtain decent AEE values in I-(60,30) and I-(140,30) respectively, they perform poorly in terms of ANT. For instance, although MORL-TS achieves the largest AEE value in I-(60,30), it results in a poor ANT value among all algorithms. While EMOQL obtains the optimal AEE value, its ANT value is worse than that of MORL-TER in I-(140,30). MORL-TER is the best because it obtains the largest ANT values in all test instances, as shown in Table VIII. This implies that the MORL-TER enables the UAV to efficiently collect abundant computation tasks from GSDs by appropriately optimizing the UAVâs flight trajectories.

Table IX shows the ACOI values of eight algorithms. One can observe that although MORL-TER cannot acquire the best results in all test instances regarding AEE, it performs better than the other seven algorithms with respect to ACOI. As aforementioned, the ACOI can reflect the overall performance of a multi-objective optimization algorithm. Thus, MORL-TER can balance the two objectives $E _ { \mathrm { t o t a l } }$ and $N _ { \mathrm { t o t a l } }$ . Based on the results of AEE, ANT, and ACOI, Table X shows the average ranks and positions of eight algorithms. It is easily seen that MORL-TER achieves the best comprehensive performance.

## VII. CONCLUSION

This paper models the problem of energy-efficient trajectory optimization with wireless charging (ETWC) by MOMDP and proposes a modified MORL algorithm with the trace-based experience replay scheme, namely MORL-TER, to solve the ETWC problem. MORL-TER can adapt to the dynamics of preferences, thus obtaining a tradeoff between objectives. Compared with five MORLs including Naive, MODQN, MORL-DW, MORL-TS, and EMOQL, and two MOEAs including NSGA-II and MOEA/D, our algorithm achieves better multi-objective optimization performance in all test instances regarding algorithmrelated metrics, including average episodic regret, adaptation error, and inverted generational distance. MORL-TER also exhibits superior performance across various system-related metrics, such as the average energy efficiency, average number of tasks collected by the UAV, and average comprehensive objective indicator, in almost all instances. Furthermore, MORL-TER achieves the best rank in the Friedman test for both algorithmand system-related metrics. Therefore, these results highlight excellent performance of MORL-TER and its potential applicability in UAV-assisted MEC networks characterized by dynamic preference requirements.

## REFERENCES

[1] F. Wang, J. Xu, and S. Cui, âOptimal energy allocation and task offloading policy for wireless powered mobile edge computing systems,â IEEE Trans. Wireless Commun., vol. 19, no. 4, pp. 2443â2459, Apr. 2020.

[2] F. Song et al., âEvolutionary multi-objective reinforcement learning based trajectory control and task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 12, pp. 7387â7405, Dec. 2023, doi: 10.1109/TMC.2022.3208457.

[3] P. Mach and Z. Becvar, âMobile edge computing: A survey on architecture and computation offloading,â IEEE Commun. Surveys Tut., vol. 19, no. 3, pp. 1628â1656, Third Quarter, 2017.

[4] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[5] K. Zhang, X. Gui, D. Ren, and D. Li, âEnergy-latency tradeoff for computation offloading in UAV-assisted multiaccess edge computing system,â IEEE Internet Things J., vol. 8, no. 8, pp. 6709â6719, Apr. 2021.

[6] Z. Ning et al., âDynamic computation offloading and server deployment for UAV-enabled multi-access edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 5, pp. 2628â2644, May 2023.

[7] Y. Liu, K. Xiong, Q. Ni, P. Fan, and K. B. Letaief, âUAV-assisted wireless powered cooperative mobile edge computing: Joint offloading, CPU control, and trajectory optimization,â IEEE Internet Things J., vol. 7, no. 4, pp. 2777â2790, Apr. 2020.

[8] Y. Yu, J. Tang, J. Huang, X. Zhang, D. K. C. So, and K.-K. Wong, âMultiobjective optimization for UAV-assisted wireless powered IoT networks based on extended DDPG algorithm,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6361â6374, Sep. 2021.

[9] Z. Cheng, M. Liwang, N. Chen, L. Huang, X. Du, and M. Guizani, âDeep reinforcement learning-based joint task and energy offloading in UAV-aided 6G intelligent edge networks,â Comput. Commun., vol. 192, pp. 234â244, Jun. 2022.

[10] M. Zhao, Q. Shi, and M. Zhao, âEfficiency maximization for UAV-enabled mobile relaying systems with laser charging,â IEEE Trans. Wireless Commun., vol. 19, no. 5, pp. 3257â3272, May 2020.

[11] X. Hu, K.-K. Wong, and Y. Zhang, âWireless-powered edge computing with cooperative UAV: Task, time scheduling and trajectory design,â IEEE Trans. Wireless Commun., vol. 19, no. 12, pp. 8083â8098, Dec. 2020.

[12] K. Wang, X. Zhang, L. Duan, and J. Tie, âMulti-UAV cooperative trajectory for servicing dynamic demands and charging battery,â IEEE Trans. Mobile Comput., vol. 22, no. 3, pp. 1599â1614, Mar. 2023.

[13] M. Li, L. Liu, Y. Gu, Y. Ding, and L. Wang, âMinimizing energy consumption in wireless rechargeable UAV networks,â IEEE Internet Things J., vol. 9, no. 5, pp. 3522â3532, Mar. 2022.

[14] Q. Liu et al., âJoint power and time allocation in energy harvesting of UAV operating system,â Comput. Commun., vol. 150, pp. 811â817, Jan. 2020.

[15] J. Chen and J. Xie, âJoint task scheduling, routing, and charging for multi-UAV based mobile edge computing,â in Proc. IEEE Int. Conf. Commun., 2022, pp. 1â6.

[16] J. Shi, P. Cong, L. Zhao, X. Wang, S. Wan, and M. Guizani, âA two-stage strategy for UAV-enabled wireless power transfer in unknown environments,â IEEE Trans. Mobile Comput., vol. 23, no. 2, pp. 1785â1802, Feb. 2024, doi: 10.1109/TMC.2023.3240763.

[17] J. Wang, C. Jin, Q. Tang, N. N. Xiong, and G. Srivastava, âIntelligent ubiquitous network accessibility for wireless-powered MEC in UAV-assisted B5G,â IEEE Trans. Netw. Sci. Eng., vol. 8, no. 4, pp. 2801â2813, Fourth Quarter, 2021.

[18] Q. Li, L. Shi, Z. Zhang, and G. Zheng, âResource allocation in UAV-enabled wireless-powered MEC networks with hybrid passive and active communications,â IEEE Internet Things J., vol. 10, no. 3, pp. 2574â2588, Feb. 2023.

[19] Y. Zhang, Z. Na, H. Ren, and B. Lin, âWireless-powered UAV-assisted MEC: Joint resource allocation and trajectory optimization,â in Proc. IEEE/CIC Int. Conf. Commun., 2023, pp. 1â6.

[20] X. Gu, G. Zhang, M. Wang, W. Duan, M. Wen, and P.-H. Ho, âUAV-aided energy-efficient edge computing networks: Security offloading optimization,â IEEE Internet Things J., vol. 9, no. 6, pp. 4245â4258, Mar. 2022.

[21] Z. Yang, W. Xu, and M. Shikh-Bahaei, âEnergy efficient UAV communication with energy harvesting,â IEEE Trans. Veh. Technol., vol. 69, no. 2, pp. 1913â1927, Feb. 2020.

[22] L. Zhang, X. Liu, and N. Ansari, âUAV-assisted efficient far-field wireless charging for WSN,â in Proc. IEEE Glob. Commun. Conf., 2022, pp. 1734â1739.

[23] Y. Li, S. Shi, Y. Miao, Z. Xu, C. Wu, and S. Zhang, âEnergy efficiency optimization in multi-UAV energy harvesting network,â in Proc. IEEE Glob. Commun. Conf. Workshops, 2022, pp. 1419â1424.

[24] L. Zhang, A. Celik, S. Dang, and B. Shihada, âEnergy-efficient trajectory optimization for UAV-assisted IoT networks,â IEEE Trans. Mobile Comput., vol. 21, no. 12, pp. 4323â4337, Dec. 2022.

[25] Z. Xiong et al., âUAV-assisted wireless energy and data transfer with deep reinforcement learning,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 1, pp. 85â99, Mar. 2021.

[26] S. Fu et al., âEnergy-efficient UAV-enabled data collection via wireless charging: A reinforcement learning approach,â IEEE Internet Things J., vol. 8, no. 12, pp. 10209â10219, Jun. 2021.

[27] K. Zhu et al., âAerial refueling: Scheduling wireless energy charging for UAV enabled data collection,â IEEE Trans. Green Commun. Netw., vol. 6, no. 3, pp. 1494â1510, Sep. 2022.

[28] C. Chen, S. Gong, W. Zhang, Y. Zheng, and Y. C. Kiat, âDeep reinforcement learning based contract incentive for UAVs and energy harvest assisted computing,â in Proc. IEEE Glob. Commun. Conf., 2022, pp. 2224â2229.

[29] L. Liu, K. Xiong, J. Cao, Y. Lu, P. Fan, and K. B. Letaief, âAverage AoI minimization in UAV-assisted data collection with RF wireless power transfer: A deep reinforcement learning scheme,â IEEE Internet of Things J., vol. 9, no. 7, pp. 5216â5228, Apr. 2022.

[30] O. S. Oubbati, A. Lakas, and M. Guizani, âMultiagent deep reinforcement learning for wireless-powered UAV networks,â IEEE Internet Things J., vol. 9, no. 17, pp. 16044â16059, Sep. 2022.

[31] S. Zhang and R. Cao, âMulti-objective optimization for UAV-enabled wireless powered IoT networks: An LSTM-based deep reinforcement learning approach,â IEEE Commun. Lett., vol. 26, no. 12, pp. 3019â3023, Dec. 2022.

[32] A. M. Seid, J. Lu, H. N. Abishu, and T. A. Ayall, âBlockchain-enabled task offloading with energy harvesting in multi-UAV-assisted IoT networks: A multi-agent DRL approach,â IEEE J. Sel. Areas Commun., vol. 40, no. 12, pp. 3517â3532, Dec. 2022.

[33] M. Fan et al., âDeep reinforcement learning for UAV routing in the presence of multiple charging stations,â IEEE Trans. Veh. Technol., vol. 72, no. 5, pp. 5732â5746, May 2023.

[34] R. Yang, X. Sun, and K. Narasimhan, âA generalized algorithm for multiobjective reinforcement learning and policy adaptation,â in Proc. Annu. Conf. Neural Inform. Proc. Syst., 2019, pp. 1â12.

[35] X. Chen et al., âInformation freshness-aware task offloading in air-ground integrated edge computing systems,â IEEE J. Sel. Areas Commun., vol. 40, no. 1, pp. 243â258, Jan. 2022.

[36] A. Abels, D. M. Roijers, T. Lenaerts, A. Nowâe, and D. Steckelmacher, âDynamic weights in multi-objective deep reinforcement learning,â in Proc. ACM Int. Conf. Mach. Learn., 2019, pp. 1â10.

[37] C. Liu, X. Xu, and D. Hu, âMultiobjective reinforcement learning: A comprehensive overview,â IEEE Trans. Syst., Man, Cybern. Syst., vol. 45, no. 3, pp. 385â398, Mar. 2015.

[38] H. Mossalam, Y. M. Assael, D. M. Roijers, and S. Whiteson, âMultiobjective deep reinforcement learning,â 2016, arXiv:1610.02707. [Online]. Available: http://arxiv.org/abs/1610.02707

[39] F. Song, H. Xing, X. Wang, S. Luo, P. Dai, and K. Li, âOffloading dependent tasks in multi-access edge computing: A multi-objective reinforcement learning approach,â Future Gener. Comput. Syst., vol. 128, pp. 333â348, Mar. 2022.

[40] K. Deb and H. Jain, âAn evolutionary many-objective optimization algorithm using reference-point-based nondominated sorting approach, Part I: Solving problems with box constraints,â IEEE Trans. Evol. Comput., vol. 18, no. 4, pp. 577â601, Aug. 2014.

[41] W. Xu, C. Chen, S. Ding, and P. M. Pardalos, âA bi-objective dynamic collaborative task assignment under uncertainty using modified MOEA/D with heuristic initialization,â Expert Syst. Appl., vol. 140, pp. 1â24, Feb. 2020.

[42] F. Song, H. Xing, S. Luo, D. Zhan, P. Dai, and R. Qu, âA multiobjective computation offloading algorithm for mobile-edge computing,â IEEE Internet Things J., vol. 7, no. 9, pp. 8780â8799, Sep. 2020.

[43] L. Cui et al., âJoint optimization of energy consumption and latency in mobile edge computing for Internet of Things,â IEEE Internet Things J., vol. 6, no. 3, pp. 4791â4803, Jun. 2019.

<!-- image-->  
Fuhong Song received the MEng degree in computer technology and the PhD degree in computer science and technology from Southwest Jiaotong University, Chengdu, China, in 2018 and 2022, respectively. He is currently a lecturer with the School of Information, Guizhou University of Finance and Economics. His research interests include mobile edge computing, multi-objective optimization, and reinforcement learning.

<!-- image-->

Mingsen Deng (Member, IEEE) is a professor of computer science with the School of Information, Guizhou University of Finance and Economics in China. He has published more the 100 papers in prestigious journals and distinguished international conferences. He has been an executive member of Technical Committee of High-Performance Computing of China Computer Federation since 2010, and received numerous awards, including Outstanding Scientists and Technologists of the Chinese Institute of Electronics (2020), One Hundred Person Project of the Guizhou Province (2016), Young Scientist Award of Guizhou Province (2018). His research interests focus on parallel and distributed computing, electronic structure calculations, and network analysis for Big-Data.

<!-- image-->

Huanlai Xing (Member, IEEE) received the PhD degree in computer science from the University of Nottingham (Supervisor: Dr Rong Qu), Nottingham, U.K., in 2013. He was a visiting scholar in computer science with the University of Rhode Island (Supervisor: Dr. Haibo He), USA, in 2020â2021. He is with the School of Computing and Artificial Intelligence, Southwest Jiaotong University (SWJTU), and Tangshan Institute of SWJTU. He was on editorial board of the Science China Information Sciences. He was a member of several international conference program and senior program committees, such as ECML-PKDD, MobiMedia, ISCIT, ICCC, TrustCom, IJCNN, and ICSINC. His research interests include semantic communication, representation learning, data mining, reinforcement learning, machine learning, network function virtualization, and software defined networking.

<!-- image-->

Yanping Liu received the BE degree in electronic and information engineering and the ME degree in communication engineering from Chongqing University, Chongqing, China, in 2006 and 2009, and the PhD degree in information and communication engineering from Southwest Jiaotong University, Chengdu, China, in 2018. He is currently an associate professor with the School of Big Data Statistics, Guizhou University of Finance and Economics. His research interests include game theory, learning theory, and optimization theory for the resource management on

UAV communication, and mmWave communication.

<!-- image-->

Fei Ye received the bachelorâs degree from the Chengdu University of Technology, China, in 2014, and the masterâs degree in computer science and technology from Southwest Jiaotong University, China, in 2018. He is currently working toward the PhD degree in computer science with the University of York. His research topics includes deep generative image models, lifelong learning, and mixture models.

<!-- image-->

Zhiwen Xiao received the BEng degree in network engineering from the Chengdu University of Information Technology, Chengdu, China, in 2019, and the MEng degree in computer science from the Northwest A & F University, Yangling, China, in 2023. He is currently working toward the PhD degree in computer science with Southwest Jiaotong University, Chengdu, China. His research interests include semantic communication, federated learning, representation learning, data mining, and computer vision.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O/page_9_img_1.png|page_9_img_1]]
2. [[../extracted_images/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O/page_18_img_1.jpeg|page_18_img_1]]
3. [[../extracted_images/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O/page_18_img_2.jpeg|page_18_img_2]]
4. [[../extracted_images/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O/page_18_img_3.jpeg|page_18_img_3]]
5. [[../extracted_images/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O/page_18_img_4.jpeg|page_18_img_4]]
6. [[../extracted_images/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O/page_18_img_5.jpeg|page_18_img_5]]
7. [[../extracted_images/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O/page_18_img_6.jpeg|page_18_img_6]]

---

