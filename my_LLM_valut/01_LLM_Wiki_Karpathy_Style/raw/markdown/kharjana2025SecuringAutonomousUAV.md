# Securing Autonomous UAV Cluster With Blockchain-Based Threshold Key Management System Utilizing Crypto-Asset and Multisignature

Mebanjop Kharjana , Subhas Chandra Sahana , and Goutam Saha

AbstractâUnmanned aerial vehicles deployed in remote locations rely on self-governed key management for their protection. However, conventional key management depends on a centralized ground-based station or single vehicle. Such a system is vulnerable to compromised certificate authority problems and single-pointsof-failure. This paper proposed to resolve these vulnerabilities using a blockchain-based threshold key management system. The proposed system utilized blockchainâs concepts of crypto-asset and multisignature. Keys are defined as crypto-assets to improve their management in the blockchain network. Multisignature facilitates collaboration during key management based on a threshold value. The threshold value is also configurable to meet systemsâ security and performance requirements. The proposed system secured the process of re-enforcement, sub-clustering, re-merging, and intercluster migration. Security analysis revealed that the proposed system complied with most key management security guidelines. The custom signature module used to authenticate intra-cluster communication was also verified as safe. Threats to the cluster were identified, assessed for risk, and mitigated accordingly. Performance analysis found that both AODV and DSDV routing protocols offer consistent performance but DSDV prevailed during the worst-case network scenario. The paper finally identified research gaps, including the requirement for an optimized mechanism for collecting consent signatures.

Index TermsâAutonomous UAV cluster, threshold key management system, blockchain, crypto-asset, multisignature.

## I. INTRODUCTION

U NMANNED aerial vehicle (UAV) is used primarily formilitary applications like real-time surveillance, intelli- military applications like real-time surveillance, intelligence data gathering, high-risk missions, and aerial warfare. It is now used in other broad spectra of civilian applications such as search and rescue operations, wildlife tracking, weather monitoring, pollution control, etc. It is also an innovative technology deployed in clusters to transform the operations of different businesses and industries. Multiple UAVs are inter-connected to form a cluster and cooperate to achieve a common goal. Such a cluster is configured as an underlying network to support various commercial applications, from mapping software to logistics operations. However, different types of attacks [1], [2], [3] on UAVs can affect their hardware, software, and networking operations. Such attacks can significantly disrupt the normal functioning of the UAV cluster and the business operations that rely on it. Therefore, securing the UAV cluster is very important, especially when deployed at remote locations for critical military or civil operations.

The important security aspect of a UAV cluster when operating at a remote location is key management. Key management is used by UAVs to perform (i) identification, (ii) authentication, and (ii) secured communication. The common approach is to designate a single UAV as a centralized certification authority (CA) to manage key information. However, such a CA can be compromised affecting normal key management services. To address this issue, different collaborative key management systems are proposed. Key management systems [4], [5], [6] propose a threshold mechanism based on Shamirâs Secret Sharing (SSS) to secure wireless sensors and other ad-hoc networks. The SSS shares a master key pair across the network with a (k, n) threshold. At least k of the total n shareholders must collaborate to perform key generation service. The threshold technique is also adopted to manage network group keys and prevent attacks from malicious actors. Further, a group key agreement protocol [7] integrates SSS with a modified centralized circular hierarchical (CCH) group model to collect m shares from n mobile nodes to generate and distribute a group key. However, SSS and its extension depend on a centralized party to construct a final key from the collected secrets. If such a party fails or is compromised, it can cause a single-point-of-failure event and even jeopardize the whole system. The current trend to address the issues of compromised CA and single-point-offailure is to use blockchain. Blockchain is a distributed ledger technology used for secured record saving and tracking. Data on the blockchain are transparent and immutable, making it suitable for managing key information. A blockchain ledger is also distributed across the network, enhancing its resilience and resistance to network failures. Distributed authentication services [8], [9] utilize blockchain-based mechanisms to secure UAV networks. They use a blockchain ledger as a distributed and immutable authentication information storage. They also deploy smart contracts as a means to provide authentication services. Shamirâs Secret Sharing is also used in blockchain-based security systems [10], [11] to facilitate threshold key-sharing mechanism. The private key is split into multiple sub-keys based on Shamirâs threshold scheme to prevent any loss and disclosure of the original key. These systems also support authentication and encryption techniques to secure wireless communications.

Recent developments of blockchainâs crypto-assets [12] and tokens [13] introduce new research opportunities. Non-fungible tokens (NFTs) are used by authentication systems [14], [15], [16] to identify users and devices. Token-based identities are unique and immutable, while the underlying blockchain ensures they are shareable and verifiable. NFTs and smart contracts are leveraged by [17] to secure its Public Key Infrastructure (PKI) Ecosystem. While NFTs represent digital assets, smart contracts provide for their execution logic. NFTsâ ownership is established through a digital signature, which is utilized for the authentication process. Similarly, decentralized identities are constructed for digital objects by an identifier management scheme [18]. They are NFT-based identifiers that are managed on the blockchain network using smart contracts. NFT ensures that ownership of digital objects is unique and authentic. Blockchain-based token technology is also used to support Self-Sovereign Identity (SSI) [19] in Metaverse. NFTs are held by users as their unique identifier and manage them independently. NFT with Zero Proof knowledge is used as evidence for trust in the Metaverse. The NFT-based identifier is also used for authentication purposes to access services.

Following the current trend, this paper aims to secure autonomous UAV clusters using a blockchain-based threshold key management system. It fully utilizes advanced blockchain features to (i) further enhance existing key management systems, (ii) address persisting security issues relating to key management, and (iii) design a configurable system that meets different security and performance requirements of UAV applications.

## II. RELATED WORKS

A secure blockchain-based key management scheme [20] was proposed for an autonomous flying ad hoc network (FANET). A head UAV was used to provide key management services and has higher storage and computation capability. Key management was also carried out autonomously without the intervention of the ground station. This was possible as blockchain was used as the trusted key store. The proposed scheme also supported key revocation and UAV migration. The scheme had minimal energy requirements and was proven secure against different security attacks. An authentication model [21] was proposed that leveraged decentralized blockchain-based security. It addressed the issue of low latency during drone authentication in smart city applications. It implemented a zone-based architecture, with each zone managed by a drone controller. The drone controller handled authentication, migration, and secure communication. The drone controller maintained a blockchain ledger and used a customized consensus algorithm of drone-based delegated proof of stake (DDPOS). This proposed model offered a low packet loss rate, high throughput, and low end-to-end delay. A blockchain-based public key infrastructure (PKI) [22] was proposed to perform decentralized authentication for UAV networks. The blockchain stored public keys, identities, and trust relationships as global trust graphs. UAV only stored a part of the blockchain that is relevant to it. Two UAVs combine their knowledge to authenticate and find a trustworthy path in their trust graph. The blockchain also acted as a secured storage and access controller for the trust graph in the PKI. A blockchainbased cross-domain authentication service [23] was proposed for intelligent 5G-enabled internet of drones. It addressed the issue of single-point-of-failure and cross-domain authentication in drone networks. It also supported federated identity for collaborative domains using a multi-party signatures scheme. It facilitated the process of drone joining and exiting between different domains. A smart contract performed cross-domain authentication and established session keys to ensure reliable communication. The system was proven efficient and resistant to security threats. An identity and aggregate signature-based authentication protocol [24] was proposed for the internet of drones. The network consisted of two types of drones, reconnaissance and attacking. These drones communicated with the remote controller through a wireless network or satellite using GPS (Global Positioning System) signals. Two protocols were designed and used to guarantee data integrity, authorization, and confidentiality of communications. Pairing cryptography generated the public-private key pairs for drone identification. The authentication scheme used aggregate signatures to ensure protection against GPS spoofing attacks. Key exchange was performed using the Computational DiffieâHellman Problem (CDHP) [25]. The proposed protocol was verified using a random oracle model (ROM), a real-or-random (ROR) model, and mathematical lemmas.

Alternate approaches were identified in which customized blockchain architectures and features were employed to secure UAV networks. A multi-layered blockchain architecture [26] was designed to manage group keys for an urban UAV network. This hierarchical blockchain structure assisted in determining node mobility and group density. Custom blockchain block and transaction types were used by a task management scheme [27] to maintain identity information and secure task management in a multi-UAV network. It also utilized a special consensus mechanism to accelerate the consensus between the server network and the ground station. NFT was used in DroneXNFT [28] to manage flight data and secure autonomous UAV operations. Further, advanced technologies like deep learning were also integrated with blockchain to devise advanced security frameworks. An intelligent fuzzy blockchain framework [29] utilized novel fuzzy deep learning algorithms to detect network attacks in blockchain-based IoT environments.

## III. MOTIVATION

Investigations revealed that most key management services are centralized which leads to single-point-of-failure. These systems are vulnerable if the centralized authority is compromised. It was noticed that most systems use blockchain only as a storage and distributing medium. The blockchain remained under-utilized with its advanced features not leveraged to address pending key management issues. Moreover, most key management systems depend on fixed infrastructure and are unsuitable when a UAV cluster is deployed to remote locations. These systems are also not configurable to meet the varying security and performance requirements of UAV applications. Based on these observations, research initiatives had been undertaken that focused on the following:

- To design a blockchain-based threshold key management system to secure an autonomous UAV cluster by utilizing advanced features of blockchain.

- To distribute key management authority among multiple entities to resolve the compromised CA problem and the single-point-of-failure event.

- To make key management system configurable to meet varying security and performance requirements.

- To ensure the key management system complies with established security guidelines.

## IV. ORGANIZATION

The rest of the paper is organized as follows. Section V presents an overview of the proposed key management system. Section VI implements the proposed key management system for autonomous UAV clusters. Section VII and Section VIII identify methodologies relating to the security and performance analysis respectively. Section IX discusses results data relating to the security and performance analysis. Section X identifies the future scope of work to improve the proposed key management system. Finally, the paper concludes in Section XI.

## V. METHODOLOGY

This paper proposes a blockchain-based threshold key management system for an autonomous UAV cluster. The proposed system leverages two features of blockchain technology, namely (i) crypto-asset and (ii) multisignature (or multisig). The core idea of the proposal is to treat a key as a crypto-asset. A cryptoasset is bound to a key and assigned a unique asset name at creation time. This asset name identifies the key during different key management operations. A blockchain network is used as a medium to manage and secure keys as crypto-assets. The m-of-n multisignature is then used to entitle ownership and usage rights of the crypto-asset to multiple owners. For this purpose, a redeem script based on Bitcoin [30] is calculated using a threshold value m and the public keys of the n owners. A locking script (also referred to as multisignature) is then constructed from the redeem script. Such m-of-n multisignature implies that the crypto-asset is collectively owned by n owners but consent signatures from at least m owner(s) are required to modify such assets. These m signatures are presented as unlocking script to prove asset ownership and authorized asset modification. The parameter m serves as a (i) functional threshold to facilitate collaborative operations, and (ii) security threshold beyond which malicious actors can collaborate to compromise the system. As shown in Fig. 1, an asset-based certification of a public key is proposed that uses asset name for identification and multisignature for multi-party certification.

The proposed system aims to be configurable to meet different security and performance requirements in a UAV cluster. For this purpose, a M:N:T cluster configuration is defined as shown in Fig. 2. It consists of T number of UAVs. Out of T UAVs, N is identified as Controller UAV (CUAV), and the remaining (T-N) as Worker UAV (WUAV). WUAVs are members entrusted to perform the actual work in the cluster. They have limited computational and storage resources. CUAVs are administrators that control key management operations in the cluster. They have higher computational and storage capabilities. CUAVs hold a copy of the blockchain and maintain consensus with each other. The threshold value M defines the minimum number of CUAVs required to perform asset/key management operations. Moreover, CUAVs are responsible for managing cluster keys and ensuring the confidentiality of cluster communication. Hence, CUAVs form the backbone of key management operations for an autonomous UAV cluster without relying on fixed infrastructure.

<!-- image-->  
Fig. 1. Standard public key vs. Asset-based public key certifications.

<!-- image-->  
Fig. 2. Cluster with M:N:T configuration.

For a cluster with M:N:T configuration, the parameter values are selected based on the following criteria:

$M \leq N \leq T$

- $M > { \frac { 1 } { 2 } } N$ (to prevent a minority group of compromised CUAVs from running malicious parallel operations).

The parameter M directly affects the performance and security of the cluster. Consider cluster configuration where (i) M=1, N=T: All members are of the CUAV type. It offers high performance as only one consent is required, but a single CUAV can compromise the whole cluster, (ii) M=N=1, T=\*: It is equivalent to a centralized system with a single CUAV controlling the cluster. It offers high performance but suffers from lower security, (iii) M=N, T=\*: It suffers from low performance as the consent of all CUAVs is required. It will be non-operational even if one CUAV is compromised, (iv) M=N=T: It consists of only CUAVs and performs poorly as all their consent is required. It will be non-operational even if just one member is compromised.

<!-- image-->  
Fig. 3. Proposed signature module.

TABLE I  
CRYPTOGRAPHIC NOTATIONS
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>hsh{A}</td><td rowspan=1 colspan=1>Hash value of a content A.</td></tr><tr><td rowspan=1 colspan=1>enc{A}kY</td><td rowspan=1 colspan=1>Encrypt content A with a keyKY.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { s i g \{ A \} _ { S Y } } }$ </td><td rowspan=1 colspan=1>Sign content A with private key SY.</td></tr><tr><td rowspan=1 colspan=1>ver{A,B}PY</td><td rowspan=1 colspan=1>Verify signature A withBusingpublic keyPY.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { T X ^ { k } } }$ </td><td rowspan=1 colspan=1>Multisig transaction that received k signatures.</td></tr><tr><td rowspan=1 colspan=1>n</td><td rowspan=1 colspan=1>Nonce value used to prevent replay attacks.e.g.random no.,timestamp,etc.</td></tr></table>

Therefore, parameter values for cluster configuration M:N:T depend on the operation requirement. For performance, the value of M should be lower so that only fewer consents are required to complete a key management operation. For better security, the value of M should be higher so that if a CUAV is compromised, it cannot singly manipulate key information. Moreover, a higher N value ensures that the system can fall back on the support of other CAUVs if a single CUAV is destroyed.

Moreover, the proposed key management system involves intra-cluster communication among UAVs. A custom signature module is proposed to authenticate such communication. As shown in Fig. 3, the custom signature module is divided into the (i) Source Signature Module (SSM) and (ii) Transition Signature Module (TSM). The SSM stores the authentication data of the requester, whereas the TSM stores the authentication data of the latest intermediate participant. In case of a key update operation, ASN1 stores the asset name of the key to be updated. The CON1 field stores the newly generated public key, and SIG1 is a signature calculated from ASN1, CON1, and NON1. Similarly, ASN2 stores the asset name of the key that had last consented to the update request. The CON2 contains the blockchain transaction in hex format, and signature SIG2 is calculated from ASN2, CON2, and NON2. NON1 and NON2 are randomly generated nonce values for preventing replay attacks. Authentication using SSM and TSM is performed as shown in Algorithm 1. Note that the authenticating key is not transmitted with the module but retrieved using its asset name.

Algorithm 1. Verify Signature Modules of Payload   
VALIDATE (P ayload)   
Compute $H S 1  h s h \{ A S 1 , C O N 1 , N O N 1 \}$   
Compute $H S 2  h s h \{ A S 2 , C O N 2 , N O N 2 \}$   
If (ver{SIG1, HS1}P ublic Key(AS1)) and   
(ver{SIG2, HS2}P ublic Key(AS2)) then   
return True   
else   
return False

## VI. IMPLEMENTATION OF BLOCKCHAIN-BASED THRESHOLD KEY MANAGEMENT SYSTEM UTILIZING CRYPTO-ASSET AND MULTISIGNATURE

Different cryptographic functions used are illustrated in Table I. The flow of communication from A to B is represented using the notation of A â B : {P ayload}. The implementation of the blockchain platform is based on the premise of MultiChain. MultiChain is an off-the-shelf private blockchain platform whose application programming interface (APIs) [31] are compatible with those of Bitcoin Core [32]. The proposed system utilizes API commands that include createmultisig, grant, issue, getassetinfo, createrawsendfrom, signrawtransaction and sendrawtransaction. The proposed system can be adapted to other blockchain platforms that support crypto-assets and multisignature (or smart contract) functionalities. Most modern blockchains support these features and the proposed system is deployable on such platforms.

## A. Configure UAV Cluster

For a cluster with M:N:T configuration, CUAV[i] and WAUV[i] represent the $i ^ { t h }$ Controller/Worker UAV, respectively. The ground control station (GCS) pre-configures CUAVs and WUAVs to perform subsequent key management operations autonomously.

1) Setting up Cryptographic Parameters: GCS uses elliptic curve cryptography (ECC) as the public key algorithm. It also uses the Elliptic Curve Digital Signature Algorithm (ECDSA) as a digital signature scheme. GCS establishes initial agreement on the elliptic curve E with a generator point g of the order n. Using the curve parameters (E, g, n), GCS generates a privatepublic key pair as its identity. If GSK is the private key, its corresponding public key GPK is calculated as $G P K = g ^ { * } G S K$ The curve parameters (E, g, n) are then published to both CUAVs and WUAVs of the cluster.

2) Generating Cryptographic Identities for UAVs: CUAV/ WUAV generates private-public key pairs as its identity using the curve parameters (E, g, n). Individual UAV secures their private key and does not depend on the GCS. For CUAV[i]/WUAV[i], the private-public key pair is denoted as (CSK[i], CPK[i]) / (WSK[i], WPK[i]). All UAVs then send their newly generated public keys to the GCS for identification and registration.

3) Setting up Cryptographic Identity for Cluster: A cryptographic identifier is assigned to the UAV cluster by deriving it from the identities of CUAVs. For this purpose, GCS calculates the cluster identifier MSA from the public keys of all CUAVs, as shown in (1).

$$
M S A = c r e a t e m u l t i s i g
$$

$$
M \ \{ \ C P K [ 0 ] , \ C P K [ 1 ] , \ \dots , \ C P K [ N - 1 ] \ \}\tag{1}
$$

Note that the cluster identifier MSA is simply a multisig address. It enforces that of all N CUAVs, at least M must consent to complete a key management operation. In addition, the (2) is executed to permit the cluster MSA to create new assets during the re-enforcement process (see Section VI-E5).

$$
g r a n t ~ M S A ~ i s s u e\tag{2}
$$

4) Registering Cryptographic Identity of GCS and UAVs: GCS registers public keys of WUAVs/CUAVs as blockchainbased crypto-assets. The crypto-asset essentially consists of (i) unique asset name, (ii) key information, and (iii) ownership information. The asset name is used to identify and access the crypto-asset and its associated key. Key information stored in the crypto-asset is the public key of a UAV. The ownership information contains ownership data of the crypto-asset. For WUAV[i], a crypto-asset named WAST#i is created and associated with its public key WPK[i]. The ownership of the crypto-asset WAST#i is set to MSA. GCS carries out the registration process, as shown in (3).

$$
\begin{array} { l } { i s s u e ~ M S A \left\{ \ n a m e : W A S T \# i \right\} } \\ { \left\{ p u b k e y : W P K [ i ] \right\} } \end{array}\tag{3}
$$

MSA owns the crypto-asset WAST#i and its public key WPK[i], so only CUAVs can manage it. In addition, the public keys of CUAVs are also registered as crypto-assets. However, their public keys are used to calculate MSA and should therefore be immutable. For this purpose, ownership of their crypto-assets is set to a burn address. A burn address is an address whose corresponding private key is not retrievable. A crypto-asset owned by a burn address is immutable and nontransferable. If BAD is a burn address, the crypto-asset for a CUAV[i] named CAST#i is created whose ownership is set to BAD using the same step as in (3). Similarly, the identity of GCS is also registered as an immutable crypto-asset named GAST using (3). Registered crypto-asset and its associated key information can be retrieved from the blockchain network. To retrieve the crypto-asset of WUAV[p], it is done by specifying its crypto-asset name of WAST#p, as shown in (4).

$$
g e t a s s e t i n f o W A S T \# p\tag{4}
$$

GCS then creates two lists: a list of Controller UAVs (LCU) and a list of Worker UAVs (LWU). LCU is immutable and contains the public keys of CUAVs and their corresponding asset names. It is denoted as $L C U = \{ ( C A S T \# 0 , ~ C P K [ O J ) , . . . ,$ (CAST#(N-1), CPK[N-1])}. In contrast, LWU is a dynamic list and contains the public keys of WUAVs and their corresponding asset names. It is denoted as $L W U = \langle ( W A S T \# 0 , \ W P K [ O J ) , . . . ,$ (WAST#T-N-1, WPK[T-N-1])}. The LCU and LWU are sent to all the WUAVs and act as their trusted source. CUAVs may optionally save copies of the LCU and LWU to facilitate quick lookup. Each UAV also saves key information related to the crypto-asset GAST of the GCS.

5) Setting up the Blockchain Network: GCS loads each CUAV with a copy of the blockchain ledger that contains crypto-assets information. CUAVs are set up as full nodes and can validate underlying transactions and blocks. They are configured with individual wallets and authorized to call different blockchain-based APIs. CUAVs form the backbone of the blockchain network to synchronize key information.

Performance and scalability are major hurdles in the practical application of blockchain. Most traditional blockchains have low transaction throughput, high transaction confirmation latency, and excessive energy consumption. As a result, many scalability issues arise when the number of users increases. MultiChain addresses these issues by utilizing a delegated consensus mechanism instead of the proof of work (POW). A round-robin technique is used to select a miner for a particular round. For this purpose, a mining diversity parameter is defined whose value is $0 \leq$ mining diversity â¤ 1. A spacing value is then calculated as the round-up product of the total number of miners and the mining diversity. A new block will be accepted only if its miner did not mine any previous spacing-1 blocks. This round-robin technique addresses two main issues: (i) mining freeze due to inactive miners and (ii) malicious miners building an alternative blockchain. A selected miner performs mining by signing the new block to prove its identity. As a result, this mining technique of MultiChain can confirm 2,000 transactions/sec (2,500 transactions/sec without confirmation) and allows the blockchain network to scale.

## B. Cluster Key Management

Intra-cluster communication is secured via symmetric encryption using a shared cluster key. GCS generates the initial cluster key $\mathrm { C K } _ { o }$ and shares it with all UAVs. To improve security, the cluster key is updated at regular intervals. For this purpose, the system randomly selects a CUAV to generate subsequent cluster keys at regular intervals. Of the N CUAVs, one CUAV is chosen using the round-robin technique mentioned in Section VI-A5. Scheduling cluster key generation based on such a technique ensures each CUAV equal opportunity and prevents inactive CUAVs from disrupting the process. If CUAV[s] is selected, it generates a new cluster key $\mathrm { C K _ { 1 } }$ and broadcasts it to other UAVs. Broadcasting $\mathrm { C K _ { 1 } }$ to CUAV[x]/WUAV[x] is done as shown in (5) and (6).

$$
\begin{array} { l } { { { \cal C U A V } [ s ]  { \cal C U A V } [ x ] : \{ e n c \{ { \cal C A S T } \# s , } }  \\ { { { \cal C K } _ { 1 } , \eta 1 , s i g \{ h s h \{ { \cal C A S T } \# s , { \cal C K } _ { 1 } , \eta 1 \} \} } } \\  { { \cal C S K } [ s ] , - , - , - \} { { \cal C K } _ { o } \} } \\ { { { \cal C U A V } [ s ]  W U A V [ x ] : \{ e n c \{ { \cal C A S T } \# s , } } } \\ { { { \cal C K } _ { 1 } , \eta 2 , s i g \{ h s h \{ { \cal C A S T } \# s , { \cal C K } _ { 1 } , \eta 2 \} \} } } \\   { \cal C S K } [ s ] , - , - , - , \} { { \cal C K } _ { o } \} } \end{array}\tag{5}
$$

(6)

Note that the symbol (-) is used wherever data is not required. The payload is per the format given in Fig. 3 and encrypted using the current cluster key $C K _ { 0 }$ . The new cluster key CK1 is accepted only if SSM is authenticated. In addition, using the round-robin scheduling technique of MultiChain, CUAVs can further verify CUAV[s] as the authorized cluster key generator. However, WUAVs cannot access the blockchain and its scheduling technique. An alternate solution is for other CUAVs to rebroadcast $\mathrm { C K _ { 1 } }$ to WUAVs. WUAVs accept $\mathrm { C K _ { 1 } }$ only if they receive rebroadcasts from at least M CUAVs.

## C. Key Update

WUAVs constantly update their key pair to prevent any potential key leakage. Consider that WUAV[j] wants to update its existing key pair of (WSK[j], WPK[j]). Using the curve parameters $( E , g , n )$ , WUAV[j] selects WSKâ[j] as its new private key and calculates the corresponding public key as $W P K ^ { \prime } [ j ] =$ $g ^ { * } W S K ^ { , } [ j ]$ . Then consent signatures should be collected from at least M CUAVs to update WPK[j] to WPKâ[j]. Assuming that these M CUAVs are identified as {CUAV[0]...CUAV[M-1]}. As shown in (7), the first request for consent is sent to CUAV[0].

$$
\begin{array} { l } { { W U A V [ j ]  C U A V [ 0 ] : \{ e n c \{ W A S T \# j , } }   \\ { { W P K ^ { \prime } [ j ] , \eta 3 , \ s i g \{ \ h s h \{ W A S T \# j , } }   \\ { { W P K ^ { \prime } [ j ] , \eta 3 \ \} \ \} _ { W S K [ j ] } , W A S T \# j , - , \eta 4 , } } \\  { s i g \{ \ h s h \{ \ W A S T \# j , - , \ \eta 4 \ \} \} _ { W S K [ j ] } \ \} _ { C K _ { 1 } } \} } \end{array}\tag{7}
$$

When CUAV[0] receives the request, it decrypts the payload using the cluster key $\mathrm { C K _ { 1 } }$ and validates it using SSM and TSM. CUAV[0] then gives its consent signature to update key information of the crypto-asset WAST-j to WPKâ[j]. For this purpose, a multisig transaction is constructed and signed, as shown in (8).

$$
\begin{array} { c } { { T X ^ { 1 } = c r e a t e r a w s e n d f r o m ~ M S A } } \\ { { \{ M S A : \{ W A S T \# j : 1 \} , D a t a : } }  \\ { { \{ p u b k e y : W P K ^ { \prime } [ j ] \} \ \} \ ( a c t i o n = s i g n ) } } \end{array}\tag{8}
$$

The action parameter is set to sign so that CUAV[0] signs the resulting transaction $T X ^ { 1 } . T X ^ { 1 }$ is a MultiChain object that consists of two parts: (i) a blockchain transaction in hexadecimal format. The notation 1 indicates that the transaction is signed only once, (ii) a complete field representing the status of the multi-signing process. The complete field value is set to true only when the transaction received M numbers of consent signatures else false. Therefore, $T X ^ { 1 }$ is forwarded to other CUAVs to collect their consent signatures. As shown in (9), CUAV[0] sends a new request with $T X ^ { 1 }$ as its content and forward it to CUAV[1].

$$
\begin{array} { r c l } { { } } & { { } } & { { C U A V [ 0 ]  C U A V [ 1 ] : \{ e n c \{ W A S T \# j , } }   \\ { { } } & { { } } & { { W P K ^ { \prime } [ j ] , \eta 3 , \ s i g \{ \ h s h \{ \ W A S T \# j , } }   \\ { { } } & { { } } & { { W P K ^ { \prime } [ j ] , \eta 3 \ \} \} _ { W S K [ j ] } , C A S T \# 0 , T X ^ { 1 } , \eta 5 , } } \\ { { } } & { { } } &  { s i g \{ \ h s h \{ \ C A S T \# 0 , T X ^ { 1 } , \eta 5 \} \} _ { C S K [ 0 ] } \} _ { C K _ { 1 } } \} } \end{array}\tag{9}
$$

Similarly, CUAV[1] receives the request and decrypts the payload using CK1. If SSM and TSM are authenticated, then CUAV[1] consents and signs the transaction (Hex) part of $T X ^ { 1 }$

as shown in (10).

$$
\begin{array} { c } { { T X ^ { 2 } = s i g n r a w t r a n s a c t i o n } } \\ { { < T r a n s a c t i o n \ ( H e x ) \ p a r t \ o f \ T X ^ { 1 } > } } \end{array}\tag{10}
$$

The object $T X ^ { 2 }$ contains a multisig transaction signed by two CUAVs, i.e., CUAV[0] and CUAV[1]. This process of signing and forwarding the partially signed multisig transaction continues until the request reaches the CUAV[M-1]. When CUAV[M-1] consented, it signs the transaction using the same command shown in (10). The output is $T X ^ { M }$ , which contains a multisig transaction signed with M consent signatures, and its complete field set as true. As shown in (11), CUAV[M-1] then submits the transaction (hex) part of $T X ^ { M }$ to the blockchain network.

$$
T X \_ I D = s e n d r a w t r a n s a c t i o n
$$

$$
< T r a n s a c t i o n \ ( H e x ) p a r t o f \ T X ^ { M } > \ ( 1 1 )
$$

CUAV[M-1] receives a TX_ID after submitting the transaction to the blockchain network. It then broadcasts the new key WPKâ[j] to every WUAV in the cluster. Broadcasting of WPKâ[j] to WUAV[x] is shown in (12).

$$
\begin{array} { r l } & { C U A V [ M - 1 ]  W U A V [ x ] : \lbrace e n c \lbrace W A S T \# j , } \\ & { W P K ^ { \prime } [ j ] , \eta 3 , s i g \lbrace h s h \lbrace W A S T \# j , W P K ^ { \prime } [ j ] , } \\ & { \eta 3 \rbrace \rbrace \rbrace _ { W S K [ j ] } , C A S T \# ( M - 1 ) , T X _ { - } I D , \eta 6 , } \\ & { s i g \lbrace h s h \lbrace C A S T \# ( M - 1 ) , T X _ { - } I D , } \\ & { \eta 6 \rbrace \rbrace _ { C S K [ M - 1 ] } \rbrace c K _ { 1 } \rbrace } \end{array}\tag{12}
$$

When WUAVs receive the payload, they decrypt and validate it using SSM and TSM. WUAVs then update the crypto-asset WAST#j in their LWUs with a new key of WPKâ[j]. Broadcasting to CUAVs is unnecessary as they can retrieve updated key information directly from the blockchain network.

## D. Key Revocation

The proposed system allows the revocation of a crypto-asset associated with a given key. For this purpose, the ownership of a crypto-asset is changed from an MSA to a burn address. If REV is identified as a burn address, a crypto-asset is revoked by changing the ownership from MSA to REV. Consider that revocation of the asset WAST#k associated with WUAV[k] is required. Then any CUAV can initiate the revocation process, as shown in (13).

$$
\begin{array} { c } { { R X ^ { 1 } = c r e a t e r a w s e n d f r o m ~ M S A } } \\ { { \{ R E V : \{ W A S T \# k : 1 \} , ~ D a t a : } }  \\ { { \{ p u b k e y : W P K [ k ] \} \{ a c t i o n = s i g n ) } }  \end{array}\tag{13}
$$

$R X ^ { 1 }$ object is then forwarded to other CUAVs to collect at least M consent signatures and revoke the crypto-asset WAST#k. This is similar to the key update process given in (9), (10), (11), and (12). Revocation of a crypto-asset is a permanent procedure and not reversible. However, note that the crypto-assets of CUAVs are immutable and not revocable.

## E. Special Scenarios

1) Permission Control on Crypto-Asset: MultiChain allows management of the global permissions of the MSA identifier. Two commands are used, namely grant and revoke. The grant command is used to give permissions to MSA to perform issue, create, send, and receive on the crypto-asset. On the other hand, the revoke command nullifies permissions granted to MSA. In addition, MultiChain is configurable such that an administrator cannot singly grant or revoke permissions. Changes relating to grant/revoke are applied only if a certain number of administrators agree. This prevents a compromised administrator from jeopardizing the blockchain network.

2) WUAV failure/compromise: WUAV does not control key management operations. Hence, a compromised or nonoperational WUAV has a limited effect on the cluster. Any CUAV can initiate the revocation process of such WUAV as mentioned in Section VI-D. Moreover, adding new WUAV to such a cluster is possible via the re-enforcement process discussed in Section VI-E5.

3) CUAV failure/compromise: Key management for a cluster with a M:N:T configuration remains (i) operational as long as M or more CUAVs are active. It becomes non-operational if the number of active CUAVs becomes less than M, (ii) secure as long as the total number of compromised CUAVs does not exceed M. If it equals or exceeds M, then such CUAVs can collaborate to compromise the system. Note that adding a new CUAV to the cluster via the re-enforcement process (refer Section VI-E5) is not supported.

4) Single-Point-of-Failure Issue: The single-point-of-failure issue can be discussed based on the key management and the network. (i) Regarding key management, it is resolved by taking advantage of the multisignature scheme. For a given M:N:T configuration, key management depends only on M numbers of CUAVs. The system remains operational even if the remaining (N-M) CUAVs are unavailable or destroyed. Therefore, the system is resilient to the single-point-of-failure of key management. While a higher M value offers better resilience to such failure, it comes at the cost of performance. (ii) Regarding the network, the single-point-of-failure event is resolved by leveraging the blockchain network. Multiple copies of the ledger are maintained across the blockchain network to eliminate the possibility of single-point-of-failure.

5) WUAV Re-Enforcement: The proposed system offers a novel feature that allows GCS to re-enforce a remote cluster with new WUAVs. Consider that GCS had no access to the latest information on the cluster key or blockchain data. GCS decides to re-enforce a cluster using WUAVr whose key pair is (WSKr, WPKr). A payload is created where GCS uses TSM to sign and certify the public key WPKr. On the other hand, WUAVr generates the SSM of the payload. GCS then equips WUAVr with the original LCU and the newly constructed payload. When WUAVr reaches the remote destination, it selects CUAV[s] from LCU to process its re-enforcement request. It sends a request as shown in (14).

$$
W U A V _ { r }  C U A V [ s ] : \{ e n c \} - , W P K _ { r } ,
$$

$$
\begin{array} { r l } & { \eta 7 , \ s i g \{ \ h s h \{ \ - , W P K _ { r } , \ \eta 7 \} \ \} \ \ = W S K _ { r } , } \\ & { G A S T , \ W P K _ { r } , \ \eta 8 , \ s i g \{ \ h s h \{ \ G A S T , \ }  \\ &  W P K _ { r } , \ \eta 8 \ \} \ \} \ = G S K \} \end{array}\tag{14}
$$

The payload is encrypted using the public key CPK[s] as the latest cluster key is unavailable to WUAVr. CUAV[s] receives the request and decrypts the payload using its private key. Then SSM is used to validate the public key of WPK . TSM is used to validate and confirm that the GCS had dispatched WUAVr. CUAV[s] then creates a new crypto-asset of WAST#r and associates it with WPKr, using (3). Note that a single CUAV can complete the re-enforcement procedure, and multiple consents are not required. Consequently, CUAV[s] encrypts the up-to-date LWU and cluster key CK1 using WPKr and sends it to the WUAVr. Further, CUAV[s] broadcasts WPKr to other WUAVs of the cluster, as shown in (15). Note that the SSM of the new payload is constructed using TSM from (14).

$$
\begin{array} { r l r } {  { C U A V [ s ]  W U A V [ x ] : \{ e n c \{ G A S T , \ W P K _ { r } , \ \eta 8 , } }  \\ { \newline } \\ { \newline } \\ { { s i g \{ h s h \{ G A S T , W P K _ { r } , \eta 8 \ \} \ \} \ \ J _ { G S K } , C A S T \# s , } } \\ {  { W A S T \# r , \eta 9 , s i g \{ \ h s h \{ C A S T \# s , W A S T \# r , \ \eta 9 \ \} } }  \\ &  \} \\ { \newline } &  \{ C S K [ s ] \ \} _ { C K _ { 1 } } \} \end{array}\tag{15}
$$

When WUAV receives the broadcast, it validates the (i) SSM to confirm that GCS dispatched the WUAVr and (ii) TSM to ascertain that a member CUAV had approved the re-enforcement. Then (WAST#r, WPKr) is added as the $( T - N ) ^ { t h }$ entry of the LWU. Broadcasting to other CUAVs is unnecessary as key information of WAUVr is retrievable directly from their blockchain ledger. Note that the proposed system does not support re-enforcement with a new CUAV.

6) Sub-Clustering and Re-Merging: Sub-clustering is the division of a large UAV cluster into smaller but fully independent and functional sub-clusters. For a cluster with M:N:T configuration, the maximum number of derivable sub-clusters is N/M. Each sub-cluster would have at least M CUAVs to carry out key management operations independently. Sub-clustering provides a flexible and scalable network with a wider coverage area. However, communication between sub-clusters is maintained via their respective CUAVs to synchronize their blockchain ledger. Re-merging of sub-clusters requires no additional permission or authentication. LCU, LWU, and blockchain are available to account for every UAV during the re-merger.

7) Inter-Cluster Migration: The proposed system allows WUAV to migrate from a cluster MSA to another cluster MSAâ if they share the same blockchain network. Migration is performed simply by changing ownership of the crypto-asset of a WUAV from MSA to MSAâ. For instance, if WUAV[m] wants to migrate from cluster MSA to cluster MSAâ, it sends a migration request to CUAV[0], similar to (7). CUAV[0] accepts the request and creates a multisig transaction based on (8). Subsequent steps to complete the migration process are similar to those of (9), (10), (11), and (12). Consequently, ownership of the crypto-asset WAST#m is changed to MSAâ. As a result, only the cluster MSAâ can now perform key management operations on the crypto-asset WAST#m.

8) Optimization of Cluster Communication: Since UAVs operate within a highly dynamic network, their network topology changes constantly and may delay the collection process of consent signatures. Therefore, an optimized network topology must be maintained to prevent such delay. For this purpose, necessary conditions include (i) maintenance of a direct CUAV-CUAV link to ensure efficient signature collection with minimum delay, and no involvement of intermediate WUAVs (ii) maintenance of a direct CUAV-WUAV link to ensure that WUAV communicates key management requests directly to a CUAV, and no involvement of other intermediate WUAVs. The sub-clustering discussed in Section VI-E6 is a useful feature that can facilitate assembly for an optimized network.

Moreover, delay due to multisignatures can be addressed based on (i) communication latency: M=1 causes no delay as a single CUAV can independently complete key management operation. M>1 causes delay due to additional signatures requirement for approval. To resolve this, the signature collection can be improved by optimizing network topology as discussed in Section VI-E8, (ii) computational latency: multisignature scheme should use efficient cryptographic primitives that ensure both security and performance. For the same security level, ECC-based cryptographic primitives use smaller key sizes. This makes ECC more efficient and suitable for resource-constrained devices. In addition, ECDSA is a relatively efficient digital signature scheme that generates compact signatures.

9) Operation Under Hostile Environment: CUAVs form the backbone of the proposed key management system and should be protected against different attacks. When the UAV cluster is deployed to a hostile environment, techniques such as (i) subclustering discussed in Section VI-E6 may be adopted to divide the main cluster into multiple sub-clusters before its deployment to the front line. At least one sub-cluster may be maintained as a backup so that any UAVs surviving the front line may re-merge with it, (ii) re-enforcement discussed in Section VI-E5 may be utilized to replete the cluster with additional WUAVs whenever needed, and (iii) optimization of cluster communication discussed in Section VI-E8 may be considered to maintain intra-cluster connectivity during any operational scenario.

10) Crypto-Asset Recovery & Dispute Resolution: In a M:N:T cluster configuration, ownership of a crypto-asset and its associated key is distributed among N CUAVs. The recovery of such crypto-assets inherently relies on the cooperation of at least M CUAVs. As long as M CUAVs are active, the crypto-asset can be retrieved from the blockchain to carry out a key management operation. Similarly, resolutions of crypto-asset disputes rely on consensus among the M CUAVs to prevent any deadlock during key management operations.

## VII. SECURITY ANALYSIS METHODOLOGY

Security analysis is performed on the (i) proposed key management system, (ii) proposed intra-cluster communication protocol, and (iii) security threats to the UAV cluster.

## A. Security Analysis of the Proposed Key Management System

The proposed key management system is analyzed based on the National Institute of Standards and Technology (NIST)

guidelines for key management [33]. This guideline establishes a minimal level of security for key management systems. It identifies four different scopes that evaluate: (i) the support for protection requirement of key information. Only the key type of public authentication key is considered since the proposed system uses the public key as an identity, (ii) the support for recommended key states and transitions. This is important as different key states have distinct restrictions on key utilization, and (iii) the support for key management phases and functions. The proposed system is required to support recommended phases and their functions, and (iv) whether a focus is given on additional design and operational concerns raised due to the real-time nature of key management operations.

## B. Security Analysis of the Intra-Cluster Communication Protocol

The proposed key management involves intra-cluster communication and is secured using the following techniques:

- A shared cluster key encrypts and decrypts communication between UAVs. Moreover, the cluster key is updated regularly to mitigate potential key leakage.

Communication uses the two signature modules of SSM and TSM. SSM and TSM are used to authenticate the source and the intermediate participant, respectively.

- Nonce values are used to secure communication by preventing it from replay attacks.

The proposed system pre-configures a trusted source using (i) blockchain for CUAVs and (ii) LCU/LWU for WUAVs. The communication protocol uses such trust sources to perform one-way authentication. Therefore, the protocol is evaluated using the notion of weak authentication. Automated Validation of Internet Security Protocols and Applications (AVISPA) [34] tool is utilized to perform the analysis. Two analyzer models are also considered, an On-the-fly Model Checker (OFMC) and a Constraint-Logic-based Attack Searcher (CL-AtSe).

## C. Security Analysis of Threats to the UAV Cluster

The safety of the UAV cluster reveals the effectiveness of the proposed key management system. For this purpose, the STRIDE Threat Model [35] is considered to identify potential security threats to the UAV cluster. These security threats are assessed using the Common Vulnerability Scoring System (CVSS) [36] and rated per CVSS v3.1. Individual UAVs (and GCS) are considered the vulnerable component, and the UAV cluster is the impacted component. In addition, the risk level of these security threats is also evaluated based on the NISTâs guideline for conducting risk assessments [37]. Moreover, risk assessment on other advanced security attacks [38] targeting the different Open Systems Interconnection (OSI) layers is performed for the UAV cluster.

## VIII. PERFORMANCE ANALYSIS METHODOLOGY

Performance analysis of the proposed system is conducted by implementing it in the UAV cluster. The following steps are considered for this purpose.

TABLE II OMNET++ CONFIGURATIONS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Max.communication range</td><td rowspan=1 colspan=1>1000m</td></tr><tr><td rowspan=1 colspan=1>Bitrate</td><td rowspan=1 colspan=1>24Mbps</td></tr><tr><td rowspan=1 colspan=1>IEEE 802.11 mgmt.module</td><td rowspan=1 colspan=1>Ieee80211MgmtAdhoc</td></tr><tr><td rowspan=1 colspan=1>Transmission protocol</td><td rowspan=1 colspan=1>UDP</td></tr><tr><td rowspan=1 colspan=1>Public Key Cryptography</td><td rowspan=1 colspan=1>ECC (secp256r1)</td></tr><tr><td rowspan=1 colspan=1>Symmetric Cryptography</td><td rowspan=1 colspan=1>AES-128-CTR</td></tr><tr><td rowspan=1 colspan=1>Digital signature scheme</td><td rowspan=1 colspan=1>ECDSA (secp256r1)</td></tr><tr><td rowspan=1 colspan=1>Requestinterval</td><td rowspan=1 colspan=1>exponential(0.1s)</td></tr><tr><td rowspan=1 colspan=1>sim-time-limit</td><td rowspan=1 colspan=1>60s</td></tr><tr><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>Express</td></tr></table>

<!-- image-->  
Fig. 4. Topologies for (a) best-case, and (b) worst-case.

## A. Platform Configuration

OMNET++ [39] is used to implement and conduct the performance analysis of the proposed key management system. The different settings of the simulation platform are given in Table II. OMNET++ is installed in a virtual 64-bit Ubuntu-20.04.5 LTS with 2 GB RAM running in an Oracle VM Virtual-Box. The VirtualBox is installed in a 64-bit Windows 11 PC with an Intel Core i3 CPU (3.60 GHz) and 8.00 GB RAM. Crypto++ [40] is used as the library to perform cryptographic-related calculations.

## B. Factors Considered for Performance Analysis

Different factors affecting the performance of the proposed system are identified. These factors include the (i) parameter M whose values are selected as M = {2, 3, 4, 5, 6}, (ii) parameter T whose values are selected as T = {25, 50, 75, 100}, (iii) case scenarios of network topology as {Best-case, Worst-case}. These scenarios are defined as follows:

- Best-case: Request passes through the shortest communication path to collect M consent signatures. This path consists only of CUAVs positioned consecutively, one after another. For example, a best-case topology for the 2:2:5 configuration is given in Fig. 4(a).

Worst-case: Request passes through the longest communication path to collect M consent signatures. This path comprises every WUAV and M CUAVs in the cluster. The CUAV[M-1] is at the end of the path. For example, a worst-case topology for the 2:2:5 configuration is given in Fig. 4(b).

In both cases, WUAV[0] sends the request, and CUAV[M-1] submits it to the blockchain. To ensure that the experimentation is reproducible, it is assumed that the UAVs are at the maximum communicable distance from one another. LinearMobility is selected as the Mobility model with a speed of 10 mbps, so the topology remains unchanged during the entire communication time. In addition, the response follows the same path as a request but in the reverse order.

The performance analysis also considers routing protocols of reactive and proactive types. Hence, the Ad Hoc On-Demand Distance Vector (AODV) and Destination-Sequenced Distance-Vector (DSDV) are used for this purpose.

## C. Domains of the Performance Analysis

The performance analysis focuses on the three domains of (i) UAV cluster network, (ii) blockchain network, and (iii) energy consumption. It is conducted by evaluating the system during the key update operation.

1) UAV Cluster Network Performance Analysis: Two network performance metrics are considered, and they are defined as follows:

- Average Response Delay: This is the average waiting time for an update request to receive its corresponding response. For topologies given in Fig. 4, it is the average waiting time for an update request from WUAV[0] to receive its corresponding response from CUAV[M-1].

- Total Response Loss: This is the total number of update requests sent that never received their corresponding responses. For topologies given in Fig. 4, it is the total number of update requests sent by WUAV[0] but never received their corresponding response from CUAV [M-1].

In addition, network bandwidth is also studied by analyzing the average rate at which data is uploaded and downloaded through the network.

2) Blockchain Network Performance Analysis: This analysis focuses on monitoring the number of transactions submitted by the system versus the (i) number of blocks created by the blockchain network, and (ii) number of new entries added to the unspent transaction output (UTXO) set. While the submitted transactions indicate the throughput of the proposed key management system, the blocks created indicate the corresponding capability of the blockchain network to process transactions. On the other hand, a change in the UTXO setâs entries reveals the memory usage of the blockchain server. This analysis aims to uncover any possible scalability bottlenecks in the blockchain network.

3) Energy Consumption Analysis: UAVs are energyconstrained devices whose power consumption directly affects the networkâs performance. This analysis examines the total energy consumption of UAVs in the cluster. Based on OMNET++, IdealEpEnergyStorage and StateBasedEpEnergyConsumer are chosen as the energy storage and consumption models, respectively.

TABLE III  
NIST: PROTECTION REQUIREMENTS FOR KEY INFORMATION (OF PUBLIC AUTHENTICATION KEY)
<table><tr><td></td><td></td><td>Supported?</td></tr><tr><td>Security Service</td><td>Identityauthentication Integrity authentication</td><td>â â</td></tr><tr><td>Security Protection</td><td>Integrity Availability</td><td>â â</td></tr><tr><td>Association Protection</td><td>Usageor application Keypair owner Authenticateddata Private authentication key Domain parameters</td><td>â Ã â â Ã</td></tr><tr><td>Assurances Required</td><td>Validity</td><td>â</td></tr><tr><td>Period of Protection</td><td>From generationuntil no protected data needs to be authenticated</td><td>7</td></tr></table>

TABLE IV

NIST: KEY STATES AND TRANSITIONS
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Supported?</td></tr><tr><td rowspan=1 colspan=1>Pre-Activation</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Active</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>Deactivated</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>Compromised</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>Suspended</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Destroyed</td><td rowspan=1 colspan=1>Ã</td></tr></table>

TABLE V

NIST: KEY-MANAGEMENT PHASES AND FUNCTIONS
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Supported?</td></tr><tr><td rowspan=1 colspan=1>Pre-operational</td><td rowspan=1 colspan=1>EntityRegistrationSystem InitializationInitializationKeying-Material InstallationKeyEstablishmentKey Registration</td><td rowspan=1 colspan=1>&gt;&gt;âÃââ</td></tr><tr><td rowspan=1 colspan=1>Operational</td><td rowspan=1 colspan=1>Normal Operational StorageContinuity of OperationsKey ChangeKey Derivation Methods</td><td rowspan=1 colspan=1>âÃâÃ</td></tr><tr><td rowspan=1 colspan=1>Post-operational</td><td rowspan=1 colspan=1>Key Archive and Key RecoveryEntity De-registrationKey De-registrationKey DestructionKey Revocation</td><td rowspan=1 colspan=1>âââÃâ</td></tr><tr><td rowspan=1 colspan=1>Destroyed</td><td rowspan=1 colspan=1>Destroyed</td><td rowspan=1 colspan=1>Ã</td></tr></table>

## IX. RESULTS AND DISCUSSION

The following sections highlight and discuss the results of security and performance analysis.

## A. On Security Analysis

Firstly, the proposed key management system is analyzed based on NISTâs guidelines for key management. Table III shows the analysis studied on the recommended properties for public authentication key. It reveals that most of the NISTâs recommended properties are satisfied. However, Table IV discloses that the proposed system did not support all the recommended key states and transitions. Table V shows that most phases of the key lifecycle are implemented, except for the Destroyed phase. The recommended functions associated with these phases are also mostly supported. Table VI shows that the proposed system addressed most of the additional concerns about the real-time nature of key management operations.

TABLE VI  
NIST: ADDITIONAL CONSIDERATIONS
<table><tr><td></td><td rowspan=1 colspan=1>Addressed?</td></tr><tr><td rowspan=1 colspan=1>Access Control&amp;Identity Authentication</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>InventoryManagement</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>Accountability</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>Audit</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Key-Management SystemSurvivability</td><td rowspan=1 colspan=1>â</td></tr></table>

<!-- image-->  
Fig. 5. Communication protocol analyzed using AVISPA.

Secondly, an AVISPA tool evaluates the proposed communication protocol that encrypts data and authenticates UAVs in the cluster. As shown in Fig. 5, it is observed that both the OFMC and CL-AtSe analyzer models confirmed the protocol as SAFE. Therefore, the proposed protocol can secure intra-cluster communication during threshold key management.

Thirdly, Table VII summarizes the security threats to the UAV cluster network, their CVSS scores, and corresponding mitigation techniques. The analysis reveals two critical security threats: (i) a compromised CUAV can generate a non-scheduled cluster key to hijack the whole network. Such a cluster key can compromise the confidentiality and privacy of cluster data and (ii) leakage of cluster information during the migration process. Denial of service attacks are another security concern that can disrupt normal key management services. Such attacks can also make the UAV cluster inaccessible and may shut it down completely. In addition, risk assessment corroborates that cluster key disclosure poses a very high risk to the network. It also reiterates the security risk due to a compromised CUAV that generates a non-scheduled cluster key. However, Table VII shows that the UAV cluster mitigates all these threats using the proposed threshold key management system. Furthermore, Table VIII reveals that the risk of attacks that target the transport, network, and data link layers is low as it requires the direct participation of a legitimate cluster member. However, the risk to the physical layer is higher as the UAV cluster network is wireless and open to attacks.

Moreover, the proposed system extensively uses ECC cryptosystems to generate public keys and digital signatures. The reason is that the ECC algorithm provides a similar security level as other algorithms but with a smaller key size. However, the proposed system is not designed to be tightly coupled with ECC algorithms. Instead, it can be integrated with other cryptosystems and potentially even those designed for postquantum security. Hence, the vulnerability of ECC algorithms to future advanced quantum computing is not a major concern to the proposed key management and the UAV cluster.

TABLE VII  
SECURITY ANALYSIS & RISK ASSESSMENT BASED ON STRIDE THREAT MODEL, CVSS
<table><tr><td></td><td>Security Threats</td><td>CVSS Base Score</td><td>Risk Level</td><td>Countermeasures</td></tr><tr><td rowspan="4">Spoofing Identity</td><td>Non-memberUAVimpersonatesWUAV/CUAV</td><td>7.6</td><td>Low</td><td>Identify using LCU/LWU/Blockchain</td></tr><tr><td>WUAV impersonates CUAV</td><td>7.6</td><td>Low</td><td>Use LCU to identify CUAV</td></tr><tr><td>WUAV impersonates other WUAVs</td><td>5.6</td><td>Low</td><td>Authenticate based on LWU</td></tr><tr><td>Attacker impersonates GCS</td><td>7.9</td><td>High</td><td>Authenticate using the key info.of GAST</td></tr><tr><td rowspan="3">Tampering</td><td>UAV tampers LCU/LWU</td><td>5.2</td><td>Low</td><td>Verifyfromblockchainledger</td></tr><tr><td>CUAV tampers Blockchain</td><td>6.6</td><td>Moderate</td><td>Required 51% control of blockchain network</td></tr><tr><td>CUAV/WUAV tampers payload</td><td>7.9</td><td>Low</td><td>Use signature modules of SSM and TSM</td></tr><tr><td rowspan="4">Repudiation</td><td>WUAV denies sending a request</td><td>5.0</td><td>Very Low</td><td>Request source verified using SSM&amp; LWU</td></tr><tr><td>CUAV denies giving consent signature</td><td>5.9</td><td>Very Low</td><td>Consent verifiable using TSM&amp; LCU</td></tr><tr><td>CUAV denies generating a cluster key</td><td>7.7</td><td>Very Low</td><td>Generator verifiable using SSM&amp; LCU</td></tr><tr><td>GCS denies re-enforcing a cluster</td><td>7.7</td><td>Very LoW</td><td>GCS verifiable using the GAST crypto-asset</td></tr><tr><td rowspan="4">Information Disclosure</td><td>Cluster key discloses to non-member UAV</td><td>7.9</td><td>Very High</td><td>Cluster key is updated regularly</td></tr><tr><td>Blockchain credentials disclosed</td><td>4.7</td><td>Very Low</td><td>Blockchain credentials are encrypted</td></tr><tr><td>Non-member UAV eavesdropping</td><td>3.3</td><td>Moderate</td><td>Payload encrypted using cluster key</td></tr><tr><td>Clusterinfo.leaks due to migration</td><td>9.6</td><td>Very High</td><td>Update cluster key after every migration</td></tr><tr><td rowspan="4">Denial of Service</td><td>Due to request flooding by WUAV/CUAV</td><td>8.6</td><td>Low</td><td>Accept&amp; forward only verified payload</td></tr><tr><td>Due to unavailability of CUAV</td><td>8.6</td><td>Low</td><td>Deployed multiple CUAVs</td></tr><tr><td>Due to single-point-of-failure issue</td><td>8.6</td><td>Low</td><td>Deployed multiple CUAVs</td></tr><tr><td>Due to sub-clustering</td><td>8.6</td><td>Low</td><td>Maintain M CUAVs in each N/M sub-cluster</td></tr><tr><td rowspan="3">Elevation of Privilege</td><td>WUAV signs consent signature</td><td>6.6</td><td>Low</td><td>Authenticate any signing UAV using LCU</td></tr><tr><td>WUAV generates cluster key</td><td>7.2</td><td>Low</td><td>Authenticate generator CUAV using LCU</td></tr><tr><td>Non-selected CUAV generates cluster key</td><td>9.9</td><td>High</td><td>Use round-robin scheduling/rebroadcast techniques</td></tr></table>

CVSS Score'sSeverityRatingScale[None:0.0,Low:0.1-3.9,Medium:4.0-6.9,High:7.O-8.9,Critical:9.010.0]

TABLE VIII  
RISK ASSESSMENT OF ADVANCED SECURITY ATTACKS
<table><tr><td rowspan=1 colspan=1>TargetofAttack</td><td rowspan=1 colspan=1>Attack Name</td><td rowspan=1 colspan=1>Risk Level</td></tr><tr><td rowspan=1 colspan=1>TransportLayer</td><td rowspan=1 colspan=1>SYN floodUDP flood</td><td rowspan=1 colspan=1>Very LowLow</td></tr><tr><td rowspan=1 colspan=1>NetworkLayer</td><td rowspan=1 colspan=1>BlackholeGray holeRushingWormhole</td><td rowspan=1 colspan=1>LowLowLowLow</td></tr><tr><td rowspan=1 colspan=1>Data LinkLayer</td><td rowspan=1 colspan=1>CollisionDe-authenticationLow link quality&amp;high latency</td><td rowspan=1 colspan=1>LowLowLow</td></tr><tr><td rowspan=1 colspan=1>PhysicalLayer</td><td rowspan=1 colspan=1>EavesdroppingGPS SpoofingJamming</td><td rowspan=1 colspan=1>HighModerateHigh</td></tr></table>

TABLE IX

SUMMARY OF THE PERFORMANCE ANALYSIS (KEY UPDATE OPERATION)
<table><tr><td rowspan=2 colspan=1>(in Average)</td><td rowspan=1 colspan=2>AODV</td><td rowspan=1 colspan=2>DSDV</td></tr><tr><td rowspan=1 colspan=1>Best</td><td rowspan=1 colspan=1>Worst</td><td rowspan=1 colspan=1>Best</td><td rowspan=1 colspan=1>Worst</td></tr><tr><td rowspan=1 colspan=1>Response delay (ms)</td><td rowspan=1 colspan=1>0.0061</td><td rowspan=1 colspan=1>2.5043</td><td rowspan=1 colspan=1>0.0060</td><td rowspan=1 colspan=1>0.0767</td></tr><tr><td rowspan=1 colspan=1>Response loss</td><td rowspan=1 colspan=1>0.2</td><td rowspan=1 colspan=1>278.25</td><td rowspan=1 colspan=1>76.35</td><td rowspan=1 colspan=1>401.75</td></tr><tr><td rowspan=1 colspan=1>Upload (bits/sec)</td><td rowspan=1 colspan=1>8991.75</td><td rowspan=1 colspan=1>46025.40</td><td rowspan=1 colspan=1>8483.42</td><td rowspan=1 colspan=1>27248.97</td></tr><tr><td rowspan=1 colspan=1>Download (bits/sec)</td><td rowspan=1 colspan=1>8991.38</td><td rowspan=1 colspan=1>45869.05</td><td rowspan=1 colspan=1>8321.93</td><td rowspan=1 colspan=1>26907.11</td></tr><tr><td rowspan=1 colspan=1>Transactions submit/sec</td><td rowspan=1 colspan=1>9.92</td><td rowspan=1 colspan=1>8.62</td><td rowspan=1 colspan=1>9.15</td><td rowspan=1 colspan=1>3.86</td></tr><tr><td rowspan=1 colspan=1>Blocks create/sec</td><td rowspan=1 colspan=1>0.31</td><td rowspan=1 colspan=1>3.98</td><td rowspan=1 colspan=1>1.28</td><td rowspan=1 colspan=1>2.20</td></tr><tr><td rowspan=1 colspan=1>UTXO entries/sec</td><td rowspan=1 colspan=1>19.84</td><td rowspan=1 colspan=1>17.23</td><td rowspan=1 colspan=1>18.29</td><td rowspan=1 colspan=1>7.73</td></tr><tr><td rowspan=1 colspan=1>Energy consumed (J)</td><td rowspan=1 colspan=1>0.01</td><td rowspan=1 colspan=1>0.15</td><td rowspan=1 colspan=1>0.13</td><td rowspan=1 colspan=1>0.14</td></tr></table>

<!-- image-->  
Fig. 6. Comparing average response delay.

## B. On Performance Analysis

Performance analysis of the UAV cluster network is conducted based on the three factors of (i) best-case/worst-case scenarios, (ii) T parameter, and (iii) M parameter. The results of the performance analysis are discussed in the following sections.

1) Network Performance: Fig. 6 indicates that the average response delay of AODV and DSDV is consistent during the best-case scenario. However, the response delay for AODV becomes slower during the worst-case scenario as T value increases. Moreover, Fig. 7 indicates that during the best-case scenario, DSDV suffers response loss while AODV does not. However, both suffer from high response loss during the worstcase scenario due to large cluster size. Fig. 8 shows that the data transfer rate across the network is minimal during the best-case scenario. During the worst-case scenario, AODV consumed more network bandwidth due to higher upload/download of data.

2) Blockchain Performance: Fig. 9 compares transactions submitted against the corresponding (i) blocks generated, and (ii) UTXO Entries added. During the best-case scenario, AODV and DSDV exhibit similar performance patterns when generating transactions/blocks/UTXO entries. During the worst-case scenario, DSDV generated fewer transactions resulting in fewer blocks/UTXO entries in the blockchain network. Therefore, DSDV provides better blockchain performance than AODV, as it requires fewer computational and memory resources.

TABLE X  
COMPARISON WITH EXISTING KEY MANAGEMENT SYSTEMS FOR UAV NETWORKS
<table><tr><td colspan="2">Attribute</td><td>[20]</td><td>[21]</td><td>[22]</td><td>[23]</td><td>[24]</td><td>Proposed</td></tr><tr><td colspan="2">Key</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>â</td></tr><tr><td rowspan="3">Management</td><td>Configurable Collaborative/Threshold</td><td>Ã</td><td>Ã</td><td>Ã</td><td>â</td><td>Ã</td><td>â</td></tr><tr><td>Autonomous</td><td>â</td><td>Ã</td><td>â</td><td>Ã</td><td>Ã</td><td>â</td></tr><tr><td>Re-enforcement</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>Ã</td><td>â</td></tr><tr><td rowspan="3">UAV Network</td><td>Sub-clustering</td><td>Ã</td><td>Ã</td><td>Ã</td><td></td><td></td><td></td></tr><tr><td>Migration</td><td>â</td><td>â</td><td>Ã</td><td>Ã â</td><td>Ã Ã</td><td>â â</td></tr><tr><td>Single-point-of-failure</td><td>Ã</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Issue Addressed</td><td>Compromised CA problem</td><td>Ã</td><td>â Ã</td><td>Ã Ã</td><td>â</td><td>Ã</td><td>â</td></tr><tr><td>Security</td><td>Key Management</td><td></td><td></td><td></td><td>â</td><td>Ã</td><td>â</td></tr><tr><td>Analysis</td><td>Communication</td><td>Ã Ã</td><td>Ã Ã</td><td>Ã Ã</td><td>Ã Ã</td><td>Ã ProVerif</td><td>NIST</td></tr><tr><td>(Tool/Model/etc.)</td><td>UAV cluster network</td><td>Custom</td><td>Ã</td><td>Ã</td><td>Custom</td><td>Custom theorem</td><td>AVISPA STRIDE</td></tr><tr><td rowspan="3">Performance Analysis</td><td>Delay/Latency</td><td>Ã</td><td>E2E 0.0226 bps</td><td>Ã</td><td></td><td></td><td></td></tr><tr><td>Loss</td><td>Ã</td><td>PKR0.01ps</td><td>Ã</td><td>Ã Ã</td><td>Ã Ã</td><td>0.0767ms (avg)</td></tr><tr><td>Energy Requirement</td><td>110J/Cltr. Head (max)</td><td></td><td>Ã</td><td>Ã</td><td></td><td>401.75 (avg)</td></tr><tr><td>Blockchain</td><td>Transaction/Block rate</td><td></td><td>Ã</td><td></td><td></td><td>Ã</td><td>0.14J(avg)</td></tr><tr><td>Network</td><td>UTXO entries</td><td>0.03tps (max) Ã</td><td>8tps (max) Ã</td><td>Ã Ã</td><td>50tps Ã</td><td>Ã Ã</td><td>3.86tps (avg) 7.73/s (avg)</td></tr></table>

Duetothenon-compatibilityofexperimentation/simulation,theperformancemetricsgivenareforreferencepurposesonly.

<!-- image-->  
Fig. 7. Comparing total response loss.

<!-- image-->  
Fig. 8. Comparing network bandwidth usage.

3) Energy Consumption: Fig. 10 reveals that AODV consumes less energy than DSDV during the best-case scenario. During the worst-case scenario, AODV and DSDV have similar energy consumption patterns.

A summary of the performance analysis is given in Table IX. Both AODV and DSDV exhibit mostly similar performance metrics during the best-case scenario. However, DSDV delivers higher performance in worst-case scenarios, especially regarding response delay, bandwidth usage, and blockchain efficiency. Further, a comparison of the proposed system with the existing key management systems is also performed and shown in Table X.

<!-- image-->  
Fig. 9. Transactions submitted vs. Blocks created vs. UTXO Entries added.

<!-- image-->  
Fig. 10. Comparing Energy consumption.

## X. FUTURE SCOPE OF WORK

Investigation of the proposed key management system and the UAV cluster infers that there is scope for further research. The UAV cluster has assumed a predefined path to collect consent signatures. A practical mechanism may be devised to optimize the signatures collection process. Such a mechanism should aim toward building an optimal routing path to forward requests, thus causing minimum delay. To secure the UAV cluster, the number of compromised CUAVs should not exceed the security threshold value of M. A checking mechanism should be adopted to prevent compromised CUAVs from teaming up and disrupting the system. Further, the effect of re-enforcement, sub-clustering, re-merging, and inter-cluster migration techniques on the cluster performance require further investigation. The need to address attacks on UAV clusters, such as signal jamming, GPS spoofing, and other forms of electronic warfare, is critical. Moreover, the cluster should be evaluated using routing protocols like Optimized Link State Routing (OLSR), Dynamic Source Routing (DSR), Greedy Perimeter Stateless Routing (GPSR), etc., and under real-life scenarios using dynamic topology and mobility. Support to other blockchain platforms like Ethereum, Hyperledger, and Directed Acyclic Graph (DAG) ledger should be extended. DAG is an emerging distributed ledger technology that allows simultaneous transaction processing. It is capable of reducing confirmation time and improving network throughput. Therefore, adopting the DAG protocol could enhance the performance and scalability of the proposed system and the UAV cluster.

## XI. CONCLUSION

An autonomous UAV cluster was secured using the blockchain-based threshold key management system. Key management operations were carried out independently without intervention from any ground-based stations. The proposed system treated key information of UAVs as blockchain-based crypto-assets. Crypto-assets enabled the creation, updating, transfer, and revocation of key information within the blockchain network. Multisignature distributed key management authority among multiple UAVs to resolve compromised CA problems and single-point-of-failure events. The system was designed to be configurable, allowing it to adapt to various security and performance requirements for UAV applications.

The proposed key management system was verified to comply with most of the NISTâs guidelines. The proposed intra-cluster communication protocol was also verified using AVISPA and found to be secure. Security threats to the UAV cluster were identified using the STRIDE Threat model and their risk assessment was performed. These threats were then mitigated using the proposed key management system. Risk assessment found that attacks could occur at the physical layer due to the wireless nature of the network. Performance analysis revealed that AODV and DSDV performed consistently during the best-case scenario, but DSDV performance exceeded during the worst-case scenario. It noted that cluster size T had a visible effect on the performance of the routing protocols and proposed system. The blockchain analysis showed that AODV generated more transactions/blocks, increasing the consumption of computational resources, bandwidth, and storage. Finally, the energy analysis showed that AODV and DSDV had similar energy consumption patterns, where consumption increases with increasing M and T values. However, DSDV consumed more energy during the best-case scenario.

Future work should focus on the security and performance of the proposed key management system. This included designing an efficient consent signature collection mechanism, identifying an optimized security threshold, and investigating performance issues related to re-enforcement, sub-clustering, re-merging, and inter-cluster migration.

## REFERENCES

[1] G. K. Pandey, D. S. Gurjar, H. H. Nguyen, and S. Yadav, âSecurity threats and mitigation techniques in UAV communications: A comprehensive survey,â IEEE Access, vol. 10, pp. 112858â112897, 2022.

[2] A. Fotouhi et al., âSurvey on UAV cellular communications: Practical aspects, standardization advancements, regulation, and security challenges,â IEEE Commun. Surveys Tut., vol. 21, no. 4, pp. 3417â3442, Fourth Quarter 2019.

[3] Y. Mekdad et al., âA survey on security and privacy issues of UAVs,â Comput. Netw., vol. 224, 2023, Art. no. 109626.

[4] D. P. Agrawal, H. Deng, and A. Mukherjee, âThreshold and Identity-Based Key Management and Authentication for Wireless ad HoC Networks,â US Patent 8,050,409, Nov. 1, 2011.

[5] A. Diop, Y. Qi, and Q. Wang, âEfficient group key management using symmetric key and threshold cryptography for cluster based wireless sensor networks,â Int. J. Comput. Netw. Inf. Secur., vol. 6, no. 8, 2014, Art. no. 9.

[6] Y. Zhang, J. Liu, Y. Wang, J. Han, H. Wang, and K. Wang, âIdentity-based threshold key management for ad hoc networks,â in Proc. IEEE Pacific-Asia Workshop Comput. Intell. Ind. Appl., 2008, pp. 797â801.

[7] A. Kumar, A. Aggarwal, and Charu, âEfficient hierarchical threshold symmetric group key management protocol for mobile ad hoc networks,â in Proc. 5th Int. Conf. Contemporary Comput., Noida, India, 2012, pp. 335â346.

[8] Y. Tan, J. Wang, J. Liu, and N. Kato, âBlockchain-assisted distributed and lightweight authentication service for industrial unmanned aerial vehicles,â IEEE Internet Things J., vol. 9, no. 18, pp. 16928â16940, Sep. 2022.

[9] R. Chen, H.-W. Tseng, J.-L. Lien, and W. Liao, âBlockchain-empowered identity management with a dual identity model for UAVs in 5G networks,â IEEE Internet Things Mag., vol. 5, no. 2, pp. 69â73, Jun. 2022.

[10] K. Gai, Y. Wu, L. Zhu, K.-K. R. Choo, and B. Xiao, âBlockchain-enabled trustworthy group communications in UAV networks,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 7, pp. 4118â4130, Jul. 2021.

[11] K. Yu et al., âA blockchain-based shamirâs threshold cryptography scheme for data protection in industrial Internet of Things settings,â IEEE Internet Things J., vol. 9, no. 11, pp. 8154â8167, Jun. 2022.

[12] T. Ankenbrand, D. Bieri, R. Cortivo, J. Hoehener, and T. Hardjono, âProposal for a comprehensive (crypto) asset taxonomy,â in Proc. Crypto Valley Conf. Blockchain Technol., 2020, pp. 16â26.

[13] P. Freni, E. Ferro, and R. Moncada, âTokenization and blockchain tokens classification: A morphological framework,â in Proc. IEEE Symp. Comput. Commun., 2020, pp. 1â6.

[14] J. Arcenegui et al., âSecure management of IoT devices based on blockchain non-fungible tokens and physical unclonable functions,â in Proc. Int. Conf. Appl. Cryptography Netw. Secur., 2020, pp. 24â40.

[15] U. Khalil, O. A. Malik, O. W. Hong, and M. Uddin, âDSCoT: An NFTbased blockchain architecture for the authentication of IoT-enabled smart devices in smart cities,â 2022, arXiv:2211.04803.

[16] D. Zelenyanszki, Z. HÃ³u, K. Biswas, and V. Muthukkumarasamy, âA privacy awareness framework for NFT avatars in the metaverse,â in Proc. Int. Conf. Comput. Netw. Commun., 2023, pp. 431â435.

[17] B. Rajendran and A. K. Pandey, âPKI ecosystem for reliable smart contracts and NFT,â in Proc. IEEE Int. Conf. Public Key Infrastructure Appl., 2022, pp. 1â5.

[18] C. Rong, J. Geng, and M. G. Jaatun, âManaging digital objects with decentralised identifiers based on NFT-like schema,â in Proc. IEEE Int. Conf. Cloud Comput. Technol. Sci., 2022, pp. 246â251.

[19] S. Ghirmai, D. Mebrahtom, M. Aloqaily, M. Guizani, and M. Debbah, âSelf-sovereign identity for trust and interoperability in the metaverse,â in Proc. IEEE Smartworld Ubiquitous Intell. Comput. Scalable Comput. Commun., Digit. Twin Privacy Comput. Metavers Auton. Trusted Veh., 2022, pp. 2468â2475.

[20] Y. Tan, J. Liu, and N. Kato, âBlockchain-based key management for heterogeneous flying ad hoc network,â IEEE Trans. Ind. Informat., vol. 17, no. 11, pp. 7629â7638, Nov. 2021.

[21] A. Yazdinejad, R. M. Parizi, A. Dehghantanha, H. Karimipour, G. Srivastava, and M. Aledhari, âEnabling drones in the Internet of Things with decentralized blockchain-based security,â IEEE Internet Things J., vol. 8, no. 8, pp. 6406â6415, Apr. 2021.

[22] N. JÃ¤ger and A. AÃmuth, âAn approach for decentralized authentication in networks of UAVs,â in Proc. 12th Int. Conf. Cloud Comput., 2021, pp. 13â17.

[23] C. Feng, B. Liu, Z. Guo, K. Yu, Z. Qin, and K.-K. R. Choo, âBlockchainbased cross-domain authentication for intelligent 5G-enabled Internet of Drones,â IEEE Internet Things J., vol. 9, no. 8, pp. 6224â6238, Apr. 2022.

[24] S. U. Jan and H. U. Khan, âIdentity and aggregate signature-based authentication protocol for IoD deployment military drone,â IEEE Access, vol. 9, no. 15, pp. 130247â130263, Apr. 2022.

[25] F. Bao, R. H. Deng, and H. Zhu, âVariations of DiffieâHellman problem,â in Information and Communications Security, S. Qing, D. Gollmann, and J. Zhou, Eds., Berlin, Germany: Springer, 2003, pp. 301â312.

[26] G. Heo, K. Chae, and I. Doh, âHierarchical blockchain-based group and group key management scheme exploiting unmanned aerial vehicles for urban computing,â IEEE Access, vol. 10, pp. 27990â28003, 2022.

[27] H. Xie, J. Zheng, T. He, S. Wei, C. Shan, and C. Hu, âB-UAVM: A blockchain-supported secure multi-UAV task management scheme,â IEEE Internet Things J., vol. 10, no. 24, pp. 21240â21253, Dec. 2023.

[28] K. Hidawi, âDronexnft: An NFT-driven framework for secure autonomous UAV operations and flight data management,â 2024, arXiv:2409.06507.

[29] A. Yazdinejad, A. Dehghantanha, R. M. Parizi, G. Srivastava, and H. Karimipour, âSecure intelligent fuzzy blockchain framework: Effective threat detection in iot networks,â Comput. Ind., vol. 144, 2023, Art. no. 103801. [Online]. Available: https://www.sciencedirect.com/ science/article/pii/S016636152200197X

[30] A. M. Antonopoulos, Mastering Bitcoin: Unlocking Digital Cryptocurrencies. Sebastopol, CA, USA: OâReilly Media, Inc., 2014.

[31] C. S. Ltd, âMultichain json-rpc api commands,â Aug. 20, 2023. [Online]. Available: https://www.multichain.com/developers/json-rpc-api/

[32] B. Project, âBitcoin core,â Sep. 9, 2023. [Online]. Available: https:// bitcoin.org/en/bitcoin-core/

[33] E. Barker, âRecommendation for key management: Part 1âgeneral,â NIST Special Publication 800-57 Part 1, Revision 5, 2020, doi: 10.6028/NIST.SP.800-57pt1r5.

[34] T. Team et al., âAvispa v1. 1 user manual,â Sep. 22, 2024. [Online]. Available: https://people.irisa.fr/Thomas.Genet/Crypt/AVISPA_manual.pdf

[35] R. Khan, K. McLaughlin, D. Laverty, and S. Sezer, âStride-based threat modeling for cyber-physical systems,â in Proc. IEEE PES Innov. Smart Grid Technol. Conf. Europe, 2017, pp. 1â6.

[36] P. Mell et al., âA complete guide to the common vulnerability scoring system version 2.0,â FIRST-Forum Incident Response Secur. Teams, vol. 1, 2007, Art. no. 23.

[37] R. S. Ross, âGuide for conducting risk assessments,â NIST Special Publication 800-30, Revision 1, 2012, doi: 10.6028/NIST.SP.800-30r1.

[38] K.-Y. Tsao, T. Girdler, and V. G. Vassilakis, âA survey of cyber security threats and solutions for UAV communications and flying ad-hoc networks,â Ad Hoc Netw., vol. 133, 2022, Art. no. 102894. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S1570870522000853

[39] O. Ltd, âOmnet discrete event simulator,â Aug. 27, 2023. [Online]. Available: https://omnetpp.org/

[40] C. Project, âCrypto 8.8 release,â Sep. 22, 2024. [Online]. Available: https: //github.com/weidai11/cryptopp/releases/tag/CRYPTOPP_8_8_0

<!-- image-->

Mebanjop Kharjana received the BE degree in computer engineering from Mumbai University, India, and the MTech degree in information technology from North-Eastern Hill University, Shillong, India. He is currently working toward the PhD degree with the Department of Information Technology, North-Eastern Hill University, Shillong, India. He is working as a system analyst with the North-Eastern Hill University, Shillong, India. His research interests include IoT security, information-centric networking, and blockchain technology.

<!-- image-->

<!-- image-->

Subhas Chandra Sahana received the PhD degree from the North-Eastern Hill University, Shillong, India, and the MTech degree from the Tezpur University, Assam, India. He is an assistant professor with the Department of Computer Science & Engineering, National Institute of Technology, Durgapur, West Bengal, India. His current research interests include IoT security and elliptic curve cryptography.

Goutam Saha received the BE degree in electrical engineering and the ME degree in electronics and telecommunication engineering from the Bengal Engineering College, Shibpur (then under the University of Calcutta), in 1984 and 1989, respectively, and the PhD degree from the Indian Institute of Technology, Kharagpur, in 1999. He also has postdoctoral research experience from the Ben Gurion University, Israel. He is currently a professor with the Department of Information Technology, North-Eastern Hill University, Shillong, India. His current research interests include computational biology, bioinformatics, systems biology, river networking, IoT, and Big Data.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature/page_3_img_1.png|page_3_img_1]]
2. [[../extracted_images/Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature/page_9_img_1.jpeg|page_9_img_1]]
3. [[../extracted_images/Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature/page_10_img_1.jpeg|page_10_img_1]]
4. [[../extracted_images/Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature/page_14_img_1.jpeg|page_14_img_1]]
5. [[../extracted_images/Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature/page_14_img_2.jpeg|page_14_img_2]]
6. [[../extracted_images/Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature/page_14_img_3.jpeg|page_14_img_3]]

---

