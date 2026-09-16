# Deep Graph Reinforcement Learning for UAV-Enabled Multi-User Secure Communications

Xiao Tang , Member, IEEE, Kexin Zhao, Chao Shen , Senior Member, IEEE, Qinghe Du , Member, IEEE, Yichen Wang , Member, IEEE, Dusit Niyato , Fellow, IEEE, and Zhu Han , Fellow, IEEE

AbstractâWhile unmanned aerial vehicles(UAVs) with flexible mobility are envisioned to enhance physical layer security in wireless communications, the efficient security design that adapts to such high network dynamics is rather challenging. The conventional approaches extended from optimization perspectives are usually quite involved, especially when jointly considering factors in different scales such as deployment and transmission in UAV-related scenarios. In this paper, we address the UAV-enabled multi-user secure communications by proposing a deep graph reinforcement learning framework. Specifically, we reinterpret the

Received 22 November 2024; revised 27 February 2025; accepted 1 April 2025. Date of publication 8 April 2025; date of current version 6 August 2025. This work was supported in part by the National Key Research and Development Program of China under Grant 2023YFB3107400, in part by the National Natural Science Foundation of China under Grant 62271383, in part by the Guangdong Basic and Applied Basic Research Foundation under Grant 2024A1515030215, in part by the National Key Laboratory of Wireless Communications Foundation under Grant IFN20230111, in part by the Open Research Subject of State Key Laboratory of Intelligent Game under Grant ZBKF-24-04, in part by the Key Research and Development Program of Shaanxi Province under Grant 2023- GHZD-05, in part by the Innovation Capability Support Program of Shaanxi under Grant 2021TD-08, in part by the New Cornerstone Science Foundation and the Xplorer Prize, National Research Foundation, Singapore and Infocomm Media Development Authority under its Future Communications Research & Development Programme under Grant FCP-NTU-RG-2022-010 and Grant FCP-ASTAR-TG-2022-003, in part by the Singapore Ministry of Education (MOE) Tier 1 under Grant RG87/22 and Grant RG24/24, in part by the NTU Centre for Computational Technologies in Finance (NTU-CCTF) under Grant RIE2025, in part by Industry Alignment Fund-Industry Collaboration Projects (IAF-ICP) under Grant I2301E0026, in part by NSF under Grant ECCS-2302469 and Grant CMMI-2222810, and in part by the Toyota, Amazon and Japan Science and Technology Agency (JST) Adopting Sustainable Partnerships for Innovative Research Ecosystem (ASPIRE) under Grant JPMJAP2326. Recommended for acceptance by Y. Zeng. (Corresponding author: Chao Shen.)

Xiao Tang is with the School of Information and Communication Engineering, Xiâan Jiaotong University, Xiâan 710049, China, also with the Research & Development Institute, Northwestern Polytechnical University in Shenzhen, Shenzhen 518063, China, also with the National Key Laboratory of Wireless Communications, Chengdu 611731, China, and also with the State Key Laboratory of Intelligent Game, Taicang 215400, China (e-mail: tangxiao@xjtu.edu.cn).

Kexin Zhao is with the School of Electronics and Information, Northwestern Polytechinical University, Xiâan 710072, China (e-mail: zhao_kexin@mail.nwpu.edu.cn).

Chao Shen is with the Faculty of Electronics and Information Engineering, Xiâan Jiaotong University, Xiâan 710049, China (e-mail: chaoshen@mail.xjtu.edu.cn).

Qinghe Du and Yichen Wang are with the School of Information and Communication Engineering, Xiâan Jiaotong University, Xiâan 710049, China (e-mail: duqinghe@mail.xjtu.edu.cn; wangyichen0819@mail.xjtu.edu.cn).

Dusit Niyato is with the College of Computing and Data Science, Nanyang Technological University,, Singapore 639798 (e-mail: dniyato@ntu.edu.sg).

Zhu Han is with the Department of Electrical and Computer Engineering, University of Houston, Houston, TX 77004 USA, and also with the Department of Computer Science and Engineering, Kyung Hee University, Seoul 446-701, South Korea (e-mail: hanzhu22@gmail.com).

Digital Object Identifier 10.1109/TMC.2025.3558790

security beamforming as a graph neural network (GNN) learning task, where mutual interference among users is managed through the message-passing mechanism. Then, the UAV deployment is obtained through soft actor-critic reinforcement learning, where the GNN-based security beamforming is exploited to guide the deployment strategy update. Simulation results demonstrate that the proposed approach achieves near-optimal security performance and significantly enhances the efficiency of strategy determination. Moreover, the deep graph reinforcement learning framework offers a scalable solution, adaptable to various network scenarios and configurations, establishing a robust basis for information security in UAV-enabled communications.

Index TermsâPhysical layer security, unmanned aerial vehicle, graph neural network, deep reinforcement learning, scalability.

## I. INTRODUCTION

U NMANNED aerial vehicles (UAVs) have become an in-creasingly important role in future 6G networks with their rapid development and wide applications [1], [2]. The transformative capabilities in terms of coverage, flexibility, and adaptability envisioned through UAVs in wireless network necessitate a heightened need for information security [3]. In this regard, physical layer security that exploits channel characteristics for secrecy has emerged as a promising solution with low-complexity security implementation [4], [5]. The keyless operations alleviate the burden for intensive computation and key management under conventional cryptographic methods, which is particularly fascinating for UAV-enabled communications with limited resources and high dynamics [6].

Accordingly, the UAV-enabled communication with physical layer security has received wide attention with insightful results [7], [8]. In this respect, the mainstream research efforts have been devoted to the optimization-based or heuristic approaches, which, though providing effective security provisioning, often suffer from high computational demand with multi-round iterations to approach some suboptimal solutions [9]. This issue becomes remarkably challenging in UAV-enabled communications as the high dynamics of UAVs induce severely fluctuating channel conditions, where the optimization-based approaches may struggle to strive with prompt adaptation [10], [11]. Therefore, there is an urgent need for efficient physical layer security design for UAV-enabled communications to facilitate the applications across civilian and military domains.

Meanwhile, deep learning has found increasingly wide applications in wireless area recently to address the computational and scalability challenges faced by traditional methods in secure communication design [12], [13]. Deep learning models excel in capturing complex relationship and patterns, allowing for data-driven approaches for security and enabling offline training with online inference. These features are rather attractive to fit the UAV-enabled systems, where the environmental conditions and network topologies change rapidly and learning-based models can be trained to optimize the performance efficiently [14]. Specifically, for UAV-enabled multi-user secure communications, the legitimate users and eavesdroppers affect each other and the mutual interference acts the pivotal factor to be tackled. This is when graph neural networks (GNNs), as a special type of deep learning model established on graph-structure data, become particularly pertinent [15], [16]. In this context, different roles in the network along with the inherent interference are interpreted as graphs, and the message-passing mechanisms in GNNs enable to track their mutual influence and evolution. By leveraging GNN-based learning, scalable and adaptive approaches can be developed to efficiently secure the UAV-enabled networks.

Furthermore, different from infrastructure-based low-mobility communications, the flexible deployment of UAVs introduces significant dynamics. Consequently, the UAV location induced large-scale channel attenuation and the small-scale fading need to be jointly considered to achieve effective security design. In this respect, deep reinforcement learning provides an effective approach to dynamically position the UAVs, achieving the refinement of the large-scale factor to maximize the security gain [17], [18]. Unlike deep learning model, the reinforcement learning interacts with the environment to update the deployment, which accommodates the highly variable scenarios involving UAVs [19], [20]. Therefore, with combined graph and reinforcement learning techniques, we can exploit the graph structure to track the interfering user interactions, and employ the reinforcement mechanism to adapt to different network scenarios, which facilitates the effective strategy design to meet real-time security needs in dynamic network environments.

In this paper, we consider the UAV-enabled multi-user communications with physical layer security provisioning. Different from existing works, we adopt a hierarchical learning model to jointly investigate the UAV deployment and transmission beamforming to maximize the secrecy rate. The main contributions are summarized as follows:

- We consider the UAV-enabled multi-user secure communications with a joint design of deployment and transmission strategies. We then propose a layered decomposition to facilitate the analysis that, the outer layer seeks for deployment as the large-scale factor and inner layer solves beamforming as the small-scale factor, which are further combined to provide the security solution.

- We reinterpret the considered communication network as a graph structure, and establish the GNN model for security beamforming. The message passing mechanism is established to track the interference relationships among the users for efficient beamforming output. Also, the proposed GNN model features permutation equivalence property to facilitate training and generalization.

- The outer-layer UAV deployment problem is addressed using the soft actor-critic (SAC) reinforcement learning approach. The learning agent exploits the GNN-based beamforming to evaluate the rewards and interacts with the environment to achieve security-oriented deployment in changing network topologies.

Extensive numerical results validate the effectiveness of our proposal, demonstrating the near-optimal secrecy performance across various scenarios. Also, the results highlight the scalability and adaptability to cover new scenarios and the computational efficiency as compared with the baselines.

The rest of this paper is organized as follows. In Section II, we review the related work. Section III introduces the UAVenabled multi-user system model with secure communication problem formulation. Section IV discusses the GNN-based secure beamforming and Section V proposes the deep reinforcement learning-based UAV deployment. The numerical results are provided in Section VI, and finally this paper is concluded in Section VII.

## II. RELATED WORK

Information security is one of the fundamental concerns for UAV-enabled communications, for which the physical layer security technique featuring keyless operations has raised wide interest. Intuitively, we can employ the classical designs of physical layer security, such as security beamforming [21], friendly relaying [22], artificial jamming [23], statistical security [24], in the context of UAV scenarios to protect the transmissions. Different from conventional-infrastructure communications, the high mobility of UAVs provides a new dimension for secrecy and has been actively exploited to combat eavesdropping. In [25], the authors propose a UAV-aided space-air-ground communications network for information secrecy, demonstrating significant security enhancement through joint UAV deployment and resource optimization. In [26], the authors investigate the strategic deployment of UAV swarm as aerial base stations, and optimize UAV positioning, user association, and power allocation to maximize secrecy performance. In [27], the authors address the security issue for UAV edge computing, and solve energy-efficient secure offloading problems against the eavesdroppers. In [28], the authors investigate secure transmissions of aerial underlay Internet of Things systems, where the average secrecy rate is maximized by optimizing UAV trajectory and resources while considering eavesdropping uncertainty. In [29], the authors propose a robust design for UAV trajectory and artificial jamming power optimization to maximize the minimum average secrecy rate. In [30], the authors propose a secure short-packet communication system with a UAV-enabled mobile relay through joint design of coding blocklengths, transmit powers, and UAV trajectory to maximize secrecy throughput. More recently, the UAV secure communications are also jointly explored with emerging techniques for more flexible and robust designs. In [31], the authors establish the game model for the anti-eavesdropping interactions in UAV communications, where the pursuit-evasion process is undertaken towards the equilibrium to evaluate the security performance. In [32], the authors exploit reconfigurable intelligent surfaces for secured UAV communications with joint optimization of beamforming, jamming and reflection to downgrade the eavesdropping. In these studies, the UAV dynamics are jointly considered with the resources in different dimensions for security-oriented designs. Consequently, the joint investigation of factors in different aspects in UAV-enabled communications generally induces complicated optimization problems. It usually requires multi-round iterations and approximations to approach the solution, which can be operationally intricate and difficult to adapt in dynamic UAV communication scenarios.

Meanwhile, learning-based security solutions have become increasingly popular in UAV-enabled communications, with the applications of various learning model, where the deep neural networks can be employed to approximate the optimal decision makings. In [33], the authors present a framework combining optimization and deep learning for UAV-assisted wireless-powered secure communications, where the output of the trained neural network serves as the initial values with optimization-based fine-tune. In [34], the authors develop a deep learning-driven 3D robust beamforming method for secure UAV communication, achieving improved beam steering under partial channel conditions. In [35], the authors investigate the secure UAV-relaying network, the deep neural networks are exploited to assist the deployment and transmission strategies. Besides the classical deep model, the GNNs with explicit graph structure can more effectively track the mutually interacting behavior in wireless systems. In [16], the authors propose a GNN-based approach for sum-rate maximization in multi-user network, a complex residual graph attention network is established to achieve effective beamforming with fast response time and scalability. In [15], the authors introduce a GNN architecture for joint multicast and unicast beamforming, improving the system performance and scaling well to different network settings. In [36], the authors study the reflection-assisted communications and leverage a GNN architecture to construct the mapping from pilot sequences to the transmission and reflection strategies to maximize the system rate. Moreover, the deep reinforcement learning technique enables interactions with the environment and updates the policy based on the obtained reward, which allows more flexible manners to learn to adapt in UAV-enabled communications. In [37], the authors consider UAV-relay communications, where GNN-enabled link selection and reinforcement learning-based trajectory are jointly exploited to maximize the number of active users. In [38], the authors propose a GNN-empowered multi-agent reinforcement learning to manage the age of information in multi-UAV networks, with distributed UAV trajectory optimization in unknown environments. In [17], the authors propose a graph-attention-based reinforcement learning framework for UAV trajectory design and resource assignment, achieving improved convergence and optimal cumulative rewards. Based on the analysis above, we can see that the learning-based designs for UAV-enabled communications are emerging rapidly, while the security concerns remain under-explored. As GNN and reinforcement learning models are capable of representing the mutual interference and adversarial interactions underlying secure communications involving dynamic UAVs, it motivates our endeavor to leverage these techniques to achieve effective information secrecy for UAV-enabled communications.

<!-- image-->  
Fig. 1. System model.

## III. SYSTEM MODEL

We consider a UAV-enabled multi-user downlink communication system within an area denoted by , where a single ÎUAV serves as a mobile base station, transmitting confidential message to K legitimate users, denoted by ${ \mathcal { K } } = \{ 1 , 2 , \ldots , K \}$ ï¼ as shown in Fig. 1. Meanwhile the legitimate communications are subject to eavesdropping threats, for which we assume each legitimate receiver is associated with one specific wiretapper and we abuse the notation K without ambiguity. The UAV as aerial base station is equipped with N antennas, and the legitimate users and eavesdroppers are of single antenna, which establishes the multi-user multi-input single-output secure communications. This setup has been well established as the studies in [39], [40], which can be justified by associating the geographically closest adversary as the corresponding eavesdropper or adopting the strong eavesdropping assumption. Also, as shown later, our approach can be conveniently extended to other eavesdropping models. The UAV operates within the area with horizontal coordinates denoted by $\pmb { q } _ { U } = ( x _ { \mathrm { U } } , y _ { \mathrm { U } } ) \in \Lambda$ , while maintaining = ( ) Îa fixed altitude H. Meanwhile, the legitimate user-k is located with horizontal coordinates $\pmb { q } _ { k } = ( x _ { k } , y _ { k } ) \in \Lambda$ , and the corresponding eavesdropper is positioned at qE $\mathbf { \Phi } _ { , k } = ( x _ { \mathrm { E } , k } , y _ { \mathrm { E } , k } ) \in \Lambda$ = ( ) ÎIn this paper, we assume fixed ground node locations while the UAV is enabled with flexible deployment for security enhancement. The channel condition between the UAV and legitimate user-k is denoted as $h _ { k } ( q _ { U } )$ , and similarly, the channel to the corresponding eavesdropper is $h _ { \mathrm { E } , k } ( \pmb { q } _ { U } )$ , as a function of UAV location in the network.

For the UAV-enabled communications, a data signal $s _ { k }$ is transmitted to legitimate user-k with $\mathbb { E } [ | s _ { k } | ^ { 2 } ] = 1$ , by adopting a dedicated beamforming vector $\mathbf { w } _ { k } \in \mathbb { C } ^ { N }$ . Then, the transmitted signal from the UAV, denoted by $^ { x , }$ is represented as

$$
{ \pmb x } = \sum _ { k \in \mathcal K } { \pmb w } _ { k } ^ { \dagger } s _ { k } ,\tag{1}
$$

where transmit beamformer is subject to the power constraint that

$$
\sum _ { k \in \mathcal { K } } \| \pmb { w } _ { k } \| ^ { 2 } \leq P ^ { \operatorname* { m a x } } ,\tag{2}
$$

with P max being the maximum allowed power at the UAV. Accordingly, the legitimate user-k receives a signal yk that includes both the intended signal and interference from signals directed to other users, given as,

$$
y _ { k } = h _ { k } ^ { \dagger } w _ { k } s _ { k } + h _ { k } ^ { \dagger } \sum _ { l \in K \backslash \{ k \} } w _ { l } s _ { l } + n _ { k } ,\tag{3}
$$

where the last term is the Gaussian noise with $n _ { k } \sim \mathcal { C N } ( 0 , \sigma _ { 0 } ^ { 2 } )$ (0 )The received signal at eavesdropper-k is similarly obtained by replacing the channel $\{ h _ { k } \} _ { k \in \mathcal K }$ with $\{ h _ { \mathrm { E } , k } \} _ { k \in \mathcal { K } }$ , where the first term is the intended wiretap signal, and the rest corresponds to the experienced interference and noise.

Based on the transmission model, the legitimate transmission of user-k has an achievable communication rate $R _ { k }$ as

$$
R _ { k } = \log \left( 1 + \frac { | h _ { k } ^ { \dagger } w _ { k } | ^ { 2 } } { \displaystyle \sum _ { l \in { \cal K } \backslash \{ k \} } | h _ { k } ^ { \dagger } w _ { l } | ^ { 2 } + \sigma _ { 0 } ^ { 2 } } \right) .\tag{4}
$$

Similarly, the wiretap rate at the corresponding eavesdropper is obtained as

$$
R _ { \mathrm { E } , k } = \log \left( 1 + \frac { | h _ { \mathrm { E } , k } ^ { \dagger } w _ { k } | ^ { 2 } } { \displaystyle \sum _ { l \in { \cal K } \backslash \{ k \} } | h _ { \mathrm { E } , k } ^ { \dagger } w _ { l } | ^ { 2 } + \sigma _ { 0 } ^ { 2 } } \right) .\tag{5}
$$

Thus, the secrecy rate for legitimate user-k is derived as

$$
R _ { k } ^ { \mathrm { s e c } } = \left( R _ { k } - R _ { \mathrm { E } , k } \right) ^ { + } ,\tag{6}
$$

where $( \cdot ) ^ { + } = \operatorname* { m a x } ( \cdot , 0 )$ ensures non-negative secrecy rate.

( ) = max( 0)The goal of this work is to maximize the total secrecy rate across all legitimate users by jointly optimizing the beamforming vectors and the UAV deployment, which leads to the problem formulation as

$$
\operatorname* { m a x } _ { \{ { \pmb w } _ { k } \} _ { k \in \mathcal { K } } , { \pmb q } _ { U } } \quad \sum _ { k \in \mathcal { K } } R _ { k } ^ { \mathrm { s e c } }\tag{7}
$$

$$
\mathrm { s . t . } \sum _ { k \in \mathcal { K } } \| \pmb { w } _ { k } \| ^ { 2 } \leq P ^ { \operatorname* { m a x } } ,\tag{8}
$$

$$
q _ { U } \in \Lambda .\tag{9}
$$

Although the formulated problem appears straightforward, it is non-convex and thus challenging to solve in an efficient manner, particularly when considering the UAV dynamics and environment adaptation. First, the joint optimization problem involves both the UAV deployment and the beamforming vectors, interdependent in a complicated manner within the nonconvex problem. The existing proposals are mostly based on optimization that generally requires multi-round relaxations and approximations and can be quite time-consuming, especially when the dimension of the problem becomes large. Second, the UAV-enabled communications are inherently dynamic, for which traditional optimization methods often require re-solving the problem each time the environment changes. As a result, optimization-based approaches may fail to adapt quickly and thus can be unsuitable for the cases requiring prompt security decision-makings. Third, the exiting optimization-based methods typically depend on problem-specific formulations and assumptions, which limits their scalability to varying network conditions or different numbers of users and eavesdroppers. The lack of generalization hinders their practical deployment in dynamic and diverse UAV-enabled networks.

Therefore, in this work, we propose a learning-based framework to find the physical layer security solution for UAV-enabled multi-user communications. As the considered issues of deployment and beamforming are taken as the large-scale and small-scale factors in the network, respectively, we decompose the problem in a double-layer structure to tackle different factors. Specifically, the inner layer addresses the security beamforming considering fixed UAV deployment with GNN-based interpretation and training, and the outer layer determines the UAV deployment by incorporating the GNN-based beamforming under a deep reinforcement learning framework. In this respect, we exploit the GNN to approximate the complex relationships between users, eavesdroppers, and the UAV in a non-convex optimization setting, and interpret the secure beamforming problem as a graph-based learning task. Moreover, the integration of DRL allows the UAV to learn optimal positioning strategies directly through interactions with the environment, adapting to changes in network environments in real time.

## IV. GNN-BASED SECURITY BEAMFORMING

In this section, we address the inner problem as security beamforming through GNN-based learning, on condition of fixed UAV deployment at the outer layer. Accordingly, the problem is specified as

$$
\operatorname* { m a x } _ { \{ w _ { k } \} _ { k \in \mathcal K } } \quad \sum _ { k \in { \mathcal K } } R _ { k } ^ { \mathrm { s e c } }\tag{10}
$$

$$
\mathrm { s . t . } \quad \sum _ { k \in \mathcal { K } } \| \pmb { w } _ { k } \| ^ { 2 } \leq P ^ { \operatorname* { m a x } } .\tag{11}
$$

Evidently, there are complex interference among the legitimate users and eavesdroppers, which needs to be tackled properly so as to maximize the secrecy rate for each legitimate user while minimizing the information leakage to the eavesdroppers. From a learning perspective, the intended neural network is fed with the channel condition as input, and produce the corresponding security beamforming design, given by $W = \Phi ( H ; \Theta )$ , where = Î¦( ; )W , H, and Î denote the collective beamforming, channel condition, and neural network parameters, respectively. In this respect, the network parameters are trained so as to maximize the sum secrecy rate as $R ^ { \mathrm { s e c } } ( \Phi ( H ; \Theta ) , H )$ , where $R ^ { \mathrm { s e c } } =$ $\textstyle \sum _ { k \in { \mathcal { K } } } R _ { k } ^ { \mathrm { s e c } }$ (Î¦( ; ) ) =. To this end, we adopt the graph model to capture the non-Euclidean structure of physical network, and establish the GNN-based learning mechanism to obtain the security beamformer.

<!-- image-->  
Fig. 2. GNN architecture for security beamforming.

## A. GNN Architecture

To leverage GNNs for secure beamforming design, we represent the elements the UAV-enabled communication network as graph components. As we can see, the spatial and interference relationships between legitimate users, eavesdroppers, and the UAV, can be reflected through the channel condition in the network with obtained secrecy rates at the legitimate users. Accordingly, we established a graph with K nodes, and each node- $k \in \mathcal { K }$ is associated with a feature as

$$
\begin{array} { r } { z _ { k } = \left[ \mathfrak { R e } \left( h _ { k } \right) ^ { \top } , \mathfrak { I m } \left( h _ { k } \right) ^ { \top } , \mathfrak { R e } \left( h _ { \mathrm { E } , k } \right) ^ { \top } , \mathfrak { I m } \left( h _ { \mathrm { E } , k } \right) ^ { \top } \right. } \\ { \left. \mathfrak { R e } \left( e _ { k } \right) ^ { \top } , \mathfrak { I m } \left( e _ { k } \right) ^ { \top } \right] ^ { \top } , } \end{array}\tag{12}
$$

by concatenating the channel conditions of legitimate user-k and its eavesdropper, along with an additional embedding $\boldsymbol { e } _ { k } \in \mathbb { C } ^ { N }$ ï¼ with Re Â· and Im Â· denoting the real and imaginary parts ( ) ( )of complex variables, respectively. Since the network channel condition is incorporated within the collective node features, we establish the graph without explicitly considering the edge model. Here, the node feature is constructed by the locally âusefulâ information (useful for the legitimate transmission, and useful for the corresponding eavesdropper), and the interference is obtained through the further interactions among nodes. Also, the nodes are of equivalent model, which facilitates the desired permutation equivalence property during GNN-based learning as elaborated below.

With graph-based representation of the physical network, the proposed GNN architecture is constructed with D cascaded graph convolutional network (GCN) layers along with a normalization layer, as shown in Fig. 2. In each GCN layer, the consecutive operations of message generation, aggregation, and combination are conducted to implement the message-passing mechanism of GNN. In accordance with the definition of node feature, during the layered learning process, only the embedding is updated while the channel information is preserved. This is motivated by the idea to achieve improved representation of network condition during learning by preserving the channel information. Therefore, for the dth GCN layer, the input is denoted by $\{ z _ { k } ^ { ( d - 1 ) } \} _ { k \in \mathcal { K } }$ with

$$
\begin{array} { r } { z _ { k } ^ { \left( d - 1 \right) } = \left[ \Re \mathfrak { e } \left( h _ { k } \right) ^ { \top } , \mathfrak { I m } \left( h _ { k } \right) ^ { \top } , \mathfrak { R e } \left( h _ { \mathrm { E } , k } \right) ^ { \top } , \mathfrak { I m } \left( h _ { \mathrm { E } , k } \right) ^ { \top } \right. } \\ { \left. \mathfrak { R e } \left( e _ { k } ^ { \left( d - 1 \right) } \right) ^ { \top } , \mathfrak { I m } \left( e _ { k } ^ { \left( d - 1 \right) } \right) ^ { \top } \right] ^ { \top } , } \end{array}\tag{13}
$$

where $e _ { k } ^ { ( d - 1 ) }$ is the obtained embedding of node-k in the previous layer. Then, the input is fed into a linear layer for message generation, given as

$$
{ \pmb m } _ { k } ^ { ( d ) } = f _ { \mathrm { g e n } , k } ^ { ( d ) } \left( \pmb { z } _ { k } ^ { ( d ) } ; \pmb { \Theta } _ { \mathrm { g e n } , k } ^ { ( d ) } \right)\tag{14}
$$

where $m _ { k } ^ { ( d ) }$ denotes the generated message through the operation $f _ { \mathrm { g e n } , k } ^ { ( d ) }$ , implemented as a fully-connected layer with parameter $\Theta _ { \mathrm { g e n } , k } ^ { ( d ) } .$

Then, the generated messages at each node are shared with the others through aggregation and combination operations, given in a general form as

$$
\begin{array} { r l r } & { } & { { \boldsymbol { c } } _ { k } ^ { ( d ) } = f _ { \mathrm { c o m b } , k } ^ { ( d ) } \left( \boldsymbol { m } _ { k } ^ { ( d ) } , f _ { \mathrm { a g g r } , k } ^ { ( d ) } \left( \left\{ \boldsymbol { m } _ { l } ^ { ( d ) } \right\} _ { l \in N ( k ) } ; \right. \right. } \\ & { } & { \left. \left. \Theta _ { \mathrm { a g g r } , k } ^ { ( d ) } \right) ; \Theta _ { \mathrm { c o m b } , k } ^ { ( d ) } \right) } \end{array}\tag{15}
$$

where $\boldsymbol { c } _ { k } ^ { ( d ) }$ is the achived message representation after aggregation and combination functions, denoted by $f _ { \mathrm { a g g r } , k } ^ { ( d ) }$ and $f _ { \mathrm { c o m b } , k } ^ { ( d ) }$ with parameters $\Theta _ { \mathrm { a g g r } , k } ^ { ( d ) }$ and $\Theta _ { \mathrm { c o m b } , k } ^ { ( d ) } ,$ , respectively, with $\mathcal { N } ( k )$

being the set of neighbors of node-k. To ensure the scalability and generalization of proposed GNN architecture, it is critical to choose appropriate implementations of aggregation and combination [36], [41]. In this respect, the message aggregation at node-k, is conducted according to

$$
{ \pmb a } _ { k } ^ { ( d ) } = f _ { \mathrm { a g g r } , k } ^ { ( d ) } \left( \left\{ { \pmb m } _ { l } ^ { ( d ) } \right\} _ { l \in K \backslash \{ k \} } ; \Theta _ { \mathrm { a g g r } , k } ^ { ( d ) } \right) ,\tag{16}
$$

where $\pmb { a } _ { k } ^ { ( d ) }$ denotes the obtained aggregation while incorporating all other nodes as the neighbors, without loss of generality. The messages from the neighbors are processed through a neural network with parameters $\Theta _ { \mathrm { a g g r } , k } ^ { ( d ) }$ and fed into the aggregation function to get $\pmb { a } _ { k } ^ { ( d ) }$ . The aggregation function usually takes the form such as max, sum, or mean, to ensure permutation-invariant property with respect to the inputs. Here, we adopt the maximization operation due to the fact that the aggregate interference is usually dominated by the heaviest interferer. Then, the nodes combines its own message with the aggregation from others as

$$
\pmb { c } _ { k } ^ { ( d ) } = f _ { \mathrm { c o m b } , k } ^ { ( d ) } \left( \pmb { m } _ { k } ^ { ( d ) } , \pmb { a } _ { k } ^ { ( d ) } ; \pmb { \Theta } _ { \mathrm { a g g r } , k } ^ { ( d ) } \right) ,\tag{17}
$$

to reach a combined message $\boldsymbol { c } _ { k } ^ { ( d ) }$ . Here we simply concatenate the messages to preserve the representation learned in previous operations. This update process refines the node representation by integrating information from its neighbors, gradually enhancing its ability to determine optimal beamforming in response to the network interference pattern.

As the output of current layer, the combined message at each node is fed into a multilayer perceptron with output fitting the dimension of the node embedding such that

$$
\begin{array} { r } { \left[ \mathfrak { R e } \left( e _ { k } ^ { ( d ) } \right) ^ { \top } , \mathfrak { I m } \left( e _ { k } ^ { ( d ) } \right) ^ { \top } \right] ^ { \top } = f _ { \mathrm { o u t } , k } ^ { ( d ) } \left( c _ { k } ^ { ( d ) } ; \Theta _ { \mathrm { o u t } , k } ^ { ( d ) } \right) . } \end{array}\tag{18}
$$

where $f _ { \mathrm { o u t } , k } ^ { ( d ) }$ denotes the output function with network parameters $\Theta _ { \mathrm { o u t } , k } ^ { ( d ) } .$ . The obtained embedding $e _ { k } ^ { ( d ) }$ is concatenated with the channel condition to constructed the output of current layer, i.e., the input of the subsequent GCN layer, in the similar manner as (13).

For the message generation, aggregation, and combination operations introduced above as implementation of messagepassing mechanism of GNN, we can see that only the embedding of nodes are updated. In this regard, we keep the channel state information in the learning processes and thus preserve its direct influence over the update of embedding. As such, the characteristics of the network environment can be sufficiently represented in the node embedding. Meanwhile, as the embedding appears in complex-valued form (which is seen later to directly lead to the beamformer), we adopt the parametric rectified linear unit (PReLU) as the activation function in the neural network layers. This activation function has both positive and negative output, fitting the mathematical requirement of the embedding. Also, the learnable weights within PReLU improve adaptation to channel coefficient data, which may vary in a wide range since the users in a large area is connected to one single UAV. Moreover, the message-passing mechanism is repeated across multiple GCN layers, enabling each node to progressively aggregate information from the distant nodes. After D layers of message passing, the node features contain a rich representation of the network environment and interference relationships, which can be used to generate the beamforming vectors.

Finally, the obtained embedding of each node at the last layer, i.e., $\{ e _ { k } ^ { ( \bar { D } ) } \} _ { k \in \mathcal K }$ , is exploited to obtain the beamforming vector. As the beamforming is required to satisfy the power constraint in (11), the normalization operation is conducted such that

$$
{ \pmb w } _ { k } = P ^ { \mathrm { m a x } } \frac { \Re \ e ( { \pmb e } _ { k } ^ { ( D ) } ) + \Im \Im \mathrm { m } ( { \pmb e } _ { k } ^ { ( D ) } ) } { \sqrt { \sum _ { k \in K } \left\| { \pmb e } _ { k } ^ { ( D ) } \right\| ^ { 2 } } } ,\tag{19}
$$

where $\jmath$ is the imaginary unit, and $e _ { k } ^ { ( D ) }$ is the final-layer node embedding output. The obtained beamforming can then be fed into the loss function for the GNN training.

## B. Loss Function and Training

The GNN model presented above takes the reinterpreted network condition as input to produce the security beamforming so as to maximize the secrecy rate. Accordingly, we define the loss function based on the sum secrecy rate overall users as

$$
\mathsf { L } \left( \Theta \right) = - \mathbb { E } _ { H \sim \mathcal { H } } R ^ { \mathrm { s e c } } ( \Phi \left( H ; \Theta \right) , H ) ,\tag{20}
$$

where the GNN-based mapping  is established with the collected neural network parameters $\begin{array} { r } { \Theta = \{ \Theta _ { \mathrm { g e n } , k } ^ { ( d ) } , \Theta _ { \mathrm { a g g r } , k } ^ { ( d ) } , } \end{array}$ $\Theta _ { \mathrm { c o m b } , k } ^ { ( d ) } , \Theta _ { \mathrm { o u t } , k } ^ { ( d ) } \} _ { \forall d , \forall k }$ , and H is the conforming distribution of the collective channel condition over the network.

As we can see above, to facilitate the GNN implementation with respect to complex-valued channel condition and beamformer, we separate the real and imaginary parts such that the GNN can be calculated in real domain. Technically, we can reconstruct the complex-valued beamformer as (19), and obtain the secrecy rate as (6). However, in this manner, the gradients need to be calculated with respect to complex-valued variables, which incurs additional difficulties for neural network training. To this issue, we separate the real and imaginary parts of the complex-valued components in secrecy rate and introduce

$$
\begin{array} { r } { \gamma _ { k l } = [ \Re \ell ( h _ { k } ^ { \dagger } ) \quad - \Im \mathfrak { m } ( h _ { k } ^ { \dagger } ) ] [ \Re \ell ( w _ { k } ) ] } \\ { \Im \mathfrak { m } ( h _ { k } ^ { \dagger } ) \quad \Re \ell ( h _ { k } ^ { \dagger } ) \int \ d \mathbf { J } \mathfrak { m } ( w _ { k } ) ] , } \end{array}\tag{21}
$$

and similarly for $\gamma _ { \mathrm { E } , k l }$ by replacing $h _ { k }$ with $h _ { \mathrm { E } , k }$ . Then, the secrecy rate can be recast as

$$
\begin{array} { l } { { \displaystyle R _ { k } ^ { \mathrm { s e c } } = \left( \log \left( 1 + \frac { \left\| \gamma _ { k k } \right\| ^ { 2 } } { l \in K \backslash \{ k \} } \right) \right. } } \\ { { \displaystyle \left. - \log \left( 1 + \frac { \left\| \gamma _ { \mathrm { E } , k k } \right\| ^ { 2 } } { l \in K \backslash \{ k \} } \right) ^ { + } \right) ^ { + } } } \end{array}\tag{22}
$$

which can be calculated along with (21) for real-domain operations.

The GNN model is trained in an unsupervised learning framework, where each training sample includes network instances with specific user and eavesdropper distributions, UAV position, and thus channel condition. During each training iteration, the following steps are performed. First, for each network instance, the UAV-enabled network is mapped to a graph representation with node features defined before. Second, the GNN performs message passing across the graph, updating node features through multiple GCN layers to produce the final node representations, which are then mapped to the security beamformer. Third, the secrecy rate-based loss is calculated based on the generated beamforming vectors and current network channel condition. Last, the gradients of the loss function with respect to the GNN parameters are computed using back propagation method. Here, we adopt the optimizer through stochastic gradient descent, minimizing the loss and improving model performance. Based on existing studies [42], with standard assumptions on the loss function, i.e., Lipschitz gradients and bounded variance, the stochastic gradient descent converges to a stationary point with a proper learning rate. While in our model, the non-convex loss induces fluctuating gradient updates in different regions, and the graph-based massage passing introduces correlations among nodes, making it intricate for a rigorous convergence proof. However, due to the effectiveness of stochastic gradient descent approach with over-parameterization mechanism in the proposed GNN, the learning process is rather likely to converge to some high-quality local optima, as evidenced in the numerical results.

Moreover, we can conveniently verify that the proposed GNN architecture features permutation equivalence, as the message generation, aggregation, combination, and output are all conducted in permutation-equivalent manners. This property enables reuse of training samples by simply shifting the indices and thus improves the training efficiency. More importantly, the GNN with permutation equivalence property can be conveniently generalized to cover various network settings and adapts to different distributions of users and eavesdroppers.

As a further remark, the proposed GNN architecture for security beamforming can be easily extended to the different network scenarios exampled below. First, while this work focuses on the one-to-one correspondence between legitimate users and eavesdroppers, we may further consider the general multi-eavesdropper or colluding eavesdropping models. In this regard, we can preserve current GNN architecture and adopt the corresponding worst-case secrecy rate when calculating the loss function, which is further back propagated to train the neural network. Second, when the receivers are also equipped with multiple antennas, which constitutes multiple-input-multiple-output transmissions, we can introduce the receiver beamformer in the node embedding, and update the neural network accordingly to cover the more complicated transceiving cases. Finally, we may also further consider the integration of friendly jammer or reconfigurable intelligent surface. In this regard, we may introduce an additional neural network module which connects with all the existing nodes, mimicking the interactions with the jammer/reconfigurable intelligent surface to calculate the secrecy rate, and train the corresponding neural network in similar manners. These extensions highlight the flexibility of the GNN-based framework, making it adaptable to a wide range of realistic or complicated network scenarios.

## V. SAC-BASED UAV DEPLOYMENT

Based on the problem decomposition presented before, in this section, we investigate the outer-layer UAV deployment while incorporating the inner-layer GNN-based security beamforming. Accordingly, the problem is specified as

$$
\begin{array} { r l } { \underset { \pmb { q } _ { U } } { \operatorname* { m a x } } } & { { } \displaystyle \sum _ { k \in \mathcal { K } } R _ { k } ^ { \mathrm { s e c } } \left( \left\{ \pmb { h } _ { k } \left( \pmb { q } _ { U } \right) \right\} _ { k \in \mathcal { K } } , \left\{ \pmb { h } _ { \mathrm { E } , k } \left( \pmb { q } _ { U } \right) \right\} _ { k \in \mathcal { K } } \right) } \end{array}\tag{23}
$$

$$
\mathrm { s . t . } W = \Phi \left( H \left( q _ { U } \right) ; \Theta \right) ,
$$

$$
q _ { U } \in \Lambda ,\tag{24}
$$

(25)

where the constraint in (24) indicates the GNN-based beamforming, with explicit UAV deployment-based channel condition $H ( q _ { U } )$ to obtain the beamforming W . Generally, the UAV ( )deployment significantly impacts the security performance by influencing large-scale channel characteristics and spatial interference patterns. As such, the outer problem poses unique challenges due to its dynamic nature and high dimensionality, making traditional optimization approaches hardly feasible for real-time applications. Towards this issue, we adopt the soft actor-critic (SAC) reinforcement learning algorithm, which handles continuous state-action spaces and encourages efficient exploration through entropy regularization. By integrating SAC with the GNN-based inner-layer beamforming, the UAV deployment adapts dynamically to user positions and improves the system secrecy rate.

## A. UAV Deployment as a Markov Decision Process

To tackle the UAV deployment issue for secrecy rate maximization, we first recast the problem as a Markov decision process (MDP). The MDP is established over a time series denoted by $\mathcal { T } = \{ 1 , 2 , \dots , t , \dots , T \}$ , where the UAV acts as the = 1 2agent seeking for deployment optimization. Meanwhile, MDP model compromises the following components:

1) State Space: The state space S captures current UAV deployment configuration and the network environment. At time step t, the state $s ( t )$ is represented as

$$
\begin{array} { r } { \pmb { s } ( t ) = \{ ( x _ { \mathrm { U } } , y _ { \mathrm { U } } ) , \{ \pmb { h } _ { k } \} _ { k \in \mathcal { K } } , \{ \pmb { h } _ { \mathrm { E } , k } \} _ { k \in \mathcal { K } } \} , } \end{array}\tag{26}
$$

where the variables are also specified with argument of time-t yet omitted for notation simplicity.

2) Action Space: The action space A defines the set of possible movements for the UAV. At each time step, the UAV takes an action $\mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \Psi \mathbf { } \Psi \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf \Psi \mathbf { } \mathbf \Psi \mathbf { } \mathbf \Psi \Psi \mathbf \Psi \Psi \mathbf { } \mathbf \Psi \mathbf \Psi \Psi \Psi \mathbf \Psi \Psi \mathbf \Psi \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \mathbf \Psi \Psi \mathbf \Psi$ to adjust its position as

$$
\begin{array} { r } { \pmb { a } ( t ) = ( \Delta x , \Delta y ) , } \end{array}\tag{27}
$$

where $\Delta x$ and $\Delta y$ are the changes in the UAV horizontal coordinates along x- and y-axes, respectively. The action space is continuous, allowing the UAV to reach a fine-tuned deployment. At a certain time instance-t, the action $\mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \Psi \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf { } \mathbf { } \mathbf \Psi \mathbf { } \mathbf { } \mathbf \Psi \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf \Psi \Psi \mathbf { } \mathbf \Psi \mathbf { } \mathbf \Psi \mathbf { } \mathbf \Psi \mathbf { } \mathbf \mathbf \Psi \Psi \Psi \mathbf { } \mathbf \mathbf \Psi \Psi \Psi \mathbf \Psi \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \Psi \mathbf \Psi \mathbf \Psi \mathbf $ induces an updated

<!-- image-->  
Fig. 3. SAC architecture for UAV deployment.

deployment as

$$
( x _ { \mathrm { U } } ( t + 1 ) , y _ { \mathrm { U } } ( t + 1 ) ) = ( x _ { \mathrm { U } } ( t ) + \Delta x , y _ { \mathrm { U } } ( t ) + \Delta y ) .\tag{28}
$$

3) Reward Function: The reward function evaluates the quality of the UAV deployment in terms of the security performance. Accordingly, we adopt the system secrecy rate as the instantaneous reward, i.e., $r ( \pmb { s } ( t ) , \pmb { a } ( t ) ) = R ^ { \mathrm { s e c } }$ , where current ( ( ) ( )) =deployment and the GNN-based security beamformer are jointly exploited for reward calculation. Then, the UAV agent learns a policy $\pi ( \boldsymbol { a } _ { t } | \boldsymbol { s } _ { t } )$ that maximizes the expected cumulative reward as

$$
J ( \pi ) = \mathbb { E } _ { \pi } \left[ \sum _ { { t } \in { \mathcal { T } } } \eta ^ { t } r ( s ( t ) , { \pmb a } ( t ) ) \right] ,\tag{29}
$$

where $\eta \in [ 0 , 1 ]$ is the discount factor that balances immediate and long-term rewards.

## B. Soft Actor-Critic Learning Architecture

To solve the UAV deployment in the form of a MDP, we employ the SAC-based learning approach. Compared with conventional deep reinforcement learning, SAC is designed for continuous state-action spaces, where its entropy-regularized objective encourages policy exploration, leading to more robust and stable learning processes.

1) Overview of SAC Architecture: The overall architecture of the proposed SAC framework is shown in Fig. 3, which consists of three main components explained below. First, the actor network: this network with parameter Ï approximates the policy $\pi _ { \psi } ( \pmb { a } ( t ) | \pmb { s } ( t ) )$ , which outputs a probabilistic distribution over actions for a given state. As the policy is stochastic, it enables effective exploration of the action space. Second, the critic networks: there are two Q-value approximators, $Q _ { \phi _ { 1 } } ( \pmb { s } ( t ) , \pmb { a } ( t ) ,$ ï¼ and $Q _ { \phi _ { 2 } } ( \pmb { s } ( t ) , \pmb { a } ( t ) )$ , to estimate the expected cumulative reward ( ( ) ( ))of a state-action pair, with parameters $\phi _ { 1 }$ and $\phi _ { 2 }$ , respectively.

Meanwhile, there are two counterparts as the target critic networks with parameters $\hat { \phi } _ { 1 }$ and $\hat { \phi } _ { 2 } :$ , respectively, for target Qvalue as $Q _ { \hat { \phi } _ { 1 } } ( \pmb { s } ( t ) , \pmb { a } ( t ) )$ and $Q _ { \hat { \phi } _ { 2 } } ( s ( t ) , \pmb { a } ( t ) )$ . The double-critic ( ( ) ( ))  ( ( ) ( ))structure helps mitigate potential overestimation issue while training. Third, the entropy regularization: an entropy term is introduced into the policy objective to encourage exploration, given as

$$
\mathcal { E } ( \pi ( \cdot | s ( t ) ) = - \mathbb { E } _ { a ( t ) \sim \pi ( \cdot | s ( t ) ) } \left[ \log \left( \pi ( a ( t ) | s ( t ) ) \right) \right] ,\tag{30}
$$

which is calculated to promote diverse action selection for reward maximization. Accordingly, the introduced entropy term leads to the revised value functions as

$$
V ( s ) = \mathbb { E } _ { \pmb { a } \sim \pi ( \cdot | s ) } [ Q ( \pmb { s } , \pmb { a } ) - \alpha \log ( \pi ( \pmb { a } | s ) ] ,\tag{31}
$$

for an initial state s along with a temperature parameter Î± as the weight of the entropy term, and the Q-function is defined with respect to an action a as

$$
Q ( s , a ) = r ( s , a ) + \eta \mathbb { E } _ { s ^ { \prime } \sim \mathcal { P } ( \cdot \vert s , a ) } \left[ V ( s ^ { \prime } ) \right] ,\tag{32}
$$

with $\mathcal { P } ( \cdot | s , a )$ being the state transition probability due to the ( )taken action in current state.

2) Loss Functions: In accordance with components incorporated within the SAC learning architecture, the loss functions are specified as below. First, for the entropy term, the temperature parameter is tuned while learning to minimize the loss as

$$
\begin{array} { r } { \mathcal { L } ( \alpha ) = \mathbb { E } _ { \pmb { a } ( t ) \sim \pi ( \cdot | \pmb { s } ( t ) ) } \left[ - \alpha \log \pi ( \pmb { a } ( t ) | \pmb { s } ( t ) ) - \bar { \mathcal { E } } \right] , } \end{array}\tag{33}
$$

where $\bar { \mathcal { E } }$ is the target entropy that determines the degree of exploration. Second, for the critics with double Q-network structure, the networks are trained to effectively estimate the Q-value for any specific action under a given state. Thus, the predicted Q-networks are subjected to the loss functions in terms of the

Algorithm 1: SAC Learning-Based UAV Deployment.   
Input: Initial UAV position so, SAC actor Ïp,critics $Q _ { \phi _ { 1 } }$   
$Q _ { \phi _ { 2 } } ,$ ,target critics $Q _ { \hat { \phi } _ { 1 } } , Q _ { \hat { \phi } _ { 2 } }$ ,replay buffer $\mathcal { D } ,$ and   
GNN model for beamforming;   
Output: Optimized UAV policy T& and deployment s.   
1 Initialize: $\bar { \pi } _ { \psi } , Q _ { \phi _ { 1 } } , Q _ { \phi _ { 2 } } , Q _ { \hat { \phi } _ { 1 } } , Q _ { \hat { \phi } _ { 2 } } ,$ ,and D;   
2 for each episode do   
3 Reset environment and set initial state So;   
4 for each time step t do   
5 Sample an action $\begin{array} { r } { \pmb { a } ( t ) \sim \pi _ { \psi } ( \cdot | \pmb { s } ( t ) ) ; } \end{array}$   
6 Update UAV position as $\pmb { s } ( t + 1 ) = \pmb { s } ( t ) + \pmb { a } ( t ) ;$   
7 Obtain the transmit beamforming vectors $\{ w _ { k } \} _ { k \in \mathcal K }$   
using GNN model under current UAV deployment;   
8 Calculate reward $r ( s ( t ) , \pmb { a } ( t ) )$ based on the secrecy   
rate;   
9 Store the transition   
$( s ( t ) , a ( t ) , r ( s ( t ) , a ( t ) ) , s ( t + 1 ) )$ in $\mathcal { D } ;$   
10 Sample a mini-batch of transitions from $\mathcal { D } ;$   
11 Update the predicted critic networks,actor network,   
and adjust entropy temperature by minimizing the   
loss in (34), (36),and (33),respectively;   
12 Softly update target critic networks;   
13 return Optimized policy $\pi _ { \psi }$ and UAV deployment.

Bellman residual, given as

$$
\begin{array} { r } { \mathcal { L } ( \phi _ { i } ) = \mathbb { E } _ { \{ s ( t ) , { a ( t ) } , s ( t + 1 ) \} \sim \mathcal { D } } \left[ \left( Q _ { \phi _ { i } } ( s ( t ) , { a ( t ) } ) - y ( t ) \right) ^ { 2 } \right] , } \end{array}\tag{34}
$$

where the transition $\{ \pmb { s } ( t ) , \pmb { a } ( t ) , \pmb { s } ( t + 1 ) \}$ is extracted from the ( ) ( ) ( + 1)replay buffer D, and the target value y t is defined as

$$
\begin{array} { r l } & { y ( t ) = r ( s ( t ) , \pmb { a } ( t ) ) + \eta \mathbb { E } _ { \pmb { a } ( t + 1 ) \sim \pi ( \cdot | \pmb { s } ( t + 1 ) ) } } \\ & { \left[ \operatorname* { m i n } Q _ { \hat { \phi } _ { i } } ( s ( t + 1 ) , \pmb { a } ( t + 1 ) ) - \alpha \log \pi ( \pmb { a } ( t + 1 ) | \pmb { s } ( t + 1 ) ) \right] , } \end{array}\tag{35}
$$

calculated based on the target Q-networks with $i = 1 , 2$ . Third, the actor network approximates the policy of the agent to determine the probability of an action for a given state. As such, the network is updated to maximize the expected Q-value while incorporating entropy regularization as

$$
\begin{array} { r l } & { \mathcal { L } ( \psi ) = \mathbb { E } _ { s ( t ) \sim \mathcal { D } , \mathbf { a } ( t ) \sim \pi ( \cdot | s ( t ) ) } \left[ \alpha \log \pi ( \mathbf { a } ( t ) | s ( t ) ) \right. } \\ & { ~ \qquad \left. - \operatorname* { m i n } _ { i } Q _ { \phi _ { i } } ( s ( t ) , \mathbf { a } ( t ) ) \right] } \end{array}\tag{36}
$$

where the exploration (via the entropy term) and exploitation (via the Q-value) are balanced for action determination.

## C. Training Process and Algorithm

Based on the SAC-based learning framework, the neural networks are then trained for security-oriented UAV deployment. First, define the environment based on the communication scenario, and initialize the parameters for the established neural networks. Then, for each episode, the UAV as the agent interacts with the environment by sampling $\mathbf { \boldsymbol { a } } ( t ) \sim \pi ( \cdot | \mathbf { \boldsymbol { s } } ( t ) )$ and observing the next state $s ( t + 1 )$ with achieved reward $r ( s ( t ) , \pmb { a } ( t ) )$ ( + 1). Note when evaluating the reward, the GNN-( ( ) ( ))based security beamforming is exploited under current UAV deployment to calculate the system secrecy rate. The transition $( s ( t ) , \pmb { a } ( t ) , r ( \pmb { s } ( t ) , \pmb { a } ( t ) ) , \pmb { s } ( t + 1 ) )$ is obtained and stored in the ( ( ) ( ) ( ( ) ( )) ( + 1))replay buffer D. With sufficiently filled replay buffer, the actor, critic, and entropy network parameters are then updated by minimizing their respective loss functions by sampling minibatches of transitions from the replay buffer. When the predicted critic networks are periodically trained, the parameters of the corresponding target critics are updated by adopting the soft update rules. The procedures above are continued until the convergence is achieved, and the overall algorithm is summarized in Algorithm 1.

For algorithm implementation, we note that the GNN model for security beamforming is trained separately before the SAC reinforcement learning model training. The GNN is trained to compute optimal beamforming vectors by directly maximizing the secrecy rate across legitimate users. The adopted GNN structure features remarkable scalability, and thus can be conveniently generated to the cases under different network settings. Once the GNN is trained, it is integrated into the SAC learning process to serve as the inner-layer model. During SAC training, the GNN is used to compute the reward for each UAV position generated by the SAC agent, where the scalability of inner-layer GNN facilitates the evolution of deployment policy under SAC learning. This hierarchical training sequence not only simplifies the overall learning process but also enhances the stability and efficiency of the proposed framework.

Generally, the SAC algorithm optimizes a policy objective incorporating an entropy term, under standard assumptions, i.e., smoothness of the MDP and bounded rewards, SAC-based learning is guaranteed to converge [43]. While in our proposal, the instantaneous reward is approximated through the GNN, which significantly complicates the rigorous analysis on the convergence from a theoretical perspective. Accordingly, we resort to numerical evidence to validate the convergence of model training, as shown later in the simulation results. Furthermore, the complexity of the proposed deep graph reinforcement learning approach is analyzed as follows. First, the inner-layer GNN-based beamforming concerns K nodes, and each node has N features. With D GCN layers and E training epochs, 6the training complexity is $\mathcal { O } ( D E ( K ^ { 2 } + K N ^ { 2 } ) )$ due to the ( ( + ))inter-user message aggregation and the feature update operations. Accordingly, when the GNN is trained, the inference is of a complexity of $\mathcal { O } ( D ( K ^ { 2 } + K N ^ { 2 } ) )$ . Additionally, for ( ( + ))the outer-layer SAC procedure, assume there are L actor/critic layers with an average M hidden units, each step involves a network complexity of $\mathcal { O } ( L M ^ { 2 } )$ . Incorporating the GNN-( )based inference for reward calculation, the training complexity becomes $\mathcal { O } ( F ( B D ( K ^ { 2 } + K N ^ { 2 } ) + L M ^ { 2 } ) )$ , with B being ( ( ( + ) + ))the batch size and F being the total training steps. When the overall network is trained, the inference complexity becomes $\mathcal { O } ( D ( K ^ { 2 } + K N ^ { 2 } ) + L M ^ { 2 } )$

## VI. SIMULATION RESULTS

In this section, we present the simulation results to evaluate the proposed deep graph reinforcement learning approach for UAV-enabled secure communications. Specifically, we consider an area of 200 mÃ200 m, where the users are randomly distributed with a corresponding eavesdropper located about 20 m away, and the the UAV base station is initialized at the area center with a height of 100 m. There are 8 legitimate user-eavesdropper pairs, and the UAV is equipped with 8 antennas. The air-ground UAV communication channel is considered as Rician fading with a Rician factor of 10 dB, where the line-of-sight component follows the path-loss model of 30+22 d in dB, with d being log( )the distance between the transmitter and receiver [44]. The maximum transmit power is 1 W, and the noise power is $1 . 2 \times 1 0 ^ { - 1 3 }$ W. This corresponds to a typical UAV communication scenario as evaluated in may existing studies, and the settings above are used as default unless otherwise noted. Also, this is the setup to train the GNN model, which is further used to cover other scenarios without re-training. For the neural networks, we establish a GNN with 5 GCN layers. The model is trained using a learning rate of 0.005 over a maximum of 300 training episodes. For the SAC framework, the action space is defined within the interval -1,1 . [ ]The SAC model is trained with a learning rate of 0.0003 and a maximum of 500 episodes, ensuring sufficient exploration and policy convergence. A summary of the main simulation settings is provided in Table I. The exiting work on GNN-based beamforming is referenced for the hyperparameter settings of the neural networks [36], [41], which are further adjusted with trial observations to balance the convergence speed, computation efficiency, and performance.

TABLE I  
SIMULATION PARAMETERS
<table><tr><td colspan="2">Network Scenario Setings</td><td colspan="2">Neural Network Settings</td></tr><tr><td>Area Size</td><td>200 mÃ200 m</td><td>GNN Learning Rate</td><td>0.005</td></tr><tr><td>No.of Users</td><td>8</td><td>GNN Train Episodes</td><td>300</td></tr><tr><td>No.of Antennas</td><td>8</td><td>GNN Batch Size</td><td>512</td></tr><tr><td>UAV Altitude</td><td>100 m</td><td>SAC Learning Rate</td><td>0.0003</td></tr><tr><td>Rician Factor</td><td>10 dB</td><td>SAC Train Episodes</td><td>500</td></tr><tr><td>Bandwidth</td><td>1 Hz</td><td>SAC Mini-Batch Size</td><td>64</td></tr><tr><td>Power Budget</td><td>1W</td><td>SAC Buffer Size</td><td>106</td></tr><tr><td>Noise Power</td><td> $1 . 2 \times ~ 1 0 ^ { - 1 3 } \mathrm { ~ W ~ }$ </td><td>Discount Factor</td><td>0.99</td></tr></table>

For performance comparison, we consider the following benchmarks. Regarding the UAV deployment, we seek for the optimal deployment through exhaustive search, and also evaluate some heuristic deployment strategies based on the node locations. Regarding the security beamforming, we consider the optimization-based scheme in [45], which is verified with nearoptimal security performance. Also, we construct a conventional deep model with pure MLP structure to approximate the security beamforming.

## A. Convergence

We first show the convergence of the proposed deep graph reinforcement learning approach. Specifically, Fig. 4 depicts the training convergence of the inner-layer security beamforming model with fixed UAV deployment. We demonstrate the achieved loss functions along with the training procedure, where the lines in different groups corresponds to the trials for the

<!-- image-->  
Fig. 4. Convergence of GNN model training.

<!-- image-->  
Fig. 5. Convergence of GNN model under changing scenarios.

GNN model (blue shaded) and MLP model (pink shaded), respectively. For both schemes, the achieved loss downgrades rapidly, indicating the effectiveness in security beamforming optimization. Furthermore, the proposed GNN model consistently outperforms the MLP baseline, achieving significantly lower loss values as training progresses. This superior performance demonstrates the capability of GNN to effectively learn graph-structured dependencies, which are essential for capturing the interference relationships among legitimate users and eavesdroppers. However, the convergence under GNN has more evident fluctuations, this is basically due to the more complicated network structure of GNN as compared with general MLP structure.

While Fig. 4 shows the case of 8 users as the default setting, we in Fig. 5 extend the evaluation to the case with 12 users under GNN model. Particularly, we compare two approaches: re-training the GNN from scratch and applying transfer learning based on the pre-trained model for 8 users. As can be seen. The transfer learning approach achieves significantly faster convergence as compared with re-training a new model, and the achieved loss is also slightly lower in former scheme. In this regard, the transfer learning can be regarded as a fine tuning for the unseen scenario. This result demonstrates the effectiveness in adapting GNN to new scenarios by leveraging the prior knowledge, and highlights the practicality of transfer learning in GNN-based solutions for rapid adaptation to changing environments. Note the transfer learning is feasible thanks to the scalability of proposed GNN model, which is generally inapplicable under MLP structures.

<!-- image-->

Fig. 6. Convergence of SAC model training.  
<!-- image-->  
Fig. 7. Procedure to approximate the optimal deployment through SAC.

In Fig. 6, we illustrate the convergence behavior of the SAC agent during reinforcement learning, showing the achieved reward and secrecy rate while training. Overall, both metrics improve gradually as the number of training episodes increases, indicating the adaptation of the agent for the UAV deployment task. Moreover, the correlation between reward and secrecy rate underscores the effectiveness of the former in guiding the agent to improve the security performance. Accordingly, Fig. 7 illustrates the SAC learning procedure for UAV deployment for a certain trial, where the UAV starts from the area center as the initial location and gradually moves to the end position. As we also indicate the optimal deployment through exhaustive search, we can see that the learned deployment is rather close to the optimal. These results demonstrate the capability of the proposed method to approximate optimal UAV placement efficiently, and confirm the practicality of our proposal in maximizing the secrecy rate in UAV-enabled communication systems.

## B. Performance Comparison

For the performance comparison, we first show the achieved secrecy rate with different deployment strategies in Fig. 8. Here we consider the same topology with the simulation trial in Fig. 7, and evaluate the baselines by deploying the UAV at the area center, the geometric center, the circumcenter, the polygon centroid of all the user locations. As shown in Fig. 8, the proposed deep graph reinforcement learning framework achieves the highest secrecy rate compared to the baselines, where the advantage can be rather significant. This results not only validate the effectiveness of the proposed framework in optimizing UAV deployment, but also highlight the importance of flexible deployment of UAV to dynamically adapt to user and eavesdropper distributions in security provisioning.

<!-- image-->  
Fig. 8. Achieved secrecy rate under different deployment strategies.

Furthermore, we evaluate the security performance under different beamforming schemes in Fig. 9, where the proposed GNN-based beamforming is compared with the cases with optimization-based solution and MLP-based learning. Specifically, Fig. 9(a) illustrates the secrecy rate with respect to the number of users in the network. Here, we emphasize that the proposed GNN model is trained for the case with 8 users, while the results for other scenarios are directly generalized based on the trained model without retraining. As can been seen, the proposed GNN-based framework approaches the performance of the optimization-based method, while achieving significantly higher secrecy rates compared to the MLP baseline across all tested scenarios. Also, as the number of users increases, the gap between the GNN model and the optimization-based approach becomes more pronounced, which reveals the slightly downgraded representation capability of GNN in more complicated cases with heavier interference. In contrast, the MLP model struggles to model complex user interactions effectively in larger networks, and thus the overall performance is rather limited. The results reveal the generalization capability of the proposed graph-based learning scheme, which directly covers the new network scenarios without retraining or additional computation overhead. More importantly, the near-optimal performance can be also preserved in new cases, indicating that the graph structure and mutual interference among the users have been effectively learned and represented in the trained networks.

Fig. 9(b) shows the secrecy rate versus transmit power, where we train the GNN model with a transmit power of 1 W, and generalized the model to other cases. Meanwhile, Fig. 9(c) presents the secrecy rate with respect to the noise power, where we train the GNN model with noise power of $\bar { 1 } . 2 \times 1 0 ^ { - 1 3 }$ W and scale to cover other cases. The results in these two figures show the similar trend that, our proposal closely approaches the optimization-based solution, while substantially dominating the MLP baseline. Also, naturally, with higher transmit power or lower background noise, the achieved secrecy rate can be higher under all schemes. The results indicate that for interferencelimited scenarios, the inherent ability to represent the interfering relationship is critical for the neural network to interpret effective beamforming strategy. Moreover, we can conveniently generalized a trained GNN model to diverse scenarios, including variations in network size, transmit power, and noise power, with maintained near-optimal secrecy performance, verifying the scalability, adaptability, and robustness of the GNN-based framework.

<!-- image-->

<!-- image-->  
(a)Performance with respect to number of users.(b) Performance with respect to transmit power.

<!-- image-->  
(c) Performance with respect to noise power.

Fig. 9. Performance under different network scenarios. (GNN is only trained at default setting, and generalized to cover other network configurations.).  
<!-- image-->  
Fig. 10. CDF of achieved rate for different numbers of users.

In Fig. 10, we presents the cumulative distribution function (CDF) of the achieved secrecy rates for two scenarios: a trained GNN model with 8 users and a generalized GNN model applied to 12 users, which are also compared with the optimizationbased method and the MLP baseline. For the 8-user case, the achieved distribution of secrecy rate under GNN scheme closely matches that of the optimization approach, significantly outperforming the MLP baseline, which is in consistence with the results presented before. In the 12-user case, where the GNN model is generalized without retraining, the CDF curve shows that the GNN continues to perform robustly while achieving near-optimal secrecy rates. In particular, we can see that the users with relatively higher and relatively lower rate under generalized GNN model are less than those under optimization strategy, while the number of users with moderate secrecy rate is higher. This indicates that the generalized GNN model achieves a relatively more âaveragedâ performance across all users, and thus induces a slightly higher performance gap as compared with the optimum. Yet the gap is still relatively small, and thus the results validate the scalability and adaptability of the GNN-based framework.

<!-- image-->  
Fig. 11. Time consumption for different approaches.

Fig. 11 compares the computational time required by the proposed GNN-based framework, the optimization-based method, and the MLP model. As the neural network model execution can be finished rather quickly, we show the time taken for 400 runs. As expected, the GNN framework demonstrates significantly lower time consumption compared to the optimization-based method, even when executed 400 times, highlighting its computational efficiency. Moreover, as the number of users increases, the time required for the GNN model remains relatively stable, demonstrating the scalability to larger network sizes. In contrast, the time required for the optimization grows rather evidently due to its inherent computational complexity as a function of number of users. The MLP baseline also shows low time consumption but delivers inferior performance compared to the GNN, as indicated in previous results. The result confirms the practicality of the GNN-based framework for real-time applications, where efficient computation with the scalability to different numbers of users corroborate our proposal as a robust solution for UAVenabled secure multi-user communications.

As a brief summary, we can see that the proposed deep graph reinforcement learning-based approach achieves near-optimal security performance in various network scenarios, while significantly reducing the implementation complexity to support real-time applications. More importantly, the graph-based learning mechanism enables compelling scalability, allowing the capability to handle large and dynamic environments effectively.

## VII. CONCLUSION

In this work, we have proposed a deep graph reinforcement learning framework to address the physical layer security issue for UAV-enabled multi-user communication. By decomposing the problem into two layers, we have designed the GNN-based security beamforming in the inner layer and SAC-based UAV deployment in the out layer to achieve security enhancement. The results have demonstrated the effectiveness of the proposed learning framework, which achieves near-optimal secrecy performance across varying network environments with significantly higher execution efficiency. Moreover, the framework can be effectively generalized to unseen scenarios without requiring substantial retraining. These results have collectively established the proposed framework as a robust and scalable solution for secure communication in dynamic UAV-enabled multi-user networks.

## REFERENCES

[1] G. Geraci et al., âWhat will the future of UAV cellular communications be? A flight from 5G to 6G,â IEEE Commun. Surv. Tuts., vol. 24, no. 3, pp. 1304â1335, Third Quarter 2022.

[2] G. Sun et al., âGenerative AI for advanced UAV networking,â IEEE Netw., early access, Nov. 11, 2024, doi: 10.1109/MNET.2024.3494862.

[3] M. A. Khan et al., âSecurity and privacy issues and solutions for UAVs in B5G networks: A review,â IEEE Trans. Netw. Service Manag., vol. 22, no. 1, pp. 892â912, Feb. 2025.

[4] E. Illi et al., âPhysical layer security for authentication, confidentiality, and malicious node detection: A paradigm shift in securing IoT networks,â IEEE Commun. Surv. Tuts., vol. 26, no. 1, pp. 347â388, First Quarter 2024.

[5] R. Dong, B. Wang, J. Tian, T. Cheng, and D. Diao, âDeep reinforcement learning based UAV for securing mmWave communications,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 5429â5434, Apr. 2023.

[6] M. Adil, M. A. Jan, Y. Liu, H. Abulkasim, A. Farouk, and H. Song, âA systematic survey: Security threats to UAV-aided IoT applications, taxonomy, current challenges and requirements with future research directions,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 2, pp. 1437â1455, Feb. 2023.

[7] V. Hassija et al., âFast, reliable, and secure drone communication: A comprehensive survey,â IEEE Commun. Surv. Tuts., vol. 23, no. 4, pp. 2802â2832, Fourth Quarter 2021.

[8] X. Tang, Z. Xiong, L. Dong, R. Zhang, and Q. Du, âUAV-enabled aerial active RIS with learning deployment for secured wireless communications,â Chin. J. Aeronaut., 2024, doi: 10.1016/j.cja.2024.103383.

[9] M. M. Azari et al., âEvolution of non-terrestrial networks from 5G to 6G: A survey,â IEEE Commun. Surv. Tuts., vol. 24, no. 4, pp. 2633â2672, Fourth Quarter 2022.

[10] G. Sun et al., âMulti-objective optimization for multi-UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 14803â14820, Dec. 2024.

[11] X. Tang, H. Zhang, R. Zhang, D. Zhou, Y. Zhang, and Z. Han, âRobust trajectory and offloading for energy-efficient UAV edge computing in industrial Internet of Things,â IEEE Trans. Ind. Informat., vol. 20, no. 1, pp. 38â49, Jan. 2024.

[12] Z. Ma, G. Mei, and F. Piccialli, âDeep learning for secure communication in cyber-physical systems,â IEEE Internet Things Mag., vol. 5, no. 2, pp. 63â68, Jun. 2022.

[13] J. Wang et al., âGenerative AI based secure wireless sensing for ISAC networks,â 2024, arXiv:2408.11398.

[14] H. Kurunathan, H. Huang, K. Li, W. Ni, and E. Hossain, âMachine learning-aided operations and communications of unmanned aerial vehicles: A contemporary survey,â IEEE Commun. Surv. Tuts., vol. 26, no. 1, pp. 496â533, First Quarter 2024.

[15] Z. Mou, F. Gao, J. Liu, and Q. Wu, âResilient UAV swarm communications with graph convolutional neural network,â IEEE J. Sel. Areas Commun., vol. 40, no. 1, pp. 393â411, Jan. 2022.

[16] X. Zhang, H. Zhao, J. Wei, C. Yan, J. Xiong, and X. Liu, âCooperative trajectory design of multiple UAV base stations with heterogeneous graph neural networks,â IEEE Trans. Wireless Commun., vol. 22, no. 3, pp. 1495â1509, Mar. 2023.

[17] Z. Feng, D. Wu, M. Huang, and C. Yuen, âGraph-attention-based reinforcement learning for trajectory design and resource assignment in multi-UAV-assisted communication,â IEEE Internet Things J., vol. 11, no. 16, pp. 27421â27434, Aug. 2024.

[18] R. Dong, B. Wang, K. Cao, J. Tian, and T. Cheng, âSecure transmission design of RIS enabled UAV communication networks exploiting deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 73, no. 6, pp. 8404â8419, Jun. 2024.

[19] K. Li, W. Ni, X. Yuan, A. Noor, and A. Jamalipour, âDeep-graph-based reinforcement learning for joint cruise control and task offloading for aerial edge Internet of Things (Edge IoT),â IEEE Internet Things J., vol. 9, no. 21, pp. 21676â21686, Nov. 2022.

[20] J. Li et al., âCollaborative ground-space communications via evolutionary multi-objective deep reinforcement learning,â IEEE J. Sel. Areas Commun., vol. 42, no. 12, pp. 3395â3411, Dec. 2024.

[21] L. Bai, Q. Chen, T. Bai, and J. Wang, âUAV-enabled secure multiuser backscatter communications with planar array,â IEEE J. Sel. Areas Commun., vol. 40, no. 10, pp. 2946â2961, Oct. 2022.

[22] G. Sun, J. Li, A. Wang, Q. Wu, Z. Sun, and Y. Liu, âSecure and energy-efficient UAV relay communications exploiting collaborative beamforming,â IEEE Trans. Commun., vol. 70, no. 8, pp. 5401â5416, Aug. 2022.

[23] D. Diao, B. Wang, K. Cao, R. Dong, and T. Cheng, âEnhancing reliability and security of UAV-enabled NOMA communications with power allocation and aerial jamming,â IEEE Trans. Veh. Technol., vol. 71, no. 8, pp. 8662â8674, Aug. 2022.

[24] Y. Xiao, Q. Du, W. Cheng, and N. Lu, âSecure communication guarantees for diverse extended-reality applications: A unified statistical security model,â IEEE J. Sel. Topics Signal Process., vol. 17, no. 5, pp. 1007â1021, Sep. 2023.

[25] C. Han, L. Bai, T. Bai, and J. Choi, âJoint UAV deployment and power allocation for secure space-air-ground communications,â IEEE Trans. Commun., vol. 70, no. 10, pp. 6804â6818, Oct. 2022.

[26] X. A. F. Cabezas and D. P. M. Osorio, âStrategic deployment of swarm of UAVs for secure IoT networks,â IEEE Trans. Aerosp. Electron. Syst., vol. 60, no. 5, pp. 6517â6530, Oct. 2024.

[27] T. Bai, J. Wang, Y. Ren, and L. Hanzo, âEnergy-efficient computation offloading for secure UAV-edge-computing systems,â IEEE Trans. Veh. Technol., vol. 68, no. 6, pp. 6074â6087, Jun. 2019.

[28] H. Lei, H. Yang, K.-H. Park, I. S. Ansari, J. Jiang, and M.-S. Alouini, âJoint trajectory design and user scheduling for secure aerial underlay IoT systems,â IEEE Internet Things J., vol. 10, no. 15, pp. 13637â13648, Aug. 2023.

[29] Z. Liu, B. Zhu, Y. Xie, K. Ma, and X. Guan, âUAV-aided secure communication with imperfect eavesdropper location: Robust design for jamming power and trajectory,â IEEE Trans. Veh. Technol., vol. 73, no. 5, pp. 7276â7286, May 2024.

[30] M. Tatar Mamaghani, X. Zhou, N. Yang, and A. L. Swindlehurst, âSecure short-packet communications via UAV-enabled mobile relaying: Joint resource optimization and 3D trajectory design,â IEEE Trans. Wireless Commun., vol. 23, no. 7, pp. 7802â7815, Jul. 2024.

[31] H. Wu, M. Li, Q. Gao, Z. Wei, N. Zhang, and X. Tao, âEavesdropping and anti-eavesdropping game in UAV wiretap system: A differential game approach,â IEEE Trans. Wireless Commun., vol. 21, no. 11, pp. 9906â9920, Nov. 2022.

[32] X. Tang, H. He, L. Dong, L. Li, Q. Du, and Z. Han, âRobust secrecy via aerial reflection and jamming: Joint optimization of deployment and transmission,â IEEE Internet Things J., vol. 10, no. 14, pp. 12562â12576, Jul. 2023.

[33] K. Heo, W. Lee, and K. Lee, âUAV-assisted wireless-powered secure communications: Integration of optimization and deep learning,â IEEE Trans. Wireless Commun., vol. 23, no. 9, pp. 10530â10545, Sep. 2024.

[34] R. Dong, B. Wang, and K. Cao, âDeep learning driven 3D robust beamforming for secure communication of UAV systems,â IEEE Wireless Commun. Lett., vol. 10, no. 8, pp. 1643â1647, Aug. 2021.

[35] X. Tang, N. Liu, R. Zhang, and Z. Han, âDeep learning-assisted secure UAV-relaying networks with channel uncertainties,â IEEE Trans. Veh. Technol., vol. 71, no. 5, pp. 5048â5059, May 2022.

[36] T. Jiang, H. V. Cheng, and W. Yu, âLearning to reflect and to beamform for intelligent reflecting surface with implicit channel estimation,â IEEE J. Sel. Areas Commun., vol. 39, no. 7, pp. 1931â1945, Jul. 2021.

[37] Y.-J. Chen, W. Chen, and M.-L. Ku, âTrajectory design and link selection in UAV-assisted hybrid satellite-terrestrial network,â IEEE Commun. Lett., vol. 26, no. 7, pp. 1643â1647, Jul. 2022.

[38] Y. Pan, X. Wang, Z. Xu, N. Cheng, W. Xu, and J.-J. Zhang, âGNNempowered effective partial observation marl method for AoI management in multi-UAV network,â IEEE Internet Things J., vol. 11, no. 21, pp. 34541â34553, Nov. 2024.

[39] H. Niu, Z. Chu, F. Zhou, Z. Zhu, M. Zhang, and K.-K. Wong, âWeighted sum secrecy rate maximization using intelligent reflecting surface,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6170â6184, Sep. 2021.

[40] Z. Sheng, H. D. Tuan, A. A. Nasir, H. V. Poor, and E. Dutkiewicz, âPhysical layer security aided wireless interference networks in the presence of strong eavesdropper channels,â IEEE Trans. Inf. Forensics Secur., vol. 16, pp. 3228â3240, 2021.

[41] Z. Zhang, M. Tao, and Y.-F. Liu, âLearning to beamform in joint multicast and unicast transmission with imperfect CSI,â IEEE Trans. Commun., vol. 71, no. 5, pp. 2711â2723, May 2023.

[42] S. Ghadimi and G. Lan, âStochastic first- and zeroth-order methods for nonconvex stochastic programming,â SIAM J. Optim., vol. 23, pp. 2341â2368, 2013.

[43] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, âSoft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,â 2018, arXiv: 1801.01290.

[44] L. Zhou, H. Ma, Z. Yang, S. Zhou, and W. Zhang, âUnmanned aerial vehicle communications: Path-loss modeling and evaluation,â IEEE Veh. Technol. Mag., vol. 15, no. 2, pp. 121â128, Jun. 2020.

[45] E. Choi, M. Oh, J. Choi, J. Park, N. Lee, and N. Al-Dhahir, âJoint precoding and artificial noise design for MU-MIMO wiretap channels,â IEEE Trans. Commun., vol. 71, no. 3, pp. 1564â1578, Mar. 2023.

<!-- image-->  
Xiao Tang (Member, IEEE) received the BS degree in information engineering (Elite Class Named After Tsien Hsue-shen) and the PhD degree in information and communication engineering from Xiâan Jiaotong University, Xiâan, China, in 2011 and 2018, respectively. He is currently an associate professor with the School of Information and Communication Engineering, Xiâan Jiaotong University, China. His research interests include wireless networking, information security, game theory, wireless AI.  
Kexin Zhao received the BE degree in information engineering from the Nanjing University of Aeronautics and Astronautics (NUAA), Nanjing, China, in 2022. She is currently working toward the MS degree in information and communication engineering with Northwestern Polytechnical University, Xiâan, China. Her research interests include unmanned aerial vehicle communications, physical layer security and graph neural networks.

<!-- image-->

Chao Shen (Senior Member, IEEE) received the BS degree in automation and the PhD degree in control theory and control engineering from Xiâan Jiaotong University, China, in 2007 and 2014, respectively. He is currently a professor with the Faculty of Electronic and Information Engineering, Xiâan Jiaotong University. His current research interests include AI security, insider/intrusion detection, behavioral biometrics, and measurement and experimental methodology.

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

Qinghe Du (Member, IEEE) received the BS degree in information engineering and the MS degree in information and communications engineering from Xiâan Jiaotong University, China, in 2001 and 2004, respectively, and the PhD degree in computer engineering from Texas A&M University, College Station, in 2010. He is currently a professor with the School of Information and Communications Engineering, Xiâan Jiaotong University. His research interests include mobile wireless communications and networking.

Yichen Wang (Member, IEEE) received the BS degree in information engineering and the PhD degree in information and communications engineering from Xiâan Jiaotong University, China, in 2007 and 2013, respectively. From 2014 to 2015, he was a visiting scholar with the Signal and Information Group, Department of Electrical and Computer Engineering, University of Maryland, College Park, Maryland. He is currently a professor with the Information and Communications Engineering School, Xiâan Jiaotong University.

<!-- image-->

Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand, and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada. He is a professor with the College of Computing and Data Science, Nanyang Technological University, Singapore. His research interests are in the areas of mobile generative AI, edge intelligence, quantum computing and networking, and incentive mechanism design.

Zhu Han (Fellow, IEEE) received the BS degree in electronic engineering from Tsinghua University, in 1997, and the MS and PhD degrees in electrical and computer engineering from the University of Maryland, College Park, in 1999 and 2003, respectively. From 2000 to 2002, he was an R&D engineer of JDSU, Germantown, Maryland. From 2003 to 2006, he was a research associate with the University of Maryland. From 2006 to 2008, he was an assistant professor with Boise State University, Idaho. Currently, he is a John and Rebecca Moores professor with the Electrical and Computer Engineering Department as well as in the Computer Science Department with the University of Houston, Texas. His research interests include wireless resource allocation and management, wireless communications and networking, game theory, Big Data analysis, security, and smart grid. He received an NSF Career Award, in 2010, the Fred W. Ellersick Prize of the IEEE Communication Society, in 2011, the EURASIP Best Paper Award for the Journal on Advances in Signal Processing, in 2015, IEEE Leonard G. Abraham Prize in the field of Communications Systems (best paper award in IEEE JSAC), in 2016, and several best paper awards in IEEE conferences. He was an IEEE Communications Society Distinguished lecturer from 2015â2018, AAAS fellow since 2019, and ACM distinguished member since 2019. He is a 1% highly cited researcher since 2017 according to Web of Science. He is also the winner of the 2021 IEEE Kiyo Tomiyasu Award, for outstanding early to mid-career contributions to technologies holding the promise of innovative applications, with the following citation: âfor contributions to game theory and distributed management of autonomous communication networks.â

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_3_img_1.png|page_3_img_1]]
2. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_5_img_1.png|page_5_img_1]]
3. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_8_img_1.jpeg|page_8_img_1]]
4. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_14_img_1.jpeg|page_14_img_1]]
5. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_14_img_2.jpeg|page_14_img_2]]
6. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_14_img_3.jpeg|page_14_img_3]]
7. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_14_img_4.jpeg|page_14_img_4]]
8. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_14_img_5.jpeg|page_14_img_5]]
9. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_14_img_6.jpeg|page_14_img_6]]
10. [[../extracted_images/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications/page_14_img_7.jpeg|page_14_img_7]]

---

