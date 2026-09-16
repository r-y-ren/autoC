# MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Channel Gain

Jiehong Wu , Member, IEEE, Jianzhou Zhou, Lei Yu, and Lijun Gao

AbstractâFANET (Fly-Adhoc-Network) does not rely on prebuilt infrastructure, and can form a temporary network through wireless links anytime and anywhere, which has been widely used in emergency communication and disaster relief. In order to solve the problem of signal transmission fading caused by heavy fog, heavy smoke and other harsh environments, and data packet transmission failure caused by high speed movement of unmanned aerial vehicle (UAV), a cooperative transmission mode is adopted to select a relay at the data link layer for packet forwarding, which effectively improves the network communication performance. Aiming at the problem of limited communication of UAV swarm in harsh environment, a cooperative medium access control protocol named energy consumption and channel gain cooperative medium access control protocol (EC-CMAC) for FANET is proposed. The protocol estimate the transmit power according to the channel propagation model, and further propose a relay selection strategy according to the estimate transmit power, the residual energy of the node, the direction and position of the node, and adaptively selecting the transmission mode. During cooperative transmission, it selected one-hop neighbors to forward the message, and extended the network lifetime by optimizing the energy consumption of the UAVs. The protocol is verified both statically and dynamically in MATLAB environment. The evaluation results of end-to-end delay, network throughput, network lifetime and packet transmission ratio testify that EC-CMAC can achieve longer network lifetime and higher packet delivery rate with little delay and throughput loss in harsh transmission environment and high speed movement of UAVs.

Index TermsâMedia access control protocol, network lifetime, relay selection, FANET, cooperative UAVs.

## I. INTRODUCTION

N RECENT years, unmanned aerial vehicles (UAVs) have I been widely used in many fields because of their advantages such as convenience, flexibility and efficiency. For example, in the high incidence season of forest fires, UAVs are used for high-altitude patrol and fire detection [1], [2]. In the area where the basic communication facilities are damaged after the earthquake, the UAV is used for emergency auxiliary communication [3], [4], [5], and post disaster search and rescue [6], [7]. However, because of the low working efficiency of a single UAV, the UAV swarm composed of multiple UAVs have gradually replaced the single UAV working mode. Flying-Adhoc-Network (FANET) [8] is a kind of decentralized, self-organizing multi hop wireless network, which does not rely on an infrastructure erected in advance and can form temporary networks via wireless links anytime and anywhere. Due to FANETâs high mobility, frequent topological changes, and limited power, it is difficult to design reliable communication solutions. At the same time, designing different FANET solutions requires meeting different quality of service requirements. For example, real-time monitoring and search have a large demand for network delay, and the link interruption caused by high-speed movement should be considered when the UAV performs decentralized tasks. In the field of post-disaster emergency communication, the energy demand of UAV becomes particularly important.

In the early stage, the research work of FANET is focus on the network layer, and the most common are reactive routing represented by Ad-hoc On-Demand Distance Vector Routing (AODV) and prior routing represented by Optimized Link State Routing (OLSR). The routing metric of AODV is re-selected [9] and the message maintenance interval of OLSR is adaptively adjusted to adapt to different application scenarios and meet different QoS [10]. In order to overcome the influence of channel fading and meet the energy demand of communication system, many MAC protocols based on data link layer come into being. Time Division Multiple Access (TDMA) is a reservation-based technique for sharing channels among users for interference-free data transmission. In this technique, the channel is divided into time slots and each time slot is assigned to an independent user. Each user with TDMA can access the channel according to the assigned rules, therefore, collision-free transmission can be achieved on the same frequency [11]. Compared with TDMA protocol, Carrier Sense Multiple Access with Collision Avoid (CSMA/CA) protocol defined in 802.11 Distributed Coordination Function (DCF) makes message carrying easier because of its broadcast characteristics. In the DCF-based protocol, a handshake mechanism is used, using Request Send (RTS) and Clear to Send (CTS) frames to preserve the channel before the data transfer [12], [13]. In CSMA/CA, nodes randomly select the back-off value in the contention window (CW) to avoid the channel contention problem. However, in different transmission environments, constant CW has some disadvantages. Therefore, adjusting the size of CW adaptively to different requirement can solve this problem [12]. In addition, in [14], [15], [16], [17], [18], [19], the adaptive MAC protocol can adaptively switch between the two protocols according to different environments and requirements, so as to meet different QoS. Multi-channel dynamic allocation mechanism allocates channel resources to different services to improve communication quality [20], [21].

<!-- image-->  
Fig. 1. Cooperative media access control.

In the real communication environment, especially in the harsh air environment, such as smoke or dusty weather caused by forest fires, strong electromagnetic wave scattering is generated due to the high density of particles and the movement of charged particles [22]. Due to the propagation fading characteristics of wireless signals, the signal strength between a pair of UAVs communication is often lower than expected. If we want to guarantee the reliability of transmission, we must increase the transmitting power of communication. In addition, because of the high-speed movement of the UAV, the position of the UAV is also changing frequently. Combined with the above two scenarios, the communication links between UAVs are interrupted frequently and have high energy consumption. While Multiple Input Multiple Output (MIMO) [23], [24] antennas can improve the transmission reliability and capacity of wireless networks, and in small UAVs, MIMO antennas are limited by their size and high energy consumption. cooperative communication (CC) [25], as a technology to reduce energy consumption and improve network life and reliability, has been applied to UAV communication, as shown in Fig. 1. In UAV communication system, reactive power relay is introduced to receive and forward information to gain performance. However, cooperative communication is not always energy efficient due to the additional overhead required for cooperative transmission. The key to the problem is to save the energy consumption of UAVs while maintaining high transmission efficiency.

The application of cooperative communication in TDMA is to select the relay node to use the free slots caused by the change of network topology for dynamic slot allocation, and select the candidate relay node to use the free slots to re-transmit the failed packets of the source node [26], [27], [28]. However, TDMA-based CC requires precise time synchronization, and it is difficult to account for node energy. In CC, the main functions of RTS/CTS transmissions are to estimate channel conditions and transmit additional information. Depending on the additional information transmitted in the frame, the selection of relay has different policies to meet different QoS in different environments. In [29], the transmission rate is attached to the CTS, each node listens to the CTS frames of all other adjacent contacts, and estimates the channel state between the source node and the target node by extracting the information in the CTS frames. In addition, in [30], a table of potential relay nodes is introduced, where each node or base station maintains a list of data rates of potential neighbor nodes, passively listens to all ongoing transmissions, and updates cooperative entries, with high-rate nodes assisting cyclic nodes to retransmit their data to the destination faster links.

There are few researches on transmission efficiency and node energy of existing CMAC protocols. While some protocols focus on the energy of nodes, there are some drawbacks in the selection of relay nodes due to the high speed movement of UAVs and frequent changes in links. This paper proposes a MAC protocol based on channel state and energy sensing, called energy channel cooperative media access control. EC-CMAC improves on the IEEE802.11 DCF, in which the UAV node adaptively selects the transmission mode between direct transmission and collaborative transmission. In the process of cooperative transmission, the selection of relay nodes takes into account the channel states between nodes, the energy of nodes, the direction and position of nodes, and forwards the message from the source node to the target node through the one-hop relay node. The contributions of this paper are as follows:

1) We propose an protocol named EC-CMAC, it based on FANET to improve the network transmission efficiency and reduce the transmission energy consumption of UAVs by selecting the relay for cooperative communication in order to solve the link interruption and energy consumption problem of UAV swarm in complex communication environment.

2) A channel model of N-LOS link in complex communication environment is proposed, which considers path loss, shadow fading and multi-path effect.

3) A relay selection strategy for cooperative communication is proposed, which selects the appropriate relay node to forward the message through the relay back-off function, which takes into account the channel states between nodes, the residual energy of UAV nodes, the estimated transmitting power, and the direction and position of UAV motion.

## II. RELATED WORK

In recent years, many scholars have conducted in depth research in the field of collaborative communications. The main research fields in collaborative communications are the necessity of collaboration, i.e., the timing of collaboration, the way of collaboration and the advantages of collaborative transmission over direct transmission. The reliability of the link and the overall performance of the network is directly affected by collaborative transmission. The relay selection strategy is diverse in different protocols. In [31], a distributed cooperative MAC (CAH-MAC) protocol based on TDMA is proposed. In order to solve the problem of time slot waste caused by topology changes, idle time slots are used as cooperative relays for data transmission. In CAH-MAC, potential relay nodes that can listen for transmission failures enter the relay stage and use the idle time interval of the superframe to re-transmit the failed packets of the original source node. Since the source node does not need to wait until the next frame to transmit again, successful transfers and throughput are significantly improved. However, because CAH-MAC uses additional information to allocate time slots and relay options, it adds overhead to the system. A cooperative MAC protocol based on TDMA (DC-TDMA) is proposed in [32] to improve the throughput of multi-hop networks. DC-TDMA uses time slots in TDMA for dynamic slot allocation. The frame is divided into signaling cycle and data transmission cycle, which are used to exchange the main information of collaborative slot allocation and the time period reserved for data transmission. Similar to [33], the neighbor node that successfully decodes the failed source packet acts as a candidate node. Each source node and candidate node reserve a slot in its time slot for re-transmitting failed packets.

Since propagation is affected by signal fading, many scholars have regarded the strength of the signal as a criterion for collaborative transmission. In [29], [30], the selection of relay is based on the premise that nodes are fixed and channel conditions are unchanged in the process of data transmission. In fact, in real applications, the node will constantly change its position, speed and direction, while the channel will also change in real time. These factors do not guarantee the reasonableness of relay selection, and even cooperative communication gains are lower than direct transmission. To solve this problem, a more efficient cooperative MAC protocol based on instantaneous channel conditions proposed an automatic rate MAC protocol CRBAR based on reactive cooperative relay [33]. In CRBAR, a high-rate node adaptively selects itself as a relay node and specifies the transmission rate and relay scheme according to the instantaneous channel information. A low-rate node sends a message through a high-rate relay node. In the selection process of relay node, single factor has certain disadvantages, so some protocols use multiple factors to set the regression function to select the relay node. The author in [34] propose a relay selection scheme based on maximum link benefit. In a multi-hop network, the candidate relay node is the neighbor node that overhears the previous hop data transmission. Then, the candidate relay node first calculates its utility value based on the instantaneous channel information and increases its benefit by transmission rate and power. and calculate the rollback values of all candidate relay nodes. The node with the highest link benefits has a smaller rollback value and is more likely to be selected as a relay node. It is worth noting that the selection of candidate relay nodes benefits from the RTS/CTS mechanism of 802.11DCF. Nodes first broadcast RTS frames to compete for channels, then target nodes broadcast CTS to indicate that it can receive messages, and nodes that receive both RTS and CTS participate in relay node competition. At the same time, the information needed for node contention is attached to RTS and CTS frames, and the winning node sends RTH frames containing the transmission rate and type to preserve the channel for collaborative transmission. In [35], the source selects the node that supports a higher transmission rate as the relay node. it use a table structure to select the best relay and update it with additional control packet exchange. Like [34], the control package includes the MAC address, the signal-to-noise ratio, and the latest timestamp of the best cooperative table entry. However, in [34] and [35], the process of relay selection, there is a lack of power optimization and energy, so the performance of the network lifetime is not satisfied.

<!-- image-->  
Fig. 2. Network model.

In addition, energy consumption has always been one of the important factors affecting the work of MAC layer. The authors in [36] propose an adaptive CMAC protocol (DEL-CMAC), which is also based on DCF and carries node energy information and optimal transmission power in RTS frame and CTS frame, and relay nodes compete for the best relay node according to residual energy and transmission power. This protocol is mainly used for extended mobile AD hoc networking (MANET). Although the protocol prolongs the network lifetime of MANET, it pays less attention to the channel state, the location and energy consumption of auxiliary nodes. Moreover, in DEL-CMAC, the criterion of direct transmission and cooperative transmission is only the threshold of transmitting power. When the power of the source node is low, it is not accurate to judge the transmission mode only by the power threshold. In addition, in DEL-CMAC, all nodes are in the same subnet, which cannot accurately reflect the network performance in a multi-hop environment. In [37], although lifetime extended sensing CMAC uses asymmetric transmission power to extend the network lifetime, source node and destination node remain unchanged during the experiment and cannot adapt to the rapid changes of nodes.

## III. SYSTEM MODEL

## A. Network Model

As shown in Fig. 2, N nodes are deployed in the collaboration area to form a UAV cluster. Each UAV is equipped with a wireless communication module and GPS tracking system, which can move autonomously and have the same speed of movement. Their direction of movement is random and they return when they touch the boundary of the area. UAV nodes in the same communication range in the network share the same wireless channel. The network layer is used for routing addressing and constructing routing table. The proposed MAC protocol works on the basis of the routing table already established, that is, optimizes the metrics in the process of data transmission rather than in the process of routing addressing. However, a qualified network layer protocol is supposed to establish more stable routing paths, which can further improve the optimization level of MAC protocol. In FANET, routing protocols can be roughly divided into two types, i.e., prior routing and reactive routing. Prior routing is represented by OLSR, which selects a part of neighbor nodes as MPRs and only allows these nodes to disseminate control messages. However, the control packets required by prior routing will occupy a large amount of network overhead. Reactive routing, for example, based on Dynamic Source Routing (DSR) protocol, the head of the data packet carries the routing information datagram to the destination node, which is forwarded by these nodes to the destination node. This mechanism can avoid updating information constantly during datagram transmission, and save the latest routing information to the cache to adapt to the change of transmission path. The network layer protocol in this paper uses the DSR protocol, first constructs the routing path through the DSR protocol, and then optimizes the frame interaction process of the MAC layer in the process of data transmission, and selects the relay node to improve the network performance. The UAV node first looks for the IP address of the target UAV in the routing table, and initiates routing addressing if no route has been established. After the IP address of the target UAV node is determined, the MAC address corresponding to the target node is found by querying the ARP table, and then the corresponding frame header is added to encapsulate the datagram into a frame and sent to the data link layer. The data link layer transmits data through the improved MAC protocol via the MAC address obtained by querying. The specific interaction flow of the data link layer is given in Section IV. The physical layer adopts 802.11b standard and supports multi-rate mode.

## B. Energy Model

The energy model in this paper is divided into two parts, namely, the motion consumption part $( E _ { m o b i l e } )$ and the transmission consumption part $( E _ { t r a n s } )$ , and the total energy consumption is $E _ { t o t a l } = E _ { m o b i l e } + E _ { t r a n s }$ . All UAV nodes have the same initial energy. The flight energy consumption of UAV is $E _ { f l y }$ and the hover energy consumption is $E _ { h o l d }$ . In the real environment, UAV consume energy whether they send, receive or process data. Therefore, the communication energy consumed by frame interaction is $E _ { t r a n s } = ( p _ { t } + p _ { r } + p _ { h } ) \times T$ , where $p _ { t }$ represents transmitting power, pr represents receiving power, and $p _ { h }$ represents processing power.

## C. Channel Gain Model

In order to better represent the severe fading of the signal due to the scattering of charged particles, we adopt the combination of large-scale fading and small-scale fading for channel modeling [38]. Since the LOS link cannot be captured, the free space propagation model is not suitable for the propagation environment proposed in this paper. In a real environment, the received signal power decreases logarithmically with distance. By introducing the path loss index that changes with the environment, the free space path loss model is modified, and the log-distance path loss model is obtained:

$$
[ P _ { L } ( d ) ] _ { d b } = - 1 0 l o g _ { 1 0 } \left( \frac { G _ { t } G _ { r } \lambda ^ { 2 } } { ( 4 \pi d _ { 0 } ) ^ { 2 } } + 1 0 n l o g _ { 1 0 } ( d / d _ { 0 } ) \right)\tag{1}
$$

Where $d _ { 0 }$ is the reference distance, n is the range decay index, and d is the actual distance between UAV nodes. $G _ { t }$ and $G _ { r }$ indicate the transmitting and receiving antenna gains respectively, and Î» is the wavelength.

Shadow fading is the attenuation of signal power caused by the absorption, reflection, scattering and diffraction of obstacles between transmitter and receiver. Shadow fading is a random variable, so the path loss model can be modified to a lognormal shadow model:

$$
[ P _ { L } ( d ) ] _ { d b } = [ P _ { L } ( d _ { 0 } ) ] _ { d b } + 1 0 n l o g _ { 1 0 } ( d / d _ { 0 } ) ) + X _ { \sigma }\tag{2}
$$

$X _ { \sigma }$ represents a Gaussian random variable with a mean of 0 and a standard deviation of $\sigma .$ . In this model, the receiver at the same distance d from the transmitter has different path losses, which change with the random shadow variable $X _ { \sigma }$

In signal propagation, different propagation delays caused by reflection, scattering and diffraction of electromagnetic wave signals. The signal arriving at the receiver is composed of multipath electromagnetic waves, resulting in fading distortion of the received signal.

Because the Nakagami-m channel model [39] is more consistent with the experimental data than the Rayleigh distribution, and its fading parameters can be adjusted to transform the fading model, and it is widely used in non-line-of-sight multipath fading modeling [24]. The signal strength at the receiver obeys the Nakagami-m distribution:

$$
f ( x ) = \frac { 2 m ^ { m } x ^ { 2 ^ { m - 1 } } } { \Gamma ( m ) \Omega } e x p \frac { m x ^ { 2 } } { \Omega }\tag{3}
$$

Where m presents the fading index, when m is equal to 1, the distribution is the Rayleigh distribution, Î© presents the transmission power, and Î(Â·) represents the gamma function.

Considering the influence of propagation loss and multipath fading, the received signal at the destination node can be expressed as:

$$
p _ { r } = \left[ p _ { t } + 2 0 l o g _ { 1 0 } ( \lambda / 4 \pi d _ { 0 } ) - 1 0 n l o g _ { 1 0 } ( d / d _ { 0 } ) \right] + X _ { \sigma } + | h _ { s d } | ^ { 2 }\tag{4}
$$

Where $X _ { \sigma }$ obeys the Gaussian distribution, and $| h _ { s d } |$ obeys the Nakagami-m distribution.

## IV. EC-CMAC PROTOCOL

In this chapter, we will introduce the EC-CMAC protocol in detail, including the interaction process of frames in the protocol, the estimation function of transmitted power and the relay selection strategy. Since EC-CMAC is proposed on the basis of IEEE802.11DCF [40], the main goal of distributed coordination function (DCF) of IEEE802.11 is to use the interaction between RTS frame and CTS frame to avoid the conflict caused by node contention of the channel. EC-CMAC is also using this interaction strategy to transmit additional necessary information. The interaction process of DCF is as follows: when the source node has a message to send, it first notifies the interface to sense the channel. When it detects that the channel is free, the mechanism activates a back-off counter, which randomly selects an integer from the range (0, CW). When the back-off counter returns to zero, an RTS frame is sent to save the channel. After receiving the RTS frame, the target node responds by sending the CTS frame to the source node. After receiving the CTS frame, the source node sends the data to the target node. After receiving the data, the target node sends an ACK frame to the source node, indicating that the data has been successfully received. Other nodes listening for RTS and CTS frames set their silent duration to wait for the end of the interaction, and this silent state is called the NAV state. This RTS-CTS-DATA-ACK interactive process avoids channel contention and hidden node problems. It needs to be added that during the interaction of frames, if the node does not receive a response within a period of time after sending frames, the re-transmitting mechanism will be started. If a complete interaction is not completed within the limited number of re-transmissions, the data transfer is considered to be failed. This process is shown in Fig. 3.

<!-- image-->  
Fig. 3. IEEE802.11DCF.

<table><tr><td rowspan=1 colspan=1>FrameControl</td><td rowspan=1 colspan=1>Duration</td><td rowspan=1 colspan=1>TransmitterAddress</td><td rowspan=1 colspan=1>ReceiverAddress</td><td rowspan=1 colspan=1>SourceInformation</td><td rowspan=1 colspan=1>FCS</td></tr></table>

Fig. 4. RTS frame.

<table><tr><td rowspan=1 colspan=1>FrameControl</td><td rowspan=1 colspan=1>Duration</td><td rowspan=1 colspan=1>ReceiverAddress</td><td rowspan=1 colspan=1>RelayInformation</td><td rowspan=1 colspan=1>FCS</td></tr></table>

Fig. 5. CTS frame.

## A. Protocol Description

The proposed EC-CMAC protocol modifies RTS and CTS frames on the basis of IEEE802.11DCF. New fields are added in RTS and CTS frames, including node position information as shown in Figs. 4 and 5. A new control frame named BRS is added to the EC-CMAC protocol. The structure of this frame is the same as that of the RTS frame, as shown in Fig. 6. This frame is sent by the winning node in the relay node competition to forward messages from the source node to the destination node.

<table><tr><td rowspan=1 colspan=1>FrameControl</td><td rowspan=1 colspan=1>Duration</td><td rowspan=1 colspan=1>TransmitterAddress</td><td rowspan=1 colspan=1>ReceiverAddress</td><td rowspan=1 colspan=1>RelayInformation</td><td rowspan=1 colspan=1>FCS</td></tr></table>

Fig. 6. BRS frame.

<!-- image-->  
Fig. 7. Protocol frame interaction process.

The optimal relay is the node with more residual energy, less asymmetrical transmission power, and motion direction and position closer to the source node and destination node. Next, we describe the protocol interaction in detail. Fig. 7 shows the EC-CMAC protocol frame interaction timing.

When the source node has the data of length L to send, it will start the back-off counter after detecting that the channel is idle, and the back-off counter is located in the interval [0,CWmin]. When the back-off counter returns to zero, the source node will send RTS frame after DIFS to preserve the channel. Since the RTS frame contains the additional information, the node that overhears the RTS frame can get the location information of the source node as well as the channel gain between the nodes. If the source node does not listen to the CTS frame after waiting for $T _ { R T S } + T _ { C T S } + S I F S .$ it starts the re-transmission effort.

All nodes within the communication range of the source node can listen to the RTS frame and parse it. If the destination node estimates the direct transmission power value through the parameters contained in the RTS frame after receiving the RTS frame, and sends a CTS frame with the estimated direct transmission power value as a response after the SIFS. If a non-destination node within communication range receives the frame, it sets its own silence time according to the Duration field in the RTS frame. Note that in the silent state, nodes still receive messages and they just do not send them.

If the UAV nodes listen to both RTS and CTS frames, these nodes are considered as candidate relay nodes. The candidate relay node and the source node compete for the best relay node by starting the back-off counter. This counter is a function of the direct transmit power, the cooperative transmission power, the residual energy, and the UAV position, as detailed in (12). There are two cases when a node starts the back-off counter:

1) If the back-off counter of the source node ends first, the gain of direct transmission is considered to be greater than that of cooperative transmission. The source node first broadcasts the BRS frame to the nodes within its communication range to inform other candidate nodes. After receiving the frame, other competing nodes update their own NAV time through the âDurationâ field in the BRS frame, and then the source node sends the message to the destination node with fixed power.

2) If the back-off counter of the candidate relay node ends first, the winning relay node sends a BRS frame containing the information of the relay node after the counter ends. Other candidate relay nodes end the current contention back-off process after overhearing the frame and update their own NAV time according to the duration field in the BRS frame. After receiving the frame, the source node initiates cooperative transmission and sends the message to the relay node.

If the source node does not receive the BRS frame after $T _ { b a c k o f f } + T _ { B R S } + S I F S$ , it is considered that the optimal cooperative relay in relay selection fail in transmitting the BRS frame to the source node due to mobility and other reasons, in which case the source node directly transmits data to the destination node through fixed power.

Whether in the direct transmission or cooperative transmission mode, if the destination node successfully receives the data and resolves the destination node to this data as itself, the destination node sends ACK to the source node by parsing the source node information in the frame to indicate successful transmission. There are two cases:

1) If the source node does not receive an ACK in $T _ { A C K } +$ $8 \times ( L + L _ { H } ) / R$ , it is deemed that the ACK has timed out, and the node selects a new timer and starts random back-off to wait for the next channel idle.

2) If the source node receives ACK, it considers that the transmission of a message is successful. If there are other data in the message buffer of the source node, it randomly selects the back- off time from [0,CW] again and starts the next transmission process.

It is important to note that the competing nodes must listen to both RTS and CTS frames before setting their NAV values based on the contention. The Duration field of CTS frames is $D _ { C T S } = T _ { A C K } + 8 \times ( L + L _ { H } ) / R _ { S R } +$ $8 { \times } ( L + L _ { H } ) / R _ { R D } + 3 S I F S$

As mentioned earlier, after a candidate relay node fail in competing, it receives a BRS frame from the best relay and then sets its NAV value, that ${ \mathrm { i s } } ,$ the persistence field of the BRS frame is $D _ { B R S } = 8 \times ( L + L _ { H } ) / R _ { S R } + 8 \times ( L +$ $L _ { H } ) / R _ { R D } + 2 S I F S$

The improved protocol interaction process is shown in Fig. 8. And the algorithm flow of EC-CMAC is shown in Algorithm 1.

## B. Transmission Power Estimation

Assume that there is a source node and a destination node, and the source node sends data to the destination, then the signal received on the target node is:

$$
y _ { d } = \sqrt { P _ { S } d _ { s d } ^ { \alpha } A _ { s d } } h _ { s d } x + n\tag{5}
$$

<!-- image-->  
Fig. 8. Motion direction from the candidate relay nodes to the source and destination nodes.

Here, $P _ { S }$ is the transmit power of the source node, $d _ { s d }$ is the distance between source and destination and Î± is path loss exponent. $A _ { s d }$ is shadow fading, and $h _ { s d }$ is the channel fading gain and n is the noise.

In wireless networks, link outage often occurs, and it is generally considered that the SNR of the received signal is less than the SNR threshold. The receiver SNR is expressed as:

$$
\gamma _ { d } = \frac { p _ { r } } { N _ { 0 } }\tag{6}
$$

Where $\gamma _ { d }$ represents the received SNR of the destination node terminal, $p _ { r }$ represents the received power, and $N _ { 0 }$ represents the noise power.

The multipath fading channel between the source and destination nodes is modeled as a Nakagami-m channel, and the channel coefficient $| h _ { s d } |$ is subject to the Nakagami-m distribution. As shown in (3). If $| h _ { s d } |$ is subject to Nakagami-m distribution, the channel gain $| h _ { s d } | ^ { 2 }$ distribution function is:

$$
f _ { | h _ { s d } | ^ { 2 } ( x ) } = \frac { m ^ { m } x ^ { m - 1 } } { \Gamma ( m ) \Omega } e x p ^ { \frac { m x } { \Omega } }\tag{7}
$$

Then the received signal shall meet the requirements of:

$$
\gamma _ { d } = \frac { p _ { t } A | h _ { s d } | ^ { 2 } d _ { s d } ^ { \alpha } } { N _ { 0 } } > \gamma _ { t h }\tag{8}
$$

Where $\gamma _ { t h }$ is the SNR threshold.

## C. Relay Selection Back-Off Function

The purpose of relay selection is to reduce the overall energy consumption of the network and extend the lifetime of the network by selecting appropriate one-hop relays to forward messages. The selection of relay is mainly considered from the following aspects: (1) the remaining energy of the node; (2) the estimated transmitting power of the node; (3) the relative position of the node; (4) the direction of motion of the node.

It is assumed that all UAV nodes in the communication range have their own moving direction and fixed speed, as shown in Fig. 8. All candidate relay nodes calculate the angles between themselves and the source node and the destination node respectively, and calculate the best moving direction according to the angles.

Then the position of UAV after time $T$ is:

$$
\left\{ \begin{array} { l l } { L _ { ( } x ) ^ { * } = L _ { ( } x ) + V _ { x } T } \\ { L _ { ( } y ) ^ { * } = L _ { ( } y ) + V _ { y } T } \end{array} \right.\tag{9}
$$

Here, $L _ { ( } x )$ and $L _ { ( \mathcal { Y } ) }$ represent the horizontal and vertical coordinates of the current node position, and $L _ { ( } x ) ^ { * }$ and $L _ { ( } x ) ^ { * }$ represent the horizontal and vertical coordinates of the estimated position of the node. $V _ { x }$ and $V _ { y }$ are the directional speed of the node, and $T$ is the expected flight time.

Then the angle $D _ { U 1 ^ { * } U 2 ^ { * } ( 0 , 2 \pi ) }$ between UAV U1 and UAV U2 is:

$$
\begin{array} { r }  D _ { U 1 ^ { * } U 2 ^ { * } ( 0 , 2 \pi ) } = \{ \begin{array} { l l } { \tan \big ( \frac { L _ { U 1 ( y ) } ^ { \varepsilon } - L _ { U 2 ( y ) } ^ { \varepsilon } } { L _ { U 1 ( z ) } ^ { \varepsilon } - L _ { U 2 ( z ) } ^ { \varepsilon } } \big ) , } \\ { L _ { U 1 ( y ) } ^ { \varepsilon } > L _ { U 2 ( y ) } ^ { \varepsilon } , L _ { U 1 ( y ) } ^ { \varepsilon } > L _ { U 1 ( y ) } ^ { * } > L _ { U 1 ( y ) } ^ { * } } \\ { \pi - \tan \big ( \frac { L _ { U 1 ( y ) } ^ { \varepsilon } - L _ { U 2 ( y ) } ^ { \varepsilon } } { L _ { U 1 ( z ) } ^ { \varepsilon } - L _ { U 2 ( z ) } ^ { \varepsilon } } \big ) , } \\ { L _ { U 1 ( y ) } ^ { \varepsilon } > L _ { U 2 ( y ) } ^ { \varepsilon } , L _ { U 1 ( y ) } ^ { \varepsilon } < L _ { U 1 ( y ) } ^ { * } } \\ { \pi + \tan \big ( \frac { L _ { U 1 ( y ) } ^ { \varepsilon } - L _ { U 2 ( y ) } ^ { \varepsilon } } { L _ { U 1 ( x ) } ^ { \varepsilon } - L _ { U 2 ( z ) } ^ { \varepsilon } } \big ) , } \\ { L _ { U 1 ( y ) } ^ { \varepsilon } < L _ { U 2 ( y ) } ^ { \varepsilon } , L _ { U 1 ( y ) } ^ { \varepsilon } < L _ { U 1 ( y ) } ^ { * } } \\ { 2 \pi - \tan \big ( \frac { L _ { U 1 ( y ) } ^ { \varepsilon } - L _ { U 2 ( x ) } ^ { \varepsilon } } { L _ { U 1 ( z ) } ^ { \varepsilon } - L _ { U 2 ( x ) } ^ { \varepsilon } } \big ) , } \\ { L _ { U 1 ( y ) } ^ { \varepsilon } < L _ { U 2 ( y ) } ^ { \varepsilon } , L _ { U 1 ( y ) } ^ { \varepsilon } > L _ { U 1 ( y ) } ^ { * } } \\  L _ { U 1 ( y ) } ^ { \varepsilon } < L _ { U 2 ( y ) } ^ { \varepsilon } , L _ { U 1 ( y ) } ^ { \varepsilon } > \end{array} \end{array}\tag{10}
$$

Then the best motion direction of node $U _ { R }$ relative to source node $U _ { S }$ and destination node $U _ { D }$ is:

$$
D _ { R } ^ { b e s t } = \left\{ \begin{array} { l l } { \operatorname* { m i n } ( D _ { U _ { R } * U _ { S } * } , D _ { U _ { R } * U _ { D } * } ) + | D _ { U _ { R } * U _ { S } * } , - D _ { U _ { R } * U _ { D } * } | , } & \\ { | D _ { U _ { R } * U _ { S } * } , - D _ { U _ { R } * U _ { D } * } | < \pi } & \\ { \frac { \operatorname* { m i n } ( D _ { U _ { R } * U _ { S } * } , D _ { U _ { R } * U _ { D } * } ) + ( 2 \pi - | D _ { U _ { R } * U _ { S } * } , - D _ { U _ { R } * U _ { D } * } | ) } { 2 } , } & \\ { | D _ { U _ { R } * U _ { S } * } , - D _ { U _ { R } * U _ { D } * } | > \pi } & \end{array} \right.\tag{11}
$$

The relay selection back-off function in this paper is as follows:

$$
\begin{array} { r l } & { B U _ { r } = } \\ & { t _ { s } \left( \alpha \frac { E _ { 0 } } { E _ { r n } - E _ { r n } ^ { * } } + \beta \frac { P _ { R } ^ { C } + P _ { S } ^ { C } } { P _ { S } ^ { D } } + \gamma \frac { E _ { S } } { E _ { r n } } + \delta \frac { D _ { R } ^ { b e s t } - D _ { R } } { D i s _ { R , S D } } \right) . } \end{array}\tag{12}
$$

Where $t _ { s }$ is the time parameter to weigh the overall back-off time length; $E _ { 0 }$ is the initial energy of the UAV, $E _ { r n }$ is the current residual energy of the UAV, $P _ { R } ^ { \breve { C } }$ is the relay and forwarding power of the cooperative mode, $\mathbf { \partial } _ { P _ { S } ^ { C } }$ is the transmission power of the source node in the cooperative mode, and $P _ { S } ^ { D }$ is the transmission power of the source node in the direct transmission mode. $E _ { S }$ is the remaining energy at the source node, and $D _ { R } ^ { b e s t }$ is the best motion direction of the candidate relay node relative to the source node and the destination node. $D i s _ { R , S D }$ is the minimum distance between the candidate relay node and the communication link between the source and destination. $\alpha , \beta , \gamma , \delta$ are the weight coefficients respectively, in order to control the influence of each term on the specific gravity of the function.

For item $\frac { E _ { 0 } } { E _ { r n } - E _ { r n } ^ { * } }$ , since all UAVs have the same initial energy, the node with less energy remaining after message transmission has a smaller value. For item $\frac { P _ { R } ^ { C } + P _ { S } ^ { C } } { P _ { S } ^ { D } }$ , the direct transmission power $P _ { S } ^ { D }$ is fixed, so the node with the smaller cooperative transmission power has the smaller item. In the transmitting process, there is less residual energy of the source node, and the direct transmission energy consumption is low, but the collaborative transmitting power is high. Therefore, $\frac { E _ { S } } { E _ { r n } }$ considers the energy ratio between the source node and the candidate relay node, when the residual energy of the source node is too small, candidate relay nodes with more residual energy are more likely to participate in the collaborative transmitting process. Item $\frac { \bar { D } _ { R } ^ { b e s t } - D _ { R } } { D i s _ { R , S D } }$ fully considers the movement direction and position of nodes.

Algorithm 1: EC-CMAC Protocol.   
PROCEDURE RT SF rameReceived(RT S)   
if(RT S.receiveraddress == this.address)then   
transmit CT S   
else set NAV (RT S)   
endif   
END PROCEDURE   
PROCEDURE CT SF rameReceived(CT S)   
if(CT S.receiveraddress == this.address)then   
utility_based_backoff start af ter   
CT S.length/datarate   
else set NAV (CT S)   
endif   
if(utility_based_backoff == 0)then   
transmit BRS   
endif   
END PROCEDURE   
PROCEDURE RT SandCT SF rameBothReceived   
compute transmit power   
utility_based_backoff start   
if(utility_based_backoff == 0)then   
transmit BRS   
endif   
END PROCEDURE   
PROCEDURE BRSF rameReceived(BRS)   
if(BRS.receiveraddress == this.address)then   
transmit DAT A   
else set NAV (BRS)   
endif   
END PROCEDURE   
PROCEDURE DAT AF rameReceived(DAT A)   
if(DAT A.receiveraddress == this.address)   
retransmit DAT A   
elseif(DAT A.receiveraddress == this.address)   
then transmit ACK   
endif   
END PROCEDURE

## V. SIMULATION EXPERIMENT

In this chapter, we compare EC-MAC with IEEE802.11DCF, LC-MAC and DEL-CMAC in multiple index, and simulate the proposed protocol in MATLAB-2021R-2021a. We evaluate the following performance using dynamic and static simulation environments in single-hop and multi-hop networks, respectively:(1) packet deliver ratio, the ratio between the number of received packets and the number of packets expected to be received, (2) network lifetime, the time it takes for the nodes in the network to run out of energy, (3) end-to-end delay, the time taken for data to be transmitted from the source node to the destination node where it is successfully received, (4) network throughput, the actual amount of data that passes through the network per unit time.

<!-- image-->  
Fig. 9. Signal loss varies with the distance.

TABLE I  
SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>RTSFrame</td><td rowspan=1 colspan=1>24Bytes</td><td rowspan=1 colspan=1>FixedTransmitPower</td><td rowspan=1 colspan=1>26dbm</td></tr><tr><td rowspan=1 colspan=1>CTS Frame</td><td rowspan=1 colspan=1>18Bytes</td><td rowspan=1 colspan=1>Initial Energy Eo</td><td rowspan=1 colspan=1>10000J</td></tr><tr><td rowspan=1 colspan=1>ACK Frame</td><td rowspan=1 colspan=1>14Bytes</td><td rowspan=1 colspan=1>Receive Power</td><td rowspan=1 colspan=1>1dbm</td></tr><tr><td rowspan=1 colspan=1>PHY Header</td><td rowspan=1 colspan=1>24Bytes</td><td rowspan=1 colspan=1>Handle Power</td><td rowspan=1 colspan=1>5dbm</td></tr><tr><td rowspan=1 colspan=1>MAC Header</td><td rowspan=1 colspan=1>34Bytes</td><td rowspan=1 colspan=1>Noise Power</td><td rowspan=1 colspan=1>-80dbm</td></tr><tr><td rowspan=1 colspan=1>Basic Data Rate</td><td rowspan=1 colspan=1>1Mbps</td><td rowspan=1 colspan=1>Time Standard</td><td rowspan=1 colspan=1>0.1ms</td></tr><tr><td rowspan=1 colspan=1>UAVFlight Power</td><td rowspan=1 colspan=1>10W</td><td rowspan=1 colspan=1>UAVHover Power</td><td rowspan=1 colspan=1>5W</td></tr></table>

During the simulation, the nodes are distributed in a circular area with a diameter of 2 km, as shown in Fig. 9. Nodes in a multi-hop network are all covered within the communication range of at least one other node. The source and destination nodes are randomly selected, and the data is sent from the source node. The physical layer adopted the 802.11b standard and used the adaptive rate mode of 1:2:5:10. The parameter settings of simulation are shown in Table I.

We first test the signal loss under the channel model, as shown in Fig. 10. In (1), both the transmitting antenna gain and the receiving antenna gain are 1, the reference distance is 100 m, and the range attenuation index is set to 4 to simulate the harsh propagation environment. In (2), the standard deviation a of shadow fading after Gaussian distribution is 3. The fading parameter m in (3) is 3.

<!-- image-->  
Fig. 10. Initialization of the node.

<!-- image-->  
Fig. 11. Network lifetime of the single-hop network changes with the increasing number of nodes(dynamic environment).

## A. Single-Hop Network

The experiment on single-hop network can reflect the influence of node density within EC-CMAC algorithm in the same subnet. The nodes are patrolling in the area at a node speed of 1 m/s. The number of nodes is continuously increased from 10 to 60 to simulate different network densities. The experimental results are shown in Fig. 11, and the results show that in singlehop networks, EC-CMAC only slightly improves the network lifetime compared to the other three protocols because of the short distance between nodes in single-hop networks. The additional control frame overhead required by EC-CMAC offsets the energy savings from optimal relay selection. It is worth noting that EC-CMAC has a certain optimization effect in terms of network lifetime because the relay selection process of LC-MAC involves intra-group competition and inter-group competition, and the additional control frame overhead of DEL-CMAC is larger than that of EC-CMAC.

<!-- image-->  
Fig. 12. Packet delivery ratio of the single-hop network changes with the increasing number of nodes(dynamic environment).

The experimental results show that with the increasing number of network nodes, the density of regional nodes and the network lifetime both increases, as shown in Fig. 11. This is because in the case of low node density, nodes are selected as relay nodes more frequently, and multiple message forwarding by relay nodes consumes more energy. In high-density nodes, the number of message forwarding is less, so the overall network lifetime is longer, and the unit energy consumption is lower. IEEE802.11DCF uses fixed transmission power, high energy consumption and short network lifetime. DEL-CMAC uses a power threshold to judge direct or collaborative transmission regardless of the remaining energy of the source node and the location of the node, therefore, the probability of cooperative transmission is low, and the source node consumes a lot of energy. In LC-MAC, the link utility only considers the energy consumption and does not consider the residual energy of the node.

Finally, we test the packet delivery ratio in a single-hop network, as shown in Fig. 12. It can be seen from the experimental results that the four protocols maintain a high packet delivery ratio, which is because in the single-hop network, the packet delivery ratio is mainly affected by signal attenuation, and the movement of nodes has nearly no influence on it. EC-CMAC is always superior to the other three protocols, because EC-CMAC not only considers signal attenuation to allocate transmission power, but also pays extra attention to the energy of the source node, guarantee transmission reliability.

## B. Muti-Hop Network

Then the network performance of the four protocols is tested in a multi-hop environment. First, the network lifetime of nodes in static environment as shown in Fig. 13. Since nodes have no moving speed and direction, EC-CMAC cannot guarantee better selection in the process of relay selection to save node energy. Therefore, the network lifetime of EC-CMAC is only slightly optimized about 100 seconds when the number of nodes is 60, this is because the frame interaction process of relay selection is simpler compared to DEL-CMAC and LC-MAC, and the residual energy of the source node is considered during relay selection.

<!-- image-->  
Fig. 13. Network lifetime of the multi-hop network changes with the increasing number of nodes(static environment).

<!-- image-->  
Fig. 14. Network lifetime of the multi-hop network changes with the increasing number of nodes(dynamic environment).

The network lifetime of a multi-hop network in a dynamic environment is shown in Fig. 14. In multi-hop networks, the network lifetime increases compared to single-hop networks because of the impact of communication range on competing relay nodes. And as the node moves, the location of the node changes frequently, which affects the selection of the relay node. Experimental results show that EC-CMAC outperforms DEL-CMAC, LC-MAC and DCF in terms of network lifetime. This is because EC-CMAC considers the movement of nodes and the residual energy of source nodes as well as the movement direction and position of nodes during cooperative transmission. When the number of nodes is 60, the average network lifetime of EC-CMAC is about 1.2 times that of DEL-CMAC and LC-MAC, which is 300 s longer than that of DCF.

<!-- image-->  
Fig. 15. Network throughput of the multi-hop network changes with the increasing number of nodes(dynamic environment).

<!-- image-->  
Fig. 16. End-to-end delay of the multi-hop network changes with the increasing number of nodes(dynamic environment).

Fig. 15 shows the network throughput in the multi-hop network. It can be clearly seen that although EC-CMAC adds additional control frames, the network throughput only decreases a little compared with that of DCF because of the consideration of the movement direction and position of nodes. Compared with EC-CMAC, DEL-CMAC and LC-MAC have higher overhead, which is because these two protocols do not consider the case of link interruption, and leads to low throughput.

The experimental results of the end-to-end delay are shown in Fig. 16. It can be seen from the results that the end-to-end delay of EC-CMAC, LC-MAC and DEL-CMAC is higher than that of DCF. This is because these three protocols all need additional control frames, which leads to a small decrease in delay compared with that of DCF, but the range is acceptable. It is worth noting that EC-CMAC has less additional control overhead than that of DEL-CMAC and does not have as complex interaction process as that of LC-MAC, so it has lower delay.

<!-- image-->  
Fig. 17. Packet delivery ratio of the multi-hop network changes with the increasing number of nodes(dynamic environment).

<!-- image-->  
Fig. 18. End-to-end delay of the multi-hop network changes with the increasing speed of nodes.

Subsequently, we compare the packet delivery ratio of the four protocols, as shown in Fig. 17. The experimental results show that EC-CMAC can better solve the packet loss problem caused by mobility and has higher PDR when considering the direction and position of node movement. However, this difference is not particularly obvious because the node speed is too small. When the UAV speed is 1 m/s, EC-CMAC only improves the PDR by about 5% with respect to the other three protocols.

Finally, we test the performance of the four protocols at different speeds, in which the number of nodes are set to 30, considering the maximum flight speed of small UAVs, the range of speed is set from 1 m/s to 19 m/s to simulate the flight of UAVs within different tasks. The experimental results are shown in Figs. 18 and 19. The changes of network throughput and latency with speed are shown in the figures. It can be seen from the results that the performance of the four protocols decreases with the increasing speed of the nodes moving. This is because in the process of transmission, as the node speed increases, the node moves out of the effective communication range and the target node gradually moves away from the source node, the signal attenuation degree continues to increase. Since EC-CMAC considers the position and movement direction of nodes in the relay selection process, the difference of delay and throughput between EC-CMAC and DCF decreases as the speed increases. The delay and throughput of EC-CMAC are better than that of DCF when the node moving speed exceeds 12.5 m/s (45 km/h) and 11.5 m/s (41.4 km/h), respectively.

<!-- image-->  
Fig. 19. Network throughput of the multi-hop network changes with the increasing speed of nodes.

<!-- image-->  
Fig. 20. Packet delivery ratio of the multi-hop network changes with the increasing speed of nodes.

Next, we test the packet delivery ratio of the four protocols within different mobility speeds, as shown in Fig. 20. The results show that with the increasing speed of node moving, the packet delivery rate gradually decreases, and the optimization effect of EC-CMAC is more and more obvious. When the mobile speed reaches 19 m/s, the packet delivery rate of EC-CMAC is 16.44%, 14.86% and 6.5% higher than that of DCF, LC-MAC and DEL-CMAC, respectively.

## VI. CONCLUSION

In FANET, when the transmission environment is harsh, signal attenuation and high speed movement of nodes cause link interruption. At the same time, the fixed transmitting power shorten the network lifetime. This paper proposes an improved cooperative MAC protocol EC-CMAC, in which an appropriate relay selection strategy can effectively improve the above problems. First, the propagation model of N-LOS channel in harsh environment is proposed, and then the transmitting power is estimated from the signal strength. In the process of message transmission, the transmission mode is adaptively selected according to the estimated transmitting power, the residual energy of the node and the position of the node. The cooperative transmission mode is used to forward the message through the one-hop relay. EC-CMAC protocol is verified in MATLAB and compared with IEEE802.11DCF, LC-MAC and DEL-CMAC. The experimental results show that EC-CMAC can effectively prolong the network lifetime, with small delay increase and throughput degradation. In addition, EC-CMAC can maintain high packet delivery ratio at high speed. The work of this paper is mainly applied to emergency communication scenarios, so the flight height difference of all UAVs can be ignored. However, in heterogeneous UAV clusters, different types of UAVs need to perform different jobs. For example, in the environment of simultaneous emergency communication and post-disaster search and rescue, UAVs usually leave the high altitude to perform tasks in low altitude areas. At this point, it is necessary to consider the communication situation of outlying UAVs to guarantee the overall communication stability. In addition, the MAC protocol proposed in this paper is based on the premise that the network routing path has been established, and different routing table update frequency has an impact on the execution efficiency of the MAC protocol. At present, we have been committed to carrying out the study on cross-layer network protocol, and we will combine cross-layer routing protocol with heterogeneous UAV swarm communication in the future, and build a complete UAV communication system.

## REFERENCES

[1] O. M. Bushnaq, A. Chaaban, and T. Y. Al-Naffouri, âThe role of UAV-IoT networks in future wildfire detection,â IEEE Internet Things J., vol. 8, no. 23, pp. 16984â16999, Dec. 2021.

[2] M. Y. Arafat and S. Moh, âBio-inspired approaches for energy-efficient localization and clustering in UAV networks for monitoring wildfires in remote areas,â IEEE Access, vol. 9, pp. 18649â18669, 2021.

[3] S. Yan, M. Peng, and X. Cao, âA game theory approach for joint access selection and re-source allocation in UAV assisted IoT communication networks,â IEEE Internet Things J., vol. 6, no. 2, pp. 1663â1674, Apr. 2019.

[4] M. Huang, A. Liu, N. N. Xiong, and J. Wu, âA UAV-Assisted ubiquitous trust communication system in 5G and BeyondNetworks,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3444â3458, Nov. 2021.

[5] N. Zhao et al., âUAV-Assisted emergency networks in disasters,â IEEE Wireless Commun., vol. 26, no. 1, pp. 45â51, Feb. 2019.

[6] D. Erdos, A. Erdos, and S. E. Watkins, âAn experimental UAV system for search and rescue challenge,â IEEE Aerosp. Electron. Syst. Mag., vol. 28, no. 5, pp. 32â37, May 2013.

[7] R. R. Pitre, X. R. Li, and R. Delbalzo, âUAV route planning for joint search and track missionsâAn information-value approach,â IEEE Trans. Aerosp. Electron. Syst., vol. 48, no. 3, pp. 2551â2565, Jul. 2012.

[8] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surveys Tut., vol. 21, no. 3, pp. 2334â2360, Third Quarter 2019.

[9] M. Adil et al., âEnhanced-AODV: A robust three phase priority-based traffic load balancing scheme for Internet of Things,â IEEE Internet Things J., vol. 9, no. 16, pp. 14426â14437, Aug. 2022.

[10] J. Toutouh, J. Garcia-Nieto, and E. Alba, âIntelligent OLSR routing protocol optimization for VANETs,â IEEE Trans. Veh. Technol., vol. 61, no. 4, pp. 1881â1894, May 2012.

[11] C. Cai, J. Fu, H. Qiu, and Y. Lu, âAn active idle timeslot transfer TDMA for flying ad-hoc networks,â in Proc. IEEE 20th Int. Conf. Commun. Technol., 2020, pp. 746â751.

[12] X. Huang, A. Liu, H. Zhou, K. Yu, W. Wang, and X. Shen, âFMAC: A self-adaptive MAC protocol for flocking of flying ad hoc network,â IEEE Internet of Things J., vol. 8, no. 1, pp. 610â625, Jan. 2021.

[13] H. Zhao and A. Du, âA self-adaptive back-off optimization scheme based on beacons probability prediction for vehicle ad-hoc networks,â China Commun., vol. 13, no. 12, pp. 132â138, Dec. 2016.

[14] I. Rhee, A. Warrier, M. Aia, J. Min, and M. L. Sichitiu, âZ-MAC: A hybrid MAC for wireless sensor networks,â IEEE/ACM Trans. Netw., vol. 16, no. 3, pp. 511â524, Jun. 2008.

[15] K.-C. Huang, X. Jing, and D. Raychaudhuri, âMAC protocol adaptation in cognitive radio networks: An experimental study,â in Proc. 18th Int. Conf. Comput. Commun. Netw., 2009, pp. 1â6.

[16] B. Shrestha, E. Hossain, and K. W. Choi, âDistributed and centralized hybrid CSMA/CA-TDMA schemes for single-hop wireless networks,â IEEE Trans. Wireless Commun., vol. 13, no. 7, pp. 4050â4065, Jul. 2014.

[17] Z. Liu and I. Elhanany, âRL-MAC: A reinforcement learning based MAC protocol for wireless sensor networks,â Int. J. Sensor Netw., vol. 1, no. 3/4, pp. 117â124, 2006.

[18] Z. Zheng, A. K. Sangaiah, and T. Wang, âAdaptive communication protocols in flying ad hoc network,â IEEE Commun. Mag., vol. 56, no. 1, pp. 136â142, Jan. 2018.

[19] M. Zhang, C. Dong, and Y. Huang, âFS-MAC: An adaptive MAC protocol with fault-tolerant synchronous switching for FANETs,â IEEE Access, vol. 7, pp. 80602â80613, 2019.

[20] T. Xie, H. Zhao, J. Xiong, and N. I. Sarkar, âA multi-channel MAC protocol with retrodirective array antennas in flying ad hoc networks,â IEEE Trans. Veh. Technol., vol. 70, no. 2, pp. 1606â1617, Feb. 2021.

[21] B. Zheng, Y. Li, W. Cheng, and W. Zhao, âA multi-channel load awarenessbased MAC protocol for flying ad hoc networks,â in Proc. IEEE 19th Int. Conf. Commun. Technol., 2019, pp. 379â384.

[22] F. de Daran, V. Vigneras-Lefebvre, and J. P. Parneix, âModeling of electromagnetic waves scattered by a system of spherical particles,â IEEE Trans. Magn., vol. 31, no. 3, pp. 1598â1601, May 1995.

[23] D. Alkama and M. A. Ouamri, âDownlink performance analysis in MIMO UAV-Cellular communication with LOS/NLOS propagation under 3D beamforming,â IEEE Access, vol. 10, pp. 6650â6659, 2022.

[24] B. Ji, Y. Li, S. Chen, C. Han, C. Li, and H. Wen, âSecrecy outage analysis of UAV assisted relay and antenna selection for cognitive network under Nakagami- m channel,â IEEE Trans. Cogn. Commun. Netw., vol. 6, no. 3, pp. 904â914, Sep. 2020.

[25] W. Zhuang and M. Ismail, âCooperation in wireless communication networks,â IEEE Wireless Commun., vol. 19, no. 2, pp. 10â20, Apr. 2012.

[26] J.-K. Lee, H.-J. Noh, and J. Lim, âTDMA-based cooperative MAC protocol for multi-hop relaying networks,â IEEE Commun. Lett., vol. 18, no. 3, pp. 435â438, Mar. 2014.

[27] Z. Tianjiao and Z. Qi, âGame-based TDMA MAC protocol for vehicular network,â J. Commun. Netw., vol. 19, no. 3, pp. 209â217, Jun. 2017.

[28] Q. Ye and W. Zhuang, âToken-based adaptive MAC for a two-hop Internetof-Things enabled MANET,â IEEE Internet Things J., vol. 4, no. 5, pp. 1739â1753, Oct. 2017.

[29] H. Zhu and G. Cao, ârDCF: A relay-enabled medium access control protocol for wireless ad hoc networks,â IEEE Trans. Mobile Comput., vol. 5, no. 9, pp. 1201â1214, Sep. 2006.

[30] P. Liu, Z. Tao, S. Narayanan, T. Korakis, and S. S. Panwar, âCoopMAC: A cooperativeMAC for wireless LANs,â IEEE J. Sel. Areas Commun., vol. 25, no. 2, pp. 340â354, Feb. 2007.

[31] S. Bharati and W. Zhuang, âCAH-MAC: Cooperative ADHOC MAC for vehicular networks,â IEEE J. Sel. Areas Commun., vol. 31, no. 9, pp. 470â479, Sep. 2013.

[32] J.-K. Lee, H.-J. Noh, and J. Lim, âDynamic cooperative retransmission scheme for TDMA systems,â IEEE Commun. Lett., vol. 16, no. 12, pp. 2000â2003, Dec. 2012.

[33] T. Guo and R. Carrasco, âCRBAR: Cooperative relay-based auto rate MAC for multirate wireless net-works,â IEEE Trans. Wireless Commun., vol. 8, no. 12, pp. 5938â5947, Dec. 2009.

[34] Y. Zhou, J. Liu, L. Zheng, C. Zhai, and H. Chen, âLink-utility-based cooperative MAC protocol for wireless multi-hop networks,â IEEE Trans. Wireless Commun., vol. 10, no. 3, pp. 995â1005, Mar. 2011.

[35] T. Zhou, H. Sharif, M. Hempel, P. Mahasukhon, W. Wang, and T. Ma, âA novel adaptive distributed cooperative relaying MAC protocol for vehicular networks,â IEEE J. Sel. Areas Commun., vol. 29, no. 1, pp. 72â82, Jan. 2011.

[36] X. Wang and J. Li, âImproving the network lifetime of MANETs through cooperative MAC protocol design,â IEEE Trans. Parallel Distrib. Syst., vol. 26, no. 4, pp. 1010â1020, Apr. 2015.

[37] D. O. Akande and M. F. Mohd Salle, âA network lifetime extension-aware cooperative MAC protocol for MANETs with optimized power control,â IEEE Access, vol. 7, pp. 18546â18557, 2019.

[38] X. Chen and X. Hu, âChannel modeling and performance analysis for UAV relay systems,â China Commun., vol. 15, no. 12, pp. 89â97, Dec. 2018.

[39] B. Dulek, N. D. Vanli, S. Gezici, and P. K. Varshney, âOptimum power randomization for the minimization of outage probability,â IEEE Trans. Wireless Commun., vol. 12, no. 9, pp. 4627â1637, Sep. 2013.

[40] IEEE Standard for Information Technology Telecommunications and Information Exchange Between Systems Local and Metropolitan Area NetworksâSpecific Requirements Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications, IEEE Standard 802.11â2007.

<!-- image-->  
Jiehong Wu (Member, IEEE) received the PhD degree in computer architecture from Northeastern University, in 2008. She was sponsored by Chinese Government as a visiting scholar with Wright State University, Dayton, OH, USA, in 2011. She is currently a professor and a doctoral supervisor with Shenyang Aerospace University, China. Her main research interests include UAV/AUV/UUV systemâs correspondence security, cluster control, path planning, and intelligent decision.

<!-- image-->

Jianzhou Zhou received the bachelorâs degree in network engineering from the Liaoning University of Science and Technology, in 2018. He is currently working toward the masterâs degree with Shenyang Aerospace University. His research interests include clustering network algorithms for unmanned aerial vehicles.

<!-- image-->

Lei Yu is an associate professor and visiting scholar with West Oregon University, America (2015) works as an English teacher in foreign language school in Shenyang Aerospace University, China. Her main research fields include English education and educational administration.

<!-- image-->

Lijun Gao received the PhD degree in computer science from Tianjin University, in 2015. Currently, he is a professor with Shenyang Aerospace University. He has extensive research interests including information security and artificial intelligence confrontation, etc.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_3_img_1.jpeg|page_3_img_1]]
3. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_5_img_1.jpeg|page_5_img_1]]
4. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_5_img_2.jpeg|page_5_img_2]]
5. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_5_img_3.jpeg|page_5_img_3]]
6. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_5_img_4.jpeg|page_5_img_4]]
7. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_5_img_5.jpeg|page_5_img_5]]
8. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_6_img_1.jpeg|page_6_img_1]]
9. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_8_img_1.jpeg|page_8_img_1]]
10. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_8_img_2.jpeg|page_8_img_2]]
11. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_8_img_3.jpeg|page_8_img_3]]
12. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_9_img_1.jpeg|page_9_img_1]]
13. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_9_img_2.jpeg|page_9_img_2]]
14. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_9_img_3.jpeg|page_9_img_3]]
15. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_10_img_1.jpeg|page_10_img_1]]
16. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_10_img_2.jpeg|page_10_img_2]]
17. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_10_img_3.jpeg|page_10_img_3]]
18. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_10_img_4.jpeg|page_10_img_4]]
19. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_11_img_1.jpeg|page_11_img_1]]
20. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_11_img_2.jpeg|page_11_img_2]]
21. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_12_img_1.jpeg|page_12_img_1]]
22. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_12_img_2.jpeg|page_12_img_2]]
23. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_12_img_3.jpeg|page_12_img_3]]
24. [[../extracted_images/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha/page_12_img_4.jpeg|page_12_img_4]]

---

