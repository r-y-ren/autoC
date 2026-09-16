# LSPSS: Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing

Haoyang Wang , Kai Fan , Member, IEEE, Chong Yu , Graduate Student Member, IEEE, Kuan Zhang , Member, IEEE, Fenghua Li, Member, IEEE, Hui Li , Member, IEEE, Yintang Yang , Senior Member, IEEE, and Haojin Zhu , Fellow, IEEE

AbstractâAerial computing is gradually playing an essential role in edge and fog computing paradigms by virtue of mobility, availability, scalability, flexibility, and simultaneity, where the Low-altitude Computing (LAC) platform, as the end close to the data sources, is mainly responsible for data collection and storage. However, because of the long physical distance of data transmission and the vulnerability of the transmission link to various attacks, how to efficiently share the stored data while ensuring data privacy is a critical issue for LAC at present. In this article, we propose a lightweight and secure private data storage and sharing scheme to support range queries over encrypted multi-dimensional data. Specifically, we first propose two data conversion methods for transforming location features and collected log files with multidimensional attributes in Unmanned Aerial Vehicles (UAVs). Based

Index TermsâAerial computing, unmanned aerial vehicle (UAV), multi-dimensional data, privacy-preserving.

on the ideas of asymmetric scalar-product-preserving encryption (ASPE) and inner product comparison (IPC), we design a privacypreserving storage and sharing technique for the converted data. In addition, to achieve secure and efficient data querying and result verification, we design a secure data index and build a data authentication structure (DAS) with G-tree. Finally, we rigorously analyze the security of our proposed scheme and conduct extensive experiments on a real-world database to prove that our proposed scheme is secure and easy to use in practical application scenarios.

## I. INTRODUCTION

A S RESEARCHERS defined the road-maps for sixth-generation (6G) networks, various Internet of Things (IoT) applications have more data to be collected and transmitted in 6G. To overcome the limitations of IoT devices in energy supply, transmission power and processing capability, and to facilitate data storage and sharing among devices in diverse regions, Aerial Access Networks (AANs) has been proposed to provide favorable channels and improved coverage. In addition, to be more applicable to computation-intensive applications such as autonomous vehicles, virtual reality (VR), and holographic communications, the edge computing has also been introduced for data collection and management in IoT devices. As a combination of AANs and edge computing, the emerging aerial computing is expected to improve the quality of services such as communication, computing, storage, sensing, navigation, and control on a global scale.

The typical aerial computing framework under the 6G architecture is shown in Fig. 1, where the aerial components are deployed in the aerial domain with vertical layering, i.e., (i) IoT; (ii) Terrestrial Computing; (iii) Low-altitude Computing (LAC) Platform; (iv) High-altitude Computing (HAC) Platform; and (v) Satellite Computing Platform. The IoT layer consists of any data-generating IoT devices, such as computation-intensive applications that require participation by aerial computing. The Terrestrial Computing layer contains traditional computing models such as fog computing, multi-access edge computing (MEC), and Cloudlet. The LAC, HAC, and satellite computing platforms provide storage and computing services at different

Digital Object Identifier 10.1109/TSC.2023.3333347 altitudes for UAVs, manned vehicles, and LEO satellites, respectively. With the above framework, aerial computing not only retains the characteristics of edge computing such as on-premises, proximity, low latency, location awareness, and network contextual information, but also offers mobility, availability, scalability, flexibility, and simultaneity. These characteristics enable aerial computing to perform essential roles in smart cities, smart transportation, smart factories, and smart grids.

<!-- image-->  
Fig. 1. Aerial computing framework under the 6G architecture.

Although aerial computing brings many benefits, it still suffers from several security threats below. (i) The risk of privacy exposure during communication increases due to the long physical distance among components in the aerial domain. (ii) UAVs in the LAC platform often require centralized data collection to facilitate subsequent training, but sharing sensitive data in the aerial domain may leak private information. (iii) The each-kind component in the framework has different storage space and computation power, how to allocate these resources to support sensitive data storage and sharing is also an urgent issue to be solved.

In aerial computing, there exists some literature to preserve data privacy during data interactions with blockchain [1], [2], [3], cryptography [4], [5], and differential privacy [6]. However, for the blockchain-based scheme, (i) block-chain construction requires huge storage space and computation capacity; (ii) the data ledger only can store a few sensitive information; (iii) the operation of on-chain smart contracts brings extra overhead. For the cryptography-based scheme, the cryptographic primitives such as online/offline signatures and FHE cause huge computational and storage overhead, and cannot be applied to resource-limited wireless-aware devices. As for the differential privacy-based scheme, although this technique is less overhead (i.e., privacy enhancement is achieved by introducing artificial noise), it is likely to generate unusable results due to noise accumulation in complex computational tasks.

In summary, the existing privacy-preserving schemes have the following problems. (i) The security cannot meet the requirements of practical scenarios; (ii) The consumption of system construction is too large to be arranged on resource-constrained devices; (iii) The storage and sharing mode is single and cannot fulfill the user demands.

To address the limitations of these schemes, we design a lightweight and secure private data storage and sharing scheme called LSPSS in aerial computing, which aims to achieve the following objectives.

1) Stronger Privacy Preservation: The primary objective of storing and sharing private data in aerial computing is privacy preservation. Thus LSPSS requires achieving stronger privacy preservation compared to existing schemes. Specifically, it should enable semantic security under the Known Background Model, as well as the achievement of single-dimensional and query unlinkability.

2) Multi-dimensional Data: UAVs in aerial computing collect and process private data consisting of multidimensional attributes. Thus LSPSS needs to focus on the storage and sharing of multi-dimensional data.

3) Lightweight Overhead: Most existing schemes result in huge space and computation overhead for privacy preservation, thus reducing the required overhead while preserving data privacy is also a key objective that needs to be achieved in LSPSS.

Our Contribution: To achieve these objectives, we address three challenges. The first one is to convert the original multidimensional data into an easily stored and shared form. Inspired by the concept of IPC [7], we convert the multi-dimensional data into vectors that can be computed with IPC. Then, we implement privacy-preserving storage and sharing of the vectors based on the ASPE algorithm and cryptographic functions. Moreover, we design a verification mechanism for completeness based on the Merkle tree to enhance the reliability of query results. Our contributions are summarized as follows.

- Aiming at two types of multi-dimensional data (i.e., location and log files) of UAVs, we propose two conversion methods to convert multi-dimensional data into vectors. These approaches not only facilitate the storage, but also enables the sharing of multi-dimensional data.

- To achieve lightweight multi-dimensional data storage and sharing with privacy preservation, we first design two secure data indexes for multi-dimensional location and log files, respectively. Then we propose two permutation and perturbation-based matrix encryption methods to encrypt private data.

- In addition, we propose a verification mechanism for the completeness of query results by combining the data index and Merkle tree (e.g., it can require 400 milliseconds to complete the result verification over 25000 files).

To validate the efficiency of LSPSS, we not only rigorously analyze its security but also conduct extensive experiments on real-world datasets (e.g., it can require 2.5 seconds to perform a query over 25000 files).

We organize the remainder of this paper as follows. In Section II, we introduce the related work. Then we depict some preliminaries about LSPSS in Section III. In Section IV, we present the system model, the security and algorithm definition of LSPSS. In Section V, we describe our LSPSS construction in detail, followed by security analysis and performance evaluation in Sections VI and VII, respectively. Finally, we draw conclusions in Section VIII.

## II. RELATED WORK

As our proposed LSPSS focuses on the secure storage and sharing of multi-dimensional data, we introduce several typical schemes aimed at this issue as well.

To reserve of plaintext order in the ciphertexts, orderpreservation encryption (OPE) is applied in most of the early range query schemes [8], [9]. However, due to the leakage of the plaintext order [10], OPE-based range query schemes cannot guarantee security under the ordered chosen plaintext attack.

After that, some literature [11], [12], [13], [14] proposed range query schemes with buckets. These works spilt the plaintext space into buckets, so the order information in the same bucket can be preserved. Though, the split of data space with buckets causes false positive in query results, so users need extra consumption to filter the returned results in most bucket-based range query schemes.

Compared with the above range query schemes, public keybased range query schemes [15], [16], [17] are introduced to enhance security. The work [15] divided one multi-dimensional range query (MRQ) into several single-dimensional range queries, thus the single-dimensional privacy1 is disclosed to servers. Moreover, public key cryptography such as hidden vector encryption (HVE) employed in these works [16], [17] brings huge computation consumption, thus not applicable in practical scenarios.

Considering the balance between security and efficiency, the currently mainstream privacy-preserving MRQ schemes utilized tree structures to design data indexes for secure and efficient retrieval, where the works are based on KD-tree [18], [19], [20], [21], [22] and the works are based on R-tree [23], [24], [25], [26], [27], [28], [29], while the works and employed B+-tree [7], [30], AVL-tree [31] and Internal tree [32], [33], respectively. However, all the above are three-party system models, which are not applicable to the architecture of aerial computing, so as we set in our design objectives, LSPSS should provide the solution to the issue of secure and efficient storage and sharing of multi-dimensional data in aerial computing.

## III. PRELIMINARIES

In this section, we introduce some preliminaries used in LSPSS, including APSE, the cryptographic hash function (SHA-256), and the permutation function. For simplicity, the details of the G-tree [34] and Merkle tree [35] adopted in LSPSS are not introduced here.

## A. Asymmetric Scalar-Product-Preserving Encryption

The literature [36] introduced asymmetric scalar-productpreserving encryption (ASPE) to enable the scalar product computation of two encrypted vectors. For privacy preservation, the ASPE encrypts data vectors and query vectors in different ways. The specific construction is illustrated below.

- ASPE.Setup(d) â SK: Given the security parameter Î», generate the secret key SK, consisting of two invertible matrices $M _ { 1 } , M _ { 2 } \in \mathbb { R } ^ { \lambda \times \lambda }$ and one bit string $S \in \{ 0 , 1 \} ^ { \lambda }$ as split vector.

- ASPE.Data_Enc $( S K , P ) \to { \hat { P } } \mathrm { . }$ Given the secret key SK and a data vector $P \in \mathbb { R } ^ { \lambda }$ , split $P$ into two vectors $\{ P _ { 1 } , P _ { 2 } \}$ with split vector S as:

$$
\left\{ \begin{array} { l l } { P _ { 1 } [ i ] + P _ { 2 } [ i ] = P [ i ] ( S [ i ] = 1 , i \in [ 1 , \lambda ] ) } \\ { P _ { 1 } [ i ] = P _ { 2 } [ i ] = P [ i ] ( S [ i ] = 0 , i \in [ 1 , \lambda ] ) } \end{array} \right.\tag{1}
$$

Generate the encrypted data vector $\hat { P } = \{ \hat { P } _ { 1 } = M _ { 1 } ^ { T } P _ { 1 }$ $\hat { P } _ { 2 } = M _ { 2 } ^ { T } P _ { 2 } \}$

- ASPE.Query_ $\mathbf { E n c } ( S K , Q )  { \hat { Q } }$ : Given the secret key SK and a query vector $Q \in \mathbb { R } ^ { \lambda }$ , split Q into two vectors $\{ Q _ { 1 } , Q _ { 2 } \}$ with split vector S as:

$$
\left\{ \begin{array} { l } { Q _ { 1 } [ i ] + Q _ { 2 } [ i ] = Q [ i ] ( S [ i ] = 0 , i \in [ 1 , \lambda ] ) } \\ { Q _ { 1 } [ i ] = Q _ { 2 } [ i ] = Q [ i ] ( S [ i ] = 1 , i \in [ 1 , \lambda ] ) } \end{array} \right.\tag{2}
$$

Generate the encrypted query vector $\hat { Q } = \{ \hat { Q } _ { 1 } =$ $M _ { 1 } ^ { - 1 } Q _ { 1 } , \hat { Q } _ { 2 } = M _ { 2 } ^ { - 1 } \bar { Q } _ { 2 } \}$

- ASPE.Match $( \hat { P } , \hat { Q } )  S c o r e \colon$ The scalar product of plaintexts $P$ and $Q$ can be calculated by encrypted data vector $\hat { P }$ and query vector $\hat { Q }$ as:

$$
\begin{array} { r l } & { \hat { P } \cdot \hat { Q } = \hat { P _ { 1 } } \cdot \hat { Q } _ { 1 } + \hat { P _ { 2 } } \cdot \hat { Q } _ { 2 } } \\ & { \quad \quad = M _ { 1 } ^ { T } P _ { 1 } \cdot M _ { 1 } ^ { - 1 } Q _ { 1 } + M _ { 2 } ^ { T } P _ { 2 } \cdot M _ { 2 } ^ { - 1 } Q _ { 2 } } \\ & { \quad \quad = P \cdot Q } \end{array}\tag{3}
$$

## B. Cryptographic Functions

1) Hash Function: To facilitate the Merkle tree to achieve the verification of query results, we employ the cryptographic hash function SHA-256 $H ( \cdot )$ and the secret key $K _ { H }$ to calculate the hash value of each data record:

$$
H a s h _ { D } = H ( D , K _ { H } )\tag{4}
$$

The function possesses two features such as (i) collisionresistance: for two different data records $D _ { 1 } , D _ { 2 }$ , it generates different hash values; (ii) one-way: it is impossible to recover the data record D from $H ( D , K _ { H } )$ . To simplify the expression, we use $H ( \cdot )$ to denote $H ( \cdot , K _ { H } )$

2) Permutation Function: To construct the matrix encryption methods to encrypt vectors, we employ the cryptographic permutation function $\Omega ( \cdot )$ and the secret key $K _ { \Omega }$ to obtain new arrangements:

$$
\Omega _ { X } = \Omega ( X , K _ { \Omega } )\tag{5}
$$

The function also possesses two features such as (i) rearrangement: for one set $X ,$ , it generates a rearrangement $\Omega _ { X }$ of $X ,$ , not an arrangement itself; (ii) one-way: it is impossible to recover the set $X$ from $\Omega ( X , K _ { \Omega } )$ without $K _ { \Omega }$ . Simply, we use $\Omega ( \cdot )$ to denote $\Omega ( X , K _ { \Omega } )$ .

## IV. PROBLEM FORMULATION

In this section, we briefly explain our proposed approach. Then, we present the formal definition of the LSPSS. Finally,

<!-- image-->  
Fig. 2. System model of LSPSS.

we describe the leakage and give the security definition of our system.

## A. System Model

The system model of LSPSS is shown as Fig. 2, which consists of six entities: (i) UAVs. UAVs have lower computation capacity and smaller storage space. UAV is responsible for collecting data and uploading them to zone servers and LAC platform after processing. (ii) Zone servers (ZS). Each aerial zone possesses one ZS, which has certain computation power and storage space. The ZS primarily stores the location information of all UAVs in the zone, and responds to user queries for UAV locations. (iii) Zone Administrators (ZA). Each aerial zone owns a unique administrator as a fully trusted entity, who builds the secure index and the DAS from the plaintext data (except location information), and later transfers the GeoHash code, index and DAS of the zone to the LAC platform together. (iv) Key Generation Authority (KGA). The KGA acts as a fully trusted entity and generates keys and security parameters for the remaining entities in the system. (v) Users. Users can initiate queries with requirements, and decrypt the obtained query results after the completeness verification. (vi) LAC platform server. These servers have powerful computation capacity and storage space. They mainly store the log indexes and encrypted logs included in each zone, and respond to user queries.

## B. Definition of LSPSS

Definition 1. (LSPSS): The LSPSS is a tuple Î  that consists of five polynomial-time algorithms such as:

. $\{ H ( \cdot ) , \Omega ( \cdot ) , S K \}  G e n K e y ( 1 ^ { \lambda } )$ : It takes a security parameter Î» as input, and outputs a secret key set $S K$ , a permutation function $\Omega ( \cdot )$ with its key $K _ { \Omega }$ , a hash function $H ( \cdot )$ with its key $K _ { H }$

$\{ I _ { L } , I _ { D } , E ( l o g ) \}  G e n I n d e x ( D , L , S K ) .$ : It takes a secret key set $S K$ , a multi-dimensional dataset D, a location dataset L as input, and outputs a secure data index $I _ { D }$ , a secure location index $I _ { L } ,$ encrypted logs $E ( l o g )$

- $\{ T K _ { L } , T K _ { D } \}  G e n T o k e n ( Q _ { D } , Q _ { L } , S K )$ : It takes a data MRQ $Q _ { D }$ , a location MRQ $Q _ { L } ,$ , a secret key set SK as input, and outputs a location token $T K _ { L } ,$ , a data token $T K _ { D }$

- $\{ D _ { R } , A V I \}  S e a r c h ( T K _ { L } , T K _ { D } , I _ { L } , I _ { D } ) .$ It takes two secure indexes $I _ { L }$ and $I _ { D }$ , two encrypted tokens $T K _ { L }$ and $T K _ { D }$ as input, and outputs query results $D _ { R } .$ , auxiliary verification information AV I.

- $\{ b \in \{ 0 , 1 \} , P _ { R } \}  V e r i f y ( D _ { R } , A V I , S K ) .$ : It takes query results $D _ { R } .$ , auxiliary verification information AV I as input, then outputs a bit $b \in \{ 0 , 1 \}$ and the plaintext $P _ { R }$ of query results $D _ { R }$

## C. Security Definition

As we discussed before, the LSPSS in this paper needs to achieve security under the known background model for semi-trusted adversaries. An adversary A can access three-type information, i.e., History, View, and Trace.

- History: An interaction among users and the server, consists of a dataset D, a secure data index I, and a query set $\mathcal { Q } = ( q _ { 1 } , \ldots , q _ { \tau } )$ , uploaded by users, represented as the information $H = ( \mathcal { D } , \mathcal { T } , \mathcal { Q } )$

- View: The server only can touch the encrypted form of H $( \mathrm { i . e . } ,$ , the views) with the secret key $S K$ , represented as $V ( H )$ . The views contains the encrypted dataset $\mathcal { D } ^ { * }$ , the secure data index $\mathcal { T } ^ { * }$ and the query tokens $T K ( \mathfrak { Q } )$

- Trace: The trace $T r ( H )$ represents the information that the server can learn from a given history H. It consists of the access pattern $\alpha ( H )$ , search pattern $\sigma ( H )$ and the returned identifiers $I D ( { \mathcal { Q } } )$ . Let $I D ( \amalg )$ represent the set of identifiers of the qualified data records, i.e., $\alpha ( H ) =$ $\{ I D ( \mathrm { I I _ { 1 } } ) , \ldots , I D ( \mathrm { I I _ { \tau } } ) \}$ . The search pattern $\sigma ( H )$ is described by $\mathrm { ~ \ i ~ } n \times \tau$ binary matrix, where $\sigma ( H ) _ { i , j }$ is $\mathrm { i } \mathrm { i } \mathrm { f } \mathscr { T } _ { i }$ is matched to a query $q _ { j }$ , and 0 otherwise. Thus the views are donated as $T r ( H ) \stackrel { \cdot } { = } \{ I D ( \mathcal { Q } ) , \alpha ( H ) , \sigma ( H ) \}$ .

Suppose that the server acquires the $T r ( H )$ , several queries and their probability pairs $( q _ { i } , p _ { i } )$ under the known background model. Under this attack model, we need to guarantee semantic security, which is defined as follows.

1) Semantic Security: The semantic security of the given encryption is modeled by a game played by a challenger C and an adversary A. The challenger generates an encryption scheme, while the adversary tries to break the scheme. the formal security model can be depicted as follows.

- Setup: Let $S P$ be the system parameters. The C performs the key generation algorithm to generate a keypair $( k _ { 1 } , k _ { 2 } )$ and sends to $k _ { 2 }$ to the A. The C keeps $k _ { 1 }$ to respond to decryption queries from the A.

Phase 1: The A makes decryption queries on ciphertext that are adaptively chosen by the A itself. For a decryption query on the ciphertext $C T _ { i } ,$ , the C performs the decryption algorithm and then sends the plaintext to the A.

Challenge: The A outputs two distinct messages $m _ { 0 } , m _ { 1 }$ from the same message space, which are adaptively chosen by the A itself. The C randomly choose $c \in \{ 0 , 1 \}$ and then computes a challenge ciphertext $C T ^ { * } = \bar { E } [ S \bar { P } , k _ { 2 } , m _ { c } ]$ ï¼ which is given to the A.

- Phase 2: The C responds to decryption queries in the same way as in Phase 1 with the restriction that no decryption query is allowed on $C T ^ { * }$

- Guess: The A outputs a guess $c ^ { \prime }$ of c and wins the game if $c ^ { \prime } = c .$ . The advantage Îµ of the A in winning this game is defined as

$$
\varepsilon = 2 \left( P r [ c ^ { \prime } = c ] - { \frac { 1 } { 2 } } \right) .
$$

Definition 2. (Semantic Security): An encryption scheme is (t, Îµ)-secure in the security model of indistinguishability against chosen-plaintext attacks (IND-CPA) if there exists no adversary who can win the above game in time t with advantage Îµ, where the adversary is not allowed to make any decryption query.

Furthermore, single-dimensional privacy preservation and query unlinkability are also crucial security requirements during data sharing. We define both of them as follows.

2) Single-Dimensional Privacy: In the design objectives of LSPSS, privacy-preserving storage and sharing is oriented to multi-dimensional data, while single-dimensional privacy, as an essential security property in multi-dimensional data query, also belongs to the privacy-preserving requirements of LSPSS. The details of single-dimensional privacy have been provided by the literature [28], thus we introduce its formal definition directly.

Definition 3. (Single-Dimensional Privacy): Given a wdimensional dataset $\mathcal { D } = \{ I D _ { 1 } , \ldots , I D _ { n } \}$ and a query $\mathcal { Q } ,$ the single-dimensional privacy of D refers to the information on which records satisfy each single dimension of the query, i.e., w record sets $Q _ { i } = \{ I D _ { x } , I D _ { y } , I D _ { z } \} ( i \in [ 1 , w ] )$ .

3) Query Unlinkability: The query unlinkability is an indispensable privacy-preserving requirement of the query over encrypted data. Briefly, if query tokens generated by the identical query are also the same, the servers can count the frequency of initiating diverse queries, and then infer part of query content with background knowledge. Thus, LSPSS also requires achieving query unlinkability. Its formal definition is given below.

Definition 4. (Query Unlinkability): Given a query Q, and generate Î· query tokens $\{ T K _ { 1 } ( Q ) , \dots , T K _ { \eta } ( Q ) \}$ for Q, the query unlinkability can be achieved if all the m tokens are not the same.

4) Completeness: To improve the availability of query results, the users are required to perform completeness verification before decrypting the query results, to ensure that all records (logs) satisfying the query requirements are returned. Therefore, we present a formal definition of completeness as follows.

Definition 5. (Completeness): Given a query Q, the server returns the result set ${ { D } _ { R } } = \left\{ { { d } _ { 1 } } , { { d } _ { 2 } } , \ldots , { { d } _ { r } } \right\}$ . If each record $f _ { i } \in$ $F$ such that $f _ { i }$ is in Q, the encrypted data $d _ { i }$ must in $D _ { R }$ , then $D _ { R }$ is complete.

<!-- image-->  
Fig. 3. Two cases for location.

## V. TWO DATA CONVERSION METHODS FOR MULTI-DIMENSIONAL FEATURES

Generally speaking, the monitoring log files of UAVs are labeled by several feature attributes such as temperature, humidity, concentration and so on, and the location of UAVs are labeled by three attributes such as (longitude, latitude, altitude). In this section, aiming at facilitating the storage and sharing of multi-dimensional features, we introduce two data conversion methods, i.e., the conversion method for location data called CMLD and the conversion method for log files called CMLF below.

## A. Conversion Method for Location Data

As Fig. 3 shows, given two points $A ( a _ { x } , a _ { y } , a _ { z } ) , B ( b _ { x } , b _ { y } , b _ { z } )$ in the zone, the sphere constructed with the line between A and B as the diameter is the query range S for the location of UAVs. Suppose that location of one UAV in the zone is $L ( l _ { x } , l _ { y } , l _ { z } )$ ï¼ there exists the following conclusion (we consider that points on the boundary of the sphere are also located in the sphere). (i) ${ \overrightarrow { L A } } \cdot { \overrightarrow { L B } } \leq 0$ , then the UAV inside the S; (ii) $\overrightarrow { L A } \cdot \overrightarrow { L B } > 0$ then the UAV outside the $\underline { { S } } _ { \bullet }$

Note that both vectors $\overrightarrow { L A }$ and $\overrightarrow { L B }$ include data information. To facilitate the storage and sharing of data, the location L and the query range S need to be divided into two independent vectors, thus we propose the following conversions of $\overrightarrow { L A } \cdot \overrightarrow { L B }$ based on the concept of IPC. In detail, $\overrightarrow { L A }$ and $\overrightarrow { L B }$ are defined as:

$$
\left\{ \begin{array} { l l } { \overrightarrow { L A } = ( a _ { x } - l _ { x } , a _ { y } - l _ { y } , a _ { z } - l _ { z } ) } \\ { \overrightarrow { L B } = ( b _ { x } - l _ { x } , b _ { y } - l _ { y } , b _ { z } - l _ { z } ) } \end{array} \right.\tag{6}
$$

Later, $\overrightarrow { L A } \cdot \overrightarrow { L B }$ can be divided into an expression of two independent vectors:

$$
\begin{array} { r l } & { \overrightarrow { L } \overrightarrow { A } \cdot \overrightarrow { L } \overrightarrow { B } } \\ & { = ( a _ { x } - l _ { x } ) ( b _ { x } - l _ { x } ) + ( a _ { y } - l _ { y } ) ( b _ { y } - l _ { y } ) + ( a _ { z } - l _ { z } ) ( b _ { z } - l _ { z } ) } \\ & { = ( a _ { x } b _ { x } - a _ { z } l _ { x } - b _ { x } l _ { x } + l _ { x } ^ { 2 } ) + ( a _ { y } b _ { y } - a _ { y } l _ { y } - b _ { y } l _ { y } + l _ { y } ^ { 2 } ) } \\ & { \quad + ( a _ { z } b _ { z } - a _ { z } l _ { z } - b _ { z } l _ { z } + l _ { z } ^ { 2 } ) } \\ & { = [ 1 \cdot ( a _ { x } b _ { x } ) + l _ { x } \cdot ( - a _ { x } ) + l _ { x } \cdot ( - b _ { z } ) + 1 \cdot \ell _ { x } ^ { 2 } ] + [ 1 \cdot ( a _ { y } b _ { y } ) } \\ & { + l _ { y } \cdot ( - a _ { y } ) + l _ { y } \cdot ( - b _ { y } ) + 1 \cdot l _ { y } ^ { 2 } ] + [ 1 \cdot ( a _ { z } b _ { z } ) + l _ { z } \cdot ( - a _ { z } ) } \\ & { + l _ { z } \cdot ( - b _ { z } ) + 1 \cdot l _ { z } ^ { 2 } ] } \\ & { = ( 1 , l _ { x } , l _ { x } ^ { 2 } , l _ { x } ^ { 2 } , l _ { y } ^ { 2 } , l _ { y } ^ { 2 } , l _ { z } ^ { 2 } , l _ { z } ^ { 2 } ) } \end{array}
$$

<!-- image-->  
Fig. 4. Instance of G-tree and MRQ.

$$
\begin{array} { l } { { \circ ( a _ { x } b _ { x } , - a _ { x } , - b _ { x } , 1 , a _ { y } b _ { y } , - a _ { y } , - b _ { y } , 1 , a _ { z } b _ { z } , - a _ { z } , - b _ { z } , 1 ) \circ } } \\ { { \qquad \mathrm { ( } a _ { x } b _ { x } , - a _ { x } , - b _ { x } , 1 , a _ { y } b _ { y } , - a _ { z } , - b _ { y } , 1 , a _ { z } b _ { z } , - a _ { z } , - b _ { z } , 1 ) \circ } } \\ { { \qquad \mathrm { ( } a _ { x } \qquad \mathrm { ( } a _ { x } \qquad \mathrm { ~ } } } \end{array}\tag{7}
$$

The correlation between $\overrightarrow { L A } \cdot \overrightarrow { L B }$ and $\textstyle \sum _ { i = 1 } ^ { 1 2 } u _ { i } \cdot v _ { i }$ can be formulated as:

$$
\left\{ \begin{array} { l l } { \overrightarrow { L A } \cdot \overrightarrow { L B } \leq 0 \Leftrightarrow \sum _ { i = 1 } ^ { 1 2 } u _ { i } \cdot v _ { i } \leq 0 } \\ { \overrightarrow { L A } \cdot \overrightarrow { L B } > 0 \Leftrightarrow \sum _ { i = 1 } ^ { 1 2 } u _ { i } \cdot v _ { i } > 0 } \end{array} \right.\tag{8}
$$

## B. Conversion Method for Log Files

Similarly, the w-d attribute values of log files and the MRQ need to be divided into two-kind independent vectors. Also, to improve query efficiency and accuracy, we design the data index of log files based on the G-tree, where the non-leaf and leaf nodes correspond to w-d attribute ranges and values, respectively. As Fig. 4 describes, each non-leaf node represents one minimum bounding rectangle (MBR) and each leaf node represents one point, as well as the MRQ represents one hyper-rectangle. Thus, queries of log files can be converted into intersection tests between MRQ and nodes, as well as inclusion tests between MRQ and leaf nodes.

1) Range Intersection: Given a w-d data range MBR = $( R _ { 1 } , \ldots , R _ { w } )$ , a query $M R Q = ( Q _ { 1 } , \dots , Q _ { w } )$ , if the k-d attribute of $M B R \left( R _ { k } = \left[ l _ { k } , h _ { k } \right] \right)$ and that of M RQ $( Q _ { k } = [ x _ { k } ^ { l } , x _ { k } ^ { r } ] )$ intersect, there exists a true proposition in (9) based on IPC. Furthermore, we add a perturbation Î´ (a random positive number) to this comparison predicate to acquire $\hat { p } = ( l _ { k } - x _ { k } ^ { l } ) ( h _ { k } - x _ { k } ^ { r } ) ( h _ { k } + \delta )$ . Then, we express pË as two independent vectors (i.e., query vector and range vector) in (10).

$$
R _ { k } \cap Q _ { k } \neq \emptyset \Leftrightarrow p = \left( l _ { k } - x _ { k } ^ { l } \right) ( h _ { k } - x _ { k } ^ { r } ) \leq 0\tag{9}
$$

$$
\begin{array} { r } { \overrightarrow { \mathbf { q } } = \left( \begin{array} { c } { x _ { k } ^ { r } + \delta } \\ { - ( x _ { k } ^ { r } ) ^ { 2 } - x _ { k } ^ { r } \delta } \\ { - x _ { k } ^ { l } x _ { k } ^ { r } - x _ { k } ^ { l } \delta } \\ { x _ { k } ^ { l } x _ { k } ^ { r } ( x _ { k } ^ { r } + \delta ) } \end{array} \right) \overrightarrow { \mathbf { \Psi } } = \left( \begin{array} { c } { l _ { k } h _ { k } } \\ { h _ { k } } \\ { l _ { k } } \\ { 1 } \end{array} \right) } \end{array}\tag{10}
$$

Obviously, whether the two ranges intersect or not is related to ${ \vec { q } } \cdot { \vec { v } }$ as described in:

$$
\left\{ \begin{array} { l l } { \vec { q } \cdot \vec { v } \leq 0 \Leftrightarrow R _ { k } \cap Q _ { k } \neq \emptyset } \\ { \vec { q } \cdot \vec { v } > 0 \Leftrightarrow R _ { k } \cap Q _ { k } = \emptyset } \end{array} \right.\tag{11}
$$

<!-- image-->  
Fig. 5. System process of the LSPSS.

2) Point Inclusion: Given a w-d data point (i.e., data record) $\boldsymbol { D } = ( d _ { 1 } , \ldots , d _ { w } )$ , a query $M R Q = ( Q _ { 1 } , \dots , Q _ { w } )$ , if the k-th dimensional attribute value of D falls within the corresponding attribute range of M RQ, there exists a true proposition in (12) based on IPC. Also, we add a perturbation Î´ to this comparison predicate to acquire $\tilde { p } ( d _ { k } ) = ( d _ { k } - x _ { k } ^ { l } ) ( d _ { k } - x _ { k } ^ { r } ) ( d _ { k } + \delta )$ . Likewise, $\tilde { p } ( d _ { k } )$ is divided into one query vector and one value vector in (13).

$$
x _ { k } ^ { l } \leq d _ { k } \leq x _ { k } ^ { r } \Leftrightarrow p ( d ) = ( d _ { k } - x _ { k } ^ { l } ) ( d _ { k } - x _ { k } ^ { r } ) \leq 0\tag{12}
$$

$$
\begin{array} { r } { \overrightarrow { q } = \left( \begin{array} { c } { 1 } \\ { - x _ { k } ^ { l } - x _ { k } ^ { r } + \delta } \\ { x _ { k } ^ { l } x _ { k } ^ { r } - x _ { k } ^ { l } \delta - x _ { k } ^ { r } \delta } \\ { x _ { k } ^ { l } x _ { k } ^ { r } \delta } \end{array} \right) \overrightarrow { \boldsymbol { \vartheta } } = \left( \begin{array} { c } { d _ { k } ^ { 3 } } \\ { d _ { k } ^ { 2 } } \\ { d _ { k } } \\ { 1 } \end{array} \right) } \end{array}\tag{13}
$$

As shown in (14), whether the k-th attribute value of D falls within the corresponding attribute range of M RQ or not is related to ${ \vec { q } } \cdot { \vec { v } }$

$$
\left\{ \begin{array} { l l } { \vec { q } \cdot \vec { v } \leq 0 \Leftrightarrow d _ { k } \in \left[ x _ { k } ^ { l } , x _ { k } ^ { r } \right] } \\ { \vec { q } \cdot \vec { v } > 0 \Leftrightarrow d _ { k } \notin \left[ x _ { k } ^ { l } , x _ { k } ^ { r } \right] } \end{array} \right.\tag{14}
$$

Note that a D falls within the M RQ iff the value of each dimensional attribute of D falls within the corresponding attribute range of the M RQ. Similarly, a M BR intersects with the M RQ iff the range of each dimensional attribute of M BR intersects with the corresponding attribute range of the MRQ.

## VI. LSPSS CONCRETE CONSTRUCTION

In the previous section, we elaborate on our LSPSS based on two methods CMLD and CMLF. First, we give the correlation among the corresponding algorithms of each entity in Fig. 5.

## A. GenKey

The KGA performs this algorithm for generating keys and functions for other system entities. First, KGA generates two $( 1 2 + N ) \times ( 1 2 + N ) { \cdot } \mathrm { d }$ invertible matrices $M _ { 1 } , ~ M _ { 2 } , \mathrm { ~ a ~ } ( 4 +$ $M ) \times ( 4 + M ) \ â \mathrm { d }$ invertible matrix $M _ { 3 }$ and a $( 1 2 + N ) { \mathrm { - d } }$ spilt vector S using the security parameter Î», and computes $\tilde { M } _ { 1 } =$ $\vert \operatorname * { d e t } ( M _ { 1 } ) \vert { \tilde { M _ { 1 } ^ { - 1 } } } , { \tilde { M } } _ { 2 } = \vert \operatorname * { d e t } ( M _ { 2 } ) \vert M _ { 2 } ^ { - 1 } , { \tilde { M } } _ { 3 } = \vert \operatorname * { d e t } ( M _ { 3 } ) \vert M _ { 3 } ^ { - 1 }$ ï¼ where $\vert \operatorname * { d e t } ( M _ { 1 } ) \vert , \ \vert \operatorname * { d e t } ( M _ { 2 } ) \vert$ and $\lvert \operatorname* { d e t } ( M _ { 3 } ) \rvert$ are the absolute values of the determinant of $M _ { 1 } , M _ { 2 }$ and $M _ { 3 }$

KGA also gives a permutation function $\Omega ( \cdot )$ , a cryptographic hash function $H ( \cdot )$ with their keys $K _ { \Omega } , K _ { H }$ . Then, KGA generates the symmetric key k of the AES algorithm and the keypair $( p k , s k )$ of the RSA algorithm. The KGA distributes the keys and the functions to the respective entities.

## B. GenIndex

We store the location data and the log files on the ZSs and LAC platform, respectively. Since the two kinds of data correspond to diverse vectors after feature conversion, we build diverse data indexes.

## - Stage 1: Location Index Generation

As designed in CMLD, the UAV first generates the plaintext of the location vector L based on the location data $( l _ { x } , l _ { y } , l _ { z } )$ and adds N 1 s to L to obtain L , as shown in (15). Then UAV obfuscates vector $L ^ { \prime }$ as $L ^ { \prime \prime }$ with permutation function Î©(Â·) and key $K _ { \Omega }$ . Then, the UAV splits $L ^ { \prime \prime }$ to obtain two $( 1 2 + N ) \mathrm { - d }$ vectors with the split vector $S ,$ as shown in (16).

$$
\begin{array} { r l } & { L = ( 1 , l _ { x } , l _ { x } , l _ { x } ^ { 2 } , 1 , l _ { y } , l _ { y } , l _ { y } ^ { 2 } , 1 , l _ { z } , l _ { z } , l _ { z } ^ { 2 } ) } \\ & { \Downarrow } \\ & { L ^ { \prime } = ( 1 , l _ { x } , l _ { x } , l _ { x } ^ { 2 } , 1 , l _ { y } , l _ { y } , l _ { y } ^ { 2 } , 1 , l _ { z } , l _ { z } , l _ { z } ^ { 2 } , \underbrace { 1 , \dots , 1 } _ { N } ) } \\ & { } \\ & { \Downarrow } \\ & { L ^ { \prime \prime } = ( \underbrace { 1 , 1 , l _ { x } , l _ { y } , 1 , l _ { z } , 1 _ { z } } _ { 1 2 + N } , \underbrace { 1 ^ { 2 } , \dots \dots , 1 , 1 , 1 , l _ { z } , l _ { x } ^ { 2 } , l _ { y } ^ { 2 } } _ { 1 2 + N } ) } \end{array}\tag{15}
$$

$$
\begin{array} { r } { \Big \{ L _ { 1 } [ i ] + L _ { 2 } [ i ] = L ^ { \prime \prime } [ i ] ( S [ i ] = 1 , i \in [ 1 , 1 2 + N ] ) } \\ { \qquad \lfloor L _ { 1 } [ i ] = L _ { 2 } [ i ] = L ^ { \prime \prime } [ i ] ( S [ i ] = 0 , i \in [ 1 , 1 2 + N ] ) } \end{array}\tag{16}
$$

Later, the UAV employs two keys $\tilde { M } _ { 1 } , \tilde { M } _ { 2 }$ to encrypt the split vector $L ^ { \prime \prime } = \{ L _ { 1 } , L _ { 2 } \}$ , and uploads the ciphertexts ${ { C } _ { L } } =$ $\{ L _ { 1 } \tilde { M _ { 1 } } , L _ { 2 } \tilde { M _ { 2 } } \}$ and $E ( U _ { i } )$ to the $Z { \mathrm { S } } .$ where $E ( U _ { i } )$ denotes as the AES ciphertext of UAV identifier.

## - Stage 2: Log Index and DAS Generation

As designed in CMLF, all UAVs located in one aerial zone encrypt the log files (labeled by UAVsâ identifiers) and multi-dimensional attribute vector sets (considered as multi-dimensional data points) with the AES algorithm and upload them to the ZA.

<!-- image-->  
Fig. 6. DAS construction.

After receiving the encrypted data from all UAVs and decrypting the data points, the ZA first builds the plaintexts of the log index with the G-tree. Each leaf node in the tree contains a data point and a log file pointer, while each non-leaf node contains a data range covering all the child nodes.

Moreover, the ZA applies the hash function $H ( \cdot )$ and the key $K _ { H }$ to compute the hash value $H ( I D _ { i } , K _ { H } )$ , where $I D _ { i } ( i \in [ 1 , n ] )$ donates the identifier of each data record. As shown in Fig. 6, the ZA links the hash values of leaf nodes covered by the same parent node with the concatenation operation, and also computes the hash value of this linked string as the non-leaf node hash $H a s h ( N L _ { j } ) ( j \in$ $[ 1 , m ] )$ . The operation is repeated until the hash value of the root node Hash(Root) is computed. The ZA encrypts the hash value of each node with the RSA private key $s k .$ , all signatures are stored on the corresponding node.

$$
\left\{ \begin{array} { l l } { S i g ( H a s h ( I D _ { i } ) ) ( i \in [ 1 , n ] ) } \\ { S i g ( H a s h ( N L _ { j } ) ) ( j \in [ 1 , m ] ) } \end{array} \right.\tag{17}
$$

For the plaintexts of multi-dimensional data points and ranges in the index, the ZA performs the following encryption operations. (i) As described in (18), the ZA inserts w random 4-d vectors into the w attribute vectors (corresponds to a w-d data range included in a nonleaf node), where all random numbers $r _ { k } \ll x _ { k , l }$ and ${ r _ { k } } \ll { x _ { k , r } } , ( k \in [ 1 , w ] )$ . Later, M 1 s are added to each vector $R V _ { j } ( j \in [ 1 , 2 w ] )$ , then each $R V _ { j }$ is obfuscated by the $\Omega ( \cdot )$ and $K _ { \Omega }$ . The ZA encrypts each obfuscated vector with the key $\tilde { M } _ { 3 }$ and a random positive number $r p _ { 1 }$ , and outputs the ciphertexts $C _ { R } = r p _ { 1 } ( \tilde { M } _ { 3 } R V _ { 1 } , \cdot \cdot \cdot$ $\tilde { M } _ { 3 } R V _ { 2 w } )$

$$
R V _ { j } = \left\{ \begin{array} { l l } { ( l _ { k } h _ { k } , l _ { k } , h _ { k } , 1 ) ^ { T } ( j = 2 k - 1 ) } \\ { ( r _ { k , 1 } , r _ { k , 2 } , r _ { k , 3 } , r _ { k , 4 } ) ^ { T } ( j = 2 k ) } \end{array} \right.\tag{18}
$$

(ii) As depicted in (19), the ZA inserts w random 4-d vectors into the w attribute vectors (corresponds to a w-d data point) included in a leaf node, where all random numbers $r _ { k } ^ { \prime } \ll d _ { k } , ( k \in [ 1 , w ] )$ . Later, M 1 s are added to each vector $D V _ { i } ( i \in [ 1 , 2 w ] )$ ), then each $D V _ { i }$ is obfuscated by the $\Omega ( \cdot )$ and $K _ { \Omega }$ . Each obfuscated vector is encrypted with the key $\tilde { M _ { 3 } }$ and a random positive number $r p _ { 2 }$ , then the ciphertexts $C _ { D } = r p _ { 2 } ( \tilde { M } _ { 3 } D V _ { 1 } , \cdot \cdot \cdot \tilde { M } _ { 3 } D V _ { 2 w } )$ are output by the ZA.

$$
D V _ { i } = \left\{ \begin{array} { l l } { \left( d _ { k } ^ { 3 } , d _ { k } ^ { 2 } , d _ { k } , 1 \right) ^ { T } ( i = 2 k - 1 ) } \\ { \left( r _ { k , 1 } ^ { \prime } , r _ { k , 2 } ^ { \prime } , r _ { k , 3 } ^ { \prime } , r _ { k , 4 } ^ { \prime } \right) ^ { T } ( i = 2 k ) } \end{array} \right.\tag{19}
$$

Finally, the secure log index I containing the DAS is uploaded to the LAC platform together with the encrypted log files $\{ E ( l o g ) , E ( U _ { i } ) \}$ for storage, and each index is identified by the GeoHash value of the aerial zone it belongs to.

## C. GenToken

The user first determines the location query range $L _ { Q }$ and data query range $M R Q$ , then executes this algorithm to generate the location query token $T K _ { Q } ^ { L }$ and log query token $\{ T \check { K } _ { Q } ^ { D } , T K _ { Q } ^ { R } \}$ as follows.

The user provides two query points $A ( a _ { x } , a _ { y } , a _ { z } )$ and $B ( b _ { x } , b _ { y } , b _ { z } )$ in one aerial zone, and takes the sphere constructed with the diameter of the line between the two points as the location query range. According to CMLD, the user first generates the plaintext of the location query vector $Q _ { L }$ with two points A, B, and adds N random numbers to $Q _ { L }$ to acquire $Q _ { L } ^ { \prime } .$ , where $\begin{array} { r } { \sum _ { i = 1 } ^ { N } n _ { i } = 0 } \end{array}$ , as shown in (20). Then the user obfuscates vector $Q _ { L } ^ { \prime }$ as $Q _ { L } ^ { \prime \prime }$ with the Î©(Â·) and $K _ { \Omega }$ , and splits $Q _ { L } ^ { \prime \prime }$ to obtain two $( 1 2 + N ) { \mathrm { - d } }$ vectors using the split vector S, as shown in (21).

$$
\begin{array} { l } { { Q _ { L } = \left( a _ { x } b _ { x } , - a _ { x } , - b _ { x } , 1 , a _ { y } b _ { y } , - a _ { y } , - b _ { y } , 1 , a _ { z } b _ { z } , \right. } } \\ { { \mathrm { } } } \\ { { \mathrm { } } } \\ { { \left. \begin{array} { r l } { { - a _ { z } , - b _ { z } , 1 } } \\ { { } } \\ { { \vphantom { \bigg ( } \Downarrow } } \end{array} \right) } } \\ { { \left. \begin{array} { r l } { { \surd } _ { L } = \left( a _ { x } b _ { x } , - a _ { x } , - b _ { x } , 1 , a _ { y } b _ { y } , - a _ { y } , - b _ { y } , 1 , a _ { z } b _ { z } \right) } \\ { { } } \\ { { - a _ { z } , - b _ { z } , 1 , \underbrace { n _ { 1 } , \ldots , n _ { N } } _ { N } } } \end{array} \right. } } \end{array}
$$

$$
Q _ { \phantom { \prime \prime } L } ^ { \prime \prime } = ( \underbrace { - a _ { x } , 1 , a _ { y } b _ { y } , n _ { 1 } , \dots , n _ { N } , - b _ { x } , 1 , - b _ { z } } _ { 1 2 + N } )\tag{20}
$$

$$
\begin{array} { r } { \left\{ Q _ { L } ^ { 1 } [ i ] + Q _ { L } ^ { 2 } [ i ] = Q _ { L } ^ { \prime \prime } [ i ] ( S [ i ] = 0 , i \in [ 1 , 1 2 + N ] ) \right. } \\ { \left. Q _ { L } ^ { 1 } [ i ] = Q _ { L } ^ { 2 } [ i ] = Q _ { L } ^ { \prime \prime } [ i ] ( S [ i ] = 1 , i \in [ 1 , 1 2 + N ] ) \right. } \end{array}\tag{21}
$$

Later, the user generates the location query token $T K _ { Q } ^ { L } =$ $\{ M _ { 1 } Q _ { L } ^ { 1 } , M _ { 2 } Q _ { L } ^ { 2 } \}$ with two keys $M _ { 1 } , M _ { 2 }$

- Stage 2: Log Query Token Generation Stage 2: Log Query Token Generation

The user presents one data range query $M R Q =$ $\{ R _ { 1 } , \ldots , R _ { w } \}$ , where $R _ { k } = [ x _ { k } ^ { l } , x _ { k } ^ { r } ] ( k \in [ 1 , w ] )$ . Based on CMLF, the user first generates the plaintexts of twokind data query vectors $D P _ { i }$ and DRi with $M R Q$ . Then the user executes the below generation operations. (i) As shown in (22), the user inserts w random 4-d vectors into the w range query vectors $D R _ { j } ( j \in [ 1 , w ] )$ , where all random numbers $r _ { k } ^ { R } \ll x _ { k , l }$ and ${ r _ { k } ^ { R } } \ll x _ { k , r } , ( k \in [ 1 , w ] )$ Later, M random numbers $m _ { i }$ are added to each vector ${ D R _ { j } } ( j \in [ 1 , 2 w ] )$ , where $\begin{array} { r } { \sum _ { i = 1 } ^ { M } m _ { i } = 0 } \end{array}$ and each $D R _ { j }$ is obfuscated by the $\Omega ( \cdot )$ and $K _ { \Omega }$ . The user encrypts each obfuscated vector with the key $M _ { 3 }$ and a random positive number $r p _ { 1 } ^ { \prime }$ , then outputs the range query token $\bar { T } K _ { Q } ^ { R } = r p _ { 1 } ^ { \prime } ( D \bar { R _ { 1 } } \bar { M } _ { 3 } , \dots , D \bar { R } _ { 2 w } { \cal M } _ { 3 } )$

$$
D R _ { j } = \left\{ \begin{array} { l l } { \left( - ( x _ { k } ^ { r } ) ^ { 2 } - x _ { k } ^ { r } \delta \right) } \\ { - ( x _ { k } ^ { r } ) ^ { 2 } - x _ { k } ^ { r } \delta } \\ { - x _ { k } ^ { l } x _ { k } ^ { r } - x _ { k } ^ { l } \delta } \\ { x _ { k } ^ { l } x _ { k } ^ { r } ( x _ { k } ^ { r } + \delta ) } \end{array} \right. ( j = 2 k - 1 )\tag{22}
$$

(ii) As shown in (23), the user inserts w random 4-d vectors into the w point query vectors $D P _ { i } ( i \in [ 1 , w ] )$ , where all random numbers $r _ { k } ^ { D } \ll x _ { k , l }$ and $r _ { k } ^ { D } \ll x _ { k , r } , ( k \in [ 1 , w ] )$ . Later, M random numbers $m _ { i }$ are added to each vector $D P _ { i } ( i \in [ 1 , 2 w ] )$ , where $\begin{array} { r } { \sum _ { i = 1 } ^ { M } m _ { i } = 0 } \end{array}$ and each $D P _ { i }$ is obfuscated by the $\Omega ( \cdot )$ and $K _ { \Omega }$ . The user encrypts each obfuscated vector with the key $M _ { 3 }$ and a random positive number $r p _ { 2 } ^ { \prime }$ , then outputs the point query token $T K _ { Q } ^ { D } =$ $r p _ { 2 } ^ { \prime } ( D P _ { 1 } \bar { M _ { 3 } } , \ldots , D P _ { 2 w } M _ { 3 } )$

$$
D P _ { i } = \left\{ \left( \begin{array} { c } { 1 } \\ { - x _ { k } ^ { l } - x _ { k } ^ { r } + \delta } \\ { x _ { k } ^ { l } x _ { k } ^ { r } - x _ { k } ^ { l } \delta - x _ { k } ^ { r } \delta } \\ { x _ { k } ^ { l } x _ { k } ^ { r } \delta } \end{array} \right) \left( i = 2 k - 1 \right) \right. \nonumber\tag{23}
$$

Finally, the user transfers the location query token to the ZA, and transfers the log query tokens along with the GeoHash of the query aerial zone to the LAC platform.

## D. Search

Once both the LAC platform and ZS receive the query tokens, they perform the following retrieval operations. (i) The ZS calculates the inner product between the location token $T K _ { O } ^ { L }$ and the location data of UAVs. As demonstrated in (24), if $C _ { L } \cdot T K _ { Q } ^ { L } \le 0$ , the UAV $U _ { i }$ located in the location query $L _ { Q }$ Otherwise, $U _ { i }$ is outside the $L _ { Q }$

$$
\begin{array} { l } { { C _ { L } \cdot T K _ { Q } ^ { L } = \left\{ L _ { 1 } \cdot \vec { M } _ { 1 } , L _ { 2 } \cdot \vec { M } _ { 2 } \right\} \cdot \left\{ M _ { 1 } \cdot Q _ { L } ^ { 1 } , M _ { 2 } \cdot Q _ { L } ^ { 2 } \right\} } } \\ { { \ } } \\ { { \displaystyle \quad = \left| \operatorname* { d e t } ( M _ { 1 } ) \right| L _ { 1 } \cdot Q _ { L } ^ { 1 } + \left| \operatorname* { d e t } ( M _ { 2 } ) \right| L _ { 2 } \cdot Q _ { L } ^ { 2 } = L ^ { \prime \prime } \cdot Q _ { L } } } \\ { ~ } \\ { { \displaystyle \quad = \Bigg ( a _ { x } b _ { x } - a _ { x } l _ { x } - b _ { x } l _ { x } + l _ { x } ^ { 2 } + a _ { y } b _ { y } - a _ { y } l _ { y } - b _ { y } l _ { y } } } \\ { { \ } } \\ { { \displaystyle \quad \quad + l _ { y } ^ { 2 } + a _ { z } b _ { z } - a _ { z } l _ { z } - b _ { z } l _ { z } + l _ { z } ^ { 2 } + \sum _ { i = 1 } ^ { N } n _ { i } \Bigg ) } } \\ { { \ } } \\ { { \displaystyle = \overrightarrow { L \ A } \cdot \overrightarrow { L \ B } } } & { { \ \mathrm { ( } } } \end{array}\tag{24}
$$

(ii) The LAC platform follows the G-tree retrieval. Starting from the root, it first calculates the inner product between the range query token $T K _ { Q } ^ { R }$ and the data range ciphertexts $C _ { R }$ starting from the root. If $\check { T } K _ { Q } ^ { R } \cdot C _ { R } \leq 0$ , the LAC platform continues to traverse down; Otherwise, it abandons this non-leaf node. After the traversal reaches the leaf nodes, the LAC platform calculates the inner product between the point query token $T K _ { Q } ^ { D }$ and the data point ciphertexts $C _ { D }$ . If $T K _ { Q } ^ { D } \cdot C _ { D } \leq 0$ , the data point falls within the query range; Otherwise, it is outside the range. Equations (25) and (26) demonstrate the above two calculation processes, respectively.

$$
\begin{array} { r l } { \langle \mathcal { R } ( \xi ) \rangle _ { \mathcal { C } } ^ { \dagger } } & { \le _ { \mathbf { R } _ { h } } ( \xi ) , } \\ & { = \Bigg \{ \langle \mathcal { R } ( \xi ) , \Psi ( \xi ) ( \xi ) , \mathcal { R } ( \xi ) , \mathcal { R } ( \xi ) \rangle _ { \mathcal { D } } , \ \mathcal { R } ( \xi ) , \tilde { \mathbf { R } } ( \xi ) \cdot \mathcal { R } - \xi , \tilde { \mathbf { R } } ( \xi ) \cdot \mathcal { R } \cdot \mathbf { R } _ { h } \ \xi \rangle } \\ & { = \Bigg \{ \langle \mathcal { R } ( \xi ) , \Psi ( \xi ) , \mathcal { R } ( \xi ) \rangle _ { \mathcal { D } } , \ \mathcal { R } ( \xi ) , \tilde { \mathbf { R } } ( \xi ) \cdot \mathcal { R } _ { h } \xi \Bigg \} } \\ & { = \Bigg \{ \langle \mathcal { R } ( \xi ) , \Psi ( \xi ) , \mathcal { R } ( \xi ) \rangle _ { \mathcal { D } } , \ \tilde { R } ( \xi ) \cdot \mathcal { R } _ { h } \xi \Bigg \} } \\ & { \quad + \langle \mathcal { R } ( \xi ) , \Psi ( \xi ) , \mathcal { R } ( \xi ) \rangle _ { \mathcal { D } } , \ \tilde { R } ( \xi ) \cdot \tilde { \mathbf { R } } _ { h } \xi \Bigg \} } \\ & { \le _ { \mathbf { R } _ { h } } ( \xi ) , \Bigg \{ \langle \mathcal { R } ( \xi ) , \Psi ( \xi ) , \mathcal { R } ( \xi ) \rangle _ { \mathcal { D } } , \ \tilde { R } ( \xi ) \} } \\ & { \leq _ { \mathbf { R } _ { h } } ( \xi ) , } \\ &  \quad \mathrm { ~ \ } \mathrm { ~ \ } \mathrm { ~ \ } \mathrm { ~ \ } \mathrm { ~ \ } \mathrm { ~ \ } \mathrm { ~ \ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } \mathrm  ~  \end{array}\tag{25}
$$

(26)

Finally, both the LAC platform and ZS return the query results $R e s u l t _ { L }$ and $R e s u l t _ { Q }$ to the user, where $R e s u l t _ { Q }$ contains not only the ciphertexts of qualified log files, but also the AV I and the signatures of the reached leaf nodes during retrieval.

Remark 1: As we designed in GenIndex and GenT oken, there exists $r _ { k } \ll x _ { k , l } , r _ { k } \ll x _ { k , r } , r _ { k } ^ { \prime } \ll d _ { k }$ and $r _ { k } ^ { D } , r _ { k } ^ { R } \ll x _ { k , l }$ $r _ { k } ^ { D } , r _ { k } ^ { R } \ll x _ { k , r }$ . Hence, the random numbers only serve as perturbations to preserve sensitive information, but cannot have an effect on the positive or negative of the inner products $T K _ { Q } ^ { R } \cdot C _ { R }$ and $T K _ { Q } ^ { D } \cdot C _ { D } , \mathrm { i . e . }$ , the probability of returning the data point is negligible if $D P$ is not inside the data range.

## E. Verify

Since data completeness verification is only aimed at data queries but not location queries, the AV I formation and completeness verification process are illustrated with the assistance of Fig. 6. We also describe the result decryption with a verification flag.

AV I Formation: We assume that $I D _ { 4 }$ and $I D _ { 5 }$ are the query results, the AV I returned by the LAC platform consists of the signatures $S i g ( H a s h ( N L _ { 3 } ) ) , S i g ( H a s h ( N L _ { 6 } ) )$ of the non-leaf nodes $N L _ { 3 } , N L _ { 6 }$ , the signatures $S i g ( H a s h ( I D _ { 3 } ) )$ , $S i g ( H a s h ( I D _ { 6 } ) )$ ) of the leaf nodes $I D _ { 3 } , I D _ { 6 }$ and the signature of the root $S i g ( H a s h ( R o o t ) )$ ).

Completeness Verification: The user first decrypts each signature in AV I and $R e s u l t _ { Q }$ with the RSA public key pk to obtain the Hash set using:

$$
\{ H a s h ( N L _ { 3 } ) , H a s h ( N L _ { 6 } ) , H a s h ( I D _ { 3 } ) , H a s h ( I D _ { 6 } ) \}\tag{27}
$$

Combined with the $H a s h ( I D _ { 3 } )$ , Has $h ( I D _ { 6 } )$ of leaf nodes $I D _ { 3 } , \ I D _ { 6 }$ , the user reconstruct the $H a s h ^ { \prime } ( R o o t )$ from the bottom as described in (28). If $H a s h ^ { \prime } ( R o o t ) = H a s h ( R o o t )$ ï¼ the query results are complete; Otherwise, the query results are incomplete.

$$
\begin{array} { r l } & { H a s h ( H a s h ( N L _ { 3 } ) | | H a s h ( I D _ { 3 } ) | | H a s h ( I D _ { 4 } ) | | } \\ & { H a s h ( I D _ { 5 } ) | | H a s h ( I D _ { 6 } ) | | H a s h ( N L _ { 6 } ) ) } \\ & { = H a s h ( H a s h ( N L _ { 1 } ) | | H a s h ( N L _ { 2 } ) ) } \\ & { = H a s h ^ { \prime } ( R o o t ) } \end{array}\tag{28}
$$

Result Decryption: Based on Definition 5, if the completeness verification passes, indicated by the flag $b = 1$ , the users decrypt the ciphertexts $D _ { R }$ with the symmetric key k and obtain the plaintext result $P _ { R }$ . Otherwise, the users reject to decrypt the ciphertexts $D _ { R }$

## VII. SECURITY ANALYSIS

In this section, we prove the semantic security of LSPSS for Chosen Plaintext Attack (CPA), single-dimensional privacy, and query unlinkability during search based on the Known Background Model.

## A. Security Under Known Background Model

Lemma 1: The LSPSS satisfies the semantic security if the encrypted data are indistinguishable under Chosen Plaintext Attack (IND-CPA).

Proof: We only require to prove that the probability of the probabilistic polynomial-time (PPT) adversary breaking the encrypted data of the LSPSS is negligible. Suppose the challenger C performs $G e n K e y ( 1 ^ { \lambda } )$ to provide an LSPSS encryption system $K = \{ K _ { 1 } , K _ { 2 } \}$ and transfers $K _ { 2 }$ to a PPT adversary A. Then A generates and uploads two data records $d _ { 0 } , d _ { 1 }$ to the C. The C randomly selects $b \in \{ 0 , 1 \}$ , encrypts $d _ { b }$ using $K _ { 1 }$ , and returns the ciphertext to A. Later the A presents a guess $b ^ { \prime }$ of b. Due to the perturbation and permutation of the encryption, random numbers are employed each time, so converting one plaintext into diverse ciphertexts based on the identical key. Additionally, since the matrix keys are randomly generated, it is hard to be broken. In conclusion, it is obvious to deduce that A cannot guess the correct b with a probability high than $1 / 2$ Hence the advantage in this game is

$$
A d v _ { L S P A , \mathcal { A } } ^ { C P A } ( \lambda ) = \left| \operatorname* { P r } [ b = b ^ { \prime } ] - \frac { 1 } { 2 } \right| < n e g l ( \lambda )
$$

Thus the LSPSS is proved to be semantically secure.

Based on Security Definition, given two histories H and $H ^ { \prime }$ with the same trace $T r .$ , if the server with the distribution of queries cannot distinguish which view of them is generated by the simulator S, they cannot learn extra information beyond what can be leaked. Thus the LSPSS is secure under the known background model.

Theorem 1: LSPSS is secure against semi-honest adversaries under the known background model.

Proof: The simulator S can simulate a view $V ^ { \prime }$ indistinguishable from the view $V ( H ) = \{ D ^ { * } , L ^ { * } , I _ { D } ^ { * } , I _ { L } ^ { * } , T K ( D )$ $T K ( L ) \}$ of the server as follows.

- S randomly selects a $d _ { i } ^ { \prime } \in \{ 0 , 1 \} ^ { | d _ { i } ^ { * } | } , d _ { i } ^ { * } \in D ^ { * } ( i \in$ $[ 1 , | D ^ { * } | ] )$ and a $l _ { i } ^ { \prime } \in \{ 0 , 1 \} ^ { | l _ { j } ^ { * } | } , l _ { i } ^ { * } \in L ^ { * } ( j \in [ 1 , | L ^ { * } | ] )$ , then generates $D ^ { \prime } = \bar { \{ d _ { i } ^ { \prime } \} } ( i \in [ 1 , | \bar { D } ^ { * } | ] )$ and $L ^ { \prime } = \{ l _ { j } ^ { \prime } \} ( j \in$ $[ 1 , | L ^ { * } | ] )$

- $\boldsymbol { \mathcal { S } }$ randomly selects two invertible matrices $M _ { 1 } ^ { \prime } , M _ { 2 } ^ { \prime } \in$ $\mathbb { R } ^ { 4 \times 4 } , ~ M _ { 3 } ^ { \prime } \overset { \cdot } { \in } \mathbb { R } ^ { 1 2 \times 1 2 }$ and forms $K ^ { \prime } = \{ M _ { 1 } ^ { \prime } , M _ { 2 } ^ { \prime } , \ M _ { 3 } ^ { \prime } \}$ Also, S generates a permutation function $\Omega ^ { \prime } ( \cdot )$ and the key $K _ { \Omega } ^ { \prime }$

S generates one vector of 2w elements for each $v _ { i } ^ { \prime } \in$ $I _ { D } ^ { \prime } ( D ^ { \prime } ) , i \in [ 1 , | I _ { D } ^ { * } | ]$ and one vector $u _ { j } ^ { \prime } \in I _ { L } ^ { \prime } ( L ^ { \prime } ) , \dot { j } \in$ $[ 1 , | I _ { L } ^ { * } | ]$ as the data index and location index, respectively. Then S performs as follows.

(i) For each element of $v _ { i } ^ { \prime } , s$ replaces it with one 4-d vector $( r _ { i , 1 } , \ldots , r _ { i , 4 } ) ^ { T }$ , where $r _ { i , k } ( i \in [ 1 , n ] )$ is a random number. For each element of $u _ { i } ^ { \prime } , s$ also replaces it with one 12-d vector $( r _ { j , 1 } ^ { \prime } , \ldots , r _ { j , 1 2 } ^ { \prime } ) ^ { \bar { T } }$ , where $r _ { j , k } ^ { \prime } ( j \in [ 1 , m ] )$ also be a random number. Later S obfuscates each $\boldsymbol { v } _ { i } ^ { \prime }$ and $u _ { i } ^ { \prime }$ with the $\Omega ^ { \prime } ( \cdot )$ and $K _ { \Omega } ^ { \prime }$

(ii) S encrypts each $\boldsymbol { v } _ { i } ^ { \prime }$ and $u _ { i } ^ { \prime }$ with the $M _ { 2 } ^ { \prime }$ and $M _ { 3 } ^ { \prime }$ , respectively. Then S obtains $I _ { D ^ { \prime } } ^ { \prime } = \{ E n c _ { K ^ { \prime } } ( v _ { i } ^ { \prime } ) , i \in [ 1 , | I _ { D } ^ { * } | ] \}$ and $I _ { L ^ { \prime } } ^ { \prime } = \{ E n c _ { K ^ { \prime } } ( u _ { j } ^ { \prime } ) , \bar { j } \in [ 1 , | I _ { L } ^ { * } | ] \}$

- S builds the query token $T K ( D ^ { \prime } )$ and $T K ( L ^ { \prime } )$ as follows. (i) For each $q d _ { i } ^ { \prime } \in Q ^ { \prime } ( D ^ { \prime } ) ( i \in [ 1 , \tau ] )$ , S generates one vector $q v _ { i } ^ { \prime }$ of 2w elements and replaces each element with one 4-d vector $( d r _ { i , i } , \ldots , d r _ { i , 4 } ) ^ { \bar { T } }$ , where $d r _ { i , k } ( i \in [ 1 , n ] )$ is a random number. For each element $q l _ { j } ^ { \prime } \in Q ^ { \prime } ( L ^ { \prime } ) ( j \in$ $[ 1 , \omega ] ) , S$ generates one vector $q u _ { j } ^ { \prime }$ and replaces it with one 12-d vector $( l r _ { j , 1 } ^ { \prime } , \ldots , l r _ { j , 1 2 } ^ { \prime } ) ^ { T }$ , where $l r _ { j , k } ( j \in [ 1 , m ] )$ also be a random number. Then S obfuscates each ${ { q } { { v } _ { i } ^ { \prime } } }$ and $q u _ { j } ^ { \prime }$ with the $\Omega ^ { \prime } ( \cdot )$ and $K _ { \Omega } ^ { \prime }$

(ii) S respectively encrypts each $q v _ { i } ^ { \prime }$ and $q u _ { j } ^ { \prime }$ using $M _ { 1 } ^ { \prime }$ and $M _ { 3 } ^ { \prime - 1 }$ to generate the query tokens for each ${ q d _ { i } ^ { \prime } }$ and $q l _ { j } ^ { \prime }$ Thus S acquires $T K ( D ^ { \prime } )$ and $T K ( L ^ { \prime } )$

$\boldsymbol { \mathcal { S } }$ outputs the view $V ^ { \prime } = \{ D ^ { \prime } , L ^ { \prime } , I _ { D ^ { \prime } } ^ { \prime } , I _ { L ^ { \prime } } ^ { \prime } , T K ( D ^ { \prime } )$ $T K ( L ^ { \prime } ) \}$

It is obvious to prove the correctness of the above construction with querying $T K ( D ^ { \prime } ) , T K ( L ^ { \prime } )$ on $I _ { D ^ { \prime } } ^ { \prime } , I _ { L ^ { \prime } } ^ { \prime }$ . The trace generated by the indexes T K(D ), T K(L ) and tokens $I _ { D ^ { \prime } } ^ { \prime } , I _ { L ^ { \prime } } ^ { \prime }$ is the same as the trace of the server. We affirm that no PPT adversary can distinguish the view $V ^ { \prime }$ from $V ( H )$

Specifically, since the semantic security of LSPSS, no PPT adversary can distinguish the $D ^ { * } , L ^ { * }$ from D , L . Also, due to the indistinguishability of random perturbation and permutation of the encryption, the PPT adversary with queries and probability pairs cannot distinguish which tokens are generated by the same queries. Thus the PPT adversary cannot employ the distributions of ciphertexts and encrypted tokens to infer sensitive information. -

## B. Single-Dimensional Privacy

Theorem 2: LSPSS can preserve single-dimensional privacy during retrievals.

Proof: We employ two-kind perturbation-based matrix encryption for location range query and data range query, respectively. Based on the query mechanism of two-kind encryption, the servers are only able to know the intersection results by inner product calculation. Moreover, with the permutation and perturbation of matrix encryption, the servers cannot distinguish the obfuscated leaf nodes or non-leaf nodes in the secure data index. Thus the servers cannot deduce the information on which records satisfy each single dimension of the query, i.e., the LSPSS can preserve single-dimensional privacy during retrievals. -

## C. Query Unlinkability

Theorem 3: LSPSS can achieve query unlinkability during query token generation.

Proof: (i) Suppose that the user presents one location range query $L _ { Q }$ and generates one original query vector $Q _ { L }$ . The user generates Î· location query tokens with the identical query $Q _ { L }$ Based on the token generation algorithm GenT oken, the user first extends Î· vectors $Q _ { L }$ to $( Q _ { L } ^ { \prime } ) _ { i } ( i \in [ 1 , \eta ] )$ with N random numbers $n _ { i }$ , where $\begin{array} { r } { \sum _ { i = 1 } ^ { N } n _ { i } = 0 } \end{array}$ . Then, after splitting the $( Q _ { L } ^ { \prime } ) _ { : }$ i using the split vector S, the user exploits the keys $M _ { 1 }$ and $M _ { 2 }$ to encrypt $\{ ( Q _ { L } ^ { \prime } ) _ { i } ^ { 1 } , ( Q _ { L } ^ { \prime } ) _ { i } ^ { 2 } \} ( i \in [ \bar { 1 , \eta } ] )$ and output the tokens $\{ T K _ { k } ( Q _ { L } ) \} _ { k = 1 } ^ { \eta }$ . Note that N random numbers $n _ { i }$ inserted into each $Q _ { L }$ just need to satisfy $\begin{array} { r } { \sum _ { i = 1 } ^ { N } n _ { i } = 0 } \end{array}$ , thus there exists infinite combinations, i.e., none of the Î· location tokens are the same. According to Definition 3, the location range query in LSPSS realizes query unlinkability.

(ii) Similarly, suppose that the user presents one data range query MRQ and generates two original query vector sets $Q _ { R } =$ $\{ D R _ { j } \} ( j \in [ 1 , w ] )$ and $Q _ { D } = \{ D P _ { i } \} ( i \in [ 1 , w ] )$ . The user generates Î· data range tokens with the identical query MRQ. Based on GenT oken, the user first inserts w 4-d random vectors into each vector set $Q _ { R } ^ { k } ( k \in [ 1 , \eta ] )$ and $Q _ { D } ^ { k } ( k \in [ 1 , \eta ] )$ , respectively. Then the user extends each vector $D R _ { j }$ and $D P _ { i }$ in Î· sets $Q _ { R } ^ { k }$ and $Q _ { D } ^ { k }$ with M random numbers $m _ { i } .$ , where $\begin{array} { r } { \sum _ { i = 1 } ^ { M } m _ { i } = } \end{array}$ 0. Later, the user employs the key $M _ { 3 }$ to encrypt $Q _ { R } ^ { k } = $ $\{ D R _ { j } , ( j \in [ 1 , 2 w ] ) \} _ { k = 1 } ^ { \eta }$ and $Q _ { D } ^ { k } = \{ D P _ { i } , ( i \in [ 1 , 2 w ] ) \} _ { k = 1 } ^ { \tilde { \eta } }$ and output the tokens $\{ T K _ { k } ( Q _ { R } ) \} _ { k = 1 } ^ { \eta }$ and $\{ T K _ { k } ( Q _ { D } ) \} _ { k = 1 } ^ { \eta } .$ Note that M random numbers $m _ { i }$ inserted into each $Q _ { R }$ and $Q _ { D }$ just need to satisfy $\begin{array} { r } { \sum _ { i = 1 } ^ { M } m _ { i } = 0 } \end{array}$ . This results in infinite combinations, i.e., none of the Î· data tokens are the same. According to Definition 3, the data range query in LSPSS achieves query unlinkability.

In conclusion, LSPSS can achieve query unlinkability during query token generation. -

TABLE I  
SCHEMES COMPARISON
<table><tr><td>Scheme</td><td>Asymptotic Query Complexity</td><td>Basic Operation</td><td></td><td>Query UnlinkabilitySingle-dimensional Privacy</td><td>Result Verification</td></tr><tr><td>Maple [17]</td><td> $O ( \log | x | \cdot d )$ </td><td>Bilinear Pairing</td><td></td><td></td><td></td></tr><tr><td>WangR [24]</td><td> $O ( \log | x | \cdot d )$ </td><td>Multiplication over R</td><td></td><td></td><td></td></tr><tr><td>PRQ[28]</td><td> $O ( \log | x | \cdot d \cdot N ^ { 2 } )$ </td><td>Multiplication over R</td><td></td><td></td><td></td></tr><tr><td>LSPSS</td><td> $O ( \log | x | \cdot d )$ </td><td>Multiplication over R</td><td>xx&gt;&gt;</td><td>&lt;Ã&gt;&gt;</td><td>xÃÃ&gt;</td></tr></table>

## VIII. PERFORMANCE EVALUATION

To evaluate the comprehensive performance, we first compare our LSPSS with other similar schemes from the view of index construction and querying. Furthermore, we discuss the performance of our LSPSS in index construction, query token generation, querying, and result verification.

Experimental Settings: We implement our LSPSS with Python (Python 3.7) on a PC (AMD Ryzen 5 4600 U Radeon Graphics 2.10 Hz, Windows 10). Additionally, we exploited a UAV environmental monitoring log dataset called UAVs Detection from the Kaggle.2 The attributes we extracted include the Location (i.e., altitude, latitude, and longitude), Temperature, Humidity, Concentration, Air Velocity, Light and Radiation Intensity.

Parameter Settings: We set the experimental parameter as the dataset size 5000, 10000, 15000, 20000, 25000, the attribute dimension from 2 to 9 (i.e., three dimensions for location and six dimensions for log files), and the number of UAVs 500, 1000, 1500, 2000, 2500 in each aerial zone. The keysâ bitsize of RSA and AES are fixed as 1024 and 128. For the objectivity of experiments, we randomly choose the query ranges and acquire the averaging results of repeated experiments.

## A. Comparison With Prior Arts

According to Related Works, data privacy preservation in aerial computing is mainly implemented with the assistance of blockchain and federated learning (FL) techniques. To compare the performance of LSPSS with other cryptography-based schemes, we first present a comprehensive comparison of LSPSS and other privacy-preserving MRQ schemes in Table I. Later, we perform the experiments of Maple, PRQ and LSPSS in index construction and querying. Note that the bilinear pairing operations in Maple are implemented with PyPBC library (512 bits security parameter), we also achieve the SHA-256 with PySHA3 library supported by Python.

1) Index Construction: Concretely, the experimental results of index construction are shown in Fig. 7(a) and (b) from the perspectives of time and storage consumption. The attribute dimension and the size of matrix keys are fixed to w = 2 and (16 Ã 16) respectively, as well as the dataset size |D| varies from 5000 to 25000. As we observed, the time and storage consumption both show a linear increasing trend as |D| increases. By comparison, Maple applies public-key cryptography called hidden vector encryption (HVE) to achieve selective security, thus LSPSS is on average about 120 and 16 times smaller than Maple in terms of time and storage consumption, respectively. And compared with PRQ, the time consumption of PRQ is also larger than that of LSPSS because of the larger coefficient of the time complexity.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 7. (a) The time consumption of index construction for three schemes with diverse datasets. (b) The storage consumption of index construction for three schemes with diverse datasets.

2) Query: In comparison with prior arts of querying, we perform the experiments from the perspective of dataset size and dimension number, respectively. Moreover, we also experimentally compare the query precision and recall rate of the three schemes under the same conditions.

Querying: Specifically, Fig. 8(a) and (b) depict the time consumption of querying with diverse schemes. The size of matrix keys is fixed to (16 Ã 16)-dimensions for PRQ and LSPSS in these experiments. We set the attribute dimension as w = 2, as well as the dataset size |D| varies from 5000 to 25000 in Fig. 8(a). Moreover, the dataset size is set as $| D | = 2 5 0 0 0$ and the attribute dimension w varies from 2 to 6 in Fig. 8(b). Intuitively, the time consumption of querying linearly increases with the sizes of the dataset and the attribute dimension. Maple is on average about 900 and 850 times larger than LSPSS in terms of the datasets and attribute dimensions, respectively. Compared with PRQ, the time consumption of LSPSS is slightly smaller than that of PRQ, not only because of the smaller coefficient query time complexity, but also due to the setting of the variable-length partition number in G-tree, which reduces the effect of data amount and distribution on the query.

Precision and Recall: Generally speaking, precision is defined as the proportion of true results in the whole query results, and recall is defined as the proportion of true query results in the whole true results. The calculation of precision and recall are depicted as (29) and (30), where T P and $F P$ represent the number of true and false results, and F N represents the number of true results that have been retrieved.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼

<!-- image-->  
(d)

Fig. 8. (a) The time consumption of querying for three schemes with diverse datasets. (b) The time consumption of querying for three schemes with diverse attributes. (c) The comparison of query precision for diverse schemes with diverse datasets. (d) The comparison of query recall rate for three schemes with diverse datasets.  
<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼

<!-- image-->  
(d)  
Fig. 9. (a) The time consumption of index construction with diverse datasets and attribute numbers. (b) The storage consumption of index construction with diverse datasets and attribute numbers. (c) The time consumption of query token generation with matrix key and attribute numbers. (d) The storage consumption of query token generation with matrix key and attribute numbers.

$$
\mathrm { P r } e c i s i o n = \frac { T P } { T P + F P }
$$

$$
{ \mathrm { R e } } c a l l = { \frac { T P } { T P + F N } }\tag{29}
$$

(30)

Concretely, the experimental results of query precision and recall varying |D| from 5000 to 25000, as well as the sizes of matrix keys and attribute dimensions are fixed to $( 1 6 \times 1 6 )$ - dimensions and $w = 8 ,$ , respectively. We exploit the same query Q to conduct 50 tests on the three schemes, then draw two box plots for query precision and recall in Fig. 8(c) and (d). The indexes of PRQ and Maple are built with R-tree, while that of LSPSS is built with G-tree. Compared to the R-tree, the sibling nodes in the G-tree are not allowed to overlap, thus our LSPSS achieves higher precision and recall than the other two schemes. Also compared with PRQ and Maple, the outliers generated by LSPSS are less than that of the other two schemes during the query, which indicates that our LSPSS has higher query stability.

## B. Self-Performance Evaluation

1) Index Construction: As the design of LSPSS, dataset size, keys size and attribute dimensions all affect the index construction. Fig. 9(a) and (b) describe the time and storage consumption of index construction with diverse datasets and attribute dimensions. We set the size of matrix keys $M _ { 1 }$ , M2 and $M _ { 3 }$ as $( 1 6 \times 1 6 )$ -dimensions. Obviously, the construction time and storage consumption increase linearly with the datasetuthorized licensed use limited to: Nanjing Univ of Post & Telecommunications. Downl size |D| and attribute dimensions w, since our LSPSS encrypts two-kind data features with the matrix encryption methods we proposed. In other words, LSPSS improves query efficiency and security at the expense of time and storage consumption.

2) Token Generation: The dominant factors in query token generation are the size of matrix keys and attribute dimensions, thus we plot the time and storage consumption of token generation varying with the above two factors in Fig. 9(c) and (d). As shown in the two figures, we set the attribute dimension $w \in [ 2 , 8 ]$ and three key sizes. Clearly, the generation time and storage consumption increase linearly with the attribute dimensions w and key size. The larger the key is set, the more secure the token is, but the resulting consumption becomes larger, so we should seek a trade-off between security and efficiency.

3) Query: The main factors affecting the query include the size of the dataset and attribute dimensions. Fig. 10(a) demonstrates the time consumption varies with the diverse sizes of the attribute dimensions $w \in \{ 2 , 4 , 6 \}$ and dataset $| D | \in \{ 5 + 0 . 5 , 1 0 + 1 , 1 5 + 1 . 5 , 2 0 + 2 , 2 5 + 2 . 5 \} \times$ $1 0 ^ { 3 }$ , where $\{ 0 . 5 , 1 , 1 . 5 , 2 , 2 . 5 \} \times 1 0 ^ { 3 }$ donates as the number of UAVs in each aerial zone, that is, each UAV generates one location record and collects ten log files. We also fix the size of three matrix keys to (16 Ã 16)-dimensions. From the perspective of attribute dimensions, the time consumption of querying linearly increases with the w in each dataset. As for the dataset size, the location and log files are indexed by the inverted and tree structures, respectively. The location query on the inverted index dominates the consumption when the dimension w â¤ 4 and the dataset |D| â¤ 15 + 1.5, thus the time oaded on December 01,2025 at 09:04:09 UTC from IEEE Xplore. Restrictions apply.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 10. (a) The time consumption of querying with diverse datasets and attribute numbers. (b) The time consumption of result verification with diverse datasets and attribute numbers.

consumption shows a linear growth. However, the data query on the tree index dominates the consumption when the $w > 4$ and $| D | > 1 5 + 1 . 5 .$ , so the time consumption shows a sub-linear growth and continues.

4) Result Verification: Similarly, the time consumption of result verification is affected by the size of the dataset and attribute dimensions. Fig. 10(b) shows the time consumption varies with the diverse sizes of the attribute dimensions $w \in \{ 2 , 4 , 6 \}$ and dataset $| D | \in \{ 5 , 1 0 , 1 5 , 2 0 , 2 5 \} \times 1 0 ^ { 3 }$ , as well as the size of matrix keys is fixed to $( 1 6 \times 1 6 )$ -dimensions. Evidently, the time consumption increases linearly with the dataset size |D|. Note that the variation in dataset size has a greater effect on the verification consumption when the attribute dimension w is larger.

## IX. CONCLUSION

In this article, we have proposed a lightweight and secure private data storage and sharing scheme to support MRQ and query result verification over encrypted data in the LAC platform of aerial computing. The security of our approach is proven under exactly-defined leakages. We first design two conversion methods to process two kinds of multi-dimensional data. Based on this, we build a secure data index and a DAS with G-tree which enables efficient ciphertext retrieval and query result verification. Practically, via experiments on real-world datasets, we show that our approach is practical for a large-scale dataset and can achieve up to 900Ã and 2Ã query time improvement compared to the prior arts [17], [28], respectively.

In our future work, we consider further enhancing the security of the solution. This will include hiding the access pattern and search pattern during the query, as well as reducing the time and storage consumption required for result verification.

## REFERENCES

[1] W. Li, Z. Su, R. Li, K. Zhang, and Y. Wang, âBlockchain-based data security for artificial intelligence applications in 6G networks,â IEEE Netw., vol. 34, no. 6, pp. 31â37, Nov./Dec. 2020.

[2] W. Sun, L. Wang, P. Wang, and Y. Zhang, âCollaborative blockchain for space-air-ground integrated networks,â IEEE Wireless Commun., vol. 27, no. 6, pp. 82â89, Dec. 2020.

[3] K. Lei, Q. Zhang, J. Lou, B. Bai, and K. Xu, âSecuring ICN-based UAV ad hoc networks with blockchain,â IEEE Commun. Mag., vol. 57, no. 6, pp. 26â32, Jun. 2019.

[4] T. Liu, H. Guo, C. Danilov, and K. Nahrstedt, âA privacy-preserving data collection and processing framework for third-party UAV services,â in Proc. IEEE 19th Int. Conf. Trust Secur. Privacy Comput. Commun., 2020, pp. 683â690.

[5] Y. Tian, J. Yuan, and H. Song, âEfficient privacy-preserving authentication framework for edge-assisted internet of drones,â J. Inf. Secur. Appl., vol. 48, 2019, Art. no. 102354.

[6] Y. Wang, Z. Su, N. Zhang, and A. Benslimane, âLearning in the air: Secure federated learning for UAV-assisted crowdsensing,â IEEE Trans. Netw. Sci. Eng., vol. 8, no. 2, pp. 1055â1069, Second Quarter, 2021.

[7] Y. Lu et al., âPrivacy-preserving logarithmic-time search on encrypted data in cloud,â in Proc. Netw. Distrib. Syst. Secur. Symp., 2012.

[8] A. Boldyreva, N. Chenette, Y. Lee, and A. Oâneillâ âOrder-preserving symmetric encryption,â in Proc. 28th Annu. Int. Conf. Theory Appl. Cryptographic Techn., Springer, 2009, pp. 224â241.

[9] A. Boldyreva, N. Chenette, and A. OâNeill, âOrder-preserving encryption revisited: Improved security analysis and alternative solutions,â in Proc. 31st Annu. Cryptol. Conf., Springer, 2011, pp. 578â595.

[10] L. Xiao and I.-L. Yen, âA note for the ideal order-preserving encryption object and generalized order-preserving encryption,â Cryptol. ePrint Arch., Paper 2012/350, 2012. [Online]. Available: https://eprint.iacr.org/2012/ 350

[11] H. HacigÃ¼mÃ¼Â¸s, B. Iyer, C. Li, and S. Mehrotra, âExecuting SQL over encrypted data in the database-service-provider model,â in Proc. ACM SIGMOD Int. Conf. Manage. Data, 2002, pp. 216â227.

[12] B. Hore, S. Mehrotra, M. Canim, and M. Kantarcioglu, âSecure multidimensional range queries over outsourced data,â VLDB J., vol. 21, pp. 333â358, 2012.

[13] Y. Lee, âSecure ordered bucketization,â IEEE Trans. Dependable Secure Comput., vol. 11, no. 3, pp. 292â303, May/Jun. 2014.

[14] H. G. Do and W. K. Ng, âMultidimensional range query on outsourced database with strong privacy guarantee,â in Proc. 14th Annu. Conf. Privacy Secur. Trust, 2016, pp. 555â560.

[15] E. Shi, J. Bethencourt, T. H. Chan, D. Song, and A. Perrig, âMultidimensional range query over encrypted data,â in Proc. IEEE Symp. Secur. Privacy, 2007, pp. 350â364.

[16] D. Boneh and B. Waters, âConjunctive, subset, and range queries on encrypted data,â in Proc. 4th Theory Cryptogr. Conf., Springer, 2007, pp. 535â554.

[17] B. Wang, Y. Hou, M. Li, H. Wang, and H. Li, âMaple: Scalable multidimensional range search over encrypted cloud data with tree-based index,â in Proc. 9th ACM Symp. Inf. Comput. Commun. Secur., 2014, pp. 111â122.

[18] R. Xu, K. Morozov, Y. Yang, J. Zhou, and T. Takagi, âPrivacy-preserving knearest neighbour query on outsourced database,â in Proc. 21st Australas. Conf. Inf. Secur. Privacy, Springer, 2016, pp. 181â197.

[19] Y. Zheng and R. Lu, âAn efficient and privacy-preserving k-NN query scheme for ehealthcare data,â in Proc. IEEE Int. Conf. Internet Things IEEE Green Comput. Commun. IEEE Cyber Phys. Social Comput. Smart Data, 2018, pp. 358â365.

[20] Z. Xu, Y. Lin, V. K. A. Sandor, Z. Huang, and X. Liu, âA lightweight privacy and integrity preserving range query scheme for mobile cloud computing,â Comput. Secur., vol. 84, pp. 318â333, 2019.

[21] Y. Zheng, R. Lu, Y. Guan, J. Shao, and H. Zhu, âEfficient and privacypreserving similarity range query over encrypted time series data,â IEEE Trans. Dependable Secure Comput., vol. 19, no. 4, pp. 2501â2516, Jul./Aug. 2022.

[22] Y. Guo, H. Xie, M. Wang, and X. Jia, âPrivacy-preserving multi-range queries for secure data outsourcing services,â IEEE Trans. Cloud Comput., vol. 11, no. 3, pp. 2431â2444, Third Quarter 2023.

[23] Y. Yang, S. Papadopoulos, D. Papadias, and G. Kollios, âAuthenticated indexing for outsourced spatial databases,â VLDB J., vol. 18, pp. 631â648, 2009.

[24] P. Wang and C. V. Ravishankar, âSecure and efficient range queries on outsourced databases using Rp-trees,â in Proc. IEEE 29th Int. Conf. Data Eng., 2013, pp. 314â325.

[25] J. Chi, C. Hong, M. Zhang, and Z. Zhang, âFast multi-dimensional range queries on encrypted cloud databases,â in Proc. 22nd Int. Conf. Database Syst. Adv. Appl., Springer, 2017, pp. 559â575.

[26] B. Wang, M. Li, and H. Wang, âGeometric range search on encrypted spatial data,â IEEE Trans. Inf. Forensics Secur., vol. 11, no. 4, pp. 704â719, Apr. 2016.

[27] W. Yang, Y. Geng, L. Li, X. Xie, and L. Huang, âAchieving secure and dynamic range queries over encrypted cloud data,â IEEE Trans. Knowl. Data Eng., vol. 34, no. 1, pp. 107â121, Jan. 2022.

[28] Y. Zheng, R. Lu, Y. Guan, J. Shao, and H. Zhu, âTowards practical and privacy-preserving multi-dimensional range query over cloud,â IEEE Trans. Dependable Secure Comput., vol. 19, no. 5, pp. 3478â3493, Sep./Oct. 2022.

[29] Y. Zheng et al., âPMRQ: Achieving efficient and privacy-preserving multidimensional range query in eHealthcare,â IEEE Internet Things J., vol. 9, no. 18, pp. 17 468â17 479, Sep. 2022.

[30] S. Wu, Q. Li, G. Li, D. Yuan, X. Yuan, and C. Wang, âServeDB: Secure, verifiable, and efficient range queries on outsourced database,â in Proc. IEEE 35th Int. Conf. Data Eng., 2019, pp. 626â637.

[31] L. Chen, N. Zhang, H.-M. Sun, C.-C. Chang, S. Yu, and K.-K. R. Choo, âSecure search for encrypted personal health records from big data NoSQL databases in cloud,â Computing, vol. 102, pp. 1521â1545, 2020.

[32] Z. Mei et al., âExecuting multi-dimensional range query efficiently and flexibly over outsourced ciphertexts in the cloud,â Inf. Sci., vol. 432, pp. 79â96, 2018.

[33] Y. Zhan, D. Shen, P. Duan, B. Zhang, Z. Hong, and B. Wang, âMDOPE: Efficient multi-dimensional data order preserving encryption scheme,â Inf. Sci., vol. 595, pp. 334â343, 2022.

[34] A. Kumar, âG-Tree: A new data structure for organizing multidimensional data,â IEEE Trans. Knowl. Data Eng., vol. 6, no. 2, pp. 341â347, Apr. 1994.

[35] R. C. Merkle, âA digital signature based on a conventional encryption function,â in Proc. Conf. Theory Appl. Cryptographic Techn., Berlin, Germany: Springer-Verlag, 1987, pp. 369â378.

[36] W. K. Wong, D. W.-L. Cheung, B. Kao, and N. Mamoulis, âSecure kNN computation on encrypted databases,â in Proc. ACM SIGMOD Int. Conf. Manage. Data, 2009, pp. 139â152.

<!-- image-->

<!-- image-->

<!-- image-->  
Haoyang Wang received the BS degree in software engineering from Northeastern University, Shenyang, China, in 2018, and the masterâs degree in computer technology from Xidian University, in 2021. He is currently working toward the PhD degree with the State Key Laboratory of Integrated Service Networks, Xidian University. His research interests include data privacy-preserving, searchable encryption, and Internet of Vehicles Security.

Fenghua Li (Member, IEEE) received the PhD degree from Xidian University. He is now a professor with the Chinese Academy of Sciences and Xiâan University, Xiâan China. His research interests include cyber and system security, information protection, and data security.

Hui Li (Member, IEEE) received the BS degree in radio electronics from Fudan University, and the MS and PhD degrees in telecommunications and information system from Xidian University, in 1993 and 1998, respectively. He is now a professor with Xidian University. His research interests include network and information security.

<!-- image-->

Kai Fan (Member, IEEE) received the BS, MS, and PhD degrees from Xidian University, P. R. China, in 2002, 2005, and 2007, respectively, in telecommunication engineering, cryptography and telecommunication and information system. He is working as a professor with the State Key Laboratory of Integrated Service Networks, Xidian University. He published more than 70 papers in journals and conferences. He received nine Chinese patents. He has managed five national research projects. His research interests include IoT security and information security.

<!-- image-->

Yintang Yang (Senior Member, IEEE) received the PhD degree in semiconductor from Xidian University. He is now a professor with the Key Laboratory of Ministry of Education for Wide Band-Gap Semiconductor Materials and Devices, Xidian University, Xiâan China. His research interests include semiconductor materials and devices, network and information security.

<!-- image-->

Chong Yu (Graduate Student Member, IEEE) received the BSc degree in communication engineering and the MSc degree in communication and information system from Northeastern University, Shenyang, China, in 2015 and 2017, respectively. She is currently working toward the PhD degree with the Department of Electrical and Computer Engineering, University of Nebraska-Lincoln, USA, in 2023. She is currently with the Department of Computer Science, University of Cincinnati, OH, USA. Her research interests include artificial intelligence (AI), machine learning,

<!-- image-->

Haojin Zhu (Fellow, IEEE) received the BSc degree from Wuhan University, China, in 2002, the MSc degree from Shanghai Jiao Tong University, China, in 2005, both in computer science, and the PhD degree in electrical and computer engineering from the University of Waterloo, Canada, in 2009. He is currently a professor with Computer Science Department, Shanghai Jiao Tong University. His current research interests include network security and privacy enhancing technologies. He published more than 70 international journal papers, including IEEE Journal

and cybersecurity with a broad range of applications including data analytics, edge-based AI, and Internet of Things.

<!-- image-->

Kuan Zhang (Member, IEEE) received the BS and MS degrees from Northeastern University, Shenyang, China, in 2009 and 2011, respectively, in communication engineering and computer applied technology, and the PhD degree from the University of Waterloo, Canada, in 2016, in electrical and computer engineering. He was a postdoctoral fellow from 2016â2017 with the University of Waterloo, Canada. He is working as an Assistant Professor with the Department of Electrical and Computer Engineering, University of NebraskaâLincoln, USA. He has published more than 50 papers in journals and conferences. He was the recipient of Best Paper Award in IEEE WCNC 2013 and Securecomm 2016. His research interests include cyber security, Big Data, and cloud/edge computing.

on Selected Areas in Communications, IEEE Transactions on Dependable and Secure Computing, IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Mobile Computing, IEEE Transactions on Information Forensics and Security, and 90 international conference papers, including IEEE S&P, ACM CCS, USENIX Security, NDSS, ACM MOBICOM. He received a number of awards including: ACM CCS Best Paper Runner-Ups Award (2021), IEEE TCSC Award for Excellence in Scalable Computing (Middle Career Researcher, 2020), IEEE ComSoc Asia-Pacific Outstanding Young Researcher Award (2014), Top 100 Most Cited Chinese Papers Published in International Journals (2014), distinguished member of the IEEE INFOCOM Technical Program Committee (2015, 2020), best paper awards of IEEE ICC (2007) and Chinacom (2008), WASA Best Paper Runner-up Award (2017). He is serving the editorial board of IEEE Transactions on Wireless Communications and program committees for top conferences such as USENIX Security, ACM CCS, NDSS, and IEEE INFOCOM.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_2_img_1.png|page_2_img_1]]
2. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_4_img_1.jpeg|page_4_img_1]]
3. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_6_img_1.jpeg|page_6_img_1]]
4. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_7_img_1.jpeg|page_7_img_1]]
5. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_14_img_1.jpeg|page_14_img_1]]
6. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_14_img_2.jpeg|page_14_img_2]]
7. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_14_img_3.jpeg|page_14_img_3]]
8. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_14_img_4.jpeg|page_14_img_4]]
9. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_14_img_5.jpeg|page_14_img_5]]
10. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_14_img_6.jpeg|page_14_img_6]]
11. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_14_img_7.jpeg|page_14_img_7]]
12. [[../extracted_images/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing/page_14_img_8.jpeg|page_14_img_8]]

---

