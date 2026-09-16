# Semantic-Aware UAV Swarm Coordination in the Metaverse: A Reputation-Based Incentive Mechanism

Jiaqi Xu, Student Member, IEEE, Haipeng Yao , Senior Member, IEEE, Ru Zhang, Tianle Mai , Member, IEEE, Shan Huang, Student Member, IEEE, Zehui Xiong , Member, IEEE, and Dusit Niyato , Fellow, IEEE

AbstractâUnmanned aerial vehicle (UAV) swarms have found extensive applications owing to their flexibility, mobility, costeffectiveness, and capacity for collaborative and autonomous service delivery. Empowered by intelligent algorithms, UAV swarm can exhibit cohesive behaviors and autonomously coordinate to achieve collective objectives. Nonetheless, in real-world scenarios with uncertainty and stochasticity, its performance suffers from the unstable information exchange among UAVs and inefficient data sampling. In this paper, we introduce a metaverse-based UAV swarm system, where monitoring, observation, analysis, and simulation can be realized collaboratively and virtually. Within the metaverse, virtual service providers (VSPs) utilize digital twin (DT) to generate and render virtual sub-worlds, while providing diverse virtual services. In particular, the VSP trains the learning model using high-fidelity data from the physical world, formulates optimal decisions for diverse tasks, and returns these decisions to the UAV swarm for the execution of the corresponding tasks. Since synchronization between two worlds needs frequent data exchange, we employ the semantic communication technique in our system which could reduce communication latency by transmitting only the semantic information. In such design, UAVs as workers are employed to collect data and provide extracted semantic information to the VSPs. Moreover, we propose a hierarchical framework to investigate the reliability and sustainability of the metaverse-based

Digital Object Identifier 10.1109/TMC.2024.3438152

UAV swarm system. In the lower layer, we design a worker selection scheme to determine reliable UAVs for data synchronization. In the upper layer, we consider deep learning (DL)-based auction as the incentive mechanism for resource allocation in semantic information trading between UAV swarm and VSPs.

Index TermsâSemantic communication, UAV swarm, metaverse, multi-armed bandit algorithm, incentive mechanism.

## I. INTRODUCTION

R ECENTLY, unmanned aerial vehicle (UAV) swarm haswitnessed remarkable expansion in civilian and military witnessed remarkable expansion in civilian and military applications, including crowd monitoring, target tracking, damage assessment and so on [1]. Empowered by intelligent algorithms, UAV swarm can exhibit cohesive behaviors and autonomously coordinate to achieve collective objectives [2]. Nonetheless, in real-world scenarios with uncertainty and stochasticity, unstable information exchange between UAVs and inefficient data sampling can affect the model performance and training speed of intelligent algorithms [3]. Simultaneously, directly training the UAV swarm in a dynamic environment is confronted with undesirable factors such as physical obstacles, consequently resulting in additional costs and safety concerns [4]. The issues above become the bottleneck that impedes the enhancement of UAV swarm intelligence cooperation.

In particular, the metaverse can offer UAV swarm virtual services where monitoring, observation, analysis, and simulation can be realized collaboratively and virtually [5]. Utilizing sensor data collected by the UAV swarm, a Virtual Service Provider (VSP) creates and visualizes a virtual sub-world by replicating the physical environment and then provides a specific virtual service [6]. For an effective replication of the real world, we employ digital twin (DT) technology to capture the evolving states of the real-world entities, i.e., the UAVs, over time [7]. With robust virtual-real interaction capabilities and resilience to environmental factors, DT reliably generates high-fidelity digital representations of real-world entities from historical data, sensor data and physical objects [8], [9]. To this end, we use DT to establish a metaverse-based UAV swarm system, in which a learning model is trained with high-fidelity data to yield optimal decisions accurately and promptly [10].

To replicate the physical world to the finest details, the UAV swarm is required to guarantee real-time and continuous data synchronization from the physical world to the virtual world. In detail, the UAV swarm needs to effectively transmit relevant data, including basic information, status, and characteristics, to the VSPs within specified latency requirements [11]. However, when confronted with complex and dynamic environments, limited bandwidth and transmission unreliability may lead to the failure of the UAV swarm in guaranteeing real-time and large-scale data synchronization between these two worlds. The unreliability of the DT derived in this case would consequently affect the accuracy of the virtual services provided by the VSPs [12].

Fortunately, semantic communication (SemCom) as a promising technique, can help to reduce communication latency by transmitting only the semantic information while eliminating unnecessary information from the original data [13]. Moreover, it exhibits greater resistance to channel noise and interference compared to bit streams in conventional communication, thereby improving data transmission reliability [14]. In pursuit of achieving real-time synchronization, we employ the SemCom technique within the metaverse-based UAV swarm network to facilitate frequent data exchange and state synchronization between the two worlds.

In such a design, UAVs extract the semantic information of collected data based on its semantic model and then, transmit it to the VSP. Subsequently, VSP in the metaverse utilizes semantic information from corresponding UAVs to update its learning model. This design can significantly reduce communication latency and improve transmission dependability, equivalently alleviating communication pressure. However, there are still several issues that need to be addressed. On the one hand, the workers, i.e., UAVs, may be unwilling to participate in the data synchronization task without a reasonable incentive due to their self-interest. On the other hand, there may be malicious workers that perform intended operations such as forging, deleting, or replacing semantic information. Additionally, unstable wireless communication channel conditions and high mobility or energy constraints of UAVs may result in their unintentional behaviors of generating inaccurate semantic information. Both of these unreliable behaviors could deteriorate the decision-making performance of the VSP.

To tackle the aforementioned challenges, we introduce a novel two-layer architecture to ensure reliable worker selection and incentivize UAV participation in data synchronization tasks. In the lower layer, we consider a multi-armed bandit (MAB)-based worker selection scheme to assess the reliability of UAVs. Then each cluster head gathers semantic information from the selected workers within the cluster to realize low-cost and high-speed transmission. In the upper layer, we propose a deep learning (DL)-based auction model to attract workers to participate in data synchronization tasks in the metaverse.

The main contributions of this paper are as follows:

- Leveraged by the SemCom technique, we propose a novel approach to enabling data synchronization in the metaverse-based UAV swarm system. Rather than transmitting raw data, UAVs within each cluster send extracted semantic information to these associated VSPs, thereby reducing the volume of transmitted data and consequently minimizing latency.

- We introduce a hierarchical architecture to investigate the reliability and sustainability of metaverse-based UAV swarm systems. In the lower layer, we propose an MABbased online worker selection scheme in which reliable UAVs are selected for data synchronization tasks.

- In the upper layer of hierarchical architecture, we develop a DL-based auction game for incentivizing the UAVsâ participation in semantic information trading, which is announced by VSPs.

The rest of the paper is organized as follows. In Section II, we discuss the relevant works about metaverse-based UAV swarm systems and deep learning-enabled semantic communication. In Section III, we describe the system model in detail. In Section IV, we present the MAB-based worker selection scheme for the DT synchronization task. In Section V, we introduce the DLbased incentive mechanism design. In Section VI, we show the simulation results of the proposed algorithms, and Section VII concludes the paper.

## II. RELATED WORK

In this section, we provide a concise review of the existing literature on the metaverse-based UAV swarm network and deep learning-enabled semantic communication.

## A. Metaverse-Based UAV Swarm System

Although metaverse-related research is still in its infancy, there are several works investigating the potential of leveraging metaverse over UAV swarms.

In [15], the authors introduce an intelligent cooperation framework for UAV swarms based on DT technology. This framework incorporates machine learning algorithms to optimize the global performance of UAV swarm. In [12], the authors investigate the synchronization in UAV-assisted metaverse scenario and model the problem as an evolutionary game to incentivize UAVs to select VSPs to work for. The authors in [16] design a double-agent reinforcement learning-based scheme for data synchronization problem in UAV-enabled metaverse system, where a proximal policy optimization algorithm is employed to enable cooperative hybrid actions. In tackling the energy management issue in the UAV-assisted metaverse, the authors in [17] establish an energy trading market which involves energy service providers and UAVs. In [18], a multi-agent deep deterministic policy gradient sim2real transfer method is implemented to establish bridges between real and virtual multi-UAV network. Their work emphasizes the modularization of perception control to enable metaverse-based multi-UAV collaborative delivery tasks. Nevertheless, existing literature pays scant attention to the effectiveness and timeliness of data synchronization between the physical and virtual worlds, which might potentially impede the implementation of the metaverse-based UAV swarm system.

## B. Deep Learning Enabled Semantic Communication

Contrary to traditional communication system that focus on Shannon information theory, SemCom introduces a paradigm shift by extracting and transmitting only the semantic symbols relevant to targeted tasks, thus obviating the need for transmitting entire raw data. With the booming development of machine learning (ML), deep learning-enabled semantic communication has sparked significant research interest. A number of works such as [19], [20], [21], [22], [23] studied deep learning-enabled semantic communication.

<!-- image-->  
Fig. 1. Semantic-aware metaverse-based UAV swarm architecture.

Specifically, the authors in [19] introduce a text-based Sem-Com system that leverages transfer learning to adapt to various communication environments and expedite the training process. The authors in [20] develop a SemCom system for speech transmission and demonstrate its superiority in the low signal-tonoise ratio situation. For image transmission, in [21], the authors introduce a novel generative adversarial networks-based semantic coding methodology to facilitate semantic reconstructions. In this research, a set of perceptual metrics is proposed to optimize and assess the effectiveness of information exchange. The authors in [22] explore a neural network-powered SemCom system in which the transmitter operates without prior knowledge of the task, and the data is dynamic. Furthermore, in [23], the authors propose a novel adaptive semantic coding method leveraging reinforcement learning. The proposed method is shown to transcend traditional pixel-level encoding and could generate reconstructions under low bit-rate conditions. In summary, the existing literature lacks consideration for semantic information allocation optimization in wireless systems under dynamic and uncertain conditions.

## III. SYSTEM MODEL

## A. Metaverse-Based UAV Swarm Architecture

In this section, we propose a novel semantic-aware metaversebased UAV swarm architecture to ensure UAV swarm cooperation.

As depicted in Fig. 1, the presented architecture primarily has three components: the physical world which serves as the foundational underpinning, the virtual world which monitors the physical space, and the interaction layer which facilitates seamless connectivity between the two worlds.

Physical World: The physical world consists of the UAV swarm and the task environment. Each UAV has a set of sensors to sense the surrounding environment state over time and extracts semantic information by equipped semantic extraction model.

Virtual World: The virtual world is developed and maintained by VSPs in the metaverse, where a high-fidelity DT of the physical world is established with the recovery of received semantic information from the UAV swarm. Leveraged by the SemCom technique, the VSP updates the digital model in an effective and real-time manner. Empowered by ML and data analytics techniques, the VSP trains the learning model for providing optimal decisions in specific metaverse services, such as resource allocation, swarm network optimization, cooperative decisions, and so on. After each task execution by the UAV swarm, the VSP collects feedback information to improve the dataset and learning model.

Interaction Layer: For the purpose of delivering better communication quality, the data transmission between the two worlds adopts the SemCom technique. The physical entity conveys semantic information to the VSP, which is equipped with a learning model to abstract environmental features, analyze cooperative tasks, derive optimal decisions, and subsequently release these decisions via the interaction layer to manage the UAV swarm.

## B. System Model

We consider a semantic-aware metaverse-based UAV swarm with N UAVs and M VSPs, which are denoted by the sets ${ \mathcal { N } } =$ $\{ 1 , . . . . , n , . . . , N \}$ and $\mathcal { M } = \{ 1 , . . . , m , . . . , M \}$ , respectively. To reduce the interruption probability caused by long-distance transmission, L UAV-BSs are introduced as relays to provide communication services between UAVs and VSPs, which are denoted as the set $\mathcal { L } = \{ 1 , . . . , l , . . . , L \}$ . The UAVs grouped into multiple clusters can collect sensing data and transmit extracted semantic information to its cluster head, i.e., UAV-BS, with the UAV-UAV channel. In the network, let $n _ { l }$ denote the number of UAVs served by UAV-BS l.

In practice, the VSP may not be able to identify reliable UAVs, which suffer the performance of the digital model and consequently degrade the service quality of the VSP [12]. We adopt a hierarchical framework, where initially in the lower layer, the reputation values and communication latency of UAVs are used to identify the trustable UAVs in the lower layer. In the upper layer, UAVs are encouraged to contribute their semantic information to VSPs in cluster units to facilitate data synchronization.

Fig. 2 shows the data synchronization process for the metaverse-based UAV swarm, which mainly includes the reliable worker selection phase and semantic information trading phase. The details are given as follows.

Step 1: The VSPs send transaction requests to the UAV swarm for acquiring semantic information, which includes the semantic type and latency requirement.

Step 2:Upon receiving the request information from the VSPs, the cluster head informs its relevant UAVs and invites them to join in semantic information transactions.

Step 3: Through the worker selection scheme, the cluster heads select trustable UAVs, collect semantic information from all their cluster members, and then perform data fusion algorithms. The details about the worker selection scheme are given in Section IV.

Step 4: A multi-round DL-based auction is conducted to promote semantic information trading between the cluster head and VSPs. Typically, for each VSP, clusters with higher semantic information value can increase the performance of DT. More details about the auction design are presented in Section V.

<!-- image-->  
Fig. 2. Main procedures in the data synchronization.

<!-- image-->  
Fig. 3. Example of extracted semantic information for the metaverse [24].

Step 5:After the auction stage, the VSP assesses the quality of acquired semantic information through the attack detection scheme, e.g., the De-Pois scheme [25], to identify poison attacks and unreliable workers. The transactions with unreliable workers are recorded as negative interactions by the VSP and vice versa. Then, the cluster head receives the deserved reward from the VSP, where the reward is allocated to all the participating workers within the cluster in a fair manner.

Subsequently, the VSP receives the semantic information from the seller, i.e., cluster head, and proceeds to refresh its digital model through a series of operations which includes data cleaning, classification, and modeling. It is worth noting that the VSP should extract fundamental attributes from semantic information. For instance, in the collaborative search services provided by the VSP, semantic information is utilized to extract task areas and the number of UAVs to create a search information map, which can provide target appearance probability in the specific area. With the well-trained learning model at the VSP, optimal decisions for various tasks are derived and returned to the UAV swarm for the execution of corresponding tasks. The notations in this paper are presented in Table I.

## C. Semantic Communication System

As illustrated in Fig. 3, we present our results on extracting semantics from an actual dataset associated with the UAV swarm and use the image as an example [24]. To accomplish this, we leverage the scene graph generation model called RelTR, as detailed in [26]. The RelTR model adopts an encoder-decoder architecture which contains a feature encoder, entity decoder, and triplet decoder. The RelTR model first obtains the visual feature context and entity representation of an image through the feature encoder and entity decoder. Then, the feature context of entities from the entity decoder layer is inferred by leveraging the triplet decoder with an attention mechanism, ultimately yielding the semantic triplet.

TABLE I NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>nEN</td><td rowspan=1 colspan=1>Index ofUAVs</td></tr><tr><td rowspan=1 colspan=1>mEM</td><td rowspan=1 colspan=1>Index ofVSPs</td></tr><tr><td rowspan=1 colspan=1>lEL</td><td rowspan=1 colspan=1>IndexofUAV-BSs</td></tr><tr><td rowspan=1 colspan=1>n</td><td rowspan=1 colspan=1>Number ofUAVs servedbyUAV-BSl</td></tr><tr><td rowspan=1 colspan=1> $\overline { { ( t _ { a } , t _ { a b } , t _ { b } ) } }$ </td><td rowspan=1 colspan=1>Semantic triplets</td></tr><tr><td rowspan=1 colspan=1> $R _ { n , l }$ </td><td rowspan=1 colspan=1>DataratebetweenUAVn andUAV-BSl</td></tr><tr><td rowspan=1 colspan=1> $\omega _ { n }$ </td><td rowspan=1 colspan=1>Semantic information size of UAV n</td></tr><tr><td rowspan=1 colspan=1> ${ \underline { { t _ { n , l } } } }$ </td><td rowspan=1 colspan=1>Communicationtime ofUAVn forUAV-BSl</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Binaryvariableofworkersâavailablestatus</td></tr><tr><td rowspan=1 colspan=1> $\overline { { W _ { t } } }$ </td><td rowspan=1 colspan=1>Chosen worker setin the round t</td></tr><tr><td rowspan=1 colspan=1> $\overline { { F } }$ </td><td rowspan=1 colspan=1>Fixedsettingof selectedworkers</td></tr><tr><td rowspan=1 colspan=1> $\overline { { k } }$ </td><td rowspan=1 colspan=1>Number of selectedworkers</td></tr><tr><td rowspan=1 colspan=1> $p _ { m  n } , q _ { m  n }$ </td><td rowspan=1 colspan=1>Number of positive/negative interactions betweenVSP m and UAV n</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \beta } }$ </td><td rowspan=1 colspan=1>Success probability of transmission</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \theta } }$ </td><td rowspan=1 colspan=1>Level of uncertainty</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \gamma _ { m \to n } } }$ </td><td rowspan=1 colspan=1>Reputation score of VSP m for UAV n</td></tr><tr><td rowspan=1 colspan=1> $\lambda _ { t h }$ </td><td rowspan=1 colspan=1>Latency requirement between the UAV and itscluster head</td></tr><tr><td rowspan=1 colspan=1> $\overline { { { r _ { n } ^ { t } } } }$ </td><td rowspan=1 colspan=1>Reputation value $\overline { { r _ { n } ^ { t } } }$ of the UAV n in the round t</td></tr><tr><td rowspan=1 colspan=1> $\underline { { a _ { m , l } } }$ </td><td rowspan=1 colspan=1>SemanticmatchlevelofVSP m forUAV-BSl</td></tr><tr><td rowspan=1 colspan=1> ${ \underline { { v _ { m } } } }$ </td><td rowspan=1 colspan=1>Valuation ofVSP m</td></tr></table>

The transmitter, e.g., UAV, first conveys a set of images $D = [ d _ { 1 } , d _ { 2 } , \ldots ]$ over the physical channel, which is subject to = [ ]transmission impairments including distortion and noise [27]. The encoded signal is defined as:

$$
x = C _ { \alpha } ( S _ { \beta } ( d ) ) ,\tag{1}
$$

where $C _ { \alpha }$ and $S _ { \beta }$ are channel encoder with parameter Î± and semantic encoder with parameter $\beta ,$ respectively. The received signal is denoted as:

$$
y = h x + n ,\tag{2}
$$

where $h$ is Rayleigh fading channel and $n \sim N ( 0 , \sigma _ { n } ^ { 2 } )$ is the Gaussian noise. Then, the received signal $y ,$ (0 )is decoded at the receiver as follows:

$$
\hat { x } = S ^ { - 1 } ( C ^ { - 1 } ( y ) ) ,\tag{3}
$$

where $S ^ { - 1 }$ is the semantic decoder and $C ^ { - 1 }$ is channel decoder at the receiver. The transmitter and receiver are jointly designed with DNNs.

The SemCom system outputs the triplet $< t _ { a } , t _ { a b } , t _ { b } >$ , which denotes the subject-relation-object relationship in text format. This representation effectively minimizes the data volume that needs to be transmitted. For example, a semantic triplet extracted by the UAV from Fig. 3 is < car on street >. This triplet is subsequently sent to the VSP for comprehensive computing and analysis. Each VSP providing traffic control services needs to extract semantic information about the conditions of physical entities such as roads, cars, traffic, and so on. Therefore, the semantic triplets $<$ car on street > align with the information that VSP requires.

The data rate between UAV n and UAV-BS l can be obtained similar to that in [28]:

$$
R _ { n , l } = B _ { n } \log _ { 2 } \left( 1 + { \frac { p _ { n } h _ { n , l } } { B _ { n } N _ { 0 } } } \right) ,\tag{4}
$$

where $p _ { n }$ is transmit power, $h _ { n , l }$ is the channel gain between UAV n and $\mathrm { U A V - B S } l , N _ { 0 }$ is the power spectral density of noise.

Accordingly, the communication latency from UAV n to UAV-BS l for transmitting the semantic information is:

$$
t _ { n , l } = \frac { \omega _ { n } } { R _ { n , l } } ,\tag{5}
$$

where $\omega _ { n }$ is the size of semantic information.

## IV. LOWER LAYER: MAB-BASED ONLINE WORKER SELECTION

In this section, we first introduce the worker selection scheme and the reputation model in the DT construction task. Then, we develop an MAB-based online worker selection algorithm.

## A. Worker Selection for DT Construction Task

As the worker selection problem is investigated under a highly dynamic UAV swarm network, it becomes impractical to assume workers are perpetually prepared to offer their services [29]. In light of this, we use a binary variable I to capture workersâ status which indicates whether they are available or not. Such information could be revealed to the cluster head at the beginning of each round t. On the other hand, due to the limited wireless channel resources, we focus on choosing a subset of the available workers for DT construction tasks. We denote the chosen subset in the round t as $W _ { t }$ . Thus, the constraint of worker availability

is denoted as:

$$
I _ { t , n } = 1 , \forall n \in W _ { t } .\tag{6}
$$

The selection of workers is not subject to a predetermined maximum threshold. Given that the number of available workers may not consistently align with the predefined parameter $F ,$ we should utilize a min function to constrain the number of selected workers:

$$
k = \operatorname* { m i n } \left\{ F , \sum _ { n = 1 } ^ { n _ { l } } I _ { t , n } \right\} ,\tag{7}
$$

where k is the number of selected workers. Then we have $| W _ { t } | = k$ where $| W _ { t } |$ is the cardinality of $W _ { t }$ . Precisely, when =the number of overall available workers could not meet the fixed setting $F ,$ we entail all currently available workers in the subsequent round of selection without any selection criteria.

## B. Reputation Model

We design a reputation model for UAV swarm. Our reputation model considers the communication quality, transmission reliability, and latency in data transactions.

1) Reputation Score: Consider $n \in \mathcal N .$ , the reputation opinions of VSP m to UAV n is expressed as a vector $\Upsilon _ { m  n } =$ $\{ b _ { m  n } , d _ { m  n } , u _ { m  n } \}$ . Here, $b _ { m  n }$ is belief, $d _ { m  n }$ Î¥ =is disbelief and $u _ { m  n }$ is uncertainty. $b _ { m  n } , d _ { m  n } , u _ { m  n } \in [ 0 , 1 ]$ and $b _ { m  n } + d _ { m  n } + u _ { m  n } = 1$ [0 1]. According to the subjective logic + + = 1model [30], belief, disbelief, and uncertainty can be represented as follows:

$$
\{ \begin{array} { l l } { b _ { m  n } = ( 1 - u _ { m  n } ) \frac { p _ { m  n } } { p _ { m  n } + q _ { m  n } } , } \\ { d _ { m  n } = ( 1 - u _ { m  n } ) \frac { q _ { m  n } } { p _ { m  n } + q _ { m  n } } , } \\ { u _ { m  n } = 1 - \beta _ { m  n } , } \end{array} \tag{8}
$$

where $p _ { m  n }$ and $q _ { m  n }$ are the numbers of positive and negative interactions, respectively. A trading interaction between the VSP and the UAV is treated as a positive event if the UAV can provide correct and trusted semantic information for the VSP to support the efficient digital copy, and vice versa. Specifically, through a poison attack detection scheme (as outlined in Section III-B, Step 5), if the VSP judges the semantic information from the worker to be trustworthy, it categorizes the transaction as a positive interaction event. Conversely, interactions with malicious workers are considered negative and result in a decrement in the workerâs reputation. $\beta _ { m  n }$ , as the uncertainty in computing the reputation score, represents the success probability of transmission. The reputation score $\gamma _ { m  n }$ is denoted as follows:

$$
\gamma _ { m  n } = b _ { m  n } + \theta u _ { m  n } ,\tag{9}
$$

where $\theta \in [ 0 , 1 ]$ is the coefficient that indicates the level of uncertainty for reputation.

2) Latency Calculation: Since stale semantic information may lead to an inaccurate model, low latency is crucial for DT construction. The reputation valuation of the UAVs also depends on the transmission latency, which refers to the time spent on transmitting the semantic information from the worker to its cluster head.

Given that the cluster head has the lowest latency requirement $\lambda _ { t h }$ of collecting semantic information from its corresponding UAV, it is imperative to establish a stringent criterion to guarantee the latency requirements. When the UAVâs transmission delay of semantic symbols exceeds the threshold of $\lambda _ { t h }$ , the corresponding UAVâs reputation value is unilaterally reduced to zero. The delay indicator function is described as:

$$
f ( t _ { n } , \lambda _ { t h } ) = { \left\{ \begin{array} { l l } { 1 , } & { { \mathrm { i f ~ t _ n \leq \lambda _ { t h } ~ } } , } \\ { 0 , } & { { \mathrm { i f ~ t _ n > \lambda _ { t h } ~ } } , } \end{array} \right. }\tag{10}
$$

where $t _ { n }$ is the communication latency incurred by UAV n, and its details are described in Section III-C.

Therefore, the reputation value $\boldsymbol { r } _ { n } ^ { t }$ of the UAV n in the round t can be calculated as follows:

$$
\begin{array} { r } { r _ { n } ^ { t } = \gamma _ { m  n } \cdot f ( t _ { n } , \lambda _ { t h } ) . } \end{array}\tag{11}
$$

## C. MAB-Based Worker Selection Scheme

The inherent uncertainty in UAV reputation during semantic information trading poses challenges for designing effective recruitment mechanisms. An MAB framework has been conceptualized as the learning strategy to navigate the balance between exploitation and exploration [31]. Compared with blockchain technologies, the flexibility and adaptability of the MAB algorithm make it a well-suited scheme for accommodating real-time adjustments in reputation values within the context of dynamic UAV swarm network [32].

To address the challenge of UAV reputations being nonstationary on a long-term basis, we adopt MAB which utilizes an estimator to adapt to the time-varying environment. Within the MAB framework, a slot machine holds multiple arms, each corresponding to an action. Pulling an arm generates a stochastic reward drawn from a probability distribution. Players decide which set of arms to pull to maximize their cumulative rewards.

We model the worker selection problem as a non-stationary MAB problem, where the cluster head and the UAVs are regarded as the player and the arms, respectively. The chosen subset of the arms $W _ { t }$ is regarded as a super arm and the corresponding reputation values of UAVs are seen as the reward for pulling the arm. The cluster head pulls k arms in every round and learns each selected UAVâs reward, i.e., reputation value. We estimate reputation value $\bar { r } _ { n } ^ { t }$ by computing weighted averages Â¯from their historical snapshots, which is represented as follows:

$$
\bar { r } _ { n } ^ { t } = \frac { 1 } { N _ { n } ^ { t } } \sum _ { s = 1 } ^ { t } \zeta ^ { t - s } r _ { n } ^ { s } \mathbb { I } _ { \{ n \in W _ { s } \} } ,\tag{12}
$$

where

$$
N _ { n } ^ { t } = \sum _ { s = 1 } ^ { t } \zeta ^ { t - s } \mathbb { I } _ { \{ n \in W _ { s } \} } ,\tag{13}
$$

$$
\mathbb { I } _ { \{ n \in W _ { s } \} } = \left\{ { \begin{array} { l l } { 1 , } & { { \mathrm { i f ~ } } n \in W _ { s } , } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } , } \end{array} } \right.\tag{14}
$$

where $N _ { n } ^ { t }$ is a normalization coefficient that indicates the number of times that cluster head selects UAV n until round t, and $\zeta \in ( 0 , 1 )$ is the discount factor. It allows us to progressively reduce the impact of past observations exponentially to aid in the tracking of changes in mean rewards. Essentially, a higher Î¶ leads to smoother estimation and a slower response to breakpoint.

```perl
Algorithm 1: MAB-Based Online Worker Selection Algo
rithm.
Input: The fixed setting about selected workers $F ;$
Workers availability I.
Output: Selected worker set $W _ { t }$
1 Initialization: Success probability of transmission Î² and
the probability of positive interactions $p ;$
2 Exploration phase:
3 while $t < n _ { l }$ do
4 Recruit worker t for DT construction task;
5 Update $\bar { r } _ { n } ^ { t }$ and $N _ { n } ^ { t }$ according to (12)-(14);
6 $t = t + 1 ;$
7 end
8 Exploitation phase:
9 while $t < T$ do
10 Obtain $\begin{array} { r } { k = \operatorname* { m i n } \{ m , \sum _ { n \in \mathcal { N } } I _ { t , n } \} ; } \end{array}$
11 Calculate $\hat { r } ^ { t }$ according to (15) and sort the workers in
a descending order;
12 Choose k workers with the largest reputation values
into $W _ { t } ;$
13 $t = t + 1 ;$
14 foreach worker w in $W _ { t }$ do
15 Update $\hat { r } _ { w } ^ { t }$ according to (12)-(14);
16 Update $p _ { w } = p _ { w } + 1$ or $q _ { w } = q _ { w } + 1 ;$
17 end
18 end
```

To strike a balance between exploitation and exploration, we employ Upper Confidence Bound (UCB) policies [33]. By introducing an additional bonus term, the UCB policy incentivizes the cluster head to collect more observations from under-sampled UAVs. We denote UCB indexes of workers, where the uncertainty of estimation is taken into consideration, as follows:

$$
\hat { r } _ { n } ^ { t } = \bar { r } _ { n } ^ { t } + \sqrt { \frac { \eta \ln p _ { n } ^ { t } } { N _ { n } ^ { t } } } ,\tag{15}
$$

where

$$
p _ { n } ^ { t } = \sum _ { n = 1 } ^ { n _ { l } } N _ { n } ^ { t } .\tag{16}
$$

Here, $\eta$ is an exploration constant that controls the adaptability into our policy, and $p _ { n } ^ { t }$ is the summation of $N _ { n } ^ { t }$ across time steps t.

Leveraging the UCB criterion, the behavioral decision of selecting k workers for the data synchronization task is accordingly determined by

$$
W _ { t } = \underset { | W _ { t } | = k } { \arg \operatorname* { m a x } } ~ \sum _ { n \in W _ { t } } \hat { r } _ { n } ^ { t } .\tag{17}
$$

## D. The Proposed Algorithm

As shown in Algorithm 1, we propose a worker selection algorithm based on the Discounted-UCB policy which considers both the reputation score and the communication latency of each worker. We first initialize $\beta$ and $p .$ In the exploration phase, we observe each workerâs reputation value at least once to update the values of $\hat { r } _ { n } ^ { t }$ and $N _ { n } ^ { t }$ . In the exploitation phase, we make use of the acquired reputations from the preceding exploration phase to make decisions about the selection of workers. In line 10, we first obtain the number of clients that should be picked. In line 11, we calculate the reward, i.e., the reputation value of choosing each worker, and sort the workers in descending order of their UCB scores. Here we adopt a greedy strategy to choose the best k workers into the winning set $W _ { t }$ . The selected workers are employed to engage in data synchronization and their positive or negative interactions will be updated and recorded by their respective cluster heads at the end of each round.

Given that the other computational procedures only involve elementary numerical operations, the computational complexity of the algorithm depends on the choice of the search algorithm employed for the identification of the highest UCB index. This complexity inherently varies with the number of arms involved. Specifically, if we use merge sort to arrange the UCB scores of $n _ { l }$ arms, the computational complexity of the algorithm will be characterized by $O ( n _ { l }$ nl .

## V. UPPER LAYER: DL-BASED AUCTION DESIGN

After the online worker selection described in Section VI, the cluster head, i.e., UAV-BS, receives the semantic information from its chosen workers and conducts information fusion. In this section, we design a continuous dynamic multi-round auction, enabling the successive semantic information trading between UAV-BSs and VSPs based on auction results. Note that the situation of auction interaction is recorded and returned to the cluster head for the purpose of updating workersâ reputations.

## A. The Semantic Information Market

We consider a semantic information market with L UAV-BSs and M VSPs. The objective of the market is to trade semantic information from the UAV swarm, which will facilitate the generation of digital copies within the VSPs. In this market, we consider a multi-round single-item auction to simplify the problem, where the VSP acts as the buyer and UAV-BS acts as the seller [34].

VSP (Buyer): The buyers provide payment to the sellers for acquiring the semantic information. Before each round of auction, each VSP submits the bid to its auctioneer. Given that all UAVs do not have the same match level and reputation value caused by their location, hardware specifications, and semantic model quality, the VSP needs to bid according to data relatedness and effectiveness of receiving semantic information.

UAV-BS (Seller): In this market, the sellers are the UAV-BSs that offer VSP semantic symbols. Upon receiving the bid profile, the UAV-BS selects the winning VSP for semantic information trading and decides the corresponding payment from the winning VSP.

Information exchange including bids and auction-related variables takes place between the cluster heads and VSPs via wireless links. The UAV swarm initializes the auction process after the fusion of semantic information by all the cluster heads. In every round of the multi-round single-item auction, the VSPs make their own private and independent valuation for the semantic information of the seller upon reception of the announcement. Thereinafter, the auctioneer collects bidding profiles $( b _ { 1 } , b _ { 2 } , . . . , b _ { m } , . . . , b _ { M } )$ from all VSPs and determines (the winning VSP $m ^ { * }$ )along with the corresponding payment price $p _ { m } ^ { * }$ . The valuation, i.e., the private value, of VSP m for semantic information is denoted as $v _ { m }$ . The utility of the VSP is considered as:

$$
u _ { m } = \left\{ { \begin{array} { l l } { v _ { m } - p _ { m } ^ { * } , } & { { \mathrm { i f ~ } } \mathrm { V S P ~ } m { \mathrm { ~ i s ~ t h e ~ w i n n e r } } . } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } . } \end{array} } \right.\tag{18}
$$

To ensure system stability and guarantee the truthfulness of participants, the auction mechanism should possess desirable attributes, namely, Incentive Compatibility (IC) and Individual Rationality (IR) [35]. IC indicates the workers can maximize their utility by submitting truthful bids without considering the bids of other participants, i.e., $b _ { m } = v _ { m }$ . IR guarantees that =involvement in the auction results in non-negative utility for all participants, thereby motivating their participation in the semantic information trading market, denoted as $u _ { m } \geq 0$

0Nonetheless, conventional single-item auction mechanisms, e.g., First-Price Auction (FPA) and Second-Price Auction (SPA), do not invariably guarantee the IC and IR properties. In the FPA, although revenue-optimal is ensured, the IC property is not satisfied. In the SPA, the second highest valuation determines the final payment even though the IC property is satisfied. Thus, we propose suitable allocation and pricing schemes to ensure the fulfillment of these two properties in our auction mechanism.

## B. Valuation Model

Here, we propose a valuation model for VSPs to better acquire semantic information.

Given the multiple services offered by VSPs, it is evident that each VSP shows different interests and objectives when participating in the bidding process for semantic information acquisition. We consider the VSPâs preference for semantic information as well as the reputation level of UAVs. According to the RelTR model introduced in Section III-C for extracting semantic information, we denote the count of semantic triplets for the UAV-BS l as $T _ { l }$ and the number of objects acquired by VSP m as $O _ { m }$ , respectively. Similar to [36], the preference, i.e., semantic match level, between VSP m and UAV-BS l is given by:

$$
a _ { m , l } = \left( \sum _ { t = 0 } ^ { T _ { l } } \left( \sum _ { o = 1 } ^ { O _ { m } } i + \sum _ { o = 1 } ^ { O _ { m } } j \right) \right) \bigg / 2 T _ { l } ,\tag{19}
$$

where i and j are binary variables. Specifically, i  when $o = t _ { l , a } , j = 1$ when $o = t _ { l , b }$

= = 1 =Meanwhile, the valuation of the semantic information also depends on the transmission latency, which represents how quickly the semantic information is conveyed to the VSP. The valuation function of VSP m receiving semantic information from cluster head l can be defined as $v _ { m } = a _ { m , l } \bar { r } _ { m }$

<!-- image-->  
Fig. 4. Illustration of the DL-based optimal auction.

## C. Optimal Auction Design

In this section, we adopt a deep learning-based approach [37] for the single-item auction as presented in Section V-A.

We elaborate on the DL-based optimal auction, which maximizes the expected revenue for the sellers, while concurrently ensuring IR and IC constraints. Noted that the auctioneer operates without prior knowledge regarding the bidders and the determination of the winner. The cluster head can optimize the auction decision through a neural network architecture that contains three key components: a monotone transform function Ï representing virtual valuation, an allocation rule $g _ { i } ,$ , and a payment rule $p _ { i } .$ . In Fig. 4, we illustrate the the DL-based optimal auction. Next, we describe the details of the three functions.

1) Monotone Transform Function: The proposed optimal auction mechanism utilizes virtual valuation transform functions, denoted as $\phi _ { m } , m = 1 , . . . , M$ , to derive allocation rule = 1and payment rule in the neural network. Virtual valuation transform functions are strictly monotonically increasing, satisfying the IC and IR characteristics of the auction.

First, the input bid $b _ { m }$ of VSP is transform into virtual bids $\bar { b } _ { m } = \phi _ { m } ( b _ { m } )$ . Each $\phi _ { m }$ is modeled as a two-layer feedforward = ( )network, featuring K sets of J linear functions. In the network, we make use of operators such as min and max across multiple linear functions. Accordingly, the transform function $\phi _ { m }$ is given by:

$$
\phi _ { m } ( b _ { m } ) = \operatorname* { m i n } _ { k = 1 , \ldots , K } \operatorname* { m a x } _ { j = 1 , \ldots , J } \left( \omega _ { k j } ^ { m } b _ { m } + \beta _ { k j } ^ { m } \right) .\tag{20}
$$

The inverse transform $\phi _ { m } ^ { - 1 } ( y )$ can be derived from the transform function as follows:

$$
\phi _ { m } ^ { - 1 } ( y ) = \operatorname* { m a x } _ { k = 1 , \ldots , K } \operatorname* { m i n } _ { j = 1 , \ldots , J } ( \omega _ { k j } ^ { m } ) ^ { - 1 } \left( y - \beta _ { k j } ^ { m } \right) .\tag{21}
$$

2) Allocation and Payment Rules: To ensure the revenueoptimal auction, we perform the SPA with zero reserve price (SPA-0) on the transformed bid $\bar { b } _ { m } .$ . Following Theorem 1, the SPA-0 constrains the allocation rules g and payment rules $p .$

Theorem 1: For any set of strictly monotonically increasing functions $\phi _ { 1 } , . . . , \phi _ { M }$ , auction characterized by allocation rule $g _ { m } = g _ { m } ^ { 0 } \circ \phi _ { m }$ and the payment rule $p _ { m } = \phi _ { m } ^ { - 1 } \circ p _ { m } ^ { 0 }$ is IC and

IR. Here, $g ^ { 0 }$ and $p ^ { 0 }$ respective represent the allocation and payment rules of the SPA with zero reserve.

If the transformed bid is greater than zero, it becomes possible to optimize the allocation probability for the highest bid by implementing a neural network-based allocation rule inspired by SPA-0. The allocation rule can be approximated by the sof tmax operation as the output layer. Sof tmax is a function in deep learning that facilitates the transformation of a real-valued vector into another within the range of 0 to 1, which can be formulated as $\textstyle s o f t m a x ( z _ { i } ) { \frac { z _ { i } } { \sum _ { j } z _ { j } } }$ and z is a vector. In the allocation network, the networkâs inputs consist of the transformed bids $\overline { { \mathbf { b } } } = ( \overline { { b } } _ { 1 } , . . . , \overline { { b } } _ { M } )$ and an additional dummy input, while b = ( )the output is a vector representing assignment probabilities $\mathbf { g } = ( g _ { 1 } , \hdots , g _ { M } )$

$$
\begin{array} { l } { g _ { m } ( \overline { { \mathbf { b } } } ) = \mathrm { s o f t m a x } _ { i } \left( \bar { b } _ { 1 } , \dots , \bar { b } _ { M + 1 } ; \kappa \right) } \\ { \quad = \displaystyle \frac { e ^ { \kappa \bar { b } _ { m } } } { \sum _ { i = 1 } ^ { M + 1 } e ^ { \kappa \bar { b } _ { i } } } , \forall m \in M } \end{array}\tag{22}
$$

where $b _ { M + 1 }$ denotes the additional auxiliary input while $\kappa > 0$ 0impacts the quality of the approximation. A higher value of Îº leads to an increase in the quality of the approximation.

The conditional payment rule determines the price $p _ { m }$ for the winning VSP $m$ . In this process, the network calculates SPA-0 payment $p _ { m } ^ { 0 }$ using an activation function, i.e., ReLU function.

Then, it derives the conditional payment $p _ { m }$ through Theorem 1. Specifically, the input ${ \bar { b } } _ { i }$ is the larger value between transformed bids from other VSPs and zero. The payment rule network is expressed as :

$$
p _ { m } ^ { 0 } ( \overline { { \mathbf { b } } } ) = \mathrm { R e } L U \left( \operatorname* { m a x } _ { i \neq m } \bar { b } _ { i } \right) , \forall m \in M .\tag{23}
$$

Here, we employ $R e L U ( x ) = \operatorname* { m a x } ( x , 0 )$ to guarantee non-( ) = max( 0)negativity for the payment. For the payment calculation, we apply a inverse transformation function to the SPA-0 price associated with . The conditional payment to VSP m is then calculated as

$$
p _ { m } = \phi _ { m } ^ { - 1 } \left( p _ { m } ^ { 0 } \left( \overline { { { \bf b } } } \right) \right) .\tag{24}
$$

3) Neural Network Training: In the following, we define the loss function $\hat { R } ( \mathbf { w } , \beta )$ to optimize the deep learning network (w )training. More precisely, loss function is formulated by the negative expectation of revenue, which can be determined through the allocation probability $g$ and payment $p .$ The goal of the network is to achieve the minimization of the loss function, as well as optimize the weights and biases associated with the transformation function, consequently enabling the maximization of revenue for the UAV swarm.

Our dataset has L bidder valuation profiles from corresponding VSPs and $v _ { m } ^ { l }$ represents the valuation of VSP m. As previously mentioned, the valuation $v _ { m } ^ { l }$ is expressed by the corresponding match level and reputation value, both of which are independently and identically sampled from a well-defined distribution function [37]. Therefore, we can derive the distribution of $v _ { m }$ by calculating the Jacobian determinant [38]. The loss function can be calculated as:

Algorithm 2: DL-Based Auction Algorithm.   
Input:Bids from VSPs $\mathbf { b } = \left( b _ { 1 } , . . . , b _ { M } \right)$   
Output: Assignment probabilities g and conditional   
payments $\mathbf { p } ;$   
1 Initialization:   
$\mathbf { w } = [ \omega _ { k j } ^ { m } ] \in R _ { + } ^ { M \times J K } , \beta = [ \beta _ { k j } ^ { m } ] \in R ^ { M \times J K }$   
2 while $\hat { R } ( \mathbf { w } , \beta )$ is not minimized do   
3 Calculate transformed bid $\bar { b } _ { m } = \phi _ { m } ( b _ { m } ) =$   
$\begin{array} { r } { \operatorname* { m i n } _ { k = 1 , \dots , K } \operatorname* { m a x } _ { j = 1 , \dots , J } ( \omega _ { k j } ^ { m } b _ { m } + \beta _ { k j } ^ { m } ) . } \end{array}$   
4 Compute the allocation probabilities   
$\begin{array} { r } { g _ { m } = \mathrm { s o f t m a x } _ { i } \left( \bar { b } _ { 1 } , \ldots , \bar { b } _ { M + 1 } ; \kappa \right) = \frac { e ^ { \kappa \bar { b } _ { m } } } { \sum _ { i = 1 } ^ { M + 1 } e ^ { \kappa \bar { b } _ { i } } } . } \end{array}$   
5 Compute the SPA-O payments   
$p _ { m } ^ { 0 } = \mathrm { R e } L U \left( \operatorname* { m a x } _ { i \neq m } \bar { b } _ { m } \right)$   
6 Compute the conditional payment $p _ { m } = \phi _ { m } ^ { - 1 } ( p _ { m } ^ { 0 } ( \mathbf { \overline { { b } } } ) )$   
7 Compute the loss $\begin{array} { r } { \hat { R } ( \mathbf { w } , \beta ) = - \sum _ { m = 1 } ^ { M } g _ { m } ( \overline { { \mathbf { b } } } ) p _ { m } . } \end{array}$   
8 Calculate $\mathbf { w } , \beta$ using SGD solver   
9 end   
10 return Winner $m ^ { * }$ ï¼payment $\mathbf { p } ^ { * }$

$$
\hat { R } ( \mathbf { w } , \beta ) = - \sum _ { m = 1 } ^ { M } g _ { m } ( \overline { { \mathbf { b } } } ) p _ { m } ,\tag{25}
$$

where  and $\beta$ are the matrices that contain weights and biases, wrespectively. The optimization of the loss function is achieved by applying a Stochastic Gradient Descent (SGD) solver to adjust the parameters $\left( \mathbf { w } , \beta \right)$

## D. Algorithm Complexity Analysis

The DL-based auction algorithm is presented in Algorithm 2. The computation cost mainly depends on the DL model training and decision-making [34]. In the DL-based auction model training stage, the training time is mostly used to assess the computation complexity. In the decision-making stage, the matrix operation and the activation function computation are considered for computation complexity evaluation. Therefore, the computation complexity of Algorithm 2 is expressed as $( O _ { M } ( i _ { n } ) + O _ { A } ( i _ { n } ) ) * i _ { l }$ , where $i _ { n }$ is the number of nodes within the network, $i _ { n }$ is the number of layers, and $O _ { M } ( \ u )$ and $O _ { A } ( . )$ are computation complexity associated with the matrix ( )operation and the activation function computation for each layer, respectively.

## VI. EXPERIMENT RESULTS

In this section, we assess the effectiveness of proposed worker selection scheme and DL-based auction method for DT construction.

## A. Simulation Setup

We consider a metaverse-based UAV swarm network with 10 UAV-BS as cluster heads, 100 UAVs, and 5 VSPs. Our experiments are conducted on the VisDrone2019 dataset, a remotely sensed image dataset collected by UAVs [24]. The

TABLE II PARAMETER SETTING
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Number ofUAV-BSs,L</td><td>10</td></tr><tr><td>Number of  $\mathrm { U A V s } , N$ </td><td>100</td></tr><tr><td>Success probability of transmission,  $\beta$ </td><td>[0.8,1]</td></tr><tr><td>Level of uncertainty for reputation,Î¸</td><td>0.5</td></tr><tr><td>Exploration constant,n</td><td>1.5</td></tr><tr><td>Semantic information size of UAV, w</td><td>3Mbit-5Mbit</td></tr><tr><td>Bandwidth ofUAV,B</td><td>8MHz-10MHz</td></tr><tr><td>Transmit power of  $\mathrm { U A V } , p$ </td><td>1W</td></tr><tr><td>Channel Gain of  $\mathrm { U A V } , h$ </td><td>5dBm-25dBm</td></tr><tr><td>Power spectral density of noise,  $N _ { 0 }$ </td><td>-169dBm/HZ</td></tr><tr><td>Lowest latency requirement,  $\lambda _ { t h }$ </td><td>0.5s</td></tr></table>

<!-- image-->  
Fig. 5. Average reward versus the number of workers.

VisDrone2019 dataset has 10 classes and 54,200 instances of objects, including diverse and complex scenes under various weather and lighting conditions. The training and validation subsets consist of 7018 and 1609 images, respectively. The predefined deep learning model, i.e., the RelTR model, is deployed in each UAV to extract the corresponding semantic symbols. The parameter settings are given in Table II.

## B. Results of Worker Selection Scheme

First, we conduct an analysis of the worker selection scheme. The performance evaluation of our scheme is based on an average of over 10,000 rounds. We compare the performance of our algorithm with the following baseline schemes:

Oracle Scheme: Oracle is the theoretically optimal method and always selects the best k workers in each round based on prior knowledge.

Îµ-Greedy Scheme: This scheme combines the exploration and exploitation by using a parameter Îµ. At each round t, it explores workers with probability Îµ and exploits the best workers with probability  â Îµ. For a more comprehensive analysis of algorithm performance, two variants of the method were employed, with Îµ values set to 0.3 and 0.7, respectively.

Random Scheme: The Random scheme randomly chooses k workers in each selection. This scheme ensures randomized exploration of available workers by the cluster head.

As shown in Fig. 5, we evaluate the average reward curves by varying the number of available workers when $k = 3$ . It can be found that the average reward obtained under our proposed scheme is slightly lower than the Oracle scheme, primarily due to the exploration actions. Meanwhile, the 0.3-Greedy scheme and 0.7-Greedy scheme exhibit similar performances, but their average rewards are both lower than our proposed approach. Given the severely suboptimal worker selection, the Random scheme has the lowest reward. As the value of $n _ { l }$ increases, it illustrates an increasing trend in the average rewards for all schemes. This phenomenon can be attributed to the emergence of more workers with higher reputations and less time delay, thereby promoting a better selection process compared to the previous.

<!-- image-->  
Fig. 6. Average reward versus the selected number of workers.

Fig. 6 illustrates the average reward changes when selecting a different number of workers with $n _ { l } = 1 6$ We can observe that = 16even with variations in the recruitment quantity of workers, our scheme still achieves satisfactory performance. It is also noteworthy that an increase in the selected number of workers results in a decrease in average rewards. This phenomenon reveals that the smaller k diminishes the recruitment of suboptimal workers in each round.

To assess the algorithmâs effectiveness in dynamic UAV network scenarios, we initially conducted 1000 rounds of selection among 6 workers. Then, we add 6 new workers to the worker set and conduct another 1000 rounds of selection among all the available workers. The algorithmâs adaptability to worker selection in highly dynamic scenarios within the UAV swarm can be assessed by examining the selection results for the newly added nodes in the last 1000 rounds. Note that the initial reputation values are set as 0.5. The selection ratio for the original 6 workers in the last 1000 rounds is illustrated in Fig. 7. The Oracle scheme consistently selects workers $w _ { 1 } , w _ { 3 }$ with the highest reputations based on known information. It is crucial to note that this approach is impractical in the real-world scenario and is used merely to represent the theoretically optimal solution. In contrast, the random scheme uniformly selects each worker with almost equal probability. Our proposed method exhibits a tendency to select workers with the highest reputation values while also allocating certain selection opportunities to other workers. These observations verify the performance of our scheme when dealing with the exploration-exploitation trade-off.

<!-- image-->  
Fig. 7. Ratio of selected original workers.

<!-- image-->  
Fig. 8. Ratio of selected newly added workers.

Fig. 8 shows the selection ratio of newly added workers. For the later participating workers with a high probability of positive interactions, the 0.3-Greedy scheme prioritizes the selection of existing workers and seldom chooses them. In contrast, the 0.7-Greedy scheme has the opportunity for exploration but with limited utilization, thus leading to unsatisfactory results. According to our proposed scheme, we observe that newly added workers have enough opportunities to update their true reputation values, and their chances are not less compared to existing workers. This implies that our scheme is effective and robust in the dynamic UAV swarm network compared to the baselines.

## C. Evaluation of DL-Based Auction

In this section, we experimentally validate the effectiveness of our DL-based optimal auction algorithm.

We employ the TensorFlow deep learning library to construct a neural network for the implementation of the proposed algorithm. The learning rate for the neural network is set to 0.001.

TABLE III SIMULATION PARAMETERS
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Total number of VSPs,M</td><td>5,10,15</td></tr><tr><td>Training dataset size,L</td><td>10000</td></tr><tr><td>Learning rate</td><td>0.001</td></tr><tr><td>Number of groups,Q</td><td>5</td></tr><tr><td>Number of linear functions,S</td><td>10</td></tr><tr><td>Quality of approximation K</td><td>1000,2000</td></tr><tr><td>Range of match level,  $a _ { m }$ </td><td> $\sim U [ 0 . 3 , 0 . 6 ] , U [ 0 . 6 , 0 . 9 ]$ </td></tr><tr><td>Range of reputation value,  $\bar { r } _ { m }$ </td><td>~U[0.5,1]</td></tr></table>

<!-- image-->  
Fig. 9. Test revenue statistics for 5 VSPs.

In the neural network, each transformation function $\phi _ { m }$ is structured by utilizing 5 groups of 10 linear functions. Furthermore, to investigate the impact of the parameter Îº on the softmax activation function, we consider two values, i.e., $\kappa = 1 0 0 0$ and $\kappa = 2 0 0 0$

= 2000The training dataset L has 10,000 valuation profiles of semantic information provided to the VSP. The valuations are associated with the level of semantic matching and the reputation values of UAVs. More specifically, the match level $a _ { m }$ and the average reputation value $\bar { r } _ { m }$ are drawn from the distributions $f _ { A } ( a _ { m } )$ and $f _ { R } ( \bar { r } _ { m } )$ Â¯, respectively. For comparison, we imple-( ) (Â¯ )ment the SPA as a baseline scheme. Simulation parameters used are shown in Table III.

1) Revenue Analysis: Under different system settings, we evaluate the proposed scheme in comparison to the baseline algorithm. From Figs. 9, 10 and 11, we find that the DL-based auction yields revenue outperforming those achieved by the baseline scheme for the given number of VSPs and distributions. This indicates that the proposed scheme can maximize the expected revenue while achieving the IC and IR. In the case of $N = 5$ and $a _ { m } \sim U [ 0 . 6 , 0 . 9 ]$ , we can observe that the revenue = 5 [0 6 0 9]obtained by our scheme is 0.2082 with Îº  2000 whereas =the SPA is 0.1966. It is clear that our scheme produces better performance compared to the baseline.

2) The Impact of the VSPs With Different Distributions: Then, we consider the impact of different uniform distributions on the cluster headâs revenue. As depicted in Fig. 10, the expected revenue has increased with $a _ { m }$ following distribution

<!-- image-->  
Fig. 10. Test revenue statistics for 10 VSPs.

<!-- image-->  
Fig. 11. Test revenue statistics for 15 VSPs.

U . , . while revenue is lower with $a _ { m } \sim U [ 0 . 3 , 0 . 6 ]$ . The [0 6 0 9] [0 3 0 6]reason is that the bids of VSPs are positively proportional to the $a _ { m }$ . We can also find similar trends in other settings, i.e., as evidenced in Figs. 9 and 11.

3) The Impact of the Parameter Îº: We next show the impact of the parameter Îº on the expected revenue of the cluster head. From Fig. 11, as $N = 1 5$ and $a _ { m } \sim U [ 0 . 6 , 0 . 9 ]$ , the expected = 15 [0 6 0 9]revenues derived from our algorithm are 0.4096 and 0.4031 for $\kappa = 1 0 0 0 \mathrm { a n d } \kappa = 2 0 0 0$ , respectively. The results confirm that = =higher approximation quality slightly increases the correctness of the winnerâs decision as well as decreases the expected revenue.

4) The Impact of the Number of VSPs: Further, we assess the impact of the number of VSPs on the cluster headâs revenue. Fig. 12 shows the results for different numbers of sellers with the distribution $a _ { m } \sim U [ 0 . 6 , 0 . 9 ]$ . We can find that the revenue [0 6 0 9]of the UAV swarm has improved with an increased number in VSPs. The reason is that more VSPs will intensify the competition, which potentially motivates VSPs to submit higher bidding prices. Consequently, the revenue of the cluster head increases as more buyers participate in this auction.

<!-- image-->  
Fig. 12. Test revenue statistics under different VSPs.

## VII. CONCLUSION

In this paper, the semantic-aware UAV swarm in the metaverse has been investigated. Leveraged by the proposed hierarchical game-theoretic framework, efficient and timeliness data synchronization can be realized which supports the seamless virtual services of VSPs in the metaverse. In the lower layer, the cluster head chooses reliable workers in order to facilitate data synchronization. To accomplish this, we develop an MAB-based worker selection scheme which considers the reputation value and communication latency of workers in the selection process. In the upper layer, we propose a DL-based auction algorithm for semantic information trading between UAV-BSs and VSPs, where an optimal solution guaranteeing IR and IC can be attained. Numerical results demonstrate the proposed algorithm can improve the revenue of UAVs compared to baseline schemes. In future work, it is meaningful to extend our work considering task allocation optimization, trajectory design, and information fusion mode.

## REFERENCES

[1] S. Javaid et al., âCommunication and control in collaborative UAVs: Recent advances and future trends,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 6, pp. 5719â5739, Jun. 2023.

[2] Z. Chang, H. Deng, L. You, G. Min, S. Garg, and G. Kaddoum, âTrajectory design and resource allocation for multi-UAV networks: Deep reinforcement learning approaches,â IEEE Trans. Netw. Sci. Eng., vol. 10, no. 5, pp. 2940â2951, Sep./Oct. 2023.

[3] G. Shen et al., âDeep reinforcement learning for flocking motion of multi-UAV systems: Learn from a digital twin,â IEEE Internet Things J., vol. 9, no. 13, pp. 11 141â11 153, Jul. 2022.

[4] L. Zhou, S. Leng, and Q. Wang, âA federated digital twin framework for UAVs-based mobile scenarios,â IEEE Trans. Mobile Comput., vol. 23, no. 6, pp. 7377â7393, Jun. 2024.

[5] L. U. Khan, Z. Han, D. Niyato, M. Guizani, and C. S. Hong, âMetaverse for wireless systems: Vision, enablers, architecture, and future directions,â 2022, arXiv:2207.00413.

[6] S. Cai and Y. Xu, âA multi-objective optimization approach to resource allocation for edge-based digital twin,â in Proc. IEEE Glob. Commun. Conf., 2022, pp. 2733â2738.

[7] W. Sun, N. Xu, L. Wang, H. Zhang, and Y. Zhang, âDynamic digital twin and federated learning with incentives for air-ground networks,â IEEE Trans. Netw. Sci. Eng., vol. 9, no. 1, pp. 321â333, Jan./Feb. 2022.

[8] L. U. Khan, Z. Han, W. Saad, E. Hossain, M. Guizani, and C. S. Hong, âDigital twin of wireless systems: Overview, taxonomy, challenges, and opportunities,â IEEE Commun. Surv. Tuts., vol. 24, no. 4, pp. 2230â2254, Fourth Quarter 2022.

[9] G. Ji, J.-G. Hao, J.-L. Gao, and C.-Z. Lu, âDigital twin modeling method for individual combat quadrotor UAV,â in Proc. IEEE 1st Int. Conf. Digit. Twins Parallel Intell., 2021, pp. 1â4.

[10] M. G. Kapteyn, J. V. Pretorius, and K. E. Willcox, âA probabilistic graphical model foundation for enabling predictive digital twins at scale,â Nature Comput. Sci., vol. 1, no. 5, pp. 337â347, 2021.

[11] B. Du et al., âYOLO-based semantic communication with generative AIaided resource allocation for digital twins construction,â IEEE Internet Things J., vol. 11, no. 5, pp. 7664â7678, Mar. 2024.

[12] Y. Han, D. Niyato, C. Leung, C. Miao, and D. I. Kim, âA dynamic resource allocation framework for synchronizing metaverse with IoT service and data,â in Proc. IEEE Int. Conf. Commun., 2022, pp. 1196â1201.

[13] G. Shi, Y. Xiao, Y. Li, and X. Xie, âFrom semantic communication to semantic-aware networking: Model, architecture, and open problems,â IEEE Commun. Mag., vol. 59, no. 8, pp. 44â50, Aug. 2021.

[14] X. Luo, H.-H. Chen, and Q. Guo, âSemantic communications: Overview, open issues, and future research directions,â IEEE Wireless Commun., vol. 29, no. 1, pp. 210â219, Feb. 2022.

[15] L. Lei, G. Shen, L. Zhang, and Z. Li, âToward intelligent cooperation of UAV swarms: When machine learning meets digital twin,â IEEE Netw., vol. 35, no. 1, pp. 386â392, Jan./Feb. 2021.

[16] P. Si, W. Yu, J. Zhao, K.-Y. Lam, and Q. Yang, âUAV aided metaverse over wireless communications: A reinforcement learning approach,â 2023, arXiv:2301.01474.

[17] N. C. Luong et al., âOptimal auction for effective energy management for UAV-assisted metaverse synchronization system,â in Proc. IEEE 20th Consum. Commun. Netw. Conf., 2023, pp. 392â397.

[18] H. Shi, G. Liu, K. Zhang, Z. Zhou, and J. Wang, âMARL Sim2real transfer: Merging physical reality with digital virtuality in metaverse,â IEEE Trans. Syst., Man, Cybern. Syst., vol. 53, no. 4, pp. 2107â2117, Apr. 2023.

[19] H. Xie, Z. Qin, G. Y. Li, and B.-H. Juang, âDeep learning enabled semantic communication systems,â IEEE Trans. Signal Process., vol. 69, pp. 2663â 2675, 2021.

[20] Z. Weng, Z. Qin, X. Tao, C. Pan, G. Liu, and G. Y. Li, âDeep learning enabled semantic communications with speech recognition and synthesis,â IEEE Trans. Wireless Commun., vol. 22, no. 9, pp. 6227â6240, Sep. 2023.

[21] D. Huang, X. Tao, F. Gao, and J. Lu, âDeep learning-based image semantic coding for semantic communications,â in Proc. IEEE Glob. Commun. Conf., 2021, pp. 1â6.

[22] H. Zhang, S. Shao, M. Tao, X. Bi, and K. B. Letaief, âDeep learningenabled semantic communication systems with task-unaware transmitter and dynamic data,â IEEE J. Sel. Areas Commun., vol. 41, no. 1, pp. 170â185, Jan. 2023.

[23] D. Huang, F. Gao, X. Tao, Q. Du, and J. Lu, âToward semantic communications: Deep learning-based image semantic coding,â IEEE J. Sel. Areas Commun., vol. 41, no. 1, pp. 55â71, Jan. 2023.

[24] P. Zhu et al., âDetection and tracking meet drones challenge,â IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 11, pp. 7380â7399, Nov. 2022.

[25] J. Chen, X. Zhang, R. Zhang, C. Wang, and L. Liu, âDe-Pois: An attack-agnostic defense against data poisoning attacks,â IEEE Trans. Inf. Forensics Secur., vol. 16, pp. 3412â3425, 2021.

[26] Y. Cong, M. Y. Yang, and B. Rosenhahn, âRelTR: Relation transformer for scene graph generation,â IEEE Trans. Pattern Anal. Mach. Intell., vol. 45, no. 9, pp. 11169â11183, Sep. 2023.

[27] X. Kang, B. Song, J. Guo, Z. Qin, and F. R. Yu, âTask-oriented image transmission for scene classification in unmanned aerial systems,â IEEE Trans. Commun., vol. 70, no. 8, pp. 5181â5192, Aug. 2022.

[28] A. S. Matar and X. Shen, âJoint subchannel allocation and power control in licensed and unlicensed spectrum for multi-cell UAV-cellular network,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3542â3554, Nov. 2021.

[29] T. Huang, W. Lin, W. Wu, L. He, K. Li, and A. Y. Zomaya, âAn efficiency-boosting client selection scheme for federated learning with fairness guarantee,â IEEE Trans. Parallel Distrib. Syst., vol. 32, no. 7, pp. 1552â1564, Jul. 2021.

[30] T. Cheng, G. Liu, Q. Yang, and J. Sun, âTrust assessment in vehicular social network based on three-valued subjective logic,â IEEE Trans. Multimedia, vol. 21, no. 3, pp. 652â663, Mar. 2019.

[31] W. Chen, Y. Wang, and Y. Yuan, âCombinatorial multi-armed bandit: General framework and applications,â in Proc. Int. Conf. Mach. Learn., 2013, pp. 151â159.

[32] H. Xiao, L. Cai, J. Feng, Q. Pei, and W. Shi, âResource optimization of MAB-based reputation management for data trading in vehicular edge computing,â IEEE Trans. Wireless Commun., vol. 22, no. 8, pp. 5278â5290, Aug. 2023.

[33] A. Garivier and E. Moulines, âOn upper-confidence bound policies for switching bandit problems,â in Proc. Int. Conf. Algorithmic Learn. Theory, Springer, 2011, pp. 174â188.

[34] K. Zhu, Y. Xu, Q. Jun, and D. Niyato, âRevenue-optimal auction for resource allocation in wireless virtualization: A deep learning approach,â IEEE Trans. Mobile Comput., vol. 21, no. 4, pp. 1374â1387, Apr. 2022.

[35] M. Babaioff and W. E. Walsh, âIncentive-compatible, budget-balanced, yet highly efficient auctions for supply chain formation,â in Proc. 4th ACM Conf. Electron. Commerce, 2003, pp. 64â75.

[36] Z. Q. Liew, H. Du, W. Y. B. Lim, Z. Xiong, D. Niyato, and H. Yu, âEconomics of semantic communication in metaverse: An auction approach,â in Proc. IEEE 20th Consum. Commun. Netw. Conf., 2023, pp. 398â403.

<!-- image-->

[37] P. DÃ¼tting, Z. Feng, H. Narasimhan, D. Parkes, and S. S. Ravindranath, âOptimal auctions through deep learning,â in Proc. Int. Conf. Mach. Learn., 2019, pp. 1706â1715.

[38] N. C. Luong, Z. Xiong, P. Wang, and D. Niyato, âOptimal auction for edge computing resource management in mobile blockchain networks: A deep learning approach,â in Proc. IEEE Int. Conf. Commun., 2018, pp. 1â6.

<!-- image-->  
Jiaqi Xu (Student Member, IEEE) received the bachelorâs degree from the Beijing University of Posts and Telecommunications and is currently working toward the PhD degree with the Beijing University of Posts and Telecommunications. Her research interests include future network, multi-agent system, and game theory.

<!-- image-->

Shan Huang (Student Member, IEEE) is currently working toward the PhD degree with the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing, China. His research interests include future network architecture, network artificial intelligence, multi-agent system, space-terrestrial integrated network, network resource allocation, and dedicated networks.

<!-- image-->

Haipeng Yao (Senior Member, IEEE) received the PhD degree from the Department of Telecommunication Engineering, University of Beijing University of Posts and Telecommunications, in 2011. He is a professor with the Beijing University of Posts and Telecommunications. His research interests include future network architecture, network artificial intelligence, networking, space-terrestrial integrated network, network resource allocation, and dedicated networks. He has published more than 150 papers in prestigious peer-reviewed journals and conferences.

Tianle Mai (Member, IEEE) received the PhD degree from the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, Beijing. His research interests include unmanned swarm networks, future network architecture, network artificial intelligence, multiagent system, space-terrestrial integrated network, network resource allocation, and dedicated networks. He has published more than 30 papers in prestigious peer-reviewed journals and conferences.

<!-- image-->

Zehui Xiong (Member, IEEE) is an assistant professor with the Singapore University of Technology and Design, and also an honorary adjunct senior research scientist with Alibaba-NTU Singapore Joint Research Institute, Singapore. His research interests include wireless communications, Internet of Things, blockchain, edge intelligence, and Metaverse.

He has served as an associate editor of IEEE Transactions on Mobile Computing, IEEE Transactions on Sustainable Computing.

<!-- image-->

Ru Zhang is a professor with the Beijing University of Posts and Telecommunications. Her research interests include fiber optic communication, information functional materials and devices, and quantum information. She has published more than 200 papers in conference and journal papers including the Advanced Composites and Hybrid Materials, Nano Research, Nano Energy, Frontiers in Chemistry, Optics Express, Optics Letters, Physical Review A, Chinese Physics Letters, and IEEE Nano.

<!-- image-->

Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand, and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada. He is a professor with the College of Computing and Data Science, Nanyang Technological University, Singapore. His research interests include the areas of mobile generative AI, edge intelligence, decentralized machine learning, and incentive mechanism design.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_4_img_1.jpeg|page_4_img_1]]
3. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_4_img_2.jpeg|page_4_img_2]]
4. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_8_img_1.png|page_8_img_1]]
5. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_10_img_1.jpeg|page_10_img_1]]
6. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_10_img_2.jpeg|page_10_img_2]]
7. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_13_img_1.jpeg|page_13_img_1]]
8. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_13_img_2.jpeg|page_13_img_2]]
9. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_13_img_3.jpeg|page_13_img_3]]
10. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_13_img_4.jpeg|page_13_img_4]]
11. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_13_img_5.jpeg|page_13_img_5]]
12. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_13_img_6.jpeg|page_13_img_6]]
13. [[../extracted_images/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism/page_13_img_7.jpeg|page_13_img_7]]

---

