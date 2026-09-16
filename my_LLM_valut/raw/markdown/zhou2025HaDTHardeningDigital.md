# HaDT: Hardening Digital Twins for UAVs-Based Industrial Logistics Distribution Systems

Longyu Zhou1, Supeng Leng2, and Tony Q.S. Quek1

1Information Systems Technology and Design, Singapore University of Technology and Design, Singapore

2School of Information & Communication Engineering, University of Electronic Science & Technology of China, China

Emails: {longyu_zhou, tonyquek}@sutd.edu.sg, spleng@uestc.edu.cn

Abstractâ With the development of network autonomy, Unmanned Aerial Vehicles (UAV) applications are attractive to serve intelligent logistics with the advantages of miniaturization and flexibility. It, however, is difficult to implement accurate UAV control in complex distribution scenarios. In this context, Digital Twins (DT) is a potential tool to assist UAVs in acquiring feasible cooperative distribution decisions with the ability of imitation and derivation. Nonetheless, it is challenging to perform real-time DT implementations due to the limited computing resources of UAVs. To address the mentioned problems, we achieve a Hardened DT (HaDT) framework, operating at the edge side, to enable a double DT cooperation manner for efficient resource scheduling and path planning. The resource scheduling model can implement the integration of computing and communication resources among UAVs to acquire feasible cooperative logistics distribution decisions. The decisions can drive the path planning model to derive positions and velocities of UAVs for low-latency logistics distribution performance with energy saving. Experiment results demonstrate the efficiency of our HaDT framework. Compared to state-of-the-art logistics distribution solutions, our solution reduces the distribution latency by 63.9% while improving the successful distribution ratio by 10.9%.

Index TermsâDigital twins, UAVs, intelligent logistics, resource scheduling.

## I. INTRODUCTION

Inspired by the development of cyber-physical systems, the European Commission has a vision to explore the implementation of the fifth industrial revolution (industry 5.0) in leaps and bounds [1]â[3]. The revolution provides high-efficiency automatic services for the intelligent manufacturing industry such as intelligent logistics systems. In addition, with the rapid promotion of the fifth generation wireless system (5G), the low-altitude network represented by Unmanned Aerial Vehicles (UAVs) has ability to contribute to the low-carbon industry 5.0 [4], [5].

Despite of the advantages of flexibility of UAVs, we still need to solve several challenges for high-efficiency logistics distributions shown as follows.

1) It is difficult to implement long-distance logistics distribution missions by deploying multiple UAVs due to limited battery energy and low-cooperation performance.

2) The traditional cloud automation paradigm may cause physical collisions among UAVs to reduce the successful distribution ratio in complex logistics scenarios due to remote transmission distances.

3) The remote transmission can lead to out-of-date distribution decisions to reduce efficiency of UAV cooperation distributions.

To address the mentioned challenges, the authors in [6], [7] propose a flexible terminal-edge automation paradigm. It can implement high-efficiency resource integration to achieve lowlatency distribution services in different logistics scenarios. Unfortunately, compared to the cloud automation paradigm, it exposes the problem of limited computing resources to cause high UAV implementation latency. To improve the logistics distribution time efficiency, the authors in [8] proposed a threestage based distribution optimization algorithm. In the first stage, the author employed a statistical method to analyze the pattern of real-time delivery rate. Subsequently, a machine learning model was used to capture the underlying correlations between time efficiency and potential impacting factors. Finally, an explainable machine learning technique was used to quantify the contributions of the impacting factors to the time efficiency. However, it may be inefficient to implement dynamic optimization of distribution paths for some urgent situations with high computing complexity. To simplify the complicated distribution implementation process, the authors in [9] presented a Predict-Then-Optimize Couriers Allocation (PTOCA) framework. Explicitly, a resource-aware prediction module was designed in the prediction stage to implement feasible resource scheduling. Then, a priority ranking module was designed to acquire a fair resource scheduling result. Finally, a task allocation module was designed to model the dynamic distribution environment using a Gated Recurrent Unit (GRU) network in the optimization stage. It may be challenging to deploy the algorithm to large-scale logistics scenarios with undetermined impacting factors.

The issue motivates us to use the attractive Digital Twins (DT) technology where we can build a mapping of the physical distribution scenario [10], [11]. The mapping can enable edge servers to construct a virtual space to derive feasible logistics distribution decisions. However, UAVs may need to implement frequent information exchange to ensure cooperative logistics distributions. The DT should be multi-functional with joint imitations for high-efficiency resource scheduling of communication and computing and UAV path planning.

Based on the above discussions, we propose a Hardened DT (HaDT) framework to achieve real-time and accurate logistics distributions in this paper. We deploy multiple UAVs with small-sized base stations as edge UAVs. The edge UAVs fly in different airspace to manage different UAVs. The edge UAVs can first imitate to derive efficient resource scheduling of UAVs. We then use the derivation results to implement path planning considering low distribution latency and flight energy consumption based on logistics information. The main contributions are summarized as follows.

â¢ We propose a Hardened DT (HaDT) logistics distribution framework. Different from the existing DT-based logistics distribution systems, our HaDT can build a double DT cooperation pattern. It can derive feasible cooperative distribution decisions by jointly deriving resource scheduling, positions, and velocities of UAVs based on a terminal-edge cooperation manner. In addition, our HaDT can achieve cross-layered computing resource cooperation. It can also integrate computing and communication resources among UAVs to efficiently guarantee real-time and accurate logistics distribution with the improvement of resource utilization.

â¢ To construct accurate HaDT models, we propose a multi-modal learning-based model acquisition algorithm. Unlike conventional AI training with high computing latency, our algorithm can reshape data structures to perform customized DT constructions using a lightweight attention mechanism. We can acquire a resource scheduling twin model and a path planning twin model simultaneously through accurate multi-resource data analysis using a data compression method. In this case, our HaDT can ensure low-energy logistics distributions in real time with the double DT cooperation manner.

â¢ We then propose a HaDT-based logistics distribution algorithm for real-time logistics distributions. Unlike the existing path planning methods with high iteration latency, our algorithm can first flexibly integrate computing and communication resources of UAVs to assist UAVs in find feasible cooperators. In addition, our algorithm can narrow the path exploration areas through a lowfrequency data exchanges with the cooperators. It can assist UAVs in exploring optimal distribution paths to further reduce the distribution latency.

â¢ We use the Gazebo, a system simulation software, to verify the validation of our solution. Under different numbers of UAVs and distribution missions, the experiment results demonstrate that our HaDT solution can significantly reduce the distribution latency by 63.9% while improving the successful distribution ratio by 10.9% on average compared to the state-of-the-art logistics solutions.

The rest of this paper is organized as follows. Section II introduces the HaDT framework and formulate the optimization model. We represent the corresponding algorithms supporting the framework in Section III. Section IV provides the system evaluation results. Finally, Section V concludes this paper.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, we propose a Hardened DT (HaDT) framework to serve the intelligent logistics scenarios.

In the intelligent logistics scenario, we can deploy multiple UAVs with computing-intensive base stations in different air areas. These UAVs can serve as edge UAVs to manage logistic UAVs flying in their areas. The edge UAVs are indexed by $\mathcal { N } = \{ 1 , 2 , \cdots , N \}$ where edge UAV n can provide sufficient computing resources for high-efficiency logistic missions with multiple logistic UAVs. The logistic UAVs (The âlogistics UAVsâ and âUAVsâ are exchanged for simplify in the following sections.) are indexed by $\mathcal { M } = \{ 1 , 2 , \cdots , M \}$ . The set of logistic packages (missions) is defined as ${ \mathcal { K } } = \{ 1 , 2 , \cdots , K \}$

In Fig. 1, Our HaDT introduces the DT technology to assist UAVs in exploring optimal distribution paths through accurate imitation and derivation with two kinds of DT models: a resource scheduling twin model and a path planning twin model. we can strengthen the DT derivation performance with sufficient computing resources of edge UAVs for efficient path planning of UAVs with our proposed DT cooperation manner. It not only improves the time of logistic distribution but also can augment the scalability of our HaDT framework for diverse logistic scenarios.

Edge UAVs can provide efficient bandwidth resources to implement data transmission for data processing by constructing DT models. The DT implementation results are distributed to UAVs to implement cooperative logistics distributions with feasible distribution paths. We can implement the distribution missions sequentially with DT model acquisition and cooperative path planning. We implement the description of the HaDT framework based on the mission orchestration. We provide details of our HaDT as follows.

## A. DT Model Acquisition

The UAVs can use onboard sensors (camera, ultrasonic, and depth vision sensor) to obtain distribution environment information using a cooperative sensing method [12]. It can instruct logistic UAVs to dynamically adjust sensing postures and positions. The neighbor status can be gained through information exchange among UAVs. For UAV i, we use an accumulative average method to formulate the communication latency model for a high-efficiency data transmission:

$$
t _ { \mathrm { c o m m } } = \operatorname* { l i m } _ { T  \infty } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \frac { \frac { \sum _ { j = 1 } ^ { N _ { i } } G _ { i } } { r _ { i , j } } } { [ \sum _ { i = 1 } ^ { N _ { i } } y _ { i , j } ] ^ { * } } \leq T _ { i , c } ,\tag{1}
$$

where $[ y ] ^ { * } = \operatorname* { m a x } \{ 1 , y \} ; G _ { i }$ is the data size of UAV i for information exchanges; $T _ { i , c }$ is the maximal acceptable communication latency for information exchanges. With the aid of the powerful computing ability of edge UAVs, we can build a virtual space where edge UAVs can train the information to obtain customized DT models using our proposed multi-modal learning-based model acquisition algorithm.

Based on this, we can construct two kinds of DT models: the Resource Scheduling Twin (RST) model and the Path

<!-- image-->  
Fig. 1. Illustration of our proposed HaDT framework.

Planning Twin (PPT) model. The RST model focuses on performance improvement of resource utilization by deriving the changes in physical environments (including buildings and surrounding neighbors). It can also enable UAVs to implement information exchanges among neighbors. The integration of communication and computing can efficiently ensure realtime logistic distribution. With the resource integration, we use the Graphics Processing Unit (GPU) to accelerate the Central Processing Unit (CPU)-based data process. We assume edge UAVs process Î· bytes of data. The GPU processes Î·1 bytes of data, and the CPU processes $\eta _ { 2 }$ bytes of data, where $\eta _ { 1 } + \eta _ { 2 } = \eta$ . The GPU processing time is formulated as $\begin{array} { r } { t _ { g } = \operatorname* { m a x } \{ \frac { \eta _ { 1 } } { \phi } , \frac { \chi } { \beta } \} } \end{array}$ [13], where $\phi$ is the bandwidth of GPU memory (bytes/s); Ï is the number of GPU runs; $\beta$ is the number of GPU blocks. With a sequential implementation manner, we formulate the CPU processing time as [14]

$$
t _ { u } = \sum _ { c = 1 } ^ { \eta _ { 2 } } \frac { 1 } { f _ { c } } ,\tag{2}
$$

where $f _ { c }$ is the frequency of CPU.

Based on this, we can acquire the RST model DTRS which is represented as $\mathrm { D T } _ { \mathrm { R S } } ~ = ~ \{ f _ { e , e } , f _ { e , d } , \mathcal { F } , B , \mathcal { R } \}$ , where $f _ { e , e }$ and $f _ { e , d }$ are the external frequency and frequency doubling of edge UAVs, respectively. $\mathcal { F } = [ f _ { 1 } , f _ { 2 } , \cdot \cdot \cdot , f _ { M } ]$ is a vector to denote frequencies of Central Processing Unit (CPU) of UAVs; $\boldsymbol { B } = [ B _ { 1 } , B _ { 2 } , \cdots , B _ { M } ]$ is a vector to present the set of assigned bandwidths for all the UAVs; R is an matrix to denote the transmission rate between any two UAVs with $\mathcal { R } _ { i , j } ~ = ~ r _ { i , j }$ . Based on the derivation result of $\mathrm { D T } _ { \mathrm { R S } }$ , the PPT model is formulated as $\mathrm { D T _ { P P } } ~ = ~ \{ \mathcal { K } , \mathcal { S } , \mathcal { D } , \mathcal { E } \}$ , where ${ \cal K } = [ 1 , 2 , \cdots , K ]$ is a vector that denotes all the logistics missions; $\boldsymbol { S } = [ S _ { 1 } , S _ { 2 } , \cdots , S _ { M } ]$ is the status of all the UAVs where, for each $\mathrm { U A V \ } i , S _ { i } = \{ p _ { i } , v _ { i } , a _ { i } \}$ . The three elements represent UAV iâs position, velocity, and posture, respectively. D is an matrix of physical distances where $\mathcal { D } _ { i , j } = d _ { i , j }$ for UAV i and $j . ~ { \mathcal { E } } = [ E _ { 1 } , E _ { 2 } , \cdot \cdot \cdot ~ , E _ { M } ]$ is a vector where $E _ { i }$ denotes the available energy of UAV i. It can continue to derive feasible distribution paths with logistics information. We can use the two DT models to implement customized logistics services through resource integration (details shown in Section III-A).

## B. Cooperative Path Planning

We first propose an Integrated Communication and Computing (ICC) algorithm to achieve accurate resource scheduling derivation in the virtual space. It can implement trajectory derivation of neighbors to plan feasible distribution paths. The computation results are transmitted to neighbor UAVs for cooperative distributions. In this case, we can integrate communication and computing resources of UAVs to perform accurate and real-time logistics distributions (details shown in Section III-B). With the resource scheduling, we can efficiently use the available resources of UAVs to explore feasible pathplanning decisions. In this case, we formulate the flight energy consumption within a time t (second) for UAV i:

$$
E _ { i } = ( P _ { i , B } + P _ { i , b } \vartheta + P _ { i , \mathrm { i r } } + P _ { i , \mathrm { c o } } ) \times t ,\tag{3}
$$

where $P _ { i , B }$ is the Back EMF loss; $P _ { i , b }$ is the brushless motor power; Ï is the number of brushless motors (namely, the number of blades); $P _ { i , \mathrm { i r } }$ is the iron loss; $P _ { i , \mathrm { c o } }$ is the cooper loss. We adjust the energy consumption percentage Î¹ to ensure a smooth logistic distribution:

$$
\iota = ( 1 - \frac { E _ { i , \mathrm { b u } } - E _ { i } } { E _ { i , \mathrm { b u } } } ) \geq \iota _ { \operatorname* { m i n } } ,\tag{4}
$$

where $E _ { i , \mathrm { b u } } ~ = ~ V _ { i , \mathrm { b u } } \times C _ { i , \mathrm { b u } }$ is the maximal energy budget of UAV i; $V _ { i , \mathrm { b u } }$ and $C _ { i , \mathrm { b u } }$ are voltage supply of battery (V) and capacity of battery (Ah), respectively. $\iota _ { \mathrm { m i n } }$ is the minimal residual energy to ensure smoothly cooperative distributions.

To make the PPT model to derive low-latency distribution paths with low-energy consumption in the virtual space, we propose a Particle Swarm Optimization-based distribution Path Planning (PSO-PP) algorithm. Unlike the traditional PSO algorithms [15], our algorithm can enable particles to simultaneously explore feasible paths from two dimensions of velocity and position. It can assist UAVs in acquiring accurate distribution paths. On the other hand, it can implement directional exploration to narrow the exploration area for real-time executions based on logistics information and environment estimation (details shown in Section III-C).

## C. Problem Formulation

Based on the HaDT framework, we invoke the Lyapunov methodology to formulate the optimization model with the consideration of cooperative resource scheduling:

$$
P 1 : \operatorname* { m i n } \left\{ \operatorname* { l i m } _ { T \to \infty } \frac { 1 } { T } \sum _ { t = 0 } ^ { T } \bigg [ \sum _ { i = 1 } ^ { M } \sum _ { k = 1 } ^ { K } \Delta t _ { i , k } \bigg ] \right\} ,\tag{5}
$$

$$
\mathrm { s . t . } \left\{ \begin{array} { r l } & { C 1 : t _ { g } + t _ { u } + t _ { \mathrm { c o m m } } \leq t _ { i , k } , \forall k \in \mathcal { K } } \\ & { C 2 : ( 1 ) , ( 4 ) . } \end{array} \right.
$$

where $\Delta X$ denotes the difference between the real backlog and the virtual backlog [16]. Explicitly, $\Delta t _ { i , k } = L _ { 1 , i , k } - L _ { 2 , i , k } ,$ where $L _ { 1 , i , k }$ and $L _ { 2 , i , k }$ are the actual distribution time and expected distribution time. We push $L _ { 1 , i , k }$ to approach $L _ { 2 , i , k }$ for real-time distributions. In C2, (1) ensures low-latency communications during cooperation; (4) guarantees the smooth distributions with feasible path planning decisions. It can facilitate UAVs to achieve the distribution mission for a high successful distribution ratio.

## III. HADT-BASED LOGISTICS DISTRIBUTION ALGORITHM

In this section, we decouple the objective function into three sub-problems with the corresponding three algorithms for clear descriptions.

## A. Construction of DT Models

Considering the data heterogeneity, we propose a multimodal learning-based model acquisition algorithm. As shown in Fig. 2, firstly, the heterogeneous data (contents, images, and videos) can be represented by a tensor Env = [EnvC, EnvI, EnvV ], where the three elements denote the content information, image information, and the video information, respectively. Our algorithm can enable to obtain the key data tensor $\mathcal { K } _ { \mathrm { E n v } }$ with a model-1 Khatri-Rao product:

$$
K _ { \mathrm { E n v } } { } ^ { i } = \mathrm { E n v } ^ { i } \odot _ { 1 } \mathrm { E n v } , i \in \{ 1 , 2 , 3 \} .\tag{6}
$$

With the key features, our algorithm can extract customized information from the heterogeneous data to construct DT models using an attention mechanism. In this case, our algorithm can implement a flat data processing by compressing dimensions with a reshape function freshape [17]:

$$
\rho _ { \mathrm { E n v } } = f _ { \mathrm { r e s h a p e } } \Big ( \big ( \mathrm { E n v } ^ { 1 } \xi _ { 1 } \big ) \odot _ { 1 } \big ( \mathrm { E n v } ^ { 2 } \xi _ { 2 } \big ) \odot \big ( \mathrm { E n v } ^ { 3 } \xi _ { 3 } \big ) \Big ) ,\tag{7}
$$

where $\xi _ { 1 } , \xi _ { 2 } ,$ , and $\xi _ { 3 }$ are linear transformation matrices. With the flat physical information, we can implement the attention mechanism with an attention core matrix and a pooling matrix. The attention core matrix $\rho _ { \mathrm { E n v } , K }$ is formulated with the Hadamard product:

$$
\rho _ { \mathrm { E n v } , \mathcal { K } } ^ { i } = \mathrm { E n v } ^ { i } \circ \mathcal { K } ^ { i } .\tag{8}
$$

The attention core matrix is used to explore relations among different kinds of data through information passing. The passing way is achieved by a pooling operation. The attention pooling matrix is deduced as

$$
M _ { \mathrm { E n v } \ K } ^ { i } = f _ { p } ( \rho _ { \mathrm { E n v } , \ K } ^ { i } ( s , w , r ) ) ,\tag{9}
$$

where $f _ { p }$ is a pooling function for information passing; $1 \leq$ $s \leq S , 1 \leq w \leq W$ , and $1 \leq r \leq R . \ S ,$ W , and R are the dimensions of EnvC, EnvI, and $\mathrm { E n v } _ { V }$ , respectively. We can acquire corresponding customized attention tensors $\mathrm { { A t } _ { R S } }$ and $\mathbf { A t } _ { \mathrm { P P } }$ when the information passing process finishes:

$$
\mathrm { A t } _ { \mathrm { R S } } = f _ { \mathrm { D T } _ { R S } } \Big ( \prod _ { i } \rho _ { \mathrm { E n v } , \kappa } { } ^ { i } \varsigma _ { i } M _ { \mathrm { E n v } \kappa } ^ { i } \Big ) ,\tag{10}
$$

$$
\mathrm { A t } _ { \mathrm { P P } } = f _ { \mathrm { D T } _ { P P } } \Big ( \prod _ { i } \rho _ { \mathrm { E n v } , \mathcal { K } } ^ { i } \varsigma _ { i } M _ { \mathrm { E n v } \mathcal { K } } ^ { i } \Big ) ,\tag{11}
$$

where $f _ { \mathrm { D T _ { R S } } }$ and $f _ { \mathrm { D T _ { P P } } }$ is two mapping function regards to the parameters of $ { \mathrm { D T } } _ { R S }$ and $\mathrm { D T } _ { P P }$ . Based on this, we can obtain our DT model:

$$
\mathrm { D T } _ { \mathrm R S } = \sum _ { i } \mathrm { A t } _ { \mathrm { R S } } \mathrm { E n v } ^ { i } ,\tag{12}
$$

<!-- image-->

Fig. 2. Illustration of the DT model acquisition.  
Algorithm 1: Model Acquisition   
Input: Physical information EnvC, EnvI, and EnvV .   
Output: The DT models.   
1 Implement a cooperative sensing using [18]   
2 Transmit all the data to edge UAVs   
3 Extract key information using (6)   
4 Reshape the data for dimension compression using (7)   
5 Obtain the attention core matrix using (8)   
6 Acquire the attention pooling matrix using (9)   
7 Compute the attention tensors using (10) and (11)   
8 Calculate the DT models using (12) and (13)

$$
\mathrm { D T } _ { P P } = \sum _ { i } \mathrm { A t _ { P P } E n v } ^ { i } .\tag{13}
$$

We also give the detailed implementation process for model acquisition in Algorithm 1.

B. Resource Scheduling Twin Model for Computing and Communication Codesign

We propose an ICC algorithm to empower the implementation of $\mathrm { D T } _ { \mathrm { R S } }$ . As mentioned in Section II, it can provide customized resource scheduling solutions for different distribution scenarios. We consider two distinguished distribution scenarios: an empty scenario and a disturbed scenario.

As shown in Fig. 3, when edge UAVs construct a virtual space to imitate and derive feasible logistics distribution solutions for an empty scenario, we can enable UAVs to implement a directional information diffusion operation towards the logistics destination using the beamforming technology [19]. The diffusion operation is implemented with the information of logistics mission l and UAV state $S _ { i }$ to invite feasible UAVs for cooperative distributions. We give diffusion time ${ \boldsymbol { v } } _ { l } ( t )$ to ensure high-efficiency distribution cooperation:

$$
v _ { l } ( t ) = \left\{ \begin{array} { l l } { v - \epsilon _ { 1 } ( t ) , \quad } & { t _ { k } \quad \mathrm { i s ~ l o w } , } \\ { v - \epsilon _ { 2 } ( t ) , \quad } & { \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{14}
$$

where Ï is a given diffusion time; $\epsilon _ { 1 } ( t )$ and $\epsilon _ { 2 } ( t )$ are variables which increase as time goes by. It is noted that the increased speed of $\epsilon _ { 1 } ( t )$ is lower than that of $\epsilon _ { 2 } ( t )$ Â·

When edge UAVs build a virtual space to imitate and derive reasonable distribution solutions for a disturbed scenario, we cannot directly use the beamforming technology to implement information transmission due to severe communication declines. In this case, our algorithm can efficiently integrate the computing resources of one-hop neighbors to implement cooperative computing for obtaining optimal cooperators based on a Multi-agent Deep Determined Policy Gradient (MA-DDPG) architecture [20]. Explicitly, UAV i can enable an actor-network with the parameter $\theta _ { i , a }$ to train local information $S _ { i }$ to acquire a UAV selection decision. Meanwhile, UAV i can combine all the decisions of neighbors and self-decisions to update parameters:

<!-- image-->  
Fig. 3. Illustration of resource codesign.

$$
\theta _ { i , a } ^ { ' } = \theta _ { i , a } + \lambda _ { j } \sum _ { j = 1 , j \neq i } ^ { N _ { i } } \theta _ { j , a } ,\tag{15}
$$

where $\theta _ { j , a }$ is the actor network parameter of UAV j.

The updated $\boldsymbol { \theta } _ { i , a } ^ { \prime }$ is input to a critic network with parameter $\theta _ { i , \mu }$ to implement decision estimation based on the neighbor status. The estimation result is given to the actor-network to implement further learning for feasible UAV selection. It is noted that the two networks use the stochastic gradient descent method to acquire training gradient values $\nabla J ( \theta _ { i , a } )$ and $\nabla J ( \theta _ { i , \mu } )$ . To ensure a satisfied learning performance, we design a reward function $R _ { i }$ to conduct UAVs to explore feasible directions based on an energy equilibrium method [21]:

$$
R _ { i } = r _ { i } + \frac { \alpha _ { E } } { E _ { j } } \sum _ { j } \operatorname* { m a x } \Big ( r _ { j } - r _ { i } , 0 \Big ) + \frac { \beta _ { E } } { E _ { j } } \sum _ { j } \operatorname* { m a x } \Big ( r _ { i } - r _ { j } , 0 \Big ) ,\tag{16}
$$

where $\begin{array} { r c l } { r _ { i } } & { = } & { \sum _ { j = 1 } ^ { N _ { i } } [ \Delta B _ { j } + \Delta F _ { j } ] ; \ \Delta B _ { j } } \end{array}$ and $\Delta F _ { j }$ denote available resources of bandwidth and CPU of $\mathrm { U A V } j ,$ , respectively. $\alpha _ { E }$ and $\beta _ { E }$ are energy parameters that are set as 5 and 0.05, respectively. In this case, UAVs can obtain suitable distribution path decisions in a cooperative computing manner. However, our ICC algorithm cannot always explore the feasible cooperator due to overloaded logistics missions. In this case, we enable the path planning twin model DTPP to optimize the UAV distribution paths.

## C. Path Planning Twin Model for Distribution Optimization

Based on our ICC algorithm, we can implement cooperative logistics distributions. However, UAVs may cause potential physical collisions due to improper path decisions. In this case, we propose a Particle Swarm Optimization (PSO)-based path planning algorithm in the virtual space. The path planning twin model $\mathrm { D T _ { P P } }$ can use the algorithm to instruct UAVs to dynamically adjust distribution paths by associating different cooperators for collision avoidance in advance. Different from the existing PSO algorithm, ours can enable UAVs to implement path exploration considering multiple dimensions (velocity and position). In addition, UAVs can narrow exploration spaces for low-latency exploration. It can efficiently reduce the computing time for low-latency distribution path decisions. As shown in Fig. 4, we first set the maximal number of iterations, the maximal UAV speed, the initial velocity, and the initial position. UAVs are regarded as particles to implement cooperative explorations based on our formulated

<!-- image-->  
Fig. 4. Illustration of PSO-based path planning.

Algorithm 2: Cooperative logistics distribution.   
Input: Available CPU resources of UAVs; diffusion   
time variables; MA-DDPG network parameters;   
UAV state information.   
Output: The cooperative distribution path decision.   
1 Edge UAVs estimate the logistics scenario   
2 if empty scenario is true then   
3 Construct the corresponding virtual space   
4 Implement directional data diffusion using (14)   
5 Explore to invite feasible cooperators   
6 if disturbed scenario is true then   
7 Construct the corresponding virtual space   
8 Build the MA-DDPG architecture for each   
iteration do   
9 Feed the state information to the actor network   
10 Acquire a UAV selection decision with   
$\nabla J ( \theta _ { i , a } )$   
11 Update the actor network parameters using (15)   
12 Estimate the actor using (16) in the critic   
network   
13 Compute the estimation result with $\nabla J ( \theta _ { i , \mu } )$   
14 Update the critic network parameter $\theta _ { i , \mu }$   
15 Obtain UAV selection decisions   
16 Formulate the fitness function using (17)   
17 for each iteration do   
18 Update UAV velocities using (18)   
19 Update UAV positions using (19) based on the   
UAV selection decisions   
20 Acquire feasible distribution path decisions

fitness function:

$$
f _ { \mathrm { U A V } } = \operatorname* { m i n } _ { \mathcal { L } } \sum _ { i } ^ { M } \sum _ { l = 1 } ^ { L } t _ { i , l } ,\tag{17}
$$

where $t _ { i , l }$ is the time for logistic mission l by UAV i. With the fitness function, UAV i can implement updates of velocity and position to meet the function requirements. The update strategy is optimized with an asynchronous update manner to avoid local optimum. Specifically, we add two probability factors, $P _ { 1 }$ and $P _ { 2 } .$ , to determine if the current velocity is updated with both the individual optimum and global optimum. When $P _ { 1 } , P _ { 2 } \ge 0 . 5 .$ , the velocity is updated as

$$
h _ { i } = \tau h _ { i } + c _ { 1 } \varpi _ { 1 } ( P _ { b , i } - x _ { i } ) + c _ { 2 } \varpi _ { 2 } ( G _ { b } - x _ { i } ) ,\tag{18}
$$

where $P _ { b , i }$ and $G _ { b }$ are the individual optimum and global optimum, respectively; Ï is an inertial parameter; $c _ { 1 }$ and $c _ { 2 }$ are random numbers under $[ 0 , 1 ] ; \varpi _ { 1 }$ and $\varpi _ { 2 }$ are learning parameters, respectively. When the $P _ { 1 } \ge 0 . 5 , P _ { 2 } \le 0 . 5$ , we only update the velocity with the individual optimum. Otherwise, we only update the velocity with the global optimum. Based on this, the position is updated as

$$
x _ { i } ^ { ' } = x _ { i } + v _ { i } .\tag{19}
$$

We can implement finite iterations to acquire the feasible paths of logistics distributions for all the UAVs. In this case, UAVs can always select suitable cooperators with the consideration of collision avoidance. The details with UAV selection are shown in Algorithm 2.

## IV. PERFORMANCE EVALUATION

In this section, we evaluate the performance of our HaDT with several system metrics through a system simulation.

## A. Preliminary

We construct a virtual logistic space using the Gazebo, a system simulation software. It can imitate the UAV mobility based on the current physical scenario. We can enable UAVs to cooperatively implement logistic distribution missions using our proposed algorithms through the Robot Operation System (ROS) interface. The DT imitation process is shown in Fig. 5. We deploy multiple logistics UAVs randomly to implement 10 logistics distribution missions (represented by spheres and cubes) which are deployed in three different logistics warehouses. The buildings (represented by green boxes) are randomly constructed to design a challenging logistics distribution scenario. The distribution destination is in the lower right corner in Fig. 5. The information of UAVs is used to construct $\mathrm { D T } _ { \mathrm { R S } }$ for efficient resource scheduling. The information of logistics missions, distribution environments, and UAVs is used to build DTPP for feasible distribution path planning. We can change numbers of UAVs and logistics missions to further evaluate the effectiveness of our proposed algorithms based on the UAV logistics distribution dataset. The main simulation parameters are summarized in Table I.

<!-- image-->  
Fig. 5. Illustration of logistics imitation in the Gazebo.

TABLE I SIMULATION PARAMETERS
<table><tr><td>Parameter description</td><td>Value</td></tr><tr><td>Number of logistics UAVs</td><td>[20,40]</td></tr><tr><td>Number of logistics missions</td><td>[10,30]</td></tr><tr><td>Average moving velocity of the UAVs</td><td>72 km/h</td></tr><tr><td>Average scalar distance of logistics distributions</td><td>50 km</td></tr><tr><td>Average carrying capability of UAVs</td><td>[15,20] kg</td></tr><tr><td>Pitch angle of the UAVs</td><td>[-130Â°ï¼+40Â°]</td></tr><tr><td>Angular-rate of horizontal rotation</td><td>[-100Â°,+100Â°]</td></tr><tr><td>Learning rate</td><td>[0.001,0.009]</td></tr><tr><td>Diffusion time U</td><td>300 milliseconds</td></tr><tr><td>Minimal safe flight distance of the UAVs</td><td>3m</td></tr><tr><td>Average sensing rate of the UAVs</td><td>1 MByte/s</td></tr><tr><td>Horizontal sensing distance of the UAVs</td><td>[0 m,30 m]</td></tr><tr><td>Gaussian White Noise</td><td>-96 dBm/Hz</td></tr><tr><td>The acceptable maximal implementation latency The acceptable minimal successful distribution ratio</td><td>5minutes</td></tr></table>

We use several metrics to evaluate the performance of our proposed VerDT-based cooperative distribution solution:

1) System communication overhead: It is used to estimate the communication data size and latency during distribution process based on Eq. (1).

2) System computing latency: This metric mainly reflects the performance of DT construction for real-time model acquisitions.

3) System energy consumption: It is used to evaluate the effectiveness of cooperative path planning with energy saving.

4) System latency overhead: This metric includes latencies of sensing, communication, DT implementation, and decision-making. It is used to perform the real time of system implementation.

5) Successful distribution ratio: It can evaluate the accuracy of mission implementation. It is formulated as $\eta =$ limT $\begin{array} { r } { \cdot \infty \ \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \frac { \sum _ { i = 1 } ^ { M } \sum _ { k = 1 } ^ { K } m _ { k } } { M K } } \end{array}$ , where $m _ { k }$ denotes that UAV m implement distribution mission k to a given destination successfully.

We use four typical benchmarks for comparison:

1) On demand-based logistics distribution foresting method [22]: It leverages a two-stage prediction optimization strategy to implement cooperative distributions based on the LSTM algorithm.

2) Three-stage path planning method [8]: It first uses a statistical method to implement distribution analysis. Then a machine learning algorithm is training to empower an explainable learning technique to explore feasible distribution paths for real-time distributions.

3) Cloud-based logistics distributions method [23]: The method leverages powerful computing resource of the cloud server to implement cooperative logistics distributions with a high successful distribution ratio.

4) Predict-Then-Optimize based Couriers Allocation (PTOCA) method [9]: It provides a high-efficiency logistics distribution solution with path prediction and allocation optimization based on the GRU network and distribution priority analysis.

## B. Result Analysis

With the resource scheduling twin model DTRS, we provide the comparison of energy consumption on communication with different numbers of UAVs and missions. Given 20 logistics distribution missions, Fig. 6 shows the comparison under different numbers of UAVs with an average speed of 72 km/h. We can find that the energy consumption on communication increases as the number of UAVs increases for all the solutions. However, our solution with $\mathrm { D T } _ { \mathrm { R S } }$ can alleviate the increasing rate by selecting feasible cooperators based on our proposed direct information diffusion method. In addition, our solution can efficiently use sensing and computing resources to acquire status of neighbors for cooperative logistics distributions. It can significantly reduce the frequency of information exchanges among neighbors for saving energy consumption on communication. In this case, our solution can reduce the energy consumption on communication by 52.78%, 56.41%, and 58.54% on average compared to the state-of-theart on-demand based, PTOCA, and cloud-based algorithms, respectively.

We also provide the comparison of data size in Fig. 7. Based on the same deployment as that of Fig. 6, we can see that our solution can reduce extra communication data size compared to all the benchmarks in Fig. 7. This is because our solution can conduct UAVs to transmit lightweight model parameters instead of raw physical information for highefficiency distribution cooperation. In this case, our solution reduces the data size by 46.6%, 49.3%, and 51.9% compared to the PTOCA, on-demand based, and cloud-based algorithms, respectively.

Our solution can still perform competitive computing latency with a variable number of logistics missions shown in Fig. 8. It implies that our solution can always assist UAVs in exploring feasible computing resources of neighbors. Moreover, it means that UAVs can acquire accurate distribution results without extra computing resources for decision optimization. In this context, ours can improve the computing efficiency by 25.6%, 51.7%, 60.8%, and 75.4% compared to the cloud-based, PTOCA, on-demand based, and three-stage algorithms, respectively.

<!-- image-->

<!-- image-->  
Fig. 6. Consum. on comm. vs. Fig. 7. Data size vs. number of number of UAVs. UAVs.

<!-- image-->

<!-- image-->  
Fig. 8. Computing latency vs. Fig. 9. Energy consumption vs. number of missions. number of UAVs.

We provide the comparison of energy consumption with different numbers of UAVs, logistics missions, and moving speeds of UAVs. Explicitly, Fig. 9 showcases the change in energy consumption. Although energy consumption of all the solutions can increase as the number of UAVs increases, our solution performs the lowest energy consumption based on the high-efficiency conduction of DT model DTPP. It can improve the probability of selecting feasible cooperators to assist UAVs in acquiring optimal path planning decisions. In addition, DTRS can provide the decision of resource scheduling to $\mathrm { D T _ { P P } }$ . The results can enable $\mathrm { D T _ { P P } }$ to optimize distribution paths of UAVs with operations of environment estimation and information exchanges. Ours reduces the energy consumption by 26.8% on average compared to the best three-stage benchmark.

Fig. 10 showcases the comparison of system latency. With the 20 UAVs, we can find our solution can efficiently cope with the overloaded distribution missions as the number of missions increases with a mild uptrend. It implies that our DT models can derive the flight trajectories of UAVs to select feasible numbers of UAVs for the optimal path planning. In this case, our solution can reduce the system latency by 67.2%, 68.3%, 73.6%, and 74.7% compared to the cloud-based, on-demand, PTOCA, and three-stage algorithms, respectively.

On the other hand, we showcase the comparison of successful distribution ratio with different number of missions in Fig. 11. We can see that our solution can still perform a high successful distribution ratio when facing the overloaded missions. This is because our solution can dynamically adjust flight trajectories of UAVs to implement different distribution missions. It is verified that this way is efficient to maximize the distribution requirements. For the four benchmarks, the PTOCA algorithm performs the highest distribution ratio using a method of joint prediction and optimization. However, the method cannot ensure a robust mission implementation in an overloaded situation due to the limited prediction ability of the GRU network. In this context, our solution can further improve the successful distribution ratio by 10.9%, 16.9%, 33.8%, and 35.7%, respectively.

<!-- image-->

<!-- image-->  
Fig. 10. System latency vs. num- Fig. 11. Successful distribution ber of missions. ratio vs. number of missions.

## V. CONCLUSION

We have proposed a hardened DT framework to empower UAVs to implement real-time logistics distributions with a high successful distribution ratio. Based on our framework, edge UAVs can train a resource scheduling twin model to implement the integration of computing and communication of UAVs for accurate logistics distributions by enhancing UAV cooperation. With the UAV cooperation decisions, edge UAVs can then acquire a path planning twin model to derive feasible UAV paths for real-time logistics distributions with low energy consumption. The experiment results demonstrate that our HaDT framework can assist UAVs with the optimization of distribution paths for low-energy logistics distributions compared to the state-of-the-art distribution solutions. Additionally, our solution can still perform high successful distribution ratios in complicated distribution scenarios with variable numbers of UAVs and distribution missions.

## ACKNOWLEDGMENTS

This paper is supported in part by the National Research Foundation, Singapore and Infocomm Media Development Authority under its Future Communications Research & Development Programme, the Chengdu Science and Technology Bureau Project under Grant 2023-YF06-00030-HZ, and the Science and Technology Project of Sichuan Province under Grant 2024YFHZ0321..

## REFERENCES

[1] E. G. Kaigom, âMetarobotics for industry and society: Vision, technologies, and opportunities,â IEEE Trans. Industr. Inform., vol. 20, no. 4, pp. 5725â5736, 2024.

[2] A. Hazra, A. Kalita, and M. Gurusamy, âDistributed service provisioning with collaboration of edge and cloud in industry 5.0,â IEEE Internet Things J., vol. 11, no. 12, pp. 21 885â21 894, 2024.

[3] L. Chen, J. Xie, X. Zhang, J. Deng, S. Ge, and F.-Y. Wang, âMining 5.0: Concept and framework for intelligent mining systems in cpss,â IEEE Trans. Intell. Veh., vol. 8, no. 6, pp. 3533â3536, 2023.

[4] P. Maurya, V. M. R. Tummala, A. Hazra, and S. P. Mohanty, âAdvancing industry 5.0 with uav-driven transformations: Future prospectives,â IEEE Consum. Electr. M., vol. 3, no. 4, pp. 1â6, 2024.

[5] D. K. Jain, Y. Li, M. J. Er, Q. Xin, D. Gupta, and K. Shankar, âEnabling unmanned aerial vehicle borne secure communication with classification framework for industry 5.0,â IEEE Trans Ind. Informat., vol. 18, no. 8, pp. 5477â5484, 2022.

[6] Y. Ma, Y. Wang, S. D. Cairano, T. Koike-Akino, J. Guo, P. Orlik, X. Guan, and C. Lu, âSmart actuation for end-edge industrial control systems,â IEEE Trans. Autom. Sci. Eng., vol. 21, no. 1, pp. 269â283, 2024.

[7] L. Ma, X. Wang, X. Wang, L. Wang, Y. Shi, and M. Huang, âTCDA: Truthful combinatorial double auctions for mobile edge computing in industrial internet of things,â IEEE Trans. Mob. Comput., vol. 21, no. 11, pp. 4125â4138, 2022.

[8] S. Hao, Y. Liu, Y. Wang, Y. Wang, and W. Zhe, âThree-stage root cause analysis for logistics time efficiency via explainable machine learning,â in Proceedings of the 28th ACM SIGKDD, ser. KDD â22, New York, NY, USA, 2022, p. 2987â2996.

[9] K. Xia, L. Lin, S. Wang, H. Wang, D. Zhang, and T. He, âA predictthen-optimize couriers allocation framework for emergency last-mile logistics,â in Proceedings of the 29th ACM SIGKDD, ser. KDD â23, New York, NY, USA, 2023, p. 5237â5248.

[10] M. Picone, M. Mamei, and F. Zambonelli, âA flexible and modular architecture for edge digital twin: Implementation and evaluation,â ACM Trans. Internet Things, vol. 4, no. 1, feb 2023.

[11] K. Xiong, Z. Wang, S. Leng, and J. He, âA digital-twin-empowered lightweight model-sharing scheme for multirobot systems,â IEEE Internet Things J., vol. 10, no. 19, pp. 17 231â17 242, 2023.

[12] X. Chen, Z. Feng, Z. Wei, F. Gao, and X. Yuan, âPerformance of joint sensing-communication cooperative sensing uav network,â IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 15 545â15 556, 2020.

[13] E. A. Traff, A. Rydahl, S. Karlsson, O. Sigmund, and N. Aage, Â¨ âSimple and efficient gpu accelerated topology optimisation: Codes and applications,â Comput. Method Appl. M., vol. 410, p. 116043, 2023.

[14] A. Ray, B. Devlin, F. Y. Quah, and R. Yesantharao, âHardcaml msm: A high-performance split cpu-fpga multi-scalar multiplication engine,â in Proceedings of the 2024 ACM/SIGDA Intl. Sym. Field Programmable Gate Arrays, 2024, pp. 33â39.

[15] Z. Liao, Y. Liu, J. Zhao et al., âMeta-learning-based multi-objective pso model for dynamic scheduling optimization,â Energy Reports, vol. 9, pp. 1227â1236, 2023.

[16] Y. Yokokura, S. Katsura, and K. Ohishi, âStability analysis and experimental validation of a motion-copying system,â IEEE Trans Industr Inform, vol. 56, no. 10, pp. 3906â3913, 2009.

[17] W. Ye, X. Zhou, J. Zhou, C. Chen, and K. Li, âAccelerating attention mechanism on fpgas based on efficient reconfigurable systolic array,â Acm Trans. Embed. Comput. Sys., vol. 22, no. 6, pp. 1â22, 2023.

[18] N. Qi, Z. Huang, W. Sun, S. Jin, and X. Su, âCoalitional formationbased group-buying for uav-enabled data collection: An auction game approach,â IEEE Trans. Mob. Comput., vol. 22, no. 12, pp. 7420â7437, 2023.

[19] J. Li, G. Sun, H. Kang, A. Wang, S. Liang, Y. Liu, and Y. Zhang, âMultiobjective optimization approaches for physical layer secure communications based on collaborative beamforming in uav networks,â IEEE/ACM Trans. Netw., 2023.

[20] H. Zhang, S. Leng, H. Yin, and S. Yu, âIntelligent consensus enhanced spectrum sharing in heterogeneous wireless networks,â IEEE Internet Things J., vol. 11, no. 19, pp. 30 939â30 952, 2024.

[21] X. Huang and S. Zhou, âQmnet: Importance-aware message exchange for decentralized multi-agent reinforcement learning,â IEEE Trans. Mob. Comput., vol. 23, no. 5, pp. 4739â4751, 2024.

[22] X. Yang, J. Meng, and Y. Liu, âResearch on the allocation of cargo space in pharmaceutical logistics center based on demand forecasting,â in 2021 8th ICAL, ser. ICAL 2021. New York, NY, USA: Association for Computing Machinery, 2021, p. 1â7.

[23] Q. Wang and X. Du, âDesign of logistics cloud platform based on blockchain,â in Proceedings of the 2022 4th Blockchain and Internet of Things Conference, ser. BIOTC â22. New York, NY, USA: Association for Computing Machinery, 2022, p. 100â106.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_3_img_5.png|page_3_img_5]]
2. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_3_img_6.png|page_3_img_6]]
3. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_4_img_1.png|page_4_img_1]]
4. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_1.png|page_5_img_1]]
5. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_2.png|page_5_img_2]]
6. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_3.png|page_5_img_3]]
7. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_4.png|page_5_img_4]]
8. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_5.png|page_5_img_5]]
9. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_6.png|page_5_img_6]]
10. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_7.png|page_5_img_7]]
11. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_8.png|page_5_img_8]]
12. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_5_img_9.png|page_5_img_9]]
13. [[../extracted_images/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems/page_6_img_1.jpeg|page_6_img_1]]

---

