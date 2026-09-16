# Digital Twin Empowered mmWave Multi-Hop V2X Routing Scheme With UAV Assistance

Taolue Zhou , Xiaohan Wu, and Xinming Zhang , Senior Member, IEEE

AbstractâIn VANETs, millimeter wave (mmWave) is capable of providing ultra-high bandwidth, large data throughput, and very low transmission latency. However, the difficulty of mmWave transmission is further exacerbated by its limited transmission range and its physical properties of low diffraction and low penetration, coupled with real-time dynamic network topology. In future 6G networks, digital twins (DTs) are considered a promising enabling technology as it can provide seamless interaction between the virtual network world and the real world. In this paper, we propose a DT-empowered multi-hop V2X routing scheme using mmWave as the transmission link in urban scenarios. First, we propose a novel DT-assisted mmWave multi-hop relay network architecture, which uses the global traffic flow information possessed by the DTs to assist vehicles in selecting the optimal relay nodes. Second, the uncrewed aerial vehicles (UAVs) are deployed at intersections to improve the packet forwarding efficiency of the intersections. Finally, a reinforcement learning algorithm is used to make forwarding decisions between streets. In addition, we also consider vehicle density and network load as key indicators for optimal street selection. The experimental results indicate that our solution has significant advantages in terms of key indicators such as packet delivery rate and latency.

Index TermsâDigital twin, mmWave, routing, VANETs.

## I. INTRODUCTION

NTELLIGENT Transport Systems (ITS) are rapidly advanc-I ing via Vehicle-to-Everything (V2X) technology, which enables the interconnection of vehicles, road infrastructure, pedestrians, and and other systems. This connectivity enhances road utilization efficiency and driving safety [1]. With V2X, ITS can support critical applications such as those in container ports, future cities, and disaster emergency scenarios [2]. These applications demand ulrta-low-latency, highly reliable communicationâ for example, collision warning messages must be broadcast to surrounding vehicles within 100 millisecondsâwhich poses significant challenges to the existing network architecture.

Digital twins (DTs) are real-time representations of the physical world in the cyber domain [3]. On one hand, DTs can collect real-time data on the physical worldâs state, monitor it, and store critical information [4]. On the other hand, DTs can provide feedback to the physical world [5]. As a key enabler for upcoming 6G networks [3], DTs have been adopted by researchers in fields such as vehicular routing [6], vehicular edge computing [7], [8], and intelligent driving assistance [9]. When adopted, AI algorithms can be implemented on DTs in the cloud, thereby reducing the hardware requirements of physical-world nodes [3]. Furthermore, historical data stored in DTs can be continuously used to retrain modelsâa capability unachievable with conventional methods. Consequently, DTs facilitate more effective intelligentization of vehicle-mounted data transmission.

In vehicular mmWave data transmission, beacons need to be broadcast in the Sub-6 GHz frequency band [10] like Dedicated Short-Range Communications (DSRC), and their performance is constrained by broadcast cycle duration and vehicle density. The seamless interaction between the virtual network domain and the physical world facilitated by DTs enables real-time modeling of vehicles and synchronized data updates, improving adaptability to dynamic topologies and optimizing routing decisions [11]. Additionally, bidirectional synchronization of heterogeneous networks with multi-mode transmission between vehicles and DTs [12] mitigate broadcast storms and other issues arising from sub-6 GHz broadcasting. Moreover, millimeter wave (mmWave) vehicles can leverage DTsâ simulation capabilities to assess beam alignment in DT, thereby minimizing beam-scanning overhead. As a central controller, DTs can optimize global network conditions by rationally allocating resources, increasing parallel mmWave links, and enhancing resource efficiency. Compared to conventional roadside units (RSUs) as central controllers, DTs offer superior support for vehicle mobility and environmental awareness. Furthermore, offloading computational tasks to DTs reduces hardware requirements for physical nodes. Fig. 1 illustrates a scenario diagram of DT-integrated vehicular networks. In summary, the DT-empowered V2X routing advantages in VANETs include:

- Direct Information Access: Vehicles can directly access required information via DT platforms, thereby preventing broadcast-induced issues arising from redundant auxiliary data packets.

C Centralized Optimization: DTs act as centralized controllers to optimize link scheduling, reducing interference and improving resource utilization. Compared with traditional centralized approaches, DTs benefit from end-to-end data synchronization between virtual and physical layers, enabling holistic awareness for superior decision-making.

- AI-Driven Intelligence: AI algorithms deployed on DTs enable intelligent decision-making for physical network nodes. These models are continuously retrained using DT-stored data, ensuring model accuracy. Furthermore, offloading computations to DTs reduces reliance on local node resources, decentralizing computational burdens.

<!-- image-->  
Fig. 1. Digital twins empowered vehicular ad hoc network.

Based on prior discussions, we propose a DT-empowered multi-hop V2X routing scheme using mmWave as the transmission link in urban scenarios. Our scheme is specifically designed for densely populated urban environments, where high vehicle density, frequent mobility, and dynamic network topology pose significant challenges to conventional mmWave-based vehicular communication systems. These scenarios include busy intersections, high-traffic arterial roads, and urban areas with dense traffic congestion, where ultra-low latency and high reliability are required for messive real-time data transmission (e.g., cooperative sensing, emergency communication). The limitations of mmWave (e.g., short transmission range, low penetration) are mitigated through DT-assisted dynamic relay selection and UAV-aided multi-hop forwarding, which are critical in urban settings with line-of-sight (LOS) dominated propagation conditions and frequent blockage caused by buildings or vehicles. The unicast multi-hop routing problem studied in this paper involves cross-street and intra-street relaying, where multi-hop forwarding spans both within a single street segment and between streets, orchestrated as pathfinding from a source intersection to a destination intersection. Streets and intersections in the urban environment are modeled as cloud-based DTs, with vehicles dynamically modeled on their respective DT upon entering these zones. The DT architecture is partitioned into three components: street sub-DTs, intersection sub-DTs, and a Core-DT, deployed across roadside edge servers, intersection edge nodes, and centralized cloud data centers, respectively. These sub-DTs form a Digital Twin Network (DTN), interconnected via ultra-highbandwidth wired backhaul links, enabling seamless cross-tier data synchronization. Nodes within the network utilize mmWave links for packet transmission. Within each street segment, the street sub-DT partitions the street into discrete segments, determining the optimal relay vehicle and beamwidth configuration for each segment to maximize link efficiency.

To enhance cross-intersection packet forwarding efficiency, uncrewed aerial vehicles (UAVs) are deployed at intersections as flexible relay nodes, tasked with receiving packets from vehicles on one street and transmitting them to another. UAVs offer adaptive deployment capabilities, such as dynamically adjusting their positions based on network demands and enabling rapid replacement in case of failures. Contrasted with RSUs, UAVs can hover at elevated altitudes to achieve LoS advantages and broader spatial coverage, while incurring lower deployment costs [13], [14]. For intersections lacking RSU infrastructure or have not yet deployed RSU, UAVs can rapidly bridge coverage gaps. Even in RSU-deployed environments, UAVs complement existing infrastructure by enhancing cross-street forwarding capacity through agile positioning. However, UAVs exhibit operational limitations, including limited endurance, short flight times, and vulnerabilities to weather conditions. This positions UAVs and ground-based RSUs as complementary rather than substitutable components in network architecture. With ongoing advancements in UAV technology and cost reductions, their flight duration and service reliability have improved, aligning with future deployment demands. Considering the UAVâs constrained computational and storage capabilities, reinforcement learning (RL) agents are offloaded to the corresponding intersection sub-DTs for decision optimization, thereby extending UAV operational endurance by reducing onboard processing overhead and leveraging edge-cloud collaboration. The key contributions of this paper are summarized as follows:

We propose a novel hierarchical DT framework that decomposes the DT into three tiers: Street sub-DTs (deployed on edge servers along roadways), Intersection sub-DTs (colocated with edge servers at intersections), and Core DT (hosted in centralized cloud data centers). These sub-DTs synchronize real-time data with VANET-enabled vehicles through VANET access nodes, enabling cross-layer situational awareness for urban traffic networks.

To optimize cross-street packet transmission, we deploy UAVs at intersections as mobile relays and introduce parallel reinforcement learning (RL) agents within intersection sub-DTs. These agents collaboratively: (1) Dynamically adjust UAV positioning based on real-time vehicle density and traffic patterns; (2) Select optimal forwarding paths by balancing end-to-end latency and link reliability; (3) Offload computation to edge servers via DTN-based synchronization, and minimizing onboard resource consumption.

We design an AI-driven decision-making scheme that partitions streets into segments and optimizes cross-intersection transmissions by: (1) Jointly considering node load, average link quality, and transmission distance; (2) Computing optimal beamwidth for both transmitters and receivers to maximize signal-to-interference-plus-noise ratio (SINR); (3) Adapting beamforming patterns in response to dynamic traffic flows and mobility constraints, thereby improving spectral efficiency and packet delivery rate in urban mmWave environments.

The rest of this paper is organized as follows. Section II presents an overview of related work. In Section III, we detail the network model involved in this scheme as well as the mmWave transmission model. In Section IV, we briefly describe the architecture of DTs in this scheme and the process of modeling physical-world entities in DT. Section V describes the mechanism by which vehicles forward packets within streets. Section VI introduces how to forward packets to the appropriate street. Section VII presents simulation settings and results. Finally, we present the conclusion in Section VIII.

## II. RELATED WORK

## A. MMWave

Since the rise of mmWave communication technology, it has gradually been applied to vehicular networks due to its ability to provide ultra-high bandwidth and ultra-low latency. Bahbahani and Alsusa [15] proposed a hybrid protocol combining DSRC and mmWave, which divides multiple vehicles into clusters. The cluster gateway vehicles use DSRC for transmission while mmWave is used for transmission within the cluster. However, ensuring the relative stability of the cluster is a major challenge, and this solution overlooks this point. In addition, this solution can only ensure the transmission rate within the cluster. Ju et al. [16] proposed a mmWave relay selection scheme based on deep reinforcement learning, assuming that in scenarios where RSUs distribute data to vehicles, links may be blocked by buildings. Therefore, the scheme selects suitable relay vehicles to forward data. However, this scheme is only applicable to vehicle-to-infrastructure (V2I) communication. Rasheed et al. [17] considered the difficulties in beam alignment and routing stability in mmWave-based V2X transmission and accordingly proposed a scheme for detecting vehicle positions in 3D scenes for beam selection or alignment. To avoid the overhead caused by beam training, the RSU aligns beams directly based on the vehicleâs position information. Fan et al. [11] proposed a solution to the problem of low signal penetration and susceptibility to obstruction in mmWave V2X. Li et al. [18] proposed a mmWave opportunistic routing scheme that avoids time overhead caused by beam scanning by utilizing location information while considering the distance of candidate forwardersâ to improve transmission distance. Shen et al. [19] proposed a fully distributed mmWave V2V one-hop multicast scheme (OHM), aimed at solving the problem of how vehicles can efficiently discover and communicate with their one-hop neighboring vehicles in highly dynamic scenarios.

## B. Digital Twins

In recent years, a large number of studies have introduced DT into VANETs, as DT can effectively utilize the digital field to develop and test new solutions and AI algorithms. Zhang et al. [7] proposed a DT-assisted vehicle caching cloud based on a social model, using deep learning to calculate the optimal vehicle cache. Zhang et al. [20] proposed a novel vehicle edge computing network based on DT and multi-agent learning, which can improve the cooperation of agents and optimize the efficiency of task offloading. Liu et al. [8] proposed a DT-assisted edge intelligent collaboration scheme that achieves optimal allocation of communication, computing, and caching resources, as well as edge intelligent collaboration. This solution focuses on minimizing response latency to meet the requirements of delay-sensitive applications in IoV. Wang et al. [21] proposed a DT framework for vehicle-to-cloud (V2C) communication in networked vehicles, mainly addressing issues related to advanced driver assistance systems (ADAS) and utilizing DTs to assist drivers in decision-making. This article does not focus on specific network communication but rather on the DTâs scenario modeling and decision-making. Fan et al. [9] proposed a DT-assisted mobile edge computing architecture to help intelligent vehicles change lanes during driving. Zheng et al. [12] first focused on the issue of data synchronization between DTs and vehicles. There are multiple ways for data synchronization between vehicles and DT, and they proposed a learning-based network selection scheme. Zhao et al. [22] proposed a typical application of DT in vehicle networks, which introduces a new network architecture called the Software-Defined Vehicle Network Based on Intelligent DTs (IDT-SDVN). Based on the research in [22], they proposed a hierarchical routing scheme based on the intersections in IDT-SDVN, called the Intelligent Digital Twin Layered (ELITE) routing, to overcome the shortcomings of complex and variable network topologies and diverse service requests.

To sum up, while DTs have been integrated into vehicle networks, resulting in a substantial body of literature, these studies primarily focus on task distribution and offloading in vehicle edge computing. However, research exploring the integration of DTs in the context of mmWave vehicle routing remains limited.

## III. SYSTEM OVERVIEW

## A. Network Model

DT can achieve real-time synchronization, but this paper does not delve into synchronization details, so real-time synchronization is assumed. The accuracy of DT modeling significantly impacts the studyâs outcomes and must align with application requirements. To address this, a suitable model is established based on these requirements. Potential issues such as timeouts, missing data, or errors in control information may degrade the proposed schemeâs performance, necessitating countermeasures to mitigate their effects. For instance, trajectory fitting methods can infer the vehicleâs current position during packet loss, while outlier detection techniques can eliminate anomalies when encountered. Consequently, the essential DTN model is presented as follows:

Fig. 2 depicts an example network model for this paper. In our scenario, streets are interconnected via intersections. DTs are deployed on edge servers and cloud infrastructure, where physical objects are synchronized with the DT system through wireless access points. This ensures real-time reflection of the physical world in the DT system. Multiple edge servers form DTNs via ultra-high-bandwidth wired links. Notably, synchronization between the physical world and DT is a bidirectional process. DT not only mirrors the physical environment in real time but also enables physical entities, such as vehicles, to retrieve necessary information from the DT system. In this work, we assume bidirectional data transmission requirements between any two vehicles in the network (e.g., between two autonomous vehicles). As illustrated in Fig. 2, a source vehicle $v _ { s }$ generates a data packet and transmits it along the street toward the destination vehicle $v _ { d } .$ . When the packet reaches a street segment, the vehicle carrying it selects the optimal next-hop vehicle for transmission, leveraging real-time synchronization with the DT. Upon reaching UAV at the intersection, the DT identifies the best target street, directs the packet to vehicles on that street, and iteratively repeats this routing process until the packet is delivered to $v _ { d }$

<!-- image-->  
Fig. 2. Overview of multi-hop V2X scenarios assisted by DTs.

## B. Antenna Pattern

Vehicles and UAVs employ multiple directional antenna beams to enhance antenna gain [23]. The number of antennas on a UAV is determined by the number of streets connected to the intersection. The directional beam formed by the antenna array is electronically adjustable in terms of beamwidth and direction [10]. To compute antenna gain, we adopt the widely used ideal two-dimensional antenna model in academic research [24]. The directional gain of antenna $G _ { s r } ^ { \xi } ( \theta )$ is defined as follows [25]:

$$
\begin{array} { r } { G _ { s r } ^ { \xi } = \left\{ g _ { \alpha } = \frac { 2 \pi - ( 2 \pi - \alpha ) g _ { \beta } } { \alpha } , \qquad | \theta | \leq \frac { \alpha } { 2 } \right. } \\ { g _ { \beta } , \qquad \left. \frac { \alpha } { 2 } < | \theta | \leq \pi ^ { \prime } \right\} } \end{array}\tag{1}
$$

where $\alpha ^ { \xi }$ and $\theta ^ { \xi }$ represent the half-power beamwidth and alignment deviation angle of the receiver and transmitter, respectively. Here, $\xi \in \{ r x , t x \}$ , $g _ { \alpha }$ denotes the main lobe gain, and $g _ { \beta }$ denotes the sidelobe gain. In addition, $g _ { \alpha }$ and $g _ { \beta }$ must satisfy the conditions $0 \leq g _ { \beta } < 1 \leq g _ { \alpha }$

## C. Channel Modeling

Due to the inherent characteristics of mmWave communication, mmWave links are significantly impacted by high path loss and penetration loss during propagation, which cannot be overlooked in end-to-end delay considerations [26]. The presence of obstacles further exacerbates these challenges by degrading transmission performance, necessitating the simultaneous consideration of both obstacles and path loss in system design. To simulate the propagation loss of 60 GHz mmWave signals, we adopt the standardized logarithmic-distance path loss model proposed in [26]. The propagation loss $P L _ { i j }$ between nodes i and j is defined as follows according to the model:

$$
P L _ { i j } = \rho + 1 0 \delta _ { i j } \log _ { 1 0 } D _ { i j } + 1 5 D _ { i j } / 1 0 0 0 ,\tag{2}
$$

where the attenuation coefficient $\delta _ { i j }$ quantifies the path loss characteristics of the mmWave propagation path, and $D _ { i j }$ denotes the euclidean distance between nodes i and j. The blocking coefficient $\rho$ accounts for the signal attenuation caused by obstacles along the link,1 which is determined by the number of obstacles between nodes i and j. $1 5 D _ { i j } / 1 0 0 0$ is related to the atmospheric 15 1000attenuation of 15 dB/km at 60 GHz. The values of parameters $\delta _ { i j }$ and $\rho$ are specified in [26] and [27], respectively. Since the Signal-to-Noise Ratio (SNR) of the non-line-of-sight (NLOS) link is much lower than that of the LOS link, only the path loss of the LOS link between vehicles is considered. Based on this, the channel gain $G _ { i j } ^ { c } = 1 0 ^ { - \frac { P L _ { i j } } { 1 0 } }$ . The SNR of receiver node $j$ = 10is given by the following [10]:

$$
S N R _ { j } = \frac { G _ { i j } ^ { t x } G _ { i j } ^ { r x } G _ { i j } ^ { c } P _ { i } } { I } ,\tag{3}
$$

where $G _ { i j } ^ { t x }$ and $G _ { i j } ^ { r x }$ represent the antenna gain at transmitter node i and receiver node $j ,$ respectively. $G _ { i j } ^ { c }$ is the channel gain between node i and node j, and $P _ { i }$ is the transmission power. I represents the product of mmWave bandwidth W and Gaussian power spectral density $N _ { 0 }$ . By referring to the Shannon theorem [11], the data rate $R _ { i j }$ on the link between node i and node j is given by:

<!-- image-->  
Fig. 3. DT Framework.

$$
R _ { i j } = W \log _ { 2 } { ( 1 + S N R _ { j } ) } .\tag{4}
$$

## D. DT Synchronization

Ensuring state synchronization between DT and physical entities requires efficient information transmission. Zheng et al. [12] conducted a detailed analysis of communication overhead and delay in DT synchronization and leveraged heterogeneous networks to enhance synchronization performance. We adopt their analysis framework to address these challenges. To minimize synchronization overhead and improve system efficiency, DT synchronization messages must be designed to be as compact as possible. The synchronization data packet format in our solution is illustrated in Fig. 4, which specifies the essential data fields required for synchronization.

Among them, âtimestampâ is used to control the timeliness of the message, âvehicle IDâ uniquely identifies the vehicle on the street, âcoordinatesâ reflect the current location information of the vehicle on the street, which can be obtained through the vehicleâs GNSS terminal, and âspeedâ is the same. In addition, the vehicle also needs to inform the DT of the occupancy rate of its sending buffer and whether it is willing to serve as a forwarding node. DSRC can handle the overhead of the above synchronization messages. DT can flexibly choose synchronization methods through heterogeneous hybrid networks. For example, in sections where RSUs are lacking, 5 G networks can be used for synchronization to achieve optimal transmission efficiency.

Fig. 4. DT synchronization message format.
<table><tr><td rowspan=1 colspan=1>Timestamp</td><td rowspan=1 colspan=1>Vehicle ID Coordinates</td><td rowspan=1 colspan=1>Vehicle ID Coordinates</td><td rowspan=1 colspan=1>Speed</td><td rowspan=1 colspan=1>BufferOccupancy</td><td rowspan=1 colspan=1>ForwardFlag</td></tr></table>

## IV. DT FRAMEWORK AND MODELLING

We consider having M streets $\mathcal { M } = \{ 1 , 2 , \dots , M \}$ and N intersections $\mathcal { N } = \{ 1 , \bar { 2 } , \dots , N \}$ = 1 2. Some of the research [6], [12] = 1 2models vehicles in DTs, where a vehicle-to-vehicle DTN is constructed in the DT system. However, for large cities, the number of streets and intersections is enormous. Deploying DT only in cloud data centers may cause problems similar to those of current urban planning. For example, when a city builds a new street, it often underestimates the amount of traffic and therefore chooses to widen the street or build a viaduct after it becomes too congested. Deploying the full functionality of DT in a cloud data center is similar to this scenario in that the capacity of a DT system may be underestimated in the early stages of its construction, resulting in the need to migrate and scale the cloud container at a later stage. However, this kind of expansion is different from street widening, as it needs to consider data integrity and consistency, thus putting higher requirements on system operation and maintenance personnel.

After considering the above issues, this paper proposes a novel DT framework that divides DT into street sub-DT, intersection sub-DT, and Core-DT, and deploys them in edge servers at roadsides and intersections and in cloud data centers, respectively, as shown in Figs. 2 and 3. These DT modules are connected to each other through ultra-high-bandwidth wired links to form a DTN. The street sub-DT, with street infrastructure and a complete view of traffic flow, is responsible for helping vehicles select the appropriate next hop within the street to relay data packets, while the intersection sub-DT is responsible for running decision algorithms to forward the data packets to the best street. Core-DT is responsible for monitoring the status of each sub-DT, storing historical data, and executing tasks that cannot be completed by each sub-DT. Street sub-DT and intersection sub-DT can exchange information to obtain necessary information, such as obtaining load conditions of other streets, obtaining historical data from Core-DT, and updating AI models. The DT framework proposed in this paper can estimate the computing power of edge servers in advance based on the maximum capacity of streets for newly built roads and intersections in urban expansion, effectively reducing operational and maintenance costs and avoiding passive expansion of cloud data centers due to insufficient early resource allocation. In addition, deploying each sub-DT on edge servers closer to the physical world can also reduce the time required for data synchronization.

The modeling of physical objects in DT involves two stages. The first stage is to model the environment (such as the length, width, and number of lanes of streets) and the static properties of physical objects (such as length, width, height of vehicles) in the corresponding sub-DT. The second stage is a dynamic process, in which the dynamic changes in attributes between vehicles and UAVs (such as location, remaining buffer capacity, etc.) will be synchronized with the DT model through data updates. This paper uses t as the time scale to represent a certain moment. When $t = 0 ,$ , it indicates being in the first stage, and when $t \neq 0$ = 0 = 0it indicates being in the second stage. In the first stage, the sub-DT for street $i \in \mathcal { M }$ can be characterized as:

$$
\begin{array} { r } { D T _ { i } ^ { S } \left( t = 0 \right) = \left\{ R ( 0 ) , V _ { k } ( 0 ) \right\} , } \end{array}\tag{5}
$$

where R represents street information, $R ( 0 ) =$ $\{ e ^ { l e n g t h } , e ^ { \dot { w i d t h } } , e ^ { l \hat { a n e } } , e ^ { o t h e r } \} . e ^ { l e n g t h } , e ^ { w i d t h }$ and $e ^ { l a n e }$ represent the length, width, and number of lanes of the street, respectively. $e ^ { o t h e r }$ represents other information about the lane. $\bar { V _ { k } ( 0 ) } = \bar { \{ v ^ { l e n g t h } , v ^ { w \bar { i } d t h } , v ^ { h e i g h t } , v ^ { o t h e r } \} }$ , where k is the ID (0) =of the vehicle. $v ^ { l e n g t h } , v ^ { w i d t h }$ , and $v ^ { h e i g h \dot { t } }$ represent the length, width, and height of the vehicle, respectively. $v ^ { o t h e r }$ represents other information about the vehicle.

The sub-DT of street $i , i \in \mathcal { M }$ in the second stage is represented as follows:

$$
D T _ { i } ^ { S } \left( t \neq 0 , k \right) = \left\{ L o c _ { k } ( t ) , L o a d _ { k } ( t ) , T X _ { k } ( t ) , \varphi ( t ) \right\} ,\tag{6}
$$

where k is the ID of the vehicle. $L o c _ { k } ( t )$ is the position of the vehicle at time t. $. \ L o a d _ { k } ( t )$ ( )represents the remaining size ( )of the vehicleâs message buffer at time t. $T X _ { k } ( t )$ and $\varphi ( t )$ ( ) ( )represent the orientation and channel state of the antenna at time t, respectively, as well as other parameters related to the vehicle (such as other operating conditions of the vehicle).

Similarly, the intersection sub-DT $j , j \in \mathcal N$ can be characterized as follows:

$$
\begin{array} { r } { D T _ { j } ^ { I } \left( t = 0 \right) = \left\{ U A V _ { j } ( t = 0 ) , S T _ { k } , j ^ { r a n g e } , j ^ { o t h e r } \right\} , } \end{array}\tag{7}
$$

$$
D T _ { j } ^ { I } \left( t \neq 0 , k \right) = \{ U A V _ { j } ( t ) , V _ { k } ( t ) \} ,\tag{8}
$$

where $U A V _ { j } ( t = 0 )$ is the state of $\mathrm { U A V } j . j ^ { r a n g e }$ and $j ^ { o t h e r }$ rep-( = 0)resent the range of the intersection and other related properties, respectively.

<!-- image-->  
Fig. 5. Divide the street into segments and evaluate the appropriate next-hop node from the next segment.

In the first stage of DT modeling, the physical properties of streets and intersections are modeled once the DT is established. For vehicles, when they enter the coverage area of DT, corresponding DT models are created. As the vehicle moves, its state maintains data synchronization with the DT system, enabling the system to update the vehicleâs model. When a vehicle leaves a street and enters an intersection, this does not require the streetâs sub-DT to destroy the model. Instead, it transfers the model to the corresponding sub-DT of the intersection via the DTN. Similarly, when a vehicle enters a street from an intersection, its model is transferred to the corresponding streetâs sub-DT. The model in DT will only be destroyed when the vehicle exits the coverage area of DT.

## V. MMWAVE V2V FORWARDING SCHEME

In this section, we will introduce how packets are transmitted via V2V communication within the street-based environment. In street-based routing schemes, data is transmitted through vehicles along the street. When a vehicle carries data, a suitable relay vehicle is selected as the next hop to forward the data. If a UAV exists among the potential next-hop nodes of the relay vehicle and the data packet has not yet reached its final destination, the data packet will be forwarded to the UAV.

## A. Street Segmentation Strategy

We divide the street into multiple sections based on half of the mmWave communication range R (i.e., . R). The purpose 0 5of this segmentation is to maximize the one-hop distance and minimize the hop count. When a data packet enters a section, a vehicle in that section temporarily stores it and prepares to transmit it to the next section. This reframes the problem as identifying the most suitable relay vehicle in the subsequent section for transmitting the data packet. Fig. 5 illustrates the forwarding mechanism under street segmentation. In more detail, with the assistance of DTs, when a relay vehicle $v _ { s }$ receives a data packet in a section, it queries the street sub-DT to obtain a set of candidate forwarders (CFs) C for the next segment. This set includes the status and priority of all CFs. Since the street sub-DT maintains a global view, all CFs in C have unobstructed LOS links with $v _ { s } .$ , as there are no obstacles blocking their paths. The vehicle then selects the CF with the highest priority for beam alignment and data transmission. If the transmission fails, $v _ { s }$ proceeds to select the next highest priority CF from the set for retransmission.

There are two scenarios where $v _ { s }$ cannot obtain CFs in the next street segment. The first arises when there are too few vehicles on the street, resulting in no available CFs in the subsequent section. The second occurs when the link between the current vehicle $v _ { s }$ and a candidate forwarder in the next section is NLOS. Regardless of these scenarios, the CFs retrieved by $v _ { s }$ from the street sub-DT must reside in the same street segment as $v _ { s }$ . If the size of the CF set C obtained by $v _ { s }$ from the sub-DT is zero, $v _ { s }$ will retain the packet until entering the next segmentâa situation that represents the worst-case scenario for transmission latency.

## B. Candidate Forwarder Selection

According to the above description, the vehicle will select the candidate forwarder with the highest priority as the next hop. The significance of calculating priority lies in evaluating the performance of candidate forwarders. As a forwarding node at the intersection, UAVs have the highest priority. The evaluation of priority will be based on the following metrics.

1) Average Link Rate Factor: The average link rate between the $C F$ and its neighboring nodes represents the link quality. The calculation is as follows:

$$
\bar { R } _ { i } = \frac { \sum R _ { i j } } { | | \mathbb { A } _ { i } | | } , \mathrm { s . t . } v _ { j } \in \mathbb { A } _ { i } , S N R _ { i j } \geq \varepsilon ,\tag{9}
$$

where $\mathbb { A } _ { i }$ denotes a set of neighboring nodes with $C F _ { i }$ , which are located on the same street segment as $C F _ { i }$ , and $\left. \mathbb { A } _ { i } \right.$ is the size of set $\mathbb { A } _ { i } . ~ v _ { j }$ is the neighbor node of $C F _ { i }$ , and Îµ is the threshold of SNR. $R _ { i j }$ denotes the link rate between $C F _ { i }$ and its neighbor $v _ { j }$ , calculated by (4). After calculating the average link rate ${ \bar { R } } _ { i } .$ , the average link rate factor is calculated as follows:

$$
R F _ { i } = \frac { \bar { R _ { i } } } { R _ { \operatorname* { m a x } } } ,\tag{10}
$$

where $R _ { \mathrm { m a x } }$ represents the theoretical maximum transmission rate. Generally speaking, the higher the average link rate, the better the link conditions of $C F _ { i }$ .

2) Distance Factor: Although the street segmentation has tried to increase the one-hop distance, this is still not enough and needs to be built upon further to increase the one-hop distance. The coordinates of the vehicle $v _ { i }$ currently holding the packet are $( x _ { i } , y _ { i } )$ , and the coordinates of $C F _ { j }$ are $( x _ { j } , y _ { j } )$ The distance $D _ { i j }$ )between $v _ { i }$ and $C F _ { j }$ ( )is calculated using the euclidean distance:

$$
D _ { i j } = \sqrt { ( x _ { i } - x _ { j } ) ^ { 2 } + ( y _ { i } - y _ { j } ) ^ { 2 } } .\tag{11}
$$

So the distance factor $D F _ { i }$ of $C F _ { i }$ can be obtained from the following equation:

$$
D F _ { i } = \frac { D _ { i j } } { \mathcal { R } } ,\tag{12}
$$

where $\mathcal { R }$ represents the mmWave communication range.

3) Load Factor: When the data packet is transmitted to the vehicle $v _ { i } .$ , it is temporarily stored in its data buffer and wait for $v _ { i }$ to process it. When a $C F$ has high link quality and is far from the current vehicle carrying the packet, it is often selected as the next hop. However, other vehicles carrying packets are also likely to choose $C F _ { i }$ as the next hop. When there are too many packets waiting to be forwarded at $C F _ { i }$ , the queuing delay caused by this cannot be ignored. We use $L _ { i }$ to represent the load of $C F _ { i }$

<!-- image-->  
Fig. 6. The beam range and angle of the transmitter.

$$
L F _ { i } = \frac { q _ { i } } { Q } ,\tag{13}
$$

where $q _ { i }$ denotes the total size of the used buffer space, and $Q$ represents the current available size of the buffer. Generally speaking, the larger the $L _ { i } .$ , the lower the load.

Based on the above three metrics, the priority $P _ { i }$ of the candidate forwarder is as follows:

$$
P _ { i } = \alpha R F _ { i } + \beta D F _ { i } + \gamma L F _ { i } ,\tag{14}
$$

where $\alpha + \beta + \gamma = 1$

## C. Beamwidth Calculation

After obtaining the C from the street sub-DT and selecting the $C F _ { i }$ with the highest priority as the receiver, $v _ { s }$ , as the transmitter, begins to perform beam alignment. Since the receiverâs position is obtained from DT, it is only necessary to point the beam direction towards the position of the receiver. Assuming the coordinates of the transmitter are $p _ { t } ( x _ { t } , y _ { t } )$ and the coordinates of the receiver are $p _ { r } ( x _ { r } , y _ { r } )$ ( ), the beam direction vector from the transmitter to the receiver is $p _ { t x } ^ {  } = ( x _ { r } - x _ { t } , y _ { r } - y _ { t } )$ = ( )Conversely, the beam direction vector from the receiver to the transmitter is $\vec { d _ { r x } } = ( x _ { r } - x _ { t } , y _ { r } - y _ { t } )$

= ( )1) Calculation of Transmitter Beamwidth: As described in Section III, the transmitter can obtain the physical information of the receiver, such as the length and width of the vehicle. As illustrated in Fig. 6, we establish a circular coverage area with the receiverâs coordinates $p _ { r }$ as the origin and $r = \mathrm { m a x } \{ \mathrm { l e n g t h , w i d t h } \}$ as the radius, and the left and right = maxboundaries of the transmitted beam are tangent to the circular area. Based on geometric relationships, we can conclude that the beamwidth $\alpha ^ { t x }$ of the transmitter is

$$
\alpha ^ { t x } = 2 \arcsin \left( \frac { r } { \sqrt { ( x _ { r } - x _ { t } ) ^ { 2 } + ( y _ { r } - y _ { t } ) ^ { 2 } } } \right) .\tag{15}
$$

However, due to the vehicleâs continuous movement, there is a certain deviation between the coordinates of the receiver obtained from DT by the transmitter and its actual coordinates. If the beamwidth is calculated according to the above method, it may cause the receiver to deviate from the range of the transmission beam during transmission, ultimately leading to link interruption. Therefore, the transmitter recalculates the beamwidth based on the information obtained from the DT receiver and predicts the position of the receiver based on its speed v and direction $\omega .$ As shown in Fig. 7, the receiver may have moved to coordinates $p _ { r c } = ( x _ { r c } , y _ { r c } )$ . Ï is the angle = ( )between the direction of travel and the east-west horizontal direction. Assuming that the time difference between obtaining the receiverâs coordinates from DT and calculating the beamwidth is $\Delta t ,$ , we can calculate the coordinates of $p _ { r c } \mathrm { : }$

<!-- image-->  
Fig. 7. Predicting the future position of vehicles and calculating beam width.

$$
p _ { r c } = ( x _ { r } + \Delta t \mathbf { v } \cos \omega , y _ { r } + \Delta t \mathbf { v } \sin \omega ) .\tag{16}
$$

The direction vector from $p _ { t }$ to $p _ { r c } \mathbf { i s } \vec { d _ { t x c } } = ( x _ { r } + \Delta t \mathbf { v } \cos \omega -$ $x _ { t } , y _ { r } + \Delta t { } \mathbf { v }$ sin $\omega - y _ { t } )$ . According to the cosine theorem, the + Îbeamwidth $\alpha _ { s r } ^ { t x }$ n )of the transmitter is

$$
\alpha _ { s r } ^ { t x } = \frac { \alpha ^ { t x } } { 2 } + \operatorname { a r c c o s } ( \frac { p _ { t x } ^ {  } \cdot p _ { t x c } ^ {  } } { | p _ { t x } ^ {  } | \cdot | p _ { t x c } ^ {  } | } ) .\tag{17}
$$

2) Calculation of Receiver Beamwidth: For the receiver, its beam direction needs to point toward the transmitter. After the transmitter selects the optimal receiver, it informs the receiver via the DT that it is ready to build the mmWave link. To ensure that the receiving beam and the transmitting beam can be aligned, once the receiver obtains the transmitterâs coordinates information from the DT, it is able to construct a circular error region centered at the receiverâs coordinates with an error radius of $r _ { \epsilon } .$ . Assuming that the error radius is a system parameter, the receiverâs beamwidth $\alpha ^ { r x }$ is:

$$
\alpha ^ { r x } = 2 \arcsin \left( \frac { r _ { \epsilon } } { \sqrt { ( x _ { r } - x _ { t } ) ^ { 2 } + ( y _ { r } - y _ { t } ) ^ { 2 } } } \right) .\tag{18}
$$

After completing the calculation of beamwidth, a mmWave link is established between the transmitter and receiver to transmit data. Algorithm 1 describes the complete process of the street sub-DT returning the set C.

The complete process of data transmission within the street is summarized as Algorithm 2. $v _ { i }$ retrieves the packet from the buffer, obtains the destination vehicle $v _ { d }$ of the packet, and obtains the set C from DT. If $v _ { d }$ is a $C F$ , the packet is forwarded to $v _ { d } .$ If it does not exist, the packet is transmitted to the $C F$ with the highest priority. If set C is empty, $v _ { i }$ carries the packet and waits for the next processing.

Algorithm 1: Street sub-DT Generates Candidate Forwarder   
Set $\mathbb { C } .$   
Input: Vehicle set V located within the street   
1 Initialize the $\mathbb { C }$ and A ;   
2 for $\nu _ { i } \in \mathbb { V }$ do   
3 obtaining the neighbors $\mathbb { A }$ of $\nu _ { i }$ in the next street   
segment;   
4 if $\mathbb { C }$ is empty then   
5 obtaining the neighbors A of $\nu _ { i }$ in the some   
street segment;   
6 end   
for $C F _ { j } \in \mathbb { A }$ do   
8 if $C F _ { j }$ is UAV then   
9 the priority of UAV is set to maximum;   
10 continue;   
11 end   
12 calculating average link rate factor ${ \bar { R { F } _ { j } } }$ as   
Eq. (10);   
13 calculating distance factor $D F _ { i j }$ ,as Eq. (12);   
14 calculating load factor $L F _ { j }$ as Eq. (13);   
15 calculating the priority $P _ { j }$ of $C F _ { j }$ as Eq. (14);   
16 $\mathbb { C } = \mathbb { C } \cup \left\{ \left\{ C F _ { j } , P _ { j } \right\} \right\}$ Â·   
17 end   
18 synchronize the set $\mathbb { C }$ to the vehicle $\nu _ { i }$   
19 end

## VI. STREET SELECTION SCHEME

In this section, we will introduce how to select the target street for a packet upon its arrival at the UAVs at the intersection and forward it to the vehicles on the corresponding street. Due to the deployment of UAVs at intersections, hereafter, the terms $U A V _ { i }$ street sub-DT, and intersection i are considered equivalent, and we will replace them with intersection i. In the scenario of this paper, both the source vehicle $v _ { s }$ (which generates the packet) and the destination vehicle $v _ { d }$ (the packetâs final destination) are located on the street. The source vehicle $v _ { s }$ obtains its own location and the location of the destination vehicle $v _ { d }$ from the DT. Subsequently, with the help of the DT, $v _ { s }$ determines the source intersection $s _ { s }$ and the destination intersection $s _ { d } .$ . The identifiers of $v _ { d } ,$ $\boldsymbol { s } _ { s }$ , and $s _ { d }$ are added to the packetâs header. The packet is forwarded along the street to the destination intersection $s _ { d }$ and forwarded by the UAV to the street where $v _ { d }$ is located.

## A. Multi-Objective Parallel Q-Learning Model

Q-Learning is a model-free tabular method that performs actions in the environment, receives feedback, and updates the Q-table accordingly. The meaning of the Q-table in Q-Learning is similar to that of the routing table in the router. The action of selecting the maximum Q-value is like selecting the best matching entry in the routing table to route data.

In our scenario, the intersection takes action to choose to forward the data packet to the corresponding street, and the packet arrives at another intersection or is lost during transmission on the street due to environmental influence. The intersection receives a reward and updates the ârouting tableâ to influence the next routing selection. Therefore, the process of generating the optimal control strategy through Q-Learning is consistent with the idea of selecting the optimal routing path [28]. The reinforcement learning agent is deployed in the intersection sub-DT and learns separately for the two key metrics of delivery rate and delay. Therefore, we divide the agent into $A g e n t _ { P D R }$ and $A g e n t _ { D e l a y }$ , which are parallel to achieve the best performance on a single metric.

Algorithm 2: The Forwarding Mechanism Within the Street   
at $v _ { i } .$   
1 for buffer is not empty do   
2 retrieve a packet from the buffer;   
3 $\nu _ { d }$ âpacket;   
4 $\nu _ { i }$ initiates a request to subDT;   
5 C â street sub-DT executes Algorithm 1;   
6 if C is empty then   
7 store the packet to buffer ;   
8 else   
9 if $\nu _ { d } \in \mathbb { C }$ then   
10 $\nu _ { i }$ selects $\nu _ { d }$ as the receiver $\nu _ { j } ;$   
11 end   
12 $\nu _ { i }$ selects the highest priority CF from $\mathbb { C }$ as   
the next hop node $\nu _ { j } ;$   
13 vi uses DT to notify $\nu j$ that it is ready to   
receive packets;   
14 $\nu _ { i }$ calculate the beamwidth $\alpha _ { i j } ^ { t x }$ ,as Eq. (17);   
15 $\nu _ { i }$ and $\nu _ { j }$ establish mmWave link and forward   
packet;   
16 if step 15 fails then   
17 $\nu _ { i }$ selects the second highest priority CF   
from $\mathbb { C }$ as the next hop node $\nu _ { j }$ and   
executes step 15 and step 16;   
18 end   
19 end   
20 end

The Q-table of the Agent is a three-dimensional matrix, where $Q ( S _ { t } , S _ { d } , a )$ represents the Q-value in the Q-table, $S _ { t }$ represents ( )the current intersection, $S _ { d }$ represents the destination intersection, and a represents the action selected at $S _ { t }$ . The state space represents the collection of all UAVs deployed at intersections. When the packet is forwarded to the UAV above intersection $i ,$ it is represented as state $S _ { i } \in S$ . The action space represents a group of street sections connected to the intersection. The agent selects action $a , a \in A$ , causing the packet to change from state $S _ { i }$ to $S _ { j }$

$R _ { P D R } ( S _ { t } , S _ { d } , a )$ represents the immediate reward for packet ( )delivery ratio after taking action a in state $S _ { t }$ . When the packet reaches the destination intersection $S _ { d }$ , the reward is Ï; otherwise, it is 0.

$R _ { D e l a y } ( S _ { t } , S _ { d } , a )$ represents the reward for packet delay after ( )taking action a in state $S _ { t }$

$$
R _ { D e l a y } ( S _ { t } , S _ { d } , a ) = \exp \left( - \frac { D e l a y _ { t } } { D e l a y _ { \mathrm { m a x } } } \right) ,\tag{19}
$$

where $D e l a y _ { t }$ is the delay of the packet on the target street, and $D e l a y _ { \mathrm { m a x } }$ is the recorded longest delay.

In the training process of the Q-learning algorithm, we use the historical traffic stored in DT to learn the Q-table, which requires exploring the environment to choose the action to update the Q-table. We use the common Îµ-greedy strategy to achieve environmental exploration. After a transmission is completed (an exploration), the agent in DT will update the Q-table, and the process of updating the Q-table is equivalent to maintaining the routing table. The update method for the Q-table is as follows:

$$
\begin{array} { r l r } & { } & { Q _ { i } ( S _ { t } , S _ { d } , a ) = \alpha \left\{ R _ { i } ( S _ { t } , S _ { d } , a ) + \gamma \operatorname* { m a x } _ { a ^ { \prime } } Q _ { i } ( S _ { t ^ { \prime } } , S _ { d } , a ^ { \prime } ) \right\} } \\ & { } & { + ( 1 - \alpha ) Q _ { i } ( S _ { t } , S _ { d } , a ) , \quad i \in \{ P D R , D e l a y \} , } \end{array}\tag{20}
$$

where Î± the learning rate, $\alpha \in [ \operatorname* { m a x } _ { y } 0 , 1 ]$ , and the larger the Î±, the higher the tendency to learn new knowledge. Î³ is the discount factor. $S _ { t ^ { \prime } }$ represents the next state of $S _ { t }$ after performing an action, and a represents all possible actions in state $S _ { t ^ { \prime } }$

## B. Selection of Target Street

In the intersection sub-DT, two parallel agents learn the packet delivery rate and delay indicators separately. After the Q-Learning algorithm converges, each agent achieves optimal performance on the corresponding indicators. However, the path with the highest packet delivery rate may perform poorly in terms of latency, while the path with the lowest latency may perform poorly in terms of delivery rate. We need to consider the packet delivery rate and delay holistically, assign weights to each of the two Q-tables, and fuse them. Therefore, we use a strategy to select the optimal street based on vehicle density. First, due to differences in learning between the two Q-tables, the range of Q-values in the interval may differ, and it is necessary to standardize them before fusion. Subsequently, we fuse the two Q-tables based on their weights. Finally, we select the street corresponding to the maximum Q-value from the fused Q-table for forwarding. If the vehicle density on the street is too low, we choose the street corresponding to the second-highest Q-value.

Normalization: First, we need to normalize the Q-value in the Q-table to the interval (0,1) and obtain the normalized Q-table $Q _ { i } ^ { N } ( S _ { t } , S _ { d } , a )$ . We use the min-max normalization function [29] ( )to normalize the data of the two Q-tables.

Fusion: After normalization, we fuse $Q _ { P D R }$ and $Q _ { D e l a y }$ into $Q ^ { * }$ according to (21):

$$
Q ^ { * } ( x , y , z ) = i \times Q _ { P D R } ^ { N } ( x , y , z ) + j \times Q _ { D e l a y } ^ { N } ( x , y , z ) ,\tag{)(21}
$$

where i and j are the normalized parameters of delay and PDR, respectively, and their values depend on the application scenario, i.e., delay priority or PDR priority orientation. For instance, in general, delay and PDR have the same priority, with $i = 0 . 5 ,$ $j = 0 . 5$ = 0 5. When the network connected to the street is under high = 0 5load, the agent will adjust parameters to ensure lower latency, with $i = 0 . 2 5 , j = 0 . 7 5$

= 0 25 = 0 75Decision: Finally, the agent will select the street corresponding to the maximum Q-value as the forwarding direction, and the UAV will transmit the packet in the buffer to the vehicles on that street. However, if the density of vehicles on the street is too low, the data packets will be carried by vehicles for a long time and cannot be forwarded, resulting in higher delays. Next, we will explain how to calculate the vehicle density on the street.

```powershell
Algorithm 3: Intersection i Forwards Packets.
1 for buffer is not empty do
2 retrieve a packet from the buffer;
3 $S _ { d }$ âpacket;
4 determine the current state $( S _ { i } , S _ { d } ) ;$
5 normalize $Q _ { P D R }$ and $\boldsymbol { Q _ { D e l a y } } ;$
6 fuse Q-table according to load conditions, as
Eq. (21);
for $a \in A$ do
8 choose action a with the maximum
$\boldsymbol { Q } ^ { * } ( S _ { i } , S _ { d } , a ) ;$
9 end
10 calculate $\mu ,$ as Eq. (23);
11 if Î¼<pmIN or $\mu > \rho _ { M A X }$ then
12 choose action a with the second largest
$\boldsymbol { Q } ^ { * } ( S _ { i } , S _ { d } , a ) ;$
13 end
14 transfer the packet to the corresponding vehicle on
the street;
15 end
```

From Section IV, the street is divided into several street segments, where L represents the length of the street and mmWave has a transmission distance of R. We can calculate the number of street segments SN on the street as:

$$
S N = \left\lceil { \frac { L } { \mathcal { R } } } \right\rceil .\tag{22}
$$

The number of vehicles in segment i is $\kappa _ { i }$ . The average number of vehicles on each street segment $\mu$ can be obtained as:

$$
\mu = \frac { \sum _ { i = 1 } ^ { S N } \kappa _ { i } } { S N } .\tag{23}
$$

The higher the value of $\mu ,$ the higher the density of the street, and the higher the probability that the data packet will be forwarded to this street segment. The smaller the value of $\mid \mu ,$ the lower the density of vehicles on the street. When the density is too low, the probability of vehicles not finding suitable candidate forwarders and carrying data packets while driving increases. When $\mu > \rho _ { M A X }$ or $\mu < \rho _ { M I N }$ , this indicates that the vehicle density is too high or too low. At this time, the intersection chooses the street corresponding to the second-highest Q-value as the target street. Algorithm 3, as a summary, demonstrates the process of forwarding packets from intersection i to the corresponding street.

## VII. PERFORMANCE EVALUATION

We use the network discrete-event simulator OMNeT++ [30] and the street traffic simulator SUMO [31] to implement our mmWave hierarchical routing scheme. In order to tackle the impact of the relative position of vehicles and vehicle density on path loss, we adopt the Krauss Model [32], a car-following model that effectively describes the vehicle speed-density relationship in traffic flow, making the simulation results closer to the performance in real-world street scenarios. We have implemented all the mmWave functionality, including the mmWave channel, antenna model, path loss model, etc., by modifying the open-source framework Veins [33]. Our simulation scenario is a 1.5 km Ã 1.5 km urban grid consisting of 25 two-directional 4-lane streets and 16 intersections. The maximum speed of the vehicles is limited to 60 km/h. The mmWave frequency is set to 60 GHz, and the bandwidth is set to 1.08 GHz. Table I presents more detailed experimental parameters.

TABLE I SIMULATION PARAMETERS
<table><tr><td colspan="2">Simulation setup</td></tr><tr><td>Simulation Times</td><td>10</td></tr><tr><td>Simulation Time</td><td>800 s</td></tr><tr><td>Vehicle Maximum Speed</td><td>60 km/h</td></tr><tr><td>Numberof Vehicle</td><td>[300,500....,1100]</td></tr><tr><td>Packet Generation Rate</td><td>[1,2.,...,.5] packet/s</td></tr><tr><td>Car Following Model</td><td>Krauss Model</td></tr><tr><td>Frequency Band</td><td>60 GHz</td></tr><tr><td>Bandwidth</td><td>1.08 GHz</td></tr><tr><td rowspan="3">Maximum transmission range Transmission Power</td><td></td></tr><tr><td>100 m</td></tr><tr><td>30 mW</td></tr><tr><td>SNR Threshold</td><td>8dB</td></tr><tr><td>Noise Power</td><td>-174 dBm/Hz</td></tr><tr><td>pmin</td><td>5</td></tr><tr><td>Pmax</td><td>20</td></tr></table>

The following performance metrics are considered for our simulation experiments:

Average Delay: Represents the delay in transmitting packets from the source vehicle to the destination vehicle, including the time spent queuing in the vehiclesâ buffers for processing (vehicle carrying packets).

Packet Delivery Ratio: Represents the ratio of the number of packets successfully delivered to the destination vehicle to the total number of packets generated by the source vehicle.

- Average Hop Count: The ratio of the total number of hops in the transmission process of data packets successfully delivered to the destination vehicle to the total number of data packets successfully delivered to the destination vehicle.

In order to demonstrate the superiority of proposed routing scheme and the necessity of incorporating DTs in the experiment, we compared it with the following schemes:

Without DT (No-DT): The scheme is not assisted by DTs, so the vehicle relies on periodic broadcast beacon packets in the 5.9 GHz band (DSRC) to obtain information about neighboring vehicles and send beam alignment packets before establishing the mmWave link. The distribution of vehicles on the street is unavailable at the intersection, and the UAV is not informed about the transmission of the packets. Therefore, when the packet is transmitted to the UAV at the intersection, the street closest to the destination vehicle is selected based on geometric relationships.

<!-- image-->  
Fig. 8. Average speed and average relative speed with the density of vehicles.

GF-DT: This scheme employs greedy forwarding within the street, and the vehicle will choose the closest CF as the next hop. When the packet is transmitted to the UAV at the intersection, the street closest to the destination vehicle will be selected.

ELITE [6]: This scheme is a routing scheme for softwaredefined vehicle networks supported by DTs. The nearest neighbor node is greedily selected for forwarding within the street. When the data packet arrives at the intersection, the reinforced Q-learning algorithm with a fusion strategy is used to select the best street for transmission. Since the original scheme did not use mmWave for data transmission, mmWave will be used as the transmission medium in the simulation experiment of this paper to evaluate its performance in this scenario.

## A. The Impact of Vehicle Density on Performance

We first evaluate the impact of vehicle density on performance. We use the number of vehicles to measure the density of vehicles. Generally speaking, the higher the number of vehicles, the higher the density of vehicles. The number of vehicles is set to 300, 500, 700, 900, and 1100 in SUMO settings. The maximum speed of the vehicle is 60 km/h. To investigate the impact of vehicle density on traffic flow dynamics, we analyzed the relationship between vehicle density (defined as the number of vehicles per kilometer per lane) and both the average vehicle speed and the relative speed between vehicles, as shown in Fig. 8. As vehicle density increases, the average vehicle speed exhibits a decreasing trend. In addition to the average speed, the relative speed between vehicles (i.e., the instantaneous speed difference between adjacent vehicles) also decreases. This phenomenon has dual technical implications:

<!-- image-->  
Fig. 9. Packet delivery ratio with the number of vehicles.

<!-- image-->  
Fig. 10. Average delay with the number of vehicles.

on one hand, the lower relative speed reduces the misalignment errors of mmWave antennas between vehicles, mitigating signal attenuation or packet loss caused by high-speed movement. On the other hand, the stability of relative positions between vehicles at higher densities improves the tracking accuracy of vehicle coordinates by DT, offering potential advantages for system performance in high-density scenarios. The experimental results are shown in Figs. 9, 10, and 11, respectively.

Fig. 9 demonstrates the packet delivery rates of the four schemes under different vehicle densities. From Fig. 10, it can be seen that as the vehicle density increases, the packet delivery rates of the four schemes all show an upward trend. However, in the case of low vehicle density, the packet delivery rate (PDR) performance of the No-DT scheme is not ideal. This may be related to the periodic broadcasting of beacon packets. During the beam alignment phase, transmission failure may occur due to the receiver status obtained by the transmitter is outdated and the vehicle potentially moving to another location. In addition, when the lifetime of a packet is zero, it may be discarded. As the density of vehicles increases, their driving speed slows down, which means they are more stable. However, due to periodic broadcast packets, as vehicle density increases, the information obtained by the transmitter may be incomplete due to broadcast storms and hidden terminal issues, resulting in conflicts between beam alignment packets and broadcast beacon packets, making it impossible to perform beam alignment. Therefore, in high-density situations, the packet delivery rate of the GF-DT scheme is not as good as that of the No-DT scheme. However, in high-density situations, the GF-DT scheme has a high probability of selecting the same relay as the relay chosen by the scheme due to the difficulty of mmWaves penetrating obstacles, thereby weakening the influence of vehicle density on intersection selection. Therefore, the packet delivery rate of this scheme is relatively close to that of the proposed scheme. Both ELITE and the proposed scheme optimize the packet delivery rate at the street selection level, so they are better than the other two schemes. The proposed scheme evaluates the vehicle density of the target street at the street selection level and selects the optimal relay within the street, which can effectively avoid the loss of data packets due to excessive hops. Therefore, the proposed scheme is better than ELITE in terms of delivery rate.

<!-- image-->  
Fig. 11. Average hop count with the number of vehicles.

Fig. 10 demonstrates the average delay of the four schemes under different vehicle densities. It can be seen that the delay performance of the No-DT scheme is the worst, followed by the GF-DT scheme. The main reasons are: (1) without DT assistance, the No-DT scheme requires the transmitter to send beam alignment packets to the receiver using the Sub-6 GHz band before establishing the mmWave link, which increases the delay. (2) The UAVs at intersections do not know the vehicle density of each street, resulting in a certain probability that the vehicle density of the target street is too low. When the packet is forwarded to the vehicle on the destination street, it cannot find a suitable next hop. At this point, the packet will be carried by the vehicle, which introduces a very high latency. (3) Failure of beam alignment leads to packet being carried by vehicles. The GF-DT scheme greedily forwards to the nearest vehicle without considering the link condition and load of the receiver, so the selection of candidate forwarders may not be optimal. Poorer link conditions and longer queuing delays lead to an increase in the total delay. In addition, the GF-DT scheme selects the nearest vehicle for transmission, leading to an increase in the number of hops, which also has a negative impact on the delay. As the density of vehicles increases, the distance of one-hop transmission decreases, which leads to an increase in the total number of hops, and therefore the average delay rises as the density of vehicles increases. Although ELITE optimizes latency at the street selection level, it still uses the nearest greedy forwarding within the street, so the latency performance is not satisfactory. The proposed scheme in this paper, with the assistance of DT, does not need to send beam-aligned auxiliary packets before the establishment of the mmWave link. In addition, at intersections, the sub-DT takes into account the transmission delay of the target street and the density of vehicles, resulting in better delay performance.

Fig. 11 demonstrates the average hop count of the four schemes under different vehicle densities. As the vehicle density increases, the average hop count is on the rise. At lower vehicle densities, the scheme proposed in this paper has the lowest number of hops, followed by the No-DT scheme, while the GF-DT scheme has the highest number of hops. The reason for this situation is also obvious. As mentioned in the previous paragraph, due to the use of periodic broadcast beacon packets, the No-DT scheme may result in the loss of broadcast packets, which can have a greater impact on the vehiclesâ ability to obtain the best next-hop node. GF-DT employs a greedy strategy that selects the closest candidate forwarder to forward the packet. In other words, the GF-DT scheme does not optimize the number of hops, and hence the average number of hops increases faster as the density of vehicles increases. Although ELITE performs greedy forwarding within the street, it takes the average number of hops of the target street into consideration at the intersection, so it is better than GF-DT in terms of hops. However, the optimization of the number of hops at the intersection cannot make up for the shortcomings of greedy forwarding, so ELITE is not as good as the NO-DT scheme in terms of average hops. When the number of vehicles is 1100, the vehicles become denser. Due to the difficulty of penetrating obstacles with mmWaves, it becomes difficult to select the next hop further away. Therefore, at higher vehicle densities, the average hop counts of the four schemes do not differ much. Our proposed scheme considers the transmission distance inside the street and the forwarding process at the intersection avoids the street with higher vehicle density, which means that the hop count metrics are optimized both inside the street and at the intersection. Therefore, the scheme has the lowest average hop count performance.

## B. The Impact of Network Load on Performance

We use the packet generation rate to measure network load. The higher the packet generation rate, the more packets there are in the network, and the network load becomes more severe. The packet generation rates are set to 1, 2, 3, 4, and 5, respectively, with units of packets/s. When discussing network load, we keep the number of vehicles fixed at 500. The experimental results are shown in Figs. 12, 13, and 14, respectively.

<!-- image-->  
Fig. 12. Packet delivery ratio with the packet generation rate.

<!-- image-->  
Fig. 13. Average hop count with the packet generation rate.

Fig. 12 demonstrates the impact of different packet generation rates on the packet delivery rate. It can be seen that as the network load increases, the idle buffer of the vehicles becomes a scarce resource, which results in some packets not being able to enter the buffer of the vehicles, thus leading to packet loss. Since the GF-DT scheme and ELITE do not pay attention to the load of the candidate relay nodes in the street, it is more sensitive to the network load, and therefore the GF-DT scheme and ELITE have the lowest packet delivery rate performance metric. For the No-DT scheme, although it considers the available buffer size of the relay vehicles, the UAVs responsible for packet intersection forwarding are merely greedy when the overall load of the network rises due to the lack of assistance from DTs. However, the scheme considers the load situation of the candidate forwarders within the street. Therefore, the packet delivery rate of the No-DT scheme is better than that of the GF-DT scheme. Our proposed scheme not only considers the load situation within the street but also adjusts the fusion policy to focus on guaranteeing the delivery rate based on the overall load of the network at the street selection level, so this scheme has the best packet delivery rate performance.

<!-- image-->  
Fig. 14. Average delay with the packet generation rate.

Fig. 13 demonstrates the impact of different packet generation rates on the average hop count, all of four schemes remain stable overall. The difference in average hop count performance among the four schemes is consistent with the analysis process of Fig. 11.

Fig. 14 demonstrates the impact of different packet generation rates on the average delay. As the number of packets in the network increases, the number of packets waiting to be processed in the buffers of the vehicles will increase dramatically, which leads to an increase in the queuing delay. Both the No-DT scheme and our proposed scheme take into account the effect of load, and the load profile of the vehicles is an important basis for calculating the priority of the candidate forwarders. As the number of packets in the network increases, the UAVs responsible for packet intersection forwarding are simply greedy and do not select the optimal street based on the learning situation; hence, the average delay of the No-DT scheme is higher than that of the scheme proposed in this paper. Although the average delay is increasing, it is still within the acceptable range. However, the GF-DT scheme and ELITE do not take into account the network load, so when the number of packets in the network exceeds a certain value, the delay increases significantly. Our proposed scheme integrates the load of the candidate forwarders in the selection of relay vehicles inside the streets, in addition to avoiding the target streets with high or low vehicle density in the street selection. Thus, this scheme performs the best in terms of average delay.

## VIII. CONCLUSION

In this paper, we applied DT to mmWave communication and proposed a street-based mmWave multi-hop V2X routing scheme under DT empowerment in urban scenarios. First, we proposed a novel DT framework that divides DT into street sub-DT and intersection sub-DT. With the assistance of street sub-DT within the street, the vehicle selects the best relay vehicle as the next hop for forwarding data and assists the transmitter and receiver in beamforming to reduce latency. We deployed the UAVâs reinforcement learning routing algorithm at intersection sub-DTs. The sub-DTs make decisions to forward packets to the optimal street. In addition, we also considered vehicle density and network load as the basis for optimal street selection. The experimental results indicate that our solution has significant advantages in key indicators of packet delivery rate and latency.

## REFERENCES

[1] A. D. Devangavi and R. Gupta, âRouting protocols in VANETâA survey,â in Proc. Int. Conf. Smart Technol. Smart Nation, 2017, pp. 163â167.

[2] N. H. Hussein, C. T. Yaw, S. P. Koh, S. K. Tiong, and K. H. Chong, âA comprehensive survey on vehicular networking: Communications, applications, challenges, and upcoming research directions,â IEEE Access, vol. 10, pp. 86127â86180, 2022.

[3] F. Tang, X. Chen, T. K. Rodrigues, M. Zhao, and N. Kato, âSurvey on digital twin edge networks (DITEN) toward 6G,â IEEE Open J. Commun. Soc., vol. 3, pp. 1360â1381, 2022.

[4] B. Li, Y. Liu, L. Tan, H. Pan, and Y. Zhang, âDigital twin assisted task offloading for aerial edge computing and networks,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 10863â10877, Oct. 2022.

[5] Y. Wu, K. Zhang, and Y. Zhang, âDigital twin networks: A survey,â IEEE Internet Things J., vol. 8, no. 18, pp. 13789â13804, Sep. 2021.

[6] L. Zhao, Z. Bi, A. Hawbani, K. Yu, Y. Zhang, and M. Guizani, âELITE: An intelligent digital twin-based hierarchical routing scheme for softwarized vehicular networks,â IEEE Trans. Mobile Comput., vol. 22, no. 9, pp. 5231â5247, Sep. 2023.

[7] K. Zhang, J. Cao, S. Maharjan, and Y. Zhang, âDigital twin empowered content caching in social-aware vehicular edge networks,â IEEE Trans. Computat. Social Syst., vol. 9, no. 1, pp. 239â251, Feb. 2022.

[8] T. Liu et al., âResource allocation in DT-assisted internet of vehicles via edge intelligent cooperation,â IEEE Internet Things J., vol. 9, no. 18, pp. 17608â17626, Sep. 2022.

[9] B. Fan, Y. Wu, Z. He, Y. Chen, T. Q. Quek, and C.-Z. Xu, âDigital twin empowered mobile edge computing for intelligent vehicular lane-changing,â IEEE Netw., vol. 35, no. 6, pp. 194â201, Nov./Dec. 2021.

[10] X. Zhang, S. Pan, and Q. Miao, âAdaptive beamforming-based gigabit message dissemination for highway VANETs,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 7666â7679, Jul. 2022.

[11] B. Fan, H. Tian, S. Zhu, Y. Chen, and X. Zhu, âTraffic-aware relay vehicle selection in millimeter-wave vehicle-to-vehicle communication,â IEEE Wireless Commun. Lett., vol. 8, no. 2, pp. 400â403, Apr. 2019.

[12] J. Zheng et al., âDigital twin empowered heterogeneous network selection in vehicular networks with knowledge transfer,â IEEE Trans. Veh. Technol., vol. 71, no. 11, pp. 12154â12168, Nov. 2022.

[13] R. Cai, Y. Feng, D. He, Y. Xu, Y. Zhang, and W. Xie, âA combined cable-connected RSU and UAV-assisted RSU deployment strategy in V2I communication,â in Proc. IEEE Int. Conf. Commun., 2020, pp. 1â6.

[14] B. Hazarika, K. Singh, C.-P. Li, A. Schmeink, and K. F. Tsang, âRADiT: Resource allocation in digital twin-driven UAV-aided internet of vehicle networks,â IEEE J. Sel. Areas Commun., vol. 41, no. 11, pp. 3369â3385, Nov. 2023.

[15] M. S. Bahbahani and E. Alsusa, âA directional clustering protocol for millimeter wave vehicular ad hoc networks,â in Proc. IEEE 91st Veh. Technol. Conf., 2020, pp. 1â6.

[16] Y. Ju et al., âDeep reinforcement learning based joint beam allocation and relay selection in mmWave vehicular networks,â IEEE Trans. Commun., vol. 71, no. 4, pp. 1997â2012, Apr. 2023.

[17] I. Rasheed, F. Hu, Y.-K. Hong, and B. Balasubramanian, âIntelligent vehicle network routing with adaptive 3D beam alignment for mmWave 5G-based V2X communications,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 5, pp. 2706â2718, May 2021.

[18] Y. Li, X. Zhang, L. Yan, and D. K. Sung, âAn opportunistic routing protocol based on position information for beam alignment in millimeter wave vehicular communications,â in Proc. IEEE Int. Conf. Commun., 2022, pp. 267â272.

[19] J. Shen et al., âTaming distributed one-hop multicasting in millimeter-wave VANETs,â IEEE Trans. Mobile Comput., vol. 23, no. 11, pp. 10570â10583, Nov. 2024.

[20] K. Zhang, J. Cao, and Y. Zhang, âAdaptive digital twin and multiagent deep reinforcement learning for vehicular edge computing and networks,â IEEE Trans. Ind. Inform., vol. 18, no. 2, pp. 1405â1413, Feb. 2022.

[21] Z. Wang et al., âA digital twin paradigm: Vehicle-to-cloud based advanced driver assistance systems,â in Proc. IEEE 91st Veh. Technol. Conf., 2020, pp. 1â6.

[22] L. Zhao, G. Han, Z. Li, and L. Shu, âIntelligent digital twin-based softwaredefined vehicular networks,â IEEE Netw., vol. 34, no. 5, pp. 178â184, Sep./Oct. 2020.

[23] L. X. Cai, L. Cai, X. Shen, and J. W. Mark, âRex: A randomized exclusive region based scheduling scheme for mmWave WPANs with directional antenna,â IEEE Trans. Wireless Commun., vol. 9, no. 1, pp. 113â121, Jan. 2010.

[24] Y. Wang, H. Wu, Y. Niu, Z. Han, B. Ai, and Z. Zhong, âCoalition game based full-duplex popular content distribution in mmWave vehicular networks,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13836â13848, Nov. 2020.

[25] J. Wildman, P. H. J. Nardelli, M. Latva-Aho, and S. Weber, âOn the joint impact of beamwidth and orientation error on throughput in directional wireless poisson networks,â IEEE Trans. Wireless Commun., vol. 13, no. 12, pp. 7072â7085, Dec. 2014.

[26] A. Yamamoto, K. Ogawa, T. Horimatsu, A. Kato, and M. Fujise, âPathloss prediction models for intervehicle communication at 60 GHz,â IEEE Trans. Veh. Technol., vol. 57, no. 1, pp. 65â78, Jan. 2008.

[27] V. Va et al., âMillimeter wave vehicular communications: A survey,â Found. Trends Netw., vol. 10, no. 1, pp. 1â113, 2016.

[28] L. Luo, L. Sheng, H. Yu, and G. Sun, âIntersection-based V2X routing via reinforcement learning in vehicular ad hoc networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 6, pp. 5446â5459, Jun. 2022.

[29] M. Xie, Y. Bai, M. Huang, Y. Deng, and Z. Hu, âEnergy-and time-aware data acquisition for mobile robots using mixed cognition particle swarm optimization,â IEEE Internet Things J., vol. 7, no. 8, pp. 7734â7750, Aug. 2020.

[30] V. AndrÃ¡s, âThe OMNeT++ discrete event simulation system,â in Proc. Eur. Simul. Multiconf., 2001, pp. 1â7.

[31] D. Krajzewicz, âTraffic simulation with SUMOâsimulation of urban mobility,â in Fundamentals of Traffic Simulation. Berlin, Germany: Springer, Aug. 2010, pp. 269â293.

[32] S. KrauÃ, âMicroscopic modeling of traffic flow: Investigation of collision free vehicle dynamics,â 1998. [Online]. Available: https://sumo.dlr.de/pdf/ KraussDiss.pdf

[33] C. Sommer, R. German, and F. Dressler, âBidirectionally coupled network and road traffic simulation for improved IVC analysis,â IEEE Trans. Mobile Comput., vol. 10, no. 1, pp. 3â15, Jan. 2011.

<!-- image-->  
Taolue Zhou received the BS degree in information security from the Hefei University of Technology, Hefei, China, in 2019. He is currently working toward the masterâs degree with the School of Data Science, University of Science and Technology of China. His research interest include vehicular networks.

<!-- image-->  
Xiaohan Wu received the BS degree in computer science and technology from the University of Electronic Science and Technology of China, Chengdu, China, in 2019. He is currently working toward the PhD degree with the School of Computer Science and Technology, University of Science and Technology of China. His research interest include wireless networks.

<!-- image-->

Xinming Zhang (Senior Member, IEEE) received the BE and ME degrees in electrical engineering from the China University of Mining and Technology, Xuzhou, China, in 1985 and 1988, respectively, and the PhD degree in computer science and technology from the University of Science and Technology of China, Hefei, China, in 2001. Since 2002, he has been with the faculty of the University of Science and Technology of China, where he is currently a professor with the School of Computer Science and Technology. From 2005 to 2006, he was a visiting

professor with the Department of Electrical Engineering and Computer Science, Korea Advanced Institute of Science and Technology, Daejeon, Korea. His research interests include wireless networks, target recognition, graph neural networks, and $\mathrm { B i g }$ Data security. He has published more than 100 papers. He won the second prize of Science and Technology Award of Anhui Province of China in Natural Sciences in 2017. He won the awards of Top reviewers (1% ) in Computer Science & Cross Field by Publons in 2019.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_4_img_1.jpeg|page_4_img_1]]
3. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_11_img_1.jpeg|page_11_img_1]]
4. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_11_img_2.jpeg|page_11_img_2]]
5. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_11_img_3.jpeg|page_11_img_3]]
6. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_12_img_1.jpeg|page_12_img_1]]
7. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_13_img_1.jpeg|page_13_img_1]]
8. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_13_img_2.jpeg|page_13_img_2]]
9. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_13_img_3.jpeg|page_13_img_3]]
10. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_14_img_1.jpeg|page_14_img_1]]
11. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_15_img_1.jpeg|page_15_img_1]]
12. [[../extracted_images/Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance/page_15_img_2.jpeg|page_15_img_2]]

---

