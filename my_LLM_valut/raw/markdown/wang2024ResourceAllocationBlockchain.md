# Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks: A Stackelberg Differential Game Approach

Die Wang , Graduate Student Member, IEEE, Yunjian Jia , Member, IEEE, Liang Liang Kaoru Ota , Member, IEEE, and Mianxiong Dong , Member, IEEE

AbstractâRecently, unmanned aerial vehicle (UAV)-enabled mobile edge computing (MEC) has emerged as a practical paradigm to enable low latency computing offloading for dispersed users in the fifth generation (5G) wireless networks. However, severe security and privacy concerns are associated with the open environment between the UAVs and edge computing nodes. In this paper, we address these challenges by integrating blockchain technology into UAV-enabled MEC networks. We present an innovative Delegated Proof of Stake (DPoS) consensus mechanism where the UAV is a primary node and verification nodes are edge computing nodes selected by the reputation mechanism. To enhance mobile usersâ Quality of Service (QoS), edge computing resources need to be allocated among UAV and verification nodes. Based on this, we propose the trading mechanism for resource pricing and allocation based on the two-stage Stackelberg differential game. Meanwhile, dynamic states of user demands and verification node reputations are modeled using differential equations as constraints of the objective function at various stages to simulate adaptive service requests for users and incentivize active participation for verification nodes. Simulation results prove the effectiveness of the proposed resource trading scheme and demonstrate the equilibrium and convergence status of resource pricing and allocation for edge computing.

Index TermsâBlockchain, mobile edge computing (MEC), unmanned aerial vehicle (UAV), resource pricing, resource allocation, stackelberg differential game.

## I. INTRODUCTION

T HE rapid evolution of the Internet of Things (IoT) tech-nology and the extensive deployment of 5G wireless com- nology and the extensive deployment of 5G wireless communication networks have led to a significant increase in the number of mobile devices [1]. According to Ciscoâs Annual Internet Report, mobile devices are expected to reach 13.1 billion worldwide by 2023. With the popularity of mobile devices accessing the IoT networks, some smart applications, such as face recognition, autonomous driving, and virtual reality, are gradually penetrating humanâs daily lives [2], [3], [4]. These applications strictly impose intensive and low-latency computation requirements on mobile devices [5]. It is challenging to perform these tasks locally due to mobile devicesâ limited battery capacity and computational power [6]. Mobile Edge Computing (MEC) is indeed a valuable technology developed to enhance the computational capabilities of mobile devices [7]. As an extension of cloud computing, MEC can effectively reduces transmission delay and energy consumption by transferring computing tasks from centralized data centers to end devices located at the network edge.

However, MEC servers deployed on the ground are typically fixed in position, which restricts their ability to effectively supply a high quality of service (QoS) to end users for particular environments (sparse distribution and natural disasters) that require dynamic adaptability [8], [9]. Recently, researchers have focused on Unmanned Aerial Vehicles (UAVs) distinguished by attributes like flexible deployment, high mobility, and low cost to assist the terrestrial edge server in overcoming these limitations. Compared with classic terrestrial networks, the UAV-enabled MEC networks leverage the inherent advantage of operating at high altitudes to circumvent geographic effects to expand MEC computation services coverage to areas [10]. In addition, the line-of-sight (LoS) link is the primary communication pathway among the MEC servers and the UAVs. With the absence of obstructions along the direct communication connection, signal attenuation is reduced, resulting in more reliable and stable data transmission. As a result, the next-generation wireless communications are anticipated to bring about a transformation in network deployment. This transformation envisions a shift from conventional ground-based network infrastructure to more dynamic and integrated systems that span the air domains [11], [12]. Although UAV-enabled MEC can significantly improve

Digital Object Identifier 10.1109/TSC.2024.3418330 the ability of ground terminals to provide reliable computing services, it faces security and privacy challenges due to untrustworthy wireless communication environments [13]. These challenges may arise from the risk of distributed denial of service (DDoS) attacks overwhelming servers and the difficulties of traditional mediated transactions regarding scalability and single points of failure [14], [15]. To this end, blockchain technology is integrated into UAV-enabled networks to provide a promising solution. The decentralized and tamper-resistant character of blockchain can enhance the security, transparency, and traceability of trading between UAVs and MEC servers without depending on a central authority [16]. However, integrating blockchain in UAV-enabled MEC networks faces essential challenges posed by high mobility. The distributed nature and the consensus mechanism of blockchain may lead to trading delays and throughput limitations in high mobility scenarios. In addition, although some research has been conducted on trading with blockchain in UAV-enabled MEC networks, the secure authorization to participate and the reliable resource allocation are still issues that have yet to be thoroughly investigated. In this paper, we propose the novel trading scheme in blockchain integration of UAV-enabled MEC networks. For the proposed trading scheme, we employ blockchain technology to record the resource interactions between UAVs and verification nodes to assure security and privacy. In addition, the resource trading between the UAV and verification nodes is modeled as the Stackelberg differential game that jointly maximizes the performance for the UAV and verification nodes by determining the pricing and allocation of computational resources under the dynamic state conditions of user demands and verification node reputations. The main contributions are summarized as follows.

- A blockchain integration of UAV-enabled MEC network is proposed to maintain the security and privacy of computational offloading with low delay for mobile users. In this network, we consider an improved Delegated Proofof-Stake (DPoS) consensus mechanism where the UAV acts as a primary node to pack transactions in flight to generate the preliminary block and then hovers to pass it to the verification nodes selected from edge nodes by the reputation mechanism for further processing.

C We propose the resource trading model based on the two-stage Stackelberg differential game, considering the dynamic states of user service demand and verification nodesâ reputation as the objective function constraints. The model employs a leader and multiple followers structure to control the edge computing resource pricing and allocation strategies to optimize the utility functions of the UAV and verification nodes, respectively.

The backward induction is used to analyze the complex decision for the proposed Stackelberg differential game, which derives the unique open-loop equilibrium solution based on the Bellman dynamic programming. Furthermore, the simulation results prove the effectiveness of the proposed computational resource trading mechanism and demonstrate the steady and convergence state of resource pricing and allocation at edge networks.

The remainder of the paper is organized as follows. In Section II, we introduce the related works. Section III presents the system model. Section IV proposes a pricing and allocation scheme for computational resources based on the Stackelberg differential game. In Section V, we analyze the unique equilibrium solution of the proposed game model. Numerical simulations are illustrated in Section VI, and we conclude this paper in Section VII.

## II. RELATED WORKS

The UAV-enabled MEC networks leverage the flexibility and mobility of UAVs can enhance computing services for mobile users. To this end, extensive research has been conducted in this field [17], [18], [19], [20]. In [17], a dual computational offloading mechanism is proposed in a collaborative multi-UAVassisted MEC network approach to improve computational efficiency under massive data. In [18], online joint optimization of UAVsâ processing rates and energy consumption while meeting long-term data queue stability is considered in UAV-enabled MEC systems serving multiple energy harvesting (EH) devices. In [19], the total power optimization problem is investigated by jointly determining user association, resource allocation, and power control for the UAV-aided MEC systems. In [20], a scalable scheduling method for large-scale UAV-assisted MEC, namely HT3O, is proposed. Considering the HT3O constructed by deep reinforcement learning (DRL) with neural networks to obtain a real-time scheduling strategy for MEC in dynamic environments where the positions of UAVs and mobile devices vary greatly. However, security concerns related to UAV-enabled MEC have not been extensively addressed in the above studies. Given the open nature of wireless communication, ensuring the security and privacy of the computational offloading in UAV-enabled MEC networks is paramount.

Blockchain is a distributed ledger that utilizes cryptography to ensure data integrity and invariance [21]. Therefore, computational offloading in blockchain with UAV-enabled MEC networks has recently attracted much attention [22], [23]. In [22], a new architecture with blockchain-based drone-aided MEC is proposed to enable a comprehensive audit trail of automatic task offloading for IoT users in MEC application scenarios. In [23], a complex joint optimization problem in the blockchain-integrated drone-assisted MEC framework is modeled as the Markov decision process (MDP) to ensure maximum data computation power and throughput under the security and reliability of data transmission in compromised machine-to-machine (M2M) communication networks. However, none of the above studies have considered the problem of secure resource trading under computational offloading. For this reason, some researchers have studied resource pricing in blockchain-integrated UAV-enabled MEC networks [24], [25]. In [24], the problem of resource management and pricing in IoT systems for MEC and Blockchain-as-a-Service (BaaS) is formulated as the stochastic Stackelberg game due to incomplete information about the actions. In [25], a resource transaction scheme based on Stackelbergâs dynamic game is investigated to optimize resource allocation for edge computing between UAVs and ECSs, and blockchain technology is involved in recording the whole resource transaction procedure to defend security and privacy. In blockchain-supported resource trading, the research on the blockchain layer and UAV-MEC layer should be inextricably intertwined because transaction records need to be executed with the help of edge computing resources, which are studied separately by the above work. In addition, few studies simultaneously consider the dynamic changes in user service demand and edge resource reliability when modeling the secure resource trading problem.

<!-- image-->  
Fig. 1. A blockchain integration of UAV-enabled MEC system.

## III. SYSTEM MODEL

As shown in Fig. 1, we consider a blockchain integration of the UAV-enabled MEC network. In this network, the blockchain nodes consist of a primary node and V verification nodes. Since direct communications on the ground are disrupted, a UAV from the set of M UAVs denoted by $\mathcal { M } = \{ 1 , \dots , m , \dots , M \}$ is = 1assigned as a primary node to fly above a fixed area range to collect usersâ task offloading requirements and place them in the transaction pool. After packing the tasks in the transaction pool into preliminary blocks, the UAV transmits them to the set of V verification nodes denoted by $\mathcal { V } = \{ 1 , \ldots , v , \ldots , V \}$ = 1for further processing to minimize battery consumption. The verification nodes are filtered from the BSs configured with MEC servers according to the reputation prioritization principle. After the agreement is reached using an improved DPoS consensus mechanism, the final block including all transactions, hash results, and other important information is added to the blockchain and stored in the verification node to ensure decentralization, immutability, and traceability. To prevent malicious blockchain nodes from dominating the network, the division of computational offloading into rounds is considered. At the end of each round, the UAV performing the task is flown to the designated point to recharge and another UAV on the ground is then dispatched. In addition, the verification nodes for the next round are re-screened based on the reputation where the reputation of the verification nodes in each round is affected by the behavior results. The main notations utilized in the paper are listed in Table I.

## A. Communication Model

1) UAV Trajectory: Assume that each round of blockchain nodes lasts for a total time duration of T and divides it into K time slots of equal step length, each of which is $\begin{array} { r } { \varDelta = \frac { T } { K } } \end{array}$ =In each equal-length time slot, the blockchain nodes complete the generation of a block. We consider the flight height H of the UAV m is constant without changing over the time slot. The horizontal position of UAV m is set to be $X _ { m } ( t ) = [ x _ { m } ( t ) , y _ { m } ( t ) ]$ where $t = 1 , 2 , . . . , T$ ( ) = [ ( ) ( )]. Thus, the trajectory of the UAV m is $\{ X _ { m } ( t ) \} \mid _ { t = 0 } ^ { T }$ 2. The average speed and flight duration of UAV m at the time slot t is denoted by $\nu ( t )$ and $T _ { m } ^ { f } ( t )$ , respectively, ( ) ( )the distance flown by UAV m at the time slot t is obtained as $d _ { m } ( t ) = \nu ( t ) T _ { m } ^ { f } ( t )$ . Let Î¸ t denote the yaw angle of UAV m ( ) = ( ) ( ) ( )at time slot t, the coordinates of the UAV m at the t time slot [26] is expressed as

$$
\begin{array} { l } { { x _ { m } } \left( { t + 1 } \right) = { x _ { m } } ( t ) + { d _ { m } } ( t ) \cos \theta ( t ) , } \\ { { y _ { m } } \left( { t + 1 } \right) = { y _ { m } } ( t ) + { d _ { m } } ( t ) \sin \theta ( t ) . } \end{array}\tag{1}
$$

2) Transmission Model: Consider the coordinates of verification node v defined as $X _ { v } = [ x _ { v } , y _ { v } ]$ , the transmission dis-= [ ]tance from the UAV m to the verification node v at the time slot t by using the euclidean distance formula is

$$
d _ { m , v } ( t ) = \sqrt { \| X _ { m } ( t ) - X _ { v } \| _ { 2 } ^ { 2 } + H ^ { 2 } } ,\tag{2}
$$

where - Â· -2 represents the L2 norm. Furthermore, owing to the high possibility of line of sight (LoS) paths under the deployment of UAVs in wireless communications, the air-to-ground channel is likely to be monopolized by LoS [27], [28], [29]. Therefore, we assume that the channel gain between the UAV m and verification nodes follows the free-space path loss model [30]. The channel gain $h _ { m , v } ( t )$ from the UAV m to the verification ( )node v at time slot t is given by

$$
h _ { m , v } ( t ) = g _ { 0 } d _ { m , v } ^ { - 2 } ( t ) = \frac { g _ { 0 } } { \|  { \boldsymbol { X } } _ { m } ( t ) -  { \boldsymbol { X } } _ { v } \| _ { 2 } ^ { 2 } + H ^ { 2 } } ,\tag{3}
$$

where parameter g0 represents the received power at a reference distance $( \mathrm { i . e . , ~ } d _ { 0 } = 1$ meter) between the UAV m and = 1verification node v. The orthogonal frequency-division multiple access (OFDMA) scheme is considered into the wireless channel [31], where the bandwidth is divided into V sub-channels, each occupied by one verification node. Let B represent the total channel bandwidth of the wireless link, and the data transmission rate from UAV m to verification node v at time slot t is

$$
R _ { m , v } ( t ) = \frac { B } { V } \log _ { 2 } \left( 1 + \frac { P _ { m , v } h _ { m , v } ( t ) } { N _ { 0 } } \right) ,\tag{4}
$$

where $P _ { m , v }$ is the transmission power from the UAV m to verification node v and $N _ { 0 }$ is the the channel noise power.

## B. Blockchain Model

Due to the limited resources of the UAV, the collected computing tasks are offloaded to the ground-based BSs to provide a higher computing service experience to the mobile user. However, the migration of computing tasks between heterogeneous entities (i.e., mobile users, UAVs, and BSs) can put the privacy and security of mobile users at risk due to the open wireless communication environment. Blockchain is therefore introduced to process the collected mobile user data in a decentralized manner to maintain its security and integrity. The adoption of the improved DPoS consensus mechanism in blockchain ensures efficient energy utilization, rapid transaction confirmation speed, decentralized balance, and incentivized community participation compared to the Proof of Work (PoW), Proof of Stake (PoS), and Practical Byzantine Fault Tolerance (PBFT). In the improved DPoS consensus mechanism, the UAV is considered as the primary node only to collect user task requests and some easy task processing for reducing battery consumption. Moreover, the reputation incentive mechanism is designed to incorporate into the DPoS consensus mechanism as a criterion for selecting BSs with high reputation to be verification nodes at the end of each round to ensure the trustworthiness of the edge resources. As the entire model of DPoS consensus is cumbersome, we focus on the main parts of generating latency to reach agreement, including initialization, propagation, verification, and confirmation.

TABLE I MAIN NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>The number of UAVs</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>The number of verification nodes</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>The set of UAVs</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>The set of verification nodes</td></tr><tr><td rowspan=1 colspan=1> $T$ </td><td rowspan=1 colspan=1>The duration of blockchain nodes in each round</td><td rowspan=1 colspan=1> $B$ </td><td rowspan=1 colspan=1>The total bandwidth of the UAV m</td></tr><tr><td rowspan=1 colspan=1> $X _ { m } \left( t \right)$ </td><td rowspan=1 colspan=1>The horizontal position of UAV m at time slot t</td><td rowspan=1 colspan=1> $X _ { v }$ </td><td rowspan=1 colspan=1>The position of verification node u</td></tr><tr><td rowspan=1 colspan=1> $\nu \left( t \right)$ </td><td rowspan=1 colspan=1>The average velocity of the UAV m at time slot t</td><td rowspan=1 colspan=1> $\overline { { H } }$ </td><td rowspan=1 colspan=1>The flight altitude of the UAV m</td></tr><tr><td rowspan=1 colspan=1> $\nu _ { m a x }$ </td><td rowspan=1 colspan=1>The maximum velocity of the UAV m</td><td rowspan=1 colspan=1> $N$ </td><td rowspan=1 colspan=1>The number of transactions in the block</td></tr><tr><td rowspan=1 colspan=1> $S _ { b }$ </td><td rowspan=1 colspan=1>The average size of the preliminary block</td><td rowspan=1 colspan=1> $q _ { v } \left( t \right)$ </td><td rowspan=1 colspan=1>The reputation of verification node v at time slot t</td></tr><tr><td rowspan=1 colspan=1> $p _ { Q }$ </td><td rowspan=1 colspan=1>The unit rewards for service satisfaction for verificationnodes</td><td rowspan=1 colspan=1> $r _ { m } \left( t \right)$ </td><td rowspan=1 colspan=1>The usersâservice demands for UAV m at time slot t</td></tr><tr><td rowspan=1 colspan=1> $f _ { m } ( t )$ </td><td rowspan=1 colspan=1>The computational capacity of UAV m at time slot t</td><td rowspan=1 colspan=1> $p _ { v } \left( t \right)$ </td><td rowspan=1 colspan=1>The unit pricing of the computational resources for theverification nodes at time slot t</td></tr><tr><td rowspan=1 colspan=1> $f _ { v } \left( t \right)$ </td><td rowspan=1 colspan=1>The computational capacity of the verification node uat time slot t</td><td rowspan=1 colspan=1> $R _ { m , v } \left( t \right)$ </td><td rowspan=1 colspan=1>The transmission rate from the UAV m to verificationnode v at time slot t</td></tr><tr><td rowspan=1 colspan=1> $P _ { m , v }$ </td><td rowspan=1 colspan=1>The transmission power from UAV m to verificationnode u</td><td rowspan=1 colspan=1> $c _ { s } , c _ { e } , c _ { h }$ </td><td rowspan=1 colspan=1>TheCPUcyclespertransactionforvalida-tion/execution/hashing</td></tr><tr><td rowspan=1 colspan=1> $p _ { h } , p _ { m }$ </td><td rowspan=1 colspan=1>The hovering / horizontal flight power of UAV m</td><td rowspan=1 colspan=1> $\overline { { T _ { m } ^ { t } ( t ) } }$ </td><td rowspan=1 colspan=1>The transmission delay of the preliminary block by theUAV m at time slot t</td></tr><tr><td rowspan=1 colspan=1>E(t)</td><td rowspan=1 colspan=1>The total propulsion energy consumption of the UAVm at time slot t</td><td rowspan=1 colspan=1>Tm(t),Tg(t)</td><td rowspan=1 colspan=1>The computational delay of the UAV m / verificationnode v at time slot t</td></tr><tr><td rowspan=1 colspan=1> $\overline { { E _ { m } ^ { t } \left( t \right) } }$ </td><td rowspan=1 colspan=1>The transmission energy consumption of UAV m of-floading the preliminary block at time slot t</td><td rowspan=1 colspan=1> $\overline { { E _ { m } ^ { c } \left( t \right) , E _ { v } ^ { c } \left( t \right) } }$ </td><td rowspan=1 colspan=1>The computational energy consumption of the UAV m/ verification node v at time slot t</td></tr></table>

1) Initialization Delay: Once the UAV m has collected data from the mobile user clusters in his service area into the transaction pool, the block initialization process is turned on. The N task requests in the transaction pool having low latency tolerance are first prioritized as transaction candidates for inclusion in the current block by UAV m. The UAV m then verifies the signature of transaction candidates in turn. If the signature is feasible, the transaction candidate will be packed into the preliminary block as a transaction. After all transactions have been identified, the UAV m will attach its signature to the preliminary block and multicast the preliminary block to the verification nodes for consensus on the block. Assuming that it takes $c _ { s }$ CPU cycles to verify a single signature, and the computational capacity of the UAV m is denoted by $f _ { m } ( t )$ , the delay consumed

in this phase is given as

$$
T _ { m } ^ { c _ { 1 } } ( t ) = \frac { N c _ { s } } { f _ { m } ( t ) } .\tag{5}
$$

2) Propagation Delay: The UAV m as the primary node needs to multicast the preliminary block to the verification nodes for verification via the OFDMA channel access scheme. Therefore, the delay in completing the block consensus includes the propagation delay of the UAV m to offload the handing over of the preliminary blocks to the verification nodes. For the propagation process, we denote the average size of the preliminary block as $S _ { b } ,$ , which is proportional to the unit data computing capability of CPU Î¶. The average transmission rate from UAV m to the verification nodes v at time slot t is denoted by $R _ { m , \nu } ( t ) = \operatorname* { m i n } _ { v \in \nu } R _ { m , v } ( t )$ , the propagation delay of the preliminary block between UAV m and the verification nodes at time slot t is

$$
T _ { m } ^ { t } ( t ) = \frac { S _ { b } } { R _ { m , \nu } ( t ) } .\tag{6}
$$

3) Processing Delay: Behind accepting the preliminary block sent by the UAV m, the verification nodes selected through the reputation mechanism will verify the preliminary block including the preliminary block signature and transaction signature. Compared with the transaction signature verification, the signature of the preliminary block can be completed quickly, and the time delay consumed by it can be ignored without explicitly being considered here. After the verification is feasible, the verification nodes will execute each transaction in turn and perform a hash operation on the execution results. Assume that the CPU cycles required to complete each transactionâs execution and the hash result calculation are $c _ { e }$ and $c _ { h }$ , respectively. The computational capability of verification node v is denoted by $f _ { v } ( t )$ to process preliminary block at time slot t, the computation delay of verification node v at time slot t can be calculated as

$$
T _ { v } ^ { c } ( t ) = \frac { N \left( c _ { s } + c _ { e } + c _ { h } \right) } { f _ { v } ( t ) } .\tag{7}
$$

4) Confirmation Delay: When the preliminary block processing is complete, the verification nodes transmit the information having execution and hash results to the UAV m. The information returned by each verification node is often minimal compared to the preliminary block sent by the UAV m. Therefore, the transmission delay of feedback information from verification nodes to the UAV m is negligible. After receiving the feedback information, the UAV m first verifies the signature attached to the feedback information. If the signature is feasible, the UAV m will then use the smart contract to compare the hash results from each verification node. According to the PBFT protocol [32], UAV m will combine the execution results and hash results into the preliminary block to the final block when more than $2 / 3$ of the same hash results exists. Then, the 2 3UAV m sends the correct execution result and the final block to the corresponding mobile user and the verification nodes, respectively. Each verification node adds it to the blockchain for storage after receiving the final block sent from the UAV m. The computational delay by the UAV m during this phase is

$$
T _ { m } ^ { c _ { 2 } } ( t ) = \frac { V c _ { s } } { f _ { m } ( t ) } .\tag{8}
$$

Therefore, the total latency incurred in the entire process of generating block by the improved DPoS consensus scheme is $\bar { T } _ { t o t a l } ( t ) \bar { = } T _ { m } ^ { c } ( t ) + T _ { m } ^ { t } ( t ) \bar { + } T _ { v } ^ { c } ( t )$ with $T _ { m } ^ { c } ( t ) = T _ { m } ^ { c _ { 1 } } ( t ) +$ T c2m t .

( )5) Security Analysis: The improved DPoS consensus mechanism in blockchain adaptively assesses the reputation of verification nodes to allow for removing or downgrading nodes that exhibit misbehavior or performance degradation. By doing so, the incentives for malicious attacks and misbehavior are reduced, contributing to the overall security and integrity of the blockchain network. Moreover, the economic incentive is integrated into the consensus mechanism to drive blockchain nodes to execute tasks honestly to enhance reputation and increase revenue, fostering a more trustworthy ecosystem. By distributing transaction records across multiple nodes and encrypting them cryptographically, blockchain systems prevent unauthorized access, tampering, or fraud, which enhances the confidentiality and integrity of transactions, bolstering user trust in the platform. Additionally, every transaction is recorded on the public ledger accessible to anyone. The transparency enables participants to verify the legitimacy of transactions and provides a means for auditing and accountability within the network.

## C. Energy Consumption Model

In order to provide sustainability for blockchain integration of UAV-enabled MEC network services, it is essential to handle energy consumption appropriately. In this paper, we focus on propulsion, transmission, and computation energy consumption. Moreover, we ignore the transmission energy consumption of the downlink due to the small size of the feedback information from the verification nodes.

1) Propulsion Energy Consumption: Assuming that the UAV m supports the flight-hover mode and the average speed remains constant during flight. After the UAV m has moved to the hover position $X _ { m } ( t )$ at the time slot t, it hovers to transmit the pre-( )liminary block. Therefore, the propulsion energy consumption for the UAV m at time slot t contains both flight energy and hover energy. The hovering energy consumption for the UAV m at time slot t is given by

$$
E _ { m } ^ { p _ { 1 } } ( t ) = P _ { h } T _ { m } ^ { t } ( t ) = \frac { P _ { h } S _ { b } } { R _ { m , \nu } ( t ) } ,\tag{9}
$$

where $P _ { h }$ is the hovering power of the UAV m. To simplify the analysis, we assume that the hover delay equals the transmission delay of the preliminary block between the UAV m and the verification nodes. Furthermore, the delay in initializing the block by the UAV m is considered to be positively proportional to the flight delay of the UAV m with scale factor Î² t , i.e., $T _ { m } ^ { c _ { 1 } } ( t ) = \bar { \beta } ( t ) T _ { m } ^ { f } ( t )$ ( ). The energy consumption for the UAV m ( ) = ( ) ( )during flight at time slot t is given by

$$
E _ { m } ^ { p _ { 2 } } ( t ) = \left( P _ { h } + P _ { m } \right) T _ { m } ^ { f } ( t ) = \frac { \left( P _ { h } + P _ { m } \right) N c _ { s } } { \beta ( t ) f _ { m } ( t ) } .\tag{10}
$$

where $\begin{array} { r } { P _ { m } = \frac { P _ { \mathrm { m a x } } - P _ { \mathrm { i d l e } } } { \nu _ { \mathrm { m a x } } } \nu ( t ) + P _ { \mathrm { i d l e } } } \end{array}$ is the horizontal flight power = ( ) +which is modeled as a linear function of average flight speed Î½ t [33], [34], [35]. $P _ { \mathrm { m a x } }$ and $P _ { \mathrm { i d l e } }$ are the hardware power ( )levels when the UAV m is in full motion and idle, respectively. Thus, the total propulsion energy consumption for the UAV m at time slot t is $E _ { m } ^ { p } ( t ) = E _ { m } ^ { p _ { 1 } } ( t ) + E _ { m } ^ { p _ { 2 } } ( t )$

( ) = ( ) + ( )2) Transmission Energy Consumption: The transmission energy consumption of the UAV m to offload the preliminary block to the verification node v via the LoS uplink at time slot t is $\begin{array} { r } { E _ { m , v } ^ { t } ( t ) = \frac { S _ { b } P _ { m , v } } { R _ { m , v } ( t ) } } \end{array}$ [36]. The total transmission energy consumption of the UAV m at time slot t is given by

$$
E _ { m } ^ { t } ( t ) = \sum _ { v \in \mathcal { V } } E _ { m , v } ^ { t } ( t ) = \sum _ { v \in \mathcal { V } } \frac { S _ { b } P _ { m , v } } { R _ { m , v } ( t ) } .\tag{11}
$$

3) Computation Energy Consumption: It is assumed that the UAV m supports the Dynamic Voltage and Frequency Scaling (DVFS) technique [37], where the computational capability can be dynamically adjusted to save computing energy consumption when processing tasks. Similar to [38], the CPU power consumption of UAV m at time slot t can be calculated by modeling as $E _ { m } ^ { c } ( t ) = \kappa _ { m } f _ { m } ^ { 3 } T _ { m } ^ { c } ( t )$ , where $\kappa _ { m }$ is the effective ( ) = ( )capacitance coefficient of the UAV m. The computational energy consumption of the UAV m to generate the final block at the time slot t is given by

$$
E _ { m } ^ { c } ( t ) = \kappa _ { m } \left( N + V \right) c _ { s } f _ { m } ^ { 2 } ( t ) .\tag{12}
$$

In the same way as the UAV m, the verification node v also supports DVFS technology. Therefore, the computational energy consumption generated by verification node v for processing block at time slot t is given by

$$
E _ { v } ^ { c } ( t ) = \kappa _ { v } N \left( c _ { s } + c _ { e } + c _ { h } \right) f _ { v } ^ { 2 } ( t ) ,\tag{13}
$$

where $\kappa _ { v }$ is the effective capacitance coefficient on the verification node v.

## IV. INCENTIVE DESIGN AND PROBLEM FORMULATION

We model the interaction between the UAV m and a set of verification nodes $\mathcal { V } = \{ 1 , \ldots , v , \ldots , V \}$ as the Stackelberg = 1differential game, which is a strategic game developed to sequential decision-marking problems [39], [40]. In the proposed Stackelberg differential game, UAV m assumes the role of the leader while the verification nodes serve as the followers. As the leader, the UAV m first publishes its strategy $p _ { m } ( t )$ , i.e., the ( )unit pricing of the edge computing resource that maximizes the utility under the constraints of the dynamic state of user demand at time slot t. Then, the verification node v as a follower decides its strategy $f _ { v } ( t )$ , i.e., its computational capacity based on the ( )strategy adopted by the UAV m to maximize the utility under the constraint of the dynamic state of verification nodesâ reputation at time slot t.

## A. System State

The Stackelberg differential game is formulated to address dynamic resource trading in blockchain integration of UAVenabled MEC networks. In order to ensure the QoS from the blockchain nodes to the users, the usersâ service demand for the UAV m at time slot t is considered as the state variable in the first stage, which is denoted as $r _ { m } ( t )$ . In addition, reputa-( )tions are introduced as the dynamic variables in the second stage to measure the reliability of each verification node in processing the preliminary block consensus from the UAV m, where a set of verification nodesâ reputation at time slot t is defined by $Q ( t ) = \{ q _ { 1 } ( t ) , q _ { 2 } ( t ) , . . . , q _ { v } ( t ) \}$

( ) = ( ) ( ) ( )During the computational offloading process, the usersâ service demand trend is determined by various factors, including the reliability of the task execution, the supply and demand of the tasks, and the userâs service unit price. The reliability of task execution is quantified by utilizing the service rate of the UAV m to meet the userâs low latency demand. The reliability of task execution is a crucial factor in ensuring users meet low-latency requirements, quantified by leveraging the service rate of UAV m. Additionally, to ensure effective supervision of user behavior, the service price is formulated as a linear function of user service demands. The interaction between users and UAV m involves the supply and demand relationship of tasks, which is modeled using dynamically changing difference equations to avoid excessive accumulation of computational tasks. Therefore, the evolution of the usersâ service demand to the UAV m at time slot t is expressed as

$$
\begin{array} { l } { d r _ { m } ( t ) } \\ { \quad = \left\{ \epsilon _ { 1 } \left( R _ { m , \mathcal { V } } ( t ) + \gamma \underset { v \in \mathcal { V } } { \operatorname* { m i n } } f _ { v } ( t ) \right) + \epsilon _ { 2 } p _ { i } ( t ) + \epsilon _ { 3 } u ( t ) \right\} d t } \end{array}\tag{14}
$$

where $\epsilon _ { 1 } , \epsilon _ { 2 }$ , and $\epsilon _ { 3 }$ are the constant adjustment coefficients with $\epsilon _ { 1 } , \epsilon _ { 2 } \geq 0$ and $\epsilon _ { 3 } \leq 0$ . The first component $( R _ { m , \nu } ( t ) +$ $\begin{array} { r } { \operatorname* { m i n } _ { v \in \mathcal { V } } \gamma f _ { v } ( t ) ) } \end{array}$ refers the userâs service experience for the UAV m where Î³ is the proportion of the processing delay of the verification nodes when the users evaluate the UAV m The second component $p _ { i } ( t ) = \alpha p _ { m } ( t ) - p _ { s } ( t )$ means invalid service unit pricing for the UAV m where $p _ { s } ( t ) = ( 1 + \eta ) r _ { m } ( t )$ is pricing per unit of service and Î± is adjustment coefficient. Moreover, the third component $u ( t ) = ( r _ { m } ( t ) - N )$ indicates supply-demand ( ) = ( ( ) )of service demand increases when the difference between the number of tasks offloaded by the users and the number of transactions in the preliminary block is positively approximated to 0.

For the verification node v, we use reputation variable $q _ { v } ( t )$ ( )to measure its edge resourcesâ reliability. In this paper, we set the reputation threshold value $q _ { \tau }$ to penalize verification nodes for malicious behavior. Moreover, the reputation of verification node v should also be related to past reliability, processing block delay, and resource gain. These considerations highlight the intricate interplay of factors in managing the reputation of verification nodes during the computational offloading process. In addition, considering the balance between past reputation, computing capability, and resource pricing is crucial for developing the reputation incentive model to maintain system stability. Thus, the evolution of reputation for verification node v at time slot t is expressed as

$$
\begin{array} { l } { d q _ { v } ( t ) } \\ { \ = \{ \omega _ { 1 } \left( q _ { v } ( t ) - q _ { \tau } \right) + \omega _ { 2 } q _ { v } ( t ) + \omega _ { 3 } f _ { v } ( t ) + \omega _ { 4 } p _ { m } ( t ) \} d t , } \end{array}\tag{15}
$$

where $\omega _ { 1 } , \omega _ { 2 } , \omega _ { 3 }$ and $\omega _ { 4 } \geq 0$ are the constant adjustment coef-0ficients. The first component $q _ { v } ( t ) - q _ { \tau }$ denotes the reputation ( )level of verification node v at time slot t compared to reputation threshold $q _ { \tau }$ . The second component $q _ { v } ( t )$ is to de-measure ( )the role of past reputation on reputation evolution. The third component $f _ { v } ( t )$ is to incentivize the verification node v to ( )process the preliminary block quickly to improve the service experience of the UAV m. Furthermore, the fourth component $p _ { m } ( t )$ is to motivate the verification node v to improve the ( )resource reliability more to get higher resource pricing from the UAV m.

## B. Utility Function

For the UAV m, it packages the usersâ task requests into preliminary blocks for offloading to the verification nodes to generate the final block, which is added to the blockchain already stored in the verification nodes to prevent data tampering. Due to the limited budget of the UAV $m ,$ we consider that the objective of the UAV m is to maximize the utility included cost of generating block. For the UAV m, the utility consists of four components at time slot t, which is expressed as

$$
u _ { m } ( t ) = R _ { m } ( t ) - C _ { m } ^ { t } ( t ) - C _ { m } ^ { e } ( t ) - C _ { m } ^ { r } ( t ) .\tag{16}
$$

Due to the interruption of direct communication with the terrestrial BSs, the users changed to offload the task requests to the UAV m. For the offloaded tasks to be completed successfully at the UAV $m ,$ the users give the unit service pricing $p _ { s } ( t )$ to the ( )UAV m. Thus, the revenue obtained by the UAV m under usersâ service demand at time slot t is written as

$$
R _ { m } ( t ) = r _ { m } ( t ) p _ { s } ( t ) = ( 1 + \eta ) r _ { m } ^ { 2 } ( t ) .\tag{17}
$$

In order to induce the blockchain nodes to be able to generate block with low latency, we consider the delay cost that occurs throughout the block processing as one of the components of the utility function for the UAV m. Let $l _ { m } ^ { t }$ denote the unit delay cost, the total delay cost due to block generation for the UAV m at time slot t is written as

$$
C _ { m } ^ { t } ( t ) = \left[ \frac { \left( N + V \right) c _ { s } } { f _ { m } ( t ) } + \frac { S _ { b } } { R _ { m , v } ( t ) } + \frac { N \left( c _ { s } + c _ { e } + c _ { h } \right) } { f _ { v } ( t ) } \right] l _ { m } ^ { t } .\tag{18}
$$

Since the UAV m has very limited real-time resources, we include energy consumption as one of the costs of the UAV m. During the whole offloading process from the flight to consensus, the energy cost for the UAV m involves computation energy cost, propulsion energy cost, and transmission energy cost, respectively. Assuming that the unit energy consumption cost is denoted by $l _ { m } ^ { e }$ , the total energy consumption cost for the UAV m at time slot t is written as

$$
\begin{array} { r l } { \displaystyle C _ { m } ^ { e } ( t ) = } & { \biggl [ \frac { \left( \left( P _ { h } + P _ { \mathrm { i d e } } \right) \nu _ { \mathrm { m a x } } + \left( P _ { \mathrm { m a x } } - P _ { \mathrm { i d e } } \right) \nu \right) N c _ { s } } { f _ { m } \nu _ { \mathrm { m a x } } } } \\ { \displaystyle + \frac { P _ { h } S _ { b } } { R _ { m , \nu } ( t ) } + \sum _ { v \in \mathcal { V } } \frac { S _ { b } P _ { m , v } ( t ) } { R _ { m , v } ( t ) } + \kappa _ { m } \left( N + V \right) } \\ { \displaystyle \qquad \times c _ { s } f _ { m } ^ { 2 } ( t ) \biggl ] l _ { m } ^ { e } . } \end{array}\tag{19}
$$

Considering the networkâs decentralized nature, the verification nodes cannot honestly organize themselves to participate in the consensus. Therefore, the UAV m provides additional rewards $P _ { Q }$ in QoS $\mathrm { i . e . , } q _ { v } ( t ) f _ { v } ( t )$ to the verification nodes putting aside the unit pricing $p _ { m } ( t )$ )of the given computational ( )resources to obtain reliable edge computational resources. The total cost of the UAV m to pay the verification nodes for the consensus at the time slot t is written as

$$
C _ { m } ^ { r } ( t ) = \sum _ { v \in \mathcal { V } } f _ { v } ( t ) p _ { m } ( t ) + \sum _ { v \in \mathcal { V } } q _ { v } ( t ) f _ { v } ( t ) p _ { Q } .\tag{20}
$$

The total utility for the UAV m at time slot t is defined in (21) shown at the bottom of the this page. The objective of the UAV m is to maximize the total utility expended on transaction offloading by determining the resource pricing per unit $p _ { m } ( t )$ ( )Therefore, the utility function for the UAV m at the time period , T is expressed as

$$
U _ { m } ( t ) = \operatorname* { m a x } _ { p _ { m } ( t ) } \int _ { 0 } ^ { T } u _ { m } ( t ) d t .\tag{22}
$$

For the verification node v, the purpose of participating in consensus with the blockchain integration of UAV-enabled MEC network is to maximize the utility. This utility refers to the profit, i.e., the verification payment received by the UAV m minus the energy consumption generated through performing the consensus task. Therefore, the utility function of the verification node v at time slot t is expressed as

$$
\begin{array} { r } { u _ { v } ( t ) = R _ { v } ( t ) - C _ { v } ( t ) . } \end{array}\tag{23}
$$

To incentivize the verification nodes to participate in the consensus computation actively, the verification revenue Rv t ( )at time slot t depends not only on the income from computational resources at that time but also correlates with the rewards obtained for delivering QoS during the same time slot, which is written as

$$
R _ { v } ( t ) = f _ { v } ( t ) p _ { m } ( t ) + q _ { v } ( t ) f _ { v } ( t ) p _ { Q } .\tag{24}
$$

In addition, the energy consumption cost spent by the verification node v is denoted by $C _ { v } ( t )$ , indicating the computational ( )cost incurred during the execution of the consensus task in time slot t. Let $l _ { v } ^ { c }$ define the computation energy consumption cost per unit. The energy consumption cost of the verification node v during time slot t is written as

$$
\begin{array} { r } { C _ { v } ( t ) = \kappa _ { v } N \left( c _ { s } + c _ { e } + c _ { h } \right) f _ { v } ^ { 2 } ( t ) l _ { v } ^ { c } . } \end{array}\tag{25}
$$

Hence, the utility for verification node v during time slot t represented as the difference between the verification revenue and the energy consumption cost can be expressed as

$$
\begin{array} { r l } & { u _ { v } ( t ) = f _ { v } ( t ) p _ { m } ( t ) + q _ { v } ( t ) f _ { v } ( t ) p _ { Q } - \kappa _ { v } N \left( c _ { s } + c _ { e } \right. } \\ & { \qquad \left. + c _ { h } \right) f _ { v } ^ { 2 } ( t ) l _ { v } ^ { c } . } \end{array}\tag{26}
$$

The objective of the verification node v is to maximize its utility by controlling the computational resources $f _ { v } ( t )$ . Thus, ( )the utility function of the verification node v during the time , T is expressed as

$$
U _ { v } ( t ) = \operatorname* { m a x } _ { f _ { v } ( t ) } \int _ { 0 } ^ { T } u _ { v } ( t ) d t .\tag{27}
$$

## C. Problem Formulation

We formulated the two-stage Stackelberg differential game to study the dynamic evolution of the interactions between the UAV m and the verification nodes over time.

- Players: The UAV m and the set of all verification nodes $\mathcal { V } = \{ 1 , \ldots , v , \ldots , V \}$ are the players of the game, where = 1v denotes one of the verification nodes. In the two-stage game, the UAV m acts as the leader and the verification nodes are the followers.

- State: For the UAV m, the usersâ service demands $r _ { m } ( t )$ is ( )to be the state variable. In addition, due to the mobility of the UAV m, the other state value $X _ { m } ( t )$ exists for ( )this stage. For the verification nodes, the set of reputation

$$
\begin{array} { c c l } { \displaystyle { u _ { m } ( t ) = ( 1 + \eta ) r _ { m } ^ { 2 } ( t ) - [ \frac { ( N + V ) c _ { s } } { f _ { m } ( t ) } + \frac { S _ { b } } { R _ { m , \nu } ( t ) } + \frac { N ( c _ { s } + c _ { e } + c _ { h } ) } { f _ { \nu } ( t ) } ] l _ { m } ^ { t } - [ \frac { ( ( P _ { h } + P _ { \mathrm { d i g } } ) \nu _ { \mathrm { m a x } } + ( P _ { \mathrm { m a x } } - P _ { \mathrm { d i g } } ) \nu ) N c _ { s } } { \beta ( t ) f _ { m } ( t ) \nu _ { \mathrm { m a x } } } } } \\ { \displaystyle { + \frac { P _ { h } S _ { b } } { R _ { m , \nu } ( t ) } + \sum _ { v \in \mathbb { V } } \frac { S _ { b } P _ { m , v } } { R _ { m , v } ( t ) } + \kappa _ { m } ( N + V ) c _ { s } J _ { m } ^ { 2 } ( t ) ] l _ { m } ^ { c } - \sum _ { v \in \mathbb { V } } f _ { v } ( t ) p _ { m } ( t ) - \sum _ { v \in \mathbb { V } } f _ { v } ( t ) q _ { v } ( t ) p _ { Q } } } & { \displaystyle { ( 2 1 - \eta ) [ ( \frac { S _ { v } + S _ { v } } { \beta ( t ) } + \frac { S _ { v } } { \beta ( t ) } ) ] l _ { m } ^ { c } } . } \end{array}
$$

$\mathcal { Q } ( t ) = \{ q _ { 1 } ( t ) , q _ { 2 } ( t ) , . . . , q _ { v } ( t ) \}$ are considered as their ( ) = ( )state variables.

Policy: The strategy of UAV m at time slot t is the resource pricing per unit $p _ { m } ( t )$ when offloading the ini-( )tial block to the verification nodes. For each verification node, the computation capability $f _ { v } ( t )$ corresponding to the reputation $q _ { v } ( t )$ ( )obtained by performing consensus at ( )time slot t is taken as its policy. Therefore, the set of policies for the verification nodes is denoted as $\mathcal { F } ( t ) =$ $\{ f _ { 1 } ( t ) , f _ { 2 } ( t ) , . . . , f _ { v } ( t ) \}$

( ) ( ) ( )Utility: Each of the players aims to maximize utilities by deciding the optimal strategies based on their identities which are denoted in (22) and (27), respectively.

Objective function: For the UAV m, its goal is maximizing the utility based on the state of usersâ service demands during the block generation process. The optimization problem $P _ { 1 }$ of the UAV m can be written as

$$
\begin{array} { l } { P _ { 1 } : \displaystyle \operatorname* { m a x } _ { p _ { m } ( t ) } \int _ { 0 } ^ { T } u _ { m } ( t ) d t \qquad \mathrm { ( } } \\ { \mathrm { s . t . } \left\{ \begin{array} { l l } { \displaystyle d r _ { m } ( t ) = \left\{ \epsilon _ { 1 } \left( R _ { m , \nu } ( t ) + \gamma \operatorname* { m i n } _ { v \in \mathcal { V } } f _ { v } ( t ) \right) + \epsilon _ { 2 } \left( R _ { m , \nu } ( t ) + \gamma \operatorname* { m i n } _ { v \in \mathcal { V } } f _ { v } ( t ) \right) + \epsilon _ { 3 } \left( R _ { m , \nu } ( t ) + \gamma \operatorname* { m i n } _ { v \in \mathcal { V } } f _ { v } ( t ) \right) + \epsilon _ { 4 } \left( R _ { m , \nu } ( t ) + \gamma \operatorname* { m i n } _ { v \in \mathcal { V } } f _ { v } ( t ) \right) \right\} } \\ { \displaystyle \quad \times p _ { i } ( t ) + \epsilon _ { 3 } u ( t ) \} d t } \\ { \displaystyle 0 \le p _ { m } ( t ) . } \end{array} \right. } \end{array}\tag{28}
$$

(29)

Furthermore, for the verification node v, its goal is maximizing the utility based on the state of the verification nodesâ reputation in participating in the consensus. The optimization problem $P _ { 2 }$ of the verification node v can be written as

$$
P _ { 2 } : \operatorname* { m a x } _ { f _ { v } ( t ) } \int _ { 0 } ^ { T } u _ { v } ( t ) d t\tag{30}
$$

$$
\mathrm { s . t . } \left\{ \begin{array} { l l } { d q _ { v } ( t ) = \left\{ \omega _ { 1 } \left( q _ { v } ( t ) - q _ { \tau } \right) + \omega _ { 2 } q _ { v } ( t ) + \omega _ { 3 } f _ { v } ( t ) \right. } \\ { \quad \left. + \omega _ { 4 } p _ { m } ( t ) \right\} d t } \\ { 0 \leq f _ { v } ( t ) \leq f _ { \operatorname* { m a x } } . } \end{array} \right.\tag{31}
$$

## V. GAME ANALYSIS

In this section, we will analyze the Stackelberg differential game problem formulated in the above section by backward induction [41]. Assume that all the players in the Stackelberg differential game possess precise knowledge of the initial state. Also, their strategies are functions of the initial state and time slot t. The optimal solution in this pattern is called the openloop solution. In the proposed Stackelberg differential game, each verification node first allocates computational resources to maximize its utility based on the resource pricing per unit policy notified by the UAV m. Then, the UAV m determines the resource pricing per unit to the solution to the computational resource allocation policy that maximizes its utility. Next, we will analyze the decision-making problem for the verification nodes (followers) and the UAV m (leader) in turn.

## A. Open-Loop Solutions of Verification Nodes

We first consider the open-loop solution for the verification nodes, in which each verification node needs to determine the allocation of computational resources based on the resource pricing per unit provided by the UAV m to maximize their utility function. To obtain the collection of conditions that must be satisfied for the open-loop equilibrium solution, we initially get the optimal strategies for the followers through the resolution of the problem in $P _ { 2 }$

Definition 1: For the verification node $v ,$ the computing capacity $f _ { v } ^ { * } ( t )$ is optimal when the following inequality keeps for ( )all possible decision strategies $f _ { v } ( t ) \neq f _ { v } ^ { * } ( t )$ ï¼

$$
U _ { v } \left( f _ { v } ^ { * } ( t ) , q _ { v } ( t ) , t \right) \geq U _ { v } \left( f _ { v } ( t ) , q _ { v } ( t ) , t \right) .\tag{32}
$$

Definition 2: A set of strategies $\{ f _ { v } ^ { * } ( t ) \}$ comprises the openloop equilibrium of problem $P _ { 2 }$ , and $\mathbf { q } ^ { * } ( t )$ is the correspond-( )ing the reputation state matrix. If there exists a set of costate functions $\mathbf { \boldsymbol { \Lambda } } _ { v } ( t ) = \left[ \lambda _ { v 1 } ( t ) \cdot \cdot \cdot \lambda _ { v j } ( t ) \cdot \cdot \cdot \lambda _ { v V } ( t ) \right]$ , the following ( ) = [ ( )relationship should be satisfied

$$
f _ { v } ^ { * } ( t ) = \underset { f _ { v } ( t ) } { \arg \operatorname* { m a x } } \left\{ u _ { v } ( t ) + \Lambda _ { v } ( t ) \dot { \mathbf { q } } ^ { * } ( t ) \right\} ,\tag{33}
$$

$$
\dot { \bf { A } } _ { v } ( t ) = \rho { \bf { A } } _ { v } ( t ) - \frac { \partial \left[ u _ { v } ( t ) + { \bf { A } } _ { v } ( t ) \dot { \bf { q } } ^ { * } ( t ) \right] } { \partial { \bf { q } } ^ { * } ( t ) } .\tag{34}
$$

According to the definitions above, we can get the open-loop equilibrium for the problem $P _ { 2 }$ . Next, we prove the existence and uniqueness of the open-loop equilibrium on the verification node v.

Theorem 1: The optimal computational resource allocation solution for the verification node v is

$$
f _ { v } ^ { * } ( t ) = \frac { q _ { v } p _ { Q } + p _ { m } ( t ) + \omega _ { 3 } \mathbf { { \Lambda } } _ { v } ( t ) } { 2 \kappa _ { v } N \left( c _ { s } + c _ { e } + c _ { h } \right) l _ { v } ^ { c } } ,\tag{35}
$$

which is also an open-loop equilibrium for the verification node v.

Proof: We first model the Hamiltonian system for the followers, where the Hamiltonian function for the verification node v based on Pontryaginâs maximum principle [42], [43] is given by

$$
H _ { v } \left( t , f _ { v } ( t ) , \mathbf { q } ( t ) , \Lambda _ { v } ( t ) \right) = u _ { v } ( t ) + \Lambda _ { v } ( t ) \dot { \mathbf { q } } ( t ) .\tag{36}
$$

Based on Definition 2, note that the optimal decision strategy for the problem $P _ { 2 }$ should also maximize the corresponding Hamiltonian function. Therefore, to obtain an open-loop solution for the verification node $v ,$ , the partial derivatives of its Hamiltonian function must satisfy the following conditions

$$
0 = \frac { \partial H \left( t , f _ { v } ( t ) , \mathbf { q } ( t ) , \mathbf { \boldsymbol { \Lambda } } _ { v } ( t ) \right) } { \partial f _ { v } ( t ) } ,\tag{37}
$$

$$
\dot { \lambda } _ { v j } ( t ) = \rho \lambda _ { v j } ( t ) - \frac { \partial H ^ { * } \left( t , f _ { v } ( t ) , \mathbf { q } ( t ) , \Lambda _ { v } ( t ) \right) } { \partial q _ { j } ( t ) } .\tag{38}
$$

Solving (37), we can derive the open-loop equilibrium solution of the verification node v to determine the optimal allocation of computational resources, which is written as

$$
f _ { v } ^ { * } ( t ) = \frac { q _ { v } p _ { Q } + p _ { m } ( t ) + \omega _ { 3 } \mathbf { { A } } _ { v } ( t ) } { 2 \kappa _ { v } N \left( c _ { s } + c _ { e } + c _ { h } \right) l _ { v } ^ { c } } .\tag{39}
$$

In addition, the Hamiltonian parameter $\dot { \lambda } _ { v j } ( t )$ for the verification node v can be calculated based on (34) and (38), which is expressed as

$$
\begin{array} { r } { \dot { \lambda } _ { v j } ( t ) = \lambda _ { v j } ( t ) \left( \rho - \omega _ { 1 } - \omega _ { 2 } \right) , v \ne j , } \end{array}\tag{40a}
$$

$$
\begin{array} { r } { \dot { \lambda } _ { v j } ( t ) = \lambda _ { v j } ( t ) \left( \rho - \omega _ { 1 } - \omega _ { 2 } \right) - f _ { v } ( t ) p _ { Q } , v = j . } \end{array}\tag{40b}
$$

Note that the open-loop equilibrium solution exists for the verification node v when $p _ { m } ( t )$ and $\lambda _ { v j } ( t )$ are determined. To this end, the proof of Theorem 1 is completed.

## B. Open-Loop Solutions of UAV

In the above analysis, a unique optimal computational resource allocation solution exists for the verification node v to maximize their utility function for the given resource pricing per unit $p _ { m } ( t )$ . In this section, we will analyze the optimal strategy ( )and state for the UAV m. Compared to the verification nodes, the UAV m is acting as the leader in the proposed game and thus is more complex to analyze for its optimal solution. The optimal strategy of the UAV m is constrained by its state function $\dot { r } _ { m } ( t )$ in addition to the dynamics of the costate function $\mathbf { \boldsymbol { \Lambda } } ( t )$ Ë ( )for all followers.

Definition 3: For the UAV $m ,$ the resource pricing per unit $p _ { m } ^ { * } ( t )$ is optimal when the following inequality keeps for all ( )possible decision strategies $p _ { m } ( t ) \neq p _ { m } ^ { * } ( t )$ ï¼

$$
\begin{array} { r } { U _ { m } \left( p _ { m } ^ { * } ( t ) , r _ { m } ( t ) , t \right) \leq U _ { m } \left( p _ { m } ( t ) , r _ { m } ( t ) , t \right) . } \end{array}\tag{41}
$$

Definition 4: The strategy $p _ { m } ^ { * } ( t )$ comprises the open-loop equilibrium of the problem $P _ { 1 } ,$ ( ) and $r _ { m } ^ { * } ( t )$ is the correspond-( )ing demand state variable. if there exists the costate functions $\varphi _ { m } ( t )$ and $\pmb { \Psi } ( t ) = [ \pmb { \Psi } _ { 1 } ( t ) \ \pmb { \Psi } _ { 2 } ( t ) \cdot \cdot \cdot \ \pmb { \Psi } _ { V } ( t ) ] ^ { T }$ , the following ( ) ( ) = [ ( )relationship should be satisfied

$$
\begin{array} { r l } & { p _ { m } ^ { * } ( t ) = \underset { p _ { m } ( t ) } { \arg \operatorname* { m a x } } } \\ & { ~ \left\{ H _ { m } \left( t , p _ { m } ( t ) , r _ { m } ( t ) , \varphi _ { m } ( t ) , \Lambda ( t ) , \Psi ( t ) \right) \right\} , } \end{array}\tag{42}
$$

$$
\begin{array} { l } { { \displaystyle { \dot { \varphi } } _ { m } ( t ) = \rho \varphi _ { m } ( t ) } \ ~ } \\ { { \displaystyle ~ - \frac { \partial \left[ H _ { m } \left( t , p _ { m } ( t ) , r _ { m } ( t ) , \varphi _ { m } ( t ) , \Lambda ( t ) , \Psi ( t ) \right) \right] } { \partial p _ { m } ^ { * } ( t ) } } , } \end{array}\tag{43}
$$

$$
\begin{array} { l } { \dot { \Psi } _ { v } ( t ) = \rho \Psi _ { v } ( t ) } \\ { \qquad - \underbrace { \partial \left[ H _ { m } \left( t , p _ { m } ( t ) , r _ { m } ( t ) , \varphi _ { m } ( t ) , \Lambda ( t ) , \Psi ( t ) \right) \right] } _ { \partial \Lambda _ { v } ( t ) } . } \end{array}\tag{44}
$$

Theorem 2: The optimal resource pricing per unit solutions for the UAV m is

$$
p _ { m } ^ { * } ( t ) = \operatorname* { m a x } \left\{ \frac { \epsilon _ { 2 } \alpha K _ { v } \varphi _ { m } ( t ) - p _ { Q } \mathbf { q } ( t ) - \omega _ { 3 } \mathbf { A } ( t ) } { V } , 0 \right\} ,\tag{45}
$$

which is also an open-loop equilibrium for the UAV m with $K _ { v } = 2 \kappa _ { v } N ( c _ { s } + c _ { e } + c _ { h } ) l _ { v } ^ { c }$

= 2 ( + + )Proof: Unlike the followersâ Hamiltonian system, the demand state variable and all followersâ costate functions are

essential to the leaderâs Hamiltonian function. Thus, the Hamiltonian function for the UAV m is given by

$$
H _ { m } \left( t , p _ { m } ( t ) , r _ { m } ( t ) , \varphi _ { m } ( t ) , \Lambda ( t ) , \Psi ( t ) \right)
$$

$$
= u _ { m } ( t ) + \varphi _ { m } ( t ) \dot { r } _ { m } ( t ) + \sum _ { v = 1 } ^ { V } \dot { \Psi } _ { v } ( t ) \dot { \bf \Lambda } _ { v } ( t )
$$

$$
= u _ { m } ( t ) + \varphi _ { m } ( t ) \dot { r } _ { m } ( t ) + \sum _ { v = 1 } ^ { V } \sum _ { j = 1 } ^ { V } \mu _ { v j } ( t ) \dot { \lambda } _ { v j } ( t ) ,\tag{46}
$$

where $\Psi _ { v } ( t ) = [ \mu _ { v 1 } ( t ) \cdot \cdot \cdot \mu _ { v j } ( t ) \cdot \cdot \cdot \mu _ { v V } ( t ) ] ^ { T }$ is the submatrix ( ) = [ ( )of the costate function $\Psi ( t ) \dot { = } [ \Psi _ { 1 } ( t ) \Psi _ { 2 } ( t ) \cdot \cdot \cdot \Psi _ { V } ( t ) ] ^ { T }$ for ( ) = [ ( ) ( ) ( )]the UAV m. Similarly, the partial derivatives of the Hamiltonian function for the UAV m must satisfy the following condition

$$
0 = \frac { \partial \left[ H _ { m } \left( t , p _ { m } ( t ) , r _ { m } ( t ) , \varphi _ { m } ( t ) , \Lambda ( t ) , \Psi ( t ) \right) \right] } { \partial p _ { m } ( t ) } .\tag{47}
$$

Substituting the optimal computational resource allocation policy $f _ { v } ^ { * } ( t ) , \forall v \in \mathcal { V }$ for the UAV m into (47) with $p _ { m } ( t ) \geq 0$ we have

$$
p _ { m } ^ { * } ( t ) = \operatorname* { m a x } \left\{ \frac { \epsilon _ { 2 } \alpha K _ { v } \varphi _ { m } ( t ) - p _ { Q } \mathbf { q } ( t ) - \omega _ { 3 } \mathbf { A } ( t ) } { V } , 0 \right\} .\tag{48}
$$

Therefore, the optimal resource pricing per unit strategy for the UAV m defined by Theorem 2 can be obtained.

In addition, the Hamiltonian parameters $\varphi _ { m } ( t )$ and $\mu _ { v j } ( t )$ (based on (43), (44), and (46) can be calculated as

$$
\begin{array} { r } { \dot { \varphi } _ { m } ( t ) = \left[ \rho + \epsilon _ { 2 } \left( 1 + \eta \right) + \epsilon _ { 3 } \right] \varphi _ { m } ( t ) - 2 \left( 1 + \eta \right) r _ { m } ( t ) , } \end{array}\tag{)(49}
$$

$$
\dot { \mu } _ { v , j } ( t ) = \smash { \left( \omega _ { 1 } + \omega _ { 2 } \right) \mu _ { v , j } ( t ) } .\tag{50}
$$

Similarly, note that the open-loop equilibrium solution exists for the UAV m when $\varphi _ { m } ( t )$ and $\mu _ { v j } ( t )$ are determined. To this ( ) ( )end, the proof of Theorem 2 is completed.

Furthermore, by substituting (48) into (15), the dynamic reputation state ${ \dot { \mathbf { q } } } ( t )$ for verification nodes can be calculated. ( )According to the optimal solution obtained from Theorem 2, the optimal resource pricing per unit $p _ { m } ^ { * } ( t )$ for the UAV m is a monotonically decreasing function concerning the reputation matrix $\mathbf { q } ( t )$ for verification nodes. Therefore, the proposed game ( )exists a unique Stackelberg equilibrium between the UAV m and verification nodes.

## VI. SIMULATION RESULTS

In this section, we evaluate the performance of the proposed dynamic resource allocation mechanism based on Stackelberg differential games by MATLAB R2018b. First, we describe the simulation setup and most of these parameters are listed in Table II. Then, we analyze the trajectory of the UAV and the performance of the proposed trading mechanism with different settings for some parameters, respectively.

TABLE II SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Channelbandwidth B</td><td rowspan=1 colspan=1>20 Mhz</td></tr><tr><td rowspan=1 colspan=1>Channel power gain go</td><td rowspan=1 colspan=1>-30 dB</td></tr><tr><td rowspan=1 colspan=1>Channel noise power $\overline { { N _ { 0 } } }$ </td><td rowspan=1 colspan=1>-80 dBm</td></tr><tr><td rowspan=1 colspan=1>Transmission power $\overline { { P _ { m , v } } }$ </td><td rowspan=1 colspan=1>0.15s</td></tr><tr><td rowspan=1 colspan=1>Duration per round T</td><td rowspan=1 colspan=1>20s</td></tr><tr><td rowspan=1 colspan=1>Duration per slotâ³</td><td rowspan=1 colspan=1>0.2s</td></tr><tr><td rowspan=1 colspan=1>Flight altitude of UAV m H</td><td rowspan=1 colspan=1>24m</td></tr><tr><td rowspan=1 colspan=1>Average speed ofUAV m U</td><td rowspan=1 colspan=1>20m/s</td></tr><tr><td rowspan=1 colspan=1>Maximum speed of UAV m Umax</td><td rowspan=1 colspan=1>30m/s</td></tr><tr><td rowspan=1 colspan=1>Computational capacity ofUAV m $\overline { { f _ { m } } }$ </td><td rowspan=1 colspan=1>2 GHz</td></tr><tr><td rowspan=1 colspan=1>Maximum computational capacity fmax</td><td rowspan=1 colspan=1>18GHz</td></tr><tr><td rowspan=1 colspan=1>Effective switched capacitance K</td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 2 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Horizontal flight power of UAV m $\overline { { P _ { m } } }$ </td><td rowspan=1 colspan=1> $\overline { { 3 . 3 ~ \mathrm { W } } }$ </td></tr><tr><td rowspan=1 colspan=1>HardpowerlevelofUAV matfull motion $\overline { { P _ { m a x } } }$ </td><td rowspan=1 colspan=1>5W</td></tr><tr><td rowspan=1 colspan=1>Hard power level of UAV m in hovering $\overline { { P _ { i d l e } } }$ </td><td rowspan=1 colspan=1>0W</td></tr><tr><td rowspan=1 colspan=1>Hovering power of UAV m $\overline { { P _ { h } } }$ </td><td rowspan=1 colspan=1>0.0015W</td></tr><tr><td rowspan=1 colspan=1>Reputation threshold $q _ { \tau }$ </td><td rowspan=1 colspan=1>1.2</td></tr><tr><td rowspan=1 colspan=1>Unit consumption cost ${ l _ { m } ^ { t } , l _ { m } ^ { e } , l _ { v } ^ { c } }$ </td><td rowspan=1 colspan=1> $\overline { { 1 , 1 , 1 } }$ </td></tr><tr><td rowspan=1 colspan=1>Unit data computing capability of CPU (</td><td rowspan=1 colspan=1>1600 cycles/bit</td></tr><tr><td rowspan=1 colspan=1>Validate/execute/hash CPUcycles $c _ { s } , c _ { e } , c _ { h }$ </td><td rowspan=1 colspan=1>{0.1,1,0.1} MHz</td></tr></table>

## A. Simulation Settings

In the simulation, we consider a UAV-enabled MEC network integrating with blockchain. The network consists of a UAV, multiple BSs, and countless ground users, covering a rectangular area of $1 0 0 0 \times 1 0 0 0 \mathrm { { m ^ { 2 } } }$ . The UAV serves as the primary node 1000 1000 mwith its initial location high above the ground location , [0 250], which moves horizontally through trajectory planning to mprovide offloading services for ground users. The number of verification nodes is set to 20, selected from the region-wide BSs based on the high reputation principle. The verification nodes are randomly distributed within the coverage area, with their x and y coordinates varying within the range of [0,1000] . In the proposed resource allocation mechanism based on mthe Stackelberg differential game, the UAV m as a leader first releases the pricing of the unit resource for performing the tasks, and the verification nodes as followers subsequently allocate the computational resource based on this for profit. The optimal strategies for resource pricing and allocation between the UAV m and verification nodes are determined in an open-loop situation. This strategy is influenced by dynamic mobile user service requirements and the reputation of verification nodes. After consensus is reached within each time slot, 100 of %resource transactions between UAV m and verification nodes are written into the blockchain to ensure transparency and trust during computing offloading. Based on previous studies [16], [33], [36], other simulation parameter settings are given in Table II.

## B. UAV Trajectory

Fig. 2 shows the UAV trajectory varies with the number of iterations for different parameter values. We consider the UAV starts from a fixed initial position and the UAVâs angle angle during flight is set to be $\begin{array} { r } { \theta ( t ) = \arcsin \frac { \sin \theta _ { 1 } ( t ) } { \sqrt { ( \sin \theta _ { 1 } ( t ) ) ^ { 2 } + ( \cos \theta _ { 2 } ( t ) ) ^ { 2 } } } } \end{array}$ with $\begin{array} { r } { \theta _ { 1 } ( t ) = \frac { \pi t ^ { 1 . 6 } T _ { m } ^ { c 1 } ( t ) } { 4 5 6 } } \end{array}$ and $\begin{array} { r } { \theta _ { 2 } ( t ) = \frac { ( \dot { 2 } . 9 t + t ^ { 1 . 6 } ) T _ { m } ^ { c 1 } ( t ) } { 4 5 6 } } \end{array}$ . At the same time, one verification node is positioned at coordinates . , .  and the UAVâs euclidean distance to the other [344 9 349 9] mverification nodes must not exceed that of the verification node. We can see that the smaller the computational resources allocated to the UAV and the higher the number of transactions in the preliminary block result in the UAV flying a greater distance. In addition, the UAVâs turning radius during flight increases under the same conditions. The reason is that smaller computational resources and a higher number of transactions cause an increase in the UAVâs initial execution latency, leading to longer flight duration.

<!-- image-->  
Fig. 2. UAV trajectories with different $f _ { m } , N .$

Fig. 3 shows the transmission delay and offloading delay for the UAV vary with the main loop iteration number across various trajectory designs. Fig. 3(a) and (b) depict that both the transmission delay and offloading delay of the UAV exhibit an initial decrease followed by an increase. However, in Fig. 3(a), the ordering of transmission delay under different parameters is reversed as iterations are made, but the ordering in Fig. 3(b) remains the same. Because the computational resources allocated to the UAV increase, along with a higher number of transactions in the preliminary block, the UAVâs speed in approaching and moving away from the verification node also increases. As the UAV approaches the verification node, the reduction in transmission distance from the UAV to the verification node takes precedence over the impact of the number of transactions in the preliminary block on the transmission delay, so the order changes. The offloading delay of the UAV results from the combined effects of both the transmission delay and execution delay. When the transmission delay decreases, it is not enough to offset the effect of the execution delay under different parameters, so the offloading delay decreases but the order remains the same.

## C. Performance Evaluation

Figs. 4 and 5 show the optimal strategies for resource pricing and allocation based on the Stackelberg differential game under different parameter settings. In Fig. 4, the unit resource pricing of UAV all converge to the equilibrium pricing level. The UAV reduces the resource pricing per unit to maximize its utility until it drops to zero as the state of the system changes over time. In addition, it can be seen that the larger the unit QoS reward is, the more the verification nodes can gain revenue from that source, and the faster the unit resource pricing of UAV decreases to the converged state. Meanwhile, the more the number of transactions, the more the UAV gains revenue from the users. Hence, the unit resource pricing decreases and the slower the UAVâs unit resource pricing decreases to the converged state. In Fig. 5(a) and (b), we can see that the computational resources allocated by the verification nodes also all converge to the equilibrium level and show that the verification nodes with higher reputations allocate larger computational resources to provide better QoS for the UAV. Meanwhile, the larger the unit QoS reward and the smaller the number of transactions, the smaller the unit resource pricing released by the UAV, so the smaller the allocated computational resources.

<!-- image-->

(a)  
<!-- image-->  
(b)

Fig. 3. (a) Transmission delay versus different $f _ { m }$ , N under different trajectory designs. (b) Offloading delay versus different $f _ { m } , N$ under different trajectory designs.  
<!-- image-->  
Fig. 4. Optimal pricing strategies of the UAV with different $p _ { Q } , N$

<!-- image-->

<!-- image-->  
ï¼(bï¼  
Fig. 5. (a) Optimal resource allocation strategies versus different $p _ { Q }$ under different types of verification nodes. (b) Optimal resource allocation strategies versus different N under different types of verification nodes.

Figs. 6 and 7 show the influence of unit QoS reward and the number of transactions within the preliminary block on the dynamics of user service demand and the reputation of the verification nodes. The adjustment parameter $\epsilon _ { 3 }$ is set to $\epsilon _ { 3 } = - 1 . 5 * 1 0 ^ { - 2 } \ \mathrm { i f } \ p _ { m } ( t ) > 0 .$ , else $\epsilon _ { 3 } = - 0 . 8$ . In Fig. 6, we = 1 5 10 ( ) 0 = 0 8find that user service demand increases at the beginning of the game. Nonetheless, as the unit resource pricing approaches zero, the usersâ service demands decline more rapidly under the higher QoS reward and a reduced number of transactions, ultimately reaching an equilibrium state. The reason for this is that the initial cause of the influence on usersâ service demands primarily arises from the QoS delivered by the UAV. After the unit resource pricing has decayed to zero, the main impact depends on the supply and demand of the service demand. In Fig. 7(a) and (b), it can be seen that the reputation of the verification nodes grows when there is the higher unit QoS reward and the reduced number of transactions as time changes. In addition, we see that the reputation status of the verification nodes has been showing an upward trend, and the larger the initial reputation of the verification nodes, the larger it will remain during the growth process to motivate the verification nodesâ active and honest participation.

<!-- image-->  
Fig. 6. Service demands of users versus different pQ, N .

<!-- image-->  
(a)

<!-- image-->  
(bï¼  
Fig. 7. (a) Reputation state versus different pQ under different types of verification nodes. (b) Reputation state versus different N under different types of verification nodes.

<!-- image-->  
Fig. 8. Utility of the UAV versus different pQ, N .

<!-- image-->  
(aï¼

<!-- image-->  
(b)  
Fig. 9. (a) Utilities versus different pQ under different types of verification nodes. (b) Utilities versus different N under different types of verification nodes.

Figs. 8 and 9 show the convergence trends in utility for both the UAV and the verification nodes under different parameter settings In Fig. 8, we can see that the utility of the UAV will first rise and then fall to converge to a stable value. It lies in the fact that the dynamic state of user service demand has a greater impact on the utility of the UAV compared to the unit resource pricing strategy of the UAV. In addition, when the unit QoS reward and the number of transactions are greater, the user service demand increases so that the utility will be higher accordingly. From Fig. 9(a) and (b), we can see that the utilities of the verification nodes decrease and then converge. Simultaneously, it is evident that an increase in the reputation of the verification nodes corresponds to a greater allocation of computational resources by these nodes. Consequently, this heightened allocation results in more substantial benefits from the UAV, ultimately leading to an enhanced overall utility. In addition, when the unit QoS reward is smaller and the number of transactions is larger, the utility decreases as both the unit resource pricing posted by the UAV and the computational resources allocated by the verification nodes increase the benefits and outweigh the increase in computational energy consumption.

## VII. CONCLUSION

In this paper, we study the blockchain integration of UAVenabled MEC networks. For security and privacy under lowlatency computing offloading for mobile users, we propose an improved DPoS consensus mechanism in which the UAV acts as a primary node and BSs selected by the reputation mechanism act as the verification nodes. In addition, the edge computing resource allocation mechanism based on the two-stage Stackelberg differential game is proposed to facilitate resource trading between the UAV and different verification nodes. Meanwhile, the dynamic states of usersâ service demands and the reputation of verification nodes designed through differential equations are used as constraints of the objective function at various stages to simulate the userâs adaptive service request and motivate the active participation of verification nodes. A unique open-loop Stackelberg equilibrium is obtained by solving to determine the optimal decision for dynamic resource pricing and allocation. Simulation results prove the effectiveness of the proposed resource trading scheme and demonstrate the equilibrium and convergence status of resource pricing and allocation for edge computing.

## REFERENCES

[1] L. Tan, Z. Kuang, L. Zhao, and A. Liu, âEnergy-efficient joint task offloading and resource allocation in OFDMA-based collaborative edge computing,â IEEE Trans. Wireless Commun., vol. 21, no. 3, pp. 1960â1972, Mar. 2022.

[2] J. Wang, J. Hu, G. Min, A. Y. Zomaya, and N. Georgalas, âFast adaptive task offloading in edge computing based on meta reinforcement learning,â IEEE Trans. Parallel Distrib. Syst., vol. 32, no. 1, pp. 242â253, Jan. 2021.

[3] J. Du, C. Jiang, J. Wang, Y. Ren, and M. Debbah, âMachine learning for 6G wireless networks: Carrying forward enhanced bandwidth, massive access, and ultrareliable/low-latency service,â IEEE Veh. Technol. Mag., vol. 15, no. 4, pp. 122â134, Dec. 2020.

[4] H. Zhou, Z. Wang, H. Zheng, S. He, and M. Dong, âCost minimizationoriented computation offloading and service caching in mobile cloud-edge computing: An A3C-based approach,â IEEE Trans. Netw. Sci. Eng., vol. 10, no. 3, pp. 1326â1338, May/Jun. 2023.

[5] W. Wen, Y. Cui, T. Q. S. Quek, F. -C. Zheng, and S. Jin, âJoint optimal software caching, computation offloading and communications resource allocation for mobile edge computing,â IEEE Trans. Veh. Technol., vol. 69, no. 7, pp. 7879â7894, Jul. 2020.

[6] X. Dai et al., âTask co-offloading for D2D-assisted mobile edge computing in industrial Internet of Things,â IEEE Trans. Ind. Inf., vol. 19, no. 1, pp. 480â490, Jan. 2023.

[7] J. Du et al., âResource pricing and allocation in MEC enabled blockchain systems: An A3C deep reinforcement learning approach,â IEEE Trans. Netw. Sci. Eng., vol. 9, no. 1, pp. 33â44, Jan./Feb. 2022.

[8] B. Liu, Y. Wan, F. Zhou, Q. Wu, and R. Q. Hu, âResource allocation and trajectory design for MISO UAV-assisted MEC networks,â IEEE Trans. Veh. Technol., vol. 71, no. 5, pp. 4933â4948, May 2022.

[9] N. Kato et al., âOptimizing space-air-ground integrated networks by artificial intelligence,â IEEE Wireless Commun., vol. 26, no. 4, pp. 140â147, Aug. 2019.

[10] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âUAV-assisted MEC networks with aerial and ground cooperation,â IEEE Trans. Wireless Commun., vol. 20, no. 12, pp. 7712â7727, Dec. 2021.

[11] G. Li, B. He, Z. Wang, X. Cheng, and J. Chen, âBlockchain-enhanced spatiotemporal data aggregation for UAV-assisted wireless sensor networks,â IEEE Trans. Ind. Inf., vol. 18, no. 7, pp. 4520â4530, Jul. 2022.

[12] H. Yomo, A. Asada, and M. Miyatake, âOn-demand data gathering with a drone-based mobile sink in wireless sensor networks exploiting wakeup receivers,â IEICE Trans. Commun., vol. 101, no. 10, pp. 2094â2103, 2018.

[13] L. Jiang, B. Chen, S. Xie, S. Maharjan, and Y. Zhang, âIncentivizing resource cooperation for blockchain empowered wireless power transfer in UAV networks,â IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 15828â15841, Dec. 2020.

[14] Y. Wang et al., âBlockchain-based secure and cooperative private charging pile sharing services for vehicular networks,â IEEE Trans. Veh. Technol., vol. 71, no. 2, pp. 1857â1874, Feb. 2022.

[15] I. Homoliak, S. Venugopalan, D. Reijsbergen, Q. Hum, R. Schumi, and P. Szalachowski, âThe security reference architecture for blockchains: Toward a standardized model for studying vulnerabilities, threats, and defenses,â IEEE Commun. Surveys Tuts., vol. 23, no. 1, pp. 341â390, First Quarter, 2021.

[16] F. Guo, F. R. Yu, H. Zhang, H. Ji, M. Liu, and V. C. M. Leung, âAdaptive resource allocation in future wireless networks with blockchain and mobile edge computing,â IEEE Trans. Wireless Commun., vol. 19, no. 3, pp. 1689â1703, Mar. 2020.

[17] X. Qi, J. Chong, Q. Zhang, and Z. Yang, âCollaborative computation offloading in the multi-UAV fleeted mobile edge computing network via connected dominating set,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 10832â10848, Oct. 2022

[18] Z. Yang, S. Bi, and Y.-J. A. Zhang, âDynamic offloading and trajectory control for UAV-enabled mobile edge computing system with energy harvesting devices,â IEEE Trans. Wireless Commun., vol. 21, no. 12, pp. 10515â10528, Dec. 2022.

[19] Y. Nie, J. Zhao, F. Gao, and F. R. Yu, âSemi-distributed resource management in UAV-aided MEC systems: A multi-agent federated reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 70, no. 12, pp. 13162â 13173, Dec. 2021.

[20] T. Ren et al., âEnabling efficient scheduling in large-scale UAV-assisted mobile-edge computing via hierarchical reinforcement learning,â IEEE Internet Things J., vol. 9, no. 10, pp. 7095â7109, May 2022.

[21] Q. Tang, Z. Fei, J. Zheng, B. Li, L. Guo, and J. Wang, âSecure aerial computing: Convergence of mobile edge computing and blockchain for UAV networks,â IEEE Trans. Veh. Technol., vol. 71, no. 11, pp. 12073â 12087, Nov. 2022.

[22] S. Luo et al., âBlockchain-based task offloading in drone-aided mobile edge computing,â IEEE Netw., vol. 35, no. 1, pp. 124â129, Jan./Feb. 2021.

[23] M. Li, F. R. Yu, P. Si, R. Yang, Z. Wang, and Y. Zhang, âUAV-assisted data transmission in blockchain-enabled M2M communications with mobile edge computing,â IEEE Netw., vol. 34, no. 6, pp. 242â249, Nov./Dec. 2020.

[24] A. Asheralieva and D. Niyato, âDistributed dynamic resource management and pricing in the IoT systems with blockchain-as-a-service and UAVenabled mobile edge computing,â IEEE Internet Things J., vol. 7, no. 3, pp. 1974â1993, Mar. 2020.

[25] H. Xu, W. Huang, Y. Zhou, D. Yang, M. Li, and Z. Han, âEdge computing resource allocation for unmanned aerial vehicle assisted mobile network with blockchain applications,â IEEE Trans. Wireless Commun., vol. 20, no. 5, pp. 3107â3121, May 2021.

[26] W. Liu, B. Li, W. Xie, Y. Dai, and Z. Fei, âEnergy efficient computation offloading in aerial edge networks with multi-agent cooperation,â IEEE Trans. Wireless Commun., vol. 22, no. 9, pp. 5725â5739, Sep. 2023.

[27] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[28] H. Hu, Z. Chen, F. Zhou, Z. Han, and H. Zhu, âJoint resource and trajectory optimization for heterogeneous-UAVs enabled aerial-ground cooperative computing networks,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 8812â8826, Jul. 2023.

[29] Silvirianti and S. Y. Shin, âEnergy-efficient multidimensional trajectory of UAV-aided IoT networks with reinforcement learning,â IEEE Internet Things J., vol. 9, no. 19, pp. 19214â19226, Oct. 2022.

[30] Y. Zeng, and R. Zhang, âEnergy-efficient UAV communication with trajectory optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 6, pp. 3747â3760, Jun. 2017.

[31] P. K. Mu, J. Zheng, T. H. Luan, L. Zhu, Z. Su, and M. Dong, âAMIS-MU: Edge computing based adaptive video streaming for multiple mobile users,â IEEE Trans. Mobile Comput., vol. 23, no. 1, pp. 117â134, Jan. 2024.

[32] K. Lei, M. Du, J. Huang, and T. Jin, âGroupchain: Towards a scalable public blockchain in fog computing of IoT services computing,â IEEE Trans. Serv. Comput., vol. 13, no. 2, pp. 252â262, Mar./Apr. 2020.

[33] C. Lv et al., âUnmanned aerial vehicle-assisted sparse sensing in wireless sensor networks,â IEEE Wireless Commun. Lett., vol. 12, no. 6, pp. 977â981, Jun. 2023.

[34] B. Zhu, E. Bedeer, H. H. Nguyen, R. Barton, and J. Henry, âUAV trajectory planning in wireless sensor networks for energy consumption minimization by deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 70, no. 9, pp. 9540â9554, Sep. 2021.

[35] D. Hulens, T. Goedem!Â§â, and J. Verbeke, âHow to choose the best embedded processing platform for on-board UAV image processing?,â in Proc. 15th Int. Conf. Comput. Vis. Theory Appl., Berlin, Germany, 2015, pp. 1â10.

[36] B. Li, R. Yang, L. Liu, J. Wang, N. Zhang, and M. Dong, âRobust computation offloading and trajectory optimization for multi-UAV-assisted MEC: A multiagent DRL approach,â IEEE Internet Things J., vol. 11, no. 3, pp. 4775â4786, Feb. 2024.

[37] X. Hu, K. -K. Wong, K. Yang, and Z. Zheng, âUAV-assisted relaying and edge computing: Scheduling and trajectory optimization,â IEEE Trans. Wireless Commun., vol. 18, no. 10, pp. 4738â4752, Oct. 2019.

[38] W. Feng et al., âHybrid beamforming design and resource allocation for UAV-aided wireless-powered mobile edge computing networks with NOMA,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3271â3286, Nov. 2021.

[39] X. He, A. Prasad, S. P. Sethi, and G. J. Gutierrez, âA survey of stackelberg differential game models in supply and marketing channels,â J. Syst. Sci. Syst. Eng., vol. 16, no. 4, pp. 385â413, Dec. 2007.

[40] H. Gao et al., âMean-field-game-based dynamic task pricing in mobile crowdsensing,â IEEE Internet Things J., vol. 9, no. 18, pp. 18098â18112, Sep. 2022.

[41] Y. Liu, F. R. Yu, X. Li, H. Ji, and V. C. M. Leung, âDecentralized resource allocation for video transcoding and delivery in blockchain-based system with mobile edge computing,â IEEE Trans. Veh. Technol., vol. 68, no. 11, pp. 11169â11185, Nov. 2019.

[42] K. Zhu, E. Hossain, and D. Niyato, âPricing, spectrum sharing, and service selection in two-tier small cell networks: A hierarchical dynamic game approach,â IEEE Trans. Mobile Comput., vol. 13, no. 8, pp. 1843â1856, Aug. 2014.

[43] J. Du, C. Jiang, A. Benslimane, S. Guo, and Y. Ren, âSDN-based resource allocation in edge and cloud computing systems: An evolutionary stackelberg differential game approach,â IEEE/ACM Trans. Netw., vol. 30, no. 4, pp. 1613â1628, Aug. 2022.

<!-- image-->  
Die Wang (Graduate Student Member, IEEE) received the BS degree in communication engineering from Heilongjiang University, Harbin, China, in 2019. She is currently working toward the PhD degree in information and communication engineering with Chongqing University, Chongqing. Her research interests include resource allocation, blockchain, mobile edge computing, and game theory.

<!-- image-->

Yunjian Jia (Member, IEEE) received the BS degree from Nankai University, China, and the ME and PhD degrees in engineering from Osaka University, Japan, in 1999, 2003, and 2006, respectively. From 2006 to 2012, he was a researcher with Central Research Laboratory, Hitachi, Ltd., where he engaged in research and development on wireless networks, and contributed to LTE and LTE-Advanced standardization in 3GPP. He is now a professor with the School of Microelectronics and Communication Engineering, Chongqing University, China. He is the author

of more than 100 published papers, and the inventor of 40 granted patents. His current research interests include future radio access technologies, mobile networks, IoT and 6G.

<!-- image-->

Liang Liang received the BEng and MEng degrees from the Southwest University of Science and Technology (SWUST), China, in 2003 and 2006, respectively, and the PhD degree in communication and information system from the University of Electronic Science and Technology of China (UESTC), in 2012. From August 2011 to January 2012, she was an international visitor at the Institute for Infocomm Research (I2R), Singapore. She is currently an associate professor in School of Microelectronics and Communication Engineering, Chongqing University,

Chongqing, China. Her research interests include wireless communication and optimization, wireless network virtualization, mobile edge computing and IoT.

<!-- image-->

Kaoru Ota (Member, IEEE) received the BS degree in computer science and engineering from the University of Aizu, Japan, in 2006, the MS degree in computer science from Oklahoma State University, the USA, in 2008, and the PhD degree in computer science and engineering from the University of Aizu, Japan, in 2012. She is a professor and Ministry of Education, Culture, Sports, Science and Technology (MEXT) Excellent Young Researcher with the Department of Sciences and Informatics. She is also the founding director of Center for Computer Science

(CCS) at Muroran Institute of Technology, Japan. From 2010 to 2011, she was a visiting scholar with the University of Waterloo, Canada. Also, she was a Japan Society of the Promotion of Science (JSPS) research fellow, Tohoku University, Japan from 2012 to 2013. She is the recipient of IEEE TCSC Early Career Award 2017, The 13th IEEE ComSoc Asia-Pacific Young Researcher Award 2018, 2020 N2Women: Rising Stars in Computer Networking and Communications, 2020 KDDI Foundation Encouragement Award, and 2021 IEEE Sapporo Young Professionals Best Researcher Award, The Young Scientistsâ Award from MEXT, in 2023. She is Clarivate Analytics 2019, 2021, 2022 Highly Cited Researcher (Web of Science) and is selected as JST-PRESTO Researcher, in 2021, Fellow of EAJ, in 2022.

<!-- image-->

Mianxiong Dong (Member, IEEE) received BS, MS, and PhD degree in computer science and engineering from the University of Aizu, Japan. He is the vice president and professor of Muroran Institute of Technology, Japan. He was a JSPS Research Fellow with School of Computer Science and Engineering, The University of Aizu, Japan and was a visiting scholar with BBCR group with the University of Waterloo, Canada supported by JSPS Excellent Young Researcher Overseas Visit Program from 2010 to 2011. He was selected as a foreigner research fellow (a total

of 3 recipients all over Japan) by NEC C &amp; C Foundation, in 2011. He is the recipient of the 12th IEEE ComSoc Asia-Pacific Young Researcher Award 2017, Funai Research Award 2018, NISTEP Researcher 2018 (one of only 11 people in Japan) in recognition of significant contributions in science and technology, The Young Scientistsâ Award from MEXT in 2021, SUEMATSU-Yasuharu Award from IEICE, in 2021, IEEE TCSC Middle Career Award, in 2021. He is Clarivate Analytics 2019, 2021, 2022 Highly Cited Researcher (Web of Science) and Foreign Fellow of EAJ.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach/page_3_img_1.png|page_3_img_1]]
2. [[../extracted_images/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach/page_14_img_1.jpeg|page_14_img_1]]
3. [[../extracted_images/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach/page_14_img_2.jpeg|page_14_img_2]]
4. [[../extracted_images/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach/page_14_img_3.jpeg|page_14_img_3]]
5. [[../extracted_images/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach/page_14_img_4.jpeg|page_14_img_4]]
6. [[../extracted_images/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach/page_14_img_5.jpeg|page_14_img_5]]

---

