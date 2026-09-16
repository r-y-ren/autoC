# Stable Matching Based Revenue Maximization for Federated Learning in UAV-Assisted WBANs

Moirangthem Biken Singh , Graduate Student Member, IEEE, Himanshu Singh , and Ajay Pratap , Member, IEEE

AbstractâThis work explores the coupling of Machine Learning (ML) and Wireless Body Area Network (WBAN) data to develop highly effective models. To support resource-constrained WBANs, we propose the integration of Drones-as-a-Service (DaaS) for on-demand data collection and model training. However, the growing number of WBAN users with varying 5G radio resources may cause interference and degrade system performance when transmitting data to Unmanned Aerial Vehicles (UAVs), hindering data sharing among independent UAVs. To address these challenges and enable privacy-preserving collaborative ML, we adopt Federated Learning (FL) framework, enabling independent UAV service providers to collaborate without sharing sensitive data. Furthermore, we aim to maximize the revenue of both WBANs, which contribute data, and UAVs, which perform model training. This requires careful resource allocation, considering minimum and maximum Physical Resource Block (PRB) requirements for transmitting critical and complete physiological data to UAVs underlying 5G networks. To tackle this complex problem, we propose an optimization framework that maximizes overall revenue while considering interference among WBANs. We apply stable matching and graph coloring-based heuristics to solve the problem efficiently. Extensive simulations and real-world data prototype demonstrate our proposed modelâs effectiveness, achieving an average revenue of 92.8% of the optimal value, outperforming existing state-of-the-art approaches.

Index Termsâ5G, graph coloring, healthcare, resource allocation, stable matching, UAV, WBAN.

## I. INTRODUCTION

W IRELESS Body Area Network (WBAN) usage inhealthcare has rapidly grown, with sensors placed on patients to collect physiological data for transmission to a Local Device (LD) [1]. These systems address resource scarcity in hospitals and facilitate remote health monitoring [2]. WBANs also enable the development of effective Machine Learning (ML) models using the abundant physiological data. Moreover, the growth of 5G network has led to the use of Unmanned Aerial Vehicles (UAVs) to address the complex WBAN infrastructure, leveraging their agility, flexibility, and mobility [3]. This growth is also reflected in the Drones-as-a-Service (DaaS) industry, where independent drone owners offer on-demand data collection and model training [3]. UAVs are typically categorized into two types: fixed-wing and rotary-wing UAVs [4]. Fixedwing UAVs provide high-speed flight capabilities while carrying heavy payloads, whereas rotary-wing UAVs, with limited velocity and payload capacity, are better suited for stationary communication applications [4]. UAVs play a crucial role in supporting resource-constrained WBANs, especially in outdoor events and remote areas, by collecting physiological data from WBANs and performing model training for applications, such as Human Activity Recognition (HAR) [5] and disease detection [6], [7].

To enhance the inference model, independent UAV companies can collaborate by sharing collected physiological data from WBANs for model training [3]. However, sharing data from multiple sources to a central server faces challenges due to limited network resources, resulting in data islands. To this end, we propose the adoption of a Federated Learning (FL) [8] approach to enable privacy-preserving collaborative ML across independently owned UAVs. This approach assists resourceconstrained WBANs with data collection and model training, ensuring privacy and communication efficiency through FL.

Typically, a model owner initiates an FL task to collect physiological data from WBAN users across different regions via rotary-wing UAVs for model training. Moreover, the model owner incentivizes WBANs to contribute their physiological data and UAVs to collect data from WBANs and perform model training. Specifically, WBANs aim to maximize their revenue by contributing data, while UAVs aim to maximize their revenue through model training within the model ownerâs maximum budget. To this end, we advocate using stable matching based Resource Allocation (RA) approach in UAV-assisted WBANbased FL framework where UAVs gather data from WBANs to train an FL model, with the help of a Macro Base Station (MBS) owned by the model owner, as shown in Fig. 1. However, this framework faces several challenges due to limited 5G radio resources, i.e., Physical Resource Blocks (PRBs),1 which affects the Quality of Service (QoS) in Healthcare Domain (HD) as can be seen in Table I [10], [11]. Moreover, there is a need to prioritize RA strategies based on the criticality of the data. For instance, patients with heart disease require continuous monitoring, where heart rate, blood pressure, and blood sugar level detection take priority over body temperature data. Hence, it is crucial to allocate minimal resources for transmitting critical data while allocating maximum resources to WBANs for transmitting complete data if the required resources are available. However, the growing number of WBANs with varying PRB demands for transmitting physiological data to UAVs may result in interference, presenting a unique challenge in 5G for real-time smart healthcare applications.

<!-- image-->  
Fig. 1. System architecture.

TABLE I  
QOS REQUIREMENT
<table><tr><td rowspan=1 colspan=1>Sensor type</td><td rowspan=1 colspan=1>Required throughput</td><td rowspan=1 colspan=1>Required PRBs</td></tr><tr><td rowspan=1 colspan=1>Blood saturation</td><td rowspan=1 colspan=1>16 bps</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Bodytemperature</td><td rowspan=1 colspan=1>120 bps</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>EEG</td><td rowspan=1 colspan=1>43.2 kbps</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>ECG</td><td rowspan=1 colspan=1>144kbps</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>Motion sensor</td><td rowspan=1 colspan=1>35kbps</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>Voice</td><td rowspan=1 colspan=1>100 kbps</td><td rowspan=1 colspan=1>4</td></tr></table>

Traditional UAV-based FL frameworks [3], [4], [12] primarily focus on enhancing the inference model, neglecting RA that considers UAVsâ revenue, network interference, and critical data transmission, altogether. Existing works [13], [14] address interference through effective channel allocation but arenât directly applicable to our proposed model. On the other hand, work in [15] focuses on improving the inference model through FL utilizing distributed healthcare data. In contrast, our current paper emphasizes on RA by considering interference, revenue, and prioritizing the transmission of critical patient data. Moreover, we formulate an optimization problem that maximizes revenue of WBANs and UAVs via RA, considering resource demands while minimizing interference among WBANs, altogether. Additionally, we propose an efficient sub-optimal solution based on stable matching [16], [17] and graph coloring approaches to solve the formulated revenue maximization problem while considering resource demands of WBANs. Finally, we convert the WBAN topology into an interference graph G V, E (see ( )Section IV-A), where nodes represent WBANs, and edges denote interference between WBANs, facilitating effective interference management. The main contributions of this work are summarized as:

TABLE II EXISTING WORKS
<table><tr><td rowspan=1 colspan=1>Problem Focus</td><td rowspan=1 colspan=1>FL</td><td rowspan=1 colspan=1>Energy</td><td rowspan=1 colspan=1>Revenue</td><td rowspan=1 colspan=1>RA</td><td rowspan=1 colspan=1>HD</td></tr><tr><td rowspan=1 colspan=1>FL via wireless network [18]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>FL convergence [19]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Decentralized FL [15]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>Location-basedFL [20]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>FL with UAV Swarm [12]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Transmissioncapacity[21]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Channel allocation [22]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Resource allocation [23]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Channel allocation [1]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Resource allocation [9]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Spectrum allocation [13]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Spectrum matching [14]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>Revenuemaximization[Proposed]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr></table>

- Propose a UAV-assisted WBAN-based FL framework2 where UAVs gather physiological data from WBANs and perform model training with the help of an MBS, to develop smart healthcare applications.

- Formulate an optimization problem that maximizes revenue of WBANs and UAVs via RA while considering minimum and maximum resource demand, as well as interference among WBANs in 5G, as an NP-hard problem.

- Solve the formulated problem efficiently using stable matching and graph coloring-based approaches in polynomial time complexity.

Simulation and prototype results on real-world data show the efficacy of the proposed model, achieving 92.8% of the optimal value.

The rest of the paper is organized as follows: Section II reviews the related works. The system model and the problem formulation are introduced in Sections III and IV, respectively. Proposed solution and analysis are given in Section V. Performance analysis is given in Section VI. Finally, Section VII provides conclusions and future works.

## II. RELATED WORK

This section presents the closely related works available in the literature along with a comparative analysis in Table II.

Authors in [18] proposed an FL framework that balances FL time, computation, communication latency, and energy consumption over wireless networks. Work in [19] optimized the number of global iterations under CPU, transmission delay, and model accuracy constraints. Work in [15] proposed a decentralized privacy-preserving FL framework for training effective models using distributed healthcare data. However, works [15], [18], [19] focused on optimizing the FL model without considering RA for data transmission. Work [20] proposed a locationbased FL model, utilizing re configurable intelligent surfaces to accurately determine the positions of computing nodes. However, this work did not consider computing energy or RA for data transmission. Y. Liu et al. [12] proposed an FL framework for UAV swarms that included joint training and RA to improve FL efficiency. However, this work did not consider PRB allocation and UAVsâ revenue, altogether, despite addressing the interference issues among users.

Work in [22] proposed a Channel Allocation Algorithm (CAA) for disaster communication relief systems using UAVs. This work used Stackelberg game to derive a channel allocation strategy, considering mutual interference of users to improve network throughput. R. Duan et al. [21] proposed a Suboptimal Subchannel Assignment Algorithm (SSAA) to maximize system capacity by jointly optimizing sub-channel assignment, IoT node uplink transmit power, and UAV flying height. K-means clustering was employed to group IoT nodes into subsystems corresponding to the number of UAVs, and subchannels were assigned to each subsystem using an efficient many-to-many matching algorithm. Work [23] proposed a joint RA problem to minimize energy consumption for mobile devices and UAVs, considering the limited resources of UAVs and task delay. However, works [21], [22], [23] mainly focused on RA without considering the revenue for providing resources.

To address the issue of limited channels, work [1] used graph coloring-based approach to minimize interference among WBANs through channel re-usability. However, this work allocated a single channel to each WBAN without considering criticality of data. Work [9] used matching theory for RA in 5G networks based on service class. Moreover, works [13], [14] studied the need for minimum resource requirements using matching theory. Work [13] proposed a matching theory-based approach for spectrum re-usability, considering minimum and maximum demand of buyers. However, it cannot be applied directly to our proposed model since it did not consider FL in UAV-assisted WBANs.

To the best of our knowledge, none of the existing works has considered prioritizing critical patient data and the revenues of both WBANs and UAVs through RA while considering resource demands and minimizing interference among WBANs, altogether. Unlike existing works, we proposed a UAV-assisted WBAN-based FL framework that considers the revenues of both WBANs and UAVs through RA while considering resource demands and minimizing interference among WBANs, altogether.

## III. SYSTEM MODEL

We consider a healthcare system, where a model owner wishes to collect data from a set of WBANs denoted by $\mathbb { K } = \{ 1 , \dots , k , \dots , K \}$ using UAVs presented by U $\{ 1 , \ldots , u , \ldots , U \}$ =for model training, such as for HAR [5] and 1disease detection [6], as shown in Fig. 1. Moreover, symbol descriptions are given in Table III. Let $\mathbb { S } = \{ 1 , \dots , s , \dots , S \}$ = 1be the set of sensors in a WBAN to capture physiological data and send it to an LD using either Bluetooth - an IEEE 802.15.1 standard designed for short-range wireless communication with a focus on security and low power consumption, or ZigBee - an IEEE 802.15.4 standard intended for use in sensor and control applications due to its low power consumption.3 Moreover, we assume that WBANs are equipped with 5G communication capability, and the transmission of health data from WBANs to UAVs occurs through a high-speed 5G network. After collecting the data, UAVs return to the UAV base for FL model training with the help of MBS.4 However, any two WBANs may interfere with each other during data transmission to UAV, causing packet collision and data loss [1]. To avoid interference, the MBS allocates PRBs to WBANs, considering various parameters, as discussed in the following.

TABLE III DESCRIPTION OF SYMBOLS
<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $\dot { \overline { { \mathbb { K } , \mathbb { U } , \mathbb { N } , \mathbb { S } } } }$  S  $\zeta _ { l , s } , \zeta _ { \mathrm { u } , s }$   $\mathcal { T } _ { k } ^ { s } , \nu _ { k } ^ { s }$   $x _ { s }$   $\varphi _ { k } , T _ { k } ^ { s }$   $\dot { \mathcal { E } } _ { s } ^ { } , \mathcal { E } _ { c } ^ { t r a i t }$   $Y , Z ^ { ^ { \circ } }$   $\operatorname { T } _ { s f } , \mathfrak { u }$   $D _ { k } ^ { m i n } , D _ { k } ^ { m a x }$   $y _ { k , u } ^ { n ^ { * } } , B$   $F _ { u } ( w ) , A , I$   $c _ { u } , \Phi _ { u }$   $\beta _ { u }$   $T _ { k , u } , \mathcal { E } _ { k , u }$   $\epsilon _ { k }$   $r _ { k , u } ^ { n }$   $\Gamma _ { l . } ^ { n } , \mathcal { E } _ { l . } ^ { i n i t }$   $\mathbb { R } _ { k , u } , \Delta$  K  $\Re _ { k } , \Pi _ { k , u }$   $\pi _ { k } , \mathcal { E } _ { k , \ i }$   $\vartheta _ { u _ { . } } ^ { t v e } , \mathrm { p } _ { u }$   $c _ { u } ^ { p d }$   $c _ { u } ^ { r d }$   $v _ { u } , \mathrm { L } _ { u }$   $P _ { k } , P _ { c i r }$   $\mathrm { E } _ { u . k } ^ { c o m }$   $\mathrm { E } _ { u } ^ { t v e } , \mathrm { E } _ { u , k } ^ { r e c } , \mathrm { E } _ { u } ^ { t o t }$   $\tau _ { u } ^ { t n t } , \psi$   $\mathbb { E } _ { u } ^ { c o m } , \mathrm { E } _ { u } ^ { t n e }$  0  $\eta _ { u } , H$ </td><td>Sets of WBANs,UAVs,PRBs,and sor Physiological data of sensor s on WBAN user k Lower &amp; upper limit of the physiological data Health severity indexand criticality index Medical criticality of sensed data by sensor s Priority parameter and required throughput Initial energy &amp; energy consumption of sensor s Number of sub-carriers and symbols per PRB Frame duration and efficiency in bits/symbol Minimum and maximum no.of required PRBs Binary variable and bandwidth of a PRB Loss function,accuracy &amp; no.of global iterations Computation capacity&amp;coverage area of UAV CPU cycles per one sample data of UAV u Transmission time and energy of WBAN Size of physiological data to be transmitted Transmission rate of a WBAN using nth PRB SINR and initial energy of a WBAN Transmission rate and total revenue of all WBANs RewardandrevenueofWBAN Transmission and unit cost of energy of WBAN Traversal time and propulsion power of UAV u Power to balance skin friction parasitic drag Power to balance redirection drag force of air Velocityof UAVand distance travelledbyUAV Transmit power &amp; circuit&#x27;s power consumption Energy consumption of UAV for model training Traversal, receiving and total energy of UAV u Model transmission time &amp; effective capacitance Model computation and transmission energy Time to send a unit data across a unit distance Transmit power of UAV and local model size Unit data price &amp; distance from UAV base to MBS Physiological data transmitted by WBAN k</td></tr></table>

## A. Health Severity Index

Heterogeneous physiological data collected by various medical sensors vary and can be classified into priority classes according to IEEE 802.15.6 standard [27]. It is a short-range wireless communication standard that operates in Industrial, Scientific, and Medical (ISM) bands, as well as other frequency bands, to support applications such as health monitoring and sports. Let $\zeta _ { k } ^ { s }$ be the health parameter sensed by physiological sensor s on WBAN $k ,$ and $\zeta _ { l , s }$ and $\zeta _ { \mathrm { u } , s }$ be the lower and the upper bounds of the health parameter under normal condition for a healthy person. Then, health severity index [24] of sensor sâs data collected from WBAN k can be defined as follows:

$$
\mathcal { T } _ { k } ^ { s } = \left| \frac { ( \zeta _ { \mathrm { u } , s } - \zeta _ { k } ^ { s } ) ^ { 2 } - ( \zeta _ { k } ^ { s } - \zeta _ { l , s } ) ^ { 2 } } { ( | \zeta _ { \mathrm { u } , s } | + | \zeta _ { l , s } | ) ^ { 2 } } \right| .\tag{1}
$$

Following our previous work [28], we define criticality index $\nu _ { k } ^ { s }$ of sensor sâs data from WBAN k as follows:

$$
\begin{array} { r } { \nu _ { k } ^ { s } = x _ { s } \mathcal { L } _ { k } ^ { s } , } \end{array}\tag{2}
$$

where $x _ { s }$ is the medical criticality of the data collected by sensor s. As a result, the criticality of WBAN k is defined as the sum of the criticality index of all sensors, as follows:

$$
\rho _ { k } = \sum _ { s \in \mathbb { S } } \nu _ { k } ^ { s } ,\tag{3}
$$

where $\rho _ { k } \in [ 0 , \infty )$ ; however, we normalized it between 0 and $1 , \mathrm { i . e . , 0 } \leq \rho _ { k } \leq 1$ ), according to our previous work [28].

## B. Required PRBs for Data Transmission

Let WBAN k requires a throughput of $\mathcal { T } _ { k } ^ { s }$ to transmit physiological data collected by sensor s to UAV via Orthogonal Frequency-Division Multiple Access (OFDMA) technique. Then, the relation between the required number of PRBs $D _ { k } ^ { s }$ and the throughput $\mathcal { T } _ { k } ^ { s }$ is given as [29]:

$$
D _ { k } ^ { s } = \lceil T _ { k } ^ { s } / ( \Psi \cdot \mathfrak { u } ) \rceil ,\tag{4}
$$

where u denotes efficiency in bits/symbol of the used modulation and coding scheme and $\Psi = ( Y Z ) / \mathrm { T } _ { s f }$ , depends on network Î¨ = ( ) Tconfiguration. Y and Z represent number of sub-carriers and symbols per PRB, respectively; and $\operatorname { T } _ { s f }$ is frame duration. Here, $\mathrm { T } _ { s f } = 0 . 5 \ : m s , Z = 7$ and $Y = 1 2 [ 2 9 ]$

= 0 5 = = 12To ensure successful physiological data transmission, WBANs have minimum and maximum PRB demands, where the minimum demand ensures the successful transmission of critical data, and the maximum demand guarantees the transmission of all data. The minimum PRB demand $( D _ { k } ^ { m i n } )$ for WBAN k is computed as the sum of required PRBs for transmitting each sensor $s \mathrm { ^ { \circ } s }$ data with a criticality index $\nu _ { k } ^ { s }$ exceeding the threshold value $\nu _ { t h }$ , while the maximum PRB demand $( D _ { k } ^ { m a x } )$ represents total required PRBs for transmitting all data of WBAN k, as:

$$
\left\{ \begin{array} { l l } { D _ { k } ^ { m i n } = \sum _ { s \in \mathbb { S } , \nu _ { k } ^ { s } \geq \nu _ { t h } } D _ { k } ^ { s } . } \\ { D _ { k } ^ { m a x } = \sum _ { s \in \mathbb { S } } D _ { k } ^ { s } . } \end{array} \right.\tag{5}
$$

For instance, let WBAN k is equipped with blood saturation, body temperature, and EEG sensors, with criticality indices for the health data collected by them being 0.7, 0.6, and 0.3, respectively. Further, let the threshold value $\nu _ { t h }$ be $0 . 5$ for classifying critical data from normal data. In this scenario, Dmink for WBAN k is determined to be 2 (based on Table I), i.e., the sum of the required PRBs for transmitting blood saturation and body temperature sensorsâ data. Meanwhile, $D _ { k } ^ { m a x }$ for WBAN k becomes 4, i.e., the total required PRBs for transmitting all the three sensorsâ data.

<!-- image-->  
Fig. 2. WBAN topology and interference graph.

## C. PRB Allocation Model

Let $\mathbb { N } = \{ 1 , \dots , n , \dots , N \}$ be the set of the available PRBs = 1in 5G network. Further, we introduce a binary variable that shows PRB allocation relation between WBAN and UAV as:

$$
y _ { k , u } ^ { n } = { \left\{ \begin{array} { l l } { 1 , } & { { \mathrm { i f } } n ^ { t h } { \mathrm { P R B ~ i s ~ a l l o c a t e d ~ t o } } ( k , u ) , } \\ { 0 , } & { { \mathrm { o t h e r w i s e . } } } \end{array} \right. }\tag{6}
$$

Each UAV has a coverage area, that can also be considered as UAVâs transmission range, and it is possible for two coverage areas to overlap. Let $\Phi _ { u }$ be the set of all WBANs within the Î¦coverage area of UAV u. Interference among the WBANs can occur in the network if: (i) same PRB is assigned to two WBANs k and $k ^ { \prime }$ that are within the coverage area of a UAV, or (ii) same PRB is allocated to two WBANs, where one is in the coverage areas of both u and $u ^ { \prime }$ and the other is in the non-overlapping area of either u or $u ^ { \prime } .$ , as shown in Fig. 2. However, the above conditions could be avoided using the following constraints for a given $n ^ { \mathrm { t h } }$ PRB:

$$
\begin{array} { r l } & { \left( C _ { 1 } \right) \mathrm { E n s u r e } \sum _ { k \in \Phi _ { u } } y _ { k , u } ^ { n } \leq 1 , \forall u \in \mathbb { U } . } \\ & { \left( C _ { 2 } \right) \mathrm { E n s u r e } y _ { k , u } ^ { n } + y _ { k ^ { \prime } , u ^ { \prime } } ^ { n } \leq 1 , \forall k \in \Phi _ { u } \cap \Phi _ { u ^ { \prime } } , \mathrm { a n d } \forall k ^ { \prime } \in \Phi } \\ & { \quad \Phi _ { u } - \Phi _ { u ^ { \prime } } , \forall u , u ^ { \prime } \in \mathbb { U } . } \end{array}
$$

In other words, the interference can be avoided if no two WBANs within a coverage area of a UAV are allocated the same PRB, as stated above in $( C _ { 1 } )$ . Further, the interference can be avoided if we ensure that a given PRB is allocated only to one of the interfering WBANs, as stated in $\left( C _ { 2 } \right)$

## D. Energy Consumption of WBAN

To facilitate the data transmission, the required number of PRBs must be allocated to WBANs. The data rate between WBAN k and UAV u using $n ^ { \mathrm { t h } }$ PRB is given as follows [9]:

$$
r _ { k , u } ^ { n } = B \ \log _ { 2 } \left( 1 + \Gamma _ { k , u } ^ { n } \right) ,\tag{7}
$$

where B and $\Gamma _ { k , u } ^ { n }$ are bandwidth of a PRB and Signal-to-Interference-plus-Noise Ratio (SINR)5 between WBAN k and UAV u, respectively. Then, the achievable data rate between WBAN k and UAV u is given as follows:

$$
\mathbb { R } _ { k , u } = \sum _ { n \in \mathbb { N } } y _ { k , u } ^ { n } r _ { k , u } ^ { n } .\tag{8}
$$

Thus, transmission time between WBAN k and UAV u can be defined as follows [26]:

$$
T _ { k , u } = \frac { \epsilon _ { k } } { \mathbb { R } _ { k , u } } ,\tag{9}
$$

where $\epsilon _ { k }$ is the size of physiological data to be transmitted by WBAN k. Thus, energy consumed by WBAN k for transmitting physiological data to UAV u is defined as follows:

$$
\mathcal { E } _ { k , u } = P _ { k } T _ { k , u } ,\tag{10}
$$

where $P _ { k }$ is the transmit power of WBAN k.

To prioritize the transmission of critical data, a priority parameter $\varphi _ { k }$ is introduced, which characterizes the criticality of physiological data and the energy consumption rate of the WBAN. Mathematically, the priority parameter $\varphi _ { k }$ is defined as the weighted average of the criticality index and the energy consumption of WBAN k, as follows [24]:

$$
\varphi _ { k } = \frac { \lambda _ { 1 } \rho _ { k } + \lambda _ { 2 } E _ { k } } { \lambda _ { 1 } + \lambda _ { 2 } } ,\tag{11}
$$

where $\begin{array} { r } { E _ { k } = \sum _ { u \in \mathbb { U } } \mathcal { E } _ { k , u } / \mathcal { E } _ { k } ^ { i n i t } } \end{array}$ , and $\mathcal { E } _ { k } ^ { i n i t }$ is the initial energy of WBAN k [24], and $\lambda _ { 1 }$ and $\lambda _ { 2 }$ are positive weights; and $\lambda _ { 1 } +$ $\lambda _ { 2 } = 1$ . The value of $\varphi _ { k }$ lies between 0 and 1, i.e., $0 \leq \varphi _ { k } \leq 1$ = 1A higher value of $\varphi _ { k }$ 0 1indicates that physiological data of WBAN k is highly critical, and vice versa.

## E. Revenue of WBAN

Model owner provides reward to WBAN for transmitting physiological data to UAV based on the number of physiological data samples. Let $d _ { k }$ be the number of physiological data samples available at WBAN k, then, the reward of WBAN k from the model owner is defined as follows [30]:

$$
\Re _ { k } = \chi d _ { k } ,\tag{12}
$$

where $\chi$ is the price per physiological data sample. Thus, the revenue of WBAN k for transmitting physiological data to UAV u is defined as follows:

$$
\Pi _ { k , u } = \Re _ { k } - \pi _ { k } \mathcal { E } _ { k , u } ,\tag{13}
$$

where $\pi _ { k }$ represents the unit cost of energy for a WBAN. Therefore, total revenue of all WBANs is defined as follows:

$$
\Delta = \sum _ { k \in \mathbb { K } } \sum _ { u \in \mathbb { U } } \Pi _ { k , u } .\tag{14}
$$

## F. UAV Data Collection

UAVs are tasked by the model owner to collect physiological data from WBANs. Subsequently, UAVs travel to a predetermined position in the region6 assigned by the model owner with velocity $\mathrm { v } _ { u } ,$ and spend a fixed propulsion power, given by: $\begin{array} { r } { \mathrm { p } _ { u } = c _ { u } ^ { p d } ( \mathrm { v } _ { u } ) ^ { 3 } + \frac { c _ { u } ^ { r d } } { \mathrm { v } _ { u } } } \end{array}$ , where $c _ { u } ^ { p d }$ represents power to balance skin friction parasitic drag, and $c _ { u } ^ { r d }$ represents power to balance redirection drag force of air7 [3]. Let $\mathrm { L } _ { u }$ be the distance travelled Lby UAV u from its base to the assigned region, known as traversal distance, then, the time taken by the UAV for traversal is given by: $\begin{array} { r } { \vartheta _ { u } ^ { t v e } = \frac { \mathrm { L } _ { u } } { \mathrm { v } _ { u } } } \end{array}$ . Thus, the energy consumption of UAV u during traversal is given by:

$$
\begin{array} { r } { \mathrm { E } _ { u } ^ { t v e } = \mathrm { p } _ { u } \vartheta _ { u } ^ { t v e } . } \end{array}\tag{15}
$$

After reaching the assigned region, UAVs receive physiological data from WBANs within their coverage area. The energy consumed by UAV u while receiving8 physiological data of WBAN k is calculated as follows [33]:

$$
\mathrm { E } _ { u , k } ^ { r e c } = \frac { \mathbb { R } _ { k , u } } { \varsigma P _ { k } + P _ { c i r } } ,\tag{16}
$$

where $P _ { c i r }$ represents the circuitâs power consumption, including the power consumption of the mixer, frequency synthesizer, and digital-to-analog converter. Ï >  is a constant that depends on the efficiency of the power amplifier [33]. Thus, the total energy consumption of UAV u for traversal and receiving physiological data is defined as follows:

$$
\mathrm { E } _ { u } ^ { t o t } = \mathrm { E } _ { u } ^ { t v e } + \sum _ { k \in \mathbb { K } } \mathrm { E } _ { u , k } ^ { r e c } .\tag{17}
$$

## G. UAV Model Training

After receiving physiological data from WBANs, UAVs return to the UAV base9 and collaboratively train an FL model [3]. Let vector $\mathbf { \Delta } _ { w } ( i )$ be the parameter of the FL model at global iteration i. In each global iteration, there are three steps involved [3], [4], [20]: (i) Local Model Training: UAV trains the local model using global parameter $\mathbf { \Delta } _ { w } ( i )$ , (ii) Local Model Transmission: UAV transmits the model parameter10 to the MBS, and (iii) Global Model Aggregation: MBS aggregates all parameters from UAVs to get a global model parameter $\mathbf { \Delta } w ^ { ( i + 1 ) }$ , which is then transmitted back to the UAVs for the i th global ( + 1)iteration. In general, each UAV solves the local optimization problem $G _ { u }$ given in the following:

$$
\operatorname* { m i n } _ { \boldsymbol { h } _ { u } \in \mathbb { R } ^ { d } } G _ { u } \left( \boldsymbol { w } ^ { ( i ) } , \boldsymbol { h } _ { u } \right) \triangleq F _ { u } \left( \boldsymbol { w } ^ { ( i ) } + \boldsymbol { h } _ { u } \right)
$$

$$
- \nabla F _ { u } \left( { \pmb w } ^ { ( i ) } \right) - \xi \nabla F _ { u } \left( { \pmb w } ^ { ( i ) } \right) ^ { T } { \pmb h } _ { u } ,\tag{18}
$$

where $\xi$ is a constant value. A solution $h _ { u }$ to (18) denotes the difference between the global model at the MBS and the local model at UAV u, i.e., the local model parameter at UAV u is $( { \pmb w } ^ { ( i ) } + { \pmb h } _ { u } )$ [36]. Each UAV performs local model training ( + )multiple times to minimize L-Lipschitz and Î³-strong convex loss function $G _ { u }$ to achieve target training accuracy A, which is defined by the model owner. A higher value of target accuracy A indicates a greater deviation from the optimal solution. The optimization problem at UAV required $v \log _ { 2 } ( 1 / \mathcal { A } )$ local log (1 )iterations for model training to achieve local accuracy of A [3]. After $\textstyle I = { \frac { \mathfrak { a } } { 1 - { \mathcal { A } } } }$ global iterations, the entire FL model training process is completed. Here, $\begin{array} { r } { \mathfrak { a } = \frac { 2 L ^ { 2 } } { \gamma ^ { 2 } \varepsilon } } \end{array}$ and Îµ is a very small value that satisfies the following constraint: $\begin{array} { r } { 0 \le \varepsilon \le \frac { \gamma } { L } } \end{array}$ . Let $c _ { u }$ and $\beta _ { u }$ 0be the computation capacity (CPU cycles per second) of UAV u and the CPU cycles per bit for computing one data sample at UAV u, respectively. Then, the energy consumption of UAV u for local model training using WBAN kâs data is defined as follows [3]:

$$
\begin{array} { r } { \mathrm { E } _ { u , k } ^ { c o m } = I \left( \psi \beta _ { u } v \log _ { 2 } ( 1 / \mathcal { A } ) c _ { u } ^ { 2 } \right) d _ { k } , } \end{array}\tag{19}
$$

where $\psi$ is the effective capacitance that depends on the chip architecture [36], and $\begin{array} { r } { v = \frac { 2 } { ( 2 - L \delta ) \delta \gamma } } \end{array}$ , where Î´ is the step size of =model training. Thus, the energy consumption of UAV u for local model training is as follows:

$$
\mathbb { E } _ { u } ^ { c o m } = \sum _ { k \in \mathbb { K } } \sum _ { n \in \mathbb { N } } y _ { k , u } ^ { n } \ : \mathrm { E } _ { u , k } ^ { c o m } .\tag{20}
$$

## H. UAV Model Transmission

After model training, UAV transmits its model parameter to MBS for aggregation [3]. The transmission time of UAV to transmit its model parameter of size H is as follows [26]:

$$
\begin{array} { r } { \tau _ { u } ^ { t n t } = \sigma I H l _ { u } , } \end{array}\tag{21}
$$

where Ï is the transmission time to send one data unit across a unit distance, and $l _ { u }$ is the distance between the UAV base and the MBS. The size of local model remains constant, independent of the number of global iterations or the quantity of data. Then, the transmission energy of a UAV with transmit power of $\eta _ { u }$ is defined as follows [3]:

$$
E _ { u } ^ { t n e } = \eta _ { u } \tau _ { u } ^ { t n t } .\tag{22}
$$

## I. Revenue of UAV

WBANsâ physiological data collected by UAVs help the MBS develop a better inference model. Specifically, the modelâs accuracy in inference time is improved when the number of data samples increases, i.e., an FL model accuracy increases when the model is trained using a wide range of physiological data collected from WBANs. Inspired by [3], [20], [30], the reward function for UAVs in FL model training is defined based on the collected physiological data from WBAN k and its criticality, as given below:

$$
\mathcal { R } _ { k } = \ln ( 1 + d _ { k } + \varphi _ { k } ) .\tag{23}
$$

Thus, the total reward of a UAV u is given as follows:

$$
\mathrm { R } _ { u } = \alpha _ { u } \sum _ { k \in \mathbb { K } } \sum _ { n \in \mathbb { N } } y _ { k , u } ^ { n } \mathcal { R } _ { k } ,\tag{24}
$$

where $\alpha _ { u }$ is the non-zero positive number [30]. Thus, the revenue of a UAV u is defined as follows:

$$
\Omega _ { u } = \mathrm { R } _ { u } - \phi _ { u } ( \mathrm { E } _ { u } ^ { t o t } + \mathbb { E } _ { u } ^ { c o m } + E _ { u } ^ { t n e } ) ,\tag{25}
$$

where $\phi _ { u }$ represents the unit cost of energy for UAV. Therefore, the total revenue of all UAVs is defined as follows:

$$
\Lambda = \sum _ { u \in \mathbb { U } } \Omega _ { u } .\tag{26}
$$

## IV. PROBLEM FORMULATION

In the proposed architecture, WBANs get rewarded by the MBS based on the number of physiological data samples they transmit. Moreover, UAVs also aim to maximize their revenue by participating in FL training. Therefore, we define the total revenue as a linear combination of the revenues of WBANs and UAVs, as follows:

$$
\mathcal { U } = \Delta + \Lambda .\tag{27}
$$

Thus, this paper aims to maximize system revenue by allocating PRBs to WBANs for transmitting physiological data while minimizing interference and considering the priority of data. However, the total revenue of WBANs and UAVs should not exceed the model ownerâs maximum budget M. Therefore, the objective of the system is given as follows:

$$
\mathbf { P } : \operatorname* { m a x } _ { \boldsymbol { y } _ { k , u } ^ { n } } \quad \boldsymbol { \mathcal { U } } ,\tag{28}
$$

Subject to the constraints:

$$
\Pi _ { k , u } \ge 0 , \Omega _ { u } \ge 0 ,\tag{28a}
$$

$$
\sum _ { k \in \mathbb { K } } \sum _ { u \in \mathbb { U } } \sum _ { n \in \mathbb { N } } y _ { k , u } ^ { n } \left( \mathfrak { R } _ { k } + \mathrm { R } _ { u } \right) \leq \mathcal { M } ,\tag{28b}
$$

$$
D _ { k } ^ { m i n } \leq \sum _ { n \in \mathbb { N } } y _ { k , u } ^ { n } \leq D _ { k } ^ { m a x } ,\tag{28c}
$$

$$
\sum _ { k \in \Phi _ { u } } y _ { k , u } ^ { n } \leq 1 ,\tag{28d}
$$

$$
y _ { k , u } ^ { n } + y _ { k ^ { \prime } , u ^ { \prime } } ^ { n } \leq 1 , \forall k \in \Phi _ { u } \cap \Phi _ { u ^ { \prime } } , \forall k ^ { \prime } \in \Phi _ { u } - \Phi _ { u ^ { \prime } } ,
$$

$$
y _ { k , u } ^ { n } \in \{ 0 , 1 \} ,\tag{28e}
$$

(28f)

âk, $k ^ { \prime } \in \mathbb { K } , u \in \mathbb { U } , n \in \mathbb { N }$ . Constraint (28a) states that the revenue of WBANs and UAVs must be non-negative. Constraint (28b) tells that the total reward given to WBANs and UAVs should not exceed the maximum budget of model owner. Constraint (28c) ensures minimum and maximum required PRBs for a WBAN. Constraints (28d) and (28e) hold the interference criteria described $\left( C _ { 1 } \right)$ and $\left( C _ { 2 } \right)$ of Section III-C, respectively. ( ) ( )Constraint (28f) is binary variable given in (6).

The objective of the proposed problem P is computationally hard to solve. However, constraint (28d) allows us to construct an interference graph, that MBS uses to allocate PRBs across different WBANs without causing interference. Moreover, Fig. 3 shows the data flow between WBAN, UAV, and MBS. Labels 1, 2, 3, 5, 7, and 9 are handled by control signals (e.g., beacons [9]). However, labels 4, 6, and 8 are handled by data signals. The formulated problem P can be considered as a graph coloring problem by mapping PRB with color in graph topology as described in the following.

<!-- image-->  
Fig. 3. Data flow diagram.

TABLE IV  
Îº-COLORING & RA
<table><tr><td rowspan=1 colspan=1>Vertexcoloring</td><td rowspan=1 colspan=1>RA</td></tr><tr><td rowspan=1 colspan=1>Set of K colors</td><td rowspan=1 colspan=1>Set ofNPRBs</td></tr><tr><td rowspan=1 colspan=1>Set ofVvertices</td><td rowspan=1 colspan=1>Set ofKWBANs</td></tr><tr><td rowspan=1 colspan=1>Set of Eedges</td><td rowspan=1 colspan=1>Interference constraints</td></tr><tr><td rowspan=1 colspan=1>Graph G</td><td rowspan=1 colspan=1>WBAN topology</td></tr></table>

## A. Interference Graph Construction

We create an interference graph G V, E from the WBAN topology where vertex $v \in V$ ( )and edge e â E represent WBANs and interference between two WBANs, respectively. In other words, any two interfering WBANs have an edge between them in the graph G. The graph G satisfies the constraints in (28d) and (28e). Fig. 2 shows a WBAN topology and the respective interference graph. Moreover, we assume that MBS maintains the interference graph.

Theorem 1: Formulated maximization problem P is NP-hard.

Proof: We map the graph Îº-coloring problem to the formulated problem P, where Îº is the total number of colors. For simplicity, we consider $D _ { k } ^ { m i n } = D _ { k } ^ { m a x } = 1$ and ignore the = = 1constraints (28a)-(28c) to prove the hardness of the problem.

- Map the set of Îº-colors to N PRBs.

- Map the set of V vertices to K WBANs.

- Map the set of E edges to interference constraints.

- Map the interference graph to the WBAN topology.

Table IV shows the mapping of the RA problem to the vertex Îº-coloring, which is NP-complete [37], implying the formulated problem P is an NP-hard.

Due to the high dimensionality and ill-posed nature of problem P, we aim to solve the formulated problem via RA in UAVassisted WBANs underlying 5G. We applied a matching and graph coloring-based approach to solve the formulated problem in computationally feasible time while satisfying the varying PRB demand, limited PRBs, and a large number of WBANs within the coverage area of UAVs.

## V. MATCHING AND GRAPH COLORING BASED RA

The conventional matching theory of buyer/seller is not applicable in the WBAN scenario. Buyers and sellers express their preferences for various sellers and buyers based on a preference list that is reflexive, complete, and transitive in relation. However, the preference list defined for buyer/seller is not sufficient for RA in WBAN-based scenarios due to the reusability of PRBs [13], [17]. To address this problem, we use the concept of the preference list of WBANs over UAV-PRB pairs, and vice-versa. Intuitively, WBAN prefers a UAV-PRB pair with the highest transmission rate. Thus, the preference list of WBAN k over UAV u using PRB n is constructed based on the data transmission rate. Let P be the set of UAV-PRB pairs denoted as $\mathcal { P } = \{ ( u , n ) | \forall u \in \mathbb { U } , \forall n \in \mathbb { N } \}$ . In the rest of the paper, we use $p _ { u } ^ { n }$ = ( )to denote u, n pair for simplicity. Then, the preference ( )list of WBAN k can be expressed as follows:

$$
p _ { u } ^ { n } \succeq _ { k } p _ { u ^ { \prime } } ^ { n } \Leftrightarrow r _ { k , u } ^ { n } \geq r _ { k , u ^ { \prime } } ^ { n } .\tag{29}
$$

We assume that the PRB related information is available to MBS, and the functionality of PRB is monitored by MBS [9].

On the other hand, UAVs always consider the revenue when selecting WBANs to match. If $\mathbb { P } , \mathbb { Q } \subseteq \mathbb { K }$ denote two subsets of WBANs, then UAV-PRB pair $p _ { u } ^ { n }$ prefers $\mathbb { P }$ to Q if: I Total revenue for collection of data from WBANs in group $\mathbb { P }$ )is larger than that of group Q, and P contains only non-interfering WBANs, or II P contains only non-interfering WBANs but ( )Q does not, as defined below:

$$
\mathbb { P } \succeq _ { p _ { u } ^ { n } } \mathbb { Q } \Leftrightarrow \left\{ \begin{array} { r l } { ( I ) \forall k , k ^ { \prime } \in \mathbb { P } , e _ { k , k ^ { \prime } } = 0 , \forall k , k ^ { \prime } \in \mathbb { Q } , e _ { k , k ^ { \prime } } = } & { } \\ { 0 , \sum _ { k \in \mathbb { P } } \{ \mathcal { R } _ { k } - \phi _ { u } ( \mathrm { E } _ { u , k } ^ { r e c } + \mathrm { E } _ { u , k } ^ { c o m } ) \} \geq } & { } \\ { \sum _ { k \in \mathbb { Q } } \{ \mathcal { R } _ { k } - \phi _ { u } ( \mathrm { E } _ { u , k } ^ { r e c } + \mathrm { E } _ { u , k } ^ { c o m } ) \} ; } & { } \\ { ( I I ) \exists k , k ^ { \prime } \in \mathbb { Q } , e _ { k , k ^ { \prime } } = 1 , \mathrm { ~ o t h e r w i s e } , } \end{array} \right.\tag{30}
$$

where $e _ { k , k ^ { \prime } } = 1$ indicates the edge between WBANs k and k in the graph $G ,$ 1 which means WBANs k and $k ^ { \prime }$ are interfering with each other. Contrary, if $e _ { k , k ^ { \prime } } = 0$ , there is no edge between = 0WBANs k and k in the graph G, which means they are noninterfering WBANs. Note that MBS maintains the preference list of UAV-PRB pairs. Based on the above discussion, we define matching in the following.

Definition 1: A feasible resource matching Î¼ is defined as a function, i.e., $\mu : \mathbb { K } \cup ( \mathbb { U } \times \mathbb { N } )  2 ^ { \mathbb { K } } \cup 2 ^ { \mathbb { U } \times \mathbb { N } }$ such that:

I) $\forall p _ { u } ^ { n } \in \mathcal { P } , \mu ( p _ { u } ^ { n } ) \subseteq \mathbb { K }$ )and $\forall k \in \mathbb { K } , \mu ( k ) \subseteq \mathcal { P }$

II) $\forall p _ { u } ^ { n } \in \mathcal { P }$ (and $\forall k \in \mathbb { K } , p _ { u } ^ { n } \in \mu ( k ) \Leftrightarrow k \in \mu ( p _ { u } ^ { n } )$

III) Interference constraint: $\forall k , k ^ { \prime } \in \mu ( p _ { u } ^ { n } ) , e _ { k , k ^ { \prime } } = 0 .$

IV) $\forall k \in \mathbb { K } , D _ { k } ^ { m i n } \leq | \mu ( k ) | \leq D _ { k } ^ { m a x }$

## A. Resource Allocation Algorithm

Each WBAN requires a minimum allocation of PRBs to prioritize critical data transmission. To facilitate this, each WBAN is divided into two dummy WBANs - steady and elaborate. Steady and elaborate WBANs handle the minimum and the maximum requirements, respectively. Let $k ^ { s }$ and $k ^ { e }$ be steady and elaborate WBANs of WBAN k, respectively, then, we transform the minimum requirement into maximum requirements of steady and elaborate WBANs such as $D _ { k ^ { s } } ^ { m a x } = D _ { k } ^ { m i n }$

$$
\begin{array} { r } { \overline { { \succeq _ { k } , \forall k \in \mathbb { K } } } , } \end{array}
$$

$$
\begin{array} { r } { \sum _ { p _ { u } ^ { n } } , \forall p _ { u } ^ { n } \in \mathcal { P } , D _ { k } ^ { m i n } , D _ { k } ^ { m a x } , \forall k \in \mathbb { K } , G ( V , E ) . } \end{array}
$$

$$
\succeq _ { k } , \forall k \in \hat { \mathbb { K } } .
$$

$$
\subseteq _ { p _ { u } ^ { n } } , \forall p _ { u } ^ { n } \in \mathcal { P } .
$$

$$
\hat { D } _ { k } ^ { m a x } ,
$$

$$
\forall k \in { \hat { \mathbb { K } } } .
$$

$$
\hat { G } ( \hat { V } , \hat { E } )
$$

$$
1 \colon \hat { \mathbb { K } } ^ { s } = \phi , \hat { \mathbb { K } } ^ { e } = \phi
$$

$$
a l l k \in \mathbb { K }
$$

$$
\hat { \mathbb { K } } ^ { s } = \hat { \mathbb { K } } ^ { s } \cup \{ k ^ { s } \} , \hat { \mathbb { K } } ^ { e } = \hat { \mathbb { K } } ^ { e } \cup \{ k ^ { e } \}
$$

$$
D _ { k ^ { s } } ^ { m a x } = D _ { k } ^ {  } , D _ { k ^ { e } } ^ { m a x } = D _ { k } ^ { m a x } - D _ { k } ^ { m i n }
$$

$$
\succeq _ { k ^ { s } } : = \succeq _ { k ^ { e } } : = \succeq _ { k }
$$

$$
6 \colon \hat { \mathbb { K } } = \hat { \mathbb { K } } ^ { s } \cup \hat { \mathbb { K } } ^ { e }
$$

$$
p _ { u } ^ { n } \in \mathcal { P }
$$

$$
\succeq _ { p _ { u } ^ { n } } : = k _ { p _ { u } ^ { n } , 1 } \succeq _ { p _ { u } ^ { n } } k _ { p _ { u } ^ { n } , 2 } \succeq _ { p _ { u } ^ { n } } \cdot \cdot \cdot ,
$$

$$
\hat { \succeq } _ { p _ { u } ^ { n } } : = k _ { p _ { u } ^ { n } , 1 } ^ { s } \hat { \succeq } _ { p _ { u } ^ { n } } k _ { p _ { u } ^ { n } , 1 } ^ { e } \hat { \succeq } _ { p _ { u } ^ { n } } k _ { p _ { u } ^ { n } , 2 } ^ { s } \hat { \succeq } _ { p _ { u } ^ { n } } k _ { p _ { u } ^ { n } , 2 } ^ { e } \hat { \succeq } _ { p _ { u } ^ { n } } \hat  
$$

$$
k \in G
$$

$$
k ^ { s }
$$

$$
k ^ { e }
$$

$$
k ^ { s }
$$

$$
\hat { V }
$$

$$
k ^ { e }
$$

$$
\hat { G }
$$

$$
\hat { E }
$$

$$
k ^ { s }
$$

$$
k ^ { e }
$$

and $D _ { k ^ { e } } ^ { m a x } = D _ { k } ^ { m a x } - D _ { k } ^ { m i n }$ , respectively. Moreover, reserving $\sum _ { k } D _ { k } ^ { m i n }$ =PRBs can guarantee resources for steady WBANs, and the remaining $\begin{array} { r } { R = N - \sum _ { k } D _ { k } ^ { m i n } } \end{array}$ can be allocated to elaborate WBANs.

We follow the Deferred Acceptance Algorithm (DAA) for school admission problem [16], wherein a set of students apply for admission to a college having a maximum quota. A school has a quota of $D ^ { m a x }$ , keeps top $D ^ { m a x }$ students in a list, or all the applicants if the number of students is less than $D ^ { m a x }$ ; others get rejected. Further, rejected students apply to other schools that have never disqualified them. Thus, the school shortlists top $D ^ { m a x }$ students from the current list and previous waiting list. These steps continue until each student has exhausted the schools that s/he can apply for. In our case, we follow the scenario where UAV-PRB pairs propose and WBANs either accept or reject them as they must fulfill the minimum and maximum demand. Further, we transform minimum resource demand of WBANs into resource matching without the minimum resource demand using Algorithm 1 in the following.

1) Derived Resource Matching: Algorithm 1 transforms minimum resource demand of WBANs into resource matching without minimum resource demand. In the transformed matching, number of resources N remains unchanged, and preference lists of steady and elaborate WBANs remain the same as the original WBAN (line 5). The preference list of resource pairs is redefined by placing elaborate WBANs immediately after steady WBANs, preserving initial preference order (line 8). The resulting interference graph $\hat { G } ( \bar { V } , \hat { E } )$ includes steady and ( )elaborate nodes for each WBAN in G, inheriting all edges along with an edge between them to avoid sharing same PRB (lines 9-12). The output of Algorithm 1 is used as input of Algorithm 3.

```perl
Algorithm 2: Minimum Resource Requirement.
Input: $D _ { k } ^ { m i n } , \forall k \in \mathbb { K } , G ( V , E ) , \mathbb { K } , \mathbb { N } ,$ a set ${ \mathcal { L } } : = \phi .$
Output: $R .$
1: for all node $k \in G$ do
2: Create clique of size $D _ { k } ^ { m i n }$
3: Each node of clique $D _ { k } ^ { m i n }$ inherits all the edges of
$k \in G$ and a new graph $G ^ { \prime } ( V ^ { \prime } , E ^ { \prime } )$ is created w.r.t. the
(requirements of steady WBANs
4: while $V ^ { \prime }$ is not empty do
5: Remove a node $v _ { k }$ from $V ^ { \prime }$
6: Allocate resource $n \in \mathbb N$ , which is not allocated to any
one hop of $v _ { k }$
7: ${ \mathcal { L } } = { \mathcal { L } } \cup \{ n \}$
8: $R = N - | \mathcal { L } |$
```

2) Minimum Resource Requirement: Algorithm 2 evaluates the minimum required PRBs for steady and elaborate WBANs by applying the graph coloring technique. A virtual clique of size $D ^ { m i n }$ is generated to account for multiple PRB requests per WBAN and inherits all the original edges of $G ,$ resulting in a new graph $G ^ { \prime } ( V ^ { \prime } , E ^ { \prime } )$ . A vertex is selected and assigned ( )with a PRB that has not been assigned within one-hop distance of that vertex and updates in the set L (lines 4-7). This process iterates for all vertices in the graph. In the end, the set $\mathcal { L }$ contains all the required PRBs for steady WBANs, and R denotes the number of required PRBs for elaborate WBANs. The output of Algorithm 2 is used as input of Algorithm 3 in the following.

3) Resource Matching Algorithm: Algorithm 3 uses different rules for steady and elaborate WBANs to accept or reject a resource pair. Let $C _ { u , n }$ be the set of WBANs that a resource pair $p _ { u } ^ { n }$ has not yet applied. Line 1 initializes the required variables. In every round, each resource pair $p _ { u } ^ { n }$ selects a set of non-interfering WBANs $Z _ { u , n }$ (lines 3-4), and finds the Maximum Weighted Independent Set (MWIS) $Z _ { u , n } ^ { m a x }$ on the set $Z _ { u , n }$ (line 5). If $Z _ { u , n } ^ { m a x }$ becomes empty for all resource pairs, Algorithm 3 terminates (lines $6 \mathrm { - } 7 ) ;$ otherwise, WBAN adds the resource pair to its waiting list (lines 9-12). A WBAN with a non-empty waiting list selects its required $D _ { k ^ { s } } ^ { m a x }$ resources and resets its waiting list (lines 14-15).

Let cnt be counter to track the number of PRBs allocated to elaborate WBANs (line 17). Add each elaborate WBANâs matched resource to the waiting list and reset the matched resources (lines 18-19). If the number of PRBs allocated to elaborate WBANs is less than R, or there exists elaborate WBANs with a non-empty waiting list and do not fulfill their maximum demand, then WBAN $k ^ { e }$ selects its most preferred UAV-PRB pairs from the waiting list until the maximum demand is reached or its waiting list is empty (lines 20-25). The counter value increases by one and returns to line 20. Finally, the waiting list of WBAN k is set to empty (line 26). This process repeats for all the resource pairs with non-empty set $C _ { u , n }$ (lines 2-26). Therefore, we get the matching such as âk $\begin{array} { r } { \mathrm { : \in \mathbb { K } , } \mu ( k ) = \hat { \mu } ( k ^ { e } ) \cup \hat { \mu } ( k ^ { s } ) \mathrm { , } \forall p _ { u } ^ { n } \in \mathcal { P } . } \end{array}$ , if $k ^ { e } \in \hat { \mu } ( p _ { u } ^ { n } )$ or $k ^ { s } \in \hat { \mu } ( p _ { u } ^ { n } )$ ( )then $k \in \mu ( p _ { u } ^ { n } )$ Ë( ) Ë( ). Thus, the total revenue can be Ë( ) ( )calculated based on the matching $\hat { \mu }$ (line 27).

Algorithm 3: Resource Matching Algorithm.   
Input: Outputs of Algorithms 1 and $\overline { { 2 ; \Pi _ { k , u } , \Omega _ { u } , \mathcal { M } } } ,$   
$y _ { k , u } ^ { n } = 0 , \mathfrak { R } _ { k } , \mathrm { R } _ { u } , \forall k \in \mathbb { K } , \forall u \in \mathbb { U } , \forall n \in \mathbb { N }$   
= 0 ROutput: Resource matching $\hat { \mu } ,$ revenue $\mathcal { U } .$   
$1 \colon \forall k \in \hat { \mathbb { K } } , \hat { \mu } ( k ) = \phi ,$ Ë, waiting list $W _ { k } = \phi ; \forall p _ { u } ^ { n } \in \mathcal P ,$   
$\hat { \mu } ( p _ { u } ^ { n } ) = \phi ,$ ) = candidate list $C _ { u , n } = \hat { \mathbb { K } } , \hat { \mathbb { N } } = \mathbb { N }$   
Ë( )2: while $\exists C _ { u , n } \neq \phi$ do   
=3: for all resource pair $p _ { u } ^ { n }$ with $| C _ { u , n } | > 0$ do   
4: $Z _ { u , n } : = \mathrm { W B A N s }$ that satisfies $k \in C _ { u , n } ; \forall k ^ { \prime } \in$   
$\mu ( p _ { u } ^ { n } ) , e _ { k , k ^ { \prime } } = 0$   
5: ( ) Find MWIS on $Z _ { u , n }$ as $Z _ { u , n } ^ { m a x }$   
6: if $\forall p _ { u } ^ { n } , Z _ { u , n } ^ { m a x } = \phi$ then   
7: Return $\hat { \mu }$   
8: else   
9: for all $W B A N k \in Z _ { u , n } ^ { m a x }$ do   
10: if Constraints (28a) and (28b) are met then   
11: Resource $p _ { u } ^ { n }$ applies for WBAN k   
12: $C _ { u , n } = { C _ { u , n } } - \{ k \} , W _ { k } = W _ { k } \cup \{ p _ { u } ^ { n } \}$   
13: =for all WBAN k for which $W _ { k } \neq \phi$ do   
14: if $\boldsymbol { k } \in \mathbb { K } ^ { s }$ then   
15: k accepts $D _ { k } ^ { m a x }$ resources in $W _ { k } \cup \hat { \mu } ( k )$ , and set   
$W _ { k } = \phi , y _ { k , u } ^ { n ^ { - } } = 1$   
16: else   
17: c n t   
18: =for all $\boldsymbol { k } \in \hat { \mathbb { K } } ^ { e }$ do   
19: $W _ { k } = W _ { k } \cup \mu ( k ) , \mu ( k ) = \phi$   
20: =while cnt $< R a n d \exists k ^ { e } , W _ { k ^ { e } } \neq \phi$ and   
$| \hat { \mu } ( k ^ { e } ) | < \hat { D } _ { k ^ { e } } ^ { m a x }$ do   
21: $\mathbf { i f } \left| \mu ( k ^ { e } ) \right| < \hat { D } _ { k ^ { e } }$ and $W _ { k ^ { e } } \neq \phi$ then   
22: $k ^ { e }$ ( ) =selects its most preferred $p _ { u } ^ { n }$ in $W _ { k ^ { e } }$ , such   
that $\hat { \mu } ( k ^ { e } ) = \hat { \mu } ( k ^ { e } ) \cup \{ p _ { u } ^ { n } \}$   
23: $y _ { k , u } ^ { n } = 1$ ) = Ë( )for accepted resource pairs   
24: $\ddot { W _ { k ^ { e } } } = W _ { k ^ { e } } - \{ p _ { u } ^ { n } \}$   
25: $c n t = c n t + 1 , \hat { \mathbb { N } } = \hat { \mathbb { N } } - \{ n \}$   
26: $W _ { k } = \phi$   
=27: Calculate revenue U based on the matching $\hat { \mu }$

## B. Analysis of the Algorithms

We analyze the computational time complexity and the correctness of the proposed algorithm in the following.

Theorem 2: The computational time complexity of the proposed algorithm is $O ( N K ^ { 2 } U \hat { V } ^ { 3 } )$ .

( )Proof: The time complexity of Algorithm 1 is O KN U , and that of Algorithm 2 is $O ( K )$ ( ). In Algorithm 3, each steady ( )WBAN is approached by a UAV-PRB pair once, and N PRBs are allocated by examining the MWIS in the graph. To find out MWIS, each edge must be traversed, which takes $O ( \hat { E } )$ ( )time complexity. This process repeats for all vertices in the derived interference graph, resulting in $O ( \hat { V } \hat { E } )$ time complexity, $\mathrm { i . e . , } O ( \hat { V } ^ { 3 } )$ ( ). Moreover, the number of MWIS is bounded by ( )the total available PRBs, i.e., 100 [38]. Therefore, an approximate algorithm for MWIS takes ${ \cal O } ( \hat { V } ^ { 3 } )$ time complexity [38]. ( )Thus, the time complexity for allocating PRBs to each steady WBAN is ${ \cal O } ( K N \hat { V } ^ { \bar { 3 } } )$ . Further, to allocate PRBs to an elaborate ( )WBAN (lines 20-26 of Algorithm 3), all the remaining elaborate

<!-- image-->  
Fig. 4. Deployment scenario.

WBANs need to be visited, resulting in a time complexity of O K . Hence, time complexity of the proposed algorithm is $\dot { O ( N K ^ { 2 } U \hat { V } ^ { 3 } ) }$

( )Lemma 1: For every WBAN $k \in \mathbb { K }$ , the proposed algorithm produces an interference-free solution.

Proof: To avoid interference, proposed approach allocates different PRBs to WBANs within one-hop distance of interference graph. Algorithm 3 always examines already allocated PRBs within one hop of particular vertex in interference graph. This phenomenon is handled by finding the MWIS in the topology (line 5 of Algorithm 3). Thus, the proposed algorithm reuses the same PRBs only after one-hop distance in the topology to ensure an interference-free network. Thus, proposed algorithm gives an interference-free RA for every WBAN.

## VI. PERFORMANCE ANALYSIS

We evaluate the performance of our proposed algorithm using the publicly available Shanghai Telecom dataset [40], [41], which comprises data from 9481 mobile phone users across 3233 Base Stations (BSs). We select BSs within a 2000 m x 2000 m area to serve as UAVs, with additional UAVs randomly placed in the same area to densify the network and simulate a 5G environment. We randomly select [100-1000] mobile phones to act as WBANs, and Fig. 4 presents a snapshot of the system at a specific time stamp. Each UAV has a coverage radius of 200 m [42]. It is worth noting that acquiring real-time user data across their BSs in cellular networks is challenging since operators usually keep such information confidential. Computation capacity of UAVs is set to 2 GHz [3], and CPU cycles per bit for computing one data sample are uniformly chosen from [10-30] cycles. Physiological data size for WBANs ranges between [500-1000] MB, and FL model size is set to 1 MB [3] (see Table V). Minimum and maximum PRB demands of a WBAN ranges between [1-6]. Simulation is done using Python 3.9 on a Windows 10 PC with an Intel Core i7-10750H processor.

We compared our results with the existing works SSAA [21], CAA [22], and the Optimal value obtained using the Gurobi optimization tool [43], using the same simulation parameters. To the best of our knowledge, existing works SSAA and CAA are the closest works to our proposed architecture. Particularly, we compared our work with SSAA since it allocates channels to users while considering mutual interference and considers the maximum number of channels each IoT device can receive. In contrast, CAA allocates subchannels to IoT nodes using a matching theory-based approach. For a fair comparison, we considered IoT nodes in [21] and mobile users in [22] as WBANs.

TABLE V SIMULATION PARAMETERS
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>K, U, N [38]  $D _ { k } ^ { m i n } , D _ { k } ^ { m a x } \ [ 3 8 ]$   $\mathrm { B a n d w i d f h } [ 3 9 ] , \sigma$   $\mathrm { D e p l o y m e n t a r e a } \ [ 2 1 ]$   $\beta _ { u } , c _ { u } \ [ 3 ]$   $\rho _ { k } [ 2 8 ] , \alpha _ { u } [ 3 ] , \lambda _ { 1 } , \lambda _ { 2 } , d _ { k }$   $\epsilon _ { k } \ [ 3 ] , P _ { k } \ [ 3 6 ]$   $\chi , \pi _ { k } , \phi _ { u }$   $\mathrm { p } _ { u } , v , L , \varepsilon , \delta \left[ 3 \right]$ </td><td>[100-1000],[20-50],100 [1-6]  $2 0 \mathrm { M H z } , \mathrm { i } \mathrm { u n i t }$   $2 0 0 0 \ ( \mathrm { m } ) \times 2 0 0 0 \ ( \mathrm { m } )$   $[ 1 0 { - } 3 0 ] \mathrm { c y c l e s / b i t } , 2 \mathrm { G H z }$  [0-1],100000,0.5,0.5,437 [500-1000] MB,[1-10] dB 1 unit,1 unit, 1 unit  $[ 1 0 - 3 5 ] , 4 , 4 , \frac { 1 } { 3 } , \frac { 1 } { 4 }$   $[ 1 0 0 0 - 2 0 0 0 ] \ \mathrm { m } , [ 1 0 ^ { \circ } - 2 0 ^ { \circ } ] \ \mathrm { m } / \mathrm { s }$   $[ 8 \small { - } 1 8 ] , 1 0 ^ { - 2 8 } , 2 5 \mathrm { d B m }$   $0 . 6 , 2 4 , 1 \mathrm { M B } , 1 0 0 0 \mathrm { m } , 1 0 ^ { 8 }$ </td></tr></table>

<!-- image-->  
(a) Revenue (#UAV = 25)

<!-- image-->  
(b) Revenue (#WBAN = 1000)  
Fig. 5. Revenue analysis.

Revenue Analysis: Fig. 5(a) compares the total revenue of our proposed algorithm with SAA, CAA, and optimal in various scenarios. The proposed algorithm outperforms SSAA and CAA, achieving 92.8% of the optimal value compared to that of 86.6% and 76.6% for SSAA and CAA, respectively. The reason is that SSAA allocates resources to maximize the uplink capacity without considering the minimum required PRBs, while CAA only allows each user to have one resource. In contrast, the proposed algorithm reuses PRBs and assigns the best UAV-PRB pair, considering minimum and maximum PRB demand, resulting in higher revenue in polynomial time complexity. Moreover, the revenue becomes constant as the number of WBANs increases (beyond 800 WBANs) because no more demand of WBANs can be fulfilled without interfering with each other.

Fig. 5(b) compares total revenue of our proposed algorithm with SSAA, CAA, and optimal in various scenarios. As seen from the result, the revenue increases as the number of UAVs increases. The proposed algorithm achieves 93.6% to optimal value compared to 85.0% and 72.4% for SSAA and CAA, on an average. The reason is that with an increasing number of UAVs, the resources are allocated more efficiently in the network, considering minimum and maximum demands of WBANs. This leads to lower transmission time, resulting in lower energy costs and higher revenue. In contrast, SSAA allocates resources to maximize the uplink capacity without considering the minimum required resources, while CAA only allows each user to obtain a single resource, leading to lower performance. Moreover, the revenue becomes constant as the number of UAVs increases (beyond 80 UAVs) because adding more UAVs introduces more interference, and no more demand of WBANs can be fulfilled without interfering with each other.

<!-- image-->  
(a) Revenue vs.No.of WBANs

<!-- image-->  
(b) Revenue vs. accuracy

Fig. 6. Revenue based on number of WBANs and accuracy.  
<!-- image-->

<!-- image-->  
(a) Reuse ratio vs.WBANs  
(b) System data rate  
Fig. 7. Reuse ratio and system data rate analysis.

Fig. 6(a) presents three cases where the numbers of available PRBs are 80, 90, and 100, and the number of WBANs varies from 100 to 1000. The result shows that the revenue increases with an increase in the number of WBANs, indicating that more WBANsâ demands are met with the given PRBs, resulting in higher revenue. However, revenue growth slows down and becomes constant as number of WBANs increases beyond a certain point because meeting more WBANsâ demands lead to interference, negatively impacting revenue. Additionally, increasing number of PRBs allows more WBANsâ demands to be met, leading to lower transmission costs and higher revenue.

In Fig. 6(b), total revenue is compared for varying FL model accuracies, ranging from 0.1 to 0.9, indicating a gradual decrease in accuracy. Numbers of WBANs and UAVs are fixed at 500 and 50, respectively. The proposed algorithm achieves 93.6% of the optimal value, compared to that of 85.5% for SSAA and 71.5% for CAA, on an average. We also observe that revenue increases as desired accuracy decreases. The reason is that achieving lower accuracy requires fewer local iterations, which results in lower energy consumption and leads to higher revenue.

Reuse Ratio Analysis: We compare PRB reuse ratio of the proposed algorithm with SSAA, and CAA. PRB reuse ratio refers to the ratio of the number of PRB that are reused in the network, to the total number of available PRBs [39].

Fig. 7(a) analyzes the impact of the number of WBANs over PRB reuse ratio in the system. The proposed algorithm outperforms SSAA, and CAA in terms of PRB reuse ratio. The reason is that SSAA allocates the resources to maximize the uplink capacity without considering the minimum required PRB, while CAA allocates only one resource to each user without considering the number of PRB demand of WBANs. Further, PRB reuse ratio obtained by the proposed algorithm is lower than that of optimal because optimal solution considers all possible combinations of allocations and selects the best out of them.

System Data Rate Analysis: Fig. 7(b) compares the system data rate achieved by our proposed algorithm with SSAA, CAA, and optimal value. The proposed algorithm outperforms SSAA and CAA in terms of system data rate. The reason is that with an increasing number of UAVs, resources are allocated more efficiently in the network by considering interference among WBANs, leading to a higher data rate. The results also show that the system data rate increases with an increasing number of WBANs, indicating that more WBANsâ demands are met using the given PRBs. However, data rate becomes constant as number of WBANs increases beyond a certain point. This is because meeting more WBANsâ demands leads to interference, preventing further increases in data rate without interference.

<!-- image-->

<!-- image-->  
(a) Execution time  
(b) Prototype implementation

Fig. 8. Execution time and prototype model analysis.  
<!-- image-->  
Fig. 9. Prototype setup.

Execution Time Analysis: Fig. 8(a) compares the execution time of our proposed algorithm with SSAA, and CAA in various scenarios. As seen from the result, the execution time increases as the number of WBANs increases. The reason is that as the number of WBANs increases, the number of RA also increases, leading to longer execution times. We also observe that SSAA completes its execution faster than that of the proposed algorithm. However, the revenue obtained by SSAA is lower than that of the proposed algorithm (see Fig. 5). Moreover, CAA takes more time to complete its execution and has a higher rate of growth. Additionally, we did not consider the execution time of the optimal solution because it has a significantly higher execution time.

Prototype Model: We use a Workstation (WS) as the MBS, a UAV with a Raspberry Pi, and two mobile phones with pulse oximeter and Electrocardiogram (ECG) sensors as WBANs, as shown in Fig. 9. Moreover, the specification of each device in the prototype setup is given in Table VI. WS, mobile phones, and UAV are connected using 4G mobile hotspot connection. Pulse oximeter and ECG sensor collect physiological data from the patient and send it to mobile phone. Then, the UAV collects physiological data from the phones and performs FL training with the help of WS.

TABLE VI HARDWARE SPECIFICATIONS
<table><tr><td rowspan=1 colspan=1>Devices</td><td rowspan=1 colspan=1>Specification</td></tr><tr><td rowspan=1 colspan=1>Raspberry Pi</td><td rowspan=1 colspan=1>Model: Raspberry Pi4 Model B,SOC:Broadcom BCM2711,Cortex-A72 (ARM-v8) 64-bit SoC,CPU: 1.5 GHz 64-bit quad-core ARM Cortex- A72 CPU,RAM: 8GB LPDDR4 SDRAM,WiFi: Dual-band 802.11b/g/n/ac wireless LAN</td></tr><tr><td rowspan=1 colspan=1>Workstation</td><td rowspan=1 colspan=1>Model: Dell Precision 3640 Workstation,Processor: 11th generation Core-i7-10700 CPU (8 Core(s) @4.10 GHz,RAM:32 GB</td></tr><tr><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>Model: Phantom 4 Pro V2.0,5 direction obstacle sensing,1 inch 20 MP CMOS sensor</td></tr><tr><td rowspan=1 colspan=1>ECG sensor</td><td rowspan=1 colspan=1>Model: SanketLife Pro-Plus ECG sensor, 12-Lead ECG Monitor,Weight:120 gms,</td></tr><tr><td rowspan=1 colspan=1>Pulse sensor</td><td rowspan=1 colspan=1>Model: Pulse Oximeter,Operating Environment:+10oC~ +40C,Measurements: SpO2,Pulse rate,leth</td></tr><tr><td rowspan=1 colspan=1>Mobile</td><td rowspan=1 colspan=1>Model:SamsungGalaxyA22 5G,OneplusNord CE 5GRAM:8 GB,8GB&amp; Memory 128 GB,128 GBAndroid version:13,12</td></tr></table>

Fig. 8(b) compares the performance of the proposed model on physiological data sizes ranging from 0.33 MB to 2.35 MB. The results show that the revenue obtained in the simulation is higher than that of the prototype model because the prototype model used 4G mobile hotspot to transmit physiological data from the mobile devices to UAV, unlike the 5G communication used in the simulation. Moreover, the devices used in the prototype model are not dedicated same configured devices as considered in the simulation, which results in longer transmission times and higher energy costs compared to the 5G communication used in the simulation. We also observe that the curves for both implementations show similar results, indicating the applicability of the proposed model in real-world scenarios.

## VII. CONCLUSION AND FUTURE WORK

The article proposed a UAV-assisted WBAN-based FL framework underlying 5G network, where UAVs collected physiological data from WBANs and performed FL training. Formulated an optimization problem by maximizing the revenues of both WBANs and UAVs for providing physiological data and computational resources, respectively, via RA, as an NP-hard problem. Further, a matching and graph coloring-based efficient RA algorithm was applied to maximize the overall revenue, considering the minimum and the maximum PRB demand of WBANs. Extensive simulations and prototype results on real-world data demonstrated the effectiveness of the proposed model, achieving an average revenue of 92.8% of the optimal value compared to that of 86.6% and 76.6% for SSAA and CAA, respectively.

In the future, we aim to jointly optimize FL model and RA, considering FL task deadline, and address fairness in RA to ensure fair allocation of network resources to WBANs. Moreover, we intend to address the revenue maximization problem via RA as an online optimization problem. Additionally, we will explore FL model training while collecting data with the help of an MBS, considering hovering energy as well as flying and receiving energy of UAVs. Lastly, we plan to address the UAV placement problem to maximize the coverage area of UAVs.

## REFERENCES

[1] K.-J. Wu, Y.-W. P. Hong, and J. -P. Sheu, âColoring-based channel allocation for multiple coexisting wireless body area networks: A game-theoretic approach,â IEEE Trans. Mobile Comput., vol. 21, no. 1, pp. 63â75, Jan. 2022.

[2] Z. Ning et al., âMobile edge computing enabled 5G health monitoring for Internet of medical things: A decentralized game theoretic approach,â IEEE J. Sel. Areas Commun., vol. 39, no. 2, pp. 463â478, Feb. 2021.

[3] W. Y. B. Lim et al., âTowards federated learning in UAV-Enabled internet of vehicles: A multi-dimensional contract-matching approach,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 8, pp. 5140â5154, Aug. 2021.

[4] H. Zhang and L. Hanzo, âFederated learning assisted multi-UAV networks,â IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 14104â14109, Nov. 2020.

[5] F. Demrozi et al., âA low-cost wireless body area network for human activity recognition in healthy life and medical applications,â IEEE Trans. Emerg. Topics Comput., vol. 11, no. 4, pp. 839â850, Oct.-Dec. 2023.

[6] M. Abubaker and B. Babayigit, âDetection of cardiovascular diseases in ECG images using machine learning and deep learning methods,â IEEE Trans. Artif. Intell., vol. 4, no. 2, pp. 373â382, Apr. 2023.

[7] J. Andreu-Perez et al., âA generic deep learning based cough analysis system from clinically validated samples for point-of-need Covid-19 test and severity levels,â IEEE Trans. Serv. Comput., vol. 15, no. 3, pp. 1220â1232, May/Jun. 2022.

[8] B. McMahan et al., âCommunication-efficient learning of deep networks from decentralized data,â in Proc. Artif. Intell. Statist., 2017, pp. 1273â1282.

[9] A. Pratap and S. K. Das, âStable matching based resource allocation for service providerâs revenue maximization in 5G networks,â IEEE Trans. Mobile Comput., vol. 21, no. 11, pp. 4094â4110, Nov. 2022.

[10] Y.-S. Liang, W. -H. Chung, G. -K. Ni, I. -Y. Chen, H. Zhang, and S. -Y. Kuo, âResource allocation with interference avoidance in OFDMA femtocell networks,â IEEE Trans. Veh. Technol., vol. 61, no. 5, pp. 2243â2255, Jun. 2012.

[11] C. Chakraborty, B. Gupta, and S. K. Ghosh, âA review on telemedicinebased wban framework for patient monitoring,â Telemed. E-Health, vol. 19, no. 8, pp. 619â626, 2013.

[12] Y. Liu, J. Nie, X. Li, S. H. Ahmed, W. Y. B. Lim, and C. Miao, âFederated learning in the sky: Aerial-ground air quality sensing framework with UAV swarms,â IEEE Internet Things J., vol. 8, no. 12, pp. 9827â9837, Jun. 2021.

[13] Y. Chen, Y. Xiong, Q. Wang, X. Yin, and B. Li, âEnsuring minimum spectrum requirement in matching-based spectrum allocation,â IEEE Trans. Mobile Comput., vol. 17, no. 9, pp. 2028â2040, Sep. 2018.

[14] Y. Chen et al., âStable matching for spectrum market with guaranteed minimum requirement,â in Proc. 18th ACM Int. Symp. Mobile Ad hoc Netw. Comput., 2017, pp. 1â10.

[15] M. B. Singh et al., âBPFISH: Blockchain and privacy-preserving FL inspired smart healthcare,â 2022, arXiv:2207.11654.

[16] D. Gale et al., âCollege admissions and the stability of marriage,â Amer. Math. Monthly, vol. 69, no. 1, pp. 9â15, 1962.

[17] D. Fragiadakis, A. Iwasaki, P. Troyan, S. Ueda, and M. Yokoo, âStrategyproof matching with minimum quotas,â ACM Trans. Econ. Comput., vol. 4, no. 1, pp. 1â40, Jan. 2016. [Online]. Available: https://doi.org/10. 1145/2841226

[18] N. H. Tran, W. Bao, A. Zomaya, M. N. Nguyen, and C. S. Hong, âFederated learning over wireless networks: Optimization model design and analysis,â in Proc. IEEE Conf. Comput. Commun., 2019, pp. 1387â1395.

[19] S. Wang et al., âAdaptive federated learning in resource constrained edge computing systems,â IEEE J. Sel. Areas Commun., vol. 37, no. 6, pp. 1205â1221, Jun. 2019.

[20] M. S. Siraj et al., âIncentives to learn: A location-based federated learning model,â in Proc. Glob. Inf. Infrastructure Netw. Symp., 2022, pp. 40â45.

[21] R. Duan, J. Wang, C. Jiang, H. Yao, Y. Ren, and Y. Qian, âResource allocation for Multi-UAV aided IoT NOMA uplink transmission systems,â IEEE Internet Things J., vol. 6, no. 4, pp. 7025â7037, Aug. 2019.

[22] M. Dai, T. H. Luan, Z. Su, N. Zhang, Q. Xu, and R. Li, âJoint channel allocation and data delivery for UAV-Assisted cooperative transportation communications in post-disaster networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 16676â16689, Sep. 2022.

[23] N. N. Ei, M. Alsenwi, Y. K. Tun, Z. Han, and C. S. Hong, âEnergy-efficient resource allocation in Multi-UAV-Assisted two-stage edge computing for beyond 5G networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 16421â16432, Sep. 2022.

[24] S. Misra and S. Sarkar, âPriority-based time-slot allocation in wireless body area networks during medical emergency situations: An evolutionary game-theoretic perspective,â IEEE J. Biomed. Health Informat., vol. 19, no. 2, pp. 541â548, Mar. 2015.

[25] M. T. Arefin, M. H. Ali, and A. F. Haque, âWireless body area network: An overview and various applications,â J. Comput. Commun., vol. 5, no. 7, pp. 53â64, 2017.

[26] Y. Lu, S. Maharjan, and Y. Zhang, âAdaptive edge association for wireless digital twin networks in 6G,â IEEE Internet Things J., vol. 8, no. 22, pp. 16219â16230, Nov. 2021.

[27] A. Astrin, âIEEE Standard for Local and Metropolitan Area Networks - Part 15.6: Wireless Body Area Networks,â IEEE Std 802.15.6-2012, pp. 1â271, 2012.

[28] M. B. Singh, N. Taunk, N. K. Mall, and A. Pratap, âCriticality and utility-aware fog computing system for remote health monitoring,â IEEE Trans. Serv. Comput., vol. 16, no. 3, pp. 1738â1749, May/Jun. 2023.

[29] A. Hatoum, R. Langar, N. Aitsaadi, R. Boutaba, and G. Pujolle, âClusterbased resource management in OFDMA femtocell networks with QoS guarantees,â IEEE Trans. Veh. Technol., vol. 63, no. 5, pp. 2378â2391, Jun. 2014.

[30] C. Li et al., âHealthchain: Secure EMRs management and trading in distributed healthcare service system,â IEEE Internet Things J., vol. 8, no. 9, pp. 7192â7202, May 2021.

[31] N. Zhao, Z. Ye, Y. Pei, Y.-C. Liang, and D. Niyato, âMulti-agent deep reinforcement learning for task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Wireless Commun., vol. 21, no. 9, pp. 6949â6960, Sep. 2022.

[32] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[33] S. Li, Q. Ni, Y. Sun, G. Min, and S. Al-Rubaye, âEnergy-efficient resource allocation for industrial cyber-physical IoT systems in 5G ERA,â IEEE Trans. Ind. Inform., vol. 14, no. 6, pp. 2618â2628, Jun. 2018.

[34] M. B. Singh, H. Singh, and A. Pratap, âEnergy-efficient and privacy-preserving blockchain based federated learning for smart healthcare system,â IEEE Trans. Serv. Comput., to be published, doi: 10.1109/TSC.2023.3332955.

[35] X. Zhang, R. Lu, J. Shao, F. Wang, H. Zhu, and A. A. Ghorbani, âFed-Sky: An efficient and privacy-preserving scheme for federated mobile crowdsensing,â IEEE Internet Things J., vol. 9, no. 7, pp. 5344â5356, Apr. 2022.

[36] Z. Yang, M. Chen, W. Saad, C. S. Hong, and M. Shikh-Bahaei, âEnergy efficient federated learning over wireless communication networks,â IEEE Trans. Wireless Commun., vol. 20, no. 3, pp. 1935â1949, Mar. 2020.

[37] H. R. Lewis, R. M. Î Garey, and D. S. Johnson, âComputers and intractability. A guide to the theory of NP-completeness. WH Freeman and Company, San Francisco1979, x 338 pp.,â J. Symbolic Log., vol. 48, no. 2, pp. 498â500, 1983.

[38] A. Pratap, R. Gupta, V. S. S. Nadendla, and S. K. Das, âBandwidthconstrained task throughput maximization in IoT-enabled 5G networks,â Pervasive Mobile Comput., vol. 69, 2020, Art. no. 101281.

[39] A. Pratap, R. Misra, and S. K. Das, âMaximizing fairness for resource allocation in heterogeneous 5G networks,â IEEE Trans. Mobile Comput., vol. 20, no. 2, pp. 603â619, Feb. 2021.

[40] Y. Li, A. Zhou, X. Ma, and S. Wang, âProfit-aware edge server placement,â IEEE Internet Things J., vol. 9, no. 1, pp. 55â67, Jan. 2022.

[41] Shanghai Telecom, Shanghai, China, âThe distribution of 3233 base stations,â 2019. [Online]. Available: http://www.sguangwang.com/dataset/ telecom.zip

[42] X. Li et al., âA near-optimal UAV-Aided radio coverage strategy for dense urban areas,â IEEE Trans. Veh. Technol., vol. 68, no. 9, pp. 9098â9109, Sep. 2019.

[43] Gurobi Optimization, LLC, âGurobi optimizer reference manual,â 2022. [Online]. Available: https://www.gurobi.com

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Stable Matching Based Revenue Maximization for Federated Learning in UAV-Assisted WBANs/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Stable Matching Based Revenue Maximization for Federated Learning in UAV-Assisted WBANs/page_4_img_1.png|page_4_img_1]]
3. [[../extracted_images/Stable Matching Based Revenue Maximization for Federated Learning in UAV-Assisted WBANs/page_9_img_1.png|page_9_img_1]]
4. [[../extracted_images/Stable Matching Based Revenue Maximization for Federated Learning in UAV-Assisted WBANs/page_11_img_1.png|page_11_img_1]]

---

