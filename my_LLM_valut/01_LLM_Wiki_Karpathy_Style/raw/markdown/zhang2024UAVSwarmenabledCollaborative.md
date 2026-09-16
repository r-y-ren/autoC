# UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper

Chuang Zhang , Geng Sun , Member, IEEE, Qingqing Wu , Senior Member, IEEE, Jiahui Li , Student Member, IEEE, Shuang Liang , Dusit Niyato , Fellow, IEEE, and Victor C.M. Leung , Life Fellow, IEEE

AbstractâUnmanned aerial vehicles (UAVs) as aerial relays are practically appealing for assisting the Internet of Things (IoT) network. In this article, we aim to utilize a UAV swarm to assist the secure communication between the micro base station (MBS) equipped with the planar antenna array (PAA) and the IoT terminal devices by collaborative beamforming (CB), so as to counteract the effects of the eavesdropper colluding in the time domain. Specifically, we formulate a UAV swarm-enabled secure relay multiobjective optimization problem (US2RMOP) for simultaneously maximizing the achievable sum rate of the associated IoT terminal devices, minimizing the achievable sum rate of the eavesdropper and minimizing the energy consumption of UAV swarm, by jointly optimizing the excitation current weights of both MBS and UAV swarm, the selection of the UAV receiver, the position of UAVs and user association order of IoT terminal devices. Furthermore, the formulated US2RMOP is proved to be a non-convex, NP-hard and large-scale optimization problem. Therefore, we propose an improved multi-objective grasshopper algorithm (IMOGOA) with some specific designs to address the problem. Simulation results

exhibit the effectiveness of the proposed UAV swarm-enabled collaborative secure relay strategy and demonstrate the superiority of IMOGOA.

## I. INTRODUCTION

Index TermsâUAV swarm, collaborative beamforming, collusive eavesdropping, secure communication, multi-objective optimization.

D UE to decreasing cost and advancements in manufacturingtechnology, unmanned aerial vehicles (UAVs) have a significant impact on military and commercial applications [2], [3]. Especially in the field of wireless networks, UAVs have created a boom and derived a lot of new application scenarios in industry and academia. Integrating UAVs into the incorporated network system becomes a foregone choice for the space-air-groundaqua network [4], [5], [6]. For example, a UAV can be regarded as an aerial base station to assist the Internet of Things (IoT) terminal devices for data upload scenarios [7], [8], wherein these devices have limited transmission power and do not have the ability to communicate over long distances. Moreover, a UAV can also act as an aerial user to access terrestrial networks for environmental monitoring and goods delivery [9]. In addition, extending limited network coverage in post-disaster rescue can be efficiently achieved by the UAV-enabled multi-hop relay strategy [10].

The UAV-enabled relay communication is a process leveraging UAVs relay some information between ground-based communication equipment, which can expand the reach of network. Generally, UAVs can be divided into two types according to their flight modes, i.e., fixed-wing UAVs and rotary-wing UAVs. Compared with fixed-wing UAVs, rotary-wing UAVs can take off or land vertically and hover, which are easier to be deployed and provide more stable relay communications. However, using a single rotary-wing UAV as a high-rate relay to assist the terrestrial network system is a challenging task due to the restricted battery capacity and limited transmit power. For example, in some long-distance communication settings, the UAV relay must first move to a position near the sender before moving to a position near the receiver, which significantly reduces the network lifetime and efficiency. Moreover, due to the broadcast nature of the wireless channel in UAV-enabled relay communications, the

Digital Object Identifier 10.1109/TMC.2024.3350885 security is a key issue that should be taken into account seriously. Although UAVs flying at the higher altitude provide line-ofsight (LoS) dominant channels for wireless communications, these links are also more vulnerable to eavesdropping attacks, especially for the UAV swarm-enabled multi-hop relay strategy since the risk of eavesdropping increases with the increase of the number of hops. Generally, the security can be regarded as a higher layer communication protocol stack design concern that could be addressed by using encryption methods. However, this requires high computational ability [11], which is not suitable for UAVs with limited resources.

Fortunately, collaborative beamforming (CB) [12], [13], as a communication technique originally used in wireless sensor networks, can enhance the signal strength and directivity. CB has garnered significant attention from researchers who seek to address the issue of secure and effective communications [14], [15]. Thus, it is reasonable to introduce CB for UAV swarm to assist terrestrial communications. Specifically, a UAV swarmenabled virtual antenna array (UVAA) consisting of multiple UAVs can greatly improve the signal strength in a special direction by controlling the radio energy distribution, thereby increasing the transmission rate and enhancing the security of the UAV swarm-enabled relay system. Nevertheless, the UAV swarm-enabled collaborative secure relay communication system based on CB needs to consider several key factors. For example, UAVs in UVAA can move to suitable positions for achieving the higher achievable rate of legitimate user and the lower achievable rate of eavesdropper. However, this significantly causes additional energy consumption because of the movement of UAVs. Moreover, the excitation current weights of UVAA are crucial factors for the beam pattern which should be considered at the same time. Additionally, it needs to adopt the necessary approach to reduce the risk of eavesdropping for the source, e.g., the selection of UAV receiver is an important factor because this can cause different wiretap rates in CB information fusion phase. Thus, obtaining the more proper positions and excitation current weights of UAVs, selecting the appropriate UAV receiver for excellent and secure communication performance, and simultaneously reducing the movement energy consumption of the UAV swarm for the collaborative secure relay communication system are of importance. In this work, we further consider the joint optimization of MBS and UVAA under the threat of an time-domain collusive eavesdropper in the complete relay communication process, which is a more practical scenario and a more comprehensive problem compared to [16]. The major contributions of this work are summarized as follows.

UAV Swarm-enabled Collaborative Secure Relay System Construction: We consider a secure relay communication scenario, where a UAV swarm-enabled collaborative secure relay system is constructed for transmitting confidential information from the source MBS with the planar antenna array (PAA) to the remote IoT terminal devices so as to counteract the threat of the eavesdropper colluding in the time domain. To the best of our knowledge, this is the first work that considers the complete secure relay communication process from the source MBS to the remote IoT terminal devices assisted by the UAV swarm-enabled CB under the threat of a time-domain collusive eavesdropper. Compared to existing works [16], [17], the considered system is more comprehensive and practical.

- Multi-objective Optimization Problem Formulation: We formulate a UAV swarm-enabled secure relay multiobjective optimization problem (US2RMOP) aiming to cooperatively maximize the achievable sum rate between the MBS and multiple remote IoT terminal devices, minimize the achievable sum rate of eavesdropper, and minimize the traveling energy consumption of the UAV swarm, by jointly optimize excitation current weights of both MBS and UAV swarm, the selection of the UAV receiver, the position of each UAV and user association order of IoT terminal devices. Furthermore, the formulated US2RMOP is proven to be a non-convex, large-scale optimization and NP-hard problem.

- Algorithm Design: Due to the complex constraints and high-dimensional decision space of the US2RMOP, reinforcement learning and convex optimization algorithms face significant challenges, e.g., the curse of dimensionality and difficult convex relaxation. Therefore, we design an improved multi-objective grasshopper algorithm (IMOGOA) to solve the formulated US2RMOP. First, IMOGOA adopts half-Halton-half-chaos (H3C) and dynamic eliminationbased crowding distance (DCDE) strategies to improve the distribution of the population. Moreover, the non-linear decreasing factor is used to better coordinate exploitation and exploration in IMOGOA. Additionally, we introduce LÃ©vy flight and archive update strategies to enhance the ability of going beyond the local optimum. The interaction among the aforementioned improvements enables IMOGOA to accomplish better diversity and uniformity when dealing with the formulated US2RMOP.

C Simulation Validation: Simulation results illustrate the performance of the proposed IMOGOA by comparing it with some benchmarks. Moreover, the traditional UAV swarm-enabled multi-hop relay and linear antenna array strategies are introduced to verify the practicability of the UAV swarm-enabled collaborative secure relay communication system. In addition, the performance comparison of the proposed IMOGOA under two schemes with multiple eavesdroppers is further analyzed.

The rest of this article is organized as follows. Section II introduces some related work. Section III provides the system model and preliminaries. The US2RMOP is detailed and analyzed in Section IV. Section V designs the multi-objective optimization algorithm. Section VI shows simulation results and the conclusion of this article is presented in Section VIII.

## II. RELATED WORK

In this section, the related works on UAV-enabled relay communications, UAV-enabled secure communications and UAVenabled CB communications are discussed.

## A. UAV-Enabled Relay Communications

Ono et al. [18] proposed a wireless relay network model, where a fixed-wing UAV serves as a resilient moving relay among the ground stations with disconnected communication links in the event of disasters. Dabiri et al. [19] studied the performance of fixed-wing UAV-based millimeter wave backhaul networks by considering the effects of realistic physical parameters, such as the UAVâs circular path, flight altitude, tracking error, real 3D antenna pattern, temperature and air pressure, etc. On the other hand, there are some works that use rotary-wing UAVs as aerial relays. For instance, in [20], the authors utilized a rotary-wing UAV serving as a relay between ground nodes dispersed in a circular cell and a central base station by optimizing the trajectory of UAV to minimize the expected average communication delay to service data transmission requests. Fan et al. [21] used one static rotary-wing UAV working on frequency division multiplexing as a relay to serve multiple user pairs on the ground, where the optimal relay position was adjusted to maximize the system throughput.

## B. UAV-Enabled Secure Communications

To prevent a ground eavesdropper, Zhong et al. [22] made use of the power and trajectory controls of both the UAV transmitter and a friendly UAV jammer. In [23], the authors proposed a dual-UAV enabled secure communication network involving multiple legitimate users and ground eavesdroppers, and the minimum worst-case secrecy rate for legitimate users was maximized by jointly optimizing the trajectory of UAV and user scheduling. Zhou et al. [24] investigated how friendly UAV jamming power and the corresponding three-dimensional deployment affected the likelihood of legitimate receivers being interrupted and the likelihood of unknown eavesdroppers being intercepted. Sun et al. [25] analyzed the secure performance of mmWave NOMA systems with both legitimate users and eavesdroppers by taking into account the spatial correlation between the selected legitimate users and eavesdroppers. In [26], the authors used a novel iterative approach to jointly optimize the time schedule and trajectory of UAV to assure the security of UAV-relayed wireless networks. Na et al. [27] considered a relay scenario by jointly optimizing the resource allocation and UAV trajectory to maximize the minimum average secrecy rate among all IoT terminal devices. Moreover, in [28], the authors explored secure transmission in a cache-enabled UAV relay network with D2D communication and eavesdroppers. Specifically, they maximized the minimum secrecy rate between users by concurrently optimizing the scheduling, trajectory and transmission power of UAV and user association.

## C. UAV-Enabled CB Communications

Mohanti et al. [29] designed a UAV swarm-enabled CB framework and verified the feasibility of this scheme under air-to-ground channels. Mozaffari et al. [30] investigated a UAV swarm-enabled CB technique for providing network service to ground users. Specifically, minimizing the service time by reducing the wireless transmission time as well as control time for the UAV movement and stabilization are considered. Dinh et al. [31] proposed a communication mode that considered both the flexible deployment and CB transmission of UAVs to maximize the number of admitted users by jointly optimizing the transmit beamforming, user admission decision, position planning and content placement. Zhu et al. [32] studied a UAV swarm-enabled CB relay system, wherein minimizing the total transmit power of the UAV relays within the interference limits of the primary network and the quality of service (QoS) requirements of cognitive networks is formulated. Furthermore, Li et al. [17] investigated a secure communication system where the UAVs communicate with multiple base stations by utilizing CB. In addition, in [16], Sun et al. made use of CB to realize secure and energy-efficient communications for different terrestrial base stations.

<!-- image-->  
Fig. 1. Illustration of UAV swarm-enabled collaborative secure relay communication system, where a UAV swarm is introduced to relay confidential messages between MBS (equipped with a PAA) and multiple IoT terminal devices via CB, and a ground eavesdropper performs eavesdropping in a time-domain colluding manner. Solid and dashed lines represent legitimate communication links and wiretap links, respectively.

The primary distinctions between this work and the aforementioned research are seen that we consider a complete secure relay communication process between the MBS and remote IoT terminal devices in a UAV swarm-assisted terrestrial IoT network. Moreover, we study the more difficult scenario of security assurance, where the ground eavesdropper adopts a maximal ratio combining (MRC) technology in the time domain for the relay process [33].

## III. SYSTEM MODEL AND PRELIMINARIES

As illustrated in Fig. 1, we consider multiple secure communications from a source MBS S to T associated IoT terminal devices expressed as $\mathcal { D } = \{ D _ { 1 } , D _ { 2 } , . . . , D _ { T } \}$ . Specifically, S is equipped with a M Ã N PAA to enhance the spatial resolution. However, due to the existence of obstacles, all direct communication links from S to D are blocked. Moreover, a ground eavesdropper E potentially intercepts information during communications in the system. Thus, a rotary-wing UAV swarm consisting of $K \ \mathrm { \ U A V s { 1 } }$ , denoted as ${ \mathcal { U } } = \{ U _ { 1 } , U _ { 2 } , . . . , U _ { K } \}$ form a virtual antenna array to relay confidential messages via CB. Here, each UAV is equipped with an omni-directional antenna with the full-duplex mode and the exact position of $\mathcal { E }$ can be detected by a radar [34] or an optical camera [35].

In the considered system, the ith communication process between S and the associated IoT terminal devices has three phases:

- Phase I: In this phase, the information is transmitted from S to the UAV swarm. Specifically, S employs traditional beamforming to transmit information to the selected UAV denoted as $U _ { k }$ in the UAV swarm, and the link between S and $U _ { k }$ is denoted as $S 2 U _ { k } ( i )$

- Phase II: In this phase, the information fusion is conducted in the UAV swarm. Specifically, $U _ { k }$ serves as the cluster leader, and it broadcasts the received message from $\boldsymbol { \mathcal { S } }$ to other UAVs directly2. To simplify this problem, we assume that all individuals in the UAV swarm can communicate with each other at a high rate within the cluster3.

- Phase III: On the basis of the Phase II, the UAV swarm forwards the information to the associated IoT terminal device $D _ { i }$ via CB, and the link between UVAA center and $D _ { i }$ is denoted as C2D(i).

Moreover, E is within the coverage of the MBS and UAV swarm, and it can perform eavesdropping by MRC to maximize the eavesdropping rate during all three phases above. Specifically, the wiretap links in phases I, II and III are denoted as $S 2 \mathcal { E } ( i ) , U _ { k } 2 \mathcal { E } ( i )$ and $\mathcal { C } 2 \mathcal { E } ( i )$ , respectively.

Without loss of generality, a 3D Cartesian coordinate system is considered, where the positions of S, IoT terminal devices and E are fixed. Specifically, the position of the mth array element of PAA arranged in rows is denoted as $( x _ { m } ^ { P } , y _ { m } ^ { P } , z _ { m } ^ { P } )$ . Moreover, the positions of the ith IoT terminal device and the kth UAV are expressed as $( x _ { i } ^ { D } , y _ { i } ^ { D } , z _ { i } ^ { D } )$ and $( x _ { k } ^ { U } , y _ { k } ^ { U } , z _ { k } ^ { U } )$ , respectively. Moreover, the positions of the PAA and UVAA centers are denoted as $\left( x _ { P } , y _ { P } , z _ { P } \right)$ and $\left( x _ { C } , y _ { C } , z _ { C } \right)$ , respectively.

To simplify the expression, $[ \overline { { x _ { m } ^ { P } } } , \overline { { y _ { m } ^ { P } } } , \overline { { z _ { m } ^ { P } } } ]$ and $[ \overline { { x _ { k } ^ { C } } } , \overline { { y _ { k } ^ { C } } } , \overline { { z _ { k } ^ { C } } } ]$ denote the 3D-component distances of array element m and k to the centers of the PAA and UVAA, respectively. Moreover, we denote the link pair sets of ground-to-air (G2A), ground-to-ground (G2G) and air-to-ground (A2G) as G2A = $\bar { \{ \xi 2 U _ { k } ( i ) \vert \bar { k } = 1 , . . . , K , i = 1 , . . . , \bar { T } \} } , G 2 G = \{ \mathcal { S } 2 \mathcal { E } ( i ) \vert i =$ $1 , . . . , T \} \mathrm { a n d } \ A 2 G = \{ { \mathcal C } 2 D ( i ) | i = 1 , . . . , T \} \cup \{ { \mathcal C } 2 { \mathcal E } ( i ) | i =$ $1 , . . . , T \} \cup \{ U _ { k } \mathcal { E } ( i ) | k = 1 , . . . , K , i = 1 , . . . , T \}$ , respectively.

## A. Channel Model

In this section, the channel models about the UAV swarmenabled collaborative secure relay communication system are given.

1) G2A and A2G Channels: UAVs can bring a higher probability of LoS links for communications compared to groundbased equipment. However, the simplified LoS channel model is not sufficient to accurately characterize the signal propagation in complex environments for G2A and A2G links. In this work, we adopt the angle-dependent probabilistic LoS channel model [36], which is described as

$$
P _ { l p } ^ { L o S } = \frac { 1 } { 1 + a e ^ { - b ( \zeta _ { l p } - a ) } } , l p \in G 2 A \cup A 2 G ,\tag{1}
$$

where a and b represent the parameters of the activation function $( S \mathrm { - c u r v e } )$ as attributed to the environments. Moreover, $\zeta _ { l p } = \arctan ( d v _ { l p } / d h _ { l p } )$ denotes the elevation angle between the sender and receiver, wherein $d v _ { l p }$ and $d h _ { l p }$ are the vertical and horizontal distances between the sender and receiver, respectively. Then, the NLoS probability is calculated by $P _ { l p } ^ { N L o S } =$ $1 - P _ { l p } ^ { L o S }$

Furthermore, the channel power gain is described as

$$
h _ { l p } = P _ { l p } ^ { L o S } h _ { l p } ^ { L o S } + P _ { l p } ^ { N L o S } h _ { l p } ^ { N L o S } , l p \in G 2 A \cup A 2 G ,\tag{2}
$$

where $h _ { l p } ^ { L o S } = \beta _ { 0 } d _ { l p } ^ { - \alpha _ { L o S } }$ and $h _ { l p } ^ { N L o S } = \mu \beta _ { 0 } d _ { l p } ^ { - \alpha _ { N L o S } }$ denote the channel power gains under the conditions of the LoS and NLoS states, respectively. Moreover, $\beta _ { 0 }$ represents the average channel power gain at a reference distance $d _ { 0 } =$ 1m in the LoS state, $\mu < .$ 1 is the additional signal attenuation factor due to the NLoS propagation, $\alpha _ { L o S }$ and $\alpha _ { N L o S }$ indicate the average path loss exponents for the LoS and NLoS states, respectively, and $d _ { l p }$ represents the distance between the sender and receiver.

2) G2G Channel: For the ground wiretap channel from S to E, we can express the channel power gain as

$$
h _ { l p } = \beta _ { 0 } d _ { l p } ^ { \alpha _ { G } } , l p \in G 2 G ,\tag{3}
$$

where $\alpha _ { G } > 2$ is the path loss exponent for the G2G link.

## B. Array Factor Model

In this work, the excitation current weights of the mth array element arranged in rows of PAA and the kth UAV element in UVAA are denoted as $I _ { m } ^ { P }$ and $I _ { k } ^ { U }$ , respectively. Accordingly, the array factor (AF) [37] of PAA can be mathematically given as

$$
\begin{array} { l } { { \displaystyle A F _ { P } ( \theta ^ { P } , \varphi ^ { P } | \theta _ { 0 } ^ { P } , \varphi _ { 0 } ^ { P } ) = } } \\ { ~ \displaystyle \sum _ { m = 1 } ^ { M \times N } I _ { m } ^ { P } e ^ { j \Psi _ { m } ^ { P } ( \theta _ { 0 } ^ { P } , \varphi _ { 0 } ^ { P } ) } e ^ { j } [ c _ { p } ( \overline { { { x _ { m } ^ { P } } } } \sin \theta ^ { P } \cos \varphi ^ { P } } \\ { ~ + \overline { { { y _ { m } ^ { P } } } } \sin \theta ^ { P } \sin \varphi ^ { P } + \overline { { { z _ { m } ^ { P } } } } \cos \theta ^ { P } ) ] , } \end{array}\tag{4}
$$

where $\theta ^ { P } \in [ 0 , \pi ]$ and $\varphi ^ { P } \in [ - \pi , \pi ]$ are the elevation and azimuth angles at the center of PAA, respectively. Moreover, $c _ { p } =$ $2 \pi / \lambda$ represents the phase constant, and Î» is the wavelength. According to [16], $\bar { \Psi _ { m } ^ { P } }$ represents the initial phase of the mth array element of PAA and can be determined as

$$
\begin{array} { l } { { \Psi _ { m } ^ { P } ( \theta _ { 0 } ^ { P } , \varphi _ { 0 } ^ { P } ) = } } \\ { { - { \displaystyle \frac { 2 \pi } { \lambda } } ( \overline { { { x _ { m } ^ { P } } } } \sin \theta _ { 0 } ^ { P } \cos \varphi _ { 0 } ^ { P } + \overline { { { y _ { m } ^ { P } } } } \sin \theta _ { 0 } ^ { P } \sin \varphi _ { 0 } ^ { P } + \overline { { { z _ { m } ^ { P } } } } \cos \theta _ { 0 } ^ { P } ) , } } \end{array}\tag{5}
$$

where $( \theta _ { 0 } ^ { P } , \varphi _ { 0 } ^ { P } )$ represents the direction of the designated UAV receiver of PAA. Likewise, the AF of UVAA can be described

as follows:

$$
\begin{array} { l } { { \displaystyle { \cal A F } _ { U } ( \theta ^ { U } , \varphi ^ { U } | \theta _ { 0 } ^ { U } , \varphi _ { 0 } ^ { U } ) = \sum _ { k = 1 } ^ { K } I _ { k } ^ { U } e ^ { j \Psi _ { k } ^ { U } ( \theta _ { 0 } ^ { U } , \varphi _ { 0 } ^ { U } ) } e ^ { j } } } \\ { { \displaystyle \left[ c _ { p } ( \overline { { { x _ { k } ^ { U } } } } \sin \theta ^ { U } \cos \varphi ^ { U } + \overline { { { y _ { k } ^ { U } } } } \sin \theta ^ { U } \sin \varphi ^ { U } + \overline { { { z _ { k } ^ { U } } } } \cos \theta ^ { U } ) \right] } , } \end{array}\tag{6}
$$

where $\theta ^ { U } \in [ 0 , \pi ]$ and $\varphi ^ { U } \in [ - \pi , \pi ]$ are the elevation and azimuth angles at the center of UVAA, respectively. Moreover, $\Psi _ { k } ^ { U }$ is the initial phase of the kth UAV of UVAA, and can be determined by

$$
\begin{array} { l } { { \displaystyle \Psi _ { k } ^ { U } ( \theta _ { 0 } ^ { U } , \varphi _ { 0 } ^ { U } ) = - \frac { 2 \pi } { \lambda } ( \overline { { { x _ { k } ^ { U } } } } \sin \theta _ { 0 } ^ { U } \cos \varphi _ { 0 } ^ { U } } } \\ { { \displaystyle \quad + \overline { { { y _ { k } ^ { U } } } } \sin \theta _ { 0 } ^ { U } \sin \varphi _ { 0 } ^ { U } + \overline { { { z _ { k } ^ { U } } } } \cos \theta _ { 0 } ^ { U } ) , } } \end{array}\tag{7}
$$

where $( \theta _ { 0 } ^ { U } , \varphi _ { 0 } ^ { U } )$ is the direction of the designated associated IoT terminal device.

## C. Achievable Rate Model

In this section, the achievable rates of IoT terminal Devices and the ground eavesdropper are presented.

1) Achievable Rate of the IoT Terminal Device $\mathcal { D } _ { i } .$ : For the phases I and III of the communication process, the signal-tonoise ratio (SNR) of $S 2 U _ { k } ( i )$ and $\mathcal { C } 2 D ( i )$ can be calculated as

$$
\gamma _ { S 2 U _ { k } } ( i ) = \frac { P _ { S } G _ { 0 } ^ { P } h _ { S 2 U _ { k } } ( i ) } { \sigma ^ { 2 } }\tag{8}
$$

and

$$
\gamma _ { \mathcal C 2 \mathcal D } ( i ) = \frac { P _ { U } G _ { 0 } ^ { U } h _ { \mathcal C D } ( i ) } { \sigma ^ { 2 } } ,\tag{9}
$$

where $P _ { S }$ and $P _ { U }$ are the transmission power of PAA and UVAA, respectively. Moreover, $h _ { S 2 U _ { k } } ( i )$ represents the channel power gain between $\boldsymbol { \mathcal { S } }$ and designated UAV receiver $U _ { k }$ in the ith communication process, hC2D(i) is the channel power gain between the UAV swarm and designated IoT terminal device $\mathcal { D }$ in the ith communication process, and the noise power of the channel is represented as $\bar { \sigma } ^ { 2 }$ . In addition, the gain $G _ { 0 } ^ { P }$ and $G _ { 0 } ^ { U }$ of PAA and UVAA towards the legitimate receivers can be respectively calculated as

$$
G _ { 0 } ^ { P } = \frac { 4 \pi \left| A F _ { P } ( \theta _ { 0 } ^ { P } , \varphi _ { 0 } ^ { P } | \theta _ { 0 } ^ { P } , \varphi _ { 0 } ^ { P } ) \right| ^ { 2 } w \left( \theta _ { 0 } ^ { P } , \varphi _ { 0 } ^ { P } \right) ^ { 2 } } { \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \pi } | A F _ { P } ( \theta ^ { P } , \varphi ^ { P } ) | ^ { 2 } w ( \theta ^ { P } , \varphi ^ { P } ) ^ { 2 } \sin \theta ^ { P } \mathrm { d } \theta ^ { P } \mathrm { d } \varphi ^ { P } } \eta _ { P }\tag{10}
$$

and

$$
G _ { 0 } ^ { U } = \frac { 4 \pi \left| A F _ { U } ( \theta _ { 0 } ^ { U } , \varphi _ { 0 } ^ { U } | \theta _ { 0 } ^ { U } , \varphi _ { 0 } ^ { U } ) \right| ^ { 2 } w \left( \theta _ { 0 } ^ { U } , \varphi _ { 0 } ^ { U } \right) ^ { 2 } } { \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \pi } | A F ( \theta ^ { U } , \varphi ^ { U } ) | ^ { 2 } w ( \theta ^ { U } , \varphi ^ { U } ) ^ { 2 } \sin \theta ^ { U } \mathrm { d } \theta ^ { U } \mathrm { d } \varphi ^ { U } } \eta _ { U } ,\tag{11}
$$

where w $\mathbf { \Omega } ( \theta ^ { P } , \varphi ^ { P } )$ and w $( \theta ^ { U } , \varphi ^ { U } )$ represent the magnitude of the far-field beam pattern of each array element in PAA and UVAA, respectively. Moreover, Î·P and Î·U are the antenna efficiencies of PAA and UVAA, respectively. Note that w $\mathbf { \Omega } ( \theta ^ { P } , \varphi ^ { P } )$ and $w ( \theta ^ { U } , \varphi ^ { U } )$ are 0 dB in all directions in this system since we consider each array element of PAA and UVAA equipped with a single isotropic antenna with identical power constraints.

Accordingly, the achievable rate between $\boldsymbol { s }$ and designated IoT terminal device D in the ith communication process can be expressed as

$$
R _ { S 2 D } ( i ) = { \cal B } \log _ { 2 } \left( 1 + \widehat { \operatorname* { m i n } \{ \gamma _ { S 2 U _ { k } } ( i ) , \gamma _ { \mathcal { C } 2 D } ( i ) \} } \right) ,\tag{12}
$$

where B represents the transmission bandwidth, and $\widehat { \operatorname* { m i n } \{ \cdot \} }$ refers to an operator that calculates the minimum value of the two elements. Note that we ignore the SNR limitation of the broadcasting process due to the close individual distance between the UAVs.

2) Achievable Rate of the Ground Eavedropper E: For the phases I, II and III of the ith communication process, the SNRs of three wiretap links, i.e., S2E(i), Uk2E(i) and C2E(i), can be calculated as

$$
\gamma _ { S 2 \mathcal { E } } ( i ) = \frac { P _ { S } G _ { \mathcal { E } } ^ { P } h _ { S 2 \mathcal { E } } ( i ) } { \sigma ^ { 2 } } ,\tag{13}
$$

$$
\gamma _ { U _ { k } 2 \mathcal { E } } ( i ) = \frac { P _ { U _ { k } } h _ { U _ { k } 2 \mathcal { E } } ( i ) } { \sigma ^ { 2 } }\tag{14}
$$

and

$$
\gamma _ { \mathcal C 2 \mathcal E } ( i ) = \frac { P _ { U } G _ { \mathcal E } ^ { U } h _ { \mathcal C 2 \mathcal E } ( i ) } { \sigma ^ { 2 } } ,\tag{15}
$$

where $G _ { \mathcal { E } } ^ { P }$ and $G _ { \mathcal { E } } ^ { U }$ can be calculated according to the same principle as (10) and (11). Moreover, $P _ { U _ { k } }$ represents the broadcast transmission power of $U _ { k }$ in phase II.

Accordingly, the achievable rate of E during the ith communication process can be expressed as

$$
R \varepsilon ( i ) = B \log _ { 2 } \left( 1 + \gamma \varepsilon ( i ) \right) ,\tag{16}
$$

where $\gamma _ { \mathcal { E } } ( i )$ is the maximal SNR obtained by using MRC technique during the ith communication process, and can be calculated as $\gamma _ { \mathcal { E } } ( i ) = \gamma _ { \mathcal { S } 2 \mathcal { E } } ( i ) + \gamma _ { U _ { k } 2 \mathcal { E } } ( i ) + \gamma _ { C \mathcal { E } } ( i )$

## D. Rotary-Wing UAV Energy Consumption Model

For the UAV swarm-enabled collaborative secure relay communication system, the energy consumption of UAVs consists of the communication energy consumption generated by transmitting data and the propulsion energy consumption to overcome air drag and gravity. Furthermore, the communication energy consumption is usually two orders of magnitude smaller than the propulsion energy consumption in practical applications [38]. Therefore, we are only concerned about the propulsion energy consumption of the UAV swarm in this article. According to [2], the energy consumption for a UAV flying in a straight-and-level manner with speed v can be modeled as

$$
\begin{array} { l } { { P ( v ) = P _ { b } \left( 1 + \frac { { 3 v ^ { 2 } } } { { u _ { t i p s } ^ { 2 } } } \right) \ + P _ { i } \left( \sqrt { 1 + \frac { { v ^ { 4 } } } { { 4 u _ { 0 } ^ { 4 } } } } - \frac { { v ^ { 2 } } } { { 2 u _ { 0 } ^ { 2 } } } \right) ^ { \frac { 1 } { 2 } } } } \\ { { \displaystyle \phantom { \frac { 1 } { 2 } } + \frac { 1 } { 2 } d _ { 0 } \rho s A v ^ { 3 } , } } \end{array}\tag{17}
$$

where $P _ { b }$ and $P _ { i }$ are two constants related to the flight speed v, which denote the blade profile power and induced power under the hovering condition, respectively. $u _ { t i p s }$ is the tip speed of the rotor blade, and $u _ { 0 }$ represents the mean rotor-induced velocity in hovering. Moreover, $d _ { 0 }$ and $\rho$ denote the fuselage drag ratio and air density, respectively. s and A denote the rotor solidity and rotor disc area, respectively.

The energy consumption including the UAV climbing and descending with time by using the heuristic closed-form can be measured as

$$
\begin{array} { l } { \displaystyle { E ( T ) \approx \int _ { 0 } ^ { T } P \left( v ( t ) \right) d t + m g \left( h ( T ) - h ( 0 ) \right) } } \\ { \displaystyle { \qquad + \frac { 1 } { 2 } m \left( v ( T ) ^ { 2 } - v ( 0 ) ^ { 2 } \right) , } } \end{array}\tag{18}
$$

where T refers to the duration of flight time, and $v ( t )$ represents the UAV speed at the time instant t. Moreover, g and m denote the gravitational acceleration and the mass of the UAV.

## E. Multi-Objective Optimization Problem

Theoretically, a basic minimization multi-objective optimization problem (MOP) can be modeled as follows:

$$
\begin{array} { r l } & { \operatorname* { m i n } \quad F ( x ) = [ f _ { 1 } ( x ) , f _ { 2 } ( x ) , . . . , f _ { o } ( x ) ] ^ { T } } \\ & { \mathrm { s . t . } g _ { j } ( x ) \leq 0 , j = 1 , 2 , . . . , l } \end{array}\tag{19}
$$

where x is the decision variable, o is the number of the optimization objectives, l is the number of constraints, $f _ { i } ( x )$ is the ith objective function, and $g _ { j } ( x )$ is the jth constraints function.

In this case, the optimal solution is non-unique due to the conflicting relationship among multiple objectives. For example, there exist some solutions that are superior in some objectives but inferior to other solutions in other objectives. Therefore, multiobjective optimization methods aim to find a set, i.e., Pareto front, which contains all the optimal trade-off solutions.

## IV. PROBLEM FORMULATION AND ANALYSIS

In this section, the US2RMOP is formulated and the corresponding analysis of the problem is presented.

## A. Problem Formulation

In the considered scenario, S transmits data to the associated IoT terminal devices with the assistance of UAV swarm as a relay. The main goal of the UAV swarm-enabled collaborative secure relay system is to guarantee the achievable rate of the associated IoT terminal devices while minimizing the achievable rate of E.

Specifically, maximizing the achievable sum rate of IoT terminal devices and minimizing the achievable sum rate of eavesdropper can be realized by optimizing the beam patterns of PAA and UVAA. According to (4) and (6), the positions and excitation current weights of array elements can be adjusted to accomplish the better directivity of PAA and UVAA, which means that we can let the UAVs fly to better positions, and use optimal excitation current weights for the relay communication. Besides, the proper selection of UAV receiver $U _ { k }$ in UVAA can also increase the achievable rate of IoT terminal devices and reduce the achievable rate of E. However, the energy consumption of the UAV elements in UVAA will undoubtedly increase due to movement, and the positions of UAVs need to be re-tuned after communicating with an IoT terminal device since the mainlobe of UVAA can only direct in the direction of one receiver each time. Accordingly, the multiple performances of the system should be comprehensively considered.

Defining the optimization decision variable, i.e., the solution as $\mathrm { \mathbb { X } } = ( \mathbb { I } _ { \mathrm { P } } ^ { \mathrm { \breve { M } N \times T } } , \mathrm { \mathbb { S } } _ { \mathrm { P } } ^ { \mathrm { 1 \times T } } , \mathbb { I } _ { \mathrm { U } } ^ { \mathrm { K \times T } } , \mathbb { P } _ { \mathrm { U } } ^ { \mathrm { K \times T } } , \mathbb { O } _ { \mathrm { U } } ^ { \mathrm { 1 \times T } } )$ , which is detailed in Table I, and the three optimization objectives are formulated as follows.

Optimization objective 1: The first optimization objective is to maximize the achievable sum rate of IoT terminal devices, which is related to the excitation current weights of both PAA and UVAA, the position of each UAV, and the selection of UAV receiver. Therefore, the first objective function can be designed as

$$
f _ { 1 } ( \mathbb { I } _ { \mathrm { P } } ^ { \mathrm { M N } \times \mathrm { T } } , \mathbb { S } _ { \mathrm { P } } ^ { 1 \times \mathrm { T } } , \mathbb { I } _ { \mathrm { U } } ^ { \mathrm { K } \times \mathrm { T } } , \mathbb { P } _ { \mathrm { U } } ^ { \mathrm { K } \times \mathrm { T } } ) = \sum _ { i = 1 } ^ { T } R _ { { \mathcal { S } } 2 { \mathcal { D } } } ( i ) .\tag{20}
$$

Remark 1: Some factors of phases I and II influence the achievable sum rate of IoT terminal device. Specifically, the excitation current weights of PAA and the selection of UAV receiver $U _ { k }$ affect the rate of $S 2 U _ { k } ( i )$ link, and the excitation current weights and UAV positions of UVAA influence the rate of C2D(i) link.

Optimization objective 2: Minimizing the achievable sum rate of E is considered as the second optimization objective, and the corresponding objective function is designed as

$$
f _ { 2 } \big ( \mathbb { I } _ { \mathrm { P } } ^ { \mathrm { M N \times T } } , \mathbb { S } _ { \mathrm { P } } ^ { \mathrm { 1 \times T } } , \mathbb { I } _ { \mathrm { U } } ^ { \mathrm { K \times T } } , \mathbb { P } _ { \mathrm { U } } ^ { \mathrm { K \times T } } \big ) = \sum _ { i = 1 } ^ { T } R _ { \mathcal { E } } \big ( i ) .\tag{21}
$$

Remark 2: The achievable sum rate of $\mathcal { E }$ is closely related to three phases of the relay communication process. Specifically, the excitation current weights of PAA affect the rate of $\mathcal { S } 2 \mathcal { E } ( i )$ link, the selection of UAV receiver $U _ { k }$ has an impact on the rate of $U _ { k } 2 \mathcal { E } ( i )$ link, and the excitation current weights and UAV positions of UVAA influence the rate of C2E(i) link.

Optimization objective 3: The third optimization objective is to minimize the energy consumption of UAV swarm, and this optimization objective is relevant to both the user association order4 of remote IoT terminal devices and the positions of UAV swarm. Thus, the specific objective function is designed as

$$
f _ { 3 } ( \mathbb { P } _ { \mathrm { C } } ^ { \mathrm { K } \times \mathrm { T } } , \mathbb { O } ^ { 1 \times \mathrm { T } } ) = \sum _ { i = 1 } ^ { T } \sum _ { k = 1 } ^ { K } E _ { k } ( i ) ,\tag{22}
$$

where $E _ { k } ( i )$ represents the motion energy consumption of kth UAV for communicating in the ith communication process. Moreover, trajectory design style, speed control strategy and the adopted model of each UAV are the same as [17].

Remark 3: The hovering energy consumption of UAVs is not taken into account since it is positively correlated with the hovering time [39]. Furthermore, the hovering time is related to the communication rate and data transfer volume. Apparently, the communication rate has been considered in optimization objective 1, and data transfer volume for each associated IoT terminal device is decided by user behaviors. Thus, the hovering energy consumption of UAVs is not necessary to be optimized separately.

TABLE I DESCRIPTION OF VARIABLES
<table><tr><td>Variable Set</td><td>Variable Element</td><td>Physical Meaning</td><td>A Case in Point</td></tr><tr><td> $\mathbb { I } _ { \mathrm { P } } ^ { \mathrm { M N \times T } }$ </td><td> $\{ I _ { m , i } ^ { P } | m \in \{ 1 , . . . , M \times N \} , i \in \{ 1 , . . . , T \} \}$ </td><td> $\mathbb { I } _ { \mathrm { P } } ^ { \mathrm { M N \times T } }$  represents the excitation current weights of  $I _ { m , i } ^ { P }$   $\mathrm { P A A } ,$  while is the excita- tion current weight of the mth row array element for serving the ith associated IoT terminal device in PAA.</td><td> $I _ { 1 , 1 } ^ { P } = 1 . 0$  means the excitation cur- rent weight of the first array ele- ment is 1.O in PAA for serving the first associated IoT terminal device.</td></tr><tr><td> $\mathrm { S _ { P } ^ { 1 \times T } }$ </td><td> $\{ S _ { i } | i \in \{ 1 , . . . , T \} \}$ </td><td> $\ S _ { \mathrm { p } } ^ { \mathrm { 1 \times T } }$  represents the selection of UAV receiver, while  $S _ { i }$  is the receiver of PAA for serving the ith associated IoT termi- nal device.</td><td> $S _ { 1 } ~ = ~ 1$  means the first UAV is scheduled to act as a receiver of PAA for serving the first associated IoT terminal device.</td></tr><tr><td> $\mathbb { I } _ { \mathrm { U } } ^ { \mathrm { K \times T } }$ </td><td> $\{ I _ { k , i } ^ { U } | k \in \{ 1 , . . . , K \} , i \in \{ 1 , . . . , T \} \}$ </td><td> $\mathbb { I } _ { [ J } ^ { \mathrm { K \times T } }$  represents the excitation current  $I _ { k , i } ^ { U }$  is the ex- weight of UVAA,while citation current weight of the kth UAV in UVAA for serving ith associated IoT terminal device.</td><td> $I _ { 1 , 1 } ^ { U } = 1 . 0$  means the excitation cur- rent weight of the firstUAV element is 1.0 in UVAA for serving the first associated IoT terminal device.</td></tr><tr><td> $\mathbb { P } _ { \mathrm { U } } ^ { \mathrm { K } \times \mathrm { T } }$ </td><td> $\{ P _ { k , i } | k \in \{ 1 , . . . , K \} , i \in \{ 1 , . . . , T \} \}$ </td><td> $\mathbb { P } _ { \mathrm { U } } ^ { \mathrm { K } \times \mathrm { T } }$  represents the position of UAV swarm,while  $P _ { k , i }$  is the position of the kth UAV for serving the ith associated IoT terminal device.</td><td> $P _ { 1 , 1 } ~ = ~ ( 3 0 0 , 3 0 0 , 1 0 0 )$  means the position of the first UAV for serv- ing the first associated IoT terminal device is (300,300,100).</td></tr><tr><td> $\mathbb { O } ^ { 1 \times \mathrm { T } }$ </td><td> $\{ O _ { i } | i \in \{ 1 , . . . , T \} \}$ </td><td> $\mathbb { O } ^ { 1 \times \mathrm { T } }$  represents the association order of IoT terminal devices,while  $O _ { i }$  is the ID of the ith associated IoT terminal device.</td><td> $O _ { 1 } ~ = ~ 1$  means UVAA first serves the IoT terminal device with ID 1.</td></tr></table>

In summary, considering the three optimization objectives mentioned above, the US2RMOP can be formulated as follows.

```latex
P1 : min $F = \{ - f _ { 1 } , f _ { 2 } , f _ { 3 } \}$
{X}
s.t. C 1 : 0 â¤ I Pm,i â¤ 1, âm â {1, . . ., M Ã N },
$\forall i \in \{ 1 , . . . , T \} ,$
$C 2 : 1 \leq S _ { i } \leq K , \forall i \in \{ 1 , . . . , T \} ,$
$C 3 : 0 \le I _ { k , i } ^ { U } \le 1 , \forall k \in \{ 1 , . . . , K \} , \forall i \in \{ 1 , . . . , T \} ,$
$C 4 : X _ { \operatorname* { m i n } } \leq X _ { k } ^ { U } \leq X _ { \operatorname* { m a x } } , \forall k \in \{ 1 , . . . , K \} ,$
C 5 : Ymin â¤ Y Uk â¤ Ymax, âk â {1, . . ., K },
C 6 : $Z _ { \operatorname* { m i n } } \le Z _ { k } ^ { U } \le Z _ { \operatorname* { m a x } } , \forall k \in \{ 1 , . . . , K \} ,$
C7 : $1 \leq O _ { i } \leq T , \forall i \in \{ 1 , . . . , T \} ,$
C 8 : $O _ { i _ { 1 } } \neq O _ { i _ { 2 } } , \forall i _ { 1 } \neq i _ { 2 } ,$
C 9 : $\begin{array} { r } { \| P _ { k _ { 1 } , i } , P _ { k _ { 2 } , i } \| \geq D _ { \operatorname* { m i n } } ^ { U } , \forall k _ { 1 } , k _ { 2 } \in \{ 1 , . . . , K \} , } \end{array}$
```

where C1 and C3 indicate the range of excitation current weights of PAA and UVAA, C2 denotes the selection range of UAV receiver, and the 3D movement area of the UAVs is limited by C4, C5 and C6, respectively. Moreover, C7 and C8 ensure service fairness for each associated IoT terminal device. Moreover, the collision constraint between UAVs is expressed as C9 where $\| P _ { k _ { 1 } , i } , P _ { k _ { 2 } , i } \|$ represents the distance between the $k _ { 1 }$ th UAV and the k2th UAV for serving the ith associated IoT terminal device.

## B. Problem Analysis

In this section, the formulated $\mathrm { U S ^ { 2 } R M O P }$ is analyzed.

Proposition 1: The $\mathrm { U S ^ { 2 } R M O P }$ is an NP-hard and non-convex optimization problem.

Proof: To simplify this discussion, we only consider the objective $f _ { 1 }$ without $f _ { 2 }$ and $f _ { 3 }$ in the context of serving a single IoT terminal device. The $\mathrm { U S ^ { 2 } R M O P }$ can be reduced as follows:

$$
{ \begin{array} { r l } & { \mathbf { P 2 } : \ { \underset { \{ \mathbb { X } _ { 1 } \} } { \operatorname* { m i n } } } \ - f _ { 1 } , } \\ & { } \\ & { \qquad { \mathrm { s . t . } } \ C 1 - C 6 , { \mathrm { a n d } } \ C 9 , } \end{array} }
$$

where $\mathbb { X } _ { 1 } = ( \mathbb { I } _ { \mathrm { P } } ^ { \mathrm { M N } } , \mathbb { S } _ { \mathrm { P } } ^ { 1 } , \mathbb { I } _ { \mathrm { C } } ^ { \mathrm { K } } , \mathbb { P } _ { \mathrm { C } } ^ { \mathrm { K } } )$ is the part of decision variable X. As can be seen, P2 can be specified as a Mixed-Integer Nonlinear Programming (MINLP) problem, which is a typical NP-hard and non-convex optimization problem [40]. Clearly, P1 is more difficult to be solved than P2 since it adds the coupling to the optimization objectives $f _ { 2 }$ and $f _ { 3 }$ . Thus, the formulated $\mathrm { U S ^ { 2 } R M O P }$ is an NP-hard and non-convex optimization problem. -

Proposition 2: The formulated US2RMOP is a large-scale optimization problem.

Proof: The solution space of the US2RMOP is composed of the excitation current weights $\mathbb { I } _ { \mathrm { P } } ,$ , the selection of UAV receiver $\mathbb { S } _ { \mathrm { P } }$ , the excitation current weight distribution of UVAA $\mathbb { I } _ { \mathrm { U } }$ , the position of UAV swarm PU and the associated order of remote IoT terminal devices O. Thus, the decision space dimension of the $\mathrm { U S ^ { 2 } R M O P }$ is $( ( M \times N + 2 + 4 \times K ) \times T )$ . As the numbers of PAA elements, UAVs and IoT terminal devices increase, the decision space dimension will increase accordingly. On this basis, the US2RMOP is a large-scale optimization problem [41]. -

<!-- image-->  
Fig. 2. Illustrative example about interaction behaviors between grasshoppers, where the resultant force exerted by grasshopper A through two distinct forces on other grasshoppers is categorized into three types as follows. (i) attraction force > repulsion force: Overall effect is attraction, e.g., grasshoppers A to D. (ii) attraction force = repulsion force: Overall effect is neither attraction nor repulsion under the condition of the comfort zone, e.g., grasshoppers A to C. (iii) attraction force < repulsion force: Overall effect is repulsion, e.g., grasshoppers A to B.

## V. PROPOSED ALGORITHM

The approaches to address the formulated US2MOP can be broadly categorized into three groups, i.e., convex optimization methods, reinforcement learning and evolutionary algorithms (EA). Specifically, due to involving complex constraints, solving the formulated US2MOP through relaxation and duality in convex optimization techniques is difficult. Likewise, the curse of dimensionality can impact reinforcement learning due to the presence of a large number of decision variables, resulting in extensive state and action spaces.

EA are classical stochastic search methods that simulate the natural selection and evolution of creatures. Compared to the other two categories of algorithms analyzed above, EA have strong robustness, global search capability, and adaptability, making them effective for solving the non-convex, NP-hard and larger-scale optimization problems. Among EA, the performances of grasshopper optimization algorithm (GOA) and its corresponding multi-objective grasshopper optimization algorithm (MOGOA) [42] are effective and they have been applied for solving problems in different areas such as the financial stress prediction [43], trajectory optimization [44], and training the neural networks [45], etc. Thus, we intend to use them as basic algorithm frameworks to deal with the formulated $\mathrm { U S ^ { 2 } R M O P } .$

## A. Conventional GOA and MOGOA

GOA is enlightened by the behavior of grasshopper swarm, where the position of each individual grasshopper in the population stands for a feasible solution to the given optimization problem. As shown in Fig. 2, grasshoppers exhibit interactive behaviors consisting of both attractive and repulsive forces. Mathematically, the resultant force is expressed as $s ( r ) = f e ^ { \frac { - r } { l } } - e ^ { - r }$ where $f$ and l is the intensity of attraction and the attractive length scale, respectively. Specifically, the solution update strategy is described as

$$
x _ { i } ^ { d } = c \left( \sum _ { j = 1 , j \neq i } ^ { N _ { p o p } } c \frac { u b _ { d } - l b _ { d } } { 2 } s \left( \left| x _ { j } ^ { d } - x _ { i } ^ { d } \right| \frac { x _ { j } - x _ { i } } { d _ { i j } } \right) \right) + T _ { d } ,\tag{23}
$$

where $x _ { i } ^ { d }$ is the dth dimension of the ith grasshopper, $N _ { p o p }$ represents the population size, $d _ { i j }$ denotes the distance between the ith and jth grasshoppers, and $u b _ { d }$ and $l b _ { d }$ are the upper and lower boundaries of dth dimension, respectively. Moreover, $T _ { d }$ is the value of the best solution found so far in the dth dimension. Notably, c is the linear decreasing coefficient to control the size of a comfort zone, which can be expressed as

$$
c = c _ { \operatorname* { m a x } } - i t e r \times \frac { c _ { \operatorname* { m a x } } - c _ { \operatorname* { m i n } } } { i t e r _ { \operatorname* { m a x } } } ,\tag{24}
$$

where $c _ { \mathrm { m a x } }$ and $c _ { \mathrm { m i n } }$ are the maximum and minimum values, respectively. iter represents the current iteration, and $i t e r _ { \operatorname* { m a x } }$ is the maximum number of iterations. In (23), the inner parameter c decreases the attractive/repulsive forces between grasshoppers proportionally to the iteration, whereas the outer parameter c diminishes the search area around the objective with the increasing of iterations.

As illustrated in Fig. 3, the MOGOA employs archive, crowded neighborhood, and roulette wheel selection to address multi-objective optimization problems in an effective manner. These adaptations allow for better management of the search space, resulting in more optimal solutions. Specifically, the archive stores the best non-domination solutions found so far, while the crowded neighborhood prevents overcrowding of these solutions. Moreover, the roulette wheel selection is used to probabilistically select the target grasshopper for update population, ensuring diversity and convergence in population.

However, traditional MOGOA faces many challenges for solving the formulated US2RMOP due to the following reasons.

- The mixture of continuous and discrete solution spaces caused by the presence of discrete part (SP, O) cannot be addressed by conventional MOGOA.

- The probability of finding the global optimal solution is reduced by the random initialization of MOGOA.

- The relationship between exploration and exploitation in a large-scale solution space cannot be efficiently balanced by linear decreasing coefficient c.

Thus, we propose the IMOGOA to improve the adaptability of MOGOA for solving the formulated $\mathrm { U S ^ { 2 } R M O P } ,$ and the details are as follows.

## B. IMOGOA

In this section, IMOGOA with several improvements is presented for solving the US2RMOP. Specifically, IMOGOA can achieve a better performance with special designs about the population initialization, non-linear decreasing coefficient, solution update and archive update. The general framework of IMOGOA is shown in Algorithm 1, and the improved strategies are described in detail as follows.

<!-- image-->  
Fig. 3. Framework of MOGOA, where the rectangles filled in light green and other colors represent solution and objective values part of population, respectively. Moreover, the dashed arrows with solid dots at the end indicate the operators applied to the populations.

1) Population Initialization: The random initialization of population in traditional MOGOA may reduce the probability of finding global optima. In response to this, we adopt a half-Halton-half-chaos $\mathrm { ( H ^ { 3 } C ) }$ strategy to enhance the diversity of the initial population, and the generation method can be described as follows:

$$
x _ { i } ^ { d } = \left\{ h _ { i , d } \times ( u b _ { d } - l b _ { d } ) + l b _ { d } , \quad i \leq N _ { p o p } / 2 \right. ,\tag{25}
$$

where $h _ { i , d }$ and $c _ { i , d }$ are the sequences between 0 and 1 which are generated by the Halton method and chaotic map, respectively. Specifically, the calculation process for Halton sequence can be expressed as

$$
h _ { i , d } = \left( \sum _ { l = 0 } ^ { L } b _ { l } ( i ) ( p _ { d } ) ^ { - l - 1 } \right) ,\tag{26}
$$

where $p _ { d }$ is a random prime number in the range of 0 to 10, and the value $b _ { 0 } ( i ) , b _ { 1 } ( i ) , \dots b _ { l } ( i )$ needs to satisfy the condition, i.e., $\begin{array} { r } { \sum _ { l = 0 } ^ { L } b _ { l } ( i ) ( p _ { d } ) ^ { l } = i . } \end{array}$ Accordingly, the calculation process for a chaotic sequence can be expressed as

$$
c _ { i , d } = \mathrm { m o d } \left( c _ { i , d - 1 } + b - ( a / 2 \pi ) \times \sin ( 2 \pi c _ { i , d - 1 } ) , 1 \right) ,\tag{27}
$$

where a and b are two constant variables. Moreover, mod (Â·) is a mathematical division operator.

2) Non-Linear Decreasing Coefficient: To increase the probability of finding the globally optimal solution, IMOGOA must balance the process of exploring new solution space and exploiting known information. Relying too heavily on known information may trap the algorithm in a local optimal solution and prevent it from finding the global optimal solution. Conversely, relying too much on random searches may cause the algorithm to waste time exploring low-quality solution spaces. To address this issue, a non-linear decreasing coefficient is adopted and

Algorithm 1: IMOGOA.   
Input: iteration number itermax, population size   
$N _ { p o p } ;$   
Output: the final archive Archive;   
1 Archive $ \emptyset , P _ { 0 }  \emptyset ;$   
2 Initialize Population $P _ { 0 }$ by using $\mathbf { H } ^ { 3 } \mathbf { C }$ Strategy;   
3 Calculate the fitness value of $P _ { 0 }$ and filtering the   
non-dominated set $S _ { 0 } ;$   
4 Archive $ S _ { 0 }$ U Archive;   
5 Update Archive using Algorithm 3;   
6 fori=1 to $i t e r _ { m a x }$ do   
7 Select a grasshopper in Archive by roulette   
wheel as target grasshopper position Xtargeti   
8 for j=1 to ${ \check { N } } _ { p o p }$ do   
9 Update the solution of the jth grasshopper   
using Algorithm 2;   
10 end   
11 Calculate the fitness value of the current   
population;   
12 Update Archive using Algorithm 3;   
13 end   
14 Return Archive;

expressed as

$$
c = c _ { \operatorname* { m a x } } - c _ { \operatorname* { m i n } } - \sin \left( \frac { 1 } { 2 } \times \pi \times \left( \frac { i t e r } { i t e r _ { \operatorname* { m a x } } } \right) ^ { \frac { 1 } { 2 } } \right) .\tag{28}
$$

The non-linear decreasing coefficient, as illustrated in Fig. 4, enables the algorithm to prioritize exploring unknown solution space in the early stages of search. Over time, the algorithmâs ability to exploit known information is gradually strengthened, leading to better balance and higher quality solutions. By enabling a better balance between exploring new solution spaces and exploiting known information, this approach helps IMOGOA find high-quality solutions in a shorter timeframe.

<!-- image-->  
Fig. 4. Comparison between non-linear and linear decreasing coefficients. We set $c _ { \operatorname* { m a x } } = 1$ and $c _ { \operatorname* { m i n } } = 0 . 0 0 0 4$

3) Solution Update: The solution update of population is an important step for efficiently searching the solution space in IMOGOA. Since the formulated $\mathrm { U S ^ { 2 } R M O P }$ has both continuous solution part $\left( \mathbb { I } _ { \mathrm { P } } , \mathbb { I } _ { \mathrm { V } } , \mathbb { P } _ { \mathrm { C } } \right)$ and discrete solution part $( \mathbb { S } _ { \mathrm { P } } , \mathbb { O } )$ , it is necessary to consider these two update operators separately.

For the continuous part of solution: Although the solution can be updated directly by using conventional MOGOA, it can easily become trapped in local optima. To improve the search capability in the large-scale solution space, we employ LÃ©vy flight in the process of solution update. Specifically, the continuous solution update method can be expressed as

$$
\mathbb { X } _ { i } ^ { C N e w } = \mathbb { X } _ { i } ^ { C G O A } + \alpha _ { 1 } \otimes L \ ' e v y ( \beta ) ,\tag{29}
$$

where $\mathbb { X } _ { i } ^ { C G O A }$ is the continuous solution obtained by traditional MOGOA after introducing the nonlinear decreasing coefficient, and $\alpha _ { 1 }$ is the step size scaling factor. Moreover, â is a mathematical Hadamard product operator, and $L e v y ( \beta )$ is the LÃ©vy random search path, which is calculated as follows:

$$
L e v y ( \beta ) = \frac { \mu } { | w | ^ { - \beta } } ,\tag{30}
$$

where $\mu$ is the normal distribution matrix with mean 0 and variance $\sigma _ { u } ^ { 2 } ,$ , wherein $\begin{array} { r } { \sigma _ { u } = [ \frac { \Gamma ( 1 + \beta ) \sin ( \frac { \pi \beta } { 2 } ) } { \Gamma ( \frac { 1 + \beta } { 2 } ) \beta \times 2 ^ { \frac { \beta - 1 } { 2 } } } ] ^ { \frac { 1 } { \beta } } } \end{array}$ . Besides, w is the normal distribution matrix with mean 0 and variance 1. Accordingly, the sizes of both $\mu$ and w are $d \times 1$

For the discrete part of solution: Since conventional MOGOA cannot handle discrete solution spaces, we design the update process in detail because of the presence of discrete part $( \mathbb { S } _ { \mathrm { P } } , \mathbb { O } )$ . Specifically, since the selection order of the UAV receiver denoted by $\mathbb { S } _ { \mathrm { P } }$ can be duplicated and the user association order of IoT terminal devices denoted by O is non-duplicated, the two-points crossover (TPC) and partially-matched crossover (PMX) [46] strategies are adopted for $\mathbb { S } _ { \mathrm { P } }$ and $\mathbb { O } .$ , respectively. As can be seen from Fig. 5, the PMX strategy appends conflict remove part for eliminating the duplicate elements compared to the TPC strategy. Accordingly, the detailed update is expressed as follows:

$$
\left\{ \begin{array} { l l } { \left[ { \mathbb X } _ { i } ^ { S N e w 1 } , { \mathbb X } _ { i } ^ { S N e w 2 } \right] = \mathrm { T P C } \left( { \mathbb X } _ { i } ^ { S C u r } , { \mathbb X } _ { T S } \right) , } & { \mathrm { f o r ~ } { \mathbb S } _ { \mathrm { P } } } \\ { \left[ { \mathbb X } _ { i } ^ { O N e w 1 } , { \mathbb X } _ { i } ^ { O N e w 2 } \right] = \mathrm { P M X } \left( { \mathbb X } _ { i } ^ { O C u r } , { \mathbb X } _ { T O } \right) , } & { \mathrm { f o r ~ } { \mathbb O } } \end{array} \right.\tag{31}
$$

where $( \mathbb { X } _ { i } ^ { S C u r } , \mathbb { X } _ { i } ^ { O C u r } )$ and $\left( \mathbb { X } _ { T S } , \mathbb { X } _ { T O } \right)$ are the discrete parts of the ith grasshopper and target grasshopper, respectively.

<!-- image-->  
Fig. 5. Illustrative example of TPC and PMX strategies, wherein TPC strategy selects randomly two crossover points to execute the exchange of elements, pounds and stars point out the repeated location after performing the TPC strategy. On the basis of TPC, PMX strategy further performs conflict remove operation.

Algorithm 2: Solution Update.   
Input: the current solution of the ith grasshopper $\mathbb { X } _ { i } ,$   
the current solution of the target grasshopper   
$\mathbb { X } _ { t a r g e t } ;$   
Output: updated solution of the ith grasshopper   
$\mathbb { X } _ { N e w } ;$   
1 Using Eq. (29) update the continuous part   
$\mathbb { X } _ { i } ^ { C \breve { C } u r } = \left( \mathbb { I } _ { \mathrm { P } } ^ { \breve { C } u r } , \mathbb { I } _ { \mathrm { V } } ^ { C u r } , \mathbb { P } _ { \mathrm { C } } ^ { C u r } \right)$ to produce the new   
continuous part $\check { \mathbb { X } } _ { i } ^ { C N e w } = ( \mathbb { I } _ { \mathrm { P } } ^ { N e w } , \mathbb { I } _ { \mathrm { V } } ^ { N e w } , \mathbb { P } _ { \mathrm { C } } ^ { N e w } ) ;$   
2 Using Eq. $\mathring { ( 3 1 ) }$ update the discrete part   
$\mathbb { X } _ { i } ^ { D \breve { C } u r } = ( \mathbb { S } _ { \mathrm { P } } ^ { C u \hat { r } } , \mathbb { O } ^ { C u r } )$ to produce two new   
discrete ofspring parts $( \mathbb { S } _ { \mathrm { P } } ^ { N e w 1 } , \mathbb { O } ^ { N e w 1 } )$ and   
$( \mathbb { S } _ { \mathrm { P } } ^ { N e w 2 } , \mathbb { O } ^ { N ^ { \star } w 2 } ) ;$   
3 Merge: Obtain two grasshopper offspring   
$O _ { 1 } = \big ( \mathbb { X } _ { i } ^ { C N e w } , \mathbb { S } _ { \mathrm { P } } ^ { N e w 1 } , \mathbb { O } ^ { N ^ { \sum } } \big )$ and   
$\hat { O _ { 2 } } = \left. \mathbb { X } _ { i } ^ { C N e w } , \mathbb { S } _ { \mathrm { P } } ^ { N e w 2 } , \mathbb { O } ^ { N e w 2 } \right.$ by merging the   
continuous and discrete part of solution;   
4 Selection:Calculate the fitness of $O _ { 1 }$ and $O _ { 2 } ;$   
5if $O _ { 1 }$ dominates $O _ { 2 }$ then   
$\mathbb { X } _ { N e w }  O _ { 1 } ;$   
7 else   
8 if $O _ { 2 }$ dominates $O _ { 1 }$ then   
9 $\mathbb { X } _ { N e w }  O _ { 2 } ;$   
10 else   
11 if rand $< 0 . 5$ then   
12 $\begin{array} { r l } { | } & { { } \mathbb { X } _ { N e w }  O _ { 1 } ; } \end{array}$   
13 else   
14 $\begin{array} { r l } { | } & { { } \mathbb { X } _ { N e w }  O _ { 2 } ; } \end{array}$   
15 end   
16 end   
17 end   
18 Return $\mathbb { X } _ { N e w } ;$

Moreover, $( \mathbb { X } _ { i } ^ { S N e w 1 } , \mathbb { X } _ { i } ^ { O N e w 1 } )$ and $( \mathbb { X } _ { i } ^ { S N e w 2 } , \mathbb { X } _ { i } ^ { O N e w 2 } )$ represent the two new offspring generated by the TPC and PMX strategies, respectively.

Accordingly, the update strategy of the solution is detailed in Algorithm 2.

4) Archive Update: A single update operator cannot simultaneously balance global exploration and local exploitation capabilities. At the same time, the archive has an impact on guiding the update of the grasshopper population. Thus, we introduce archive mutation and dynamic elimination-based crowding distance (DCDE) [47] to improve global searchability and solution distribution in the archive. In the archive mutation stage, we employ mutation and crossover for the continuous and discrete parts, respectively. The mutation for the continuous part is described as

<!-- image-->  
Fig. 6. Comparison sketch between elimination-based crowding distance and DCDE: Elimination-based crowding distance only sorts once and then deletes the archive regardless of how many individuals it overflows, while DCDE adopts the strategy of sorting once and deleting once, which better achieves uniformity of archive.

$$
\mathbb { X } _ { i } ^ { C M } = \mathbb { X } _ { i } ^ { C } + \alpha _ { 2 } \otimes C a u c h y ( 0 , 1 ) ,\tag{32}
$$

where $\mathbb { X } _ { i } ^ { C }$ is the continuous part of the ith solution in current archive, and $\mathbb { X } _ { i } ^ { C M }$ represents the continuous part of the ith solution after Cauchy mutation. Moreover, $\alpha _ { 2 }$ is the step size scaling factor, and $C a u c h y ( 0 , 1 )$ is the standard Cauchy distribution. Similar to the discrete solution update method, we simply treat a random grasshopper position in the archive as the target grasshopper location $\mathbb { X } _ { T S }$ and $\mathbb { X } _ { T O }$ in (31). In the archive determination stage, we replaced the traditional MOGOA archive elimination method with DCDE. The purpose of this modification is to more effectively maintain the diverse and uniform distributions of IMOGOA archive on the Pareto front. Specifically, the difference between DCDE and the traditional elimination-based crowding distance strategy is shown in Fig. 6. A more detailed explanation of DCDE can be found in the [47].

## C. Scheduling Mechanism of the IMOGOA

A simple and efficient scheduling mechanism is necessary for implementing the proposed IMOGOA in the UAV swarmenabled collaborative secure relay communication system. Supposing that UAVs can gather the initial state information during the start stage of communications. Considering the limited computing and energy resources, running IMOGOA on a single UAV may waste too much time and bring extra energy consumption. Due to the sufficient ability in terms of energy and computing, the MBS can be considered as a supercomputer to run IMOGOA. The main steps of the scheduling mechanism are as follows.

Step 1 - Information Fusion (at UAV Swarm): Select UAV $U _ { k }$ to broadcast the start message $M _ { S t a r t }$ , where the position and network information of UAV $U _ { k }$ is included. After UAV $U _ { k }$ â receives the message $M _ { S t a r t }$ , it replies a confirm message

$M _ { A C K 1 }$ , which contains its own position and network information. Subsequently, $\mathrm { U A V } U _ { k }$ aggregates the position and network information UAV $U _ { k }$ aggregates the position and network information, and transmits the fusion information $M _ { F u s i o n }$ to MBS.

Step 2 - Optimization Algorithm Execution (at MBS): MBS receives the message $M _ { F u s i o n }$ and replies a confirm message $M _ { A C K 2 }$ . Then, the supercomputer of MBS runs the proposed IMOGOA to produce the optimized solution for the $\mathrm { U S ^ { 2 } R M O P } .$ Subsequently, MBS sends the solution distribution message $M _ { S o l u t i o n }$ to UAV $U _ { k }$ , which contains the optimized solution for the US2RMOP.

Step 3 - Optimization Information Distribution (at UAV Swarm): The UAV $U _ { k }$ receives the message $M _ { S o l u t i o n } .$ , and distributes optimization information to other UAVs by using the wireless channel allocation [48]. Until all other UAVs reply to the message $M _ { A C K 3 }$ , the scheduling mechanism of IMOGOA is terminated.

Note that the UAV $U _ { k }$ will resent the message $M _ { S t a r t } .$ $M _ { F u s i o n }$ or $M _ { S o l u t i o n }$ every $T _ { w a i t i n g }$ until it receives $M _ { A C K 1 }$ $M _ { A C K 2 }$ or $M _ { A C K 3 }$ to ensure the reliability of scheduling mechanism.

## D. Algorithm Analysis

In this section, the scheduling overhead and computational complexity of the proposed IMOGOA are analyzed.

1) Scheduling Overhead Analysis: In this analysis, we assume that the maximum number of re-transmissions is $N _ { r e }$ for the messages $M _ { S t a r t } , M _ { F u s i o n }$ and $M _ { S o l u t i o n }$ . The bit numbers of the messages $M _ { S t a r t }$ $M _ { F u s i o n } .$ $M _ { S o l u t i o n }$ $M _ { A C K 1 }$ and $M _ { A C K 3 }$ are $b _ { S } , b _ { F } , b _ { O } , b _ { A 1 }$ and $b _ { A 3 }$ , respectively. Moreover, the packet loss probabilities of links are $f ,$ , and the transmission rate and power of the UAV are r and $P _ { T } .$ , respectively.

Proposition 3: The communication energy consumption of the UAV swarm for the scheduling mechanism of IMOGOA is

$$
\begin{array} { l } { E _ { C } = } \\ { \frac { P _ { T } [ ( b _ { S } + b _ { F } + b _ { O } ) ( 1 - f ^ { N _ { r e } } ) + ( K - 1 ) ( b _ { A 1 } + b _ { A 3 } ) ( 1 - f ) ] } { r ( 1 - f ) } . } \end{array}\tag{33}
$$

Algorithm 3: Archive Update.   
Input: the updated solution of current grasshopper   
population $\{ \mathbb { X } _ { 1 } , \mathbb { X } _ { 2 } , \cdot \cdot \cdot , \mathbb { X } _ { N p o p } \} \mathrm { ~ . ~ }$ ,the current   
Archive $A _ { c u r r e n t } ,$ ,the current Archive size   
$N _ { A } ;$   
Output: the updated Archive Aupdated;   
1 $A _ { u p d a t e d }  A _ { c u r r e n t } ;$   
2 for $i = 1$ to $N _ { A }$ do   
3 Using Eq. (32) mutate the continuous part   
$\mathbb { X } _ { i } ^ { C \breve { C } u r } = ( \mathbb { I } _ { \mathrm { P } } ^ { \breve { C } u r } , \mathbb { I } _ { \mathrm { V } _ { - - } } ^ { C u r } , \mathbb { P } _ { \mathrm { C } } ^ { C u r } )$ to produce the new   
continuous part $\check {  { \mathbb X } } _ { i } ^ { C M } = ( \mathbb { I } _ { \mathrm { P } } ^ { \tilde { N } e w } , \mathbb { I } _ { \mathrm { V } } ^ { \tilde { N } e w } , \mathbb { P } _ { \mathrm { C } } ^ { N e w } ) ;$   
4 Random select the discrete part of a grasshopper   
in $A _ { c u r r e n t }$ as $\left( \mathbb { X } _ { T S } , \mathbb { X } _ { T O } \right)$   
5 Using $\operatorname { E q . } \left( 3 1 \right)$ crossover the discrete part   
$\mathbb { X } _ { i } ^ { D \breve { C } u r } = ( \mathbb { S } _ { \mathrm { P } } ^ { C u r } , \mathbb { O } ^ { C u r } )$ to produce two new   
discrete offspring parts $( \mathbb { S } _ { \mathrm { P } } ^ { \lambda _ { \mathrm { P } } e w 1 } , \mathbb { O } ^ { N e w 1 } )$ and   
$( \mathbb { S } _ { \mathrm { P } } ^ { N e w 2 } , \mathbb { O } ^ { N e w 2 } ) ;$   
6 Merge: Obtain two grasshopper offspring   
$M _ { 1 } = ( \mathbb { X } _ { i } ^ { C M } , \mathbb { S } _ { \mathrm { P } } ^ { N e w 1 } , \mathbb { O } ^ { n e w 1 } ) ^ { \bullet }$ and   
$\hat { M _ { 2 } } = \hat { ( } \mathbb { X } _ { i } ^ { C M } , \mathbb { S } _ { \mathrm { P } } ^ { \hat { N } e w 2 } , \mathbb { O } ^ { N e w 2 } )$ by merging the   
continuous and discrete part of solution;   
7 Selection: Calculate the fitness of $M _ { 1 }$ and $M _ { 2 } ;$   
8 if $M _ { 1 }$ dominates $M _ { 2 }$ then   
9 $\begin{array} { r l } { | } & { { } A _ { u p d a t e d }  A _ { u p d a t e d } \cup M _ { 1 } ; } \end{array}$   
10 else   
11 if $M _ { 2 }$ dominates $M _ { 1 }$ then   
12 $A _ { u p d a t e d }  A _ { u p d a t e d } \cup M _ { 2 } ;$   
13 else   
14 ifrand $< 0 . 5$ then   
15 $A _ { u p d a t e d }  A _ { u p d a t e d } \cup M _ { 1 } ;$   
16 else   
17 $\begin{array} { r l } { | } & { { } A _ { u p d a t e d }  A _ { u p d a t e d } \cup M _ { 2 } ; } \end{array}$   
18 end   
19 end   
20 end   
21 end   
22 Remove dominated solutions in $A _ { u p d a t e d } ;$   
23if $s i z e ( A _ { u p d a t e d } ) \geq$ maxArchiveSize then   
24 Execute DCDE on $A _ { u p d a t e d } ;$   
25 end   
26 Return $A _ { u p d a t e d } ;$

Proof: The average re-transmission number of $M _ { S t a r t } .$ $M _ { F u s i o n }$ and $M _ { S o l u t i o n }$ can be expressed as

$$
\begin{array} { r l } & { \overline { { N } } _ { T } = 1 \cdot \operatorname* { P r } ( S ^ { 1 } ) + 2 \cdot \operatorname* { P r } ( F ^ { 1 } , S ^ { 2 } ) + \cdot \cdot \cdot } \\ & { \qquad + \left( N _ { r e } - 1 \right) \cdot \operatorname* { P r } ( F ^ { 1 } , F ^ { 2 } , \ldots , S ^ { N _ { r e } - 1 } ) } \\ & { \qquad + N _ { r e } \cdot \operatorname* { P r } ( F ^ { 1 } , F ^ { 2 } , \ldots , F ^ { N _ { r e } - 1 } ) , } \end{array}\tag{34}
$$

where the successful probability of transmission at the m round is denoted as $\operatorname* { P r } ( F ^ { 1 } , \overbar { F } ^ { 2 } , \ldots , \overbar { F } ^ { m - 1 } , S ^ { m } )$ . Since the successful and failed probabilities of transmission are independent for each round, the average re-transmission number of $M _ { S t a r t } , M _ { F u s i o n }$ and $M _ { S o l u t i o n }$ can further be written as

$$
\begin{array} { l } { \overline { { N } } _ { T } = ( 1 - f ) + 2 ( f - f ^ { 2 } ) + \cdot \cdot \cdot } \\ { \quad \quad + ( N _ { r e } - 1 ) ( f ^ { N _ { r e } - 2 } - f ^ { N _ { r e } - 1 } ) + N _ { r e } f ^ { N _ { r e } - 1 } } \\ { \quad \quad = \displaystyle \frac { 1 - f ^ { N _ { r e } } } { 1 - f } . } \end{array}\tag{35}
$$

Thus, the communication energy consumption of the UAV swarm for the scheduling mechanism of IMOGOA can be calculated as follows:

$$
\begin{array} { r l } & { E _ { C } = E _ { S t e p 1 } + E _ { S t e p 3 } } \\ & { \quad = P _ { T } \cdot [ ( b _ { S } + b _ { F } ) \cdot \overline { { N } } _ { T } + ( K - 1 ) \cdot b _ { A 1 } ] / r } \\ & { \quad \ + P _ { t } \cdot [ b _ { O } \cdot \overline { { N } } _ { T } + ( K - 1 ) \cdot b _ { A 3 } ] / r } \\ & { \quad \ = \frac { P _ { T } \cdot \big [ ( b _ { S } + b _ { F } + b _ { O } ) \cdot \overline { { N } } _ { T } + ( K - 1 ) \cdot \big ( b _ { A 1 } + b _ { A 3 } \big ) \big ] } { r } . } \end{array}\tag{36}
$$

Substituting (35) into (36), the scheduling energy consumption can be re-written as (34).

The communication energy consumption of the UAV swarm for the scheduling mechanism of IMOGOA is a small enough energy overhead compared to the motion energy consumption we optimized previously for the UAV swarm. For instance, we consider a scenario where 16 UAVs serve 8 remote IoT terminal devices. Moreover, the MBS is equipped with a PAA with $6 \times 6$ array elements. The maximum number of re-transmissions is set to 3. The common format of the scheduling messages is expressed as $\left[ S r c , D s t , D a t a \right]$ , where Src and Dst represent the source and destination addresses of the message, respectively, each of which occupies 4 Bytes. Moreover, Data indicates the specific content of message. For the five types of messages in the scheduling process, the specific data of messages are as follows.

- $M _ { S t a r t }$ and $M _ { A C K 1 }$ contain information about the positions of the UAV and the ground eavesdropper, which occupies $5 \times 4$ Bytes (if the ground eavesdropper cannot be detected by this UAV, Data is padded with 0).

C $M _ { F u s i o n }$ contains information about the positions of each UAV and the ground eavesdropper, which occupies $( 3 \times$ $K + 2 ) \times 4 ~ \mathrm { B y t e s }$

- $M _ { S o l u t i o n }$ contains information about the solution obtained by MBS, which occupies $( M \times N + 2 + 4 \times K ) \times$ $T \times 4 ~ { \mathrm { B y t e s } } .$

. $M _ { A C K 3 }$ contains information about the acknowledgment information, which occupies 1 Ã 4 Bytes.

Accordingly, $b _ { S } , b _ { F } , b _ { O } , b _ { A 1 }$ and $b _ { A 3 }$ can be approximately computed as 28 Bytes, 208 Bytes, 3272 Bytes, 28 Bytes and 9 Bytes, respectively. We assume that the transmission rate and power of each UAV are 1 Mbps and 0.1 W, respectively. As a result, the communication energy consumption of the UAV swarm for the scheduling mechanism of IMOGOA is 0.0034 J, which is significantly less than the motion energy consumption.

2) Computational Complexity Analysis: The computational complexity of IMOGOA is primarily dependent on its population size $N _ { p o p }$ , the number of objectives n and the maximum number of iterations $i t e r _ { \operatorname* { m a x } }$ . For simplicity, we assume that the size of the external archive is equal to the population size. The following operators represent worst-case computational complexity:

TABLE II OTHER SIMULATION PARAMETER SETTINGS
<table><tr><td>Parameters</td><td>Values</td></tr><tr><td>Bandwidth</td><td> $B = 2 0 \mathrm { M H z }$ </td></tr><tr><td>Parameters of S-curve</td><td> $a = 9 . 6 1 , b = 0 . 1 6$ </td></tr><tr><td>Average channel power gain at  $d _ { 0 } = 1$  m for LoS state</td><td> $\beta _ { 0 } = - 6 0 ~ \mathrm { d B }$ </td></tr><tr><td>Additional signal attenuation factor for NLoS propagation</td><td> $\mu = - 2 0 \mathrm { d B }$ </td></tr><tr><td>Average path loss exponents for NLoS state</td><td> $\alpha _ { N L o S } = 3 . 5$ </td></tr><tr><td>Average path loss exponents for LoS state</td><td> $\alpha _ { L o S } = 2 . 5$ </td></tr><tr><td>Average path loss exponents for G2G link</td><td> $\alpha _ { G } = 3 . 5$ </td></tr><tr><td>Noise power of channel</td><td> $\sigma ^ { 2 } = - 1 7 4 ~ \mathrm { d B m / H z }$ </td></tr><tr><td>Mass of a UAV</td><td> $m = 2 \mathrm { k g }$ </td></tr><tr><td>Tip speed of the rotor blade</td><td> $u _ { t i p s } = 1 2 0 \mathrm { m } / \mathrm { s }$ </td></tr><tr><td>Mean rotor-induced velocity for hovering</td><td> $u _ { 0 } = 4 . 0 3 \ : \mathrm { m } / \mathrm { s }$ </td></tr><tr><td>Air density</td><td> $\rho = 1 . 2 2 5 \mathrm { k g / m ^ { 3 } }$ </td></tr><tr><td>Rotor disc area</td><td> $A = 0 . 0 5 3 ~ \mathrm { m ^ { 3 } }$ </td></tr><tr><td>Fuselage drag ratio</td><td> $d _ { 0 } = 0 . 6$ </td></tr><tr><td>Rotor solidity</td><td> $s = 0 . 0 5$ </td></tr></table>

Solution Update: Updating the continuous and discrete components accounts for the computational complexity of IMOGOA, with complexities of $O ( i t e r _ { \operatorname* { m a x } { } } \times N _ { p o p } ^ { 2 } )$ and $O ( i t e r _ { \operatorname* { m a x } { } } \times N _ { p o p } )$ , respectively.

- Archive Update: The archive update includes archive mutation and DCDE with complexities of $O ( i t e r _ { \operatorname* { m a x } } \times$ 2n $N _ { p o p } )$ and $O ( ( i t e r _ { \operatorname* { m a x } } \times n N _ { p o p } ^ { 2 } \log N _ { p o p } )$ , respectively.

Therefore, the overall computational complexity of IMOGOA is $O ( i t e r _ { \operatorname* { m a x } } \times n N _ { p o p } ^ { 2 } \mathrm { l o g } N _ { p o p } )$

## VI. SIMULATION RESULTS

In this part, we perform simulations to verify the effectiveness and efficiency of the proposed strategy and algorithm.

## A. Simulation Setups

We consider 8 IoT terminal devices which are with the queued state for service associated with S. The S is equipped with a PAA with $6 \times 6$ elements and its transmit power is set to 3.6 W. The UAV swarm has 16 UAV individuals that can be operated and the transmit power of each UAV is set to be 0.1 W. Additionally, other parameters about channels and UAVs are shown in Table II. Moreover, the UAV swarm is randomly distributed in a 100 m $\times ~ 1 0 0$ m area. This study selects the carrier frequency 2.4 GHz as it was early exploited by Wi-Fi technology and is still widely supported by many IoT terminal devices.

On the one hand, the effectiveness of our strategy is verified by comparing it with other relay strategies. On the other hand, several multi-objective optimization algorithms are employed to solve the $\mathrm { U S ^ { 2 } R M O P }$ to identify the efficiency of our proposed IMOGOA.

## B. Performance Metric

For the performance of multi-objective optimization algorithms, the convergence and diversity are two critical dimensions. Hypervolume (HV), as a comprehensive evaluation metric has been used frequently to evaluate the comprehensive performance of multi-objective optimization algorithms [49], [50]. Specifically, HV is defined as the hypervolume between the estimated Pareto front $\mathcal { F }$ and the reference vector r, which can be expressed as

$$
H V ( \mathcal { F } , r ) = \mathcal { L } ( \cup _ { 0 \leq i \leq F } [ f _ { 1 } ( i ) , r _ { 1 } ] \times \cdots \times [ f _ { n } ( i ) , r _ { n } ] ) ,\tag{37}
$$

where the reference vector is defined as $r = [ r _ { 1 } , \ldots , r _ { n } ]$ , n is the number of objectives, and the size of $\mathcal { F }$ is represented as $F .$ . Moreover, $[ f _ { 1 } ( i ) , r _ { 1 } ] \times \cdot \cdot \cdot \times [ f _ { n } ( i ) , r _ { n } ]$ represents the hypercubes by all points that are dominated by solution i but not dominated by reference points. Note that $\mathcal { L } ( * )$ is Lebesgue measure, which inscribes the hypervolume of all objectivesâ hypercubes. Specifically, $H V ( { \mathcal { F } } , r )$ is calculated by the Monte Carlo estimation proposed in [49].

## C. Simulation Results

In this section, we first show the visualization results of IMOGOA and compare our strategy with two other relay strategies. Furthermore, several multi-objective optimization algorithms are employed to evaluate the efficiency of IMOGOA. Finally, the performance comparisons of two different schemes with multiple eavesdroppers are analyzed.

1) Visualization Results: Fig. 7 shows the optimization results of IMOGOA, by visualizing the optimized transmission rate distribution of PAA, the optimized transmission rate distribution of UVAA, and the trajectory of UAV swarm. Due to space limitations, we only show a schematic for serving one associated IoT terminal device. From the Fig. 7(a) and (b), we can observe that the transmission rate is the highest in the direction of the target, regardless of whether the direction is towards the UAV receiver at PAA or the IoT terminal device at UVAA. Moreover, the transmission rate is relatively low in the direction of the ground eavesdropper. Furthermore, Fig. 7(c) depicts the trajectory of UAV swarm, demonstrating that the UAVs are appropriately spaced without colliding or coupling with each other, yet not overly dispersed. Accordingly, these results indicate that the proposed IMOGOA can yield significant optimization results by optimizing the three optimization objectives in the given scenario.

2) Comparison With Other Relay Strategies: In this work, we consider other two relay strategies that are the conventional UAV swarm-enabled multi-hop relay [51] and UAV swarm-enabled linear antenna array (LAA) relay [30] for comparison, and these two scenarios are shown in Fig. 8 and the details are as follows.

UAV Swarm-Enabled Multi-Hop Relay Strategy (MRS): The traditional MRS in our simulation design for sequentially serving 8 associated IoT terminal devices where $n = 2 , 4 , 8 , 1 6$ UAVs are equally spaced as hop-by-hop relays.

UAV Swarm-Enabled LAA Relay Strategy (LRS): In our simulation, the traditional LRS is deployed in the center of movement space and set with different array element spacings of 1 m, 2 m, 3 m, 4 m, 5 m.

Fig. 9(a) shows the results for all three objectives with different numbers of hops in UAV swarm-enabled MRS. Note that all the three objectives have been processed by log-transformation because of different orders of magnitude. First, it is clear that as the number of hops increases, the achievable sum rate of IoT terminal devices depicts an upward trend. This is attributed to the diminished channel loss. Specifically, the closer distance and the higher probability of LoS are attained with the increase of hops. Moreover, the achievable sum rate of E exhibits an upward trend with the increase of hops, which is associated with the increase of wiretap links. Additionally, the energy consumption of UAV swarm also shows an upward trend with the increase of hops. Furthermore, Table III provides numerical simulation results for three objectives for the UVAA relay strategy (URS) utilizing the proposed IMOGOA in the case of 16 UAVs and MRS in the cases of 2, 4, 8, 16 UAVs. As can be seen, our strategy has achieved a better trade-off among the three optimization objectives, which provided a lower achievable sum rate of E and less UAV swarm energy consumption with the similar achievable sum rate of IoT terminal devices.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼c)

Fig. 7. Optimization results obtained by IMOGOA. (a) The optimized transmission rate distribution of PAA. (b) The optimized transmission rate distribution of UVAA. (c) The optimized trajectory of UAV swarm.  
<!-- image-->  
Fig. 8. Schematic maps of UAV swarm-enabled multi-hop relay and UAV swarm-enabled LAA relay strategies.

<!-- image-->  
(a)

<!-- image-->  
(b)  
Fig. 9. Performance comparison with other relay strategies. (a) MRS performance with the different number of UAV relay hops. (b) Performance comparison between LRS and URS.

TABLE III  
PERFORMANCE COMPARISON BETWEEN MRS AND URS
<table><tr><td>Benchmarks</td><td>f1[bps]</td><td>f2 [bps]</td><td>f3[J]</td></tr><tr><td>MRS (2 UAVs)</td><td> $2 . 2 8 2 7 \times 1 0 ^ { 5 }$ </td><td> $3 . 8 9 7 4 \times 1 0 ^ { 4 }$ </td><td> $1 . 6 3 2 5 \times 1 0 ^ { 5 }$ </td></tr><tr><td>MRS (4 UAVs)</td><td> $1 . 3 7 3 7 \times 1 0 ^ { 6 }$ </td><td> $6 . 7 7 7 1 \times 1 0 ^ { 4 }$ </td><td> $3 . 2 8 6 5 \times 1 0 ^ { 5 }$ </td></tr><tr><td>MRS (8 UAVs)</td><td> $1 . 3 8 3 7 \times 1 0 ^ { 7 }$ </td><td> $1 . 3 7 2 5 \times 1 0 ^ { 5 }$ </td><td> $6 . 6 0 5 0 \times 1 0 ^ { 5 }$ </td></tr><tr><td>MRS (16 UAVs)</td><td> $1 . 1 8 0 8 \times 1 0 ^ { 8 }$ </td><td> $2 . 6 7 3 8 \times 1 0 ^ { 5 }$ </td><td> $1 . 3 2 2 5 \times 1 0 ^ { 6 }$ </td></tr><tr><td>URS (16 UAVs)</td><td> $3 . 7 0 2 1 \times 1 0 ^ { 6 }$ </td><td> $1 . 6 8 4 6 \times 1 0 ^ { 4 }$ </td><td> $5 . 7 8 1 8 \times 1 0 ^ { 4 }$ </td></tr></table>

TABLE IV

PERFORMANCE COMPARISON BETWEEN LRS AND URS
<table><tr><td>Benchmarks</td><td>f1[bps]</td><td>f2[bps]</td></tr><tr><td>LRS (13 m)</td><td> $1 . 4 7 4 3 \times 1 0 ^ { 6 }$ </td><td> $1 . 1 3 5 8 \times 1 0 ^ { 5 }$ </td></tr><tr><td>LRS (2 m)</td><td> $1 . 4 7 1 2 \times 1 0 ^ { 6 }$ </td><td> $2 . 6 1 2 8 \times 1 0 ^ { 5 }$ </td></tr><tr><td>LRS (3 m)</td><td> $1 . 4 7 1 3 \times 1 0 ^ { 6 }$ </td><td> $6 . 0 7 9 8 \times 1 0 ^ { 4 }$ </td></tr><tr><td>LRS (4 m)</td><td> $1 . 4 8 0 4 \times 1 0 ^ { 6 }$ </td><td> $2 . 4 4 4 1 \times 1 0 ^ { 5 }$ </td></tr><tr><td>LRS (5 m)</td><td> $1 . 4 4 7 4 \times 1 0 ^ { 6 }$ </td><td> $3 . 0 7 2 5 \times 1 0 ^ { 5 }$ </td></tr><tr><td>URS</td><td> $3 . 7 0 2 1 \times 1 0 ^ { 6 }$ </td><td> $1 . 6 8 4 6 \times 1 0 ^ { 4 }$ </td></tr></table>

Fig. 9(b) shows the corresponding simulation results of LRS and URS, where each group of LRS is the mean calculated by simulating 100 times to reduce the effect of randomness. Specifically, according numerical results are listed in Table IV. We can clearly observe that our proposed URS is superior to LRS, which may be due to the advantage of our strategy in the adjustable space of antenna array element positions.

TABLE V  
HYPERPARAMETERS OF THE ALGORITHMS
<table><tr><td>Algorithms</td><td>Hyperparameters</td></tr><tr><td>NSGA-II</td><td> $p _ { c } = 0 . 9 , p _ { m } = 0 . 1$ </td></tr><tr><td>MOPSO</td><td> $w = 0 . 5 , c _ { 1 } = 1 , c _ { 2 } = 2 , w _ { d a m p } = 0 . 9 9$ </td></tr><tr><td>MOGWO</td><td> $\alpha = 0 . 1 , \beta = 4 , \gamma = 2$ </td></tr><tr><td>MOGOA</td><td> $c _ { m a x } = 1 , c _ { m i n } = 0 . 0 0 0 4$ </td></tr><tr><td>MOMVO</td><td> $W E P _ { m a x } = 1 , W E P _ { m i n } = 0 . 2$ </td></tr><tr><td>IMOGOA</td><td> $c _ { m a x } = 1 , c _ { m i n } = 0 . 0 0 0 4 , \alpha _ { 1 } = 0 . 2 , \alpha _ { 2 } = 0 . 2$ </td></tr></table>

TABLE VI

NUMERICAL OPTIMIZATION RESULTS OBTAINED BY DIFFERENT ALGORITHMS
<table><tr><td>Algorithms</td><td>f1[bps]</td><td>f2 [bps]</td><td> $f _ { 3 } \ [ \mathrm { J } ]$ </td><td>HV</td></tr><tr><td>NSGA-II</td><td> $2 . 2 9 2 1 \times 1 0 ^ { 6 }$ </td><td> $3 . 2 1 4 5 \times 1 0 ^ { 4 }$ </td><td> $1 . 3 6 1 7 \times 1 0 ^ { 5 }$ </td><td>0.4604</td></tr><tr><td>MOPSO</td><td> $1 . 9 4 6 1 \times 1 0 ^ { 6 }$ </td><td> $5 . 2 6 7 8 \times 1 0 ^ { 4 }$ </td><td> $1 . 7 5 9 4 \times 1 0 ^ { 5 }$ </td><td>0.3358</td></tr><tr><td>MOGWO</td><td> $1 . 8 1 2 9 \times 1 0 ^ { 6 }$ </td><td> $4 . 0 5 0 0 \times 1 0 ^ { 4 }$ </td><td> $1 . 2 5 3 2 \times 1 0 ^ { 5 }$ </td><td>0.4695</td></tr><tr><td>MOMVO</td><td> $3 . 5 0 6 7 \times 1 0 ^ { 6 }$ </td><td> $6 . 5 8 2 1 \times 1 0 ^ { 4 }$ </td><td> $1 . 5 2 7 8 \times 1 0 ^ { 5 }$ </td><td>0.4303</td></tr><tr><td>MOGOA</td><td> $1 . 9 7 2 7 \times 1 0 ^ { 6 }$ </td><td> $4 . 4 3 1 3 \times 1 0 ^ { 4 }$ </td><td> $1 . 6 9 6 4 \times 1 0 ^ { 5 }$ </td><td>0.3801</td></tr><tr><td>IMOGOA</td><td> $\mathbf { 3 . 7 0 2 1 \times 1 0 ^ { 6 } }$ </td><td> $\mathbf { 1 . 6 8 4 6 \times 1 0 ^ { 4 } }$ </td><td> $\mathbf { 5 . 7 8 1 8 \times 1 0 ^ { 4 } }$ </td><td>0.6615</td></tr></table>

3) Comparison With Other Multi-Objective Optimization Algorithms: In this section, the proposed IMOGOA is compared with five other multi-objective optimization algorithms that are NSGA-II [52], multi-objective particle swarm optimization (MOPSO) [53], multi-objective grey wolf optimizer (MOGWO) [54], multi-objective multi-verse optimization (MOMVO) [55] and conventional MOGOA. The maximum iteration number and population size of each algorithm are set to 500 and 30, respectively. Moreover, the hyperparameters of these algorithms are listed in Table V and the details are as follows.

NSGA-II: NSGA-II draws inspiration from biological evolution theories and it uses fast non-dominated sorting and crowding distance calculation. The advantage of NSGA-II is the fast convergence performance in several optimization problems [56].

MOPSO: MOPSO simulates the collective behavior of bird or fish swarm, and it has an advantage of short computational time and ease of implementation [57].

MOGWO: MOGWO mimics the searching and hunting behavior of grey wolves and it introduces a hypercubebased update strategy for archive. MOGWO is demonstrated to have a strong global search ability for several problems [58].

MOMVO: MOMVO simulates the concept of the parallel universes in multiverse theory and achieves optimization through information exchange between universes. This algorithm has a simple structure, few parameters and strong search capability [59].

Table VI shows the numerical results obtained by these algorithms in terms of the achievable sum rate of IoT terminal devices, achievable sum rate of E, energy consumption of UAV swarm and HV indicator. As can be observed, the proposed IMOGOA achieves the best results on all the three objectives compared to other algorithms. Additionally, the HV indicator of IMOGOA is also larger than other algorithms, which indicates that the comprehensive performance of IMOGOA is superior among all algorithms.

<!-- image-->  
(a)

<!-- image-->

<!-- image-->  
(b)

<!-- image-->  
(c)  
(d)  
Fig. 10. Solution distributions obtained by different algorithms of (a) perspective view, (b) front plan view, (c) left plan view and (d) top plan view. The direction pointed by the red arrow is the direction of true Pareto front.

To further demonstrate, Fig. 10 shows the Pareto solution distributions of these algorithms. Specifically, NSGA-II faces search inefficiency in terms of $f _ { 1 }$ and $f _ { 2 }$ since the crossover and mutation operators are relatively simple and cannot effectively generate new excellent solutions. MOPSO suffers from the poor population diversity, which may be because it does not have good population perturbation and archive update mechanisms. MOGWO traps in local optima due to the insufficient information exchange between grey wolf individuals. Moreover, MOMVO also encounters the problem of the insufficient population diversity, and the reason may be that the population update operation of this algorithm is mainly carried out through relatively simple black hole movements, white hole explosions and big tears. In addition, MOGOA falls into local optima due to the insufficient search efficiency as well as the poor balance performance between exploration and exploitation. Compared to these benchmarks, the proposed IMOGOA has a closer estimated Pareto Front to the actual Pareto Front and better population diversity.

Fig. 11 depicts a more intuitive comparison of solution distributions obtained by the conventional MOGOA and the proposed IMOGOA at various iterations, which indicates the effectiveness of the introduced improvement factors of IMOGOA.

Accordingly, the abovementioned results demonstrate that the proposed IMOGOA is more suitable for solving the US2RMOP and outperforms other benchmarks.

4) Results With Multiple Eavesdroppers: In the real-world scenarios, the proposed method may face the presence of multiple eavesdroppers, which will bring more serious security challenges. Thus, in this part, we verify the performance of the proposed method by considering multiple eavesdroppers. Note that our considered second optimization objective $f _ { 2 }$ will be changed to the maximum achievable sum rate of multiple eavesdroppers5, while other settings remain consistent as Section IV. Specifically, multiple eavesdroppers can work in the following schemes:

<!-- image-->

<!-- image-->  
(b)

(a)  
<!-- image-->  
ï¼cï¼

<!-- image-->  
(d)

Fig. 11. Comparison of solution distributions obtained by MOGOA and IMOGOA of (a) perspective view, (b) front plan view, (c) left plan view and (d) top plan view at different iterations: (i) 1th iteration. (ii) 100th iteration. (iii) 200th iteration. (iv) 400th iteration.  
<!-- image-->  
(a)

<!-- image-->

<!-- image-->  
(b)

(c)  
<!-- image-->  
(d)

<!-- image-->  
(e)

<!-- image-->  
(f)  
Fig. 12. Performance comparison with different number of eavesdroppers. (a) $f _ { 1 }$ under OCTD. (b) $f _ { 2 }$ under OCTD. $\mathrm { ( c ) } f _ { 3 }$ under OCTD. (d) f1 under CTSD. (e) $f _ { 2 }$ under CTSD. (f) $f _ { 3 }$ under CTSD.

C Only Collude in the Time Domain (OCTD): The eavesdropper only colludes alone in the time domain, and these multiple eavesdroppers do not cooperate.

C Collude Both in the Time and Space Domains (CTSD): CTSD has a stronger eavesdropping risk than OCTD, where not only a single eavesdropper colludes in the time domain, but also multiple eavesdroppers at different locations will collude with each other by adopting MRC in the space domain.

Fig. 12(a), (b) and (c) show the performance comparison under OCTD scheme with different numbers of eavesdroppers.

As can be seen, there is no obvious changing trend in $f _ { 1 }$ and $f _ { 3 }$ when the number of eavesdroppers increases, and the proposed IMOGOA also achieves superior performance than other comparison algorithms. The reason is that $f _ { 1 }$ and $f _ { 3 }$ have ignorable relationships with the number of eavesdroppers. However, the results of $f _ { 2 }$ of most algorithms tend to be worse when the number of eavesdroppers increases, while IMOGOA keeps $f _ { 2 }$ almost unchanged. This is because the beam pattern which can suppress multiple eavesdroppers is difficult to search. In this case, the improved solution update and archive update of the proposed IMOGOA can enhance the ability to escape from local optima, thereby boosting the algorithm to search the solutions for suppressing multiple eavesdroppers.

Fig. 12(d), (e) and (f) show the performance comparison under CTSD scheme with different numbers of eavesdroppers. Likewise, the proposed IMOGOA achieves superior performance in $f _ { 1 }$ and $f _ { 3 }$ than other comparison algorithms. However, when focusing on $f _ { 2 } ,$ , the results of $f _ { 2 }$ obtained by all the benchmarks under the CTSD scheme are obviously worse with the increasing number of eavesdroppers, and they are also inferior to the same condition of the OCTD scheme. The reason is that the maximal SNR obtained by eavesdroppers greatly increases due to multiple eavesdroppers colluding in the space domain. In this case, our proposed IMOGOA is still on a slower growth trend in $f _ { 2 } ,$ , which also validates the robustness and scalability of the IMOGOA.

## VII. DISCUSSIONS

In this section, the motivations for using a rotary-wing UAV swarm, the rationality for assuming high-rate communications within UAV swarm and the impact of cooperative reception or diversity combining scheme of UAVs are further discussed.

## A. Motivations for Using a Rotary-Wing UAV Swarm

Using the rotary-wing UAVs to construct the relay swarm is more reasonable for the considered scenario, and the reasons are explained in Appendix B of the supplementary material available online.

## B. Rationality of High-Rate Communications Within UAV Swarm

In this work, we assume that the UAVs in the swarm can communicate with each other at a high rate, and the corresponding rationality are presented in Appendix C of the supplementary material available online.

## C. Impact of Cooperative Reception or Diversity Combing

The cooperative reception or diversity combining can be a potential scheme to improve communication performance in most scenarios. However, this scheme may be inappropriate for the considered system, and the specific reasons are provided in Appendix D of the supplementary material available online.

## VIII. CONCLUSION

In this article, the UAV swarm-enabled collaborative secure relay system is proposed where a UAV swarm serves for forwarding confidential messages from the source MBS with PAA to the remote IoT terminal devices via CB so as to counteract the threat of the eavesdropper colluding in the time domain. Furthermore, we formulate a US2RMOP to maximize the achievable sum rate of all IoT terminal devices, minimizing the achievable sum rate of the eavesdropper, and minimizing the energy consumption of UAV swarm. Subsequently, an IMOGOA with several improvements is proposed to solve the US2RMOP. Simulation results illustrate the effectiveness of the proposed UAV swarm-enabled collaborative secure relay system by comparing both traditional UAV swarm-enabled multi-hop relay and LAA relay strategies, and verify that IMOGOA has better performance than several other comparison algorithms. In addition, IMOGOA is more stable and effective under OCTD and CTSD with multiple eavesdroppers.

## REFERENCES

[1] C. Zhang, G. Sun, J. Li, and X. Zheng, âBi-objective optimization for UAV swarm-enabled relay communications via collaborative beamforming,â in Proc. IEEE 26th Int. Conf. Comput. Supported Cooperative Work Des., 2023, pp. 984â989.

[2] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[3] L. Zhu, J. Zhang, Z. Xiao, X. Xia, and R. Zhang, âMulti-UAV aided millimeter-wave networks: Positioning, clustering, and beamforming,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 4637â4653, Jul. 2022.

[4] J. Liu, X. Du, J. Cui, M. Pan, and D. Wei, âTask-oriented intelligent networking architecture for the space-air-ground-aqua integrated network,â IEEE Internet Things J., vol. 7, no. 6, pp. 5345â5358, Jun. 2020.

[5] L. Zhu, J. Zhang, Z. Xiao, X. Cao, X. Xia, and R. Schober, âMillimeterwave full-duplex UAV relay: Joint positioning, beamforming, and power control,â IEEE J. Sel. Areas Commun., vol. 38, no. 9, pp. 2057â2073, Sep. 2020.

[6] J. Li et al., âMulti-objective optimization approaches for physical layer secure communications based on collaborative beamforming in UAV networks,â IEEE/ACM Trans. Netw., vol. 31, no. 4, pp. 1902â1917, Aug. 2023, doi: 10.1109/TNET.2023.3234324.

[7] M. Samir, S. Sharafeddine, C. M. Assi, T. M. Nguyen, and A. Ghrayeb, âUAV trajectory planning for data collection from time-constrained IoT devices,â IEEE Trans. Wireless Commun., vol. 19, no. 1, pp. 34â46, Jan. 2020.

[8] H. Pan, Y. Liu, G. Sun, J. Fan, S. Liang, and C. Yuen, âJoint power and 3D trajectory optimization for UAV-enabled wireless powered communication networks with obstacles,â IEEE Trans. Commun., vol. 71, no. 4, pp. 2364â2380, Apr. 2023.

[9] Y. Zeng, J. Lyu, and R. Zhang, âCellular-connected UAV: Potential, challenges, and promising technologies,â IEEE Wireless Commun., vol. 26, no. 1, pp. 120â127, Feb. 2019.

[10] S. Zhang and J. Liu, âAnalysis and optimization of multiple unmanned aerial vehicle-assisted communications in post-disaster areas,â IEEE Trans. Veh. Technol., vol. 67, no. 12, pp. 12049â12060, Dec. 2018.

[11] G. Sun et al., âUAV-enabled secure communications via collaborative beamforming with imperfect eavesdropper information,â IEEE Trans. Mobile Comput., early access, doi: 10.1109/TMC.2023.3273293.

[12] H. Ochiai, P. Mitran, H. V. Poor, and V. Tarokh, âCollaborative beamforming for distributed wireless ad hoc sensor networks,â IEEE Trans. Signal Process., vol. 53, no. 11, pp. 4110â4124, Nov. 2005.

[13] M. F. A. Ahmed and S. A. Vorobyov, âCollaborative beamforming for wireless sensor networks with Gaussian distributed sensor nodes,â IEEE Trans. Wireless Commun., vol. 8, no. 2, pp. 638â643, Feb. 2009.

[14] J. Zhang and M. C. Gursoy, âCollaborative relay beamforming for secrecy,â in Proc. IEEE Int. Conf. Commun., 2010, pp. 1â5.

[15] W. Yang, K. Wang, X. Xu, and J. Zhou, âSecure transmission for AF relaying spectrum-sharing systems with collaborative distributed beamforming,â in Proc. 25th Wireless Opt. Commun. Conf., 2016, pp. 1â4.

[16] G. Sun, J. Li, A. Wang, Q. Wu, Z. Sun, and Y. Liu, âSecure and energy-efficient UAV relay communications exploiting collaborative beamforming,â IEEE Trans. Commun., vol. 70, no. 8, pp. 5401â5416, Aug. 2022.

[17] J. Li, H. Kang, G. Sun, S. Liang, Y. Liu, and Y. Zhang, âPhysical layer secure communications based on collaborative beamforming for UAV networks: A multi-objective optimization approach,â in Proc. IEEE 40th Conf. Comput. Commun., 2021, pp. 1â10.

[18] F. Ono, H. Ochiai, and R. Miura, âA wireless relay network based on unmanned aircraft system with rate optimization,â IEEE Trans. Wireless Commun., vol. 15, no. 11, pp. 7699â7708, Nov. 2016.

[19] M. T. Dabiri, M. Hasna, N. Zorba, T. Khattab, and K. A. Qaraqe, âEnabling long mmWave aerial backhaul links via fixed-wing UAVs: Performance and design,â IEEE Trans. Commun., vol. 71, no. 10, pp. 6146â6161, Oct. 2023.

[20] M. A. Bliss and N. Michelusi, âPower-constrained trajectory optimization for wireless UAV relays with random requests,â in Proc. IEEE Int. Conf. Commun., 2020, pp. 1â6.

[21] R. Fan, J. Cui, S. Jin, K. Yang, and J. An, âOptimal node placement and resource allocation for UAV relaying network,â IEEE Commun. Lett., vol. 22, no. 4, pp. 808â811, Apr. 2018.

[22] C. Zhong, J. Yao, and J. Xu, âSecure UAV communication with cooperative jamming and trajectory control,â IEEE Commun. Lett., vol. 23, no. 2, pp. 286â289, Feb. 2019.

[23] Y. Cai, F. Cui, Q. Shi, M. Zhao, and G. Y. Li, âDual-UAV-enabled secure communications: Joint trajectory design and user scheduling,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1972â1985, Sep. 2018.

[24] Y. Zhou et al., âImproving physical layer security via a UAV friendly jammer for unknown eavesdropper location,â IEEE Trans. Veh. Technol., vol. 67, no. 11, pp. 11280â11284, Nov. 2018.

[25] X. Sun, W. Yang, and Y. Cai, âSecure communication in NOMA-assisted millimeter-wave SWIPT UAV networks,â IEEE Internet Things J., vol. 7, no. 3, pp. 1884â1897, Mar. 2020.

[26] F. Cheng, G. Gui, N. Zhao, Y. Chen, J. Tang, and H. Sari, âUAV-relayingassisted secure transmission with caching,â IEEE Trans. Commun., vol. 67, no. 5, pp. 3140â3153, May 2019.

[27] Z. Na, C. Ji, B. Lin, and N. Zhang, âJoint optimization of trajectory and resource allocation in secure UAV relaying communications for Internet of Things,â IEEE Internet Things J., vol. 9, no. 17, pp. 16284â16296, Sep. 2022.

[28] J. Ji, K. Zhu, D. Niyato, and R. Wang, âJoint trajectory design and resource allocation for secure transmission in cache-enabled UAV-relaying networks with D2D communications,â IEEE Internet Things J., vol. 8, no. 3, pp. 1557â1571, Feb. 2021.

[29] S. Mohanti et al., âAirBeam: Experimental demonstration of distributed beamforming by a swarm of UAVs,â in Proc. IEEE 16th Int. Conf. Mobile Ad Hoc Sensor Syst., 2019, pp. 162â170.

[30] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âCommunications and control for wireless drone-based antenna array,â IEEE Trans. Commun., vol. 67, no. 1, pp. 820â834, Jan. 2019.

[31] P. Dinh, T. M. Nguyen, S. Sharafeddine, and C. Assi, âJoint location and beamforming design for cooperative UAVs with limited storage capacity,â IEEE Trans. Commun., vol. 67, no. 11, pp. 8112â8123, Nov. 2019.

[32] S. Zhu, K. Yang, J. Ouyang, and Y. Du, âCooperative beamforming for UAV-assisted cognitive relay networks with partial channel state information,â in Proc. IEEE 4th Int. Conf. Comput. Commun., 2018, pp. 158â162.

[33] L. Yang, J. Chen, H. Jiang, S. A. Vorobyov, and H. Zhang, âOptimal relay selection for secure cooperative communications with an adaptive eavesdropper,â IEEE Trans. Wireless Commun., vol. 16, no. 1, pp. 26â42, Jan. 2017.

[34] S. Yan and R. A. Malaney, âLocation-based beamforming for enhancing secrecy in Rician wiretap channels,â IEEE Trans. Wireless Commun., vol. 15, no. 4, pp. 2780â2791, Apr. 2016.

[35] X. Sun, D. W. K. Ng, Z. Ding, Y. Xu, and Z. Zhong, âPhysical layer security in UAV systems: Challenges and opportunities,â IEEE Wireless Commun., vol. 26, no. 5, pp. 40â47, Oct. 2019.

[36] B. Duo, H. Hu, Y. Li, Y. Hu, and X. Zhu, âRobust 3D trajectory and power design in probabilistic LoS channel for UAV-enabled cooperative jamming,â Veh. Commun., vol. 32, Dec. 2021, Art. no. 100387.

[37] C. A. Balanis, Antenna Theory: Analysis and Design, 4th ed. Hoboken, NJ, USA: Wiley, 2016.

[38] R. Ding, F. Gao, and X. S. Shen, â3D UAV trajectory design and frequency band allocation for energy-efficient and fair communication: A deep reinforcement learning approach,â IEEE Trans. Wireless Commun., vol. 19, no. 12, pp. 7796â7809, Dec. 2020.

[39] N. Babu, M. Virgili, C. B. Papadias, P. Popovski, and A. J. Forsyth, âCostand energy-efficient aerial communication networks with interleaved hovering and flying,â IEEE Trans. Veh. Technol., vol. 70, no. 9, pp. 9077â9087, Sep. 2021.

[40] S. Burer and A. N. Letchford, âNon-convex mixed-integer nonlinear programming: A survey,â Surv. Oper. Res. Manage. Sci., vol. 17, pp. 97â106, Jul. 2012.

[41] B. Cao, S. Fan, J. Zhao, P. Yang, K. Muhammad, and M. Tanveer, âQuantum-enhanced multiobjective large-scale optimization via parallelism,â Swarm Evol. Comput., vol. 57, Sep. 2020, Art. no. 100697.

[42] S. Z. Mirjalili, S. Mirjalili, S. Saremi, H. Faris, and I. Aljarah, âGrasshopper optimization algorithm for multi-objective optimization problems,â Appl. Intell., vol. 48, no. 4, pp. 805â820, Aug. 2018.

[43] J. Luo, H. Chen, Q. Zhang, Y. Xu, H. Huang, and X. Zhao, âAn improved grasshopper optimization algorithm with application to financial stress prediction,â Appl. Math. Model., vol. 64, pp. 654â668, Dec. 2018.

[44] J. Wu et al., âDistributed trajectory optimization for multiple solarpowered UAVs target tracking in urban environment by adaptive grasshopper optimization algorithm,â Aerosp. Sci. Technol., vol. 70, pp. 497â510, Nov. 2017.

[45] A. A. Heidari, H. Faris, I. Aljarah, and S. Mirjalili, âAn efficient hybrid multilayer perceptron neural network with grasshopper optimization,â Soft Comput., vol. 23, no. 17, pp. 7941â7958, Jul. 2019.

[46] D. E. Goldberg and R. Lingle, âAlleles, loci, and the traveling salesman problem,â in Proc. 1st Int. Conf. Genet. Algorithms Appl., 2014, pp. 154â159.

[47] W. Zhao, Z. Zhang, S. Mirjalili, L. Wang, N. Khodadadi, and S. M. Mirjalili, âAn effective multi-objective artificial hummingbird algorithm with dynamic elimination-based crowding distance for solving engineering design problems,â Comput. Methods Appl. Mech. Eng., vol. 398, Aug. 2022, Art. no. 115223.

[48] M. Dai, T. H. Luan, Z. Su, N. Zhang, Q. Xu, and R. Li, âJoint channel allocation and data delivery for UAV-assisted cooperative transportation communications in post-disaster networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 16676â16689, Sep. 2022.

[49] J. Bader and E. Zitzler, âHypE: An algorithm for fast hypervolume-based many-objective optimization,â Evol. Comput., vol. 19, no. 1, pp. 45â76, Mar. 2011.

[50] J. Zhang, Z. Ning, R. H. Ali, M. Waqas, S. Tu, and I. Ahmad, âA many-objective ensemble optimization algorithm for the edge cloud resource scheduling problem,â IEEE Trans. Mobile Comput., vol. 23, no. 2, pp. 1330â1346, Feb. 2024, doi: 10.1109/TMC.2023.3235064.

[51] T. Kim and D. Qiao, âEnergy-efficient data collection for IoT networks via cooperative multi-hop UAV networks,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13796â13811, Nov. 2020.

[52] K. Deb, S. Agrawal, A. Pratap, and T. Meyarivan, âA fast and elitist multiobjective genetic algorithm: NSGA-II,â IEEE Trans. Evol. Comput., vol. 6, no. 2, pp. 182â197, Apr. 2002.

[53] C. A. C. Coello and M. S. Lechuga, âMOPSO: A proposal for multiple objective particle swarm optimization,â in Proc. Congr. Evol. Comput., 2002, pp. 1051â1056.

[54] S. Mirjalili, S. Saremi, S. M. Mirjalili, and L. dos Santos Coelho, âMultiobjective grey wolf optimizer: A novel algorithm for multi-criterion optimization,â Expert Syst. Appl., vol. 47, pp. 106â119, Apr. 2016.

[55] S. Mirjalili, P. Jangir, S. Z. Mirjalili, S. Saremi, and I. N. Trivedi, âOptimization of problems with multiple objectives using the multi-verse optimization algorithm,â Knowl. Based Syst., vol. 134, pp. 50â71, Oct. 2017.

[56] H. Li, B. Wang, Y. Yuan, M. Zhou, Y. Fan, and Y. Xia, âScoring and dynamic hierarchy-based NSGA-II for multiobjective workflow scheduling in the cloud,â IEEE Trans Autom. Sci. Eng., vol. 19, no. 2, pp. 982â993, Apr. 2022.

[57] X. Zheng and H. Liu, âA scalable coevolutionary multi-objective particle swarm optimizer,â Int. J. Comput. Intell. Syst., vol. 3, no. 5, pp. 590â600, 2010.

[58] B. Zhou and Y. Lei, âBi-objective grey wolf optimization algorithm combined levy flight mechanism for the FMC green scheduling problem,â Appl. Soft Comput., vol. 111, 2021, Art. no. 107717.

[59] Y. Alaouchiche, Y. Ouazene, and F. Yalaoui, âMulti-objective optimization of energy-efficient buffer allocation problem for non-homogeneous unreliable production lines,â IEEE Access, vol. 10, pp. 3320â3335, 2022.

<!-- image-->

Chuang Zhang received the BS degree in 2021 in computer science and technology from Jilin University, Changchun, China, where he is currently working toward the PhD degree with the College of Computer Science and Technology. His research interests include UAV communications, distributed beamforming, and multi-objective optimization.

<!-- image-->

beamforming, and optimizations.

Geng Sun (Member, IEEE) received the BS degree in communication engineering from Dalian Polytechnic University, China, and the PhD degree in computer science and technology from Jilin University, China, in 2011 and 2018, respectively. He was a visiting researcher with the School of Electrical and Computer Engineering, Georgia Institute of Technology, USA. He is currently an Associate Professor with the College of Computer Science and Technology, Jilin University. His research interests include wireless networks, UAV communications, collaborative

<!-- image-->

Qingqing Wu (Senior Member, IEEE) received the BEng degree in electronic engineering from the South China University of Technology, China, in 2012, and the PhD degree in electronic engineering from Shanghai Jiao Tong University, China, in 2016. From 2016 to 2020, he was a Research Fellow with the Department of Electrical and Computer Engineering, National University of Singapore, Singapore. He is currently an associate professor with Shanghai Jiao Tong University. He has coauthored more than 100 IEEE journal papers with 26 ESI highly cited papers

and eight ESI hot papers, which have more than 18,000 Google citations. His research interest includes intelligent reflecting surface (IRS), unmanned aerial vehicle (UAV) communications, and MIMO transceiver design. He was listed as the Clarivate ESI Highly Cited Researcher in 2022 and 2021, the Most Influential Scholar Award in AI-2000 by Aminer in 2021 and Worldâs Top 2% Scientist by Stanford University in 2020 and 2021.

<!-- image-->

Jiahui Li (Student Member, IEEE) received the BS degree in software engineering, and the MS degree in computer science and technology from Jilin University, Changchun, China, in 2018 and 2021, respectively. He is currently working toward the PhD degree in computer science with Jilin University, China. He is also a visiting PhD degree student with the Singapore University of Technology and Design, Singapore. His research interests include UAV networks, antenna arrays, and optimization.

<!-- image-->

Shuang Liang received the BS degree in communication engineering from Dalian Polytechnic University, China, in 2011, the MS degree in software engineering from Jilin University, China, in 2017, and the PhD degree in computer science from Jilin University, China, in 2022. She is currently a postdoctoral with the School of Information Science and Technology, Northeast Normal University. Her research interests include wireless communication and UAV networks.

<!-- image-->  
Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkuts Institute of Technology Ladkrabang, Thailand, in 1999, and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada, in 2008. He is currently a professor with the School of Computer Science and Engineering, Nanyang Technological University, Singapore. His research interests include the Internet of Things (IoT), machine learning, and incentive mechanism design.

<!-- image-->

Victor C.M. Leung (Life Fellow, IEEE) is currently a distinguished professor of computer science and software engineering with Shenzhen University, China. He is also an emeritus professor of electrial and computer engineering and the director with the Laboratory for Wireless Networks and Mobile Systems, University of British Columbia (UBC). He has coauthored more than 1300 journal/conference papers and book chapters, and is also named in the current Clarivate Analytics list of Highly Cited Researchers. His research interests include the broad areas of wireless

networks and mobile systems. Dr. Leung is also on the editorial boards of IEEE Transactions on Green Communications and Networking, IEEE Transactions on Cloud Computing, IEEE Access, and several other journals. He was the recipient of the IEEE Vancouver Section Centennial Award, 2011 UBC Killam Research Prize, 2017 Canadian Award for Telecommunications Research, 2018 IEEE TCGCC Distinguished Technical Achievement Recognition Award, and has coauthored papers that was the recipient of the 2017 IEEE ComSoc Fred W. Ellersick Prize, 2017 IEEE Systems Journal Best Paper Award, 2018 IEEE CSIM Best Journal Paper Award, and 2019 IEEE TCGCC Best Journal Paper Award. He is also the life fellow of IEEE, and a fellow of the Royal Society of Canada, Canadian Academy of Engineering, and Engineering Institute of Canada.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_8_img_1.jpeg|page_8_img_1]]
3. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_14_img_1.jpeg|page_14_img_1]]
4. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_14_img_2.jpeg|page_14_img_2]]
5. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_18_img_1.jpeg|page_18_img_1]]
6. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_18_img_2.jpeg|page_18_img_2]]
7. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_18_img_3.jpeg|page_18_img_3]]
8. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_18_img_4.jpeg|page_18_img_4]]
9. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_18_img_5.jpeg|page_18_img_5]]
10. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_19_img_1.jpeg|page_19_img_1]]
11. [[../extracted_images/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper/page_19_img_2.jpeg|page_19_img_2]]

---

