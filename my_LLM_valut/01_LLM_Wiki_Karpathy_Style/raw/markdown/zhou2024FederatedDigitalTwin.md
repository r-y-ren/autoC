# A Federated Digital Twin Framework for UAVs-Based Mobile Scenarios

Longyu Zhou , Student Member, IEEE, Supeng Leng , Member, IEEE, and Qing Wang , Senior Member, IEEE

AbstractâWith the development of communication networks and Artificial Intelligence (AI) technologies, Digital Twin (DT) now emerges to support various applications such as engineering, monitoring, controlling, healthcare and the optimization of cyber-physical systems. There is an increasing demand to create DTs that can represent physical entities for improving operational efficiency. A conventional DT consists of monitoring, imitation, and feedback control. However, conventional DTs cannot ensure efficient real-time imitation due to the high dynamics of physical systems such as UAV-based target tracking scenario. To address this issue, we propose a federated DT framework to support the imitation of mobile systems. It can guarantee real-time and accurate imitations under the prerequisite of comprehensive information acquired by a cooperative collection algorithm with the aid of UAVs. The framework can rapidly aggregate local DT models using an attention-based mechanism to improve mobile imitation accuracy. Additionally, we propose a multimodal-based DT inspection algorithm that can correct the postures of UAVs affected by winds for reliable imitations. We implement the framework in Gazebo. Our system simulations demonstrate the efficiency of the proposed federated DT framework. Our solution can reduce the imitation latency by an average of 68.4%, meanwhile, can improve the imitation accuracy by 16.4% on average when compared to traditional centralized and distributed imitation schemes.

Index TermsâDigital twins, federated mobile imitation, target tracking, UAVs.

## I. INTRODUCTION

W ITH the ongoing development of the wireless commu-nication and manufacturing industry, Internet of Things nication and manufacturing industry, Internet of Things technology is rapidly serving emerging applications such as healthcare, intelligent logistics, and intelligent transportation for smart cities [1], [2], [3]. As one kind of potential mobile platform for IoT, Unmanned Aerial Vehicles (UAVs) play a significant role in replacing humans for the high efficiency of city management. With the advantages of flexibility and large-scale area sensing, UAVs can implement various missions such as package delivery, security monitoring for infrastructures, area surveillance, and target tracking [4], [5]. Taking the application in the Intelligent Transportation System (ITS) as an instance, UAVs can autonomously plan feasible mobile paths to monitor city traffic and transportation convoy. Once illegal targets such as hit-and-run vehicles are detected, UAVs can cooperatively collect the target data and transmit it to the cloud for mobility analysis. The cloud server may conduct reasonable tracking scheduling of UAVs for traffic safety.

Despite the superiority of flexibility for UAVs, some challenges still hinder tracking efficiency. First of all, UAVs cannot always sense mobile targets accurately since many inevitable physical obstacles like tunnels and buildings may block out the views of UAVs. These obstacles also reduce the efficiency of the information exchange for the cooperation among UAVs. Moreover, the challenges from surrounding environments such as wind shear directly affect the flight postures of UAVs [6]. Consequently, UAVs may not accurately observe the moving status of neighbors which further results in physical collisions. On the other hand, a long transmission distance from UAVs to the cloud server leads to a significantly high latency on data transmission. In this case, the cloud cannot provide accurate trajectory prediction based on traditional inertial prediction algorithms [7].

Fortunately, as a potential digital transformation technology, Digital Twin (DT) can assist UAVs with the design of a closedloop interaction pattern between the physical space and the virtual space. The DT is a set of virtual information that fully describes a potential or actual physical production from the micro level. It is also an integrated system that can simulate, monitor, calculate, regulate, and control the system status and process from the macro level [8]. In the tracking scenario, the DT can imitate the behaviors of mobile targets to acquire continuous moving trajectories based in mobility imitation in the virtual space. It can also adjust the number of imitation iterations to output different imitation results where the best result is selected for the accurate model derivation [9]. The derivation can optimize the flight paths of UAVs to avoid physical collisions in the physical space. In addition, the DT is promising to imitate and derive the changes of the wind speeds [10]. With the imitation and derivation, the DT can predict subsequent changes of winds to rapidly adjust the flight postures of UAVs for accurate target sensing and tracking.

However, the traditional cloud-based DTs are not feasible for highly-dynamic mobile scenarios. Such DTs could be unreliable since server breakdown can lead to direct imitation failures. A local and distributed DT system can ensure a reliable imitation while with a high management complexity [11]. The Mobile Edge Computing (MEC) approaches are capable of supporting mobile DT systems. However, the MEC cannot ensure reliable communications among all the UAVs in the large-scale mobile scenario. Thus, the edge server cannot obtain real-time target information to achieve a reliable DT, although Artificial Intelligence (AI) algorithms can run on the edge server to digest large amounts of physical data [12]. Nevertheless, both AI and DT conducted in the MEC servers will consume significant resources. A new DT system is expected to achieve highly reliable, accurate, and real-time mobile imitation performance.

In this paper, we design a flexible federated DT framework for the use case of mobile tracking of multiple highly-dynamic targets. We deploy a UAV hosting a lightweight mobile base station as an edge server flying in feasible airspace. It can conduct other UAVs to cooperatively collect target data in order to train accurate DT models. The model accuracy can be improved through a model aggregation operation on the edge server. When the edge UAV cannot provide reliable communications among the local UAVs, the UAVs can autonomously decompose into multiple groups where group leaders are elected to aggregate the DT models for the accurate imitation. We then propose a federated DT imitation algorithm in the framework to improve the efficiency of the DT system. The main contributions are summarized as follows.

We propose a flexible federated DT framework to perform accurate and real-time imitations for UAV-based multitarget tracking. The framework provides a possibility of DT derivation and aggregation for mobile scenario imitations. Explicitly, the DT can assist UAVs in mapping the trajectories and velocities of moving targets and neighbors of UAVs to digital spaces based on local observations. With DT models acquired from the digital spaces, the framework can perform a lightweight DT aggregation using an attention mechanism in the edge server. It can accurately imitate subsequent motions of targets and neighbors to optimize the tracking paths for collision avoidance and energy-saving in the physical scenario. In addition, it can select feasible DT models from historical experiences to derive the future motions of targets and neighbors with low-latency overheads.

- A new federated imitation algorithm is proposed to ensure the smooth operation of the DT system either with or without the support of an edge server. In the case of an available edge server, the server can dynamically adjust the positions and postures of UAVs to perform cooperative target sensing and imitation using our algorithm. The bidirectional cooperation can reduce the system imitation latency with non-redundant target data. When the edge server cannot meet reliable communications, UAVs can autonomously decompose into multiple groups to implement cooperative imitation by exchanging lightweight model parameters with low energy consumption in communications. Furthermore, when additional targets are involved, our algorithm can enable a model re-aggregation operation in real time to evaluate the trajectories and velocities of the targets involved by transferring similar DT models. The model transfer achieves a highly flexible imitation with respect to various numbers of targets.

<!-- image-->  
Fig. 1. Illustration of general digital twin procedure.

- We also propose a multimodal-based DT inspection algorithm to ensure the reliable imitation. The algorithm can adaptively update the model parameters to cope with the interference of wind based on joint consideration of historical imitation experiences, velocities and postures of UAVs, and wind speeds measured by sensors. Unlike the existing linear quadratic optimization method with a high exploration latency, ours uses a state prediction method that can correct the postures of UAVs in real time at different levels of wind speeds. We use Gazebo, a system simulation software, to set up a mobile imitation simulation system. The evaluation results demonstrate that our solution reduces the imitation latency by 68.4% on average when compared to the traditional centralized and distributed schemes. Our solution can also achieve a successful tracking ratio up to 95.0%.

The rest of this paper is organized as follows. The related work is given in Section II. Section III introduces the federated DT framework. The mobile DT optimization model is formulated in Section IV. The corresponding algorithms supporting the mobile DT framework are presented in Section V. Section VI provides the system evaluation results. Finally, Section VII concludes this paper.

## II. RELATED WORK

Many works have focused on DTs with particular merits, such as accurate estimation and real-time decision-making. With the system implementation procedure shown in Fig. 1, we present and summarize state-of-the-art studies from three parts: Data collection and transmission, Data processing, and Imitation implementation. In addition, we give latest work of DT-assisted UAV scenarios with the mentioned three parts in this section.

Data collection and transmission: The physical information can be collected and transmitted based on deployed sensors. To ensure data collection completeness, the authors in [13] proposed a sustainable data collection and management approach to construct digital twins for physical assets. It could optimize the metrics of data fidelity while ensuring sustainable information in a distributed pattern. An efficient data collection goal is achieved by relying on reliable transmission modes. In this case, the authors in [14] developed an application-driven digital twin networking middleware. It simplified the data interaction process based on an internet protocol. Moreover, the network transmission resource could be dynamically scheduled using a software-defined networking technology. These studies seem to be theoretically feasible for some specific applications with static physical entities.

To ensure the security of data during the data interaction in intrusion detection-based UAV networks, the authors in [15] proposed a federated continuous learning framework with a stacked broad learning system based on DT Networks. It can allow UAVs as edge servers to learn and train system models on new data quickly and continuously. Besides, the authors in [16] represented a dynamic DT-assisted resource scheduling and allocation approach to improve the utilization of sensing resources for effective data collection. The existing work of the DT-based UAV scenario mainly focuses on the learning accuracy and frequency of data updates while ignoring the consideration of UAV mobility. In this case, the authors in [17] proposed a Mobile Edge Computing (MEC) network with multiple UAVs and a DT-empowered ground Base Station (BS) to improve the MEC service. It can enable the BS to process data effectively based on optimal computing resource scheduling. Nonetheless, these state-of-the-art studies pay attention to the heterogeneity of data while neglecting the impact of the high dynamic of UAVs on data processing.

Data processing: To process data efficiently, the processor selection is the basis to cope with massive collected data. The authors in [18] proposed a DT-assisted task offloading scheme. It could deliver data of different physical entities to feasible edge servers using a channel state information detection method. After that, the processors need to estimate the data quality for accurate decision-making. To achieve the goal, the authors in [19] developed a data pre-processing and XGBoost-based learning method to perform data quality prediction in real time. It provided a new highly-precise quality prediction approach under a single-shot refinement neural network. With the high-quality data, the authors in [20] designed a hybrid deep neural network model to realize an efficient multi-type object detection for intelligent manufacturing applications based on feature fusion.

Imitation implementation: Imitation accuracy is important for feasible decision-making. The authors in [21] introduced a new concept to develop a robot DT for future robotized cyber-physical applications. It could capture robot information to facilitate insight and deliver capabilities based on a valuedriven method. The method achieved a low average imitation error with 1.52 Newton meters under 70 s imitation time. To make decisions in real time, the authors in [22] proposed a robot-centered smart DT framework to facilitate the deployment of robots in complicated environments. The framework could update robot actions and send them back to the robot with a feedback loop.

In the DT-assisted UAV network, the authors in [23] represented a novel DT-based intelligent cooperation framework. It can enable such large-scale UAV swarm imitation to perform deep swarm cooperation with the guidance of DT. The authors verified the prominent superiority of DT imitation with a trajectory planning case. To optimize to reduce the imitation latency in UAV networks, the authors in [24] represented a DT-enabled deep reinforcement learning training framework that can allow UAVs to acquire training models quickly with the help of DT.

<!-- image-->  
Fig. 2. Flexible federated DT framework.

The aforementioned DT researches are feasible to improve service effectiveness in some specific UAV scenarios. UAVs have the advantages of flexible sensing and miniaturization. However, the natural characteristics also lead to several disadvantages for existing studies. Firstly, few articles consider the impact of UAV mobility on the accuracy and reliability of DT imitation. Moreover, many researchers ignore the optimization of DT while paying close attention to the use of DT for particular applications. Furthermore, the impact of the physical environment on the DT capability must be considered for a reliable DT framework that supports UAV scenarios. In this case, enabling a flexible cooperative DT manner may be a feasible solution to ensure accurate and real-time imitation.

## III. SYSTEM MODEL

In this section, we propose a flexible federated DT framework. We leverage the multi-target tracking as the use case to explain the federated DT framework. It can perform real-time and accurate imitations in tracking multiple targets.

The proposed federated DT framework is shown in Fig. 2. UAVs can cooperatively observe mobile targets such as hit-andrun vehicles and collect their mobile information by exchanging lightweight position and velocity information. The set of UAVs is defined as $\mathcal { M } = \{ 1 , 2 , \dots , M \}$ and the set of mobile targets is denoted as $\mathcal { K } = \{ 1 , 2 , \dots , K \}$ . UAVs can train local observation information to acquire customized DT models. An edge UAV can fly in feasible airspace for cooperative mobile imitation. The edge UAV can decompose UAVs into multiple groups managed by elected group leaders. It can implement a model aggregation operation to construct a global virtual mobile scenario to accurately analyze and derive target mobility. The aggregated DT models are distributed to the corresponding UAVs to improve model accuracy of the local DT. However, the moving paths of UAVs are various that depend on the dynamic trajectories of targets. Edge servers cannot always acquire the position information of UAVs to implement the swarm decomposition operation under unreliable communication conditions. In this case, UAVs can autonomously decompose into multiple groups using the proposed swarm decomposition algorithm. In the group, UAVs can communicate with corresponding group leaders to implement cooperative DT imitation. In addition, group leaders can obtain DT models received from the local UAV members. These local DT models are aggregated and exchanged among neighboring group leaders. Based on this, UAVs can obtain DT models of neighboring groups to improve imitation accuracy instead of UAVs acquiring all DT models from all the group leaders. The cross-layered iteration manner also accelerates the consistency of imitation convergence for real-time DT imitation.

The edge UAV can run a DT inspection algorithm to correct and optimize the UAV tracking performance influenced by physical interference such as winds. However, the edge UAV cannot always support the mobile DT system due to dynamic of local UAVs. When the edge UAV is unavailable, UAVs can autonomously decompose into multiple groups based on collected target information. In each group, UAVs implement cooperative imitation to obtain local DT models and elect a feasible UAV for model aggregation and DT inspection. The aggregated models and inspection results are shared among different UAV groups to acquire a global mobile DT model for high imitation accuracy. In this context, we specifically describe the framework that is decoupled into three parts from the perspective of functions:

1) UAV local imitation and data exchange.

2) DT model aggregation.

3) DT inspection.

UAV local imitation and data exchange: We need to ensure a comprehensive and accurate target collection operation for the authenticity of data. The targets may be incorrectly sensed due to the change of posture of UAVs. We can analyze the sensing performance by formulating a probability model by defining the probability of incorrect sensing for UAV i sensing target k as $\bar { p } _ { i , k }$ . We assume that $c _ { k } \ \mathrm { U A V s }$ are allocated to sense target $k$ Â¯simultaneously. The assumption is reasonable because dynamic of UAVs allows multiple UAVs to sense target k at the same time slot t with $c _ { k } \geq 1 [ 2 5 ]$ ]. The successful sensing probability $p _ { k }$ is

$$
p _ { k } = \prod _ { i = 1 } ^ { c _ { k } } ( 1 - \bar { p } _ { i , k } ) > p _ { k , \operatorname* { m i n } } ,\tag{1}
$$

where $p _ { k , \mathrm { m i n } }$ is the minimal acceptable successful sensing probability. It mainly depends on sensing directions and angles of onboard sensors and physical distances among UAVs and targets directly [26]. On the one hand, UAVs can cooperatively adjust sensing directions and angles of onboard sensors to ensure effective data collection using the proposed cooperative sensing algorithm in Section V. The algorithm can also improve the sensing cooperation performance of UAVs by dynamically changing physical distances among UAVs and targets for accurate target sensing.

Based on the constraint, UAVs train self-sensing information to construct virtual mobile scenarios using 3D reconstruction method [27]. The features of the virtual scenario, such as target positions, postures, and velocities, are extracted to represent DT models. The DT models can assist UAVs in dynamically adjusting sensing postures for accurate information collection in return. The model exchange occurs between the UAVs and the edge server or happens among UAVs. Both two cases use Wi-Fi 6E technology [28]. The transmission rate $r _ { i , j }$ between UAV i and UAV j is

$$
r _ { i , j } = \sum _ { l } B _ { i , j } ( l ) \log _ { 2 } \left( 1 + \frac { P _ { i } ( l ) g _ { i } ( l ) } { \sigma ^ { 2 } } \right) ,\tag{2}
$$

where L is the number of sub-carriers, $B _ { i , j } ( l )$ is the transmission bandwidth of sub-carrier $l , P _ { i } ( l )$ and $g _ { i } ( l )$ ( )are the corresponding ( )transmission power and power gain, $g _ { i } ( l ) \sim f ( x | v , \delta )$ is a standard rice distribution with $v = 0$ and $\delta = 0 . 5 $ , and $\sigma \sim N ( 0 , \delta ^ { 2 } )$ = 0 = 0 5 (0 )is the zero mean Gaussian variable with a standard deviation Î´. The transmission rate model between the UAV i and the edge is similar only with the different $B _ { i , e }$ allocated by the edge server. In this case, each edge UAV can obtain all the DT models of group members by dynamically electing the group leader with reliable communications. However, the change in the physical environment may make partial UAVs isolated. On the one hand, isolated UAVs can use local DT models to autonomously plan suitable tracking paths through the trajectory prediction of targets. Meanwhile, the UAVs implement information broadcast operations to join the nearest group for reliable UAV connections during the tracking imitation. On the other hand, edge UAVs can implement DT model derivation operations based on the model aggregation result. It can assist edge UAVs with adjusting association decisions among UAVs and targets for accurate mobile imitation.

DT model aggregation: UAVs can transmit their local model parameters to the edge server. The parameters mainly include features of UAVs, sensed targets, and corresponding neighbors. It is represented as $\mathrm { D T } _ { i } \left( h _ { i } , \mathbf { H } _ { i } , \mathbf { h } _ { i , k } \right)$ , where $h _ { i }$ is the features ( )of UAV i, including flight position, posture, velocity, height, physical distances with neighbors and targets, as well as terrain information. The $h _ { i }$ is a vector that can index the neighbor feature $\mathbf { H } _ { i } = \{ h _ { i } , h _ { i + 1 } , \cdot \cdot \cdot \}$ and target feature $\mathbf { h } _ { i , k }$ to constitute DTi $( h _ { i } , { \bf H } _ { i } , { \bf h } _ { i , k } )$ . The detailed expressions are given in ( )Section V. When the edge server is available, it can analyze the relations among different parameters through a global view. The aggregation process is implemented by a cross-layered iteration between the UAVs and the edge server. The edge server uses an attention-based mechanism to accelerate the model aggregation process. The aggregated models are distributed to the local UAVs for further imitations.

Edge servers cannot always acquire the position information of UAVs to implement the swarm decomposition operation under unreliable communication conditions. In this case, UAVs need to perform an autonomous decomposition behavior. Specifically, Specifically, UAV i can acquire physical distances with the targets moving in their sensing ranges using onboard sensors. The distance information is represented as a vector $d _ { i }$ , where $d _ { i } = [ d _ { i , 1 } , d _ { i , 2 } , \ldots , d _ { i , k } ]$ and $d _ { i , k } = \infty$ if UAV i cannot sense target k. UAV i can associate the nearest target k with the shortest physical distance $d _ { i , k }$ based on a K-means methodology [29].

The association result is exchanged with neighbors. Those UAVs associating with the same target can form a group for accurate tracking imitation. When the decomposition result cannot make UAVs associate all the targets, UAVs can select the multiple closest targets based on the vector $d _ { i }$ until sensing all the targets. In addition, this network can provide desired communication bandwidth for UAV groups to perform reliable information exchange among UAVs for accurate mobile imitation based on Wi-Fi 6E technology. The group leader receives the model parameters of UAVs to implement the model aggregation operation. The aggregation models are exchanged among different group leaders for acquiring global information. In addition, the group leaders use the attention-based mechanism to further aggregate DT models and distribute them to the group members.

DT inspection: The inspection operation is run on the edge server based on historical imitation experience, environmental information, and the aggregated models. On one hand, the inspection can optimize imitation performance for cooperative tracking among UAVs with feasible mobile paths. The environmental information is considered as a reference metric to ensure inspection accuracy. The inspection results are used to further optimize the DT models on the edge server. On the other hand, the inspection operation can make the imitation process more reliable with the consideration of different speeds of winds in physical scenarios. It is thought to have a noticeable impact on the UAV tracking [6]. The inspection can assist UAVs in adjusting flight postures for accurate data collection and physical collision avoidance during the tracking process under the influence of wind.

When the edge server is not available, the elected group leaders can implement the inspection operation using a multimodalbased learning algorithm. The lightweight inspection results are exchanged among groups to obtain consensus decisions for accurate mobile imitation. The decisions are also distributed to the local UAVs for tracking targets. The operation reduces the imitation error and optimizes the system energy consumption which is reflected in the physical tracking performance. The inspection results are cached in UAVs as historical imitation experiences for further imitations.

## IV. PROBLEM FORMULATION

In this section, we formulate a federated DT optimization model to ensure real-time and accurate mobile imitations.

## A. Sensing and Transmission Analysis

We discuss two different cases to analyze the performance of sensing and transmission. When there are no sensed mobile targets in the monitoring area, UAVs imitate themselves and one-hop neighbors to perform a cooperative mission implementation. The other case is to add the imitation of targets. In the first case, the sensing latency is mainly considered for collecting the information of neighbors. It is noted that the self-sensing latency can be neglected in a wired manner. In the second case, the sensing latency incorporates neighbor sensing and target sensing. It is assumed that A onboard sensors can be simultaneously enabled to collect the relevant information. The latency overhead $t _ { i , s }$ is given by:

$$
t _ { i , s } = \operatorname* { m a x } \left\{ \frac { q _ { i } ^ { 1 } } { b _ { 1 } } , \frac { q _ { i } ^ { 2 } } { b _ { 2 } } , \ldots , \frac { q _ { i } ^ { a } } { b _ { a } } , \ldots , \frac { q _ { i } ^ { A } } { b _ { A } } \right\} ,\tag{3}
$$

where $b _ { a }$ is the sensing frequency of sensor $a ; q _ { i } ^ { a }$ is the acquired data (bits) from the sensor $a .$ The sensing rate $b _ { a }$ is mainly constrained by sampling rate, the number of sensing channels, Analog-to-Digital Converter (ADC) resolution [30]. We explore the feasible sample rates to meet accurate and real-time data collection requirements through power controls of onboard sensors [31]. The sensing frequency can be dynamically adjusted to meet effective information collection for accurate mobile imitation [32].

With the sensing information, UAVs can implement a local imitation to construct a virtual space to acquire a local DT model. In this case, there exist two data transmission directors for UAVs. The first one is that UAV i transmits its model parameters to the edge server for the model aggregation (details are represented in Section V). The size of model parameters is small which can be defined as a constant value $u _ { i }$ . The second one is that UAV i exchanges its partial model parameters and high-priority information, such as flight positions, with neighbors to avoid physical collisions. We formulate the communication latency $t _ { i , c }$ for both two cases:

$$
t _ { i , c } = \operatorname* { m a x } \left\{ \frac { \sum _ { a = 1 } ^ { A } q _ { i } ^ { a } } { r _ { i , 1 } } , \frac { \sum _ { a = 1 } ^ { A } q _ { i } ^ { a } } { r _ { i , 2 } } , . . . , \frac { \sum _ { a = 1 } ^ { A } q _ { i } ^ { a } } { r _ { i , j } } \right\} + \frac { u _ { i } } { r _ { i , e } } .\tag{4}
$$

We expect to reduce latencies of sensing and communication under a given threshold $t _ { \mathrm { s c , m a x } }$ for the real-time imitation. The corresponding constraint is formulated as

$$
t _ { i , s } + t _ { i , c } < t _ { \mathrm { s c , m a x } } .\tag{5}
$$

## B. Mobile Imitation Analysis

1) Mobile Imitation Latency: UAVs can implement DT imitation based on the collected information. The collected environment information is used to build digital space using 3D modeling technology [27]. Meanwhile, information of UAVs and targets is used to construct digital twins for acquiring corresponding DT models using data fusion technology [33]. These technologies acquire the support of computing resources of UAVs. From (4), we can know that UAV i can collect $\textstyle \sum _ { a = 1 } ^ { A } q _ { i } ^ { a }$ bits of data. The number of Central Process Unit (CPU) cycles for computing one-bit data for UAV i is denoted as $c _ { i } .$ . The imitation latency $\xi _ { i }$ of UAV i is represented as $\begin{array} { r } { \xi _ { i } = \frac { \sum _ { a = 1 } ^ { A } q _ { i } ^ { a } c _ { i } } { b _ { i } } } \end{array}$ ï¼ where $b _ { i }$ = denotes the number of CPU cycles in a unit of time for UAV i. We can draw that imitation latency is dependent on the CPU frequency, data size, and computing capability of UAVs. The edge servers then receive local DT models to implement data aggregation operations. Similarly, the edge imitation latency $\begin{array} { r } { \xi _ { e } = \frac { \sum _ { i = 1 } ^ { M } D _ { i } c _ { e } } { b _ { e } } } \end{array}$ , where $D _ { i }$ is the received data sizes from UAV $i ; c _ { \epsilon }$ =and $b _ { e }$ are the number of CPU cycles for one-bit data and the number of CPU cycles in a unit of time for edge server e. The imitation decisions are distributed to local UAVs for tracking implementation. The small-sized data size from edge server e to

UAV i is represented as $U _ { e , i }$ . The feedback latency $\xi _ { i , d }$ is $\frac { U _ { e , i } } { r _ { e , i } }$ where $r _ { e , i }$ is transmission rate based on (4). We assume that all the imitation results reach convergence after p iterations. With the maximal acceptable imitation latency $t _ { \xi , \mathrm { m a x } }$ , the imitation latency is constrained as

$$
\begin{array} { r l r } {  { \sum _ { p } \big [ \operatorname* { m a x } \{ \xi _ { 1 } , \xi _ { 2 } , \dots , \xi _ { i } \} + \xi _ { e } } } \\ & { } & { + \operatorname* { m a x } \{ \xi _ { 1 , d } , \xi _ { 2 , d } , \dots , \xi _ { i , d } \} \big ] < t _ { \xi , \operatorname* { m a x } } . } \end{array}\tag{6}
$$

2) Mobile Imitation Accuracy: We give a highly-accurate imitation solution using a local model aggregation algorithm which is specifically described in Section V. The aggregated model for UAV i is formulated as $\mathrm { D T } _ { i , \Phi }$ , where is a set Î¦of model parameters obtained according to features of UAV i and neighbors $\mathbf { H } _ { i } = \{ h _ { i } , h _ { i + 1 } , \cdot \cdot \cdot \}$ . The $\mathrm { D T } _ { i , \Phi }$ is used to =predict the mobile trajectories. The aggregated model can be further optimized by a proposed DT inspection algorithm. This algorithm can inspect the current imitation performance. The inspection results are applied to correct moving paths of UAVs in advance through trajectory prediction of targets. A closed-loop prediction is formulated as

$$
\psi _ { k } ^ { \prime } = \left[ { \begin{array} { l } { x _ { k } ( 1 ) , x _ { k } ( 2 ) , \cdots , x ( t ) } \\ { x _ { k } ( 2 ) , x _ { k } ( 3 ) , \cdots , x _ { k } ( t + 1 ) } \\ { \vdots \vdots \quad \ddots , \quad \vdots } \\ { \vdots \quad } \end{array} } \right] \left[ { \begin{array} { l } { \chi _ { 1 } } \\ { \chi _ { 2 } } \\ { \vdots } \\ { \chi _ { i } } \\ { \vdots } \\ { \chi _ { m } } \end{array} } \right] ,\tag{7}
$$

where $\chi _ { m }$ is the estimation coefficient; $x _ { k } ( t )$ is the position ( )coordination of target k at time t [34]. In this case, we can constrain the imitation error under an acceptable $\psi _ { i , \mathrm { { m i n } } }$ with real trajectories (ground truth) collected in advance:

$$
\| \psi _ { k } - \psi _ { k } ^ { \prime } \| < \psi _ { k , \operatorname* { m i n } } .\tag{8}
$$

The constraint is optimized by our DT inspection algorithm.

## C. Objective Formulation

The imitation energy consumption in the unit time for UAV i is $b _ { i } \xi _ { i }$ . Based on dynamic voltage and frequency scaling technology [35], UAV i can adjust the CPU working frequency $f _ { i , u }$ for each cycle u to control the energy consumption, where $f _ { i , u } \in$ $( 0 , f _ { i , \operatorname* { m a x } } ) ; f _ { i , \operatorname* { m a x } }$ is the maximal CPU frequency. From [36], we know that power consumption is proportional to the cubic frequency:

$$
E ( \xi _ { i } ) = \sum _ { u = 1 } ^ { b _ { i } \xi _ { i } } \kappa _ { i } f _ { i , u } ^ { 3 } ,\tag{9}
$$

where $\kappa _ { i }$ is the efficient capacitance coefficient that depends on the clip characteristic. It is noted that computing consumption is neglected for computing-intensive edge servers. The imitation

consumption is constrained by the maximal energy budget $B _ { \mathrm { m a x } } i$

$$
\sum _ { i } { ( E ( \xi _ { i } ) ) } < B _ { \mathrm { m a x } } .\tag{10}
$$

To accelerate the imitation process with a highly-accurate performance, we invoke the Lyapunov methodology to formulate the optimization model:

$$
P 1 : \operatorname* { m i n } \left\{ \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T } \left[ \sum _ { i = 1 } ^ { M } \sum _ { k = 1 } ^ { K } ( \beta _ { 1 } \Delta \xi _ { i } + \beta _ { 2 } \Delta \psi _ { k } ) \right] \right\} ,
$$

$$
\mathrm { s . t . } \left\{ { C 1 : ( 5 ) , ( 1 0 ) , \forall k \in \mathcal K } \right.\tag{11}
$$

where $\beta _ { 1 }$ and $\beta _ { 2 }$ are weight coefficients used to tradeoff realtime and accurate tracking metrics; $\Delta \xi _ { i } = L _ { 1 , i } - L _ { 2 , i }$ , where $L _ { 1 , i }$ and $L _ { 2 , i }$ Î =denote the actual imitation time and expected imitation time, respectively. We aim to reduce the actual imitation time $L _ { 1 , i }$ to make it close to the expected imitation time $L _ { 2 , i }$ with a drift plus penalty method for real-time mobile imitation [37]. Similarly, $\Delta \psi _ { k }$ ensures accurate mobile imitation. In Îterms of constraints, (5) ensures low-latency target sensing and information exchange among UAVs. Equation (10) makes UAVs perform a low-energy DT imitation. C2 is the constraint of the transmission rate, ensuring low-latency information exchange operations among UAVs for effective tracking cooperation.

## V. FEDERATED MOBILE DIGITAL TWINS

In this section, we present our federated DT solution. We decouple the complex mobile imitation problem into three subproblems for clear analysis: cooperative sensing, DT model aggregation, and DT inspection.

## A. Cooperative Sensing

The Value Decomposition Network (VDN) algorithm can decompose the complex UAV sensing problem into multiple sub-problems for accurately learning cooperative sensing decisions [38]. It is implemented by fully decomposing actionvalue functions of all the UAVs. It can significantly improve the computing energy consumption of the UAV system with high computing complexity. The QMIX is an attractive learning algorithm to ensure consistency of UAV sensing without fully action-value decomposition operation [39]. Nonetheless, it cannot effectively learn to dynamically adjust the sensing positions of UAVs due to the undetermined numbers of UAVs and targets involved. To ensure cooperative sensing in the proposed federated DT framework, we propose a Deep Deterministic Policy Gradient (DDPG)-based cooperative sensing algorithm. It can ensure comprehensive data collection in the continuous sensing process by dynamically scheduling sensing resources of UAVs. The high-efficiency sensing resource utilization can also assist UAVs in acquiring states of targets and one-hop neighbors for non-redundant sensing data. As shown in Fig. 3, the information of UAV i and its neighbors are used to construct the state space $S _ { i }$ of UAV i under the DDPG architecture. The architecture can assist UAV i in obtaining feasible sensing actions. The actions can be optimized and updated through information exchange with neighbors. The action space $A _ { i }$ is built to provide available actions for UAV i. The selected sensing actions from $A _ { i }$ can be estimated using a critic network with an estimation function. The estimation criterion is given by formulating a reward function $R _ { i }$ which can assist UAVs in reaching a cooperative sensing consensus. We can quantify the process as a stochastic game problem with a tuple $\{ S _ { i } , A _ { i } , \mathcal { T } , R _ { i } \}$ , where T is a transfer function to give the next state $S _ { i } ( t + 1 ) \gets S _ { i } ( t ) \times A _ { i }$ . The state space $S _ { i }$ is composed of three parts:

<!-- image-->  
Fig. 3. Illustration of cooperative sensing.

1) States of $\mathrm { U A V } ~ i ; h _ { i }$

2) States of one-hop neighbors: $\mathbf { H } _ { i }$

3) States of mobile targets: $\mathbf { h } _ { i , k } .$

The action space $A _ { i } = \{ U _ { i } , \{ V _ { i } \} \}$ , where $U _ { i }$ is the current sensing action; {Vi} is the set of selected neighbors for information exchange. Based on this, we formulate a loss function $L ( \theta ^ { Q } )$ with which UAVs can obtain sensing consensus results ( )based on the Bellman equation:

$$
L ( \theta ^ { Q } ) = E _ { S , A , R } \left[ \sum _ { i } \left( Q ^ { \theta ^ { \mu } } ( S _ { i } , A _ { i } ) - Y \right) ^ { 2 } \right] ,\tag{12}
$$

where $\theta ^ { Q }$ and $\theta ^ { \mu }$ are hyper-parameters of the action network; $Y = \Re _ { i } + \gamma Q ^ { \theta ^ { \mu } } ( S _ { i } , A _ { i } ) | _ { A _ { i } ^ { \prime } = \mu _ { i } ^ { \prime } ( S _ { i } ) } ; \gamma$ is the discount factor. The hyper-parameter $\theta ^ { \mu }$ can be updated as $\theta ^ { \mu ^ { \prime } }$ during the training process. The action $A _ { i }$ will be updated as $A _ { i } ^ { \prime }$ . To obtain a consensual sensing decision, we formulate a policy gradient function ${ \cal J } ( \theta ^ { \mu } )$ which can explore the optimal gradient direction of the $\theta ^ { \mu , }$

$$
\nabla _ { \theta ^ { \mu } } J ( \theta ^ { \mu } ) = E _ { \mathrm { { R m } } } \left[ \sum _ { i } \nabla _ { \theta ^ { \mu } } \mu ( A _ { i } | S _ { i } ) \nabla _ { A _ { i } } Q ^ { \mu } ( S _ { i } , A _ { i } ) | _ { A _ { i } = \mu ( S _ { i } ) } \right] .\tag{13}
$$

The output action is then estimated under the reward function $R _ { i }$ which considers completeness and redundancy of data simultaneously. The $R _ { i }$ is given by

$$
R _ { i } ( S _ { i } , A _ { i } ) = f _ { i } ( h _ { i , k } ) - t _ { i , s } - \| D _ { i , k } - D _ { j , k } \| _ { 2 } ,\tag{14}
$$

where $f _ { i } ( h _ { i , k } )$ is a function representing the efficient data col-(lected by $\mathrm { U A V } \ i ; \ \lVert D _ { i , k } - D _ { j , k } \rVert$ denotes overlapped sensing areas between UAV i and $j .$ . The intersections of sensing areas among UAVs are expected to reduce for non-redundancy and comprehension of data.

However, the current reward function may make a UAV immoderately consume sensing resources. Thus, we invoke a resource equilibrium mechanism to optimize $R _ { i }$ as $\Re _ { i }$

$$
\begin{array} { r l } & { \mathbb { R } _ { i } ( S _ { i } , A _ { i } ) = R _ { i } ( S _ { i } , A _ { i } ) } \\ & { \quad \quad \quad + \frac { \alpha _ { i } } { \mathrm { c a r d } ( V _ { i } ) } \operatorname* { m a x } \left( R _ { j } ( S _ { j } , A _ { j } ) - R _ { i } ( S _ { i } , A _ { i } ) , 0 \right) } \\ & { \quad \quad \quad + \frac { \beta _ { i } } { \mathrm { c a r d } ( V _ { i } ) } \operatorname* { m a x } \left( R _ { i } ( S _ { i } , A _ { i } ) - R _ { j } ( S _ { j } , A _ { j } ) , 0 \right) , } \end{array}\tag{15}
$$

where card $( V _ { i } )$ is the number of one-hop neighbors of UAV $i ; \alpha _ { i }$ and $\beta _ { i }$ )are usually set as 5 and 0.05, respectively [40]. The current state-action pair is cached to the Rm. The action is estimated in the critic network using the chain rule [41]:

$$
\begin{array} { l } { { \nabla _ { \theta ^ { C } } J ( \theta ^ { C } ) = E _ { S , A \sim \mathrm { R m } } \Bigg [ \displaystyle \sum _ { i } w _ { i } ( \theta ^ { C } ) \nabla _ { C _ { i } } \mu ( A _ { i } | C _ { i } ) } } \\ { { \times \nabla _ { A _ { i } } Q ^ { \mu } ( S _ { i } , A _ { i } ) \vert _ { A _ { i } = \mu ( S _ { i } ) } \Bigg ] , } } \end{array}\tag{16}
$$

where $w _ { i } ( \theta ^ { C } )$ is a function to adjust connections between two ( )neural network layers; $\theta ^ { C }$ is the hyper-parameter of the critic network to optimize the current action based on the reward function. The optimization process is given using a loss function $L ( \theta ^ { C } )$ in the critic network:

$$
\begin{array} { r l } & { L ( \theta ^ { C } ) = - \Delta \hat { Q } _ { i } \log \left( p ( \theta ^ { C } | \theta ^ { \mu } ) \right) } \\ & { - \left( 1 - \hat { Q } _ { i } \right) \log \left( 1 - p ( \theta ^ { C } | \theta ^ { \mu } ) \right) . } \end{array}\tag{17}
$$

The cooperative sensing is implemented by Algorithm 1.

Based on Algorithm 1, UAVs can acquire comprehensive data for accurate mobile imitation. However, there may exist some redundant data due to multiple sensors collecting data simultaneously. we invoke a data prune method to obtain lightweight local DT models with effective and non-redundant data [42]. UAV i collects $D _ { i }$ bits of data based on the proposed cooperative sensing algorithm, where $D _ { i } = \{ D _ { i , 1 } , . . . , D _ { i , a } , . . . , D _ { i , A } \}$ . We ex-=pect to reduce the data redundancy with -redundant mechanism:

$$
\| \Delta D _ { i , a } \| _ { 2 } \leq \epsilon ,\tag{18}
$$

where $\Delta D _ { i , a }$ is the difference between any two kinds of data Îfrom different sensors;  is a constant value. The specific implementation steps are given as follows.

S1. Set $D _ { i } = \{ D _ { i , 1 } , D _ { i , 2 } , \dots , D _ { i , a } , \dots , D _ { i , A } \} .$

=S2. Build neural network using Ï and loss function L.

S3. Give the expected .

$$
\begin{array} { r } { \mathrm { S 4 . ~ L e t } \hat { \vartheta } = \arg \operatorname* { m i n } _ { \vartheta } \frac { 1 } { A } \sum _ { D _ { i , a } } L ( D _ { i , a } , \vartheta ) . } \end{array}
$$

S5. Compute ${ \hat { \vartheta } } .$

S6. Initialize $\mathbb { S } = \emptyset .$

=S7. Construct Hessian and positive definite matrix: $H _ { \hat { \vartheta } } =$ $\begin{array} { r } { \frac { 1 } { n } \sum _ { D _ { i , a } } \bigtriangledown _ { \vartheta } ^ { 2 } L ( D _ { i , a } , \hat { \vartheta } ) . } \end{array}$

(S8. Set a discrete variable $W \in \{ 0 , 1 \} ^ { n }$

S9. Maximize $\textstyle \sum _ { a = 1 } ^ { A } W _ { a }$ under $\| W ^ { T } \mathbb { S } \| _ { 2 } \leq \epsilon$ and Step 7.

S10. Compute $D _ { \epsilon , \operatorname* { m a x } } = \{ D _ { i , a } | \forall D _ { i , a } , W _ { a } = 1 \}$

=S11. Remove redundant data: $D \gets D \backslash D _ { \epsilon }$ ,max.

The method can assist UAVs in acquiring lightweight DT models through reducing data redundancy. With such a model,

Algorithm 1: Cooperative Sensing.   
Input: Observation information $S _ { i } ;$ DDPG network   
parameters $\theta ^ { Q } , \theta ^ { \mu } ;$ discount factor $\gamma ;$ action   
parameter $\theta ^ { C }$ and $\theta ^ { a } ;$ replaymemory Rm.   
Output: The cooperative target sensing decision.   
Definition: $\gamma = 0 . 9 9$   
1 for each episode in all rounds do   
2 Obtain the selected neighbors of UAV i   
3 for each time slot t do   
4 foreachUAViin Mdo   
5 Construct a mobile scenario by $S _ { i }$   
6 $a _ { i } \longleftarrow \mu _ { \theta _ { i } } ( S _ { i , t } ) + N _ { t }$   
if UAV i has overlapped areas with j then   
8 Implement action selection by Eq. (12)   
9 Obtain the feasible action by Eq. (13)   
10 if j performs the same action then   
11 Remove $\theta ^ { Q _ { j } }$ and $\theta ^ { \mu _ { j } }$   
12 Store the state-action pair to Rm   
13 Compute the reward by Eq. (15)   
14 Compute the gradient by Eq. (16)   
15 Optimize the action by Eq. (17)

UAVs can exchange lightweight model parameters for an accurate and real-time mobile imitation.

## B. DT Model Aggregation

With the cooperative sensing results, UAV i can collect efficient information to train a local DT model $\mathrm { D T } _ { i } \left( h _ { i } , \mathbf { H } _ { i } , \mathbf { h } _ { i , k } \right)$ ( )The model can replicate mobile targets to the virtual space through real-time information collection and updates. The imitation results are transmitted to the edge server for model optimization. We provide a macro-viewed DT imitation on the edge side with a model aggregation operation. It can assist UAVs in improving imitation accuracy. In addition, UAVs can autonomously decompose themselves into multiple groups based on an effective decomposition method [43]. A feasible UAV is elected as group leader in each group using the betweenness centrality method:

$$
\operatorname* { m a x } _ { v } \left\{ g ( v ) = \sum _ { i \neq v \neq j } \frac { \zeta _ { i j } ( v ) } { \zeta _ { i j } } \right\} ,\tag{19}
$$

where $g ( v )$ is the betweenness centrality of UAV v; $\zeta _ { i j }$ is the ( )total number of shortest paths from UAV i to $j ; \zeta _ { i , j } ( v )$ is the number of paths passing through v.

We propose an attention-based model aggregation algorithm shown in Fig. 4. Considering the high processing time for the amounts of data, we use a key-value association rule where we can process a lightweight $\omega _ { i }$ with necessary features instead of the large-sized data Hi [44]. Explicitly, we formulate a comparison function $\Theta ( \mathrm { D T } _ { i , \Phi } ; \mathrm { D T } _ { i } ( h _ { i } , { \bf H } _ { i } , { \bf h } _ { i , k } ) , \omega _ { i } )$ to estimate the performance of local model $\mathrm { D T } _ { i } \left( h _ { i } , \mathbf { H } _ { i } , \mathbf { h } _ { i , k } \right)$ , where $\mathrm { D T } _ { i , \Phi }$ ( )is an ideal optimization result. The function shows that if the value is smaller, the model performance is better. With the comparison function, we expect to acquire the optimal $\omega _ { i } ^ { * }$ :

<!-- image-->  
Fig. 4. Illustration of model aggregation.

$$
\begin{array} { l } { { \displaystyle { \omega } _ { i } ^ { * } = \arg \operatorname* { m i n } _ { \omega _ { i } } \frac { 1 } { \mathrm { c a r d } ( V _ { i } ) } \sum _ { i = 1 } ^ { \mathrm { c a r d } ( V _ { i } ) } } } \\ { { \displaystyle ~ \times E \left[ \Theta \left( \mathrm { D T } _ { i , \Phi } ; \mathrm { D T } _ { i } ( h _ { i } , { \bf H } _ { i } , { \bf h } _ { i , k } ) , \omega _ { i } \right) \right] } . } \end{array}\tag{20}
$$

It is feasible to optimize the function  by continuous itera-Îtions between the edge server and UAVs. However, the iteration latency may be unacceptable for high-speed moving targets. We invoke an attention mechanism to accelerate the aggregation process in each round of iteration. In detail, the parameter Ïj is optimized by a multiple layers perception network shown in Fig. 4. An encoder-decoder architecture is designed according to the deep learning ideology [45]. For the encoder operation, the feature parameters of UAV i are input into the neural network. The original state space is mapped to a new feature space with a lightweight conversion operation $\omega _ { i , j } = f ( h _ { i , j } , W _ { i , j } ^ { k } )$ ï¼ where $W _ { i , j } ^ { k }$ is a weight value that can be adjusted based on the similarity between UAV i and $j$ with the same sensed target k. The decoder operation is implemented by the activation function $\exists _ { i } = \omega _ { i } ^ { t } W _ { i , j } ^ { q }$ , where $W _ { i , j } ^ { q }$ is a hyper-parameter. We can use = tanhfunction to obtain the aggregation probability between UAV i and $j \colon$

$$
e _ { i , j } = \operatorname { t a n h } { ( \mathbb { \tilde { \partial } } _ { i } \omega _ { i , j } ) } ,\tag{21}
$$

where $e _ { i , j }$ is a probability vector; $w _ { i }$ is updated as $w _ { j }$ when $e _ { i , j } > 0 . 5 ; w _ { i }$ replaces $w _ { j }$ when $e _ { i , j } < - 0 . 5$

0 5 0 5The algorithm can dynamically updating the lightweight $W _ { i , j } ^ { k }$ instead of re-training for different tracking scenarios with different numbers and speeds of targets. The value represents the mobile feature of targets which can reflect the change frequency in the mobile velocity and the posture. When the change of velocity of a target is high-frequent, the corresponding weight is adjusted to highlight the mobile feature. In this case, when other targets are involved, we only add their lightweight feature information to the input queue. The historical learning parameters similar to the feature information are transferred to the new round of model aggregation for real-time imitation. The model aggregation is implemented by Algorithm 2.

Algorithm 2: Model Aggregation.   
Input: Observation information $S _ { i } ^ { e } { ; }$ DDPG network   
parameters $\theta ^ { Q }$ / $\theta ^ { \mu } ;$ updatedweighted $\gamma ;$   
Action parameter $\stackrel { \cdot } { \theta ^ { C ^ { \prime } } }$ and $\theta ^ { a } ;$ parameter   
vector V.   
Output: The optimal aggregation decision.   
1 Obtain sensing decisions in Algorithm 1   
2 Construct DT model $\mathrm { D T } _ { i } ( h _ { i } , \bar { { \bf H } _ { i } } , { \bf h } _ { i , k } )$   
3 if edge server is reachable then   
4 for each UAV j âVi do   
5 if j is neighbor of i then   
6 Map $h _ { j }$ toWj   
7 Aggregate model parameters using   
Eq. (20)   
8 Obtain the output action $A _ { i } ^ { * }$ by Eq. (21)   
9 if other UAVs involue then   
10 Adjust parameter weights in the edge side   
11 Implement re-aggregation operation   
12 if edge server is unavailable then   
13 for each UAV i do   
14 Implement decomposition operation   
15 Select feasible group leaders by Eq.(19)   
16 for each group do   
17 Aggregate model parameters by Eq. (20)   
18 Exchange DT models and compute $A _ { i } ^ { * }$ by   
Eq. (21)   
19 if other UAVs involue then   
20 Adjust parameter weights in group leaders   
21 Implement re-aggregation operation

## C. DT Inspection

Many state-of-the-art investigations have tried to design synchronous algorithms between the physical space and the virtual space for the high imitation accuracy [46]. However, it is difficult to give a real-time synchronization method due to various influences including the different capabilities of sensors, dynamic communication environments, and inevitable imitation latency. In this case, we give an inspection method instead of eliminating the system latency for imitation synchronization in the federated DT to ensure the imitation accuracy by adding a feedback loop.

Explicitly, UAVs transmit historical imitation data and selffeature information to edge servers for the DT inspection operation. It avoids potential physical collisions among UAVs, and reduces system energy consumption by analyzing mobile trajectories. Based on this, we propose a DT inspection algorithm that can jointly consider the historical imitation data and the current states of UAVs. Fig. 5 shows our algorithm from two perspectives: states of UAVs and historical data. The inspection process may be time-consuming due to the amounts of state information. With the aid of the model aggregation algorithm, we can select representative features based on $\omega _ { i }$ to input to multimodal learning architecture where we invoke the actor-network of the DDPG architecture to support the learning stage. We can construct an input matrix in which rows are filled by UAV features. It is noted that the matrix is sparse due to only filling the representative features. In this case, we expect to narrow the gap between the prediction value $\psi _ { k } ^ { \prime }$ in (7) and the ground truth $\psi _ { k }$ collected in the practical scenario:

<!-- image-->  
Fig. 5. Illustration of DT inspection.

$$
\operatorname* { m i n } \sum _ { i } ^ { M } \sum _ { k } ^ { K } \| \psi _ { k } - \psi _ { k } ^ { \prime } \| .\tag{22}
$$

With the learning result, we formulate an action-value function $V ( S _ { i } )$ which is derived by the Hamilton Jacobi-Bellman ( )equation [47]:

$$
\frac { 1 } { \tau } V ( S _ { i } ) = \operatorname* { m a x } _ { A _ { i } } \left[ \frac { 1 } { \| \psi _ { i , k } - \psi _ { i , k } ^ { \prime } \| } + \frac { \partial V ( S _ { i } ) } { S _ { i } } f ( S _ { i } , A _ { i } ) \right] ,\tag{23}
$$

where $\tau$ is a given discount factor. Based on the equation, we can explore feasible training direction to acquire the optimized mobile action $A _ { i } ^ { * }$ using a greedy policy:

$$
A _ { i } ^ { * } = D \left( \frac { \partial f ( S _ { i } , A _ { i } ) } { \partial A _ { i } } \frac { \partial V ( S _ { i } ) } { \partial S _ { i } } \right) ,\tag{24}
$$

where $D ( x )$ is a Sigmoid function; $f ( x )$ is a mapping func-( ) ( )tion [48]. It is a fact that we cannot always obtain the optimal results. Therefore, the historical imitation data is used to implement the prediction of the optimal states of UAVs. We can adjust the weights of features based on the $A _ { i } ^ { * }$ . With the updated features, the current state of UAVs are updated as

$$
{ \dot { S } } _ { i } = f ( S _ { i } , A _ { i } ) + v _ { i } ,\tag{25}
$$

where $v _ { i }$ is a random noise. An estimation $\lambda _ { i }$ is given by

$$
\lambda _ { i } = \frac { P ( \dot { S } _ { i } | i ) } { \sum _ { j } ^ { M } P ( \dot { S } _ { j } | j ) } ,\tag{26}
$$

where $P ( \dot { S } _ { i } | i )$ is a likelihood probability under the $\dot { S } _ { i }$

( )We can aggregate $A _ { i } ^ { * }$ and $\lambda _ { i }$ for the optimal DT inspection result. It can control UAVs to avoid potential physical collisions and can optimize the behaviors of UAVs to perform accurate target sensing and imitation. The inspection results are transmitted to the local UAVs for high imitation accuracy. The iteration numbers between the UAVs and the edge server are also reduced for the real-time imitation. The DT inspection is implemented by Algorithm 3.

```powershell
Algorithm 3: DT Inspection
Input: Ground truth Ï; Observation information $S _ { i } ^ { e . } ; $
DDPG network parameters $\theta ^ { Q } , \theta ^ { \mu } ;$ Sigmoid
function D; Mapping function $f ( x )$
Output: The optimal inspection decision.
1 Construct DT model DTi $( h _ { i } , { \bf H } _ { i } , { \bf h } _ { i , k } )$ for each round
do
2 for eachUAVi do
3 for each time slot t do
4 if edge server is reachable then
5 Construct the learning function in the
edge side using Eq. (22)
6 Train the multimodal network with
representative features by Eq. (23)
7 if edge server is unavailable then
8 Construct the learning function using
Eq. (22)
9 Train the multimodal network with
representative features using Eq. (23)
10 Exchange network parameters among
group leaders
11 foreachUAVido
12 Update state information using Eq. (25)
13 Obtain estimation results using Eq. (26)
14 Aggregate the acquired parameters
15 Transmit the result to local UAVs
```

## D. Algorithm Complexity Analysis

The computational complexity is analyzed in three parts. Firstly, the complexity of the actor-network is focused on the matrix inversion operation with $O ( k ( \theta ) )$ , where k Î¸ is a func-( ( )) ( )tion whose input Î¸ is the number of hidden layers. Therefore, the time complexity for cooperative sensing is $O ( K \cdot | E | \cdot k ( \theta ) )$ Then, the time complexity of model aggregation is $n \cdot d ^ { 2 }$ ( )), where n is the dimension of the parameter vector; d is the number of parameters for different UAVs. Finally, the complexity of inspection operation is $\{ O ( K \cdot | E | \cdot k ( \theta ) ) , n ( \psi _ { \mathrm { m i n } } ) k ( \psi _ { \mathrm { m i n } } ) \}$ , where $n ( \psi _ { \mathrm { m i n } } ) k ( \psi _ { \mathrm { m i n } } )$ is the complexity of prediction net-(work with $n ( \psi _ { \mathrm { m i n } } )$ )neurons and $k ( \psi _ { \mathrm { m i n } } )$ iterations. Therefore, the system time complexity is $\{ O ( K \cdot | E | \cdot k ( \theta ) \cdot n$ $d ^ { 2 } )$ ,max $\{ O ( K \cdot | E | \cdot k ( \theta ) ) , n ( \psi _ { \mathrm { m i n } } ) k ( \bar { \psi _ { \mathrm { m i n } } } ) \} \}$ ( ). The complex-) max ( ( )) ( ) ( )ity is lower than traditional deep reinforcement learning by decoupling the functions of the DT framework with the federated imitation.

## VI. PERFORMANCE EVALUATION

In this section, we present the implementation of our federated DT framework and evaluate its performance.

## A. System Evaluation Metrics

UAVs can collect the target information cooperatively. The local models are aggregated in a computing-intensive UAV as an edge server that performs a macro DT imitation. As shown in Fig. 6, we use the Gazebo, a stand-alone simulation application [49], to imitate the tracking scenario. The states of UAVs, including velocity, position, and posture, are limited in reasonable ranges. The UAV paths are planned based on a Robot Operation System (ROS) [50] shown in Fig. 7. In addition, the sensing performance of the data collection comprehension is obtained during the tracking process based on Network Simulation (NS-3) software. The main simulation parameters are summarized in Table I. We use four metrics to evaluate the performance of our proposed federated DT:

<!-- image-->  
Fig. 6. Snapshot of tracking imitation in Gazebo.

<!-- image-->  
Fig. 7. Implementation Procedure in Gazebo with ROS.

TABLE I  
SIMULATION PARAMETERS
<table><tr><td>Parameterdescription</td><td>Value</td></tr><tr><td>Number of mobile targets</td><td>[30,80]</td></tr><tr><td>Average moving velocity of the UAVs</td><td>36 km/h</td></tr><tr><td>Average moving velocity of the targets</td><td>[12 km/h, 90 km/h]</td></tr><tr><td>Pitch angle of the UAVs</td><td> $[ - 1 3 0 ^ { \circ } , + 4 0 ^ { \circ } ]$ </td></tr><tr><td>Angular-rate of horizontal rotation</td><td> $[ - 1 0 0 ^ { \circ } , + 1 0 0 ^ { \circ } \ ]$ </td></tr><tr><td>Learning rate</td><td>[0.001,0.009]</td></tr><tr><td>Minimal safe flight distance of the UAVs</td><td>3m</td></tr><tr><td>Average sensing rate of the UAVs</td><td>10 MByte/s</td></tr><tr><td>Horizontal sensing distance of the UAVs</td><td>[0 m,30 m]</td></tr><tr><td>Gaussian White Noise</td><td>-96dBm/Hz</td></tr><tr><td>The acceptable maximal system latency</td><td>2 seconds</td></tr></table>

1) System latency overhead: This metric reflects the DT system latency.

2) Successful tracking ratio: It reflects the imitation accuracy by recording the number of sensed mobile targets. It can be also used to estimate the target sensing performance of the cooperative sensing algorithm. The ratio Î· is formulated with $P _ { k }$ under (1):

$$
\eta = \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \frac { \sum _ { i = 1 } ^ { M } \sum _ { k = 1 } ^ { K } P _ { k } } { M K } .\tag{27}
$$

<!-- image-->  
Fig. 8. Obtained reward with different numbers of targets.

3) Collision frequency among UAVs: We use the metric to evaluate the imitation robustness by analyzing the collision frequency.

4) System energy consumption: The metric can reflect the performance of our DT inspection algorithm which assists UAVs in planning optimal tracking paths.

We use four typical benchmarks for comparison:

1) Centralized DT imitation method [51]: It leverages a deep reinforcement learning method running on the edge server to implement a centralized imitation based on environmental information.

2) Distributed DT imitation method: UAVs exchange their local DT models with neighbors for imitation consensus under a multi-agent learning architecture [52].

3) Matched Deep Q-network (DQN) [53]: It leverages a deep learning framework where agents interact with the physical scenario without the support of DT.

4) Evolution theory-based target tracking [54]: It provides an adaptive differential evolution by continued iterations to acquire positions of targets for accurate tracking.

## B. Evaluation for Cooperative Sensing

Fig. 8 provides the training performance for cooperative sensing algorithm based on DDPG architecture. We find that all the rewards can obtain convergences with the different numbers of targets under 20 UAVs. In other word, our cooperative sensing algorithm has the ability to acquire comprehensive target data. Based on this, Fig. 9 gives the transient state of cooperative sensing performance under 20 deployed UAVs to evaluate the cooperative sensing performance. The green circle represents UAVs marked as âUâ, and the red triangle denotes mobile targets marked as âTâ implemented in NS-3. Meanwhile, the targets that are not sensed are encircled using black circles. Based on the sensing parameter requirement in Table I, we find that our federated DT can realize full-scale sensing during the tracking process shown in Fig. 9(a). We can ensure a highly accurate sensing performance with 20 UAVs tracking 30 targets.

Fig. 9(b) depicts the cooperative sensing performance under 50 targets with an average speed of 56 km/h. UAVs track the targets with an average speed of 32 km/h. We draw that our solution sense more than 90% of targets successfully. It implies that our method is efficient for accurate DT imitation. UAVs seem to overlap with targets in the 2-dimension simulation figure with the same horizontal and vertical coordinates but different height values. When the number of targets increases to 70, our method can still realize a robust sensing performance. As shown in Fig. 9(c), except for a few targets such as T47 and T2 cannot be sensed, our federated DT can realize up to 87.5% of targets to ensure a comprehensive data collection operation.

## C. Evaluation for Real-Time Performance of DT

We estimate the real-time of our federated DT under multidimensional imitations based on different numbers of targets and UAVs with different velocity values. Fig. 10(a) gives the comparison by imitating different numbers of targets under 20 UAVs with an average velocity value of 32 km/h. We find that all the latency overheads increase with the increase in the number of targets. However, our federated DT algorithm always meets the imitation requirement with the given maximal latency of 1.5 s. The distributed imitation algorithm performs worse than the centralized algorithm. It is because UAVs exchange information in the virtual space frequently which causes a high latency overhead. The performance of the matched-DQN algorithm is satisfied when the number of targets is less than 40. When the number of targets increases, the latency overhead increases significantly due to frequent interactions with the physical environment. Our federated DT system can enable UAVs to exchange lightweight DT model parameters for low-latency sensing cooperation and tracking imitation. It can reduce the imitation pressures of edge servers from the centralized imitation method. On the other hand, it can also reduce the frequency of information exchange for real-time mobile imitation. Quantitatively, our algorithm can reduce 25.0% imitation latency compared to the best benchmark.

Fig. 10(b) depicts the comparison of the real-time metric in imitating 50 targets with different moving velocity values and the same number of UAVs as Fig. 10(a). We draw the conclusion that the imitation latency overhead still keeps under the given 2 s using our federated DT scheme. The centralized imitation manner performs well when the average velocity of targets is less than 48 km/h. It is because the high-moving targets incur huge pressure on the centralized manner. Similarly, the frequent information exchange that occurs in the distributed manner performs a high-latency system performance. The performance of the matched DQN algorithm is worse than that of the distributed imitation manner. It is because the high dynamic of the targets causes huge computing pressure on the matched DQN algorithm implemented in resource-restrained edge servers. Furthermore, the algorithm may cause physical collisions among UAVs with unreasonable tracking decisions. The case can further increase computing latency for feasible tracking decisions. The evolution-based algorithm also causes a high-latency system response with frequent iterations. Our federated DT solution enables edge servers to perform rapid model aggregation for high-speed moving targets. Besides, our solution can further reduce imitation latency with the aid of the trajectory prediction method. In this case, our algorithm reduces the imitation latency overhead of 28.6% compared to the best benchmark approximately.

<!-- image-->  
(a) 30 mobile targets.

<!-- image-->  
(b) 50 mobile targets.

<!-- image-->  
(cï¼ 70 mobile targets.

Fig. 9. Transient state of cooperative sensing performance under 20 UAVs.  
<!-- image-->

<!-- image-->

<!-- image-->  
(a)Latencyoverheadvs.numbersof targets.(b)Latencyoverheadvs.velociesoftargets.(c)Latency overheadvs.numbersofUAVs.

Fig. 10. Real time of imitation reflected by latency overhead under different metrics.  
<!-- image-->  
(a) Latency overhead vs.velocities of UAVs.

<!-- image-->  
(b) Tracking ratio vs. numbers of targets.

<!-- image-->  
(c) Tracking ratio vs. velocities of targets.  
Fig. 11. Real time of imitation reflected by latency overhead under different velocities of UAVs. Imitation accuracy reflected by successful tracking ratio under different velocities and numbers of targets.

In addition, Fig. 10(c) gives the comparison based on different numbers of UAVs with different velocity values. With 30 targets, we discover that the increased slope of our latency overhead is the lowest than other benchmarks. In our federated DT, the latency is mainly consumed in the stage of the model aggregation with additional UAVs. The mild increase in slope demonstrates that the model aggregation algorithm can meet the real-time imitation requirement. It reduces 68.0% imitation latency compared to the centralized manner. Quantitatively, the imitation latency will tend to be stable when the number of UAVs is more than 31 with a constant number of mobile targets. The tendency also demonstrates that our algorithm is robust in the highly-dynamic mobile tracking scenario.

Fig. 11(a) tells us that the imitation latency overhead is significantly reduced when we change the velocity values of UAVs. Given the same numbers of targets as that in Fig. 10(c) with an average speed of 56 km/h and 20 UAVs, we find that our federated DT alleviates the imitation latency overhead compared to other benchmarks. It is because ours can implement an efficient imitation to explore optimal flight paths, with which UAVs can perform low-latency tracking. It saves more time to imitate what the targets will do next. In this case, our algorithm decreases the imitation latency overhead of 68.4% compared to the centralized manner. Quantitatively, when we set the sensing frequency of sensor $b , b _ { i } \in [ 4 \mathrm { M B } / \mathrm { s } , 5 \mathrm { M B } / \mathrm { s } ]$ [ ]and the number of sensors A  , UAVs perform the low-= 8est latency overhead of 600 ms with an average speed of 72 km/h.

<!-- image-->  
(a) Collision frequency imitation vs. iterations.

<!-- image-->

<!-- image-->  
(c) Energy consum.in comm.vs.number of targets  
Fig. 12. Imitation inspection for collision-avoidance, system energy consumption optimization and energy consumption in communications.

## D. Evaluation for DT Accuracy

We evaluate the DT accuracy based on the successful tracking ratio metric given by (27) under different numbers of targets with different velocity values. Fig. 11(b) provides a comparison under different numbers of targets with an average speed of 56 km/h. In the case of 25 UAVs with an average of 32 km/h moving speed, our federated DT achieves a successful tracking ratio of up to 90% even the number of targets increases to 50. For the centralized scheme, our solution reduces the pressure of imitation on the center side by aggregating received model parameters. Our framework also achieves a higher imitation accuracy with a high successful tracking ratio compared to the distributed scheme. It is because the frequent information exchange in distributed imitation is eliminated in our framework. Our solution improves 10.4% and 22.4% successful tracking ratios contrasting to the centralized and distributed schemes, respectively.

Furthermore, Fig. 11(c) gives the comparison in the imitation accuracy with different velocity values of the targets. The number of UAVs is 20, with an average speed of 32 km/h; the number of targets is 40. We draw that the successful tracking ratios of all the algorithms reduce with the increase of velocities of targets. However, ours maintains the highest successful tracking ratio with up to 95.0%. It implies that our framework realizes a highly robust imitation in dynamic scenarios. Our frameworkâs advantages are obvious considering two aspects: 1) The imitation accuracy can be improved by selecting feasible DT model parameters on the edge server. 2) We provide an efficient DT inspection solution to dynamically correct imitation results. It also provides the imitation experience for local UAVs. The results can conduct UAVs to perform accurate tracking with a highly successful tracking ratio. Our federate DT improves

13.0% and 14.3% successful tracking ratios compared to the centralized manner and the distributed scheme, respectively.

## E. Evaluation for DT Inspection

The DT inspection is mainly divided into three parts: 1) Collision avoidance. 2) Tracking path optimization. 3) Energy consumption in communication.

Our federated DT can conduct cooperative tracking imitation based on aggregated DT models. The edge UAV inspects the mobile positions of UAVs to predict the potential collisions among UAVs during the tracking process. Fig. 12(a) gives the inspection performance for collision avoidance. We draw that our federated DT can imitate to predict the potential collisions among UAVs. Based on the cross-layered cooperation manner, UAVs can efficiently avoid physical collisions when reaching 80 iterations. The centralized manner can not eliminate the collision risk due to the obvious time-consuming imitation manner. The Matched DQN algorithm can implement the collision inspection operation that UAVs sense the state of neighbors frequently. In this case, the time of collision avoidance is significantly unacceptable.

The federated DT can also inspect the moving paths of UAVs to explore the optimal cooperative tracking solution with acceptable energy consumption. Fig. 12(b) depicts the comparison of system energy consumption under the different benchmarks. With the same parameters as that of Fig. 11(b), we see that energy consumption increases with the increase in the number of targets. However, our federated DT realizes the lowest increase slope compared to other benchmarks. It is because the model aggregation method assists UAVs in dynamically associating feasible targets with the energy budget constraint. Compared to the distributed imitation scheme, the centralized DT gives a better UAV allocation solution thanks to a global view. Our federated DT reduces 28.3% and 50.0% energy consumption compared to the centralized and distributed scheme, respectively.

Fig. 12(c) shows the comparison of energy consumption in communication. The energy consumption in communications using our solution is the lowest compared to the benchmarks. It implies that our federated DT framework can efficiently reduce data transmission frequency with lightweight DT parameters.

<!-- image-->  
(a)Imitation of UAV postures under no winds

<!-- image-->  
(b) Posture imitation at a wind speed of 15m/s and 25m/s.

<!-- image-->  
(c) Inspection and correction of UAV postures.  
Fig. 13. Imitation of UAV postures at the different wind speeds and posture correction.

The centralized framework incurs more energy consumption in communication by transmitting a mass of data among edge servers and UAVs. On the other hand, the distributed framework gets into the worst condition with the highest energy consumption in communication. It is because UAVs need frequently exchange data with neighbors for accurate imitation decisions. Our solution can reduce 33.3% and 77.8% energy consumption in communications compared to the centralized and distributed frameworks, respectively.

We also evaluate the interference of wind speeds which has the main impact on UAV tracking performance [6]. We use the Gazebo to record the UAV postures in the condition of no wind. As shown in Fig. 13(a), UAVs can adjust roll angles to cooperative sense target information for comprehensive data collection and accurate imitation with a flight speed of 5 m/s. When targets move toward a fixed direction, the yaw and pitch angles of UAVs are approximately constant. The UAV postures are shown in Fig. 13(b) under 15 m/s and 25 m/s wind speeds respectively. We find that the wind can cause UAVs to deflect significantly to influence the data collection performance. In this case, our federated DT can efficiently inspect the status of UAVs and correct their postures for comprehensive sensing and accurate imitation. Fig. 13(c) shows that our algorithm can rapidly correct the postures of UAVs in a unit of time.

To test our solution in a real scenario, we provide a test case to evaluate the proposed federated DT solution where two DJI UAVs managed by an edge UAV track a target. As shown in Fig. 14, UAVs can implement a cooperative DT imitation operation with the Manifold 2 computer, a powerful onboard computer with NVIDIA Jetson TX2 GPU model [55]. We implement our federated DT through code portability from the Gazebo system to the Manifold computer [56]. Before that, we use DJI APP to plan target trajectories randomly shown in Fig. 15. The target moves with an average speed of 3.4 m/s. UAVs use onboard sensors to collect environment information shown in Fig. 16. The UWB and ultrasonic sensors are used to acquire physical distances between UAVs and targets and the velocities of targets. The camera captures images of targets. The gyroscope sensor enables to acquire postures of UAVs.

We use socket communication technology to implement the information transmission with IP address and port number where all the UAVs can communicate in a Local Area Network (LAN).

<!-- image-->  
Fig. 14. Implementation of tracking imitation.

<!-- image-->  
Fig. 15. Target trajectory planning.

<!-- image-->  
Fig. 16. UAV with sensors.

It is bound to a port number so that the Transmission Control Protocol (TCP) layer can identify the application to which data is destined to be sent. With an average 10 MByte/s of sensing rate and 5 m/s moving speed, UAVs can adjust sensing directions to collect target information cooperatively for tracking imitation. The system energy consumption is compared based on the same physical scenario with 2 m/s of natural wind speed and the same target trajectory. We can calculate the energy consumption metric through changes in voltage charges of UAVs with TB60 batteries [57]:

$$
0 . 4 \mathrm { V } \times 5 9 3 5 \mathrm { m H A } \times 3 . 6 = 8 . 5 4 6 4 \mathrm { k J } .\tag{28}
$$

Compared to the centralized and distributed imitation manner, our federated DT solution can save 0.03 V voltages (472.21 J) and 0.05 V voltage (640.98 J), respectively. Sensing and communication ranges are circular areas with 30 m radii, respectively. With the same system parameters, the system latency is defined as the time from the time the target escapes from the sensing ranges of UAVs to the time UAVs sense the target again. In this context, our system latency overhead is about 1.2 s using the time stamping method while the centralized and distributed DT are approximately 2 s and 2.5 s, respectively. Our federated DT solution can effectively reduce the DT imitation latency with the lightweight data exchange manner.

## F. Performance Discussion

We consider a specific application area of hit-and-run pursuit where the UAV swarm performs our proposed federated Digital Twin (DT) imitation for cooperative target tracking on the plain terrain. The system performance is affected by the changes of environment changes, including weather influence (temperature and humidity, illumination intensity, and wind speed), as well as the number, density and velocity of UAVs and targets, etc. We implement offline training to acquire several typical network models based on different environments. To improve the diversity of network models, we invoke a Generative Adversarial Network (GAN) algorithm to generate new data through a generator network based on the information of different environments [58]. The GAN algorithm can then evaluate the generative data through a discriminative network to output high-quality training samples. The samples are imported into the training database to enrich the diversity of network models based on offline learning. The diverse models can assist UAVs in optimizing their tracking paths, velocities, and postures for different environments. When edge servers are available, we can enable the computing-intensive edge servers to assist UAVs in implementing online training with DT derivations. It can provide highly accurate optimization decisions to cope with unprecedented environmental patterns. In this work, we specifically analyze three important system metrics to evaluate the impacts of the number and the density for mobile targets, including imitation response time, system imitation capability, and imitation error ratio.

As a significant system metric, the imitation response time, including sensing time, imitation latency, data transmission latency, and DT inspection time, can reflect the imitation efficiency. In Fig. 10(a) and (b), we find that the response time of our solution is always less than 1.5 s for all the cases with different numbers and densities of targets. The response time is still acceptable when the number of targets is more than that of UAVs. In other words, our framework can rapidly output imitation decisions even in overloaded conditions.

The system imitation capability can closely reflect the cooperative imitation performance. It can analyze the cooperative effectiveness when the number of targets is overloaded. In this context, we mainly focus on the software process capability based on the cross-layered cooperation between the UAVs and the edge server. Based on the simulation results, our federated DT can imitate 20 UAVs cooperatively tracking 75 targets at most with a deployment density of 8.3 targets per km2 under response latency of 2 s. This implies that our federated DT can perform an overloaded imitation.

The imitation error ratio can be estimated by the timeout ratio. The timeout ratio reflects the imitation effectiveness that is equivalent to the successful tracking ratio metric. In Fig. 11(b), the highly successful tracking performance with over 90% can be still obtained when the number of targets is more than twice as many as that of UAVs. When the number of targets is twice as many as that of UAVs from Fig. 11(c), we observe that UAVs with an average speed of 32 km/h can still track targets with an average speed of 72 km/h with up to 95% successful tracking ratio. It implies that the imitation error is low.

## VII. CONCLUSION

We have designed a flexible federated DT framework to ensure real-time and accurate imitation with high reliability in mobile tracking scenarios. To acquire comprehensive information on mobile targets, we present a cooperative sensing algorithm to reduce data redundancy while accelerating the data collection process. Then, we propose a model aggregation algorithm in the federated DT framework to ensure an accurate mobile imitation. Based on this, we give multiple representative metrics to estimate our solution. The results demonstrate that our federated DT can realize a real-time tracking imitation. The mobile imitation decisions also ensure a highly successful tracking ratio. This work provides a foundation for the application of DT imitation in general mobile scenarios. There still exist several technical challenges. In the future, we will explore a more universal DT solution to serve different types of mobile scenarios.

## REFERENCES

[1] D. C. Nguyen et al., â6G Internet of Things: A comprehensive survey,â IEEE Internet Things J., vol. 9, no. 1, pp. 359â383, Jan. 2022.

[2] X. Chen, S. Leng, J. He, and L. Zhou, âDeep-learning-based intelligent intervehicle distance control for 6G-enabled cooperative autonomous driving,â IEEE Internet Things J., vol. 8, no. 20, pp. 15180â15190, Oct. 2021.

[3] K. Zhang, Y. Zhu, S. Maharjan, and Y. Zhang, âEdge intelligence and blockchain empowered 5G beyond for the industrial Internet of Things,â IEEE Netw., vol. 33, no. 5, pp. 12â19, Sep./Oct. 2019.

[4] M. Liwang, Z. Gao, and X. Wang, âLetâs trade in the future! A futuresenabled fast resource trading mechanism in edge computing-assisted UAV networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3252â3270, Nov. 2021.

[5] T. Li, S. Leng, Z. Wang, K. Zhang, and L. Zhou, âIntelligent resource allocation schemes for UAV-swarm-based cooperative sensing,â IEEE Internet Things J., vol. 9, no. 21, pp. 21570â21582, Nov. 2022.

[6] A. Dhulipalla, N. Han, H. Hu, and H. Hu, âA comparative study to characterize the effects of adverse weathers on the flight performance of an unmanned-aerial-system,â in Proc. AIAA AVIATION Forum, 2022, Art. no. 3962.

[7] F. Y. P. Feng, M. Rihan, and L. Huang, âPositional perturbations analysis for micro-UAV array with relative position-based formation,â IEEE Commun. Lett., vol. 25, no. 9, pp. 2918â2922, Sep. 2021.

[8] F. Tao et al., âDigital twin-driven product design framework,â Int. J. Prod. Res., vol. 57, no. 12, pp. 3935â3953, 2019.

[9] K. Xiong, Z. Wang, S. Leng, and J. He, âA digital-twin-empowered lightweight model-sharing scheme for multirobot systems,â IEEE Internet Things J., vol. 10, no. 19, pp. 17231â17242, Oct. 2023.

[10] R. P. MÃ©xas, F. R. Leta, and E. W. G. Clua, âComparison of reinforcement and imitation learning algorithms in autonomous sailboat digital twins,â IEEE Latin Amer. Trans., vol. 20, no. 9, pp. 2153â2161, Sep. 2022.

[11] L. U. Khan, W. Saad, D. Niyato, Z. Han, and C. S. Hong, âDigital-twinenabled 6G: Vision, architectural trends, and future directions,â IEEE Commun Mag., vol. 60, no. 1, pp. 74â80, Jan. 2022.

[12] L. Zhu, S. Zhang, X. Wang, S. Chen, H. Zhao, and D. Wei, âMultilevel recognition of UAV-to-ground targets based on micro-doppler signatures and transfer learning of deep convolutional neural networks,â IEEE Trans. Instrum. Meas., vol. 70, pp. 1â11, 2021.

[13] C. Wang, Z. Cai, and Y. Li, âSustainable blockchain-based digital twin management architecture for IoT devices,â IEEE Internet Things J., vol. 10, no. 8, pp. 6535â6548, Apr. 2023.

[14] P. Bellavista, C. Giannelli, M. Mamei, M. Mendula, and M. Picone, âApplication-driven network-aware digital twin management in industrial edge environments,â IEEE Trans. Ind. Informat., vol. 17, no. 11, pp. 7791â7801, Nov. 2021.

[15] X. He et al., âFederated continuous learning based on stacked broad learning system assisted by digital twin networks: An incremental learning approach for intrusion detection in UAV networks,â IEEE Internet Things J., vol. 10, no. 22, pp. 19825â19838, Nov. 2023.

[16] W. Sun, P. Wang, N. Xu, G. Wang, and Y. Zhang, âDynamic digital twin and distributed incentives for resource allocation in aerial-assisted internet of vehicles,â IEEE Internet Things J., vol. 9, no. 8, pp. 5839â5852, Apr. 2022.

[17] W. Liu, B. Li, W. Xie, Y. Dai, and Z. Fei, âEnergy efficient computation offloading in aerial edge networks with multi-agent cooperation,â IEEE Trans. Wireless Commun., vol. 22, no. 9, pp. 5725â5739, Sep. 2023.

[18] T. Liu, L. Tang, W. Wang, Q. Chen, and X. Zeng, âDigital-twin-assisted task offloading based on edge collaboration in the digital twin edge network,â IEEE Internet Things J., vol. 9, no. 2, pp. 1427â1444, Jan. 2022.

[19] D. Liu, Y. Du, W. Chai, C. Lu, and M. Cong, âDigital twin and data-driven quality prediction of complex die-casting manufacturing,â IEEE Trans. Ind. Informat., vol. 18, no. 11, pp. 8119â8128, Nov. 2022.

[20] X. Zhou et al., âIntelligent small object detection for digital twin in smart manufacturing with industrial cyber-physical systems,â IEEE Trans. Ind. Informat., vol. 18, no. 2, pp. 1377â1386, Feb. 2022.

[21] E. G. Kaigom and J. RoÃmann, âValue-driven robotic digital twins in cyberâphysical applications,â IEEE Trans. Ind. Informat., vol. 17, no. 5, pp. 3609â3619, May 2021.

[22] Y. Mo, S. Ma, H. Gong, Z. Chen, J. Zhang, and D. Tao, âTerra: A smart and sensible digital twin framework for robust robot deployment in challenging environments,â IEEE Internet Things J., vol. 8, no. 18, pp. 14039â14050, Sep. 2021.

[23] L. Lei, G. Shen, L. Zhang, and Z. Li, âToward intelligent cooperation of UAV swarms: When machine learning meets digital twin,â IEEE Netw., vol. 35, no. 1, pp. 386â392, Jan./Feb. 2021.

[24] G. Shen et al., âDeep reinforcement learning for flocking motion of multi-UAV systems: Learn from a digital twin,â IEEE Internet Things J., vol. 9, no. 13, pp. 11141â11153, Jul. 2022.

[25] Y. M. Chen and S. H. Chang, âAn agent-based simulation for multi-UAVs coordinative sensing,â Int. J. Intell. Comput. Cybern., vol. 1, no. 2, pp. 269â284, 2008.

[26] T. J. Ma, âRemote sensing detection enhancement,â J. Big Data, vol. 8, no. 1, pp. 1â13, 2021.

[27] A. Arsalan Soltani, H. Huang, J. Wu, T. D. Kulkarni, and J. B. Tenenbaum, âSynthesizing 3D shapes via modeling multi-view depth maps and silhouettes with deep generative networks,â in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2017, pp. 1511â1519.

[28] C.-A. Cai, K.-Y. Kai, and W.-J. Liao, âA WLAN/WiFi-6E MIMO antenna design for handset devices,â in Proc. Int. Symp. Antennas Propag., 2021, pp. 1â2.

[29] G. Oliva, R. Setola, and C. N. Hadjicostis, âDistributed k-means algorithm,â 2013, arXiv:1312.4176.

[30] N. Kern, B. Schiele, and A. Schmidt, âMulti-sensor activity context detection for wearable computing,â in Proc. 1st Eur. Symp. Ambient Intell., 2003, pp. 220â232.

[31] J. A. Santoyo-RamÃ³n, E. Casilari, and J. M. Cano-GarcÃ­a, âA study of the influence of the sensor sampling frequency on the performance of wearable fall detectors,â Measurement, vol. 193, 2022, Art. no. 110945.

[32] K. Meng, Q. Wu, S. Ma, W. Chen, K. Wang, and J. Li, âThroughput maximization for UAV-enabled integrated periodic sensing and communication,â IEEE Trans. Wireless Commun., vol. 22, no. 1, pp. 671â687, Jan. 2023.

[33] A. Alkhateeb, S. Jiang, and G. Charan, âReal-time digital twins: Vision and research directions for 6G and beyond,â IEEE Commun. Mag., Aug. 2023.

[34] Y. Wang, M. Long, J. Wang, Z. Gao, and P. S. Yu, âPredRNN: Recurrent neural networks for predictive learning using spatiotemporal LSTMs,â in Proc. 31st Int. Conf. Neural Inf. Process. Syst., 2017, pp. 879â888.

[35] Y. Mao, C. You, J. Zhang, K. Huang, and K. B. Letaief, âA survey on mobile edge computing: The communication perspective,â IEEE Commun. Surv. Tuts., vol. 19, no. 4, pp. 2322â2358, Fourthquarter 2017.

[36] J. M. Kim, Y. G. Kim, and S. W. Chung, âStabilizing CPU frequency and voltage for temperature-aware DVFS in mobile devices,â IEEE Trans. Comput., vol. 64, no. 1, pp. 286â292, Jan. 2015.

[37] V. Matrosov, âOn the stability of motion,â J. Appl. Math. Mech., vol. 26, no. 5, pp. 1337â1353, 1962. [Online]. Available: https://www. sciencedirect.com/science/article/pii/0021892862900102

[38] Y. Hu, M. Chen, W. Saad, H. V. Poor, and S. Cui, âDistributed multi-agent meta learning for trajectory design in wireless drone networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3177â3192, Oct. 2021.

[39] X. Liu, S. Wang, M. Chen, C. Yin, S. Cui, and H. V. Poor, âMinimization of age of information for monitoring realistic physical processes in unmanned aerial vehicle networks,â in Proc. IEEE 22nd Int. Workshop Signal Process. Adv. Wireless Commun., 2021, pp. 261â265.

[40] Z. Qin, H. Yao, and T. Mai, âTraffic optimization in satellites communications: A multi-agent reinforcement learning approach,â in Proc. Int. Wireless Commun. Mobile Comput., 2020, pp. 269â273.

[41] J. Filar and K. Vrieze, Competitive Markov Decision Processes. Berlin, Germany: Springer, 2012.

[42] P. Zyblewski and M. WoÂ´zniak, âNovel clustering-based pruning algorithms,â Pattern Anal. Appl., vol. 23, no. 3, pp. 1049â1058, 2020.

[43] S. Scardapane, I. Spinelli, and P. D. Lorenzo, âDistributed training of graph convolutional networks,â IEEE Trans. Signal Inf. Process. Netw., vol. 7, pp. 87â100, 2021.

[44] E. League, âKey-value pairs explained,â 2021. [Online]. Available: https://experienceleague.adobe.com/docs/audience-manager/userguide/reference/key-value-pairs-explained.html?lang=en

[45] X. Zhang, Y. Yang, Z. Li, X. Ning, Y. Qin, and W. Cai, âAn improved encoder-decoder network based on strip pool method applied to segmentation of farmland vacancy field,â Entropy, vol. 23, no. 4, 2021, Art. no. 435.

[46] S. Mihai et al., âDigital twins: A survey on enabling technologies, challenges, trends and future prospects,â IEEE Commun. Surv. Tuts., vol. 24, no. 4, pp. 2255â2291, Fourthquarter 2022.

[47] C. Rieger, R. Boring, B. Johnson, and T. McJunkin, Resilient Control Architectures and Power Systems. Hoboken, NJ, USA: Wiley, 2022.

[48] B. Liu, âRobust sequential online prediction with dynamic ensemble of multiple models: A review,â Neurocomputing, Jul. 2023, Art. no. 126553.

[49] N. Koenig and A. Howard, âDesign and use paradigms for Gazebo, an open-source multi-robot simulator,â in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., 2004, pp. 2149â2154.

[50] S. Macenski et al., âRobot operating system 2: Design, architecture, and uses in the wild,â Sci. Robot., vol. 7, 2022, Art. no. eabm6074.

[51] Y. Lu, S. Maharjan, and Y. Zhang, âAdaptive edge association for wireless digital twin networks in 6G,â IEEE Internet Things J., vol. 8, no. 22, pp. 16219â16230, Nov. 2021.

[52] W. Chen et al., âMADDPG algorithm for coordinated welding of multiple robots,â in Proc. IEEE 6th Int. Conf. Autom. Control Robot. Eng., 2021, pp. 1â5.

[53] Y. S. Nasir and D. Guo, âMulti-agent deep reinforcement learning for dynamic power allocation in wireless networks,â IEEE J. Sel. Areas Commun., vol. 37, no. 10, pp. 2239â2250, Oct. 2019.

[54] Y. Yu et al., âDistributed multi-agent target tracking: A nash-combined adaptive differential evolution method for UAV systems,â IEEE Trans. Veh. Technol., vol. 70, no. 8, pp. 8122â8133, Aug. 2021.

[55] X. Hui, J. Bian, Y. Yu, X. Zhao, and M. Tan, âA novel autonomous navigation approach for UAV power line inspection,â in Proc. IEEE Int. Conf. Robot. Biomimetics, 2017, pp. 634â639.

[56] A. Staranowicz and G. L. Mariottini, âA survey and comparison of commercial and open-source robotic simulator software,â in Proc. 4th Int. Conf. PErvasive Technol. Related Assistive Environ., 2011, pp. 1â8.

[57] T. Kersten, J. Wolf, and M. Lindstaedt, âInvestigations into the accuracy of the UAV system DJI matrice 300 RTK with the sensors Zenmuse p1 and l1 in the Hamburg test field,â in XXIV ISPRS Congress âImaging Today, Foreseeing Tomorrowâ. Nice, France:Copernicus, 2022, pp. 339â346.

[58] E. Brophy, Z. Wang, Q. She, and T. Ward, âGenerative adversarial networks in time series: A systematic literature review,â ACM Comput. Surv., vol. 55, no. 10, pp. 1â31, 2023.

<!-- image-->

Longyu Zhou (Student Member, IEEE) is currently working toward the PhD degree with the School of Information and Communication Engineering, University of Electronic Science and Technology of China (UESTC). He is also a visiting student with Embedded Systems (ES) Group, Delft University of Technology, The Netherlands. His research interests include Internet of Things, edge intelligence, resource scheduling, and wireless sensor networks. He was the recipient of the best paper award in 20th IEEE Conference on Communications and Technology. He is/was

a PC member of the IEEE Global Communications Conference (Globecom) and the IEEE International Conference on Communications (ICC). He is also a reviewer of IEEE Transactions on Vehicular Technology and IEEE Internet of Things Journal.

<!-- image-->

Supeng Leng (Member, IEEE) received the PhD degree from Nanyang Technological University (NTU), Singapore. He is currently a full professor and the vice dean with the School of Information and Communication Engineering, University of Electronic Science and Technology of China (UESTC). He is also the Director of the Sichuan International Joint Research Center for Ubiquitous Wireless Networks. His research interests include spectrum, energy, routing and networking in the Internet of Things, vehicular networks, broadband wireless access networks, and

the next generation intelligent mobile networks. He published over 200 research papers and 4 books/book chapters in recent years. He got the Best Paper Awards at 4 IEEE international conferences. He serves as an organizing committee chair and a TPC member for many international conferences. He is the editorial member of 4 international journals and a reviewer for over 20 well-known academic international journals.

<!-- image-->

Qing Wang (Senior Member, IEEE) received the PhD degree from UC3M and IMDEA Networks Institute, Spain, in 2016. He is currently an assistant professor of the Embedded and Networked Systems Group, Delft University of Technology, The Netherlands. He is the co-founder of OpenVLC, an open-source and low-cost platform for VLC research. His research interests include visible light communication and sensing systems, and the Internet of Things. His research outcomes on active/passive visible light communication and sensing systems have been published

at IEEE/ACM conferences and journals such as ACM MobiCom, CoNEXT, SenSys, IEEE INFOCOM, IEEE/ACM Transactions on Networking, and IEEE Journal on Selected Areas in Communications. He has received several paper awards, including the Best Paper Awards from ICCâ23, EWSNâ23, SenSysâ22, Morseâ22, COMSNETSâ19, and Best Paper Runner-Ups from EWSNâ22, MobiComâ20 (Honourable Mention), and CoNEXTâ16.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_7_img_1.jpeg|page_7_img_1]]
3. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_8_img_1.jpeg|page_8_img_1]]
4. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_10_img_1.jpeg|page_10_img_1]]
5. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_10_img_2.jpeg|page_10_img_2]]
6. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_12_img_1.png|page_12_img_1]]
7. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_14_img_1.png|page_14_img_1]]
8. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_14_img_2.jpeg|page_14_img_2]]
9. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_14_img_3.jpeg|page_14_img_3]]
10. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_17_img_1.jpeg|page_17_img_1]]
11. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_17_img_2.jpeg|page_17_img_2]]
12. [[../extracted_images/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based /page_17_img_3.jpeg|page_17_img_3]]

---

