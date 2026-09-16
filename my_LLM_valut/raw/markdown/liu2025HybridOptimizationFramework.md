# A Hybrid Optimization Framework for Age of Information Minimization in UAV-Assisted MCS

Yuxin Liu, Qingyong Deng , Senior Member, IEEE, Zhiwen Zeng , Anfeng Liu , and Zhetao Li , Member, IEEE

AbstractâUAVs-enabled Mobile Crowdsensing (UMCS) has gained considerable attention recently, but it is challenging to meet the data collection needs of the entire city using only the UAV with limited energy. Furthermore, how to effectively minimize Age-of-Information (AoI) and ensure data quality has not been well solved in previous studies. Therefore, this paper proposes a hybrid optimization framework for AoI minimization, which recruits massive distributed workers as the main force for data collection, while the UAV acts as a data collection collaborator and is more inclined to fly to the SNs that cannot establish connections with workers, To mitigate the potential security threats incurred by dishonest workers of the MCS system, we first provide a Greedybased Multi-worker Task Assignment (GMTA) strategy, aiming to assign more urgent data collection tasks to reliable workers under workload constraints. Then, we propose a Deep-Reinforcement-Learning-based Global AoI Minimization (DRL-GAM) strategy for the UAV path planning to find a set of optimal actions to minimize the global AoI. Based on the real dataset, our simulation experiments show that compared with traditional strategies, our DRL-GAM strategy can reduce the global AoI by an average of 6.49%â¼68.21% in various network sizes, and is more stable for the average standard deviation is only 51.75% of other strategies.

Index TermsâAge of information, data collection, deep reinforcement learning, unmanned aerial vehicles.

## I. INTRODUCTION

M OBILE Crowdsensing (MCS) enlists mobile workers tocarry out diverse data collection tasks by leveraging the carry out diverse data collection tasks by leveraging the sensing devices they carry, such as mobile phones, wristbands, and wearables, which has been widely studied [1], [2]. This mode has the advantages of wide range and low cost. However, the biggest shortcoming of such data collection mode is that most of the sensed data are of general type and the data type is relatively single, which is determined by the sensing devices carried by workers [2]. Since the actual network needs a variety of specialized, complex data, it is often necessary to deploy a large number of professional sensing nodes (SNs) (or devices) for sensing and monitoring a large number of physical phenomena according to different applications [3], [4]. At present, many professional SNs are widely deployed in areas that need to be monitored, forming the basis of various emerging applications [4], [5]. However, collecting data from such a large number of SNs deployed on demand faces huge challenges. SNs have their own communication device, which can easily upload sensed data to the data center (or platform) at any time through 4 G/5 G communication technology and internet communication [6]. However, the sensed cost of this way is expensive, one is that the SNs hardware increases the cost of communication equipment. Studies have pointed out that if a large number of SNs with simple hardware and low cost are deployed in cities, the cost will be doubled if communication devices are added to them [6]. Second, the communication cost is expensive. This mode needs to pay the communication cost to the communication company, and the long-term communication cost is even much higher than the cost of equipment hardware [6]. Therefore, many deployed SNs are often relatively simple in structure in the actual network, and do not have the ability of long-distance communication with the internet [6]. So, it is a challenging issue how to collect the data of these vast SNs without long distance communication conditions. There are two types of data collection models for such network. One is feasible to provide the opportunistic connection between SNs and applications through Unmanned aerial vehicles (UAVs) [7], [8]. When UAVs move close to the SNs, the SNs offload the stored data to the UAVs through a temporary connection [7], [9]. The UAV characterized with wide coverage and high mobility provides new opportunities for supporting data collection [5], [9], which has the advantages of high agility, high flexibility, and low cost [8], [9]. This data collection model is called as the UAVs-enabled Mobile Crowdsensing (UMCS) system. However, there are potential functional limitations for purely UMCS, mainly energy constraints. This means that the UAV must be recharged frequently, which is particularly unsuitable for large-scale continuous data collection [7], [9]. The other model is worker-based Mobile Crowdsensing (WMCS) in which workers are recruited as mobile data collectors to collect sensed data of SNs [1], [2]. WMCS in this paper is an extension of the commonly study of MCS. In a typical MCS, workers use their own sensing devices to sense data. In the WMCS, workers can not only use their own sensing devices to sense data, but also move to the task area to establish a connection with the SNs, and then report the data to the data center. The numerical superiority of workers makes the improvement of data collection efficiency extremely significant [1], [2]. However, purely WMCS still can not meet the practical application of the network, due to many SNs may be deployed in disaster scenarios such as floods and fires, or hostile areas of military systems with sensors in which workers are hard to reach [7], [8]. It is challenging to deploy stable communication facilities in these scenarios, and the communication between SN is often blocked due to obstacles or channel interference [7], [8]. It can be seen that both purely UMCS and purely WMCS are difficult to meet the needs of practical applications in the actual network.

Besides, Age-of-Information (AoI) is another important issue for data collection in real networks [10]. It is coined to represent the freshness status of update data [11], [12], [13], which is a metric to characterize the latency in status updating systems and applications [14], [15]. The lower AoI means that the collected data is more consistent with the current status, and applications can respond and control more appropriately to events [16], [17] , so, the more valuable the data will be. Therefore, how to minimize the AoI becomes an important research issue in MCS [18], [19].

We argue that combine UMCS and WMCS well, so as to establish a hybrid data collection mode which will be a low-cost and good-performance mode. We call such hybrid data collection mode as UAV-assisted Mobile Crowdsensing System (UaMCS), which recruits low-cost workers to do as many data collection tasks as possible. For tasks that workers cannot reach the task position or no workers are willing to perform, we will dispatch the UAV to collect data [7], [8]. In this way, most tasks are performed by employing workers [1], [2], while the UAV assists a small number of tasks that workers cannot complete or cannot complete in time, so as to achieve the effect of low cost and AoI optimization [18], [19]. It is a natural thought, however, to the best of our knowledge, there are still no valid studies similar to the one we proposed. The reason lies in the following key issues are not well addressed:

(1) The data quality is an everlasting issue in AoIminimization data collection method. If the data collector is trustworthy and the data reported by workers are all true, it means its quality is guaranteed [11], [12], [18]. Such an assumption is valid in UMCS, due to the fact that UAVs are sent from the platform, and UAVs are credible, that is, UAVs will truthfully fly to the communication range of SNs to collect real data [7], [8]. However, this is not necessarily true in WMCS. Many studies have pointed out that because workers consume resources, time and energy to perform tasks, some dishonest or malicious workers are failing to report data or intentionally submitting false data, which can easily lead to misperception of the network environment [2], [20]. Therefore, researchers usually design some trustworthy policies to assign tasks to trusted workers for MCS [21], [22]. However, there is no AoI-minimization data collection method can ensure data quality for UaMCS, which will be solved in this paper.

(2) Considering the credibility of workers, the previous methods of minimizing AoI cannot be applied, so it is urgent to establish new data collection strategies for UaMCS. Many AoIminimization data collection methods have been proposed, but all assume that the data reported by workers is true [18], [19]. Even worse, if the data reported by the workers are false, making it more challenging to estimate the AoI [9], [18]. If workers report false data or even malicious data, no data is collected for this task, and its AoI is infinite. If it is malicious data, it will further harm the entire system. Therefore, the traditional research that calculates and minimizes AoI based on the time of receiving data once the data is received, which is not in line with the actual network.

(3) Efficiently assigning tasks to the UAV or workers and minimizing AoI is a challenging issue in UaMCS. On the whole, workers are mainly active in urban hotspots. For areas with poor infrastructure (e.g., areas without roads, forests, or mountains) or the outskirts of the city, the possibility of workers undertaking tasks will reduce significantly [7]. Therefore, it is natural that the UAV is mainly used for data collection in remote areas, and workers are mainly used for data collection in hotspots [7]. However, the practical task allocation for minimizing AoI in UaMCS is very complex. After the platform makes an announcement to recruit workers for tasks, in order to minimize AoI, UAVs are usually dispatched after the earliest possible assignment is determined. However, workers respond dynamically to tasks, which leads to many different situations: (a) The task which had no workers to undertake at first have recruited the willing workers after the UAV dispatched, at this time the UAV does not need to perform the task, so it is necessary to dynamically adjust the flight trajectory of the UAV. (b) Some tasks that had been assigned to workers could not be performed due to breach of contracts or other reasons, which required increasing the number of tasks to be performed by the UAV and adjusting its flight trajectory. (c) Taking worker trust and the quality of tasks into account, it is often necessary to dynamically adjust the UAVâs flight trajectory so that the platform can obtain the highest quality data possible and quickly identify worker trust. Therefore, it is a very challenging issue to design dynamic and multi-objective optimization strategies for dynamic task allocation.

In response to the above challenges, this paper proposes a novel data collection framework that organically combines the ability of the UAV to quickly respond to changes and the numerical superiority of the workers to bear the majority of data collection at low cost, thus realizing the rapid data collection and minimizing the AoI. The main innovations in this paper are as follows.

1) We propose an integrated hybrid optimization framework for AoI minimization, where the UAV and massive workers are complementary data collectors. The workers achieve fast data collection in the city hot-spots with the numerical advantage, while the UAV will cooperate with these workers to collect data in the peripheral areas. In addition, the UAV can evaluate the workers based on our proposed trust evaluation model, thereby improving the accuracy of AoI estimation.

2) A Greedy-based Multi-workers Task Assignment (GMTA) strategy is proposed, aiming to select more credible workers based on the trust model to perform more urgent data collection tasks under the workload constraints, thereby quickly and reliably reducing the AoI of SNs in each cell.

3) A Deep-Reinforcement-Learning-based Global AoI Minimization (DRL-GAM) strategy is proposed for the UAV, aiming to find a set of optimal actions that minimize AoI based on the estimated AoI reflected by the current workerâs performance within the energy constraint. Specifically, we first model this problem as a Markov Decision Process (MDP), then optimize our problem based on the network D3QN by combining two original networks Dueling DQN and Double DQN.

The remainder of this article is organized as follows: Section II introduces the related works. Section III presents the system

model and problem formulation. Then, the proposed hybrid optimization for AoI minimization is designed in Section IV. The performance and related analysis are presented in Section V. Finally, Section VI provides the limitations of our work and relevant conclusions.

## II. RELATED WORKS

In this section, the overview of the data collection model is presented first. Then, the UAV-enabled AoI-aware data collection model and the worker-enabled data collection model are analyzed in detail respectively.

## A. The Overview of the Data Collection Model

Generally, the MCS system consists of three parts: workers, the platform, and data requester [1], [2]. The main process of data collection is as follows: The data requester submits the time, location and other performance indicators of sensed data tasks to the platform. Then the platform publishes tasks. Workers mainly refer to those who carry sensing device. After they are informed of the task by the platform, if they are willing to do the task, they will apply to the platform for the task [1], [2]. The platform recruits workers to do tasks and obtain data, and then sends the data to the data requester to complete the whole data collection process. This kind of data collection mode has the characteristics of low cost, wide collection range and sustainability, so it has been widely studied and concerned [1], [2]. However, the shortcoming of this data collection mode is that the sensed data often depends on the sensing device carried by the worker, so the data type is relatively simple. The most commonly used sensing device is the mobile phone, which can sense sound, images, text and other data [1], [2]. In practice, specialized sensing devices are often needed to sense professional data, such as all kinds of professional sensing devices that sense physical phenomena [6]. According to the study of Bonola et al. [6], a large number of sensing devices are deployed on bridges, large buildings and roadside devices such as street lights and garbage bins to monitor and sense the operating status of these infrastructures. In such applications, these sensing devices are relatively inexpensive, and have simple hardware, which can be deployed to the monitored devices in large numbers at any time to sense data [6]. However, these sensing devices only have short-range communication capability and cannot communicate with the Internet. Therefore, how to collect data from these sensing devices cheaply and efficiently is a challenging issue. Bonola et al. [6] believe that the existence of a large number of mobile vehicles in cities is a kind of mobile workers, so these mobile vehicles can act as data mules to be recruited for data collection. When mobile vehicles move near sensing devices, sensing devices transmit their sensed data to them, which can report the data to the platform [6]. This kind of data collection model has a wide range of application scenarios such as Supervisory Control and Data Acquisition (SCADA) system [23], [24]. The SCADA system is based on the need of application to deploy some sensing devices in the monitoring area [23], [24]. For example, in the study of wild animals, sensing devices need to be deployed in areas where wild animals may appear to detect the behavior of wild animals [25]. These areas are difficult for people to reach and do not have communication infrastructure, or are extremely expensive to deploy communication lines [25]. Say et al. [26] proposed a priority-based data gathering framework in UAV-enabled wireless sensor networks. In this framework, when the UAV flies over the sensing devices, the sensing devices within the communication range can send data packets to the UAV, so that the data of these sensing devices can be collected to the platform [25], [26]. In the edge computing proposed in recent years, the research on sending UAVs to fly over the sensing devices and offloading tasks to edge servers with stronger computing capability [27] is similar to the data collection in this paper. In this paper, the UAV relays data instead of tasks, and does not require the ability to sense data. Here, the main function of the UAV is to move to the communication range of sensing devices and relays data of the sensing devices to the platform. As can be seen from the above discussion, workers hold the sensing devices and the sensed data can be uploaded to the platform in the typical MCS [1]. However, there are limits to the application of this data collection model. Then traditional MCS will be expanded when workers move within the range of the sensing devices for data collection [6]. In the above methods, there are sensing devices that cannot be reached by workers (or mobile vehicles) and data cannot be collected. Obviously, the UAV has greater flexibility and can obtain data from the sensing devices that workers cannot reach [7], [8]. So we argue that UAVs are relatively expensive, while workers are relatively cheap, and they can also move to the area where the task is located for data sensing and collection from the sensing device. Therefore, the combination of workers and UAVs to form a new UaMCS is an effective data collection model.

## B. UAV-Enabled AoI-Aware Data Collection

The research on UAV-enabled data collection is pervasive, and its core is to find the optimal flight trajectory under the constraint conditions (e.g., battery capacity) to achieve specific research goals (e.g., AoI, delay, energy consumption, path loss rate, and path length). According to the path planning algorithms, early proposed UAV-enabled data collection strategies often used bio-inspired algorithms such as heuristic algorithms [13], Genetic Algorithm (GA) [22], Particle Swarm Optimization (PSO) algorithm [28]. Hu et al. [13] decomposed the problem of minimizing the average AoI into two subproblems: time allocation of data collection and trajectory planning for the UAV. They searched for the optimal trajectory by combining classical dynamic programming and ant heuristic colony algorithm. Luo et al. [29] first studied the lower bound of the AoI minimization problem, then modeled the trajectory planning problem on a square grid graph that contains only one Hamilton cycle, and proposed a tree-search algorithm to search for the optimal trajectory, which can achieve the average AoI minimization in polynomial time.

Recently, machine learning-based intelligence methods have emerged, such as Deep Reinforcement Learning (DRL) based strategies [17]. DRL is one of the most critical strategies for AoI optimization [17]. Most of them modeled the AoI minimization problem as a MDP [25], [29], [30], [31], or an integer programming problem [32], and then implemented the path planning based on different DRL frameworks and backgrounds. Based on the Deep Q-Network (DQN), Tong et al. [30] proposed an optimization policy for flight path planning, which can minimize the average AoI of SNs while maintaining their low packet loss rate. Sun et al. [33] proposed a Twin Delayed Deep Deterministic (TD3) strategy based on Deep Deterministic Policy Gradient (DDPG) algorithm under the constraints of UAV propulsion energy and SN transmission energy, and the optimal UAV speed, direction, and channel allocation by the neural network can be obtained in real-time.

Ferdowsi et al. [17] decomposed the Normalized Weighted Sum of AoI (NWS-AoI) optimization problem into two subproblems. First, they estimated the update time and trajectory of SNs based on Convex Optimization (CO). Then, based on the MDP with finite state and action space, a neural-combinatorialbased algorithm was proposed to find the optimal hybrid solution of flight path and update packet scheduling.

## C. Worker-Enabled Data Collection

Recruiting workers for data collection has been widely used in MCS [34], [35]. The general process is that first the platform publishes the collection scope, time, type, and reward as a task, then workers perform the task and report data to the platform. Zhou et al. [35] proposed a Contributor-Initiated Proactive Sensing (CIPS) system for large-scale sensing and data collection. Such data collection model has been extensively studied in Ref. [1], [2]. The data sensed by workers through their own sensing devices is essentially the same as the data collected by employing workers in the communication range of mobile SNs, so this paper will not make any distinction in the following discussion. In this case, there are two issues worth studying. One issue is to obtain high quality data [2], [21], [36], another is minimizing AoI that few researches concentrate on.

The first critical challenge is to ensure data quality, while securing data in MCS is also a very challenging issue. This is because some dishonest or malicious workers do not collect data sincerely but report false data to defraud the reward [2], [21]. Researchers have proposed many solutions to infer data authenticity from different data sources [2], [21], [36]. In earlier studies, the platform was assumed to know the quality of workers in advance, so that high-quality data can be obtained by selecting high-quality workers [36]. Subsequent research has found that this assumption does not hold up in practice. Instead, it is assumed that once the platform receives the data reported by the workers, it can evaluate the quality of the submitted data, and thus evaluate the quality of the workers based on the quality of the data [1]. The idea is that if a worker always submits high-quality data, he/she is considered as a trusted worker, and vice versa [2], [37]. In such method, the platform will evaluate the workers according to the quality of the data after receiving the data, and then select high-quality workers to collect the data, so as to ensure the quality of the data. The classic study of this kind is the Multi-Armed Bandit (MAB) based data collection strategy [1]. However, recent research has found that because of the so-called Information Elicitation Without Verification (IEWV) problem in MCS [38], even if the platform receives the workersâ data, it still does not know the data quality. This situation makes it particularly difficult for MCS to obtain highquality data. Currently, a popular solution method is Conflict Resolution on Heterogeneous (CRH) [39]. In the CRH method, if the workerâs data is closer to the final result, the greater the weight. Most workers in the network are believed to be trustworthy, so the result obtained by weighting the data of k workers is relatively close to the true value [39]. However, this approach can hardly guarantee data quality in practice. As long as there are dishonest workers among the k recruited workers, the final data quality will be relegated. Malicious workers can use the method of collusion attack to attack system, and as long as the number of malicious workers reaches k/2 or more, the strategy will be completely invalid. To this end, a trust-based worker recruitment method is proposed to guarantee data quality, the key of which is to effectively identify trusted workers and select out for data collection [2], [21]. The method of worker trust evaluation is to compare the data of workers whose trust is uncertain with the data reported by trusted workers to change the trust of identified workers. The second critical challenge is to minimize AoI while maintaining data quality, which has not been effectively studied. In previous studies, data quality and Aol were optimized separately, and the single data collectionmodel was often considered, which limited its performance to some extent. Hybrid data collection mode of the UAV and workers can enhance system performance but has been less studied due to its design complexity. Therefore, this paper proposes a hybrid Aol optimization framework to both improve data quality and minimize Aol for UaMCS which is of great significance.

<!-- image-->  
Fig. 1. The hybrid data collection network model, including the data collectors (workers and UAV), Sensing Nodes(SNs).

## III. SYSTEM MODEL AND PROBLEM FORMULATION

This section will introduce the system architecture and our research objectives, including the basic network, communication, trust evaluation, AoI, and energy models. Finally, we present our research problem and derive two subproblems.

## A. Network Model

Our network model is shown in Fig. 1. There are three main components: The data collectors, the sensor nodes (SNs), the data center [2]. The data collectors mainly include a programmable UAV and massive task-assignable workers. People carrying sensing or communication equipment (workers), as well as mobile sensing devices such as mobile vehicles, can act as data collectors. The main function of the UAV is to collect data of tasks that workers cannot reach or that no workers are willing to perform [7], [8]. The SNs mainly mean that devices of sensing data which do not have the ability to communicate with the Internet, so their sensing data are stored in their memory. When workers or the UAV move within their communication range, sensing data will be relayed to the data center. The data center is the final destination of the data, and is responsible for the worker recruitment and the trajectory planning and data collection of the UAV.

Since the UAV flies over a cell, it can collect the data of the SNs in the entire cell. Therefore, similar to Ref. [9], [27], we divide the monitoring area into multiple cells, which are the basic unit of data collection for the UAV. According to the geographical location, ground space is decomposed into many regular hexagonal cells. We use $c \in C$ to denote a logical cell c belonging to observed cells C, where $c = [ x , y ] \in \mathbb { N } ^ { \breve { 1 } \times 2 }$ denotes its number in the x and y directions. The center point of each cell is defined by $l _ { c } = [ p _ { c } , q _ { c } ] \in \mathbb { R } ^ { 1 \times 2 }$ , where $p _ { c }$ and $q _ { c }$ can be calculated by (1) and (2), where b is the side length of the cell.

$$
p _ { c } = { \left\{ \begin{array} { l l } { { \sqrt { 3 } } b x } & { \quad { \mathrm { i f ~ } } x { \mathrm { ~ i s ~ o d d } } , } \\ { { \sqrt { 3 } } b x + { \sqrt { 3 } } b / 2 } & { \quad { \mathrm { e l s e } } . } \end{array} \right. }\tag{1}
$$

$$
q _ { c } = 3 b y / 2\tag{2}
$$

The SNs are defined by $\mathcal { N } = \{ n | n = 1 , 2 , . . . , N \}$ , where N represents the number of SNs. In fact, they also represent the location of the task. If SNs are deployed at the location of the tasks, they sense specialized data, else workers or the UAV can also use their own sensing devices to sense and collect common data when they arrive at the location of the task. As a subset of $\mathcal { N } , \mathcal { N } _ { c } \subseteq \mathcal { N }$ represents the SNs belonging to cell c that satisfies $\begin{array} { r } { \mathcal { N } = \bigcup _ { c \in C } \mathcal { N } _ { c } } \end{array}$ . In addition, a virtual cell $c ^ { \mathrm { { \acute { o u t } } } }$ is used to represent the cells beyond the observed cell, satisfying $N _ { c \mathrm { o u t } } = \emptyset$ . A feature set $u _ { t }$ is used to describe the state of the UAV at timeslot t, denoted by $\boldsymbol { u } _ { t } = \{ \mathcal { C } _ { t } , E _ { t } , c _ { t } ^ { \mathrm { u a v } } , a _ { t } \} . ~ \mathcal { C } _ { t } \in \{ 0 , 1 \}$ represents the charge state. If the UAV is charging, $\mathcal { C } _ { t } = 1$ , otherwise $\mathcal { C } _ { t } = 0 . \bar { E } _ { t } \in ( 0 , E _ { \operatorname* { m a x } } ]$ is the residual energy, where $E _ { \mathrm { m a x } }$ is the maximum energy determined by the battery device. $c _ { t } ^ { \mathrm { u a v } } \in C$ indicates the cell where the UAV is currently located. $a _ { t } \in A$ indicates the movement action of the UAV, where A is the action space as shown in (3), indicating that the UAV can only move to six adjacent hexagonal cells or hover over the current cell.

$$
A = \{ [ 0 , - 1 ] , [ 1 , - 1 ] , [ 1 , 0 ] , [ 1 , 1 ] , [ 0 , 1 ] , [ - 1 , 0 ] , [ 0 , 0 ] \} .\tag{3}
$$

We use $\mathcal { M } = \{ m | m = 1 , 2 , . . . , M \}$ to represent workers, and a feature set $m _ { t } = \{ T _ { m , t } , L _ { m , t } , c _ { m , t } , k _ { m , n , t } \}$ to describe the state of worker m at timeslot t. $T _ { m , t } \in [ 0 , 1 ]$ is the trust value obtained by the trust evaluation model to evaluation the expectation that a task will be successfully completed. $c _ { m , t } \in \bar { C } \cup c ^ { \mathrm { o u t } }$ is the current cell of the worker. $L _ { m , t } \in \mathbb { N }$ represents the number of tasks that the worker can carry, $L _ { m , t } = 0$ means that no more tasks can be assigned to it. $k _ { m , n , t } \in \{ 0 , 1 \}$ indicates whether the task of collecting SN n should be assigned to worker $m ,$ 1 means yes and 0 means no.

## B. Communication Model

Based on the grid model [27], the position of the UAV in each timeslot is assumed to be the center of the current cell, so we use H to represent the altitude. For the SN n in cell $c ,$ we denote its position by $o _ { n , c } = [ p _ { n , c } , q _ { n , c } ] \in \mathbb { R } ^ { 1 \times 2 }$ . When the UAV moves to cell $c ,$ its distance from the SN n is given by (4).

$$
d _ { n , c } = \sqrt { H ^ { 2 } + \parallel o _ { n , c } - l _ { c } \parallel _ { 2 } } .\tag{4}
$$

The communication channel between the UAV and SNs is generally modeled as a Line-of-Sight (LoS) propagation model [25]. (5) gives the probability of establishing a LoS channel.

$$
P _ { n , c } ^ { \mathrm { L o S } } = \frac { 1 } { 1 + \zeta \exp [ - \varpi ( \psi - \zeta ) ] ^ { \prime } } .\tag{5}
$$

Where Î¶ and  are determined by the communication environment, and $\begin{array} { r } { \psi = \frac { 1 8 0 } { \pi } \sin ^ { - 1 } { \frac { H } { d _ { n , c } } } } \end{array}$ represents the elevation angle. The probability of establishing a NLoS channel is $P _ { n , c } ^ { \mathrm { N L o S } } =$

DH: Datapacket Header HC: Hash Codes of data  
<!-- image-->  
Fig. 2. The trust evaluation model mainly consists of the direct trust and the recommendation trust.

$1 - P _ { n , c } ^ { \mathrm { L o S } }$ . Therefore, the path loss can be obtained by (6).

$$
\begin{array} { c l c r } { { } } & { { \displaystyle K _ { n , c } = \frac { P _ { n , c } ^ { \mathrm { L o S } } K _ { 0 } ( d _ { n , c } ) ^ { - \zeta } } { \eta _ { 1 } } + \frac { ( 1 - P _ { n , c } ^ { \mathrm { L o S } } ) K _ { 0 } ( d _ { n , c } ) ^ { - \zeta } } { \eta _ { 2 } } } } \\ { { } } & { { } } \\ { { } } & { { = \overline { { { P } } } _ { n , c } ^ { \mathrm { L o S } } K _ { 0 } ( d _ { i } ^ { c } ) ^ { - \zeta } . } } \end{array}\tag{6}
$$

$\begin{array} { r } { \overline { { P } } _ { n , c } ^ { \mathrm { L o S } } = \frac { 1 } { \eta _ { 1 } } P _ { n , c } ^ { \mathrm { L o S } } + \frac { 1 } { \eta _ { 2 } } ( 1 - P _ { n , c } ^ { \mathrm { L o S } } ) } \end{array}$ is the average probability of establishing a LoS channel, where $\eta _ { 1 }$ and Î·2 are the path loss coefficients of the LoS and NLoS channels, respectively [25]. The coefficient $K _ { 0 } = ( 4 \pi f _ { c } / c ) ^ { - \zeta }$ is the path loss when the distance is 1 m, where $f _ { c }$ is the carrier frequency and c represents the speed of light. Based on this, the transmission rate can be obtained through Shannonâs theorem, as shown in (7). Here, B is the channel bandwidth, $P _ { T }$ is the transmit power, and $N _ { 0 }$ is the white noise power.

$$
r _ { n , c } = B \log _ { 2 } \left( 1 + \frac { P _ { T } K _ { n , c } } { N _ { 0 } } \right)\tag{7}
$$

Therefore, the duration of each timeslot in seconds can be obtained from (8), where v represents the UAVâs flight speed, B is the message size in bits, and $r _ { \mathrm { m i n } }$ represents the minimum transmission rate in cells.

$$
\Delta t = \operatorname* { m a x } { \left( \frac { \sqrt { 3 } b } { v } , \frac { B N } { r _ { \operatorname* { m i n } } | C | } \right) }\tag{8}
$$

## C. Trust Evaluation Model

Trust mechanism is one of the feasible methods to evaluate interaction and behavior. The trust value is usually clamped between 0 and 1. The closer it is to 1, the more likely its behavior is to match expectations. In our model, the UAV is managed by the data center, so it is entitled to the highest trust, i.e., 1. The trust evaluation model is illustrated in Fig. 2. In this model, the trust evaluated by the UAV is direct trust, while the trust evaluated by mutual interaction between workers is recommendation trust.

1) Direct Trust: As shown in Fig. 2, the data collected by the UAV can be treated as a baseline standard to evaluate workers. As mentioned in Ref. [22], the UAV can verify the data authenticity according to matching the hash codes of historical data stored in the SN with the data reported by workers. The validation process is briefly described as follows: Suppose that workers a, b and $c ,$ as well as the UAV in slots $t _ { 1 } , t _ { 2 } , t _ { i } , t _ { n }$ collect the data of the same SN in Fig. 2, when workers and the UAV collect data, the SN sends the stored data as well as corresponding hash codes to data collectors. In Fig. 2, the UAV collects the data at the nearest time to the current time, so the data sent from SN including hash codes in the slots $t _ { 1 } , t _ { 2 } , t _ { i }$ . Considering that the UAV is credible, we can use its hash codes in slot $t _ { 1 }$ to verify whether the data reported by worker a is true. If it is true, it is a successful verification. Otherwise, it is a failed verification.

Also, the data from the UAV can verify the data authenticity of worker b, worker c in the solts $t _ { 2 }$ and $t _ { i }$ . Since the UAVâs data is considered to be true, the worker trust verified by using it is direct trust.

We store such successful verifications $s _ { * } \in \mathbb { N }$ and failed verifications $f _ { * } \in \mathbb { N }$ in record sets $\boldsymbol { s }$ and $\mathcal { F }$ respectively. Assuming that the capacities of S and $\mathcal { F }$ are both $W ^ { \mathrm { d i r e c t } }$ , the direct trust of worker m can be obtained by (9).

$$
T _ { m } ^ { \mathrm { d i r e c t } } = \frac { 1 } { 2 } \frac { 2 \sum _ { s _ { * } \in S _ { m } } s _ { * } + 1 } { \sum _ { s _ { * } \in S _ { m } } s _ { * } + \sum _ { f _ { * } \in \mathcal { F } _ { m } } f _ { * } + 1 } ,\tag{9}
$$

Initially, both $\boldsymbol { s }$ and $\mathcal { F }$ are empty sets. The initial value of direct trust is 0.5, due to uncertain expectations. As the successful or failed verifications are recorded, the direct trust will approach 1 or 0. When the size of S and $\mathcal { F }$ reaches $W ^ { \mathrm { d i r e c t } }$ , the earliest stored record will be removed.

2) Recommendation Trust: Recommendation trust is evaluated by matching the hash code of reports from different workers on the same SN in the same time slot, called a virtual interaction. As shown in Fig. 2, worker c and b collect the data of the same SN respectively in the slot $t _ { i }$ and $t _ { 2 }$ . Data from worker c contains the hash code of SN in the slot $t _ { 2 }$ . Although worker c and b do not have interaction, the platform can verify the correctness of worker bâs data in slot $t _ { 2 }$ based on the hash code collected by worker c. In this way, the data collected by different workers on the same SN in the same slot can be verified, which is equivalent to the virtual interaction between workers. This kind of trust relationship derived based on verification between workers is called recommendation trust. Specifically, if worker c is a high-trust worker and its data is used to check whether worker b is trusted, the result will be more likely to be true. Therefore, recommendation trust plays a role in speeding up trust calculation and helps the system select trusted workers quickly. Each worker has an interaction record set $\mathcal { R }$ , whose capacity is W recom. Each element in R is a tuple consisting of the trust of the interacting worker $T \in [ 0 , 1 ]$ and the interaction result $I \in \{ 0 , 1 \}$ , where $I = 1$ means that the hash codes provided by the two workers are consistent, otherwise, $I = 0 .$ . Similarly, when the size of R grows to W recom, the oldest record will be removed. The recommendation trust is obtained by (10).

$$
T _ { m } ^ { \mathrm { r e c o m } } = \frac { \sum \langle T , I \rangle \in \mathcal { R } _ { m } } { \sum \langle T , I \rangle \in \mathcal { R } _ { m } } T .\tag{10}
$$

To prevent the division error, if R is empty, $T _ { m } ^ { \mathrm { r e c o m } } = 0 . 5$ Finally, as shown in (11), the two trusts are weighted to obtain the total trust, where Ï is the weight of the direct trust.

$$
T _ { m } = \rho T _ { m } ^ { \mathrm { d i r e c t } } + ( 1 - \rho ) T _ { m } ^ { r e c o m }\tag{11}
$$

## D. AoI Model

The AoI emphasizes the update characteristics of SNs, which represents whether the fresh data of the SN can be collected and forwarded to the data center in time. In other words, how long has the SN not been update since the last collection, or the freshness of the last collected data. A lower AoI means fresher perception data, which provides a data basis for quick response. The AoI of the SN n is generally defined by (12), where $\tau _ { n }$ represents the time stamp of the last sampling.

$$
z _ { n , t } = t - \tau _ { n } ,\tag{12}
$$

Due to the variability of the network environment, including channel uncertainties (e.g., channel fading, Doppler shift) and behavior uncertainties (e.g., fail to submit task), it is not easy to ensure the accuracy of $\tau _ { n } .$ . Therefore, we use the trust evaluation model to estimate and update the sampling timestamp by (13), where $\begin{array} { r } { 1 - \prod _ { \stackrel { { m \in \mathcal { M } } } { k _ { m , n , t } = 1 } } \big ( 1 ^ { \circ } - T _ { m } \big ) } \end{array}$ represents the expectation that at least one worker successfully samples and reports the data from SN n.

$$
\tau _ { n } \gets ( t - \tau _ { n } ) \cdot \left[ 1 - \prod _ { { m \in \cal { M } } \atop { k _ { m , n , t } = 1 } } ( 1 - T _ { m } ) \right] + \tau _ { n } .\tag{13}
$$

For the cell $c \in C .$ it contains an indefinite number of SNs, each of which is estimated according to (12). Therefore, the cell AoI can be obtained by (14).

$$
g _ { c , t } = \sum _ { n \in \mathcal { N } _ { c } } z _ { n , t } .\tag{14}
$$

By summing the AoI of each cell and dividing by the total number of SNs, the global AoI can be calculated, i.e,

$$
G _ { t } = \frac { \sum _ { c \in C } g _ { c , t } } { N } .\tag{15}
$$

## E. Energy Model

The energy of a UAV is mainly consumed in maintaining flight and communication. For flight energy consumption, we refer to Ref. [40]. As shown in (16) and 17, the flight energy consumption includes the drag power $P _ { \mathrm { d r a g } }$ for overcoming the parasitic drag, and the lift power $P _ { \mathrm { l i f t } }$ for defying gravity. Here, $C _ { \mathrm { d r a g } }$ is the aerodynamic drag coefficient, $A _ { \mathrm { { f r o n t } } }$ is the front-facing area in $m ^ { 2 }$ , $D _ { \mathrm { a i r } }$ is the air density in $k g / m ^ { 3 }$ , v is the relative speed through the air in $m / s , W _ { \mathrm { u a v } }$ is the weight of the UAV in $k g ,$ and $d _ { \mathrm { u a v } }$ is the width of the UAV in meters. For the communication power $P _ { \mathrm { c o m m } } ,$ , we mainly refer to Ref. [25], which is related to the hardware device.

$$
P _ { \mathrm { d r a g } } = \frac { 1 } { 2 } C _ { \mathrm { d r a g } } A _ { \mathrm { f r o n t } } D _ { \mathrm { a i r } } v ^ { 3 } ,\tag{16}
$$

$$
P _ { \mathrm { l i f t } } = \frac { W _ { \mathrm { u a v } } ^ { 2 } } { D _ { \mathrm { a i r } } ( d _ { \mathrm { u a v } } ) ^ { 2 } v ^ { \prime } } ,\tag{17}
$$

In addition, the UAV needs to be charged regularly for continuous flight. We use $P _ { \mathrm { c h a r g e } }$ to represent the charging power, which is related to the battery device. We can obtain the UAVâs energy change $\Delta E _ { c }$ in cell $c ,$ as shown in (18).

$$
\begin{array} { r l } & { \Delta E _ { c } = } \\ & { \left\{ \begin{array} { l l } { - ( P _ { \mathrm { d r a g } } + P _ { \mathrm { l i f t } } ) \Delta t - P _ { \mathrm { c o m m } } \sum _ { n \in \mathcal { N } _ { c } } \mathcal { B } / r _ { n , c } } & { \mathrm { m o v e } , } \\ { - P _ { \mathrm { l i f t } } \Delta t - P _ { \mathrm { c o m m } } \sum _ { n \in \mathcal { N } _ { c } } \mathcal { B } / r _ { n , c } } & { \mathrm { h o v e r } , } \\ { P _ { \mathrm { c h a r g e } } \Delta t } & { \mathrm { c h a r g e } . } \end{array} \right. } \end{array}\tag{18}
$$

## F. Problem Formulation

Since the UAV can be dispatched to a specific cell in a targeted manner to quickly collect data, while the data collection of workers can be performed by task assignment, the policies they adopt are different.

We use $\Gamma = \langle \pi _ { \mathrm { u a v } } , \pi _ { \mathrm { w o r k e r } } \rangle$ to represent the policy in each timeslot, where $\langle \pi _ { \mathrm { u a v } } , \pi _ { \mathrm { w o r k e r } } \rangle$ is a tuple composed of the movement policy for the UAV and the task assignment policy for workers at the timeslot t.

$$
\mathbf { P } : \operatorname* { m i n } _ { \Gamma } \mathbb { E } _ { t } [ G _ { t } ] ,
$$

$$
\mathrm { s . t . } \mathrm { C 1 } : t \in \{ 1 , 2 , . . . , t _ { \operatorname* { m a x } } \}\tag{19}
$$

Our problem can be initially expressed by P, i.e., we should adopt a feasible policy in each timeslot to minimize the expectation of global AoI during the systemâs operation. According to the type of data collectors, P can be further involved into two subproblems, i.e., the path planning problem for the UAV and the task assignment problem for the workers.

1) Path Planning Problem for the UAV: In this paper, we adopt the hierarchical hexagonal cell model mentioned in the network model to simplify the movement and collection process. It can be assumed that the UAV can complete the data collection of all SNs in the cell in a timeslot and move to the next cell. Based on this assumption, the focus is shifted from each SN to each cell, thus significantly reducing complexity. Therefore, this subproblem is reorganized as P1, where C2 refers to the movement constraint, the UAV can choose one of the six neighbor cells to move or just hover. C3 and C4 are energy constraints, which specify the energy range and the energy update model, respectively. C5 describes the charging state, i.e., charging or not charging. C6 means that the AoI of all SNs in the cell will be set to 0. C7 and C8 are position constraints, and the UAV is only allowed to move among the observed cells.

$$
\begin{array} { r l } & { \mathbb { P } { \mathbf 1 } \cdot \displaystyle \frac { \mathrm { s i n } } { \mathrm { s u s } } \frac { 1 } { N } \mathbb { E } [ \displaystyle \sum _ { \rho \in S _ { r } } { \mathbf { \bar { x } } } _ { \rho \in S _ { r } } ] , } \\ & { \mathrm { s } { \mathbf t } , \mathbb { C } { \mathbf 1 } \cdot \boldsymbol { \mathcal { E } } \{ \mathbf { \bar { \pi } } \boldsymbol { \mathcal { A } } , \rho \boldsymbol { \mathcal { A } } , \rho \} , } \\ & { \quad \quad \quad \quad \quad \mathrm { C } { \mathbf 2 } : \alpha { \mathbf { \bar { t } } } , } \\ & { \quad \quad \quad \quad \quad \quad \mathrm { C } { \mathbf 3 } : E _ { \rho } \in \{ 0 , E _ { \mathrm { a n } } \} , } \\ & { \quad \quad \quad \quad \quad \quad \mathrm { C } { \mathbf 4 } : \kappa _ { t i 1 } = E _ { e s t } + \Delta E _ { e s t } , } \\ & { \quad \quad \quad \quad \quad \mathrm { C } { \mathbf 5 } : C _ { t } \in \{ 0 , 1 \} , } \\ & { \quad \quad \quad \quad \mathrm { C } { \mathbf 6 } : z _ { n , i } = 0 , \mathrm { f o r } \ \forall n \in \mathcal { N } _ { e } , } \\ & { \quad \quad \quad \quad \quad \mathrm { C } { \mathbf 7 } : e _ { s t } ^ { \mathrm { a s w } } \in \mathcal { C } , } \\ &  \quad \quad \quad \quad \quad \quad \mathrm { C } { \mathbf 8 } : e _ { s t } ^ { \mathrm { a w } } = \{ \begin{array} { l l } { \displaystyle \mathrm { c } _ { s t } ^ { \mathrm { a v s } } + \alpha _ { 1 } \ \mathrm { f o r } ^ { \mathrm { a v s } } + \alpha _ { 4 } \in E _ { \rho } ^ { \mathrm { a v s } } + \alpha _ { 6 } \in C , } \\ { \quad \quad \mathrm { d r } _ { a b s } ^ { \mathrm { a v s } } + \alpha _ { 1 } \ \mathrm { f o r } ^ { \mathrm { a v s } } } \\  \quad \quad \quad \quad \mathrm { C } { \mathbf 8 } : e _ { s t } ^ { \mathrm { a v s } }  \end{array} \end{array}\tag{20}
$$

2) Task Assignment Problem for Workers: As mentioned before, The worker is a data collector with uncertain trustworthiness, and the data center does not need to fully accept all the data submitted by it. So, a premise needs to be guaranteed, i.e., there must be enough number or sufficiently credible workers to ensure the data accuracy, thus significantly increasing the probability of successful data collection. Similarly, the complexity of directly assigning tasks across the entire network is unacceptable. We should assign the tasks of the nearest cell to workers according to their current position, so that task assignment can be carried out independently in each timeslot and in each cell. Task assignment in cell c at slot t is as follows.

$$
\begin{array} { r l } & { \mathrm { P 2 } : \operatorname* { m a x } \frac { \sum _ { n \in \mathcal { N } _ { c } } z _ { n , t } \left[ 1 - \prod _ { k _ { m , n , t } = 1 } ( 1 - T _ { n , t } ) \right] } { \sum _ { k _ { m , n , t } \in \varphi _ { c , t } } k _ { m , n , t } } , } \\ & { \mathrm { s . t . } \mathrm { C 1 } : m \in \mathcal { M } _ { c } , } \\ & { \mathrm { C 2 } : n \in \mathcal { N } _ { c } , } \\ & { \mathrm { C 3 } : k _ { m , n , t } \in \{ 0 , 1 \} , } \end{array}
$$

$$
\mathrm { C } 4 : \sum _ { n \in \mathcal { N } _ { c } } k _ { m , n , t } \leq L _ { i } .\tag{21}
$$

The purpose of P2 is to increase the expectation that, the SNs with higher AoI will be correctly collected with as fewer assignments as possible. The numerator represents the expectation of AoI decrease in the cell c, and the denominator is the number of assignments. We define $\pi _ { \mathrm { w o r k e r } } = \{ \Psi _ { t } | t = 1 , 2 , \dots , t _ { \operatorname* { m a x } } \}$ as the assignment policy, where $\Psi _ { t } = \{ \stackrel { \cdot } { \varphi } _ { c , t } | c \in C \}$ and $\varphi _ { c , t } =$ $\{ k _ { m , n , t } | \bar { m ^ { } } \in \bar { \mathcal { M } } _ { c } , \bar { n } \in \bar { \mathcal { N } } _ { c } \}$ denote the assignment policy for each cell and specific cell c, respectively. $k _ { m , n , t }$ indicates whether the task of collecting SN n should be assigned to worker m. C1 and C2 indicate that the task assignment is limited in cell c. C3 constrains the assignment states. C4 indicates that the workload should be within the workerâs capacity. Obviously, the higher the numerator, the more likely the AoI can be reduced, and the lower the denominator, the fewer the assignments.

## IV. PROPOSED HYBRID OPTIMIZATION FRAMEWORK FOR AOI MINIMIZATION

This section first gives an overall view of our framework and then provides a detailed description to the worker task assignment strategy and the UAV path planning strategy.

## A. Overview of Hybrid Optimization Framework

In our proposed optimization strategy, the actions of the UAV and workers at each timeslot are different. The UAV mainly collects the data of the cell where it is located, and makes a decision on the following action, then moves to the next cell. The main task of the worker is to accept assignments and execute the data collection of designated SNs. Therefore, the hybrid optimization framework involves two separate parts at timeslot t: the data collection and the path planning. The pseudo-code is shown in Algorithm 1. The overview of our hybrid optimization framework is given in Fig. 3, which includes three stages: (a) task assignment and data collection, (b) state collection and prediction of next action, and (c) data collection of the next slot.

1) Data Collection: As shown in Fig. 3(a), in the data collection part, the UAV will collect the freshest data of the SNs in the cell and the historical data for comparison with the data submitted by the workers. Then, the data center will update the success and failure verification records. Meanwhile, the data center will execute the task assignment policy in each cell to select workers to collect data, which will be detailed in Part B of this section. The workers then start the data collection of the designated SNs in this timeslot. Workers who have the same data collection tasks for the same SN will update the interaction records with each other. It is worth mentioning that there is no need to perform task assignments for the cell where the UAV is located because the UAV is working on it.

2) Path Planning: As shown in Fig. 3(b), the main work of the path planning part is to predict the following action of the UAV based on the current network state, which will be described in detail in Part C of this section. The network state consists of four states, three of which are gathered from the UAV, i.e., energy state, charging state, and position state. The remaining AoI state is estimated by the current network using 13. When these states are fed to the neural network, an optimal action $a ^ { * }$ with the highest reward can be obtained.

<!-- image-->  
(a) Task assignment and data collection

<!-- image-->  
(b) State collection and prediction of next action

<!-- image-->  
(c) Data collection of the next slot

Fig. 3. An overview of our hybrid optimization framework includes optimizing the data collection task assignment for workers and the UAV in each slot, as well as the path planning of the UAV.  
Algorithm 1: The Hybrid Optimization Framework.   
Input: workersâ position and trust value; the UAVâs   
position, energy and charge state; the AoI data of each cell   
1: for $t = 1 , 2 , . . . , t _ { \mathrm { m a x } }$ do   
2: The UAV performs data collection in $c _ { t } ^ { \mathrm { u a v } }$   
3: Update record sets S and F by matching hash code   
4: for $c \in C \backslash c _ { t } ^ { \mathrm { u a v } }$ do   
5: Get the workers $\mathcal { M } _ { c } ,$ , which are located in the cell c   
6: Perform GMTA and assign tasks to workers in $\mathcal { M } _ { c }$   
7: Workers in $\mathcal { M } _ { c }$ execute task immediately   
8: Update interaction records R for workers   
9: end for   
10: Update the total trust of each worker in M by   
(9)â(11)   
11: Get the estimated AoI from each cell by (12)â(14)   
12: Get position, energy, and charging state from the   
UAV   
13: Perform DRL-GAM to get the optimal action $a ^ { * }$   
14: The UAV moves to the next cell or just hovers   
through $a ^ { * }$   
15: end for

Before the end of a timeslot, the data center will update the trust of each worker based on (9)â(11), and update the estimated sampled timestamp of each SN with (12). Then the UAV will enter the next cell according to the status aâ, or just hover.

## B. Greedy-Based Multi-Workers Task Assignment Strategy

There are many existing researches on task assignment [41], [22]. We can find the optimal solution by dynamic programming, but it shows a high complexity in computing time and storage space. Conversely, we can find an approximate solution to combinatorial optimization problems by heuristic algorithms with acceptable complexity, but these methods cannot guarantee the optimal solution.

We propose a fast Greedy-based Multi-workers Task Assignment (GMTA) strategy to reduce AoI, aiming to assign data collection tasks with higher AoI to more trusted workers as much as possible under the workload constraint. Conversely, if untrusted workers handle more urgent tasks, the risk of task failure and AoI increase will be higher. Our strategy is shown in Algorithm 2. First, the assignment strategy $\varphi _ { c , t }$ and the profit ratios T are initialized (lines 1-2). $\mathcal { T } _ { n } \in \mathcal { T }$ represents the profit ratio brought by assigning workers to collect SN n. As workers are continuously assigned to perform the collection tasks of SN n, $\mathcal { T } _ { n }$ will continue to decrease. Then, find the SN $n ^ { * }$ with the highest expectation of AoI decrease and the most reliable worker $m ^ { * }$ for the task assignment, where mâ has not been assigned the task of collecting nâ before (lines 4-6). Finally, update the profit ratio $\mathcal { T } _ { n ^ { * } }$ and workload $L _ { m ^ { * } }$ (lines 7-8). When a worker has no remaining workload, it is removed from the Mc (lines 9-11). When the ratio of the AoI decrease reaches Î, the assignment is terminated (lines 12-14), avoiding redundant tasks and reducing computational overhead.

Algorithm 2: Greedy-Based Multi-Workers Task Assign  
ment.   
Input: t, time slot; c, the cellular cell; $\mathcal { M } _ { c } ,$ the workers in   
cell $c ; \mathcal { N } _ { c } ,$ the SNs in cell $c ; \mathbf { z } = \{ z _ { n , t } | n \in \mathcal { N } _ { c } \}$ , the AoI   
of SNs; $\mathbf { T } = \{ T _ { m } | m \in \mathcal { M } _ { c } \}$ , the trust of workers;   
$\mathbf { L } = \{ L _ { m } | m \in \mathcal { M } _ { c } \}$ , the workload of workers.   
Output: $\varphi _ { c , t } ,$ the task assignment policy in cell c at slot t.   
1: Initialize the task assignment policy   
$\varphi _ { c , t } = \{ k _ { m , n , t } = 0 | \bar { m } \in \bar { \mathcal { M } } _ { c } , n \in \bar { \mathcal { N } } _ { c } \}$   
2: Initialize the profit ratio for each SN   
$\mathbf { T } = \{ { \mathcal { T } } _ { n } = { \dot { 1 } } | n \in { \mathcal { N } } _ { c } \}$   
3: while $\mathcal { M } _ { c } \neq \dot { \varnothing }$ do   
4: Find $n ^ { * } = \arg \operatorname* { m a x } _ { n \in \mathcal { N } _ { c } } z _ { n , t } \mathcal { T } _ { n }$   
5: Find mâ = arg max mâMc Tm   
km,nâ,t=0   
6: $k _ { m ^ { * } , n ^ { * } , t } = 1$   
7: $\mathcal { T } _ { n ^ { * } } = \mathcal { T } _ { n ^ { * } } \cdot ( 1 - T _ { m ^ { * } } )$   
8: $L _ { m ^ { * } } = L _ { m ^ { * } } - 1$   
9: if $L _ { m ^ { * } } = 0$ then   
10: $\mathcal { M } _ { c } = \mathcal { M } _ { c } \backslash m ^ { * }$   
11: end if   
$\sum _ { n \in \mathcal { N } _ { c } } ^ { \mathbf { u } } z _ { n , t } \bigl [ 1 - \prod _ { k \mathop {  } _ { k \mathop {  } _ { c } } } ( 1 - T _ { m , t } ) \bigr ]$   
12: if km,n,t â¤ Î then   
- nâNc zn,t   
13: break   
14: end if   
15: end while

Theorem 1: The time complexity of the proposed GMTA algorithm is O(max (log |Nc|, log $| \mathcal { M } _ { c } | ) \cdot \sum _ { m \in \mathcal { M } _ { c } } L _ { m } )$ , the space complexity is O(max $\textstyle \bigl ( \sum _ { m \in \mathcal { M } _ { c } } L _ { m } , | \mathcal { N } _ { c } | \bigr ) \bigr )$

Proof: The computational overhead in Algorithm 2 is mainly concentrated on the task assignment for each worker. In the worst case, the number of task assignment loops is $\textstyle \sum _ { m \in { \mathcal { M } } _ { c } } L _ { m }$ . For each loop, the time overhead is mainly focused on finding the optimal SN and worker (lines 4-5), and the time complexity of searching can be optimized by using the array-based binary heap, so the search complexity is reduced to log $\vert \mathcal { N } _ { c } \vert$ or $\log { | \mathcal { M } _ { c } | }$ The space overhead is mainly concentrated on the storage of the policy matrix $\varphi _ { c , t }$ , the SN information, and the worker information. Since the number of assignments does not exceed $\textstyle \sum _ { m \in { \mathcal { M } } _ { c } } L _ { m }$ , the matrix $\varphi _ { c , t }$ can be transformed into a set to compress the storage. If the worker m can participate in the task, we have $L _ { m } \ge 1$ , then deduce $\sum _ { m \in \mathcal { M } _ { c } } \dot { L } _ { m } \stackrel { \cdot } { \geq } | \mathcal { M } _ { c } |$ . So the space complexity is the larger value of $\textstyle \sum _ { m \in { \mathcal { M } } _ { c } } L _ { m }$ and $| \mathcal { N } _ { c } |$

## C. DRL-Based Global AoI Minimization Strategy

This section presents our Deep-Reinforcement-Learningbased Global AoI Minimization (DRL-GAM) strategy. The path planning problem of the UAV has been modeled as P1. Continuous path planning can be treated as a Markov Decision Process(MDP), and a tuple $\langle S , A , R , P , \pi \rangle$ can be used to characterize the continuous decision process of the UAV. S represents the state set, A represents the action set, R represents the reward function, $P$ represents transition function of the policy, and $\pi$ is the action policy. We have the following definitions:

1) State $S \stackrel { \triangledown } { = } \{ s _ { t } | t = 1 , 2 , \ldots , t _ { \operatorname* { m a x } } \}$ , where $s _ { t }$ means the state at timeslot t, denoted by $s _ { t } = \{ \mathcal { H } _ { t } , \mathcal { K } _ { t } , \mathcal { C } _ { t } , \mathcal { E } _ { t } \}$ . Here, $\mathcal { H } _ { t } = \{ g _ { c , t } | c \in C \}$ is the AoI of each cell, and $\textstyle { \mathcal { K } } _ { t }$ is the one-hot coding of the position $c _ { t } ^ { \mathrm { u a v } } . ~ { \mathcal { C } } _ { t } \in \{ 0 , 1 \}$ is the charge state, and $\begin{array} { r } { \mathcal { E } _ { t } = \frac { { { { E } _ { t } } } } { { { E } _ { \operatorname* { m a x } } } } } \end{array}$ is the energy state.

2) Action A, as shown in 3, includes moving to six adjacent cells, or just hovering. For our model, arbitrary hovering will lead to an increase in the AoI of all other cells. However, the design of the hovering action is not meaningless. When the UAV hovers, we allow the UAV to find nearby charging spots, enter the charging state and replenish energy, thus preventing the UAV from dying due to lack of energy.

3) Reward function $R _ { s , s ^ { \prime } } ^ { a }$  represents the immediate reward for entering the next state $s ^ { \prime }$ from the state s after taking action a. We use 22 to represent the reward in timeslot $t ,$ where $- G _ { t }$ is the negative global AoI. $\begin{array} { r } { \omega _ { t } ^ { \mathrm { e n e r g y } } = \frac { 2 | C | e ^ { \delta \mathcal { E } _ { t } } } { 1 + e ^ { \delta \mathcal { E } _ { t } } } } \end{array}$ is the energy penalty, where $\delta ( \delta < 0 )$ is a constant. When the UAV dies from insufficient ener $\mathrm { y y } , \omega _ { t } ^ { \mathrm { e n e r g y } } = \left| C \right| \cdot \omega _ { t } ^ { \mathrm { h } }$ over is a penalty designed for meaningless hovering. When the UAVâs position at timeslot t is the same as that at timeslot $t - 1$ but it is not recharging, then $\omega _ { t } ^ { \mathrm { h o v e r } } = | C |$ , otherwise $\omega _ { t } ^ { \mathrm { h o v e r } } = 0$

$$
r _ { t } = - G _ { t } - \omega _ { t } ^ { \mathrm { e n e r g y } } - \omega _ { t } ^ { \mathrm { h o v e r } } .\tag{22}
$$

4) State transition function $P _ { s , s ^ { \prime } } ^ { a }$ represents the probability of entering the state $s ^ { \prime }$ after taking action a, and can be expressed by $P _ { s . s ^ { \prime } } ^ { a } = P [ S ^ { \prime } = s ^ { \prime } | S = s , A = a ]$

5) Policy Ï, which represents the probability of taking action a when the current state is s, can be expressed as $\pi ( a | s ) =$ $P [ A = a | S = s ]$

Based on the feedback of network state, the agent attempts to optimize the policy Ï to maximize the cumulative reward. The agent learns the policy by repeatedly acting on the environment and trying to get a higher cumulative reward for the action. So the cumulative reward is an essential basis for realizing various responses to the environment.

Two types of value functions are introduced to calculate the cumulative reward. The first is the state value function, as shown in 23, where $\gamma$ represents the discount rate, which means the effect of future rewards on the current state. The state value function measures the cumulative reward brought by the strategy Ï starting from the state s.

$$
V ^ { \pi } ( s ) = \mathbb { E } _ { \pi } \Bigg [ \sum _ { t } \gamma ^ { t } r _ { t + 1 } | s _ { 0 } = s \Bigg ] .\tag{23}
$$

The second is the state-action value function, as shown in (24). It measures the cumulative reward of the strategy Ï starting from the union of state s and action a.

$$
Q ^ { \pi } ( s , a ) = \mathbb { E } _ { \pi } \left[ \sum _ { t } \gamma ^ { t } r _ { t + 1 } | s _ { 0 } = s , a _ { 0 } = a \right] .\tag{24}
$$

According to Bellmanâs equation [42], the state-action value function can be converted to (25), where $s ^ { \prime }$ denotes the next state, equivalent to $s _ { t + 1 }$

$$
Q ^ { \pi } ( s , a ) = \sum _ { s ^ { \prime } \in S } P _ { s , s ^ { \prime } } ^ { a } \mathbb { E } _ { \pi } \left[ R _ { s , s ^ { \prime } } ^ { a } + \gamma V ^ { \pi } ( s ^ { \prime } ) \right] .\tag{25}
$$

Then the optimal Q function is adjusted to (27) by adopting the optimal policy function $\pi ^ { * }$

$$
\pi ^ { * } ( s ) = \arg \operatorname* { m a x } _ { a \in A } V ^ { \pi } ( s ^ { \prime } ) .\tag{26}
$$

$$
\begin{array} { r l } & { Q ^ { * } ( s , a ) = \displaystyle \sum _ { s ^ { \prime } \in S } P _ { s , s ^ { \prime } } ^ { a } \mathbb { E } _ { \pi } \left[ R _ { s , s ^ { \prime } } ^ { a } + \gamma \operatorname* { m a x } _ { a \in A } V ^ { \pi } ( s ^ { \prime } ) \right] . } \end{array}\tag{27}
$$

Based on the Temporal Difference (TD) in Ref. [42], the updating policy for the average reward value can be obtained by (28), where $\mu$ is the learning rate, and $Q _ { t + 1 } ( s , a )$ represents the state-action value of taking action a in the state s at the timeslot t + 1. $\operatorname* { m a x } _ { a \in A } Q _ { t } ( s ^ { \prime } , a )$ represents the maximum state reward by choosing the best action in the next state, where $Q _ { t } ( s ^ { \prime } , a )$ gives the average reward return of each action, so our goal is to choose the action that maximizes $Q _ { t } .$ , as shown in (29).

$$
Q _ { t + 1 } ( s , a ) \gets Q _ { t } ( s , a )
$$

$$
+ \mu \left[ r _ { t + 1 } + \gamma \operatorname* { m a x } _ { a \in A } Q _ { t } ( s ^ { \prime } , a ) - Q _ { t } ( s , a ) \right] .\tag{28}
$$

$$
a _ { t } ^ { * } = \arg \operatorname* { m a x } _ { a \in A } Q _ { t } ( s , a )\tag{29}
$$

The above estimation process is the main content of Nature Deep Q-Network (Nature DQN) [43]. It contains only one evaluator and the estimation of the future state-action value function $Q _ { t } ( s ^ { \prime } , a )$ , which is used to update $Q _ { t + 1 } ( s , a )$ , is based on partial experience, so it is easy to cause overestimation. We have combined two improved DRL frameworks to enhance the above problems, strengthen stability and weaken overestimation. The first is Double DQN, which uses two neural networks, the target network $Q ^ { A }$ and the evaluation network $Q ^ { B }$ to split the estimation and selection operations, forming two estimators. We use (30) to express the updating of the target network.

$$
\begin{array} { r l } & { Q _ { t + 1 } ^ { A } ( s , a ) \gets Q _ { t } ^ { A } ( s , a ) } \\ & { + \mu \left[ r _ { t + 1 } + \gamma \operatorname* { m a x } _ { a ^ { * } \in A } Q _ { t } ^ { B } ( s ^ { \prime } , a ^ { * } ) - Q _ { t } ^ { A } ( s , a ) \right] . } \end{array}\tag{30}
$$

The optimal action is shown in (31), which represents the optimal action value of the target network $Q ^ { A }$ that maximizes the value function $Q _ { t } ^ { A } ( s ^ { \prime } , a ^ { * } )$ . During the update, the network $Q ^ { B }$ is used to evaluate $\dot { Q } ^ { A }$ , and the target network $Q ^ { A }$ is used for the actual

<!-- image-->  
Fig. 4. The structure of Dueling DQN.

training.

$$
a ^ { * } = \arg \operatorname* { m a x } _ { a \in A } Q _ { t } ^ { A } ( s ^ { \prime } , a ) .\tag{31}
$$

The second improved network is Dueling DQN [44], which is a structural improvement to Nature DQN. Nature DQN outputs the Q values of |A| actions respectively, and selects the action $a ^ { * }$ that maximizes $Q .$ The Dueling DQN introduces two kinds of special neurons in the front of the output layer. The authors in Ref. [44] call them value $V ( s ; \vartheta , \beta )$ and advantage $A ( s , a ; \vartheta , \alpha )$ , and its structure is shown in Fig. 4. As shown in 32, the original $Q ( s , a )$ is denoted as $Q ( s , a ; \vartheta , \alpha , \beta )$ , where Ï represents the overall network parameters, Î± and $\beta$ represent the independent parameters of the value $V ( s ; \vartheta , \beta )$ and the advantage $\bar { A } ( s , a ; \vartheta , \alpha )$ , where $| A |$ is the total number of actions. The action advantage function is set as the individual action function minus the average action advantage functions to eliminate redundant freedom degrees, improving the algorithmâs stability.

$$
\begin{array} { l } { \displaystyle Q ( s , a ; \vartheta , \alpha , \beta ) } \\ { = \displaystyle V ( s ; \vartheta , \beta ) + \left[ A ( s , a ; \vartheta , \alpha ) - \frac { 1 } { | A | } \sum _ { a ^ { \prime } \in A } A ( s , a ^ { \prime } ; \vartheta , \alpha ) \right] . } \end{array}\tag{32}
$$

Finally, the gradient descent method with learning rate Î· is used to minimize the loss function as 33.

$$
\mathcal { L } ( \vartheta ) = \frac { 1 } { 2 } \left| r _ { t + 1 } + \gamma \operatorname* { m a x } _ { a \in A } Q _ { t } ^ { B } ( s ^ { \prime } , a ^ { * } ) - Q _ { t } ^ { A } ( s , a ) \right| ^ { 2 } .\tag{33}
$$

According to the above two improved DQN algorithms, the design diagram of D3QN neural network is shown in Fig. ${ 5 } .$ The input parameters are four state objects, including the cell AoI state, position state, charging state and energy state. Here, the cell AoI state is a matrix with the shape of $X \times Y .$ , and each element is the AoI of different cell. The position state is a $2 \times \operatorname* { m a x } ( X , Y )$ matrix, and the position information is the One-Hot Encoding. The charging state and energy state are both values of $1 \times 1$ shape. In order to integrate the input layers of different dimensions, it is necessary to do some processing of the input layer. For the position states and cell AoI states, the matrix needs to be converted into vector form through a flatten layer. Then the four vectors are passed into the concatenate layer for concatenation and merging, and then into several dense layers. Rectified Linear Unit (ReLU) is used as the activation function of dense layers to provide the ability to fit nonlinear functions. Finally, the dense layers are respectively connected to the value function and the advantage function provided by

<!-- image-->  
Fig. 5. The design of D3QN neural network, mainly including input layer, flatten layer, concatenate layer, and dense layer.

<!-- image-->  
Fig. 6. Simulation environment which contains the GPS trajectories of 10,357 taxis in Beijing from Feb. 2 to Feb. 8, 2008, and observation area is ranged between 116.15â¦E â¼ 116.22â¦E and 39.72â¦N â¼ 40.122â¦N.

Dueling DQN, where the value function has the shape of $1 \times 1$ and the advantage function has the shape of $1 \times 7 ,$ which is then output to the final action output in the form of linear activation function.

Algorithm 3 provides the online training process based on Dueling DQN and Double DQN, called D3QN. The method first initializes the replay memory, which is used to train the target network, then initializes the neural networks $Q ^ { A }$ and $Q ^ { \breve { B } }$ (line 1). The training is divided into many episodes, and each episode contains $t _ { \mathrm { m a x } }$ slots. At the beginning of each episode, the network state will be initialized to $s _ { 0 }$ (line 3). The -greedy strategy is adopted to decide whether to perform random exploration, that is, allow the UAV to randomly select the next action with the probability of $\epsilon ,$ or choose the output from the neural network with the probability of 1 â . As slots evolve, the exploration rate  will tighten to 0 (line 16), and the network will be more inclined to choose the action output of the neural network. The current state $s _ { t } .$ , the action ${ { a } _ { t } } ,$ the next state $s _ { t + 1 }$ and the reward $r _ { t + 1 }$ will be saved in the replay memory U (line 7). During the training, we take out some records from memory, and train the target network $Q ^ { A }$ in the form of mini-batches (lines 8-15). At the end of each episode, the weights of $Q ^ { A }$ are assigned to the $Q ^ { B }$ (line 18).

Algorithm 3: Online Training Based on D3QN.   
Input: $\gamma ,$ discount rate; $\epsilon _ { d } ,$ decay rate of $\epsilon ; \mu ,$ learning rate;   
Î©, batch size.   
1: Initialize replay memory U, networks $Q ^ { A }$ and $Q ^ { B } , \epsilon = 1$   
2: for episode = 0, 1, 2, . . . , do   
3: Initialize state $s _ { 0 }$   
4: for $t = 0 , 1 , 2 , \ldots , t _ { \mathrm { m a x } }$ do   
5: Select a random action $a _ { t }$ from A with probability $\epsilon ,$   
or the action $a _ { t } = \arg \operatorname* { m a x } _ { a _ { t } \in A } Q ^ { A } ( s ^ { \prime } , \bar { a } ^ { * } )$ with   
probability $1 - \epsilon$   
$_ { 6 ; }$ Execute ${ { a } } _ { t } ,$ get reward $r _ { t + 1 }$ and next state $s _ { t + 1 }$   
7: Store $\langle s _ { t } , s _ { t + 1 } , a _ { t } , r _ { t + 1 } \rangle$ in replay memory U   
8: if $| \boldsymbol { \mathcal { U } } | \dot { \mathrm { > } } \Omega$ then   
9: Randomly select minibatch memories $\mathcal { G }$ from U   
10: for $\langle s _ { i } , s _ { i + 1 } , a _ { i } , r _ { i + 1 } \rangle \in \mathcal { G }$ do   
11: $y = r _ { i + 1 } + \gamma$ maxaâA $Q _ { j } ^ { B } \left( s ^ { \prime } , a ^ { * } \right)$ , where   
$a ^ { * } =$ arg ma $\mathrm { x } _ { a \in A } Q _ { i } ^ { A } ( s ^ { \prime } , a )$   
12: $y ^ { \prime } = Q _ { i } ^ { A } ( s , a )$   
13: Perform gradient descent by $? ? ,$ update $Q ^ { A }$   
14: end for   
15: end if   
16: $\epsilon = \epsilon \cdot \epsilon _ { d }$   
17: end for   
18: Assign the network parameters of $Q ^ { A }$ to $Q ^ { B }$   
19: end for

## V. PERFORMANCE AND ANALYSIS

To verify the performance of our framework, we built this network based on TensorFlow with Python 3.8. The core neural network, D3QN, is built based on the open-source network framework Keras.

## A. Training Environment and Parameter Settings

To make the simulation experiment closer to reality, our simulation is based on the t-drive dataset provided by Yuan et al. [45]. This dataset contains the GPS trajectories of 10,357 taxis in Beijing from Feb. 2 to Feb. 8, 2008. Based on the dataset, we present the simulation scenario as shown in Fig. 6. Our observation area is ranged between 116.15â¦E â¼ 116.22â¦E and 39.72â¦N â¼ 40.122â¦N. The city is divided into 10 Ã 10 hexagonal cells with evenly distributed 5000 SNs, and each cell contains an indeterminate number of SNs (i.e., blue dots). Grey dots refer to vehicle coordinates provided by the dataset. The red dot indicates the coordinate of the UAV. The vehicle trajectories are mainly distributed in the cityâs central area, while the trajectories in the peripheral regions are much fewer.

Without loss of generality, some default parameters and their references are shown in Table I. $t _ { \mathrm { m a x } }$ is set according to the s datasetâs sampling period, the UAVâs flight speed, and the cellâs actual length. Î´ is an adjustment factor for calculating the energy penalty of reward $r _ { t } .$ . We expected the UAV to avoid hovering due to frequent charging, but also not die from low energy. The energy penalty is capped at |C|, so the parameter Î´ = â29.44 means that when the residual energy is only 10%, the penalty value reaches 0.1|C|, while the energy is less than 10%, the penalty increases rapidly to |C|. W direct and W recom do not affect the accuracy of trust evaluation, but larger values will take up more storage capacity for trust calculation. The batch size Î© and decay rate $\epsilon _ { d }$ only affect the convergence speed and have little effect on the convergence value.

TABLE I MAIN PARAMETERS
<table><tr><td></td><td>Meaning</td><td>Value</td><td>Ref.</td></tr><tr><td> $C _ { \mathrm { d r a g } }$ </td><td>Aerodynamic drag coefficient</td><td>0.0895</td><td>[46]</td></tr><tr><td> $A _ { \mathrm { { f r o n t } } }$ </td><td>Front-facing area of the UAV</td><td> $\mathrm { 0 . 0 4 0 7 m ^ { 2 } }$ </td><td>[47]</td></tr><tr><td> $D _ { \mathrm { a i r } }$ </td><td>Air density</td><td> $1 . 2 9 \mathrm { k g / m ^ { 3 } }$ </td><td>â </td></tr><tr><td> $W _ { \mathrm { u a v } }$ </td><td>Weight of the UAV</td><td> $0 . 8 9 9 \mathrm { k g }$ </td><td>[47]</td></tr><tr><td> $v$ </td><td>Flight speed of the UAV</td><td> $1 5 \mathrm { m / s } ^ { - }$ </td><td>[47]</td></tr><tr><td> $d _ { \mathrm { u a v } }$ </td><td>Width of the UAV</td><td> $0 . 2 8 3 \mathrm { { m } }$ </td><td>[47]</td></tr><tr><td> $E _ { \mathrm { m a x } }$ </td><td>Maximum energy of the UAV</td><td>77wh</td><td>[47]</td></tr><tr><td> $P _ { \mathrm { c h a r g e } }$ </td><td>Charging power of the UAV</td><td>65w</td><td>[47]</td></tr><tr><td> $P _ { \mathrm { c o m m } }$ </td><td>Communication power of the UAV</td><td>0.0126w</td><td>[25]</td></tr><tr><td> $N _ { 0 }$ </td><td>White noise power</td><td>-50dBm</td><td>[25]</td></tr><tr><td>PT</td><td>Transmission power</td><td>23dBm</td><td>[25]</td></tr><tr><td> $\grave { H }$ </td><td>Height of the UAV</td><td>50m</td><td>[25]</td></tr><tr><td> $f _ { c }$ </td><td>Carrier frequency</td><td>2GHz</td><td>[33]</td></tr><tr><td> $B$ </td><td>Bandwidth</td><td>4MHz</td><td>[33]</td></tr><tr><td> $\boldsymbol { B }$ </td><td>Message size</td><td>4Mbyte</td><td>-</td></tr><tr><td> $\eta _ { 1 } , \eta _ { 2 }$ </td><td>Path loss coefficients of LoS channel</td><td>3dB,23dB</td><td>[33]</td></tr><tr><td> $\zeta , \varpi$ </td><td>Parameters ofLoS channel</td><td>11.95,0.14</td><td>[33]</td></tr><tr><td> $t _ { \mathrm { m a x } }$ </td><td>Maximum time slot</td><td>1394â³t</td><td>â </td></tr><tr><td> $\Omega$ </td><td>Batch size</td><td>256</td><td></td></tr><tr><td> $\epsilon _ { d }$ </td><td>Decay rate of random exploration rate</td><td>0.99999</td><td></td></tr><tr><td> $W ^ { \mathrm { d i r e c t } }$ </td><td>Capacity of direct records</td><td>10</td><td></td></tr><tr><td> $W ^ { \mathrm { r e c o m } }$ </td><td>Capacity of recommendation records</td><td>20</td><td></td></tr><tr><td> $\delta$ </td><td>Factor of the energy penalty</td><td>-29.44</td><td></td></tr></table>

<!-- image-->

<!-- image-->  
Fig. 7. Learning rate $\mu$ and discount rate Î³ for training D3QN.

Since D3QN still has the same characteristics as general deep neural networks, it is necessary to adjust some network parameters to obtain better optimization. The two most important parameters are the learning rate $\mu$ and the discount rate $\gamma .$ . The learning rate $\mu$ directly affects the convergence, while the discount rate Î³ affects the accuracy. We tune these two hyper-parameters, and the results are shown in Fig. 7. It shows that higher learning rates tend to peaks after the learning curve converges, which means that the training is insufficient. In contrast, lower learning rates lead to slower convergence rate. The discount rate $\gamma$ is an indication of future predictions. To make sufficiently long-term predictions for the future, Î³ should be as large as possible. When $\gamma \geq 0 . 7 5$ , the training accuracy performs are better. However, when Î³ = 0.99, there are many oscillations, which shows that it is difficult for the agent to predict the longer-term future stably. So, we take $\mu = 0 . 0 0 0 0 5$ and $\gamma = 0 . 9$ for all subsequent simulation experiments.

## B. AoI Performance

Based on our hybrid framework, we compare the following path planning strategies:

1) DRL-GAM, our proposed method. The agent needs to be pre-trained according to the network environment, and

<!-- image-->  
(a) Worker number M = 100

<!-- image-->  
(b) Worker number M = 500

Fig. 8. Average global AoI curve with different worker scales.  
<!-- image-->

<!-- image-->  
(d) Worker number M = 5000

<!-- image-->

<!-- image-->  
(b) SN number N= 1000

Fig. 9. Average global AoI with different network scales.  
<!-- image-->

<!-- image-->

<!-- image-->  
(a) SN number N = 500

<!-- image-->  
(b) SN number N = 1000

<!-- image-->  
(c) SN number N= 5000

<!-- image-->  
(d) SN number N = 10000

Fig. 10. Stability performance of AoI with different SN scales.

then selects the next action aâ according to the optimal output by the neural network.

2) Greedy [48], which is a short-sighted strategy. The agent greedily selects the next movement according to the AoI state of neighbor cells.

3) Robin Round [25], which is the most balanced strategy. The agent chooses a fixed, recurring path, continues to move on this path, and visits each cell in turn.

4) Complete Coverage Path Planning (CCPP) [49], which is a method that simultaneously emphasizes path coverage and AoI minimization. It prioritizes to finding a complete coverage path that minimizes the sum of AoI in the path.

We first plot the global AoI curve of the four path planning strategies under our hybrid framework with different worker scales, as shown in Fig. 8. Each curve is the mean of 100 replicates to measure the average performance of each strategy better. Intuitively, under our hybrid framework, all strategies can significantly reduce the global AoI with the participation of massive workers. A very interesting phenomenon is repeat-ed everyday, i.e, regardless of the path planning strategy, the AoI rises at midnight and drops rapidly around 7:00 am. From the dataset we can see that most vehicles are active between 8:00 am and 10:00 pm, with less activity between 10:00 pm and 8:00 pm, so the AoI curve peaks around 7:00 am, and then declines as worker activity increases. Compared with other strategies, our DRL-GAM strategy has a more pronounced compensatory effect on AoI deterioration at mid-night, and the suppression of AoI peak is more significant. Meanwhile, our DRL-GAM strategy has a lower average AoI and better stability.

To intuitively compare the AoI performance of these strategies under different networks, Figs. 9 and 10 illustrate the average global AoI and stability performance, respectively. Stability performance is measured by the standard deviation of the global AoI in each timeslot. The smaller the value, the more stable the global AoI. The results show that our DRL-GAM strategy outperforms other strategies in terms of average global AoI and stability among all network scenarios, while the Greedy strategy performed the worst. Besides, the CCPP strategy is better than that of the Robin Round strategy in scenarios with fewer workers. According to the statistics, our strategy can reduce global AoI by 6.49%â¼68.21% compared with other strategies, with an average of 34.65%. The average standard deviation of AoI is only 51.75% of other strategies.

Figs. 11 and 12 demonstrate the UAVâs adaptability to the perturbation of the worker-driven data collection, which respectively show the average AoI and the access probability of each cell in the network with 500 workers and 5000 SNs. The more uniform the AoI of cells and the fewer the extreme values, the stronger the UAVâs ability to adapt to worker data collection. These two figures show that our strategy is more balanced for AoI optimization for each cell, and the UAV tends to fly to the city fringe to collect data, thus reducing conflicts with workers. The Greedy strategy is starved, so some cells cannot be updated by the UAV or by the workers for a long time. The Robin Round strategy has a good grasp of AoI balance, but it ignores the fact that many workers are distributed in the center of city. Repeatedly collecting these areas will not further reduce AoI, but will delay the collection of peripheral cells. The performance of the CCPP strategy is between Greedy and Robin Round, which alleviates the starvation of some cells, but fails to solve the conflict work with workers.

<!-- image-->  
(a) DRL-GAM

<!-- image-->  
Fig. 11. Average AoI of each cell with the four strategies.

(c) Robin Round  
<!-- image-->  
(a) DRL-GAM

<!-- image-->  
(d) CCPP  
(b) Greedy  
Fig. 12. Access probability for each cell with the four strategies.

## C. Trust Evaluation and Task Assignment Performance

In our hybrid framework, the calculation of AoI is based on the trust evaluation model. Inaccurate trust evaluation will affect current action decision value and worsen future AoI.

Experiments in this section are based on the network with 500 workers and 5000 SNs. For each experiment, we run 250 repetitions. In our framework, two parameters play a crucial role in trust evaluation and AoI estimation. The first is the weight $\rho$ for calculating direct trust. The larger Ï is, the more the total trust adopts the direct trust. On the contrary, the more the total trust adopts the recommendation trust. Fig. 13(a) shows the error between the estimated cell AoI and the actual cell AoI for different $\rho$ values and different work environments, where the error can be evaluated by the 2-norm of the difference between the two, and the work environment is characterized by the ratio of malicious workers to the total workers. The smaller the 2-norm error, the closer the estimated AoI is to the actual AoI, and the more beneficial for the UAV to choose the optimal action. The higher the malicious ratio, the lower the completion rate of tasks assigned to workers. The results show that all errors increase as the malicious ratio increases. A Ï value that is too high or too low will affect the accuracy of the estimation. Fig. 13(b) shows the trust values of normal and malicious workers with different $\rho$ values. When the $\rho$ value is higher, it means that the total trust which adopts the direct trust from the UAV is higher. Since the data collected by the UAV is relatively small compared with that of workers, the proportion of workers who can use direct trust to calculate trust is not large, and many workers still are indirectly evaluated for trust. Therefore, the higher the value of $\rho ,$ the lower the weight of the indirect calculation of worker trust, resulting in the slower change of trust in most of the indirect trust evaluation methods, the slower trust convergence, and the inaccurate estimation of AoI in the unstable phase. Conversely, the lower the value of $\rho ,$ , the greater the weight of indirect trust evaluation among the majority workers, therefore, the faster the trust convergence, and the worse the AoI estimation in the stable stage. This is also consistent with the AoI estimation curve in Fig. 13(a). To balance convergence speed and accuracy, we use $\rho = 0 . 5$ for the subsequent evaluation experiments.

<!-- image-->

<!-- image-->

<!-- image-->  
(c) Robin Round

<!-- image-->  
(d) CCPP

<!-- image-->  
(a) Effect of p on Aol estimation

<!-- image-->  
(b) Effect of p on trust of workers

Fig. 13. The effect curve of Ï value on AoI estimation and trust.  
<!-- image-->  
(a) Effect of ^on Aol estimation

<!-- image-->  
(b) Effect of Aon task assignment  
Fig. 14. The effect curve of Î value on AoI estimation and task assignment.

<!-- image-->  
(a) Error performance

<!-- image-->  
(b) Aol performance

<!-- image-->  
(c) Tasks assigned to normal workers

<!-- image-->  
(d) Tasks assigned to malicious workers  
Fig. 15. Performance comparisons of random strategy and GMTA strategy.

The second parameter is Î, which determines the convergence rate of the GMTA strategy. A higher Î means that the collection tasks of a single SN can be assigned to more workers, which means more task assignments and more costs. If Î is too low, it will lead to poor AoI estimation. Fig. 14(a) and (b) present the effect of Î on the error of AoI estimation and task assignment, respectively. When $\Lambda \geq 0 . 8 7 5$ , the AoI estimation is almost the same, but more tasks are assigned, requiring more computational resources and cost. Therefore, $\Lambda = \bar { 0 } . 8 7 5$ is chosen.

We use the Random strategy as the baseline to compare the proposed GMTA strategy, where the Random strategy refers to the random selection of workers when assigning tasks, and the others are consistent with Algorithm 2. Fig. 15 gives the comparisons of error performance, AoI performance and task assignment performance. We can conclude that, compared to the Random strategy, our strategy does not significantly change the AoI, but reduces the AoI estimation error by 22.01%, task assignment by 5.57% and the tasks assigned to malicious workers by 16.5%, respectively. The reasons for the significant reduction of the AoI estimation error in Fig. 15(a) are as follows: our strategy can effectively identify trusted workers through the effective worker trust evaluation mechanism, and select trusted workers for data collection, so the calculated AoI is accurate. Unfortunately, there is no worker trust identification mechanism in the previous strategy, so some untrusted workers are recruited, and their submitted data are false or malicious, resulting in the invalidity of their calculated AoI and the large AoI estimation error. However, the main reason for the small reduction of the average global AoI in Fig. 15(b) is that the trust identification method in this paper needs a long period of time to identify the worker trust. At the beginning, the trust of many workers in the system is still uncertain, and it is difficult to recruit trusted workers effectively. As a result, the effect has not been significantly improved. Besides, benefiting from the worker trust identification mechanism, it shows an effective reduction of the tasks assigned to malicious workers in Fig. 15(d). Once the malicious workers are identified, they will not be recruited, so as to effectively reduce the possibility of tasks assigned to malicious workers.

## VI. DISCUSSIONS AND CONCLUSION

In this section, we first give the limitations of this paper and future work. Then, the conclusion of our work is presented.

## A. Limitations and Future Work

The hexagonal cell proposed in the network model of this paper is a logical area established based on geographic location, and we have not further discussed the network topology within it. For example, whether there is a mutual connection between the SNs in the cell. We assume that the UAV and workers are treated as access points, and they can collect any SNs as long as they are inside the cell. Therefore, our proposed path planning and task assignment strategy are macroscopic and cell-based. In future work, we will take the SNs in the cell as the optimization object, and not only optimize the global network but also conduct more detailed research on the activities in each cell.

In addition, in this paper, we consider the data collection involving a single UAV and workers. This type of study is applicable to most scenarios because data collection solely by workers can maintain high task completion rates in most MCS. Nevertheless, when multiple UAVs are employed, the AoI will be smaller, data quality will be better guaranteed, the task completion rate will be enhanced, and the applicable network scale will be larger at the expense of higher system costs. Therefore, it is highly suitable for applications with more rigorous AoI and data quality requirements. Hence, in the future, we will explore the possibility of using multiple UAVs in combination with workers for data collection.

## B. Conclusion

Utilizing the UAV for path planning to minimize AoI is one of the hot topics. However, the energy limitation makes the UAV unsuitable for continuous and large-scale data collection. Besides, employing workers to collect data is faced with the challenge that data quality is difficult to guarantee and AoI is poor, because dishonest workers may report false data, which will affect the development of the entire application. Therefore, we propose an integrated hybrid optimization framework. On one hand, the GMTA strategy based on the trust mechanism is used to assign more urgent data collection tasks to more credible workers to ensure high data quality and effective AoI. On the other hand, a DRL-GAM strategy based on the D3QN neural network is proposed, which enables the UAV to intelligently find the optimal next action according to the AoI state of the current network, minimizing the global AoI. Our experiments show that under different network scales, our strategy can reduce the global AoI by 6.49% to 68.21% on average, and the stability is also greatly improved. The average standard deviation of AoI is only 51.75% of other strategies.

## REFERENCES

[1] K. Fan et al., âCRL-MABA: A completion rate learning based accurate data collection scheme in large-scale energy internet,â IEEE Internet Things J., vol. 11, no. 14, pp. 24400â24413, Jul. 2024.

[2] Z. Chen et al., âUITDE: A UAV-assisted intelligent true data evaluation method for ubiquitous IoT systems in intelligent transportation of smart city,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 8, pp. 9597â9607, Aug. 2024.

[3] Y. Deng, S. Wu, J. You, J. Jiao, N. Zhang, and Q. Zhang, âOptimizing age of information in polar coded status update system,â IEEE Internet Things J., vol. 11, no. 1, pp. 1285â1300, Jan. 2024.

[4] Z. Wei et al., âIntegrated sensing and communication enabled multiple base stations cooperative sensing towards 6G,â IEEE Netw., vol. 38, no. 4, pp. 207â215, Jul. 2024.

[5] B. Li, W. Liu, W. Xie, N. Zhang, and Y. Zhang, âAdaptive digital twin for UAV-assisted integrated sensing, communication, and computation networks,â IEEE Trans. Green Commun. Netw., vol. 7, no. 4, pp. 1996â2009, Dec. 2023.

[6] M. Bonola, L. Bracciale, P. Loreti, R. Amici, A. Rabuffi, and G. Bianchi, âOpportunistic communication in smart city: Experimental insight with small-scale taxi fleets as data carriers,â Ad Hoc Netw., vol. 43, pp. 43â55, 2016.

[7] R. Liu, A. Liu, Z. Qu, and N. N. Xiong, âAn UAV-enabled intelligent connected transportation system with 6G communications for internet of vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 2, pp. 2045â2059, Feb. 2023.

[8] Y. Emami, H. Gao, K. Li, L. Almeida, E. Tovar, and Z. Han, âAge of information minimization using multi-agent UAVs based on AI-enhanced mean field resource allocation,â IEEE Trans. Veh. Technol., vol. 73, no. 9, pp. 13368â13380, Sep. 2024.

[9] P. D. Mankar, Z. Chen, M. A. Abd-Elmagid, N. Pappas, and H. S. Dhillon, âThroughput and age of information in a cellular-based IoT network,â IEEE Trans. Wireless Commun., vol. 20, no. 12, pp. 8248â8263, Dec. 2021.

[10] Y. Xu, M. Xiao, Y. Zhu, J. Wu, S. Zhang, and J. Zhou, âAoI-guaranteed incentive mechanism for mobile crowdsensing with freshness concerns,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 4107â4125, May 2024.

[11] Y. Liu, L. X. Cai, Q. Chen, H. Zhang, F. Hou, and T. H. Luan, âMinimizing age of information in non-orthogonal random access networks,â IEEE Internet Things J., vol. 11, no. 14, pp. 24886â24902, Jul. 2024.

[12] J. Zhu and J. Gong, âOptimizing peak age of information in MEC systems: Computing preemption and non-preemption,â IEEE/ACM Trans. Netw., vol. 32, no. 4, pp. 3285â3300, Aug. 2024.

[13] H. Hu, K. Xiong, G. Qu, Q. Ni, P. Fan, and K. B. Letaief, âAoI-minimal trajectory planning and data collection in UAV-assisted wireless powered IoT networks,â IEEE Internet Things J., vol. 8, no. 2, pp. 1211â1223, Jan. 2021.

[14] Y. Cheng, X. Wang, P. Zhou, X. Zhang, and W. Wu, âFreshness-aware incentive mechanism for mobile crowdsensing with budget constraint,â IEEE Trans. Services Comput., vol. 16, no. 6, pp. 4248â4260, Nov./Dec. 2023.

[15] R. D. Yates, Y. Sun, D. R. Brown, S. K. Kaul, E. Modiano, and S. Ulukus, âAge of information: An introduction and survey,â IEEE J. Sel. Areas Commun., vol. 39, no. 5, pp. 1183â1210, May 2021.

[16] A. Alabbasi and V. Aggarwal, âJoint information freshness and completion time optimization for vehicular networks,â IEEE Trans. Services Comput., vol. 15, no. 2, pp. 1118â1129, Mar./Apr. 2022.

[17] A. Ferdowsi, M. A. Abd-Elmagid, W. Saad, and H. S. Dhillon, âNeural combinatorial deep reinforcement learning for age-optimal joint trajectory and scheduling design in UAV-assisted networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 5, pp. 1250â1265, May 2021.

[18] X. Chi, X. Qin, X. Xu, S. Han, L. Jin, and P. Zhang, âAge of model: A metric for keeping ai models up-to-date in edge intelligence-enabled IoV,â IEEE Trans. Veh. Technol., vol. 73, no. 9, pp. 13047â13059, Sep. 2024.

[19] Z. Huang et al., âAoI-guaranteed bandit: Information gathering over unreliable channels,â IEEE Trans. Mobile Comput., vol. 23, no. 10, pp. 9469â 9486, Oct. 2024.

[20] J. Liu, J. Shao, M. Sheng, Y. Xu, T. Taleb, and N. Shiratori, âMobile crowdsensing ecosystem with combinatorial multi-armed bandit-based dynamic truth discovery,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 13095â13113, Dec. 2024.

[21] J. Bai, J. Gui, N. N. Xiong, A. Liu, and J. Wu, âL3P-DLI: A lightweight positioning-privacy protection scheme with double-layer incentives for wireless crowd sensing systems,â IEEE J. Sel. Areas Commun., vol. 42, no. 10, pp. 2938â2953, Oct. 2024.

[22] J. Bai, G. Huang, S. Zhang, Z. Zeng, and A. Liu, âGA-DCTSP: An intelligent active data processing scheme for UAV-enabled edge computing,â IEEE Internet Things J., vol. 10, no. 6, pp. 4891â4906, Mar. 2023.

[23] A. T. A. Ghazo and R. Kumar, âANDVI: Automated network device and vulnerability identification in SCADA/ICS by passive monitoring,â IEEE Trans. Syst., Man, Cybern. Syst., vol. 54, no. 4, pp. 2539â2550, Apr. 2024.

[24] N. K. Barsha and N. Hubballi, âAnomaly detection in SCADA systems: A state transition modeling,â IEEE Trans. Netw. Service Manag., vol. 21, no. 3, pp. 3511â3521, Jun. 2024.

[25] R. Liu, M. Xie, A. Liu, and H. Song, âJoint optimization risk factor and energy consumption in IoT networks with TinyML-enabled internet of UAVs,â IEEE Internet Things J., vol. 11, no. 12, pp. 20983â20994, Jun. 2024.

[26] S. Say, H. Inata, J. Liu, and S. Shimamoto, âPriority-based data gathering framework in UAV-assisted wireless sensor networks,â IEEE Sensors J., vol. 16, no. 14, pp. 5785â5794, Jul. 2016.

[27] H. Guo and J. Liu, âUAV-enhanced intelligent offloading for Internet of Things at the edge,â IEEE Trans. Ind. Inform., vol. 16, no. 4, pp. 2737â 2746, Apr. 2020.

[28] J. Sun, W. Wang, S. Li, Q. Da, and L. Chen, âScheduling optimization for UAV communication coverage using virtual force-based PSO model,â Digit. Commun. Netw., vol. 10, no. 4, pp. 1103â1112, 2024.

[29] Y. Luo, J. Xu, J. Chen, and J. Huang, âUAV trajectory planning with network age of information minimization,â in Proc. IEEE Wireless Commun. Netw. Conf., 2022, pp. 1862â1867.

[30] P. Tong, J. Liu, X. Wang, B. Bai, and H. Dai, âDeep reinforcement learning for efficient data collection in UAV-aided Internet of Things,â in Proc. IEEE Int. Conf. Commun. Workshops, 2020, pp. 1â6.

[31] L. Liu, K. Xiong, Y. Lu, P. Fan, and K. B. Letaief, âAge-constrained energy minimization in uav-assisted wireless powered sensor networks: A DQN-based approach,â in Proc. IEEE Conf. Comput. Commun. Workshops, 2021, pp. 1â2.

[32] R. G. Ribeiro, L. P. Cota, T. A. M. EuzÃ©bio, J. A. RamÃ­rez, and F. G. GuimarÃ£es, âUnmanned-aerial-vehicle routing problem with mobile charging stations for assisting search and rescue missions in postdisaster scenarios,â IEEE Trans. Syst., Man, Cybern. Syst., vol. 52, no. 11, pp. 6682â6696, Nov. 2022.

[33] M. Sun, X. Xu, X. Qin, and P. Zhang, âAoI-energy-aware UAV-assisted data collection for IoT networks: A deep reinforcement learning method,â IEEE Internet Things J., vol. 8, no. 24, pp. 17275â17289, Dec. 2021.

[34] S. Wu, C. Guo, Z. Deng, J. Jiao, N. Zhang, and Q. Zhang, âOptimizing age of information in adaptive NOMA/OMA/cooperative-SWIPT-NOMA system,â IEEE Trans. Wireless Commun., vol. 21, no. 12, pp. 11125â11138, Dec. 2022.

[35] C. Zhou, C.-K. Tham, and M. Motani, âLong-term incentives for contributor-initiated proactive sensing in mobile crowdsensing,â IEEE Trans. Syst., Man, Cybern. Syst., vol. 52, no. 3, pp. 1475â1491, Mar. 2022.

[36] Y. Liu, A. Liu, T. Wang, X. Liu, and N. N. Xiong, âAn intelligent incentive mechanism for coverage of data collection in cognitive Internet of Things,â Future Gener. Comput. Syst., vol. 100, pp. 701â714, 2019.

[37] Z. Zhan et al., âEnhancing worker recruitment in collaborative mobile crowdsourcing: A graph neural network trust evaluation approach,â IEEE Trans. Mobile Comput., vol. 23, no. 10, pp. 10093â10110, Oct. 2024.

[38] B. Waggoner and Y. Chen, âOutput agreement mechanisms and common knowledge,â in Proc. AAAI Conf. Hum. Comput. Crowdsourcing, 2014, pp. 220â226.

[39] Q. Li, Y. Li, J. Gao, B. Zhao, W. Fan, and J. Han, âResolving conflicts in heterogeneous data by truth discovery and source reliability estimation,â in Proc. ACM SIGMOD Int. Conf. Manage. Data, 2014, pp. 1187â1198.

[40] A. Thibbotuwawa, P. Nielsen, B. Zbigniew, and G. Bocewicz, âEnergy consumption in unmanned aerial vehicles: A review of energy consumption models and their relation to the UAV routing,â in Proc. 39th Int. Conf. Inf. Syst. Architecture Technol. Part II, Springer, 2019, pp. 173â184.

[41] Z. Zhou et al., âWhen mobile crowd sensing meets UAV: Energy-efficient task assignment and route planning,â IEEE Trans. Commun., vol. 66, no. 11, pp. 5526â5538, Nov. 2018.

[42] H. Van Hasselt, A. Guez, and D. Silver, âDeep reinforcement learning with double Q-learning,â in Proc. AAAI Conf. Artif. Intell., 2016, pp. 2094â2100.

[43] V. Mnih et al., âHuman-level control through deep reinforcement learning,â Nature, vol. 518, no. 7540, pp. 529â533, 2015.

[44] Z. Wang, T. Schaul, M. Hessel, H. Hasselt, M. Lanctot, and N. Freitas, âDueling network architectures for deep reinforcement learning,â in Proc. Int. Conf. Mach. Learn., PMLR, 2016, pp. 1995â2003.

[45] J. Yuan, Y. Zheng, X. Xie, and G. Sun, âDriving with knowledge from the physical world,â in Proc. 17th ACM SIGKDD Int. Conf. Knowl. Discov. Data Mining, 2011, pp. 316â324.

[46] R. Felismina, M. Silva, A. Mateus, and C. MalÃ§a, âStudy on the aerodynamic behavior of a UAV with an applied seeder for agricultural practices,â in Proc. Int. Conf. Appl. Math. Comput. Sci., AIP Publishing, 2017, Art. no. 020049.

[47] DJI.com, âDJI mavic 3,â 2021. Accessed: Jan. 11, 2023. [Online]. Available: https://www.dji.com/uk/mavic-3/specs

[48] R. I. Ansari, N. Ashraf, and C. Politis, âAn energy-aware distributed open market model for UAV-assisted communications,â in Proc. IEEE 91st Veh. Technol. Conf., 2020, pp. 1â6.

[49] Y. Zhou, R. Sun, S. Yu, Y. Sun, and L. Sun, âA complete coverage path planning algorithm for cleaning robots based on the distance transform algorithm and the rolling window approach in dynamic environments,â in Proc. IEEE 7th Annu. Int. Conf. CYBER Technol. Automat., Control, Intell. Syst., 2017, pp. 1335â1340.

<!-- image-->

<!-- image-->

<!-- image-->  
Yuxin Liu received the BE degree from the School of Information Science and Engineering, Central South University, China, in 2018, and the PhD degree from the School of Computer Science and Engineering, Central South University, China, in 2023. She is currently a lecturer with the College of Computer Science and Engineering, Changsha University, China. Her research interests are trust based network, edge computing, crowd sensing networks. She has published more than 30 papers in the field of edge computing, crowd sensing.

<!-- image-->

Anfeng Liu received the MSc and PhD degrees from Central South University, China, in 2002 and 2005, respectively, both in computer science. He is currently a professor with the School of Information Science and Engineering, Central South University, China. His major research interest is wireless sensor networks, Internet of Things, information security, edge computing and Crowdsensing.

<!-- image-->

Zhiwen Zeng received the BE degree in physics from Fudan University, China, in 1992, and the PhD degree from the school of Information Science and Engineering, Central South University, China, in 2011. He is a professor with the School of Computer Science and Engineering of Central South University, China. His major research interests are wireless sensor network and distributed computing.

Zhetao Li (Member, IEEE) received the BEng degree in electrical information engineering from Xiangtan University, in 2002, the MEng degree in pattern recognition and intelligent system from Beihang University, in 2005, and the PhD degree in computer application technology from Hunan University, in 2010. He is a professor with the College of Information Science and Technology, Jinan University. He is a member of CCF. His research interests include cloud computing, and artificial intelligence.

Qingyong Deng (Senior Member, IEEE) received the masterâs degree in signal and information processing from Xiangtan University, China, in 2009 and the PhD degree from the Beijing University of Posts and Telecommunications (BUPT), China, in 2019. He is a professor with the School of Computer Science and Engineering & School of Software, Guangxi Normal University, China. He has published more than 30 referred journal papers in his current research interests, including IoT, AI and wireless network.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_5_img_1.png|page_5_img_1]]
3. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_8_img_1.jpeg|page_8_img_1]]
4. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_10_img_1.jpeg|page_10_img_1]]
5. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_11_img_1.jpeg|page_11_img_1]]
6. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_12_img_1.jpeg|page_12_img_1]]
7. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_12_img_2.jpeg|page_12_img_2]]
8. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_12_img_3.jpeg|page_12_img_3]]
9. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_13_img_1.jpeg|page_13_img_1]]
10. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_13_img_2.jpeg|page_13_img_2]]
11. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_13_img_3.jpeg|page_13_img_3]]
12. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_13_img_4.jpeg|page_13_img_4]]
13. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_14_img_1.jpeg|page_14_img_1]]
14. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_16_img_1.jpeg|page_16_img_1]]
15. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_16_img_2.jpeg|page_16_img_2]]
16. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_16_img_3.jpeg|page_16_img_3]]
17. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_16_img_4.jpeg|page_16_img_4]]
18. [[../extracted_images/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS/page_16_img_5.jpeg|page_16_img_5]]

---

