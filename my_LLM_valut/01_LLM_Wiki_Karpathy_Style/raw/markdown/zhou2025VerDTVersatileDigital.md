# VerDT: A Versatile Digital Twins Framework for UAVs-Based Industrial Cyber-Physical Systems

Longyu Zhou , Member, IEEE, Supeng Leng , Member, IEEE, and Tony Q. S. Quek , Fellow, IEEE

AbstractâWith the development of cyber-physical systems, Digital Twins (DT)-powered network autonomy is emerging to embrace the fifth-generation industrial revolution. In this context, Unscrewed Aerial Vehicles (UAVs)-based low-altitude networks are expected to be the engines that drive industrial development. As an attractive industry application, UAVs-based intelligent logistics has been widely investigated to achieve a fully automated distribution manner without the aid of a workforce. However, it is difficult to perform real-time DT implementations due to limited computing resources and the high mobility of UAVs. To address the mentioned problems, we propose a Versatile DT (VerDT) framework operating at the edge. It can enable a double DT cooperation manner with a resource scheduling model and a path planning model for real-time and accurate logistics distributions. The resource scheduling model can implement the integration of computing and communication resources among UAVs for feasible cooperative distribution decisions. With the decisions, the path planning model can imitate to derive positions and velocities of UAVs for low-latency distribution performance with energy saving. Experiment results demonstrate the efficiency of our VerDT framework. Compared to state-of-the-art logistics distribution solutions, our solution reduces the distribution latency by 63.9% while improving the successful distribution ratio by 10.9%.

Index TermsâDigital twins, UAVs, intelligent logistics, cyberphysical systems.

## I. INTRODUCTION

D RIVEN by the Industrial Internet of Things (IIoT) andcyber-physical systems, the European Commission has a vision to explore the implementation of the fifth industrial revolution (industry 5.0) with the consideration of people and the environment based on the development of cyber-physical systems in leaps and bounds [1], [2], [3]. The new technological innovation can provide high-efficiency automatic services for the intelligent manufacturing industry. It can also facilitate the development of smart cities to derivative emerging industries, such as digital factories and intelligent logistics. Additionally, with the rapid promotion of the fifth generation wireless system (5G), the low-altitude network represented by Unscrewed Aerial Vehicles (UAVs) has been progressing well to contribute to the low-carbon industry 5.0 [4], [5]. Taking the UAVs-based intelligent logistics as an instance [6], UAVs can use onboard sensors to collect logistics information and transmit it to a central server for data processing based on the cloud automation paradigm. The decisions are distributed to instruct UAVs for high-efficiency logistics distributions with feasible flight paths.

Although the cloud automation paradigm can assist UAVs in planning feasible distribution paths with sufficient computing resources [7], [8], UAVs cannot implement long-distance logistics distribution missions with limited battery energy. A UAV swarm cooperation manner can improve the successful distribution ratio. However, the cloud-based paradigm causes high data transmission latency due to remote physical distances. It is challenging to find feasible cooperators for real-time logistics distributions. In addition, UAVs may implement frequent information exchanges among neighbors for accurate logistics distributions. It may expose significant pressure on the limited communication resources of UAVs.

The resource integration of computing and communication of UAVs may improve distribution efficiency for highly cooperative distribution performance. UAVs can use computing resources to implement efficient environmental estimation. The estimation results can assist UAVs in planning feasible distribution paths to reduce the frequency of communication with neighbors. However, it is challenging for UAVs to ensure an accurate environment estimation with computing resource limitations. In this case, the cloud server can provide extra computing resources to implement cooperative estimations. However, the cloud-based paradigm may lead to out-of-date estimation results due to high transmission latency for UAVs.

A flexible terminal-edge automation paradigm can implement high-efficiency resource integration to achieve low-latency distribution services [9], [10], [11]. Unfortunately, compared to the cloud automation paradigm, it exposes the problem of high UAV distribution latency for complex distribution scenarios. Artificial Intelligence (AI) is a potential tool to assist edge servers in analyzing complex environments [12], [13]. We can use conventional AI algorithms, such as Deep Determined Policy Gradient (DDPG), to enable UAVs to interact with complex distribution environments. The self-driven interaction manner can assist UAVs in exploring feasible cooperative distribution decisions for accurate logistics distributions [14]. However, It might lead to high computing latency with frequent iterations for accurate explorations. Furthermore, UAVs cannot collect comprehensive physical information to ensure accurate interactions with limited sensing ability. The issue motivates us to use the attractive Digital Twins (DT) technology with which we can build a mapping of the physical distribution scenario [15], [16]. The mapping can enable edge servers to construct a virtual space to derive feasible logistics distribution decisions with high-efficiency resource scheduling and path planning. We can use the DT technology to flexibly schedule computing resources for heterogeneous logistics distribution missions [17], [18]. With the high-efficiency resource scheduling performance, we can enable the DT technology to plan cooperative distribution paths by imitating flight positions, velocities, and postures of UAVs [19], [20]. The existing investigations ignore the mutual influence between resource scheduling and path planning for complex distribution scenarios. Consequently, we can only sometimes meet the requirements for low-latency logistics distribution.

Based on the above discussions, we propose a Versatile DT (VerDT) framework to achieve real-time and accurate logistics distributions in this paper. We deploy multiple UAVs with smallsized base stations as edge UAVs. The edge UAVs fly in different airspace to manage different terminal UAVs. Compared to the conventional DDPG algorithm with high computing latency, our VerDT solution can perform joint optimization of resource scheduling and path planning with two DT models. The DT models can empower UAVs to autonomously adjust distribution paths. It can significantly reduce frequency of model updates for low computing latency. Explicitly, the edge UAVs can first imitate to derive efficient resource scheduling of terminal UAVs. We then use the derivation results to implement path planning considering low distribution latency and flight energy consumption based on logistics information. In this case, we can ensure real-time and accurate UAVs-based logistics distributions by decoupling the traditional DT with a high computing complexity with heterogeneous resource orchestrations. The main contributions are summarized as follows.

We propose a Versatile DT (VerDT)-based logistics distribution framework for diverse logistics scenarios. Different from the existing DT-based logistics systems, our VerDT can build a serial double DT cooperation pattern. It can derive feasible cooperative distribution decisions through joint imitations of resource scheduling, positions, and velocities of UAVs based on a terminal-edge cooperation manner. Unlike the traditional terminal-edge cooperative network automation manner, our VerDT can achieve crosslayered computing resource cooperation. In addition, it can integrate computing and communication resources among UAVs. The multi-dimensional resource scheduling way can efficiently guarantee real-time and accurate logistics distribution with the improvement of resource utilization.

- To support the implementation of the VerDT framework, we propose a multi-modal learning-based model acquisition algorithm. Unlike conventional AI training with high computing latency, our algorithm can reshape data structures to perform low-latency DT model constructions using a lightweight attention mechanism. It can assist edge UAVs in constructing a resource scheduling twin model and a path planning twin model simultaneously through accurate multi-resource data analysis using a data compression method. The former DT model can assist UAVs in finding feasible cooperators for accurate logistics distributions by integrating computing and communication resources. The latter DT model can derive optimal distribution paths by imitating positions and velocities of UAVs to ensure lowenergy logistics distributions in real time.

- We verify the validation of our solution using a hardwarein-the-loop simulation. We deploy real DJI UAVs to collect environmental information in the practical physical scenario. With the reliable data, we use the Gazebo, a system simulation software, to construct a virtual logistics distribution scenario. Under different numbers of UAVs and distribution missions, the experiment results demonstrate that our VerDT solution can significantly reduce the distribution latency by 63.9% while improving the successful distribution ratio by 10.9% on average compared to the state-of-the-art logistics distribution solutions.

The rest of this paper is organized as follows. We discuss the existing work in Section II. Section III introduces the VerDT framework. To enable the framework, we formulate the logistics distribution model in Section IV. The corresponding algorithms supporting the VerDT framework are presented in Section V. Section VI provides the system evaluation results. Finally, Section VII concludes this paper.

## II. RELATED WORK

Many works have focused on the study of UAVs-based cyberphysical systems such as intelligent logistics for real-time and accurate logistics distributions [21], [22]. We discuss state-ofthe-art investigations with the representative intelligent logistics application in this section.

There are two concerned metrics in scenarios of UAVs-based intelligent logistics: distribution latency and successful distribution ratio. We can optimize the distribution latency by flexibly scheduling heterogeneous UAV resources. The authors in [17] proposed a DT-driven edge-end collaborative scheduling algorithm. The DT could derive UAV computing resource scheduling decisions to maximize transmission powers among UAVs. It could ensure a reliable logistics distribution through effective resource scheduling. Based on the optimization of transmit power, the authors in [18] further reduced transmission latency by only transmitting helpful information. It could facilitate cooperative logistics distributions. However, UAVs can only sometimes select feasible neighbors to implement high-efficiency resource collaboration due to dynamic moving trajectories. In this context, the authors in [23] proposed a two-stage optimization method to implement low-latency distributions by predicting suitable distribution paths in advance based on the information of cargoes. Unfortunately, it cannot provide accurate path-planning decisions in dynamic physical distribution environments.

<!-- image-->  
Fig. 1. Performance summary.

To ensure comprehensive environment observation, the authors in [24] built a logistics cloud platform based on blockchain technology. The cloud platform can perform global observation to instruct UAVs to implement cooperative distributions in an information-sharing manner. Blockchain technology can conduct UAVs to acquire consensus distribution decisions. It can further guarantee a high successful distribution ratio. Unfortunately, the cloud computing-based logistics platform incurs high transmission latency between UAVs and cloud servers. It is an obvious challenge to achieve a real-time distribution performance. To improve the logistics distribution time efficiency, the authors in [25] proposed a three-stage based distribution optimization algorithm. In the first stage, the author employed a statistical method to analyze the pattern of real-time delivery rate. Subsequently, a machine learning model was used to capture the underlying correlations between time efficiency and potential impacting factors. Finally, an explainable machine learning technique was used to quantify the contributions of the impacting factors to the time efficiency. It was verified to be efficient to reduce the distribution time based on the real JingDong logistics dataset. However, it may be inefficient to implement dynamic optimization of distribution paths for some urgent situations with high computing complexity.

To simplify the distribution implementation process, the authors in [26] presented a Predict-Then-Optimize Couriers Allocation (PTOCA) framework. Explicitly, a resource-aware prediction module was designed in the prediction stage to implement feasible resource scheduling. Then, a priority ranking module was designed to acquire a fair resource scheduling result. Finally, a task allocation module was designed to model the dynamic distribution environment using a Gated Recurrent Unit (GRU) network in the optimization stage. It can efficiently reduce the implementation latency for real-time logistics distributions. But it may be challenging to apply the algorithm to large-scale logistics scenarios with undetermined impacting factors. The authors in [27] developed a large-scale logistics network simulation software based on the real logistics network. Inspired by the DT technology [28], the authors established a virtual logistics network in the simulation software. It could implement accurate distribution imitation and predict suitable distribution paths for high-efficiency implementation.

Based on the above discussions, we summarize the performance of state-of-the-art investigations in Fig. 1. The advantage of the existing work is obvious to perform accurate logistics distributions based on the computing-intensive cloud servers.

<!-- image-->  
Fig. 2. Distinguished resources.

However, the disadvantage must be addressed with unreliable communication in complex UAVs-based logistics scenarios. Compared to the existing work, our Versatile DT (VerDT) framework can eliminate reliance on cloud services to achieve real-time logistics distributions through high-efficiency resource collaboration. It can also expand distribution areas of UAVs with cooperative path planning decisions. However, two technical challenges exist to achieve our VerDT for real-time logistics distribution with a high successful distribution ratio. Based on the analysis of resource skew in Fig. 2, we expect to collect complete data for accurate DT constructions with high resource utilization. It might cause high communication overhead by frequently adjusting sensing positions and directions of UAVs. We expect that effective resource scheduling can assist UAVs in finding feasible neighbors to implement cooperative distributions. With the two challenges and potentially high communication overhead, we provide our schemes in the subsequent sections for high-efficiency logistics distributions.

## III. SYSTEM MODEL

In this section, we propose a Versatile DT (VerDT) framework to serve the UAVs-based intelligent logistics scenarios.

We take a practical cargo delivery scenario as an instance to describe our proposed framework for clear understanding [6]. In such a scenario, logistic UAVs can receive distribution mission information from a central server to implement dynamic logistics distributions. It, however, can cause unacceptable pressures on communication resource scheduling and network management in the central server due to lots of UAVs involved. Inspired by [29], we can deploy multiple UAVs as edge UAVs flying in different air areas with small-sized base stations. It can reduce the UAV management difficulty to effectively schedule feasible computing and communication resources for high-efficiency cooperation among logistic UAVs. In the pattern, logistic UAVs can adjust flight positions to shorten communication distances for reliable communication among UAVs. The edge UAVs are indexed by $\mathcal { N } = \{ 1 , 2 , \dots , N \}$ . The logistic UAVs are indexed by $\mathcal { M } = \{ 1 , 2 , \dots , M \}$ . The set of logistic parcel (missions) is =defined as $\mathcal { K } = \{ 1 , 2 , \dots , K \}$ . Unfortunately, it is challenging = 1 2to serve large-scale logistics distribution scenarios with massive distribution missions due to the limitation of UAV sizes and energy in practical logistic scenarios [30].

Motivated by the advantages of DT [28], we propose a VerDT framework to achieve real-time logistic distributions with a high successful distribution ratio based on a double DT cooperation manner shown in Fig. 3. Our VerDT can assist logistic UAVs in exploring optimal distribution paths through accurate imitation and derivation with two kinds of DT models: a resource scheduling twin model and a path planning twin model. We can ensure a high imitation accuracy based on cooperative data collection of logistic UAVs. In addition, we can further enrich the data through a data generation method based on a Generative Adversarial Network (GAN). On the other hand, we can strengthen the DT derivation performance for efficient UAV path planning with our proposed DT cooperation manner. It not only reduces the time of logistic distribution but also can perform high scalability of our VerDT to diverse logistic scenarios. We can operate our VerDT sequentially with data sensing, data training, DT model acquisition, and cooperative path planning for high-efficiency distribution mission implementations. It is noted that we express the logistics UAVs as UAVs in the following sections for simplify. We summarize the main symbols in Table I. We provide details of our VerDT as follows.

<!-- image-->  
Fig. 3. Illustration of our proposed VerDT framework.

TABLE I  
LIST OF USED MAIN NOTATIONS IN THIS WORK
<table><tr><td>Notation</td><td>Description</td></tr><tr><td>M</td><td>Set of logistics UAVs</td></tr><tr><td> $\mathcal { K }$ </td><td>Set of distribution missions</td></tr><tr><td> $s$ </td><td>State information of all the UAVs</td></tr><tr><td> $D _ { i , j }$ </td><td>Physical distance between UAViand j</td></tr><tr><td> $\mathrm { D T _ { R S } }$ </td><td>Resource scheduling twin model</td></tr><tr><td> $\mathrm { D T _ { P P } }$ </td><td>Path planning twin model</td></tr><tr><td> $\boldsymbol { r } _ { i , j }$ </td><td>Transmission ratio from UAVi to j</td></tr><tr><td> $t ^ { C ^ { \dagger } }$   $\iota _ { i , s }$ </td><td>Sensing latency ofUAVi for content information</td></tr><tr><td> $t _ { i , s } ^ { \prime }$ </td><td>Sensing latency of UAVi for image information</td></tr><tr><td> $t _ { i , s }$ </td><td>The whole sensing latency of UAV i</td></tr><tr><td> $E _ { i } ( n )$ </td><td>Computing energy consumption of UAV i</td></tr><tr><td> $t _ { g }$ </td><td>GPU processing time</td></tr><tr><td> $t _ { u }$ </td><td>CPU processing time</td></tr><tr><td> $\iota$ </td><td>Energy consumption percentage</td></tr><tr><td> $v _ { l } ( t )$ </td><td>Time of information diffusion</td></tr><tr><td> $\eta$ </td><td>Successful distribution ratio</td></tr></table>

## A. Complete Data Acquisition

In the physical logistics space, the logistic UAVs can implement the data acquisition mission. The data mainly includes logistic information, distribution environment information, and neighbor status (such as positions, velocities, and postures). The logistic UAVs can use onboard sensors (camera, ultrasonic, and depth vision sensor) to obtain distribution environment information using a cooperative sensing method [31]. It can instruct logistic UAVs to dynamically adjust sensing postures and positions. The neighbor status can be gained through information exchange among UAVs.

However, the method cannot always ensure complete data collection in dynamic environments. We propose a GAN-based data generation algorithm to improve the completeness of data collection with a data generation operation. We can use it to generate heterogeneous physical information such as images and contents. Different from the existing GAN network, we embed a switch (ON/OFF) procedure to empower an adaptive data generation action. Our algorithm can trigger on-off to implement the corresponding training process based on analysis of data types (step 1 to step 3 in Fig. 3 and details shown in Section V-A). In this case, logistic UAVs can obtain rich physical information to construct accurate DT models for high-efficiency distribution path planning.

## B. DT Model Construction

UAVs can transmit the information to edge UAVs through available communication resources to support such shortdistance transmissions. With the aid of the powerful computing ability of edge UAVs, we can build a virtual space where edge UAVs can train the information to obtain customized DT models using our proposed multi-modal learning-based model acquisition algorithm. It can endow the different DT models with personal functions to perform versatile logistics missions with a cross-modality attention mechanism. The mechanism can accurately select feasible heterogeneous data by extracting key information using a data aggregation operation.

Based on this, we can construct two kinds of DT models: the Resource Scheduling Twin (RST) model and the Path Planning Twin (PPT) model (step 4 in Fig. 3). The RST model focuses on performance improvement of resource utilization by deriving the changes in physical environments (including buildings and surrounding neighbors). It can also enable UAVs to implement information exchanges among neighbors based on available communication resources. The integration of communication and computing can efficiently ensure collision avoidance for real-time logistic distribution. The RST model $\mathrm { D T _ { R S } }$ is represented as

$$
\mathrm { D T } _ { \mathrm { R S } } = \{ f _ { e , e } , f _ { e , d } , \mathcal { F } , \mathcal { B } , \mathcal { R } \} ,\tag{1}
$$

where $f _ { e , e }$ and $f _ { e , d }$ are the external frequency and frequency doubling of edge UAVs, respectively. $\mathcal { F } = [ f _ { 1 } , f _ { 2 } , \dotsc , f _ { M } ]$ is a = [ ]vector to denote frequencies of Central Processing Unit (CPU) of UAVs; $\boldsymbol { B } = [ B _ { 1 } , B _ { 2 } , \dots , B _ { M } ]$ is a vector to present the set of = [ ]assigned bandwidths for all the UAVs; R is an matrix to denote the transmission rate between any two UAVs with $\mathcal { R } _ { i , j } = r _ { i , j }$ . It =is a fact that UAV i can only transmit information to surrounding neighbors efficiently due to limited communication resources. Therefore, R is a sparse matrix. Based on the derivation result of DTRS, the PPT model can continue to derive feasible distribution paths with logistics information. The PPT model is formulated as

$$
\begin{array} { r } { \mathrm { D T } _ { \mathrm { P P } } = \{ \mathcal { K } , \mathcal { S } , \mathcal { D } , \mathcal { E } \} , } \end{array}\tag{2}
$$

where $\mathcal { K } = [ 1 , 2 , \dots , K ]$ is a vector that denotes all the logistics missions; $\boldsymbol { S } = [ S _ { 1 } , S _ { 2 } , \dots , S _ { M } ]$ is the status of all the UAVs = [where, for each UAV i, $S _ { i } = \{ p _ { i } , v _ { i } , a _ { i } \}$ . The three elements =represent UAV iâs position, velocity, and posture, respectively. D is an matrix of physical distances where $\mathcal { D } _ { i , j }$ is the physical distance between UAV i and $j . \mathcal { E } = [ E _ { 1 } , E _ { 2 } , . . . , E _ { M } ]$ is a vector where $E _ { i }$ = [ ]denotes the available energy of UAV i. We can use the two DT models to implement customized logistics services through resource integration (details shown in Section V-B).

## C. Cooperative Resource Scheduling

To achieve accurate resource scheduling derivation in the virtual space, we propose an Integrated Communication and Computing (ICC) algorithm (step 5 to step 6 in Fig. 3). It can implement trajectory derivation of neighbors to plan feasible distribution paths. The computation results are transmitted to neighbor UAVs for cooperative distributions. The communication model $a _ { i } [ l ]$ for l-th symbol is presented as

$$
\begin{array} { r } { a _ { i } [ l ] = \varpi _ { p , i } \times f _ { N _ { i } } ^ { \mathrm { t r a } } ( C _ { i } [ l ] ) , } \end{array}\tag{3}
$$

where $l \in \mathcal L$ denotes l-th communication symbol with L symbols; $\varpi _ { p , i }$ is the precoding matrix of communication symbols. We use the Wifi 6 technology to implement data transmission [32]. $C _ { i } [ l ]$ represents an individual communication signal; $f _ { N _ { i } } ^ { \mathrm { t r a } } ( C _ { i } [ l ] )$ is a function that can combine the computing results ( [ ])(trajectory prediction) of $N _ { i }$ neighbor UAVs and communication signals. We formulate a transmission power model for UAV i:

$$
t r ( A _ { i } ) = t r \left( E \left[ a _ { i } [ l ] a _ { i } [ l ] ^ { H } \right] \right) ,\tag{4}
$$

where $t r ( A _ { i } )$ denotes the trace of matrix $A _ { i }$ . Considering the ( )practical low-altitude UAV network, we use the Nakagami fading model $N _ { i , j }$ to reflect the channel between UAV i and $j [ 3 3 ]$ . The Signal-to-Interference-plus-Noise Ratio (SINR) $\Pi _ { i , j }$ at UAV j is formulated as

$$
\Pi _ { i , j } = N _ { i , j } A _ { i } N _ { i , j } ^ { H } G _ { i , j } ^ { - 1 } ,\tag{5}
$$

where $G _ { i , j } ^ { - 1 }$ denotes the interference of other UAVs with physical noises. The transmission rate between UAV i and $j$ is obtain to construct $\mathrm { D T } _ { \mathrm { R S } }$ with the parameter R:

$$
r _ { i , j } = B \log _ { 2 } d e t \left( I _ { N _ { i } } + \Pi _ { i , j } \right) .\tag{6}
$$

In this case, we can integrate communication and computing resources of UAVs to perform accurate and real-time logistics distributions (details shown in Section V-C).

## D. Cooperative Path Planning

With the resource scheduling operation, we can efficiently use the available resources of UAVs to explore feasible pathplanning decisions. To make the PPT model to derive lowlatency distribution paths with a high successful distribution ratio in the virtual space, we propose a Particle Swarm Optimization-based distribution Path Planning (PSO-PP) algorithm (step 7 to step 8 in Fig. 3). Unlike the traditional PSO algorithms [34], our algorithm can enable particles to simultaneously explore feasible paths from two dimensions of velocity and position. It can assist UAVs in acquiring accurate distribution paths. On the other hand, it can implement directional exploration to narrow the exploration area for real-time executions based on logistics information and environment estimation (details shown in Section V-D). In the next section, we formulate the objective function to optimize the distribution performance.

Supported by the VerDT framework, UAVs can implement a cooperative data collection operation to ensure complete data acquisition with step 1. The data can be further enriched for accurate DT construction using our proposed GAN-based data generation algorithm with step 2. With the heterogeneous data, edge UAVs can construct two kinds of accurate DT models, the RST and PPT models, through our proposed multi-modal learning-based model acquisition algorithm with steps 3, 4, and 5. The RST model can collaborate resources of computing and communication of logistics UAVs by deriving changes in physical distribution environments with step 6. Based on resource collaboration results, edge UAVs can enable the PPT model to plan cooperative distribution paths for logistics UAVs with step 7. The logistics UAVs can achieve accurate and real-time logistics distributions through multi-dimensional optimization in resource scheduling and cooperative path planning with step 8.

Our framework can ensure high-efficiency path planning for accurate and real-time logistics distributions with high resource utilization by collaborating computing and communication resources. Compared to existing centralized and distributed DT frameworks [15], [16], we can enable our RST model to flexibly schedule the computing and communication resources by estimating the environmental changes. It can assist UAVs in exploring feasible numbers of neighbors for cooperative distributions instead of all the neighbors. Based on this, our PPT model can acquire low-latency path planning decisions with a few involved UAVs. The decisions can instruct the RST model to perform accurate neighbor selection for low energy consumption in the communication resource. In this case, our framework can trade off the performance cost between the resource scheduling and the path planning for accurate and real-time logistics distributions.

## IV. PROBLEM FORMULATION

In this section, we formulate a distribution optimization model for real-time logistics distributions with a high successful distribution ratio based on our VerDT.

## A. Analysis of UAV Sensing

In the physical space, UAVs can collect environmental information and the status of neighbor UAVs based on onboard sensors. The information includes contents (such as physical distance among UAVs), images (such as sizes of buildings), and videos (such as mobile paths of neighbors). We can implement a complete data collection by adjusting the postures of UAVs. For UAV i, Y onboard sensors can implement the data collection with diverse sensing rates. It is a fact that we can use $Y$ sensors simultaneously through different Input/Output interfaces. In this case, we can acquire sensing latency of UAV i, $t _ { i , s } ^ { C }$ , for content information:

$$
t _ { i , s } ^ { C } = \operatorname* { m a x } \left\{ \frac { 1 } { f _ { 1 } } \alpha _ { 1 } , \frac { 1 } { f _ { 2 } } \alpha _ { 2 } , \ldots , \frac { 1 } { f _ { Y } } \alpha _ { Y } \right\} ,\tag{7}
$$

where $f _ { 1 } , \dots , f _ { y } \ge f _ { N }$ are the sampling rates for Y sensors, where $f _ { N }$ is the Nyquist sampling rate; $\alpha _ { 1 } , \ldots , \alpha _ { Y }$ are the numbers of sampling for $Y$ sensors. It is noted that $f _ { y } = 0$ if = 0the sensor y cannot collect content information. The sensing latency of UAV i for image information is given by

$$
t _ { i , s } ^ { I } \mathrm { = m a x } \left\{ \frac { w _ { 1 } h _ { 1 } \mathrm { f r } _ { 1 } \mathrm { D e } _ { 1 } } { f _ { 1 } } , \frac { w _ { 2 } h _ { 2 } \mathrm { f r } _ { 2 } \mathrm { D e } _ { 2 } } { f _ { 2 } } , \ldots , \frac { w _ { Y } h _ { Y } \mathrm { f r } _ { Y } \mathrm { D e } _ { Y } } { f _ { Y } } \right\} ,\tag{8}
$$

where $w _ { y }$ and $h _ { y }$ are the width and height of an image, respectively; $\mathrm { f r } _ { y }$ is the frame rate of sensor y; $\mathrm { D e } _ { y }$ is the image depth (Bit) based on sensor $y .$ It is worthy noting that we can splice multiple images to acquire videos. Therefore, we can only obtain image information for videos. In this case, the whole sensing latency is presented as

$$
t _ { i , s } = \operatorname* { m a x } \left\{ t _ { i , s } ^ { C } , t _ { i , s } ^ { I } \right\} .\tag{9}
$$

## B. Analysis of UAV Computing

In the virtual space, we can empower the UAVs to use DTRS for trajectory derivation of neighbors. It can ensure cooperative resource scheduling based on the derivation results. The traditional Kalman Filter (KF) prediction method can lead to a high error accumulation for highly dynamic trajectory prediction. We select the Unscented Filter (UF) method with a sampling operation to implement trajectory prediction. The sampling way can reduce the prediction error to ensure a high-accuracy requirement. We can adjust sampling frequency to achieve a real-time prediction manner.The motion model of neighbor j is defined as $x _ { j } ( t ) = f _ { j } ( t - 1 , x _ { j } ( t - 1 ) , \delta ( t - 1 ) )$ . We can use a motion estimation model $z _ { j } ( t ) = h _ { j } ( t , x _ { j } ( t ) , w ( t ) )$ to analyze the prediction performance, where $x _ { j } ( t )$ is the position coordinate of the neighbor $j ; \delta ( t )$ and $w ( t )$ are zero mean noises that ( ) ( )obey the Gaussian distribution, respectively; $f _ { j } ( X )$ is a state ( )transform function. The sampling process is formulated as

$$
x _ { j } ^ { ( i + n ) } ( t ) | _ { x _ { j } ( t ) } = \hat { x _ { j } } ( t ) | _ { x _ { j } ( t ) } - \sqrt { ( n + \kappa ) P _ { j } ( t ) } _ { i } \omega ^ { ( i + n ) } ,\tag{10}
$$

where Îº is the scaling factor; $\omega ^ { ( i + n ) }$ is a weight coefficient; $\begin{array} { r } { \hat { x } ( t + 1 | t ) = \sum _ { i = 0 } ^ { 2 \bar { n } } \omega ^ { ( i ) } \hat { x } ^ { ( i ) } ( t + 1 | t ) } \end{array}$ . The state prediction covariance is defined as $\begin{array} { r } { P ( t + 1 | t ) = \sum _ { i = 0 } ^ { 2 n } \omega ^ { ( i ) } [ \hat { x } ( t + } \end{array}$ $1 | t ) - \hat { x } ^ { ( i ) } ( t + 1 | t ) ] [ \hat { x } ( t + 1 | t ) - \hat { x } ^ { ( i ) } ( t + 1 | t ) ] ^ { T } ; \stackrel { \sim } { \omega } ^ { ( i + n ) }$ [Ë( +is de-1 ) Ërived as $\begin{array} { r } { \hat { z } ( t | t - 1 ) = \sum _ { i = 0 } ^ { 2 n } \omega ^ { ( i ) } \hat { z } ^ { ( i ) } ( t | t - 1 ) } \end{array}$ )], where $\hat { z } ^ { ( i ) } ( t | t -$ $1 ) = h ( t , \hat { x } ^ { ( i ) } ( t | t - 1 ) ) ; h ( \cdot )$ Ë ( 1) Ë (is the nonlinear observation vector. 1) = ( Ë ( 1)) ( )The estimation covariance is $\begin{array} { r } { S ( t ) = \sum _ { i = 0 } ^ { 2 n } \omega ^ { ( i ) } [ \hat { z } ( t | t - 1 ) - } \end{array}$ $\hat { z } ^ { ( i ) } ( t | t - 1 ) ] [ \hat { z } ( t | t - 1 ) - \hat { z } ^ { ( i ) } ( t | t - 1 ) ] ^ { T }$ [Ë( 1). The trajectory is pre-Ë (dicted as $x _ { i } ^ { p } = { \hat { x } } ( t + 1 | t ) + W ( t + 1 ) [ z ( t + 1 ) - { \hat { z } } ( t + 1 | t ) ]$ where $W ( t + 1 )$ Ë( + 1 ) + ( + 1)[ ( + 1) Ë( + 1 )]is the system gain which is acquired through the ( + 1)prediction covariance and the observation vector. Based on this, we can discover that the time complexity of UF is mainly from stages of estimation and prediction. The whole time complexity $O ( n )$ is presented as $\begin{array} { r } { O ( \bar { n } ) = \frac { 3 n ^ { 2 } } { 2 } + \frac { 3 n } { 2 } \left[ 3 5 \right] } \end{array}$ , where n is the size ( ) ( ) = + of input. We can then calculate the computing consumption of UAV i [36]:

$$
E _ { i } ( n ) = c _ { 1 } O ( n ) + \frac { c _ { 2 } n ^ { 4 } } { O ( n ) ^ { 3 } } + \frac { c _ { 3 } n ^ { 3 } } { O ( n ) ^ { 2 } } + c _ { 4 } n < E _ { i , \mathrm { m a x } } ,\tag{11}
$$

where $E _ { i , \mathrm { { m a x } } }$ is the maximal budget of UAV i for computing consumption. The prediction accuracy is also guaranteed by

$$
\| x _ { j } ^ { p } - x _ { j } \| \leq d _ { \operatorname* { m a x } } ^ { p } ,\tag{12}
$$

where $x _ { j }$ is the real position of UAV j and $d _ { \mathrm { m a x } } ^ { p }$ is the maximal acceptable prediction error.

In addition to the computing resource consumed by UAVs, we also consider the computing overhead of DT construction in the edge UAVs. We can neglect energy consumption due to sufficient computing resources owned by edge UAVs. We mainly consider the DT construction latency. To ensure real-time DT construction, we use the Graphics Processing Unit (GPU) to accelerate the Central Processing Unit (CPU)-based data process. We assume edge UAVs process Î· bytes of data. The GPU processes $\eta _ { 1 }$ bytes of data, and the CPU processes Î·2 bytes of data, where $\eta _ { 1 } + \eta _ { 2 } = \eta$ . The GPU processing time is formulated as [37]

$$
t _ { g } = \operatorname* { m a x } \left\{ \frac { \eta _ { 1 } } { \phi } , \frac { \chi } { \beta } \right\} ,\tag{13}
$$

where $\phi$ is the bandwidth of GPU memory (bytes/s); $\chi$ is the number of GPU runs; $\beta$ is the number of GPU blocks. With a sequential implementation manner, we formulate the CPU

processing time as [38]

$$
t _ { u } = \sum _ { c = 1 } ^ { \eta _ { 2 } } \frac { 1 } { f _ { c } } ,\tag{14}
$$

where $f _ { c }$ is the frequency of CPU.

## C. Analysis of UAV Communication

UAVs can implement information exchange with neighbors for accurate logistics distributions. We can enable UAVs to transmit lightweight model parameters to reduce the data size where the communication data overhead can be neglected. However, we need to ensure low-latency data transmission for real-time logistics distributions. For UAV i, we use an accumulative average method to formulate the communication latency model for a high-efficiency data transmission:

$$
t _ { \mathrm { c o m m } } = \operatorname* { l i m } _ { T  \infty } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \frac { \frac { \sum _ { j = 1 } ^ { N _ { i } } G _ { i } } { r _ { i , j } } } { [ \sum _ { i = 1 } ^ { N _ { i } } y _ { i , j } ] ^ { * } } \leq T _ { i , c } ,\tag{15}
$$

where $[ y ] ^ { * } = \operatorname* { m a x } \{ 1 , y \} ; G _ { i }$ is the data size of UAV i for [ ] = max 1information exchanges; $T _ { i , c }$ Tic is the maximal acceptable communication latency for information exchanges.

## D. Analysis of UAV Flight

In addition to the analysis of resource scheduling, we can infer the flight energy consumption to ensure cooperative logistics distributions. We consider the flight power consumption for UAVs from four aspects: Back EMF loss, Direct Current (DC) brushless motor power loss, iron loss, and copper loss [39]. For UAV i, the Back EMF loss $P _ { i , B }$ is inferred as $P _ { i , B } =$ $Q _ { i } \times R _ { i }$ , where $Q _ { i }$ and $R _ { i }$ =are the torque and rotational speed (rad/s), respectively. The DC brushless motor power loss $P _ { i , b }$ is $P _ { i , b } = V _ { B } I _ { B }$ , where $V _ { B }$ and $I _ { B }$ are voltage and current of the Back EMF, respectively. The iron loss $P _ { i , \mathrm { i r } }$ is formulated as $P _ { i , \mathrm { i r } } = \zeta \varepsilon \nu ^ { 2 }$ , where $\zeta , \varepsilon ,$ and Î½ are Steinmetz coefficient, =frequency of motors (Hz), and peak magnetic flux density (T). The copper loss $P _ { i , \mathrm { c o } }$ is $P _ { i , \mathrm { c o } } = I _ { B } ^ { 2 } R$ , where R is the resistance =of the propulsion system circuit. Based on this, we can give the flight energy consumption within a time t (second) for UAV i:

$$
E _ { i } = ( P _ { i , B } + P _ { i , b } \vartheta + P _ { i , \mathrm { i r } } + P _ { i , \mathrm { c o } } ) \times t ,\tag{16}
$$

where $\vartheta$ is the number of brushless motors (namely, the number of blades). We ensure a smooth logistic distribution by controlling the energy consumption percentage Î¹:

$$
\iota = \left( 1 - \frac { E _ { i , \mathrm { b u } } - E _ { i } } { E _ { i , \mathrm { b u } } } \right) \geq \iota _ { \operatorname* { m i n } } ,\tag{17}
$$

where $E _ { i , \mathrm { b u } } = V _ { i , \mathrm { b u } } \times C _ { i , \mathrm { b u } }$ is the maximal energy budget of UAV i; $V _ { i , \mathrm { b u } }$ =and $C _ { i , \mathrm { b u } }$ are voltage supply of battery (V) and capacity of battery (Ah), respectively. $l _ { \mathrm { { m i n } } }$ is the minimal residual energy which ensures cooperative distributions.

## E. Objective Formulation

To assure real-time logistics distributions with a high successful distribution ratio, we invoke the Lyapunov methodology

to formulate the optimization model with the consideration of cooperative resource scheduling:

$$
\begin{array} { c } { { P 1 : \displaystyle \operatorname* { m i n } \left\{ \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T } \left[ \sum _ { i = 1 } ^ { M } \sum _ { k = 1 } ^ { K } \Delta ( t _ { i , k } ) \right] \right\} , \hfill } } \\ { { \mathrm { s . t . } \left\{ { \begin{array} { l } { { C 1 : t _ { i , s } + t _ { g } + t _ { u } + t _ { \mathrm { c o m m } } \leq t _ { i , k } \forall k \in K } } \\ { { C 2 : r _ { i , j } \geq r _ { \mathrm { m i n } } , \forall i , j \in \mathcal { M } } } \\ { { C 3 : ( 1 1 ) , ( 1 2 ) , ( 1 5 ) , ( 1 7 ) } } \end{array} } \right. } } \end{array}\tag{18}
$$

where $\Delta$ denotes the difference between the real backlog and Îthe virtual backlog [40]. Explicitly, $\Delta ( t _ { i , k } ) = L _ { 1 , i , k } - L _ { 2 , i , k } ,$ where $L _ { 1 , i , k }$ and $\boldsymbol { L } _ { 2 , i , k }$ Î( ) =are the actual distribution time and expected distribution time. We push $L _ { 1 , i , k }$ to approach $L _ { 2 , i , k }$ for real-time distributions; C2 is the constraint of the transmission rate. In C3, (11) constrains the computing consumption of UAVs; (12) can make UAVs to seek out feasible neighbors for cooperative distributions; (15) ensures low-latency communications during cooperation; (16) guarantees the smooth distributions with feasible path planning decisions. It can facilitate UAVs to achieve the distribution mission for a high successful distribution ratio.

The P 1 is proved to be an NP-hard problem based on the detailed proof process shown in Appendix A. We can only sometimes explore optimal logistics distribution decisions with different numbers of UAVs and distribution missions. We can use AI algorithms such as machine learning and heuristic methods to implement iterative explorations for real-time and cooperative distributions with a high successful distribution ratio. However, it is essential to implement such intelligent algorithms through the support of sufficient computing resources. In this case, we need to collaborate heterogeneous resources of UAVs to improve resource utilization for performance enhancement based on accurate environment estimation. To achieve this, we can use the DT technology to imitate and derive the changes in distribution environments for high-efficiency resource scheduling and path planning. We provide detailed algorithms in Section V.

## V. VERDT-BASED LOGISTICS DISTRIBUTION METHOD

This section presents our solution for the formulated objective function in Section IV.

To ensure accurate DT construction, we need to acquire complete physical information. We propose a GAN-based data acquisition algorithm with a cooperative data collection manner. We can then process the heterogeneous data to construct accurate DT models using our proposed multi-modal learning-based mobile acquisition method. It can assist the UAV distribution system in estimating the changes in physical environments through scenario imitation and derivation. We can propose corresponding resource scheduling and path planning algorithms to ensure lowlatency logistics distributions with a high successful distribution ratio. In this context, we can solve the objective function by decoupling it into four sub-problems with the corresponding four algorithms.

<!-- image-->  
Fig. 4. Illustration of data acquisition.

## A. GAN-Based Data Acquisition

As mentioned in Section III-A, we propose a GAN-based data acquisition algorithm in the physical space with two steps: cooperative data collection and data augmentation. The cooperative data collection is achieved by dynamically adjusting directors of sensors to acquire comprehensive data using an efficient data sensing method [41]. However, the method cannot always perform comprehensive data collection in dynamic logistics scenarios. It is essential to augment the data for the data completeness. Our GAN-based data acquisition algorithm can augment the data completeness by adversarial training with an ON/OFF function.

As shown in Fig. 4, we use the GAN network to train the collected data to enrich image and content data simultaneously. For the image data, we can combine noise images and a Convolutional Neural Network (CNN) to acquire extra image information for data augmentation. The noise images are obtained using a map function. It converts a noise vector z with a Gaussian distribution to a noise image based on the given true image information. We use the CNN network to extract the image information of neighbors and buildings. Specifically, the training dataset is prepared based on the UAV image dataset. We construct a CNN with one input layer, three convolutional layers, three pooling layers, one fully connected layer, and one output layer. The size of input image I is denoted as $I = H \times W \times C .$ =where H, W , and C are the height and width of image I and number of channels, respectively. It is trained in the convolutional layer with different numbers of convolutional kernels. After the convolution operation, the feature image IY can be represented as $\begin{array} { r } { I _ { Y } = ( \frac { H - \dot { K } _ { h } + 2 p } { s } + 1 ) \times ( \frac { W - K _ { w } + \widecheck { 2 p } } { s } + 1 ) \times M } \end{array}$ , where $K _ { h }$ and $K _ { w }$ ( + 1) ( + 1)are height and width of convolutional kernel K, respectively; p and s denote padding and stride, respectively; M is the number of convolutional kernels. We then use the pooling layer to reduce the sizes of feature images to acquire important features with the ReLU activation function. It is also used in fully connected layers with 64 neural units. The training results are output by the output layer with ten neural units using the SoftMax activation function. We implement multiple iterative trainings with 100 epochs with 64 batch size for minimizing the Loss function $\begin{array} { r } { L _ { \mathrm { C N N } } = - \sum _ { a = 1 } ^ { C _ { k } } I _ { Y } ( a ) \log ( \hat { I _ { Y } ( a ) } ) } \end{array}$ , where $I _ { Y } ( a )$ and $\hat { I _ { Y } ( a ) }$ are the true label and the output probability, ( )respectively; $C _ { k }$ is the number of classes. We use the Adam optimizer to update network weights with a learning rate of 0.001.

The image information is inputted to a generation network to generate synthetic images. The discriminator network can distinguish true images from synthetic images with a classified label. The discriminate images are transmitted to the generator network for accurate data generation. Explicitly, we deploy three fully connected layers and one deconvolution layer in the generation network, where the ReLU activation function is used to connect the two kinds of network layers for smooth training. We use the  activation function to output the generation results. tanhThe results can be estimated by the formulated Loss function $V _ { G }$ based on the WGAN method with Gradient Penalty [42]:

$$
\begin{array} { r l } & { V _ { G } = \mathrm { ~ - ~ } \mathrm { E } _ { x \sim P _ { d } } [ D ( x ) ] + \mathrm { E } _ { z \sim P _ { z } } [ D ( G ( z ) ) ] } \\ & { ~ + ~ \varrho \mathrm { E } _ { \hat { x } \sim D _ { \hat { x } } } [ ( \| \nabla \hat { x } D ( \hat { x } \| - 1 ) ^ { 2 } ] , } \end{array}\tag{19}
$$

where x is given true samples; $D ( x )$ and $D ( G ( z ) )$ are proba-( ) ( ( ))bility values based on the true samples x and generated samples $G ( z )$ , respectively; $P _ { d }$ and $P _ { z }$ are real data distribution and false samples from the noise vector $z ; \varrho$ is the weight of gradient plenty; x is the interpolated samples acquired by random sam-Ëpling between the real samples and the generated samples.

We deploy three convolutional layers and one fully connected layer for the discriminator network. We use the Leaky ReLU activation function to connect the two kinds of network layers. The training results can be obtained by the Sigmoid activation function. The formulated loss function $V ( D )$ can evaluate the results using the WGAN method [43]:

$$
V _ { D } \mathrm { ~ -- ~ } \mathrm { E } _ { z \sim P _ { z } } [ D ( G ( z ) ) ] .\tag{20}
$$

We can maximize the $V _ { G }$ and minimize the $V _ { D }$ to achieve data augment. We set the noise dimension for each iteration as 100 with 64 batch sizes. We implement 1000 epochs based on the Adam optimizer with a 0.0002 learning rate to stabilize the learning process. Under iterative training, both networks can update their parameters to obtain a convergent state. The involved training aim is formulated as

$$
\operatorname* { m a x } _ { D } \operatorname* { m i n } _ { G } \operatorname { E } _ { x \sim P _ { D } } \log D ( x ) + \operatorname { E } _ { z \sim P _ { z } } \left[ \log ( 1 - D ( G ( z ) ) ) \right] ,\tag{21}
$$

From the perspective of the network training, we can enable the generation network to train the data for an expected gradient $\Delta _ { \theta _ { G } } \mathrm { E } \{ J _ { \theta _ { G } ( \theta _ { G } ; \theta _ { D } ) } \}$ , where $\theta _ { G }$ and $\theta _ { D }$ is the parameters of gen-Î Eeration network and discriminator network; $J ( x )$ is the gradient ( )function. We can use the gradient value to update the generation parameter $\theta _ { G } = \theta _ { G } ( \Delta _ { \theta _ { G } } )$ . The discriminator network can respond to the update with an asynchronous update manner to explore the corresponding gradient value $\Delta _ { \theta _ { D } } \mathrm { E } \{ J _ { \theta _ { D } ( \theta _ { D } ; \theta _ { G } ) } \}$ . The gradient value is used to update the parameter $\theta _ { D } = \theta _ { D } ( \Delta _ { \theta _ { D } } )$ = (Î )The implementation process is the same as that of content information without the CNN network. In this case, we can obtain the extra information from the generation network for accurate DT construction.

## B. DT Model Acquisitions

Based on the fresh physical information, we can train the data to acquire versatile DT models DTRS and DTPP for highefficiency logistics distributions in UAV scenarios. Considering the data heterogeneity, we propose a multi-modal learning-based model acquisition algorithm. As shown in Fig. 5, firstly, the heterogeneous data (contents, images, and videos) can be represented by a tensor $\mathrm { E n v } = [ \mathrm { E n v } _ { C } , \mathrm { E n v } _ { I } , \mathrm { E n v } _ { V } ]$ , where the three = [ ]elements denote the content information, image information, and the video information, respectively. Our algorithm can enable to obtain the key data tensor ${ \kappa _ { \mathrm { E n v } } }$ with a model-1 Khatri-Rao product:

<!-- image-->  
Fig. 5. Illustration of the DT model acquisition.

$$
K _ { \mathrm { E n v } } { } ^ { i } = \mathrm { E n v } ^ { i } \odot _ { 1 } \mathrm { E n v } , i \in \{ 1 , 2 , 3 \} .\tag{22}
$$

With the key information, our algorithm can extract customized information from the heterogeneous data to construct DT models using an attention mechanism. However, it is a fact that the attention mechanism cannot efficiently process high dimensional tensors due to distinguished information differences among different dimensions. In this case, our algorithm can implement a flat data processing by compressing dimensions with a reshape function $f _ { \mathrm { r e s h a p e } }$ [44]:

$$
\rho _ { \mathrm { E n v } } = f _ { \mathrm { r e s h a p e } } \left( \left( \mathrm { E n v } ^ { 1 } \xi _ { 1 } \right) \odot _ { 1 } \left( \mathrm { E n v } ^ { 2 } \xi _ { 2 } \right) \odot \left( \mathrm { E n v } ^ { 3 } \xi _ { 3 } \right) \right) ,\tag{23}
$$

where $\xi _ { 1 } , \xi _ { 2 }$ , and $\xi _ { 3 }$ are linear transformation matrices. With the flat physical information, we can implement the attention mechanism with an attention core matrix and a pooling matrix. The attention core matrix $\rho _ { \mathrm { E n v } , \mathcal { K } }$ is formulated with the Hadamard product:

$$
\rho _ { \mathrm { E n v } , \mathcal { K } } ^ { i } = \mathrm { E n v } ^ { i } \circ \mathcal { K } ^ { i } .\tag{24}
$$

The attention core matrix is used to explore relations among different kinds of data through information passing. The passing way is achieved by a pooling operation. The attention pooling matrix is deduced as

$$
M _ { \mathrm { E n v } } ^ { i } = f _ { p } \left( \rho _ { \mathrm { E n v } , \mathcal { K } } { } ^ { i } ( s , w , r ) \right) ,\tag{25}
$$

where $f _ { p }$ is a pooling function for information passing; $1 \leq$ $s \leq S , \ \mathrm { i } \leq w \leq W .$ , and $1 \leq r \leq R . \ S$ 1, W , and R are the 1 1dimensions of EnvC, EnvI, and EnvV , respectively. We can acquire corresponding customized attention tensors AtRS and AtPP when the information passing process finishes:

$$
\mathrm { A t } _ { \mathrm { R S } } = f _ { \mathrm { D T } _ { R S } } \left( \prod _ { i } \rho _ { \mathrm { E n v } , \mathcal { K } } ^ { i } \varsigma _ { i } M _ { \mathrm { E n v } \mathcal { K } } ^ { i } \right) ,\tag{26}
$$

$$
\mathrm { A t } _ { \mathrm { P P } } = f _ { \mathrm { D T } _ { P P } } \left( \prod _ { i } \rho _ { \mathrm { E n v } , K } ^ { i } \varsigma _ { i } { \cal M } _ { \mathrm { E n v } K } ^ { i } \right) ,\tag{27}
$$

Algorithm 1: Model Acquisition.   
Input: Physical information Envc,Env1,and Envv;   
GAN network parameters.   
Output: The versatile DT models.   
1 Implement a cooperative sensing using [41]   
2 Construct the GAN network model with parameters   
3 Generate the noise contents and images   
4 if image information is true then   
5 Implement CNN network to obtain desired data   
6 for each iteration do   
7 Obtain the gradient value ${ \Delta _ { \theta _ { G } } } \mathcal { E } \{ J _ { \theta _ { G } ( \theta _ { G } ; \theta _ { D } ) } \}$   
8 Generate content samples based on the   
Generation network   
9 Update the parameter $\theta _ { G }$   
10 Obtain the gradient value $\Delta _ { \theta _ { D } } \mathcal { E } \{ J _ { \theta _ { D } ( \theta _ { D } ; \theta _ { G } ) } \}$   
11 Update the parameter $\theta _ { D }$   
12 Compute the training aim using (21)   
13 Transmit all the data to edge UAVs   
14 Extract key information using (22)   
15 Reshape the data for dimension compression   
using (23)   
16 Obtain the attention core matrix using (24)   
17 Acquire the attention pooling matrix using (25)   
18 Compute the attention tensors using (26) and (27)   
19 Calculate the DT models using (28) and (29)

where $f _ { \mathrm { D T _ { R S } } }$ and $f _ { \mathrm { D T _ { P P } } }$ is two mapping function regards to the parameters of $ { \mathrm { D T } } _ { R S }$ and $\mathrm { D T } _ { P P }$ . Based on this, we can obtain our versatile DT model:

$$
\mathrm { D T } _ { \mathrm { R S } } = \sum _ { i } \mathrm { A t } _ { \mathrm { R S } } \mathrm { E n v } ^ { i } ,\tag{28}
$$

$$
\mathrm { D T } _ { P P } = \sum _ { i } \mathrm { A t _ { P P } E n v } ^ { i } .\tag{29}
$$

We give the detailed implementation process for model acquisition in Algorithm 1. We also prove our proposed algorithm can acquire accurate DT models for high-efficiency logistics distributions in the Appendix C.

## C. Resource Scheduling Twin Model Implementation

With the resource scheduling twin model $\mathrm { D T } _ { \mathrm { R S } }$ , we can instruct UAVs to plan distribution paths. To empower the DT model to play its superiority, we propose an ICC algorithm as mentioned in Section III. It can cope with the changes in physical distribution environments with rational resource scheduling strategies. The reason why environmental change is considered is that it has a significant impact on UAV communications. In this case, our algorithm can provide customized resource scheduling solutions for different distribution scenarios. We consider two distinguished distribution scenarios: an empty scenario and a disturbed scenario.

As shown in Fig. 6, when edge UAVs construct a virtual space to imitate and derive feasible logistics distribution solutions for an empty scenario, we can enable UAVs to implement a directional information diffusion operation towards the logistics destination. It is achieved using the beamforming technology [45]. The diffusion operation is implemented with the information of logistics mission l and UAV state $S _ { i }$ to invite feasible UAVs for cooperative distributions. Additionally, considering the priority of logistics, we give diffusion time Ïl t to ensure high-efficiency distribution cooperation:

<!-- image-->  
Fig. 6. Illustration of DT-based heterogeneous resource scheduling.

$$
v _ { l } ( t ) = \{ { v - \epsilon _ { 1 } ( t ) } , \qquad t _ { k } \mathrm { i s \ s h o r t } , \qquad \tag{30}
$$

where Ï is a given diffusion time; $\epsilon _ { 1 } ( t )$ and $\epsilon _ { 2 } ( t )$ are variables ( ) ( )which increase as time goes by. It is noted that the increased speed of $\epsilon _ { 1 } ( t )$ is lower than that of $\epsilon _ { 2 } ( t )$ . It can provide more time to explore feasible cooperators for time-sensitive logistics missions.

On the other hand, when edge UAVs build a virtual space to imitate and derive reasonable distribution solutions for a disturbed scenario, we cannot directly use the beamforming technology to implement information transmission due to severe communication declines. In this case, our algorithm can efficiently integrate the computing resources of one-hop neighbors to implement cooperative computing for obtaining optimal cooperators based on a Multi-agent Deep Determined Policy Gradient (MA-DDPG) architecture. The architecture includes a critic module and an actor module. Each module supports a policy network and an estimation network. UAVs can learn feasible resource scheduling actions based on the local information $S _ { i } .$ . All the actions $A = \{ A _ { 1 } , \dotsc , A _ { M } \}$ of all the UAVs =are estimated centrally. The policy network trains the data for each UAV based on constructed state space $S _ { i }$ . The resource scheduling action from action space $A _ { i }$ is obtained with the aid of actions of other UAVs. The estimation network evaluates the resource scheduling performance using an estimation function. The training process is quantified as a Stochastic Game (SG) problem with a tuple $\{ S _ { i } , A _ { i } , \mathcal { T } , R _ { i } \}$ , where $\tau$ is a transfer function which can represent a transfer process from the current state to the next state based on Markov process; $R _ { i }$ is a reward function to estimate the action. We can design a state space and an action space where UAVs can select feasible resource scheduling actions from the action space based on the current states acquired from the state space. The state space $S _ { i }$ of UAV i is divided into four parts:

1) States of UAV i: $s _ { i } = \{ a _ { i } , v _ { i } , p _ { i } , \varrho _ { i } , \{ D _ { i , j } \} \}$ , where $a _ { i } .$ $v _ { i } .$ , and $p _ { i }$ =are position, velocity, and posture of UAV i; $\varrho _ { i }$ is the height of UAV $i ; \{ D _ { i , j } \}$ is the set of physical distances between UAV i and neighbor $j .$

2) States of one-hop neighbors: $o _ { i } = \{ a _ { j } , v _ { j } , p _ { j } , \varrho _ { j } , \}$ , where $a _ { j } , v _ { j } .$ , and $p _ { j }$ =are position, velocity, and posture of UAV j; $\varrho _ { j }$ is the height of UAV j;.

3) States of logistics mission k: $a _ { i , k }$ , where $a _ { i , k }$ is the association relation between UAV i and mission k.

4) Environmental states: $l _ { i } = \{ G _ { t } , B _ { t } \}$ , where $G _ { t }$ and $B _ { t }$ are =noise and terrain information.

The action space is $A _ { i } = \{ f _ { e , e } , f _ { e , d } , \mathcal { F } , B , \mathcal { R } \}$ . The explana-=tions of the indicators can be found in (1). UAV i can enable an actor-network with the parameter $\theta _ { i , a }$ to implement local training with local information $S _ { i }$ to acquire a UAV selection decision. Meanwhile, UAV i can combine all the decisions of neighbors and self-decisions to update parameters:

$$
\theta _ { i , a } ^ { \prime } = ( 1 - \lambda _ { j } ) \theta _ { i , a } + \lambda _ { j } \sum _ { j = 1 , j \neq i } ^ { N _ { i } } \theta _ { j , a } ,\tag{31}
$$

where $\theta _ { j , a }$ is the actor network parameter of UAV $j ; \lambda _ { j }$ is an update coefficient that is generally assigned a relatively small value.

The updated $\theta _ { i , a } ^ { \prime }$ is input to a critic network with parameter $\theta _ { i , \mu }$ to implement decision estimation based on the neighbor status. The estimation result is given to the actor-network to implement further learning for feasible UAV selection. It is noted that the two networks use the stochastic gradient descent method to acquire training gradient values $\nabla J ( \theta _ { i , a } )$ and $\nabla J ( \theta _ { i , \mu } )$ . To ( ) ( )ensure a satisfied learning performance, we design a reward function $R _ { i }$ to conduct UAVs to explore feasible directions based on an energy equilibrium method [46]:

$$
R _ { i } = r _ { i } + \frac { \alpha _ { E } } { E _ { j } } \sum _ { j } \operatorname* { m a x } \left( r _ { j } - r _ { i } , 0 \right) + \frac { \beta _ { E } } { E _ { j } } \sum _ { j } \operatorname* { m a x } \left( r _ { i } - r _ { j } , 0 \right) ,\tag{32}
$$

where $\begin{array} { r } { r _ { i } = \sum _ { j = 1 } ^ { N _ { i } } [ \Delta B _ { j } + \Delta F _ { j } ] ; \Delta B _ { j } } \end{array}$ and $\Delta F _ { j }$ denote avail-= [Î + Î ] Î Îable resources of bandwidth and CPU of UAV j, respectively. $\alpha _ { E }$ and $\beta _ { E }$ are energy parameters that are set as 5 and 0.05, respectively. In this case, UAVs can obtain suitable distribution path decisions in a cooperative computing manner.

Based on this, we can use our ICC algorithm to implement a considerable amount of offline training for acquiring resource scheduling twin models of different logistics distribution scenarios according to the various numbers of UAVs and distribution missions. We can select the optimal resource scheduling twin model for real-time distribution services to serve a specific distribution scenario. In addition, our ICC algorithm can enable the resource scheduling twin model to implement flexible resource scheduling of computing and communication. It can assist UAVs in selecting optimal neighbors in dynamic physical environments for cooperative logistic distribution with a high successful distribution ratio. We also give the relevant proofs for efficient resource scheduling and neighbor selections in the Appendix D and Appendix E.

## D. Path Planning Twin Model Implementation

Based on our ICC algorithm, we can implement cooperative logistics distributions. However, UAVs may cause potential physical collisions due to improper path decisions. In this case, we propose a Particle Swarm Optimization (PSO)-based path planning algorithm in the virtual space. The path planning twin model DTPP can use the algorithm to instruct UAVs to dynamically adjust distribution paths by associating different cooperators for collision avoidance in advance. Different from the existing PSO algorithm, ours can enable UAVs to implement path exploration considering multiple dimensions (velocity and position). In addition, UAVs can narrow exploration spaces for low-latency exploration. It can efficiently reduce the computing time for low-latency distribution path decisions. As shown in Fig. 7, we first set the maximal number of iterations, the maximal UAV speed, the initial velocity, and the initial position. UAVs are regarded as particles to implement cooperative explorations based on our formulated fitness function:

<!-- image-->  
Fig. 7. Illustration of PSO-based path planning.

$$
\begin{array} { c } { f _ { \mathrm { U A V } } = \displaystyle \operatorname* { m i n } _ { \mathcal { L } } \sum _ { i } ^ { M } \sum _ { l = 1 } ^ { L } t _ { i , l } , } \\ { \displaystyle \left( x _ { i } ( t ) , y _ { i } ( t ) , z _ { i } ( t ) \right) \neq \left( x _ { j } ( t ) , y _ { j } ( t ) , z _ { j } ( t ) \right) \forall j \neq i , } \end{array}\tag{33}
$$

where $t _ { i , l }$ is the time for logistic mission l by UAV i; $( x _ { i } ( t ) , y _ { i } ( t ) , z _ { i } ( t ) )$ is the three-dimensional coordinate of UAV ( ( ) ( ) ( ))i at time t. With the fitness function, UAV i implements updates of velocity and position to meet the function requirements. The update strategy is optimized with an asynchronous update manner to avoid local optimum. We add two probability factors, 1 and 2, to determine if the current velocity is updated Pr Prwith both the individual optimum and global optimum. When $\mathrm { P r } _ { 1 } , \mathrm { P r } _ { 2 } \ge 0 . 5$ , the velocity is updated as

$$
h _ { i } = \tau h _ { i } + c _ { 1 } \varpi _ { 1 } ( P _ { b , i } - x _ { i } ) + c _ { 2 } \varpi _ { 2 } ( G _ { b } - x _ { i } ) ,\tag{34}
$$

where $P _ { b , i }$ and $G _ { b }$ are the individual optimum and global optimum, respectively; Ï is an inertial parameter; c1 and $c _ { 2 }$ are random numbers under $[ 0 , 1 ] ; \varpi _ { 1 }$ and -2 are learning parameters, respectively. When the $\operatorname* { P r } _ { 1 } \geq 0 . 5 , \operatorname* { P r } _ { 2 } \leq 0 . 5$ , we update Pr 0 5 Pr 0 5the velocity with the individual optimum. Otherwise, we only update the velocity with the global optimum. The position is updated by

$$
x _ { i } ^ { \prime } = x _ { i } + v _ { i } .\tag{35}
$$

We can implement finite iterations to acquire the feasible paths of logistics distributions for all the UAVs. In this case, UAVs can always select suitable cooperators with the consideration of collision avoidance. The details with UAV selection are shown in Algorithm 2.

Based on the above descriptions, the RST model can derivate to acquire feasible resource scheduling decisions using our proposed ICC algorithm. It can significantly reduce UAVsâ communication overheads and computing latency for high-efficiency UAV cooperation. The PPT model can use the resource scheduling derivation results to dynamically plan feasible distribution paths of UAVs using our proposed PSO-PP algorithm with low energy consumption. In return, the feasible path planning decisions can improve resource utilization by selecting feasible neighbors. The positive interplay allows our VerDT framework to assist UAV systems in implementing real-time logistics distribution services with a high successful distribution ratio. We also provide the detailed analysis for algorithm complexity in the Appendix B.

Algorithm 2: Cooperative Logistics Distribution.   
Input: Available CPU resource of UAVs; diffusion   
time variables:MA-DDPG network   
parameters; UAV state information.   
Output: The cooperative distribution path decision.   
1 Edge UAVs estimate the logistics scenario   
2 if empty scenario is true then   
3 Construct the corresponding virtual space   
4 Implement directional data diffusion using (30)   
5 Explore to invite feasible cooperators   
6 if disturbed scenario is true then   
7 Construct the corresponding virtual space   
8 Build the MA-DDPG architecture for each   
iteration do   
9 Feed the state information to the actor network   
10 Acquire a UAV selection decision with   
$\nabla J ( \theta _ { i , a } )$   
11 Update the actor network parameters   
using (31)   
12 Estimate the actor using (32) in the critic   
network   
13 Compute the estimation result with $\nabla J ( \theta _ { i , \mu } )$   
14 Update the critic network parameter $\theta _ { i , \mu }$   
15 Obtain UAV selection decisions   
16 Formulate the fitness function using (33)   
17 for each iteration do   
18 Update UAV velocities using (34)   
19 Update UAV positions using (35) based on the   
UAV selection decisions   
20 Acquire feasible distribution path decisions

## VI. PERFORMANCE EVALUATION

In this section, we present the performance evaluation with several system metrics through a system simulation.

## A. Preliminary

Explicitly, we first implement data collection. The status information of UAVs is acquired in a practical scenario shown in Fig. 8. We deploy the DJI FlyCart-30 UAV to implement a given logistics distribution mission. The relevant information, including flight velocities, positions, postures, mobile trajectories, and change in energy, can be obtained using onboard sensors and energy detector. In addition, for the physical environment information, we use wind speed sensors to measure the changes in winds which is used to analyze the impact on UAV mobility. The building information is acquired using onboard depth vision sensors.

<!-- image-->  
Fig. 8. Illustration of UAV data collection.

<!-- image-->  
Fig. 9. Illustration of logistics imitation in the Gazebo.

Based on the above information, we construct a virtual logistic space using the Gazebo, a system simulation software. It can imitate the UAV mobility based on the current physical scenario. We can enable UAVs to cooperatively implement logistic distribution missions using our proposed algorithms through the Robot Operation System (ROS) interface. The DT imitation process is shown in Fig. 9. We deploy multiple UAVs randomly to implement 10 logistics distribution missions (represented by spheres and cubes) which are deployed in three different logistics warehouses. The buildings (represented by green boxes) are randomly constructed to design a challenging logistics distribution scenario. The distribution destination is in the lower right corner in Fig. 9.

TABLE II SIMULATION PARAMETERS
<table><tr><td>Parameter description</td><td>Value</td></tr><tr><td>Number of logistics UAVs</td><td>[20,40]</td></tr><tr><td>Number of logistics missions</td><td>[10,30]</td></tr><tr><td>Average moving velocity of the UAVs</td><td>72 km/h</td></tr><tr><td>Average scalar distance of logistics distributions</td><td>50km</td></tr><tr><td>Average carrying capability of UAVs</td><td>[15,20] kg</td></tr><tr><td>Pitch angle of the UAVs</td><td>[-130Â°,+40Â°]</td></tr><tr><td>Angular-rate of horizontal rotation</td><td>[-100Â°,+100Â°]</td></tr><tr><td>Learning rate</td><td>[0.001,0.009]</td></tr><tr><td>Diffusion time U</td><td>300 milliseconds</td></tr><tr><td>Minimal safe flight distance of the UAVs</td><td>3m</td></tr><tr><td>Average sensing rate of the UAVs</td><td>1 MByte/s</td></tr><tr><td>Horizontal sensing distance of the UAVs</td><td>[0 m,30 m]</td></tr><tr><td>Gaussian White Noise</td><td>-96 dBm/Hz</td></tr><tr><td>The acceptable maximal implementation latency The acceptable minimal successful distribution ratio</td><td>5 minutes</td></tr></table>

To ensure efficient distribution implementation, we use UAV image dataset to train the GAN network training to enrich physical information for constructing an accurate DT imitation scenario. We use DJI UAVs with Manifold computers as edge UAVs to implement DT imitation. The information of UAVs is used to construct $\mathrm { D T _ { R S } }$ for efficient resource scheduling. The information of logistics missions, environments, and UAVs is utilized to build $\mathrm { D T _ { P P } }$ for feasible distribution path planning. In addition, we can change numbers of UAVs and logistics missions to further evaluate the effectiveness of our proposed algorithms based on the UAV logistics distribution dataset. The main simulation parameters are summarized in Table II.

We use several metrics to evaluate the performance of our proposed VerDT-based cooperative distribution solution:

1) Effectiveness of data generation: We can use the Frechet Inception Distance (FID) metric [47] to evaluate the GAN network training performance for efficient data acquisition and DT constructions. The FID is formulated to capture the similarity between the real data $d _ { R }$ and generated data $d _ { G }$ based on the inception score [48]:

$$
\mathrm { F I D } = \Vert m _ { R } - m _ { G } \Vert _ { 2 } ^ { 2 } + t r a \left( c _ { R } + c _ { G } - 2 \sqrt { c _ { R } c _ { G } } \right) ,\tag{)(36}
$$

where $\{ m _ { R } , m _ { G } \}$ and $\{ c _ { R } , c _ { G } \}$ are mean values and covariance values of samples with distribution $d _ { R }$ and $d _ { G }$ respectively.

2) System communication overhead: It is used to estimate the communication data size and latency during distribution process based on (15).

3) System computing latency: This metric mainly reflects the performance of DT construction for real-time model acquisitions.

4) System energy consumption: It is used to evaluate the effectiveness of cooperative path planning with energy saving.

5) System latency overhead: This metric includes latencies of sensing, communication, DT implementation, and decision-making. It is used to perform the real time of system implementation.

<!-- image-->  
Fig. 10. Performance of content generation.

6) Successful distribution ratio: It can evaluate the accuracy of mission implementation. It is formulated as $\begin{array} { r } { \eta = \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \frac { \sum _ { i = 1 } ^ { M } \sum _ { k = 1 } ^ { K } m _ { k } } { M K } } \end{array}$ , where $m _ { k } \in$ { , }; $m _ { k } = 1$ denotes that UAV m implements delivery 0 1 = 1mission k to a given destination successfully, otherwise $m _ { k } = 0$

= 0We use four typical benchmarks for comparison:

1) Centralized DT framework [15]: The DT is implemented in the edge side without the involvement of terminal UAVs.

2) Distributed DT framework [16]: Terminal UAVs implement a cooperative DT imitation operation with an information exchange manner.

3) On demand-based logistics distribution foresting method [23]: It leverages a two-stage prediction optimization strategy to implement cooperative distributions based on the LSTM algorithm.

4) Three-stage path planning method [25]: It first uses a statistical method to implement distribution analysis. Then a machine learning algorithm is training to empower an explainable learning technique to explore feasible distribution paths for real-time distributions.

5) Cloud-based logistics distributions method [24]: The method leverages powerful computing resource of the cloud server to implement cooperative logistics distributions with a high successful distribution ratio.

6) Predict-Then-Optimize based Couriers Allocation (PTOCA) method [26]: It provides a high-efficiency logistics distribution solution with path prediction and allocation optimization based on the GRU network and distribution priority analysis.

## B. Evaluation of Data Generation

To enrich the physical information, we use the GAN network to implement data generation for accurate DT model construction. Figs. 10 and 11 give the performance of data generation (contents and images, respectively). It is noted that the lower FID value corresponds to the higher similarity between $d _ { R }$ and $d _ { G }$ . We can see that all the data generation results decrease gradually as the number of iterations increases. It implies that we can generate desired contents (such as physical distances among UAVs) and images (UAVs obscured by buildings) to construct accurate virtual logistics space. On the other hand, we can see that the FID scores are related to the data size. We can increase data size to improve the performance of data generation.

<!-- image-->  
Fig. 11. Performance of image generation.

<!-- image-->  
Fig. 12. System latency vs. number of missions.

However, the convergence rate may be fluctuating with different sizes of data. We can select the optimal data size with a fast convergence rate and a low FID score for the data generation.

We use the rich data to construct accurate DT models for precious scenario imitation and derivation. A resource scheduling twin model can collaborate communication and computing resources of UAVs to implement cooperative logistics distributions with information exchanges among UAVs for meeting low-latency distribution requirements. In addition, the DT model can dynamically optimize resource scheduling decisions for real-time distributions by imitating changes in distribution scenarios, such as the change in the number of distribution missions. With the flexible resource scheduling performance, we can enable a path planning twin model to adjust the distribution paths of UAVs to shorten physical distribution distances for energy saving. In this context, we must generate high-quality data to support accurate DT implementation for real-time, low-energy, and robust logistics distributions.

## C. Evaluation of VerDT Framework

We evaluate the performance of our VerDT framework from perspectives of system latency, computing energy consumption, and energy consumption on communications. Given 20 UAVs with an average speed of 72 km/h, Fig. 12 shows the performance of system latency. Our framework can ensure low-latency DT implementation and logistics distributions in a terminal-edge cooperative manner. Based on this, we can enable terminal UAVs to enrich the training data for highly accurate DT model constructions with a GAN network. We can further guarantee accurate DT construction by jointly analyzing resource scheduling and path planning with two kinds of DT models. The resource scheduling twin model can improve resource utilization based on the environment estimation for cooperative logistics distribution with feasible neighbor selection. The path planning twin model can use the selection results to explore optimal distribution paths for real-time logistics distributions. In this case, our VerDT reduces the system latency by 44.4% and 50.0% compared to the centralized DT and distributed DT frameworks, respectively.

<!-- image-->  
Fig. 13. Consum. on comm. & comput. energy consum. vs. number of missions.

<!-- image-->  
Fig. 14. Position changes and error estimation over times.

Fig. 13 shows the performance of energy consumption on computing and communications with the same deployment as Fig. 12 (blue line for computing energy consumption and red line for energy consumption on communications). In terms of computing energy consumption, we find that the energy consumption increases as the number of missions increases for all the DT frameworks. However, our VerDT can maintain the lowest computing consumption with the slowest growth slope. It is because our framework can enable UAVs to invite feasible numbers of neighbors to implement cooperative exploration for optimal distribution paths. It can reduce extra computing energy consumption in a collaborative computing manner. In this case, our VerDT reduces the computing energy consumption by 43.5% and 48.0% compared to the centralized DT and distributed DT frameworks, respectively. In addition, we analyze the energy consumption on communications with the changes in the number of missions. Our framework can still perform the lowest energy consumption on communications. Our framework allows UAVs to implement information exchanges with feasible numbers of neighbors instead of all the neighbors. It can significantly reduce the energy consumption on communication with partial neighbors involved. Additionally, we implement a directional diffusion operation in our framework to reduce the frequency of information exchanges with enhanced communication quality. Our framework minimizes the energy consumption on communications by 10.5% and 32.0% compared to the centralized DT and distributed DT frameworks, respectively. Our framework can efficiently trade off resource scheduling and path planning performance to ensure real-time and accurate logistics distributions.

We also evaluate the path planning performance of our VerDT. Fig. 14 gives the changes in UAV positions with the time change. Under a given distribution path, we can see that our VerDT can perform accurate logistics distributions with a low path planning error. Our VerDT enables the path planning twin model to implement a precise distribution path exploration with feasible resource scheduling decisions. It can conduct UAVs to dynamically schedule sensing and communication resources to estimate the changes in distribution environments. The estimation results can be used to conduct UAVs to select feasible neighbors for cooperative path planning. In addition, our VerDT can achieve smooth distribution cooperation with suitable UAV allocations in advance through cooperative computing among edge UAVs for a low path planning error. Compared to the centralized DT framework, our VerDT can reduce the path planning error by 71.3% on average. With accurate path planning, we provide the analysis of the change in UAV speeds in Fig. 15. Our VerDT can guarantee smooth logistics distributions with almost uniform moving speeds in the time-varying distribution scenario. It is because our VerDT can perform accurate environment imitations to derive feasible speed optimization decisions based on abundant training data using our data generation algorithm. Our VerDT can enable UAVs to maintain smooth flight at a uniform speed in empty distribution scenarios. For disturbed distribution scenarios, our VerDT can conduct UAVs to adjust flight speeds and directions in advance to ensure smooth logistics distributions through environment imitations. In addition, the uniform moving speed can effectively reduce the UAV energy consumption [49]. Consequently, our solution ensures more effective logistics distributions in practical time-varying scenarios.

<!-- image-->  
Fig. 15. Changes in speeds over times.

<!-- image-->  
Fig. 16. Consum. on comm. vs. number of UAVs.

## D. Evaluation of System Communication and Computing

With the resource scheduling twin model $\mathrm { D T _ { R S } }$ , we provide the comparison of energy consumption on communication with different numbers of UAVs and missions. Given 20 logistics distribution missions, Fig. 16 shows the comparison under different numbers of UAVs with an average speed of 72 km/h. We can find that the energy consumption on communication increases as the number of UAVs increases for all the solutions. However, our solution with $\mathrm { D T } _ { \mathrm { R S } }$ can alleviate the increasing rate by selecting feasible cooperators based on our proposed direct information diffusion method. In addition, our solution can efficiently use sensing and computing resources to acquire status of neighbors for cooperative logistics distributions. It can significantly reduce the frequency of information exchanges among neighbors for saving energy consumption on communication. In this case, our solution can reduce the energy consumption on communication by 52.78%, 56.41%, and 58.54% on average compared to the state-of-the-art on-demand based, PTOCA, and cloud-based algorithms, respectively.

<!-- image-->  
Fig. 17. Consum. on Comm. vs. number of missions.

<!-- image-->  
Fig. 18. Data size vs. number of UAVs.

<!-- image-->  
Fig. 19. Data size vs. number of missions.

Additionally, our solution still performs well in a dynamic logistics scenario with variable numbers of missions shown in Fig. 17. Under the given 20 UAVs with an average speed of 72 km/h, we can draw that our solution saves significant energy consumption on communication based on the conduction of $\mathrm { D T } _ { \mathrm { R S } } .$ . It can instruct UAVs to implement lightweight information exchanges with model parameters for low energy consumption on communication. In addition, The lightweight information is shared with partial neighbors instead of all the neighbors. In this point, our solution can further reduce the energy consumption on communication by 18.3%, 21.9%, and 32.7% compared to the on-demand based, PTOCA, and cloudbased algorithms, respectively.

We also provide the comparison of data size during information exchanges with different numbers of UAVs and logistics missions shown in Figs. 18 and 19. Based on the same deployment as that of Fig. 16, we can see that our solution can reduce extra communication data size compared to all the benchmarks in Fig. 18. This is because our solution can conduct UAVs to transmit lightweight model parameters instead of raw physical information for high-efficiency distribution cooperation. In this case, our solution reduces the data size by 46.6%, 49.3%, and 51.9% compared to the PTOCA, on-demand based, and cloud-based algorithms, respectively. On the other hand, with the same deployment as that of Fig. 17, we can still keep a low communication data size for real-time distribution cooperation in the dynamic logistic scenario with variable missions in Fig. 19. It implies that our DT model $\mathrm { D T } _ { \mathrm { R S } }$ can instruct UAVs to autonomously associate feasible logistics missions without frequent information exchanges. The PTOCA algorithm performs the best result in all the benchmarks. However, it increases more data size compared to ours with frequent requests among UAVs for efficient path prediction. Our solution decreases the data size by 37.4%, 44.8%, 47.4% compared to the PTOCA, on-demand based, and cloud-based algorithms, respectively.

<!-- image-->  
Fig. 20. Computing latency vs. number of UAVs.

<!-- image-->  
Fig. 21. Computing latency vs. number of missions.

Expect for the communication overhead, we also give the comparison of computing latency with different numbers of UAVs and missions in Figs. 20 and 21. With the same number of missions as that of Fig. 16, we can see that the computing latency of our solution is the lowest than all the benchmarks. This is because our DT model $\mathrm { D T _ { R S } }$ can assist UAVs in requesting available computing resources from neighbors for cooperative computing. Furthermore, our solution can implement DT model exchanges which can directly instruct UAVs to perform real-time logistics distributions without the help of computing resources. The resource cooperation of computing and communication reduces the computing latency by 43.5%, 58.1%, 66.7%, 77.2% compared to the cloud-based, PTOCA, on-demand based, and three-stage algorithms, respectively. On the other hand, our solution can still perform a low computing latency with a variable number of logistics missions shown in Fig. 21. It implies that our solution can always assist UAVs in exploring feasible computing resources of neighbors. Moreover, it means that UAVs can acquire accurate distribution results without extra computing resources for decision optimization. In this context, ours can improve the computing efficiency by 25.6%, 51.7%, 60.8%, and 75.4% compared to the cloud-based, PTOCA, on-demand based, and three-stage algorithms, respectively.

## E. Evaluation of System Energy Consumption

We provide the comparison of energy consumption with different numbers of UAVs, logistics missions, and moving speeds of UAVs. Explicitly, Fig. 22 showcases the change in energy consumption. Although energy consumption of all the solutions can increase as the number of UAVs increases, our solution performs the lowest energy consumption based on the high-efficiency conduction of DT model $\mathrm { D T _ { P P } }$ . It can improve the probability of selecting feasible cooperators to assist UAVs in acquiring optimal path planning decisions. In addition, DTRS can provide the decision of resource scheduling to $\mathrm { D T _ { P P } }$ . The results can enable $\mathrm { D T _ { P P } }$ to optimize distribution paths of UAVs with operations of environment estimation and information exchanges. Ours reduces the energy consumption by 26.8% on average compared to the best three-stage benchmark. On the other hand, when the number of UAVs is determined, our solution can still ensure the low energy consumption with the change in number of distribution missions shown in Fig. 23. With the aid of the $\mathrm { D T _ { P P } }$ , UAVs can fly to feasible airspace to implement cooperative distributions based on considerations of positions and speeds of neighbors. Moreover, the $\mathrm { D T } _ { \mathrm { R S } }$ model can invite remote UAVs to fly to assigned spatial positions for smooth distribution cooperation with optimized flight paths. The bidirectional cooperation makes UAVs to shorten flight paths for real-time logistics distribution with low energy consumption. In this case, our solution improve the energy efficiency by 8.7%, 20.7%, 33.8%, and 39.1% compared to the three-stage, the PTOCA, the cloud-based, and on-demand based algorithms, respectively.

<!-- image-->  
Fig. 22. Energy consumption vs. number of UAVs.

<!-- image-->  
Fig. 23. Energy consumption vs. number of missions.

<!-- image-->  
Fig. 24. Energy consumption vs. speeds of UAVs.

With the given 30 UAVs and 20 distribution missions, we also showcase the comparison of energy consumption under different flight speeds shown in Fig. 24. It is a fact that high-speed moving UAVs need the support of high powers. The energy consumption of UAVs can then increase as the speeds of UAVs increase. However, our solution can alleviate the significant energy consumption with efficient path planning decisions. This is because our DT model $\mathrm { D T _ { P P } }$ can allocate feasible UAVs to implement continued distributions by flying to feasible airspace based on environment estimation. In this case, our solution can further reduce the energy consumption by 27.2%, 39.6%, 44.7%, and 48.4% compared to the three-stage, the PTOCA, the cloud-based, and on-demand based algorithms, respectively.

<!-- image-->  
Fig. 25. System latency vs. number of UAVs.

<!-- image-->  
Fig. 26. System latency vs. number of missions.

## F. Evaluation of System Implementation Latency

Based on our design distribution scenario using the Gazebo, we evaluate the system implementation latency, including environment sensing time, resource collaboration time, and distribution time, from different perspectives. With the same deployment as that of Fig. 16, we showcase the comparison of energy consumption with different numbers of UAVs in Fig. 25. We can see that the system latency can decrease as the number of UAVs increases. This is because all the algorithm can make it easier to find feasible UAVs to implement cooperative distributions. Among them, our solution can further shorten the distribution time by imitating positions and speeds of UAVs in real time. The imitation results can assist UAVs in accurately finding feasible cooperators using our proposed PSO-based path planning algorithm. Nonetheless, the system latency can increase when UAVs face overloaded distribution missions shown in Fig. 26. With the same number of UAVs as that of Fig. 17, we can find our solution can efficiently cope with the overloaded distribution missions as the number of missions increases with a mild uptrend. It implies that our DT models can derive the flight trajectories of UAVs to select feasible numbers of UAVs for the optimal path planning. In this case, our solution can reduce the system latency by 67.2%, 68.3%, 73.6%, and 74.7% compared to the cloud-based, on-demand, PTOCA, and three-stage algorithms, respectively.

<!-- image-->  
Fig. 27. System latency vs. speeds of UAVs.

<!-- image-->  
Fig. 28. Successful distribution ratio vs. number of UAVs.

In addition, we provide the comparison of system latency with different speeds of UAVs in Fig. 27. It is obvious to shorten the distribution time by improving the flight speeds of UAVs. However, it is difficult to ensure a low-latency distribution decision due to high-speed moving UAVs. Under the given 30 UAVs and 20 distribution missions, our solution performs the lowest distribution latency compared to all the benchmarks. This is because our versatile DT models can perform an accurate derivation capability for planning feasible distribution paths with high-efficiency resource cooperation of computing and communication. Compared to the cloud-based, on-demand, PTOCA, and three-stage algorithms, our solution can improve the distribution time efficiency by 63.9%, 67.2%, 68.1%, and 70.6%, respectively.

## G. Evaluation of Successful Distribution Ratio

In addition to the analysis of system latency, we also give the comparison of successful distribution ratio Î· with different numbers of UAVs and distribution missions. Based on the same deployment as that of Fig. 17, Fig. 28 showcases the comparison under different numbers of UAVs. with the given 20 distribution missions, we can discover that our solution can always achieve up to 90% successful distribution ratio. In other words, we can always accurately implement more than 18 distribution missions using our solution. The high distribution ratio performance is due to accurate path planning decisions with the aid of our versatile DT models. It can allocate UAVs to suitable airspace in advance for smooth distribution cooperation by accurately deriving trajectories of UAVs. In this case, our solution can improve the successful distribution ratio by 10.6%, 14.6%, 20.5%, and 25.3% compared to the PTOCA, three-stage, cloud-based, and on-demand algorithms, respectively.

On the other hand, we showcase the comparison of successful distribution ratio with different number of missions in Fig. 29. We can see that our solution can still perform a high distribution ratio when facing the overloaded missions. This is because our solution can dynamically adjust flight trajectories of UAVs to implement different distribution missions. It is verified that this way is efficient to maximize the distribution requirements. For the four benchmarks, the PTOCA algorithm performs the highest distribution ratio using a method of joint prediction and optimization. However, the method cannot ensure a robust mission implementation in an overloaded situation due to the limited prediction ability of the GRU network. In this context, our solution can further improve the successful distribution ratio by 10.9%, 16.9%, 33.8%, and 35.7% compared to the PTOCA, three-stage, cloud-based, and on-demand algorithms, respectively.

<!-- image-->  
Fig. 29. Successful distribution ratio vs. number of missions.

## H. Performance Discussion

We evaluate our VerDT solution from multiple perspectives based on our designed logistic distribution scenario with different numbers of UAVs and various distribution missions. We discuss our VerDT based on the given metrics.

Explicitly, Unlike the on-demand logistics distribution algorithm with the LSTM scheme, our VerDT can significantly reduce the energy consumption on communication. Our VerDT performs high-efficiency scenario derivation based on joint trajectory derivation and topology control estimations. It can reduce the frequency of information exchanges among UAVs with low communication consumption. In addition, our VerDT can further reduce communication data sizes compared to the cloud-based distribution algorithm with lightweight DT model parameters instead of raw data. With the apparent advantages of low communication overhead, our VerDT can still perform highly cooperative logistics distributions for overloaded distribution missions.

Our VerDT performs well for real-time logistics distributions with low computing latency compared to the PTOCA algorithm. The PTOCA algorithm must frequently implement data training for time-varying distribution scenarios based on the GRU network. Our VerDT accelerates the DT imitation process by flexibly collaborating computing and communication resources for low DT implementation time. Additionally, UAVs can use communication resources to implement cooperative DT imitation for real-time logistics distributions. The heterogeneous resource collaboration can also assist UAVs in reducing energy consumption by exploring feasible distribution paths cooperatively. By contrast, the three-stage path planning method only uses a machine learning scheme to acquire distribution paths. It might experience a performance decline due to excessive reliance on data sets. In this case, our VerDT can enable UAVs to dynamically adjust distribution paths to implement different distribution missions cooperatively for real-time logistics distributions with a high successful distribution ratio.

## VII. CONCLUSION

We have propose a versatile DT framework to empower UAVs to implement real-time logistics distributions with a high successful distribution ratio. Based on our framework, edge UAVs can train a resource scheduling twin model to implement the integration of computing and communication of UAVs for accurate logistics distributions by enhancing UAV cooperation. With the UAV cooperation decisions, edge UAVs can then acquire a path planning twin model to derive feasible UAV paths for real-time logistics distributions with low energy consumption. The experiment results demonstrate that our versatile DT framework can assist UAVs with the optimization of distribution paths for low-energy logistics distributions compared to the state-of-the-art distribution solutions. Additionally, our solution can still perform high successful distribution ratios in complicated distribution scenarios with variable numbers of UAVs and distribution missions.

## REFERENCES

[1] X. Wang et al., âA paradigm shift for modeling and operation of oil and gas: From industry 4.0 in CPS to industry 5.0 in CPSS,â IEEE Trans. Ind. Inform., vol. 20, no. 7, pp. 9186â9193, Jul. 2024.

[2] W. Xiang, K. Yu, F. Han, L. Fang, and D. He, âAdvanced manufacturing in industry 5.0: A survey of key enabling technologies and future trends,â IEEE Trans. Ind. Inform., vol. 20, no. 2, pp. 1055â1068, Feb. 2024.

[3] L. Chen, J. Xie, X. Zhang, J. Deng, S. Ge, and F.-Y. Wang, âMining 5.0: Concept and framework for intelligent mining systems in CPSS,â IEEE Trans. Intell. Veh., vol. 8, no. 6, pp. 3533â3536, Jun. 2023.

[4] P. Maurya, V. M. R. Tummala, A. Hazra, and S. P. Mohanty, âAdvancing industry 5.0 with UAV-driven transformations: Future prospectives,â IEEE Consum. Electron. Mag., vol. 13, no. 5, pp. 30â35, Sep. 2024.

[5] D. K. Jain, Y. Li, M. J. Er, Q. Xin, D. Gupta, and K. Shankar, âEnabling unmanned aerial vehicle borne secure communication with classification framework for industry 5.0,â IEEE Trans. Ind. Inform., vol. 18, no. 8, pp. 5477â5484, Aug. 2022.

[6] H. Huang, C. Hu, J. Zhu, and M. Wu, âStochastic task scheduling in UAVbased intelligent on-demand meal delivery system,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 13040â13054, Aug. 2022.

[7] J. Jin, K. Yu, J. Kua, N. Zhang, and Z. Pang, âCloud-fog automation: Vision, enabling technologies, and future research directions,â IEEE Trans. Ind. Inform., vol. 20, no. 2, pp. 1039â1054, Feb. 2024.

[8] R. Yu et al., âCooperative resource management in cloud-enabled vehicular networks,â IEEE Trans. Ind. Electron., vol. 62, no. 12, pp. 7938â7951, Dec. 2015.

[9] Y. Ma et al., âSmart actuation for end-edge industrial control systems,â IEEE Trans. Autom. Sci. Eng., vol. 21, no. 1, pp. 269â283, Jan. 2024.

[10] L. Ma, X. Wang, X. Wang, L. Wang, Y. Shi, and M. Huang, âTCDA: Truthful combinatorial double auctions for mobile edge computing in industrial Internet of Things,â IEEE Trans. Mob. Comput., vol. 21, no. 11, pp. 4125â4138, Nov. 2022.

[11] Z. Li, Z. Chen, X. Wei, S. Gao, C. Ren, and T. Q. Quek, âHPFL-CN: Communication-efficient hierarchical personalized federated edge learning via complex network feature clustering,â in Proc. 19th Annu. IEEE Int. Conf. Sens. Commun. Netw., 2022, pp. 325â333.

[12] T. Li, S. Leng, Z. Wang, K. Zhang, and L. Zhou, âIntelligent resource allocation schemes for UAV-swarm-based cooperative sensing,â IEEE Internet Things J., vol. 9, no. 21, pp. 21570â21582, Nov. 2022.

[13] Z. Li et al., âExploiting complex network-based clustering for personalization-enhanced hierarchical federated edge learning,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 14852â14870, Dec. 2024.

[14] W. Chen et al., âMADDOG algorithm for coordinated welding of multiple robots,â in Proc. 6th Int. Conf. Automat. Control Robot. Eng., 2021, pp. 1â5.

[15] S. GeiÃler, F. Wamser, W. Bauer, S. Gebert, S. Kounev, and T. HoÃfeld, âMVNOCoreSim: A digital twin for virtualized iot-centric mobile core networks,â IEEE Internet Things J., vol. 10, no. 15, pp. 13974â13987, Aug. 2023.

[16] Z. Chen, W. Yi, A. Nallanathan, and J. A. Chambers, âDistributed digital twin migration in multi-tier computing systems,â IEEE J. Sel. Top. Signal Process., vol. 18, no. 1, pp. 109â123, Jan. 2024.

[17] C. Xu, Z. Tang, H. Yu, P. Zeng, and L. Kong, âDigital twin-driven collaborative scheduling for heterogeneous task and edge-end resource via multi-agent deep reinforcement learning,â IEEE J. Sel. Areas Commun., vol. 41, no. 10, pp. 3056â3069, Oct. 2023.

[18] X. Huang, W. Wu, S. Hu, M. Li, C. Zhou, and X. Shen, âDigital twin based user-centric resource management for multicast short video streaming,â IEEE J. Sel. Top. Signal Process., vol. 18, no. 1, pp. 50â65, Jan. 2024.

[19] M. Maboudi, M. Homaei, S. Song, S. Malihi, M. Saadatseresht, and M. Gerke, âA review on viewpoints and path planning for UAV-based 3-D reconstruction,â IEEE J. Sel. Top. Appl. Earth Obs., vol. 16, pp. 5026â5048, 2023.

[20] X. Tang et al., âDigital-twin-assisted task assignment in multi-UAV systems: A deep reinforcement learning approach,â IEEE Internet Things J., vol. 10, no. 17, pp. 15362â15375, Sep. 2023.

[21] J. Li, R. Qin, C. Olaverri-Monreal, R. Prodan, and F.-Y. Wang, âLogistics 5.0: From intelligent networks to sustainable ecosystems,â IEEE Trans. Intell. Veh., vol. 8, no. 7, pp. 3771â3774, Jul. 2023.

[22] Z. Yang, R. Wang, D. Wu, H. Wang, H. Song, and X. Ma, âLocal trajectory privacy protection in 5G enabled industrial intelligent logistics,â IEEE Trans. Ind. Inform., vol. 18, no. 4, pp. 2868â2876, Apr. 2022.

[23] X. Yang, J. Meng, and Y. Liu, âResearch on the allocation of cargo space in pharmaceutical logistics center based on demand forecasting,â in Proc. 8th Int. Conf. Automat. Logistics, New York, NY, USA: Association for Computing Machinery, 2021, Art. no. 1â7.

[24] Q. Wang and X. Du, âDesign of logistics cloud platform based on blockchain,â in Proc. 4th Blockchain Internet Things Conf., New York, NY, USA: Association for Computing Machinery, 2022, p. 100â106.

[25] S. Hao, Y. Liu, Y. Wang, Y. Wang, and W. Zhe, âThree-stage root cause analysis for logistics time efficiency via explainable machine learning,â in Proc. 28th ACM SIGKDD Conf. Knowl. Discov. Data Mining, New York, NY, USA: Association for Computing Machinery, 2022, pp. 2987â2996.

[26] K. Xia, L. Lin, S. Wang, H. Wang, D. Zhang, and T. He, âA predict-thenoptimize couriers allocation framework for emergency last-mile logistics,â in Proc. 29th ACM SIGKDD Conf. Knowl. Discov. Data Mining, New York, NY, USA: Association for Computing Machinery, 2023, pp. 5237â5248.

[27] L. Sheng, Z. Xiaotian, Y. Liang, W. Yu, and W. Shengnan, âLarge scale logistics network simulation and its application in JD logistics,â in Proc. Winter Simul. Conf., 2024, pp. 1605â1616.

[28] F. Tao, F. Sui, and A. Liu, âDigital twin-driven product design framework,â Int. J. Prod. Res., vol. 57, no. 12, pp. 3935â3953, 2019.

[29] C. Yang, S. Lan, Z. Zhao, M. Zhang, W. Wu, and G. Q. Huang, âEdge-cloud blockchain and IoE-enabled quality management platform for perishable supply chain logistics,â IEEE Internet Things J., vol. 10, no. 4, pp. 3264â3275, Feb. 2023.

[30] D. Hanover, A. Loquercio, L. Bauersfeld, and A. Romero, âAutonomous drone racing: A survey,â IEEE Trans. Robot., vol. 40, pp. 3044â3067, 2024.

[31] X. Chen, Z. Feng, Z. Wei, F. Gao, and X. Yuan, âPerformance of joint sensing-communication cooperative sensing UAV network,â IEEE Trans. Veh. Tech., vol. 69, no. 12, pp. 15545â15556, Dec. 2020.

[32] C.-A. Cai, K.-Y. Kai, and W.-J. Liao, âA WLAN/WiFi-6E MIMO antenna design for handset devices,â in Proc. Int. Symp. Antennas Propag., 2021, pp. 1â2.

[33] C.-Y. Wang, S.-Y. Chu, Y.-C. Lin, Y.-W. Tsai, and C.-L. Tai, âQuantitative imaging of ultrasound backscattered signals with information entropy for bone microstructure characterization,â Sci. Rep., vol. 12, no. 1, 2022, Art. no. 414.

[34] A. Pradhan, S. K. Bisoy, and A. Das, âA survey on PSO based metaheuristic scheduling mechanism in cloud computing environment,â J. King Saud Univ., Comp. Info., vol. 34, no. 8, pp. 4888â4901, 2022.

[35] R. Dutt and A. Acharyya, âLow-complexity square-root unscented kalman filter design methodology,â Circuits Syst. Signal Process., vol. 42, no. 11, pp. 6900â6928, 2023.

[36] J. B. Gross, D. Jacoby, K. Coogan, and A. Helman, âMotivating complexity understanding by profiling energy usage,â in Proc. ACM SIGPLAN Int. Symp. New Ideas New Paradigms Reflections Programm. Softw., 2021, pp. 85â96.

[37] E. A. TrÃ¤ff, A. Rydahl, S. Karlsson, O. Sigmund, and N. Aage, âSimple and efficient GPU accelerated topology optimisation: Codes and applications,â Comput. Methods. Appl. Mech. Eng., vol. 410, 2023, Art. no. 116043.

[38] A. Ray, B. Devlin, F. Y. Quah, and R. Yesantharao, âHardcaml MSM: A high-performance split CPU-FPGA multi-scalar multiplication engine,â in Proc. 2024 ACM/SIGDA ISFPGA, 2024, pp. 33â39.

[39] Q. Wu, Y. Zeng, and R. Zhang, âJoint trajectory and communication design for multi-UAV enabled wireless networks,â IEEE Trans. Wireless Commun., vol. 17, no. 3, pp. 2109â2121, Mar. 2018.

[40] Y. Yokokura, S. Katsura, and K. Ohishi, âStability analysis and experimental validation of a motion-copying system,â IEEE Trans Industr. Inform., vol. 56, no. 10, pp. 3906â3913, Oct. 2009.

[41] N. Qi, Z. Huang, W. Sun, S. Jin, and X. Su, âCoalitional formationbased group-buying for UAV-enabled data collection: An auction game approach,â IEEE Trans. Mob. Comput., vol. 22, no. 12, pp. 7420â7437, Dec. 2023.

[42] L. Tirel, A. M. Ali, and H. A. Hashim, âNovel hybrid integrated Pix2Pix and WGAN model with gradient penalty for binary images denoising,â Sys. Soft Comput., vol. 6, 2024, Art. no. 200122.

[43] M. Patil, M. M. Patil, and S. Agrawal, âWGAN for Data Augmentation,â in GANs Data Augmentation Healthcare. Berlin, Germany: Springer, 2023, pp. 223â241.

[44] W. Ye, X. Zhou, J. Zhou, C. Chen, and K. Li, âAccelerating attention mechanism on FPGAs based on efficient reconfigurable systolic array,â ACM Trans. Embed. Comput. Syst., vol. 22, no. 6, pp. 1â22, 2023.

[45] J. Li et al., âMulti-objective optimization approaches for physical layer secure communications based on collaborative beamforming in UAV networks,â IEEE/ACM Trans. Net., vol. 31, no. 4, pp. 1902â1917, Aug. 2023.

[46] Z. Qin, H. Yao, and T. Mai, âTraffic optimization in satellites communications: A multi-agent reinforcement learning approach,â in Proc. Int. Wireless Commun. Mobile Comput., 2020, pp. 269â273.

[47] S. Jayasumana, S. Ramalingam, A. Veit, D. Glasner, A. Chakrabarti, and S. Kumar, âRethinking FID: Towards a better evaluation metric for image generation,â in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024, pp. 9307â9315.

[48] J. Sautter, F. Faubel, M. Buck, and G. Schmidt, âArtificial bandwidth extension using a conditional generative adversarial network with discriminative training,â in Proc. IEEE Int. Conf. Acoust. Speech Signal Process., 2019, pp. 7005â7009.

[49] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wirel. Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

<!-- image-->

Longyu Zhou (Member, IEEE) received the PhD degree with a MD-PhD program from the School of Information and Communication Engineering, University of Electronic Science and Technology of China (UESTC) in 2013. He is a research fellow working with Singapore University of Technology and Design. He also worked in Embedded Systems (ES) group, Delft University of Technology (TU Delft), the Netherlands, as a visiting student. His research interests include Internet of Things, AI-RAN, and digital twins. He was a recipient of the best paper award at 20th IEEE ICCT and received the Young Scientist Award at 10th IEEE ICCCS. He serves/has serves as a TPC member for the IEEE Global Communications Conference (Globecom) and the IEEE International Conference on Communications (ICC), etc. He also serve a reviewer for several Journals and international conferences such as the IEEE Transactions on Mobile Computing, the IEEE Journal on Selected Areas in Communications, the IEEE Transactions on Vehicular Technology, and the IEEE Internet of Things Journal, etc.

<!-- image-->

Supeng Leng (Member, IEEE) received the PhD degree from Nanyang Technological University (NTU), Singapore, in 2005. He is a full professor with the School of Information & Communication Engineering, University of Electronic Science and Technology of China (UESTC). He is also the director with the Sichuan International Joint Research Center for Ubiquitous Wireless Networks. He has been working as a research fellow with the Network Technology Research Center, NTU. His research focuses on resource, spectrum, energy, routing and networking in

Internet of Things, vehicular networks, broadband wireless access networks, and the next generation intelligent mobile networks. He published more than 200 research papers and 4 books/book chapters in recent years. He got the Best Paper Awards at 4 IEEE international conferences. He serves as an organizing committee chair and a TPC member for many international conferences. He is the editorial member of 4 international journals and a reviewer for more than 20 well-known academic international journals.

<!-- image-->

Tony Q. S. Quek (Fellow, IEEE) received the BE and ME degrees in electrical and electronics engineering from the Tokyo Institute of Technology, in 1998 and 2000, respectively, and the PhD degree in electrical engineering and computer science from the Massachusetts Institute of Technology, in 2008. Currently, he is the associate provost (AI & Digital Innovation) and Cheng Tsang Man chair professor with Singapore University of Technology and Design (SUTD). He also serves as the director of the Future Communications R&D Programme, the ST

Engineering Distinguished professor, and the AI-on-RAN Working Group Chair in AI-RAN Alliance. His current research topics include wireless communications and networking, network intelligence, non-terrestrial networks, open radio access network, and 6G. He was honored with the 2008 Philip Yeo Prize for Outstanding Achievement in Research, the 2012 IEEE William R. Bennett Prize, the 2015 SUTD Outstanding Education Awards â Excellence in Research, the 2016 IEEE Signal Processing Society Young Author Best Paper Award, the 2017 CTTC Early Achievement Award, the 2017 IEEE ComSoc AP Outstanding Paper Award, the 2020 IEEE Communications Society Young Author Best Paper Award, the 2020 IEEE Stephen O. Rice Prize, the 2020 Nokia visiting professor, the 2022 IEEE Signal Processing Society Best Paper Award, and the 2024 IIT Bombay International Award For Excellence in Research in Engineering and Technology. He is a WWRF fellow, and a fellow of the Academy of Engineering Singapore.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_8_img_1.png|page_8_img_1]]
3. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_9_img_1.jpeg|page_9_img_1]]
4. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_10_img_1.png|page_10_img_1]]
5. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_11_img_1.png|page_11_img_1]]
6. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_12_img_1.jpeg|page_12_img_1]]
7. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_12_img_2.jpeg|page_12_img_2]]
8. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_14_img_1.png|page_14_img_1]]
9. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_19_img_1.jpeg|page_19_img_1]]
10. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_19_img_2.jpeg|page_19_img_2]]
11. [[../extracted_images/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems/page_19_img_3.jpeg|page_19_img_3]]

---

