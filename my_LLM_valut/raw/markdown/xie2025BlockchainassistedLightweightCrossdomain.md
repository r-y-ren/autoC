# Blockchain-Assisted Lightweight Cross-Domain Authentication for Multi-UAV Wireless Networks

Mingyue Xie , Zheng Chang , Senior Member, IEEE, Li Wang , Senior Member, IEEE, and Geyong Min , Senior Member, IEEE

AbstractâThe evolution of future network and control technologies has enabled unmanned aerial vehicles (UAVs) to collaborate across diverse geographical areas and task domains, enhancing task execution efficiency through data and resource sharing. In response to the increasing demand for cross-domain task allocation and operations for UAVs, establishing robust authentication mechanisms within trusted domains has become a critical foundation for ensuring secure cross-domain access. Despite significant progress in UAV identity authentication and cross-domain access, challenges persist, such as cumbersome and inefficient processes, UAV resource limitations, and establishing trust relationships across different domains. To address these challenges, this paper introduces a dual blockchain-assisted trusted authentication scheme for UAVsâ cross-domain access. Our approach utilizes a certificateless signcryption algorithm for lightweight UAV authentication, thereby eliminating the need for certificate management. Then, an efficient credit-based trust model is designed to measure the trustworthiness of data-in-transit and cross-domain entities. Furthermore, blockchain technology is introduced to store the relevant information of UAVs and credibility to assist cross-domain authentication. Theoretical security analysis and extensive simulations have been conducted, demonstrating the effectiveness and efficiency of our proposed scheme.

Index TermsâUAV network, cross-domain authentication, trust, blockchain, certificateless signcryption.

## I. INTRODUCTION

support large-scale device connectivity and intelligent interconnection, facilitating the growth of emerging applications such as unmanned aerial vehicles (UAVs) [1]. UAVs, renowned for their flexibility, high mobility, and extended endurance, are capable of collaborating across diverse geographical and task domains [2]. By enabling devices from different domains to exchange information and share resources, UAVs can significantly enhance task execution efficiency [3]. Compared to deploying new UAVs, leveraging existing legitimate UAVs to participate in tasks across domains can reduce costs associated with re-registration and local authentication. Furthermore, multi-UAV networks that support cross-domain operations can achieve superior performance in communication tasks and data collection [4].

The existing challenges in multi-UAV networks primarily involve the potential risks of identity forgery, data tampering, and privacy breaches. When developing security solutions, it is crucial to consider the distinctive features of UAV networks, including their decentralized architecture, the resource limitations of networked devices, intricate network topologies, and the challenges in device interoperability [5]. Furthermore, UAV domains are generally autonomous and structurally diverse. UAVs within the same domain are coordinated by an internal management [6]. Different domains may adopt different UAV authentication protocols and standards, leading to interoperability issues between cross-domain entities, which may undermine the communications effectiveness and security. Consequently, cross-domain access by UAVs necessitates robust authentication and authorization processes to ensure secure and seamless interoperability between domains [7].

Currently, to enable secure information exchange across multiple domains, cross-domain identity authentication methods for UAVs have been extensively explored. Current solutions primarily rely on centralized servers, such as public key infrastructures, for cross-domain authentication [8]. Some approaches involve certificates issued by trusted certificate authorities (CAs) to verify UAV identities [9], [10]. However, if a UAV or its certificate is compromised, revocation is necessary to prevent misuse, which requires complex management mechanisms and increases the difficulty of cross-domain authentication. Additionally, certificate generation imposes substantial computational and communication overhead as the system scales [11]. Many existing schemes also rely on computationally intensive operations [12], [13], such as bilinear pairing, which are illsuited for resource-constrained UAVs. These issues highlight critical importance in developing lightweight and decentralized cross-domain authentication approaches for UAV networks.

Unlike conventional centralized technologies, blockchain significantly mitigates issues such as the vulnerability of centralized systems to single-point attacks [14]. With its decentralized and traceable nature, blockchain securely stores information related to UAV authentication in a tamper-resistant manner. While other distributed technologies, such as traditional peer-to-peer systems, lack the same level of security, traceability, and immutability as blockchain. These characteristics highlight the potential and advantages of blockchain in the filed of UAV cross-domain authentication. On one hand, it ensures the security, reliability, and decentralization of data in distributed multi-domain network environments [15]. On the other hand, it provides anonymity by protecting privacy, as only the hash values of UAV information are stored on the blockchain [16]. Therefore, exploring the application of blockchain in cross-domain authentication for multi-UAV networks holds significant research value.

However, current blockchain-based authentication schemes often overlook two critical issues: the trustworthiness of UAVs and the limitations of blockchain performance. The majority of these methods concentrate on ensuring message integrity and confidentiality, which are essential for preventing external security threats such as eavesdropping and replay attacks [17]. However, internal security vulnerabilities, such as denial-ofservice attacks, still remain a concern [18]. In our approach, in addition to considering the negative impacts of untrustable data-in-transit in the UAV network, we develop a credit-based trust model to evaluate the dynamic trust relationship between the UAVs and their domains to ensure the trustworthy of crossdomain entities. Additionally, as a single blockchain can only support domain-specific and inter-domain authentication, we adopt a dual-blockchain structure to improve the efficiency and flexibility of cross-domain authentication. To further enhance the security and efficiency of cross-domain authentication, we introduce a certificateless signcryption algorithm to meet the lightweight and decentralized requirements of multi-UAV networks. The main contributions of this paper are as follows:

We propose a dual blockchain-assisted authentication scheme for cross-domain UAVs to enhance their decentralized features. This scheme employs blockchain to maintain decentralized intra-domain and inter-domain trust transmission, and ensures the trustworthiness of data-in-transit and cross-domain entities, further enhancing the security and reliability of authentication scheme.

- To avoid the complex certificate management and high cost in the conventional UAV authentication scheme, we utilize a certificateless signcryption algorithm without pairing operations for lightweight verification. The private blockchain enables intra-domain UAVs to jointly manage identity parameters, providing strict identity and permission management within the domain.

- To address concerns regarding the trustworthiness of UAVs, we have developed an efficient credit-based trust model. This model meticulously assesses the credibility of a UAV seeking cross-domain access by examining four key factors: the UAVâs own credibility, the credibility of its originating domain, the credibility of the target domain, and the degree of feature similarity between these domains. The credibility data, which is securely stored on a consortium blockchain, is then integrated into the authentication process. This integration significantly bolsters the reliability and robustness of the authentication mechanism.

- We provide security analysis and verification to consider multiple mainstream attacks to ensure the security and universality of the scheme. Moreover, simulations are conducted to evaluate the costs, latency, throughput and UAV energy consumption of the scheme. Theoretical analysis and simulation results prove the superiority of the scheme, especially the security and effectiveness of cross-domain authentication for the resource-limited UAVs.

Our work differs from existing research in three key aspects: 1) exploring promising cross-domain authentication schemes for multi-UAV networks; 2) achieving lightweight and decentralized identity authentication for highly mobile and resourceconstrained UAVs, significantly reducing communication and computing costs; and 3) addressing the trustworthiness of both data-in-transit and cross-domain entities.

The remainder of this paper is organized as follows. Section II reviews the related work. Section III presents the system model, threat model, and security notions. The details of the scheme are given in Section IV. Security analysis and extensive experiments are provided in Section V and VI. Finally, Section VII concludes the paper.

## II. RELATED WORK

Authentication schemes for UAV networks are receiving increasing research interets over the past decade. Considering the risk of unauthorized data access by UAVs, Khan et al. [19] proposed a UAV authentication scheme that combines digital signatures, hyperelliptic curve cryptography techniques, and hash functions. To achieve mutual authentication and anonymity for UAVs and entities, Tanveer et al. [20] established an authentication framework incorporating symmetric encryption and hash functions. These schemes rely on centralized third-party institutions, thus occurring problems such as costly management and single point of failure. Bhattarai et al. [21] utilized hash functions and bitwise xor to implement application-aware authentication protocol for UAVs and introduced physical unclonable functions (PUFs) to enhance resistance to physical cloning attacks. Yu et al. [22] presented a blockchain-enhanced authentication and key agreement scheme with privacy-preserving for UAVs, which guarantees essential security prerequisites while preventing severe security attacks. Huang et al. [23] proposed a blockchain-based authentication and key agreement scheme for UAVs. Blockchain and PUFs are introduced to improve the reliability of UAV communication and protect identity privacy. The stability and fault tolerance of PUFs make it exceptionally challenging to extract identical confidential information under adverse conditions. Xie et al. [24] introduced a blockchain-based authentication scheme that allows for the dynamic addition and removal of UAVs. However, the bilinear pairing operations utilized in this scheme incur significant authentication costs, particularly for UAVs with limited resources. Moreover, these authentication methods were designed to authenticate UAVs within a single domain, rendering them unsuitable for crossdomain applications.

Considering the development and support of future wireless networks, providing cross-domain authentication with communication security for UAVs has gradually received considerable research interest. The cross-domain UAV authentication scheme should ensure that the targeted domain accurately verifies the legitimacy of the UAVs without compromising the integrity of authentication protocol of the original domain. Tian et al. [25] presented a PUF-based authentication scheme for UAVs towards multi-domain settings. It samples the response of PUF based on the identity of the domain, which relies on thirdparty control server to achieve reusability. Khalid et al. [26] proposed an authentication protocol for out-of-zone flying UAVs, which combines symmetric and asymmetric techniques for key generation, message signing, encryption, and decryption during UAV authentication. However, the certificate authority adds substantial overhead and complexity of certificate management. Therefore, Given the distributed nature of UAVs operating in airspace, the collapse of the entire UAV system caused by a single point of failure of a ground station should be avoided, and therefore centralized certification approaches should be avoided. Feng et al. [27], [28] proposed a smart contract-based multi-signature scheme for cross-domain UAV authentication, but the computational cost of registering UAVs to smart contracts is high. Similarly, Pan et al. [29] aimed to achieve distributed low-altitude UAV identities authentication, yet bilinear pairing operations introduce significant overhead. Nair et al. [30] proposed a post-quantum protocol, but its intricate key management requirements, such as the distribution of large keys, impose a significant burden on UAVs. Shahidinejad et al. [31] applied chaotic maps in their blockchain-based protocol, which, despite ensuring anonymity, suffers from authentication delays due to nonlinear computations.

TABLE I COMPARISON OF EXISTING WORKS
<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>[19]</td><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1>[21]</td><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>[25]</td><td rowspan=1 colspan=1>[26]</td><td rowspan=1 colspan=1>[27]</td><td rowspan=1 colspan=1>[28]</td><td rowspan=1 colspan=1>[29]</td><td rowspan=1 colspan=1>[30]</td><td rowspan=1 colspan=1>[31]</td><td rowspan=1 colspan=1>Ours</td></tr><tr><td rowspan=1 colspan=1> $f _ { 1 }$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1> $\checkmark$ </td></tr><tr><td rowspan=1 colspan=1> $f _ { 2 }$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1> $f _ { 3 }$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1> $f _ { 4 }$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1> $f _ { 5 }$ </td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1> $f _ { 6 }$ </td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1> $f _ { 7 }$ </td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1> $f _ { 8 }$ </td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr></table>

â:Provide; X: Does Not Provide; f1: Identity Authentication; f2: Anonymity; f3: Lightweight Operation;  
$f _ { 4 } { \mathrm { : } }$ Data Confidentialityï¼f5: Data Integrity;f6: Entity Trustï¼f7:Decentralizationï¼f8:Support Cross-Domain.

In summary, while existing schemes partially address UAV authentication in cross-domain environments, most methods focus solely on verifying the trustworthiness of data or individual UAVs. In contrast, our work introduces a credit-based trust model that evaluates the trustworthiness of both data-in-transit and UAV entities. To support decentralized trust management and identity authentication across domains, we employ a distributed blockchain to store intra- and inter-domain trust information. Furthermore, to ensure the confidentiality and integrity of authentication information, we utilize a certificateless signcryption algorithm, enabling lightweight and efficient authentication suitable for resource-constrained UAVs. Finally, we compare the proposed scheme with existing schemes in Table 1.

<!-- image-->  
Fig. 1. System model.

## III. SYSTEM OVERVIEW

In this section, we present the system model, threat model, and security notions.

## A. System Model

The overall architecture of the cross-domain authentication system for UAVs is presented in Fig. 1. We generally consider a multi-UAV system where the UAVs are assigned to different domains according to their own features. The system contains the following components.

1) >UAV: UAVs have the ability to initiate cross-domain requests. Since each UAV within various domains possesses a unique identity, multiple pseudonyms, and legitimate information for identity verification. UAVs must undergo identity authentication before accessing other domains.

2) Domain edge server (DES): The DES is distributed at the network edge. It possesses strong computing capabilities and is used for pseudonym generation and identity authentication of UAVs.

3) Key generation center (KGC): The KGC is unique among all domains. KGC participates in the system parameters generation. In the entity registration phase, its role is to generate partial private keys for DES and terminal UAVs within the domain.

4) Blockchain: Each domain maintains a private blockchain to store UAVs information, such as public keys, pseudonyms, and account addresses. A consortium blockchain is applied for trust sharing among DESs across different domains.

## B. Threat Model

Given the security considerations of the proposed scheme, we employ the widely-recognized Dolev-Yao threat model [32]. The adversary has the capability to eavesdrop on messages within the UAV network and can also intercept and modify any information transmitted within the network. The adversary can access secret information stored within the UAVs and send messages or requests to all entities within the UAV network. Moreover, The adversary has the ability to impersonate any entity in the UAV network and send information on its behalf to other entities. However, the adversary lacks the ability to guess random numbers and control the DES.

## C. Security Notions

1) Security Requirements: To address the various issues that may be encountered in the cross-domain process of UAVs, the proposed scheme should meet the following requirements.

a) Message authentication: All cross-domain request messages from the UAV are encrypted and signed before being sent.

b) Non-repudiation: Once a UAV sends a cross-domain request or message, it cannot later deny its actions or the content of the communication.

c) Anonymity: All UAVs should remain anonymous during communication, and unauthorized entities must not be able to discern the UAVsâ true identities.

d) Forward secrecy: Even if a UAVâs secret key is compromised at a certain point, the session keys and communication contents from previous sessions remain confidential.

e) Unlinkability: The malicious adversary cannot infer the identity of the UAV sending the information based on the intercepted message.

f) Traceability: Although UAVs communicate anonymously over the network, the authorized entities should be able to trace the pseudonym of the UAV back to its real identity.

g) Resistance of replay attack: The system is capable of preventing adversaries from deceiving the system or gaining unauthorized access by capturing and replaying previously transmitted legitimate messages from UAVs.

2) Security Model: Considering security and privacy issues, this scheme should be able to withstand the various attacks mentioned above. Based on the adversaryâs behavior, adversaries can be classified into the following two types.

a) Type I Adversaries: A malicious UAV adversary $\boldsymbol { \mathcal { A } } _ { I }$ can replace any UAVâs public key but cannot obtain the master secret key s generated by the KGC.

b) Type II Adversaries: A malicious KGC adversary AII can obtain the master secret key s but cannot replace the UAVsâ public keys.

TABLE II  
NOTATION AND DESCRIPTION
<table><tr><td>Notations</td><td>Descriptions</td></tr><tr><td> $\overline { { D ^ { A } } }$ </td><td>The DES in domain A</td></tr><tr><td> $D I D ^ { A }$ </td><td>The identity of  $D ^ { A }$ </td></tr><tr><td> $D S K ^ { A } / D P K ^ { A }$ </td><td>The private/public key of  $D ^ { A }$ </td></tr><tr><td> $U _ { i } ^ { A }$ </td><td>The i-th UAV in domain A</td></tr><tr><td> $U I D _ { i } ^ { A }$ </td><td>The identity of  $U _ { i } ^ { A }$ </td></tr><tr><td> $P _ { U I D _ { i } ^ { A } }$ </td><td>The pseudonym of  $U _ { i } ^ { A }$ </td></tr><tr><td> $D _ { U I D _ { i } ^ { A } }$ </td><td>The partial private key of  $U _ { i } ^ { A }$ </td></tr><tr><td> $U S K _ { i } ^ { A } / U P K _ { i } ^ { A }$ </td><td>The private/public key of  $U _ { i } ^ { A }$ </td></tr><tr><td>â£</td><td>XOR operation</td></tr><tr><td> $a d d _ { i } ^ { A }$ </td><td>The blockchain account address</td></tr><tr><td> $\pi _ { i } ^ { A }$ </td><td>The temporary period</td></tr><tr><td> $C r _ { U }$ </td><td>The credibility of UAV</td></tr><tr><td> $C r _ { T }$ </td><td>The credibility of targeted domain</td></tr><tr><td> $C r _ { O }$ </td><td>The credibility of original domain</td></tr><tr><td> $C r _ { S } ( , )$ </td><td>The similarity credibility of two domains</td></tr></table>

## IV. PROPOSED SCHEME

The proposed scheme consists of four parts: the system initialization, the entity registration, the trust evaluation, and the cross-domain authentication process. Specifically, the signcrypt algorithm is based on [33]. We replace the original signature with the Edwards-curve Digital Signature Algorithm (EdDSA) signature [34] to offer improved security and performance. The symbols used are shown in Table 2.

## A. Overview of the Proposed Scheme

The proposed UAV cross-domain authentication scheme comprises four phases, which are described as follows:

1) System initialization: In this phase, the master key and system public parameters are generated, and the initial configuration of the UAV domain is completed.

2) Entity registration: The UAVs and DES within the domain obtain the information related to authentication, such as public/private key pairs, identities, pseudonyms, etc. Then, UAV uploads the related authentication parameters to the private blockchain.

3) Trust evaluation: The trust evaluation encompasses both UAV and domain trust. Specifically, the UAVâs trust is determined based on its historical behavior. Domain trust is assessed by calculating the credibility of both the UAVâs original domain and the target domain, as well as the similarity between the two domains.

4) Cross-domain authentication: The cross-domain authentication algorithm consists of intra-domain licensing and inter-domain authentication. Only UAVs with local domain permission can be authenticated by the DES of the targeted domain.

The cross-domain authentication process involves interactions between the entities mentioned above. First, the KGC needs register the DES and the UAVs separately. Notably, this registration process may have already been completed during the local authentication phase. The UAV sends a cross-domain license request to the DES within its current domain and obtain the relevant identity information. Subsequently, the DES queries the blockchain for the UAVâs trust information and then notifies the DES in the target domain, authorizing the UAV for cross-domain operations. The UAV then sends a cross-domain request to the target domainâs DES. After verifying the UAVâs identity and trust value, the DES within target domain grants permission for cross-domain operations. The communication flowchart diagram of the proposed scheme is shown in Fig. 2. Our proposed scheme is flexible and does not target any specific type of domain, such as geographical or task domains. Instead, it provides a general solution for cross-domain authentication that can support a wide range of multi-UAV operations across various geographic areas or different types of tasks.

<!-- image-->  
Fig. 2. The communication flowchart diagram.

Remark: In this paper, we deploy a private blockchain within each individual domain and a consortium blockchain that is collaboratively managed by multiple domains. The private blockchain supports UAV cross-domain licensing within a single domain, enabling strict identity and access management while ensuring data privacy and integrity within the domain. Meanwhile, the consortium blockchain serves to facilitate authentication and data sharing across various domains, establishing a trust mechanism that is jointly maintained for cross-domain access and multi-party interactions. This framework fosters inter-domain collaboration and the transfer of trust between different domains.

## B. System Initialization

1) System Setup: The KGC generates an elliptic curve group G of defined order q, where q and $P$ are the order and generator, respectively. Then, KGC determines its master secret key by choosing a value $s \in \mathbb { Z } _ { q } ^ { * }$ randomly, and computes $P _ { \mathrm { p u b } } = s P$ . Additionally, five hash functions are picked: $H _ { 0 } : \{ 0 , 1 \} ^ { l } \times G \times G \to \{ 0 , 1 \} ^ { l }$ $H _ { 1 } : \{ 0 , 1 \} ^ { l } \times G \times G \times G \to \mathbb { Z } _ { q } ^ { * } , \quad \quad \dot { H } _ { 2 } : \{ 0 , 1 \} ^ { l } \times \{ \dot { 0 , } 1 \} ^ { \bar { l } } \times$ $\begin{array} { r } { \dots \times \{ 0 , 1 \} ^ { l } \to \mathbb { Z } _ { q } ^ { * } , \quad H _ { 3 } : \{ 0 , 1 \} ^ { l } \times G \times G \to \{ 0 , 1 \} ^ { l } } \end{array}$ and

<!-- image-->  
Fig. 3. The UAV registration phase.

$H _ { 4 } : \{ 0 , 1 \} ^ { l } \times \{ 0 , 1 \} ^ { l } \times G \times G \to \mathbb { Z } _ { q } ^ { * }$ . Finally, the system : 0 1 0 1parameters of domain $p a r a m s = \{ G , q , P , P _ { \mathrm { p u b } } , H _ { 0 } , H _ { 1 } , H _ { 2 }$ $H _ { 3 } , H _ { 4 } \}$ is published.

2) Domain Configuration: To ensure that inter-domain authentication and communication are not constrained by the configurations of individual domains, during system initialization, the DESs of all domains share authentication schemes and cryptographic algorithms used for cross-domain purposes. It is worth noting that the sharing of this information does not constitute a security threat, as modern cryptographic designs adhere to Kerckhoffsâ principle [35].

## C. Entity Registration

At deployment time, entities in each domain perform this phase on the secure channel, including DES registration and UAV registration. First, using the key extraction algorithm of the signcryption scheme, the DES and UAV, with the assistance of the KGC, complete identity registration and generate their respective public/private key pairs. Then, in collaboration with the KGC, the DES uploads the UAVâs public key and pseudonym to the blockchain.

1) DES Registration: For example, the registration process of a DES $D ^ { A }$ in domain A is as follows.

a) $D ^ { A }$ sends its real identity $D I D ^ { A }$ to KGC. KGC generates a random number $\alpha ^ { A } \in \mathbb { Z } _ { q } ^ { * } .$ , and computes $T ^ { \bar { A } } = \alpha ^ { A } P$ and $h ^ { A } = H _ { 1 } ( D I D ^ { A } , T ^ { \dot { A } }$ , P , Ppub . Next, the KGC calculates $d _ { D I D ^ { A } } = s h ^ { A } + \alpha ^ { A }$ )mod q. Finally, KGC sends $D _ { D I D ^ { A } } = \{ d _ { D I D ^ { A } } , T ^ { A } \}$ to $D ^ { A }$

b) $D ^ { A }$ first checks $d _ { D I D ^ { A } } { \cal P } \overset { ? } { = } h ^ { A } P _ { \mathrm { p u b } } + T ^ { A }$ to decide whether to accept $D _ { D I D ^ { A } }$ =. Next, $\bar { D } ^ { A }$ +randomly selects a value $x _ { D I D ^ { A } } \in \mathbb { Z } _ { q } ^ { * }$ as its secret value. The private key of $D I D ^ { A }$ is $D S K ^ { A } = ( D _ { D I D ^ { A } } , x _ { D I D ^ { A } } )$ , the public key is ${ \cal D } P { \cal K } ^ { A } = \{ Q _ { { \cal D } I { \cal D } ^ { A } } , T ^ { A } \}$ , where $Q _ { D I D ^ { A } } = x _ { D I D ^ { A } } P$

= =2) UAV Registration: As depicted in Fig. 3, a UAV sends its real identity to the DES to obtain a corresponding pseudonym generated by the DES and public/private key pairs by the KGC.

Taking the i-th UAV $U _ { i } ^ { A }$ in domain A as an example, it executes this phase together with the DES and KGC.

In the UAV network, the use of the same pseudonym for an extended period will increase the leakage risk of the UAVâs real identity. Therefore, it is necessary for the UAV to update its pseudonym periodically. In the pseudonym generation stage, the UAV $U _ { i } ^ { \bar { A } }$ obtains its pseudonym as follows.

a) $\dot { U } _ { i } ^ { A }$ with identity $U I D _ { i } ^ { \bar { A } }$ generates a random number $r _ { i } ^ { A } \in$ $\mathbb { Z } _ { q } ^ { * } .$ , and computes $R _ { i } ^ { A } { = } r _ { i } ^ { A } P$ . Then it sends $\{ R _ { i } ^ { A } , U I \dot { D } _ { i } ^ { A } \}$ through a secure channel to $D ^ { A }$

b) $D ^ { A }$ verifies the validity of $U I D _ { i } ^ { A }$ . If $U I D _ { i } ^ { A }$ is valid, $D ^ { A }$ generates a temporary period $\pi _ { i } ^ { A }$ of identity and a pseudonym $P _ { U I D _ { i } ^ { A } } \bar { = } U I \bar { D } _ { i } ^ { \bar { A } } \oplus H _ { 0 } ( \bar { \pi _ { i } ^ { A } } , P _ { \mathrm { p u b } } , \omega _ { i } ^ { A } )$ , where $\omega _ { i } ^ { A } = x _ { D I D ^ { A } } R _ { i } ^ { A } . D ^ { A }$ generates a proof $\pi _ { \mathrm { Z K } }$ using zeroknowledge proof that $P _ { U I D _ { i } ^ { A } }$ is calculated as described above, without revealing its private key.

c) $D ^ { A }$ sends $P _ { U I D _ { i } ^ { A } }$ to $U _ { i } ^ { A }$ and $\{ P _ { U I D _ { i } ^ { A } } , \pi _ { i } ^ { A } , \pi _ { \mathrm { Z K } } \}$ to KGC through a secure channel.

In addition, during the UAV registration phase, a validity period $\pi _ { i } ^ { A }$ is set for each UAVâs pseudonym by DES. The expiration time of the pseudonym is determined by adding the respective validity period to the current time. When the pseudonym expires, the DES will send a re-registration request to the UAV, prompting the UAV to re-execute the registration phase. Additionally, a UAV can request multiple pseudonyms from the DES to maintain a list of pseudonyms. The UAV randomly selects a pseudonym from the pseudonym list to sign its message. Once a pseudonym is used, it will be discarded and no longer used.

In the private key extraction stage, the KGC generates a partial private key for the UAV as follows.

a) KGC receives $\{ P _ { U I D _ { i } ^ { A } } , \pi _ { i } ^ { A } , \pi _ { \mathrm { Z K } } \}$ from $D ^ { A }$ . It verifies ÏZK using zero-knowledge verification to confirm the correctness of $P _ { U I D _ { i } ^ { A } }$ . After successful verification, KGC generates a random number $\alpha _ { i } ^ { A } \in \mathbb { Z } _ { q } ^ { * }$ , and computes $T _ { i } ^ { A }$ $= \alpha _ { i } ^ { A } P , \ : h _ { i } ^ { A } = H _ { 1 } ( P _ { U I D _ { i } ^ { A } } , \ : T _ { i } ^ { A } , \ : \dot { P } , \ : P _ { \mathrm { p u b } } ) , \ : d _ { U I D _ { i } ^ { A } } =$ $s h _ { i } ^ { A } + \alpha _ { i } ^ { A }$ mod q. KGC generates a proof $\pi _ { \mathrm { Z K } } ^ { 2 }$ using +zero-knowledge proof that $d _ { U I D _ { i } ^ { A } }$ and $T _ { i }$ are calculated as described above, without revealing its private key.

b) KGC sends the partial private key $D _ { U I D _ { i } ^ { A } } = \{ d _ { U I D _ { i } ^ { A } }$ $T _ { i } ^ { A } , \pi _ { \mathrm { Z K } } ^ { 2 } \}$ and its to $U _ { i } ^ { A }$ through a secure channel.

In the key generation stage, the UAV can generate its secret keys as the following steps.

a) After receiving $D _ { U I D _ { i } ^ { A } } , ~ U _ { i } ^ { A }$ verifies $\pi _ { \mathrm { Z K } } ^ { 2 }$ using zeroknowledge verification to confirm the correctness of $d _ { U I D _ { i } ^ { A } }$ and $T _ { i } ^ { A } . U _ { i } ^ { A }$ verifies $d _ { U I D _ { i } ^ { A } } P { \stackrel { ? } { = } } h _ { i } ^ { A } P _ { \mathrm { p u b } } + T _ { i } ^ { A }$ and $P _ { U I D _ { i } ^ { A } } \stackrel { ? } { = } U I D _ { i } ^ { A } \oplus H _ { 0 } ( \pi _ { i } ^ { A } , P _ { \mathrm { p u b } } , R _ { i } ^ { A } )$ . If the verification = (passes, continue, otherwise request resend.

b) $U _ { i } ^ { A }$ chooses $x _ { U I D _ { i } ^ { A } } \in \mathbb { Z } _ { q } ^ { * }$ and calculates ${ \mathcal { H } } ( d _ { U I D _ { i } ^ { A } }$ $x _ { U I D _ { i } ^ { A } } ) = ( g _ { 0 } , g _ { 1 } , . . . , g _ { 2 l - 1 } )$ , where H is a hush function with 2l-bit output. Next, $U _ { i } ^ { A }$ sets $g _ { 0 } = g _ { 1 } = g _ { 2 } = g _ { l - 1 }$ $= 0$ and $g _ { l - 2 } = 1$ = =. Then a scalar is calculated as $x _ { L } =$ $\textstyle \sum _ { i = 0 } ^ { l - 1 } g _ { i } 2 ^ { \bar { i } }$ =mod q to obtain $X = x _ { L } P$ =, and the second half 2defined as $\boldsymbol { x } _ { R } = ( g _ { l } , . . . , g _ { 2 l - 1 } ) . \boldsymbol { U } _ { i } ^ { A }$ generates its private key $U S K _ { i } ^ { A } = ( D _ { U I D _ { i } ^ { A } } , x _ { U I D _ { i } ^ { A } } )$ . Then it computes $Q _ { U I D _ { i } ^ { A } }$ $= x _ { U I D _ { i } ^ { A } } P _ { }$ . The public key of $U _ { i } ^ { A }$ is $U P K _ { i } ^ { A } = \{ Q _ { U I D _ { i } ^ { A } }$ $T _ { i } ^ { A } \}$

c) $U _ { i } ^ { A }$ constructs a transaction $T x _ { p r i } = \{ P _ { U I D _ { i } ^ { A } } , U P K _ { i } ^ { A }$ $a d d _ { i } ^ { A } \}$ stored in the private blockchain, where $a d d _ { i } ^ { A }$ is the private blockchain account of $U _ { i } ^ { A }$

It is noted that $U _ { i } ^ { A }$ retains $\{ P _ { U I D _ { i } ^ { A } } , \bar { U } I D _ { i } ^ { A } , U P K _ { i } ^ { A } , U S K _ { i } ^ { A } \}$ in its memory. The DES maintains $\{ P _ { U I D _ { i } ^ { A } } , U I D _ { i } ^ { A } , D P K ^ { A }$ $D S K ^ { A } \}$ to trace the true identity of any UAV. The private blockchain keeps $\{ P _ { U I D _ { i } ^ { A } } , U P K _ { i } ^ { \mathbf { \bar { A } } } , a d d _ { i } ^ { \mathbf { \bar { A } } } \}$ of each registered UAV in the block.

## D. Trust Evaluation

Trust evaluation is the process of quantifying trustworthiness. In the proposed scheme, when an adversary originates within the domain and masquerades as a legitimate UAV, the concealment is typically more effective. Trust evaluation can maintain the integrity of UAVs within the domain by assessing their historical behaviors to evaluate performance and reliability.

1) UAV Trust Evaluation: During the authentication process, the targeted domain assesses the trustworthiness of guest UAV by utilizing UAVâs domain trust and self-evaluation trust. In the following, we present a credit-based trust model from [36] to evaluate the self-evaluation trusts of UAVs.

The self-evaluation credibility of UAV U is calculated based on its credibility $C r _ { U }$ . Particularly, $C r _ { U }$ is associated with $\mathrm { U A V } _ { \mathrm { \Delta } }$ behaviors. Good behavior can gradually enhance the trust value, whereas malicious behavior (e.g., failed authentication or non-mission UAV) can significantly damage it. Therefore, credibility is composed of the positive part $\hat { C r _ { U } ^ { P } }$ and negative part $C r _ { U } ^ { \bar { N } } . \ C r _ { U } ^ { P }$ is positively correlated with the number of successful authentication $n _ { U }$ of U and the targeted domains. The calculation of $\mathit { C r } _ { U } ^ { P }$ is defined as

$$
C r _ { U } ^ { P } = ( 1 + e ^ { - n _ { U } } ) ^ { - 1 } .\tag{1}
$$

Similarly, $C r _ { U } ^ { N }$ is negatively correlated with the number of misbehavior committed by U, which is defined as

$$
C r _ { U } ^ { N } = - \sum _ { j = 1 } ^ { m _ { U } } \alpha \left( \frac { \Delta T _ { U } ^ { N } } { t ^ { N } - t _ { j } ^ { N } } \right) ,\tag{2}
$$

where $m _ { U }$ is the number of malicious behaviors, Î± is the punishment factor, $T _ { U } ^ { N }$ is one unit of time, $t ^ { N }$ is the current time, and $t _ { j } ^ { N }$ is the time of occurrence of the j-th malicious behavior.

Therefore, the calculation of $C r _ { U }$ is described as

$$
C r _ { U } = \lambda _ { U } C r _ { U } ^ { P } + ( 1 - \lambda _ { U } ) C r _ { U } ^ { N } ,\tag{3}
$$

where $\lambda _ { U }$ is the adjustment coefficient.

The initial credibility of the UAV is set to 0.5, which changes as cross-domain authentication continues. The $C r _ { U }$ of UAV will be stored in the consortium blockchain by the DES within the domain.

2) Domain Trust Evaluation: Domain trust evaluation is divided into two categories, namely, the original domain trust and the targeted domain trust. Specifically, when a UAV seeks entry into a different domain, it is required to acquire permission from the DES of the local domain. The DES not only verifies the its legitimacy but also evaluates the credibility of both the UAV and the targeted domain. Similar to the UAV credibility, domain credibility will be uploaded to the blockchain by the corresponding DES.

The credibility of a targeted domain $\boldsymbol { C } \boldsymbol { r } _ { T }$ is related to its history of cooperation with other domains, including the frequency, reliability, and satisfaction of cooperation. The calculation of $\boldsymbol { C r } _ { T }$ is defined as

$$
\mathrm { C r } _ { T } = \lambda _ { T } ^ { 1 } \left( \frac { C _ { t o t } } { C _ { \operatorname* { m a x } } } \right) + \lambda _ { T } ^ { 2 } \left( \frac { C _ { s u c } } { C _ { t o t } } \right) + \left( 1 - \lambda _ { T } ^ { 1 } - \lambda _ { T } ^ { 2 } \right) F _ { a v g } ,\tag{4}
$$

where $\lambda _ { T } ^ { 1 } , \lambda _ { T } ^ { 2 }$ are adjustment coefficients, $C _ { t o t }$ indicates the total number of the targeted domain and other domains cooperated, $C _ { s u c }$ is the success rate of past cooperative tasks, $F _ { a v g }$ is the average feedback score from other domains (within the range of [0,1]), and $C _ { \mathrm { m a x } }$ is a constant representing the upper limit of cooperation to normalize the value.

Similarly, once the UAV receives license from its local domain, in addition to authenticating the UAVâs identity, the DES in the targeted domain needs to assess the UAVâs trust $C r _ { U }$ and its original domain trust $\mathit { C r } _ { \mathit { O } }$ . If the original domain maliciously provides false UAV identity information, it will seriously undermine the validity of the trust evaluation results and affect the security performance of the authentication framework. Therefore, CrO is related to the UAV trust level, which can be described as

$$
\mathbf { C r } _ { O } = \lambda _ { O } \frac { \sum _ { j = 1 } ^ { N _ { t o t } } C r _ { U } ^ { j } } { N _ { t o t } } + ( 1 - \lambda _ { O } ) ( 1 - e ^ { - \frac { N _ { s u c } } { N _ { l i c } } } ) ,\tag{5}
$$

where $\lambda _ { O }$ is the adjustment coefficient, $N _ { t o t }$ is the total UAV number of the original domain, $C r _ { U } ^ { j }$ is the self-evaluation trust of the j-th UAV, $N _ { l i c }$ is the number of UAVs that have license to access other domains, and $N _ { s u c }$ is the number of UAVs that get successfully authentication.

Furthermore, while considering the individual credibility of these two domains, it is also essential to evaluate their feature similarity. This assessment includes aspects such as similarity in task demands and historical task execution data. Significant disparities between the original domain and the targeted domain in these aspects may hinder the UAVâs adaptation to the new domainâs task demands and network environment post-crossing, thereby impacting the efficiency execution of tasks. The similarity between two domains A and B is defined as

$$
S i m ( A , B ) = \lambda _ { S } S _ { t a s k } + \left( 1 - \lambda _ { S } \right) S _ { h i s t } ,\tag{6}
$$

where $S _ { t a s k }$ and $S _ { h i s t }$ denote the similarity in task demands and historical task execution of A and B, which can be calculated by

$$
S _ { t a s k } = 1 - \frac { \sqrt { ( r _ { s } ^ { A } - r _ { s } ^ { B } ) ^ { 2 } + ( r _ { e } ^ { A } - r _ { e } ^ { B } ) ^ { 2 } } } { 2 } ,
$$

$$
S _ { h i s t } = 1 - \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \left( \frac { | b _ { i } ^ { A } - b _ { i } ^ { B } | + | d _ { i } ^ { A } - d _ { i } ^ { B } | } { b _ { i } ^ { A } + b _ { i } ^ { B } + d _ { i } ^ { A } + d _ { i } ^ { B } } \right) .
$$

Here, $r _ { s }$ and $r _ { e }$ are storage resource and energy resource requirements, n is the number of historical tasks, and $b _ { i } , d _ { i }$ are

<!-- image-->  
Fig. 4. The cross-domain authentication phase.

communication metrics about bandwidth and latency. Therefore, the corresponding similarity credibility can be mapped as

$$
C r _ { S } ( A , B ) = \gamma S i m ( A , B ) + \vartheta ,\tag{7}
$$

where $\gamma$ and $\vartheta$ are mapping parameters, which can be adjusted automatically.

It is noted that each UAV and domain is assigned an initial credibility upon joining the system, such as a default of 0.5. If historical data is available, the initial credibility can be dynamically calculated based on such data or domain attributes $( \mathrm { e . g . }$ , resource levels or historical task completion rates). To prevent new UAVs from failing cross-domain authentication due to credibility falling below the standard threshold $\theta _ { s } ,$ , the system sets a relaxed temporary authentication threshold $\theta _ { t e m p }$ (lower than the standard threshold) for UAVs applying for cross-domain authentication. The duration of the relaxed period can be defined by a specific time frame or task count (e.g., the first 5 authentication tasks). Once authentication begins, the credibility of UAVs and domains are dynamically adjusted based on the UAVâs authentication performance and recorded in the blockchain before UAV authentication, gradually reflecting their actual capabilities. The details of these updates will be presented in the next subsection.

## E. Cross-Domain Authentication

As shown in Fig. 4, the cross-domain authentication of UAV is divided into two phases. First, the UAV is required to obtain the cross-domain license from its local domain. Then, the authentication is perform by the targeted domain.

1) Intra-Domain Licensing: During the intra-domain licensing phase, this scheme will neither alter nor interfere with the original authentication methods adopted by each domain. In other words, UAVs within the domain will continue to authenticate according to the initial scheme. After the implementation of this scheme, UAVs that have completed intra-domain licensing will retain their respective privileges.

Assume that the edge serves for domains A and B are $D ^ { A }$ and $D ^ { B } . \mathrm { A U A V } U _ { i } ^ { A }$ in domain A prepares to access $B . U _ { i } ^ { A }$ first structures a cross-domain request $m _ { U } ^ { I } = \{ L i c , T a r _ { B } , \bar { P _ { U I D _ { i } ^ { A } } } .$ , $U P K _ { i } ^ { A } , t _ { U } ^ { I } \}$ , where Lic denotes the message type, $T a r _ { B }$ denotes the target domain, and $t _ { U } ^ { I }$ is current time. Then $U _ { i } ^ { A }$ sends the tuple $\{ m _ { U } ^ { I } , \sigma _ { m _ { U } ^ { I } } \}$ to $D ^ { A }$ , where $\sigma _ { m _ { \scriptscriptstyle { I } ) } ^ { I } }$ is its signature of $m _ { U } ^ { I }$

First, $D ^ { A }$ processes the request using the authentication scheme within the domain. Based on the UAVâs identity, a smart contract is invoked to query the public key of $U _ { i } ^ { A }$ from the private blockchain within the domain. If the UAV identity is valid, the corresponding public key of $U _ { i } ^ { A }$ is returned; otherwise, the search fails. Upon receiving the right feedback from the private blockchain, $U _ { i } ^ { \bar { A } }$ is confirmed as a legitimate UAV in domain A. Next, $D ^ { A }$ invokes a consortium blockchain contract function to query the credibility of $U _ { i } ^ { A }$ , the credibility of domain $B ,$ and the similarity between the two domains. The comprehensive trust of $U _ { i } ^ { A }$ for tagerted domain B is calculated as

$$
C r e _ { U } ^ { I } = \lambda _ { 1 } C r _ { U } + \lambda _ { 2 } C r _ { T } + ( 1 - \lambda _ { 1 } - \lambda _ { 2 } ) C r _ { S } ( A , B ) ,
$$

where $\lambda _ { 1 }$ and $\lambda _ { 2 }$ are the adjustment factors, and $\lambda _ { 1 } + \lambda _ { 2 }$ 1. For $C r e _ { U } ^ { I }$ =above a set threshold, the authentication in A is successful. Then, $D ^ { A }$ sends the authentication result to $U _ { i } ^ { A }$

Based on the authentication result, $D ^ { A }$ sends an authentication message encrypted and signed with the public key $D P K ^ { B }$ employing the encryption and signature schemes to $D ^ { B }$ of the target domain B. The plaintext message is structured as $m _ { D ^ { A } } ^ { I } = \{ \bar { C } r o L i c , O r i _ { A } , \bar { P _ { U I D _ { i } ^ { A } } } , I n f o _ { i } ^ { A } , \bar { U } P K _ { i } ^ { A } , t _ { D ^ { A } } ^ { I } \}$ = where CroLic denotes the message type, $O r i _ { A }$ denotes the original domain, $I n f o _ { i } ^ { A }$ denotes the real identity information of $U _ { i } ^ { A }$ , and $t _ { D A } ^ { I }$ is current time. Then $D ^ { A }$ sends the tuple $\{ E n c ( m _ { D ^ { A } } ^ { I } ) , \overline { { \sigma } } _ { m _ { D ^ { A } } ^ { I } } \}$ to $D ^ { B }$ , where $E n c ( m _ { D ^ { A } } ^ { I } )$ and $\sigma _ { m _ { D } ^ { I } _ { A } }$ are ciphertext and signature, respectively.

Upon receiving and decrypting the message from $D ^ { A } , D ^ { B }$ verifies the correctness of the signature and the legality of $I n f o _ { i } ^ { A }$ . After a successful verification, $D ^ { B }$ generates a license $L i c s = ( P _ { U I D _ { i } ^ { A } } , O r i _ { A } )$ and its signature $\sigma _ { L i c s ^ { B } }$ . Then $D ^ { B }$ i sends $\{ L i c s , \sigma _ { L i c s ^ { B } } \}$ to $D ^ { A }$ . Finally, $D ^ { A }$ verifies the signature and sends the license results from the domain B to $U _ { i } ^ { A }$

2) Inter-Domain Authentication: $U _ { i } ^ { A }$ initiates a crossdomain request after obtaining the license from $D ^ { B }$ . The plaintext format of the request is $\bar { \mathsf { m } _ { U } ^ { C } } = \{ A u t h e n , P _ { U I D _ { i } ^ { A } } , U \bar { P } K _ { i } ^ { A }$ , $t _ { U } ^ { C } \}$ , where Authen is the message type, and $t _ { U } ^ { C }$ is current time. Afterwards, $U _ { i } ^ { A }$ with $P _ { U I D _ { i } ^ { A } }$ and public key $\breve { U } P K _ { i } ^ { A }$ can signcrypt $m _ { U } ^ { C }$ to $D ^ { B }$ , who owns $\dot { D } I D ^ { B }$ and $D P K ^ { B }$ . Particularly, $U _ { i } ^ { \dot { A } }$ should perform the following steps:

a) $U _ { i } ^ { A }$ calculates $U = k _ { i } ^ { A } ( Q _ { U I D _ { i } ^ { A } } + T _ { i } ^ { A } + h _ { i } ^ { A } P _ { \mathrm { p u b } } )$ where $k _ { i } ^ { A } = H _ { 2 } ( x _ { R } , \ m _ { U } ^ { C } )$ . Then, $U _ { i } ^ { A }$ calculates $h ^ { B }$ $= \ H _ { 1 } ( \bar { D } I D ^ { B } , \ T ^ { B } , \ P , \ \bar { P } _ { \mathrm { p u b } } )$ and $\dot { Y } ~ = ~ H _ { 3 } ( D I D ^ { B }$ =U, $\begin{array} { r l r } { k _ { i } ^ { A } ( d _ { U I D _ { i } ^ { A } } } & { { } + } & { x _ { U I D _ { i } ^ { A } } ) ( h ^ { B } Q _ { D I D ^ { B } } + h _ { i } ^ { A } ( T ^ { B } + } \end{array}$ $h ^ { B } P _ { \mathrm { p u b } } ) )$ . Therefore, the ciphertext is constructed as $c =$ $Y \oplus { \dot { m } } _ { I J } ^ { C }$

b) Based on the previous calculations, $U _ { i } ^ { A }$ calculates $R =$ $k _ { i } ^ { A } P , \ r = \bar { H _ { 4 } } ( t , \ c , \ R , \ X )$ , and $\theta = r ( h _ { i } ^ { A } x _ { U I D _ { i } ^ { A } } \ +$ $h ^ { B } d _ { U I D _ { i } ^ { A } } ) + k _ { i } ^ { A }$ mod q. Finally, $U _ { i } ^ { A }$ transmits $\sigma = ( U$ $\theta , R , r , \dot { c } , t ) \mathrm { t o } D ^ { B } .$

Upon receiving $\sigma = ( U , \ \theta , \ R , \ r , \ c , \ t ) .$ $D ^ { B }$ first calls a =smart contract function on consortium blockchain to query and calculate the comprehensive trust of $U _ { i } ^ { A }$ within domain A as

$$
C r e _ { U } ^ { C } = \lambda _ { 3 } C r _ { U } + \lambda _ { 4 } C r _ { O } + ( 1 - \lambda _ { 3 } - \lambda _ { 4 } ) C r _ { S } ( A , B ) ,
$$

where $\lambda _ { 3 } + \lambda _ { 4 } = 1$ are the adjustment factors.

For $\mathit { C r e } _ { U } ^ { C }$ =above the threshold, the UAV trustworthiness is verified successfully. Then, $D ^ { B }$ requires to verify the trustworthiness of data-in-transit. $D ^ { B }$ computes $Y ^ { \prime } = H _ { 3 } ( D I D ^ { B }$ , U , $( h ^ { B } x _ { D I D ^ { B } } + h _ { i } ^ { A } d _ { D I D ^ { B } } ) U )$ and decrypts $m ^ { \prime } = Y ^ { \prime } \oplus c .$ Then, $\dot { D } ^ { B }$ computes $\bar { R } = \theta P - r ( h _ { i } ^ { A } Q _ { U I D _ { i } ^ { A } } + h ^ { B } ( T _ { i } ^ { A } + h _ { i } ^ { A } P _ { \mathrm { p u b } } ) )$ and verifies $r \overset { ? } { = } H _ { 4 } ( t , c , R , X )$ . If the overall verification is = ( )successful, the cross-domain authentication of $U _ { i } ^ { A }$ is complete.

## V. SECURITY PROOF AND ANALYSIS

In this section, we perform a security analysis using both formal analysis within the ROM model and informal analysis.

## A. Computational Assumptions

The security of the proposed scheme is based on the following hard problems.

Definition 1 (Computational Diffie-Hellman (CDH) assumption): Given a cyclic additive group $\mathbb { G }$ with the order q and a generator $G ,$ for two unknown integers $a , b \in \mathbb { Z } _ { a } ^ { * }$ and a tuple $( G ,$ $a G , b G )$ , the CDH assumption is to compute $a b G \in \mathbb { G }$

Definition 2 (Elliptic Curve Discrete Logarithm (ECDL) assumption): Given a cyclic additive group G with the order q and a generator G, for $a G = G _ { a }$ with unknown a $\in \mathbb { Z } _ { q } ^ { * }$ and $G _ { a } \in \mathbb { G }$ ï¼ =the ECDL assumption is to compute the value of a.

## B. Formal Analysis

This section discusses the resilience of our proposed scheme against the previously described adversary model.

Theorem 1 (Confidentiality): Assume that there is an adversary $\boldsymbol { \mathcal { A } } _ { I }$ that can make at most $q _ { p s k }$ extract-partial-private-key queries, $q _ { s k }$ extract-private-key queries, $q _ { s }$ signcrypt queries, $q _ { u }$ unsigncrypt queries, and $q _ { H _ { 3 } }$ hash queries of the random oracle $H _ { 3 } .$ . If $\boldsymbol { \mathcal { A } } _ { I }$ can win the IND-CCA2-I game of scheme with the probability at least Îµ in probability polynomial time (PPT), then a challenger $\boldsymbol { B } _ { 1 }$ can solve the CDH problem with a non-negligible advantage.

Proof: Supposing that $\boldsymbol { \mathcal { A } } _ { I }$ is able to break the confidentiality of the proposed scheme with a non-negligible probability, then $\boldsymbol { B } _ { 1 }$ has the ability to compute $a b P$ for solving the CDH problem instance $( P , a P , b P )$ by interacting with $\boldsymbol { \mathcal { A } } _ { I }$

Initial: $\boldsymbol { B } _ { 1 }$ generates $P _ { \mathrm { p u b } } = s P$ and params $= \{ G , q , P _ { \mathrm { { \ell } } }$ $P _ { \mathrm { p u b } } , H _ { 0 } , H _ { 1 } , H _ { 2 } , H _ { 3 } , H _ { 4 } \}$ = =. Then it submits params to $\boldsymbol { \mathcal { A } } _ { I }$

Phase $\mathbf { \Phi } _ { l \mathbf { : } } \ A _ { I }$ can issue some queries and $\boldsymbol { B } _ { 1 }$ answers these queries as follows:

. $H _ { 1 } â q u e r y . \ B _ { 1 }$ maintains a list $L _ { H _ { 1 } } \colon ( I D _ { i } , T _ { i } , P , P _ { \mathrm { p u b } } ,$ $h _ { i } )$ . Let $I D _ { i }$ and $I D _ { j }$ denote pseudo or real identities of the UAV and DES, respectively. When receiving a query $< I D _ { i } , T _ { i } , P , P _ { \mathrm { p u b } } >$ from $A _ { I } , B _ { 1 }$ retrieves $L _ { H _ { 1 } }$ to return the relevant value $h _ { i } \ t 0 \ A _ { I } .$ . If the searching fails, $\boldsymbol { B } _ { 1 }$ chooses a random value $h _ { i } \in \mathbb { Z } _ { q } ^ { * }$ and sets $h _ { i } = H _ { 1 } ( I D _ { i } , T _ { i } , P , P _ { \mathrm { p u b } } )$ Then $\boldsymbol { B } _ { 1 }$ sends $h _ { i }$ = (to AI and inserts it into $L _ { H _ { 1 } }$

. $H _ { 2 } â q u e r y . \ B _ { 1 }$ maintains a list $L _ { H _ { 2 } } \colon ( x _ { R _ { i } } , m _ { i } , k _ { i } )$ . After receiving a query $< x _ { R _ { i } } , m _ { i } >$ from $A _ { I } , B _ { 1 }$ looks up $L _ { H _ { 2 } }$ to send the corresponding $k _ { i } \mathrm { t o } \mathcal { A } _ { I } .$ If it fails, $\boldsymbol { B } _ { 1 }$ randomly picks $k _ { i } \in \mathbb { Z } _ { q } ^ { * }$ as the target value. Finally, $\boldsymbol { B } _ { 1 }$ inserts it into $L _ { H _ { 2 } }$

. $H _ { 3 } â q u e r y . \ B _ { 1 }$ maintains a list $L _ { H _ { 3 } } \colon ( I D _ { i } , U _ { i } , V _ { i } , Y _ { i } ) . B _ { 1 }$ sets $V _ { i } = ( h _ { j } x _ { I D _ { j } } + h _ { i } d _ { I D _ { j } } ) U _ { i }$ . When receiving a query $< I D _ { i } , U _ { i } , V _ { i } >$ +from $\boldsymbol { \mathcal { A } } _ { I } , \boldsymbol { B } _ { 1 }$ )retrieves $L _ { H _ { 3 } }$ and returns the relevant value $Y _ { i }$ to $\boldsymbol { \mathcal { A } } _ { I }$ . Otherwise, $\boldsymbol { B } _ { 1 }$ sends a random value $Y _ { i }$ to $\boldsymbol { \mathcal { A } } _ { I }$ and inserts it into $L _ { H _ { 3 } }$

. $H _ { 4 } â q u e r y . B _ { 1 }$ maintains a list $L _ { H _ { 4 } } \colon ( t _ { i } , c _ { i } , R _ { i } , X _ { i } , r _ { i } )$ . For a query $< t _ { i } , c _ { i } , R _ { i } , X _ { i } >$ from $A _ { I } , B _ { 1 }$ first sends $r _ { i }$ in $L _ { H _ { 4 } }$ to $\boldsymbol { \mathcal { A } } _ { I }$ if it exists. Otherwise, $\boldsymbol { B } _ { 1 }$ randomly chooses $r _ { i } \in \mathbb { Z } _ { q } ^ { * }$ and sets $r _ { i } = H _ { 4 } ( t _ { i } , c _ { i } , R _ { i } , X _ { i } )$ . Next, $\boldsymbol { B } _ { 1 }$ returns $r _ { i }$ to $\boldsymbol { \mathcal { A } } _ { I }$ =and adds it to $L _ { H _ { 4 } }$

- H-query. $\boldsymbol { B } _ { 1 }$ maintains a list $L _ { { \mathcal { H } } } \colon ( d _ { I D _ { i } } , x _ { I D _ { i } } , ( g _ { 0 } , g _ { 1 } , . . . ,$ $g _ { 2 l - 1 } ) )$ . When receiving a query $< d _ { I D _ { i } } , x _ { I D _ { i } } >$ (from $\boldsymbol { \mathcal { A } } _ { I }$ $\boldsymbol { B } _ { 1 }$ executes similar operations as in $H _ { 1 } { \mathrm { - } } { \mathrm { q u e r y } } .$

- Create-user. $\boldsymbol { B } _ { 1 }$ maintains a list $L _ { c u } \colon ( I D _ { i } , P K _ { i } , x _ { I D _ { i } }$ $d _ { I D _ { i } } , ~ h _ { i } )$ . Let $I D _ { i ^ { * } }$ and $I D _ { j }$ denote two challenging pseudo or real identities. When $\boldsymbol { \mathcal { A } } _ { I }$ issues an identity generating request on $I D _ { i } , B _ { 1 }$ first retrieves the existence of $I D _ { i }$ in $L _ { c u } .$ . If it fails, $\boldsymbol { B } _ { 1 }$ chooses $x _ { I D _ { i } }$ to calculate $Q _ { I D _ { i } } . \mathrm { I f } I D _ { i } \ne I D _ { i ^ { * } } , { \cal B } _ { 1 }$ calculates $d _ { I D _ { i } } = s h _ { i } + \alpha _ { i }$ mod q and Ti Î±iP . Otherwise, $\boldsymbol { B } _ { 1 }$ sets $d _ { I D . }$ = +as an unknown =value. Finally, $\boldsymbol { B } _ { 1 }$ adds it to $L _ { c u }$

- Extract-partial-private-key-query: For the request on $I D _ { i }$ to query the partial private key from $A _ { I } , B _ { 1 }$ will look up $L _ { c u }$ to return $D _ { I D _ { i } }$ if $I D _ { i } = I D _ { i ^ { * } }$ . Otherwise, $\boldsymbol { B } _ { 1 }$ returns failure.

- Request-public-key-query: After receiving the query on $I D _ { i }$ from $A _ { I } , B _ { 1 }$ first retrieves $L _ { c u }$ to return the related $P K _ { i }$ . If it fails, it preforms create-user to generate $P K _ { i }$ and updates $L _ { c u }$

. Extract-private-key-query: After receiving the private key query on $I D _ { i }$ from $\boldsymbol { \mathcal { A } } _ { I } , \boldsymbol { B } _ { 1 }$ searches $L _ { H _ { 1 } }$ and $L _ { c u }$ to calculate $S K _ { i }$ . Otherwise, it executes create-user to generate $S K _ { i }$ . Finally, $\boldsymbol { B } _ { 1 }$ sends $S K _ { i } \ : \mathrm { t o } \ : \mathcal { A } _ { I }$

- Replace-public-key-query: If AI intends to replace $P K _ { i }$ $\mathbf { \Psi } = ( Q _ { I D _ { i } } , T _ { i } )$ with $P K _ { i } ^ { \prime } = ( Q _ { I D _ { i } } ^ { \prime } , T _ { i } ^ { \prime } )$ for $I D _ { i } , B _ { 1 }$ first re-=trieves $L _ { c u }$ and replaces $P K _ { i }$ with $P K _ { i } ^ { \prime }$ and sets $x _ { I D _ { i } } { = } \perp$ Then, $\boldsymbol { B } _ { 1 }$ inserts it into $L _ { c u }$

- Signcrypt-query: On the tuple $< I D _ { i } , I D _ { j } , m _ { i } , t _ { i } >$ from $\boldsymbol { \mathcal { A } } _ { I }$ , if $I D _ { i } \neq I D _ { i ^ { * } } , B _ { 1 }$ retrieves $L _ { c u }$ to obtain the corresponding items of $I D _ { i }$ and $I D _ { j }$ . Next, it calls Signcrypt algorithm to generate a ciphertext Ï and sends Ï to $\boldsymbol { \mathcal { A } } _ { I }$ . If $I D _ { i } = I D _ { i }$ â and $I D _ { j } \ne I D _ { j ^ { * } } , B _ { 1 }$ computes $X _ { i } = x _ { L _ { i } } P$ and $R _ { i } = k _ { i } P$ . Noted that $x _ { L _ { i } }$ and $k _ { i }$ =can be obtained by =performing H1-query and H2-query. Next, $\boldsymbol { B } _ { 1 }$ calculates $U _ { i } , Y _ { i } , c _ { i } , R _ { i } , r _ { i }$ , and $\theta _ { i }$ . Finally, $\boldsymbol { B } _ { 1 }$ sends $\sigma _ { i } = ( U _ { i } , \theta _ { i }$ $R _ { i } , r _ { i } , c _ { i } , t _ { i } ) \mathrm { t o } \mathcal { A } _ { I }$

- Unsigncrypt-query: On the tuple $< I D _ { i } , I D _ { j } , \sigma _ { i } >$ from $\boldsymbol { \mathcal { A } } _ { I }$ , if $I D _ { j } \ne I D _ { j ^ { * } } , B _ { 1 }$ retrieves $L _ { c u }$ to obtain the cor-=responding items of $I D _ { i }$ and $I D _ { j }$ . Then, it performs

Unsigncrypt algorithm to recover plaintext $m _ { i }$ and sends $m _ { i }$ to AI . If $I D _ { j } = I D _ { j }$ â and $I D _ { i } \neq I D _ { i ^ { * } } , B _ { 1 }$ computes $Y _ { i }$ =and decrypts mi. Next, $\boldsymbol { B } _ { 1 }$ =computes $\theta _ { i } P$ and verifies $r _ { i } \overset { ? } { = } H _ { 4 } ( t _ { i } , c _ { i } , R _ { i } , X _ { i } )$ . If they hold, $\boldsymbol { B } _ { 1 }$ sends $m _ { i }$ to $\boldsymbol { \mathcal { A } } _ { I }$

=Challenge: $\boldsymbol { \mathcal { A } } _ { I }$ )selects two messages $( m _ { 0 } , m _ { 1 } )$ with equal length, a UAV identity $I D _ { i ^ { * } }$ and a DES identity $I D _ { j ^ { * } } . \mathrm { ~ I f ~ } I D _ { i }$ $= I D _ { i }$ â and $I D _ { j } \ne I D _ { j ^ { * } } , B _ { 1 }$ sets $U _ { j ^ { * } }$ and $Y _ { j ^ { * } }$ . Next, $\boldsymbol { B } _ { 1 }$ picks =a random value $\iota \in \{ 0 , 1 \}$ to calculate $c _ { j ^ { * } }$ . Then, $\boldsymbol { B } _ { 1 }$ calculates $R _ { j ^ { * } } , r _ { j ^ { * } }$ , and $\theta _ { j ^ { * } }$ 0 1. Finally, $\boldsymbol { B } _ { 1 }$ sends $\sigma _ { j ^ { \ast } } = ( U _ { j ^ { \ast } } , \theta _ { j ^ { \ast } } , R _ { j ^ { \ast } } , r _ { j ^ { \ast } } , c _ { j ^ { \ast } }$ ï¼ $t _ { j ^ { * } } )$ to $\boldsymbol { \mathcal { A } } _ { I } .$

Phase 2: $\boldsymbol { \mathcal { A } } _ { I }$ is able to adaptively query as in Phase 1. However, it cannot make extract-partial-private-key-query and extract-private-key-query on $I D _ { i ^ { * } }$ and $I D _ { j ^ { * } }$ , and the unsigncrypt-query on $\theta _ { j ^ { \ast } }$ â .

Guess: $\boldsymbol { \mathcal { A } } _ { I }$ outputs $\iota ^ { \prime }$ as its answer. The challenge $H _ { 3 }$ -query is defined as

$$
V _ { j ^ { * } } = h _ { j ^ { * } } x _ { I D _ { j ^ { * } } } b P + h _ { j ^ { * } } x _ { I D _ { j ^ { * } } } u _ { i } P + h _ { i ^ { * } } a b P + h _ { i ^ { * } } a u _ { i } P .
$$

Then, the CDH problem can be concluded as

$$
a b P = h _ { j ^ { * } } ^ { - 1 } \left( V _ { j ^ { * } } - \left( a h _ { i ^ { * } } u _ { i } + b h _ { j ^ { * } } x _ { I D _ { j ^ { * } } } + h _ { j ^ { * } } x _ { I D _ { j ^ { * } } } u _ { i } \right) P \right) .
$$

$\boldsymbol { B } _ { 1 }$ can search $L _ { H _ { 3 } }$ to compute abP with a probability

$$
\varepsilon ^ { \prime } \geq \frac { 1 } { q ^ { 2 } } \cdot \varepsilon \cdot \frac { 1 } { q _ { H _ { 3 } } } \left( 1 - \frac { 2 } { q } \right) ^ { q _ { p s k } } \left( 1 - \frac { 1 } { q } \right) ^ { q _ { s k } } \left( 1 - \frac { 1 } { q ^ { 2 } } \right) ^ { q _ { s } }
$$

$$
\left( 1 - \frac { 1 } { q ^ { 2 } } \right) ^ { q _ { u } }
$$

$$
= \frac { \varepsilon } { q ^ { 2 } \cdot q _ { H _ { 3 } } } \left( 1 - \frac { 2 } { q } \right) ^ { q _ { p s k } } \left( 1 - \frac { 1 } { q } \right) ^ { q _ { s k } } \left( 1 - \frac { 1 } { q ^ { 2 } } \right) ^ { q _ { s } + q _ { u } } .
$$

Theorem $2 { \it \Delta } ( C o n f i d e n t i a l i t y ) .$ : Assume that an adversary $\boldsymbol { \mathcal { A } } _ { I I }$ can make the same queries as listed in Theorem 1. If $\boldsymbol { \mathcal { A } } _ { I I }$ is able to win the IND-CCA2-II game of scheme with Îµ in PPT, then a challenger $B _ { 2 }$ can address the CDH problem.

Proof: Supposing that $\boldsymbol { A } _ { I I }$ is able to break the confidentiality of the proposed scheme, then $B _ { 2 }$ has the ability to compute $a b P$ for solving the CDH problem by interacting with $\boldsymbol { \mathcal { A } } _ { I }$

Initial: $\boldsymbol { B } _ { 1 }$ generates $P _ { \mathrm { p u b } } = s P$ and params. Then it submits the params to $\boldsymbol { \mathcal { A } } _ { I I }$

Phase $l \colon A _ { I I }$ can issue some queries and $B _ { 2 }$ answers these queries as follows:

- Hash-query: $B _ { 2 }$ is able to answer the queries from $\boldsymbol { \mathcal { A } } _ { I I }$ by performing the operations as aforementioned $H _ { 1 } { - } q u e r y _ { : }$ H2-query, H3-query, H4-query, and ${ \mathcal { H } } { \mathrm { - } } q u e r y .$

. Create-user. $B _ { 2 }$ maintains a list $L _ { c u } \colon ( I D _ { i } , P K _ { i } , x _ { I D _ { i } } ,$ $d _ { I D _ { i } } , h _ { i } )$ . If $L _ { c u }$ contains no items related to $I D _ { i }$ from $\boldsymbol { A } _ { I I } , \boldsymbol { B } _ { 2 }$ randomly picks $x _ { I D _ { i } }$ . Next, $B _ { 2 }$ calculates $Q _ { I D _ { i } }$ $= a P$ and $d _ { I D _ { i } } = s h _ { i } + \alpha _ { i }$ mod $q .$ Finally, $B _ { 2 }$ inserts $< I D _ { i } , P K _ { i } , x _ { I D _ { i } } , d _ { I D _ { i } } , h _ { i } >$ into $L _ { c u } .$

- Extract-partial-private-key-query: After receiving the query on $I D _ { i }$ from $\boldsymbol { A } _ { I I } , ~ \boldsymbol { B } _ { 2 }$ searches $L _ { c u }$ and returns the related $D _ { I D _ { i } }$ of $I D _ { i }$ to $\boldsymbol { \mathcal { A } } _ { I I }$ . Otherwise, $B _ { 2 }$ executes create-user to generate $D _ { I D _ { i } }$ and updates $L _ { c u }$

Request-public-key-query: $B _ { 2 }$ is able to answer the queries from $\boldsymbol { \mathcal { A } } _ { I I }$ by performing the operations as aforementioned request-public-key-query.

Extract-private-key-query: For the query of $I D _ { i }$ from $\boldsymbol { \mathcal { A } } _ { I I }$ if $I D _ { i } \neq I D _ { i ^ { * } } , B _ { 2 }$ searches $L _ { c u }$ and returns $S K _ { i }$ of $I D _ { i }$ to $\boldsymbol { A } _ { I I }$ . Otherwise, the query is aborted.

Signcrypt-query: $B _ { 2 }$ is able to answer the queries from $\boldsymbol { \mathcal { A } } _ { I I }$ by performing the operations as aforementioned signcryptquery.

Unsigncrypt-query: $B _ { 2 }$ is able to answer the queries from $\boldsymbol { \mathcal { A } } _ { I I }$ by performing the operations as aforementioned unsigncrypt-query.

Challenge: Based on two messages $( m _ { 0 } , ~ m _ { 1 } )$ with equal length from $\boldsymbol { A } _ { I I } , \boldsymbol { B } _ { 2 }$ picks a random value $\iota \in \{ 0 , 1 \}$ . Then, $B _ { 2 }$ performs the same operations as What $\boldsymbol { B } _ { 1 }$ does. $B _ { 2 }$ 1sends $\sigma _ { j ^ { * } }$ $= ( U _ { j ^ { * } } , \theta _ { j ^ { * } } , R _ { j ^ { * } } , r _ { j ^ { * } } , c _ { j ^ { * } } , t _ { j ^ { * } } )$ to $\boldsymbol { A } _ { I I }$

Phase $2 \colon A _ { I I }$ is able to adaptively query as in Phase 1. However, it cannot make extract-private-key-query on $I D _ { i ^ { * } }$ and $I D _ { j ^ { * } }$ , and the unsigncrypt-query on $\theta _ { j ^ { * } }$

Guess: $\boldsymbol { \mathcal { A } } _ { I }$ outputs $\iota ^ { \prime }$ as its answer. The challenge $H _ { \mathrm { 3 } } â \mathbf { q u e r y }$ is defined as

$$
V _ { j ^ { * } } = h _ { j ^ { * } } a b P + h _ { j ^ { * } } a u _ { i } P + h _ { i ^ { * } } d _ { I D _ { j ^ { * } } } b P + h _ { i ^ { * } } d _ { I D _ { j ^ { * } } } u _ { i } P .
$$

Then, the CDH problem can be concluded as

$$
a b P = { h _ { j ^ { * } } } ^ { - 1 } \left( V _ { j ^ { * } } - \left( a h _ { j ^ { * } } u _ { i } + b h _ { i ^ { * } } d _ { I D _ { j ^ { * } } } + h _ { i ^ { * } } d _ { I D _ { j ^ { * } } } u _ { i } \right) P \right)
$$

$\boldsymbol { B } _ { 1 }$ can search $L _ { H _ { 3 } }$ to compute abP with a probability

$$
\begin{array} { l } { { \varepsilon ^ { \prime } \geq \displaystyle \frac { 1 } { q ^ { 2 } } \cdot \varepsilon \cdot \displaystyle \frac { 1 } { q _ { H _ { 3 } } } \left( 1 - \displaystyle \frac { 2 } { q } \right) ^ { q _ { s k } } \left( 1 - \displaystyle \frac { 1 } { q ^ { 2 } } \right) ^ { q _ { s } } \left( 1 - \displaystyle \frac { 1 } { q ^ { 2 } } \right) ^ { q _ { u } } } } \\ { { = \displaystyle \frac { \varepsilon } { q ^ { 2 } \cdot q _ { H _ { 3 } } } \left( 1 - \displaystyle \frac { 2 } { q } \right) ^ { q _ { s k } } \left( 1 - \displaystyle \frac { 1 } { q ^ { 2 } } \right) ^ { q _ { s } + q _ { u } } . } } \end{array}
$$

Theorem 3 (Unforgeability): Assume that there is an adversary $\boldsymbol { \mathcal { A } } _ { I }$ that can make at most $q _ { p s k }$ extract-partial-private-key queries, $q _ { s k }$ extract-private-key queries, $q _ { s }$ signcrypt queries, $q _ { u }$ unsigncrypt queries, and $q _ { H _ { 4 } }$ hash queries of the random oracle $H _ { 4 }$ . If $\boldsymbol { \mathcal { A } } _ { I }$ can win the EU-CMA-I game of scheme with the probability at least Îµ in PPT, then a challenger $\mathcal { C } _ { 1 }$ can solve the ECDL problem with a non-negligible advantage.

Proof: Supposing that $\boldsymbol { \mathcal { A } } _ { I }$ is able to break the unforgeability of the proposed scheme with a non-negligible probability, then $\mathcal { C } _ { 1 }$ has the ability to compute $a P$ for solving the ECDL problem instance $( P , a P )$ by interacting with $\boldsymbol { \mathcal { A } } _ { I }$

Initial: As with the Initial in the proof in Phase 1 of Theorem $1 , { \mathcal { C } } _ { 1 }$ generates $P _ { \mathrm { p u b } } = s P$ and params. Then params is published to $\boldsymbol { \mathcal { A } } _ { I }$

Attack $\mathcal { C } _ { 1 }$ maintains lists $L _ { H _ { 1 } } , L _ { H _ { 2 } } , L _ { H _ { 3 } } , L _ { H _ { 4 } } , L _ { \mathcal { H } }$ , and $L _ { c u }$ as presented in Phase 1 of Theorem 1. Then, $\mathcal { C } _ { 1 }$ is able to reply the queries from $\boldsymbol { \mathcal { A } } _ { I }$ for various oracles. In addition, $\mathcal { C } _ { 1 }$ sets $d _ { I D _ { i ^ { * } } } P = T _ { i ^ { * } } + h _ { i ^ { * } } P _ { \mathrm { p u b } } = a P ,$

= =Forgery: For the challenge identities $I D _ { i }$ and $I D _ { j } , A _ { I }$ is able to output a forged ciphertext $\sigma _ { i ^ { * } } = ( U _ { i ^ { * } } , \theta _ { i ^ { * } } , R _ { i ^ { * } } , r _ { i ^ { * } } , c _ { i ^ { * } } , t _ { i ^ { * } } ) . \mathcal { C } _ { 1 }$ =can employ the forking lemma in the literature [37] to obtain two ciphertext tuples. Next, $\mathcal { C } _ { 1 }$ calculates $r _ { i ^ { * } } ^ { \prime } = H _ { 4 } ( t _ { i ^ { * } } , c _ { i ^ { * } } , R _ { i ^ { * } } , X _ { i ^ { * } } )$ where $r _ { i ^ { * } } ^ { \prime } \neq r _ { i ^ { * } }$ = (â due to the different values returned by $H _ { 4 } . { \mathcal { C } } _ { 1 }$ outputs a valid ciphertext $\sigma _ { i ^ { * } } ^ { \prime } = ( U _ { i ^ { * } } , \theta _ { i ^ { * } } ^ { \prime } , R _ { i ^ { * } } , r _ { i ^ { * } } ^ { \prime } , c _ { i ^ { * } } , t _ { i ^ { * } } )$ . Then, =the ECDL problem can be concluded as

$$
a = \frac { ( \theta _ { i ^ { * } } - \theta _ { i ^ { * } } ^ { \prime } ) - h _ { i ^ { * } } x _ { I D _ { i ^ { * } } } \left( r _ { i ^ { * } } - r _ { i ^ { * } } ^ { \prime } \right) } { h _ { j ^ { * } } \left( r _ { i ^ { * } } - r _ { i ^ { * } } ^ { \prime } \right) }
$$

due to $R _ { i ^ { * } } = \theta _ { i ^ { * } } P - r _ { i ^ { * } } ( h _ { i ^ { * } } Q _ { I D _ { i ^ { * } } } + h _ { j ^ { * } } ( T _ { i ^ { * } } + h _ { i ^ { * } } P _ { \mathrm { p u b } } ) )$ and $R _ { i ^ { * } }$ $= \theta _ { i ^ { * } } P - r _ { i ^ { * } } ^ { \prime } ( h _ { i ^ { * } } Q _ { I D _ { i ^ { * } } } + h _ { j ^ { * } } ( T _ { i ^ { * } } + h _ { i ^ { * } } P _ { \mathrm { p u b } } ) )$

$\mathcal { C } _ { 1 }$ (can search $L _ { H _ { 4 } }$ to compute $a P$ ))with a probability

$$
\varepsilon ^ { \prime } \geq \frac { \varepsilon } { q ^ { 2 } \cdot q _ { H _ { 4 } } } \left( 1 - \frac { 2 } { q } \right) ^ { q _ { p s k } } \left( 1 - \frac { 1 } { q } \right) ^ { q _ { s k } } \left( 1 - \frac { 1 } { q ^ { 2 } } \right) ^ { q _ { s } + q _ { u } } .
$$

Theorem 4 (Unforgeability): Assume that there is an adversary $\boldsymbol { A } _ { I I }$ that can make the queries presented in Theorem 3. If $\boldsymbol { \mathcal { A } } _ { I I }$ can win the EU-CMA-II game of scheme with the probability at least Îµ in PPT, then a challenger $\mathcal { C } _ { 2 }$ can solve the ECDL problem with a non-negligible advantage.

Initial: The operations of $\boldsymbol { \mathcal { A } } _ { I I }$ and $\mathcal { C } _ { 2 }$ are same as in Theorem 3.

Attack: $\mathcal { C } _ { 2 }$ maintains the aforementioned lists presented in Phase 1 of Theorem 1 and replies adaptively queries from $\boldsymbol { \mathcal { A } } _ { I I }$ In addition, $\mathcal { C } _ { 2 }$ sets $Q _ { I D _ { i ^ { * } } } = a P$

=Forgery: As illustrated in Forgery of Theorem $3 , { \mathcal { C } } _ { 2 }$ outputs a valid ciphertext $\boldsymbol { \sigma } _ { i ^ { * } } ^ { \prime }$ to obtain $R _ { i ^ { * } }$ . Then, the ECDL problem can be concluded as

$$
a = \frac { ( \theta _ { i ^ { * } } - \theta _ { i ^ { * } } ^ { \prime } ) - h _ { j ^ { * } } d _ { I D _ { i ^ { * } } } \left( r _ { i ^ { * } } - r _ { i ^ { * } } ^ { \prime } \right) } { h _ { i ^ { * } } \left( r _ { i ^ { * } } - r _ { i ^ { * } } ^ { \prime } \right) } .
$$

Therefore, $\mathcal { C } _ { 1 }$ can search $L _ { H _ { 4 } }$ to compute $a P$ with a probability

$$
\varepsilon ^ { \prime } \geq \frac { \varepsilon } { q ^ { 2 } \cdot q _ { H _ { 4 } } } \left( 1 - \frac { 1 } { q } \right) ^ { q _ { s k } } \left( 1 - \frac { 1 } { q ^ { 2 } } \right) ^ { q _ { s } + q _ { u } } .
$$

## C. Informal Analysis

In this section, we analyze the security requirements previously proposed.

1) Message authentication: When a UAV initiates a crossdomain request, it need to encrypt and sign the message. The DES has the ability to verify the ciphertext, ensuring that the message has not been tampered with or forged by adversaries. Furthermore, the proposed scheme can resist both Type I and Type II adversaries, thus meeting the security requirements for message authentication.

2) Non-repudiation: From Theorems 3 and 4, it is evident that our scheme is unforgeable. A UAV that generates the ciphertext $\sigma$ cannot deny it. Furthermore, the DES in domain can retrieve a malicious UAVâs real identity through its pseudonym, thus ensuring that no UAV can repudiate its signature on a message.

3) Anonymity: All UAVs employ pseudonyms for communication, and their true identities are concealed from all adversaries except the DES.

4) Forward secrecy: Even if an adversary can forcibly break the UAVâs partial private key and secret value pairs $( D _ { U I D _ { i } ^ { A } } , x _ { U I D _ { i } ^ { A } } )$ , it would still be difficult for adversary to decipher the plaintext Ï. In the Signcryption process, the random number $k _ { i } ^ { A }$ is generated based on the hash of the private key and the message $m ,$ , mitigating the risks associated with using insecure random number generators. Therefore, it is difficult for the adversary to compute the session key $Y$ during the plaintext calculation, unless the CDH problem is solved.

<!-- image-->  
Fig. 5. Security verification results. (a) Using OFMC. (b) Using CL-AtSe.

5) Unlinkability: During the communication process, UAVs use different pseudonyms for each interaction. There is no correlation between the new pseudonyms and the old ones, making it impossible for adversaries to infer the previous pseudonyms from the new ones.

6) Traceability: When a UAV violates the law or performs malicious operations, the DES can retrieve the real identity corresponding to the pseudonym from its database $\{ P _ { U I D _ { i } ^ { A } } , U I D _ { i } ^ { A } \}$

7) Resistance of replay attack: In this attack, an adversary attempts a replay attack by replaying previously received legitimate messages. Nevertheless, since the message generated when the UAV initiates an authentication request includes a timestamp $T _ { s }$ , the DES will evaluate whether the request is a replay based on the $T _ { s }$ of the current message. Additionally, the use of random numbers in the Signcryption algorithm ensures that each signature is unique. Even if the same message is processed multiple times, the results will be different. Thus, the proposed scheme is able to resist replay attacks.

## D. Security Verification

In this paper, we employed the widely recognized AVISPA tool [38] to verify the security of the proposed scheme. AVISPA offers four backends, namely the on-the-fly model-checker (OFMC), the constraint-logic-based attack searcher (CL-AtSe), the SAT-based model-checker (SATMC), and the tree automatabased protocol analyzer (TA4SP). Since SATMC and TA4SP do not support bitwise XOR operations, we utilized the OFMC and CL-AtSe to evaluate the security. The high-level protocol specification language (HLPSL) facilitates the creation of protocol specifications, which are later validated using the AVISPA tool. It defines protocol participants and their interactions through basic and mandatory roles. In HLPSL, attackers can be modeled as legitimate participants in the communication, enabling the simulation of potential protocol attacks.

In our implementation, the basic roles include UAVs and the DES, while the mandatory roles encompass sessions, goals, the environment, and the attacker role. We conducted the security simulation of the scheme using the security protocol animator (SPAN) on a VirtualBox virtual machine running Ubuntu 10.10. SPAN assesses the potential for malicious attackers to exploit vulnerabilities based on the threat model. The simulation results using the OFMC and CL-AtSe backends are shown in Fig. 5, with all outputs were marked SAFE. This demonstrates that the proposed scheme meets security design standards and effectively mitigates potential attacks.

## VI. PERFORMANCE EVALUATION

## A. Experimental Environment and Benchmarks

In this section, comparative analysis of the proposed scheme in terms of computational and communication overhead is performed with some related schemes. To make the performance evaluation more fair and convenient, the proposed schemes are compared with the schemes of cross-domain authentication [26], [27], [29], [39], [40] and UAV authentication [19], [23], [41], [42] respectively. Our experiments were conducted on a virtual machine running Ubuntu 16.04.12 LTS within VMware Workstation 16.1.1 Pro, utilizing a system with an Intel Core i5-13600KF and 32GB of RAM. For cryptographic operations, we implemented Type D pairings from the pairing-based cryptography (PBC) library and used Libsodium in C++ language to perform the necessary computations. For the blockchain-related evaluation, we employed the Hyperledger Fabric 1.4 platform in Go language in conjunction with Hyperledger Caliper to assess the performance and scalability of the proposed solution in a decentralized environment. Specifically, a brief summary highlighting the central ideas of the UAV cross-domain authentication schemes [26], [27], [29] are given below:

1) Ref. [26]: Khalid et al. proposed an anonymous handover authentication protocol for UAVs across different domains. It consists of drone certificate requests, ground station server (GSS) certificates, drone-GSS mutual authentication and drone-drone authentication. In the drone certificate requests phase, the drone operators can control their drones by requesting a certificate from CA. During the GSS certificates phase, the ground station requests a certificate from the CA. In the drone-GSS mutual authentication phase, the drone mutually authenticates with GSS using its certificates. In the drone-drone authentication phase, drones within different domains verify encrypted and signed messages for authentication.

2) Ref. [27]: Feng et al. proposed an authentication scheme which adopts multisignature smart contract for crossdomain drones. It consists of identity management, session key negotiation, and cross-domain authentication. In the identity management phase, drones or smart mobile terminals can perform registration, deregistration, and renewal. In the session key negotiation phase, drones negotiate session keys by exchanging their public keys and generating cryptographically secure random numbers. During the cross-domain authentication phase, the KGC in the domain will call the smart contract on the consortium blockchain to query the registration information of the drone. Then the drone will generate the ciphertext and upload it to the blockchain for authentication.

3) Ref. [29]: Pan et al. proposed an authentication and access control scheme using identity-based signature and automatic dependent surveillance broadcast technologies. It involves three main phases: flight application, access reservation, and UAV access. Initially, UAVs communicate with the regulatory authority to secure airspace authorization. Next, the UAV invokes access reservation contract to schedule the necessary services. Service providers respond to these requests and prepare by caching UAV authentication information. Finally, based on the UAV access requests, the access point authenticates the UAV based on the locally cached information.

TABLE III COMPUTATIONAL OVERHEAD COMPARISON OF CROSS-DOMAIN AUTHENTICATION SCHEMES
<table><tr><td rowspan=1 colspan=1>Scheme</td><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>DES</td></tr><tr><td rowspan=1 colspan=1>[26]</td><td rowspan=1 colspan=1> $2 T _ { s e } + T _ { s d } + T _ { v }$ </td><td rowspan=1 colspan=1> $3 T _ { s e } + 2 T _ { s d } + 2 T _ { s } + T _ { v }$ </td></tr><tr><td rowspan=1 colspan=1>[27]</td><td rowspan=1 colspan=1> $3 T _ { m } + T _ { a }$ </td><td rowspan=1 colspan=1> $3 T _ { m } + T _ { a } + T _ { h } + 2 T _ { p }$ </td></tr><tr><td rowspan=1 colspan=1>[29]</td><td rowspan=1 colspan=1> $T _ { h } + T _ { p } + 4 T _ { e }$ </td><td rowspan=1 colspan=1> $\overline { { 2 T _ { m } + 2 T _ { a } + 4 T _ { h } + T _ { p } + 7 T _ { e } } }$ </td></tr><tr><td rowspan=1 colspan=1>[39]</td><td rowspan=1 colspan=1> $7 T _ { m } + 3 T _ { a } + 4 T _ { h } + T _ { v }$ </td><td rowspan=1 colspan=1> $5 T _ { m } + T _ { a } + 3 T _ { h } + 3 T _ { e } + T _ { s }$ </td></tr><tr><td rowspan=1 colspan=1>[40]</td><td rowspan=1 colspan=1> $7 T _ { m } + 3 T _ { a } + 4 T _ { h } + T _ { v }$ </td><td rowspan=1 colspan=1> $4 T _ { m } + T _ { a } + 3 T _ { h } + T _ { s }$ </td></tr><tr><td rowspan=1 colspan=1>Ours</td><td rowspan=1 colspan=1> $5 T _ { m } + 2 T _ { a } + 2 T _ { h }$ </td><td rowspan=1 colspan=1> $5 T _ { m } + 3 T _ { a } + 2 T _ { h }$ </td></tr></table>

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 6. The computational overhead comparison of various schemes. (a) Crossdomain authentication schemes. (b) UAV authentication schemes.

## B. Computational Overhead

To assess the computational overhead, we use a consistent method to compare the proposed scheme with other authentication schemes. We assume that all schemes employ identical cryptographic operations and standardize the scalar operation results across 1000 tests. The symbols $T _ { m } , T _ { a } , T _ { h } , T _ { p } , T _ { e } , T _ { s e } / T _ { s d }$ and $T _ { s } / T _ { v }$ denote the execute time required for âpoint multiplicationâ, âpoint additionâ, âhash functionâ, âpairingâ, âexponentiationâ, âsymmetrical encryption/decryptionâ, and âsignature/verificationâ operations, respectively. The average time required for these operations across 1000 tests are 1.065 ms, 0.012 ms, 0.001 ms, 3.179 ms, 0.981 ms, 0.158/ 0.147 ms, and 4.446/ 1.315 ms.

1) Cross-Domain Authentication: Table 3 gives a comparison of the computational overhead of different cross-domain authentication schemes. For fairness, we focus solely on the computational overhead related to authentication process. Fig. 6(a) shows the computational overhead comparison of UAV side and DES side. Firstly, we evaluate the computational overhead on the

TABLE IV  
COMPUTATION OVERHEAD COMPARISON OF UAV AUTHENTICATION SCHEMES
<table><tr><td rowspan=1 colspan=1>Scheme</td><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>DES</td></tr><tr><td rowspan=1 colspan=1>[19]</td><td rowspan=1 colspan=1> $7 T _ { m } + T _ { a } + 3 T _ { h }$ </td><td rowspan=1 colspan=1> $7 T _ { m } + T _ { a } + 3 T _ { h }$ </td></tr><tr><td rowspan=1 colspan=1>[23]1</td><td rowspan=1 colspan=1> $8 T _ { m } + T _ { a } + 9 T _ { h }$ </td><td rowspan=1 colspan=1> $8 T _ { m } + 6 T _ { h }$ </td></tr><tr><td rowspan=1 colspan=1>[23]Â²</td><td rowspan=1 colspan=1> $1 1 T _ { m } + T _ { a } + 7 T _ { h }$ </td><td rowspan=1 colspan=1> $1 1 T _ { m } + T _ { a } + 8 T _ { h }$ </td></tr><tr><td rowspan=1 colspan=1>[41]</td><td rowspan=1 colspan=1> $5 T _ { m } + 2 T _ { a } + 3 T _ { h }$ </td><td rowspan=1 colspan=1> $5 T _ { m } + 2 T _ { a } + 3 T _ { h }$ </td></tr><tr><td rowspan=1 colspan=1>[42]</td><td rowspan=1 colspan=1> $4 T _ { m } + T _ { a } + 9 T _ { h } + T _ { e }$ </td><td rowspan=1 colspan=1> $6 T _ { m } + 2 T _ { a } + 1 7 T _ { h }$ </td></tr><tr><td rowspan=1 colspan=1>Ours</td><td rowspan=1 colspan=1> $5 T _ { m } + 2 T _ { a } + 2 T _ { h }$ </td><td rowspan=1 colspan=1> $5 T _ { m } + 3 T _ { a } + 2 T _ { h }$ </td></tr></table>

UAV side or other devices. For the scheme proposed in [26], the UAVâs time cost is totaling approximately 1.778 ms. The UAVs in [27] performs operations leading to 3.027 ms. In scheme [29], UAVs requires a computational overhead of 7.103 ms. In [39], the user performs operations resulting in 8.81 ms. For [40], the time cost is totaling approximately 8.81 ms. On the DES side, or other devices handles the cross-domain requests, the computational costs for these schemes are 9.197 ms [26], 9.566 ms [27], 12.2 ms [29], 12.729 ms [39], and 8.721 ms [40]. Our proposed scheme requires 5.531 ms on the UAV side and 5.363 ms on the DES side. To sum up, the computational costs are totally 10.975 ms [26], 12.773 ms [27], 19.303 ms [29], 21.539 ms [39], and 17.531 ms [40], respectively.

2) UAV Authentication: For assessing the cross-domain authentication efficiency, we compare our proposed scheme with the one presented by other UAV authentication schemes. Table 4 shows the main conclusions drawn from the comparison. Similarly, we analyze the UAV and the authenticating party separately. For the computational overhead of UAV, seven multiplication, one addition, and three hash function operations exist in scheme [19], with a cost of 7.47 ms. In scheme [23], two types of authentication schemes are presented, that is UAV-2-ground control station (GCS) and UAV-2-UAV. In the UAV-2-GCS mechanism [23]1, the cryptographic primitive operations are totaling approximately 8.541 ms. The UAV-2-UAV [23]2 mechanism results in 11.734 ms. In scheme [41], the UAV performs operations leading to 5.352 ms. The UAV in scheme [42] requires approximately 5.262 ms. In our proposed scheme, the time cost is about 5.531 ms. On the DES side, the computational costs required for the authenticating device of other schemes are 7.47 ms [19], 8.526 ms [23]1, 11.735 ms [23]2, 5.352 ms [41], and 6.431 ms [42]. In addition, in our scheme, we can calculate that the time cost of DES is about 5.363 ms. As can be seen from Fig. 6(b), the proposed scheme achieves less computational cost.

The computational complexity of our scheme is primarily composed of signcryption, blockchain queries, unsigncryption, and trust calculation. Specifically, signcryption involves scalar multiplication and addition on the elliptic curve, with a computational complexity of O q , where q is the order of the elliptic (log )curve. The complexity of blockchain queries is O n , where (log )n is the number of transactions in the blockchain. Similarly, unsigncryption relies on elliptic curve operations and can be expressed as O q . The trust calculation is simply a weighted summation, with a time complexity of O . Therefore, the over-(1)all computational complexity of the scheme is O q   n .

TABLE V  
COMMUNICATION OVERHEAD COMPARISON OF CROSS-DOMAIN AUTHENTICATION SCHEMES
<table><tr><td rowspan=1 colspan=1>Scheme</td><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>DES</td></tr><tr><td rowspan=1 colspan=1>[26]</td><td rowspan=1 colspan=1> $L _ { z } + 2 L _ { i } + 4 L _ { p } + 6 L _ { h } + L _ { t }$ </td><td rowspan=1 colspan=1> $3 L _ { g }$ </td></tr><tr><td rowspan=1 colspan=1>[27]</td><td rowspan=1 colspan=1> $2 L _ { g } + 4 L _ { z } + 2 L _ { i }$ </td><td rowspan=1 colspan=1>äº</td></tr><tr><td rowspan=1 colspan=1>[29]</td><td rowspan=1 colspan=1> $2 L _ { g } + L _ { z } + L _ { p } + 2 L _ { i } + L _ { s }$ </td><td rowspan=1 colspan=1> $L _ { g } + L _ { z } + L _ { p } + 2 L _ { i } +$ Ls</td></tr><tr><td rowspan=1 colspan=1>[39]</td><td rowspan=1 colspan=1> $2 L _ { g } + L _ { h } + L _ { p } + L _ { i }$ </td><td rowspan=1 colspan=1> $L _ { g } + 2 L _ { z } + L _ { t }$ </td></tr><tr><td rowspan=1 colspan=1>[40]</td><td rowspan=1 colspan=1> $3 L _ { g } + L _ { s } + L _ { p } + 2 L _ { i } + L _ { t }$ </td><td rowspan=1 colspan=1> $L _ { s } + L _ { i } + L _ { t }$ </td></tr><tr><td rowspan=1 colspan=1>Ours</td><td rowspan=1 colspan=1> $2 L _ { g } + 2 L _ { z } + L _ { p } + L _ { t }$ </td><td rowspan=1 colspan=1></td></tr></table>

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 7. The communication overhead comparison of various schemes. (a) Cross-domain authentication schemes. (b) UAV authentication schemes.

## C. Communication Overhead

The communication costs of our scheme, along with those of the comparison schemes, are statistically analyzed. This analysis considers both the number of messages exchanged between entities during the authentication process and the bits required for message transmission. The length of an element in |G| $L _ { g }$ is 128 bytes. The length of an element in $| \mathbb { Z } _ { q } | \ L _ { z }$ is 20 bytes. The lengths of hash value $L _ { h }$ and signature $L _ { s }$ are both 32 bytes. The lengths of the plaintext $L _ { p } ,$ the identity $L _ { i } .$ , and the timestamp $L _ { t }$ are all 20 bytes.

1) Cross-Domain Authentication: As detailed in Table 5, the $^ { 6 6 } - ^ { 5 9 }$ in indicates no operations of the corresponding entity. Specifically, one message is interacted to accomplish the cross-domain authentication process. A UAV sends an authentication request Ï (U, Î¸, R, r, c, t) to the targeted domain, where U and =R are two elements in |G|, Î¸ and r are two elements in $\vert \mathbb { Z } _ { q } \vert$ c is a ciphertext, and t denotes a timestamp. Therefore, the total overhead of our scheme is about 336 bytes. Calculated by the above method, the results are shown in Fig. 7(a). For the communication overhead incurred by UAV, or other entities that make cross-domain requests, the communication overheads are 352 bytes [26], 376 bytes [27], 368 bytes [29], 328 bytes [39], and 496 bytes [40]. The communication costs of the other side, such as DES, GCS, et al. are 384 bytes [26], 240 bytes [29], 188 bytes [39], and 72 bytes [40]. Therefore, the total overhead of our proposed scheme is about 45.7% [26], 89.4% [27], 55.2% [29], 65.1% [39], 59.2% [40].

2) UAV Authentication: Table 6 gives the detailed communication overhead of various schemes. From Fig. 7(b), we can obtain that the communication overhead required for the authenticated UAV in schemes [19], [23]1, [23]2, [41], [42] are

TABLE VI  
COMMUNICATION OVERHEAD COMPARISON OF UAV AUTHENTICATION SCHEMES
<table><tr><td rowspan=1 colspan=1>Scheme</td><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>DES</td></tr><tr><td rowspan=1 colspan=1>[19]</td><td rowspan=1 colspan=1> $L _ { g } + L _ { z } + L _ { h } + L _ { i } + L _ { t }$ </td><td rowspan=1 colspan=1> $L _ { g } + L _ { z } + L _ { h } + L _ { i } + L _ { t }$ </td></tr><tr><td rowspan=1 colspan=1>[23]1</td><td rowspan=1 colspan=1> $2 L _ { g } + 2 L _ { z } + 3 L _ { h } + L _ { i } +$ 2Lt</td><td rowspan=1 colspan=1> $L _ { g } + L _ { z } + L _ { h } + L _ { t }$ </td></tr><tr><td rowspan=1 colspan=1>[23]2</td><td rowspan=1 colspan=1> $L _ { g } + L _ { h } + L _ { i } + L _ { t } + L _ { m }$ </td><td rowspan=1 colspan=1> $\begin{array} { c } { { L _ { g } + 3 L _ { h } + L _ { i } + 3 L _ { t } + } } \\ { { L _ { m } } } \end{array}$ </td></tr><tr><td rowspan=1 colspan=1>[41]</td><td rowspan=1 colspan=1> $\begin{array} { c } { { L _ { g } + L _ { z } + 2 L _ { h } + L _ { i } + } } \\ { { 2 L _ { t } } } \end{array}$ </td><td rowspan=1 colspan=1> $L _ { g } + L _ { z } + L _ { h } + L _ { i } + L _ { t }$ </td></tr><tr><td rowspan=1 colspan=1>[42]</td><td rowspan=1 colspan=1> $L _ { g } + 3 L _ { h } + L _ { i } + L _ { t }$ </td><td rowspan=1 colspan=1> $L _ { g } + L _ { h } + L _ { i } + L _ { t }$ </td></tr><tr><td rowspan=1 colspan=1>Ours</td><td rowspan=1 colspan=1> $2 L _ { g } + 2 L _ { z } + L _ { m } + L _ { t }$ </td><td rowspan=1 colspan=1></td></tr></table>

220 bytes, 452 bytes, 220 bytes, 272 bytes, and 264 bytes. For the DES or entities that authenticate UAVs, the communication overheads are 220 bytes [19], 200 bytes [23]1, 324 bytes [23]2, 220 bytes [41], 200 bytes [42], respectively. Therefore, the total communication overhead of our proposed scheme is about 65.1% [19], 51.5% [23]1, 61.8% [23]2, 76.4% [41], and 72.4% [42].

In summary, compared with other cross-domain authentication schemes, whether itâs the cross-domain of UAVs or other entities, the proposed scheme has less computational and communication overhead, thereby making it more suitable for resource-constrained UAV networks. Compared with UAV authentication scheme, the proposed scheme also outperforms effectiveness and superiority than existing methods.

## D. Communication Performance

To validate the superior communication performance of the proposed scheme, we conducted a series of detailed experimental analyses. The focus is placed on comparing our scheme with existing approaches in terms of system blockchain latency, throughput, and UAV energy consumption.

1) Latency: For the latency of blockchain, we configured the consortium blockchain nodes using Docker 20.10.7 containers with the Hyperledger Fabric 1.4.1 platform on Ubuntu 16.04 virtual machines. The clients, emulating UAVs and DES, run on a Windows 11 host. Interactions between clients and the blockchain are handled through the Fabric Java SDK, while the smart contract is implemented in Go language. To assess the additional latency introduced when writing to or querying data from the blockchain, we initially created a concurrent process script to simulate parallel data writing and querying across two different domains. We then performed writing and querying operations based on the deployed chaincode. For a configuration with one orderer node and one peer node, the average time for each write operation was 6.2 ms, while each query took an average of 1.85 ms. In schemes [29] and [23]1, three writing and one querying operations are performed. Two writing and two querying operations exist in schemes [27] and [23]. 2 Scheme [40] performs four querying operations. However, since no ledger modification operations exist, only one querying operation is required in ours and scheme [39]. Therefore, as detailed in Fig. 8(a), our proposed scheme and scheme [39] achieves the lowest latency of 1.85 ms, outperforming than 7.4 ms [40], 16.1 ms [27], [23]2, and 20.45 ms [29], [23]1.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 8. (a) Blockchain latency comparison. (b) Throughput comparison. (c) Energy consumption comparison.

2) Throughput: Throughput is used to evaluate the efficiency of data transmission during the authentication process, defined as the amount of data successfully transmitted per unit time. We conducted simulation experiments to analyze the data volume and transmission delays of different schemes. The transmitted data sizes in these schemes are 376 bytes [27], 608 bytes [29], 516 bytes [39], 568 bytes [40], 652 bytes [23]1, and 544 bytes [23]2. The corresponding transmission delays, encompassing computational costs and blockchain delays, are 28.873 ms [27], 39.753 ms [29], 23.389 ms [39], 24.931 ms [40], 37.517 ms [23]1, and 39.569 ms [23]. 2 In our proposed scheme, the communication data sizes and corresponding delays are 336 bytes and 12.564 ms. The throughput result is shown in Fig. 8(b). The throughput of the compared are 0.094 Mbps [27], 0.109 Mbps [29], 0.15 Mbps [39], 0.154 Mbps [40], 0.122 Mbps [23]1, and 0.099 Mbps [23]2, which are lower than ours of 0.176Mbps. Although the proposed scheme transmits a smaller amount of data, it requires less transmission time. This indicates that the proposed scheme achieves better communication efficiency.

3) Energy Consumption: Energy consumption is a critical performance metric that directly affects system endurance and resource utilization efficiency during the UAV cross-domain authentication process. In our evaluation, we consider UAVs operating at altitudes ranging from 200 to 500 meters, with a maximum flight speed of $V _ { \mathrm { m a x } } = 4 0 ~ \mathrm { m / s }$ . The energy analysis is conducted under the following assumptions: noise power $\delta ^ { 2 }$ is set to â dBm/Hz, transmission power $P _ { i }$ is 1W, available 130bandwidth B is 1 MHz, and the energy consumption coefficient $\rho$ is $1 . 4 2 \times 1 0 ^ { 3 }$ . We compare the energy consumption of our 1 42 10proposed scheme against several representative cross-domain authentication approaches for UAV networks [26], [27], [29], considering varying numbers of UAVs. The size of transmitted data in these schemes is 352 bytes [26], 376 bytes [27], 368 bytes [29], and 336 bytes in our proposed scheme. As illustrated in Fig. 8(c), the proposed method achieves significant energy savings, with UAV energy consumption reduced by approximately 53.6%, 29.4%, and 38.4% compared to the schemes in [26], [27], and [29], respectively. This improvement is primarily attributed to the reduced data transmission overhead in our design.

According to the performance analysis, our proposed scheme offers several advantages. In terms of computational cost, it benefits from the lightweight signcryption algorithm, resulting in lower costs compared to other related schemes. Regarding communication overhead, our scheme incurs the least cost. On the latency cost, it performs better due to fewer smart contract invocation operations. Finally, in terms of throughput and energy cost, the proposed scheme excels by reducing data volume and transmission time.

## VII. CONCLUSION

As the demand for resource sharing and access across multiple domains in UAV networks continues to grow, the issue of information theft or malicious access by unauthorized UAVs has become a focal point of concern, making cross-domain authentication has become a key means of ensuring information security. To tackle this issue, we proposed a blockchain-based lightweight and trusted cross-domain authentication scheme for resourceconstrained UAVs. To eliminate the additional overhead of UAV certificate management, a certificateless signcryption algorithm is employed to authenticate UAVs. An efficient credit-based trust model is designed to calculated the corresponding credibility of UAVs and domains, thereby enhancing the reliability of the authentication. Moreover, a private blockchain stored the UAV information and a consortium blockchain with the credibility information are introduced to realize decentralized authentication. Although our proposed scheme outperforms existing schemes, we still notice potential for further improvements. Specifically, addressing the scalability requirements in large-scale UAV networks remains a non-trivial problem. As a future work, we plan to focus on designing and analyzing batch cross-domain authentication schemes for multiple UAVs, which will allow simultaneous authentication of numerous UAVs across different domains with minimal computational overhead.

## REFERENCES

[1] H. Kurunathan, H. Huang, K. Li, W. Ni, and E. Hossain, âMachine learning-aided operations and communications of unmanned aerial vehicles: A contemporary survey,â IEEE Commun. Surveys Tuts., vol. 26, no. 1, pp. 496â533, Firstquarter 2024.

[2] J. Chen, J. Wang, J. Wang, and L. Bai, âJoint fairness and efficiency optimization for CSMA/CA-based multi-user MIMO UAV Ad Hoc networks,â IEEE J. Sel. Topics Signal Process., vol. 18, no. 7, pp. 1311â1323, Oct. 2024.

[3] G. Sun et al., âJoint task offloading and resource allocation in aerialterrestrial UAV networks with edge and fog computing for post-disaster rescue,â IEEE Trans. Mobile Comput., vol. 23, no. 9, pp. 8582â8600, Sep. 2024.

[4] X. Hou, J. Wang, C. Jiang, Z. Meng, J. Chen, and Y. Ren, âEfficient federated learning for metaverse via dynamic user selection, gradient quantization and resource allocation,â IEEE J. Sel. Areas Commun., vol. 42, no. 4, pp. 850â866, Apr. 2024.

[5] C. Pu, C. Warner, K.-K. R. Choo, S. Lim, and I. Ahmed, âlitegap: Lightweight group authentication protocol for internet of drones systems,â IEEE Trans. Veh. Technol., vol. 73, no. 4, pp. 5849â5860, Apr. 2024.

[6] R. Karmakar, G. Kaddoum, and O. Akhrif, âA blockchain-based distributed and intelligent clustering-enabled authentication protocol for UAV swarms,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 6178â6195, May 2024.

[7] A. Aldaej, M. Atiquzzaman, T. A. Ahanger, and P. K. Shukla, âMultidomain blockchain-based intelligent routing in UAV-IoT networks,â Comput. Commun., vol. 205, pp. 158â169, 2023.

[8] B. Chai, J. Yu, B. Yan, Y. Yu, and S. Wang, âBSCDA: Blockchain-based secure cross-domain data access scheme for Internet of Things,â IEEE Trans. Netw. Service Manag., vol. 21, no. 4, pp. 4006â4023, Aug. 2024.

[9] M. A. El-Zawawy, A. Brighente, and M. Conti, âAuthenticating drone-assisted internet of vehicles using elliptic curve cryptography and blockchain,â IEEE Trans. Netw. Service Manag., vol. 20, no. 2, pp. 1775â1789, Jun. 2023.

[10] J. Miao, Z. Z. Wang, X. Ning, A. Shankar, C. Maple, and J. J. Rodrigues, âA UAV-assisted authentication protocol for Internet of Vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 8, pp. 10286â10297, Aug. 2024.

[11] W. Wang, Z. Han, T. R. Gadekallu, S. Raza, J. Tanveer, and C. Su, âLightweight blockchain-enhanced mutual authentication protocol for UAVs,â IEEE Internet Things J., vol. 11, no. 6, pp. 9547â9557, Mar. 2024.

[12] F. Tong, X. Chen, K. Wang, and Y. Zhang, âCCAP: A complete crossdomain authentication based on blockchain for Internet of Things,â IEEE Trans. Inf. Forensics Secur., vol. 17, pp. 3789â3800, 2022.

[13] C. Wang, Y. Zhang, Q. Zhang, X. Xu, W. Chen, and H. Li, âSE-CAS: Secure and efficient cross-domain authentication scheme based on blockchain for space tt&c networks,â IEEE Internet Things J., vol. 11, no. 16, pp. 26806â26818, Aug. 2024.

[14] M. Xie et al., âTraceability and identity protection in smart agricultural IoT system framework based on blockchains,â IEEE Trans. Dependable Secure Comput., early access, Apr. 29, 2025, doi: 10.1109/TDSC.2025.3565593.

[15] Y. Tan, J. Liu, and N. Kato, âBlockchain-based lightweight authentication for resilient UAV communications: Architecture, scheme, and future directions,â IEEE Wireless Commun., vol. 29, no. 3, pp. 24â31, Jun. 2022.

[16] J. Wang, Z. Jiao, J. Chen, X. Hou, T. Yang, and D. Lan, âBlockchain-aided secure access control for UAV computing networks,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 6, pp. 5267â5279, Nov./Dec. 2024.

[17] B. Wang, Z. Chang, S. Li, and T. HÃ¤mÃ¤lÃ¤inen, âAn efficient and privacypreserving blockchain-based authentication scheme for low earth orbit satellite-assisted Internet of Things,â IEEE Trans. Aerosp. Electron. Syst., vol. 58, no. 6, pp. 5153â5164, Dec. 2022.

[18] B. Li et al., âTrust management strategy for digital twins in vehicular ad hoc networks,â IEEE J. Sel. Areas Commun., vol. 41, no. 10, pp. 3279â3292, Oct. 2023.

[19] M. A. Khan et al., âA provable and privacy-preserving authentication scheme for UAV-enabled intelligent transportation systems,â IEEE Trans. Ind. Informat., vol. 18, no. 5, pp. 3416â3425, May 2022.

[20] M. Tanveer, H. Alasmary, N. Kumar, and A. Nayak, âSAAF-IoD: Secure and anonymous authentication framework for the internet of drones,â IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 232â244, Jan. 2024.

[21] I. Bhattarai, C. Pu, K.-K. R. Choo, and D. KoraÂ´c, âA lightweight and anonymous application-aware authentication and key agreement protocol for the internet of drones,â IEEE Internet Things J., vol. 11, no. 11, pp. 19790â19803, Jun. 2024.

[22] S. Yu, A. K. Das, and Y. Park, âRLBA-UAV: A robust and lightweight blockchain-based authentication and key agreement scheme for PUFenabled UAVs,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 12, pp. 21697â21708, Dec. 2024.

[23] K. Huang, H. Hu, and C. Lin, âBakas-uav: A secure blockchain-assisted authentication and key agreement scheme for unmanned aerial vehicles networks,â IEEE Internet Things J., vol. 11, no. 22, pp. 36858â36883, Nov. 2024.

[24] M. Xie, Z. Chang, H. Li, and G. Min, âBASUV: A blockchain-enabled UAV authentication scheme for Internet of Vehicles,â IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 9055â9069, 2024.

[25] C. Tian, Q. Jiang, T. Li, J. Zhang, N. Xi, and J. Ma, âReliable PUF-based mutual authentication protocol for UAVs towards multi-domain environment,â Comput. Netw., vol. 218, 2022, Art. no. 109421.

[26] H. Khalid et al., âHOOPOE: High performance and efficient anonymous handover authentication protocol for flying out of zone UAVs,â IEEE Trans. Veh. Technol., vol. 72, no. 8, pp. 10906â10920, Aug. 2023.

[27] C. Feng, B. Liu, Z. Guo, K. Yu, Z. Qin, and K.-K. R. Choo, âBlockchainbased cross-domain authentication for intelligent 5g-enabled internet of drones,â IEEE Internet Things J., vol. 9, no. 8, pp. 6224â6238, Apr. 2022.

[28] C. Feng, B. Liu, K. Yu, S. K. Goudos, and S. Wan, âBlockchain-empowered decentralized horizontal federated learning for 5G-enabled UAVs,â IEEE Trans. Ind. Inform., vol. 18, no. 5, pp. 3582â3592, May 2022.

[29] H. Pan, P. Cao, W. Wang, Y. Liu, and Z. Yin, âBlockchain-assisted crossdomain authentication and access control for low-altitude UAV,â in Proc. IEEE/CIC Int. Conf. Commun. China, 2023, pp. 1â6.

[30] A. S. Nair, S. M. Thampi, and V. Jafeel, âA post-quantum secure PUF based cross-domain authentication mechanism for internet of drones,â Veh. Commun., vol. 47, 2024, Art. no. 100780.

[31] A. Shahidinejad and J. Abawajy, âAnonymous blockchain-assisted authentication protocols for secure cross-domain iod communications,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 3, pp. 34924â34940, May/Jun. 2024.

[32] D. Dolev and A. Yao, âOn the security of public key protocols,â IEEE Trans. Inf. Theory, vol. 29, no. 2, pp. 198â208, Mar. 1983.

[33] D. Hongzhen, W. Qiaoyan, Z. Shanshan, and G. Mingchu, âA pairing-free certificateless signcryption scheme for vehicular ad hoc networks,â Chin. J. Electron., vol. 30, no. 5, pp. 947â955, 2021.

[34] D. J. Bernstein, N. Duif, T. Lange, P. Schwabe, and B.-Y. Yang, âHighspeed high-security signatures,â J. Cryptographic Eng., vol. 2, no. 2, pp. 77â89, 2012.

[35] F. A. Petitcolas, âKerckhoffsâ principle,â in Encyclopedia of Cryptography, Security and Privacy. Berlin, Germany: Springer, 2023, pp. 1â2.

[36] Y. Wang, Z. Su, K. Zhang, and A. Benslimane, âChallenges and solutions in autonomous driving: A blockchain approach,â IEEE Netw., vol. 34, no. 4, pp. 218â226, Jul./Aug. 2020.

[37] D. Pointcheval and J. Stern, âSecurity arguments for digital signatures and blind signatures,â J. Cryptol., vol. 13, pp. 361â396, 2000 .

[38] T. Team et al., âAvispa v1. 1 user manual,â Inf. Soc. Technol. Programme, vol. 62, p. 112, Jun. 2006. [Online] Available: http://avispa-project.org

[39] L. Xue, H. Huang, F. Xiao, and W. Wang, âA cross-domain authentication scheme based on cooperative blockchains functioning with revocation for medical consortiums,â IEEE Trans. Netw. Service Manag., vol. 19, no. 3, pp. 2409â2420, Sep. 2022.

[40] Z. Wangetal, âRevocable certificateless cross-domain authentication scheme based on primaryâsecondary blockchain,â IEEE Trans. Computat. Soc. Syst., vol. 11, no. 5, pp. 5880â5891, Oct. 2024.

[41] S. A. Chaudhry, K. Yahya, M. Karuppiah, R. Kharel, A. K. Bashir, and Y. B. Zikria, âGcacs-iod: A certificate based generic access control scheme for internet of drones,â Comput. Netw., vol. 191, 2021, Art. no. 107999.

[42] D. Kwon, S. Son, M. Kim, J. Lee, A. K. Das, and Y. Park, âA secure selfcertified broadcast authentication protocol for intelligent transportation systems in UAV-assisted mobile edge computing environments,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 11, pp. 19004â19017, Nov. 2024.

<!-- image-->  
Mingyue Xie received the MS degree from the School of Software Engineering, Chongqing University of Posts and Telecommunications, Chongqing, China. She is currently working toward the PhD degree with the School of Computer Science and Engineering, University of Electronic Science and Technology of China, Chengdu, China. Her research interests include blockchain, unmanned aerial vehicle networks, and Internet of Things.

<!-- image-->

Zheng Chang (Senior Member, IEEE) received the BEng degree from Jilin University, Changchun, China, in 2007, the MSc (Tech.) degree from the Helsinki University of Technology (Now Aalto University), Espoo, Finland, in 2009, and the PhD degree from the University of Jyvaskyla, Jyvaskyla, Finland, in 2013. In 2008, he has held various research positions with the Helsinki University of Technology, University of Jyvaskyla, and Magister Solutions Ltd., in Finland. From June to August 2013, he was a visiting researcher with Tsinghua University, China,

and with the University of Houston, Houston, TX, USA, from April to May 2015. He has been awarded by the Ulla Tuominen Foundation, Nokia Foundation, and Riitta and Jorma J. Takanen Foundation for his research excellence. He was the recipient of the 2018 IEEE Communications Society Best Young Researcher for Europe, Middle East and Africa Region and 2021 IEEE Communications Society MMTC Outstanding Young Researcher, and the Best Paper awards from IEEE ICC in 2023, IEEE TCGCC, and APCC in 2017. He is also the editor of IEEE Wireless Communications Letters, IEEE Transactions on Machine Learning in Communications and Networking, and China Communications, and guest editor of IEEE Network, IEEE Wireless Communications, IEEE Communications Magazine, IEEE Internet of Things Journal, and IEEE Transactions on Industrial Informatics. He was the best editor of IEEE Wireless Communication Letters and China Communications in 2024, exemplary reviewer of IEEE Wireless Communication Letters in 2018. He has also participated in organizing workshop and special session in Globecomâ 19, WCNCâ18-â24, SPAWCâ19 and ISWCSâ18. He is Symposium/Track co-chair of IEEE ICCâ20, Globecomâ23, VTSâ25S, and ICCâ26, publicity co-chair of IEEE Infocomâ22, Workshop co-chair of ICCCâ22 and VTSâ25F, TPC co-chair of IEEE iThingâ22, and TPC member for many IEEE major conferences, such as INFOCOM, ICC, and Globecom.

<!-- image-->

Li Wang (Senior Member, IEEE) received the PhD degree from the Beijing University of Posts and Telecommunications (BUPT), Beijing, China, in 2009. She is currently a full professor with the School of Computer Science (National Pilot Software Engineering School), BUPT. She is also an associate dean and the head with High Performance Computing and Networking Laboratory, vice dean with the Key Laboratory of Application Innovation in Emergency Command Communication Technology, Ministry of Emergency Management, and member with the Key

<!-- image-->

Laboratory of the Universal Wireless Communications, Ministry of Education, Beijing. From 2013 to 2015, she held visiting positions with the School of Electrical and Computer Engineering, Georgia Tech, Atlanta, GA, USA, and with the Department of Signals and Systems, Chalmers University of Technology, Gothenburg, Sweden, from 2015 to 2015 and from July to August 2018. Her research interests include wireless communications, distributed networking and storage, vehicular communications, social networks, and edge AI. Prof. Wang was the recipient of the 2013 Beijing Young Elite Faculty for Higher Education Award, Best Paper awards from several IEEE conferences, such as IEEE ICCC 2017, IEEE GLOBECOM 2018, and IEEE WCSP 2019, and also the Beijing Technology Rising Star Award in 2018. She is also with editorial boards of IEEE Transactions on Vehicular Technology, IEEE Transactions on Cognitive Communications and Networking, Computer Networks, and China Communications. She was an associate editor for IEEE Transactions on Green Communications and Networking, Symposium chair of IEEE ICC 2019 on Cognitive Radio and Networks Symposium, and a tutorial chair of IEEE VTC. She is also the chair of the Special Interest Group on Sensing, Communications, Caching, and Computing in Cognitive Networks for IEEE Technical Committee on Cognitive Networks. From 2020 to 2021, she was the vice chair of the Meetings and Conference Committee for IEEE Communication Society AsiaâPacific Board. She was with TPC of multiple IEEE conferences, including IEEE Infocom, Globecom, International Conference on Communications, IEEE Wireless Communications and Networking Conference, and IEEE Vehicular Technology Conference in recent years.

Geyong Min (Senior Member, IEEE) received the BSc degree in computer science from the Huazhong University of Science and Technology, China, in 1995, and the PhD degree in computing science from the University of Glasgow, U.K., in 2003. He is currently a professor of high-performance computing and networking with the Department of Computer Science, University of Exeter, U.K. His research interests include computer networks, wireless communications, parallel and distributed computing, ubiquitous computing, and multimedia systems.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_5_img_1.jpeg|page_5_img_1]]
3. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_11_img_1.png|page_11_img_1]]
4. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_12_img_1.png|page_12_img_1]]
5. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_13_img_1.png|page_13_img_1]]
6. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_14_img_1.jpeg|page_14_img_1]]
7. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_15_img_1.jpeg|page_15_img_1]]
8. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_16_img_1.jpeg|page_16_img_1]]
9. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_16_img_2.jpeg|page_16_img_2]]
10. [[../extracted_images/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks/page_16_img_3.jpeg|page_16_img_3]]

---

