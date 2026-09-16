# A Blockchain-Based Distributed and Intelligent Clustering-Enabled Authentication Protocol for UAV Swarms

Raja Karmakar , Member, IEEE, Georges Kaddoum , Senior Member, IEEE, and Ouassima Akhrif , Senior Member, IEEE

AbstractâUnmanned aerial vehicles (UAVs) are operated remotely without the presence of a unified system of identity authentication, and wireless communications in untrusted environments can cause the loss of valuable data carried by UAVs. Traditional UAV authentication mechanisms are centralized approaches, which suffer from a single point of failure problem and may incur high complexity computations. Therefore, it is crucial to establish a distributed authentication mechanism between the ground station controller (GSC) and a UAV. Moreover, in case of UAV swarms, the high mobility of the UAVs affects the stability of UAV communications, which leads to the degradation of the UAV authentication performance. Addressing these challenges, we design a blockchain-based distributed authentication mechanism, known as SwarmAuth, for UAV swarms, where the GSC and UAVs follow a mutual authentication approach using physical unclonable functions (PUFs), and the K-means clustering-based intelligent approach is used to dynamically create location-based clusters. The blockchain helps store UAVsâ authentication information in an immutable storage and the associated smart contracts provide a convenient access control model. The security analysis of SwarmAuth is carried out through both formal and informal proofs considering general attacks. Experimental evaluation shows that SwarmAuth can assure trustworthy communications and improve the network performance.

Index TermsâUAV swarms, blockchain, mutual authentication, physical unclonable functions, K-means clustering.

## I. INTRODUCTION

U NMANNED aerial vehicle (UAV) technology is recog-nized as one of the promising aircraft technologies in recent years, with their various capabilities, such as sensing, processing, and delivery of information. Due to their deployment flexibility, high-mobility, ability to hover, and low maintenance cost, UAVs can be used in limited access and reachability location-based applications, such as search and rescue, smart agriculture, remote sensing, surveillance, package delivery, and extending wireless network coverage [1]. To this end, swarms of UAVs are designed with advanced sensors in order to facilitate the aforementioned operations with higher levels of accuracy and automation [2]. In UAV swarms, the ground station controller (GSC) communicates with a group of UAVs belonging to a UAV cluster, which changes with the position of the UAVs. Specifically, the GSC communicates with the cluster head (CH), which is responsible for data gathering and transfer between two clusters, and the CH also transmits data between a cluster and the GSC. In a cluster, apart from the CH, the UAVs are known as cluster members (CMs). Fig. 1 shows an example of UAV swarm consisting of three UAV clusters which provide services to three different regions.

<!-- image-->  
Fig. 1. Illustration of UAV swarm.

Although UAV technologies and applications have been going through rapid development, there are several challenges that hinder their large scale deployment [3]. For instance, in case of UAV-enabled mobile edge computing (MEC)-based services, if UAVs are brought closer to the end users, the consumers will get better services, leading to quality of service (QoS) improvement of UAV applications. However, such deployment results in increased vulnerabilities and high threats that can disrupt the UAV communication. In fact, the messages communicated over wireless channels can be seized by malicious entities, which makes them prone to various attacks, such as man-in-the-middle, node tampering, and replay attacks. Attackers may exploit UAV devices to acquire sensitive information, corrupt the data, cause malicious interference, and distort normal UAV functionalities [4]. Such attacks can drastically affect the output of an operation, which can occur in non-commercial and commercial sectors. For instance, terrorists can use UAVs for malicious purposes, such as impersonating a malicious UAV as a legitimate one. If the legitimate UAV acts as an access point, the attackers gain the access of the access point. Consequently, the malicious UAV injects malware into connected devices through the redirection and interception of usersâ data traffic or through phishing. As a result, terrorists can acquire and corrupt sensitive data, such as passwords, and distort the functionalities of legitimate UAVs.

Moreover, in the context of UAV swarms, a large number of UAV communications needs to be handled, which also increases the number of security threats.

One of the primary security demands for UAV deployments is designing proper authentication mechanisms which can ensure the participation of only legitimate devices in the data communication [5]. Before initiating a secure and trusted communication session, the first security aspect that needs to be fulfilled is node authentication. In UAV communications, due to highly dynamic nature of the UAVs, the devices are required to be authenticated frequently to ensure that UAVsâ normal operations are not affected and the UAV application related information and resources cannot be accessed by a malicious adversary [6]. Moreover, due to the open air deployment of UAVs, they are prone to node capturing attacks, which expose secret keys. Thus, secret information can be obtained by the adversary from the GSC and legitimate UAVs. In addition, since UAVs have limited computation capabilities and memory constraints, it is a challenge to properly execute cryptography algorithms and store the secret keys [7]. Finally, in UAV swarms, the different UAVs should follow the same authentication mechanism, such that they can avoid communication interoperability issues between UAVs of different clusters. Otherwise, the challenges of ensuring authentication security will be compounded during message integration [8].

Considering the aforementioned security issues in UAV communications, a lightweight and scalable UAV authentication mechanism that can achieve a mutual authentication between a UAV and the GSC in a UAV swarm is needed. To resist node capturing attacks, physical unclonable functions (PUFs), which support unique and unclonable identities to devices, are very promising [9]. PUFs use a challenge-response pair, which is unique for every devices, i.e., two different devices with the same manufacturing configuration are expected to provide different responses for the same challenge. The PUF is defined as

$$
R = P U F ( C ) ,\tag{1}
$$

where C and R are binary strings denoting the challenge and response, respectively. Moreover, in order to support the authentication services in a distributed way, blockchain can be exploited. The blockchain is a distributed, immutable, and shared ledger that can enable different devices to approve transactions without involving a central authority [10]. Due to the traceability and unalterable properties of the blockchain, it is resistant to several attacks [11]. Since, the dimension and mobility of a UAV swarm vary frequently, blockchain can be used to securely store authentication related information in a distributed way for a large number of UAVs, and thus blockchain can help increase the scalability of an authentication approach and make it lightweight to be deployed at resource-constrained UAVs.

## A. Related Works and Motivation

1) Non-Blockchain-Based UAV Authentication: In [12], a PUF-based authentication protocol is presented for secure communications between base stations and UAVs in UAV swarms, where the K-Means clustering is used to form clusters of UAVs based on their locations. Using PUFs, the work in [6] also designs an authentication mechanism for UAV swarms, which supports spanning tree-based traversal for multi-hop communications. To leverage secure PUFs and programmable high-speed packet-processing data planes, a UAV authentication system is developed in [13]. Wang et al. [14] specifically design a CH safeguarding mechanism for UAV swarms, which utilizes edge intelligence and a situation-aware authentication approach. However, UAV authentication is not addressed in that work. The authors in [15] design UAV-GSC and UAV-UAV authentication schemes using PUFs. The work in [16] addresses secure UAV-UAV communications enabling message integrity, confidentiality, and authenticity. Addressing the tradeoff between lightweight features and security, in [17], a key agreement technique is proposed for internet of drones (IoD). In [18], a decentralized UAV authentication mechanism is designed to overcome the single-point failure in a cluster, caused by the wrong estimations. Furthermore, to reduce the computational cost of the authentication approach and further improve the authentication accuracy of the scheme, a situational-aware authentication mechanism is designed at each UAV. However, the work in [18] does not consider PUFs, blockchain, mutual authentication, and dynamic cluster formation in UAV swarms.

In the case of a non-blockchain-based UAV authentication, no distributed platform is available to store UAV registration and authentication related data such that the data can be shared in a tamper-proof way and can be traceable by the GSC and multiple UAVs, which are authorized to access the data. Moreover, in a non-blockchain-based approach, since authentication related data cannot be securely shared among the GSC and UAVs using a distributed architecture, the number of message transmissions between the GSC and UAV will be higher than that of a blockchain-based approach. As a result, the probability of intercepting messages by attackers will increase.

2) Blockchain-Based UAV Authentication: In order to support security in IoT data collection, the work in [19] constructs a proof-of-stake (PoS) consensus-based blockchain among UAVs. In that work, the IoT communication and UAV deployment are optimized for maximizing the blockchain throughput. Considering security and privacy concerns for centralized authentication services in 5G-enabled UAVs, a blockchain-based authentication mechanism is proposed in [20], which particularly addresses the cross domain authentication for drones operating in different domains. For secure data collection in wireless sensor networks (WSNs), a blockchain-assisted data collection framework is designed in [21] for UAV-enabled WSNs. In addition, an identity authentication mechanism is also developed for UAVs to secure the data transmission. Tan et al. [2] propose a blockchain-enabled distributed authentication solution for industrial UAVs. Here, the proposed mechanism designs smart contracts that help perform secure operations for UAVs to update or acquire the corresponding information. The authors in [22] propose a machine learning-based UAV-base stations deployment mechanism based on computational power, energy, criticality of the network scenario, and nature of data. In addition, to address security issues in untrusted wireless connectivity for UAV-base stations, a blockchain-based information-sharing scheme is proposed. To develop a secure information sharing mechanism for UAV-assisted disaster rescue, Wang et al. [23] propose a blockchain-based architecture to protect data sharing in UAV communications, where vehicular fog computing is introduced to offload UAVsâ tasks. However, the aforementioned works do not consider the authentication of group of UAVs in UAV swarms.

3) Authentication in UAV Swarms: The work in [24] discusses the application of blockchain for UAV security in industries, along with the evaluation of Hyperledger Fabricbased blockchain technology to UAV networks. The authors in [25] investigate security upgrades supported by blockchain and the improvement of UAV swarm authentication utilizing blockchain-enabled security services. Bansal et al. [26] propose a PUF-based authentication and attestation approach for UAV swarms. Here, the scheme uses an optimal trajectory, which can help establish the trust in the communication. The work in [27] designs a blockchain-assisted trustworthy group communication scheme for UAV networks, where the authors use blockchain to facilitate key distributions and record communication activities. However, this work does not consider PUFs-based security and location-based clustering of UAVs. For multi-UAV coordination and swarm optimization, the authors in [28] propose a model that forms a Wireless Mesh Network (WMN) from the input of the UAVsâ locations. In that work, Blowfish and Advanced Encryption Standard (AES) are used to overcome security attacks.

4) Motivation: Based on the aforementioned related works, it is noted that there is a lack of research in designing decentralized authentication for UAV groups in UAV swarms. In that direction, location-based UAV cluster formation is important for reducing the message transmission delay, and consequently overall network performance is improved. Moreover, blockchain can help impose a decentralized authentication framework that can be used to store security-related information in a tamperproof way by multiple UAVs in a swarm. Thus, the blockchain helps guarantee trustworthy communications and data integrity, which are required by several UAV swarm-based applications, such as industrial applications, disaster management, and mission critical applications. Existing works do not investigate the use of blockchain for providing PUF-based authentication services in UAV swarms, where location-based clusters can be formed in an intelligent approach.

## B. Our Approach and Contributions

In this paper, by exploiting blockchain, we design a distributed authentication mechanism, SwarmAuth, which performs an authentication service for a group of UAVs, i.e., UAV swarms. Each UAV follows UAV registration and authentication with the GSC. In order to create UAV clusters, we use the K-means clustering approach, where we perform location-based clustering of UAVs. The K-means clustering scheme is an unsupervised machine learning algorithm, and thus it is considered an intelligent approach that dynamically forms clusters based on the current position of objects. Since the proposed SwarmAuth uses Kmeans clustering to create UAV clusters, the clustering approach becomes intelligent. The clustering can reduce communication delay and routing overhead, while improving the overall network performance. To the best of our knowledge, this work is the first to jointly consider online learning-based location-aware cluster formation and blockchain-based trusted authentication using PUFs for UAV swarms.

Contributions: Our most notable contributions are summarized as follows.

- Using the PUF, we design a two-way authentication scheme to mutually authenticate the GSC and UAV. Based on the individual authentication mechanism, we design an authentication approach for UAV swarms. The authentication services are provided cluster-wise, where the messages targeted for a set of UAVs in a cluster are aggregated and then transmitted from the GSC to the cluster and vice versa.

- To dynamically generate the UAV cluster, we use a Kmeans clustering-based online learning mechanism, where a cluster is formed dynamically considering the location of the UAVs.

- We introduce a blockchain-based authentication service for UAV swarms. The information required for the authentication is stored in the blockchain, and we design smart contracts to impose access control mechanisms on the secure information.

A formal security analysis is provided using the Mao and Boyd logic [29] and Scyther tool [30]. Considering several mainstream attacks, we also present an informal security proof.

- We implement the proposed blockchain in Truffle, which is a popular Ethereum blockchain development and testing framework. The blockchain peer nodes are hosted on the cloud server. Evaluation results show the access controls of the users and the time cost of the smart contract APIs designed in the blockchain.

We implement SwarmAuth in NS-3.36 [31], where the practical impact of SwarmAuth is assessed using several metrics, such as the average network throughput, delay, and communication and computation costs.

## C. Organization of This Paper

The organization of this paper is as follows. Section II presents the design philosophy of SwarmAuth. Section III discusses the authentication and group message transmission procedure. Section IV describes the proposed blockchain-based authentication service. Section V discusses the UAV cluster formation mechanism in SwarmAuth. In Section VI, a thorough security analysis of SwarmAuth is presented. Then, in Section VII, we present a comparative performance analysis of SwarmAuth with related mechanisms and evaluate the performance of the blockchain. Finally, Section VIII concludes the paper.

<!-- image-->  
Fig. 2. SwarmAuth design framework.

## II. SWARMAUTH: DESIGN PHILOSOPHY

In this section, we present the design details of SwarmAuth, which has three primary objectives as follows:

1) Defining an authentication process between the GSC and a UAV,

2) Implementing the UAV-GSC authentication process using a blockchain framework, such that a decentralized authentication approach can be achieved to store the authentication related information in the blockchain, and

3) Dynamically generating the UAV cluster considering the location of the UAVs, which will take the blockchainbased authentication service for the UAV-GSC authentication.

Accordingly, we define three primary functionalities â (i) authentication procedure, (ii) blockchain-based authentication service, and (iii) UAV cluster formation, as shown in Fig. 2. Once UAV clusters are formed, the UAVs use the blockchain-based UAV-GSC authentication service. Further details about these functionalities are discussed below.

1) Authentication procedure: This functionality defines the UAV-GSC authentication process and also describes the group message communication approach in a UAV swarm in SwarmAuth. The authentication procedure is done over two phases â (a) registration and (b) mutual authentication. In the registration phase, a UAV registers with the GSC, while in the mutual authentication phase, a UAV and the GSC authenticate each other to start UAV communications.

2) Blockchain-based authentication service: This functionality defines a blockchain architecture that is used to provide a distributed authentication service based on the aforementioned authentication procedure. Blockchain peer nodes are stored in the cloud server and can be accessed by the GSC and the UAVs.

3) UAV cluster formation: This functionality describes the mechanism to intelligently generate location-based UAV clusters using the K-means clustering approach, considering the position of each UAV while forming clusters. After generating UAV clusters, the UAV cluster formation functionality takes services from the other two functionalities for UAV authentication using a blockchain platform.

TABLE I LIST OF PRIMARY NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1> $\overline { { T I D _ { v } } }$ </td><td rowspan=1 colspan=1>Temporary IDofV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { U I D _ { v } } }$ </td><td rowspan=1 colspan=1>Permanent IDofV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N _ { v } } }$ </td><td rowspan=1 colspan=1>Randomnonce generated byV</td></tr><tr><td rowspan=1 colspan=1> $\overrightharpoon { G S I D }$ </td><td rowspan=1 colspan=1>ID of G</td></tr><tr><td rowspan=1 colspan=1> $\overline { { ( C _ { v } , R _ { v } ) } }$ </td><td rowspan=1 colspan=1>PUFchallenge-response pair ofV</td></tr><tr><td rowspan=1 colspan=1> $\overline { { h ( ) } }$ </td><td rowspan=1 colspan=1>Hash function</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D I C _ { v } } }$ </td><td rowspan=1 colspan=1>Dynamic identity code (DIC) of V</td></tr><tr><td rowspan=1 colspan=1> $\overline { { S K _ { v } } }$ </td><td rowspan=1 colspan=1>Session key for secure communication between Gand V</td></tr><tr><td rowspan=1 colspan=1> $\oplus$ </td><td rowspan=1 colspan=1>XOR operation</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Concatenationoperation</td></tr><tr><td rowspan=1 colspan=1> $F _ { k }$ </td><td rowspan=1 colspan=1>List ofUAVs in $\scriptstyle { \overline { { k ^ { t h } } } }$ flow (or cluster)</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \boldsymbol { M } _ { k j } ^ { R } } }$ </td><td rowspan=1 colspan=1>Message transmitted to $\overline { { j ^ { t h } } }$ UAVin the $\overline { { k ^ { t h } } }$ flow,during registration</td></tr><tr><td rowspan=1 colspan=1> $\overline { { M _ { k j } ^ { A i } } }$ </td><td rowspan=1 colspan=1>Message transmitted to $\overline { { j ^ { t h } \ U A \mathrm { V } } }$ in the $\overline { { k ^ { t h } } }$ flow,during authentication $( 1 \leq i \leq 2 )$ </td></tr><tr><td rowspan=1 colspan=1> $E ( M _ { k j } ^ { R } ) _ { k e y }$ </td><td rowspan=1 colspan=1> $\overline { { M _ { k j } ^ { R } } }$ encrypted with $\overline { { k e y } } = ( R _ { k j } \oplus N _ { k j } )$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { E ( M _ { k j } ^ { A i } ) _ { k e y } } }$ </td><td rowspan=1 colspan=1> $\widehat { M _ { k j } ^ { A i } }$ encrypted with key = (Rkj $\overline { { \boldsymbol { N } _ { k j } } } )$ (1â¤iâ¤2)</td></tr><tr><td rowspan=1 colspan=1> $\overline { { M ^ { R , a g g r } } }$ </td><td rowspan=1 colspan=1>Aggregated message transmitted in the $\overline { { k ^ { t h } } }$ flow,during registration</td></tr><tr><td rowspan=1 colspan=1> $\overline { { M ^ { A i , a g g r } } }$ </td><td rowspan=1 colspan=1>Aggregated message transmitted in the $\overline { { k ^ { t h } } }$ flow,during authentication $( 1 \leq i \leq 2 )$ </td></tr><tr><td rowspan=1 colspan=1> $\underline { { ( x _ { i } , y _ { i } , z _ { i } ) } }$ </td><td rowspan=1 colspan=1>Position of UAV Ui</td></tr><tr><td rowspan=1 colspan=1> $\overline { { K } }$ </td><td rowspan=1 colspan=1>Number of UAV clusters</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathcal { C } } }$ </td><td rowspan=1 colspan=1>Setof cluster centers</td></tr></table>

Table I shows the primary notations used in this paper. Next, we present details of the registration and authentication approaches defined in the authentication procedure.

## III. AUTHENTICATION PROCEDURE

The proposed registration and authentication approaches are followed by each UAV in a UAV swarm.

## A. Registration

Before the deployment, UAV V registers with GSC G. To this end, the UAV generates a dynamic identity code (DIC), which is shared with the GSC. The registration process follows two steps, as decribed in what follows. Fig. 3 shows different messages used for UAV registration in SwarmAuth. Details of the registration approach are described in what follows (the brief of a step is mentioned inside the parenthesis).

Step-1 (DIC generation at UAV):

1) V randomly generates a challenge $C _ { v }$ , then applies the PUF to produce the response $R _ { v }$ as

$$
R _ { v } = P U F ( C _ { v } ) .
$$

2) A random nonce, $N _ { v }$ , is generated, based on which a temporary ID, $T I D _ { v } ,$ v, is generated by V , as

$$
T I D _ { v } = h ( U I D _ { v } , N _ { v } ) .
$$

After registration, $T I D _ { \imath }$ is used to uniquely identify a vUAV during authentication.

3) T ID is split into D1 and D2. In order to retrieve $N _ { v }$ at vthe GSC-end, a parameter $Q _ { v }$ vis calculated by encoding $N _ { v }$ as

$$
Q _ { v } = N _ { v } \oplus T I D _ { v } \oplus D 1 \oplus D 2 .
$$

UAV V Ground station controller G   
1. Randomly generate $\overline { { C _ { v } } }$ and $\overline { { N _ { v } } } .$   
2. Compute $\check { R _ { v } } = P U F ( C _ { v } ) .$   
3. Calculate $T I D _ { v } = h ( \dot { U } I \dot { D } , N _ { v } ) .$   
4. Split TIDu into D1 and D2.   
5. Compute $Q _ { v } = N _ { v } \oplus T I D _ { v } \oplus D 1 \oplus D 2 .$   
6. Compute $P _ { v } = ( R _ { v } \oplus N _ { v } ) \oplus ( D 1 \parallel D 2 ) .$   
7. Generate $D I C _ { v } = h ( T I D _ { v } \parallel ( P _ { v } \oplus Q _ { v } ) \parallel R _ { v } )$   
8.Send $\langle T I D _ { v } , P _ { v } , Q _ { v } , D I C _ { v } \rangle$ toG.   
9. Store $\{ T I D _ { v } \}$ in database. 1. Split $T I D _ { v }$ into D1 and $D 2 .$   
terminate 2. Compute $N _ { v } = Q _ { v } \oplus T I D _ { v } \oplus D 1 \oplus D 2 .$   
3. Compute $R _ { v } = ( P _ { v } \oplus N _ { v } ) \oplus ( D 1 \parallel D 2 ) .$   
4.Verify $D I C _ { v } = h ( T I D _ { v } \parallel ( P _ { v } \oplus Q _ { v } ) \parallel R _ { v } )$   
5. Store $\{ T I D _ { v } , D I C _ { v } , P _ { v } , Q _ { v } \}$ in blockchain.   
terminate  
Fig. 3. UAV registration.

4) To retrieve $R _ { v }$ at the GSC, a parameter $P _ { v }$ is computed as

$$
P _ { v } = ( R _ { v } \oplus N _ { v } ) \oplus ( D 1 \parallel D 2 ) .
$$

5) $V '$ DIC, denoted by $D I C _ { v } ,$ is computed as

$$
D I C _ { v } = h ( T I D _ { v } \parallel ( P _ { v } \oplus Q _ { v } ) \parallel R _ { v } ) .
$$

6) V sends $T I D _ { v } , P _ { v } , Q _ { v } ,$ , and $D I C _ { v }$ to the GSC and stores $\{ T I D _ { v } \}$ v v vin its database. Let $M _ { v } ^ { R }$ denote the v vmessage sent by V to the GSC, and thus $M _ { v } ^ { R } =$ $\{ T I D _ { v } , D I C _ { v } , P _ { v } , Q _ { v } \}$

v v v vStep-2 (DIC verification at GSC):

1) When G receives $T I D _ { \imath }$ from V , G splits $T I D _ { \imath }$ into D1 vand D2, following the approach used by V .

2) The GSC decrypts $N _ { v }$ from $Q _ { v }$ as

$$
N _ { v } = Q _ { v } \oplus T I D _ { v } \oplus D 1 \oplus D 2 .
$$

3) Based on $N _ { v } , R _ { v }$ is decrypted from $P _ { v }$ as

$$
R _ { v } = ( P _ { v } \oplus N _ { v } ) \oplus ( D 1 \parallel D 2 ) .
$$

4) Based on $T I D _ { v } , \ P _ { v }$ , and $R _ { v } .$ , the value of $D I C _ { v }$ is v vcomputed and it is verified with $D I C _ { v }$ vsent by V . This vervification ensures that the correct information is retrieved by the GSC.

5) The GSC stores the tuple $\{ T I D _ { v } , D I C _ { v } , P _ { v } , Q _ { v } \}$ in the blockchain.

Therefore, at the end of the registration, the blockchain contains the tuple $\langle T I D _ { v } , D I C _ { v } , P _ { v } , Q _ { v } \rangle$ for each UAV in a swarm. In general, this tuple is represented as $\langle T I D , D I C , P , Q \rangle$ . The GSC can add or delete records of the ledger in the blockchain. In order to avoid information loss by a UAV, UAVs can only update $T I D , D I C , P$ , and Q. Each UAV can only update its own information, while GSC as $\mathrm { U A V s } ^ { \prime }$ registrar has the permission to add or delete records of the ledger. $T I D _ { v }$ is divided into D1 and D2, so if an adversary guesses $T I D _ { v } ,$ , they cannot use it to calculate $Q _ { v } , P _ { v }$ , and $D I C _ { v }$ v, which are computed by the v v vUAV through D1 and D2. Consequently, these two parts are also employed by the GSC to decrypt $N _ { v }$ and $R _ { v } .$ . As a result, decomposing $T I D _ { v }$ increases the security level in the UAV vauthentication process.

## B. Mutual Authentication

After a mutual authentication establishment between G and $V ,$ , a secure session key is generated between them, which is used for subsequent secure communication between these parties. For each new authentication, V generates a new $C _ { v }$ and $N _ { v } .$ . Accordingly, $P _ { v }$ and $Q _ { v }$ vare updated. This approach v v vensures the freshness of an authentication request. Both UAVs and the GSC do not store $N _ { v }$ and $R _ { v }$ in their databases. After v vthe successful registration of UAVs or the completion of an authenticated session, UAVs compute $\langle T I D , D I C , P , Q \rangle$ for the next authentication process and update the tuple accordingly in the blockchain. This approach is taken to avoid the time it takes to update the data in the next authentication process. Fig. 4 shows different messages used for the mutual authentication in SwarmAuth. Details of the authentication approach are described in what follows.

Step-1 (Authentication initiation at UAV):

1) When V wants to establish a communication session with the GSC, it randomly generates $N _ { v }$ and $C _ { v }$ and then applies the PUF to produce $R _ { v }$ from $C _ { v }$

2) V recomputes $T I D _ { v } , P _ { v } , Q _ { v }$ , and $D I C _ { v }$ and updates vthem in the blockchain.

3) In order to authenticate V at the GSC, $T I D _ { v }$ is sent to G. At this step, let $M _ { v } ^ { A 1 }$ vdenote the message sent by V to G, where $M _ { v } ^ { \bar { A } 1 } = \{ T { \bar { I } } D _ { v } \}$

v vStep-2 (UAV verification and session key generation at GSC):

1) After getting $\{ T I D _ { v } \}$ from the UAV, G splits $T I D _ { v }$ v vinto D1 and D2 by using the mechanism followed at registration time. From the blockchain, the GSC finds $P _ { v }$ and $Q _ { v }$ corresponding to T ID sent by the UAV.

v2) Based on $T I D _ { v } , P _ { v }$ , and $Q _ { v }$ v, the GSC computes $N _ { v }$ and $R _ { v }$

v3) The GSC calculates $D I C _ { v } = h ( T I D _ { v } \parallel ( P _ { v } \oplus Q _ { v } )$  $R _ { v } )$ . If it matches the $D I C _ { v }$ vcorresponding $\tan \ T I D _ { \imath }$ stored in the blockchain, V is successfully verified as a registered UAV.

UAVV Ground station controller G   
1. Randomly generate $\overline { { N _ { v } } }$ and ${ \overline { { C _ { v } } } } .$   
2. Calculate $\begin{array} { r } { \check { R _ { v } } = P U F ( C _ { v } ) . } \end{array}$   
3. Compute $\begin{array} { r } { T I D _ { v } = h ( \dot { U } I \dot { D } , N _ { v } ) . } \end{array}$   
4. Calculate $Q _ { v } = N _ { v } \oplus T I D _ { v } \oplus D 1 \oplus D 2 .$   
5. Calculate $P _ { v } = ( R _ { v } \oplus N _ { v } ) \oplus ( D 1 \parallel D 2 ) .$   
6. Compute $D I C _ { v } = h ( T I \dot { D } _ { v } \parallel ( P _ { v } \oplus Q _ { v } ) \parallel R _ { v } ) .$   
7.Update $T I D _ { v } , P _ { v } , Q _ { v } ,$ and $D I C _ { v }$ in blockchain.   
8.Send $\underbrace { \langle T I D _ { v } \rangle } _ { \mathrm { ~ } }$ to G.   
1. Split $T I D _ { v }$ into $D 1$ and D2.   
2.Find $P _ { v }$ and $Q _ { v }$ from blockchain, for $T I D _ { v }$   
3. Compute $N _ { v } = Q _ { v } \oplus T I D _ { v } \oplus D 1 \oplus D 2 .$   
4. Compute $R _ { v } = \left( P _ { v } \oplus N _ { v } \right) \oplus \left( D 1 \parallel D 2 \right)$   
5.Verify $D I C _ { v } = \dot { h } ( T I D _ { v } \parallel ( P _ { v } \oplus \dot { Q _ { v } } ) \parallel R _ { v } ) .$   
6. Generate $G V C = h ( T I \vec { D _ { v } } \parallel G S I D \parallel R _ { v } \parallel N _ { v } )$   
7. Compute $S K _ { v } = h ( T I D _ { v } \parallel ( R _ { v } \oplus \ddot { N _ { v } } ) \parallel \xrightarrow { . } { \cal D I C } _ { v } )$   
8. Generate $S K C _ { v } = h ( S K _ { v } \parallel G V C \parallel R _ { v } \parallel N _ { v } ) .$   
9. Send $\underbrace { \langle G V C , S K C _ { v } \rangle } _ { \mathrm { ~ } }$ to $V .$   
9. Verify $G V C = h ( T I D _ { v } \parallel G S I D \parallel R _ { v } \parallel N _ { v } )$ terminate   
10. Calculate $S K _ { v } = h ( T I { \cal D } _ { v } \parallel ( R _ { v } \oplus N _ { v } ) \parallel D I C _ { v } )$   
11. Verify $S K C _ { v } = h ( S K _ { v } \parallel G V C \parallel R _ { v } \parallel N _ { v } ) .$   
terminate  
Fig. 4. UAV authentication.

4) The GSC generates a GSC verification code (GVC) as

$$
G V C = h ( T I D _ { v } \parallel G S I D \parallel R _ { v } \parallel N _ { v } ) ,
$$

$$
S K C _ { v } = h ( S K _ { v } \parallel G V C \parallel R _ { v } \parallel N _ { v } ) .
$$

where GSID is the unique identifier (ID) of the GSC. The GVC is used to verify the GSC at the UAV end.

6) To verify the session key at V , a session key code (SKC) is generated as

7) The GSC sends GV C and $S K C _ { v }$ to V . At this step, let $M _ { v } ^ { A 2 }$ vdenote the message sent by G to V , where $M _ { v } ^ { A 2 } =$ $\{ \bar { G } V C , S K C _ { v } \}$

5) For further communication with V , the session key, denoted by $S K _ { v }$ , is computed as

$$
S K _ { v } = h ( T I D _ { v } \parallel ( R _ { v } \oplus N _ { v } ) \parallel D I C _ { v } ) .
$$

vStep-3 (GSC verification at UAV):

1) V computes $G V C = h ( T I D _ { v } \parallel G S I D \parallel R _ { v } \parallel N _ { v } )$ and vverifies it against the GV C sent by the GSC.

2) After the successful verification of the GSC, the UAV calculates $S K _ { v } = h ( T I D _ { v } \parallel ( R _ { v } \oplus N _ { v } ) \parallel D I C _ { v } )$ . Then, $S K C _ { v }$ v v v vis computed, and if it matches the $S K C _ { v }$ sent by vV , the session key $S K _ { \imath }$ is verified.

In general, $M _ { v } ^ { R } , ~ M _ { v } ^ { \dot { A } 1 }$ , and $M _ { v } ^ { A 2 }$ are represented as $M ^ { R }$ $M ^ { A 1 }$ , and $M ^ { A 2 }$ v v v, respectively. Next, we discuss the proposed group message transmission procedure for a UAV swarm.

## C. Group Message Transmission

Based on the individual registration and authentication mechanisms discussed in Sections III-A and III-B, SwarmAuth performs an authentication for a cluster of UAVs. In order to communicate with the UAVs in a cluster, the GSC creates a flow path connecting the GSC with the CH in a cluster. The communication between the GSC and UAVs are carried out in a hop-by-hop approach. The GSC provides the services cluster-wise, and for that purpose, messages for a cluster are aggregated and then transmitted to the cluster. In this context, the GSC G first transmits a message to $V _ { i } ,$ , which is the CH of the $i ^ { t h }$ cluster. Then, $V _ { i }$ iforwards the message to other UAVs iin the cluster. For UAV registration and authentication, since messages are communicated between the GSC and the UAVs, the mutual authentication is performed between the GSC and a UAV. In this context, the CH only performs forwarding of messages to the UAVs in a cluster. Specifically, clusters determine the number of flow paths for the UAV communication. Thus, for K clusters, K flows (or paths) are formed, which are denoted by $\{ F _ { 1 } , F _ { 2 } , \ldots , F _ { K } \}$ , where $F _ { k } \ ( 1 \leq k \leq K )$ denotes the set of UAVs in the $k ^ { t h }$ Kflow. Let $n ^ { k }$ kbe the number of UAVs in $F _ { k }$ and thus $n ^ { k } = | F _ { k } |$ |. At the time of registration, let $M _ { k j } ^ { R }$ be the message transmitted $\tan j ^ { t h }$ kjUAV in flow k. At the authentication time, let $M _ { k j } ^ { A 1 }$ and $M _ { k j } ^ { A 2 }$ be the messages transmitted to the $j ^ { t h }$ kj kjUAV in flow k. Fig. 5 shows the group message transmission in a cluster.

The location of the UAVs is not considered in the proposed authentication mechanism, and therefore, the cluster formation approach does not impact the authentication process. However, as the number of clusters increases, the number of aggregated messages used for authentication services are increased. This is because authentication services for the UAVs are provided cluster-wise by aggregating the messages destined for a cluster.

<!-- image-->  
Fig. 5. Group message transmission in a cluster.

1) Message Encryption: The PUF response and nonce value are changed in each authentication initiation. Thus, to ensure message authentication and freshness in an authentication approach, each $M _ { k j } ^ { R }$ is encrypted with $\mathrm { \dot { \it ~  ~ } } e y = \left( R _ { k j } \oplus N _ { k j } \right)$ , where $R _ { k j }$ and $N _ { k j }$ are the PUF response and random nonce of the $j ^ { t h }$ kj kUAV in the $\ddot { k } ^ { t h }$ flow, respectively. Let $E ( M _ { k j } ^ { R } ) _ { k e y }$ represent the message $M _ { k j } ^ { R }$ encrypted by key. For the encryption purpose, the kjAES is used.

2) Flow Paths in Registration: To create the aggregated message for flow k, a message $L _ { k j } ^ { R }$ is constructed for UAV j by appending $D I C _ { k j }$ kjbefore the encrypted value of $M _ { k j } ^ { R }$ . The kj kjpurpose of this aggregation is to enable the UAV to decrypt messages intended for it by finding its $D I C _ { k }$ in the flow and decrypting the message using $k e y = \left( R _ { k j } \oplus N _ { k j } \right)$ . Even if an adversary manages to guess $D I C _ { k j }$ kjfor the $j ^ { t h }$ kjUAV in flow $k ,$ kjthey will not be able to decrypt the corresponding message $M _ { k j } ^ { R }$ because it is encrypted with k ${ \mathcal { Y } } = ( R _ { k j } \oplus N _ { k j } )$ kj). Therefore, the adversary would need to guess $R _ { k j } , N _ { k j }$ kj, and the key to decrypt the message. In general, for the $k ^ { t h }$ kjflow, we represent $L _ { k j } ^ { R }$ as $L _ { k } ^ { R }$ . Thus, we have

$$
L _ { k j } ^ { R } = { \cal D } I C _ { k j } \parallel E ( M _ { k j } ^ { R } ) _ { k e y } ,\tag{2}
$$

where $1 \leq j \leq n ^ { k }$ and $D I C _ { k j }$ is the DIC of the $j ^ { t h }$ UAV in the $k ^ { t h }$ flow. Based on $D I C _ { k j } , \bar { L } _ { k j } ^ { R }$ helps the $j ^ { t h }$ UAV identify its message $M _ { k j } ^ { R }$ . Then, considering all the UAVs in the $k ^ { t h }$ flow, the aggregated message is formed. Let $M _ { k } ^ { R , a g g r }$ represent the aggregated message, defined as

$$
M _ { k } ^ { R , a g g r } = L _ { k 1 } ^ { R } \parallel L _ { k 2 } ^ { R } \parallel \cdots \parallel L _ { k n ^ { k } } ^ { R } .\tag{3}
$$

3) Flow Paths in Authentication: For the authentication purpose, let $L _ { k j } ^ { A l }$ represent the concatenation of $D I C _ { k j }$ and $M _ { k j } ^ { A l }$ and $M _ { k } ^ { A l , a g { \bar { g } } r }$ be the aggregated authentication messages, where $l \in \{ 1 , 2 \}$ . Now, based on (2) and (3), $L _ { k j } ^ { A l }$ and $M _ { k } ^ { A l , a g g r }$ are defined for the authentication. Thus, $L _ { k j } ^ { A l }$ kcan be defined as

$$
L _ { k j } ^ { A l } = D I C _ { k j } \parallel E ( M _ { k j } ^ { A l } ) _ { k e y } , l \in \{ 1 , 2 \} .\tag{4}
$$

Therefore, the aggregated message $M _ { k } ^ { A l , a g g r }$ can be represented as

$$
M _ { k } ^ { A l , a g g r } = L _ { k 1 } ^ { A l } \parallel L _ { k 2 } ^ { A l } \parallel \cdots \parallel L _ { k n ^ { k } } ^ { A l } , l \in \{ 1 , 2 \} .\tag{5}
$$

## D. Intended Message Identification in Cluster

During registration (or authentication), when $M _ { k } ^ { R , a g g r }$ (or $M _ { k } ^ { A l , a g g r } )$ k is transmitted to a cluster, each UAV first checks $D I C _ { k }$ in $L _ { k } ^ { R }$ (or $L _ { k } ^ { A l } )$ . If a UAV finds its $D I C _ { k }$ in the flow, the k kmessage followed by $D I C _ { k }$ kis intended for the UAV, and thus it decrypts the message using key.

## E. Difference Between Our Approach and the Existing PUF-Based UAV Authentication Mechanism in [15]

The authors in [15] designed UAV-GSC and UAV-UAV authentication schemes using PUFs. However, our work proposes a UAV-GSC authentication mechanism for UAV swarms using PUFs. Moreover, the work in [15] does not address the authentication for UAV swarms. In addition, blockchain is not used in [15], and thus the authentication mechanism proposed in [15] is not a distributed approach, where the GSC stores several authentication related information, such as the challenge-response pair and the temporary ID of UAVs, in its database. Furthermore, the UAV stores the challenge value, the temporary ID of the UAV, and the ID of the GSC in the UAVâs database. However, in our approach, the GSC does not store any authentication related data in its database, and the UAV stores only its temporary ID in its database. At the end of the registration, the blockchain contains the information for each UAV in a swarm.

In the next section, we elaborate on the blockchain architecture for the authentication service proposed in SwarmAuth.

## IV. BLOCKCHAIN-BASED AUTHENTICATION SERVICE

In this section, we describe the proposed blockchain architecture and the working flow of the authentication service.

## A. Architecture

Since blockchain eases the process of securely storing data and recording transactions, we apply it for the following two purposes.

1) We use blockchain as a distributed storage to store the parameters required for the registration and authentication in a tamper-proof way. We call these parameters Security Information (SI). As discussed in Section III, the blockchain stores T ID, DIC, P, Q, and therefore SI includes T ID, DIC, P, Q.

2) Using smart contracts, we restrict the operations on security parameters, such that only authorized users can update those parameters.

The proposed system architecture of the blockchain-based authentication service is shown in Fig. 6. Each of the blockchain peer nodes stores a copy of the ledger that holds the security information. Thus, a ârecordâ of the ledger contains the security information. Any update in this information results in changes in the ledger, leading to a new block in the blockchain. Thus, every change in the blockchain is incrementally recorded by the blockchain, and consequently the UAV authentication service becomes unforgeable and traceable. To automatically execute operations (such as addition, update or deletion) on the security information, we apply smart contracts which are installed on blockchain peer nodes. The GSC and UAVs can call smart contract APIs and trigger executions of smart contracts. Before the authentication, a UAV needs to be registered in the GSC, and UAVs have the permission to only update their own information. In our approach, we introduce a validation step, where blockchain peer nodes validate changes of the ledger before finally being recorded into the blockchain.

<!-- image-->  
Fig. 6. System model for SwarmAuth.

Next, we discuss the key components of the proposed blockchain architecture. Based on these components, the working flow of SwarmAuth is defined.

## B. Key Components

In SwarmAuth, the key components of the blockchain include blockchain nodes, ledger, and smart contracts.

1) Blockchain Nodes: In the proposed blockchain, we introduce two types of nodes â (i) endorsement nodes and (ii) validation nodes. All blockchain peer nodes act as endorsement nodes, which are responsible for receiving transaction proposals from the GSC or UAVs, checking the permission to update the ledger, executing the appropriate smart contracts and returning the results as proposal responses to validation nodes. These verify and validate the endorsements. If they are verified, validation nodes create new blocks and add them into the blockchain. Thus, validation nodes have the responsibility for validating each new block before it is inserted into the blockchain. Validation nodes are randomly selected from blockchain peer nodes. Each of the endorsement and validation nodes holds a copy of the updated ledger, and the smart contracts are installed on endorsement/validation nodes to execute modifications in the blockchain. Validation nodes ensure that copies of the ledger hosted by blockchain peer nodes remain the same.

2) Ledger and Smart Contracts: To realize the registration and authentication service, we designed a ledger known as Security Information Ledger (SIL), which stores T ID, DIC, P, Q. For SIL, a smart contract called Security Information Contract (SIC) is designed, which contains several APIs for the GSC or UAVs to invoke at the time of the UAV registration or authentication process. Details of the smart contract are discussed below.

Smart Contract Operations: In the smart contract, the APIs perform the following operations: (i) saveSI, (ii) deleteSI, (iii) updateSI, (iv) queryP Q, and (v) queryDIC. The details of these operations are defined below.

saveSI is used to store a new SI into SIL, and it can only be invoked by the GSC. deleteSI is the opposite function of saveSI, used to delete an SI from SIL. It can only be invoked by the GSC. The SI of a UAV is deleted when the UAV loses connection with the GSC or is identified as malicious. We define a permission mechanism in the SIC to ensure that the saveSI and deleteSI APIs are accessed by the GSC only. If any UAV requests access to these APIs, the request is refused by the SIC.

- To update the SI of a UAV, updateSI is used by the UAV, where it can only update its own T ID, DIC, P , and Q, corresponding to the UAVâs old T ID.

We also define two query APIs, queryP Q and queryDIC, which are used to find P , Q, and DIC corresponding to the T ID of a UAV. Specifically, for a given T ID, queryP Q returns P and Q, and queryDIC returns DIC. Therefore, these two query APIs are used by the GSC to ask for $P ,$ Q, or DIC for a T ID supplied to the SIC. Since these values are modified for a UAV before the beginning of the authentication approach, the GSC receives fresh values of these parameters for each authentication. Furthermore, a UAV does not have permission to get P , Q, and DIC for another UAV.

Determination of Freshness of SI: After the authentication process of UAV V is completed, the GSC stores $N _ { v }$ , which vhelps check the freshness of an authentication initiation in the future. This is because each authentication procedure should generate a new $N _ { v }$ . The freshness of $N _ { v }$ is reflected in P , Q, v vand DIC. Therefore, if a UAV fails to update these values before the authentication time, the GSC will refuse its authentication initiation request.

3) Smart Contract Applications: The blockchain platform provides a Software Development Kit (SDK) that uses a set of functionalities to define a blockchain. We use the SDK to install smart contract applications on the GSC and UAVs. The applications enable them to create transaction proposals, which can be used to update the SI in the SIL. Then, to submit the proposals, appropriate smart contract APIs are invoked by the smart contract applications. All applications are executed in a listening mode, such that the submission of any transaction proposal can be captured and the corresponding API is invoked.

## C. Working Flow of Updating SIL

The SIL update procedure is shown in Fig. 7. For instance, we assume that V wants to update its SI in order to prepare it for the authentication initiation. First, it is required to send a transaction proposal by V , and for that purpose, $V$ calls updateSI through the smart contract application installed on V and sends the proposal to endorsement nodes situated near it. The nodes check whether V has the permission to update the corresponding SI. If the update request is validated, the endorsement nodes execute SIC and return the results to validation nodes as a transaction proposal response. The endorsement nodes forward the results to their nearby validation nodes. After receiving enough responses, these nodes validate the proposal response, and if it is verified, a new block is inserted into the blockchain. As a result, the SIL of V is updated according to the executed transaction. Therefore, after this step, the SIL will reflect the updated value, which can be accessed by the GSC. Lastly, a feedback is sent to V informing it about the status of the transaction proposal result, i.e., success or failure, where success indicates that the proposal is executed successfully. When the GSC wants the SI of V , it accesses the blockchain and runs a query proposal (queryP Q or queryDIC), which is processed by the endorsement and validation nodes following the aforementioned steps.

<!-- image-->  
Fig. 7. Working flow of SwarmAuth.

Next, we discuss a K-means clustering-based UAV cluster formation mechanism used in SwarmAuth.

## V. UAV CLUSTER FORMATION

Let the set of UAVs be modeled as $U = \{ v _ { 1 } , v _ { 2 } , . . . v _ { n } \}$ nBy sending messages, UAVs exchange information including identification numbers of the cluster and UAV, role of a UAV (CH or CM), position of a UAV, distance between a UAV and the corresponding CH, and distance between a UAV and the GSC.

## A. Determination of the Number of Clusters

To reduce the cluster formation overhead and utilize the channel bandwidth efficiently, it is required to determine the optimal number of clusters for the clustering center selection. In a cluster, let the throughput of a CM be $T _ { M }$ , which can be defined as [32]

$$
T _ { M } = \Theta ( B _ { 1 } / \sqrt { n / K } ) .\tag{6}
$$

Similarly, the throughput of the CH is defined as [32]

$$
T _ { H } = \Theta ( B _ { 2 } / \sqrt { K } ) .\tag{7}
$$

Here, n is the total number of UAVs in the network, and K denotes the number of clusters. $B _ { 1 }$ represents the bandwidth of intra-cluster communications, and $B _ { 2 }$ is the bandwidth of inter-cluster communications. In order to maintain the throughput balance between the aforementioned two cluster communications, the following relationship needs to be

maintained [33].

$$
\frac { K - 1 } { K } T _ { M } \leq T _ { H }\tag{8}
$$

When $\textstyle { \frac { K - 1 } { K } } T _ { M }$ reaches the maximum value, and n is large K Menough, the value of K is obtained as

$$
K = { \frac { B _ { 2 } } { B _ { 1 } } } { \sqrt { n } } .\tag{9}
$$

## B. Clustering Center Selection

Using the uniform distribution, the initial clustering center, denoted by $c _ { 1 } .$ , is randomly chosen from the set U . Let $D ( v _ { i } )$ idenote the minimum value of the euclidean distance between the currently chosen clustering center and $v _ { i } .$ , where $1 \leq i \leq n$ Let $P ( v _ { i } )$ be the probability of choosing $v _ { i }$ as the next cluster icenter. We compute $P ( v _ { i } )$ as follows.

$$
P ( v _ { i } ) = { \frac { D ( v _ { i } ) ^ { 2 } } { \sum _ { v _ { i } \in U } } } D ( v _ { i } ) ^ { 2 }\tag{10}
$$

The UAV which has the highest $P ( v _ { i } )$ is selected as the next icluster center. This process is repeated until K centers are selected, and let the set of clustering centers be expressed as $\mathcal { C } = \{ c _ { 1 } , c _ { 2 } , . . . c _ { K } \}$ . We use the K centers for the K-means Kclustering algorithm.

## C. Cluster Formation

Based on the closest cluster center, the set U is divided into K clusters using the K-means clustering algorithm [34]. To this end, after generating C, we compute the distance between each UAV and the cluster centers. Then, we compute the minimum distance $d _ { c v _ { p } } ^ { m i n }$ , which is expressed as

$$
d _ { c v _ { p } } ^ { m i n } = m i n ( d _ { c _ { 1 } v _ { p } } , d _ { c _ { 2 } v _ { p } } , \ldots , d _ { c _ { K } v _ { p } } ) .\tag{11}
$$

Based on (11), we assign each UAV to its nearest cluster center. For instance, if $d _ { c v _ { p } } ^ { m i n } = d _ { c _ { i } v _ { p } }$ , UAV $v _ { p }$ is clustered into the $i ^ { t h }$ cv c v pcluster. This process is repeated until K clusters are formed with all the UAVs. Let $( x _ { p } , y _ { p } , z _ { p } )$ be the position of $v _ { p } { } _ { ; }$ , where $x _ { p } ,$ $y _ { p } .$ , and $z _ { p }$ p p p p pare X, Y, and Z coordinate values, respectively. Since p pUAVs can have high mobility, the clustering center values are updated as

$$
\mathcal { C } = \frac { 1 } { J _ { i } } \left( \sum _ { p = 1 } ^ { J _ { i } } x _ { p } , \sum _ { p = 1 } ^ { J _ { i } } y _ { p } , \sum _ { p = 1 } ^ { J _ { i } } z _ { p } \right) ,\tag{12}
$$

where $J _ { i }$ is the number of UAVs in the $i ^ { t h }$ cluster. Therefore, ibased on the positions of the UAVs, C is changed, and consequently, the clusters of the UAVs are updated dynamically. After the formation of clusters, when UAV $v _ { p }$ travels further than a distance of $d _ { c _ { i } v _ { p } }$ p, the distance between UAV $v _ { p }$ and the corresponding cluster center is recomputed. If the calculated distance becomes greater than $d _ { c _ { i } v _ { p } }$ , C is updated following (12). This is because the distance $d _ { c _ { i } v _ { p } }$ exceeds its last distance from c vthe associated cluster center, leading to a high probability of leaving the cluster by the UAV.

## VI. SECURITY ANALYSIS

The formal security proof of SwarmAuth is analyzed using the broadly-accepted Mao and Boyd logic [29] and Scyther tool [30]. In addition, we also provide an informal proof, which uses the old-fashioned cryptanalysis and guarantees versatility and security [35], [36].

## A. Formal Security Proof Using Mao and Boyd Logic

For the formal security proof using Mao and Boyd logic, we apply the nonce-verification, authentication, confidentiality, good-key, super-principal, and fresh inference rules [29]. To this end, we prove the statements ${ } ^ { * * } V$ believes $N _ { v }$ is a good secret key between V and $G ^ { \dprime }$ and $^ { * } G$ believes $N _ { v }$ vis a secret key between V and $G ^ { \dprime }$

Claim 1: V believes $N _ { v }$ is a secret key between V and G.

Proof: Since $R _ { v }$ vis the output of the PUF, and G receives $R _ { v }$ vin encrypted format, we can have the statement $^ { 6 6 } V$ believes $R _ { v }$ is a good secret between V and Gâ (13). Moreover, each vauthentication process is initiated with a new nonce $N _ { v }$ , which vis only shared with G in encrypted format. Thus, âV believes none other than G have access to $N _ { v } { } ^ { , , }$ (14). V uses $R _ { v }$ to encrypt $N _ { v } \left( 1 5 \right)$ v v. The confidentiality rule is applied to (13), (14), vand (15), which yields âV believes none other than V and G have access to $N _ { v } \} ^ { * } \left( 1 6 \right)$ .

$$
V \left| \equiv V \xrightarrow { R _ { v } } G . \right.\tag{13}
$$

$$
V \left| \equiv \left\{ G \right\} ^ { c } \triangleleft \right\| N _ { v } .\tag{14}
$$

$$
V \stackrel { R _ { v } } { \backsim } N _ { v } .\tag{15}
$$

$$
V \perp \equiv \{ V , G \} ^ { c } \triangleleft \| N _ { v } .\tag{16}
$$

At each authentication initiation, since a new $N _ { v }$ is generated, $^ { 6 6 } V$ believes $N _ { v }$ vis freshâ (17). Applying the good-key rule to (16) vand (17), proves that âV believes $N _ { v }$ is a secret key between V and $G " ( 1 8 )$ .

$$
V \equiv \# ( N _ { v } ) .\tag{17}
$$

$$
V \uplus V \land \bigotimes U .\tag{18}
$$

Claim 2: G believes $N _ { v }$ is a secret key between V and G.

Proof: $R _ { v }$ vis unique to V and is transmitted to G in encrypted vform. Moreover, $R _ { v }$ is computed using D1 and D2, which are vonly known to V and G. Thus, âG believes $R _ { v }$ is a good secret between V and $G ^ { \prime 9 } ~ ( 1 9 ) . ~ G$ can decipher $N _ { v }$ using $R _ { v }$ (20). v vNow, the authentication rule is applied to (19) and (20), and consequently the statement, âG believes V encrypted $N _ { v }$ using $R _ { v } { } ^ { \ast }$ v, is obtained (21). In each authentication process, V creates a new $N _ { v }$ , and thus $^ { 6 6 } G$ believes $N _ { v }$ is freshâ (22).

$$
G \left| \equiv U \xrightarrow { R _ { v } } G . \right.\tag{19}
$$

$$
G \ { } ^ { R _ { v } } \ N _ { v } .\tag{20}
$$

$$
G \equiv U \stackrel { R _ { v } } { \sim } N _ { v } .\tag{21}
$$

$$
G \models \# ( N _ { v } ) .\tag{22}
$$

Now, we apply the nonce-verification rule to (21) and (22) and get âG $^ { 6 6 } G$ believes V believes that $R _ { v }$ is a good secret between V and $G ^ {  }$ (23). Since $N _ { v }$ is new in each authentication, we have the statement $^ { 6 6 } G$ vbelieves V believes that none other than G have access to $N _ { v } \textsuperscript { * } ( 2 4 )$ . The confidentiality rule is applied vto statements (21), (23), and (24), and we obtain $^ { 6 6 } G$ believes V believes that no one other than V and G have access to $N _ { v } { } ^ { , , }$ (25). It is considered that V is legitimate and G believes V vis trusted (26).

$$
G | \equiv V | \equiv \langle \stackrel { R _ { v } } { \longrightarrow } G . 
$$

$$
G \perp \equiv V \perp \equiv \{ G \} ^ { c } \triangleleft \| N _ { v } . \tag{23}
$$

$$
G \equiv V \equiv \{ V , G \} ^ { c } \triangleleft \Vert N _ { v } .\tag{24}
$$

$$
G \Vdash { s u p } ( V ) .\tag{25}
$$

(26)

Using the super-principal rule on (25) and (26), we get $^ { 6 6 } G$ believes no one other than G and V have access to $N _ { v } \textsuperscript { , } ( 2 7 )$ vNow, we apply the good-key rule to (22) and (27) and obtain $^ { 6 6 } G$ believes $N _ { v }$ is a secret key between V and $G ^ { \ast }$ (28).

$$
G \mid \equiv \{ V , G \} ^ { c } \triangleleft \| \ N _ { v } .\tag{27}
$$

$$
G \mid \equiv V \stackrel { N _ { v } } { \longleftrightarrow } G .\tag{28}
$$

Hence, adversaries cannot access $N _ { v }$ . Similarly, it can be proved that adversaries cannot access $R _ { v }$ . Therefore, if $N _ { v }$ and $R _ { v }$ v vcannot be accessed by adversaries, the secrecy of these vparameters is maintained in different types of attacks, such as man-in-the-middle, masquerade, and replay attacks.

## B. Formal Security Analysis Using Scyther

Scyther [30] is a security analysis simulator that verifies security protocols with different number of sessions. We implement SwarmAuth in Scyther, where we set (i) the search pruning to âFind All Attacksâ, (ii) the matching type to âFind All Type Flawsâ, (iii) the number of runs to 10, and (iv) the per claim maximum number of patterns to $^ { 6 6 } 1 0 ^ { \circ }$ . In our implementation in Scyther, the name of the protocol is SwarmAuth, in which $\cdot _ { G } ,$ and $^ { \bullet } V ^ { \bullet }$ are known as ârolesâ. Each of them states 7 claims, as shown in Fig. 8, where it is noted that both $R _ { v }$ and $N _ { v }$ are v vsecret between G and V , which is mentioned in claims 1 and 2 (in both V and G). The general synchronous property and consistency of the protocol are defined by claim 3 (N isynch), which also ensures that a message receiving event is preceded by a message sending event. In claim 4 (N iagree), it is stated that a role who is acting as an initiator and performing one-way authentication with another one acting as a responder believes that after the execution of the protocol, the data consistency is achieved with the responder. In claim 5 (Commit), the successful execution of the protocol is ensured maintaining the secrets of $N _ { v }$ and $R _ { v }$ . Claim 6 (Alive) maintains the liveness v vof G and V throughout a protocol execution. If it is believed by a role that it can communicate with another one, claim 7 (W eakagree) is satisfied.

<table><tr><td colspan="5"> Scyther results : verify</td></tr><tr><td>Claim</td><td></td><td></td><td>Status</td><td>Comments</td></tr><tr><td>SwarmAuth V</td><td> SwarmAuth,i1</td><td>Secret Nv</td><td>Ok</td><td>No attacks within bounds.</td></tr><tr><td></td><td> SwarmAuth,i2</td><td> Secret Rv</td><td>Ok</td><td> No attacks within bounds.</td></tr><tr><td></td><td> SwarmAuth,i3</td><td> Nisynch</td><td>Ok</td><td> No attacks within bounds.</td></tr><tr><td></td><td>SwarmAuth,i4</td><td> Niagree</td><td>Ok</td><td> No attacks within bounds.</td></tr><tr><td></td><td>SwarmAuth,i5</td><td> Commit G,Nv,Rv</td><td>Ok</td><td> No attacks within bounds.</td></tr><tr><td></td><td>SwarmAuth,i6</td><td> Alive</td><td>Ok</td><td>No attacks within bounds.</td></tr><tr><td></td><td>SwarmAuth,i7</td><td> Weakagree</td><td>Ok</td><td>No attacks within bounds.</td></tr><tr><td>G</td><td>SwarmAuth,r1</td><td> Secret Nv</td><td>Ok</td><td> No attacks within bounds.</td></tr><tr><td></td><td>SwarmAuth,r2 </td><td> Secret Rv</td><td>Ok</td><td>No attacks within bounds.</td></tr><tr><td></td><td> SwarmAuth,r3</td><td> Nisynch</td><td>Ok</td><td> No attacks within bounds.</td></tr><tr><td></td><td> SwarmAuth,r4</td><td> Niagree</td><td>Ok</td><td>No attacks within bounds.</td></tr><tr><td></td><td>SwarmAuth,r5</td><td> Commit V,Nv,Rv</td><td>Ok</td><td> No attacks within bounds.</td></tr><tr><td></td><td> SwarmAuth,r6</td><td> Alive</td><td>Ok</td><td>No attacks within bounds.</td></tr><tr><td>Done.</td><td>SwarmAuth,r7</td><td> Weakagree</td><td>Ok</td><td>No attacks within bounds.</td></tr></table>

Fig. 8. Result of formal security analysis using Scyther.

## C. Informal Security Analysis

Using informal security proof, we analyze the security of SwarmAuth considering different well-known security attacks, as discussed below.

1) Mutual Authentication: In each authentication process, new $( C _ { v } , R _ { v } )$ and $N _ { v }$ are created, and they are not stored in $G \ ' \mathrm { s }$ or $V \mathrm { \ ' } _ { \mathrm { s } }$ v database. Moreover, V transmits these values to G in encrypted format. Therefore, the session key $S K _ { v }$ generated using $R _ { v }$ and $N _ { v } ,$ v, is unique in each sessions and can v vbe successfully computed only between G and V . Hence, mutual authentication can be achieved between these two parties.

2) Forward Secrecy: In a session, if an adversary is able to guess $S K _ { v }$ , the security of the next session will not be hampered. vThis is because the $( C _ { v } , R _ { v } )$ pair, $R _ { v } .$ , and $N _ { v }$ are fresh in each v v v vnew authentication initiation, and accordingly, $S K _ { \imath }$ and $D I C _ { v }$ are changed in every session. Moreover, based on $R _ { v }$ and $N _ { v } ,$

$S K C _ { v }$ needs to be verified before the communication using $S K _ { \tau }$ starts. In addition, before generating a session key, $D I C _ { v }$ and $G V C$ vmust be verified at G and V , respectively. Therefore, $D I C _ { v }$ and $G V C$ help maintain forward secrecy, whose prior verifications are required to establish a secure session in each authentication.

3) Untraceability: Since $D I C _ { v }$ is verified based on $R _ { v }$ and $N _ { v } .$ , an adversary cannot use $D I C _ { v }$ of $V .$ v. Due to the freshness v vof these values in a new mutual authentication process, the same values cannot be reused in seccessive secure session establishments. Thus, the untraceability of UAVs and authentication parameters are ensured.

4) Clock Synchronization Avoidance: Timestamps are not used by SwarmAuth. Therefore, it can avoid clock synchronization issues and the time delay in message transmissions.

5) Secure Key Agreement: The secrecy of $N _ { v }$ and $R _ { v }$ is v vproved in Section VI-A, and these parameters are used to verify

TABLE IICOMPARISON OF BASELINE MECHANISMS
<table><tr><td rowspan=1 colspan=1>Item</td><td rowspan=1 colspan=1>Contributions</td><td rowspan=1 colspan=1>UAV-GSAuthenti-cation</td><td rowspan=1 colspan=1>MutualAuthentication</td><td rowspan=1 colspan=1>UAV Swarms</td><td rowspan=1 colspan=1>Blockchain</td><td rowspan=1 colspan=1>PUFs</td><td rowspan=1 colspan=1>IntelligentUAV ClusterFormation</td></tr><tr><td rowspan=1 colspan=1>[2]</td><td rowspan=1 colspan=1>Proposes a blockchain-enableddistributed authentication solu-tion,which deals with messageauthentication and key agree-ment for industrial UAVs.</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>[6]</td><td rowspan=1 colspan=1>Designs  an  authenticationmechanism for UAV swarms,which supports spanning tree-based traversal for multi-hopcommunications.</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>[12]</td><td rowspan=1 colspan=1>Presents a PUF-based authen-ticationprotocol forsecurecommunications between basestations and UAVs in UAVswarms.</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>[26]</td><td rowspan=1 colspan=1>Proposes a PUF-based authen-tication and attestation schemefor UAV swarms using an opti-mal trajectory approach.</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1>Proposesablockchain-basedauthentication    mechanism,which particularlyaddressesthe cross-domain authenticationfor 5G-enabled UAVs.</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>SwarmAuth</td><td rowspan=1 colspan=1>Proposes a blockchain-basedauthentication mechanism forUAV swarms,where the GSCand UAVs follow a mutualauthentication approach usingPUFs,and the K-means cluster-ing scheme is used to dynami-cally create location-based clus-ters.</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr></table>

$S K C _ { v }$ at V before using the generated $S K _ { v } .$ . Thus, based on $S K C _ { v }$ v, the key agreement is securely maintained.

v6) Resistance to Common Attacks: Since the PUF is hardware-specific, it cannot be accessed by A. Thus, V cannot be masqueraded by A, leading to the failure of masquerade attacks. Due to the encrypted transmission of $R _ { v }$ and $N _ { v } .$ , they are good vsecrets between G and V (proved in Section $\mathrm { V I - A } )$ , which helps prevent man-in-the-middle attacks. In each authentication approach, a new $T I D _ { v }$ is generated, and a new $\left( C _ { v } , R _ { v } \right)$ pair, $N _ { v }$ , and $D I C _ { v }$ are used. Consequently, based on old values of these parameters, messages cannot be decoded and replay attacks are prevented. If a device is captured by A, the aforementioned parameters cannot be accessed because they are not stored in V âs or $G \mathrm { ' s }$ databases. Moreover, since PUFs are inherently unclonable, A cannot clone V . Therefore, SwarmAuth is secure against node tampering and cloning attacks.

7) User Anonymity: $T I D _ { v }$ and $D I C _ { v }$ are updated in each v vnew authentication procedure, and the update is based on $C _ { v }$ $N _ { v }$ , and $R _ { v }$ v. Thus, SwarmAuth guarantees user anonymity for v vevery fresh authentication.

## VII. PERFORMANCE EVALUATION

In this section, we present a comparative analysis of SwarmAuth and related schemes, such as the mechanisms proposed by Tan et al. [2], Bansal et al. [12], Gaurang et al. [26], Feng et al. [20], and Bansal et al. [6]. In this context, we consider the computation and communication overheads, along with different security features.

## A. Baseline Mechanisms

The authors in [2] design a blockchain-enabled authentication mechanism for industrial UAVs. The blockchain peer nodes maintain a ledger that stores authentication information, and using APIs, UAVs execute smart contracts to facilitate the authentication process, which applies elliptic curve cryptography. Considering a group of UAVs, the authors in [12] propose an authentication protocol for the communication between base stations and UAVs. Based on the UAVsâ locations, UAV clusters are formed using the K-Means clustering scheme, which helps reduce the message propagation time. In [20], a blockchainbased cross-domain authentication mechanism is proposed for 5G-enabled drones, where the identity of UAVs is dynamically managed using a multi-signature-based smart contract. In that work, the authors design a digital identity credential for UAVs. The work in [26] proposes a PUF-based mutual authentication and attestation protocol for UAV swarms with base stations. In that work, based on an optimal messaging path, a Christofides algorithm is used to find an optimal trajectory to attain scalability. In [6], the authors design a PUF-based mutual authentication protocol for UAV swarm networks, where a spanning tree-based traversal is used to support multi-hop communication and dynamic topologies considering mobile UAVs. Table II presents a comparison of baseline mechanisms with our approach. In the proposed blockchain-based authentication mechanism, both UAV registration and authentication are performed using the blockchain, which stores the information related to the UAV registration. Therefore, both the GSC and the UAV can use untampered information for their mutual authentication.

TABLE III  
SECURITY FEATURES COMPARISON
<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=2>Tan et al. [2]</td><td rowspan=1 colspan=2>Bansal et al. [12]</td><td rowspan=1 colspan=2>Gaurang et al. [26]</td><td rowspan=1 colspan=2>Feng et al. [20]</td><td rowspan=1 colspan=2>Bansal et al. [6]</td><td rowspan=1 colspan=2>SwarmAuth</td></tr><tr><td rowspan=1 colspan=1>Mutual authentication</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Secure key agreement</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Avoidanceof clock synchronization</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Confidentiality</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Forward secrecy</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Useranonymity</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Man-in-the-middleattacks</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Masqueradeattacks</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Replayattacks</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Node tamperingattacks</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Cloning attacks</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=2>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Untraceability property</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>Ã</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1></td></tr></table>

## B. Security Features Comparison

The security feature comparison is presented in Table III, where $\cdot _ { \sqrt { } } ,$ represents the satisfaction of a criterion, and $\mathbf { \nabla } \cdot \mathbf { { \boldsymbol { x } } } ^ { * }$ denotes that the corresponding criterion is not fulfilled by the mechanism. From Table III, it is noted that SwarmAuth provides superior security features than baselines. SwarmAuth and baselines protect against common attacks, such as man-in-themiddle, masquerade, replay, and node tampering attacks. The mutual authentication is not satisfied by the scheme in [12]. The secure key agreement and forward secrecy are satisfied by SwarmAuth and [2]. Apart from [20], other baselines and SwarmAuth use PUFs and thus can guard against node tampering and cloning attacks. The clock synchronization avoidance feature, user anonymity, and untraceability property are failed by all the baselines.

## C. Computation Cost Comparison

Let $T _ { a } , T _ { e }$ , and $T _ { h }$ define the notations of computing analog extractor operations, encryption/decryption, and hash operations, respectively. The costs $\mathrm { ) f } T _ { a } , T _ { e }$ , and $T _ { h }$ are taken from the a e hworks in [37], [38], [39]. Considering the experimental results given in [37], [38], [39], we have $T _ { a } \approx 2 . 0 4 5$ ms, $T _ { e } \approx 8 . 7$ ms, and $T _ { h } \approx 0 . 5 \ : \mathrm { m s }$

hConsidering the authentication process, Table IV highlights the computational cost of SwarmAuth and baselines. In that table, it is noted that SwarmAuth has a lower cost than other baselines. In SwarmAuth, G and V need to perform $4 T _ { h } + T _ { e }$ and $5 T _ { h } + T _ { e }$ operations, respectively, which yields a total cost of $9 T _ { h } + 2 T _ { e }$ operations, i.e., 21.9 ms. In this context, $T _ { e }$ is associh e eated with the authentication for the group message transmission. For [2], the numbers of hash $( T _ { h } )$ and encryption/decryption $( T _ { e } )$ h operations are 4 and 3, respectively, which are primarily associated with the authentication and key agreement, and thus the computation cost is 38.3. The mechanisms in [12] and [26] do not use hash functions and their computation cost is 34.8 ms, which primarily depends on the encryption/decryption. In [20], the sum of session key negotiation and intra-domain authentication cost is 88 ms. Considering the authentication and attestation for a UAV, the computation cost in [6] is based on hash and encryption/decryption operations.

TABLE IV  
COMPUTATION COST COMPARISON
<table><tr><td>Scheme</td><td>UAV</td><td>GSC</td><td>Total cost</td></tr><tr><td>SwarmAuth</td><td> $5 T _ { h } + T _ { e }$   $\approx 1 1 . 2$ </td><td> $\overline { { 4 T _ { h } + T _ { e } } }$   $\approx 1 0 . 7$ </td><td> $\overline { { 9 T _ { h } + 2 T _ { e } } }$   $\approx 2 1 . 9 ~ \mathrm { m s }$ </td></tr><tr><td>Tan et al. [2]</td><td> $\overline { { 7 T _ { h } + 4 T _ { e } } }$  ~38.3</td><td></td><td> $7 T _ { h } + 4 T _ { e }$   $\approx 3 8 . 3 ~ \mathrm { m s }$ </td></tr><tr><td>Bansal et al. [12]</td><td> $\overline { { 2 T _ { e } } }$  ~ 17.4</td><td> $\overline { { 2 T _ { e } } }$  ~17.4</td><td> $\overline { { 4 { T _ { e } } } }$  ~ 34.8 ms</td></tr><tr><td>Gaurang et al. [26]</td><td> $\overline { { 2 T _ { e } } }$  ~ 17.4</td><td> $\overline { { 2 T _ { e } } }$  ~ 17.4</td><td> $\overline { { 4 T _ { e } } }$   $\approx 3 4 . 8 ~ \mathrm { m s }$ </td></tr><tr><td>Feng et al. [20]</td><td> $\overline { { 2 T _ { h } + 1 0 T _ { e } } }$  ~88</td><td>1</td><td> $\overline { { 2 T _ { h } + 1 0 T _ { e } } }$   $\approx 8 8 ~ \mathrm { m s }$ </td></tr><tr><td>Bansal et al. [6]</td><td> $\overline { { 2 T _ { e } } }$  ~ 17.4</td><td> $\overline { { T _ { h } + 2 T _ { e } } }$  ~17.9</td><td> $\overline { { T _ { h } + 4 T _ { e } } }$   $\approx 3 5 . 3 \mathrm { m s }$ </td></tr></table>

TABLE V

COMMUNICATION COST COMPARISON
<table><tr><td>Scheme No. of messages</td><td>No.of bits</td></tr><tr><td>SwarmAuth 2</td><td>480</td></tr><tr><td>Tan et al. [2] 3</td><td>1088</td></tr><tr><td>Bansal et al. [12] 2</td><td>992</td></tr><tr><td>Gaurang et al. [26] 2</td><td>576</td></tr><tr><td>Feng et al. [20] 6</td><td>1056</td></tr><tr><td>Bansal et al. [6] 2</td><td>416</td></tr></table>

## D. Communication Cost Comparison

In order to calculate the communication cost in the UAV authentication, we consider that the hash output, identity, random nonce, and each of the PUF challenge and response contain 160, 160, 128, and 128 bits, respectively. To compute the hash, we apply secure hash algorithm (SHA-1) [40]. For baselines, the elliptic curve cryptography (ECC) point, ciphertext block (using the AES-128), and timestamp contain 320, 128, and 32 bits, respectively. Table V represents the communication cost of our and baseline mechanisms.

In SwarmAuth, during the authentication of a UAV, the total number of communicated messages is 2. The first $\langle T I D _ { v } \rangle$ and the second $\langle G V C , S K C _ { v } \rangle$ messages require 160 and $1 6 0 +$ v160 = 320 bits, respectively, and thus our approach has a total communication cost of 480 bits. From Table V, it is noted that the mechanism in [2] has the highest communication cost. Although the scheme in [6] has the lowest communication overhead, it does not use any hash operation, which is useful to verify the correct reception of a message. The mechanism proposed in [20] requires the largest number of message communications.

TABLE VI  
TIME COST OF APIS IN THE SMART CONTRACT
<table><tr><td rowspan=2 colspan=1>SmartcontractAPIs</td><td rowspan=1 colspan=3>Average time (s)</td></tr><tr><td rowspan=1 colspan=1>4blockchainnodes</td><td rowspan=1 colspan=1>6blockchainnodes</td><td rowspan=1 colspan=1>8blockchainnodes</td></tr><tr><td rowspan=1 colspan=1>saveSI</td><td rowspan=1 colspan=1>1.2</td><td rowspan=1 colspan=1>1.8</td><td rowspan=1 colspan=1>2.1</td></tr><tr><td rowspan=1 colspan=1>deleteSI</td><td rowspan=1 colspan=1>1.14</td><td rowspan=1 colspan=1>1.62</td><td rowspan=1 colspan=1>2.12</td></tr><tr><td rowspan=1 colspan=1>updateSI</td><td rowspan=1 colspan=1>1.1</td><td rowspan=1 colspan=1>1.6</td><td rowspan=1 colspan=1>1.9</td></tr><tr><td rowspan=1 colspan=1>queryPQ</td><td rowspan=1 colspan=1>0.664</td><td rowspan=1 colspan=1>0.667</td><td rowspan=1 colspan=1>0.669</td></tr><tr><td rowspan=1 colspan=1>queryDIC</td><td rowspan=1 colspan=1>0.684</td><td rowspan=1 colspan=1>0.686</td><td rowspan=1 colspan=1>0.687</td></tr></table>

## E. Evaluation of Blockchain on Ethereum Virtual Machine

We implement the proposed blockchain in Truffle, which is a popular blockchain development and testing framework using the Ethereum Virtual Machine (EVM). The blockchain peer nodes are hosted on the cloud server. First, we compute the time cost of the smart contract APIs, which are designed in SwarmAuth. Second, we test the permission scheme of our blockchain-based authentication service, which is crucial because it can directly impact the security feature of the system. Each API is executed 50 times, and Table VI shows the results of the APIsâ computing time. For the consensus algorithm, kafka is used. To meet the endorsement policy, each transaction proposal needs to be endorsed by a minimum of 50% of the blockchain nodes. Since saveSI, deleteSI, and updateSI APIs involve modifications of the SIL, they are recorded in transactions, which are packaged into blocks, then all UAVs are informed about the modification of the SIL. However, queryP Q and queryDIC APIs only query the SIL and do not create any new block. As a result, the average time of saveSI, deleteSI, and updateSI is higher than queryP Q and queryDIC, as shown in Table VI. In SwarmAuth, in order to prepare the next authentication session, a UAV can call the APIs to update its own record after each current authentication session. Thus, during the authentication phase, it is not required for UAVs to wait for the results of the smart contract execution.

The performance of the blockchain network depends on the time cost of the smart contract APIs. If the number of blockchain nodes increases, the number of traffic to access the blockchain nodes also increases. Consequently, the number of executions of the smart contract APIs increases, which can impact the average time cost of the APIs and thus the performance of the blockchain. In order to evaluate the performance of the blockchain network, we have computed the time cost of the smart contract APIs with different number of blockchain peer nodes, and the results are shown in Table VI. From this table, it is noted that, as the number of peer nodes in the blockchain increases, the time costs of saveSI, deleteSI, and updateSI increase compared to queryP Q and queryDIC. This is because saveSI, deleteSI, and updateSI APIs modify SIL, which involves recording transactions, packaging into blocks, and informing all UAVs about the update of SIL. Whereas, queryP Q and queryDIC APIs only query SIL and do not generate any new blocks. Therefore, if the number of UAVs increases, the number of blockchain nodes can be increased. However, as a result, the average time cost of the smart contract APIs will be higher.

In case of the permission scheme evaluation, only the GSC can add a new UAV or delete an existing UAV to/from the blockchain. Fig. 9(a) shows the scenarios where the GSC successfully adds a new UAV UAV1. The validate_id variable is first used to validate the user. When the value of validate_id is âGSCâ, validate_id represents the GSC. Thus, the details of UAV1 can be successfully added. In Fig. 9(b), the value of validate_id is âUAV1â, i.e., a UAV, which sends a proposal to add another UAV UAV2. Thus, the proposal fails to execute and UAV1 gets an error message. A UAV can only update its own information in the SIL, as illustrated in Fig. 10(a), where UAV1 modifies its record. Since a UAV does not have the permission to update the record of another UAV, UAV1 cannot update UAV2âs information, as shown in Fig. 10(b). In this context, UAV1 sends a transaction proposal to blockchain nodes to modify UAV2âs record; however, the permission is denied.

## F. Simulation Scenario

We implement SwarmAuth in NS-3.36 [31] with a 5 GHz IEEE 802.11ac network. We set the area of the simulation to a 500 Ã 500 Ã 300m region, with one GSC and several swarms of UAVs, where the GSC is placed at the center of the region. In particular, n is the total number of UAVs in the network. In the simulation, we consider 500 UAVs. In the simulation, we consider 500 UAVs, and we create multiple clusters dynamically, where each cluster has a maximum number of 10 UAVs. In the performance analysis of SwarmAuth, we show the results of a single cluster among the multiple clusters formed in the simulation. The results are the average performances of the UAVs in a cluster. The UAVs fly within {[0, 500], [0, 500], [0, 300]} at a maximum speed of 50 m/s. The analysis of the throughput performance is based on the UDP throughput. The duration of each simulation experiment is 100s, and each experiment is run 10 times. Thus, results are computed as an average of 10 runs. Table VII presents the simulation parameters with their values.

## G. Communication and Computation Cost Analysis Under Different Cluster Size

From Tables IV and V, the communication and computation costs are reduced in SwarmAuth; however, the costs increase as the cluster size increases, as shown in Fig. 11. When the number of UAVs is 10, SwarmAuth has lower overheads than the schemes proposed in [2], [12], [26], and [20]. Specifically, SwarmAuth has approximately 38%, 37%, 27%, and 3.70% less communication cost than the schemes proposed in [2], [12], [20], and [26], respectively. As given in Table IV, SwarmAuth has marginally higher communication overhead than that of Bansal et al. [6]. As a result, the communication cost in SwarmAuth is approximately 4% higher than that of the work in [6].

<!-- image-->

(b) UAV1 does not have permission to add UAV2  
<!-- image-->  
Fig. 9. (a) GSC successfully adds UAV1 (b) UAV1 does not have permission to add UAV2.

(a) UAV1 can update its own record  
<!-- image-->

(b) UAV1 cannot update UAV2's record  
<!-- image-->  
Fig. 10. (a) UAV1 can update its own record (b) UAV1 cannot update UAV2âs record.

TABLE VII SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Area</td><td rowspan=1 colspan=1>500mÃ500mÃ300m</td></tr><tr><td rowspan=1 colspan=1>Wirelessstandard</td><td rowspan=1 colspan=1>IEEE 802.11ac</td></tr><tr><td rowspan=1 colspan=1>Channel bandwidth</td><td rowspan=1 colspan=1>40MHz</td></tr><tr><td rowspan=1 colspan=1>Dataand control mode</td><td rowspan=1 colspan=1>Constant ratewifi manager</td></tr><tr><td rowspan=1 colspan=1>Maximumphysical datarate</td><td rowspan=1 colspan=1>41 Mbps</td></tr><tr><td rowspan=1 colspan=1>Path loss model</td><td rowspan=1 colspan=1>Log-normalpath loss model(path loss exponent=3.0)</td></tr><tr><td rowspan=1 colspan=1>Propagation delay model</td><td rowspan=1 colspan=1>Constant speed propagation de-lay model</td></tr><tr><td rowspan=1 colspan=1>Mobility model</td><td rowspan=1 colspan=1>Random walk 2dmobilitymodel (&quot;Mode:Time&quot;,&quot;Time:2s&quot;,&quot;Bounds: Rectangle (0, 500, 0,500)&quot;,&quot;Speed:UniformRandom-Variable[Min=2.0,   Max=4.0]&quot;,&quot;Direction:UniformRandomVari-able[Min=0.0,Max=6.283184]&quot;)</td></tr><tr><td rowspan=1 colspan=1>UAVs&#x27;maximumtransmitpower</td><td rowspan=1 colspan=1>5W</td></tr><tr><td rowspan=1 colspan=1>Noise power</td><td rowspan=1 colspan=1>-110 dBm</td></tr><tr><td rowspan=1 colspan=1>Noise power spectral</td><td rowspan=1 colspan=1>-170 dBm/Hz</td></tr></table>

<!-- image-->

<!-- image-->  
Fig. 11. Impact of cluster size on: (a) Communication cost and (b) Computation cost.

In our mechanism, the computation overheads are approximately 31%, 16%, 14%, 11%, and 7.27% lower than that of [2], [6], [12], [20], and [26], respectively. This is because the computation overheads of the authentication related operations are higher in baselines than SwarmAuth. Since the work in [18] tries to reduce the computational cost of the authentication approach, we also compare the communication and computation costs of SwarmAuth with the scheme proposed in [18]. From Fig. 11, it is noted that our SwarmAuth has approximately 32% and 13% lower communication and computational overheads than that of [18], respectively. This is because the scheme in [18] runs three authentication related algorithms.

In Fig. 11, the communication and computation costs are computed under different numbers of UAVs in a cluster, where a UAV can join or leave the cluster dynamically. Since we consider a maximum of 10 UAVs in a cluster, the number of UAVs varies from 1 to 10 in Fig. 11. Therefore, this figure captures the impact of dynamically changing the number of UAVs in a cluster on the performance of SwarmAuth.

## H. Throughput and Delay Analysis

The throughput analysis is shown in Fig. 12(a). The throughput of SwarmAuth is approximately 23.46%, 8.17%, 21.04%, and 10.52% higher than that of Tan et al. [2], Bansal et al. [12], Gaurang et al. [26], and Feng et al. [20], respectively. This is because the communication cost of SwarmAuth is lower than that of the aforementioned baselines, as shown in Table V. As shown in Fig. 12(b), the delay in SwarmAuth is approximately 8%, 3.85%, 3.22%, and 13.83% lower than the delays in Tan et al. [2], Bansal et al. [12], Gaurang et al. [26], and Feng et al. [20], respectively. Since small sized messages are used in SwarmAuth, the delay is reduced in the proposed mechanism. Since the mechanism proposed in Bansal et al. [6] has marginally lower communication cost than SwarmAuth, the average throughput and delay in [6] are approximately 2% higher and 0.48% lower than that of SwarmAuth, respectively.

<!-- image-->

<!-- image-->  
Fig. 12. (a) Average throughput and (b) Average delay.

<!-- image-->

<!-- image-->  
Fig. 13. Impact of number of clusters on: (a) Communication cost and (b) Computation cost.

## I. Impact of Dynamic Cluster Formation on Network Performance

In order to analyze the impact of the dynamic cluster formation on the performance of SwarmAuth, we consider 5 clusters and compute the average communication and computation costs, throughput, and delay of the 5 clusters in the network. Since the works in [2], [6], [12], and [26] consider multiple clusters of UAVs, we include these baselines in the performance analysis of the dynamic cluster formation.

1) Communication and Computation Cost Analysis Under Different Number of Clusters: From Fig. 13, it is noted that when multiple clusters are considered to compute the average communication and computation costs in the network, these average costs increase as the number of clusters increases. However, since SwarmAuth uses a K-means clustering-based intelligent approach to dynamically form clusters, our proposed mechanism has lower costs than baselines. For instance, when the number of clusters is 5, SwarmAuth has approximately 14%, 26%, 28%, and 40% lower average communication cost than that of the works in [6], [12], [26], and [2], respectively, as shown in Fig. 13(a). In the case of the computation overhead, in SwarmAuth, the average computation cost is approximately 15%, 22%, 24%, and 34% lower than that of the works in [6], [12], [26], and [2], respectively, as shown in Fig. 13(b). The works in [6] and [26] do not use any learning-based approach for the dynamic cluster creation. The work in [2] does not deal with dynamic cluster formation. Although the work in [12] uses a K-means clustering scheme for the cluster creation, the impact of the UAVâs movement on the recomputation of the cluster center is not included in the cluster update.

<!-- image-->

<!-- image-->  
Fig. 14. (a) Communication cost distribution and (b) Computation cost distribution.

2) Communication and Computation Cost Distribution: In order to analyze the impact of the UAVsâ high mobility on the stability of the clusters, we run the simulation for 200 continuous iterations considering 5 clusters and calculate the average communication and computation costs in the network after each iteration. Then, we compute the cumulative distribution function (CDF) of the average communication and computation costs, and the results are shown in Fig. 14. Since our simulation scenario (Section VII-F) emulates a practical environment, Fig. 14 captures the performance of SwarmAuth in practical scenarios. In Fig. 14, it is noted that SwarmAuth has higher CDFs of the aforementioned costs than baselines. In SwarmAuth, the cluster centers are updated based on the number of UAVs in a cluster and the positions of the UAVs. That approach helps reconstruct clusters dynamically when there is a change in the number of UAVs in a cluster.

Moreover, when a UAV travels further than a distance of dmin , p cvthe distance between the UAV and the corresponding cluster center is recomputed. Consequently, when a UAV travels less than or equal to a distance of $d _ { c v _ { v } } ^ { m i n }$ , a cluster is not affected cvby the frequent movement of the UAV. As a result, a balance is maintained between the stability of a cluster and the high mobility of the UAVs. Thus, SwarmAuth uses a better adaptive cluster formation approach than the work in [12]. Fig. 14(a) shows that, in SwarmAuth, the density of the communication cost spans through 7 â 14 kbits; whereas, in baselines, the distributions are high in the 9 â 15 kbits range. From Fig. 14(b), it is noted that the density of the computation cost of SwarmAuth is high in the 250 â 500 ms range. In that case, baselines have high CDFs in the 350 â 600 ms range.

3) Throughput and Delay Analysis Under Different Number of Clusters: Fig. 15 shows the average throughput and delay analysis under different number of clusters in the network. For instance, when the number of clusters is 5 in Fig. 15(a), the average throughput of SwarmAuth is approximately 8.59%, 14.34%, 23.13%, and 66.25% higher than that of Bansal et al. [12], Gaurang et al. [26], Bansal et al. [6], and Tan et al. [2], respectively. This is because, under a higher number of clusters, the average communication cost of SwarmAuth is lower than that of the aforementioned baselines, as shown in Fig. 13(a). Similarly, due to the lower average computation cost in SwarmAuth (shown in Fig. 13(b)), the average delay in SwarmAuth is approximately 6.7%, 11.1%, 16.87%, and 25.8% lower than the delays in Bansal et al. [12], Gaurang et al. [26], Bansal et al. [6], and Tan et al. [2], respectively, as shown in Fig. 15(b).

<!-- image-->

<!-- image-->  
Fig. 15. (a) Average throughput and (b) Average delay.

## VIII. CONCLUSION

SwarmAuth uses a blockchain-based distributed mechanism to provide a UAV authentication service for UAV swarms, where the authentication approach imposes a PUF-based mutual authentication between the GSC and a UAV. The ledger maintained by the blockchain peer nodes stores authentication information, and the smart contract APIs control the access to the ledger to perform trustworthy operations facilitating the UAV authentication process. Moreover, considering the locations of UAVs, the K-means clustering scheme helps dynamically create UAV clusters, and consequently the overall network performance is improved. Both formal verfication and informal proofs of SwarmAuth are proved considering general attacks. To analyze the practical impact of SwarmAuth, we implement the proposed blockchain in Truffle-based EVM, and SwarmAuth is evaluated through simulations, where the results show the effectiveness of SwarmAuth for UAV swarms and its superior performance compared to baselines. In our future work, we shall add intelligent cross-domain authentication to further improve the security of UAV swarms.

## ACKNOWLEDGMENTS

Any opinions and conclusions in this work are strictly those of the author(s) and do not reflect the views, positions, or policies of-and are not endorsed by-IDEaS, DND, or the Government of Canada.

## REFERENCES

[1] H. Shakhatreh et al., âUnmanned aerial vehicles (UAVs): A survey on civil applications and key research challenges,â IEEE Access, vol. 7, pp. 48 572â48 634, 2019.

[2] Y. Tan, J. Wang, J. Liu, and N. Kato, âBlockchain-assisted distributed and lightweight authentication service for industrial unmanned aerial vehicles,â IEEE Internet Things J., vol. 9, no. 18, pp. 16928â16940, Sep. 2022.

[3] Y. Yan, Y. Qian, H. Sharif, and D. Tipper, âA survey on cyber security for smart grid communications,â IEEE Commun. Surveys Tuts., vol. 14, no. 4, pp. 998â1010, Fourth Quarter 2012.

[4] J. Srinivas, A. K. Das, N. Kumar, and J. J. Rodrigues, âTCALAS: Temporal credential-based anonymous lightweight authentication scheme for Internet of drones environment,â IEEE Trans. Veh. Technol, vol. 68, no. 7, pp. 6903â6916, Jul. 2019.

[5] D. Wang, P. Wang, C.-G. Ma, and Z. Chen, âRobust smart card based password authentication scheme against smart card security breach,â Cryptol. ePrint Arch., 2012.

[6] G. Bansal and B. Sikdar, âS-MAPS: Scalable mutual authentication protocol for dynamic UAV swarms,â IEEE Trans. Veh. Technol, vol. 70, no. 11, pp. 12 088â12 100, Nov. 2021.

[7] M. Gharibi, R. Boutaba, and S. L. Waslander, âInternet of drones,â IEEE Access, vol. 4, pp. 1148â1162, 2016.

[8] Y. Sun, J. Liu, K. Yu, M. Alazab, and K. Lin, âPMRSS: Privacypreserving medical record searching scheme for intelligent diagnosis in IoT healthcare,â IEEE Trans. Ind. Inform., vol. 18, no. 3, pp. 1981â1990, Mar. 2022.

[9] G. Bansal, N. Naren, V. Chamola, B. Sikdar, N. Kumar, and M. Guizani, âLightweight mutual authentication protocol for V2G using physical unclonable function,â IEEE Trans. Veh. Technol, vol. 69, no. 7, pp. 7234â7246, Jul. 2020.

[10] M. Zhaofeng, W. Lingyun, W. Xiaochang, W. Zhen, and Z. Weizhe, âBlockchain-enabled decentralized trust management and secure usage control of IoT big data,â IEEE Internet Things J., vol. 7, no. 5, pp. 4000â4015, May 2020.

[11] T. Jiang, H. Fang, and H. Wang, âBlockchain-based internet of vehicles: Distributed network architecture and performance analysis,â IEEE Internet Things J., vol. 6, no. 3, pp. 4640â4649, Jun. 2019.

[12] G. Bansal and B. Sikdar, âLocation aware clustering: Scalable authentication protocol for UAV swarms,â IEEE Netw. Lett., vol. 3, no. 4, pp. 177â180, Dec. 2021.

[13] K. Ranjitha, D. Pathak, P. Tammana, A. Franklin A, and T. Alladi, âAccelerating PUF-based UAV authentication protocols using programmable switch,â in Proc. 14th Int. Conf. Commun. Syst. Netw., 2022, pp. 309â313.

[14] H. Wang, H. Fang, and X. Wang, âSafeguarding cluster heads in UAV swarm using edge intelligence: Linear discriminant analysis-based crosslayer authentication,â IEEE Open J. Commun. Soc., vol. 2, pp. 1298â1309, 2021.

[15] T. Alladi, Naren, G. Bansal, V. Chamola, and M. Guizani, âSecAuthUAV: A novel authentication scheme for UAV-ground station and UAV-UAV communication,â IEEE Trans. Veh. Technol, vol. 69, no. 12, pp. 15 068â15 077, Dec. 2020.

[16] B. Semal, K. Markantonakis, and R. N. Akram, âA certificateless group authenticated key agreement protocol for secure communication in untrusted UAV networks,â in Proc. IEEE/AIAA 37th Digit. Avionics Syst. Conf., 2018, pp. 1â8.

[17] M. Yahuza, M. Y. I. Idris, A. W. A. Wahab, T. Nandy, I. B. Ahmedy, and R. Ramli, âAn edge assisted secure lightweight authentication technique for safe communication on the internet of drones network,â IEEE Access, vol. 9, pp. 31 420â31 440, 2021.

[18] H. Wang, H. Fang, and X. Wang, âEdge intelligence enabled soft decentralized authentication in UAV swarm,â in Proc. IEEE/CIC Int. Conf. Commun. China, 2021, pp. 86â91.

[19] X. Lan, X. Tang, D. Zhai, D. Wang, and Z. Han, âBlockchain-secured data collection for UAV-Assisted IoT: A DDPG approach,â in Proc. IEEE Glob. Commun. Conf., 2021, pp. 1â6.

[20] C. Feng, B. Liu, Z. Guo, K. Yu, Z. Qin, and K.-K. R. Choo, âBlockchain-based cross-domain authentication for intelligent 5Genabled internet of drones,â IEEE Internet Things J., vol. 9, no. 8, pp. 6224â6238, Apr. 2022.

[21] G. Li, B. He, Z. Wang, X. Cheng, and J. Chen, âBlockchain-enhanced spatiotemporal data aggregation for UAV-assisted wireless sensor networks,â IEEE Trans. Ind. Inform., vol. 18, no. 7, pp. 4520â4530, Jul. 2022.

[22] A. Aftab, N. Ashraf, H. K. Qureshi, S. A. Hassan, and S. Jangsher, âBLOCK-ML: Blockchain and machine learning for UAV-BSs deployment,â in Proc. IEEE 92nd Veh. Technol. Conf., 2020, pp. 1â5.

[23] Y. Wang, Z. Su, Q. Xu, R. Li, and T. H. Luan, âLifesaving with RescueChain: Energy-efficient and partition-tolerant blockchain based secure information sharing for UAV-aided disaster rescue,â in Proc. IEEE INFO-COM, 2021, pp. 1â10.

[24] I. J. Jensen, D. F. Selvaraj, and P. Ranganathan, âBlockchain technology for networked swarms of unmanned aerial vehicles (UAVs),â in Proc. IEEE 20th Int. Symp. âA World Wireless Mobile Multimedia Netw.â, 2019, pp. 1â7.

[25] S. Sahoo, A. K. Shukla, and H. Rana, âFuture directions of UAV swarm communications,â in Proc. 8th Int. Conf. Signal Process. Integr. Netw., 2021, pp. 324â327.

[26] G. Bansal, N. Naren, V. Chamola, and B. Sikdar, âSHOTS: Scalable secure hardware based authentication-attestation protocol using optimal trajectory in UAV swarms,â IEEE Trans. Veh. Technol, vol. 71, no. 6, pp. 5827â5836, Jun. 2022.

[27] K. Gai, Y. Wu, L. Zhu, K.-K. R. Choo, and B. Xiao, âBlockchain-enabled trustworthy group communications in UAV networks,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 7, pp. 4118â4130, Jul. 2021.

[28] G. Raja, S. Anbalagan, A. Ganapathisubramaniyan, M. S. Selvakumar, A. K. Bashir, and S. Mumtaz, âEfficient and secured swarm pattern multi-UAV communication,â IEEE Trans. Veh. Technol, vol. 70, no. 7, pp. 7050â7058, Jul. 2021.

[29] W. Mao and C. Boyd, âTowards formal analysis of security protocols,â in Proc. Comput. Secur. Found. Workshop VI, 1993, pp. 147â158.

[30] The scyther tool, 2016. Accessed: May 10, 2022. [Online]. Available: https://people.cispa.io/cas.cremers/scyther/

[31] Ns-3.36 - nsnam. [Online]. Available: https://www.nsnam.org/releases/ ns-3--36

[32] P. Gupta and P. R. Kumar, âThe capacity of wireless networks,â IEEE Trans. Inf. Theory, vol. 46, no. 2, pp. 388â404, Mar. 2000.

[33] K. Xu, X. Hong, and M. Gerla, âAn ad hoc network with mobile backbones,â in Proc. IEEE Int. Conf. Commun., 2002, pp. 3138â3143.

[34] K. Kandali, L. Bennis, and H. Bennis, âA new hybrid routing protocol using a modified K-means clustering algorithm and continuous hopfield network for VANET,â IEEE Access, vol. 9, pp. 47 169â47 183, 2021.

[35] D. Wang, D. He, P. Wang, and C.-H. Chu, âAnonymous two-factor authentication in distributed systems: Certain goals are beyond attainment,â IEEE Trans. Dependable Secure Comput., vol. 12, no. 4, pp. 428â442, Jul./Aug. 2015.

[36] D. Wang, H. Cheng, D. He, and P. Wang, âOn the challenges in designing identity-based privacy-preserving authentication schemes for mobile devices,â IEEE Syst. J., vol. 12, no. 1, pp. 916â925, Mar. 2018.

[37] D. He, N. Kumar, M. K. Khan, and J.-H. Lee, âAnonymous two-factor authentication for consumer roaming service in global mobility networks,â IEEE Trans. Consum. Electron., vol. 59, no. 4, pp. 811â817, Nov. 2013.

[38] Q. Jiang, J. Ma, G. Li, and L. Yang, âAn efficient ticket based authentication protocol with unlinkability for wireless access networks,â Wireless Pers. Commun., vol. 77, no. 2, pp. 1489â1506, 2014.

[39] Y. Lei, L. Zeng, Y.-X. Li, M.-X. Wang, and H. Qin, âA lightweight authentication protocol for UAV networks based on security and computational resource optimization,â IEEE Access, vol. 9, pp. 53 769â53 785, 2021.

[40] S. H. Standard, âFIPS Pub 180-1,â Nat. Inst. Standards Technol., vol. 17, no. 180, p. 15, 1995.

<!-- image-->

Raja Karmakar (Member, IEEE) received the bachelor of technology (BTech) degree in computer science and engineering from the Government College of Engineering and Leather Technology, Kolkata, India, the master of engineering (ME) degree in software engineering from Jadavpur University, Kolkata, India, and the doctor of philosophy (PhD) degree from Jadavpur University, Kolkata, India. Currently, he is an associate professor with the Department of Computer Science and Engineering, Heritage Institute of Technology, Kolkata, India. Prior to that, he was a

postdoctoral research fellow with the Ãcole de Technologie SupÃ©rieure (ÃTS), UniversitÃ© du QuÃ©bec, MontrÃ©al, Canada. His research area includes computer systems, wireless networks, mobile computing, IoT, machine learning, and UAV communications.

<!-- image-->

Georges Kaddoum (Senior Member, IEEE) received the bachelorâs degree in electrical engineering from the Ãcole Nationale SupÃ©rieure de Techniques AvancÃ©s (ENSTA Bretagne), Brest, France, the MS degree in telecommunications and signal processing (circuits, systems, and signal processing) from the UniversitÃ© de Bretagne Occidentale and Telecom Bretagne (ENSTB), Brest, in 2005, and the PhD (honors) degree in signal processing and telecommunications from the National Institute of Applied Sciences (INSA), University of Toulouse, Toulouse, France,

in 2009. He is currently an associate professor and Tier 2 Canada research chair with the Ãcole de Technologie SupÃ©rieure (ÃTS), UniversitÃ© du QuÃ©bec, MontrÃ©al, Canada and associated with Cyber Security Systems and Applied AI Research Center, Lebanese American University, Beirut, Lebanon. In 2014, he was awarded the ÃTS research chair in physical-layer security for wireless networks. Since 2010, he has been a scientific consultant in the field of Space and Wireless Telecommunications for several US and Canadian companies. He has published more than 200+ journal and conference papers and has two pending patents. His recent research activities cover mobile communication systems, modulations, security, and space communications and navigation. He received the Best Papers Awards at the 2014 IEEE International Conference on Wireless and Mobile Computing, Networking, Communications (WIMOB), with three coauthors, and at the 2017 IEEE International Symposium on Personal Indoor and Mobile Radio Communications (PIMRC), with four coauthors. Moreover, he received IEEE Transactions on Communications Exemplary Reviewer Award for the year 2015, 2017, 2019. In addition, he received the research excellence award of the UniversitÃ© du QuÃ©bec in the year 2018. In the year 2019, he received the research excellence award from the ÃTS in recognition of his outstanding research outcomes. He is currently serving as an associate editor of IEEE Transactions on Information Forensics and Security, and IEEE Communications Letters.

<!-- image-->

Ouassima Akhrif (Senior Member, IEEE) received the MSc and PhD degrees in electrical engineering, control systems with the University of Maryland, College Park, USA, in 1987 and 1989, respectively, as a fulbright scholar. After one year as an assistant professor, with the Systems Engineering Department, Case Western Reserve University in Cleveland, she moved to Montreal, Canada, and joined in 1992 the âÃcole de Technologie SupÃ©rieure (ÃTS)â, UniversitÃ© du QuÃ©bec, MontrÃ©al, Canada, where she is currently a full professor with the Electrical Engineering Department. She is a member of GREPCI (Groupe de Recherche en Commande Industrielle et Ãlectronique de Puissance), a research group that she directed from 2004 to 2009. Her research interests include bifurcation analysis, nonlinear geometric control, nonlinear adaptive control and their applications in electric drives, power systems, renewable energy integration, autopilot design, and flight control systems.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_7_img_1.jpeg|page_7_img_1]]
2. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_8_img_1.jpeg|page_8_img_1]]
3. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_9_img_1.jpeg|page_9_img_1]]
4. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_11_img_1.jpeg|page_11_img_1]]
5. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_15_img_1.jpeg|page_15_img_1]]
6. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_15_img_2.jpeg|page_15_img_2]]
7. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_18_img_1.jpeg|page_18_img_1]]
8. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_18_img_2.jpeg|page_18_img_2]]
9. [[../extracted_images/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu/page_18_img_3.jpeg|page_18_img_3]]

---

