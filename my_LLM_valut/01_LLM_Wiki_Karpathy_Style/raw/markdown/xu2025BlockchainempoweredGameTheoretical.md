# Blockchain-Empowered Game Theoretical Incentive for Secure Bandwidth Allocation in UAV-Assisted Wireless Networks

Qichao Xu , Zhou Su , Haixia Peng , Yuan Wu , and Ruidong Li , Senior Member, IEEE

AbstractâRecently, the promising unmanned aerial vehicle (UAV)-assisted wireless networks (UAWNs) have emerged by advocating the UAVs to provide wireless transmission services. However, owing to the ever-growing volume of data traffic and the untrusted network operation environment, efficiently and securely assigning limited bandwidth for high-quality wireless communication between UAVs and mobile users poses a significant challenge. To address this challenge, we propose a novel secure UAV-bandwidth allocation scheme to provision reliable wireless transmission services for mobile users in UAWNs. Specifically, we first introduce a novel blockchain-empowered framework for secure bandwidth allocation, designed to automate payment processes and deter malicious activities through the immutable logging of transactional and behavioral data. Wherein, a smart contract is designed to regulate the honest behaviors of both mobile users and UAVs during bandwidth allocation with a distributed manner. Besides, a delegated proof-of-stake (DPoS) with reputation consensus protocol is presented to ensure the authenticity and efficiency of the decision-making process. Further, we apply the Stackelberg game theory to model the dynamic of the bandwidth allocation between mobile users and UAVs. In this game, the UAVs act as game leaders to determine the bandwidth price, while each mobile user acts as a game follower, making decision on the bandwidth request. We utilize the backward induction method to derive the optimal strategies of both parties, culminating in the identification of the Stackelberg equilibrium of the formulated game. Finally, extensive simulations are carried out to show the superiority of the proposed scheme over conventional schemes in terms of security, efficiency, and fairness in bandwidth allocation.

Index TermsâUAV-assisted wireless networks (UAWNs), bandwidth allocation, blockchain, game theory.

## I. INTRODUCTION

S the use of unmanned aerial vehicles (UAVs) with wire-A less transceivers increases, UAV-assisted wireless networks (UAWNs) are being advocated to offer extensive wireless connectivity for mobile users [1], [2], [3], [4], [5], [6]. UAWNs offer significant advantages over the conventional communication networks that rely on ground-based stations (GBSs) to meet mobile usersâ access requirements. Due to their flexible deployments, UAVs could quickly fly to designated destinations, such as disaster centers and temporary communication points, to provide wireless coverage. In addition, UAVs can significantly enhance the wireless networkâs capacity, addressing the blind spots caused by uneven GBS wireless signals. Moreover, wireless communication with high data rates facilitated by UAVs can effectively alleviate the geographical hotspots, which are often caused by the substantial traffic demands from mobile users. Accordingly, UAWNs, which integrate GBSs and UAVs, have emerged as a promising paradigm for the next-generation wireless communication networks, including 6G [7], [8], [9], [10].

However, efficiently provisioning spectrum bandwidth of UAVs in UAWNs faces several challenges due to limited spectrum resource and an untrusted network operating environment. The growing volume of wireless traffic limits the bandwidth available to meet each mobile userâs demand, leading to competition among users for bandwidth. In addition, the networkâs vulnerability to untrustworthiness raises the malicious UAVs capable of executing a range of attacks, such as data tampering and the dissemination of malware and viruses, during the bandwidth provisioning process. These threats can erode the confidence of mobile users in the wireless services provided by UAVs. Besides, owing to lack of authentication mechanism, the illegal mobile users can disguise as honest users to carry out attacks (e.g., distributed denial of service attack, man-in-middle, etc.) and even tamper the data delivered to other mobile users, inducing that honest mobile users cannot acquire the safe and reliable wireless communication services from UAVs. Therefore, securely allocating the limited spectrum bandwidth of UAVs to meet the growing demands of mobile users is a pressing issue.

Some existing works [11], [12], [13], [14] have provided approaches such as jamming assistance, reputation mechanism, and cryptology based auction as regards of secure bandwidth resource provisioning for mobile users. For example, in [11], [12], cooperative jamming is introduced during bandwidth allocation to prevent the eavesdropping from malicious mobile users. In [13], a reputation mechanism assesses the credibilities of both UAVs and mobile users to increase the network reliability. Additionally, cryptosystem-based auction is leveraged to avoid fraud and bid-rigging in spectrum bandwidth allocation, ensuring that the user with the highest bid attains the desired bandwidth [14]. Nevertheless, most of the current works do not take the diversity and dynamic of mobile usersâ bandwidth demands into consideration, which practically are unevenly distributed and change over time. Furthermore, in the existing works, the malicious behavior information of suspicious mobile users/UAVs is typically stored on the central servers, making it susceptible to access, removal, replacement, and tampering by attackers to avoid punishment. Besides, unlike the premise of existing works, mobile users are inherently not always to honestly pay for the bandwidth allocation to UAVs. An automatic payment mechanism that ensures accountability and non-repudiation is needed. Therefore, it is still an open and vital concern to securely allocate spectrum bandwidth between UAVs and mobile users.

In this paper, we design a novel secure bandwidth allocation scheme to provision high-quality and trusted wireless communication services in UAWNs, particularly in scenarios where partially ground infrastructures are severely damaged (e.g., disaster relief) or overloaded (e.g., communication hotspots). By deploying UAVs, flexible and responsive communication services can be rapidly established. Specifically, we first devise a blockchainempowered framework for UAV-bandwidth allocation, where the allocation process is supervised by smart contracts to enforce the honest behaviors of all entities, including UAVs and mobile users. All bandwidth allocation transactions and malicious behavior information are immutably recorded on the blockchain, enabling automatic financial settlements and preventing tampering with malicious behavior records. In particular, a reputationbased delegated proof-of-stake (DPoS) consensus protocol is devised to achieve efficient agreements in blockchain, where the reputation value is determined by assessing the entitiesâ behaviors. We then utilize a Stackelberg game model to devise a dynamic bandwidth allocation strategy between mobile users and UAVs, with the goal of maximizing the utilities of both parties. For example, during the early stages of a disaster relief operation, UAVs can dynamically adjust bandwidth prices to meet urgent rescue demands, ensuring fair and efficient use of limited communication resources. The backward induction method is exploited to derive the optimal bandwidth price for each UAV and the optimal bandwidth request for each mobile user, thereby achieving the Stackelberg equilibrium of the formulated game. Extensive simulations illustrate that the proposed scheme yields superior utilities for both UAVs and mobile users compared to conventional schemes. The key contributions of this paper are four-fold.

Framework: A blockchain-based secure bandwidth allocation framework is developed, wherein a smart contract is dedicated to regulating the executions of transactions. It records bandwidth transactions and malicious behavior information of adversaries to realize the automatical payment of bandwidth allocation and prevent the malicious denial of payment.

- Protocol: A novel reputation-based DPoS consensus protocol is devised, incorporating witness voting, block generation, and accusation behaviors of consensus entities to improve the authenticity and efficiency of the consensus process. A blacklist is deployed to mitigate the compromise by malicious UAVs and mobile users.

- Mechanism: A Stackelberg game-based incentive mechanism is presented to stimulate each UAV to allocate the spectrum bandwidth for covered mobile users. The UAVs act as game leaders to decide the bandwidth prices, and each mobile user acts as a game follower to decide the bandwidth request based on the bandwidth prices.

Strategy: The backward induction approach is used to analyze the optimal strategies of both mobile users and UAVs. The optimal bandwidth request of each mobile user is first obtained and then the close-formed expression of each UAVâs optimal bandwidth price under different budgets is resolved.

The rest of this paper is organized as follows: Section II revisits related works. The system model is presented in Section III. Section IV details the blockchain-based secure bandwidth allocation framework. Section V introduces the Stackelberg gamebased incentive mechanism. Section VI presents the simulations, and Section VII concludes the paper.

## II. RELATED WORKS

In this section, we first review the bandwidth allocation in UAWNs, and then revisit the works of game-based incentive and blockchain applications in UAWNs.

## A. Bandwidth Allocation in UAV-Assisted Wireless Networks

Recently, bandwidth allocation in UAWNs has been extensively studied. Zeng et al. [15] investigated the bandwidth allocation for UAVs deployed to provide wireless communication services with varying quality of experience (QoE) to ground users, where user requirements are randomly and unevenly distributed. Nguyen et al. [16] presented a bandwidth allocation scheme for UAVs and device-to-device users, developing a mixed-binary maximization problem to search for the optimal assignment strategy. Yan et al. [17] introduced a hierarchical game-based approach for base station bandwidth allocation and UAV access selection, investigating how much bandwidth base stations should allocate through a noncooperative game. Chen et al. [18] explored the distribution of bandwidth resources for video transmissions among multiple users in UAV-assisted relay networks, aiming to improve the enduring QoE, by employing an ascending bid auction mechanism to identify the most effective allocation strategy. Hu et al. [19] studied bandwidth allocation in UAV-aided relay networks, where a UAV can fly over users and provide decode-and-forward mobile relay services to enhance transmission performance.

However, the aforementioned bandwidth allocation scheme assumes that all entities, including mobile users and UAVs, are reliable and trustworthy during bandwidth allocation. This assumption may not hold in practical scenarios, where multiple attackers could be present. In our work, we employ a blockchain platform to immutably record and trace the malicious behaviors of both mobile users and UAVs, enhancing the security of bandwidth allocation.

## B. Game-Based Incentive in UAV-Assisted Wireless Networks

Some related works have studied the game-based incentive in UAWNs. Zhu et al. [20] proposed an incentive framework from an economic perspective for cooperative localization, where a game-theoretic algorithm is devised to obtain the optimal budget strategy for each player. Nie et al. [21] employed a game-theoretic framework involving multiple leaders and followers to devise an incentive scheme for socially responsive mobile crowd sensing, with underscoring the pivotal importance of the behaviors of both participants and service providers in the incentivization process. Le et al. [22] devised an incentive mechanism with auction game for federated learning between the base station and mobile users in wireless cellular networks, incorporating the primal-dual greedy auction algorithm to ensure truthfulness, individual rationality, and efficiency. Jiao et al. [23] proposed an incentive mechanism with Stackelberg game for wireless-powered spatial crowdsensing to assign spatial missions and the wireless charging capacity to each worker, considering the misreports of workersâ locations on the accuracy of collected data. Chen et al. [24] explored an incentive mechanism using the signaling game and applied contact theory to address information asymmetry in device-to-device computational offloading.

However, many existing game-based incentive models formulate static interactions between entities, which may not be suitable for UAV-assisted wireless networks where the locations of UAVs and mobile users change over time. In our work, we take into account the time-varying UAV network topology and the varying transmission rate demands of each mobile user. We design a dynamic game-based incentive mechanism for bandwidth allocation to address these challenges.

## C. Blockchain in UAV-Assisted Wireless Networks

The blockchain technology has been deeply applied in UAWNs. Xu et al. [25] introduced an innovative blockchainbased protocol tailored for multi-hop wireless networks, seamlessly integrating the characteristics of wireless communication and blockchain within a practical Signal-to-Interference-plus-Noise Ratio (SINR) framework. Jiang et al. [26] presented a blockchain-based decentralized flexible spectrum acquisition solution for the downlink radio communication system, accommodating a large number of mobile virtual network operators. Lu et al. [27] introduced a federated learning framework empowered by blockchain that operates in a digital twin wireless network used for cooperative computing, enhancing data privacy with improved reliability and security. Guo et al. [28] devised a mobile edge computing framework based on blockchain for next-generation wireless networks with adaptive resource allocation and compute offloading, in which the blockchain serves to provide behavior management as an overlay system. Velliangiri et al. [29] introduced the new idea of combining the privacyprotecting blockchain with the 6G wireless communication network to enhance decentralization, trust-free, immutability, openness, and so on.

<table><tr><td rowspan=1 colspan=1>Notations</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>The set of mobile users.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathcal { I } } }$ </td><td rowspan=1 colspan=1>The set ofUAVs.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathfrak { R } ^ { G B S } / \mathfrak { R } _ { i } ^ { A 2 G } } }$ </td><td rowspan=1 colspan=1>The radius of communication range of GBS/UAV.</td></tr><tr><td rowspan=1 colspan=1> $\overline { T }$ </td><td rowspan=1 colspan=1>Time horizon.</td></tr><tr><td rowspan=1 colspan=1> $\tau$ </td><td rowspan=1 colspan=1>Length of a time slot.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N } }$ </td><td rowspan=1 colspan=1>The number of time slots.</td></tr><tr><td rowspan=1 colspan=1> $t _ { n }$ </td><td rowspan=1 colspan=1>The nth time slot.</td></tr><tr><td rowspan=1 colspan=1> $h _ { i , j } ( t _ { n } )$ </td><td rowspan=1 colspan=1>Binary variable to indicate whether mobile useriinthe coverageofUAVjattime slot $t _ { n } .$ </td></tr><tr><td rowspan=1 colspan=1> $d _ { i , j } ( t _ { n } )$ </td><td rowspan=1 colspan=1>Horizontal distance between mobileuseriandUAV j at time slot $t _ { n } .$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { d _ { i , j } ( t _ { n } ) } }$ </td><td rowspan=1 colspan=1>Distance between mobile useriand UAV j at tn.</td></tr><tr><td rowspan=1 colspan=1> $\beta _ { 0 }$ </td><td rowspan=1 colspan=1>A2G channel gain with the unit distance.</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \boldsymbol { \mu } } }$ </td><td rowspan=1 colspan=1>Pathlossparameter ofLoSlink.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \sigma ^ { 2 } } }$ </td><td rowspan=1 colspan=1>Power of white Gaussian noise.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathbf { l } _ { i } ( t _ { n } ) / \mathbf { l } _ { j } ( t _ { n } ) } }$ </td><td rowspan=1 colspan=1>Location of mobile useri/UAVjat $t _ { n } .$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { V _ { j } ^ { \mathrm { m a x } } } }$ </td><td rowspan=1 colspan=1>The maximum flight velocity of UAV j.</td></tr><tr><td rowspan=1 colspan=1> $\mathcal { T } _ { j } ( t _ { n } )$ </td><td rowspan=1 colspan=1>The set of mobile users in the coverage of UAV jat $t _ { n } .$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { g _ { i , j } ( t _ { n } ) } }$ </td><td rowspan=1 colspan=1>The channel gain from UAVj to mobile useriat $t _ { n } .$ </td></tr><tr><td rowspan=1 colspan=1> $\gamma _ { i , j } ( t _ { n } )$ </td><td rowspan=1 colspan=1>SINR received by mobile useri from UAV jat tn.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P _ { j } } }$ </td><td rowspan=1 colspan=1>Transmission power of UAVj.</td></tr><tr><td rowspan=1 colspan=1> $Q _ { j }$ </td><td rowspan=1 colspan=1>Themaximum interference fromUAVjthatthe GBS can tolerate.</td></tr><tr><td rowspan=1 colspan=1> $B _ { 0 }$ </td><td rowspan=1 colspan=1>The amount of spectrum bandwidth shared bythe GBS.</td></tr><tr><td rowspan=1 colspan=1> $R _ { i , j } ( t _ { n } )$ </td><td rowspan=1 colspan=1>Transmission rate between UAVj and mobile useriat $t _ { n } .$ </td></tr><tr><td rowspan=1 colspan=1> $b _ { i , j } ( t _ { n } )$ </td><td rowspan=1 colspan=1>Spectrumbandwidth acquired fromUAV j by mobileuseriat $t _ { n } .$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { R _ { i } ( t _ { n } ) } }$ </td><td rowspan=1 colspan=1>Transmission rate demand of mobile useriat $t _ { n } .$ </td></tr><tr><td rowspan=1 colspan=1> $\underline { { \rho _ { i } } }$ </td><td rowspan=1 colspan=1>Transmission rate demand degree of mobile useri.</td></tr><tr><td rowspan=1 colspan=1> $\lambda _ { i }$ </td><td rowspan=1 colspan=1>Weighted parameter of the satisfaction of mobileuseri.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { p _ { j } ( t _ { n } ) } }$ </td><td rowspan=1 colspan=1>Bandwidth price of UAVjat $\overline { { t _ { n } . } }$ </td></tr></table>

TABLE I VARIABLES

However, unlike current works on blockchain, the entities involved in the blockchain system may be malicious, compromising the integrity of transaction records. In our work, we propose a reputation-based consensus protocol to promptly identify and exclude malicious users. This approach ensures the reliable and efficient operation of the blockchain system.

## III. SYSTEM MODEL

In this section, we present the system model, which encompasses the network model, mobility model, communication model, and security model. Table I is a summary of the notations used in this paper.

## A. Network Model

We consider a general UAWN, as shown in Fig. 1, mainly composed of one GBS, multiple UAVs and a number of mobile users. Due to the strong transmission capacity, the GBS serves a wide communication range with a radius of $\Re ^ { G B S }$ . A set of UAVs are deployed within the serving region of the GBS, which is denoted as $\mathcal { I } = \{ 1 , \ldots , j , \ldots , J \}$ . These UAVs are = 1spatially distributed over the hotspot or scotoma and act as flying base stations to provision transmission services in the respective coverage areas through the air-to-ground (A2G) communication. The communication range of each UAV j is a circular area with a radius of $\Re _ { j } ^ { A 2 G }$ . Let $\mathcal { T } = \{ 1 , \dots , i , \dots , I \}$ denote the set of j = 1mobile users that locate in the hotspot or scotoma and urgently require wireless communication services to transmit and receive data. Apparently, within the coverage of a UAV, each mobile user can connect to that UAV to access the communication services.

<!-- image-->  
Fig. 1. An illustration of UAV-assisted wireless network model.

Blockchain is a distributed transaction ledger cooperatively managed by authorized entities, including mobile users and UAVs in the network. It can be used as a distributed storage database to immutably record bandwidth allocation transactions and malicious behaviors of both mobile users and UAVs in hash-linked blocks. Due to its transparency, immutability, and traceability, each mobile user or UAV can download and check the blockchain to trace historical transactions and malicious behavior information for bandwidth allocation decision-making. Each block B in the blockchain comprises a block head and block body. The block head contains the parent block hash, current block hash, signature of the block producer, signatures of the block verifiers, timestamp, and Merkel root of transactions. The block body contains all valid transactions, sorted by timestamps and packed into a Merkle tree structure. When a new block is created by a producer, it can be appended to the end of the blockchain after achieving unanimous consensus.

## B. Mobility Model

The flying of UAVs is modeled using a 3D Cartesian coordinate system. A finite time horizon $T$ is discretized into N equal-length time slots. Let Ï denote the length of a time slot, and we have $T = N \tau$ . Then, the instantaneous location of UAV $j$ at time slot $t _ { n } \in [ t _ { 0 } + ( n - 1 ) \tau , t _ { 0 } + n \tau ]$ can be expressed as $\mathbf { l } _ { j } ( t _ { n } ) = [ x _ { j } ( t _ { n } ) , y _ { j } ( t _ { n } ) , a _ { j } ]$ 1) 0 +, where $x _ { j } ( t _ { n } )$ and $y _ { j } ( t _ { n } )$ are j( n) = [ j( n) j( n) j]horizontal location of UAV j at time slot $t _ { n } . \mathrm { ~ } a _ { j }$ j( n)is the hovering n jaltitude of UAV j, which is constant to maintain the flight without frequent ascending and descending [30].

In addition, the initial and terminal locations of $\mathrm { U A V } ~ j$ are predetermined, denoted as $1 _ { j } ( t _ { 0 } )$ and $1 _ { j } ( t _ { N } )$ , respectively. As Ï j( 0) j( N )is small enough, each UAV can be approximatively fixed at a time slot. As such, the flight trajectory of UAV j within time horizon $T$ can be represented by $\mathbf { l } _ { j } = [ \mathbf { l } _ { j } ( t _ { 0 } ) , \ldots , \mathbf { l } _ { j } ( t _ { n } ) , \ldots , \mathbf { l } _ { j } ( t _ { N } ) ]$ , where $| | \mathbf { l } _ { j } ( t _ { n - 1 } ) - \mathbf { l } _ { j } ( t _ { n } ) | | \leq V _ { j } ^ { \operatorname* { m a x } } \tau$ j. Here, $V _ { j } ^ { \mathrm { m a x } }$ represents the largest flight velocity of $\mathrm { U A V } j$ j, which serves as a constraint on mobility.

Moreover, owing to the high-speed mobility, the number of mobile users covered by each UAV changes over time. The location of mobile user i at time slot $t _ { n }$ is denoted as $\mathbf { l } _ { i } ( t _ { n } ) =$ $[ x _ { i } ( t _ { n } ) , y _ { i } ( t _ { n } ) , 0 ]$ n i( n) =, where the altitude of each mobile user is 0. [ i( n) i( n) 0]A binary indicator $h _ { i , j } ( t _ { n } ) \in \{ 0 , 1 \}$ is used to denote whether i,j( n) 0 1mobile user i is within the coverage of UAV j at time slot $t _ { n }$ . If nmobile user i is within the coverage of UAV j at time slot $t _ { n } ,$ we set $h _ { i , j } ( t _ { n } ) = 1$ , and otherwise $h _ { i , j } ( t _ { n } ) = 0$ n. The horizontal i,j( n) = 1 i,j( n) = 0distance between a mobile user and a UAV can be utilized to decide whether the mobile user is within the coverage of this UAV, i.e.,

$$
h _ { i , j } ( t _ { n } ) = \left\{ \begin{array} { l l } { 1 , \mathrm { i f } d _ { i , j } ( t _ { n } ) \le \Re _ { j } ^ { A 2 G } , } \\ { 0 , \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{1}
$$

where $d _ { i , j } ( t _ { n } )$ is the horizontal distance between UAV j and i,j ( n)mobile user i at time slot $t _ { n }$ . It is calculated by

$$
\begin{array} { r } { d _ { i , j } ( t _ { n } ) = \left[ \left( x _ { i } \left( t _ { n } \right) - x _ { j } \left( t _ { n } \right) \right) ^ { 2 } + \left( y _ { i } \left( t _ { n } \right) - y _ { j } \left( t _ { n } \right) \right) ^ { 2 } \right] ^ { \frac { 1 } { 2 } } . } \end{array}
$$

Thus, the set of mobile users within the coverage of UAV j at time slot $t _ { n }$ is denoted as $\mathcal { T } _ { j } ( t _ { n } ) = \{ i | h _ { i , j } ( t _ { n } ) = 1 , i \in \mathcal { T } \}$

(2)

## C. Communication Model

In this paper, we concentrate on the downlink communication of the network. The amount of available bandwidth occupied by the GBS is denoted as $B _ { 0 }$ . Without loss of generality, the GBS 0shares the spectrum with UAVs by an underlay model, where an interference constraint is set to avoid severe performance degradation. The interference power from UAV j to GBS is given by $F _ { j , 0 } = P _ { j } g _ { j , 0 } ,$ , where $P _ { j }$ is the transmission power j,0of UAV j and $g _ { j , 0 }$ j,0 jis the interference power gain from UAV j,0j to the GBS. The maximum interference from UAV j that the GBS can tolerate is denoted as $Q _ { j } , \mathrm { i . e . , } F _ { j , 0 } \leq Q _ { j }$ . As such, the j j,transmission power of UAV j must satisfy $P _ { j } \leq Q _ { j } / g _ { j , 0 }$

j j j,0Preliminary measurements show that A2G communication in general is comprised of a robust direct line-of-sight (LoS) link [31]. As such, for simplicity, we assume that the LoS link prevails in the transmissions between UAVs and mobile users. Thus, the power gain from the UAV j to the mobile user i is described as

$$
g _ { i , j } ( t _ { n } ) = \left\{ \begin{array} { l l } { \beta _ { 0 } \left( d _ { i , j } \left( t _ { n } \right) \right) ^ { - \mu } , \mathrm { { i f } } h _ { i , j } \left( t _ { n } \right) = 1 , } \\ { 0 , \mathrm { { i f } } h _ { i , j } \left( t _ { n } \right) = 0 , } \end{array} \right.\tag{3}
$$

where $\beta _ { 0 }$ is the A2G channel gain with the unit distance $( \mathrm { e . g . }$ 1m) and $\mu$ is the power gain parameter of LoS link. $d _ { i , j } ( t _ { n } )$ is the distance between mobile user i and UAV j at $t _ { n } .$ i,j ( n), which is calculated by

$$
d _ { i , j } \left( t _ { n } \right) = \lvert \lvert \mathbf { l } _ { i } \left( t _ { n } \right) - \mathbf { l } _ { j } \left( t _ { n } \right) \rvert \rvert _ { 2 } .\tag{4}
$$

Equation (3) also means that there is no wireless connection when mobile user i is not within the coverage of UAV i, i.e., $h _ { i , j } ( t _ { n } ) = 0$ . Then, the SINR received by mobile user i is given i,jby

$$
\gamma _ { i , j } ( t _ { n } ) = \frac { P _ { j } g _ { i , j } ( t _ { n } ) } { \sigma ^ { 2 } + P ^ { G B S } g _ { i } ^ { G B S } } ,\tag{5}
$$

where $\sigma ^ { 2 }$ is the noise power. $P ^ { G B S }$ is the transmission power of the GBS and $g _ { i } ^ { G B S }$ is channel gain between the GBS and moibile user i. Based on Shannon-Hartley theorem, the achievable transmission rate between UAV j and mobile user i at time slot $t _ { n }$ is given by

$$
R _ { i , j } ( t _ { n } ) = b _ { i , j } ( t _ { n } ) \mathrm { l o g } _ { 2 } \left( 1 + \gamma _ { i , j } ( t _ { n } ) \right) ,\tag{6}
$$

where $b _ { i , j } ( t _ { n } )$ is the acquired spectrum bandwidth of mobile i,j ( n)user i from UAV j at $t _ { n }$

## D. Threat Model

In the network, the following potential threats are considered during bandwidth allocation.

1) Malicious UAVs: There exist some malicious UAVs in the network, who can forge or tamper the transmitted data during connections with mobile users. Whatâs worse, viruses or malwares may be injected into mobile users by malicious UAVs to compromise the normal operations of the mobile devices.

2) Malicious mobile users: On one hand, malicious mobile users may disguise themselves as legitimate users to access UAVs, enabling attacks such as DDoS, man-in-themiddle, and blackhole attacks, which disrupt the normal operations of UAVs. On the other hand, malicious mobile users may deny bandwidth provisioning from UAVs and refuse to make payments.

3) Malicious behavior tampering: Cyber attackers may conduct various attacks (e.g., intrusion attacks, single point of failure attacks, etc.) on the central server responsible for tracing misbehavior. This can lead to the removal, tampering, replacement, and forging of misbehavior records to evade punishment.

## IV. BLOCKCHAIN-BASED SECURE BANDWIDTH ALLOCATION FRAMEWORK

By leveraging blockchain technology, the proposed framework provides tamper-resistant recording of malicious activities, enforces real-identity verification, and prevents deceptive acts like refusal to pay. In contrast, conventional systems without blockchain generally lack such transparency and robustness, leaving them more vulnerable to data tampering, unauthorized access, and payment disputes. In this section, we first devise a smart contract for secure bandwidth allocation and then present the reputation-based DPoS consensus protocol. At last, we conduct a security analysis of the proposed framework.

Algorithm 1: Smart Contract Execution Algorithm.   
1: Initialization   
2: Input: $I D _ { i } , \forall i \in \mathcal { T }$ and $I D _ { j } , \forall j \in { \mathcal { I } } .$   
3: i j{ pk , sk , pk , sk , add , add , depT ime, T }.   
4: $S i g _ { s k _ { i } } , \forall i \in \mathcal { T }$ jand $S i g _ { s k _ { j } } , \forall j \in \mathcal { I }$ on the smart   
contract.   
5: Deployment   
6: Input: $\overline { { d e p o s i } } i _ { i } , \forall i \in \mathcal { I }$ and deposit , $\forall j \in { \mathcal { I } } .$   
7: i Verify (deposi ${ \bf \Phi } _ { i } \geq$ userT hre).   
8: Verify (depos $i t _ { j } \geq$ uavT hre).   
9: jif t â¥ depT ime then   
10: Deploy the smart contract on the blockchain.   
11: end if   
12: Transaction   
13: Input:()   
14: for $t _ { 1 }$ to $t _ { N }$ do   
15: 1 Each $\mathrm { U A V } ~ j \in \mathcal { I }$ declares its bandwidth price   
$p _ { i } ( t _ { n } )$ to mobile users at time slot $t _ { n } .$   
16: i( n) Each mobile user $i \in \mathcal { T }$ nrequest the bandwidth   
$b _ { i , j } ( t _ { n } )$ from his/her connected UAV j at time slot   
$t _ { n } .$   
17: nif Malicious behaviors of mobile users or UAVs are   
identified then   
18: Generate a malicious behavior recording   
transaction.   
19: else   
20: Generate a normal bandwidth allocation   
transaction.   
21: end if   
22: Broadcast transactions to the whole network.   
23: end for   
24: Finalization   
25: Input:()   
26: Verify (t > depT ime  T ).   
27: +if Malicious behaviors of mobile user i or UAV j has   
been identified then   
28: Invoke P enalty .   
29: () Confiscate deposit or deposit .   
30: else   
31: Send deposit â add amd deposit â add .   
32: end if

## A. Smart Contract Design

In the blockchain system, a smart contract is a digital protocol that facilitates negotiations among interest-related entities or the processing of transactions. The smart contract uses predefined rules to execute reliable transactions without third-party intervention. In this paper, the recording of malicious behavior and optimal bandwidth allocation are automatically managed by the smart contract. The detailed composition of the smart contract is depicted in Algorithm 1, which contains four functions: Initialization, Deployment, Transaction, and Finalization.

1) Initialization: This function represents the setup phase of the smart contract, where mobile users and UAVs negotiate the terms for bandwidth allocation. Specifically, mobile users and

UAVs first register with a certification authority (CA) using their real identifications, such as a unique social security number issued by a government agency. Mobile user $i \in \mathcal { T }$ and UAV $j \in \mathcal I$ then obtain their asymmetric private/public key pairs $s k _ { i } , p k _ { i }$ and $s k _ { j } , p k _ { j }$ , account addresses $a d _ { i } = H ( p k _ { i } )$ and $a d _ { j } = H ( p k _ { j } )$ , and certifications $c e r _ { i }$ and $c e r _ { j }$ , respectively. j =Here,

$$
c e r _ { i } = { S i g _ { s k _ { C A } } \left( p k _ { i } | | i s s T i m e | | e x p T i m e \right) , }\tag{7}
$$

$$
c e r _ { j } = S i g _ { s k _ { C A } } \left( p k _ { j } | | i s s T i m e | | e x p T i m e \right) ,\tag{8}
$$

where $s k _ { C A }$ is the private key of the CA. issT ime and expT ime CAare the issue and expiration time of the certification, respectively. $H ( \cdot )$ is the secure hash function (e.g, SHA256). After that, each ( )registered entity (i.e., each mobile user or UAV) broadcasts its public key along with the certification to other entities in the blockchain system. Each entity can verify the received public keys by decrypting the certifications with the CAâs public key. Additionally, this function includes parameters related to the smart contract, such as the deployment time depT ime and the time horizon T . Finally, both mobile user i and UAV j sign the contract with their signatures using their private keys, i.e., $S i g _ { s k _ { 1 } }$ and $S i g _ { s k _ { j } }$ , respectively.

2) Deployment: Upon reaching an agreement between mobile users and UAVs, this function is invoked to initiate a new smart contract on the blockchain. Its output is the contract account address, which is then shared publicly with all registered mobile users and UAVs, to allow optional access by any entity. To mitigate malicious behavior, both mobile users i and UAV j have to deposit sufficient amounts from their accounts to the smart contract account, denoted as deposit and ${ d e p o s i t } _ { j }$ i jrespectively. To ensure compliance and normal operations, these deposits must exceed the specified thresholds userT hre and uavT hre, respectively.

3) Transaction: This function automatically executes after deploying the smart contract on blockchain. Transactions between mobile users and UAVs begin from initial time slot $t _ { 1 }$ to end time slot $t _ { N }$ 1. Here, we consider two types of transactions, Ni.e., normal bandwidth allocation transaction and malicious behavior declaring transaction.

Before UAV j offers the bandwidth price, it first generates a price token $p r i T o k e n _ { j } = \langle p _ { j } ( t _ { n } ) , H ( p _ { j } ( t _ { n } ) ) \rangle$ , where $p _ { j } ( t _ { n } )$ j = j( n)is the bandwidth price of UAV j and $H ( p _ { j } ( t _ { n } ) )$ j( n)is the hash value of $p _ { j } ( t _ { n } )$ . UAV j then sends the $p r i T o k e n _ { j }$ ))together with j (its signature $S i g _ { s k _ { j } }$ jto the mobile users within its coverage. skUpon receiving priT oken , mobile user i verifies it using the public key of UAV $\textit { j } ( p k _ { j } )$ and validates the bandwidth price $p _ { j } ( t _ { n } )$ by comparing the hash value $H ( p _ { j } ( t _ { n } ) )$ . After passing validation, mobile user i generates a bandwidth request token $r e q T o k e n _ { i } = \langle b _ { i , j } ( t _ { n } ) , p r i T o k e n _ { j } , H ( b _ { i , j } ( t _ { n } ) ) \rangle$ , where $b _ { i , j } ( t _ { n } )$ i = i,j( n) j ( i,j( n))is the requested bandwidth from UAV i and $H ( b _ { i , j } ( t _ { n } ) )$ n)is the hash value of $b _ { i , j } ( t _ { n } )$ . Mobile user i then sends reqT oken with the signature $S i g _ { s k }$ back to UAV j. UAV i skj verifies the authenticity and validity of reqT oken using pk and $H ( b _ { i , j } ( t _ { n } ) )$ i i, and subsequently allocates the corresponding ( i,j( n))bandwidth to mobile user j. Finally, the smart contract generates a bandwidth allocation transaction:

$$
t x ^ { B A } = \langle p _ { j } \left( t _ { n } \right) , b _ { i , j } \left( t _ { n } \right) , p k _ { i } , p k _ { j } , t S t a m p , S i g _ { s k _ { i } } , S i g _ { s k _ { j } } \rangle ,
$$

where tStamp is the timestamp of the transaction. Here, $p k _ { i }$ and $p k _ { j }$ iare used to denote the identities of the transaction parties.

(9)

jFor malicious behavior declaring transaction, mobile user i (or $\mathrm { U A V } ~ j )$ who recognizes the abnormal behavior (e.g., delivering fake information, virus, etc.) from any adversary can initiate a declaring transaction:

$$
\begin{array} { r l } & { t x ^ { M D } } \\ & { \quad = \langle p k _ { j } ( \mathrm { o r } p k _ { i } ) , t S t a m p , H ( E v i d ) , S i g _ { s k _ { i } } ( \mathrm { o r } ~ S i g _ { s k _ { j } } ) \rangle , } \end{array}\tag{)(10}
$$

where Evid represents the evidence collected regarding the malicious behavior. Finally, all newly generated transactions are broadcasted to all entities. Once consensus is reached, both the malicious behavior and bandwidth transaction information are immutably recorded on the blockchain. Proper security countermeasures can then be taken to address the malicious behaviors.

4) Finalization: This function is executed when the current time exceeds the time horizon. If malicious behavior occurs, the Penalty() function is called. For instance, if the malicious behavior of mobile user i is identified by UAV j and verified by entities in the blockchain, deposit will be confiscated by ithe smart contract. Conversely, if both mobile user i and UAV j behave legitimately, the smart contract performs the financial settlement, returning the deposits to their respective accounts. Additionally, after the consensus process, the payment for the corresponding bandwidth allocation is automatically transferred from the account of mobile user i to that of UAV j.

The computational complexity of Algorithm 1 is analyzed as follows:

In the Initialization phase (Lines 1-4), the algorithm registers mobile users and UAVs, generates cryptographic key pairs, and stores digital signatures. Let |I| and $| \mathcal { I } |$ be the numbers of mobile users and UAVs, respectively. These operations require a single pass over the entire set of participants, resulting in a complexity of $\mathcal { O } ( | \mathcal { T } | + | \mathcal { I } | )$

( + )The Deployment phase (Lines 5-11) verifies each users and UAVs deposit, ensuring it meets the threshold requirements, and deploys the smart contract when depTime is reached. Verifying deposits for |I| users and |J | UAVs incurs $\mathcal { O } ( | \mathcal { T } | + | \mathcal { I } | )$ time, ( + )while time validation and contract deployment occur in $\mathcal { O } ( 1 )$ Thus, overall complexity remains $\mathcal { O } ( | \mathcal { T } | + | \mathcal { I } | )$ .

( + )The Transaction phase (Lines 12-23) repeats for N time slots. It includes generating price tokens, validating requests, and broadcasting transactions. Most cryptographic routines (hashing, signing, and verification) execute in O . Transaction (1)broadcasting, which involves sending data among $| \mathcal { T } | + | \mathcal { I } |$ network nodes, dominates the complexity at $\mathcal { O } ( | \mathcal { T } | + | \mathcal { I } | )$ . Across ( +N time slots, this leads to a total complexity of $O ( N \cdot ( | \mathcal { T } | +$ $| \mathcal { I } | )$

)The Finalization phase (Lines 24-32) checks contract expiration and processes deposits, requiring only O .

Overall, the Transaction phase determines the worst-case complexity, whereby the total complexity of Algorithm 1 is $\mathcal { O } ( N \cdot ( | \mathcal { T } | + | \mathcal { I } | )$

## B. Reputation-Based DPoS Consensus Protocol

We devise a DPoS with reputation consensus protocol to securely achieve consensus in the blockchain. The detailed consensus process comprises the following steps:

Step 1: Reputation Assessment. The reputation value serves as the stake of each entity for blockchain consensus, updated after each consensus round based on the entitiesâ behaviors. Positive behaviors increase the reputation value, while negative behaviors (e.g., malicious behavior, non-cooperation) can decrease it. During a consensus round, the following behaviors are considered:

1) Voting Behavior: Entities actively participating in voting receive a high voting reward $\widetilde { r } ^ { v o t }$ , while refusing to vote results in a punishment $\widetilde { p } ^ { v o t }$

2) Block Generation: Successfully generating a block is rewarded with $\widetilde { r } ^ { g e n }$ , but failure to do so or generating a wrong block leads to a penalty $\widetilde { p } ^ { g e n }$

3) Malicious Behavior Identification: Successfully identifying malicious behaviors of other entities is rewarded with $\widetilde { r } ^ { m a l }$ while misidentifying or falsely claiming normal behavior as malicious results in a punishment $\widetilde { p } ^ { m a l }$

Entities accurately identified and confirmed for malicious behavior are directly blacklisted. Considering that the influence of behavior decays over time, the positive reputation value of entity $k \in \mathcal { T } \bigcup \mathcal { T }$ is given by:

$$
\Upsilon _ { k } ^ { p } = \sum _ { l = 1 } ^ { L _ { k } ^ { p } } \left\{ \left( \varepsilon _ { l } ^ { v o t } \widetilde { r } ^ { v o t } + \varepsilon _ { l } ^ { g e n } \widetilde { r } ^ { g e n } + \varepsilon _ { l } ^ { m a l } \widetilde { r } ^ { m a l } \right) \right\} ,\tag{11}
$$

where $L _ { k } ^ { p }$ is the total number of positive behaviors conducted by entity $k . \exp ( \cdot )$ represents the exponential time decay function, and $\chi$ is the decay parameter. t denotes the current time, and t lis the time at which the lth behavior occurred. The parameters $\varepsilon _ { l } ^ { v o t } , \varepsilon _ { l } ^ { g e n }$ , and $\varepsilon _ { l } ^ { m a l }$ are defined as follows:

$$
\varepsilon _ { l } ^ { v o t } = \left\{ { 1 , \mathrm { ~ i f ~ b e h a v i o r ~ i s ~ a ~ v o t i n g ~ b e h a v i o r } , } \atop { 0 , \mathrm { ~ o t h e r w i s e . } }  \right.\tag{12}
$$

$$
\varepsilon _ { l } ^ { g e n } = \left\{ \begin{array} { l l } { 1 , \mathrm { i f ~ b e h a v i o r ~ i s ~ a ~ s u c c e s s f u l ~ b l o c k ~ g e n e r a t i o n } , } \\ { 0 , \mathrm { ~ o t h e r w i s e } . } \end{array} \right.\tag{13}
$$

$$
\varepsilon _ { l } ^ { m a l } = \left\{ \begin{array} { l l } { { 1 , \mathrm { ~ i f ~ b e h a v i o r ~ i s ~ a ~ s u c c e s s f u l ~ i d e n t i f i c a t i o n , } } } \\ { { 0 , \mathrm { ~ o t h e r w i s e . } } } \end{array} \right.\tag{14}
$$

The negative reputation value of entity k is calculated as

$$
\Upsilon _ { k } ^ { n } = \sum _ { l = 1 } ^ { L _ { k } ^ { n } } \left\{ \left( \epsilon _ { l } ^ { v o t } \widetilde { p } ^ { v o t } + \epsilon _ { l } ^ { \mathrm { g e n } } \widetilde { p } ^ { \mathrm { g e n } } + \epsilon _ { l } ^ { \mathrm { m a l } } \widetilde { p } ^ { m a l } \right) \times \right\} ,\tag{15}
$$

where $L _ { k } ^ { n }$ is the total number of negative behaviors conducted by entity $k . \epsilon _ { l } ^ { v o t } , \epsilon _ { l } ^ { g e n }$ and $\epsilon _ { l } ^ { m a l }$ are respectively defined as follows:

$$
\epsilon _ { l } ^ { v o t } = \left\{ \begin{array} { l l } { { 1 , \mathrm { ~ i f ~ b e h a v i o r ~ i s ~ t h e ~ n o n v o t i n g ~ b e h a v i o r , } } } \\ { { 0 , \mathrm { ~ o t h e r w i s e . } } } \end{array} \right.\tag{16}
$$

$$
\epsilon _ { l } ^ { g e n } = \left\{ \begin{array} { l } { { 1 , \mathrm { ~ i f ~ b e h a v i o r ~ i s ~ f a l s e ~ b l o c k ~ g e n e r a t i o n } , } } \\ { { 0 , \mathrm { ~ o t h e r w i s e } . } } \end{array} \right.\tag{17}
$$

$$
\epsilon _ { l } ^ { m a l } = \left\{ \begin{array} { l } { { 1 , \mathrm { ~ i f ~ b e h a v i o r ~ i s ~ t h e ~ f a l s e ~ i d e n t i f i c a t i o n , } } } \\ { { 0 , \mathrm { ~ o t h e r w i s e . } } } \end{array} \right.\tag{18}
$$

By integrating the positive and negative reputation values, the comprehensive reputation value of entity k can be obtained by

$$
R e p _ { k } = \frac { \Upsilon _ { k } ^ { p } } { \Upsilon _ { k } ^ { p } + \eta \Upsilon _ { k } ^ { n } } ,\tag{19}
$$

where Î· is a punishment factor used to penalize negative behaviors of each entity, and it is a real number greater than 1. Then, we define a threshold: an entity whose reputation value is less than $\zeta ^ { R e p } \ : ( \mathrm { i . e . , } \ : R e p _ { k } < \zeta ^ { R e p } )$ is added to the blacklist. Members in kthe blacklist are excluded from participating in the consensus process to ensure the security and stability of the blockchain.

Step 2: Witness Election. A subset of entities, called witnesses, are elected to produce and validate blocks instead of involving all entities in the blockchain. This approach significantly enhances transaction throughput, with potential rates exceeding 100,000 transactions per second [32]. Entities not on the blacklist, referred to as shareholders, have the right to vote for members of the witness committee $\mathcal { W } = \{ 1 , \dots , w , \dots , W \}$ . The voting power of each shareholder $k \in \mathcal { K }$ 1is determined by its reputation value, i.e., $R e p _ { k }$ . Therefore, entities with higher reputation valkues wield greater influence on the blockchain, as they are more invested in the systemâs operation and stand to incur heavier losses if the blockchain fails. Let $\Pi _ { k }$ represent the voting weight of entity $k ,$ calculated as:

$$
\Pi _ { k } = \sum _ { k ^ { \prime } \in \mathcal { V } _ { k } } R e p _ { k ^ { \prime } } ,\tag{20}
$$

where $\nu _ { k }$ is the set of entities that vote for the entity k and $R e p _ { k ^ { \prime } }$ is the reputation value of entity $k ^ { \prime }$ . Entities with higher kvoting scores have a greater chance of becoming witnesses. By arranging entities in descending order of their voting scores, we can select the top $W$ entities to form the witness committee.

Committee members possess equal rights to create, broadcast, and verify blocks, regardless of the number of votes they received. This approach ensures that entities with low reputation values require substantial support from high-reputation entities to become witnesses, reducing the risk of malicious entities being elected. All voting scores and reputation values are recorded on the blockchain, allowing each entity to verify the scores through blockchain synchronization. If a witness fails to adhere strictly to the consensus protocol, entities voting for that witness can revoke their votes. Consequently, the witnessâs voting score decreases, potentially leading to their removal from the committee. This process ensures that committee remains honest and reliable.

Step 3: Consensus Process. In each consensus round, a witness is randomly selected from witness committee to validate transactions and create blocks. Once a witness has produced a block, he/she cannot be selected as a producer again until the committee is updated after $W$ consensus rounds. When selected as a block producer, the witness w first validates all collected transactions, including bandwidth allocation transactions and malicious behavior declaring transactions. Valid transactions are then packaged into a local block B. Subsequently, the witness broadcasts a block proposal blockP rop, which includes the unverified block B and the producerâs signature $S i g _ { k }$ , to other witnesses for block validation, where we have

$$
b l o c k P r o p = \langle P r o p o s a l | \mathfrak { B } | | H ( \mathfrak { B } ) | t S t a m p | | S i g _ { s k _ { w } } \rangle .\tag{21}
$$

After receiving the proposal message, all witnesses verify the attached block and return the auditing results to all members of witness committee. If the block passes verification, each verifier $w ^ { \prime } \in \mathcal { W }$ broadcasts a block confirmation blockConf with its signature $S i g _ { s k _ { w } ^ { \prime } }$ :

$$
b l o c k C o n f = \langle C o n f i r m | | H ( \mathfrak { B } ) | t S t a m p | | S i g _ { w ^ { \prime } } \rangle .\tag{22}
$$

If more than two-thirds of witnesses confirm the block B, the newly created block is sequentially appended to the blockchain. In the event of a fork, the longest chain representing the majority of entity decisions is accepted as the correct one. All entities download the longest chain to synchronize their local copies and prepare for the next consensus round.

## C. Security Analysis

First, since the smart contract is utilized to supervise the interactions between UAVs and mobile users, any malicious behavior (e.g., DDoS attacks, data tampering attacks, etc.) can be detected and recorded on the blockchain, where the deposits of malicious entities are confiscated. As conducting malicious behavior greatly increases the cost, the willingness of malicious mobile users or UAVs to compromise the normal performance of bandwidth allocation is reduced. Second, all mobile users must use their real identities to obtain authorization to access the network, making it difficult for malicious UAVs to disguise themselves as honest users to launch attacks. Third, since transactions are distributedly audited and recorded on the blockchain, the ârefuse to payâ attacks carried out by malicious mobile users and other deceptive actions by malicious entities can be effectively addressed. Additionally, due to the distributed ledger and specific hash-linked structure of the blockchain, if an entity intends to alter the information about malicious behavior recorded on the blockchain, the modified block would require no less than 2/3 agreement from witnesses and would need to further modify the hash values of subsequent blocks, which would undoubtedly incur a considerable cost. Thus, the threat of malicious behavior tampering can be successfully mitigated.

## D. Resource Consumption Analysis of Blockchain-Based Framework

The resource consumption of UAVs and mobile users in our blockchain-based framework primarily comprises memory overhead, computational load, and communication cost.

- Memory overhead: Because UAVs and mobile users often have limited storage, it is not mandatory for each participant to maintain the entire blockchain locally. Rather, they can function as lightweight nodes, storing only a recent subset of blocks necessary for ongoing bandwidthallocation transactions. Older blocks can be pruned or offloaded to external storage (e.g., cloud servers), which significantly reduces the memory footprint on resourceconstrained devices.

Computational load: Our reputation-based DPoS mechanism incurs much lower computational overhead compared to mining-based protocols. Only a small subset of witnesses handle tasks such as block creation and validation, while most UAVs and mobile users only submit transactions and do not directly participate in intensive consensus operations. Consequently, the majority of nodes experience limited computational overhead, making the framework suitable for resource-constrained UAVs and mobile users.

Communication cost: Because each consensus round involves only a small committee of witness nodes, the communication overhead for the majority of UAVs and mobile users is kept at a feasible level. Additionally, Only lightweight messages (e.g., vote casting or identity verification) are broadcast network-wide, further reducing overall communication requirements.

By employing partial block storage and a DPoS-based committee, the framework keeps resource consumption within practical limits for UAVs and mobile users, ensuring overall feasibility of the framework.

## V. STACKELBERG GAME-BASED OPTIMAL BANDWIDTH ALLOCATION DECISION

In this section, we use the Stackelberg game to determine the optimal bandwidth allocation strategies for UAVs and mobile users. We begin by formulating the bandwidth allocation problem as a Stackelberg game, where the UAVs act as leaders and the mobile users as followers. Next, we apply the backward induction method to analyze the Stackelberg equilibrium, which provides the optimal solution for both parties. This involves analyzing the optimal bandwidth requests of mobile users first, followed by determining the optimal bandwidth prices set by the UAVs.

## A. Problem Formulation

In the network, subject to interference constraints, each UAV allocates the spectrum bandwidth shared from the GBS to the covered mobile users. Each UAV initially set bandwidth price to maximize its utility. Subsequently, each mobile user purchases a certain bandwidth from connecting UAV to achieve the desired A2G transmission rate. The utility of UAV j is given by

$$
\mathbb { U } _ { j } \left( p _ { j } ( t _ { n } ) , \mathbf { b } _ { j } ( t _ { n } ) \right) = \sum _ { i = 1 } ^ { I } h _ { i , j } ( t _ { n } ) \cdot p _ { j } ( t _ { n } ) \cdot b _ { i , j } ( t _ { n } ) ,\tag{23}
$$

where $\mathbf { b } _ { j } ( t _ { n } )$ is the bandwidth request vector of mobile users j( n)that connect to UAV j at $t _ { n }$

nThe utility of each mobile user is based on the satisfaction and cost. The satisfaction of mobile user i is given by

$$
\mathbb { S } _ { i } \left( b _ { i , j } ( t _ { n } ) , p _ { j } ( t _ { n } ) \right) = 1 - \exp \left( - \rho _ { i } \frac { R _ { i } ( t _ { n } ) } { \widetilde { R _ { i } } ( t _ { n } ) } \right) ,\tag{24}
$$

where $\widetilde { R _ { i } } ( t _ { n } )$ is transmission rate demand of mobile user i at $t _ { n }$ and $\rho _ { i }$ represents the demand degree of mobile user i on $\widetilde { R _ { i } } ( t _ { n } )$ i i( n)As shown in (24), mobile user i obtains a large satisfaction when he/she attains much bandwidth. Since a mobile user should pay for the bandwidth purchase, he/she has a certain cost on the bandwidth request. The cost of mobile user i is defined as

$$
\mathbb { C } _ { i } \left( b _ { i , j } ( t _ { n } ) , p _ { j } ( t _ { n } ) \right) = p _ { j } ( t _ { n } ) \cdot b _ { i , j } ( t _ { n } ) ,\tag{25}
$$

where $p _ { j } ( t _ { n } )$ is the unit price of UAV j at $t _ { n }$ . Combining the satisfaction and the cost, the utility of mobile user i is

$$
\begin{array} { r l } & { \mathbb { U } _ { i } \left( b _ { i , j } ( t _ { n } ) , p _ { j } ( t _ { n } ) \right) } \\ & { \quad = \mathrm { S } _ { i } \big ( b _ { i , j } ( t _ { n } ) , p _ { j } ( t _ { n } ) \big ) - \mathbb { C } _ { i } \left( b _ { i , j } ( t _ { n } ) , p _ { j } ( t _ { n } ) \right) } \\ & { \quad = \lambda _ { i } \left( 1 - \exp \left( - \rho _ { i } \frac { b _ { i , j } \left( t _ { n } \right) \log _ { 2 } \left( 1 + \gamma _ { i , j } \left( t _ { n } \right) \right) } { \widetilde { R _ { i } } \left( t _ { n } \right) } \right) \right) } \\ & { \quad \quad - p _ { j } ( t _ { n } ) b _ { i , j } ( t _ { n } ) , } \end{array}\tag{26}
$$

where $\lambda _ { i }$ is the weighted parameter of the satisfaction from imobile user i.

The Stackelberg game model is employed to formulate the bandwidth allocation between UAVs and mobile users, with UAV acting as the leaders and the mobile users as followers. This model allows for the investigation of the multi-level decisionmaking process in which independent decisions are made by multiple decision-makers with respect to the leading player in the game. Specifically, each $\mathrm { U A V } ~ j \in \mathcal { I }$ determines the bandwidth price $p _ { j } ( t _ { n } )$ first. Each mobile user $i \in \mathcal { T }$ then responds with j( n)the optimal bandwidth request $b _ { i , j } ( t _ { n } )$ , with the objectives of i,j( n)both UAVs and mobile users being to maximize their utilities. Therefore, for each mobile user i and each UAV j, we can formulate the following maximization problems:

$$
\mathrm { s . t . } \ \left\{ { p } _ { j } ( t _ { n } ) \geq 0 , \right. \qquad { \mathrm { S . t . } } \ \left\{ { \sum } _ { i = 1 } ^ { I _ { j } } b _ { i , j } ( t _ { n } ) \leq { B } _ { 0 } . \right.\tag{27}
$$

$$
\mathrm { s . t . } b _ { i , j } ( t _ { n } ) \geq 0 .\tag{28}
$$

The Stackelberg equilibrium is deemed as the solution to formulated problems, which is defined as follows.

Definition 1: Let $b _ { i , j } ( t _ { n } ) ^ { * }$ denote the solution to Problem 2, and $p _ { j } ( t _ { n } ) ) ^ { * }$ i,j( n)denote the solution to Problem 1. Then, the point $( \mathbf { b } _ { j } ( t _ { n } ) ^ { * } , p _ { j } ( t _ { n } ) ^ { * } )$ is a Stackelberg equilibrium if for any $( \mathbf { b } _ { j } ( t _ { n } ) , p _ { j } ( t _ { n } ) )$ j( n)with $\mathbf { b } _ { j } ( t _ { n } ) \geq \mathbf { 0 }$ and $p _ { j } ( t _ { n } ) \geq 0$ , the following ( j( n) j( n)) jconditions are satisfied:

$$
\mathbb { U } _ { j } \left( p _ { j } ( t _ { n } ) ^ { * } , \mathbf { b } _ { j } ( t _ { n } ) ^ { * } \right) \geq \mathbb { U } _ { j } \left( p _ { j } ( t _ { n } ) , \mathbf { b } _ { j } ( t _ { n } ) ^ { * } \right) ,\tag{29}
$$

$$
\mathbb { U } _ { i } \left( b _ { i , j } ( t _ { n } ) ^ { * } , p _ { j } ( t _ { n } ) ^ { * } \right) \geq \mathbb { U } _ { i } \left( b _ { i , j } ( t _ { n } ) , p _ { j } \left( t _ { n } \right) ^ { * } \right) ,\tag{30}
$$

$$
{ \mathrm { w h e r e } } \ \mathbf { b } _ { j } ( t _ { n } ) ^ { * } = [ b _ { 1 , j } ( t _ { n } ) ^ { * } , \ldots , b _ { i , j } ( t _ { n } ) ^ { * } , \ldots , b _ { I , j } ( t _ { n } ) ^ { * } ] .
$$

## B. Game Analysis

We utilize the backward induction method to analyze the Stackelberg equilibrium. Specifically, we analyze the optimal bandwidth request of each mobile user and subsequently elaborate on the optimal bandwidth prices of UAVs.1

1) The Optimal Bandwidth Request of Mobile User: After receiving the bandwidth price set by UAV j, mobile user i determines the optimal decision on bandwidth request to maximize its utility. The optimal decision for mobile user i can be determined by solving Problem 2, as stated in the following theorem.

Theorem 1: When the bandwidth price of UAV j is given, the optimal bandwidth request of mobile user i that connects to UAV j is

$$
b _ { i , j } ^ { * } = \left[ \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { i } } } \right] ^ { + } ,\tag{31}
$$

where $[ \cdot ] ^ { + } = \operatorname* { m a x } ( \cdot , 0 )$ and $\Lambda _ { i , j } = \log _ { 2 } ( 1 + \gamma _ { i , j } )$

[ ] = max( 0) Îi,j = log2(1 + i,j)Proof: The first derivative of the utility from mobile user i with respect to bandwidth request $b _ { i , j }$ is

$$
\frac { \partial \mathbb { U } _ { i } \left( b _ { i , j } , p _ { j } \right) } { \partial b _ { i , j } } \ = \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { \widetilde { R _ { j } } } \exp \left( \frac { - \rho _ { i } b _ { i , j } \Lambda _ { i , j } } { \widetilde { R _ { j } } } \right) - p _ { j } .\tag{32}
$$

The second derivative of the utility $\mathbb { U } _ { i } ( b _ { i , j } , p _ { j } )$ with respect to $b _ { i , j }$ is

$$
\frac { \partial ^ { 2 } \mathbb { U } _ { i } \left( b _ { i , j } , p _ { j } \right) } { \partial { \left( b _ { i , j } \right) } ^ { 2 } } = - \lambda \left( \frac { \rho _ { i } \Lambda _ { i , j } } { \widetilde { R _ { j } } } \right) ^ { 2 } \exp \left( \frac { - \rho _ { i } b _ { i , j } \Lambda _ { i , j } } { \widetilde { R _ { j } } } \right) < 0 .\tag{33}
$$

As the second derivative is negative, the utility $\mathbb { U } _ { i } ( b _ { i , j } , p _ { j } )$ is a i( i,j j)concave function, whereby the maximum utility for mobile user i exists. Then, we conduct the following two limit calculations.

$$
\operatorname* { l i m } _ { b _ { i , j }  + \infty } \frac { \partial \mathbb { U } _ { i } ( b _ { i , j } , p _ { j } ) } { \partial b _ { i , j } } = - p _ { j } < 0 ,\tag{34}
$$

$$
\operatorname* { l i m } _ { b _ { i , j }  0 } \frac { \partial \mathbb { U } _ { i } ( b _ { i , j } , p _ { j } ) } { \partial b _ { i , j } } = \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { \widetilde { R _ { j } } } - p _ { j } .\tag{35}
$$

From (35), when $b _ { i , j } = 0$ , the first derivative of the utility can i,j = 0be negative or positive. Here, two cases are considered:

Case 1. Bandwidth price is low: Here, the bandwidth price determined by UAV j is less than or equal to $\frac { \Lambda _ { i , j } \lambda \rho _ { i } } { \widetilde { R _ { i } } }$ , i.e, $\begin{array} { r } { p _ { j } \le \frac { \Lambda _ { i , j } \lambda \rho _ { i } } { \widetilde { R _ { i } } } } \end{array}$ . As such, $\begin{array} { r l } { b _ { i , j } {  } 0 } & { { } \frac { { \partial } \mathbb { U } _ { i } ( b _ { i , j } , p _ { j } ) } { { \partial } b _ { i , j } } } \end{array}$ is larger than Rzero. Hereby, $\mathbb { U } _ { i } ( b _ { i , j } , p _ { j } )$ first monotonically increases and then i( i,j j)gradually decreases with respect to $b _ { i , j }$ . The optimal bandwidth i,jrequest of mobile user i from UAV j is attained by solving the

following equation.

$$
\frac { \partial \mathbb { U } _ { i } \left( b _ { i , j } , p _ { j } \right) } { \partial b _ { i , j } } = 0 .\tag{36}
$$

As such, the optimal bandwidth request decision of mobile user i from UAV j is

$$
b _ { i , j } ^ { * } = \frac { \widetilde { R _ { j } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { j } } } .\tag{37}
$$

Case 2. Bandwidth price is high: Here, the bandwidth price of UAV j is larger than $\frac { \Lambda _ { i , j } \lambda \rho _ { i } } { \widetilde { R _ { i } } }$ , i.e, $\begin{array} { r } { p _ { j } > \frac { \Lambda _ { i , j } \lambda \rho _ { i } } { \widetilde { R _ { i } } } } \end{array}$ . As such, $\begin{array} { r } { \operatorname* { l i m } _ { b _ { i , j }  0 } \frac { \partial \mathbb { U } _ { i } ( b _ { i , j } , p _ { j } ) } { \partial b _ { i . i } } < 0 } \end{array}$ , whereby the first derivative of utility âbcontinues to be negative with an escalation in the bandwidth demand. Accordingly, the optimal bandwidth request determined by mobile user i from UAV j is $b _ { i , j } { } ^ { * } = 0$ -

i,j = 02) The Optimal Bandwidth Price of UAV: Based on Theorem 1, the utility function of UAV j can be rewritten by

$$
\mathbb { U } _ { j } ( p _ { j } , \mathbf { b } _ { j } ) = p _ { j } \sum _ { i = 1 } ^ { I } h _ { i , j } \left[ \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { i } } } \right] ^ { + } .\tag{38}
$$

Then, Problem 1 can be rewritten as

Problem 3

$$
\operatorname* { m a x } _ { p _ { j } } p _ { j } \sum _ { i = 1 } ^ { I } h _ { i , j } \left[ \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { i } } } \right] ^ { + }
$$

$$
\mathrm { s . t . } \ \left\{ \begin{array} { l l } { p _ { j } \geq 0 , } \\ { \sum _ { i = 1 } ^ { I } h _ { i , j } \left[ \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { i } } } \right] ^ { + } \leq B _ { 0 } . } \end{array} \right.\tag{39}
$$

Due to the constraint imposed by the bandwidth price, the utility function of each UAV in (38) is discontinuous. This makes solving Problem 3 directly for seeking extremes intractable. However, Problem 3 can be reformulated into multiple convex subproblems once the bandwidth budget (i.e., the amount of available bandwidth) of each UAV is determined.

For mobile user i located within the coverage of UAV j, the following indicator function is first introduced.

$$
z _ { i , j } = \left\{ \begin{array} { l l } { 1 , \ \mathrm { i f } \ p _ { j } \le \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { \widetilde { R _ { i } } } , } \\ { 0 , \ \mathrm { o t h e r w i e s e } . } \end{array} \right.\tag{40}
$$

Then, Problem 3 is reformulated as

Problem 4

$$
\operatorname* { m a x } _ { p _ { j } , \mathbf { z } _ { j } } p _ { j } \sum _ { i = 1 } ^ { I } { h _ { i , j } z _ { i , j } \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { i } } } } ,
$$

$$
\mathrm { s . t . } \ \left\{ \begin{array} { l l } { p _ { j } \geq 0 , } \\ { \sum _ { i = 1 } ^ { I } h _ { i , j } z _ { i , j } \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { i } } } \leq B _ { 0 } , } \end{array} \right.\tag{41}
$$

where $\mathbf z _ { j } = [ z _ { 1 , j } , \dotsc , z _ { i , j } , \dotsc , z _ { I , j } ]$ . Problem 4 is non-convex due to $\mathbf { z } _ { j } .$ = [ 1,j i,j I,j ], whose elements are 0-1 variables. Yet, when the jindicator vector $\mathbf { z } _ { j }$ is determined, Problem 4 is apparently a convex problem.

First of all, a special case is considered that available bandwidth owned by UAV j is large enough, so that all requesting mobile users can acquire bandwidth. As such, all indicators equal to 1, whereby $\begin{array} { r } { \bar { p } _ { j } \le \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { \widetilde { R _ { i } } } } \end{array}$ . Here, Problem 4 could be

rewritten as

$$
\mathbf { P r o b l e m 5 : } \operatorname* { m a x } _ { p _ { j } } p _ { j } \sum _ { i = 1 } ^ { I } h _ { i , j } \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { i } } }
$$

$$
\begin{array} { r } { \mathrm { s . t . ~ } \left\{ \begin{array} { l l } { p _ { j } \geq 0 , } \\ { \sum _ { i = 1 } ^ { I } h _ { i , j } \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { p _ { j } \widetilde { R _ { i } } } \leq B _ { 0 } , } \\ { p _ { j } \leq \operatorname* { m i n } \{ \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { R _ { i , j } } \} _ { i \in \mathcal { I } _ { j } } . } \end{array} \right. } \end{array}\tag{42}
$$

Here $\mathcal { T } _ { j }$ is the set of mobile users within the coverage of UAV j.   
jThe solution to Problem 5 is delineated in the following theorem.

Theorem 2: The optimal bandwidth price of UAV j for Problem 5 is at the top of the next page.

Proof: Please refer to the Appendix A, available online. We then associate the optimal solution of Problem 5 with that of Problem 3, through the following theorem.

Theorem 3: The bandwidth price given by (43), shown at the bottom of the next page, is the optimal solution to Problem 3 if and only if that the following condition is satisfied:

$$
B _ { 0 } \geq \sum _ { i = 1 } ^ { I } h _ { i , j } \frac { \widetilde { R _ { i } } } { \rho _ { i } \Lambda _ { i , j } } \log \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { \operatorname* { m i n } \{ \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { \widetilde { R _ { i } } } \} _ { i \in \mathcal { I } _ { j } } \widetilde { R _ { i } } } .\tag{44}
$$

Proof: Please refer to the Appendix B, available online. According to the above obtained results, the optimal solution to Problem 3 is achieved from the following theorem.

Theorem 4: We set $\begin{array} { r } { \varphi _ { i , j } = \frac { \lambda \rho _ { i } \Lambda _ { i , j } } { \widetilde { R } _ { i } } } \end{array}$ and assume that all mobile users in the coverage of $\mathrm { U A V } ~ j$ have been sorted in the order $\varphi _ { 1 , j } > \cdot \cdot \cdot > \varphi _ { i , j } > \cdot \cdot \cdot > \varphi _ { | \mathscr { T } _ { j } | , j }$ . The optimal solution 1,j i,jfor Problem 3 is expressed as

$$
\begin{array} { r } { { p _ { j } } ^ { * } = \left\{ \begin{array} { l l } { p _ { j } ^ { | \mathcal { T } _ { j } | ^ { * } } , \mathrm { ~ i f ~ } B _ { 0 } \geq \Phi _ { | \mathcal { Z } _ { j } | , j } , } \\ { \vdots } \\ { p _ { j } ^ {  i } , \mathrm { ~ i f ~ } \Phi _ { i + 1 , j } > B _ { 0 } \geq \Phi _ { i , j } , } \\ { \vdots } \\ { p _ { j } ^ { 1 * } , \mathrm { ~ i f ~ } \Phi _ { 2 , j } > B _ { 0 } \geq \Phi _ { 1 , j } , } \end{array} \right. } \end{array}\tag{45}
$$

where $p _ { j } ^ { i ^ { * } }$ is expressed by (46) shown at the bottom of the next page, and $\begin{array} { r } { \Phi _ { i , j } = \sum _ { l = 1 } ^ { i } { \frac { \widetilde { R _ { l } } } { \rho _ { l } \Lambda _ { l , j } } } \log { \frac { \lambda \rho _ { l } \Lambda _ { l , j } } { \varphi _ { i , j } \widetilde { R _ { l } } } } } \end{array}$

Proof: If $B _ { 0 } \geq \Phi _ { | T _ { j } | , j } .$ Ï, the optimal ${ p _ { j } } ^ { * }$ can be easily resolved 0 Î¦ ,jbased on Theorem 3. For $B _ { 0 }$ jwith other intervals, such as $\Phi _ { | \mathcal { T } _ { j } | , j } > B _ { 0 } \geq \Phi _ { | \mathcal { T } _ { j } | - 1 , j }$ 0, the proof of the optimal solution of Î¦ ,j 0 Î¦the corresponding ${ p _ { j } } ^ { * }$ ,jcan be derived in a similar manner to jTheorem 3. This completes our proof. -

Now, bandwidth allocation problem between UAVs and mobile users is completely addressed. The Stackelberg equilibrium is then obtained in the following theorem.

Theorem 5: The Stackelberg equilibrium for the bandwidth allocation between UAVs and mobile users, formulated in Problem 1 and 2 is $( \mathbf { b } _ { j } ^ { \ast } , p _ { j } ^ { \ast } )$ , where ${ b _ { i , j } } ^ { * }$ is an element of $\mathbf { b } _ { j } ^ { \ast }$ is (given by (31), and ${ p _ { j } } ^ { * }$ j ) i,jis given by (45).

jProof: When each UAV j broadcasts the bandwidth price $p _ { j } .$ jeach mobile user i within the coverage of UAV j responds with a bandwidth request ${ b _ { i , j } } ^ { * }$ which is given by (31). By Theorem 1, we know that ${ b _ { i , j } } ^ { * }$ i,jis the optimal strategy of each mobile user. As a result, for $\forall b _ { i , j } ^ { \prime } \geq 0$ , we have $\mathbb { U } _ { i } ( b _ { i , j } ^ { \mathrm { ~ * ~ } } ) \geq \mathbb { U } _ { i } ( b _ { i , j } ^ { \mathrm { ~ \prime ~ } } )$ . Also, with a certain $B _ { 0 } ,$ , the indicator function of each mobile user 0can be obtained and the utility of each UAV is concave with respect to $p _ { j }$ . Hereby, each UAV can achieve the optimal ${ p _ { j } } ^ { * }$ i.e., for $\forall p _ { j } ^ { \prime } \geq 0 , \mathbb { U } _ { j } ( { p _ { j } } ^ { * } ) \geq \mathbb { U } _ { j } ( { p _ { j } } ^ { \prime } )$ j. Therefore, according to jDefinition 1, $\mathbf { b } _ { j } ^ { \ast }$ j( j )formed by ${ b _ { i , j } } ^ { * }$ )in (31), and ${ p _ { j } } ^ { * }$ in (45) constitute the Stackelberg equilibrium. -

A Stackelberg game-based bandwidth allocation algorithm is devised as shown in Algorithm 2. In Algorithm 2, each UAV first initializes by determining its power constraints, initial position, and coverage radius. During each time slot, the UAVs employ (45) to set optimal prices ${ p _ { j } } ^ { * } ( t _ { n } )$ , evaluating j ( n)their utilities by (23) based on anticipated user requests. Each mobile user then computes a best-response bandwidth request ${ b _ { i , j } } ^ { * } ( t _ { n } ) \ ( \mathrm { i . e . , ~ } ( 3 1 ) )$ , aiming to maximize its own utility (i.e., i,j ( n)(26)). The algorithm verifies the resulting $( { p _ { j } } ^ { * } ( t _ { n } ) , { b _ { i , j } } ^ { * } ( t _ { n } ) )$ ( j ( n) i,j ( n))pairs to confirm the Stackelberg equilibrium and records these values. By iterating this process across multiple time slots, the system adapts prices and requests as network conditions evolve, ultimately ensuring incentive compatibility and efficient resource allocation in the network.

The proposed scheme scales with respect to both network size and resource availability. By electing a relatively small committee of witnesses to generate and verify blocks, the consensus overhead is kept low even as the total number of UAVs and mobile users grows. The majority of participants operate as lightweight or partial nodes, incurring minimal computational and storage overhead. Entities with limited resources only store recent block data. This design alleviates the memory burden on UAVs and mobile users, making the system more scalable without sacrificing security. Besides, the Stackelberg game formulation yields low-complexity solutions. Each UAV optimizes its bandwidth price, and each mobile user computes its best response. These computations scale linearly in the number of mobile users within a UAVâs coverage, avoiding exponential complexity. Because each UAV independently performs pricing and allocation for its covered users, the system naturally supports parallel execution across multiple UAVs, further enhancing scalability.

## VI. PERFORMANCE EVALUATION

In this section, we carry out extensive simulations to validate the effectiveness of the proposed scheme. We begin by describing the simulation setup and then proceed to analyze the results in detail.

## A. Simulation Setup

In the simulation, a 1000 m Ã 1000 m coverage area is defined, which contains one GBS and three UAVs, with the numbers of mobile users in each UAVs coverage set to 10, 12, and 15, respectively, to reflect varying user densities. We discretize the time horizon into 1000 time slots of 1 s each, allow a maximum UAV velocity of 20 m/s, and adopt an air-to-ground channel model with LoS path loss $( \beta _ { 0 } = 1$ , path loss exponent $\mu = 0 . 5 )$ [30]. 0 = 1 = 0 5UAVs share the GBS spectrum under an interference constraint $( F _ { j , 0 } \leq Q _ { j } )$ where $Q _ { j }$ is set to 1000 mW, and the GBS trans-( j,0 j) jmission power is 25 mW [33]. Mobile usersâ transmission rate demands follow a uniform distribution U ,  Mbps to repre-[1 15]sent different application requirements, with the demand degree $\rho _ { i }$ drawn from U . , . . We also incorporate a reputationi [0 1 1 5]based DPoS consensus with a witness committee of 3 [34], and transaction generation includes bandwidth-allocation transactions and malicious-behavior-recording transactions. Additionally, according to [34], [35], Table II summarizes key simulation parametersâsuch as UAV altitude, velocity constraints, and T âto support a clearer understanding of simulations, and we run all experiments on standard desktop hardware with Matlab implementations.

To evaluate the performance of the proposed scheme, we introduce the two following conventional schemes:

- Max-min scheme [34]: In this scheme, UAVs use a linear pricing method to determine the bandwidth price. This

$$
\begin{array} { r } { p _ { j } \ast = \{ \begin{array} { l l } { \exp ( { - \frac { \sum _ { i = 1 } ^ { I _ { j } } \frac { \widetilde { R } _ { i } } { R _ { i } \Delta _ { j } } } { \widetilde { R } _ { i \Delta _ { i , j } } } \log \frac { \widetilde { R } _ { i } } { \widetilde { R } _ { i } } - \sum _ { i = 1 } ^ { I } h _ { i , j } \frac { \widetilde { R } _ { i } } { p _ { i \Delta _ { i , j } } } } { \sum _ { i = 1 } ^ { I } h _ { i , j } \frac { \widetilde { R } _ { i } } { p _ { i \Delta _ { i , j } } } } } ) , } & { \mathrm { i f ~ } B _ { 0 } \ge \sum _ { i = 1 } ^ { I } h _ { i , j } \frac { \widetilde { R } _ { i } } { p _ { i \Delta _ { i , j } } } \ge \sum _ { i = 1 } ^ { I } h _ { i , j } \frac { \widetilde { R } _ { i } } { p _ { i \Delta _ { i , j } } } \log \frac { \lambda _ { j } \rho _ { \Delta _ { i , j } } } { \operatorname* { m i n } \{ \frac { \widetilde { R } _ { j } \delta _ { \Delta _ { i , j } } } { R _ { i , j } } \} _ { u _ { i , j } \ge u _ { j } } \widetilde { R } _ { i } } , } \\ { \qquad \sum _ { i = 1 } ^ { I } h _ { i , j } \frac { \widetilde { R } _ { i } } { p _ { i \Delta _ { i , j } } } } &  \mathrm { i f ~ } B _ { 0 } \ge \sum _ { i = 1 } ^ { I } \frac { \widetilde { R } _ { i } } { p _ { i \Delta _ { i , j } } } \log \frac { \lambda _ { j } \rho _ { \Delta _ { i , j } } } { \operatorname* { m i n } \{ \frac { \widetilde { R } _ { j } \delta _ { \Delta _ { i , j } } } { R _ { i , j } } \} _ { u _ { i , j } \ge \widetilde { R } _ { i } } } \ge \sum _ { i = 1 } ^ { I } \frac { \widetilde { R } _ { i } }  p _ { i \Delta _ { i , j } } \end{array} \end{array}\tag{43}
$$

$$
\begin{array} { r }  p _ { j } ^ { i ^ { * } } = \{ \begin{array} { l l } { \exp ( \frac { - \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } } { \widetilde { \rho } L _ { l , j } } \log \frac { \widetilde { R } _ { l } } { \widetilde { R } _ { l } L _ { l , j } } - \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } } { \rho L _ { l } L _ { l , j } } } { \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } } { \rho L _ { l } } } ) , } & { \mathrm { i f ~ } B _ { 0 } \geq \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } } { \rho _ { l } \Delta _ { l , j } } \geq \sum _ { l = 1 } ^ { l } \frac { \widetilde { R } _ { l } } { \rho _ { l } \Delta _ { l , j } } \log \frac { \lambda \rho _ { l } \Delta _ { l , j } } { \varphi _ { i , j } \widetilde { R } _ { l } } , } \\ { \qquad \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } } { \rho _ { l } \Delta _ { l , j } } } & { \mathrm { i f ~ } B _ { 0 } > \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } } { \rho _ { l } \Delta _ { l , j } } \log \frac { \lambda \rho _ { l } \Delta _ { l , j } } { \varphi _ { i , j } \widetilde { R } _ { l } } > \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } } { \rho _ { l } \Delta _ { l , j } } , } \\ { \exp ( \frac { - \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } } { \rho L _ { l , j } } \log \frac { \widetilde { R } _ { l } } { \widetilde { R } _ { l } \Delta _ { l , j } } - B _ { 0 } } { \widetilde { R } _ { l } \widetilde { R } _ { l } } ) , } &  \mathrm { i f ~ } \sum _ { l = 1 } ^ { i } \frac { \widetilde { R } _ { l } }  \rho  \end{array} \end{array}\tag{46}
$$

TABLE II SIMULATION PARAMETERS
<table><tr><td>Parameter</td><td>Value</td><td>Parameter</td><td>Value</td></tr><tr><td>J</td><td>3</td><td>T</td><td>1 s</td></tr><tr><td> $a _ { j }$ </td><td>100</td><td> $P _ { 0 }$ </td><td>25 mW</td></tr><tr><td> $V _ { i } ^ { m a x }$ </td><td>20 m/s</td><td> $\Re _ { j } ^ { A 2 G }$ </td><td>250 m</td></tr><tr><td> $\beta _ { 0 }$ </td><td>1</td><td> $g _ { j , 0 }$ </td><td>0.1</td></tr><tr><td> $\sigma _ { 0 } ^ { 2 }$ </td><td>0.0001mW</td><td> $Q _ { j }$ </td><td>1000 mW</td></tr><tr><td> $T$ </td><td>1000 s</td><td> $\lambda$ </td><td>5</td></tr><tr><td> $g _ { i } ^ { G B S }$ </td><td>0.001</td><td> $\Re ^ { G B S }$ </td><td>500 m</td></tr></table>

Algorithm 2: Stackelberg Game-Based Bandwidth Alloca  
tion Algorithm.   
1: Input: Set of UAVs J , set of mobile users $\mathcal { T } ,$ the   
number of time slots $N ,$ , channel parameters $( \mathrm { i . e . }$ ,   
$\beta _ { 0 } , \mu , \sigma ^ { 2 } )$ , interference constraints $Q _ { j }$ for each $\mathrm { U A V } ~ j _ { \mathrm { \Omega } }$   
0user demands $\tilde { R } _ { i }$ jand demand degrees $\rho _ { i }$   
2: iOutput: Optimal bandwidth price $p _ { j } ^ { \ast } , j \in \mathcal { I }$ , optimal   
bandwidth request from user $i \in \mathcal { T }$ jto UAV $j \in \mathcal I$ , i.e.,   
${ b _ { i , j } } ^ { * }$   
3: i,jInitialization:   
4: for UAV $j \in \mathcal { I }$ do   
5: Determine maximum transmit power $P _ { j }$ (subject to   
$Q _ { j } ) ;$   
6: j Initialize UAV coverage radius, $\Re _ { j } ^ { U A V } \}$   
7: end for   
8: Repeat:   
9: for $\overline { { t _ { n } \in } } \left\{ t _ { 1 } , \ldots , t _ { n } , \ldots , t _ { N } \right\}$ do   
10: n 1 nLeader Stage (UAVs):   
11: for $\overline { { \mathrm { U A V } ~ j \in \mathcal { I } } }$ do   
12: Obtain optimal bandwidth $( p _ { j } ) ^ { * } ( t _ { n } )$ by (45);   
13: ( j ) ( n) Calculate the utility of UAV j by (23);   
14: end for   
15: Follower Stage (Mobile Users):   
16: for Mobile user $\overline { { i \in { \mathcal { I } } } }$ do   
17: Obtain the best response $( b _ { i , j } ) ^ { * } ( t _ { n } )$ via (31).   
18: ( i,j ) ( n) Calculate the utility of mobile user i by (26).   
19: end for   
20: Stackelberg Equilibrium and Updating:   
21: Verify Stackelberg equilibrium $\overline { { ( { p _ { j } } ^ { * } ( t _ { n } ) , { b _ { i , j } } ^ { * } ( t _ { n } ) ) } }$ ;   
22: Record and output the results ${ p _ { j } } ^ { * } , b _ { i , j } { ^ { * } } , \forall i \in \mathcal { T }$ n))and   
$\forall j \in \mathcal { I }$ at each time slot;   
23: end for

means that the bandwidth price is directly proportional to the bandwidth requests and inversely proportional to $B _ { 0 }$ 0Additionally, the fair max-min algorithm is employed to allocate the bandwidth of each UAV, taking into account the transmission rate demands of mobile users.

Random scheme $I ^ { g } { \cal { I } } ;$ In this scheme, the bandwidth price of each UAV is randomly set in order to maximize benefits. Mobile users also randomly request bandwidth from UAVs, without consideration for their transmission rate demands.

- Auction-based scheme [36]: In this scheme, each mobile user within a UAVâs coverage submits a bid based on its individual demand. The UAV then allocates the available bandwidth proportionally to each userâs bid relative to the total bid sum. Each user pays an amount equal to its bid multiplied by its allocated bandwidth.

<!-- image-->  
Fig. 2. The optimal bandwidth price of the UAV versus $B _ { 0 } .$

## B. Simulation Results

Fig. 2 shows the optimal bandwidth price of the UAV versus the available bandwidth $B _ { 0 }$ , where $B _ { 0 }$ changes from 1MHz 0 0to 15MHz. Here, we select three demand degrees to show the results, which are 0.5, 1, 1.5, respectively. Four mobile users are set to request bandwidth. In Fig. 2, the optimal bandwidth price decreases with an increase in available bandwidth. This is because the UAV with small $B _ { 0 }$ selects a large bandwidth 0price to regulate the number of mobile users permitted to access the network. For example, when $B _ { 0 } = 1$ and $\rho = 0 . 5 ,$ only one 0 = 1 = 0 5mobile user is able to access the network. In addition, for the same $B _ { 0 } ,$ bandwidth price $p _ { j }$ is generally higher under a large 0 jdemand degree compared to a lower one. This can be explained as follows. For the large $\rho _ { i } .$ , even though the acquired bandwidth iis small, mobile users can also have a high satisfaction. As such, UAV should increase the bandwidth price to enlarge its utility. On the other hand, from (45), the optimal bandwidth price is in proportion to the rho , i.e., the bandwidth price rises with the increase of $\rho _ { i }$

iIn Fig. 3, the obtained transmission rate of each mobile user is shown versus the available bandwidth $B _ { 0 }$ , where $B _ { 0 }$ ranges from 0 01MHz to 15MHz. Four mobile users are used to demonstrate the results, with transmission rate demands of 4, 6, 10, and 15Mbps, respectively. In Fig. 3(a), the bandwidth request of each mobile user generally increases with $B _ { 0 }$ . This is because a UAV with a large $B _ { 0 }$ 0offers a low bandwidth price, allowing each mobile user to request a large bandwidth. Additionally, when $B _ { 0 }$ is small, only mobile users with small transmission rate demands can obtain bandwidth. For example, when $B _ { 0 } = 1$ MHz, only 0 = 1mobile users 1 and 2 have positive bandwidth requests. Furthermore, mobile users with large transmission rate demands also exhibit high rates of increase in bandwidth requests. This is because satisfaction is difficult to achieve when the transmission rate demand is large, requiring mobile users to obtain a large bandwidth to improve their satisfaction. Fig. 3(b) shows similar results to Fig. 3(a). However, for each mobile user, the rate of increase in obtained transmission rate is larger in Fig. 3(b) than that of the optimal bandwidth request in Fig. 3(a). When $B _ { 0 }$ is large, interference limitations cause the transmission power to be small, resulting in a low transmission rate.

<!-- image-->  
(a) The optimal bandwidth request of each mobile user vs. $B _ { 0 }$

<!-- image-->  
(b) The obtained transmission rate of each mobile user vs. $B _ { 0 }$  
Fig. 3. The optimal bandwidth strategy of each mobile user versus $B _ { 0 }$

Fig. 4. The optimal bandwidth request of mobile users versus Ïi.

Fig. 4 shows the optimal bandwidth request of each mobile user versus the mobile userâs transmission rate demand degree $\rho ,$ where Ï changes from 0.1 to 1.5. Other settings are unchanged. It can be observed that for each mobile user, the optimal bandwidth request first increases and then decreases with the increase of the transmission rate demand degree. When the transmission rate demand degree is low, mobile users have to request a large bandwidth to improve their satisfaction. Conversely, when the transmission rate demand degree is high, even with a small bandwidth request, the mobile user can still obtain high satisfaction. Additionally, a mobile user with a high transmission rate demand also needs a large transmission rate demand degree to require positive bandwidth requests. For example, for mobile user 4 whose desired transmission rate is 15Mbps, only when the bandwidth request degree is larger than 1, his/her optimal bandwidth request is positive. This is because when the transmission rate demand is large, if the bandwidth degree is small, the bandwidth price threshold is low, and his/her optimal bandwidth request is zero.

<!-- image-->

<!-- image-->  
Fig. 5. The comparison of the proposal with conventional schemes on the utility of the UAV.

Fig. 5 shows the performance comparison of the proposed scheme in terms of UAV utility, where five mobile users request bandwidth with transmission rate demands of 0.5, 1, 2, 4, and 8.5 Mbps, respectively. For the same $B _ { 0 }$ , our proposed scheme 0yields a higher UAV utility compared to conventional schemes. In the random scheme, UAVs rarely achieve maximum utility because the bandwidth price is determined randomly, leading to suboptimal outcomes. In the max-min scheme, although bandwidth is allocated based on the usersâ transmission rate demands, a linear pricing method is used, which results in a non-ideal pricing strategy that prevents UAVs from reaching their maximum potential utility. Additionally, the auction-based scheme relies on fixed bidding strategies that do not adapt to the dynamic network environment, leading to a non-optimal utility for the UAV. In contrast, our proposed approach employs game theory to establish the bandwidth pricing, ensuring an optimal outcome and enabling UAVs to maximize their utilities.

<!-- image-->  
Fig. 6. The comparison of the proposal with conventional schemes on the average utility of mobile users.

Fig. 6 shows the performance comparison of the proposed scheme on the average utility of mobile users, which is computed by averaging the utility of each mobile user that requests bandwidth. Here, the available bandwidth $B _ { 0 }$ ranges from 6 MHz to 10 MHz. In Fig. 6, for the same $B _ { 0 } ,$ , our proposed scheme yields the highest average utility compared to the other schemes. In the random scheme, bandwidth is assigned arbitrarily, which often prevents users from obtaining the optimal allocation they need. In the max-min scheme, although bandwidth is allocated based on the users transmission rate demands, the use of a linear pricing method results in a suboptimal pricing strategy that limits user utility. Furthermore, in the auction-based scheme, since the allocated bandwidth is directly based on bids, when the available bandwidth increases, users quickly reach their demand limits, causing their satisfaction and utility to saturate. In contrast, our proposed approach leverages a Stackelberg game model that carefully balances the conflicting interests between UAVs and mobile users, leading to an optimal bandwidth pricing and allocation strategy that maximizes user utility.

## VII. CONCLUSION

In this paper, we have proposed a blockchain-empowered game theoretical incentive scheme in UAWNs to securely allocate bandwidth between UAVs and mobile users. Specifically, we have first developed a blockchain-based secure bandwidth allocation framework to address three critical security problems:

security threats from malicious mobile users, malicious UAVs, and malicious behavior tampering. To enforce the honest behaviors of both mobile users and UAVs, a smart contract has been designed to automatically execute the bandwidth transactions. To efficiently incentivize the cooperation of UAVs, we have then employed the Stackelberg game model to formulate the bandwidth allocation between UAVs and mobile users, where the optimal bandwidth prices of UAVs and the optimal bandwidth requests of mobile users are obtained to maximize their utilities through backward inducting method. Performance evaluation have been carried out to demonstrate that the proposed scheme provides higher utilities for both mobile users and UAVs compared to conventional schemes. For the future work, we will focus on the defending against collusion attacks during the joint allocation of heterogeneous resources including power, bandwidth and computing.

## REFERENCES

[1] V. D. Tuong, W. Noh, and S. Cho, âSparse CNN and deep reinforcement learning-based D2D scheduling in UAV-assisted industrial IoT networks,â IEEE Trans. Ind. Informat., vol. 20, no. 1, pp. 213â223, Jan. 2024.

[2] R. Ma, J. Cao, S. He, Y. Zhang, B. Niu, and H. Li, âA UAV-assisted UE access authentication scheme for 5G/6G network,â IEEE Trans. Netw. Service Manag., vol. 21, no. 2, pp. 2426â2444, Apr. 2024.

[3] Y. Wang and J. Farooq, âDeep-reinforcement-learning-based placement for integrated access backhauling in UAV-assisted wireless networks,â IEEE Internet Things J., vol. 11, no. 8, pp. 14727â14738, Apr. 2024.

[4] X. Liu, M. Chen, Y. Liu, Y. Chen, S. Cui, and L. Hanzo, âArtificial intelligence aided next-generation networks relying on UAVs,â IEEE Wireless Commun., vol. 28, no. 1, pp. 120â127, Feb. 2021.

[5] P. Luong, F. Gagnon, L.-N. Tran, and F. Labeau, âDeep reinforcement learning based resource allocation in cooperative UAV-assisted wireless networks,â IEEE Trans. Wireless Commun., vol. 20, no. 11, pp. 7610â7625, Nov. 2021.

[6] B. Fan, Y. Dong, T. Li, and Y. Wu, âBlockchain-FRL for vehicular lanechanging: Towards traffic, data and training safety,â IEEE Internet Things J., vol. 10, no. 24, pp. 22153â22164, Dec. 2023.

[7] H. Zeng, Z. Su, Q. Xu, and R. Li, âSecurity and privacy in space-air-ocean integrated unmanned surface vehicle networks,â IEEE Netw., vol. 38, no. 3, pp. 48â56, May 2024.

[8] N. Chukhno et al., âModels, methods, and solutions for multicasting in 5G/6G mmWave and Sub-THz systems,â IEEE Commun. Surveys Tuts., vol. 26, no. 1, pp. 119â159, First Quarter 2024.

[9] Q. Xu, Z. Su, D. Fang, and Y. Wu, âBASIC: Distributed task assignment with auction incentive in UAV-enabled crowdsensing system,â IEEE Trans. Veh. Technol., vol. 73, no. 2, pp. 2416â2430, Feb. 2024.

[10] Y. Wu, G. Ji, T. Wang, L. Qian, B. Lin, and X. Shen, âNon-orthogonal multiple access assisted secure computation offloading via cooperative jamming,â IEEE Trans. Veh. Technol., vol. 71, no. 7, pp. 7751â7768, Jul. 2022.

[11] H. Zhang, H. Xing, J. Cheng, A. Nallanathan, and V. C. M. Leung, âSecure resource allocation for OFDMA two-way relay wireless sensor networks without and with cooperative jamming,â IEEE Trans. Ind. Informat., vol. 12, no. 5, pp. 1714â1725, Oct. 2016.

[12] R. Li, Z. Wei, L. Yang, D. W. K. Ng, J. Yuan, and J. An, âResource allocation for secure multi-UAV communication systems with multieavesdropper,â IEEE Trans. Commun., vol. 68, no. 7, pp. 4490â4506, Jul. 2020.

[13] K. Gu, L. Tang, J. Jiang, and W. Jia, âResource allocation scheme for community-based fog computing based on reputation mechanism,â IEEE Trans. Computat. Social Syst., vol. 7, no. 5, pp. 1246â1263, Oct. 2020.

[14] A. Abdelhadi, H. Shajaiah, and C. Clancy, âA multitier wireless spectrum sharing system leveraging secure spectrum auctions,â IEEE Trans. Cogn. Commun. Netw., vol. 1, no. 2, pp. 217â229, Jun. 2015.

[15] F. Zeng et al., âResource allocation and trajectory optimization for QoE provisioning in energy-efficient UAV-enabled wireless networks,â IEEE Trans. Veh. Technol., vol. 69, no. 7, pp. 7634â7647, Jul. 2020.

[16] H. T. Nguyen, H. D. Tuan, T. Q. Duong, H. V. Poor, and W.-J. Hwang, âJoint D2D assignment, bandwidth and power allocation in cognitive UAV-enabled networks,â IEEE Trans. Cogn. Commun. Netw., vol. 6, no. 3, pp. 1084â1095, Sep. 2020.

[17] S. Yan, M. Peng, and X. Cao, âA game theory approach for joint access selection and resource allocation in UAV assisted IoT communication networks,â IEEE Internet Things J., vol. 6, no. 2, pp. 1663â1674, Apr. 2019.

[18] Y. Chen, H. Zhang, and Y. Hu, âOptimal power and bandwidth allocation for multiuser video streaming in UAV relay networks,â IEEE Trans. Veh. Technol., vol. 69, no. 6, pp. 6644â6655, Jun. 2020.

[19] Q. Hu, Y. Cai, A. Liu, G. Yu, and G. Y. Li, âLow-complexity joint resource allocation and trajectory design for UAV-aided relay networks with the segmented ray-tracing channel model,â IEEE Trans. Wireless Commun., vol. 19, no. 9, pp. 6179â6195, Sep. 2020.

[20] Y. Zhu, F. Yan, S. Zhao, F. Shen, S. Xing, and L. Shen, âIncentive mechanism for cooperative localization in wireless networks,â IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 15920â15932, Dec. 2020.

[21] J. Nie, J. Luo, Z. Xiong, D. Niyato, P. Wang, and H. V. Poor, âA multileader multi-follower game-based analysis for incentive mechanisms in socially-aware mobile crowdsensing,â IEEE Trans. Wireless Commun., vol. 20, no. 3, pp. 1457â1471, Mar. 2021.

[22] T. H. Thi Le et al., âAn incentive mechanism for federated learning in wireless cellular networks: An auction approach,â IEEE Trans. Wireless Commun., vol. 20, no. 8, pp. 4874â4887, Aug. 2021.

[23] Y. Jiao, P. Wang, D. Niyato, B. Lin, and D. I. Kim, âMechanism design for wireless powered spatial crowdsourcing networks,â IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 920â934, Jan. 2020.

[24] M. Chen, H. Wang, D. Han, and X. Chu, âSignaling-based incentive mechanism for D2D computation offloading,â IEEE Internet Things J., vol. 9, no. 6, pp. 4639â4649, Mar. 2022.

[25] M. Xu, C. Liu, Y. Zou, F. Zhao, J. Yu, and X. Cheng, âwChain: A fast fault-tolerant blockchain protocol for multihop wireless networks,â IEEE Trans. Wireless Commun., vol. 20, no. 10, pp. 6915â6926, Oct. 2021.

[26] M. Jiang, Y. Li, Q. Zhang, G. Zhang, and J. Qin, âDecentralized blockchain-based dynamic spectrum acquisition for wireless downlink communications,â IEEE Trans. Signal Process., vol. 69, pp. 986â997, 2021.

[27] Y. Lu, X. Huang, K. Zhang, S. Maharjan, and Y. Zhang, âLow-latency federated learning and blockchain for edge association in digital twin empowered 6G networks,â IEEE Trans. Ind. Informat., vol. 17, no. 7, pp. 5098â5107, Jul. 2021.

[28] F. Guo, F. R. Yu, H. Zhang, H. Ji, M. Liu, and V. C. M. Leung, âAdaptive resource allocation in future wireless networks with blockchain and mobile edge computing,â IEEE Trans. Wireless Commun., vol. 19, no. 3, pp. 1689â 1703, Mar. 2020.

[29] V. S, R. Manoharn, S. Ramachandran, and V. R. Rajasekar, âBlockchain based privacy preserving framework for emerging 6G wireless communications,â IEEE Trans. Ind. Informat., vol. 18, no. 7, pp. 4868â4874, Jul. 2022.

[30] F. Zhou, Y. Wu, R. Q. Hu, and Y. Qian, âComputation rate maximization in UAV-enabled wireless-powered mobile-edge computing systems,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1927â1941, Sep. 2018.

[31] Q. Wu, J. Xu, and R. Zhang, âCapacity characterization of UAV-enabled two-user broadcast channel,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1955â1971, Sep. 2018.

[32] S. Tikhomirov, E. Voskresenskaya, I. Ivanitskiy, R. Takhaviev, E. Marchenko, and Y. Alexandrov, âSmartCheck: Static analysis of ethereum smart contracts,â in Proc. 1st Int. Workshop Emerg. Trends Softw. Eng. Blockchain, 2018, pp. 9â16.

[33] P. Li, L. Xie, J. Yao, and J. Xu, âCellular-connected UAV with adaptive air-to-ground interference cancellation and trajectory optimization,â IEEE Commun. Lett., vol. 26, no. 6, pp. 1368â1372, Jun. 2022.

[34] Z. Su, Y. Wang, Q. Xu, and N. Zhang, âLVBS: Lightweight vehicular blockchain for secure data sharing in disaster rescue,â IEEE Trans. Dependable Secure Comput., vol. 19, no. 1, pp. 19â32, Jan./Feb. 2022.

[35] X. Kang, R. Zhang, and M. Motani, âPrice-based resource allocation for spectrum-sharing femtocell networks: A stackelberg game approach,â IEEE J. Sel. Areas Commun., vol. 30, no. 3, pp. 538â549, Apr. 2012.

[36] J. Wang, B. Zhang, B. Zhao, G. Ding, and D. Guo, âA gametheoretical learning approach for spectrum trading in cognitive satelliteterrestrial networks,â IEEE Commun. Lett., vol. 25, no. 9, pp. 3065â3069, Sep. 2021.

<!-- image-->

Qichao Xu is currently an associate professor with Shanghai University, Shanghai. He has published more than 50 papers in some respected journals, such as IEEE Transactions on Information Forensics and Security, IEEE Transactions on Dependable and Secure Computing, IEEE Transactions on Wireless Communications, IEEE Transactions on Industrial Informatics, and IEEE Transactions on Vehicular Technology. His research interests are in trust and security, the general area of wireless network architecture, Internet of Things, vehicular networks, and

resource allocation. He was receipt of the best paper awards from several international conferences including IEEE AIoT2024, IEEE IWCMC2022, IEEE MSN2020, IEEE Comsoc GCCTC2018, and IEEE CyberSciTech 2017.

<!-- image-->

Zhou Su is a professor with Xiâan Jiaotong University and his research interests include multimedia communication, wireless communication, network security and network traffic. He has published technical papers, including top journals and top conferences including IEEE Journal on Selected Areas in Communications, IEEE/ACM Transactions on Networking, IEEE Transactions on Wireless Communications, IEEE INFOCOM, etc. He received the best paper Award of International Conference IEEE AIoT2024, IEEE WCNC2023, IEEE VTC-Fall2023,

IEEE ICC2020, etc. He is an associate editor of IEEE Internet of Things Journal, IEEE Open Journal of Computer Society. He is the chair of IEEE VTS Xiâan Chapter Section.

<!-- image-->

Haixia Peng received the PhD degrees in computer science and electrical and computer engineering from Northeastern University, China, and University of Waterloo, Canada, in 2017 and 2021, respectively. She is currently a professor with the School of Cyber Science and Engineering, Xiâan Jiaotong University, Xiâan, China. Her current research focuses on Internet of vehicles, resource management, multi-access edge computing, and reinforcement learning. She has authored or co-authored more than 30 technical papers dealing with network issues. She serves/served as a reviewer for IEEE Journals on Selected Areas in Communications (JSAC), IEEE Transactions on Communications, IEEE Transactions on Vehicular Technologies, etc. more than 20 prestigious journals, and as a TPC member in IEEE ICC, Globecom, VTC, etc. conferences.

<!-- image-->

Yuan Wu received the PhD degree in electronic and computer engineering from the Hong Kong University of Science and Technology, in 2010. He is currently an associate professor with the State Key Laboratory of Internet of Things for Smart City, University of Macau, Macao, China, and also with the Department of Computer and Information Science, University of Macau. His research interests include resource management for wireless networks, green communications and computing, and edge computing and edge intelligence. He received the Best Pa-

per Award from the IEEE ICC2016, IEEE TCGCC2017, IWCMC2021, and WCNC2023. He is currently on the editorial board of IEEE Transactions on Vehicular Technology, IEEE Transactions on Network Science and Engineering, and IEEE Internet of Things Journal.

<!-- image-->

Ruidong Li (Senior Member, IEEE) received the PhD degree in electronic and computer engineering from the Hong Kong University of Science and Technology, Hong Kong, in 2010. He is currently an associate professor with the State Key Laboratory of Internet of Things for Smart City, University of Macau, Macau SAR, China, and also with the Department of Computer and Information Science, University of Macau. His research interests include mobile edge computing and edge intelligence, and integrated sensing and communications. He was the recipient of the Best

Paper Award from the IEEE ICC2016, IEEE TCGCC2017, IWCMC2021, and IEEE WCNC2023. He is on the editorial board of IEEE Transactions on Wireless Communications, IEEE Transactions on Vehicular Technology, and IEEE Transactions on Network Science and Engineering. He is the distinguished lecturer of IEEE Vehicular Technology Society (2025â2027).

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks/page_3_img_1.png|page_3_img_1]]
2. [[../extracted_images/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks/page_4_img_1.png|page_4_img_1]]
3. [[../extracted_images/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks/page_15_img_1.jpeg|page_15_img_1]]
4. [[../extracted_images/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks/page_15_img_2.jpeg|page_15_img_2]]
5. [[../extracted_images/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks/page_15_img_3.jpeg|page_15_img_3]]
6. [[../extracted_images/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks/page_15_img_4.jpeg|page_15_img_4]]
7. [[../extracted_images/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks/page_15_img_5.jpeg|page_15_img_5]]

---

