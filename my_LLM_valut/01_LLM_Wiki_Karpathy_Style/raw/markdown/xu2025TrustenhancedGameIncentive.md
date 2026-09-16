# Trust-Enhanced Game Incentive for Secure Quantum Federated Learning in UAV-Assisted Wireless Networks

Qichao Xu , Ruidong Li , Senior Member, IEEE, Yihao Qi, Zhou Su , Senior Member, IEEE, and Dongfeng Fang , Member, IEEE

AbstractâRecently, quantum federated learning (QFL) is advocated to leverage the robust computing power of quantum edge computing devices (QECDs) within unmanned aerial vehicle (UAV)-assisted wireless networks, to enhance the efficiency of distributed learning. However, the presence of malicious and selfish behaviors among some QECDs poses significant challenges for QFL model training to achieve high accuracy and rapid convergence. To tackle this issue, we introduce a trustenhanced incentive scheme for QFL in the UAV-assisted wireless networks. Specifically, a QECD-empowered QFL framework is first presented in the UAV-assisted wireless networks, where the QECDs independently train local models with their private data by using the quantum computing capabilities, while UAVs aggregate these trained local models to update the global model. Then, to ensure security and eliminate malicious participants, we devise a Bayesian inference-based trust assessment mechanism to select honest QECDs for local model training. Furthermore, we design a Stackelberg game-based incentive mechanism to incentivize QECDs to cooperatively provide high-quality training services. Afterwards, through game analysis using the backward induction method, we prove the existence of a Stackelberg equilibrium. The optimal payment strategies of the UAVs are obtained using the deep Q-learning network (DQN) algorithm in dynamic networks, and the optimal training contribution strategy of each QECD is derived using the convex optimization method. Finally, extensive simulations demonstrate that the proposed scheme can significantly enhance the accuracy and training speed of QFL in UAV-assisted wireless networks.

Index TermsâUAV-assisted wireless networks (UAWNs), quantum federated learning (QFL), trust assessment, game-based incentive.

## I. INTRODUCTION

D UE to considerable advantages including easy deploy-ment, flexibility, high speed, and maneuverability, unmanned aerial vehicles (UAVs) have been advocated to provide temporary communication and computing services, so as to form UAV-assisted wireless networks [1], [2]. Especially, with the fast advancement of quantum computing, the quantum edge computing devices (QECDs) can be integrated into these networks to provision powerful quantum computing capabilities, significantly enhancing data processing and computational efficiency [3], [4], [5]. With advancements in addressing hardware limitations [6], such as limited qubit counts and high susceptibility to environmental noise, QECDs offer significant advantages in UAV-assisted wireless networks. They enable the accelerated execution of complex tasks, such as resource allocation and routing, through quantum speedup, facilitating adaptive decision-making in near real-time, even in highly dynamic network environments [7]. Given these advantages, QECDs have gradually found applications in real-world scenarios, including generative artificial intelligence (AI) and smart healthcare. For instance, in generative AI, quantumassisted generative adversarial networks have been employed to accelerate training and enhance synthetic data generation [8]. In smart healthcare, quantum-enhanced optimization is being utilized in drug discovery, while quantum machine learning is enabling faster and more accurate early disease detection [9], [10]. Here, in order to achieve the high-quality intelligent services provided by QECDs, a large volume of data should be required to train the corresponding AI models. However, due to data scarcity and privacy concerns, the data available for training these AI models is often insufficient, which hampers the intelligent functions of UAV-assisted wireless networks [11].

Quantum federated learning (QFL) [12], [13] integrating quantum computing and federated learning (FL) has been advocated to address data insufficiency and privacy issues by leveraging the distributed quantum learning capabilities of QECDs in UAV-assisted networks [14]. QFL not only enhances the efficiency of model training but also preserves data privacy. On one hand, during QFL, QECDs cooperatively train AI models using their own data through quantum computing, significantly increasing AI model accuracy and convergence speed [15]. On the other hand, QFL allows QECDs to independently train local models with their private data without exchanging raw data, thereby ensuring data privacy [16]. Apparently, the deployment of QFL in UAV-assisted wireless networks can revolutionize various applications, from autonomous vehicle navigation to smart city infrastructure, by providing highly accurate, real-time insights derived from aggregated data models.

Nevertheless, the full implementation of QFL in UAVassisted wireless networks faces several challenges due to the potentially malicious and inherently selfish behavior of QECDs. First, malicious QECDs can exploit quantum-specific vulnerabilities, such as entanglement corruption, quantum data poisoning, or the introduction of fake datasets during QFL model training, which can lead to low accuracy or even failure of the FL models [17]. Second, some QECDs are honest but may intentionally use low-quality datasets for model training to gain potential benefits, further diminishing the quality of the trained FL models [18]. Third, due to the limited availability of quantum resources, where QECDs require specialized hardware and precise control mechanisms to maintain and manipulate qubits, these devices may exhibit selfish behaviors, hesitating to participate in the training process without adequate compensation. This reluctance can result in insufficient data contributions for the QFL model [19]. Fourth, the inherent fragility of quantum states causes variability in the stability of QECDs, which can negatively impact the quality of QFL models and, in some cases, even disrupt the training process entirely. Therefore, it is urgent to ensure the security and cooperation among QECDs to achieve high-quality QFL in UAV-assisted wireless networks.

Recently, some existing works have attempted to enhance the security and cooperation of QFL in wireless networks. For example, trust-based QFL mechanisms have been utilized to ensure the quality of model training by evaluating the trustworthiness of participating devices [20], [21]. Additionally, game-based incentive mechanisms have been explored to encourage participation by providing appropriate payments [22]. However, most of these works fall short in providing sufficient security and incentives for QFL in UAVassisted networks. The existing trust assessment methods may not accurately evaluate the trustworthiness of QECDs, as they primarily rely on direct interaction data without considering the interaction information of others, making it difficult to fully eliminate malicious QECDs [23], [24]. Furthermore, due to the dynamic nature of UAV-assisted networks, UAVs struggle to obtain knowledge of each QECDâs parameters, preventing them from making optimal decisions to incentivize QECDs for FL model training [25]. Therefore, designing a secure and incentive-based QFL scheme in UAV-assisted wireless networks remains an open and vital issue [26].

In this paper, we propose a novel trust-enhanced incentive scheme for QFL in UAV-assisted wireless networks. Specifically, we first develop a QECD-empowered QFL framework, where QECDs conduct local model training with private data by using the powerful quantum computing capacities, and the UAV then aggregates the trained local model parameters to update the global model. Afterwards, we devise a Bayesian inference-based trust assessment mechanism, involving direct evaluation and mutual recommendation, to select honest QECDs for providing high-quality quantum local model training services. Additionally, we design a Stackelberg game-based incentive mechanism to motivate QECDs to cooperatively participate in local model training. The existence of the Stackelberg equilibrium is proven by game analysis with the backward induction method. Optimal decisions on training contribution by each QECD are obtained using convex optimization methods, and the optimal payment decisions are achieved through deep Qlearning (DQN) algorithm in the dynamic network without prior knowledge of the QECDs. Finally, extensive simulations are conducted to validate the efficiency of the proposed scheme. The following are the contributions of this paper:

â¢ Framework. We develop a novel QECD-assisted QFL framework for UAV-assisted wireless networks. Each UAV can quickly generate a temporary AI model with the cooperation of QECDs. Within this framework, local model training can be rapidly completed by the QECDs using their powerful quantum capabilities. The UAVs then aggregate the trained model parameters obtained from the proximal QECDs via high-speed communication links to update the global model.

â¢ Mechanism. We devise a Bayesian inference-based trust assessment mechanism to select honest QECDs for providing high-quality quantum local model training services. This mechanism involves both direct evaluation and mutual recommendation among QECDs, creating a dynamic and adaptive trust evaluation process. By ensuring the selection of reliable participants, this mechanism enhances the security and integrity of the QFL process.

â¢ Strategy. We design a Stackelberg game-based incentive strategy to motivate QECDs to participate in local model training. By proving the existence of a Stackelberg equilibrium and employing convex optimization and DQN for optimal decision-making, the strategy effectively enhances the utilities of both UAVs and QECDs, thereby further increasing the performance of the QFL model.

The remainder of the paper is organized as follows. In Section II, related works are reviewed. The system model is introduced in Section III. Subsequently, we present the Bayesian inference-based trust assessment mechanism in Section IV. The game-based incentive strategy is analyzed in Section V. The performance evaluation is carried out in Section VI, and the paper concludes in Section VII.

## II. RELATED WORK

In this section, we review the related works including FL in UAV-assisted wireless networks, QFL in wireless communication networks, and game-based incentive for FL.

## A. FL in UAV-Assisted Wireless Networks

The emerging FL in UAV-assisted wireless networks presents a powerful solution to enhance data privacy, efficiency, and sustainability. Yang et al. introduced a UAVassisted FL framework that enhances training accuracy and efficiency by optimizing user selection and resource management, and executing FL asynchronously. Fu et al. [27] proposed a UAV-enabled FL framework that optimizes device scheduling, time allocation, and UAV trajectory through a unified optimization framework, significantly reducing completion time and enhancing communication efficiency. Xu et al. [28] investigated a personalized federated deep reinforcement learning approach aimed at optimizing UAV location and resource management with a two-level parameter aggregation scheme to form a robust global model. To address the impact of non-independent identically distributed data in heterogeneous UAVs, He et al. [29] designed a clustered FL architecture enabled by a three-stage Stackelberg game for heterogeneous UAV swarms, optimizing resource allocation and improving training efficiency through a hierarchical reinforcement learning algorithm.

The aforementioned researches primarily focus on optimizing network resources to enhance the efficiency of FL training. However, due to the inherent computing resource limitations of devices, the efficiency of FL model training remains constrained in UAV-assisted wireless networks.

## B. QFL in Wireless Communication Networks

To address the computational bottlenecks for FL, QFL has been proposed in wireless communication networks. Huang et al. [30] proposed a communication-efficient QFL approach using decentralized data. This method extends the conventional variational quantum algorithm (VQA) to improve data privacy by aggregating updates from local computations to share model parameters. Yamany et al. [31] introduced an optimized QFL framework (OQFL) to protect intelligent transportation systems against adversarial attacks. They utilized particle swarm optimization with quantum behavior to adjust hyperparameters, enhancing the resilience of FL models against adversarial attacks. Park et al. [32] proposed a dynamic QFL framework for satellite-ground communication systems using slimmable quantum neural networks, optimizing computational and communication efficiency and demonstrating superior performance over classical FL and standard QFL under low signal-to-noise ratios and non-identically distributed data distributions. Wang et al. [10] introduced a QFL framework for space-air-ground integrated networks (SAGIN), utilizing VQA and quantum relays to address issues concerning large datasets, complex machine learning models, and the secure transmission of models.

However, these studies overlook a critical issue: the selfishness and untrustworthy nature of quantum devices. These devices may upload false information or underperform, necessitating the implementation of reputation evaluation and incentive mechanisms.

## C. Game-Based Incentive for FL

FL preserves data privacy but faces challenges in encouraging participants to provide their computational resources and data. Zhan et al. [33] proposed a framework combining deep reinforcement learning and game-theoretic incentive mechanisms to optimize payment and training strategies in FL, effectively addressing challenges of information non-sharing and contribution evaluation. Kang et al. [34] developed a scheme that uses reputation and contract theory to incentivize high-quality, reputable mobile devices to participate in FL. Xu et al. [35] introduced a differential privacy gamebased incentive mechanism using Stackelberg games to enable clients to adjust their privacy budgets flexibly while participating in FL, ensuring privacy and utility optimization. Ding et al. [36] analyzed optimal incentive mechanisms with a multi-dimensional contract-theoretic approach, focusing on how varying levels of information asymmetry affect server strategies.

However, most of the related work often assumes that the cooperating QECDs are honest, stable, and capable of providing high-quality local training services, while also possessing complete knowledge of each otherâs capabilities. In reality, some QECDs may be malicious, have varying levels of training quality, and be part of a dynamic network where device information frequently changes. In this paper, we propose a Bayesian inference-based trust assessment mechanism to effectively address the untrustworthy nature of QECDs. Additionally, we introduce a Stackelberg game-based incentive mechanism, combined with DQN, to encourage QECDs to collaborate in local FL model training within the dynamic UAV-assisted wireless networks.

## III. SYSTEM MODEL

In this section, we first introduce the basis of quantum computing. Then, we describe the system model, including the network model, communication model, QFL framework, threat model, and the overview of the proposed scheme.

## A. Quantum Computing Basis

Quantum computing [37], [38] is a form of computation that utilizes quantum-mechanical operations, including superposition and entanglement, to process information. There are two critical components in quantum computing: qubits and quantum gates. A qubit is the fundamental unit of quantum information. In contrast to classical bits, which can only be in a state of either 0 or 1, a qubit can exist in a superposition, meaning it can represent both states at the same time. A quantum device with $Q _ { u }$ qubits has a total of $2 ^ { Q _ { \imath } }$ u basis states. The j-th basis state can be represented by $| \mathbf { b } \rangle _ { j } ^ { ( Q _ { u } ) } =$ $\left| b _ { Q _ { u - 1 } } b _ { Q _ { u - 2 } } \ldots \ldots b _ { 1 } b _ { 0 } \right.$ , where $b _ { i } , \forall i \in \{ 0 , 1 , \cdot \cdot \cdot Q _ { u - 1 } \}$ are either 0 or 1. |Â·i is used to denote a quantum state vector. For example, in a 2-qubit quantum device, the basis states are |00i, |01i, |10i, and |11i. As such, for this device, any quantum state can be a superposition of the above four basis states. This property enables quantum computers to perform certain computations exponentially faster.

Quantum gates manipulate qubits through unitary transformations and are the quantum analogs of classical logic gates. Common qubit gates include one-qubit gates, two-qubit gates, and measurement gates. One-qubit gates, such as the Pauli-X gate [39], [40], act on a single qubit to change its state. Twoqubit gates, such as the controlled-NOT (CNOT) gate, act on pairs of qubits to create entanglement. Measurement gates are used to observe the state of qubits and extract classical information. When a qubit is measured, its superposition collapses to one of the basis states, either |0i or |1i, with probabilities determined by its quantum state. Quantum gates manipulate data on qubits according to the algorithm implemented by the quantum circuit. Quantum circuits exploit the principles of superposition and entanglement to perform parallel computations and achieve potential speedups for specific tasks.

<!-- image-->  
Fig. 1. QFL in UAV-assisted wireless network.

Quantum computing can manage between a few dozen and several hundred qubits. However, its results are often unstable and inaccurate due to environmental noise and hardware imperfections. Quantum error correction has been introduced to address this issue, which can enhance the computational reliability and accuracy by incorporating quantum error-correcting codes (e.g., Shor code [41], surface codes) to detect and correct errors [41].

## B. Network Model

As shown in Fig. 1, we consider a UAV-assisted wireless network that consists of multiple UAVs and a number of QECDs.

1) UAVs: Considering the advantages of UAVs, such as ease of deployment, flexibility, and scalability, they hold great potential in dynamically providing intelligent services. Let $\mathcal { M } = \{ 1 , 2 , \dots , M \}$ denote the set of UAVs in the network. Due to the poor communication condition between ground nodes and base stationsâcaused, for instance, by congestion during large sports events or lack of coverage in remote areasâUAVs can serve as temporary alternatives to provide wireless coverage for ground devices. Here, different UAVs have different coverage areas. The coverage area of UAV m is a circle with a radius of $R _ { m }$

2) Quantum Edge Computing Devices: QECDs are deployed on the ground, which are proximal to the users. Let $\mathcal { N } = \{ 1 , 2 , \dots , N \}$ denote the set of QECDs in the network. Each QECD can collect usersâ data for model training. The dataset of QECD n is expressed as $\mathcal { D } _ { n } .$ , where the size of dataset is $D _ { n } = | \mathcal { D } _ { n } |$ . In addition, each QECD has a certain quantum computing capability, which is equipped with a quantum processing unit (QPU). The largest quantum computing capacity of QECD n is denoted as $Q _ { n } ,$ which is the qubits owned by QECD n.

## C. Communication Model

We first use the 3D-Cartesian coordinate system to show the locations of both UAVs and QECDs. A finite time horizon is divided into T time slots with the equal length Ï , whereby the set of time slots can be expressed as $\mathcal { T } = \{ 1 , 2 , \hdots , T \}$ At time slot t, the location of UAV m is denoted as $\mathbf { l } _ { m } ( t ) =$ $( x _ { m } ( t ) , y _ { m } ( t ) , H _ { m } )$ . Altitude $H _ { m }$ of UAV m during time slot t remains unchanged to minimize frequent altitude adjustments. Owing to the sufficiently short duration Ï , the location of each UAV can be approximated as stationary within the time slot interval. As such, the flying trajectory of UAV m can be expressed as $l _ { m } = ( l _ { m } ( 1 ) , l _ { m } ( 2 ) , \cdot \cdot \cdot , l _ { m } ( T ) )$ , where $| | l _ { m } ( t ) - l _ { m } ( t - 1 ) | | \leq V _ { m a x } \tau . \ V _ { m a x }$ is the maximum flying velocity of UAVs. Meanwhile, the location of QECD n is denoted as $\mathbf { l } _ { n } = ( x _ { n } , y _ { n } , 0 )$ , where the altitude of QECD n is 0. Here, let $\mu _ { m , n } ( t ) \in \{ 0 , 1 \}$ denote whether QECD n locates within the coverage area of UAV m at time slot t. It is obtained by

$$
\mu _ { m , n } ( t ) = \left\{ \begin{array} { r l } & { 1 , \mathrm { i f } \sqrt { \left( x _ { m } ( t ) - x _ { n } \right) ^ { 2 } + \left( y _ { m } ( t ) - y _ { n } \right) ^ { 2 } } \leq R _ { m } , } \\ & { 0 , \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{1}
$$

Considering the obstruction by obstacles, such as high buildings and trees, both line of sight (LoS) and non-line of sight (NLoS) channels are used to model the wireless connections between UAVs and QECDs. The path loss between UAV m and QECD n through the LoS channel and the NLoS channel at time slot t is respectively given by

$$
L _ { m , n } ^ { \mathrm { L o S } } ( t ) = 2 0 \log \hat { f } + 2 0 \log \frac { 4 \pi } { c } + 2 0 \log d _ { m , n } ( t ) + \eta ^ { \mathrm { L o S } } ,\tag{2}
$$

$$
{ \cal L } _ { m , n } ^ { \mathrm { N L o S } } ( t ) = 2 0 \log \hat { f } + 2 0 \log \frac { 4 \pi } { c } + 2 0 \log d _ { m , n } ( t ) + \eta ^ { \mathrm { N L o s } } ,\tag{3}
$$

where $\hat { f }$ is the carrier frequency and c is the speed of light. $d _ { m , n } ( t )$ is the Euclidean distance between UAV m and QECD n, which is expressed by

$$
d _ { m , n } ( t ) = \sqrt { ( x _ { m } ( t ) - x _ { n } ( t ) ) ^ { 2 } + ( y _ { m } ( t ) - y _ { n } ( t ) ) ^ { 2 } + { H _ { m } } ^ { 2 } } .\tag{4}
$$

$\eta ^ { \mathrm { L o s } }$ and $\eta ^ { \mathrm { N L o s } }$ are the attenuation factors for the LoS and NLoS channels, respectively.

The probability of the LoS channel between UAV m and QECD n is

$$
\mathrm { P r } _ { m , n } ^ { \mathrm { L o S } } ( t ) = \frac { 1 } { \hat { a } + \hat { a } e ^ { - \hat { b } ( \phi _ { m , n } ( t ) - \hat { a } ) } } ,\tag{5}
$$

where aË and $\hat { b }$ are environmental constants. $\begin{array} { r l } { \phi _ { m , n } ( t ) } & { { } = } \end{array}$ arcsin $\frac { H _ { m } } { d _ { m , n } ( t ) }$ is the elevation angle between UAV m and QECD n at time slot t. As such, the average path loss between UAV m and QECD n at time slot t can be obtained by

$$
L _ { m , n } ( t ) = \mathrm { P r } _ { m , n } ^ { \mathrm { L o S } } ( t ) \times L _ { m , n } ^ { \mathrm { L o S } } ( t ) + ( 1 - \mathrm { P r } ^ { \mathrm { L o S } } ( t ) ) \times L _ { m , n } ^ { \mathrm { L o S } } ( t ) .\tag{6}
$$

Here, the orthogonal frequency division multiple access (OFDMA) technology is utilized for QECDs to connect UAVs. Then, the signal-to-interference-plus-noise-ratio (SINR) received by UAV m from associated QECD n (i.e., $\mu _ { m , n } ( t ) = 1 )$ at time slot t is given by

$$
\widetilde { \gamma } _ { m , n } ^ { \mathrm { G 2 A } } ( t )
$$

$$
= \frac { \mu _ { m , n } ( t ) P _ { n } ( t ) 1 0 ^ { - L _ { m , n } ( t ) / 1 0 } } { \sigma ^ { 2 } + \sum _ { n ^ { \prime } \in \mathcal { N } \backslash \{ n \} } \left( 1 - \mu _ { m , n } ( t ) \right) \varsigma _ { n , n ^ { \prime } } P _ { n ^ { \prime } } ( t ) 1 0 ^ { - L _ { m , n ^ { \prime } } ( t ) / 1 0 } } ,\tag{7}
$$

where $P _ { n } ( t )$ is the transmission power of QECD n at time slot t. $\sigma ^ { 2 }$ is the power of white Gaussian noise. $\begin{array} { r } { \sum _ { n ^ { \prime } \in \mathcal { N } \backslash \{ n \} } ( 1 - } \end{array}$ $\mu _ { m , n } ( t ) ) \varsigma _ { n , n ^ { \prime } } P _ { n ^ { \prime } } ( t )$ is the interference received by UAV m from QECDs within the coverage area of other UAVs and sharing the wireless spectrum with QECD n. $\varsigma _ { n , n ^ { \prime } }$ denotes whether QECD n and QECD $n ^ { \prime }$ occupy the same wireless spectrum to communicate with associated UAVs. As such, according to Shannon theory, the data rate of uplink between UAV m and QECD n at time slot t is expressed as

$$
R _ { m , n } ^ { \mathrm { G 2 A } } ( t ) = \frac { \mu _ { m , n } ( t ) ( t ) B _ { n } ^ { \mathrm { G 2 A } } } { \sum _ { n = 1 } ^ { N } \mu _ { m , n } ( t ) } \log _ { 2 } ( 1 + \mathfrak { T } _ { m , n } ^ { \mathrm { G 2 A } } ( t ) ) ,\tag{8}
$$

where $B _ { m } ^ { \mathrm { G 2 A } }$ is the total bandwidth of uplink channel owned by UAV m.

Unlike QECDs orthogonally accessing associated UAVs, each UAV can utilize the same wireless spectrum to serve the QECDs within its coverage area. As such, UAVs exploit the A2G multicast transmission technology to deliver data to QECDs. At time slot t, the SINR received by QECD n from its associated UAV m is

$$
\widetilde { \gamma } _ { m , n } ^ { \mathrm { A 2 G } } ( t ) = \frac { \mu _ { m , n } ( t ) P _ { m } ( t ) 1 0 ^ { - L _ { m , n } ( t ) / 1 0 } } { \sigma ^ { 2 } + \sum _ { m ^ { \prime } \in \mathcal { M } \backslash \{ m \} } P _ { m ^ { \prime } } ( t ) 1 0 ^ { - L _ { m ^ { \prime } , n } ( t ) / 1 0 } } ,\tag{9}
$$

where $P _ { m } ( t )$ is the transmission power of UAV m at time slot $\begin{array} { r } { t . \sum _ { m ^ { \prime } \in \mathcal { M } \backslash \{ m \} } P _ { m ^ { \prime } } ( t ) 1 0 ^ { - L _ { m ^ { \prime } , n } ( \bar { t } ) / 1 0 } } \end{array}$ is the received interference of QECD n from all UAVs except UAV m. To guarantee successful signal decoding for all QECDs in a UAVâs coverage area, the UAVâs multicast data rate is constrained by the QECD with the poorest channel quality. This ensures compatibility with the most disadvantaged communication link among the covered devices. Thereby, the data rate of downlink between UAV m and its associated QECDs at time slot t is

$$
R _ { m } ^ { \mathrm { A 2 G } } ( t ) = B _ { m } ^ { \mathrm { A 2 G } } \log _ { 2 } ( 1 + \tilde { \gamma } _ { m } ^ { \mathrm { A 2 G } } ( t ) ) ,\tag{10}
$$

where $B _ { m } ^ { \mathrm { A 2 G } }$ is the spectrum bandwidth of multicast channel owned by UAV m. $\widetilde { \gamma } _ { m } ^ { \mathrm { A 2 G } } ( t )$ is the minimum SINR from UAV m to all QECDs within its coverage area at time slot t. It is obtained by

$$
\widetilde { \gamma } _ { m } ^ { \mathrm { A 2 G } } ( t ) = \operatorname* { m i n } _ { \substack { n \in \{ n | \mu _ { m , n } ( t ) = 1 , \forall n \in \mathcal { N } \} } } \widetilde { \gamma } _ { m , n } ^ { \mathrm { A 2 G } } ( t ) .\tag{11}
$$

## D. QECD-Empowered QFL Framework

The QECD-empowered QFL framework integrates QECDs with quantum neural networks (QNNs) to enhance distributed learning processes. Referencing the architecture of traditional neural networks, QNNs are constructed within QECDs using qubits and quantum gates. QNN is a combination of classical computing and quantum computing, forming a hybrid quantum-classical computing framework, which can make full use of the potential of quantum computing and the optimization power of classical computing.

A QNN comprises three components: data encoding, parameterized quantum circuits (PQC), and measurement, corresponding to the input layer, hidden layers, and output layer of classical neural networks, respectively. Data encoding transforms individual classical bits into qubits. The PQC comprises qubits and quantum gates, with some gates having adjustable parameters. These parameters, typically real numbers, can be optimized using classical algorithms to improve the modelâs output or performance. Measurements turn qubits back into classical bits.

1) Data Encoding and Initialization: For QECDempowered QFL, the process begins with the UAV m distributing QFL tasks to associated QECDs, including initial parameters $\theta _ { m } ^ { \mathrm { G l o } }$ QECD n first initializes the adjustable parameters of the quantum perceptrons in PQC $\begin{array} { l l l } { \theta _ { n } } & { = } & { \theta _ { m } ^ { \mathrm { G l o } } } \end{array}$ . And QECD n owns the classical data samples $\mathcal { D } _ { n } = \{ \tilde { \mathbf { x } } _ { n , i } , z _ { n , i } \} _ { i \in \{ 1 , 2 , \cdots , D _ { n } \} }$ , where $D _ { n } = | \mathcal { D } _ { n } |$ is the number of data samples. Each data sample is described by a feature vector ${ \bf x } _ { n , i }$ and corresponding label $z _ { n , i }$

Data encoding converts local classical bits into qubits through quantum rotation gates, since QPU can only process qubits. In this paper, the amplitude coding algorithm is used to convert classical bit data $\tilde { \mathbf { x } } _ { n , i }$ into qubits $\left| { \psi _ { n , i } } \right.$ , which can be expressed as [30]

$$
\left| { \psi _ { n , i } } \right. = \frac { 1 } { { \sqrt { \sum _ { j = 1 } ^ { n _ { i } } { { \tilde { x } } _ { n , i , j } ^ { 2 } } } } \sum _ { j = 1 } ^ { { n _ { i } } } { { \tilde { x } } _ { n , i , j } { \left| { { \bf { b } } } \right. } _ { j } ^ { \left( { Q _ { \mathrm { { L o c } } } } \right) } } } ,\tag{12}
$$

where $\tilde { \mathbf { x } } _ { n , i } = [ \tilde { x } _ { n , i , 1 } , . . . , \tilde { x } _ { n , i , n _ { i } } ]$ is a $n _ { i } .$ -dimensional vector. $| \mathbf { b } \rangle _ { j } ^ { ( Q _ { \mathrm { L o c } } ) }$ is the j-th basis state of the $Q ^ { \mathrm { L o c } }$ qubits, and satisfies $\langle \psi _ { n , i } | \psi _ { n , i } \rangle = 1 . \ Q ^ { \mathrm { L o c } }$ is the number of qubits needed to encode one element in a data sample.

2) Local Model Training: During the local model training process, QNN is used to train the model. For sample inference, QECD n processes the encoded data $| \psi _ { n , i } \rangle$ , which then enters the PQC. Within the PQC, unitary operations are performed on the qubits $\left| { \psi _ { n , i } } \right.$ , converting them into the output quantum states $\left| \hat { z } _ { n , i } \right.$ . Then, the gradient descent algorithm with classical computing is used by QECD n to optimize the local model parameter $\theta _ { n } .$

Specifically, a QNN uses multiple quantum gates to model a classical neural network as a PQC. In a specific QFL model, a PQC-based QNN with multiple layers of quantum gates is designed for learning. This QNN includes $\hat { N } _ { 1 }$ one-qubit gates, $\hat { N } _ { 2 }$ two-qubit gates, and $\hat { N } _ { 3 }$ measurement gates, all organized into $\dot { L } _ { n } ^ { \mathrm { Q N N } }$ qubit hidden layers. Each layerâs gates are parameterized by $\theta _ { n } .$ , which is analogous to weights in traditional neural networks. This parameterization allows the quantum gates to be adjusted during the learning process, enabling the model to optimize its performance similarly to how weights are adjusted in classical neural networks. Moreover, quantum error-correcting codes are incorporated to detect and correct qubit errors at each layer of quantum gate operations. According to [42] and [43], the unitary operation can be expressed as the composition of a sequence of completely positive layer-to-layer transition maps. Then, the output of QNN on QECD n is

$$
\left| \hat { z } _ { n , i } \right. = \mathcal { E } _ { n } ^ { L _ { n } ^ { \mathrm { Q N N } } } \left( \cdot \cdot \cdot \mathcal { E } _ { n } ^ { 2 } \left( \mathcal { E } _ { n } ^ { 1 } ( \left| \psi _ { n , i } \right. ) \right) \cdot \cdot \cdot \right) ,\tag{13}
$$

where $\mathcal { E } _ { n } ^ { l } \ = \ \mathcal { C } _ { n } ^ { l } ( \mathcal { U } _ { n } ^ { l } ( \cdot ) ) , l \ \in \ \{ 1 , 2 , \cdot \cdot \cdot , L _ { n } ^ { \mathrm { Q N N } } \}$ }. $\mathcal { U } _ { n } ^ { l }$ is the transition map of the l-th layer. ${ \mathcal { C } } _ { n } ^ { l }$ represents a quantum error correction operation for the l-th layer.

The measurements cause quantum states to collapse from a superposition or entangled state to indicate the associated classical information. After inference, the loss function for QECD n is expressed as a mean square error of the predicted and actual labels.

$$
L o s s ( \theta _ { n } ) = \frac { 1 } { D _ { n } } \sum _ { z _ { n , i } \in \mathcal D _ { n } } ( z _ { n , i } - \langle \hat { z } _ { n , i } | \hat { M } | \hat { z } _ { n , i } \rangle ) ^ { 2 } ,\tag{14}
$$

where $\hat { M }$ is a measurement operator of QECD n. The gradient descent algorithm is used to optimize the parameters $\theta _ { n }$ by minimizing the loss function. Then, the optimal parameter $\theta _ { n } ^ { * }$ is calculated by

$$
\theta _ { n } ^ { * } = \arg \operatorname* { m i n } L o s s ( \theta _ { n } ) .\tag{15}
$$

Local training continues until the required accuracy is achieved.

3) Model Aggregation and Update: Following the local training processes, the trained parameters $\theta _ { n } ^ { * }$ from individual QECDs are securely transmitted and aggregated at their associated UAV m through a federated averaging protocol, ensuring collaborative model updates while maintaining data privacy. The global parameters on UAV m are calculated by

$$
\theta _ { m } ^ { \mathrm { G l o } } = \frac { \sum _ { n = 1 } ^ { N } \mu _ { m , n } ( t ) D _ { n } \theta _ { n } ^ { * } } { \sum _ { n = 1 } ^ { N } \mu _ { m , n } ( t ) D _ { n } } .\tag{16}
$$

Then, UAV m multicasts the latest model parameters to the associated QECDs for a new round of local training. The model training continues until the model converges or the maximum number of rounds is reached.

## E. QFL Model Update Latency Analysis

1) Global Model Download Latency: Let $G _ { m } ^ { \mathrm { G l o } }$ denote the number of bits used for UAV m to multicast global model parameters to associated QECDs for local training. As such, the latency of QECD n to download the global model parameters from the associated UAV m at time slot t is

$$
T _ { n } ^ { \mathrm { D o w n } } ( t ) = \frac { G _ { m } ^ { \mathrm { G l o } } } { R _ { m , n } ^ { \mathrm { A 2 G } } ( t ) } .\tag{17}
$$

2) Local Training Latency: In the local training phase, each QECD refines its local model by leveraging its local dataset and the latest global model parameters provided by its linked UAV. The parameter k specifies the quantity of local training iterations executed per FL communication cycle. According to quantum computing technology, the latency required to process one sample in the quantum dataset is related to the number of qubits, one-qubit gates, two-qubit gates, measurement gates, and quantum error correction modules. As such, the latency of QECD n to train the local model with one sample is given by

$$
T _ { n } ^ { \mathrm { L o c } } = \left\lceil \frac { Q ^ { \mathrm { L o c } } } { Q _ { n } } \right\rceil k ( \tau _ { n } ^ { 1 } \hat { N } _ { 1 } + \tau _ { n } ^ { 2 } \hat { N } _ { 2 } + \tau _ { n } ^ { 3 } \hat { N } _ { 3 } + \tau _ { n } ^ { C } L _ { n } ^ { Q N N } ) ,\tag{18}
$$

where $Q ^ { \mathrm { L o c } }$ is the number of qubits needed to locally train the model. dÂ·e is an upward rounding function. $Q _ { n }$ is the total number of qubits owned by QECD n. $\tau _ { n } ^ { 1 } , \ \tau _ { n } ^ { 2 } ,$ , and $\tau _ { n } ^ { 3 }$ are the time of processing a one-qubit gate, a two-qubit gate, a measurement gate, and a quantum error correction module respectively. $\hat { N } _ { 1 } , \hat { N } _ { 2 }$ , and $\hat { N } _ { 3 }$ are the number of onequbit gates, two-qubit gates, and measurement gates designed according to training model, respectively.

3) Local FL Model Upload Latency: Each QECD uses the classical bits to deliver the trained model. The number of bits required for QECD n to upload its local model parameters to the associated UAV is denoted as $G _ { n } ^ { \mathrm { L o c } }$ . As such, the local model parameters upload latency of QECD n is expressed as

$$
T _ { n } ^ { \mathrm { U p } } ( t ) = \frac { G _ { n } ^ { \mathrm { L o c } } } { R _ { m , n } ^ { \mathrm { G 2 A } } ( t ) } .\tag{19}
$$

The time of one round for the UAV to obtain the updated model is composed of global model downloading latency, local model quantum training latency, and local trained model uploading latency. Therefore, the total time cost of QECD n to update the global model with one round at time slot t is given by

$$
T _ { n } ( t ) = T _ { n } ^ { \mathrm { D o w n } } ( t ) + T _ { n } ^ { \mathrm { L o c } } D _ { n } + T _ { n } ^ { \mathrm { U p } } ( t ) .\tag{20}
$$

## F. Threat Model

In this paper, we consider the following two threats during QFL in the network.

1) Low-Quality Local Model Update Attack: Because QECDs are not completely trusted, some malicious QECDs may tamper with training results, upload false model parameters, disrupt the learning process, and adversely affect the training of other QECDs to gain additional benefits. This behavior ultimately reduces the overall training performance.

2) Selfish Behavior Attack: In QFL, some QECDs may not fully contribute their computing power due to selfishness, leading to âfree-ridingâ behavior. This results in a less efficient system, as more iterations and time are required to achieve the same model performance. Consequently, the final aggregated model may not be of as high quality as it would be if all QECDs do not fully participate in the training process.

## G. Overview of the Proposed Scheme

The proposed scheme, as shown in Fig. 2, consists of the following steps:

â¢ Initialization and QFL task distribution: The UAV initializes global model parameters and distributes them to QECDs. Here, UAVs use classical communication links. Then, UAVs publish QFL tasks to associated QECDs within their coverage areas, including model parameters and training instructions.

â¢ Trust Assessment: To avoid the influence of malicious QECDs on model training, QECDsâ contributions are evaluated based on their historical performance before transmitting model updates. The trust degree of each QECD is calculated, and malicious users with low trust degrees are excluded from participating in QFL.

<!-- image-->  
Fig. 2. Overview of the proposed scheme.

â¢ Game-based incentives: UAVs hire trusted QECDs to train the model and leverage Stackelberg game theory-based incentives to ensure that QECDs deliver high-quality models. The UAV releases rewards to the connected QECDs via traditional communication channels using NLoS or LoS links.

â¢ Local training at QECDs: The QECD encodes local classical data into quantum data, and performs quantum computations to update model parameters based on the local quantum data.

â¢ Global model aggregate and update: The UAV aggregates the local model parameters uploaded from associated QECDs, which are then redistributed to all QECDs and UAVs.

The local training and global model aggregation steps are repeated until the global model converges to an acceptable level of accuracy.

Due to the high mobility of UAVs, wireless connections between QECDs and UAVs are not consistently stable, and some QECDs may occasionally fall outside the coverage range of their associated UAVs. To address these challenges, the proposed scheme facilitates cooperative QFL among QECDs. Specifically, once a UAV assigns a QFL task to QECDs, the QECDs leverage their quantum capabilities to rapidly complete local model training and send the resulting model parameters back to the associated UAVs. If the wireless connection between a QECD and its associated UAV is interrupted due to the mobility of the UAV, the QECD can use wired ground communication links to transmit the trained model parameters to neighboring QECDs that are covered by the associated UAV. These neighboring QECDs then relay the parameters to the associated UAV, ensuring seamless aggregation and updates of the model while maintaining the reliability and continuity of the QFL process.

## IV. TRUST ASSESSMENT MECHANISM

Since QECDs with high trust degrees tend to provide highquality model update parameters in the process of QFL, in this paper, a QECD trust estimation model based on Bayesian inference is proposed to evaluate the trust degrees of QECDs. Bayesian inference is a widely used probabilistic framework that can combine prior knowledge and historical behavioral data to calculate the posterior probability. The trust assessment process for QECDs consists of three steps: (1) Local trust evaluation, which analyzes the quality of model parameters uploaded during federated learning tasks and employs

Bayesian inference to update trust scores; (2) Recommendation trust evaluation, where trust recommendations from other UAVs are combined based on similarity to refine the trust assessment; and (3) Comprehensive trust calculation, where local and recommendation trust scores are integrated with a weight factor to achieve a balanced evaluation.

## A. Local Trust Evaluation

From the initial time to the current time slot t, H QFL tasks of all UAVs have been executed. The set of QFL tasks is denoted as $\mathcal { H } ( t ) = \{ 1 , 2 , \dots , H \}$ . Let $\tilde { a } _ { m } ^ { ( h ) } = 1$ denote that QFL task h is published by UAV m, and $\tilde { a } _ { m } ^ { ( h ) } = 0$ is that QFL task h is not published by UAV m. Each QFL task is published only by one UAV, i.e., $\begin{array} { r } { \sum _ { m = 1 } ^ { M } \tilde { a } _ { m } ^ { ( h ) } = \bar { 1 } , \forall h \in \mathcal { H } . } \end{array}$ Let $\tilde { b } _ { n } ^ { ( h ) } = 1$ indicate that QECD n participates in the model training of QFL task h, and otherwise $\tilde { b } _ { n } ^ { ( h ) } = 0$

For QFL task $h \in \mathcal H$ , there are $G _ { h }$ rounds for global model training. In this context, the number of interactions between the UAV and associated QECDs is $G _ { h }$ for executing QFL task h. In the g-th round of QFL task h, and if $\tilde { a } _ { m } ^ { ( h ) } = 1$ and $\tilde { b } _ { n } ^ { ( h ) } = 1$ , the model parameters uploaded by QECD n are $\theta _ { n } ^ { ( h , g ) }$ . The set of QECDs participating in QFL task h is denoted as $\Theta ^ { ( h ) } = \bar { \{ { n ^ { \prime } } | { { \tilde { b } } _ { n ^ { \prime } } ^ { ( h ) } } = 1 , \forall { { \tilde { n } } ^ { \prime } } \in \bar { \mathcal { N } } \} }$ . The relative offset distance of model parameters uploaded by QECD n in the g-th round of QFL task h is given by

$$
D i s _ { n } ^ { ( h , g ) } = \frac { 1 } { | \Theta ^ { ( h ) } | - 1 } \sum _ { n ^ { \prime } \in \Theta ^ { ( h ) } / \{ n \} } \Big \Vert \theta _ { n } ^ { ( h , g ) } - \theta _ { n ^ { \prime } } ^ { ( h , g ) } \Big \Vert _ { F } ,\tag{21}
$$

where $\left\| \cdot \right\| _ { F }$ is the Frobenius norm of the matrix. Generally, most of the QECDs in the network are honest, resulting in minimal difference in their model parameters. Consequently, the relative offset distances of model parameters from honest QECDs are significantly smaller compared to those from dishonest QECDs. It is assumed that the model parameters with a low relative offset distance are high-quality, and otherwise the model parameters are low-quality. As such, the quality of model parameters uploaded by QECD n in the g-th round of QFL task h is expressed by

$$
\widetilde { Q } _ { n } ^ { ( h , g ) } = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f } \frac { \operatorname* { m i n } _ { n ^ { \prime } \in \Theta ^ { ( h ) } } \{ D i s _ { n ^ { \prime } } ^ { ( h , g ) } \} } { D i s _ { n } ^ { ( h , g ) } } \geq Q _ { h , g } ^ { \mathrm { T h r e } } , } \\ { 0 , } & { \mathrm { o t h e r w i s e , } } \end{array} \right.\tag{22}
$$

where $Q _ { h , g } ^ { \mathrm { T h r e } }$ is the adjustable threshold of global model parameters in the g-th round of QFL task h. Here, $\widetilde { Q } _ { n } ^ { ( h , g ) } = 1$ means that the model parameters from QECD n in the g-th round of QFL task h is high-quality, and otherwise $\widetilde { Q } _ { n } ^ { ( h , g ) } = 0 .$

For UAV m, the set of QFL tasks that QECD n participates in is denoted as $\mathcal { H } _ { m , n } ( t )$ $\{ h \left| \tilde { a } _ { m } ^ { ( h ) } = 1 , \tilde { b } _ { n } ^ { ( h ) } = 1 , \forall h \in \mathcal { H } ( t ) \right. \}$ The number of global model training rounds of $| \mathcal { H } _ { m , n } ( t ) |$ QFL tasks is $\sum _ { h \in \mathcal { H } _ { m , n } ( t ) } G _ { h }$ , and let $\begin{array} { r } { \tilde { N } _ { m , n } ( t ) \stackrel { \Delta } { = } \sum _ { h \in \mathcal { H } _ { m , n } ( t ) } G _ { h } } \end{array}$ . We use a discrete random variable $X _ { n } \in \{ 0 , 1 \}$ to indicate whether QECD n is credible. $X _ { n } ~ = ~ 1$ indicates that QECD n is credible, and otherwise $X _ { n } = 0$ . The probability distribution of $X _ { n }$ is

$$
\operatorname* { P r } ( X _ { n } ) = { \left\{ \begin{array} { l l } { q _ { n } , } & { { \mathrm { i f } } X _ { n } = 1 , } \\ { 1 - q _ { n } , } & { { \mathrm { o t h e r w i s e } } , } \end{array} \right. }\tag{23}
$$

where $0 \leq q _ { n } \leq 1$ . Since we do not have any prior knowledge about whether QECDs are credible or not, it is assumed that $q _ { n }$ follows a uniform distribution between 0 and 1. The probability density function of $q _ { n }$ is

$$
f ( q _ { n } ) = { \left\{ \begin{array} { l l } { 1 , } & { { \mathrm { i f ~ } } 0 \leq q _ { n } \leq 1 } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }\tag{24}
$$

Without loss of generality, the credible QECD can generate the high-quality QFL model parameters. A random variable $\hat { c } ( \tilde { N } _ { m , n } ( t ) )$ is used to indicate the number of that rounds model parameters updated from QECD n to UAV m until time slot t being high-quality. Then, $\hat { c } ( \tilde { N } _ { m , n } ( t ) )$ ) follows a binomial distribution, where the probability of $\hat { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell$ can be expressed as

$$
\begin{array} { r l } & { \operatorname* { P r } \Big ( \hat { c } \Big ( \tilde { N } _ { m , n } ( t ) \Big ) = \ell \mid q _ { n } \Big ) } \\ & { = \binom { \tilde { N } _ { m , n } ( t ) } { \ell } q _ { n } ^ { \ell } \left( 1 - q _ { n } \right) ^ { \bar { N } _ { m , n } ( t ) - \ell } , \ell \in \left\{ 0 , \cdots , \tilde { N } _ { m , n } ( t ) \right\} , } \end{array}\tag{25}
$$

$$
\begin{array} { r } { \mathrm { w h e r e } \left( \begin{array} { l } { \widetilde { N } _ { m , n } ( t ) } \\ { \ell } \end{array} \right) = \frac { \widetilde { N } _ { m , n } ( t ) ! } { \ell ! \left( \widetilde { N } _ { m , n } ( t ) - \ell \right) ! } . } \end{array}
$$

In order to assess the local trust degree of QECD n at time slot t from UAV mâs point of view, Bayesian inference is utilized to update the probability distribution about the probability of that QECD n is credible. According to Bayes theorem, the posterior distribution $f \left( q _ { n } \left| \hat { c } ( \tilde { N } _ { m , n } ( t ) ) = \bar { \ell } \right. \right)$ can be calculated by

$$
f \left( \boldsymbol { q } _ { n } \left| \hat { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell \right. \right) = \frac { \operatorname* { P r } \left( \hat { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell | \boldsymbol { q } _ { n } \right) f ( \boldsymbol { q } _ { n } ) } { \operatorname* { P r } \left( \hat { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell \right) } ,\tag{26}
$$

where $\operatorname* { P r } \left( \hat { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell \right)$ can be expressed as

$$
\begin{array} { r l } & { \operatorname* { P r } \Big ( \hat { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell \Big ) } \\ & { = \displaystyle \int _ { 0 } ^ { 1 } \operatorname* { P r } \Big ( \hat { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell | q _ { n } \Big ) f ( q _ { n } ) d q _ { n } . } \end{array}\tag{27}
$$

Substituting Eq. (27) into the Eq. (26), we can attain

$$
\begin{array} { l } { f \left( q _ { n } \left| \tilde { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell \right. \right) } \\ { = \frac { \operatorname* { P r } \left( \tilde { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell \left| q _ { n } \right) f ( q _ { n } ) } { \int _ { 0 } ^ { 1 } \operatorname* { P r } \left( \tilde { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell \right| q _ { n } \right) f ( q _ { n } ) d q _ { n } } } \\ { = \frac { \binom { \tilde { N } _ { m , n } ( t ) } { \tilde { \ell } } q _ { n } \ell ( 1 - q _ { n } ) ^ { \tilde { N } _ { m , n } ( t ) - \ell } } { \int _ { 0 } ^ { 1 } \operatorname* { P r } \big ( \tilde { c } ( \tilde { N } _ { m , n } ( t ) ) = \ell \big | q _ { n } \big ) f ( q _ { n } ) d q _ { n } } } \\ { = \frac { q _ { n } \ell ( 1 - q _ { n } ) ^ { \tilde { N } _ { m , n } ( t ) - \ell } } { \int _ { 0 } ^ { 1 } q _ { n } \ell ( 1 - q _ { n } ) ^ { \tilde { N } _ { m , n } ( t ) - \ell } d q _ { n } } . } \end{array}\tag{28}
$$

Eq. (28) indicates that $q _ { n } \ | \hat { c } \left( \tilde { N } _ { m , n } ( t ) \right)$ follows a Beta distribution, i.e.,

$$
q _ { n } \left| \hat { c } ( \tilde { N } _ { m , n } ( t ) ) \sim B e t a ( \ell + 1 , \tilde { N } _ { m , n ( t ) } - \ell + 1 ) . \right.\tag{29}
$$

Based on the interactions between UAV m and QECD $n ,$ the local trust degree of UAV m on QECD n at time slot t is obtained by

$$
\begin{array} { r l r } {  { \boldsymbol { \Psi } _ { m , n } ^ { \mathrm { L o c } } ( t ) = \mathbf { I } \alpha _ { m } ( t ) \cdot \mathbf { E } [ q _ { n } | \hat { c } ( \tilde { N } _ { m , n } ( t ) )  ] \Big | _ { \ell = \sum _ { h = 1 } ^ { H } \sum _ { g = 1 } ^ { G _ { h } } \widetilde { Q } _ { n } ^ { ( h , g ) } } } } \\ & { } & { \ \underset { = \mathbf { I } \alpha _ { m } ( t ) \cdot \frac { h = 1 } { \tilde { N } _ { m , n } ( t ) + 2 } } { \sum _ { m } ^ { H } \sum _ { n } ^ { G _ { h } } } \widetilde { Q } _ { n } ^ { ( h , g ) } + 1 } , \qquad ( 3 0 )  \end{array}
$$

where the dynamic adjustment factor $\begin{array} { r l } { \mathbf { l } \alpha _ { m } ( t ) } & { { } = } \end{array}$ $\log _ { 2 } { ( 1 + \widetilde { \gamma } _ { m , n } ^ { \mathrm { G 2 A } } ( t ) ) }$ is used to describe the quality of econnection stability between UAV m and QECD n. This factor can be dynamically adjusted based on changes in UAVsâ mobility.

## B. Recommendation Trust Evaluation

Since different UAVs have different historical interactions with QECDs for QFL model training, each UAV can also require recommendations from other UAVs to assess the trust on the same QECD. To obtain the recommendation, the similarity among different UAVs should be first analyzed. The similarity between UAV m and $m ^ { \prime }$ is calculated as

$$
\begin{array} { r l } & { S i m _ { m , m ^ { \prime } } ( t ) } \\ & { = \frac { \sum _ { n \in \Phi _ { m \cap m ^ { \prime } } } \left( \Psi _ { m , n } ( t ) - \Psi _ { m ^ { \prime } , n } ( t ) \right) } { \sqrt { \sum _ { n \in \Phi _ { m \cap m ^ { \prime } } } \left( \Psi _ { m , n } ( t ) \right) ^ { 2 } } \sqrt { \sum _ { n \in \Phi _ { m \cap m ^ { \prime } } } \left( \Psi _ { m ^ { \prime } , n } ( t ) \right) ^ { 2 } } } , } \end{array}\tag{31}
$$

where $\Phi _ { m } ~ = ~ \{ n \left| \tilde { a } _ { m } ^ { ( h ) } = 1 , \tilde { b } _ { n } ^ { ( h ) } = 1 , \forall h ~ \in ~ \mathcal { H } , \forall n ~ \in ~ \mathcal { N } \right\}$ denotes the set of QECDs having interacted with UAV m and $\Phi _ { m ^ { \prime } } = \{ n \left| \tilde { a } _ { m ^ { \prime } } ^ { ( h ) } = 1 , \tilde { b } _ { n } ^ { ( h ) } = 1 , \forall h \in \mathcal { H } \mathrm { ~ , } \forall n \in \mathcal { N } \right\}$ is the set of QECDs interacting with UAV m0. $\Phi _ { m \cap m ^ { \prime } } = \Phi _ { m } \cap \Phi _ { m ^ { \prime } }$ is the set of QECDs that have interactions with both QECD m and $m ^ { \prime }$

As such, the recommendation of other UAVs for UAV m to assess the trust of QECD n can be given by

$$
\Psi _ { m , n } ^ { \mathrm { R e c o } } = \frac { \sum _ { m ^ { \prime } \in \mathcal { M } / m } S i m _ { m , m ^ { \prime } } ( t ) \Psi _ { m ^ { \prime } , n } ( t ) } { \sum _ { m ^ { \prime } \in \mathcal { M } / m } S i m _ { m , m ^ { \prime } } ( t ) } .\tag{32}
$$

In summary, by combining local trust assessment and recommended trust, the comprehensive trust degree of UAV m on QECD n at time slot t can be obtained by

$$
\Psi _ { m , n } ^ { \mathrm { C o m p } } ( t ) { = } \omega _ { m } \Psi _ { m , n } ^ { \mathrm { L o c } } ( t ) + ( 1 - \omega _ { m } ) \Psi _ { m , n } ^ { \mathrm { R e c o } ( t ) } ,\tag{33}
$$

where $\omega _ { m }$ is the weight factor. The weight factor $\omega _ { m }$ plays a critical role in balancing local trust and recommended trust within the final trust assessment. A higher value of $\omega _ { m }$ increases reliance on local trust, which is advantageous in environments with ample interaction data but may overlook the broader global perspective. Conversely, a lower $\omega _ { m }$ places greater emphasis on recommended trust, leveraging global insights from other agents while potentially exposing the system to noise or biased recommendations. The selection of $\omega _ { m }$ should be tailored to the specific requirements of the task. For instance, in scenarios where trust uncertainty arises due to limited local interactions, a smaller $\omega _ { m }$ can incorporate external recommendations to reduce uncertainty, thereby enabling a more robust and accurate trust assessment on QECDs.

When UAV m publishes a new QFL task at time slot t, it can set the trust threshold $\Psi _ { m } ^ { \mathrm { T h r e } } ( t )$ according to its own requirements to select the QECDs, and filter out the QECDs with low trust degree.

## V. GAME-BASED INCENTIVE STRATEGY

After the trusted QECDs have been selected, a Stackelberg game theory-based incentive strategy is designed to incentivize these QECDs to actively participate in model training. In this strategy, the UAV, as the leader, first determines the payment strategy, which is the reward delivered to the trusted QECDs within its coverage area. Subsequently, the QECDs, as followers, choose their optimal level of effort (i.e., the number of data samples) to participate in the model training based on the payment strategy provided by the associated UAVs, aiming to maximize their own utilities.

## A. Utility Analysis

The utility function of the UAV: The objective of each UAV is to design an appropriate payment strategy to maximize the quality of the global model. Based on the findings in [44], [45], and [46], the relationship between model training accuracy and the amount of data can be approximated by a natural logarithm function. As the data volume increases, the incremental improvement in model training accuracy and utility tends to diminish. The logarithmic function effectively captures this relationship by exhibiting rapid growth when data sizes are small, while the growth rate gradually decreases as the data volume increases. Therefore, the utility of UAV m can be obtained by

$$
u _ { m } ( \mathbf { p } _ { m } ) = v _ { s } F ( \mathbf { a } _ { m } ) - \sum _ { n = 1 } ^ { N _ { m } } v _ { p } p _ { n , m } \zeta _ { m } \log ( 1 + a _ { n , m } D _ { n } ) ,\tag{34}
$$

where $F ( \mathbf { a } _ { m } )$ denotes the satisfaction function. $v _ { p }$ and $v _ { s }$ are the adjustment coefficients. $\mathbf { p } _ { m } ~ = ~ \left( p _ { 1 , m } , \cdots , p _ { N _ { m } , m } \right)$ and $\mathbf { a } _ { m } ~ = ~ \left( a _ { 1 , m } , \cdot \cdot \cdot , a _ { N _ { m } , m } \right)$ are the payment strategy vector of UAV m and the contribution level vector of selected trusted $N _ { m }$ QECDs, respectively. $\zeta _ { m } = 1 / \ln ( 1 + D _ { n } )$ is the normalization factor. $D _ { n }$ is the total size of the dataset used by QECD n to execute the training task for UAV m.

The satisfaction function of the UAV depends on the model training quality and latency of the QECDs, which is related to the amount of data contributed by the QECDs and their computing capabilities. Hence, the satisfaction function of UAV m can be defined as

$$
F ( \mathbf { a } _ { m } ) = \sum _ { n = 1 } ^ { N _ { m } } \alpha _ { m } \zeta _ { m } \Psi _ { m , n } ^ { \mathrm { C o m p } } \log ( 1 + a _ { n , m } D _ { n } )
$$

$$
- \beta _ { m } \sum _ { n = 1 } ^ { N _ { m } } { ( a _ { n , m } D _ { n } T _ { n } ^ { \mathrm { L o c } } + T _ { n } ^ { \mathrm { U p } } + T _ { n } ^ { \mathrm { D o w n } } ) } ,\tag{35}
$$

where $\alpha _ { m }$ and $\beta _ { m }$ are the adjustment coefficients used to balance the satisfaction function.

The utility function of QECDs: The objective of the QECDs is to maximize their own profit. The utility function of QECD n can be expressed as the reward obtained from the UAV m minus the cost, i.e.,

$$
u _ { n , m } ( a _ { n , m } ) = p _ { n , m } \zeta _ { m } \ln ( 1 + a _ { n , m } D _ { n } ) - v _ { n , m } C _ { n , m } ,\tag{36}
$$

where $v _ { n , m }$ is an adjustment factor used to balance the reward and the cost. $C _ { n , m }$ represents the cost for the QECD to participate in training, which specifically includes the computational cost $C _ { n , m } ^ { c o m p }$ of local model training and the communication cost $C _ { n , m } ^ { c o m }$ of model parameters uploading.

Generally, a larger amount of local model training data will result in greater computational energy consumption for the QECD, which is also related to the configuration of the quantum computer. Specifically, the computational cost can be represented as

$$
C _ { n , m } ^ { c o m p } = P _ { n , m } ^ { q } a _ { n , m } D _ { n } T _ { n } ^ { \mathrm { L o c } } ,\tag{37}
$$

where $P _ { n , m } ^ { q }$ is the power consumption per data sample during the training task of UAV m, which can be obtained from [47]. On the other hand, the communication cost of model uploading can be expressed as

$$
C _ { n , m } ^ { c o m } = P _ { n } T _ { n } ^ { \mathrm { U p } } ,\tag{38}
$$

where $P _ { n }$ is the transmission power.

Then the utility function of QECD n is given by

$$
\begin{array} { r l } & { u _ { n , m } ( a _ { n , m } ) = p _ { n , m } \zeta _ { m } \ln ( 1 + a _ { n , m } D _ { n } ) } \\ & { \phantom { = } - v _ { n , m } \left( P _ { n , m } ^ { q } a _ { n , m } D _ { n } T _ { n } ^ { \mathrm { L o c } } + P _ { n } T _ { n } ^ { \mathrm { U p } } \right) . } \end{array}\tag{39}
$$

The utilities of both UAVs and QECDs are influenced by the payment and the total size of the dataset, i.e., $D _ { n }$ . When $D _ { n }$ is large, according to (35), the satisfaction of the UAV increases. However, a large $D _ { n }$ also imposes a significant computational overhead on the QECD, referring to (37). To ensure satisfactory utility for both the QECD and the UAV, a negotiation between the UAV and QECD on the payment is conducted. Through this negotiation, the payment from the UAV for local training services increases, thereby enhancing the utility of the QECD, as described in (36).

## B. Problem Formulation and Game Analysis

In the network, the UAV, acting as the leader, needs to formulate the optimal payment strategy to maximize its utility (i.e., model training quality), which can be defined as

$$
\operatorname* { m a x } _ { \mathbf { p } _ { m } } \quad u _ { m } ( \mathbf { p } _ { m } )\tag{40}
$$

$$
\begin{array} { r } { s . t . \quad 0 \leq p _ { n , m } \leq p ^ { \operatorname* { m a x } } , } \end{array}\tag{41}
$$

where $p ^ { \mathrm { m a x } }$ is the allowable payment for a QECD.

After obtaining the payment strategy from UAV m, each QECD will choose the optimal level of contribution to balance the benefits and costs for participating in the training, i.e.,

$$
\operatorname* { m a x } _ { a _ { n , m } } \quad u _ { n , m } ( a _ { n , m } )\tag{42}
$$

$$
s . t . \quad a _ { n , m } \in [ 0 , 1 ] .\tag{43}
$$

Theorem 1: There exists a Stackelberg equilibrium for UAV and QECD which satisfies

$$
\begin{array} { r l } & { u ( \mathbf { p } _ { m } ^ { * } , \mathbf { a } _ { n } ^ { * } ) \geq u ( \mathbf { p } _ { m } , \mathbf { a } _ { n } ^ { * } ) , \forall \mathbf { p } _ { m } \neq \mathbf { p } _ { m } ^ { * } , } \\ & { \qquad u _ { n , m } ( a _ { n , m } ^ { * } , \mathbf { a } _ { - n } ^ { * } , \mathbf { p } _ { m } ^ { * } ) \geq u _ { n , m } ( a _ { n , m } , \mathbf { a } _ { - n } ^ { * } , \mathbf { p } _ { m } ^ { * } ) , } \\ & { \qquad \forall a _ { n , m } \neq a _ { n , m } ^ { * } , } \end{array}\tag{44}
$$

where $\mathbf { a } _ { - n } ^ { * }$ is the optimal contribution of all QECDs except QECD n.

Proof: To find the optimal strategy for this game, we first analyze the existence of a Nash equilibrium using the backward induction method. First, the first-order and secondorder derivative of $u _ { n , m } ( a _ { n , m } )$ with respect to $a _ { n , m }$ are respectively given by

$$
\frac { \partial u _ { n , m } } { \partial a _ { n , m } } = p _ { n , m } \zeta _ { m } \cdot \frac { D _ { n } } { 1 + a _ { n , m } D _ { n } } - v _ { n , m } P _ { n , m } ^ { q } D _ { n } T _ { n } ^ { \mathrm { L o c } } ,\tag{45}
$$

$$
\frac { \partial ^ { 2 } u _ { n , m } } { \partial a _ { n , m } ^ { 2 } } = - p _ { n , m } \zeta _ { m } \cdot \frac { D _ { n } ^ { 2 } } { ( 1 + a _ { n , m } D _ { n } ) ^ { 2 } } .\tag{46}
$$

From (46), we can get $\begin{array} { r } { \frac { \partial ^ { 2 } u _ { n , m } } { \partial a _ { n , m } ^ { 2 } } \leq 0 . } \end{array}$ As such, the utility function of QECD m is concave, whereby the optimal contribution strategy can be obtained by letting $\begin{array} { r } { \frac { \partial u _ { n , m } } { \partial a _ { n , m } } \stackrel {  } { = } 0 , } \end{array}$ i.e.,

$$
a _ { n , m } ^ { * } = \frac { p _ { n , m } \zeta _ { m } - v _ { n , m } P _ { n , m } ^ { q } T _ { n } ^ { \mathrm { L o c } } } { v _ { n , m } P _ { n , m } ^ { q } T _ { n } ^ { \mathrm { L o c } } D _ { n } } .\tag{47}
$$

Considering that $a _ { n , m } ~ \in ~ [ 0 , 1 ]$ , the optimal contribution strategy under the given optimal payment strategy is given by

$$
\begin{array} { r l } & { a _ { n , m } ^ { * } } \\ & { = \left\{ \begin{array} { l l } { 0 , } & { \mathrm { i f ~ } p _ { n , m } < \Xi _ { n } ^ { \mathrm { m i n } } } \\ { \displaystyle \frac { p _ { n , m } \zeta _ { m } - v _ { n , m } P _ { n , m } ^ { q } T _ { n } ^ { \mathrm { L o c } } } { v _ { n , m } P _ { n , m } ^ { q } T _ { n } ^ { \mathrm { L o c } } D _ { n } } , } & { \mathrm { i f ~ } \Xi _ { n } ^ { \mathrm { m i n } } \leq p _ { n , m } \leq \Xi _ { n } ^ { \mathrm { m a x } } } \\ { 1 , } & { \mathrm { i f ~ } p _ { n , m } > \Xi _ { n } ^ { \mathrm { m a x } } } \end{array} \right. } \end{array}\tag{48}
$$

where $\begin{array} { r } { \Xi _ { n } ^ { \mathrm { m i n } } = \frac { v _ { n , m } P _ { n , m } ^ { q } T _ { n } ^ { \mathrm { L o c } } } { \zeta _ { m } } \mathrm { ~ a n d ~ } \Xi _ { n } ^ { \mathrm { m a x } } = \Xi _ { n } ^ { \mathrm { m i n } } ( 1 + D _ { n } ) . } \end{array}$

Similarly, given the optimal contribution strategy vector $\mathbf { a } _ { n } ^ { * } ,$ the first-order and second-order derivative of $u _ { m } ( \mathbf { p } _ { m } )$ with respect to $p _ { n , m }$ are respectively calculated by

$$
\frac { \partial u _ { m } } { \partial p _ { n , m } } = v _ { s } \left( \frac { \Omega _ { n , m } } { p _ { n , m } } - \Lambda _ { n , m } \left( \ln ( p _ { n , m } ) + 1 \right) \right) ,\tag{49}
$$

$$
\frac { \partial ^ { 2 } u _ { m } } { \partial p _ { n , m } ^ { 2 } } = v _ { s } \left( - \frac { \Omega _ { n , m } } { p _ { n , m } ^ { 2 } } - \frac { \Lambda _ { n , m } } { p _ { n , m } } \right) ,\tag{50}
$$

where $\Omega _ { n , m } = \alpha _ { m } \zeta _ { m } \Psi _ { m , n } ^ { \mathrm { C o m p } }$ and $\Lambda _ { n , m } = v _ { p } \zeta _ { m }$ . Similarly, it can be concluded that $\frac { \partial ^ { 2 } u _ { m } ( \mathbf { p } _ { m } ) } { \partial p _ { n . m } ^ { 2 } } \leq 0$ , thus there exists an optimal payment strategy $\mathbf { p } _ { m } ^ { * }$ that maximizes the utility of the UAV m. In summary, there exists an optimal payment strategy $\mathbf { p } _ { m } ^ { * }$ and contribution strategy $\mathbf { a } _ { n } ^ { * }$ that maximize the utilities for both UAV and QECDs, thereby ensuring the existence of the Nash equilibrium. This compelets our proof. 

## C. Nash Equilibrium Solution Based on Deep Q-Network

Considering the dynamic nature of the network and the need for privacy protection in practical applications, the UAV cannot accurately obtain all system parameters. We model the aforementioned incentive problem as a Markov decision process (MDP) and use DQN to find the optimal strategy.

DQN is a model-free deep reinforcement learning algorithm that enables the UAV to obtain the optimal payment strategy without having access to the specific parameters of the QECDs. First, the payment strategy can be transformed into an MDP problem, specifically encompassing the state space, action space, and reward, which can be denoted as $\langle S , A , r \rangle$ The state space at each time slot t includes the historical payment strategies and the past strategies of the QECDs from the last L steps, specifically represented as

$$
{ \cal S } _ { m } ^ { t } = \left\{ { \bf p } _ { m } ^ { t - L } , \cdot \cdot \cdot , { \bf p } _ { m } ^ { t - 1 } , { \bf a } _ { n } ^ { t - L } , \cdot \cdot \cdot , { \bf a } _ { n } ^ { t - 1 } \right\} ,\tag{51}
$$

where $\begin{array} { r l r } { \mathbf { p } _ { m } ^ { t } } & { { } \ = \ } & { \{ p _ { 1 , m } ^ { t } , \cdot \cdot \cdot , p _ { N _ { m } , m } ^ { t } \} } \end{array}$ and $\begin{array} { r l } { \mathbf { a } _ { n } ^ { t } } & { { } = } \end{array}$ $\left\{ a _ { 1 , m } ^ { t } , \cdots , a _ { N _ { m } , m } ^ { t } \right\}$ . The action space and reward are given by $A _ { m } ^ { t } = \mathbf { p } _ { m } ^ { t }$ and $r _ { m } ^ { t } = u _ { m } ( \mathbf { p } _ { m } ^ { t } )$

Algorithm 1 DQN-Based Payment Decision Algorithm   
1 Initialize replay buffer $\tilde { \mathcal { D } } ,$ the Q-network and target Q   
network with $\theta _ { q , m } = \tilde { \theta } _ { q }$ ,m.   
2 for episode = 1 to $T ^ { E P }$ do   
3 Initialize state S.   
4 for t = 1 to T do   
5 Choose the payment $A _ { m } ^ { t }$ with probability   
. Otherwise choose $A _ { m } ^ { t }$ by $A _ { m } ^ { t }$ =   
arg max $_ A Q ( S _ { m } ^ { t } , A ; \theta _ { q , m } )$   
6 Execute action $A _ { m } ^ { t } ,$ get the reward $r ^ { t }$ and next   
observation $S _ { m } ^ { t + 1 }$ according to (34) and (48).   
7 Save transition $( { S _ { m } ^ { t } } , { A _ { m } ^ { t } } , { \bar { r _ { m } ^ { t } } } , { S _ { m } ^ { t + 1 } } )$ into the replay   
buffer ${ \widetilde { \cal D } } ,$ and sample a mini-batch of transitions   
from $\widetilde { \mathcal { D } } .$   
8 for all each mini-batch transition do   
9 Compute target for each mini-batch transition   
according to (52).   
10 Update Q network parameter according to (53).   
11 end for   
12 Update state $S _ { m } ^ { t } = S _ { m } ^ { t + 1 }$   
13 Reduce exploration rate $\epsilon = \operatorname* { m a x } ( \epsilon _ { \mathrm { m i n } } , \epsilon \cdot \epsilon _ { \mathrm { d e c a y } } )$   
14 if $t \% T ^ { U p \dot { d a } t e } = = 0$ then   
15 Update target network: $\theta _ { q , m } = \tilde { \theta } _ { q , m } .$   
16 end if   
17 end for   
18 end for

DQN approximates the Q-function using a neural network, thereby addressing the limitations of traditional Q-learning in handling complex state and action spaces. As shown in Fig. 3, the Q-network $Q ( S _ { m } ^ { t } , A _ { m } ^ { t } ; \theta _ { q , m } )$ represents the expected return for taking action $A _ { m } ^ { t }$ in state $S _ { m } ^ { t } ,$ where $\theta _ { q , m }$ is the parameter of the Q-network. The objective is to enable the UAV, acting as an agent, to interact with the environment through exploration and trial-and-error to generate experience trajectories $( S _ { m } ^ { t } , A _ { m } ^ { t } , r _ { m } ^ { t } , S _ { m } ^ { t + 1 } )$ . These experience trajectories are then used to train the neural network to approximate the optimal Q-function. To improve training stability, the target Q-network $Q ( S _ { m } ^ { t } , A _ { m } ^ { t } ; \tilde { \theta } _ { q , m } )$ , which shares the same structure as the Q-network, is introduced. Its parameter $\tilde { \theta } _ { q , m }$ is synchronized with the Q-networkâs parameter $\theta _ { q , m }$ at fixed steps. During the network training phase, a small batch of samples is randomly selected from the experience replay buffer to calculate the target Q-values based on the Bellman equation, which can be specifically represented as

<!-- image-->  
Fig. 3. Framework of proposed DQN-based algorithm.

$$
\tilde { y } _ { m } ^ { t } = \boldsymbol { r } _ { m } ^ { t } + \gamma \operatorname* { m a x } _ { A _ { m } ^ { t + 1 } } Q ( S _ { m } ^ { t + 1 } , A _ { m } ^ { t + 1 } ; \tilde { \boldsymbol { \theta } } _ { q , m } ) ,\tag{52}
$$

where $\gamma$ is the discount factor, used to balance the importance of future rewards. Therefore, the loss function for model training is given by

$$
L o s s ( \theta _ { q , m } ) = \frac { 1 } { T _ { s } } { \sum _ { t = 1 } ^ { T _ { s } } } \big ( \tilde { y } _ { m } ^ { t } - Q ( S _ { m } ^ { t } , A _ { m } ^ { t } ; \theta _ { q , m } ) \big ) ^ { 2 } ,\tag{53}
$$

where $T _ { s }$ is the size of the mini-batch. To minimize the loss function, gradient descent is used to update the network parameter: $\theta _ { q , m }  \theta _ { q , m } - \eta _ { l r } \nabla _ { \theta } L o s s ( \theta _ { q , m } )$ . The specific algorithm flow is represented in Algorithm 1.

The computational complexity of Algorithm 1 can be analyzed as follows. The training process runs for $T ^ { E P }$ episodes, and within each episode, it executes T time steps. At every time step, the UAV first needs to select an action based on the current state, which typically involves a forward pass through the Q-network, which incurs a complexity of $O ( \psi _ { N N } )$ . ÏNN represents the complexity of a single forward pass (and backward pass) through the neural network. After selecting the action, the UAV interacts with the environment to obtain the next state and reward, and then stores the resulting transition in the replay buffer. It subsequently samples a mini-batch of size $T _ { s }$ from the replay buffer and uses these samples to update the Q-network parameters. This parameter update step is dominated by forward and backward passes over $T _ { s }$ samples, resulting in a complexity of approximately $O ( T _ { s } \cdot \psi _ { N N } )$ per time step for the training process. Combining the action selection cost $O ( \psi _ { N N } )$ and the mini-batch update cost $O ( T _ { s } \cdot \psi _ { N N } )$ yields $O ( ( T _ { s } + 1 ) \cdot \psi _ { N N } )$ per time step. Finally, considering all T steps per episode and $\dot { T } ^ { E P }$ episodes, the total complexity is $O ( T ^ { \bar { E } P } \cdot T \cdot ( T _ { s } + 1 ) \cdot \psi _ { N N } )$

TABLE I  
SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>The noise power $\delta ^ { 2 }$ </td><td rowspan=1 colspan=1>-170 dBM</td></tr><tr><td rowspan=1 colspan=1>The maximum flying velocity of UAVs $V _ { m a x }$ </td><td rowspan=1 colspan=1>20m/s</td></tr><tr><td rowspan=1 colspan=1>The maximum payment $p ^ { m a x }$ </td><td rowspan=1 colspan=1>100</td></tr><tr><td rowspan=1 colspan=1>Number of episodes in DQN $\overline { { T ^ { E P } } }$ </td><td rowspan=1 colspan=1>2000</td></tr><tr><td rowspan=1 colspan=1>The discount factor  in DQN</td><td rowspan=1 colspan=1>0.75</td></tr><tr><td rowspan=1 colspan=1>The Q-network update frequency TUpdate</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>The transmission power $P _ { n }$ </td><td rowspan=1 colspan=1>25dBM</td></tr><tr><td rowspan=1 colspan=1>The carrier frequency f</td><td rowspan=1 colspan=1>1 GHz</td></tr></table>

## D. Security Analysis

In this paper, we propose a novel QFL scheme designed to address two primary threats in UAV-assisted wireless networks: low-quality local model updates and selfish behavior attacks. To mitigate the first threat, we implement a trust evaluation model that continuously monitors and assesses the contributions of each QECD. By integrating Bayesian inference, this model dynamically adjusts trust levels, combining prior knowledge with historical behavior data to accurately determine the trustworthiness of each QECD. To combat selfish behaviors, we employ a Stackelberg game-based incentive strategy, where the UAV acts as the leader and sets a payment strategy to reward trusted QECDs. This approach motivates QECDs to actively participate in model training, optimizing their effort levels and reducing free-riding behaviors. Consequently, system efficiency is enhanced, and the final aggregated model quality is maintained at a high standard. These combined measures effectively defend against both lowquality model update attacks and selfish behavior, ensuring the security and cooperation necessary for reliable QFL. Overall, the proposed scheme not only improves the robustness and reliability of QFL but also fosters collaboration among participants, providing a secure and efficient distributed learning environment.

## VI. PERFORMANCE EVALUATION

In this section, extensive simulations are carried out to evaluate the performance of the proposed scheme. First, the simulation setup is described, followed by an analysis of the numerical results.

## A. Simulation Setup

In this paper, MATLAB is used to construct the experimental platform, leveraging the MATLAB support package for quantum computing [48] to simulate and execute quantum operations. We consider a UAV-assisted wireless network with two UAVs uniformly deployed in the air, and multiple QECDs are uniformly distributed within the communication radius 300 m of each UAV to participate in local model training. Each UAVâs flight altitude is fixed at 200 m. The communication bandwidth $B ^ { \mathrm { G 2 A } }$ and $B ^ { \mathrm { A 2 G } }$ are 5 MHz and 1 MHz, and the transmission power of UAVs and QECDs is set to 50 mW and 80 mW. For the quantum computation model, as referenced in [47], the qubit frequency typically operates at 6 GHz. The one-qubit and two-qubit gate operations are randomly selected from [10,30] ns and [100,200] ns respectively. Similarly, measurements are conducted over a duration of 100 ns. For the QFL, the total training data size of each QECD n follows uniform distribution [100, 200] MB. The adjustment factors $\alpha _ { m }$ and $\beta _ { m }$ are set to 100 and 0.0001. The adjustment coefficients $v _ { p }$ and $v _ { s }$ are set to 1. $v _ { n , m }$ is set to 0.0001. The maximum payment $p ^ { m a x }$ is set to 100, and we uniformly discretize the payment space based on its dimensions for the DQN algorithm. In the QNN of QCED n, the number of quantum gates $\hat { N } _ { 1 } , \ \hat { N } _ { 2 } .$ , and $\hat { N } _ { 3 }$ is set to 20, 10, and 5, respectively, while the number of hidden layers $L _ { n } ^ { \mathrm { Q N N } }$ is set to 3 [49]. According to [29], [50], [51], and [52], Table I lists the key parameters used in the simulation. The performance of our proposed scheme is assessed by making comparisons with the following schemes:

<!-- image-->  
Fig. 4. Trust degrees on three types of QECDs.

â¢ Incentive without trust scheme [29]. In this scheme, the UAV incentivizes all QECDs to participate in model training without implementing trust management.

â¢ The random scheme [53]. In this scheme, each UAV randomly determines its payment to incentivize the QECDs to participate in the QFL task.

â¢ Fixed payment scheme [54]. In this scheme, the UAV incentivizes all QECDs with fixed payment.

## B. Simulation Results

To evaluate the trust degrees of the QECDs, three types of QECDs are considered: high-quality QECDs, malicious QECDs, and neutral QECDs. Both high-quality QECDs and neutral QECDs are honest QECDs. High-quality QECDs are likely to provide high-quality model update parameters, malicious QECDs tend to provide low-quality or false model update parameters with high probability, and neutral QECDs sometimes provide high-quality and sometimes low-quality model update parameters. The initial trust degrees of all QECDs are set to 0.5. Fig. 4 shows the changes in trust degrees for the three types of QECDs as the number of QFL tasks executed ranges from 0 to 15. From Fig. 4, it can be seen that the trust degree of the high-quality QECD gradually rises to a relatively stable value, the trust degree of the malicious QECD gradually declines to a relatively stable value, and the trust degree of the neutral QECD fluctuates less and gradually stabilizes. The reason is that the highquality QECD consistently provides high-quality model update parameters during the QFL tasks it participates in, causing its trust degree to rise. In contrast, the malicious QECD consistently provides low-quality model update parameters during the QFL tasks it participates in, causing its trust degree to decline. The neutral QECD alternates between providing high-quality and low-quality model update parameters, resulting in smaller fluctuations in its trust degree. Thus, it can be seen that the proposed trust assessment mechanism can effectively evaluate the trust degrees of the three types of QECDs based on their historical behaviors during QFL tasks. This allows for the selection of required QECDs by setting trust thresholds according to the quality requirements of the UAVs.

<!-- image-->  
Fig. 5. Trust degrees of a QECD under different threshold $Q _ { h , g } ^ { \mathrm { T h r e } }$

Fig. 5 shows that the trust degree of a QECD changes with the number of executed QFL tasks under different values of $Q _ { h , g } ^ { \mathrm { T h r e } }$ , ranging from 0 to 15. The figure illustrates that when the value of $Q _ { h , g } ^ { \mathrm { T h r e } }$ is 0.2 or 0.4, the trust degree of the QECD gradually decreases as the number of QFL tasks increases. Conversely, when the value of $Q _ { h , g } ^ { \mathrm { T h r e } }$ is 0.6 or 0.8, the trust degree of the QECD gradually increases with the number of QFL tasks. This is because a smaller threshold value raises the standard for judging the model update parameters of the QECD as high quality, making it easier for the model parameters to be considered low quality, thus leading to a decrease in the trust degree. On the other hand, a larger threshold value lowers the standard for judging the model update parameters as high quality, making it easier for the model parameters to be considered high quality, thereby leading to an increase in the trust degree.

Fig. 6 shows the average utility of UAV with different numbers of QECDs and qubits, where the number of qubits in each QECD varies from 32 to 156. $Q ^ { \mathrm { L o c } }$ is set to 128. From Fig. 6, we can see that the average utility of UAVs increases with the number of qubits, when the number of qubits is less than $Q ^ { \mathrm { L o c } }$ . When the number of qubits in the QECD exceeds $Q ^ { \mathrm { L o c } }$ , the utility of a UAV grows slowly. This is because, according to (18), when the number of qubits is less than $Q ^ { \mathrm { L o c } }$ , the QECD needs to execute multiple unit gate circuits to complete the training task. Increasing the number of qubits will reduce the QECDâs local model training latency, leading to higher utility of the UAV. However, when the number of qubits exceeds QLoc, the performance improvement is limited due to the excess capacity.

<!-- image-->  
Fig. 6. Average utility of UAVs with different numbers of QECDs and qubits.

<!-- image-->  
Fig. 7. Convergence performance of the proposed DQN algorithm.

Fig. 7 shows the convergence performance of the proposed DQN algorithm with different learning rates and the last L steps. As shown in Fig. 7, the proposed algorithm converges to a stable state as the number of episodes increases. On the other hand, keeping L constant, increasing the learning rate can accelerate the convergence speed, but a larger learning rate may cause instability in the training process. Furthermore, it can be observed that the convergence speed and average reward can be further improved as L increases. This is because as L increases, the UAV has more historical experience to learn from, thereby improving learning efficiency. However, a larger L results in higher computational complexity and may include more ineffective strategies, potentially affecting the quality of training.

Fig. 8 shows the change in model accuracy of a QFL task with the number of QECDs under four different schemes. From the figure, it can be seen that the proposed scheme achieves the highest accuracy compared to the other schemes. This is because, in the proposed scheme, honest QECDs are first selected through a trust evaluation mechanism, and then an incentive mechanism based on Stackelberg games encourages these honest QECDs to provide high-quality local model updates, resulting in high model accuracy. In the incentive without trust scheme, malicious QECDs are not filtered out, and their low-quality model update parameters are aggregated, leading to lower accuracy. In the random scheme and the fixed scheme, there is no trust mechanism to select honest QECDs. The random scheme and the fixed payment scheme limit the proactivity of QECDs in participating in the QFL task, resulting in suboptimal model parameter updates and lower model accuracy. Additionally, as the number of QECDs increases, the accuracy in all four schemes gradually rises. This is because, in the three schemes other than the random scheme, more QECDs mean more training data and more model update parameters aggregation, enhancing the accuracy of the trained model.

<!-- image-->  
Fig. 8. The comparison of the proposed scheme with conventional scheme on model accuracy.

<!-- image-->  
Fig. 9. The comparison of the proposed scheme with conventional scheme on the average utility of UAVs.

Fig. 9 and Fig. 10 show the average utility comparison of UAVs and QECDs under different schemes, with the number of QECDs varying from 3 to 15. It can be observed that the proposed scheme achieves higher utility compared to other schemes. In the incentive without trust scheme, malicious QECDs degrade the quality of the global model, reducing overall utility. The fixed payment scheme does not comprehensively consider the computational capacity of QECDs, leading to high-capacity QECDs being less motivated to participate in model training due to lower payments. Additionally, this scheme cannot eliminate malicious QECDs, further reducing utility. In our proposed scheme, malicious QECDs are first eliminated through the trust management mechanism. By utilizing the DQN algorithm, the optimal payment strategy and the corresponding training strategy for QECDs are obtained, maximizing their utilities.

<!-- image-->  
Fig. 10. The comparison of the proposed scheme with conventional schemes on average utility of QECDS.

In summary, the simulation results illustrate that integrating a trust assessment mechanism with a Stackelberg game-based incentive strategy substantially improves the performance and reliability of QFL services. The trust mechanism effectively identifies and filters out malicious QECDs, enabling UAVs to collaborate with trustworthy QECDs. Concurrently, the incentive mechanism encourages honest QECDs to contribute high-quality model updates, resulting in enhanced global model accuracy and greater system utility. These results highlight the significance of combining trust management with incentive mechanisms for QFL services. By ensuring the selection of trustworthy participants and motivating high-quality contributions, the proposed scheme effectively addresses critical challenges, such as security threats and selfish behaviors.

## VII. CONCLUSION

In this paper, we have proposed a novel trust-enhanced incentive scheme for QFL in UAV-assisted wireless networks. First, we have developed a QECD-empowered QFL framework in the UAV-assisted wireless networks, where the QECDs independently train local models with their private data by using the quantum computing capacities, while UAVs aggregate these trained local models to update the global model. We have then devised a Bayesian inference-based trust assessment mechanism, involving direct evaluation and mutual recommendation, to select honest QECDs for high-quality training services. Additionally, we have designed a Stackelberg gamebased incentive mechanism to motivate QECDsâ participation, and proved the existence of a Stackelberg equilibrium. Optimal training contribution decisions by QECDs are obtained using convex optimization methods, and optimal payment decisions are achieved through the DQN algorithm. Extensive simulations have been conducted to demonstrate that the proposed scheme achieves higher accuracy of the QFL model and greater utilities for UAVs compared to conventional schemes. For future work, we will investigate quantum communication during interactions between UAVs and QECDs in QFL.

## REFERENCES

[1] W. A. Nelson, S. R. Yeduri, A. Jha, A. Kumar, and L. R. Cenkeramaddi, âRL-based energy-efficient data transmission over hybrid BLE/LTE/Wi-Fi/LoRa UAV-assisted wireless network,â IEEE/ACM Trans. Netw., vol. 32, no. 3, pp. 1951â1966, Jun. 2024.

[2] T. Feng, L. Xie, J. Yao, and J. Xu, âUAV-enabled data collection for wireless sensor networks with distributed beamforming,â IEEE Trans. Wireless Commun., vol. 21, no. 2, pp. 1347â1361, Feb. 2022.

[3] L. Chen et al., âREDP: Reliable entanglement distribution protocol design for large-scale quantum networks,â IEEE J. Sel. Areas Commun., vol. 42, no. 7, pp. 1723â1737, Jul. 2024.

[4] W. He, Y. Wang, M. Zhou, R. Li, L. Xie, and Z. Su, âAn efficient and robust fusion positioning system based on entangled photons,â IEEE J. Sel. Areas Commun., vol. 42, no. 1, pp. 78â92, Jan. 2024.

[5] D. Ferrari, S. Carretta, and M. Amoretti, âA modular quantum compilation framework for distributed quantum computing,â IEEE Trans. Quantum Eng., vol. 4, pp. 1â13, 2023.

[6] B. Doolittle, R. T. Bromley, N. Killoran, and E. Chitambar, âVariational quantum optimization of nonlocality in noisy quantum networks,â IEEE Trans. Quantum Eng., vol. 4, pp. 1â27, 2023.

[7] A. S. Cacciapuoti, M. Caleffi, F. Tafuri, F. S. Cataliotti, S. Gherardini, and G. Bianchi, âQuantum Internet: Networking challenges in distributed quantum computing,â IEEE Netw., vol. 34, no. 1, pp. 137â143, Jan. 2020.

[8] M. Benedetti, E. Lloyd, S. Sack, and M. Fiorentini, âParameterized quantum circuits as machine learning models,â Quantum Sci. Technol., vol. 4, no. 4, Nov. 2019, Art. no. 043001.

[9] F. Bova, A. Goldfarb, and R. G. Melko, âCommercial applications of quantum computing,â EPJ Quantum Technol., vol. 8, no. 1, p. 2, Dec. 2021.

[10] T. Wang, P. Li, Y. Wu, L. Qian, Z. Su, and R. Lu, âQuantum-empowered federated learning in space-air-ground integrated networks,â IEEE Netw., vol. 38, no. 1, pp. 96â103, Jan. 2024.

[11] M. Xu et al., âQuantum-secured space-air-ground integrated networks: Concept, framework, and case study,â IEEE Wireless Commun., vol. 30, no. 6, pp. 136â143, Dec. 2023.

[12] Z. Li et al., âEntanglement-assisted quantum networks: Mechanics, enabling technologies, challenges, and research directions,â IEEE Commun. Surveys Tuts., vol. 25, no. 4, pp. 2133â2189, 4th Quart., 2023.

[13] Z. Wang et al., âAn efficient scheduling scheme of swapping and purification operations for end-to-end entanglement distribution in quantum networks,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 1, pp. 380â391, Jan. 2024.

[14] B. Narottama and S. Y. Shin, âFederated quantum neural network with quantum teleportation for resource optimization in future wireless communication,â IEEE Trans. Veh. Technol., vol. 72, no. 11, pp. 14717â14733, Nov. 2023.

[15] M. Xu et al., âPrivacy-preserving intelligent resource allocation for federated edge learning in quantum Internet,â IEEE J. Sel. Top Signal Proces, vol. 17, no. 1, pp. 142â157, Jan. 2023.

[16] C. Ren et al., âQFDSA: A quantum-secured federated learning system for smart grid dynamic security assessment,â IEEE Internet Things J., vol. 11, no. 5, pp. 8414â8426, Mar. 2024.

[17] D. Namakshenas, A. Yazdinejad, A. Dehghantanha, and G. Srivastava, âFederated quantum-based privacy-preserving threat detection model for consumer Internet of Things,â IEEE Trans. Consum. Electron., vol. 70, no. 3, pp. 5829â5838, Aug. 2024.

[18] P. Wang et al., âServer-initiated federated unlearning to eliminate impacts of low-quality data,â IEEE Trans. Services Comput., vol. 17, no. 3, pp. 1196â1211, May 2024.

[19] X. Wang, Y. Zhao, C. Qiu, Z. Liu, J. Nie, and V. C. M. Leung, âInFEDge: A blockchain-based incentive mechanism in hierarchical federated learning for end-edge-cloud communications,â IEEE J. Sel. Areas Commun., vol. 40, no. 12, pp. 3325â3342, Dec. 2022.

[20] J. Lu, B. Pan, A. M. Seid, B. Li, G. Hu, and S. Wan, âTruthful incentive mechanism design via internalizing externalities and LP relaxation for vertical federated learning,â IEEE Trans. Computat. Social Syst., vol. 10, no. 6, pp. 2909â2923, Jun. 2023.

[21] L. Liu, J. Feng, C. Wu, C. Chen, and Q. Pei, âReputation management for consensus mechanism in vehicular edge metaverse,â IEEE J. Sel. Areas Commun., vol. 42, no. 4, pp. 919â932, Apr. 2024.

[22] Y. Zhan, J. Zhang, Z. Hong, L. Wu, P. Li, and S. Guo, âA survey of incentive mechanism design for federated learning,â IEEE Trans. Emerg. Top. Comput., vol. 10, no. 2, pp. 1035â1044, Mar. 2022.

[23] J. Huang et al., âIncentive mechanism design of federated learning for recommendation systems in MEC,â IEEE Trans. Consum. Electron., vol. 70, no. 1, pp. 2596â2607, Feb. 2024.

[24] Z. Wei, Q. Pei, N. Zhang, X. Liu, C. Wu, and A. Taherkordi, âLightweight federated learning for large-scale IoT devices with privacy guarantee,â IEEE Internet Things J., vol. 10, no. 4, pp. 3179â3191, Feb. 2023.

[25] L. Chen et al., âQ-DDCA: Decentralized dynamic congestion avoid routing in large-scale quantum networks,â IEEE/ACM Trans. Netw., vol. 32, no. 1, pp. 368â381, Feb. 2023.

[26] W. Sun, S. Lian, H. Zhang, and Y. Zhang, âLightweight digital twin and federated learning with distributed incentive in air-ground 6G networks,â IEEE Trans. Netw. Sci. Eng., vol. 10, no. 3, pp. 1214â1227, May/Jun. 2023.

[27] M. Fu, Y. Shi, and Y. Zhou, âFederated learning via unmanned aerial vehicle,â IEEE Trans. Wireless Commun., vol. 23, no. 4, pp. 2884â2900, Apr. 2024.

[28] X. Xu, G. Feng, S. Qin, Y. Liu, and Y. Sun, âJoint UAV deployment and resource allocation: A personalized federated deep reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 73, no. 3, pp. 4005â4018, Mar. 2024.

[29] W. He, H. Yao, T. Mai, F. Wang, and M. Guizani, âThree-stage Stackelberg game enabled clustered federated learning in heterogeneous UAV swarms,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 9366â9380, Jul. 2023.

[30] R. Huang, X. Tan, and Q. Xu, âQuantum federated learning with decentralized data,â IEEE J. Sel. Topics Quantum Electron., vol. 28, no. 4, pp. 1â10, Jul. 2022.

[31] W. Yamany, N. Moustafa, and B. Turnbull, âOQFL: An optimized quantum-based federated learning framework for defending against adversarial attacks in intelligent transportation systems,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 1, pp. 893â903, Jan. 2023.

[32] S. Park, S. Jung, and J. Kim, âDynamic quantum federated learning for satellite-ground integrated systems using slimmable quantum neural networks,â IEEE Access, vol. 12, pp. 58239â58247, 2024.

[33] Y. Zhan, P. Li, Z. Qu, D. Zeng, and S. Guo, âA learning-based incentive mechanism for federated learning,â IEEE Internet Things J., vol. 7, no. 7, pp. 6360â6368, Jul. 2020.

[34] J. Kang, Z. Xiong, D. Niyato, S. Xie, and J. Zhang, âIncentive mechanism for reliable federated learning: A joint optimization approach to combining reputation and contract theory,â IEEE Internet Things J., vol. 6, no. 6, pp. 10700â10714, Dec. 2019.

[35] Y. Xu, M. Xiao, H. Tan, A. Liu, G. Gao, and Z. Yan, âIncentive mechanism for differentially private federated learning in industrial Internet of Things,â IEEE Trans. Ind. Informat., vol. 18, no. 10, pp. 6927â6939, Oct. 2022.

[36] N. Ding, Z. Fang, and J. Huang, âOptimal contract design for efficient federated learning with multi-dimensional private information,â IEEE J. Sel. Areas Commun., vol. 39, no. 1, pp. 186â200, Jan. 2021.

[37] Z. Li et al., âSwapping-based entanglement routing design for congestion mitigation in quantum networks,â IEEE Trans. Netw. Service Manage., vol. 20, no. 12, pp. 3999â4012, Dec. 2023.

[38] Z. Yang, M. Zolanvari, and R. Jain, âA survey of important issues in quantum computing and communications,â IEEE Commun. Surveys Tuts., vol. 25, no. 2, pp. 1059â1094, 2nd Quart., 2023.

[39] J. Han et al., âEdAR: An experience-driven multipath scheduler for seamless handoff in mobile networks,â IEEE Trans. Wireless Commun., vol. 22, no. 10, pp. 6839â6852, Oct. 2023.

[40] J. Li et al., âFidelity-guaranteed entanglement routing in quantum networks,â IEEE Trans. Commun., vol. 70, no. 10, pp. 6748â6763, Oct. 2022.

[41] N. Delfosse, B. W. Reichardt, and K. M. Svore, âBeyond singleshot fault-tolerant quantum error correction,â IEEE Trans. Inf. Theory, vol. 68, no. 1, pp. 287â301, Jan. 2022.

[42] K. Beer et al., âTraining deep quantum neural networks,â Nature Commun., vol. 11, no. 1, p. 808, Feb. 2020.

[43] M. Wang et al., âA segment-based multipath distribution method in partially-trusted relay quantum networks,â IEEE Commun. Mag., vol. 61, no. 12, pp. 184â190, Dec. 2023.

[44] Y. Wang, Z. Su, N. Zhang, and A. Benslimane, âLearning in the air: Secure federated learning for UAV-assisted crowdsensing,â IEEE Trans. Netw. Sci. Eng., vol. 8, no. 2, pp. 1055â1069, Feb. 2021.

[45] M. J. Neely, âConvergence and adaptation for utility optimal opportunistic scheduling,â IEEE/ACM Trans. Netw., vol. 27, no. 3, pp. 904â917, Jun. 2019.

[46] K. Wang, F. C. M. Lau, L. Chen, and R. Schober, âPricing mobile data offloading: A distributed market framework,â IEEE Trans. Wireless Commun., vol. 15, no. 2, pp. 913â927, Feb. 2016.

[47] M. Xu, D. Niyato, J. Kang, Z. Xiong, and M. Chen, âLearningbased sustainable multi-user computation offloading for mobile edgequantum computing,â in Proc. IEEE Int. Conf. Commun., May 2023, pp. 4045â4050.

[48] B. Schmidt and U. Lorenz, âWavePacket: A MATLAB package for numerical quantum dynamics. I: Closed quantum systems and discrete variable representations,â Comput. Phys. Commun., vol. 213, pp. 223â234, Apr. 2017.

[49] D. Ferrari, A. S. Cacciapuoti, M. Amoretti, and M. Caleffi, âCompiler design for distributed quantum computing,â IEEE Trans. Quantum Eng., vol. 2, pp. 1â20, 2021.

[50] F. Zhou, Y. Wu, R. Q. Hu, and Y. Qian, âComputation rate maximization in UAV-enabled wireless-powered mobile-edge computing systems,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1927â1941, Sep. 2018.

[51] H. Yang, J. Zhao, Z. Xiong, K.-Y. Lam, S. Sun, and L. Xiao, âPrivacy-preserving federated learning for UAV-enabled networks: Learning-based joint scheduling and resource management,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3144â3159, Oct. 2021.

[52] T. Wang, X. Huang, Y. Wu, L. Qian, B. Lin, and Z. Su, âUAV swarmassisted two-tier hierarchical federated learning,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 1, pp. 943â956, Feb. 2024.

[53] H. Wu, X. Tang, Y.-J.-A. Zhang, and L. Gao, âIncentive mechanism for federated learning with random client selection,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 2, pp. 1922â1933, Mar. 2024.

[54] L. U. Khan et al., âFederated learning for edge networks: Resource optimization and incentive mechanism,â IEEE Commun. Mag., vol. 58, no. 10, pp. 88â93, Oct. 2020.

<!-- image-->

Qichao Xu received the Ph.D. degree from the School of Mechatronic Engineering and Automation, Shanghai University, Shanghai, China, in 2019. He is currently an Associate Professor with Shanghai University. He has published more than 90 articles in some respected journals, such as IEEE TRANSAC-TIONS ON INFORMATION FORENSICS AND SECU-RITY, IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, IEEE TRANSACTIONS ON WIRELESS COMMUNICATIONS, IEEE TRANS-ACTIONS ON INDUSTRIAL INFORMATICS, and

IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY. His research interests include trust and security, the general area of wireless network architecture, the Internet of Things, vehicular networks, and resource allocation. He was a recipient of the Best Paper Award from several international conferences, including IEEE IWCMC 2022, IEEE MSN 2020, EAI MONAMI 2020, IEEE Comsoc GCCTC 2018, IEEE CyberSciTech 2017, and WiCon 2016.

<!-- image-->

Ruidong Li (Senior Member, IEEE) received the bachelorâs degree in engineering from the Department of Information Science and Electronic Engineering, Zhejiang University, Zhejiang, China, in 2001, and the masterâs and Doctor of Engineering degrees in computer science from the University of Tsukuba. He was a Senior Researcher with the National Institute of Information and Communications Technology, Japan, from April 2008 to February 2021. He is currently an Associate Professor with Kanazawa University, Japan. He has been involved in designing, implementing, evaluating, and optimizing future network architecture.

Yihao Qi is currently pursuing the Ph.D. degree with the School of Mechatronic Engineering and Automation, Shanghai University, Shanghai, China. His research interests include wireless communications, physical layer security, reconfigurable intelligent surface, and UAV networks.

<!-- image-->

<!-- image-->

Zhou Su (Senior Member, IEEE) is a Professor with Xiâan Jiaotong University. He has published technical papers, including top journals and top conferences including IEEE JSAC, IEEE/ACM ToN, IEEE TWC, IEEE INFOCOM, etc. His research interests include multimedia communication, wireless communication, network security, and network traffic. He received the Best Paper Award of International Conference IEEE AIoT2024, IEEE WCNC2023, IEEE VTC-Fall2023, IEEE ICC2020, etc. He is an Associate Editor of IEEE INTERNET

OF THINGS JOURNAL, IEEE OPEN JOURNAL OF COMPUTER SOCIETY. He is the chair of IEEE VTS Xiâan Chapter Section.  
<!-- image-->

Dongfeng Fang (Member, IEEE) received the B.S. degree in control theory and control engineering from Harbin Institute of Technology, Harbin, China, in 2009, the M.S. degree in control theory and control engineering from Shanghai University, Shanghai, China, in 2013, and the Ph.D. degree in electrical and computer engineering from the University of Nebraska-Lincoln, Lincoln, NE, USA, in 2019. She is currently an Assistant Professor with the Department of Computer Science and Software Engineering, California Polytechnic State University, San Luis Obispo, CA, USA. Her research interests include cybersecurity (wireless security, cyber-physical security, critical infrastructure security, 5G security, the IoT security, and privacy), wireless communications and networks, and public safety communications.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_2.png|page_4_img_2]]
3. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_3.png|page_4_img_3]]
4. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_4.png|page_4_img_4]]
5. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_5.png|page_4_img_5]]
6. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_6.jpeg|page_4_img_6]]
7. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_7.png|page_4_img_7]]
8. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_8.jpeg|page_4_img_8]]
9. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_9.png|page_4_img_9]]
10. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_10.png|page_4_img_10]]
11. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_11.png|page_4_img_11]]
12. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_12.png|page_4_img_12]]
13. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_13.png|page_4_img_13]]
14. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_14.png|page_4_img_14]]
15. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_15.png|page_4_img_15]]
16. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_16.jpeg|page_4_img_16]]
17. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_17.png|page_4_img_17]]
18. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_18.png|page_4_img_18]]
19. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_19.jpeg|page_4_img_19]]
20. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_20.jpeg|page_4_img_20]]
21. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_21.png|page_4_img_21]]
22. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_22.jpeg|page_4_img_22]]
23. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_23.jpeg|page_4_img_23]]
24. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_24.jpeg|page_4_img_24]]
25. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_25.png|page_4_img_25]]
26. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_26.jpeg|page_4_img_26]]
27. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_4_img_27.png|page_4_img_27]]
28. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_1.png|page_7_img_1]]
29. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_2.jpeg|page_7_img_2]]
30. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_3.png|page_7_img_3]]
31. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_4.jpeg|page_7_img_4]]
32. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_5.png|page_7_img_5]]
33. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_6.png|page_7_img_6]]
34. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_7.png|page_7_img_7]]
35. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_8.png|page_7_img_8]]
36. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_9.png|page_7_img_9]]
37. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_10.png|page_7_img_10]]
38. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_11.png|page_7_img_11]]
39. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_12.jpeg|page_7_img_12]]
40. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_13.png|page_7_img_13]]
41. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_14.jpeg|page_7_img_14]]
42. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_7_img_15.jpeg|page_7_img_15]]
43. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_11_img_1.jpeg|page_11_img_1]]
44. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_11_img_2.png|page_11_img_2]]
45. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_15_img_1.png|page_15_img_1]]
46. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_16_img_1.png|page_16_img_1]]
47. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_16_img_2.png|page_16_img_2]]
48. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_16_img_3.png|page_16_img_3]]
49. [[../extracted_images/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks/page_16_img_4.png|page_16_img_4]]

---

