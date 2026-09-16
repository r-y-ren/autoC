# Anchor: A Novel Modeling Methodology forS 0(&4XHXHHOHQJWK Cooperative UAV-MEC Based on Stochastic+DQGRII3URF8\$9&R038\$9&R036HW2 K c  ZL Geometry

Yan Li1, Lailong Luo1, Bangbang Ren1, Deke Guo1,âU

National Key Laboratory of Information Systems Engineering, National University of Defence Technology1\$FFHVV/8\$9&R036HW 8VHU(TXLSPHQW Deke Guo is the corresponding author: dekeguo@nudt.edu.cnâ

AbstractâUnmanned aerial vehicles (UAVs) play a vital role in the air-to-ground integrated network, which can offer a mobile edge computing (MEC) environment closer to terrestrial user equipments (UEs). This integrated network faces the challenges of unstable links and node mobility. It is urgent to rethink the UAV-assisted MEC architecture to satisfy the requirements of reliable and low-latency communication in dynamic scenarios. This paper proposes a novel dynamic cooperative offloading model for UAV swarms based on Delaunay triangulation, where each UE offloads its data to a triangular cell composed of three UAVs for joint processing. Then, we propose a novel and efficient cooperative handoff mechanism and an innovative analysis method to well tackle the mobility characteristics of UAVs. Finally, we design a performance evaluation method for UAV cooperative task offloading by leveraging the stochastic geometry analysis framework. The simulation and numerical results verify the correctness and practicability of the proposed model and analysis method. Compared to conventional cooperative and noncooperative offloading mechanisms, our approach achieves an average performance improvement of 20% and 30%, respectively.

Index TermsâCooperative offloading model, Delaunay triangulation, mobile edge computing (MEC), unmanned aerial vehicles (UAVs)

## I. INTRODUCTION

The unmanned aerial vehicle (UAV)-assisted mobile edge computing (MEC) network represents a novel architectural paradigm that effectively integrates UAV-assisted communication technology with MEC technology. The primary objective is to furnish terrestrial user equipment (UEs) with communication and computing resources that are both adaptable and scalable, thereby transcending the constraints inherent in conventional terrestrial communication and computing services [1], [2]. As the UAV and MEC technologies continue to advance and their applications increasingly diversify across various fields, integrated models show great potential in improving network coverage and computing efficiency [3]. These aerial platforms enhance terrestrial infrastructureâs coverage and computation capabilities and efficiently solve the communication and computing needs in addressing remote or mobile scenarios, facilitating convenient and swift services to UEs.

Current research on UAV-assisted MEC networks mainly focuses on optimizing the performance of individual UAV nodes within specific parameters. This includes addressing critical issues such as allocating communication and computational resources, offloading computational tasks, and developing strategies for deploying UAVs and planning trajectories [4]â[6]. However, the demand for real-time processing and computing power has also grown with the continuous development of emerging applications like autonomous driving, digital twins, and virtual realms. Focusing solely on optimizing single-node UAV performance or augmenting the scale of UAV-assisted MEC systems to enhance edge computing capabilities and extend coverage areas poses significant challenges in ensuring the systemâs stability and reliability. Moreover, this approach fails to exploit the inherent potential of the large-scale UAV-MEC architecture. The main problem is that the optimization strategy for single-node performance is challenging to adapt to complex and changeable mobile scenarios. Moreover, expanding the scale introduces intricate interference that can degrade the overall task offloading performance, including communication and computing delays. Therefore, it is urgent to design a novel UAV-assisted MEC model that can comprehensively consider the cooperation between UAV nodes and dynamically changing mobile scenarios to improve the performance of the entire edge computing system effectively.

<!-- image-->  
Fig. 1. A UAV-assisted model based on Delaunay triangulation.

To address this issue, as shown in Fig. 1, this paper presents a novel cooperative offloading model for UAV swarms based on Delaunay triangulation. By leveraging cooperation among UAVs, the model can enhance network reliability and reduce inter-cell interference, thus significantly improving system throughput and reducing communication delay during task offloading. However, the challenge of mobility management intensifies within this cooperative offloading model. Compared to the traditional single-node network, the cooperative handoff is more intricate, primarily due to the irregularity and complexity of the service area boundary, making it challenging to describe precisely. When a typical UE crosses the boundary of a cooperation area, its service cooperation node needs to be switched in real time. Considering the random movement of UAVs, cooperative handoffs by UEs become even more unpredictable. To provide a detailed illustration, Fig. 1 depicts the handoff process of a coordinated multi-point (CoMP) set for a typical projected UE. It graphically reveals the dynamic changes in the structural and positional information of the triangular unit triggered by the movement of a UAV. Traditional analytical approaches that rely on single-node UAV handoff mechanisms, as referenced in [7], [8], are insufficient for accommodating the complexities of handoff modeling within dynamic cooperative scenarios. Therefore, designing an efficient cooperative UAV handoff mechanism and evaluating methods for handoff performance is vital to the cooperative offloading model.

Evaluating the cooperative handoff performance can provide crucial guidance for system design. It lays a foundational basis for assessing the performance of cooperative offloading models in terms of the successful edge computing probability (SECP). Its evaluation strategy necessitates a balanced consideration of successful communication and computing probabilities. In this study, we characterize the UAVs as a Poisson point process (PPP) to capture their spatial randomness. Then, we construct the UAV mobility and cooperative offloading models based on the Delaunay triangulation. Further, an efficient cooperative handoff mechanism is proposed. Finally, we design an optimization method for SECP by precisely quantifying the successful uplink communication probability (SUCP) for coherent joint transmission and the successful computing probability (SCP) for task offloading. The main contributions are as follows:

â¢ Network modeling: A dynamic cooperative offloading model for UAV swarms is proposed based on the Delaunay triangulation theory. It ingeniously integrates the CoMP technology to significantly enhance the network coverage and strengthen the reliability of the UAV offloading link. Specifically, the data of each UE is offloaded to a triangular cell composed of three UAVs for joint processing. This method effectively constructs a deterministic UAV CoMP offloading set, avoiding exhaustive searching and optimizing computational efficiency and system performance.

â¢ Handoff mechanism: A dynamic cooperative handoff mechanism is developed by leveraging the geometric properties of Delaunay triangulation. This mechanism, in turn, facilitates the establishment of a parameterized probabilistic model to characterize the time-varying scenarios of the dynamic CoMP set, which can effectively predict cooperative handoff behaviors. This establishment lays a fundamental basis for accurately quantifying the SECP.

â¢ Offloading strategy: A performance evaluation method for UAV cooperative task offloading has been designed based on SECP. Specifically, the SECP for UEs was analytically derived by leveraging the analytical framework of stochastic geometry. Compared to conventional cooperative and non-cooperative offloading mechanisms, the proposed scheme demonstrates superior performance in edge computing.

The rest of this paper is organized as follows: Section II discusses the relationship between our research and existing literature. Section III presents the system model. Section IV presents the theoretical analysis of the SECP. Section V validates our analysis with simulation. Finally, Section VI presents the conclusions.

## II. RELATED WORKS

In this section, we will provide an overview of the current models for optimizing UAV-assisted MEC networks and discuss the most recent research on handoff evaluation methodologies.

## A. Optimization Model for UAV-Assisted MEC Networks

Researchers have extensively studied multi-parameter cooperative optimization strategies to improve the overall performance of UAV-assisted MEC networks. Recent research has concentrated on optimizing system goals, such as reducing energy consumption, minimizing latency, and enhancing network throughput. In a single-UAV scenario, the work [9] achieved the minimization of the average weighted energy consumption for all users. In [10], the total energy consumption of users and UAVs was minimized, considering the constraints of task delay and its dependencies. Furthermore, the study [11] was primarily concerned with optimizing the propulsion energy efficiency of UAVs while enhancing the overall system throughput. In [12], a problem was proposed regarding minimizing energy consumption in UAV-assisted MEC networks. The issue of minimizing total energy consumption in UAV-assisted MEC networks was investigated in [13], which involved jointly optimizing core parameters such as the UAV beamforming vector and UAV trajectory.

In the extensive application of multi-UAV systems, the total energy consumption of ground users was successfully minimized [14]. The work [15] then aimed to minimize the maximum task completion delay between devices, and the study [16] focused on the energy limitation problem of UAVs, aiming to minimize weighted energy consumption. More recently, for the multi-UAV cooperative computing scenario, the total network utility of the cooperative UAV edge computing network was maximized [17]. The work [18] then took minimizing the total energy consumption of tasks as the goal. Nonetheless, significant gaps remain in the scholarly exploration of the cooperative networking paradigm of UAVassisted MEC systems and the refinement of optimization approaches for SECP. In particular, the current literature still needs to tackle the challenge of managing the handoff of UAV mobility, a critical aspect that could impact system performance and reliability.

## B. UAV-Assisted MEC Network Handoff Evaluation

Stochastic geometry is frequently employed to assess handoff performance. In this context, the analysis of handoffs often simplifies by comparing the distances between UE and BSs. Based on this approach, the handoff probability in terrestrial networks was examined [19], [20]. Then, the handoff probability within UAV networks was investigated in [21]. However, it is known that proximity to a BS does not necessarily ensure more substantial signal power. Therefore, distance-based methods are not appropriate for analyzing heterogeneous networks. In [22]â[24], an equivalent analysis approach was put forward, which regarded vertical handoffs as horizontal handoffs for processing, aiming to describe the handoff performance in heterogeneous networks better. In [25], the equivalent model was further extended to UAV networks with variable BS heights. Recently, a time-varying boundary model was proposed to characterize the handoffs in UAV-assisted networks [26]. Moreover, a handoff mechanism grounded in the flight direction was introduced in [27], notably decreasing the handoff rate. Nonetheless, these studies are limited to scenarios involving single BS associations and do not apply to cooperative wireless networks.

<!-- image-->  
Fig. 2. An illustration of the DMM mobility model.

## III. SYSTEM MODEL

As depicted in Fig. 1, we investigate a UAV-assisted communication network that supports MEC. All UAVs are assumed to follow a PPP $\Phi _ { u }$ with density $\lambda _ { u }$ and operate at the same flight altitude $h ^ { 1 }$ . Each UAV is equipped with M antennas and is interconnected via a reliable backhaul link to a central server (CS). Concurrently, all UE are distributed throughout the network following a PPP $\Phi _ { e }$ with density $\lambda _ { e } ,$ each equipped with a single antenna. Without loss of generality, it is assumed that the data of a typical UE located at the origin $O ( 0 , 0 , 0 )$ is simultaneously offloaded to the three UAVs within its designated offloading CoMP set, denoted as ${ { \mathcal U } _ { 0 } } = \left\{ { { A } _ { 0 } } , { { A } _ { 1 } } , { { A } _ { 2 } } \right\}$ . Each offloading CoMP set encompasses a circular region of radius $r _ { 0 }$ . The Euclidean distance from the $i ^ { \mathrm { { t h } } }$ UAV to the typical UE at O is denoted as $u _ { i } ,$ where $i \in \{ 1 , 2 , \cdots , \infty \}$ . Let wi represent the distance between the $i ^ { \mathrm { t h } } \ \mathrm { \ U A V }$ and the projected UE, denoted as $O ^ { \prime } ( 0 , 0 , h )$ . Consequently, the relationship between $u _ { i }$ and $w _ { i }$ can be expressed as $u _ { i } = \sqrt { w _ { i } ^ { 2 } + h ^ { 2 } }$ . The advantage of this model lies in its seamless integration of CoMP transmission capabilities, enabling the UAV swarm to deliver URLLC services to terrestrial UEs.

Since computational tasks typically yield minimal output, the time consumed for downlink transmission is negligible relative to the latency experienced during the data backhaul process [28]â[30]. Therefore, our analysis will focus exclusively on uplink communication transmission and edge computing processing, omitting any consideration of downlink transmission.

## A. Mobility Model

Inspired by the mobility model employed in the 3GPP specifications [31], we propose a dynamic mobility model (DMM)

<!-- image-->  
Fig. 3. The illustrative Poisson-Delaunay triangulation network, in which the CoMP set is composed of UAVs located at the vertices of the black dashed boundaries of the Delaunay triangles. The projected UAVs (represented by blue triangles) are distributed as a PPP, and the UEs (denoted by red circles) are uniformly distributed within a normalized coverage area.

for UAV swarms. Within this model, each UAV navigates in a straight line at a random speed and altitude, with its direction being uniformly and independently distributed. However, the DMM provides a foundational benchmark against which more intricate mobility models can be assessed.

For illustrative purposes, Fig. 2 presents the trajectories of two UAVs with random velocities Ï0 and $v _ { 1 }$ , which are independent and identically distributed (i.i.d). Qk and $S _ { k }$ represent their turning points at time instants $t _ { k } , k \in { 0 , 1 , 2 }$ , respectively. Similarly, the angle between the direction from $Q _ { 0 }$ to $Q _ { 1 }$ and the positive x-axis is denoted by $\theta _ { 0 } .$ , which is uniformly distributed in [0, 2Ï). When the UAV reaches $Q _ { 1 }$ , it changes direction at a new angle $\theta _ { 1 }$ to reach the next turning point $Q _ { 2 } ,$ where the distribution of $\theta _ { 1 }$ is independent and identical to that of $\theta _ { 0 }$

## B. Offloading CoMP Set

To facilitate understanding the 3D scene presented in Fig. 1, Fig. 3 depicts the UAVs and their corresponding projected UEs on a two-dimensional plane, utilizing blue triangles $( \ ' \triangle ' )$ and red circles (ââ¦â) to represent them, respectively. Additionally, the Poisson-Delaunay triangulation [32], [33] is illustrated in Fig. 3, represented by triangles with black dashed line boundaries.

Each projected UE should have a corresponding offloading CoMP set, which can be determined as follows. Using $\mathrm { U E _ { 1 } }$ in Fig. 3 as an example, it first selects the nearest UAVs $A _ { 0 }$ and $A _ { 1 }$ as its two associated BSs, establishing the edge of a cooperative triangle cell. Two adjacent triangles sharing the same side define a quadrilateral with vertices $\{ A _ { 0 } , A _ { 2 } , A _ { 1 } , A _ { 4 } \}$ $\mathrm { U E _ { 1 } }$ selects the two UAVs that have the shortest distances among the four UAVs located at the vertices of the quadrilateral, as well as another UAV positioned between the remaining two opposite UAVs and closer to UE1. Eventually, this forms the CoMP set ${ { \mathcal U } _ { 0 } } = \left\{ { { A _ { 0 } } , { A _ { 1 } } , { A _ { 2 } } } \right\}$ . For a typical UE, the UAVs within the CoMP set are designated as serving UAVs, while all the other UAVs are interfering UAVs.

## C. Uplink Communication Transmission Model

We propose a cooperative model where each UE can connect with up to three UAVs in its offloading CoMP set. Each CoMP set covers a designated area represented as a circle with a radius of $r _ { 0 } .$ . The system operates in time division duplexing (TDD) mode, with channels subject to Rayleigh fading. Based on these assumptions, we analyze the signal-to-interference ratio (SIR) for uplink transmissions under interference-limited conditions.

We assume that all UEs are modeled as a PPP. In this context, we focus on the SIR of a typical UE, designated as the $0 ^ { \mathrm { t h } }$ UE without loss of generality. If each UAV is equipped with a maximum ratio combining (MRC) receiver, the received SIR at the $i ^ { \mathrm { t h } }$ UAV can be expressed.:

$$
\mathrm { S I R } _ { i 0 , \mathrm { u l } } = \frac { g _ { i 0 } u _ { i 0 } ^ { - \alpha } } { \sum _ { q \in \Phi _ { e } \backslash \{ 0 \} } \hat { g } _ { i q } u _ { k q } ^ { - \alpha } }\tag{1}
$$

where $g _ { i 0 } \sim \Gamma ( M , 1 )$ is the total received channel gain at the $i ^ { \mathrm { t h } } \ \mathrm { U A V }$ from the $0 ^ { \mathrm { t h } }$ UE and $\hat { g } _ { k q . } ~ \sim ~ \exp ( 1 )$ models the independent channel gains for the $\hat { \boldsymbol q } ^ { \mathrm { t h } }$ interfering UE. Here, $q ^ { \mathrm { t h } }$ interfering UE. denotes the link distance between the $i ^ { \mathrm { t h } }$ UAV and the

## D. Task Offloading Model

We consider a scenario in which UAVs are equipped with distinct MEC servers while the CS possesses cloud computing capabilities. As a result, the offloaded tasks can be allocated with a probability p for processing at the CS and a complementary probability $1 - p$ for processing at the MEC servers connected to the UE. We denote the computation latency associated with the MEC servers as $T _ { \mathrm { m } }$ and that of the central server as $T _ { \mathrm { c } }$ . The overall computation latency for the proposed task offloading model can be expressed as

$$
T _ { \mathrm { s c p } } = \left\{ \begin{array} { l l } { T _ { \mathrm { c } } , \mathrm { \ w i t h \ p r o b a b i l i t y \ } p } \\ { T _ { \mathrm { m } } , \mathrm { \ w i t h \ p r o b a b i l i t y \ } 1 - p } \end{array} \right. .\tag{2}
$$

1) Edge Computing Model: Our proposed model configures each UE to establish simultaneous connections with three MEC servers. Upon offloading a task for processing at an MEC server, the task execution can be performed on any available server within the CoMP set. The selection of the MEC server for task execution is based on the server exhibiting the lowest instantaneous computation load within the CoMP set. In this context, the total latency incurred for processing a task offloaded by the UE at an MEC server can be defined as

$$
T _ { \mathrm { m } } \triangleq T _ { \mathrm { m } , \hat { i } } , \mathrm { w h e r e ~ } \hat { \mathrm { i } } \triangleq \arg \operatorname* { m i n } _ { \mathrm { i } \in \{ 1 , 2 , 3 \} } \mathrm { N } _ { \mathrm { m } , \mathrm { i } } ,\tag{3}
$$

where $T _ { \mathrm { m } , \hat { i } }$ denotes the computation delay, $N _ { m , i }$ represents the instantaneous queue load at the $i ^ { \mathrm { t h } }$ MEC server connected to the UE.

2) Task Execution Time: We assume that the average task processing time on the CS and MEC servers is $1 / u _ { c }$ seconds and $1 / u _ { m }$ seconds, respectively. The computing time is called the service time in the queuing model. Similar to [34], [35], we assume that the taskâs service rate is $u _ { i } ( i \in \{ c , m \} )$ , and its computing time is exponentially distributed. The overall distribution of the service time $\tau _ { i }$ on the CS and MEC servers is given by

$$
f _ { \tau , i } ( t ^ { \prime } ) = u _ { i } e ^ { - u _ { i } t ^ { \prime } } , \ t ^ { \prime } \geq 0 .\tag{4}
$$

## E. Performace Metric

For a comprehensive evaluation of communication performance, similar to [20], the successful uplink communication probability with handoffs (SUPH) is defined as

$$
P _ { \mathrm { s u p h } } ( t ) \triangleq [ ( 1 - \varsigma ) + \varsigma ( 1 - \mathbb { P } [ \mathrm { H o f f } ( t ) ] ) ] P _ { \mathrm { c , u l } } ( t )\tag{5}
$$

where Ï denotes the probability of failure due to handoffs, reflecting the systemâs degree of tolerance towards handoff events, and $P [ \mathrm { H o f f } ( t ) ]$ represents the cooperative handoff probability. Finally, given the threshold SIR Î³, $P _ { \mathrm { c , u l } } ( t )$ then refers to the SUCP, which is defined as

$$
P _ { \mathrm { c , u l } } ( t ) \triangleq \mathbb { P } \left[ \operatorname* { m a x } _ { i \in \{ 1 , 2 , 3 \} } \mathrm { S I R } _ { i 0 , \mathrm { u l } } \geq \gamma \right] .\tag{6}
$$

Therefore, based on the (5) and (6), the SECP can be further defined as

$$
P _ { \mathrm { s e c p } } = P _ { \mathrm { s u p h } } ( t ) \mathbb { P } \left[ T _ { \mathrm { s c p } } \leq t ^ { \prime } \right] = P _ { \mathrm { s u p h } } ( t ) P _ { \mathrm { s c p } } ( t ^ { \prime } ) ,\tag{7}
$$

where $P _ { \mathrm { s c p } } ( t )$ denotes the SCP, which is given by

$$
\begin{array} { r l r } {  { P _ { \mathrm { s c p } } ( t ^ { \prime } ) \triangleq \mathbb { P } [ T _ { \mathrm { s c p } } \le t ^ { \prime } ] } } \\ & { } & { = p \mathbb { P } [ T _ { \mathrm { c } } \le t ^ { \prime } ] + ( 1 - p ) \mathbb { P } [ T _ { \mathrm { m } } \le t ^ { \prime } ] . } \end{array}\tag{8}
$$

## IV. SUCCESSFUL EDGE COMPUTING PROBABILITY

The overall performance of edge computing depends on both communication and computation capabilities. In this section, we initially derive the cooperative handoff probability, analyze the SUPH by characterizing the SUCP, and ultimately analyze the SECP.

## A. CoMP Handoff Probability

1) CoMP Handoff Strategy: In the proposed handoff mechanism, we first define a handoff event. As shown in Fig. 3, the decision for a typical UE to perform a handoff depends on whether the average received power changes, where the average is taken with respect to the channel fading. Let $\ * U _ { i } ( t ) \dot { \ } = \ \{ A _ { i } , B _ { i } , C _ { i } \}$ , denote the $i ^ { \mathrm { t h } }$ CoMP set, we have $\begin{array} { r } { \Phi ( t ) = \{ \mathcal { U } _ { i } ( t ) \} | _ { i = 0 } ^ { \infty } . \mathrm { ~ I f ~ } \mathcal { E } _ { i } ( t ) = \left| \sum _ { k \in U _ { i } ( t ) } P ^ { \frac { 1 } { 2 } } ( t ) u _ { k } ^ { - \frac { \alpha } { 2 } } ( t ) \right| ^ { 2 } < } \end{array}$ $\begin{array} { r } { \mathcal { E } _ { j } ( s ) = \left| \sum _ { j \in U _ { j } ( s ) } P ^ { \frac { 1 } { 2 } } ( s ) u _ { k } ^ { - \frac { \alpha } { 2 } } ( s ) \right| ^ { 2 } } \end{array}$ , a handoff occurs from the $i ^ { \mathrm { t h } }$ CoMP set to an adjacent $j ^ { \mathrm { t h } }$ CoMP set. This transition manifests as changing the associated CoMP sets and the triangular lists.

The handoff process for a typical projected UE is shown in Fig. 1. At time $t _ { 0 } ,$ the initial CoMP set is represented by $\{ \bar { A } , B , C \}$ . Due to independent movements, these UAVs transition to $\{ A ^ { \prime } , B ^ { \prime } , D ^ { \prime } \}$ at the next moment, $t _ { 1 } .$ . Since UAVs $\{ A ^ { \prime } , B ^ { \prime } , C ^ { \prime } \}$ do not form a triangular Delaunay cell, the typical projected UE must switch to its nearest CoMP set, $\{ \dot { A } ^ { \prime } , B ^ { \prime } , \dot { D } ^ { \prime } \}$ . Due to the UAVsâ movement, both the UAV locations and the triangular lists for a typical UE are timevarying. Consequently, characterizing the virtual triangular cellsâ coverage area (i.e., the area associated with the same offloading CoMP set for the UE) presents a challenge.

2) CoMP Handoff Probability: The cooperative handoff probability is derived in the following. Before that, we first derive the density of interfering UAVs.

Due to introducing the exclusion region $\mathbb { B } = \mathbb { C } ( O , \hat { w } )$ by the nearest neighbor association criterion, the interfering UAVs follow a non-homogeneous point process. When considering B, the density of UAVs can be divided into two parts: One part is contributed by B, denoted as $\lambda _ { 1 } ( t ; w _ { i } , \hat { w } )$ . The other part is for the interfering UAVs, denoted as $\lambda ( t ; w _ { i } , \hat { w } )$ . Since the total density of UAVs is $\lambda _ { u } ,$ then we obtain $\lambda ( t ; w _ { i } , \hat { w } ) =$ $\lambda _ { u } - \lambda _ { 1 } ( t ; w _ { i } , \hat { w } )$ . Using a method similar to [36, Lemma 2], we can explicitly calculate the density of interfering UAVs, as described in the following lemma.

Lemma 1. Let Ï denote a non-negative random variable (RV) representing the speed of a UAV, which has a cumulative distribution function (CDF) $F _ { v } ( x )$ and a probability density function (PDF) $f _ { v } ( x )$ . The difference set $\bar { \Phi _ { u } } ( t ) \backslash U _ { 0 } \dot { ( t ) }$ forms a non-homogeneous PPP, and its intensity is calculated as

$$
\begin{array} { l } { { \lambda ( t ; w _ { i } , \hat { w } ) = \lambda _ { u } - \lambda _ { u } F _ { v } \left( \displaystyle \frac { \hat { w } - w _ { i } } { t } \right) - \frac { \lambda _ { u } } { \pi } \int _ { \frac { | \hat { w } - w | } { t } } ^ { \frac { \hat { w } + w _ { i } } { t } } } } \\ { { \times f _ { v } ( x ) \operatorname { a r c c o s } \left( \displaystyle \frac { { w _ { i } } ^ { 2 } + v ^ { 2 } t ^ { 2 } - \hat { w } ^ { 2 } } { 2 w _ { i } v t } \right) \mathrm { d } x } . } \end{array}\tag{9}
$$

With (9), we can derive the handoff probability for the DMM model.

We utilize the equivalent handoff model recently developed in [37] for ground-to-air (G2A) wireless networks to address the complex handoff patterns in mobile ground terminals. This model examines the handoff performance of mobile UAV terminals served by multiple ground BSs. Similar to the G2A network, the average coverage area of virtual Delaunay triangular cells in this paper is comparable to that of dual Voronoi cells, as the coverage area of triangular cells only depends on the density of the corresponding PPP. This way, the challenging-to-analyze initial CoMP handoff region is equivalent to the classical Voronoi structure with the nearestneighbor association criterion. The resulting Voronoi cells exhibit convexity, allowing for their quantitative characterization using stochastic geometry theory.

Without loss of generality, we assume that a typical UE offloads signals to three serving UAVs within a CoMP set ${ \mathcal U } _ { 0 } ( t ) \stackrel { - } { = } \{ A _ { 0 } , A _ { 1 } , A _ { 2 } \}$ , and each UAV in ${ \mathcal { U } } _ { 0 } ( t )$ moves at a speed $v _ { k }$ with angle $\theta _ { k }$ , where $\theta _ { k }$ is uniformly distributed in [0, 2Ï), $k \in \{ 1 , 2 , 3 \}$ . Let $\hat { \upsilon }$ and ËÎ¸ denote the velocity and direction of the equivalent serving UAV, respectively. Utilizing elementary geometric theory, we obtain

$$
\hat { v } = \left( \left( \sum _ { k = 1 } ^ { 3 } v _ { k } \cos \theta _ { k } \right) ^ { 2 } + \left( \sum _ { k = 1 } ^ { 3 } v _ { k } \sin \theta _ { k } \right) ^ { 2 } \right) ^ { 1 / 2 } ,\tag{10}
$$

and

$$
\hat { \boldsymbol { \theta } } = \arctan \left( \frac { \sum _ { k = 1 } ^ { 3 } \boldsymbol { v } _ { k } \sin \theta _ { k } } { \sum _ { k = 1 } ^ { 3 } \boldsymbol { v } _ { k } \cos \theta _ { k } } \right) .\tag{11}
$$

Next, the distributions of ÏË and $\hat { \theta }$ are derived and summarized in the following lemma.

Lemma 2. The PDF of ÏË defined by (10) is expressed as

$$
{ f } _ { \hat { v } } ( x ) = \frac { 2 } { \Gamma ( a ) b ^ { a } } x ^ { 2 a - 1 } \exp \bigg ( { - \frac { x ^ { 2 } } { b } } \bigg ) ,\tag{12a}
$$

with

$$
a \triangleq \frac { 3 \left( \mathbb { E } \left( v _ { k } ^ { 2 } \right) \right) ^ { 2 } } { \mathbb { E } \left( v _ { k } ^ { 4 } \right) + \left( \mathbb { E } \left( v _ { k } ^ { 2 } \right) \right) ^ { 2 } } ,\tag{12b}
$$

$$
b \triangleq \frac { \mathbb { E } \left( v _ { k } ^ { 4 } \right) + \left( \mathbb { E } \left( v _ { k } ^ { 2 } \right) \right) ^ { 2 } } { \mathbb { E } \left( v _ { k } ^ { 2 } \right) } ,\tag{12c}
$$

<!-- image-->  
Fig. 4. The equivalent UAV moves from $Q _ { 0 }$ with speed ÏË and angle $\hat { \theta }$ during time t to $\bar { Q } _ { 1 \cdot } \mathrm { ~ \bf ~ A ~ }$ handoff occurs if another equivalent UAV at $\bar { Q } _ { 2 }$ is closer than RË to ${ \partial } ^ { \prime }$

and $\hat { \theta }$ defined by (11) is uniformly distributed within [0, 2Ï).

Proof. See Appendix A.

Using Lemma 2, we can deduce the CoMP handoff probability. As depicted in Fig. 4, let $Q _ { 0 }$ denote the initial position of the equivalent serving UAV at a distance wË from the projected UE ${ \hat { O } } ^ { \prime }$ . Suppose the UAV travels to a new location $Q _ { 1 }$ at time $t ,$ moving at speed ÏË in the direction ${ \hat { \theta } } .$ By employing the cosine theorem, $Q _ { 2 }$ is at a distance

$$
\hat { R } = \left( \hat { w } ^ { 2 } + \hat { v } ^ { 2 } t ^ { 2 } + 2 \hat { w } \hat { v } t \cos \hat { \theta } \right) ^ { 1 / 2 }\tag{13}
$$

from $O ^ { \prime } .$ . Therefore, a handoff occurs if another equivalent UAV (for instance, a UAV at $Q _ { 2 }$ in Fig. 4) is closer to $O ^ { \prime }$ than ${ \hat { R } } .$ Let ${ \mathcal { C } } ( O ^ { \prime } , { \hat { R } } )$ represent the circle with radius $\hat { R }$ centered at $O ^ { \prime }$ . Define $\mathcal { G }$ as the event that there is no UAV in ${ \mathcal { C } } ( O ^ { \prime } , { \hat { R } } )$ , and Hoff(t)as the event that no handoff occurs until time t. We know Hoff $( t ) \subset \mathcal { G }$ because of the different speeds of the equivalent serving UAVs and the events that UAVs may enter and exit the circle ${ \mathcal { C } } ( O ^ { \prime } , { \hat { R } } )$ during time t, such as the interfering UAV moving from $Q _ { 2 }$ to $Q _ { 3 }$ in Fig. 4. Thus, we have $\mathbb { P } \left[ \mathbf { \overline { { H o f f } } } ( t ) \right] \leq \mathbb { P } [ \mathcal { G } ]$ , which establishes a lower bound for the handoff probability as follows.

Theorem 1. In the DMM model, the lower bound on the CoMP handoff probability can be calculated as

$$
\begin{array} { r } { \mathbb { P } [ \mathrm { H o f } ( t ) ] \ge 1 - \displaystyle \int _ { 0 } ^ { \infty } \int _ { 0 } ^ { \infty } \int _ { - \pi } ^ { \pi } 2 \hat { w } \lambda _ { u } \exp \big ( - 2 \pi \hat { w } ^ { 2 } \lambda _ { u } \big ) f _ { \hat { v } } ( x ) } \\ { \times \exp \left[ - \displaystyle \int _ { 0 } ^ { \hat { R } } 4 \pi w \lambda \left( t ; w , \hat { w } \right) \mathrm { d } w \right] \mathrm { d } \hat { \theta } \mathrm { d } \hat { w } \mathrm { d } x , } \end{array}\tag{14}
$$

where $\lambda \left( t ; w , \hat { w } \right)$ is given by (9) with $f _ { v ^ { \ast } } ( x )$ in place of $f _ { v } ( x )$

Proof. Given $\{ \hat { w } , \hat { \theta } , \hat { v } \}$ , the conditional handoff probability can be computed as

$$
\begin{array} { r l r } {  { \mathbb { P } [ \mathrm { H o f f } ( t ) | \hat { w } , \hat { \theta } , \hat { \upsilon } ] = 1 - \mathbb { P } [ \mathrm { H o f f } ( t ) ] \geq 1 - \mathbb { P } [ \mathcal { G } ] } } \\ & { } & { = 1 - \exp [ \int _ { 0 } ^ { \hat { R } } 4 \pi w \lambda ( t ; w , \hat { w } ) \mathrm { d } w ] . } \end{array}\tag{15}
$$

Integrating (15) with respect to wË, ${ \widehat { \theta } } ,$ and ÏË yields (14).

B. Successful Uplink Communication Probability with Handoffs

In our proposed model, all UAVs are interconnected with the CS through a reliable backhaul network. This interconnection facilitates the sharing of offloaded data by the UAVs once a UE has transmitted it via uplink. If none of the connected UAVs can successfully receive the data, the uplink transmission from the UE may experience an outage. Therefore, the uplink outage probability for a typical UE can be expressed as

$$
p _ { \mathrm { o , u l } } \triangleq 1 - p _ { \mathrm { c , u l } } = \mathbb { P } \left[ \mathrm { S I R } _ { i 0 , \mathrm { u l } } \leq \gamma , \forall i \in \{ 1 , 2 , 3 \} \right] ,\tag{16}
$$

where $\mathrm { S I R } _ { i 0 , \mathrm { u l } }$ is defined in (1). To calculate the SUCP, we first derive the distance distribution involved in (16).

By applying the Palm distribution theory, as detailed in reference [38], the distribution of the horizontal distances $w _ { 1 }$ $w _ { 2 }$ , and $w _ { 3 }$ are derived and presented as

$$
f _ { w _ { i } } \left( w _ { i } \right) = \frac { 2 ( \lambda _ { u } \pi ) ^ { i } } { ( i - 1 ) ! } w _ { i } ^ { 2 i - 1 } \exp \left( - \lambda _ { u } \pi w _ { i } ^ { 2 } \right) ,\tag{17}
$$

where $i \in \{ 1 , 2 , 3 \}$

The Laplace transform of the uplink interference power is then given by

$$
\begin{array} { c c } { { { \mathcal { L } } _ { I } ( s ) = \displaystyle \exp \left( \lambda _ { e } \pi { u _ { 0 } } ^ { 2 } - \lambda _ { e } \pi { h ^ { 2 } } _ { 2 } F _ { 1 } \left[ \begin{array} { l } { { 1 ~ - { \frac { 2 } { \alpha } } } } \\ { { 1 - { \frac { 2 } { \alpha } } } } \end{array} ; - s { u _ { 0 } } ^ { - \alpha } \right] \right) } } \\ { { \mathrm { ~ } \times \exp \left( - \lambda _ { e } \pi { u _ { 0 } ^ { 2 } } \left( 1 - { \frac { 1 } { 1 + s { u _ { 0 } ^ { - \alpha } } } } \right) \right) , ~ } } & { { { ( 1 \mathrm { ~ } } } } \end{array}\tag{8}
$$

where $u _ { 0 } = \sqrt { w _ { 0 } ^ { 2 } + h ^ { 2 } } .$

Utilizing the relation provided in (16), we finally derive the SUCP for the reference UAV in the subsequent lemma.

Lemma 3. The successful uplink communication probability for a typical UE is given by

$$
\begin{array} { r } { p _ { \mathrm { c , u l } } = 1 - \displaystyle \prod _ { k = 1 } ^ { 3 } \left( 1 - \int _ { 0 < w _ { k } \leq \infty } \sum _ { m = 0 } ^ { M - 1 } \frac { ( - 1 ) ^ { m } } { m ! } u _ { i 0 } ^ { \alpha m } \gamma ^ { m } \mathcal { L } _ { I } ^ { m } \left( u _ { k 0 } ^ { \alpha } \gamma \right) \right. } \\ { \left. \times f _ { w _ { k } } \left( w _ { k } \right) \mathrm { d } w _ { k } \right) \qquad ( 1 9 ) } \end{array}
$$

where $f _ { w _ { i } } ( w _ { i } )$ and $\mathcal { L } _ { I } ( s )$ are given by (17) and (18), respectively.

Proof. See Appendix B.

In light of (14) and (19), the SUPH summarized in the following theorem.

Theorem 2. The successful uplink communication probability with handoffs for a typical UE can be calculated as

$$
P _ { \mathrm { s u p h } } ( t ) \leq [ ( 1 - \varsigma ) + \varsigma ( 1 - \mathbb { P } [ \mathrm { H o f f } ( t ) ] ) ] P _ { \mathrm { c , u l } } ( t ) .\tag{20}
$$

C. Successful Edge Computing Probability Analysis

Recalling the task offloading model proposed in Section III-D, each MEC server (UAV) is connected to all UEs requesting edge computing resources within a coverage area with radius $r _ { 0 }$ . Since UEs follow a homogeneous PPP, the task arrival rate also follows a Poisson process. Since users choose to process tasks at the CS and MEC servers with a fixed probability, their task arrival rates can be modeled as Poisson processes. For traceability in the analysis, we assume that all MEC servers have the same computation capabilities. In the following, we will derive the task arrival rates and the computing probability, followed by the final edge computing probability.

1) Task Arrival Rate: In the task offloading model, either the CS or the MEC server executes the offloaded tasks, provided that at least one MEC server successfully receives the task. As a result, the overall arrival rate of tasks at the computational devices (i.e., CS and MEC servers) is denoted by $\dot { \lambda _ { e } } | S | P _ { \mathrm { s u p h } } ( t )$ . Given that a proportion p of the total tasks is allocated to the CS, the arrival rate of tasks at the CS can be expressed as:

$$
\mathrm { r } _ { c } = p \lambda _ { e } | \boldsymbol { S } | P _ { \mathrm { s u p h } } ( t ) ,\tag{21}
$$

where |S| denotes the whole network area, and $P _ { \mathrm { s u p h } } ( t )$ is given in (20).

On the other hand, the MEC server receives all offloaded tasks from UEs within its coverage area, which is defined as a circle with radius $r _ { 0 } .$ The rate of task offloading to the MEC server is expressed as $\mathrm { r _ { o } } = ( 1 - p ) \lambda _ { e } \pi r _ { 0 } ^ { 2 } P _ { \mathrm { s u p h } } ( t )$ . It is important to note that only MEC servers with minimal computational load are designated for task processing. Since all MEC servers possess identical computational capabilities, the probability that a connected MEC server will handle a task is $1 / 3$ . Therefore, the task arrival rate at the MEC server can be calculated as

$$
\mathrm { r } _ { m } = \frac { 1 } { 3 } \mathrm { r } _ { \mathrm { { o } } } = \frac { 1 } { 3 } ( 1 - p ) \lambda _ { e } \pi r _ { 0 } ^ { 2 } P _ { \mathrm { s u p h } } ( t ) .\tag{22}
$$

2) Successful Computation Probability Analysis: The SCP is defined as the probability that task processing is completed within the target computation time. We employ queuing system concepts to compute the SCP to separately model the $T _ { \mathrm { c } }$ and $T _ { \mathrm { m } }$ for different UEs. Given the target computation delay, we derive the SCP expression in the following theorem.

Theorem 3. According to (8), the successful computing probability can be calculated as

$$
P _ { \mathrm { s c p } } ( t ^ { \prime } ) = p \mathbb { P } \left[ T _ { \mathrm { c } } \leq t ^ { \prime } \right] + ( 1 - p ) \mathbb { P } \left[ T _ { \mathrm { m } } \leq t ^ { \prime } \right] ,\tag{23}
$$

where $\mathbb { P } \left[ T _ { \mathrm { c } } \leq t ^ { \prime } \right]$ is given by

$$
\mathbb { P } \left[ T _ { c } \le t ^ { \prime } \right] = 1 - \exp \left( - u _ { c } t ^ { \prime } + \mathrm { r } _ { c } t ^ { \prime } \right)\tag{24}
$$

where $\mathbb { P } \left[ T _ { \mathrm { m } } \leq t ^ { \prime } \right]$ is given by

$$
\begin{array} { r } { \mathbb { P } \left[ T _ { m } \leq t ^ { \prime } \right] = 1 - e ^ { - u _ { m } t ^ { \prime } \left( 1 - \rho _ { m } ^ { 3 } \right) } , } \end{array}\tag{25}
$$

where $\rho _ { \mathrm { m } } \triangleq { \frac { \mathrm { r } _ { m } } { u _ { \mathrm { m } } } }$

Proof. Given the service rate $u _ { c } ,$ the distribution of the computation latency at the CS is $f _ { T _ { \mathrm { c } } } ( x ) = \left( u _ { c } - \mathrm { r } _ { c } \right) e ^ { - \left( u _ { c } - \mathrm { r } _ { c } \right) x }$ with $x \geq 0$ . By virtue of the definition $\begin{array} { r } { \mathbb { P } \left[ T _ { c } \leq t ^ { \prime } \right] = \int _ { 0 } ^ { t ^ { \prime } } f _ { T _ { c } } } \end{array}$ (x)dx and after some simple algebraic operations, we get (24). Besides, since tasks are processed on the MEC server with the least load (i.e., the server with the smallest queue length), the minimum queue length $N _ { \mathrm { m } } ( 3 )$ for three connected MEC servers is defined as

$$
\hat { N } _ { \mathrm { m } } ( 3 ) = N _ { \mathrm { m , \hat { i } } } , w h e r e \ i = \arg \operatorname* { m i n } _ { i \in ( 1 , 2 , 3 ) } N _ { \mathrm { m , i } }\tag{26}
$$

where $N _ { \mathrm { m , i } }$ denotes the queue length for the $i ^ { \mathrm { t h } }$ MEC server.

It is known that $N _ { \mathrm { m , i } }$ is a geometric RV with parameter $1 - \rho _ { \mathrm { m } }$ [39], then, we have

$$
\begin{array} { r l } & { \mathbb { P } [ \hat { N } _ { \mathrm { m } } ( 3 ) = \zeta ] = \mathbb { P } [ \hat { N } _ { \mathrm { m } } ( 3 ) \leq \zeta ] - \mathbb { P } [ \hat { N } _ { \mathrm { m } } ( 3 ) \leq \zeta - 1 ] } \\ & { \qquad = ( 1 - \rho _ { \mathrm { m } } ^ { v } ) \rho _ { \mathrm { m } } ^ { v n } , } \end{array}\tag{27}
$$

where $\rho _ { \mathrm { m } } ^ { v n } \triangleq  { \mathrm { r } } _ { \mathrm { m } } / u _ { m }$

In addition, $\begin{array} { r } { T _ { \mathrm { m } } = T _ { \mathrm { m , i } } = \sum _ { j = 1 } ^ { \hat { N } _ { m } ( 3 ) + 1 } \tau _ { \mathrm { m , i , j } } : } \end{array}$ , where $\tau _ { \mathrm { m , \hat { i } } }$ refers to the service time at the $i ^ { \mathrm { { t h } } }$ MEC server for the $j ^ { \mathrm { t h } }$ task. Finally, given $\hat { N } _ { m } ( 3 )$ , P $[ T _ { m } \leq t ^ { \prime } ]$ is given by

$$
\mathbb { P } \left[ T _ { \mathrm { m } } \le t ^ { \prime } \right] = \int _ { 0 } ^ { t ^ { \prime } } f _ { T _ { \mathrm { m } } | \hat { N } _ { m } ( 3 ) = \zeta } ( x ) \mathrm { d } x ,\tag{28}
$$

where $f _ { T _ { \mathrm { m } } | \hat { N } _ { m } ( 3 ) = \zeta } ( x )$ represents the PDF of $T _ { \mathrm { m } }$ for a fixed $\hat { N } _ { m } ( 3 )$ , which is calculated as

$$
\begin{array} { l } { f _ { T _ { \mathrm { m } } | \hat { N } _ { m } ( 3 ) = \zeta } ( x ) = \mathcal { L } ^ { - 1 } \left[ \displaystyle \prod _ { j = 1 } ^ { \zeta + 1 } \mathcal { L } _ { \tau _ { m , \hat { i } , j } } \right] = \mathcal { L } ^ { - 1 } \left[ \left( \frac { u _ { m } } { s + u _ { m } } \right) ^ { \zeta + 1 ^ { - } } \right. } \\ { \displaystyle \left. = \frac { u _ { m } ^ { \zeta + 1 } x ^ { \zeta } e ^ { - u _ { m } x } } { \Gamma ( \zeta + 1 ) } \qquad ( 2 9 ) \qquad \quad \right. } \end{array}
$$

with $x \geq 0$ . Substituting (27) and (29) into (28) and after some elementary calculations, we attain (25).

3) Successful Edge Computing Probability Analysis: Combing (20) and (23), recalling (7), we get the SECP expression in the following theorem.

Theorem 4. The successful edge computing probability for a target computing latency is given by

$$
P _ { \mathrm { s e c p } } \leq P _ { \mathrm { s u p h } } ( t ) P _ { \mathrm { s c p } } ( t ^ { \prime } ) ,\tag{30}
$$

where $P _ { \mathrm { s u p h } } ( t )$ and $P _ { \mathrm { s c p } } ( t ^ { \prime } )$ are given in (20) and (23), respectively.

TABLE I  
PARAMETERS ASSOCIATED WITH EDGE COMPUTING PROBABILITY
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1> $\lambda _ { u }$ </td><td rowspan=1 colspan=1> $\overline { { 1 \sim 2 0 0 / \mathrm { k m } ^ { 2 } } }$ </td><td rowspan=1 colspan=1>p</td><td rowspan=1 colspan=1>[0,1]</td></tr><tr><td rowspan=1 colspan=1> $\lambda _ { e }$ </td><td rowspan=1 colspan=1> $1 \sim 2 0 0 0 / \mathrm { k m } ^ { 2 }$ </td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1> $4 0 { \sqrt { \frac { 2 } { \pi } } }$ </td></tr><tr><td rowspan=1 colspan=1>h</td><td rowspan=1 colspan=1>100m</td><td rowspan=1 colspan=1>a</td><td rowspan=1 colspan=1> $2 . 4 \sim 3 . 6 $ </td></tr><tr><td rowspan=1 colspan=1> $r _ { 0 }$ </td><td rowspan=1 colspan=1> $\frac { 1 } { 2 \sqrt { 2 \lambda _ { u } } }$ </td><td rowspan=1 colspan=1>wo</td><td rowspan=1 colspan=1>1m</td></tr><tr><td rowspan=1 colspan=1> $f _ { \mathrm { m } }$ </td><td rowspan=1 colspan=1>2 GHz</td><td rowspan=1 colspan=1>fe</td><td rowspan=1 colspan=1>5GHz</td></tr><tr><td rowspan=1 colspan=1> $L _ { u }$ </td><td rowspan=1 colspan=1>0.5 Mbits</td><td rowspan=1 colspan=1> $\overline { { C _ { p } } }$ </td><td rowspan=1 colspan=1>330Cycle/Byte</td></tr><tr><td rowspan=1 colspan=1> $u _ { \mathrm { m } }$ </td><td rowspan=1 colspan=1> $\overline { { \frac { 8 f _ { \mathrm { m } } } { C _ { p } L _ { u } } } }$ </td><td rowspan=1 colspan=1> $u _ { \mathrm { c } }$ </td><td rowspan=1 colspan=1> $\frac { 8 f _ { \mathrm { c } } } { C _ { p } L _ { u } }$ </td></tr></table>

## V. SIMULATION RESULTS

This section discusses the numerical outcomes computed from the previously obtained analytical expressions and compares them with results from Monte Carlo simulations. We assume that the speed of the UAV follows a Rayleigh distribution with parameter Î´ (note that in this case, the average speed of the UAV is determined as $\hat { v _ { i } } = \sqrt { \pi / 2 } \delta )$ . Table I provides the main parameters related to the edge computing probability associated with the UAV.

## A. CoMP Handoff Probability

Figure 5 illustrates the cooperative handoff probabilities of a typical UE. Specifically, for the DMM, Fig. 5 presents the numerical results about the lower bound derived in (14). It is indicated that when the UAV density $\lambda _ { u }$ is set to $2 \mathrm { U A V / k m ^ { 2 } }$ the cooperative handoff probability monotonically increases when the parameter rises from $\delta = 2 0 \sqrt { 2 / \pi }$ to $4 0 \sqrt { 2 / \pi }$ (the variation of Î´ effectively reflects changes of average speed of UAVs.). Moreover, with a fixed Î´, the cooperative handoff probability increases with the rise in the density of UAVs. These phenomena can be attributed to the fact that as the speed of the UAV increases or the average cell area decreases, the handoff frequency increases, aligning with expectations.

## B. Successful Uplink Communication Probability

Figure 6 and Fig. 7 separately depict the variation of the SUCP, with and without handoffs, as a function of the SIR threshold (Î³) (in dB) for a typical UE. The variable Ï denotes the probability of connection failure due to handoffs, defined immediately after (5). Observations indicate that across all scenarios, the SUCP decreases with an increase in the SIR threshold yet rises with an increase in the number of antennas M , aligning with prior expectations. Moreover, the simulated SUCP closely matches the theoretical predictions, confirming the effectiveness of the approximate method employed in this study. Further analysis reveals that under conditions with a fixed UE density and antenna number, the SUCP increases with the increased UAV density. On the other hand, with a fixed UAV density and antenna number, the SUCP decreases with increased user density. The former is due to the enhancement of the energy received by UEs as UAV density increases; the latter is attributed to the increased interference received by UEs as the user density increases. Moreover, the cooperative SUCP is lower when $\varsigma = 0 . 8$ compared to when $\varsigma = 0 . 2$ indicating that the system is more sensitive to higher Ï values during handoffs, reducing the SUCP.

Figure 8 illustrates the SUCP of the traditional single BS association scenario in [40]. As a comparison, the SUCP of the traditional regular hexagonal model with three UAVs is also depicted. It is noted that the proposed model outperforms the traditional regular hexagonal model in terms of SUCP. This superiority is attributed to the Delaunay CoMP mechanism, which ensures that the distances between CoMP UAVs and the typical UEs are notably closer to the three nearest nodes than the disordered distances within a traditional hexagonal cell. On the other hand, it also reveals that the proposed schemeâs transmission performance is superior to that of the single BS transmission model. This indicates that the proposed transmission scheme can achieve cooperative power gain compared with the single BS association model.

## C. Successful Computing Probability

Figure 9 illustrates the SCP as a function of parameters p and $p _ { \mathrm { s u p h } }$ . Given a specific SUPH, it is noted that the SCP is maximized for some $p \in [ 0 , 1 ]$ . Additionally, it is observed that when $p$ is small, the SCP increases with $p .$ However, when p is sufficiently large, the SCP decreases with $p .$ The reasons for these results are as follows: if the p value is small, the task is likely to be processed on the MEC server. Since the task arrival rate at the MEC server $\mathrm { r } _ { m }$ decreases with increasing $p ,$ and $\mathbb { P } [ T _ { \mathrm { m e c } } \leq t ^ { \prime } ]$ increases with increasing $p ,$ SCP increases with increasing $p .$ On the other hand, when $p  1$ , task processing has a high probability of occurring in CS. Since the rate $\mathrm { r } _ { c }$ of the mission to CS increases with increasing $p ,$ SCP decreases with increasing $p .$ This indicates that for a given t, some $p \in$ [0, 1] maximizes the SCP.

<!-- image-->  
Fig. 5. The cooperative handoff probability for the DMM model.

<!-- image-->  
Fig. 6. The cooperative SUCP without handoffs for a typical UE.

<!-- image-->  
Fig. 9. The SCP, as a function of $\left( p , p _ { \mathrm { s u p h } } \right)$ with $t ^ { \prime } = 2 ~ \mathrm { m s }$

<!-- image-->  
Fig. 10. The SCP, as a function of p with $t ^ { \prime } \ = \ 2$ ms in the case of $p _ { \mathrm { s u p h } } = 0 . 6$ versus $p _ { \mathrm { s u p h } } = 0 . 8$

<!-- image-->  
Fig. 7. The cooperative SUPH for a typical UE in the case of $\varsigma = 0 . 2$ and $\varsigma = 0 . 8$

<!-- image-->  
Fig. 11. The SECP, as functions of $( p , t ^ { \prime } )$ with $p _ { \mathrm { s u p h } } = 0 . 8 .$

Fig. 12. The SECP, as functions of $\left( p , p _ { \mathrm { s u p h } } \right)$ with $t ^ { \prime } = 2$ ms.  
<!-- image-->  
Fig. 8. The SUCP for a typical UE under the proposed Delaunay offloading model versus the traditional single BS association scenario and the hexagon model with three UAVs average.

Figure 10 compares the SCP versus $p$ in case of $p = 0 . 1$ and $p = 0 . 9$ . Observations reveal that the SCP is higher when the $p$ value is smaller. This phenomenon is because the CS can access all MEC nodes within the CoMP set. Therefore, increasing the probability $p$ of offloading to the CS will increase the task arrival rate of the CS, thereby leading to an increase in computing delay. Conversely, choosing the MEC server for processing (i.e., a lower $p$ value) can increase the SCP, thereby improving the SECP. This is also the main driving factor for introducing the concept of MEC in cooperative UAV networks.

## D. Successful Edge Computing Probability

Finally, in Fig. 11, we comprehensively considered communication and computing performance indicators to assess the overall performance of the SECP. Within this context, we depict the SECP as a function of parameter $p$ and the computing latency threshold $t ^ { \prime } .$ Through analysis, we found that when the parameter $p$ remained constant, SECP showed an increasing trend as the computing latency threshold $t ^ { \prime }$ increased. This phenomenon can be explained by the following theory: Under the given conditions of SUPH, SECP is constrained mainly by the SCP. SCP increases as the computing latency threshold increases. Conversely, when the computation time $t ^ { \check { \prime } }$ is constant, the SECP arrives at its maximum value for a specific $p$ within the interval of 0 to 1. The SECP changes with $p ,$ mirroring that of the SCP with respect to $p .$ This alignment primarily occurs because, under consistent SUPH conditions, the SECP is fundamentally influenced by the SCP. Meanwhile, at lower values of $p ,$ the SCP increases as p increases, whereas at higher values of $p ,$ the SCP decreases as $p$ increases. Consequently, the SCP exhibits a peak value consistent with the findings in Fig. 9.

<!-- image-->

Figure 12 plots the SECP as a function of parameter p and $p _ { \mathrm { s u p h } }$ with fixed $t ^ { \prime } \ = \ 2$ ms. When the value of $p$ is relatively low, it is observed that the SECP increases as SUPH increases. This phenomenon can be attributed to the predominant reliance on MEC servers for task processing during this phase. Specifically, as $p$ increases, the arrival rate of tasks on the MEC server, denoted as $\mathrm { r } _ { m }$ , decreases, while the SCP increases correspondingly. A similar trend is observed when $p$ is higher. Although SCP decreases with an increase in $p ,$ the continuous growth of SUPH ultimately leads to an increase in SECP.

## VI. CONCLUSION

This paper proposes a UAV-assisted MEC cooperative offloading mechanism based on Poisson-Delaunay triangulation. Specifically, the data of each UE is jointly offloaded to three UAVs, forming a triangular cell. Compared with the single UAV scheme, this mechanism significantly enhances the linkâs reliability and improves service quality. Furthermore, a handoff tracking and quantitative evaluation scheme was developed based on the topological characteristics of Delaunay triangulation, demonstrating effective adaptability to complex network topologies. Finally, the SECP was analytically characterized to facilitate the optimal design of the task offloading mechanism. Compared to non-cooperative offloading mechanisms, our proposed model can improve performance by 30% on average. Compared with the conventional regular hexagon scheme that typically includes an average of three serving UAVs, the proposed scheme can achieve a higher SUCP by 20% under an equal handoff probability. The proposed CoMP offloading strategy is anticipated to be applied in airto-ground (A2G) networks to enhance network performance, reduce system latency, and improve user experience.

## ACKNOWLEDGMENT

We would like to thank the anonymous reviewers for their detailed comments and suggestions. This work was partially supported by National Natural Science Foundation of China under Grant No. U23B2004 and 62302510, in part by the China Postdoctoral Science Foundation under Grants GZC20233529, 2024T71181 and 2023M734314, in part by the Natural Science Foundation of Hunan Province under Grant 2023JJ20055, in part by the Hunan Provincial Education Department Project under Grant 24B0296.

## APPENDIX A PROOF OF LEMMA 2

Define $\hat { v } \triangleq \sqrt { Y }$ , where

$$
\begin{array} { c } { { { \cal Y } \triangleq \left( \displaystyle \sum _ { k = 1 } ^ { 3 } v _ { k } \cos \theta _ { k } \right) ^ { 2 } + \left( \displaystyle \sum _ { k = 1 } ^ { 3 } v _ { k } \sin \theta _ { k } \right) ^ { 2 } } } \\ { { = \displaystyle \sum _ { k = 1 } ^ { 3 } v _ { k } ^ { 2 } + \displaystyle \sum _ { k = 1 } ^ { 3 } \displaystyle \sum _ { q = 1 , q \neq k } ^ { 3 } v _ { k } v _ { q } \cos \left( \theta _ { k } - \theta _ { q } \right) . } } \end{array}\tag{31}
$$

Assuming $v _ { k }$ are i.i.d. with mean $\mathbb { E } ( v _ { k } )$ and variance $\mathrm { V a r } ( v _ { k } )$ , the distributions of ÏË is thus derived as follows.

By the central limit theorem, the distribution of $Y$ can be approximated by a Gamma distribution, represented as

$$
f _ { Y } ( y ) = { \frac { y ^ { a - 1 } } { \Gamma ( a ) b ^ { a } } } \exp \left( - { \frac { y } { b } } \right)\tag{32}
$$

with the parameters determined by

$$
a = { \frac { \mathbb { E } ^ { 2 } ( Y ) } { \operatorname { V a r } ( Y ) } } , \ b = { \frac { \operatorname { V a r } ( \mathrm { Y } ) } { \mathbb { E } ( Y ) } } ,\tag{33}
$$

where

$$
\mathbb { E } ( Y ) = 3 \mathbb { E } \left( v _ { k } ^ { 2 } \right)\tag{34}
$$

and

$$
\operatorname { V a r } ( Y ) = 3 \mathbb { E } \left( v _ { i } ^ { 4 } \right) + 3 \left( \mathbb { E } \left( v _ { i } ^ { 2 } \right) \right) ^ { 2 } .\tag{35}
$$

Using (32), the CDF of ÏË can be expressed as

$$
{ \cal F } _ { \hat { v } } ( x ) \triangleq \operatorname* { P r } \left\{ \hat { v } \leq x \right\} = { \cal F } _ { Y } \left( x ^ { 2 } \right) .\tag{36}
$$

By differentiating $F _ { \hat { v } } ( x )$ concerning x and subsequently simplifying the resulting equation, we arrive at the desired (12a).

To derive the PDF of ${ \hat { \theta } } ,$ we employ a method similar to [36, Appendix C] by introducing two auxiliary RVs $\psi _ { k } = \theta _ { k }$ for $k = 1 , 2$ . We then determine the joint PDF for the three RVs ËÎ¸ and $\psi _ { k }$ for $k = 1 , 2$ . Subsequently, we integrate these auxiliary RVs to obtain the PDF of ${ \hat { \theta } } .$ We begin by solving three equations (one for the definition of ËÎ¸ and two introduced by the auxiliary RVs) to derive the $\theta _ { k } \mathrm { { ' s } }$ expressed in terms of ËÎ¸ and the $\psi _ { k } \mathbf { ^ { \prime } s }$ . Ultimately, we arrive at two solution sets:

$$
( 1 ) \left\{ \begin{array} { l l } { \theta _ { k } = \psi _ { k } , } & { k = 1 , 2 ; } \\ { \theta _ { 3 } = \arctan \left( \frac { - A \cos ( \hat { \theta } ) + A ^ { \prime } \sin ( \hat { \theta } ) } { A \sin ( \hat { \theta } ) + A ^ { \prime } \cos ( \hat { \theta } ) } \right) \triangleq \psi _ { 3 a } , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.
$$

$$
( 2 ) \left\{ \begin{array} { l l } { \theta _ { k } = \psi _ { k } , } & { k = 1 , 2 ; } \\ { \theta _ { 3 } = \arctan \left( \frac { - A \cos ( \hat { \theta } ) - A ^ { \prime } \sin ( \hat { \theta } ) } { A \sin ( \hat { \theta } ) - A ^ { \prime } \cos ( \hat { \theta } ) } \right) \triangleq \psi _ { 3 b } , } & { \mathrm { o t h e r w i s e , } } \end{array} \right.
$$

where ${ \mathcal { A } } \triangleq \textstyle \sum _ { k = 1 } ^ { 2 }$ Ïk sin $\left( \psi _ { k } - { \hat { \theta } } \right)$ and ${ \mathcal { A } } ^ { \prime } \triangleq { \sqrt { v _ { 3 } ^ { 2 } - A ^ { 2 } } }$ Calculating the determinant of the Jacobian matrix J, i.e., $\begin{array} { r } { | J | = \left| \frac { \partial \theta _ { 3 } } { \partial \hat { \theta } } \right| } \end{array}$ for both solution sets. After performing some algebraic manipulations, we attain

$$
| J | \bigg | _ { \theta _ { 3 } = \psi _ { 3 a } } + | J | \bigg | _ { \theta _ { 3 } = \psi _ { 3 b } } = 2 .\tag{37}
$$

As $\theta _ { k } , k = 1 , 2 ,$ is uniformly distribution in $[ 0 , 2 \pi )$ , the joint distribution of ËÎ¸ and $\psi _ { k } , k = 1 , 2$ , can be written as

$$
f _ { { \hat { \theta } } , \psi } \left( { \hat { \theta } } , \psi \right) = \frac { 1 } { 4 \pi ^ { 3 } } .\tag{38}
$$

Integrating (38) with respect to $\psi _ { k } , ~ k ~ = ~ 1 , 2$ , we get the distribution of ${ \hat { \theta } } ,$ which is given by $f _ { \hat { \Theta } } ( \hat { \theta } ) ~ = ~ 1 / \pi$ , for all $\hat { \theta } \in \left[ - \frac { \pi } { 2 } , \frac { \pi } { 2 } \right)$ . Accordingly, we have $f _ { \hat { \Theta } } ( \hat { \theta } ) = 1 / 2 \pi$ , for all $\hat { \theta } \in [ - \pi , \pi )$ , which is obviously independent of the speed distribution $v _ { k }$ . The proof is completed.

## APPENDIX B PROOF OF THEOREM 3

According to the uplink outage probability defined in (16), we have

$$
\begin{array} { r l r } {  { p _ { \mathrm { o , u l } } = \mathbb { P } [ \operatorname* { m a x } _ { i \in \{ 1 , 2 , 3 \} } \mathrm { S I R } _ { i 0 , \mathrm { u l } } \le \gamma ] = \prod _ { i = 1 } ^ { 3 } \mathbb { P } [ \mathrm { S I R } _ { i 0 , \mathrm { u l } } < \gamma ] } } \\ & { } & { \ = \prod _ { i = 1 } ^ { 3 } ( 1 - \mathbb { P } _ { c i , \mathrm { u l } } ) , \quad \quad ( 3 } \end{array}\tag{9}
$$

where $\mathbb { P } _ { c i , \mathrm { u l } } \triangleq \mathbb { P } \left[ \mathrm { S I R } _ { i 0 , \mathrm { u l } } \geq \gamma \right]$ , it can be calculated as

(40)

$$
= \int _ { 0 < w _ { i } \infty } f _ { w _ { i } } ( w _ { i } ) \sum _ { m = 0 } ^ { M - 1 } \frac { ( - 1 ) ^ { m } } { m ! } u _ { i 0 } ^ { \alpha m } \gamma ^ { m } \mathcal { L } _ { I } ^ { m } \left( u _ { i 0 } ^ { \alpha } \gamma \right) \mathrm { d } w _ { i }\tag{41}
$$

where (40) follows from the gamma distribution of $. g _ { i 0 }$ , and (41) comes from the eqality $\begin{array} { r } { \bar { \Gamma ( v , x ) } = \Gamma ( v ) \sum _ { i = 0 } ^ { v - 1 } \frac { x ^ { i } } { i ! } e ^ { - x } } \end{array}$

With (41), (39) can be further calculated as

$$
\begin{array} { r l r } { \displaystyle { p _ { \mathrm { o , u l } } = \prod _ { k = 1 } ^ { 3 } \left( 1 - \int _ { 0 < w _ { k } \leq \infty } \sum _ { m = 0 } ^ { M - 1 } \frac { ( - 1 ) ^ { m } } { m ! } u _ { i 0 } ^ { \alpha m } \gamma ^ { m } \mathcal { L } _ { I } ^ { m } \left( u _ { k 0 } ^ { \alpha } \gamma \right) \right. } } \\ { \displaystyle { \left. \qquad \times f _ { w _ { k } } ( w _ { k } ) \mathrm { d } w _ { k } \right) } , } & { } & { \displaystyle { ( 4 . \qquad } } \end{array}\tag{2}
$$

where $f _ { w _ { k } } ( w _ { k } )$ is given by (17). Refer to the derivation of [33, Eq. $( 7 1 ) ] , L _ { I } ( s )$ can be explicitly computed as (18). Using the relation shown in (16) yields the final result (19).

## REFERENCES

[1] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Communications Surveys & Tutorials, vol. 21, no. 3, pp. 2334â2360, 2019.

[2] Y.-H. Hsu and R.-H. Gau, âReinforcement learning-based collision avoidance and optimal trajectory planning in UAV communication networks,â IEEE Transactions on Mobile Computing, vol. 21, no. 1, pp. 306â320, 2022.

[3] H. Lee, B. Lee, H. Yang, J. Kim, S. Kim, W. Shin, B. Shim, and H. V. Poor, âTowards 6G hyper-connectivity: Vision, challenges, and key enabling technologies,â Journal of Communications and Networks, vol. 25, no. 3, pp. 344â354, 2023.

[4] B. Hazarika, K. Singh, C.-P. Li, A. Schmeink, and K. F. Tsang, âRadit: Resource allocation in digital twin-driven UAV-aided internet of vehicle networks,â IEEE Journal on Selected Areas in Communications, vol. 41, no. 11, pp. 3369â3385, 2023.

[5] Z. Hu, F. Zeng, Z. Xiao, B. Fu, H. Jiang, H. Xiong, Y. Zhu, and M. Alazab, âJoint resources allocation and 3D trajectory optimization for UAV-enabled space-air-ground integrated networks,â IEEE Transactions on Vehicular Technology, vol. 72, no. 11, pp. 14 214â14 229, 2023.

[6] H. Hu, Z. Chen, F. Zhou, Z. Han, and H. Zhu, âJoint resource and trajectory optimization for heterogeneous-UAVs enabled aerial-ground cooperative computing networks,â IEEE Transactions on Vehicular Technology, vol. 72, no. 7, pp. 8812â8826, 2023.

[7] M. Salehi and E. Hossain, âHandover rate and sojourn time analysis in mobile drone-assisted cellular networks,â IEEE Wireless Communications Letters, vol. 10, no. 2, pp. 392â395, 2021.

[8] F. A. Khan, H. N. Qureshi, A. Imran, and H. Refai, âHandover probability analysis in multi-tier aerial networks at varying altitudes,â in ICC 2023 - IEEE International Conference on Communications, 2023, pp. 2890â2895.

[9] Z. Yang, S. Bi, and Y.-J. A. Zhang, âOnline trajectory and resource optimization for stochastic UAV-enabled MEC systems,â IEEE Transactions on Wireless Communications, vol. 21, no. 7, pp. 5629â5643, 2022.

[10] B. Xu, Z. Kuang, J. Gao, L. Zhao, and C. Wu, âJoint offloading decision and trajectory design for UAV-enabled edge computing with task dependency,â IEEE Transactions on Wireless Communications, vol. 22, no. 8, pp. 5043â5055, 2023.

[11] Z. Yang, S. Bi, and Y.-J. A. Zhang, âDynamic offloading and trajectory control for UAV-enabled mobile edge computing system with energy harvesting devices,â IEEE Transactions on Wireless Communications, vol. 21, no. 12, pp. 10 515â10 528, 2022.

[12] W. Mao, K. Xiong, Y. Lu, P. Fan, and Z. Ding, âEnergy consumption minimization in secure multi-antenna UAV-assisted MEC networks with channel uncertainty,â IEEE Transactions on Wireless Communications, vol. 22, no. 11, pp. 7185â7200, 2023.

[13] B. Liu, Y. Wan, F. Zhou, Q. Wu, and R. Q. Hu, âResource allocation and trajectory design for MISO UAV-assisted MEC networks,â IEEE Transactions on Vehicular Technology, vol. 71, no. 5, pp. 4933â4948, 2022.

[14] Y. Qu, H. Dai, H. Wang, C. Dong, F. Wu, S. Guo, and Q. Wu, âService provisioning for UAV-enabled mobile edge computing,â IEEE Journal on Selected Areas in Communications, vol. 39, no. 11, pp. 3287â3305, 2021.

[15] G. Zheng, C. Xu, M. Wen, and X. Zhao, âService caching based aerial cooperative computing and resource allocation in multi-UAV enabled MEC systems,â IEEE Transactions on Vehicular Technology, vol. 71, no. 10, pp. 10 934â10 947, 2022.

[16] W. Liu, B. Li, W. Xie, Y. Dai, and Z. Fei, âEnergy efficient computation offloading in aerial edge networks with multi-agent cooperation,â IEEE Transactions on Wireless Communications, vol. 22, no. 9, pp. 5725â 5739, 2023.

[17] Y. Liu, S. Xie, and Y. Zhang, âCooperative offloading and resource management for UAV-enabled mobile edge computing in power iot system,â IEEE Transactions on Vehicular Technology, vol. 69, no. 10, pp. 12 229â12 239, 2020.

[18] C. Li, Y. Gan, Y. Zhang, and Y. Luo, âA cooperative computation offloading strategy with on-demand deployment of multi-UAVs in UAVaided mobile edge computing,â IEEE Transactions on Network and Service Management, vol. 21, no. 2, pp. 2095â2110, 2024.

[19] H. Zhang, W. Huang, and Y. Liu, âHandover probability analysis of anchor-based multi-connectivity in 5g user-centric network,â IEEE Wireless Communications Letters, vol. 8, no. 2, pp. 396â399, 2019.

[20] S. Sadr and R. S. Adve, âHandoff rate and coverage analysis in multi-tier heterogeneous networks,â IEEE Transactions on Wireless Communications, vol. 14, no. 5, pp. 2626â2638, 2015.

[21] R. Amer, W. Saad, and N. Marchetti, âMobility in the sky: Performance and mobility analysis for cellular-connected UAVs,â IEEE Transactions on Communications, vol. 68, no. 5, pp. 3229â3246, 2020.

[22] H. Wei and H. Zhang, âAn equivalent model for handover probability analysis of IRS-aided networks,â IEEE Transactions on Vehicular Technology, vol. 72, no. 10, pp. 13 770â13 774, 2023.

[23] S.-Y. Hsueh and K.-H. Liu, âAn equivalent analysis for handoff probability in heterogeneous cellular networks,â IEEE Communications Letters, vol. 21, no. 6, pp. 1405â1408, 2017.

[24] T. M. Duong and S. Kwon, âVertical handover analysis for randomly deployed small cells in heterogeneous networks,â IEEE Transactions on Wireless Communications, vol. 19, no. 4, pp. 2282â2292, 2020.

[25] H. Wei and H. Zhang, âEquivalent modeling and analysis of handover process in k-tier UAV networks,â IEEE Transactions on Wireless Communications, vol. 22, no. 12, pp. 9658â9671, Dec 2023.

[26] âTime-varying boundary modeling and handover analysis of UAV-assisted networks with fading,â IEEE Transactions on Wireless Communications, vol. 23, no. 7, pp. 7552â7565, July 2024.

[27] L. Lai, F.-C. Zheng, and J. Luo, âFlight direction-based handover in cellular-connected UAV communications,â IEEE Transactions on Vehicular Technology, pp. 1â6, 2024.

[28] F. Wang, J. Xu, X. Wang, and S. Cui, âJoint offloading and computing optimization in wireless powered mobile-edge computing systems,â IEEE Transactions on Wireless Communications, vol. 17, no. 3, pp. 1784â1797, 2018.

[29] M. Li, N. Cheng, J. Gao, Y. Wang, L. Zhao, and X. Shen, âEnergyefficient UAV-assisted mobile edge computing: Resource allocation and trajectory optimization,â IEEE Transactions on Vehicular Technology, vol. 69, no. 3, pp. 3424â3438, 2020.

[30] J. Zhou, D. Tian, Y. Wang, Z. Sheng, X. Duan, and V. C. Leung, âReliability-optimal cooperative communication and computing in connected vehicle systems,â IEEE Transactions on Mobile Computing, vol. 19, no. 5, pp. 1216â1232, 2020.

[31] M. Banagar and H. S. Dhillon, â3GPP-inspired stochastic geometrybased mobility model for a drone cellular network,â in 2019 IEEE Global Commun. Conf. (GLOBECOM), Dec. 2019, pp. 1â6.

[32] M. Xia and S. AÂ¨Ä±ssa, âUnified analytical volume distribution of Poisson-Delaunay simplex and its application to coordinated multi-point transmission,â IEEE Trans. Wireless Commun., vol. 17, no. 7, pp. 4912â4921, Jul. 2018.

[33] Y. Li, M. Xia, and S. AÂ¨Ä±ssa, âCoordinated multi-point transmission: A Poisson-Delaunay triangulation based approach,â IEEE Trans. Wireless Commun., vol. 19, no. 5, pp. 2946â2959, May 2020.

[34] M. Guevara, B. Lubin, and B. C. Lee, âNavigating heterogeneous processors with market mechanisms,â in 2013 IEEE 19th International Symposium on High Performance Computer Architecture (HPCA), 2013, pp. 95â106.

[35] J. Bi, Z. Zhu, R. Tian, and Q. Wang, âDynamic provisioning modeling for virtualized multi-tier applications in cloud data center,â in 2010 IEEE 3rd International Conference on Cloud Computing, 2010, pp. 370â377.

[36] M. Banagar and H. S. Dhillon, âPerformance characterization of canonical mobility models in drone cellular networks,â IEEE Trans. Wireless Commun., vol. 19, no. 7, pp. 4994â5009, Jul. 2020.

[37] Y. Li and M. Xia, âGround-to-air communications beyond 5G: A coordinated multipoint transmission based on Poisson-Delaunay triangulation,â IEEE Transactions on Wireless Communications, vol. 22, no. 3, pp. 1841â1854, 2023.

[38] D. Moltchanov, âDistance distributions in random networks,â Ad Hoc Netw., vol. 10, no. 6, pp. 1146â1166, Mar. 2012.

[39] L. Kleinrock, Queueing Systems: Theory, vol. 1. New York, NY: USA: Wiley, 1975.

[40] J. G. Andrews, F. Baccelli, and R. K. Ganti, âA tractable approach to coverage and rate in cellular networks,â IEEE Transactions on Communications, vol. 59, no. 11, pp. 3122â3134, 2011.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_1.png|page_5_img_1]]
2. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_2.png|page_5_img_2]]
3. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_3.jpeg|page_5_img_3]]
4. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_4.png|page_5_img_4]]
5. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_5.png|page_5_img_5]]
6. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_6.png|page_5_img_6]]
7. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_7.png|page_5_img_7]]
8. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_8.png|page_5_img_8]]
9. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_9.png|page_5_img_9]]
10. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_5_img_10.png|page_5_img_10]]
11. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_1.png|page_8_img_1]]
12. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_2.jpeg|page_8_img_2]]
13. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_3.png|page_8_img_3]]
14. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_4.png|page_8_img_4]]
15. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_5.png|page_8_img_5]]
16. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_6.jpeg|page_8_img_6]]
17. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_7.png|page_8_img_7]]
18. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_8.png|page_8_img_8]]
19. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_9.png|page_8_img_9]]
20. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_10.jpeg|page_8_img_10]]
21. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_11.png|page_8_img_11]]
22. [[../extracted_images/Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry/page_8_img_12.png|page_8_img_12]]

---

