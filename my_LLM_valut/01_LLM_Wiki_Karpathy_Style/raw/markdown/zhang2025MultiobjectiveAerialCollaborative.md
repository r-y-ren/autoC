# Multi-Objective Aerial Collaborative Secure Communication Optimization via Generative Diffusion Model-Enabled Deep Reinforcement Learning

Chuang Zhang , Geng Sun , Senior Member, IEEE, Jiahui Li , Member, IEEE, Qingqing Wu , Senior Member, IEEE, Jiacheng Wang , Dusit Niyato , Fellow, IEEE, and Yuanwei Liu , Fellow, IEEE

AbstractâDue to flexibility and low-cost, unmanned aerial vehicles (UAVs) are increasingly crucial for enhancing coverage and functionality of wireless networks. However, incorporating UAVs into next-generation wireless communication systems poses significant challenges, particularly in sustaining high-rate and longrange secure communications against eavesdropping attacks. In this work, we consider a UAV swarm-enabled secure surveillance network system, where a UAV swarm forms a virtual antenna array to transmit sensitive surveillance data to a remote base station (RBS) via collaborative beamforming (CB) so as to resist mobile eavesdroppers. Specifically, we formulate an aerial secure communication and energy efficiency multi-objective optimization problem (ASCEE-MOP) to maximize the secrecy rate of the system

Received 7 July 2024; revised 16 October 2024; accepted 15 November 2024. Date of publication 20 November 2024; date of current version 6 March 2025. This work was supported in part by the National Natural Science Foundation of China under Grant 62172186, Grant 62272194, Grant 62371289, and Grant 62471200, in part by the Science and Technology Development Plan Project of Jilin Province under Grant 20230201087GX, in part by the Youth Talent Program of Sci-Tech Think Tank of CAST and ZTE Industry-University-Institute Cooperation Funds under Grant IA20240420003, in part by the National Research Foundation, Singapore, and Infocomm Media Development Authority under its Future Communications Research & Development Programme, in part by Defence Science Organisation (DSO) National Laboratories through the AI Singapore Programme under Grant FCP-NTU-RG-2022-010 and Grant FCP-ASTAR-TG-2022-003, in part by the Singapore Ministry of Education (MOE) Tier 1 under Grant RG87/22, in part by the NTU Centre for Computational Technologies in Finance (NTU-CCTF), and in part by Seitee Pte Ltd. Recommended for acceptance by D. Yang. (Corresponding authors: Geng Sun; Jiahui Li.)

Chuang Zhang and Jiahui Li are with the College of Computer Science and Technology, Jilin University Changchun 130012, China, and also with the Key Laboratory of Symbolic Computation and Knowledge Engineering of Ministry of Education, Jilin University Changchun 130012, China (e-mail: chuangzhang1999@gmail.com; lijiahui0803@foxmail.com).

Geng Sun is with the College of Computer Science and Technology, Jilin University Changchun 130012, China, and also with the College of Computing and Data Science, Nanyang Technological University, Singapore 639798 (email: sungeng@jlu.edu.cn).

Qingqing Wu is with the Department of Electronic Engineering, Shanghai Jiao Tong University Shanghai 200240, China (e-mail: qingqingwu@sjtu.edu.cn).

Jiacheng Wang and Dusit Niyato are with the College of Computing and Data Science, Nanyang Technological University, Singapore 639798 (e-mail: jiacheng.wang@ntu.edu.sg; dniyato@ntu.edu.sg).

Yuanwei Liu is with the Department of Electrical and Electronic Engineering, The University of Hong Kong, Hong Kong (e-mail: yuanwei@hku.hk).

This article has supplementary downloadable material available at https://doi.org/10.1109/TMC.2024.3502685, provided by the authors.

Digital Object Identifier 10.1109/TMC.2024.3502685

and to minimize the flight energy consumption of the UAV swarm. To address the non-convex, NP-hard and dynamic ASCEE-MOP, we propose a generative diffusion model-enabled twin delayed deep deterministic policy gradient (GDMTD3) method. Specifically, GDMTD3 leverages an innovative application of diffusion models to determine optimal excitation current weights and position decisions of UAVs. The diffusion models can better capture the complex dynamics and the trade-off of the ASCEE-MOP, thereby yielding promising solutions. Simulation results highlight the superior performance of the proposed approach compared with traditional deployment strategies and some other deep reinforcement learning (DRL) benchmarks. Moreover, performance analysis under various parameter settings of GDMTD3 and different numbers of UAVs verifies the robustness of the proposed approach.

Index TermsâCollaborative beamforming, deep reinforcement learning, generative diffusion models, secure communications, unmanned aerial vehicle.

## I. INTRODUCTION

U NMANNED aerial vehicles (UAVs), noted for their flex-ibility and low-cost, have become increasingly pivotal ibility and low-cost, have become increasingly pivotal in various sectors, including military surveillance [1], environmental monitoring [2], and emergency response [3], etc. With the widespread deployment of the sixth generation (6G) wireless networks, UAVs are foreseen to play a crucial role in wireless networks as well as key enablers of innovative wireless applications [4]. For instance, UAVs can serve as the mobile aerial base stations [5] to support temporary and instant network coverage, which is especially valuable when the ground infrastructure is disrupted or the network capacity is insufficient to meet the demands. Moreover, UAVs can function as the aerial relays [6] for connecting the ground users to the distant base stations and extending the coverage, particularly in rural and remote areas. Furthermore, UAVs can also access the wireless network by acting as the mobile users [7], enabling them to obtain real-time data and support various applications such as precision agriculture, aerial goods delivery, and environmental monitoring.

Although the UAVs offer significant advantages in enhancing the coverage and functionality of wireless networks, integrating them into the remote secure communication system also raises some crucial challenges. On the one hand, traditional high-level encryption is computationally expensive and consumes significant resources [8], [9], which is a major limitation for UAVs with constrained processing power and battery life. On the other hand, physical layer security techniques, such as jamming resistance or frequency hopping, can provide secure communications at short range with lower computational demands [10], [11]. However, for remote operations, relying solely on a single UAV is inadequate due to both the increased vulnerability of long-range signals to interception and the limited transmission power of a single UAV, which may not be sufficient to ensure secure communications over long distances.

Collaborative beamforming (CB) has arisen as a potential solution to the above challenges [12]. Specifically, multiple UAVs can work cooperatively to construct a UAV-enabled virtual antenna array (UVAA). Compared to traditional multi-antenna UAVs, UVAA can achieve a more flexible array distribution by leveraging the mobility of each UAV element, thereby enhancing the signal strength and directivity, which not only extends the communication range but also improves the overall secrecy rate by effectively concentrating the radiated energy in the desired direction. However, there exists a fundamental trade-off between the secure communication performance and energy consumption in the UVAA system design. In particular, to achieve an optimal beam pattern and maximize the secure transmission rate, all participating UAVs need to relocate to more suitable positions and readjust their excitation current weights, causing the increasing of the energy. Moreover, the UAVs of UVAA need to continuously adjust their positions if mobile eavesdroppers exist, which further results in additional flight energy consumption. Thus, the UVAA system must be carefully designed to balance the objectives of improving the secrecy rate of the system and reducing the flight energy consumption of the UAV swarm.

Traditional optimization methods, such as convex optimization [13] and evolutionary strategies [12], have been employed to deal with the optimization problems of UVAA. However, these methods may be impractical in dynamic environments due to the mobility of eavesdroppers and time-varying channel characteristics. Deep reinforcement learning (DRL) presents a compelling alternative, offering the capability to adapt to the changing conditions. It can learn optimal strategies through interactions with the environment, eliminating the need for prior knowledge and achieving near-optimal performance. Thus, DRL has been demonstrated to have great potential in wireless network optimizations [14]. Nevertheless, standard DRL techniques may encounter challenges in representing the complex and high-dimensional action space required for the joint optimization of excitation current weights and positions of UAVs in UVAA. Specifically, traditional DRL methods typically use stacked fully-connected layers in the actor network, which may struggle to capture deeper data features [15]. As a result, these algorithms usually exhibit high variance, leading to a learned policy distribution that deviates from the true data distribution.

Recent developments in generative artificial intelligence, notably in generative diffusion models, have advanced the effective representation of complex data distributions [16]. Consequently, in this study, we delve into the combination of DRL and generative diffusion models to tackle the multi-objective optimization problem in UVAA system, aimed at countering the presence of mobile eavesdroppers. The main contributions of this paper are summarized as follows:

. UAV Swarm-enabled Secure Surveillance Network System: We propose a novel UAV swarm-enabled secure surveillance network system under the threat of mobile eavesdroppers. In this system, a UAV swarm performs CB to enhance the signal strength and directivity, thereby ensuring the secure communications between the UAV swarm and the remote base station (RBS). To the best of our knowledge, this is the first work that focuses on mobile eavesdroppers in the context of UAV-enabled CB secure communications, which is directly applicable real-world scenarios.

Multi-objective Optimization Problem Formulation: We formulate an aerial secure communication and energy efficiency multi-objective optimization problem (ASCEE-MOP), with the objective of maximizing the secrecy rate between UAV swarm and RBS while minimizing the flight energy consumption of the UAV swarm by jointly optimizing the excitation current weights and positions of UAVs. Moreover, we show that the formulated ASCEE-MOP is a non-convex, NP-hard and dynamic optimization problem involving the complex trade-off, rendering it challenging to solve using traditional convex optimization techniques and evolutionary methods.

Generative Diffusion Model-enabled DRL Approach Design: To deal with the non-convexity and dynamic nature of the formulated ASCEE-MOP, we re-formulate it as a Markov decision process, and address it by the DRL framework. Specifically, we propose a generative diffusion model-enabled twin delayed deep deterministic policy gradient (GDMTD3) method, which integrates the generative diffusion models within twin delayed deep deterministic policy gradient (TD3) algorithm. By utilizing the generation and inference capabilities of diffusion model, the proposed GDMTD3 can capture the complex probabilistic distribution more effectively in the high-dimensional action spaces.

Simulation Validation: Simulation results are provided to demonstrate the effectiveness and robustness of the proposed approach. Specifically, compared with four deployment policies and five DRL benchmarks, the proposed approach exhibits superior performance. To further verify to the robustness, we conduct the performance analysis of the proposed GDMTD3 under various parameter settings and varying numbers of UAVs.

The remainder of this paper is structured as follows. An overview of related work is provided in Section II. Section III outlines the system model. Next, the optimization problem is formulated and analyzed in Section IV. Section V details the GDMTD3 for addressing the formulated optimization problem. Simulation results are listed and discussed in Section VI, and the conclusion of the paper is presented in Section VII.

TABLE I MAJOR NOTIONS
<table><tr><td></td><td>Symbols</td><td>Definition</td><td>Symbols</td><td>Definition</td></tr><tr><td rowspan="10">Sspor eeirt</td><td>K</td><td>Set of UAV indexes,  $| { \mathcal { K } } | = K$ </td><td>WB</td><td>Coordinate of BS</td></tr><tr><td> $N$ </td><td>Total number of time slots</td><td> $\pmb q _ { k } ^ { U }$ </td><td>Coordinate of UAV k</td></tr><tr><td> $I _ { k } ^ { U }$ </td><td>Excitation current weight of UAV k</td><td> $q _ { c }$ </td><td>Coordinate of UVAA center</td></tr><tr><td> $A F$ </td><td>Array factor of UVAA</td><td> $q _ { E }$ </td><td>Coordinate of mobile eavesdropper</td></tr><tr><td> $P _ { c , S } ^ { \mathrm { L o S } } , P _ { c , E } ^ { \mathrm { L o S } }$ </td><td>LoS link probability between UVAA and BS/eavesdropper</td><td> $\mu _ { 1 } , \mu _ { 2 }$ </td><td>Excessive path loss for LoS and NLoS links</td></tr><tr><td> $g _ { c , S } , g _ { c , \mathcal { E } }$ </td><td>Channel gain between UVAA and BS/eavesdropper</td><td> $\alpha$ </td><td>Path loss exponent</td></tr><tr><td> $G _ { U , S } , G _ { U , E }$ </td><td>Antenna gain of UVAA towards BS/eavesdropper</td><td> $\sigma ^ { 2 }$ </td><td>Noise power of A2G channel</td></tr><tr><td> $R _ { U , S } , R _ { U , E }$ </td><td>Transmission rate from UVAA to BS/eavesdropper</td><td> $R _ { S E }$ </td><td>Achievable secrecy rate of A2G link</td></tr><tr><td> $v _ { k } ^ { x } , v _ { k } ^ { y } , v _ { k } ^ { z }$ </td><td>x/y/z-axis component speed of the UAV k</td><td> $P _ { \mathrm { l e v e l } } ^ { k }$ </td><td>Induced power of UAVk for level flight</td></tr><tr><td> $P _ { \mathrm { v e r t i c a l } } ^ { k }$ </td><td>Power of UAVk for vertical flight</td><td> $E$ </td><td>Energy consumption of UAV swarm</td></tr><tr><td rowspan="5">1orra</td><td> $s , s$ </td><td>State space and state vector of environment</td><td> ${ \mathcal { A } } , a$ </td><td>Action space and action vector of agent</td></tr><tr><td> $\mathcal { P }$ </td><td>State transition probability of environment</td><td> $\mathcal { R } , r$ </td><td>Reward space and reward</td></tr><tr><td> $\gamma$ </td><td>Discount factor</td><td> $d$ </td><td>Frequency of policy update</td></tr><tr><td> $\theta _ { Q _ { i } } , \theta _ { Q _ { i } } ^ { \prime }$ </td><td>Parameters of the ith critic network and target critic network</td><td> $Q ( s , a )$ </td><td>State-action value function</td></tr><tr><td> $\theta _ { d } , \theta _ { d } ^ { \prime }$ </td><td>Parameters of actor network and target actor network</td><td> $\kappa _ { \theta _ { d } } ( x _ { t } , t , \pmb { g } )$ </td><td>Mean function of diffusion reverse process</td></tr></table>

Notations: We use plain symbols to stand for scalars (e.g., $a , b )$ , bold symbols for vectors or functions $( \mathrm { e } . \mathrm { g } . , a , b )$ , and a bcalligraphic symbols for sets (e.g., A, B). - Â· - represents euclidean norm, and $\{ \cdot \} ^ { + }$ refers to max{0, Â·}. Accordingly, Table I outlines the major notions adopted in the following sections.

In this section, we discuss related works on UAV-enabled secure communications, optimization objectives in aerial secure communications, and optimization methods for aerial secure communications.

## II. RELATED WORK

## A. UAV-Enabled Aerial Secure Communications

A number of prior works have concentrated on utilizing UAVs to enhance the security performance of wireless communications. In terms of the number of UAVs, the existing works can primarily be categorized into the single UAV-enabled secure communications and multiple UAVs-enabled secure communications.

For the single UAV-enabled secure communications, Zhang et al. [17] investigated the security of both UAV-to-ground and ground-to-UAV communications to mitigate the risk posed by an stationary eavesdropper. Cheng et al. [18] introduced a secure scheme to maximize the secrecy rate of the UAV-enabled wireless relay networks with caching, where a UAV is employed to relay the data from the base station to the users, leveraging its mobility. In [19], the authors considered a secure UAV mobile edge computing system, where a legitimate UAV assists in processing large computing tasks offloaded from multiple ground users in the presence of multiple eavesdropping UAVs. Moreover, Sun et al. [20] explored UAV-enabled downlink mmWave simultaneous wireless information and power transfer (SWIPT) networks, involving two types of authorized users with different communication needs and multiple passive eavesdroppers modeled by independent homogeneous Poisson point processes.

In [21], the authors studied a UAV-enabled mobile jamming strategy to enhance the secrecy rate of ground wiretap channels.

For multiple UAVs-enabled secure communications, Cai et al. [22] explored a joint optimization strategy for the trajectory and resource allocation of the UAV communication systems. In their approach, one UAV acts as an information transmitter while another one serves as an assisting jammer to enhance the energy efficiency and security. In [23], the authors presented a dynamic role-switching strategy, where the UAVs act as data collectors or jammers based on their locations to serve multiple ground users. Hanna et al. [24] achieved the reliable beamforming by considering estimation errors and employing a Kalman filter for frequency tracking, with validation through simulations and experiments on software-defined radios and UAVs.

However, these aforementioned works focus on non-remote communication settings due to the limited energy of UAVs. Moreover, they primarily consider secure communication scenarios involving static eavesdroppers.

## B. Optimization Objectives in Aerial Secure Communications

Optimization objectives have a significant role in enhancing the performance and security of UAV-enabled secure communications. Previous research has predominantly concentrated on two aspects that are the secrecy rate and flight energy consumption of UAVs.

The secrecy rate is a key metric for measuring communication security, representing the maximum achievable confidential transmission rate in the existence of potential eavesdroppers. Several studies are dedicated to maximizing the secrecy rate in UAV-enabled secure communication systems. For example, in [25], the authors studied a secure short-packet communication system by using a UAV as the mobile relay. Specifically, they jointly optimized the coding blocklengths, transmit powers, and UAV trajectory to enhance the secrecy throughput. Fan et al. [26] proposed an iterative algorithm to optimize the UAV trajectory, transmit power, and user scheduling for achieving secure communications, addressing eavesdropper position estimation errors and ensuring user service fairness. In [27], the authors investigated an iterative suboptimal algorithm to maximize the worst average secrecy rate in the UAV-enabled networks by optimizing the UAV trajectory, transmit power, and user scheduling while considering energy constraints and security threats from external and internal eavesdroppers.

Several studies take into account the flight energy consumption of UAVs due to the limited battery capacity. For example, Gao et al. [28] aimed to minimize the energy consumption of a fixed-wing UAV under security constraints, where they jointly optimized user scheduling and UAV trajectory in a scenario with multiple colluding eavesdroppers. In [29], the authors formulated an energy consumption minimization problem subject to constraints such as users service quality and information security requirements by jointly optimizing the offloading time, CPU frequency, artificial noise, beamforming vectors, and trajectory of UAV, along with the offloading time, CPU frequency, and transmit power of each user.

However, there exists a clear trade-off between maximizing the secrecy rate and minimizing flight energy consumption, especially in UAV-enabled CB communication systems. In such systems, each individual in the UAV swarm must continuously adjust its position to enhance the directivity of UVAA. Dong et al. [30] considered a UVAA-enabled relay system, where they focused on maximizing achievable secrecy rate of downlink by jointly optimizing the beamforming vector of UVAA and bandwidth allocation. Although this process improves the security performance compared to a single UAV-enabled secure communications, it also results in the increased flight energy consumption. To deal with this trade-off, we formulate a multi-objective optimization problem that seeks to maximize the secrecy rate of system and minimize the flight energy consumption of the UAV swarm by jointly optimizing the excitation current weights and positions of UAVs.

## C. DRL for Wireless Network Optimization

To overcome the challenges in wireless network optimization, DRL methods are being increasingly applied to complex and dynamic communication systems. For example, Yang et al. [31] proposed a DRL-based framework for the dynamic resource scheduling in federated learning over time-sensitive networks, aiming to optimize the transmission reliability and the latency in industrial IoT environments. In [32], the authors introduced the reinforcement on the federated scheme, which utilized multi-agent reinforcement learning to further enhance federated learning by optimizing the device selection and resource allocation, while minimizing the energy consumption in distributed industrial IoT networks. Zhang et al. [33] integrated deterministic communication and computation through DRL to support large artificial intelligence models with minimal latency and near-zero packet loss across multiple computing domains. Moreover, Xiao et al. [34] developed a hierarchical DRL algorithm to enhance the anti-eavesdropping performance, with regard to outage probability, intercept probability, energy consumption and latency. In addition, the authors in [35] utilized a modified proximal policy optimization method to minimize the secrecy outage duration and the weighted sum of flight period by jointly optimizing the UAV trajectory, the user scheduling and the beamforming vector.

Despite the potential advantages of many DRL-based methods in dynamic environments, they still face limitations in handling the complexities and uncertainties of dynamic environments. To address this issue, our work integrates the generative diffusion model with DRL, thereby improving the ability of the algorithm to model more complex probabilistic distribution in high-dimensional action spaces.

## D. Generative Models for Wireless Network Optimization

Recent developments in generative models have demonstrated significant potential in optimizing wireless networks. For instance, Yang et al. [36] proposed a GAN-powered multi-agent reinforcement learning framework for optimizing the terminalcooperative caching and the render offloading for virtual reality tasks, addressing the trade-off among power, delay, and resource utilization. In [37], the authors proposed a novel framework that integrated generative diffusion models with DRL to enhance discrete decision-making processes in network traffic managements. Moreover, Li et al. [38] introduced a novel generative model-empowered federated learning framework, where the FIlling the MIssing (FIMI) data augmentation strategy was developed to effectively address data and resource heterogeneity problems in mobile edge networks. In [39], the authors introduced a GAN-enhanced DRL strategy for dynamic spectrum anti-jamming access in overlay cognitive radio networks, where a GAN-based decision network was introduced to avoid interference from both primary users and jammers. Furthermore, Chen et al. [40] proposed a Transformer-based deep multi-agent reinforcement learning algorithm to address the multi-UAV network area coverage problem where the transformer model was leveraged to adapt to variable input dimensions and extract important information from complex network states by using an attention mechanism.

Although the authors integrated the generative diffusion model into DRL framework in [37], this method cannot be applied to the continuous action space of the formulated ASCEE-MOP. To address this limitation, we propose the GDMTD3 approach, which tailors the generative diffusion model for continuous action spaces to meet the specific needs of ASCEE-MOP.

## III. SYSTEM MODEL

In this section, we first present a comprehensive system description. Subsequently, we delve into the details of the considered models, including the array factor, channel gain, secrecy rate, and UAV energy consumption models.

## A. System Description

As shown in Fig. 1, we consider a UAV swarm-enabled secure surveillance network system, which consists of K UAVs denoted by ${ \mathcal { K } } \triangleq \{ 1 , 2 , \dots \dots , K \}$ and one RBS denoted by S. Specifically, the UAVs have collected some sensitive surveillance data and need to transmit the data back to the RBS S by wireless links over a given time period T . For ease of exposition, the total time T is further divided into N time slots with equal duration $\delta _ { t } .$ , i.e., $T \triangleq N \delta _ { t }$ . However, due to blockage of obstacles and signal attenuation for long distance communication, a single powerconstrained UAV is not able to send data to RBS S directly. We assume that the position of the eavesdropper can be detected by cameras, radar, or advanced prediction algorithms [41], [42], [43]. Moreover, there exists a mobile eavesdropper on the ground trying to intercept the sensitive information. To enhance the transmission efficiency and resist eavesdropping attacks from the mobile eavesdropper, these UAVs will form a UVAA to perform CB and transmit data back to RBS S on the air-to-ground (A2G) link.

<!-- image-->  
Fig. 1. A UAV swarm-enabled secure surveillance network system, where a UAV swarm is deployed for surveillance tasks, transmitting sensitive data to a RBS. The security of system is challenged by a mobile eavesdropper, depicted by red dashed lines, attempting to intercept the data via wiretap links over various time slots.

Mathematically, all entities are defined within a threedimensional Cartesian coordinate system. Specifically, the RBS S is situated at a fixed point denoted by ${ \pmb w } _ { B } = ( x _ { S } , y _ { S } , H _ { S } )$ wMoreover, it is worth noting that the position change of UAVs and eavesdropper within a time slot can be negligible since the duration $\delta _ { t }$ is chosen to be sufficiently small. Thus, the 3D coordinates of UAV k and mobile eavesdropper at time slot n are denoted by $\pmb { q } _ { k } ^ { U } [ n ] = ( x _ { k } ^ { U } [ n ] , y _ { k } ^ { U } [ n ] , z _ { k } ^ { U } [ n ] )$ and ${ \pmb q } _ { E } [ n ] =$ $( x _ { E } [ n ] , y _ { E } [ n ] , 0 )$ , respectively.

## B. Array Factor Model

The virtual antenna array formed by UAV swarm can significantly improve the antenna directivity by optimizing its beam pattern. Specifically, at time slot n, the excitation current weight of UAV k is denoted as $I _ { k } ^ { U } [ n ]$ , the coordinate of UVAA center $\pmb q _ { c } [ n ] = ( x _ { c } ^ { U } [ n ] , y _ { c } ^ { U } [ n ] , z _ { c } ^ { \tilde { U } } [ \tilde { n } ] )$ , and the component distances in qthe x-axis, y-axis and z-axis between UAV k and UVAA center are represented by $d _ { c , k } ^ { x } [ n ] , d _ { c , k } ^ { y } [ n ]$ and $d _ { c , k } ^ { z } [ n ]$ , respectively. According to electromagnetic wave superposition principle, the array factor (AF) of UVAA at time slot n can be described as follows [44]:

$$
A F \left( \theta , \varphi | \theta s [ n ] , \varphi s [ n ] \right) = \sum _ { k = 1 } ^ { K } \Big ( I _ { k } ^ { U } [ n ] e ^ { \Psi _ { k } \left( \theta _ { S } [ n ] , \varphi _ { S } [ n ] \right) }
$$

$$
\cdot e ^ { j [ c _ { p } ( d _ { c , k } ^ { x } [ n ] \sin \theta \cos \varphi + d _ { c , k } ^ { y } [ n ] \sin \theta \sin \varphi + d _ { c , k } ^ { z } [ n ] \cos \theta ) ] } )\tag{1}
$$

where Î» is the wavelength, and $c _ { p } = 2 \pi / \lambda$ is the phase constant. Moreover, $\theta \in [ 0 , \pi ]$ and $\varphi \in [ - \pi , \pi ]$ are the elevation and azimuth angles, respectively. In addition, the direction of RBS $s$ with respect to UVAA $\mathbf { \Delta } q _ { c } [ n ]$ is denoted as $( \theta _ { S } [ n ] , \varphi s [ n ] )$ at time slot $n ,$ and $\Psi _ { k } ( \theta _ { \cal { S } } [ n ] , \varphi _ { \cal { S } } [ n ] )$ is the initial phase of UAV k in UVAA at time slot n.

In this work, we adopt an open-loop phase synchronization scheme [45], which can be easily implemented through UAV swarm intra-cluster communication protocols [46]. For this case, the initial phase synchronization is accomplished by offsetting the distance between the UAV and UVAA center. As a result, the initial phase of UAV k in UVAA can be calculated as follows:

$$
\begin{array} { r l } & { \Psi _ { k } \left( \theta _ { \mathcal { S } } [ n ] , \varphi _ { \mathcal { S } } [ n ] \right) = \mathrm { ~ - ~ } c _ { p } \left( d _ { c , k } ^ { x } [ n ] \sin \theta _ { \mathcal { S } } [ n ] \cos \varphi _ { \mathcal { S } } [ n ] \right. } \\ & { ~ \left. ~ + d _ { c , k } ^ { y } [ n ] \sin \theta _ { \mathcal { S } } [ n ] \sin \varphi _ { \mathcal { S } } [ n ] \right. } \\ & { ~ \left. ~ + d _ { c , k } ^ { z } [ n ] \cos \theta _ { \mathcal { S } } [ n ] \right) . } \end{array}\tag{2}
$$

## C. Channel Gain Model

To precisely model the A2G wireless communications, we utilize the elevation angle-dependent probabilistic Line-of-Sight (LoS) model [47] to characterize the A2G communication between UVAA and RBS S. Specifically, the LoS link probability between UVAA and RBS S at time slot n can be given by

$$
P _ { c , \mathcal { S } } ^ { \mathrm { L o S } } [ n ] = \frac { 1 } { 1 + c _ { 0 } \exp { ( - c _ { 1 } \left( \xi [ n ] - c _ { 0 } \right) ) } } ,\tag{3}
$$

where $c _ { 0 }$ and $c _ { 1 }$ are two constants depending on the carrier frequency and environment. As depicted in Fig. 1, Î¾[n] is the elevation between UVAA center and RBS S at time slot n and can be calculated by $\textstyle { \frac { 1 8 0 } { \pi } }$ arcsin $\big ( \frac { z _ { c } ^ { U } [ n ] - H _ { \mathcal { S } } } { d _ { c , s } [ n ] } \big )$ , wherein $d _ { c , S } [ n ] =$ $\sqrt { \| \pmb q _ { c } [ n ] - \pmb w _ { B } \| ^ { 2 } }$ is the distance between UVAA center and q wRBS S at time slot n. Accordingly, the NLoS link probability at time slot n can be expressed as $\bar { P } _ { c , S } ^ { \mathrm { N L o S } } [ n ] = 1 - \bar { P } _ { c , S } ^ { \mathrm { L o S } } [ n ]$

Thus, the path loss for LoS and NLoS links between UVAA and RBS S at time slot n can be given by [48]

$$
L _ { c , } s [ n ] = \left\{ \begin{array} { l l } { \displaystyle \mu _ { 1 } \left( \frac { 4 \pi f _ { c } d _ { c , } s [ n ] } { c } \right) ^ { \alpha } , } & { \mathrm { L o S \ l i n k } } \\ { \displaystyle \mu _ { 2 } \left( \frac { 4 \pi f _ { c } d _ { c , } s [ n ] } { c } \right) ^ { \alpha } , } & { \mathrm { N L o S \ l i n k } } \end{array} , \right.\tag{4}
$$

where $\mu _ { 1 }$ and $\mu _ { 2 } \ ( \mu _ { 2 } > \mu _ { 1 } > 1 )$ represent the excessive path loss for LoS and NLoS links, respectively. Moreover, c is the light speed, Î± is the path loss exponent, and $f _ { c }$ is the carrier frequency.

Typically, considering both LoS and NLoS links, the average pass loss between UVAA and RBS S at time slot n can be express as follows:

$$
\overline { { L } } _ { c , \mathcal { S } } [ n ] = \left[ P _ { c , \mathcal { S } } ^ { \mathrm { L o S } } [ n ] \mu _ { 1 } + P _ { c , \mathcal { S } } ^ { \mathrm { N L o S } } [ n ] \mu _ { 2 } \right] \left( K _ { o } d _ { c , \mathcal { S } } [ n ] \right) ^ { \alpha } ,\tag{5}
$$

where $\begin{array} { r } { K _ { o } = \frac { 4 \pi f _ { c } } { c } } \end{array}$ represents the free-space path loss factor. Furthermore, the channel gain between UVAA center and RBS $\boldsymbol { \mathcal { S } }$ at time slot n can be calculated as $\begin{array} { r } { g _ { c , S } [ n ] = \frac { 1 } { \overline { { L } } _ { c , S } [ n ] } } \end{array}$

Similarly, the channel gain between UVAA and mobile eavesdropper at time slot n is described as follows:

$$
g _ { c , E } [ n ] = \frac { 1 } { \left[ P _ { c , E } ^ { \mathrm { L o S } } [ n ] \mu _ { 1 } + P _ { c , E } ^ { \mathrm { N L o S } } [ n ] \mu _ { 2 } \right] \left( K _ { o } d _ { c , E } [ n ] \right) ^ { \alpha } } ,\tag{6}
$$

where $P _ { c , E } ^ { \mathrm { L o S } } [ n ]$ and $P _ { c , E } ^ { \mathrm { N L o S } } [ n ]$ represent the probabilities of LoS and NLoS links between UVAA and mobile eavesdropper at time slot n, respectively. Moreover, $d _ { c , E } [ n ]$ is the distance between UVAA center and mobile eavesdropper at time slot n, which can be calculated by $d _ { c , E } [ n ] = \sqrt { \| \pmb q _ { c } [ n ] - \pmb q _ { E } [ n ] \| ^ { 2 } }$

## D. Secrecy Rate Model

By exploiting the previously mentioned array factor and channel model, the transmission rate from UVAA to RBS at time slot n can be expressed as follows:

$$
R _ { U , \mathcal { S } } [ n ] = \log _ { 2 } \left( 1 + \frac { P _ { U } [ n ] g _ { c , \mathcal { S } } [ n ] G _ { U , \mathcal { S } } ( \theta _ { \mathcal { S } } [ n ] , \varphi _ { \mathcal { S } } [ n ] ) } { \sigma ^ { 2 } } \right) ,\tag{7}
$$

where $\begin{array} { r } { P _ { U } [ n ] = \sum _ { k = 1 } ^ { K } I _ { k } ^ { U } [ n ] P _ { k } ^ { \operatorname* { m a x } } } \end{array}$ represents the transmit power of UVAA, and $P _ { k } ^ { \mathrm { m a x } }$ is the maximum transmit power of UAV k. Moreover, $\sigma ^ { 2 }$ is the noise power of the A2G channel. Furthermore, $G _ { U , S } ( \theta _ { S } [ n ] , \varphi _ { S } [ n ] )$ is the antenna gain of UVAA towards RBS S at time slot $n ,$ which can be defined as follows:

$$
G _ { U , \mathcal { S } } ( \theta _ { \mathcal { S } } [ n ] , \varphi _ { \mathcal { S } } [ n ] ) = \frac { U ( \theta _ { \mathcal { S } } [ n ] , \varphi _ { \mathcal { S } } [ n ] ) } { U _ { 0 } [ n ] }\tag{8}
$$

where $U ( \theta _ { S } [ n ] , \varphi _ { \bar { S } } [ n ] )$ represents the normalized radiation intensity1 produced by the AF to the RBS S, which can be calculated as follows:

$$
U ( \theta _ { S } [ n ] , \varphi _ { S } [ n ] ) = 4 \pi \left| A F \left( \theta _ { S } [ n ] , \varphi _ { S } [ n ] | \theta _ { S } [ n ] , \varphi _ { S } [ n ] \right) \right| ^ { 2 }\tag{9}
$$

Moreover, $U _ { 0 } [ n ]$ represents the average radiation intensity, which can be calculated as follows:

$$
U _ { 0 } [ n ] = \frac { \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \pi } | A F ( \theta , \varphi | \theta _ { S } [ n ] , \varphi _ { S } [ n ] ) | ^ { 2 } \sin \theta \mathrm { d } \theta \mathrm { d } \varphi } { 4 \pi }\tag{10}
$$

Similarly, the antenna gain of UVAA towards the mobile eavesdropper at time slot n can be written as follows:

$$
\begin{array} { r l } & { G _ { U , E } ( \theta _ { E } [ n ] , \varphi _ { E } [ n ] ) } \\ & { \qquad = \frac { 4 \pi \vert A F ( \theta _ { E } [ n ] , \varphi _ { E } [ n ] \vert \theta _ { S } [ n ] , \varphi _ { S } [ n ] ) \vert ^ { 2 } } { \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \pi } \vert A F ( \theta , \varphi \vert \theta _ { S } [ n ] , \varphi _ { S } [ n ] ) \vert ^ { 2 } \sin \theta \mathrm { d } \theta \mathrm { d } \varphi } , } \end{array}\tag{11}
$$

where $( \theta _ { E } [ n ] , \varphi _ { E } [ n ] )$ is the direction of the mobile eavesdropper with respect to the UVAA center at time slot n. Accordingly, the transmission rate from UVAA to the mobile eavesdropper can be expressed as follows:

$$
R _ { U , E } [ n ] = \log _ { 2 } \left( 1 + \frac { P _ { U } [ n ] g _ { c , E } [ n ] G _ { U , E } ( \theta _ { S } [ n ] , \varphi _ { S } [ n ] ) } { \sigma ^ { 2 } } \right) _ { . }\tag{12}
$$

Furthermore, the achievable secrecy rate of A2G wireless link at time slot n is given by

$$
R _ { S E } [ n ] = \{ R _ { U , S } [ n ] - R _ { U , E } [ n ] \} ^ { + } ,\tag{13}
$$

where $\{ x \} ^ { + }$ is defined as max{x, 0}.

## E. UAV Energy Consumption Model

In this work, rotary-wing UAVs are adopted for their inherent hovering ability, which suppresses the Doppler effect and simplifies the beam alignment at each time slot2. According to the aircraft dynamics of rotary-wing UAVs, the power consumption can be expressed as the sum of the power for level flight and the power for vertical flight [49]. Specifically, the power of UAV k for level flight at time slot n can be calculated as follows:

$$
\begin{array} { r l } & { P _ { \mathrm { l e v e l } } ^ { k } [ n ] = P _ { i } \sqrt { 1 + \frac { \| v _ { k } ^ { x } [ n ] , v _ { k } ^ { y } [ n ] \| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \| v _ { k } ^ { x } [ n ] , v _ { k } ^ { y } [ n ] \| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } } \\ & { \qquad + P _ { 0 } \left( 1 + \frac { 3 \| v _ { k } ^ { x } [ n ] , v _ { k } ^ { y } [ n ] \| ^ { 2 } } { u _ { t i p } ^ { 2 } } \right) } \\ & { \qquad + \frac { 1 } { 2 } d _ { 0 } \rho s A \| v _ { k } ^ { x } [ n ] , v _ { k } ^ { y } [ n ] \| ^ { 3 } , } \end{array}\tag{14}
$$

where $v _ { k } ^ { x }$ and $v _ { k } ^ { y }$ are the x-axis component speed and y-axis component speed of UAV k at time slot n, respectively. v0 is the mean rotor induced velocity for hovering, $U _ { t i p }$ is the tip speed of the rotor blade, $d _ { 0 }$ is the fuselage drag ratio, Ï is the density of air, s is the rotor solidity and A is the rotor disk area. Moreover, $P _ { i }$ and $P _ { 0 }$ denote the induced power and the blade profile power in hovering status, which can be calculated as follows [50]:

$$
P _ { i } = ( 1 + M ) \frac { W ^ { 3 / 2 } } { \sqrt { 2 \rho A } } , P _ { 0 } = \frac { \kappa } { 8 } \rho s A \Omega ^ { 3 } \Lambda ^ { 3 } ,\tag{15}
$$

where Î© is the blade angular velocity, M is the incremental correction factor to induced power, Î is the rotor radius, and Îº is the profile drag coefficient. Moreover, $W = m g$ is the weight of UAV, wherein g is gravitational acceleration and m is the mass of UAV.

In addition, the power of UAV k for vertical flight at time slot n can be modeled as follows:

$$
P _ { \mathrm { v e r t i c a l } } ^ { k } [ n ] = \Big \{ { W v _ { k } ^ { z } [ n ] } , \quad v _ { k } ^ { z } [ n ] > 0 \ ,\tag{16}
$$

where $v _ { k } ^ { z }$ is the z-axis component speed of UAV k at time slot n. Moreover, $P _ { \mathrm { v e r t i c a l } } ^ { k } [ n ] = 0$ as the UAVs operate in auto-rotation and are unpowered during the vertical descent [49].

Accordingly, the flight energy consumption of UAV swarm at time slot n can be modeled as follows:

$$
E [ n ] = \sum _ { k = 1 } ^ { K } \delta _ { t } ( P _ { \mathrm { l e v e l } } ^ { k } [ n ] + P _ { \mathrm { v e r t i c a l } } ^ { k } [ n ] ) .\tag{17}
$$

## F. Eavesdropper Mobility Model

To simulate potential security threats, we assume that the mobility of eavesdropper follows the Gauss-Markov mobility model [51]. Specifically, the movement of an eavesdropper is governed by its speed and direction which are influenced by the past values and random variations. As a result, the speed of the eavesdropper at time slot n can be calculated as follows [51]:

$$
v _ { E } [ n ] = \beta v _ { E } [ n - 1 ] + ( 1 - \beta ) \overline { { v } } + \sqrt { 1 - \beta ^ { 2 } } w _ { E }\tag{18}
$$

where $v _ { E } [ n - 1 ]$ represents the speed of the eavesdropper at time slot $n - 1$ , and Î± denotes the correlation coefficient, which regulates the balance between randomness and historical dependence. Moreover, v is the average speed, and ${ \pmb w } _ { E }$ is a Gaussian wrandom variable that introduces stochastic variations in speed. Similarly, the movement direction $\Theta _ { E }$ of the eavesdropper can be updated as follows:

$$
\Theta _ { E } [ n ] = \alpha \Theta _ { E } [ n - 1 ] + ( 1 - \alpha ) \overline { { { \Theta } } } + \sqrt { 1 - \alpha ^ { 2 } } z _ { E }\tag{19}
$$

where $\Theta _ { E } [ n - 1 ]$ represents the direction of the eavesdropper at time slot $n - 1$ , Î is the mean direction, and $z _ { E }$ is a Gaussian zrandom variable to represent randomness in the direction.

## IV. PROBLEM FORMULATION AND ANALYSIS

In this work, we aim to maximize the secrecy rate of the system while minimizing the flight energy consumption of the UAV swarm by determining the excitation current weights and positions of UAVs during a period of N time slots. Thus, the ASCEE-MOP is formulated as follows:

$$
\mathbf { P 1 } : \operatorname* { m a x } _ { I , q } \left( \sum _ { n = 1 } ^ { N } R _ { S E } [ n ] , - \sum _ { n = 1 } ^ { N } E [ n ] \right) ,\tag{20a}
$$

$$
\mathrm { s . t . ~ 0 } \leq I _ { k } ^ { U } [ n ] \leq 1 , \forall k \in \{ 1 , . . . , K \} ,\tag{20b}
$$

$$
X _ { \operatorname* { m i n } } \leq x _ { k } ^ { U } [ n ] \leq X _ { \operatorname* { m a x } } , \forall k \in \{ 1 , . . . , K \} ,\tag{20c}
$$

$$
Y _ { \mathrm { m i n } } \le y _ { k } ^ { U } [ n ] \le Y _ { \mathrm { m a x } } , \forall k \in \{ 1 , . . . , K \} ,\tag{20d}
$$

$$
Z _ { \mathrm { m i n } } \le z _ { k } ^ { U } [ n ] \le Z _ { \mathrm { m a x } } , \forall k \in \{ 1 , . . . , K \} ,\tag{20e}
$$

$$
0 \leq v _ { k } ^ { U } [ n ] \leq V _ { \operatorname* { m a x } } , \forall k \in \{ 1 , . . . , K \} ,\tag{20f}
$$

$$
\| q _ { k _ { 1 } } [ n ] , q _ { k _ { 2 } } [ n ] \| \ge D _ { \operatorname* { m i n } } ^ { U } , \forall k _ { 1 } , k _ { 2 } \in \{ 1 , . . . , K \} ,\tag{20g}
$$

where ${ \cal I } = \{ { \cal I } _ { k } ^ { U } [ n ] \} _ { k \in K , n \in N }$ and ${ \pmb q } = \{ { \pmb q } _ { k } [ n ] \} _ { k \in K , n \in N }$ are the I q qexcitation current weight matrix and the position matrix of UAVs at all time slots, respectively. Constraint (20b) expresses the range constraint of the excitation current weight. Moreover, Constraints (20c), (20d) and (20e) restrict the flight area of the UAV which may be imposed by surveillance area and government regulations. In addition, Constraint (20f) is the speed constrain of the UAV, and Constraint (20g) is imposed to guarantee the minimum distance between two UAVs.

Non-convexity: The formulated ASCEE-MOP is non-convex. For a detailed proof, please refer to the Appendix B of the supplementary material, available online.

NP-hard: The formulated ASCEE-MOP can be proven to be NP-hard. For a detailed proof, please refer to the Appendix C of the supplementary material, available online.

Trade-off: Furthermore, the objective function of ASCEE-MOP seeks to concurrently maximize the secrecy rate of the system while minimizing the flight energy consumption of the UAV swarm. Specifically, it is essential for UAVs to fly to suitable positions to improve the antenna directivity of the UVAA system, thereby maximizing the total secrecy rate during task execution. However, constantly adjusting the positions of UAVs to maintain optimal antenna directivity leads to significant energy consumption. Thus, there is an inherent trade-off between maximizing the secrecy rate of the system and minimizing flight energy consumption of the UAV swarm within the formulated ASCEE-MOP, and striking the right balance between these two conflicting objectives poses a challenging task.

To deal with such non-convex optimization problems, most works subdivide them into several convex subproblems which can be solved by an iterative manner. However, the accuracy is impacted as a result of the decomposition. Moreover, the dynamics of environment, e.g., the changed position of mobile eavesdropper and the time-varying channel, brings some challenges. In this case, existing optimization-based methods and heuristic algorithms needs to re-run once the environment changes. Fortunately, DRL provides a feasible and efficient way for the sequential decision making and optimal control in dynamic environments. Thus, this motives us to utilize DRL-based methods to address the formulated ASCEE-MOP.

## V. THE PROPOSED GDMTD3

In this section, the formulated non-convex multi-objective optimization problem is solved by the DRL-based method. Specifically, we first adopt a Markov decision process to reformulate the ASCEE-MOP, and then propose the GDMTD3 method to solve the problem.

## A. Markov Decision Process for ASCEE-MOP

The formulated ASCEE-MOP of the UAV swarm-enabled surveillance network system can be modeled as a Markov decision process to facilitate the application of DRL. In general, a Markov decision process is represented as a tuple < $s , 4 , \mathcal { P } , \mathcal { R } , \gamma >$ , where S is the state space of environment, A is the action space of agent, P denotes the state transition probability of environment, R is the reward space, and $\gamma \in [ 0 , 1 ]$ denotes the reward discount factor. Specifically, the UVAA is treated as a decision-making agent in the Markov decision process. With the framework of the Markov decision process, the environment state at any given time slot n is signified by $s [ n ]$ ï¼ wherein $s [ n ] \in S$ s n. Subsequently, the agent selects an action ${ \pmb a } [ n ]$ according to the policy $\pi ( s [ n ] )$ . After that, the environa Ï sment dispenses the agent a reward r[n] and transitions to the next state $s [ n + 1 ]$ based on the transition probability function $\mathcal { P } ( \pmb { s } [ n + 1 ] | \pmb { s } [ n ] , \pmb { a } [ n ] )$ ). Accordingly, the crucial elements in our s s amodel are described below in detail.

1) State Space: The state of the system at time slot n can be defined by $\begin{array} { r } { \pmb { s } [ n ] = ( \pmb { q } [ n ] , \pmb { q } _ { E } ^ { x y } [ n ] ) } \end{array}$ . Specifically, [n] represents the positions of all UAVs at time slot $n ,$ and $\pmb { q } _ { E } ^ { x y } [ n ]$ is the coordinates of the eavesdroppers within the $x { - } y$ plane at time slot n. Note that to enhance the adaptability of the approach, the position of RBS is not included in the state space

2) Action Space: At a certain time slot $n ,$ each UAV needs to choose its own proper excitation current weight and position. Accordingly, the action set of UAV swarm can be represented by ${ \pmb a } [ n ] = ( { \pmb I } [ n ] , { \pmb q } [ n ] )$ , where $I [ n ]$ and ${ \pmb q } [ n ]$ represent the excia I q I qtation current weights and positions of all UAVs at time slot $n ,$ respectively.

3) Reward Function: In DRL, the reward garnered from the agent-environment interchange provides a quantifiable measure of action efficiency in a given state. Therefore, the formulated ASCEE-MOP can be transformed into maximizing the accumulative reward. Accordingly, the reward function can be constructed as follows:

$$
r [ n ] = \omega _ { 1 } r _ { S E } [ n ] + \omega _ { 2 } r _ { E } [ n ] - r _ { P } [ n ] ,\tag{21}
$$

where the first term, i.e., $r _ { S E } [ n ] = R _ { S E } [ n ]$ represents the secrecy rate that the system achieves at time slot n. Moreover, the second term $r _ { E } [ n ] = - E [ n ]$ quantifies the total flight energy consumption of all UAVs at time slot $n .$ Furthermore, $\omega _ { 1 }$ and Ï2 denote the weight factors for the two objectives, which can be determined based on their respective value ranges. In addition, the penalty $r _ { P } [ n ]$ is applied if the UAVs violate the constraint of speed or collide with each other.

4) Transition Probability: In our work, the transition probability of the state, which is denoted as $\mathcal { P } ( \pmb { s } [ n + 1 ] | \pmb { s } [ n ] , \pmb { a } [ n ] )$ s s aspecifies the probability distribution of the subsequent state after the UAVs execute their respective actions in the current state.

## B. Basic Principles of Conventional TD3

TD3 [52] is an advanced reinforcement learning algorithm that extends from the foundations of deep deterministic policy gradient (DDPG) [53] method. Specifically, TD3 addresses the key limitations in DDPG by incorporating several novel techniques including twin critic networks, delayed policy updates, and target policy smoothing, which collectively contribute to its superior performance in continuous control tasks.

1) Actor-Critic Framework: Similar to DDPG, TD3 employs an actor-critic structure, where the actor network $\mu ( s | \theta _ { \mu } )$ outputs deterministic actions, and the critic networks $Q ( s , a | \theta _ { Q } )$ Q s a Î¸evaluate the action-state value function. The objective is to find the optimal policy  that maximizes the expected accumulated return.

The Bellman equation provides a recursive decomposition to update the action-value function $Q ( s , a )$ , which can be Qdescribed mathematically as follows [54]:

$$
\begin{array} { r } { Q ( s [ n ] , \pmb { a } [ n ] ) = r [ n ] + \gamma \mathbb { E } _ { s [ n + 1 ] \sim p _ { \pi } } [ Q ( s [ n + 1 ] , \ } \\ { \pmb { \mu } ( s [ n ] , \pmb { a } [ n ] ) ) ] , } \end{array}\tag{22}
$$

where $p _ { \pi }$ represents the transition probability distribution under ppolicy .

Ï2) Twin Critic Networks: One of the significant improvements in TD3 is the use of twin critic networks to address overestimation bias. Specifically, overestimation usually occurs when the action-value estimates are consistently higher than the true values, leading to the suboptimal policy updates. While in TD3, two independent critic networks, i.e., $Q _ { 1 } ( s , a | \theta _ { Q _ { 1 } } )$ and $Q _ { 2 } ( s , a | \theta _ { Q _ { 2 } } )$ , are used to estimate the value of state-action pairs. The target Q-value is computed as the minimum of the two estimates, which is represented as follows:

$$
y [ n ] = r [ n ] + \gamma \operatorname * { m i n } _ { i = 1 , 2 } Q _ { i } ^ { \prime } ( s [ n + 1 ] , \mu ^ { \prime } ( s [ n + 1 ] | \theta _ { \mu } ^ { \prime } ) ) ,\tag{23}
$$

where $Q _ { i } ^ { \prime }$ is the target critic networks corresponding to $Q _ { i }$ , and $\mu ^ { \prime }$ Qis the target actor network.

3) Delayed Policy Update: TD3 incorporates the delayed policy update to prevent the policy network from overfitting to noisy value estimates. While the critic networks are updated at each time step, the actor network is updated less frequently. Specifically, the policy is updated every d iterations of the critic networks, and this delay allows the value estimates to stabilize, leading to more reliable policy updates.

4) Target Policy Smoothing: To further enhance the stability, TD3 introduces target policy smoothing, which adds extra noise to the target action during the critic update process. This process involves sampling noise from a Gaussian distribution $\mathbf { \bar { \epsilon } } \sim \mathcal { N } ( 0 , \sigma ^ { 2 } )$ and clipping it to a certain range to maintain the target action within the permissible action space. Specifically, the process above can be represented as follows:

$$
s a [ n + 1 ] = \mu ^ { \prime } ( s [ n + 1 ] | \theta _ { \mu } ^ { \prime } ) + \epsilon , \epsilon \sim \mathrm { c l i p } ( { \mathcal N } ( 0 , \sigma ^ { 2 } ) , - c , c ) ,\tag{24}
$$

where $\mathrm { c l i p } ( x , a , b )$ is a clipping operator, which is defined as $\operatorname { c l i p } ( x , a , b ) = x { \mathrm { ~ i f ~ } } a < x < b , \ \operatorname { c l i p } ( x , a , b ) = a { \mathrm { ~ i f ~ } } x \leq a$ and $\mathrm { c l i p } ( x , a , b ) = b \mathrm { i f } x \geq b .$ . This smoothed target action $s a [ n + 1 ]$ sais used in the Bellman update to replace the target action $\mu ^ { \prime } ( s [ n + 1 ] | \theta _ { \mu } ^ { \prime } )$ in (23), which reduces the variance of the value Î¼ s Î¸estimates and preventing sharp changes in the policy.

5) Network Training: The training process of TD3 involves updating the actor and critic networks based on specific loss functions, which is designed to improve the learning stability and performance. The update of critic network is through minimizing the temporal difference (TD) error loss function, which is defined as follows:

$$
L ( \theta _ { Q _ { i } } ) = \mathbb { E } \left[ \left( Q _ { i } ( s [ n ] , a [ n ] | \theta _ { Q _ { i } } ) - y [ n ] \right) ^ { 2 } \right] , i = 1 , 2 .\tag{25}
$$

With a batch of randomly sampled B transitions from experience replay buffer D, the loss function for the critic network can be approximated as follows:

$$
L ( \theta _ { Q _ { i } } ) \approx \frac { 1 } { B } \sum _ { b = 1 } ^ { B } \left( Q _ { i } ( s _ { b } , a _ { b } | \theta _ { Q _ { i } } ) - y _ { b } \right) ^ { 2 } , i = 1 , 2 ,\tag{26}
$$

where $y _ { b } = r _ { b } + \gamma$ mini=1,2 -i( _b, - ( _b| -Î¼) + ).

The actor network $\mu ( s | \theta _ { \mu } )$ Q s Î¼ s Î¸ is updated less frequently than the Î¼ s Î¸critic networks to ensure stable learning. The objective of actor network is to maximize the expected Q-value as evaluated by the first critic network. The loss function for the actor network is represented as follows:

$$
L ( \theta _ { \mu } ) = - \mathbb { E } \left[ Q _ { 1 } ( s , \mu ( s | \theta _ { \mu } ) | \theta _ { Q _ { 1 } } ) \right] .\tag{27}
$$

With a batch of randomly sampled B transitions from experience replay buffer D, the loss function for the actor network can be approximated as follows:

$$
L ( \theta _ { \mu } ) \approx - \frac { 1 } { B } \sum _ { b = 1 } ^ { B } { Q _ { 1 } ( s _ { b } , \mu ( s _ { b } | \theta _ { \mu } ) | \theta _ { Q _ { 1 } } ) } .\tag{28}
$$

The target networks are updated using a soft update mechanism, which blends the parameters of the main networks with those of the target networks using a weight factor. The updates are defined as follows:

$$
\theta _ { Q _ { i } } ^ { \prime }  \tau \theta _ { Q _ { i } } + ( 1 - \tau ) \theta _ { Q _ { i } } ^ { \prime } , i = 1 , 2 ,\tag{29}
$$

and

$$
\pmb { \theta } _ { \mu } ^ { \prime }  \tau \pmb { \theta } _ { \mu } + ( 1 - \tau ) \pmb { \theta } _ { \mu } ^ { \prime } ,\tag{30}
$$

where Ï is a small soft weight factor. It can be observed that the updated parameters of a target network are a weighted combination of its original parameters and the corresponding network parameters.

## C. Generative Diffusion Model for Actor Network

In this section, we first elaborate the motivation behind employing diffusion models within the actor network of TD3 algorithm. Then, we explore the customization of the diffusion model for generating optimal decisions regarding the formulated ASCEE-MOP.

1) Motivation of Employing Diffusion Model: Deep reinforcement learning (DRL) has become an effective method for dealing with various network optimization problems in dynamic environments. Generally, DRL employs deep neural networks (DNNs) to provide optimal actions according to the current environment state. Multi-layer perceptrons (MLPs), a prevalent fully-connected DNN architecture in DRL, consist of hidden layers with nonlinear activation functions. However, the ASCEE-MOP faces unique challenges, such as the mobility of eavesdroppers, which introduces uncertainty and results in a highly dynamic and complex state space. Moreover, ASCEE-MOP involves intricate trade-offs between various optimization objectives, making it challenging to identify optimal solutions in this constantly changing environment. Thus, traditional MLP approaches may struggle to fully capture and balance these interconnected objectives.

In contrast, generative diffusion models [55], [56], with their superior feature learning capabilities, can better comprehend environmental states and the relationships between different objectives. This understanding allows DRL agents to make more balanced and optimized decisions in the highly uncertain and dynamic environment of ASCEE-MOP. Consequently, the use of diffusion models can be highly advantageous for addressing the complex issues inherent in ASCEE-MOP.

2) Diffusion Model: Diffusion model, such as the denoising diffusion probabilistic model (DDPM) [57], operate through a dual-phase process that are the forward process and reverse process. Specifically, the forward phase incrementally adds Gaussian noise to the data, converting it progressively into a pure noise distribution. Conversely, the reverse phase reconstructs the original data by systematically removing this noise.

Forward Process: Given a original data $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ , the forward process produces a series of noisy samples $\{ \boldsymbol { x } _ { t } \} _ { t = 0 } ^ { T }$ by gradually xadding the Gaussian noise. Specifically, at each step t, the noisy sample $\mathbf { \Delta } _ { \mathbf { \mathcal { X } } _ { t } }$ is sampled from the distribution ${ \pmb p } ( { \pmb x } _ { t } | { \pmb x } _ { t - 1 } )$ , which is generated from the previous sample ${ \mathbf { \mathcal { x } } } _ { t - 1 }$ p x xby using the method as follows:

$$
p ( \pmb { x } _ { t } | \pmb { x } _ { t - 1 } ) = \mathcal { N } ( \pmb { x } _ { t } ; \sqrt { 1 - \beta _ { t } } \pmb { x } _ { t - 1 } , \beta _ { t } \pmb { I } ) ,\tag{31}
$$

where  represents the identity matrix, and $\beta _ { t }$ is a variance Ischedule that is controlled by the variance preserving (VP) schedule. Moreover, $\beta _ { t }$ is the variance function of VP stochastic differential equations, which is as follows [58]:

$$
\beta _ { t } = 1 - e ^ { - \frac { \beta _ { \mathrm { m i n } } } { T } - \frac { 2 t - 1 } { 2 T ^ { 2 } } \left( \beta _ { \mathrm { m a x } } - \beta _ { \mathrm { m i n } } \right) } ,\tag{32}
$$

where $\beta _ { \mathrm { m i n } }$ and $\beta _ { \mathrm { m a x } }$ are the two constants that define the minimum and maximum variance.

The entire forward process from $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ to $\mathbf {  { x } } _ { T }$ can be expressed as follows:

$$
p ( \pmb { x } _ { T } | \pmb { x } _ { 0 } ) = \prod _ { t = 1 } ^ { T } p ( \pmb { x } _ { t } | \pmb { x } _ { t - 1 } ) .\tag{33}
$$

Moreover, the forward process that delineates the mathematical relation between $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ and any $\mathbf { \Delta } _ { \mathbf { \mathcal { X } } _ { t } }$ is described as follows:

$$
\pmb { x } _ { t } = \sqrt { \bar { \alpha } _ { t } } \pmb { x } _ { 0 } + \sqrt { 1 - \bar { \alpha } _ { t } } \pmb { \epsilon } ,\tag{34}
$$

where $\bar { \alpha } _ { t } = \prod _ { k = 1 } ^ { t }$ Î±k represents the cumulative product of Î±k for all steps $k \leq t _ { \mathrm { { \ell } } }$ , wherein $\alpha _ { t } = 1 - \beta _ { t }$ , and $\mathbf { \epsilon } \epsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } )$ is a standard Gaussian noise. With an increase in t, T gradually xtransitions into purely noise, adhering to an isotropic Gaussian distribution $\mathcal { N } ( 0 , \pmb { I } )$ . However, note that due to the absence of an Ioptimal decision solution dataset $( \mathrm { i } . \mathrm { e } . , \pmb { x } _ { 0 }$ in the forward process) xfor the formulated optimization problem, the forward process is not integrated into the proposed GDMTD3.

Reverse Process: In the reverse process, the goal is to recover the original data $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ from a noisy sample $\mathbf { \nabla } _ { \mathbf { \mathcal { X } } \mathcal { T } }$ that follows a standard Gaussian distribution $\mathcal { N } ( \mathbf { 0 } , \pmb { I } )$ xby iteratively removing the noise. However, the statistical distribution $q ( \pmb { x } _ { t - 1 } | \pmb { x } _ { t } )$ nex xcessitate computations that involve the data distribution, which is typically intractable in practice. Instead, our strategy is to approximate the conditional distribution $q ( \pmb { x } _ { t - 1 } | \pmb { x } _ { t } )$ by using a parameterized model $p _ { \theta _ { d } }$ x x, which can be expressed as follows:

$$
p _ { \theta _ { d } } ( \pmb { x } _ { t - 1 } | \pmb { x } _ { t } ) = \mathcal { N } ( \pmb { x } _ { t - 1 } ; \kappa _ { \theta _ { d } } ( \pmb { x } _ { t } , t , \pmb { g } ) , \tilde { \beta } _ { t } \pmb { I } ) ,\tag{35}
$$

where $\kappa _ { \theta _ { d } } ( x _ { t } , t , g )$ is the mean, wherein  is the condition Îº xinformation, and $\beta _ { t }$ grepresents a predetermined variance factor, which is represented as follows:

$$
\tilde { \beta } _ { t } = \frac { 1 - \bar { \alpha } _ { t - 1 } } { 1 - \bar { \alpha } _ { t } } \beta _ { t } .\tag{36}
$$

Utilizing Bayesian formulation, the reverse process is restructured as a Gaussian probability density function. The mean for

```powershell
Algorithm 1: Action Sampling Based on Generative
Diffusion Model.
Input: The state of current environment $s [ n ]$
Output: The action decision ${ \pmb a } [ n ]$
1 Initialize a random Gaussian distribution
$\mathbf { \boldsymbol { x } } _ { T } \sim \mathcal { N } ( \mathbf { \boldsymbol { 0 } } , \mathbf { \boldsymbol { I } } ) ;$
2 for the denoising step $t = T$ to 1 do
3 Deduce a denoising distribution $\varepsilon _ { \theta _ { d } } ( { \pmb x } _ { t } , t , { \pmb s } [ n ] )$
by a deep neural network;
4 Compute the mean $\kappa _ { \theta _ { d } } ( \pmb { x } _ { t } , t , \pmb { s } [ n ] )$ of
$p _ { \theta _ { d } } ( \pmb { x } _ { t - 1 } | \pmb { x } _ { t } )$ according to Eq. (39);
5 Compute the distribution $\mathbf { \nabla } x _ { t - 1 }$ using the
reparameterization trick according to Eq. (41);
6end
7 Compute the distribution of $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ according to Eq. (40)
and randomly select an action ${ \pmb a } [ n ]$ based on it;
8 return ${ \pmb a } [ n ]$
```

the reverse process is computed as follows [57]:

$$
\kappa _ { \theta _ { d } } ( x _ { t } , t , g ) = \frac { \sqrt { \alpha _ { t } } \left( 1 - \bar { \alpha } _ { t - 1 } \right) } { 1 - \bar { \alpha } _ { t } } \pmb { x } _ { t } + \frac { \sqrt { \bar { \alpha } _ { t - 1 } } \beta _ { t } } { 1 - \bar { \alpha } _ { t } } \pmb { x } _ { 0 } .\tag{37}
$$

Nonetheless, the parameterized model $p _ { \theta _ { d } }$ does not have access to $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ pand therefore must estimate it as a substitute. xAccording to (34), $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ can be calculated as follows:

$$
{ \pmb x } _ { 0 } = \frac { 1 } { \sqrt { \bar { \alpha } _ { t } } } \left( { \pmb x } _ { t } - \sqrt { 1 - \bar { \alpha } _ { t } } \cdot { \pmb \varepsilon } _ { { \pmb \theta } _ { d } } ( { \pmb x } _ { t } , t , { \pmb g } ) \right) ,\tag{38}
$$

where $\varepsilon _ { \theta _ { d } } ( x _ { t } , t , g )$ is a deep neural network that generates the Îµ x gdenoising noise based on the condition , and then indirectly approximate the mean by

$$
\kappa _ { \theta _ { d } } ( \boldsymbol { x } _ { t } , t , \boldsymbol { g } ) = \frac { 1 } { \sqrt { \alpha _ { t } } } \left( \boldsymbol { x } _ { t } - \frac { \boldsymbol { \beta } _ { t } \cdot \boldsymbol { \varepsilon } _ { \theta _ { d } } ( \boldsymbol { x } _ { t } , t , \boldsymbol { g } ) } { \sqrt { 1 - \bar { \alpha } _ { t } } } \right) .\tag{39}
$$

Tracing the reverse transitions from $\mathbf { \nabla } _ { \mathbf { x } _ { T } }$ back to $\scriptstyle { \pmb x } _ { 1 }$ , we can establish the generative distribution ${ p } _ { \theta _ { d } } ( { \boldsymbol { x } } _ { 0 } )$ xas follows:

$$
p _ { \theta _ { d } } ( \pmb { x } _ { 0 } ) = \pmb { p } ( \pmb { x } _ { T } ) \prod _ { t = 1 } ^ { T } p _ { \theta _ { d } } ( \pmb { x } _ { t - 1 } | \pmb { x } _ { t } ) ,\tag{40}
$$

where $p ( { \pmb x } _ { T } )$ represents a standard normal distribution. Once xthe generative distribution ${ p } _ { \theta _ { d } } ( { \pmb x } _ { 0 } )$ is successfully trained, we can then proceed to sample $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ from (40).

x3) Integration of Diffusion Model and Actor Network of TD3: Integrating diffusion model into the actor network of conventional TD3 algorithm significantly enhances the decisionmaking by providing a more diverse set of potential actions. Specifically, the generative capabilities of diffusion model allow for the creation of complex action sets, which are refined through the learned reverse process, enabling direct sampling of actions from the generative distribution $p _ { \theta _ { d } } ( \boldsymbol { x } _ { 0 } )$

p xA significant challenge in integrating diffusion model is managing stochastic components, which complicates gradient descent methods typically used in training. To overcome this issue, a reparameterization process that facilitates differentiable sampling is employed, which can be represented as follows:

TABLE II  
OTHER ENVIRONMENTAL PARAMETER SETTINGS [50], [60]
<table><tr><td>Parameter</td><td>Value</td><td>Parameter</td><td>Value</td></tr><tr><td> $f _ { c }$ </td><td>2.4 GHz</td><td>Î¼1</td><td>1 dB</td></tr><tr><td>C0</td><td>9.61</td><td>Î¼2</td><td>20 dB</td></tr><tr><td>C1</td><td>0.16</td><td>W</td><td>19.6N</td></tr><tr><td>v0</td><td>4.03</td><td> $u _ { \mathrm { { t i p s } } }$ </td><td>120</td></tr><tr><td>do</td><td>0.6</td><td>p</td><td>1.225</td></tr><tr><td>S</td><td>0.05</td><td>A</td><td>0.503</td></tr><tr><td>M</td><td>0.1</td><td>K</td><td>0.012</td></tr><tr><td>Î©</td><td>300</td><td>A</td><td>0.4</td></tr></table>

$$
\begin{array} { r } { \pmb { x } _ { t - 1 } = \pmb { \kappa } _ { \pmb { \theta } _ { d } } \left( \pmb { x } _ { t } , t , \pmb { s } \right) + \left( \tilde { \beta } _ { t } / 2 \right) ^ { 2 } \odot \epsilon , } \end{array}\tag{41}
$$

where which represents the current state of the environment in sDRL, is used as a conditional variable in the parameterization function $\kappa _ { \theta _ { d } }$ . Moreover,  is the operator of Hadamard product.

ÎºThis adaptation allows the diffusion process to be contextually responsive and adjusting actions dynamically according to the state of the environment, which is crucial for DRL algorithms where the environmental state guides the necessary action responses. Accordingly, the main steps of the action sampling process based on generative diffusion model is detailed in Algorithm 1.

## D. Main Flow of Proposed Algorithm

Fig. 2 shows the framework and main flow of the proposed GDMTD3 for the formulated ASCEE-MOP. Specifically, the proposed method integrates the diffusion model within DRL, which enhances the capability of the actor network for navigating the complex decision spaces under high-dimensional and noisy input data. The detailed implementation of this process is elaborated in Algorithm 2. From Lines 1 to 2, we initialize two online critic networks and a generative diffusion-enabled online actor network, along with their respective target networks. The training procedure begins with the environment initialization at Line 4. At each time step, the agent gets an action from the generative diffusion-enabled online network at Line 7. Then, the agent executes this action in the environment, and receives the reward from the environment at Line 8. The agent stores the transition in the replay memory at Line 9. Moreover, from Lines 10 to 15, the according parameters of critic and actor networks are updated.

1) Training and Execution: In the considered UAV swarmenabled surveillance network system, the RBS coordinates the training phase through an actor-critic network framework. In this phase, the interaction information between UAV swarm and the environment is regularly recorded and stored into a replay buffer. Note that the RBS possesses the sufficient capabilities to transmit the training parameters to UAV swarm [59]. Following a comprehensive training period, the actor network is then integrated with UAV swarm, steering their real-time operations to adaptively accomplish the secure communication mission throughout the execution phase.

<!-- image-->  
Fig. 2. Schematic of GDMTD3 framework, where the generative diffusion model is integrated into the actor network of TD3 algorithm to capture complex state features and generate optimal actions according to the current state of the environment.

2) Complexity Analysis: In this section, we analyze the computational and space complexity of GDMTD3 during training and execution phases.

Training Phase: The computational complexity of GDMTD3 is $\mathcal { O } ( 4 \vert \theta _ { Q _ { 1 } } \vert + 2 \vert \theta _ { d } \vert + M N T \vert \theta _ { d } \vert + M N V + M N ( 2 \vert \theta _ { Q _ { 1 } } \vert ) +$ $M N / d ( 2 | \theta _ { Q _ { 1 } } | + 2 | \theta _ { d } | ) )$ Î¸ Î¸) in the training phase, which can be Î¸ Î¸summarized as follows:

- Network Initialize: This phase involves the initialization of network parameters. Specifically, the computational complexity is expressed as $\mathcal { O } ( 4 | \theta _ { Q _ { 1 } } | + 2 | \theta _ { d } | )$ ), where $| \theta _ { Q _ { 1 } } |$ Î¸ Î¸ Î¸denotes the number of parameters in each of the twin online critic networks, and $| \pmb { \theta } _ { d } |$ represents the number of Î¸parameters in the diffusion-enabled online actor network.

- Action Sampling: This phase entails generating actions according to the current state using the diffusion reverse process, and its complexity is $\mathcal { O } ( M N T | \theta _ { d } | )$ . Here, M Î¸denotes the number of training episodes, N is the number of steps per episode, and T is the number of denoising steps required to sample an action in diffusion-enabled actor network.

Replay Buffer Collection: The complexity of collecting state transitions in the replay buffer is O(M N V ), where V represents the complexity of interacting with environment.

Network Update: The updating phase is divided into three main parts that are the frequent updates of the critic networks and less frequent updates of the actor network along with their respective soft updates. Thus, the complexity for this phase is calculated as $\mathcal { O } ( M N ( 2 \vert \theta _ { Q _ { 1 } } \vert ) +$ $M N / d ( 2 | \theta _ { Q _ { 1 } } | + 2 | \theta _ { d } | ) )$ .

Î¸ Î¸In the training phase, the space complexity of GDMTD3 is $\mathcal { O } ( 4 | \theta _ { Q _ { 1 } } | + 2 | \theta _ { d } | ) + D ( 2 | s | + | a | + 1 ) )$ , where D represents Î¸ Î¸ s athe size of the replay buffer and | |, | | denote the dimensions of s athe state and action spaces, respectively. This space complexity accounts for the storage of neural network parameters and the data structures required to maintain the replay buffer, which holds tuples of states, actions, rewards, and next states.

Execution Phase: During the execution phase, the computational complexity of GDMTD3 is $\mathcal { O } ( M N T | \theta _ { d } | )$ , which can be Î¸contributed by action selection according to the current state using the diffusion-enabled actor network. Moreover, the space complexity during the execution phase is $\mathcal { O } ( | \theta _ { d } | )$ since the Î¸diffusion-enabled actor network parameters need to be stored in memory for action selection.

## VI. SIMULATION RESULTS

In this section, we present the comprehensive evaluations of our proposed approach and verify the effectiveness and robustness of the proposed GDMTD3 in addressing ASCEE-MOP under various settings.

## A. Simulation Setup

This section provides an extensive description of the simulation setup, including the simulation platform, environmental details, model design, and benchmarks utilized to evaluate the performance of the proposed approach.

1) Simulation Platform: Our experiments are conducted using a computing setup that included an NVIDIA GeForce RTX 3090 GPU with 24 GB of memory and a 13th Gen Intel(R) Core(TM) i9-13900K 32-core processor with 128 GB of RAM. The operating system on the workstation is Ubuntu 22.04.3 LTS. For our deep learning computations, we use PyTorch 2.2.2, along with the CUDA 11.8.

2) Environmental Details: In this study, we consider a UAV swarm consisting of 8 individual UAVs, each of which equipped with a transmit power of 0.1 W. Moreover, the UAV swarm is dispersed randomly within an area measuring 40 m by 40 m in each training episode. We assume the presence of a mobile eavesdropper in the environment with an average speed of 5.0 m/s, a correlation coefficient of 0.1, and a random variance of 1.0 in both speed and direction. In addition, Table II provides the details about the channel characteristics and the UAVs.

```perl
Algorithm 2: GDMTD3.
1 Initialize two online critic networks denoted as $Q _ { 1 }$
and $Q _ { 2 }$ with parameters $\theta _ { Q _ { 1 } }$ and $\theta _ { Q _ { 2 } }$ and a
generative diffusion-enabled online actor network
denoted as Îµ with parameters $\theta _ { d } ;$
2 Initialize the corresponding target networks:
$\theta _ { Q _ { 1 } } ^ { \prime }  \theta _ { Q _ { 1 } } , \theta _ { Q _ { 2 } } ^ { \prime } \stackrel { . } {  } \theta _ { Q _ { 2 } }$ and $\bar { \theta } _ { \mu } ^ { \prime }  \theta _ { \mu } ;$
3 for the training episode = 1 to M do
4 Reset the initial state s[0] of environment;
5 repeat
6 step $ 0 ;$
7 Call Algorithm 1 to obtain the action a[step];
8 Execute the action a[step] in the environment
and receive the reward r[step] and the next
state s[step +1] from the environment;
9 Store the experience
(s[step],a[step],r[step],s[step+1]) in the
replay buffer D;
10 Sample a random batch B from the replay
buffer D;
11 Update the online critic network parameters
according to Eq. (26);
12 if step mod d then
13 Update the actor network parameters
according to Eq. (28);
14 Soft-update the target networks according
to Eqs. (29) and (30);
15 end
16 step â step +1;
17 until environment is terminated;
18 end
```

3) Model Design: GDMTD3 utilizes a diffusion model at the core of its actor network, and it employs two structurally identical critic networks to address overestimation issues. Specifically, the critic networks consist of three-layer MLPs with ReLU activation function [61]. Moreover, Fig. 3 shows the detailed configuration of actor network. Specifically, the actor network in GDMTD3 uses sinusoidal position embeddings to capture the temporal dynamics inside the diffusion process and predicts the denoised distribution according to the current state and a random Gaussian distribution. This enhancement enables the actor network to better understand the interdependencies among steps in the diffusion chain. In addition, the Adam optimizer [62] is used to train the actor and critic networks, with a learning rate of $l r = 3 \times 1 0 ^ { - 4 }$ for each network. The target networks, which replicate the structure of the online networks, can minimize the learning variance. We adopt a soft update rate of $\tau = 0 . 0 0 5$ as specified in (29) and (30). Additional training hyperparameters are outlined in Table III.

4) Benchmarks: To validate the superiority of our proposed approach, we compare the following approaches:

<!-- image-->  
Fig. 3. The diffusion-enabled actor network architecture, where Mish activation function [63] is adopted.

TABLE III  
OTHER TRAINING PARAMETER SETTINGS
<table><tr><td>Parameter</td><td>Description</td><td>Value</td></tr><tr><td>B</td><td>Batch size</td><td>128</td></tr><tr><td>Y</td><td>Discount factor</td><td>0.90</td></tr><tr><td>D</td><td>Capacity of the experience replay buffer</td><td>2Ã106</td></tr><tr><td>d</td><td>Frequency of policy updates</td><td>2</td></tr><tr><td>T</td><td>Denoising steps for the diffusion model</td><td>4</td></tr><tr><td>M</td><td>Number of training episodes</td><td>8000</td></tr></table>

- Random Strategy: The random strategy arranges each UAV in a random position within the surveillance area at each time slot, without any specific formation. The excitation current weight for each UAV is also assigned random values within the allowable range. This approach serves as a baseline to evaluate the performance improvements achieved by more strategies.

- Linear Antenna Array Strategy: The linear antenna array (LAA) strategy arranges UAVs in a linear alignment with an equal inter-UAV separation distance of 0.5 m. Moreover, the geometric center of the linear formation of UAVs coincides with the center of the designated monitoring region.

- Planar Antenna Array Strategy: The planar antenna array (PAA) strategy arranges UAVs in a two-dimensional grid with an equal inter-UAV separation distance of 0.5 m.

<!-- image-->

<!-- image-->  
Fig. 4. Comparison results of the proposed GDM-enabled DRL approach and other four deployment policies. (a) Average secrecy rate per step. (b) Average flight energy consumption per step.

Similarly, the geometric center of grid formation of UAVs coincides with the center of the monitoring region.

Circular Antenna Array Strategy: The circular antenna array (CAA) strategy arranges UAVs in a circular pattern with a radius of 0.5 m and equal inter-UAV separation distance. Similarly to the LAA and PAA strategies, the center point of this circular UAV formation coincides with the center of the designated monitoring region.

The Proposed GDM-enabled DRL Approach: Our approach optimizes the secure rate of system and the flight energy consumption of the UAV swarm by formulating the ASCEE-MOP, and then solving it by using the proposed GDMTD3 algorithm.

In addition to comparing these approaches, we also compare the proposed GDMTD3 with four well-known DRL benchmarks: DDPG, TD3, SAC [64], and PPO [65]. Specifically, DDPG, TD3, and SAC are off-policy methods that are used for the continuous action spaces and utilize advanced strategies for stability and performance enhancement. In contrast, PPO is an on-policy method that offers robustness and simplicity in implementation, which is also suitable for the continuous action but focuses on effective policy updates through direct learning from the current policy. Moreover, we implement a transformer-based TD3 method as another point of comparison, which serves as a benchmark to evaluate the capability of the proposed diffusion model in extracting relevant features and representing complex state representations for DRL. Specifically, this method employs a transformer network [66] with two attention heads as the actor network, designed to handle sequential dependencies and complex state representations.

## B. Simulation Results

The detailed results of our simulation are provided in this section. We compare the effectiveness of the proposed GDMenabled DRL approach with several above-mentioned benchmark deployment policies, and analyze the performance of the proposed GDMTD3 under various algorithm configurations and environmental settings.

1) Comparisons With Other Deployment Policies: In this part, the proposed GDM-enabled DRL approach is compared to the four different deployment policies. Specifically, Fig. 4(a)

<!-- image-->  
Fig. 5. Comparison of position distributions of UAVs in different deployment policies.

and (b) show the average secrecy rate of the system and average flight energy consumption of the UAV swarm, respectively.

As shown in Fig. 4(a), the GDM-enabled DRL approach obtains a higher average secrecy rate. This result demonstrates the effectiveness of our proposed approach in ensuring secure communications by optimizing excitation current weights and positions of UAVs. Interestingly, the random strategy performs better than the structured LAA, PAA, and CAA strategies. The most likely reason is that the fixed formations in these three deployment strategies make it more difficult to handle the mobility of the eavesdropper.

From Fig. 4(b), it is evident that the suggested GDM-enabled DRL strategy uses less energy on average than the other approaches. the proposed GDM-enabled DRL approach exhibits the lower average energy consumption compared to the other strategies. This highlights the efficiency of the proposed GDMenabled DRL approach in optimizing the flight energy consumption of UAV swarm, which is crucial for the operation of resource-constrained UAVs. Moreover, the random policy shows the highest energy consumption, reflecting its inefficiency. In addition, the LAA, PAA, and CAA strategies demonstrate moderate energy consumption, but they do not achieve the same level of secrecy rate as the proposed GDM-enabled DRL approach, underscoring the advantage of the proposed GDM-enabled DRL approach in optimizing energy consumption while maintaining secure communications.

In addition, Fig. 5 depicts the UAV position distributions under various deployment policies, including the our proposed approach, LAA, PAA, and CAA. It can be seen from the figure that the proposed GDM-enabled DRL approach supports a flexible and adaptive position distribution of UAVs, thereby enhancing the secrecy rate of the system by dynamically optimizing beam patterns in response to environmental changes. In conclusion, it is apparent that the proposed GDM-enabled DRL approach achieves a superior performance in terms of both the secrecy rate of the system and the flight energy consumption of the UAV swarm.

2) Comparisons With Other DRL Benchmarks: Fig. 6 shows the comparison results of GDMTD3 with five different DRL benchmarks, including TD3, PPO, DDPG, SAC and transformer-based TD3 methods. As shown in Fig. 6(a), the proposed GDMTD3 reports significantly higher rewards per episode than the other DRL methods. This superiority of GDMTD3 is originated from the incorporation of diffusion model in GDMTD3, which allows for more efficient exploration and exploitation of the state-action space, resulting in higher cumulative rewards. Moreover, Fig. 6(b) and (c) indicate that GDMTD3 achieves the highest average secrecy rate of the system and relatively low average flight energy consumption of the UAV swarm among the compared methods. In addition, although the transformer-based TD3 method outperforms traditional TD3, PPO, DDPG, and SAC methods, it does not reach the secrecy rate achieved by GDMTD3, highlighting the advantage of diffusion model in adapting to the complex secure communication scenario involving the mobile eavesdropper.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼  
Fig. 6. Comparison results of GDMTD3 and DRL benchmarks. (a) Reward per episode. (b) Average secrecy rate per step. (c) Average flight energy consumption per step.

3) Impact of Algorithm Parameters: In this section, we evaluate effects of different parameters on the performance of GDMTD3 including the random seed, noise schedule function, and denoising step.

Effect of Different Random Seeds: DRL algorithms are known to be sensitive to random seeds, which can significantly impact their performance, sometimes even causing the algorithm failing to converge when different seeds are used [67]. Specifically, this sensitivity arises because random seeds influence various aspects of the training process, such as the initialization of neural network weights, the order of data processing, and the exploration strategies. To this end, we compare the impact of different random seeds on the performance of the GDMTD3. As shown in Fig. 7, GDMTD3 consistently converges and achieves high rewards although the reward curves vary slightly depending on the random seed. This result demonstrates its robustness and stability across different initial conditions.

Effect of Different Noise Schedule Functions: Diffusion-based models are also affected by the selection of noise schedule functions, which determine how parameters such as noise levels are adjusted over time [68]. Specifically, this influence stems from the direct effect of noise schedule functions on the diffusion process, which depends on how effectively the model learns to generate high-quality samples. In our scenario, we evaluate the impact of different noise schedule functions on the performance of GDMTD3, which includes VP, linear and cosine noise schedule functions [68]. As illustrated in Fig. 8, the results show that the VP schedule leads to the highest reward and faster convergence among the three noise schedule functions. This result highlights the superior performance of the VP schedule when applying GDMTD3 method to address the formulated ASCEE-MOP.

<!-- image-->  
Fig. 7. Comparison of reward curves of GDMTD3 with different random seeds.

<!-- image-->  
Fig. 8. Comparison of reward curves of GDMTD3 with different schedule strategies.

Effect of Different Denoising Steps: The number of denoising steps in the diffusion reverse process is another critical factor that can significantly impact the performance of diffusion-based models. First, denoising steps determine how effectively the model can reduce noise and generate high-quality samples [37]. Second, an increase in denoising steps also leads to longer training time. Therefore, we compare the impact of varying the number of denoising steps on the performance of GDMTD3. As shown in Fig. 9, increasing the number of denoising steps generally improves the performance of the diffusion model by enabling more precise noise reduction. However, beyond a certain step, which is 4in the context of our formulated ASCEE-MOP, the benefits of additional denoising steps diminish. This is because increasing the denoising steps can cause the model to overfit the noise pattern. As a result, unnecessary details appear in the generated actions, reducing their quality. The result demonstrates the importance of selecting an appropriate number of denoising steps to balance performance and computational efficiency in the specific problem.

<!-- image-->  
Fig. 9. Comparison of curves of GDMTD3 with different denoising steps.

<!-- image-->  
Fig. 10. Comparison of curves of GDMTD3 with different UAV numbers.

4) Impact of Number of UAVs: To verify the impact of the number of UAVs on system performance, we performed a detailed simulation under varying numbers of UAVs. As shown in Fig. 10, the average secrecy rate of the system improves significantly with the initial increase in the number of UAVs. Specifically, when the number of UAVs increases from 4 to 8, the average secrecy rate per step rises from 5.58 bps/Hz to approximately 7.24 bps/Hz. This improvement is mainly attributed to the more accurate CB capabilities provided by the denser UAV network. However, the increase in the number of

<!-- image-->  
Fig. 11. Performance analysis under imperfect phase synchronization.

UAVs also leads to higher overall flight energy consumption. For instance, when the number of UAVs increases from 8 to 16, the average flight energy consumption per step of the system rises from approximately 1879.85 J to 2850.38 J. Moreover, we can notice that after the number of UAVs reaches a certain threshold, the improvement in terms of secrecy rate tends to saturate, while energy consumption still continues to increase. This may be because as the density of UAVs in the fixed space increases, the distance between array elements decreases, potentially leading to increased mutual coupling and interference among UAVs. Consequently, adding more UAVs beyond this number does not significantly enhance the security performance of the system.

5) Impact of Imperfect Phase Synchronization: Imperfect phase synchronization in the process of CB has a negative impact on performance. To quantify this effect, we executed a set of simulations under different imperfect phase synchronization conditions. The detailed mathematical modeling, including the AF considering phase error and the associated phase error distribution, is presented in the Appendix D of the supplementary material, available online. Specifically, a larger Î³ value indicates a smaller phase error. Fig. 11 shows the average secrecy rate per step under different synchronization conditions. It can be seen from the figure that the secure communication performance decreases as the phase synchronization error increases. However, the degradation in performance is generally within acceptable limits, supported by existing mitigation techniques such as closed-loop and open-loop methods [69]. Continued advancements in synchronization algorithms are expected to further ameliorate these effects and enhance system robustness.

## VII. CONCLUSION

In this work, we investigated a novel UAV swarm-enabled secure surveillance network system, where a UAV swarm perform CB to enhance the security performance between UAV swarm and RBS so as to resist eavesdropping attacks from mobile eavesdroppers. Moreover, we formulated an ASCEE-MOP with an aim to maximize the secrecy rate of the system while minimizing the flight energy consumption of the UAV swarm by optimizing both the excitation current weights and positions of UAVs in conjunction. To solve the non-convex, NP-hard and dynamic optimization problem, we introduced GDMTD3, which effectively captures the high-dimensional probabilistic distributions required for optimal policy decisions. Simulation results demonstrated that the GDMDRL approach outperforms various deployment policies in terms of both the secrecy rate of the system and the flight energy consumption of the UAV swarm. Additionally, the results highlighted the superiority of the GDMTD3 algorithm over several advanced DRL benchmarks in solving the formulated ASCEE-MOP.

## REFERENCES

[1] T. Samad, J. S. Bay, and D. N. Godbole, âNetwork-centric systems for military operations in urban terrain: The role of UAVs,â Proc. IEEE, vol. 95, no. 1, pp. 92â107, Jan. 2007.

[2] K. Liu and J. Zheng, âUAV trajectory optimization for time-constrained data collection in UAV-enabled environmental monitoring systems,â IEEE Internet Things J., vol. 9, no. 23, pp. 24 300â24 314, Dec. 2022.

[3] R. W. L. Coutinho and A. Boukerche, âUAV-mounted cloudlet systems for emergency response in industrial areas,â IEEE Trans. Ind. Inform., vol. 18, no. 11, pp. 8007â8016, Nov. 2022.

[4] B. Li, Z. Fei, and Y. Zhang, âUAV communications for 5G and beyond: Recent advances and future trends,â IEEE Internet Things J., vol. 6, no. 2, pp. 2241â2263, Apr. 2019.

[5] H. Wang, H. Zhao, W. Wu, J. Xiong, D. Ma, and J. Wei, âDeployment algorithms of flying base stations: 5G and beyond with UAVs,â IEEE Internet Things J., vol. 6, no. 6, pp. 10 009â10 027, Dec. 2019.

[6] Y. Takahashi, Y. Kawamoto, H. Nishiyama, N. Kato, F. Ono, and R. Miura, âA novel radio resource optimization method for relay-based unmanned aerial vehicles,â IEEE Trans. Wirel. Commun., vol. 17, no. 11, pp. 7352â7363, Nov. 2018.

[7] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[8] J. Sun, G. Xu, T. Zhang, X. Yang, M. Alazab, and R. H. Deng, âPrivacyaware and security-enhanced efficient matchmaking encryption,â IEEE Trans. Inf. Forensics Secur., vol. 18, pp. 4345â4360, 2023.

[9] J. Sun et al., âPrivacy-preserving fine-grained data sharing with dynamic service for the cloud-edge IoT,â IEEE Trans. Dependable Secur. Comput., early access, Jul. 23, 2024, doi: 10.1109/TDSC.2024.3432650.

[10] Z. Yin et al., âUAV-assisted physical layer security in multi-beam satelliteenabled vehicle communications,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 3, pp. 2739â2751, Mar. 2022.

[11] Z. Yin, N. Cheng, T. H. Luan, Y. Song, and W. Wang, âDT-assisted multipoint symbiotic security in space-air-ground integrated networks,â IEEE Trans. Inf. Forensics Secur., vol. 18, pp. 5721â5734, 2023.

[12] C. Zhang et al., âUAV swarm-enabled collaborative secure relay communications with time-domain colluding eavesdropper,â IEEE Trans. Mob. Comput., vol. 23, no. 9, pp. 8601â8619, Sep. 2024, doi: 10.1109/TMC.2024.3350885.

[13] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âCommunications and control for wireless drone-based antenna array,â IEEE Trans. Commun., vol. 67, no. 1, pp. 820â834, Jan. 2019.

[14] N. C. Luong et al., âApplications of deep reinforcement learning in communications and networking: A survey,â IEEE Commun. Surv. Tut., vol. 21, no. 4, pp. 3133â3174, Fourth quarter 2019.

[15] Z. Wang, J. J. Hunt, and M. Zhou, âDiffusion policies as an expressive policy class for offline reinforcement learning,â 2022, arXiv:2208.06193.

[16] H. Cao et al., âA survey on generative diffusion models,â IEEE Trans. Knowl. Data Eng., vol. 36, no. 7, pp. 2814â2830, Jul. 2024, doi: 10.1109/TKDE.2024.3361474.

[17] G. Zhang, Q. Wu, M. Cui, and R. Zhang, âSecuring UAV communications via joint trajectory and power control,â IEEE Trans. Wirel. Commun., vol. 18, no. 2, pp. 1376â1389, Feb. 2019.

[18] F. Cheng, G. Gui, N. Zhao, Y. Chen, J. Tang, and H. Sari, âUAV-relayingassisted secure transmission with caching,â IEEE Trans. Commun., vol. 67, no. 5, pp. 3140â3153, May 2019.

[19] Y. Zhou et al., âSecure communications for UAV-enabled mobile edge computing systems,â IEEE Trans. Commun., vol. 68, no. 1, pp. 376â388, Jan. 2020.

[20] X. Sun, W. Yang, and Y. Cai, âSecure communication in noma-assisted millimeter-wave SWIPT UAV networks,â IEEE Internet Things J., vol. 7, no. 3, pp. 1884â1897, Mar. 2020.

[21] A. Li, Q. Wu, and R. Zhang, âUAV-enabled cooperative jamming for improving secrecy of ground wiretap channel,â IEEE Wirel. Commun. Lett., vol. 8, no. 1, pp. 181â184, Feb. 2019.

[22] Y. Cai, Z. Wei, R. Li, D. W. K. Ng, and J. Yuan, âJoint trajectory and resource allocation design for energy-efficient secure UAV communication systems,â IEEE Trans. Commun., vol. 68, no. 7, pp. 4536â4553, Jul. 2020.

[23] A. Gao, Q. Wang, Y. Hu, W. Liang, and J. Zhang, âDynamic role switching scheme with joint trajectory and power control for multi-UAV cooperative secure communication,â IEEE Trans. Wirel. Commun., vol. 23, no. 2, pp. 1260â1275, Feb. 2024.

[24] S. S. Hanna and D. Cabric, âDistributed transmit beamforming: Design and demonstration from the Lab to UAVs,â IEEE Trans. Wirel. Commun., vol. 22, no. 2, pp. 778â792, Feb. 2023.

[25] M. T. Mamaghani, X. Zhou, N. Yang, and A. L. Swindlehurst, âSecure short-packet communications via UAV-enabled mobile relaying: Joint resource optimization and 3D trajectory design,â IEEE Trans. Wirel. Commun., vol. 23, no. 7, pp. 7802â7815, Jul. 2024, doi: 10.1109/TWC.2023.3344802.

[26] W. Fan, Y. Wu, X. Sun, and W. Yang, âRobust secure UAV-enabled multiple user communication with fairness consideration,â in Proc. 2020 Int. Conf. Wirel. Commun. Signal Process., 2020, pp. 1028â1033.

[27] Y. Gao, H. Tang, B. Li, and X. Yuan, âSecuring energy-constrained UAV communications against both internal and external eavesdropping,â IEEE Commun. Lett., vol. 25, no. 3, pp. 749â753, Mar. 2021.

[28] Y. Gao, H. Tang, B. Li, and X. Yuan, âEnergy minimization for robust secure transmission in UAV networks with multiple colluding eavesdroppers,â IEEE Commun. Lett., vol. 25, no. 7, pp. 2353â2357, Jul. 2021.

[29] W. Mao, K. Xiong, Y. Lu, P. Fan, and Z. Ding, âEnergy consumption minimization in secure multi-antenna UAV-assisted MEC networks with channel uncertainty,â IEEE Trans. Wirel. Commun., vol. 22, no. 11, pp. 7185â7200, Nov. 2023.

[30] R. Dong, B. Wang, and K. Cao, âSecurity enhancement of UAV swarm enabled relaying systems with joint beamforming and resource allocation,â China Commun., vol. 18, pp. 71â87, Sep. 2021.

[31] D. Yang et al., âDetFed: Dynamic resource scheduling for deterministic federated learning over time-sensitive networks,â IEEE Trans. Mob. Comput., vol. 23, no. 5, pp. 5162â5178, May 2024.

[32] W. Zhang et al., âOptimizing federated learning in distributed industrial IoT: A multi-agent approach,â IEEE J. Sel. Areas Commun., vol. 39, no. 12, pp. 3688â3703, Dec. 2021.

[33] W. Zhang, N. Tang, D. Yang, R. Guo, H. Zhang, and X. Shen, âDet(Com)2: Deterministic communication and computation integration toward AIGC services,â IEEE Wirel. Commun., vol. 31, no. 3, pp. 32â41, Jun. 2024.

[34] L. Xiao, H. Li, S. Yu, Y. Zhang, L. Wang, and S. Ma, âReinforcement learning based network coding for drone-aided secure wireless communications,â IEEE Trans. Commun., vol. 70, no. 9, pp. 5975â5988, Sep. 2022.

[35] R. Dong, B. Wang, J. Tian, T. Cheng, and D. Diao, âDeep reinforcement learning based UAV for securing mmWave communications,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 5429â5434, Apr. 2023.

[36] Y. Yang et al., âDecentralized cooperative caching and offloading for virtual reality task based on GAN-powered multi-agent reinforcement learning,â IEEE Trans. Serv. Comput., vol. 17, no. 1, pp. 291â305, Jan. 2024.

[37] H. Du et al., âDiffusion-based reinforcement learning for edge-enabled AI-generated content services,â IEEE Trans. Mob. Comput., vol. 23, no. 9, pp. 8902â8918, Sep. 2024, doi: 10.1109/TMC.2024.3356178.

[38] P. Li et al., âFilling the missing: Exploring generative AI for enhanced federated learning over heterogeneous mobile edge devices,â IEEE Trans. Mob. Comput., vol. 23, no. 10, pp. 10 001â10 015, Oct. 2024.

[39] H. Han et al., âPrimary-user-friendly dynamic spectrum anti-jamming access: A GAN-enhanced deep reinforcement learning approach,â IEEE Wirel. Commun. Lett., vol. 11, no. 2, pp. 258â262, Feb. 2022.

[40] D. Chen, Q. Qi, Q. Fu, J. Wang, J. Liao, and Z. Han, âTransformer-based reinforcement learning for scalable multi-UAV area coverage,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 8, pp. 10 062â10 077, Aug. 2024.

[41] N. Su, F. Liu, and C. Masouros, âSensing-assisted eavesdropper estimation: An ISAC breakthrough in physical layer security,â IEEE Trans. Wirel. Commun., vol. 23, no. 4, pp. 3162â3174, Apr. 2024.

[42] D. Migliore, R. Rigamonti, D. Marzorati, M. Matteucci, and D. G. S. Sorrenti, âUse a single camera for simultaneous localization and mapping with mobile object tracking in dynamic environments,â in Proc. ICRA Workshop Safe Navigation Open Dynamic Environ. Appl. Auton. Veh., 2009, pp. 12â17.

[43] Y. Tian, Y. Huo, C. Hu, Q. Gao, and T. Jing, âA location prediction-based physical layer security scheme for suspicious eavesdroppers,â in Proc. 12th Int. Conf. Wirel. Algorithms Syst. Appl., 2017, pp. 854â859.

[44] J. Li, G. Sun, L. Duan, and Q. Wu, âMulti-objective optimization for UAV swarm-assisted IoT with virtual antenna arrays,â IEEE Trans. Mob. Comput., vol. 23, no. 5, pp. 4890â4907, May 2024.

[45] H. Ochiai, P. Mitran, H. V. Poor, and V. Tarokh, âCollaborative beamforming for distributed wireless ad hoc sensor networks,â IEEE Trans. Signal Process., vol. 53, no. 11, pp. 4110â4124, Nov. 2005.

[46] J. Feng, Y. Lu, B. Jung, D. Peroulis, and Y. C. Hu, âEnergy-efficient data dissemination using beamforming in wireless sensor networks,â ACM Trans. Sens. Netw., vol. 9, no. 3, pp. 31:1â31:30, Jun. 2013.

[47] A. Al-Hourani, K. Sithamparanathan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wirel. Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[48] S. K. Nobar, M. H. Ahmed, Y. Morgan, and S. A. Mahmoud, âResource allocation in cognitive radio-enabled UAV communication,â IEEE Trans. Cogn. Commun. Netw., vol. 8, no. 1, pp. 296â310, Mar. 2022.

[49] A. Meng, X. Gao, Y. Zhao, and Z. Yang, âThree-dimensional trajectory optimization for energy-constrained UAV-enabled IoT system in probabilistic LoS channel,â IEEE Internet Things J., vol. 9, no. 2, pp. 1109â1121, Jan. 2022.

[50] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wirel. Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[51] R. He, B. Ai, G. L. StÃ¼ber, and Z. Zhong, âNon-stationary mobileto-mobile channel modeling using the Gauss-Markov mobility model,â in Proc. 9th Int. Conf. Wirel. Commun. Signal Process., 2017, pp. 1â6.

[52] S. Fujimoto, H. van Hoof, and D. Meger, âAddressing function approximation error in actor-critic methods,â in Proc. 35th Int. Conf. Mach. Learn., 2018, pp. 1582â1591.

[53] T. P. Lillicrap et al., âContinuous control with deep reinforcement learning,â 2018, arXiv:1509.02971.

[54] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction, 2nd ed. Cambridge, MA, USA: MIT Press, Nov. 2018.

[55] H. GM, M. K. Gourisaria, M. Pandey, and S. S. Rautaray, âA comprehensive survey and analysis of generative models in machine learning,â Comput. Sci. Rev., vol. 38, Nov. 2020, Art. no. 100285.

[56] L. Yang et al., âDiffusion models: A comprehensive survey of methods and applications,â ACM Comput. Surv., vol. 56, no. 4, pp. 105:1â105:39, Apr. 2024.

[57] J. Ho, A. Jain, and P. Abbeel, âDenoising diffusion probabilistic models,â in Proc. 34th Int. Conf. Neural Inf. Process. Syst., 2020, pp. 6840â6851.

[58] Z. Xiao, K. Kreis, and A. Vahdat, âTackling the generative learning trilemma with denoising diffusion GANs,â 2022, arXiv:2112.07804.

[59] M. Chen, Z. Yang, W. Saad, C. Yin, H. V. Poor, and S. Cui, âA joint learning and communications framework for federated learning over wireless networks,â IEEE Trans. Wirel. Commun., vol. 20, no. 1, pp. 269â283, Jan. 2021.

[60] R. I. B. Yaliniz, A. El-Keyi, and H. Yanikomeroglu, âEfficient 3-D placement of an aerial base station in next generation cellular networks,â in Proc. 2016 IEEE Int. Conf. Commun., 2016, pp. 1â5.

[61] X. Glorot, A. Bordes, and Y. Bengio, âDeep sparse rectifier neural networks,â in Proc. 14th Int. Conf. Artif. Intell. Statist., 2011, pp. 315â323.

[62] D. P. Kingma and J. Ba, âAdam: A method for stochastic optimization,â 2015, arXiv:1412.6980.

[63] D. Misra, âMish: A self regularized non-monotonic activation function,â 2019, arXiv:1908.08681.

[64] T. Haarnoja et al., âSoft actor-critic algorithms and applications,â 2018, arXiv:1812.05905.

[65] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, âProximal policy optimization algorithms,â 2017, arXiv:1707.06347.

[66] A. Vaswani et al., âAttention is all you need,â in Proc. 31st Int. Conf. Neural Inf. Process. Syst., 2017, pp. 5998â6008.

[67] C. Colas, O. Sigaud, and P. Oudeyer, âHow many random seeds? Statistical power analysis in deep reinforcement learning experiments,â 2018, arXiv:1806.08295.

[68] A. Q. Nichol and P. Dhariwal, âImproved denoising diffusion probabilistic models,â in Proc. 38th Int. Conf. Mach. Learn., 2021, pp. 8162â8171.

[69] S. Jayaprakasam, S. K. A. Rahim, and C. Y. Leow, âDistributed and collaborative beamforming in wireless sensor networks: Classifications, trends, and research directions,â IEEE Commun. Surv. Tut., vol. 19, no. 4, pp. 2092â2116, Fourth Quarter 2017.

<!-- image-->

Chuang Zhang received the BS degree in computer science and technology from Jilin University, Changchun, China, in 2021, where he is currently working toward the PhD degree with the College of Computer Science and Technology. His current research interests include UAV communications, secure communications, distributed beamforming, and multi-objective optimization.

<!-- image-->

Geng Sun (Senior Member, IEEE) received the BS degree in communication engineering from Dalian Polytechnic University, in 2011 and the PhD degree in computer science and technology from Jilin University, in 2018. He was a visiting researcher with the School of Electrical and Computer Engineering, Georgia Institute of Technology, USA. He is a professor with the College of Computer Science and Technology, Jilin University, and His research interests include wireless networks, UAV communications, collaborative beamforming, and optimizations.

<!-- image-->

Jiahui Li (Member, IEEE) received the BS degree in software engineering, and the MS and PhD degrees in computer science and technology from Jilin University, Changchun, China, in 2018, 2021, and 2024, respectively. He was a visiting PhD student with the Singapore University of Technology and Design (SUTD). He currently serves as an assistant researcher with the College of Computer Science and Technology, Jilin University. His current research focuses on integrated air-ground networks, UAV networks, wireless energy transfer, and optimization.

<!-- image-->

Qingqing Wu (Senior Member, IEEE) received the BEng and PhD degrees in electronic engineering from the South China University of Technology and Shanghai Jiao Tong University (SJTU) in 2012 and 2016, respectively. From 2016 to 2020, he was a research fellow with the Department of Electrical and Computer Engineering, National University of Singapore. He is currently an associate professor with Shanghai Jiao Tong University. His current research interest includes intelligent reflecting surface (IRS), unmanned aerial vehicle (UAV) communications, and

MIMO transceiver design. He has coauthored more than 100 IEEE journal papers with 26 ESI highly cited papers and 8 ESI hot papers, which have received more than 30,000 Google citations. He was listed as the Clarivate ESI Highly Cited Researcher in 2022 and 2021, the Most Influential Scholar Award in AI-2000 by Aminer in 2021 and Worldâs Top 2% Scientist by Stanford University in 2020 and 2021. He was the recipient of the IEEE Communications Society Asia Pacific Best Young Researcher Award and Outstanding Paper Award in 2022, the IEEE Communications Society Young Author Best Paper Award in 2021, the Outstanding PhD Thesis Award of China Institute of Communications in 2017, the Outstanding PhD Thesis Funding in SJTU in 2016, the IEEE ICCC Best Paper Award in 2021, and IEEE WCSP Best Paper Award in 2015. He was the Exemplary editor of IEEE Communications Letters in 2019 and the Exemplary Reviewer of several IEEE journals. He serves as an associate editor for IEEE Transactions on Communications, IEEE Communications Letters, IEEE Wireless Communications Letters, IEEE Open Journal of Communications Society (OJ COMS), and IEEE Open Journal of Vehicular Technology (OJVT). He is the lead guest editor for IEEE Journal on Selected Areas in Communications on âUAV Communications in 5G and Beyond Networksâ, and the guest editor for IEEE Open Journal of Vehicular Technology on â6G Intelligent Communicationsâ and IEEE Open Journal of Communications Society on âReconfigurable Intelligent Surface-Based Communications for 6G Wireless Networksâ. He is the workshop co-chair for IEEE ICC 2019-2022 workshop on âIntegrating UAVs into 5G and Beyondâ, and the workshop co-chair for IEEE GLOBECOM 2020 and ICC 2021 workshop on âReconfigurable Intelligent Surfaces for Wireless Communication for Beyond 5Gâ. He serves as the Workshops and Symposia Officer of Reconfigurable Intelligent Surfaces Emerging Technology Initiative and Research Blog Officer of Aerial Communications Emerging Technology Initiative. He is the IEEE Communications Society Young Professional chair in Asia Pacific Region.

<!-- image-->

<!-- image-->  
Jiacheng Wang received the PhD degree from the School of Communications and Information Engineering, Chongqing University of Posts and Telecommunications, Chongqing, China. He is the research fellow with the College of Computing and Data Science, Nanyang Technological University, Singapore. His research interests include wireless sensing, semantic communications, and generative AI, Metaverse.

Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand, in 1999, and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada, in 2008. He is currently a professor with the College of Computing and Data Science, Nanyang Technological University, Singapore. His research interests include the Internet of Things (IoT), machine learning, and incentive mechanism design.

<!-- image-->

Yuanwei Liu (Fellow, IEEE) received the PhD degree from QMUL in 2016. He is a tenured full professor with the Department of Electrical and Electronic Engineering (EEE) at The University of Hong Kong (HKU) and a visiting professor with the Queen Mary University of London (QMUL). Prior to that, he was a senior lecturer (associate professor) (2021- 2024) and a lecturer (assistant professor) (2017-2021) with QMUL, London, U.K, and a postdoctoral research fellow (2016-2017) with Kingâs College London (KCL), London. His research interests include non-orthogonal multiple access, reconfigurable intelligent surface, near field communications, integrated sensing and communications, and machine learning. He is a fellow of AAIA, a Web of Science Highly Cited researcher, an IEEE Communication Society distinguished lecturer, an IEEE Vehicular Technology Society distinguished lecturer, the rapporteur of ETSI Industry Specification Group on Reconfigurable Intelligent Surfaces on work item of âMulti-functional Reconfigurable Intelligent Surfaces (RIS): Modeling, Optimisation, and Operationâ, and the U.K. representative for the URSI Commission C on âRadio communication Systems and Signal Processingâ. He was listed as one of 35 Innovators Under 35 China in 2022 by MIT Technology Review. He received IEEE ComSoc Outstanding Young Researcher Award for EMEA in 2020. He received the 2020 IEEE Signal Processing and Computing for Communications (SPCC) Technical Committee Early Achievement Award, IEEE Communication Theory Technical Committee (CTTC) 2021 Early Achievement Award. He received IEEE ComSoc Outstanding Nominee for Best Young Professionals Award in 2021. He is the co-recipient of the 2024 IEEE Communications Society Heinrich Hertz Award, the Best Student Paper Award in IEEE VTC2022-Fall, the Best Paper Award in ISWCS 2022, the 2022 IEEE SPCC-TC Best Paper Award, the 2023 IEEE ICCT Best Paper Award, and the 2023 IEEE ISAP Best Emerging Technologies Paper Award. He serves as the coeditor-in-chief of IEEE ComSoc TC Newsletter, an area editor of IEEE Transactions on Communications and IEEE Communications Letters, an editor of IEEE Communications Surveys & Tutorials, IEEE Transactions on Wireless Communications, IEEE Transactions on Vehicular Technology, IEEE Transactions on Network Science and Engineering, and IEEE Transactions on Cognitive Communications and Networking. He serves as the (leading) guest editor for Proceedings of the IEEE on Next Generation Multiple Access, IEEE JSAC on Next Generation Multiple Access, IEEE JSTSP on Intelligent Signal Processing and Learning for Next Generation Multiple Access, and IEEE Network on Next Generation Multiple Access for 6G. He serves as the Publicity co-chair for IEEE VTC 2019-Fall, the Panel co-chair for IEEE WCNC 2024, Symposium co-chair for several flagship conferences such as IEEE GLOBECOM, ICC and VTC. He serves the academic chair for the Next Generation Multiple Access Emerging Technology Initiative, vice chair of SPCC and Technical Committee on Cognitive Networks (TCCN).

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_5_img_1.png|page_5_img_1]]
2. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_11_img_1.jpeg|page_11_img_1]]
3. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_12_img_1.png|page_12_img_1]]
4. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_13_img_1.jpeg|page_13_img_1]]
5. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_13_img_2.png|page_13_img_2]]
6. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_15_img_1.png|page_15_img_1]]
7. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_15_img_2.png|page_15_img_2]]
8. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_15_img_3.png|page_15_img_3]]
9. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_17_img_1.jpeg|page_17_img_1]]
10. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_17_img_2.jpeg|page_17_img_2]]
11. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_17_img_3.jpeg|page_17_img_3]]
12. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_17_img_4.jpeg|page_17_img_4]]
13. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_18_img_1.jpeg|page_18_img_1]]
14. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_18_img_2.jpeg|page_18_img_2]]
15. [[../extracted_images/Zhang-2025-Multi-Objective Aerial Collaborativ/page_18_img_3.jpeg|page_18_img_3]]

---

